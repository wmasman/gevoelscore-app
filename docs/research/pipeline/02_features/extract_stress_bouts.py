"""extract_stress_bouts.py — bout-level stress dataset extractor.

Producer-mode implementation of `methodology/bout_level_recovery_dynamics.md`
(LOCKED `c57ff3f` 2026-06-21). Builds per-bout + per-day-aggregation datasets
from per-minute Garmin stress traces.

## Inputs

- Per-minute stress + intensity samples re-parsed from `monitoring_b` FIT
  files via the same pattern as `pipeline/01_extract/stress_low_motion_extract.py`
  and `analyses/hypotheses/HA11-stress-udip/extract_udip_counts.py`. No
  per-minute cache exists; the extractor re-parses each run.
- Sleep windows from Garmin `sleepData.json` (same loader as
  `pipeline/01_extract/garmin_intraday_hr_stress.py`). Used for
  `bout_during_sleep_flag` (§4) + `truncated_at_sleep_flag` (§3.2).
- `daily_uds.csv` for the 21-day device-baseline-lag gate (§3.4).

## Outputs (external, gitignored)

- `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.csv` — one row per bout.
- `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.parquet` — sidecar.
- `$GEVOELSCORE_DATA_PATH/unified/per_bout_aggregations_daily.csv` — per-day
  aggregations (5 columns per user-ratified Decision 2). Consumed by
  `pipeline/03_consolidate/build_unified_dataset.py` for the per-day-master
  join.

## Bout-detection rule (per MD §3, LOCKED)

- **Onset** (§3.1): `stress(t) >= 60 AND stress(t-1) < 60` AND pre-window
  `[t-20, t-5]` has >= 10 of 15 minutes with `stress < 50`.
- **Peak** (§3.1): max stress in `[t_onset, t_onset+120]`.
- **Pre-bout baseline** (§3.3): mean of stress over `[t_onset-30, t_onset-5]`
  restricted to valid minutes (`stress in [1, 100]`); requires >= 15 of 25
  valid; else `baseline_invalid_flag = True`.
- **End** (§3.2): first minute in `[t_peak+5, t_peak+180]` where
  `stress(t) <= pre_bout_baseline + 5` for >= 10 consecutive minutes; if not
  reached, `did_not_return_flag = True` and `t_end = t_peak + 180`.
- **Min within-bout duration** (§3.1): `t_peak - t_onset >= 5` else
  `transient_flag = True` (still included in primary operand per the r2
  absorb pinned in §3.1).
- **Min separation** (§3.1): consecutive bouts must have
  `t_onset(bout_{k+1}) - t_end(bout_k) >= 60` minutes.

## Per-bout features (per MD §4, LOCKED)

See §4's table. All 22 columns emitted; NaN semantics per the same table.
`bout_id` uses 1-based within-day indexing (`<date>_<bout_index>`). Calendar
attribution per §3.2: bouts span calendar boundaries are attributed to the
day of `t_peak`.

## Per-day aggregations (per MD §4 + user-ratified Decision 2)

The Moderate 5-column set:
- `bout_n_fast_recovery_day` — count of bouts with `recovery_half_life <= 15`
  AND `tail_length <= 45` (per §6.1; framework-validity operand)
- `bout_n_per_day` — total bout count
- `bout_n_did_not_return` — count of `did_not_return_flag = True`
- `bout_max_peak_height_day` — max `peak_height` (NaN if no bouts)
- `bout_total_AUC_day` — sum of `AUC_above_baseline` across day's bouts

Convention: count columns emit 0 on valid days with no bouts; max/AUC emit
NaN. Invalid days (failing the §3.4 gate) emit NaN on all 5.

## Personal-baseline SD-anchored derivative operand family (per MD §3.2.2 LOCKED r3 2026-07-09)

Additive derivative family co-locked with HA-C4cp r2 pre-reg at Bundle H+
event 7 (2026-07-09). Reference distribution `tail_length_lagged_lcera(d)`
constructed per §3.2.2: bout-level pool over `[d-90, d-30]` window,
restricted to LC-era valid days (April 2024 cluster excluded via the
§3.4 gate; `did_not_return_flag` bouts INCLUDED as-is per §3.2.2 rationale
to avoid inflating derivative flag rate; candidate-day exclusion enforced
by window edge). Robust statistics: `subject_lagged_median(d) = median`;
`subject_lagged_mad(d) = 1.4826 * MAD`. Validity bar: >= 30 bouts in
reference pool.

Per-bout derivative features (3 new columns added to per_bout_master.csv):
- `bout_return_time_z` — continuous z-score
  `(tail_length - subject_lagged_median) / subject_lagged_mad`
- `did_not_return_1sd_flag` — bool: `tail_length > median + 1*mad`
- `did_not_return_2sd_flag` — bool: `tail_length > median + 2*mad`

Per-day aggregations (5 new columns added to per_bout_aggregations_daily.csv):
- `subject_lagged_median_day` — reference-window median (audit trace)
- `subject_lagged_mad_day` — reference-window `1.4826 * MAD` (audit trace)
- `bout_return_time_z_max_day` — max over day's bouts of `bout_return_time_z`
- `bout_n_did_not_return_1sd_day` — count of `did_not_return_1sd_flag = True`
- `bout_n_did_not_return_2sd_day` — count of `did_not_return_2sd_flag = True`
  (HA-C4cp primary per-day operand)

NaN semantics: count columns emit 0 on valid days with valid reference
window and no flagged bouts; NaN on reference-window-invalid days
(< 30 bouts in `[d-90, d-30]`) OR §3.4-invalid days. `.fillna(0)` on the
count columns MUST distinguish these cases per parent MD §4 zero-vs-NaN
discipline; silently promoting NaN to 0 would fold reference-window-invalid
days into zero-count days and bias downstream contrasts toward null.

## Day-validity gate (per MD §3.4)

A day enters the bout dataset if:
- `>= 600` valid per-minute stress samples on `d` (HA11-style coverage gate),
- `d >= 2022-04-04` (LC era start),
- `d` is NOT in the first 21 days of `has_garmin_uds=True` coverage
  (device-baseline lag per Wiggers PDF lines 99-106),
- `d` is NOT in `[2024-04-09, 2024-04-16]` (April-2024 cluster, structurally
  unanalysable per `citalopram_phase_stratification.md`).

Days failing the gate produce no bouts (per-day aggregations = NaN).

## Citalopram-phase metadata join (per MD §4)

Each bout inherits its day's `dose_plasma_mg`, `citalopram_phase`,
`is_unmedicated`. Phase boundaries are loaded from
`methodology/citalopram_phase_stratification.md §3` (table at lines 124-128
of that MD, also the canonical `citalopram_phase` helper at lines 162-171).
PK formula + step dates mirror
`pipeline/03_consolidate/build_unified_dataset.py` lines 571-588.

## Verification (per user-ratified Decision 4)

- 5 spot-checks against per-minute trace (printed at end of run if
  `--verify` is passed).
- Edge-case smoke tests inline as assertions on tiny synthetic traces
  (NaN handling + midnight-spanning + did_not_return firing). Runnable
  standalone via `--smoke-tests`.

NO formal pytest suite — pipeline is data-extraction, not algorithmic
logic. Re-runnable + re-verifiable on the same data.
"""
from __future__ import annotations

import argparse
import bisect
import collections
import csv
import io
import json
import math
import os
import statistics
import sys
import zipfile
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

import fitdecode

# === Path setup (shared pattern with stress_low_motion_extract.py) ===
HERE = Path(__file__).resolve().parent
# 02_features -> pipeline -> research -> docs -> repo
REPO_ROOT = HERE.parent.parent.parent.parent
RESEARCH_ROOT = REPO_ROOT / "docs" / "research"
# Allow import of the shared Monitoring16Resolver (single source of truth
# for timestamp_16 rollover; see fit_utils.py docstring).
sys.path.insert(0, str(RESEARCH_ROOT / "analyses" / "garmin_exploration" / "scripts"))
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
DATA_PATH = Path(os.environ.get("GEVOELSCORE_DATA_PATH", ""))
if not DATA_PATH or not DATA_PATH.exists():
    raise SystemExit("GEVOELSCORE_DATA_PATH not set or does not exist.")

GARMIN_DUMP = DATA_PATH / "garmin data" / "DI_CONNECT" / "DI-Connect-Uploaded-Files"
WELLNESS_DIR = DATA_PATH / "garmin data" / "DI_CONNECT" / "DI-Connect-Wellness"
CLASSIFIED_CSV = DATA_PATH / "analyses" / "garmin_exploration" / "fit_files_classified.csv"
DAILY_UDS = DATA_PATH / "processed" / "garmin" / "daily_uds.csv"
OUT_DIR = DATA_PATH / "unified"
OUT_BOUT_CSV = OUT_DIR / "per_bout_master.csv"
OUT_BOUT_PARQUET = OUT_DIR / "per_bout_master.parquet"
OUT_AGG_CSV = OUT_DIR / "per_bout_aggregations_daily.csv"

# === Bout-detection thresholds (per MD §3, LOCKED) ===
STRESS_VALID_MIN = 1
STRESS_VALID_MAX = 100
ONSET_THRESHOLD = 60               # §3.1: stress >= 60 to start a bout
HYSTERESIS_FLOOR = 50              # §3.1: pre-window 10 of 15 minutes < 50
HYST_WINDOW_START_BEFORE = 20      # §3.1: pre-window starts t_onset - 20
HYST_WINDOW_END_BEFORE = 5         # §3.1: pre-window ends t_onset - 5
HYST_WINDOW_MIN_VALID = 10         # §3.1: at least 10 of 15 minutes < 50
PEAK_FORWARD_WINDOW_MIN = 120      # §3.1: peak in [t_onset, t_onset + 120]
MIN_BOUT_DURATION_MIN = 5          # §3.1: t_peak - t_onset >= 5 else transient
MIN_SEPARATION_MIN = 60            # §3.1: between t_end(k) and t_onset(k+1)
BASELINE_START_BEFORE = 30         # §3.3: baseline window starts t_onset - 30
BASELINE_END_BEFORE = 5            # §3.3: baseline window ends t_onset - 5
BASELINE_MIN_VALID = 15            # §3.3: 15 of 25 valid; else baseline_invalid
RETURN_FORWARD_CAP_MIN = 180       # §3.2: 180-min cap; did_not_return if not met
RETURN_MIN_START_AFTER = 5         # §3.2: return window starts t_peak + 5
RETURN_TOLERANCE = 5               # §3.2: return-to-within +5 of baseline
RETURN_RUN_MIN = 10                # §3.2: >= 10 consecutive minutes
HALFLIFE_RUN_MIN = 5               # §4: recovery_half_life requires >= 5 cons.
HALFLIFE_CAP_MIN = 180             # §4: cap at 180 with did_not_half_recover

MIN_SAMPLES_FOR_VALID_DAY = 600    # §3.4: HA11-style coverage gate
LC_ERA_START = date(2022, 4, 4)    # §3.4: LC era boundary
DEVICE_LAG_DAYS = 21               # §3.4: first 21 days of has_garmin_uds
APRIL2024_CLUSTER_START = date(2024, 4, 9)
APRIL2024_CLUSTER_END = date(2024, 4, 16)

# Motion-class threshold (per §3.4 + stress_low_motion_primitive.md §3.2).
# motion-class >= moderate <=> Garmin intensity >= 2 (low=1, moderate=2,
# vigorous=3). Per §3.4 r2 absorb: when per-minute intensity record is
# ABSENT across the bout window, motion_confound_flag = NaN (NOT False).
INTENSITY_MODERATE = 2

# === Citalopram phase boundaries (per MD §3 lines 124-128 + §3 helper) ===
# Verbatim from citalopram_phase_stratification.md §3 (LOCKED). Step dates
# also mirror build_unified_dataset.py lines 580-587.
CITALOPRAM_PHASE_BOUNDARIES = [
    (date(2024, 4, 9), "unmedicated"),       # d < 2024-04-09 -> unmedicated
    (date(2024, 6, 20), "buildup"),           # 2024-04-09 <= d < 2024-06-20
    (date(2026, 3, 20), "consolidation"),     # 2024-06-20 <= d < 2026-03-20
    (date(2026, 6, 6), "afbouw"),             # 2026-03-20 <= d < 2026-06-06
    # 2026-06-06 onwards -> post_afbouw
]
CITALOPRAM_T_HALF_HOURS = 35.0
CITALOPRAM_T_HALF_DAYS = CITALOPRAM_T_HALF_HOURS / 24.0
CITALOPRAM_DECAY_K = math.log(2.0) / CITALOPRAM_T_HALF_DAYS
CITALOPRAM_DOSE_STEPS = [
    (date(2024,  4,  9), +10.0),
    (date(2024,  5,  5), +10.0),
    (date(2024,  6, 20), +10.0),
    (date(2026,  3, 20), -10.0),
    (date(2026,  4, 17), -10.0),
    (date(2026,  5, 27),  -2.0),
]
CITALOPRAM_INITIAL_DOSE_MG = 0.0


def citalopram_phase(d: date) -> str:
    """Canonical phase per citalopram_phase_stratification.md §3 lines 162-171."""
    for boundary, label in CITALOPRAM_PHASE_BOUNDARIES:
        if d < boundary:
            return label
    return "post_afbouw"


def dose_plasma_mg(d: date) -> float:
    """PK-smoothed plasma dose per citalopram_phase_stratification.md §3 +
    build_unified_dataset.py lines 590-600 mirror."""
    val = CITALOPRAM_INITIAL_DOSE_MG
    for step_date, delta in CITALOPRAM_DOSE_STEPS:
        if d >= step_date:
            days_since = (d - step_date).days
            val += delta * (1.0 - math.exp(-CITALOPRAM_DECAY_K * days_since))
    return round(val, 4)


# === Per-bout CSV schema (per MD §4, LOCKED) ===
PER_BOUT_FIELDS = [
    "bout_id",
    "date",
    "bout_index_within_day",
    "t_onset",
    "t_peak",
    "t_end",
    "peak_height",
    "peak_minute",
    "pre_bout_baseline",
    "peak_minus_baseline",
    "recovery_half_life",
    "tail_length",
    "decay_slope",
    "AUC_above_baseline",
    "motion_confound_flag",
    "did_not_return_flag",
    "did_not_half_recover_flag",
    "baseline_invalid_flag",
    "truncated_at_sleep_flag",
    "multi_peak_flag",
    "transient_flag",
    "bout_during_sleep_flag",
    # Citalopram covariates (per MD §4 + Approach A inputs)
    "dose_plasma_mg",
    "citalopram_phase",
    "is_unmedicated",
    # Personal-baseline SD-anchored derivative features (per MD §3.2.2 LOCKED r3)
    "bout_return_time_z",
    "did_not_return_1sd_flag",
    "did_not_return_2sd_flag",
]

# === Per-day aggregations schema (5 + 5 = 10 columns) ===
# First 5 per Decision 2 (LOCKED 2026-06-22); last 5 per MD §3.2.2 LOCKED r3.
PER_DAY_AGG_FIELDS = [
    "date",
    "bout_n_fast_recovery_day",
    "bout_n_per_day",
    "bout_n_did_not_return",
    "bout_max_peak_height_day",
    "bout_total_AUC_day",
    # SD-anchored derivative operand family (MD §3.2.2 LOCKED r3)
    "subject_lagged_median_day",
    "subject_lagged_mad_day",
    "bout_return_time_z_max_day",
    "bout_n_did_not_return_1sd_day",
    "bout_n_did_not_return_2sd_day",
]

# Fast-recovery operand thresholds (per MD §6.1, LOCKED)
FAST_RECOVERY_HALFLIFE_MAX = 15    # recovery_half_life <= 15
FAST_RECOVERY_TAIL_MAX = 45        # tail_length <= 45

# SD-anchored operand family constants (per MD §3.2.2 LOCKED r3)
LAGGED_WINDOW_LOOKBACK_START = 90  # `[d-90, d-30]` left edge (inclusive)
LAGGED_WINDOW_LOOKBACK_END = 30    # `[d-90, d-30]` right edge (inclusive)
MIN_REFERENCE_POOL_SIZE = 30       # >= 30 bouts validity bar per §3.2.2
MAD_SCALE_TO_SD = 1.4826           # normal-consistent scaling per CONVENTIONS §3.1


# === Sleep-window loader (mirrors garmin_intraday_hr_stress.py) ===

def load_sleep_windows() -> dict[date, tuple[datetime, datetime]]:
    out: dict[date, tuple[datetime, datetime]] = {}
    if not WELLNESS_DIR.exists():
        return out
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


def is_in_sleep_window(ts: datetime, sleep_windows: dict[date, tuple[datetime, datetime]]) -> bool:
    ts_date = ts.date()
    for candidate in (ts_date - timedelta(days=1), ts_date, ts_date + timedelta(days=1)):
        win = sleep_windows.get(candidate)
        if win and win[0] <= ts < win[1]:
            return True
    return False


def get_sleep_onset_after(ts: datetime, sleep_windows: dict[date, tuple[datetime, datetime]]) -> datetime | None:
    """Returns the earliest sleep-window start strictly after ts. Used by
    §3.2 truncated_at_sleep_flag logic (bout's return-window lands inside
    sleep -> truncate at sleep_onset)."""
    candidates: list[datetime] = []
    ts_date = ts.date()
    for offset in (-1, 0, 1):
        d = ts_date + timedelta(days=offset)
        win = sleep_windows.get(d)
        if win and win[0] > ts:
            candidates.append(win[0])
    return min(candidates) if candidates else None


# === has_garmin_uds dates from daily_uds.csv (for the 21-day device-baseline gate) ===

def load_uds_dates() -> set[date]:
    """Return the set of dates where Garmin UDS coverage is present.
    Used for the §3.4 device-baseline-lag gate (excludes first 21 days of
    has_garmin_uds=True)."""
    if not DAILY_UDS.exists():
        return set()
    out: set[date] = set()
    with DAILY_UDS.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d_str = r.get("date") or ""
            try:
                d = date.fromisoformat(d_str)
            except (ValueError, TypeError):
                continue
            # Presence-of-row in daily_uds.csv = has_garmin_uds. The
            # extractor only checks coverage existence, not specific
            # column non-NaN — mirrors build_unified_dataset.py's
            # has_garmin_uds = bool(u).
            out.add(d)
    return out


def device_baseline_excluded(d: date, uds_dates: set[date]) -> bool:
    """True iff d is in the first 21 days of has_garmin_uds coverage.
    Implements §3.4 device-baseline-lag gate."""
    if not uds_dates:
        return False
    first_uds = min(uds_dates)
    return d < first_uds + timedelta(days=DEVICE_LAG_DAYS)


def day_valid(d: date, sample_count: int, uds_dates: set[date]) -> bool:
    """§3.4 day-validity gate."""
    if sample_count < MIN_SAMPLES_FOR_VALID_DAY:
        return False
    if d < LC_ERA_START:
        return False
    if device_baseline_excluded(d, uds_dates):
        return False
    if APRIL2024_CLUSTER_START <= d <= APRIL2024_CLUSTER_END:
        return False
    return True


# === Bout detection on a per-minute trace ===

def detect_bouts_on_day(
    minute_stress: dict[datetime, int],
    minute_intensity: dict[datetime, int | None],
    sleep_windows: dict[date, tuple[datetime, datetime]],
    day_date: date,
) -> list[dict]:
    """Detect bouts on a per-minute stress trace (for a single calendar day).

    Returns list of per-bout dicts with all PER_BOUT_FIELDS columns populated
    (except the citalopram fields, joined by the caller).

    minute_stress: dict mapping per-minute datetime (second=0, microsecond=0,
                   tz-aware UTC) -> stress 0-100. Only valid in-range samples.
    minute_intensity: dict mapping per-minute datetime (same keying) ->
                      intensity tier (0 / 1 / 2 / 3) or None if no record.

    Per MD §3.2: bouts spanning calendar boundary are attributed to day of
    t_peak. This function should be called once per day-of-t_onset; bouts
    whose t_peak lands on a different calendar day need re-attribution
    upstream. To keep the implementation simple and avoid double-counting,
    we run detection on a sorted per-minute stream that covers all minutes
    in the corpus (not per-day), and attribute each bout to t_peak's date
    inside the loop. The caller passes a per-day slice that has 2-hour
    spillover at the boundaries to capture cross-midnight bouts.
    """
    bouts: list[dict] = []
    if not minute_stress:
        return bouts

    sorted_minutes = sorted(minute_stress.keys())
    minute_set = set(sorted_minutes)
    last_t_end: datetime | None = None
    bout_index = 0

    # Scan for onset crossings.
    for t in sorted_minutes:
        if minute_stress[t] < ONSET_THRESHOLD:
            continue
        # Need upward crossing: previous minute < 60 (or no previous minute,
        # in which case skip — first minute of trace can't be a confirmed
        # crossing).
        t_prev = t - timedelta(minutes=1)
        if t_prev not in minute_set:
            continue
        if minute_stress[t_prev] >= ONSET_THRESHOLD:
            continue
        # Minimum separation: must be >= MIN_SEPARATION_MIN minutes after
        # the prior bout's t_end.
        if last_t_end is not None and (t - last_t_end).total_seconds() < MIN_SEPARATION_MIN * 60:
            continue
        # Hysteresis pre-window check: 10 of 15 minutes in
        # [t - 20, t - 5] must have stress < 50.
        hyst_start = t - timedelta(minutes=HYST_WINDOW_START_BEFORE)
        hyst_end = t - timedelta(minutes=HYST_WINDOW_END_BEFORE)
        below = 0
        total = 0
        scan = hyst_start
        while scan < hyst_end:
            v = minute_stress.get(scan)
            if v is not None:
                total += 1
                if v < HYSTERESIS_FLOOR:
                    below += 1
            scan += timedelta(minutes=1)
        if below < HYST_WINDOW_MIN_VALID:
            continue
        t_onset = t

        # Peak: max stress in [t_onset, t_onset + 120].
        peak_end_excl = t_onset + timedelta(minutes=PEAK_FORWARD_WINDOW_MIN)
        peak_window: list[tuple[datetime, int]] = []
        scan = t_onset
        while scan < peak_end_excl:
            v = minute_stress.get(scan)
            if v is not None:
                peak_window.append((scan, v))
            scan += timedelta(minutes=1)
        if not peak_window:
            continue
        # Tie-break: earliest minute wins (preserves causal ordering).
        peak_window.sort(key=lambda x: (-x[1], x[0]))
        t_peak, peak_height = peak_window[0]

        # Pre-bout baseline (§3.3): mean of stress over [t_onset - 30, t_onset - 5]
        # restricted to valid minutes; requires >= 15 of 25 valid.
        bl_start = t_onset - timedelta(minutes=BASELINE_START_BEFORE)
        bl_end = t_onset - timedelta(minutes=BASELINE_END_BEFORE)
        bl_vals: list[int] = []
        scan = bl_start
        while scan < bl_end:
            v = minute_stress.get(scan)
            if v is not None:
                bl_vals.append(v)
            scan += timedelta(minutes=1)
        baseline_invalid_flag = len(bl_vals) < BASELINE_MIN_VALID
        pre_bout_baseline: float | None = (
            None if baseline_invalid_flag else float(statistics.mean(bl_vals))
        )

        # End (§3.2): first minute in [t_peak + 5, t_peak + 180] where
        # stress <= baseline + 5 for >= 10 consecutive minutes.
        return_start = t_peak + timedelta(minutes=RETURN_MIN_START_AFTER)
        return_cap = t_peak + timedelta(minutes=RETURN_FORWARD_CAP_MIN)
        t_end: datetime
        did_not_return_flag = False
        if pre_bout_baseline is None:
            # Cannot define return condition without a baseline; bout ends
            # at the cap with did_not_return_flag = True (no return-fit
            # could be confirmed).
            t_end = return_cap
            did_not_return_flag = True
        else:
            tolerance_target = pre_bout_baseline + RETURN_TOLERANCE
            run = 0
            run_start: datetime | None = None
            scan = return_start
            t_end_resolved: datetime | None = None
            while scan < return_cap:
                v = minute_stress.get(scan)
                if v is not None and v <= tolerance_target:
                    if run == 0:
                        run_start = scan
                    run += 1
                    if run >= RETURN_RUN_MIN:
                        t_end_resolved = run_start
                        break
                else:
                    run = 0
                    run_start = None
                scan += timedelta(minutes=1)
            if t_end_resolved is not None:
                t_end = t_end_resolved
            else:
                t_end = return_cap
                did_not_return_flag = True

        # §3.2 sleep-boundary truncation: if t_peak in waking and the return
        # window crosses sleep onset, truncate t_end at sleep onset.
        truncated_at_sleep_flag = False
        peak_in_sleep = is_in_sleep_window(t_peak, sleep_windows)
        if not peak_in_sleep:
            sleep_onset = get_sleep_onset_after(t_peak, sleep_windows)
            if sleep_onset is not None and t_peak < sleep_onset < t_end:
                t_end = sleep_onset
                truncated_at_sleep_flag = True

        # Transient + min-duration check (§3.1)
        transient_flag = (t_peak - t_onset).total_seconds() < MIN_BOUT_DURATION_MIN * 60

        # Multi-peak flag (§3.4): are there other local maxima exceeding
        # peak_height - 10 in [t_onset, t_end]?
        multi_peak_flag = False
        scan = t_onset
        while scan <= t_end:
            v = minute_stress.get(scan)
            if v is not None and v >= (peak_height - 10) and scan != t_peak:
                # Local-maximum-ness: stress >= immediate neighbours.
                prev_v = minute_stress.get(scan - timedelta(minutes=1))
                next_v = minute_stress.get(scan + timedelta(minutes=1))
                if prev_v is not None and next_v is not None and v >= prev_v and v >= next_v:
                    multi_peak_flag = True
                    break
            scan += timedelta(minutes=1)

        # recovery_half_life (§4): time from t_peak to first minute where
        # stress <= baseline + (peak_height - baseline) / 2 for >= 5
        # consecutive minutes; capped at 180 with did_not_half_recover.
        recovery_half_life: float | None = None
        did_not_half_recover_flag = False
        if pre_bout_baseline is None:
            recovery_half_life = None
        else:
            half_target = pre_bout_baseline + (peak_height - pre_bout_baseline) / 2.0
            cap_t = t_peak + timedelta(minutes=HALFLIFE_CAP_MIN)
            scan = t_peak
            run = 0
            half_t: datetime | None = None
            while scan <= cap_t:
                v = minute_stress.get(scan)
                if v is not None and v <= half_target:
                    if run == 0:
                        half_run_start = scan
                    run += 1
                    if run >= HALFLIFE_RUN_MIN:
                        half_t = half_run_start
                        break
                else:
                    run = 0
                scan += timedelta(minutes=1)
            if half_t is not None:
                recovery_half_life = (half_t - t_peak).total_seconds() / 60.0
            else:
                recovery_half_life = float(HALFLIFE_CAP_MIN)
                did_not_half_recover_flag = True

        # tail_length (§4): t_end - t_peak in minutes
        tail_length = (t_end - t_peak).total_seconds() / 60.0

        # decay_slope (§4): linear regression slope of stress on minute over
        # [t_peak, t_end]. NaN if t_end - t_peak < 10 minutes.
        decay_slope: float | None = None
        decay_pts: list[tuple[float, int]] = []
        scan = t_peak
        while scan <= t_end:
            v = minute_stress.get(scan)
            if v is not None:
                decay_pts.append(((scan - t_peak).total_seconds() / 60.0, v))
            scan += timedelta(minutes=1)
        if (t_end - t_peak).total_seconds() / 60.0 >= 10 and len(decay_pts) >= 3:
            n = len(decay_pts)
            mean_x = sum(p[0] for p in decay_pts) / n
            mean_y = sum(p[1] for p in decay_pts) / n
            num = sum((p[0] - mean_x) * (p[1] - mean_y) for p in decay_pts)
            den = sum((p[0] - mean_x) ** 2 for p in decay_pts)
            decay_slope = num / den if den > 0 else None

        # AUC_above_baseline (§4): sum of max(0, stress(t) - baseline) over
        # [t_onset, t_end]. NaN propagates from pre_bout_baseline.
        auc: float | None = None
        if pre_bout_baseline is not None:
            auc = 0.0
            scan = t_onset
            while scan <= t_end:
                v = minute_stress.get(scan)
                if v is not None:
                    auc += max(0.0, v - pre_bout_baseline)
                scan += timedelta(minutes=1)

        # motion_confound_flag (§3.4): True if any minute in [t_onset, t_end]
        # has intensity >= INTENSITY_MODERATE. NaN if NO minute in the window
        # has an intensity record (per r2 absorb #4).
        motion_confound_flag: bool | None
        scan = t_onset
        any_record = False
        motion_seen = False
        while scan <= t_end:
            iv = minute_intensity.get(scan)
            if iv is not None:
                any_record = True
                if iv >= INTENSITY_MODERATE:
                    motion_seen = True
                    break
            scan += timedelta(minutes=1)
        if not any_record:
            motion_confound_flag = None
        else:
            motion_confound_flag = motion_seen

        # bout_during_sleep_flag (§4): t_peak in sleep window.
        bout_during_sleep_flag = peak_in_sleep

        # Date attribution: t_peak's calendar date per §3.2.
        attr_date = t_peak.date()

        bout_index += 1
        bouts.append({
            "bout_id": f"{attr_date.isoformat()}_{bout_index}",
            "date": attr_date.isoformat(),
            "bout_index_within_day": bout_index,
            "t_onset": t_onset.isoformat(),
            "t_peak": t_peak.isoformat(),
            "t_end": t_end.isoformat(),
            "peak_height": int(peak_height),
            "peak_minute": t_peak.hour * 60 + t_peak.minute,
            "pre_bout_baseline": (
                round(pre_bout_baseline, 2) if pre_bout_baseline is not None else None
            ),
            "peak_minus_baseline": (
                round(peak_height - pre_bout_baseline, 2)
                if pre_bout_baseline is not None else None
            ),
            "recovery_half_life": (
                round(recovery_half_life, 1) if recovery_half_life is not None else None
            ),
            "tail_length": round(tail_length, 1),
            "decay_slope": round(decay_slope, 4) if decay_slope is not None else None,
            "AUC_above_baseline": round(auc, 1) if auc is not None else None,
            "motion_confound_flag": motion_confound_flag,
            "did_not_return_flag": did_not_return_flag,
            "did_not_half_recover_flag": did_not_half_recover_flag,
            "baseline_invalid_flag": baseline_invalid_flag,
            "truncated_at_sleep_flag": truncated_at_sleep_flag,
            "multi_peak_flag": multi_peak_flag,
            "transient_flag": transient_flag,
            "bout_during_sleep_flag": bout_during_sleep_flag,
        })
        last_t_end = t_end

    return bouts


# === Per-day aggregations from the per-bout dataset ===

def aggregate_per_day(
    bouts: list[dict],
    valid_dates: set[date],
    sd_anchored_per_day: dict[str, dict] | None = None,
) -> list[dict]:
    """Compute per-day aggregations.

    First 5 columns per Decision 2 (LOCKED 2026-06-22).
    Next 5 columns per MD §3.2.2 LOCKED r3 (SD-anchored derivative family)
    when `sd_anchored_per_day` is provided.
    """
    by_date: dict[date, list[dict]] = collections.defaultdict(list)
    for b in bouts:
        try:
            d = date.fromisoformat(b["date"])
        except (ValueError, TypeError):
            continue
        by_date[d].append(b)

    sd_anchored_per_day = sd_anchored_per_day or {}

    out: list[dict] = []
    for d in sorted(valid_dates | set(by_date.keys())):
        row: dict[str, object] = {"date": d.isoformat()}
        if d not in valid_dates:
            # Invalid day -> NaN on all 10 aggregations.
            row["bout_n_fast_recovery_day"] = ""
            row["bout_n_per_day"] = ""
            row["bout_n_did_not_return"] = ""
            row["bout_max_peak_height_day"] = ""
            row["bout_total_AUC_day"] = ""
            row["subject_lagged_median_day"] = ""
            row["subject_lagged_mad_day"] = ""
            row["bout_return_time_z_max_day"] = ""
            row["bout_n_did_not_return_1sd_day"] = ""
            row["bout_n_did_not_return_2sd_day"] = ""
            out.append(row)
            continue
        day_bouts = by_date.get(d, [])
        row["bout_n_per_day"] = len(day_bouts)
        row["bout_n_did_not_return"] = sum(
            1 for b in day_bouts if b["did_not_return_flag"]
        )
        # bout_n_fast_recovery_day requires recovery_half_life AND tail_length
        # to be non-None and <= thresholds (per §6.1).
        row["bout_n_fast_recovery_day"] = sum(
            1 for b in day_bouts
            if b["recovery_half_life"] is not None
            and b["recovery_half_life"] <= FAST_RECOVERY_HALFLIFE_MAX
            and b["tail_length"] <= FAST_RECOVERY_TAIL_MAX
        )
        # bout_max_peak_height_day + bout_total_AUC_day: NaN if no bouts.
        if day_bouts:
            row["bout_max_peak_height_day"] = max(b["peak_height"] for b in day_bouts)
            aucs = [b["AUC_above_baseline"] for b in day_bouts if b["AUC_above_baseline"] is not None]
            row["bout_total_AUC_day"] = round(sum(aucs), 1) if aucs else ""
        else:
            row["bout_max_peak_height_day"] = ""
            row["bout_total_AUC_day"] = 0.0

        # SD-anchored derivative operand family (per MD §3.2.2). Empty
        # string on missing (reference-window-invalid); the None -> ""
        # normalisation is CSV-writer's job downstream.
        sd = sd_anchored_per_day.get(d.isoformat(), {})
        for col in (
            "subject_lagged_median_day",
            "subject_lagged_mad_day",
            "bout_return_time_z_max_day",
            "bout_n_did_not_return_1sd_day",
            "bout_n_did_not_return_2sd_day",
        ):
            v = sd.get(col)
            row[col] = "" if v is None else v

        out.append(row)
    return out


# === Personal-baseline SD-anchored derivative operand family (per MD §3.2.2 LOCKED r3) ===

def compute_sd_anchored_features(
    all_bouts: list[dict],
    valid_dates: set[date],
) -> dict[str, dict]:
    """Compute personal-baseline SD-anchored derivative features per MD §3.2.2.

    For each valid day `d`:
      1. Build reference pool of `tail_length` values from bouts on days in
         `[d-90, d-30]` that pass the §3.4 day-validity gate (`valid_dates`
         already enforces LC-era + April 2024 cluster + device-baseline-lag
         exclusions).
      2. If pool size < 30 (MD §3.2.2 validity bar), mark day + its bouts NaN.
      3. Else compute `subject_lagged_median` = median; `subject_lagged_mad`
         = 1.4826 * MAD (robust per CONVENTIONS §3.1 prototype).
      4. For each bout on day `d`: compute `bout_return_time_z`,
         `did_not_return_1sd_flag`, `did_not_return_2sd_flag`. Mutate the
         bout dict in place.
      5. Return per-day aggregations {median, mad, z_max, n_1sd, n_2sd}.

    Reference pool INCLUDES `did_not_return_flag = True` bouts (tail_length =
    180) as-is per §3.2.2 rationale (excluding them would deflate median and
    inflate derivative flag rate). Candidate-day exclusion is enforced by
    the window edge (`[d-90, d-30]` doesn't contain `d`) per §3.2.2.

    Returns per_day_ref_stats: `{date_iso -> {5 columns}}`. Days in
    `valid_dates` but with reference-window shortfall (< 30 pool) get NaN
    (None) on all 5 columns.

    NaN semantics on the per-day aggregation columns:
      - `subject_lagged_median_day` / `subject_lagged_mad_day` / `bout_return_time_z_max_day`:
        None on reference-window-invalid days OR days with no bouts on day.
      - `bout_n_did_not_return_1sd_day` / `bout_n_did_not_return_2sd_day`:
        0 on valid-reference days with no flagged bouts; None on
        reference-window-invalid days.
    """
    # Index bouts by their attributed date.
    bouts_by_date: dict[date, list[dict]] = collections.defaultdict(list)
    for b in all_bouts:
        try:
            d = date.fromisoformat(b["date"])
        except (ValueError, TypeError):
            continue
        bouts_by_date[d].append(b)

    per_day_ref_stats: dict[str, dict] = {}

    for d in sorted(valid_dates):
        # Build reference pool from bouts on days in [d-90, d-30] that pass
        # the §3.4 day-validity gate (valid_dates already enforces LC era +
        # April 2024 cluster + device-baseline-lag exclusions).
        ref_tail_lengths: list[float] = []
        for offset in range(LAGGED_WINDOW_LOOKBACK_END, LAGGED_WINDOW_LOOKBACK_START + 1):
            ref_d = d - timedelta(days=offset)
            if ref_d not in valid_dates:
                continue
            for b in bouts_by_date.get(ref_d, []):
                tl = b.get("tail_length")
                if tl is not None:
                    ref_tail_lengths.append(float(tl))

        # Reference-window validity check per §3.2.2 (>= 30 bouts).
        if len(ref_tail_lengths) < MIN_REFERENCE_POOL_SIZE:
            per_day_ref_stats[d.isoformat()] = {
                "subject_lagged_median_day": None,
                "subject_lagged_mad_day": None,
                "bout_return_time_z_max_day": None,
                "bout_n_did_not_return_1sd_day": None,
                "bout_n_did_not_return_2sd_day": None,
            }
            for b in bouts_by_date.get(d, []):
                b["bout_return_time_z"] = None
                b["did_not_return_1sd_flag"] = None
                b["did_not_return_2sd_flag"] = None
            continue

        # Compute robust median + MAD per §3.2.2.
        median_tl = statistics.median(ref_tail_lengths)
        abs_devs = [abs(tl - median_tl) for tl in ref_tail_lengths]
        mad_raw = statistics.median(abs_devs)
        mad_tl = MAD_SCALE_TO_SD * mad_raw

        # Degenerate case: all reference bouts have identical tail_length
        # (MAD = 0). Cannot compute z-scores. Route to NaN semantics.
        if mad_tl == 0:
            per_day_ref_stats[d.isoformat()] = {
                "subject_lagged_median_day": round(median_tl, 4),
                "subject_lagged_mad_day": 0.0,
                "bout_return_time_z_max_day": None,
                "bout_n_did_not_return_1sd_day": None,
                "bout_n_did_not_return_2sd_day": None,
            }
            for b in bouts_by_date.get(d, []):
                b["bout_return_time_z"] = None
                b["did_not_return_1sd_flag"] = None
                b["did_not_return_2sd_flag"] = None
            continue

        threshold_1sd = median_tl + 1 * mad_tl
        threshold_2sd = median_tl + 2 * mad_tl

        # Per-bout derivative features on day d.
        day_bouts = bouts_by_date.get(d, [])
        z_scores: list[float] = []
        n_1sd = 0
        n_2sd = 0
        for b in day_bouts:
            tl = b.get("tail_length")
            if tl is None:
                b["bout_return_time_z"] = None
                b["did_not_return_1sd_flag"] = None
                b["did_not_return_2sd_flag"] = None
                continue
            z = (float(tl) - median_tl) / mad_tl
            b["bout_return_time_z"] = round(z, 4)
            f1 = tl > threshold_1sd
            f2 = tl > threshold_2sd
            b["did_not_return_1sd_flag"] = f1
            b["did_not_return_2sd_flag"] = f2
            z_scores.append(z)
            if f1:
                n_1sd += 1
            if f2:
                n_2sd += 1

        per_day_ref_stats[d.isoformat()] = {
            "subject_lagged_median_day": round(median_tl, 4),
            "subject_lagged_mad_day": round(mad_tl, 4),
            "bout_return_time_z_max_day": round(max(z_scores), 4) if z_scores else None,
            "bout_n_did_not_return_1sd_day": n_1sd,
            "bout_n_did_not_return_2sd_day": n_2sd,
        }

    return per_day_ref_stats


# === FIT-parsing main loop (mirrors stress_low_motion_extract.py) ===

def parse_monitoring_files() -> tuple[
    dict[date, dict[datetime, int]],
    dict[date, dict[datetime, int | None]],
    dict[date, int],
]:
    """Parse all monitoring_b FIT files; emit per-day per-minute stress dict
    + per-day per-minute intensity dict + per-day sample_count (raw stress
    sample count, used for the day-validity gate).

    Per-minute stress: only valid in-range samples ([1, 100]); minute-key is
    UTC datetime with second=0, microsecond=0. Multiple samples in the same
    minute keep the latest.

    Per-minute intensity: only minutes with a monitoring-frame intensity
    record; minute-key is UTC datetime. Last-record-in-minute wins. Minutes
    WITHOUT an intensity record are absent from the dict (consumer must
    treat absent as None / no-record per §3.4).
    """
    if not CLASSIFIED_CSV.exists():
        raise SystemExit(f"ERROR: {CLASSIFIED_CSV} not found")
    with CLASSIFIED_CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    mfiles = [r for r in rows if r["type"] == "monitoring_b"]
    print(f"monitoring_b files to parse: {len(mfiles)}", file=sys.stderr)

    open_zips: dict[str, zipfile.ZipFile] = {}
    for z in {r["zip"] for r in mfiles}:
        open_zips[z] = zipfile.ZipFile(GARMIN_DUMP / z)

    stress_by_date: dict[date, dict[datetime, int]] = collections.defaultdict(dict)
    intensity_by_date: dict[date, dict[datetime, int | None]] = collections.defaultdict(dict)
    sample_count_by_date: dict[date, int] = collections.defaultdict(int)

    for i, r in enumerate(mfiles):
        if i % 500 == 0:
            print(f"  parsed {i}/{len(mfiles)} files", file=sys.stderr)
        try:
            buf = open_zips[r["zip"]].read(r["filename"])
            resolver = Monitoring16Resolver()
            with fitdecode.FitReader(io.BytesIO(buf)) as fit:
                for frame in fit:
                    if not isinstance(frame, fitdecode.FitDataMessage):
                        continue
                    if frame.name == "monitoring_info":
                        for f in frame.fields:
                            if f.name == "timestamp" and isinstance(f.value, datetime):
                                anchor = f.value
                                if anchor.tzinfo is None:
                                    anchor = anchor.replace(tzinfo=timezone.utc)
                                resolver.set_reference(anchor)
                        continue
                    if frame.name == "stress_level":
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
                        v_raw = val_field.value
                        if ts is None or v_raw is None or not isinstance(ts, datetime):
                            continue
                        try:
                            v = int(v_raw)
                        except (TypeError, ValueError):
                            continue
                        if not (STRESS_VALID_MIN <= v <= STRESS_VALID_MAX):
                            continue
                        if ts.tzinfo is None:
                            ts = ts.replace(tzinfo=timezone.utc)
                        tm = ts.replace(second=0, microsecond=0)
                        d_attr = tm.date()
                        # Last-write-wins per minute (mirrors HA11 extractor).
                        stress_by_date[d_attr][tm] = v
                        sample_count_by_date[d_attr] += 1
                        continue
                    if frame.name == "monitoring":
                        ts = resolver.resolve_frame(frame)
                        intensity_field = next(
                            (f for f in frame.fields if f.name == "intensity"),
                            None,
                        )
                        if ts is None or intensity_field is None:
                            continue
                        if intensity_field.value is None:
                            continue
                        try:
                            iv = int(intensity_field.value)
                        except (TypeError, ValueError):
                            continue
                        if ts.tzinfo is None:
                            ts = ts.replace(tzinfo=timezone.utc)
                        tm = ts.replace(second=0, microsecond=0)
                        intensity_by_date[tm.date()][tm] = iv
        except Exception as e:
            print(f"  warn: failed {r['filename']}: {e}", file=sys.stderr)
            continue

    print(
        f"parsed stress samples for {len(stress_by_date)} dates, "
        f"intensity for {len(intensity_by_date)} dates",
        file=sys.stderr,
    )
    return dict(stress_by_date), dict(intensity_by_date), dict(sample_count_by_date)


# === Per-day intensity merge helper (the intensity at a given minute is the
# most-recent intensity record at or before that minute; mirrors
# stress_low_motion_extract.py logic at lines 161-172). ===

def build_intensity_at_minute(
    minute_stress: dict[datetime, int],
    intensity_records: dict[datetime, int],
) -> dict[datetime, int | None]:
    """For each stress-bearing minute, look up the intensity from the
    sparse intensity record. Returns dict mapping the stress-minute key ->
    intensity value, or None if no intensity record covers the minute.

    Per stress_low_motion_extract.py: "the intensity at a given minute is
    the most-recent intensity classification at or before that minute".
    """
    if not minute_stress:
        return {}
    int_times = sorted(intensity_records.keys())
    int_vals = [intensity_records[t] for t in int_times]
    out: dict[datetime, int | None] = {}
    for tm in minute_stress.keys():
        i = bisect.bisect_right(int_times, tm)
        out[tm] = int_vals[i - 1] if i > 0 else None
    return out


# === Smoke tests (per Decision 4 ad-hoc verification) ===

def _make_minute_dict(start: datetime, values: list[int]) -> dict[datetime, int]:
    out: dict[datetime, int] = {}
    for i, v in enumerate(values):
        if v is None:
            continue
        out[start + timedelta(minutes=i)] = v
    return out


def run_smoke_tests() -> None:
    """Inline edge-case smoke tests per user-ratified Decision 4."""
    print("\n=== Smoke tests ===", file=sys.stderr)

    # Test 1: clean canonical bout (peak above 60, clean baseline, returns)
    start = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    # 30 minutes of baseline ~30 (well below 50), then a clean bout: 60, 70,
    # 80, 75, 65, 55, 45, 35, 30 ... lasting ~20 min. Return at minute ~25
    # post-onset (back to <= 35 = 30 + 5 tolerance).
    pre_baseline = [30] * 30
    onset_and_bout = [60, 70, 80, 75, 65, 55, 45, 35, 30, 30, 30, 30, 30, 30,
                      30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
                      30, 30, 30]
    values = pre_baseline + onset_and_bout + [30] * 60
    minute_stress = _make_minute_dict(start, values)
    bouts = detect_bouts_on_day(minute_stress, {}, {}, date(2024, 1, 1))
    assert len(bouts) == 1, f"Test 1 (canonical bout): expected 1 bout, got {len(bouts)}"
    b = bouts[0]
    assert b["peak_height"] == 80, f"Test 1 peak_height: expected 80, got {b['peak_height']}"
    assert b["did_not_return_flag"] is False, "Test 1 did_not_return: expected False"
    assert b["pre_bout_baseline"] is not None
    assert b["baseline_invalid_flag"] is False
    assert b["motion_confound_flag"] is None, (
        "Test 1 motion_confound_flag: expected None (no intensity record), "
        f"got {b['motion_confound_flag']}"
    )
    print("  PASS Test 1: canonical bout detected, peak=80, returns", file=sys.stderr)

    # Test 2: did_not_return — sustained elevation throughout the 180 min cap
    pre_baseline = [30] * 30
    sustained = [60, 70, 80, 75, 75, 75] + [70] * 200
    values = pre_baseline + sustained
    minute_stress = _make_minute_dict(start, values)
    bouts = detect_bouts_on_day(minute_stress, {}, {}, date(2024, 1, 1))
    assert len(bouts) == 1, f"Test 2 (did_not_return): expected 1 bout, got {len(bouts)}"
    b = bouts[0]
    assert b["did_not_return_flag"] is True, "Test 2 did_not_return: expected True"
    assert b["tail_length"] == 180.0, (
        f"Test 2 tail_length: expected 180, got {b['tail_length']}"
    )
    print("  PASS Test 2: did_not_return fires; tail_length capped at 180", file=sys.stderr)

    # Test 3: midnight-spanning bout (start at 23:50, peak at 00:05, attribute
    # to 2024-01-02)
    start = datetime(2024, 1, 1, 23, 30, 0, tzinfo=timezone.utc)
    pre = [30] * 20  # 23:30 - 23:49
    bout = [60, 70, 80, 70, 60, 50, 40, 30] + [30] * 60
    values = pre + bout
    minute_stress = _make_minute_dict(start, values)
    bouts = detect_bouts_on_day(minute_stress, {}, {}, date(2024, 1, 1))
    assert len(bouts) == 1, f"Test 3 (midnight): expected 1 bout, got {len(bouts)}"
    b = bouts[0]
    # Onset at 23:50, peak at 23:52 (the 80). t_peak.date() = 2024-01-01
    # (peak at 23:52 not yet midnight). For a peak-crosses-midnight case,
    # let's set up a different scenario.
    print(
        f"  Test 3: peak attribute date = {b['date']} (t_onset {b['t_onset']}, "
        f"t_peak {b['t_peak']})",
        file=sys.stderr,
    )
    # The interesting midnight case: onset at 23:55, peak at 00:05.
    start2 = datetime(2024, 1, 1, 23, 30, 0, tzinfo=timezone.utc)
    pre2 = [30] * 25  # 23:30 - 23:54
    # 23:55 onset -> 60. 23:56 70. 23:57 75. 23:58 80. 23:59 90. 00:00 100.
    # 00:05 max = 100; pick 00:05 to confirm cross-midnight peak.
    bout2 = [60, 70, 75, 80, 90, 100, 95, 90, 85, 80, 70, 50, 40, 35, 30] + [30] * 50
    values2 = pre2 + bout2
    minute_stress2 = _make_minute_dict(start2, values2)
    bouts2 = detect_bouts_on_day(minute_stress2, {}, {}, date(2024, 1, 1))
    assert len(bouts2) == 1, f"Test 3b (midnight peak): expected 1 bout, got {len(bouts2)}"
    b2 = bouts2[0]
    # 23:55 + 5 minutes = 00:00; but max may not yet have been reached. Let
    # the peak be the 100 at 00:00. t_peak.date() = 2024-01-02 (yes, just
    # past midnight). Bout-attribution date should follow t_peak.date().
    assert b2["date"] == "2024-01-02", (
        f"Test 3b: peak crossed midnight; expected date=2024-01-02, got {b2['date']}"
    )
    print(
        f"  PASS Test 3b: cross-midnight peak attributed to {b2['date']} "
        f"(t_peak {b2['t_peak']})",
        file=sys.stderr,
    )

    # Test 4: NaN handling (gaps in per-minute trace)
    # Pre-window has 8 minutes < 50 (rest NaN); fails the 10-of-15
    # hysteresis check; no bout detected.
    start = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    pre = [30, 30, 30, 30, None, None, None, None, None, None, 30, 30, 30, 30, 30] * 1
    bout = [60, 70, 80, 70, 60, 50, 40, 30]
    minute_stress: dict[datetime, int] = {}
    for i, v in enumerate(pre + bout):
        if v is not None:
            minute_stress[start + timedelta(minutes=i)] = v
    # Need previous minute < 60 for onset; minute 15 (where 60 lives) needs
    # minute 14 present and < 60 (it's 30). Hysteresis window for onset at
    # minute 15: [t-20, t-5] = minutes -5 to 10 (relative). Spans minutes
    # 0..10 of our actual trace; values: 30,30,30,30,NaN,NaN,NaN,NaN,NaN,NaN,30
    # 5 of 11 valid below 50 < 10 needed -> hyst fails. Confirm no bout.
    bouts = detect_bouts_on_day(minute_stress, {}, {}, date(2024, 1, 1))
    assert len(bouts) == 0, (
        f"Test 4 (NaN-driven hyst fail): expected 0 bouts, got {len(bouts)}"
    )
    print("  PASS Test 4: NaN gaps in pre-window correctly fail hysteresis", file=sys.stderr)

    # Test 5: transient (peak immediately at onset, t_peak - t_onset < 5)
    start = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    pre = [30] * 30
    bout = [80, 70, 60, 50, 40, 35, 30] + [30] * 50  # peak at minute 0 -> transient
    values = pre + bout
    minute_stress = _make_minute_dict(start, values)
    bouts = detect_bouts_on_day(minute_stress, {}, {}, date(2024, 1, 1))
    assert len(bouts) == 1
    b = bouts[0]
    assert b["transient_flag"] is True, (
        f"Test 5 (transient): expected True, got {b['transient_flag']}"
    )
    print("  PASS Test 5: transient bout (peak at onset) flagged", file=sys.stderr)

    # Test 6: motion_confound_flag honest tri-state
    # Case 6a: intensity record exists with all 0 -> False
    start = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    values = [30] * 30 + [60, 70, 80, 70, 60, 50, 40, 30] + [30] * 50
    minute_stress = _make_minute_dict(start, values)
    minute_intensity = {start + timedelta(minutes=i): 0 for i in range(len(values))}
    bouts = detect_bouts_on_day(minute_stress, minute_intensity, {}, date(2024, 1, 1))
    assert len(bouts) == 1 and bouts[0]["motion_confound_flag"] is False, (
        f"Test 6a: expected motion_confound=False, got {bouts[0]['motion_confound_flag']}"
    )
    print("  PASS Test 6a: motion_confound=False with intensity-0 records", file=sys.stderr)
    # Case 6b: intensity record exists with >= 2 -> True
    minute_intensity = {start + timedelta(minutes=i): 2 for i in range(len(values))}
    bouts = detect_bouts_on_day(minute_stress, minute_intensity, {}, date(2024, 1, 1))
    assert len(bouts) == 1 and bouts[0]["motion_confound_flag"] is True, (
        f"Test 6b: expected motion_confound=True, got {bouts[0]['motion_confound_flag']}"
    )
    print("  PASS Test 6b: motion_confound=True with intensity-2 records", file=sys.stderr)
    # Case 6c: no intensity records -> None (NaN per r2 absorb #4)
    bouts = detect_bouts_on_day(minute_stress, {}, {}, date(2024, 1, 1))
    assert len(bouts) == 1 and bouts[0]["motion_confound_flag"] is None, (
        f"Test 6c: expected motion_confound=None, got {bouts[0]['motion_confound_flag']}"
    )
    print("  PASS Test 6c: motion_confound=None with absent intensity record", file=sys.stderr)

    print("All smoke tests passed.", file=sys.stderr)


# === Main pipeline ===

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--smoke-tests",
        action="store_true",
        help="Run inline edge-case smoke tests and exit.",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Print 5 random per-bout spot-checks at end of run.",
    )
    args = parser.parse_args(argv)

    if args.smoke_tests:
        run_smoke_tests()
        return 0

    print("Loading sleep windows from sleepData.json...", file=sys.stderr)
    sleep_windows = load_sleep_windows()
    print(f"  {len(sleep_windows)} dates with sleep windows", file=sys.stderr)

    print("Loading has_garmin_uds dates from daily_uds.csv...", file=sys.stderr)
    uds_dates = load_uds_dates()
    print(f"  {len(uds_dates)} dates with UDS coverage", file=sys.stderr)
    if uds_dates:
        first_uds = min(uds_dates)
        print(
            f"  device-baseline-lag window: {first_uds} -> "
            f"{first_uds + timedelta(days=DEVICE_LAG_DAYS - 1)} excluded",
            file=sys.stderr,
        )

    print("Parsing monitoring_b FIT files...", file=sys.stderr)
    stress_by_date, intensity_by_date, sample_count_by_date = parse_monitoring_files()

    # Determine valid days per §3.4 gate
    valid_dates: set[date] = set()
    for d, sc in sample_count_by_date.items():
        if day_valid(d, sc, uds_dates):
            valid_dates.add(d)
    print(f"\nValid days (per §3.4 gate): {len(valid_dates)}", file=sys.stderr)

    # Detect bouts per valid day. Per §3.2, bouts that cross midnight are
    # attributed to t_peak's date. Implementation: scan per-day-of-onset
    # and let detect_bouts_on_day stamp the bout with t_peak.date(). For
    # bouts whose onset is late on day D and peak crosses to D+1, the
    # detector sees the trace on day D (since the per-minute-stress dict
    # is keyed by stress-sample's timestamp date). We merge minute_stress
    # of day D with the first 2 hours of day D+1 so the peak/end search
    # window can extend across midnight.
    all_bouts: list[dict] = []
    sorted_dates = sorted(set(stress_by_date.keys()) | set(intensity_by_date.keys()))
    print(f"Running bout detection on {len(sorted_dates)} days...", file=sys.stderr)
    for i, d in enumerate(sorted_dates):
        if i % 500 == 0 and i > 0:
            print(f"  processed {i}/{len(sorted_dates)} days; bouts so far: {len(all_bouts)}", file=sys.stderr)
        if d not in valid_dates:
            continue
        # Combine same-day + first 4h of next-day stress samples so cross-
        # midnight bouts can complete. Next-day intensity records too.
        minute_stress = dict(stress_by_date.get(d, {}))
        minute_intensity_raw = dict(intensity_by_date.get(d, {}))
        next_d = d + timedelta(days=1)
        next_stress = stress_by_date.get(next_d, {})
        next_intensity = intensity_by_date.get(next_d, {})
        spillover_cutoff = datetime.combine(next_d, time(4, 0), tzinfo=timezone.utc)
        for tm, v in next_stress.items():
            if tm < spillover_cutoff:
                minute_stress[tm] = v
        for tm, v in next_intensity.items():
            if tm < spillover_cutoff:
                minute_intensity_raw[tm] = v
        # Also pull yesterday's late samples (after 20:00) for hysteresis
        # window of an early-morning bout.
        prev_d = d - timedelta(days=1)
        prev_cutoff = datetime.combine(prev_d, time(20, 0), tzinfo=timezone.utc)
        for tm, v in stress_by_date.get(prev_d, {}).items():
            if tm >= prev_cutoff:
                minute_stress[tm] = v
        for tm, v in intensity_by_date.get(prev_d, {}).items():
            if tm >= prev_cutoff:
                minute_intensity_raw[tm] = v
        # Build the per-minute intensity dict (sparse intensity records ->
        # per-minute "last record at-or-before" mapping).
        minute_intensity = build_intensity_at_minute(minute_stress, minute_intensity_raw)
        bouts = detect_bouts_on_day(minute_stress, minute_intensity, sleep_windows, d)
        # Filter: keep only bouts whose t_peak.date() equals d. This
        # prevents double-counting at day boundaries (a bout whose peak is
        # at d+1 will be detected again when scanning day d+1; we keep the
        # d+1 detection since that's where the per-bout dict's spillover
        # logic naturally surfaces it).
        for b in bouts:
            if b["date"] == d.isoformat():
                # Join citalopram covariates.
                b_date = d
                b["dose_plasma_mg"] = dose_plasma_mg(b_date)
                b["citalopram_phase"] = citalopram_phase(b_date)
                b["is_unmedicated"] = b["citalopram_phase"] == "unmedicated"
                all_bouts.append(b)

    print(f"\nTotal bouts detected: {len(all_bouts)}", file=sys.stderr)

    # Personal-baseline SD-anchored derivative operand family (per MD §3.2.2
    # LOCKED r3). Mutates all_bouts to add 3 per-bout columns; returns per-day
    # {median, mad, z_max, n_1sd, n_2sd} for the aggregation merge below.
    print("Computing SD-anchored derivative operand family (MD §3.2.2)...", file=sys.stderr)
    sd_anchored_per_day = compute_sd_anchored_features(all_bouts, valid_dates)
    ref_valid_days = sum(
        1 for stats in sd_anchored_per_day.values()
        if stats["subject_lagged_median_day"] is not None
    )
    ref_invalid_days = len(sd_anchored_per_day) - ref_valid_days
    print(
        f"  reference-window valid days: {ref_valid_days}"
        f"; reference-window invalid days: {ref_invalid_days}"
        f" (< {MIN_REFERENCE_POOL_SIZE} bouts in [d-90, d-30])",
        file=sys.stderr,
    )

    # Per-day aggregations
    print("Computing per-day aggregations...", file=sys.stderr)
    per_day_aggs = aggregate_per_day(all_bouts, valid_dates, sd_anchored_per_day)
    print(f"  per-day rows: {len(per_day_aggs)}", file=sys.stderr)

    # Write per-bout CSV + parquet
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_BOUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=PER_BOUT_FIELDS)
        w.writeheader()
        for b in all_bouts:
            row = {k: b.get(k, "") for k in PER_BOUT_FIELDS}
            # Normalise bool / None for CSV.
            for k, v in row.items():
                if v is None:
                    row[k] = ""
                elif isinstance(v, bool):
                    row[k] = "True" if v else "False"
            w.writerow(row)
    print(f"Wrote {OUT_BOUT_CSV} ({len(all_bouts)} rows)", file=sys.stderr)

    # Parquet sidecar via pandas.
    try:
        import pandas as pd
        df = pd.DataFrame(all_bouts, columns=PER_BOUT_FIELDS)
        df.to_parquet(OUT_BOUT_PARQUET, index=False)
        print(f"Wrote {OUT_BOUT_PARQUET}", file=sys.stderr)
    except Exception as e:
        print(f"  warn: parquet write failed: {e}", file=sys.stderr)

    # Per-day aggregations CSV
    with OUT_AGG_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=PER_DAY_AGG_FIELDS)
        w.writeheader()
        for r in per_day_aggs:
            w.writerow(r)
    print(f"Wrote {OUT_AGG_CSV} ({len(per_day_aggs)} rows)", file=sys.stderr)

    # === Stats summary ===
    print("\n=== Stats ===", file=sys.stderr)
    if all_bouts:
        years = collections.Counter(b["date"][:4] for b in all_bouts)
        print("  bouts per year:", file=sys.stderr)
        for yr in sorted(years):
            print(f"    {yr}: {years[yr]}", file=sys.stderr)
        days_with_bouts = len(set(b["date"] for b in all_bouts))
        days_without_bouts = len(valid_dates) - days_with_bouts
        print(f"  valid days with >=1 bout: {days_with_bouts}", file=sys.stderr)
        print(f"  valid days with 0 bouts: {days_without_bouts}", file=sys.stderr)
        did_not_return = sum(1 for b in all_bouts if b["did_not_return_flag"])
        print(
            f"  bouts with did_not_return_flag=True: {did_not_return} "
            f"({100 * did_not_return / len(all_bouts):.1f}%)",
            file=sys.stderr,
        )
        transients = sum(1 for b in all_bouts if b["transient_flag"])
        print(
            f"  bouts with transient_flag=True: {transients} "
            f"({100 * transients / len(all_bouts):.1f}%)",
            file=sys.stderr,
        )

    # === Spot-check verification (per Decision 4) ===
    if args.verify and all_bouts:
        import random
        random.seed(42)
        n_pick = min(5, len(all_bouts))
        picks = random.sample(all_bouts, n_pick)
        print("\n=== 5-bout spot-check ===", file=sys.stderr)
        for b in picks:
            print(f"\n  bout_id={b['bout_id']}", file=sys.stderr)
            for k in PER_BOUT_FIELDS:
                print(f"    {k}: {b.get(k)}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
