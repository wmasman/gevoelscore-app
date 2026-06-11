"""Prepare a hidden-dip review CSV from the quasi_crash_context buckets.

Reads:
  - data/triage_notes_classified_YYYY.csv (for each year)
  - data/sub_threshold_dips.csv (to exclude already-marked dips)
  - garmin/hypotheses/crash_v2-definition/labels_crash_v2.csv (to exclude
    days already labeled crash/dip)

Writes:
  - data/hidden_dip_review.csv

Output columns:
  date, score, year, original_note, triage_note, brainfog_mention,
  muscle_pain_mention, action_to_take, user_notes

Filters:
  - Only rows in bucket=quasi_crash_context
  - Score is included only when present in labels_crash_v2.csv
  - Excludes dates already in sub_threshold_dips.csv or labeled
    crash/dip in labels_crash_v2.csv

This is the operational input for Q2 (queued_work.md) and feeds the
training-label set for the §3a brainfog-hidden-dip hypothesis (Q1).
"""
from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
RESEARCH_ROOT = HERE.parent.parent

YEARS = [2022, 2023, 2024, 2025, 2026]
OUTPUT = DATA / "hidden_dip_review.csv"
SUB_DIPS = DATA / "sub_threshold_dips.csv"
LABELS_CRASH_V2 = RESEARCH_ROOT / "garmin" / "hypotheses" / "crash_v2-definition" / "labels_crash_v2.csv"

BRAINFOG_PATTERNS = re.compile(
    r"\b(brainfog|brain\s*fog|duf\s*hoofd|wazig\s*hoofd|wattenhoofd"
    r"|vergeetachtig|niet\s+helder|mistig\s+hoofd|hoofd\s+vol)\b",
    re.IGNORECASE,
)
MUSCLE_PAIN_PATTERNS = re.compile(
    r"\b(spierpijn|zere\s+benen|zwaar\s+in\s+de\s+benen|dof\s+gevoel"
    r"|spieren\s+pijn|zwaar\s+lichaam|stijf|stramme\s+spieren)\b",
    re.IGNORECASE,
)


def parse_iso(s):
    if not s:
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def load_excluded_dates() -> set[date]:
    """Dates already labeled as crash/dip in labels_crash_v2.csv or sub_threshold_dips."""
    excluded: set[date] = set()
    if LABELS_CRASH_V2.exists():
        for r in csv.DictReader(LABELS_CRASH_V2.open(encoding="utf-8")):
            d = parse_iso(r.get("date"))
            if d and r.get("label") in ("crash", "dip"):
                excluded.add(d)
    if SUB_DIPS.exists():
        for r in csv.DictReader(SUB_DIPS.open(encoding="utf-8")):
            d = parse_iso(r.get("date"))
            if d:
                excluded.add(d)
    return excluded


def main():
    excluded = load_excluded_dates()
    print(f"Excluded dates (already crash/dip): {len(excluded)}")

    all_candidates = []
    per_year = {}
    for year in YEARS:
        p = DATA / f"triage_notes_classified_{year}.csv"
        if not p.exists():
            continue
        for r in csv.DictReader(p.open(encoding="utf-8")):
            if r.get("bucket") != "quasi_crash_context":
                continue
            d = parse_iso(r.get("date"))
            if d is None or d in excluded:
                continue
            triage_note = (r.get("triage_note") or "").strip()
            original_note = (r.get("original_note") or "").strip()
            score = (r.get("score") or "").strip()
            brainfog = bool(BRAINFOG_PATTERNS.search(original_note) or BRAINFOG_PATTERNS.search(triage_note))
            muscle = bool(MUSCLE_PAIN_PATTERNS.search(original_note) or MUSCLE_PAIN_PATTERNS.search(triage_note))
            all_candidates.append({
                "date": d.isoformat(),
                "year": year,
                "score": score,
                "brainfog_mention": "y" if brainfog else "",
                "muscle_pain_mention": "y" if muscle else "",
                "original_note": original_note[:200],
                "triage_note": triage_note[:160],
                "action_to_take": "",
                "user_notes": "",
            })
            per_year[year] = per_year.get(year, 0) + 1

    all_candidates.sort(key=lambda r: r["date"])

    fields = ["date", "year", "score", "brainfog_mention", "muscle_pain_mention",
              "original_note", "triage_note", "action_to_take", "user_notes"]
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in all_candidates:
            w.writerow(r)

    print(f"\nWrote {OUTPUT}")
    print(f"  Total candidates: {len(all_candidates)}")
    print("  Per year:")
    for y in YEARS:
        print(f"    {y}: {per_year.get(y, 0)}")
    # Brainfog / muscle stats
    bf = sum(1 for r in all_candidates if r["brainfog_mention"])
    mp = sum(1 for r in all_candidates if r["muscle_pain_mention"])
    print(f"  With brainfog mention: {bf}")
    print(f"  With muscle-pain mention: {mp}")


if __name__ == "__main__":
    main()
