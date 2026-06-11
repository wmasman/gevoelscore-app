"""Prepare reintegration_gaps.csv for user review in a Google Sheet.

Reads:  data/reintegration_gaps.csv (gap_type / date_start / date_end / length / context / overlap)
Writes: data/reintegration_gaps_review.csv (review-ready format)

The review file adds:
  - suggested_action  (what we propose based on gap_type + context)
  - action_to_take    (empty, user fills: add_event / mark_dip / add_cog_load:N / skip / other)
  - notes             (empty, user fills with any clarification)

Also pulls the gevoelscore for each date (from labels_crash_v2.csv) so
the user can see the score context without leaving the sheet.
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
RESEARCH_ROOT = HERE.parent.parent

INPUT = DATA / "reintegration_gaps.csv"
OUTPUT = DATA / "reintegration_gaps_review.csv"
LABELS_CSV = RESEARCH_ROOT / "garmin" / "hypotheses" / "crash_v2-definition" / "labels_crash_v2.csv"
REINTEG_CSV = DATA / "reintegration_hours_2022-2024.csv"


def parse_iso(s):
    if not s:
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def load_scores() -> dict[date, str]:
    out: dict[date, str] = {}
    if not LABELS_CSV.exists():
        return out
    for r in csv.DictReader(LABELS_CSV.open(encoding="utf-8")):
        d = parse_iso(r.get("date"))
        if d and r.get("score"):
            out[d] = r["score"]
    return out


def load_pwc_notes() -> dict[date, str]:
    out: dict[date, str] = {}
    if not REINTEG_CSV.exists():
        return out
    for r in csv.DictReader(REINTEG_CSV.open(encoding="utf-8")):
        d = parse_iso(r.get("date"))
        if d:
            out[d] = (r.get("toelichting") or "")
    return out


SUGGESTIONS = {
    "illness_stretch": (
        "Confirm if this multi-day illness was a PEM dip/crash period "
        "(if it overlaps with existing labels, likely already covered). "
        "If yes and not yet marked: action `mark_dip` for the worst day. "
        "If no (just a regular cold/virus): action `skip`."
    ),
    "work_heavy_no_load": (
        "Day with 4+ work hours but no cog_load in per_day_intensity. "
        "Suggested: action `add_cog_load:N` with N = 1 (light), 2 (moderate), "
        "or 3 (heavy) based on the PwC note context. If the day was a "
        "vacation or admin-only day, action `skip`."
    ),
    "doctor_visit_missing": (
        "Doctor visit (bedrijfsarts / huisarts / casemanager / ergotherapeut) "
        "not in annotations. Suggested: action `add_event` with category "
        "`medical`. If it was a brief phone-only check-in, action `skip`."
    ),
}


def main():
    if not INPUT.exists():
        print(f"ERROR: {INPUT} does not exist. Run cross_validate_with_intensity.py first.")
        return 1

    scores = load_scores()
    pwc_notes = load_pwc_notes()

    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    out_rows = []
    for r in rows:
        d_start = parse_iso(r.get("date_start"))
        # Score for the day (or "" if no score yet, e.g. pre-2022-09-03)
        score = scores.get(d_start, "") if d_start else ""
        pwc_note = pwc_notes.get(d_start, "")
        out_rows.append({
            "gap_type": r.get("gap_type", ""),
            "date_start": r.get("date_start", ""),
            "date_end": r.get("date_end", ""),
            "length": r.get("length", ""),
            "score": score,
            "context": r.get("context", ""),
            "pwc_note": pwc_note,
            "overlap_with_existing": r.get("overlap_with_existing", ""),
            "suggested_action": SUGGESTIONS.get(r.get("gap_type", ""), ""),
            "action_to_take": "",  # USER FILLS
            "notes": "",            # USER FILLS
        })

    # Sort by gap_type then by date so similar gaps cluster
    bucket_order = ["illness_stretch", "doctor_visit_missing", "work_heavy_no_load"]
    out_rows.sort(key=lambda r: (
        bucket_order.index(r["gap_type"]) if r["gap_type"] in bucket_order else 99,
        r["date_start"],
    ))

    fields = ["gap_type", "date_start", "date_end", "length", "score",
              "context", "pwc_note", "overlap_with_existing",
              "suggested_action", "action_to_take", "notes"]
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print(f"Wrote {OUTPUT}")
    print(f"  Total rows: {len(out_rows)}")
    from collections import Counter
    counts = Counter(r["gap_type"] for r in out_rows)
    for k, v in counts.most_common():
        print(f"    {k}: {v}")


if __name__ == "__main__":
    raise SystemExit(main())
