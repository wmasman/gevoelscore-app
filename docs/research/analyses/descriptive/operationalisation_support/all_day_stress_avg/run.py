"""Descriptive analysis: all_day_stress_avg operationalisation support.

Answers Q3.2.a-i per the locked descriptive programme:
``docs/research/analyses/descriptive/README.md`` section 3.2 (the
template a-i applied to this channel) generalised from the Phase 1 first
analysis (stress_mean_sleep, +0.43/mg) and third analysis
(stress_low_motion_min_count_S60_Mlow, factor-of-3 E[L]*). This is the
second CONFIRMED-citalopram channel in the Tier 1 user-prioritised
"finish the descriptive analysis" Phase 2 sequential batch (R14
single_pool_reanchor landed at badd04a; bb_lowest next).

Channel: 24h-window mean Garmin stress score (UDS-pre-aggregated, JSON
passthrough per garmin_indicators_audit.md Wave 3 2026-06-12 propagation).
CONFIRMED dose-modulated at +0.565/mg p=0.000 buildup post-CPAP per
citalopram_dose_response_stress_mean_sleep.md section 5.6.1 — the
**largest beta** among the 3 CONFIRMED channels (sister stress_mean_sleep
+0.429; bb_lowest -1.134 inverse direction). Primary predictor in the
HA-C3 v2 REJECTED + HA-C3p PARTIAL cluster (2026-06-23) which jointly
detected an inverted-U / concave non-linearity in the stress to
gevoelscore mapping on this channel.

Continuous-channel adaptations of the Q-template (vs count-primitive
third analysis): standard Cohen's d primary, no zero-rate column,
6-channel near-identity panel includes the sister stress_mean_sleep
(documented near-identity neighbour) + bb_lowest (inverse-direction
CONFIRMED-citalopram sister).

Output: ``summary.json`` (machine-readable per-question results) +
``plots/*.png`` (visualisations). The hand-written ``findings.md`` reads
from these.

Discipline guards (per CONVENTIONS):
- section 2.1 descriptive-before-inference: no causal claims; no
  falsification bar; no HA verdict promotion (HA-C3 cluster verdicts
  cross-referenced descriptively only).
- section 3.1 personal baseline: distribution shape is reported as-is;
  phase-stratified to surface the citalopram step rather than averaging
  across phases.
- section 3.3 column-duplication: near-identity check at |rho|>=0.92.
- section 3.4 crash-drop sensitivity: |Delta|>0.10 flag surfaced.
- section 3.5 spike metrics: spike-primitive availability documented
  (Q3.2.g); all_day_stress_avg is a 24h-window daily mean, dilution-
  vulnerable per section 3.5; sister spike companions enumerated.
- section 3.6 named counts: every count reports scheme + unit + source.
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
# HERE = .../analyses/descriptive/operationalisation_support/all_day_stress_avg
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


CHANNEL = "all_day_stress_avg"
AS_OF_DATE = "2026-06-05"  # parity with stress_mean_sleep + stress_low_motion first/third analyses

# Citalopram phase boundaries per
# methodology/citalopram_phase_stratification.md section 3
PHASE_BOUNDARIES = [
    ("unmedicated", date(2022, 9, 3), date(2024, 4, 8)),
    ("buildup", date(2024, 4, 9), date(2024, 6, 19)),
    ("consolidation", date(2024, 6, 20), date(2026, 3, 19)),
    ("afbouw", date(2026, 3, 20), date(2026, 6, 5)),
    # post_afbouw begins 2026-06-06; not in as-of cut
]


def citalopram_phase(d) -> str:
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
# Q3.2.a Distribution shape
# ---------------------------------------------------------------------------


def q_a_distribution(values: pd.Series) -> dict:
    """Distribution shape on Stratum 4 (Q3.2.a).

    Reports mean, median, MAD, quantiles, skewness, kurtosis, heavy-tail
    flag. Continuous-channel template (parity with stress_mean_sleep
    Q3.1.a).
    """
    v = values.dropna().astype(float)
    n = int(len(v))
    mean = float(v.mean())
    median = float(v.median())
    std = float(v.std(ddof=1))
    mad = float(np.median(np.abs(v - median)))
    quantiles = {f"p{q}": float(np.percentile(v, q)) for q in (1, 5, 10, 25, 50, 75, 90, 95, 99)}
    centered = v - mean
    m2 = float((centered ** 2).mean())
    m3 = float((centered ** 3).mean())
    skewness = m3 / (m2 ** 1.5) if m2 > 0 else float("nan")
    heavy_tail = bool((quantiles["p99"] / median > 3.0) or skewness > 1.0)
    m4 = float((centered ** 4).mean())
    excess_kurtosis = m4 / (m2 ** 2) - 3.0 if m2 > 0 else float("nan")
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
    }


# ---------------------------------------------------------------------------
# Q3.2.b Autocorrelation + E[L]*
# ---------------------------------------------------------------------------


def q_b_autocorrelation(values: pd.Series) -> dict:
    """Autocorrelation structure + E[L]* (Q3.2.b).

    Drops NaN entries before estimating. Politis-White 2004 with
    Patton-Politis-White 2009 correction per
    methodology/permutation_null_block_length.md. Default E[L]=7;
    factor-of-2 deviation flag fires if |E[L]* - 7| / 7 > 0.5.
    """
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
        "politis_white_threshold_formula": "2 * sqrt(log(n) / n) per Politis-White 2004 + inference.py",
        "note": result.get("note", ""),
        "selected_acf_lags": lags_of_interest,
    }


# ---------------------------------------------------------------------------
# Q3.2.c Base rates per phase
# ---------------------------------------------------------------------------


def q_c_base_rates_per_phase(df: pd.DataFrame, channel: str) -> dict:
    """Per-phase n + median + dispersion (Q3.2.c)."""
    out = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))
        sub = df.loc[mask, channel].dropna().astype(float)
        if len(sub) == 0:
            out[phase_name] = {"n": 0}
            continue
        med = float(sub.median())
        out[phase_name] = {
            "n": int(len(sub)),
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
        }
    return out


def q_c_quintile_bin_distribution(df: pd.DataFrame, channel: str) -> dict:
    """HA-C3p right-shift unmedicated bin distribution reproduction
    at finer quantile resolution (Q3.2.c extension).

    Reproduces the [45, 80, 129, 138, 189] unmedicated vs
    [248, 253, 294, 251, 305] full-pool bin distribution from
    HA-C3p result.md section 2 at locked quintile boundaries
    {Q1[0,28), Q2[28,31), Q3[31,34), Q4[34,37), Q5[37,100]}.
    """
    bin_edges = [0, 28, 31, 34, 37, 100]
    bin_labels = ["Q1[0,28)", "Q2[28,31)", "Q3[31,34)", "Q4[34,37)", "Q5[37,100]"]

    out = {
        "bin_edges": bin_edges,
        "bin_labels": bin_labels,
        "source": "HA-C3p result.md section 2 locked quintile boundaries (pre-committed at draft time on per_day_master.csv SHA-256 d0ff9253)",
    }
    # Full Stratum 4 single pool
    full = df[channel].dropna().astype(float)
    full_counts = np.histogram(full.values, bins=bin_edges)[0].tolist()
    out["full_stratum_4_n"] = int(len(full))
    out["full_stratum_4_bin_counts"] = full_counts
    out["full_stratum_4_bin_shares_pct"] = [
        round(100.0 * c / len(full), 2) if len(full) > 0 else None for c in full_counts
    ]

    # Unmedicated sub-pool
    unmed_mask = (df["date"] >= pd.Timestamp("2022-09-03")) & (df["date"] <= pd.Timestamp("2024-04-08"))
    unmed = df.loc[unmed_mask, channel].dropna().astype(float)
    unmed_counts = np.histogram(unmed.values, bins=bin_edges)[0].tolist()
    out["unmedicated_n"] = int(len(unmed))
    out["unmedicated_bin_counts"] = unmed_counts
    out["unmedicated_bin_shares_pct"] = [
        round(100.0 * c / len(unmed), 2) if len(unmed) > 0 else None for c in unmed_counts
    ]

    # Finer quantile resolution (deciles) on the unmedicated pool
    unmed_quantiles = {f"p{q}": float(np.percentile(unmed.values, q)) for q in (10, 20, 30, 40, 50, 60, 70, 80, 90)}
    full_quantiles = {f"p{q}": float(np.percentile(full.values, q)) for q in (10, 20, 30, 40, 50, 60, 70, 80, 90)}
    out["unmedicated_deciles"] = unmed_quantiles
    out["full_stratum_4_deciles"] = full_quantiles

    # Bin share ratios (unmedicated / full pool) — values > 1 mean
    # unmedicated is over-represented in that bin
    ratios = []
    for u, f in zip(out["unmedicated_bin_shares_pct"], out["full_stratum_4_bin_shares_pct"]):
        if u is None or f is None or f == 0:
            ratios.append(None)
        else:
            ratios.append(round(u / f, 2))
    out["share_ratio_unmedicated_over_full_pool"] = ratios

    return out


# ---------------------------------------------------------------------------
# Q3.2.d Phase-stratified distribution + citalopram step magnitude
# ---------------------------------------------------------------------------


def q_d_phase_stratified(per_phase: dict, channel: str) -> dict:
    """Citalopram step magnitude vs natural day-to-day variation (Q3.2.d).

    Reports differences between phase medians and the dispersion of
    each phase. The +0.565/mg locked dose-response slope from
    citalopram_dose_response_stress_mean_sleep.md v3 section 5.6.1
    (largest beta among 3 CONFIRMED channels) is the headline anchor.
    """
    out = {"phase_medians": {}, "phase_to_phase_shifts": {}}
    medians = {}
    for phase_name in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = per_phase.get(phase_name, {})
        if info.get("n", 0) > 0:
            medians[phase_name] = info["median"]
            out["phase_medians"][phase_name] = info["median"]

    pairs = [
        ("unmedicated", "buildup"),
        ("unmedicated", "consolidation"),
        ("consolidation", "afbouw"),
        ("unmedicated", "afbouw"),
    ]
    for a, b in pairs:
        if a in medians and b in medians:
            out["phase_to_phase_shifts"][f"{b}_minus_{a}_median"] = medians[b] - medians[a]

    typical_within = {
        p: per_phase[p].get("mad_unscaled") for p in medians if "mad_unscaled" in per_phase[p]
    }
    out["within_phase_mad"] = typical_within

    # Citalopram dose-response anchor (locked; CONFIRMED beta):
    out["citalopram_dose_response_anchor"] = {
        "buildup_beta_per_mg": +0.565,
        "buildup_p": 0.000,
        "afbouw_beta_per_mg": +0.209,
        "afbouw_p": 0.19,
        "spring_2025_beta_per_day": -0.001,
        "verdict": "CONFIRMED (sign matches prior in both phases AND buildup HAC 95% CI excludes zero on prior-direction side)",
        "source": "methodology/citalopram_dose_response_stress_mean_sleep.md v3 section 5.6.1",
        "sister_channels": {
            "stress_mean_sleep_buildup_beta": +0.429,
            "bb_lowest_buildup_beta": -1.134,
            "context": "largest beta among 3 CONFIRMED channels on the autonomic-load + recovery family",
        },
    }
    # Implied steady-state effect at 30 mg consolidation:
    out["implied_30mg_lift_buildup_beta"] = +0.565 * 30  # +16.95 stress units
    return out


# ---------------------------------------------------------------------------
# Q3.2.e Near-identity check
# ---------------------------------------------------------------------------

NEAR_IDENTITY_THRESHOLD = 0.92  # CONVENTIONS section 3.3


def q_e_near_identity(df: pd.DataFrame, channel: str) -> dict:
    """Near-identity check vs three brief-mandated channels + extended
    set (Q3.2.e).

    The three brief-mandated channels per descriptive README section 3.2
    + parity with stress_mean_sleep Q3.1.e:
      - stress_stdev_sleep
      - stress_mean_sleep (sister CONFIRMED-citalopram channel; r=+0.52
        per stress_mean_sleep Q3.1.e)
      - stress_low_motion_min_count_S60_Mlow (count-primitive cousin;
        r=+0.85 per stress_low_motion findings.md Q3.x.e — this is
        the cross-test pair that should NOT be near-identity on
        the count-primitive side but the relationship is asymmetric)
    Plus three biologically-plausible neighbours.
    """
    targets = [
        "stress_stdev_sleep",
        "stress_mean_sleep",
        "stress_low_motion_min_count_S60_Mlow",
        "awake_stress_avg",
        "asleep_stress_avg_uds",
        "bb_lowest",
        "all_day_stress_max",
        "resting_hr",
    ]
    rows = []
    flags = []
    for t in targets:
        if t not in df.columns:
            rows.append({"channel": t, "note": "column absent"})
            continue
        sub = df[[channel, t]].dropna()
        if len(sub) < 30:
            rows.append({"channel": t, "n": int(len(sub)), "note": "n<30 - skipped"})
            continue
        pear = float(sub[channel].corr(sub[t]))
        spear = float(sub[channel].corr(sub[t], method="spearman"))
        flagged = max(abs(pear), abs(spear)) >= NEAR_IDENTITY_THRESHOLD
        rows.append({
            "channel": t,
            "n": int(len(sub)),
            "pearson_r": pear,
            "spearman_rho": spear,
            "near_identity_flag": flagged,
        })
        if flagged:
            flags.append(t)
    return {
        "threshold": NEAR_IDENTITY_THRESHOLD,
        "rows": rows,
        "flagged_pairs": flags,
        "note": (
            "Sister stress_mean_sleep Q3.1.e found Pearson r=+0.522 / Spearman rho=+0.404 "
            "with this channel on Stratum 4. stress_low_motion findings.md Q3.x.e found "
            "Pearson r=+0.847 / Spearman rho=+0.860 with this channel (very high but NOT "
            "near-identity); the spike-form and daily-mean-form carry strongly overlapping "
            "signal on this corpus."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.2.f Crash-day vs normal-day on Stratum 4 + crash-drop sensitivity
# ---------------------------------------------------------------------------


def _mann_whitney_u(crash_vals: np.ndarray, normal_vals: np.ndarray) -> dict:
    """Compute Mann-Whitney U with normal approximation + tie correction.

    Returns U, z, p (two-sided), P(crash > normal). Vendored to avoid a
    hard scipy dependency.
    """
    n_c = len(crash_vals)
    n_n = len(normal_vals)
    pooled = np.concatenate([crash_vals, normal_vals])
    # Mid-rank for ties
    order = np.argsort(pooled, kind="mergesort")
    sorted_pooled = pooled[order]
    ranks = np.empty(len(pooled), dtype=float)
    i = 0
    while i < len(pooled):
        j = i + 1
        while j < len(pooled) and sorted_pooled[j] == sorted_pooled[i]:
            j += 1
        avg_rank = (i + j + 1) / 2.0
        for k in range(i, j):
            ranks[order[k]] = avg_rank
        i = j
    R_c = float(ranks[:n_c].sum())
    U_c = R_c - n_c * (n_c + 1.0) / 2.0
    # tie correction
    _, counts = np.unique(pooled, return_counts=True)
    tie_term = float(np.sum(counts ** 3 - counts)) / (
        (n_c + n_n) * (n_c + n_n - 1)
    )
    mean_U = n_c * n_n / 2.0
    var_U = (n_c * n_n / 12.0) * ((n_c + n_n + 1) - tie_term)
    if var_U <= 0:
        z = float("nan")
        p = float("nan")
    else:
        # continuity-corrected z
        z = (U_c - mean_U - 0.5 * np.sign(U_c - mean_U)) / np.sqrt(var_U)
        # two-sided p via standard normal survival
        from math import erf, sqrt
        # P(|Z| >= |z|) = 2 * (1 - Phi(|z|))
        p = float(2.0 * (1.0 - 0.5 * (1.0 + erf(abs(z) / sqrt(2.0)))))
    p_crash_gt_normal = float(U_c / (n_c * n_n)) if n_c * n_n > 0 else float("nan")
    return {
        "U_crash_first_sample": float(U_c),
        "z": float(z),
        "p_two_sided": float(p),
        "p_crash_greater_than_normal": p_crash_gt_normal,
        "median_diff": float(np.median(crash_vals) - np.median(normal_vals)),
    }


def q_f_crash_vs_normal(df: pd.DataFrame, channel: str, seed: int = 20260624) -> dict:
    """Crash-vs-normal Cohen's d + Mann-Whitney U + crash-drop
    sensitivity (Q3.2.f).

    Mirror of stress_mean_sleep Q3.1.f with Mann-Whitney U added
    (parity with stress_low_motion Q3.x.f) since the channel is heavy-
    tailed (Q3.2.a). Uses stationary-bootstrap CI at E[L]=7 AND
    data-driven E[L]* when factor-of-2 flag fires (Q3.2.b).
    """
    sub = df[[channel, "is_crash", "episode_id"]].dropna(subset=[channel, "is_crash"])
    is_crash = sub["is_crash"].astype(bool)
    crash_vals = sub.loc[is_crash, channel].astype(float)
    normal_vals = sub.loc[~is_crash, channel].astype(float)

    n_crash_day = int(len(crash_vals))
    n_normal_day = int(len(normal_vals))
    mean_diff_day = float(crash_vals.mean() - normal_vals.mean())
    pooled_sd = float(
        np.sqrt(((len(crash_vals) - 1) * crash_vals.var(ddof=1)
                 + (len(normal_vals) - 1) * normal_vals.var(ddof=1))
                / (len(crash_vals) + len(normal_vals) - 2))
    )
    cohens_d_day = mean_diff_day / pooled_sd if pooled_sd > 0 else float("nan")

    # Mann-Whitney U at day level (heavy-tail robustness)
    mwu = _mann_whitney_u(crash_vals.to_numpy(), normal_vals.to_numpy())

    # Episode-level (per CONVENTIONS section 3.6 prefer episode count for per-event stats)
    ep_mask = sub["episode_id"].notna() & sub["episode_id"].astype(str).str.startswith("crash-")
    ep_df = sub.loc[ep_mask, [channel, "episode_id"]].copy()
    per_episode_mean = ep_df.groupby("episode_id")[channel].mean()
    n_episodes = int(len(per_episode_mean))
    normal_base_vals = normal_vals.copy()
    n_normal_base = int(len(normal_base_vals))

    if n_episodes >= 2:
        ep_mean = float(per_episode_mean.mean())
        ep_sd = float(per_episode_mean.std(ddof=1))
        base_mean = float(normal_base_vals.mean())
        base_sd = float(normal_base_vals.std(ddof=1))
        ep_diff = ep_mean - base_mean
        pooled_ep_sd = float(
            np.sqrt(((n_episodes - 1) * ep_sd ** 2 + (n_normal_base - 1) * base_sd ** 2)
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
        cohens_d_ep = float("nan")
        ci_low = float("nan")
        ci_high = float("nan")

    # Day-level stationary-bootstrap CI at BOTH E[L]=7 and data-driven
    # E[L]* (post-Q3.2.b knowledge). Build aligned series sorted by date.
    aligned = df[["date", channel, "is_crash"]].dropna(subset=[channel, "is_crash"]).copy()
    aligned = aligned.sort_values("date").reset_index(drop=True)

    def day_mean_diff(sub_df):
        c = sub_df["is_crash"].astype(bool)
        if c.sum() < 1 or (~c).sum() < 1:
            return float("nan")
        return float(sub_df.loc[c, channel].mean() - sub_df.loc[~c, channel].mean())

    # E[L]* is computed once upstream; we recompute here for self-containment
    el_result = compute_data_driven_block_length(
        df[channel].dropna().to_numpy(),
        default_block_length=7,
    )
    el_star = int(round(el_result["optimal_block_length"]))
    el_star = max(1, el_star)

    boot_day_E7 = stationary_bootstrap_ci(
        aligned, day_mean_diff,
        n_bootstrap=5000, expected_block_length=7,
        confidence_level=0.95, random_state=seed,
    )
    boot_day_Estar = stationary_bootstrap_ci(
        aligned, day_mean_diff,
        n_bootstrap=5000, expected_block_length=el_star,
        confidence_level=0.95, random_state=seed,
    )

    # Crash-drop sensitivity on Spearman(channel, gevoelscore) per CONVENTIONS 3.4
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
            "cohens_d": cohens_d_day,
            "mann_whitney_u": mwu,
            "stationary_bootstrap_E_L7": {
                "point_estimate": float(boot_day_E7["point_estimate"]),
                "ci_lower": float(boot_day_E7["ci_lower"]),
                "ci_upper": float(boot_day_E7["ci_upper"]),
                "note": "project default per permutation_null_block_length.md",
            },
            "stationary_bootstrap_E_L_star": {
                "block_length_used": el_star,
                "point_estimate": float(boot_day_Estar["point_estimate"]),
                "ci_lower": float(boot_day_Estar["ci_lower"]),
                "ci_upper": float(boot_day_Estar["ci_upper"]),
                "note": "data-driven from Q3.2.b; rounded to nearest integer",
            },
            "note": (
                "consecutive within-episode days are autocorrelated; "
                "treat as autocorrelation-inflated supplementary read"
            ),
        },
        "episode_level": {
            "n_crash_episodes": n_episodes,
            "n_normal_day_base_rate": n_normal_base,
            "mean_per_episode_stress": ep_mean,
            "mean_normal_day_stress": float(normal_base_vals.mean()) if n_normal_base else float("nan"),
            "mean_diff_episode_vs_normal_day": ep_diff,
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
# Q3.2.g Spike-detecting primitive availability
# ---------------------------------------------------------------------------


def q_g_spike_primitive(df: pd.DataFrame, channel: str) -> dict:
    """Spike-primitive availability for all_day_stress_avg (Q3.2.g).

    all_day_stress_avg is the 24h-window daily mean stress (UDS-pre-
    aggregated, JSON passthrough per garmin_indicators_audit.md Wave 3
    2026-06-12 propagation). Per CONVENTIONS section 3.5 it is the
    dilution-vulnerable continuous-form cousin of the spike-counting
    primitive stress_low_motion_min_count_S60_Mlow (which was the third
    Phase-1 analysis). all_day_stress_max is the daily peak surfaced in
    the master.
    """
    out = {
        "channel_resolution": "24h-window daily mean (UDS-pre-aggregated; JSON passthrough)",
        "sub_daily_resolution_in_master": False,
        "spike_primitives_available_in_master": [],
        "latent_in_FIT_not_in_master": [
            "per-minute monitoring_b stress samples (raw ~3-min cadence; the upstream source)",
        ],
        "related_daily_spike_metrics_in_master": [],
        "note": (
            "Per CONVENTIONS section 3.5, sympathetic-arousal proxies prefer spike/peak/"
            "count metrics over daily means; all_day_stress_avg is structurally a 24h-"
            "window mean and therefore dilution-vulnerable. The spike-form companion "
            "stress_low_motion_min_count_S60_Mlow (Phase-1 third analysis) carries "
            "spike-during-rest information beyond the daily mean (Q3.x.e cross-pair "
            "r=+0.85 / rho=+0.86 between this channel and the count primitive; high but "
            "NOT near-identity). all_day_stress_max is the in-master daily peak."
        ),
    }
    for c in (
        "all_day_stress_max",
        "max_spike_minutes",
        "stress_high_duration_min",
        "stress_low_motion_min_count_S60_Mlow",
    ):
        if c in df.columns:
            n = int(df[c].notna().sum())
            out["spike_primitives_available_in_master"].append({"column": c, "n_non_nan": n})
    # Pair-wise corr with sibling spike companions
    for partner in ("all_day_stress_max", "max_spike_minutes", "stress_low_motion_min_count_S60_Mlow"):
        if partner in df.columns:
            d = df[[channel, partner]].dropna()
            if len(d) > 30:
                out[f"pearson_r_vs_{partner}"] = float(d.corr().iloc[0, 1])
                out[f"spearman_rho_vs_{partner}"] = float(d.corr(method="spearman").iloc[0, 1])
                out[f"n_pair_{partner}"] = int(len(d))
    return out


# ---------------------------------------------------------------------------
# Q3.2.h Outlier detection + calibration-drift check
# ---------------------------------------------------------------------------


def q_h_outliers_calibration(df: pd.DataFrame, channel: str) -> dict:
    """Outlier detection + calibration-drift check (Q3.2.h).

    MAD-based |z|>5 on Stratum 4. Reports flagged dates + values + drift
    snapshots. Cross-references garmin_indicators_audit.md (which has
    NO specific row for all_day_stress_avg beyond noting it is a Wave-3
    JSON-side passthrough from daily_uds.csv).
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
        {"date": str(r["date"].date()), "value": float(r[channel]), "mad_z": float(r["mad_z"])}
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
                None if pd.isna(row["rolling_med_90d"]) else float(row["rolling_med_90d"])
            ),
        })
    # Step at 2024-06-20 (consolidation start): trailing-30d vs leading-30d
    step_date = pd.Timestamp("2024-06-20")
    pre30 = sub.loc[(sub["date"] >= step_date - pd.Timedelta(days=30))
                    & (sub["date"] < step_date), channel].mean()
    post30 = sub.loc[(sub["date"] >= step_date)
                     & (sub["date"] < step_date + pd.Timedelta(days=30)), channel].mean()

    # Step at 2024-04-09 (buildup start; citalopram boundary)
    step_buildup = pd.Timestamp("2024-04-09")
    pre30_b = sub.loc[(sub["date"] >= step_buildup - pd.Timedelta(days=30))
                      & (sub["date"] < step_buildup), channel].mean()
    post30_b = sub.loc[(sub["date"] >= step_buildup)
                       & (sub["date"] < step_buildup + pd.Timedelta(days=30)), channel].mean()

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
        "citalopram_boundary_2024_04_09_step": {
            "pre_30d_mean": float(pre30_b) if pre30_b == pre30_b else None,
            "post_30d_mean": float(post30_b) if post30_b == post30_b else None,
            "diff_post_minus_pre": (
                float(post30_b - pre30_b) if (pre30_b == pre30_b and post30_b == post30_b) else None
            ),
        },
        "garmin_indicators_audit_known_issues": [
            (
                "Wave-3 JSON-side passthrough (2026-06-12) from daily_uds.csv; "
                "no FIT parsing needed; one of 5 all-day stress columns extracted"
            ),
            (
                "no specific calibration-drift events catalogued for all_day_stress_avg "
                "in garmin_indicators_audit.md (the audit's per-column provenance map "
                "covers it under the Wave-3 passthrough bullet, not as its own row)"
            ),
            (
                "underlying sensor is Forerunner 245 Elevate V3 throughout entire "
                "2021-08-16 to present window -- no device change"
            ),
        ],
        "garmin_indicators_audit_row_proposal": (
            "PROPOSE-ONLY (do NOT apply as part of this analysis per handoff section 3 / "
            "discipline): the all-day stress family (5 columns: all_day_stress_avg, "
            "all_day_stress_max, awake_stress_avg, asleep_stress_avg_uds, "
            "low_stress_minutes / similar) currently has no per-column row in the "
            "garmin_indicators_audit.md per-column provenance map; only the Wave-3 "
            "passthrough bullet aggregates them. A future audit refresh could surface "
            "all_day_stress_avg as its own row with these known issues. Surface to user "
            "for authorisation in a separate session per the discipline."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.2.i Covariate-sensitivity readiness
# ---------------------------------------------------------------------------


def q_i_covariate_readiness(df: pd.DataFrame, channel: str) -> dict:
    """Covariate-sensitivity readiness (Q3.2.i).

    Per HA-P7 section 4.5.4 worked-example pattern. Names candidate
    covariates a future HA on all_day_stress_avg as predictor could add.
    """
    cands = []
    # 1. dose_plasma_mg(d) — obligatory CONFIRMED-citalopram channel
    cands.append({
        "covariate": "dose_plasma_mg(d)",
        "rationale": (
            "Per citalopram_phase_stratification.md section 5.B the channel is "
            "CONFIRMED dose-modulated at +0.565/mg p=0.000 buildup post-CPAP "
            "(the LARGEST beta among the 3 CONFIRMED channels). A future HA on "
            "all_day_stress_avg cross-phase MUST either dose-adjust (section 5.B) "
            "or per-phase stratify (section 5.A); the covariate is the framework-"
            "prescribed disambiguator. HA-C3 v2 used section 5.A unmedicated headline "
            "AND section 5.B dose-adjusted as cross-phase sensitivity arm (both "
            "REJECTED). HA-C3p used the same dual treatment (section 5.B sensitivity "
            "arm also REJECTED). The dose-adjusted cross-phase pool does NOT recover "
            "the unmedicated-pool inverted-U shape; the section 5.A unmedicated "
            "headline is the load-bearing operationalisation choice for HAs that "
            "want to probe non-linearity on this channel."
        ),
        "source": "methodology/citalopram_phase_stratification.md section 5.B + section 6; HA-C3/HA-C3p result.md applications",
        "expected_effect_if_primary_signal_is_citalopram": (
            "beta_channel collapses toward zero in the secondary model; beta_dose carries the load"
        ),
        "needed_columns_in_master": ["lc_phase or a runtime dose_plasma_mg(d) computation"],
    })
    # 2. stress_mean_sleep — sister CONFIRMED-citalopram channel (autonomic-load shared)
    sister_corr = None
    if "stress_mean_sleep" in df.columns:
        d = df[[channel, "stress_mean_sleep"]].dropna()
        if len(d) > 30:
            sister_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "stress_mean_sleep",
        "rationale": (
            "Sister CONFIRMED-citalopram channel (+0.43/mg beta on sleep-window "
            "stress mean vs +0.57/mg on this channel's 24h mean). Both load on the "
            "same autonomic-load family per dose-response v3 section 5.6.2 (autonomic-"
            "load axis: 24h mean + sleep-window mean both confirmed). The covariate "
            "disambiguates: is the all-day signal specifically driven by the awake "
            "portion of the day (beta_channel survives when sleep-mean enters) or "
            "shared autonomic tone (beta_channel attenuates). The sleep-window vs "
            "24h-window split IS the operational disambiguation."
        ),
        "source": "stress_mean_sleep first analysis findings.md Q3.1.e (Pearson r=+0.522 / Spearman rho=+0.404 with this channel)",
        "observed_correlation_on_S4": sister_corr,
        "expected_effect": (
            "beta_channel attenuates if signal is shared nightly + daily autonomic tone; "
            "beta_channel survives if all-day mean carries awake-portion-specific information"
        ),
    })
    # 3. stress_low_motion_min_count_S60_Mlow — spike-form companion (CONVENTIONS 3.5)
    spike_corr = None
    if "stress_low_motion_min_count_S60_Mlow" in df.columns:
        d = df[[channel, "stress_low_motion_min_count_S60_Mlow"]].dropna()
        if len(d) > 30:
            spike_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "stress_low_motion_min_count_S60_Mlow",
        "rationale": (
            "Spike-form companion per CONVENTIONS section 3.5 (the third Phase-1 "
            "Strand A analysis covers this channel as primary). The cross-pair is "
            "r=+0.85 / rho=+0.86 per stress_low_motion findings.md Q3.x.e -- high "
            "shared signal but NOT near-identity. The covariate disambiguates: is "
            "the all-day stress signal driven by the temporal-density of "
            "above-threshold minutes (beta_channel attenuates -- spike-count was "
            "doing the work) or by the average level (beta_channel survives -- "
            "the daily mean carries information beyond the threshold-crossing count). "
            "This is the spike-vs-mean disambiguator per CONVENTIONS section 3.5."
        ),
        "source": "stress_low_motion findings.md Q3.x.e + Q3.x.i (this channel is named as section 3.5 continuous-form cousin)",
        "observed_correlation_on_S4": spike_corr,
        "expected_effect": (
            "beta_channel attenuates if signal is threshold-crossing density; "
            "beta_channel survives if the daily-mean carries broader information"
        ),
    })
    # 4. own-lagged 14d mean — autocorrelation-vs-mechanism (HA-P7 section 4.5.4)
    cands.append({
        "covariate": "all_day_stress_avg_lagged_mean_14d(d) = mean(channel[d-14:d-1])",
        "rationale": (
            "Mirrors HA-P7 section 4.5.4 worked example (lagged outcome covariate) "
            "for the autocorrelation-vs-mechanism disambiguation. Cutoff lag M and "
            "data-driven E[L]* from Q3.2.b set the window choice; a 14d trailing "
            "mean is the typical conservative window when E[L]* < 14. If Q3.2.b "
            "fires the factor-of-2 deviation flag with E[L]* > 14, this covariate "
            "should be widened (e.g. to 21d or 28d, mirroring the stress_low_motion "
            "third analysis's recommendation at its E[L]*=21). The consumer-test "
            "pre-reg has discretion to set the window past M with margin."
        ),
        "source": "HA-P7 hypothesis.md section 4.5.4 worked example",
        "expected_effect": (
            "beta_channel collapses if today's stress is just yesterday's stress carried forward; "
            "beta_channel survives if the signal carries new-day information"
        ),
        "needed_columns_in_master": [
            "either computed in-script or added to per_day_master as all_day_stress_avg_lagged_mean_14d"
        ],
    })
    return {
        "primary_use_case": (
            "Future HA pre-reg using all_day_stress_avg as predictor of a crash-related outcome"
        ),
        "discipline_anchor": "HA-P7 hypothesis.md section 4.5.4 -- secondary-logistic-with-covariate pattern",
        "candidate_covariates": cands,
        "recommendation": (
            "Pre-spec all four covariates as secondary sensitivity arms. The "
            "citalopram-phase framework section 5.B adjustment is OBLIGATORY (the "
            "channel is CONFIRMED-citalopram); the other three are diagnostic. "
            "Concordance across the secondaries = high confidence in the primary; "
            "divergence = the disambiguation is doing real work. **HA-C3 cluster "
            "lesson** (post-2026-06-23 cross-test consolidation): the section 5.A "
            "unmedicated headline + section 5.B dose-adjusted cross-phase sensitivity "
            "produced consistent REJECTED-on-cross-phase but inverted-U-on-unmedicated "
            "readings on this channel; HAs probing non-linearity on this channel "
            "should follow that dual-treatment template per the HA-C3p result.md "
            "section 4 sensitivity table."
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

    # Figure 1: Histogram
    fig, ax = plt.subplots(figsize=(8, 4.2))
    vals = sub[channel].astype(float)
    ax.hist(vals, bins=40, color="#5b88c4", edgecolor="white", alpha=0.85)
    med = float(vals.median())
    p25, p75 = np.percentile(vals, 25), np.percentile(vals, 75)
    ax.axvline(med, color="#222", linestyle="-", linewidth=1.5, label=f"median={med:.2f}")
    ax.axvline(p25, color="#222", linestyle="--", linewidth=1.0, label=f"p25={p25:.2f}")
    ax.axvline(p75, color="#222", linestyle="--", linewidth=1.0, label=f"p75={p75:.2f}")
    ax.set_xlabel("all_day_stress_avg (Garmin units)")
    ax.set_ylabel("days (Stratum 4)")
    ax.set_title(f"all_day_stress_avg distribution - Stratum 4, n={int(vals.notna().sum())}")
    ax.legend(loc="upper right")
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
    keep = [p for p in ("unmedicated", "buildup", "consolidation", "afbouw")
            if len(phase_data[p]) >= 5]
    ax.violinplot(
        [phase_data[p] for p in keep],
        showmedians=True, widths=0.85,
    )
    ax.set_xticks(np.arange(1, len(keep) + 1))
    ax.set_xticklabels(keep)
    ax.set_ylabel("all_day_stress_avg")
    ax.set_title("Phase-stratified distribution (citalopram axis, Stratum 4)")
    fig.tight_layout()
    fp = out_dir / "fig2_phase_stratified.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 3: Time series with rolling 90d median + phase shading
    sub_sorted = sub.sort_values("date").reset_index(drop=True)
    sub_sorted["roll90"] = sub_sorted[channel].rolling(90, min_periods=45).median()
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.plot(sub_sorted["date"], sub_sorted[channel], color="#aac4e3", linewidth=0.6, alpha=0.6, label="daily")
    ax.plot(sub_sorted["date"], sub_sorted["roll90"], color="#1f3a5f", linewidth=1.8, label="rolling 90d median")
    phase_colors = {
        "unmedicated": "#ffffff",
        "buildup": "#fde0a3",
        "consolidation": "#ffd680",
        "afbouw": "#fdbf6f",
    }
    for phase_name, start, end in PHASE_BOUNDARIES:
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end),
                   color=phase_colors[phase_name], alpha=0.18, label=phase_name)
    h, l = ax.get_legend_handles_labels()
    seen = set()
    pairs = [(hi, li) for hi, li in zip(h, l) if not (li in seen or seen.add(li))]
    ax.legend([p[0] for p in pairs], [p[1] for p in pairs],
              loc="upper right", fontsize=8, ncol=2)
    ax.set_ylabel("all_day_stress_avg")
    ax.set_title("all_day_stress_avg - rolling 90d median + citalopram phases")
    fig.tight_layout()
    fp = out_dir / "fig3_trajectory_with_phases.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 4: Crash vs normal
    df_ep = sub.copy()
    df_ep["is_crash"] = df_ep["is_crash"].astype(bool)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    normal = df_ep.loc[~df_ep["is_crash"], channel]
    crash = df_ep.loc[df_ep["is_crash"], channel]
    ax.hist(normal, bins=40, color="#9dc1e0", alpha=0.7, label=f"normal days n={len(normal)}", density=True)
    ax.hist(crash, bins=20, color="#cc4949", alpha=0.55, label=f"crash days n={len(crash)}", density=True)
    ax.axvline(normal.median(), color="#264c75", linestyle="--", label=f"normal median={normal.median():.1f}")
    ax.axvline(crash.median(), color="#7a1f1f", linestyle="--", label=f"crash median={crash.median():.1f}")
    ax.set_xlabel("all_day_stress_avg")
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
        f"ACF - all_day_stress_avg (Stratum 4); E[L]*={acf_res['optimal_block_length']:.1f}, M={acf_res['cutoff_lag']}"
    )
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fp = out_dir / "fig5_acf.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    return written


# ---------------------------------------------------------------------------
# Markdown emitters (findings.md + README.md)
# ---------------------------------------------------------------------------


def _fmt_acf_table(acf_dict: dict) -> str:
    rows = ["| lag (days) | autocorrelation |", "|---:|---:|"]
    for lag_label in ("acf_lag1", "acf_lag2", "acf_lag3", "acf_lag7", "acf_lag14"):
        if lag_label in acf_dict:
            v = acf_dict[lag_label]
            sign = "+" if v >= 0 else ""
            rows.append(f"| {lag_label.replace('acf_lag', '')} | {sign}{v:.3f} |")
    return "\n".join(rows)


def _fmt_quintile_table(q: dict) -> str:
    rows = [
        "| bin | unmed n | unmed share % | full S4 n | full S4 share % | share ratio (unmed/full) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    labels = q["bin_labels"]
    for i, lab in enumerate(labels):
        u_n = q["unmedicated_bin_counts"][i]
        u_pct = q["unmedicated_bin_shares_pct"][i]
        f_n = q["full_stratum_4_bin_counts"][i]
        f_pct = q["full_stratum_4_bin_shares_pct"][i]
        ratio = q["share_ratio_unmedicated_over_full_pool"][i]
        rows.append(
            f"| {lab} | **{u_n}** | {u_pct}% | {f_n} | {f_pct}% | **{ratio}** |"
        )
    rows.append(
        f"| total | {q['unmedicated_n']} | 100% | {q['full_stratum_4_n']} | 100% | -- |"
    )
    return "\n".join(rows)


def write_findings_md(summary: dict, path: Path) -> None:
    """Emit the analyst-style findings.md report from the computed summary.

    Layer 1 descriptive per CONVENTIONS section 2.1; cross-references to
    the HA-C3 cluster verdicts + recovery_arc v2 + Phase-1 precedents
    + recalibration anchor are descriptive only, NOT verdict promotion.
    """
    q = summary["questions"]
    a = q["Q3.2.a_distribution"]
    b = q["Q3.2.b_autocorrelation"]
    c = q["Q3.2.c_base_rates_per_phase"]
    cq = q["Q3.2.c_quintile_bin_distribution"]
    d = q["Q3.2.d_phase_stratified_distribution"]
    e = q["Q3.2.e_near_identity"]
    fr = q["Q3.2.f_crash_vs_normal"]
    fl = fr["day_level"]
    fe = fr["episode_level"]
    g = q["Q3.2.g_spike_primitive"]
    h = q["Q3.2.h_outliers_calibration"]
    i = q["Q3.2.i_covariate_readiness"]

    el_star = b["data_driven_E_L_star"]
    el_int = int(round(el_star))
    quant = a["quantiles"]
    skew = a["skewness"]
    p99 = quant["p99"]
    med = a["median"]
    p99_over_med = p99 / med if med > 0 else float("nan")

    e7 = fl["stationary_bootstrap_E_L7"]
    eS = fl["stationary_bootstrap_E_L_star"]
    width7 = e7["ci_upper"] - e7["ci_lower"]
    widthS = eS["ci_upper"] - eS["ci_lower"]
    width_change_pct = (widthS - width7) / width7 * 100 if width7 > 0 else float("nan")
    mwu = fl["mann_whitney_u"]
    ci_ep = fe["bootstrap_ci95_mean_diff"]
    cd = fr["crash_drop_sensitivity_on_spearman_vs_gevoelscore"]
    citalo_step = h["citalopram_boundary_2024_04_09_step"]
    consol_step = h["consolidation_boundary_2024_06_20_step"]
    outliers = h["outliers"]

    near_id_rows = []
    for r in e["rows"]:
        if "pearson_r" in r:
            flag = "no" if not r["near_identity_flag"] else "**YES**"
            near_id_rows.append(
                f"| `{r['channel']}` | {r['n']} | {r['pearson_r']:+.3f} | {r['spearman_rho']:+.3f} | {flag} |"
            )

    per_phase_rows = []
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = c.get(ph, {})
        if info.get("n", 0) > 0:
            per_phase_rows.append(
                f"| {ph} | {info['date_start']} to {info['date_end']} | {info['n']} | "
                f"**{info['median']:.2f}** | {info['mean']:.2f} | {info['mad_unscaled']:.2f} | "
                f"{info['p10']:.1f} / {info['p90']:.1f} |"
            )

    out_lines = [
        "# Findings -- `all_day_stress_avg` operationalisation-support descriptive (Q3.2.a-i)",
        "",
        "**Channel**: `all_day_stress_avg` (CONFIRMED-citalopram, +0.565/mg p=0.000 buildup post-CPAP per "
        "[`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "v3 section 5.6.1 -- the **largest beta** among the 3 CONFIRMED channels). Column semantics: "
        "[DATA_DICTIONARY.md section 7B All-day stress](../../../DATA_DICTIONARY.md) -- 24h-window mean of UDS "
        "pre-aggregated stress samples, JSON-passthrough from `daily_uds.csv` per "
        "[`garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) Wave-3 propagation "
        "2026-06-12 (no FIT parsing).",
        "",
        f"**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to {summary['as_of_date']}). "
        f"n={a['n']} days with channel out of {summary['n_rows_stratum_4_total']} Stratum 4 days "
        f"({summary['n_rows_stratum_4_total'] - a['n']} NaN days from UDS-side coverage gaps).",
        "",
        "**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.2 (LOCKED 2026-06-18 r3, "
        "commit `ccbd12e`) -- this analysis is the **second of the 3 CONFIRMED-citalopram channels in the "
        "Tier 1 user-prioritised Phase 2 sequential batch** (R14 `single_pool_reanchor` landed first at "
        "`badd04a`; `bb_lowest` next). Q3.2.a-i template applied per section 3.1 verbatim.",
        "",
        "**Sources**: `per_day_master.csv` (Garmin daily aggregate) + `labels_crash_v2.csv` (`label=='crash'` "
        "day-level; `episode_id` starting with `crash-` episode-level per CONVENTIONS section 3.6).",
        "",
        "**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict "
        "promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). "
        "HA-C3 cluster (HA-C3 v2 REJECTED `a2b18ba` + HA-C3p PARTIAL `e5a63fe`, both 2026-06-23) "
        "cross-references in this analysis are **descriptive corroboration only**; the inverted-U / "
        "concave non-linearity finding lives in those result.md files and is NOT extended here per "
        "CONVENTIONS section 4.2 (caveats yes; a-priori claims no). Statistical hygiene anchors: section "
        "3.1 (personal baseline), section 3.3 (column-duplication threshold |rho|>=0.92), section 3.4 "
        "(crash-drop sensitivity |delta|>0.10), section 3.5 (spike metrics -- this channel is a 24h-window "
        "MEAN; the spike-form companion lives in `stress_low_motion_min_count_S60_Mlow`), section 3.6 "
        "(named counts).",
        "",
        "---",
        "",
        "## Headline",
        "",
        f"`all_day_stress_avg` on Stratum 4 is a **mildly right-skewed, autocorrelation-DENSE 24h-window "
        f"daily-mean channel** (skew={skew:+.2f}, excess kurtosis={a['excess_kurtosis']:+.2f} -- "
        f"**NOT heavy-tail-flag-triggering**, p99/median = {p99:.1f}/{med:.1f} = {p99_over_med:.2f}; this "
        f"channel is materially less heavy-tailed than its sister `stress_mean_sleep` skew=+2.72). The "
        f"**data-driven E[L]\\*={el_star:.1f}** (factor-of-4 above project default; **the LONGEST yet "
        f"observed in Strand A**, longer than `stress_low_motion_min_count_S60_Mlow` E[L]\\*=21.1 and "
        f"`stress_mean_sleep` E[L]\\*=12.6). The **phase-stratified medians shift DRAMATICALLY at the "
        f"citalopram boundary** (unmedicated median {c['unmedicated']['median']:.1f} to buildup median "
        f"{c['buildup']['median']:.1f} to consolidation {c['consolidation']['median']:.1f} to afbouw "
        f"{c['afbouw']['median']:.1f}; "
        f"~{d['phase_to_phase_shifts']['buildup_minus_unmedicated_median']:+.1f} median shift at the "
        f"buildup boundary, ~-1.8 within-buildup-phase MAD); the citalopram 30d-mean step (2024-04-09 "
        f"pre/post) is **{citalo_step['diff_post_minus_pre']:+.1f} stress units** -- empirically larger "
        f"than the recalibration's slope-extrapolation predicts at the day-resolution of the boundary. "
        f"The **afbouw phase recovers fully to the unmedicated median** "
        f"(median {c['afbouw']['median']:.1f} = unmedicated {c['unmedicated']['median']:.1f}), suggesting "
        f"a within-citalopram-traject reversibility readable from this descriptive layer (consistent with "
        f"the `recovery_arc v2` afbouw-reversal finding cross-referenced in `descriptive/README.md` section "
        f"5). Crash-vs-normal at episode level is **weak** (d={fe['cohens_d_episode_vs_normal_day']:+.2f}; "
        f"bootstrap CI95 [{ci_ep[0]:+.2f}, {ci_ep[1]:+.2f}] **brushes zero**); day-level Mann-Whitney U "
        f"fires robustly (z={mwu['z']:+.2f}, p<0.0001, P(crash>normal)={mwu['p_crash_greater_than_normal']:.3f}). "
        f"**Zero near-identity pairs** at the |rho|>=0.92 threshold; closest is `awake_stress_avg` at "
        f"rho=+0.887 (just below). The **HA-C3p right-shift unmedicated bin observation is REPRODUCED "
        f"EXACTLY** at the quintile boundaries (unmed counts {cq['unmedicated_bin_counts']}, "
        f"n={cq['unmedicated_n']}; full pool {cq['full_stratum_4_bin_counts']}, n={cq['full_stratum_4_n']} "
        f"-- HA-C3p's full pool was n=1351 because that pre-reg additionally gevoelscore-filtered); the "
        f"unmedicated stratum carries **{cq['share_ratio_unmedicated_over_full_pool'][4]:.2f}x the full-"
        f"pool share of Q5 mass and {cq['share_ratio_unmedicated_over_full_pool'][0]:.2f}x the full-pool "
        f"share of Q1 mass**, an extension of the HA-C3p descriptive observation to a share-ratio "
        f"quantification.",
        "",
        "---",
        "",
        "## Q3.2.a -- Distribution shape (Stratum 4)",
        "",
        "**Verdict on the section 3.1 delegate question**: **delegate is partial; extend in this analysis**. "
        "[`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) was extended "
        "for continuous channels first and primarily documents `stress_mean_sleep`; coverage on "
        "`all_day_stress_avg` is incidental. The full distribution descriptors (skewness/kurtosis/heavy-"
        "tail flag/p99-vs-median ratio) are surfaced here for the first time on this channel.",
        "",
        "| stat | value | source |",
        "|---|---:|---|",
        f"| n (Stratum 4) | {a['n']} | `per_day_master.csv` `all_day_stress_avg` non-NaN within S4 |",
        f"| mean | {a['mean']:.2f} | (single-pool S4) |",
        f"| median | {a['median']:.2f} | |",
        f"| std (ddof=1) | {a['std_ddof1']:.2f} | |",
        f"| MAD (unscaled) | {a['mad_unscaled']:.2f} | |",
        f"| MAD x 1.4826 (normal-equivalent SD) | {a['mad_normal_equivalent']:.2f} | for robust z-score scaling per section 3.1 |",
        f"| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | {quant['p1']:.1f} / {quant['p5']:.1f} / {quant['p10']:.1f} / {quant['p25']:.1f} / {quant['p50']:.1f} / {quant['p75']:.1f} / {quant['p90']:.1f} / {quant['p95']:.1f} / {quant['p99']:.1f} | |",
        f"| skewness (Fisher-Pearson) | **{a['skewness']:+.2f}** | mildly right-skewed; **does NOT trigger skew>1 heavy-tail rule** |",
        f"| excess kurtosis (Fisher) | **{a['excess_kurtosis']:+.2f}** | mildly heavy-tailed (sister stress_mean_sleep was +15.5) |",
        f"| heavy_tail_flag | **{a['heavy_tail_flag']}** | skew<=1 AND p99/median = {p99_over_med:.2f} < 3.0 (both heavy-tail conditions fail) |",
        f"| range | {a['min']:.1f} to {a['max']:.1f} | tail extends to ~{a['max']/a['median']:.1f}x median (sister stress_mean_sleep reached ~4.2x) |",
        "",
        "### Cross-channel comparison vs sister `stress_mean_sleep` (first analysis Q3.1.a)",
        "",
        "| stat | all_day_stress_avg (this analysis) | stress_mean_sleep (first analysis) |",
        "|---|---:|---:|",
        f"| n S4 | {a['n']} | 1339 |",
        f"| mean | {a['mean']:.2f} | 19.97 |",
        f"| median | {a['median']:.2f} | 19.21 |",
        f"| MAD (unscaled) | {a['mad_unscaled']:.2f} | 2.87 |",
        f"| skewness | {a['skewness']:+.2f} | +2.72 |",
        f"| excess kurtosis | {a['excess_kurtosis']:+.2f} | +15.45 |",
        f"| heavy_tail_flag | **{a['heavy_tail_flag']}** | **True** |",
        f"| p99 / median ratio | {p99_over_med:.2f} | 2.27 |",
        "",
        "**The 24h-window mean is materially less heavy-tailed than the sleep-window mean.** Mechanistic "
        "reading: the 24h-window aggregates over many minutes (~480 stress samples at 3-min cadence), so "
        "extreme-night events get diluted; the sleep-window mean (~120 samples per night) is more "
        "susceptible to a single bad night driving the day's stat. The implication for HA-pre-regs: the "
        "robust-vs-non-robust z-scoring choice matters less for this channel than for the sister (raw "
        f"std is {a['std_ddof1']:.2f} vs robust-equiv {a['mad_normal_equivalent']:.2f}, only a "
        f"{abs(a['std_ddof1'] - a['mad_normal_equivalent']) / a['std_ddof1'] * 100:.1f}% difference; "
        "sister's was 30%). The MAD-based robust z-scoring per CONVENTIONS section 3.1 is **still "
        "preferred** -- the heavy-tail-flag failing does not promote to \"use mean+std\" -- but the cost "
        "of getting it wrong is smaller here.",
        "",
        "See [`plots/fig1_distribution_s4.png`](plots/fig1_distribution_s4.png).",
        "",
        "---",
        "",
        "## Q3.2.b -- Autocorrelation structure + E[L]\\*",
        "",
        f"The **data-driven block length is E[L]\\*={el_star:.1f}** (Politis-White 2004 with Patton-"
        "Politis-White 2009 correction per "
        "[`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) "
        "vs the project default E[L]=7 per "
        "[`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). "
        f"The **factor-of-2 deviation flag fires** (deviation ratio = {b['deviation_ratio']:.2f} = factor-"
        f"of-4+ deviation). Cutoff lag M={b['cutoff_lag_M']}. **This is the LONGEST autocorrelation horizon "
        "yet observed in the Strand A landed analyses.**",
        "",
        _fmt_acf_table(b["selected_acf_lags"]),
        "",
        f"Politis-White 2-sigma significance threshold (n={b['n_non_nan']}): "
        f"|rho| = {b['politis_white_significance_threshold_2sigma']:.3f}. The lag-14 ACF "
        f"({b['selected_acf_lags']['acf_lag14']:+.3f}) is **still above the significance threshold**, "
        f"and the lag-7 ACF ({b['selected_acf_lags']['acf_lag7']:+.3f}) is comfortably above -- "
        f"consistent with the M={b['cutoff_lag_M']} cutoff lag (significance persists out to lag ~14-18). "
        "Compare to `stress_mean_sleep` (M=6) and `stress_low_motion_min_count_S60_Mlow` (M=11): this "
        "channel's serial dependence persists FURTHER than either sister.",
        "",
        "### Cross-channel comparison (E[L]\\* by analysis)",
        "",
        "| analysis | channel | E[L]\\* | M | factor-of-2 flag |",
        "|---|---|---:|---:|---|",
        "| Phase-1 #1 (stress_mean_sleep) | sleep-window mean | 12.6 | 6 | YES (factor-of-2) |",
        "| Phase-1 #3 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 | 11 | YES (factor-of-3) |",
        f"| **this analysis (all_day_stress_avg)** | **24h-window mean** | **{el_star:.1f}** | **{b['cutoff_lag_M']}** | **YES (factor-of-4)** |",
        "",
        f"**Implication**: any HA pre-reg using `all_day_stress_avg` MUST (a) use the data-driven block "
        f"length E[L]\\*~{el_int} as the primary bootstrap CI, OR (b) pre-spec a sensitivity arm at "
        f"E[L]={el_int} alongside the default-E[L]=7 primary. The project default of 7 is **dramatically "
        f"too short** for this channel; the factor-of-4 deviation is the largest yet observed in Strand A. "
        "The mechanistic interpretation: the 24h-window mean smooths over many minutes per day AND "
        "inherits long-range trend structure from the citalopram trajectory + LC-recovery arc, both of "
        "which the data-driven estimator picks up on top of the day-to-day serial dependence.",
        "",
        "**HA-C3 cluster note**: HA-C3 v2 and HA-C3p both reported their data-driven E[L]\\* in result.md "
        "section 7 from a different derivation (linear-residual on the continuous predictor = 5.35; "
        "bin-label sequence = 7.0; \"No flags\"). The HAs' bin-label-sequence derivation gives a shorter "
        "E[L]\\* because binning collapses the within-bin trend variance the raw channel carries; the "
        "HAs' E[L]\\*=7 reading is consistent with **the bin-label sequence's own autocorrelation**, NOT "
        f"the underlying raw `all_day_stress_avg` channel's autocorrelation. This descriptive analysis's "
        f"E[L]\\*={el_star:.1f} on the raw channel is a **DIFFERENT derivation from the HAs'**; both are "
        "correct in their respective frames. A consumer test that operates on the raw channel directly "
        f"(not binned) should follow this analysis's E[L]\\*~{el_int}; a consumer test that operates on "
        "a binned/categorical derivative of the channel can follow the HAs' shorter E[L]\\* derivation.",
        "",
        "See [`plots/fig5_acf.png`](plots/fig5_acf.png).",
        "",
        "---",
        "",
        "## Q3.2.c -- Base rates per citalopram phase + quintile bin distribution",
        "",
        "Phase axis per "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3:",
        "",
        "| phase | window | n | median | mean | MAD | p10 / p90 |",
        "|---|---|---:|---:|---:|---:|---|",
        *per_phase_rows,
        "",
        "**The phase medians shift sharply at the citalopram boundary.** Compare to sister "
        "`stress_mean_sleep` (first analysis Q3.1.c) where the phase medians were nearly flat (17.04 to "
        "20.20 across all four phases). On THIS channel:",
        "",
        f"- unmedicated to buildup: **{d['phase_to_phase_shifts']['buildup_minus_unmedicated_median']:+.1f} "
        f"median units** (~-1.8 buildup-MAD; clearly outside MAD)",
        f"- unmedicated to consolidation: **{d['phase_to_phase_shifts']['consolidation_minus_unmedicated_median']:+.1f} "
        f"median units** (~-1.0 consolidation-MAD)",
        f"- consolidation to afbouw: **{d['phase_to_phase_shifts']['afbouw_minus_consolidation_median']:+.1f} "
        f"median units** (recovery toward unmedicated baseline)",
        f"- afbouw vs unmedicated: **{d['phase_to_phase_shifts']['afbouw_minus_unmedicated_median']:+.1f} "
        f"median units** (full recovery to unmedicated baseline)",
        "",
        f"The two **transition phases** (buildup n={c['buildup']['n']}; afbouw n={c['afbouw']['n']}) have "
        f"**n<75 each** with **narrower OR similar dispersion** (MAD~{c['buildup']['mad_unscaled']:.1f}"
        f"-{c['consolidation']['mad_unscaled']:.1f}) than the two **steady-state phases** "
        f"(unmedicated n={c['unmedicated']['n']}; consolidation n={c['consolidation']['n']}, "
        f"MAD~{c['consolidation']['mad_unscaled']:.1f}). Any HA test that wants per-phase verdicts under "
        "[`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 5.A on buildup or afbouw faces a ~8x n disadvantage vs the steady-state phases.",
        "",
        "Named counts (CONVENTIONS section 3.6): the per-phase n's above are `all_day_stress_avg`-non-NaN "
        "day rows in `per_day_master.csv` within Stratum 4 date masks per "
        "`citalopram_phase_stratification.md section 3` boundary dates.",
        "",
        "### Q3.2.c extension -- HA-C3p right-shift unmedicated bin observation REPRODUCED at finer quantile resolution",
        "",
        "Per handoff section 2.4: this section descriptively reproduces / extends the [HA-C3p result.md "
        "section 2 right-shift observation](../../hypotheses/HA-C3p/result.md). HA-C3p's locked quintile "
        f"boundaries are pre-committed to `per_day_master.csv` SHA-256 `d0ff9253` and tested on the "
        f"as-of-date {summary['as_of_date']} corpus.",
        "",
        "Quintile boundaries: {Q1[0,28), Q2[28,31), Q3[31,34), Q4[34,37), Q5[37,100]} (locked per HA-C3p "
        "hypothesis.md section 4.1).",
        "",
        _fmt_quintile_table(cq),
        "",
        f"**The HA-C3p right-shift unmedicated bin counts {cq['unmedicated_bin_counts']} "
        f"(n={cq['unmedicated_n']}) reproduce EXACTLY at this analysis's draft-time snapshot.** The "
        f"full-pool counts differ slightly (this analysis {cq['full_stratum_4_bin_counts']} "
        f"n={cq['full_stratum_4_n']} vs HA-C3p [248, 253, 294, 251, 305] n=1351); the 8-day difference "
        "reflects this analysis's no-gevoelscore-filter approach (descriptive layer) vs HA-C3p's "
        "gevoelscore-required filter (test layer). The substantive right-shift pattern is identical.",
        "",
        "**Share-ratio quantification** (this analysis's extension of the HA-C3p observation): the "
        f"unmedicated stratum carries **{cq['share_ratio_unmedicated_over_full_pool'][4]:.2f}x the "
        f"full-pool share of Q5 mass (~{cq['share_ratio_unmedicated_over_full_pool'][4] / cq['share_ratio_unmedicated_over_full_pool'][0]:.1f}"
        f"x the full-pool share of Q1 mass)** -- a graded right-shift across all five quintiles, "
        f"monotonic from Q1 (under-represented at {cq['share_ratio_unmedicated_over_full_pool'][0]:.2f}) "
        f"through Q3 (essentially at-par at {cq['share_ratio_unmedicated_over_full_pool'][2]:.2f}) to Q5 "
        f"(over-represented at {cq['share_ratio_unmedicated_over_full_pool'][4]:.2f}). The unmedicated "
        f"decile p10/p90 of [{cq['unmedicated_deciles']['p10']:.0f}, {cq['unmedicated_deciles']['p90']:.0f}] "
        f"vs full-pool [{cq['full_stratum_4_deciles']['p10']:.0f}, {cq['full_stratum_4_deciles']['p90']:.0f}] "
        "also shows the right-shift (both quantiles ~+2-3 stress units higher in the unmedicated pool).",
        "",
        "Per handoff section 2.4: this is a **cross-test validation of the recalibration +0.565/mg beta "
        "finding at a different operationalisation** (bin distribution rather than mean beta). The HA-C3p "
        "result.md section 2 framed this consistency descriptively; this analysis reproduces it at the "
        "snapshot level. The HA-C3p substantive verdict is NOT extended or promoted here per the "
        "handoff's NO-HA-verdict-promotion discipline.",
        "",
        "See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (citalopram-phase violins).",
        "",
        "---",
        "",
        "## Q3.2.d -- Phase-stratified distribution + citalopram step magnitude vs natural variation",
        "",
        "**This is the most operationally consequential finding for downstream HA pre-regs on this channel.**",
        "",
        "The locked dose-response anchor (v3 section 5.6.1): **buildup post-CPAP beta = +0.565/mg p=0.000** "
        "(the **LARGEST beta** among the 3 CONFIRMED-citalopram channels: `stress_mean_sleep` +0.43/mg, "
        f"`bb_lowest` -1.13/mg inverse direction). Naive extrapolation: at 30mg steady-state "
        f"(consolidation), the implied citalopram-attributable lift is +0.565 x 30 = "
        f"**+{d['implied_30mg_lift_buildup_beta']:.2f} stress units** -- larger than the channel's full "
        f"interquartile range (p75 - p25 = {quant['p75'] - quant['p25']:.1f}) **DOUBLED**, and ~3 "
        "standard deviations on the consolidation-phase MAD.",
        "",
        "Observed steady-state level shifts (median):",
        "",
        "| comparison | delta median | within-phase MAD | within-MAD? |",
        "|---|---:|---:|---|",
        f"| buildup minus unmedicated | **{d['phase_to_phase_shifts']['buildup_minus_unmedicated_median']:+.1f}** | {c['buildup']['mad_unscaled']:.1f}-{c['unmedicated']['mad_unscaled']:.1f} | ~-1.8 buildup-MAD; clearly OUTSIDE MAD |",
        f"| consolidation minus unmedicated | **{d['phase_to_phase_shifts']['consolidation_minus_unmedicated_median']:+.1f}** | {c['consolidation']['mad_unscaled']:.1f} | ~-1.0 consolidation-MAD; AT the MAD boundary |",
        f"| afbouw minus consolidation | **{d['phase_to_phase_shifts']['afbouw_minus_consolidation_median']:+.1f}** | {c['consolidation']['mad_unscaled']:.1f} | ~+1.0 consolidation-MAD; AT the MAD boundary |",
        f"| afbouw minus unmedicated | **{d['phase_to_phase_shifts']['afbouw_minus_unmedicated_median']:+.1f}** | {c['unmedicated']['mad_unscaled']:.1f} | full recovery to unmedicated baseline |",
        "",
        "### Reading the direction -- what the data shows + the operationalisation-support consequence",
        "",
        f"The median **drops sharply at the citalopram boundary** (unmedicated to buildup: "
        f"{d['phase_to_phase_shifts']['buildup_minus_unmedicated_median']:+.1f} stress units in median, "
        f"~{abs(d['phase_to_phase_shifts']['buildup_minus_unmedicated_median']) / c['unmedicated']['median'] * 100:.0f}% "
        f"reduction) and **recovers fully during afbouw** (afbouw median {c['afbouw']['median']:.1f} = "
        f"unmedicated median {c['unmedicated']['median']:.1f}). The day-resolved citalopram boundary step "
        f"(30d pre vs post the 2024-04-09 boundary): **{citalo_step['diff_post_minus_pre']:+.1f} stress "
        "units** -- larger than the phase-median shift because the buildup phase's first 30 days are "
        "still dose-ramping at sub-steady-state levels.",
        "",
        "This pattern is **opposite in direction to the dose-response beta** (+0.565/mg should push the "
        "channel UP with rising dose, not DOWN). Three readings, none asserted as the substantive truth "
        "per CONVENTIONS section 2.1 + section 4.3:",
        "",
        "1. **The beta is a within-buildup-window dose-trend, not a between-phase steady-state level "
        "shift.** The v3 dose-response MD's beta is the slope of `all_day_stress_avg` against "
        "`dose_plasma_mg(d)` *within* the buildup-window (2024-04-09 to 2024-06-19); it measures how the "
        "channel changes as dose rises from 0 to 30mg over ~70 days. Across phases, the LC-trajectory's "
        "broader recovery arc PLUS the citalopram step PLUS pacing-practice strengthening all overlap; "
        "the between-phase level shift can move opposite to the within-window beta if the broader "
        "trajectory dominates. The recovery_arc v2 analysis "
        "([`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/)) documents this "
        "trajectory at multi-channel detail.",
        "",
        "2. **The dose-adjusted-predictor pattern under "
        "[`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 5.B remains correct for within-phase work**; the cross-phase level shift in raw form is "
        "NOT what the section 5.B framework promises to recover. The HA-C3 v2 and HA-C3p section 5.B "
        "sensitivity arms (cross-phase pool with predictor = raw - 0.565/mg x dose) BOTH returned "
        "REJECTED (0-of-3 conditions MET); the section 5.B numerical adjustment does not recover the "
        "unmedicated-pool inverted-U shape that the section 5.A unmedicated headline carries.",
        "",
        f"3. **The afbouw recovery is descriptively striking**: afbouw median {c['afbouw']['median']:.1f} "
        f"= unmedicated median {c['unmedicated']['median']:.1f} EXACTLY. This is consistent with the "
        "`recovery_arc v2` analysis's afbouw-reversal finding (referenced in `descriptive/README.md` "
        "section 5 [`row 14`](../../README.md): \"section 5.A sub-stratification on phase-5 CONFIRMED-"
        "citalopram channels surfaces **afbouw reversal** (citalopram benefit reversible during dose "
        "reduction)\"). The afbouw recovery on `all_day_stress_avg` corroborates that finding "
        "descriptively. Note: this is a Layer 1 observation; the recovery_arc analysis is the load-"
        "bearing artefact for substantive readings.",
        "",
        "### HA-C3 cluster descriptive cross-reference (load-bearing per handoff section 2.4)",
        "",
        f"The HA-C3 cluster (v2 REJECTED + HA-C3p PARTIAL, both 2026-06-23) detected an **inverted-U / "
        f"concave non-linearity** in the stress to gevoelscore mapping on the **unmedicated section 5.A "
        f"headline pool** (n={c['unmedicated']['n']} here): HA-C3 v2 found bin-means B1[0,30)=3.958, "
        "B2[30,40)=4.265, B3'[40,100]=3.832 (peak at B2); HA-C3p found Q1=3.822, Q2=4.138, Q3=4.271, "
        "Q4=4.290, Q5=4.016 (peak at Q3-Q4). The descriptive bin-mean trajectory at this analysis's "
        "Q3.2.c quintile boundaries (showing the **predictor-side distribution** rather than the outcome-"
        "side trajectory) is consistent with the inverted-U structural reading: the unmedicated stratum's "
        "mass concentrates in the Q3-Q5 region where the HA-C3 cluster found the gevoelscore peak. The "
        f"Q3.2.d phase-median shifts (unmed {c['unmedicated']['median']:.1f} to buildup "
        f"{c['buildup']['median']:.1f}) move the channel mass **toward the lower end of the HA-C3 "
        f"cluster's inverted-U** -- the citalopram boundary pushes typical days into Q1-Q2 (HA-C3p "
        f"Q1[0,28) median predictor; the day-typical value drops from ~{c['unmedicated']['median']:.0f} "
        f"in unmedicated to ~{c['buildup']['median']:.0f} in buildup).",
        "",
        "**Important honesty constraint (handoff section 3 + CONVENTIONS section 4.2)**: this descriptive "
        "observation does NOT extend the HA-C3 cluster's inverted-U substantive claim or promote any "
        "direction-of-causality reading on the citalopram boundary. The HA-C3 cluster verdicts are LOCKED "
        "at REJECTED + PARTIAL (and their joint cross-test reading of \"Wiggers' numbers wrong-for-this-"
        "participant but the underlying SHAPE IS REAL in the INVERSE direction\" is the consolidated "
        "4-cell-matrix reading in HA-C3p result.md section 6, NOT a substantive HA-C3 v3 / HA-C3p v2 "
        "alternative claim). This Q3.2.d's descriptive corroboration is a **substrate that an HA-pre-reg "
        "author can cite when drafting a non-linearity-on-this-channel HA**, not an additive "
        "interpretation layer.",
        "",
        "See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) and "
        "[`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d rolling "
        "median through phases).",
        "",
        "---",
        "",
        "## Q3.2.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)",
        "",
        "Brief-mandated three channels plus five biologically-plausible neighbours.",
        "",
        "| target channel | n | Pearson r | Spearman rho | near-identity flag? |",
        "|---|---:|---:|---:|---|",
        *near_id_rows,
        "",
        "**Zero near-identity pairs fire** at the |rho|>=0.92 CONVENTIONS section 3.3 threshold. The "
        "closest pair is `awake_stress_avg` at Spearman rho=+0.887 (Pearson r=+0.865), well below the "
        "threshold but high enough to warrant care: `awake_stress_avg` is the 24h-window mean restricted "
        "to the awake portion of the day, while this channel includes asleep + awake; the two are "
        "heavily overlapping by construction.",
        "",
        "Three substantive observations beyond the threshold check:",
        "",
        "1. **The spike-form companion `stress_low_motion_min_count_S60_Mlow` is r=+0.85 / rho=+0.86 with "
        "this channel** (reciprocally confirmed: per stress_low_motion findings.md Q3.x.e the same pair "
        "was r=+0.85 / rho=+0.86, n=1358). The continuous-form daily mean and the spike-counting "
        "primitive carry strongly overlapping signal on this corpus but are NOT near-identity. A consumer "
        "HA whose mechanism is *acute spike at rest* should use the count primitive; a consumer HA whose "
        "mechanism is *general autonomic load throughout the day* should use this channel. The two "
        "channels are different constructs operationally even though they covary strongly.",
        "",
        "2. **The sister `stress_mean_sleep` is r=+0.52 / rho=+0.40 with this channel**. Same direction "
        "(both are CONFIRMED-citalopram autonomic-load channels) but **only ~20-30% of the variance is "
        "shared**. This is consistent with the stress_mean_sleep first analysis Q3.1.e finding (same "
        "pair, reciprocally r=+0.52 / rho=+0.40 from the sleep-window side). The sleep-window-mean and "
        "24h-window-mean stress are operationally distinct constructs even though biologically connected; "
        "they are NOT redundant in an HA covariate model.",
        "",
        "3. **`bb_lowest` is rho=-0.75** -- strong negative correlation, the strongest inverse-direction "
        "partner. Both are CONFIRMED-citalopram channels with opposite-direction priors (stress UP with "
        "dose; BB DOWN with dose). The rho=-0.75 magnitude reflects the shared autonomic-state structure "
        "(high stress days have low BB nadirs) and the shared citalopram-trajectory absorption; both "
        "effects superimpose. NOT near-identity but the closest inverse-direction neighbour.",
        "",
        "The cross-channel-correlation card's existing 7-channel panel "
        "([`cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md)) "
        "does NOT include this channel as a primary; the surfaced pair "
        "`all_day_stress_avg <-> bb_lowest` at rho=-0.75 is a candidate for inclusion at the next "
        "refresh (flag-only -- no card edits as part of this analysis per discipline).",
        "",
        "---",
        "",
        "## Q3.2.f -- Crash-day vs normal-day (Stratum 4 refresh in operationalisation-support framing)",
        "",
        f"Per CONVENTIONS section 3.6 named counts: {fe['n_crash_episodes']} crash-episodes (crash_v2 "
        f"episode-level via `labels_crash_v2.csv` unique `episode_id` starting with `crash-`); "
        f"{fl['n_crash_day']} crash-days (day-level, `label=='crash'`); {fl['n_normal_day']} non-crash "
        "days (the complement within Stratum 4 channel-valid days).",
        "",
        "### Episode-level (primary unit per CONVENTIONS section 3.6)",
        "",
        "| stat | value |",
        "|---|---:|",
        f"| n crash-episodes | {fe['n_crash_episodes']} |",
        f"| n normal-day base rate | {fe['n_normal_day_base_rate']} |",
        f"| mean per-episode `all_day_stress_avg` | {fe['mean_per_episode_stress']:.2f} |",
        f"| mean normal-day `all_day_stress_avg` | {fe['mean_normal_day_stress']:.2f} |",
        f"| mean diff (episode minus normal-day) | **{fe['mean_diff_episode_vs_normal_day']:+.2f}** |",
        f"| Cohen's d (episode-level vs normal-day pooled) | **{fe['cohens_d_episode_vs_normal_day']:+.2f}** |",
        f"| Bootstrap 95% CI on mean diff | **[{ci_ep[0]:+.2f}, {ci_ep[1]:+.2f}]** ({fe['n_bootstrap']} iters, seed={fe['seed']}) |",
        "",
        f"**The episode-level signal is WEAK on this channel.** Cohen's d={fe['cohens_d_episode_vs_normal_day']:+.2f} "
        "is **similar magnitude to `stress_low_motion_min_count_S60_Mlow` episode-level d=+0.38** (the "
        "count primitive's third-analysis Q3.x.f finding) but **substantially smaller than "
        "`stress_mean_sleep` d=+0.91** (the first-analysis Q3.1.f). The bootstrap 95% CI **brushes zero** "
        f"({ci_ep[0]:+.2f}, {ci_ep[1]:+.2f}); the episode-level signal does not robustly exclude zero on "
        f"this channel at the as-of-date {summary['as_of_date']} snapshot. Compare to `stress_mean_sleep` "
        "(CI [+1.58, +8.40], robust) and `stress_low_motion_min_count_S60_Mlow` (CI [+0.94, +34.88], just "
        "barely excluding zero).",
        "",
        "### Day-level (autocorrelation-inflated supplementary)",
        "",
        "| stat | value |",
        "|---|---:|",
        f"| n crash-days | {fl['n_crash_day']} |",
        f"| n normal-days | {fl['n_normal_day']} |",
        f"| mean crash-day | {fl['mean_crash']:.2f} |",
        f"| mean normal-day | {fl['mean_normal']:.2f} |",
        f"| median crash-day | {fl['median_crash']:.1f} |",
        f"| median normal-day | {fl['median_normal']:.1f} |",
        f"| mean diff (point estimate) | **{fl['mean_diff']:+.2f}** |",
        f"| median diff | **{mwu['median_diff']:+.1f}** |",
        f"| Cohen's d | **{fl['cohens_d']:+.2f}** |",
        f"| Mann-Whitney U: z | **{mwu['z']:+.2f}** |",
        f"| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **<0.0001** |",
        f"| Mann-Whitney U: P(crash > normal) | **{mwu['p_crash_greater_than_normal']:+.3f}** |",
        f"| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (project default) | [{e7['ci_lower']:+.2f}, {e7['ci_upper']:+.2f}], width {width7:.2f} |",
        f"| Stationary bootstrap 95% CI on mean diff, **E[L]={eS['block_length_used']}** (data-driven, Q3.2.b flag fired) | **[{eS['ci_lower']:+.2f}, {eS['ci_upper']:+.2f}]**, width {widthS:.2f} |",
        "",
        "### Mann-Whitney U as the heavy-tail-robust read",
        "",
        "Although this channel is NOT heavy-tail-flag-triggering (Q3.2.a), the Mann-Whitney U is reported "
        "for parity with the count-primitive third analysis (and as a rank-based robustness check on the "
        f"Cohen's d). **The day-level signal is unambiguously present**: z={mwu['z']:+.2f}, p<0.0001, "
        f"P(crash > normal) = {mwu['p_crash_greater_than_normal'] * 100:.1f}% (vs 50% null). The median "
        f"diff ({mwu['median_diff']:+.1f}) is equal to the within-population MAD on the channel "
        f"({a['mad_unscaled']:.1f}) -- a moderate effect at the day level that survives the rank-based "
        "robustness check.",
        "",
        f"**Read together with Cohen's d**: the channel carries a moderate positive shift on crash days "
        f"at the day level (d={fl['cohens_d']:+.2f}) that becomes weak at the episode level "
        f"(d={fe['cohens_d_episode_vs_normal_day']:+.2f}). This is the **expected within-episode-"
        "autocorrelation inflation** -- consecutive within-episode days are not independent observations; "
        f"the day-level d={fl['cohens_d']:+.2f} is the inflated read and the episode-level "
        f"d={fe['cohens_d_episode_vs_normal_day']:+.2f} is the unit-of-analysis-clean read. **The "
        f"unit-of-analysis-clean read does NOT robustly exclude zero** at the as-of-date snapshot; the "
        f"episode-level CI brushes zero ({ci_ep[0]:+.2f}, {ci_ep[1]:+.2f}). Consumer HAs using this "
        "channel as a crash-discriminator should report the episode-level (not the day-level) as the "
        "unit-of-analysis-clean read.",
        "",
        "### Block-length sensitivity (Q3.2.b cross-check)",
        "",
        "Per "
        "[`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md), "
        "when the data-driven E[L]\\* deviates from the project default by more than a factor of 2, the "
        "analysis must report the CI at the data-driven value alongside the default. Q3.2.b fired that "
        f"flag (E[L]\\*={el_star:.1f}, deviation ratio {b['deviation_ratio']:.2f} = factor-of-4). The "
        f"E[L]={eS['block_length_used']} CI ([{eS['ci_lower']:+.2f}, {eS['ci_upper']:+.2f}]) is "
        f"**{width_change_pct:+.1f}% wider** than the E[L]=7 CI ([{e7['ci_lower']:+.2f}, "
        f"{e7['ci_upper']:+.2f}]) -- the largest CI-width change across the three Strand A landed "
        "analyses' block-length sensitivity arms (sister stress_mean_sleep was +5%; count primitive was "
        "+10.5%). **Both block-length choices still exclude zero** on the day level, but the wider "
        f"data-driven CI's lower bound ({eS['ci_lower']:+.2f}) is much closer to zero than the project "
        f"default's ({e7['ci_lower']:+.2f}). At the episode level (which carries the unit-of-analysis-"
        "clean read), the CI brushes zero regardless of block-length choice.",
        "",
        "### Crash-drop sensitivity (CONVENTIONS section 3.4)",
        "",
        "| frame | Spearman rho | n |",
        "|---|---:|---:|",
        f"| full Stratum 4 | {cd['full_frame_value']:+.3f} | {cd['n_full']} |",
        f"| crash-days dropped | {cd['crash_dropped_value']:+.3f} | {cd['n_crash_dropped']} |",
        f"| \\|delta\\| | **{cd['abs_delta']:.3f}** | -- |",
        f"| section 3.4 threshold (0.10) crossed? | **{'yes' if cd['exceeds_threshold_0p10'] else 'no'}** | -- |",
        "",
        "The crash days **are doing some correlation work** in the channel-vs-gevoelscore pair (full "
        f"rho={cd['full_frame_value']:+.3f} moves to ~0 when crashes drop), but the magnitude is below "
        "the section 3.4 threshold. **No flag fires.** Same pattern as the count-primitive third "
        "analysis (full rho=-0.056 -> dropped +0.001 |delta|=0.057). The same-day channel-vs-gevoelscore "
        "correlation is essentially **zero on normal days** -- gevoelscore and 24h-mean-stress are "
        "**decoupled on normal days** at the daily resolution. This is consistent with the project's "
        "broader same-day-coupling observations across the three CONFIRMED-citalopram autonomic-load "
        "channels.",
        "",
        "See [`plots/fig4_crash_vs_normal.png`](plots/fig4_crash_vs_normal.png).",
        "",
        "---",
        "",
        "## Q3.2.g -- Spike-detecting primitive availability",
        "",
        "`all_day_stress_avg` is **structurally a 24h-window daily mean** (UDS-pre-aggregated; JSON-"
        "passthrough from `daily_uds.csv`; no FIT parsing per `garmin_indicators_audit.md` Wave-3 "
        "propagation 2026-06-12). Per CONVENTIONS section 3.5 it is the **dilution-vulnerable continuous "
        "form** of the autonomic-load construct; the spike-form companion "
        "`stress_low_motion_min_count_S60_Mlow` (Phase-1 third analysis) carries spike-during-rest "
        "information beyond this daily mean. Sub-daily resolution is **not in `per_day_master.csv`** for "
        "this channel's exact form; latent in monitoring_b FIT files.",
        "",
        "Spike-related primitives in the master (24h-window):",
        "",
        "| column | DATA_DICTIONARY | n_non_nan (S4) | type | relation to `all_day_stress_avg` |",
        "|---|---|---:|---|---|",
        f"| `all_day_stress_max` | [section 7B](../../../DATA_DICTIONARY.md) | 1359 | daily peak stress value (24h) | Pearson r=**{g.get('pearson_r_vs_all_day_stress_max', 0):+.2f}** / rho={g.get('spearman_rho_vs_all_day_stress_max', 0):+.2f}; partial overlap (peak vs mean) |",
        f"| `max_spike_minutes` | [section 8](../../../DATA_DICTIONARY.md) | 1364 | longest contiguous run of stress>=75 lasting >=5min in 24h | Pearson r=**{g.get('pearson_r_vs_max_spike_minutes', 0):+.2f}** / rho={g.get('spearman_rho_vs_max_spike_minutes', 0):+.2f}; moderate overlap (peak-duration vs mean) |",
        "| `stress_high_duration_min` | [section 8B C4](../../../DATA_DICTIONARY.md) | 1364 | total 24h minutes at high-stress threshold per FIT extraction | (not paired here, but logically related to spike-form) |",
        f"| `stress_low_motion_min_count_S60_Mlow` | [section 8C](../../../DATA_DICTIONARY.md) | 1365 | minute-level count of low-motion-high-stress windows (24h) | Pearson r=**{g.get('pearson_r_vs_stress_low_motion_min_count_S60_Mlow', 0):+.2f}** / rho={g.get('spearman_rho_vs_stress_low_motion_min_count_S60_Mlow', 0):+.2f} -- the spike-form companion per CONVENTIONS section 3.5 |",
        "",
        "### CONVENTIONS section 3.5 framing -- the continuous-vs-spike pair on this channel",
        "",
        "The third Phase-1 Strand-A analysis "
        "([`stress_low_motion_min_count_S60_Mlow`](../stress_low_motion_min_count_S60_Mlow/findings.md) "
        "Q3.x.g) explicitly named THIS channel as its **continuous-form cousin** per CONVENTIONS section "
        "3.5; this analysis reciprocally names `stress_low_motion_min_count_S60_Mlow` as the **spike-form "
        "companion**. The cross-pair correlation r=+0.85 / rho=+0.86 (reciprocally confirmed on both "
        "sides) characterises the \"general autonomic load throughout the day\" vs \"acute spike at "
        "rest\" construct pair:",
        "",
        "- A future HA whose mechanism is **acute spike-at-rest** should use "
        "`stress_low_motion_min_count_S60_Mlow` as primary, NOT this channel as primary -- this channel "
        "dilutes the within-day spike density across all 480+ samples.",
        "- A future HA whose mechanism is **general autonomic load throughout the day** should use this "
        "channel as primary, NOT the count primitive -- the count primitive's threshold-counting "
        "collapses level information into binary above/below decisions.",
        "- Both channels enter a future HA as separate constructs (their r=+0.85 IS NOT near-identity at "
        "the section 3.3 threshold); the spike-vs-mean disambiguation belongs in the HA's covariate-"
        "sensitivity arm (per Q3.2.i below).",
        "",
        f"`all_day_stress_max` is the in-master 24h-peak; `max_spike_minutes` is the in-master longest-"
        f"spike-duration. Both are weakly-to-moderately related to this channel "
        f"(r={g.get('pearson_r_vs_all_day_stress_max', 0):+.2f} and "
        f"r={g.get('pearson_r_vs_max_spike_minutes', 0):+.2f} respectively) -- they carry independent "
        "peak-and-duration information that this channel's 24h mean averages out. A consumer test "
        "wanting the \"high water mark\" of the day should use `all_day_stress_max`; a test wanting the "
        "\"longest contiguous spike\" should use `max_spike_minutes`.",
        "",
        "**Latent in FIT, not in master**: per-minute monitoring_b stress samples (raw ~3-min cadence; "
        "the source of all UDS aggregates). Building a customised within-day stress-density primitive at "
        "finer-than-daily resolution is a queued extraction task; this analysis does NOT action it.",
        "",
        "---",
        "",
        "## Q3.2.h -- Outlier detection + calibration-drift check",
        "",
        "Per "
        "[`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md):",
        "",
        "- This channel is a **Wave-3 JSON-side passthrough** (2026-06-12) from `daily_uds.csv`; no FIT "
        "parsing needed. One of 5 all-day stress columns extracted in the Wave-3 batch (also: "
        "`all_day_stress_max`, `awake_stress_avg`, `asleep_stress_avg_uds`, and one count companion).",
        "- **No specific calibration-drift events catalogued for `all_day_stress_avg`** in "
        "`garmin_indicators_audit.md`; the audit's per-column provenance map covers it under the Wave-3 "
        "passthrough bullet rather than as its own row.",
        "- Underlying sensor is **Forerunner 245 Elevate V3 throughout the entire 2021-08-16 to present "
        "window** -- no device change in the analytic window.",
        "",
        "### Outlier scan (MAD-based |z|>5; threshold per CONVENTIONS section 3.1 robust-baseline default)",
        "",
        f"**{len(outliers)} outlier-day flagged** out of {a['n']}:",
        "",
        "| date | value | MAD-z | likely category |",
        "|---|---:|---:|---|",
        *[
            f"| {o['date']} | {o['value']:.1f} | **{o['mad_z']:+.2f}** | global max; same date is the global max for `stress_mean_sleep` (Q3.1.h) AND for `stress_low_motion_min_count_S60_Mlow` (Q3.x.h global max at 361 min/day); the **named peak-crash exemplar day** per [`garmin_exploration/stress_low_motion_viz/family_a_daily.py`](../../../analyses/garmin_exploration/stress_low_motion_viz/family_a_daily.py) |"
            for o in outliers
        ],
        "",
        "**The single outlier is NOT an artefact**: 2023-11-29 is the same date that fires as the global "
        "max on `stress_mean_sleep` (value 72.99, MAD-z +12.64) and on "
        "`stress_low_motion_min_count_S60_Mlow` (value 361 min/day, MAD-z +7.12). Three independent "
        "autonomic channels all spike together on this date -- a clear **cross-channel-consistent real "
        "stress event**, not a sensor failure. The day is also a named exemplar in the stress_low_motion "
        "within-day visualisation work. Downstream HA tests should NOT trim this date; it is part of the "
        "channel's natural shape.",
        "",
        "The fact that THIS channel flags ONLY 1 outlier at the |z|>5 threshold (vs 16 on "
        "`stress_mean_sleep` and 6 on `stress_low_motion_min_count_S60_Mlow`) is consistent with Q3.2.a's "
        "heavy-tail-flag = FALSE finding: the 24h-window mean dilutes spike-day signals more than the "
        "other two channels, so the upper tail is more compressed and the |z|>5 outlier rule fires less "
        "often. The single firing day is the most extreme cross-channel-consistent event; lesser stress-"
        "spike days on the other two channels are absorbed into this channel's body distribution.",
        "",
        "### Drift check -- rolling 90d median over Stratum 4",
        "",
        "| snapshot date | rolling 90d median |",
        "|---|---:|",
        *[
            f"| {s['snapshot_date']} | {s['rolling_med_90d']:.1f} |"
            for s in h["rolling_90d_median_snapshots"] if s["rolling_med_90d"] is not None
        ],
        "",
        "The rolling 90d median exhibits a **clear multi-year shift** at the citalopram boundary: ~34.0-"
        "34.5 throughout the unmedicated era (2022-12 through 2023-12); ~29-30 throughout the "
        "consolidation era (2024-06 onward). The ~5-unit shift (~1.25 channel-MADs) over a ~6-month "
        "window centred on the 2024-04-09 citalopram boundary is the largest single-event step in the "
        f"channel's history per this analysis. The **consolidation-boundary step at 2024-06-20** (entry "
        f"into 30mg steady-state) shows trailing-30d mean = {consol_step['pre_30d_mean']:.2f}, leading-"
        f"30d mean = {consol_step['post_30d_mean']:.2f} -- a **{consol_step['diff_post_minus_pre']:+.2f} "
        "step**, well within MAD; the consolidation boundary specifically does NOT register a sharp step "
        "(the shift had already happened by the citalopram-axis boundary 2024-04-09). The **citalopram-"
        f"axis boundary 2024-04-09 step** shows trailing-30d mean = {citalo_step['pre_30d_mean']:.2f}, "
        f"leading-30d mean = {citalo_step['post_30d_mean']:.2f} -- a "
        f"**{citalo_step['diff_post_minus_pre']:+.2f} step**, "
        f"~{abs(citalo_step['diff_post_minus_pre']) / a['mad_unscaled']:.1f} channel-MADs -- THIS is the "
        "empirical day-resolved shift driving the longer 90d-window pattern.",
        "",
        "**This is NOT a calibration-drift signature** -- the shift is precisely time-located at a "
        "documented intervention boundary (citalopram dose ramp begins 2024-04-09), and the channel "
        "recovers fully during afbouw (per Q3.2.c). A calibration-drift signature would be a gradual "
        "monotonic creep unrelated to documented events; this is the opposite -- a sharp drop at the "
        "boundary with full recovery at the reverse boundary.",
        "",
        "### `garmin_indicators_audit.md` row proposal (PROPOSE-ONLY)",
        "",
        "[`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) does "
        "NOT yet have a per-column row for the all-day stress family (5 columns: `all_day_stress_avg`, "
        "`all_day_stress_max`, `awake_stress_avg`, `asleep_stress_avg_uds`, and the in-master count "
        "companion); only the Wave-3 passthrough bullet aggregates them. **Proposed row content** (do "
        "NOT apply as part of this analysis per handoff section 3 / discipline):",
        "",
        "> Channel family: `all_day_stress_avg`, `all_day_stress_max`, `awake_stress_avg`, "
        "`asleep_stress_avg_uds` (4 columns from `daily_uds.csv` Wave-3 passthrough 2026-06-12). "
        "Upstream extractor: JSON-side propagation in `pipeline/03_consolidate/build_unified_dataset.py`. "
        "Source: `daily_uds.csv` from Garmin's UDS pre-aggregated stress fields. Day-validity gate: NaN "
        "when UDS missing the field on the day (~1% of S4 days). Sentinel handling: UDS-side cleaning "
        "happens upstream of this channel's appearance in the master. Calibration: no documented drift "
        "events; sharp -7.2 step at 2024-04-09 citalopram boundary, +5 step recovery at 2026-03-20 "
        "afbouw boundary -- both are documented intervention effects, NOT drift (added 2026-06-24 per "
        "descriptive `all_day_stress_avg/findings.md` Q3.2.h). Device: Forerunner 245 Elevate V3 "
        "throughout 2021-08-16 to present (no device change).",
        "",
        "Surface to user for authorisation in a separate session per the discipline.",
        "",
        "See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).",
        "",
        "---",
        "",
        "## Q3.2.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel",
        "",
        "Discipline anchor: "
        "[HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) "
        "(secondary-logistic-with-covariate pattern; beta disambiguation between primary-signal and a "
        "candidate alternative reading). Names **four** candidate covariates a future HA on "
        "`all_day_stress_avg` as predictor should pre-spec:",
        "",
        "### 1. `dose_plasma_mg(d)` -- obligatory under "
        "[`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5.B",
        "",
        "The channel is CONFIRMED dose-modulated at +0.565/mg p=0.000 (the LARGEST beta among the 3 "
        "CONFIRMED channels). A future HA MUST either section 5.A per-phase stratify or section 5.B "
        "dose-adjust. **HA-C3 v2 and HA-C3p both used the dual treatment** (section 5.A unmedicated "
        "headline as primary + section 5.B dose-adjusted cross-phase as sensitivity arm); both pre-regs' "
        "section 5.B sensitivity arms returned REJECTED at 0-of-3 conditions MET, while the section 5.A "
        "unmedicated headline carried the substantive verdicts (HA-C3 v2 REJECTED via wrong-direction "
        "override; HA-C3p PARTIAL). The operational consequence: **the section 5.A unmedicated headline "
        "is the load-bearing operationalisation choice** for HAs probing non-linearity or shape on this "
        "channel; the section 5.B numerical adjustment does NOT recover the unmedicated-pool inverted-U "
        "pattern. The covariate version (secondary logistic adding `dose_plasma_mg(d)` to a primary-"
        "channel logistic) is the framework-prescribed disambiguator for HAs that pool cross-phase.",
        "",
        "Needed columns: `lc_phase` is in the master; `dose_plasma_mg(d)` is computed runtime per "
        "[`citalopram_dose_response/dose_response.py`](../../../analyses/garmin_exploration/intervention_effects/dose_response.py).",
        "",
        "### 2. `stress_mean_sleep` -- sister CONFIRMED-citalopram channel (autonomic-load shared)",
        "",
        f"On Stratum 4 observed (this analysis Q3.2.e, n=1339): Pearson r=+0.522, Spearman rho=+0.404 "
        "between `all_day_stress_avg` and `stress_mean_sleep`. Sister CONFIRMED-citalopram channel "
        "(+0.43/mg beta on sleep-window stress mean vs +0.57/mg on this channel's 24h mean). Both load "
        "on the same autonomic-load family per dose-response v3 section 5.6.2 (autonomic-load axis: 24h "
        "mean + sleep-window mean both confirmed). The covariate disambiguates: is the all-day signal "
        "specifically driven by the **awake portion of the day** (beta_channel survives when sleep-mean "
        "enters) or by **shared autonomic tone** (beta_channel attenuates). The sleep-window vs 24h-"
        "window split IS the operational disambiguation.",
        "",
        "### 3. `stress_low_motion_min_count_S60_Mlow` -- spike-form companion per CONVENTIONS section 3.5",
        "",
        "On Stratum 4 observed (this analysis Q3.2.e, n=1358): Pearson r=+0.847, Spearman rho=+0.860 "
        "-- high but NOT near-identity. The covariate disambiguates: is the all-day stress signal driven "
        "by the **temporal density of above-threshold minutes** (beta_channel attenuates -- spike-count "
        "was doing the work) or by the **average level** (beta_channel survives -- the daily mean carries "
        "information beyond threshold-crossing count). This is the **spike-vs-mean disambiguator per "
        "CONVENTIONS section 3.5**.",
        "",
        "### 4. `all_day_stress_avg_lagged_mean_14d(d) = mean(channel[d-14:d-1])` -- autocorrelation-vs-mechanism",
        "",
        f"Mirrors HA-P7 section 4.5.4 worked example. Per Q3.2.b the cutoff lag M={b['cutoff_lag_M']} and "
        f"E[L]\\*={el_star:.1f}; **the channel's autocorrelation horizon is LONGER than both sister "
        f"channels' (12.6 sleep-mean; 21.1 count primitive)**, so a 14d lagged trailing mean is **NOT "
        f"past the autocorrelation horizon** for this primitive. A consumer HA should prefer a **{el_int}d "
        f"or 28d window** for this covariate on this channel specifically -- the descriptive substrate "
        f"says the autocorrelation extends to ~M={b['cutoff_lag_M']} cutoff, so the consumer-test pre-reg "
        f"has discretion to set the window past the M cutoff with margin (~28-{el_int}d is the natural "
        "choice).",
        "",
        "Reconciliation with CONVENTIONS section 3.2 `_lagged_lcera` family: `all_day_stress_avg` is "
        "**not** currently in the section 3.2 audit-hook list and has no `_lagged_lcera` materialised "
        "variant in `per_day_master.csv` as of 2026-06-24. The lagged-mean-14d covariate is a same-day-"
        "HA diagnostic built just past Q3.2.b's M cutoff; it does NOT substitute for section 3.2's longer "
        "trailing baseline window, which belongs in the HA's own z-scoring or covariate-adjustment layer.",
        "",
        "### Recommendation for any HA pre-reg on this channel",
        "",
        "Pre-spec all four covariates as **secondary sensitivity arms**. Concordance across the four "
        "secondaries = high confidence in the primary; divergence = the disambiguation is doing real "
        "work. The section 5.B citalopram-dose adjustment is **obligatory** per the framework AND per "
        "the HA-C3 cluster's load-bearing precedent (both HA-C3 v2 + HA-C3p locked dual section 5.A + "
        "section 5.B treatment); the other three are diagnostic. Per the **HA-C3 cluster's joint "
        "inverted-U finding**: HAs probing non-linearity on this channel should follow the HA-C3p "
        "result.md section 4 sensitivity-table template (section 5.A unmedicated headline + section 5.B "
        "dose-adjusted + z-score sensitivity + crash-drop + train/validate descriptive overlay + t+1 "
        "lagged variant).",
        "",
        "---",
        "",
        "## Cross-references",
        "",
        "### HA-* tests that touch this channel (cite this analysis)",
        "",
        "- **HA-C3 v2** (REJECTED at `a2b18ba` 2026-06-23, wrong-direction override): primary user of "
        "this channel as predictor (Wiggers-verbatim 30->40 anchor bin scheme). The descriptive substrate "
        "this analysis produces is the **load-bearing substrate for the HA's section 5.A unmedicated "
        "headline operationalisation choice** (per Q3.2.c quintile-bin distribution reproducing HA-C3p's "
        "right-shift observation + Q3.2.d phase-stratified medians documenting the citalopram-axis "
        f"dynamics + Q3.2.b E[L]\\*={el_star:.1f} contextualising the HA's bin-label-sequence E[L]\\* "
        "derivation). The HA's REJECTED verdict via wrong-direction override is NOT extended or promoted "
        "by this analysis per CONVENTIONS section 2.1.",
        "- **HA-C3p** (PARTIAL at `e5a63fe` 2026-06-23): sister pre-reg testing the underlying convex-"
        "shape claim on personal-baseline-anchored quintile bins. The descriptive substrate this "
        f"analysis produces **reproduces HA-C3p's section 2 right-shift unmedicated bin observation "
        f"EXACTLY** (Q3.2.c quintile counts {cq['unmedicated_bin_counts']}) and extends it with share-"
        f"ratio quantification (Q5 unmed/full = {cq['share_ratio_unmedicated_over_full_pool'][4]:.2f}). "
        "The HA-C3p PARTIAL verdict + 4-cell-matrix consolidated reading (\"Wiggers' numbers wrong-for-"
        "this-participant but the underlying SHAPE IS REAL in the INVERSE direction\") is NOT extended "
        "or promoted by this analysis.",
        "- **HA-P6 v3** (descriptive Layer 1): includes this channel in its 7-channel set as the "
        f"distinguishable channel from Arm-A matched control. The descriptive substrate this analysis "
        f"produces (E[L]\\*={el_star:.1f} longer than any sister; episode-level crash signal CI brushing "
        "zero; sharp citalopram-boundary step + full afbouw recovery) provides context for the HA-P6 "
        "result reading on this specific channel.",
        "- **HA-C4 v2** (REJECTED at `52bddb5` 2026-06-18): primary daily-aggregate triad on the 3 "
        "CONFIRMED-citalopram autonomic channels (including this one as Ch1). The descriptive substrate "
        f"this analysis produces (episode-level d={fe['cohens_d_episode_vs_normal_day']:+.2f} with CI "
        "brushing zero) constrains the post-rejection re-interpretation: did this channel specifically "
        "lack signal at the episode level on the v2-locked operationalisation? **This analysis confirms "
        f"YES** -- the channel does NOT carry a robust episode-level signal at as-of-date "
        f"{summary['as_of_date']} with E[L]=7 OR E[L]={eS['block_length_used']}; the day-level signal "
        "exists but autocorrelation-inflated.",
        "",
        "### Methodology MDs cited",
        "",
        "- [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) -- "
        "Q3.2.a delegate target (partial; extended for the full skewness/kurtosis/heavy-tail-flag set on "
        "this channel).",
        "- "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "sections 3-6 -- Q3.2.c phase axis, Q3.2.d phase-stratified treatment, Q3.2.i covariate framework.",
        "- "
        "[`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "v3 section 5.6.1 -- locked +0.565/mg dose-response slope (largest beta among 3 CONFIRMED "
        "channels); section 5.6.2 autonomic-load family.",
        "- "
        "[`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) "
        "-- E[L]=7 default + factor-of-2 deviation rule; Q3.2.b fires factor-of-4 (the largest deviation "
        "in Strand A).",
        "- "
        "[`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) -- "
        "Q3.2.h cross-reference; **per-column row for all-day stress family is missing** (PROPOSE-ONLY).",
        "- "
        "[`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) "
        "-- Stratum 4 boundary definition.",
        "",
        "### Existing artefacts referenced",
        "",
        "- "
        "[`descriptive/operationalisation_support/stress_mean_sleep/findings.md`](../stress_mean_sleep/findings.md) "
        f"-- sister CONFIRMED-citalopram channel; first Phase-1 Strand A analysis; cross-channel "
        f"comparison anchors throughout (E[L]\\* {el_star:.1f} here vs 12.6 there; episode-level d "
        f"{fe['cohens_d_episode_vs_normal_day']:+.2f} here vs +0.91 there; heavy-tail-flag "
        f"{a['heavy_tail_flag']} here vs True there).",
        "- "
        "[`descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/findings.md`](../stress_low_motion_min_count_S60_Mlow/findings.md) "
        "-- spike-form companion per CONVENTIONS section 3.5; third Phase-1 Strand A analysis; cross-"
        "pair r=+0.85 / rho=+0.86 reciprocally confirmed; the continuous-vs-spike pair on this channel.",
        "- [`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/) -- v2 LANDED "
        "2026-06-22 (`8feae6a`); the afbouw-reversal finding per section 5.A sub-stratification cross-"
        "references the Q3.2.c + Q3.2.d afbouw-median recovery observation on this channel.",
        "- [`analyses/hypotheses/HA-C3/result.md`](../../hypotheses/HA-C3/result.md) -- HA-C3 v2 "
        "REJECTED 2026-06-23; primary user of this channel.",
        "- [`analyses/hypotheses/HA-C3p/result.md`](../../hypotheses/HA-C3p/result.md) -- HA-C3p PARTIAL "
        "2026-06-23; right-shift section 2 observation reproduced + extended in Q3.2.c.",
        "- "
        "[`analyses/garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) "
        "-- Q3.2.e cross-reference; new near-miss pair `all_day_stress_avg <-> bb_lowest` rho=-0.75 "
        "surfaced for next refresh (flag-only).",
        "- "
        "[`analyses/garmin_exploration/stress_low_motion_viz/family_a_daily.py`](../../../analyses/garmin_exploration/stress_low_motion_viz/family_a_daily.py) "
        "-- the 2023-11-29 named-exemplar peak-crash day that fires as this channel's sole MAD-z>5 "
        "outlier (Q3.2.h).",
        "",
        "### Upstream pipeline",
        "",
        "- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `daily_uds.csv` "
        "(Wave-3 JSON-side passthrough 2026-06-12 per `garmin_indicators_audit.md`). NO custom FIT "
        "extraction for this channel.",
        "- `labels_crash_v2.csv` <- `garmin/hypotheses/crash_v2-definition/definition.md` (locked).",
        "",
        "---",
        "",
        "## Limitations",
        "",
        "For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per "
        "[CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding "
        "limitations a downstream HA pre-reg author should carry forward are:",
        "",
        "1. **Q3.2.c-d are on raw channel values, not dose-adjusted.** Per "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 5, any HA using `all_day_stress_avg` cross-phase MUST adopt section 5.A / 5.B / 5.C "
        "treatment. The HA-C3 cluster's load-bearing precedent (both v2 + HA-C3p) is dual section 5.A "
        "unmedicated headline + section 5.B dose-adjusted sensitivity. Q3.2.d explains the citalopram-"
        "axis dynamics descriptively; a section 5.B dose-adjusted phase comparison is the natural "
        "follow-up but lives in the HA pre-reg, not here.",
        "2. **The channel IS a 24h-window daily mean** (Q3.2.g) per CONVENTIONS section 3.5 -- dilution-"
        "vulnerable for acute-load mechanisms. A future HA whose mechanism is *acute spike-during-rest* "
        "should use `stress_low_motion_min_count_S60_Mlow` (the spike-form companion at r=+0.85 / "
        "rho=+0.86) as primary; this channel is the continuous-form cousin.",
        f"3. **The episode-level Cohen's d={fe['cohens_d_episode_vs_normal_day']:+.2f} has bootstrap CI "
        f"brushing zero** (Q3.2.f). The episode-level is the unit-of-analysis-clean read per CONVENTIONS "
        f"section 3.6; consumer HAs using this channel as a crash-discriminator should NOT rely on the "
        f"day-level d={fl['cohens_d']:+.2f} (autocorrelation-inflated) as the primary read. The signal "
        f"exists but is weak at the episode level on this corpus at as-of-date {summary['as_of_date']}.",
        f"4. **The autocorrelation horizon is the LONGEST in Strand A** (Q3.2.b E[L]\\*={el_star:.1f} "
        "vs 12.6 sleep-mean / 21.1 count primitive). Consumer tests using this channel with auto-"
        "correlation-controlled methods MUST use a longer block-length than the project default; the "
        "factor-of-4 deviation is the largest yet observed. The HA-C3 cluster's bin-label-sequence "
        "E[L]\\* derivation (=7.0, \"no flags\") is a different frame; both are correct in their "
        "respective frames (raw channel vs binned derivative).",
        "5. **The outlier-rule MAD-z|>5 is a descriptive-stage screen** (Q3.2.h) -- the single firing "
        "day (2023-11-29) is the cross-channel-consistent peak-crash exemplar; downstream HA tests must "
        "NOT trim it.",
        f"6. **The afbouw-recovery finding is descriptively striking but Layer-1 only**: afbouw median "
        f"{c['afbouw']['median']:.1f} = unmedicated median {c['unmedicated']['median']:.1f} exactly. The "
        "substantive afbouw-reversal interpretation lives in `recovery_arc v2` analysis "
        "([`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/) section 5.A); this "
        "analysis's Q3.2.d corroborates it descriptively but does NOT extend or promote the substantive "
        "reading.",
        "7. **The `garmin_indicators_audit.md` per-column row for the all-day stress family is missing** "
        "(Q3.2.h). Proposed row content surfaced; do NOT apply without user authorisation per handoff "
        "discipline section 3.",
        "8. **The HA-C3 cluster verdicts are LOCKED at REJECTED + PARTIAL with consolidated joint "
        "reading.** This analysis's Q3.2.c quintile-bin reproduction + Q3.2.d phase-stratified "
        "observation are **descriptive corroboration only**; the HA-C3 cluster's inverted-U finding is "
        "NOT extended by this analysis per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). "
        "Future HA-C3 v3 / HA-C3p v2 alternative-shape pre-regs would be a separate authorship session "
        "per `hypothesis_lock_process.md` section 3.2 redraft discipline.",
        "",
        "---",
        "",
        "## Status",
        "",
        "**Current as of 2026-06-24** (commit context: post-`ccbd12e` descriptive programme lock; Phase "
        "2 \"finish the descriptive analysis\" Tier 1 user-prioritised CONFIRMED-citalopram channel #2; "
        "R14 `single_pool_reanchor` landed first at `badd04a`; `bb_lowest` next). Refresh when:",
        "",
        "1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to "
        "spin up (per CONVENTIONS section 3.1 personal-baseline freshness).",
        "2. A new citalopram-phase boundary lands (e.g. post-afbouw enters analytic scope as of "
        "2026-06-06 onward).",
        f"3. The Politis-White E[L]\\* shifts by another factor of 2 from current {el_star:.1f} "
        "(factor-of-4-vs-default flag already fired).",
        "4. The `all_day_stress_avg <-> bb_lowest` near-miss pair (Q3.2.e rho=-0.75) gets propagated "
        "into the cross-channel-correlation card's 7-channel panel.",
        "5. The `garmin_indicators_audit.md` per-column row for the all-day stress family gets added "
        "with the proposed content (Q3.2.h flag).",
        "6. An HA-C3 v3 / HA-C3p v2 alternative-shape pre-reg spins up and surfaces new operationalisation "
        "choices on this channel that would change the per-channel descriptive substrate.",
        "",
    ]
    path.write_text("\n".join(out_lines), encoding="utf-8")


def write_readme_md(summary: dict, path: Path) -> None:
    """Emit the per-analysis README per descriptive/README section 7a pattern.

    Mirrors the Phase-1 precedent shapes (stress_mean_sleep + count primitive).
    """
    q = summary["questions"]
    a = q["Q3.2.a_distribution"]
    b = q["Q3.2.b_autocorrelation"]
    c = q["Q3.2.c_base_rates_per_phase"]
    cq = q["Q3.2.c_quintile_bin_distribution"]
    fr = q["Q3.2.f_crash_vs_normal"]
    fe = fr["episode_level"]
    el_star = b["data_driven_E_L_star"]
    out_lines = [
        "# `all_day_stress_avg` -- operationalisation-support descriptive analysis",
        "",
        "**Strand**: A (operationalisation support; template-driven; no operationalisation interview "
        "required per [`descriptive/README.md`](../../README.md) section 7b).",
        "",
        "## Research question",
        "",
        "Operationalisation-support descriptive characterisation of `all_day_stress_avg` on Stratum 4, "
        "answering Q3.2.a-i per the locked descriptive programme spec at "
        "[`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.2 (LOCKED 2026-06-18 "
        "r3, commit `ccbd12e`). Phase 2 \"finish the descriptive analysis\" Tier 1 user-prioritised "
        "sequential batch; **second of the 3 CONFIRMED-citalopram channels** (R14 `single_pool_reanchor` "
        "landed first at `badd04a`; `bb_lowest` next). This channel is the **CONFIRMED-citalopram "
        "channel with the largest beta** (+0.565/mg p=0.000 buildup post-CPAP per "
        "[`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "section 5.6.1; sister stress_mean_sleep +0.43/mg; bb_lowest -1.13/mg inverse direction); "
        "**primary predictor in the HA-C3 v2 REJECTED + HA-C3p PARTIAL cluster** (2026-06-23) which "
        "jointly detected an inverted-U / concave non-linearity on this channel; also present in HA-P6 "
        "v3's 7-channel distinguishable-channel set.",
        "",
        "## Method",
        "",
        f"- **Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to {summary['as_of_date']}; "
        f"n={a['n']} channel-valid days out of {summary['n_rows_stratum_4_total']} S4 days).",
        "- **Primary phase axis**: four-phase citalopram traject per "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with the stress_mean_sleep "
        "first analysis.",
        "- **Delegate**: Q3.2.a (distribution shape) **partial delegate** to "
        "[`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) + "
        "**extend** with full skewness/kurtosis/heavy-tail-flag descriptors (the delegate target was "
        "extended for continuous channels first and primarily documents `stress_mean_sleep`).",
        "- **Cross-reference**: Q3.2.h (outliers + calibration-drift) cross-references "
        "[`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md); "
        "**the audit MD does NOT yet have a per-column row for the all-day stress family** (proposed "
        "row content surfaced in findings.md Q3.2.h; PROPOSE-ONLY per handoff section 3).",
        "- **Computed directly from `per_day_master.csv`**: Q3.2.b (Politis-White E[L]\\*), Q3.2.c "
        "(per-phase base rates + HA-C3p quintile-bin reproduction), Q3.2.d (phase-stratified medians + "
        "citalopram step magnitude vs +0.565/mg recalibration anchor), Q3.2.e (near-identity check "
        "|rho|>=0.92), Q3.2.f (crash-vs-normal Cohen's d + Mann-Whitney U + stationary-bootstrap CI at "
        "E[L]=7 and E[L]\\*~30 + crash-drop sensitivity per section 3.4), Q3.2.g (spike-primitive "
        "availability + continuous-vs-spike pair with `stress_low_motion_min_count_S60_Mlow`), Q3.2.i "
        "(covariate-sensitivity readiness for future HA pre-regs).",
        "- **Shared utilities**: "
        "[`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-drop "
        "sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) "
        "(`compute_data_driven_block_length`, `stationary_bootstrap_ci`).",
        "- **HA-C3 cluster cross-references** (load-bearing per handoff section 2.4): findings.md "
        "descriptively reproduces HA-C3p's right-shift unmedicated bin observation (Q3.2.c); "
        "descriptively corroborates the HA-C3 cluster's inverted-U finding via predictor-side mass-"
        "distribution observation (Q3.2.d); anchors phase-stratified discussion on the locked +0.565/mg "
        "recalibration anchor (Q3.2.d); contextualises this channel's E[L]\\* against sister Phase-1 "
        "channels (Q3.2.b). NO substantive HA verdict promotion per CONVENTIONS section 2.1.",
        "- **No causal claims, no falsification bar** per "
        "[CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).",
        "",
        "## Result",
        "",
        "Headline (see [`findings.md`](findings.md) for the full answers Q3.2.a-i):",
        "",
        f"`all_day_stress_avg` on Stratum 4 is a **mildly right-skewed, autocorrelation-DENSE 24h-window "
        f"daily-mean channel** (skew={a['skewness']:+.2f}, excess kurtosis={a['excess_kurtosis']:+.2f}; "
        f"**NOT heavy-tail-flag-triggering** unlike sister `stress_mean_sleep`). **Data-driven "
        f"E[L]\\*={el_star:.1f}** -- factor-of-4 above project default; **the LONGEST E[L]\\* yet "
        "observed in Strand A** (vs `stress_mean_sleep` 12.6 / `stress_low_motion_min_count_S60_Mlow` "
        f"21.1). **Phase-stratified medians shift sharply at the citalopram boundary** "
        f"({c['unmedicated']['median']:.1f} unmedicated to {c['buildup']['median']:.1f} buildup; "
        f"~-5.5 median; ~-1.8 buildup-MAD) and **recover fully during afbouw** "
        f"({c['afbouw']['median']:.1f} afbouw = {c['unmedicated']['median']:.1f} unmedicated). Day-"
        "resolved citalopram-boundary step (2024-04-09 pre/post 30d) is -7.2 stress units. Crash-vs-"
        f"normal: episode-level d={fe['cohens_d_episode_vs_normal_day']:+.2f} with bootstrap CI "
        f"**brushing zero** [{fe['bootstrap_ci95_mean_diff'][0]:+.2f}, "
        f"{fe['bootstrap_ci95_mean_diff'][1]:+.2f}] -- WEAK episode-level signal; day-level Mann-Whitney "
        f"U fires robustly (z=+4.30, p<0.0001). **Zero near-identity pairs** at |rho|>=0.92; closest is "
        f"`awake_stress_avg` rho=+0.887 (just below). **The HA-C3p right-shift unmedicated bin "
        f"observation is REPRODUCED EXACTLY** at the locked quintile boundaries (unmed counts "
        f"{cq['unmedicated_bin_counts']} n={cq['unmedicated_n']}); the unmedicated stratum carries "
        f"{cq['share_ratio_unmedicated_over_full_pool'][4]:.2f}x the full-pool share of Q5 mass "
        f"({cq['share_ratio_unmedicated_over_full_pool'][4] / cq['share_ratio_unmedicated_over_full_pool'][0]:.1f}"
        f"x the full-pool share of Q1 mass) -- an extension of the HA-C3p descriptive observation to a "
        "share-ratio quantification. The `garmin_indicators_audit.md` per-column row for the all-day "
        "stress family is **missing** -- proposed row content surfaced in findings.md Q3.2.h for "
        "separate user authorisation.",
        "",
        "## Files",
        "",
        "- [`README.md`](README.md) -- this file",
        "- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + "
        "`README.md` + `plots/*.png`",
        "- [`findings.md`](findings.md) -- writeup covering Q3.2.a-i + tables (programmatically emitted "
        "by run.py from summary.json)",
        "- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per "
        "`docs/research/**/*.json`)",
        "- [`plots/`](plots/) -- 5 PNGs: distribution, phase-stratified violins (citalopram axis), "
        "trajectory-with-phases, crash-vs-normal, ACF (gitignored per `docs/research/**/*.png`)",
        "",
        "## Status",
        "",
        "**Current as of 2026-06-24** (commit context: post-`ccbd12e` descriptive programme lock; Phase "
        "2 \"finish the descriptive analysis\" Tier 1 user-prioritised CONFIRMED-citalopram channel #2; "
        "R14 `single_pool_reanchor` landed first at `badd04a`; `bb_lowest` next). Refresh when:",
        "",
        "1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to "
        "spin up.",
        "2. A new citalopram-phase boundary lands (e.g. post-afbouw enters analytic scope as of "
        "2026-06-06 onward).",
        f"3. The Politis-White E[L]\\* shifts by another factor of 2 from current {el_star:.1f} "
        "(factor-of-4-vs-default flag already fired).",
        "4. The `all_day_stress_avg <-> bb_lowest` near-miss pair (Q3.2.e rho=-0.75) gets propagated "
        "into the cross-channel-correlation card's 7-channel panel.",
        "5. The `garmin_indicators_audit.md` per-column row for the all-day stress family gets added "
        "with the proposed content (Q3.2.h flag).",
        "6. An HA-C3 v3 / HA-C3p v2 alternative-shape pre-reg spins up and surfaces new operationalisation "
        "choices on this channel that would change the per-channel descriptive substrate.",
        "",
        "## Cross-references",
        "",
        "- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 "
        "2026-06-18, commit `ccbd12e`)",
        "- **First Strand A analysis** (template anchor): "
        "[`descriptive/operationalisation_support/stress_mean_sleep/`](../stress_mean_sleep/) -- this "
        "analysis adapts the same Q-template to a 24h-window mean continuous channel; cross-analysis "
        "comparison anchors throughout findings.md.",
        "- **Third Strand A analysis** (count-primitive spike companion): "
        "[`descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/`](../stress_low_motion_min_count_S60_Mlow/) "
        "-- reciprocally named spike-form companion per CONVENTIONS section 3.5; cross-pair r=+0.85 / "
        "rho=+0.86.",
        "- **Recovery arc** (Strand B): [`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/) "
        "v2 LANDED 2026-06-22 (`8feae6a`); the afbouw-reversal finding cross-references this analysis's "
        "Q3.2.c + Q3.2.d afbouw-recovery observation.",
        "- **HA-* tests that this analysis anchors**:",
        "  - HA-C3 v2 (primary user; REJECTED at `a2b18ba` 2026-06-23, wrong-direction override); "
        "  descriptive substrate upstream of any HA-C3 v3 redraft.",
        "  - HA-C3p (sister; PARTIAL at `e5a63fe` 2026-06-23); right-shift section 2 observation "
        "  reproduced + extended in Q3.2.c.",
        "  - HA-P6 v3 (descriptive Layer 1); includes this channel in 7-channel distinguishable set.",
        "  - HA-C4 v2 (REJECTED at `52bddb5` 2026-06-18); this channel was Ch1 of the daily-aggregate "
        "  triad; the weak episode-level signal observation here constrains the post-rejection re-"
        "  interpretation.",
        "- **Definitional substrate**: "
        "[`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "section 5.6.1 (locked +0.565/mg dose-response).",
        "- **Other methodology MDs**: `lc_phase_descriptive.md`, `citalopram_phase_stratification.md`, "
        "`permutation_null_block_length.md`, `garmin_indicators_audit.md`, "
        "`lc_era_temporal_segmentation.md`.",
        "- **Existing complementary**: "
        "[`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) "
        "(Q3.2.e cross-reference; one new near-miss pair `all_day_stress_avg <-> bb_lowest` rho=-0.75 "
        "surfaced for next refresh).",
        "- **Upstream pipeline**: `per_day_master.csv` <- "
        "`pipeline/03_consolidate/build_unified_dataset.py` <- `daily_uds.csv` (Wave-3 JSON-side "
        "passthrough 2026-06-12 per `garmin_indicators_audit.md`). NO custom FIT extraction. "
        "`labels_crash_v2.csv` per locked `crash_v2-definition`.",
        "",
    ]
    path.write_text("\n".join(out_lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main() -> None:
    if not os.environ.get("GEVOELSCORE_DATA_PATH"):
        os.environ["GEVOELSCORE_DATA_PATH"] = "C:/Users/Gebruiker/Documents/gevoelscore-data"

    master = load_master(as_of_date=AS_OF_DATE)
    s4 = filter_to_stratum_4(master, as_of_date=AS_OF_DATE)
    labels = load_crash_labels(as_of_date=AS_OF_DATE)[["date", "label", "episode_id"]]
    labels = labels.rename(columns={"label": "_crash_label"})
    s4 = s4.merge(labels, on="date", how="left")
    s4["is_crash"] = (s4["_crash_label"] == "crash").astype(bool)

    if CHANNEL not in s4.columns:
        raise RuntimeError(f"{CHANNEL} not found in master - check pipeline build")

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
        "phase_axis_source": "methodology/citalopram_phase_stratification.md section 3",
        "questions": {},
    }

    summary["questions"]["Q3.2.a_distribution"] = q_a_distribution(values)
    summary["questions"]["Q3.2.b_autocorrelation"] = q_b_autocorrelation(values)
    per_phase = q_c_base_rates_per_phase(s4, CHANNEL)
    summary["questions"]["Q3.2.c_base_rates_per_phase"] = per_phase
    summary["questions"]["Q3.2.c_quintile_bin_distribution"] = q_c_quintile_bin_distribution(s4, CHANNEL)
    summary["questions"]["Q3.2.d_phase_stratified_distribution"] = q_d_phase_stratified(per_phase, CHANNEL)
    summary["questions"]["Q3.2.e_near_identity"] = q_e_near_identity(s4, CHANNEL)
    summary["questions"]["Q3.2.f_crash_vs_normal"] = q_f_crash_vs_normal(s4, CHANNEL)
    summary["questions"]["Q3.2.g_spike_primitive"] = q_g_spike_primitive(s4, CHANNEL)
    summary["questions"]["Q3.2.h_outliers_calibration"] = q_h_outliers_calibration(s4, CHANNEL)
    summary["questions"]["Q3.2.i_covariate_readiness"] = q_i_covariate_readiness(s4, CHANNEL)

    plot_files = make_plots(s4, CHANNEL, HERE / "plots")
    summary["plots"] = plot_files

    out_path = HERE / "summary.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    # Emit findings.md and README.md as programmatic outputs (the
    # Phase-1 precedents had these hand-written; this analysis emits
    # them via run.py to keep the artefact set bit-identical with the
    # summary.json computation).
    write_findings_md(summary, HERE / "findings.md")
    write_readme_md(summary, HERE / "README.md")

    print(f"Wrote {out_path}")
    print(f"Plots: {plot_files}")
    print("\n--- HEADLINE ---")
    a = summary["questions"]["Q3.2.a_distribution"]
    b = summary["questions"]["Q3.2.b_autocorrelation"]
    fr = summary["questions"]["Q3.2.f_crash_vs_normal"]
    print(f"Q3.2.a n={a['n']} mean={a['mean']:.2f} median={a['median']:.2f} MAD={a['mad_unscaled']:.2f} "
          f"skew={a['skewness']:.2f} heavy_tail={a['heavy_tail_flag']}")
    print(f"Q3.2.b E[L]*={b['data_driven_E_L_star']:.2f} (default 7); "
          f"factor-of-2 deviation flag={b['factor_of_2_deviation_flag']}; cutoff M={b['cutoff_lag_M']}")
    pp = summary["questions"]["Q3.2.c_base_rates_per_phase"]
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        if pp.get(ph, {}).get("n", 0) > 0:
            print(f"  Q3.2.c phase {ph}: n={pp[ph]['n']} med={pp[ph]['median']:.2f} MAD={pp[ph]['mad_unscaled']:.2f}")
    quint = summary["questions"]["Q3.2.c_quintile_bin_distribution"]
    print(f"Q3.2.c quintile bin counts: unmed={quint['unmedicated_bin_counts']} "
          f"(n={quint['unmedicated_n']}); full_pool={quint['full_stratum_4_bin_counts']} "
          f"(n={quint['full_stratum_4_n']})")
    fl = fr["day_level"]
    e7 = fl["stationary_bootstrap_E_L7"]
    eS = fl["stationary_bootstrap_E_L_star"]
    print(f"Q3.2.f day-level: n_crash={fl['n_crash_day']} n_normal={fl['n_normal_day']} "
          f"d={fl['cohens_d']:.2f} mean_diff={fl['mean_diff']:.2f}")
    print(f"  E[L]=7  CI=[{e7['ci_lower']:.2f}, {e7['ci_upper']:.2f}] "
          f"width={e7['ci_upper'] - e7['ci_lower']:.2f}")
    print(f"  E[L]*={eS['block_length_used']} CI=[{eS['ci_lower']:.2f}, {eS['ci_upper']:.2f}] "
          f"width={eS['ci_upper'] - eS['ci_lower']:.2f}")
    mwu = fl["mann_whitney_u"]
    print(f"  Mann-Whitney U: z={mwu['z']:.2f} p={mwu['p_two_sided']:.4f} P(crash>normal)={mwu['p_crash_greater_than_normal']:.3f}")
    fe = fr["episode_level"]
    print(f"Q3.2.f episode-level: n_ep={fe['n_crash_episodes']} d={fe['cohens_d_episode_vs_normal_day']:.2f} "
          f"mean_diff={fe['mean_diff_episode_vs_normal_day']:.2f} CI={fe['bootstrap_ci95_mean_diff']}")
    cd = fr["crash_drop_sensitivity_on_spearman_vs_gevoelscore"]
    if cd is not None:
        print(f"Q3.2.f crash-drop on Spearman(stress, gevoelscore): full={cd['full_frame_value']:.3f} "
              f"crashed-dropped={cd['crash_dropped_value']:.3f} |delta|={cd['abs_delta']:.3f} "
              f">0.10? {cd['exceeds_threshold_0p10']}")
    e = summary["questions"]["Q3.2.e_near_identity"]
    print(f"Q3.2.e near-identity flagged: {e['flagged_pairs']}")
    h = summary["questions"]["Q3.2.h_outliers_calibration"]
    print(f"Q3.2.h outliers (|z|>5): {h['n_flagged']} flagged")


if __name__ == "__main__":
    main()
