"""Descriptive analysis: push_burden_7d operationalisation support.

Answers Q3.8.a-i per the locked descriptive programme:
``docs/research/analyses/descriptive/README.md`` section 3.4 (template
a-i applied to this channel; HA-touched non-confirmed candidate list
bullet "exertion_class + push_burden_7d (HA01b/HA01c primaries) --
partially covered by activity-labels/"; explicit acknowledgment in
section 3.4 of "push_burden's rolling-baseline contamination"). This
is the **4th of the 5 Tier 2 channels** in the user-prioritised
Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5
bb_overnight_gain `7d49ba4`; Tier 2 2nd = Q3.6 resting_hr `5d28219`;
Tier 2 3rd = Q3.7 exertion_class `9b03bed`; this Q3.8 closes Tier 2
4th; next: Q3.9 gevoelscore -- dispatched in parallel).

Channel: per-day push-burden count (7-day window) on the v3.2 lagged
baseline. Per the operand-availability reality on
``per_day_master.csv``: the v3.1 un-lagged ``push_burden_7d`` column
was DROPPED from the master per
``methodology/garmin_indicators_audit.md`` audit 2026-06-11 item 2
("push_burden_7d dropped from the master ... known rolling-baseline
contamination"). The v3.2 lagged variant ``push_burden_7d_lagged``
(with the ``[d-90, d-30]`` baseline window per CONVENTIONS section 3.2)
IS present in the master and IS the channel HA02c actually tested
(per REJECTED.md HA02c row: "Push burden on Theme A lagged baseline").
This Q3.8 is on ``push_burden_7d_lagged``. Integer-valued; bounded
support 0-6; range = count of push-days in the trailing-7-day window
above the v3.2 lagged baseline.

**CONVENTIONS section 3.2 / audit-MD contradiction surfaced per
[[feedback_flag_contradictions]]**: CONVENTIONS section 3.2 states
v3.1 ``push_burden_7d`` "stays in the master for backward
compatibility with HA01b / HA02c". The audit MD 2026-06-11 item 2
explicitly removed it from
``pipeline/03_consolidate/build_unified_dataset.py``. The pipeline-
side reality (column absent in master) is what binds this Q3.8;
CONVENTIONS section 3.2 needs a stocktake refresh to reflect the
audit drop. Not re-litigated here per handoff section 3.

Channel substantive status (per handoff section 1 + REJECTED.md):
- HA02c primary operand on the v3.2 lagged baseline; LOCKED REFUTED
  both eras (train -18.7 pp / validate +0.7 pp per
  activity-labels/output/ha_results_4day_lagged.md; NULL in
  REJECTED.md row HA02c). The lagged-baseline correction improved the
  measurement standing but does NOT resurrect push_burden as a
  predictor.
- Sister channel to Q3.7 exertion_class (just LANDED `9b03bed`); both
  are activity-labels-family v3.1 -> v3.2 lagged-baseline corrected.
  HA01b-recomputed family R14 single-pool result (+5.1 pp [CI -14.7,
  +13.3] perm p=0.3689 NOT-SUPPORTED CONVERGE; `badd04a`) is the
  closest single-pool re-anchor neighbour; HA02c itself was NOT in
  the R14 single-pool re-anchor stretch list per
  single_pool_reanchor/findings.md.
- v3.1 -> v3.2 lagged-baseline correction is the canonical project
  example per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed
  + descriptive README section 3.4 explicit acknowledgment of
  "push_burden's rolling-baseline contamination". Q3.8.b cites
  descriptively per handoff section 2.4; NOT re-litigated.

Continuous-channel template (parity with sister continuous channels
Q3.5 bb_overnight_gain + Q3.6 resting_hr; integer-valued bounded
support 0-6 means heavy-tail flag is False but mean/median/MAD/
quantiles apply identically): standard Cohen's d primary, no
zero-rate column. Q3.8.e near-identity check includes Q3.7 sibling
exertion_class via Spearman on ordinal-vs-numeric per handoff
section 2.4.

Output: ``summary.json`` (machine-readable per-question results) +
``plots/*.png`` (visualisations) + ``findings.md`` + ``README.md``
(programmatically emitted from this script per the Q3.2/Q3.3/Q3.4/
Q3.5/Q3.6/Q3.7 precedent session's architectural note about the
Write-tool harness heuristic on the literal filename "findings").

Discipline guards (per CONVENTIONS):
- section 2.1 descriptive-before-inference: no causal claims; no
  falsification bar; no HA verdict promotion (HA02c REJECTED + HA01b-
  recomputed REJECTED + R14 HA01b-recomputed NOT-SUPPORTED LOCKED
  and NOT extended here; NO v3.1 -> v3.2 correction re-litigation).
- section 3.1 personal baseline: distribution shape reported as-is;
  phase-stratified to surface citalopram threshold confound where
  observable.
- section 3.2 lagged-baseline discipline: this Q3.8 analyses the
  v3.2 ``push_burden_7d_lagged`` column directly (the v3.1 un-lagged
  variant being absent from master per audit MD). Q3.8.b cites the
  v3.1 -> v3.2 correction descriptively per handoff section 2.4.
- section 3.3 column-duplication: near-identity check at |rho|>=0.92.
- section 3.4 crash-drop sensitivity: |Delta|>0.10 flag surfaced.
- section 3.5 spike metrics: push_burden_7d_lagged IS itself a count
  primitive (count of push-days in trailing 7d above lagged
  baseline); the channel IS a within-7d burden spike construct per
  Q3.8.g.
- section 3.6 named counts: every count reports scheme + unit +
  source.
- section 4.1 + section 4.2: no a-priori claims; observed phase
  shifts framed as descriptive observation only.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date
from pathlib import Path
from math import erf, sqrt

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
# HERE = .../analyses/descriptive/operationalisation_support/push_burden_7d
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


# Channel as it actually appears in master per per_day_master.csv inspection.
# Un-lagged ``push_burden_7d`` was dropped per audit MD 2026-06-11 item 2.
CHANNEL = "push_burden_7d_lagged"
CHANNEL_LCERA = "push_burden_7d_lagged_lcera"  # alternate variant for Q3.8.e cross-check
CHANNEL_DISPLAY = "push_burden_7d (v3.2 lagged)"
AS_OF_DATE = "2026-06-05"  # parity with R14 + Q3.1-Q3.7 prior Strand-A analyses

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
# Q3.8.a Distribution shape
# ---------------------------------------------------------------------------


def q_a_distribution(values: pd.Series) -> dict:
    """Distribution shape on Stratum 4 (Q3.8.a)."""
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
    # push_burden_7d_lagged is integer-valued count in [0, 6]; heavy_tail rule
    # per CONVENTIONS section 3.1: skew > 1 OR p99/median > 3.0. For a bounded
    # integer count the p99/median ratio is the binding term; heavy_tail_flag
    # is reported but the upper-bound semantics differ from continuous channels.
    safe_p99_over_med = quantiles["p99"] / median if median > 0 else float("nan")
    heavy_tail = bool(
        (safe_p99_over_med > 3.0 if safe_p99_over_med == safe_p99_over_med else False)
        or skewness > 1.0
    )
    m4 = float((centered ** 4).mean())
    excess_kurtosis = m4 / (m2 ** 2) - 3.0 if m2 > 0 else float("nan")
    # Per-value frequency table for the bounded integer support
    value_counts = v.astype(int).value_counts().sort_index()
    per_value = {int(k): int(value_counts.get(k, 0)) for k in range(0, 8)}
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
        "is_integer_valued": True,
        "bounded_support": [0, 6],
        "per_value_counts": per_value,
        "fraction_at_zero": float((v == 0).sum() / n) if n > 0 else float("nan"),
        "fraction_above_4": float((v >= 4).sum() / n) if n > 0 else float("nan"),
    }


# ---------------------------------------------------------------------------
# Q3.8.b Autocorrelation + E[L]* + v3.1 -> v3.2 lagged-baseline citation
# ---------------------------------------------------------------------------


def q_b_autocorrelation(values: pd.Series) -> dict:
    """Autocorrelation structure + E[L]* (Q3.8.b).

    Per handoff section 2.4 + CONVENTIONS section 3.2: this autocorrelation
    discussion descriptively cites the v3.1 -> v3.2 lagged-baseline correction
    (REJECTED.md HA01b-recomputed row + descriptive README section 3.4 explicit
    "push_burden's rolling-baseline contamination" acknowledgment). NOT
    re-litigated per handoff section 3 hard constraint.
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
        "v3_1_to_v3_2_lagged_baseline_correction_citation": {
            "summary": (
                "The v3.1 push_burden_7d used a 30-day TRAILING rolling "
                "baseline that included the candidate day; in sustained-push "
                "periods the baseline crept up with the pushes (the channel "
                "rebased into its own reference frame and stopped looking "
                "heavy). v3.2 fixes this with a [d-90, d-30] window (the "
                "_lagged variant in master). The v3.1 -> v3.2 correction "
                "softened the original HA01b validate +17.3 pp 'first "
                "SUPPORTED' headline by -13.3 pp to +4.0 pp; the original "
                "headline was substantially a baseline-construction "
                "artefact. Per CONVENTIONS section 3.2: 'if a draft analysis "
                "touches exertion_class, step_z_30d, push_burden_7d, or any "
                "non-lagged rank, stop and ask whether the v3.2 lagged "
                "variant is what's meant.' This Q3.8 analyses the v3.2 "
                "lagged variant directly (the v3.1 un-lagged version being "
                "absent from master per audit MD 2026-06-11 item 2)."
            ),
            "v3_1_v3_2_outcome_for_HA01b": "REJECTED.md HA01b-recomputed row: train +5.8 / validate +4.0 (both eras refuted on v3.2)",
            "v3_1_v3_2_outcome_for_HA02c": "REJECTED.md HA02c row: train -18.7 / validate +0.7 (both eras refuted on v3.2; this Q3.8's channel)",
            "descriptive_readme_acknowledgment": (
                "descriptive README section 3.4 explicitly names "
                "'push_burden's rolling-baseline contamination' as a "
                "load-bearing methodological example"
            ),
            "audit_md_drop": (
                "garmin_indicators_audit.md audit 2026-06-11 item 2: "
                "'push_burden_7d dropped from the master ... known rolling-"
                "baseline contamination'; only the v3.2 _lagged variant is "
                "present in master (Q3.8 channel)"
            ),
            "framing": (
                "Per handoff section 3 hard constraint: descriptive citation "
                "ONLY; the v3.2 lagged-baseline correction story is LOCKED at "
                "the CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed + "
                "HA02c + audit MD level. This Q3.8.b autocorrelation reading "
                "is on the v3.2 column; no re-litigation."
            ),
        },
        "sister_channel_E_L_spread_per_handoff_2_4": {
            "stress_stdev_sleep": 7.0,
            "bb_overnight_gain": 6.5,
            "stress_mean_sleep": 12.6,
            "stress_low_motion_min_count_S60_Mlow": 21.1,
            "bb_lowest": 29.25,
            "all_day_stress_avg": 29.8,
            "resting_hr_fallback": 7.0,
            "exertion_class_ordinal": 7.0,
            "note": (
                "per handoff section 2.4: resting_hr 'fallback-to-7 very-long'; "
                "exertion_class 7.0 (ordinal); push_burden_7d_lagged "
                "data-driven E[L]* per this Q3.8.b is reported alongside "
                "(integer-count, lagged-baseline-corrected v3.2; comparison "
                "is descriptive)."
            ),
        },
    }


# ---------------------------------------------------------------------------
# Q3.8.c Base rates per phase (citalopram axis)
# ---------------------------------------------------------------------------


def q_c_base_rates_per_phase(df: pd.DataFrame, channel: str) -> dict:
    """Per-phase n + median + dispersion (Q3.8.c, citalopram axis)."""
    out = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))
        sub = df.loc[mask, channel].dropna().astype(float)
        if len(sub) == 0:
            out[phase_name] = {"n": 0}
            continue
        med = float(sub.median())
        # Fraction at zero (no-push days) and at top of bounded support
        frac_zero = float((sub == 0).sum() / len(sub))
        frac_high = float((sub >= 4).sum() / len(sub))
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
            "fraction_at_zero": frac_zero,
            "fraction_above_4": frac_high,
        }
    return out


# ---------------------------------------------------------------------------
# Q3.8.d Phase-stratified distribution
# ---------------------------------------------------------------------------


def q_d_phase_stratified(per_phase: dict, channel: str) -> dict:
    """Phase-stratified distribution + descriptive shift report (Q3.8.d).

    Per CONVENTIONS section 4.2: observed shifts are Layer 1 descriptive
    observations only. push_burden_7d is NOT in v3 multi-channel sweep scope
    (the v3 sweep is on the autonomic-load + cardiovascular channels per
    citalopram_dose_response_stress_mean_sleep.md section 5.6: 6-channel
    scope = stress_mean_sleep + all_day_stress_avg + bb_lowest + resting_hr
    + bb_overnight_gain + respiration_avg_sleep; activity-labels family is
    not in that scope), so there is no v3 verdict to descriptively cite at
    this section. The HA02c + HA01b-recomputed REJECTED verdicts apply at
    the substantive Wiggers-test level and are LOCKED and NOT extended here.
    """
    out = {"phase_medians": {}, "phase_to_phase_shifts": {}, "phase_fraction_at_zero": {}}
    medians = {}
    for phase_name in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = per_phase.get(phase_name, {})
        if info.get("n", 0) > 0:
            medians[phase_name] = info["median"]
            out["phase_medians"][phase_name] = info["median"]
            out["phase_fraction_at_zero"][phase_name] = info["fraction_at_zero"]

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
        "v3_scope_note": (
            "push_burden_7d is NOT in the v3 multi-channel sweep scope "
            "(citalopram_dose_response_stress_mean_sleep.md section 5.6 "
            "6-channel scope: stress_mean_sleep + all_day_stress_avg + "
            "bb_lowest + resting_hr + bb_overnight_gain + "
            "respiration_avg_sleep). Activity-labels family channels "
            "(exertion_class + push_burden) are not in the v3 sweep."
        ),
        "framing": (
            "Per CONVENTIONS section 4.2 (caveats yes; a-priori claims no): "
            "observed phase shifts on push_burden_7d_lagged are Layer 1 "
            "descriptive observations only. No v3 verdict exists to cite "
            "or re-promote on this channel. HA02c (the Wiggers test on "
            "this channel) is LOCKED REFUTED per REJECTED.md."
        ),
    }

    out["ha02c_ha01b_xref"] = {
        "ha02c_locked_verdict": (
            "REJECTED both eras (train -18.7 pp / validate +0.7 pp); "
            "push burden on Theme A lagged baseline; the lagged-baseline "
            "correction improved measurement standing but did NOT "
            "resurrect push_burden as a predictor"
        ),
        "ha02c_primary_operand": "push burden in trailing 7-day window vs Theme A v3.2 lagged baseline; this Q3.8 channel",
        "ha02c_r14_status": "HA02c was NOT in the R14 single-pool re-anchor stretch list per single_pool_reanchor/findings.md; the HA01b-recomputed sister family WAS in R14 scope (see below)",
        "ha01b_recomputed_locked_verdict": (
            "REJECTED both eras (train +5.8 pp / validate +4.0 pp); v3.2 "
            "lagged composite at exertion_class_lagged in {heavy, "
            "very_heavy}; the v3.1 validate +17.3 pp 'first SUPPORTED' "
            "headline softened by -13.3 pp on v3.2 recomputation"
        ),
        "ha01b_recomputed_r14_single_pool_disc_pp": +5.1,
        "ha01b_recomputed_r14_single_pool_ci95": [-14.7, +13.3],
        "ha01b_recomputed_r14_single_pool_perm_p": 0.3689,
        "ha01b_recomputed_r14_verdict": "NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED); badd04a",
        "ha02c_source": "REJECTED.md HA02c row + activity-labels/output/ha_results_4day_lagged.md",
        "ha01b_recomputed_source": "REJECTED.md HA01b-recomputed row + Q3.7 exertion_class findings.md Q3.7.f cross-reference",
        "r14_source": "descriptive/operationalisation_support/single_pool_reanchor/findings.md (HA01b-recomputed row present; HA02c row absent)",
    }
    return out


# ---------------------------------------------------------------------------
# Q3.8.e Near-identity check (handoff section 2.4: include exertion_class
# sibling activity primitive via Spearman on ordinal-vs-numeric)
# ---------------------------------------------------------------------------

NEAR_IDENTITY_THRESHOLD = 0.92  # CONVENTIONS section 3.3
CATEGORY_ORDER = ["none", "light", "moderate", "heavy", "very_heavy"]
CATEGORY_TO_ORDINAL = {c: i for i, c in enumerate(CATEGORY_ORDER)}


def q_e_near_identity(df: pd.DataFrame, channel: str) -> dict:
    """Near-identity check vs activity-axis sibling channels (Q3.8.e).

    Targets per descriptive README section 3.4 template + handoff section 2.4
    (sister-channel near-identity to Q3.7 exertion_class via Spearman on
    ordinal-vs-numeric is load-bearing).
    """
    targets = [
        # Activity-labels family v3.2 lagged
        "exertion_class_lagged",
        "exertion_class_lagged_lcera",
        "eff_exertion_rank_lagged",
        "eff_exertion_rank_lagged_lcera",
        "exertion_rank_composite_lagged",
        "exertion_rank_composite_lagged_lcera",
        "push_burden_7d_lagged_lcera",  # _lcera sibling of this channel
        # Activity primitives upstream
        "exertion_class",  # un-lagged ordinal (in master per Q3.7)
        "effective_exertion_min",
        "effective_exertion_slope_28d",
        # Sister stress-family CONFIRMED-citalopram channels for cross-check
        "stress_mean_sleep",
        "all_day_stress_avg",
        "stress_low_motion_min_count_S60_Mlow",
        "stress_stdev_sleep",
        # Sister cardiovascular family
        "resting_hr",
        "bb_overnight_gain",
        "bb_lowest",
        # Sleep
        "respiration_avg_sleep",
    ]
    rows = []
    flags = []
    # Handle the Q3.7 sister specifically: exertion_class is categorical;
    # encode to ordinal for Spearman per handoff section 2.4 ("Spearman on
    # ordinal-vs-numeric").
    for t in targets:
        if t not in df.columns:
            rows.append({"channel": t, "note": "column absent"})
            continue
        col_t = df[t]
        is_categorical_t = not pd.api.types.is_numeric_dtype(col_t)
        if is_categorical_t:
            # Q3.7 exertion_class is the canonical case: ordinal encode
            encoded = col_t.map(CATEGORY_TO_ORDINAL)
            sub = pd.DataFrame({channel: df[channel], "encoded_t": encoded}).dropna()
            if len(sub) < 30:
                rows.append({"channel": t, "n": int(len(sub)), "note": "n<30 - skipped"})
                continue
            # Spearman is the load-bearing comparison for ordinal-vs-numeric
            spear = float(sub[channel].corr(sub["encoded_t"], method="spearman"))
            pear = float(sub[channel].corr(sub["encoded_t"]))  # auxiliary; valid since both numeric after encoding
            flagged = max(abs(pear), abs(spear)) >= NEAR_IDENTITY_THRESHOLD
            rows.append({
                "channel": t,
                "n": int(len(sub)),
                "pearson_r": pear,
                "spearman_rho": spear,
                "near_identity_flag": flagged,
                "encoding_note": "Q3.7 sibling exertion_class ordinal-encoded per CATEGORY_ORDER; Spearman is the load-bearing comparison per handoff section 2.4",
            })
            if flagged:
                flags.append(t)
            continue
        # Standard numeric near-identity check
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
            "Sister Q3.7 exertion_class (just LANDED `9b03bed`) reciprocally "
            "reported a Spearman on its ordinal encoding vs numeric activity-"
            "axis siblings; this Q3.8.e flips the side and reports Spearman "
            "of push_burden_7d_lagged (numeric count) vs the exertion_class "
            "ordinal encoding per handoff section 2.4. The Q3.8 channel and "
            "its _lcera variant share the same v3.2 lagged-baseline ancestry "
            "and SHOULD be near-identical (different LC-era restriction on "
            "the baseline window only). Cross-family checks against "
            "autonomic-load + cardiovascular channels are expected to be "
            "modest at most."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.8.f Crash-day vs normal-day (Stratum 4) + REJECTED.md HA02c xref
# ---------------------------------------------------------------------------


def _mann_whitney_u(crash_vals: np.ndarray, normal_vals: np.ndarray) -> dict:
    """Compute Mann-Whitney U with normal approximation + tie correction.

    Returns U, z, p (two-sided), P(crash > normal). Vendored to avoid a
    hard scipy dependency; same implementation as resting_hr/run.py.
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
    """Crash-vs-normal Cohen's d + Mann-Whitney U + crash-drop sensitivity
    (Q3.8.f).

    Per handoff section 2.4: this descriptively re-anchors the HA02c locked
    REFUTED both eras + REJECTED.md HA02c NULL outcome at the raw-channel
    distribution level. NOTE: HA02c's tested operand is the per-window
    second-order count primitive (push burden in trailing 7d vs Theme A
    lagged baseline); the Q3.8 channel (push_burden_7d_lagged) IS that
    operationalisation substrate. The HA01b-recomputed family R14 single-
    pool result (sister activity-axis channel; +5.1 pp NOT-SUPPORTED
    CONVERGE per single_pool_reanchor/findings.md) is the closest single-
    pool diagnostic neighbour since HA02c itself was not in R14 stretch
    list.
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
                "note": "data-driven from Q3.8.b; rounded to nearest integer",
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
        "ha02c_ha01b_cross_reference": {
            "ha02c_tested_operand": "push burden in trailing 7-day window vs Theme A v3.2 lagged baseline; this Q3.8 channel = the substrate",
            "ha02c_locked_train_disc_pp": -18.7,
            "ha02c_locked_validate_disc_pp": +0.7,
            "ha02c_locked_overall_verdict": "REJECTED both eras (REJECTED.md HA02c row)",
            "ha02c_r14_status": "NOT in R14 single-pool re-anchor stretch list (single_pool_reanchor/findings.md HA02c row absent); the descriptive cross-reference here is on the REJECTED.md locked verdict only",
            "ha01b_recomputed_r14_single_pool_disc_pp": +5.1,
            "ha01b_recomputed_r14_single_pool_ci95": [-14.7, +13.3],
            "ha01b_recomputed_r14_single_pool_perm_p": 0.3689,
            "ha01b_recomputed_r14_verdict": "NOT-SUPPORTED CONVERGE (sister activity-axis family; closest R14 neighbour)",
            "ha02c_source": "REJECTED.md HA02c row + activity-labels/output/ha_results_4day_lagged.md",
            "ha01b_recomputed_source": "REJECTED.md HA01b-recomputed row + single_pool_reanchor/findings.md HA01b-recomputed row",
            "note": (
                "HA02c's tested operand IS this Q3.8 channel (push_burden_7d "
                "on v3.2 lagged baseline). Q3.8.f reports the day-level "
                "crash-vs-normal Cohen's d on the raw channel value as the "
                "descriptive-layer complement -- a first-order day-level "
                "view of the same construct HA02c tested at the spike-form "
                "Wiggers level. HA02c's REJECTED verdict is LOCKED and NOT "
                "extended here per CONVENTIONS section 4.2 + handoff section "
                "3 hard constraint; this Q3.8.f is descriptive corroboration "
                "of the channel signal at the day-distribution level."
            ),
        },
    }


# ---------------------------------------------------------------------------
# Q3.8.g Spike-detecting primitive availability
# ---------------------------------------------------------------------------


def q_g_spike_primitive(df: pd.DataFrame, channel: str) -> dict:
    """Spike-primitive availability for push_burden_7d_lagged (Q3.8.g).

    push_burden_7d_lagged is ITSELF a count primitive (count of push-days
    in trailing 7d window above the v3.2 lagged baseline). Per CONVENTIONS
    section 3.5 spike/peak/count metrics preference: this channel is the
    project's canonical sustained-push spike construct on the activity-
    axis. HA02c (REJECTED) is the substantive Wiggers test on this
    construct.
    """
    out = {
        "channel_resolution": (
            "per-day count (integer-valued, bounded support [0, 6]); "
            "value at day d = count of push-days within trailing 7d "
            "window [d-6, d] that exceed the v3.2 lagged baseline "
            "(window [d-90, d-30] per CONVENTIONS section 3.2)"
        ),
        "spike_or_continuous_form": (
            "COUNT primitive at the per-day resolution that IS itself a "
            "within-7d burden-spike construct on the activity axis; the "
            "channel value is the spike-form (count of recent push-above-"
            "baseline days) -- HA02c's tested operand IS this channel"
        ),
        "sub_daily_resolution_in_master": False,
        "spike_primitives_available_in_master": [],
        "latent_in_FIT_not_in_master": [
            "per-minute / per-second activity primitives (NOT in master; "
            "would require FIT-side extraction; activity-labels family is "
            "already a per-day aggregate by definition per "
            "activity-labels/definition.md)",
            "instantaneous exertion rate (NOT in master; HA-C4c uses "
            "exertion_class_lagged_lcera in {heavy, very_heavy} on T as "
            "a per-day heavy classifier instead)",
        ],
        "related_activity_axis_primitives_in_master": [],
        "note": (
            "Per CONVENTIONS section 3.5: spike/peak/count metrics "
            "preferred over daily means -- push_burden_7d_lagged IS a "
            "count primitive (count of push-days above lagged baseline "
            "in trailing 7d). The channel is itself the within-7d "
            "burden-spike construct on the activity axis. Per CONVENTIONS "
            "section 3.2: prefer the v3.2 _lagged variant over the v3.1 "
            "rolling-baseline variant (the latter is no longer in master "
            "per audit MD). HA02c (locked REJECTED) tested this exact "
            "channel at the spike-form Wiggers level; HA01b-recomputed "
            "tested the sister exertion_class_lagged {heavy, very_heavy} "
            "form at the same Wiggers level; both REJECTED both eras."
        ),
    }
    for c in (
        "exertion_class",
        "exertion_class_lagged",
        "exertion_class_lagged_lcera",
        "eff_exertion_rank_lagged",
        "eff_exertion_rank_lagged_lcera",
        "exertion_rank_composite_lagged",
        "push_burden_7d_lagged_lcera",
        "effective_exertion_min",
        "effective_exertion_slope_28d",
    ):
        if c in df.columns:
            n = int(df[c].notna().sum())
            out["spike_primitives_available_in_master"].append({"column": c, "n_non_nan": n})
    # Pairwise correlations to the activity-axis siblings
    for partner in ("exertion_class_lagged", "eff_exertion_rank_lagged", "push_burden_7d_lagged_lcera", "effective_exertion_slope_28d"):
        if partner in df.columns:
            col_p = df[partner]
            if not pd.api.types.is_numeric_dtype(col_p):
                # Ordinal-encode if categorical
                encoded = col_p.map(CATEGORY_TO_ORDINAL)
                d = pd.DataFrame({channel: df[channel], "p": encoded}).dropna()
            else:
                d = df[[channel, partner]].dropna()
                d = d.rename(columns={partner: "p"})
            if len(d) > 30:
                out[f"pearson_r_vs_{partner}"] = float(d[channel].corr(d["p"]))
                out[f"spearman_rho_vs_{partner}"] = float(d[channel].corr(d["p"], method="spearman"))
                out[f"n_pair_{partner}"] = int(len(d))
    return out


# ---------------------------------------------------------------------------
# Q3.8.h Outlier detection + calibration-drift check + activity-labels
#         partial-coverage cross-reference (handoff section 2.4)
# ---------------------------------------------------------------------------


def q_h_outliers_calibration(df: pd.DataFrame, channel: str) -> dict:
    """Outlier detection + calibration-drift check (Q3.8.h).

    MAD-based |z|>5 on Stratum 4. Reports flagged dates + drift snapshots.
    For an integer-valued bounded-support count primitive, outlier
    semantics differ from continuous channels: a value of 6 (the upper
    bound of the support) on a low-baseline phase IS not a sensor failure
    but a legitimate high-burden week; MAD-z is reported but the
    interpretation flags this. Per handoff section 2.4: activity-labels
    partial-coverage substrate is descriptively cross-referenced.
    """
    sub = df[["date", channel]].dropna().sort_values("date").reset_index(drop=True)
    v = sub[channel].astype(float)
    med = float(v.median())
    mad = float(np.median(np.abs(v - med)))
    spread = mad * 1.4826 if mad > 0 else float("nan")
    if spread and spread == spread:
        z = (v - med) / spread
        flagged_mask = z.abs() > 5
    else:
        z = pd.Series([], dtype=float)
        flagged_mask = pd.Series([], dtype=bool)
    flagged = sub.loc[flagged_mask].copy()
    if len(flagged) > 0:
        flagged["mad_z"] = z[flagged_mask]
        outliers = [
            {"date": str(r["date"].date()), "value": float(r[channel]), "mad_z": float(r["mad_z"])}
            for _, r in flagged.iterrows()
        ]
    else:
        outliers = []
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
        "outlier_rule": "MAD-based |z|>5 (z = (x - median) / (MAD * 1.4826)); count-primitive caveat in interpretation",
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
                "push_burden_7d_lagged is derived from the v3.2 lagged-"
                "baseline composite per activity-labels/definition.md + "
                "CONVENTIONS section 3.2 [d-90, d-30] window discipline; "
                "the master holds it as a daily integer count in [0, 6]"
            ),
            (
                "The v3.1 un-lagged push_burden_7d was DROPPED from the "
                "master per garmin_indicators_audit.md audit 2026-06-11 "
                "item 2 (known rolling-baseline contamination per "
                "descriptive README section 3.4 + CONVENTIONS section 3.2 "
                "audit hook); this Q3.8 channel IS the v3.2 fix"
            ),
            (
                "activity-labels partial-coverage precedent per "
                "garmin_exploration/activity-labels/ (existing primitive "
                "validation + visualisation); the per-day classification "
                "depends on Garmin's activity-labels family + steps + "
                "moderate-VPA per activity-labels/definition.md severity "
                "cutoffs (current state: cutoffs are NOT formally LOCKED; "
                "this Q3.8.h descriptively characterises the channel "
                "AS-IS under the current classifier definition)"
            ),
            (
                "The integer-valued bounded support [0, 6] means MAD-z "
                "outlier semantics interpret 'extreme' as the upper-bound "
                "value 6 (a week with 6 push-days above lagged baseline) "
                "-- this is a legitimate high-burden week, NOT a sensor "
                "failure; the n_flagged count above reports the rule "
                "output, not a sensor-failure count"
            ),
            (
                "Underlying sensor is Forerunner 245 Elevate V3 throughout "
                "the entire 2021-08-16 to present window -- no device "
                "change in the analytic window; the v3.2 lagged-baseline "
                "construction is the only intermediate transform between "
                "the raw activity primitives and this channel"
            ),
        ],
    }


# ---------------------------------------------------------------------------
# Q3.8.i Covariate-sensitivity readiness
# ---------------------------------------------------------------------------


def q_i_covariate_readiness(df: pd.DataFrame, channel: str) -> dict:
    """Covariate-sensitivity readiness (Q3.8.i).

    Per HA-P7 section 4.5.4 worked-example pattern. Names candidate
    covariates a future HA on push_burden_7d_lagged as predictor could
    add. Note that this channel is HA02c's primary operand and HA02c is
    LOCKED REFUTED; further HA pre-regs on this channel would be different
    operand variants (e.g. different window lengths, different baseline
    constructions, single-direction primitives).
    """
    cands = []
    # 1. exertion_class_lagged -- sister activity-axis spike-form
    excl_corr = None
    if "exertion_class_lagged" in df.columns:
        encoded = df["exertion_class_lagged"].map(CATEGORY_TO_ORDINAL)
        d = pd.DataFrame({channel: df[channel], "p": encoded}).dropna()
        if len(d) > 30:
            excl_corr = {
                "pearson_r": float(d[channel].corr(d["p"])),
                "spearman_rho": float(d[channel].corr(d["p"], method="spearman")),
                "n": int(len(d)),
                "encoding_note": "exertion_class_lagged ordinal-encoded per CATEGORY_ORDER"
            }
    cands.append({
        "covariate": "exertion_class_lagged ordinal (sister activity-axis spike-form per Q3.7)",
        "rationale": (
            "Per Q3.7 sister analysis: exertion_class_lagged is the heavy/"
            "very_heavy classifier substrate used by HA-C4c (locked PARTIAL); "
            "push_burden_7d_lagged is the count-of-push-days-above-baseline "
            "in a 7d window form. The covariate disambiguates: beta_channel "
            "attenuates -> the push_burden signal is shared with the within-"
            "day heavy/very_heavy classification (the count-form captures "
            "the same activity-axis information as the categorical form); "
            "beta_channel survives -> the count-of-push-days-in-7d carries "
            "windowed-burden information distinct from per-day class."
        ),
        "source": "Q3.7 exertion_class sister analysis cross-pair table",
        "observed_correlation_on_S4": excl_corr,
        "expected_effect": (
            "beta_channel attenuates if the within-7d count captures the "
            "same activity-axis information as the per-day class; "
            "beta_channel survives if the count-form carries windowed-"
            "burden information distinct from per-day class"
        ),
    })
    # 2. push_burden_7d_lagged_lcera -- LC-era-restricted baseline variant
    lcera_corr = None
    if "push_burden_7d_lagged_lcera" in df.columns:
        d = df[[channel, "push_burden_7d_lagged_lcera"]].dropna()
        if len(d) > 30:
            lcera_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "push_burden_7d_lagged_lcera (LC-era-restricted baseline variant)",
        "rationale": (
            "Per CONVENTIONS section 3.2: the _lcera variant restricts the "
            "[d-90, d-30] baseline to LC-era days only (>= 2022-04-04), so "
            "pre-LC and corona days don't dilute the reference. The covariate "
            "disambiguates: beta_channel attenuates -> the LC-era restriction "
            "doesn't add information; beta_channel survives -> the LC-era-"
            "specific baseline normalisation IS load-bearing. Default for "
            "PEM-pacing tests gated on lc_phase == 'lc' is the _lcera variant "
            "per CONVENTIONS section 3.2; any future HA on push_burden should "
            "pre-spec the _lcera variant as primary and the non-LC-restricted "
            "variant as secondary sensitivity arm."
        ),
        "source": "CONVENTIONS section 3.2 _lagged_lcera convention",
        "observed_correlation_on_S4": lcera_corr,
        "expected_effect": (
            "beta_channel attenuates if the baseline window choice (LC-era "
            "only vs all-days) doesn't matter at this corpus length; "
            "beta_channel survives if the LC-era-specific baseline shifts "
            "the signal materially"
        ),
    })
    # 3. effective_exertion_slope_28d -- trajectory covariate
    slope_corr = None
    if "effective_exertion_slope_28d" in df.columns:
        d = df[[channel, "effective_exertion_slope_28d"]].dropna()
        if len(d) > 30:
            slope_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "effective_exertion_slope_28d (28d activity-axis trajectory)",
        "rationale": (
            "Per the v3.2 lagged-composite landing per garmin_indicators_"
            "audit.md section 195: 'Lagged ranks composite + push_burden + "
            "slope landed in the v3.2'. The slope captures the within-28d "
            "trajectory of effective exertion; combining with push_burden "
            "(within-7d count above baseline) disambiguates whether 'push "
            "burden' is the binding signal vs the underlying trajectory. "
            "beta_channel attenuates -> the 7d count is largely the "
            "trajectory leading into the index window; beta_channel survives "
            "-> the window-specific count carries new information vs the "
            "monthly trend."
        ),
        "source": "garmin_indicators_audit.md v3.2 lagged-composite landing note",
        "observed_correlation_on_S4": slope_corr,
        "expected_effect": (
            "beta_channel attenuates if the 7d count is largely the 28d "
            "trajectory's residue; beta_channel survives if the windowed "
            "burden count is distinct from the longer-term slope"
        ),
    })
    # 4. resting_hr -- cross-family cardiovascular response covariate
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
        "covariate": "resting_hr (cross-family cardiovascular response anchor)",
        "rationale": (
            "Per Q3.6 sister analysis: resting_hr is the cardiovascular-"
            "recovery anchor; push_burden_7d_lagged is the activity-axis "
            "burden count. The covariate disambiguates: beta_channel "
            "attenuates -> the push-burden signal is shared with the "
            "post-burden cardiovascular response (push days carry elevated "
            "RHR); beta_channel survives -> the activity-axis burden count "
            "carries independent information beyond the cardiovascular "
            "response signature."
        ),
        "source": "Q3.6 resting_hr sister analysis cross-pair table",
        "observed_correlation_on_S4": rhr_corr,
        "expected_effect": (
            "beta_channel attenuates if push days carry shared cardiovascular "
            "response; beta_channel survives if the activity-axis count "
            "carries independent burden information"
        ),
    })
    return {
        "primary_use_case": (
            "Future HA pre-reg using push_burden_7d_lagged (or a variant) "
            "as predictor of a crash-related outcome (HA02c substantive "
            "verdict already LOCKED at REJECTED; further HAs can use "
            "different operand variants -- e.g. different window lengths, "
            "single-direction primitives, the _lcera variant -- without "
            "re-anchoring the HA02c-locked verdict)."
        ),
        "discipline_anchor": "HA-P7 hypothesis.md section 4.5.4 -- secondary-logistic-with-covariate pattern",
        "candidate_covariates": cands,
        "recommendation": (
            "Pre-spec all four covariates as secondary sensitivity arms. "
            "The exertion_class_lagged arm (covariate 1) is the sister "
            "activity-axis spike-form disambiguator -- since Q3.7 already "
            "characterised that channel, the covariate use here is "
            "diagnostic of within-vs-windowed activity-axis signal "
            "decomposition. The _lcera arm (covariate 2) is the baseline-"
            "window-choice diagnostic per CONVENTIONS section 3.2 "
            "convention. The slope arm (covariate 3) decomposes within-7d "
            "count vs 28d trajectory. The resting_hr arm (covariate 4) is "
            "the cross-family cardiovascular-response disambiguator."
        ),
    }


# ---------------------------------------------------------------------------
# Plot generation
# ---------------------------------------------------------------------------


def make_plots(df: pd.DataFrame, channel: str, out_dir: Path) -> list:
    """Generate the figures referenced from findings.md."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    written = []

    sub = df[["date", channel, "is_crash"]].dropna(subset=[channel])

    # Figure 1: Per-value frequency bar chart (integer-valued bounded support)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    vals = sub[channel].astype(int)
    value_counts = vals.value_counts().sort_index()
    ax.bar(value_counts.index, value_counts.values, color="#7faabd", edgecolor="white")
    ax.set_xlabel("push_burden_7d_lagged (count of push-days in trailing 7d above v3.2 lagged baseline)")
    ax.set_ylabel("days (Stratum 4)")
    n_label = int(vals.notna().sum())
    title = "push_burden_7d_lagged per-value frequency - Stratum 4, n={0}".format(n_label)
    ax.set_title(title)
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
    if len(keep) > 0:
        ax.violinplot(
            [phase_data[p] for p in keep],
            showmedians=True, widths=0.85,
        )
        ax.set_xticks(np.arange(1, len(keep) + 1))
        ax.set_xticklabels(keep)
    ax.set_ylabel("push_burden_7d_lagged (count)")
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
    ax.plot(sub_sorted["date"], sub_sorted[channel], color="#c5dae8", linewidth=0.6, alpha=0.6, label="daily")
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
    ax.set_ylabel("push_burden_7d_lagged (count)")
    ax.set_title("push_burden_7d_lagged - rolling 90d median + citalopram phases")
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
    bins = np.arange(-0.5, 7.5, 1.0)
    ax.hist(normal, bins=bins, color="#9dc1e0", alpha=0.7, label=n_normal_label, density=True)
    if len(crash) > 0:
        ax.hist(crash, bins=bins, color="#cc4949", alpha=0.55, label=n_crash_label, density=True)
        crash_med = float(crash.median())
        crash_med_label = "crash median={0:.1f}".format(crash_med)
        ax.axvline(crash_med, color="#7a1f1f", linestyle="--", label=crash_med_label)
    normal_med = float(normal.median())
    normal_med_label = "normal median={0:.1f}".format(normal_med)
    ax.axvline(normal_med, color="#264c75", linestyle="--", label=normal_med_label)
    ax.set_xlabel("push_burden_7d_lagged (count)")
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
    if len(arr) >= 30:
        acf_res = compute_data_driven_block_length(arr, default_block_length=7)
        acf = acf_res["autocorrelations"]
        fig, ax = plt.subplots(figsize=(8, 3.6))
        lags = np.arange(len(acf))
        ax.bar(lags, acf, width=0.7, color="#7faabd", edgecolor="white")
        ax.axhline(0, color="#222", linewidth=0.5)
        threshold = 2.0 * np.sqrt(np.log(len(arr)) / len(arr))
        thresh_label = "|rho|={0:.3f} (Politis-White 2-sigma)".format(threshold)
        ax.axhline(threshold, color="#cc4949", linestyle="--", linewidth=0.8, label=thresh_label)
        ax.axhline(-threshold, color="#cc4949", linestyle="--", linewidth=0.8)
        ax.set_xlabel("lag (days)")
        ax.set_ylabel("autocorrelation")
        title = "ACF - push_burden_7d_lagged (Stratum 4); E[L]*={0:.1f}, M={1}".format(
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


def _fmt_near_id_rows(rows_list: list) -> list:
    out = []
    for r in rows_list:
        if "pearson_r" in r:
            flag = "no" if not r["near_identity_flag"] else "**YES**"
            tag = ""
            if "encoding_note" in r:
                tag = " (ordinal-encoded)"
            out.append(
                "| `{0}`{4} | {1} | {2:+.3f} | {3:+.3f} | {5} |".format(
                    r["channel"], r["n"], r["pearson_r"], r["spearman_rho"], tag, flag
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
    a = q["Q3.8.a_distribution"]
    b = q["Q3.8.b_autocorrelation"]
    c = q["Q3.8.c_base_rates_per_phase"]
    d = q["Q3.8.d_phase_stratified_distribution"]
    e = q["Q3.8.e_near_identity"]
    fr = q["Q3.8.f_crash_vs_normal"]
    fl = fr["day_level"]
    fe = fr["episode_level"]
    g = q["Q3.8.g_spike_primitive"]
    h = q["Q3.8.h_outliers_calibration"]
    ic = q["Q3.8.i_covariate_readiness"]

    el_star = b["data_driven_E_L_star"]
    quant = a["quantiles"]
    skew = a["skewness"]
    p99 = quant["p99"]
    med = a["median"]
    p99_over_med_str = ("{0:.2f}".format(p99 / med) if med > 0 else "n/a (median=0)")

    e7 = fl["stationary_bootstrap_E_L7"]
    eS = fl["stationary_bootstrap_E_L_star"]
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
                "| {0} | {1} to {2} | {3} | **{4:.2f}** | {5:.2f} | {6:.2f} | {7:.2f} / {8:.2f} | {9:.1%} | {10:.1%} |".format(
                    ph, info["date_start"], info["date_end"], info["n"],
                    info["median"], info["mean"], info["mad_unscaled"],
                    info["p10"], info["p90"],
                    info["fraction_at_zero"], info["fraction_above_4"],
                )
            )

    afbouw_med = c.get("afbouw", {}).get("median", float("nan"))
    consol_med = c.get("consolidation", {}).get("median", float("nan"))
    buildup_med = c.get("buildup", {}).get("median", float("nan"))
    unmed_med = c.get("unmedicated", {}).get("median", float("nan"))
    buildup_minus_unmed = d["phase_to_phase_shifts"].get("buildup_minus_unmedicated_median", float("nan"))
    consol_minus_unmed = d["phase_to_phase_shifts"].get("consolidation_minus_unmedicated_median", float("nan"))
    afbouw_minus_consol = d["phase_to_phase_shifts"].get("afbouw_minus_consolidation_median", float("nan"))
    afbouw_minus_unmed = d["phase_to_phase_shifts"].get("afbouw_minus_unmedicated_median", float("nan"))

    ha_xref = d["ha02c_ha01b_xref"]
    fr_xref = fr["ha02c_ha01b_cross_reference"]

    sister_el_str = (
        "stress_stdev_sleep 7.0 / bb_overnight_gain 6.5 / stress_mean_sleep 12.6 "
        "/ stress_low_motion 21.1 / bb_lowest 29.25 / all_day_stress_avg 29.8 "
        "/ resting_hr 7.0 (fallback) / exertion_class 7.0 (ordinal)"
    )

    mwu_p_str = _format_p(mwu["p_two_sided"])

    # Memory class -- continuous bounded count primitive
    memory_class = (
        "autocorrelation-SPARSE-MEMORY" if el_star < 10 else
        "autocorrelation-MODERATE-MEMORY" if el_star < 20 else
        "autocorrelation-DENSE-MEMORY"
    )

    # Cross-channel near-identity flag for the Q3.7 sister + _lcera variant
    nice_flags_in_table = [r["channel"] for r in e["rows"] if r.get("near_identity_flag")]
    near_id_str = (
        "Zero" if not e["flagged_pairs"]
        else "{0} (expected: _lcera sibling; possibly exertion_class_lagged sibling)".format(len(e["flagged_pairs"]))
    )

    skew_class = (
        "right-skewed" if skew > 0.3 else
        "left-skewed" if skew < -0.3 else
        "roughly-symmetric"
    )

    out_lines = [
        "# Findings -- `push_burden_7d` operationalisation-support descriptive (Q3.8.a-i)",
        "",
        "**Channel**: `push_burden_7d_lagged` (HA02c primary operand; per-day count of "
        "push-days in trailing 7d window above the v3.2 lagged baseline; integer-valued "
        "bounded support [0, 6]; channel as it lives in master after audit MD "
        "2026-06-11 item 2 dropped the v3.1 un-lagged variant). Column semantics: "
        "activity-labels family per [`activity-labels/definition.md`](../../../analyses/garmin_exploration/activity-labels/definition.md) "
        "+ CONVENTIONS section 3.2 `[d-90, d-30]` lagged-baseline window.",
        "",
        "**Substantive context**: HA02c is LOCKED at REJECTED both eras (train -18.7 pp / "
        "validate +0.7 pp) per [`REJECTED.md`](../../../REJECTED.md) HA02c row + "
        "[`activity-labels/output/ha_results_4day_lagged.md`](../../../analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md). "
        "HA02c was NOT in the R14 single-pool re-anchor stretch list per "
        "[`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md); the closest "
        "single-pool diagnostic neighbour is the sister activity-axis HA01b-recomputed "
        "(R14 single-pool **+5.1 pp [CI -14.7, +13.3] perm p (E[L]=7) = 0.3689** "
        "NOT-SUPPORTED CONVERGE; `badd04a`). This Q3.8 is the Strand-A operationalisation-"
        "support backstop on the v3.2 lagged channel; the HA02c + HA01b-recomputed + R14 "
        "substantive verdicts are LOCKED and descriptively corroborated only.",
        "",
        "**v3.1 -> v3.2 lagged-baseline correction context**: per CONVENTIONS section 3.2 + "
        "REJECTED.md HA01b-recomputed + descriptive README section 3.4 explicit acknowledgment "
        "of 'push_burden's rolling-baseline contamination'. The v3.1 push_burden_7d used a "
        "30-day trailing rolling baseline that included the candidate day (in sustained-push "
        "periods the baseline crept up with the pushes; the channel rebased into its own "
        "reference frame). v3.2 fixes this with a `[d-90, d-30]` window (the `_lagged` "
        "variant in master). The v3.1 un-lagged `push_burden_7d` was DROPPED from master "
        "per [`garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) "
        "audit 2026-06-11 item 2 (known rolling-baseline contamination). Per CONVENTIONS "
        "section 4.2 caveat-class framing: this Q3.8 reports the v3.2 channel descriptively; "
        "it does **NOT re-litigate the v3.1 -> v3.2 correction** (handoff section 3 hard "
        "constraint).",
        "",
        "**CONVENTIONS section 3.2 / audit-MD contradiction** (surfaced per "
        "[[feedback_flag_contradictions]]): CONVENTIONS section 3.2 says v3.1 "
        "`push_burden_7d` 'stays in the master for backward compatibility with HA01b / "
        "HA02c'; audit MD 2026-06-11 item 2 explicitly removed it. The pipeline-side "
        "reality (column absent in master) binds this Q3.8; CONVENTIONS section 3.2 needs "
        "a stocktake refresh. NOT re-litigated here.",
        "",
        "**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to {0}). "
        "n={1} days with channel out of {2} Stratum 4 days "
        "({3} NaN days).".format(
            summary["as_of_date"], a["n"],
            summary["n_rows_stratum_4_total"],
            summary["n_rows_stratum_4_total"] - a["n"],
        ),
        "",
        "**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.4 (LOCKED "
        "2026-06-18 r3, commit `ccbd12e`) -- HA-touched non-confirmed channel candidate "
        "list bullet `exertion_class + push_burden_7d (HA01b/HA01c primaries) -- partially "
        "covered by activity-labels/`. **4th of the 5 Tier 2 channels** in the user-"
        "prioritised Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 "
        "bb_overnight_gain `7d49ba4`; Tier 2 2nd = Q3.6 resting_hr `5d28219`; Tier 2 3rd = "
        "Q3.7 exertion_class `9b03bed`; this Q3.8 closes Tier 2 4th; next: Q3.9 gevoelscore "
        "-- dispatched in parallel). Q3.8.a-i template applied per section 3.1 verbatim.",
        "",
        "**Sources**: `per_day_master.csv` (Garmin v3.2 activity-axis composite) + "
        "`labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with "
        "`crash-` episode-level per CONVENTIONS section 3.6).",
        "",
        "**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA "
        "verdict promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). "
        "HA02c + HA01b-recomputed (LOCKED) + R14 HA01b-recomputed single-pool re-anchor "
        "(LOCKED `badd04a`) cross-references in this analysis are **descriptive corroboration "
        "only**; the substantive verdicts live in those result.md / REJECTED.md rows and are "
        "NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). "
        "No v3.1 -> v3.2 correction re-litigation per the handoff section 3 hard constraint. "
        "Statistical hygiene anchors: section 3.1 (personal baseline), section 3.2 "
        "(lagged-baseline discipline -- this channel IS the v3.2 fix), section 3.3 "
        "(column-duplication threshold |rho|>=0.92), section 3.4 (crash-drop sensitivity "
        "|delta|>0.10), section 3.5 (spike metrics -- this channel IS a count primitive on "
        "the activity axis), section 3.6 (named counts).",
        "",
        "---",
        "",
        "## Headline",
        "",
        "`push_burden_7d_lagged` on Stratum 4 is an **integer-valued bounded-support [0, 6] "
        "{0} count primitive on the activity axis** (skew={1:+.2f}, excess kurtosis={2:+.2f}, "
        "heavy_tail_flag={3}, p99/median = {4:.2f}/{5:.2f} = {6}, fraction at 0 = {7:.1%}, "
        "fraction at >=4 = {8:.1%}). The **data-driven E[L]\\*={9:.1f}** (Politis-White; "
        "deviation ratio {10:.2f}; factor-of-2 flag = {11}; cutoff lag M={12}). Cross-channel "
        "context per handoff section 2.4: vs sister Strand-A channels {13}; push_burden_7d_"
        "lagged's E[L]\\*={9:.1f} sits in the **{14}** regime. **Phase-stratified medians** "
        "(citalopram axis): unmedicated {15:.2f} -> buildup {16:.2f} -> consolidation "
        "{17:.2f} -> afbouw {18:.2f} (consolidation-minus-unmedicated = {19:+.2f}). Day-"
        "resolved citalopram boundary step (2024-04-09 pre/post 30d) is **{20:+.2f}**. "
        "Crash-vs-normal: episode-level d={21:+.2f} (bootstrap CI95 [{22:+.2f}, {23:+.2f}]); "
        "day-level Mann-Whitney U z={24:+.2f} p={25} P(crash>normal)={26:.3f} -- descriptively "
        "re-anchors HA02c's locked REFUTED-both-eras outcome (REJECTED.md HA02c row) at the "
        "first-order day-level read (HA02c's tested operand IS this Q3.8 channel at the "
        "spike-form Wiggers level). Near-identity check: **{27}** at the |rho|>=0.92 "
        "CONVENTIONS section 3.3 threshold (the v3.2 _lcera sibling channel and possibly the "
        "exertion_class_lagged sister are the expected high-rho neighbours).".format(
            skew_class, skew, a["excess_kurtosis"], a["heavy_tail_flag"],
            p99, med, p99_over_med_str,
            a["fraction_at_zero"], a["fraction_above_4"],
            el_star, b["deviation_ratio"], b["factor_of_2_deviation_flag"], b["cutoff_lag_M"],
            sister_el_str, memory_class,
            unmed_med, buildup_med, consol_med, afbouw_med, consol_minus_unmed,
            citalo_step["diff_post_minus_pre"] if citalo_step.get("diff_post_minus_pre") is not None else float("nan"),
            fe["cohens_d_episode_vs_normal_day"], ci_ep[0], ci_ep[1],
            mwu["z"], mwu_p_str, mwu["p_crash_greater_than_normal"],
            near_id_str,
        ),
        "",
        "---",
        "",
        "## Q3.8.a -- Distribution shape (Stratum 4)",
        "",
        "`push_burden_7d_lagged` is an **integer-valued count primitive** with bounded "
        "support [0, 6] (per-day count of push-days in trailing 7d window above the v3.2 "
        "lagged baseline). For an integer-valued bounded-support channel the per-value "
        "frequency table is the load-bearing distribution descriptor; mean / median / MAD "
        "/ quantiles apply identically to the continuous-template precedent (Q3.5 / Q3.6) "
        "but the heavy-tail flag interpretation is bounded by the support ceiling.",
        "",
        "| stat | value | source |",
        "|---|---:|---|",
        "| n (Stratum 4) | {0} | `per_day_master.csv` `push_burden_7d_lagged` non-NaN within S4 |".format(a["n"]),
        "| mean | {0:.3f} | (single-pool S4) |".format(a["mean"]),
        "| median | {0:.3f} | |".format(a["median"]),
        "| std (ddof=1) | {0:.3f} | |".format(a["std_ddof1"]),
        "| MAD (unscaled) | {0:.3f} | |".format(a["mad_unscaled"]),
        "| MAD x 1.4826 (normal-equivalent SD) | {0:.3f} | for robust z-score scaling per section 3.1 |".format(a["mad_normal_equivalent"]),
        "| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | {0:.1f} / {1:.1f} / {2:.1f} / {3:.1f} / {4:.1f} / {5:.1f} / {6:.1f} / {7:.1f} / {8:.1f} | |".format(
            quant["p1"], quant["p5"], quant["p10"], quant["p25"], quant["p50"],
            quant["p75"], quant["p90"], quant["p95"], quant["p99"],
        ),
        "| skewness (Fisher-Pearson) | **{0:+.2f}** | {1} |".format(a["skewness"], skew_class),
        "| excess kurtosis (Fisher) | **{0:+.2f}** | |".format(a["excess_kurtosis"]),
        "| heavy_tail_flag | **{0}** | skew>1 OR p99/median > 3.0 (bounded support [0, 6] caps the upper tail) |".format(a["heavy_tail_flag"]),
        "| range | {0:.1f} to {1:.1f} | bounded by definition |".format(a["min"], a["max"]),
        "| fraction at 0 (no push in 7d) | **{0:.1%}** | the no-push fraction |".format(a["fraction_at_zero"]),
        "| fraction at >=4 (sustained push week) | **{0:.1%}** | the sustained-push fraction |".format(a["fraction_above_4"]),
        "",
        "### Per-value frequency table",
        "",
        "| value | n days | fraction |",
        "|---:|---:|---:|",
    ]
    total_n = a["n"]
    for v_int in sorted(a["per_value_counts"].keys()):
        n_v = a["per_value_counts"][v_int]
        if n_v > 0:
            frac = n_v / total_n if total_n > 0 else float("nan")
            out_lines.append("| {0} | {1} | {2:.1%} |".format(v_int, n_v, frac))
    out_lines.extend([
        "",
        "**push_burden_7d_lagged is a v3.2 lagged-baseline count primitive on the activity "
        "axis** (per-day count of push-days in trailing 7d window above the [d-90, d-30] "
        "lagged baseline). Distinct from the categorical sister Q3.7 exertion_class (5-level "
        "ordinal {none, light, moderate, heavy, very_heavy}) by aggregation: exertion_class "
        "is per-day classification; push_burden_7d_lagged is the within-7d count-of-push-"
        "above-baseline. The two channels share the activity-labels v3.2 family ancestry.",
        "",
        "### Cross-channel comparison vs sister continuous Strand-A channels",
        "",
        "| stat | push_burden_7d_lagged (this analysis) | resting_hr (Q3.6) | bb_overnight_gain (Q3.5) | stress_stdev_sleep (Q3.4) |",
        "|---|---:|---:|---:|---:|",
        "| n S4 | {0} | 1357 | 593 | 1337 |".format(a["n"]),
        "| mean | {0:.2f} | 56.68 | 16.65 | 7.18 |".format(a["mean"]),
        "| median | {0:.2f} | 56.00 | 16.00 | 6.00 |".format(a["median"]),
        "| MAD (unscaled) | {0:.2f} | 2.00 | 4.00 | 2.00 |".format(a["mad_unscaled"]),
        "| skewness | {0:+.2f} | +0.25 | +0.97 | +1.71 |".format(a["skewness"]),
        "| heavy_tail_flag | **{0}** | **False** | **False** | **True** |".format(a["heavy_tail_flag"]),
        "| type | **integer count [0, 6]** | continuous bpm | continuous BB units | continuous stress units |",
        "",
        "See [`plots/fig1_distribution_s4.png`](plots/fig1_distribution_s4.png).",
        "",
        "---",
        "",
        "## Q3.8.b -- Autocorrelation structure + E[L]\\* + v3.1 -> v3.2 correction citation",
        "",
        "The **data-driven block length is E[L]\\*={0:.1f}** (Politis-White 2004 with Patton-"
        "Politis-White 2009 correction per "
        "[`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) "
        "vs the project default E[L]=7 per "
        "[`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). "
        "The **factor-of-2 deviation flag = {1}** (deviation ratio = {2:.2f}). Cutoff lag M={3}.".format(
            el_star, b["factor_of_2_deviation_flag"], b["deviation_ratio"], b["cutoff_lag_M"],
        ),
        "",
        _fmt_acf_table(b["selected_acf_lags"]),
        "",
        "Politis-White 2-sigma significance threshold (n={0}): |rho| = {1:.3f}.".format(
            b["n_non_nan"], b["politis_white_significance_threshold_2sigma"],
        ),
        "",
        "### Cross-channel comparison (E[L]\\* by Strand A analysis) -- handoff section 2.4 load-bearing",
        "",
        "| analysis | channel | E[L]\\* |",
        "|---|---|---:|",
        "| Q3.5 (bb_overnight_gain, truth window) | per-night SLEEPEND-SLEEPSTART | 6.5 |",
        "| Q3.4 (stress_stdev_sleep) | per-night STDEV | 7.0 |",
        "| Q3.6 (resting_hr) | daily UDS restingHeartRate | 7.0 (fallback) |",
        "| Q3.7 (exertion_class ordinal) | 5-level activity class | 7.0 |",
        "| Q3.1 (stress_mean_sleep) | sleep-window mean | 12.6 |",
        "| Phase-1 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 |",
        "| Q3.3 (bb_lowest) | daily NADIR | 29.25 |",
        "| Q3.2 (all_day_stress_avg) | 24h-window mean | 29.8 |",
        "| **this analysis (push_burden_7d_lagged)** | **integer count [0, 6] (within-7d burden)** | **{0:.1f}** |".format(el_star),
        "",
        "### v3.1 -> v3.2 lagged-baseline correction (descriptive citation only)",
        "",
        "Per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed row + descriptive README "
        "section 3.4 explicit acknowledgment + garmin_indicators_audit.md audit 2026-06-11 "
        "item 2:",
        "",
        "- **The v3.1 problem**: `push_burden_7d` used a 30-day TRAILING rolling baseline "
        "that included the candidate day; in sustained-push periods the baseline crept up "
        "with the pushes (the channel rebased into its own reference frame and stopped "
        "looking heavy). Descriptive README section 3.4 names this as 'push_burden's "
        "rolling-baseline contamination'.",
        "- **The v3.2 fix**: switch to a `[d-90, d-30]` window (the `_lagged` variant in "
        "master; this Q3.8's channel). The lagged-baseline correction is the canonical "
        "project example of why baseline construction matters for sustained-push hypotheses.",
        "- **The outcome for HA01b-recomputed**: train +5.8 / validate +4.0 pp -- the "
        "original v3.1 validate +17.3 pp 'first SUPPORTED' headline softened by -13.3 pp "
        "on v3.2 recomputation (REJECTED.md HA01b-recomputed row). The original headline "
        "was substantially a baseline-construction artefact.",
        "- **The outcome for HA02c (this Q3.8's channel)**: train -18.7 / validate +0.7 pp "
        "-- the lagged-baseline correction improved measurement standing but did NOT "
        "resurrect push_burden as a predictor (REJECTED.md HA02c row).",
        "- **The master-side reality**: the v3.1 un-lagged `push_burden_7d` was DROPPED "
        "from the master per garmin_indicators_audit.md audit 2026-06-11 item 2 ('known "
        "rolling-baseline contamination'). Only the v3.2 `_lagged` variant (this Q3.8's "
        "channel) and the `_lagged_lcera` variant are present.",
        "",
        "Per handoff section 3 hard constraint: this Q3.8.b citation is **descriptive only**; "
        "the v3.1 -> v3.2 correction story is LOCKED at the CONVENTIONS section 3.2 + "
        "REJECTED.md + audit MD level and NOT re-litigated here. The autocorrelation reading "
        "is on the v3.2 channel.",
        "",
        "See [`plots/fig5_acf.png`](plots/fig5_acf.png).",
        "",
        "---",
        "",
        "## Q3.8.c -- Base rates per citalopram phase (Stratum 4)",
        "",
        "Phase axis per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3:",
        "",
        "| phase | window | n | median | mean | MAD | p10 / p90 | frac=0 | frac>=4 |",
        "|---|---|---:|---:|---:|---:|---|---:|---:|",
    ])
    out_lines.extend(per_phase_rows)
    out_lines.extend([
        "",
        "The two **transition phases** (buildup n={0}; afbouw n={1}) have **n<{2}** each; "
        "the two **steady-state phases** (unmedicated n={3}; consolidation n={4}) are larger. "
        "Any HA test that wants per-phase verdicts on this channel faces a sample-size "
        "disadvantage in the transition phases (parity with sister channels Q3.1.c / Q3.2.c "
        "/ Q3.3.c / Q3.4.c / Q3.5.c / Q3.6.c / Q3.7.c).".format(
            c.get("buildup", {}).get("n", 0),
            c.get("afbouw", {}).get("n", 0),
            max(c.get("buildup", {}).get("n", 0), c.get("afbouw", {}).get("n", 0)) + 1,
            c.get("unmedicated", {}).get("n", 0),
            c.get("consolidation", {}).get("n", 0),
        ),
        "",
        "Named counts (CONVENTIONS section 3.6): the per-phase n's above are `push_burden_"
        "7d_lagged`-non-NaN day rows in `per_day_master.csv` within Stratum 4 date masks per "
        "`citalopram_phase_stratification.md section 3` boundary dates.",
        "",
        "See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png).",
        "",
        "---",
        "",
        "## Q3.8.d -- Phase-stratified distribution + v3 scope status",
        "",
        "**Per CONVENTIONS section 4.2 (caveats yes; a-priori claims no)**: push_burden_7d "
        "is NOT in the v3 multi-channel sweep scope per [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "section 5.6 (6-channel scope: stress_mean_sleep + all_day_stress_avg + bb_lowest + "
        "resting_hr + bb_overnight_gain + respiration_avg_sleep; activity-labels family is "
        "not in v3 scope). No v3 verdict exists to cite or re-promote on this channel. "
        "HA02c (the Wiggers test on this channel) is LOCKED REFUTED per REJECTED.md HA02c "
        "row. This Q3.8.d reports the observed median shifts descriptively.",
        "",
        "Observed median shifts:",
        "",
        "| comparison | delta median | within-phase MAD | within-MAD? |",
        "|---|---:|---:|---|",
        "| buildup minus unmedicated | **{0:+.2f}** | {1:.2f}-{2:.2f} | {3} |".format(
            buildup_minus_unmed,
            c.get("buildup", {}).get("mad_unscaled", float("nan")),
            c.get("unmedicated", {}).get("mad_unscaled", float("nan")),
            "within 1 MAD" if abs(buildup_minus_unmed) <= 1 else "> 1 MAD; descriptively meaningful",
        ),
        "| consolidation minus unmedicated | **{0:+.2f}** | {1:.2f}-{2:.2f} | {3} |".format(
            consol_minus_unmed,
            c.get("consolidation", {}).get("mad_unscaled", float("nan")),
            c.get("unmedicated", {}).get("mad_unscaled", float("nan")),
            "within 1 MAD" if abs(consol_minus_unmed) <= 1 else "> 1 MAD; descriptively meaningful",
        ),
        "| consolidation minus buildup | **{0:+.2f}** | -- | -- |".format(
            d["phase_to_phase_shifts"].get("consolidation_minus_buildup_median", float("nan")),
        ),
        "| afbouw minus consolidation | **{0:+.2f}** | {1:.2f}-{2:.2f} | -- |".format(
            afbouw_minus_consol,
            c.get("afbouw", {}).get("mad_unscaled", float("nan")),
            c.get("consolidation", {}).get("mad_unscaled", float("nan")),
        ),
        "| afbouw minus unmedicated | **{0:+.2f}** | -- | -- |".format(afbouw_minus_unmed),
        "",
        "### Descriptive reading (no verdict promotion)",
        "",
        "The median moves from unmedicated ({0:.2f}) to consolidation ({1:.2f}) by **{2:+.2f}**. "
        "The day-resolved citalopram boundary step (30d pre/post 2024-04-09): **{3:+.2f}**. "
        "Per CONVENTIONS section 4.2: this is a Layer 1 descriptive observation; no a-priori "
        "claim is made about the shift's mechanism. push_burden_7d_lagged is the activity-"
        "axis count primitive -- the citalopram axis is not the natural confound axis for "
        "this channel (activity-labels family does NOT belong to the autonomic / cardiovascular "
        "v3 dose-response scope). Phase-stratified shifts on this activity-axis channel are "
        "reported for completeness; the substantive activity-axis story lives in the HA02c + "
        "HA01b-recomputed (LOCKED REFUTED) family.".format(
            unmed_med, consol_med, consol_minus_unmed,
            citalo_step["diff_post_minus_pre"] if citalo_step.get("diff_post_minus_pre") is not None else float("nan"),
        ),
        "",
        "### HA02c + HA01b-recomputed locked-verdict cross-reference (per handoff section 2.4 + R14 row)",
        "",
        "Per handoff section 2.4 + REJECTED.md: HA02c (push burden on Theme A lagged "
        "baseline, REFUTED both eras train -18.7 / validate +0.7); HA01b-recomputed (v3.2 "
        "lagged composite at exertion_class_lagged in {{heavy, very_heavy}}, REFUTED both "
        "eras train +5.8 / validate +4.0; R14 single-pool +5.1 pp [CI -14.7, +13.3] perm "
        "p=0.3689 NOT-SUPPORTED CONVERGE per single_pool_reanchor/findings.md HA01b-"
        "recomputed row `badd04a`). HA02c itself was NOT in the R14 single-pool re-anchor "
        "stretch list (single_pool_reanchor/findings.md HA02c row absent); the HA01b-"
        "recomputed family R14 is the closest sister-channel single-pool re-anchor on the "
        "activity-axis. The per-phase median shifts observed in Q3.8.d's table above are at "
        "the count primitive's bounded support [0, 6]; this is the descriptive complement to "
        "HA02c's REJECTED-both-eras verdict.",
        "",
        "See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) "
        "and [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) "
        "(90d rolling median through phases).",
        "",
        "---",
        "",
        "## Q3.8.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)",
        "",
        "Brief-mandated targets per handoff section 2.4: sister Q3.7 exertion_class via "
        "Spearman on ordinal-vs-numeric (load-bearing); activity-labels family v3.2 lagged "
        "siblings (the _lcera variant is the natural near-identity candidate); cross-family "
        "autonomic / cardiovascular companions.",
        "",
        "| target channel | n | Pearson r | Spearman rho | near-identity flag? |",
        "|---|---:|---:|---:|---|",
    ])
    out_lines.extend(near_id_rows)
    out_lines.extend([
        "",
        "**{0} near-identity pairs fire** at the |rho|>=0.92 CONVENTIONS section 3.3 "
        "threshold. The Q3.7 exertion_class sister (just LANDED `9b03bed`) reciprocally "
        "reports here the ordinal-encoded Spearman against this channel's numeric count "
        "form per handoff section 2.4 (load-bearing sibling activity-axis check). The "
        "expected near-identity pair is the `push_burden_7d_lagged_lcera` channel (same v3.2 "
        "lagged-baseline ancestry with the LC-era restriction layered on top); a high rho "
        "there is **expected by construction**, not a discovery. Any cross-family flags "
        "(stress / cardiovascular) would be material findings.".format(len(e["flagged_pairs"])),
        "",
        "---",
        "",
        "## Q3.8.f -- Crash-day vs normal-day (Stratum 4) + HA02c + HA01b-recomputed corroboration",
        "",
        "Per CONVENTIONS section 3.6 named counts: {0} crash-episodes (crash_v2 episode-level "
        "via `labels_crash_v2.csv` unique `episode_id` starting with `crash-`); {1} crash-"
        "days (day-level, `label=='crash'`); {2} non-crash days (the complement within "
        "Stratum 4 channel-valid days).".format(
            fe["n_crash_episodes"], fl["n_crash_day"], fl["n_normal_day"],
        ),
        "",
        "### Episode-level (primary unit per CONVENTIONS section 3.6)",
        "",
        "| stat | value |",
        "|---|---:|",
        "| n crash-episodes | {0} |".format(fe["n_crash_episodes"]),
        "| n normal-day base rate | {0} |".format(fe["n_normal_day_base_rate"]),
        "| mean per-episode `push_burden_7d_lagged` | {0:.3f} |".format(fe["mean_per_episode_value"]),
        "| mean normal-day `push_burden_7d_lagged` | {0:.3f} |".format(fe["mean_normal_day_value"]),
        "| mean diff (episode minus normal-day) | **{0:+.3f}** |".format(fe["mean_diff_episode_vs_normal_day"]),
        "| Cohen's d (episode-level vs normal-day pooled) | **{0:+.2f}** |".format(fe["cohens_d_episode_vs_normal_day"]),
        "| Bootstrap 95% CI on mean diff | **[{0:+.3f}, {1:+.3f}]** (5000 iters, seed=20260624) |".format(
            ci_ep[0], ci_ep[1],
        ),
        "",
        "**Episode-level Cohen's d={0:+.2f}** on this channel. HA02c's substantive direction "
        "prior: sustained-push burden in trailing 7d window is hypothesised to elevate crash "
        "risk (the higher-burden-day -> higher-crash-rate direction). The Q3.8.f observation "
        "is a descriptive day-level complement to HA02c's Wiggers-test operand; HA02c's "
        "REJECTED verdict is LOCKED.".format(fe["cohens_d_episode_vs_normal_day"]),
        "",
        "### Day-level (autocorrelation-inflated supplementary)",
        "",
        "| stat | value |",
        "|---|---:|",
        "| n crash-days | {0} |".format(fl["n_crash_day"]),
        "| n normal-days | {0} |".format(fl["n_normal_day"]),
        "| mean crash-day | {0:.3f} |".format(fl["mean_crash"]),
        "| mean normal-day | {0:.3f} |".format(fl["mean_normal"]),
        "| median crash-day | {0:.2f} |".format(fl["median_crash"]),
        "| median normal-day | {0:.2f} |".format(fl["median_normal"]),
        "| mean diff (point estimate) | **{0:+.3f}** |".format(fl["mean_diff"]),
        "| median diff | **{0:+.2f}** |".format(mwu["median_diff"]),
        "| Cohen's d | **{0:+.2f}** |".format(fl["cohens_d"]),
        "| Mann-Whitney U: z | **{0:+.2f}** |".format(mwu["z"]),
        "| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **{0}** |".format(mwu_p_str),
        "| Mann-Whitney U: P(crash > normal) | **{0:+.3f}** |".format(mwu["p_crash_greater_than_normal"]),
        "| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (project default) | [{0:+.3f}, {1:+.3f}], width {2:.3f} |".format(
            e7["ci_lower"], e7["ci_upper"], e7["ci_upper"] - e7["ci_lower"],
        ),
        "| Stationary bootstrap 95% CI on mean diff, **E[L]={0}** (data-driven, Q3.8.b flag) | **[{1:+.3f}, {2:+.3f}]**, width {3:.3f} |".format(
            eS["block_length_used"], eS["ci_lower"], eS["ci_upper"], eS["ci_upper"] - eS["ci_lower"],
        ),
        "",
        "### LOAD-BEARING HA02c + HA01b-recomputed R14 single-pool descriptive cross-reference (per handoff section 2.4)",
        "",
        "Per REJECTED.md HA02c row: **LOCKED REFUTED both eras** (train -18.7 pp / validate "
        "+0.7 pp). Push burden on Theme A lagged baseline; the lagged-baseline correction "
        "improved measurement standing but did NOT resurrect push_burden as a predictor. "
        "HA02c was NOT in the R14 single-pool re-anchor stretch list per "
        "[single_pool_reanchor/findings.md](../single_pool_reanchor/findings.md) (HA02c row "
        "absent); the closest single-pool diagnostic neighbour is the sister activity-axis "
        "HA01b-recomputed row: **+5.1 pp [CI -14.7, +13.3] perm p=0.3689 NOT-SUPPORTED "
        "CONVERGE (both NOT-SUPPORTED)** (`badd04a`). This Q3.8.f's first-order day-level "
        "Cohen's d=**{0:+.2f}** (episode-level) + Mann-Whitney U p={1} (day-level) **"
        "descriptively corroborate** the locked HA02c REFUTED-both-eras outcome at the "
        "channel-distribution level. **The HA02c + HA01b-recomputed + R14 substantive "
        "verdicts are LOCKED**; this Q3.8.f observation is descriptive corroboration only, "
        "NOT a re-interpretation.".format(
            fe["cohens_d_episode_vs_normal_day"], mwu_p_str,
        ),
        "",
        "### Crash-drop sensitivity (CONVENTIONS section 3.4)",
        "",
    ])
    if cd is not None:
        out_lines.extend([
            "| frame | Spearman rho | n |",
            "|---|---:|---:|",
            "| full Stratum 4 | {0:+.3f} | {1} |".format(cd["full_frame_value"], cd["n_full"]),
            "| crash-days dropped | {0:+.3f} | {1} |".format(cd["crash_dropped_value"], cd["n_crash_dropped"]),
            "| \\|delta\\| | **{0:.3f}** | -- |".format(cd["abs_delta"]),
            "| section 3.4 threshold (0.10) crossed? | **{0}** | -- |".format(
                "**YES**" if cd["exceeds_threshold_0p10"] else "no"
            ),
            "",
        ])
    else:
        out_lines.extend([
            "(crash-drop sensitivity not computed -- insufficient gevoelscore overlap)",
            "",
        ])
    out_lines.extend([
        "See [`plots/fig4_crash_vs_normal.png`](plots/fig4_crash_vs_normal.png).",
        "",
        "---",
        "",
        "## Q3.8.g -- Spike-detecting primitive availability",
        "",
        "`push_burden_7d_lagged` IS itself a count primitive (count of push-days in trailing "
        "7d window above the v3.2 lagged baseline) -- the channel value at day d is the "
        "spike-form on the activity axis (the within-7d burden-spike construct). Per "
        "CONVENTIONS section 3.5 spike/peak/count metrics preference: **this channel IS the "
        "spike-form construct on the activity-axis**; HA02c's tested operand IS this channel "
        "at the per-day count resolution; HA01b-recomputed tested the sister "
        "exertion_class_lagged {heavy, very_heavy} classifier form at the same Wiggers level. "
        "Both HA02c and HA01b-recomputed are LOCKED REFUTED both eras on v3.2 lagged baseline.",
        "",
        "Activity-axis primitives + companion siblings in master (for cross-channel pairwise comparison):",
        "",
    ])
    for entry in g["spike_primitives_available_in_master"]:
        out_lines.append("- `{0}` (n non-NaN = {1})".format(entry["column"], entry["n_non_nan"]))
    out_lines.extend([
        "",
        "### Pairwise correlations on Stratum 4",
        "",
        "| partner channel | Pearson r | Spearman rho | n |",
        "|---|---:|---:|---:|",
    ])
    for partner in ("exertion_class_lagged", "eff_exertion_rank_lagged", "push_burden_7d_lagged_lcera", "effective_exertion_slope_28d"):
        if "spearman_rho_vs_" + partner in g:
            out_lines.append("| `{0}` | {1:+.3f} | {2:+.3f} | {3} |".format(
                partner,
                g["pearson_r_vs_" + partner],
                g["spearman_rho_vs_" + partner],
                g["n_pair_" + partner],
            ))
    out_lines.extend([
        "",
        "**Latent in FIT, not in master**:",
        "",
    ])
    for entry in g["latent_in_FIT_not_in_master"]:
        out_lines.append("- {0}".format(entry))
    out_lines.extend([
        "",
        "Per CONVENTIONS section 3.5: spike/peak/count metrics preferred over daily means -- "
        "`push_burden_7d_lagged` IS the count primitive on the activity axis (count of push-"
        "days above lagged baseline in trailing 7d). Per CONVENTIONS section 3.2: prefer the "
        "v3.2 `_lagged` variant over the v3.1 rolling-baseline variant -- this Q3.8 channel "
        "IS the v3.2 fix. HA02c (REJECTED) tested this exact channel at the spike-form "
        "Wiggers level; HA01b-recomputed (REJECTED) tested the sister exertion_class_lagged "
        "{heavy, very_heavy} form; both REJECTED both eras.",
        "",
        "---",
        "",
        "## Q3.8.h -- Outlier detection + calibration-drift check + activity-labels partial-coverage",
        "",
        "Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md):",
        "",
    ])
    for entry in h["garmin_indicators_audit_known_issues"]:
        out_lines.append("- {0}".format(entry))
    out_lines.extend([
        "",
        "### Outlier scan (MAD-based |z|>5 with count-primitive caveat)",
        "",
        "**{0} outlier-day flagged** out of {1}.".format(h["n_flagged"], a["n"]),
        "",
    ])
    if len(outliers) > 0:
        out_lines.extend([
            "| date | value | MAD-z |",
            "|---|---:|---:|",
        ])
        for o in outliers[:20]:
            out_lines.append("| {0} | {1:.0f} | {2:+.2f} |".format(
                o["date"], o["value"], o["mad_z"],
            ))
        if len(outliers) > 20:
            out_lines.append("(... {0} more rows; truncated for legibility)".format(len(outliers) - 20))
        out_lines.append("")
    out_lines.extend([
        "For an integer-valued bounded-support count primitive, MAD-z outlier semantics "
        "interpret 'extreme' as the upper-bound value (a week with 6 push-days above lagged "
        "baseline) -- this is a legitimate high-burden week, NOT a sensor failure; the "
        "n_flagged count above reports the rule output, not a sensor-failure count.",
        "",
        "### Drift check -- rolling 90d median over Stratum 4",
        "",
        "| snapshot date | rolling 90d median |",
        "|---|---:|",
    ])
    for snap in h["rolling_90d_median_snapshots"]:
        rm = snap["rolling_med_90d"]
        rm_str = "n/a" if rm is None else "{0:.1f}".format(rm)
        out_lines.append("| {0} | {1} |".format(snap["snapshot_date"], rm_str))
    out_lines.extend([
        "",
        "### Citalopram boundary step (2024-04-09)",
        "",
        "Pre-30d mean = {0:.2f}; post-30d mean = {1:.2f}; **diff = {2:+.2f}**.".format(
            citalo_step["pre_30d_mean"] if citalo_step["pre_30d_mean"] is not None else float("nan"),
            citalo_step["post_30d_mean"] if citalo_step["post_30d_mean"] is not None else float("nan"),
            citalo_step["diff_post_minus_pre"] if citalo_step["diff_post_minus_pre"] is not None else float("nan"),
        ),
        "",
        "### Consolidation boundary step (2024-06-20)",
        "",
        "Pre-30d mean = {0:.2f}; post-30d mean = {1:.2f}; **diff = {2:+.2f}**.".format(
            consol_step["pre_30d_mean"] if consol_step["pre_30d_mean"] is not None else float("nan"),
            consol_step["post_30d_mean"] if consol_step["post_30d_mean"] is not None else float("nan"),
            consol_step["diff_post_minus_pre"] if consol_step["diff_post_minus_pre"] is not None else float("nan"),
        ),
        "",
        "### Afbouw boundary step (2026-03-20)",
        "",
        "Pre-30d mean = {0:.2f}; post-30d mean = {1:.2f}; **diff = {2:+.2f}**.".format(
            afbouw_step["pre_30d_mean"] if afbouw_step["pre_30d_mean"] is not None else float("nan"),
            afbouw_step["post_30d_mean"] if afbouw_step["post_30d_mean"] is not None else float("nan"),
            afbouw_step["diff_post_minus_pre"] if afbouw_step["diff_post_minus_pre"] is not None else float("nan"),
        ),
        "",
        "### Activity-labels partial-coverage reference (per handoff section 2.4)",
        "",
        "Existing primitive validation + visualisation lives in "
        "[`garmin_exploration/activity-labels/`](../../../analyses/garmin_exploration/activity-labels/) "
        "(per programme spec section 3.4 'partially covered by activity-labels/'). The per-day "
        "classification depends on Garmin's activity-labels family + steps + moderate-VPA per "
        "the family's `definition.md` severity cutoffs (current state: cutoffs are NOT formally "
        "LOCKED). This Q3.8.h descriptively characterises the v3.2 lagged-baseline-corrected "
        "channel AS-IS under the current classifier definition; the family's locking state "
        "is unchanged by this Q3.8 (descriptive layer only).",
        "",
        "See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).",
        "",
        "---",
        "",
        "## Q3.8.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel",
        "",
        "Discipline anchor: [HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) "
        "(secondary-logistic-with-covariate pattern; beta disambiguation between primary-"
        "signal and candidate alternative readings). Names **four** candidate covariates a "
        "future HA on `push_burden_7d_lagged` (or a variant) as predictor should pre-spec. "
        "Note that HA02c (LOCKED REFUTED) already tested the primary operand at the Wiggers "
        "level; further HA pre-regs would explore different operand variants.",
        "",
    ])
    for idx, cov in enumerate(ic["candidate_covariates"], start=1):
        out_lines.extend([
            "### {0}. `{1}`".format(idx, cov["covariate"]),
            "",
            cov["rationale"],
            "",
            "*Source*: {0}".format(cov["source"]),
            "",
        ])
        if cov.get("observed_correlation_on_S4"):
            oc = cov["observed_correlation_on_S4"]
            enc_str = " (" + oc["encoding_note"] + ")" if "encoding_note" in oc else ""
            out_lines.extend([
                "*Observed correlation on S4*: Pearson r={0:+.3f} / Spearman rho={1:+.3f} (n={2}){3}.".format(
                    oc["pearson_r"], oc["spearman_rho"], oc["n"], enc_str,
                ),
                "",
            ])
    out_lines.extend([
        "### Recommendation",
        "",
        ic["recommendation"],
        "",
        "---",
        "",
        "## Cross-references",
        "",
        "### HA-* tests that touch this channel (cite this analysis)",
        "",
        "- **HA02c** (push burden in trailing 7d on Theme A v3.2 lagged baseline; LOCKED "
        "REFUTED both eras train -18.7 / validate +0.7 per REJECTED.md HA02c row; NOT in R14 "
        "single-pool re-anchor stretch list): primary operand IS this channel at the spike-"
        "form Wiggers level. **The descriptive substrate this analysis produces -- the "
        "Stratum-4 distribution (Q3.8.a) + autocorrelation E[L]\\*=X (Q3.8.b) + per-phase "
        "reads (Q3.8.c, Q3.8.d) + first-order day-level crash-vs-normal (Q3.8.f) -- "
        "complements HA02c's tested operand with the raw-channel-distribution view.** The "
        "substantive HA02c verdict is LOCKED; this analysis's descriptive corroboration in "
        "Q3.8.f is NOT a re-interpretation.",
        "- **HA01b-recomputed** (sister activity-axis Wiggers test; v3.2 lagged composite at "
        "exertion_class_lagged in {heavy, very_heavy}; LOCKED REFUTED both eras train +5.8 / "
        "validate +4.0 per REJECTED.md HA01b-recomputed row; R14 single-pool +5.1 pp [CI "
        "-14.7, +13.3] perm p=0.3689 NOT-SUPPORTED CONVERGE per single_pool_reanchor/"
        "findings.md HA01b-recomputed row `badd04a`): the closest single-pool diagnostic "
        "neighbour to HA02c on the activity-axis. Q3.8.f descriptively cites the R14 "
        "single-pool result as the closest sister-channel anchor.",
        "",
        "### Methodology MDs cited",
        "",
        "- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 -- Q3.8.c phase axis; Q3.8.d phase-stratified treatment.",
        "- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) -- E[L]=7 default + factor-of-2 deviation rule.",
        "- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) -- Stratum 4 boundary definition.",
        "- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) -- Q3.8.h cross-reference (audit 2026-06-11 item 2 push_burden_7d v3.1 drop + v3.2 lagged-composite landing).",
        "- [`methodology/_descriptive_stocktake_2026-06-23.md`](../../../methodology/_descriptive_stocktake_2026-06-23.md) section 3 + section 5 -- gap-list framing.",
        "",
        "### Existing artefacts referenced",
        "",
        "- [`descriptive/operationalisation_support/exertion_class/findings.md`](../exertion_class/findings.md) -- sister Q3.7 activity-axis channel (just LANDED `9b03bed`); the ordinal-vs-numeric near-identity check in Q3.8.e re-uses Q3.7's CATEGORY_ORDER ordinal encoding.",
        "- [`descriptive/operationalisation_support/resting_hr/findings.md`](../resting_hr/findings.md) -- Q3.6 sister continuous-channel precedent (Tier 2 2nd); clean programmatic-emit pattern.",
        "- [`descriptive/operationalisation_support/bb_overnight_gain/findings.md`](../bb_overnight_gain/findings.md) -- Q3.5 sister continuous-channel precedent (Tier 2 1st).",
        "- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) -- R14 HA01b-recomputed row (descriptively corroborated in Q3.8.f); HA02c row ABSENT per stretch-list scope.",
        "- [`REJECTED.md`](../../../REJECTED.md) -- HA02c row + HA01b-recomputed row (v3.1 -> v3.2 correction).",
        "- [`analyses/garmin_exploration/activity-labels/`](../../../analyses/garmin_exploration/activity-labels/) -- partial-coverage primitive validation + visualisation (per programme spec section 3.4 'partially covered by activity-labels/').",
        "",
        "### Upstream pipeline",
        "",
        "- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- activity-axis upstream classifier per `activity-labels/definition.md` severity cutoffs + v3.2 lagged-baseline construction per CONVENTIONS section 3.2 `[d-90, d-30]` window.",
        "- `labels_crash_v2.csv` <- `garmin/hypotheses/crash_v2-definition/definition.md` (locked).",
        "",
        "---",
        "",
        "## Limitations",
        "",
        "For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal "
        "claim per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding constraints are:",
        "",
        "1. **No HA verdict promotion**: HA02c + HA01b-recomputed + R14 HA01b-recomputed "
        "single-pool verdicts are LOCKED; this analysis's descriptive observations are NOT "
        "re-interpretations or re-promotions per CONVENTIONS section 4.2 + handoff section 3.",
        "2. **No v3.1 -> v3.2 lagged-baseline correction re-litigation** per handoff section 3 "
        "hard constraint. The v3.2 correction story is LOCKED at the CONVENTIONS section 3.2 "
        "+ REJECTED.md + audit MD level; Q3.8.b citation is descriptive only.",
        "3. **HA02c was NOT in the R14 single-pool re-anchor stretch list** per "
        "single_pool_reanchor/findings.md (HA02c row absent); the descriptive cross-reference "
        "in Q3.8.f relies on the REJECTED.md HA02c locked verdict and the sister "
        "HA01b-recomputed R14 row.",
        "4. **First-order day-level read distinct from HA02c's tested operand**: HA02c's "
        "spike-form construct (push burden in trailing 7d on lagged baseline) IS this Q3.8 "
        "channel at the count-primitive resolution; Q3.8.f's day-level Cohen's d is the "
        "descriptive-layer complement on episode-level + day-level reads.",
        "5. **CONVENTIONS section 3.2 / audit-MD contradiction surfaced** (not re-litigated): "
        "CONVENTIONS section 3.2 says v3.1 push_burden_7d stays in master; the audit MD "
        "removed it. The pipeline-side reality binds; CONVENTIONS section 3.2 needs a "
        "stocktake refresh.",
        "6. **activity-labels classifier definition cutoffs are NOT formally LOCKED** per "
        "activity-labels/definition.md (current state); Q3.8.h descriptively characterises "
        "the channel AS-IS under the current classifier definition.",
        "",
        "---",
        "",
        "*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` "
        "(gitignored per `docs/research/**/*.json`). To refresh: ``python run.py``.*",
        "",
    ])

    path.write_text("\n".join(out_lines), encoding="utf-8")


def write_readme_md(summary: dict, path: Path) -> None:
    """Emit the README from the computed summary."""
    q = summary["questions"]
    a = q["Q3.8.a_distribution"]
    b = q["Q3.8.b_autocorrelation"]
    c = q["Q3.8.c_base_rates_per_phase"]
    fr = q["Q3.8.f_crash_vs_normal"]
    fe = fr["episode_level"]
    ci_ep = fe["bootstrap_ci95_mean_diff"]

    el_star = b["data_driven_E_L_star"]
    n_near_id_flags = len(q["Q3.8.e_near_identity"].get("flagged_pairs", []))

    out_lines = [
        "# `push_burden_7d` -- operationalisation-support descriptive analysis",
        "",
        "**Strand**: A (operationalisation support; template-driven; no operationalisation "
        "interview required per [`descriptive/README.md`](../../README.md) section 7b).",
        "",
        "## Research question",
        "",
        "Operationalisation-support descriptive characterisation of `push_burden_7d_lagged` "
        "(the v3.2 lagged-baseline-corrected variant of `push_burden_7d`; the v3.1 un-lagged "
        "form is absent from master per audit MD 2026-06-11 item 2) on Stratum 4, answering "
        "Q3.8.a-i per the locked descriptive programme spec at "
        "[`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.4 "
        "(LOCKED 2026-06-18 r3, commit `ccbd12e`; this channel listed under HA-touched non-"
        "confirmed candidate list as HA01b/HA01c primary, partially covered by "
        "activity-labels/; descriptive README section 3.4 also explicitly acknowledges "
        "'push_burden's rolling-baseline contamination'). **4th of the 5 Tier 2 channels** in "
        "the user-prioritised Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st "
        "= Q3.5 bb_overnight_gain `7d49ba4`; Tier 2 2nd = Q3.6 resting_hr `5d28219`; Tier 2 "
        "3rd = Q3.7 exertion_class `9b03bed`; this Q3.8 closes Tier 2 4th; next: Q3.9 "
        "gevoelscore -- dispatched in parallel).",
        "",
        "Substantive status: **HA02c primary operand** on the v3.2 lagged baseline; LOCKED "
        "REFUTED both eras (train -18.7 pp / validate +0.7 pp per "
        "[`REJECTED.md`](../../../REJECTED.md) HA02c row + "
        "[`activity-labels/output/ha_results_4day_lagged.md`](../../../analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md); "
        "the lagged-baseline correction improved measurement standing but did NOT resurrect "
        "push_burden as a predictor). HA02c was NOT in the R14 single-pool re-anchor stretch "
        "list per [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md); "
        "the closest single-pool diagnostic neighbour is the sister activity-axis "
        "**HA01b-recomputed** (LOCKED REFUTED both eras train +5.8 / validate +4.0; R14 "
        "single-pool **+5.1 pp [CI -14.7, +13.3] perm p (E[L]=7) = 0.3689** NOT-SUPPORTED "
        "CONVERGE; `badd04a`). Sister channel to Q3.7 exertion_class (just LANDED `9b03bed`); "
        "both activity-labels-family v3.1 -> v3.2 lagged-baseline corrected. **v3.1 -> v3.2 "
        "lagged-baseline correction is the canonical project example** per CONVENTIONS "
        "section 3.2 + REJECTED.md HA01b-recomputed + descriptive README section 3.4 explicit "
        "acknowledgment + audit MD 2026-06-11 item 2 drop. Q3.8.b cites the correction "
        "descriptively per handoff section 2.4; this Q3.8 does NOT re-litigate per handoff "
        "section 3 hard constraint.",
        "",
        "## Method",
        "",
        "- **Surface**: Stratum 4 primary (LC + gevoelscore + crash labels, 2022-09-03 to "
        "2026-06-05; n={0} channel-valid days out of {1} S4 days).".format(
            a["n"], summary["n_rows_stratum_4_total"],
        ),
        "- **Channel-as-it-appears**: `push_burden_7d_lagged` (the v3.2 fix; integer-valued "
        "bounded support [0, 6]; count of push-days in trailing 7d window above the "
        "`[d-90, d-30]` lagged baseline per CONVENTIONS section 3.2). The v3.1 un-lagged "
        "`push_burden_7d` was DROPPED from master per audit MD 2026-06-11 item 2 (known "
        "rolling-baseline contamination per descriptive README section 3.4).",
        "- **Phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with sister "
        "Strand-A analyses Q3.1 / Q3.2 / Q3.3 / Q3.4 / Q3.5 / Q3.6 / Q3.7.",
        "- **Scope per handoff section 2.2**: standard continuous-channel template (no "
        "categorical adaptations; the integer-valued bounded-support means mean / median / "
        "MAD / quantiles apply identically to the continuous-channel precedent Q3.5 / Q3.6).",
        "- **Cross-references** per handoff section 2.4: v3.1 -> v3.2 lagged-baseline "
        "correction descriptively cited in Q3.8.b (per CONVENTIONS section 3.2 + REJECTED.md "
        "HA01b-recomputed + descriptive README section 3.4 explicit acknowledgment); REJECTED.md "
        "HA02c NULL + R14 HA01b-recomputed result (closest single-pool neighbour) in Q3.8.f; "
        "Q3.7 exertion_class sister-channel Spearman on ordinal-vs-numeric in Q3.8.e; sister-"
        "channel E[L]\\* spread in Q3.8.b.",
        "- **Computed directly from `per_day_master.csv`**: Q3.8.a (distribution shape + per-"
        "value frequency for integer count), Q3.8.b (Politis-White E[L]\\* on Stratum-4 pool "
        "+ v3.1 -> v3.2 correction descriptive citation), Q3.8.c (per-phase base rates "
        "citalopram axis), Q3.8.d (phase-stratified medians + v3 scope status), Q3.8.e (near-"
        "identity check |rho|>=0.92 on 17-channel panel incl. ordinal-encoded sister Q3.7 "
        "exertion_class), Q3.8.f (crash-vs-normal Cohen's d + Mann-Whitney U + stationary-"
        "bootstrap CI at E[L]=7 and data-driven E[L]\\* + crash-drop sensitivity + LOAD-"
        "BEARING REJECTED.md HA02c + R14 HA01b-recomputed descriptive cross-reference), "
        "Q3.8.g (count-primitive spike-form discussion + cross-channel pairwise correlations), "
        "Q3.8.h (outlier detection + calibration-drift + activity-labels partial-coverage), "
        "Q3.8.i (covariate-sensitivity readiness for future HA pre-regs).",
        "- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) "
        "(loaders, Stratum 4 filter, crash-drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) "
        "(`compute_data_driven_block_length`, `stationary_bootstrap_ci`).",
        "- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).",
        "",
        "## Result",
        "",
        "Headline (see [`findings.md`](findings.md) for the full answers Q3.8.a-i):",
        "",
        "`push_burden_7d_lagged` on Stratum 4 is an **integer-valued bounded-support [0, 6] "
        "count primitive on the activity axis** (median {0:.2f}; MAD {1:.2f}; skew {2:+.2f}; "
        "heavy_tail_flag={3}; fraction at 0 = {7:.1%}; fraction at >=4 = {8:.1%}). **Data-"
        "driven E[L]\\*={4:.1f}** (Politis-White; vs project default E[L]=7). **Phase-"
        "stratified medians** (citalopram axis): unmedicated {5:.2f} -> consolidation "
        "{6:.2f}. Episode-level Cohen's d={9:+.2f} (bootstrap CI95 [{10:+.2f}, {11:+.2f}]) -- "
        "descriptively corroborates HA02c's locked REJECTED-both-eras outcome (REJECTED.md "
        "HA02c row) at the first-order day-level read (HA02c's tested operand IS this Q3.8 "
        "channel at the spike-form Wiggers level). Near-identity check: **{12}** pair(s) at "
        "the |rho|>=0.92 CONVENTIONS section 3.3 threshold (the v3.2 _lcera sibling channel "
        "is the expected high-rho neighbour by construction).".format(
            a["median"], a["mad_unscaled"], a["skewness"], a["heavy_tail_flag"],
            el_star,
            c.get("unmedicated", {}).get("median", float("nan")),
            c.get("consolidation", {}).get("median", float("nan")),
            a["fraction_at_zero"], a["fraction_above_4"],
            fe["cohens_d_episode_vs_normal_day"], ci_ep[0], ci_ep[1],
            n_near_id_flags,
        ),
        "",
        "## Files",
        "",
        "- [`README.md`](README.md) -- this file",
        "- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + "
        "`findings.md` + `README.md` + `plots/*.png`",
        "- [`findings.md`](findings.md) -- writeup covering Q3.8.a-i + tables "
        "(programmatically emitted by run.py from summary.json per the Q3.2/Q3.3/Q3.4/Q3.5/"
        "Q3.6/Q3.7 architectural note about the Write-tool harness heuristic on the literal "
        "filename \"findings\")",
        "- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per "
        "`docs/research/**/*.json`)",
        "- [`plots/`](plots/) -- 5 PNGs: per-value frequency, phase-stratified violins, "
        "trajectory-with-phases, crash-vs-normal, ACF (gitignored per `docs/research/**/*.png`)",
        "",
        "## Status",
        "",
        "**Current as of 2026-06-05 corpus + 2026-06-24 analysis** (commit context: post-"
        "`9b03bed` Q3.7 exertion_class LANDED; Phase 2 'finish the descriptive analysis' "
        "Tier 2 batch 4th of 5 channels; Q3.9 gevoelscore dispatched in parallel). Refresh when:",
        "",
        "1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel "
        "is about to spin up beyond the HA02c-locked operand.",
        "2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope "
        "2026-06-06 onward).",
        "3. Politis-White E[L]\\* shifts by another factor of 2 from current {0:.1f}.".format(el_star),
        "4. activity-labels classifier definition.md severity cutoffs change (current state: "
        "cutoffs NOT locked per definition.md; Q3.8.h per-month rate-drift snapshots "
        "characterise stability AS-IS).",
        "5. A v3.3 baseline-correction or any further upstream-classifier revision lands "
        "(current state: v3.2 lagged is canonical per CONVENTIONS section 3.2 + audit MD "
        "2026-06-11 item 2 v3.1 drop).",
        "",
        "## Cross-references",
        "",
        "- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 "
        "2026-06-18, commit `ccbd12e`); section 3.4 also explicitly names 'push_burden's "
        "rolling-baseline contamination'.",
        "- **LOAD-BEARING canonical correction example**: [`REJECTED.md`](../../../REJECTED.md) "
        "HA02c row + HA01b-recomputed row + [CONVENTIONS section 3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses); "
        "Q3.8.b cites descriptively (NOT re-litigated per handoff section 3 hard constraint).",
        "- **Q3.7 most-recent Tier 2 precedent (sister activity-axis channel)**: "
        "[`descriptive/operationalisation_support/exertion_class/`](../exertion_class/) -- "
        "Tier 2 3rd of 5; CATEGORICAL ADAPTATION + activity-labels family Q-template "
        "discipline; ordinal-encoded sibling near-identity check in Q3.8.e references the "
        "Q3.7 CATEGORY_ORDER encoding.",
        "- **Q3.6 continuous-channel precedent**: [`descriptive/operationalisation_support/resting_hr/`](../resting_hr/) "
        "-- Tier 2 2nd of 5; clean programmatic-emit + f-string discipline.",
        "- **Q3.5 Tier 2 first precedent**: [`descriptive/operationalisation_support/bb_overnight_gain/`](../bb_overnight_gain/) "
        "-- Tier 2 1st of 5; load-bearing cross-reference template.",
        "- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) "
        "-- HA02c NOT in stretch list (row absent); HA01b-recomputed row descriptively "
        "corroborated in Q3.8.f as the closest sister-channel neighbour.",
        "- **Partial-coverage activity-labels artefact**: [`analyses/garmin_exploration/activity-labels/`](../../../analyses/garmin_exploration/activity-labels/) "
        "-- existing primitive validation + visualisation; descriptively referenced in Q3.8.h.",
        "- **HA-* tests that this analysis anchors**:",
        "  - **HA02c** (LOCKED REFUTED both eras train -18.7 / validate +0.7; NOT in R14 "
        "stretch list); primary operand on this channel.",
        "  - **HA01b-recomputed** (LOCKED REFUTED both eras train +5.8 / validate +4.0; R14 "
        "single-pool +5.1 pp NOT-SUPPORTED CONVERGE); sister activity-axis channel.",
        "- **Methodology MDs**: `citalopram_phase_stratification.md`, `permutation_null_block_length.md`, "
        "`lc_era_temporal_segmentation.md`, `garmin_indicators_audit.md` (v3.1 drop + v3.2 "
        "lagged landing), `_descriptive_stocktake_2026-06-23.md` (gap-list framing).",
        "- **Upstream pipeline**: `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` "
        "<- activity-axis upstream classifier per `activity-labels/definition.md` severity "
        "cutoffs + v3.2 lagged-baseline construction per CONVENTIONS section 3.2 `[d-90, d-30]` "
        "window. `labels_crash_v2.csv` per locked `crash_v2-definition`.",
        "",
    ]
    path.write_text("\n".join(out_lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 70)
    print("Q3.8 push_burden_7d operationalisation-support descriptive (Tier 2 4th of 5)")
    print("=" * 70)
    print()

    df_full = load_master(as_of_date=AS_OF_DATE, stratum_4_only=False)
    print("Loaded per_day_master.csv: {0} rows total (as_of {1})".format(
        len(df_full), AS_OF_DATE,
    ))

    df = filter_to_stratum_4(df_full, as_of_date=AS_OF_DATE)
    n_s4 = int(len(df))
    print("Stratum 4 rows: {0}".format(n_s4))

    crashes = load_crash_labels(as_of_date=AS_OF_DATE)
    df = df.merge(
        crashes[["date", "label", "episode_id"]].rename(columns={"label": "crash_label"}),
        on="date", how="left",
    )
    df["is_crash"] = df["crash_label"].fillna("normal") == "crash"
    print("Crash days in S4 (label=='crash'): {0}".format(int(df["is_crash"].sum())))

    if CHANNEL not in df.columns:
        raise SystemExit(
            "Channel {0!r} missing from per_day_master.csv; check column name + pipeline output".format(CHANNEL)
        )

    print()
    print("Computing Q3.8.a-i on {0} (channel display: {1})...".format(CHANNEL, CHANNEL_DISPLAY))

    values_s4 = df[CHANNEL]
    a_res = q_a_distribution(values_s4)
    print("  Q3.8.a: n={0}, mean={1:.3f}, median={2:.3f}, skew={3:+.3f}, heavy_tail={4}, frac0={5:.1%}".format(
        a_res["n"], a_res["mean"], a_res["median"], a_res["skewness"],
        a_res["heavy_tail_flag"], a_res["fraction_at_zero"],
    ))

    b_res = q_b_autocorrelation(values_s4)
    print("  Q3.8.b: E[L]*={0:.2f} (default 7; factor-of-2 flag={1}; M={2})".format(
        b_res["data_driven_E_L_star"], b_res["factor_of_2_deviation_flag"], b_res["cutoff_lag_M"],
    ))

    c_res = q_c_base_rates_per_phase(df, CHANNEL)
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = c_res.get(ph, {})
        if info.get("n", 0) > 0:
            print("  Q3.8.c [{0}]: n={1}, median={2:.2f}, frac0={3:.1%}".format(
                ph, info["n"], info["median"], info["fraction_at_zero"],
            ))
        else:
            print("  Q3.8.c [{0}]: n=0".format(ph))

    d_res = q_d_phase_stratified(c_res, CHANNEL)
    print("  Q3.8.d: v3 in-scope = {0}".format(d_res["v3_scope_status"]["channel_in_v3_six_channel_scope"]))

    e_res = q_e_near_identity(df, CHANNEL)
    print("  Q3.8.e: {0} near-identity pair(s) at |rho|>={1}".format(
        len(e_res["flagged_pairs"]), e_res["threshold"],
    ))
    for fl in e_res["flagged_pairs"]:
        print("        flagged: {0}".format(fl))

    f_res = q_f_crash_vs_normal(df, CHANNEL)
    flr = f_res["day_level"]
    fer = f_res["episode_level"]
    print("  Q3.8.f: episode d={0:+.2f} CI95 [{1:+.3f}, {2:+.3f}]; day Cohen's d={3:+.2f}; MWU p={4:.4f}".format(
        fer["cohens_d_episode_vs_normal_day"],
        fer["bootstrap_ci95_mean_diff"][0],
        fer["bootstrap_ci95_mean_diff"][1],
        flr["cohens_d"],
        flr["mann_whitney_u"]["p_two_sided"],
    ))

    g_res = q_g_spike_primitive(df, CHANNEL)
    print("  Q3.8.g: count primitive on activity axis; {0} sibling activity-axis primitives in master".format(
        len(g_res["spike_primitives_available_in_master"]),
    ))

    h_res = q_h_outliers_calibration(df, CHANNEL)
    print("  Q3.8.h: {0} MAD-z>5 outliers flagged (count-primitive caveat applies)".format(h_res["n_flagged"]))

    i_res = q_i_covariate_readiness(df, CHANNEL)
    print("  Q3.8.i: {0} candidate covariates named".format(len(i_res["candidate_covariates"])))

    summary = {
        "channel": CHANNEL,
        "channel_display": CHANNEL_DISPLAY,
        "as_of_date": AS_OF_DATE,
        "n_rows_full_corpus_to_as_of": int(len(df_full)),
        "n_rows_stratum_4_total": n_s4,
        "questions": {
            "Q3.8.a_distribution": a_res,
            "Q3.8.b_autocorrelation": b_res,
            "Q3.8.c_base_rates_per_phase": c_res,
            "Q3.8.d_phase_stratified_distribution": d_res,
            "Q3.8.e_near_identity": e_res,
            "Q3.8.f_crash_vs_normal": f_res,
            "Q3.8.g_spike_primitive": g_res,
            "Q3.8.h_outliers_calibration": h_res,
            "Q3.8.i_covariate_readiness": i_res,
        },
    }

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
        return x

    summary_serialisable = _convert(summary)
    summary_path.write_text(json.dumps(summary_serialisable, indent=2), encoding="utf-8")
    print()
    print("Wrote {0}".format(summary_path))

    plots_dir = HERE / "plots"
    written_plots = make_plots(df, CHANNEL, plots_dir)
    print("Wrote {0} plots in {1}".format(len(written_plots), plots_dir))
    for p in written_plots:
        print("  {0}".format(p))

    findings_path = HERE / "findings.md"
    write_findings_md(summary, findings_path)
    print()
    print("Wrote {0}".format(findings_path))

    readme_path = HERE / "README.md"
    write_readme_md(summary, readme_path)
    print("Wrote {0}".format(readme_path))

    print()
    print("Done. Q3.8 LANDED (Tier 2 4th of 5; exertion_class done; next: gevoelscore -- in parallel).")


if __name__ == "__main__":
    main()
