"""H02d calibration — characterise sentinel-stress minutes vs HR sample
presence.

Question for the pre-registration:
  For minutes where stress is a sentinel value (the H02b filter drops
  these), how close is the nearest heart_rate sample? This tells us
  what time-window tolerance to lock for the rule
    'HR present near sentinel minute => too_active; else => off_wrist'.

Stratified-sampled 8 monitoring_b files across 2022-09 -> 2026-05.
Reports:
  - sentinel-value distribution (what numbers Garmin actually emits)
  - HR cadence (median + p90 seconds between samples)
  - for each sentinel sample, gap-seconds to nearest HR sample
  - fraction of sentinels with HR within {30, 60, 90, 180, 300}s
"""
from __future__ import annotations

import bisect
import collections
import csv
import io
import statistics
import sys
import zipfile
from datetime import datetime
from pathlib import Path

import fitdecode

# Shared FIT timestamp_16 resolver — see its module docstring for the
# FIT-epoch / Unix-epoch gotcha this avoids.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from fit_utils import Monitoring16Resolver  # noqa: E402

GARMIN_DUMP = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Uploaded-Files"
)
CLASSIFIED_CSV = Path(__file__).resolve().parent.parent.parent / "output" / "fit_files_classified.csv"
OUT = Path(__file__).resolve().parent / "calibrate_sentinel_hr_result.md"

N_FILES = 8
TOLERANCE_BUCKETS_S = [30, 60, 90, 180, 300]


def stratified_pick(rows: list[dict], n: int) -> list[dict]:
    rows = [r for r in rows if r["time_created"] and r["time_created"] != "None"]
    rows.sort(key=lambda r: r["time_created"])
    if len(rows) <= n:
        return rows
    step = len(rows) / n
    return [rows[int(i * step)] for i in range(n)]


def extract(buf: bytes) -> tuple[list[tuple[datetime, int]], list[datetime]]:
    """Return (stress_samples, hr_timestamps).

    stress_samples preserves sentinel values (no [1,100] filter).
    hr_timestamps are reconstructed from monitoring frames; both full
    `timestamp` and 16-bit relative `timestamp_16` are handled.
    """
    stress: list[tuple[datetime, int]] = []
    hr_ts: list[datetime] = []
    resolver = Monitoring16Resolver()

    with fitdecode.FitReader(io.BytesIO(buf)) as fit:
        for frame in fit:
            if not isinstance(frame, fitdecode.FitDataMessage):
                continue
            if frame.name == "stress_level":
                ts = None
                val = None
                for f in frame.fields:
                    if f.name == "stress_level_time" and isinstance(f.value, datetime):
                        ts = f.value
                    elif f.name == "stress_level_value" and isinstance(f.value, int):
                        val = f.value
                if ts is not None and val is not None:
                    stress.append((ts, val))
            elif frame.name == "monitoring_info":
                for f in frame.fields:
                    if f.name == "timestamp" and isinstance(f.value, datetime):
                        resolver.set_reference(f.value)
                        break
            elif frame.name == "monitoring":
                ts = resolver.resolve_frame(frame)
                hr = next(
                    (f.value for f in frame.fields
                     if f.name == "heart_rate" and isinstance(f.value, int)),
                    None,
                )
                if ts is not None and hr is not None:
                    hr_ts.append(ts)
    return stress, hr_ts


def gap_to_nearest(target: datetime, sorted_ts: list[datetime]) -> float:
    """Seconds to the nearest element of sorted_ts (inf if list empty)."""
    if not sorted_ts:
        return float("inf")
    i = bisect.bisect_left(sorted_ts, target)
    candidates: list[float] = []
    if i < len(sorted_ts):
        candidates.append(abs((sorted_ts[i] - target).total_seconds()))
    if i > 0:
        candidates.append(abs((target - sorted_ts[i - 1]).total_seconds()))
    return min(candidates)


def main() -> int:
    with CLASSIFIED_CSV.open(encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["type"] == "monitoring_b"]
    picks = stratified_pick(rows, N_FILES)
    print(f"calibrating on {len(picks)} files:", file=sys.stderr)
    for r in picks:
        print(f"  {r['time_created'][:10]}  {r['filename']}", file=sys.stderr)

    zips_needed = sorted({r["zip"] for r in picks})
    open_zips = {z: zipfile.ZipFile(GARMIN_DUMP / z) for z in zips_needed}

    all_stress: list[tuple[datetime, int]] = []
    all_hr_ts: list[datetime] = []
    per_file_summary: list[dict] = []

    for r in picks:
        buf = open_zips[r["zip"]].read(r["filename"])
        stress, hr_ts = extract(buf)
        all_stress.extend(stress)
        all_hr_ts.extend(hr_ts)
        per_file_summary.append({
            "date": r["time_created"][:10],
            "stress_n": len(stress),
            "hr_n": len(hr_ts),
            "sentinels": sum(1 for _, v in stress if v < 1 or v > 100),
        })

    for z in open_zips.values():
        z.close()

    # Dedup & sort
    hr_sorted = sorted(set(all_hr_ts))
    # Sentinel value distribution
    sentinel_vals = collections.Counter(v for _, v in all_stress if v < 1 or v > 100)
    valid_count = sum(1 for _, v in all_stress if 1 <= v <= 100)

    # HR cadence
    deltas = [
        (hr_sorted[i + 1] - hr_sorted[i]).total_seconds()
        for i in range(len(hr_sorted) - 1)
        if (hr_sorted[i + 1] - hr_sorted[i]).total_seconds() > 0
    ]
    hr_med = statistics.median(deltas) if deltas else None
    hr_p90 = sorted(deltas)[int(len(deltas) * 0.9)] if deltas else None
    hr_p99 = sorted(deltas)[int(len(deltas) * 0.99)] if deltas else None

    # Gaps from each sentinel to nearest HR
    sentinel_gaps: list[float] = []
    for ts, v in all_stress:
        if v < 1 or v > 100:
            sentinel_gaps.append(gap_to_nearest(ts, hr_sorted))

    # Tolerance bucket counts
    bucket_counts = {b: sum(1 for g in sentinel_gaps if g <= b) for b in TOLERANCE_BUCKETS_S}

    # Same for valid (non-sentinel) stress samples for comparison
    valid_gaps: list[float] = []
    for ts, v in all_stress:
        if 1 <= v <= 100:
            valid_gaps.append(gap_to_nearest(ts, hr_sorted))
    valid_bucket = {b: sum(1 for g in valid_gaps if g <= b) for b in TOLERANCE_BUCKETS_S}

    # Write result
    lines: list[str] = []
    lines.append("# H02d sentinel-vs-HR calibration\n")
    lines.append("Stratified sample of {} monitoring_b files across the analysis window.\n".format(len(picks)))
    lines.append("## Files sampled\n")
    lines.append("| date | stress samples | HR samples | sentinel count |")
    lines.append("|---|---:|---:|---:|")
    for s in per_file_summary:
        lines.append(f"| {s['date']} | {s['stress_n']} | {s['hr_n']} | {s['sentinels']} |")
    lines.append("")
    lines.append(f"Totals: {len(all_stress)} stress samples, {valid_count} valid (1-100), "
                 f"{len(sentinel_gaps)} sentinel, {len(hr_sorted)} unique HR timestamps.\n")
    lines.append("## Sentinel value distribution\n")
    lines.append("| value | count |")
    lines.append("|---:|---:|")
    for val, n in sorted(sentinel_vals.items()):
        lines.append(f"| {val} | {n} |")
    lines.append("")
    lines.append("## HR sample cadence (seconds between consecutive HR samples)\n")
    if hr_med is not None:
        lines.append(f"- median: {hr_med:.0f}s")
        lines.append(f"- p90: {hr_p90:.0f}s")
        lines.append(f"- p99: {hr_p99:.0f}s")
        lines.append(f"- max: {max(deltas):.0f}s")
    lines.append("")
    lines.append("## Gap from each sentinel-stress sample to nearest HR sample\n")
    if sentinel_gaps:
        finite_gaps = [g for g in sentinel_gaps if g != float("inf")]
        if finite_gaps:
            lines.append(f"- N sentinel samples: {len(sentinel_gaps)}")
            lines.append(f"- N with no HR in this file: {sum(1 for g in sentinel_gaps if g == float('inf'))}")
            lines.append(f"- median gap (finite): {statistics.median(finite_gaps):.0f}s")
            lines.append(f"- p90 gap (finite): {sorted(finite_gaps)[int(len(finite_gaps) * 0.9)]:.0f}s")
    lines.append("")
    lines.append("## Fraction of sentinels with HR within tolerance window\n")
    lines.append("| tolerance (s) | sentinels covered | % of sentinels | valid-stress covered | % of valid |")
    lines.append("|---:|---:|---:|---:|---:|")
    for b in TOLERANCE_BUCKETS_S:
        pct_s = 100 * bucket_counts[b] / max(1, len(sentinel_gaps))
        pct_v = 100 * valid_bucket[b] / max(1, len(valid_gaps))
        lines.append(f"| {b} | {bucket_counts[b]} | {pct_s:.1f}% | {valid_bucket[b]} | {pct_v:.1f}% |")
    lines.append("")
    lines.append("## Reading\n")
    lines.append("If sentinel-coverage % at small tolerances (30-90s) is high, "
                 "the 'HR-present means too_active' rule is clean. "
                 "If coverage drops sharply between sentinels and valid samples, "
                 "the sentinels are systematically clustered in HR-gaps (off-wrist).")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
