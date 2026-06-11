"""Map FIT monitoring_b coverage by calendar day and surface any gaps.

Uses the file_id.time_created already extracted in 01_*. We assume each
monitoring_b file represents one continuous monitoring session — most days have
multiple files because Garmin Connect rolls over per-sync.
"""
from __future__ import annotations

import csv
import collections
from datetime import date, timedelta
from pathlib import Path

CSV_IN = Path(__file__).resolve().parent.parent / "output" / "fit_files_classified.csv"
OUT = Path(__file__).resolve().parent.parent / "output" / "monitoring_coverage.csv"


def main() -> int:
    with CSV_IN.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    by_day: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    for r in rows:
        if not r["time_created"] or r["time_created"] == "None":
            continue
        day = r["time_created"][:10]
        by_day[day][r["type"]] += 1

    if not by_day:
        print("no dated rows")
        return 1

    first = min(by_day)
    last = max(by_day)
    f_d = date.fromisoformat(first)
    l_d = date.fromisoformat(last)
    days_total = (l_d - f_d).days + 1
    days_with_monitoring = sum(1 for d, c in by_day.items() if c.get("monitoring_b", 0) > 0)
    days_with_49 = sum(1 for d, c in by_day.items() if c.get("49", 0) > 0)
    days_with_any = len(by_day)

    print(f"span: {first} -> {last} = {days_total} calendar days")
    print(f"days with monitoring_b file: {days_with_monitoring}  ({100*days_with_monitoring/days_total:.1f}%)")
    print(f"days with type-49 (sleep): {days_with_49}  ({100*days_with_49/days_total:.1f}%)")
    print(f"days with any FIT: {days_with_any}  ({100*days_with_any/days_total:.1f}%)")

    # find gap runs in monitoring_b coverage
    gap_start = None
    gaps: list[tuple[str, str, int]] = []
    d = f_d
    while d <= l_d:
        key = d.isoformat()
        has_mon = by_day.get(key, {}).get("monitoring_b", 0) > 0
        if not has_mon:
            if gap_start is None:
                gap_start = d
        else:
            if gap_start is not None:
                gaps.append((gap_start.isoformat(), (d - timedelta(days=1)).isoformat(), (d - gap_start).days))
                gap_start = None
        d += timedelta(days=1)
    if gap_start is not None:
        gaps.append((gap_start.isoformat(), l_d.isoformat(), (l_d - gap_start).days + 1))

    long_gaps = [g for g in gaps if g[2] >= 3]
    print(f"\ngaps >= 3 days in monitoring_b coverage: {len(long_gaps)}")
    for g in long_gaps[:30]:
        print(f"  {g[0]} -> {g[1]}  ({g[2]} days)")
    if len(long_gaps) > 30:
        print(f"  ...and {len(long_gaps)-30} more")

    # Write per-day CSV
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "monitoring_b_files", "type_49_files", "type_44_files", "type_41_files", "activity_files"])
        d = f_d
        while d <= l_d:
            key = d.isoformat()
            c = by_day.get(key, {})
            w.writerow(
                [
                    key,
                    c.get("monitoring_b", 0),
                    c.get("49", 0),
                    c.get("44", 0),
                    c.get("41", 0),
                    c.get("activity", 0),
                ]
            )
            d += timedelta(days=1)
    print(f"\nwrote per-day coverage -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
