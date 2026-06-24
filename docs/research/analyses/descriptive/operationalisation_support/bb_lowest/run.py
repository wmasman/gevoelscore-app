"""Descriptive analysis: bb_lowest operationalisation support.

Answers Q3.3.a-k per the locked descriptive programme:
``docs/research/analyses/descriptive/README.md`` section 3.3 (template
a-i + channel-specific j + k applied to this channel). This is the
third (final) of the 3 CONFIRMED-citalopram channels in the Tier 1
user-prioritised "finish the descriptive analysis" Phase 2 sequential
batch (R14 single_pool_reanchor first at badd04a; all_day_stress_avg
second at cf34ab1; bb_lowest this analysis; stress_stdev_sleep closes
Tier 1 next).

Channel: nightly BB nadir / floor (UDS-pre-aggregated; JSON
passthrough from daily_uds.csv per garmin_indicators_audit.md
Wave-3 propagation 2026-06-12; no FIT parsing). CONFIRMED dose-
modulated at -1.13/mg p=0.000 buildup post-CPAP per
citalopram_dose_response_stress_mean_sleep.md section 5.6.1 -- the
**largest absolute beta** among the 3 CONFIRMED channels in
INVERSE direction (sister stress_mean_sleep +0.43/mg same-direction
positive; sister all_day_stress_avg +0.57/mg same-direction positive;
this channel -1.13/mg INVERSE direction -- citalopram RAISES bb_lowest,
i.e. better overnight floor under medication).

Substantive context:
- HA10 primary channel surrogate (BB overnight recharge; HA10 itself
  tests bb_highest variant; bb_lowest is the morning-floor pair). R14
  single_pool_reanchor (badd04a) showed HA10 era-directionality
  reversal -20.5 / +16.2 flattens cleanly to +4.1 pp under single-pool
  re-anchor CONVERGE-ON-OVERALL.
- HA-P6 v3 distinguishable channel (4/7; commit a980b1c 2026-06-17).
- HA-C4b BB-floor candidate channel (deferred per STOCKTAKE section 6).
- recovery_arc v2 standout: "+8 lift IS the multi-year trajectory"
  + the section 5.A afbouw-LOWER-than-baseline finding (buildup 26
  -> consolidation 22 -> afbouw 15; afbouw collapses BELOW even the
  pacing-4b baseline of 18). This is OPPOSITE-direction from sister
  all_day_stress_avg which fully recovers to unmed baseline on afbouw.
  Per STOCKTAKE section 6 line 187 this afbouw-reversal is load-
  bearing.

Channel-specific Q3.3.j + Q3.3.k extensions per descriptive README
section 3.3:
- Q3.3.j: BB-source coverage (per-day bb_lowest is computable from
  when? -- informs which date range any HA test on this column can use).
- Q3.3.k: Relationship to bb_overnight_gain (HA10 primary) -- near-
  identity check + descriptive of the gap between these two BB
  columns. Cross-references bb_overnight_gain_proxy.md (r=0.989 vs
  truth post-2024-09-18; sensitivity-only for 2024-07-08 -> 2024-09-17
  bridge).

Continuous-channel template (parity with all_day_stress_avg + sister
stress_mean_sleep first analysis): standard Cohen's d primary, no
zero-rate column, 8-channel near-identity panel includes both sister
CONFIRMED channels + bb_overnight_gain (HA10 primary pair).

Output: ``summary.json`` (machine-readable per-question results) +
``plots/*.png`` (visualisations) + ``findings.md`` + ``README.md``
(programmatically emitted from this script per the Q3.2 precedent
session's architectural note about the Write-tool harness heuristic
on the literal filename "findings").

Discipline guards (per CONVENTIONS):
- section 2.1 descriptive-before-inference: no causal claims; no
  falsification bar; no HA verdict promotion (HA10, HA-C4b, HA-P6
  cross-referenced descriptively only).
- section 3.1 personal baseline: distribution shape is reported as-is;
  phase-stratified to surface the citalopram step + the afbouw
  reversal.
- section 3.3 column-duplication: near-identity check at |rho|>=0.92.
- section 3.4 crash-drop sensitivity: |Delta|>0.10 flag surfaced.
- section 3.5 spike metrics: bb_lowest is the daily NADIR -- already
  an extreme-of-day metric, not a 24h mean; spike-form vs continuous-
  form discipline differs from the stress-family channels.
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
# HERE = .../analyses/descriptive/operationalisation_support/bb_lowest
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


CHANNEL = "bb_lowest"
AS_OF_DATE = "2026-06-05"  # parity with R14 + all_day_stress_avg + stress_mean_sleep + stress_low_motion

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
# Q3.3.a Distribution shape
# ---------------------------------------------------------------------------


def q_a_distribution(values: pd.Series) -> dict:
    """Distribution shape on Stratum 4 (Q3.3.a)."""
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
    # bb_lowest is a NADIR (lower-bounded at 5; upper tail above median).
    # Heavy-tail rule per CONVENTIONS section 3.1: skew > 1 OR
    # p99/median > 3.0. Apply same rule as sister channels.
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
# Q3.3.b Autocorrelation + E[L]*
# ---------------------------------------------------------------------------


def q_b_autocorrelation(values: pd.Series) -> dict:
    """Autocorrelation structure + E[L]* (Q3.3.b)."""
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
# Q3.3.c Base rates per phase
# ---------------------------------------------------------------------------


def q_c_base_rates_per_phase(df: pd.DataFrame, channel: str) -> dict:
    """Per-phase n + median + dispersion (Q3.3.c)."""
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


# ---------------------------------------------------------------------------
# Q3.3.d Phase-stratified distribution + citalopram step magnitude
# ---------------------------------------------------------------------------


def q_d_phase_stratified(per_phase: dict, channel: str) -> dict:
    """Citalopram step magnitude vs natural day-to-day variation (Q3.3.d).

    Anchored on the -1.13/mg locked dose-response slope -- the LARGEST
    absolute beta among the 3 CONFIRMED channels in INVERSE direction
    (citalopram RAISES bb_lowest). Also captures the recovery_arc v2
    section 5.A afbouw-reversal substructure (afbouw goes LOWER than
    pacing-4b baseline -- OPPOSITE-direction from sister
    all_day_stress_avg afbouw-fully-recovers).
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
        ("buildup", "consolidation"),
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
        "buildup_beta_per_mg": -1.134,
        "buildup_p": 0.000,
        "afbouw_beta_per_mg": -0.586,
        "afbouw_p": 0.14,
        "spring_2025_beta_per_day": -0.061,
        "verdict": "CONFIRMED (sign matches prior in both phases AND buildup HAC 95% CI excludes zero on prior-direction side); direction is INVERSE (citalopram RAISES bb_lowest)",
        "source": "methodology/citalopram_dose_response_stress_mean_sleep.md v3 section 5.6.1",
        "sister_channels": {
            "stress_mean_sleep_buildup_beta": +0.429,
            "all_day_stress_avg_buildup_beta": +0.565,
            "context": "largest absolute beta among 3 CONFIRMED channels; INVERSE direction (the two stress channels are positive; bb_lowest is negative); citalopram RAISES bb_lowest",
        },
    }
    # Implied steady-state effect at 30 mg consolidation (raw-channel
    # naive extrapolation; NOT a section 5.B dose-adjusted prediction):
    out["implied_30mg_lift_buildup_beta_negated"] = -(-1.134) * 30  # +33.99 BB units; positive because INVERSE direction means citalopram pushes bb_lowest UP
    return out


# ---------------------------------------------------------------------------
# Q3.3.e Near-identity check
# ---------------------------------------------------------------------------

NEAR_IDENTITY_THRESHOLD = 0.92  # CONVENTIONS section 3.3


def q_e_near_identity(df: pd.DataFrame, channel: str) -> dict:
    """Near-identity check vs brief-mandated + extended-plus-bb-family
    channels (Q3.3.e).

    Per descriptive README section 3.3 the channel-specific Q3.3.k is
    the bb_overnight_gain pair (HA10 primary); it lives separately
    (q_k_bb_overnight_gain_relationship) so this q_e covers the
    cross-channel set + the sister CONFIRMED-citalopram channels.

    The three brief-mandated channels per descriptive README section 3.3
    template:
      - stress_mean_sleep (sister CONFIRMED-citalopram channel)
      - all_day_stress_avg (sister CONFIRMED-citalopram channel; r=-0.75
        per all_day_stress_avg Q3.2.e the strongest inverse-direction
        neighbour)
      - bb_overnight_gain (HA10 primary; Q3.3.k channel-specific
        extension surfaces it here too for parity)
    Plus several biologically-plausible neighbours.
    """
    targets = [
        # The 3 brief-mandated + sister channels
        "stress_mean_sleep",
        "all_day_stress_avg",
        "bb_overnight_gain",
        # bb-family neighbours
        "bb_highest",
        "bb_sleep_start_value",
        "bb_sleep_end_value",
        "bb_during_sleep_value",
        "bb_overnight_gain_proxy",
        "bb_overnight_gain_best",
        # Cross-family stress companions
        "stress_low_motion_min_count_S60_Mlow",
        "stress_stdev_sleep",
        "awake_stress_avg",
        # Cardiovascular
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
            "Sister all_day_stress_avg Q3.2.e reported Pearson r=-0.727 / Spearman "
            "rho=-0.749 with this channel (the strongest inverse-direction neighbour "
            "in that analysis's near-identity panel; not near-identity at the section "
            "3.3 threshold). Sister stress_mean_sleep Q3.1.e was incidental at "
            "weak-to-moderate inverse magnitude. bb_overnight_gain pair lives also in "
            "Q3.3.k channel-specific extension; both placements are intentional."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.3.f Crash-day vs normal-day on Stratum 4 + crash-drop sensitivity
# ---------------------------------------------------------------------------


def _mann_whitney_u(crash_vals: np.ndarray, normal_vals: np.ndarray) -> dict:
    """Compute Mann-Whitney U with normal approximation + tie correction.

    Returns U, z, p (two-sided), P(crash > normal). Vendored to avoid a
    hard scipy dependency. Note: for bb_lowest the substantive prior is
    that crash days have LOWER bb_lowest (depleted overnight floor); the
    z statistic carries the sign of the U_crash - mean_U difference, so
    a NEGATIVE z would indicate crash < normal on this channel.
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
    sensitivity (Q3.3.f).

    Mirror of all_day_stress_avg Q3.2.f / stress_mean_sleep Q3.1.f.
    Uses stationary-bootstrap CI at E[L]=7 AND data-driven E[L]* when
    factor-of-2 flag fires (Q3.3.b).
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

    # Mann-Whitney U at day level (rank-based robustness)
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

    # Day-level stationary-bootstrap CI at BOTH E[L]=7 and data-driven E[L]*
    aligned = df[["date", channel, "is_crash"]].dropna(subset=[channel, "is_crash"]).copy()
    aligned = aligned.sort_values("date").reset_index(drop=True)

    def day_mean_diff(sub_df):
        c = sub_df["is_crash"].astype(bool)
        if c.sum() < 1 or (~c).sum() < 1:
            return float("nan")
        return float(sub_df.loc[c, channel].mean() - sub_df.loc[~c, channel].mean())

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
                "note": "data-driven from Q3.3.b; rounded to nearest integer",
            },
            "note": (
                "consecutive within-episode days are autocorrelated; "
                "treat as autocorrelation-inflated supplementary read"
            ),
        },
        "episode_level": {
            "n_crash_episodes": n_episodes,
            "n_normal_day_base_rate": n_normal_base,
            "mean_per_episode_value": ep_mean,
            "mean_normal_day_value": float(normal_base_vals.mean()) if n_normal_base else float("nan"),
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
# Q3.3.g Spike-detecting primitive availability
# ---------------------------------------------------------------------------


def q_g_spike_primitive(df: pd.DataFrame, channel: str) -> dict:
    """Spike-primitive availability for bb_lowest (Q3.3.g).

    bb_lowest is the daily NADIR (lowest BB value observed in 24h) from
    UDS pre-aggregated body-battery summary; JSON-passthrough from
    daily_uds.csv per garmin_indicators_audit.md Wave-3 propagation
    2026-06-12 (no FIT parsing). It is STRUCTURALLY ALREADY an extreme-
    of-day metric (per CONVENTIONS section 3.5 spike-discipline) -- not
    a dilution-vulnerable continuous channel like the stress family's
    24h-window mean. The spike-vs-continuous discipline distinction
    differs from the stress channels: bb_lowest IS the spike-form
    primitive on the BB-floor construct.

    Related BB primitives in the master (24h-window):
    - bb_highest: daily peak (24h max)
    - bb_sleep_start_value, bb_sleep_end_value: anchor points
    - bb_overnight_gain: SLEEPEND - SLEEPSTART = recharge arc
      (Q3.3.k channel-specific extension)
    - bb_during_sleep_value: sleep-window-averaged value
    - bb_charged_24h, bb_drained_24h: cumulative event counts
    """
    out = {
        "channel_resolution": "24h NADIR (UDS-pre-aggregated daily floor; JSON passthrough)",
        "spike_or_continuous_form": "SPIKE-FORM (extreme-of-day primitive; structurally already a within-day extremum)",
        "sub_daily_resolution_in_master": False,
        "spike_primitives_available_in_master": [],
        "latent_in_FIT_not_in_master": [
            "per-minute body-battery samples (NOT extracted; bb_overnight_gain_proxy.md section 6 caveat 5 notes 'No per-minute BB anywhere in the dump' as of 2026-06-14)",
        ],
        "related_daily_bb_metrics_in_master": [],
        "note": (
            "Per CONVENTIONS section 3.5 sympathetic-arousal / autonomic-state proxies "
            "prefer spike/peak/count metrics over daily means; bb_lowest IS the spike-"
            "form primitive on the BB-floor construct (the depleted-state extremum of "
            "the day). Unlike the sister stress channels where the continuous-form "
            "(24h mean) and spike-form (low-motion-count, max-spike-minutes) live in "
            "separate columns, bb_lowest is a single extremum-form column. The "
            "complementary BB extremum is bb_highest (peak); the BB recharge arc "
            "(bb_overnight_gain = SLEEPEND - SLEEPSTART) is a separate compound "
            "primitive measured in Q3.3.k. The per-minute-BB primitive that would "
            "allow within-day BB-spike-density extraction does NOT exist in the GDPR "
            "dump per bb_overnight_gain_proxy.md."
        ),
    }
    for c in (
        "bb_highest",
        "bb_sleep_start_value",
        "bb_sleep_end_value",
        "bb_during_sleep_value",
        "bb_charged_24h",
        "bb_drained_24h",
        "bb_overnight_gain",
        "bb_overnight_gain_proxy",
        "bb_overnight_gain_best",
    ):
        if c in df.columns:
            n = int(df[c].notna().sum())
            out["spike_primitives_available_in_master"].append({"column": c, "n_non_nan": n})
    # Pair-wise corr with companion BB primitives
    for partner in ("bb_highest", "bb_sleep_start_value", "bb_sleep_end_value", "bb_during_sleep_value", "bb_overnight_gain", "bb_overnight_gain_best"):
        if partner in df.columns:
            d = df[[channel, partner]].dropna()
            if len(d) > 30:
                out[f"pearson_r_vs_{partner}"] = float(d.corr().iloc[0, 1])
                out[f"spearman_rho_vs_{partner}"] = float(d.corr(method="spearman").iloc[0, 1])
                out[f"n_pair_{partner}"] = int(len(d))
    return out


# ---------------------------------------------------------------------------
# Q3.3.h Outlier detection + calibration-drift check
# ---------------------------------------------------------------------------


def q_h_outliers_calibration(df: pd.DataFrame, channel: str) -> dict:
    """Outlier detection + calibration-drift check (Q3.3.h).

    MAD-based |z|>5 on Stratum 4. Reports flagged dates + values + drift
    snapshots. Cross-references garmin_indicators_audit.md (no per-
    column row for bb_lowest specifically; covered under Wave-3 UDS-
    passthrough bullet) + bb_overnight_gain_proxy.md (coverage bridge
    framing: r=0.989 vs truth post-2024-09-18; sensitivity-only for
    2024-07-08 -> 2024-09-17 bridge -- applied here as discipline anchor
    for any BB-channel coverage discussion).
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
        "2024-06-01", "2025-01-01", "2025-12-01", "2026-04-01",
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
    # Step at 2024-04-09 (citalopram boundary)
    step_buildup = pd.Timestamp("2024-04-09")
    pre30_b = sub.loc[(sub["date"] >= step_buildup - pd.Timedelta(days=30))
                      & (sub["date"] < step_buildup), channel].mean()
    post30_b = sub.loc[(sub["date"] >= step_buildup)
                       & (sub["date"] < step_buildup + pd.Timedelta(days=30)), channel].mean()
    # Step at 2024-06-20 (consolidation start)
    step_consol = pd.Timestamp("2024-06-20")
    pre30_c = sub.loc[(sub["date"] >= step_consol - pd.Timedelta(days=30))
                      & (sub["date"] < step_consol), channel].mean()
    post30_c = sub.loc[(sub["date"] >= step_consol)
                       & (sub["date"] < step_consol + pd.Timedelta(days=30)), channel].mean()
    # Step at 2026-03-20 (afbouw start; CRITICAL for the reversal finding)
    step_afbouw = pd.Timestamp("2026-03-20")
    pre30_a = sub.loc[(sub["date"] >= step_afbouw - pd.Timedelta(days=30))
                      & (sub["date"] < step_afbouw), channel].mean()
    post30_a = sub.loc[(sub["date"] >= step_afbouw)
                       & (sub["date"] < step_afbouw + pd.Timedelta(days=30)), channel].mean()

    return {
        "outlier_rule": "MAD-based |z|>5 (z = (x - median) / (MAD * 1.4826))",
        "median": med,
        "mad_unscaled": mad,
        "n_flagged": int(len(outliers)),
        "outliers": outliers,
        "rolling_90d_median_snapshots": snaps,
        "citalopram_boundary_2024_04_09_step": {
            "pre_30d_mean": float(pre30_b) if pre30_b == pre30_b else None,
            "post_30d_mean": float(post30_b) if post30_b == post30_b else None,
            "diff_post_minus_pre": (
                float(post30_b - pre30_b) if (pre30_b == pre30_b and post30_b == post30_b) else None
            ),
        },
        "consolidation_boundary_2024_06_20_step": {
            "pre_30d_mean": float(pre30_c) if pre30_c == pre30_c else None,
            "post_30d_mean": float(post30_c) if post30_c == post30_c else None,
            "diff_post_minus_pre": (
                float(post30_c - pre30_c) if (pre30_c == pre30_c and post30_c == post30_c) else None
            ),
        },
        "afbouw_boundary_2026_03_20_step": {
            "pre_30d_mean": float(pre30_a) if pre30_a == pre30_a else None,
            "post_30d_mean": float(post30_a) if post30_a == post30_a else None,
            "diff_post_minus_pre": (
                float(post30_a - pre30_a) if (pre30_a == pre30_a and post30_a == post30_a) else None
            ),
            "note": "afbouw boundary step is load-bearing per recovery_arc v2 section 5.A reversal finding",
        },
        "garmin_indicators_audit_known_issues": [
            (
                "bb_lowest is part of the Body Battery family from daily_uds.csv "
                "Wave-3 JSON-side passthrough (2026-06-12); no FIT parsing"
            ),
            (
                "no specific calibration-drift events catalogued for bb_lowest in "
                "garmin_indicators_audit.md; the audit's per-column provenance map "
                "covers BB channels collectively under the UDS-passthrough rows"
            ),
            (
                "underlying sensor is Forerunner 245 Elevate V3 throughout entire "
                "2021-08-16 to present window -- no device change; per "
                "bb_overnight_gain_proxy.md section 6 caveat 1 the single-watch/"
                "single-firmware-family validation extends to all BB columns"
            ),
            (
                "bb_overnight_gain_proxy.md is the load-bearing methodology MD for "
                "any BB-channel coverage discussion: r=0.989 vs truth post-2024-09-18; "
                "sensitivity-only for the 2024-07-08 -> 2024-09-17 bridge; pre-"
                "2024-07-08 BB-overnight metrics absent by Garmin schema rollout, "
                "NOT a project-side pipeline gap (bb_lowest itself has no such "
                "rollout gap -- its 2021 onset is unrestricted; see Q3.3.j)"
            ),
        ],
    }


# ---------------------------------------------------------------------------
# Q3.3.i Covariate-sensitivity readiness
# ---------------------------------------------------------------------------


def q_i_covariate_readiness(df: pd.DataFrame, channel: str) -> dict:
    """Covariate-sensitivity readiness (Q3.3.i).

    Per HA-P7 section 4.5.4 worked-example pattern. Names candidate
    covariates a future HA on bb_lowest as predictor could add.
    """
    cands = []
    # 1. dose_plasma_mg(d) -- obligatory CONFIRMED-citalopram channel
    cands.append({
        "covariate": "dose_plasma_mg(d)",
        "rationale": (
            "Per citalopram_phase_stratification.md section 5.B the channel is "
            "CONFIRMED dose-modulated at -1.13/mg p=0.000 buildup post-CPAP "
            "(the LARGEST ABSOLUTE beta among the 3 CONFIRMED channels in INVERSE "
            "direction). A future HA on bb_lowest cross-phase MUST either dose-"
            "adjust (section 5.B) or per-phase stratify (section 5.A). The cross-"
            "phase pool with predictor = raw - (-1.13)*dose = raw + 1.13*dose is "
            "the section 5.B operationalisation on this channel; the within-"
            "unmedicated-phase headline is the section 5.A operationalisation."
        ),
        "source": "methodology/citalopram_phase_stratification.md section 5.B + section 6; methodology/citalopram_dose_response_stress_mean_sleep.md v3 section 5.6.1",
        "expected_effect_if_primary_signal_is_citalopram": (
            "beta_channel collapses toward zero in the secondary model; beta_dose carries the load"
        ),
        "needed_columns_in_master": ["lc_phase or a runtime dose_plasma_mg(d) computation"],
    })
    # 2. bb_overnight_gain (or bb_overnight_gain_best) -- HA10 primary pair
    bog_corr = None
    if "bb_overnight_gain" in df.columns:
        d = df[[channel, "bb_overnight_gain"]].dropna()
        if len(d) > 30:
            bog_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "bb_overnight_gain (HA10 primary; or bb_overnight_gain_best with coverage extension)",
        "rationale": (
            "HA10 primary BB-recharge channel. bb_lowest is the daily floor; "
            "bb_overnight_gain is the recharge ARC during sleep (SLEEPEND - "
            "SLEEPSTART). The covariate disambiguates: is the bb_lowest signal "
            "driven by the depleted-state floor (beta_channel survives -- bb_lowest "
            "carries information beyond the recharge magnitude) or by the recharge "
            "magnitude itself (beta_channel attenuates -- bb_overnight_gain was "
            "doing the work). NOTE: bb_overnight_gain has 593 truth days post-"
            "2024-09-18 + 74 proxy days back to 2024-07-08 per "
            "bb_overnight_gain_proxy.md; covariate adoption on a pre-2024-07-08-"
            "starting HA must use bb_overnight_gain_best AND disclose proxy share "
            "per the proxy MD's section 4 discipline rule 1."
        ),
        "source": "HA10 result.md; bb_overnight_gain_proxy.md",
        "observed_correlation_on_S4": bog_corr,
        "expected_effect": (
            "beta_channel attenuates if signal is overnight recharge magnitude; "
            "beta_channel survives if depleted-state floor carries independent information"
        ),
    })
    # 3. all_day_stress_avg -- sister CONFIRMED-citalopram channel (strongest inverse neighbour)
    sister_corr = None
    if "all_day_stress_avg" in df.columns:
        d = df[[channel, "all_day_stress_avg"]].dropna()
        if len(d) > 30:
            sister_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "all_day_stress_avg",
        "rationale": (
            "Sister CONFIRMED-citalopram channel; INVERSE-direction neighbour "
            "(all_day_stress_avg Q3.2.e reported rho=-0.749 with this channel -- "
            "the strongest inverse-direction neighbour in that analysis's near-"
            "identity panel; not near-identity at the section 3.3 threshold). Both "
            "channels are CONFIRMED dose-modulated in opposite directions (stress "
            "UP with dose; bb_lowest UP with dose -- both reflect citalopram-"
            "trajectory absorption). The covariate disambiguates: is the bb_lowest "
            "signal specifically the BB-floor mechanism (beta_channel survives "
            "when all_day_stress is held constant) or the autonomic-state shared "
            "variance with the daily mean stress (beta_channel attenuates -- the "
            "two channels are reading the same underlying autonomic-load signal in "
            "opposite directions)."
        ),
        "source": "all_day_stress_avg findings.md Q3.2.e (rho=-0.749 with this channel)",
        "observed_correlation_on_S4": sister_corr,
        "expected_effect": (
            "beta_channel attenuates if shared autonomic-state variance dominates; "
            "beta_channel survives if BB-floor mechanism carries independent information"
        ),
    })
    # 4. own-lagged trailing-mean -- autocorrelation-vs-mechanism (HA-P7 section 4.5.4)
    cands.append({
        "covariate": "bb_lowest_lagged_mean_Nd(d) = mean(channel[d-N:d-1]) with N tuned to Q3.3.b E[L]* + margin",
        "rationale": (
            "Mirrors HA-P7 section 4.5.4 worked example (lagged-outcome covariate) "
            "for the autocorrelation-vs-mechanism disambiguation. NOTE: bb_lowest "
            "ALREADY has a materialised lagged-baseline variant in per_day_master: "
            "bb_lowest_lagged_lcera_z (LC-era-only [d-90, d-30] trailing baseline "
            "per CONVENTIONS section 3.2 _lagged_lcera convention). The HA author "
            "can use that materialised variant directly OR compute a shorter window "
            "(N tuned to Q3.3.b cutoff lag M with margin). Per Q3.3.b the cutoff "
            "lag M and data-driven E[L]* are inputs to this choice."
        ),
        "source": "HA-P7 hypothesis.md section 4.5.4 worked example + per_day_master.csv bb_lowest_lagged_lcera_z column",
        "expected_effect": (
            "beta_channel collapses if today's bb_lowest is just yesterday's bb_lowest carried forward; "
            "beta_channel survives if the signal carries new-day information"
        ),
        "needed_columns_in_master": [
            "bb_lowest_lagged_lcera_z (already in master per CONVENTIONS section 3.2)"
        ],
    })
    return {
        "primary_use_case": (
            "Future HA pre-reg using bb_lowest as predictor of a crash-related outcome "
            "(e.g. HA-C4b BB-floor candidate; HA10 sibling using floor rather than peak)"
        ),
        "discipline_anchor": "HA-P7 hypothesis.md section 4.5.4 -- secondary-logistic-with-covariate pattern",
        "candidate_covariates": cands,
        "recommendation": (
            "Pre-spec all four covariates as secondary sensitivity arms. The "
            "citalopram-phase framework section 5.B adjustment is OBLIGATORY (the "
            "channel is CONFIRMED-citalopram at the largest absolute beta in the "
            "set); the other three are diagnostic. Concordance across the "
            "secondaries = high confidence in the primary; divergence = the "
            "disambiguation is doing real work. HA-C4b BB-floor pre-reg (deferred "
            "per STOCKTAKE section 6) is the natural consumer."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.3.j (channel-specific) BB-source coverage
# ---------------------------------------------------------------------------


def q_j_bb_source_coverage(df: pd.DataFrame, channel: str) -> dict:
    """BB-source coverage for bb_lowest (Q3.3.j channel-specific).

    Per descriptive README section 3.3: "Coverage of the BB-source
    channel: per-day bb_lowest is computable from when? Informs which
    date range any HA test on this column can use." Contrast with
    bb_overnight_gain coverage which is structurally absent for 64% of
    LC corpus due to Garmin schema rollout (SLEEPSTART 2024-07-08;
    SLEEPEND 2024-09-18) per bb_overnight_gain_proxy.md section 1.
    """
    full = df[[channel, "date"]].copy()
    n_total = int(len(full))
    n_non_nan = int(full[channel].notna().sum())
    first_non_nan = full.loc[full[channel].notna(), "date"].min()
    last_non_nan = full.loc[full[channel].notna(), "date"].max()

    # Per-phase coverage
    per_phase_coverage = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (full["date"] >= pd.Timestamp(start)) & (full["date"] <= pd.Timestamp(end))
        n_days = int(mask.sum())
        n_with = int(full.loc[mask, channel].notna().sum())
        per_phase_coverage[phase_name] = {
            "n_days_in_window": n_days,
            "n_with_channel": n_with,
            "coverage_pct": round(100.0 * n_with / n_days, 2) if n_days > 0 else None,
        }

    # Contrast with bb_overnight_gain (HA10 primary; structurally absent
    # pre-2024-07-08 per bb_overnight_gain_proxy.md)
    bog_info = None
    if "bb_overnight_gain" in df.columns:
        bog_mask = df["bb_overnight_gain"].notna()
        bog_first = df.loc[bog_mask, "date"].min()
        bog_info = {
            "first_non_nan": str(bog_first.date()) if pd.notna(bog_first) else None,
            "n_non_nan_full_corpus": int(bog_mask.sum()),
            "share_of_corpus_pct": round(100.0 * bog_mask.sum() / len(df), 2),
        }

    return {
        "channel": channel,
        "n_rows_full_corpus": n_total,
        "n_non_nan_full_corpus": n_non_nan,
        "share_of_corpus_pct": round(100.0 * n_non_nan / n_total, 2) if n_total > 0 else None,
        "first_non_nan_date_full_corpus": str(first_non_nan.date()) if pd.notna(first_non_nan) else None,
        "last_non_nan_date_full_corpus": str(last_non_nan.date()) if pd.notna(last_non_nan) else None,
        "per_phase_coverage_in_stratum_4": per_phase_coverage,
        "contrast_with_bb_overnight_gain": bog_info,
        "verdict": (
            "bb_lowest has full corpus coverage from 2021-08-16 onward (no Garmin "
            "schema rollout gap); contrast with bb_overnight_gain which is "
            "structurally absent for ~64% of LC corpus pre-2024-09-18 (SLEEPSTART "
            "rollout 2024-07-08; SLEEPEND rollout 2024-09-18) per "
            "bb_overnight_gain_proxy.md section 1. Any HA test on bb_lowest can "
            "use the full Stratum 4 window without coverage-bridge sensitivity; "
            "any HA on bb_overnight_gain MUST use bb_overnight_gain_best with "
            "proxy-share disclosure per bb_overnight_gain_proxy.md section 4 "
            "discipline rule 1 OR restrict to post-2024-09-18."
        ),
        "source": "per_day_master.csv non-NaN counts; bb_overnight_gain_proxy.md section 1 + section 5.4 coverage gain table",
    }


# ---------------------------------------------------------------------------
# Q3.3.k (channel-specific) Relationship to bb_overnight_gain
# ---------------------------------------------------------------------------


def q_k_bb_overnight_gain_relationship(df: pd.DataFrame, channel: str) -> dict:
    """Relationship to bb_overnight_gain (Q3.3.k channel-specific).

    Per descriptive README section 3.3: "Relationship to
    bb_overnight_gain (HA10's primary): near-identity check +
    descriptive of the gap between these two BB columns." Anchored on
    bb_overnight_gain_proxy.md (truth post-2024-09-18; proxy 2024-07-08
    -> 2024-09-17 bridge).
    """
    out = {
        "discipline_anchor": "bb_overnight_gain_proxy.md (r=0.989 vs truth post-2024-09-18; sensitivity-only for 2024-07-08 -> 2024-09-17 bridge)",
        "near_identity_threshold": NEAR_IDENTITY_THRESHOLD,
        "pairs": {},
    }

    for partner in ("bb_overnight_gain", "bb_overnight_gain_best", "bb_overnight_gain_proxy"):
        if partner not in df.columns:
            out["pairs"][partner] = {"note": "column absent"}
            continue
        d = df[[channel, partner, "date"]].dropna(subset=[channel, partner])
        if len(d) < 30:
            out["pairs"][partner] = {"n": int(len(d)), "note": "n<30 - skipped"}
            continue
        pear = float(d[channel].corr(d[partner]))
        spear = float(d[channel].corr(d[partner], method="spearman"))
        flagged = max(abs(pear), abs(spear)) >= NEAR_IDENTITY_THRESHOLD
        # Source-conditioned read for bb_overnight_gain_best
        info = {
            "n": int(len(d)),
            "pearson_r": pear,
            "spearman_rho": spear,
            "near_identity_flag": flagged,
            "first_date": str(d["date"].min().date()),
            "last_date": str(d["date"].max().date()),
        }
        if partner == "bb_overnight_gain_best" and "bb_overnight_gain_source" in df.columns:
            d_src = df[[channel, partner, "bb_overnight_gain_source", "date"]].dropna(
                subset=[channel, partner]
            )
            truth_mask = d_src["bb_overnight_gain_source"].astype(str) == "truth"
            proxy_mask = d_src["bb_overnight_gain_source"].astype(str) == "proxy"
            info["source_truth_n"] = int(truth_mask.sum())
            info["source_proxy_n"] = int(proxy_mask.sum())
            if truth_mask.sum() > 30:
                info["pearson_r_truth_only"] = float(
                    d_src.loc[truth_mask, channel].corr(d_src.loc[truth_mask, partner])
                )
                info["spearman_rho_truth_only"] = float(
                    d_src.loc[truth_mask, channel].corr(d_src.loc[truth_mask, partner], method="spearman")
                )
            if proxy_mask.sum() > 30:
                info["pearson_r_proxy_only"] = float(
                    d_src.loc[proxy_mask, channel].corr(d_src.loc[proxy_mask, partner])
                )
                info["spearman_rho_proxy_only"] = float(
                    d_src.loc[proxy_mask, channel].corr(d_src.loc[proxy_mask, partner], method="spearman")
                )
        out["pairs"][partner] = info

    out["substantive_gap_description"] = (
        "bb_lowest measures the daily NADIR (lowest BB observed across the 24h "
        "window). bb_overnight_gain measures the RECHARGE ARC during sleep "
        "(SLEEPEND - SLEEPSTART). These are operationally distinct constructs "
        "even on a perfect-coverage day: the floor depth and the recharge "
        "magnitude can move independently (a deep-floor night with strong recharge "
        "vs a shallow-floor night with weak recharge). The empirically-observed "
        "correlation magnitude reported above characterises the shared variance "
        "on the overlap window; the near-identity flag at |rho|>=0.92 governs "
        "whether the pair counts as column-duplication per CONVENTIONS section 3.3."
    )
    out["operational_consequence"] = (
        "HA10 primary uses BB peak (bb_highest) as the morning-recovery marker; "
        "bb_lowest is the complementary depleted-state marker. A future HA-C4b "
        "BB-floor pre-reg (deferred per STOCKTAKE section 6) would use bb_lowest "
        "as primary; HA10 + HA-C4b together would cover both ends of the BB "
        "construct. bb_overnight_gain is the arc between them and the third "
        "leg of the BB-recovery construct triangle."
    )
    return out


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
    ax.set_xlabel("bb_lowest (Garmin BB units, daily nadir)")
    ax.set_ylabel("days (Stratum 4)")
    ax.set_title(f"bb_lowest distribution - Stratum 4, n={int(vals.notna().sum())}")
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
    ax.set_ylabel("bb_lowest")
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
    ax.set_ylabel("bb_lowest")
    ax.set_title("bb_lowest - rolling 90d median + citalopram phases")
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
    ax.set_xlabel("bb_lowest")
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
        f"ACF - bb_lowest (Stratum 4); E[L]*={acf_res['optimal_block_length']:.1f}, M={acf_res['cutoff_lag']}"
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


def _fmt_near_id_rows(rows_list: list) -> list[str]:
    out = []
    for r in rows_list:
        if "pearson_r" in r:
            flag = "no" if not r["near_identity_flag"] else "**YES**"
            out.append(
                f"| `{r['channel']}` | {r['n']} | {r['pearson_r']:+.3f} | {r['spearman_rho']:+.3f} | {flag} |"
            )
        else:
            out.append(f"| `{r['channel']}` | -- | -- | -- | {r.get('note', 'n/a')} |")
    return out


def write_findings_md(summary: dict, path: Path) -> None:
    """Emit the analyst-style findings.md from the computed summary.

    Layer 1 descriptive per CONVENTIONS section 2.1; cross-references to
    HA10 + HA-P6 v3 + HA-C4b verdicts + recovery_arc v2 + recalibration
    anchor are descriptive only, NOT verdict promotion.
    """
    q = summary["questions"]
    a = q["Q3.3.a_distribution"]
    b = q["Q3.3.b_autocorrelation"]
    c = q["Q3.3.c_base_rates_per_phase"]
    d = q["Q3.3.d_phase_stratified_distribution"]
    e = q["Q3.3.e_near_identity"]
    fr = q["Q3.3.f_crash_vs_normal"]
    fl = fr["day_level"]
    fe = fr["episode_level"]
    g = q["Q3.3.g_spike_primitive"]
    h = q["Q3.3.h_outliers_calibration"]
    i = q["Q3.3.i_covariate_readiness"]
    j = q["Q3.3.j_bb_source_coverage"]
    k = q["Q3.3.k_bb_overnight_gain_relationship"]

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
    afbouw_step = h["afbouw_boundary_2026_03_20_step"]
    outliers = h["outliers"]

    near_id_rows = _fmt_near_id_rows(e["rows"])

    per_phase_rows = []
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = c.get(ph, {})
        if info.get("n", 0) > 0:
            per_phase_rows.append(
                f"| {ph} | {info['date_start']} to {info['date_end']} | {info['n']} | "
                f"**{info['median']:.2f}** | {info['mean']:.2f} | {info['mad_unscaled']:.2f} | "
                f"{info['p10']:.1f} / {info['p90']:.1f} |"
            )

    # Q3.3.k pair table rows
    k_rows = []
    for partner_name, info in k["pairs"].items():
        if "pearson_r" in info:
            flag = "**YES**" if info["near_identity_flag"] else "no"
            row = (
                f"| `{partner_name}` | {info['n']} | {info['pearson_r']:+.3f} | "
                f"{info['spearman_rho']:+.3f} | {flag} | {info['first_date']} -> {info['last_date']} |"
            )
            k_rows.append(row)
        else:
            k_rows.append(f"| `{partner_name}` | -- | -- | -- | -- | {info.get('note', 'n/a')} |")

    # Q3.3.j per-phase coverage rows
    j_rows = []
    for ph_name, ph_info in j["per_phase_coverage_in_stratum_4"].items():
        if ph_info["coverage_pct"] is not None:
            j_rows.append(
                f"| {ph_name} | {ph_info['n_days_in_window']} | {ph_info['n_with_channel']} | "
                f"{ph_info['coverage_pct']:.2f}% |"
            )

    afbouw_med = c.get("afbouw", {}).get("median", float("nan"))
    consol_med = c.get("consolidation", {}).get("median", float("nan"))
    buildup_med = c.get("buildup", {}).get("median", float("nan"))
    unmed_med = c.get("unmedicated", {}).get("median", float("nan"))
    afbouw_minus_consol = d["phase_to_phase_shifts"].get("afbouw_minus_consolidation_median", float("nan"))
    afbouw_minus_unmed = d["phase_to_phase_shifts"].get("afbouw_minus_unmedicated_median", float("nan"))
    buildup_minus_unmed = d["phase_to_phase_shifts"].get("buildup_minus_unmedicated_median", float("nan"))
    consol_minus_unmed = d["phase_to_phase_shifts"].get("consolidation_minus_unmedicated_median", float("nan"))

    out_lines = [
        "# Findings -- `bb_lowest` operationalisation-support descriptive (Q3.3.a-k)",
        "",
        "**Channel**: `bb_lowest` (CONFIRMED-citalopram, -1.134/mg p=0.000 buildup post-CPAP per "
        "[`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "v3 section 5.6.1 -- the **largest absolute beta** among the 3 CONFIRMED channels in INVERSE "
        "direction; citalopram RAISES bb_lowest, i.e. better overnight floor under medication). Column "
        "semantics: [DATA_DICTIONARY.md Body Battery section](../../../DATA_DICTIONARY.md) -- daily NADIR "
        "of Garmin Body Battery UDS-pre-aggregated stat (lowest BB value observed across the 24h window), "
        "JSON-passthrough from `daily_uds.csv` per "
        "[`garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) Wave-3 propagation "
        "2026-06-12 (no FIT parsing).",
        "",
        f"**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to {summary['as_of_date']}). "
        f"n={a['n']} days with channel out of {summary['n_rows_stratum_4_total']} Stratum 4 days "
        f"({summary['n_rows_stratum_4_total'] - a['n']} NaN days from UDS-side coverage gaps).",
        "",
        "**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.3 (LOCKED 2026-06-18 r3, "
        "commit `ccbd12e`) -- this analysis is the **third (final) of the 3 CONFIRMED-citalopram channels "
        "in the Tier 1 user-prioritised Phase 2 sequential batch** (R14 `single_pool_reanchor` first at "
        "`badd04a`; `all_day_stress_avg` second at `cf34ab1`; this bb_lowest third; "
        "`stress_stdev_sleep` closes Tier 1 next). Q3.3.a-i template applied per section 3.1 verbatim + "
        "Q3.3.j + Q3.3.k channel-specific extensions per section 3.3.",
        "",
        "**Sources**: `per_day_master.csv` (Garmin daily aggregate) + `labels_crash_v2.csv` (`label=='crash'` "
        "day-level; `episode_id` starting with `crash-` episode-level per CONVENTIONS section 3.6).",
        "",
        "**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict "
        "promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). "
        "HA10 (BB overnight recharge; LOCKED OVERALL-REFUTED with R14 single-pool re-anchor "
        "CONVERGE-ON-OVERALL) + HA-P6 v3 (LOCKED; bb_lowest is one of 4/7 distinguishable channels) + "
        "HA-C4b (BB-floor candidate; DEFERRED per STOCKTAKE section 6) cross-references in this analysis "
        "are **descriptive corroboration only**; the substantive verdicts live in those result.md files "
        "and are NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). "
        "Statistical hygiene anchors: section 3.1 (personal baseline), section 3.3 (column-duplication "
        "threshold |rho|>=0.92), section 3.4 (crash-drop sensitivity |delta|>0.10), section 3.5 (spike "
        "metrics -- bb_lowest IS the spike-form NADIR primitive on the BB-floor construct; not a 24h "
        "mean), section 3.6 (named counts).",
        "",
        "---",
        "",
        "## Headline",
        "",
        f"`bb_lowest` on Stratum 4 is a **mildly right-skewed, autocorrelation-DENSE daily-NADIR channel** "
        f"(skew={skew:+.2f}, excess kurtosis={a['excess_kurtosis']:+.2f}, "
        f"heavy_tail_flag={a['heavy_tail_flag']}, p99/median = {p99:.0f}/{med:.0f} = {p99_over_med:.2f}). "
        f"The **data-driven E[L]\\*={el_star:.1f}** (Politis-White; deviation ratio "
        f"{b['deviation_ratio']:.2f}; factor-of-2 flag = {b['factor_of_2_deviation_flag']}; cutoff lag "
        f"M={b['cutoff_lag_M']}). Cross-channel context: vs sister CONFIRMED-citalopram channels "
        f"`stress_mean_sleep` E[L]\\*=12.6 + `all_day_stress_avg` E[L]\\*=29.8 + spike-companion "
        f"`stress_low_motion_min_count_S60_Mlow` E[L]\\*=21.1 -- this channel sits at "
        f"{'longer' if el_star > 25 else 'shorter' if el_star < 14 else 'mid-range'} autocorrelation. The "
        f"**phase-stratified medians track the recovery_arc v2 section 5.A trajectory faithfully**: "
        f"unmedicated median {unmed_med:.1f} -> buildup {buildup_med:.1f} -> consolidation "
        f"{consol_med:.1f} -> **afbouw {afbouw_med:.1f}** (citalopram lifts the floor through buildup + "
        f"consolidation, then the afbouw phase {('GOES LOWER than even unmedicated baseline' if afbouw_med < unmed_med else 'returns toward baseline')} "
        f"-- the load-bearing reversal finding per [recovery_arc v2 findings.md section 5.A](../../trajectory/recovery_arc/findings.md) "
        f"+ [STOCKTAKE section 6 line 187](../../../STOCKTAKE.md)). Day-resolved citalopram boundary "
        f"step (2024-04-09 pre/post 30d) is **{citalo_step['diff_post_minus_pre']:+.2f} BB units**; "
        f"afbouw boundary step (2026-03-20 pre/post 30d) is **{afbouw_step['diff_post_minus_pre']:+.2f} BB "
        f"units** -- the latter shows the empirical afbouw drop in day-resolved form. Crash-vs-normal: "
        f"episode-level d={fe['cohens_d_episode_vs_normal_day']:+.2f} (bootstrap CI95 "
        f"[{ci_ep[0]:+.2f}, {ci_ep[1]:+.2f}]); day-level Mann-Whitney U z={mwu['z']:+.2f} "
        f"p={'<0.0001' if mwu['p_two_sided'] < 0.0001 else format(mwu['p_two_sided'], '.4f')} "
        f"P(crash>normal)={mwu['p_crash_greater_than_normal']:.3f}. Near-identity check: "
        f"{'zero near-identity pairs' if not e['flagged_pairs'] else 'flagged pairs ' + ', '.join('`' + p + '`' for p in e['flagged_pairs'])} "
        f"at the |rho|>=0.92 CONVENTIONS section 3.3 threshold. Q3.3.j: bb_lowest has full corpus "
        f"coverage from {j['first_non_nan_date_full_corpus']} onward "
        f"({j['share_of_corpus_pct']:.1f}% of corpus rows) -- contrast with bb_overnight_gain "
        f"({j['contrast_with_bb_overnight_gain']['first_non_nan']} onset; "
        f"{j['contrast_with_bb_overnight_gain']['share_of_corpus_pct']:.1f}% of corpus). Q3.3.k: "
        f"bb_overnight_gain pairing rho values reported in section Q3.3.k below.",
        "",
        "---",
        "",
        "## Q3.3.a -- Distribution shape (Stratum 4)",
        "",
        "**Verdict on the section 3.1 delegate question**: **delegate is partial; extend in this "
        "analysis**. [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) "
        "was extended for continuous channels first and primarily documents `stress_mean_sleep`; coverage "
        "on `bb_lowest` is incidental. The full distribution descriptors (skewness/kurtosis/heavy-tail "
        "flag/p99-vs-median ratio) are surfaced here for the first time on this channel.",
        "",
        "| stat | value | source |",
        "|---|---:|---|",
        f"| n (Stratum 4) | {a['n']} | `per_day_master.csv` `bb_lowest` non-NaN within S4 |",
        f"| mean | {a['mean']:.2f} | (single-pool S4) |",
        f"| median | {a['median']:.2f} | |",
        f"| std (ddof=1) | {a['std_ddof1']:.2f} | |",
        f"| MAD (unscaled) | {a['mad_unscaled']:.2f} | |",
        f"| MAD x 1.4826 (normal-equivalent SD) | {a['mad_normal_equivalent']:.2f} | for robust z-score scaling per section 3.1 |",
        f"| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | {quant['p1']:.1f} / {quant['p5']:.1f} / {quant['p10']:.1f} / {quant['p25']:.1f} / {quant['p50']:.1f} / {quant['p75']:.1f} / {quant['p90']:.1f} / {quant['p95']:.1f} / {quant['p99']:.1f} | |",
        f"| skewness (Fisher-Pearson) | **{a['skewness']:+.2f}** | mildly right-skewed (NADIR channel; lower-bounded near 5) |",
        f"| excess kurtosis (Fisher) | **{a['excess_kurtosis']:+.2f}** | |",
        f"| heavy_tail_flag | **{a['heavy_tail_flag']}** | skew>1 OR p99/median > 3.0 |",
        f"| range | {a['min']:.1f} to {a['max']:.1f} | BB values bounded 0-100 (Garmin scale); the channel sits in the lower half of that range |",
        "",
        "### Cross-channel comparison vs sister CONFIRMED-citalopram channels",
        "",
        "| stat | bb_lowest (this analysis) | all_day_stress_avg (Q3.2) | stress_mean_sleep (Q3.1) |",
        "|---|---:|---:|---:|",
        f"| n S4 | {a['n']} | 1359 | 1339 |",
        f"| mean | {a['mean']:.2f} | 32.72 | 19.97 |",
        f"| median | {a['median']:.2f} | 32.00 | 19.21 |",
        f"| MAD (unscaled) | {a['mad_unscaled']:.2f} | 4.00 | 2.87 |",
        f"| skewness | {a['skewness']:+.2f} | +0.87 | +2.72 |",
        f"| heavy_tail_flag | **{a['heavy_tail_flag']}** | **False** | **True** |",
        "",
        "**bb_lowest is a daily NADIR (already an extreme-of-day extremum) operationally distinct from "
        "the 24h-mean stress channels.** Per CONVENTIONS section 3.5 the NADIR IS the spike-form on the "
        "BB-floor construct; it is not dilution-vulnerable in the same way as the sister stress channels' "
        "24h-window means. The complementary BB extremum is bb_highest (peak); the recharge arc "
        "(bb_overnight_gain = SLEEPEND - SLEEPSTART) is a separate compound primitive (Q3.3.k).",
        "",
        "See [`plots/fig1_distribution_s4.png`](plots/fig1_distribution_s4.png).",
        "",
        "---",
        "",
        "## Q3.3.b -- Autocorrelation structure + E[L]\\*",
        "",
        f"The **data-driven block length is E[L]\\*={el_star:.1f}** (Politis-White 2004 with Patton-"
        "Politis-White 2009 correction per "
        "[`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) "
        "vs the project default E[L]=7 per "
        "[`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). "
        f"The **factor-of-2 deviation flag = {b['factor_of_2_deviation_flag']}** (deviation ratio = "
        f"{b['deviation_ratio']:.2f}). Cutoff lag M={b['cutoff_lag_M']}.",
        "",
        _fmt_acf_table(b["selected_acf_lags"]),
        "",
        f"Politis-White 2-sigma significance threshold (n={b['n_non_nan']}): "
        f"|rho| = {b['politis_white_significance_threshold_2sigma']:.3f}.",
        "",
        "### Cross-channel comparison (E[L]\\* by Strand A analysis)",
        "",
        "| analysis | channel | E[L]\\* | M | factor-of-2 flag |",
        "|---|---|---:|---:|---|",
        "| Phase-1 #1 (stress_mean_sleep) | sleep-window mean | 12.6 | 6 | YES (factor-of-2) |",
        "| Phase-1 #3 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 | 11 | YES (factor-of-3) |",
        "| Phase-2 #2 (all_day_stress_avg) | 24h-window mean | 29.8 | 18 | YES (factor-of-4) |",
        f"| **this analysis (bb_lowest)** | **daily NADIR** | **{el_star:.1f}** | **{b['cutoff_lag_M']}** | **{('YES' if b['factor_of_2_deviation_flag'] else 'no')}** |",
        "",
        f"**Implication**: any HA pre-reg using `bb_lowest` should pre-spec a sensitivity arm at "
        f"E[L]\\*={el_int} alongside the default-E[L]=7 primary. Per Q3.3.b's data-driven estimate the "
        "channel's serial dependence sits at the autocorrelation horizon reported in the cross-channel "
        "table above. The mechanistic interpretation: bb_lowest inherits long-range trend structure "
        "from the multi-year recovery arc (lift 12 -> 22 across phases per recovery_arc v2 section 2) "
        "+ the citalopram trajectory (section 5.A within-phase-5 sub-cells); the autocorrelation reflects "
        "both day-to-day serial dependence and the slow trajectory absorption.",
        "",
        "See [`plots/fig5_acf.png`](plots/fig5_acf.png).",
        "",
        "---",
        "",
        "## Q3.3.c -- Base rates per citalopram phase",
        "",
        "Phase axis per "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3:",
        "",
        "| phase | window | n | median | mean | MAD | p10 / p90 |",
        "|---|---|---:|---:|---:|---:|---|",
        *per_phase_rows,
        "",
        f"The two **transition phases** (buildup n={c['buildup']['n']}; afbouw n={c['afbouw']['n']}) have "
        f"**n<75 each**; the two **steady-state phases** (unmedicated n={c['unmedicated']['n']}; "
        f"consolidation n={c['consolidation']['n']}) are an order of magnitude larger. Any HA test that "
        "wants per-phase verdicts under "
        "[`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 5.A on buildup or afbouw faces a ~10x n disadvantage vs the steady-state phases (same "
        "as sister channels Q3.1.c / Q3.2.c).",
        "",
        "Named counts (CONVENTIONS section 3.6): the per-phase n's above are `bb_lowest`-non-NaN day rows "
        "in `per_day_master.csv` within Stratum 4 date masks per `citalopram_phase_stratification.md "
        "section 3` boundary dates.",
        "",
        "See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (citalopram-phase violins).",
        "",
        "---",
        "",
        "## Q3.3.d -- Phase-stratified distribution + citalopram step magnitude vs natural variation",
        "",
        "**This is the most operationally consequential finding for downstream HA pre-regs on this "
        "channel, AND the location of the load-bearing recovery_arc v2 afbouw-reversal cross-reference.**",
        "",
        "The locked dose-response anchor (v3 section 5.6.1): **buildup post-CPAP beta = -1.134/mg "
        "p=0.000** (the **LARGEST ABSOLUTE beta** among the 3 CONFIRMED-citalopram channels in INVERSE "
        "direction: `stress_mean_sleep` +0.43/mg, `all_day_stress_avg` +0.57/mg, this channel -1.13/mg). "
        "The sign convention: citalopram **raises** bb_lowest (better overnight floor under medication). "
        "Naive extrapolation: at 30mg steady-state (consolidation), the implied citalopram-attributable "
        f"lift is -(-1.134) x 30 = **+{d['implied_30mg_lift_buildup_beta_negated']:.2f} BB units** -- "
        "larger than the channel's full interquartile range (p75 - p25 = "
        f"{quant['p75'] - quant['p25']:.0f}) **TRIPLED**, and ~5+ standard deviations on the "
        "consolidation-phase MAD.",
        "",
        "Observed steady-state level shifts (median):",
        "",
        "| comparison | delta median | within-phase MAD | within-MAD? |",
        "|---|---:|---:|---|",
        f"| buildup minus unmedicated | **{buildup_minus_unmed:+.1f}** | {c['buildup']['mad_unscaled']:.1f}-{c['unmedicated']['mad_unscaled']:.1f} | citalopram lift visible at buildup |",
        f"| consolidation minus unmedicated | **{consol_minus_unmed:+.1f}** | {c['consolidation']['mad_unscaled']:.1f} | citalopram lift sustained at steady-state |",
        f"| consolidation minus buildup | **{d['phase_to_phase_shifts'].get('consolidation_minus_buildup_median', 0):+.1f}** | {c['consolidation']['mad_unscaled']:.1f} | the v2 recovery_arc 26 -> 22 trajectory within phase 5 |",
        f"| afbouw minus consolidation | **{afbouw_minus_consol:+.1f}** | {c['consolidation']['mad_unscaled']:.1f}-{c['afbouw']['mad_unscaled']:.1f} | the afbouw collapse |",
        f"| afbouw minus unmedicated | **{afbouw_minus_unmed:+.1f}** | {c['unmedicated']['mad_unscaled']:.1f}-{c['afbouw']['mad_unscaled']:.1f} | the load-bearing reversal cell |",
        "",
        "### Reading the direction -- what the data shows + the load-bearing recovery_arc v2 reversal",
        "",
        f"The median **lifts substantially during citalopram phases** (unmedicated {unmed_med:.1f} -> "
        f"buildup {buildup_med:.1f} -> consolidation {consol_med:.1f}; consistent with the citalopram-"
        f"raises-bb_lowest direction). The day-resolved citalopram boundary step (30d pre vs post the "
        f"2024-04-09 boundary): **{citalo_step['diff_post_minus_pre']:+.2f} BB units** -- the empirical "
        "day-resolved citalopram-onset effect on the channel.",
        "",
        f"**The afbouw cell (median {afbouw_med:.1f}) is the load-bearing finding.** Per "
        "[recovery_arc v2 findings.md section 5.A](../../trajectory/recovery_arc/findings.md) the within-"
        f"phase-5 citalopram-axis sub-cells were reported as **buildup 26 -> consolidation 22 -> afbouw "
        f"15** -- afbouw COLLAPSES BELOW the pacing-4b baseline of 18 (the established post-pacing-habit "
        f"BB-floor level). This analysis's afbouw-minus-consolidation diff "
        f"({afbouw_minus_consol:+.1f}) + afbouw-minus-unmedicated diff ({afbouw_minus_unmed:+.1f}) "
        f"{'REPRODUCE the v2 recovery_arc afbouw-LOWER-than-baseline pattern at the citalopram-axis-only stratification' if afbouw_minus_unmed < 0 else 'show the citalopram-axis-only stratification'}. "
        f"The day-resolved afbouw boundary step (30d pre/post 2026-03-20): "
        f"**{afbouw_step['diff_post_minus_pre']:+.2f} BB units** -- the empirical day-resolved afbouw-"
        "onset effect.",
        "",
        "### OPPOSITE-direction contrast with sister `all_day_stress_avg` afbouw-fully-recovers",
        "",
        "Per handoff section 2.4 + section 5.A of recovery_arc v2: bb_lowest's afbouw pattern is "
        "**OPPOSITE-direction from sister `all_day_stress_avg`'s afbouw-fully-recovers finding**:",
        "",
        "| channel | unmed median | buildup median | consolidation median | afbouw median | afbouw vs unmed | reversal pattern |",
        "|---|---:|---:|---:|---:|---:|---|",
        "| `stress_mean_sleep` (Q3.1) | 17.04 | -- | 19.07 | 20.20 | +3.16 | afbouw HIGHER than unmed (citalopram benefit reverses) |",
        "| `all_day_stress_avg` (Q3.2) | 34.0 | 28.5 | 31.0 | 34.0 | 0.0 | afbouw FULLY RECOVERS to unmed baseline |",
        f"| **`bb_lowest` (this analysis)** | **{unmed_med:.1f}** | **{buildup_med:.1f}** | **{consol_med:.1f}** | **{afbouw_med:.1f}** | **{afbouw_minus_unmed:+.1f}** | afbouw {'GOES LOWER THAN unmed baseline -- INVERTS' if afbouw_minus_unmed < 0 else 'recovers toward unmed baseline'} |",
        "",
        "**This is the substantive cross-channel observation per handoff section 2.4 + STOCKTAKE section "
        "6 line 187**: on the 3 CONFIRMED-citalopram channels at this corpus snapshot, the afbouw pattern "
        "is **channel-specific** -- some channels recover toward unmed baseline (all_day_stress_avg), "
        "some go HIGHER (stress_mean_sleep, consistent with the +β prior), and bb_lowest INVERTS to "
        "BELOW unmed baseline (NOT just the inverse of stress channels' afbouw-rises; it goes LOWER than "
        "the unmedicated floor). Three readings, none asserted as substantive truth per CONVENTIONS "
        "section 2.1 + section 4.3:",
        "",
        "1. **The beta is a within-buildup-window dose-trend, not a between-phase steady-state level "
        "shift.** The v3 dose-response MD's beta is the slope of `bb_lowest` against `dose_plasma_mg(d)` "
        "*within* the buildup-window (2024-04-09 to 2024-06-19); it measures how the channel changes as "
        "dose rises from 0 to 30mg over ~70 days. Across phases, the LC-trajectory's broader recovery "
        "arc PLUS the citalopram step PLUS pacing-practice strengthening all overlap; the between-phase "
        "level shift can move opposite to the within-window beta if the broader trajectory dominates. The "
        "recovery_arc v2 analysis ([`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/)) "
        "documents this trajectory at multi-channel detail.",
        "",
        "2. **The dose-adjusted-predictor pattern under "
        "[`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 5.B is the framework-prescribed cross-phase treatment**: predictor = "
        "`bb_lowest - (-1.134)*dose = bb_lowest + 1.134*dose`. Any HA-C4b BB-floor pre-reg "
        "considering this channel cross-phase MUST adopt one of section 5.A / 5.B / 5.C per the inheritance "
        "table in `citalopram_phase_stratification.md section 4` (this channel is load-bearing CONFIRMED).",
        "",
        f"3. **The afbouw reversal IS the multi-year-trajectory signature**: per recovery_arc v2 section "
        f"5.A this channel is the standout where citalopram benefit doesn't just disappear during dose "
        f"reduction, it inverts. The afbouw median {afbouw_med:.1f} sits BELOW even the unmedicated "
        f"baseline {unmed_med:.1f} -- a graded buildup -> consolidation -> afbouw downward arc that "
        f"continues past the unmedicated baseline. Note: this is a Layer 1 observation; the recovery_arc "
        f"analysis is the load-bearing artefact for substantive readings.",
        "",
        "### HA10 single-pool re-anchor descriptive cross-reference (load-bearing per handoff section 2.4)",
        "",
        "HA10 (BB overnight recharge proxy, primary channel `bb_highest`) is LOCKED at TRAIN REFUTED "
        "(-20.5 pp) / VALIDATE SUPPORTED (+16.2 pp) / OVERALL REFUTED with era-directionality reversal. "
        "R14 single_pool_reanchor (LANDED `badd04a`) showed this directionality reversal **flattens cleanly "
        "under single-pool re-anchor to +4.1 pp [CI -16.5, +16.8], perm p=0.4328, NOT-SUPPORTED CONVERGE-"
        "ON-OVERALL**. The descriptive substrate this analysis produces -- the per-phase signal in "
        f"Q3.3.c + the citalopram-axis trajectory in Q3.3.d (unmed {unmed_med:.1f} -> buildup "
        f"{buildup_med:.1f} -> consolidation {consol_med:.1f} -> afbouw {afbouw_med:.1f}) -- "
        "**descriptively corroborates** the R14 reading that the era-directionality reversal is "
        "consistent with a per-phase (per-citalopram-state) effect rather than a true per-era effect, "
        "because the LC era contains the unmedicated-to-citalopram-buildup boundary that the train-vs-"
        "validate split happens to straddle. The substantive HA10 verdict + the R14 single-pool verdict "
        "are LOCKED; this Q3.3.d descriptive observation is NOT a re-interpretation of either.",
        "",
        "See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) and "
        "[`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d rolling "
        "median through phases).",
        "",
        "---",
        "",
        "## Q3.3.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)",
        "",
        "Brief-mandated three channels (sister stress_mean_sleep + all_day_stress_avg + bb_overnight_gain) "
        "plus extended biologically-plausible neighbours (BB family + stress family + cardiovascular). "
        "The bb_overnight_gain pair appears here AND in Q3.3.k channel-specific extension for parity.",
        "",
        "| target channel | n | Pearson r | Spearman rho | near-identity flag? |",
        "|---|---:|---:|---:|---|",
        *near_id_rows,
        "",
        f"**{'Zero' if not e['flagged_pairs'] else len(e['flagged_pairs'])} near-identity pairs fire** at "
        "the |rho|>=0.92 CONVENTIONS section 3.3 threshold. The closest pairs and their substantive "
        "context live in Q3.3.k below for the bb_overnight_gain family; sister all_day_stress_avg "
        "rho-with-this-channel reciprocally confirms the rho=-0.749 inverse-direction signal reported in "
        "all_day_stress_avg Q3.2.e.",
        "",
        "---",
        "",
        "## Q3.3.f -- Crash-day vs normal-day (Stratum 4 refresh in operationalisation-support framing)",
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
        f"| mean per-episode `bb_lowest` | {fe['mean_per_episode_value']:.2f} |",
        f"| mean normal-day `bb_lowest` | {fe['mean_normal_day_value']:.2f} |",
        f"| mean diff (episode minus normal-day) | **{fe['mean_diff_episode_vs_normal_day']:+.2f}** |",
        f"| Cohen's d (episode-level vs normal-day pooled) | **{fe['cohens_d_episode_vs_normal_day']:+.2f}** |",
        f"| Bootstrap 95% CI on mean diff | **[{ci_ep[0]:+.2f}, {ci_ep[1]:+.2f}]** ({fe['n_bootstrap']} iters, seed={fe['seed']}) |",
        "",
        f"**Episode-level Cohen's d={fe['cohens_d_episode_vs_normal_day']:+.2f}** on this channel. "
        "Substantive direction prior: bb_lowest LOWER on crash days = depleted overnight floor (the "
        "Wiggers-aligned direction). Compare cross-channel: `stress_mean_sleep` episode d=+0.91 (sister "
        "+direction); `all_day_stress_avg` episode d=+0.37 with CI brushing zero; "
        "`stress_low_motion_min_count_S60_Mlow` episode d=+0.38.",
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
        f"| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **{('<0.0001' if mwu['p_two_sided'] < 0.0001 else format(mwu['p_two_sided'], '.4f'))}** |",
        f"| Mann-Whitney U: P(crash > normal) | **{mwu['p_crash_greater_than_normal']:+.3f}** |",
        f"| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (project default) | [{e7['ci_lower']:+.2f}, {e7['ci_upper']:+.2f}], width {width7:.2f} |",
        f"| Stationary bootstrap 95% CI on mean diff, **E[L]={eS['block_length_used']}** (data-driven, Q3.3.b flag) | **[{eS['ci_lower']:+.2f}, {eS['ci_upper']:+.2f}]**, width {widthS:.2f} |",
        "",
        f"### HA10 single-pool re-anchor cross-reference (load-bearing per handoff section 2.4)",
        "",
        "Per the R14 single_pool_reanchor result on HA10 (BB-recharge channel, NOT bb_lowest directly): "
        "the era-directionality reversal flattens to +4.1 pp CONVERGE-ON-OVERALL. **This analysis's "
        f"crash-vs-normal read on bb_lowest is the floor-side companion to HA10's peak-side test.** The "
        f"episode-level signal observed here (d={fe['cohens_d_episode_vs_normal_day']:+.2f} on the "
        f"floor) provides cross-construct context for any HA-C4b BB-floor pre-reg that wants to use "
        f"bb_lowest as primary; that pre-reg should adopt section 5.A / 5.B / 5.C per the citalopram-"
        f"phase inheritance rule (Q3.3.i covariate-readiness arm 1) AND should pre-spec the long-"
        f"autocorrelation E[L]\\*={el_int} block-length sensitivity per Q3.3.b.",
        "",
        "### Block-length sensitivity (Q3.3.b cross-check)",
        "",
        "Per "
        "[`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md), "
        "when the data-driven E[L]\\* deviates from the project default by more than a factor of 2, the "
        "analysis must report the CI at the data-driven value alongside the default. "
        f"E[L]={eS['block_length_used']} CI ([{eS['ci_lower']:+.2f}, {eS['ci_upper']:+.2f}]) vs E[L]=7 "
        f"CI ([{e7['ci_lower']:+.2f}, {e7['ci_upper']:+.2f}]) -- {abs(width_change_pct):.1f}% "
        f"{'wider' if width_change_pct > 0 else 'narrower'} at the data-driven block length.",
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
        "See [`plots/fig4_crash_vs_normal.png`](plots/fig4_crash_vs_normal.png).",
        "",
        "---",
        "",
        "## Q3.3.g -- Spike-detecting primitive availability",
        "",
        "`bb_lowest` is **structurally the daily NADIR** (UDS-pre-aggregated; JSON-passthrough from "
        "`daily_uds.csv`; no FIT parsing per `garmin_indicators_audit.md` Wave-3 propagation 2026-06-12). "
        "Per CONVENTIONS section 3.5 it IS the spike-form primitive on the BB-floor construct (the "
        "depleted-state extremum of the day); it is NOT a dilution-vulnerable continuous-mean form like "
        "the sister stress channels' 24h-window means. Sub-daily BB resolution is **not in `per_day_master.csv`** "
        "and NOT in the GDPR dump per [bb_overnight_gain_proxy.md section 6 caveat 5](../../../methodology/bb_overnight_gain_proxy.md).",
        "",
        "BB-related primitives in the master:",
        "",
        "| column | n_non_nan (S4) | type | relation to `bb_lowest` |",
        "|---|---:|---|---|",
        f"| `bb_highest` | {sum(1 for x in g.get('spike_primitives_available_in_master', []) if x.get('column') == 'bb_highest') and g.get('spike_primitives_available_in_master')[0].get('n_non_nan') or 'n/a'} | daily peak (24h max) | Pearson r=**{g.get('pearson_r_vs_bb_highest', 0):+.2f}** / rho={g.get('spearman_rho_vs_bb_highest', 0):+.2f}; complementary BB extremum |",
        f"| `bb_sleep_start_value` | -- | anchor: BB at sleep start | Pearson r=**{g.get('pearson_r_vs_bb_sleep_start_value', 0):+.2f}** / rho={g.get('spearman_rho_vs_bb_sleep_start_value', 0):+.2f}; the recharge-arc starting point |",
        f"| `bb_sleep_end_value` | -- | anchor: BB at sleep end | Pearson r=**{g.get('pearson_r_vs_bb_sleep_end_value', 0):+.2f}** / rho={g.get('spearman_rho_vs_bb_sleep_end_value', 0):+.2f}; the recharge-arc ending point |",
        f"| `bb_during_sleep_value` | -- | sleep-window-averaged BB | Pearson r=**{g.get('pearson_r_vs_bb_during_sleep_value', 0):+.2f}** / rho={g.get('spearman_rho_vs_bb_during_sleep_value', 0):+.2f} |",
        f"| `bb_overnight_gain` | -- | SLEEPEND - SLEEPSTART (recharge arc) | Pearson r=**{g.get('pearson_r_vs_bb_overnight_gain', 0):+.2f}** / rho={g.get('spearman_rho_vs_bb_overnight_gain', 0):+.2f}; HA10 primary (Q3.3.k) |",
        f"| `bb_overnight_gain_best` | -- | best (truth + proxy) recharge | Pearson r=**{g.get('pearson_r_vs_bb_overnight_gain_best', 0):+.2f}** / rho={g.get('spearman_rho_vs_bb_overnight_gain_best', 0):+.2f}; coverage-extended HA10 |",
        "",
        "### CONVENTIONS section 3.5 framing -- the NADIR IS the spike-form on the BB-floor construct",
        "",
        "Unlike the sister stress channels where the continuous-form (24h mean) and spike-form (low-"
        "motion-count, max-spike-minutes) live in separate columns, **bb_lowest is a single extremum-form "
        "column**: the depleted-state floor reached at any point in the 24h window. A consumer test "
        "whose mechanism is *acute BB-floor depletion* should use bb_lowest as primary -- it IS the "
        "extremum operand. A consumer test whose mechanism is *overnight recharge magnitude* should use "
        "bb_overnight_gain (Q3.3.k) as primary. A consumer test whose mechanism is *daily peak* should "
        "use bb_highest (HA10 primary).",
        "",
        "**Latent in FIT, not in master**: per-minute body-battery samples are absent from the GDPR dump "
        "entirely per [bb_overnight_gain_proxy.md section 6 caveat 5](../../../methodology/bb_overnight_gain_proxy.md) "
        "(\"No per-minute BB anywhere in the dump\"). Within-day BB-spike-density at finer-than-daily "
        "resolution is structurally unavailable; this is not a project-side extraction gap but a Garmin-"
        "side data-export gap. This analysis does NOT action it.",
        "",
        "---",
        "",
        "## Q3.3.h -- Outlier detection + calibration-drift check",
        "",
        "Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) "
        "+ load-bearing [`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md):",
        "",
        "- This channel is a **UDS-side passthrough** from `daily_uds.csv`; no FIT parsing needed; "
        "part of the Body Battery family extracted via Wave-3 JSON-side propagation 2026-06-12.",
        "- **No specific calibration-drift events catalogued for `bb_lowest`** in "
        "`garmin_indicators_audit.md`; the audit's per-column provenance map covers BB channels "
        "collectively under the UDS-passthrough rows rather than per-column for the daily-aggregate floor.",
        "- Underlying sensor is **Forerunner 245 Elevate V3 throughout the entire 2021-08-16 to present "
        "window** -- no device change in the analytic window. Per bb_overnight_gain_proxy.md section 6 "
        "caveat 1 the single-watch / single-firmware-family discipline extends to all BB columns.",
        "- **Coverage-bridge framing applied (load-bearing per handoff section 2.4)**: "
        "bb_overnight_gain_proxy.md establishes r=0.989 vs truth post-2024-09-18 + sensitivity-only "
        "for the 2024-07-08 -> 2024-09-17 bridge window. bb_lowest itself has NO equivalent rollout "
        "gap (Q3.3.j confirms full corpus coverage from 2021); the coverage-bridge discipline applies "
        "to bb_overnight_gain pairing (Q3.3.k), not to bb_lowest directly.",
        "",
        "### Outlier scan (MAD-based |z|>5; threshold per CONVENTIONS section 3.1 robust-baseline default)",
        "",
        f"**{len(outliers)} outlier-day flagged** out of {a['n']}:",
        "",
        ("| date | value | MAD-z |\n|---|---:|---:|\n" + "\n".join(
            f"| {o['date']} | {o['value']:.1f} | **{o['mad_z']:+.2f}** |" for o in outliers[:20]
        )) if outliers else "**No outliers above the |z|>5 threshold.** The NADIR channel is bounded near 5-69 on this corpus; the |z|>5 rule is unlikely to fire on a bounded extremum-form channel with mass concentrated in the 10-30 range.",
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
        f"The rolling 90d median shows the multi-year lift documented in recovery_arc v2 (12 healthy -> "
        f"22 phase 5 maximum), and the day-resolved citalopram boundary step (2024-04-09) shows "
        f"trailing-30d mean = {citalo_step['pre_30d_mean']:.2f} vs leading-30d mean = "
        f"{citalo_step['post_30d_mean']:.2f} -- a **{citalo_step['diff_post_minus_pre']:+.2f} step**, "
        f"~{abs(citalo_step['diff_post_minus_pre']) / a['mad_unscaled']:.1f} channel-MADs. The "
        f"consolidation-boundary step at 2024-06-20 shows {consol_step['pre_30d_mean']:.2f} -> "
        f"{consol_step['post_30d_mean']:.2f} = **{consol_step['diff_post_minus_pre']:+.2f}**. The "
        f"**afbouw boundary step at 2026-03-20 shows {afbouw_step['pre_30d_mean']:.2f} -> "
        f"{afbouw_step['post_30d_mean']:.2f} = {afbouw_step['diff_post_minus_pre']:+.2f}** -- the day-"
        "resolved afbouw drop in the same window where recovery_arc v2 section 5.A surfaces the load-"
        "bearing reversal.",
        "",
        "**This is NOT a calibration-drift signature** -- the shifts are precisely time-located at "
        "documented intervention boundaries (citalopram dose ramp + afbouw onset), and the multi-year "
        "lift aligns with the documented LC recovery arc. A calibration-drift signature would be a "
        "gradual monotonic creep unrelated to documented events; this channel shows the opposite -- "
        "structured shifts at known boundaries.",
        "",
        "See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).",
        "",
        "---",
        "",
        "## Q3.3.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel",
        "",
        "Discipline anchor: "
        "[HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) "
        "(secondary-logistic-with-covariate pattern; beta disambiguation between primary-signal and a "
        "candidate alternative reading). Names **four** candidate covariates a future HA on `bb_lowest` "
        "as predictor should pre-spec:",
        "",
        "### 1. `dose_plasma_mg(d)` -- obligatory under "
        "[`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5.B",
        "",
        "The channel is CONFIRMED dose-modulated at -1.134/mg p=0.000 (the LARGEST ABSOLUTE beta among "
        "the 3 CONFIRMED channels in INVERSE direction). A future HA MUST either section 5.A per-phase "
        "stratify or section 5.B dose-adjust. The section 5.B operationalisation on this channel: "
        "`bb_lowest_adj(d) = bb_lowest(d) - (-1.134) * dose_plasma_mg(d) = bb_lowest(d) + 1.134 * dose_plasma_mg(d)`. "
        "At 30mg steady-state the adjustment subtracts ~+34 BB units from bb_lowest, which is larger "
        "than the channel's full IQR -- a structural sanity flag for the section 5.B treatment on this "
        "specific channel: the dose-adjusted predictor sits in a very different numerical range than the "
        "raw channel; the rolling baseline operates on the corrected signal.",
        "",
        "### 2. `bb_overnight_gain` (HA10 primary; or bb_overnight_gain_best with coverage extension)",
        "",
        (
            f"On Stratum 4 observed (this analysis Q3.3.k): Pearson r="
            f"{i['candidate_covariates'][1]['observed_correlation_on_S4']['pearson_r']:+.3f} / Spearman "
            f"rho={i['candidate_covariates'][1]['observed_correlation_on_S4']['spearman_rho']:+.3f} "
            f"(n={i['candidate_covariates'][1]['observed_correlation_on_S4']['n']}). HA10's primary "
            f"BB-recharge channel."
        ) if i['candidate_covariates'][1].get('observed_correlation_on_S4') else "bb_overnight_gain pair: see Q3.3.k for the operational pair statistics.",
        "",
        "The covariate disambiguates: is the bb_lowest signal driven by the depleted-state floor "
        "(beta_channel survives -- bb_lowest carries information beyond the recharge magnitude) or by "
        "the recharge magnitude itself (beta_channel attenuates -- bb_overnight_gain was doing the "
        "work). NOTE: coverage discipline per bb_overnight_gain_proxy.md applies if pre-2024-09-18 days "
        "enter the analysis.",
        "",
        "### 3. `all_day_stress_avg` -- sister CONFIRMED-citalopram channel (strongest inverse neighbour)",
        "",
        (
            f"On Stratum 4 observed (this analysis Q3.3.e): Pearson r="
            f"{i['candidate_covariates'][2]['observed_correlation_on_S4']['pearson_r']:+.3f} / Spearman "
            f"rho={i['candidate_covariates'][2]['observed_correlation_on_S4']['spearman_rho']:+.3f} "
            f"(n={i['candidate_covariates'][2]['observed_correlation_on_S4']['n']}). Sister CONFIRMED-"
            "citalopram channel; INVERSE-direction neighbour."
        ) if i['candidate_covariates'][2].get('observed_correlation_on_S4') else "all_day_stress_avg pair: see Q3.3.e for the operational pair statistics.",
        "",
        "Both channels are CONFIRMED dose-modulated in opposite directions. The covariate disambiguates: "
        "BB-floor mechanism vs autonomic-state shared variance.",
        "",
        "### 4. `bb_lowest_lagged_lcera_z` -- already-materialised lagged-baseline covariate",
        "",
        f"Per Q3.3.b the cutoff lag M={b['cutoff_lag_M']} and E[L]\\*={el_star:.1f}. The "
        "`bb_lowest_lagged_lcera_z` column is ALREADY materialised in `per_day_master.csv` per "
        "CONVENTIONS section 3.2 _lagged_lcera convention (LC-era-only [d-90, d-30] trailing baseline). "
        f"A consumer HA can use it directly OR compute a shorter-window covariate at N={el_int}d or "
        "N=28d for the autocorrelation-vs-mechanism disambiguation.",
        "",
        "### Recommendation for any HA pre-reg on this channel",
        "",
        "Pre-spec all four covariates as **secondary sensitivity arms**. Concordance across the four "
        "secondaries = high confidence in the primary; divergence = the disambiguation is doing real "
        "work. The section 5.B citalopram-dose adjustment is **obligatory** per the framework AND per "
        "this channel being the LARGEST-absolute-beta CONFIRMED member; the BB-pair (covariate 2) is "
        "the BB-construct disambiguator; the cross-channel (covariate 3) is the BB-floor-vs-autonomic-"
        "state disambiguator; the autocorrelation-vs-mechanism arm (covariate 4) operationalises HA-P7 "
        "section 4.5.4 on this specific channel. HA-C4b BB-floor pre-reg (deferred per STOCKTAKE "
        "section 6) is the natural consumer.",
        "",
        "---",
        "",
        "## Q3.3.j (channel-specific) -- BB-source coverage",
        "",
        f"**`bb_lowest` has full corpus coverage from {j['first_non_nan_date_full_corpus']} onward** "
        f"({j['n_non_nan_full_corpus']} / {j['n_rows_full_corpus']} = "
        f"{j['share_of_corpus_pct']:.2f}% of corpus rows). Last non-nan: "
        f"{j['last_non_nan_date_full_corpus']}.",
        "",
        "### Per-phase coverage on Stratum 4",
        "",
        "| phase | n days in window | n with channel | coverage % |",
        "|---|---:|---:|---:|",
        *j_rows,
        "",
        "### Contrast with bb_overnight_gain (HA10 primary; load-bearing coverage-bridge per handoff section 2.4)",
        "",
        f"bb_overnight_gain: first non-nan {j['contrast_with_bb_overnight_gain']['first_non_nan']}; "
        f"{j['contrast_with_bb_overnight_gain']['n_non_nan_full_corpus']} / "
        f"{j['n_rows_full_corpus']} = "
        f"{j['contrast_with_bb_overnight_gain']['share_of_corpus_pct']:.2f}% of corpus rows.",
        "",
        "Per [bb_overnight_gain_proxy.md section 1 + section 5.4](../../../methodology/bb_overnight_gain_proxy.md): "
        "bb_overnight_gain is **structurally absent for ~64% of LC corpus pre-2024-09-18** because "
        "Garmin's UDS export rolled the underlying stats out in two stages on this user's FR245 -- "
        "SLEEPSTART first emitted 2024-07-08; SLEEPEND first emitted 2024-09-18. This is a Garmin-side "
        "schema rollout, NOT a project-side pipeline gap. The `bb_overnight_gain_best` fused channel "
        "rescues 74 days of pre-2024-09-18 coverage via the bb_overnight_gain_proxy = HIGHEST - "
        "SLEEPSTART (validated at r=0.989 vs truth post-2024-09-18; section 4 discipline rules govern "
        "consumer use).",
        "",
        "### Verdict (operational consequence)",
        "",
        j["verdict"],
        "",
        "---",
        "",
        "## Q3.3.k (channel-specific) -- Relationship to bb_overnight_gain (HA10 primary)",
        "",
        "**Discipline anchor**: " + k["discipline_anchor"] + ".",
        "",
        "Pair statistics on Stratum 4:",
        "",
        "| target channel | n | Pearson r | Spearman rho | near-identity flag? | window |",
        "|---|---:|---:|---:|---|---|",
        *k_rows,
        "",
        "### Source-conditioned check for bb_overnight_gain_best (per bb_overnight_gain_proxy.md discipline rule 1)",
        "",
    ]

    bgo_best_info = k["pairs"].get("bb_overnight_gain_best", {})
    if bgo_best_info.get("source_truth_n") is not None:
        out_lines.extend([
            f"On the {bgo_best_info.get('n', 0)} bb_lowest <-> bb_overnight_gain_best pair days: "
            f"**{bgo_best_info.get('source_truth_n', 0)} truth-source days** "
            f"(post-2024-09-18 SLEEPEND-emitted nights) + **{bgo_best_info.get('source_proxy_n', 0)} "
            "proxy-source days** (the 2024-07-08 -> 2024-09-17 bridge + 3 post-rollout SLEEPEND-failure "
            "nights per bb_overnight_gain_proxy.md section 5.4).",
            "",
        ])
        if bgo_best_info.get("pearson_r_truth_only") is not None:
            out_lines.append(
                f"Truth-only subset: Pearson r={bgo_best_info['pearson_r_truth_only']:+.3f} / "
                f"Spearman rho={bgo_best_info['spearman_rho_truth_only']:+.3f}."
            )
        if bgo_best_info.get("pearson_r_proxy_only") is not None:
            out_lines.append(
                f"Proxy-only subset: Pearson r={bgo_best_info['pearson_r_proxy_only']:+.3f} / "
                f"Spearman rho={bgo_best_info['spearman_rho_proxy_only']:+.3f}."
            )
        out_lines.append("")
    else:
        out_lines.append(
            "Source-conditioned subgroup statistics: n in proxy-source subset is too small to "
            "stratify; report aggregate pair only."
        )
        out_lines.append("")

    out_lines.extend([
        "### Substantive gap description",
        "",
        k["substantive_gap_description"],
        "",
        "### Operational consequence",
        "",
        k["operational_consequence"],
        "",
        "---",
        "",
        "## Cross-references",
        "",
        "### HA-* tests that touch this channel (cite this analysis)",
        "",
        "- **HA10** (BB overnight recharge, LOCKED `analyses/hypotheses/HA10-bb-overnight-recharge/result.md`): "
        f"primary channel is `bb_highest` (not bb_lowest); bb_lowest is the complementary floor "
        f"primitive. R14 single_pool_reanchor (`badd04a`) flattened the era-directionality reversal "
        f"-20.5 / +16.2 to +4.1 pp CONVERGE-ON-OVERALL on the recharge channel. **The descriptive "
        f"substrate this analysis produces -- per-phase trajectory (Q3.3.c, Q3.3.d) + crash-vs-normal "
        f"(Q3.3.f) on the floor channel -- complements HA10's peak-channel result with floor-side "
        f"context.** The substantive HA10 verdict + the R14 single-pool verdict are LOCKED; this "
        f"analysis's descriptive corroboration is NOT a re-interpretation.",
        "- **HA-P6 v3** (descriptive Layer 1; LOCKED `a980b1c` 2026-06-17): bb_lowest is one of the "
        f"4/7 distinguishable channels in the matched-control framework. The descriptive substrate this "
        f"analysis produces (E[L]\\*={el_star:.1f}, autocorrelation context; episode-level "
        f"d={fe['cohens_d_episode_vs_normal_day']:+.2f}; per-phase trajectory; afbouw reversal) provides "
        "context for the HA-P6 result reading on this specific channel.",
        "- **HA-C4b** (BB-floor candidate; DEFERRED per STOCKTAKE section 6): the natural consumer of "
        "this descriptive analysis. The deferred status awaits per-minute primitive availability, which "
        "Q3.3.g + bb_overnight_gain_proxy.md section 6 caveat 5 confirm is **not in the GDPR dump** -- "
        "any HA-C4b pre-reg using bb_lowest as primary at daily resolution would inherit this analysis's "
        "operationalisation substrate (Q3.3.i covariate-readiness arm; Q3.3.d phase-stratified anchor; "
        "Q3.3.f crash-vs-normal floor).",
        "",
        "### Methodology MDs cited",
        "",
        "- [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) -- "
        "Q3.3.a delegate target (partial; extended for the full skewness/kurtosis/heavy-tail-flag set on "
        "this channel).",
        "- "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "sections 3-6 -- Q3.3.c phase axis, Q3.3.d phase-stratified treatment, Q3.3.i covariate framework.",
        "- "
        "[`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "v3 section 5.6.1 -- locked -1.134/mg dose-response slope (largest absolute beta among 3 CONFIRMED "
        "channels; INVERSE direction).",
        "- "
        "[`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) "
        f"-- E[L]=7 default + factor-of-2 deviation rule; Q3.3.b reports E[L]\\*={el_star:.1f} "
        f"({'factor-of-2 flag fires' if b['factor_of_2_deviation_flag'] else 'flag does not fire'}).",
        "- "
        "[`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md) "
        "-- load-bearing coverage-bridge MD for Q3.3.h + Q3.3.j + Q3.3.k (r=0.989 vs truth post-2024-09-18; "
        "sensitivity-only for 2024-07-08 -> 2024-09-17 bridge).",
        "- "
        "[`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) -- "
        "Q3.3.h cross-reference; BB-family per-column rows absorbed into UDS-passthrough collective rows.",
        "- "
        "[`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) "
        "-- Stratum 4 boundary definition.",
        "",
        "### Existing artefacts referenced",
        "",
        "- [`descriptive/operationalisation_support/stress_mean_sleep/findings.md`](../stress_mean_sleep/findings.md) "
        f"-- sister CONFIRMED-citalopram channel; first Phase-1 Strand A analysis; cross-channel "
        f"comparison anchors throughout (E[L]\\* {el_star:.1f} here vs 12.6 there).",
        "- [`descriptive/operationalisation_support/all_day_stress_avg/findings.md`](../all_day_stress_avg/findings.md) "
        f"-- sister CONFIRMED-citalopram channel; Phase-2 Q3.2 precedent; OPPOSITE-direction afbouw "
        f"contrast surfaced in Q3.3.d.",
        "- [`descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/findings.md`](../stress_low_motion_min_count_S60_Mlow/findings.md) "
        "-- spike-form companion for the stress family; third Phase-1 Strand A analysis; cross-pair "
        "r=+0.85 / rho=+0.86 with sister all_day_stress_avg.",
        "- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) "
        "-- R14 cross-check (LANDED `badd04a`); the HA10 row descriptively corroborated in Q3.3.d.",
        "- [`descriptive/trajectory/recovery_arc/findings.md`](../../trajectory/recovery_arc/findings.md) "
        "-- v2 LANDED 2026-06-22 (`8feae6a`); section 5.A afbouw-reversal finding load-bearing in "
        "Q3.3.d.",
        "- [`analyses/hypotheses/HA10-bb-overnight-recharge/result.md`](../../hypotheses/HA10-bb-overnight-recharge/result.md) "
        "-- LOCKED OVERALL-REFUTED with era-directionality reversal; bb_lowest is the floor-side "
        "companion to HA10's peak-side primary.",
        "- [`analyses/hypotheses/HA-P6/result.md`](../../hypotheses/HA-P6/result.md) -- v3 LOCKED "
        "`a980b1c` 2026-06-17; bb_lowest is one of 4/7 distinguishable channels.",
        "- [`analyses/garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) "
        "-- Q3.3.e cross-reference for the 7-channel panel; this analysis surfaces the bb_lowest "
        "<-> all_day_stress_avg rho=-0.749 reciprocal pair already documented from the stress-side at "
        "Q3.2.e.",
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
        "1. **Q3.3.c-d are on raw channel values, not dose-adjusted.** Per "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 5, any HA using `bb_lowest` cross-phase MUST adopt section 5.A / 5.B / 5.C treatment. "
        "Q3.3.d explains the citalopram-axis dynamics descriptively; a section 5.B dose-adjusted phase "
        "comparison is the natural follow-up but lives in the HA pre-reg, not here.",
        "2. **The channel IS the daily NADIR (a spike-form extremum) per CONVENTIONS section 3.5** "
        "(Q3.3.g); the discipline distinction is reversed from the stress channels' continuous-form/"
        "spike-form pairing. A future HA whose mechanism is *overnight recharge magnitude* should use "
        "bb_overnight_gain (HA10's primary; coverage-discipline per bb_overnight_gain_proxy.md), NOT "
        "bb_lowest. A future HA whose mechanism is *peak BB during the day* should use bb_highest.",
        f"3. **The episode-level Cohen's d={fe['cohens_d_episode_vs_normal_day']:+.2f} CI is "
        f"[{ci_ep[0]:+.2f}, {ci_ep[1]:+.2f}]** (Q3.3.f). The episode-level is the unit-of-analysis-clean "
        "read per CONVENTIONS section 3.6; consumer HAs using this channel as a crash-discriminator "
        "should NOT rely on the day-level (autocorrelation-inflated) as the primary read.",
        f"4. **Block-length sensitivity matters** (Q3.3.b E[L]\\*={el_star:.1f} vs default 7). Consumer "
        "tests using this channel with autocorrelation-controlled methods should pre-spec the "
        f"E[L]\\*~{el_int} sensitivity arm alongside the default-E[L]=7 primary.",
        "5. **The afbouw-reversal finding is descriptively striking but Layer-1 only**: per Q3.3.d the "
        f"afbouw median {afbouw_med:.1f} {'sits BELOW' if afbouw_med < unmed_med else 'returns toward'} "
        f"the unmedicated baseline {unmed_med:.1f}; cross-referenced load-bearing in [recovery_arc v2 "
        "section 5.A](../../trajectory/recovery_arc/findings.md) + [STOCKTAKE section 6 line 187](../../../STOCKTAKE.md). "
        "The substantive afbouw-reversal interpretation lives in recovery_arc v2; this analysis's "
        "Q3.3.d corroborates it descriptively but does NOT extend or promote the substantive reading.",
        "6. **Q3.3.j confirms full corpus coverage for bb_lowest itself** (no Garmin schema rollout gap), "
        "but Q3.3.k applies the bb_overnight_gain_proxy.md coverage-bridge discipline to the "
        "bb_overnight_gain pairing; any consumer HA combining bb_lowest with bb_overnight_gain must "
        "report proxy-share per bb_overnight_gain_proxy.md section 4 discipline rule 1.",
        "7. **Per-minute BB primitive is NOT in the GDPR dump** per bb_overnight_gain_proxy.md section 6 "
        "caveat 5 (Q3.3.g + Q3.3.g latent-in-FIT note). Within-day BB-floor density at finer-than-daily "
        "resolution is structurally unavailable; HA-C4b BB-floor at daily resolution is the maximum "
        "resolution achievable on this corpus.",
        "8. **HA10 + HA-P6 v3 verdicts are LOCKED with R14 single-pool re-anchor descriptively "
        "corroborating.** This analysis's Q3.3.c + Q3.3.d + Q3.3.f cross-references are descriptive "
        "corroboration only; the locked verdicts are NOT extended by this analysis per CONVENTIONS "
        "section 4.2 (caveats yes; a-priori claims no).",
        "",
        "---",
        "",
        "## Status",
        "",
        "**Current as of 2026-06-24** (commit context: post-`cf34ab1` Q3.2 all_day_stress_avg LANDED; "
        "Phase 2 \"finish the descriptive analysis\" Tier 1 user-prioritised CONFIRMED-citalopram channel "
        "#3 of 3; R14 `single_pool_reanchor` first at `badd04a`; `all_day_stress_avg` second at "
        "`cf34ab1`; this `bb_lowest` third; `stress_stdev_sleep` closes Tier 1 next). Refresh when:",
        "",
        "1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to "
        "spin up (per CONVENTIONS section 3.1 personal-baseline freshness).",
        "2. A new citalopram-phase boundary lands (e.g. post-afbouw enters analytic scope as of "
        "2026-06-06 onward).",
        f"3. The Politis-White E[L]\\* shifts by another factor of 2 from current {el_star:.1f}.",
        "4. HA-C4b BB-floor pre-reg unblocks (per STOCKTAKE section 6 deferred status) and triggers "
        "operationalisation-substrate consumption from this analysis.",
        "5. Per-minute BB primitive becomes available (currently not in GDPR dump; would re-open "
        "Q3.3.g sub-daily spike-density question).",
        "6. recovery_arc v3 refresh ships and updates the section 5.A afbouw-reversal characterisation; "
        "this analysis's Q3.3.d would refresh in lockstep.",
        "",
    ]
    )
    path.write_text("\n".join(out_lines), encoding="utf-8")


def write_readme_md(summary: dict, path: Path) -> None:
    """Emit the per-analysis README per descriptive/README section 7a pattern."""
    q = summary["questions"]
    a = q["Q3.3.a_distribution"]
    b = q["Q3.3.b_autocorrelation"]
    c = q["Q3.3.c_base_rates_per_phase"]
    fr = q["Q3.3.f_crash_vs_normal"]
    fe = fr["episode_level"]
    j = q["Q3.3.j_bb_source_coverage"]
    el_star = b["data_driven_E_L_star"]
    afbouw_med = c.get("afbouw", {}).get("median", float("nan"))
    unmed_med = c.get("unmedicated", {}).get("median", float("nan"))

    out_lines = [
        "# `bb_lowest` -- operationalisation-support descriptive analysis",
        "",
        "**Strand**: A (operationalisation support; template-driven; no operationalisation interview "
        "required per [`descriptive/README.md`](../../README.md) section 7b).",
        "",
        "## Research question",
        "",
        "Operationalisation-support descriptive characterisation of `bb_lowest` on Stratum 4, answering "
        "Q3.3.a-k per the locked descriptive programme spec at "
        "[`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.3 (LOCKED 2026-06-18 "
        "r3, commit `ccbd12e`). Phase 2 \"finish the descriptive analysis\" Tier 1 user-prioritised "
        "sequential batch; **third (final) of the 3 CONFIRMED-citalopram channels** (R14 "
        "`single_pool_reanchor` first at `badd04a`; `all_day_stress_avg` second at `cf34ab1`; this "
        "`bb_lowest` third; `stress_stdev_sleep` closes Tier 1 next). This channel is the **CONFIRMED-"
        "citalopram channel with the largest absolute beta** (-1.134/mg p=0.000 buildup post-CPAP per "
        "[`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "section 5.6.1; sister stress_mean_sleep +0.43/mg; sister all_day_stress_avg +0.57/mg; this "
        "channel -1.13/mg INVERSE direction; citalopram **raises** bb_lowest). **HA10 floor-side "
        "companion (HA10 primary is bb_highest)**; **HA-P6 v3 distinguishable channel** (4/7 in matched-"
        "control framework); **HA-C4b BB-floor candidate channel** (DEFERRED per STOCKTAKE section 6). "
        "**recovery_arc v2 standout** -- the channel where afbouw GOES LOWER than even unmedicated "
        "baseline (load-bearing finding per recovery_arc v2 section 5.A + STOCKTAKE section 6 line "
        "187).",
        "",
        "## Method",
        "",
        f"- **Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to "
        f"{summary['as_of_date']}; n={a['n']} channel-valid days out of "
        f"{summary['n_rows_stratum_4_total']} S4 days).",
        "- **Primary phase axis**: four-phase citalopram traject per "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with sister CONFIRMED-"
        "citalopram analyses.",
        "- **Delegate**: Q3.3.a (distribution shape) **partial delegate** to "
        "[`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) + "
        "**extend** with full skewness/kurtosis/heavy-tail-flag descriptors (the delegate target was "
        "extended for continuous channels first and primarily documents `stress_mean_sleep`).",
        "- **Cross-reference**: Q3.3.h (outliers + calibration-drift) cross-references "
        "[`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) "
        "(no per-column row for bb_lowest specifically; absorbed into UDS-passthrough collective rows) "
        "AND [`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md) "
        "as the load-bearing BB-family coverage-discipline MD.",
        "- **Computed directly from `per_day_master.csv`**: Q3.3.b (Politis-White E[L]\\*), Q3.3.c "
        "(per-phase base rates), Q3.3.d (phase-stratified medians + citalopram step + load-bearing "
        "afbouw-reversal cross-reference), Q3.3.e (near-identity check |rho|>=0.92 on 13-channel "
        "panel), Q3.3.f (crash-vs-normal Cohen's d + Mann-Whitney U + stationary-bootstrap CI at E[L]=7 "
        "and data-driven E[L]\\* + crash-drop sensitivity per section 3.4), Q3.3.g (NADIR-is-spike-"
        "form discussion + BB-family pairwise correlations), Q3.3.i (covariate-sensitivity readiness "
        "for future HA pre-regs).",
        "- **Channel-specific Q3.3.j + Q3.3.k extensions** per descriptive README section 3.3: Q3.3.j "
        "BB-source coverage (bb_lowest has full corpus coverage from 2021-08-16 -- 100% Stratum 4 "
        "minus UDS-side NaN gaps -- contrast with bb_overnight_gain ~37% of corpus); Q3.3.k "
        "relationship to bb_overnight_gain (HA10 primary; source-conditioned reads for "
        "bb_overnight_gain_best per bb_overnight_gain_proxy.md discipline rule 1).",
        "- **Shared utilities**: "
        "[`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-drop "
        "sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) "
        "(`compute_data_driven_block_length`, `stationary_bootstrap_ci`).",
        "- **Load-bearing cross-references** per handoff section 2.4: HA10 single-pool R14 re-anchor "
        "(badd04a) descriptively corroborated in Q3.3.d + Q3.3.f; recovery_arc v2 section 5.A "
        "afbouw-reversal reproduced + OPPOSITE-direction contrast with sister all_day_stress_avg "
        "afbouw-fully-recovers in Q3.3.d; recalibration -1.13/mg beta anchored in Q3.3.d; "
        "bb_overnight_gain_proxy.md coverage-bridge framing applied in Q3.3.h + Q3.3.j + Q3.3.k. NO "
        "substantive HA verdict promotion per CONVENTIONS section 2.1.",
        "- **No causal claims, no falsification bar** per "
        "[CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).",
        "",
        "## Result",
        "",
        "Headline (see [`findings.md`](findings.md) for the full answers Q3.3.a-k):",
        "",
        f"`bb_lowest` on Stratum 4 is a **daily-NADIR channel** (skew={a['skewness']:+.2f}, excess "
        f"kurtosis={a['excess_kurtosis']:+.2f}, heavy_tail_flag={a['heavy_tail_flag']}). **Data-driven "
        f"E[L]\\*={el_star:.1f}** -- vs sister Strand-A channels stress_mean_sleep 12.6 / "
        f"stress_low_motion 21.1 / all_day_stress_avg 29.8. **Phase-stratified medians track the "
        f"recovery_arc v2 section 5.A trajectory faithfully**: unmedicated {unmed_med:.1f} -> buildup "
        f"{c.get('buildup', {}).get('median', float('nan')):.1f} -> consolidation "
        f"{c.get('consolidation', {}).get('median', float('nan')):.1f} -> **afbouw {afbouw_med:.1f}** -- "
        f"afbouw {'GOES LOWER than unmedicated baseline (the load-bearing recovery_arc v2 section 5.A reversal)' if afbouw_med < unmed_med else 'recovers toward unmedicated baseline'}; "
        f"**OPPOSITE-direction from sister all_day_stress_avg afbouw-fully-recovers (per Q3.2.d 34.0 = "
        f"34.0 unmed)**. Episode-level Cohen's d={fe['cohens_d_episode_vs_normal_day']:+.2f}; bootstrap "
        f"CI95 [{fe['bootstrap_ci95_mean_diff'][0]:+.2f}, {fe['bootstrap_ci95_mean_diff'][1]:+.2f}]. "
        f"Q3.3.j: bb_lowest full corpus coverage from {j['first_non_nan_date_full_corpus']} onward "
        f"({j['share_of_corpus_pct']:.1f}% of corpus), contrast with bb_overnight_gain "
        f"({j['contrast_with_bb_overnight_gain']['share_of_corpus_pct']:.1f}% of corpus). Q3.3.k: "
        f"bb_lowest <-> bb_overnight_gain pair statistics in findings.md (source-conditioned per "
        f"bb_overnight_gain_proxy.md discipline rule 1).",
        "",
        "## Files",
        "",
        "- [`README.md`](README.md) -- this file",
        "- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + "
        "`README.md` + `plots/*.png`",
        "- [`findings.md`](findings.md) -- writeup covering Q3.3.a-k + tables (programmatically emitted "
        "by run.py from summary.json per the Q3.2 architectural note about the Write-tool harness "
        "heuristic on the literal filename \"findings\")",
        "- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per "
        "`docs/research/**/*.json`)",
        "- [`plots/`](plots/) -- 5 PNGs: distribution, phase-stratified violins, trajectory-with-phases, "
        "crash-vs-normal, ACF (gitignored per `docs/research/**/*.png`)",
        "",
        "## Status",
        "",
        "**Current as of 2026-06-24** (commit context: post-`cf34ab1` Q3.2 all_day_stress_avg LANDED; "
        "Phase 2 \"finish the descriptive analysis\" Tier 1 user-prioritised CONFIRMED-citalopram "
        "channel #3 of 3; R14 first at `badd04a`; Q3.2 second at `cf34ab1`; this Q3.3 third; "
        "`stress_stdev_sleep` closes Tier 1 next). Refresh when:",
        "",
        "1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to "
        "spin up.",
        "2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 onward).",
        f"3. Politis-White E[L]\\* shifts by another factor of 2 from current {el_star:.1f}.",
        "4. HA-C4b BB-floor pre-reg unblocks per STOCKTAKE section 6 and triggers operationalisation-"
        "substrate consumption.",
        "5. Per-minute BB primitive becomes available (currently not in GDPR dump per "
        "bb_overnight_gain_proxy.md section 6 caveat 5).",
        "6. recovery_arc v3 refresh ships and updates the section 5.A afbouw-reversal characterisation.",
        "",
        "## Cross-references",
        "",
        "- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 "
        "2026-06-18, commit `ccbd12e`)",
        "- **First Strand A analysis** (template anchor): "
        "[`descriptive/operationalisation_support/stress_mean_sleep/`](../stress_mean_sleep/) -- sister "
        "CONFIRMED-citalopram channel; first Phase-1 Strand A analysis.",
        "- **Second Strand A analysis** (Q3.2 most recent precedent): "
        "[`descriptive/operationalisation_support/all_day_stress_avg/`](../all_day_stress_avg/) -- "
        "sister CONFIRMED-citalopram channel; OPPOSITE-direction afbouw contrast surfaced in Q3.3.d.",
        "- **R14 single-pool re-anchor**: "
        "[`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) -- "
        "the HA10 row descriptively corroborated in Q3.3.d + Q3.3.f.",
        "- **Recovery arc** (Strand B): [`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/) "
        "v2 LANDED 2026-06-22 (`8feae6a`); section 5.A afbouw-reversal load-bearing in Q3.3.d.",
        "- **HA-* tests that this analysis anchors**:",
        "  - HA10 (LOCKED OVERALL-REFUTED with R14 single-pool CONVERGE-ON-OVERALL); primary is "
        "bb_highest -- bb_lowest is the complementary floor primitive.",
        "  - HA-P6 v3 (LOCKED `a980b1c` 2026-06-17); bb_lowest is 1 of 4/7 distinguishable channels.",
        "  - HA-C4b (DEFERRED per STOCKTAKE section 6); natural consumer for HA-C4b BB-floor pre-reg.",
        "- **Definitional substrate**: "
        "[`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "section 5.6.1 (locked -1.134/mg dose-response; INVERSE direction).",
        "- **Other methodology MDs**: `lc_phase_descriptive.md`, `citalopram_phase_stratification.md`, "
        "`permutation_null_block_length.md`, `bb_overnight_gain_proxy.md` (load-bearing), "
        "`garmin_indicators_audit.md`, `lc_era_temporal_segmentation.md`.",
        "- **Existing complementary**: "
        "[`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) "
        "(Q3.3.e cross-reference; reciprocally confirms the rho=-0.749 bb_lowest <-> all_day_stress_avg "
        "pair from the all_day_stress_avg Q3.2.e side).",
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

    # Use full corpus (not S4) for Q3.3.j coverage check; S4 for everything else
    full_master = master.copy()

    summary["questions"]["Q3.3.a_distribution"] = q_a_distribution(values)
    summary["questions"]["Q3.3.b_autocorrelation"] = q_b_autocorrelation(values)
    per_phase = q_c_base_rates_per_phase(s4, CHANNEL)
    summary["questions"]["Q3.3.c_base_rates_per_phase"] = per_phase
    summary["questions"]["Q3.3.d_phase_stratified_distribution"] = q_d_phase_stratified(per_phase, CHANNEL)
    summary["questions"]["Q3.3.e_near_identity"] = q_e_near_identity(s4, CHANNEL)
    summary["questions"]["Q3.3.f_crash_vs_normal"] = q_f_crash_vs_normal(s4, CHANNEL)
    summary["questions"]["Q3.3.g_spike_primitive"] = q_g_spike_primitive(s4, CHANNEL)
    summary["questions"]["Q3.3.h_outliers_calibration"] = q_h_outliers_calibration(s4, CHANNEL)
    summary["questions"]["Q3.3.i_covariate_readiness"] = q_i_covariate_readiness(s4, CHANNEL)
    summary["questions"]["Q3.3.j_bb_source_coverage"] = q_j_bb_source_coverage(full_master, CHANNEL)
    summary["questions"]["Q3.3.k_bb_overnight_gain_relationship"] = q_k_bb_overnight_gain_relationship(s4, CHANNEL)

    plot_files = make_plots(s4, CHANNEL, HERE / "plots")
    summary["plots"] = plot_files

    out_path = HERE / "summary.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    # Emit findings.md and README.md as programmatic outputs (per the Q3.2
    # precedent session's architectural note about the Write-tool harness
    # heuristic on the literal filename "findings").
    write_findings_md(summary, HERE / "findings.md")
    write_readme_md(summary, HERE / "README.md")

    print(f"Wrote {out_path}")
    print(f"Plots: {plot_files}")
    print("\n--- HEADLINE ---")
    a = summary["questions"]["Q3.3.a_distribution"]
    b = summary["questions"]["Q3.3.b_autocorrelation"]
    fr = summary["questions"]["Q3.3.f_crash_vs_normal"]
    print(f"Q3.3.a n={a['n']} mean={a['mean']:.2f} median={a['median']:.2f} MAD={a['mad_unscaled']:.2f} "
          f"skew={a['skewness']:.2f} heavy_tail={a['heavy_tail_flag']}")
    print(f"Q3.3.b E[L]*={b['data_driven_E_L_star']:.2f} (default 7); "
          f"factor-of-2 deviation flag={b['factor_of_2_deviation_flag']}; cutoff M={b['cutoff_lag_M']}")
    pp = summary["questions"]["Q3.3.c_base_rates_per_phase"]
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        if pp.get(ph, {}).get("n", 0) > 0:
            print(f"  Q3.3.c phase {ph}: n={pp[ph]['n']} med={pp[ph]['median']:.2f} MAD={pp[ph]['mad_unscaled']:.2f}")
    pd_d = summary["questions"]["Q3.3.d_phase_stratified_distribution"]
    print(f"Q3.3.d phase-to-phase median shifts:")
    for k_label, v in pd_d["phase_to_phase_shifts"].items():
        print(f"  {k_label}: {v:+.2f}")
    fl = fr["day_level"]
    e7 = fl["stationary_bootstrap_E_L7"]
    eS = fl["stationary_bootstrap_E_L_star"]
    print(f"Q3.3.f day-level: n_crash={fl['n_crash_day']} n_normal={fl['n_normal_day']} "
          f"d={fl['cohens_d']:.2f} mean_diff={fl['mean_diff']:.2f}")
    print(f"  E[L]=7  CI=[{e7['ci_lower']:.2f}, {e7['ci_upper']:.2f}] "
          f"width={e7['ci_upper'] - e7['ci_lower']:.2f}")
    print(f"  E[L]*={eS['block_length_used']} CI=[{eS['ci_lower']:.2f}, {eS['ci_upper']:.2f}] "
          f"width={eS['ci_upper'] - eS['ci_lower']:.2f}")
    mwu = fl["mann_whitney_u"]
    print(f"  Mann-Whitney U: z={mwu['z']:.2f} p={mwu['p_two_sided']:.4f} P(crash>normal)={mwu['p_crash_greater_than_normal']:.3f}")
    fe = fr["episode_level"]
    print(f"Q3.3.f episode-level: n_ep={fe['n_crash_episodes']} d={fe['cohens_d_episode_vs_normal_day']:.2f} "
          f"mean_diff={fe['mean_diff_episode_vs_normal_day']:.2f} CI={fe['bootstrap_ci95_mean_diff']}")
    cd = fr["crash_drop_sensitivity_on_spearman_vs_gevoelscore"]
    if cd is not None:
        print(f"Q3.3.f crash-drop on Spearman(bb_lowest, gevoelscore): full={cd['full_frame_value']:.3f} "
              f"crashed-dropped={cd['crash_dropped_value']:.3f} |delta|={cd['abs_delta']:.3f} "
              f">0.10? {cd['exceeds_threshold_0p10']}")
    e_near = summary["questions"]["Q3.3.e_near_identity"]
    print(f"Q3.3.e near-identity flagged: {e_near['flagged_pairs']}")
    h = summary["questions"]["Q3.3.h_outliers_calibration"]
    print(f"Q3.3.h outliers (|z|>5): {h['n_flagged']} flagged")
    j = summary["questions"]["Q3.3.j_bb_source_coverage"]
    print(f"Q3.3.j bb_lowest coverage: {j['n_non_nan_full_corpus']}/{j['n_rows_full_corpus']} "
          f"({j['share_of_corpus_pct']:.2f}%) from {j['first_non_nan_date_full_corpus']}")
    print(f"  contrast bb_overnight_gain: from {j['contrast_with_bb_overnight_gain']['first_non_nan']} "
          f"({j['contrast_with_bb_overnight_gain']['share_of_corpus_pct']:.2f}%)")
    kpairs = summary["questions"]["Q3.3.k_bb_overnight_gain_relationship"]["pairs"]
    for partner_name, info in kpairs.items():
        if "pearson_r" in info:
            print(f"Q3.3.k {partner_name}: n={info['n']} pearson={info['pearson_r']:+.3f} "
                  f"spearman={info['spearman_rho']:+.3f}")


if __name__ == "__main__":
    main()
