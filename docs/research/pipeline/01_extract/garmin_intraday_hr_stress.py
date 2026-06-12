"""Extract per-day intraday HR + stress summaries from monitoring_b FIT files.

Wave 4: builds per-day aggregates operationalising Wiggers A4 (sustained
multi-hour HR elevation) and C4 (stress fails to drop during rest
after overexertion). Both signals share the same source file
(monitoring_b), so one walk produces both.

Reads monitoring_b FIT files using the existing
`output/fit_files_classified.csv` index and the same zip-cache /
fitdecode pattern as `extract_sleep_stress.py`.

Sleep-window vs waking-window: sleep windows come from sleepData.json
(same loader as extract_sleep_stress.py). Samples falling inside a
sleep window are excluded from these metrics — both Wiggers A4 and
C4 are about waking-period dynamics.

A4 baseline (v3, locked 2026-06-12 — see evolution note below):
- For each day d, `hr_median_waking[d]` = median HR across all waking
  samples that day. Stands as its own column — honest descriptor of
  where the user's daytime HR actually sat (the "missing" middle bucket
  between sleep-derived `resting_hr` and noisy peak `max_hr`).
- `hr_daytime_baseline_lagged[d]` = median of `hr_median_waking` over
  the window `[d - 90, d - 30]` — same shape as the v3.2 lagged
  exertion baseline (see memory feedback_use_lagged_exertion_for_pem
  and severity_spec.md § Lagged baseline). The lag-30 buffer ensures
  the recent push window does not contaminate its own reference.
- Threshold for "elevated" = `hr_daytime_baseline_lagged[d] + 20 bpm`.
  Offset chosen to clear the natural spread of typical daytime HR
  (sitting / standing / light household activity); +15 was the v2
  candidate but the reviewer flagged that a daytime baseline already
  embeds those activities into the reference, so a slightly larger
  offset is appropriate.

Evolution:
- v1 (commit 98f416b): threshold = `resting_hr + 15`. Used Garmin's
  sleep-derived RHR as the reference. Any waking activity cleared
  it; median day had 459 elevated minutes and 31-min longest run,
  tripping `hr_sustained_elevated_flag=True` on the median day. The
  flag separated nothing.
- v2 (uncommitted, this file's history briefly): switched to
  `hr_daytime_baseline_28d + 15` (28d trailing). Direction-of-travel
  correct; window and offset suboptimal per reviewer:
  - window of 28d trailing differs from v3.2's `[d-90, d-30]`
    lagged pattern; methodological inconsistency
  - offset +15 may be too lenient given daytime baseline already
    accounts for "where you usually are"
- v3 (this file, locked 2026-06-12): `[d-90, d-30]` window +
  `+20` offset. Matches v3.2 discipline and reviewer recommendation.

C4 baselines (unchanged from v1):
- Stress "rest" zone cutoff of 25 (Garmin app colour scheme).
- Stress "high" zone cutoff of 75 (matches existing H02b threshold
  used by daily_max_spike.csv).

Output: $GEVOELSCORE_DATA_PATH/processed/garmin/intraday_hr_stress_daily.csv

Coverage: from 2021-08-16 (earliest FIT file), per the locked
re-extract convention. A4 columns NaN until 14 valid `hr_median_waking`
days have accumulated within the `[d-90, d-30]` lagged window —
roughly the first ~3 months of coverage will lack A4 columns
(`hr_daytime_baseline_lagged` only valid from ~2021-11-15 onward).

Columns:
- A4 (6 HR cols):
  - hr_median_waking                                <- transparency descriptor
  - hr_daytime_baseline_lagged                      <- transparency: [d-90, d-30] rolling median
  - hr_min_above_daytime_baseline_plus_20_waking
  - hr_longest_elevated_run_min_waking
  - hr_sustained_elevated_flag
  - hr_area_above_daytime_baseline_waking
- C4 (4 stress cols, unchanged from v1):
  - stress_post_peak_drop_avg
  - stress_post_peak_time_to_rest_min
  - stress_high_duration_min
  - stress_recovery_pct_within_2h
"""
from __future__ import annotations

import collections
import csv
import io
import json
import os
import statistics
import sys
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import fitdecode

# --- Paths ---
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent.parent.parent

# Allow importing the shared Monitoring16Resolver from analyses/
# rather than re-implementing the timestamp_16 rollover logic. See
# fit_utils.py docstring for the three-rules-must-all-be-correct
# explanation (FIT epoch != Unix epoch; fitdecode does not auto-
# resolve; rolling reference updates every resolve).
sys.path.insert(0, str(REPO_ROOT / "docs" / "research" / "analyses" / "garmin_exploration" / "scripts"))
from fit_utils import Monitoring16Resolver  # noqa: E402


def _load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


_load_env_file(REPO_ROOT / ".env")
DATA_ROOT = Path(os.environ.get("GEVOELSCORE_DATA_PATH", ""))
if not DATA_ROOT or not DATA_ROOT.exists():
    raise SystemExit("GEVOELSCORE_DATA_PATH not set or does not exist.")

GARMIN_DUMP = DATA_ROOT / "garmin data" / "DI_CONNECT" / "DI-Connect-Uploaded-Files"
WELLNESS_DIR = DATA_ROOT / "garmin data" / "DI_CONNECT" / "DI-Connect-Wellness"
CLASSIFIED_CSV = DATA_ROOT / "analyses" / "garmin_exploration" / "fit_files_classified.csv"
DAILY_UDS = DATA_ROOT / "processed" / "garmin" / "daily_uds.csv"
OUT_CSV = DATA_ROOT / "processed" / "garmin" / "intraday_hr_stress_daily.csv"

# --- Thresholds (Wave 4 v3 2026-06-12; tunable, document if changed) ---
# Window matches v3.2 lagged exertion convention: [d - WINDOW_END, d - WINDOW_LAG]
HR_BASELINE_WINDOW_END = 90           # A4: trailing edge of personal-baseline window (90 days back)
HR_BASELINE_WINDOW_LAG = 30           # A4: leading edge (30-day lag, excludes recent push period)
HR_BASELINE_MIN_VALID = 14            # A4: need at least N valid days in the window to call baseline valid
HR_MEDIAN_MIN_SAMPLES = 120           # A4: need at least N waking HR samples to call hr_median_waking valid
HR_ELEVATION_OFFSET_BPM = 20          # A4: "elevated" = HR > daytime baseline + this
HR_SUSTAINED_MIN = 30                 # A4: "sustained" flag threshold
STRESS_REST_THRESHOLD = 25            # C4: "back to rest" = stress < this
STRESS_HIGH_THRESHOLD = 75            # C4: "high stress" = stress > this
STRESS_POST_PEAK_WINDOW_MIN = 60      # C4: minutes after peak for drop_avg
STRESS_RECOVERY_WINDOW_HRS = 2        # C4: window for recovery_pct

# Cadence assumptions for converting consecutive-minute-bin counts
# back to durations. Per-minute bucketing makes the logic robust to
# whatever the actual sample cadence is (15s, 30s, 1min, etc.).
MINUTES_PER_DAY = 24 * 60

FIELDS = [
    "date",
    # A4 — HR sustained elevation (v3: [d-90, d-30] lagged personal daytime baseline + offset 20)
    "hr_median_waking",                          # transparency: per-day median waking HR
    "hr_daytime_baseline_lagged",                # transparency: [d-90, d-30] rolling-median baseline
    "hr_min_above_daytime_baseline_plus_20_waking",
    "hr_longest_elevated_run_min_waking",
    "hr_sustained_elevated_flag",
    "hr_area_above_daytime_baseline_waking",
    # C4 — stress decay (unchanged)
    "stress_post_peak_drop_avg",
    "stress_post_peak_time_to_rest_min",
    "stress_high_duration_min",
    "stress_recovery_pct_within_2h",
]


def load_sleep_windows() -> dict[date, tuple[datetime, datetime]]:
    """Mirrors extract_sleep_stress.py.load_sleep_windows."""
    out: dict[date, tuple[datetime, datetime]] = {}
    for p in sorted(WELLNESS_DIR.glob("*_sleepData.json")):
        try:
            with p.open(encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as e:
            print(f"  warn: failed to load {p.name}: {e}", file=sys.stderr)
            continue
        if not isinstance(data, list):
            continue
        for rec in data:
            cd = rec.get("calendarDate")
            ss = rec.get("sleepStartTimestampGMT")
            se = rec.get("sleepEndTimestampGMT")
            if not (cd and ss and se):
                continue
            try:
                d = date.fromisoformat(cd)
                s_dt = datetime.fromisoformat(ss.replace(".0", "")).replace(tzinfo=timezone.utc)
                e_dt = datetime.fromisoformat(se.replace(".0", "")).replace(tzinfo=timezone.utc)
            except Exception:
                continue
            if d in out:
                existing = out[d]
                if (e_dt - s_dt) > (existing[1] - existing[0]):
                    out[d] = (s_dt, e_dt)
            else:
                out[d] = (s_dt, e_dt)
    return out


def in_sleep_window(ts: datetime, sleep_windows: dict[date, tuple[datetime, datetime]]) -> bool:
    """Is ts inside ANY sleep window (current or next-day's)?"""
    ts_date = ts.date()
    for candidate in (ts_date, ts_date + timedelta(days=1)):
        win = sleep_windows.get(candidate)
        if win and win[0] <= ts < win[1]:
            return True
    return False


def compute_hr_median_waking(samples: list[tuple[datetime, int]]) -> float | None:
    """First-pass per-day median waking HR.

    Returns None if fewer than HR_MEDIAN_MIN_SAMPLES samples were
    collected (insufficient evidence to claim a reliable daily median).
    """
    if len(samples) < HR_MEDIAN_MIN_SAMPLES:
        return None
    return statistics.median(s for _, s in samples)


def compute_hr_metrics(samples: list[tuple[datetime, int]], baseline: float | None) -> dict:
    """A4 metrics from a day's waking HR samples + the personal daytime baseline.

    samples: list of (timestamp_utc, hr_bpm) for waking minutes only.
    baseline: hr_daytime_baseline_28d for the day (lagged-trailing
              28d median of hr_median_waking). None => all outputs NaN.

    Per-minute binning: build a sparse set of 'was HR above threshold
    during this minute', then walk for longest consecutive run.
    Robust to varying sample cadence (15s / 30s / 1min).
    """
    out = {
        "hr_min_above_daytime_baseline_plus_20_waking": "",
        "hr_longest_elevated_run_min_waking": "",
        "hr_sustained_elevated_flag": "",
        "hr_area_above_daytime_baseline_waking": "",
    }
    if baseline is None or not samples:
        return out
    threshold = baseline + HR_ELEVATION_OFFSET_BPM

    above_minutes: set[int] = set()
    area = 0.0  # sum of (hr - baseline) over above-threshold minutes
    minute_max_hr: dict[int, int] = {}
    for ts, hr in samples:
        minute = ts.hour * 60 + ts.minute
        prev = minute_max_hr.get(minute)
        if prev is None or hr > prev:
            minute_max_hr[minute] = hr
    for m, hr in minute_max_hr.items():
        if hr > threshold:
            above_minutes.add(m)
            area += hr - baseline

    out["hr_min_above_daytime_baseline_plus_20_waking"] = len(above_minutes)
    out["hr_area_above_daytime_baseline_waking"] = round(area, 1)

    # Longest consecutive-minute run
    if not above_minutes:
        out["hr_longest_elevated_run_min_waking"] = 0
        out["hr_sustained_elevated_flag"] = False
    else:
        sorted_min = sorted(above_minutes)
        longest = current = 1
        prev = sorted_min[0]
        for m in sorted_min[1:]:
            if m == prev + 1:
                current += 1
                if current > longest:
                    longest = current
            else:
                current = 1
            prev = m
        out["hr_longest_elevated_run_min_waking"] = longest
        out["hr_sustained_elevated_flag"] = longest >= HR_SUSTAINED_MIN

    return out


def compute_daytime_baselines(
    median_by_date: dict[date, float],
) -> dict[date, float]:
    """Two-pass rolling [d - 90, d - 30] median of per-day waking HR median.

    For each date d, baseline = median of `median_by_date` values over
    [d - HR_BASELINE_WINDOW_END, d - HR_BASELINE_WINDOW_LAG)
    (60 days of history ending 30 days BEFORE d — same shape as the
    v3.2 lagged exertion baseline, so the recent push window does not
    contaminate its own reference).

    Returns: dict mapping date -> baseline. Dates without enough valid
    history (HR_BASELINE_MIN_VALID days within the window) are omitted.
    """
    out: dict[date, float] = {}
    dates_sorted = sorted(median_by_date.keys())
    if not dates_sorted:
        return out
    first_d = dates_sorted[0]
    last_d = dates_sorted[-1] + timedelta(days=HR_BASELINE_WINDOW_LAG)
    d = first_d
    while d <= last_d:
        window_start = d - timedelta(days=HR_BASELINE_WINDOW_END)
        window_end = d - timedelta(days=HR_BASELINE_WINDOW_LAG)  # exclusive upper
        window_vals: list[float] = []
        wd = window_start
        while wd < window_end:
            v = median_by_date.get(wd)
            if v is not None:
                window_vals.append(v)
            wd += timedelta(days=1)
        if len(window_vals) >= HR_BASELINE_MIN_VALID:
            out[d] = statistics.median(window_vals)
        d += timedelta(days=1)
    return out


def compute_stress_metrics(samples: list[tuple[datetime, int]]) -> dict:
    """C4 metrics from a day's waking stress samples.

    samples: list of (timestamp_utc, stress_0_100) for waking minutes only.
    """
    out = {
        "stress_post_peak_drop_avg": "",
        "stress_post_peak_time_to_rest_min": "",
        "stress_high_duration_min": "",
        "stress_recovery_pct_within_2h": "",
    }
    if not samples:
        return out
    samples = sorted(samples, key=lambda x: x[0])

    # stress_high_duration_min: count distinct minutes with stress > 75
    high_minutes: set[int] = set()
    for ts, v in samples:
        if v > STRESS_HIGH_THRESHOLD:
            minute = ts.hour * 60 + ts.minute
            high_minutes.add(minute)
    out["stress_high_duration_min"] = len(high_minutes)

    # Find daily peak
    peak_ts, peak_val = max(samples, key=lambda x: x[1])

    # post_peak_drop_avg: mean stress in the W minutes after peak_ts
    post_window_end = peak_ts + timedelta(minutes=STRESS_POST_PEAK_WINDOW_MIN)
    post_samples = [v for ts, v in samples if peak_ts < ts <= post_window_end]
    if post_samples:
        out["stress_post_peak_drop_avg"] = round(statistics.mean(post_samples), 1)

    # post_peak_time_to_rest_min: minutes from peak until stress < 25
    time_to_rest: int | None = None
    for ts, v in samples:
        if ts <= peak_ts:
            continue
        if v < STRESS_REST_THRESHOLD:
            time_to_rest = int((ts - peak_ts).total_seconds() / 60)
            break
    out["stress_post_peak_time_to_rest_min"] = time_to_rest if time_to_rest is not None else ""

    # recovery_pct_within_2h: percentage stress drop between peak and peak+2h.
    # Find the sample CLOSEST TO peak + 2h (within +/- 15 min); if none in
    # window, NaN.
    target_ts = peak_ts + timedelta(hours=STRESS_RECOVERY_WINDOW_HRS)
    window_lo = target_ts - timedelta(minutes=15)
    window_hi = target_ts + timedelta(minutes=15)
    candidates = [(ts, v) for ts, v in samples if window_lo <= ts <= window_hi]
    if candidates and peak_val > 0:
        candidates.sort(key=lambda x: abs((x[0] - target_ts).total_seconds()))
        _, v_at_2h = candidates[0]
        drop_pct = 100.0 * (peak_val - v_at_2h) / peak_val
        out["stress_recovery_pct_within_2h"] = round(drop_pct, 1)

    return out


def main() -> int:
    if not CLASSIFIED_CSV.exists():
        print(f"ERROR: {CLASSIFIED_CSV} not found", file=sys.stderr)
        return 1

    print("Loading sleep windows from sleepData.json...", file=sys.stderr)
    sleep_windows = load_sleep_windows()
    print(f"  {len(sleep_windows)} dates with sleep windows", file=sys.stderr)

    with CLASSIFIED_CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    mfiles = [r for r in rows if r["type"] == "monitoring_b"]
    print(f"monitoring_b files to parse: {len(mfiles)}", file=sys.stderr)

    open_zips: dict[str, zipfile.ZipFile] = {}
    for z in {r["zip"] for r in mfiles}:
        open_zips[z] = zipfile.ZipFile(GARMIN_DUMP / z)

    # waking_by_date[d] = list of (ts_utc, hr or stress, kind)
    hr_by_date: dict[date, list[tuple[datetime, int]]] = collections.defaultdict(list)
    stress_by_date: dict[date, list[tuple[datetime, int]]] = collections.defaultdict(list)

    for i, r in enumerate(mfiles):
        if i % 500 == 0:
            print(f"  parsed {i}/{len(mfiles)} files", file=sys.stderr)
        try:
            buf = open_zips[r["zip"]].read(r["filename"])
            # Per-file resolver: monitoring_b carries timestamp_16 in
            # most HR samples; resolver needs to be anchored from
            # `monitoring_info.timestamp` (and re-anchored on any full
            # `monitoring.timestamp` it encounters). See fit_utils.py
            # docstring for why this is non-optional.
            resolver = Monitoring16Resolver()
            with fitdecode.FitReader(io.BytesIO(buf)) as fit:
                for frame in fit:
                    if not isinstance(frame, fitdecode.FitDataMessage):
                        continue
                    # Anchor the resolver from monitoring_info frames.
                    if frame.name == "monitoring_info":
                        for f in frame.fields:
                            if f.name == "timestamp" and isinstance(f.value, datetime):
                                anchor = f.value
                                if anchor.tzinfo is None:
                                    anchor = anchor.replace(tzinfo=timezone.utc)
                                resolver.set_reference(anchor)
                        continue
                    # Stress samples (carry their own full stress_level_time)
                    if frame.name == "stress_level":
                        ts_field = next((f for f in frame.fields if f.name == "stress_level_time"), None)
                        val_field = next((f for f in frame.fields if f.name == "stress_level_value"), None)
                        if ts_field and val_field:
                            ts = ts_field.value
                            val = val_field.value
                            if ts and val is not None and isinstance(ts, datetime):
                                try:
                                    v = int(val)
                                except (TypeError, ValueError):
                                    v = None
                                if v is not None and 1 <= v <= 100:
                                    if ts.tzinfo is None:
                                        ts = ts.replace(tzinfo=timezone.utc)
                                    if not in_sleep_window(ts, sleep_windows):
                                        stress_by_date[ts.date()].append((ts, v))
                        continue
                    # HR samples — in monitoring frames; timestamp is usually
                    # timestamp_16, requiring resolver.resolve_frame().
                    if frame.name != "monitoring":
                        continue
                    hr_field = next((f for f in frame.fields if f.name == "heart_rate"), None)
                    if hr_field is None or hr_field.value is None:
                        continue
                    try:
                        hr_i = int(hr_field.value)
                    except (TypeError, ValueError):
                        continue
                    if hr_i < 30 or hr_i > 220:
                        continue
                    ts = resolver.resolve_frame(frame)
                    if ts is None:
                        continue
                    if ts.tzinfo is None:
                        ts = ts.replace(tzinfo=timezone.utc)
                    if not in_sleep_window(ts, sleep_windows):
                        hr_by_date[ts.date()].append((ts, hr_i))
        except Exception as e:
            print(f"  warn: failed {r['filename']}: {e}", file=sys.stderr)
            continue

    print(f"parsed waking HR samples for {len(hr_by_date)} dates", file=sys.stderr)
    print(f"parsed waking stress samples for {len(stress_by_date)} dates", file=sys.stderr)

    # Pass 2: per-day median + rolling [d-90, d-30] lagged baseline
    print(
        f"computing hr_median_waking + [d-{HR_BASELINE_WINDOW_END}, d-{HR_BASELINE_WINDOW_LAG}] lagged baseline "
        f"(min {HR_MEDIAN_MIN_SAMPLES} samples/day, min {HR_BASELINE_MIN_VALID} valid days in window)...",
        file=sys.stderr,
    )
    median_by_date: dict[date, float] = {}
    for d in hr_by_date:
        m = compute_hr_median_waking(hr_by_date[d])
        if m is not None:
            median_by_date[d] = m
    print(f"  {len(median_by_date)} dates with valid hr_median_waking", file=sys.stderr)
    baseline_by_date = compute_daytime_baselines(median_by_date)
    print(f"  {len(baseline_by_date)} dates with valid hr_daytime_baseline_lagged", file=sys.stderr)

    # Emit per-day CSV
    all_dates = sorted(set(hr_by_date.keys()) | set(stress_by_date.keys()))
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for d in all_dates:
            row = {"date": d.isoformat()}
            m = median_by_date.get(d)
            row["hr_median_waking"] = round(m, 1) if m is not None else ""
            bl = baseline_by_date.get(d)
            row["hr_daytime_baseline_lagged"] = round(bl, 1) if bl is not None else ""
            row.update(compute_hr_metrics(hr_by_date.get(d, []), bl))
            row.update(compute_stress_metrics(stress_by_date.get(d, [])))
            w.writerow(row)
    print(f"\nWrote {len(all_dates)} rows to {OUT_CSV}", file=sys.stderr)

    # Fill-rate summary
    rows_check = list(csv.DictReader(OUT_CSV.open(encoding="utf-8")))
    print("\nFill rates:")
    for f in FIELDS[1:]:
        n = sum(1 for r in rows_check if r[f] not in ("", None))
        print(f"  {f}: {n}/{len(rows_check)} ({100*n/len(rows_check):.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
