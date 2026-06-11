"""Add an `existing_on_day` column to notes triage CSVs.

For each candidate date in notes_*_triage.csv, looks up what events
already cover that date in:
  - annotations.yaml (hand-curated + calendar-derived spans/markers)
  - labels_crash_v2.csv (research-derived crash episodes + dips)

Output: rewrites the CSVs in-place with the new column inserted
between `matched_keyword` and `keep_yn`. ALL existing user-entered
columns (keep_yn, event_label, category, loads, notes) are preserved
exactly.

Idempotent: re-running just overwrites the existing_on_day column
with fresh data; user input is never touched.
"""
from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TIMELINE_ROOT = HERE.parent
DATA = TIMELINE_ROOT / "data"
RESEARCH_ROOT = TIMELINE_ROOT.parent

ANNOTATIONS = DATA / "annotations.yaml"
LABELS_CSV = RESEARCH_ROOT / "garmin" / "hypotheses" / "crash_v2-definition" / "labels_crash_v2.csv"

NOTES_CSVS = [
    DATA / "notes_medical_triage.csv",
    DATA / "notes_overload_triage.csv",
    DATA / "notes_events_triage.csv",
]

# All CSVs whose y-marked rows have loads we want to surface back to the user
# during note-triage to avoid double-scoring the same day.
ALL_TRIAGE_CSVS = sorted(DATA.glob("calendar_*_triage.csv")) + sorted(DATA.glob("notes_*_triage.csv"))

ORDERED_FIELDS = [
    "date_start", "date_end", "score", "note_full",
    "matched_keyword",
    "existing_on_day",
    "keep_yn", "event_label", "category",
    "cognitive_load", "physical_load", "emotional_load", "notes",
]


def parse_date(s) -> date | None:
    if not s:
        return None
    if isinstance(s, date):
        return s
    try:
        return date.fromisoformat(str(s))
    except ValueError:
        return None


def load_annotations_index() -> tuple[list[dict], list[dict]]:
    if not ANNOTATIONS.exists():
        return [], []
    raw = yaml.safe_load(ANNOTATIONS.read_text(encoding="utf-8")) or {}
    spans = []
    for s in (raw.get("spans") or []):
        start = parse_date(s.get("start"))
        end = parse_date(s.get("end")) or start
        if start is None:
            continue
        spans.append({
            "start": start,
            "end": end,
            "label": (s.get("label") or "").strip(),
            "category": (s.get("category") or "").strip(),
        })
    markers = []
    for m in (raw.get("markers") or []):
        d = parse_date(m.get("date"))
        if d is None:
            continue
        markers.append({
            "date": d,
            "label": (m.get("label") or "").strip(),
            "category": (m.get("category") or "").strip(),
        })
    return spans, markers


def load_existing_loads_per_day() -> dict[date, list[dict]]:
    """Index of (calendar + notes) triage rows already marked y, by date.

    Each value is a list of dicts: {label, c, p, e} so we can show the user
    every label + load on that day during triage.
    """
    index: dict[date, list[dict]] = {}
    for csv_path in ALL_TRIAGE_CSVS:
        # Skip the file we're currently enriching (caller decides which CSVs
        # to skip via a separate filter; here we collect everything)
        try:
            rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
        except Exception:
            continue
        for r in rows:
            if (r.get("keep_yn") or "").strip().lower() != "y":
                continue
            d = parse_date(r.get("date_start"))
            if d is None:
                continue
            label_field = r.get("event_label") or r.get("title") or ""
            label = (label_field or "").strip() or "(unlabelled)"
            entry = {
                "label": label[:40],
                "c": (r.get("cognitive_load") or "").strip(),
                "p": (r.get("physical_load") or "").strip(),
                "e": (r.get("emotional_load") or "").strip(),
                "src": csv_path.stem,
            }
            index.setdefault(d, []).append(entry)
    return index


def load_crashes_dips() -> tuple[dict[date, str], dict[date, str]]:
    """Returns ({date -> episode_id_for_crash}, {date -> 'dip' marker})."""
    crashes_by_date: dict[date, str] = {}
    dips_by_date: dict[date, str] = {}
    if not LABELS_CSV.exists():
        return crashes_by_date, dips_by_date
    for r in csv.DictReader(LABELS_CSV.open(encoding="utf-8")):
        d = parse_date(r.get("date"))
        if d is None:
            continue
        label = (r.get("label") or "").strip()
        if label == "crash":
            ep = (r.get("episode_id") or "").strip()
            crashes_by_date[d] = ep or "crash"
        elif label == "dip":
            dips_by_date[d] = "dip"
    return crashes_by_date, dips_by_date


def existing_context_for(d: date, spans: list[dict], markers: list[dict],
                          crashes: dict[date, str], dips: dict[date, str],
                          loads_index: dict[date, list[dict]],
                          self_csv_stem: str,
                          umbrella_min_days: int = 30) -> str:
    """Returns a short string describing what already covers this date.

    Format: pipe-separated items. Each item shows either the
    annotation/research label or an already-triaged event with its load
    values. `self_csv_stem` is the file currently being enriched so its own
    y-rows are excluded (we surface OTHER files' loads, not the current
    file's own).
    """
    parts: list[str] = []

    # Research labels first (these are the most important "already on
    # timeline" markers — they should not be duplicated by notes events)
    if d in crashes:
        parts.append(f"CRASH ({crashes[d]})")
    if d in dips:
        parts.append("DIP")

    # Loads already assigned for this day from OTHER triage CSVs
    for entry in loads_index.get(d, []):
        if entry["src"] == self_csv_stem:
            continue
        loads = f"c{entry['c'] or '-'}/p{entry['p'] or '-'}/e{entry['e'] or '-'}"
        parts.append(f"{entry['label']} [{loads}]")

    # Markers (single-day biographical anchors)
    for m in markers:
        if m["date"] == d:
            parts.append(f"{m['label']}[{m['category']}]")

    # Spans that contain this date (only annotation-derived spans, no
    # double-listing with the loads_index above which captures the source
    # triage row directly)
    for s in spans:
        if s["start"] <= d <= s["end"]:
            length = (s["end"] - s["start"]).days + 1
            tag = " (umbrella)" if length >= umbrella_min_days else ""
            parts.append(f"{s['label']}[{s['category']}]{tag}")

    return " | ".join(parts) if parts else ""


def enrich_csv(csv_path: Path, spans: list[dict], markers: list[dict],
               crashes: dict[date, str], dips: dict[date, str],
               loads_index: dict[date, list[dict]]) -> tuple[int, int]:
    """Adds/refreshes the existing_on_day column. Returns (total_rows, n_with_existing)."""
    if not csv_path.exists():
        return 0, 0
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    n_with = 0
    self_stem = csv_path.stem
    for r in rows:
        d = parse_date(r.get("date_start"))
        if d is None:
            r["existing_on_day"] = ""
            continue
        ctx = existing_context_for(d, spans, markers, crashes, dips,
                                    loads_index, self_stem)
        r["existing_on_day"] = ctx
        if ctx:
            n_with += 1

    # Write back with consistent column order
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ORDERED_FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in ORDERED_FIELDS})

    return len(rows), n_with


def main():
    print("Loading existing annotations + research crash labels + prior loads...")
    spans, markers = load_annotations_index()
    crashes, dips = load_crashes_dips()
    loads_index = load_existing_loads_per_day()
    print(f"  {len(spans)} spans, {len(markers)} markers, "
          f"{len(crashes)} crash-days, {len(dips)} dip-days")
    print(f"  prior y-marked events across all triage CSVs: "
          f"{sum(len(v) for v in loads_index.values())} on {len(loads_index)} unique days")
    print()

    for csv_path in NOTES_CSVS:
        if not csv_path.exists():
            print(f"  skip (not found): {csv_path.name}")
            continue
        total, with_ctx = enrich_csv(csv_path, spans, markers, crashes, dips, loads_index)
        print(f"  {csv_path.name}: {total} rows | {with_ctx} have existing context "
              f"({with_ctx / max(total, 1) * 100:.0f}%)")


if __name__ == "__main__":
    main()
