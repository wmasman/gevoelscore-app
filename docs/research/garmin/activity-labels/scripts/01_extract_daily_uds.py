"""Extract daily UDS summaries to a flat CSV.

Walks all UDSFile_*.json in DI-Connect-Aggregator and emits one row
per calendar day with the fields locked in definition.md §3.2.
"""
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

GARMIN_ROOT = Path(r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT")
UDS_DIR = GARMIN_ROOT / "DI-Connect-Aggregator"

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output" / "daily_uds.csv"

FIELDS = [
    "date", "total_steps", "daily_step_goal", "total_distance_m",
    "moderate_min", "vigorous_min",
    "highly_active_sec", "active_sec", "active_kcal",
    "resting_hr", "min_hr", "max_hr", "max_avg_hr",
    "is_vigorous_day",
]


def load_uds_files() -> list[Path]:
    files = sorted(UDS_DIR.glob("UDSFile_*.json"))
    if not files:
        raise SystemExit(f"No UDS files found in {UDS_DIR}")
    return files


def parse_one(p: Path) -> list[dict]:
    raw = json.loads(p.read_text(encoding="utf-8"))
    rows = []
    for item in raw:
        cd = item.get("calendarDate")
        if not cd:
            continue
        rows.append({
            "date": cd,
            "total_steps": item.get("totalSteps"),
            "daily_step_goal": item.get("dailyStepGoal"),
            "total_distance_m": item.get("totalDistanceMeters"),
            "moderate_min": item.get("moderateIntensityMinutes"),
            "vigorous_min": item.get("vigorousIntensityMinutes"),
            "highly_active_sec": item.get("highlyActiveSeconds"),
            "active_sec": item.get("activeSeconds"),
            "active_kcal": item.get("activeKilocalories"),
            "resting_hr": item.get("restingHeartRate"),
            "min_hr": item.get("minHeartRate"),
            "max_hr": item.get("maxHeartRate"),
            "max_avg_hr": item.get("maxAvgHeartRate"),
            "is_vigorous_day": item.get("isVigorousDay"),
        })
    return rows


def main():
    files = load_uds_files()
    print(f"Loading {len(files)} UDS files...")
    by_date: dict[str, dict] = {}
    for p in files:
        rows = parse_one(p)
        for r in rows:
            # Most recent file wins for boundary days (later file processed last)
            by_date[r["date"]] = r
    print(f"  {len(by_date)} unique calendar days")

    sorted_rows = [by_date[d] for d in sorted(by_date)]
    print(f"  date range: {sorted_rows[0]['date']} -> {sorted_rows[-1]['date']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in sorted_rows:
            w.writerow(r)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
