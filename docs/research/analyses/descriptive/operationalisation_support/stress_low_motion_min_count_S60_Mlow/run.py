"""Descriptive analysis: stress_low_motion_min_count_S60_Mlow operationalisation support.

Answers Q3.x.a-i per the locked descriptive programme:
``docs/research/analyses/descriptive/README.md`` §3.1 template (LOCKED r3
2026-06-18, commit ccbd12e) generalised to this channel per §6.3 (r2
closure D1.8 two-gaps-one-analysis). Phase 1 third analysis; Strand A
template-driven (no operationalisation interview required per §7b).

Channel: per-day count of minutes where Garmin stress(t) >= 60 AND
intensity(t) <= 1 (low-motion class). Primary per
``methodology/stress_low_motion_primitive.md §4`` (Session E lock
2026-06-15).

Count-primitive adaptations of the Q-template (vs continuous-channel
first analysis stress_mean_sleep):
- Q3.x.a reports zero-rate explicitly alongside heavy-tail flag.
- Q3.x.c includes per-phase zero-rate.
- Q3.x.e includes the 8 sibling sensitivity-ladder columns as natural
  near-identity peers (highly correlated by construction; the
  diagnostic value is whether the primary is degenerate with a
  neighbour or carries independent signal).
- Q3.x.f reports median difference + Mann-Whitney U alongside Cohen's d
  (count data with possible zero-inflation may be Cohen's-d-sensitive).
- Q3.x.g notes "the channel IS the spike primitive by construction"
  per CONVENTIONS §3.5; describes the sensitivity-ladder coverage +
  relation to the continuous daily-aggregate cousin all_day_stress_avg.

Output: ``summary.json`` (machine-readable per-question results) +
``plots/*.png`` (visualisations). The hand-written ``findings.md`` reads
from these.

Discipline guards (per CONVENTIONS):
- §2.1 descriptive-before-inference: no causal claims; no falsification bar.
- §3.1 personal baseline: distribution shape is reported as-is;
  phase-stratified to surface citalopram-threshold confound.
- §3.3 column-duplication: near-identity check at |rho|>=0.92.
- §3.4 crash-drop sensitivity: |Delta|>0.10 flag surfaced.
- §3.5 spike metrics: the channel IS a spike-counting primitive by
  construction (Q3.x.g).
- §3.6 named counts: every count reports scheme + unit + source file.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
# HERE = .../analyses/descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow
# parents[0]=operationalisation_support, [1]=descriptive, [2]=analyses
UTILS_DIR = HERE.parents[2] / "_utils"
sys.path.insert(0, str(UTILS_DIR))

from frame import (  # noqa: E402
    crash_drop_sensitivity,
    filter_to_stratum_4,
    load_crash_labels,
    load_master,
)
from inference import (  # noqa: E402
    compute_data_driven_block_length,
    stationary_bootstrap_ci,
)


CHANNEL = "stress_low_motion_min_count_S60_Mlow"
AS_OF_DATE = "2026-06-05"  # parity with stress_mean_sleep first analysis

# Citalopram phase boundaries per
# methodology/citalopram_phase_stratification.md §3
PHASE_BOUNDARIES = [
    ("unmedicated", date(2022, 9, 3), date(2024, 4, 8)),
    ("buildup", date(2024, 4, 9), date(2024, 6, 19)),
    ("consolidation", date(2024, 6, 20), date(2026, 3, 19)),
    ("afbouw", date(2026, 3, 20), date(2026, 6, 5)),
]

# Sensitivity-ladder sibling columns per stress_low_motion_primitive.md §4.
# The primary S60_Mlow is the centre; 8 siblings cover the 3x3 lattice.
SIBLING_COLUMNS = [
    "stress_low_motion_min_count_S50_Mstrict",
    "stress_low_motion_min_count_S50_Mlow",
    "stress_low_motion_min_count_S50_Mbelow_mod",
    "stress_low_motion_min_count_S60_Mstrict",
    # S60_Mlow is the primary; excluded from the sibling list
    "stress_low_motion_min_count_S60_Mbelow_mod",
    "stress_low_motion_min_count_S75_Mstrict",
    "stress_low_motion_min_count_S75_Mlow",
    "stress_low_motion_min_count_S75_Mbelow_mod",
]

# Respiration companion columns per stress_low_motion_primitive.md §4b
RESP_COMPANIONS = [
    "n_minutes_resp_above_18",
    "n_minutes_resp_in_rest_band_10_18",
]

# Continuous cousins per primitive MD §10 + the project's autonomic-load family
CONTINUOUS_COUSINS = [
    "stress_mean_sleep",
    "stress_stdev_sleep",
    "all_day_stress_avg",
    "all_day_stress_max",
    "awake_stress_avg",
    "asleep_stress_avg_uds",
]

NEAR_IDENTITY_THRESHOLD = 0.92  # CONVENTIONS §3.3


def citalopram_phase(d) -> str:
    # Coerce to datetime.date defensively (pandas Timestamp does not compare
    # to datetime.date directly)
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
# Q3.x.a Distribution shape (count-primitive adaptation: zero-rate explicit)
# ---------------------------------------------------------------------------


def q_a_distribution(values: pd.Series) -> dict:
    """Distribution shape on Stratum 4 (Q3.x.a).

    Count-primitive adaptation: zero-rate reported explicitly + tail
    quantiles (p90, p95, p99) called out.
    """
    v = values.dropna().astype(float)
    n = int(len(v))
    mean = float(v.mean())
    median = float(v.median())
    std = float(v.std(ddof=1))
    mad = float(np.median(np.abs(v - median)))
    quantiles = {f"p{q}": float(np.percentile(v, q))
                 for q in (1, 5, 10, 25, 50, 75, 90, 95, 99)}
    centered = v - mean
    m2 = float((centered ** 2).mean())
    m3 = float((centered ** 3).mean())
    skewness = m3 / (m2 ** 1.5) if m2 > 0 else float("nan")
    m4 = float((centered ** 4).mean())
    excess_kurtosis = m4 / (m2 ** 2) - 3.0 if m2 > 0 else float("nan")
    heavy_tail = bool((quantiles["p99"] / max(median, 1.0) > 3.0) or skewness > 1.0)
    n_zero = int((v == 0).sum())
    zero_rate = n_zero / n if n > 0 else float("nan")
    return {
        "n": n,
        "mean": mean,
        "median": median,
        "std_ddof1": std,
        "mad_unscaled": mad,
        "mad_normal_equivalent": mad * 1.4826,
        "quantiles": quantiles,
        "skewness": skewness,
        "excess_kurtosis": excess_kurtosis,
        "heavy_tail_flag": heavy_tail,
        "min": float(v.min()),
        "max": float(v.max()),
        "n_zero_days": n_zero,
        "zero_rate": zero_rate,
        "zero_inflation_flag": bool(zero_rate >= 0.10),
        "unit": "minutes/day (integer count)",
    }


# ---------------------------------------------------------------------------
# Q3.x.b Autocorrelation + E[L]*
# ---------------------------------------------------------------------------


def q_b_autocorrelation(values: pd.Series) -> dict:
    """Autocorrelation + Politis-White E[L]* (Q3.x.b)."""
    arr = values.dropna().to_numpy()
    result = compute_data_driven_block_length(arr, default_block_length=7)
    acf = result["autocorrelations"]
    lags_of_interest = {}
    for k in (1, 2, 3, 7, 14, 28):
        if len(acf) > k:
            lags_of_interest[f"acf_lag{k}"] = float(acf[k])
    n_arr = len(arr)
    politis_white_threshold = float(2.0 * np.sqrt(np.log(n_arr) / n_arr))
    return {
        "n_non_nan": int(n_arr),
        "default_E_L": 7,
        "data_driven_E_L_star": float(result["optimal_block_length"]),
        "cutoff_lag_M": result["cutoff_lag"],
        "factor_of_2_deviation_flag": bool(result["flagged_deviation"]),
        "deviation_ratio": float(abs(result["optimal_block_length"] - 7) / 7),
        "politis_white_significance_threshold_2sigma": politis_white_threshold,
        "politis_white_threshold_formula": (
            "2 * sqrt(log(n) / n) per Politis-White 2004 + inference.py"
        ),
        "note": result.get("note", ""),
        "selected_acf_lags": lags_of_interest,
        # Comparison anchor for findings.md: stress_mean_sleep first analysis
        # observed E[L]*=12.6 on the same Stratum 4 surface.
        "comparison_anchor_stress_mean_sleep_E_L_star": 12.6,
    }


# ---------------------------------------------------------------------------
# Q3.x.c Base rates per phase (count-primitive: include zero-rate per phase)
# ---------------------------------------------------------------------------


def q_c_base_rates_per_phase(df: pd.DataFrame, channel: str) -> dict:
    """Per-phase n + median + dispersion + zero-rate (Q3.x.c).

    Count-primitive adaptation: per-phase zero-rate added.
    Cross-tabulated against the 6-phase lc_recovery_phase_axis where
    available.
    """
    out = {"by_citalopram_phase": {}, "by_recovery_phase": {}}
    # Primary: 4-phase citalopram axis (parity with stress_mean_sleep)
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))
        sub = df.loc[mask, channel].dropna().astype(float)
        n = int(len(sub))
        if n == 0:
            out["by_citalopram_phase"][phase_name] = {"n": 0}
            continue
        med = float(sub.median())
        n_zero = int((sub == 0).sum())
        out["by_citalopram_phase"][phase_name] = {
            "n": n,
            "date_start": str(start),
            "date_end": str(end),
            "mean": float(sub.mean()),
            "median": med,
            "std_ddof1": float(sub.std(ddof=1)),
            "mad_unscaled": float(np.median(np.abs(sub - med))),
            "p10": float(np.percentile(sub, 10)),
            "p25": float(np.percentile(sub, 25)),
            "p75": float(np.percentile(sub, 75)),
            "p90": float(np.percentile(sub, 90)),
            "p99": float(np.percentile(sub, 99)),
            "n_zero_days": n_zero,
            "zero_rate": n_zero / n,
        }

    # Secondary: 6-phase recovery axis (LOCKED 2026-06-19 d47e0d3)
    if "recovery_phase" in df.columns:
        for phase_name, sub_df in df.groupby("recovery_phase", dropna=True):
            vals = sub_df[channel].dropna().astype(float)
            n = int(len(vals))
            if n == 0:
                continue
            med = float(vals.median())
            n_zero = int((vals == 0).sum())
            out["by_recovery_phase"][str(phase_name)] = {
                "n": n,
                "mean": float(vals.mean()),
                "median": med,
                "mad_unscaled": float(np.median(np.abs(vals - med))),
                "p25": float(np.percentile(vals, 25)),
                "p75": float(np.percentile(vals, 75)),
                "p90": float(np.percentile(vals, 90)),
                "zero_rate": n_zero / n,
            }
        # Cross-tab counts (citalopram x recovery) per the structural finding
        # that recovery_phase finer-grains the unmedicated portion of cital axis
        df_cross = df[[channel, "recovery_phase"]].dropna().copy()
        df_cross["_cital"] = df["date"].apply(citalopram_phase)
        cross = (df_cross.groupby(["recovery_phase", "_cital"])[channel]
                 .agg(["count", "median"]).reset_index())
        out["cross_tab_recovery_vs_citalopram"] = [
            {"recovery_phase": str(r["recovery_phase"]),
             "citalopram_phase": str(r["_cital"]),
             "n": int(r["count"]),
             "median": float(r["median"])}
            for _, r in cross.iterrows()
        ]

    return out


# ---------------------------------------------------------------------------
# Q3.x.d Phase-stratified distribution + citalopram threshold-shift impact
# ---------------------------------------------------------------------------


def q_d_phase_stratified(per_phase: dict, channel: str) -> dict:
    """Phase-stratified distribution + count-primitive citalopram caveat (Q3.x.d).

    Key adaptation vs stress_mean_sleep: the per-mg dose-response slope
    on THIS count primitive is NOT a locked finding. The dose-modulation
    operates UPSTREAM on the raw stress channel (+12-17 raw stress points
    at 30mg per the dose-response v3); that shifts how many minutes per
    day cross the S=60 threshold even if true sympathetic-rest-arousal
    is constant. Document the qualitative direction; do not extrapolate
    a per-mg slope on the count.
    """
    cital = per_phase.get("by_citalopram_phase", {})
    out = {
        "phase_medians": {},
        "phase_zero_rates": {},
        "phase_to_phase_shifts": {},
    }
    medians = {}
    zero_rates = {}
    for phase_name in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = cital.get(phase_name, {})
        if info.get("n", 0) > 0:
            medians[phase_name] = info["median"]
            zero_rates[phase_name] = info["zero_rate"]
            out["phase_medians"][phase_name] = info["median"]
            out["phase_zero_rates"][phase_name] = info["zero_rate"]

    pairs = [
        ("unmedicated", "buildup"),
        ("unmedicated", "consolidation"),
        ("consolidation", "afbouw"),
        ("unmedicated", "afbouw"),
    ]
    for a, b in pairs:
        if a in medians and b in medians:
            out["phase_to_phase_shifts"][f"{b}_minus_{a}_median"] = (
                medians[b] - medians[a]
            )
            out["phase_to_phase_shifts"][f"{b}_minus_{a}_zero_rate"] = (
                zero_rates[b] - zero_rates[a]
            )

    typical_within = {
        p: cital[p].get("mad_unscaled") for p in medians if "mad_unscaled" in cital[p]
    }
    out["within_phase_mad"] = typical_within

    # Conceptual link to the raw-stress dose response (NOT a per-count slope)
    out["citalopram_conceptual_link"] = {
        "primitive_is_dose_naive": True,
        "downstream_consumer_applies": (
            "methodology/citalopram_phase_stratification.md §5.B per "
            "methodology/stress_low_motion_primitive.md §1.3"
        ),
        "upstream_raw_stress_shift_at_30mg": (
            "+12-17 stress units per citalopram_dose_response_stress_mean_sleep.md "
            "v3 §5.6 (acts on all_day_stress_avg + stress_mean_sleep). "
            "Threshold S=60 captures more minutes when the raw stress baseline "
            "shifts upward even if true sympathetic-rest-arousal is constant."
        ),
        "per_mg_slope_on_count_NOT_locked": (
            "Unlike stress_mean_sleep (+0.43/mg p=0.001 buildup post-CPAP), the "
            "per-mg slope on THIS count primitive is not a locked dose-response "
            "finding. The relationship is non-linear by construction (the count "
            "depends on the upstream raw-stress distribution's mass above S=60)."
        ),
    }
    return out


# ---------------------------------------------------------------------------
# Q3.x.e Near-identity check (sibling ladder + respiration + continuous cousins)
# ---------------------------------------------------------------------------


def q_e_near_identity(df: pd.DataFrame, channel: str) -> dict:
    """Near-identity check vs sibling-ladder + companions + cousins (Q3.x.e).

    Count-primitive adaptation: the 8 sibling sensitivity-ladder
    columns are highly correlated by construction (same data with
    different thresholds); the diagnostic value is whether the primary
    S60_Mlow is degenerate with a particular neighbour or carries
    independent signal. Reports the 8 siblings + 2 respiration
    companions + 6 continuous cousins separately.
    """
    sections = {
        "sibling_sensitivity_ladder": SIBLING_COLUMNS,
        "respiration_companions": RESP_COMPANIONS,
        "continuous_cousins": CONTINUOUS_COUSINS,
    }
    out = {"threshold": NEAR_IDENTITY_THRESHOLD, "sections": {}, "flagged_pairs": []}
    flagged: list[str] = []

    for section_name, cols in sections.items():
        rows = []
        for t in cols:
            if t not in df.columns:
                rows.append({"channel": t, "note": "column absent"})
                continue
            sub = df[[channel, t]].dropna()
            if len(sub) < 30:
                rows.append({"channel": t, "n": int(len(sub)),
                             "note": "n<30 -- skipped"})
                continue
            pear = float(sub[channel].corr(sub[t]))
            spear = float(sub[channel].corr(sub[t], method="spearman"))
            is_flagged = max(abs(pear), abs(spear)) >= NEAR_IDENTITY_THRESHOLD
            rows.append({
                "channel": t,
                "n": int(len(sub)),
                "pearson_r": pear,
                "spearman_rho": spear,
                "near_identity_flag": is_flagged,
            })
            if is_flagged:
                flagged.append(t)
        out["sections"][section_name] = rows

    out["flagged_pairs"] = flagged
    out["note"] = (
        "Sibling sensitivity-ladder peers are highly correlated by construction "
        "(same per-minute base with different (S, M) thresholds per "
        "stress_low_motion_primitive.md §4); the diagnostic value is whether "
        "the primary S60_Mlow carries information beyond a neighbour. "
        "Cross-channel-correlation card "
        "(analyses/garmin_exploration/cards/cross-channel-correlation.md) "
        "already recorded H02b ≡ H02d (rho=+1.000) + HA10 ≡ -HA07c (rho=-0.922) "
        "on Stratum 4."
    )
    return out


# ---------------------------------------------------------------------------
# Q3.x.f Crash-vs-normal: Cohen's d + median diff + Mann-Whitney U robustness
# ---------------------------------------------------------------------------


def _mann_whitney_u(x: np.ndarray, y: np.ndarray) -> dict:
    """Compute Mann-Whitney U statistic + asymptotic z + p (two-sided).

    Vendored implementation (avoids hard scipy dependency at module
    import time; matches scipy.stats.mannwhitneyu within rounding).
    """
    nx = len(x)
    ny = len(y)
    combined = np.concatenate([x, y])
    ranks = pd.Series(combined).rank(method="average").to_numpy()
    rank_x_sum = float(ranks[:nx].sum())
    U_x = rank_x_sum - nx * (nx + 1) / 2.0
    U_y = nx * ny - U_x
    U = min(U_x, U_y)
    # Asymptotic two-sided p via normal approximation with tie correction
    mean_U = nx * ny / 2.0
    # tie correction
    counts = pd.Series(combined).value_counts().to_numpy()
    tie_term = float(((counts ** 3 - counts).sum()) / ((nx + ny) * (nx + ny - 1)))
    var_U = (nx * ny / 12.0) * ((nx + ny + 1) - tie_term)
    if var_U <= 0:
        return {"U": float(U), "z": float("nan"), "p_two_sided": float("nan")}
    z = (U_x - mean_U) / np.sqrt(var_U)
    # two-sided p
    from math import erf, sqrt
    p = 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))
    # Common-language effect size (probability of superiority)
    p_superiority = U_x / (nx * ny)
    return {
        "U_x": float(U_x),
        "U_y": float(U_y),
        "U_min": float(U),
        "z": float(z),
        "p_two_sided_normal_approx": float(p),
        "probability_of_superiority_x_over_y": float(p_superiority),
    }


def q_f_crash_vs_normal(df: pd.DataFrame, channel: str, seed: int = 20260622) -> dict:
    """Crash-vs-normal on Stratum 4 + count-primitive robustness (Q3.x.f).

    Count-primitive adaptation: report Cohen's d alongside median
    difference + Mann-Whitney U probability-of-superiority (Cohen's d
    on count data with right-skew can mislead; the rank-based test is
    the robust read).
    """
    sub = df[[channel, "is_crash", "episode_id"]].dropna(subset=[channel, "is_crash"])
    is_crash = sub["is_crash"].astype(bool)
    crash_vals = sub.loc[is_crash, channel].astype(float)
    normal_vals = sub.loc[~is_crash, channel].astype(float)

    n_crash_day = int(len(crash_vals))
    n_normal_day = int(len(normal_vals))
    mean_diff_day = float(crash_vals.mean() - normal_vals.mean())
    median_diff_day = float(crash_vals.median() - normal_vals.median())
    pooled_sd = float(
        np.sqrt(((len(crash_vals) - 1) * crash_vals.var(ddof=1)
                 + (len(normal_vals) - 1) * normal_vals.var(ddof=1))
                / (len(crash_vals) + len(normal_vals) - 2))
    )
    cohens_d_day = mean_diff_day / pooled_sd if pooled_sd > 0 else float("nan")

    mw = _mann_whitney_u(crash_vals.to_numpy(), normal_vals.to_numpy())

    # Episode-level (per CONVENTIONS §3.6 prefer episode count for per-event stats)
    ep_mask = (sub["episode_id"].notna()
               & sub["episode_id"].astype(str).str.startswith("crash-"))
    ep_df = sub.loc[ep_mask, [channel, "episode_id"]].copy()
    per_episode_mean = ep_df.groupby("episode_id")[channel].mean()
    n_episodes = int(len(per_episode_mean))
    normal_base_vals = normal_vals.copy()
    n_normal_base = int(len(normal_base_vals))

    if n_episodes >= 2:
        ep_mean = float(per_episode_mean.mean())
        ep_median = float(per_episode_mean.median())
        ep_sd = float(per_episode_mean.std(ddof=1))
        base_mean = float(normal_base_vals.mean())
        base_sd = float(normal_base_vals.std(ddof=1))
        ep_diff = ep_mean - base_mean
        ep_median_diff = ep_median - float(normal_base_vals.median())
        pooled_ep_sd = float(
            np.sqrt(((n_episodes - 1) * ep_sd ** 2
                     + (n_normal_base - 1) * base_sd ** 2)
                    / (n_episodes + n_normal_base - 2))
        )
        cohens_d_ep = ep_diff / pooled_ep_sd if pooled_ep_sd > 0 else float("nan")
        rng = np.random.default_rng(seed)
        ep_arr = per_episode_mean.to_numpy()
        base_arr = normal_base_vals.to_numpy()
        boot_diffs = np.empty(5000)
        for i in range(5000):
            b_ep = rng.choice(ep_arr, size=n_episodes, replace=True)
            b_base = rng.choice(base_arr, size=n_normal_base, replace=True)
            boot_diffs[i] = b_ep.mean() - b_base.mean()
        ci_low = float(np.quantile(boot_diffs, 0.025))
        ci_high = float(np.quantile(boot_diffs, 0.975))
    else:
        ep_mean = float("nan")
        ep_diff = float("nan")
        ep_median_diff = float("nan")
        cohens_d_ep = float("nan")
        ci_low = float("nan")
        ci_high = float("nan")

    # Day-level stationary bootstrap CI on mean diff at E[L]=7 AND
    # data-driven E[L]* (rounded from Q3.x.b).
    aligned = df[["date", channel, "is_crash"]].dropna(
        subset=[channel, "is_crash"]).copy()
    aligned = aligned.sort_values("date").reset_index(drop=True)

    def day_mean_diff(sub_df):
        c = sub_df["is_crash"].astype(bool)
        if c.sum() < 1 or (~c).sum() < 1:
            return float("nan")
        return float(sub_df.loc[c, channel].mean() - sub_df.loc[~c, channel].mean())

    # Use the empirical E[L]* rounded up for the second CI row (will be
    # populated when q_b_autocorrelation runs ahead).
    arr_for_el = df[channel].dropna().to_numpy()
    el_star = compute_data_driven_block_length(
        arr_for_el, default_block_length=7)["optimal_block_length"]
    el_star_rounded = max(2, int(round(el_star)))

    boot_day_E7 = stationary_bootstrap_ci(
        aligned, day_mean_diff,
        n_bootstrap=5000, expected_block_length=7,
        confidence_level=0.95, random_state=seed,
    )
    boot_day_E_star = stationary_bootstrap_ci(
        aligned, day_mean_diff,
        n_bootstrap=5000, expected_block_length=el_star_rounded,
        confidence_level=0.95, random_state=seed,
    )

    # Crash-drop sensitivity on same-day Spearman channel vs gevoelscore
    crash_drop_info = None
    if "gevoelscore" in df.columns:
        d2 = df[[channel, "gevoelscore", "is_crash"]].dropna()
        d2["is_crash"] = d2["is_crash"].astype(bool)
        if d2["is_crash"].sum() > 1 and (~d2["is_crash"]).sum() > 1:
            def spearman_stat(d):
                return float(d[channel].corr(d["gevoelscore"], method="spearman"))
            crash_drop_info = crash_drop_sensitivity(spearman_stat, d2)

    return {
        "day_level": {
            "n_crash_day": n_crash_day,
            "n_normal_day": n_normal_day,
            "mean_crash": float(crash_vals.mean()),
            "mean_normal": float(normal_vals.mean()),
            "median_crash": float(crash_vals.median()),
            "median_normal": float(normal_vals.median()),
            "mean_diff": mean_diff_day,
            "median_diff": median_diff_day,
            "cohens_d": cohens_d_day,
            "mann_whitney_u": mw,
            "stationary_bootstrap_E_L7": {
                "point_estimate": float(boot_day_E7["point_estimate"]),
                "ci_lower": float(boot_day_E7["ci_lower"]),
                "ci_upper": float(boot_day_E7["ci_upper"]),
                "note": (
                    "project default per permutation_null_block_length.md"
                ),
            },
            "stationary_bootstrap_E_L_star": {
                "expected_block_length": el_star_rounded,
                "point_estimate": float(boot_day_E_star["point_estimate"]),
                "ci_lower": float(boot_day_E_star["ci_lower"]),
                "ci_upper": float(boot_day_E_star["ci_upper"]),
                "note": (
                    f"data-driven E[L]*={el_star:.2f} rounded to "
                    f"{el_star_rounded}; closes the factor-of-2 audit gate"
                ),
            },
            "note": (
                "consecutive within-episode days are autocorrelated; treat as "
                "autocorrelation-inflated supplementary read"
            ),
        },
        "episode_level": {
            "n_crash_episodes": n_episodes,
            "n_normal_day_base_rate": n_normal_base,
            "mean_per_episode_count": ep_mean,
            "median_per_episode_count": (
                float(per_episode_mean.median())
                if n_episodes >= 2 else float("nan")
            ),
            "mean_normal_day_count": (
                float(normal_base_vals.mean()) if n_normal_base else float("nan")
            ),
            "median_normal_day_count": (
                float(normal_base_vals.median()) if n_normal_base else float("nan")
            ),
            "mean_diff_episode_vs_normal_day": ep_diff,
            "median_diff_episode_vs_normal_day": ep_median_diff,
            "cohens_d_episode_vs_normal_day": cohens_d_ep,
            "bootstrap_ci95_mean_diff": [ci_low, ci_high],
            "n_bootstrap": 5000,
            "seed": seed,
        },
        "crash_drop_sensitivity_on_spearman_vs_gevoelscore": (
            None if crash_drop_info is None else {
                "full_frame_value": crash_drop_info["full_frame_value"],
                "crash_dropped_value": crash_drop_info["crash_dropped_value"],
                "abs_delta": crash_drop_info["abs_delta"],
                "exceeds_threshold_0p10": crash_drop_info["exceeds_threshold"],
                "n_full": crash_drop_info["n_full"],
                "n_crash_dropped": crash_drop_info["n_crash_dropped"],
                "n_crash": crash_drop_info["n_crash"],
            }
        ),
    }


# ---------------------------------------------------------------------------
# Q3.x.g Spike-detecting primitive availability — channel IS the spike primitive
# ---------------------------------------------------------------------------


def q_g_spike_primitive(df: pd.DataFrame, channel: str) -> dict:
    """Q3.x.g: this channel IS the spike primitive by construction.

    Per CONVENTIONS §3.5 + stress_low_motion_primitive.md §7.4 audit
    hook on §3.5: the channel is a per-minute threshold-crossing
    aggregated to a per-day count. The corresponding continuous
    daily-aggregate cousin is all_day_stress_avg. Document the
    sensitivity-ladder coverage + relate to the continuous form.
    """
    out = {
        "channel_resolution": (
            "per-day integer count of minutes where stress(t) >= 60 AND "
            "intensity(t) <= 1; per-minute threshold-crossing aggregated to "
            "per-day count per stress_low_motion_primitive.md §2"
        ),
        "channel_IS_the_spike_primitive": True,
        "spike_primitive_basis": (
            "CONVENTIONS §3.5 acute-load discipline + "
            "stress_low_motion_primitive.md §7.4 audit hook"
        ),
        "continuous_daily_aggregate_cousin": "all_day_stress_avg",
        "sensitivity_ladder_columns_in_master": [],
        "respiration_companions": [],
    }
    # Sensitivity-ladder coverage in master
    ladder = [
        "stress_low_motion_min_count_S50_Mstrict",
        "stress_low_motion_min_count_S50_Mlow",
        "stress_low_motion_min_count_S50_Mbelow_mod",
        "stress_low_motion_min_count_S60_Mstrict",
        "stress_low_motion_min_count_S60_Mlow",
        "stress_low_motion_min_count_S60_Mbelow_mod",
        "stress_low_motion_min_count_S75_Mstrict",
        "stress_low_motion_min_count_S75_Mlow",
        "stress_low_motion_min_count_S75_Mbelow_mod",
    ]
    for c in ladder:
        if c in df.columns:
            n = int(df[c].notna().sum())
            v = df[c].dropna().astype(float)
            out["sensitivity_ladder_columns_in_master"].append({
                "column": c,
                "n_non_nan": n,
                "median": float(v.median()) if n else None,
                "p90": float(np.percentile(v, 90)) if n else None,
                "is_primary": c == channel,
            })
    # Respiration companions
    for c in RESP_COMPANIONS:
        if c in df.columns:
            n = int(df[c].notna().sum())
            v = df[c].dropna().astype(float)
            out["respiration_companions"].append({
                "column": c,
                "n_non_nan": n,
                "median": float(v.median()) if n else None,
            })

    # Continuous-cousin relation: pair primary count vs all_day_stress_avg
    if "all_day_stress_avg" in df.columns:
        d = df[[channel, "all_day_stress_avg"]].dropna()
        if len(d) > 30:
            out["pair_vs_all_day_stress_avg"] = {
                "n": int(len(d)),
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "interpretation_note": (
                    "Continuous daily mean vs spike-count of same underlying "
                    "minute-level stress channel. Strong positive correlation "
                    "is expected by construction (when the day's stress mean "
                    "rises, more minutes cross any fixed threshold)."
                ),
            }

    # Monotonicity check: at fixed motion class, count(S=50) >= count(S=60) >= count(S=75)
    out["monotonicity_check"] = {}
    for motion in ("Mstrict", "Mlow", "Mbelow_mod"):
        c50 = f"stress_low_motion_min_count_S50_{motion}"
        c60 = f"stress_low_motion_min_count_S60_{motion}"
        c75 = f"stress_low_motion_min_count_S75_{motion}"
        if all(c in df.columns for c in (c50, c60, c75)):
            d = df[[c50, c60, c75]].dropna()
            n = len(d)
            viol_60_50 = int((d[c60] > d[c50]).sum())
            viol_75_60 = int((d[c75] > d[c60]).sum())
            out["monotonicity_check"][motion] = {
                "n_days": int(n),
                "violations_count_S60_gt_S50": viol_60_50,
                "violations_count_S75_gt_S60": viol_75_60,
                "monotonic_ok": bool(viol_60_50 == 0 and viol_75_60 == 0),
            }

    out["note"] = (
        "Per CONVENTIONS §3.5, sympathetic-arousal proxies prefer spike / "
        "peak / count metrics over daily means. The channel IS the spike "
        "primitive: it is the per-minute threshold-crossing aggregated to a "
        "per-day count. The 9-column sensitivity ladder (3 stress thresholds x "
        "3 motion classes) covers the threshold-sensitivity dimension; the 2 "
        "respiration companion columns (n_minutes_resp_above_18 + "
        "n_minutes_resp_in_rest_band_10_18) cover the hidden-motion / "
        "sympathetic-arousal disambiguation per stress_low_motion_primitive.md "
        "§4b. The continuous-form cousin is all_day_stress_avg (CONFIRMED-"
        "citalopram +0.57/mg per dose-response MD v3); a future test that "
        "wants the dilution-vulnerable daily-mean reading uses that channel, "
        "and a future test that wants the acute-load spike-count reading "
        "uses this one."
    )
    return out


# ---------------------------------------------------------------------------
# Q3.x.h Outliers + calibration-drift; flag missing audit-MD row
# ---------------------------------------------------------------------------


def q_h_outliers_calibration(df: pd.DataFrame, channel: str) -> dict:
    """Outliers + calibration-drift (Q3.x.h).

    Count-primitive: MAD-based |z|>5 on the count value; the day-validity
    gate (>=600 in-range stress samples per stress_low_motion_primitive.md
    §5) already excludes off-wrist days at the upstream extraction layer.
    Flags the missing audit-MD row for this primitive.
    """
    sub = df[["date", channel]].dropna().sort_values("date").reset_index(drop=True)
    v = sub[channel].astype(float)
    med = float(v.median())
    mad = float(np.median(np.abs(v - med)))
    spread = mad * 1.4826 if mad > 0 else float("nan")
    z = (v - med) / spread if spread and spread == spread else pd.Series([], dtype=float)
    flagged_mask = z.abs() > 5
    flagged = sub.loc[flagged_mask].copy()
    flagged["mad_z"] = z[flagged_mask]
    outliers = [
        {"date": str(r["date"].date()), "value": float(r[channel]),
         "mad_z": float(r["mad_z"])}
        for _, r in flagged.iterrows()
    ]
    sub["rolling_med_90d"] = v.rolling(window=90, min_periods=45).median()
    snapshot_dates = [
        "2022-12-01", "2023-06-01", "2023-12-01",
        "2024-06-01", "2025-01-01", "2025-12-01",
    ]
    snaps = []
    for s in snapshot_dates:
        t = pd.Timestamp(s)
        idx = (sub["date"] - t).abs().idxmin()
        row = sub.loc[idx]
        snaps.append({
            "snapshot_date": s,
            "actual_date": str(row["date"].date()),
            "rolling_med_90d": (
                None if pd.isna(row["rolling_med_90d"])
                else float(row["rolling_med_90d"])
            ),
        })
    # Consolidation boundary step (per stress_mean_sleep precedent)
    step_date = pd.Timestamp("2024-06-20")
    pre30 = sub.loc[(sub["date"] >= step_date - pd.Timedelta(days=30))
                    & (sub["date"] < step_date), channel].mean()
    post30 = sub.loc[(sub["date"] >= step_date)
                     & (sub["date"] < step_date + pd.Timedelta(days=30)), channel].mean()

    return {
        "outlier_rule": "MAD-based |z|>5 (z = (x - median) / (MAD * 1.4826))",
        "median": med,
        "mad_unscaled": mad,
        "n_flagged": int(len(outliers)),
        "outliers": outliers,
        "rolling_90d_median_snapshots": snaps,
        "consolidation_boundary_2024_06_20_step": {
            "pre_30d_mean": float(pre30) if pre30 == pre30 else None,
            "post_30d_mean": float(post30) if post30 == post30 else None,
            "diff_post_minus_pre": (
                float(post30 - pre30) if (pre30 == pre30 and post30 == post30) else None
            ),
        },
        "garmin_indicators_audit_md_gap": {
            "audit_md_path": "docs/research/methodology/garmin_indicators_audit.md",
            "missing_row_for_this_primitive": True,
            "proposed_row_content": (
                "Channel family: stress_low_motion_min_count_S<S>_M<M> "
                "(9 columns per stress_low_motion_primitive.md §4 + 2 "
                "respiration companions per §4b). "
                "Upstream extractor: pipeline/01_extract/stress_low_motion_extract.py. "
                "Source FIT: monitoring_b classified files per HA11 precedent. "
                "Day-validity gate: >=600 in-range stress samples (values in [1,100]) "
                "per stress_low_motion_primitive.md §5; days below gate get count=0 "
                "+ _valid_flag=0. Sentinel handling: too_active + off_wrist values "
                "outside [1,100] not counted; both contribute to day's in-range "
                "sample count being below the 600 gate if numerous. Calibration: "
                "no documented drift events for this primitive (added "
                f"{date.today().isoformat()} per this descriptive analysis). "
                "Device: Forerunner 245 Elevate V3 throughout 2021-08-16 -> present "
                "(no device change)."
            ),
            "action": (
                "PROPOSE-ONLY (do not edit garmin_indicators_audit.md as part "
                "of this analysis per handoff §6 + §5.5 discipline). Surface "
                "for user authorisation."
            ),
        },
        "known_issues_summary": [
            "Day-validity gate >=600 in-range stress samples per stress_low_motion_primitive.md §5",
            "Days below gate set to count=0 + valid_flag=0 (not NaN) per same §5",
            "Days with no monitoring_b FIT file at all: all 9 columns NaN + valid_flag NaN (device-off)",
            "Sentinels (too_active / off_wrist values outside [1,100]) not counted",
            "Single FR245 device throughout 2021-08-16 to present -- no device change confound per project_garmin_research_bias_boundary",
            "Respiration companions exclude values outside [5, 40] breaths/min as off-wrist / sensor-error per stress_low_motion_primitive.md §4b",
            "Respiration thresholds (10, 18) are general adult-rest physiology, NOT calibrated to participant's personal baseline per §3.3b",
        ],
    }


# ---------------------------------------------------------------------------
# Q3.x.i Covariate-sensitivity readiness
# ---------------------------------------------------------------------------


def q_i_covariate_readiness(df: pd.DataFrame, channel: str) -> dict:
    """Covariate-sensitivity readiness (Q3.x.i).

    For a future HA pre-reg using this channel as predictor of a
    crash-related outcome. Count-primitive adaptation: continuous and
    count-form covariates each have their use; HA-P7 §4.5.4
    secondary-with-covariate pattern carries.
    """
    cands = []

    # 1. all_day_stress_avg — continuous-form cousin; "general stress level" control
    all_day_corr = None
    if "all_day_stress_avg" in df.columns:
        d = df[[channel, "all_day_stress_avg"]].dropna()
        if len(d) > 30:
            all_day_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "all_day_stress_avg",
        "rationale": (
            "Continuous-form daily aggregate of the same upstream stress "
            "channel; controls for 'general stress level' so the spike-count "
            "predictor's signal is isolated to the spike-during-rest "
            "construct rather than overall stress. CONFIRMED-citalopram "
            "+0.57/mg per dose-response MD v3 -- the dose-modulation "
            "confound is shared between predictor + covariate."
        ),
        "source": (
            "methodology/citalopram_dose_response_stress_mean_sleep.md v3 §5.6"
        ),
        "observed_correlation_on_S4": all_day_corr,
        "expected_effect": (
            "beta_channel attenuates if the signal is just 'today was a "
            "higher-stress day overall'; beta_channel survives if the "
            "spike-during-rest count carries information beyond mean stress"
        ),
    })

    # 2. n_minutes_resp_above_18 — respiration companion; hidden-motion check
    resp_corr = None
    if "n_minutes_resp_above_18" in df.columns:
        d = df[[channel, "n_minutes_resp_above_18"]].dropna()
        if len(d) > 30:
            resp_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "n_minutes_resp_above_18",
        "rationale": (
            "Respiration-elevated minute count; per "
            "stress_low_motion_primitive.md §3.3b a high-stress-low-motion "
            "minute that is ALSO in n_minutes_resp_above_18 is either "
            "hidden motion the intensity proxy missed OR genuine "
            "sympathetic arousal with breathing change. The covariate "
            "disambiguates the hidden-motion vs sympathetic-arousal "
            "readings of the predictor."
        ),
        "source": "methodology/stress_low_motion_primitive.md §3.3b + §4b",
        "observed_correlation_on_S4": resp_corr,
        "expected_effect": (
            "beta_channel attenuates if respiration is doing the predictive "
            "work (signal is generic sympathetic arousal); beta_channel "
            "survives if the stress-at-rest construct is the discriminator"
        ),
    })

    # 3. resting_hr or min_hr — autonomic-tone baseline control
    rhr_corr = None
    if "resting_hr" in df.columns:
        d = df[[channel, "resting_hr"]].dropna()
        if len(d) > 30:
            rhr_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "resting_hr",
        "rationale": (
            "Alternative autonomic-tone anchor (continuous). Controls for "
            "baseline sympathetic-parasympathetic balance; the predictor's "
            "spike-during-rest signal can then be disambiguated from "
            "underlying chronic autonomic-load."
        ),
        "source": (
            "HRV proxy validation Check 7.2 + cross-channel-correlation card"
        ),
        "observed_correlation_on_S4": rhr_corr,
        "expected_effect": (
            "beta_channel attenuates if the signal is shared autonomic-tone; "
            "beta_channel survives if the acute-spike-at-rest construct is "
            "distinct from chronic tone"
        ),
    })

    # 4. own-lagged 14d mean — autocorrelation-vs-mechanism (HA-P7 §4.5.4)
    cands.append({
        "covariate": f"{channel}_lagged_mean_14d(d) = mean(channel[d-14:d-1])",
        "rationale": (
            "Mirrors HA-P7 §4.5.4 (lagged outcome covariate) for the "
            "autocorrelation-vs-mechanism disambiguation. Computed past the "
            "cutoff lag M reported in Q3.x.b; the 14d window is the "
            "conservative pick for a count primitive (the autocorrelation "
            "behaviour may differ from continuous channels)."
        ),
        "source": "HA-P7 hypothesis.md §4.5.4 worked example",
        "expected_effect": (
            "beta_channel collapses if today's spike-count is just "
            "yesterday's count carried forward; beta_channel survives if "
            "the signal carries new-day information"
        ),
    })

    return {
        "primary_use_case": (
            "Future HA pre-reg using stress_low_motion_min_count_S60_Mlow "
            "as predictor of a crash-related outcome (e.g. HA-C4b vNext, "
            "or any HA test reusing the lived-experience 'stress at rest' "
            "construct from garmin_pacing_practice.md §3.3)."
        ),
        "discipline_anchor": (
            "HA-P7 hypothesis.md §4.5.4 -- secondary-logistic-with-covariate "
            "pattern"
        ),
        "candidate_covariates": cands,
        "recommendation": (
            "Pre-spec all four covariates as secondary sensitivity arms. "
            "Concordance across the four secondaries = high confidence in "
            "the primary; divergence = the disambiguation is doing real "
            "work. The all_day_stress_avg covariate is the obligatory "
            "spike-vs-mean disambiguator; the respiration companion is the "
            "obligatory hidden-motion disambiguator; the resting_hr arm is "
            "diagnostic; the 14d-lagged arm is the autocorrelation-vs-"
            "mechanism diagnostic per HA-P7."
        ),
        "count_primitive_note": (
            "For Poisson-or-negative-binomial-natural count outcomes the "
            "covariates above can be used as predictors in a Poisson / NB "
            "GLM where the predictor is also a count (cardinality matching). "
            "Whether to model as Poisson, NB, or log-linear OLS depends on "
            "the consumer test's specific question and the day-level "
            "dispersion (variance / mean ratio) reported in Q3.x.a."
        ),
    }


# ---------------------------------------------------------------------------
# Plot generation
# ---------------------------------------------------------------------------


def make_plots(df: pd.DataFrame, channel: str, out_dir: Path) -> list[str]:
    """Generate the figures referenced from findings.md."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    sub = df[["date", channel, "is_crash"]].dropna(subset=[channel])

    # Figure 1: Histogram with zero-rate annotation
    fig, ax = plt.subplots(figsize=(8, 4.2))
    vals = sub[channel].astype(float)
    ax.hist(vals, bins=50, color="#5b88c4", edgecolor="white", alpha=0.85)
    med = float(vals.median())
    p25, p75 = np.percentile(vals, 25), np.percentile(vals, 75)
    p90, p99 = np.percentile(vals, 90), np.percentile(vals, 99)
    ax.axvline(med, color="#222", linestyle="-", linewidth=1.5,
               label=f"median={med:.1f}")
    ax.axvline(p25, color="#222", linestyle="--", linewidth=1.0,
               label=f"p25={p25:.1f}")
    ax.axvline(p75, color="#222", linestyle="--", linewidth=1.0,
               label=f"p75={p75:.1f}")
    ax.axvline(p90, color="#a85b5b", linestyle=":", linewidth=1.0,
               label=f"p90={p90:.1f}")
    ax.axvline(p99, color="#cc4949", linestyle=":", linewidth=1.0,
               label=f"p99={p99:.1f}")
    n_zero = int((vals == 0).sum())
    ax.set_xlabel(f"{channel} (minutes/day)")
    ax.set_ylabel("days (Stratum 4)")
    ax.set_title(
        f"{channel} distribution -- Stratum 4, n={int(vals.notna().sum())}, "
        f"zero-days={n_zero}"
    )
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fp = out_dir / "fig1_distribution_s4.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 2: Phase-stratified violins (citalopram axis)
    phase_data = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (sub["date"] >= pd.Timestamp(start)) & (sub["date"] <= pd.Timestamp(end))
        phase_data[phase_name] = sub.loc[mask, channel].dropna().astype(float).to_numpy()
    fig, ax = plt.subplots(figsize=(9, 4.2))
    labels = [p for p in ("unmedicated", "buildup", "consolidation", "afbouw")
              if len(phase_data[p]) >= 5]
    parts = ax.violinplot(
        [phase_data[p] for p in labels],
        showmedians=True, widths=0.85,
    )
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_ylabel(f"{channel} (minutes/day)")
    ax.set_title("Phase-stratified distribution (Stratum 4, 4-phase citalopram axis)")
    fig.tight_layout()
    fp = out_dir / "fig2_phase_stratified_citalopram.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 2b: Phase-stratified violins (recovery axis, 6-phase)
    if "recovery_phase" in df.columns:
        rec_order = [
            "pre_illness_healthy", "acute_infection", "lc_pre_ergo",
            "pacing_pre_citalopram_learning", "pacing_habit_established",
            "citalopram_modulated",
        ]
        rec_data = {}
        for p in rec_order:
            vals_p = df.loc[df["recovery_phase"] == p, channel].dropna().astype(float)
            if len(vals_p) >= 5:
                rec_data[p] = vals_p.to_numpy()
        if rec_data:
            fig, ax = plt.subplots(figsize=(10, 4.4))
            labels = list(rec_data.keys())
            ax.violinplot([rec_data[p] for p in labels],
                          showmedians=True, widths=0.85)
            ax.set_xticks(np.arange(1, len(labels) + 1))
            ax.set_xticklabels(labels, rotation=20, ha="right", fontsize=8)
            ax.set_ylabel(f"{channel} (minutes/day)")
            ax.set_title(
                "Phase-stratified distribution -- 6-phase recovery axis "
                "(LOCKED 2026-06-19 d47e0d3)"
            )
            fig.tight_layout()
            fp = out_dir / "fig2b_phase_stratified_recovery_axis.png"
            fig.savefig(fp, dpi=110)
            plt.close(fig)
            written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 3: Time series with rolling 90d median + phase shading
    sub_sorted = sub.sort_values("date").reset_index(drop=True)
    sub_sorted["roll90"] = sub_sorted[channel].rolling(90, min_periods=45).median()
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.plot(sub_sorted["date"], sub_sorted[channel],
            color="#aac4e3", linewidth=0.6, alpha=0.6, label="daily")
    ax.plot(sub_sorted["date"], sub_sorted["roll90"],
            color="#1f3a5f", linewidth=1.8, label="rolling 90d median")
    phase_colors = {
        "unmedicated": "#ffffff",
        "buildup": "#fde0a3",
        "consolidation": "#ffd680",
        "afbouw": "#fdbf6f",
    }
    for phase_name, start, end in PHASE_BOUNDARIES:
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end),
                   color=phase_colors[phase_name], alpha=0.18, label=phase_name)
    h, labels_legend = ax.get_legend_handles_labels()
    seen = set()
    pairs = [(hi, li) for hi, li in zip(h, labels_legend)
             if not (li in seen or seen.add(li))]
    ax.legend([p[0] for p in pairs], [p[1] for p in pairs],
              loc="upper right", fontsize=8, ncol=2)
    ax.set_ylabel(f"{channel} (minutes/day)")
    ax.set_title(f"{channel} -- rolling 90d median + citalopram phases")
    fig.tight_layout()
    fp = out_dir / "fig3_trajectory_with_phases.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 4: Crash vs normal density
    df_ep = sub.copy()
    df_ep["is_crash"] = df_ep["is_crash"].astype(bool)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    normal = df_ep.loc[~df_ep["is_crash"], channel]
    crash = df_ep.loc[df_ep["is_crash"], channel]
    bins = np.linspace(0, max(normal.max(), crash.max()) + 1, 50)
    ax.hist(normal, bins=bins, color="#9dc1e0", alpha=0.7,
            label=f"normal days n={len(normal)}", density=True)
    ax.hist(crash, bins=bins, color="#cc4949", alpha=0.55,
            label=f"crash days n={len(crash)}", density=True)
    ax.axvline(normal.median(), color="#264c75", linestyle="--",
               label=f"normal median={normal.median():.0f}")
    ax.axvline(crash.median(), color="#7a1f1f", linestyle="--",
               label=f"crash median={crash.median():.0f}")
    ax.set_xlabel(f"{channel} (minutes/day)")
    ax.set_ylabel("density")
    ax.set_title("Crash-day vs normal-day distribution (Stratum 4)")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fp = out_dir / "fig4_crash_vs_normal.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 5: ACF
    arr = sub[channel].dropna().to_numpy()
    acf_res = compute_data_driven_block_length(arr, default_block_length=7)
    acf = acf_res["autocorrelations"]
    fig, ax = plt.subplots(figsize=(8, 3.6))
    lags = np.arange(len(acf))
    ax.bar(lags, acf, width=0.7, color="#5b88c4", edgecolor="white")
    ax.axhline(0, color="#222", linewidth=0.5)
    threshold = 2.0 * np.sqrt(np.log(len(arr)) / len(arr))
    ax.axhline(threshold, color="#cc4949", linestyle="--", linewidth=0.8,
               label=f"|rho|={threshold:.3f} (Politis-White 2-sigma)")
    ax.axhline(-threshold, color="#cc4949", linestyle="--", linewidth=0.8)
    ax.set_xlabel("lag (days)")
    ax.set_ylabel("autocorrelation")
    ax.set_title(
        f"ACF -- {channel} (Stratum 4); "
        f"E[L]*={acf_res['optimal_block_length']:.1f}, M={acf_res['cutoff_lag']}"
    )
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fp = out_dir / "fig5_acf.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 6: Sibling sensitivity-ladder correlation heat
    ladder_all = SIBLING_COLUMNS + [channel]
    avail = [c for c in ladder_all if c in df.columns]
    if len(avail) >= 4:
        d = df[avail].dropna()
        if len(d) > 30:
            corr = d.corr(method="spearman")
            fig, ax = plt.subplots(figsize=(8.5, 7))
            im = ax.imshow(corr.values, vmin=0, vmax=1, cmap="viridis")
            ax.set_xticks(range(len(avail)))
            ax.set_yticks(range(len(avail)))
            short = [c.replace("stress_low_motion_min_count_", "") for c in avail]
            ax.set_xticklabels(short, rotation=45, ha="right", fontsize=8)
            ax.set_yticklabels(short, fontsize=8)
            for i in range(len(avail)):
                for j in range(len(avail)):
                    ax.text(j, i, f"{corr.values[i, j]:.2f}",
                            ha="center", va="center", fontsize=7,
                            color="white" if corr.values[i, j] < 0.5 else "black")
            cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            cbar.set_label("Spearman rho")
            ax.set_title("Sensitivity-ladder Spearman correlations (Stratum 4)")
            fig.tight_layout()
            fp = out_dir / "fig6_sibling_ladder_corr.png"
            fig.savefig(fp, dpi=110)
            plt.close(fig)
            written.append(str(fp.relative_to(out_dir.parent)))

    return written


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main() -> None:
    if not os.environ.get("GEVOELSCORE_DATA_PATH"):
        os.environ["GEVOELSCORE_DATA_PATH"] = (
            "C:/Users/Gebruiker/Documents/gevoelscore-data"
        )

    master = load_master(as_of_date=AS_OF_DATE)
    s4 = filter_to_stratum_4(master, as_of_date=AS_OF_DATE)
    labels = load_crash_labels(as_of_date=AS_OF_DATE)[["date", "label", "episode_id"]]
    labels = labels.rename(columns={"label": "_crash_label"})
    s4 = s4.merge(labels, on="date", how="left")
    s4["is_crash"] = (s4["_crash_label"] == "crash").astype(bool)

    if CHANNEL not in s4.columns:
        raise RuntimeError(f"{CHANNEL} not found in master -- check pipeline build")

    values = s4[CHANNEL].astype(float)

    summary = {
        "channel": CHANNEL,
        "as_of_date": AS_OF_DATE,
        "stratum_4_start": "2022-09-03",
        "n_rows_stratum_4_total": int(len(s4)),
        "n_rows_with_channel": int(values.notna().sum()),
        "labelling_scheme": "crash_v2 (labels_crash_v2.csv, label=='crash')",
        "source_file_master": "per_day_master.csv",
        "source_file_crash_labels": "labels_crash_v2.csv",
        "phase_axis_source_primary": (
            "methodology/citalopram_phase_stratification.md §3 (4-phase, parity "
            "with stress_mean_sleep first analysis)"
        ),
        "phase_axis_source_secondary": (
            "methodology/lc_recovery_phase_axis.md §2 (6-phase, LOCKED "
            "2026-06-19 d47e0d3; cross-tabulated for context)"
        ),
        "primitive_methodology": (
            "methodology/stress_low_motion_primitive.md (Session E lock "
            "2026-06-15)"
        ),
        "questions": {},
    }

    summary["questions"]["Q3.x.a_distribution"] = q_a_distribution(values)
    summary["questions"]["Q3.x.b_autocorrelation"] = q_b_autocorrelation(values)
    per_phase = q_c_base_rates_per_phase(s4, CHANNEL)
    summary["questions"]["Q3.x.c_base_rates_per_phase"] = per_phase
    summary["questions"]["Q3.x.d_phase_stratified_distribution"] = (
        q_d_phase_stratified(per_phase, CHANNEL)
    )
    summary["questions"]["Q3.x.e_near_identity"] = q_e_near_identity(s4, CHANNEL)
    summary["questions"]["Q3.x.f_crash_vs_normal"] = q_f_crash_vs_normal(s4, CHANNEL)
    summary["questions"]["Q3.x.g_spike_primitive"] = q_g_spike_primitive(s4, CHANNEL)
    summary["questions"]["Q3.x.h_outliers_calibration"] = (
        q_h_outliers_calibration(s4, CHANNEL)
    )
    summary["questions"]["Q3.x.i_covariate_readiness"] = (
        q_i_covariate_readiness(s4, CHANNEL)
    )

    plot_files = make_plots(s4, CHANNEL, HERE / "plots")
    summary["plots"] = plot_files

    out_path = HERE / "summary.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"Wrote {out_path}")
    print(f"Plots: {plot_files}")
    print("\n--- HEADLINE ---")
    a = summary["questions"]["Q3.x.a_distribution"]
    b = summary["questions"]["Q3.x.b_autocorrelation"]
    print(
        f"Q3.x.a n={a['n']} mean={a['mean']:.1f} median={a['median']:.1f} "
        f"MAD={a['mad_unscaled']:.1f} skew={a['skewness']:.2f} "
        f"zero-rate={a['zero_rate']:.3f} heavy_tail={a['heavy_tail_flag']}"
    )
    print(
        f"Q3.x.b E[L]*={b['data_driven_E_L_star']:.2f} (default 7); "
        f"factor-of-2 flag={b['factor_of_2_deviation_flag']}; "
        f"cutoff M={b['cutoff_lag_M']}"
    )
    f = summary["questions"]["Q3.x.f_crash_vs_normal"]
    fl = f["day_level"]
    e7 = fl["stationary_bootstrap_E_L7"]
    estar = fl["stationary_bootstrap_E_L_star"]
    print(
        f"Q3.x.f day-level: n_crash={fl['n_crash_day']} "
        f"n_normal={fl['n_normal_day']} d={fl['cohens_d']:.2f} "
        f"mean_diff={fl['mean_diff']:.2f} median_diff={fl['median_diff']:.2f}"
    )
    mw = fl["mann_whitney_u"]
    print(
        f"  Mann-Whitney U: z={mw['z']:.2f} p={mw['p_two_sided_normal_approx']:.4f} "
        f"P(superiority crash>normal)={mw['probability_of_superiority_x_over_y']:.3f}"
    )
    print(
        f"  E[L]=7   CI=[{e7['ci_lower']:.2f}, {e7['ci_upper']:.2f}] "
        f"width={e7['ci_upper'] - e7['ci_lower']:.2f}"
    )
    print(
        f"  E[L]={estar['expected_block_length']}  "
        f"CI=[{estar['ci_lower']:.2f}, {estar['ci_upper']:.2f}] "
        f"width={estar['ci_upper'] - estar['ci_lower']:.2f}"
    )
    fe = f["episode_level"]
    print(
        f"Q3.x.f episode-level: n_ep={fe['n_crash_episodes']} "
        f"d={fe['cohens_d_episode_vs_normal_day']:.2f} "
        f"mean_diff={fe['mean_diff_episode_vs_normal_day']:.2f} "
        f"median_diff={fe['median_diff_episode_vs_normal_day']:.2f} "
        f"CI={fe['bootstrap_ci95_mean_diff']}"
    )
    cd = f["crash_drop_sensitivity_on_spearman_vs_gevoelscore"]
    if cd is not None:
        print(
            f"Q3.x.f crash-drop on Spearman(channel, gevoelscore): "
            f"full={cd['full_frame_value']:.3f} "
            f"crash-dropped={cd['crash_dropped_value']:.3f} "
            f"|delta|={cd['abs_delta']:.3f} >0.10? {cd['exceeds_threshold_0p10']}"
        )
    e = summary["questions"]["Q3.x.e_near_identity"]
    print(f"Q3.x.e near-identity flagged: {e['flagged_pairs']}")
    h = summary["questions"]["Q3.x.h_outliers_calibration"]
    print(f"Q3.x.h outliers (|z|>5): {h['n_flagged']} flagged")


if __name__ == "__main__":
    main()
