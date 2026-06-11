"""Build per-day intensity triage CSVs (one per year).

For each year, lists every day that has either a gevoelscore (from
day_entries) or a notes entry or an annotation event. Pre-fills the
per-day load suggestion from per-event loads where they exist
(showing the source events so the user can decide), and flags days
needing manual consolidation or fresh assignment.

This is the statistical scaffolding the future qualitative + stat
work depends on. The output CSVs are designed to be triaged in
Google Sheets like the calendar/notes triage CSVs.

CSV columns:
  date
  score                            (gevoelscore on that day; read-only)
  note_full                        (day_entries.note text; read-only)
  events_on_day                    (label[c/p/e] | label[c/p/e] | ...; read-only)
  existing_max_cog/phy/emo         (MAX over per-event loads as pre-fill suggestion)
  needs_consolidation              (Y if 2+ load-bearing events on this day)
  no_loads_yet                     (Y if no per-event loads cover this day)
  cog_load / phy_load / emo_load   (USER assigns the unified per-day score)
  notes                            (USER adds context if useful)

Output: docs/research/timeline/data/per_day_intensity_YYYY.csv per year.
"""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TIMELINE_ROOT = HERE.parent
DATA = TIMELINE_ROOT / "data"
RESEARCH_ROOT = TIMELINE_ROOT.parent

ANNOTATIONS = DATA / "annotations.yaml"
NOTES_JSON = RESEARCH_ROOT / "notes" / "01-language-around-crashes" / "day_entries_with_notes.json"
PER_DAY_INTENSITY = DATA / "per_day_intensity.csv"

YEARS_TO_GENERATE = [2022, 2023, 2024, 2025, 2026]

FIELDS = [
    "date", "score", "note_full", "events_on_day",
    "existing_max_cog", "existing_max_phy", "existing_max_emo",
    "needs_consolidation", "no_loads_yet",
    "already_triaged",
    "cog_load", "phy_load", "emo_load", "notes",
]


def load_per_day_intensity() -> dict[date, dict]:
    """Load existing per-day intensity entries so already-triaged dates are
    pre-filled rather than re-asked."""
    if not PER_DAY_INTENSITY.exists():
        return {}
    out = {}
    for r in csv.DictReader(PER_DAY_INTENSITY.open(encoding="utf-8")):
        d = parse_date(r.get("date"))
        if d is None:
            continue
        out[d] = {
            "cog": (r.get("cog") or "").strip(),
            "phy": (r.get("phy") or "").strip(),
            "emo": (r.get("emo") or "").strip(),
            "source": (r.get("source") or "").strip(),
            "notes": (r.get("notes") or "").strip(),
        }
    return out


def parse_date(s) -> date | None:
    if not s:
        return None
    if isinstance(s, date):
        return s
    try:
        return date.fromisoformat(str(s))
    except ValueError:
        return None


def parse_loads_from_note(note: str) -> tuple[int | None, int | None, int | None]:
    if not note:
        return None, None, None
    cm = re.search(r"\bcog\s*=\s*(\d)", note, re.IGNORECASE)
    pm = re.search(r"\bphy\s*=\s*(\d)", note, re.IGNORECASE)
    em = re.search(r"\bemo\s*=\s*(\d)", note, re.IGNORECASE)
    c = int(cm.group(1)) if cm else None
    p = int(pm.group(1)) if pm else None
    e = int(em.group(1)) if em else None
    return c, p, e


def clean_ascii(s: str) -> str:
    return re.sub(r'[^\x20-\x7e]', '', s or '').strip()


def load_annotations() -> list[dict]:
    if not ANNOTATIONS.exists():
        return []
    raw = yaml.safe_load(ANNOTATIONS.read_text(encoding="utf-8")) or {}
    out = []
    for s in (raw.get("spans") or []):
        start = parse_date(s.get("start"))
        end = parse_date(s.get("end")) or start
        if start is None:
            continue
        c, p, e = parse_loads_from_note(s.get("note") or "")
        out.append({
            "start": start, "end": end,
            "label": (s.get("label") or "").strip(),
            "category": (s.get("category") or "").strip(),
            "c": c, "p": p, "e": e,
        })
    return out


def load_notes_by_date() -> dict[date, dict]:
    if not NOTES_JSON.exists():
        return {}
    data = json.loads(NOTES_JSON.read_text(encoding="utf-8"))
    out = {}
    for r in data:
        d = parse_date(r.get("date"))
        if d is None:
            continue
        out[d] = {
            "score": r.get("score", ""),
            "note": (r.get("note") or "").strip(),
        }
    return out


def events_per_day_index(spans: list[dict],
                          umbrella_min_days: int = 30) -> dict[date, list[dict]]:
    """For each date, list events (excluding long umbrellas) that touch it.

    Umbrellas are excluded from the per-day events list so the day's load
    is driven by point-events, not by ambient umbrella context. Umbrellas
    still appear in the events_on_day column for user awareness, but they
    do not contribute to MAX(loads) suggestions.
    """
    index: dict[date, list[dict]] = defaultdict(list)
    for ev in spans:
        length = (ev["end"] - ev["start"]).days + 1
        is_umbrella = length >= umbrella_min_days
        d = ev["start"]
        while d <= ev["end"]:
            ev_copy = {**ev, "is_umbrella": is_umbrella}
            index[d].append(ev_copy)
            d += timedelta(days=1)
    return index


def build_year_csv(year: int, spans: list[dict],
                    notes_by_date: dict[date, dict],
                    events_index: dict[date, list[dict]],
                    per_day_intensity: dict[date, dict]) -> tuple[int, int, int, int]:
    """Returns (n_rows, n_needs_consolidation, n_no_loads_yet, n_already_triaged)."""
    out_rows = []
    n_consol = 0
    n_no_loads = 0
    n_already = 0
    d = date(year, 1, 1)
    end_y = date(year, 12, 31)
    while d <= end_y:
        events_today = events_index.get(d, [])
        has_score = d in notes_by_date
        if not events_today and not has_score:
            d += timedelta(days=1)
            continue

        # Build events_on_day display (events sorted: umbrellas last for
        # readability)
        ev_display = []
        load_events = [ev for ev in events_today
                       if not ev["is_umbrella"]
                       and any(x is not None for x in (ev["c"], ev["p"], ev["e"]))]
        for ev in events_today:
            loads_str = (
                f"c{ev['c'] if ev['c'] is not None else '-'}"
                f"/p{ev['p'] if ev['p'] is not None else '-'}"
                f"/e{ev['e'] if ev['e'] is not None else '-'}"
            )
            tag = "[umbrella]" if ev["is_umbrella"] else ""
            ev_display.append(f"{clean_ascii(ev['label'])[:40]} {loads_str}{tag}")
        events_on_day = " | ".join(ev_display)

        # MAX over per-event loads (only point-events, not umbrellas)
        cs = [ev["c"] for ev in load_events if ev["c"] is not None]
        ps = [ev["p"] for ev in load_events if ev["p"] is not None]
        es = [ev["e"] for ev in load_events if ev["e"] is not None]
        max_c = max(cs) if cs else ""
        max_p = max(ps) if ps else ""
        max_e = max(es) if es else ""

        needs_consol = "Y" if len(load_events) >= 2 else ""
        no_loads_yet = "Y" if not load_events else ""

        if needs_consol == "Y":
            n_consol += 1
        if no_loads_yet == "Y":
            n_no_loads += 1

        info = notes_by_date.get(d, {})

        # Pre-fill from per_day_intensity.csv if already triaged
        existing_decision = per_day_intensity.get(d)
        already = "Y" if existing_decision else ""
        if already:
            n_already += 1

        out_rows.append({
            "date": d.isoformat(),
            "score": info.get("score", ""),
            "note_full": info.get("note", "").replace("\n", " ").strip(),
            "events_on_day": events_on_day,
            "existing_max_cog": max_c,
            "existing_max_phy": max_p,
            "existing_max_emo": max_e,
            "needs_consolidation": needs_consol,
            "no_loads_yet": no_loads_yet,
            "already_triaged": already,
            "cog_load": existing_decision["cog"] if existing_decision else "",
            "phy_load": existing_decision["phy"] if existing_decision else "",
            "emo_load": existing_decision["emo"] if existing_decision else "",
            "notes": existing_decision["notes"] if existing_decision else "",
        })
        d += timedelta(days=1)

    out_path = DATA / f"per_day_intensity_{year}.csv"
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)
    return len(out_rows), n_consol, n_no_loads, n_already


def main():
    print("Loading annotations + day entries + existing per-day intensity...")
    spans = load_annotations()
    notes_by_date = load_notes_by_date()
    events_index = events_per_day_index(spans)
    per_day_intensity = load_per_day_intensity()
    print(f"  {len(spans)} spans loaded; {len(notes_by_date)} day-notes loaded")
    print(f"  {len(events_index)} dates covered by at least one span")
    print(f"  {len(per_day_intensity)} existing per-day intensity entries (pre-fill source)")
    print()

    print("Building per-year per-day intensity triage CSVs...")
    for year in YEARS_TO_GENERATE:
        n, consol, no_loads, already = build_year_csv(
            year, spans, notes_by_date, events_index, per_day_intensity
        )
        if n == 0:
            print(f"  per_day_intensity_{year}.csv: 0 rows (no data)")
            continue
        print(f"  per_day_intensity_{year}.csv: {n} rows "
              f"| {already} already triaged | {consol} multi-event | {no_loads} no loads yet")


if __name__ == "__main__":
    main()
