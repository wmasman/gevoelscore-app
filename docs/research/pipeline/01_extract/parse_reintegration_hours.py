"""Parse PwC reintegration daily hours into a clean per-day CSV.

Reads:  data/raw_pwc_uren.csv (the raw spreadsheet text, manually saved)
Writes: data/reintegration_hours_2022-2024.csv

Output columns:
  date           ISO date
  week           ISO week number
  primary_hours  numeric (or empty)
  secondary_hours numeric (or empty)
  total_hours    numeric
  illness_flag   1 if 'ziek' / 'niet lekker' / 'corona' / 'voelde mij niet goed'
  doctor_visit_flag  1 if 'bedrijfsarts' / 'huisarts' / 'casemanager' /
                     'ergotherapeut' / 'job coach' / 'jobcoaching'
  amsterdam_flag 1 if 'naar amsterdam' / 'naar kantoor amsterdam'
  vacation_flag  1 if 'vakantie' / 'vrij' / 'kerstvakantie' / 'herfstvakantie'
  source_tab     'oud' (Sep 2022 - Aug 2023) or 'nieuw' (Oct 2023 - Feb 2024)
  toelichting    raw user note for the day

The source CSV has two tabs concatenated: the 'oud' tab is the original
2022-2023 reintegration log; 'nieuw' is the resumed 2023-2024 log after
the Sep-Oct 2023 gap. Both share the same column layout.
"""
from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
INPUT = DATA / "raw_pwc_uren.csv"
OUTPUT = DATA / "reintegration_hours_2022-2024.csv"

ILLNESS_PATTERNS = re.compile(
    r"\b(ziek|niet\s*lekker|corona|voelde\s+mij\s+niet\s+goed|erg\s+moe|keelpijn"
    r"|hoofdpijn|slechte\s+dag)\b",
    re.IGNORECASE,
)
DOCTOR_PATTERNS = re.compile(
    r"\b(bedrijfsarts|huisarts|casemanager|ergotherapeut|jobcoach|job\s+coach"
    r"|jobcoaching|dockters\s+visit|keuringsgesprek)\b",
    re.IGNORECASE,
)
AMSTERDAM_PATTERNS = re.compile(
    r"\b(naar\s+amsterdam|kantoor\s+amsterdam|naar\s+kantoor|op\s+kantoor)\b",
    re.IGNORECASE,
)
VACATION_PATTERNS = re.compile(
    r"\b(vakantie|herfstvakantie|kerstvakantie|^\s*vrij\s*$)\b",
    re.IGNORECASE,
)


def parse_dutch_date(s: str):
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%d-%m-%Y", "%d-%m-%y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def parse_float(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def main():
    rows_in = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    rows_out = []
    skipped = 0
    for r in rows_in:
        d = parse_dutch_date(r.get("Datum"))
        if d is None:
            skipped += 1
            continue
        toel = (r.get("Toelichting uren") or "") + " " + (r.get("Toelichting secundaire uren") or "")
        toel = toel.strip()
        primary = parse_float(r.get("Primaire uren"))
        secondary = parse_float(r.get("Secundaire uren"))
        total = parse_float(r.get("Primair+secundair"))
        if total is None:
            total = (primary or 0) + (secondary or 0)

        # Flags
        illness = 1 if ILLNESS_PATTERNS.search(toel) else 0
        doctor = 1 if DOCTOR_PATTERNS.search(toel) else 0
        amsterdam = 1 if AMSTERDAM_PATTERNS.search(toel) else 0
        vacation = 1 if VACATION_PATTERNS.search(toel) else 0

        rows_out.append({
            "date": d.isoformat(),
            "week": d.isocalendar()[1],
            "primary_hours": primary if primary is not None else "",
            "secondary_hours": secondary if secondary is not None else "",
            "total_hours": total,
            "illness_flag": illness,
            "doctor_visit_flag": doctor,
            "amsterdam_flag": amsterdam,
            "vacation_flag": vacation,
            "source_tab": r.get("tab", ""),
            "toelichting": toel,
        })

    rows_out.sort(key=lambda r: r["date"])
    fields = ["date", "week", "primary_hours", "secondary_hours", "total_hours",
              "illness_flag", "doctor_visit_flag", "amsterdam_flag",
              "vacation_flag", "source_tab", "toelichting"]
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows_out:
            w.writerow(r)

    # Summary
    n = len(rows_out)
    n_ill = sum(1 for r in rows_out if r["illness_flag"])
    n_doc = sum(1 for r in rows_out if r["doctor_visit_flag"])
    n_ams = sum(1 for r in rows_out if r["amsterdam_flag"])
    n_vac = sum(1 for r in rows_out if r["vacation_flag"])
    n_work = sum(1 for r in rows_out if r["total_hours"] and r["total_hours"] >= 1)

    print(f"Parsed {n} days ({skipped} skipped)")
    print(f"  Date range: {rows_out[0]['date']} -> {rows_out[-1]['date']}")
    print(f"  Days with work (>=1h): {n_work}")
    print(f"  Days flagged illness: {n_ill}")
    print(f"  Days flagged doctor visit: {n_doc}")
    print(f"  Days flagged amsterdam: {n_ams}")
    print(f"  Days flagged vacation: {n_vac}")
    print(f"\nWrote {OUTPUT}")


if __name__ == "__main__":
    main()
