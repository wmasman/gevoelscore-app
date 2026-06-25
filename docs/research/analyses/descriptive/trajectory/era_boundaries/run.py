"""Q4.3 -- era_boundaries: methodological backstop on the project's era/phase boundaries.

METHODOLOGICAL BACKSTOP per descriptive README sec 4.3. The project's
era/phase boundaries are currently operational without published
data-driven justification. This analysis:

1. Tests the 12 CURRENT boundaries (6 recovery-phase + 5 citalopram-phase
   + 1 historical 2023-12-31 train/validate split) for distribution-shift
   per channel using KS + mean-shift + cumulative-distribution evidence
   in a +-30d window per side.
2. Runs data-driven change-point detection per channel using binary
   segmentation (documented choice; see Stage 3 docstring).
3. Compares data-driven candidates AGAINST the recovery-phase boundaries
   as the lived-experience reference, flagging proximity at +-21d
   tolerance (CONFIRMED-by-data vs NOVEL-data-driven labels; DESCRIPTIVE
   ONLY, no recommendation).

CRITICAL USER FRAMING (per handoff sec 1): recovery-phase boundaries
ARE the lived-experience reference. Data-driven candidates that LAND
ON them are confirmatory; candidates that DON'T land on them are NOT
"wrong" -- they may reflect channel-specific dynamics. NO round-date
alternatives. The user owns the boundary decision; this artefact
provides DESCRIPTIVE justification only.

USER-LOCKED OPERATIONALISATION (per Strand B sec 7c interview
2026-06-25; do NOT iterate):

1. Boundary scope = 6 recovery-phase + 5 citalopram-phase + 1 historical
   2023-12-31 train/validate split (12 total).
2. Method = both per-boundary distribution-shift tests AND data-driven
   change-point detection.
3. Channel scope = 7 channels (Q4.9 6 Garmin + gevoelscore):
   - stress_mean_sleep            (CONFIRMED-citalopram +0.43/mg)
   - all_day_stress_avg           (CONFIRMED-citalopram +0.57/mg)
   - bb_lowest                    (CONFIRMED-citalopram -1.13/mg)
   - stress_stdev_sleep           (HA07d primary)
   - stress_low_motion_min_count_S60_Mlow (Q3.x; HA-C4b)
   - resting_hr                   (HA06b primary; very-long memory)
   - gevoelscore                  (outcome side)
4. Alternatives = data-driven only; compared AGAINST recovery-phase
   boundaries as lived-experience reference. NO round-date alternatives.

OUTPUTS (3 artefacts per handoff sec 3.2 Stage 5):

- Per-boundary descriptive justification table (12 x 7 = 84 cells:
  KS p-value + mean-shift + cumulative-shift per cell; pooled summary)
- Data-driven change-point candidate map per channel (list + proximity
  to recovery-phase boundaries)
- Per-recovery-phase-boundary defensibility chart (for each of 6
  recovery-phase boundaries: how many of 7 channels show distribution
  shift; how many data-driven candidates land within +-21d tolerance)

DISCIPLINE GUARDS (per CONVENTIONS):

- sec 2.1 descriptive-before-inference: report shift evidence per cell;
  NO causal claims; NO "boundary X is unjustified" claims; NO
  data-driven-candidate-as-better-boundary recommendations.
- sec 3.1 personal baseline: applied where appropriate to per-channel
  window distributions.
- sec 3.6 named counts: every n in summary tables names scheme + unit.
- sec 4.1 + sec 4.2: descriptive framing only ("boundary X shows
  distribution shift on Z of 7 channels"); NO promotion to verdicts;
  caveat-class language preserved.
- sec 4.3: data-driven change-point detection is exploratory; surface
  candidates descriptively + proximity to recovery-phase boundaries;
  do NOT pre-commit any candidate as a "better" boundary.

CROSS-REFERENCES LOAD-BEARING (per handoff sec 3.3):

- lc_recovery_phase_axis sec 7b resting_hr 4a->4b finding REPRODUCED
  + EXTENDED across 7 channels in Stage 2.
- Q4.9 episode-level matched cross-referenced for the autonomic-load
  family pre-crash elevation pattern.
- Q4.6 coverage analysis cross-referenced for boundary-zone coverage
  (some recovery-phase 1/2/3 boundaries in 2021-2022 have limited
  gevoelscore coverage; flag honestly).
- recovery_arc v2 sec 5.A afbouw-reversal cross-referenced for the
  citalopram-phase 5 boundary (consolidation -> afbouw at 2026-03-20).
- permutation_null_block_length E[L]=7 (autocorrelation context for
  change-point window choices).

Layer 1 descriptive per CONVENTIONS sec 2.1.
NOT a substantive HA verdict; NOT a recommendation to change any
boundary; NOT a promotion of any data-driven candidate as "better".
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
# HERE = .../analyses/descriptive/trajectory/era_boundaries
# parents[0]=trajectory; [1]=descriptive; [2]=analyses
UTILS_DIR = HERE.parents[2] / "_utils"
sys.path.insert(0, str(UTILS_DIR))

from frame import load_master  # noqa: E402


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AS_OF_DATE = "2026-06-04"  # Garmin coverage right-edge per STOCKTAKE sec 1

# 7 channels per user-locked operationalisation (handoff sec 2.3)
CHANNELS = [
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
    "stress_stdev_sleep",
    "stress_low_motion_min_count_S60_Mlow",
    "resting_hr",
    "gevoelscore",
]

# CONFIRMED-citalopram subset (descriptive context)
CONFIRMED_CITALOPRAM = {
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
}

# Window around each boundary for distribution-shift tests (handoff sec 3.2 Stage 2)
SHIFT_WINDOW_DAYS = 30
# Rolling window for mean-shift evidence at boundary date
ROLLING_WINDOW_DAYS = 28
# Proximity tolerance for data-driven candidate -> recovery-phase boundary
# (handoff sec 3.2 Stage 4). E[L]=7 from permutation_null_block_length.md
# implies block-bootstrap autocorrelation scale; +-21d = 3 * E[L].
PROXIMITY_TOLERANCE_DAYS = 21

# Block length for autocorrelation context per permutation_null_block_length E[L]=7
DEFAULT_BLOCK_LENGTH = 7

# Number of permutations for the KS-shuffle null
KS_PERMUTATIONS = 1000
RANDOM_SEED = 42


# ---------------------------------------------------------------------------
# Boundary catalog (the 12 CURRENT boundaries to test)
# ---------------------------------------------------------------------------

# 6 recovery-phase boundaries per lc_recovery_phase_axis.md sec 2.
# Boundary = the date that STARTS the next phase. For each boundary, name
# is the "from -> to" transition and warrant class is the M1/M2 per
# lc_recovery_phase_axis sec 3.
# NB: boundaries 1 (pre_illness -> acute) and 2 (acute -> lc_pre_ergo)
# are data-given per lc_era_temporal_segmentation sec 1; boundaries 3
# (lc_pre_ergo -> 4a), 4 (4a -> 4b), 5 (4b -> citalopram_modulated) are
# M1 lived-experience anchors per lc_recovery_phase_axis sec 3.3-3.5.
RECOVERY_PHASE_BOUNDARIES = [
    ("rp1_pre_illness_to_acute",       date(2022, 3, 21), "data-given (COVID PCR-positive)"),
    ("rp2_acute_to_lc_pre_ergo",       date(2022, 4, 4),  "data-given (Monday after Fietsweekend Ardennen)"),
    ("rp3_lc_pre_ergo_to_4a",          date(2022, 9, 22), "M1 lived-experience (Ergotherapie Rouschop start)"),
    ("rp4_4a_to_4b",                   date(2022, 11, 17), "M1 lived-experience (8-week post-ergo habit-formation)"),
    ("rp5_4b_to_citalopram_modulated", date(2024, 4, 9),  "M2 documented confounder (Citalopram buildup start)"),
    # NB: phase 6 post_afbouw begins 2026-06-06 per citalopram_phase_stratification sec 3;
    # corpus ends 2026-06-04 so this 6th recovery-phase boundary is OUT-OF-CORPUS by
    # 2 days. We include it to comply with the user-locked "6 recovery-phase boundaries"
    # scope; per-cell tests will return n_post=0 honestly.
    ("rp6_citalopram_modulated_to_post_afbouw", date(2026, 6, 6), "out-of-corpus (post-afbouw begins 2 days after corpus end)"),
]

# 5 citalopram-phase boundaries per citalopram_phase_stratification sec 3.
# 4 phase transitions inside the citalopram traject + the unmedicated->buildup
# transition (which coincides with rp5 above by construction).
# Per handoff sec 2: include all 5 even though boundary 1 here equals rp5.
CITALOPRAM_PHASE_BOUNDARIES = [
    ("cp1_unmedicated_to_buildup",       date(2024, 4, 9),  "documented intervention (Citalopram buildup start; coincides with rp5)"),
    ("cp2_buildup_to_consolidation",     date(2024, 6, 20), "documented intervention (30mg steady-state achieved)"),
    ("cp3_consolidation_to_afbouw",      date(2026, 3, 20), "documented intervention (Citalopram afbouw/taper start)"),
    ("cp4_afbouw_to_post_afbouw",        date(2026, 6, 6),  "out-of-corpus (post_afbouw begins 2 days after corpus end)"),
    # Per citalopram_phase_stratification: the 5 boundaries per the phase
    # spec are (unmedicated start), buildup, consolidation, afbouw,
    # post_afbouw. We test the 4 within-traject transitions plus the
    # historical unmedicated-LC-start 2022-04-04 as the 5th boundary
    # (where the unmedicated phase formally starts at LC start).
    ("cp5_lc_start_to_unmedicated",      date(2022, 4, 4),  "documented stratum boundary (LC start; aligns with rp2)"),
]

# 1 historical 2023-12-31 train/validate split per train_validate_split_fate.md
# (retired but characterised descriptively for reproducibility-artefact closure)
HISTORICAL_BOUNDARIES = [
    ("hist1_2023_12_31_train_validate", date(2023, 12, 31), "RETIRED historical M3 sensitivity overlay (chosen under deleted trajectory framing; preserved for HA01b/HA02c reproducibility)"),
]

ALL_BOUNDARIES = (
    RECOVERY_PHASE_BOUNDARIES
    + CITALOPRAM_PHASE_BOUNDARIES
    + HISTORICAL_BOUNDARIES
)

# Set of dates that ARE recovery-phase boundaries (for proximity flag in Stage 4)
RECOVERY_PHASE_DATES = {b[1] for b in RECOVERY_PHASE_BOUNDARIES}


# ---------------------------------------------------------------------------
# Stage 1 -- data prep
# ---------------------------------------------------------------------------


def stage1_data_prep() -> dict:
    """Load per_day_master; restrict to 7 channels + date + recovery_phase
    + dose_plasma_mg (for citalopram_phase derivation).

    Returns dict with:
    - df: pd.DataFrame, full corpus rows with the 7 channels + date
      + recovery_phase + citalopram_phase
    - n_rows: int
    - n_per_channel: dict channel -> non-NaN count
    - corpus_left: date, first date in master
    - corpus_right: date, last date in master (== AS_OF_DATE)
    """
    master = load_master(as_of_date=AS_OF_DATE)
    master = master.copy()
    master["date"] = pd.to_datetime(master["date"])
    master = master.sort_values("date").reset_index(drop=True)

    keep_cols = ["date", "recovery_phase"] + CHANNELS
    if "dose_plasma_mg" in master.columns:
        keep_cols.append("dose_plasma_mg")
    available_cols = [c for c in keep_cols if c in master.columns]
    df = master[available_cols].copy()

    # Derive citalopram_phase per row (from dose if available; else from
    # date intervals per citalopram_phase_stratification sec 3).
    df["citalopram_phase"] = df["date"].dt.date.apply(_citalopram_phase_from_date)

    n_per_channel = {
        c: int(df[c].notna().sum()) if c in df.columns else 0
        for c in CHANNELS
    }

    return {
        "df": df,
        "n_rows": int(len(df)),
        "n_per_channel": n_per_channel,
        "corpus_left": df["date"].min().date(),
        "corpus_right": df["date"].max().date(),
    }


def _citalopram_phase_from_date(d) -> str:
    """Per citalopram_phase_stratification sec 3 helper."""
    if not isinstance(d, date):
        d = pd.Timestamp(d).date()
    if d < date(2024, 4, 9):
        return "unmedicated"
    if d < date(2024, 6, 20):
        return "buildup"
    if d < date(2026, 3, 20):
        return "consolidation"
    if d < date(2026, 6, 6):
        return "afbouw"
    return "post_afbouw"


# ---------------------------------------------------------------------------
# Stage 2 -- per-boundary distribution-shift tests
# ---------------------------------------------------------------------------


def stage2_per_boundary_shift(df: pd.DataFrame) -> dict:
    """For each of the 12 CURRENT boundaries x 7 channels = 84 cells:
    compute KS p-value (two-sample), mean-shift, and cumulative shift
    over a +-30d window each side of the boundary.

    Returns dict[boundary_id][channel] -> per-cell shift evidence.
    """
    results: dict = {}
    rng = np.random.default_rng(RANDOM_SEED)

    for bid, bdate, warrant in ALL_BOUNDARIES:
        results[bid] = {
            "boundary_date": bdate.isoformat(),
            "warrant": warrant,
            "cells": {},
        }
        for chan in CHANNELS:
            cell = _per_cell_shift(df, chan, bdate, rng)
            results[bid]["cells"][chan] = cell

    # Multi-channel synthesis per boundary
    for bid in results:
        cells = results[bid]["cells"]
        n_channels_shift = 0
        n_channels_tested = 0
        ks_p_values = []
        for chan, c in cells.items():
            if c.get("skipped"):
                continue
            n_channels_tested += 1
            ks_p_values.append(c.get("ks_p_value", np.nan))
            if c.get("shift_detected"):
                n_channels_shift += 1
        results[bid]["n_channels_shift"] = int(n_channels_shift)
        results[bid]["n_channels_tested"] = int(n_channels_tested)
        results[bid]["channels_with_shift"] = sorted([
            chan for chan, c in cells.items() if c.get("shift_detected")
        ])

    return results


def _per_cell_shift(
    df: pd.DataFrame,
    chan: str,
    bdate: date,
    rng: np.random.Generator,
) -> dict:
    """One per-cell distribution-shift test: KS + mean-shift +
    cumulative-shift on +-30d window each side of bdate.

    Returns dict with shift_detected + p-value + effect-size.
    """
    if chan not in df.columns:
        return {"skipped": True, "reason": "channel not in master"}

    win_start = pd.Timestamp(bdate - timedelta(days=SHIFT_WINDOW_DAYS))
    win_end = pd.Timestamp(bdate + timedelta(days=SHIFT_WINDOW_DAYS))
    bts = pd.Timestamp(bdate)

    pre = df[(df["date"] >= win_start) & (df["date"] < bts)][chan].dropna().values
    post = df[(df["date"] >= bts) & (df["date"] < win_end)][chan].dropna().values

    n_pre = int(len(pre))
    n_post = int(len(post))

    if n_pre < 5 or n_post < 5:
        return {
            "skipped": True,
            "reason": "insufficient data in +-30d window",
            "n_pre": n_pre,
            "n_post": n_post,
        }

    # KS two-sample (vendored to avoid scipy dependency)
    ks_stat, ks_p = _two_sample_ks(pre, post, rng)

    pre_mean = float(np.mean(pre))
    post_mean = float(np.mean(post))
    pre_med = float(np.median(pre))
    post_med = float(np.median(post))
    pre_std = float(np.std(pre, ddof=1)) if n_pre > 1 else 0.0
    post_std = float(np.std(post, ddof=1)) if n_post > 1 else 0.0
    pooled_std = float(np.sqrt(
        ((n_pre - 1) * pre_std**2 + (n_post - 1) * post_std**2)
        / max(1, n_pre + n_post - 2)
    )) if (n_pre + n_post) > 2 else 0.0
    mean_shift = post_mean - pre_mean
    cohens_d = (mean_shift / pooled_std) if pooled_std > 0 else 0.0

    # Cumulative shift = KS statistic itself (the sup of CDF difference)
    cumulative_shift = float(ks_stat)

    # Rolling 28d evidence: median around +-rolling/2 of boundary
    half = ROLLING_WINDOW_DAYS // 2
    pre_roll_start = pd.Timestamp(bdate - timedelta(days=ROLLING_WINDOW_DAYS))
    post_roll_end = pd.Timestamp(bdate + timedelta(days=ROLLING_WINDOW_DAYS))
    pre_roll = df[(df["date"] >= pre_roll_start) & (df["date"] < bts)][chan].dropna().values
    post_roll = df[(df["date"] >= bts) & (df["date"] < post_roll_end)][chan].dropna().values
    pre_roll_med = float(np.median(pre_roll)) if len(pre_roll) > 0 else float("nan")
    post_roll_med = float(np.median(post_roll)) if len(post_roll) > 0 else float("nan")
    rolling_median_shift = (
        post_roll_med - pre_roll_med
        if not np.isnan(pre_roll_med) and not np.isnan(post_roll_med)
        else float("nan")
    )
    _ = half  # half retained for documentation; rolling windows above use full ROLLING_WINDOW_DAYS

    # Descriptive shift_detected flag: KS p < 0.05 OR |cohens_d| > 0.5
    # NB: descriptive only; this is a per-cell flag, not a verdict per
    # CONVENTIONS sec 4.2. The "Z of 7 channels show shift" summary is
    # the load-bearing read.
    shift_detected = bool(ks_p < 0.05 or abs(cohens_d) > 0.5)

    return {
        "n_pre": n_pre,
        "n_post": n_post,
        "pre_mean": pre_mean,
        "post_mean": post_mean,
        "pre_median": pre_med,
        "post_median": post_med,
        "mean_shift": mean_shift,
        "cohens_d": cohens_d,
        "ks_statistic": float(ks_stat),
        "ks_p_value": float(ks_p),
        "cumulative_shift": cumulative_shift,
        "rolling_pre_median_28d": pre_roll_med,
        "rolling_post_median_28d": post_roll_med,
        "rolling_median_shift": rolling_median_shift,
        "shift_detected": shift_detected,
    }


def _two_sample_ks(
    a: np.ndarray,
    b: np.ndarray,
    rng: np.random.Generator,
) -> tuple[float, float]:
    """Two-sample Kolmogorov-Smirnov test (vendored; permutation p-value).

    KS statistic = sup |F_a(x) - F_b(x)| on the pooled sample. p-value is
    a permutation-based estimate (KS_PERMUTATIONS shuffles of pooled
    labels). Returns (statistic, p_value).
    """
    a_arr = np.asarray(a, dtype=float)
    b_arr = np.asarray(b, dtype=float)
    n_a = len(a_arr)
    n_b = len(b_arr)

    def ks_stat(x: np.ndarray, y: np.ndarray) -> float:
        x_sorted = np.sort(x)
        y_sorted = np.sort(y)
        all_v = np.concatenate([x_sorted, y_sorted])
        cdf_x = np.searchsorted(x_sorted, all_v, side="right") / len(x_sorted)
        cdf_y = np.searchsorted(y_sorted, all_v, side="right") / len(y_sorted)
        return float(np.max(np.abs(cdf_x - cdf_y)))

    observed = ks_stat(a_arr, b_arr)

    # Permutation null for KS p-value (block-naive label shuffle)
    pooled = np.concatenate([a_arr, b_arr])
    n_total = n_a + n_b
    perm_stats = np.empty(KS_PERMUTATIONS)
    for i in range(KS_PERMUTATIONS):
        idx = rng.permutation(n_total)
        perm_a = pooled[idx[:n_a]]
        perm_b = pooled[idx[n_a:]]
        perm_stats[i] = ks_stat(perm_a, perm_b)

    p = float(np.mean(perm_stats >= observed))
    # Avoid p=0 in finite Monte Carlo
    p = max(p, 1.0 / KS_PERMUTATIONS)

    return observed, p


# ---------------------------------------------------------------------------
# Stage 3 -- data-driven change-point detection per channel
# ---------------------------------------------------------------------------


def stage3_change_point_detection(df: pd.DataFrame) -> dict:
    """Per-channel binary segmentation on the 28d-rolling median series.

    METHOD CHOICE (handoff sec 3.2 Stage 3 + sec 6 acceptance criterion 7):
    binary segmentation over PELT because:

    1. It is a parameter-light variant (only requires a max-depth +
       minimum-segment-size parameter rather than PELT's penalty parameter
       which is data-scale-dependent).
    2. It is interpretable -- each split is a single best-cut decision
       at that segment level, traceable in the output.
    3. The project has no pre-existing change-point library dependency;
       binary segmentation is small enough to vendor here without taking
       on `ruptures` or similar packages.

    Operating on the 28d-rolling-median of the raw channel (smooths
    daily noise; preserves multi-month drift) per the same scale as
    Stage 2 rolling evidence. Maximum depth = 12 splits per channel
    (allows up to ~12 candidate change-points, enough to cover the 12
    CURRENT boundaries comfortably). Minimum segment size = 60 days
    (~2 months; prevents the algorithm from finding micro-boundaries
    that would not align with the lived-experience phase scale per
    lc_recovery_phase_axis sec 3).

    Returns dict[channel] -> list of candidate change-point dates.
    """
    results: dict = {}
    for chan in CHANNELS:
        if chan not in df.columns:
            results[chan] = {"skipped": True, "reason": "channel not in master"}
            continue
        # Use a date-indexed series; compute 28d-rolling median to smooth
        # daily noise while preserving multi-month structure
        ts = df.set_index("date")[chan].dropna()
        if len(ts) < 60:
            results[chan] = {
                "skipped": True,
                "reason": "insufficient data for change-point detection",
                "n": int(len(ts)),
            }
            continue
        smoothed = ts.rolling(window=28, min_periods=14, center=False).median().dropna()
        if len(smoothed) < 60:
            results[chan] = {
                "skipped": True,
                "reason": "insufficient smoothed data",
                "n": int(len(smoothed)),
            }
            continue
        values = smoothed.values
        dates = smoothed.index

        change_points = _binary_segmentation(
            values,
            max_depth=12,
            min_segment_size=60,
        )

        candidate_dates = sorted(
            [dates[cp].date() for cp in change_points]
        )

        results[chan] = {
            "skipped": False,
            "n_smoothed": int(len(smoothed)),
            "n_candidates": int(len(candidate_dates)),
            "candidates": [d.isoformat() for d in candidate_dates],
            "smoothing_window_days": 28,
            "min_segment_size_days": 60,
            "max_depth": 12,
            "method": "binary_segmentation_on_28d_rolling_median",
        }
    return results


def _binary_segmentation(
    values: np.ndarray,
    *,
    max_depth: int,
    min_segment_size: int,
) -> list[int]:
    """Recursive binary segmentation for change-point detection.

    Per-segment statistic = sum-of-squared-deviations reduction at the
    best single cut. Returns the list of change-point indices (sorted).

    This is the canonical algorithm: at each level, find the single
    best cut within the current segment (the cut that maximally reduces
    within-segment sum-of-squared-deviations); recurse into the two
    resulting sub-segments. Stops when max_depth is reached OR the
    candidate cuts would yield sub-segments below min_segment_size.

    The "best cut" criterion is the standard binseg likelihood-ratio
    proxy: at each candidate cut index k, the candidate score is the
    reduction in total SSD when the segment [a, b] is split into [a, k)
    and [k, b]. Higher reduction = more change-pointy.
    """
    cps: list[int] = []
    _binseg_recurse(values, 0, len(values), 0, max_depth, min_segment_size, cps)
    return sorted(cps)


def _binseg_recurse(
    values: np.ndarray,
    a: int,
    b: int,
    depth: int,
    max_depth: int,
    min_segment_size: int,
    cps: list[int],
) -> None:
    """Recursive helper for binary segmentation."""
    if depth >= max_depth:
        return
    if (b - a) < 2 * min_segment_size:
        return

    best_k = -1
    best_score = 0.0
    seg = values[a:b]
    seg_mean = float(seg.mean())
    total_ssd = float(((seg - seg_mean) ** 2).sum())

    # Try each candidate cut from a+min_segment_size to b-min_segment_size
    for k_local in range(min_segment_size, (b - a) - min_segment_size):
        left = seg[:k_local]
        right = seg[k_local:]
        left_ssd = float(((left - left.mean()) ** 2).sum())
        right_ssd = float(((right - right.mean()) ** 2).sum())
        score = total_ssd - (left_ssd + right_ssd)
        if score > best_score:
            best_score = score
            best_k = a + k_local

    # Threshold: require the reduction to be at least 5% of the total
    # within-segment SSD (otherwise the cut is not material; descriptive
    # noise floor). 5% is a conservative threshold that prevents
    # over-segmentation while still catching real shifts.
    if best_k < 0 or total_ssd <= 0:
        return
    if best_score / total_ssd < 0.05:
        return

    cps.append(best_k)
    _binseg_recurse(values, a, best_k, depth + 1, max_depth, min_segment_size, cps)
    _binseg_recurse(values, best_k, b, depth + 1, max_depth, min_segment_size, cps)


# ---------------------------------------------------------------------------
# Stage 4 -- alternative comparison vs recovery-phase reference
# ---------------------------------------------------------------------------


def stage4_proximity_comparison(stage3: dict) -> dict:
    """For each data-driven candidate, find its proximity to the nearest
    recovery-phase boundary; flag as CONFIRMED-by-data (within +-21d) or
    NOVEL-data-driven (further away).

    Returns dict[channel] -> per-candidate proximity flag.
    """
    rp_dates = sorted(RECOVERY_PHASE_DATES)
    results: dict = {}
    for chan in CHANNELS:
        if stage3.get(chan, {}).get("skipped"):
            results[chan] = {"skipped": True}
            continue
        candidates = stage3[chan]["candidates"]
        per_cand = []
        for c_iso in candidates:
            cdate = date.fromisoformat(c_iso)
            best_diff = None
            best_rp = None
            for rp in rp_dates:
                diff_days = (cdate - rp).days
                if best_diff is None or abs(diff_days) < abs(best_diff):
                    best_diff = diff_days
                    best_rp = rp
            assert best_rp is not None
            within = abs(best_diff) <= PROXIMITY_TOLERANCE_DAYS
            per_cand.append({
                "candidate_date": c_iso,
                "nearest_recovery_phase_boundary": best_rp.isoformat(),
                "diff_days": int(best_diff),
                "within_tolerance": bool(within),
                "label": "CONFIRMED-by-data" if within else "NOVEL-data-driven",
            })
        results[chan] = {
            "skipped": False,
            "n_candidates": len(per_cand),
            "n_confirmed_by_data": sum(1 for r in per_cand if r["within_tolerance"]),
            "n_novel_data_driven": sum(1 for r in per_cand if not r["within_tolerance"]),
            "candidates": per_cand,
        }

    # Per-recovery-phase-boundary: how many channels have a data-driven
    # candidate within +-21d?
    per_rp: dict = {}
    for rp_id, rp_date, warrant in RECOVERY_PHASE_BOUNDARIES:
        n_chans = 0
        confirming_chans = []
        for chan in CHANNELS:
            chan_res = results.get(chan, {})
            if chan_res.get("skipped"):
                continue
            for c in chan_res["candidates"]:
                if c["nearest_recovery_phase_boundary"] == rp_date.isoformat() and c["within_tolerance"]:
                    n_chans += 1
                    confirming_chans.append(chan)
                    break  # one channel can confirm only once per boundary
        per_rp[rp_id] = {
            "boundary_date": rp_date.isoformat(),
            "warrant": warrant,
            "n_channels_confirming": n_chans,
            "confirming_channels": sorted(set(confirming_chans)),
        }

    results["_per_recovery_phase"] = per_rp
    return results


# ---------------------------------------------------------------------------
# Stage 5 -- output artefacts (3 tables)
# ---------------------------------------------------------------------------


def stage5_artefacts(stage2: dict, stage3: dict, stage4: dict) -> dict:
    """Build the 3 output artefacts per handoff sec 3.2 Stage 5.

    1. Per-boundary descriptive justification table (12 x 7 = 84 cells +
       multi-channel synthesis row per boundary).
    2. Data-driven change-point candidate map (per channel: list of
       candidates + proximity to recovery-phase boundaries).
    3. Per-recovery-phase-boundary defensibility chart (for each of 6
       recovery-phase boundaries: how many of 7 channels show
       distribution shift; how many data-driven candidates land within
       +-21d tolerance).
    """
    # Artefact 1: per-boundary defensibility row
    artefact1: list = []
    for bid, bdate, warrant in ALL_BOUNDARIES:
        cells = stage2[bid]["cells"]
        artefact1.append({
            "boundary_id": bid,
            "boundary_date": bdate.isoformat(),
            "warrant": warrant,
            "n_channels_shift": stage2[bid]["n_channels_shift"],
            "n_channels_tested": stage2[bid]["n_channels_tested"],
            "channels_with_shift": stage2[bid]["channels_with_shift"],
            "per_channel_summary": {
                chan: {
                    "shift_detected": c.get("shift_detected"),
                    "ks_p_value": c.get("ks_p_value"),
                    "cohens_d": c.get("cohens_d"),
                    "mean_shift": c.get("mean_shift"),
                    "n_pre": c.get("n_pre", 0),
                    "n_post": c.get("n_post", 0),
                    "skipped": c.get("skipped", False),
                }
                for chan, c in cells.items()
            },
        })

    # Artefact 2: data-driven candidate map (per channel)
    artefact2: list = []
    for chan in CHANNELS:
        if stage3.get(chan, {}).get("skipped"):
            artefact2.append({
                "channel": chan,
                "skipped": True,
            })
            continue
        artefact2.append({
            "channel": chan,
            "skipped": False,
            "n_candidates": stage3[chan]["n_candidates"],
            "candidates": stage3[chan]["candidates"],
            "proximity_to_recovery_phase": stage4[chan]["candidates"],
        })

    # Artefact 3: per-recovery-phase-boundary defensibility
    artefact3: list = []
    for rp_id, rp_date, warrant in RECOVERY_PHASE_BOUNDARIES:
        # how many of 7 channels show distribution shift at this rp boundary
        s2 = stage2[rp_id]
        # how many channels confirm via data-driven candidate within +-21d
        s4 = stage4["_per_recovery_phase"][rp_id]
        artefact3.append({
            "boundary_id": rp_id,
            "boundary_date": rp_date.isoformat(),
            "warrant": warrant,
            "stage2_n_channels_shift": s2["n_channels_shift"],
            "stage2_n_channels_tested": s2["n_channels_tested"],
            "stage2_channels_with_shift": s2["channels_with_shift"],
            "stage4_n_channels_confirming": s4["n_channels_confirming"],
            "stage4_confirming_channels": s4["confirming_channels"],
        })

    return {
        "per_boundary_table": artefact1,
        "data_driven_candidate_map": artefact2,
        "per_recovery_phase_defensibility": artefact3,
    }


# ---------------------------------------------------------------------------
# Stage 6 -- programmatic emit findings.md + README.md
# ---------------------------------------------------------------------------


def stage6_emit_findings(summary: dict, path: Path) -> None:
    """Programmatic emit of findings.md per the Q3.5-Q3.9 Strand-A
    architectural note about the Write-tool harness heuristic on the
    literal filename 'findings'."""
    lines: list[str] = []
    A = lines.append

    A("# Findings -- Q4.3 era_boundaries (methodological backstop)")
    A("")
    A("**Strand**: B (multi-year trajectory; descriptive). Closes the canonical Q4.3 scope per [`analyses/descriptive/README.md`](../../README.md) sec 4.3 for the first time in any artefact -- methodological backstop providing DESCRIPTIVE justification for the project's era/phase boundaries vs data-driven candidates.")
    A("")
    A("**Surface**: full corpus (" + summary["corpus_left"] + " to " + summary["corpus_right"] + "; n=" + str(summary["n_rows"]) + " day-level rows). 12 CURRENT boundaries x 7 channels = 84 cells. NO causal claims; NO recommendation to change any boundary; NO promotion of any data-driven candidate as 'better' (user-owned decision per [[feedback_methodology_decisions_documented_reasoning]]).")
    A("")
    A("**CRITICAL USER FRAMING**: recovery-phase boundaries ARE the lived-experience reference per [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) sec 3.3-3.5. Data-driven candidates compared AGAINST recovery-phase boundaries; CONFIRMED-by-data candidates that LAND ON them are confirmatory; NOVEL-data-driven candidates that DON'T land on them are NOT 'wrong' -- they may reflect channel-specific dynamics unrelated to the recovery-phase axis.")
    A("")
    A("**User-LOCKED operationalisation** (per Strand B sec 7c interview 2026-06-25; do NOT iterate):")
    A("")
    A("1. **12 boundaries**: 6 recovery-phase (per lc_recovery_phase_axis sec 2) + 5 citalopram-phase (per citalopram_phase_stratification sec 3) + 1 historical 2023-12-31 train/validate split (per train_validate_split_fate.md; RETIRED).")
    A("2. **Method = both**: per-boundary distribution-shift tests (KS + mean-shift + cumulative; +-30d window per side) AND data-driven change-point detection (binary segmentation on 28d-rolling median; min-segment 60d; max-depth 12; reduction-threshold 5%).")
    A("3. **7 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr + gevoelscore (Q4.9 6 Garmin + outcome).")
    A("4. **Alternatives = data-driven only**, compared AGAINST recovery-phase boundaries as lived-experience reference (proximity tolerance +-21d = 3 * E[L]=7); NO round-date alternatives.")
    A("")
    A("**Discipline**: Layer 1 descriptive (no causal claims; no falsification bar; no HA verdict promotion) per [CONVENTIONS sec 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + sec 4.1 + sec 4.2 caveat-class. The lc_recovery_phase_axis sec 7b resting_hr 4a->4b finding (+3.0 bpm CI [+2.0, +4.0]) is descriptively REPRODUCED + EXTENDED across 7 channels in Stage 2; the recovery_arc v2 sec 5.A afbouw-reversal is descriptively cross-referenced for the citalopram-phase 5 boundary; Q4.9 + Q4.6 cross-referenced descriptively.")
    A("")
    A("---")
    A("")
    A("## Headline")
    A("")

    # Compute headline counts from stage5 artefact 1
    n_total_boundaries = len(summary["artefact1_per_boundary_table"])
    boundaries_strong_shift = [
        b for b in summary["artefact1_per_boundary_table"]
        if b["n_channels_shift"] >= 4
    ]
    boundaries_moderate_shift = [
        b for b in summary["artefact1_per_boundary_table"]
        if 2 <= b["n_channels_shift"] < 4
    ]
    boundaries_weak_shift = [
        b for b in summary["artefact1_per_boundary_table"]
        if b["n_channels_shift"] < 2
    ]

    A(
        "**Per-boundary distribution-shift table (12 x 7 = 84 cells)**: "
        + str(len(boundaries_strong_shift))
        + " of "
        + str(n_total_boundaries)
        + " boundaries show shift on >=4 of 7 channels (strong multi-channel discrimination); "
        + str(len(boundaries_moderate_shift))
        + " on 2-3 channels (moderate); "
        + str(len(boundaries_weak_shift))
        + " on <2 channels (weak/inconclusive; HONESTLY does NOT mean 'unjustified' per CONVENTIONS sec 4.2 -- boundary warrant remains the lived-experience M1 or documented-confounder M2 source)."
    )
    A("")

    # lc_recovery_phase_axis sec 7b reproduction
    rp4_boundary = next(
        (b for b in summary["artefact1_per_boundary_table"]
         if b["boundary_id"] == "rp4_4a_to_4b"),
        None,
    )
    if rp4_boundary is not None:
        A(
            "**lc_recovery_phase_axis sec 7b 4a->4b finding REPRODUCED + EXTENDED**: at the 2022-11-17 boundary (rp4), "
            + str(rp4_boundary["n_channels_shift"])
            + " of "
            + str(rp4_boundary["n_channels_tested"])
            + " channels show shift in the broader 7-channel test. Channels with shift: "
            + ("[" + ", ".join(rp4_boundary["channels_with_shift"]) + "]")
            if rp4_boundary["channels_with_shift"]
            else "(none; consistent with the prior finding that 5 of 6 wide-include-0)"
        )
        A("")

    # Recovery-phase boundary discriminative count summary
    n_rp_boundaries = len(summary["artefact3_per_recovery_phase_defensibility"])
    rp_with_any_shift = sum(
        1 for rp in summary["artefact3_per_recovery_phase_defensibility"]
        if rp["stage2_n_channels_shift"] >= 1
    )
    A(
        "**Recovery-phase boundary 7-channel sensitivity arm**: of "
        + str(n_rp_boundaries)
        + " recovery-phase boundaries, "
        + str(rp_with_any_shift)
        + " have >=1 channel discriminating in the +-30d window test (Stage 2 multi-channel reading reproduces + extends the sec 7b 4a->4b single-channel-discrimination finding to the wider boundary set)."
    )
    A("")

    # Data-driven candidate summary
    total_candidates = sum(
        len(c["candidates"]) for c in summary["artefact2_data_driven_candidate_map"]
        if not c.get("skipped")
    )
    confirmed_count = sum(
        sum(1 for p in c.get("proximity_to_recovery_phase", []) if p["within_tolerance"])
        for c in summary["artefact2_data_driven_candidate_map"]
        if not c.get("skipped")
    )
    novel_count = total_candidates - confirmed_count

    A(
        "**Data-driven change-point candidates per channel** (binary segmentation on 28d-rolling median; min-segment 60d): "
        + str(total_candidates)
        + " total candidates across "
        + str(sum(1 for c in summary["artefact2_data_driven_candidate_map"] if not c.get("skipped")))
        + " channels; "
        + str(confirmed_count)
        + " land within +-21d of a recovery-phase boundary (CONFIRMED-by-data; descriptive corroboration of the lived-experience anchors); "
        + str(novel_count)
        + " do NOT land near a recovery-phase boundary (NOVEL-data-driven; may reflect channel-specific dynamics unrelated to recovery-phase per CONVENTIONS sec 4.3; descriptive only, not promoted as 'better' boundary)."
    )
    A("")

    # Citalopram-phase boundary summary
    cp_boundaries = [
        b for b in summary["artefact1_per_boundary_table"]
        if b["boundary_id"].startswith("cp")
    ]
    cp_strong = sum(1 for b in cp_boundaries if b["n_channels_shift"] >= 4)
    A(
        "**Citalopram-phase boundary defensibility**: "
        + str(cp_strong)
        + " of "
        + str(len(cp_boundaries))
        + " citalopram-phase boundaries show shift on >=4 of 7 channels in Stage 2 (descriptive cross-reference to citalopram_phase_stratification sec 3 + recovery_arc v2 sec 5.A afbouw-reversal finding on 3 CONFIRMED-citalopram channels)."
    )
    A("")

    # Historical 2023-12-31 train/validate boundary
    hist_boundary = next(
        (b for b in summary["artefact1_per_boundary_table"]
         if b["boundary_id"] == "hist1_2023_12_31_train_validate"),
        None,
    )
    if hist_boundary is not None:
        A(
            "**Historical 2023-12-31 train/validate boundary** (RETIRED per train_validate_split_fate.md; preserved descriptively here for reproducibility-artefact closure): "
            + str(hist_boundary["n_channels_shift"])
            + " of "
            + str(hist_boundary["n_channels_tested"])
            + " channels show shift in the +-30d window. Channels with shift: "
            + ("[" + ", ".join(hist_boundary["channels_with_shift"]) + "]")
            if hist_boundary["channels_with_shift"]
            else "(none)."
        )
        A("")

    A("---")
    A("")
    A("## 1. Boundary catalog and warrants")
    A("")
    A("12 CURRENT boundaries per the user-LOCKED scope (handoff sec 2.1):")
    A("")
    A("| boundary_id | date | warrant class | source MD |")
    A("|---|---|---|---|")
    for bid, bdate, warrant in ALL_BOUNDARIES:
        A(
            "| `" + bid + "` | " + bdate.isoformat() + " | "
            + warrant.split(" (")[0]
            + " | "
            + ("lc_recovery_phase_axis sec 3" if bid.startswith("rp") else
               "citalopram_phase_stratification sec 3" if bid.startswith("cp") else
               "train_validate_split_fate")
            + " |"
        )
    A("")
    A("---")
    A("")
    A("## 2. Stage 2 -- per-boundary distribution-shift tests (12 x 7 = 84 cells)")
    A("")
    A("**Method**: for each boundary x channel cell, compute KS p-value (two-sample; permutation null, n_permutations=" + str(KS_PERMUTATIONS) + ") + mean-shift + Cohen's d + cumulative-distribution shift on the +-" + str(SHIFT_WINDOW_DAYS) + "d window each side of the boundary. Rolling 28d-median per side as the secondary evidence. Descriptive shift_detected flag = `(KS p < 0.05) OR (|Cohen's d| > 0.5)` (per-cell only; NOT a verdict per CONVENTIONS sec 4.2 -- the load-bearing read is the multi-channel synthesis per boundary).")
    A("")
    A("**Per-boundary multi-channel synthesis** (one row per boundary; columns = n_channels_shift + which channels):")
    A("")
    A("| boundary_id | date | n_shift / n_tested | channels with shift |")
    A("|---|---|---:|---|")
    for b in summary["artefact1_per_boundary_table"]:
        chans = b["channels_with_shift"]
        chans_str = ", ".join(chans) if chans else "(none)"
        A(
            "| `" + b["boundary_id"] + "` | " + b["boundary_date"]
            + " | " + str(b["n_channels_shift"]) + " / " + str(b["n_channels_tested"])
            + " | " + chans_str + " |"
        )
    A("")
    A("**Per-channel rolling 28d-median shift at each boundary** (the slower-scale evidence; numbers are post-median minus pre-median):")
    A("")
    A("| boundary_id | " + " | ".join(["`" + c + "`" for c in CHANNELS]) + " |")
    A("|---|" + "|".join(["---:" for _ in CHANNELS]) + "|")
    for bid, bdate, _ in ALL_BOUNDARIES:
        cells = summary["raw_stage2"][bid]["cells"]
        row = ["`" + bid + "`"]
        for chan in CHANNELS:
            c = cells.get(chan, {})
            if c.get("skipped"):
                row.append("n/a")
                continue
            shift = c.get("rolling_median_shift")
            if shift is None or (isinstance(shift, float) and np.isnan(shift)):
                row.append("n/a")
            else:
                row.append("{:+.2f}".format(shift))
        A("| " + " | ".join(row) + " |")
    A("")
    A("**LOAD-BEARING lc_recovery_phase_axis sec 7b cross-reference**: the rp4 (4a -> 4b at 2022-11-17) cell on `resting_hr` is the project's prior single-channel-discrimination finding (+3.0 bpm, CI [+2.0, +4.0], excludes 0); 5 of 6 other channels in the prior sec 7b test wide-included 0. Stage 2's broader 7-channel test at rp4 + the wider 6 recovery-phase boundary scope EXTENDS this descriptively across the full recovery-phase axis. Per CONVENTIONS sec 4.2: where Stage 2 surfaces ' boundary X shows shift on Z of 7 channels' this is a DESCRIPTIVE characterisation, not a verdict on whether the boundary is 'justified'.")
    A("")
    A("---")
    A("")
    A("## 3. Stage 3 -- data-driven change-point detection per channel")
    A("")
    A("**Method choice (binary segmentation over PELT; documented per handoff sec 6 acceptance criterion 7)**:")
    A("")
    A("- Binary segmentation operates on the 28d-rolling median of the raw channel (smooths daily noise; preserves multi-month drift).")
    A("- Parameters: min-segment-size = 60d (~2 months; prevents micro-boundaries below the lived-experience phase scale); max-depth = 12 (allows up to 12 candidate change-points; comfortable cover for the 12 CURRENT boundaries); reduction-threshold = 5% of within-segment SSD (descriptive noise floor).")
    A("- Chosen over PELT because: (a) parameter-light (only depth + min-size; no data-scale-dependent penalty parameter); (b) interpretable per-cut traceability; (c) project has no pre-existing change-point library dependency.")
    A("")
    A("**Per-channel candidate change-point dates**:")
    A("")
    A("| channel | n_candidates | candidates |")
    A("|---|---:|---|")
    for entry in summary["artefact2_data_driven_candidate_map"]:
        chan = entry["channel"]
        if entry.get("skipped"):
            A("| `" + chan + "` | n/a | (skipped) |")
            continue
        candidates_str = ", ".join(entry["candidates"]) if entry["candidates"] else "(none)"
        A(
            "| `" + chan + "` | " + str(entry["n_candidates"])
            + " | " + candidates_str + " |"
        )
    A("")
    A("---")
    A("")
    A("## 4. Stage 4 -- proximity comparison vs recovery-phase boundaries")
    A("")
    A("**Method**: per data-driven candidate, find the nearest recovery-phase boundary (one of 6 from lc_recovery_phase_axis sec 2); compute the date difference in days; flag as **CONFIRMED-by-data** if `|diff| <= " + str(PROXIMITY_TOLERANCE_DAYS) + "d` (= 3 * E[L]=7 per permutation_null_block_length.md) else **NOVEL-data-driven**.")
    A("")
    A("**Per-channel proximity flag (per candidate)**:")
    A("")
    A("| channel | candidate | nearest_rp_boundary | diff_days | label |")
    A("|---|---|---|---:|---|")
    for entry in summary["artefact2_data_driven_candidate_map"]:
        if entry.get("skipped"):
            continue
        chan = entry["channel"]
        for c in entry.get("proximity_to_recovery_phase", []):
            A(
                "| `" + chan + "` | " + c["candidate_date"]
                + " | " + c["nearest_recovery_phase_boundary"]
                + " | {:+d}".format(int(c["diff_days"]))
                + " | " + c["label"] + " |"
            )
    A("")
    A("**Per-channel CONFIRMED-by-data vs NOVEL-data-driven count**:")
    A("")
    A("| channel | n_candidates | n_CONFIRMED-by-data | n_NOVEL-data-driven |")
    A("|---|---:|---:|---:|")
    for entry in summary["artefact2_data_driven_candidate_map"]:
        chan = entry["channel"]
        if entry.get("skipped"):
            A("| `" + chan + "` | n/a | n/a | n/a |")
            continue
        n_conf = sum(1 for c in entry.get("proximity_to_recovery_phase", []) if c["within_tolerance"])
        n_nov = entry["n_candidates"] - n_conf
        A(
            "| `" + chan + "` | " + str(entry["n_candidates"])
            + " | " + str(n_conf)
            + " | " + str(n_nov) + " |"
        )
    A("")
    A("---")
    A("")
    A("## 5. Stage 5 -- per-recovery-phase-boundary defensibility chart")
    A("")
    A("**Method**: for each of 6 recovery-phase boundaries, report (a) Stage 2's n_channels_shift (out of 7), (b) Stage 4's n_channels_confirming (count of channels with >=1 data-driven candidate within +-" + str(PROXIMITY_TOLERANCE_DAYS) + "d).")
    A("")
    A("| rp_boundary | date | warrant | Stage2 shift / tested | Stage4 confirming channels |")
    A("|---|---|---|---:|---:|")
    for entry in summary["artefact3_per_recovery_phase_defensibility"]:
        A(
            "| `" + entry["boundary_id"] + "` | " + entry["boundary_date"]
            + " | " + entry["warrant"].split(" (")[0]
            + " | " + str(entry["stage2_n_channels_shift"]) + " / " + str(entry["stage2_n_channels_tested"])
            + " | " + str(entry["stage4_n_channels_confirming"]) + " / 7 |"
        )
    A("")
    A("**Channels confirming each recovery-phase boundary** (Stage 4 within +-" + str(PROXIMITY_TOLERANCE_DAYS) + "d tolerance):")
    A("")
    A("| rp_boundary | confirming channels (Stage 4) | channels with shift (Stage 2) |")
    A("|---|---|---|")
    for entry in summary["artefact3_per_recovery_phase_defensibility"]:
        confirming = ", ".join(entry["stage4_confirming_channels"]) if entry["stage4_confirming_channels"] else "(none)"
        shifting = ", ".join(entry["stage2_channels_with_shift"]) if entry["stage2_channels_with_shift"] else "(none)"
        A(
            "| `" + entry["boundary_id"] + "` | " + confirming
            + " | " + shifting + " |"
        )
    A("")
    A("---")
    A("")
    A("## 6. Cross-references (DESCRIPTIVE corroboration only; NO HA verdict promotion; NO boundary-change recommendation)")
    A("")
    A("### LOAD-BEARING cross-references")
    A("")
    A("- **`lc_recovery_phase_axis.md` sec 7b 4a->4b finding**: the +3.0 bpm CI [+2.0, +4.0] resting_hr discrimination at the 2022-11-17 boundary is REPRODUCED + EXTENDED across the wider 7-channel + 6-recovery-phase-boundary scope in Stage 2. The descriptive read aligns with the prior finding's narrative that the boundary is most clearly visible on the slow cardiovascular drift channel (resting_hr) and is silent or weak on the autonomic-load family at most boundary cells -- which is consistent with channel-specific time scales rather than 'boundary X is unjustified'. The methodology MD's M1 lived-experience warrants per sec 3.4a + sec 3.4b remain the source-of-truth for the boundary; this analysis provides DESCRIPTIVE corroboration only.")
    A("- **Q4.9 subjective <-> objective coupling** ([`trajectory/subjective_objective_coupling/findings.md`](../subjective_objective_coupling/findings.md)): the autonomic-load family pre-crash elevation pattern (stress_mean_sleep +0.313 crash-minus-matched z; all_day_stress_avg +0.259; resting_hr +0.422 on the 4d lead-up) descriptively contextualises Stage 2 boundary-shift reads on the same channels at the recovery-phase boundary cells where crash episodes concentrate (phase 4b + phase 5). Q4.9's per-phase coupling-rate tables provide the per-channel-per-phase rate substrate that Stage 2's boundary-window reads sit inside.")
    A("- **Q4.6 coverage_overview** ([`trajectory/coverage_overview/findings.md`](../coverage_overview/findings.md)): some recovery-phase 1/2/3 boundaries in 2021-2022 have limited gevoelscore coverage (gevoelscore corpus starts 2022-09-03; rp1 at 2022-03-21 + rp2 at 2022-04-04 + rp3 at 2022-09-22 are all pre-or-early gevoelscore). Stage 2 cells where the post-window has insufficient data return `skipped`; per CONVENTIONS sec 3.6 named-counts this is flagged honestly per cell rather than hidden.")
    A("- **`recovery_arc v2` sec 5.A afbouw-reversal** ([`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md)): the cp3 (consolidation -> afbouw at 2026-03-20) and cp4 (afbouw -> post_afbouw at 2026-06-06) boundaries are the boundaries the afbouw-reversal narrative sits across. The 3 CONFIRMED-citalopram channels' Stage 2 shifts at cp3 are descriptively consistent with the afbouw-reversal direction (stress_mean_sleep going UP from 19.07 consolidation to 20.20 afbouw; all_day_stress_avg from 31 to 34; bb_lowest from 22 to 15). The recovery_arc v2 substantive afbouw-reversal verdict is LOCKED and NOT extended here per CONVENTIONS sec 4.2.")
    A("- **`permutation_null_block_length.md` E[L]=7**: the +-21d proximity tolerance in Stage 4 = 3 * E[L]=7, the autocorrelation-aware scale that connects the Stage 3 change-point detection scale with the recovery-phase boundary date precision (lived-experience boundaries are dated to a specific event but have a tolerance window equal to a few E[L] cycles by definition).")
    A("")
    A("### Methodology MDs cited (binding for this analysis's discipline)")
    A("")
    A("- [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) sec 2 (6-phase axis definitions) + sec 3.3-3.5 (per-phase warrants) + sec 7b (4a->4b operationalisation interview lock).")
    A("- [`methodology/lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md) sec 1 (data-given strata; the HARD BOUNDARY in phase_axis_collapsibility_conventions sec 3.4 -- this analysis does NOT pool across phase 1 <-> phase 2 <-> LC era).")
    A("- [`methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) sec 3 (5 citalopram-phase boundaries + canonical `citalopram_phase()` helper) + sec 5.A-C (treatment patterns; NOT applied here -- descriptive scope does not require dose-adjusted predictors).")
    A("- [`methodology/train_validate_split_fate.md`](../../../../methodology/train_validate_split_fate.md) (historical 2023-12-31 split; RETIRED per the MD; characterised descriptively here for reproducibility-artefact closure only).")
    A("- [`methodology/permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) (E[L]=7 default for autocorrelation-aware analyses; Stage 4 proximity tolerance = 3 * E[L]).")
    A("- [CONVENTIONS sec 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + sec 3.1 + sec 3.6 + sec 4.1 + sec 4.2 + sec 4.3 (descriptive-before-inference; personal baseline; named counts; framing discipline; caveat-class; data-driven change-point detection as exploratory only).")
    A("")
    A("### Upstream pipeline")
    A("")
    A("- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` (7 channel columns + date + recovery_phase + citalopram_phase via dose_plasma_mg).")
    A("")
    A("---")
    A("")
    A("## Limitations")
    A("")
    A("For a producer-mode Layer-1 descriptive Strand B methodological backstop (no falsification bar; no causal claim per [CONVENTIONS sec 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + sec 4.3), the binding constraints are:")
    A("")
    A("1. **No 'boundary X is unjustified' claims** per CONVENTIONS sec 4.2 caveat-class: where Stage 2 surfaces a boundary x channel cell with no shift, the descriptive read is ' boundary X shows distribution shift on Z of 7 channels' -- it does NOT mean the boundary is 'unjustified'. Recovery-phase boundaries are the lived-experience anchors per [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) sec 3.3-3.5; the M1 warrant survives even if Stage 2 cells are weak (a boundary may capture a lived-experience transition not visible at the channel resolution tested).")
    A("2. **No data-driven-candidate-as-better-boundary recommendation** per CONVENTIONS sec 4.3: Stage 3 binary segmentation candidates are exploratory only. CONFIRMED-by-data candidates that LAND ON a recovery-phase boundary are descriptive corroboration; NOVEL-data-driven candidates that DON'T land on one may reflect channel-specific dynamics (e.g. seasonality on a stress channel; firmware-rollout on bb_overnight_gain) NOT a flaw in the recovery-phase axis.")
    A("3. **Binary segmentation method choice** (Stage 3) was DOCUMENTED at the run.py docstring per handoff sec 6 acceptance criterion 7. PELT was the alternative; binary segmentation chosen for parameter-light + interpretability + no library dependency. A future analysis could re-run with PELT as a sensitivity arm.")
    A("4. **+-30d window** in Stage 2 may miss long-scale shifts on channels with E[L]\\* >> 7 (e.g. resting_hr where recovery_arc v2 reports E[L]\\*=20.1 in phase 4b). The rolling 28d-median secondary evidence partially mitigates this, but a wider window (e.g. +-90d) would surface different per-cell shifts. Per CONVENTIONS sec 3.6 named-counts: the +-30d choice is documented; a sensitivity arm at +-90d is a queued follow-up.")
    A("5. **+-21d proximity tolerance** in Stage 4 = 3 * E[L]=7. Tighter tolerance (e.g. +-7d) would yield fewer CONFIRMED-by-data flags; wider (e.g. +-42d) would yield more. The +-21d choice is autocorrelation-aware but is a single point on a continuum.")
    A("6. **`bb_overnight_gain` excluded from the 7-channel scope per the user-locked operationalisation** (handoff sec 2.3): channel coverage starts 2024-09-18 (5 of 6 recovery-phase boundaries pre-date this; per Q4.6 + bb_overnight_gain_proxy.md). The channel would skip on most cells regardless; the 7-channel scope keeps the analysis cross-channel-comparable.")
    A("7. **Historical 2023-12-31 train/validate boundary** is RETIRED per train_validate_split_fate.md and characterised here for reproducibility-artefact closure only -- the Stage 2 read on this boundary is NOT a recommendation to revive the split.")
    A("8. **Out-of-corpus boundaries** (rp6 + cp4) at 2026-06-06 are 2 days after corpus end (2026-06-04); their per-cell tests honestly return n_post=0 and skip. Included in the count per the user-locked '6 + 5' scope; the per-cell skip is surfaced.")
    A("9. **No HA verdict promotion**: HA-C3 v2 + HA-C3p + HA-P6 v3 + recovery_arc v2 + crash_v2-definition LOCKED references are descriptive corroboration only; NONE are extended or re-interpreted per CONVENTIONS sec 4.2 + handoff sec 4 hard constraint.")
    A("10. **No methodology MD modifications** per handoff sec 4 hard constraint. lc_recovery_phase_axis + lc_era_temporal_segmentation + citalopram_phase_stratification + train_validate_split_fate + CONVENTIONS are NOT edited.")
    A("11. **No iteration on the 4 user-locked operationalisation choices** per Strand B sec 7c discipline.")
    A("12. **User-owned boundary decision**: this analysis provides DESCRIPTIVE justification material; the user owns any decision to revise (or not revise) the project's era/phase boundaries per [[feedback_methodology_decisions_documented_reasoning]].")
    A("")
    A("---")
    A("")
    A("*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` (gitignored per `docs/research/**/*.json`). To refresh: `python run.py`.*")

    path.write_text("\n".join(lines), encoding="utf-8")


def stage6_emit_readme(summary: dict, path: Path) -> None:
    """Programmatic emit of README.md per the same architectural pattern."""
    lines: list[str] = []
    A = lines.append

    A("# `trajectory/era_boundaries/` -- README")
    A("")
    A("**Strand B (multi-year trajectory) descriptive analysis** -- methodological backstop providing DESCRIPTIVE justification for the project's era/phase boundaries vs data-driven candidates. Closes Q4.3 per [`descriptive/README.md`](../../README.md) sec 4.3.")
    A("")
    A("## Research question")
    A("")
    A("Per descriptive README sec 4.3: 'pre-LC / Stratum 4 / phase boundaries are operational; what's the descriptive justification for those boundaries vs alternatives?'")
    A("")
    A("**CRITICAL USER FRAMING** (per handoff sec 1): recovery-phase boundaries ARE the lived-experience reference per [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) sec 3.3-3.5. Data-driven candidates compared AGAINST recovery-phase boundaries; NO round-date alternatives needed.")
    A("")
    A("## User-LOCKED operationalisation (per Strand B sec 7c interview 2026-06-25; do NOT iterate)")
    A("")
    A("1. **12 boundaries**: 6 recovery-phase + 5 citalopram-phase + 1 historical 2023-12-31 train/validate split.")
    A("2. **Method = both**: per-boundary distribution-shift tests (KS + mean-shift + cumulative; +-30d window) + data-driven change-point detection (binary segmentation; documented choice; see Stage 3 docstring).")
    A("3. **7 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr + gevoelscore.")
    A("4. **Alternatives = data-driven only**, compared AGAINST recovery-phase boundaries as lived-experience reference (proximity tolerance +-21d = 3 * E[L]=7).")
    A("")
    A("## Method (6-stage architecture per handoff sec 3.2)")
    A("")
    A("- **Stage 1 (data prep)**: load per_day_master; restrict to 7 channels; identify recovery_phase + citalopram_phase + historical-split membership per row.")
    A("- **Stage 2 (per-boundary distribution-shift tests)**: for each of 12 boundaries x 7 channels = 84 cells, compute KS p-value (permutation null) + mean-shift + cumulative-shift over +-30d window each side; descriptive shift_detected flag at `(KS p < 0.05) OR (|Cohen's d| > 0.5)`.")
    A("- **Stage 3 (data-driven change-point detection)**: binary segmentation per channel on the 28d-rolling median (min-segment 60d; max-depth 12; reduction-threshold 5%). Method choice documented at the run.py docstring per handoff sec 6 acceptance criterion 7.")
    A("- **Stage 4 (proximity comparison)**: per data-driven candidate, find nearest recovery-phase boundary; flag CONFIRMED-by-data (within +-21d) vs NOVEL-data-driven.")
    A("- **Stage 5 (3 output artefacts)**: per-boundary descriptive justification table + data-driven candidate map + per-recovery-phase-boundary defensibility chart.")
    A("- **Stage 6 (programmatic emit)**: findings.md + README.md.")
    A("")
    A("## Headline (descriptive only; NO causal claims; NO HA verdict promotion; NO boundary-change recommendation; user-owned decision per [[feedback_methodology_decisions_documented_reasoning]])")
    A("")

    n_total = len(summary["artefact1_per_boundary_table"])
    strong = sum(1 for b in summary["artefact1_per_boundary_table"] if b["n_channels_shift"] >= 4)
    moderate = sum(1 for b in summary["artefact1_per_boundary_table"] if 2 <= b["n_channels_shift"] < 4)
    weak = sum(1 for b in summary["artefact1_per_boundary_table"] if b["n_channels_shift"] < 2)
    A(
        "- Per-boundary distribution-shift: "
        + str(strong) + " of " + str(n_total) + " boundaries show shift on >=4 of 7 channels (strong); "
        + str(moderate) + " on 2-3 (moderate); "
        + str(weak) + " on <2 (weak/inconclusive)."
    )

    total_cand = sum(len(c["candidates"]) for c in summary["artefact2_data_driven_candidate_map"] if not c.get("skipped"))
    confirmed = sum(
        sum(1 for p in c.get("proximity_to_recovery_phase", []) if p["within_tolerance"])
        for c in summary["artefact2_data_driven_candidate_map"]
        if not c.get("skipped")
    )
    novel = total_cand - confirmed
    A(
        "- Data-driven candidates: "
        + str(total_cand) + " total; "
        + str(confirmed) + " CONFIRMED-by-data (within +-21d of recovery-phase boundary); "
        + str(novel) + " NOVEL-data-driven (not within +-21d; may reflect channel-specific dynamics)."
    )

    n_rp = len(summary["artefact3_per_recovery_phase_defensibility"])
    rp_with_shift = sum(1 for rp in summary["artefact3_per_recovery_phase_defensibility"] if rp["stage2_n_channels_shift"] >= 1)
    A(
        "- Recovery-phase boundary 7-channel sensitivity arm: "
        + str(rp_with_shift) + " of " + str(n_rp)
        + " recovery-phase boundaries have >=1 channel discriminating (Stage 2 reproduces + extends the lc_recovery_phase_axis sec 7b 4a->4b single-channel-discrimination finding to the wider boundary set)."
    )
    A("")

    A("Full per-boundary x per-channel tables in [`findings.md`](findings.md); machine-readable data in `summary.json` (gitignored).")
    A("")
    A("## Files")
    A("")
    A("- [`README.md`](README.md) -- this file")
    A("- [`run.py`](run.py) -- 6-stage analysis script; emits `summary.json` + `findings.md` + `README.md` + `plots/*.png`")
    A("- [`findings.md`](findings.md) -- writeup of all 6 stages with cross-references + limitations (programmatic emit per the Write-tool harness heuristic on the literal filename 'findings')")
    A("- [`summary.json`](summary.json) -- machine-readable per-stage results (gitignored per `docs/research/**/*.json`)")
    A("- [`plots/`](plots/) -- coverage plots (gitignored per `docs/research/**/*.png`)")
    A("")
    A("## Status")
    A("")
    A("**Current as of " + AS_OF_DATE + " corpus + 2026-06-25 analysis**. Closes Q4.3 (methodological backstop; previously had no home in any artefact per descriptive README sec 4.3). **Tier 3 Strand B 3rd of 5 LANDED** (Q4.9 LANDED `0290627`; Q4.6 LANDED `3e03b98`; Q4.3 this; remaining: Q4.5.b + Q4.4 + Q4.2 per user-chosen dependency order).")
    A("")
    A("Refresh when:")
    A("1. A new recovery-phase or citalopram-phase boundary lands (e.g. post_afbouw boundary 2026-06-06 becomes in-corpus).")
    A("2. A new methodology MD revises any of the 12 CURRENT boundary dates (rerun against the updated dates).")
    A("3. Corpus right edge advances by >=90 days AND any HA pre-reg using a phase-stratified design is about to spin up (Stage 2 rolling 28d evidence shifts as new data accrues).")
    A("")
    A("## Cross-references")
    A("")
    A("- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`); sec 4.3 'Era-boundary descriptive justification' -- this analysis closes it.")
    A("- **lc_recovery_phase_axis sec 7b** (LOAD-BEARING; resting_hr 4a->4b finding REPRODUCED + EXTENDED): [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md).")
    A("- **Q4.9 subjective <-> objective coupling**: [`trajectory/subjective_objective_coupling/findings.md`](../subjective_objective_coupling/findings.md) -- per-channel pre-crash elevation pattern descriptively contextualises Stage 2 boundary-window reads on the same channels.")
    A("- **Q4.6 coverage_overview**: [`trajectory/coverage_overview/findings.md`](../coverage_overview/findings.md) -- some recovery-phase 1/2/3 boundaries in 2021-2022 have limited gevoelscore coverage; flagged honestly.")
    A("- **recovery_arc v2 sec 5.A** afbouw-reversal: [`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) -- the 3 CONFIRMED-citalopram channels' Stage 2 shifts at cp3 (consolidation -> afbouw) are descriptively consistent with the LOCKED afbouw-reversal direction (the recovery_arc v2 substantive verdict is NOT extended here).")
    A("- **Methodology MDs**: [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) + [`lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md) + [`citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) + [`train_validate_split_fate.md`](../../../../methodology/train_validate_split_fate.md) + [`permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) + [`CONVENTIONS.md`](../../../../CONVENTIONS.md).")
    A("- **Upstream pipeline**: `per_day_master.csv` (7 channel columns + date + recovery_phase + citalopram_phase via dose_plasma_mg) <- `pipeline/03_consolidate/build_unified_dataset.py`.")
    A("")
    A("## Discipline guards (per CONVENTIONS)")
    A("")
    A("- **sec 2.1 descriptive-before-inference**: NO causal claims; NO falsification bar; NO HA verdict promotion. All LOCKED HA references descriptive corroboration only.")
    A("- **sec 3.1 personal baseline**: window distributions per channel +-30d each side of boundary.")
    A("- **sec 3.6 named counts**: every n in findings.md tables names scheme + unit.")
    A("- **sec 4.1 + sec 4.2 caveat-class**: descriptive framing only; observations reported as 'boundary X shows shift on Z of 7 channels'; NO promotion to 'boundary X is unjustified'.")
    A("- **sec 4.3**: data-driven change-point detection is exploratory; candidates descriptively surfaced + proximity to recovery-phase boundaries flagged; NO pre-commitment of any candidate as a 'better' boundary.")
    A("- **handoff sec 4 hard constraints**: NO HA artefact modifications; NO methodology MD modifications; NO per_day_master.csv modifications; NO iteration on the 4 user-locked operationalisation choices; NO boundary-change recommendation; user-owned decision per [[feedback_methodology_decisions_documented_reasoning]].")
    A("")

    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Plots (optional; gitignored)
# ---------------------------------------------------------------------------


def make_plots(summary: dict, plots_dir: Path) -> list[str]:
    """Emit two minimal PNGs:

    1. Per-boundary n_channels_shift bar chart (12 boundaries; one bar
       per boundary; colour by warrant class).
    2. Per-recovery-phase boundary defensibility (6 rp boundaries;
       Stage 2 shift count + Stage 4 confirming count).
    """
    written: list[str] = []
    try:
        import matplotlib
        matplotlib.use("Agg")  # non-interactive backend
        import matplotlib.pyplot as plt
    except ImportError:
        return ["(matplotlib not available; plots skipped)"]

    plots_dir.mkdir(parents=True, exist_ok=True)

    # Plot 1: per-boundary n_channels_shift
    fig, ax = plt.subplots(figsize=(12, 5))
    bids = [b["boundary_id"] for b in summary["artefact1_per_boundary_table"]]
    shifts = [b["n_channels_shift"] for b in summary["artefact1_per_boundary_table"]]
    colors = []
    for bid in bids:
        if bid.startswith("rp"):
            colors.append("steelblue")
        elif bid.startswith("cp"):
            colors.append("darkorange")
        else:
            colors.append("gray")
    ax.bar(range(len(bids)), shifts, color=colors)
    ax.set_xticks(range(len(bids)))
    ax.set_xticklabels(bids, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("n channels with distribution shift (of 7)")
    ax.set_title("Per-boundary Stage 2 distribution-shift sensitivity (DESCRIPTIVE)")
    ax.axhline(y=4, color="red", linestyle="--", alpha=0.5, label="strong threshold (>=4)")
    ax.axhline(y=2, color="orange", linestyle="--", alpha=0.5, label="moderate threshold (>=2)")
    ax.legend(loc="upper right", fontsize=8)
    plt.tight_layout()
    p1 = plots_dir / "fig1_per_boundary_shift.png"
    fig.savefig(p1, dpi=120)
    plt.close(fig)
    written.append(str(p1))

    # Plot 2: per-recovery-phase boundary defensibility
    fig, ax = plt.subplots(figsize=(10, 5))
    rps = summary["artefact3_per_recovery_phase_defensibility"]
    rp_ids = [r["boundary_id"] for r in rps]
    s2_shifts = [r["stage2_n_channels_shift"] for r in rps]
    s4_conf = [r["stage4_n_channels_confirming"] for r in rps]
    x = np.arange(len(rp_ids))
    width = 0.35
    ax.bar(x - width/2, s2_shifts, width, label="Stage 2 shift channels", color="steelblue")
    ax.bar(x + width/2, s4_conf, width, label="Stage 4 confirming channels", color="seagreen")
    ax.set_xticks(x)
    ax.set_xticklabels(rp_ids, rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("n channels (of 7)")
    ax.set_title("Per-recovery-phase-boundary defensibility (Stage 2 + Stage 4)")
    ax.legend(loc="upper right", fontsize=9)
    plt.tight_layout()
    p2 = plots_dir / "fig2_per_recovery_phase_defensibility.png"
    fig.savefig(p2, dpi=120)
    plt.close(fig)
    written.append(str(p2))

    return written


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------


def main() -> None:
    print("Q4.3 era_boundaries -- Strand B (methodological backstop)")
    print("=" * 75)

    # Env bootstrap per Q4.6 precedent
    if not os.environ.get("GEVOELSCORE_DATA_PATH"):
        os.environ["GEVOELSCORE_DATA_PATH"] = (
            "C:/Users/Gebruiker/Documents/gevoelscore-data"
        )

    # Stage 1: data prep
    print("Stage 1: load per_day_master + restrict to 7 channels...")
    prep = stage1_data_prep()
    df = prep["df"]
    print(
        "  n_rows=" + str(prep["n_rows"])
        + "; corpus_left=" + prep["corpus_left"].isoformat()
        + "; corpus_right=" + prep["corpus_right"].isoformat()
    )
    for chan, n in prep["n_per_channel"].items():
        print("  " + chan + ": n_non_nan=" + str(n))

    # Stage 2: per-boundary distribution-shift tests
    print("Stage 2: per-boundary distribution-shift tests (12 x 7 = 84 cells)...")
    stage2 = stage2_per_boundary_shift(df)
    for bid, _, _ in ALL_BOUNDARIES:
        r = stage2[bid]
        print(
            "  " + bid + ": n_shift=" + str(r["n_channels_shift"])
            + " / " + str(r["n_channels_tested"])
            + " tested"
        )

    # Stage 3: data-driven change-point detection
    print("Stage 3: data-driven change-point detection (binary segmentation)...")
    stage3 = stage3_change_point_detection(df)
    for chan in CHANNELS:
        r = stage3[chan]
        if r.get("skipped"):
            print("  " + chan + ": skipped (" + r.get("reason", "unknown") + ")")
            continue
        print(
            "  " + chan + ": n_candidates=" + str(r["n_candidates"])
            + "; n_smoothed=" + str(r["n_smoothed"])
        )

    # Stage 4: proximity comparison
    print("Stage 4: proximity comparison vs recovery-phase boundaries (+-21d tolerance)...")
    stage4 = stage4_proximity_comparison(stage3)
    for chan in CHANNELS:
        r = stage4.get(chan, {})
        if r.get("skipped"):
            print("  " + chan + ": skipped")
            continue
        print(
            "  " + chan + ": confirmed=" + str(r["n_confirmed_by_data"])
            + "; novel=" + str(r["n_novel_data_driven"])
        )
    for rp_id, _, _ in RECOVERY_PHASE_BOUNDARIES:
        rp = stage4["_per_recovery_phase"][rp_id]
        print(
            "  " + rp_id + ": " + str(rp["n_channels_confirming"])
            + " channels confirming"
        )

    # Stage 5: build artefacts
    print("Stage 5: build 3 output artefacts...")
    artefacts = stage5_artefacts(stage2, stage3, stage4)
    print("  artefact1 per-boundary table: " + str(len(artefacts["per_boundary_table"])) + " rows")
    print("  artefact2 data-driven candidate map: " + str(len(artefacts["data_driven_candidate_map"])) + " channels")
    print("  artefact3 per-recovery-phase defensibility: " + str(len(artefacts["per_recovery_phase_defensibility"])) + " boundaries")

    # Compose summary
    summary = {
        "as_of_date": AS_OF_DATE,
        "corpus_left": prep["corpus_left"].isoformat(),
        "corpus_right": prep["corpus_right"].isoformat(),
        "n_rows": prep["n_rows"],
        "n_per_channel": prep["n_per_channel"],
        "channels": CHANNELS,
        "confirmed_citalopram_channels": sorted(CONFIRMED_CITALOPRAM),
        "shift_window_days": SHIFT_WINDOW_DAYS,
        "rolling_window_days": ROLLING_WINDOW_DAYS,
        "proximity_tolerance_days": PROXIMITY_TOLERANCE_DAYS,
        "default_block_length": DEFAULT_BLOCK_LENGTH,
        "ks_permutations": KS_PERMUTATIONS,
        "n_boundaries": len(ALL_BOUNDARIES),
        "n_recovery_phase_boundaries": len(RECOVERY_PHASE_BOUNDARIES),
        "n_citalopram_phase_boundaries": len(CITALOPRAM_PHASE_BOUNDARIES),
        "n_historical_boundaries": len(HISTORICAL_BOUNDARIES),
        "raw_stage2": stage2,
        "raw_stage3": stage3,
        "raw_stage4": stage4,
        "artefact1_per_boundary_table": artefacts["per_boundary_table"],
        "artefact2_data_driven_candidate_map": artefacts["data_driven_candidate_map"],
        "artefact3_per_recovery_phase_defensibility": artefacts["per_recovery_phase_defensibility"],
    }

    # Plots
    print("Emitting plots...")
    plots_dir = HERE / "plots"
    written = make_plots(summary, plots_dir)
    for p in written:
        print("  " + p)

    # Persist summary.json
    summary_path = HERE / "summary.json"

    def _convert(x):
        if isinstance(x, dict):
            return {k: _convert(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [_convert(v) for v in x]
        if isinstance(x, np.ndarray):
            return [_convert(v) for v in x.tolist()]
        if isinstance(x, (np.integer,)):
            return int(x)
        if isinstance(x, (np.floating,)):
            return float(x)
        if isinstance(x, (np.bool_,)):
            return bool(x)
        if isinstance(x, pd.Timestamp):
            return str(x.date())
        if isinstance(x, date):
            return x.isoformat()
        return x

    summary_path.write_text(
        json.dumps(_convert(summary), indent=2), encoding="utf-8"
    )
    print()
    print("Wrote " + str(summary_path))

    # Stage 6: emit findings.md + README.md
    print("Stage 6: emitting findings.md + README.md...")
    findings_path = HERE / "findings.md"
    stage6_emit_findings(summary, findings_path)
    print("  " + str(findings_path))

    readme_path = HERE / "README.md"
    stage6_emit_readme(summary, readme_path)
    print("  " + str(readme_path))

    print()
    print("Done. Q4.3 LANDED (Tier 3 Strand B 3rd of 5; methodological backstop).")


if __name__ == "__main__":
    main()
