"""Extract recorded activities to a flat CSV.

Parses summarizedActivities.json and emits one row per activity with
the fields locked in definition.md §3.1.

PEM-framing note: training-effect fields are kept as descriptors only.
They do NOT drive the daily exertion_class — primary classification
uses passive intensity minutes from UDS (see definition.md §1.1).
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ACTIVITIES_JSON = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data"
    r"\DI_CONNECT\DI-Connect-Fitness\user@example.com_0_summarizedActivities.json"
)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output" / "activities.csv"

FIELDS = [
    "start_date", "activity_type", "name",
    "duration_min", "moving_duration_min",
    "avg_hr", "max_hr", "min_hr",
    "time_in_zone_4plus_min", "time_in_zone_0_min",
    "moderate_min", "vigorous_min", "intensity_min_total",
    "aerobic_te", "anaerobic_te",
    "calories",
    "start_stress", "end_stress", "difference_stress", "avg_stress", "max_stress",
    "distance_m", "elevation_gain_m", "elevation_loss_m",
    "workout_rpe", "workout_feel",
]


def ms_to_min(ms):
    if ms is None:
        return None
    return round(ms / 60000, 2)


def main():
    print(f"Loading {ACTIVITIES_JSON}...")
    raw = json.loads(ACTIVITIES_JSON.read_text(encoding="utf-8"))
    acts = raw[0]["summarizedActivitiesExport"]
    print(f"  {len(acts)} activities")

    rows = []
    for a in acts:
        ts = a.get("startTimeLocal")  # local-time epoch ms
        if ts is None:
            ts = a.get("startTimeGmt")
        if ts is None:
            continue
        # Local-time interpretation: Garmin stores both startTimeLocal and startTimeGmt
        # in epoch ms; using startTimeLocal so the date matches the participant's
        # calendar day, not UTC.
        d = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).date()

        zone4plus_ms = (
            (a.get("hrTimeInZone_4") or 0)
            + (a.get("hrTimeInZone_5") or 0)
            + (a.get("hrTimeInZone_6") or 0)
        )

        rows.append({
            "start_date": d.isoformat(),
            "activity_type": a.get("activityType", ""),
            "name": (a.get("name") or "").replace("|", "/").replace("\n", " "),
            "duration_min": ms_to_min(a.get("duration")),
            "moving_duration_min": ms_to_min(a.get("movingDuration")),
            "avg_hr": a.get("avgHr"),
            "max_hr": a.get("maxHr"),
            "min_hr": a.get("minHr"),
            "time_in_zone_4plus_min": ms_to_min(zone4plus_ms),
            "time_in_zone_0_min": ms_to_min(a.get("hrTimeInZone_0")),
            "moderate_min": a.get("moderateIntensityMinutes"),
            "vigorous_min": a.get("vigorousIntensityMinutes"),
            "intensity_min_total": (
                (a.get("moderateIntensityMinutes") or 0)
                + (a.get("vigorousIntensityMinutes") or 0)
            ),
            "aerobic_te": a.get("aerobicTrainingEffect"),
            "anaerobic_te": a.get("anaerobicTrainingEffect"),
            "calories": a.get("calories"),
            "start_stress": a.get("startStress"),
            "end_stress": a.get("endStress"),
            "difference_stress": a.get("differenceStress"),
            "avg_stress": a.get("avgStress"),
            "max_stress": a.get("maxStress"),
            "distance_m": a.get("distance"),
            "elevation_gain_m": a.get("elevationGain"),
            "elevation_loss_m": a.get("elevationLoss"),
            "workout_rpe": a.get("workoutRpe"),
            "workout_feel": a.get("workoutFeel"),
        })

    rows.sort(key=lambda r: r["start_date"])
    print(f"  date range: {rows[0]['start_date']} -> {rows[-1]['start_date']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
