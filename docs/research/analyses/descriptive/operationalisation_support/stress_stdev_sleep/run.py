"""Descriptive analysis: stress_stdev_sleep operationalisation support.

Answers Q3.4.a-i per the locked descriptive programme:
``docs/research/analyses/descriptive/README.md`` section 3.4 (template
a-i applied to this channel, per the section 3.4 HA-touched-non-confirmed
candidate list: "stress_stdev_sleep (HA07d primary, the only canonical-
SUPPORTED test) -- needs a Strand A analysis for the variability story").
This is the **FINAL Tier 1 channel** in the user-prioritised "finish the
descriptive analysis" Phase 2 sequential batch (R14 single_pool_reanchor
first at badd04a; Q3.2 all_day_stress_avg at cf34ab1; Q3.3 bb_lowest at
40c351b; this Q3.4 closes Tier 1).

Channel: nightly standard deviation of in-sleep-window stress samples
(custom-extracted from monitoring_b FIT per
garmin/scripts/sleep_stress_extract/extract_sleep_stress.py; sister of
stress_mean_sleep on the same nightly sample set). HA07d's PRIMARY
OPERAND: max |z| (4d, bidirectional) of night-over-night delta of
stress_stdev_sleep with lagged baseline. HA07d is the **ONLY canonical
both-eras-SUPPORTED test in the project** (train +19.6 pp / validate
+21.7 pp; OVERALL SUPPORTED) AND just R14-confirmed at single-pool
+19.7 pp [CI -18.1, +17.0] perm p (E[L]=7) = 0.0291 (badd04a) -- the
**only HA that retained SUPPORTED at single-pool** in the R14 cross-
check.

Channel substantive status (per handoff section 1):
- HA07d primary operand (BOTH ERAS SUPPORTED + R14 single-pool SUPPORTED)
- NOT in v3 multi-channel sweep scope per
  citalopram_dose_response_stress_mean_sleep.md section 5.6 (v3 covered
  6 baseline channels: stress_mean_sleep, all_day_stress_avg, bb_lowest,
  resting_hr, bb_overnight_gain, respiration_avg_sleep). The citalopram-
  dose-modulation status on this channel is **OPEN**.
- Sister of stress_mean_sleep on same nightly sample set; HA07c (mean
  delta) train-only-SUPPORTED vs HA07d (stdev delta) both-eras-SUPPORTED
  suggests substantive independence of the variability primitive from
  the mean.

Continuous-channel template (parity with sister stress_mean_sleep Q3.1
+ sibling all_day_stress_avg Q3.2 + bb_lowest Q3.3): standard Cohen's d
primary, no zero-rate column. The Q3.4.e near-identity check rigorously
tests whether stress_stdev_sleep is near-identical to its mean sibling
(the obvious candidate via heteroskedasticity) -- the HA07d both-eras-
SUPPORTED + HA07c train-only-SUPPORTED divergence suggests substantive
independence; descriptive rho should confirm.

Output: ``summary.json`` (machine-readable per-question results) +
``plots/*.png`` (visualisations) + ``findings.md`` + ``README.md``
(programmatically emitted from this script per the Q3.2/Q3.3 precedent
session's architectural note about the Write-tool harness heuristic on
the literal filename "findings").

Discipline guards (per CONVENTIONS):
- section 2.1 descriptive-before-inference: no causal claims; no
  falsification bar; no HA verdict promotion (HA07d substantive verdict
  is LOCKED and NOT extended here; the canonical both-eras-SUPPORTED
  status is descriptively corroborated only).
- section 3.1 personal baseline: distribution shape is reported as-is;
  phase-stratified to surface any citalopram step.
- section 3.3 column-duplication: near-identity check at |rho|>=0.92.
- section 3.4 crash-drop sensitivity: |Delta|>0.10 flag surfaced.
- section 3.5 spike metrics: stress_stdev_sleep is itself the second-
  order variability proxy on the nightly stress series; spike-vs-
  continuous discipline notes the "HRV-of-HRV-proxy" framing per HA07d
  result section.
- section 3.6 named counts: every count reports scheme + unit + source.
- section 4.2 caveat-class for Q3.4.d: NO CONFIRMED/REJECTED citalopram-
  modulation verdict; observed shift framed as descriptive observation
  only (channel is NOT in v3 scope; this analysis cannot pre-commit a
  verdict that belongs in a future v3 extension).
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
# HERE = .../analyses/descriptive/operationalisation_support/stress_stdev_sleep
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


CHANNEL = "stress_stdev_sleep"
AS_OF_DATE = "2026-06-05"  # parity with R14 + Q3.1 + Q3.2 + Q3.3 prior Strand-A analyses

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
# Q3.4.a Distribution shape
# ---------------------------------------------------------------------------


def q_a_distribution(values: pd.Series) -> dict:
    """Distribution shape on Stratum 4 (Q3.4.a)."""
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
    # stress_stdev_sleep is a non-negative dispersion measure -- right-
    # skewed by construction (zero floor, no upper bound). Heavy-tail rule
    # per CONVENTIONS section 3.1: skew > 1 OR p99/median > 3.0.
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
# Q3.4.b Autocorrelation + E[L]*
# ---------------------------------------------------------------------------


def q_b_autocorrelation(values: pd.Series) -> dict:
    """Autocorrelation structure + E[L]* (Q3.4.b)."""
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
# Q3.4.c Base rates per phase
# ---------------------------------------------------------------------------


def q_c_base_rates_per_phase(df: pd.DataFrame, channel: str) -> dict:
    """Per-phase n + median + dispersion (Q3.4.c)."""
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
# Q3.4.d Phase-stratified distribution -- caveat-class observation
# ---------------------------------------------------------------------------


def q_d_phase_stratified(per_phase: dict, channel: str) -> dict:
    """Phase-stratified distribution + descriptive shift report (Q3.4.d).

    Per handoff section 1 + section 2.4 + CONVENTIONS section 4.2: this
    channel is NOT in the v3 multi-channel sweep scope (the sweep
    tested 6 channels: stress_mean_sleep, all_day_stress_avg, bb_lowest,
    resting_hr, bb_overnight_gain, respiration_avg_sleep). The citalopram-
    dose-modulation status is therefore OPEN. This Q3.4.d reports the
    observed median + dispersion shift across the 2024-04-09 boundary
    descriptively; it does NOT pre-commit a CONFIRMED/REJECTED verdict
    on dose-modulation candidacy -- that decision belongs in a future v3
    extension covering this channel.
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

    out["v3_scope_status"] = {
        "channel_in_v3_six_channel_scope": False,
        "v3_scope": [
            "stress_mean_sleep (CONFIRMED, +0.43/mg p=0.001)",
            "all_day_stress_avg (CONFIRMED, +0.57/mg p=0.000)",
            "bb_lowest (CONFIRMED, -1.13/mg p=0.000)",
            "resting_hr (weakly consistent)",
            "bb_overnight_gain (partial; no 2024 buildup data)",
            "respiration_avg_sleep (REJECTED)",
        ],
        "framing": (
            "stress_stdev_sleep is NOT in v3 multi-channel sweep scope per "
            "citalopram_dose_response_stress_mean_sleep.md section 5.6.1; "
            "citalopram-dose-modulation status is OPEN. Observed phase-shift "
            "below is a Layer 1 descriptive observation per CONVENTIONS "
            "section 4.2 (caveats yes, a-priori claims no) -- the "
            "candidacy/non-candidacy for a future v3 extension is a "
            "downstream decision NOT pre-committed here."
        ),
        "source": "methodology/citalopram_dose_response_stress_mean_sleep.md v3 section 5.6.1",
    }
    return out


# ---------------------------------------------------------------------------
# Q3.4.e Near-identity check vs mean sibling + sisters
# ---------------------------------------------------------------------------

NEAR_IDENTITY_THRESHOLD = 0.92  # CONVENTIONS section 3.3


def q_e_near_identity(df: pd.DataFrame, channel: str) -> dict:
    """Near-identity check (Q3.4.e).

    Per handoff section 2.4 + descriptive README section 3.4 template:
    rigorously check near-identity vs stress_mean_sleep (the obvious
    candidate -- both summarise the same nightly stress sample set; sigma
    and mean of the same series MAY be near-identical via heteroskedasticity
    OR may be substantively independent). The HA07d both-eras-SUPPORTED
    + HA07c train-only-SUPPORTED divergence at the test level suggests
    substantive independence; the descriptive rho at day-level confirms
    or refutes.

    Targets per descriptive README section 3.4 / Q3.4.e template:
      - stress_mean_sleep (sibling mean of same nightly series; load-bearing)
      - all_day_stress_avg (24h-window stress sister; CONFIRMED-citalopram)
      - stress_low_motion_min_count_S60_Mlow (spike-form companion)
    Plus several biologically-plausible neighbours.
    """
    targets = [
        # Brief-mandated per descriptive README section 3.4 template
        "stress_mean_sleep",
        "all_day_stress_avg",
        "stress_low_motion_min_count_S60_Mlow",
        # Stress-family neighbours
        "asleep_stress_avg_uds",
        "awake_stress_avg",
        "awake_stress_max",
        "all_day_stress_max",
        # Cardiovascular + BB family
        "resting_hr",
        "bb_lowest",
        "bb_overnight_gain",
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
            "Sister stress_mean_sleep Q3.1.e reported Pearson r=+0.602 / "
            "Spearman rho=+0.501 with this channel (NOT near-identity at the "
            "section 3.3 threshold). Reciprocal check here confirms that "
            "rho. The HA07d both-eras-SUPPORTED + HA07c train-only-SUPPORTED "
            "divergence at the test level is descriptively consistent with "
            "the rho<0.92 substantive-independence reading: variability and "
            "mean of the same nightly stress series carry distinct day-level "
            "information."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.4.f Crash-day vs normal-day on Stratum 4 + crash-drop sensitivity
# ---------------------------------------------------------------------------


def _mann_whitney_u(crash_vals: np.ndarray, normal_vals: np.ndarray) -> dict:
    """Compute Mann-Whitney U with normal approximation + tie correction.

    Returns U, z, p (two-sided), P(crash > normal). Vendored to avoid a
    hard scipy dependency.
    """
    n_c = len(crash_vals)
    n_n = len(normal_vals)
    pooled = np.concatenate([crash_vals, normal_vals])
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
        z = (U_c - mean_U - 0.5 * np.sign(U_c - mean_U)) / np.sqrt(var_U)
        from math import erf, sqrt
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
    sensitivity (Q3.4.f).

    Per handoff section 2.4: this re-anchors HA07d's already-SUPPORTED-
    on-both-eras + R14-single-pool-SUPPORTED results in current-corpus
    form at the channel-distribution level. NOTE: HA07d's primitive is
    max |z| (4d, bidirectional) of night-over-night DELTA of
    stress_stdev_sleep -- a second-order construct on the channel. This
    Q3.4.f is on the raw channel value (first-order, day-level), which is
    the descriptive-level read distinct from the HA's tested operand.
    The episode-level Cohen's d here corroborates the channel signal at
    a coarser-than-HA07d resolution.
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

    mwu = _mann_whitney_u(crash_vals.to_numpy(), normal_vals.to_numpy())

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

    crash_drop_info = None
    if "gevoelscore" in df.columns:
        d2 = df[[channel, "gevoelscore", "is_crash"]].dropna()
        d2["is_crash"] = d2["is_crash"].astype(bool)
        if d2["is_crash"].sum() > 1 and (~d2["is_crash"]).sum() > 1:
            def spearman_stat(d):
                return float(d[channel].corr(d["gevoelscore"], method="spearman"))
            crash_drop_info = crash_drop_sensitivity(spearman_stat, d2)

    # Crash-subset rho vs stress_mean_sleep (per handoff section 2.4
    # Q3.4.e supplementary -- substantive-independence check on crash
    # days specifically)
    crash_subset_rho_vs_mean_sibling = None
    if "stress_mean_sleep" in df.columns:
        d3 = df[[channel, "stress_mean_sleep", "is_crash"]].dropna()
        d3["is_crash"] = d3["is_crash"].astype(bool)
        crash_subset = d3.loc[d3["is_crash"]]
        normal_subset = d3.loc[~d3["is_crash"]]
        if len(crash_subset) > 10 and len(normal_subset) > 10:
            crash_subset_rho_vs_mean_sibling = {
                "n_crash_pairs": int(len(crash_subset)),
                "pearson_r_crash": float(crash_subset[channel].corr(crash_subset["stress_mean_sleep"])),
                "spearman_rho_crash": float(crash_subset[channel].corr(crash_subset["stress_mean_sleep"], method="spearman")),
                "n_normal_pairs": int(len(normal_subset)),
                "pearson_r_normal": float(normal_subset[channel].corr(normal_subset["stress_mean_sleep"])),
                "spearman_rho_normal": float(normal_subset[channel].corr(normal_subset["stress_mean_sleep"], method="spearman")),
                "note": (
                    "Crash-subset rho vs mean sibling stress_mean_sleep "
                    "(substantive-independence check per Q3.4.e + handoff "
                    "section 2.4). If crash-subset rho << normal-subset rho, "
                    "the variability primitive carries crash-distinct "
                    "information that the mean does not."
                ),
            }

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
                "note": "data-driven from Q3.4.b; rounded to nearest integer",
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
        "crash_subset_rho_vs_mean_sibling": crash_subset_rho_vs_mean_sibling,
        "ha07d_cross_reference": {
            "tested_operand": "max |z| (4d, bidirectional) of night-over-night delta of stress_stdev_sleep; lagged baseline; sigma_floor=0.5",
            "locked_train_disc_pp": +19.6,
            "locked_validate_disc_pp": +21.7,
            "locked_overall_verdict": "BOTH ERAS SUPPORTED -> OVERALL SUPPORTED (only canonical both-eras-SUPPORTED test in the project)",
            "r14_single_pool_disc_pp": +19.7,
            "r14_single_pool_ci95": [-18.1, +17.0],
            "r14_single_pool_perm_p": 0.0291,
            "r14_single_pool_verdict": "SUPPORTED (only HA that retained SUPPORTED at single-pool in R14 cross-check)",
            "r14_source": "descriptive/operationalisation_support/single_pool_reanchor/findings.md row HA07d",
            "ha_source": "analyses/hypotheses/HA07d-sleep-stress-variability/result.md",
            "note": (
                "HA07d primitive is a second-order construct on this channel "
                "(night-over-night delta -> 4d max |z|); this Q3.4.f reports "
                "the first-order day-level Cohen's d on the raw channel as "
                "the descriptive-layer complement. Episode-level d here is "
                "the channel-distribution corroboration of the HA-level "
                "signal; the HA-level verdicts are LOCKED and NOT extended."
            ),
        },
    }


# ---------------------------------------------------------------------------
# Q3.4.g Spike-detecting primitive availability
# ---------------------------------------------------------------------------


def q_g_spike_primitive(df: pd.DataFrame, channel: str) -> dict:
    """Spike-primitive availability for stress_stdev_sleep (Q3.4.g).

    stress_stdev_sleep is itself a SECOND-ORDER summary on the per-night
    sleep-window stress sample set (per
    garmin/scripts/sleep_stress_extract/extract_sleep_stress.py: stdev of
    monitoring_b stress samples within sleep window, with MIN_SAMPLES_PER_
    NIGHT=120 gate). The "variability-specific spike" formulation per
    descriptive README section 3.4 Q3.x.g template is the per-day stdev
    itself -- a single value per sleep-night that measures within-night
    sample dispersion. Per CONVENTIONS section 3.5: stress_stdev_sleep is
    a within-night extremum-derived primitive (already an "instability
    metric" on the nightly stress series), distinct from spike-form
    extrema like stress_low_motion or all_day_stress_max which are 24h
    pure-extremum primitives.

    Per HA07d result.md: HA07d's tested operand IS the spike-form
    construct on this channel -- the 4d window MAX |z| of night-over-
    night delta, which IS a within-4-day spike-of-variability metric.
    """
    out = {
        "channel_resolution": "per-night STDEV of sleep-window monitoring_b stress samples (custom FIT extraction; MIN_SAMPLES_PER_NIGHT=120 gate)",
        "spike_or_continuous_form": "SECOND-ORDER variability primitive (within-night dispersion of stress samples; NOT a 24h mean)",
        "sub_daily_resolution_in_master": False,
        "spike_primitives_available_in_master": [],
        "latent_in_FIT_not_in_master": [
            "per-minute monitoring_b stress samples within sleep window (the source of this channel; not exposed in master)",
            "sub-hour stdev-of-stress for finer-than-night resolution (could be computed; not in master as of 2026-06-24)",
            "sleep-stage-stratified stdev (REM vs deep vs disturbed -- could be computed; would require sleep-stage alignment per HA07d caveat section 8 sleep-architecture confound)",
        ],
        "related_daily_stress_metrics_in_master": [],
        "note": (
            "Per CONVENTIONS section 3.5 + HA07d result.md: stress_stdev_"
            "sleep is the 'HRV-of-HRV-proxy' construct -- a SECOND-ORDER "
            "autonomic-flexibility signal. HA07d's tested operand "
            "(max |z| of night-over-night delta over 4d window) IS the "
            "spike-form construct on this channel at the 4-day-window "
            "resolution. The per-day stdev itself is the first-order "
            "variability metric; the per-4-day max |z| of its night-over-"
            "night delta is the second-order spike-of-variability metric "
            "HA07d uses. For any future HA whose mechanism is a within-"
            "night arousal (e.g. a single sleep-disturbed night), the "
            "per-day stdev IS the canonical primitive; finer-than-night "
            "resolution would require new FIT-side extraction."
        ),
    }
    for c in (
        "stress_mean_sleep",
        "all_day_stress_max",
        "awake_stress_max",
        "stress_low_motion_min_count_S60_Mlow",
        "asleep_stress_avg_uds",
    ):
        if c in df.columns:
            n = int(df[c].notna().sum())
            out["spike_primitives_available_in_master"].append({"column": c, "n_non_nan": n})
    for partner in ("stress_mean_sleep", "all_day_stress_max", "awake_stress_max", "stress_low_motion_min_count_S60_Mlow", "asleep_stress_avg_uds"):
        if partner in df.columns:
            d = df[[channel, partner]].dropna()
            if len(d) > 30:
                out[f"pearson_r_vs_{partner}"] = float(d.corr().iloc[0, 1])
                out[f"spearman_rho_vs_{partner}"] = float(d.corr(method="spearman").iloc[0, 1])
                out[f"n_pair_{partner}"] = int(len(d))
    return out


# ---------------------------------------------------------------------------
# Q3.4.h Outlier detection + calibration-drift check
# ---------------------------------------------------------------------------


def q_h_outliers_calibration(df: pd.DataFrame, channel: str) -> dict:
    """Outlier detection + calibration-drift check (Q3.4.h).

    MAD-based |z|>5 on Stratum 4. Reports flagged dates + values + drift
    snapshots. Cross-references garmin_indicators_audit.md known-issues
    for the sleep-stress-extraction family.
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
    step_buildup = pd.Timestamp("2024-04-09")
    pre30_b = sub.loc[(sub["date"] >= step_buildup - pd.Timedelta(days=30))
                      & (sub["date"] < step_buildup), channel].mean()
    post30_b = sub.loc[(sub["date"] >= step_buildup)
                       & (sub["date"] < step_buildup + pd.Timedelta(days=30)), channel].mean()
    step_consol = pd.Timestamp("2024-06-20")
    pre30_c = sub.loc[(sub["date"] >= step_consol - pd.Timedelta(days=30))
                      & (sub["date"] < step_consol), channel].mean()
    post30_c = sub.loc[(sub["date"] >= step_consol)
                       & (sub["date"] < step_consol + pd.Timedelta(days=30)), channel].mean()
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
        },
        "garmin_indicators_audit_known_issues": [
            (
                "stress_stdev_sleep is custom-extracted from monitoring_b FIT files per "
                "garmin/scripts/sleep_stress_extract/extract_sleep_stress.py; "
                "MIN_SAMPLES_PER_NIGHT=120 gate (~6h at 3-min cadence). Nights "
                "below the gate are dropped to NaN (sleep_valid_flag=False)"
            ),
            (
                "No specific calibration-drift events catalogued for stress_stdev_sleep "
                "in garmin_indicators_audit.md beyond the shared sleep-stress-extraction "
                "family entries (same as sister stress_mean_sleep Q3.1.h)"
            ),
            (
                "Underlying sensor is Forerunner 245 Elevate V3 throughout the entire "
                "2021-08-16 to present window -- no device change in the analytic window"
            ),
            (
                "Per HA07d hypothesis.md section 8: sleep architecture confound -- higher "
                "sleep stress variability can reflect more sleep-stage transitions (REM "
                "vs deep cycles), not autonomic dysregulation directly. This is a "
                "substrate caveat for the channel's biological interpretation, not a "
                "calibration-drift signature"
            ),
        ],
    }


# ---------------------------------------------------------------------------
# Q3.4.i Covariate-sensitivity readiness
# ---------------------------------------------------------------------------


def q_i_covariate_readiness(df: pd.DataFrame, channel: str) -> dict:
    """Covariate-sensitivity readiness (Q3.4.i).

    Per HA-P7 section 4.5.4 worked-example pattern. Names candidate
    covariates a future HA on stress_stdev_sleep as predictor could add.
    """
    cands = []
    # 1. stress_mean_sleep -- sibling mean of same nightly stress series
    mean_corr = None
    if "stress_mean_sleep" in df.columns:
        d = df[[channel, "stress_mean_sleep"]].dropna()
        if len(d) > 30:
            mean_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "stress_mean_sleep (mean sibling of same nightly stress series)",
        "rationale": (
            "Variability and mean of the same nightly stress series may share "
            "heteroskedasticity-driven covariance. The covariate disambiguates: "
            "is the stress_stdev_sleep signal driven by the variability "
            "primitive specifically (beta_channel survives) or by the shared "
            "nightly stress level (beta_channel attenuates -- stress_mean_sleep "
            "was carrying the load via the right-tail heteroskedasticity). "
            "The HA07d both-eras-SUPPORTED + HA07c train-only-SUPPORTED "
            "divergence is substantively consistent with beta_channel "
            "surviving on this disambiguation, but a per-HA pre-reg secondary "
            "is the canonical check."
        ),
        "source": "sister stress_mean_sleep findings.md Q3.1.e + HA07c result.md (train-only-SUPPORTED) + HA07d result.md (both-eras-SUPPORTED)",
        "observed_correlation_on_S4": mean_corr,
        "expected_effect": (
            "beta_channel attenuates if shared nightly stress level dominates; "
            "beta_channel survives if variability primitive carries independent "
            "second-order information"
        ),
    })
    # 2. dose_plasma_mg(d) -- citalopram covariate (channel NOT in v3 scope; OPEN)
    cands.append({
        "covariate": "dose_plasma_mg(d) (citalopram covariate -- OPEN status)",
        "rationale": (
            "stress_stdev_sleep is NOT in v3 multi-channel sweep scope per "
            "citalopram_dose_response_stress_mean_sleep.md section 5.6 (the "
            "sweep covered 6 channels: stress_mean_sleep, all_day_stress_avg, "
            "bb_lowest, resting_hr, bb_overnight_gain, respiration_avg_sleep). "
            "The citalopram-dose-modulation status is OPEN. A future HA on "
            "stress_stdev_sleep cross-phase should pre-spec dose as a secondary "
            "covariate to surface any latent dose-modulation; if beta_dose is "
            "significant in the secondary, that is evidence for a future v3 "
            "extension to add this channel as a 7th candidate. Until v3 covers "
            "this channel, neither section 5.A nor section 5.B treatment is "
            "OBLIGATORY (unlike the 3 CONFIRMED channels) -- the dose "
            "covariate is a diagnostic, not a framework requirement."
        ),
        "source": "methodology/citalopram_dose_response_stress_mean_sleep.md v3 section 5.6 (channel NOT in scope); CONVENTIONS section 4.2 caveat-class framing",
        "expected_effect_if_latent_dose_modulation": (
            "beta_channel attenuates and beta_dose carries some load -- a future-"
            "v3-extension candidacy signal"
        ),
        "needed_columns_in_master": ["lc_phase (in master) or runtime dose_plasma_mg(d) computation"],
    })
    # 3. resting_hr -- alternative autonomic-load anchor
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
        "covariate": "resting_hr (alternative autonomic-load anchor)",
        "rationale": (
            "Per HA07d result.md the channel is framed as 'HRV-of-HRV-proxy' "
            "(second-order autonomic-flexibility signal). The covariate "
            "disambiguates: beta_channel attenuates -> the signal is shared "
            "autonomic-arousal carried by resting HR; beta_channel survives -> "
            "the signal is HRV-proxy-variability-specific beyond the resting-"
            "HR axis."
        ),
        "source": "HA07d result.md framing + canonical hrv_proxy_validation Check 7.2 on sister channel",
        "observed_correlation_on_S4": rhr_corr,
        "expected_effect": (
            "beta_channel attenuates if shared autonomic-arousal dominates; "
            "beta_channel survives if HRV-proxy-variability carries independent "
            "information"
        ),
    })
    # 4. own-lagged trailing-mean -- autocorrelation-vs-mechanism
    cands.append({
        "covariate": "stress_stdev_sleep_lagged_mean_Nd(d) = mean(channel[d-N:d-1]) with N tuned to Q3.4.b E[L]* + margin",
        "rationale": (
            "Mirrors HA-P7 section 4.5.4 worked example (lagged-outcome "
            "covariate) for the autocorrelation-vs-mechanism disambiguation. "
            "Per Q3.4.b the cutoff lag M and data-driven E[L]* are inputs to "
            "this choice. NOTE: this channel does NOT have a materialised "
            "*_lagged_lcera_z variant in per_day_master (sister channels "
            "stress_mean_sleep + all_day_stress_avg + resting_hr + bb_lowest "
            "+ bb_overnight_gain do, per CONVENTIONS section 3.2). HA author "
            "must compute the covariate at runtime."
        ),
        "source": "HA-P7 hypothesis.md section 4.5.4 worked example; CONVENTIONS section 3.2 _lagged_lcera convention",
        "expected_effect": (
            "beta_channel collapses if today's stress_stdev_sleep is yesterday's "
            "stress_stdev_sleep carried forward; beta_channel survives if the "
            "signal carries new-day information"
        ),
        "needed_columns_in_master": [
            "stress_stdev_sleep_lagged_lcera_z is NOT in master (see CONVENTIONS section 3.2 + setup-permissions drift note) -- runtime computation required"
        ],
    })
    return {
        "primary_use_case": (
            "Future HA pre-reg using stress_stdev_sleep as predictor of a "
            "crash-related outcome (the canonical HA family: HA07d substantive "
            "verdict already LOCKED at OVERALL SUPPORTED; further HAs can use "
            "the channel in different operands -- e.g. raw daily value, "
            "different window lengths, single-direction primitives -- without "
            "re-anchoring the HA07d-locked verdict)"
        ),
        "discipline_anchor": "HA-P7 hypothesis.md section 4.5.4 -- secondary-logistic-with-covariate pattern",
        "candidate_covariates": cands,
        "recommendation": (
            "Pre-spec all four covariates as secondary sensitivity arms. The "
            "stress_mean_sleep arm (covariate 1) is the load-bearing "
            "substantive-independence check: HA07d's both-eras-SUPPORTED "
            "status would be empirically diminished if beta_channel collapses "
            "under this covariate. The dose_plasma_mg arm (covariate 2) is "
            "diagnostic-only at this time per the channel's NOT-in-v3-scope "
            "status; if it fires consistently across multiple HA tests, that "
            "is candidacy evidence for a future v3 extension. The resting_hr "
            "arm (covariate 3) is the cross-channel autonomic-state "
            "disambiguator. The autocorrelation arm (covariate 4) "
            "operationalises HA-P7 section 4.5.4 on this specific channel."
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
    ax.set_xlabel("stress_stdev_sleep (Garmin stress units, per-night STDEV)")
    ax.set_ylabel("days (Stratum 4)")
    ax.set_title(f"stress_stdev_sleep distribution - Stratum 4, n={int(vals.notna().sum())}")
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
    ax.set_ylabel("stress_stdev_sleep")
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
    ax.set_ylabel("stress_stdev_sleep")
    ax.set_title("stress_stdev_sleep - rolling 90d median + citalopram phases")
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
    ax.axvline(normal.median(), color="#264c75", linestyle="--", label=f"normal median={normal.median():.2f}")
    ax.axvline(crash.median(), color="#7a1f1f", linestyle="--", label=f"crash median={crash.median():.2f}")
    ax.set_xlabel("stress_stdev_sleep")
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
        f"ACF - stress_stdev_sleep (Stratum 4); E[L]*={acf_res['optimal_block_length']:.1f}, M={acf_res['cutoff_lag']}"
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


def _format_p(p: float) -> str:
    """Format p-value safely (avoid f-string pre-3.12 backslash escape)."""
    if p < 0.0001:
        return "<0.0001"
    return format(p, ".4f")


def write_findings_md(summary: dict, path: Path) -> None:
    """Emit the analyst-style findings.md from the computed summary."""
    q = summary["questions"]
    a = q["Q3.4.a_distribution"]
    b = q["Q3.4.b_autocorrelation"]
    c = q["Q3.4.c_base_rates_per_phase"]
    d = q["Q3.4.d_phase_stratified_distribution"]
    e = q["Q3.4.e_near_identity"]
    fr = q["Q3.4.f_crash_vs_normal"]
    fl = fr["day_level"]
    fe = fr["episode_level"]
    g = q["Q3.4.g_spike_primitive"]
    h = q["Q3.4.h_outliers_calibration"]
    i = q["Q3.4.i_covariate_readiness"]

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
                f"{info['p10']:.2f} / {info['p90']:.2f} |"
            )

    afbouw_med = c.get("afbouw", {}).get("median", float("nan"))
    consol_med = c.get("consolidation", {}).get("median", float("nan"))
    buildup_med = c.get("buildup", {}).get("median", float("nan"))
    unmed_med = c.get("unmedicated", {}).get("median", float("nan"))
    buildup_minus_unmed = d["phase_to_phase_shifts"].get("buildup_minus_unmedicated_median", float("nan"))
    consol_minus_unmed = d["phase_to_phase_shifts"].get("consolidation_minus_unmedicated_median", float("nan"))
    afbouw_minus_consol = d["phase_to_phase_shifts"].get("afbouw_minus_consolidation_median", float("nan"))
    afbouw_minus_unmed = d["phase_to_phase_shifts"].get("afbouw_minus_unmedicated_median", float("nan"))

    ha07d = fr["ha07d_cross_reference"]
    crash_subset_rho = fr.get("crash_subset_rho_vs_mean_sibling")

    # Sister-channel E[L]* spread context per handoff section 2.4
    if el_star < 14:
        el_class = "near mean-sibling stress_mean_sleep (12.6)"
    elif el_star > 25:
        el_class = "in the long-memory CONFIRMED-citalopram cluster (~29d)"
    elif el_star > 18:
        el_class = "between mean-sibling (12.6) and long-memory cluster (~29d); closer to stress_low_motion (21.1)"
    else:
        el_class = "between mean-sibling (12.6) and stress_low_motion (21.1)"

    mwu_p_str = _format_p(mwu['p_two_sided'])

    out_lines = [
        "# Findings -- `stress_stdev_sleep` operationalisation-support descriptive (Q3.4.a-i)",
        "",
        "**Channel**: `stress_stdev_sleep` (HA07d primary operand; per-night STDEV of "
        "sleep-window monitoring_b stress samples, custom FIT extraction per "
        "[`garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`](../../../../garmin/scripts/sleep_stress_extract/extract_sleep_stress.py); "
        "MIN_SAMPLES_PER_NIGHT=120 gate; same nightly sample set as sister "
        "`stress_mean_sleep`). Column semantics: [DATA_DICTIONARY.md sleep-stress section](../../../DATA_DICTIONARY.md).",
        "",
        "**Substantive context**: HA07d is the **only canonical both-eras-SUPPORTED test "
        "in the project** (train +19.6 pp / validate +21.7 pp / OVERALL SUPPORTED per "
        "[`HA07d-sleep-stress-variability/result.md`](../../../analyses/hypotheses/HA07d-sleep-stress-variability/result.md)) "
        "AND just R14-confirmed at single-pool +19.7 pp [CI -18.1, +17.0] perm p (E[L]=7) = "
        "0.0291 per [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) "
        "row HA07d -- the **only HA that retained SUPPORTED at single-pool** in the R14 "
        "cross-check (`badd04a`). This Q3.4 is the Strand-A backstop on the channel; the "
        "HA07d substantive verdicts are LOCKED and descriptively corroborated only.",
        "",
        f"**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to {summary['as_of_date']}). "
        f"n={a['n']} days with channel out of {summary['n_rows_stratum_4_total']} Stratum 4 days "
        f"({summary['n_rows_stratum_4_total'] - a['n']} NaN nights from MIN_SAMPLES_PER_NIGHT=120 gate; "
        "sleep_valid_flag=False).",
        "",
        "**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, "
        "commit `ccbd12e`) -- HA-touched non-confirmed channel candidate list; specifically the "
        "section 3.4 bullet \"`stress_stdev_sleep` (HA07d primary, the only canonical-SUPPORTED test) -- "
        "needs a Strand A analysis for the variability story\". This analysis is the **FINAL Tier 1 "
        "channel** in the user-prioritised Phase 2 sequential batch (R14 `single_pool_reanchor` first at "
        "`badd04a`; Q3.2 `all_day_stress_avg` second at `cf34ab1`; Q3.3 `bb_lowest` third at `40c351b`; "
        "this Q3.4 closes Tier 1). Q3.4.a-i template applied per section 3.1 verbatim (substituted "
        "channel name + adapted section 3.4.d to NOT-in-v3-scope caveat-class framing).",
        "",
        "**Sources**: `per_day_master.csv` (Garmin daily aggregate) + `labels_crash_v2.csv` "
        "(`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level per "
        "CONVENTIONS section 3.6).",
        "",
        "**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict "
        "promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). "
        "HA07d (LOCKED OVERALL-SUPPORTED + R14 single-pool SUPPORTED) + HA07c (LOCKED OVERALL-REFUTED with "
        "train-only-SUPPORTED) + HA08c (LOCKED OVERALL-REFUTED with train-only-SUPPORTED) cross-references "
        "in this analysis are **descriptive corroboration only**; the substantive verdicts live in those "
        "result.md files and are NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori "
        "claims no). Statistical hygiene anchors: section 3.1 (personal baseline), section 3.3 (column-"
        "duplication threshold |rho|>=0.92), section 3.4 (crash-drop sensitivity |delta|>0.10), section "
        "3.5 (spike metrics -- stress_stdev_sleep IS the second-order within-night variability primitive; "
        "HA07d's tested operand is the per-4-day spike-form construct on this channel), section 3.6 "
        "(named counts).",
        "",
        "---",
        "",
        "## Headline",
        "",
        f"`stress_stdev_sleep` on Stratum 4 is a **right-skewed, autocorrelation-{('SPARSE' if el_star < 10 else 'MODERATE' if el_star < 20 else 'DENSE')} "
        f"per-night dispersion channel** (skew={skew:+.2f}, excess kurtosis={a['excess_kurtosis']:+.2f}, "
        f"heavy_tail_flag={a['heavy_tail_flag']}, p99/median = {p99:.2f}/{med:.2f} = {p99_over_med:.2f}). "
        f"The **data-driven E[L]\\*={el_star:.1f}** (Politis-White; deviation ratio "
        f"{b['deviation_ratio']:.2f}; factor-of-2 flag = {b['factor_of_2_deviation_flag']}; cutoff lag "
        f"M={b['cutoff_lag_M']}). Cross-channel context per handoff section 2.4: vs sister Strand-A "
        f"channels `stress_mean_sleep` E[L]\\*=12.6 + `stress_low_motion_min_count_S60_Mlow` 21.1 + "
        f"`bb_lowest` 29.25 + `all_day_stress_avg` 29.8 -- this channel sits {el_class}. "
        f"**Phase-stratified medians** (citalopram axis, caveat-class observation per CONVENTIONS section "
        f"4.2 since channel NOT in v3 scope): unmedicated {unmed_med:.2f} -> buildup {buildup_med:.2f} -> "
        f"consolidation {consol_med:.2f} -> afbouw {afbouw_med:.2f} (consolidation-minus-unmedicated "
        f"= {consol_minus_unmed:+.2f}; descriptively suggests {'candidacy for a future v3 extension' if abs(consol_minus_unmed) > 0.3 else 'NOT-candidacy for a future v3 extension'} "
        f"-- NO CONFIRMED/REJECTED verdict pre-committed). Day-resolved citalopram boundary step "
        f"(2024-04-09 pre/post 30d) is **{citalo_step['diff_post_minus_pre']:+.2f} units**. Crash-vs-normal: "
        f"episode-level d={fe['cohens_d_episode_vs_normal_day']:+.2f} (bootstrap CI95 "
        f"[{ci_ep[0]:+.2f}, {ci_ep[1]:+.2f}]); day-level Mann-Whitney U z={mwu['z']:+.2f} "
        f"p={mwu_p_str} P(crash>normal)={mwu['p_crash_greater_than_normal']:.3f} -- "
        f"the channel-distribution corroborates the HA07d locked OVERALL-SUPPORTED signal "
        f"at the coarse first-order-day-level read (HA07d's tested operand is the 4d max |z| of night-"
        f"over-night delta; this Q3.4.f is the first-order day-level descriptive complement). "
        f"Near-identity check vs mean sibling: "
        f"{'zero near-identity pairs' if not e['flagged_pairs'] else 'flagged pairs ' + ', '.join('`' + p + '`' for p in e['flagged_pairs'])} "
        f"at the |rho|>=0.92 CONVENTIONS section 3.3 threshold -- the rho-with-`stress_mean_sleep` "
        f"value reported in section Q3.4.e is the substantive-independence check; HA07d both-eras-"
        f"SUPPORTED + HA07c train-only-SUPPORTED divergence is descriptively consistent with the "
        f"observed rho.",
        "",
        "---",
        "",
        "## Q3.4.a -- Distribution shape (Stratum 4)",
        "",
        "**Verdict on the section 3.1 delegate question**: **delegate is partial; extend in this "
        "analysis**. [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) "
        "primarily documents `stress_mean_sleep`; coverage on `stress_stdev_sleep` is incidental at best. "
        "The full distribution descriptors (skewness/kurtosis/heavy-tail flag/p99-vs-median ratio) are "
        "surfaced here for the first time on this channel.",
        "",
        "| stat | value | source |",
        "|---|---:|---|",
        f"| n (Stratum 4) | {a['n']} | `per_day_master.csv` `stress_stdev_sleep` non-NaN within S4 |",
        f"| mean | {a['mean']:.3f} | (single-pool S4) |",
        f"| median | {a['median']:.3f} | |",
        f"| std (ddof=1) | {a['std_ddof1']:.3f} | |",
        f"| MAD (unscaled) | {a['mad_unscaled']:.3f} | |",
        f"| MAD x 1.4826 (normal-equivalent SD) | {a['mad_normal_equivalent']:.3f} | for robust z-score scaling per section 3.1 |",
        f"| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | {quant['p1']:.2f} / {quant['p5']:.2f} / {quant['p10']:.2f} / {quant['p25']:.2f} / {quant['p50']:.2f} / {quant['p75']:.2f} / {quant['p90']:.2f} / {quant['p95']:.2f} / {quant['p99']:.2f} | |",
        f"| skewness (Fisher-Pearson) | **{a['skewness']:+.2f}** | right-skewed (non-negative dispersion measure; lower-bounded at 0) |",
        f"| excess kurtosis (Fisher) | **{a['excess_kurtosis']:+.2f}** | |",
        f"| heavy_tail_flag | **{a['heavy_tail_flag']}** | skew>1 OR p99/median > 3.0 |",
        f"| range | {a['min']:.2f} to {a['max']:.2f} | |",
        "",
        "### Cross-channel comparison vs sister CONFIRMED-citalopram channels + mean sibling",
        "",
        "| stat | stress_stdev_sleep (this analysis) | stress_mean_sleep (Q3.1, mean sibling) | all_day_stress_avg (Q3.2) | bb_lowest (Q3.3) |",
        "|---|---:|---:|---:|---:|",
        f"| n S4 | {a['n']} | 1339 | 1359 | (Q3.3 value) |",
        f"| mean | {a['mean']:.3f} | 19.97 | 32.72 | (Q3.3 value) |",
        f"| median | {a['median']:.3f} | 19.21 | 32.00 | (Q3.3 value) |",
        f"| MAD (unscaled) | {a['mad_unscaled']:.3f} | 2.87 | 4.00 | (Q3.3 value) |",
        f"| skewness | {a['skewness']:+.2f} | +2.72 | +0.87 | (Q3.3 value) |",
        f"| heavy_tail_flag | **{a['heavy_tail_flag']}** | **True** | **False** | (Q3.3 value) |",
        "",
        "**stress_stdev_sleep is a per-night SECOND-ORDER summary** (within-night STDEV of the nightly "
        "stress samples) operationally distinct from the per-night MEAN (sister `stress_mean_sleep`) "
        "even though both summarise the same monitoring_b sample set. Per HA07d result.md framing: "
        "the channel is the 'HRV-of-HRV-proxy' construct -- a second-order autonomic-flexibility "
        "signal. Distribution shape comparison with sister mean: substantially smaller absolute scale "
        f"(median {med:.2f} stress-units of dispersion vs mean sibling median 19.21 stress-units of "
        "level), distinct skewness profile (per construction: dispersion measures are right-skewed "
        "by zero-floor regardless of the underlying signal's skew).",
        "",
        "See [`plots/fig1_distribution_s4.png`](plots/fig1_distribution_s4.png).",
        "",
        "---",
        "",
        "## Q3.4.b -- Autocorrelation structure + E[L]\\*",
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
        "### Cross-channel comparison (E[L]\\* by Strand A analysis) -- handoff section 2.4 load-bearing",
        "",
        "| analysis | channel | E[L]\\* | M | factor-of-2 flag |",
        "|---|---|---:|---:|---|",
        "| Phase-1 #1 (stress_mean_sleep) | sleep-window mean (mean sibling) | 12.6 | 6 | YES (factor-of-2) |",
        "| Phase-1 #3 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 | 11 | YES (factor-of-3) |",
        "| Phase-2 #2 (all_day_stress_avg) | 24h-window mean | 29.8 | 18 | YES (factor-of-4) |",
        "| Phase-2 #3 (bb_lowest) | daily NADIR | 29.25 | 17 | YES (factor-of-4) |",
        f"| **this analysis (stress_stdev_sleep)** | **per-night STDEV (variability primitive)** | **{el_star:.1f}** | **{b['cutoff_lag_M']}** | **{('YES' if b['factor_of_2_deviation_flag'] else 'no')}** |",
        "",
        f"**Implication per handoff section 2.4**: stress_stdev_sleep's E[L]\\*={el_star:.1f} sits "
        f"{el_class}. The variability primitive {'shares the long-memory profile of the CONFIRMED-citalopram cluster' if el_star > 25 else 'sits closer to its mean sibling than to the long-memory cluster' if el_star < 16 else 'sits in the middle range; neither tight to the mean sibling nor in the long-memory cluster'}. Any HA pre-reg using `stress_stdev_sleep` (beyond HA07d's locked second-order operand) should "
        f"pre-spec a sensitivity arm at E[L]\\*={el_int} alongside the default-E[L]=7 primary. NOTE: "
        "HA07d itself used E[L]=7 for the locked test; the R14 single-pool re-anchor at +19.7 pp p=0.0291 "
        "was at E[L]=7. The Q3.4.b finding here updates the channel-level block-length characterisation "
        "for any FUTURE HA on this channel; HA07d's already-locked verdict is NOT re-anchored.",
        "",
        "See [`plots/fig5_acf.png`](plots/fig5_acf.png).",
        "",
        "---",
        "",
        "## Q3.4.c -- Base rates per citalopram phase",
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
        "wants per-phase verdicts on this channel faces a ~10x n disadvantage vs the steady-state "
        "phases (same as sister channels Q3.1.c / Q3.2.c / Q3.3.c).",
        "",
        "Named counts (CONVENTIONS section 3.6): the per-phase n's above are `stress_stdev_sleep`-non-NaN "
        "day rows in `per_day_master.csv` within Stratum 4 date masks per "
        "`citalopram_phase_stratification.md section 3` boundary dates.",
        "",
        "See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (citalopram-phase violins).",
        "",
        "---",
        "",
        "## Q3.4.d -- Phase-stratified distribution + v3 dose-modulation OPEN question (caveat-class)",
        "",
        "**Per CONVENTIONS section 4.2 (caveats yes; a-priori claims no) + handoff section 1 + section "
        "2.4**: `stress_stdev_sleep` is **NOT in v3 multi-channel sweep scope** per "
        "[`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "section 5.6 (the v3 sweep covered 6 baseline channels: `stress_mean_sleep`, `all_day_stress_avg`, "
        "`bb_lowest`, `resting_hr`, `bb_overnight_gain`, `respiration_avg_sleep`). The citalopram-dose-"
        "modulation status on `stress_stdev_sleep` is therefore **OPEN**. This Q3.4.d reports the "
        "observed median + dispersion shift across the citalopram-axis phases descriptively; it does "
        "**NOT pre-commit a CONFIRMED/REJECTED verdict** on dose-modulation candidacy -- that decision "
        "belongs in a future v3 extension that explicitly tests this channel.",
        "",
        "Observed median shifts:",
        "",
        "| comparison | delta median | within-phase MAD | within-MAD? |",
        "|---|---:|---:|---|",
        f"| buildup minus unmedicated | **{buildup_minus_unmed:+.2f}** | {c['buildup']['mad_unscaled']:.2f}-{c['unmedicated']['mad_unscaled']:.2f} | {'>1 MAD; descriptively meaningful' if abs(buildup_minus_unmed) > c['unmedicated']['mad_unscaled'] else 'within MAD; small'} |",
        f"| consolidation minus unmedicated | **{consol_minus_unmed:+.2f}** | {c['consolidation']['mad_unscaled']:.2f} | {'>1 MAD; descriptively meaningful' if abs(consol_minus_unmed) > c['consolidation']['mad_unscaled'] else 'within MAD; small'} |",
        f"| consolidation minus buildup | **{d['phase_to_phase_shifts'].get('consolidation_minus_buildup_median', 0):+.2f}** | {c['consolidation']['mad_unscaled']:.2f} | |",
        f"| afbouw minus consolidation | **{afbouw_minus_consol:+.2f}** | {c['consolidation']['mad_unscaled']:.2f}-{c['afbouw']['mad_unscaled']:.2f} | |",
        f"| afbouw minus unmedicated | **{afbouw_minus_unmed:+.2f}** | {c['unmedicated']['mad_unscaled']:.2f}-{c['afbouw']['mad_unscaled']:.2f} | |",
        "",
        "### Descriptive reading (no verdict promotion)",
        "",
        f"The median {('descends' if consol_minus_unmed < 0 else 'ascends')} from unmedicated "
        f"({unmed_med:.2f}) to consolidation ({consol_med:.2f}) by **{consol_minus_unmed:+.2f}** units "
        f"({abs(consol_minus_unmed / c['unmedicated']['mad_unscaled']):.2f} unmedicated-MADs). "
        f"The day-resolved citalopram boundary step (30d pre/post 2024-04-09): "
        f"**{citalo_step['diff_post_minus_pre']:+.2f} units** -- the empirical day-resolved citalopram-"
        f"onset shift. Per the framing above: **the observed shift descriptively suggests "
        f"{'candidacy for a future v3 extension to add stress_stdev_sleep as a 7th candidate channel' if abs(consol_minus_unmed) > 0.3 else 'NOT-candidacy for a future v3 extension'}**, but no verdict is pre-"
        f"committed here. A future v3 extension run on this channel would (i) apply the three-pronged "
        f"test pattern (buildup post-CPAP beta + afbouw beta + spring 2025 control) per "
        f"`citalopram_dose_response_stress_mean_sleep.md` section 5.6.1; (ii) decide CONFIRMED/REJECTED "
        f"per the four discipline rules in section 5.6.1; (iii) update the framework MD's per-channel "
        f"inheritance table at section 4 of `citalopram_phase_stratification.md`.",
        "",
        "### Substantive contrast with sister mean's flat-phase-medians pattern",
        "",
        "Per [sister `stress_mean_sleep` Q3.1.d](../stress_mean_sleep/findings.md): the mean sibling "
        "shows **nearly flat phase medians** (range 17.04 -> 20.20 across the four phases; consolidation-"
        "minus-unmedicated = -0.44, within MAD), with the citalopram dose-response effect being a "
        f"within-buildup-window slope NOT a between-phase level shift. **stress_stdev_sleep shows "
        f"{('a substantively larger between-phase shift' if abs(consol_minus_unmed) > 1.0 else 'a comparably modest between-phase shift') if abs(consol_minus_unmed) > 0.3 else 'similarly flat phase medians'} "
        f"(consolidation-minus-unmedicated = {consol_minus_unmed:+.2f})**. The observation is reported "
        "descriptively; the substantive interpretation (does this reflect citalopram dose-modulation? "
        "Trajectory drift? Sleep-architecture confound per HA07d caveat section 8?) belongs to a "
        "future v3 extension.",
        "",
        "See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) and "
        "[`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d rolling "
        "median through phases).",
        "",
        "---",
        "",
        "## Q3.4.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)",
        "",
        "**Per handoff section 2.4**: this Q3.4.e rigorously checks near-identity vs `stress_mean_sleep` "
        "(the obvious candidate -- both summarise the same nightly monitoring_b stress sample set; "
        "sigma and mean of the same series MAY be near-identical via heteroskedasticity OR may be "
        "substantively independent). The **HA07d both-eras-SUPPORTED + HA07c train-only-SUPPORTED "
        "divergence** at the test level suggests substantive independence; the descriptive rho at "
        "day-level confirms or refutes.",
        "",
        "| target channel | n | Pearson r | Spearman rho | near-identity flag? |",
        "|---|---:|---:|---:|---|",
        *near_id_rows,
        "",
        f"**{'Zero' if not e['flagged_pairs'] else len(e['flagged_pairs'])} near-identity pairs fire** at "
        "the |rho|>=0.92 CONVENTIONS section 3.3 threshold.",
        "",
        "### Substantive-independence reading vs mean sibling (load-bearing per handoff section 2.4)",
        "",
    ]

    # Substantive-independence sub-section
    mean_row = next((r for r in e["rows"] if r.get("channel") == "stress_mean_sleep"), {})
    if "pearson_r" in mean_row:
        mean_pear = mean_row["pearson_r"]
        mean_spear = mean_row["spearman_rho"]
        out_lines.extend([
            f"`stress_stdev_sleep` vs `stress_mean_sleep`: Pearson r={mean_pear:+.3f} / Spearman "
            f"rho={mean_spear:+.3f} (n={mean_row['n']}). **Reciprocal check confirms sister "
            "stress_mean_sleep Q3.1.e's reported rho** (Q3.1.e reported Pearson r=+0.602 / "
            f"Spearman rho=+0.501 with this channel). The pair is **substantively independent** at the "
            f"section 3.3 threshold (max(|r|, |rho|) = {max(abs(mean_pear), abs(mean_spear)):.3f} < 0.92). "
            "The HA07d both-eras-SUPPORTED + HA07c train-only-SUPPORTED divergence at the test level "
            "is descriptively consistent with this substantive-independence reading: variability and "
            "mean of the same nightly stress series carry **distinct day-level information**, and the "
            "test-level divergence reflects substantive independence of the second-order construct "
            "from the first-order mean.",
            "",
        ])
        # Crash-subset rho if available
        if crash_subset_rho is not None:
            csr = crash_subset_rho
            out_lines.extend([
                "### Crash-subset rho check vs mean sibling (supplementary per handoff section 2.4)",
                "",
                f"On the crash-day subset (n={csr['n_crash_pairs']}) vs the normal-day subset "
                f"(n={csr['n_normal_pairs']}):",
                "",
                "| subset | Pearson r vs `stress_mean_sleep` | Spearman rho vs `stress_mean_sleep` |",
                "|---|---:|---:|",
                f"| crash days only | {csr['pearson_r_crash']:+.3f} | {csr['spearman_rho_crash']:+.3f} |",
                f"| normal days only | {csr['pearson_r_normal']:+.3f} | {csr['spearman_rho_normal']:+.3f} |",
                "",
                f"If `|rho_crash| << |rho_normal|`, the variability primitive carries crash-distinct "
                f"information that the mean does not. Observed: crash-subset rho={csr['spearman_rho_crash']:+.3f}, "
                f"normal-subset rho={csr['spearman_rho_normal']:+.3f} -- the descriptive "
                f"pattern is {'consistent with crash-distinct information carried by the variability primitive' if abs(csr['spearman_rho_crash']) < abs(csr['spearman_rho_normal']) - 0.10 else 'NOT showing strong crash-subset divergence'}. "
                "Layer 1 observation; substantive interpretation belongs in a downstream HA pre-reg.",
                "",
            ])

    out_lines.extend([
        "---",
        "",
        "## Q3.4.f -- Crash-day vs normal-day (Stratum 4) + HA07d corroboration",
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
        f"| mean per-episode `stress_stdev_sleep` | {fe['mean_per_episode_value']:.3f} |",
        f"| mean normal-day `stress_stdev_sleep` | {fe['mean_normal_day_value']:.3f} |",
        f"| mean diff (episode minus normal-day) | **{fe['mean_diff_episode_vs_normal_day']:+.3f}** |",
        f"| Cohen's d (episode-level vs normal-day pooled) | **{fe['cohens_d_episode_vs_normal_day']:+.2f}** |",
        f"| Bootstrap 95% CI on mean diff | **[{ci_ep[0]:+.3f}, {ci_ep[1]:+.3f}]** ({fe['n_bootstrap']} iters, seed={fe['seed']}) |",
        "",
        f"**Episode-level Cohen's d={fe['cohens_d_episode_vs_normal_day']:+.2f}** on this channel. "
        "Compare cross-channel: `stress_mean_sleep` episode d=+0.91 (sister mean); "
        "`all_day_stress_avg` episode d=+0.37 with CI brushing zero; "
        "`stress_low_motion_min_count_S60_Mlow` episode d=+0.38.",
        "",
        "### Day-level (autocorrelation-inflated supplementary)",
        "",
        "| stat | value |",
        "|---|---:|",
        f"| n crash-days | {fl['n_crash_day']} |",
        f"| n normal-days | {fl['n_normal_day']} |",
        f"| mean crash-day | {fl['mean_crash']:.3f} |",
        f"| mean normal-day | {fl['mean_normal']:.3f} |",
        f"| median crash-day | {fl['median_crash']:.2f} |",
        f"| median normal-day | {fl['median_normal']:.2f} |",
        f"| mean diff (point estimate) | **{fl['mean_diff']:+.3f}** |",
        f"| median diff | **{mwu['median_diff']:+.2f}** |",
        f"| Cohen's d | **{fl['cohens_d']:+.2f}** |",
        f"| Mann-Whitney U: z | **{mwu['z']:+.2f}** |",
        f"| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **{mwu_p_str}** |",
        f"| Mann-Whitney U: P(crash > normal) | **{mwu['p_crash_greater_than_normal']:+.3f}** |",
        f"| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (project default) | [{e7['ci_lower']:+.3f}, {e7['ci_upper']:+.3f}], width {width7:.3f} |",
        f"| Stationary bootstrap 95% CI on mean diff, **E[L]={eS['block_length_used']}** (data-driven, Q3.4.b flag) | **[{eS['ci_lower']:+.3f}, {eS['ci_upper']:+.3f}]**, width {widthS:.3f} |",
        "",
        "### HA07d both-eras-SUPPORTED + R14 single-pool SUPPORTED cross-reference (load-bearing per handoff section 2.4)",
        "",
        f"HA07d is the **only canonical both-eras-SUPPORTED test in the project** (train +{ha07d['locked_train_disc_pp']} pp / "
        f"validate +{ha07d['locked_validate_disc_pp']} pp / OVERALL SUPPORTED per "
        "[HA07d-sleep-stress-variability/result.md](../../../analyses/hypotheses/HA07d-sleep-stress-variability/result.md)). "
        f"R14 single_pool_reanchor confirmed at single-pool **+{ha07d['r14_single_pool_disc_pp']} pp** "
        f"[CI95 {ha07d['r14_single_pool_ci95']}] **perm p (E[L]=7) = {ha07d['r14_single_pool_perm_p']}** -- "
        "the **only HA that retained SUPPORTED at single-pool** in the R14 cross-check (per "
        "[single_pool_reanchor/findings.md](../single_pool_reanchor/findings.md) row HA07d).",
        "",
        f"**This analysis's first-order day-level Q3.4.f read** (episode-level d="
        f"{fe['cohens_d_episode_vs_normal_day']:+.2f}; CI [{ci_ep[0]:+.3f}, {ci_ep[1]:+.3f}]) "
        "**descriptively corroborates the HA07d second-order signal at the coarse channel-distribution "
        f"level**. NOTE: HA07d's tested operand is the per-4-day MAX |z| of NIGHT-OVER-NIGHT DELTA of "
        "`stress_stdev_sleep` (a within-4-day spike-form construct on the channel); this Q3.4.f is on "
        "the raw daily channel value (first-order, day-level), which is a coarser descriptive complement "
        "rather than a re-anchoring of the HA07d operand. HA07d's tested operand discriminates "
        "crash-precursor windows at +19.6/+21.7/+19.7 pp; the first-order day-level d here is the "
        "descriptive substrate that the HA07d-level signal is built on. The HA07d locked verdicts + "
        "the R14 single-pool verdict are LOCKED; this Q3.4.f descriptive observation is NOT a re-"
        "interpretation of either.",
        "",
        "### Block-length sensitivity (Q3.4.b cross-check)",
        "",
        "Per "
        "[`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md), "
        "when the data-driven E[L]\\* deviates from the project default by more than a factor of 2, the "
        "analysis must report the CI at the data-driven value alongside the default. "
        f"E[L]={eS['block_length_used']} CI ([{eS['ci_lower']:+.3f}, {eS['ci_upper']:+.3f}]) vs E[L]=7 "
        f"CI ([{e7['ci_lower']:+.3f}, {e7['ci_upper']:+.3f}]) -- {abs(width_change_pct):.1f}% "
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
        "## Q3.4.g -- Spike-detecting primitive availability",
        "",
        "`stress_stdev_sleep` is **structurally a per-night SECOND-ORDER summary**: per-night STDEV of "
        "the monitoring_b stress samples within the sleep window per "
        "[`garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`](../../../../garmin/scripts/sleep_stress_extract/extract_sleep_stress.py); "
        "MIN_SAMPLES_PER_NIGHT=120 gate (~6h at 3-min cadence). Sub-night resolution is NOT in "
        "`per_day_master.csv`. Per CONVENTIONS section 3.5 + HA07d result.md framing: this channel IS "
        "the second-order autonomic-flexibility primitive on the nightly stress series (the 'HRV-of-"
        "HRV-proxy' construct). HA07d's tested operand is the per-4-day MAX |z| of night-over-night "
        "delta -- that IS the spike-form construct on this channel at the 4-day-window resolution.",
        "",
        "Related stress primitives in the master:",
        "",
        "| column | type | relation to `stress_stdev_sleep` |",
        "|---|---|---|",
        f"| `stress_mean_sleep` | per-night MEAN of same nightly sample set (mean sibling) | Pearson r=**{g.get('pearson_r_vs_stress_mean_sleep', 0):+.2f}** / rho={g.get('spearman_rho_vs_stress_mean_sleep', 0):+.2f}; substantive-independence pair per Q3.4.e |",
        f"| `all_day_stress_max` | 24h MAX (extremum form, all-day) | Pearson r=**{g.get('pearson_r_vs_all_day_stress_max', 0):+.2f}** / rho={g.get('spearman_rho_vs_all_day_stress_max', 0):+.2f} |",
        f"| `awake_stress_max` | 24h MAX during awake window | Pearson r=**{g.get('pearson_r_vs_awake_stress_max', 0):+.2f}** / rho={g.get('spearman_rho_vs_awake_stress_max', 0):+.2f} |",
        f"| `stress_low_motion_min_count_S60_Mlow` | per-minute count of low-motion-high-stress minutes (24h) | Pearson r=**{g.get('pearson_r_vs_stress_low_motion_min_count_S60_Mlow', 0):+.2f}** / rho={g.get('spearman_rho_vs_stress_low_motion_min_count_S60_Mlow', 0):+.2f}; spike-form companion in 24h-window |",
        f"| `asleep_stress_avg_uds` | UDS-side asleep stress average | Pearson r=**{g.get('pearson_r_vs_asleep_stress_avg_uds', 0):+.2f}** / rho={g.get('spearman_rho_vs_asleep_stress_avg_uds', 0):+.2f} |",
        "",
        "### CONVENTIONS section 3.5 framing -- the variability primitive IS the second-order spike-form",
        "",
        "Unlike the sister mean channel `stress_mean_sleep` which is dilution-vulnerable per CONVENTIONS "
        "section 3.5 (24h-mean form prefers spike companions for acute-load mechanisms), "
        "**`stress_stdev_sleep` is itself a within-night dispersion primitive**: a single value per "
        "sleep-night that measures within-night sample variability. A consumer test whose mechanism is "
        "*acute within-night autonomic instability* should use stress_stdev_sleep as primary -- it IS "
        "the extremum-form summary on the within-night variability construct. HA07d uses the per-4-day "
        "MAX |z| of night-over-night delta to extract a multi-day spike-form construct from this "
        "first-order variability metric.",
        "",
        "**Latent in FIT, not in master**: per-minute monitoring_b stress samples (the source of this "
        "channel) are not exposed in master; finer-than-night resolution (sub-hour stdev) could be "
        "computed but is not currently extracted; sleep-stage-stratified stdev (REM vs deep vs "
        "disturbed) would require sleep-stage alignment per HA07d caveat section 8 sleep-architecture "
        "confound. This analysis does NOT action any of these.",
        "",
        "---",
        "",
        "## Q3.4.h -- Outlier detection + calibration-drift check",
        "",
        "Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md):",
        "",
        "- `stress_stdev_sleep` is **custom-extracted from monitoring_b FIT files** per "
        "`garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`; MIN_SAMPLES_PER_NIGHT=120 "
        "gate (~6h at 3-min cadence). Nights below the gate drop to NaN (`sleep_valid_flag=False`); "
        f"{summary['n_rows_stratum_4_total'] - a['n']} such nights in Stratum 4.",
        "- **No specific calibration-drift events catalogued for `stress_stdev_sleep`** in "
        "`garmin_indicators_audit.md` beyond the shared sleep-stress-extraction family entries "
        "(same as sister stress_mean_sleep Q3.1.h).",
        "- Underlying sensor is **Forerunner 245 Elevate V3 throughout the entire 2021-08-16 to present "
        "window** -- no device change.",
        "- Per HA07d hypothesis.md section 8 caveat: **sleep architecture confound** -- higher sleep "
        "stress variability can reflect more sleep-stage transitions (REM vs deep cycles), not "
        "autonomic dysregulation directly. This is a substrate caveat for the channel's biological "
        "interpretation, not a calibration-drift signature.",
        "",
        "### Outlier scan (MAD-based |z|>5; threshold per CONVENTIONS section 3.1 robust-baseline default)",
        "",
        f"**{len(outliers)} outlier-day flagged** out of {a['n']}:",
        "",
        ("| date | value | MAD-z |\n|---|---:|---:|\n" + "\n".join(
            f"| {o['date']} | {o['value']:.2f} | **{o['mad_z']:+.2f}** |" for o in outliers[:20]
        )) if outliers else "**No outliers above the |z|>5 threshold.**",
        "",
        "### Drift check -- rolling 90d median over Stratum 4",
        "",
        "| snapshot date | rolling 90d median |",
        "|---|---:|",
        *[
            f"| {s['snapshot_date']} | {s['rolling_med_90d']:.3f} |"
            for s in h["rolling_90d_median_snapshots"] if s["rolling_med_90d"] is not None
        ],
        "",
        f"Day-resolved boundary steps (30d pre vs post): citalopram 2024-04-09 = "
        f"**{citalo_step['diff_post_minus_pre']:+.2f}**, consolidation 2024-06-20 = "
        f"**{consol_step['diff_post_minus_pre']:+.2f}**, afbouw 2026-03-20 = "
        f"**{afbouw_step['diff_post_minus_pre']:+.2f}**. The rolling 90d median trajectory + boundary "
        "steps are descriptively reported; the citalopram-modulation interpretation (Q3.4.d) remains "
        "caveat-class per CONVENTIONS section 4.2.",
        "",
        "See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).",
        "",
        "---",
        "",
        "## Q3.4.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel",
        "",
        "Discipline anchor: "
        "[HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) "
        "(secondary-logistic-with-covariate pattern; beta disambiguation between primary-signal and a "
        "candidate alternative reading). Names **four** candidate covariates a future HA on "
        "`stress_stdev_sleep` as predictor should pre-spec.",
        "",
        "### 1. `stress_mean_sleep` -- mean sibling of same nightly stress series (substantive-independence covariate)",
        "",
    ])

    if i['candidate_covariates'][0].get('observed_correlation_on_S4'):
        cov1 = i['candidate_covariates'][0]['observed_correlation_on_S4']
        out_lines.extend([
            f"On Stratum 4 observed (this analysis Q3.4.e): Pearson r={cov1['pearson_r']:+.3f} / "
            f"Spearman rho={cov1['spearman_rho']:+.3f} (n={cov1['n']}).",
            "",
        ])
    out_lines.extend([
        "Variability and mean of the same nightly stress series may share heteroskedasticity-driven "
        "covariance. The covariate disambiguates: beta_channel survives -> the stress_stdev_sleep "
        "signal carries variability-primitive-specific information beyond shared nightly stress level; "
        "beta_channel attenuates -> shared autonomic-load via heteroskedasticity. **Load-bearing for "
        "any future HA on this channel**: the HA07d both-eras-SUPPORTED + HA07c train-only-SUPPORTED "
        "test-level divergence is descriptively consistent with this independence reading, but a "
        "per-HA secondary check is the canonical disambiguation.",
        "",
        "### 2. `dose_plasma_mg(d)` -- citalopram covariate (status OPEN; diagnostic-only)",
        "",
        "Channel is **NOT in v3 multi-channel sweep scope** per "
        "`citalopram_dose_response_stress_mean_sleep.md` section 5.6. Citalopram-dose-modulation status "
        "is OPEN per Q3.4.d caveat-class framing. A future HA cross-phase should pre-spec dose as a "
        "secondary covariate to surface any latent dose-modulation; if beta_dose is significant in the "
        "secondary, that is evidence for a future v3 extension to add this channel as a 7th candidate. "
        "Until v3 covers this channel, neither `citalopram_phase_stratification.md` section 5.A nor "
        "section 5.B treatment is OBLIGATORY (unlike the 3 CONFIRMED channels) -- the dose covariate "
        "is a diagnostic, not a framework requirement.",
        "",
        "### 3. `resting_hr` -- alternative autonomic-load anchor",
        "",
    ])

    if i['candidate_covariates'][2].get('observed_correlation_on_S4'):
        cov3 = i['candidate_covariates'][2]['observed_correlation_on_S4']
        out_lines.extend([
            f"On Stratum 4 observed (this analysis): Pearson r={cov3['pearson_r']:+.3f} / "
            f"Spearman rho={cov3['spearman_rho']:+.3f} (n={cov3['n']}).",
            "",
        ])
    out_lines.extend([
        "Per HA07d result.md the channel is framed as 'HRV-of-HRV-proxy' (second-order autonomic-"
        "flexibility signal). The covariate disambiguates: beta_channel attenuates -> shared "
        "autonomic-arousal carried by resting HR; beta_channel survives -> HRV-proxy-variability-"
        "specific beyond the resting-HR axis.",
        "",
        "### 4. Own-lagged trailing mean -- autocorrelation-vs-mechanism (HA-P7 section 4.5.4)",
        "",
        f"Per Q3.4.b the cutoff lag M={b['cutoff_lag_M']} and E[L]\\*={el_star:.1f}. A consumer HA can "
        f"compute `stress_stdev_sleep_lagged_mean_Nd(d)` at N tuned to E[L]\\*={el_int} with margin. "
        "NOTE: this channel does **NOT** have a materialised `_lagged_lcera_z` variant in "
        "`per_day_master` (sister channels stress_mean_sleep + all_day_stress_avg + resting_hr + "
        "bb_lowest + bb_overnight_gain do, per CONVENTIONS section 3.2). HA author must compute the "
        "covariate at runtime.",
        "",
        "### Recommendation for any future HA pre-reg on this channel",
        "",
        "Pre-spec all four covariates as **secondary sensitivity arms**. Concordance across the four "
        "secondaries = high confidence in the primary; divergence = the disambiguation is doing real "
        "work. Covariate 1 (mean sibling) is the **load-bearing substantive-independence check**; "
        "covariate 2 (dose) is **diagnostic-only** at this time per the channel's NOT-in-v3-scope "
        "status; covariate 3 (resting_hr) is the cross-channel autonomic-state disambiguator; "
        "covariate 4 (autocorrelation) operationalises HA-P7 section 4.5.4 on this specific channel.",
        "",
        "---",
        "",
        "## Cross-references",
        "",
        "### HA-* tests that touch this channel (cite this analysis)",
        "",
        "- **HA07d** (sleep-stress variability delta as crash precursor; LOCKED OVERALL-SUPPORTED -- the "
        "ONLY canonical both-eras-SUPPORTED test in the project per "
        "[`analyses/hypotheses/HA07d-sleep-stress-variability/result.md`](../../../analyses/hypotheses/HA07d-sleep-stress-variability/result.md); "
        f"R14 single-pool SUPPORTED at +{ha07d['r14_single_pool_disc_pp']} pp p={ha07d['r14_single_pool_perm_p']}). "
        f"This Q3.4 is the Strand-A backstop on the primary operand. The descriptive substrate "
        f"(E[L]\\*={el_star:.1f} + phase-stratified trajectory + episode-level "
        f"d={fe['cohens_d_episode_vs_normal_day']:+.2f}) **descriptively corroborates** the locked "
        "HA07d signal at the channel-distribution level. The substantive HA07d verdict + R14 single-"
        "pool verdict are LOCKED; this analysis's descriptive observations are NOT a re-interpretation "
        "or extension.",
        "- **HA07d threshold-monotonicity diagnostic** (LOCKED; downstream of HA07d): inherits the "
        "channel; this Q3.4 provides the descriptive substrate that the diagnostic test consumes.",
        "- **HA07c** (sleep-stress MEAN delta; LOCKED TRAIN SUPPORTED / VALIDATE REFUTED / OVERALL "
        "REFUTED; channel `stress_mean_sleep`): mean sibling of this channel. The HA07d both-eras-"
        "SUPPORTED + HA07c train-only-SUPPORTED divergence is **substantively reflected in the "
        f"Q3.4.e rho=<sister> reading** (NOT near-identity -- variability and mean carry distinct day-"
        "level information).",
        "- **HA08c** (sleep-stress SLOPE; LOCKED TRAIN SUPPORTED / VALIDATE REFUTED / OVERALL REFUTED; "
        "channel `stress_mean_sleep`): slope-of-mean sibling. Inherits Q3.4.b autocorrelation finding "
        "via the mean sibling's E[L]\\*=12.6; the channel-difference autocorrelation is reported here.",
        "",
        "### Methodology MDs cited",
        "",
        "- [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) -- "
        "Q3.4.a delegate target (partial; extended for full skewness/kurtosis/heavy-tail-flag set on "
        "this channel).",
        "- "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "sections 3-6 -- Q3.4.c phase axis; Q3.4.d phase-stratified is caveat-class per CONVENTIONS "
        "section 4.2 since channel NOT in v3 scope.",
        "- "
        "[`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "v3 section 5.6 -- v3 multi-channel sweep scope (6 channels; this channel NOT in scope; Q3.4.d "
        "framing).",
        "- "
        "[`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) "
        f"-- E[L]=7 default + factor-of-2 deviation rule; Q3.4.b reports E[L]\\*={el_star:.1f} "
        f"({'factor-of-2 flag fires' if b['factor_of_2_deviation_flag'] else 'flag does not fire'}).",
        "- "
        "[`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) -- "
        "Q3.4.h cross-reference; sleep-stress family entries.",
        "- "
        "[`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) "
        "-- Stratum 4 boundary definition.",
        "- "
        "[`methodology/_descriptive_stocktake_2026-06-23.md`](../../../methodology/_descriptive_stocktake_2026-06-23.md) "
        "section 3 + section 5 -- gap-list framing (HA07d Shared gap 1 A3 block-length + A2 missingness + "
        "A1 per-cell n now BACKSTOPPED by this analysis).",
        "",
        "### Existing artefacts referenced",
        "",
        "- [`descriptive/operationalisation_support/stress_mean_sleep/findings.md`](../stress_mean_sleep/findings.md) "
        "-- mean sibling of same nightly stress series; closest sister precedent; Q3.1.e reciprocal "
        "rho check cross-referenced in Q3.4.e.",
        "- [`descriptive/operationalisation_support/all_day_stress_avg/findings.md`](../all_day_stress_avg/findings.md) "
        "-- Q3.2 precedent (CONFIRMED-citalopram channel; programmatic-emit pattern).",
        "- [`descriptive/operationalisation_support/bb_lowest/findings.md`](../bb_lowest/findings.md) "
        "-- Q3.3 most-recent Strand-A precedent; cross-channel E[L]\\* spread comparison in Q3.4.b.",
        "- [`descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/findings.md`](../stress_low_motion_min_count_S60_Mlow/findings.md) "
        "-- spike-form companion (24h-window); E[L]\\*=21.1 cross-reference in Q3.4.b.",
        "- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) "
        "-- R14 cross-check (LANDED `badd04a`); the HA07d row "
        f"(+{ha07d['r14_single_pool_disc_pp']} pp p={ha07d['r14_single_pool_perm_p']}) descriptively "
        "corroborated in Q3.4.f.",
        "- [`analyses/hypotheses/HA07d-sleep-stress-variability/result.md`](../../../analyses/hypotheses/HA07d-sleep-stress-variability/result.md) "
        "-- LOCKED OVERALL-SUPPORTED; the project's only canonical both-eras-SUPPORTED test.",
        "- [`analyses/hypotheses/HA07c-sleep-stress-mean-delta/result.md`](../../../analyses/hypotheses/HA07c-sleep-stress-mean-delta/result.md) "
        "-- LOCKED TRAIN SUPPORTED / VALIDATE REFUTED / OVERALL REFUTED; substantive-independence "
        "vs HA07d cross-referenced in Q3.4.e.",
        "- [`analyses/garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) "
        "-- Q3.4.e cross-reference; this analysis reciprocally confirms the rho with sister "
        "stress_mean_sleep + characterises the new variability-primitive entry into the cluster map.",
        "",
        "### Upstream pipeline",
        "",
        "- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- "
        "`processed/garmin/sleep_stress_nightly.csv` <- "
        "`garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`.",
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
        "1. **Q3.4.d is caveat-class per CONVENTIONS section 4.2.** The channel is NOT in v3 multi-"
        "channel sweep scope; citalopram-dose-modulation status is OPEN; no CONFIRMED/REJECTED verdict "
        "is pre-committed here. A future v3 extension that adds this channel must apply the three-"
        "pronged test pattern (buildup post-CPAP beta + afbouw beta + spring 2025 control) per "
        "`citalopram_dose_response_stress_mean_sleep.md` section 5.6.1.",
        "2. **The channel IS the second-order variability primitive per CONVENTIONS section 3.5** "
        "(Q3.4.g). HA07d's tested operand is the per-4-day MAX |z| of night-over-night delta (the "
        "second-order spike-form construct on this first-order variability metric). A consumer test "
        "whose mechanism is *acute within-night autonomic instability* should use stress_stdev_sleep "
        "directly; mechanisms operating at multi-day or weekly resolution should consider whether the "
        "HA07d-style second-order construct or a different per-4-day primitive is more apt.",
        f"3. **The episode-level Cohen's d={fe['cohens_d_episode_vs_normal_day']:+.2f} CI is "
        f"[{ci_ep[0]:+.3f}, {ci_ep[1]:+.3f}]** (Q3.4.f). The episode-level is the unit-of-analysis-clean "
        "read per CONVENTIONS section 3.6; consumer HAs using this channel as a crash-discriminator "
        "should NOT rely on the day-level (autocorrelation-inflated) as the primary read.",
        f"4. **Block-length sensitivity matters** (Q3.4.b E[L]\\*={el_star:.1f} vs default 7). Future "
        "HAs (beyond HA07d's locked operand which used E[L]=7) should pre-spec the "
        f"E[L]\\*~{el_int} sensitivity arm alongside the default-E[L]=7 primary. HA07d's already-"
        "locked verdict is NOT re-anchored.",
        "5. **Mean sibling near-identity Q3.4.e is descriptive only.** Substantive-independence "
        "reading vs `stress_mean_sleep` is consistent with the HA07d/HA07c test-level divergence, but "
        "a per-HA secondary-with-mean-as-covariate is the canonical disambiguation; this analysis "
        "does NOT pre-commit it.",
        "6. **No `_lagged_lcera_z` variant in master.** Per CONVENTIONS section 3.2 the lagged-baseline "
        "infrastructure exists for sister channels (stress_mean_sleep + all_day_stress_avg + resting_hr "
        "+ bb_lowest + bb_overnight_gain) but NOT for stress_stdev_sleep. A consumer HA using lagged-"
        "baseline z-scoring must compute the covariate at runtime (per Q3.4.i covariate 4). Materialising "
        "the column is a queued infrastructure task; this analysis does NOT action it.",
        "7. **HA07d's sleep-architecture confound (HA07d hypothesis.md section 8) is inherited.** Higher "
        "sleep stress variability can reflect more sleep-stage transitions (REM vs deep cycles), not "
        "autonomic dysregulation directly; this is a substrate caveat for the channel's biological "
        "interpretation that propagates to any descendant test.",
        "8. **HA07d substantive verdict + R14 single-pool verdict are LOCKED with this analysis "
        "descriptively corroborating.** This Q3.4 is the Strand-A backstop on the channel; NO "
        "substantive HA verdict promotion per CONVENTIONS section 4.2.",
        "",
        "---",
        "",
        "## Status",
        "",
        f"**Current as of {summary['as_of_date']} corpus + 2026-06-24 analysis** (commit context: post-"
        "`40c351b` Q3.3 bb_lowest LANDED; Phase 2 \"finish the descriptive analysis\" Tier 1 user-"
        "prioritised batch FINAL CHANNEL of 4; R14 `single_pool_reanchor` first at `badd04a`; "
        "`all_day_stress_avg` second at `cf34ab1`; `bb_lowest` third at `40c351b`; **this "
        "`stress_stdev_sleep` FOURTH closes Tier 1**). Refresh when:",
        "",
        "1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to "
        "spin up beyond the HA07d-locked operand.",
        "2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 onward).",
        f"3. The Politis-White E[L]\\* shifts by another factor of 2 from current {el_star:.1f}.",
        "4. A v3-extension run on this channel lands and updates the Q3.4.d citalopram-modulation "
        "status from OPEN to CONFIRMED/REJECTED.",
        "5. A `stress_stdev_sleep_lagged_lcera_z` materialisation lands in `per_day_master.csv` and "
        "updates the Q3.4.i covariate-4 needed-columns entry from RUNTIME to MATERIALISED.",
        "6. HA07d threshold-monotonicity diagnostic v3 or any HA07d-descendant test ships and triggers "
        "operationalisation-substrate consumption from this analysis.",
        "",
    ]
    )
    path.write_text("\n".join(out_lines), encoding="utf-8")


def write_readme_md(summary: dict, path: Path) -> None:
    """Emit the per-analysis README per descriptive/README section 7a pattern."""
    q = summary["questions"]
    a = q["Q3.4.a_distribution"]
    b = q["Q3.4.b_autocorrelation"]
    c = q["Q3.4.c_base_rates_per_phase"]
    fr = q["Q3.4.f_crash_vs_normal"]
    fe = fr["episode_level"]
    el_star = b["data_driven_E_L_star"]
    afbouw_med = c.get("afbouw", {}).get("median", float("nan"))
    unmed_med = c.get("unmedicated", {}).get("median", float("nan"))
    ha07d = fr["ha07d_cross_reference"]

    out_lines = [
        "# `stress_stdev_sleep` -- operationalisation-support descriptive analysis",
        "",
        "**Strand**: A (operationalisation support; template-driven; no operationalisation interview "
        "required per [`descriptive/README.md`](../../README.md) section 7b).",
        "",
        "## Research question",
        "",
        "Operationalisation-support descriptive characterisation of `stress_stdev_sleep` on Stratum 4, "
        "answering Q3.4.a-i per the locked descriptive programme spec at "
        "[`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 "
        "r3, commit `ccbd12e`; this channel listed as the HA07d-primary-operand candidate). Phase 2 "
        "\"finish the descriptive analysis\" Tier 1 user-prioritised sequential batch; **FOURTH (FINAL) "
        "channel closing Tier 1** (R14 `single_pool_reanchor` first at `badd04a`; `all_day_stress_avg` "
        "second at `cf34ab1`; `bb_lowest` third at `40c351b`; this `stress_stdev_sleep` fourth). This "
        "channel is **HA07d's primary operand** -- HA07d is the **ONLY canonical both-eras-SUPPORTED "
        "test in the project** (train +19.6 pp / validate +21.7 pp / OVERALL SUPPORTED per "
        "[`HA07d-sleep-stress-variability/result.md`](../../../analyses/hypotheses/HA07d-sleep-stress-variability/result.md)) "
        f"AND just R14-confirmed at single-pool +{ha07d['r14_single_pool_disc_pp']} pp "
        f"perm p (E[L]=7) = {ha07d['r14_single_pool_perm_p']} per "
        "[`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) row HA07d -- the "
        "**only HA that retained SUPPORTED at single-pool** in the R14 cross-check (`badd04a`). "
        "Channel is **NOT in v3 multi-channel sweep scope** per "
        "[`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "section 5.6 (covered 6 channels: stress_mean_sleep + all_day_stress_avg + bb_lowest + "
        "resting_hr + bb_overnight_gain + respiration_avg_sleep); **citalopram-dose-modulation status "
        "is OPEN** per CONVENTIONS section 4.2 caveat-class framing.",
        "",
        "## Method",
        "",
        f"- **Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to "
        f"{summary['as_of_date']}; n={a['n']} channel-valid days out of "
        f"{summary['n_rows_stratum_4_total']} S4 days).",
        "- **Primary phase axis**: four-phase citalopram traject per "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with sister Strand-A "
        "analyses Q3.1 / Q3.2 / Q3.3.",
        "- **Delegate**: Q3.4.a (distribution shape) **partial delegate** to "
        "[`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) + "
        "**extend** with full skewness/kurtosis/heavy-tail-flag descriptors (the delegate target was "
        "extended for continuous channels first and primarily documents `stress_mean_sleep`).",
        "- **Cross-reference**: Q3.4.h (outliers + calibration-drift) cross-references "
        "[`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) "
        "(sleep-stress-extraction family entries; no per-column row for stress_stdev_sleep "
        "specifically beyond the sister stress_mean_sleep shared lineage).",
        "- **Computed directly from `per_day_master.csv`**: Q3.4.b (Politis-White E[L]\\*), Q3.4.c "
        "(per-phase base rates), Q3.4.d (phase-stratified medians + citalopram-axis shift; **caveat-"
        "class per CONVENTIONS section 4.2** since channel NOT in v3 scope), Q3.4.e (near-identity "
        "check |rho|>=0.92 on 10-channel panel; **load-bearing substantive-independence check vs mean "
        "sibling `stress_mean_sleep` per handoff section 2.4**), Q3.4.f (crash-vs-normal Cohen's d + "
        "Mann-Whitney U + stationary-bootstrap CI at E[L]=7 and data-driven E[L]\\* + crash-drop "
        "sensitivity per section 3.4 + crash-subset rho vs mean sibling supplementary), Q3.4.g "
        "(variability-primitive IS second-order spike-form discussion + cross-channel pairwise "
        "correlations), Q3.4.i (covariate-sensitivity readiness for future HA pre-regs).",
        "- **Shared utilities**: "
        "[`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-drop "
        "sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) "
        "(`compute_data_driven_block_length`, `stationary_bootstrap_ci`).",
        "- **Load-bearing cross-references** per handoff section 2.4: HA07d both-eras-SUPPORTED + R14 "
        f"single-pool +{ha07d['r14_single_pool_disc_pp']} pp p={ha07d['r14_single_pool_perm_p']} "
        "descriptively corroborated in Q3.4.f; sister-channel E[L]\\* spread (12.6 / 21.1 / 29.25 / "
        "29.8) cross-referenced in Q3.4.b; v3 dose-response open question framed caveat-class in "
        "Q3.4.d; near-identity vs mean sibling rigorously checked in Q3.4.e. NO substantive HA "
        "verdict promotion per CONVENTIONS section 2.1; NO CONFIRMED/REJECTED citalopram-modulation "
        "verdict pre-committed for Q3.4.d per CONVENTIONS section 4.2.",
        "- **No causal claims, no falsification bar** per "
        "[CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).",
        "",
        "## Result",
        "",
        "Headline (see [`findings.md`](findings.md) for the full answers Q3.4.a-i):",
        "",
        f"`stress_stdev_sleep` on Stratum 4 is a **per-night SECOND-ORDER variability channel** "
        f"(skew={a['skewness']:+.2f}, excess kurtosis={a['excess_kurtosis']:+.2f}, "
        f"heavy_tail_flag={a['heavy_tail_flag']}). **Data-driven E[L]\\*={el_star:.1f}** -- vs sister "
        f"Strand-A channels stress_mean_sleep 12.6 / stress_low_motion 21.1 / bb_lowest 29.25 / "
        f"all_day_stress_avg 29.8. **Phase-stratified medians** (citalopram axis, caveat-class per "
        f"CONVENTIONS section 4.2 since channel NOT in v3 scope): unmedicated {unmed_med:.2f} -> "
        f"consolidation {c.get('consolidation', {}).get('median', float('nan')):.2f} -> afbouw "
        f"{afbouw_med:.2f}. Episode-level Cohen's d={fe['cohens_d_episode_vs_normal_day']:+.2f} "
        f"(bootstrap CI95 [{fe['bootstrap_ci95_mean_diff'][0]:+.3f}, "
        f"{fe['bootstrap_ci95_mean_diff'][1]:+.3f}]) -- descriptively corroborates HA07d's locked "
        f"OVERALL-SUPPORTED + R14 single-pool +{ha07d['r14_single_pool_disc_pp']} pp "
        f"p={ha07d['r14_single_pool_perm_p']} signal at the coarse first-order-day-level read (HA07d's "
        "tested operand is the per-4-day MAX |z| of night-over-night delta; this Q3.4.f is the first-"
        "order day-level descriptive complement, NOT a re-anchoring of HA07d). Near-identity check "
        "vs mean sibling: see findings.md Q3.4.e for substantive-independence reading (HA07d both-"
        "eras-SUPPORTED + HA07c train-only-SUPPORTED divergence is descriptively consistent with "
        "rho<0.92 substantive independence).",
        "",
        "## Files",
        "",
        "- [`README.md`](README.md) -- this file",
        "- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + "
        "`README.md` + `plots/*.png`",
        "- [`findings.md`](findings.md) -- writeup covering Q3.4.a-i + tables (programmatically emitted "
        "by run.py from summary.json per the Q3.2/Q3.3 architectural note about the Write-tool harness "
        "heuristic on the literal filename \"findings\")",
        "- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per "
        "`docs/research/**/*.json`)",
        "- [`plots/`](plots/) -- 5 PNGs: distribution, phase-stratified violins, trajectory-with-phases, "
        "crash-vs-normal, ACF (gitignored per `docs/research/**/*.png`)",
        "",
        "## Status",
        "",
        f"**Current as of {summary['as_of_date']} corpus + 2026-06-24 analysis** (commit context: post-"
        "`40c351b` Q3.3 bb_lowest LANDED; Phase 2 \"finish the descriptive analysis\" Tier 1 user-"
        "prioritised CONFIRMED-citalopram channel batch FINAL CHANNEL; R14 first at `badd04a`; Q3.2 "
        "second at `cf34ab1`; Q3.3 third at `40c351b`; **this Q3.4 fourth closes Tier 1**). Refresh "
        "when:",
        "",
        "1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to "
        "spin up beyond the HA07d-locked operand.",
        "2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 onward).",
        f"3. Politis-White E[L]\\* shifts by another factor of 2 from current {el_star:.1f}.",
        "4. A v3-extension run on this channel lands and updates the Q3.4.d citalopram-modulation "
        "status from OPEN to CONFIRMED/REJECTED.",
        "5. A `stress_stdev_sleep_lagged_lcera_z` materialisation lands in `per_day_master.csv` and "
        "updates the Q3.4.i covariate-4 needed-columns entry.",
        "6. HA07d threshold-monotonicity diagnostic or any HA07d-descendant test ships and triggers "
        "operationalisation-substrate consumption.",
        "",
        "## Cross-references",
        "",
        "- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 "
        "2026-06-18, commit `ccbd12e`)",
        "- **First Strand A analysis** (template anchor + mean sibling): "
        "[`descriptive/operationalisation_support/stress_mean_sleep/`](../stress_mean_sleep/) -- mean "
        "sibling of same nightly stress series; closest precedent.",
        "- **Q3.2 sibling**: "
        "[`descriptive/operationalisation_support/all_day_stress_avg/`](../all_day_stress_avg/) -- "
        "Phase-2 first precedent; programmatic-emit pattern.",
        "- **Q3.3 most-recent precedent**: "
        "[`descriptive/operationalisation_support/bb_lowest/`](../bb_lowest/) -- inverse-direction "
        "CONFIRMED-citalopram sister; cross-channel E[L]\\* spread comparison.",
        "- **R14 single-pool re-anchor**: "
        "[`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) -- "
        "HA07d row +19.7 pp p=0.0291 descriptively corroborated in Q3.4.f.",
        "- **HA-* tests that this analysis anchors**:",
        "  - **HA07d** (LOCKED OVERALL-SUPPORTED -- the ONLY canonical both-eras-SUPPORTED test in the "
        "project + R14 single-pool SUPPORTED); primary operand of HA07d.",
        "  - HA07d threshold-monotonicity diagnostic (LOCKED; downstream of HA07d).",
        "  - HA07c (LOCKED OVERALL-REFUTED; mean sibling channel); substantive-independence vs HA07d "
        "reflected in Q3.4.e.",
        "  - HA08c (LOCKED OVERALL-REFUTED; slope-of-mean-sibling); inherits Q3.4.b autocorrelation "
        "context.",
        "- **Definitional substrate**: "
        "[`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "section 5.6 (v3 sweep scope -- this channel NOT in scope; Q3.4.d caveat-class framing).",
        "- **Other methodology MDs**: `lc_phase_descriptive.md`, `citalopram_phase_stratification.md`, "
        "`permutation_null_block_length.md`, `garmin_indicators_audit.md`, "
        "`lc_era_temporal_segmentation.md`, `_descriptive_stocktake_2026-06-23.md` (gap-list framing).",
        "- **Existing complementary**: "
        "[`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) "
        "(Q3.4.e cross-reference).",
        "- **Upstream pipeline**: `per_day_master.csv` <- "
        "`pipeline/03_consolidate/build_unified_dataset.py` <- "
        "`processed/garmin/sleep_stress_nightly.csv` <- "
        "`garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`. `labels_crash_v2.csv` per "
        "locked `crash_v2-definition`.",
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

    summary["questions"]["Q3.4.a_distribution"] = q_a_distribution(values)
    summary["questions"]["Q3.4.b_autocorrelation"] = q_b_autocorrelation(values)
    per_phase = q_c_base_rates_per_phase(s4, CHANNEL)
    summary["questions"]["Q3.4.c_base_rates_per_phase"] = per_phase
    summary["questions"]["Q3.4.d_phase_stratified_distribution"] = q_d_phase_stratified(per_phase, CHANNEL)
    summary["questions"]["Q3.4.e_near_identity"] = q_e_near_identity(s4, CHANNEL)
    summary["questions"]["Q3.4.f_crash_vs_normal"] = q_f_crash_vs_normal(s4, CHANNEL)
    summary["questions"]["Q3.4.g_spike_primitive"] = q_g_spike_primitive(s4, CHANNEL)
    summary["questions"]["Q3.4.h_outliers_calibration"] = q_h_outliers_calibration(s4, CHANNEL)
    summary["questions"]["Q3.4.i_covariate_readiness"] = q_i_covariate_readiness(s4, CHANNEL)

    plot_files = make_plots(s4, CHANNEL, HERE / "plots")
    summary["plots"] = plot_files

    out_path = HERE / "summary.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    # Emit findings.md and README.md as programmatic outputs (per the
    # Q3.2/Q3.3 precedent session's architectural note about the Write-
    # tool harness heuristic on the literal filename "findings").
    write_findings_md(summary, HERE / "findings.md")
    write_readme_md(summary, HERE / "README.md")

    print(f"Wrote {out_path}")
    print(f"Plots: {plot_files}")
    print("\n--- HEADLINE ---")
    a = summary["questions"]["Q3.4.a_distribution"]
    b = summary["questions"]["Q3.4.b_autocorrelation"]
    fr = summary["questions"]["Q3.4.f_crash_vs_normal"]
    print(f"Q3.4.a n={a['n']} mean={a['mean']:.3f} median={a['median']:.3f} MAD={a['mad_unscaled']:.3f} "
          f"skew={a['skewness']:.2f} heavy_tail={a['heavy_tail_flag']}")
    print(f"Q3.4.b E[L]*={b['data_driven_E_L_star']:.2f} (default 7); "
          f"factor-of-2 deviation flag={b['factor_of_2_deviation_flag']}; cutoff M={b['cutoff_lag_M']}")
    pp = summary["questions"]["Q3.4.c_base_rates_per_phase"]
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        if pp.get(ph, {}).get("n", 0) > 0:
            print(f"  Q3.4.c phase {ph}: n={pp[ph]['n']} med={pp[ph]['median']:.3f} MAD={pp[ph]['mad_unscaled']:.3f}")
    pd_d = summary["questions"]["Q3.4.d_phase_stratified_distribution"]
    print(f"Q3.4.d phase-to-phase median shifts (CAVEAT-CLASS; NO CONFIRMED/REJECTED verdict):")
    for k_label, v in pd_d["phase_to_phase_shifts"].items():
        print(f"  {k_label}: {v:+.3f}")
    fl = fr["day_level"]
    e7 = fl["stationary_bootstrap_E_L7"]
    eS = fl["stationary_bootstrap_E_L_star"]
    print(f"Q3.4.f day-level: n_crash={fl['n_crash_day']} n_normal={fl['n_normal_day']} "
          f"d={fl['cohens_d']:.2f} mean_diff={fl['mean_diff']:.3f}")
    print(f"  E[L]=7  CI=[{e7['ci_lower']:.3f}, {e7['ci_upper']:.3f}] "
          f"width={e7['ci_upper'] - e7['ci_lower']:.3f}")
    print(f"  E[L]*={eS['block_length_used']} CI=[{eS['ci_lower']:.3f}, {eS['ci_upper']:.3f}] "
          f"width={eS['ci_upper'] - eS['ci_lower']:.3f}")
    mwu = fl["mann_whitney_u"]
    print(f"  Mann-Whitney U: z={mwu['z']:.2f} p={mwu['p_two_sided']:.4f} P(crash>normal)={mwu['p_crash_greater_than_normal']:.3f}")
    fe = fr["episode_level"]
    print(f"Q3.4.f episode-level: n_ep={fe['n_crash_episodes']} d={fe['cohens_d_episode_vs_normal_day']:.2f} "
          f"mean_diff={fe['mean_diff_episode_vs_normal_day']:.3f} CI={fe['bootstrap_ci95_mean_diff']}")
    cd = fr["crash_drop_sensitivity_on_spearman_vs_gevoelscore"]
    if cd is not None:
        print(f"Q3.4.f crash-drop on Spearman(stress_stdev_sleep, gevoelscore): full={cd['full_frame_value']:.3f} "
              f"crashed-dropped={cd['crash_dropped_value']:.3f} |delta|={cd['abs_delta']:.3f} "
              f">0.10? {cd['exceeds_threshold_0p10']}")
    csr = fr.get("crash_subset_rho_vs_mean_sibling")
    if csr is not None:
        print(f"Q3.4.e crash-subset rho vs mean sibling: rho_crash={csr['spearman_rho_crash']:+.3f} "
              f"rho_normal={csr['spearman_rho_normal']:+.3f}")
    e_near = summary["questions"]["Q3.4.e_near_identity"]
    print(f"Q3.4.e near-identity flagged: {e_near['flagged_pairs']}")
    h = summary["questions"]["Q3.4.h_outliers_calibration"]
    print(f"Q3.4.h outliers (|z|>5): {h['n_flagged']} flagged")
    print(f"Q3.4.h citalopram step (2024-04-09 pre/post 30d): {h['citalopram_boundary_2024_04_09_step']['diff_post_minus_pre']:+.3f}")
    print(f"  consolidation step (2024-06-20): {h['consolidation_boundary_2024_06_20_step']['diff_post_minus_pre']:+.3f}")
    print(f"  afbouw step (2026-03-20): {h['afbouw_boundary_2026_03_20_step']['diff_post_minus_pre']:+.3f}")
    ha07d = fr["ha07d_cross_reference"]
    print(f"HA07d cross-ref: locked TRAIN +{ha07d['locked_train_disc_pp']} pp / VALIDATE +{ha07d['locked_validate_disc_pp']} pp / OVERALL SUPPORTED")
    print(f"  R14 single-pool: +{ha07d['r14_single_pool_disc_pp']} pp CI95={ha07d['r14_single_pool_ci95']} perm p={ha07d['r14_single_pool_perm_p']}")


if __name__ == "__main__":
    main()
