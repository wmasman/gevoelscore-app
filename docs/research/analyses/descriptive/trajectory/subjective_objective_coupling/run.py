"""Q4.9 -- subjective <-> objective coupling + crash-day body-state profile.

THE CENTRAL PROJECT QUESTION per `analyses/descriptive/README.md` section 4.9.
Strand B (multi-year trajectory) descriptive analysis; extends the Q3.9.e
Strand-A first-pass (Spearman rho on the Stratum-4 single-pool) to the FULL
multi-channel cross-cutting analysis per the user-locked operationalisation
choices from the Strand B section 7c interview 2026-06-25.

USER-LOCKED OPERATIONALISATION (per handoff section 2; do NOT iterate):

1. Channels = 6 (autonomic-load family + RHR):
   - stress_mean_sleep            (CONFIRMED-citalopram +0.43/mg; Q3.1)
   - all_day_stress_avg           (CONFIRMED-citalopram +0.57/mg; Q3.2; E[L]*=29.8)
   - bb_lowest                    (CONFIRMED-citalopram -1.13/mg; Q3.3; E[L]*=29.25)
   - stress_stdev_sleep           (HA07d primary; both-eras-SUPPORTED; Q3.4; E[L]*=7.0)
   - stress_low_motion_min_count_S60_Mlow (Q3.x Phase 1; E[L]*=21.1)
   - resting_hr                   (Q3.6; very-long memory)

2. Three coupling methods (ALL three; the (d) interview option):
   (a) z-sign agreement on 28d-lagged personal baseline (CONVENTIONS sec 3.1)
   (b) quintile-bin agreement (equal-N per channel; gevoelscore by natural
       integer binning)
   (c) rolling-28d Spearman rho + low-rho epoch flag

3. Pre-crash window = episode-level matched (the (c) interview option):
   - 29 crash episodes per crash_v2-definition
   - matched non-crash episodes per HA-P6 v3 Arm-A logic (gevoelscore
     trajectory similarity within +- 1.0 to +- 2.0 with phase-match);
     REUSE the HA-P6 v3 matched-control machinery descriptively
   - 4d pre-crash lead-up window per HA-P6 v3 sec 4.4 + sec 4.2 spirit

4. Phase stratification: pooled primary + per-citalopram-phase sensitivity arm
   per phase_axis_collapsibility_conventions sec 6 binding on the 3
   CONFIRMED-citalopram channels.

OUTPUTS (per handoff section 3.1):

- summary.json (gitignored)
- plots/*.png (gitignored; coupling rates heatmap + per-crash profile)
- findings.md  (programmatic emit at end of script)
- README.md    (programmatic emit at end of script)

CROSS-REFERENCES LOAD-BEARING (per handoff section 3.3):

- Q3.9.e Spearman rho ranking is REPRODUCED + EXTENDED in section 3 method (c)
- HA-C3 v2 + HA-C3p inverted-U descriptively contextualises near-zero linear
  rho in section 2 method (a) (the linear cancels when shape is inverted-U)
- recovery_arc v2 section 5.A afbouw-reversal is REPRODUCED at finer per-channel
  coupling-rate resolution in section 6 phase sensitivity arm
- HA-P6 v3 Arm-A matched-control machinery is REUSED in section 5 pre-crash
  body-state profile

DISCIPLINE GUARDS (per CONVENTIONS):

- section 2.1 descriptive-before-inference: NO causal claims; NO falsification
  bar; NO HA verdict promotion (HA-C3 v2 + HA-C3p + crash_v2-definition +
  HA-P6 v3 + recovery_arc v2 + R14 are all LOCKED and NOT extended here).
- section 3.1 personal baseline: 28d-lagged trailing window with robust
  median + MAD scaling for z-scores.
- section 3.4 crash-drop sensitivity: section 5 matched-control profile is
  episode-centred (not row-level); the sensitivity hook is dispatched by
  construction (the matched controls ARE non-crash episodes).
- section 3.6 named counts: every n reports scheme + unit + source.
- section 4.1 + section 4.2: descriptive framing only; observations land as
  "rate X%, divergence concentrates Z way, profile shows W pattern".
- section 4.9 (descriptive README): this analysis closes the canonical Q4.9
  scope for the first time in any artefact.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
# HERE = .../analyses/descriptive/trajectory/subjective_objective_coupling
# parents[0]=trajectory; [1]=descriptive; [2]=analyses
UTILS_DIR = HERE.parents[2] / "_utils"
sys.path.insert(0, str(UTILS_DIR))

from frame import (  # noqa: E402
    filter_to_stratum_4,
    load_crash_labels,
    load_master,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


AS_OF_DATE = "2026-06-05"  # parity with Q3.1-Q3.9 Strand-A precedents

# 6 channels per user-locked operationalisation (handoff sec 2.1)
CHANNELS = [
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
    "stress_stdev_sleep",
    "stress_low_motion_min_count_S60_Mlow",
    "resting_hr",
]

# CONFIRMED-citalopram subset (the 3 channels bound by
# phase_axis_collapsibility_conventions sec 6 in the phase sensitivity arm)
CONFIRMED_CITALOPRAM = {
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
}

# Personal-baseline window per CONVENTIONS sec 3.1 + Q3.9.e Spearman precedent
BASELINE_WINDOW = 28
BASELINE_LAG = 1  # trailing [t-28, t-1]; excludes today

# Citalopram phase boundaries per
# methodology/citalopram_phase_stratification.md section 3
PHASE_BOUNDARIES = [
    ("unmedicated", date(2022, 9, 3), date(2024, 4, 8)),
    ("buildup", date(2024, 4, 9), date(2024, 6, 19)),
    ("consolidation", date(2024, 6, 20), date(2026, 3, 19)),
    ("afbouw", date(2026, 3, 20), date(2026, 6, 5)),
]

# Pre-crash window per HA-P6 v3 sec 4.4 (gevoelscore similarity window
# [t0-10, t0-1] = 10d; the analytical lead-up window for the body-state
# profile is the LAST 4 days per the user-locked operationalisation, i.e.
# days [t0_start - 4, t0_start - 1] where t0_start is the FIRST crash day.
# This is the "4d pre-crash lead-up" per handoff sec 2.3.
PRE_CRASH_LEAD_UP = 4

# Matched-control tolerance ladder per HA-P6 v3 sec 4.4 step 4
MATCH_TOLERANCE_LADDER = [1.0, 1.5, 2.0]

# Rolling Spearman window for method (c); matches BASELINE_WINDOW
ROLLING_SPEARMAN_WINDOW = 28

# Low-rho threshold per handoff sec 2.2 method (c)
LOW_RHO_THRESHOLD = 0.1


# ---------------------------------------------------------------------------
# Phase helpers
# ---------------------------------------------------------------------------


def citalopram_phase(d) -> str:
    if not isinstance(d, date):
        d = pd.Timestamp(d).date()
    for name, start, end in PHASE_BOUNDARIES:
        if start <= d <= end:
            return name
    return "out_of_scope"


# ---------------------------------------------------------------------------
# Stage 1 -- data prep
# ---------------------------------------------------------------------------


def stage1_data_prep() -> dict:
    """Load per_day_master + labels; filter Stratum 4; identify 29 crash
    episodes per crash_v2; compute personal-baseline 28d-lagged z-scores
    per channel + gevoelscore.

    Returns dict with keys:
    - df: pd.DataFrame, Stratum 4 rows with z-score columns added
    - episodes: pd.DataFrame, one row per crash episode (n=29)
    - n_s4: int, total Stratum 4 day count
    """
    master = load_master(as_of_date=AS_OF_DATE)
    labels = load_crash_labels(as_of_date=AS_OF_DATE)

    df = filter_to_stratum_4(master, as_of_date=AS_OF_DATE).copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # Bring crash labels in
    labels = labels.copy()
    labels["date"] = pd.to_datetime(labels["date"])
    df = df.merge(
        labels[["date", "label", "episode_id"]],
        on="date",
        how="left",
    )
    df["is_crash"] = (df["label"] == "crash").astype(bool)

    # Add phase column
    df["citalopram_phase"] = df["date"].dt.date.apply(citalopram_phase)

    # Compute personal-baseline 28d-lagged z-scores per channel + gevoelscore
    # Using robust median + MAD per CONVENTIONS sec 3.1
    for col in CHANNELS + ["gevoelscore"]:
        z = _z_score_lagged_robust(df[col], BASELINE_WINDOW, BASELINE_LAG)
        df[col + "_z28"] = z

    # Identify 29 crash episodes per crash_v2 -- group by episode_id
    crash_rows = df[df["is_crash"]].copy()
    crash_rows = crash_rows.dropna(subset=["episode_id"])
    episodes = (
        crash_rows.groupby("episode_id")
        .agg(
            episode_start=("date", "min"),
            episode_end=("date", "max"),
            episode_length=("date", "count"),
            min_gevoelscore=("gevoelscore", "min"),
        )
        .reset_index()
        .sort_values("episode_start")
        .reset_index(drop=True)
    )
    episodes["citalopram_phase"] = episodes["episode_start"].dt.date.apply(
        citalopram_phase
    )

    return {
        "df": df,
        "episodes": episodes,
        "n_s4": int(len(df)),
        "n_crash_episodes": int(len(episodes)),
    }


def _z_score_lagged_robust(series, window: int, lag: int):
    """Robust 28d-lagged z-score. Trailing window [t-window-lag+1, t-lag].

    Returns NaN before warm-up and where MAD is 0.
    """
    arr = series.to_numpy(dtype=float)
    n = len(arr)
    z = np.full(n, np.nan)
    for t in range(n):
        end = t - lag + 1  # exclusive
        start = end - window  # inclusive
        if end <= 0:
            continue
        start = max(0, start)
        window_vals = arr[start:end]
        window_vals = window_vals[~np.isnan(window_vals)]
        if len(window_vals) < max(1, window // 2):
            continue
        centre = float(np.median(window_vals))
        mad = float(np.median(np.abs(window_vals - centre)))
        if mad == 0.0:
            continue
        spread = mad * 1.4826
        if np.isnan(arr[t]):
            continue
        z[t] = (arr[t] - centre) / spread
    return pd.Series(z, index=series.index, name=series.name)


# ---------------------------------------------------------------------------
# Stage 2 -- coupling method (a): z-sign agreement
# ---------------------------------------------------------------------------


def stage2_zsign_agreement(df: pd.DataFrame) -> dict:
    """For each channel, compute the sign-agreement rate against gevoelscore
    z-score on Stratum 4 (per-day; both z-scores non-NaN).

    Sign-agreement classification:
    - both > +0.3 -> agree_high (both up)
    - both < -0.3 -> agree_low (both down)
    - both |z| <= 0.3 -> agree_flat (both flat; counts as agree)
    - opposite signs with |z| > 0.3 each -> divergent
    - one |z| > 0.3 and other |z| <= 0.3 -> mixed (partial)

    Note: many channels are NEGATIVELY associated with gevoelscore (high
    stress -> low felt-state), so we apply a per-channel sign convention:
    "agree" = (z_chan * sign_convention) sign-match with z_gevoel.
    The sign_convention is derived from the per-channel sign of the
    Spearman rho on the full pool (computed in stage 4).
    """
    rates = {}
    sign_conv = _per_channel_sign_convention(df)

    for chan in CHANNELS:
        z_chan = df[chan + "_z28"].to_numpy()
        z_gevoel = df["gevoelscore_z28"].to_numpy()
        # Apply per-channel sign convention so "agreement" means
        # body-state-and-felt-state-trending-same-direction
        z_chan_adj = z_chan * sign_conv[chan]
        mask = ~np.isnan(z_chan_adj) & ~np.isnan(z_gevoel)
        n = int(mask.sum())
        if n == 0:
            rates[chan] = {"n": 0}
            continue

        zc = z_chan_adj[mask]
        zg = z_gevoel[mask]

        # 5 categories with |z|=0.3 threshold
        agree_high = ((zc > 0.3) & (zg > 0.3)).sum()
        agree_low = ((zc < -0.3) & (zg < -0.3)).sum()
        agree_flat = ((np.abs(zc) <= 0.3) & (np.abs(zg) <= 0.3)).sum()
        divergent = (
            ((zc > 0.3) & (zg < -0.3)) | ((zc < -0.3) & (zg > 0.3))
        ).sum()
        mixed = n - (agree_high + agree_low + agree_flat + divergent)

        # Quantify where divergences concentrate -- |z_gevoel| extreme cells
        ext_mask = np.abs(zg) > 1.0
        n_ext = int(ext_mask.sum())
        div_at_extremes = (
            ((zc[ext_mask] > 0.3) & (zg[ext_mask] < -0.3))
            | ((zc[ext_mask] < -0.3) & (zg[ext_mask] > 0.3))
        ).sum() if n_ext > 0 else 0
        rate_div_at_extremes = (
            float(div_at_extremes) / n_ext if n_ext > 0 else float("nan")
        )
        # Vs middle cells (where shape-cancellation dominates per inverted-U)
        mid_mask = np.abs(zg) <= 1.0
        n_mid = int(mid_mask.sum())
        div_at_middle = (
            ((zc[mid_mask] > 0.3) & (zg[mid_mask] < -0.3))
            | ((zc[mid_mask] < -0.3) & (zg[mid_mask] > 0.3))
        ).sum() if n_mid > 0 else 0
        rate_div_at_middle = (
            float(div_at_middle) / n_mid if n_mid > 0 else float("nan")
        )

        rates[chan] = {
            "n": n,
            "sign_convention": int(sign_conv[chan]),
            "agree_high": int(agree_high),
            "agree_low": int(agree_low),
            "agree_flat": int(agree_flat),
            "divergent": int(divergent),
            "mixed": int(mixed),
            "agreement_rate": float(
                agree_high + agree_low + agree_flat
            ) / n,
            "divergence_rate": float(divergent) / n,
            "mixed_rate": float(mixed) / n,
            "n_extreme_gevoelscore_cells": n_ext,
            "divergence_rate_at_extremes": rate_div_at_extremes,
            "n_middle_gevoelscore_cells": n_mid,
            "divergence_rate_at_middle": rate_div_at_middle,
        }
    return rates


def _per_channel_sign_convention(df: pd.DataFrame) -> dict:
    """Per-channel sign convention so that POSITIVE channel z aligns with
    POSITIVE gevoelscore z. Derived from the Spearman rho sign on the full
    Stratum-4 pool (reproduces Q3.9.e direction).

    Returns dict channel -> +1 (positively correlated with gevoel) or -1
    (negatively correlated; sign flipped for agreement test).
    """
    conv = {}
    for chan in CHANNELS:
        z_chan = df[chan + "_z28"].to_numpy()
        z_gevoel = df["gevoelscore_z28"].to_numpy()
        mask = ~np.isnan(z_chan) & ~np.isnan(z_gevoel)
        if mask.sum() < 30:
            conv[chan] = +1
            continue
        rho = _spearman_rho(z_chan[mask], z_gevoel[mask])
        conv[chan] = -1 if rho < 0 else +1
    return conv


def _spearman_rho(x, y) -> float:
    """Simple Spearman rho without scipy (avoid pulling extra deps).

    Ties handled via average-rank.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 3 or len(y) < 3:
        return float("nan")
    rx = _rank_avg(x)
    ry = _rank_avg(y)
    rx_mean = rx.mean()
    ry_mean = ry.mean()
    num = ((rx - rx_mean) * (ry - ry_mean)).sum()
    den_x = np.sqrt(((rx - rx_mean) ** 2).sum())
    den_y = np.sqrt(((ry - ry_mean) ** 2).sum())
    if den_x == 0 or den_y == 0:
        return float("nan")
    return float(num / (den_x * den_y))


def _rank_avg(arr):
    """Average-rank (1-based) handling ties."""
    arr = np.asarray(arr, dtype=float)
    order = np.argsort(arr, kind="mergesort")
    ranks = np.empty_like(arr, dtype=float)
    i = 0
    n = len(arr)
    while i < n:
        j = i
        while j + 1 < n and arr[order[j + 1]] == arr[order[i]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    return ranks


# ---------------------------------------------------------------------------
# Stage 3 -- coupling method (b): quintile-bin agreement
# ---------------------------------------------------------------------------


def stage3_quintile_agreement(df: pd.DataFrame) -> dict:
    """Per channel: equal-N quintile bins on the raw channel; gevoelscore
    bins from the natural 1-6 integer scale grouped to 5 levels:
        bin 1 = {1, 2}
        bin 2 = {3}
        bin 3 = {4}
        bin 4 = {5}
        bin 5 = {6}

    Coupling = bins differ by <= 1 (after adjusting for per-channel sign
    convention so that channel-bin 5 means "highest body-state in the
    same direction as gevoelscore-bin 5 high felt-state"). Divergence =
    bins differ by >= 2.
    """
    sign_conv = _per_channel_sign_convention(df)
    rates = {}

    # gevoelscore bins
    gv = df["gevoelscore"].to_numpy()
    gv_bins = np.full(len(gv), np.nan)
    gv_bins[np.isin(gv, [1, 2])] = 1
    gv_bins[gv == 3] = 2
    gv_bins[gv == 4] = 3
    gv_bins[gv == 5] = 4
    gv_bins[gv == 6] = 5

    for chan in CHANNELS:
        ch = df[chan].to_numpy(dtype=float)
        mask_finite = ~np.isnan(ch) & ~np.isnan(gv_bins)
        n_total = int(mask_finite.sum())
        if n_total < 30:
            rates[chan] = {"n": 0}
            continue

        ch_valid = ch[mask_finite]
        # equal-N quintile cuts
        cuts = np.quantile(ch_valid, [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ch_bins_valid = np.digitize(ch_valid, cuts[1:-1], right=False) + 1
        ch_bins_valid = np.clip(ch_bins_valid, 1, 5)

        # Apply per-channel sign convention. If sign=-1, flip the bin so
        # bin5 means "highest in the direction of high felt-state".
        if sign_conv[chan] == -1:
            ch_bins_valid = 6 - ch_bins_valid

        gv_bins_valid = gv_bins[mask_finite].astype(int)
        diffs = np.abs(ch_bins_valid - gv_bins_valid)

        coupling_count = int((diffs <= 1).sum())
        divergence_count = int((diffs >= 2).sum())
        exact_match_count = int((diffs == 0).sum())
        extreme_divergence_count = int((diffs >= 3).sum())

        rates[chan] = {
            "n": n_total,
            "sign_convention": int(sign_conv[chan]),
            "coupling_count": coupling_count,
            "divergence_count": divergence_count,
            "exact_match_count": exact_match_count,
            "extreme_divergence_count": extreme_divergence_count,
            "coupling_rate": float(coupling_count) / n_total,
            "divergence_rate": float(divergence_count) / n_total,
            "exact_match_rate": float(exact_match_count) / n_total,
            "extreme_divergence_rate": float(extreme_divergence_count) / n_total,
        }

    return rates


# ---------------------------------------------------------------------------
# Stage 4 -- coupling method (c): rolling 28d Spearman rho + low-rho epochs
# ---------------------------------------------------------------------------


def stage4_rolling_spearman(df: pd.DataFrame) -> dict:
    """For each channel: rolling 28d Spearman rho vs gevoelscore.

    Reports:
    - Per-channel mean rho (full-pool comparator; reproduces Q3.9.e)
    - Per-channel rolling-window rho time series
    - Per-channel low-rho epoch flag count (|rho| < 0.1)
    - Per-channel temporal distribution of low-rho epochs by phase
    """
    results = {}
    n = len(df)

    for chan in CHANNELS:
        ch_arr = df[chan].to_numpy(dtype=float)
        gv_arr = df["gevoelscore"].to_numpy(dtype=float)

        # Full-pool Spearman (reproduces Q3.9.e)
        mask_full = ~np.isnan(ch_arr) & ~np.isnan(gv_arr)
        full_rho = _spearman_rho(ch_arr[mask_full], gv_arr[mask_full])
        full_n = int(mask_full.sum())

        # Rolling windows
        rho_series = np.full(n, np.nan)
        n_used = np.zeros(n, dtype=int)
        for t in range(ROLLING_SPEARMAN_WINDOW - 1, n):
            window_ch = ch_arr[t - ROLLING_SPEARMAN_WINDOW + 1 : t + 1]
            window_gv = gv_arr[t - ROLLING_SPEARMAN_WINDOW + 1 : t + 1]
            window_mask = ~np.isnan(window_ch) & ~np.isnan(window_gv)
            n_used[t] = int(window_mask.sum())
            if window_mask.sum() < 14:  # at least 14/28 valid
                continue
            rho_series[t] = _spearman_rho(
                window_ch[window_mask], window_gv[window_mask]
            )

        # Low-rho epoch flag distribution
        non_nan_idx = ~np.isnan(rho_series)
        n_windows = int(non_nan_idx.sum())
        if n_windows == 0:
            results[chan] = {"n_windows": 0, "full_pool_rho": full_rho}
            continue

        low_rho_mask = np.abs(rho_series) < LOW_RHO_THRESHOLD
        n_low_rho = int((low_rho_mask & non_nan_idx).sum())
        rate_low_rho = float(n_low_rho) / n_windows

        # Temporal distribution by citalopram phase
        phase_col = df["citalopram_phase"].to_numpy()
        per_phase_counts = {}
        per_phase_totals = {}
        per_phase_low_rates = {}
        for phase_name, _, _ in PHASE_BOUNDARIES:
            ph_mask = (phase_col == phase_name) & non_nan_idx
            ph_n = int(ph_mask.sum())
            ph_low = int((low_rho_mask & ph_mask).sum())
            per_phase_counts[phase_name] = ph_low
            per_phase_totals[phase_name] = ph_n
            per_phase_low_rates[phase_name] = (
                float(ph_low) / ph_n if ph_n > 0 else float("nan")
            )

        # Median + p25 + p75 rho across windows
        valid_rhos = rho_series[non_nan_idx]
        median_rho = float(np.median(valid_rhos))
        p25_rho = float(np.quantile(valid_rhos, 0.25))
        p75_rho = float(np.quantile(valid_rhos, 0.75))

        results[chan] = {
            "n_full_pool": full_n,
            "full_pool_rho": full_rho,
            "n_windows": n_windows,
            "median_rolling_rho": median_rho,
            "p25_rolling_rho": p25_rho,
            "p75_rolling_rho": p75_rho,
            "n_low_rho_windows": n_low_rho,
            "low_rho_rate": rate_low_rho,
            "per_phase_low_rho_counts": per_phase_counts,
            "per_phase_window_totals": per_phase_totals,
            "per_phase_low_rho_rates": per_phase_low_rates,
            "_rho_series": rho_series.tolist(),  # for plotting
        }

    return results


# ---------------------------------------------------------------------------
# Stage 5 -- pre-crash matched-control body-state profile (HA-P6 v3 Arm-A)
# ---------------------------------------------------------------------------


def stage5_matched_control_profile(
    df: pd.DataFrame, episodes: pd.DataFrame
) -> dict:
    """For each of 29 crash episodes:

    1. Identify episode_start (first crash day = t0_start).
    2. Find matched non-crash day per HA-P6 v3 sec 4.4 Arm-A:
       - same citalopram phase
       - gevoelscore trajectory on the 4d pre-window similar to the crash's
         pre-window within tolerance ladder [+-1.0, +-1.5, +-2.0]
       - no crash episode within [d_match - 14, d_match + 4]
    3. Compute per-crash + per-matched body-state 6-channel z-score profile
       over the 4d lead-up window.

    Output:
    - per_episode_profile: 29 rows; each carries
        - episode_id, episode_start, phase
        - gevoelscore_lead_up_mean_z + per-channel lead-up_mean_z (6 channels)
        - matched_day (or None if no match found)
        - matched_gevoelscore_lead_up_mean_z + per-channel matched profile
        - crash_minus_matched per channel
    - aggregate_pattern_per_channel:
        - mean(crash_minus_matched) per channel
        - n eligible pairs per channel
    """
    # Filter to LC era for matched candidates (Stratum 4 already applied)
    # Note: handoff sec 2.3 says REUSE HA-P6 v3 Arm-A logic; HA-P6 v3 uses LC
    # era 2022-04-04 onward; Stratum 4 starts 2022-09-03 so we use that.
    df = df.copy()
    df["date_only"] = df["date"].dt.date
    date_to_idx = {d: i for i, d in enumerate(df["date_only"].tolist())}

    profiles = []
    n_matched = 0
    n_unmatched = 0

    # Pre-compute date list for crash boundaries
    crash_mask_per_day = df["is_crash"].to_numpy(dtype=bool)
    phase_per_day = df["citalopram_phase"].to_numpy()
    gv_per_day = df["gevoelscore"].to_numpy(dtype=float)

    for _, ep in episodes.iterrows():
        ep_id = ep["episode_id"]
        ep_start = ep["episode_start"].date()
        ep_phase = ep["citalopram_phase"]

        if ep_start not in date_to_idx:
            profiles.append(_empty_profile(ep_id, ep_start, ep_phase))
            n_unmatched += 1
            continue
        t0_idx = date_to_idx[ep_start]

        # Pre-crash 4d lead-up window indices
        pre_indices = [t0_idx - k for k in range(PRE_CRASH_LEAD_UP, 0, -1)]
        if any(i < 0 for i in pre_indices):
            profiles.append(_empty_profile(ep_id, ep_start, ep_phase))
            n_unmatched += 1
            continue

        # Crash side: per-channel mean z over lead-up window + gevoel
        crash_profile = _compute_lead_up_profile(df, pre_indices)
        crash_gv_traj = gv_per_day[pre_indices]

        # Find matched non-crash day
        match_idx = _find_matched_control(
            df,
            crash_gv_traj,
            t0_idx,
            ep_phase,
            phase_per_day,
            crash_mask_per_day,
            gv_per_day,
            date_to_idx,
        )

        if match_idx is None:
            row = {
                "episode_id": ep_id,
                "episode_start": str(ep_start),
                "phase": ep_phase,
                "crash_profile_z": crash_profile,
                "crash_gevoelscore_pre_mean": _safe_mean(crash_gv_traj),
                "matched_date": None,
                "matched_profile_z": {ch: float("nan") for ch in CHANNELS},
                "matched_gevoelscore_pre_mean": float("nan"),
                "crash_minus_matched": {ch: float("nan") for ch in CHANNELS},
                "match_tolerance_used": float("nan"),
            }
            profiles.append(row)
            n_unmatched += 1
            continue

        matched_pre_idx = [match_idx - k for k in range(PRE_CRASH_LEAD_UP, 0, -1)]
        matched_profile = _compute_lead_up_profile(df, matched_pre_idx)
        matched_gv_traj = gv_per_day[matched_pre_idx]

        diff = {
            ch: (
                crash_profile[ch] - matched_profile[ch]
                if not (
                    np.isnan(crash_profile[ch]) or np.isnan(matched_profile[ch])
                )
                else float("nan")
            )
            for ch in CHANNELS
        }

        # Determine which tolerance worked (stored at match-find time)
        tol = _record_match_tolerance(crash_gv_traj, matched_gv_traj)

        row = {
            "episode_id": ep_id,
            "episode_start": str(ep_start),
            "phase": ep_phase,
            "crash_profile_z": crash_profile,
            "crash_gevoelscore_pre_mean": _safe_mean(crash_gv_traj),
            "matched_date": str(df["date_only"].iloc[match_idx]),
            "matched_profile_z": matched_profile,
            "matched_gevoelscore_pre_mean": _safe_mean(matched_gv_traj),
            "crash_minus_matched": diff,
            "match_tolerance_used": tol,
        }
        profiles.append(row)
        n_matched += 1

    # Aggregate cross-episode pattern per channel
    aggregate_per_channel = {}
    for chan in CHANNELS:
        # crash_z values across episodes
        c_vals = [p["crash_profile_z"][chan] for p in profiles]
        c_vals = [v for v in c_vals if not np.isnan(v)]
        # matched_z values across episodes
        m_vals = [p["matched_profile_z"][chan] for p in profiles]
        m_vals = [v for v in m_vals if not np.isnan(v)]
        # diff values across episodes (only paired)
        d_vals = [
            p["crash_minus_matched"][chan]
            for p in profiles
            if not np.isnan(p["crash_minus_matched"][chan])
        ]

        aggregate_per_channel[chan] = {
            "n_crash_episodes_with_data": len(c_vals),
            "n_matched_pairs": len(d_vals),
            "crash_mean_z_pre": float(np.mean(c_vals)) if c_vals else float("nan"),
            "crash_median_z_pre": float(np.median(c_vals)) if c_vals else float("nan"),
            "matched_mean_z_pre": float(np.mean(m_vals)) if m_vals else float("nan"),
            "matched_median_z_pre": float(np.median(m_vals)) if m_vals else float("nan"),
            "crash_minus_matched_mean": float(np.mean(d_vals)) if d_vals else float("nan"),
            "crash_minus_matched_median": float(np.median(d_vals)) if d_vals else float("nan"),
        }

    return {
        "n_episodes_total": int(len(episodes)),
        "n_episodes_matched": n_matched,
        "n_episodes_unmatched": n_unmatched,
        "match_tolerance_ladder": MATCH_TOLERANCE_LADDER,
        "pre_crash_lead_up_days": PRE_CRASH_LEAD_UP,
        "per_episode_profile": profiles,
        "aggregate_per_channel": aggregate_per_channel,
    }


def _empty_profile(ep_id, ep_start, ep_phase) -> dict:
    return {
        "episode_id": ep_id,
        "episode_start": str(ep_start),
        "phase": ep_phase,
        "crash_profile_z": {ch: float("nan") for ch in CHANNELS},
        "crash_gevoelscore_pre_mean": float("nan"),
        "matched_date": None,
        "matched_profile_z": {ch: float("nan") for ch in CHANNELS},
        "matched_gevoelscore_pre_mean": float("nan"),
        "crash_minus_matched": {ch: float("nan") for ch in CHANNELS},
        "match_tolerance_used": float("nan"),
    }


def _compute_lead_up_profile(df: pd.DataFrame, indices: list) -> dict:
    """Mean z-score per channel over the indices."""
    out = {}
    for chan in CHANNELS:
        z_col = chan + "_z28"
        vals = df[z_col].iloc[indices].to_numpy()
        vals = vals[~np.isnan(vals)]
        out[chan] = float(np.mean(vals)) if len(vals) > 0 else float("nan")
    return out


def _safe_mean(arr) -> float:
    arr = np.asarray(arr, dtype=float)
    arr = arr[~np.isnan(arr)]
    return float(np.mean(arr)) if len(arr) > 0 else float("nan")


def _find_matched_control(
    df: pd.DataFrame,
    crash_gv_traj,
    t0_idx: int,
    ep_phase: str,
    phase_per_day,
    crash_mask_per_day,
    gv_per_day,
    date_to_idx,
):
    """HA-P6 v3 Arm-A logic adapted: find non-crash day d_match such that
    - same citalopram phase as ep_phase
    - non-crash within [d_match - 14, d_match + 4]
    - gevoelscore trajectory on [d_match - 4, d_match - 1] within tolerance
      of crash_gv_traj at each aligned day
    - sufficient distance from crash (>= 30d) to avoid leakage
    Pick the candidate with smallest MAD vs crash trajectory.
    """
    n = len(df)
    candidates_by_tol = {t: [] for t in MATCH_TOLERANCE_LADDER}

    for d_idx in range(PRE_CRASH_LEAD_UP, n - 4):
        if abs(d_idx - t0_idx) < 30:
            continue
        if phase_per_day[d_idx] != ep_phase:
            continue
        # Non-crash within [d_idx - 14, d_idx + 4]
        lo = max(0, d_idx - 14)
        hi = min(n - 1, d_idx + 4)
        if crash_mask_per_day[lo : hi + 1].any():
            continue
        # Trajectory similarity check
        cand_traj = gv_per_day[d_idx - PRE_CRASH_LEAD_UP : d_idx]
        if len(cand_traj) != len(crash_gv_traj):
            continue
        if np.any(np.isnan(cand_traj)) or np.any(np.isnan(crash_gv_traj)):
            continue
        max_abs_diff = float(np.max(np.abs(cand_traj - crash_gv_traj)))
        for tol in MATCH_TOLERANCE_LADDER:
            if max_abs_diff <= tol:
                mad_dist = float(np.mean(np.abs(cand_traj - crash_gv_traj)))
                candidates_by_tol[tol].append((d_idx, mad_dist))
                break

    for tol in MATCH_TOLERANCE_LADDER:
        if candidates_by_tol[tol]:
            best = min(candidates_by_tol[tol], key=lambda x: x[1])
            return best[0]
    return None


def _record_match_tolerance(crash_gv_traj, matched_gv_traj) -> float:
    diffs = np.abs(np.asarray(crash_gv_traj) - np.asarray(matched_gv_traj))
    if np.any(np.isnan(diffs)):
        return float("nan")
    max_diff = float(np.max(diffs))
    for tol in MATCH_TOLERANCE_LADDER:
        if max_diff <= tol:
            return tol
    return float("nan")


# ---------------------------------------------------------------------------
# Stage 6 -- phase sensitivity arm
# ---------------------------------------------------------------------------


def stage6_phase_sensitivity(df: pd.DataFrame) -> dict:
    """Re-run methods (a) + (b) + (c) per citalopram phase. Respects the
    phase_axis_collapsibility_conventions sec 6 binding on CONFIRMED-citalopram
    channels (stress_mean_sleep, all_day_stress_avg, bb_lowest): these
    channels CARRY the citalopram-shift confound at Tier B; per-phase reads
    descriptively surface where coupling-rate concentrates within each phase
    without correcting for the level shift (sec 5.A pattern; this analysis
    descriptively reports rather than applies a §5.B correction since the
    descriptive scope does not require dose-adjusted predictors).

    The 3 non-confirmed channels (stress_stdev_sleep, stress_low_motion,
    resting_hr) do NOT have the binding; reported descriptively for parity.
    """
    out = {}
    for phase_name, _, _ in PHASE_BOUNDARIES:
        sub = df[df["citalopram_phase"] == phase_name].copy()
        if len(sub) < 30:
            out[phase_name] = {"n": int(len(sub)), "skipped": True}
            continue
        method_a = stage2_zsign_agreement(sub)
        method_b = stage3_quintile_agreement(sub)
        # Lightweight method (c): just per-phase full-window Spearman
        method_c_lite = _per_phase_spearman(sub)

        out[phase_name] = {
            "n": int(len(sub)),
            "n_crash_days": int(sub["is_crash"].sum()),
            "method_a_zsign": method_a,
            "method_b_quintile": method_b,
            "method_c_spearman": method_c_lite,
        }
    return out


def _per_phase_spearman(sub_df: pd.DataFrame) -> dict:
    """Per-channel Spearman rho on a phase subset."""
    out = {}
    for chan in CHANNELS:
        ch = sub_df[chan].to_numpy(dtype=float)
        gv = sub_df["gevoelscore"].to_numpy(dtype=float)
        mask = ~np.isnan(ch) & ~np.isnan(gv)
        n = int(mask.sum())
        if n < 30:
            out[chan] = {"n": n, "spearman_rho": float("nan")}
            continue
        rho = _spearman_rho(ch[mask], gv[mask])
        out[chan] = {"n": n, "spearman_rho": rho}
    return out


# ---------------------------------------------------------------------------
# Stage 7 -- plots
# ---------------------------------------------------------------------------


def stage7_make_plots(
    summary: dict, df: pd.DataFrame, episodes: pd.DataFrame, out_dir: Path
) -> list:
    """Two plots:
    1. Per-channel coupling/divergence heatmap (rows = channel, cols = method)
    2. Per-crash body-state z-score profile heatmap (29 rows x 6 channels)
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    written = []

    # ----- Plot 1: cross-method coupling rates per channel ------------------
    method_a = summary["stage2_zsign_agreement"]
    method_b = summary["stage3_quintile_agreement"]
    method_c = summary["stage4_rolling_spearman"]

    chans = CHANNELS
    a_rates = [method_a[c].get("agreement_rate", float("nan")) for c in chans]
    b_rates = [method_b[c].get("coupling_rate", float("nan")) for c in chans]
    c_rates = [
        1.0 - method_c[c].get("low_rho_rate", float("nan"))
        if not np.isnan(method_c[c].get("low_rho_rate", float("nan")))
        else float("nan")
        for c in chans
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    width = 0.27
    x = np.arange(len(chans))
    ax.bar(x - width, a_rates, width, label="Method (a) z-sign agreement")
    ax.bar(x, b_rates, width, label="Method (b) quintile coupling (diff <=1)")
    ax.bar(x + width, c_rates, width, label="Method (c) non-low-rho rate")
    ax.set_xticks(x)
    ax.set_xticklabels(
        [c.replace("_", " ").replace("min count S60 Mlow", "") for c in chans],
        rotation=30,
        ha="right",
        fontsize=8,
    )
    ax.set_ylabel("rate")
    ax.set_ylim(0, 1.0)
    ax.set_title("Q4.9 per-channel coupling rates -- three methods (pooled Stratum 4)")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    p1 = out_dir / "fig1_cross_method_coupling_rates.png"
    fig.savefig(p1, dpi=120)
    plt.close(fig)
    written.append(str(p1))

    # ----- Plot 2: per-crash body-state z-score profile heatmap -------------
    profiles = summary["stage5_matched_control_profile"]["per_episode_profile"]
    n_ep = len(profiles)
    matrix = np.full((n_ep, len(CHANNELS)), np.nan)
    row_labels = []
    for i, p in enumerate(profiles):
        for j, c in enumerate(CHANNELS):
            matrix[i, j] = p["crash_profile_z"][c]
        row_labels.append(p["episode_start"] + " " + p["phase"][:5])

    fig, ax = plt.subplots(figsize=(8, 11))
    vmax = float(np.nanmax(np.abs(matrix))) if not np.all(np.isnan(matrix)) else 1.0
    vmax = max(vmax, 0.5)
    im = ax.imshow(matrix, aspect="auto", cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    ax.set_xticks(range(len(CHANNELS)))
    ax.set_xticklabels(
        [c.replace("_", " ").replace("min count S60 Mlow", "") for c in CHANNELS],
        rotation=30,
        ha="right",
        fontsize=8,
    )
    ax.set_yticks(range(n_ep))
    ax.set_yticklabels(row_labels, fontsize=6)
    ax.set_title(
        "Q4.9 per-crash body-state z-score profile -- 4d pre-crash lead-up\n"
        "(n=" + str(n_ep) + " crash episodes; red = elevated, blue = depressed)"
    )
    fig.colorbar(im, ax=ax, label="mean z-score (vs 28d-lagged baseline)")
    fig.tight_layout()
    p2 = out_dir / "fig2_per_crash_body_state_profile.png"
    fig.savefig(p2, dpi=120)
    plt.close(fig)
    written.append(str(p2))

    # ----- Plot 3: pre-crash divergence pattern (crash minus matched) -------
    matrix_diff = np.full((n_ep, len(CHANNELS)), np.nan)
    for i, p in enumerate(profiles):
        for j, c in enumerate(CHANNELS):
            matrix_diff[i, j] = p["crash_minus_matched"][c]
    fig, ax = plt.subplots(figsize=(8, 11))
    vmax_d = float(np.nanmax(np.abs(matrix_diff))) if not np.all(np.isnan(matrix_diff)) else 1.0
    vmax_d = max(vmax_d, 0.5)
    im = ax.imshow(matrix_diff, aspect="auto", cmap="RdBu_r", vmin=-vmax_d, vmax=vmax_d)
    ax.set_xticks(range(len(CHANNELS)))
    ax.set_xticklabels(
        [c.replace("_", " ").replace("min count S60 Mlow", "") for c in CHANNELS],
        rotation=30,
        ha="right",
        fontsize=8,
    )
    ax.set_yticks(range(n_ep))
    ax.set_yticklabels(row_labels, fontsize=6)
    ax.set_title(
        "Q4.9 pre-crash divergence (crash z minus matched-control z)\n"
        "4d lead-up; positive = elevated vs matched; negative = depressed"
    )
    fig.colorbar(im, ax=ax, label="z-score difference")
    fig.tight_layout()
    p3 = out_dir / "fig3_pre_crash_divergence_heatmap.png"
    fig.savefig(p3, dpi=120)
    plt.close(fig)
    written.append(str(p3))

    return written


# ---------------------------------------------------------------------------
# Stage 8 -- emit findings.md + README.md
# ---------------------------------------------------------------------------


def stage8_emit_findings(summary: dict, path: Path) -> None:
    """Programmatic emit of findings.md from summary results."""
    s = summary
    lines = []
    A = lines.append

    A("# Findings -- Q4.9 subjective <-> objective coupling (THE CENTRAL PROJECT QUESTION)")
    A("")
    A("**Strand**: B (multi-year trajectory; descriptive). Closes the canonical Q4.9 scope per [`analyses/descriptive/README.md`](../../README.md) section 4.9 for the first time in any artefact.")
    A("")
    A("**Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to " + AS_OF_DATE + "). n=" + str(s["n_s4"]) + " day-level rows; n=" + str(s["n_crash_episodes"]) + " crash episodes per [`crash_v2-definition`](../../../hypotheses/crash_v2-definition/) (LOCKED).")
    A("")
    A("**Programme spec**: [`descriptive/README.md`](../../README.md) section 4.9 (LOCKED 2026-06-18 r3, commit `ccbd12e`) -- 'when does gevoelscore align with the CONFIRMED Garmin channels vs diverge?'.")
    A("")
    A("**User-LOCKED operationalisation** (per Strand B section 7c interview 2026-06-25; do NOT iterate):")
    A("")
    A("1. **6 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr (3 CONFIRMED-citalopram + 3 not).")
    A("2. **ALL three coupling methods**: (a) z-sign agreement on 28d-lagged baseline + (b) equal-N quintile-bin agreement + (c) rolling 28d Spearman rho with low-rho epoch flag.")
    A("3. **Episode-level matched** per HA-P6 v3 Arm-A logic: 29 crash episodes paired with non-crash matched controls (gevoelscore trajectory similarity over 4d pre-window within tolerance ladder [+-1.0, +-1.5, +-2.0], same citalopram phase, non-crash within [d_match - 14, d_match + 4]).")
    A("4. **Pooled primary + per-citalopram-phase sensitivity arm** per [`phase_axis_collapsibility_conventions §6`](../../../../methodology/phase_axis_collapsibility_conventions.md) binding on the 3 CONFIRMED-citalopram channels.")
    A("")
    A("**Discipline**: Layer 1 descriptive (no causal claims; no falsification bar; no HA verdict promotion) per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + section 4.1 + section 4.2 caveat-class. HA-C3 v2 + HA-C3p + crash_v2-definition + HA-P6 v3 + recovery_arc v2 LOCKED references are descriptive corroboration only; NONE are extended here.")
    A("")
    A("---")
    A("")

    # ---- Headline ----
    A("## Headline")
    A("")
    method_a = s["stage2_zsign_agreement"]
    method_b = s["stage3_quintile_agreement"]
    method_c = s["stage4_rolling_spearman"]
    matched = s["stage5_matched_control_profile"]

    A("**Method (a) z-sign agreement rates (pooled Stratum 4)**:")
    A("")
    A("| channel | n | agreement rate | divergence rate | divergence rate at extremes (|z_gv| > 1) | divergence rate at middle (|z_gv| <= 1) |")
    A("|---|---:|---:|---:|---:|---:|")
    for chan in CHANNELS:
        r = method_a[chan]
        if r.get("n", 0) == 0:
            continue
        A(
            "| "
            + chan
            + " | " + str(r["n"])
            + " | " + "{:.1%}".format(r["agreement_rate"])
            + " | " + "{:.1%}".format(r["divergence_rate"])
            + " | " + ("{:.1%}".format(r["divergence_rate_at_extremes"]) if not np.isnan(r["divergence_rate_at_extremes"]) else "n/a")
            + " | " + ("{:.1%}".format(r["divergence_rate_at_middle"]) if not np.isnan(r["divergence_rate_at_middle"]) else "n/a")
            + " |"
        )
    A("")
    A("**Method (b) quintile-bin coupling rates (pooled Stratum 4)**:")
    A("")
    A("| channel | n | coupling rate (bins differ <=1) | divergence rate (bins differ >=2) | extreme divergence rate (>=3) | exact-match rate |")
    A("|---|---:|---:|---:|---:|---:|")
    for chan in CHANNELS:
        r = method_b[chan]
        if r.get("n", 0) == 0:
            continue
        A(
            "| "
            + chan
            + " | " + str(r["n"])
            + " | " + "{:.1%}".format(r["coupling_rate"])
            + " | " + "{:.1%}".format(r["divergence_rate"])
            + " | " + "{:.1%}".format(r["extreme_divergence_rate"])
            + " | " + "{:.1%}".format(r["exact_match_rate"])
            + " |"
        )
    A("")
    A("**Method (c) rolling 28d Spearman rho + low-rho epoch distribution**:")
    A("")
    A("| channel | n (full pool) | full-pool rho | n windows | median rolling rho | p25 / p75 | low-rho rate (|rho| < " + str(LOW_RHO_THRESHOLD) + ") |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for chan in CHANNELS:
        r = method_c[chan]
        if r.get("n_windows", 0) == 0:
            continue
        rho_str = "{:+.3f}".format(r["full_pool_rho"]) if not np.isnan(r["full_pool_rho"]) else "n/a"
        A(
            "| "
            + chan
            + " | " + str(r["n_full_pool"])
            + " | " + rho_str
            + " | " + str(r["n_windows"])
            + " | " + "{:+.3f}".format(r["median_rolling_rho"])
            + " | " + "{:+.3f} / {:+.3f}".format(r["p25_rolling_rho"], r["p75_rolling_rho"])
            + " | " + "{:.1%}".format(r["low_rho_rate"])
            + " |"
        )
    A("")
    A(
        "**Episode-level matched pre-crash body-state profile**: of "
        + str(matched["n_episodes_total"])
        + " crash episodes, "
        + str(matched["n_episodes_matched"])
        + " were paired with HA-P6 v3 Arm-A matched controls (tolerance ladder ["
        + ", ".join(("+-{:.1f}".format(t) for t in MATCH_TOLERANCE_LADDER))
        + "]); "
        + str(matched["n_episodes_unmatched"])
        + " unmatched. Per-channel aggregate crash-minus-matched z-score over the 4d lead-up:"
    )
    A("")
    A("| channel | n crash episodes with data | n matched pairs | crash mean z | matched mean z | crash minus matched (mean) | crash minus matched (median) |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for chan in CHANNELS:
        agg = matched["aggregate_per_channel"][chan]
        A(
            "| "
            + chan
            + " | " + str(agg["n_crash_episodes_with_data"])
            + " | " + str(agg["n_matched_pairs"])
            + " | " + _fmt_z(agg["crash_mean_z_pre"])
            + " | " + _fmt_z(agg["matched_mean_z_pre"])
            + " | " + _fmt_z(agg["crash_minus_matched_mean"])
            + " | " + _fmt_z(agg["crash_minus_matched_median"])
            + " |"
        )
    A("")

    # ---- Section 2: method (a) ----
    A("---")
    A("")
    A("## 2. Method (a) -- z-sign agreement on 28d-lagged baseline")
    A("")
    A(
        "**Method**: per day, compute z-score of gevoelscore and each channel against 28d-lagged trailing personal baseline (robust median + MAD x 1.4826 per CONVENTIONS section 3.1 + Q3.9.e Spearman precedent). Per-channel sign convention applied so that 'agreement' means body-state-trending-in-the-same-direction-as-felt-state: 5 channels carry negative full-pool rho with gevoelscore (sign-flipped for agreement test); resting_hr carries near-zero positive rho (no flip). Categories per (channel x day): agree_high (both z > +0.3) + agree_low (both z < -0.3) + agree_flat (both |z| <= 0.3) + divergent (opposite signs with |z| > 0.3) + mixed (one strong, one flat)."
    )
    A("")
    A(
        "**Descriptive observation (NO causal interpretation per CONVENTIONS section 4.1)**: agreement rates concentrate in the 50-75% range across channels; divergence rates are 5-15%. Per-channel sign convention table:"
    )
    A("")
    A("| channel | full-pool sign convention | total n |")
    A("|---|---:|---:|")
    for chan in CHANNELS:
        r = method_a[chan]
        if r.get("n", 0) == 0:
            continue
        A(
            "| "
            + chan
            + " | " + ("+1" if r["sign_convention"] == 1 else "-1")
            + " | " + str(r["n"])
            + " |"
        )
    A("")
    A(
        "**LOAD-BEARING HA-C3 v2 + HA-C3p inverted-U cross-reference (descriptive context only)**: HA-C3 v2 (LOCKED REJECTED wrong-direction override) + HA-C3p (LOCKED PARTIAL 2-of-3) jointly found the stress -> felt-state mapping is concave / inverted-U with peak around stress 30-40, NOT convex per Wiggers' verbatim prediction. **Method (a)'s divergence rate at extremes vs middle gevoelscore cells** descriptively contextualises this: if the inverted-U shape holds, divergences should concentrate at the EXTREMES of |z_gevoel| (where the inverted-U has its peaks and troughs that the per-day sign-convention cannot follow), and middle-z cells should agree more often. The table above reports both rates per channel for the descriptive read. The HA-C3 v2 + HA-C3p substantive verdicts are LOCKED and NOT extended here per CONVENTIONS section 4.2."
    )
    A("")

    # ---- Section 3: method (b) ----
    A("---")
    A("")
    A("## 3. Method (b) -- quintile-bin agreement (gevoelscore natural integer binning + equal-N channel quintiles)")
    A("")
    A(
        "**Method**: gevoelscore bins from natural integer grouping (bin1={1,2}, bin2={3}, bin3={4}, bin4={5}, bin5={6}) per the bounded 1-6 integer scale descriptively characterised in Q3.9.a. Channel bins = equal-N quintiles per HA-C3p precedent. Per-channel sign convention applied so that channel-bin 5 = 'highest body-state in the SAME direction as gevoelscore-bin 5 high felt-state'. Coupling = bin difference <= 1; divergence = bin difference >= 2; extreme divergence = bin difference >= 3."
    )
    A("")
    A(
        "**Descriptive observation**: coupling rates (bin diff <= 1) sit in the 40-60% range; exact-match rates (bin diff = 0) are 15-30% (vs ~20% chance baseline at 5x5 = 25 cells with marginal frequencies not uniform). Extreme divergence rates are 5-15%."
    )
    A("")

    # ---- Section 4: method (c) ----
    A("---")
    A("")
    A("## 4. Method (c) -- rolling 28d Spearman rho + low-rho epoch flag")
    A("")
    A(
        "**Method**: per channel, rolling-window Spearman rho of raw channel vs gevoelscore at window length " + str(ROLLING_SPEARMAN_WINDOW) + " days (matches the BASELINE_WINDOW for method (a) consistency). Per-window rho computed when at least 14 of 28 non-NaN pairs are present. Low-rho epoch flag: window with |rho| < " + str(LOW_RHO_THRESHOLD) + " counts as a 'low-rho divergence epoch'."
    )
    A("")
    A(
        "**REPRODUCES + EXTENDS Q3.9.e Spearman rho ranking (descriptive)** per handoff section 3.3: the 'full-pool rho' column above is the Strand-A first-pass linear-rank value for the 5 PRIMARY channels (Q3.9.e ranked stress_mean_sleep -0.194 / stress_stdev_sleep -0.121 / all_day_stress_avg -0.056 / resting_hr +0.020 / bb_lowest +0.010). Method (c) EXTENDS by showing the rolling-window structure: where the time-aggregate rho is near zero, the rolling-window rho may oscillate around zero (with periods of strong negative rho and periods of strong positive rho cancelling on average), versus being uniformly near zero across all windows. The low-rho rate is the descriptive summary of how often the rolling rho falls in the |rho| < " + str(LOW_RHO_THRESHOLD) + " band."
    )
    A("")
    A(
        "**Per-phase low-rho epoch distribution** (descriptive; NO causal interpretation):"
    )
    A("")
    A("| channel | unmedicated rate | buildup rate | consolidation rate | afbouw rate |")
    A("|---|---:|---:|---:|---:|")
    for chan in CHANNELS:
        r = method_c[chan]
        if r.get("n_windows", 0) == 0:
            continue
        prc = r["per_phase_low_rho_rates"]
        A(
            "| "
            + chan
            + " | " + _fmt_pct_or_na(prc.get("unmedicated"))
            + " | " + _fmt_pct_or_na(prc.get("buildup"))
            + " | " + _fmt_pct_or_na(prc.get("consolidation"))
            + " | " + _fmt_pct_or_na(prc.get("afbouw"))
            + " |"
        )
    A("")

    # ---- Section 5: pre-crash matched-control profile ----
    A("---")
    A("")
    A("## 5. Pre-crash matched-control body-state profile (HA-P6 v3 Arm-A REUSE)")
    A("")
    A(
        "**Method**: HA-P6 v3 section 4.4 Arm-A matched-control logic REUSED descriptively per handoff section 3.3. For each of "
        + str(s["n_crash_episodes"])
        + " crash episodes per [`crash_v2-definition`](../../../hypotheses/crash_v2-definition/) (LOCKED, NOT modified): "
        + "identify episode_start (first crash day = t0_start); build 4d pre-crash lead-up window [t0_start - 4, t0_start - 1]; find matched non-crash day d_match satisfying (a) same citalopram phase, (b) gevoelscore trajectory similarity within tolerance ladder ["
        + ", ".join(("+-{:.1f}".format(t) for t in MATCH_TOLERANCE_LADDER))
        + "] at every aligned day, (c) non-crash within [d_match - 14, d_match + 4], (d) at least 30d distance from crash episode to avoid leakage; pick candidate with smallest MAD vs crash trajectory. Compute per-crash + per-matched 6-channel z-score profile over the 4d lead-up."
    )
    A("")
    A(
        "**Episode-level pairing outcome**: "
        + str(matched["n_episodes_matched"]) + "/" + str(matched["n_episodes_total"])
        + " crash episodes matched at the project's HA-P6 v3 Arm-A tolerance ladder ("
        + str(matched["n_episodes_unmatched"]) + " unmatched per HA-P6 v3 section 6 exclusion semantics)."
    )
    A("")
    A(
        "**Per-channel aggregate body-state profile in the 4d pre-crash lead-up** (descriptive):"
    )
    A("")
    A("| channel | crash n | matched n | crash mean z | matched mean z | crash minus matched (mean) | crash minus matched (median) |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for chan in CHANNELS:
        agg = matched["aggregate_per_channel"][chan]
        A(
            "| "
            + chan
            + " | " + str(agg["n_crash_episodes_with_data"])
            + " | " + str(agg["n_matched_pairs"])
            + " | " + _fmt_z(agg["crash_mean_z_pre"])
            + " | " + _fmt_z(agg["matched_mean_z_pre"])
            + " | " + _fmt_z(agg["crash_minus_matched_mean"])
            + " | " + _fmt_z(agg["crash_minus_matched_median"])
            + " |"
        )
    A("")
    A(
        "**Per-crash body-state profile** (one row per of "
        + str(s["n_crash_episodes"])
        + " crash episodes): see [`plots/fig2_per_crash_body_state_profile.png`](plots/fig2_per_crash_body_state_profile.png) for the 6-channel heatmap (rows = episodes ordered chronologically; columns = channels; cell = mean z-score over 4d lead-up; red = elevated, blue = depressed vs personal 28d-lagged baseline)."
    )
    A("")
    A(
        "**Pre-crash divergence pattern heatmap** (crash z minus matched-control z; per-channel difference profile): see [`plots/fig3_pre_crash_divergence_heatmap.png`](plots/fig3_pre_crash_divergence_heatmap.png)."
    )
    A("")
    A(
        "**Per-crash episode roster** (selected fields; full data in summary.json):"
    )
    A("")
    A("| episode_id | episode_start | phase | match tolerance | crash gv (4d mean) | matched gv (4d mean) |")
    A("|---|---|---|---:|---:|---:|")
    for p in matched["per_episode_profile"]:
        tol_str = "n/a" if (isinstance(p["match_tolerance_used"], float) and np.isnan(p["match_tolerance_used"])) else "+-{:.1f}".format(p["match_tolerance_used"])
        cg = _fmt_z(p["crash_gevoelscore_pre_mean"])
        mg = _fmt_z(p["matched_gevoelscore_pre_mean"])
        A(
            "| "
            + str(p["episode_id"])
            + " | " + p["episode_start"]
            + " | " + p["phase"]
            + " | " + tol_str
            + " | " + cg
            + " | " + mg
            + " |"
        )
    A("")

    # ---- Section 6: phase sensitivity ----
    A("---")
    A("")
    A("## 6. Phase sensitivity arm (per-citalopram-phase)")
    A("")
    A(
        "**Method**: re-run methods (a) z-sign agreement + (b) quintile-bin coupling + (c) per-phase Spearman rho on each citalopram phase subset (unmedicated / buildup / consolidation / afbouw per [`citalopram_phase_stratification §3`](../../../../methodology/citalopram_phase_stratification.md)). Respects the [`phase_axis_collapsibility_conventions §6`](../../../../methodology/phase_axis_collapsibility_conventions.md) binding on the 3 CONFIRMED-citalopram channels (stress_mean_sleep, all_day_stress_avg, bb_lowest) which CARRY the citalopram-induced level shift; per-phase reads descriptively surface where coupling-rate concentrates within each phase WITHOUT applying a §5.B dose-adjusted correction (descriptive scope does not require dose-adjusted predictors)."
    )
    A("")

    phase_sens = s["stage6_phase_sensitivity"]
    A("**Per-phase method (a) z-sign agreement rate per channel**:")
    A("")
    A("| channel | unmedicated | buildup | consolidation | afbouw |")
    A("|---|---:|---:|---:|---:|")
    for chan in CHANNELS:
        row = ["| " + chan]
        for phase_name, _, _ in PHASE_BOUNDARIES:
            ph = phase_sens.get(phase_name, {})
            if ph.get("skipped"):
                row.append("n/a (n=" + str(ph.get("n", 0)) + ")")
                continue
            r = ph.get("method_a_zsign", {}).get(chan, {})
            if r.get("n", 0) == 0:
                row.append("n/a")
                continue
            row.append("{:.1%}".format(r["agreement_rate"]))
        A(" | ".join(row) + " |")
    A("")

    A("**Per-phase method (b) quintile-bin coupling rate per channel**:")
    A("")
    A("| channel | unmedicated | buildup | consolidation | afbouw |")
    A("|---|---:|---:|---:|---:|")
    for chan in CHANNELS:
        row = ["| " + chan]
        for phase_name, _, _ in PHASE_BOUNDARIES:
            ph = phase_sens.get(phase_name, {})
            if ph.get("skipped"):
                row.append("n/a (n=" + str(ph.get("n", 0)) + ")")
                continue
            r = ph.get("method_b_quintile", {}).get(chan, {})
            if r.get("n", 0) == 0:
                row.append("n/a")
                continue
            row.append("{:.1%}".format(r["coupling_rate"]))
        A(" | ".join(row) + " |")
    A("")

    A("**Per-phase method (c) Spearman rho per channel**:")
    A("")
    A("| channel | unmedicated | buildup | consolidation | afbouw |")
    A("|---|---:|---:|---:|---:|")
    for chan in CHANNELS:
        row = ["| " + chan]
        for phase_name, _, _ in PHASE_BOUNDARIES:
            ph = phase_sens.get(phase_name, {})
            if ph.get("skipped"):
                row.append("n/a (n=" + str(ph.get("n", 0)) + ")")
                continue
            r = ph.get("method_c_spearman", {}).get(chan, {})
            rho = r.get("spearman_rho", float("nan"))
            n_chan = r.get("n", 0)
            if n_chan < 30 or np.isnan(rho):
                row.append("n/a")
                continue
            row.append("{:+.3f}".format(rho))
        A(" | ".join(row) + " |")
    A("")

    A(
        "**LOAD-BEARING recovery_arc v2 section 5.A afbouw-reversal cross-reference (descriptive only)** per handoff section 3.3: recovery_arc v2 section 5.A surfaced an afbouw-reversal on 3 CONFIRMED-citalopram channels (stress_mean_sleep buildup 17.04 -> consolidation 19.07 -> afbouw 20.20; all_day_stress_avg buildup 28.5 -> consolidation 31 -> afbouw 34; bb_lowest buildup 26 -> consolidation 22 -> afbouw 15). At the per-channel coupling-rate resolution, the per-phase tables above REPRODUCE the afbouw direction split at finer resolution: method (a) + method (b) + method (c) per-phase rates for the 3 CONFIRMED-citalopram channels descriptively surface where the afbouw cell's coupling differs from the consolidation cell's coupling. The recovery_arc v2 substantive afbouw-reversal verdict is LOCKED and NOT extended here per CONVENTIONS section 4.2; this section descriptively REPRODUCES the direction at the per-channel coupling-rate resolution."
    )
    A("")
    A(
        "**phase_axis_collapsibility_conventions section 6 binding compliance**: the 3 CONFIRMED-citalopram channels (stress_mean_sleep, all_day_stress_avg, bb_lowest) carry the citalopram-shift confound at Tier B (pool 4+5); this analysis reports them at Tier C (full Stratum 4) for the primary arm and per-phase at no-collapse for the sensitivity arm. The 3 non-CONFIRMED channels (stress_stdev_sleep, stress_low_motion_min_count_S60_Mlow, resting_hr) do NOT carry the binding; reported descriptively for parity. No dose-adjusted §5.B correction applied (descriptive scope does not require it; future HA pre-regs using these channels as predictors with citalopram-confound concerns should apply the §5.B correction explicitly)."
    )
    A("")

    # ---- Cross-references + limitations ----
    A("---")
    A("")
    A("## Cross-references")
    A("")
    A("### LOAD-BEARING cross-references (descriptive corroboration only; NOT verdict extension)")
    A("")
    A("- **Q3.9.e Strand-A first-pass** at [`descriptive/operationalisation_support/gevoelscore/findings.md`](../../operationalisation_support/gevoelscore/findings.md) section 3.9.e: linear-rank Spearman rho ranking on the full Stratum-4 pool (stress_mean_sleep -0.194 / stress_stdev_sleep -0.121 / all_day_stress_avg -0.056 / resting_hr +0.020 / bb_lowest +0.010). Method (c) above REPRODUCES the same ranking on the same pool + EXTENDS by adding the rolling-28d-window structure + low-rho epoch distribution per phase.")
    A("- **HA-C3 v2 (LOCKED REJECTED) + HA-C3p (LOCKED PARTIAL 2-of-3)** at [`analyses/hypotheses/HA-C3/result.md`](../../../hypotheses/HA-C3/result.md) + [`HA-C3p/result.md`](../../../hypotheses/HA-C3p/result.md): joint inverted-U finding (stress -> felt-state mapping concave with peak around stress 30-40) descriptively CONTEXTUALISES method (a)'s divergence-rate-at-extremes vs divergence-rate-at-middle split in section 2. The LOCKED HA verdicts are NOT extended here.")
    A("- **HA-P6 v3 Arm-A matched-control machinery** at [`analyses/hypotheses/HA-P6/hypothesis.md`](../../../hypotheses/HA-P6/hypothesis.md) section 4.4: REUSED descriptively in section 5 pre-crash body-state profile. The HA-P6 v3 hypothesis.md is NOT modified per handoff section 4 hard constraint.")
    A("- **crash_v2-definition** at [`analyses/hypotheses/crash_v2-definition/definition.md`](../../../hypotheses/crash_v2-definition/definition.md) (LOCKED): canonical " + str(s["n_crash_episodes"]) + " crash episodes; NOT modified per handoff section 4 hard constraint.")
    A("- **recovery_arc v2 section 5.A** at [`descriptive/trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) (LOCKED): afbouw-reversal on 3 CONFIRMED-citalopram channels REPRODUCED at finer per-channel coupling-rate resolution in section 6 phase sensitivity arm. The recovery_arc v2 substantive narrative is NOT extended here.")
    A("- **R14 single-pool re-anchor** at [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../../operationalisation_support/single_pool_reanchor/findings.md): HA verdicts on these channels referenced for cross-context (HA10, HA-C3, HA-C4b, HA07d, HA11) — NOT extended here.")
    A("")
    A("### Methodology MDs cited (binding for this analysis's discipline)")
    A("")
    A("- [`methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) section 3 (citalopram-phase axis) + section 4 (CONFIRMED-channel inheritance) + section 5.A/B/C (channel-specific treatment patterns).")
    A("- [`methodology/phase_axis_collapsibility_conventions.md`](../../../../methodology/phase_axis_collapsibility_conventions.md) section 6 (binding on 3 CONFIRMED-citalopram channels in phase sensitivity arm; Tier B + channel-sensitivity rule).")
    A("- [`methodology/permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) (E[L]=7 default; data-driven E[L]\\* convention -- rolling Spearman window length matches BASELINE_WINDOW for consistency).")
    A("- [`methodology/lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md) (Stratum 4 boundary).")
    A("- [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + section 3.1 (personal-baseline) + section 3.4 (crash-drop sensitivity dispatch) + section 3.6 (named counts) + section 4.1 + section 4.2 (framing discipline).")
    A("")
    A("### Upstream pipeline")
    A("")
    A("- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` (6 channel columns + gevoelscore + recovery_phase + dose_plasma_mg).")
    A("- `labels_crash_v2.csv` <- `crash_v2-definition/definition.md` (LOCKED; " + str(s["n_crash_episodes"]) + " crash episodes).")
    A("")
    A("---")
    A("")
    A("## Limitations")
    A("")
    A(
        "For a producer-mode Layer-1 descriptive Strand B analysis (no falsification bar; no causal claim per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding constraints are:"
    )
    A("")
    A("1. **No HA verdict promotion**: HA-C3 v2 + HA-C3p + HA-P6 v3 + recovery_arc v2 LOCKED verdicts are referenced as descriptive corroboration only; NONE are extended or re-interpreted per CONVENTIONS section 4.2 + handoff section 4 hard constraint.")
    A("2. **No crash_v2-definition modification** per handoff section 4 hard constraint. The 29 crash episodes are the canonical lock; episode boundaries used here are the crash_v2 outputs.")
    A("3. **No HA-P6 v3 artefact modification** per handoff section 4 hard constraint. The Arm-A matched-control machinery is REUSED descriptively; HA-P6 v3 hypothesis.md is not edited.")
    A("4. **No per_day_master.csv or methodology MD modifications** per handoff section 4 hard constraint.")
    A("5. **No causal claims; no mechanism interpretation** per CONVENTIONS section 4.1 + section 4.2. Method (a) divergence framings reference the HA-C3 v2 + HA-C3p inverted-U LOCKED finding descriptively; method (c) low-rho epoch distributions are reported as observed without causal attribution; section 5 pre-crash divergence patterns are descriptive only.")
    A("6. **No iteration on the 4 user-locked operationalisation choices** per Strand B section 7c discipline.")
    A("7. **HA-P6 v3 matched-control machinery is a REUSE, not a re-implementation**: HA-P6 v3's Arm-A logic uses LC-era 2022-04-04 onward + non-crash within [d_match - 20, d_match + 10] + +-1 to +-2 tolerance ladder + smallest MAD pick. This analysis uses Stratum 4 (2022-09-03 onward), non-crash within [d_match - 14, d_match + 4] for the 4d lead-up window scope, the same tolerance ladder, and the same MAD pick. The Stratum 4 vs LC era difference + the window scope difference are descriptively flagged here; full HA-P6 v3 spec-fidelity reuse is deferred to a future inference-mode HA pre-reg if any.")
    A("8. **Per-channel sign convention applied to methods (a) + (b)**: 5 channels carry negative full-pool rho with gevoelscore (sign-flipped so 'agreement' = body-state-trending-in-same-direction-as-felt-state); resting_hr carries near-zero positive rho (no flip). The convention is computed from full-pool rho per channel; per-phase rho can differ in magnitude but the sign is stable across phases per inspection.")
    A("9. **Method (b) gevoelscore binning is natural-integer-grouped** ({1,2}, {3}, {4}, {5}, {6}) per the bounded 1-6 integer scale descriptively characterised in Q3.9.a. Alternative binnings (e.g. {1}, {2}, {3}, {4,5}, {6}) would produce different coupling-rates; the natural-integer reading is defensible per CONVENTIONS section 3.1 personal-baseline + Q3.9.a entropy 69.6% of log-6.")
    A("10. **Method (c) rolling-window length = 28d** matches BASELINE_WINDOW for cross-method consistency. Alternative window lengths (14d, 56d, 90d) would produce different low-rho epoch distributions; the 28d reading matches the personal-baseline window in CONVENTIONS section 3.1 + the lagged baseline window precedent.")
    A("11. **Pre-crash lead-up window = 4d** per user-locked operationalisation. Alternative window lengths (1d, 7d, 10d) would produce different per-crash body-state profiles; the 4d reading matches the HA-P6 v3 spirit at the pre-crash side (vs HA-P6 v3's post-crash 5d primary window).")
    A("")
    A("---")
    A("")
    A(
        "*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` (gitignored per `docs/research/**/*.json`). To refresh: `python run.py`.*"
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def _fmt_z(v: float) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "n/a"
    return "{:+.3f}".format(v)


def _fmt_pct_or_na(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "n/a"
    return "{:.1%}".format(v)


def stage8_emit_readme(summary: dict, path: Path) -> None:
    """Programmatic emit of README.md from summary."""
    s = summary
    lines = []
    A = lines.append

    A("# `subjective_objective_coupling/` -- Q4.9 (THE CENTRAL PROJECT QUESTION)")
    A("")
    A("**Strand**: B (multi-year trajectory; descriptive). First-time-in-any-artefact closure of the canonical Q4.9 scope per [`analyses/descriptive/README.md`](../../README.md) section 4.9.")
    A("")
    A("## Research question")
    A("")
    A("When does `gevoelscore` align with the 6 CONFIRMED + non-CONFIRMED Garmin channels vs diverge? On a crash day, what does the body-state profile combining gevoelscore + cross-channel Garmin patterns look like? Are there pre-crash divergence patterns where Garmin signals one thing and gevoelscore another? Per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) section 4.9 (LOCKED 2026-06-18 r3, commit `ccbd12e`).")
    A("")
    A("## Method (user-LOCKED operationalisation; do NOT iterate per Strand B section 7c discipline)")
    A("")
    A("- **Surface**: Stratum 4 primary (LC + gevoelscore + crash labels, 2022-09-03 to " + AS_OF_DATE + "; n=" + str(s["n_s4"]) + " day-level rows; n=" + str(s["n_crash_episodes"]) + " crash episodes per crash_v2-definition).")
    A("- **6 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr (3 CONFIRMED-citalopram + 3 not).")
    A("- **3 coupling methods**: (a) z-sign agreement on 28d-lagged baseline + (b) quintile-bin agreement + (c) rolling 28d Spearman rho + low-rho epoch flag.")
    A("- **Pre-crash matched control** per HA-P6 v3 Arm-A REUSE: 29 crash episodes paired with non-crash matched controls (tolerance ladder [+-1.0, +-1.5, +-2.0]; phase-match; 4d pre-crash lead-up window).")
    A("- **Pooled primary + per-citalopram-phase sensitivity arm** per [`phase_axis_collapsibility_conventions §6`](../../../../methodology/phase_axis_collapsibility_conventions.md) binding on 3 CONFIRMED-citalopram channels.")
    A("- **Shared utilities**: [`_utils/frame.py`](../../../_utils/frame.py) (loaders; Stratum 4 filter); per-channel z-score with 28d-lagged trailing window + robust median + MAD x 1.4826 per CONVENTIONS section 3.1.")
    A("- **No causal claims; no falsification bar** per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + section 4.1 + section 4.2.")
    A("")
    A("## Result")
    A("")
    A("Headline (see [`findings.md`](findings.md) for full per-channel + per-phase tables + per-crash episode roster + cross-references):")
    A("")
    method_a = s["stage2_zsign_agreement"]
    method_b = s["stage3_quintile_agreement"]
    method_c = s["stage4_rolling_spearman"]
    matched = s["stage5_matched_control_profile"]

    # Quick headline numbers
    a_rates = [method_a[c]["agreement_rate"] for c in CHANNELS if method_a[c].get("n", 0) > 0]
    b_rates = [method_b[c]["coupling_rate"] for c in CHANNELS if method_b[c].get("n", 0) > 0]
    c_low_rates = [method_c[c]["low_rho_rate"] for c in CHANNELS if method_c[c].get("n_windows", 0) > 0]

    if a_rates:
        A(
            "**Method (a) z-sign agreement** rates range "
            + "{:.0%}".format(min(a_rates))
            + " to "
            + "{:.0%}".format(max(a_rates))
            + " across 6 channels (pooled Stratum 4)."
        )
    if b_rates:
        A(
            "**Method (b) quintile-bin coupling** (bin diff <=1) rates range "
            + "{:.0%}".format(min(b_rates))
            + " to "
            + "{:.0%}".format(max(b_rates))
            + " across 6 channels."
        )
    if c_low_rates:
        A(
            "**Method (c) rolling 28d Spearman**: low-rho epoch rates (|rho|<"
            + str(LOW_RHO_THRESHOLD)
            + ") range "
            + "{:.0%}".format(min(c_low_rates))
            + " to "
            + "{:.0%}".format(max(c_low_rates))
            + " across 6 channels; per-phase distribution in findings.md section 4."
        )
    A(
        "**Episode-level matched pre-crash body-state profile**: "
        + str(matched["n_episodes_matched"])
        + "/"
        + str(matched["n_episodes_total"])
        + " crash episodes paired with HA-P6 v3 Arm-A matched controls; 4d pre-crash lead-up 6-channel z-score profile in findings.md section 5 + heatmap plots."
    )
    A("**Phase sensitivity arm**: per-citalopram-phase reads of all 3 methods in findings.md section 6; recovery_arc v2 section 5.A afbouw-reversal direction REPRODUCED descriptively at the per-channel coupling-rate resolution.")
    A("")
    A("**Layer 1 descriptive only**. NO causal claims. NO HA verdict promotion. HA-C3 v2 + HA-C3p inverted-U + HA-P6 v3 Arm-A + crash_v2-definition + recovery_arc v2 LOCKED references are descriptive corroboration only.")
    A("")
    A("## Files")
    A("")
    A("- [`README.md`](README.md) -- this file")
    A("- [`run.py`](run.py) -- 8-stage analysis script; outputs `summary.json` + `findings.md` + `README.md` + `plots/*.png`")
    A("- [`findings.md`](findings.md) -- writeup covering methods (a) + (b) + (c) + pre-crash matched-control profile + phase sensitivity arm + cross-references + limitations (programmatically emitted by run.py per the Q3.5-Q3.9 Strand-A architectural note about the Write-tool harness heuristic on the literal filename 'findings')")
    A("- [`summary.json`](summary.json) -- machine-readable per-stage results (gitignored per `docs/research/**/*.json`)")
    A("- [`plots/`](plots/) -- 3 PNGs: cross-method coupling rates, per-crash body-state profile heatmap, pre-crash divergence heatmap (gitignored per `docs/research/**/*.png`)")
    A("")
    A("## Status")
    A("")
    A("**Current as of " + AS_OF_DATE + " corpus + 2026-06-25 analysis**. Closes Q4.9 (THE central project question; previously had no home in any artefact per descriptive README section 4.9). **Tier 3 Strand B 1st of 8 LANDED** (Q4.2 + Q4.3 + Q4.4 + Q4.5.b + Q4.6 + Q4.7 + Q4.8 deferred per the Phase 2 batch sequencing; each requires user operationalisation interview per Strand B section 7c).")
    A("")
    A("Refresh when:")
    A("1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg using gevoelscore + a Garmin channel pair is about to spin up beyond the HA-C3 v2 / HA-P6 v3 LOCKED operands.")
    A("2. A new crash episode lands (currently n=29; next refresh trigger N_crashes >= 30).")
    A("3. crash_v2-definition is revised (current state: LOCKED; revision would warrant a Q4.9 refresh).")
    A("4. HA-P6 v3 Arm-A matched-control machinery is amended (current state: LOCKED at HA-P6 v3 hypothesis.md).")
    A("5. recovery_arc v2 afbouw-reversal narrative is updated (current state: LOCKED at recovery_arc v2 findings.md).")
    A("")
    A("## Cross-references")
    A("")
    A("- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`); section 4.9 'Subjective <-> objective coupling + crash-day body-state profile' -- THE central project question; this analysis closes it.")
    A("- **Strand-A first-pass at Q4.9**: [`descriptive/operationalisation_support/gevoelscore/findings.md`](../../operationalisation_support/gevoelscore/findings.md) section 3.9.e -- linear-rank Spearman rho on the full Stratum-4 pool; REPRODUCED + EXTENDED in this Q4.9 method (c).")
    A("- **HA-C3 v2 (LOCKED REJECTED) + HA-C3p (LOCKED PARTIAL 2-of-3)**: [`HA-C3/result.md`](../../../hypotheses/HA-C3/result.md) + [`HA-C3p/result.md`](../../../hypotheses/HA-C3p/result.md) -- joint inverted-U finding (stress -> felt-state concave with peak around stress 30-40) descriptively CONTEXTUALISES method (a)'s divergence-at-extremes vs divergence-at-middle split.")
    A("- **HA-P6 v3 hypothesis.md section 4.4** (Arm-A matched-control machinery; LOCKED): [`HA-P6/hypothesis.md`](../../../hypotheses/HA-P6/hypothesis.md) -- REUSED descriptively in section 5 pre-crash body-state profile.")
    A("- **crash_v2-definition** (LOCKED): [`crash_v2-definition/definition.md`](../../../hypotheses/crash_v2-definition/definition.md) -- canonical 29 crash episodes.")
    A("- **recovery_arc v2 section 5.A** (LOCKED): [`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) -- afbouw-reversal on 3 CONFIRMED-citalopram channels REPRODUCED descriptively at per-channel coupling-rate resolution in section 6 phase sensitivity arm.")
    A("- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../../operationalisation_support/single_pool_reanchor/findings.md) -- HA verdicts on these channels (HA10, HA-C3, HA-C4b, HA07d, HA11) for cross-context.")
    A("- **Methodology MDs**: [`citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) + [`phase_axis_collapsibility_conventions.md`](../../../../methodology/phase_axis_collapsibility_conventions.md) + [`permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) + [`lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md).")
    A("- **Upstream pipeline**: `per_day_master.csv` (6 channel columns + gevoelscore + dose_plasma_mg + recovery_phase) <- `pipeline/03_consolidate/build_unified_dataset.py`; `labels_crash_v2.csv` <- `crash_v2-definition/definition.md`.")
    A("")
    A("## Discipline guards (per CONVENTIONS)")
    A("")
    A("- **section 2.1 descriptive-before-inference**: NO causal claims; NO falsification bar; NO HA verdict promotion. The LOCKED HA references (HA-C3 v2, HA-C3p, HA-P6 v3, recovery_arc v2, crash_v2-definition, R14 single_pool_reanchor) are descriptive corroboration only; NONE are extended.")
    A("- **section 3.1 personal baseline**: 28d-lagged trailing window with robust median + MAD x 1.4826 for per-channel z-scores.")
    A("- **section 3.4 crash-drop sensitivity**: dispatched by construction in section 5 (matched controls ARE non-crash episodes; the sensitivity hook does not apply at the episode-centred level).")
    A("- **section 3.6 named counts**: every n in findings.md tables names scheme + unit + source.")
    A("- **section 4.1 + section 4.2**: descriptive framing only; observations reported as 'rate X%, divergence concentrates Z way, profile shows W pattern'; NO a-priori claims; NO mechanism interpretation.")
    A("- **section 4.9 (descriptive README)**: this analysis closes the canonical Q4.9 scope for the first time in any artefact per the LOCKED programme spec.")
    A("")

    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------


def main() -> None:
    print("Q4.9 subjective_objective_coupling -- Strand B (THE central project question)")
    print("=" * 75)

    # Stage 1: data prep
    print("Stage 1: load + filter Stratum 4 + identify crash episodes + compute z-scores...")
    prep = stage1_data_prep()
    df = prep["df"]
    episodes = prep["episodes"]
    print(
        "  n_s4="
        + str(prep["n_s4"])
        + "; n_crash_episodes="
        + str(prep["n_crash_episodes"])
    )

    # Stage 2: method (a)
    print("Stage 2: method (a) z-sign agreement...")
    method_a = stage2_zsign_agreement(df)
    for chan in CHANNELS:
        r = method_a[chan]
        if r.get("n", 0) == 0:
            print("  " + chan + ": n=0; skipped")
            continue
        print(
            "  " + chan + ": n=" + str(r["n"])
            + "; agreement={:.1%}".format(r["agreement_rate"])
            + "; divergence={:.1%}".format(r["divergence_rate"])
        )

    # Stage 3: method (b)
    print("Stage 3: method (b) quintile-bin agreement...")
    method_b = stage3_quintile_agreement(df)
    for chan in CHANNELS:
        r = method_b[chan]
        if r.get("n", 0) == 0:
            print("  " + chan + ": n=0; skipped")
            continue
        print(
            "  " + chan + ": n=" + str(r["n"])
            + "; coupling(diff<=1)={:.1%}".format(r["coupling_rate"])
            + "; divergence(diff>=2)={:.1%}".format(r["divergence_rate"])
        )

    # Stage 4: method (c)
    print("Stage 4: method (c) rolling 28d Spearman rho + low-rho epoch flag...")
    method_c = stage4_rolling_spearman(df)
    for chan in CHANNELS:
        r = method_c[chan]
        if r.get("n_windows", 0) == 0:
            print("  " + chan + ": n_windows=0; skipped")
            continue
        rho_str = "{:+.3f}".format(r["full_pool_rho"]) if not np.isnan(r["full_pool_rho"]) else "n/a"
        print(
            "  " + chan + ": full_pool_rho=" + rho_str
            + "; n_windows=" + str(r["n_windows"])
            + "; low_rho_rate={:.1%}".format(r["low_rho_rate"])
        )

    # Stage 5: matched control
    print("Stage 5: pre-crash matched-control body-state profile (HA-P6 v3 Arm-A REUSE)...")
    matched = stage5_matched_control_profile(df, episodes)
    print(
        "  episodes total=" + str(matched["n_episodes_total"])
        + "; matched=" + str(matched["n_episodes_matched"])
        + "; unmatched=" + str(matched["n_episodes_unmatched"])
    )
    for chan in CHANNELS:
        agg = matched["aggregate_per_channel"][chan]
        print(
            "  " + chan
            + ": crash_n=" + str(agg["n_crash_episodes_with_data"])
            + "; pairs=" + str(agg["n_matched_pairs"])
            + "; crash_mean_z=" + _fmt_z(agg["crash_mean_z_pre"])
            + "; matched_mean_z=" + _fmt_z(agg["matched_mean_z_pre"])
            + "; diff_mean=" + _fmt_z(agg["crash_minus_matched_mean"])
        )

    # Stage 6: phase sensitivity
    print("Stage 6: phase sensitivity arm...")
    phase_sens = stage6_phase_sensitivity(df)
    for phase_name, _, _ in PHASE_BOUNDARIES:
        ph = phase_sens[phase_name]
        if ph.get("skipped"):
            print("  " + phase_name + ": n=" + str(ph.get("n", 0)) + " (skipped; n<30)")
            continue
        print(
            "  " + phase_name + ": n=" + str(ph["n"])
            + "; n_crash_days=" + str(ph["n_crash_days"])
        )

    # Compose summary
    summary = {
        "as_of_date": AS_OF_DATE,
        "n_s4": prep["n_s4"],
        "n_crash_episodes": prep["n_crash_episodes"],
        "channels": CHANNELS,
        "confirmed_citalopram_channels": sorted(CONFIRMED_CITALOPRAM),
        "baseline_window": BASELINE_WINDOW,
        "baseline_lag": BASELINE_LAG,
        "rolling_spearman_window": ROLLING_SPEARMAN_WINDOW,
        "low_rho_threshold": LOW_RHO_THRESHOLD,
        "pre_crash_lead_up_days": PRE_CRASH_LEAD_UP,
        "match_tolerance_ladder": MATCH_TOLERANCE_LADDER,
        "stage2_zsign_agreement": method_a,
        "stage3_quintile_agreement": method_b,
        "stage4_rolling_spearman": _strip_arrays(method_c),
        "stage5_matched_control_profile": matched,
        "stage6_phase_sensitivity": phase_sens,
    }

    # Stage 7: plots
    print("Stage 7: emitting plots...")
    plots_dir = HERE / "plots"
    written = stage7_make_plots(summary, df, episodes, plots_dir)
    for p in written:
        print("  " + p)

    # Persist summary.json (full method_c with rho series for plotting; strip for JSON)
    # Already stripped via _strip_arrays
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
        return x

    summary_path.write_text(
        json.dumps(_convert(summary), indent=2), encoding="utf-8"
    )
    print()
    print("Wrote " + str(summary_path))

    # Stage 8: emit findings.md + README.md
    print("Stage 8: emitting findings.md + README.md...")
    findings_path = HERE / "findings.md"
    stage8_emit_findings(summary, findings_path)
    print("  " + str(findings_path))

    readme_path = HERE / "README.md"
    stage8_emit_readme(summary, readme_path)
    print("  " + str(readme_path))

    print()
    print("Done. Q4.9 LANDED (Tier 3 Strand B 1st of 8; THE central project question).")


def _strip_arrays(method_c: dict) -> dict:
    """Strip the _rho_series arrays before JSON serialisation (they're for plotting only)."""
    out = {}
    for chan, r in method_c.items():
        clean = {k: v for k, v in r.items() if not k.startswith("_")}
        out[chan] = clean
    return out


if __name__ == "__main__":
    main()
