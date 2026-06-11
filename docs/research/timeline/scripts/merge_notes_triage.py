"""Merge notes-triage CSVs into annotations.yaml.

Reads:
  - notes_medical_triage.csv
  - notes_overload_triage.csv
  - notes_events_triage.csv

Applies same load -> category mapping as merge_calendar_triage.py, with one
addition: user can OVERRIDE the category by filling the `category` column
explicitly (e.g. "medical" for a one-off medical event, "interventie" for
a treatment span). If category is empty, the load mapping decides.

Output: appends to the existing annotations.yaml. Does NOT touch the
hand-curated entries or the calendar-CSV-derived entries; this is a
separate top-up layer.

To keep one single source of truth for annotations, this script is
designed to be COMPLEMENTARY to merge_calendar_triage.py: run that first
to lay down the base, then run this to add notes-derived entries.

Re-run safe: deduplicates against the existing annotations.yaml by
(start, end, label).
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TIMELINE_ROOT = HERE.parent
DATA = TIMELINE_ROOT / "data"
ANNOTATIONS = DATA / "annotations.yaml"

NOTES_CSVS = [
    ("medical", DATA / "notes_medical_triage.csv"),
    ("overload", DATA / "notes_overload_triage.csv"),
    ("events", DATA / "notes_events_triage.csv"),
]

# Default category per topic if user does not override and no loads given
TOPIC_DEFAULT_CATEGORY = {
    "medical": "medical",
    "overload": "high_intensity",  # overload days are by definition high intensity
    "events": "levensgebeurtenis",
}


def parse_load(v):
    if v is None:
        return None
    v = (v or "").strip()
    if v in ("", "y", "n"):
        return None
    try:
        n = int(v)
        if 1 <= n <= 3:
            return n
    except ValueError:
        pass
    return None


def map_category(cog, phy, emo, override: str | None, topic_default: str) -> str:
    """Apply the same logic as merge_calendar_triage.py with topic-default fallback."""
    if override and override.strip():
        return override.strip()
    loads = [n for n in (cog, phy, emo) if n is not None]
    if not loads:
        return topic_default
    mx = max(loads)
    if mx >= 3:
        return "high_intensity"
    return "levensgebeurtenis" if topic_default not in ("medical", "interventie") else topic_default


def load_summary(cog, phy, emo) -> str | None:
    parts = []
    if cog is not None:
        parts.append(f"cog={cog}")
    if phy is not None:
        parts.append(f"phy={phy}")
    if emo is not None:
        parts.append(f"emo={emo}")
    return "/".join(parts) if parts else None


def read_topic_csv(csv_path: Path, topic: str) -> list[dict]:
    if not csv_path.exists():
        return []
    out = []
    for r in csv.DictReader(csv_path.open(encoding="utf-8")):
        if (r.get("keep_yn") or "").strip().lower() != "y":
            continue
        start = (r.get("date_start") or "").strip()
        end = (r.get("date_end") or "").strip() or start
        label = (r.get("event_label") or "").strip()
        if not label:
            # If user marked y but did not provide a label, fall back to a
            # short slice of the note for traceability.
            note_full = (r.get("note_full") or "").strip()
            label = note_full[:50] + ("..." if len(note_full) > 50 else "")
        cog = parse_load(r.get("cognitive_load", ""))
        phy = parse_load(r.get("physical_load", ""))
        emo = parse_load(r.get("emotional_load", ""))
        override = (r.get("category") or "").strip()
        topic_default = TOPIC_DEFAULT_CATEGORY[topic]
        category = map_category(cog, phy, emo, override, topic_default)
        loads_str = load_summary(cog, phy, emo)
        user_notes = (r.get("notes") or "").strip()
        note_full = (r.get("note_full") or "").strip()
        # Per methodology §2a: strip load: prefix for multi-day spans.
        # See merge_calendar_triage.py for the same rule.
        is_multi_day = end and start and end != start
        # Note body: load summary + user note + original day entry note (truncated)
        note_parts = []
        if loads_str and not is_multi_day:
            note_parts.append(f"load: {loads_str}")
        if user_notes:
            note_parts.append(user_notes)
        if note_full:
            note_parts.append(f"note: \"{note_full[:200]}{'...' if len(note_full) > 200 else ''}\"")
        note = "; ".join(note_parts) if note_parts else None
        out.append({
            "start": start,
            "end": end,
            "label": label,
            "category": category,
            "note": note,
            "source": f"notes:{topic}",
        })
    return out


def main():
    if not ANNOTATIONS.exists():
        print(f"ERROR: {ANNOTATIONS} does not exist. Run merge_calendar_triage.py first.")
        return 1

    # Load existing annotations to dedupe against
    raw = yaml.safe_load(ANNOTATIONS.read_text(encoding="utf-8"))
    spans = raw.get("spans") or []
    markers = raw.get("markers") or []
    existing_keys = set()
    for s in spans:
        key = (str(s.get("start", "")), str(s.get("end", "")), (s.get("label") or "").strip())
        existing_keys.add(key)

    # Read all topic CSVs
    new_spans = []
    for topic, csv_path in NOTES_CSVS:
        rows = read_topic_csv(csv_path, topic)
        print(f"  {topic:10}: {len(rows)} new entries from {csv_path.name}")
        new_spans.extend(rows)

    # Deduplicate against existing + within new batch
    deduped = []
    seen = set(existing_keys)
    for s in new_spans:
        key = (s["start"], s["end"], s["label"].strip())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(s)

    # Append to spans
    spans.extend({
        "start": s["start"],
        "end": s["end"],
        "label": s["label"],
        "category": s["category"],
        "note": s["note"],
    } for s in deduped)

    # Re-sort
    def sort_key(s):
        return s.get("start") or s.get("date") or "9999-12-31"
    spans.sort(key=sort_key)

    # Write back
    header = (
        "# annotations.yaml - user-curated context for the research timeline.\n"
        "# Hand-curated entries + calendar-triage CSV + notes-triage CSV merged.\n"
        "# Re-render with: python docs/research/timeline/scripts/build_timeline.py\n\n"
    )
    doc = {
        "markers": markers,
        "spans": [{k: v for k, v in s.items() if v is not None} for s in spans],
    }
    body = yaml.safe_dump(doc, allow_unicode=True, sort_keys=False,
                          default_flow_style=False, width=120)
    ANNOTATIONS.write_text(header + body, encoding="utf-8")
    print(f"\nWrote {ANNOTATIONS}")
    print(f"  Total spans now: {len(spans)}")
    print(f"  Total markers: {len(markers)}")
    print(f"  New entries added from notes: {len(deduped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
