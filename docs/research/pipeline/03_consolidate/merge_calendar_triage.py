"""Merge calendar triage CSV into annotations.yaml.

Reads the user-triaged calendar CSVs (keep_yn=y rows + per-event
cognitive/physical/emotional load 1-3 + notes) plus the hand-curated
narrative spans (external YAML), applies the agreed load to category
mapping, deduplicates, and writes a clean chronological
annotations.yaml.

Load to category mapping:
- any load = 3                       -> high_intensity
- max load = 2                       -> levensgebeurtenis
- all loads empty or 1               -> levensgebeurtenis (subtle)

Inputs (all external; resolved against $GEVOELSCORE_DATA_PATH):
- reviews/calendar_*_triage.csv       (user-triaged calendar feed)
- processed/manual_triage/triage_events.csv  (notes-triage-derived events)
- raw/directus_exports/hand_curated_spans.yaml  (PII narrative spans;
  markers + spans_pre_2022 + spans_post_2022)

Output:
- raw/directus_exports/annotations.yaml
"""
from __future__ import annotations

import csv
import os
import re
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
# docs/research/pipeline/03_consolidate -> ... -> repo root
REPO_ROOT = HERE.parent.parent.parent.parent


def _load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_env_file(REPO_ROOT / ".env")
_data_env = os.environ.get("GEVOELSCORE_DATA_PATH")
if not _data_env:
    raise SystemExit(
        "GEVOELSCORE_DATA_PATH not set (env var or .env at repo root). "
        "See .env.example."
    )

DATA_ROOT = Path(_data_env)
TRIAGE_DIR = DATA_ROOT / "reviews"
TRIAGE_EVENTS_CSV = DATA_ROOT / "processed" / "manual_triage" / "triage_events.csv"
HAND_CURATED_YAML = DATA_ROOT / "raw" / "directus_exports" / "hand_curated_spans.yaml"
ANNOTATIONS = DATA_ROOT / "raw" / "directus_exports" / "annotations.yaml"
GARMIN_ACTIVITIES_CSV = DATA_ROOT / "processed" / "garmin" / "activities.csv"

TRIAGE_CSVS = sorted(TRIAGE_DIR.glob("calendar_*_triage.csv"))

# Per-session activity types that get emitted as Garmin-derived single-day
# markers. Mapping: activity_type -> (label_prefix, default category).
# Other activity types in activities.csv (sailing_v2, incident_detected) are
# intentionally skipped.
ACTIVITY_TYPES_TO_LABEL = {
    "running": ("Running", "high_intensity"),
    "cycling": ("Cycling", "high_intensity"),
    "walking": ("Walking", "levensgebeurtenis"),
    "breathwork": ("Breathwork", "interventie"),
}


def _stringify_dates(entries: list[dict]) -> list[dict]:
    """YAML auto-converts bare ISO dates to datetime.date; convert back to
    ISO strings so the rest of the pipeline (which treats start/end/date as
    strings) is undisturbed."""
    for e in entries:
        for k, v in list(e.items()):
            if isinstance(v, date):
                e[k] = v.isoformat()
    return entries


def _load_hand_curated() -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    """Load PII-containing narrative spans from the external YAML.

    File schema:
      markers:         [{date, label, category, note}]
      spans_pre_2022:  [{start, end, label, category, note}]
      spans_post_2022: [{start, end, label, category, note}]
      daily_mentions:  [{start, end, label, category, note}]  single-day
                       medication/condition mentions extracted from
                       day_entries notes by a pre-Phase-C pipeline (now
                       defunct); preserved here so annotations.yaml stays
                       reproducible.
    """
    if not HAND_CURATED_YAML.exists():
        raise SystemExit(
            f"Missing hand-curated spans file: {HAND_CURATED_YAML}\n"
            "This file lives outside the repo (contains PII)."
        )
    doc = yaml.safe_load(HAND_CURATED_YAML.read_text(encoding="utf-8")) or {}
    return (
        _stringify_dates(list(doc.get("markers") or [])),
        _stringify_dates(list(doc.get("spans_pre_2022") or [])),
        _stringify_dates(list(doc.get("spans_post_2022") or [])),
        _stringify_dates(list(doc.get("daily_mentions") or [])),
    )


def clean_title(title: str) -> str:
    """Strip mojibake emoji-replacement bytes; keep readable text."""
    if not title:
        return ""
    # Common mojibake -> readable replacements
    replacements = {
        "ð": "",          # corrupted pin / party emoji
        "â¤ï¸": "",       # corrupted heart
        "ð¥³": "",        # corrupted party
        "Ã«": "e",         # corrupted e-umlaut (Australie)
        "Ã©": "e",
        "Ã¨": "e",
    }
    out = title
    for bad, good in replacements.items():
        out = out.replace(bad, good)
    # Strip orphan non-ASCII high-bit characters that survived mojibake
    out = "".join(ch for ch in out if (ord(ch) < 128 or ch.isalpha()))
    # Collapse repeated whitespace
    out = re.sub(r"\s+", " ", out).strip()
    return out


def parse_load(v: str) -> int | None:
    if v is None:
        return None
    v = v.strip()
    if v in ("", "y", "n"):  # accidental y/n in load columns
        return None
    try:
        n = int(v)
        if 1 <= n <= 3:
            return n
    except ValueError:
        pass
    return None


def map_category(cog: int | None, phy: int | None, emo: int | None) -> str:
    loads = [n for n in (cog, phy, emo) if n is not None]
    if not loads:
        return "levensgebeurtenis"
    mx = max(loads)
    if mx >= 3:
        return "high_intensity"
    return "levensgebeurtenis"


def load_summary(cog: int | None, phy: int | None, emo: int | None) -> str | None:
    parts = []
    if cog is not None:
        parts.append(f"cog={cog}")
    if phy is not None:
        parts.append(f"phy={phy}")
    if emo is not None:
        parts.append(f"emo={emo}")
    return "/".join(parts) if parts else None


def read_triage(csv_path: Path) -> list[dict]:
    """Read one triage CSV; return entries to add."""
    entries: list[dict] = []
    seen_titles: dict[tuple[str, str, str], int] = {}
    for r in csv.DictReader(csv_path.open(encoding="utf-8")):
        if (r.get("keep_yn") or "").strip().lower() != "y":
            continue
        title = clean_title(r.get("title", ""))
        if not title:
            continue
        start = (r.get("date_start") or "").strip()
        end = (r.get("date_end") or "").strip() or start
        cog = parse_load(r.get("cognitive_load", ""))
        phy = parse_load(r.get("physical_load", ""))
        emo = parse_load(r.get("emotional_load", ""))
        notes = (r.get("notes") or "").strip()
        # Skip duplicates within the CSV
        key = (start, end, title)
        if key in seen_titles:
            continue
        seen_titles[key] = 1

        category = map_category(cog, phy, emo)
        # Special-case: pinned "interventie" titles (the markers)
        title_lower = title.lower()
        if "ergotherapie" in title_lower or "fysiotherapie" in title_lower:
            category = "interventie"
        elif title_lower.startswith("huisarts") or "verwijzing" in title_lower:
            category = "medical"
        # Compose note
        # Per methodology §2a: loads are per-day, not per-multi-day-event.
        # Strip the `load:` prefix from multi-day spans so a generic per-event
        # rating does not get implicitly attributed to every day in the span.
        # The CSV row still carries the raw load values for traceability.
        is_multi_day = end and start and end != start
        note_parts = []
        loads_str = load_summary(cog, phy, emo)
        if loads_str and not is_multi_day:
            note_parts.append(f"load: {loads_str}")
        if notes:
            note_parts.append(notes)
        note = "; ".join(note_parts) if note_parts else None
        entries.append({
            "start": start,
            "end": end,
            "label": title,
            "category": category,
            "note": note,
        })
    return entries


def _opt_float(v: str | None) -> float | None:
    if v is None:
        return None
    s = v.strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def read_garmin_activities() -> list[dict]:
    """Emit one single-day marker per Garmin activity session for the types
    in ACTIVITY_TYPES_TO_LABEL. Label is a concise summary
    (e.g. 'Running, 38min, 6.2km, HR avg/max 144/166'); note carries the
    Garmin activity name plus a source tag for provenance.

    Note on the distance unit: the column is named `distance_m` in
    `activities.csv` (set by 02_extract_activities.py via
    `a.get('distance')`), but Garmin Connect returns distance in
    centimetres. Dividing by 100_000 converts to kilometres; verified
    against typical pace/speed for cycling and running.
    """
    if not GARMIN_ACTIVITIES_CSV.exists():
        return []
    markers: list[dict] = []
    for r in csv.DictReader(GARMIN_ACTIVITIES_CSV.open(encoding="utf-8")):
        atype = (r.get("activity_type") or "").strip().lower()
        if atype not in ACTIVITY_TYPES_TO_LABEL:
            continue
        date_str = (r.get("start_date") or "").strip()
        if not date_str:
            continue
        type_label, category = ACTIVITY_TYPES_TO_LABEL[atype]

        duration_min = _opt_float(r.get("duration_min"))
        avg_hr = _opt_float(r.get("avg_hr"))
        max_hr = _opt_float(r.get("max_hr"))
        distance_cm = _opt_float(r.get("distance_m"))

        parts = [type_label]
        if duration_min is not None:
            parts.append(f"{int(round(duration_min))}min")
        if distance_cm is not None and distance_cm > 0:
            distance_km = distance_cm / 100_000.0
            parts.append(f"{distance_km:.1f}km")
        if avg_hr is not None or max_hr is not None:
            avg_s = str(int(avg_hr)) if avg_hr is not None else "-"
            max_s = str(int(max_hr)) if max_hr is not None else "-"
            parts.append(f"HR avg/max {avg_s}/{max_s}")
        label = ", ".join(parts)

        name = (r.get("name") or "").strip()
        note_parts = []
        if name:
            note_parts.append(f"name: {name}")
        note_parts.append("source: garmin_activities_csv")
        note = "; ".join(note_parts)

        markers.append({
            "date": date_str,
            "label": label,
            "category": category,
            "note": note,
        })
    return markers


def read_triage_events(csv_path: Path) -> list[dict]:
    """Read triage_events.csv produced by process_triage_actions.py.

    Different column names from calendar triage CSVs: date_start/date_end/label
    + category override (not derived from loads) + source for provenance.
    """
    if not csv_path.exists():
        return []
    entries = []
    for r in csv.DictReader(csv_path.open(encoding="utf-8")):
        start = (r.get("date_start") or "").strip()
        end = (r.get("date_end") or "").strip() or start
        label = (r.get("label") or "").strip()
        if not start or not label:
            continue
        category = (r.get("category") or "levensgebeurtenis").strip()
        cog = parse_load(r.get("cognitive_load", ""))
        phy = parse_load(r.get("physical_load", ""))
        emo = parse_load(r.get("emotional_load", ""))
        loads_str = load_summary(cog, phy, emo)
        user_note = (r.get("note") or "").strip()
        source = (r.get("source") or "").strip()
        # Multi-day rule from methodology section 2b: only single-day events get loads in note
        is_multi_day = end and start and end != start
        note_parts = []
        if loads_str and not is_multi_day:
            note_parts.append(f"load: {loads_str}")
        if user_note:
            note_parts.append(user_note)
        if source:
            note_parts.append(f"source: {source}")
        note = "; ".join(note_parts) if note_parts else None
        entries.append({
            "start": start, "end": end,
            "label": label,
            "category": category,
            "note": note,
        })
    return entries


def main():
    (
        hand_curated_markers,
        hand_curated_spans_pre,
        hand_curated_spans_post,
        hand_curated_daily_mentions,
    ) = _load_hand_curated()

    # Gather all entries
    spans = list(hand_curated_spans_pre)

    # CSV-derived entries
    for csv_path in TRIAGE_CSVS:
        print(f"Reading {csv_path.name}...")
        new = read_triage(csv_path)
        print(f"  {len(new)} entries (keep_yn=y after dedupe)")
        spans.extend(new)

    spans.extend(hand_curated_spans_post)

    # Events extracted from triage notes (via process_triage_actions.py)
    triage_event_entries = read_triage_events(TRIAGE_EVENTS_CSV)
    if triage_event_entries:
        print(f"Reading {TRIAGE_EVENTS_CSV.name}...")
        print(f"  {len(triage_event_entries)} entries from triage-notes-derived events")
        spans.extend(triage_event_entries)

    # Daily mentions extracted by the (now-defunct) pre-Phase-C pipeline.
    # Appended last so stable-sort on `start` places them after same-day
    # triage_events entries, matching baseline ordering.
    spans.extend(hand_curated_daily_mentions)

    # Deduplicate spans by (start, end, label) — favouring earlier-added
    # (which prefers hand-curated over CSV-derived).
    deduped = []
    seen = set()
    for s in spans:
        key = (s.get("start"), s.get("end"), s.get("label", "").strip())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(s)

    # Sort chronologically
    def sort_key(s):
        d = s.get("start") or s.get("date")
        return d if d else "9999-12-31"
    deduped.sort(key=sort_key)

    # Garmin per-session activity markers (running + cycling + walking + breathwork)
    activity_markers = read_garmin_activities()
    if activity_markers:
        print(f"Reading {GARMIN_ACTIVITIES_CSV.name}...")
        print(f"  {len(activity_markers)} activity markers from activities.csv")

    markers_sorted = sorted(
        list(hand_curated_markers) + activity_markers,
        key=lambda m: m["date"],
    )

    header = (
        "# annotations.yaml - user-curated context for the research timeline.\n"
        "# Hand-curated entries (external YAML) + calendar-triage CSV + notes-triage CSV merged.\n"
        "# Re-render with: python docs/research/pipeline/03_consolidate/merge_calendar_triage.py\n\n"
    )
    # Build a single YAML document so quoting / escaping is handled correctly.
    doc = {
        "markers": [
            {k: v for k, v in m.items() if v is not None}
            for m in markers_sorted
        ],
        "spans": [
            {k: v for k, v in s.items() if v is not None}
            for s in deduped
        ],
    }
    body = yaml.safe_dump(doc, allow_unicode=True, sort_keys=False,
                          default_flow_style=False, width=120)
    ANNOTATIONS.write_text(header + body, encoding="utf-8")
    print(f"\nWrote {ANNOTATIONS}")
    print(f"Total spans: {len(deduped)}")
    print(f"Total markers: {len(markers_sorted)}")

    # Summary of CSV-derived categories
    csv_by_cat: dict[str, int] = {}
    for s in deduped:
        csv_by_cat[s["category"]] = csv_by_cat.get(s["category"], 0) + 1
    print("\nSpan categories:")
    for cat, n in sorted(csv_by_cat.items(), key=lambda kv: -kv[1]):
        print(f"  {cat:20} {n}")


if __name__ == "__main__":
    main()
