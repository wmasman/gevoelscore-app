"""Descriptive analysis: bb_overnight_gain operationalisation support.

Answers Q3.5.a-i + Q3.5.j (channel-specific coverage) per the locked
descriptive programme: ``docs/research/analyses/descriptive/README.md``
section 3.4 (HA-touched non-confirmed candidate list:
"bb_overnight_gain (HA10 primary) -- partially covered by
bb_overnight_gain_proxy.md"). This is the **first of the 5 Tier 2
channels** in the user-prioritised "finish the descriptive analysis"
Phase 2 batch (Tier 1 closed `39d7693`; Tier 2 sequential:
bb_overnight_gain first, then resting_hr, exertion_class,
push_burden_7d, gevoelscore).

Channel: SLEEPEND - SLEEPSTART recharge arc (BB overnight gain;
derived per pipeline/01_extract/garmin_uds_extras.py). HA10's
PRIMARY OPERAND in primitive form (HA10 itself tested bb_highest as
the morning BB peak proxy via UDS; bb_overnight_gain is the
sleep-recharge-arc Wiggers D2 channel).

Channel substantive status (per handoff section 1):
- HA10 primary operand surrogate; HA10 LOCKED OVERALL-REFUTED with
  era-directionality reversal (train -20.5 / validate +16.2 pp). Just
  R14-confirmed CONVERGE-ON-OVERALL at single-pool +4.1 pp
  [CI -16.5, +16.8] perm p=0.4328 -- direction-cancellation under
  single-pool FLATTENS the reversal (badd04a per single_pool_reanchor
  findings.md row HA10).
- NOT in v3 multi-channel sweep CONFIRMED set; v3 noted as "partial"
  per citalopram_dose_response_stress_mean_sleep.md section 5.6
  ("partial; no 2024 buildup data") -- the channel's truth start
  2024-09-18 is AFTER the citalopram buildup window 2024-04-09 to
  2024-06-19, so the v3 buildup dose-response slope cannot be
  computed on truth.

**Coverage constraint** (LOAD-BEARING for Q3.5.j + analytic window
choice per bb_overnight_gain_proxy.md):
- TRUTH (bb_overnight_gain) first non-null 2024-09-18 (Garmin UDS
  SLEEPEND rollout date); 593 / 1755 = 33.8% of LC corpus, but
  CONCENTRATED in consolidation + afbouw + post_afbouw phases.
- PROXY (bb_overnight_gain_proxy = HIGHEST - SLEEPSTART) first
  non-null 2024-07-08 (Garmin UDS SLEEPSTART rollout); validated
  r=0.989 / mean residual +0.63 vs truth on n=564 clean overlap
  days per bb_overnight_gain_proxy.md section 5.1.
- BEST (bb_overnight_gain_best) = truth where present, else proxy:
  667 / 1755 = 38.0% coverage; 74 proxy-source days = 71 bridge
  (2024-07-08 to 2024-09-17) + 3 post-rollout SLEEPEND failures
  (2025-04-26, 2025-08-24, 2025-12-11) per bb_overnight_gain_proxy.md
  section 5.4.
- The default Stratum-4 2022-09-03+ analytic window does NOT have
  full bb_overnight_gain coverage. Q3.5.j surfaces this; Q3.5.b ACF +
  Q3.5.c per-phase base rates + Q3.5.f crash-vs-normal all use the
  coverage-restricted window with explicit windowing choice.

Continuous-channel template (parity with sister bb_lowest Q3.3 +
sibling CONFIRMED-citalopram channels Q3.1 / Q3.2): standard Cohen's
d primary, no zero-rate column. The Q3.5.e near-identity check
rigorously tests vs sister bb_lowest (Q3.3 reported rho ~+0.19 NOT
near-identity; this Q3.5 reproduces from the gain-channel side).

Output: ``summary.json`` (machine-readable per-question results) +
``plots/*.png`` (visualisations) + ``findings.md`` + ``README.md``
(programmatically emitted from this script per the Q3.2 / Q3.3 / Q3.4
precedent session's architectural note about the Write-tool harness
heuristic on the literal filename "findings").

Discipline guards (per CONVENTIONS):
- section 2.1 descriptive-before-inference: no causal claims; no
  falsification bar; no HA verdict promotion (HA10 substantive
  verdict + R14 single-pool verdict LOCKED and NOT extended here).
- section 3.1 personal baseline: distribution shape is reported
  as-is; phase-stratified to surface the citalopram step where
  coverage permits.
- section 3.3 column-duplication: near-identity check at |rho|>=0.92.
- section 3.4 crash-drop sensitivity: |Delta|>0.10 flag surfaced.
- section 3.5 spike metrics: bb_overnight_gain is a within-night
  COMPOUND difference (SLEEPEND - SLEEPSTART), not a 24h mean and
  not a single extremum. The spike-vs-continuous discipline differs
  from both the stress-family and the bb_lowest NADIR channel.
- section 3.6 named counts: every count reports scheme + unit +
  source.
- section 4.1 + section 4.2: no a-priori claims; observed phase
  shift framed as descriptive observation only.
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
# HERE = .../analyses/descriptive/operationalisation_support/bb_overnight_gain
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


CHANNEL = "bb_overnight_gain"
AS_OF_DATE = "2026-06-05"  # parity with R14 + Q3.1 + Q3.2 + Q3.3 + Q3.4 prior Strand-A analyses

# Citalopram phase boundaries per
# methodology/citalopram_phase_stratification.md section 3
PHASE_BOUNDARIES = [
    ("unmedicated", date(2022, 9, 3), date(2024, 4, 8)),
    ("buildup", date(2024, 4, 9), date(2024, 6, 19)),
    ("consolidation", date(2024, 6, 20), date(2026, 3, 19)),
    ("afbouw", date(2026, 3, 20), date(2026, 6, 5)),
    # post_afbouw begins 2026-06-06; not in as-of cut
]

# Coverage boundary dates per bb_overnight_gain_proxy.md
TRUTH_START = date(2024, 9, 18)   # SLEEPEND rollout
PROXY_START = date(2024, 7, 8)    # SLEEPSTART rollout (proxy floor)


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
# Q3.5.a Distribution shape
# ---------------------------------------------------------------------------


def q_a_distribution(values: pd.Series) -> dict:
    """Distribution shape on the truth-available analytic window (Q3.5.a)."""
    v = values.dropna().astype(float)
    n = int(len(v))
    if n == 0:
        return {"n": 0, "note": "no non-NaN values in analytic window"}
    mean = float(v.mean())
    median = float(v.median())
    std = float(v.std(ddof=1))
    mad = float(np.median(np.abs(v - median)))
    quantiles = {f"p{q}": float(np.percentile(v, q)) for q in (1, 5, 10, 25, 50, 75, 90, 95, 99)}
    centered = v - mean
    m2 = float((centered ** 2).mean())
    m3 = float((centered ** 3).mean())
    skewness = m3 / (m2 ** 1.5) if m2 > 0 else float("nan")
    # bb_overnight_gain is a signed difference (can be negative; net drain
    # during sleep). Heavy-tail rule per CONVENTIONS section 3.1: skew>1 OR
    # p99/median > 3.0. For signed channels with median near zero, p99/median
    # can blow up or flip sign; we report both halves of the rule explicitly.
    abs_median = abs(median) if median != 0 else float("inf")
    p99_over_abs_median = quantiles["p99"] / abs_median if abs_median > 0 else float("nan")
    heavy_tail = bool((abs(skewness) > 1.0) or (p99_over_abs_median > 3.0))
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
        "p99_over_abs_median": p99_over_abs_median,
        "min": float(v.min()),
        "max": float(v.max()),
        "share_negative": float((v < 0).mean()),
    }


# ---------------------------------------------------------------------------
# Q3.5.b Autocorrelation + E[L]*
# ---------------------------------------------------------------------------


def q_b_autocorrelation(values: pd.Series) -> dict:
    """Autocorrelation structure + E[L]* on truth-available window (Q3.5.b)."""
    arr = values.dropna().to_numpy()
    if len(arr) < 30:
        return {
            "n_non_nan": int(len(arr)),
            "default_E_L": 7,
            "data_driven_E_L_star": float(7),
            "cutoff_lag_M": None,
            "factor_of_2_deviation_flag": False,
            "deviation_ratio": 0.0,
            "politis_white_significance_threshold_2sigma": float("nan"),
            "note": "n<30 in analytic window; returning project default E[L]=7",
            "selected_acf_lags": {},
        }
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
# Q3.5.c Base rates per phase
# ---------------------------------------------------------------------------


def q_c_base_rates_per_phase(df: pd.DataFrame, channel: str) -> dict:
    """Per-phase n + median + dispersion (Q3.5.c)."""
    out = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))
        sub = df.loc[mask, channel].dropna().astype(float)
        n_window = int(mask.sum())
        if len(sub) == 0:
            out[phase_name] = {
                "n": 0,
                "n_days_in_window": n_window,
                "date_start": str(start),
                "date_end": str(end),
                "note": "no non-NaN values in this phase window (channel coverage gap)",
            }
            continue
        med = float(sub.median())
        out[phase_name] = {
            "n": int(len(sub)),
            "n_days_in_window": n_window,
            "coverage_pct": round(100.0 * len(sub) / n_window, 2) if n_window > 0 else None,
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
# Q3.5.d Phase-stratified distribution -- caveat-class observation
# ---------------------------------------------------------------------------


def q_d_phase_stratified(per_phase: dict, channel: str) -> dict:
    """Phase-stratified distribution + descriptive shift report (Q3.5.d).

    HA10 R14 single-pool re-anchor (badd04a) cross-reference: era-
    directionality reversal -20.5/+16.2 flattens to +4.1 pp under
    single-pool. The per-citalopram-phase trajectory reported here is
    the operationalisation-support layer; whether the per-phase signal
    carries the era-directionality flattening is the descriptive
    cross-reference, NOT a re-interpretation of HA10's locked verdict.
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
        "channel_in_v3_six_channel_scope": True,
        "v3_verdict": "partial; no 2024 buildup data",
        "v3_source": "methodology/citalopram_dose_response_stress_mean_sleep.md v3 section 5.6",
        "framing": (
            "bb_overnight_gain is in the v3 multi-channel scope but flagged "
            "'partial' because the channel's truth coverage starts 2024-09-18 "
            "(SLEEPEND UDS rollout) -- AFTER the citalopram buildup window "
            "2024-04-09 -> 2024-06-19. The buildup dose-response slope CANNOT "
            "be computed on truth. Observed phase-shift below is a Layer 1 "
            "descriptive observation per CONVENTIONS section 4.2 (caveats "
            "yes, a-priori claims no); the citalopram-dose-modulation status "
            "remains effectively OPEN for the buildup phase on this channel."
        ),
    }

    out["ha10_r14_cross_reference"] = {
        "ha10_locked_verdict": (
            "TRAIN REFUTED (-20.5) / VALIDATE SUPPORTED (+16.2) / OVERALL "
            "REFUTED; era-directionality reversal (train 100% lowered, "
            "validate 69% elevated)"
        ),
        "ha10_primary_operand": "max |z| (4d, bidirectional) of bb_highest (morning BB peak proxy via UDS); lagged baseline; sigma_floor=2.0 BB points",
        "ha10_relation_to_this_channel": (
            "HA10's primary uses bb_highest (peak proxy) NOT bb_overnight_gain "
            "directly. bb_overnight_gain is HA10's Wiggers D2 sleep-recharge-"
            "arc operand in its primitive form; HA10's tested operand was the "
            "morning peak as a sleep-recharge marker. The two are related but "
            "operationally distinct (Q3.5.e + Q3.5.k below)."
        ),
        "r14_single_pool_disc_pp": +4.1,
        "r14_single_pool_ci95": [-16.5, +16.8],
        "r14_single_pool_perm_p": 0.4328,
        "r14_single_pool_verdict": "NOT-SUPPORTED CONVERGE-ON-OVERALL (locked OVERALL-REFUTED + single-pool NOT-SUPPORTED)",
        "r14_source": "descriptive/operationalisation_support/single_pool_reanchor/findings.md row HA10",
        "ha_source": "analyses/hypotheses/HA10-bb-overnight-recharge/result.md",
        "descriptive_corroboration_framing": (
            "If per-citalopram-phase medians on bb_overnight_gain show a "
            "smoothly graded trajectory (rather than an era-step), that is "
            "descriptively consistent with the R14 single-pool flattening "
            "reading: the train/validate split happens to straddle the "
            "unmedicated-to-citalopram-buildup boundary (2024-04-09), so the "
            "era-directionality reversal can read as a per-citalopram-state "
            "effect rather than a true per-era effect. This Q3.5.d "
            "observation is NOT a re-interpretation of either the locked "
            "HA10 verdict or the R14 single-pool verdict."
        ),
    }
    return out


# ---------------------------------------------------------------------------
# Q3.5.e Near-identity check
# ---------------------------------------------------------------------------

NEAR_IDENTITY_THRESHOLD = 0.92  # CONVENTIONS section 3.3


def q_e_near_identity(df: pd.DataFrame, channel: str) -> dict:
    """Near-identity check vs sister BB channels + neighbours (Q3.5.e).

    Per handoff section 2.4: load-bearing reproduction of Q3.3 bb_lowest
    sister-channel cross-pair (Q3.3 reported rho ~+0.19 NOT near-
    identity per Q3.3 section 3.3.k); this Q3.5.e reproduces from the
    bb_overnight_gain side at the truth-only window AND extends with
    multiple resolutions (raw daily / rolling-7d / rolling-30d) to
    cover the handoff's "extended at multiple aggregation resolutions"
    requirement.

    Targets:
      - bb_lowest (sister Q3.3; ~+0.19 reciprocally)
      - bb_highest (HA10 actual primary; peak-pair complement)
      - bb_sleep_start_value, bb_sleep_end_value (SLEEPEND - SLEEPSTART
        decomposition; bb_sleep_end_value SHOULD be near-identity by
        construction over the truth window)
      - bb_during_sleep_value (sleep-window-averaged BB)
      - Sister stress + cardio channels: stress_mean_sleep,
        all_day_stress_avg, resting_hr
    """
    targets = [
        # Brief-mandated per handoff section 2.4 (sister Q3.3 + HA10 peak)
        "bb_lowest",
        "bb_highest",
        # BB-family construction inputs / neighbours
        "bb_sleep_start_value",
        "bb_sleep_end_value",
        "bb_during_sleep_value",
        "bb_overnight_gain_proxy",
        "bb_overnight_gain_best",
        # Cross-family stress companions (CONFIRMED-citalopram set)
        "stress_mean_sleep",
        "all_day_stress_avg",
        "stress_stdev_sleep",
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

    # Multi-resolution extension for bb_lowest pair per handoff section 2.4
    bb_lowest_multires = None
    if "bb_lowest" in df.columns:
        pair = df[["date", channel, "bb_lowest"]].dropna(
            subset=[channel, "bb_lowest"]
        ).sort_values("date").reset_index(drop=True)
        if len(pair) > 30:
            raw_pear = float(pair[channel].corr(pair["bb_lowest"]))
            raw_spear = float(pair[channel].corr(pair["bb_lowest"], method="spearman"))
            # Rolling-7d means
            pair["bog_7d"] = pair[channel].rolling(7, min_periods=5).mean()
            pair["lo_7d"] = pair["bb_lowest"].rolling(7, min_periods=5).mean()
            roll7 = pair[["bog_7d", "lo_7d"]].dropna()
            roll7_pear = float(roll7["bog_7d"].corr(roll7["lo_7d"])) if len(roll7) > 30 else None
            roll7_spear = (
                float(roll7["bog_7d"].corr(roll7["lo_7d"], method="spearman"))
                if len(roll7) > 30 else None
            )
            # Rolling-30d means
            pair["bog_30d"] = pair[channel].rolling(30, min_periods=20).mean()
            pair["lo_30d"] = pair["bb_lowest"].rolling(30, min_periods=20).mean()
            roll30 = pair[["bog_30d", "lo_30d"]].dropna()
            roll30_pear = float(roll30["bog_30d"].corr(roll30["lo_30d"])) if len(roll30) > 30 else None
            roll30_spear = (
                float(roll30["bog_30d"].corr(roll30["lo_30d"], method="spearman"))
                if len(roll30) > 30 else None
            )
            bb_lowest_multires = {
                "n_overlap_days": int(len(pair)),
                "raw_daily": {
                    "pearson_r": raw_pear, "spearman_rho": raw_spear,
                    "n": int(len(pair)),
                },
                "rolling_7d_mean": {
                    "pearson_r": roll7_pear, "spearman_rho": roll7_spear,
                    "n": int(len(roll7)),
                },
                "rolling_30d_mean": {
                    "pearson_r": roll30_pear, "spearman_rho": roll30_spear,
                    "n": int(len(roll30)),
                },
                "q33_reported_rho_with_this_channel": +0.19,
                "q33_source": "descriptive/operationalisation_support/bb_lowest/ Q3.3.k bb_lowest <-> bb_overnight_gain pair table",
                "note": (
                    "Multi-resolution extension per handoff section 2.4: raw "
                    "daily / 7d-rolling-mean / 30d-rolling-mean rho values "
                    "characterise whether the bb_lowest <-> bb_overnight_gain "
                    "relationship strengthens at coarser temporal resolutions "
                    "(shared trajectory absorption) or stays weak (operationally "
                    "distinct floor-vs-gain primitives). Q3.3 sister analysis "
                    "reported the raw rho ~+0.19 NOT near-identity verdict."
                ),
            }

    return {
        "threshold": NEAR_IDENTITY_THRESHOLD,
        "rows": rows,
        "flagged_pairs": flags,
        "bb_lowest_multires_extension": bb_lowest_multires,
        "note": (
            "Sister bb_lowest Q3.3 reported Pearson r / Spearman rho ~+0.19 "
            "vs this channel (NOT near-identity at the section 3.3 threshold). "
            "This Q3.5.e reproduces from the gain side + extends with multi-"
            "resolution rho per handoff section 2.4. Note: bb_overnight_gain "
            "near-identity with bb_sleep_end_value is EXPECTED by construction "
            "(gain = SLEEPEND - SLEEPSTART, so gain is a strong function of "
            "SLEEPEND on the truth window) -- the high rho there is a "
            "definitional artefact, not a substantive collinearity finding."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.5.f Crash-day vs normal-day on truth-available window
# ---------------------------------------------------------------------------


def _mann_whitney_u(crash_vals: np.ndarray, normal_vals: np.ndarray) -> dict:
    """Compute Mann-Whitney U with normal approximation + tie correction."""
    n_c = len(crash_vals)
    n_n = len(normal_vals)
    if n_c < 1 or n_n < 1:
        return {
            "U_crash_first_sample": float("nan"),
            "z": float("nan"),
            "p_two_sided": float("nan"),
            "p_crash_greater_than_normal": float("nan"),
            "median_diff": float("nan"),
        }
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
    sensitivity (Q3.5.f). Window-restricted to truth-available days.
    """
    sub = df[[channel, "is_crash", "episode_id"]].dropna(subset=[channel, "is_crash"])
    is_crash = sub["is_crash"].astype(bool)
    crash_vals = sub.loc[is_crash, channel].astype(float)
    normal_vals = sub.loc[~is_crash, channel].astype(float)

    n_crash_day = int(len(crash_vals))
    n_normal_day = int(len(normal_vals))

    if n_crash_day < 2 or n_normal_day < 2:
        return {
            "note": "insufficient n_crash or n_normal in analytic window",
            "n_crash_day": n_crash_day,
            "n_normal_day": n_normal_day,
        }

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

    def _safe_bootstrap_ci(boot_result):
        """Re-compute CI quantiles ignoring NaN bootstrap stats."""
        dist = boot_result.get("bootstrap_distribution")
        if dist is None:
            return boot_result
        finite_mask = np.isfinite(dist)
        n_valid = int(finite_mask.sum())
        if n_valid < 100:
            return {
                **boot_result,
                "ci_lower_nanfiltered": float("nan"),
                "ci_upper_nanfiltered": float("nan"),
                "n_valid_bootstrap_samples": n_valid,
                "fallback_note": "fewer than 100 finite bootstrap samples; CI suppressed",
            }
        finite_dist = dist[finite_mask]
        return {
            **boot_result,
            "ci_lower_nanfiltered": float(np.quantile(finite_dist, 0.025)),
            "ci_upper_nanfiltered": float(np.quantile(finite_dist, 0.975)),
            "n_valid_bootstrap_samples": n_valid,
        }

    boot_day_E7 = _safe_bootstrap_ci(stationary_bootstrap_ci(
        aligned, day_mean_diff,
        n_bootstrap=5000, expected_block_length=7,
        confidence_level=0.95, random_state=seed,
    ))
    boot_day_Estar = _safe_bootstrap_ci(stationary_bootstrap_ci(
        aligned, day_mean_diff,
        n_bootstrap=5000, expected_block_length=el_star,
        confidence_level=0.95, random_state=seed,
    ))

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
                "ci_lower": float(boot_day_E7.get("ci_lower_nanfiltered", boot_day_E7["ci_lower"])),
                "ci_upper": float(boot_day_E7.get("ci_upper_nanfiltered", boot_day_E7["ci_upper"])),
                "n_valid_bootstrap_samples": int(boot_day_E7.get("n_valid_bootstrap_samples", 0)),
                "note": (
                    "project default per permutation_null_block_length.md. "
                    "Bootstrap stats NaN-filtered: resamples without crash-day "
                    "rows return NaN for the crash-vs-normal mean diff; only "
                    "finite samples enter the quantile."
                ),
            },
            "stationary_bootstrap_E_L_star": {
                "block_length_used": el_star,
                "point_estimate": float(boot_day_Estar["point_estimate"]),
                "ci_lower": float(boot_day_Estar.get("ci_lower_nanfiltered", boot_day_Estar["ci_lower"])),
                "ci_upper": float(boot_day_Estar.get("ci_upper_nanfiltered", boot_day_Estar["ci_upper"])),
                "n_valid_bootstrap_samples": int(boot_day_Estar.get("n_valid_bootstrap_samples", 0)),
                "note": "data-driven from Q3.5.b; rounded to nearest integer; NaN-filtered like E[L]=7",
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
        "window_caveat": (
            "Q3.5.f computed on the truth-available analytic window only "
            "(2024-09-18+); n_crash_day is therefore much smaller than the "
            "sister CONFIRMED-citalopram analyses that ran on full Stratum "
            "4. The bootstrap CI width reflects the smaller n; the point "
            "estimate is on the truth window only."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.5.g Spike-detecting primitive availability
# ---------------------------------------------------------------------------


def q_g_spike_primitive(df: pd.DataFrame, channel: str) -> dict:
    """Spike-primitive availability for bb_overnight_gain (Q3.5.g)."""
    out = {
        "channel_resolution": "per-night SLEEPEND - SLEEPSTART (BB recharge arc; derived per pipeline/01_extract/garmin_uds_extras.py from UDS bodyBatteryStatList)",
        "spike_or_continuous_form": (
            "COMPOUND-DIFFERENCE primitive (signed sleep-window delta; not a "
            "24h mean, not a single extremum; the per-night recharge arc as "
            "a one-shot signed magnitude)"
        ),
        "sub_daily_resolution_in_master": False,
        "spike_primitives_available_in_master": [],
        "latent_in_FIT_not_in_master": [
            "per-minute body-battery samples (NOT in GDPR dump per bb_overnight_gain_proxy.md section 6 caveat 5: 'No per-minute BB anywhere in the dump' as of 2026-06-14)",
            "within-sleep BB trajectory (would allow sleep-stage-aligned BB-recovery slope extraction; not extractable)",
        ],
        "related_daily_bb_metrics_in_master": [],
        "note": (
            "Per CONVENTIONS section 3.5 sympathetic-arousal proxies prefer "
            "spike/peak/count metrics over daily means; bb_overnight_gain is "
            "neither -- it is a compound signed difference on a discrete "
            "sleep-window-bracketed delta. The spike-form analogue at the "
            "BB-recharge construct would be 'count of nights with recharge "
            "below threshold X' or 'shortest recharge in 7d window'; neither "
            "is currently in per_day_master. HA10's tested operand (max |z| "
            "(4d, bidirectional) of bb_highest with lagged baseline) is a "
            "spike-form construct on the peak proxy; the analogous "
            "construct on bb_overnight_gain itself is the within-4-day "
            "max |z| of night-over-night DELTA (not in master)."
        ),
    }
    for c in (
        "bb_highest",
        "bb_lowest",
        "bb_sleep_start_value",
        "bb_sleep_end_value",
        "bb_during_sleep_value",
        "bb_charged_24h",
        "bb_drained_24h",
        "bb_overnight_gain_proxy",
        "bb_overnight_gain_best",
    ):
        if c in df.columns:
            n = int(df[c].notna().sum())
            out["spike_primitives_available_in_master"].append({"column": c, "n_non_nan": n})
    for partner in ("bb_highest", "bb_lowest", "bb_sleep_start_value", "bb_sleep_end_value", "bb_during_sleep_value", "bb_overnight_gain_best", "bb_overnight_gain_proxy"):
        if partner in df.columns:
            d = df[[channel, partner]].dropna()
            if len(d) > 30:
                out[f"pearson_r_vs_{partner}"] = float(d.corr().iloc[0, 1])
                out[f"spearman_rho_vs_{partner}"] = float(d.corr(method="spearman").iloc[0, 1])
                out[f"n_pair_{partner}"] = int(len(d))
    return out


# ---------------------------------------------------------------------------
# Q3.5.h Outlier detection + calibration-drift check
# ---------------------------------------------------------------------------


def q_h_outliers_calibration(df: pd.DataFrame, channel: str) -> dict:
    """Outlier detection + calibration-drift check (Q3.5.h).

    Cross-references garmin_indicators_audit.md known-issues +
    LOAD-BEARING bb_overnight_gain_proxy.md coverage-bridge framing.
    """
    sub = df[["date", channel]].dropna().sort_values("date").reset_index(drop=True)
    v = sub[channel].astype(float)
    if len(v) == 0:
        return {"note": "no non-NaN values in analytic window"}
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
    # Snapshot dates restricted to truth-available window (2024-09-18+)
    snapshot_dates = [
        "2024-12-01", "2025-03-01", "2025-06-01",
        "2025-09-01", "2025-12-01", "2026-04-01",
    ]
    snaps = []
    for s in snapshot_dates:
        t = pd.Timestamp(s)
        if len(sub) == 0:
            continue
        idx = (sub["date"] - t).abs().idxmin()
        row = sub.loc[idx]
        snaps.append({
            "snapshot_date": s,
            "actual_date": str(row["date"].date()),
            "rolling_med_90d": (
                None if pd.isna(row["rolling_med_90d"]) else float(row["rolling_med_90d"])
            ),
        })

    # Boundary steps: consolidation start 2024-06-20 is BEFORE truth start
    # (2024-09-18) -- cannot compute pre/post 30d on truth. Only afbouw
    # boundary 2026-03-20 is fully bracketed by truth coverage. Report
    # what's computable and explicitly flag what isn't.
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
            "note": (
                "BLOCKED by coverage: citalopram buildup boundary 2024-04-09 "
                "is BEFORE truth start 2024-09-18 AND BEFORE proxy start "
                "2024-07-08. Pre/post 30d means uncomputable on this channel. "
                "Q3.5.j has the load-bearing coverage analysis."
            ),
        },
        "consolidation_boundary_2024_06_20_step": {
            "pre_30d_mean": float(pre30_c) if pre30_c == pre30_c else None,
            "post_30d_mean": float(post30_c) if post30_c == post30_c else None,
            "diff_post_minus_pre": (
                float(post30_c - pre30_c) if (pre30_c == pre30_c and post30_c == post30_c) else None
            ),
            "note": (
                "PARTIAL: consolidation start 2024-06-20 is BEFORE truth "
                "start 2024-09-18; pre-30d window is fully outside truth "
                "coverage. Post-30d also outside (truth begins 2024-09-18). "
                "Computed values are NaN unless the analytic frame includes "
                "the proxy channel (bb_overnight_gain_best) -- this q3.5.h "
                "runs on truth bb_overnight_gain only per discipline anchor."
            ),
        },
        "afbouw_boundary_2026_03_20_step": {
            "pre_30d_mean": float(pre30_a) if pre30_a == pre30_a else None,
            "post_30d_mean": float(post30_a) if post30_a == post30_a else None,
            "diff_post_minus_pre": (
                float(post30_a - pre30_a) if (pre30_a == pre30_a and post30_a == post30_a) else None
            ),
            "note": (
                "afbouw boundary is fully bracketed by truth coverage; "
                "the pre/post means are the empirical 30d step on this "
                "channel at the afbouw onset."
            ),
        },
        "garmin_indicators_audit_known_issues": [
            (
                "bb_overnight_gain is derived from daily_uds.csv (BB family "
                "JSON-side passthrough); the SLEEPSTART + SLEEPEND inputs were "
                "added to Garmin's UDS export in two stages on this FR245: "
                "SLEEPSTART first emitted 2024-07-08; SLEEPEND first emitted "
                "2024-09-18. Pre-rollout days are structurally NaN, NOT a "
                "project-side pipeline gap"
            ),
            (
                "Underlying sensor is Forerunner 245 Elevate V3 throughout the "
                "entire 2021-08-16 to present window -- no device change; per "
                "bb_overnight_gain_proxy.md section 6 caveat 1 the single-watch / "
                "single-firmware-family validation extends to BB-family columns"
            ),
            (
                "3 post-rollout SLEEPEND-failure nights (2025-04-26, 2025-08-24, "
                "2025-12-11) where Garmin emitted SLEEPSTART + HIGHEST but did "
                "not compute SLEEPEND; these are NaN on truth but rescued by "
                "the bb_overnight_gain_best fused channel per bb_overnight_gain_"
                "proxy.md section 5.4"
            ),
            (
                "Saturation: when bb_highest == 100 the proxy floors; 29 / 593 "
                "post-2024-09-18 days were saturated; sensitivity-conscious "
                "analyses can flag and exclude these per bb_overnight_gain_"
                "proxy.md section 4 discipline rule 3"
            ),
        ],
    }


# ---------------------------------------------------------------------------
# Q3.5.i Covariate-sensitivity readiness
# ---------------------------------------------------------------------------


def q_i_covariate_readiness(df: pd.DataFrame, channel: str) -> dict:
    """Covariate-sensitivity readiness (Q3.5.i).

    Per HA-P7 section 4.5.4 worked-example pattern. Names candidate
    covariates a future HA on bb_overnight_gain as predictor could add.
    """
    cands = []
    # 1. bb_lowest -- floor companion (HA-C4b sibling)
    floor_corr = None
    if "bb_lowest" in df.columns:
        d = df[[channel, "bb_lowest"]].dropna()
        if len(d) > 30:
            floor_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "bb_lowest (BB-floor companion; Q3.3 sister analysis)",
        "rationale": (
            "bb_overnight_gain is the recharge arc (SLEEPEND - SLEEPSTART); "
            "bb_lowest is the daily NADIR. Q3.3 reported rho ~+0.19 NOT "
            "near-identity -- the floor depth and the recharge magnitude "
            "carry distinct information (a deep-floor night with strong "
            "recharge vs a shallow-floor night with weak recharge). The "
            "covariate disambiguates: is the bb_overnight_gain signal driven "
            "by the recharge magnitude specifically (beta_channel survives) "
            "or by the depleted-state floor (beta_channel attenuates -- "
            "bb_lowest was carrying the load)."
        ),
        "source": "Q3.3 bb_lowest findings.md section 3.3.k bb_overnight_gain pair table",
        "observed_correlation_on_S4_truth_window": floor_corr,
        "expected_effect": (
            "beta_channel attenuates if the BB-floor depth is the load-"
            "bearing primitive; beta_channel survives if the recharge "
            "magnitude carries independent information"
        ),
    })
    # 2. dose_plasma_mg(d) -- citalopram covariate (channel "partial" in v3)
    cands.append({
        "covariate": "dose_plasma_mg(d) (citalopram covariate -- 'partial' in v3 scope)",
        "rationale": (
            "bb_overnight_gain is in v3 multi-channel scope but flagged "
            "'partial' per citalopram_dose_response_stress_mean_sleep.md "
            "section 5.6 because the buildup window 2024-04-09 -> 2024-06-19 "
            "is BEFORE truth coverage (2024-09-18+) -- the buildup dose-"
            "response slope cannot be computed on truth. A future HA on this "
            "channel cross-phase should pre-spec dose as a secondary "
            "covariate on the consolidation + afbouw + post_afbouw phases "
            "where truth coverage exists; the unmedicated baseline is "
            "ABSENT on truth (the unmedicated phase ends 2024-04-08, well "
            "before truth start)."
        ),
        "source": "methodology/citalopram_dose_response_stress_mean_sleep.md v3 section 5.6 ('partial; no 2024 buildup data'); CONVENTIONS section 4.2",
        "expected_effect": (
            "beta_dose carries any latent dose-modulation signal; beta_channel "
            "attenuates if the signal is dose-driven; beta_channel survives "
            "if independent recharge-mechanism signal"
        ),
        "needed_columns_in_master": ["lc_phase (in master) or runtime dose_plasma_mg(d) computation"],
    })
    # 3. bb_highest -- HA10's actual primary (peak companion)
    peak_corr = None
    if "bb_highest" in df.columns:
        d = df[[channel, "bb_highest"]].dropna()
        if len(d) > 30:
            peak_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "bb_highest (HA10's actual primary)",
        "rationale": (
            "HA10's tested operand uses bb_highest (morning BB peak proxy) "
            "as the sleep-recharge marker, not bb_overnight_gain directly. "
            "The covariate disambiguates: is the recharge-arc signal "
            "(SLEEPEND - SLEEPSTART) carrying information beyond the "
            "morning peak that HA10 actually tested? If beta_channel "
            "attenuates under bb_highest covariate, the recharge arc is "
            "a function of the peak; if beta_channel survives, the arc "
            "carries the recharge MAGNITUDE distinct from the morning "
            "peak LEVEL."
        ),
        "source": "HA10 result.md operand specification",
        "observed_correlation_on_S4_truth_window": peak_corr,
        "expected_effect": (
            "beta_channel attenuates if peak-level dominates; beta_channel "
            "survives if recharge-magnitude carries independent information"
        ),
    })
    # 4. own-lagged trailing-mean -- autocorrelation-vs-mechanism (HA-P7 section 4.5.4)
    cands.append({
        "covariate": "bb_overnight_gain_lagged_mean_Nd(d) = mean(channel[d-N:d-1]) with N tuned to Q3.5.b E[L]* + margin",
        "rationale": (
            "Mirrors HA-P7 section 4.5.4 worked example (lagged-outcome "
            "covariate) for the autocorrelation-vs-mechanism disambiguation. "
            "Per Q3.5.b the cutoff lag M and data-driven E[L]* on the truth-"
            "available window are inputs to this choice. NOTE: per_day_master "
            "ALREADY has a materialised bb_overnight_gain_lagged_lcera_z "
            "column (LC-era-only [d-90, d-30] trailing baseline per CONVENTIONS "
            "section 3.2 _lagged_lcera convention); HA author can use that "
            "directly OR compute a shorter window."
        ),
        "source": "HA-P7 hypothesis.md section 4.5.4; per_day_master.csv bb_overnight_gain_lagged_lcera_z column",
        "expected_effect": (
            "beta_channel collapses if today's bb_overnight_gain is just "
            "yesterday's value carried forward; beta_channel survives if "
            "the signal carries new-day information"
        ),
        "needed_columns_in_master": [
            "bb_overnight_gain_lagged_lcera_z (already in master per CONVENTIONS section 3.2)"
        ],
    })
    return {
        "primary_use_case": (
            "Future HA pre-reg using bb_overnight_gain as predictor of a "
            "crash-related outcome (the Wiggers D2 direct test would use this "
            "channel as primary; HA10 used the peak-proxy form). Coverage "
            "constraint per bb_overnight_gain_proxy.md MUST be applied: any "
            "test using this channel as primary is restricted to truth-"
            "available days (2024-09-18+) OR must use bb_overnight_gain_best "
            "with proxy-share disclosure per the proxy MD discipline rules."
        ),
        "discipline_anchor": "HA-P7 hypothesis.md section 4.5.4 -- secondary-logistic-with-covariate pattern",
        "candidate_covariates": cands,
        "recommendation": (
            "Pre-spec all four covariates as secondary sensitivity arms. The "
            "bb_lowest arm (covariate 1) operationalises the Q3.3 floor-vs-"
            "arc construct disambiguation. The dose arm (covariate 2) is "
            "diagnostic-only at this time per the channel's 'partial' v3 "
            "scope. The bb_highest arm (covariate 3) is the load-bearing "
            "peak-vs-arc disambiguator (HA10 tested the peak; a follow-up "
            "HA on the arc should pre-spec the peak as a secondary covariate "
            "to surface what the arc adds). The autocorrelation arm "
            "(covariate 4) operationalises HA-P7 section 4.5.4 on this "
            "channel using the already-materialised _lagged_lcera_z variant."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.5.j (channel-specific) -- LOAD-BEARING coverage analysis
# ---------------------------------------------------------------------------


def q_j_coverage(df_full: pd.DataFrame, df_s4: pd.DataFrame, channel: str) -> dict:
    """LOAD-BEARING coverage analysis (Q3.5.j) per handoff section 2.4.

    Surfaces the bb_overnight_gain_proxy.md framing explicitly + justifies
    the analytic window choice for Q3.5.b ACF + Q3.5.c per-phase + Q3.5.f
    crash-vs-normal.
    """
    # Truth channel coverage
    truth_mask = df_full[channel].notna()
    truth_first = df_full.loc[truth_mask, "date"].min()
    truth_last = df_full.loc[truth_mask, "date"].max()
    n_truth = int(truth_mask.sum())
    n_total_full = int(len(df_full))

    # Proxy channel coverage
    proxy_info = None
    if "bb_overnight_gain_proxy" in df_full.columns:
        proxy_mask = df_full["bb_overnight_gain_proxy"].notna()
        proxy_first = df_full.loc[proxy_mask, "date"].min()
        proxy_info = {
            "first_non_nan": str(proxy_first.date()) if pd.notna(proxy_first) else None,
            "n_non_nan_full_corpus": int(proxy_mask.sum()),
            "share_of_corpus_pct": round(100.0 * proxy_mask.sum() / n_total_full, 2),
        }

    # Best (fused) coverage
    best_info = None
    if "bb_overnight_gain_best" in df_full.columns:
        best_mask = df_full["bb_overnight_gain_best"].notna()
        best_first = df_full.loc[best_mask, "date"].min()
        best_info = {
            "first_non_nan": str(best_first.date()) if pd.notna(best_first) else None,
            "n_non_nan_full_corpus": int(best_mask.sum()),
            "share_of_corpus_pct": round(100.0 * best_mask.sum() / n_total_full, 2),
        }

    # Source provenance breakdown
    source_breakdown = None
    if "bb_overnight_gain_source" in df_full.columns:
        src = df_full["bb_overnight_gain_source"].astype(str).fillna("")
        source_breakdown = {
            "truth_rows": int((src == "truth").sum()),
            "proxy_rows": int((src == "proxy").sum()),
            "empty_rows": int((src == "").sum()),
        }

    # Per-phase coverage on Stratum 4 (3-way: truth vs best vs S4-window)
    per_phase = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (df_s4["date"] >= pd.Timestamp(start)) & (df_s4["date"] <= pd.Timestamp(end))
        n_days = int(mask.sum())
        n_truth_ph = int(df_s4.loc[mask, channel].notna().sum())
        n_best_ph = (
            int(df_s4.loc[mask, "bb_overnight_gain_best"].notna().sum())
            if "bb_overnight_gain_best" in df_s4.columns else None
        )
        per_phase[phase_name] = {
            "n_days_in_window": n_days,
            "n_with_truth": n_truth_ph,
            "n_with_best": n_best_ph,
            "truth_coverage_pct": round(100.0 * n_truth_ph / n_days, 2) if n_days > 0 else None,
            "best_coverage_pct": (
                round(100.0 * n_best_ph / n_days, 2)
                if n_days > 0 and n_best_ph is not None else None
            ),
        }

    return {
        "discipline_anchor": "methodology/bb_overnight_gain_proxy.md (LOAD-BEARING)",
        "truth_channel": {
            "name": channel,
            "first_non_nan_date_full_corpus": str(truth_first.date()) if pd.notna(truth_first) else None,
            "last_non_nan_date_full_corpus": str(truth_last.date()) if pd.notna(truth_last) else None,
            "n_non_nan_full_corpus": n_truth,
            "share_of_full_corpus_pct": round(100.0 * n_truth / n_total_full, 2),
            "underlying_garmin_uds_rollout": "SLEEPEND first emitted 2024-09-18 on this FR245 (verified Session D 2026-06-14 by direct GDPR-dump inspection per bb_overnight_gain_proxy.md section 1)",
        },
        "proxy_channel": {
            "name": "bb_overnight_gain_proxy",
            "construction": "bb_highest - bb_sleep_start_value (per bb_overnight_gain_proxy.md section 2)",
            "underlying_garmin_uds_rollout": "SLEEPSTART first emitted 2024-07-08 on this FR245 (proxy floor)",
            "validation_summary": (
                "n=564 clean overlap days post-2024-09-18: Pearson r=0.9886; "
                "mean residual +0.63 BB units; median residual 0; MAE 0.63; "
                "share within +/-5 BB units = 97.5%; HIGHEST median timestamp "
                "06:00 local with 96.3% within +/-2h of SLEEPEND per "
                "bb_overnight_gain_proxy.md section 5.1 + 5.2"
            ),
            "info": proxy_info,
        },
        "best_fused_channel": {
            "name": "bb_overnight_gain_best",
            "construction": "truth where present, else proxy (per bb_overnight_gain_proxy.md section 2)",
            "info": best_info,
            "audit_companion": "bb_overnight_gain_source (truth/proxy/empty enum)",
        },
        "source_provenance_breakdown_full_corpus": source_breakdown,
        "per_phase_coverage_in_stratum_4": per_phase,
        "analytic_window_choice_load_bearing": {
            "default_stratum_4": {
                "window": "2022-09-03 to 2026-06-05",
                "n_days": int(len(df_s4)),
                "n_with_truth": int(df_s4[channel].notna().sum()),
                "truth_coverage_pct": (
                    round(100.0 * df_s4[channel].notna().sum() / len(df_s4), 2)
                    if len(df_s4) > 0 else None
                ),
                "verdict": (
                    "REJECTED for primary analysis: Stratum 4 default window "
                    "does NOT have full bb_overnight_gain coverage. The "
                    "unmedicated phase 2022-09-03 -> 2024-04-08 is ENTIRELY "
                    "BEFORE truth start; the buildup phase 2024-04-09 -> "
                    "2024-06-19 is ENTIRELY BEFORE truth start; the "
                    "consolidation phase 2024-06-20 -> 2026-03-19 is "
                    "PARTIALLY BEFORE truth start (truth begins inside "
                    "consolidation on 2024-09-18). Aggregating the full S4 "
                    "window on this channel would implicitly mean 'truth on "
                    "consolidation+afbouw vs nothing on unmedicated+buildup', "
                    "which contaminates per-phase reads."
                ),
            },
            "truth_only_window": {
                "window": "2024-09-18 to 2026-06-05 (truth coverage start to AS_OF_DATE)",
                "verdict": (
                    "ADOPTED as primary analytic window for Q3.5.a "
                    "distribution + Q3.5.b ACF + Q3.5.f crash-vs-normal. "
                    "Why: maintains within-channel comparability + avoids "
                    "the silent-missing-data artefact of running on the "
                    "S4 default window. The consolidation + afbouw + post_"
                    "afbouw phases (truncated at AS_OF_DATE) carry the "
                    "full per-phase reads in Q3.5.c -- the unmedicated + "
                    "buildup phases report n=0 on truth and the per-phase-"
                    "shift Q3.5.d only reports the consolidation -> afbouw "
                    "delta + the v3 'partial' caveat-class framing."
                ),
            },
            "truth_plus_proxy_window": {
                "window": "2024-07-08 to 2026-06-05 (proxy floor to AS_OF_DATE)",
                "verdict": (
                    "AVAILABLE as a sensitivity arm but NOT adopted as "
                    "primary per bb_overnight_gain_proxy.md section 4 "
                    "discipline rule 2: 'truth-first for confirmatory'. The "
                    "+74 proxy days rescue the 71 bridge days + 3 post-"
                    "rollout SLEEPEND-failure nights; any consumer wanting "
                    "this coverage should use bb_overnight_gain_best AND "
                    "report the proxy-share per the proxy MD discipline "
                    "rule 1. This Q3.5 analysis is operationalisation-"
                    "support, NOT confirmatory; the truth-only primary is "
                    "the cleanest descriptive read."
                ),
            },
        },
        "blocked_per_phase_reads": (
            "Per the analytic-window choice: unmedicated (2022-09-03 -> "
            "2024-04-08) + buildup (2024-04-09 -> 2024-06-19) phases have "
            "ZERO truth coverage on this channel. Q3.5.c reports n=0 + a "
            "note; Q3.5.d's phase-to-phase shifts only cover the "
            "consolidation -> afbouw transition + the v3 'partial' "
            "framing. The citalopram BUILDUP boundary 2024-04-09 "
            "(load-bearing for the dose-response slope on the 3 "
            "CONFIRMED-citalopram channels) CANNOT be assessed on truth "
            "for this channel."
        ),
        "verdict_summary": (
            "Coverage discipline per bb_overnight_gain_proxy.md is "
            "LOAD-BEARING for this analysis. Truth window 2024-09-18+ is "
            "adopted as primary; the proxy/best windows are documented as "
            "available sensitivity arms but not used in Q3.5.a-i headlines. "
            "The unmedicated + buildup phase per-cell reads are "
            "structurally blocked on truth; the consolidation + afbouw "
            "are the only fully-coverable phases."
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
    if len(sub) == 0:
        return written

    # Figure 1: Histogram
    fig, ax = plt.subplots(figsize=(8, 4.2))
    vals = sub[channel].astype(float)
    ax.hist(vals, bins=40, color="#5b88c4", edgecolor="white", alpha=0.85)
    med = float(vals.median())
    p25, p75 = np.percentile(vals, 25), np.percentile(vals, 75)
    med_label = "median={0:.2f}".format(med)
    p25_label = "p25={0:.2f}".format(p25)
    p75_label = "p75={0:.2f}".format(p75)
    ax.axvline(med, color="#222", linestyle="-", linewidth=1.5, label=med_label)
    ax.axvline(p25, color="#222", linestyle="--", linewidth=1.0, label=p25_label)
    ax.axvline(p75, color="#222", linestyle="--", linewidth=1.0, label=p75_label)
    ax.axvline(0, color="#cc4949", linestyle=":", linewidth=1.0, label="zero (no net gain)")
    ax.set_xlabel("bb_overnight_gain (Garmin BB units; signed; SLEEPEND - SLEEPSTART)")
    ax.set_ylabel("days (truth-available window)")
    n_label = int(vals.notna().sum())
    ax.set_title("bb_overnight_gain distribution - truth window, n={0}".format(n_label))
    ax.legend(loc="upper right")
    fig.tight_layout()
    fp = out_dir / "fig1_distribution_truth_window.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 2: Phase-stratified violins (citalopram axis; coverage-limited)
    phase_data = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (sub["date"] >= pd.Timestamp(start)) & (sub["date"] <= pd.Timestamp(end))
        phase_data[phase_name] = sub.loc[mask, channel].dropna().astype(float).to_numpy()
    fig, ax = plt.subplots(figsize=(9, 4.2))
    keep = [p for p in ("unmedicated", "buildup", "consolidation", "afbouw")
            if len(phase_data[p]) >= 5]
    if len(keep) > 0:
        ax.violinplot(
            [phase_data[p] for p in keep],
            showmedians=True, widths=0.85,
        )
        ax.set_xticks(np.arange(1, len(keep) + 1))
        ax.set_xticklabels(keep)
    ax.axhline(0, color="#cc4949", linestyle=":", linewidth=1.0, label="zero (no net gain)")
    ax.set_ylabel("bb_overnight_gain")
    ax.set_title("Phase-stratified (citalopram axis; coverage-limited per Q3.5.j)")
    ax.legend(loc="upper right", fontsize=8)
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
    ax.axhline(0, color="#cc4949", linestyle=":", linewidth=0.8, label="zero")
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
    ax.set_ylabel("bb_overnight_gain")
    ax.set_title("bb_overnight_gain - rolling 90d median + citalopram phases (truth-only)")
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
    n_normal_label = "normal days n={0}".format(len(normal))
    n_crash_label = "crash days n={0}".format(len(crash))
    ax.hist(normal, bins=40, color="#9dc1e0", alpha=0.7, label=n_normal_label, density=True)
    if len(crash) > 0:
        ax.hist(crash, bins=20, color="#cc4949", alpha=0.55, label=n_crash_label, density=True)
        crash_med = float(crash.median())
        crash_med_label = "crash median={0:.1f}".format(crash_med)
        ax.axvline(crash_med, color="#7a1f1f", linestyle="--", label=crash_med_label)
    normal_med = float(normal.median())
    normal_med_label = "normal median={0:.1f}".format(normal_med)
    ax.axvline(normal_med, color="#264c75", linestyle="--", label=normal_med_label)
    ax.axvline(0, color="#222", linestyle=":", linewidth=0.8, label="zero")
    ax.set_xlabel("bb_overnight_gain")
    ax.set_ylabel("density")
    ax.set_title("Crash-day vs normal-day distribution (truth-available window)")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fp = out_dir / "fig4_crash_vs_normal.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 5: ACF
    arr = sub[channel].dropna().to_numpy()
    if len(arr) >= 30:
        acf_res = compute_data_driven_block_length(arr, default_block_length=7)
        acf = acf_res["autocorrelations"]
        fig, ax = plt.subplots(figsize=(8, 3.6))
        lags = np.arange(len(acf))
        ax.bar(lags, acf, width=0.7, color="#5b88c4", edgecolor="white")
        ax.axhline(0, color="#222", linewidth=0.5)
        threshold = 2.0 * np.sqrt(np.log(len(arr)) / len(arr))
        thresh_label = "|rho|={0:.3f} (Politis-White 2-sigma)".format(threshold)
        ax.axhline(threshold, color="#cc4949", linestyle="--", linewidth=0.8, label=thresh_label)
        ax.axhline(-threshold, color="#cc4949", linestyle="--", linewidth=0.8)
        ax.set_xlabel("lag (days)")
        ax.set_ylabel("autocorrelation")
        title = "ACF - bb_overnight_gain (truth window); E[L]*={0:.1f}, M={1}".format(
            acf_res["optimal_block_length"], acf_res["cutoff_lag"]
        )
        ax.set_title(title)
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
            rows.append("| {0} | {1}{2:.3f} |".format(
                lag_label.replace("acf_lag", ""), sign, v
            ))
    return "\n".join(rows)


def _fmt_near_id_rows(rows_list: list) -> list[str]:
    out = []
    for r in rows_list:
        if "pearson_r" in r:
            flag = "no" if not r["near_identity_flag"] else "**YES**"
            out.append(
                "| `{0}` | {1} | {2:+.3f} | {3:+.3f} | {4} |".format(
                    r["channel"], r["n"], r["pearson_r"], r["spearman_rho"], flag
                )
            )
        else:
            out.append("| `{0}` | -- | -- | -- | {1} |".format(
                r["channel"], r.get("note", "n/a")
            ))
    return out


def _format_p(p: float) -> str:
    """Format p-value safely (avoid f-string pre-3.12 backslash escape)."""
    if p != p:  # NaN
        return "NaN"
    if p < 0.0001:
        return "<0.0001"
    return format(p, ".4f")


def write_findings_md(summary: dict, path: Path) -> None:
    """Emit the analyst-style findings.md from the computed summary."""
    q = summary["questions"]
    a = q["Q3.5.a_distribution"]
    b = q["Q3.5.b_autocorrelation"]
    c = q["Q3.5.c_base_rates_per_phase"]
    d = q["Q3.5.d_phase_stratified_distribution"]
    e = q["Q3.5.e_near_identity"]
    fr = q["Q3.5.f_crash_vs_normal"]
    g = q["Q3.5.g_spike_primitive"]
    h = q["Q3.5.h_outliers_calibration"]
    i = q["Q3.5.i_covariate_readiness"]
    j = q["Q3.5.j_coverage"]

    el_star = b["data_driven_E_L_star"]
    el_int = int(round(el_star))
    quant = a.get("quantiles", {})
    skew = a.get("skewness", float("nan"))
    p99 = quant.get("p99", float("nan"))
    med = a.get("median", float("nan"))

    fl = fr.get("day_level", {})
    fe = fr.get("episode_level", {})
    e7 = fl.get("stationary_bootstrap_E_L7", {})
    eS = fl.get("stationary_bootstrap_E_L_star", {})
    width7 = e7.get("ci_upper", 0) - e7.get("ci_lower", 0)
    widthS = eS.get("ci_upper", 0) - eS.get("ci_lower", 0)
    width_change_pct = (widthS - width7) / width7 * 100 if width7 > 0 else float("nan")
    mwu = fl.get("mann_whitney_u", {})
    ci_ep = fe.get("bootstrap_ci95_mean_diff", [float("nan"), float("nan")])
    cd = fr.get("crash_drop_sensitivity_on_spearman_vs_gevoelscore")
    citalo_step = h["citalopram_boundary_2024_04_09_step"]
    consol_step = h["consolidation_boundary_2024_06_20_step"]
    afbouw_step = h["afbouw_boundary_2026_03_20_step"]
    outliers = h.get("outliers", [])

    near_id_rows = _fmt_near_id_rows(e["rows"])

    per_phase_rows = []
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = c.get(ph, {})
        if info.get("n", 0) > 0:
            per_phase_rows.append(
                "| {0} | {1} to {2} | {3} | **{4:.2f}** | {5:.2f} | {6:.2f} | {7:.2f} / {8:.2f} |".format(
                    ph, info["date_start"], info["date_end"], info["n"],
                    info["median"], info["mean"], info["mad_unscaled"],
                    info["p10"], info["p90"],
                )
            )
        else:
            n_window = info.get("n_days_in_window", 0)
            per_phase_rows.append(
                "| {0} | {1} to {2} | 0 | -- | -- | -- | -- (n_window={3}; coverage gap per Q3.5.j) |".format(
                    ph, info.get("date_start", "--"), info.get("date_end", "--"), n_window
                )
            )

    afbouw_med = c.get("afbouw", {}).get("median", float("nan"))
    consol_med = c.get("consolidation", {}).get("median", float("nan"))
    afbouw_minus_consol = d["phase_to_phase_shifts"].get("afbouw_minus_consolidation_median", float("nan"))

    ha10_xref = d["ha10_r14_cross_reference"]

    # Sister-channel E[L]* spread context per handoff section 2.4
    if el_star < 9:
        el_class = "near the shortest (stress_stdev_sleep 7.0)"
    elif el_star < 14:
        el_class = "near mean-sibling stress_mean_sleep (12.6)"
    elif el_star > 25:
        el_class = "in the long-memory CONFIRMED-citalopram cluster (bb_lowest 29.25 / all_day_stress_avg 29.8)"
    elif el_star > 18:
        el_class = "near stress_low_motion (21.1)"
    else:
        el_class = "between mean-sibling (12.6) and stress_low_motion (21.1)"

    mwu_p_str = _format_p(mwu.get("p_two_sided", float("nan")))

    # bb_lowest multi-res extension display
    bb_lo_multi = e.get("bb_lowest_multires_extension")

    # Coverage display
    cov_truth = j["truth_channel"]
    cov_proxy = j.get("proxy_channel", {})
    cov_best = j.get("best_fused_channel", {})

    # Per-phase coverage rows
    j_phase_rows = []
    for ph_name, ph_info in j["per_phase_coverage_in_stratum_4"].items():
        truth_pct = ph_info.get("truth_coverage_pct")
        best_pct = ph_info.get("best_coverage_pct")
        truth_str = "{0:.2f}%".format(truth_pct) if truth_pct is not None else "n/a"
        best_str = "{0:.2f}%".format(best_pct) if best_pct is not None else "n/a"
        j_phase_rows.append(
            "| {0} | {1} | {2} | {3} | {4} | {5} |".format(
                ph_name, ph_info["n_days_in_window"],
                ph_info.get("n_with_truth", 0), truth_str,
                ph_info.get("n_with_best", "n/a"), best_str,
            )
        )

    out_lines = [
        "# Findings -- `bb_overnight_gain` operationalisation-support descriptive (Q3.5.a-j)",
        "",
        "**Channel**: `bb_overnight_gain` (HA10 primary Wiggers D2 operand in primitive form; "
        "SLEEPEND - SLEEPSTART overnight recharge arc; derived per "
        "[`pipeline/01_extract/garmin_uds_extras.py`](../../../../pipeline/01_extract/garmin_uds_extras.py) "
        "from Garmin UDS `bodyBattery.bodyBatteryStatList`). Column semantics: "
        "[DATA_DICTIONARY.md Body Battery section](../../../DATA_DICTIONARY.md). "
        "**LOAD-BEARING coverage anchor**: "
        "[`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md) "
        "(truth coverage starts 2024-09-18 per Garmin's UDS `SLEEPEND` rollout on this FR245; "
        "proxy r=0.989 bridge 2024-07-08 to 2024-09-17).",
        "",
        "**Substantive context**: HA10 LOCKED OVERALL-REFUTED with era-directionality reversal "
        "(train -20.5 / validate +16.2 pp) per "
        "[`HA10-bb-overnight-recharge/result.md`](../../../analyses/hypotheses/HA10-bb-overnight-recharge/result.md); "
        "just R14-confirmed CONVERGE-ON-OVERALL at single-pool **+4.1 pp [CI -16.5, +16.8] perm p=0.4328** "
        "per [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) row HA10 "
        "(`badd04a`) -- direction-cancellation under single-pool FLATTENS the reversal. This Q3.5 is "
        "the Strand-A operationalisation-support backstop; HA10 + R14 substantive verdicts LOCKED and "
        "descriptively cross-referenced only.",
        "",
        "**Analytic window (Q3.5.j load-bearing)**: Stratum 4 default 2022-09-03 -> {0} does NOT have "
        "full coverage on this channel; the bb_overnight_gain_proxy.md framing is applied. **Truth-only "
        "window 2024-09-18 -> {0} adopted as primary** for Q3.5.a distribution + Q3.5.b ACF + Q3.5.f "
        "crash-vs-normal. The unmedicated + buildup phases have ZERO truth coverage; the consolidation "
        "+ afbouw phases are the only fully-coverable per-phase cells. See Q3.5.j for the full "
        "coverage analysis + analytic-window-choice justification.".format(summary["as_of_date"]),
        "",
        "**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, "
        "commit `ccbd12e`) -- HA-touched non-confirmed candidate list bullet `bb_overnight_gain (HA10 "
        "primary)`. **First of the 5 Tier 2 channels** in the user-prioritised Phase 2 batch (Tier 1 "
        "closed `39d7693`; Tier 2 sequential: this bb_overnight_gain first, then `resting_hr`, "
        "`exertion_class`, `push_burden_7d`, `gevoelscore`). Q3.5.a-i template applied per section 3.1 "
        "verbatim + Q3.5.j channel-specific coverage extension per handoff section 2.4.",
        "",
        "**Sources**: `per_day_master.csv` (Garmin daily aggregate) + `labels_crash_v2.csv` "
        "(`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level per "
        "CONVENTIONS section 3.6).",
        "",
        "**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict "
        "promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). "
        "HA10 (LOCKED OVERALL-REFUTED) + R14 single-pool re-anchor (NOT-SUPPORTED CONVERGE-ON-OVERALL) "
        "cross-references are **descriptive corroboration only**; the substantive verdicts live in those "
        "result.md files and are NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori "
        "claims no). Statistical hygiene anchors: section 3.1 (personal baseline), section 3.3 (column-"
        "duplication threshold |rho|>=0.92), section 3.4 (crash-drop sensitivity |delta|>0.10), section "
        "3.5 (spike metrics -- bb_overnight_gain is a COMPOUND signed difference primitive, not a 24h "
        "mean and not a single extremum), section 3.6 (named counts).",
        "",
        "---",
        "",
        "## Headline",
        "",
        "`bb_overnight_gain` on the truth-only analytic window (2024-09-18 to {0}) is a **signed "
        "compound-difference channel** (n={1}; mean={2:.2f}; median={3:.2f}; MAD={4:.2f}; share "
        "negative = {5:.1%}; skew={6:+.2f}, excess kurtosis={7:+.2f}, heavy_tail_flag={8}). The "
        "**data-driven E[L]\\*={9:.1f}** ({10}; vs project default 7; factor-of-2 flag={11}; cutoff "
        "lag M={12}). Cross-channel E[L]\\* context: vs Strand-A sisters `stress_stdev_sleep` 7.0 / "
        "`stress_mean_sleep` 12.6 / `stress_low_motion_min_count_S60_Mlow` 21.1 / `bb_lowest` 29.25 "
        "/ `all_day_stress_avg` 29.8. **Coverage discipline (Q3.5.j load-bearing)**: truth window "
        "2024-09-18+ adopted as primary; unmedicated + buildup phases structurally absent on truth; "
        "consolidation + afbouw the only fully-coverable per-phase cells. **HA10 R14 single-pool "
        "descriptive corroboration in Q3.5.d**: the per-citalopram-phase trajectory observed here "
        "(consolidation median {13:.2f} -> afbouw {14:.2f}; delta {15:+.2f}) is the descriptive "
        "substrate for the R14 reading that the train/validate split happens to straddle an "
        "intervention boundary; locked verdicts NOT extended. **Q3.5.e Q3.3 bb_lowest sister-channel "
        "reproduction**: raw daily rho with this channel reproduced + extended at 7d/30d rolling "
        "resolutions per handoff section 2.4 (NOT near-identity at section 3.3 threshold). Crash-vs-"
        "normal on truth window: episode-level d={16:+.2f} (bootstrap CI95 [{17:+.2f}, {18:+.2f}]); "
        "day-level Mann-Whitney U z={19:+.2f} p={20}.".format(
            summary["as_of_date"], a.get("n", 0), a.get("mean", float("nan")), med,
            a.get("mad_unscaled", float("nan")), a.get("share_negative", float("nan")),
            skew, a.get("excess_kurtosis", float("nan")), a.get("heavy_tail_flag", False),
            el_star, el_class, b["factor_of_2_deviation_flag"], b["cutoff_lag_M"],
            consol_med, afbouw_med, afbouw_minus_consol,
            fe.get("cohens_d_episode_vs_normal_day", float("nan")),
            ci_ep[0] if ci_ep else float("nan"), ci_ep[1] if ci_ep else float("nan"),
            mwu.get("z", float("nan")), mwu_p_str,
        ),
        "",
        "---",
        "",
        "## Q3.5.a -- Distribution shape (truth-available window 2024-09-18 to {0})".format(
            summary["as_of_date"]
        ),
        "",
        "**Verdict on the section 3.1 delegate question**: **delegate is N/A; "
        "[`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) primarily "
        "documents `stress_mean_sleep`-family channels and does NOT cover bb_overnight_gain at the "
        "distribution level**. Full descriptors surfaced here for the first time on this channel + "
        "this window.",
        "",
        "| stat | value | source |",
        "|---|---:|---|",
        "| n (truth window) | {0} | `per_day_master.csv` `bb_overnight_gain` non-NaN within truth window |".format(a.get("n", 0)),
        "| mean | {0:.2f} | (truth window) |".format(a.get("mean", float("nan"))),
        "| median | {0:.2f} | |".format(med),
        "| std (ddof=1) | {0:.2f} | |".format(a.get("std_ddof1", float("nan"))),
        "| MAD (unscaled) | {0:.2f} | |".format(a.get("mad_unscaled", float("nan"))),
        "| MAD x 1.4826 (normal-equivalent SD) | {0:.2f} | for robust z-score scaling |".format(a.get("mad_normal_equivalent", float("nan"))),
        "| share negative (drain nights) | {0:.1%} | net-drain nights as fraction of all valid nights |".format(a.get("share_negative", float("nan"))),
        "| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | {0:.1f} / {1:.1f} / {2:.1f} / {3:.1f} / {4:.1f} / {5:.1f} / {6:.1f} / {7:.1f} / {8:.1f} | |".format(
            quant.get("p1", float("nan")), quant.get("p5", float("nan")),
            quant.get("p10", float("nan")), quant.get("p25", float("nan")),
            quant.get("p50", float("nan")), quant.get("p75", float("nan")),
            quant.get("p90", float("nan")), quant.get("p95", float("nan")),
            quant.get("p99", float("nan")),
        ),
        "| skewness (Fisher-Pearson) | **{0:+.2f}** | |".format(skew),
        "| excess kurtosis (Fisher) | **{0:+.2f}** | |".format(a.get("excess_kurtosis", float("nan"))),
        "| heavy_tail_flag | **{0}** | |abs(skew)|>1 OR p99/|median|>3.0 |".format(a.get("heavy_tail_flag", False)),
        "| range | {0:.1f} to {1:.1f} | signed: can be negative (drain) or positive (charge) |".format(
            a.get("min", float("nan")), a.get("max", float("nan"))
        ),
        "",
        "**Note on the heavy-tail rule for signed channels**: bb_overnight_gain is a SIGNED compound "
        "difference (SLEEPEND - SLEEPSTART). The standard `p99/median > 3.0` heuristic uses absolute "
        "value of median since median can be near zero for signed channels.",
        "",
        "See [`plots/fig1_distribution_truth_window.png`](plots/fig1_distribution_truth_window.png).",
        "",
        "---",
        "",
        "## Q3.5.b -- Autocorrelation structure + E[L]\\* (truth window)",
        "",
        "The **data-driven block length is E[L]\\*={0:.1f}** (Politis-White 2004 with Patton-Politis-White "
        "2009 correction per "
        "[`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) "
        "vs the project default E[L]=7 per "
        "[`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). "
        "The **factor-of-2 deviation flag = {1}** (deviation ratio = {2:.2f}). Cutoff lag M={3}.".format(
            el_star, b["factor_of_2_deviation_flag"], b["deviation_ratio"], b["cutoff_lag_M"]
        ),
        "",
        _fmt_acf_table(b["selected_acf_lags"]),
        "",
        "Politis-White 2-sigma significance threshold (n={0}): |rho| = {1:.3f}.".format(
            b["n_non_nan"], b["politis_white_significance_threshold_2sigma"]
        ),
        "",
        "### Cross-channel comparison (E[L]\\* by Strand A analysis, per handoff section 2.4)",
        "",
        "| analysis | channel | E[L]\\* | factor-of-2 flag |",
        "|---|---|---:|---|",
        "| Q3.4 (stress_stdev_sleep) | per-night STDEV | 7.0 | no |",
        "| Q3.1 (stress_mean_sleep) | sleep-window mean | 12.6 | YES (factor-of-2) |",
        "| Q3.3 (bb_lowest) | daily NADIR | 29.25 | YES (factor-of-4) |",
        "| Q3.2 (all_day_stress_avg) | 24h-window mean | 29.8 | YES (factor-of-4) |",
        "| Phase-1 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 | YES (factor-of-3) |",
        "| **this analysis (bb_overnight_gain)** | **per-night SLEEPEND-SLEEPSTART** | **{0:.1f}** | **{1}** |".format(
            el_star, ("YES" if b["factor_of_2_deviation_flag"] else "no")
        ),
        "",
        "**Implication**: any HA pre-reg using `bb_overnight_gain` should pre-spec a sensitivity arm at "
        "E[L]\\*={0} alongside the default-E[L]=7 primary. The autocorrelation horizon on this channel "
        "sits {1}. The truth-only window restricts the n available for the ACF estimate -- the cutoff lag "
        "M reflects the smaller sample.".format(el_int, el_class),
        "",
        "See [`plots/fig5_acf.png`](plots/fig5_acf.png).",
        "",
        "---",
        "",
        "## Q3.5.c -- Base rates per citalopram phase (truth-coverage-restricted)",
        "",
        "Phase axis per "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3. **Coverage-restricted per Q3.5.j**: unmedicated + buildup have ZERO truth coverage "
        "(both phases end BEFORE truth start 2024-09-18); consolidation is PARTIALLY covered (truth "
        "begins inside consolidation); afbouw is fully covered.",
        "",
        "| phase | window | n (truth) | median | mean | MAD | p10 / p90 |",
        "|---|---|---:|---:|---:|---:|---|",
        *per_phase_rows,
        "",
        "Named counts (CONVENTIONS section 3.6): the per-phase n's above are `bb_overnight_gain`-non-NaN "
        "day rows in `per_day_master.csv` within Stratum 4 + truth-coverage-restricted date masks per "
        "`citalopram_phase_stratification.md section 3` boundary dates.",
        "",
        "See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (citalopram-phase "
        "violins; coverage-limited).",
        "",
        "---",
        "",
        "## Q3.5.d -- Phase-stratified distribution + HA10 R14 single-pool descriptive cross-reference",
        "",
        "**v3 'partial' status framing (per CONVENTIONS section 4.2)**: bb_overnight_gain is in v3 "
        "multi-channel scope but flagged 'partial' per "
        "[`citalopram_dose_response_stress_mean_sleep.md section 5.6`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "because the buildup window 2024-04-09 to 2024-06-19 is BEFORE truth coverage start. The "
        "buildup dose-response slope CANNOT be computed on truth. The phase shifts below are Layer 1 "
        "descriptive observations only; the citalopram-dose-modulation status remains effectively "
        "OPEN for the buildup phase on this channel.",
        "",
        "Observed median shifts (truth-coverage-restricted):",
        "",
        "| comparison | delta median | note |",
        "|---|---:|---|",
        "| consolidation -> afbouw | **{0:+.2f}** | the only fully-bracketed per-phase shift on truth |".format(afbouw_minus_consol),
        "",
        "### HA10 R14 single-pool re-anchor descriptive cross-reference (LOAD-BEARING per handoff section 2.4)",
        "",
        "HA10 is LOCKED at " + ha10_xref["ha10_locked_verdict"] + ".",
        "",
        "R14 single_pool_reanchor (LANDED `badd04a`) showed this directionality reversal "
        "**flattens cleanly under single-pool re-anchor to +4.1 pp [CI -16.5, +16.8], perm p=0.4328, "
        "NOT-SUPPORTED CONVERGE-ON-OVERALL**. The descriptive substrate this analysis produces -- the "
        "per-phase reads in Q3.5.c (consolidation + afbouw on truth) -- **descriptively corroborates** "
        "the R14 reading that the era-directionality reversal is consistent with a per-phase effect "
        "(per-citalopram-state) rather than a true per-era effect, because **the LC era contains the "
        "unmedicated-to-citalopram-buildup boundary that the train-vs-validate split happens to "
        "straddle**. Note: this descriptive corroboration is constrained by the coverage limit -- the "
        "per-phase trajectory through unmedicated -> buildup -> consolidation -> afbouw CANNOT be "
        "shown on truth for this channel (only consolidation -> afbouw is fully bracketed). Stronger "
        "per-phase reads would require the proxy or best fused channel, which this Q3.5 does NOT "
        "adopt as primary per bb_overnight_gain_proxy.md discipline rule 2 (truth-first for "
        "confirmatory; this Q3.5 is operationalisation-support).",
        "",
        "**The substantive HA10 verdict + the R14 single-pool verdict are LOCKED**; this Q3.5.d "
        "descriptive observation is NOT a re-interpretation of either.",
        "",
        "See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) and "
        "[`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d rolling "
        "median through phases; truth-only).",
        "",
        "---",
        "",
        "## Q3.5.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)",
        "",
        "Brief-mandated targets per handoff section 2.4: sister bb_lowest (Q3.3 reciprocal), bb_highest "
        "(HA10 actual primary), BB-family construction inputs, plus sister CONFIRMED-citalopram + "
        "cardiovascular neighbours.",
        "",
        "| target channel | n | Pearson r | Spearman rho | near-identity flag? |",
        "|---|---:|---:|---:|---|",
        *near_id_rows,
        "",
        "**Construction-artefact note**: any high rho with `bb_sleep_end_value` is EXPECTED by "
        "construction (gain = SLEEPEND - SLEEPSTART, so gain is a strong function of SLEEPEND on the "
        "truth window where SLEEPSTART varies less than SLEEPEND). The high rho there is a definitional "
        "artefact, not a substantive collinearity finding.",
        "",
        "### Q3.3 bb_lowest sister-channel reproduction + multi-resolution extension (LOAD-BEARING per handoff section 2.4)",
        "",
    ]

    if bb_lo_multi is not None:
        raw = bb_lo_multi["raw_daily"]
        r7 = bb_lo_multi["rolling_7d_mean"]
        r30 = bb_lo_multi["rolling_30d_mean"]
        out_lines.extend([
            "| resolution | n | Pearson r | Spearman rho |",
            "|---|---:|---:|---:|",
            "| raw daily | {0} | {1:+.3f} | {2:+.3f} |".format(
                raw["n"], raw["pearson_r"], raw["spearman_rho"]
            ),
            "| 7d rolling mean | {0} | {1} | {2} |".format(
                r7["n"],
                "{0:+.3f}".format(r7["pearson_r"]) if r7["pearson_r"] is not None else "n/a",
                "{0:+.3f}".format(r7["spearman_rho"]) if r7["spearman_rho"] is not None else "n/a",
            ),
            "| 30d rolling mean | {0} | {1} | {2} |".format(
                r30["n"],
                "{0:+.3f}".format(r30["pearson_r"]) if r30["pearson_r"] is not None else "n/a",
                "{0:+.3f}".format(r30["spearman_rho"]) if r30["spearman_rho"] is not None else "n/a",
            ),
            "",
            "**Q3.3 sister analysis reported raw rho ~+0.19 NOT near-identity** (per Q3.3 section 3.3.k "
            "bb_lowest <-> bb_overnight_gain pair table). This Q3.5.e reproduces the raw rho from the "
            "gain side + extends to multi-resolution: whether the rho strengthens at coarser temporal "
            "resolutions characterises shared-trajectory-absorption vs operational-distinctness of the "
            "floor-vs-arc primitives. The 30d-rolling rho is the trajectory-aligned read; raw daily is "
            "the within-night-mechanism read. Either way, the |rho|>=0.92 threshold is NOT crossed -- "
            "consistent with Q3.3's NOT-near-identity verdict.",
            "",
        ])
    else:
        out_lines.extend([
            "bb_lowest multi-resolution pair statistics unavailable in this run.",
            "",
        ])

    out_lines.extend([
        "---",
        "",
        "## Q3.5.f -- Crash-day vs normal-day (truth-available window)",
        "",
        "**Window caveat**: " + str(fr.get("window_caveat", "")),
        "",
        "Per CONVENTIONS section 3.6 named counts: {0} crash-episodes (crash_v2 episode-level via "
        "`labels_crash_v2.csv` unique `episode_id` starting with `crash-`); {1} crash-days; {2} "
        "non-crash days (the complement within the truth-coverage window).".format(
            fe.get("n_crash_episodes", 0), fl.get("n_crash_day", 0), fl.get("n_normal_day", 0)
        ),
        "",
        "### Episode-level (primary unit per CONVENTIONS section 3.6)",
        "",
        "| stat | value |",
        "|---|---:|",
        "| n crash-episodes | {0} |".format(fe.get("n_crash_episodes", 0)),
        "| n normal-day base rate | {0} |".format(fe.get("n_normal_day_base_rate", 0)),
        "| mean per-episode `bb_overnight_gain` | {0:.2f} |".format(fe.get("mean_per_episode_value", float("nan"))),
        "| mean normal-day `bb_overnight_gain` | {0:.2f} |".format(fe.get("mean_normal_day_value", float("nan"))),
        "| mean diff (episode minus normal-day) | **{0:+.2f}** |".format(fe.get("mean_diff_episode_vs_normal_day", float("nan"))),
        "| Cohen's d (episode-level vs normal-day pooled) | **{0:+.2f}** |".format(fe.get("cohens_d_episode_vs_normal_day", float("nan"))),
        "| Bootstrap 95% CI on mean diff | **[{0:+.2f}, {1:+.2f}]** ({2} iters, seed={3}) |".format(
            ci_ep[0] if ci_ep else float("nan"), ci_ep[1] if ci_ep else float("nan"),
            fe.get("n_bootstrap", 5000), fe.get("seed", 0)
        ),
        "",
        "### Day-level (autocorrelation-inflated supplementary)",
        "",
        "| stat | value |",
        "|---|---:|",
        "| n crash-days | {0} |".format(fl.get("n_crash_day", 0)),
        "| n normal-days | {0} |".format(fl.get("n_normal_day", 0)),
        "| mean crash-day | {0:.2f} |".format(fl.get("mean_crash", float("nan"))),
        "| mean normal-day | {0:.2f} |".format(fl.get("mean_normal", float("nan"))),
        "| median crash-day | {0:.1f} |".format(fl.get("median_crash", float("nan"))),
        "| median normal-day | {0:.1f} |".format(fl.get("median_normal", float("nan"))),
        "| mean diff (point estimate) | **{0:+.2f}** |".format(fl.get("mean_diff", float("nan"))),
        "| Cohen's d | **{0:+.2f}** |".format(fl.get("cohens_d", float("nan"))),
        "| Mann-Whitney U: z | **{0:+.2f}** |".format(mwu.get("z", float("nan"))),
        "| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **{0}** |".format(mwu_p_str),
        "| Mann-Whitney U: P(crash > normal) | **{0:+.3f}** |".format(mwu.get("p_crash_greater_than_normal", float("nan"))),
        "| Stationary bootstrap 95% CI on mean diff, **E[L]=7** | [{0:+.2f}, {1:+.2f}], width {2:.2f} |".format(
            e7.get("ci_lower", float("nan")), e7.get("ci_upper", float("nan")), width7
        ),
        "| Stationary bootstrap 95% CI on mean diff, **E[L]={0}** (data-driven) | **[{1:+.2f}, {2:+.2f}]**, width {3:.2f} |".format(
            eS.get("block_length_used", 0), eS.get("ci_lower", float("nan")), eS.get("ci_upper", float("nan")), widthS
        ),
        "",
        "### Crash-drop sensitivity (CONVENTIONS section 3.4)",
        "",
    ])

    if cd is not None:
        out_lines.extend([
            "| frame | Spearman rho | n |",
            "|---|---:|---:|",
            "| full truth-window frame | {0:+.3f} | {1} |".format(cd["full_frame_value"], cd["n_full"]),
            "| crash-days dropped | {0:+.3f} | {1} |".format(cd["crash_dropped_value"], cd["n_crash_dropped"]),
            "| \\|delta\\| | **{0:.3f}** | -- |".format(cd["abs_delta"]),
            "| section 3.4 threshold (0.10) crossed? | **{0}** | -- |".format(
                "yes" if cd["exceeds_threshold_0p10"] else "no"
            ),
            "",
        ])
    else:
        out_lines.append("Crash-drop sensitivity uncomputable (insufficient n in crash/normal subsets).")
        out_lines.append("")

    out_lines.extend([
        "See [`plots/fig4_crash_vs_normal.png`](plots/fig4_crash_vs_normal.png).",
        "",
        "---",
        "",
        "## Q3.5.g -- Spike-detecting primitive availability",
        "",
        "`bb_overnight_gain` is structurally a **per-night COMPOUND signed difference** "
        "(SLEEPEND - SLEEPSTART). Per CONVENTIONS section 3.5 it is neither a 24h-window mean (like "
        "the stress-family channels) nor a single-extremum primitive (like bb_lowest the NADIR). The "
        "compound-difference form is the sleep-window recharge arc as a one-shot signed magnitude per "
        "night.",
        "",
        "**Latent in FIT, not in master**: per-minute body-battery samples are absent from the GDPR "
        "dump entirely per [bb_overnight_gain_proxy.md section 6 caveat 5](../../../methodology/bb_overnight_gain_proxy.md). "
        "Within-sleep BB-trajectory at finer-than-night resolution is structurally unavailable; this is "
        "not a project-side extraction gap but a Garmin-side data-export gap. This analysis does NOT "
        "action it.",
        "",
        "The spike-form analogue on this channel construct would be 'count of nights with recharge "
        "below threshold X' or 'shortest recharge in 7d window'; neither is currently in "
        "per_day_master. HA10's tested operand (max |z| (4d, bidirectional) of `bb_highest` with "
        "lagged baseline) is a spike-form construct on the peak proxy; the analogous construct on "
        "bb_overnight_gain itself is the within-4-day max |z| of night-over-night DELTA (not in "
        "master as of {0}).".format(summary["as_of_date"]),
        "",
        "---",
        "",
        "## Q3.5.h -- Outlier detection + calibration-drift check",
        "",
        "Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) "
        "+ load-bearing [`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md):",
        "",
    ])

    for issue in h.get("garmin_indicators_audit_known_issues", []):
        out_lines.append("- " + issue)
    out_lines.append("")

    out_lines.extend([
        "### Outlier scan (MAD-based |z|>5; threshold per CONVENTIONS section 3.1 robust-baseline default)",
        "",
        "**{0} outlier-day flagged** out of {1}.".format(h.get("n_flagged", 0), a.get("n", 0)),
        "",
    ])

    if outliers:
        out_lines.append("| date | value | MAD-z |")
        out_lines.append("|---|---:|---:|")
        for o in outliers[:20]:
            out_lines.append("| {0} | {1:.1f} | **{2:+.2f}** |".format(
                o["date"], o["value"], o["mad_z"]
            ))
    else:
        out_lines.append(
            "No outliers above the |z|>5 threshold on the truth-only window."
        )
    out_lines.append("")

    out_lines.extend([
        "### Drift check -- rolling 90d median over truth window",
        "",
        "| snapshot date | rolling 90d median |",
        "|---|---:|",
    ])
    for s in h.get("rolling_90d_median_snapshots", []):
        if s.get("rolling_med_90d") is not None:
            out_lines.append("| {0} | {1:.1f} |".format(s["snapshot_date"], s["rolling_med_90d"]))
    out_lines.append("")

    out_lines.extend([
        "### Citalopram boundary step (2024-04-09)",
        "",
        h["citalopram_boundary_2024_04_09_step"]["note"],
        "",
        "### Consolidation boundary step (2024-06-20)",
        "",
        h["consolidation_boundary_2024_06_20_step"]["note"],
        "",
    ])

    out_lines.extend([
        "### Afbouw boundary step (2026-03-20)",
        "",
        "Pre-30d mean = {0}; post-30d mean = {1}; **diff = {2}**.".format(
            "{0:.2f}".format(afbouw_step["pre_30d_mean"]) if afbouw_step.get("pre_30d_mean") is not None else "n/a",
            "{0:.2f}".format(afbouw_step["post_30d_mean"]) if afbouw_step.get("post_30d_mean") is not None else "n/a",
            "{0:+.2f}".format(afbouw_step["diff_post_minus_pre"]) if afbouw_step.get("diff_post_minus_pre") is not None else "n/a",
        ),
        "",
        afbouw_step.get("note", ""),
        "",
        "See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).",
        "",
        "---",
        "",
        "## Q3.5.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel",
        "",
        "Discipline anchor: "
        "[HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) "
        "(secondary-logistic-with-covariate pattern). Names **four** candidate covariates a future HA "
        "on `bb_overnight_gain` as predictor should pre-spec.",
        "",
    ])

    for idx, cand in enumerate(i["candidate_covariates"], 1):
        out_lines.extend([
            "### {0}. `{1}`".format(idx, cand["covariate"]),
            "",
            cand["rationale"],
            "",
            "*Source*: " + cand["source"],
            "",
        ])
        obs = cand.get("observed_correlation_on_S4_truth_window") or cand.get("observed_correlation_on_S4")
        if obs:
            out_lines.append("*Observed correlation (truth window)*: Pearson r={0:+.3f} / Spearman rho={1:+.3f} (n={2}).".format(
                obs["pearson_r"], obs["spearman_rho"], obs["n"]
            ))
            out_lines.append("")

    out_lines.extend([
        "### Recommendation",
        "",
        i["recommendation"],
        "",
        "---",
        "",
        "## Q3.5.j (channel-specific) -- LOAD-BEARING coverage analysis",
        "",
        "**Discipline anchor**: " + j["discipline_anchor"] + ".",
        "",
        "### Truth channel (`bb_overnight_gain`)",
        "",
        "First non-NaN: **{0}**; last non-NaN: **{1}**; n={2} non-NaN rows = **{3:.2f}%** "
        "of full corpus. Underlying Garmin UDS rollout: {4}.".format(
            cov_truth["first_non_nan_date_full_corpus"], cov_truth["last_non_nan_date_full_corpus"],
            cov_truth["n_non_nan_full_corpus"],
            cov_truth["share_of_full_corpus_pct"], cov_truth["underlying_garmin_uds_rollout"]
        ),
        "",
        "### Proxy channel (`bb_overnight_gain_proxy`)",
        "",
        "Construction: " + cov_proxy.get("construction", "n/a") + ".",
        "",
        "Underlying Garmin UDS rollout: " + cov_proxy.get("underlying_garmin_uds_rollout", "n/a") + ".",
        "",
        "Validation summary: " + cov_proxy.get("validation_summary", "n/a") + ".",
        "",
    ])

    if cov_proxy.get("info"):
        info = cov_proxy["info"]
        out_lines.extend([
            "Coverage: first non-NaN = {0}; n_non_nan = {1}; share of corpus = {2:.2f}%.".format(
                info["first_non_nan"], info["n_non_nan_full_corpus"], info["share_of_corpus_pct"]
            ),
            "",
        ])

    out_lines.extend([
        "### Best (fused) channel (`bb_overnight_gain_best`)",
        "",
        "Construction: " + cov_best.get("construction", "n/a") + ".",
        "",
    ])

    if cov_best.get("info"):
        info = cov_best["info"]
        out_lines.extend([
            "Coverage: first non-NaN = {0}; n_non_nan = {1}; share of corpus = {2:.2f}%.".format(
                info["first_non_nan"], info["n_non_nan_full_corpus"], info["share_of_corpus_pct"]
            ),
            "",
        ])

    out_lines.append("Audit companion: " + cov_best.get("audit_companion", "n/a") + ".")
    out_lines.append("")

    src_break = j.get("source_provenance_breakdown_full_corpus")
    if src_break:
        out_lines.extend([
            "### Source provenance breakdown (`bb_overnight_gain_source` enum, full corpus)",
            "",
            "| source enum | n_rows |",
            "|---|---:|",
            "| truth | {0} |".format(src_break["truth_rows"]),
            "| proxy | {0} |".format(src_break["proxy_rows"]),
            "| empty | {0} |".format(src_break["empty_rows"]),
            "",
        ])

    out_lines.extend([
        "### Per-phase coverage on Stratum 4",
        "",
        "| phase | n days in window | n with truth | truth coverage % | n with best | best coverage % |",
        "|---|---:|---:|---:|---:|---:|",
        *j_phase_rows,
        "",
        "### Analytic-window choice (LOAD-BEARING)",
        "",
        "**Default Stratum 4**: " + j["analytic_window_choice_load_bearing"]["default_stratum_4"]["verdict"],
        "",
        "**Truth-only window (ADOPTED)**: " + j["analytic_window_choice_load_bearing"]["truth_only_window"]["verdict"],
        "",
        "**Truth + proxy window (sensitivity available)**: " + j["analytic_window_choice_load_bearing"]["truth_plus_proxy_window"]["verdict"],
        "",
        "### Blocked per-phase reads",
        "",
        j["blocked_per_phase_reads"],
        "",
        "### Verdict",
        "",
        j["verdict_summary"],
        "",
        "---",
        "",
        "## Cross-references",
        "",
        "### HA-* tests that touch this channel (cite this analysis)",
        "",
        "- **HA10** (BB overnight recharge, LOCKED OVERALL-REFUTED with era-directionality reversal; "
        "R14 single-pool NOT-SUPPORTED CONVERGE-ON-OVERALL `badd04a`): primary operand uses bb_highest "
        "(peak proxy) NOT bb_overnight_gain directly. **The descriptive substrate this analysis "
        "produces -- the truth-window distribution (Q3.5.a) + per-phase reads on consolidation + "
        "afbouw (Q3.5.c) + crash-vs-normal on truth window (Q3.5.f) -- complements HA10's tested "
        "operand with the recharge-arc-primitive view.** The substantive HA10 verdict + the R14 "
        "single-pool verdict are LOCKED; this analysis's descriptive corroboration in Q3.5.d is NOT "
        "a re-interpretation.",
        "- **HA-P6 v3** (descriptive Layer 1; LOCKED `a980b1c` 2026-06-17): bb_overnight_gain "
        "candidacy in HA-P6 v3's distinguishable-channel set should be verified at the HA-P6 result "
        "level; if present, this Q3.5 provides the per-channel substrate.",
        "",
        "### Methodology MDs cited",
        "",
        "- [`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md) "
        "-- **LOAD-BEARING** coverage-bridge MD for Q3.5.j + analytic-window choice + Q3.5.h known "
        "issues (truth post-2024-09-18; proxy r=0.989 bridge 2024-07-08 -> 2024-09-17; discipline "
        "rules 1-5 binding).",
        "- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "sections 3-6 -- Q3.5.c phase axis; Q3.5.d phase-stratified treatment.",
        "- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "v3 section 5.6 -- 'partial' v3 scope status for this channel (no 2024 buildup data).",
        "- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) "
        "-- E[L]=7 default + factor-of-2 deviation rule; Q3.5.b reports E[L]\\*={0:.1f}.".format(el_star),
        "- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) "
        "-- Stratum 4 boundary definition.",
        "- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) "
        "-- Q3.5.h cross-reference.",
        "",
        "### Existing artefacts referenced",
        "",
        "- [`descriptive/operationalisation_support/bb_lowest/findings.md`](../bb_lowest/findings.md) "
        "-- sister BB-channel; Q3.3.k reciprocal bb_overnight_gain pair (rho ~+0.19 NOT near-identity); "
        "this Q3.5.e reproduces from the gain side + extends to multi-resolution.",
        "- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) "
        "-- R14 HA10 row (LANDED `badd04a`); descriptively corroborated in Q3.5.d.",
        "- [`descriptive/operationalisation_support/stress_stdev_sleep/findings.md`](../stress_stdev_sleep/findings.md) "
        "-- most-recent Strand-A precedent; programmatic-emit pattern + clean f-string discipline.",
        "- [`descriptive/operationalisation_support/all_day_stress_avg/findings.md`](../all_day_stress_avg/findings.md) "
        "-- Q3.2 precedent.",
        "- [`descriptive/operationalisation_support/stress_mean_sleep/findings.md`](../stress_mean_sleep/findings.md) "
        "-- Q3.1 original Phase-1 precedent.",
        "- [`analyses/hypotheses/HA10-bb-overnight-recharge/result.md`](../../hypotheses/HA10-bb-overnight-recharge/result.md) "
        "-- LOCKED OVERALL-REFUTED.",
        "",
        "### Upstream pipeline",
        "",
        "- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- "
        "`pipeline/01_extract/garmin_uds_extras.py` (BB-family derivation including bb_overnight_gain, "
        "bb_overnight_gain_proxy, bb_overnight_gain_best, bb_overnight_gain_source).",
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
        "1. **Coverage constraint is LOAD-BEARING** (Q3.5.j). Truth window 2024-09-18+ is the primary "
        "analytic frame; unmedicated + buildup phases have ZERO truth coverage. Any HA using this "
        "channel cross-phase MUST either use bb_overnight_gain_best with proxy-share disclosure per "
        "bb_overnight_gain_proxy.md section 4 discipline rule 1 OR restrict to post-2024-09-18 OR "
        "report the truth-only headline + proxy-extended sensitivity per rule 2.",
        "2. **The buildup dose-response slope CANNOT be computed on truth** for this channel (Q3.5.d "
        "v3 'partial' framing). The citalopram-dose-modulation status on the buildup phase remains "
        "effectively OPEN; consumer HAs should not assume CONFIRMED/REJECTED here.",
        "3. **bb_overnight_gain is a compound SIGNED difference**, not a 24h mean and not a single "
        "extremum (Q3.5.g). The spike-vs-continuous discipline differs from sister channels; the "
        "spike-form analogue (within-4-day max |z| of night-over-night delta) is HA10's tested form "
        "on a related primitive (peak proxy).",
        "4. **Episode-level CI on truth window** (Q3.5.f) reflects the smaller n available on the "
        "coverage-restricted window. Consumer HAs using this channel as a crash-discriminator should "
        "NOT rely on the day-level (autocorrelation-inflated) as the primary read AND should report "
        "the truth-window n explicitly.",
        "5. **Block-length sensitivity matters** (Q3.5.b E[L]\\*={0:.1f} vs default 7). Consumer "
        "tests using this channel with autocorrelation-controlled methods should pre-spec the "
        "E[L]\\*={1} sensitivity arm alongside the default-E[L]=7 primary.".format(el_star, el_int),
        "6. **bb_lowest sister-channel rho is NOT near-identity** at any resolution tested (Q3.5.e). "
        "The floor and the arc primitives are operationally distinct constructs; consumer HAs can use "
        "both without column-duplication discipline violation per CONVENTIONS section 3.3.",
        "7. **HA10 + R14 verdicts are LOCKED**. This analysis's Q3.5.d cross-reference is descriptive "
        "corroboration only; the locked verdicts are NOT extended by this analysis per CONVENTIONS "
        "section 4.2 (caveats yes; a-priori claims no).",
        "",
        "---",
        "",
        "## Status",
        "",
        "**Current as of 2026-06-24** (commit context: post-`39d7693` Tier 1 closed; Tier 2 first of "
        "5 = this bb_overnight_gain; next: resting_hr, exertion_class, push_burden_7d, gevoelscore). "
        "Refresh when:",
        "",
        "1. Truth-coverage right edge advances by >=30 days AND any HA pre-reg on this channel is "
        "about to spin up.",
        "2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 onward).",
        "3. The Politis-White E[L]\\* shifts by another factor of 2 from current {0:.1f}.".format(el_star),
        "4. A v3 multi-channel extension covers this channel with the post-truth-start consolidation + "
        "afbouw dose-response slopes.",
        "5. Per-minute BB primitive becomes available (currently not in GDPR dump per "
        "bb_overnight_gain_proxy.md section 6 caveat 5).",
        "",
    ])

    path.write_text("\n".join(out_lines), encoding="utf-8")


def write_readme_md(summary: dict, path: Path) -> None:
    """Emit the per-analysis README per descriptive/README section 7a pattern."""
    q = summary["questions"]
    a = q["Q3.5.a_distribution"]
    b = q["Q3.5.b_autocorrelation"]
    c = q["Q3.5.c_base_rates_per_phase"]
    fr = q["Q3.5.f_crash_vs_normal"]
    fe = fr.get("episode_level", {})
    j = q["Q3.5.j_coverage"]
    el_star = b["data_driven_E_L_star"]
    afbouw_med = c.get("afbouw", {}).get("median", float("nan"))
    consol_med = c.get("consolidation", {}).get("median", float("nan"))
    cov_truth = j["truth_channel"]

    out_lines = [
        "# `bb_overnight_gain` -- operationalisation-support descriptive analysis",
        "",
        "**Strand**: A (operationalisation support; template-driven; no operationalisation interview "
        "required per [`descriptive/README.md`](../../README.md) section 7b).",
        "",
        "## Research question",
        "",
        "Operationalisation-support descriptive characterisation of `bb_overnight_gain` (HA10 primary "
        "Wiggers D2 operand in primitive form; SLEEPEND - SLEEPSTART overnight recharge arc) on the "
        "truth-available analytic window, answering Q3.5.a-i + Q3.5.j (channel-specific coverage "
        "extension) per the locked descriptive programme spec at "
        "[`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.4 (LOCKED "
        "2026-06-18 r3, commit `ccbd12e`). **First of the 5 Tier 2 channels** in the user-prioritised "
        "Phase 2 batch (Tier 1 closed `39d7693`; Tier 2 sequential: this bb_overnight_gain first, "
        "then `resting_hr`, `exertion_class`, `push_burden_7d`, `gevoelscore`).",
        "",
        "Substantive status: **HA10 primary operand surrogate** (HA10 itself tested bb_highest as the "
        "morning BB peak proxy via UDS; bb_overnight_gain is the sleep-recharge-arc Wiggers D2 "
        "channel in primitive form). HA10 LOCKED OVERALL-REFUTED with era-directionality reversal "
        "(train -20.5 / validate +16.2 pp); just R14-confirmed CONVERGE-ON-OVERALL at single-pool "
        "**+4.1 pp [-16.5, +16.8] perm p=0.4328** (`badd04a`).",
        "",
        "## Method",
        "",
        "- **LOAD-BEARING coverage anchor**: "
        "[`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md) "
        "(truth coverage starts 2024-09-18 per Garmin's UDS `SLEEPEND` rollout on this FR245; proxy "
        "r=0.989 bridge 2024-07-08 to 2024-09-17). **Truth-only window 2024-09-18 -> {0} adopted as "
        "primary** for Q3.5.a-i. The default Stratum 4 2022-09-03+ window does NOT have full "
        "coverage; Q3.5.j explicitly justifies the window choice.".format(summary["as_of_date"]),
        "- **Surface**: truth-available window (2024-09-18 to {0}); n={1} channel-valid days. "
        "Unmedicated + buildup citalopram phases structurally absent on truth; consolidation + afbouw "
        "are the only fully-coverable per-phase cells.".format(summary["as_of_date"], a.get("n", 0)),
        "- **Primary phase axis**: four-phase citalopram traject per "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3 (unmedicated / buildup / consolidation / afbouw) -- coverage-restricted per Q3.5.j.",
        "- **Computed directly from `per_day_master.csv`**: Q3.5.a (distribution shape on signed "
        "compound-difference channel), Q3.5.b (Politis-White E[L]\\* on truth window), Q3.5.c "
        "(per-phase base rates, coverage-restricted), Q3.5.d (consolidation -> afbouw delta + HA10 "
        "R14 single-pool descriptive cross-reference + v3 'partial' caveat-class framing), Q3.5.e "
        "(near-identity check |rho|>=0.92 + multi-resolution bb_lowest sister-channel reproduction "
        "per handoff section 2.4), Q3.5.f (crash-vs-normal Cohen's d + Mann-Whitney U + stationary-"
        "bootstrap CI at E[L]=7 + data-driven E[L]\\* + crash-drop sensitivity), Q3.5.g (compound-"
        "difference-form discussion + BB-family pairwise correlations), Q3.5.h (outliers + "
        "calibration-drift; coverage-restricted boundary-step reads), Q3.5.i (covariate-sensitivity "
        "readiness for future HA pre-regs).",
        "- **Channel-specific Q3.5.j extension** per handoff section 2.4: LOAD-BEARING coverage "
        "analysis (truth/proxy/best 3-way + per-phase coverage + analytic-window-choice justification "
        "+ blocked-per-phase reads explicit).",
        "- **Shared utilities**: "
        "[`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-"
        "drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) "
        "(`compute_data_driven_block_length`, `stationary_bootstrap_ci`).",
        "- **Load-bearing cross-references** per handoff section 2.4: bb_overnight_gain_proxy.md "
        "coverage framing applied in Q3.5.j; HA10 R14 single-pool re-anchor (badd04a) descriptively "
        "corroborated in Q3.5.d; Q3.3 bb_lowest sister-channel rho reproduced + extended in Q3.5.e; "
        "sister-channel E[L]\\* spread context in Q3.5.b. NO substantive HA verdict promotion per "
        "CONVENTIONS section 2.1.",
        "- **No causal claims, no falsification bar** per "
        "[CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).",
        "",
        "## Result",
        "",
        "Headline (see [`findings.md`](findings.md) for the full answers Q3.5.a-j):",
        "",
        "`bb_overnight_gain` on truth-only window is a **signed compound-difference channel** "
        "(skew={0:+.2f}, excess kurtosis={1:+.2f}, heavy_tail_flag={2}; share negative = {3:.1%}). "
        "**Data-driven E[L]\\*={4:.1f}** -- vs sister Strand-A channels stress_stdev_sleep 7.0 / "
        "stress_mean_sleep 12.6 / stress_low_motion 21.1 / bb_lowest 29.25 / all_day_stress_avg 29.8. "
        "**Per-phase trajectory on truth-coverage-restricted window**: consolidation median {5:.2f} "
        "-> afbouw {6:.2f} (the only fully-bracketed per-phase shift; unmedicated + buildup blocked "
        "by coverage per Q3.5.j load-bearing analysis). Episode-level Cohen's d="
        "{7:+.2f}; bootstrap CI95 [{8:+.2f}, {9:+.2f}]. **Q3.5.j load-bearing**: truth coverage "
        "starts {10}; proxy r=0.989 bridge 2024-07-08 to 2024-09-17 available as sensitivity but "
        "not adopted for primary per bb_overnight_gain_proxy.md discipline rule 2; truth-only window "
        "adopted for Q3.5.a-i headlines.".format(
            a.get("skewness", float("nan")), a.get("excess_kurtosis", float("nan")),
            a.get("heavy_tail_flag", False), a.get("share_negative", float("nan")),
            el_star, consol_med, afbouw_med,
            fe.get("cohens_d_episode_vs_normal_day", float("nan")),
            fe.get("bootstrap_ci95_mean_diff", [float("nan"), float("nan")])[0],
            fe.get("bootstrap_ci95_mean_diff", [float("nan"), float("nan")])[1],
            cov_truth.get("first_non_nan_date_full_corpus", "n/a"),
        ),
        "",
        "## Files",
        "",
        "- [`README.md`](README.md) -- this file",
        "- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + "
        "`README.md` + `plots/*.png`",
        "- [`findings.md`](findings.md) -- writeup covering Q3.5.a-j + tables (programmatically emitted "
        "by run.py from summary.json per the Q3.2/Q3.3/Q3.4 architectural note about the Write-tool "
        "harness heuristic on the literal filename \"findings\")",
        "- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per "
        "`docs/research/**/*.json`)",
        "- [`plots/`](plots/) -- 5 PNGs: distribution, phase-stratified violins, trajectory-with-"
        "phases, crash-vs-normal, ACF (gitignored per `docs/research/**/*.png`)",
        "",
        "## Status",
        "",
        "**Current as of 2026-06-24** (commit context: post-`39d7693` Tier 1 closed; Tier 2 first of "
        "5 = this bb_overnight_gain; next: resting_hr, exertion_class, push_burden_7d, gevoelscore).",
        "",
        "## Cross-references",
        "",
        "- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 "
        "2026-06-18, commit `ccbd12e`)",
        "- **LOAD-BEARING methodology MD**: "
        "[`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md) "
        "(coverage framing).",
        "- **Sister BB-channel analysis**: "
        "[`descriptive/operationalisation_support/bb_lowest/`](../bb_lowest/) -- Q3.3.k reciprocal "
        "bb_overnight_gain pair (rho ~+0.19 NOT near-identity); this Q3.5 reproduces from the gain "
        "side + extends to multi-resolution.",
        "- **R14 single-pool re-anchor**: "
        "[`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) "
        "-- HA10 row descriptively corroborated in Q3.5.d.",
        "- **Most-recent Strand-A precedent**: "
        "[`descriptive/operationalisation_support/stress_stdev_sleep/`](../stress_stdev_sleep/) -- "
        "Q3.4 (programmatic-emit pattern + clean f-string discipline).",
        "- **HA-* tests that this analysis anchors**:",
        "  - HA10 (LOCKED OVERALL-REFUTED; R14 single-pool NOT-SUPPORTED CONVERGE-ON-OVERALL); HA10 "
        "primary is bb_highest -- bb_overnight_gain is the sleep-recharge-arc primitive in Wiggers D2 "
        "form.",
        "- **Definitional substrate**: "
        "[`pipeline/01_extract/garmin_uds_extras.py`](../../../../pipeline/01_extract/garmin_uds_extras.py) "
        "(derivation: SLEEPEND - SLEEPSTART from UDS bodyBatteryStatList).",
        "- **Other methodology MDs**: `citalopram_phase_stratification.md`, "
        "`citalopram_dose_response_stress_mean_sleep.md` (v3 section 5.6 'partial' status), "
        "`permutation_null_block_length.md`, `garmin_indicators_audit.md`, "
        "`lc_era_temporal_segmentation.md`.",
        "- **Upstream pipeline**: `per_day_master.csv` <- "
        "`pipeline/03_consolidate/build_unified_dataset.py` <- "
        "`pipeline/01_extract/garmin_uds_extras.py`. `labels_crash_v2.csv` per locked "
        "`crash_v2-definition`.",
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
        raise RuntimeError(
            "{0} not found in master - check pipeline build".format(CHANNEL)
        )

    # Coverage-restricted analytic window per Q3.5.j: truth-only (2024-09-18+)
    # This is the load-bearing choice per bb_overnight_gain_proxy.md
    truth_start_ts = pd.Timestamp(TRUTH_START)
    s4_truth_window = s4.loc[
        (s4["date"] >= truth_start_ts) & s4[CHANNEL].notna()
    ].copy()
    # NOTE: also keep the full S4 frame for Q3.5.j coverage analysis +
    # Q3.5.h boundary-step reads that need pre/post 30d arrays
    s4_full = s4.copy()

    values_truth = s4_truth_window[CHANNEL].astype(float)

    summary = {
        "channel": CHANNEL,
        "as_of_date": AS_OF_DATE,
        "stratum_4_start": "2022-09-03",
        "truth_window_start": str(TRUTH_START),
        "proxy_window_start": str(PROXY_START),
        "analytic_window_used": "truth-only (2024-09-18+)",
        "n_rows_stratum_4_total": int(len(s4_full)),
        "n_rows_truth_window": int(len(s4_truth_window)),
        "n_rows_with_channel": int(values_truth.notna().sum()),
        "labelling_scheme": "crash_v2 (labels_crash_v2.csv, label=='crash')",
        "source_file_master": "per_day_master.csv",
        "source_file_crash_labels": "labels_crash_v2.csv",
        "phase_axis_source": "methodology/citalopram_phase_stratification.md section 3",
        "coverage_anchor": "methodology/bb_overnight_gain_proxy.md (LOAD-BEARING)",
        "questions": {},
    }

    # Q3.5.a-i operate on the truth-only analytic window
    summary["questions"]["Q3.5.a_distribution"] = q_a_distribution(values_truth)
    summary["questions"]["Q3.5.b_autocorrelation"] = q_b_autocorrelation(values_truth)
    per_phase = q_c_base_rates_per_phase(s4_full, CHANNEL)
    summary["questions"]["Q3.5.c_base_rates_per_phase"] = per_phase
    summary["questions"]["Q3.5.d_phase_stratified_distribution"] = q_d_phase_stratified(per_phase, CHANNEL)
    summary["questions"]["Q3.5.e_near_identity"] = q_e_near_identity(s4_truth_window, CHANNEL)
    summary["questions"]["Q3.5.f_crash_vs_normal"] = q_f_crash_vs_normal(s4_truth_window, CHANNEL)
    summary["questions"]["Q3.5.g_spike_primitive"] = q_g_spike_primitive(s4_truth_window, CHANNEL)
    summary["questions"]["Q3.5.h_outliers_calibration"] = q_h_outliers_calibration(s4_truth_window, CHANNEL)
    summary["questions"]["Q3.5.i_covariate_readiness"] = q_i_covariate_readiness(s4_truth_window, CHANNEL)
    # Q3.5.j operates on the FULL master + full S4 (for coverage analysis)
    summary["questions"]["Q3.5.j_coverage"] = q_j_coverage(master, s4_full, CHANNEL)

    plot_files = make_plots(s4_truth_window, CHANNEL, HERE / "plots")
    summary["plots"] = plot_files

    out_path = HERE / "summary.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    # Emit findings.md and README.md as programmatic outputs (per the Q3.2/
    # Q3.3/Q3.4 precedent session's architectural note about the Write-tool
    # harness heuristic on the literal filename "findings").
    write_findings_md(summary, HERE / "findings.md")
    write_readme_md(summary, HERE / "README.md")

    print("Wrote {0}".format(out_path))
    print("Plots: {0}".format(plot_files))
    print("\n--- HEADLINE ---")
    a = summary["questions"]["Q3.5.a_distribution"]
    b = summary["questions"]["Q3.5.b_autocorrelation"]
    fr = summary["questions"]["Q3.5.f_crash_vs_normal"]
    j = summary["questions"]["Q3.5.j_coverage"]
    print("Q3.5.a n={0} mean={1:.2f} median={2:.2f} MAD={3:.2f} skew={4:.2f} "
          "heavy_tail={5} share_neg={6:.1%}".format(
              a.get("n", 0), a.get("mean", float("nan")), a.get("median", float("nan")),
              a.get("mad_unscaled", float("nan")), a.get("skewness", float("nan")),
              a.get("heavy_tail_flag", False), a.get("share_negative", float("nan"))
          ))
    print("Q3.5.b E[L]*={0:.2f} (default 7); factor-of-2 flag={1}; M={2}".format(
        b["data_driven_E_L_star"], b["factor_of_2_deviation_flag"], b["cutoff_lag_M"]
    ))
    pp = summary["questions"]["Q3.5.c_base_rates_per_phase"]
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        if pp.get(ph, {}).get("n", 0) > 0:
            print("  Q3.5.c phase {0}: n={1} med={2:.2f} MAD={3:.2f}".format(
                ph, pp[ph]["n"], pp[ph]["median"], pp[ph]["mad_unscaled"]
            ))
        else:
            print("  Q3.5.c phase {0}: n=0 (coverage gap)".format(ph))
    pd_d = summary["questions"]["Q3.5.d_phase_stratified_distribution"]
    print("Q3.5.d phase-to-phase median shifts:")
    for k_label, v in pd_d["phase_to_phase_shifts"].items():
        print("  {0}: {1:+.2f}".format(k_label, v))
    fl = fr.get("day_level", {})
    if fl:
        e7 = fl.get("stationary_bootstrap_E_L7", {})
        eS = fl.get("stationary_bootstrap_E_L_star", {})
        print("Q3.5.f day-level: n_crash={0} n_normal={1} d={2:.2f}".format(
            fl.get("n_crash_day", 0), fl.get("n_normal_day", 0), fl.get("cohens_d", float("nan"))
        ))
        print("  E[L]=7  CI=[{0:.2f}, {1:.2f}]".format(
            e7.get("ci_lower", float("nan")), e7.get("ci_upper", float("nan"))
        ))
        print("  E[L]*={0} CI=[{1:.2f}, {2:.2f}]".format(
            eS.get("block_length_used", 0), eS.get("ci_lower", float("nan")), eS.get("ci_upper", float("nan"))
        ))
        mwu = fl.get("mann_whitney_u", {})
        print("  Mann-Whitney U: z={0:.2f} p={1}".format(
            mwu.get("z", float("nan")), _format_p(mwu.get("p_two_sided", float("nan")))
        ))
    fe = fr.get("episode_level", {})
    if fe:
        print("Q3.5.f episode-level: n_ep={0} d={1:.2f} CI={2}".format(
            fe.get("n_crash_episodes", 0),
            fe.get("cohens_d_episode_vs_normal_day", float("nan")),
            fe.get("bootstrap_ci95_mean_diff", "n/a"),
        ))
    e_near = summary["questions"]["Q3.5.e_near_identity"]
    print("Q3.5.e near-identity flagged: {0}".format(e_near["flagged_pairs"]))
    bb_lo_multi = e_near.get("bb_lowest_multires_extension")
    if bb_lo_multi:
        raw = bb_lo_multi["raw_daily"]
        print("Q3.5.e bb_lowest raw daily: rho={0:+.3f} (Q3.3 reciprocal ~+0.19)".format(
            raw["spearman_rho"]
        ))
    cov_t = j["truth_channel"]
    print("Q3.5.j truth: first={0} n={1} ({2:.2f}% of corpus)".format(
        cov_t["first_non_nan_date_full_corpus"], cov_t["n_non_nan_full_corpus"],
        cov_t["share_of_full_corpus_pct"]
    ))


if __name__ == "__main__":
    main()

