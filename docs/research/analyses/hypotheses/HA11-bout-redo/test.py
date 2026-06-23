"""HA11-bout-redo - framework-validity reproduction of HA11 v1 on bout-level operand.

Implements the LOCKED r2 pre-registration (hypothesis.md LOCKED 2026-06-23 r2
commit 5c71aa0 + footer fix b5bf0f8) per its detection-script architecture
section 10.

What this test does (per pre-reg sections 1, 4, 5, 10):
  - Loads bout_n_fast_recovery_day from per_day_master.csv (joined from
    per_bout_aggregations_daily.csv per pipeline commit d5b394c).
  - Replays HA11 v1's build_null_sample with seed 20260605 to regenerate the
    200 reference dates (the calm-day pool); restricts to unmedicated x
    train era subset.
  - For each reference date r: computes per-day z-score of
    bout_n_fast_recovery_day against the participant's lagged personal
    baseline (60-day window [d-90, d-30], >= 40/60 valid prior days,
    sigma > 0.5 floor per HA11 v1 section 4.5); aggregates to per-window
    max-signed-z over [r-3, r-2, r-1, r] (4-day primary window) per HA11 v1
    section 4.7.
  - Identifies crash-episode 4d lead-up windows in the unmedicated x train
    era; same per-window aggregation.
  - Computes trigger frequencies on both pools (max signed z >= 1.5,
    one-sided elevated per HA11 v1 section 4.8 primary tier).
  - Discrimination (pp) = frac_crash - frac_calm. Block-permutation p-value
    at E[L]=7 with seed 20260622 per pre-reg section 4.8.
  - Cliff's delta on per-window max-signed-z distributions (descriptive
    companion).
  - Three framework-validity comparability bars per parent MD section 6.2
    (pre-reg section 5):
      Bar 1: directional sign positive
      Bar 2: discrimination >= +12.8 pp (HA11 v1 +22.8 pp minus 10 pp band)
      Bar 3: p-value < 0.05 under block-permutation null
    Verdict: PASSED iff all 3 bars; PARTIAL iff exactly 2; FAILED iff <= 1;
    INCONCLUSIVE iff walk-forward gate fails (n_calm < 30 OR n_crash < 10).
  - Sensitivity arms per section 4.10: motion-clean-only, transient-excluded,
    baseline-invalid-excluded, crash-drop. Re-aggregates the per-day
    bout_n_fast_recovery_day count from per_bout_master.csv with the
    appropriate per-bout flag-filtered subset; otherwise byte-identical
    pipeline. Each reports a descriptive variant; cannot promote to PASSED.
  - Crash-drop sensitivity per CONVENTIONS section 3.4 + pre-reg section 4.10:
    re-run with is_crash == True dropped from both pools; flag if
    |Delta pp| > 5.

Modes:
  python test.py --dry-run      run section 7.5 sanity gates only (n_calm
                                vs section 4.9 walk-forward gate; sigma vs
                                section 4.6 floor; operand-presence). HALT
                                on any gate FAIL per pre-reg section 10.4 +
                                hypothesis_lock_process.md section 3.9.
  python test.py                dry-run first; if all 3 sanity gates PASS,
                                run the full evaluation + emit
                                result-data.json.

ASCII-only stdout per project convention (no em-dash, no emojis); markdown
output may use unicode for readability.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np


# === Path setup so we can import the shared _utils.inference helper. ===

HERE = Path(__file__).resolve().parent
UTILS_DIR = HERE.parent.parent / "_utils"
if str(UTILS_DIR) not in sys.path:
    sys.path.insert(0, str(UTILS_DIR))

from inference import compute_data_driven_block_length  # noqa: E402


# === Constants per LOCKED r2 hypothesis.md ==============================

# Eras and phase per HA11 v1 + pre-reg section 4.2 + 4.3 + 4.4
ANALYSIS_START = date(2022, 9, 3)      # HA11 v1 train start
TRAIN_END = date(2023, 12, 31)         # HA11 v1 train end
VALIDATE_END = date(2026, 6, 5)        # HA11 v1 build_null_sample upper bound
UNMED_START = date(2022, 4, 4)         # citalopram_phase_stratification section 3
UNMED_END = date(2024, 4, 8)           # citalopram start = 2024-04-09
APRIL_2024_CLUSTER_START = date(2024, 4, 9)
APRIL_2024_CLUSTER_END = date(2024, 4, 16)
DEVICE_BASELINE_LAG_DAYS = 21          # parent MD section 3.4

# Lagged baseline (HA11 v1 section 4.5; inherited verbatim per pre-reg section 4.6)
LAGGED_WINDOW_START_DAYS = 30
LAGGED_WINDOW_END_DAYS = 90
MIN_LAGGED_DAYS = 40
TRIMMED_PCT = 0.10
MIN_BASELINE_STD = 0.5                 # HA11 v1 section 4.5 low-variability floor

# Lead-up window (HA11 v1 section 4.7; inherited verbatim per pre-reg section 4.7)
LEADUP_PRIMARY = 4
MIN_LEADUP_VALID_PRIMARY = 3

# Z-score threshold (HA11 v1 section 4.8 primary tier; inherited per pre-reg section 4.7)
N_STD_PRIMARY = 1.5

# HA11 v1 null sample (pre-reg section 4.5)
NULL_SAMPLE_SIZE = 200
HA11_V1_SEED = 20260605                # HA11 v1 reference-date seed

# Block-permutation null (pre-reg section 4.8)
RANDOM_SEED = 20260622                 # HA11-bout-redo seed (distinct from HA11 v1)
BOOTSTRAP_E_L = 7                      # E[L]=7 per permutation_null_block_length.md
B_HEADLINE = 10_000                    # B draws per pre-reg section 4.8 step 2

# Framework-validity comparability bars (pre-reg section 5; parent MD section 6.2 verbatim)
BAR_2_DISC_PP = 12.8                   # HA11 v1 +22.8 pp - 10 pp band
BAR_3_P_VALUE = 0.05

# HA11 v1 train discrimination (reference frame anchor per pre-reg section 1)
HA11_V1_TRAIN_DISC_PP = 22.8

# Walk-forward gate (pre-reg section 4.9)
WF_GATE_N_CALM = 30
WF_GATE_N_CRASH = 10

# Crash-drop sensitivity flag (pre-reg section 4.10 + CONVENTIONS section 3.4)
CRASH_DROP_FLAG_PP = 5.0

# Bout-fast-recovery operand thresholds (parent MD section 6.1; inherited per pre-reg section 4.1)
RECOVERY_HALF_LIFE_MAX = 15.0          # minutes
TAIL_LENGTH_MAX = 45.0                 # minutes

# Pre-reg pinned counts (r2 absorb per pre-reg section 4.5 + 4.6)
PINNED_N_EFFECTIVE = 70                # post all restrictions per section 4.5 + 4.7
PINNED_SIGMA_MEDIAN = 0.739            # bout_n_fast_recovery_day across 413 analysis days
PIPELINE_COMMIT = "d5b394c"
PRE_REG_LOCK_COMMIT = "5c71aa0"
PRE_REG_FOOTER_FIX = "b5bf0f8"


# Paths
DATA_ROOT = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH",
    r"C:\Users\Gebruiker\Documents\gevoelscore-data"))
PER_DAY_CSV = DATA_ROOT / "unified" / "per_day_master.csv"
PER_BOUT_CSV = DATA_ROOT / "unified" / "per_bout_master.csv"
UDIP_CSV = DATA_ROOT / "analyses" / "hypotheses" / "HA11-stress-udip" / "udip_counts.csv"
LABELS_CSV = DATA_ROOT / "processed" / "crash_labels" / "labels_crash_v2.csv"

OUT_RESULT_JSON = HERE / "result-data.json"


# === Loaders ============================================================

def load_per_day_master() -> tuple[dict[date, float | None], dict[date, bool], dict[date, bool]]:
    """Return (bout_n_fast_recovery_day per date, has_garmin_uds per date, is_crash per date).

    Per pre-reg section 3 + section 4.4 data source. is_crash drives the
    crash-drop sensitivity arm per pre-reg section 4.10.
    """
    bouts: dict[date, float | None] = {}
    has_uds: dict[date, bool] = {}
    is_crash: dict[date, bool] = {}
    with PER_DAY_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            raw = r["bout_n_fast_recovery_day"]
            bouts[d] = float(raw) if raw not in ("", None) else None
            has_uds[d] = r["has_garmin_uds"].strip().lower() == "true"
            is_crash[d] = r.get("is_crash", "").strip().lower() == "true"
    return bouts, has_uds, is_crash


def load_per_bout_master() -> list[dict]:
    """Return per-bout records with the per-bout flags + features needed for
    pre-reg section 4.10 sensitivity arms.

    Each record: {date, recovery_half_life, tail_length, motion_confound_flag,
    transient_flag, baseline_invalid_flag, did_not_return_flag, ...}.
    """
    out: list[dict] = []
    with PER_BOUT_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                d = date.fromisoformat(r["date"])
            except (KeyError, ValueError):
                continue
            try:
                rhl = float(r["recovery_half_life"])
                tl = float(r["tail_length"])
            except (ValueError, KeyError):
                continue
            out.append({
                "date": d,
                "recovery_half_life": rhl,
                "tail_length": tl,
                "motion_confound_flag": _parse_bool(r.get("motion_confound_flag", "")),
                "transient_flag": _parse_bool(r.get("transient_flag", "")),
                "baseline_invalid_flag": _parse_bool(r.get("baseline_invalid_flag", "")),
                "did_not_return_flag": _parse_bool(r.get("did_not_return_flag", "")),
            })
    return out


def _parse_bool(s: str) -> bool:
    return s.strip().lower() == "true"


def load_udip_counts() -> tuple[dict[date, int], dict[date, bool]]:
    """HA11 v1 udip_counts.csv -> per-date u_dip_count + valid flag.

    Used to regenerate HA11 v1's null-pool reference dates with seed 20260605
    per pre-reg section 4.5.
    """
    counts: dict[date, int] = {}
    valid: dict[date, bool] = {}
    with UDIP_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            counts[d] = int(r["u_dip_count"])
            valid[d] = r["valid"] == "1"
    return counts, valid


def load_crashes() -> list[date]:
    """Crash episode start dates per HA11 v1 load_crashes pattern."""
    crashes_by_id: dict[str, list[date]] = {}
    with LABELS_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["label"] != "crash":
                continue
            d = date.fromisoformat(r["date"])
            crashes_by_id.setdefault(r["episode_id"], []).append(d)
    return sorted(min(ds) for ds in crashes_by_id.values())


# === HA11 v1 null-pool reference-date replay (pre-reg section 4.5) ======

def build_null_sample_replay(
    counts_v1: dict[date, int],
    valid_v1: dict[date, bool],
    crash_starts: list[date],
) -> list[date]:
    """Replay HA11 v1's build_null_sample with seed 20260605.

    Matches HA11 v1 test.py lines 190-219 verbatim (the script that produced
    the LOCKED reference dates). Returns the 200 reference dates pre any
    HA11-bout-redo restriction. Subsequent restrictions per section 4.2 + 4.3
    + 4.4 + 4.5 + 4.7 are applied downstream.
    """
    rng = random.Random(HA11_V1_SEED)
    occupied: set[date] = set()
    for ref in crash_starts:
        for i in range(1, LEADUP_PRIMARY + 1):
            occupied.add(ref - timedelta(days=i))
    all_dates = sorted(
        d for d in counts_v1
        if valid_v1.get(d, False)
        and ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END
    )
    out: list[date] = []
    attempts = 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 10000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_PRIMARY + 1)}
        if leadup & occupied:
            continue
        # HA11 v1 also required >= 3 of 4 valid in the leadup for the episode
        # profile; replay must mirror.
        n_valid = sum(
            1 for d in leadup if d in counts_v1 and valid_v1.get(d, False)
        )
        if n_valid < MIN_LEADUP_VALID_PRIMARY:
            continue
        out.append(ref)
    return out


# === Day-validity gate (pre-reg section 4.4) ============================

def device_baseline_lag_set(has_uds: dict[date, bool]) -> set[date]:
    uds_dates = sorted(d for d, v in has_uds.items() if v)
    return set(uds_dates[:DEVICE_BASELINE_LAG_DAYS])


def day_is_valid_for_bout_redo(
    d: date,
    bouts: dict[date, float | None],
    baseline_lag_set: set[date],
) -> bool:
    """Pre-reg section 4.4: era + bout-non-NaN + not in device-baseline lag
    + not in April 2024 cluster.
    """
    if not (ANALYSIS_START <= d <= TRAIN_END):
        return False
    if bouts.get(d) is None:
        return False
    if d in baseline_lag_set:
        return False
    if APRIL_2024_CLUSTER_START <= d <= APRIL_2024_CLUSTER_END:
        return False
    return True


# === Lagged personal baseline + z-score (pre-reg section 4.6) ===========

def trimmed_list(values: list[float], trim_pct: float) -> list[float]:
    if not values:
        return []
    vs = sorted(values)
    n = len(vs)
    trim = int(n * trim_pct)
    if n - 2 * trim < 1:
        return vs
    return vs[trim: n - trim]


def compute_baseline_mu_sigma(
    d: date,
    series: dict[date, float | None],
    is_day_valid: dict[date, bool],
) -> tuple[float | None, float | None]:
    """Trimmed mean + stdev of `series` over [d-90, d-30] for prior days
    that are themselves valid AND have non-None series value. Returns
    (mu, sigma) or (None, None) if < MIN_LAGGED_DAYS valid prior days or
    sigma <= MIN_BASELINE_STD.
    """
    prior_vals: list[float] = []
    for i in range(LAGGED_WINDOW_START_DAYS + 1, LAGGED_WINDOW_END_DAYS + 1):
        wd = d - timedelta(days=i)
        if (
            wd in series
            and series[wd] is not None
            and is_day_valid.get(wd, False)
        ):
            prior_vals.append(float(series[wd]))
    if len(prior_vals) < MIN_LAGGED_DAYS:
        return None, None
    trimmed = trimmed_list(prior_vals, TRIMMED_PCT)
    if len(trimmed) < 2:
        return None, None
    mu = statistics.mean(trimmed)
    sigma = statistics.stdev(trimmed)
    if sigma <= MIN_BASELINE_STD:
        return None, None
    return mu, sigma


def build_analysis_pool(
    bouts: dict[date, float | None],
    bout_redo_valid: dict[date, bool],
) -> tuple[dict[date, tuple[float, float, float]], int, int]:
    """For each bout-redo-valid day, compute (bout_count, mu, sigma).

    Returns (per_day_inputs, sigma_skips, insufficient_baseline_skips).
    per_day_inputs maps date -> (bout_count, mu, sigma); only days passing
    section 4.6 valid-baseline gate are included.
    """
    per_day_inputs: dict[date, tuple[float, float, float]] = {}
    sigma_skips = 0
    insuf_skips = 0
    for d in sorted(bouts):
        if not bout_redo_valid[d]:
            continue
        mu, sigma = compute_baseline_mu_sigma(d, bouts, bout_redo_valid)
        if mu is None and sigma is None:
            # Distinguish low-variability vs insufficient-prior.
            prior_vals = [
                float(bouts[d - timedelta(days=i)])
                for i in range(LAGGED_WINDOW_START_DAYS + 1, LAGGED_WINDOW_END_DAYS + 1)
                if (d - timedelta(days=i)) in bouts
                and bouts[d - timedelta(days=i)] is not None
                and bout_redo_valid.get(d - timedelta(days=i), False)
            ]
            if len(prior_vals) < MIN_LAGGED_DAYS:
                insuf_skips += 1
            else:
                trimmed = trimmed_list(prior_vals, TRIMMED_PCT)
                if len(trimmed) >= 2 and statistics.stdev(trimmed) <= MIN_BASELINE_STD:
                    sigma_skips += 1
                else:
                    insuf_skips += 1
            continue
        bv = bouts[d]
        assert bv is not None
        per_day_inputs[d] = (float(bv), float(mu), float(sigma))
    return per_day_inputs, sigma_skips, insuf_skips


# === Per-window max-signed-z aggregation (pre-reg section 4.7) ==========

def window_max_signed_z(
    ref: date,
    per_day_inputs: dict[date, tuple[float, float, float]],
) -> float | None:
    """For reference date ref, return max signed z over [ref-3, ref-2, ref-1, ref].

    Requires >= MIN_LEADUP_VALID_PRIMARY of 4 days with a valid (mu, sigma)
    AND a valid bout count, per HA11 v1 section 4.7.
    """
    window = [ref - timedelta(days=i) for i in range(0, LEADUP_PRIMARY)]
    zs: list[float] = []
    for d in window:
        if d in per_day_inputs:
            bv, mu, sigma = per_day_inputs[d]
            zs.append((bv - mu) / sigma)
    if len(zs) < MIN_LEADUP_VALID_PRIMARY:
        return None
    return max(zs)


# === Crash-episode 4d windows in unmedicated x train ====================

def crash_window_refs(
    crashes: list[date],
) -> list[date]:
    """Crash episode start dates whose 4d lead-up window anchor (the day
    immediately before crash start) sits in unmedicated x train era.

    Per HA11 v1 section 4.7: the lead-up window is [C-4, C-3, C-2, C-1].
    For uniformity with the null-pool aggregation (which uses [ref-3, ref-2,
    ref-1, ref] anchored at ref), we set ref = C-1 (the day immediately
    before the crash). The window then aligns to [C-4, C-3, C-2, C-1].
    """
    out: list[date] = []
    for c in crashes:
        ref = c - timedelta(days=1)
        if not (ANALYSIS_START <= ref <= TRAIN_END):
            continue
        if not (UNMED_START <= ref <= UNMED_END):
            continue
        out.append(ref)
    return out


# === Restriction of null-pool reference dates to unmed x train ==========

def restrict_null_refs(null_refs: list[date]) -> list[date]:
    """Pre-reg section 4.2 + 4.3: keep reference dates in unmed x train era."""
    return [
        r for r in null_refs
        if ANALYSIS_START <= r <= TRAIN_END
        and UNMED_START <= r <= UNMED_END
    ]


# === Trigger frequency + discrimination (pre-reg section 4.8) ===========

def evaluate_pool(
    refs: list[date],
    per_day_inputs: dict[date, tuple[float, float, float]],
    N_std: float,
) -> tuple[int, int, list[float]]:
    """Return (n_trigger, n_total, per_window_max_signed_zs).

    Reference dates failing the window-coverage gate are excluded from
    n_total (per HA11 v1 section 4.7 + pre-reg section 4.5).
    """
    zs: list[float] = []
    for r in refs:
        z = window_max_signed_z(r, per_day_inputs)
        if z is None:
            continue
        zs.append(z)
    n_trigger = sum(1 for z in zs if z >= N_std)
    return n_trigger, len(zs), zs


# === Statistics =========================================================

def _rankdata(a: np.ndarray) -> np.ndarray:
    """Rank with mid-rank for ties (vendored to avoid hard scipy dep)."""
    n = len(a)
    order = np.argsort(a, kind="mergesort")
    sorted_a = a[order]
    ranks = np.empty(n, dtype=float)
    i = 0
    while i < n:
        j = i + 1
        while j < n and sorted_a[j] == sorted_a[i]:
            j += 1
        avg_rank = (i + j + 1) / 2.0
        for k in range(i, j):
            ranks[order[k]] = avg_rank
        i = j
    return ranks


def mann_whitney_u_first_arm(
    arm1: np.ndarray, arm2: np.ndarray,
) -> tuple[float, float]:
    """Return (U, p_normal_approx) for arm1 vs arm2.

    U = R_arm1 - n_arm1 * (n_arm1 + 1) / 2. p is a one-sided normal-
    approximation (alternative: arm1 > arm2); reported for descriptive
    triangulation against the block-permutation p only.
    """
    pooled = np.concatenate([arm1, arm2])
    ranks = _rankdata(pooled)
    n1 = len(arm1)
    n2 = len(arm2)
    R1 = float(ranks[:n1].sum())
    U = R1 - n1 * (n1 + 1) / 2.0
    mean_U = n1 * n2 / 2.0
    # Tie-adjusted variance is overkill for the descriptive companion.
    var_U = n1 * n2 * (n1 + n2 + 1) / 12.0
    if var_U <= 0 or n1 < 2 or n2 < 2:
        return U, float("nan")
    z = (U - mean_U) / math.sqrt(var_U)
    # One-sided p for arm1 > arm2 (large U = arm1 ranked higher)
    p = 0.5 * math.erfc(z / math.sqrt(2.0))
    return U, float(p)


def cliffs_delta(arm1: np.ndarray, arm2: np.ndarray) -> float:
    """Cliff's delta = (#{arm1>arm2} - #{arm1<arm2}) / (n1 * n2).

    +1.0 = arm1 strictly dominates; 0 = no ordinal difference; -1.0 = arm2
    dominates. Per pre-reg section 4.8 descriptive companion.
    """
    n1 = len(arm1)
    n2 = len(arm2)
    if n1 == 0 or n2 == 0:
        return float("nan")
    arm2_sorted = np.sort(arm2)
    less = np.searchsorted(arm2_sorted, arm1, side="left")
    greater = n2 - np.searchsorted(arm2_sorted, arm1, side="right")
    return float((less.sum() - greater.sum()) / (n1 * n2))


def cliffs_delta_ci(
    arm1: np.ndarray, arm2: np.ndarray,
    *, n_bootstrap: int = 2000, random_state: int = RANDOM_SEED,
) -> tuple[float, float]:
    """95 percent CI on Cliff's delta via paired-bootstrap of the two arms.

    Per pre-reg section 4.10 + Authorship locked-decisions item 4: project
    default for Cliff's delta CI is the walk-forward bootstrap (resample the
    arms independently).
    """
    rng = np.random.default_rng(random_state)
    n1, n2 = len(arm1), len(arm2)
    if n1 == 0 or n2 == 0:
        return float("nan"), float("nan")
    deltas = np.empty(n_bootstrap)
    for b in range(n_bootstrap):
        s1 = arm1[rng.integers(0, n1, size=n1)]
        s2 = arm2[rng.integers(0, n2, size=n2)]
        deltas[b] = cliffs_delta(s1, s2)
    return float(np.quantile(deltas, 0.025)), float(np.quantile(deltas, 0.975))


def stationary_bootstrap_indices(n: int, p: float, rng: np.random.Generator) -> np.ndarray:
    """Politis-Romano stationary bootstrap indices. Mirrors HA-C4 test.py."""
    indices = np.empty(n, dtype=np.int64)
    i = 0
    while i < n:
        start = int(rng.integers(0, n))
        L = int(rng.geometric(p))
        end = min(i + L, n)
        for j in range(end - i):
            indices[i + j] = (start + j) % n
        i = end
    return indices


def block_permutation_p_value(
    series_dates: list[date],
    crash_label: list[bool],
    null_refs: list[date],
    per_day_inputs: dict[date, tuple[float, float, float]],
    *,
    B: int,
    expected_block_length: int,
    seed: int,
    observed_disc_pp: float,
) -> dict:
    """Block-permutation null on the (date, is_crash_anchor) label sequence.

    Per pre-reg section 4.8 step 2: keep bout_n_fast_recovery_day values
    fixed in place; resample is_crash labels via stationary bootstrap with
    geometric block length E[L]=7; recompute discrimination per draw.

    Implementation: build a label vector L[i] in {True, False} over
    series_dates (True where i is a crash-episode 4d-window-anchor date in
    the unmed x train era). On each draw, stationary-bootstrap-resample the
    indices (length n with geometric block lengths) and read the permuted
    label as `L[idx]`; positions where the permuted label is True are the
    new crash anchors. Compute discrimination on the new anchors vs the
    (un-permuted) HA11 v1 null-pool reference dates.

    The bootstrap preserves day-level autocorrelation in the label series at
    E[L]=7 days but does NOT preserve the exact crash-anchor count
    (n_crash_anchors_null fluctuates run-to-run); this is the spec'd
    procedure per pre-reg section 4.8 step 2 (mirrors HA-C4 test.py +
    inference.py).

    Returns dict with p_value, n_ge, null_disc_distribution summary.
    """
    rng = np.random.default_rng(seed)
    n_obs = len(series_dates)
    p = 1.0 / expected_block_length
    label_arr = np.asarray(crash_label, dtype=bool)
    n_crash_anchors_obs = int(label_arr.sum())
    if n_crash_anchors_obs == 0:
        return {
            "p_value": float("nan"), "n_ge": 0, "B": B,
            "null_disc_median": float("nan"),
            "null_disc_p025": float("nan"),
            "null_disc_p975": float("nan"),
            "n_crash_anchors_null_mean": float("nan"),
            "n_crash_anchors_null_std": float("nan"),
        }

    # Precompute null-pool (calm) trigger fraction once - it does not change
    # under permutation.
    null_trigger_count = 0
    null_total = 0
    for r in null_refs:
        z = window_max_signed_z(r, per_day_inputs)
        if z is None:
            continue
        null_total += 1
        if z >= N_STD_PRIMARY:
            null_trigger_count += 1
    if null_total == 0:
        return {
            "p_value": float("nan"), "n_ge": 0, "B": B,
            "null_disc_median": float("nan"),
            "null_disc_p025": float("nan"),
            "null_disc_p975": float("nan"),
            "n_crash_anchors_null_mean": float("nan"),
            "n_crash_anchors_null_std": float("nan"),
        }
    frac_null = null_trigger_count / null_total

    null_disc = np.empty(B)
    null_n_anchors = np.empty(B, dtype=int)
    for b in range(B):
        idx = stationary_bootstrap_indices(n_obs, p, rng)
        perm_labels = label_arr[idx]
        # Permuted crash-anchor ref dates: the dates at original-series
        # positions where the resampled label is True.
        perm_anchors = [series_dates[i] for i in range(n_obs) if perm_labels[i]]
        null_n_anchors[b] = len(perm_anchors)
        if not perm_anchors:
            null_disc[b] = float("nan")
            continue
        n_t = 0
        n_total = 0
        for r in perm_anchors:
            z = window_max_signed_z(r, per_day_inputs)
            if z is None:
                continue
            n_total += 1
            if z >= N_STD_PRIMARY:
                n_t += 1
        if n_total == 0:
            null_disc[b] = float("nan")
            continue
        frac_crash_perm = n_t / n_total
        null_disc[b] = (frac_crash_perm - frac_null) * 100

    null_disc_clean = null_disc[~np.isnan(null_disc)]
    n_ge = int((null_disc_clean >= observed_disc_pp).sum())
    p_value = (1 + n_ge) / (len(null_disc_clean) + 1)
    return {
        "p_value": float(p_value),
        "n_ge": n_ge,
        "B": int(len(null_disc_clean)),
        "null_disc_median": float(np.median(null_disc_clean)),
        "null_disc_p025": float(np.quantile(null_disc_clean, 0.025)),
        "null_disc_p975": float(np.quantile(null_disc_clean, 0.975)),
        "n_crash_anchors_null_mean": float(null_n_anchors.mean()),
        "n_crash_anchors_null_std": float(null_n_anchors.std()),
    }


# === Sensitivity-arm bout-count re-aggregation (pre-reg section 4.10) ===

def reaggregate_per_day_bouts(
    per_bout: list[dict],
    bouts_primary: dict[date, float | None],
    *,
    arm: str,
) -> dict[date, float | None]:
    """Re-compute per-day bout_n_fast_recovery_day count with the
    sensitivity-arm filter applied.

    arm in:
      'primary'                 - matches the per_day_master.csv column
                                  (includes everything; sanity check).
      'motion_clean'            - exclude motion_confound_flag == True
      'transient_excluded'      - exclude transient_flag == True
      'baseline_invalid_excluded' - exclude baseline_invalid_flag == True

    Returns date -> count. Days that are NaN in the primary (bouts_primary
    is None) remain NaN (the pipeline section 3.4 day-validity gate is
    upstream of the per-bout flag filters).
    """
    counts: dict[date, int] = {}
    for b in per_bout:
        if b["recovery_half_life"] > RECOVERY_HALF_LIFE_MAX:
            continue
        if b["tail_length"] > TAIL_LENGTH_MAX:
            continue
        if arm == "motion_clean" and b["motion_confound_flag"]:
            continue
        if arm == "transient_excluded" and b["transient_flag"]:
            continue
        if arm == "baseline_invalid_excluded" and b["baseline_invalid_flag"]:
            continue
        counts[b["date"]] = counts.get(b["date"], 0) + 1
    out: dict[date, float | None] = {}
    for d, v in bouts_primary.items():
        if v is None:
            out[d] = None  # day was pipeline-invalid; preserve NaN
        else:
            out[d] = float(counts.get(d, 0))
    return out


# === Single-arm evaluation glue =========================================

def evaluate_arm(
    arm_name: str,
    bouts: dict[date, float | None],
    has_uds: dict[date, bool],
    null_refs_all: list[date],
    crashes: list[date],
    *,
    crash_drop: bool = False,
    is_crash: dict[date, bool] | None = None,
    run_permutation: bool = True,
    compute_el_companion: bool = True,
) -> dict:
    """End-to-end evaluation of one arm (primary or sensitivity).

    Returns dict with: n_calm, n_crash, frac_calm, frac_crash, disc_pp,
    cliffs_delta, cliffs_delta_ci95, mannwhitney_u, mannwhitney_p_normal,
    block_perm_p, bar1/2/3 verdicts, aggregate verdict, descriptive arrays.

    If crash_drop=True: drops is_crash==True rows from the analysis-day pool
    (both calm-pool windows whose [r-3,r] window includes a crash-day are
    affected by the day disappearing from per_day_inputs; crash-anchor
    windows whose anchor day is a crash-day are also dropped). The is_crash
    argument MUST be supplied when crash_drop=True.
    """
    baseline_lag = device_baseline_lag_set(has_uds)
    bout_redo_valid = {
        d: day_is_valid_for_bout_redo(d, bouts, baseline_lag) for d in bouts
    }
    if crash_drop:
        assert is_crash is not None, "crash_drop=True requires is_crash"
        for d in list(bout_redo_valid):
            if bout_redo_valid[d] and is_crash.get(d, False):
                bout_redo_valid[d] = False
    per_day_inputs, sigma_skips, insuf_skips = build_analysis_pool(
        bouts, bout_redo_valid
    )
    n_analysis_days = len(per_day_inputs)

    # Restrict null-pool to unmed x train; restrict crash-anchor pool too.
    null_refs_restricted = restrict_null_refs(null_refs_all)
    crash_anchors = crash_window_refs(crashes)
    if crash_drop:
        # Drop crash anchors whose anchor day itself is a crash-day in the
        # original is_crash flag (the anchor day is C-1, not the crash day
        # itself, so this is usually a no-op; but if a crash day immediately
        # follows another crash day, it can fire).
        crash_anchors = [a for a in crash_anchors if not is_crash.get(a, False)]

    n_trig_calm, n_calm, zs_calm = evaluate_pool(
        null_refs_restricted, per_day_inputs, N_STD_PRIMARY
    )
    n_trig_crash, n_crash, zs_crash = evaluate_pool(
        crash_anchors, per_day_inputs, N_STD_PRIMARY
    )

    # Walk-forward gate per pre-reg section 4.9.
    inconclusive = n_calm < WF_GATE_N_CALM or n_crash < WF_GATE_N_CRASH

    frac_calm = n_trig_calm / n_calm if n_calm > 0 else float("nan")
    frac_crash = n_trig_crash / n_crash if n_crash > 0 else float("nan")
    disc_pp = (frac_crash - frac_calm) * 100 if n_calm > 0 and n_crash > 0 else float("nan")

    arr_calm = np.asarray(zs_calm, dtype=float)
    arr_crash = np.asarray(zs_crash, dtype=float)
    if n_calm >= 2 and n_crash >= 2:
        delta = cliffs_delta(arr_crash, arr_calm)
        delta_ci_lo, delta_ci_hi = cliffs_delta_ci(arr_crash, arr_calm)
        U, p_normal = mann_whitney_u_first_arm(arr_crash, arr_calm)
        median_signed_z = float(np.median([z for z in zs_crash if z >= N_STD_PRIMARY])) if n_trig_crash > 0 else float("nan")
    else:
        delta = float("nan")
        delta_ci_lo = float("nan")
        delta_ci_hi = float("nan")
        U = float("nan")
        p_normal = float("nan")
        median_signed_z = float("nan")

    block_perm = {
        "p_value": float("nan"), "n_ge": 0, "B": 0,
        "null_disc_median": float("nan"),
        "null_disc_p025": float("nan"),
        "null_disc_p975": float("nan"),
        "n_crash_anchors_null_mean": float("nan"),
        "n_crash_anchors_null_std": float("nan"),
    }
    if run_permutation and not inconclusive and not math.isnan(disc_pp):
        # Build (date, is_crash_anchor) label sequence over the analysis pool.
        series_dates = sorted(per_day_inputs.keys())
        crash_anchor_set = set(crash_anchors)
        crash_label_seq = [d in crash_anchor_set for d in series_dates]
        block_perm = block_permutation_p_value(
            series_dates, crash_label_seq,
            null_refs_restricted, per_day_inputs,
            B=B_HEADLINE,
            expected_block_length=BOOTSTRAP_E_L,
            seed=RANDOM_SEED,
            observed_disc_pp=disc_pp,
        )

    # E[L]* data-driven companion (pre-reg section 4.8 + parent MD section 5.1)
    el_companion = None
    if compute_el_companion and not inconclusive:
        series_dates = sorted(per_day_inputs.keys())
        series_bouts = np.asarray(
            [per_day_inputs[d][0] for d in series_dates], dtype=float
        )
        el_res = compute_data_driven_block_length(series_bouts)
        el_companion = {
            "optimal_block_length": el_res["optimal_block_length"],
            "flagged_deviation": bool(el_res["flagged_deviation"]),
            "cutoff_lag": el_res["cutoff_lag"],
        }

    # Bar verdicts per pre-reg section 5 / parent MD section 6.2
    bar1 = (disc_pp > 0) if not math.isnan(disc_pp) else None
    bar2 = (disc_pp >= BAR_2_DISC_PP) if not math.isnan(disc_pp) else None
    bar3 = (block_perm["p_value"] < BAR_3_P_VALUE) if not math.isnan(block_perm["p_value"]) else None
    bars = [b for b in (bar1, bar2, bar3) if b is not None]
    bars_met = sum(1 for b in bars if b)

    if inconclusive:
        verdict = "INCONCLUSIVE"
    elif bars_met == 3 and len(bars) == 3:
        verdict = "PASSED"
    elif bars_met == 2 and len(bars) == 3:
        verdict = "PARTIAL"
    elif bars_met <= 1 and len(bars) == 3:
        verdict = "FAILED"
    else:
        verdict = "INCONCLUSIVE"  # one of the bars was uncomputable

    return {
        "arm_name": arm_name,
        "n_analysis_days": n_analysis_days,
        "sigma_skips": sigma_skips,
        "insufficient_baseline_skips": insuf_skips,
        "n_calm": n_calm,
        "n_crash": n_crash,
        "n_trig_calm": n_trig_calm,
        "n_trig_crash": n_trig_crash,
        "frac_calm": frac_calm,
        "frac_crash": frac_crash,
        "discrimination_pp": disc_pp,
        "median_signed_z_triggering_crash": median_signed_z,
        "cliffs_delta": delta,
        "cliffs_delta_ci95_lo": delta_ci_lo,
        "cliffs_delta_ci95_hi": delta_ci_hi,
        "mannwhitney_u": U,
        "mannwhitney_p_normal_one_sided": p_normal,
        "block_perm_p_value": block_perm["p_value"],
        "block_perm_n_ge": block_perm["n_ge"],
        "block_perm_B": block_perm["B"],
        "block_perm_null_disc_median": block_perm["null_disc_median"],
        "block_perm_null_disc_p025": block_perm["null_disc_p025"],
        "block_perm_null_disc_p975": block_perm["null_disc_p975"],
        "block_perm_n_anchors_null_mean": block_perm["n_crash_anchors_null_mean"],
        "block_perm_n_anchors_null_std": block_perm["n_crash_anchors_null_std"],
        "el_companion": el_companion,
        "bar1_directional": bar1,
        "bar2_effect_size_geq_12_8pp": bar2,
        "bar3_p_lt_0_05": bar3,
        "bars_met": bars_met,
        "verdict": verdict,
        "inconclusive": inconclusive,
        "crash_drop": crash_drop,
        "zs_calm": zs_calm,
        "zs_crash": zs_crash,
    }


# === Per-bout-n reporting (pre-reg section 4.11) ========================

def per_bout_n_report(
    per_bout: list[dict],
    crash_anchors: list[date],
    null_refs: list[date],
) -> dict:
    """Per pre-reg section 4.11 + parent MD section 6.3: report per-arm
    n_bouts + per-cell (n_bouts, n_days, n_bouts_per_day).

    Counts bouts that pass the operand definition (recovery_half_life <= 15
    AND tail_length <= 45) on the days covered by either pool's 4-day
    windows.
    """
    def bouts_in_windows(refs: list[date]) -> tuple[int, int]:
        window_days: set[date] = set()
        for r in refs:
            for i in range(LEADUP_PRIMARY):
                window_days.add(r - timedelta(days=i))
        n_b = sum(
            1 for b in per_bout
            if b["date"] in window_days
            and b["recovery_half_life"] <= RECOVERY_HALF_LIFE_MAX
            and b["tail_length"] <= TAIL_LENGTH_MAX
        )
        return n_b, len(window_days)

    crash_b, crash_d = bouts_in_windows(crash_anchors)
    null_b, null_d = bouts_in_windows(null_refs)
    return {
        "crash_n_bouts": crash_b,
        "crash_n_days_in_windows": crash_d,
        "crash_bouts_per_day": (crash_b / crash_d) if crash_d > 0 else float("nan"),
        "null_n_bouts": null_b,
        "null_n_days_in_windows": null_d,
        "null_bouts_per_day": (null_b / null_d) if null_d > 0 else float("nan"),
    }


# === Dry-run sanity gates (pre-reg section 7.5 + section 10.4) ==========

def dry_run_gates(
    bouts: dict[date, float | None],
    has_uds: dict[date, bool],
    null_refs_all: list[date],
    crashes: list[date],
) -> dict:
    """Reproduce the r2-pinned counts INLINE without re-executing the count
    script. Each gate prints PASS/FAIL.
    """
    print("\n=== DRY-RUN SANITY GATES (pre-reg section 7.5 + section 10.4) ===")
    print()

    # Gate 3: operand-presence (run FIRST because it gates the others).
    non_nan = sum(1 for v in bouts.values() if v is not None)
    print(f"GATE 3 - operand presence (bout_n_fast_recovery_day non-NaN count)")
    print(f"  observed: {non_nan} days non-NaN")
    print(f"  threshold: >= 1479 per pipeline README")
    gate3_pass = non_nan >= 1479
    print(f"  result: {'PASS' if gate3_pass else 'FAIL'}")
    print()

    baseline_lag = device_baseline_lag_set(has_uds)
    bout_redo_valid = {
        d: day_is_valid_for_bout_redo(d, bouts, baseline_lag) for d in bouts
    }
    per_day_inputs, sigma_skips, insuf_skips = build_analysis_pool(
        bouts, bout_redo_valid
    )

    # Gate 1: walk-forward n_calm via §4.5 effective-n reproduction.
    null_refs_restricted = restrict_null_refs(null_refs_all)
    analysis_day_set = set(per_day_inputs.keys())
    eligible_refs = []
    for r in null_refs_restricted:
        window = [r - timedelta(days=i) for i in range(0, LEADUP_PRIMARY)]
        n_valid = sum(1 for d in window if d in analysis_day_set)
        if n_valid >= MIN_LEADUP_VALID_PRIMARY:
            eligible_refs.append(r)
    n_eff = len(eligible_refs)
    print(f"GATE 1 - distribution-sanity (effective n_calm reproduction)")
    print(f"  observed: {n_eff} reference dates surviving section 4.4 + 4.5 + 4.7")
    print(f"    (of {len(null_refs_all)} HA11 v1 null refs; "
          f"{len(null_refs_restricted)} in unmed x train pre-window-coverage)")
    print(f"  threshold: >= {WF_GATE_N_CALM} (section 4.9 walk-forward gate)")
    print(f"  r2 pinned: {PINNED_N_EFFECTIVE}")
    gate1_pass = n_eff >= WF_GATE_N_CALM
    print(f"  pinned-match: {'OK' if n_eff == PINNED_N_EFFECTIVE else 'DRIFT (pinned=70, observed=' + str(n_eff) + ')'}")
    print(f"  result: {'PASS' if gate1_pass else 'FAIL'}")
    print()

    # Gate 2: sigma-distribution gate on bout_n_fast_recovery_day.
    sigmas = sorted(s for _, (_, _, s) in per_day_inputs.items())
    if sigmas:
        med_sigma = sigmas[len(sigmas) // 2]
    else:
        med_sigma = float("nan")
    print(f"GATE 2 - sigma-distribution (bout_n_fast_recovery_day median sigma)")
    print(f"  observed: median = {med_sigma:.3f} across {len(sigmas)} analysis days")
    print(f"    range: [{sigmas[0]:.3f}, {sigmas[-1]:.3f}]")
    print(f"  threshold: > {MIN_BASELINE_STD} (section 4.6 low-variability floor)")
    print(f"  r2 pinned: median {PINNED_SIGMA_MEDIAN}")
    gate2_pass = med_sigma > MIN_BASELINE_STD if not math.isnan(med_sigma) else False
    print(f"  result: {'PASS' if gate2_pass else 'FAIL'}")
    print()

    n_crash_anchors_pre = len(crash_window_refs(crashes))
    n_t, n_c, _ = evaluate_pool(crash_window_refs(crashes), per_day_inputs, N_STD_PRIMARY)
    print(f"AUX - crash-anchor pool size (informational; not a separate gate)")
    print(f"  observed: {n_c} crash-anchor 4d windows surviving section 4.7 coverage")
    print(f"    (of {n_crash_anchors_pre} unmed x train crash anchors)")
    print(f"  walk-forward gate floor: >= {WF_GATE_N_CRASH} per section 4.9")
    print()

    overall = gate1_pass and gate2_pass and gate3_pass
    print(f"=== DRY-RUN OVERALL: {'PASS' if overall else 'HALT'} ===")
    if not overall:
        print("Per pre-reg section 10.4 + hypothesis_lock_process.md section 3.9: HALT.")

    return {
        "gate1_pass": gate1_pass,
        "gate2_pass": gate2_pass,
        "gate3_pass": gate3_pass,
        "n_effective_calm": n_eff,
        "median_sigma": med_sigma,
        "non_nan_count": non_nan,
        "n_crash_anchors": n_c,
        "overall_pass": overall,
    }


# === Main ==============================================================

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Run section 7.5 sanity gates only.")
    args = parser.parse_args()

    print(f"DATA_ROOT: {DATA_ROOT}")
    print(f"PER_DAY:   {PER_DAY_CSV}")
    print(f"PER_BOUT:  {PER_BOUT_CSV}")
    print(f"UDIP_V1:   {UDIP_CSV}")
    print(f"CRASHES:   {LABELS_CSV}")
    print()

    print("Loading inputs...")
    bouts, has_uds, is_crash = load_per_day_master()
    counts_v1, valid_v1 = load_udip_counts()
    crashes = load_crashes()
    print(f"  per_day_master rows: {len(bouts)} "
          f"(non-NaN bout: {sum(1 for v in bouts.values() if v is not None)})")
    print(f"  HA11 v1 udip rows: {len(counts_v1)} "
          f"(valid: {sum(1 for v in valid_v1.values() if v)})")
    print(f"  crash episodes: {len(crashes)}")

    print("Replaying HA11 v1 null-pool reference dates (seed 20260605)...")
    null_refs_all = build_null_sample_replay(counts_v1, valid_v1, crashes)
    print(f"  generated: {len(null_refs_all)} reference dates")

    # Dry-run gates (always runs).
    gate_outcomes = dry_run_gates(bouts, has_uds, null_refs_all, crashes)
    if not gate_outcomes["overall_pass"]:
        # HALT.
        return 1

    if args.dry_run:
        print()
        print("Dry-run only mode; not running full evaluation.")
        return 0

    # === Full run ======================================================
    print("\n=== FULL RUN ===")
    print("Loading per_bout_master.csv for sensitivity arms...")
    per_bout = load_per_bout_master()
    print(f"  per-bout records: {len(per_bout)}")

    # Primary arm.
    print("\nEvaluating PRIMARY arm (bout_n_fast_recovery_day, unmed x train, calm-day pool)...")
    primary = evaluate_arm("primary", bouts, has_uds, null_refs_all, crashes)
    _print_arm_summary(primary)

    # Sensitivity arms via per-bout re-aggregation.
    sens_arms: dict[str, dict] = {}
    for arm_name in ("motion_clean", "transient_excluded", "baseline_invalid_excluded"):
        print(f"\nEvaluating SENSITIVITY arm '{arm_name}'...")
        bouts_arm = reaggregate_per_day_bouts(per_bout, bouts, arm=arm_name)
        r = evaluate_arm(arm_name, bouts_arm, has_uds, null_refs_all, crashes,
                         run_permutation=True, compute_el_companion=False)
        sens_arms[arm_name] = r
        _print_arm_summary(r)

    # Crash-drop sensitivity.
    print(f"\nEvaluating CRASH-DROP sensitivity (is_crash dropped from analysis pool)...")
    crash_dropped = evaluate_arm("crash_drop", bouts, has_uds, null_refs_all, crashes,
                                  crash_drop=True, is_crash=is_crash,
                                  run_permutation=True, compute_el_companion=False)
    _print_arm_summary(crash_dropped)
    delta_pp = abs(crash_dropped["discrimination_pp"] - primary["discrimination_pp"]) \
        if not math.isnan(crash_dropped["discrimination_pp"]) and not math.isnan(primary["discrimination_pp"]) else float("nan")
    crash_drop_flag = (delta_pp > CRASH_DROP_FLAG_PP) if not math.isnan(delta_pp) else False
    print(f"  |Delta pp| primary vs crash-dropped: {delta_pp:.2f}")
    print(f"  CONVENTIONS section 3.4 flag (|Delta pp| > {CRASH_DROP_FLAG_PP}): "
          f"{'FIRED (crash-driven signal)' if crash_drop_flag else 'CLEAN'}")

    # Per-bout-n reporting (pre-reg section 4.11).
    print("\nPer-bout-n reporting (pre-reg section 4.11 + parent MD section 6.3)...")
    null_refs_restricted = restrict_null_refs(null_refs_all)
    crash_anchors = crash_window_refs(crashes)
    pb_report = per_bout_n_report(per_bout, crash_anchors, null_refs_restricted)
    print(f"  crash-anchor windows: n_bouts={pb_report['crash_n_bouts']}, "
          f"n_days={pb_report['crash_n_days_in_windows']}, "
          f"bouts/day={pb_report['crash_bouts_per_day']:.3f}")
    print(f"  null-ref windows:     n_bouts={pb_report['null_n_bouts']}, "
          f"n_days={pb_report['null_n_days_in_windows']}, "
          f"bouts/day={pb_report['null_bouts_per_day']:.3f}")

    # Final aggregate verdict.
    print("\n=== AGGREGATE VERDICT ===")
    print(f"  Primary arm verdict: {primary['verdict']}")
    print(f"  Bars met: {primary['bars_met']}/3")
    print(f"    Bar 1 (directional sign positive):    "
          f"{'PASS' if primary['bar1_directional'] else 'FAIL'} "
          f"(disc = {primary['discrimination_pp']:+.2f} pp)")
    print(f"    Bar 2 (disc >= +12.8 pp):             "
          f"{'PASS' if primary['bar2_effect_size_geq_12_8pp'] else 'FAIL'} "
          f"(observed {primary['discrimination_pp']:+.2f} pp; "
          f"target >= {BAR_2_DISC_PP:+.1f} pp)")
    print(f"    Bar 3 (block-perm p < 0.05):          "
          f"{'PASS' if primary['bar3_p_lt_0_05'] else 'FAIL'} "
          f"(p = {primary['block_perm_p_value']:.4f})")

    sens_verdicts = {k: v["verdict"] for k, v in sens_arms.items()}
    sens_disc = {k: v["discrimination_pp"] for k, v in sens_arms.items()}
    fragility_flags = {
        k: ("flagged" if v["verdict"] != primary["verdict"] else "consistent")
        for k, v in sens_arms.items()
    }

    # Write result-data.json.
    out_data = {
        "schema_version": 1,
        "pre_reg_lock_commit": PRE_REG_LOCK_COMMIT,
        "pre_reg_footer_fix": PRE_REG_FOOTER_FIX,
        "pipeline_commit": PIPELINE_COMMIT,
        "random_seed_perm": RANDOM_SEED,
        "ha11_v1_seed": HA11_V1_SEED,
        "B_headline": B_HEADLINE,
        "expected_block_length": BOOTSTRAP_E_L,
        "n_std_primary": N_STD_PRIMARY,
        "bar_2_disc_pp": BAR_2_DISC_PP,
        "bar_3_p_value": BAR_3_P_VALUE,
        "ha11_v1_train_disc_pp_reference": HA11_V1_TRAIN_DISC_PP,
        "pinned": {
            "n_effective": PINNED_N_EFFECTIVE,
            "sigma_median": PINNED_SIGMA_MEDIAN,
        },
        "dry_run_gates": gate_outcomes,
        "primary": _serialise(primary),
        "sensitivity_arms": {k: _serialise(v) for k, v in sens_arms.items()},
        "crash_drop": _serialise(crash_dropped),
        "crash_drop_delta_pp": delta_pp,
        "crash_drop_flag_fired": crash_drop_flag,
        "per_bout_n_report": pb_report,
        "sensitivity_fragility_flags": fragility_flags,
    }
    OUT_RESULT_JSON.write_text(
        json.dumps(out_data, indent=2, default=str), encoding="utf-8"
    )
    print(f"\nWrote {OUT_RESULT_JSON}")
    return 0


def _print_arm_summary(r: dict) -> None:
    print(f"  arm='{r['arm_name']}' n_calm={r['n_calm']} n_crash={r['n_crash']}; "
          f"frac_calm={r['frac_calm']*100:.1f}% frac_crash={r['frac_crash']*100:.1f}%; "
          f"disc={r['discrimination_pp']:+.2f} pp")
    print(f"    Cliff's delta={r['cliffs_delta']:+.3f} "
          f"CI95=[{r['cliffs_delta_ci95_lo']:+.3f}, {r['cliffs_delta_ci95_hi']:+.3f}]; "
          f"MW-U={r['mannwhitney_u']:.0f} p_norm={r['mannwhitney_p_normal_one_sided']:.4f}")
    print(f"    block-perm p={r['block_perm_p_value']:.4f} "
          f"(B={r['block_perm_B']}, n_ge={r['block_perm_n_ge']})")
    print(f"    median signed z triggering={r['median_signed_z_triggering_crash']:.3f}")
    print(f"    bars met: {r['bars_met']}/3; verdict={r['verdict']}")


def _serialise(r: dict) -> dict:
    """Drop large arrays from arm dict before JSON serialisation."""
    out = {k: v for k, v in r.items() if k not in ("zs_calm", "zs_crash")}
    return out


if __name__ == "__main__":
    raise SystemExit(main())
