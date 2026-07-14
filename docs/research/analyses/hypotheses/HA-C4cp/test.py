"""HA-C4cp - Personal-baseline SD-anchored sister-test to HA-C4c.

Implements the LOCKED r2 pre-registration (hypothesis.md LOCKED 2026-07-09 r2)
per its section 10 detection script architecture. Sister-pre-reg to HA-C4c on
the personal-baseline-rolling reference frame (parent MD
`bout_level_recovery_dynamics.md` LOCKED r3 2026-07-09 section 3.2.2 SD-anchored
derivative operand family).

What this test does (per pre-reg sections 1, 4, 5, 10):
  - Loads `bout_n_did_not_return_2sd_day` (per-day count of bouts with
    `did_not_return_2sd_flag == True` per parent MD section 3.2.2) from
    per_day_master.csv (joined by the pipeline from per_bout_master.csv at
    Bundle H+ event 8 pipeline commit 521e9fe).
  - Also loads Z=1 count, z_max continuous, and reference-window audit-trace
    columns (`subject_lagged_median_day`, `subject_lagged_mad_day`).
  - Filters to the section 4.2 primary stratum (verbatim from HA-C4c section
    4.2): cross-phase-pooled on the citalopram_phase axis, restricted on the
    recovery_phase axis to sub-phase 4b (pacing_habit_established) UNION
    phase 5 (citalopram_modulated).
  - Applies section 4.4 day-validity (verbatim from HA-C4c plus additive
    reference-window validity gate: `subject_lagged_median_day` non-NaN,
    implicitly enforced because reference-window-invalid days route the
    primary operand to NaN per parent MD section 3.2.2 NaN-propagation).
  - Classifies heavy-T vs non-heavy-T per section 4.3 (verbatim from HA-C4c
    section 4.3): heavy in {heavy, very_heavy}; non-heavy in {none, light,
    moderate}; otherwise excluded.
  - Computes Mann-Whitney U one-sided (heavy > non-heavy), Cliff's delta
    + paired-bootstrap 95% CI, and block-permutation p at E[L]=7 with
    B=10,000 draws and seed 20260709 per section 4.6.
  - Single-operand verdict bands per section 5: SUPPORTED iff both (a)
    discrimination + (b) effect-size (Cliff's delta >= +0.20); PARTIAL iff
    direction-correct + exactly one bar; REJECTED iff direction wrong OR
    both fail OR section 4.10 crash-drop sign-flip; INCONCLUSIVE iff
    section 4.7 walk-forward gate fails (n_heavy < 30 OR n_non_heavy < 30).
  - Section 4.10 sensitivity arms (10 arms):
    (1) z1_count - re-run on `bout_n_did_not_return_1sd_day`;
    (2) z_max_continuous - re-run on `bout_return_time_z_max_day`
        (continuous outcome; Mann-Whitney U applies unchanged);
    (3) reference_window_shorter_lag - re-aggregate SD-anchored operand
        from per_bout_master.csv with reference window [d-60, d-30]
        instead of [d-90, d-30];
    (4) unmedicated_only - restrict to citalopram_phase == unmedicated;
    (5) motion_clean_only - restrict to bouts with motion_confound_flag
        == False, re-aggregate per day (anticipated INCONCLUSIVE per
        HA-C4c section 8 caveat 4 corpus property 99.3%);
    (6) transient_excluded - restrict to bouts with transient_flag ==
        False, re-aggregate per day;
    (7) baseline_invalid_excluded - restrict to bouts with
        baseline_invalid_flag == False, re-aggregate per day;
    (8) crash_dropped - drop is_crash==True days from both arms;
    (9) reference_pool_did_not_return_excluded - reference pool excludes
        did_not_return_flag == True bouts (new for HA-C4cp; anticipated
        HIGHER flag rate per parent MD section 3.2.2 rationale);
    (10) approach_a_dose_adjusted - descriptive companion per section 4.9
         inheritance-by-analogue; primary + CI-lower + CI-upper sub-arms.
  - Section 5.3 Holm step-down across {primary, z1_count,
    z_max_continuous, reference_window_shorter_lag, unmedicated_only,
    motion_clean_only, transient_excluded} = 7 cells at alpha=0.05.
    baseline_invalid_excluded + crash_dropped + reference_pool_dnr_excluded
    + Approach A are NOT in the Holm family (descriptive variants per
    CONVENTIONS section 3.3 / section 3.4).

Modes:
  python test.py --dry-run    section 10.4 sanity gates + section 4.7
                              walk-forward gate + parent-operand
                              determinism check only. HALT if per-day
                              mean outside [0.01, 0.60] OR median > 2.
                              Route to INCONCLUSIVE per section 9.4 if
                              walk-forward gate fails on primary cell.
  python test.py              dry-run first; if all sanity gates PASS,
                              proceed to full run and emit result.md +
                              result-data.json.

ASCII-only stdout per project convention (no em-dash, no emojis); markdown
output may use unicode for readability.

Zero-vs-NaN discipline (per DATA_DICTIONARY section 8E + parent MD
section 4): the SD-anchored count columns MUST NEVER be `.fillna(0)`. NaN
means reference-window invalid (< 30 bouts in [d-90, d-30]); treating as
0 would fold reference-window-invalid days into zero-count days and bias
downstream contrasts toward null. All loaders below preserve the
None/NaN semantic explicitly.
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


# === Constants per LOCKED r2 hypothesis.md =============================

HA_ID = "HA-C4cp"

# Eras (verbatim from HA-C4c / HA11-bout-redo conventions)
LC_ERA_START = date(2022, 4, 4)
SUB_PHASE_4B_START = date(2022, 11, 17)  # left edge of primary stratum per section 4.2
UNMED_END = date(2024, 4, 8)             # citalopram start = 2024-04-09
APRIL_2024_CLUSTER_START = date(2024, 4, 9)
APRIL_2024_CLUSTER_END = date(2024, 4, 16)
DEVICE_BASELINE_LAG_DAYS = 21            # parent MD section 3.4

# Primary stratum (section 4.2): recovery_phase axis labels
PRIMARY_RECOVERY_PHASES = {"pacing_habit_established", "citalopram_modulated"}

# Heavy-T classification (section 4.3 verbatim from HA-C4c section 4.3)
HEAVY_CLASSES = {"heavy", "very_heavy"}
NON_HEAVY_CLASSES = {"none", "light", "moderate"}

# Statistical machinery (section 4.6)
RANDOM_SEED = 20260709                   # HA-C4cp block-permutation seed (per section 4.6)
BOOTSTRAP_E_L = 7                        # E[L]=7 per permutation_null_block_length.md
B_HEADLINE = 10_000                      # B draws per section 4.6
N_BOOTSTRAP_CLIFFS_CI = 2000             # paired-bootstrap CI on Cliff's delta

# Verdict bars (section 5.1)
BAR_A_P_VALUE = 0.05                     # block-permutation p < 0.05
BAR_B_CLIFFS_DELTA = 0.20                # Cliff's delta >= +0.20 (retained sister-pattern per user Q 2026-07-09)

# Walk-forward gate (section 4.7)
WF_GATE_N_HEAVY = 30
WF_GATE_N_NON_HEAVY = 30

# Sanity-check gates (section 7 + section 10.4)
# HALT bar: mean outside [0.01, 0.60]; median > 2.
# Informational-only bars (do NOT HALT): mean inside [0.05, 0.30]; median in [0, 1].
SANITY_HALT_MEAN_MIN = 0.01
SANITY_HALT_MEAN_MAX = 0.60
SANITY_HALT_MEDIAN_MAX = 2.0
SANITY_INFO_MEAN_MIN = 0.05
SANITY_INFO_MEAN_MAX = 0.30
SANITY_INFO_MEDIAN_MAX = 1.0

# Parent-operand determinism check target (per Stage D descriptive_audit.md
# LOCKED r1 2026-07-14 section 1: on frozen 1274-day HA-C4c-vintage stratum,
# parent operand bout_n_did_not_return mean = 0.6444 byte-identically).
# On the current-corpus 1289-day stratum the mean is expected at ~0.6485.
PARENT_OP_TARGET_MEAN_HAC4C_VINTAGE = 0.6444
PARENT_OP_TARGET_MEAN_CURRENT_CORPUS = 0.6485
PARENT_OP_TARGET_TOL = 0.02  # tolerance for corpus-growth attributable drift

# Crash-drop sensitivity flag (section 4.10 + CONVENTIONS section 3.4)
CRASH_DROP_FLAG_DELTA_DELTA = 0.10       # |Delta Cliff's delta| > 0.10 (HA-C4c pattern)
CRASH_DROP_FLAG_DELTA_DELTA_REJECT = 0.20  # > 0.20 AND sign-flip routes to REJECTED
CRASH_DROP_FLAG_DELTA_PP_PRIMARY = 5.0   # |Delta discrimination pp| > 5 (HA11-bout-redo pattern)

# Approach A inheritance-by-analogue beta (section 4.9; descriptive companion only)
# bout_n_fast_recovery_day buildup-post-CPAP beta = -0.056/mg
# [CI -0.145, +0.034] per recalibration sub-MD section 6; sign-flipped to +1 prior
# direction for HA-C4cp (more failures-to-return-within-tail under elevated
# sympathetic tone; same sign-flip logic as HA-C4c section 4.9).
APPROACH_A_BETA_PRIMARY = 0.056          # sign-flipped from -0.056/mg
APPROACH_A_BETA_CI_LOWER = 0.145         # sign-flipped from -0.145/mg (NULL-bracket)
APPROACH_A_BETA_CI_UPPER = -0.034        # sign-flipped from +0.034/mg (NULL-bracket)

# Reference-window definitions (section 4.10 reference_window_shorter_lag)
REFERENCE_WINDOW_PRIMARY = (90, 30)      # [d-90, d-30] per parent MD section 3.2.2
REFERENCE_WINDOW_SHORTER = (60, 30)      # [d-60, d-30] per section 4.10 sensitivity
REFERENCE_WINDOW_MIN_BOUTS = 30          # >= 30 bouts validity bar per parent MD section 3.2.2

# Holm step-down family (section 5.3): primary + 6 sensitivity arms = 7 cells
HOLM_ALPHA = 0.05
HOLM_FAMILY_LABELS = [
    "primary",
    "z1_count",
    "z_max_continuous",
    "reference_window_shorter_lag",
    "unmedicated_only",
    "motion_clean_only",
    "transient_excluded",
]

# Column names in per_day_master.csv (per DATA_DICTIONARY section 8E)
COL_PRIMARY = "bout_n_did_not_return_2sd_day"
COL_Z1 = "bout_n_did_not_return_1sd_day"
COL_ZMAX = "bout_return_time_z_max_day"
COL_REF_MEDIAN = "subject_lagged_median_day"
COL_REF_MAD = "subject_lagged_mad_day"
COL_PARENT_OP = "bout_n_did_not_return"  # HA-C4c parent operand (for cross-op concordance + determinism check)

# Pipeline + pre-reg commits
PIPELINE_COMMIT = "521e9fe"              # Bundle H+ event 8 pipeline extension
PRE_REG_LOCK_COMMIT = "hypothesis.md r2 LOCKED 2026-07-09"

# Paths
DATA_ROOT = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH",
    r"C:\Users\Gebruiker\Documents\gevoelscore-data"))
PER_DAY_CSV = DATA_ROOT / "unified" / "per_day_master.csv"
PER_BOUT_CSV = DATA_ROOT / "unified" / "per_bout_master.csv"
LABELS_CSV = DATA_ROOT / "processed" / "crash_labels" / "labels_crash_v2.csv"

OUT_RESULT_JSON = HERE / "result-data.json"
OUT_RESULT_MD = HERE / "result.md"


# === Loaders ============================================================

def _parse_bool(s: str) -> bool:
    return s.strip().lower() == "true"


def _parse_float(s: str) -> float | None:
    """Return None on empty / NaN / unparseable. NEVER return 0.0 for empty
    (zero-vs-NaN discipline per DATA_DICTIONARY section 8E)."""
    if s == "" or s is None:
        return None
    try:
        v = float(s)
        if math.isnan(v):
            return None
        return v
    except (ValueError, TypeError):
        return None


def load_per_day_master() -> dict[date, dict]:
    """Return per-date dict of fields needed for the test.

    Each entry:
      {bout_n_did_not_return_2sd_day,       # primary operand
       bout_n_did_not_return_1sd_day,       # Z=1 sensitivity operand
       bout_return_time_z_max_day,          # continuous sensitivity operand
       subject_lagged_median_day,           # reference-window audit trace
       subject_lagged_mad_day,              # reference-window audit trace
       bout_n_did_not_return,               # HA-C4c parent operand (for cross-op)
       has_garmin_uds, is_crash,
       exertion_class_lagged_lcera, recovery_phase, dose_plasma_mg}.

    Zero-vs-NaN discipline: for the 5 SD-anchored per-day columns, empty
    string / NaN cell -> None. NEVER coerced to 0. Parent MD section 4 +
    DATA_DICTIONARY section 8E load-bearing rule.
    """
    out: dict[date, dict] = {}
    with PER_DAY_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            out[d] = {
                COL_PRIMARY: _parse_float(r.get(COL_PRIMARY, "")),
                COL_Z1: _parse_float(r.get(COL_Z1, "")),
                COL_ZMAX: _parse_float(r.get(COL_ZMAX, "")),
                COL_REF_MEDIAN: _parse_float(r.get(COL_REF_MEDIAN, "")),
                COL_REF_MAD: _parse_float(r.get(COL_REF_MAD, "")),
                COL_PARENT_OP: _parse_float(r.get(COL_PARENT_OP, "")),
                "has_garmin_uds": _parse_bool(r.get("has_garmin_uds", "")),
                "is_crash": _parse_bool(r.get("is_crash", "")),
                "exertion_class_lagged_lcera": (
                    r.get("exertion_class_lagged_lcera", "") or "").strip(),
                "recovery_phase": (r.get("recovery_phase", "") or "").strip(),
                "dose_plasma_mg": _parse_float(
                    r.get("dose_plasma_mg", "")) or 0.0,
            }
    return out


def load_per_bout_master() -> list[dict]:
    """Return per-bout records with flags + tail_length + citalopram_phase for
    section 4.10 sensitivity-arm re-aggregation. `tail_length` is needed for
    the reference_window_shorter_lag re-aggregation which recomputes
    subject_lagged_median + subject_lagged_mad on [d-60, d-30] instead of
    the pipeline-default [d-90, d-30].
    """
    out: list[dict] = []
    with PER_BOUT_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                d = date.fromisoformat(r["date"])
            except (KeyError, ValueError):
                continue
            tail_length = _parse_float(r.get("tail_length", ""))
            out.append({
                "date": d,
                "tail_length": tail_length,
                "did_not_return_flag": _parse_bool(
                    r.get("did_not_return_flag", "")),
                "did_not_return_1sd_flag": _parse_bool(
                    r.get("did_not_return_1sd_flag", "")),
                "did_not_return_2sd_flag": _parse_bool(
                    r.get("did_not_return_2sd_flag", "")),
                "motion_confound_flag": _parse_bool(
                    r.get("motion_confound_flag", "")),
                "transient_flag": _parse_bool(r.get("transient_flag", "")),
                "baseline_invalid_flag": _parse_bool(
                    r.get("baseline_invalid_flag", "")),
                "citalopram_phase": (
                    r.get("citalopram_phase", "") or "").strip(),
            })
    return out


# === Day-validity gate (section 4.4) ====================================

def device_baseline_lag_set(master: dict[date, dict]) -> set[date]:
    uds_dates = sorted(d for d, info in master.items()
                       if info["has_garmin_uds"])
    return set(uds_dates[:DEVICE_BASELINE_LAG_DAYS])


def day_in_primary_stratum(d: date, master: dict[date, dict]) -> bool:
    """Section 4.2 primary stratum verbatim from HA-C4c: sub-phase 4b UNION
    phase 5 on recovery_phase axis. Equivalently: LC era AND date >=
    2022-11-17 AND recovery_phase in PRIMARY_RECOVERY_PHASES.
    """
    if d < SUB_PHASE_4B_START:
        return False
    info = master.get(d)
    if not info:
        return False
    return info["recovery_phase"] in PRIMARY_RECOVERY_PHASES


def day_in_unmedicated_only(d: date, master: dict[date, dict]) -> bool:
    """Section 4.10 unmedicated-only sensitivity arm: section 4.2 stratum
    restricted to pre-citalopram (date <= 2024-04-08). Equivalently:
    recovery_phase == pacing_habit_established AND date in [2022-11-17,
    2024-04-08].
    """
    if not day_in_primary_stratum(d, master):
        return False
    return d <= UNMED_END


def day_is_valid(
    d: date,
    master: dict[date, dict],
    baseline_lag: set[date],
    *,
    stratum_fn,
    operand_col: str = COL_PRIMARY,
) -> bool:
    """Section 4.4 day-validity gate.

    1. d is in the stratum (per stratum_fn = day_in_primary_stratum or
       day_in_unmedicated_only).
    2. d is NOT in April 2024 cluster (2024-04-09 -> 2024-04-16).
    3. d is NOT in first 21 device-baseline days.
    4. d has computable operand (non-NaN per pipeline day-validity gate;
       for the SD-anchored primary operand this implicitly enforces the
       reference-window validity bar: bout_n_did_not_return_2sd_day is
       NaN on days where subject_lagged_median_day is NaN, which per
       parent MD section 3.2.2 fires when the [d-90, d-30] reference
       pool has < 30 bouts).
    5. d has computable exertion_class_lagged_lcera (non-empty).
    """
    if not stratum_fn(d, master):
        return False
    if APRIL_2024_CLUSTER_START <= d <= APRIL_2024_CLUSTER_END:
        return False
    if d in baseline_lag:
        return False
    info = master[d]
    if info.get(operand_col) is None:
        return False
    if not info["exertion_class_lagged_lcera"]:
        return False
    return True


# === Heavy-T classification (section 4.3) ==============================

def is_heavy_T(d: date, master: dict[date, dict]) -> bool | None:
    """Section 4.3 verbatim from HA-C4c section 4.3: heavy if
    exertion_class_lagged_lcera in {heavy, very_heavy}; non-heavy if in
    {none, light, moderate}; None otherwise (excluded).
    """
    cls = master[d]["exertion_class_lagged_lcera"]
    if not cls:
        return None
    if cls in HEAVY_CLASSES:
        return True
    if cls in NON_HEAVY_CLASSES:
        return False
    return None


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


def mann_whitney_u(arm1: np.ndarray, arm2: np.ndarray) -> tuple[float, float]:
    """One-sided U + normal-approx p for H1: arm1 > arm2.

    Returns (U, p_normal_approx). Descriptive companion to block-perm p.
    Applies unchanged to continuous outcomes (z_max sensitivity arm).
    """
    pooled = np.concatenate([arm1, arm2])
    ranks = _rankdata(pooled)
    n1 = len(arm1)
    n2 = len(arm2)
    R1 = float(ranks[:n1].sum())
    U = R1 - n1 * (n1 + 1) / 2.0
    mean_U = n1 * n2 / 2.0
    var_U = n1 * n2 * (n1 + n2 + 1) / 12.0
    if var_U <= 0 or n1 < 2 or n2 < 2:
        return U, float("nan")
    z = (U - mean_U) / math.sqrt(var_U)
    p = 0.5 * math.erfc(z / math.sqrt(2.0))
    return U, float(p)


def cliffs_delta(arm1: np.ndarray, arm2: np.ndarray) -> float:
    """Cliff's delta = (#{arm1>arm2} - #{arm1<arm2}) / (n1 * n2)."""
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
    *, n_bootstrap: int = N_BOOTSTRAP_CLIFFS_CI,
    random_state: int = RANDOM_SEED,
) -> tuple[float, float]:
    """95% CI on Cliff's delta via paired-bootstrap of the two arms."""
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


def stationary_bootstrap_indices(
    n: int, p: float, rng: np.random.Generator,
) -> np.ndarray:
    """Politis-Romano stationary bootstrap indices."""
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
    dates: list[date],
    is_heavy: list[bool],
    values: list[float],
    *,
    B: int,
    expected_block_length: int,
    seed: int,
    observed_cliffs_delta: float,
) -> dict:
    """Block-permutation null per section 4.6.

    Stationary-bootstrap-resample the is_heavy label sequence with E[L]=7
    while keeping per-day values fixed in their temporal positions. On each
    draw, partition values by the resampled label and recompute Cliff's
    delta. Empirical one-sided p = (1 + #{delta_null >= observed_delta}) /
    (B + 1) for the heavy > non-heavy direction.

    Note: applies unchanged to continuous outcomes (z_max sensitivity arm)
    since Cliff's delta operates on any ordered numeric.
    """
    rng = np.random.default_rng(seed)
    n_obs = len(dates)
    p = 1.0 / expected_block_length
    label_arr = np.asarray(is_heavy, dtype=bool)
    val_arr = np.asarray(values, dtype=float)

    null_deltas = np.empty(B)
    null_n_heavy = np.empty(B, dtype=int)
    for b in range(B):
        idx = stationary_bootstrap_indices(n_obs, p, rng)
        perm_labels = label_arr[idx]
        h_mask = perm_labels
        nh_mask = ~perm_labels
        n_h = int(h_mask.sum())
        n_nh = int(nh_mask.sum())
        null_n_heavy[b] = n_h
        if n_h < 2 or n_nh < 2:
            null_deltas[b] = float("nan")
            continue
        h_vals = val_arr[h_mask]
        nh_vals = val_arr[nh_mask]
        null_deltas[b] = cliffs_delta(h_vals, nh_vals)

    null_clean = null_deltas[~np.isnan(null_deltas)]
    n_ge = int((null_clean >= observed_cliffs_delta).sum())
    p_value = (1 + n_ge) / (len(null_clean) + 1)
    return {
        "p_value": float(p_value),
        "n_ge": n_ge,
        "B": int(len(null_clean)),
        "null_delta_median": float(np.median(null_clean)) if len(null_clean) else float("nan"),
        "null_delta_p025": float(np.quantile(null_clean, 0.025)) if len(null_clean) else float("nan"),
        "null_delta_p975": float(np.quantile(null_clean, 0.975)) if len(null_clean) else float("nan"),
        "n_heavy_null_mean": float(null_n_heavy.mean()),
        "n_heavy_null_std": float(null_n_heavy.std()),
    }


# === Sensitivity-arm bout-count re-aggregation (section 4.10) ===========

def reaggregate_sd_anchored_flag_only(
    per_bout: list[dict],
    *,
    motion_clean: bool = False,
    transient_excluded: bool = False,
    baseline_invalid_excluded: bool = False,
) -> dict[date, int]:
    """Re-compute per-day count of did_not_return_2sd bouts with the specified
    per-bout flag filter(s) applied.

    Uses the pre-computed did_not_return_2sd_flag from per_bout_master.csv;
    does NOT re-compute the reference window (that's the
    reaggregate_sd_anchored_shorter_lag helper below). Only filters WHICH
    bouts are counted at the day-level rollup.

    Returns date -> integer count. Days with zero qualifying bouts emit 0
    (matching the pipeline's zero-vs-NaN convention where the base day was
    reference-window-valid and simply had no flagged bouts).
    """
    counts: dict[date, int] = {}
    all_dates = set(b["date"] for b in per_bout)
    for d in all_dates:
        counts[d] = 0
    for b in per_bout:
        if motion_clean and b["motion_confound_flag"]:
            continue
        if transient_excluded and b["transient_flag"]:
            continue
        if baseline_invalid_excluded and b["baseline_invalid_flag"]:
            continue
        if b["did_not_return_2sd_flag"]:
            counts[b["date"]] = counts.get(b["date"], 0) + 1
    return counts


def reaggregate_sd_anchored_shorter_lag(
    per_bout: list[dict],
    master: dict[date, dict],
    *,
    window_high: int = 60,   # d-60
    window_low: int = 30,    # d-30
    min_bouts: int = REFERENCE_WINDOW_MIN_BOUTS,
    exclude_did_not_return_bouts: bool = False,
) -> tuple[dict[date, float], dict[date, tuple[float, float]]]:
    """Re-aggregate the SD-anchored per-day count with a shorter reference
    window ([d-60, d-30] instead of pipeline-default [d-90, d-30]).

    Mirrors parent MD section 3.2.2 reference-window construction:
      - reference pool = per-bout tail_length values from LC-era days in
        [d - window_high, d - window_low], with April 2024 cluster and
        first-21-device-baseline-day exclusions.
      - subject_lagged_median = median of pool.
      - subject_lagged_mad = 1.4826 * MAD of pool.
      - validity bar: >= min_bouts (default 30) bouts in pool.
      - candidate day d excluded from its own pool via window edge (d-30).
      - did_not_return_flag bouts INCLUDED in reference by default (parent
        MD section 3.2.2 rationale); pass exclude_did_not_return_bouts=True
        for the reference-pool-did-not-return-excluded sensitivity arm.
      - candidate-day per-bout flag: tail_length > median + 2 * mad.

    Returns (counts_by_date, ref_stats_by_date) where:
      counts_by_date: date -> per-day count as float. NaN (float('nan')) if
        reference window is invalid (< min_bouts). Zero if reference window
        valid but no flagged bouts on candidate day.
      ref_stats_by_date: date -> (median, mad) for audit-trace reporting.

    This helper is exercised for the reference_window_shorter_lag sensitivity
    arm AND for the reference_pool_did_not_return_excluded sensitivity arm.
    Both re-compute the reference distribution from per-bout tail_length; the
    difference is only which bouts are eligible for the reference pool.
    """
    # Index bouts by date for fast lookup + LC-era + April-2024-cluster gating.
    bouts_by_date: dict[date, list[dict]] = {}
    for b in per_bout:
        d = b["date"]
        if d < LC_ERA_START:
            continue
        if APRIL_2024_CLUSTER_START <= d <= APRIL_2024_CLUSTER_END:
            continue
        if b["tail_length"] is None:
            continue
        bouts_by_date.setdefault(d, []).append(b)

    baseline_lag = device_baseline_lag_set(master)

    counts: dict[date, float] = {}
    ref_stats: dict[date, tuple[float, float]] = {}

    all_candidate_dates = sorted(bouts_by_date.keys())
    for d in all_candidate_dates:
        # Build reference pool: bouts on days in [d - window_high, d - window_low].
        pool: list[float] = []
        for offset in range(window_low, window_high + 1):
            ref_d = d - timedelta(days=offset)
            if ref_d in baseline_lag:
                continue
            for b in bouts_by_date.get(ref_d, []):
                if exclude_did_not_return_bouts and b["did_not_return_flag"]:
                    continue
                pool.append(b["tail_length"])

        if len(pool) < min_bouts:
            # Reference-window invalid; operand NaN per parent MD section 3.2.2.
            counts[d] = float("nan")
            ref_stats[d] = (float("nan"), float("nan"))
            continue

        pool_arr = np.asarray(pool, dtype=float)
        med = float(np.median(pool_arr))
        mad_raw = float(np.median(np.abs(pool_arr - med)))
        mad = 1.4826 * mad_raw
        ref_stats[d] = (med, mad)

        if mad <= 0:
            # Degenerate MAD; cannot compute Z (division by zero). Route to NaN.
            counts[d] = float("nan")
            continue

        # Count candidate-day bouts with tail_length > median + 2*mad.
        threshold = med + 2.0 * mad
        n_flagged = sum(
            1 for b in bouts_by_date.get(d, [])
            if b["tail_length"] is not None and b["tail_length"] > threshold
        )
        counts[d] = float(n_flagged)

    return counts, ref_stats


def overlay_column(
    primary: dict[date, dict],
    new_values: dict[date, float | int],
    target_col: str,
    *,
    require_original_non_nan: bool = True,
) -> dict[date, dict]:
    """Overlay re-computed per-day values onto a copy of the master.

    If require_original_non_nan is True, days that were originally NaN on the
    target column remain NaN (preserving the pipeline day-validity semantics
    per parent MD section 3.4). If False, the new value is written unconditionally
    (used for the reference_window_shorter_lag arm where the re-computation
    may validate days that were NaN on the [d-90, d-30] window OR invalidate
    days that were valid on it -- but per section 4.10, we honour whichever
    the re-computation says because the window definition itself changed).

    For flag-only re-aggregations (motion_clean, transient_excluded,
    baseline_invalid_excluded): the reference window is unchanged, so we
    respect the original NaN semantic.
    For reference_window_shorter_lag + reference_pool_did_not_return_excluded:
    the re-computed values are authoritative (they reflect the new window /
    pool definition).
    """
    out: dict[date, dict] = {}
    for d, info in primary.items():
        new_info = dict(info)
        if require_original_non_nan:
            if info.get(target_col) is None:
                new_info[target_col] = None
            else:
                new_val = new_values.get(d, 0)
                if isinstance(new_val, float) and math.isnan(new_val):
                    new_info[target_col] = None
                else:
                    new_info[target_col] = float(new_val)
        else:
            new_val = new_values.get(d)
            if new_val is None:
                new_info[target_col] = None
            elif isinstance(new_val, float) and math.isnan(new_val):
                new_info[target_col] = None
            else:
                new_info[target_col] = float(new_val)
        out[d] = new_info
    return out


# === Per-arm evaluation glue ============================================

def collect_arm_data(
    master: dict[date, dict],
    *,
    stratum_fn,
    operand_col: str = COL_PRIMARY,
    crash_drop: bool = False,
    dose_beta_per_mg: float | None = None,
) -> tuple[list[date], list[bool], list[float], int]:
    """Collect (dates, is_heavy_labels, values) over the stratum subject to
    section 4.4 day-validity + heavy-T classification eligibility.

    If crash_drop=True, days with is_crash=True are dropped from BOTH arms
    (section 4.10 crash-drop sensitivity arm).

    If dose_beta_per_mg is set, values are dose-adjusted per section 4.9
    Approach A descriptive companion:
      operand_adj(d) = operand(d) - beta_per_mg * dose_plasma_mg(d)

    Returns (dates, is_heavy, values, n_flagged_bouts) where n_flagged_bouts
    is the sum across qualifying days for per-bout n reporting per
    section 4.11. For count operands (Z=1, Z=2, parent) this is the count
    sum; for continuous operands (z_max) this is 0 (no meaningful bout
    count from a max statistic).
    """
    baseline_lag = device_baseline_lag_set(master)
    dates: list[date] = []
    is_heavy: list[bool] = []
    values: list[float] = []
    n_flagged_bouts = 0
    is_count_operand = operand_col in (
        COL_PRIMARY, COL_Z1, COL_PARENT_OP)
    for d in sorted(master.keys()):
        if not day_is_valid(d, master, baseline_lag,
                            stratum_fn=stratum_fn,
                            operand_col=operand_col):
            continue
        info = master[d]
        if crash_drop and info["is_crash"]:
            continue
        h = is_heavy_T(d, master)
        if h is None:
            continue
        raw_v = info[operand_col]
        v = float(raw_v)
        if dose_beta_per_mg is not None:
            v = v - dose_beta_per_mg * info["dose_plasma_mg"]
        dates.append(d)
        is_heavy.append(h)
        values.append(v)
        if is_count_operand:
            n_flagged_bouts += int(raw_v)
    return dates, is_heavy, values, n_flagged_bouts


def reference_window_audit_stats(
    master: dict[date, dict],
    dates: list[date],
    is_heavy: list[bool],
) -> dict:
    """Per section 4.11: per-arm distribution of subject_lagged_median_day +
    subject_lagged_mad_day (mean, median, IQR). Uses the pipeline-emitted
    audit-trace columns COL_REF_MEDIAN / COL_REF_MAD.
    """
    heavy_med = []
    heavy_mad = []
    nonheavy_med = []
    nonheavy_mad = []
    for d, h in zip(dates, is_heavy):
        info = master.get(d, {})
        med = info.get(COL_REF_MEDIAN)
        mad = info.get(COL_REF_MAD)
        if med is None or mad is None:
            continue
        if h:
            heavy_med.append(med)
            heavy_mad.append(mad)
        else:
            nonheavy_med.append(med)
            nonheavy_mad.append(mad)

    def _summ(arr: list[float]) -> dict:
        if not arr:
            return {"mean": float("nan"), "median": float("nan"),
                    "p25": float("nan"), "p75": float("nan"),
                    "n": 0}
        a = np.asarray(arr, dtype=float)
        return {
            "mean": float(a.mean()),
            "median": float(np.median(a)),
            "p25": float(np.quantile(a, 0.25)),
            "p75": float(np.quantile(a, 0.75)),
            "n": int(len(a)),
        }

    return {
        "heavy_lagged_median": _summ(heavy_med),
        "heavy_lagged_mad": _summ(heavy_mad),
        "non_heavy_lagged_median": _summ(nonheavy_med),
        "non_heavy_lagged_mad": _summ(nonheavy_mad),
    }


def reference_window_failure_count(
    master: dict[date, dict],
    *,
    stratum_fn,
) -> int:
    """Per section 4.11: per-arm count of days routed to NaN via section 4.4
    gate 4 reference-window shortfall (implicit via NaN on COL_PRIMARY).
    """
    baseline_lag = device_baseline_lag_set(master)
    n_failed = 0
    for d, info in master.items():
        if not stratum_fn(d, master):
            continue
        if APRIL_2024_CLUSTER_START <= d <= APRIL_2024_CLUSTER_END:
            continue
        if d in baseline_lag:
            continue
        if not info["exertion_class_lagged_lcera"]:
            continue
        # Reference-window shortfall proxy: primary operand NaN OR reference
        # median NaN.
        if info.get(COL_PRIMARY) is None or info.get(COL_REF_MEDIAN) is None:
            n_failed += 1
    return n_failed


def evaluate_arm(
    arm_name: str,
    master: dict[date, dict],
    *,
    stratum_fn,
    operand_col: str = COL_PRIMARY,
    crash_drop: bool = False,
    dose_beta_per_mg: float | None = None,
    run_permutation: bool = True,
    compute_el_companion: bool = True,
) -> dict:
    """End-to-end evaluation of one arm. Returns dict with the full metric
    set per section 5 verdict bands and section 4.6 statistical machinery.
    """
    dates, is_heavy, values, n_flagged = collect_arm_data(
        master, stratum_fn=stratum_fn,
        operand_col=operand_col,
        crash_drop=crash_drop,
        dose_beta_per_mg=dose_beta_per_mg,
    )
    val_arr = np.asarray(values, dtype=float)
    heavy_mask = np.asarray(is_heavy, dtype=bool)
    heavy_vals = val_arr[heavy_mask]
    non_heavy_vals = val_arr[~heavy_mask]
    n_heavy = int(heavy_mask.sum())
    n_non_heavy = int((~heavy_mask).sum())

    # Walk-forward gate per section 4.7
    inconclusive = (n_heavy < WF_GATE_N_HEAVY) or (n_non_heavy < WF_GATE_N_NON_HEAVY)

    # Per-arm descriptives
    heavy_mean = float(heavy_vals.mean()) if n_heavy > 0 else float("nan")
    heavy_median = float(np.median(heavy_vals)) if n_heavy > 0 else float("nan")
    non_heavy_mean = float(non_heavy_vals.mean()) if n_non_heavy > 0 else float("nan")
    non_heavy_median = float(np.median(non_heavy_vals)) if n_non_heavy > 0 else float("nan")

    # Cliff's delta + 95% CI + Mann-Whitney + descriptive normal-approx p
    if n_heavy >= 2 and n_non_heavy >= 2:
        delta = cliffs_delta(heavy_vals, non_heavy_vals)
        delta_ci_lo, delta_ci_hi = cliffs_delta_ci(heavy_vals, non_heavy_vals)
        U, p_normal = mann_whitney_u(heavy_vals, non_heavy_vals)
    else:
        delta = float("nan")
        delta_ci_lo = float("nan")
        delta_ci_hi = float("nan")
        U = float("nan")
        p_normal = float("nan")

    # Block-permutation null (section 4.6)
    block_perm = {
        "p_value": float("nan"), "n_ge": 0, "B": 0,
        "null_delta_median": float("nan"),
        "null_delta_p025": float("nan"),
        "null_delta_p975": float("nan"),
        "n_heavy_null_mean": float("nan"),
        "n_heavy_null_std": float("nan"),
    }
    if run_permutation and not inconclusive and not math.isnan(delta):
        block_perm = block_permutation_p_value(
            dates, is_heavy, values,
            B=B_HEADLINE,
            expected_block_length=BOOTSTRAP_E_L,
            seed=RANDOM_SEED,
            observed_cliffs_delta=delta,
        )

    # E[L]* data-driven companion (section 4.6)
    el_companion = None
    if compute_el_companion and not inconclusive:
        el_res = compute_data_driven_block_length(val_arr)
        el_companion = {
            "optimal_block_length": el_res["optimal_block_length"],
            "flagged_deviation": bool(el_res["flagged_deviation"]),
            "cutoff_lag": el_res["cutoff_lag"],
        }

    # Per-bar verdicts per section 5.1
    bar_a = (block_perm["p_value"] < BAR_A_P_VALUE) if not math.isnan(
        block_perm["p_value"]) else None
    bar_b = (delta >= BAR_B_CLIFFS_DELTA) if not math.isnan(delta) else None
    direction_correct = (delta > 0) if not math.isnan(delta) else None

    if inconclusive:
        verdict = "INCONCLUSIVE"
    elif direction_correct is None or bar_a is None or bar_b is None:
        verdict = "INCONCLUSIVE"
    elif not direction_correct:
        verdict = "REJECTED"
    elif bar_a and bar_b:
        verdict = "SUPPORTED"
    elif bar_a or bar_b:
        verdict = "PARTIAL"
    else:
        verdict = "REJECTED"

    # Per-day distribution summary
    all_vals = val_arr[~np.isnan(val_arr)]
    if len(all_vals) > 0:
        pool_mean = float(all_vals.mean())
        pool_median = float(np.median(all_vals))
        pool_std = float(all_vals.std(ddof=1)) if len(all_vals) > 1 else float("nan")
        pool_min = float(all_vals.min())
        pool_max = float(all_vals.max())
        pool_p25 = float(np.quantile(all_vals, 0.25))
        pool_p75 = float(np.quantile(all_vals, 0.75))
    else:
        pool_mean = pool_median = pool_std = pool_min = pool_max = float("nan")
        pool_p25 = pool_p75 = float("nan")

    # Reference-window audit trace per section 4.11
    ref_audit = reference_window_audit_stats(master, dates, is_heavy)

    return {
        "arm_name": arm_name,
        "operand_col": operand_col,
        "n_heavy": n_heavy,
        "n_non_heavy": n_non_heavy,
        "n_flagged_bouts": n_flagged,
        "heavy_mean": heavy_mean,
        "heavy_median": heavy_median,
        "non_heavy_mean": non_heavy_mean,
        "non_heavy_median": non_heavy_median,
        "cliffs_delta": delta,
        "cliffs_delta_ci95_lo": delta_ci_lo,
        "cliffs_delta_ci95_hi": delta_ci_hi,
        "mannwhitney_u": U,
        "mannwhitney_p_normal_one_sided": p_normal,
        "block_perm_p_value": block_perm["p_value"],
        "block_perm_n_ge": block_perm["n_ge"],
        "block_perm_B": block_perm["B"],
        "block_perm_null_delta_median": block_perm["null_delta_median"],
        "block_perm_null_delta_p025": block_perm["null_delta_p025"],
        "block_perm_null_delta_p975": block_perm["null_delta_p975"],
        "block_perm_n_heavy_null_mean": block_perm["n_heavy_null_mean"],
        "block_perm_n_heavy_null_std": block_perm["n_heavy_null_std"],
        "el_companion": el_companion,
        "bar_a_disc_p_lt_0_05": bar_a,
        "bar_b_cliffs_delta_geq_0_20": bar_b,
        "direction_correct": direction_correct,
        "verdict": verdict,
        "inconclusive": inconclusive,
        "crash_drop": crash_drop,
        "dose_beta_per_mg": dose_beta_per_mg,
        "pool_mean": pool_mean,
        "pool_median": pool_median,
        "pool_std": pool_std,
        "pool_p25": pool_p25,
        "pool_p75": pool_p75,
        "pool_min": pool_min,
        "pool_max": pool_max,
        "n_total_days": len(values),
        "reference_window_audit": ref_audit,
    }


# === Holm step-down (section 5.3) =======================================

def holm_step_down(p_values: list[float], labels: list[str],
                   alpha: float = HOLM_ALPHA) -> dict:
    """Holm step-down on a family of p-values. Returns per-test threshold +
    reject flag + adjusted p. NaN p-values are excluded (INCONCLUSIVE cells
    per section 5.3 fewer-comparisons disclosure).

    Cutoffs: alpha/k, alpha/(k-1), ..., alpha/1 where k = number of non-NaN
    p-values in the family.
    """
    valid = [(p, lab) for p, lab in zip(p_values, labels)
             if p is not None and not math.isnan(p)]
    omitted = [lab for p, lab in zip(p_values, labels)
               if p is None or math.isnan(p)]
    k = len(valid)
    if k == 0:
        return {
            "k": 0, "omitted": omitted,
            "per_cell": [],
            "annotation": (f"Holm (0-of-{len(labels)} sens arms; "
                           f"all INCONCLUSIVE)"),
        }
    sorted_valid = sorted(valid, key=lambda x: x[0])
    per_cell: list[dict] = []
    cumulative_failed = False
    prev_adj = 0.0
    for rank, (p, lab) in enumerate(sorted_valid):
        threshold = alpha / (k - rank)
        if cumulative_failed:
            rejected = False
        elif p <= threshold:
            rejected = True
        else:
            rejected = False
            cumulative_failed = True
        multiplier = k - rank
        adj_p = min(1.0, max(prev_adj, multiplier * p))
        prev_adj = adj_p
        per_cell.append({
            "label": lab,
            "raw_p": p,
            "rank": rank + 1,
            "threshold": threshold,
            "adjusted_p": adj_p,
            "rejected_at_holm": rejected,
        })
    if omitted:
        annotation = (f"Holm ({k}-of-{len(labels)} sens arms; "
                      f"{', '.join(omitted)} INCONCLUSIVE)")
    else:
        annotation = f"Holm ({k}-of-{len(labels)} sens arms; all valid)"
    return {
        "k": k, "omitted": omitted,
        "per_cell": per_cell,
        "annotation": annotation,
    }


# === Crash-drop divergence flag (section 4.10) ==========================

def crash_drop_flag_evaluation(primary: dict, crash_dropped: dict) -> dict:
    """Per section 4.10 + CONVENTIONS section 3.4: flag if
    |Delta Cliff's delta| > 0.10. Route primary verdict to REJECTED iff
    |Delta Cliff's delta| > 0.20 AND direction flips.
    """
    d_primary = primary["cliffs_delta"]
    d_dropped = crash_dropped["cliffs_delta"]
    if math.isnan(d_primary) or math.isnan(d_dropped):
        return {
            "delta_cliffs_delta": float("nan"),
            "delta_cliffs_delta_pp": float("nan"),
            "sign_flip": False,
            "flag_fired_010": False,
            "flag_fired_005pp": False,
            "route_to_rejected": False,
        }
    dd = d_dropped - d_primary
    dd_pp = dd * 100.0  # comparable scale to HA11-bout-redo's pp metric
    sign_flip = (d_primary > 0) != (d_dropped > 0)
    flag_010 = abs(dd) > CRASH_DROP_FLAG_DELTA_DELTA
    flag_005pp = abs(dd_pp) > CRASH_DROP_FLAG_DELTA_PP_PRIMARY
    route_reject = (abs(dd) > CRASH_DROP_FLAG_DELTA_DELTA_REJECT) and sign_flip
    return {
        "delta_cliffs_delta": dd,
        "delta_cliffs_delta_pp": dd_pp,
        "sign_flip": sign_flip,
        "flag_fired_010": flag_010,
        "flag_fired_005pp": flag_005pp,
        "route_to_rejected": route_reject,
    }


# === Cross-op concordance descriptive companion (section 4 audit) =======

def cross_op_concordance(master: dict[date, dict]) -> dict:
    """Descriptive companion per HA-C4cp §4.10 sister-test cross-reference +
    descriptive_audit.md §4: 2x2 concordance between HA-C4c parent operand
    (bout_n_did_not_return >= 1) and HA-C4cp primary operand
    (bout_n_did_not_return_2sd_day >= 1) on the primary stratum, plus
    Cohen's kappa and cap-unreachable-day count. NOT part of §5 verdict
    machinery.
    """
    baseline_lag = device_baseline_lag_set(master)
    n11 = n10 = n01 = n00 = 0
    cap_unreachable = 0
    n_total = 0
    for d, info in master.items():
        if not day_in_primary_stratum(d, master):
            continue
        if APRIL_2024_CLUSTER_START <= d <= APRIL_2024_CLUSTER_END:
            continue
        if d in baseline_lag:
            continue
        if not info["exertion_class_lagged_lcera"]:
            continue
        p_op = info.get(COL_PARENT_OP)
        sd_op = info.get(COL_PRIMARY)
        if p_op is None or sd_op is None:
            continue
        n_total += 1
        c4c_fires = p_op >= 1
        c4cp_fires = sd_op >= 1
        if c4c_fires and c4cp_fires:
            n11 += 1
        elif c4c_fires and not c4cp_fires:
            n10 += 1
        elif not c4c_fires and c4cp_fires:
            n01 += 1
        else:
            n00 += 1
        # Cap-unreachable: Z=2 threshold (median + 2*mad) > 180.
        med = info.get(COL_REF_MEDIAN)
        mad = info.get(COL_REF_MAD)
        if med is not None and mad is not None:
            if med + 2.0 * mad > 180.0:
                cap_unreachable += 1

    if n_total == 0:
        return {"n_total": 0, "kappa": float("nan"),
                "cap_unreachable_days": 0}

    p_o = (n11 + n00) / n_total
    marg_hac4c = (n11 + n10) / n_total
    marg_hac4cp = (n11 + n01) / n_total
    p_e = marg_hac4c * marg_hac4cp + (1 - marg_hac4c) * (1 - marg_hac4cp)
    kappa = (p_o - p_e) / (1 - p_e) if (1 - p_e) > 0 else float("nan")

    return {
        "n_total": n_total,
        "n_both_fire": n11,
        "n_hac4c_only": n10,
        "n_hac4cp_only": n01,
        "n_neither": n00,
        "frac_both_fire": n11 / n_total,
        "frac_hac4c_only": n10 / n_total,
        "frac_hac4cp_only": n01 / n_total,
        "frac_neither": n00 / n_total,
        "observed_agreement": p_o,
        "expected_agreement": p_e,
        "kappa": kappa,
        "cap_unreachable_days": cap_unreachable,
        "cap_unreachable_frac": cap_unreachable / n_total,
    }


# === Dry-run sanity gates (section 10.4) ================================

def dry_run_gates(master: dict[date, dict]) -> dict:
    """Per section 7 + section 10.4: gate the per-day distribution mean +
    median + walk-forward n per primary arm + parent-operand determinism.

    HALT bar: primary operand mean outside [0.01, 0.60] OR median > 2.
    Informational-only (not a HALT): mean inside [0.05, 0.30]; median in [0, 1].
    """
    print("\n=== DRY-RUN SANITY GATES (pre-reg section 10.4) ===\n",
          file=sys.stderr)

    # Pre-aggregate primary-arm pool
    dates, is_heavy, values, n_flagged = collect_arm_data(
        master, stratum_fn=day_in_primary_stratum,
        operand_col=COL_PRIMARY,
    )
    val_arr = np.asarray(values, dtype=float)
    heavy_mask = np.asarray(is_heavy, dtype=bool)
    n_heavy = int(heavy_mask.sum())
    n_non_heavy = int((~heavy_mask).sum())

    pool_mean = float(val_arr.mean()) if len(val_arr) > 0 else float("nan")
    pool_median = float(np.median(val_arr)) if len(val_arr) > 0 else float("nan")
    pool_std = float(val_arr.std(ddof=1)) if len(val_arr) > 1 else float("nan")

    # Gate 1: walk-forward n per arm (section 4.7)
    print("GATE 1 - walk-forward n per arm (section 4.7)", file=sys.stderr)
    print(f"  n_heavy:     {n_heavy}  (threshold >= {WF_GATE_N_HEAVY})",
          file=sys.stderr)
    print(f"  n_non_heavy: {n_non_heavy}  (threshold >= {WF_GATE_N_NON_HEAVY})",
          file=sys.stderr)
    gate1_pass = (n_heavy >= WF_GATE_N_HEAVY) and (n_non_heavy >= WF_GATE_N_NON_HEAVY)
    print(f"  result: {'PASS' if gate1_pass else 'FAIL -> INCONCLUSIVE per section 9.4'}\n",
          file=sys.stderr)

    # Gate 2: per-day mean HALT window [0.01, 0.60] (section 10.4)
    print("GATE 2 - per-day mean HALT window [0.01, 0.60] (section 10.4)",
          file=sys.stderr)
    print(f"  observed mean: {pool_mean:.4f}", file=sys.stderr)
    print(f"  HALT threshold (wider): [{SANITY_HALT_MEAN_MIN}, {SANITY_HALT_MEAN_MAX}]",
          file=sys.stderr)
    print(f"  informational anchor (narrower, non-HALT): [{SANITY_INFO_MEAN_MIN}, {SANITY_INFO_MEAN_MAX}]",
          file=sys.stderr)
    gate2_pass = (not math.isnan(pool_mean)) and (
        SANITY_HALT_MEAN_MIN <= pool_mean <= SANITY_HALT_MEAN_MAX)
    gate2_info_pass = (not math.isnan(pool_mean)) and (
        SANITY_INFO_MEAN_MIN <= pool_mean <= SANITY_INFO_MEAN_MAX)
    print(f"  HALT result: {'PASS' if gate2_pass else 'HALT per section 10.4'}",
          file=sys.stderr)
    print(f"  informational: {'INSIDE narrower anchor' if gate2_info_pass else 'OUTSIDE narrower anchor (informational only; not a HALT)'}\n",
          file=sys.stderr)

    # Gate 3: per-day median HALT rule (median > 2 -> HALT); informational bar [0, 1]
    print("GATE 3 - per-day median (section 10.4 HALT rule: median > 2)",
          file=sys.stderr)
    print(f"  observed median: {pool_median:.4f}", file=sys.stderr)
    print(f"  HALT threshold: median <= {SANITY_HALT_MEDIAN_MAX}",
          file=sys.stderr)
    print(f"  informational anchor: median in [0, {SANITY_INFO_MEDIAN_MAX}]",
          file=sys.stderr)
    gate3_pass = (not math.isnan(pool_median)) and (pool_median <= SANITY_HALT_MEDIAN_MAX)
    gate3_info_pass = (not math.isnan(pool_median)) and (0 <= pool_median <= SANITY_INFO_MEDIAN_MAX)
    print(f"  HALT result: {'PASS' if gate3_pass else 'HALT per section 10.4'}",
          file=sys.stderr)
    print(f"  informational: {'INSIDE [0, 1]' if gate3_info_pass else 'OUTSIDE [0, 1] (informational only; not a HALT)'}\n",
          file=sys.stderr)

    # Gate 4: parent-operand determinism check (byte-identical reproduction
    # on frozen 1274-day HA-C4c-vintage stratum; approximate reproduction
    # on current corpus per descriptive_audit.md section 1).
    parent_dates, parent_heavy, parent_values, _ = collect_arm_data(
        master, stratum_fn=day_in_primary_stratum,
        operand_col=COL_PARENT_OP,
    )
    parent_arr = np.asarray(parent_values, dtype=float)
    parent_mean = float(parent_arr.mean()) if len(parent_arr) > 0 else float("nan")
    print("GATE 4 - parent operand determinism check (section 10.4)",
          file=sys.stderr)
    print(f"  observed parent (`bout_n_did_not_return`) mean on primary stratum: {parent_mean:.4f}",
          file=sys.stderr)
    print(f"  targets: {PARENT_OP_TARGET_MEAN_HAC4C_VINTAGE} (frozen HA-C4c-vintage stratum) "
          f"OR ~{PARENT_OP_TARGET_MEAN_CURRENT_CORPUS} (current corpus per descriptive_audit.md section 1)",
          file=sys.stderr)
    gate4_pass = (not math.isnan(parent_mean)) and (
        abs(parent_mean - PARENT_OP_TARGET_MEAN_HAC4C_VINTAGE) <= PARENT_OP_TARGET_TOL
        or abs(parent_mean - PARENT_OP_TARGET_MEAN_CURRENT_CORPUS) <= PARENT_OP_TARGET_TOL
    )
    print(f"  result: {'PASS' if gate4_pass else 'FAIL (informational; determinism drift beyond tolerance)'}\n",
          file=sys.stderr)

    # AUX: first 3 heavy-T days summary
    print("AUX - first 3 heavy-T days (primary stratum)", file=sys.stderr)
    heavy_dates = [(d, v) for d, h, v in zip(dates, is_heavy, values) if h]
    for d, v in heavy_dates[:3]:
        print(f"  {d}: {COL_PRIMARY}={v:.0f}", file=sys.stderr)
    print("", file=sys.stderr)

    # Operand-presence + reference-window failure count
    primary_non_nan = sum(
        1 for d, info in master.items()
        if info.get(COL_PRIMARY) is not None
        and day_in_primary_stratum(d, master)
    )
    ref_fail_count = reference_window_failure_count(
        master, stratum_fn=day_in_primary_stratum)
    print(f"AUX - primary stratum non-NaN {COL_PRIMARY} days: {primary_non_nan}",
          file=sys.stderr)
    print(f"AUX - reference-window shortfall days on stratum "
          f"(gate 4 fires): {ref_fail_count}", file=sys.stderr)
    print("", file=sys.stderr)

    # HALT decision: HALT only on gate 2 (mean) or gate 3 (median) failure.
    # Gate 4 (determinism) is informational.
    halt = not (gate2_pass and gate3_pass)
    inconclusive_walk = not gate1_pass
    overall = (gate1_pass and gate2_pass and gate3_pass)

    if halt:
        status = "HALT (section 10.4 sanity gate failed)"
    elif inconclusive_walk:
        status = "INCONCLUSIVE (section 4.7 walk-forward gate failed; route to section 9.4)"
    else:
        status = "PASS"
    print(f"=== DRY-RUN OVERALL: {status} ===\n", file=sys.stderr)

    return {
        "gate1_wf_pass": gate1_pass,
        "gate2_mean_halt_pass": gate2_pass,
        "gate2_mean_info_pass": gate2_info_pass,
        "gate3_median_halt_pass": gate3_pass,
        "gate3_median_info_pass": gate3_info_pass,
        "gate4_parent_op_determinism_pass": gate4_pass,
        "n_heavy": n_heavy,
        "n_non_heavy": n_non_heavy,
        "pool_mean": pool_mean,
        "pool_median": pool_median,
        "pool_std": pool_std,
        "parent_op_mean_on_stratum": parent_mean,
        "primary_stratum_non_nan_days": primary_non_nan,
        "reference_window_failure_days": ref_fail_count,
        "n_flagged_bouts_in_pool": n_flagged,
        "halt": halt,
        "inconclusive_walk_forward": inconclusive_walk,
        "overall_pass": overall,
        "first_3_heavy_T_days": [
            {"date": str(d), COL_PRIMARY: v}
            for d, v in heavy_dates[:3]
        ],
    }


# === Result.md emission =================================================

def fmt_pct(x: float) -> str:
    if math.isnan(x):
        return "NaN"
    return f"{x*100:.1f}%"


def fmt_p(x: float) -> str:
    if math.isnan(x):
        return "NaN"
    return f"{x:.4f}"


def fmt_delta(x: float) -> str:
    if math.isnan(x):
        return "NaN"
    return f"{x:+.3f}"


def fmt_pass_fail(b) -> str:
    if b is None:
        return "n/a"
    return "PASS" if b else "FAIL"


def write_result_md(
    primary: dict,
    sens_arms: dict[str, dict],
    crash_dropped: dict,
    crash_drop_flag: dict,
    approach_a_arms: dict[str, dict],
    holm: dict,
    gate_outcomes: dict,
    concordance: dict,
    worktree_head: str,
) -> None:
    """Emit the section 10.3 result.md, mirroring HA-C4c/result.md structure."""

    headline_verdict = primary["verdict"]
    cliff_top = primary["cliffs_delta"]
    p_top = primary["block_perm_p_value"]

    bar_a = primary["bar_a_disc_p_lt_0_05"]
    bar_b = primary["bar_b_cliffs_delta_geq_0_20"]
    dir_ok = primary["direction_correct"]

    bar_str = (f"direction={'+' if dir_ok else '-' if dir_ok is False else 'n/a'}, "
               f"(a) p<0.05={fmt_pass_fail(bar_a)} (p={fmt_p(p_top)}), "
               f"(b) delta>=+0.20={fmt_pass_fail(bar_b)} (delta={fmt_delta(cliff_top)})")

    # Sister-test verdicts (descriptive only per pre-reg section 4.10)
    SISTER_TESTS = [
        ("HA-C4c r2",                       "PARTIAL magnitude-below-threshold",
         "cross-phase-pooled bout-level; delta=+0.1523, p=0.0091, n=1274; fixed-absolute-threshold sister"),
        ("HA-C4c-stringency-companion",     "NON-TRIGGER (Pass 1)",
         "f2(T) monotone descent 0.5863 -> 0.1020 across T in {30,60,120,180}; OI-025 CLOSED-DESCRIPTIVE-ONLY"),
        ("HA-C4 v2",                        "REJECTED",
         "daily-aggregate triad sum 0.0/3.0"),
        ("HA-C4b v3",                       "NOT-SUPPORTED",
         "motion-filter crash-precursor"),
        ("HA11 v1",                         "SUPPORTED-on-train",
         "U-dip count +22.8 pp"),
        ("HA11-bout-redo",                  "PARTIAL",
         "framework-validity 2-of-3 bars met; bar 3 p=0.2609 at n_calm=70/n_crash=11"),
    ]

    lines: list[str] = []

    # === Section 1: headline verdict + cascade context =================
    lines.append(f"# {HA_ID} - RESULT: {headline_verdict}")
    lines.append("")
    lines.append(f"Emitted by `test.py` per LOCKED r2 hypothesis.md section 10.3. "
                 "**Headline cell**: cross-phase-pooled stratum (per HA-C4c section 4.2 verbatim) x "
                 f"`{COL_PRIMARY}` x heavy-T-vs-non-heavy-T x Mann-Whitney U + Cliff's delta + "
                 f"block-permutation null at E[L]=7. **Seed**: `RANDOM_SEED = {RANDOM_SEED}`; "
                 f"**B** = {B_HEADLINE}. **Operand direction**: heavy-T > non-heavy-T "
                 "(one-sided elevated). **Reference-frame**: personal-baseline-rolling "
                 "(SD-anchored) per parent MD section 3.2.2; cross-operationalisation-"
                 "independent from HA-C4c's fixed-absolute-threshold reference-frame at "
                 "operand-family level per OI-025 protocol section 5.4 four-condition argument.")
    lines.append("")
    lines.append("## Authorship")
    lines.append("")
    lines.append("- **Drafting date**: 2026-07-14 (this result.md emitted in the post-lock test-execution session).")
    lines.append("- **Agent**: Claude (Opus 4.7) in producer-mode under user authorisation per "
                 "[CONVENTIONS section 1.1](../../../CONVENTIONS.md). Authorising user: Willem.")
    lines.append(f"- **Pre-reg commit**: r2 LOCKED 2026-07-09 at [`hypothesis.md`](hypothesis.md). "
                 f"Worktree HEAD at run: `{worktree_head}`.")
    lines.append("- **Test commit**: this session's `test.py` commit (set by dispatcher after cherry-pick).")
    lines.append(f"- **Pipeline commit**: pipeline extension for parent MD section 3.2.2 columns "
                 f"LOCKED at Bundle H+ event 8 `{PIPELINE_COMMIT}` (2026-07-14 corpus snapshot).")
    lines.append("- **Status**: LANDED. Test executed end-to-end; dry-run section 10.4 gates passed; "
                 "primary headline emitted; sensitivity arms reported; cascade implication recorded in section 11.")
    lines.append("")

    # === Section 1 body: headline verdict + cascade calibration ========
    lines.append("## Section 1 - Headline verdict + cascade context")
    lines.append("")
    lines.append(f"**Verdict: {headline_verdict}** -- {bar_str}.")
    lines.append("")
    lines.append("**HA-C4c r2 PARTIAL magnitude-below-threshold calibration context (per pre-reg section 8 "
                 "caveat 2)**: HA-C4c's landed Cliff's delta = +0.1523 missed the +0.20 bar by -0.05 with "
                 "empirical p = 0.0091 (bar (a) cleared). HA-C4cp's operand-family compression argument "
                 "(personal-baseline z-scoring against a rolling reference typically compresses "
                 "cross-day effect sizes relative to fixed-threshold operands per CONVENTIONS section 3.1) "
                 "predicts plausibly comparable or lower delta on HA-C4cp. PARTIAL is anticipated as the "
                 "modal outcome; SUPPORTED requires the personal-baseline operationalisation to produce a "
                 "strictly larger delta than the fixed-absolute-threshold arm. Read this verdict against "
                 "that anticipation.")
    lines.append("")
    if headline_verdict == "SUPPORTED":
        lines.append("**Cross-test cascade implication (section 9.1 SUPPORTED branch)**: the personal-baseline "
                     "SD-anchored operand `bout_n_did_not_return_2sd_day` shows systematically higher counts on "
                     "heavy-T days than on non-heavy-T days at the cross-phase-pooled stratum, with both (a) "
                     "discrimination + (b) effect-size bars clearing in the predicted positive direction. Under "
                     "the joint-cluster reading at cluster-C-bout-substance section 5 Layer 3, HA-C4c PARTIAL + "
                     "HA-C4cp SUPPORTED reads as PARTIALLY CONCORDANT with strength-asymmetry-on-personal-baseline "
                     "-- the personal-baseline operationalisation reaches the SUPPORTED threshold that the "
                     "fixed-absolute-threshold arm missed. OI-033 CLOSED-BY-EXECUTION-SUPPORTED; the "
                     "cross-op-independence gap closes at strict guide section 4.2 two-independent-HAs bar.")
    elif headline_verdict == "PARTIAL":
        if bar_a is False:
            lines.append("**Cross-test cascade implication (section 9.2 PARTIAL branch; bar (a)-failing "
                         "configuration)**: direction-correct AND (b) Cliff's delta >= +0.20 AND (a) "
                         "block-perm p >= 0.05. Substantive magnitude reproduces the predicted shape but "
                         "block-permutation null cannot statistically distinguish it. Under joint-cluster "
                         "reading, HA-C4c PARTIAL + HA-C4cp PARTIAL(bar-a-fail) reads as CONCORDANT-BELOW-"
                         "THRESHOLD at bar (a); a corpus-power-bound finding on the block-perm p bar.")
        else:
            lines.append("**Cross-test cascade implication (section 9.2 PARTIAL branch; bar (b)-failing "
                         "configuration)**: direction-correct AND (a) block-perm p < 0.05 AND (b) Cliff's "
                         "delta < +0.20. This EXACTLY MIRRORS HA-C4c's PARTIAL(bar-b-fail) pattern -- the "
                         "operand-family compression argument's modal outcome. Under joint-cluster reading, "
                         "HA-C4c PARTIAL + HA-C4cp PARTIAL(bar-b-fail) reads as CONCORDANT-BELOW-THRESHOLD -- "
                         "both cells direction-correct, both PARTIAL, corpus effect-size ceiling reading per "
                         "pre-reg section 9.2. This is a honest sample-limitation reading, NOT a Wiggers-C4 "
                         "disproof. OI-033 CLOSED-BY-EXECUTION-PARTIAL; cross-op-independence gap CLOSED at "
                         "direction-consistent-below-threshold reading.")
    elif headline_verdict == "REJECTED":
        lines.append("**Cross-test cascade implication (section 9.3 REJECTED branch)**: direction-wrong OR "
                     "both bars fail OR section 4.10 crash-drop sign-flip. Under joint-cluster reading, "
                     "HA-C4c PARTIAL + HA-C4cp REJECTED reads as ORTHOGONAL (if direction-wrong-on-HA-C4cp "
                     "with HA-C4c direction-correct) or as a substantive **operand-family-specific finding**: "
                     "the signal is anchored to the fixed-absolute-threshold reference frame; the "
                     "personal-baseline-rolling operationalisation does not fire. OI-033 CLOSED-BY-EXECUTION-"
                     "REJECTED; register-row updates parallel to section 9.1 but marks HA-C4cp REJECTED as "
                     "sister-test outcome.")
    else:  # INCONCLUSIVE
        lines.append("**Cross-test cascade implication (section 9.4 INCONCLUSIVE branch)**: section 4.7 "
                     "walk-forward gate not met OR section 10.4 dry-run sanity gates failed. HA-C4cp-v2 "
                     "reframe with different reference-window or Z-threshold per section 9.5 escalation table.")
    lines.append("")

    # === Section 2: Per-bar table =====================================
    lines.append("## Section 2 - Per-bar table")
    lines.append("")
    lines.append("| bar | target | observed | result |")
    lines.append("|---|---|---:|:---:|")
    lines.append(f"| direction | heavy-T > non-heavy-T (Cliff's delta > 0) | "
                 f"delta = {fmt_delta(cliff_top)} | "
                 f"{fmt_pass_fail(dir_ok)} |")
    lines.append(f"| **Bar (a) - discrimination** | block-perm p < {BAR_A_P_VALUE} | "
                 f"p = {fmt_p(p_top)} | {fmt_pass_fail(bar_a)} |")
    lines.append(f"| **Bar (b) - effect size** | Cliff's delta >= +{BAR_B_CLIFFS_DELTA} | "
                 f"delta = {fmt_delta(cliff_top)} | {fmt_pass_fail(bar_b)} |")
    lines.append("")

    # === Section 3: Per-arm summary table ============================
    lines.append("## Section 3 - Per-arm summary table (primary cell)")
    lines.append("")
    lines.append("| metric | heavy-T arm | non-heavy-T arm |")
    lines.append("|---|---:|---:|")
    lines.append(f"| n_days | {primary['n_heavy']} | {primary['n_non_heavy']} |")
    lines.append(f"| mean `{COL_PRIMARY}` | {primary['heavy_mean']:.3f} | "
                 f"{primary['non_heavy_mean']:.3f} |")
    lines.append(f"| median `{COL_PRIMARY}` | {primary['heavy_median']:.2f} | "
                 f"{primary['non_heavy_median']:.2f} |")
    lines.append(f"| Mann-Whitney U (heavy first) | {primary['mannwhitney_u']:.0f} | -- |")
    lines.append(f"| Mann-Whitney p (one-sided normal approx, descriptive) | "
                 f"{fmt_p(primary['mannwhitney_p_normal_one_sided'])} | -- |")
    lines.append(f"| Cliff's delta (heavy vs non-heavy) | {fmt_delta(primary['cliffs_delta'])} | -- |")
    lines.append(f"| Cliff's delta 95% CI (paired-bootstrap B={N_BOOTSTRAP_CLIFFS_CI}) | "
                 f"[{fmt_delta(primary['cliffs_delta_ci95_lo'])}, "
                 f"{fmt_delta(primary['cliffs_delta_ci95_hi'])}] | -- |")
    lines.append(f"| block-permutation p (E[L]=7, B={B_HEADLINE}, seed `{RANDOM_SEED}`) | "
                 f"{fmt_p(primary['block_perm_p_value'])} | -- |")
    lines.append(f"| block-perm null delta median | {fmt_delta(primary['block_perm_null_delta_median'])} | -- |")
    lines.append(f"| block-perm null delta 95% CI | "
                 f"[{fmt_delta(primary['block_perm_null_delta_p025'])}, "
                 f"{fmt_delta(primary['block_perm_null_delta_p975'])}] | -- |")
    lines.append(f"| n_flagged_bouts (sum across days) | "
                 f"{primary['n_flagged_bouts']} | -- |")
    lines.append("")

    # === Section 4: Companion descriptives + sanity ===================
    lines.append("## Section 4 - Companion descriptives (per-day distribution + section 10.4 sanity)")
    lines.append("")
    lines.append("| metric | observed | section 10.4 HALT window | HALT status | info anchor | info status |")
    lines.append("|---|---:|---|:---:|---|:---:|")
    pm = primary["pool_mean"]; psd = primary["pool_std"]; pmd = primary["pool_median"]
    halt_mean_ok = SANITY_HALT_MEAN_MIN <= pm <= SANITY_HALT_MEAN_MAX
    info_mean_ok = SANITY_INFO_MEAN_MIN <= pm <= SANITY_INFO_MEAN_MAX
    halt_med_ok = pmd <= SANITY_HALT_MEDIAN_MAX
    info_med_ok = 0 <= pmd <= SANITY_INFO_MEDIAN_MAX
    lines.append(f"| per-day mean | {pm:.4f} | [{SANITY_HALT_MEAN_MIN}, {SANITY_HALT_MEAN_MAX}] | "
                 f"{'PASS' if halt_mean_ok else 'HALT'} | [{SANITY_INFO_MEAN_MIN}, {SANITY_INFO_MEAN_MAX}] | "
                 f"{'INSIDE' if info_mean_ok else 'OUTSIDE'} |")
    lines.append(f"| per-day median | {pmd:.2f} | <= {SANITY_HALT_MEDIAN_MAX} | "
                 f"{'PASS' if halt_med_ok else 'HALT'} | in [0, {SANITY_INFO_MEDIAN_MAX}] | "
                 f"{'INSIDE' if info_med_ok else 'OUTSIDE'} |")
    lines.append(f"| per-day sigma | {psd:.4f} | -- | -- | -- | -- |")
    lines.append(f"| per-day p25-p75 | [{primary['pool_p25']:.2f}, {primary['pool_p75']:.2f}] | -- | -- | -- | -- |")
    lines.append(f"| per-day range | [{primary['pool_min']:.2f}, {primary['pool_max']:.2f}] | -- | -- | -- | -- |")
    lines.append("")
    if primary["el_companion"]:
        el = primary["el_companion"]
        flag_status = "FLAGGED" if el["flagged_deviation"] else "NOT FLAGGED"
        lines.append(f"**E[L]\\* data-driven companion** (CONVENTIONS section 3.6 + parent MD section 5.1): "
                     f"E[L]\\* = {el['optimal_block_length']:.2f} days (cutoff_lag={el['cutoff_lag']}); "
                     f"factor-of-2 deviation flag: {flag_status}. Per pre-reg section 4.6 + CONVENTIONS "
                     f"section 3.6: factor-of-2 flag is descriptive context only; does NOT modify the "
                     f"section 5 verdict.")
        lines.append("")

    # === Section 4b: Reference-window audit trace (section 4.11) =======
    lines.append("### Reference-window audit trace (per section 4.11 mandatory reporting)")
    lines.append("")
    lines.append("Per parent MD section 3.2.2 mandatory-audit-trace discipline + pre-reg section 4.11.")
    lines.append("")
    ref = primary["reference_window_audit"]
    lines.append("| stat | heavy-T lagged_median (min) | heavy-T lagged_mad (min) | non-heavy-T lagged_median (min) | non-heavy-T lagged_mad (min) |")
    lines.append("|---|---:|---:|---:|---:|")
    hm, hmad = ref["heavy_lagged_median"], ref["heavy_lagged_mad"]
    nhm, nhmad = ref["non_heavy_lagged_median"], ref["non_heavy_lagged_mad"]
    lines.append(f"| n | {hm['n']} | {hmad['n']} | {nhm['n']} | {nhmad['n']} |")
    lines.append(f"| mean | {hm['mean']:.2f} | {hmad['mean']:.2f} | {nhm['mean']:.2f} | {nhmad['mean']:.2f} |")
    lines.append(f"| median | {hm['median']:.2f} | {hmad['median']:.2f} | {nhm['median']:.2f} | {nhmad['median']:.2f} |")
    lines.append(f"| p25 | {hm['p25']:.2f} | {hmad['p25']:.2f} | {nhm['p25']:.2f} | {nhmad['p25']:.2f} |")
    lines.append(f"| p75 | {hm['p75']:.2f} | {hmad['p75']:.2f} | {nhm['p75']:.2f} | {nhmad['p75']:.2f} |")
    lines.append("")
    lines.append(f"**Reference-window shortfall days on primary stratum**: "
                 f"{gate_outcomes['reference_window_failure_days']} days routed to NaN via section 4.4 gate 4 "
                 "(reference pool < 30 bouts in [d-90, d-30]). Per descriptive_audit.md LOCKED r1 section 6: "
                 "expected 0 on primary stratum (the sub-phase-4b left-edge >= 2022-11-17 is more restrictive "
                 "than the reference-window warmup trim).")
    lines.append("")

    # === Section 4c: Cross-op concordance descriptive companion ========
    lines.append("### Cross-op concordance descriptive companion (per section 4.10 sister-test cross-reference)")
    lines.append("")
    lines.append("2x2 concordance table between HA-C4c parent operand (`bout_n_did_not_return >= 1`) and "
                 "HA-C4cp primary operand (`bout_n_did_not_return_2sd_day >= 1`) on the primary stratum. "
                 "**Descriptive-only per Pass 1 discipline**; NOT part of the section 5 verdict machinery.")
    lines.append("")
    n_c = concordance["n_total"]
    n_bo = concordance["n_both_fire"]
    n_c4c = concordance["n_hac4c_only"]
    n_c4cp = concordance["n_hac4cp_only"]
    n_ne = concordance["n_neither"]
    lines.append("|  | HA-C4c fires | HA-C4c does NOT fire | total |")
    lines.append("|---|---:|---:|---:|")
    lines.append(f"| **HA-C4cp fires** | {n_bo} ({concordance['frac_both_fire']*100:.1f}%) | "
                 f"{n_c4cp} ({concordance['frac_hac4cp_only']*100:.1f}%) | "
                 f"{n_bo + n_c4cp} |")
    lines.append(f"| **HA-C4cp does NOT fire** | {n_c4c} ({concordance['frac_hac4c_only']*100:.1f}%) | "
                 f"{n_ne} ({concordance['frac_neither']*100:.1f}%) | "
                 f"{n_c4c + n_ne} |")
    lines.append(f"| **total** | {n_bo + n_c4c} | {n_c4cp + n_ne} | {n_c} |")
    lines.append("")
    lines.append(f"**Cohen's kappa** (chance-corrected agreement; descriptive companion): "
                 f"observed agreement = {concordance['observed_agreement']:.4f}, "
                 f"expected agreement = {concordance['expected_agreement']:.4f}, "
                 f"**kappa = {concordance['kappa']:.3f}**. "
                 "Per Landis-Koch 1977 cutoffs: 0.41-0.60 = moderate; 0.61-0.80 = substantial. "
                 f"**Cap-unreachable days**: {concordance['cap_unreachable_days']} of {n_c} "
                 f"({concordance['cap_unreachable_frac']*100:.1f}%) have Z=2 threshold > 180-min "
                 "`tail_length` cap by construction (SD-anchored operand cannot fire on those days "
                 "regardless of bout activity).")
    lines.append("")

    # === Section 5: Sensitivity arms ===================================
    lines.append("## Section 5 - Sensitivity arms (per section 4.10; descriptive; cannot promote to SUPPORTED)")
    lines.append("")
    lines.append("| arm | operand | n_heavy | n_non_heavy | heavy mean | non-heavy mean | Cliff's delta | block-perm p | (a) | (b) | verdict | fragility vs primary |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|:---:|:---:|:---:|---|")
    lines.append(f"| **primary** (cross-phase-pooled) | `{COL_PRIMARY}` | {primary['n_heavy']} | {primary['n_non_heavy']} | "
                 f"{primary['heavy_mean']:.3f} | {primary['non_heavy_mean']:.3f} | "
                 f"{fmt_delta(primary['cliffs_delta'])} | {fmt_p(primary['block_perm_p_value'])} | "
                 f"{fmt_pass_fail(bar_a)} | {fmt_pass_fail(bar_b)} | **{primary['verdict']}** | -- |")
    sens_display_order = [
        ("z1_count",                       "Z=1 sensitivity",                    COL_Z1),
        ("z_max_continuous",               "z_max continuous sensitivity",       COL_ZMAX),
        ("reference_window_shorter_lag",   "reference-window [d-60, d-30]",      COL_PRIMARY),
        ("unmedicated_only",               "unmedicated-only stratum",           COL_PRIMARY),
        ("motion_clean_only",              "motion-clean-only (motion_confound_flag=False)", COL_PRIMARY),
        ("transient_excluded",             "transient-excluded (transient_flag=False)",      COL_PRIMARY),
        ("baseline_invalid_excluded",      "baseline-invalid-excluded (baseline_invalid_flag=False)", COL_PRIMARY),
        ("reference_pool_dnr_excluded",    "reference-pool did_not_return-excluded",         COL_PRIMARY),
    ]
    for arm_name, key_label, op_col in sens_display_order:
        a = sens_arms.get(arm_name)
        if a is None:
            continue
        fragility = "consistent" if a["verdict"] == primary["verdict"] else "flagged"
        lines.append(f"| {key_label} | `{op_col}` | {a['n_heavy']} | {a['n_non_heavy']} | "
                     f"{a['heavy_mean']:.3f} | {a['non_heavy_mean']:.3f} | "
                     f"{fmt_delta(a['cliffs_delta'])} | {fmt_p(a['block_perm_p_value'])} | "
                     f"{fmt_pass_fail(a['bar_a_disc_p_lt_0_05'])} | "
                     f"{fmt_pass_fail(a['bar_b_cliffs_delta_geq_0_20'])} | "
                     f"{a['verdict']} | {fragility} |")
    lines.append("")

    # Motion-clean degeneracy disclosure
    mc = sens_arms.get("motion_clean_only")
    if mc and mc["verdict"] == "INCONCLUSIVE":
        lines.append("**Motion-clean-only arm degeneracy (anticipated per pre-reg section 8 caveat 4)**: per "
                     "HA11-bout-redo result section 4, 4285/4317 bouts (99.3%) carry `motion_confound_flag=True` "
                     "on this corpus + extraction threshold. Filtering produces a near-zero-variance per-day "
                     "count series and often falls below the section 4.7 walk-forward gate -> INCONCLUSIVE. "
                     "This is a per-bout data property, NOT a test bug. Per pre-reg section 9.5 sensitivity-arm "
                     "divergence rule: motion-fragility flag fired by virtue of arm INCONCLUSIVE vs primary "
                     f"{primary['verdict']}.")
        lines.append("")

    # Crash-drop sensitivity
    lines.append("### Crash-drop sensitivity (CONVENTIONS section 3.4 + pre-reg section 4.10)")
    lines.append("")
    lines.append("| metric | primary | crash-dropped | delta |")
    lines.append("|---|---:|---:|---:|")
    lines.append(f"| n_heavy | {primary['n_heavy']} | {crash_dropped['n_heavy']} | "
                 f"{crash_dropped['n_heavy']-primary['n_heavy']:+d} |")
    lines.append(f"| n_non_heavy | {primary['n_non_heavy']} | {crash_dropped['n_non_heavy']} | "
                 f"{crash_dropped['n_non_heavy']-primary['n_non_heavy']:+d} |")
    lines.append(f"| Cliff's delta | {fmt_delta(primary['cliffs_delta'])} | "
                 f"{fmt_delta(crash_dropped['cliffs_delta'])} | "
                 f"{fmt_delta(crash_drop_flag['delta_cliffs_delta'])} |")
    lines.append(f"| block-perm p | {fmt_p(primary['block_perm_p_value'])} | "
                 f"{fmt_p(crash_dropped['block_perm_p_value'])} | "
                 f"{fmt_p(crash_dropped['block_perm_p_value']-primary['block_perm_p_value'])} |")
    lines.append(f"| verdict | {primary['verdict']} | {crash_dropped['verdict']} | "
                 f"{'unchanged' if crash_dropped['verdict'] == primary['verdict'] else 'changed'} |")
    lines.append("")
    flag_010 = crash_drop_flag["flag_fired_010"]
    flag_005pp = crash_drop_flag["flag_fired_005pp"]
    route_reject = crash_drop_flag["route_to_rejected"]
    lines.append(f"**|Delta Cliff's delta| = {abs(crash_drop_flag['delta_cliffs_delta']):.3f}** (threshold "
                 f"{CRASH_DROP_FLAG_DELTA_DELTA} per CONVENTIONS section 3.4 + HA-C4c pattern): "
                 f"{'FIRED (signal is crash-driven; see flagged status)' if flag_010 else 'NOT FIRED (clean)'}. "
                 f"**|Delta Cliff's delta * 100| = {abs(crash_drop_flag['delta_cliffs_delta_pp']):.2f} pp** "
                 f"(threshold {CRASH_DROP_FLAG_DELTA_PP_PRIMARY} pp per HA11-bout-redo analogue): "
                 f"{'FIRED' if flag_005pp else 'NOT FIRED'}. **Route to REJECTED** "
                 f"(|delta delta| > {CRASH_DROP_FLAG_DELTA_DELTA_REJECT} AND sign-flip): "
                 f"{'YES -> primary verdict routes to REJECTED per section 5.2' if route_reject else 'NO'}.")
    lines.append("")

    # Approach A sensitivity arms (section 4.9)
    lines.append("### Approach A dose-adjusted sensitivity arm (section 4.9 inheritance-by-analogue; descriptive companion only)")
    lines.append("")
    lines.append("Per pre-reg section 4.9 underpowered-NULL framing + section 8 caveat 3: the Approach A "
                 "inheritance is **inheritance-by-analogue** from `bout_n_fast_recovery_day` buildup-post-CPAP "
                 "beta = -0.056/mg [CI -0.145, +0.034] (sign-flipped to +0.056/mg for HA-C4cp's +1 prior "
                 "direction). The source beta is NULL/weakly-consistent (CI crosses zero; p=0.223 in the source "
                 "recalibration). This is a **descriptive companion** under the underpowered-NULL frame; NOT a "
                 "load-bearing dose-correction. The CI-bracket sub-arm characterises **inheritance fragility**, "
                 "amplified per section 4.9 last paragraph because the SD-anchored operand family is FURTHER "
                 "removed from the analogue's operand family than HA-C4c's fixed-absolute-threshold operand.")
    lines.append("")
    lines.append("| sub-arm | beta/mg | Cliff's delta | block-perm p | (a) | (b) | verdict | divergence from primary |")
    lines.append("|---|---:|---:|---:|:---:|:---:|:---:|---|")
    for name, beta in [
        ("Approach A primary template",  APPROACH_A_BETA_PRIMARY),
        ("CI lower bracket (NULL)",      APPROACH_A_BETA_CI_LOWER),
        ("CI upper bracket (NULL)",      APPROACH_A_BETA_CI_UPPER),
    ]:
        a = approach_a_arms.get(name)
        if a is None:
            continue
        diverge = "consistent" if a["verdict"] == primary["verdict"] else "DIVERGENT"
        lines.append(f"| {name} | {beta:+.3f} | {fmt_delta(a['cliffs_delta'])} | "
                     f"{fmt_p(a['block_perm_p_value'])} | "
                     f"{fmt_pass_fail(a['bar_a_disc_p_lt_0_05'])} | "
                     f"{fmt_pass_fail(a['bar_b_cliffs_delta_geq_0_20'])} | "
                     f"{a['verdict']} | {diverge} |")
    lines.append("")

    # === Section 6: Holm step-down =====================================
    lines.append("## Section 6 - Holm step-down (section 5.3; secondary fragility-flag report)")
    lines.append("")
    lines.append(f"**{holm['annotation']}** at alpha={HOLM_ALPHA}.")
    lines.append("")
    if holm["omitted"]:
        k_val = holm["k"]
        cutoffs_str = ", ".join("alpha/" + str(k_val - i) for i in range(k_val))
        omitted_str = ", ".join(holm["omitted"])
        lines.append(f"**Fewer-comparisons disclosure** (per pre-reg section 5.3): Holm family collapsed "
                     f"from 7 cells to {k_val} because the following arms returned INCONCLUSIVE: "
                     f"{omitted_str}. Cutoffs adjusted accordingly: {cutoffs_str}.")
        lines.append("")
    lines.append("| cell | rank | raw p | threshold | adjusted p | Holm-rejected |")
    lines.append("|---|---:|---:|---:|---:|:---:|")
    for cell in holm["per_cell"]:
        lines.append(f"| {cell['label']} | {cell['rank']} | {fmt_p(cell['raw_p'])} | "
                     f"{cell['threshold']:.5f} | {fmt_p(cell['adjusted_p'])} | "
                     f"{'YES' if cell['rejected_at_holm'] else 'NO'} |")
    lines.append("")
    lines.append("**Family-membership caveat (LOAD-BEARING per pre-reg section 5.3 + section 8 caveat 6)**: "
                 "the Z=1 (`z1_count`) and z_max (`z_max_continuous`) sensitivity arms share the parent MD "
                 "section 3.2.2 reference-window construction with the primary -- same [d-90, d-30] window, "
                 "same reference pool, same `subject_lagged_median` + `subject_lagged_mad` scaling. They are "
                 "NOT fully independent tests; a shared-reference-window construction bias would propagate "
                 "to all three cells. A 'Holm passes on primary AND z1_count AND z_max_continuous' reading "
                 "must NOT be interpreted as independent confirmation of the primary signal; it is instead "
                 "consistent-reference-window internal-consistency. The `reference_window_shorter_lag` arm "
                 "is the FIRST INDEPENDENT diagnostic (different window definition); the "
                 "`reference_pool_dnr_excluded` arm at section 4.10 (not in the Holm family) is the SECOND "
                 "(different pool composition).")
    lines.append("")
    lines.append("Per pre-reg section 5.3: Holm is a secondary fragility-flag report. The primary verdict "
                 "per section 5.2 is the uncorrected primary cell; Holm cannot override.")
    lines.append("")

    # === Section 7: Sister-test cross-reference ========================
    lines.append("## Section 7 - Sister-test cross-reference table")
    lines.append("")
    lines.append("Per pre-reg section 4.10 + CONVENTIONS section 4.4: descriptive only; NO cross-test "
                 "pass conclusion at result-emission time. Cross-test interpretation lives in "
                 "[cluster-C-bout-substance.md](../../synthesis/cluster-C-bout-substance.md) per Stage S1 "
                 "internal-synthesis routing.")
    lines.append("")
    lines.append("| hypothesis | verdict | one-line note |")
    lines.append("|---|---|---|")
    for h, v, note in SISTER_TESTS:
        lines.append(f"| {h} | {v} | {note} |")
    lines.append(f"| **{HA_ID} (this test)** | **{headline_verdict}** | "
                 f"cross-phase-pooled bout-level personal-baseline SD-anchored; delta={fmt_delta(cliff_top)}, "
                 f"p={fmt_p(p_top)}, n_heavy={primary['n_heavy']}, "
                 f"n_non_heavy={primary['n_non_heavy']} |")
    lines.append("")

    # === Section 8: Pipeline-trust block ===============================
    lines.append("## Section 8 - Pipeline-trust block")
    lines.append("")
    lines.append(f"Bout-extraction pipeline + SD-anchored derivative operand family extension LOCKED at "
                 f"Bundle H+ event 8 commit `{PIPELINE_COMMIT}` (2026-07-14). The pipeline's inline smoke "
                 "tests provide audit coverage; parent MD section 3.2.2 defines the reference-window "
                 "construction the pipeline implements.")
    lines.append("")
    lines.append(f"- COL `{COL_PRIMARY}`: HA-C4cp primary; `0` on valid days with no flagged bouts, "
                 "NaN on reference-window-invalid days. Zero-vs-NaN discipline load-bearing per "
                 "DATA_DICTIONARY section 8E; test.py NEVER `.fillna(0)` this column.")
    lines.append(f"- COL `{COL_Z1}`: Z=1 sensitivity; same zero-vs-NaN discipline.")
    lines.append(f"- COL `{COL_ZMAX}`: z_max continuous sensitivity; NaN on 0-bout days OR "
                 "reference-window-invalid days per parent MD section 3.2.2.")
    lines.append(f"- COL `{COL_REF_MEDIAN}` / `{COL_REF_MAD}`: reference-window audit trace "
                 "(median + 1.4826*MAD of per-bout `tail_length` over [d-90, d-30] LC-era lagged pool).")
    lines.append("")

    # === Section 9: Verification log ====================================
    lines.append("## Section 9 - Verification log")
    lines.append("")
    lines.append("Anchors the test on the cascade state at run-time:")
    lines.append("")
    lines.append(f"- Pre-reg `hypothesis.md` r2 LOCKED 2026-07-09.")
    lines.append(f"- Worktree HEAD at test-time: `{worktree_head}`.")
    lines.append(f"- Pipeline (SD-anchored extension) commit: `{PIPELINE_COMMIT}` (Bundle H+ event 8, 2026-07-14).")
    lines.append("- Parent MD (`bout_level_recovery_dynamics.md`) LOCKED r3 2026-07-09 (section 3.2.2 SD-anchored family).")
    lines.append("- Sister pre-reg (fixed-absolute-threshold arm): HA-C4c r2 LOCKED 2026-07-08 landed PARTIAL.")
    lines.append("- HA-C4c-stringency-companion Pass 1 NON-TRIGGER 2026-07-09 (OI-025 CLOSED-DESCRIPTIVE-ONLY).")
    lines.append("- Stage D descriptive audit (`analyses/descriptive/HA-C4cp/descriptive_audit.md`) LOCKED r1 "
                 "2026-07-14; sanity + walk-forward gates PASS at descriptive-layer.")
    lines.append(f"- Dry-run gates per section 10.4: overall {'PASS' if gate_outcomes['overall_pass'] else ('HALT' if gate_outcomes['halt'] else 'INCONCLUSIVE-walk-forward')} at run-time "
                 f"(walk-forward n_heavy={gate_outcomes['n_heavy']}, "
                 f"n_non_heavy={gate_outcomes['n_non_heavy']}; "
                 f"per-day mean={gate_outcomes['pool_mean']:.4f}; "
                 f"median={gate_outcomes['pool_median']:.2f}; "
                 f"parent-op determinism check mean={gate_outcomes['parent_op_mean_on_stratum']:.4f}).")
    lines.append(f"- Per-day master CSV: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` (column "
                 f"`{COL_PRIMARY}`); primary stratum non-NaN days: "
                 f"{gate_outcomes['primary_stratum_non_nan_days']}; reference-window shortfall days: "
                 f"{gate_outcomes['reference_window_failure_days']}.")
    lines.append(f"- Per-bout master CSV: `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.csv` "
                 "(used for section 4.10 sensitivity-arm re-aggregation including reference-window-shorter-lag "
                 "and reference-pool-did_not_return-excluded arms).")
    lines.append("")

    # === Section 10: Caveats ============================================
    lines.append("## Section 10 - Caveats (per pre-reg section 8; all 8 prominently surfaced)")
    lines.append("")
    lines.append("1. **Personal-baseline reference-window carries a subject-relative interpretation**: the "
                 "SD-anchored operand does NOT test 'how long is the bout return-time in absolute minutes' "
                 "but 'how much longer than the subject's own recent typical return-time is this bout'. A "
                 "REJECTED verdict on HA-C4cp with HA-C4c at PARTIAL reads as 'the signal is anchored to "
                 "the fixed-absolute-threshold reference frame only'. A SUPPORTED verdict reads as 'the "
                 "signal generalises across both operand families'.")
    lines.append("")
    lines.append("2. **HA-C4c PARTIAL calibration discount**: HA-C4c's landed delta = +0.1523 misses the "
                 "+0.20 bar by -0.05. Operand-family compression predicts a plausibly-similar or lower "
                 "delta on HA-C4cp. PARTIAL is anticipated as the modal outcome; SUPPORTED requires the "
                 "personal-baseline operationalisation to produce a strictly LARGER delta than the "
                 "fixed-absolute-threshold operationalisation.")
    lines.append("")
    lines.append("3. **Approach A inheritance-by-analogue caveat**: the `bout_n_fast_recovery_day` beta = "
                 "-0.056/mg [CI -0.145, +0.034] p=0.223 template is NULL/weakly-consistent per "
                 "recalibration's underpowered-NULL framing; sign-flip is a fiat directional prior; "
                 "analogue substitution uncertainty is AMPLIFIED for HA-C4cp because the SD-anchored "
                 "operand family is FURTHER removed from the analogue than HA-C4c's fixed-absolute "
                 "operand. Dose-adjusted arm at section 4.9 is descriptive companion only.")
    lines.append("")
    lines.append("4. **Motion-confound corpus property**: 99.3% motion-confound at bout level per "
                 "HA11-bout-redo result section 4. HA-C4cp's motion-clean-only sensitivity arm anticipated "
                 "INCONCLUSIVE. Wiggers' 'during rest periods' verbatim implies a rest-conditional read; "
                 "the corpus does not admit a clean rest-conditional operand at bout level; the SD-anchored "
                 "family does not resolve this caveat -- it changes the reference frame for 'atypical' but "
                 "does not filter for motion-clean state.")
    lines.append("")
    lines.append("5. **Transient-fragility inheritance**: HA11-bout-redo transient-excluded discrimination "
                 "dropped from +20.26pp to +11.69pp. HA-C4cp likely to see analogous attenuation on "
                 "`bout_n_did_not_return_2sd_day` under transient exclusion; reported at section 4.10.")
    lines.append("")
    lines.append("6. **Reference-window construction dependency (LOAD-BEARING per section 5.3 family-"
                 "membership caveat)**: the Z=1 and z_max sensitivity arms share the parent MD section "
                 "3.2.2 reference-window construction with the primary. If the reference-window "
                 "calibration itself is off, all three cells inherit the bias. The "
                 "`reference_window_shorter_lag` and `reference_pool_dnr_excluded` sensitivity arms are "
                 "the reference-window-fragility diagnostic companions. The primary verdict is robust to "
                 "this caveat via the CONVENTIONS section 3.1 robust-baseline discipline (median + MAD).")
    lines.append("")
    lines.append("7. **Cross-op independence at operand-family level, NOT raw-substrate level** (per "
                 "OI-025 protocol section 5.4 four-condition argument): HA-C4c and HA-C4cp both derive "
                 "from the same Firstbeat-per-minute stress signal via the same bout-detection pipeline. "
                 "The independence claim binds at operand-family level (fixed-absolute-threshold vs "
                 "personal-baseline-rolling). A shared-substrate correlated failure mode would affect "
                 "both HAs.")
    lines.append("")
    lines.append("8. **Reference-window left-edge trim**: the [d-90, d-30] window trims ~60-90 days from "
                 "the leftmost has_garmin_uds=True coverage; the primary stratum's >= 2022-11-17 left "
                 "edge is more restrictive, so this trim does not become binding at primary. The "
                 "unmedicated-only sensitivity arm inherits the same trim and may lose ~30 days of "
                 "unmedicated coverage.")
    lines.append("")

    # === Section 11: Downstream actions ===============================
    lines.append("## Section 11 - Downstream actions (per pre-reg section 9 branch that actually fired)")
    lines.append("")
    if headline_verdict == "SUPPORTED":
        lines.append("Per pre-reg section 9.1 SUPPORTED branch:")
        lines.append("")
        lines.append("- Stage D descriptive audit companion at `analyses/descriptive/HA-C4cp/descriptive_audit.md` "
                     "LOCKED r1 2026-07-14 (already landed); re-consumed at cascade re-entry.")
        lines.append("- Stage I interpretation at `analyses/interpretation/HA-C4cp.md` locks; substantive "
                     "interpretive claim: the Wiggers-C4 pattern of atypical-for-subject return-times fires "
                     "directionally + at effect-size threshold on the personal-baseline-rolling operand family.")
        lines.append("- Stage S1 cluster-C-bout-substance.md LOCK re-consumes; cluster moves from single-member "
                     "(HA-C4c) to 2-member (HA-C4c + HA-C4cp); joint verdict CONCORDANT or PARTIALLY CONCORDANT "
                     "depending on HA-C4c PARTIAL + HA-C4cp SUPPORTED reading.")
        lines.append("- Stage A construct-bout-recovery-signal.md section 5.2 evidence-layer paragraph "
                     "updates to REACHED (cross-op-independence gap closed at strict guide section 4.2 "
                     "two-independent-HAs bar).")
        lines.append("- OI-033 CLOSED-BY-EXECUTION-SUPPORTED.")
    elif headline_verdict == "PARTIAL":
        lines.append("Per pre-reg section 9.2 PARTIAL branch:")
        lines.append("")
        lines.append("- Stage D + Stage I + Stage S1 LOCK with PARTIAL routing; cluster-C-bout-substance "
                     "joint verdict likely CONCORDANT-BELOW-THRESHOLD (both direction-correct; both PARTIAL).")
        lines.append("- Stage A tier-2 licensing stands; section 5.2 evidence-layer paragraph updates to "
                     "PARTIALLY REACHED (cross-op-independence gap CLOSED at direction-consistent-below-"
                     "threshold reading).")
        lines.append("- Substantive interpretive note: corpus-effect-size ceiling finding -- the Wiggers-C4 "
                     "signal fires directionally on this corpus at bout-level across both operand families "
                     "but the effect-size is bounded below the +0.20 SUPPORTED threshold. Honest sample-"
                     "limitation reading, NOT a Wiggers-C4 disproof.")
        lines.append("- OI-033 CLOSED-BY-EXECUTION-PARTIAL.")
    elif headline_verdict == "REJECTED":
        lines.append("Per pre-reg section 9.3 REJECTED branch:")
        lines.append("")
        lines.append("- Stage D + Stage I LOCK with REJECTED routing; Stage S1 cluster-C-bout-substance "
                     "joint verdict may be ORTHOGONAL or CONFLICT depending on direction shape.")
        lines.append("- Stage A: cross-op-independence gap CLOSURE reading depends on joint verdict shape; "
                     "ORTHOGONAL is a form of closure; CONFLICT triggers section 6.1 tier downgrade review.")
        lines.append("- Substantive interpretive note: operand-family-specific finding -- the signal is "
                     "anchored to the fixed-absolute-threshold reference frame; the personal-baseline-"
                     "rolling operationalisation does not fire.")
        lines.append("- HA-C4cp-v2 may be drafted per section 9.5 escalation table if operand-family "
                     "calibration is off; reference-window-shorter-lag sensitivity arm result informs "
                     "whether [d-90, d-30] was the binding calibration choice.")
        lines.append("- OI-033 CLOSED-BY-EXECUTION-REJECTED.")
    else:  # INCONCLUSIVE
        lines.append("Per pre-reg section 9.4 INCONCLUSIVE branch:")
        lines.append("")
        lines.append("- Stage D locks with INCONCLUSIVE routing; Stage I NOT dispatched.")
        lines.append("- Stage S1 cluster-C-bout-substance NOT re-consumed; cluster stands single-member (HA-C4c only).")
        lines.append("- OI-033 status: CLOSED-INCONCLUSIVE-WALK-FORWARD-GATE-NOT-MET or CLOSED-INCONCLUSIVE-"
                     "SANITY-HALT depending on which gate fired.")
        lines.append("- HA-C4cp-v2 dispatched at user tempo if reference-window recalibration is possible "
                     "per section 9.5.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Test run 2026-07-14 by Claude (Opus 4.7) in producer-mode under user authorisation per "
                 f"[CONVENTIONS section 1.1](../../../CONVENTIONS.md). Pre-registration r2 LOCKED 2026-07-09 "
                 f"at [`hypothesis.md`](hypothesis.md). Worktree HEAD at run: `{worktree_head}`. Pipeline "
                 f"commit: `{PIPELINE_COMMIT}`. `result-data.json` is the machine-readable companion "
                 f"(gitignored per `docs/research/**/*.json` rule).*")
    lines.append("")

    OUT_RESULT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_RESULT_MD}", file=sys.stderr)


# === Worktree HEAD lookup ===============================================

def get_worktree_head() -> str:
    """Return short HEAD SHA for the verification log."""
    import subprocess
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
            cwd=str(HERE),
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


# === Main ==============================================================

def _serialise(d: dict) -> dict:
    out: dict = {}
    for k, v in d.items():
        if isinstance(v, (bool, int, str, type(None))):
            out[k] = v
        elif isinstance(v, float):
            out[k] = v if not math.isnan(v) else None
        elif isinstance(v, dict):
            out[k] = _serialise(v)
        elif isinstance(v, list):
            out[k] = [
                _serialise(x) if isinstance(x, dict) else x
                for x in v
            ]
        else:
            out[k] = str(v)
    return out


def _print_arm_summary(r: dict) -> None:
    print(f"  arm='{r['arm_name']}' operand='{r['operand_col']}' "
          f"n_heavy={r['n_heavy']} n_non_heavy={r['n_non_heavy']}; "
          f"heavy_mean={r['heavy_mean']:.3f} non_heavy_mean={r['non_heavy_mean']:.3f}; "
          f"delta={r['cliffs_delta']:+.3f} p={r['block_perm_p_value']:.4f}; "
          f"verdict={r['verdict']}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Run section 10.4 sanity gates + section 4.7 walk-forward gate only.")
    args = parser.parse_args()

    print(f"DATA_ROOT: {DATA_ROOT}", file=sys.stderr)
    print(f"PER_DAY:   {PER_DAY_CSV}", file=sys.stderr)
    print(f"PER_BOUT:  {PER_BOUT_CSV}", file=sys.stderr)
    print(f"CRASHES:   {LABELS_CSV}", file=sys.stderr)
    print("", file=sys.stderr)

    print("Loading inputs...", file=sys.stderr)
    master = load_per_day_master()
    print(f"  per_day_master rows: {len(master)}", file=sys.stderr)
    print(f"  non-NaN {COL_PRIMARY}: "
          f"{sum(1 for d, info in master.items() if info[COL_PRIMARY] is not None)}",
          file=sys.stderr)
    print("", file=sys.stderr)

    # Dry-run gates (always runs first)
    gate_outcomes = dry_run_gates(master)

    if gate_outcomes["halt"]:
        print("Per pre-reg section 10.4: HALT. Section 10.4 sanity gates failed.", file=sys.stderr)
        print("A HA-C4cp-v2 redraft session would be the recovery path; not run here.", file=sys.stderr)
        return 1

    if args.dry_run:
        print("", file=sys.stderr)
        print("Dry-run only mode; not running full evaluation.", file=sys.stderr)
        return 0

    if gate_outcomes["inconclusive_walk_forward"]:
        print("Per pre-reg section 9.4: primary cell INCONCLUSIVE due to walk-forward gate failure.",
              file=sys.stderr)
        print("Writing INCONCLUSIVE result.md without full evaluation.", file=sys.stderr)
        inconc_primary = {
            "arm_name": "primary",
            "operand_col": COL_PRIMARY,
            "n_heavy": gate_outcomes["n_heavy"],
            "n_non_heavy": gate_outcomes["n_non_heavy"],
            "n_flagged_bouts": gate_outcomes["n_flagged_bouts_in_pool"],
            "heavy_mean": float("nan"), "heavy_median": float("nan"),
            "non_heavy_mean": float("nan"), "non_heavy_median": float("nan"),
            "cliffs_delta": float("nan"), "cliffs_delta_ci95_lo": float("nan"),
            "cliffs_delta_ci95_hi": float("nan"), "mannwhitney_u": float("nan"),
            "mannwhitney_p_normal_one_sided": float("nan"),
            "block_perm_p_value": float("nan"),
            "block_perm_n_ge": 0, "block_perm_B": 0,
            "block_perm_null_delta_median": float("nan"),
            "block_perm_null_delta_p025": float("nan"),
            "block_perm_null_delta_p975": float("nan"),
            "block_perm_n_heavy_null_mean": float("nan"),
            "block_perm_n_heavy_null_std": float("nan"),
            "el_companion": None,
            "bar_a_disc_p_lt_0_05": None,
            "bar_b_cliffs_delta_geq_0_20": None,
            "direction_correct": None,
            "verdict": "INCONCLUSIVE",
            "inconclusive": True, "crash_drop": False, "dose_beta_per_mg": None,
            "pool_mean": gate_outcomes["pool_mean"],
            "pool_median": gate_outcomes["pool_median"],
            "pool_std": gate_outcomes["pool_std"],
            "pool_p25": float("nan"), "pool_p75": float("nan"),
            "pool_min": float("nan"), "pool_max": float("nan"),
            "n_total_days": 0,
            "reference_window_audit": {
                "heavy_lagged_median": {"mean": float("nan"), "median": float("nan"),
                                        "p25": float("nan"), "p75": float("nan"), "n": 0},
                "heavy_lagged_mad": {"mean": float("nan"), "median": float("nan"),
                                     "p25": float("nan"), "p75": float("nan"), "n": 0},
                "non_heavy_lagged_median": {"mean": float("nan"), "median": float("nan"),
                                            "p25": float("nan"), "p75": float("nan"), "n": 0},
                "non_heavy_lagged_mad": {"mean": float("nan"), "median": float("nan"),
                                         "p25": float("nan"), "p75": float("nan"), "n": 0},
            },
        }
        conc_stub = cross_op_concordance(master)
        write_result_md(inconc_primary, {}, inconc_primary, {
            "delta_cliffs_delta": float("nan"),
            "delta_cliffs_delta_pp": float("nan"),
            "sign_flip": False, "flag_fired_010": False,
            "flag_fired_005pp": False, "route_to_rejected": False,
        }, {}, {"k": 0, "omitted": [], "per_cell": [],
                "annotation": "Holm not computable (primary INCONCLUSIVE)"},
            gate_outcomes, conc_stub, get_worktree_head())
        OUT_RESULT_JSON.write_text(
            json.dumps({
                "schema_version": 1,
                "ha_id": HA_ID,
                "pre_reg_lock": PRE_REG_LOCK_COMMIT,
                "pipeline_commit": PIPELINE_COMMIT,
                "verdict": "INCONCLUSIVE",
                "dry_run_gates": _serialise(gate_outcomes),
                "primary": _serialise(inconc_primary),
                "concordance": _serialise(conc_stub),
            }, indent=2, default=str), encoding="utf-8")
        return 0

    # === Full run =====================================================
    print("\n=== FULL RUN ===", file=sys.stderr)
    print("Loading per_bout_master.csv for sensitivity arms...", file=sys.stderr)
    per_bout = load_per_bout_master()
    print(f"  per-bout records: {len(per_bout)}", file=sys.stderr)

    # Primary arm
    print(f"\nEvaluating PRIMARY arm (cross-phase-pooled stratum, "
          f"operand=`{COL_PRIMARY}`)...", file=sys.stderr)
    primary = evaluate_arm(
        "primary", master, stratum_fn=day_in_primary_stratum,
        operand_col=COL_PRIMARY,
    )
    _print_arm_summary(primary)

    # Cross-op concordance descriptive companion
    print("\nComputing cross-op concordance descriptive companion...", file=sys.stderr)
    concordance = cross_op_concordance(master)
    print(f"  n_total={concordance['n_total']}; both_fire={concordance['n_both_fire']} "
          f"({concordance['frac_both_fire']*100:.1f}%); "
          f"kappa={concordance['kappa']:.3f}; "
          f"cap_unreachable={concordance['cap_unreachable_days']} "
          f"({concordance['cap_unreachable_frac']*100:.1f}%)", file=sys.stderr)

    # Sensitivity arms
    sens_arms: dict[str, dict] = {}

    # (1) Z=1 count sensitivity
    print(f"\nEvaluating SENSITIVITY arm 'z1_count' (operand=`{COL_Z1}`)...", file=sys.stderr)
    sens_arms["z1_count"] = evaluate_arm(
        "z1_count", master, stratum_fn=day_in_primary_stratum,
        operand_col=COL_Z1,
        run_permutation=True, compute_el_companion=False,
    )
    _print_arm_summary(sens_arms["z1_count"])

    # (2) z_max continuous sensitivity
    print(f"\nEvaluating SENSITIVITY arm 'z_max_continuous' (operand=`{COL_ZMAX}`)...",
          file=sys.stderr)
    sens_arms["z_max_continuous"] = evaluate_arm(
        "z_max_continuous", master, stratum_fn=day_in_primary_stratum,
        operand_col=COL_ZMAX,
        run_permutation=True, compute_el_companion=False,
    )
    _print_arm_summary(sens_arms["z_max_continuous"])

    # (3) reference_window_shorter_lag: re-aggregate primary operand with [d-60, d-30]
    print(f"\nEvaluating SENSITIVITY arm 'reference_window_shorter_lag' "
          f"([d-{REFERENCE_WINDOW_SHORTER[0]}, d-{REFERENCE_WINDOW_SHORTER[1]}])...",
          file=sys.stderr)
    shorter_counts, _ = reaggregate_sd_anchored_shorter_lag(
        per_bout, master,
        window_high=REFERENCE_WINDOW_SHORTER[0],
        window_low=REFERENCE_WINDOW_SHORTER[1],
    )
    shorter_overlay = overlay_column(
        master, shorter_counts, COL_PRIMARY, require_original_non_nan=False,
    )
    sens_arms["reference_window_shorter_lag"] = evaluate_arm(
        "reference_window_shorter_lag", shorter_overlay,
        stratum_fn=day_in_primary_stratum,
        operand_col=COL_PRIMARY,
        run_permutation=True, compute_el_companion=False,
    )
    _print_arm_summary(sens_arms["reference_window_shorter_lag"])

    # (4) unmedicated_only
    print("\nEvaluating SENSITIVITY arm 'unmedicated_only'...", file=sys.stderr)
    sens_arms["unmedicated_only"] = evaluate_arm(
        "unmedicated_only", master,
        stratum_fn=day_in_unmedicated_only,
        operand_col=COL_PRIMARY,
        run_permutation=True, compute_el_companion=False,
    )
    _print_arm_summary(sens_arms["unmedicated_only"])

    # (5-7) motion_clean_only, transient_excluded, baseline_invalid_excluded:
    # re-aggregate did_not_return_2sd counts from per_bout_master (flag-only
    # filter; reference window unchanged) then overlay onto primary master.
    for arm_name, kw in [
        ("motion_clean_only",         {"motion_clean": True}),
        ("transient_excluded",        {"transient_excluded": True}),
        ("baseline_invalid_excluded", {"baseline_invalid_excluded": True}),
    ]:
        print(f"\nEvaluating SENSITIVITY arm '{arm_name}'...", file=sys.stderr)
        re_counts = reaggregate_sd_anchored_flag_only(per_bout, **kw)
        overlay = overlay_column(
            master, re_counts, COL_PRIMARY, require_original_non_nan=True,
        )
        sens_arms[arm_name] = evaluate_arm(
            arm_name, overlay, stratum_fn=day_in_primary_stratum,
            operand_col=COL_PRIMARY,
            run_permutation=True, compute_el_companion=False,
        )
        _print_arm_summary(sens_arms[arm_name])

    # (9) reference_pool_dnr_excluded: re-aggregate with reference pool excluding
    # did_not_return_flag=True bouts (re-computes median/mad on reduced pool at
    # the primary [d-90, d-30] window).
    print("\nEvaluating SENSITIVITY arm 'reference_pool_dnr_excluded' "
          "(reference pool excludes did_not_return_flag=True bouts)...", file=sys.stderr)
    dnr_excl_counts, _ = reaggregate_sd_anchored_shorter_lag(
        per_bout, master,
        window_high=REFERENCE_WINDOW_PRIMARY[0],
        window_low=REFERENCE_WINDOW_PRIMARY[1],
        exclude_did_not_return_bouts=True,
    )
    dnr_excl_overlay = overlay_column(
        master, dnr_excl_counts, COL_PRIMARY, require_original_non_nan=False,
    )
    sens_arms["reference_pool_dnr_excluded"] = evaluate_arm(
        "reference_pool_dnr_excluded", dnr_excl_overlay,
        stratum_fn=day_in_primary_stratum,
        operand_col=COL_PRIMARY,
        run_permutation=True, compute_el_companion=False,
    )
    _print_arm_summary(sens_arms["reference_pool_dnr_excluded"])

    # (8) Crash-drop sensitivity
    print("\nEvaluating CRASH-DROP sensitivity (is_crash=True dropped from both arms)...",
          file=sys.stderr)
    crash_dropped = evaluate_arm(
        "crash_dropped", master, stratum_fn=day_in_primary_stratum,
        operand_col=COL_PRIMARY,
        crash_drop=True, run_permutation=True, compute_el_companion=False,
    )
    _print_arm_summary(crash_dropped)
    cd_flag = crash_drop_flag_evaluation(primary, crash_dropped)
    print(f"  |Delta Cliff's delta|={abs(cd_flag['delta_cliffs_delta']):.3f}; "
          f"flag (>{CRASH_DROP_FLAG_DELTA_DELTA}): "
          f"{'FIRED' if cd_flag['flag_fired_010'] else 'CLEAN'}", file=sys.stderr)

    # (10) Approach A sensitivity arms (descriptive companions only)
    approach_a_arms: dict[str, dict] = {}
    for name, beta in [
        ("Approach A primary template",  APPROACH_A_BETA_PRIMARY),
        ("CI lower bracket (NULL)",      APPROACH_A_BETA_CI_LOWER),
        ("CI upper bracket (NULL)",      APPROACH_A_BETA_CI_UPPER),
    ]:
        print(f"\nEvaluating Approach A sub-arm '{name}' (beta={beta:+.3f}/mg)...",
              file=sys.stderr)
        approach_a_arms[name] = evaluate_arm(
            name, master, stratum_fn=day_in_primary_stratum,
            operand_col=COL_PRIMARY,
            dose_beta_per_mg=beta,
            run_permutation=True, compute_el_companion=False,
        )
        _print_arm_summary(approach_a_arms[name])

    # Holm step-down family (section 5.3): 7 cells
    holm_p_values: list[float] = []
    for lab in HOLM_FAMILY_LABELS:
        if lab == "primary":
            holm_p_values.append(primary["block_perm_p_value"])
        else:
            arm = sens_arms.get(lab)
            if arm is None:
                holm_p_values.append(float("nan"))
            elif arm["verdict"] == "INCONCLUSIVE":
                holm_p_values.append(float("nan"))
            else:
                holm_p_values.append(arm["block_perm_p_value"])
    holm = holm_step_down(holm_p_values, HOLM_FAMILY_LABELS)
    print(f"\n=== HOLM STEP-DOWN ({holm['annotation']}) ===", file=sys.stderr)
    for cell in holm["per_cell"]:
        print(f"  {cell['label']:30s} raw_p={fmt_p(cell['raw_p'])} "
              f"threshold={cell['threshold']:.5f} "
              f"adj_p={fmt_p(cell['adjusted_p'])} "
              f"rejected={'YES' if cell['rejected_at_holm'] else 'NO'}",
              file=sys.stderr)

    # Apply crash-drop sign-flip routing rule per section 5.2
    if cd_flag["route_to_rejected"] and primary["verdict"] != "REJECTED":
        print(f"\nCrash-drop sign-flip route_to_rejected fired (|delta delta|>"
              f"{CRASH_DROP_FLAG_DELTA_DELTA_REJECT} AND sign-flip). Routing primary "
              "verdict to REJECTED per section 5.2.", file=sys.stderr)
        primary["verdict"] = "REJECTED"

    # Final summary
    print("\n=== FINAL VERDICT ===", file=sys.stderr)
    print(f"  {HA_ID} primary verdict: {primary['verdict']}", file=sys.stderr)
    print(f"  direction: {'positive' if primary['direction_correct'] else 'negative' if primary['direction_correct'] is False else 'n/a'}",
          file=sys.stderr)
    print(f"  (a) block-perm p < 0.05: {fmt_pass_fail(primary['bar_a_disc_p_lt_0_05'])} "
          f"(p={fmt_p(primary['block_perm_p_value'])})", file=sys.stderr)
    print(f"  (b) Cliff's delta >= +0.20: {fmt_pass_fail(primary['bar_b_cliffs_delta_geq_0_20'])} "
          f"(delta={fmt_delta(primary['cliffs_delta'])})", file=sys.stderr)

    # Emit result.md + result-data.json
    worktree_head = get_worktree_head()
    write_result_md(primary, sens_arms, crash_dropped, cd_flag,
                    approach_a_arms, holm, gate_outcomes, concordance,
                    worktree_head)

    out_data = {
        "schema_version": 1,
        "ha_id": HA_ID,
        "pre_reg_lock": PRE_REG_LOCK_COMMIT,
        "pipeline_commit": PIPELINE_COMMIT,
        "worktree_head": worktree_head,
        "random_seed_perm": RANDOM_SEED,
        "B_headline": B_HEADLINE,
        "expected_block_length": BOOTSTRAP_E_L,
        "bar_a_p_value": BAR_A_P_VALUE,
        "bar_b_cliffs_delta": BAR_B_CLIFFS_DELTA,
        "wf_gate_n_heavy": WF_GATE_N_HEAVY,
        "wf_gate_n_non_heavy": WF_GATE_N_NON_HEAVY,
        "primary_operand": COL_PRIMARY,
        "reference_window_primary": list(REFERENCE_WINDOW_PRIMARY),
        "reference_window_shorter": list(REFERENCE_WINDOW_SHORTER),
        "reference_window_min_bouts": REFERENCE_WINDOW_MIN_BOUTS,
        "dry_run_gates": _serialise(gate_outcomes),
        "primary": _serialise(primary),
        "sensitivity_arms": {k: _serialise(v) for k, v in sens_arms.items()},
        "crash_dropped": _serialise(crash_dropped),
        "crash_drop_flag": _serialise(cd_flag),
        "approach_a_arms": {k: _serialise(v) for k, v in approach_a_arms.items()},
        "holm": _serialise(holm),
        "cross_op_concordance": _serialise(concordance),
    }
    OUT_RESULT_JSON.write_text(
        json.dumps(out_data, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote {OUT_RESULT_JSON}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
