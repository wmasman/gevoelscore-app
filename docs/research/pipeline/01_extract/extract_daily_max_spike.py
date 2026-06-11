"""H02b — Stage 1: parse all monitoring_b FIT files and emit per-day
max-spike-duration.

This is the expensive step (~5 minutes to parse ~8.000 FIT files).
Cached to daily_max_spike.csv so the test.py stage runs in seconds.

Output schema:
  date, sample_count, max_spike_minutes, valid (1 if sample_count >= 60)

Per hypothesis.md §4.1:
  - spike = contiguous run of samples ≥ 75 lasting ≥ 5 minutes, with
    gaps ≤ 3 minutes between consecutive samples
  - daily max_spike_minutes = duration of longest qualifying spike
  - days with < 60 stress samples are marked invalid (off-wrist)
"""
from __future__ import annotations

import collections
import csv
import io
import sys
import zipfile
from datetime import date, datetime, timedelta
from pathlib import Path

import fitdecode

GARMIN_DUMP = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Uploaded-Files"
)
ZIPS = ["UploadedFiles_0-_Part1.zip", "UploadedFiles_0-_Part2.zip"]
CLASSIFIED_CSV = Path(__file__).resolve().parent.parent.parent / "output" / "fit_files_classified.csv"
OUT_CSV = Path(__file__).resolve().parent / "daily_max_spike.csv"

SPIKE_THRESHOLD = 75
MIN_SPIKE_MINUTES = 5
MAX_GAP_MINUTES = 3
MIN_SAMPLES_FOR_VALID_DAY = 60


def find_max_spike(samples: list[tuple[datetime, int]]) -> float:
    """Return the longest spike duration (in minutes) where:
    - all stress values are ≥ SPIKE_THRESHOLD
    - gaps between consecutive samples are ≤ MAX_GAP_MINUTES
    - total duration is ≥ MIN_SPIKE_MINUTES
    """
    if not samples:
        return 0.0
    samples.sort(key=lambda x: x[0])
    best = 0.0
    cur_start: datetime | None = None
    cur_last: datetime | None = None
    for ts, v in samples:
        if v >= SPIKE_THRESHOLD:
            if cur_start is None:
                cur_start = ts
                cur_last = ts
            else:
                gap_min = (ts - cur_last).total_seconds() / 60.0
                if gap_min > MAX_GAP_MINUTES:
                    # gap broke the spike; finalise prior
                    dur = (cur_last - cur_start).total_seconds() / 60.0
                    if dur >= MIN_SPIKE_MINUTES and dur > best:
                        best = dur
                    cur_start = ts
                    cur_last = ts
                else:
                    cur_last = ts
        else:
            if cur_start is not None:
                dur = (cur_last - cur_start).total_seconds() / 60.0
                if dur >= MIN_SPIKE_MINUTES and dur > best:
                    best = dur
                cur_start = None
                cur_last = None
    if cur_start is not None:
        dur = (cur_last - cur_start).total_seconds() / 60.0
        if dur >= MIN_SPIKE_MINUTES and dur > best:
            best = dur
    return best


def main() -> int:
    # Load classified CSV to find monitoring_b files
    with CLASSIFIED_CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    mfiles = [r for r in rows if r["type"] == "monitoring_b"]
    print(f"monitoring_b files to parse: {len(mfiles)}", file=sys.stderr)

    # Open zips once
    open_zips = {z: zipfile.ZipFile(GARMIN_DUMP / z) for z in {r["zip"] for r in mfiles}}

    # date -> [(timestamp, stress_level), ...]
    by_date: dict[date, list[tuple[datetime, int]]] = collections.defaultdict(list)

    for i, r in enumerate(mfiles):
        if i % 500 == 0:
            print(f"  {i}/{len(mfiles)}", file=sys.stderr)
        try:
            buf = open_zips[r["zip"]].read(r["filename"])
            with fitdecode.FitReader(io.BytesIO(buf)) as fit:
                for frame in fit:
                    if not isinstance(frame, fitdecode.FitDataMessage):
                        continue
                    if frame.name != "stress_level":
                        continue
                    ts = None
                    val = None
                    for f in frame.fields:
                        if f.name == "stress_level_time" and isinstance(f.value, datetime):
                            ts = f.value
                        elif f.name == "stress_level_value" and isinstance(f.value, int):
                            val = f.value
                    if ts is None or val is None:
                        continue
                    if val < 1 or val > 100:
                        continue
                    # use UTC date for indexing (Garmin's calendarDate
                    # convention is the local-day, but at per-minute resolution
                    # day-boundary samples will rarely matter; we use the
                    # timestamp's date)
                    d = ts.date()
                    by_date[d].append((ts, val))
        except Exception as e:
            print(f"  ERROR on {r['filename']}: {e}", file=sys.stderr)

    for z in open_zips.values():
        z.close()

    # Dedupe samples per day (same ts can appear in multiple files)
    print("\nDeduping and computing max-spike per day…", file=sys.stderr)
    out_rows = []
    for d in sorted(by_date):
        samples = by_date[d]
        # dedup on timestamp keeping max value (rare collisions)
        seen: dict[datetime, int] = {}
        for ts, v in samples:
            if ts not in seen or v > seen[ts]:
                seen[ts] = v
        deduped = list(seen.items())
        max_spike = find_max_spike(deduped)
        valid = len(deduped) >= MIN_SAMPLES_FOR_VALID_DAY
        out_rows.append({
            "date": d.isoformat(),
            "sample_count": len(deduped),
            "max_spike_minutes": round(max_spike, 1),
            "valid": 1 if valid else 0,
        })

    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["date", "sample_count", "max_spike_minutes", "valid"])
        w.writeheader()
        w.writerows(out_rows)
    print(f"wrote {len(out_rows)} days -> {OUT_CSV}", file=sys.stderr)
    n_valid = sum(1 for r in out_rows if r["valid"])
    print(f"  valid days (sample_count >= {MIN_SAMPLES_FOR_VALID_DAY}): {n_valid}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
