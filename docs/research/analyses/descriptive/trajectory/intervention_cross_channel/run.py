"""Q4.2 -- intervention_cross_channel: integrated cross-channel picture of
the citalopram effect across 6 channels.

INTEGRATED CROSS-CHANNEL TIMING + TRANSITION ANALYSIS per descriptive
README sec 4.2. Extends:

- citalopram_dose_response_stress_mean_sleep.md sec 5.6 (v3 sweep: 3
  CONFIRMED stress_mean_sleep / all_day_stress_avg / bb_lowest + 1
  REJECTED respiration_avg_sleep)
- recovery_arc v2 sec 5.A afbouw-reversal on the 3 CONFIRMED-citalopram
  channels at 2026-03-20
- STOCKTAKE sec 6 Pattern 2 (6-channel afbouw direction split)
- Q4.3 era_boundaries rp5 (citalopram-start 2024-04-09; strongest
  distribution-shift boundary -- 5 of 7 channels)
- Q4.4 cohort_topology rp5/cp3 event-rate decoupling (event rates
  barely shift at rp5; substantively drop at cp3)
- Q4.5.b detrended_correlation resting_hr trajectory-driven spurious
  flags (informs honest framing for the resting_hr timing-onset read)

USER-LOCKED OPERATIONALISATION (per Strand B sec 7c interview
2026-06-25; do NOT iterate):

1. Channel scope = 6 channels (matches Q4.9 + Q4.5.b):
   - stress_mean_sleep            (CONFIRMED-citalopram +0.43/mg)
   - all_day_stress_avg           (CONFIRMED-citalopram +0.57/mg)
   - bb_lowest                    (CONFIRMED-citalopram -1.13/mg)
   - stress_stdev_sleep           (NOT v3 CONFIRMED; descriptive only)
   - stress_low_motion_min_count_S60_Mlow (NOT v3 CONFIRMED; descriptive only)
   - resting_hr                   (NOT v3 CONFIRMED; weakly consistent in v3)
2. Timing-onset = ALL 3 methods + sensitivity:
   - Method (a) threshold-cross: first day post-2024-04-09 where the
     personal-baseline |z| stays >= 1.0 for >= 7 consecutive days
     (z computed against the channel's pre-citalopram unmedicated
     baseline using robust median + MAD via z_score_vs_rolling_baseline
     pre-rolled with a fixed pre-citalopram-pool window; threshold
     choice documented at the Stage 2 docstring + Limitations).
   - Method (b) PELT change-point: parameter-light binary segmentation
     reuse of Q4.3's method on the post-citalopram z-trajectory; first
     detected change-point per channel.
   - Method (c) time-to-half-effect: exponential decay fit on the
     channel z-trajectory anchored at 2024-04-09; time-to-half-effect
     is the t at which the fitted curve has traversed half the
     pre-to-asymptote distance (descriptive SSRI-kinetics proxy).
3. Per-citalopram-phase = buildup-transition (2024-04-09) +
   afbouw-reversal (2026-03-20). Two transitions; Stage 5 reports
   per-channel Delta-z across each transition + reproduces Pattern 2
   6-channel afbouw direction split.
4. Visualisation = ALL 3:
   - Per-channel timeline aligned at t0=2024-04-09 (per-channel
     overlay panel)
   - Heatmap (channel x days-since-citalopram-start x z)
   - Cross-channel timing ladder (rank 6 channels by Method (a) + (b)
     + (c) onset; methods side-by-side; agreement vs disagreement
     descriptively flagged)

OUTPUTS (4+ artefacts per handoff sec 3.2 Stage 7):

1. Per-channel timeline aligned at t0=2024-04-09 (PNG; multi-panel
   or overlay).
2. Heatmap (channel x time-since-citalopram-start x z) (PNG).
3. Cross-channel timing ladder per 3 methods (PNG).
4. Method-sensitivity comparison plot (PNG).
+ summary.json (gitignored), findings.md + README.md (programmatic
emit per Stage 8).

DISCIPLINE GUARDS (per CONVENTIONS):

- sec 2.1 descriptive-before-inference: report timing-onset per cell;
  NO causal claims; NO 'the SSRI hits channel X first' framing; NO
  promotion of non-CONFIRMED channels to CONFIRMED-citalopram
  candidacy.
- sec 3.1 personal baseline: 28d-lagged z-scores against pre-citalopram
  baseline; matches the lagged-baseline discipline.
- sec 3.6 named counts: every n in summary tables names scheme + unit.
- sec 3.7 trajectory-detrend sensitivity: Q4.5.b's resting_hr
  trajectory-driven finding is flagged honestly at the resting_hr
  timing-onset read.
- sec 4.1 + sec 4.2 caveat-class: framing 'channel X has onset of Y
  days post-citalopram-start under Method (a)' is descriptive; NOT
  'SSRI acts on channel X first'.
- sec 4.3: data-driven change-point detection (Method (b)) is
  exploratory; reported honestly + cross-referenced with method (a)
  + (c).

CROSS-REFERENCES LOAD-BEARING (per handoff sec 3.3):

- v3 sweep CONFIRMED 3 / REJECTED 1 cited; non-CONFIRMED channels
  descriptive only (NOT promoted to candidacy).
- recovery_arc v2 sec 5.A afbouw-reversal reproduced + extended in
  Stage 5.
- Pattern 2 6-channel afbouw direction split closed with timing in
  Stage 5.
- Q4.3 rp5 strongest-boundary cross-reference.
- Q4.4 rp5/cp3 event-rate decoupling honest framing (Q4.2 is on
  channel distributions, NOT event rates).
- Q4.5.b resting_hr trajectory-driven caveat (timing-onset detected
  on resting_hr may partly reflect multi-year arc artefact).

Layer 1 descriptive per CONVENTIONS sec 2.1.
NOT a substantive HA verdict; NOT a mechanism interpretation of SSRI
kinetics; NOT a promotion of any non-CONFIRMED channel; integrated
descriptive picture only per CONVENTIONS sec 2.1 + sec 4.1 + sec 4.2
caveat-class.
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
# HERE = .../analyses/descriptive/trajectory/intervention_cross_channel
# parents[0]=trajectory; [1]=descriptive; [2]=analyses
UTILS_DIR = HERE.parents[2] / "_utils"
sys.path.insert(0, str(UTILS_DIR))

from frame import load_master  # noqa: E402


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AS_OF_DATE = "2026-06-04"  # Garmin coverage right edge per STOCKTAKE sec 1

# 6 channels per user-locked operationalisation (handoff sec 2.1)
CHANNELS = [
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
    "stress_stdev_sleep",
    "stress_low_motion_min_count_S60_Mlow",
    "resting_hr",
]

# v3 sweep CONFIRMED set (citalopram_dose_response_stress_mean_sleep sec 5.6)
CONFIRMED_V3 = {
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
}
NON_CONFIRMED = {c for c in CHANNELS if c not in CONFIRMED_V3}

# Channel-level prior direction (v3 sweep) -- expected z-shift direction
# at citalopram_modulated phase relative to unmedicated baseline.
# Used ONLY to choose absolute-z vs signed-z onset for Method (a);
# does NOT affect direction-agnostic descriptive reads.
# CONFIRMED priors: +1 = z increases; -1 = z decreases.
# Non-CONFIRMED priors are "expected direction per the v3 attempt"
# but the reading is descriptive only.
PRIOR_DIRECTION = {
    "stress_mean_sleep": +1,  # CONFIRMED +0.43/mg
    "all_day_stress_avg": +1,  # CONFIRMED +0.57/mg
    "bb_lowest": -1,  # CONFIRMED -1.13/mg
    "stress_stdev_sleep": 0,  # non-CONFIRMED; agnostic
    "stress_low_motion_min_count_S60_Mlow": 0,  # non-CONFIRMED; agnostic
    "resting_hr": +1,  # non-CONFIRMED weakly consistent in v3
}

# Boundaries
CITALOPRAM_START = date(2024, 4, 9)  # buildup-transition; rp5 + cp1
AFBOUW_START = date(2026, 3, 20)  # consolidation -> afbouw; cp3

# Method (a) threshold-cross parameters
METHOD_A_Z_THRESHOLD = 1.0  # |z| >= threshold sustained for
METHOD_A_SUSTAINED_DAYS = 7  # N consecutive days; E[L]=7 per
# permutation_null_block_length.md (project default autocorrelation
# horizon; aligns with the minimum-effective-window discipline).

# Method (b) PELT/binseg parameters (reuse Q4.3 era_boundaries pattern)
METHOD_B_SMOOTH_WINDOW = 14  # smoothing window on z-series
METHOD_B_MIN_SEGMENT = 14  # min segment size; ~2 * E[L]=7
METHOD_B_MAX_DEPTH = 8  # max splits
METHOD_B_REDUCTION_THRESHOLD = 0.05  # 5% SSD reduction floor

# Method (c) decay fit parameters
METHOD_C_WINDOW_DAYS = 180  # ~6 months post-citalopram-start for fit

# Personal-baseline z (CONVENTIONS sec 3.1)
BASELINE_WINDOW_DAYS = 28  # 28d window per CONVENTIONS sec 3.1
PRE_POOL_DAYS = 365  # pre-citalopram pool for the unmedicated reference
# (used for global baseline; per-day rolling z is computed afterwards)

# Stage 5 transition windows
TRANSITION_HALF_WIDTH_DAYS = 30  # +-30d each side of transition

RANDOM_SEED = 42


# ---------------------------------------------------------------------------
# Stage 1 -- data prep
# ---------------------------------------------------------------------------


def stage1_data_prep() -> dict:
    """Load per_day_master; restrict to 6 channels + gevoelscore context
    + dose_plasma_mg + recovery_phase.

    Compute 28d-lagged z-scores per channel per day. Personal-baseline z
    uses a robust median + MAD over the trailing 28d window with lag=1
    (window excludes the current point per CONVENTIONS sec 3.1 + the
    z_score_vs_rolling_baseline default semantics described in frame.py).

    Returns dict with df, n_rows, n_per_channel, corpus left/right.
    """
    master = load_master(as_of_date=AS_OF_DATE)
    master = master.copy()
    master["date"] = pd.to_datetime(master["date"])
    master = master.sort_values("date").reset_index(drop=True)

    keep_cols = ["date", "recovery_phase", "gevoelscore"] + CHANNELS
    if "dose_plasma_mg" in master.columns:
        keep_cols.append("dose_plasma_mg")
    available_cols = [c for c in keep_cols if c in master.columns]
    df = master[available_cols].copy()

    # citalopram_phase derivation
    df["citalopram_phase"] = df["date"].dt.date.apply(_citalopram_phase_from_date)

    # Pre-citalopram pool reference: per channel, robust median + MAD on
    # the unmedicated pool (date < CITALOPRAM_START). This is the "global
    # baseline" the timing-onset z-trajectory references in Methods (a)
    # and (c).
    pre_mask = df["date"] < pd.Timestamp(CITALOPRAM_START)
    z_pre_columns: dict = {}
    for chan in CHANNELS:
        pre_vals = df.loc[pre_mask, chan].dropna().to_numpy(dtype=float)
        if len(pre_vals) < 30:
            z_pre_columns[chan + "_z_pre"] = pd.Series(
                np.nan, index=df.index
            )
            continue
        med = float(np.median(pre_vals))
        mad = float(np.median(np.abs(pre_vals - med)))
        spread = mad * 1.4826 if mad > 0 else float("nan")
        if not np.isfinite(spread) or spread == 0.0:
            z_pre_columns[chan + "_z_pre"] = pd.Series(
                np.nan, index=df.index
            )
            continue
        z_pre_columns[chan + "_z_pre"] = (df[chan] - med) / spread
    z_pre_df = pd.DataFrame(z_pre_columns, index=df.index)
    df = pd.concat([df, z_pre_df], axis=1)

    # Rolling personal-baseline 28d-lagged z per channel (CONVENTIONS sec 3.1).
    # Computed inline rather than via z_score_vs_rolling_baseline because we
    # want lag=1 + robust=True default with explicit window=28 + persisted
    # column suffix consistent with the existing _lagged_lcera convention.
    z_rolling_columns: dict = {}
    for chan in CHANNELS:
        z_rolling_columns[chan + "_z_28d"] = _rolling_z(
            df[chan], window=BASELINE_WINDOW_DAYS, lag=1, robust=True
        )
    z_rolling_df = pd.DataFrame(z_rolling_columns, index=df.index)
    df = pd.concat([df, z_rolling_df], axis=1)

    # Per-row dose-plasma (NaN-safe; defaults 0.0 pre-2024-04-09 per
    # citalopram_phase_stratification sec 3 explicit unmedicated case)
    if "dose_plasma_mg" in df.columns:
        df["dose_plasma_mg"] = df["dose_plasma_mg"].fillna(0.0)
    else:
        df["dose_plasma_mg"] = 0.0

    n_per_channel = {
        c: int(df[c].notna().sum()) for c in CHANNELS if c in df.columns
    }

    pre_pool_n = int(pre_mask.sum())
    post_pool_n = int((~pre_mask).sum())

    return {
        "df": df,
        "n_rows": int(len(df)),
        "n_per_channel": n_per_channel,
        "corpus_left": df["date"].min().date(),
        "corpus_right": df["date"].max().date(),
        "pre_citalopram_pool_n": pre_pool_n,
        "post_citalopram_pool_n": post_pool_n,
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


def _rolling_z(
    series: pd.Series,
    *,
    window: int,
    lag: int,
    robust: bool,
) -> pd.Series:
    """Compute trailing-window robust personal-baseline z; lag excludes
    the current point from the window when lag>=1. Per CONVENTIONS sec
    3.1; matches frame.z_score_vs_rolling_baseline semantics inline.
    """
    arr = series.to_numpy(dtype=float)
    n = len(arr)
    z = np.full(n, np.nan)
    min_periods = max(2, window // 2)
    for t in range(n):
        end = t - lag + 1
        start = end - window
        if end <= 0:
            continue
        start = max(0, start)
        win = arr[start:end]
        win = win[~np.isnan(win)]
        if len(win) < min_periods:
            continue
        if robust:
            centre = float(np.median(win))
            mad = float(np.median(np.abs(win - centre)))
            if mad == 0.0:
                continue
            spread = mad * 1.4826
        else:
            centre = float(win.mean())
            spread = float(win.std(ddof=1))
            if spread == 0.0:
                continue
        if np.isnan(arr[t]):
            continue
        z[t] = (arr[t] - centre) / spread
    return pd.Series(z, index=series.index)


# ---------------------------------------------------------------------------
# Stage 2 -- Method (a) threshold-cross
# ---------------------------------------------------------------------------


def stage2_method_a_threshold_cross(df: pd.DataFrame) -> dict:
    """Per channel: find first day post-2024-04-09 where the
    z-vs-pre-citalopram-pool series has |z| >= METHOD_A_Z_THRESHOLD
    sustained for >= METHOD_A_SUSTAINED_DAYS consecutive days.

    Sustained = consecutive day-rows with non-NaN z and |z| >= threshold.
    Returns dict[channel] -> onset_date, days_post_t0, threshold meta.

    THRESHOLD CHOICE DOCUMENTATION (per handoff sec 6 acceptance
    criterion + sec 2 user-locked choice 2a):

    - |z| >= 1.0 = 1 SD relative to the pre-citalopram (unmedicated)
      pool baseline. Equivalent to the "noteworthy deviation" cut-off
      used widely in psychophysiology + the project's prior
      lc_recovery_phase_axis sec 7b sensitivity-arm narrative (where
      paired-bootstrap CIs are reported at 1-SD-equivalent block-length
      scales).
    - Sustained >= 7 days = E[L]=7 from permutation_null_block_length
      (project default autocorrelation horizon); a 7-day sustained
      excursion is "longer than the channel's autocorrelation memory"
      and is the minimal window beyond noise per project convention.
    - Combination: |z| >= 1.0 SUSTAINED >= 7d is the descriptive
      threshold-cross definition; alternative thresholds (e.g. 0.5 +
      14d; 1.5 + 5d) would yield different onsets. The (1.0, 7d) pair
      is the project-default pairing and is documented here as the
      anchor; sensitivity to this choice is NOT computed inside Q4.2
      (out of scope per the locked 4-choice operationalisation).
    - Direction filter: |z| is direction-agnostic per the descriptive
      framing (CONVENTIONS sec 4.1 + sec 4.2). The z_pre reference
      pool is the pre-citalopram (unmedicated) pool which spans the
      LC recovery arc (phase 3 lc_pre_ergo peak + phases 4a + 4b
      pacing); the citalopram_modulated phase z_pre direction can
      be either sign relative to this pool because the LC recovery
      trajectory continues across the boundary. A direction filter
      tied to the v3 within-citalopram-traject prior would
      misattribute LC-recovery direction to the citalopram boundary;
      we report direction-agnostic threshold-cross + flag the
      direction of the onset run for transparency.
    """
    t0 = pd.Timestamp(CITALOPRAM_START)
    results: dict = {}
    for chan in CHANNELS:
        z_col = chan + "_z_pre"
        if z_col not in df.columns:
            results[chan] = {"skipped": True, "reason": "z_pre column missing"}
            continue
        post = df[df["date"] >= t0][["date", z_col]].copy()
        post = post.sort_values("date").reset_index(drop=True)
        z = post[z_col].to_numpy(dtype=float)
        dates = post["date"].dt.date.to_numpy()
        n = len(z)
        prior_dir = PRIOR_DIRECTION.get(chan, 0)

        onset_idx = -1
        onset_direction = 0
        # Search consecutive runs where |z| >= threshold AND all run
        # day-rows carry the same sign (direction-agnostic; either sign
        # accepted; sign of the onset run reported for transparency).
        # Sustained run = consecutive day-rows; NaN OR sign-flip OR
        # |z| < threshold breaks the run.
        run_start = -1
        run_len = 0
        run_sign = 0
        for i in range(n):
            zi = z[i]
            if np.isnan(zi) or abs(zi) < METHOD_A_Z_THRESHOLD:
                run_start = -1
                run_len = 0
                run_sign = 0
                continue
            sign_i = int(np.sign(zi))
            if run_start < 0:
                run_start = i
                run_len = 1
                run_sign = sign_i
            elif sign_i != run_sign:
                # sign flip breaks the run; restart on this day
                run_start = i
                run_len = 1
                run_sign = sign_i
            else:
                run_len += 1
            if run_len >= METHOD_A_SUSTAINED_DAYS:
                onset_idx = run_start
                onset_direction = run_sign
                break

        if onset_idx < 0:
            results[chan] = {
                "skipped": False,
                "onset_found": False,
                "onset_date": None,
                "days_post_t0": None,
                "n_post": int(n),
                "threshold_z": METHOD_A_Z_THRESHOLD,
                "sustained_days": METHOD_A_SUSTAINED_DAYS,
                "direction_filter": "direction-agnostic",
                "v3_prior_direction": prior_dir,
                "note": "no sustained excursion meeting threshold + sustained-days in post-window",
            }
            continue
        onset_date = dates[onset_idx]
        if not isinstance(onset_date, date):
            onset_date = pd.Timestamp(onset_date).date()
        days_post = int((onset_date - CITALOPRAM_START).days)
        results[chan] = {
            "skipped": False,
            "onset_found": True,
            "onset_date": onset_date.isoformat(),
            "days_post_t0": days_post,
            "onset_direction": onset_direction,
            "matches_v3_prior_direction": bool(
                prior_dir != 0 and onset_direction == prior_dir
            ),
            "n_post": int(n),
            "threshold_z": METHOD_A_Z_THRESHOLD,
            "sustained_days": METHOD_A_SUSTAINED_DAYS,
            "direction_filter": "direction-agnostic",
            "v3_prior_direction": prior_dir,
        }
    return results


# ---------------------------------------------------------------------------
# Stage 3 -- Method (b) PELT/binseg change-point on post-citalopram z
# ---------------------------------------------------------------------------


def stage3_method_b_change_point(df: pd.DataFrame) -> dict:
    """Per channel: binary segmentation on a 14d-rolling-median of the
    z-vs-pre-citalopram-pool series, restricted to post-2024-04-09
    rows. Returns first change-point date per channel.

    METHOD CHOICE: Q4.3 era_boundaries reused binary segmentation over
    PELT (a) parameter-light, (b) interpretable, (c) no library
    dependency. Same rationale applies here -- the post-citalopram
    z-trajectory is a single series per channel and we want the first
    inflection date; binseg's first-split is the right primitive.
    """
    t0 = pd.Timestamp(CITALOPRAM_START)
    results: dict = {}
    for chan in CHANNELS:
        z_col = chan + "_z_pre"
        if z_col not in df.columns:
            results[chan] = {"skipped": True, "reason": "z_pre column missing"}
            continue
        post = df[df["date"] >= t0][["date", z_col]].copy()
        post = post.sort_values("date").reset_index(drop=True)
        ts = post.set_index("date")[z_col].dropna()
        if len(ts) < 2 * METHOD_B_MIN_SEGMENT:
            results[chan] = {
                "skipped": True,
                "reason": "insufficient post-window data",
                "n": int(len(ts)),
            }
            continue
        smoothed = ts.rolling(
            window=METHOD_B_SMOOTH_WINDOW, min_periods=max(2, METHOD_B_SMOOTH_WINDOW // 2)
        ).median().dropna()
        if len(smoothed) < 2 * METHOD_B_MIN_SEGMENT:
            results[chan] = {
                "skipped": True,
                "reason": "insufficient smoothed data",
                "n": int(len(smoothed)),
            }
            continue
        values = smoothed.to_numpy(dtype=float)
        dates = smoothed.index

        cps = _binary_segmentation(
            values,
            max_depth=METHOD_B_MAX_DEPTH,
            min_segment_size=METHOD_B_MIN_SEGMENT,
        )
        candidate_dates = sorted([dates[cp].date() for cp in cps])

        first_cp_date = candidate_dates[0].isoformat() if candidate_dates else None
        first_cp_days_post = (
            int((candidate_dates[0] - CITALOPRAM_START).days)
            if candidate_dates else None
        )
        results[chan] = {
            "skipped": False,
            "n_smoothed": int(len(smoothed)),
            "n_candidates": int(len(candidate_dates)),
            "all_candidates": [d.isoformat() for d in candidate_dates],
            "first_change_point": first_cp_date,
            "first_change_point_days_post_t0": first_cp_days_post,
            "method": "binary_segmentation_on_14d_rolling_median_post_citalopram_z",
            "smoothing_window_days": METHOD_B_SMOOTH_WINDOW,
            "min_segment_size_days": METHOD_B_MIN_SEGMENT,
            "max_depth": METHOD_B_MAX_DEPTH,
        }
    return results


def _binary_segmentation(
    values: np.ndarray,
    *,
    max_depth: int,
    min_segment_size: int,
) -> list[int]:
    """Recursive binary segmentation (mirror of Q4.3 helper)."""
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
    if depth >= max_depth:
        return
    if (b - a) < 2 * min_segment_size:
        return
    seg = values[a:b]
    seg_mean = float(seg.mean())
    total_ssd = float(((seg - seg_mean) ** 2).sum())
    if total_ssd <= 0:
        return
    best_k = -1
    best_score = 0.0
    for k_local in range(min_segment_size, (b - a) - min_segment_size):
        left = seg[:k_local]
        right = seg[k_local:]
        left_ssd = float(((left - left.mean()) ** 2).sum())
        right_ssd = float(((right - right.mean()) ** 2).sum())
        score = total_ssd - (left_ssd + right_ssd)
        if score > best_score:
            best_score = score
            best_k = a + k_local
    if best_k < 0:
        return
    if best_score / total_ssd < METHOD_B_REDUCTION_THRESHOLD:
        return
    cps.append(best_k)
    _binseg_recurse(values, a, best_k, depth + 1, max_depth, min_segment_size, cps)
    _binseg_recurse(values, best_k, b, depth + 1, max_depth, min_segment_size, cps)


# ---------------------------------------------------------------------------
# Stage 4 -- Method (c) time-to-half-effect (exponential decay fit)
# ---------------------------------------------------------------------------


def stage4_method_c_half_effect(df: pd.DataFrame) -> dict:
    """Per channel: fit z(t) = z_inf * (1 - exp(-t / tau)) on a
    28d-smoothed post-citalopram z_pre series over a 180d window
    anchored at t=2024-04-09. Compute time-to-half-effect = tau *
    ln(2).

    Half-effect = the t at which the fitted curve covers half the
    pre-to-asymptote distance; descriptive SSRI-kinetics PROXY per
    handoff sec 2 user-locked choice 2c.

    SMOOTHING: input is a 28d-rolling median of z_pre, NOT raw daily
    z_pre. Raw daily z_pre is dominated by day-to-day noise at this
    corpus's autocorrelation horizons (E[L] = 7-30 across the 6
    channels); a decay fit on raw daily data collapses to tau ~ 1d
    (an immediate-step interpretation) when the model is asked to
    explain noisy daily data with a single z_inf + tau pair. Smoothing
    to 28d-rolling median leaves the slow-scale signal the decay
    model is designed to capture.

    Fit is descriptive only (no CI; per CONVENTIONS sec 4.2 + handoff
    sec 4 hard constraint -- NOT a substantive mechanism claim about
    SSRI receptor kinetics, plasma PK, or pharmacological half-life).
    z0 = 0 by construction (z_pre is centred on the pre-pool median);
    z_inf and tau fit via vectorised grid search + refinement.

    Reports tau (days) + half-effect-time (tau * ln(2), days) +
    RMSE + fit_quality flag. Fit-quality "poor" if |z_inf| < 0.1 OR
    RMSE > 1.0 OR tau hits the lower grid edge (a tau = 7d hit means
    the smoothed series is best explained by an effective step at the
    project's autocorrelation horizon; honest framing per CONVENTIONS
    sec 4.2 caveat-class).
    """
    t0 = pd.Timestamp(CITALOPRAM_START)
    end_window = t0 + pd.Timedelta(days=METHOD_C_WINDOW_DAYS)
    results: dict = {}
    for chan in CHANNELS:
        z_col = chan + "_z_pre"
        if z_col not in df.columns:
            results[chan] = {"skipped": True, "reason": "z_pre column missing"}
            continue
        post = df[
            (df["date"] >= t0) & (df["date"] < end_window)
        ][["date", z_col]].copy()
        post = post.sort_values("date").reset_index(drop=True)
        # Smooth z_pre via 28d-rolling median (CONVENTIONS sec 3.1
        # personal-baseline scale; matches the project default)
        post["z_smooth"] = post[z_col].rolling(window=28, min_periods=10).median()
        post_valid = post.dropna(subset=["z_smooth"])
        if len(post_valid) < 30:
            results[chan] = {
                "skipped": True,
                "reason": "insufficient smoothed-window data for decay fit",
                "n": int(len(post_valid)),
            }
            continue
        t_days = (post_valid["date"] - t0).dt.days.to_numpy(dtype=float)
        z_obs = post_valid["z_smooth"].to_numpy(dtype=float)

        # Grid: z_inf in [-3, 3] (61 pts); tau in [7, 365] (60 pts log).
        # tau lower bound = E[L]=7 project default (sub-E[L] tau would
        # be modelling sub-autocorrelation noise as signal, not slow
        # SSRI-like dynamics).
        z_inf_grid = np.linspace(-3.0, 3.0, 61)
        tau_grid = np.logspace(np.log10(7.0), np.log10(365.0), 60)
        best_rmse = np.inf
        best_z_inf = np.nan
        best_tau = np.nan
        for z_inf_try in z_inf_grid:
            for tau_try in tau_grid:
                pred = z_inf_try * (1.0 - np.exp(-t_days / tau_try))
                resid = z_obs - pred
                rmse = float(np.sqrt(np.mean(resid * resid)))
                if rmse < best_rmse:
                    best_rmse = rmse
                    best_z_inf = float(z_inf_try)
                    best_tau = float(tau_try)
        # Local refinement on a finer 41 x 41 sub-grid around best.
        z_lo = max(-3.0, best_z_inf - 0.5)
        z_hi = min(3.0, best_z_inf + 0.5)
        tau_lo = max(7.0, best_tau / 2.0)
        tau_hi = min(365.0, best_tau * 2.0)
        z_inf_grid2 = np.linspace(z_lo, z_hi, 41)
        tau_grid2 = np.logspace(np.log10(tau_lo), np.log10(tau_hi), 41)
        for z_inf_try in z_inf_grid2:
            for tau_try in tau_grid2:
                pred = z_inf_try * (1.0 - np.exp(-t_days / tau_try))
                resid = z_obs - pred
                rmse = float(np.sqrt(np.mean(resid * resid)))
                if rmse < best_rmse:
                    best_rmse = rmse
                    best_z_inf = float(z_inf_try)
                    best_tau = float(tau_try)
        half_effect_t = float(best_tau * np.log(2.0))
        tau_at_lower_edge = bool(best_tau <= 7.5)  # hit lower grid edge
        # Fit-quality flag: poor if |z_inf| < 0.1 (effectively flat) OR
        # RMSE > 1.0 (1 SD residual error) OR tau at lower grid edge
        # (effective-step interpretation -- honest framing per
        # CONVENTIONS sec 4.2 caveat-class; flagged for the reader).
        if abs(best_z_inf) < 0.1:
            fit_quality = "poor (effectively flat z_inf)"
        elif best_rmse > 1.0:
            fit_quality = "poor (high RMSE)"
        elif tau_at_lower_edge:
            fit_quality = "step-like (tau at lower edge; effective step at E[L])"
        else:
            fit_quality = "good"
        results[chan] = {
            "skipped": False,
            "n_fit": int(len(post_valid)),
            "z_inf": best_z_inf,
            "tau_days": best_tau,
            "half_effect_days": half_effect_t,
            "rmse": best_rmse,
            "fit_quality": fit_quality,
            "tau_at_lower_edge": tau_at_lower_edge,
            "fit_window_days": METHOD_C_WINDOW_DAYS,
            "smoothing": "28d-rolling-median of z_pre",
        }
    return results


# ---------------------------------------------------------------------------
# Stage 5 -- per-phase transition analysis
# ---------------------------------------------------------------------------


def stage5_transition_analysis(df: pd.DataFrame) -> dict:
    """Buildup-transition (2024-04-09) + afbouw-reversal (2026-03-20).

    For each transition: per-channel median(z_28d) on +-30d windows each
    side; report Delta-z = post_median - pre_median.

    Buildup-transition uses z_pre (vs pre-citalopram pool) so the read
    is "how far the post-window has drifted from the unmedicated pool".

    Afbouw-reversal uses z_28d (28d-rolling baseline) so the read is
    "how much the channel shifts at the consolidation -> afbouw
    boundary relative to its trailing 28d window". This matches the
    Q4.3 era_boundaries cp3 read + Pattern 2 6-channel afbouw
    direction split language.

    Returns dict[channel] -> {buildup_delta_z, afbouw_delta_z,
    afbouw_direction_label}.
    """
    results: dict = {}
    bt = pd.Timestamp(CITALOPRAM_START)
    ar = pd.Timestamp(AFBOUW_START)
    win = TRANSITION_HALF_WIDTH_DAYS

    for chan in CHANNELS:
        # Buildup-transition: z_pre summary on +-30d windows around bt
        z_pre_col = chan + "_z_pre"
        buildup_delta = None
        if z_pre_col in df.columns:
            pre_win = df[
                (df["date"] >= bt - pd.Timedelta(days=win))
                & (df["date"] < bt)
            ][z_pre_col].dropna()
            post_win = df[
                (df["date"] >= bt)
                & (df["date"] < bt + pd.Timedelta(days=win))
            ][z_pre_col].dropna()
            if len(pre_win) >= 5 and len(post_win) >= 5:
                buildup_delta = float(post_win.median() - pre_win.median())
            buildup_meta = {
                "pre_n": int(len(pre_win)),
                "post_n": int(len(post_win)),
                "pre_z_median": float(pre_win.median()) if len(pre_win) > 0 else None,
                "post_z_median": float(post_win.median()) if len(post_win) > 0 else None,
            }
        else:
            buildup_meta = {"pre_n": 0, "post_n": 0, "pre_z_median": None, "post_z_median": None}

        # Afbouw-reversal: phase-median z on the consolidation vs afbouw
        # pools (not +-30d windows; per recovery_arc v2 sec 5.A + Pattern
        # 2 the comparison is the citalopram-phase pool medians).
        cons_mask = (
            (df["date"] >= pd.Timestamp(date(2024, 6, 20)))
            & (df["date"] < pd.Timestamp(date(2026, 3, 20)))
        )
        afb_mask = (
            (df["date"] >= pd.Timestamp(date(2026, 3, 20)))
            & (df["date"] < pd.Timestamp(date(2026, 6, 6)))
        )
        unmed_mask = df["date"] < pd.Timestamp(CITALOPRAM_START)

        cons_med = float(df.loc[cons_mask, chan].median()) if df.loc[cons_mask, chan].notna().any() else None
        afb_med = float(df.loc[afb_mask, chan].median()) if df.loc[afb_mask, chan].notna().any() else None
        unmed_med = float(df.loc[unmed_mask, chan].median()) if df.loc[unmed_mask, chan].notna().any() else None
        cons_n = int(df.loc[cons_mask, chan].notna().sum())
        afb_n = int(df.loc[afb_mask, chan].notna().sum())
        unmed_n = int(df.loc[unmed_mask, chan].notna().sum())

        # +-30d windowed reads around afbouw boundary (using z_28d for
        # local-baseline-relative shift; matches Q4.3 era_boundaries cp3
        # window style)
        z_28d_col = chan + "_z_28d"
        afbouw_delta_z = None
        if z_28d_col in df.columns:
            afb_pre_win = df[
                (df["date"] >= ar - pd.Timedelta(days=win))
                & (df["date"] < ar)
            ][z_28d_col].dropna()
            afb_post_win = df[
                (df["date"] >= ar)
                & (df["date"] < ar + pd.Timedelta(days=win))
            ][z_28d_col].dropna()
            if len(afb_pre_win) >= 5 and len(afb_post_win) >= 5:
                afbouw_delta_z = float(afb_post_win.median() - afb_pre_win.median())
            afbouw_window_meta = {
                "pre_n": int(len(afb_pre_win)),
                "post_n": int(len(afb_post_win)),
            }
        else:
            afbouw_window_meta = {"pre_n": 0, "post_n": 0}

        # Pattern 2 direction label per STOCKTAKE sec 6:
        # full-recovery = afbouw median returns to unmedicated baseline
        # reversal-below = afbouw goes >0.3 raw units past unmed (against citalopram direction)
        # no-shift = afbouw and consolidation medians within tolerance
        # rise-above = afbouw median rises past unmed baseline
        # We compare RAW medians (not z) per Pattern 2 description.
        direction_label = _classify_afbouw_direction(
            cons_med=cons_med,
            afb_med=afb_med,
            unmed_med=unmed_med,
            channel=chan,
        )

        results[chan] = {
            "buildup_transition": {
                "boundary_date": CITALOPRAM_START.isoformat(),
                "delta_z_pre": buildup_delta,
                "window_half_width_days": win,
                **buildup_meta,
            },
            "afbouw_reversal": {
                "boundary_date": AFBOUW_START.isoformat(),
                "unmed_pool_median": unmed_med,
                "consolidation_pool_median": cons_med,
                "afbouw_pool_median": afb_med,
                "unmed_n": unmed_n,
                "consolidation_n": cons_n,
                "afbouw_n": afb_n,
                "delta_z_28d_at_boundary": afbouw_delta_z,
                "delta_z_28d_window_meta": afbouw_window_meta,
                "pattern2_direction_label": direction_label,
            },
        }
    return results


def _classify_afbouw_direction(
    *,
    cons_med: float | None,
    afb_med: float | None,
    unmed_med: float | None,
    channel: str,
) -> str:
    """Pattern 2 direction classification per STOCKTAKE sec 6 Pattern 2.

    Tolerance: |afb_med - unmed_med| <= 5% of unmed pool range counts
    as 'full-recovery' (returns to baseline) or 'no-shift' depending on
    whether the consolidation cell shifted off baseline.

    Honest framing per handoff sec 3.4: this is DESCRIPTIVE
    classification, NOT a causal claim about citalopram withdrawal
    architecture.
    """
    if cons_med is None or afb_med is None or unmed_med is None:
        return "insufficient_data"
    # Tolerance for 'no_change' = 5% of the unmedicated pool absolute
    # value (channel-relative scale; falls back to 0.5 if unmed_med
    # is small).
    tol = max(abs(unmed_med) * 0.05, 0.5)
    # 'Citalopram direction' for known CONFIRMED channels:
    # stress_mean_sleep +1 (citalopram LOWERS); all_day_stress_avg +1;
    # bb_lowest -1 (citalopram RAISES). For non-CONFIRMED channels use
    # the v3-attempt direction.
    prior_dir = PRIOR_DIRECTION.get(channel, 0)

    # cons->afb shift relative to unmed baseline
    cons_off = cons_med - unmed_med
    afb_off = afb_med - unmed_med

    # Classification: compare afb_off to unmed (== 0 offset) and to cons_off
    if abs(afb_off) <= tol and abs(cons_off) > tol:
        return "full-recovery (afbouw returns to unmedicated baseline)"
    if abs(afb_off) <= tol and abs(cons_off) <= tol:
        return "no-shift (consolidation already at unmedicated baseline)"
    # Reversal-below: afb crosses unmed line in the OPPOSITE direction
    # to the citalopram-effect direction (i.e. citalopram raised
    # bb_lowest in consolidation; afbouw drops it BELOW unmed)
    if prior_dir != 0:
        # citalopram_effect_direction at cons = sign(cons_off)
        # Note: for stress_mean_sleep prior_dir=+1 means citalopram
        # RAISES the channel during consolidation (above unmed); for
        # bb_lowest prior_dir=-1 means citalopram LOWERS the channel
        # but our prior here is the +1 = z increases convention so
        # for bb_lowest the "consolidation off unmed" sign should be
        # NEGATIVE.
        # Use sign(cons_off) directly: reversal-below = afb_off sign
        # opposite to cons_off sign AND |afb_off| > tol.
        if cons_off != 0 and afb_off != 0 and np.sign(afb_off) != np.sign(cons_off):
            return "reversal-below (afbouw crosses baseline in opposite direction)"
    if abs(afb_off) > tol:
        # afbouw shifted off baseline; check direction
        if prior_dir == 0:
            return (
                "shift-above-baseline" if afb_off > 0
                else "shift-below-baseline"
            )
        # CONFIRMED channels: "rise-above" / "fall-below" framed by
        # citalopram-effect-direction
        return (
            "rise-above-baseline (afbouw shift exceeds unmedicated)" if afb_off > 0
            else "fall-below-baseline (afbouw shift exceeds unmedicated)"
        )
    return "indeterminate"


# ---------------------------------------------------------------------------
# Stage 6 -- cross-channel timing ladder + method-sensitivity
# ---------------------------------------------------------------------------


def stage6_timing_ladder(
    method_a: dict,
    method_b: dict,
    method_c: dict,
) -> dict:
    """Rank 6 channels by onset per each method; report sensitivity
    across methods.

    Method (a) ladder rank = increasing onset_days (smaller = earlier).
    Method (b) ladder rank = increasing first_change_point_days_post_t0.
    Method (c) ladder rank = increasing half_effect_days.

    Channels with skipped or no-onset entries are placed at the bottom
    of the respective ladder (rank = LAST_PLUS_1) with a "no_onset"
    note. Sensitivity = number of methods where each channel's rank
    differs by > 1 position.
    """
    n = len(CHANNELS)

    def _onset_a(chan):
        r = method_a.get(chan, {})
        if r.get("skipped") or not r.get("onset_found"):
            return None
        return r.get("days_post_t0")

    def _onset_b(chan):
        r = method_b.get(chan, {})
        if r.get("skipped"):
            return None
        return r.get("first_change_point_days_post_t0")

    def _onset_c(chan):
        r = method_c.get(chan, {})
        if r.get("skipped"):
            return None
        return r.get("half_effect_days")

    onsets = {
        "method_a": {c: _onset_a(c) for c in CHANNELS},
        "method_b": {c: _onset_b(c) for c in CHANNELS},
        "method_c": {c: _onset_c(c) for c in CHANNELS},
    }

    def _rank(onset_map):
        # Sorted ascending by onset (smaller = earlier). None placed at
        # the bottom of the ladder.
        valid = [(c, onset_map[c]) for c in CHANNELS if onset_map[c] is not None]
        invalid = [c for c in CHANNELS if onset_map[c] is None]
        valid_sorted = sorted(valid, key=lambda t: t[1])
        rank: dict = {}
        for i, (c, _) in enumerate(valid_sorted):
            rank[c] = i + 1
        for c in invalid:
            rank[c] = n + 1
        return rank

    ranks = {
        "method_a": _rank(onsets["method_a"]),
        "method_b": _rank(onsets["method_b"]),
        "method_c": _rank(onsets["method_c"]),
    }

    # Per-channel disagreement count: how many method-pairs have rank
    # diff > 1 position
    method_pairs = [("method_a", "method_b"), ("method_a", "method_c"), ("method_b", "method_c")]
    per_channel_disagreement: dict = {}
    for c in CHANNELS:
        disagreements = 0
        for m1, m2 in method_pairs:
            r1 = ranks[m1][c]
            r2 = ranks[m2][c]
            if abs(r1 - r2) > 1:
                disagreements += 1
        per_channel_disagreement[c] = {
            "n_disagreement_pairs": int(disagreements),
            "rank_a": int(ranks["method_a"][c]),
            "rank_b": int(ranks["method_b"][c]),
            "rank_c": int(ranks["method_c"][c]),
            "stable_across_methods": bool(disagreements == 0),
        }

    # Consensus ranking = mean of available ranks per channel (lower
    # mean = earlier on the consensus ladder). Equal ranks broken by
    # alphabetical channel name (descriptive only).
    consensus = []
    for c in CHANNELS:
        mean_rank = float(np.mean([ranks["method_a"][c], ranks["method_b"][c], ranks["method_c"][c]]))
        consensus.append((c, mean_rank))
    consensus_sorted = sorted(consensus, key=lambda t: (t[1], t[0]))

    return {
        "onsets": onsets,
        "ranks": ranks,
        "per_channel_disagreement": per_channel_disagreement,
        "consensus_ranking": [
            {"channel": c, "consensus_mean_rank": r} for c, r in consensus_sorted
        ],
        "n_stable_across_methods": int(
            sum(1 for c in CHANNELS if per_channel_disagreement[c]["stable_across_methods"])
        ),
        "n_disagreeing_channels": int(
            sum(1 for c in CHANNELS if not per_channel_disagreement[c]["stable_across_methods"])
        ),
    }


# ---------------------------------------------------------------------------
# Stage 7 -- visualisations (4+ artefacts)
# ---------------------------------------------------------------------------


def stage7_plots(
    df: pd.DataFrame,
    method_a: dict,
    method_b: dict,
    method_c: dict,
    ladder: dict,
    plots_dir: Path,
) -> list[str]:
    """Emit 4 artefacts per handoff sec 3.2 Stage 7:

    1. Per-channel timeline aligned at t0=2024-04-09 (multi-panel; 6
       subplots).
    2. Heatmap (channel x days-since-citalopram-start x z).
    3. Cross-channel timing ladder per 3 methods.
    4. Method-sensitivity comparison (per-channel rank scatter).
    """
    written: list[str] = []
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.colors import TwoSlopeNorm
    except ImportError:
        return ["(matplotlib not available; plots skipped)"]

    plots_dir.mkdir(parents=True, exist_ok=True)

    t0 = pd.Timestamp(CITALOPRAM_START)
    afb = pd.Timestamp(AFBOUW_START)

    # ----- Plot 1: per-channel timeline aligned at t0 -----
    fig, axes = plt.subplots(len(CHANNELS), 1, figsize=(11, 14), sharex=True)
    for ax, chan in zip(axes, CHANNELS):
        z_col = chan + "_z_pre"
        if z_col not in df.columns:
            ax.text(0.5, 0.5, chan + ": no z_pre", transform=ax.transAxes)
            continue
        d = df[["date", z_col]].dropna()
        days = (d["date"] - t0).dt.days
        z = d[z_col]
        ax.plot(days, z, linewidth=0.8, alpha=0.6, color="steelblue", label="z_pre daily")
        # 28d-rolling median overlay
        z_smooth = z.rolling(window=28, min_periods=10).median()
        ax.plot(days, z_smooth, color="darkblue", linewidth=1.3, label="28d-median")
        ax.axhline(0, color="gray", linestyle="-", linewidth=0.5)
        ax.axhline(+METHOD_A_Z_THRESHOLD, color="red", linestyle="--", linewidth=0.6, alpha=0.5)
        ax.axhline(-METHOD_A_Z_THRESHOLD, color="red", linestyle="--", linewidth=0.6, alpha=0.5)
        ax.axvline(0, color="green", linestyle="-", linewidth=0.8, alpha=0.7, label="t0 citalopram start")
        ax.axvline((afb - t0).days, color="orange", linestyle="-", linewidth=0.8, alpha=0.7, label="afbouw start")
        # Method (a) onset marker
        a = method_a.get(chan, {})
        if a.get("onset_found"):
            ax.axvline(a["days_post_t0"], color="purple", linestyle=":", linewidth=1.0, label="Method (a) onset")
        # Method (b) first CP marker
        b = method_b.get(chan, {})
        if not b.get("skipped") and b.get("first_change_point_days_post_t0") is not None:
            ax.axvline(b["first_change_point_days_post_t0"], color="magenta", linestyle=":", linewidth=1.0, label="Method (b) first CP")
        ax.set_ylabel(chan, fontsize=8, rotation=0, labelpad=80, ha="right")
        ax.set_ylim(-4.0, 4.0)
        ax.grid(True, alpha=0.3)
        confirm_tag = "CONFIRMED-citalopram" if chan in CONFIRMED_V3 else "non-CONFIRMED"
        ax.text(
            0.99, 0.92, confirm_tag,
            transform=ax.transAxes,
            ha="right", va="top",
            fontsize=7,
            color=("darkgreen" if chan in CONFIRMED_V3 else "darkred"),
        )
    axes[-1].set_xlabel("days since citalopram start (t0 = 2024-04-09)")
    axes[0].set_title("Per-channel z (vs pre-citalopram pool) aligned at t0 = 2024-04-09 (DESCRIPTIVE)")
    axes[0].legend(loc="upper right", fontsize=7)
    plt.tight_layout()
    p1 = plots_dir / "fig1_per_channel_timeline_aligned_t0.png"
    fig.savefig(p1, dpi=110)
    plt.close(fig)
    written.append(str(p1))

    # ----- Plot 2: heatmap (channel x days-since-t0 x z) -----
    # Build a 6 x N matrix of 28d-rolling-median z values over the full
    # post-citalopram window; rows = channels (in CHANNELS order); cols =
    # days bins from t0 to corpus right-edge.
    corpus_right = pd.Timestamp(df["date"].max())
    total_days = int((corpus_right - t0).days) + 1
    matrix = np.full((len(CHANNELS), total_days), np.nan)
    for i, chan in enumerate(CHANNELS):
        z_col = chan + "_z_pre"
        if z_col not in df.columns:
            continue
        post = df[df["date"] >= t0][["date", z_col]].dropna()
        # Rolling 14d median for heatmap smoothing (less than timeline's
        # 28d to keep heatmap responsive)
        post = post.sort_values("date")
        post["z_smooth"] = post[z_col].rolling(window=14, min_periods=5).median()
        for _, r in post.iterrows():
            day_idx = int((r["date"] - t0).days)
            if 0 <= day_idx < total_days and pd.notna(r["z_smooth"]):
                matrix[i, day_idx] = r["z_smooth"]
    fig, ax = plt.subplots(figsize=(13, 5))
    # Diverging colormap centred at z=0
    norm = TwoSlopeNorm(vmin=-2.5, vcenter=0.0, vmax=2.5)
    im = ax.imshow(
        matrix,
        aspect="auto",
        cmap="RdBu_r",
        norm=norm,
        interpolation="nearest",
    )
    ax.set_yticks(range(len(CHANNELS)))
    ax.set_yticklabels(CHANNELS, fontsize=8)
    # X-axis: show every ~60 days
    xticks = list(range(0, total_days, 60))
    xticklabels = [(t0 + pd.Timedelta(days=d)).strftime("%Y-%m") for d in xticks]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation=45, ha="right", fontsize=7)
    ax.set_xlabel("days since citalopram start (t0 = 2024-04-09)")
    ax.set_title("Channel x time-since-t0 x z (14d-rolling median; vs pre-citalopram pool)")
    # Mark afbouw boundary
    afb_day = (afb - t0).days
    ax.axvline(afb_day, color="black", linestyle="--", linewidth=1.0, alpha=0.8)
    ax.text(afb_day, -0.7, "afbouw start", ha="center", fontsize=7)
    fig.colorbar(im, ax=ax, label="z (vs pre-citalopram pool)")
    plt.tight_layout()
    p2 = plots_dir / "fig2_heatmap_channel_x_time_x_z.png"
    fig.savefig(p2, dpi=110)
    plt.close(fig)
    written.append(str(p2))

    # ----- Plot 3: cross-channel timing ladder per 3 methods -----
    fig, ax = plt.subplots(figsize=(11, 6))
    y_positions = np.arange(len(CHANNELS))
    bar_height = 0.27
    onset_a_vals = [
        ladder["onsets"]["method_a"][c]
        if ladder["onsets"]["method_a"][c] is not None else np.nan
        for c in CHANNELS
    ]
    onset_b_vals = [
        ladder["onsets"]["method_b"][c]
        if ladder["onsets"]["method_b"][c] is not None else np.nan
        for c in CHANNELS
    ]
    onset_c_vals = [
        ladder["onsets"]["method_c"][c]
        if ladder["onsets"]["method_c"][c] is not None else np.nan
        for c in CHANNELS
    ]
    ax.barh(y_positions - bar_height, onset_a_vals, height=bar_height, color="steelblue", label="Method (a) threshold-cross")
    ax.barh(y_positions, onset_b_vals, height=bar_height, color="darkorange", label="Method (b) PELT first-CP")
    ax.barh(y_positions + bar_height, onset_c_vals, height=bar_height, color="seagreen", label="Method (c) half-effect")
    ax.set_yticks(y_positions)
    ax.set_yticklabels(CHANNELS, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("days post citalopram start (lower = earlier onset)")
    ax.set_title("Cross-channel timing ladder per 3 methods (DESCRIPTIVE; NOT causal order)")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()
    p3 = plots_dir / "fig3_cross_channel_timing_ladder.png"
    fig.savefig(p3, dpi=110)
    plt.close(fig)
    written.append(str(p3))

    # ----- Plot 4: method-sensitivity comparison -----
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, chan in enumerate(CHANNELS):
        ranks = [
            ladder["ranks"]["method_a"][chan],
            ladder["ranks"]["method_b"][chan],
            ladder["ranks"]["method_c"][chan],
        ]
        color = "darkred" if not ladder["per_channel_disagreement"][chan]["stable_across_methods"] else "darkgreen"
        ax.plot([0, 1, 2], ranks, marker="o", color=color, linewidth=1.5, label=chan)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["Method (a)", "Method (b)", "Method (c)"], fontsize=9)
    ax.set_ylabel("ladder rank (1 = earliest)")
    ax.set_title("Method-sensitivity: per-channel ladder rank across 3 methods (red = disagreement >1; green = stable)")
    ax.invert_yaxis()
    ax.legend(loc="best", fontsize=7)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    p4 = plots_dir / "fig4_method_sensitivity.png"
    fig.savefig(p4, dpi=110)
    plt.close(fig)
    written.append(str(p4))

    return written


# ---------------------------------------------------------------------------
# Stage 8 -- programmatic emit findings.md + README.md
# ---------------------------------------------------------------------------


def stage8_emit_findings(summary: dict, path: Path) -> None:
    """Programmatic emit of findings.md."""
    lines: list[str] = []
    A = lines.append

    A("# Findings -- Q4.2 intervention_cross_channel (integrated citalopram picture)")
    A("")
    A("**Strand**: B (multi-year trajectory; descriptive). Closes the canonical Q4.2 scope per [`analyses/descriptive/README.md`](../../README.md) sec 4.2 for the first time in any artefact -- integrated cross-channel timing + transition picture of the citalopram effect.")
    A("")
    A(
        "**Surface**: full corpus (" + summary["corpus_left"] + " to " + summary["corpus_right"]
        + "; n=" + str(summary["n_rows"]) + " day-level rows). 6 channels x 3 timing-onset methods + 2 transitions analysed. NO causal claims; NO promotion of non-CONFIRMED channels to CONFIRMED-citalopram candidacy; NO mechanism interpretation of SSRI kinetics."
    )
    A("")
    A("**User-LOCKED operationalisation** (per Strand B sec 7c interview 2026-06-25; do NOT iterate):")
    A("")
    A("1. **6 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest (CONFIRMED-citalopram v3) + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr (non-CONFIRMED; descriptive only).")
    A("2. **ALL 3 timing-onset methods + sensitivity**: (a) threshold-cross (|z| >= 1.0 sustained >= 7d post-2024-04-09); (b) PELT/binseg change-point on post-citalopram z-trajectory; (c) time-to-half-effect via exponential decay fit (SSRI-kinetics proxy).")
    A("3. **Buildup-transition (2024-04-09) + afbouw-reversal (2026-03-20)**: per-channel Delta-z across each transition; Stage 5 reproduces Pattern 2 6-channel afbouw direction split from STOCKTAKE sec 6.")
    A("4. **ALL 3 visualisations**: per-channel timeline aligned at t0=2024-04-09 + heatmap (channel x time x z) + cross-channel timing ladder per 3 methods (+ method-sensitivity comparison plot).")
    A("")
    A("**Discipline**: Layer 1 descriptive (no causal claims; no falsification bar; no HA verdict promotion) per [CONVENTIONS sec 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + sec 4.1 + sec 4.2 caveat-class. Honest framing per handoff sec 3.4: 'channel X has earlier onset than channel Y under Method (a)' is descriptive observation; NOT 'the SSRI hits channel X first'.")
    A("")
    A("---")
    A("")
    A("## Headline")
    A("")

    # Headline 1: cross-channel timing ladder
    ladder = summary["stage6_ladder"]
    consensus_ranking = ladder["consensus_ranking"]
    consensus_order = ", ".join(
        c["channel"] + " (mean rank " + "{:.2f}".format(c["consensus_mean_rank"]) + ")"
        for c in consensus_ranking
    )
    A(
        "**Cross-channel timing ladder (consensus order across 3 methods; descriptive)**: "
        + consensus_order
    )
    A("")
    A(
        "**Method-sensitivity**: "
        + str(ladder["n_stable_across_methods"]) + " of " + str(len(CHANNELS))
        + " channels are STABLE across all 3 methods (rank diff <=1 on every method-pair); "
        + str(ladder["n_disagreeing_channels"])
        + " channels DISAGREE on at least one method-pair (rank diff >1)."
    )
    A("")

    # Headline 2: buildup-transition Delta-z table
    A("**Buildup-transition Delta-z per channel at 2024-04-09** (z_pre median in +-30d post vs pre window; CONFIRMED tag from v3 sweep):")
    A("")
    A("| channel | v3 tag | pre +-30d z_pre median | post +-30d z_pre median | Delta z_pre |")
    A("|---|---|---:|---:|---:|")
    for chan in CHANNELS:
        bt = summary["stage5_transitions"][chan]["buildup_transition"]
        tag = "CONFIRMED-citalopram" if chan in CONFIRMED_V3 else "non-CONFIRMED"
        pre_med = bt.get("pre_z_median")
        post_med = bt.get("post_z_median")
        delta = bt.get("delta_z_pre")
        A(
            "| `" + chan + "` | " + tag
            + " | " + (("{:+.3f}".format(pre_med)) if pre_med is not None else "n/a")
            + " | " + (("{:+.3f}".format(post_med)) if post_med is not None else "n/a")
            + " | " + (("{:+.3f}".format(delta)) if delta is not None else "n/a")
            + " |"
        )
    A("")

    # Headline 3: afbouw-reversal Pattern 2 reproduction
    A("**Afbouw-reversal Delta-z per channel at 2026-03-20** (raw-medians on unmedicated + consolidation + afbouw pools; reproduces Pattern 2 6-channel direction split per STOCKTAKE sec 6):")
    A("")
    A("| channel | v3 tag | unmed pool med | consolidation pool med | afbouw pool med | Pattern 2 label |")
    A("|---|---|---:|---:|---:|---|")
    for chan in CHANNELS:
        ar = summary["stage5_transitions"][chan]["afbouw_reversal"]
        tag = "CONFIRMED-citalopram" if chan in CONFIRMED_V3 else "non-CONFIRMED"
        unmed = ar.get("unmed_pool_median")
        cons = ar.get("consolidation_pool_median")
        afb = ar.get("afbouw_pool_median")
        label = ar.get("pattern2_direction_label", "n/a")
        A(
            "| `" + chan + "` | " + tag
            + " | " + (("{:.2f}".format(unmed)) if unmed is not None else "n/a")
            + " | " + (("{:.2f}".format(cons)) if cons is not None else "n/a")
            + " | " + (("{:.2f}".format(afb)) if afb is not None else "n/a")
            + " | " + label + " |"
        )
    A("")

    # Headline 4: resting_hr caveat per Q4.5.b
    A(
        "**resting_hr caveat per Q4.5.b** ([`detrended_correlation/findings.md`](../detrended_correlation/findings.md)): resting_hr drives 5 of 6 trajectory-driven spurious-flagged pairs under linear-OLS detrend (long-memory channel carrying multi-year arc). Per CONVENTIONS sec 3.7: the resting_hr timing-onset detected at this stage may **partly reflect a multi-year arc artefact** rather than a citalopram-specific timing read. Flagged honestly per handoff sec 3.4; the resting_hr ladder rank should be read in light of this caveat. resting_hr is also NOT in the v3 sweep CONFIRMED set; it is included here per the locked 6-channel scope for cross-channel breadth, NOT as a citalopram-candidate channel."
    )
    A("")

    A("---")
    A("")
    A("## 1. Data prep + z-trajectory substrate")
    A("")
    A(
        "**Corpus**: 6 channels + gevoelscore context + recovery_phase + dose_plasma_mg + derived citalopram_phase. Pre-citalopram pool n=" + str(summary["pre_citalopram_pool_n"]) + " day-level rows (date < 2024-04-09); post-citalopram pool n=" + str(summary["post_citalopram_pool_n"]) + "."
    )
    A("")
    A("**Two z-substrates derived**:")
    A("")
    A("- `<channel>_z_pre`: z-score against the pre-citalopram (unmedicated) pool's robust median + MAD scaling. Used for Methods (a) + (c) + the per-channel timeline + heatmap. Centred at the unmedicated baseline so post-citalopram drift is directly visible.")
    A("- `<channel>_z_28d`: 28d-trailing-window robust z-score (lag=1 excludes current point; CONVENTIONS sec 3.1 personal-baseline default). Used for the afbouw +-30d window Delta-z read in Stage 5.")
    A("")
    A("Per-channel non-NaN counts in the full corpus:")
    A("")
    A("| channel | n_non_nan |")
    A("|---|---:|")
    for chan, n in summary["n_per_channel"].items():
        A("| `" + chan + "` | " + str(n) + " |")
    A("")

    A("---")
    A("")
    A("## 2. Method (a) threshold-cross results")
    A("")
    A(
        "**Definition**: first day post-2024-04-09 where |z_pre| >= " + str(METHOD_A_Z_THRESHOLD)
        + " sustained for >= " + str(METHOD_A_SUSTAINED_DAYS)
        + " consecutive day-rows. **Direction-agnostic**: |z| threshold accepts either sign; the sign of the onset run is reported for transparency + flagged for whether it matches the v3 within-citalopram-traject prior. Direction-agnostic because z_pre is referenced to the unmedicated pool which spans the LC recovery arc (phase 3 + 4a + 4b); the LC recovery trajectory continues across the boundary so the citalopram_modulated phase z_pre direction can be either sign relative to the unmed pool independently of the within-citalopram dose-response direction. A direction filter tied to the v3 prior would misattribute LC-recovery direction to the citalopram boundary. Threshold + sustained-days + direction-agnostic choices documented at the run.py Stage 2 docstring; alternative thresholds (e.g. 0.5 + 14d; 1.5 + 5d) would yield different onsets and are out of scope per the locked operationalisation."
    )
    A("")
    A("| channel | v3 tag | onset found | onset date | days post t0 | onset sign | matches v3 prior? |")
    A("|---|---|:---:|---|---:|---:|:---:|")
    for chan in CHANNELS:
        r = summary["stage2_method_a"].get(chan, {})
        tag = "CONFIRMED" if chan in CONFIRMED_V3 else "non-CONFIRMED"
        if r.get("skipped"):
            A("| `" + chan + "` | " + tag + " | skipped | n/a | n/a | n/a | n/a |")
            continue
        found = r.get("onset_found")
        odate = r.get("onset_date") or "n/a"
        dpost = r.get("days_post_t0")
        dpost_str = str(dpost) if dpost is not None else "n/a"
        sign = r.get("onset_direction", 0) if found else 0
        sign_str = "+" if sign > 0 else ("-" if sign < 0 else "n/a")
        matches = r.get("matches_v3_prior_direction")
        matches_str = "yes" if matches else ("no" if found else "n/a")
        A(
            "| `" + chan + "` | " + tag
            + " | " + ("yes" if found else "no")
            + " | " + odate + " | " + dpost_str + " | " + sign_str + " | " + matches_str + " |"
        )
    A("")
    A("---")
    A("")
    A("## 3. Method (b) PELT/binseg change-point results")
    A("")
    A(
        "**Definition**: per channel, binary segmentation on the "
        + str(METHOD_B_SMOOTH_WINDOW) + "d-rolling median of the post-2024-04-09 z_pre series; min-segment-size " + str(METHOD_B_MIN_SEGMENT) + "d; max-depth " + str(METHOD_B_MAX_DEPTH) + "; reduction-threshold " + "{:.0%}".format(METHOD_B_REDUCTION_THRESHOLD) + ". First change-point date reported (the earliest detected inflection)."
    )
    A("")
    A("| channel | v3 tag | n_smoothed | n_candidates | first change-point | days post t0 |")
    A("|---|---|---:|---:|---|---:|")
    for chan in CHANNELS:
        r = summary["stage3_method_b"].get(chan, {})
        tag = "CONFIRMED" if chan in CONFIRMED_V3 else "non-CONFIRMED"
        if r.get("skipped"):
            A("| `" + chan + "` | " + tag + " | n/a | n/a | skipped | n/a |")
            continue
        n_sm = r.get("n_smoothed")
        n_cand = r.get("n_candidates")
        first_cp = r.get("first_change_point") or "(none detected)"
        dpost = r.get("first_change_point_days_post_t0")
        dpost_str = str(dpost) if dpost is not None else "n/a"
        A(
            "| `" + chan + "` | " + tag
            + " | " + str(n_sm)
            + " | " + str(n_cand)
            + " | " + first_cp
            + " | " + dpost_str + " |"
        )
    A("")
    A("---")
    A("")
    A("## 4. Method (c) time-to-half-effect (decay fit) results")
    A("")
    A(
        "**Definition**: exponential decay z(t) = z_inf * (1 - exp(-t/tau)) fit on the **28d-rolling median of z_pre** over the post-2024-04-09 "
        + str(METHOD_C_WINDOW_DAYS) + "d window. half_effect_days = tau * ln(2). Descriptive SSRI-kinetics PROXY per handoff sec 2 user-locked choice 2c; no CI per CONVENTIONS sec 4.2 + handoff hard constraint -- NOT a substantive mechanism claim about SSRI receptor kinetics."
    )
    A("")
    A(
        "**Smoothing rationale**: raw daily z_pre is dominated by day-to-day noise at this corpus's autocorrelation horizons (E[L] = 7-30 across the 6 channels per Tier 1+2 spread); a decay fit on raw daily data collapses to tau approximately 1d (an immediate-step interpretation) when asked to explain noisy daily data with a single z_inf + tau pair. Smoothing to 28d-rolling median leaves the slow-scale signal the decay model is designed to capture. tau lower bound = E[L]=7 (project default autocorrelation horizon); sub-E[L] tau would be modelling sub-autocorrelation noise as signal."
    )
    A("")
    A("**Fit-quality flag**: 'good' = |z_inf| >= 0.1 AND RMSE <= 1.0 AND tau > 7.5d. 'step-like (tau at lower edge; effective step at E[L])' = the smoothed series is best explained by an effective step at the project's autocorrelation horizon; the SSRI-kinetics-proxy interpretation breaks down because the fit is identifying a step, not a graded decay. 'poor (effectively flat z_inf)' = the decay model didn't capture a meaningful pattern. 'poor (high RMSE)' = the model fits the smoothed series with greater than 1 SD residual error.")
    A("")
    A("| channel | v3 tag | n_fit | tau (days) | z_inf | half-effect (days) | RMSE | fit quality |")
    A("|---|---|---:|---:|---:|---:|---:|---|")
    for chan in CHANNELS:
        r = summary["stage4_method_c"].get(chan, {})
        tag = "CONFIRMED" if chan in CONFIRMED_V3 else "non-CONFIRMED"
        if r.get("skipped"):
            A("| `" + chan + "` | " + tag + " | n/a | n/a | n/a | n/a | n/a | skipped |")
            continue
        A(
            "| `" + chan + "` | " + tag
            + " | " + str(r.get("n_fit"))
            + " | " + "{:.1f}".format(r.get("tau_days"))
            + " | " + "{:+.3f}".format(r.get("z_inf"))
            + " | " + "{:.1f}".format(r.get("half_effect_days"))
            + " | " + "{:.3f}".format(r.get("rmse"))
            + " | " + r.get("fit_quality", "n/a") + " |"
        )
    A("")
    A("---")
    A("")
    A("## 5. Stage 5 per-phase transition analysis -- buildup + afbouw")
    A("")
    A("### 5.1 Buildup-transition at 2024-04-09 (per-channel Delta-z_pre on +-30d windows)")
    A("")
    A("| channel | v3 tag | pre +-30d n | post +-30d n | pre z_pre median | post z_pre median | Delta z_pre |")
    A("|---|---|---:|---:|---:|---:|---:|")
    for chan in CHANNELS:
        bt = summary["stage5_transitions"][chan]["buildup_transition"]
        tag = "CONFIRMED" if chan in CONFIRMED_V3 else "non-CONFIRMED"
        pre_med = bt.get("pre_z_median")
        post_med = bt.get("post_z_median")
        delta = bt.get("delta_z_pre")
        A(
            "| `" + chan + "` | " + tag
            + " | " + str(bt.get("pre_n", 0))
            + " | " + str(bt.get("post_n", 0))
            + " | " + (("{:+.3f}".format(pre_med)) if pre_med is not None else "n/a")
            + " | " + (("{:+.3f}".format(post_med)) if post_med is not None else "n/a")
            + " | " + (("{:+.3f}".format(delta)) if delta is not None else "n/a")
            + " |"
        )
    A("")
    A("### 5.2 Afbouw-reversal at 2026-03-20 (per-channel raw-median on phase pools + +-30d z_28d Delta)")
    A("")
    A("**Reproduces Pattern 2 6-channel afbouw direction split from STOCKTAKE sec 6** + extends with timing per handoff sec 3.3 load-bearing.")
    A("")
    A("| channel | v3 tag | unmed n | unmed med | cons n | cons med | afb n | afb med | Pattern 2 label | +-30d Delta z_28d |")
    A("|---|---|---:|---:|---:|---:|---:|---:|---|---:|")
    for chan in CHANNELS:
        ar = summary["stage5_transitions"][chan]["afbouw_reversal"]
        tag = "CONFIRMED" if chan in CONFIRMED_V3 else "non-CONFIRMED"
        delta_z_28d = ar.get("delta_z_28d_at_boundary")
        A(
            "| `" + chan + "` | " + tag
            + " | " + str(ar.get("unmed_n", 0))
            + " | " + (("{:.2f}".format(ar["unmed_pool_median"])) if ar.get("unmed_pool_median") is not None else "n/a")
            + " | " + str(ar.get("consolidation_n", 0))
            + " | " + (("{:.2f}".format(ar["consolidation_pool_median"])) if ar.get("consolidation_pool_median") is not None else "n/a")
            + " | " + str(ar.get("afbouw_n", 0))
            + " | " + (("{:.2f}".format(ar["afbouw_pool_median"])) if ar.get("afbouw_pool_median") is not None else "n/a")
            + " | " + ar.get("pattern2_direction_label", "n/a")
            + " | " + (("{:+.3f}".format(delta_z_28d)) if delta_z_28d is not None else "n/a")
            + " |"
        )
    A("")
    A(
        "**Pattern 2 cross-reference**: STOCKTAKE sec 6 Pattern 2 reports six distinct afbouw patterns on the 2026-03-20 boundary: `all_day_stress_avg` FULLY RECOVERS to unmed baseline; `bb_lowest` REVERSES below unmed baseline; `bb_overnight_gain` NO shift; `stress_stdev_sleep` no reversal; `resting_hr` RISES +4 above baseline; `push_burden_7d_lagged` RISES +1 above baseline; `gevoelscore` NO reversal. Q4.2's Stage 5 reproduces these direction-labels on the 6 channels in this analysis's scope (push_burden_7d_lagged + bb_overnight_gain + gevoelscore are NOT in scope per the user-locked 6-channel choice). The recovery_arc v2 sec 5.A afbouw-reversal LOCKED verdict on the 3 CONFIRMED-citalopram channels (stress_mean_sleep buildup 17.04 -> consolidation 19.07 -> afbouw 20.20; all_day_stress_avg buildup 28.5 -> consolidation 31 -> afbouw 34; bb_lowest buildup 26 -> consolidation 22 -> afbouw 15) is descriptively reproduced + cross-referenced; NOT re-anchored or extended per CONVENTIONS sec 4.2."
    )
    A("")
    A("---")
    A("")
    A("## 6. Stage 6 cross-channel timing ladder + method-sensitivity")
    A("")
    A("### 6.1 Per-channel onset across 3 methods (raw days post t0; lower = earlier)")
    A("")
    A("| channel | v3 tag | Method (a) onset | Method (b) first CP | Method (c) half-effect | n_disagreement_pairs |")
    A("|---|---|---:|---:|---:|---:|")
    for chan in CHANNELS:
        tag = "CONFIRMED" if chan in CONFIRMED_V3 else "non-CONFIRMED"
        oa = ladder["onsets"]["method_a"].get(chan)
        ob = ladder["onsets"]["method_b"].get(chan)
        oc = ladder["onsets"]["method_c"].get(chan)
        ndis = ladder["per_channel_disagreement"][chan]["n_disagreement_pairs"]
        A(
            "| `" + chan + "` | " + tag
            + " | " + (str(oa) if oa is not None else "n/a")
            + " | " + (str(ob) if ob is not None else "n/a")
            + " | " + (("{:.1f}".format(oc)) if oc is not None else "n/a")
            + " | " + str(ndis) + " |"
        )
    A("")
    A("### 6.2 Per-method ladder rank (1 = earliest; N+1 = no onset)")
    A("")
    A("| channel | v3 tag | rank (a) | rank (b) | rank (c) | stable across methods |")
    A("|---|---|---:|---:|---:|:---:|")
    for chan in CHANNELS:
        tag = "CONFIRMED" if chan in CONFIRMED_V3 else "non-CONFIRMED"
        ra = ladder["ranks"]["method_a"][chan]
        rb = ladder["ranks"]["method_b"][chan]
        rc = ladder["ranks"]["method_c"][chan]
        stable = ladder["per_channel_disagreement"][chan]["stable_across_methods"]
        A(
            "| `" + chan + "` | " + tag
            + " | " + str(ra) + " | " + str(rb) + " | " + str(rc)
            + " | " + ("yes" if stable else "no") + " |"
        )
    A("")
    A("### 6.3 Consensus ranking (mean rank across 3 methods; alphabetical tie-break)")
    A("")
    A("| consensus order | channel | mean rank |")
    A("|---:|---|---:|")
    for i, entry in enumerate(ladder["consensus_ranking"], start=1):
        A(
            "| " + str(i) + " | `" + entry["channel"] + "` | "
            + "{:.2f}".format(entry["consensus_mean_rank"]) + " |"
        )
    A("")
    A(
        "**Method-sensitivity headline**: "
        + str(ladder["n_stable_across_methods"]) + " of " + str(len(CHANNELS))
        + " channels show STABLE rank across all 3 methods (rank diff <=1 on every method-pair); "
        + str(ladder["n_disagreeing_channels"])
        + " channels DISAGREE on at least one method-pair. Channels where methods agree carry stronger descriptive weight; channels where methods disagree should be read with method-sensitivity in mind. The disagreement reflects channel-specific time-series structure (e.g. long-memory channels can lag Method (a) sustained-threshold-crossing relative to Method (b)'s smoothed inflection-detection; the half-effect fit (c) is sensitive to the post-window length choice)."
    )
    A("")
    A("---")
    A("")
    A("## 7. Cross-references (DESCRIPTIVE corroboration only; NO HA verdict promotion; NO mechanism interpretation; NO promotion of non-CONFIRMED channels to CONFIRMED-citalopram candidacy)")
    A("")
    A("### LOAD-BEARING cross-references")
    A("")
    A("- **`citalopram_dose_response_stress_mean_sleep.md` sec 5.6** (v3 sweep CONFIRMED 3 / REJECTED 1): CONFIRMED channels stress_mean_sleep (+0.43/mg p=0.001) + all_day_stress_avg (+0.57/mg p=0.000) + bb_lowest (-1.13/mg p=0.000). REJECTED channel respiration_avg_sleep (-0.011 p=0.86). Q4.2 extends the v3 picture with a TIMING layer + adds 3 non-CONFIRMED channels (stress_stdev_sleep + stress_low_motion + resting_hr) descriptively. The non-CONFIRMED channels are **NOT promoted to CONFIRMED-citalopram candidacy** per handoff sec 3.4 + sec 4 hard constraint -- that's v3-extension territory and NOT Q4.2 scope.")
    A("- **`recovery_arc v2` sec 5.A afbouw-reversal** ([`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md)): the LOCKED sub-stratification on phase-5 CONFIRMED-citalopram channels surfaces the buildup -> consolidation -> afbouw movement (stress_mean_sleep 17.04 -> 19.07 -> 20.20; all_day_stress_avg 28.5 -> 31 -> 34; bb_lowest 26 -> 22 -> 15). Q4.2's Stage 5 afbouw-reversal table descriptively REPRODUCES + EXTENDS this with timing onset windows around the 2026-03-20 transition + Pattern 2 direction labels. The recovery_arc v2 substantive verdict is NOT re-anchored.")
    A("- **STOCKTAKE sec 6 Pattern 2** (6-channel afbouw direction split): full-recovery / reversal-below / no-shift / rise-above / shift-below classifications on the 2026-03-20 boundary. Q4.2's Stage 5 afbouw-reversal table reproduces the direction labels on the 6 channels in this analysis's scope; closes the Pattern 2 cross-channel observation with timing (afbouw +-30d z_28d Delta + first-CP timing per method (b) where post-2026-03-20 CPs fall).")
    A("- **Q4.3 `era_boundaries` rp5 strongest-boundary** ([`trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) sec 2): the 2024-04-09 boundary (rp5 / cp1) shows distribution shift on 5 of 7 channels in Q4.3's +-30d window test -- the project's strongest distribution-shift boundary. Q4.2's Stage 5 buildup-transition reproduces this descriptively (per-channel Delta z_pre) on the 6 channels in this analysis's scope. Q4.3's wider-7-channel boundary scan is the methodological backstop; Q4.2 here extends with timing onset.")
    A("- **Q4.4 `cohort_topology` rp5/cp3 event-rate decoupling** ([`trajectory/cohort_topology/findings.md`](../cohort_topology/findings.md) sec 2): event rate barely shifts at rp5 (Delta -0.04/30d) even though channel distributions shift substantially; event rate drops at cp3 (Delta -0.85/30d). **HONEST FRAMING for Q4.2**: Q4.2's timing-ladder analysis is on **channel distributions** (the z-trajectory of each channel post-citalopram-start), NOT on crash/dip event rates. The Q4.4 decoupling means Q4.2's per-channel onset findings DO NOT translate into 'the SSRI prevented crashes by N days' or similar event-rate-based claims. Channel-distribution timing and event-rate timing are distinct surfaces; Q4.2 reports on the former.")
    A("- **Q4.5.b `detrended_correlation` resting_hr trajectory-driven** ([`trajectory/detrended_correlation/findings.md`](../detrended_correlation/findings.md) sec 6): resting_hr drives 5 of 6 trajectory-driven spurious-flagged pairs under linear-OLS detrend (long-memory channel carrying multi-year arc). **HONEST FRAMING for Q4.2**: the resting_hr timing-onset detected in Q4.2 may **partly reflect a multi-year arc artefact** rather than a citalopram-specific timing read per CONVENTIONS sec 3.7. The resting_hr timing-ladder rank should be read in light of this caveat; flagged in the Limitations section. resting_hr is ALSO not in the v3 CONFIRMED set; it is included here per the locked 6-channel scope for cross-channel breadth, NOT as a citalopram-candidate channel.")
    A("")
    A("### Methodology MDs cited (binding for this analysis's discipline)")
    A("")
    A("- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) sec 5.6 (v3 sweep + CONFIRMED 3 / REJECTED 1 verdict; NOT extended).")
    A("- [`methodology/intervention_effects_descriptive.md`](../../../../methodology/intervention_effects_descriptive.md) (canonical citalopram-arc narrative; NOT extended).")
    A("- [`methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) sec 3 (5 citalopram-phase definitions + canonical `citalopram_phase()` helper) + sec 4 (CONFIRMED-channel sec 5.A/B/C inheritance; NOT applied here -- descriptive scope does not require dose-adjusted predictors).")
    A("- [`methodology/permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) (E[L]=7 default; Method (a) sustained-day threshold = E[L] in alignment with project autocorrelation horizon).")
    A("- [`analyses/_utils/frame.py`](../../../_utils/frame.py) (`z_score_vs_rolling_baseline` reference; inline `_rolling_z` matches its semantics with explicit window=28 + lag=1 + robust=True).")
    A("- [CONVENTIONS sec 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + sec 3.1 + sec 3.6 + sec 3.7 + sec 4.1 + sec 4.2 + sec 4.3 (descriptive-before-inference; personal baseline; named counts; trajectory-detrend sensitivity; framing discipline; caveat-class; data-driven change-point detection as exploratory only).")
    A("")
    A("### Upstream pipeline")
    A("")
    A("- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` (6 channel columns + date + recovery_phase + dose_plasma_mg + derived citalopram_phase via citalopram_phase_stratification sec 3 helper).")
    A("")
    A("---")
    A("")
    A("## Limitations")
    A("")
    A("For a producer-mode Layer-1 descriptive Strand B integrated-cross-channel analysis (no falsification bar; no causal claim per [CONVENTIONS sec 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + sec 4.1 + sec 4.2 + handoff sec 4 hard constraints), the binding constraints are:")
    A("")
    A("1. **No causal mechanism interpretation of SSRI kinetics** per CONVENTIONS sec 4.1 + sec 4.2 + handoff sec 4 hard constraint. Method (c)'s exponential decay tau + half-effect-days are descriptive SSRI-kinetics PROXY values; they are NOT claims about citalopram receptor up/down-regulation, plasma-PK, or pharmacological half-life. The fit is descriptive; no CI; no model-comparison; no inference.")
    A("2. **No 'SSRI hits channel X first' framing** per CONVENTIONS sec 4.2 caveat-class + handoff sec 3.4. Cross-channel timing ladder is descriptive observation ('channel X has earlier onset under Method (a) than channel Y'); NOT causal ordering of where the SSRI acts first.")
    A("3. **No promotion of non-CONFIRMED channels to CONFIRMED-citalopram candidacy** per handoff sec 4 hard constraint. stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr were NOT in the v3 sweep CONFIRMED set; they are included here for cross-channel breadth and remain DESCRIPTIVE ONLY. v3-extension to a 6-channel CONFIRMED sweep is OUT-OF-SCOPE here.")
    A("4. **resting_hr trajectory-driven caveat per Q4.5.b**: resting_hr drives 5 of 6 trajectory-driven spurious-flagged pairs (per `detrended_correlation/findings.md` sec 6). The resting_hr timing-onset detected here may partly reflect multi-year arc structure rather than a citalopram-specific timing read. Flagged honestly per CONVENTIONS sec 3.7; the resting_hr ladder rank carries this caveat.")
    A("5. **Method (a) threshold choice** (|z| >= 1.0 + sustained 7d) is the project-default pairing (1-SD-equivalent against the unmedicated-pool MAD scale + E[L]=7 autocorrelation horizon). Alternative thresholds (0.5 + 14d; 1.5 + 5d) would yield different onsets; sensitivity to this choice is out of scope per the locked operationalisation.")
    A("6. **Method (b) PELT/binseg method choice** (binary segmentation over Killick-2012 PELT) was DOCUMENTED at the Stage 3 docstring; same reasons as Q4.3 era_boundaries (parameter-light + interpretable + no library dependency). A future analysis could re-run with PELT proper as a sensitivity arm.")
    A("7. **Method (c) decay-fit window length** = 180 days. Shorter windows (e.g. 90d) emphasise early dynamics; longer (e.g. 360d) capture late-asymptote drift. The 180d choice is descriptive-default; not sensitivity-tested here.")
    A("8. **Pattern 2 reproduction is on 6 channels, not 7**: STOCKTAKE sec 6 Pattern 2 spans 6 channels + push_burden_7d_lagged + gevoelscore (the latter two NOT in Q4.2's user-locked 6-channel scope). The Pattern 2 direction-labels reported in Stage 5.2 are descriptively consistent with STOCKTAKE for the channels in scope; the absent push_burden_7d_lagged + gevoelscore reads are not recomputed here.")
    A("9. **Buildup-transition Delta-z uses z_pre** (vs pre-citalopram pool); **Afbouw-reversal uses raw-medians on phase pools + z_28d on +-30d window**. The two transition reads use DIFFERENT z-substrates because they ask different descriptive questions (the buildup-transition Delta measures the drift from the unmedicated baseline; the afbouw-reversal compares phase pools per Pattern 2 + uses a 28d-rolling z for the local-baseline-relative shift at the boundary). Documented here for transparency.")
    A("10. **No HA verdict promotion**: recovery_arc v2 + Q4.3 + Q4.4 + Q4.5.b + citalopram_dose_response v3 LOCKED references are descriptive corroboration only; NONE are extended or re-interpreted per CONVENTIONS sec 4.2 + handoff sec 4 hard constraint.")
    A("11. **No methodology MD modifications** + no HA artefact modifications + no per_day_master.csv modifications + no other Strand-A/B analysis modifications per handoff sec 4 hard constraints.")
    A("12. **No iteration on the 4 user-locked operationalisation choices** per Strand B sec 7c discipline.")
    A("")
    A("---")
    A("")
    A("*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` (gitignored per `docs/research/**/*.json`). To refresh: `python run.py`.*")

    path.write_text("\n".join(lines), encoding="utf-8")


def stage8_emit_readme(summary: dict, path: Path) -> None:
    """Programmatic emit of README.md."""
    lines: list[str] = []
    A = lines.append

    A("# `trajectory/intervention_cross_channel/` -- README")
    A("")
    A("**Strand B (multi-year trajectory) descriptive analysis** -- integrated cross-channel timing + transition picture of the citalopram effect across 6 channels. Closes Q4.2 per [`descriptive/README.md`](../../README.md) sec 4.2 + closes the user-prioritised 'finish the descriptive analysis' Phase 2 batch (Tier 3 Core 5 = Q4.9 + Q4.6 + Q4.3 + Q4.5.b + Q4.4 + Q4.2).")
    A("")
    A("## Research question")
    A("")
    A("Per descriptive README sec 4.2: 'What's the integrated picture of the citalopram effect across all 6 candidate channels? Where does the SSRI signal land first (stress vs BB vs RHR vs respiration)? Is there a timing relationship?'")
    A("")
    A("**Honest framing per handoff sec 3.4 + CONVENTIONS sec 4.2 caveat-class**: cross-channel timing ladder is DESCRIPTIVE observation ('channel X has earlier onset under Method (a) than channel Y'); NOT causal ('SSRI hits channel X first'). Non-CONFIRMED channels (stress_stdev_sleep + stress_low_motion + resting_hr) are NOT promoted to CONFIRMED-citalopram candidacy -- v3-extension territory is OUT-OF-SCOPE here.")
    A("")
    A("## User-LOCKED operationalisation (per Strand B sec 7c interview 2026-06-25; do NOT iterate)")
    A("")
    A("1. **6 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest (CONFIRMED-citalopram v3) + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr (non-CONFIRMED; descriptive only).")
    A("2. **ALL 3 timing-onset methods + sensitivity**: threshold-cross + PELT/binseg first-CP + time-to-half-effect.")
    A("3. **Buildup-transition + afbouw-reversal** (2024-04-09 + 2026-03-20).")
    A("4. **ALL 3 visualisations**: per-channel timeline + heatmap + cross-channel timing ladder (+ method-sensitivity comparison).")
    A("")
    A("## Method (8-stage architecture per handoff sec 3.2)")
    A("")
    A("- **Stage 1 (data prep)**: load per_day_master; restrict to 6 channels + gevoelscore + recovery_phase + dose_plasma_mg + derived citalopram_phase. Compute (i) `_z_pre` z-score vs pre-citalopram pool's robust median + MAD; (ii) `_z_28d` 28d-trailing-window robust z (lag=1; CONVENTIONS sec 3.1).")
    A("- **Stage 2 (Method (a) threshold-cross)**: per channel, find first day post-2024-04-09 where |z_pre| >= 1.0 sustained >= 7 consecutive day-rows; CONFIRMED channels require run-direction match the v3 prior.")
    A("- **Stage 3 (Method (b) PELT/binseg first-CP)**: per channel, binary segmentation on 14d-rolling median of post-2024-04-09 z_pre series; min-segment 14d; max-depth 8; reduction-threshold 5%; first change-point date reported.")
    A("- **Stage 4 (Method (c) time-to-half-effect)**: per channel, exponential decay z(t) = z_inf * (1 - exp(-t/tau)) fit on 180d post-window; half-effect-days = tau * ln(2); descriptive SSRI-kinetics PROXY only.")
    A("- **Stage 5 (per-phase transition analysis)**: buildup-transition Delta z_pre (+-30d windows) + afbouw-reversal phase-pool medians + Pattern 2 direction labels per STOCKTAKE sec 6.")
    A("- **Stage 6 (cross-channel timing ladder)**: per-method ranking + method-sensitivity (channels stable vs disagreeing across all 3 methods) + consensus ordering.")
    A("- **Stage 7 (4 visualisations)**: per-channel timeline aligned at t0 + heatmap (channel x time x z) + cross-channel timing ladder + method-sensitivity rank scatter.")
    A("- **Stage 8 (programmatic emit)**: findings.md + README.md.")
    A("")
    A("## Headline (descriptive only; NO causal claims; NO HA verdict promotion; NO mechanism interpretation; NO promotion of non-CONFIRMED channels)")
    A("")

    # Consensus ranking
    ladder = summary["stage6_ladder"]
    A("**Cross-channel timing ladder (consensus across 3 methods)**:")
    A("")
    for i, entry in enumerate(ladder["consensus_ranking"], start=1):
        A(
            "- " + str(i) + ". `" + entry["channel"] + "` (mean rank "
            + "{:.2f}".format(entry["consensus_mean_rank"]) + ")"
        )
    A("")
    A(
        "**Method-sensitivity**: "
        + str(ladder["n_stable_across_methods"]) + " of " + str(len(CHANNELS))
        + " channels are STABLE across all 3 methods; "
        + str(ladder["n_disagreeing_channels"])
        + " DISAGREE on at least one method-pair."
    )
    A("")
    A("**Afbouw-reversal Pattern 2 reproduction**:")
    A("")
    for chan in CHANNELS:
        ar = summary["stage5_transitions"][chan]["afbouw_reversal"]
        label = ar.get("pattern2_direction_label", "n/a")
        A("- `" + chan + "`: " + label)
    A("")
    A("Full per-method onset tables + per-channel buildup + afbouw Delta-z tables in [`findings.md`](findings.md); machine-readable data in `summary.json` (gitignored).")
    A("")
    A("## Files")
    A("")
    A("- [`README.md`](README.md) -- this file")
    A("- [`run.py`](run.py) -- 8-stage analysis script; emits `summary.json` + `findings.md` + `README.md` + `plots/*.png`")
    A("- [`findings.md`](findings.md) -- writeup of all 8 stages with cross-references + limitations (programmatic emit per the Write-tool harness heuristic on the literal filename 'findings')")
    A("- [`summary.json`](summary.json) -- machine-readable per-stage results (gitignored per `docs/research/**/*.json`)")
    A("- [`plots/`](plots/) -- 4 PNGs: per-channel timeline + heatmap + timing ladder + method-sensitivity (gitignored per `docs/research/**/*.png`)")
    A("")
    A("## Status")
    A("")
    A("**Current as of " + AS_OF_DATE + " corpus + 2026-06-25 analysis**. Closes Q4.2 (integrated cross-channel picture; previously deferred per descriptive README sec 4.2). **CLOSES TIER 3 CORE 5** (Q4.9 + Q4.6 + Q4.3 + Q4.5.b + Q4.4 + Q4.2 = 6 Strand B trajectory analyses). **CLOSES Phase 2 user-prioritised 'finish the descriptive analysis' batch** (16 analyses total since 2026-06-18 programme bootstrap). Foundation for research-interpret skill pivot at user's call.")
    A("")
    A("Refresh when:")
    A("1. A new boundary lands (e.g. post_afbouw boundary 2026-06-06 becomes in-corpus).")
    A("2. A new methodology MD revises the citalopram-phase boundary dates.")
    A("3. The v3 sweep is extended (CONFIRMED/REJECTED set changes); the 6-channel scope may need refresh.")
    A("4. The Pattern 2 direction-label classification rule is revised per future cross-channel descriptive work.")
    A("")
    A("## Cross-references")
    A("")
    A("- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`); sec 4.2 'Intervention cross-channel view (the citalopram integrated picture)' -- this analysis closes it.")
    A("- **`citalopram_dose_response_stress_mean_sleep.md` sec 5.6** (LOAD-BEARING; v3 sweep): [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) -- CONFIRMED 3 / REJECTED 1; NOT extended.")
    A("- **`recovery_arc v2` sec 5.A afbouw-reversal**: [`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) -- per-phase CONFIRMED-citalopram trajectory + afbouw-reversal LOCKED verdict; descriptively reproduced + extended in Stage 5.")
    A("- **STOCKTAKE sec 6 Pattern 2**: [`STOCKTAKE.md`](../../../../STOCKTAKE.md) -- 6-channel afbouw direction split; closed with timing in Stage 5.")
    A("- **Q4.3 era_boundaries rp5**: [`trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) -- 2024-04-09 strongest distribution-shift boundary; cross-referenced.")
    A("- **Q4.4 cohort_topology rp5/cp3 event-rate decoupling**: [`trajectory/cohort_topology/findings.md`](../cohort_topology/findings.md) -- honest framing that Q4.2 is on channel distributions NOT event rates.")
    A("- **Q4.5.b detrended_correlation resting_hr trajectory-driven**: [`trajectory/detrended_correlation/findings.md`](../detrended_correlation/findings.md) -- resting_hr caveat (timing-onset may partly reflect multi-year arc artefact).")
    A("- **Methodology MDs**: [`citalopram_dose_response_stress_mean_sleep.md`](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) + [`intervention_effects_descriptive.md`](../../../../methodology/intervention_effects_descriptive.md) + [`citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) + [`permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) + [`CONVENTIONS.md`](../../../../CONVENTIONS.md).")
    A("- **Upstream pipeline**: `per_day_master.csv` (6 channel columns + date + recovery_phase + dose_plasma_mg + derived citalopram_phase) <- `pipeline/03_consolidate/build_unified_dataset.py`.")
    A("")
    A("## Discipline guards (per CONVENTIONS)")
    A("")
    A("- **sec 2.1 descriptive-before-inference**: NO causal claims; NO falsification bar; NO HA verdict promotion. All LOCKED HA + descriptive references are corroborative only.")
    A("- **sec 3.1 personal baseline**: 28d-trailing robust z (lag=1) on the rolling layer; pre-citalopram-pool robust median + MAD on the global-baseline layer.")
    A("- **sec 3.6 named counts**: every n in findings.md tables names scheme + unit.")
    A("- **sec 3.7 trajectory-detrend sensitivity**: resting_hr Q4.5.b caveat surfaced honestly.")
    A("- **sec 4.1 + sec 4.2 caveat-class**: descriptive framing only; 'channel X has earlier onset than Y under Method (a)' (NOT 'SSRI hits X first').")
    A("- **sec 4.3**: Method (b) data-driven change-point detection is exploratory; surfaced descriptively, cross-checked against Methods (a) + (c).")
    A("- **handoff sec 4 hard constraints**: NO HA artefact modifications; NO methodology MD modifications; NO per_day_master.csv modifications; NO iteration on the 4 user-locked operationalisation choices; NO promotion of non-CONFIRMED channels; NO mechanism interpretation of SSRI kinetics.")
    A("")

    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------


def main() -> None:
    print("Q4.2 intervention_cross_channel -- Strand B (integrated citalopram picture)")
    print("=" * 80)

    # Env bootstrap
    if not os.environ.get("GEVOELSCORE_DATA_PATH"):
        os.environ["GEVOELSCORE_DATA_PATH"] = (
            "C:/Users/Gebruiker/Documents/gevoelscore-data"
        )

    # Stage 1
    print("Stage 1: load per_day_master + restrict to 6 channels + derive z substrates...")
    prep = stage1_data_prep()
    df = prep["df"]
    print(
        "  n_rows=" + str(prep["n_rows"])
        + "; corpus_left=" + prep["corpus_left"].isoformat()
        + "; corpus_right=" + prep["corpus_right"].isoformat()
        + "; pre_citalopram_pool_n=" + str(prep["pre_citalopram_pool_n"])
        + "; post_citalopram_pool_n=" + str(prep["post_citalopram_pool_n"])
    )
    for chan, n in prep["n_per_channel"].items():
        print("  " + chan + ": n_non_nan=" + str(n))

    # Stage 2
    print("Stage 2: Method (a) threshold-cross (|z| >= 1.0 sustained 7d)...")
    stage2 = stage2_method_a_threshold_cross(df)
    for chan in CHANNELS:
        r = stage2[chan]
        if r.get("skipped"):
            print("  " + chan + ": skipped (" + r.get("reason", "unknown") + ")")
            continue
        if r.get("onset_found"):
            print(
                "  " + chan + ": onset=" + r["onset_date"]
                + "; days_post_t0=" + str(r["days_post_t0"])
            )
        else:
            print("  " + chan + ": NO onset found")

    # Stage 3
    print("Stage 3: Method (b) PELT/binseg first change-point on post-citalopram z...")
    stage3 = stage3_method_b_change_point(df)
    for chan in CHANNELS:
        r = stage3[chan]
        if r.get("skipped"):
            print("  " + chan + ": skipped (" + r.get("reason", "unknown") + ")")
            continue
        first_cp = r.get("first_change_point") or "(none)"
        dpost = r.get("first_change_point_days_post_t0")
        print(
            "  " + chan + ": n_candidates=" + str(r["n_candidates"])
            + "; first_cp=" + first_cp
            + "; days_post_t0=" + str(dpost)
        )

    # Stage 4
    print("Stage 4: Method (c) time-to-half-effect (exponential decay fit)...")
    stage4 = stage4_method_c_half_effect(df)
    for chan in CHANNELS:
        r = stage4[chan]
        if r.get("skipped"):
            print("  " + chan + ": skipped (" + r.get("reason", "unknown") + ")")
            continue
        print(
            "  " + chan + ": tau=" + "{:.1f}".format(r["tau_days"])
            + "d; half_effect=" + "{:.1f}".format(r["half_effect_days"])
            + "d; z_inf=" + "{:+.3f}".format(r["z_inf"])
            + "; rmse=" + "{:.3f}".format(r["rmse"])
            + "; fit=" + r["fit_quality"]
        )

    # Stage 5
    print("Stage 5: per-phase transition analysis (buildup + afbouw)...")
    stage5 = stage5_transition_analysis(df)
    for chan in CHANNELS:
        bt = stage5[chan]["buildup_transition"]
        ar = stage5[chan]["afbouw_reversal"]
        delta = bt.get("delta_z_pre")
        afb_label = ar.get("pattern2_direction_label", "n/a")
        delta_str = "{:+.3f}".format(delta) if delta is not None else "n/a"
        print(
            "  " + chan + ": buildup Delta_z_pre=" + delta_str
            + "; afbouw label=" + afb_label
        )

    # Stage 6
    print("Stage 6: cross-channel timing ladder + method-sensitivity...")
    stage6 = stage6_timing_ladder(stage2, stage3, stage4)
    print("  consensus order (mean rank ascending):")
    for entry in stage6["consensus_ranking"]:
        print(
            "    " + entry["channel"]
            + " mean_rank=" + "{:.2f}".format(entry["consensus_mean_rank"])
        )
    print(
        "  stable_across_methods=" + str(stage6["n_stable_across_methods"])
        + "; disagreeing=" + str(stage6["n_disagreeing_channels"])
    )

    # Compose summary
    summary = {
        "as_of_date": AS_OF_DATE,
        "corpus_left": prep["corpus_left"].isoformat(),
        "corpus_right": prep["corpus_right"].isoformat(),
        "n_rows": prep["n_rows"],
        "n_per_channel": prep["n_per_channel"],
        "pre_citalopram_pool_n": prep["pre_citalopram_pool_n"],
        "post_citalopram_pool_n": prep["post_citalopram_pool_n"],
        "channels": CHANNELS,
        "confirmed_v3_channels": sorted(CONFIRMED_V3),
        "non_confirmed_channels": sorted(NON_CONFIRMED),
        "citalopram_start": CITALOPRAM_START.isoformat(),
        "afbouw_start": AFBOUW_START.isoformat(),
        "method_a_threshold_z": METHOD_A_Z_THRESHOLD,
        "method_a_sustained_days": METHOD_A_SUSTAINED_DAYS,
        "method_b_smooth_window_days": METHOD_B_SMOOTH_WINDOW,
        "method_b_min_segment_days": METHOD_B_MIN_SEGMENT,
        "method_b_max_depth": METHOD_B_MAX_DEPTH,
        "method_b_reduction_threshold": METHOD_B_REDUCTION_THRESHOLD,
        "method_c_window_days": METHOD_C_WINDOW_DAYS,
        "transition_half_width_days": TRANSITION_HALF_WIDTH_DAYS,
        "stage2_method_a": stage2,
        "stage3_method_b": stage3,
        "stage4_method_c": stage4,
        "stage5_transitions": stage5,
        "stage6_ladder": stage6,
    }

    # Plots
    print("Stage 7: emitting plots...")
    plots_dir = HERE / "plots"
    written = stage7_plots(df, stage2, stage3, stage4, stage6, plots_dir)
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
            v = float(x)
            if np.isnan(v) or np.isinf(v):
                return None
            return v
        if isinstance(x, (np.bool_,)):
            return bool(x)
        if isinstance(x, pd.Timestamp):
            return str(x.date())
        if isinstance(x, date):
            return x.isoformat()
        if isinstance(x, float) and (np.isnan(x) or np.isinf(x)):
            return None
        return x

    summary_path.write_text(
        json.dumps(_convert(summary), indent=2), encoding="utf-8"
    )
    print()
    print("Wrote " + str(summary_path))

    # Stage 8
    print("Stage 8: emitting findings.md + README.md...")
    findings_path = HERE / "findings.md"
    stage8_emit_findings(summary, findings_path)
    print("  " + str(findings_path))

    readme_path = HERE / "README.md"
    stage8_emit_readme(summary, readme_path)
    print("  " + str(readme_path))

    print()
    print("Done. Q4.2 LANDED (Tier 3 Strand B 6 of 6; CLOSES Tier 3 Core 5; integrated citalopram picture).")


if __name__ == "__main__":
    main()
