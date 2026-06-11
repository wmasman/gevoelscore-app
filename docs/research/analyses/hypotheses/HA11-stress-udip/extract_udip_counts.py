"""HA11 - Stage 1: parse all monitoring_b FIT files, build per-day
per-minute stress sequences, detect U-dip events per the locked
hypothesis.md spec, emit udip_counts.csv.

Output schema:
  date, sample_count, u_dip_count, valid
where valid = 1 if sample_count >= 600.

U-dip event definition (locked hypothesis.md §4.2):
  - pre_dip window [t-35, t-5]: 30 min, mean S_pre with >= 21 samples
  - dip window [t-7, t+7]: 15 min, min S_floor with >= 11 samples
  - post_dip window [t+8, t+38]: 30 min, mean S_post with >= 21 samples
  - All samples must be in [1, 100]
Triggers when:
  - S_pre >= 40
  - S_floor <= S_pre - 25
  - S_post >= S_pre + 5
Consecutive triggers must be >= 60 min apart.

This is the expensive stage (~5-10 min). Cached to udip_counts.csv
so test.py runs in seconds.
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
CLASSIFIED_CSV = (
    Path(__file__).resolve().parent.parent.parent / "output" / "fit_files_classified.csv"
)
OUT_CSV = Path(__file__).resolve().parent / "udip_counts.csv"

STRESS_MIN_VALID = 1
STRESS_MAX_VALID = 100

PRE_DIP_START_MIN = 5     # window starts 35 min before t, ends 5 before
PRE_DIP_END_MIN = 35
DIP_HALF_MIN = 7          # dip window is [t-7, t+7]
POST_DIP_START_MIN = 8
POST_DIP_END_MIN = 38

PRE_DIP_DURATION = PRE_DIP_END_MIN - PRE_DIP_START_MIN  # 30 min
DIP_DURATION = 2 * DIP_HALF_MIN + 1                      # 15 min
POST_DIP_DURATION = POST_DIP_END_MIN - POST_DIP_START_MIN  # 30 min

MIN_PRE_SAMPLES = int(0.7 * PRE_DIP_DURATION)
MIN_DIP_SAMPLES = int(0.7 * DIP_DURATION)
MIN_POST_SAMPLES = int(0.7 * POST_DIP_DURATION)

S_PRE_MIN = 40
DROP_MIN = 25
PLATEAU_DELTA_MIN = 5

REFRACTORY_MIN = 60       # at least 60 min between consecutive events
MIN_SAMPLES_FOR_VALID_DAY = 600


def detect_udip_events(samples: list[tuple[datetime, int]]) -> int:
    """Detect U-dip events on a per-day sequence of (ts, stress) tuples.

    Returns the count of distinct U-dip events satisfying the locked spec.
    """
    if len(samples) < MIN_SAMPLES_FOR_VALID_DAY:
        return 0
    samples = sorted(samples, key=lambda x: x[0])
    # Build a minute-keyed lookup for fast window slicing
    # Each sample slot is one minute; multiple samples per minute keep latest
    by_min: dict[datetime, int] = {}
    for ts, v in samples:
        if STRESS_MIN_VALID <= v <= STRESS_MAX_VALID:
            # Round to nearest minute
            tm = ts.replace(second=0, microsecond=0)
            by_min[tm] = v
    if not by_min:
        return 0
    sorted_mins = sorted(by_min.keys())
    count = 0
    last_trigger_ts: datetime | None = None
    for t in sorted_mins:
        # Refractory: skip if within 60 min of last trigger
        if last_trigger_ts is not None and (t - last_trigger_ts).total_seconds() < REFRACTORY_MIN * 60:
            continue
        # Compute window samples
        pre_start = t - timedelta(minutes=PRE_DIP_END_MIN)
        pre_end = t - timedelta(minutes=PRE_DIP_START_MIN)
        dip_start = t - timedelta(minutes=DIP_HALF_MIN)
        dip_end = t + timedelta(minutes=DIP_HALF_MIN)
        post_start = t + timedelta(minutes=POST_DIP_START_MIN)
        post_end = t + timedelta(minutes=POST_DIP_END_MIN)
        pre_samples = [by_min[m] for m in by_min if pre_start <= m < pre_end]
        dip_samples = [by_min[m] for m in by_min if dip_start <= m <= dip_end]
        post_samples = [by_min[m] for m in by_min if post_start <= m < post_end]
        if (len(pre_samples) < MIN_PRE_SAMPLES
                or len(dip_samples) < MIN_DIP_SAMPLES
                or len(post_samples) < MIN_POST_SAMPLES):
            continue
        s_pre = sum(pre_samples) / len(pre_samples)
        s_floor = min(dip_samples)
        s_post = sum(post_samples) / len(post_samples)
        if s_pre < S_PRE_MIN:
            continue
        if s_floor > s_pre - DROP_MIN:
            continue
        if s_post < s_pre + PLATEAU_DELTA_MIN:
            continue
        count += 1
        last_trigger_ts = t
    return count


def main() -> int:
    if not CLASSIFIED_CSV.exists():
        print(f"ERROR: {CLASSIFIED_CSV} not found", file=sys.stderr)
        return 1
    with CLASSIFIED_CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    mfiles = [r for r in rows if r["type"] == "monitoring_b"]
    print(f"monitoring_b files to parse: {len(mfiles)}", file=sys.stderr)

    open_zips: dict[str, zipfile.ZipFile] = {}
    for z in {r["zip"] for r in mfiles}:
        open_zips[z] = zipfile.ZipFile(GARMIN_DUMP / z)

    # date -> [(timestamp, stress_level), ...]
    by_date: dict[date, list[tuple[datetime, int]]] = collections.defaultdict(list)

    for i, r in enumerate(mfiles):
        if i % 500 == 0:
            print(f"  parsed {i}/{len(mfiles)} files", file=sys.stderr)
        try:
            buf = open_zips[r["zip"]].read(r["filename"])
            with fitdecode.FitReader(io.BytesIO(buf)) as fit:
                for frame in fit:
                    if not isinstance(frame, fitdecode.FitDataMessage):
                        continue
                    if frame.name != "stress_level":
                        continue
                    ts_field = next(
                        (f for f in frame.fields if f.name == "stress_level_time"),
                        None,
                    )
                    val_field = next(
                        (f for f in frame.fields if f.name == "stress_level_value"),
                        None,
                    )
                    if ts_field is None or val_field is None:
                        continue
                    ts = ts_field.value
                    val = val_field.value
                    if ts is None or val is None:
                        continue
                    if not isinstance(ts, datetime):
                        continue
                    try:
                        v = int(val)
                    except (TypeError, ValueError):
                        continue
                    by_date[ts.date()].append((ts, v))
        except Exception as e:
            print(f"  warn: failed {r['filename']}: {e}", file=sys.stderr)
            continue

    print(f"parsed {len(by_date)} dates with stress samples", file=sys.stderr)

    # Detect U-dip events per day
    out_rows: list[dict] = []
    for d in sorted(by_date.keys()):
        samples = by_date[d]
        # sample_count = total samples (any value); spec uses in-range only
        # but the validity threshold (600 samples) is on total samples to
        # be consistent with H02b
        in_range = [s for s in samples if STRESS_MIN_VALID <= s[1] <= STRESS_MAX_VALID]
        sample_count = len(in_range)
        valid = 1 if sample_count >= MIN_SAMPLES_FOR_VALID_DAY else 0
        if valid:
            u_dip_count = detect_udip_events(samples)
        else:
            u_dip_count = 0
        out_rows.append({
            "date": d.isoformat(),
            "sample_count": sample_count,
            "u_dip_count": u_dip_count,
            "valid": valid,
        })

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["date", "sample_count", "u_dip_count", "valid"])
        w.writeheader()
        for r in out_rows:
            w.writerow(r)
    n_valid = sum(1 for r in out_rows if r["valid"])
    total_udips = sum(r["u_dip_count"] for r in out_rows)
    print(f"Wrote {OUT_CSV} ({len(out_rows)} days, {n_valid} valid, "
          f"{total_udips} total U-dip events)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
