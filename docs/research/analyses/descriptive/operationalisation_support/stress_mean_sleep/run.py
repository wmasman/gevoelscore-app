"""Descriptive analysis: stress_mean_sleep operationalisation support.

Answers Q3.1.a-i per the locked descriptive programme:
``docs/research/analyses/descriptive/README.md`` §3.1 (LOCKED r3 2026-06-18,
commit ccbd12e). First Phase-1 first-analysis under Strand A
(template-driven; no operationalisation interview required).

Output: ``summary.json`` (machine-readable per-question results) +
``plots/*.png`` (visualisations). The hand-written ``findings.md`` reads
from these.

Discipline guards (per CONVENTIONS):
- §2.1 descriptive-before-inference: no causal claims; no falsification bar.
- §3.1 personal baseline: distribution shape is reported as-is; phase-
  stratified to surface the citalopram step rather than averaging across
  phases.
- §3.3 column-duplication: near-identity check at |rho|>=0.92.
- §3.4 crash-drop sensitivity: |Delta|>0.10 flag surfaced.
- §3.5 spike metrics: spike-primitive availability documented (Q3.1.g).
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
# HERE = .../analyses/descriptive/operationalisation_support/stress_mean_sleep
# parents[0]=operationalisation_support, [1]=descriptive, [2]=analyses, ...
UTILS_DIR = HERE.parents[2] / "_utils"  # analyses/_utils
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


CHANNEL = "stress_mean_sleep"
AS_OF_DATE = "2026-06-05"  # last LC-era day in master as observed; aligns with descriptive/README S4 right edge

# Citalopram phase boundaries per
# methodology/citalopram_phase_stratification.md §3
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
# Q3.1.a Distribution shape
# ---------------------------------------------------------------------------


def q_a_distribution(values: pd.Series) -> dict:
    """Distribution shape on Stratum 4 (Q3.1.a).

    Reports mean, median, MAD, quantiles, skewness, heavy-tail flag.
    Delegate-or-extend verdict against lc_phase_descriptive.md is decided
    in findings.md.
    """
    v = values.dropna().astype(float)
    n = int(len(v))
    mean = float(v.mean())
    median = float(v.median())
    std = float(v.std(ddof=1))
    mad = float(np.median(np.abs(v - median)))
    quantiles = {f"p{q}": float(np.percentile(v, q)) for q in (1, 5, 10, 25, 50, 75, 90, 95, 99)}
    # Sample skewness (Fisher-Pearson; matches scipy.stats.skew default)
    centered = v - mean
    m2 = float((centered ** 2).mean())
    m3 = float((centered ** 3).mean())
    skewness = m3 / (m2 ** 1.5) if m2 > 0 else float("nan")
    # Heavy-tail flag: p99/median ratio > 3 OR positive skew > 1
    heavy_tail = bool((quantiles["p99"] / median > 3.0) or skewness > 1.0)
    # Excess kurtosis (Fisher; normal = 0)
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
# Q3.1.b Autocorrelation + E[L]*
# ---------------------------------------------------------------------------


def q_b_autocorrelation(values: pd.Series) -> dict:
    """Autocorrelation structure + E[L]* (Q3.1.b).

    Drops NaN entries before estimating. The Politis-White estimator
    is robust to mild non-stationarity; we report both the data-driven
    optimum and the canonical default E[L]=7 from
    methodology/permutation_null_block_length.md.
    """
    arr = values.dropna().to_numpy()
    result = compute_data_driven_block_length(arr, default_block_length=7)
    acf = result["autocorrelations"]
    # Surface lag-1, lag-7, lag-14, lag-28 explicitly
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
# Q3.1.c Base rates per phase
# ---------------------------------------------------------------------------


def q_c_base_rates_per_phase(df: pd.DataFrame, channel: str) -> dict:
    """Per-phase n + median + dispersion (Q3.1.c)."""
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
# Q3.1.d Phase-stratified distribution + citalopram step magnitude
# ---------------------------------------------------------------------------


def q_d_phase_stratified(per_phase: dict, channel: str) -> dict:
    """Citalopram step magnitude vs natural day-to-day variation (Q3.1.d).

    Reports differences between phase medians and the dispersion of each
    phase (so the reader can compare the citalopram step to the within-
    phase day-to-day spread). The +0.43/mg locked dose-response slope
    from citalopram_dose_response_stress_mean_sleep.md v3 is the headline.
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

    # Compare to within-phase MAD (typical day-to-day variation)
    typical_within = {
        p: per_phase[p].get("mad_unscaled") for p in medians if "mad_unscaled" in per_phase[p]
    }
    out["within_phase_mad"] = typical_within

    # Citalopram dose-response anchor (locked):
    out["citalopram_dose_response_anchor"] = {
        "buildup_beta_per_mg": +0.43,
        "buildup_ci95_low": +0.16,
        "buildup_ci95_high": +0.70,
        "buildup_p": 0.001,
        "afbouw_beta_per_mg": +0.25,
        "source": "methodology/citalopram_dose_response_stress_mean_sleep.md v3 §5.6.1",
    }
    # Implied steady-state effect at 30 mg consolidation:
    out["implied_30mg_lift_buildup_beta"] = +0.43 * 30  # +12.9 stress units
    return out


# ---------------------------------------------------------------------------
# Q3.1.e Near-identity check
# ---------------------------------------------------------------------------

NEAR_IDENTITY_THRESHOLD = 0.92  # CONVENTIONS §3.3


def q_e_near_identity(df: pd.DataFrame, channel: str) -> dict:
    """Near-identity check vs three named channels + extended set
    (Q3.1.e).

    The three brief-mandated channels:
      - stress_stdev_sleep
      - all_day_stress_avg
      - stress_low_motion_min_count_S60_Mlow

    Also reports a few neighbours that are biologically plausible
    duplicates so the reader sees the wider picture without re-running.
    """
    targets = [
        "stress_stdev_sleep",
        "all_day_stress_avg",
        "stress_low_motion_min_count_S60_Mlow",
        "asleep_stress_avg_uds",
        "awake_stress_avg",
        "bb_lowest",
    ]
    rows = []
    flags = []
    for t in targets:
        if t not in df.columns:
            rows.append({"channel": t, "note": "column absent"})
            continue
        sub = df[[channel, t]].dropna()
        if len(sub) < 30:
            rows.append({"channel": t, "n": int(len(sub)), "note": "n<30 — skipped"})
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
            "Cross-channel-correlation card recorded HA07c vs HA10 (bb-derived) "
            "Spearman -0.922 on the same Stratum 4 surface; "
            "see analyses/garmin_exploration/cards/cross-channel-correlation.md"
        ),
    }


# ---------------------------------------------------------------------------
# Q3.1.f Crash-day vs normal-day on Stratum 4 + crash-drop sensitivity
# ---------------------------------------------------------------------------


def q_f_crash_vs_normal(df: pd.DataFrame, channel: str, seed: int = 20260618) -> dict:
    """Crash-vs-normal Cohen's d + crash-drop sensitivity (Q3.1.f).

    Refresh in operationalisation-support framing of
    garmin_exploration/hrv_proxy_validation/ Check 7.3. Uses
    stationary-bootstrap CI on the mean difference (E[L]=7 default).
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

    # Episode-level (per CONVENTIONS §3.6 prefer episode count for per-event stats)
    ep_mask = sub["episode_id"].notna() & sub["episode_id"].astype(str).str.startswith("crash-")
    ep_df = sub.loc[ep_mask, [channel, "episode_id"]].copy()
    per_episode_mean = ep_df.groupby("episode_id")[channel].mean()
    n_episodes = int(len(per_episode_mean))
    # Normal-day base rate: days not in any crash episode
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
        # Bootstrap CI on episode-level mean diff (event-level, no block needed; sample
        # crash episodes with replacement)
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

    # Day-level stationary-bootstrap CI on mean diff at BOTH E[L]=7 (project default)
    # AND E[L]=13 (data-driven, rounded up from Q3.1.b E[L]*=12.6 — closes the
    # half-in-half-out posture flagged by the L3.4 review on this analysis).
    # Build aligned series sorted by date so block bootstrap preserves day-level
    # autocorrelation; statistic operates on rows from the resampled frame.
    aligned = df[["date", channel, "is_crash"]].dropna(subset=[channel, "is_crash"]).copy()
    aligned = aligned.sort_values("date").reset_index(drop=True)

    def day_mean_diff(sub_df):
        c = sub_df["is_crash"].astype(bool)
        if c.sum() < 1 or (~c).sum() < 1:
            return float("nan")
        return float(sub_df.loc[c, channel].mean() - sub_df.loc[~c, channel].mean())

    boot_day_E7 = stationary_bootstrap_ci(
        aligned, day_mean_diff,
        n_bootstrap=5000, expected_block_length=7,
        confidence_level=0.95, random_state=seed,
    )
    boot_day_E13 = stationary_bootstrap_ci(
        aligned, day_mean_diff,
        n_bootstrap=5000, expected_block_length=13,
        confidence_level=0.95, random_state=seed,
    )

    # Crash-drop sensitivity on the SAME-day Spearman between channel and gevoelscore
    # (per CONVENTIONS §3.4 the binding venue is "every Layer 4+ correlation /
    # regression that touches PEM-pacing variables"; for a descriptive q, we
    # report the |delta| flag on the channel vs gevoelscore correlation).
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
            "mean_diff": mean_diff_day,
            "cohens_d": cohens_d_day,
            "stationary_bootstrap_E_L7": {
                "point_estimate": float(boot_day_E7["point_estimate"]),
                "ci_lower": float(boot_day_E7["ci_lower"]),
                "ci_upper": float(boot_day_E7["ci_upper"]),
                "note": "project default per permutation_null_block_length.md",
            },
            "stationary_bootstrap_E_L13": {
                "point_estimate": float(boot_day_E13["point_estimate"]),
                "ci_lower": float(boot_day_E13["ci_lower"]),
                "ci_upper": float(boot_day_E13["ci_upper"]),
                "note": "data-driven E[L]*=12.6 rounded up; factor-of-2 deviation flag fired at Q3.1.b",
            },
            "note": "consecutive within-episode days are autocorrelated; treat as autocorrelation-inflated supplementary read",
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
# Q3.1.g Spike-detecting primitive availability
# ---------------------------------------------------------------------------


def q_g_spike_primitive(df: pd.DataFrame) -> dict:
    """Spike-primitive availability for stress_mean_sleep (Q3.1.g).

    stress_mean_sleep is a daily-aggregate by construction. The sub-daily
    primitives that could replace it for spike-detection are:
      - max_spike_minutes (daily; uses 24h FIT samples + threshold>=75)
      - per-minute monitoring_b stress samples (raw 3-min cadence;
        latent in FIT, not in master)
    Reports counts + relation to the daily-aggregate channel.
    """
    out = {
        "channel_resolution": "daily aggregate (mean of nightly monitoring_b stress samples within sleep window)",
        "sub_daily_resolution_in_master": False,
        "spike_primitives_available_in_master": [],
        "latent_in_FIT_not_in_master": [
            "per-minute monitoring_b stress samples (raw ~3-min cadence; the source of stress_mean_sleep)",
            "monitoring_b motion + activity windows that could carve sleep into deep vs disturbed segments",
        ],
        "related_daily_spike_metrics_in_master": [],
        "note": (
            "Per CONVENTIONS §3.5, sympathetic-arousal proxies prefer spike / peak / "
            "count metrics over daily means; stress_mean_sleep is structurally a "
            "daily mean of sleep-window samples and therefore dilution-vulnerable. "
            "A spike-detecting companion lives in max_spike_minutes (24h) and in the "
            "raw monitoring_b stream (latent). The minimum-samples-per-night gate "
            "is 120 (~6h at 3-min cadence) per "
            "garmin/scripts/sleep_stress_extract/extract_sleep_stress.py."
        ),
    }
    for c in ("max_spike_minutes", "stress_high_duration_min", "stress_low_motion_min_count_S60_Mlow"):
        if c in df.columns:
            n = int(df[c].notna().sum())
            out["spike_primitives_available_in_master"].append({"column": c, "n_non_nan": n})
    # Day-level alignment: how does stress_mean_sleep covary with the in-master
    # daily spike companion max_spike_minutes?
    if "max_spike_minutes" in df.columns:
        d = df[["stress_mean_sleep", "max_spike_minutes"]].dropna()
        if len(d) > 30:
            out["pearson_r_vs_max_spike_minutes"] = float(d.corr().iloc[0, 1])
            out["spearman_rho_vs_max_spike_minutes"] = float(
                d.corr(method="spearman").iloc[0, 1]
            )
            out["n_pair_max_spike"] = int(len(d))
    return out


# ---------------------------------------------------------------------------
# Q3.1.h Outlier detection + calibration-drift check
# ---------------------------------------------------------------------------


def q_h_outliers_calibration(df: pd.DataFrame, channel: str) -> dict:
    """Outlier detection + calibration-drift check (Q3.1.h).

    Outlier rule: MAD-based |z|>5 on Stratum 4. Reports flagged dates
    + their values. Drift check: 90-day rolling median over the full
    Stratum 4 window so the reader can see whether the channel has a
    monotonic creep (vs a clean step at the citalopram boundary).
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
    # Rolling 90d median (centred trailing)
    sub["rolling_med_90d"] = v.rolling(window=90, min_periods=45).median()
    # Sample the rolling median at six time points so we don't dump 1339 rows
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
        "garmin_indicators_audit_known_issues": [
            "MIN_SAMPLES_PER_NIGHT=120 (~6h at 3-min cadence); nights below threshold drop to NaN; watch-off nights silently lost",
            "no calibration-drift events catalogued for stress_mean_sleep in garmin_indicators_audit.md",
            "underlying sensor is Forerunner 245 Elevate V3 across entire 2021-08-16 to present — no device change in window",
        ],
    }


# ---------------------------------------------------------------------------
# Q3.1.i Covariate-sensitivity readiness
# ---------------------------------------------------------------------------


def q_i_covariate_readiness(df: pd.DataFrame, channel: str) -> dict:
    """Covariate-sensitivity readiness (Q3.1.i).

    Per HA-P7 §4.5.4 worked-example pattern: pre-spec a secondary model
    that adds a candidate covariate to disambiguate the predictor's
    primary signal from a candidate alternative reading. Names 2-3
    covariates a future HA pre-reg on stress_mean_sleep as predictor
    could add.
    """
    cands = []
    # 1. dose_plasma_mg(d) — addresses the locked citalopram dose confound
    cands.append({
        "covariate": "dose_plasma_mg(d)",
        "rationale": (
            "Per citalopram_phase_stratification.md §5.B the channel is dose-modulated "
            "at +0.43/mg p=0.001 (buildup post-CPAP). A future HA on stress_mean_sleep "
            "must either dose-adjust (§5.B) or per-phase stratify (§5.A); the covariate "
            "is the framework-prescribed disambiguator between the citalopram step and "
            "the LC-physiology signal."
        ),
        "source": "methodology/citalopram_phase_stratification.md §5.B + §6",
        "expected_effect_if_primary_signal_is_citalopram": (
            "β_channel collapses toward zero in the secondary model; β_dose carries the load"
        ),
        "needed_columns_in_master": ["lc_phase or a runtime dose_plasma_mg(d) computation"],
    })
    # 2. resting_hr — addresses the autonomic-shared-axis confound
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
            "Resting HR is the alternative autonomic-load anchor; Pearson r=+0.342 on the "
            "LC era (hrv_proxy_validation Check 7.2) means ~12% of stress_mean_sleep "
            "variance is RHR-explained. A secondary model adding RHR disambiguates "
            "'is the predictor's signal HRV-proxy specific or shared autonomic-arousal'."
        ),
        "source": "hrv_proxy_validation/result-table.txt Check 7.2; cross-channel-correlation card",
        "observed_correlation_on_S4": rhr_corr,
        "expected_effect": (
            "β_channel attenuates if the signal is shared autonomic arousal; "
            "β_channel survives if HRV-proxy-specific"
        ),
    })
    # 3. stress_mean_sleep own-lagged 14d mean — addresses autocorrelation
    cands.append({
        "covariate": "stress_mean_sleep_lagged_mean_14d(d) = mean(channel[d-14:d-1])",
        "rationale": (
            "Mirrors HA-P7 §4.5.4 (lagged outcome covariate) for the autocorrelation-vs-"
            "mechanism disambiguation. With cutoff lag M reported in Q3.1.b and data-driven "
            "E[L]* nearby, a 14d lagged mean is the conservative window that captures the "
            "trailing autonomic state without overlapping today."
        ),
        "source": "HA-P7 hypothesis.md §4.5.4 worked example",
        "expected_effect": (
            "β_channel collapses if today's stress is just yesterday's stress carried forward; "
            "β_channel survives if the signal carries new-day information"
        ),
        "needed_columns_in_master": [
            "either computed in-script or added to per_day_master as stress_mean_sleep_lagged_mean_14d"
        ],
    })
    return {
        "primary_use_case": (
            "Future HA pre-reg using stress_mean_sleep as predictor of a crash-related outcome"
        ),
        "discipline_anchor": "HA-P7 hypothesis.md §4.5.4 — secondary-logistic-with-covariate pattern",
        "candidate_covariates": cands,
        "recommendation": (
            "Pre-spec all three covariates as secondary sensitivity arms; the citalopram-phase "
            "framework §5.B adjustment is the obligatory one, the others are diagnostic. "
            "Concordance across the three secondaries = high confidence in the primary; "
            "divergence = the disambiguation is doing real work."
        ),
    }


# ---------------------------------------------------------------------------
# Plot generation
# ---------------------------------------------------------------------------


def make_plots(df: pd.DataFrame, channel: str, out_dir: Path) -> list[str]:
    """Generate the required figures referenced from findings.md."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    sub = df[["date", channel, "is_crash"]].dropna(subset=[channel])

    # Figure 1: Histogram + KDE-like overlay
    fig, ax = plt.subplots(figsize=(8, 4.2))
    vals = sub[channel].astype(float)
    ax.hist(vals, bins=40, color="#5b88c4", edgecolor="white", alpha=0.85)
    med = float(vals.median())
    p25, p75 = np.percentile(vals, 25), np.percentile(vals, 75)
    ax.axvline(med, color="#222", linestyle="-", linewidth=1.5, label=f"median={med:.2f}")
    ax.axvline(p25, color="#222", linestyle="--", linewidth=1.0, label=f"p25={p25:.2f}")
    ax.axvline(p75, color="#222", linestyle="--", linewidth=1.0, label=f"p75={p75:.2f}")
    ax.set_xlabel("stress_mean_sleep (Garmin units)")
    ax.set_ylabel("days (Stratum 4)")
    ax.set_title(f"stress_mean_sleep distribution — Stratum 4, n={int(vals.notna().sum())}")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fp = out_dir / "fig1_distribution_s4.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 2: Phase-stratified violins
    phase_data = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (sub["date"] >= pd.Timestamp(start)) & (sub["date"] <= pd.Timestamp(end))
        phase_data[phase_name] = sub.loc[mask, channel].dropna().astype(float).to_numpy()
    fig, ax = plt.subplots(figsize=(9, 4.2))
    parts = ax.violinplot(
        [phase_data[p] for p in ("unmedicated", "buildup", "consolidation", "afbouw")
         if len(phase_data[p]) >= 5],
        showmedians=True, widths=0.85,
    )
    labels = [p for p in ("unmedicated", "buildup", "consolidation", "afbouw")
              if len(phase_data[p]) >= 5]
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_ylabel("stress_mean_sleep")
    ax.set_title("Phase-stratified distribution (Stratum 4)")
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
    # Phase shading
    phase_colors = {
        "unmedicated": "#ffffff",
        "buildup": "#fde0a3",
        "consolidation": "#ffd680",
        "afbouw": "#fdbf6f",
    }
    ymin, ymax = ax.get_ylim()
    for phase_name, start, end in PHASE_BOUNDARIES:
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end),
                   color=phase_colors[phase_name], alpha=0.18, label=phase_name)
    # Deduplicate legend
    h, l = ax.get_legend_handles_labels()
    seen = set()
    pairs = [(hi, li) for hi, li in zip(h, l) if not (li in seen or seen.add(li))]
    ax.legend([p[0] for p in pairs], [p[1] for p in pairs],
              loc="upper right", fontsize=8, ncol=2)
    ax.set_ylabel("stress_mean_sleep")
    ax.set_title("stress_mean_sleep — rolling 90d median + citalopram phases")
    fig.tight_layout()
    fp = out_dir / "fig3_trajectory_with_phases.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 4: Crash vs normal stripplot + per-episode mean
    df_ep = sub.copy()
    df_ep["is_crash"] = df_ep["is_crash"].astype(bool)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    normal = df_ep.loc[~df_ep["is_crash"], channel]
    crash = df_ep.loc[df_ep["is_crash"], channel]
    ax.hist(normal, bins=40, color="#9dc1e0", alpha=0.7, label=f"normal days n={len(normal)}", density=True)
    ax.hist(crash, bins=20, color="#cc4949", alpha=0.55, label=f"crash days n={len(crash)}", density=True)
    ax.axvline(normal.median(), color="#264c75", linestyle="--", label=f"normal median={normal.median():.1f}")
    ax.axvline(crash.median(), color="#7a1f1f", linestyle="--", label=f"crash median={crash.median():.1f}")
    ax.set_xlabel("stress_mean_sleep")
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
    ax.axhline(threshold, color="#cc4949", linestyle="--", linewidth=0.8, label=f"|rho|={threshold:.3f} (Politis-White 2-sigma)")
    ax.axhline(-threshold, color="#cc4949", linestyle="--", linewidth=0.8)
    ax.set_xlabel("lag (days)")
    ax.set_ylabel("autocorrelation")
    ax.set_title(f"ACF — stress_mean_sleep (Stratum 4); E[L]*={acf_res['optimal_block_length']:.1f}, M={acf_res['cutoff_lag']}")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fp = out_dir / "fig5_acf.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    return written


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main() -> None:
    # Resolve data path (default per CONVENTIONS §5 if not set)
    if not os.environ.get("GEVOELSCORE_DATA_PATH"):
        os.environ["GEVOELSCORE_DATA_PATH"] = "C:/Users/Gebruiker/Documents/gevoelscore-data"

    master = load_master(as_of_date=AS_OF_DATE)
    s4 = filter_to_stratum_4(master, as_of_date=AS_OF_DATE)
    labels = load_crash_labels(as_of_date=AS_OF_DATE)[["date", "label", "episode_id"]]
    labels = labels.rename(columns={"label": "_crash_label"})
    s4 = s4.merge(labels, on="date", how="left")
    s4["is_crash"] = (s4["_crash_label"] == "crash").astype(bool)

    if CHANNEL not in s4.columns:
        raise RuntimeError(f"{CHANNEL} not found in master — check pipeline build")

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
        "phase_axis_source": "methodology/citalopram_phase_stratification.md §3",
        "questions": {},
    }

    summary["questions"]["Q3.1.a_distribution"] = q_a_distribution(values)
    summary["questions"]["Q3.1.b_autocorrelation"] = q_b_autocorrelation(values)
    per_phase = q_c_base_rates_per_phase(s4, CHANNEL)
    summary["questions"]["Q3.1.c_base_rates_per_phase"] = per_phase
    summary["questions"]["Q3.1.d_phase_stratified_distribution"] = q_d_phase_stratified(per_phase, CHANNEL)
    summary["questions"]["Q3.1.e_near_identity"] = q_e_near_identity(s4, CHANNEL)
    summary["questions"]["Q3.1.f_crash_vs_normal"] = q_f_crash_vs_normal(s4, CHANNEL)
    summary["questions"]["Q3.1.g_spike_primitive"] = q_g_spike_primitive(s4)
    summary["questions"]["Q3.1.h_outliers_calibration"] = q_h_outliers_calibration(s4, CHANNEL)
    summary["questions"]["Q3.1.i_covariate_readiness"] = q_i_covariate_readiness(s4, CHANNEL)

    plot_files = make_plots(s4, CHANNEL, HERE / "plots")
    summary["plots"] = plot_files

    out_path = HERE / "summary.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"Wrote {out_path}")
    print(f"Plots: {plot_files}")
    print("\n--- HEADLINE ---")
    a = summary["questions"]["Q3.1.a_distribution"]
    b = summary["questions"]["Q3.1.b_autocorrelation"]
    f = summary["questions"]["Q3.1.f_crash_vs_normal"]
    print(f"Q3.1.a n={a['n']} mean={a['mean']:.2f} median={a['median']:.2f} MAD={a['mad_unscaled']:.2f} skew={a['skewness']:.2f} heavy_tail={a['heavy_tail_flag']}")
    print(f"Q3.1.b E[L]*={b['data_driven_E_L_star']:.2f} (default 7); factor-of-2 deviation flag={b['factor_of_2_deviation_flag']}; cutoff M={b['cutoff_lag_M']}")
    fl = f["day_level"]
    e7 = fl["stationary_bootstrap_E_L7"]
    e13 = fl["stationary_bootstrap_E_L13"]
    print(f"Q3.1.f day-level: n_crash={fl['n_crash_day']} n_normal={fl['n_normal_day']} d={fl['cohens_d']:.2f} mean_diff={fl['mean_diff']:.2f}")
    print(f"  E[L]=7  CI=[{e7['ci_lower']:.2f}, {e7['ci_upper']:.2f}] width={e7['ci_upper']-e7['ci_lower']:.2f}")
    print(f"  E[L]=13 CI=[{e13['ci_lower']:.2f}, {e13['ci_upper']:.2f}] width={e13['ci_upper']-e13['ci_lower']:.2f}")
    fe = f["episode_level"]
    print(f"Q3.1.f episode-level: n_ep={fe['n_crash_episodes']} d={fe['cohens_d_episode_vs_normal_day']:.2f} mean_diff={fe['mean_diff_episode_vs_normal_day']:.2f} CI={fe['bootstrap_ci95_mean_diff']}")
    cd = f["crash_drop_sensitivity_on_spearman_vs_gevoelscore"]
    if cd is not None:
        print(f"Q3.1.f crash-drop on Spearman(stress, gevoelscore): full={cd['full_frame_value']:.3f} crashed-dropped={cd['crash_dropped_value']:.3f} |delta|={cd['abs_delta']:.3f} >0.10? {cd['exceeds_threshold_0p10']}")
    e = summary["questions"]["Q3.1.e_near_identity"]
    print(f"Q3.1.e near-identity flagged: {e['flagged_pairs']}")
    h = summary["questions"]["Q3.1.h_outliers_calibration"]
    print(f"Q3.1.h outliers (|z|>5): {h['n_flagged']} flagged")


if __name__ == "__main__":
    main()
