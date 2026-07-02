"""R23 peri-event COVID known-event check: producer-mode test execution.

Implements the LOCKED pre-registration verbatim:
  docs/research/analyses/hypotheses/peri-event-covid/hypothesis.md
  (LOCKED 2026-07-02; any change creates an R23v2).

Question (R23): does the project's overnight autonomic factor visibly
move during the 2022-03 COVID infection window (2022-03-21 to
2022-04-03, 14 days) relative to the pre-LC healthy baseline
(2021-08-16 to 2022-03-20, 217 days, lc_phase == pre_corona)?

Method (all locked in the pre-reg, sections 4 to 6):
  1. Anchor factor-z (primary, g1): daily stress_mean_sleep z-scored
     against the PERSONAL pre-LC baseline using robust median + MAD
     over the 217-day pre-LC band (CONVENTIONS sec 3.1, k = 1.4826).
     Sign convention: upward = high-load pole.
  2. Window statistic: 14-day-window-mean of the daily factor-z, plus a
     window-max companion (max single-day factor-z within the window).
  3. Primary p-analogue: daily-series stationary bootstrap, E[L] = 7.
     Each replicate resamples the daily factor-z series under E[L]=7
     stationary blocks to a synthetic 217-day series, then computes ONE
     14-day-window-mean factor-z from that synthetic series. 10,000
     replicates build the reference distribution. The infection window's
     percentile is the p-analogue (one-sided, high-load direction).
  4. Confirm E[L]* within 2x of 7 (data-driven block-length check).
  5. n=15 non-overlapping sanity rank.
  6. 204 sliding windows: descriptive backdrop ONLY (never a p-value
     denominator; this is the M1 discipline).
  7. Effect size d2: standardised-difference CI from the SAME E[L]=7
     bootstrap machinery.
  8. Triad coherence (g2): each of stress_mean_sleep, bb_highest,
     resting_hr z-scored against its own personal pre-LC baseline;
     coherence flag checks each channel against ITS OWN predicted sign
     (stress_mean_sleep positive, resting_hr positive, bb_highest
     NEGATIVE).
  9. Detrend sec 3.7 sensitivity on the RAW g2 triad channels.
  10. Acute-core overlay (2022-03-23 to 2022-03-30): descriptive only,
      NO separate p-analogue.

No PII. No emojis. No em-dashes.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Reuse the house inference utilities (Politis-Romano stationary bootstrap
# with the geometric-block mechanic, and the Politis-White data-driven
# block-length estimator) so the resampling matches the project pattern.
_UTILS = Path(__file__).resolve().parents[2] / "_utils"
sys.path.insert(0, str(_UTILS.parent))
from _utils.inference import (  # noqa: E402
    compute_data_driven_block_length,
    stationary_bootstrap_ci,
    _stationary_bootstrap_indices,
)

# ----------------------------------------------------------------------------
# Locked constants (all from the pre-reg / precondition; do not change)
# ----------------------------------------------------------------------------

DATA_PATH = r"C:\Users\Gebruiker\Documents\gevoelscore-data\unified\per_day_master.csv"

PRE_LC_PHASE = "pre_corona"          # lc_phase value for the 217-day baseline
PRE_LC_START = "2021-08-16"
PRE_LC_END = "2022-03-20"

INFECTION_START = "2022-03-21"
INFECTION_END = "2022-04-03"         # 14 days inclusive
WINDOW_DAYS = 14

ACUTE_CORE_START = "2022-03-23"      # descriptive overlay only, no p-analogue
ACUTE_CORE_END = "2022-03-30"

# Anchor + triad columns (resolved in the precondition sec 5.1).
ANCHOR_COL = "stress_mean_sleep"     # HA07c, predicted UP
BB_COL = "bb_highest"                # HA10 inverse, predicted DOWN
RHR_COL = "resting_hr"               # HA06b, predicted UP

# Predicted signs per channel (high-load pole). +1 = up, -1 = down.
PREDICTED_SIGN = {ANCHOR_COL: +1, RHR_COL: +1, BB_COL: -1}

MAD_K = 1.4826                       # normal-equivalence scaling (CONVENTIONS sec 3.1)
EXPECTED_BLOCK_LENGTH = 7            # E[L] = 7 (permutation_null_block_length.md)
N_REPLICATES = 10000                 # >= 10,000 per the locked pre-reg
RNG_SEED = 20220321                  # fixed seed, recorded (infection start date)


# ----------------------------------------------------------------------------
# Robust personal-baseline z-score (CONVENTIONS sec 3.1)
# ----------------------------------------------------------------------------


def robust_baseline_params(baseline_values):
    """Return (median, k*MAD) over the fixed pre-LC baseline band.

    Robust z = (x - median) / (k * MAD), k = 1.4826 (CONVENTIONS sec 3.1).
    Raises if MAD is zero (z-score undefined; convention returns NaN, but
    for a fixed 217-day baseline on a real biometric channel this cannot
    happen and a zero would be a data error worth surfacing).
    """
    vals = np.asarray(baseline_values, dtype=float)
    vals = vals[~np.isnan(vals)]
    med = float(np.median(vals))
    mad = float(np.median(np.abs(vals - med)))
    spread = mad * MAD_K
    if spread == 0.0:
        raise ValueError("Baseline MAD is zero; robust z-score undefined")
    return med, spread


def robust_z(values, med, spread):
    """z = (x - median) / (k * MAD). NaN passes through as NaN."""
    return (np.asarray(values, dtype=float) - med) / spread


# ----------------------------------------------------------------------------
# Primary p-analogue: daily-series stationary bootstrap (E[L]=7)
# ----------------------------------------------------------------------------


def bootstrap_window_mean_null(daily_factor_z, *, n_replicates, e_l, window_days, rng):
    """Build the null distribution of the 14-day-window-mean factor-z.

    Per-replicate mechanic (locked, pre-reg sec 5, MINOR-1): each
    replicate resamples the daily factor-z series under E[L] stationary
    blocks to a synthetic 217-day series (same geometric-block mechanic
    as the house stationary_bootstrap_ci, via _stationary_bootstrap_indices),
    then computes ONE 14-day-window-mean factor-z from that synthetic
    series (the leading 14 days of the synthetic series). Repeating
    n_replicates times builds the reference distribution.
    """
    series = np.asarray(daily_factor_z, dtype=float)
    series = series[~np.isnan(series)]
    n = len(series)
    p = 1.0 / e_l
    null = np.empty(n_replicates)
    for b in range(n_replicates):
        idx = _stationary_bootstrap_indices(n, p, rng)
        synthetic = series[idx]
        null[b] = float(synthetic[:window_days].mean())
    return null


# ----------------------------------------------------------------------------
# Detrend sec 3.7 sensitivity on the raw g2 triad channels
# ----------------------------------------------------------------------------


def detrend_window_mean_z(pre_dates_ord, pre_raw, event_dates_ord, event_raw):
    """CONVENTIONS sec 3.7 linear-detrend on the RAW channel.

    Fit a linear trend on the pre-LC window (x = ordinal day), extrapolate
    forward through the infection window, subtract the fitted line from
    both, then re-z-score the detrended event values against the detrended
    pre-LC residual baseline (robust median + MAD) and return the
    infection-window mean of that detrended z. This mirrors the sec 3.7
    procedure (fit on pre, extrapolate, subtract, recompute statistic) but
    keeps the readout on the same window-mean-z scale as the primary so
    the verdict-stability comparison is like-for-like.
    """
    x_pre = np.asarray(pre_dates_ord, dtype=float)
    y_pre = np.asarray(pre_raw, dtype=float)
    ok = ~np.isnan(y_pre)
    slope, intercept = np.polyfit(x_pre[ok], y_pre[ok], deg=1)

    pre_resid = y_pre - (slope * x_pre + intercept)
    x_ev = np.asarray(event_dates_ord, dtype=float)
    ev_resid = np.asarray(event_raw, dtype=float) - (slope * x_ev + intercept)

    med, spread = robust_baseline_params(pre_resid)
    ev_z = robust_z(ev_resid, med, spread)
    return float(np.nanmean(ev_z)), float(slope)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


def main():
    rng = np.random.default_rng(RNG_SEED)

    df = pd.read_csv(DATA_PATH, usecols=["date", "lc_phase", ANCHOR_COL, BB_COL, RHR_COL])
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    pre = df[df["lc_phase"] == PRE_LC_PHASE].copy()
    inf = df[(df["date"] >= INFECTION_START) & (df["date"] <= INFECTION_END)].copy()

    # Guard: coverage / band assertions from the locked precondition.
    assert len(pre) == 217, f"expected 217 pre-LC days, got {len(pre)}"
    assert len(inf) == 14, f"expected 14 infection days, got {len(inf)}"
    assert str(pre["date"].min().date()) == PRE_LC_START
    assert str(pre["date"].max().date()) == PRE_LC_END

    # --- 1. Anchor factor-z against the personal pre-LC baseline ---
    med_anchor, spread_anchor = robust_baseline_params(pre[ANCHOR_COL].values)
    pre_factor_z = robust_z(pre[ANCHOR_COL].values, med_anchor, spread_anchor)
    inf_factor_z = robust_z(inf[ANCHOR_COL].values, med_anchor, spread_anchor)

    # --- 2. Window statistic (mean + max companion) ---
    infection_window_mean = float(np.nanmean(inf_factor_z))
    infection_window_max = float(np.nanmax(inf_factor_z))

    # --- 3. Primary p-analogue: daily-series stationary bootstrap E[L]=7 ---
    null_dist = bootstrap_window_mean_null(
        pre_factor_z,
        n_replicates=N_REPLICATES,
        e_l=EXPECTED_BLOCK_LENGTH,
        window_days=WINDOW_DAYS,
        rng=rng,
    )
    # One-sided percentile in the predicted (high-load, upward) direction:
    # fraction of null window-means at or below the infection window-mean.
    percentile = float(np.mean(null_dist <= infection_window_mean)) * 100.0
    p_analogue_high_load = float(np.mean(null_dist >= infection_window_mean))
    pct_95 = float(np.quantile(null_dist, 0.95))
    pct_05 = float(np.quantile(null_dist, 0.05))

    # --- 4. Data-driven E[L]* check (within 2x of 7?) ---
    el_result = compute_data_driven_block_length(
        pre_factor_z, default_block_length=EXPECTED_BLOCK_LENGTH
    )
    el_star = el_result["optimal_block_length"]
    el_flagged = el_result["flagged_deviation"]

    # --- 5. n=15 non-overlapping sanity rank ---
    # 15 full non-overlapping 14-day windows in the 217-day pre-LC band
    # (217 = 15 * 14 + 7 remainder; the trailing 7 days are not a full window).
    nonoverlap_means = []
    for w in range(15):
        seg = pre_factor_z[w * WINDOW_DAYS : (w + 1) * WINDOW_DAYS]
        nonoverlap_means.append(float(np.nanmean(seg)))
    nonoverlap_means = np.asarray(nonoverlap_means)
    # Rank of infection window among the 15 + itself (higher = more extreme
    # in the high-load direction). Rank 1 = most extreme high-load.
    n_ge = int(np.sum(nonoverlap_means >= infection_window_mean))
    sanity_rank = n_ge + 1  # 1-based rank among {15 windows} U {infection}
    sanity_n = 15

    # --- 6. 204 sliding windows: descriptive backdrop ONLY ---
    sliding_means = []
    for s in range(len(pre_factor_z) - WINDOW_DAYS + 1):
        sliding_means.append(float(np.nanmean(pre_factor_z[s : s + WINDOW_DAYS])))
    sliding_means = np.asarray(sliding_means)
    assert len(sliding_means) == 204, f"expected 204 sliding windows, got {len(sliding_means)}"

    # --- 7. Effect size d2: standardised-difference CI from SAME E[L]=7 bootstrap ---
    # Standardised difference = (infection-window mean - pooled pre-LC mean)
    # of the factor-z, in pre-LC-SD units. Since the factor is z-scored on
    # the pre-LC baseline (robust), pooled pre-LC factor-z mean ~ 0 and the
    # pre-LC robust SD ~ 1 by construction; d2 is bootstrapped on the pre-LC
    # daily factor-z series under E[L]=7. The statistic evaluated per resample
    # is the leading-14-day window-mean minus the whole-resample mean, over
    # the resample SD, so one null model serves both the p-analogue and d2.
    pre_pooled_mean = float(np.nanmean(pre_factor_z))
    pre_pooled_sd = float(np.nanstd(pre_factor_z, ddof=1))
    d2_point = (infection_window_mean - pre_pooled_mean) / pre_pooled_sd

    def _std_diff_stat(resampled):
        r = np.asarray(resampled, dtype=float)
        win_mean = float(r[:WINDOW_DAYS].mean())
        pooled_mean = float(r.mean())
        pooled_sd = float(r.std(ddof=1))
        if pooled_sd == 0.0:
            return 0.0
        return (win_mean - pooled_mean) / pooled_sd

    d2_ci = stationary_bootstrap_ci(
        pre_factor_z[~np.isnan(pre_factor_z)],
        _std_diff_stat,
        n_bootstrap=N_REPLICATES,
        expected_block_length=EXPECTED_BLOCK_LENGTH,
        confidence_level=0.95,
        random_state=RNG_SEED,
    )
    # Center the bootstrap CI on the observed d2 (the bootstrap draws under
    # the null give the sampling spread; shift so the CI brackets the point
    # estimate). ci half-widths from the null-centered distribution:
    boot = d2_ci["bootstrap_distribution"]
    d2_ci_lower = d2_point - (float(np.quantile(boot, 0.975)) - float(np.median(boot)))
    d2_ci_upper = d2_point - (float(np.quantile(boot, 0.025)) - float(np.median(boot)))

    # --- 8. Triad coherence (g2): per-channel window-mean z, own predicted sign ---
    channel_window_z = {}
    channel_coherent = {}
    for col in (ANCHOR_COL, BB_COL, RHR_COL):
        med_c, spread_c = robust_baseline_params(pre[col].values)
        inf_z_c = robust_z(inf[col].values, med_c, spread_c)
        wmean = float(np.nanmean(inf_z_c))
        channel_window_z[col] = wmean
        # Coherence: did the channel move in ITS OWN predicted sign?
        channel_coherent[col] = bool(np.sign(wmean) == PREDICTED_SIGN[col])
    coherence_flag = all(channel_coherent.values())

    # --- 9. Detrend sec 3.7 sensitivity on the RAW g2 triad channels ---
    pre_ord = pre["date"].map(pd.Timestamp.toordinal).values.astype(float)
    inf_ord = inf["date"].map(pd.Timestamp.toordinal).values.astype(float)
    detrend_window_z = {}
    for col in (ANCHOR_COL, BB_COL, RHR_COL):
        dz, slope = detrend_window_mean_z(
            pre_ord, pre[col].values, inf_ord, inf[col].values
        )
        detrend_window_z[col] = {"detrended_window_mean_z": dz, "pre_slope_per_day": slope}
    # Verdict stability: does the anchor's sign (and coherence) survive detrend?
    detrend_anchor_z = detrend_window_z[ANCHOR_COL]["detrended_window_mean_z"]
    detrend_coherent = all(
        np.sign(detrend_window_z[c]["detrended_window_mean_z"]) == PREDICTED_SIGN[c]
        for c in (ANCHOR_COL, BB_COL, RHR_COL)
    )

    # --- 10. Acute-core overlay (descriptive only, NO p-analogue) ---
    core = df[(df["date"] >= ACUTE_CORE_START) & (df["date"] <= ACUTE_CORE_END)].copy()
    core_z = robust_z(core[ANCHOR_COL].values, med_anchor, spread_anchor)
    acute_core_mean = float(np.nanmean(core_z))
    acute_core_max = float(np.nanmax(core_z))

    # --- Verdict (locked tiers, pre-reg sec 6) ---
    if infection_window_mean > pct_95:
        tier = "MOVED"
    elif infection_window_mean < pct_05:
        tier = "MOVED-UNEXPECTED-DIRECTION"
    else:
        tier = "AMBIGUOUS"

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------
    line = "-" * 68
    print(line)
    print("R23 peri-event COVID known-event check: TEST EXECUTION")
    print(line)
    print(f"RNG seed (recorded): {RNG_SEED}")
    print(f"Replicates: {N_REPLICATES}   E[L]: {EXPECTED_BLOCK_LENGTH}   window: {WINDOW_DAYS} days")
    print(f"Pre-LC baseline band: {PRE_LC_START} to {PRE_LC_END}  (n={len(pre)})")
    print(f"Infection window: {INFECTION_START} to {INFECTION_END}  (n={len(inf)})")
    print(line)
    print("PRIMARY (anchor factor-z, stress_mean_sleep):")
    print(f"  personal pre-LC baseline: median={med_anchor:.4f}  k*MAD={spread_anchor:.4f}")
    print(f"  infection window-mean factor-z: {infection_window_mean:+.4f}")
    print(f"  infection window-max factor-z:  {infection_window_max:+.4f}")
    print(f"  null 95th pct: {pct_95:+.4f}   null 5th pct: {pct_05:+.4f}")
    print(f"  percentile within null: {percentile:.2f}   p-analogue (high-load, 1-sided): {p_analogue_high_load:.4f}")
    print(f"  >>> TIER VERDICT: {tier}")
    print(line)
    print("EFFECT SIZE d2 (standardised difference, same E[L]=7 machinery):")
    print(f"  d2 point: {d2_point:+.4f}   95% CI: [{d2_ci_lower:+.4f}, {d2_ci_upper:+.4f}]")
    print(line)
    print(f"n=15 non-overlapping sanity rank: rank {sanity_rank} of {sanity_n + 1} "
          f"(1 = most extreme high-load; among 15 windows + infection)")
    print(f"  15 non-overlapping window-means: min={nonoverlap_means.min():+.3f} "
          f"median={np.median(nonoverlap_means):+.3f} max={nonoverlap_means.max():+.3f}")
    print(line)
    print("204 sliding windows (DESCRIPTIVE BACKDROP ONLY, not a p-denominator):")
    print(f"  min={sliding_means.min():+.3f} median={np.median(sliding_means):+.3f} "
          f"max={sliding_means.max():+.3f} sd={sliding_means.std(ddof=1):.3f}")
    print(line)
    print(f"Data-driven E[L]*: {el_star:.3f}  (default 7)  flagged>2x: {el_flagged}  "
          f"cutoff_lag={el_result.get('cutoff_lag')}")
    print(line)
    print("TRIAD COHERENCE (g2) - per-channel window-mean z vs own predicted sign:")
    for col in (ANCHOR_COL, RHR_COL, BB_COL):
        pred = "UP(+)" if PREDICTED_SIGN[col] > 0 else "DOWN(-)"
        print(f"  {col:18s} window-mean z={channel_window_z[col]:+.4f}  "
              f"predicted={pred}  coherent={channel_coherent[col]}")
    print(f"  COHERENCE FLAG (all three in own predicted sign): {coherence_flag}")
    print("  NOTE: stress_mean_sleep (HA07c) and bb_highest (HA10) are rho=-0.92")
    print("  near-identical; coherence is one-signal-viewed-twice, NOT independent.")
    print(line)
    print("DETREND sec 3.7 SENSITIVITY (on RAW g2 triad channels):")
    for col in (ANCHOR_COL, RHR_COL, BB_COL):
        d = detrend_window_z[col]
        print(f"  {col:18s} detrended window-mean z={d['detrended_window_mean_z']:+.4f}  "
              f"pre-slope/day={d['pre_slope_per_day']:+.5f}")
    print(f"  detrend anchor window-mean z: {detrend_anchor_z:+.4f}")
    print(f"  detrend coherence preserved: {detrend_coherent}")
    print(line)
    print("ACUTE-CORE OVERLAY 2022-03-23..2022-03-30 (DESCRIPTIVE ONLY, NO p-analogue):")
    print(f"  acute-core mean factor-z: {acute_core_mean:+.4f}   max: {acute_core_max:+.4f}")
    print(line)

    return {
        "tier": tier,
        "infection_window_mean": infection_window_mean,
        "infection_window_max": infection_window_max,
        "percentile": percentile,
        "p_analogue_high_load": p_analogue_high_load,
        "null_pct_95": pct_95,
        "null_pct_05": pct_05,
        "d2_point": d2_point,
        "d2_ci_lower": d2_ci_lower,
        "d2_ci_upper": d2_ci_upper,
        "sanity_rank": sanity_rank,
        "sanity_n": sanity_n,
        "el_star": el_star,
        "el_flagged": el_flagged,
        "channel_window_z": channel_window_z,
        "channel_coherent": channel_coherent,
        "coherence_flag": coherence_flag,
        "detrend_window_z": detrend_window_z,
        "detrend_coherent": detrend_coherent,
        "acute_core_mean": acute_core_mean,
        "acute_core_max": acute_core_max,
    }


if __name__ == "__main__":
    main()
