"""Profile sub-daily sample density in monitoring_b and type-49 FIT files.

For a representative sample drawn across the full 5-year span, decode each file
and tally: message counts, field names that appear, time span covered, and HR
sample cadence.

We're answering one question: is there enough within-day granularity in this
dump to detect spikes (HR, stress, body battery dips) as crash predictors, or
do we only have rolled-up daily numbers?

Reads files directly from the source zips so we don't have to keep an extracted
copy on disk.
"""
from __future__ import annotations

import collections
import csv
import io
import random
import statistics
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import fitdecode

GARMIN_DUMP = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Uploaded-Files"
)
ZIPS = ["UploadedFiles_0-_Part1.zip", "UploadedFiles_0-_Part2.zip"]
CLASSIFIED_CSV = Path(__file__).resolve().parent.parent / "output" / "fit_files_classified.csv"
OUT_DIR = Path(__file__).resolve().parent.parent / "output"

SAMPLE_PER_TYPE = 60  # spread across the 5-year span
TYPES = ("monitoring_b", "49")


def stratified_sample(rows: list[dict], n: int) -> list[dict]:
    """Pick ~n rows spread evenly across time_created order."""
    rows = [r for r in rows if r["time_created"] and r["time_created"] != "None"]
    rows.sort(key=lambda r: r["time_created"])
    if len(rows) <= n:
        return rows
    step = len(rows) / n
    return [rows[int(i * step)] for i in range(n)]


def profile_file(buf: bytes) -> dict:
    """Return profile dict for one FIT file."""
    msg_count: collections.Counter[str] = collections.Counter()
    field_count: collections.Counter[str] = collections.Counter()
    hr_timestamps: list[datetime] = []
    hr_values: list[int] = []
    stress_count = 0
    body_battery_count = 0
    spo2_count = 0
    resp_count = 0
    timestamps: list[datetime] = []

    with fitdecode.FitReader(io.BytesIO(buf)) as fit:
        for frame in fit:
            if not isinstance(frame, fitdecode.FitDataMessage):
                continue
            msg_count[frame.name] += 1
            for f in frame.fields:
                field_count[f"{frame.name}.{f.name}"] += 1
                if f.name == "timestamp" and isinstance(f.value, datetime):
                    timestamps.append(f.value)
                if f.name == "heart_rate" and isinstance(f.value, int):
                    hr_values.append(f.value)
                    hr_timestamps.append(
                        next(
                            (
                                ff.value
                                for ff in frame.fields
                                if ff.name == "timestamp" and isinstance(ff.value, datetime)
                            ),
                            None,
                        )
                    )
                if f.name in ("stress_level_value", "current_stress_level"):
                    stress_count += 1
                if "body_battery" in f.name.lower():
                    body_battery_count += 1
                if f.name in ("spo2", "current_spo2") or "spo2" in f.name.lower():
                    spo2_count += 1
                if "respiration" in f.name.lower() or f.name in ("breaths_per_minute",):
                    resp_count += 1

    result = {
        "msg_total": sum(msg_count.values()),
        "msg_kinds": len(msg_count),
        "top_messages": ";".join(f"{k}:{v}" for k, v in msg_count.most_common(8)),
        "hr_samples": len(hr_values),
        "hr_min": min(hr_values) if hr_values else "",
        "hr_max": max(hr_values) if hr_values else "",
        "hr_mean": round(statistics.mean(hr_values), 1) if hr_values else "",
        "stress_samples": stress_count,
        "body_battery_samples": body_battery_count,
        "spo2_samples": spo2_count,
        "respiration_samples": resp_count,
        "span_seconds": (
            int((max(timestamps) - min(timestamps)).total_seconds()) if len(timestamps) >= 2 else 0
        ),
        "first_ts": min(timestamps).isoformat() if timestamps else "",
        "last_ts": max(timestamps).isoformat() if timestamps else "",
    }

    valid_hr_ts = [t for t in hr_timestamps if t is not None]
    if len(valid_hr_ts) >= 2:
        deltas = sorted(
            (valid_hr_ts[i + 1] - valid_hr_ts[i]).total_seconds()
            for i in range(len(valid_hr_ts) - 1)
            if (valid_hr_ts[i + 1] - valid_hr_ts[i]).total_seconds() > 0
        )
        if deltas:
            result["hr_delta_median_s"] = deltas[len(deltas) // 2]
            result["hr_delta_p90_s"] = deltas[int(len(deltas) * 0.9)]
    return result


def main() -> int:
    with CLASSIFIED_CSV.open(encoding="utf-8") as fh:
        all_rows = list(csv.DictReader(fh))

    by_type: dict[str, list[dict]] = collections.defaultdict(list)
    for r in all_rows:
        by_type[r["type"]].append(r)

    rng = random.Random(20260605)  # deterministic; date-as-seed
    work: list[dict] = []
    for t in TYPES:
        sample = stratified_sample(by_type[t], SAMPLE_PER_TYPE)
        for r in sample:
            work.append(r)
    print(f"profiling {len(work)} files across types {TYPES}", file=sys.stderr)

    # open both zips once
    open_zips = {z: zipfile.ZipFile(GARMIN_DUMP / z) for z in ZIPS}

    out_rows = []
    aggregate_fields: dict[str, collections.Counter[str]] = {t: collections.Counter() for t in TYPES}

    for i, r in enumerate(work):
        if i % 20 == 0:
            print(f"  {i}/{len(work)} ({r['type']}, {r['time_created'][:10]})", file=sys.stderr)
        buf = open_zips[r["zip"]].read(r["filename"])
        prof = profile_file(buf)
        out_rows.append({**r, **prof})
        # field presence aggregate
        for token in prof["top_messages"].split(";"):
            pass  # already in row
        # re-decode for field aggregate (cheap; already have buf)
        with fitdecode.FitReader(io.BytesIO(buf)) as fit:
            for frame in fit:
                if isinstance(frame, fitdecode.FitDataMessage):
                    for f in frame.fields:
                        aggregate_fields[r["type"]][f"{frame.name}.{f.name}"] += 1

    for z in open_zips.values():
        z.close()

    # Write per-file profile
    out_csv = OUT_DIR / "monitoring_density_profile.csv"
    fieldnames = list(out_rows[0].keys())
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)
    print(f"wrote {len(out_rows)} rows -> {out_csv}", file=sys.stderr)

    # Write field-presence summary per type
    summary_path = OUT_DIR / "monitoring_field_presence.txt"
    with summary_path.open("w", encoding="utf-8") as fh:
        for t, counter in aggregate_fields.items():
            fh.write(f"\n=== type={t} (across {SAMPLE_PER_TYPE} sampled files) ===\n")
            for k, v in counter.most_common(80):
                fh.write(f"  {v:6d}  {k}\n")
    print(f"wrote field presence -> {summary_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
