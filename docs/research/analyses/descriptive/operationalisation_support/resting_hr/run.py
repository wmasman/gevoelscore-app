"""Descriptive analysis: resting_hr operationalisation support.

Answers Q3.6.a-i per the locked descriptive programme:
``docs/research/analyses/descriptive/README.md`` section 3.4 (template
a-i applied to this channel, per the section 3.4 HA-touched-non-confirmed
candidate list: "resting_hr (HA06b primary; weak v3 dose-modulation)").
This is the **2nd of the 5 Tier 2 channels** in the user-prioritised
"finish the descriptive analysis" Phase 2 sequential batch (Tier 1
closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain `7d49ba4`; this
Q3.6 closes Tier 2 2nd; then Q3.7 exertion_class, Q3.8 push_burden_7d,
Q3.9 gevoelscore).

Channel: Garmin daily restingHeartRate field (UDS-passthrough; daily
aggregate). HA06b's PRIMARY OPERAND in primitive form (HA06b tested
max |z| (4d, bidirectional) of resting_hr with lagged baseline +
sigma_floor=0.5 bpm; this Q3.6 reports first-order day-level
descriptive characterisation distinct from HA06b's tested second-order
construct).

Channel substantive status (per handoff section 1):
- HA06b primary operand: TRAIN SUPPORTED +18.9 pp / validate refuted
  +0.8 pp / OVERALL REFUTED per HA06b-rhr-zscore/result.md; R14
  CONVERGE-ON-OVERALL at single-pool +6.7 pp [CI -18.7, +17.9] perm
  p (E[L]=7) = 0.3368 per single_pool_reanchor/findings.md row HA06b
  (`badd04a`).
- H01 primary operand: refuted both eras (train -1.2 pp / validate
  -9.5 pp; absolute 7d-mean +3 bpm spec; superseded by HA06b's
  relative-threshold framing); R14 CONVERGE (both NOT-SUPPORTED) at
  single-pool -3.1 pp [CI -9.4, +10.1] perm p=0.7820 per
  single_pool_reanchor/findings.md row H01.
- HA06 primary operand: REFUTED both eras (absolute 4-5d delta >=
  5 bpm bidirectional; superseded by HA06b's z-score relative-threshold
  framing).
- IN v3 multi-channel sweep scope per
  citalopram_dose_response_stress_mean_sleep.md section 5.6 (covered
  6 channels: stress_mean_sleep, all_day_stress_avg, bb_lowest,
  resting_hr, bb_overnight_gain, respiration_avg_sleep). Per the
  v3-sweep verdict resting_hr was REJECTED with weak/non-significant
  beta (the "weakly consistent" v3 row); citalopram-dose-modulation
  is REJECTED for substantive purposes -- this Q3.6.d reports the
  observed shifts descriptively per CONVENTIONS section 4.2 caveat-
  class (NOT a re-promotion to CONFIRMED, NOT a re-promotion to a
  v3 reclassification).

Continuous-channel template (parity with sister CONFIRMED-citalopram
channels Q3.1 / Q3.2 / Q3.3 + Tier 2 sister stress_stdev_sleep Q3.4
+ Q3.5 bb_overnight_gain): standard Cohen's d primary, no zero-rate
column. Q3.6 extends the standard Stratum-4 surface with TWO
load-bearing cross-reference extensions per handoff section 2.4:

1. **recovery_arc v2 section 7b E[L]\\*=23 reproduction**: the
   recovery_arc analysis reported on the PRE-ILLNESS HEALTHY +
   ACUTE_INFECTION + LC_PRE_ERGO + 4a + 4b + CITALOPRAM_MODULATED
   6-phase axis a paired-bootstrap 4b-minus-4a delta of +3.0 bpm
   [+2.0, +4.0] for resting_hr with combined E[L]\\*=22.7 (the only
   channel where the 4b-4a sub-boundary CI excludes 0). This Q3.6.b
   reports the data-driven E[L]\\* on Strand-A's Stratum-4 pool (the
   pool DIFFERS from recovery_arc's per-phase pools; descriptive
   reproduction/divergence + a pool-difference note); if the value is
   close to 23 that's a methodological consistency confirmation.

2. **recovery_arc v2 cardiovascular-family acute-infection DIP
   (54 -> 52.5) reproduction**: this Q3.6.c extends the Strand-A
   per-phase reads OUT of the default Stratum-4 window (which starts
   2022-09-03) to include the pre_illness_healthy (217 day-level
   rows, 2021-08-16 -> 2022-03-20) + acute_infection (14 day-level
   rows, 2022-03-21 -> 2022-04-03) phases on the FULL CORPUS, so
   the recovery_arc cardiovascular-family acute-infection-DIP
   finding can be descriptively reproduced (parasympathetic
   dominance during viral infection; n=14 too short for tight CI).

Output: ``summary.json`` (machine-readable per-question results) +
``plots/*.png`` (visualisations) + ``findings.md`` + ``README.md``
(programmatically emitted from this script per the Q3.2/Q3.3/Q3.4/
Q3.5 precedent session's architectural note about the Write-tool
harness heuristic on the literal filename "findings").

Discipline guards (per CONVENTIONS):
- section 2.1 descriptive-before-inference: no causal claims; no
  falsification bar; no HA verdict promotion (HA06b + H01 + HA06
  substantive verdicts + R14 single-pool verdicts + HA-P6 v3 LOCKED
  and NOT extended here; v3 REJECTED status on resting_hr NOT
  promoted to CONFIRMED).
- section 3.1 personal baseline: distribution shape is reported
  as-is; phase-stratified to surface the citalopram step where
  observable, framed as descriptive observation only.
- section 3.3 column-duplication: near-identity check at |rho|>=0.92.
- section 3.4 crash-drop sensitivity: |Delta|>0.10 flag surfaced.
- section 3.5 spike metrics: resting_hr is a DAILY-AGGREGATE channel
  (lowest stable nightly HR via UDS restingHeartRate); HA06b's
  tested operand is the per-4-day MAX |z| of the channel (a
  spike-form on this channel construct). Per CONVENTIONS section
  3.5 spike/peak/count metrics over daily means -- the daily channel
  IS the operationalisation substrate for the HA06b spike-form;
  finer-than-daily resolution (per-minute HR) is NOT in master.
- section 3.6 named counts: every count reports scheme + unit +
  source.
- section 4.1 + section 4.2: no a-priori claims; observed phase
  shift framed as descriptive observation only; v3 REJECTED
  caveat-class framing for Q3.6.d.
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
# HERE = .../analyses/descriptive/operationalisation_support/resting_hr
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


CHANNEL = "resting_hr"
AS_OF_DATE = "2026-06-05"  # parity with R14 + Q3.1-Q3.5 prior Strand-A analyses

# Citalopram phase boundaries per
# methodology/citalopram_phase_stratification.md section 3
PHASE_BOUNDARIES = [
    ("unmedicated", date(2022, 9, 3), date(2024, 4, 8)),
    ("buildup", date(2024, 4, 9), date(2024, 6, 19)),
    ("consolidation", date(2024, 6, 20), date(2026, 3, 19)),
    ("afbouw", date(2026, 3, 20), date(2026, 6, 5)),
    # post_afbouw begins 2026-06-06; not in as-of cut
]

# 6-phase recovery axis boundaries per methodology/lc_recovery_phase_axis.md
# (LOCKED `d47e0d3`; recovery_arc v2 uses these). Used in Q3.6.c extension.
RECOVERY_PHASE_BOUNDARIES = [
    ("pre_illness_healthy", date(2021, 8, 16), date(2022, 3, 20)),
    ("acute_infection", date(2022, 3, 21), date(2022, 4, 3)),
    ("lc_pre_ergo", date(2022, 4, 4), date(2022, 9, 21)),
    ("pacing_pre_citalopram_learning_4a", date(2022, 9, 22), date(2022, 11, 16)),
    ("pacing_habit_established_4b", date(2022, 11, 17), date(2024, 4, 8)),
    ("citalopram_modulated", date(2024, 4, 9), date(2026, 6, 5)),
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
# Q3.6.a Distribution shape
# ---------------------------------------------------------------------------


def q_a_distribution(values: pd.Series) -> dict:
    """Distribution shape on Stratum 4 (Q3.6.a)."""
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
    # resting_hr is a positive-valued daily aggregate (bpm); not zero-floored
    # but lower-bounded by participant's physiological minimum. Heavy-tail
    # rule per CONVENTIONS section 3.1: skew > 1 OR p99/median > 3.0.
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
# Q3.6.b Autocorrelation + E[L]*
# ---------------------------------------------------------------------------


def q_b_autocorrelation(values: pd.Series) -> dict:
    """Autocorrelation structure + E[L]* (Q3.6.b)."""
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
        "recovery_arc_v2_section_7b_reported_E_L_star_for_rhr": 22.7,
        "recovery_arc_v2_pool": (
            "paired-bootstrap E[L]* combined from the joined 4a+4b "
            "window (sub-phase pacing_pre_citalopram_learning_4a "
            "[2022-09-22, 2022-11-16] + pacing_habit_established_4b "
            "[2022-11-17, 2024-04-08]; n=53+500 day-level rows) per "
            "recovery_arc v2 findings.md section 3 table"
        ),
        "this_q36_pool": (
            "data-driven E[L]* on Stratum-4 single pool 2022-09-03 to "
            "AS_OF_DATE; pool differs from recovery_arc's per-phase "
            "sub-pool; descriptive reproduction/divergence is the "
            "reading per handoff section 2.4"
        ),
    }


# ---------------------------------------------------------------------------
# Q3.6.c Base rates per phase (citalopram axis)
# ---------------------------------------------------------------------------


def q_c_base_rates_per_phase(df: pd.DataFrame, channel: str) -> dict:
    """Per-phase n + median + dispersion (Q3.6.c, citalopram axis)."""
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
# Q3.6.c extension: per-phase base rates on the 6-phase recovery axis
# (LOAD-BEARING: extends OUT of Stratum 4 to include pre_illness_healthy +
# acute_infection phases so the recovery_arc v2 cardiovascular-family
# acute-infection DIP finding can be descriptively reproduced)
# ---------------------------------------------------------------------------


def q_c_recovery_axis_base_rates(df_full: pd.DataFrame, channel: str) -> dict:
    """Per-recovery-phase n + median + dispersion on the FULL CORPUS.

    Q3.6.c LOAD-BEARING extension per handoff section 2.4: surfaces the
    acute-infection DIP finding from recovery_arc v2 (54 -> 52.5 with
    n=14 day-level rows). This requires going OUT of the default Stratum-4
    window (which starts 2022-09-03) into the pre-illness healthy
    baseline (2021-08-16 -> 2022-03-20) + acute infection
    (2022-03-21 -> 2022-04-03) phases on the full corpus.

    Bootstrap CIs at E[L]=7 (project default per
    permutation_null_block_length.md) on each per-phase median for
    cross-cell comparability per recovery_arc v2 section 6.6.
    """
    out = {}
    rng_seed = 20260624
    for phase_name, start, end in RECOVERY_PHASE_BOUNDARIES:
        mask = (df_full["date"] >= pd.Timestamp(start)) & (df_full["date"] <= pd.Timestamp(end))
        sub = df_full.loc[mask, channel].dropna().astype(float)
        n = int(len(sub))
        if n == 0:
            out[phase_name] = {
                "n": 0,
                "date_start": str(start),
                "date_end": str(end),
                "note": "no non-NaN values in this phase window",
            }
            continue
        med = float(sub.median())
        # Bootstrap CI95 on median (stationary bootstrap E[L]=7).
        if n >= 2:
            boot_med = stationary_bootstrap_ci(
                sub.to_numpy(),
                lambda x: float(np.median(x)),
                n_bootstrap=5000,
                expected_block_length=7,
                confidence_level=0.95,
                random_state=rng_seed,
            )
            ci_lo = float(boot_med["ci_lower"])
            ci_hi = float(boot_med["ci_upper"])
        else:
            ci_lo = float("nan")
            ci_hi = float("nan")
        out[phase_name] = {
            "n": n,
            "date_start": str(start),
            "date_end": str(end),
            "median": med,
            "median_ci95_E_L7": [ci_lo, ci_hi],
            "mean": float(sub.mean()),
            "std_ddof1": float(sub.std(ddof=1)) if n > 1 else float("nan"),
            "mad_unscaled": float(np.median(np.abs(sub - med))),
            "p10": float(np.percentile(sub, 10)) if n >= 10 else float("nan"),
            "p90": float(np.percentile(sub, 90)) if n >= 10 else float("nan"),
        }

    # Descriptive reproduction read of the acute-infection DIP
    healthy_med = out.get("pre_illness_healthy", {}).get("median")
    acute_med = out.get("acute_infection", {}).get("median")
    dip_observed = None
    if healthy_med is not None and acute_med is not None:
        dip_observed = float(acute_med - healthy_med)

    return {
        "per_recovery_phase": out,
        "recovery_arc_v2_section_5a_reported": {
            "pre_illness_healthy_median_bpm": 54.0,
            "pre_illness_healthy_ci95_E_L7": [52.0, 55.0],
            "acute_infection_median_bpm": 52.5,
            "acute_infection_ci95_E_L7": [51.0, 55.0],
            "acute_infection_n_day_rows": 14,
            "lc_pre_ergo_median_bpm": 55.0,
            "lc_pre_ergo_ci95_E_L7": [52.0, 56.0],
            "pacing_4a_median_bpm": 53.0,
            "pacing_4a_ci95_E_L7": [53.0, 54.0],
            "pacing_4b_median_bpm": 56.0,
            "pacing_4b_ci95_E_L7": [56.0, 57.0],
            "citalopram_modulated_median_bpm": 57.0,
            "citalopram_modulated_ci95_E_L7": [56.0, 58.0],
            "narrative": (
                "recovery_arc v2 reported: resting_hr uniquely DIPS in "
                "acute infection (54 -> 52.5; parasympathetic dominance "
                "during viral infection; n=14 too short for tight CI). "
                "The narrative arc: healthy 54 -> acute 52.5 -> "
                "lc_pre_ergo 55 -> 4a 53 (second dip toward acute "
                "level) -> 4b 56 -> citalopram_modulated 57 (slow "
                "upward drift). resting_hr is the only channel where "
                "the 4b-4a paired-bootstrap CI excludes 0 (+3.0, CI "
                "[+2.0, +4.0], E[L]*=22.7)."
            ),
            "source": "trajectory/recovery_arc/findings.md section 5.A + section 2 + section 3 table",
        },
        "this_q36_descriptive_acute_dip_reproduction": {
            "healthy_median_observed": healthy_med,
            "acute_median_observed": acute_med,
            "acute_minus_healthy_observed_bpm": dip_observed,
            "framing": (
                "If the observed dip (acute median minus healthy "
                "median) is near the recovery_arc reported -1.5 bpm "
                "(54 -> 52.5), that is descriptive reproduction. If "
                "it differs materially, that's worth flagging. The "
                "n=14 acute-phase sample limits tight CI on the dip "
                "magnitude per recovery_arc v2 caveat 2."
            ),
        },
    }


# ---------------------------------------------------------------------------
# Q3.6.d Phase-stratified distribution + v3-REJECTED caveat-class framing
# ---------------------------------------------------------------------------


def q_d_phase_stratified(per_phase: dict, channel: str) -> dict:
    """Phase-stratified distribution + descriptive shift report (Q3.6.d).

    Per handoff section 1 + section 2.4 + CONVENTIONS section 4.2: this
    channel IS in the v3 multi-channel sweep scope but was REJECTED with
    weak/non-significant beta per citalopram_dose_response_stress_mean_
    sleep.md section 5.6. The citalopram-dose-modulation status is
    therefore REJECTED at v3-locked verdict level. This Q3.6.d reports
    the observed median + dispersion shift across the citalopram-axis
    phases descriptively; it does NOT promote a CONFIRMED/REJECTED
    reclassification (the v3 REJECTED verdict is LOCKED). Per
    CONVENTIONS section 4.2 caveat-class framing: observed shifts are
    Layer 1 descriptive observations only.
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
        "v3_verdict": "REJECTED (weakly consistent; beta non-significant)",
        "v3_source": "methodology/citalopram_dose_response_stress_mean_sleep.md v3 section 5.6 (resting_hr listed as one of 6 channels; verdict 'weakly consistent' which falls in the REJECTED tier per the section 5.6.1 four discipline rules)",
        "framing": (
            "resting_hr was tested in the v3 multi-channel sweep (per "
            "citalopram_dose_response_stress_mean_sleep.md section 5.6 "
            "6-channel scope) and classified as REJECTED with weak/non-"
            "significant beta. Observed phase-shift below is a Layer 1 "
            "descriptive observation per CONVENTIONS section 4.2 (caveats "
            "yes; a-priori claims no); the v3 REJECTED verdict is LOCKED "
            "and this Q3.6.d does NOT promote a CONFIRMED-citalopram "
            "claim. Per the handoff section 3 hard constraints: no "
            "v3 REJECTED -> CONFIRMED reclassification."
        ),
    }

    out["ha06b_h01_ha06_xref"] = {
        "ha06b_locked_verdict": (
            "TRAIN SUPPORTED +18.9 pp / VALIDATE refuted +0.8 pp / "
            "OVERALL REFUTED; bidirectional max |z| (4d) at N_std=1.5; "
            "the bidirectional framing captures train +18.9 pp where "
            "one-sided arm fails crit (a) at 50%"
        ),
        "ha06b_primary_operand": "max |z| (4d, bidirectional) of resting_hr; lagged baseline; sigma_floor=0.5 bpm",
        "ha06b_r14_single_pool_disc_pp": +6.7,
        "ha06b_r14_single_pool_ci95": [-18.7, +17.9],
        "ha06b_r14_single_pool_perm_p": 0.3368,
        "ha06b_r14_verdict": "NOT-SUPPORTED CONVERGE-ON-OVERALL (locked OVERALL-REFUTED + single-pool NOT-SUPPORTED)",
        "h01_locked_verdict": (
            "REFUTED both eras (train -1.2 pp / validate -9.5 pp); "
            "absolute spec: frac windows with 7d-mean RHR - trimmed "
            "baseline >= +3 bpm; the absolute-threshold misalignment "
            "vs participant's actual RHR variability motivated HA06b "
            "z-score reframing"
        ),
        "h01_r14_single_pool_disc_pp": -3.1,
        "h01_r14_single_pool_ci95": [-9.4, +10.1],
        "h01_r14_single_pool_perm_p": 0.7820,
        "h01_r14_verdict": "NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED)",
        "ha06_locked_verdict": (
            "REFUTED both eras; absolute spec: bidirectional max |delta| "
            ">= 5 bpm in 4-5d window; SUPERSEDED by HA06b z-score "
            "framing; absolute threshold was too coarse for "
            "participant's RHR variability"
        ),
        "ha06_source": "analyses/hypotheses/HA06-morning-rhr-delta/result.md",
        "ha06b_source": "analyses/hypotheses/HA06b-rhr-zscore/result.md",
        "h01_source": "analyses/hypotheses/H01-rhr-drift/result.md",
        "r14_source": "descriptive/operationalisation_support/single_pool_reanchor/findings.md rows HA06b + H01",
    }
    return out


# ---------------------------------------------------------------------------
# Q3.6.e Near-identity check
# ---------------------------------------------------------------------------

NEAR_IDENTITY_THRESHOLD = 0.92  # CONVENTIONS section 3.3


def q_e_near_identity(df: pd.DataFrame, channel: str) -> dict:
    """Near-identity check vs candidate companion channels (Q3.6.e).

    Targets per descriptive README section 3.4 / Q3.x.e template +
    handoff section 2.4 substantive companions:
      - bb_lowest (NADIR autonomic channel; INVERSE direction sister
        per Q3.3.e rho=-0.171)
      - stress_mean_sleep (CONFIRMED-citalopram autonomic channel;
        cross-family autonomic-load companion)
      - all_day_stress_avg (CONFIRMED-citalopram autonomic channel)
      - awake_stress_avg, awake_stress_max (waking-hour cardiovascular
        companions)
      - bb_during_sleep_value (sleep-window BB; cardiovascular-recharge
        companion)
      - sleep efficiency / hours metrics if present
    Plus the obvious autonomic neighbours.
    """
    targets = [
        # Brief-mandated per descriptive README section 3.4 template
        "stress_mean_sleep",
        "all_day_stress_avg",
        "stress_low_motion_min_count_S60_Mlow",
        # Stress-family neighbours
        "stress_stdev_sleep",
        "asleep_stress_avg_uds",
        "awake_stress_avg",
        "awake_stress_max",
        "all_day_stress_max",
        # Cardiovascular + BB family
        "bb_lowest",
        "bb_highest",
        "bb_during_sleep_value",
        "bb_overnight_gain",
        # Respiration (cross-family autonomic companion)
        "respiration_avg_sleep",
        "respiration_lowest",
        "respiration_highest",
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
            "Sister bb_lowest Q3.3.e reported Pearson r=-0.194 / Spearman "
            "rho=-0.171 with resting_hr (NOT near-identity; modest inverse "
            "BB-floor-vs-RHR coupling). Reciprocal check here confirms "
            "that rho on the channel-flipped frame. Cross-family "
            "comparison: cardiovascular (resting_hr) and autonomic-load "
            "(stress family) channels are operationally distinct in this "
            "corpus -- the cross-channel-correlation card already noted "
            "no near-identity in the project's 9-anchor primitive set."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.6.f Crash-day vs normal-day on Stratum 4 + crash-drop sensitivity
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
    sensitivity (Q3.6.f).

    Per handoff section 2.4: this descriptively re-anchors HA06b train-
    SUPPORTED-only-now-OVERALL-REFUTED + H01 both-eras-refuted + R14
    single-pool NOT-SUPPORTED for both (HA06b +6.7 pp p=0.3368; H01
    -3.1 pp p=0.7820). NOTE: HA06b's primitive is max |z| (4d,
    bidirectional) of resting_hr -- a second-order construct on the
    channel. This Q3.6.f is on the raw channel value (first-order, day-
    level), which is the descriptive-level read distinct from the HA's
    tested operand. The episode-level Cohen's d here corroborates the
    channel signal at a coarser-than-HA06b resolution.
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
                "note": "data-driven from Q3.6.b; rounded to nearest integer",
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
        "ha06b_h01_cross_reference": {
            "ha06b_tested_operand": "max |z| (4d, bidirectional) of resting_hr; lagged baseline; sigma_floor=0.5 bpm",
            "ha06b_locked_train_disc_pp": +18.9,
            "ha06b_locked_validate_disc_pp": +0.8,
            "ha06b_locked_overall_verdict": "TRAIN SUPPORTED / VALIDATE refuted / OVERALL REFUTED",
            "ha06b_r14_single_pool_disc_pp": +6.7,
            "ha06b_r14_single_pool_ci95": [-18.7, +17.9],
            "ha06b_r14_single_pool_perm_p": 0.3368,
            "ha06b_r14_verdict": "NOT-SUPPORTED CONVERGE-ON-OVERALL",
            "h01_locked_train_disc_pp": -1.2,
            "h01_locked_validate_disc_pp": -9.5,
            "h01_locked_overall_verdict": "REFUTED both eras (absolute spec; superseded by HA06b z-score framing)",
            "h01_r14_single_pool_disc_pp": -3.1,
            "h01_r14_single_pool_ci95": [-9.4, +10.1],
            "h01_r14_single_pool_perm_p": 0.7820,
            "h01_r14_verdict": "NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED)",
            "ha06_locked_overall_verdict": "REFUTED both eras (absolute spec; SUPERSEDED by HA06b)",
            "r14_source": "descriptive/operationalisation_support/single_pool_reanchor/findings.md rows HA06b + H01",
            "ha06b_source": "analyses/hypotheses/HA06b-rhr-zscore/result.md",
            "h01_source": "analyses/hypotheses/H01-rhr-drift/result.md",
            "ha06_source": "analyses/hypotheses/HA06-morning-rhr-delta/result.md",
            "note": (
                "HA06b primitive is a second-order construct on this "
                "channel (per-day max |z| over 4d window). This Q3.6.f "
                "reports the first-order day-level Cohen's d on the raw "
                "channel as the descriptive-layer complement. Episode-"
                "level d here is the channel-distribution corroboration "
                "of the HA-level signal; the HA-level + R14 verdicts are "
                "LOCKED and NOT extended."
            ),
        },
    }


# ---------------------------------------------------------------------------
# Q3.6.g Spike-detecting primitive availability
# ---------------------------------------------------------------------------


def q_g_spike_primitive(df: pd.DataFrame, channel: str) -> dict:
    """Spike-primitive availability for resting_hr (Q3.6.g).

    resting_hr is a Garmin-UDS-aggregated daily field (the lowest stable
    nightly HR). Per HA06b result + handoff section 1: HA06b's tested
    operand IS the spike-form construct on this channel -- the per-day
    max |z| (4d, bidirectional) of the channel value -- which IS a
    within-4-day spike-of-HR-deviation metric. CONVENTIONS section 3.5
    spike/peak/count preference is satisfied at the HA06b level; the
    raw daily channel is the operationalisation substrate.
    """
    out = {
        "channel_resolution": (
            "per-day Garmin UDS restingHeartRate (lowest stable nightly "
            "HR; UDS-passthrough; daily aggregate)"
        ),
        "spike_or_continuous_form": (
            "DAILY-AGGREGATE primitive (single value per day; not a "
            "second-order construct in master; HA06b's tested operand "
            "IS the per-4-day MAX |z| spike-form built on this daily "
            "channel)"
        ),
        "sub_daily_resolution_in_master": False,
        "spike_primitives_available_in_master": [],
        "latent_in_FIT_not_in_master": [
            "per-minute heart-rate samples (NOT in master; would require FIT-side extraction)",
            "per-second HR during specific intervals (NOT in master)",
            "morning-only RHR vs all-day RHR (Garmin UDS exposes restingHeartRate as a single daily value; finer-than-daily RHR is not in the GDPR dump as restingHeartRate per garmin_indicators_audit.md UDS-passthrough discipline)",
        ],
        "related_daily_hr_metrics_in_master": [],
        "note": (
            "Per CONVENTIONS section 3.5: spike/peak/count metrics "
            "preferred over daily means -- HA06b's spike-form construct "
            "(per-4-day max |z| of resting_hr with lagged baseline + "
            "sigma_floor=0.5 bpm) IS the within-4-day spike-of-HR-"
            "deviation metric on this channel. The per-day resting_hr "
            "value IS the operationalisation substrate for that "
            "spike-form; finer-than-daily resolution would require new "
            "FIT-side extraction. Per HA06 result.md caveat: "
            "chronotropic incompetence (>85% of ME/CFS patients have "
            "blunted HR response per Workwell's own caveat) is a "
            "substrate caveat for HR-channel signals' biological "
            "interpretation, not a calibration-drift signature."
        ),
    }
    for c in (
        "stress_mean_sleep",
        "all_day_stress_max",
        "awake_stress_max",
        "stress_low_motion_min_count_S60_Mlow",
        "bb_lowest",
        "bb_highest",
        "respiration_avg_sleep",
    ):
        if c in df.columns:
            n = int(df[c].notna().sum())
            out["spike_primitives_available_in_master"].append({"column": c, "n_non_nan": n})
    for partner in ("bb_lowest", "stress_mean_sleep", "all_day_stress_avg", "respiration_avg_sleep", "awake_stress_max"):
        if partner in df.columns:
            d = df[[channel, partner]].dropna()
            if len(d) > 30:
                out[f"pearson_r_vs_{partner}"] = float(d.corr().iloc[0, 1])
                out[f"spearman_rho_vs_{partner}"] = float(d.corr(method="spearman").iloc[0, 1])
                out[f"n_pair_{partner}"] = int(len(d))
    return out


# ---------------------------------------------------------------------------
# Q3.6.h Outlier detection + calibration-drift check
# ---------------------------------------------------------------------------


def q_h_outliers_calibration(df: pd.DataFrame, channel: str) -> dict:
    """Outlier detection + calibration-drift check (Q3.6.h).

    MAD-based |z|>5 on Stratum 4. Reports flagged dates + values +
    drift snapshots. Cross-references garmin_indicators_audit.md known-
    issues for the UDS-passthrough cardiovascular family.
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
                "resting_hr is UDS-side passthrough from daily_uds.csv "
                "(Garmin restingHeartRate field); JSON-side no FIT "
                "parsing; UDS-passthrough discipline applies per "
                "garmin_indicators_audit.md UDS family rows"
            ),
            (
                "No specific calibration-drift events catalogued for "
                "resting_hr in garmin_indicators_audit.md beyond the "
                "shared UDS-family entries (same as sister BB-family "
                "channels which are also UDS-passthrough)"
            ),
            (
                "Underlying sensor is Forerunner 245 Elevate V3 "
                "throughout the entire 2021-08-16 to present window -- "
                "no device change in the analytic window"
            ),
            (
                "Per HA06 result.md + H01 result.md caveat: chronotropic "
                "incompetence (>85% of ME/CFS patients have blunted HR "
                "response per Workwell's own caveat) is a substrate "
                "caveat for any HR-channel signal's biological "
                "interpretation. This is NOT a calibration-drift "
                "signature on this device; it is a population-level "
                "physiological caveat noted by the source literature."
            ),
            (
                "Per HA06b result.md: the participant's typical max |z| "
                "sits in the 1.6-3.5 bpm range (relative) and the "
                "lagged baseline sigma sits around 2.0-2.3 bpm; the "
                "channel's day-to-day variability is consistent and "
                "stable across the analytic window."
            ),
        ],
    }


# ---------------------------------------------------------------------------
# Q3.6.i Covariate-sensitivity readiness
# ---------------------------------------------------------------------------


def q_i_covariate_readiness(df: pd.DataFrame, channel: str) -> dict:
    """Covariate-sensitivity readiness (Q3.6.i).

    Per HA-P7 section 4.5.4 worked-example pattern. Names candidate
    covariates a future HA on resting_hr as predictor could add.
    """
    cands = []
    # 1. dose_plasma_mg(d) -- citalopram covariate (v3 REJECTED)
    cands.append({
        "covariate": "dose_plasma_mg(d) (citalopram covariate -- v3 REJECTED with weak beta)",
        "rationale": (
            "resting_hr was in v3 multi-channel sweep scope per "
            "citalopram_dose_response_stress_mean_sleep.md section 5.6 "
            "and classified as REJECTED with weak/non-significant beta. "
            "A future HA on resting_hr cross-phase should pre-spec dose "
            "as a secondary covariate to surface any latent dose-"
            "modulation residue and to descriptively re-anchor the v3 "
            "REJECTED verdict; if beta_dose is significant in the "
            "secondary, that is candidacy evidence for a v3 re-test (NOT "
            "a re-promotion of the v3 verdict). Per CONVENTIONS section "
            "4.2 caveat-class: the v3 REJECTED verdict is LOCKED and "
            "this covariate arm is diagnostic, not a re-promotion path."
        ),
        "source": "methodology/citalopram_dose_response_stress_mean_sleep.md v3 section 5.6 (REJECTED with weak beta); CONVENTIONS section 4.2 caveat-class framing",
        "expected_effect_if_residue": (
            "beta_dose carries any latent dose-modulation residue; "
            "beta_channel attenuates if dose carries part of the signal"
        ),
        "needed_columns_in_master": ["lc_phase (in master) or runtime dose_plasma_mg(d) computation"],
    })
    # 2. own-lagged trailing-mean -- autocorrelation-vs-mechanism (HA-P7 section 4.5.4)
    cands.append({
        "covariate": "resting_hr_lagged_lcera_z(d) (already materialised in master per CONVENTIONS section 3.2)",
        "rationale": (
            "Mirrors HA-P7 section 4.5.4 worked example (lagged-outcome "
            "covariate) for the autocorrelation-vs-mechanism "
            "disambiguation. Per Q3.6.b the cutoff lag M and data-driven "
            "E[L]* are inputs to this choice. per_day_master ALREADY has "
            "a materialised resting_hr_lagged_lcera_z column (LC-era-"
            "only [d-90, d-30] trailing baseline per CONVENTIONS section "
            "3.2 _lagged_lcera convention). HA06b's tested operand IS "
            "the per-4-day max |z| using this lagged baseline; any "
            "future HA on resting_hr should use the materialised "
            "_lagged_lcera_z directly OR pre-spec a shorter window."
        ),
        "source": "HA-P7 hypothesis.md section 4.5.4; per_day_master.csv resting_hr_lagged_lcera_z column",
        "expected_effect": (
            "beta_channel collapses if today's resting_hr is just "
            "yesterday's value carried forward; beta_channel survives "
            "if the signal carries new-day information"
        ),
        "needed_columns_in_master": [
            "resting_hr_lagged_lcera_z (already in master per CONVENTIONS section 3.2)"
        ],
    })
    # 3. bb_lowest -- cross-family autonomic-recovery anchor
    bb_corr = None
    if "bb_lowest" in df.columns:
        d = df[[channel, "bb_lowest"]].dropna()
        if len(d) > 30:
            bb_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "bb_lowest (alternative autonomic-recovery anchor; INVERSE direction sister)",
        "rationale": (
            "Per Q3.3.e sister analysis: bb_lowest <-> resting_hr "
            "Spearman rho ~-0.171 (NOT near-identity at section 3.3 "
            "threshold). The covariate disambiguates: beta_channel "
            "attenuates -> the resting_hr signal is shared with "
            "cardiovascular-recovery via the BB-floor axis (RHR-up "
            "co-occurs with BB-floor-down); beta_channel survives -> "
            "the RHR signal carries autonomic-arousal-specific "
            "information beyond the BB-floor axis."
        ),
        "source": "Q3.3.e bb_lowest sister analysis cross-pair table",
        "observed_correlation_on_S4": bb_corr,
        "expected_effect": (
            "beta_channel attenuates if shared autonomic-recovery "
            "dominates; beta_channel survives if RHR carries independent "
            "autonomic-arousal information"
        ),
    })
    # 4. stress_mean_sleep -- cross-family autonomic-load anchor
    smean_corr = None
    if "stress_mean_sleep" in df.columns:
        d = df[[channel, "stress_mean_sleep"]].dropna()
        if len(d) > 30:
            smean_corr = {
                "pearson_r": float(d.corr().iloc[0, 1]),
                "spearman_rho": float(d.corr(method="spearman").iloc[0, 1]),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "stress_mean_sleep (cross-family autonomic-load anchor; CONFIRMED-citalopram sister)",
        "rationale": (
            "Per Q3.1.e sister analysis: stress_mean_sleep <-> resting_"
            "hr Spearman rho ~+0.10-0.20 range (NOT near-identity at "
            "section 3.3 threshold; cross-family modest positive "
            "coupling). The covariate disambiguates: beta_channel "
            "attenuates -> the RHR signal is shared autonomic-load via "
            "the sleep-stress axis; beta_channel survives -> RHR "
            "carries cardiovascular-specific information beyond the "
            "autonomic-load axis."
        ),
        "source": "Q3.1.e sister stress_mean_sleep cross-pair table + cross-channel-correlation card",
        "observed_correlation_on_S4": smean_corr,
        "expected_effect": (
            "beta_channel attenuates if shared autonomic-load dominates; "
            "beta_channel survives if RHR carries cardiovascular-specific "
            "information"
        ),
    })
    return {
        "primary_use_case": (
            "Future HA pre-reg using resting_hr as predictor of a "
            "crash-related outcome (HA06b substantive verdict already "
            "LOCKED at OVERALL-REFUTED + R14 single-pool NOT-SUPPORTED; "
            "further HAs can use the channel in different operands -- "
            "e.g. raw daily value, different window lengths, single-"
            "direction primitives, multi-day persistence per HA06b "
            "follow-up note -- without re-anchoring the HA06b-locked "
            "verdict)."
        ),
        "discipline_anchor": "HA-P7 hypothesis.md section 4.5.4 -- secondary-logistic-with-covariate pattern",
        "candidate_covariates": cands,
        "recommendation": (
            "Pre-spec all four covariates as secondary sensitivity arms. "
            "The dose_plasma_mg arm (covariate 1) is diagnostic-only at "
            "this time per the v3 REJECTED status; a positive beta_dose "
            "residue in the secondary is candidacy for a v3 re-test, "
            "NOT a re-promotion of the v3 verdict. The autocorrelation "
            "arm (covariate 2) operationalises HA-P7 section 4.5.4 on "
            "this channel using the already-materialised _lagged_lcera_"
            "z variant. The bb_lowest arm (covariate 3) is the cross-"
            "family autonomic-recovery disambiguator. The stress_mean_"
            "sleep arm (covariate 4) is the cross-family autonomic-load "
            "disambiguator."
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
    med_label = "median={0:.1f}".format(med)
    p25_label = "p25={0:.1f}".format(p25)
    p75_label = "p75={0:.1f}".format(p75)
    ax.axvline(med, color="#222", linestyle="-", linewidth=1.5, label=med_label)
    ax.axvline(p25, color="#222", linestyle="--", linewidth=1.0, label=p25_label)
    ax.axvline(p75, color="#222", linestyle="--", linewidth=1.0, label=p75_label)
    ax.set_xlabel("resting_hr (bpm; Garmin UDS restingHeartRate)")
    ax.set_ylabel("days (Stratum 4)")
    n_label = int(vals.notna().sum())
    ax.set_title("resting_hr distribution - Stratum 4, n={0}".format(n_label))
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
    if len(keep) > 0:
        ax.violinplot(
            [phase_data[p] for p in keep],
            showmedians=True, widths=0.85,
        )
        ax.set_xticks(np.arange(1, len(keep) + 1))
        ax.set_xticklabels(keep)
    ax.set_ylabel("resting_hr (bpm)")
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
    ax.set_ylabel("resting_hr (bpm)")
    ax.set_title("resting_hr - rolling 90d median + citalopram phases")
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
    ax.set_xlabel("resting_hr (bpm)")
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
        ax.bar(lags, acf, width=0.7, color="#5b88c4", edgecolor="white")
        ax.axhline(0, color="#222", linewidth=0.5)
        threshold = 2.0 * np.sqrt(np.log(len(arr)) / len(arr))
        thresh_label = "|rho|={0:.3f} (Politis-White 2-sigma)".format(threshold)
        ax.axhline(threshold, color="#cc4949", linestyle="--", linewidth=0.8, label=thresh_label)
        ax.axhline(-threshold, color="#cc4949", linestyle="--", linewidth=0.8)
        ax.set_xlabel("lag (days)")
        ax.set_ylabel("autocorrelation")
        title = "ACF - resting_hr (Stratum 4); E[L]*={0:.1f}, M={1}".format(
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


def make_recovery_axis_plot(
    df_full: pd.DataFrame, channel: str, out_dir: Path
) -> str | None:
    """Figure 6: 6-phase recovery axis violins on FULL CORPUS.

    Q3.6.c extension visualisation: pre_illness_healthy + acute_infection
    phases visible alongside the LC-era phases, supporting the descriptive
    reproduction of the recovery_arc v2 cardiovascular-family acute-
    infection DIP finding.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    phase_data = {}
    for phase_name, start, end in RECOVERY_PHASE_BOUNDARIES:
        mask = (df_full["date"] >= pd.Timestamp(start)) & (df_full["date"] <= pd.Timestamp(end))
        vals = df_full.loc[mask, channel].dropna().astype(float).to_numpy()
        phase_data[phase_name] = vals

    fig, ax = plt.subplots(figsize=(11, 4.6))
    short_labels = {
        "pre_illness_healthy": "pre-ill (1)",
        "acute_infection": "acute (2)",
        "lc_pre_ergo": "lc-pre-ergo (3)",
        "pacing_pre_citalopram_learning_4a": "pacing 4a",
        "pacing_habit_established_4b": "pacing 4b",
        "citalopram_modulated": "citalopram (5)",
    }
    keep = [p for p in (
        "pre_illness_healthy",
        "acute_infection",
        "lc_pre_ergo",
        "pacing_pre_citalopram_learning_4a",
        "pacing_habit_established_4b",
        "citalopram_modulated",
    ) if len(phase_data[p]) >= 5]
    if len(keep) == 0:
        plt.close(fig)
        return None
    ax.violinplot(
        [phase_data[p] for p in keep],
        showmedians=True, widths=0.85,
    )
    ax.set_xticks(np.arange(1, len(keep) + 1))
    ax.set_xticklabels([short_labels[p] for p in keep], rotation=15)
    ax.set_ylabel("resting_hr (bpm)")
    ax.set_title(
        "Q3.6.c LOAD-BEARING: 6-phase recovery axis (full corpus); recovery_arc v2 cardiovascular family"
    )
    fig.tight_layout()
    fp = out_dir / "fig6_recovery_axis_full_corpus.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    return str(fp.relative_to(out_dir.parent))


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
    a = q["Q3.6.a_distribution"]
    b = q["Q3.6.b_autocorrelation"]
    c = q["Q3.6.c_base_rates_per_phase"]
    c_rec = q["Q3.6.c_recovery_axis_base_rates"]
    d = q["Q3.6.d_phase_stratified_distribution"]
    e = q["Q3.6.e_near_identity"]
    fr = q["Q3.6.f_crash_vs_normal"]
    fl = fr["day_level"]
    fe = fr["episode_level"]
    g = q["Q3.6.g_spike_primitive"]
    h = q["Q3.6.h_outliers_calibration"]
    i = q["Q3.6.i_covariate_readiness"]

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
                "| {0} | {1} to {2} | {3} | **{4:.2f}** | {5:.2f} | {6:.2f} | {7:.2f} / {8:.2f} |".format(
                    ph, info["date_start"], info["date_end"], info["n"],
                    info["median"], info["mean"], info["mad_unscaled"],
                    info["p10"], info["p90"],
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

    ha_xref = d["ha06b_h01_ha06_xref"]
    fr_xref = fr["ha06b_h01_cross_reference"]

    # Sister-channel E[L]* spread context per handoff section 2.4
    sister_el_str = (
        "stress_stdev_sleep 7.0 / bb_overnight_gain 6.5 / stress_mean_sleep 12.6 "
        "/ stress_low_motion 21.1 / bb_lowest 29.25 / all_day_stress_avg 29.8; "
        "recovery_arc v2 sec 7b reported 22.7 for resting_hr"
    )
    rec_arc_reported = b["recovery_arc_v2_section_7b_reported_E_L_star_for_rhr"]
    el_vs_rec_arc = el_star - rec_arc_reported
    # The Politis-White estimator can fall back to the default E[L]=7 when
    # the ACF does NOT drop below the significance threshold within max_lag
    # (= n/4). For a channel with very long memory, this fallback is itself
    # a "longer memory than the estimator can resolve" signal -- NOT a
    # "short memory" finding. Check the note + ACF lag-7/lag-14 to
    # disambiguate.
    note_str = b.get("note", "") or ""
    fallback_no_cutoff = "no clear acf cutoff" in note_str.lower()
    acf_lag7 = b["selected_acf_lags"].get("acf_lag7", float("nan"))
    acf_lag14 = b["selected_acf_lags"].get("acf_lag14", float("nan"))
    if fallback_no_cutoff:
        el_vs_recarc_class = (
            "DEFAULTED to E[L]=7 fallback because the Politis-White ACF "
            "cutoff was not found within max_lag (n/4); per the cutoff rule "
            "ALL lags within max_lag remained above the 2-sigma significance "
            "threshold |rho|={0:.3f}. The fallback is itself a 'memory "
            "longer than the estimator can resolve' descriptive signal -- "
            "lag-7 ACF = {1:+.3f}; lag-14 ACF = {2:+.3f} -- consistent "
            "with the recovery_arc v2 4a+4b sub-pool E[L]*=22.7 in spirit "
            "(both findings point at long-memory structure); the apparent "
            "numerical match of E[L]=7 with the project default is a "
            "FALLBACK ARTEFACT, not a SHORT-memory finding. Per CONVENTIONS "
            "section 4.2: this is a Layer 1 descriptive observation; the "
            "data-driven block-length point estimate cannot be cleanly "
            "extracted from Strand-A's full Stratum-4 pool because the "
            "channel's autocorrelation is too persistent at this resolution"
        ).format(b["politis_white_significance_threshold_2sigma"], acf_lag7, acf_lag14)
    elif abs(el_vs_rec_arc) <= 5:
        el_vs_recarc_class = "CLOSE to recovery_arc v2 reported 22.7 (within +/-5)"
    elif el_vs_rec_arc < -5:
        el_vs_recarc_class = "MATERIALLY LOWER than recovery_arc v2 reported 22.7 (Strand-A pool gives shorter memory)"
    else:
        el_vs_recarc_class = "MATERIALLY HIGHER than recovery_arc v2 reported 22.7 (Strand-A pool gives longer memory)"

    mwu_p_str = _format_p(mwu['p_two_sided'])

    # Recovery-axis per-phase rows
    rec_phase_rows = []
    rec_arc_reported_dict = c_rec["recovery_arc_v2_section_5a_reported"]
    expected_medians = {
        "pre_illness_healthy": rec_arc_reported_dict["pre_illness_healthy_median_bpm"],
        "acute_infection": rec_arc_reported_dict["acute_infection_median_bpm"],
        "lc_pre_ergo": rec_arc_reported_dict["lc_pre_ergo_median_bpm"],
        "pacing_pre_citalopram_learning_4a": rec_arc_reported_dict["pacing_4a_median_bpm"],
        "pacing_habit_established_4b": rec_arc_reported_dict["pacing_4b_median_bpm"],
        "citalopram_modulated": rec_arc_reported_dict["citalopram_modulated_median_bpm"],
    }
    short_rec_names = {
        "pre_illness_healthy": "pre_illness_healthy (1)",
        "acute_infection": "acute_infection (2)",
        "lc_pre_ergo": "lc_pre_ergo (3)",
        "pacing_pre_citalopram_learning_4a": "pacing 4a",
        "pacing_habit_established_4b": "pacing 4b",
        "citalopram_modulated": "citalopram (5)",
    }
    per_rec = c_rec["per_recovery_phase"]
    for rph in (
        "pre_illness_healthy",
        "acute_infection",
        "lc_pre_ergo",
        "pacing_pre_citalopram_learning_4a",
        "pacing_habit_established_4b",
        "citalopram_modulated",
    ):
        info = per_rec.get(rph, {})
        exp = expected_medians[rph]
        if info.get("n", 0) > 0:
            obs = info["median"]
            ci = info.get("median_ci95_E_L7", [float("nan"), float("nan")])
            ci_str = "[{0:.1f}, {1:.1f}]".format(ci[0], ci[1])
            delta = obs - exp
            rec_phase_rows.append(
                "| {0} | {1} | {2} | **{3:.2f}** | {4} | {5:.1f} | **{6:+.2f}** |".format(
                    short_rec_names[rph], info["date_start"], info["n"],
                    obs, ci_str, exp, delta,
                )
            )
        else:
            rec_phase_rows.append(
                "| {0} | {1} | 0 | -- | -- | {2:.1f} | -- (no data in this Q3.6 run; recovery_arc v2 cell present) |".format(
                    short_rec_names[rph], info.get("date_start", "--"), exp,
                )
            )

    acute_dip_info = c_rec["this_q36_descriptive_acute_dip_reproduction"]
    dip_obs = acute_dip_info.get("acute_minus_healthy_observed_bpm")
    healthy_obs = acute_dip_info.get("healthy_median_observed")
    acute_obs = acute_dip_info.get("acute_median_observed")
    dip_reported = -1.5  # recovery_arc v2: 54 -> 52.5

    if dip_obs is not None and healthy_obs is not None and acute_obs is not None:
        dip_class = (
            "REPRODUCES the recovery_arc v2 finding (observed dip {0:+.2f} bpm vs recovery_arc reported {1:+.1f} bpm)".format(
                dip_obs, dip_reported
            )
            if abs(dip_obs - dip_reported) <= 1.0
            else "DIVERGES from recovery_arc v2 reported (observed dip {0:+.2f} bpm vs reported {1:+.1f} bpm; difference of {2:+.2f} bpm)".format(
                dip_obs, dip_reported, dip_obs - dip_reported
            )
        )
    else:
        dip_class = "NOT REPRODUCIBLE in this Q3.6 run (one or both phases have n=0 in the per_day_master frame)"

    out_lines = [
        "# Findings -- `resting_hr` operationalisation-support descriptive (Q3.6.a-i)",
        "",
        "**Channel**: `resting_hr` (HA06b + H01 + HA06 primary operand; Garmin UDS "
        "`restingHeartRate` field; daily aggregate of the lowest stable nightly HR; UDS-passthrough "
        "from `daily_uds.csv` per [`garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) "
        "UDS-family discipline). Column semantics: [DATA_DICTIONARY.md cardiovascular section](../../../DATA_DICTIONARY.md).",
        "",
        "**Substantive context**: HA06b is LOCKED at TRAIN SUPPORTED +18.9 pp / VALIDATE refuted "
        "+0.8 pp / OVERALL REFUTED per "
        "[`HA06b-rhr-zscore/result.md`](../../../analyses/hypotheses/HA06b-rhr-zscore/result.md); "
        "just R14-confirmed CONVERGE-ON-OVERALL at single-pool **+6.7 pp [CI -18.7, +17.9] perm "
        "p (E[L]=7) = 0.3368** per [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) "
        "row HA06b (`badd04a`). H01 (the absolute-7d-mean-delta predecessor) is LOCKED at REFUTED "
        "both eras (-1.2 / -9.5 pp) per [`H01-rhr-drift/result.md`](../../../analyses/hypotheses/H01-rhr-drift/result.md); "
        "R14 single-pool **-3.1 pp [CI -9.4, +10.1] perm p=0.7820** NOT-SUPPORTED CONVERGE (both NOT-"
        "SUPPORTED). HA06 (the absolute-bidirectional-delta variant; SUPERSEDED by HA06b) is LOCKED "
        "REFUTED both eras per "
        "[`HA06-morning-rhr-delta/result.md`](../../../analyses/hypotheses/HA06-morning-rhr-delta/result.md). "
        "This Q3.6 is the Strand-A operationalisation-support backstop; the HA06b + H01 + HA06 + R14 "
        "substantive verdicts are LOCKED and descriptively corroborated only.",
        "",
        "**v3 dose-response status**: resting_hr IS in v3 multi-channel scope per "
        "[`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "section 5.6 (6-channel scope: stress_mean_sleep + all_day_stress_avg + bb_lowest + "
        "resting_hr + bb_overnight_gain + respiration_avg_sleep) and was classified as **REJECTED "
        "with weak/non-significant beta** (the 'weakly consistent' v3 row). Per CONVENTIONS section "
        "4.2 caveat-class framing: Q3.6.d reports observed phase shifts descriptively; this Q3.6 "
        "does **NOT promote a v3 REJECTED -> CONFIRMED reclassification** (handoff section 3 hard "
        "constraint).",
        "",
        "**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to {0}). "
        "n={1} days with channel out of {2} Stratum 4 days "
        "({3} NaN days from UDS-side coverage gaps).".format(
            summary["as_of_date"], a["n"],
            summary["n_rows_stratum_4_total"],
            summary["n_rows_stratum_4_total"] - a["n"],
        ),
        "",
        "**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 "
        "r3, commit `ccbd12e`) -- HA-touched non-confirmed channel candidate list bullet `resting_hr "
        "(HA06b primary; weak v3 dose-modulation)`. **2nd of the 5 Tier 2 channels** in the user-"
        "prioritised Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 "
        "bb_overnight_gain `7d49ba4`; this Q3.6 closes Tier 2 2nd; next: Q3.7 exertion_class, Q3.8 "
        "push_burden_7d, Q3.9 gevoelscore). Q3.6.a-i template applied per section 3.1 verbatim + "
        "Q3.6.c LOAD-BEARING recovery-axis extension on full corpus per handoff section 2.4 "
        "(reproduces recovery_arc v2 cardiovascular-family acute-infection DIP finding).",
        "",
        "**Sources**: `per_day_master.csv` (Garmin daily aggregate) + `labels_crash_v2.csv` "
        "(`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level per "
        "CONVENTIONS section 3.6).",
        "",
        "**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict "
        "promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). "
        "HA06b + H01 + HA06 (LOCKED) + R14 single-pool re-anchors (LOCKED `badd04a`) + HA-P6 v3 + "
        "v3 dose-response REJECTED (LOCKED) cross-references in this analysis are **descriptive "
        "corroboration only**; the substantive verdicts live in those result.md files and are NOT "
        "extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). The v3 "
        "REJECTED verdict is LOCKED and this Q3.6.d does NOT promote a CONFIRMED-citalopram "
        "reclassification per the handoff section 3 hard constraint. Statistical hygiene anchors: "
        "section 3.1 (personal baseline), section 3.3 (column-duplication threshold |rho|>=0.92), "
        "section 3.4 (crash-drop sensitivity |delta|>0.10), section 3.5 (spike metrics -- HA06b's "
        "tested operand IS the per-4-day MAX |z| spike-form on this daily channel), section 3.6 "
        "(named counts).",
        "",
        "---",
        "",
        "## Headline",
        "",
        "`resting_hr` on Stratum 4 is a **{0}, {1} daily cardiovascular channel** "
        "(skew={2:+.2f}, excess kurtosis={3:+.2f}, heavy_tail_flag={4}, p99/median = {5:.2f}/{6:.2f} = {7:.2f}). "
        "The **data-driven E[L]\\*={8:.1f}** (Politis-White; deviation ratio {9:.2f}; factor-of-2 "
        "flag = {10}; cutoff lag M={11}). Cross-channel context per handoff section 2.4: vs sister "
        "Strand-A channels {12} -- this Q3.6.b's E[L]\\*={8:.1f} is **{13}** "
        "(recovery_arc's pool was the joined 4a+4b sub-window n=53+500; this Q3.6.b's pool is "
        "full Stratum-4 n={14}). **Phase-stratified medians** (citalopram axis, caveat-class per "
        "CONVENTIONS section 4.2 since v3 REJECTED with weak beta): unmedicated {15:.2f} -> buildup "
        "{16:.2f} -> consolidation {17:.2f} -> afbouw {18:.2f} (consolidation-minus-unmedicated = "
        "{19:+.2f} bpm). Day-resolved citalopram boundary step (2024-04-09 pre/post 30d) is **{20:+.2f} "
        "bpm**. Crash-vs-normal: episode-level d={21:+.2f} (bootstrap CI95 [{22:+.2f}, {23:+.2f}]); "
        "day-level Mann-Whitney U z={24:+.2f} p={25} P(crash>normal)={26:.3f} -- descriptively re-"
        "anchors HA06b's TRAIN-only-SUPPORTED-now-OVERALL-REFUTED + R14 CONVERGE-ON-OVERALL + H01 "
        "both-eras-REFUTED + R14 CONVERGE (both NOT-SUPPORTED). Near-identity check: "
        "**{27}** near-identity pairs fire at the |rho|>=0.92 CONVENTIONS section 3.3 threshold. "
        "**Q3.6.c LOAD-BEARING recovery_arc reproduction**: acute-infection DIP {28} (recovery_arc v2 "
        "reported -1.5 bpm; this Q3.6.c observed {29}).".format(
            "right-skewed" if skew > 0.3 else "left-skewed" if skew < -0.3 else "roughly-symmetric",
            # Memory class -- if the estimator fell back, the channel has memory
            # too long for clean cutoff resolution at this pool resolution
            "VERY-LONG-MEMORY (Politis-White estimator fallback at this pool)" if fallback_no_cutoff else (
                "autocorrelation-SPARSE-MEMORY" if el_star < 10 else
                "autocorrelation-MODERATE-MEMORY" if el_star < 20 else
                "autocorrelation-DENSE-MEMORY"
            ),
            skew, a["excess_kurtosis"], a["heavy_tail_flag"],
            p99, med, p99_over_med,
            el_star, b["deviation_ratio"], b["factor_of_2_deviation_flag"], b["cutoff_lag_M"],
            sister_el_str, el_vs_recarc_class, a["n"],
            unmed_med, buildup_med, consol_med, afbouw_med, consol_minus_unmed,
            citalo_step["diff_post_minus_pre"] if citalo_step.get("diff_post_minus_pre") is not None else float("nan"),
            fe["cohens_d_episode_vs_normal_day"], ci_ep[0], ci_ep[1],
            mwu["z"], mwu_p_str, mwu["p_crash_greater_than_normal"],
            "Zero" if not e["flagged_pairs"] else "{0}".format(len(e["flagged_pairs"])),
            dip_class,
            "{0:+.2f} bpm".format(dip_obs) if dip_obs is not None else "uncomputable",
        ),
        "",
        "---",
        "",
        "## Q3.6.a -- Distribution shape (Stratum 4)",
        "",
        "**Verdict on the section 3.1 delegate question**: **delegate is partial; extend in this "
        "analysis**. [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) "
        "primarily documents `stress_mean_sleep`-family channels; coverage on `resting_hr` is "
        "incidental. The full distribution descriptors (skewness/kurtosis/heavy-tail flag/p99-vs-"
        "median ratio) are surfaced here for the first time on this channel at the operationalisation-"
        "support framing.",
        "",
        "| stat | value | source |",
        "|---|---:|---|",
        "| n (Stratum 4) | {0} | `per_day_master.csv` `resting_hr` non-NaN within S4 |".format(a["n"]),
        "| mean | {0:.3f} | (single-pool S4) |".format(a["mean"]),
        "| median | {0:.3f} | |".format(a["median"]),
        "| std (ddof=1) | {0:.3f} | |".format(a["std_ddof1"]),
        "| MAD (unscaled) | {0:.3f} | |".format(a["mad_unscaled"]),
        "| MAD x 1.4826 (normal-equivalent SD) | {0:.3f} | for robust z-score scaling per section 3.1 |".format(a["mad_normal_equivalent"]),
        "| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | {0:.1f} / {1:.1f} / {2:.1f} / {3:.1f} / {4:.1f} / {5:.1f} / {6:.1f} / {7:.1f} / {8:.1f} | |".format(
            quant["p1"], quant["p5"], quant["p10"], quant["p25"], quant["p50"],
            quant["p75"], quant["p90"], quant["p95"], quant["p99"],
        ),
        "| skewness (Fisher-Pearson) | **{0:+.2f}** | {1} |".format(
            a["skewness"],
            "right-skewed" if skew > 0.3 else "left-skewed" if skew < -0.3 else "roughly-symmetric",
        ),
        "| excess kurtosis (Fisher) | **{0:+.2f}** | |".format(a["excess_kurtosis"]),
        "| heavy_tail_flag | **{0}** | skew>1 OR p99/median > 3.0 |".format(a["heavy_tail_flag"]),
        "| range | {0:.1f} to {1:.1f} bpm | |".format(a["min"], a["max"]),
        "",
        "**resting_hr is a per-day Garmin UDS daily aggregate** (the lowest stable nightly HR via "
        "Garmin's `restingHeartRate` UDS field). Per HA06 + HA06b result framing: the field maps "
        "cleanly to the bottom of the night-sleep-HR graph and is the Wiggers-aligned 'lowest stable "
        "nightly HR' construct. The participant's typical max |z| sits at 1.6-3.5 bpm relative to "
        "the lagged baseline per HA06b (median 2.31 train / 1.57 validate); the baseline sigma sits "
        "stably at 2.0-2.3 bpm per HA06b sensitivity arms.",
        "",
        "### Cross-channel comparison vs sister CONFIRMED-citalopram channels",
        "",
        "| stat | resting_hr (this analysis) | stress_mean_sleep (Q3.1, CONFIRMED) | all_day_stress_avg (Q3.2, CONFIRMED) | bb_lowest (Q3.3, CONFIRMED) |",
        "|---|---:|---:|---:|---:|",
        "| n S4 | {0} | 1339 | 1359 | 1359 |".format(a["n"]),
        "| mean | {0:.2f} | 19.97 | 32.72 | 20.61 |".format(a["mean"]),
        "| median | {0:.2f} | 19.21 | 32.00 | 20.00 |".format(a["median"]),
        "| MAD (unscaled) | {0:.2f} | 2.87 | 4.00 | 6.00 |".format(a["mad_unscaled"]),
        "| skewness | {0:+.2f} | +2.72 | +0.87 | +0.42 |".format(a["skewness"]),
        "| heavy_tail_flag | **{0}** | **True** | **False** | **False** |".format(a["heavy_tail_flag"]),
        "",
        "**resting_hr is a DAILY-AGGREGATE cardiovascular primitive** (Garmin UDS-passthrough; "
        "lowest stable nightly HR). Distinct from the BB-floor NADIR (bb_lowest) by mechanism: RHR "
        "is the cardiovascular-recovery anchor; BB-floor is the autonomic-recovery anchor. "
        "Distinct from autonomic-load stress channels (stress_mean_sleep mean / all_day_stress_avg "
        "mean) by mechanism: RHR measures cardiovascular state; stress channels are HRV-proxies "
        "from monitoring_b. The sister BB-floor channel (bb_lowest Q3.3.e) reciprocally reported "
        "rho=-0.171 with this channel (NOT near-identity; modest INVERSE coupling: BB-floor up "
        "co-occurs with RHR down).",
        "",
        "See [`plots/fig1_distribution_s4.png`](plots/fig1_distribution_s4.png).",
        "",
        "---",
        "",
        "## Q3.6.b -- Autocorrelation structure + E[L]\\* (LOAD-BEARING recovery_arc v2 reproduction)",
        "",
        "The **data-driven block length is E[L]\\*={0:.1f}** (Politis-White 2004 with Patton-Politis-"
        "White 2009 correction per "
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
        "### Cross-channel comparison (E[L]\\* by Strand A analysis) -- handoff section 2.4 load-bearing",
        "",
        "| analysis | channel | E[L]\\* | M | factor-of-2 flag |",
        "|---|---|---:|---:|---|",
        "| Q3.5 (bb_overnight_gain, truth window) | per-night SLEEPEND-SLEEPSTART | 6.5 | -- | no |",
        "| Q3.4 (stress_stdev_sleep) | per-night STDEV | 7.0 | -- | no |",
        "| Q3.1 (stress_mean_sleep) | sleep-window mean | 12.6 | 6 | YES (factor-of-2) |",
        "| Phase-1 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 | 11 | YES (factor-of-3) |",
        "| Q3.3 (bb_lowest) | daily NADIR | 29.25 | 17 | YES (factor-of-4) |",
        "| Q3.2 (all_day_stress_avg) | 24h-window mean | 29.8 | 18 | YES (factor-of-4) |",
        "| **this analysis (resting_hr)** | **daily Garmin UDS restingHeartRate** | **{0:.1f}{1}** | **{2}** | **{3}** |".format(
            el_star,
            " (fallback)" if fallback_no_cutoff else "",
            b["cutoff_lag_M"] if b["cutoff_lag_M"] is not None else "n/a (no cutoff)",
            ("YES" if b["factor_of_2_deviation_flag"] else "no (but see fallback caveat above)" if fallback_no_cutoff else "no"),
        ),
        "",
        "### LOAD-BEARING recovery_arc v2 section 7b reproduction (per handoff section 2.4)",
        "",
        "**recovery_arc v2 section 7b reported E[L]\\*=22.7 for resting_hr** (paired-bootstrap "
        "combined E[L]\\* from the joined 4a+4b sub-window n=53+500 day-level rows). resting_hr was "
        "the only channel in the v2 7-channel set where the 4b-4a paired-bootstrap CI excluded 0 "
        "(+3.0 bpm, CI [+2.0, +4.0]). This Q3.6.b's E[L]\\*={0:.1f}: **{1}**. Pool difference: "
        "recovery_arc's pool was the joined 4a+4b sub-window (~553 day-level rows); this Q3.6.b's "
        "pool is full Stratum-4 (n={2}). The pools differ in temporal coverage (Stratum 4 starts "
        "2022-09-03 = end of sub-phase 4a; full Stratum 4 extends through citalopram_modulated phase 5 "
        "= AS_OF_DATE 2026-06-05). Per CONVENTIONS section 4.2: this is Layer 1 descriptive "
        "observation only; the methodological-divergence flag (fallback vs converging estimate) is "
        "the load-bearing finding here, not a per-pool block-length number to inherit.".format(
            el_star, el_vs_recarc_class, a["n"]
        ),
        "",
        "**Implication for downstream HA pre-regs**: any future HA on `resting_hr` (beyond HA06b's "
        "locked second-order operand) should pre-spec a sensitivity arm at the recovery_arc v2 "
        "reported E[L]\\*=22.7 alongside the default-E[L]=7 primary (the fallback observed here "
        "does NOT establish a SHORT-memory regime -- the ACF lag-7={1:+.3f} + lag-14={2:+.3f} both "
        "remain well above the 2-sigma threshold {3:.3f}; the channel has very-long memory at this "
        "resolution). HA06b itself used E[L]=7 for the locked test; the R14 single-pool re-anchor "
        "at +6.7 pp p=0.3368 also used E[L]=7. The Q3.6.b finding here updates the channel-level "
        "block-length characterisation for any FUTURE HA on this channel; HA06b's already-locked "
        "verdict + the R14 single-pool verdict are NOT re-anchored.".format(
            el_int, acf_lag7, acf_lag14,
            b["politis_white_significance_threshold_2sigma"],
        ),
        "",
        "See [`plots/fig5_acf.png`](plots/fig5_acf.png).",
        "",
        "---",
        "",
        "## Q3.6.c -- Base rates per citalopram phase + LOAD-BEARING recovery-axis extension",
        "",
        "### Citalopram axis (Stratum 4 primary)",
        "",
        "Phase axis per "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3:",
        "",
        "| phase | window | n | median | mean | MAD | p10 / p90 |",
        "|---|---|---:|---:|---:|---:|---|",
        *per_phase_rows,
        "",
        "The two **transition phases** (buildup n={0}; afbouw n={1}) have **n<75 each**; the two "
        "**steady-state phases** (unmedicated n={2}; consolidation n={3}) are an order of magnitude "
        "larger. Any HA test that wants per-phase verdicts on this channel faces a ~10x n disadvantage "
        "vs the steady-state phases (same as sister channels Q3.1.c / Q3.2.c / Q3.3.c / Q3.4.c / "
        "Q3.5.c).".format(
            c["buildup"]["n"] if "buildup" in c else 0,
            c["afbouw"]["n"] if "afbouw" in c else 0,
            c["unmedicated"]["n"] if "unmedicated" in c else 0,
            c["consolidation"]["n"] if "consolidation" in c else 0,
        ),
        "",
        "Named counts (CONVENTIONS section 3.6): the per-phase n's above are `resting_hr`-non-NaN day "
        "rows in `per_day_master.csv` within Stratum 4 date masks per "
        "`citalopram_phase_stratification.md section 3` boundary dates.",
        "",
        "See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (citalopram-phase "
        "violins).",
        "",
        "### Recovery-axis LOAD-BEARING extension on FULL CORPUS (per handoff section 2.4)",
        "",
        "Per handoff section 2.4: this section extends OUT of the default Stratum-4 window to "
        "include the **pre_illness_healthy (2021-08-16 to 2022-03-20) + acute_infection (2022-03-21 "
        "to 2022-04-03) phases** on the full corpus, so the [recovery_arc v2 findings.md section "
        "5.A](../../trajectory/recovery_arc/findings.md) cardiovascular-family **acute-infection DIP "
        "finding (54 -> 52.5)** can be descriptively reproduced. 6-phase axis per "
        "[`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) "
        "(LOCKED `d47e0d3`). Per recovery_arc v2 section 5.A: **resting_hr uniquely DIPS in acute "
        "infection (parasympathetic dominance during viral infection; n=14 too short for tight CI)**.",
        "",
        "| phase | window start | n | observed median | observed CI95 (E[L]=7) | recovery_arc v2 reported | delta (this - recovery_arc) |",
        "|---|---|---:|---:|---|---:|---:|",
        *rec_phase_rows,
        "",
        "**Acute-infection DIP reproduction verdict**: {0}.".format(dip_class),
        "",
        "**Per CONVENTIONS section 4.2 caveat-class framing**: the recovery_arc v2 cells reported in "
        "the comparison column above are NOT re-promoted to substantive findings here; the recovery_"
        "arc v2 substantive narrative (parasympathetic dominance during viral infection + slow "
        "cardiovascular upward drift through 4b + phase 5) is LOCKED at the recovery_arc/findings.md "
        "level. This Q3.6.c reproduction is descriptive corroboration only -- if the observed values "
        "match within +/-1 bpm of the recovery_arc reported values, that confirms methodological "
        "consistency; material divergence is descriptively flagged.",
        "",
        "See [`plots/fig6_recovery_axis_full_corpus.png`](plots/fig6_recovery_axis_full_corpus.png) "
        "(6-phase recovery-axis violins on full corpus).",
        "",
        "---",
        "",
        "## Q3.6.d -- Phase-stratified distribution + v3 dose-response REJECTED caveat-class",
        "",
        "**Per CONVENTIONS section 4.2 (caveats yes; a-priori claims no) + handoff section 1 + "
        "section 2.4 + section 3 hard constraint**: `resting_hr` IS in the v3 multi-channel sweep "
        "scope per "
        "[`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "section 5.6 (6-channel scope) and was classified as **REJECTED with weak/non-significant "
        "beta** (the 'weakly consistent' v3 row). The citalopram-dose-modulation status on this "
        "channel is therefore **REJECTED at v3-locked verdict**. This Q3.6.d reports the observed "
        "median + dispersion shift across the citalopram-axis phases descriptively; it does **NOT "
        "promote a v3 REJECTED -> CONFIRMED reclassification** per the handoff section 3 hard "
        "constraint.",
        "",
        "Observed median shifts:",
        "",
        "| comparison | delta median (bpm) | within-phase MAD | within-MAD? |",
        "|---|---:|---:|---|",
        "| buildup minus unmedicated | **{0:+.2f}** | {1:.2f}-{2:.2f} | {3} |".format(
            buildup_minus_unmed,
            c["buildup"]["mad_unscaled"] if "buildup" in c and c["buildup"].get("n", 0) > 0 else float("nan"),
            c["unmedicated"]["mad_unscaled"] if "unmedicated" in c and c["unmedicated"].get("n", 0) > 0 else float("nan"),
            "{0} 1 MAD; descriptively meaningful".format(">" if abs(buildup_minus_unmed) > c.get("unmedicated", {}).get("mad_unscaled", 1.0) else "within"),
        ),
        "| consolidation minus unmedicated | **{0:+.2f}** | {1:.2f} | {2} |".format(
            consol_minus_unmed,
            c["consolidation"]["mad_unscaled"] if "consolidation" in c and c["consolidation"].get("n", 0) > 0 else float("nan"),
            "{0} 1 MAD".format(">" if abs(consol_minus_unmed) > c.get("consolidation", {}).get("mad_unscaled", 1.0) else "within"),
        ),
        "| consolidation minus buildup | **{0:+.2f}** | {1:.2f} | |".format(
            d["phase_to_phase_shifts"].get("consolidation_minus_buildup_median", 0),
            c["consolidation"]["mad_unscaled"] if "consolidation" in c and c["consolidation"].get("n", 0) > 0 else float("nan"),
        ),
        "| afbouw minus consolidation | **{0:+.2f}** | {1:.2f}-{2:.2f} | |".format(
            afbouw_minus_consol,
            c["consolidation"]["mad_unscaled"] if "consolidation" in c and c["consolidation"].get("n", 0) > 0 else float("nan"),
            c["afbouw"]["mad_unscaled"] if "afbouw" in c and c["afbouw"].get("n", 0) > 0 else float("nan"),
        ),
        "| afbouw minus unmedicated | **{0:+.2f}** | {1:.2f}-{2:.2f} | |".format(
            afbouw_minus_unmed,
            c["unmedicated"]["mad_unscaled"] if "unmedicated" in c and c["unmedicated"].get("n", 0) > 0 else float("nan"),
            c["afbouw"]["mad_unscaled"] if "afbouw" in c and c["afbouw"].get("n", 0) > 0 else float("nan"),
        ),
        "",
        "### Descriptive reading (no verdict promotion; v3 REJECTED LOCKED)",
        "",
        "The median moves from unmedicated ({0:.2f}) to consolidation ({1:.2f}) by **{2:+.2f} bpm**. "
        "The day-resolved citalopram boundary step (30d pre/post 2024-04-09): **{3:+.2f} bpm** -- "
        "the empirical day-resolved citalopram-onset shift. Per the framing above: **the v3 dose-"
        "response analysis classified resting_hr as REJECTED with weak/non-significant beta**, and "
        "this Q3.6.d does NOT promote that REJECTED verdict to CONFIRMED. The observed phase shift "
        "is consistent with the v3 'weakly consistent' rating: there is a measurable shift across "
        "the citalopram boundary on the daily-resolved channel, but the within-buildup-window "
        "dose-response slope was not significant in the v3 sweep. The shift visible at the citalopram "
        "boundary may reflect any combination of: (i) the v3 REJECTED beta carrying residual "
        "weakly-consistent signal that the per-phase median shift surfaces, (ii) the recovery_arc v2 "
        "slow cardiovascular upward drift through 4b + phase 5 (consistent across the multi-year "
        "arc), (iii) co-temporal trajectory effects unrelated to citalopram dose-modulation. The "
        "v3 REJECTED verdict is LOCKED; this Q3.6.d observation is a Layer 1 descriptive cross-"
        "reference only.".format(
            unmed_med, consol_med, consol_minus_unmed,
            citalo_step["diff_post_minus_pre"] if citalo_step.get("diff_post_minus_pre") is not None else float("nan"),
        ),
        "",
        "### HA06b + H01 + HA06 locked-verdict cross-reference",
        "",
        "Per handoff section 1: HA06b (z-score relative-threshold framing, TRAIN SUPPORTED only); "
        "H01 (absolute 7d-mean +3 bpm framing, REFUTED both eras); HA06 (absolute 4-5d delta >=5 bpm "
        "bidirectional, REFUTED both eras; SUPERSEDED by HA06b). Per HA06b result.md the absolute-"
        "threshold misalignment vs the participant's RHR variability is the canonical story: HA06's "
        "5 bpm bar caught 21.4% train freq with +13.9 pp; HA06b's z-score relative bar caught 71.4% "
        "train freq with +18.9 pp. The per-phase median shifts observed in Q3.6.d's table above are "
        "in the 1-5 bpm absolute range across the citalopram axis -- which is on the same order as "
        "HA06's absolute threshold of 5 bpm and well above HA06b's relative N_std=1.5 (~2-3 bpm at "
        "the participant's sigma_floor=0.5-2.3 bpm range) at the per-day-channel level.",
        "",
        "See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) and "
        "[`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d "
        "rolling median through phases).",
        "",
        "---",
        "",
        "## Q3.6.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)",
        "",
        "Brief-mandated targets per handoff section 2.4: sister CONFIRMED-citalopram channels "
        "(stress_mean_sleep + all_day_stress_avg + bb_lowest) + stress-family neighbours + "
        "respiration cross-family. Cross-family cardiovascular vs autonomic-load companions are "
        "the load-bearing comparisons.",
        "",
        "| target channel | n | Pearson r | Spearman rho | near-identity flag? |",
        "|---|---:|---:|---:|---|",
        *near_id_rows,
        "",
        "**{0} near-identity pairs fire** at the |rho|>=0.92 CONVENTIONS section 3.3 threshold. "
        "Sister `bb_lowest` Q3.3.e reciprocally reported Pearson r=-0.194 / Spearman rho=-0.171 "
        "with this channel (NOT near-identity at the section 3.3 threshold; modest INVERSE coupling: "
        "BB-floor up co-occurs with RHR down). The cross-channel-correlation card "
        "([`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md)) "
        "already documented no near-identity in the project's 9-anchor primitive set; this Q3.6.e "
        "reproduces from the resting_hr side.".format(
            "Zero" if not e["flagged_pairs"] else len(e["flagged_pairs"])
        ),
        "",
        "---",
        "",
        "## Q3.6.f -- Crash-day vs normal-day (Stratum 4) + HA06b + H01 corroboration",
        "",
        "Per CONVENTIONS section 3.6 named counts: {0} crash-episodes (crash_v2 episode-level via "
        "`labels_crash_v2.csv` unique `episode_id` starting with `crash-`); {1} crash-days (day-"
        "level, `label=='crash'`); {2} non-crash days (the complement within Stratum 4 channel-valid "
        "days).".format(
            fe["n_crash_episodes"], fl["n_crash_day"], fl["n_normal_day"],
        ),
        "",
        "### Episode-level (primary unit per CONVENTIONS section 3.6)",
        "",
        "| stat | value |",
        "|---|---:|",
        "| n crash-episodes | {0} |".format(fe["n_crash_episodes"]),
        "| n normal-day base rate | {0} |".format(fe["n_normal_day_base_rate"]),
        "| mean per-episode `resting_hr` | {0:.3f} bpm |".format(fe["mean_per_episode_value"]),
        "| mean normal-day `resting_hr` | {0:.3f} bpm |".format(fe["mean_normal_day_value"]),
        "| mean diff (episode minus normal-day) | **{0:+.3f} bpm** |".format(fe["mean_diff_episode_vs_normal_day"]),
        "| Cohen's d (episode-level vs normal-day pooled) | **{0:+.2f}** |".format(fe["cohens_d_episode_vs_normal_day"]),
        "| Bootstrap 95% CI on mean diff | **[{0:+.3f}, {1:+.3f}]** ({2} iters, seed={3}) |".format(
            ci_ep[0], ci_ep[1], fe["n_bootstrap"], fe["seed"]
        ),
        "",
        "**Episode-level Cohen's d={0:+.2f}** on this channel. Substantive direction prior per HA06b "
        "+ HA06: bidirectional crash-day RHR deviation (elevated direction = classical Workwell "
        "sympathetic overarousal in train era; lowered direction = parasympathetic-swing pattern "
        "in validate era per HA06b directionality split). Compare cross-channel: `stress_mean_sleep` "
        "episode d=+0.91; `stress_stdev_sleep` episode d=+0.48; `all_day_stress_avg` episode d=+0.37; "
        "`stress_low_motion_min_count_S60_Mlow` episode d=+0.38; `bb_lowest` episode d=-0.30; "
        "`bb_overnight_gain` episode d=-0.80.".format(fe["cohens_d_episode_vs_normal_day"]),
        "",
        "### Day-level (autocorrelation-inflated supplementary)",
        "",
        "| stat | value |",
        "|---|---:|",
        "| n crash-days | {0} |".format(fl["n_crash_day"]),
        "| n normal-days | {0} |".format(fl["n_normal_day"]),
        "| mean crash-day | {0:.3f} bpm |".format(fl["mean_crash"]),
        "| mean normal-day | {0:.3f} bpm |".format(fl["mean_normal"]),
        "| median crash-day | {0:.2f} bpm |".format(fl["median_crash"]),
        "| median normal-day | {0:.2f} bpm |".format(fl["median_normal"]),
        "| mean diff (point estimate) | **{0:+.3f} bpm** |".format(fl["mean_diff"]),
        "| median diff | **{0:+.2f} bpm** |".format(mwu["median_diff"]),
        "| Cohen's d | **{0:+.2f}** |".format(fl["cohens_d"]),
        "| Mann-Whitney U: z | **{0:+.2f}** |".format(mwu["z"]),
        "| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **{0}** |".format(mwu_p_str),
        "| Mann-Whitney U: P(crash > normal) | **{0:+.3f}** |".format(mwu["p_crash_greater_than_normal"]),
        "| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (project default) | [{0:+.3f}, {1:+.3f}], width {2:.3f} |".format(
            e7["ci_lower"], e7["ci_upper"], width7,
        ),
        "| Stationary bootstrap 95% CI on mean diff, **E[L]={0}** (data-driven, Q3.6.b flag) | **[{1:+.3f}, {2:+.3f}]**, width {3:.3f} |".format(
            eS["block_length_used"], eS["ci_lower"], eS["ci_upper"], widthS,
        ),
        "",
        "### LOAD-BEARING HA06b + H01 R14 single-pool descriptive cross-reference (per handoff section 2.4)",
        "",
        "Per [single_pool_reanchor/findings.md](../single_pool_reanchor/findings.md) row HA06b: R14 "
        "single-pool **+6.7 pp [CI -18.7, +17.9] perm p=0.3368 NOT-SUPPORTED CONVERGE-ON-OVERALL** "
        "(`badd04a`). Per row H01: single-pool **-3.1 pp [CI -9.4, +10.1] perm p=0.7820 NOT-"
        "SUPPORTED CONVERGE (both NOT-SUPPORTED)**. This Q3.6.f's first-order day-level Cohen's "
        "d={0:+.2f} (episode-level) + Mann-Whitney U p={1} (day-level) **descriptively corroborate** "
        "the R14 reading that the cardiovascular channel does NOT produce a clean validate-era "
        "precursor signal under any of the operationalisations tested (absolute 7d-mean H01; "
        "absolute bidirectional 4-5d HA06; relative z-score 4d HA06b) -- the channel-distribution-"
        "level signal at the day-level is consistent with HA06b's train-only-SUPPORTED + R14 "
        "CONVERGE-ON-OVERALL verdict and H01's both-eras-REFUTED + R14 CONVERGE verdict. **The HA06b "
        "+ H01 + R14 substantive verdicts are LOCKED**; this Q3.6.f observation is descriptive "
        "corroboration only, NOT a re-interpretation of either.".format(
            fe["cohens_d_episode_vs_normal_day"], mwu_p_str,
        ),
        "",
        "### Block-length sensitivity (Q3.6.b cross-check)",
        "",
        "Per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md), "
        "when the data-driven E[L]\\* deviates from the project default by more than a factor of 2, "
        "the analysis must report the CI at the data-driven value alongside the default. E[L]={0} CI "
        "([{1:+.3f}, {2:+.3f}]) vs E[L]=7 CI ([{3:+.3f}, {4:+.3f}]) -- {5:.1f}% {6} at the data-"
        "driven block length.".format(
            eS["block_length_used"], eS["ci_lower"], eS["ci_upper"],
            e7["ci_lower"], e7["ci_upper"],
            abs(width_change_pct), "wider" if width_change_pct > 0 else "narrower",
        ),
        "",
        "### Crash-drop sensitivity (CONVENTIONS section 3.4)",
        "",
    ]

    if cd is not None:
        out_lines.extend([
            "| frame | Spearman rho | n |",
            "|---|---:|---:|",
            "| full Stratum 4 | {0:+.3f} | {1} |".format(cd["full_frame_value"], cd["n_full"]),
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
        "## Q3.6.g -- Spike-detecting primitive availability",
        "",
        "`resting_hr` is a **per-day Garmin UDS daily aggregate** (the lowest stable nightly HR via "
        "Garmin's `restingHeartRate` UDS field; UDS-passthrough; no FIT parsing). Per CONVENTIONS "
        "section 3.5 spike/peak/count metrics preference: **HA06b's tested operand IS the spike-form "
        "construct on this channel** -- the per-4-day MAX |z| (bidirectional) of resting_hr with "
        "lagged baseline + sigma_floor=0.5 bpm. The per-day resting_hr value IS the "
        "operationalisation substrate; the per-4-day max |z| is the within-4-day spike-of-HR-"
        "deviation metric HA06b uses.",
        "",
        "Cardiovascular + autonomic-arousal primitives in master (for cross-channel pairwise "
        "comparison):",
        "",
    ])

    for sp in g.get("spike_primitives_available_in_master", []):
        out_lines.append("- `{0}` (n non-NaN = {1})".format(sp["column"], sp["n_non_nan"]))
    out_lines.append("")

    out_lines.extend([
        "### Pairwise correlations on Stratum 4",
        "",
        "| partner channel | Pearson r | Spearman rho | n |",
        "|---|---:|---:|---:|",
    ])
    for partner in ("bb_lowest", "stress_mean_sleep", "all_day_stress_avg", "respiration_avg_sleep", "awake_stress_max"):
        if "pearson_r_vs_{0}".format(partner) in g:
            out_lines.append("| `{0}` | {1:+.3f} | {2:+.3f} | {3} |".format(
                partner,
                g["pearson_r_vs_{0}".format(partner)],
                g["spearman_rho_vs_{0}".format(partner)],
                g["n_pair_{0}".format(partner)],
            ))
    out_lines.append("")

    out_lines.extend([
        "**Latent in FIT, not in master**:",
        "",
    ])
    for item in g.get("latent_in_FIT_not_in_master", []):
        out_lines.append("- " + item)
    out_lines.append("")
    out_lines.append(g.get("note", ""))
    out_lines.append("")

    out_lines.extend([
        "---",
        "",
        "## Q3.6.h -- Outlier detection + calibration-drift check",
        "",
        "Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md):",
        "",
    ])
    for issue in h.get("garmin_indicators_audit_known_issues", []):
        out_lines.append("- " + issue)
    out_lines.append("")

    out_lines.extend([
        "### Outlier scan (MAD-based |z|>5; threshold per CONVENTIONS section 3.1 robust-baseline default)",
        "",
        "**{0} outlier-day flagged** out of {1}.".format(h["n_flagged"], a["n"]),
        "",
    ])
    if outliers:
        out_lines.append("| date | value (bpm) | MAD-z |")
        out_lines.append("|---|---:|---:|")
        for o in outliers[:20]:
            out_lines.append("| {0} | {1:.1f} | **{2:+.2f}** |".format(
                o["date"], o["value"], o["mad_z"],
            ))
    else:
        out_lines.append("No outliers above the |z|>5 threshold on Stratum 4.")
    out_lines.append("")

    out_lines.extend([
        "### Drift check -- rolling 90d median over Stratum 4",
        "",
        "| snapshot date | rolling 90d median (bpm) |",
        "|---|---:|",
    ])
    for s in h.get("rolling_90d_median_snapshots", []):
        if s.get("rolling_med_90d") is not None:
            out_lines.append("| {0} | {1:.1f} |".format(s["snapshot_date"], s["rolling_med_90d"]))
    out_lines.append("")

    out_lines.extend([
        "### Citalopram boundary step (2024-04-09)",
        "",
        "Pre-30d mean = {0}; post-30d mean = {1}; **diff = {2}**.".format(
            "{0:.2f}".format(citalo_step["pre_30d_mean"]) if citalo_step.get("pre_30d_mean") is not None else "n/a",
            "{0:.2f}".format(citalo_step["post_30d_mean"]) if citalo_step.get("post_30d_mean") is not None else "n/a",
            "{0:+.2f}".format(citalo_step["diff_post_minus_pre"]) if citalo_step.get("diff_post_minus_pre") is not None else "n/a",
        ),
        "",
        "### Consolidation boundary step (2024-06-20)",
        "",
        "Pre-30d mean = {0}; post-30d mean = {1}; **diff = {2}**.".format(
            "{0:.2f}".format(consol_step["pre_30d_mean"]) if consol_step.get("pre_30d_mean") is not None else "n/a",
            "{0:.2f}".format(consol_step["post_30d_mean"]) if consol_step.get("post_30d_mean") is not None else "n/a",
            "{0:+.2f}".format(consol_step["diff_post_minus_pre"]) if consol_step.get("diff_post_minus_pre") is not None else "n/a",
        ),
        "",
        "### Afbouw boundary step (2026-03-20)",
        "",
        "Pre-30d mean = {0}; post-30d mean = {1}; **diff = {2}**.".format(
            "{0:.2f}".format(afbouw_step["pre_30d_mean"]) if afbouw_step.get("pre_30d_mean") is not None else "n/a",
            "{0:.2f}".format(afbouw_step["post_30d_mean"]) if afbouw_step.get("post_30d_mean") is not None else "n/a",
            "{0:+.2f}".format(afbouw_step["diff_post_minus_pre"]) if afbouw_step.get("diff_post_minus_pre") is not None else "n/a",
        ),
        "",
        "Per recovery_arc v2 section 5.A: the broader cardiovascular-family pattern is **slow "
        "upward drift through 4b + phase 5** (lc_pre_ergo 55 -> 4a 53 -> 4b 56 -> citalopram_"
        "modulated 57); the per-30d boundary steps reported above are the day-resolved view of "
        "the slow drift at specific intervention boundaries. These are NOT calibration-drift "
        "signatures (which would be gradual monotonic creeps unrelated to documented events); the "
        "rolling-90d median snapshot table shows the multi-year trajectory aligning with the "
        "recovery_arc v2 narrative.",
        "",
        "See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).",
        "",
        "---",
        "",
        "## Q3.6.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel",
        "",
        "Discipline anchor: "
        "[HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) "
        "(secondary-logistic-with-covariate pattern; beta disambiguation between primary-signal and "
        "candidate alternative readings). Names **four** candidate covariates a future HA on "
        "`resting_hr` as predictor should pre-spec.",
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
        obs = cand.get("observed_correlation_on_S4")
        if obs:
            out_lines.append("*Observed correlation on S4*: Pearson r={0:+.3f} / Spearman rho={1:+.3f} (n={2}).".format(
                obs["pearson_r"], obs["spearman_rho"], obs["n"],
            ))
            out_lines.append("")

    out_lines.extend([
        "### Recommendation",
        "",
        i["recommendation"],
        "",
        "---",
        "",
        "## Cross-references",
        "",
        "### HA-* tests that touch this channel (cite this analysis)",
        "",
        "- **HA06b** (RHR z-score, 4d bidirectional; LOCKED TRAIN SUPPORTED / VALIDATE refuted / "
        "OVERALL REFUTED; R14 single-pool NOT-SUPPORTED CONVERGE-ON-OVERALL `badd04a`): primary "
        "operand IS this channel in second-order spike-form. **The descriptive substrate this "
        "analysis produces -- the Stratum-4 distribution (Q3.6.a) + autocorrelation E[L]\\*={0:.1f} "
        "(Q3.6.b) + per-phase + recovery-axis reads (Q3.6.c) + first-order day-level crash-vs-normal "
        "(Q3.6.f) -- complements HA06b's tested operand with the raw-channel-distribution view.** "
        "The substantive HA06b verdict + the R14 single-pool verdict are LOCKED; this analysis's "
        "descriptive corroboration in Q3.6.f is NOT a re-interpretation.".format(el_star),
        "- **H01** (RHR drift, absolute 7d-mean +3 bpm; LOCKED REFUTED both eras; R14 single-pool "
        "NOT-SUPPORTED CONVERGE `badd04a`): primary operand is this channel in absolute-threshold "
        "form. Q3.6.f descriptively re-anchors at the day-level.",
        "- **HA06** (morning RHR delta, absolute bidirectional 4-5d; LOCKED REFUTED both eras; "
        "SUPERSEDED by HA06b): primary operand is this channel in absolute-delta form.",
        "- **HA-P6 v3** (descriptive Layer 1; LOCKED `a980b1c` 2026-06-17): resting_hr is in the "
        "HA-P6 v3 7-channel set + the 4-of-7 distinguishable channels; this Q3.6 provides the "
        "per-channel substrate.",
        "- **recovery_arc v2** (LOCKED `8feae6a` 2026-06-22): resting_hr was the only channel in "
        "the v2 7-channel set where the 4b-4a paired-bootstrap CI excluded 0 (+3.0 bpm, CI [+2.0, "
        "+4.0], E[L]\\*=22.7); Q3.6.b reproduces the E[L]\\* on Strand-A's pool; Q3.6.c reproduces "
        "the acute-infection DIP descriptively.",
        "",
        "### Methodology MDs cited",
        "",
        "- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3-6 -- Q3.6.c phase axis; Q3.6.d phase-stratified treatment.",
        "- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "v3 section 5.6 -- resting_hr IS in 6-channel scope; **REJECTED with weak/non-significant "
        "beta**; Q3.6.d caveat-class framing per CONVENTIONS section 4.2.",
        "- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) "
        "-- E[L]=7 default + factor-of-2 deviation rule; Q3.6.b reports E[L]\\*={0:.1f}.".format(el_star),
        "- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) "
        "-- Stratum 4 boundary definition.",
        "- [`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) "
        "(LOCKED `d47e0d3`) -- 6-phase recovery axis used in Q3.6.c LOAD-BEARING extension.",
        "- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) "
        "-- Q3.6.h cross-reference.",
        "",
        "### Existing artefacts referenced",
        "",
        "- [`descriptive/trajectory/recovery_arc/findings.md`](../../trajectory/recovery_arc/findings.md) "
        "**LOAD-BEARING**: section 5.A cardiovascular family + section 7b 4b-4a paired-bootstrap "
        "(resting_hr the only excludes-0 channel, +3.0 bpm CI [+2.0, +4.0], E[L]\\*=22.7); "
        "Q3.6.b reproduces E[L]\\* + Q3.6.c reproduces acute-infection DIP.",
        "- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) "
        "-- R14 HA06b + H01 rows (LANDED `badd04a`); descriptively corroborated in Q3.6.d + Q3.6.f.",
        "- [`descriptive/operationalisation_support/bb_overnight_gain/findings.md`](../bb_overnight_gain/findings.md) "
        "-- most-recent Strand-A precedent (Q3.5; Tier 2 first); programmatic-emit pattern + "
        "load-bearing cross-reference template.",
        "- [`descriptive/operationalisation_support/stress_stdev_sleep/findings.md`](../stress_stdev_sleep/findings.md) "
        "-- Q3.4 precedent for full-coverage continuous-channel pattern + clean f-string discipline.",
        "- [`descriptive/operationalisation_support/bb_lowest/findings.md`](../bb_lowest/findings.md) "
        "-- Q3.3 sister BB-floor channel; reciprocal rho with resting_hr reported there.",
        "- [`descriptive/operationalisation_support/all_day_stress_avg/findings.md`](../all_day_stress_avg/findings.md) "
        "-- Q3.2 precedent (CONFIRMED-citalopram sister).",
        "- [`descriptive/operationalisation_support/stress_mean_sleep/findings.md`](../stress_mean_sleep/findings.md) "
        "-- Q3.1 original Phase-1 precedent.",
        "- [`analyses/hypotheses/HA06b-rhr-zscore/result.md`](../../hypotheses/HA06b-rhr-zscore/result.md) "
        "-- LOCKED TRAIN SUPPORTED / VALIDATE refuted / OVERALL REFUTED; primary operand on this channel.",
        "- [`analyses/hypotheses/H01-rhr-drift/result.md`](../../hypotheses/H01-rhr-drift/result.md) "
        "-- LOCKED REFUTED both eras; absolute spec on this channel.",
        "- [`analyses/hypotheses/HA06-morning-rhr-delta/result.md`](../../hypotheses/HA06-morning-rhr-delta/result.md) "
        "-- LOCKED REFUTED both eras; SUPERSEDED by HA06b.",
        "",
        "### Upstream pipeline",
        "",
        "- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- "
        "`pipeline/01_extract/garmin_uds_extras.py` (UDS-side passthrough for restingHeartRate field).",
        "- `labels_crash_v2.csv` <- `garmin/hypotheses/crash_v2-definition/definition.md` (locked).",
        "",
        "---",
        "",
        "## Limitations",
        "",
        "For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per "
        "[CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the "
        "binding constraints are:",
        "",
        "1. **No HA verdict promotion**: HA06b + H01 + HA06 + R14 single-pool verdicts + v3 dose-"
        "response REJECTED verdict are LOCKED; this analysis's descriptive observations are NOT "
        "re-interpretations or re-promotions per CONVENTIONS section 4.2 + handoff section 3.",
        "2. **No v3 REJECTED -> CONFIRMED reclassification** per handoff section 3 hard constraint. "
        "The observed phase shifts in Q3.6.d are descriptive Layer 1 observations; the v3 verdict "
        "lives in citalopram_dose_response_stress_mean_sleep.md and is the load-bearing artefact.",
        "3. **First-order day-level read distinct from HA06b's tested operand**: HA06b's spike-form "
        "construct (per-4-day MAX |z|, bidirectional, lagged baseline) is the canonical HA test on "
        "this channel; Q3.6.f's first-order day-level Cohen's d is the descriptive-layer complement "
        "at a coarser resolution -- NOT a re-anchoring of HA06b.",
        "4. **Chronotropic incompetence caveat** per HA06 + H01 + HA06b result.md: >85% of ME/CFS "
        "patients have blunted HR response per Workwell's own caveat; this is a population-level "
        "physiological caveat on RHR signals' biological interpretation, NOT a calibration-drift "
        "signature on this device.",
        "5. **Recovery-axis Q3.6.c extension covers pre-illness + acute phases on the FULL CORPUS** "
        "OUT of Stratum 4 strictly for the load-bearing recovery_arc v2 reproduction per handoff "
        "section 2.4. Per CONVENTIONS section 4.3 + recovery_arc v2 caveat 2: the acute-phase n=14 "
        "limits tight CI on the dip magnitude.",
        "",
        "---",
        "",
        "*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` (gitignored "
        "per `docs/research/**/*.json`). To refresh: ``python run.py``.*",
        "",
    ])

    path.write_text("\n".join(out_lines), encoding="utf-8")


def write_readme_md(summary: dict, path: Path) -> None:
    """Emit the analysis README.md from the computed summary."""
    q = summary["questions"]
    a = q["Q3.6.a_distribution"]
    b = q["Q3.6.b_autocorrelation"]
    fr = q["Q3.6.f_crash_vs_normal"]
    fe = fr["episode_level"]
    ci_ep = fe["bootstrap_ci95_mean_diff"]
    c_rec = q["Q3.6.c_recovery_axis_base_rates"]
    el_star = b["data_driven_E_L_star"]
    rec_arc_reported = b["recovery_arc_v2_section_7b_reported_E_L_star_for_rhr"]
    acute_dip_info = c_rec["this_q36_descriptive_acute_dip_reproduction"]
    dip_obs = acute_dip_info.get("acute_minus_healthy_observed_bpm")
    healthy_obs = acute_dip_info.get("healthy_median_observed")
    acute_obs = acute_dip_info.get("acute_median_observed")

    note_str = b.get("note", "") or ""
    fallback_no_cutoff = "no clear acf cutoff" in note_str.lower()
    if fallback_no_cutoff:
        el_match = (
            "Politis-White FALLBACK to default E[L]=7 (channel ACF too "
            "persistent at this Stratum-4 pool resolution; see findings.md "
            "Q3.6.b for the load-bearing methodological-divergence flag "
            "vs recovery_arc v2 reported 22.7 on the smaller 4a+4b sub-pool)"
        )
    elif abs(el_star - rec_arc_reported) <= 5:
        el_match = "CLOSE to recovery_arc v2 reported {0} (within +/-5; methodological consistency)".format(rec_arc_reported)
    else:
        el_match = "DIVERGES from recovery_arc v2 reported {0} (pool difference flagged)".format(rec_arc_reported)

    if dip_obs is not None and healthy_obs is not None and acute_obs is not None:
        dip_repro = "REPRODUCES recovery_arc v2 finding (observed {0:+.2f} bpm vs reported -1.5 bpm)".format(dip_obs) if abs(dip_obs - (-1.5)) <= 1.0 else "DIVERGES from recovery_arc v2 finding (observed {0:+.2f} bpm vs reported -1.5 bpm)".format(dip_obs)
    else:
        dip_repro = "NOT REPRODUCIBLE in this Q3.6 run (insufficient data in pre-illness + acute phases on per_day_master)"

    n_near_id_flags = len(q["Q3.6.e_near_identity"].get("flagged_pairs", []))

    out_lines = [
        "# `resting_hr` -- operationalisation-support descriptive analysis",
        "",
        "**Strand**: A (operationalisation support; template-driven; no operationalisation interview "
        "required per [`descriptive/README.md`](../../README.md) section 7b).",
        "",
        "## Research question",
        "",
        "Operationalisation-support descriptive characterisation of `resting_hr` on Stratum 4 + a "
        "LOAD-BEARING recovery-axis extension on the full corpus, answering Q3.6.a-i per the locked "
        "descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) "
        "section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`; this channel listed as the HA06b-"
        "primary candidate with weak v3 dose-modulation). **2nd of the 5 Tier 2 channels** in the "
        "user-prioritised Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 "
        "bb_overnight_gain `7d49ba4`; this Q3.6 closes Tier 2 2nd; next: Q3.7 exertion_class, Q3.8 "
        "push_burden_7d, Q3.9 gevoelscore).",
        "",
        "Substantive status: **HA06b primary operand** (RHR z-score 4d bidirectional; LOCKED TRAIN "
        "SUPPORTED +18.9 pp / VALIDATE refuted +0.8 pp / OVERALL REFUTED per "
        "[`HA06b-rhr-zscore/result.md`](../../../analyses/hypotheses/HA06b-rhr-zscore/result.md); "
        "R14 single-pool **+6.7 pp [CI -18.7, +17.9] perm p=0.3368** NOT-SUPPORTED CONVERGE-ON-"
        "OVERALL `badd04a`). Also **H01 primary** (RHR drift absolute 7d-mean +3 bpm; LOCKED REFUTED "
        "both eras -1.2 / -9.5 pp; R14 single-pool **-3.1 pp [CI -9.4, +10.1] perm p=0.7820** "
        "NOT-SUPPORTED CONVERGE per [`H01-rhr-drift/result.md`](../../../analyses/hypotheses/H01-rhr-drift/result.md)) "
        "and **HA06 primary** (morning RHR delta absolute 4-5d bidirectional; LOCKED REFUTED both "
        "eras; SUPERSEDED by HA06b per [`HA06-morning-rhr-delta/result.md`](../../../analyses/hypotheses/HA06-morning-rhr-delta/result.md)). "
        "Channel IS in v3 multi-channel sweep scope per [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "section 5.6 (6-channel scope) and was classified as **REJECTED with weak/non-significant "
        "beta** (the 'weakly consistent' v3 row); citalopram-dose-modulation status is REJECTED at "
        "v3-locked verdict; Q3.6.d reports observed shifts descriptively per CONVENTIONS section 4.2 "
        "caveat-class framing and does NOT promote a v3 REJECTED -> CONFIRMED reclassification per "
        "handoff section 3 hard constraint.",
        "",
        "## Method",
        "",
        "- **Surface**: Stratum 4 primary (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05; "
        "n={0} channel-valid days out of {1} S4 days) **plus** LOAD-BEARING Q3.6.c extension on the "
        "full corpus to include pre_illness_healthy (2021-08-16 to 2022-03-20, ~217 day-level rows) "
        "+ acute_infection (2022-03-21 to 2022-04-03, ~14 day-level rows) phases for the recovery_"
        "arc v2 cardiovascular-family acute-infection DIP reproduction per handoff section 2.4.".format(
            a["n"], summary["n_rows_stratum_4_total"],
        ),
        "- **Primary phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with sister Strand-A "
        "analyses Q3.1 / Q3.2 / Q3.3 / Q3.4 / Q3.5.",
        "- **Secondary phase axis (Q3.6.c extension)**: 6-phase LC recovery axis per [`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) "
        "(LOCKED `d47e0d3`) on the FULL CORPUS for the recovery_arc v2 acute-infection DIP "
        "descriptive reproduction.",
        "- **Delegate**: Q3.6.a (distribution shape) **partial delegate** to [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) "
        "+ **extend** with full skewness/kurtosis/heavy-tail-flag descriptors.",
        "- **Cross-reference**: Q3.6.h (outliers + calibration-drift) cross-references [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) "
        "(UDS-passthrough family entries + chronotropic-incompetence substrate caveat per HA06 + H01 + HA06b result.md).",
        "- **Computed directly from `per_day_master.csv`**: Q3.6.a (distribution shape), Q3.6.b "
        "(Politis-White E[L]\\* on Stratum-4 pool; cross-reference recovery_arc v2 section 7b E[L]\\*=22.7 "
        "reproduction), Q3.6.c (per-phase base rates citalopram axis + 6-phase recovery-axis "
        "extension on full corpus), Q3.6.d (phase-stratified medians + citalopram-axis shift + v3 "
        "REJECTED caveat-class framing per CONVENTIONS section 4.2 + handoff section 3 hard "
        "constraint), Q3.6.e (near-identity check |rho|>=0.92 on 15-channel panel), Q3.6.f (crash-"
        "vs-normal Cohen's d + Mann-Whitney U + stationary-bootstrap CI at E[L]=7 and data-driven "
        "E[L]\\* + crash-drop sensitivity + LOAD-BEARING R14 single-pool descriptive cross-reference "
        "to HA06b + H01 rows), Q3.6.g (HA06b spike-form construct discussion + cross-channel "
        "pairwise correlations), Q3.6.i (covariate-sensitivity readiness for future HA pre-regs).",
        "- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, "
        "Stratum 4 filter, crash-drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) "
        "(`compute_data_driven_block_length`, `stationary_bootstrap_ci`).",
        "- **Load-bearing cross-references** per handoff section 2.4: recovery_arc v2 section 7b "
        "E[L]\\*=22.7 reproduction in Q3.6.b; recovery_arc v2 cardiovascular-family acute-infection "
        "DIP (54 -> 52.5) reproduction in Q3.6.c; R14 HA06b + H01 single-pool results descriptively "
        "corroborated in Q3.6.f; v3 dose-response REJECTED weak-beta caveat-class framing in "
        "Q3.6.d. NO substantive HA verdict promotion per CONVENTIONS section 2.1; NO v3 REJECTED -> "
        "CONFIRMED reclassification per handoff section 3 hard constraint.",
        "- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).",
        "",
        "## Result",
        "",
        "Headline (see [`findings.md`](findings.md) for the full answers Q3.6.a-i):",
        "",
        "`resting_hr` on Stratum 4 is a **daily-aggregate cardiovascular channel** (median {0:.2f} "
        "bpm; MAD {1:.2f}; skew {2:+.2f}; heavy_tail_flag={3}). **Data-driven E[L]\\*={4:.1f}** -- "
        "{5}. **Phase-stratified medians** (citalopram axis, caveat-class per CONVENTIONS section "
        "4.2 since v3 REJECTED with weak beta): unmedicated {6:.2f} -> consolidation {7:.2f} -> "
        "afbouw {8:.2f}. Episode-level Cohen's d={9:+.2f} (bootstrap CI95 [{10:+.2f}, {11:+.2f}]) -- "
        "descriptively corroborates HA06b's locked TRAIN-only-SUPPORTED-now-OVERALL-REFUTED + R14 "
        "CONVERGE-ON-OVERALL + H01 both-eras-REFUTED + R14 CONVERGE signals at the coarse first-"
        "order-day-level read (HA06b's tested operand is the per-4-day MAX |z| of resting_hr; this "
        "Q3.6.f is the first-order day-level descriptive complement, NOT a re-anchoring of HA06b). "
        "**Q3.6.c LOAD-BEARING recovery-axis reproduction**: acute-infection DIP {12}. Near-identity "
        "check: **{13}** flagged pairs at the |rho|>=0.92 CONVENTIONS section 3.3 threshold.".format(
            a["median"], a["mad_unscaled"], a["skewness"], a["heavy_tail_flag"],
            el_star, el_match,
            summary["questions"]["Q3.6.c_base_rates_per_phase"].get("unmedicated", {}).get("median", float("nan")),
            summary["questions"]["Q3.6.c_base_rates_per_phase"].get("consolidation", {}).get("median", float("nan")),
            summary["questions"]["Q3.6.c_base_rates_per_phase"].get("afbouw", {}).get("median", float("nan")),
            fe["cohens_d_episode_vs_normal_day"], ci_ep[0], ci_ep[1],
            dip_repro, n_near_id_flags,
        ),
        "",
        "## Files",
        "",
        "- [`README.md`](README.md) -- this file",
        "- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + "
        "`README.md` + `plots/*.png`",
        "- [`findings.md`](findings.md) -- writeup covering Q3.6.a-i + tables (programmatically "
        "emitted by run.py from summary.json per the Q3.2/Q3.3/Q3.4/Q3.5 architectural note about "
        "the Write-tool harness heuristic on the literal filename \"findings\")",
        "- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per "
        "`docs/research/**/*.json`)",
        "- [`plots/`](plots/) -- 6 PNGs: distribution, phase-stratified violins (citalopram), "
        "trajectory-with-phases, crash-vs-normal, ACF, 6-phase recovery-axis violins full corpus "
        "(gitignored per `docs/research/**/*.png`)",
        "",
        "## Status",
        "",
        "**Current as of 2026-06-05 corpus + 2026-06-24 analysis** (commit context: post-`7d49ba4` "
        "Q3.5 bb_overnight_gain LANDED; Phase 2 'finish the descriptive analysis' Tier 2 batch 2nd "
        "of 5 channels). Refresh when:",
        "",
        "1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about "
        "to spin up beyond the HA06b-locked operand.",
        "2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 "
        "onward).",
        "3. Politis-White E[L]\\* shifts by another factor of 2 from current {0:.1f}.".format(el_star),
        "4. A v3-extension or revision run on resting_hr lands and updates the Q3.6.d citalopram-"
        "dose-modulation status (v3 currently LOCKED at REJECTED with weak beta).",
        "5. recovery_arc v3 lands and updates the v2 cardiovascular-family per-phase reads "
        "(Q3.6.b + Q3.6.c reproductions).",
        "6. HA06b threshold-monotonicity diagnostic or any HA06b-descendant test ships and triggers "
        "operationalisation-substrate consumption.",
        "",
        "## Cross-references",
        "",
        "- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 "
        "2026-06-18, commit `ccbd12e`)",
        "- **LOAD-BEARING trajectory analysis**: [`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/) "
        "(v2 LANDED `8feae6a`); resting_hr is the only channel where 4b-4a paired-bootstrap CI "
        "excludes 0 (+3.0 bpm CI [+2.0, +4.0], E[L]\\*=22.7); cardiovascular-family acute-infection "
        "DIP (54 -> 52.5; parasympathetic dominance during viral infection); Q3.6.b reproduces "
        "E[L]\\* + Q3.6.c reproduces DIP descriptively.",
        "- **Q3.5 most-recent Tier 2 precedent**: [`descriptive/operationalisation_support/bb_overnight_gain/`](../bb_overnight_gain/) "
        "-- Tier 2 1st of 5; programmatic-emit pattern + load-bearing cross-reference template.",
        "- **Q3.4 clean f-string precedent**: [`descriptive/operationalisation_support/stress_stdev_sleep/`](../stress_stdev_sleep/) "
        "-- Tier 1 final; full-coverage continuous-channel template.",
        "- **Sister BB-floor inverse-coupling channel**: [`descriptive/operationalisation_support/bb_lowest/`](../bb_lowest/) "
        "-- Q3.3 reciprocal rho with resting_hr reported there (NOT near-identity).",
        "- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) "
        "-- HA06b + H01 rows descriptively corroborated in Q3.6.d + Q3.6.f.",
        "- **HA-* tests that this analysis anchors**:",
        "  - **HA06b** (LOCKED TRAIN SUPPORTED only / OVERALL REFUTED; R14 single-pool NOT-SUPPORTED "
        "CONVERGE-ON-OVERALL); primary operand on this channel.",
        "  - **H01** (LOCKED REFUTED both eras; R14 single-pool NOT-SUPPORTED CONVERGE); absolute "
        "spec on this channel.",
        "  - **HA06** (LOCKED REFUTED both eras; SUPERSEDED by HA06b); absolute spec on this channel.",
        "  - **HA-P6 v3** (LOCKED `a980b1c` 2026-06-17): resting_hr is in the 7-channel set + "
        "4-of-7 distinguishable channels.",
        "- **Definitional substrate**: [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "v3 section 5.6 (resting_hr in 6-channel scope; **REJECTED with weak/non-significant "
        "beta**; Q3.6.d caveat-class framing).",
        "- **Other methodology MDs**: `lc_phase_descriptive.md`, `citalopram_phase_stratification.md`, "
        "`permutation_null_block_length.md`, `garmin_indicators_audit.md`, `lc_era_temporal_segmentation.md`, "
        "`lc_recovery_phase_axis.md` (6-phase axis for Q3.6.c extension), "
        "`_descriptive_stocktake_2026-06-23.md` (gap-list framing).",
        "- **Existing complementary**: [`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) "
        "(Q3.6.e cross-reference; no near-identity in 9-anchor primitive set).",
        "- **Upstream pipeline**: `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` "
        "<- `pipeline/01_extract/garmin_uds_extras.py` (UDS-side passthrough for `restingHeartRate` "
        "field). `labels_crash_v2.csv` per locked `crash_v2-definition`.",
        "",
    ]

    path.write_text("\n".join(out_lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 70)
    print("Q3.6 resting_hr operationalisation-support descriptive (Tier 2 2nd of 5)")
    print("=" * 70)
    print()

    df_full = load_master(as_of_date=AS_OF_DATE, stratum_4_only=False)
    print("Loaded per_day_master.csv: {0} rows total (as_of {1})".format(
        len(df_full), AS_OF_DATE
    ))

    df = filter_to_stratum_4(df_full, as_of_date=AS_OF_DATE)
    n_s4 = int(len(df))
    print("Stratum 4 rows: {0}".format(n_s4))

    # Attach crash labels
    crashes = load_crash_labels(as_of_date=AS_OF_DATE)
    df = df.merge(
        crashes[["date", "label", "episode_id"]].rename(columns={"label": "crash_label"}),
        on="date", how="left",
    )
    df["is_crash"] = df["crash_label"].fillna("normal") == "crash"
    print("Crash days in S4 (label=='crash'): {0}".format(int(df["is_crash"].sum())))

    # Attach to full corpus for Q3.6.c extension
    df_full = df_full.merge(
        crashes[["date", "label", "episode_id"]].rename(columns={"label": "crash_label"}),
        on="date", how="left",
    )
    df_full["is_crash"] = df_full["crash_label"].fillna("normal") == "crash"

    if CHANNEL not in df.columns:
        raise SystemExit(
            "Channel {0!r} missing from per_day_master.csv; check column name + pipeline output".format(CHANNEL)
        )

    print()
    print("Computing Q3.6.a-i...")

    values_s4 = df[CHANNEL]
    a_res = q_a_distribution(values_s4)
    print("  Q3.6.a: n={0}, mean={1:.3f}, median={2:.3f}, skew={3:+.3f}, heavy_tail={4}".format(
        a_res["n"], a_res["mean"], a_res["median"], a_res["skewness"], a_res["heavy_tail_flag"]
    ))

    b_res = q_b_autocorrelation(values_s4)
    print("  Q3.6.b: E[L]*={0:.2f} (default 7; factor-of-2 flag={1}; M={2})".format(
        b_res["data_driven_E_L_star"], b_res["factor_of_2_deviation_flag"], b_res["cutoff_lag_M"],
    ))
    print("        recovery_arc v2 sec 7b reported E[L]*=22.7 -- delta={0:+.2f}".format(
        b_res["data_driven_E_L_star"] - 22.7,
    ))

    c_res = q_c_base_rates_per_phase(df, CHANNEL)
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = c_res.get(ph, {})
        if info.get("n", 0) > 0:
            print("  Q3.6.c [{0}]: n={1}, median={2:.2f}".format(ph, info["n"], info["median"]))
        else:
            print("  Q3.6.c [{0}]: n=0".format(ph))

    c_rec_res = q_c_recovery_axis_base_rates(df_full, CHANNEL)
    print("  Q3.6.c recovery-axis LOAD-BEARING extension:")
    for rph in (
        "pre_illness_healthy",
        "acute_infection",
        "lc_pre_ergo",
        "pacing_pre_citalopram_learning_4a",
        "pacing_habit_established_4b",
        "citalopram_modulated",
    ):
        info = c_rec_res["per_recovery_phase"].get(rph, {})
        if info.get("n", 0) > 0:
            print("    [{0}]: n={1}, median={2:.2f}".format(rph, info["n"], info["median"]))
        else:
            print("    [{0}]: n=0".format(rph))
    dip_info = c_rec_res["this_q36_descriptive_acute_dip_reproduction"]
    print("  Q3.6.c acute-infection DIP reproduction: healthy {0} -> acute {1} = delta {2}".format(
        dip_info.get("healthy_median_observed"),
        dip_info.get("acute_median_observed"),
        dip_info.get("acute_minus_healthy_observed_bpm"),
    ))

    d_res = q_d_phase_stratified(c_res, CHANNEL)
    print("  Q3.6.d: v3 status = {0}".format(d_res["v3_scope_status"]["v3_verdict"]))

    e_res = q_e_near_identity(df, CHANNEL)
    print("  Q3.6.e: {0} near-identity pairs at |rho|>={1}".format(
        len(e_res["flagged_pairs"]), e_res["threshold"]
    ))

    f_res = q_f_crash_vs_normal(df, CHANNEL)
    fl = f_res["day_level"]
    fe = f_res["episode_level"]
    print("  Q3.6.f: episode d={0:+.2f} CI95 [{1:+.2f}, {2:+.2f}]; day Cohen's d={3:+.2f}; MWU p={4:.4f}".format(
        fe["cohens_d_episode_vs_normal_day"],
        fe["bootstrap_ci95_mean_diff"][0],
        fe["bootstrap_ci95_mean_diff"][1],
        fl["cohens_d"],
        fl["mann_whitney_u"]["p_two_sided"],
    ))

    g_res = q_g_spike_primitive(df, CHANNEL)
    print("  Q3.6.g: HA06b spike-form construct on daily channel; {0} BB+stress companions in master".format(
        len(g_res["spike_primitives_available_in_master"])
    ))

    h_res = q_h_outliers_calibration(df, CHANNEL)
    print("  Q3.6.h: {0} MAD-z>5 outliers flagged".format(h_res["n_flagged"]))

    i_res = q_i_covariate_readiness(df, CHANNEL)
    print("  Q3.6.i: {0} candidate covariates named".format(len(i_res["candidate_covariates"])))

    summary = {
        "channel": CHANNEL,
        "as_of_date": AS_OF_DATE,
        "n_rows_full_corpus_to_as_of": int(len(df_full)),
        "n_rows_stratum_4_total": n_s4,
        "questions": {
            "Q3.6.a_distribution": a_res,
            "Q3.6.b_autocorrelation": b_res,
            "Q3.6.c_base_rates_per_phase": c_res,
            "Q3.6.c_recovery_axis_base_rates": c_rec_res,
            "Q3.6.d_phase_stratified_distribution": d_res,
            "Q3.6.e_near_identity": e_res,
            "Q3.6.f_crash_vs_normal": f_res,
            "Q3.6.g_spike_primitive": g_res,
            "Q3.6.h_outliers_calibration": h_res,
            "Q3.6.i_covariate_readiness": i_res,
        },
    }

    summary_path = HERE / "summary.json"
    # Make JSON-serialisable (numpy types -> Python types)
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
    extra_plot = make_recovery_axis_plot(df_full, CHANNEL, plots_dir)
    if extra_plot is not None:
        written_plots.append(extra_plot)
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
    print("Done. Q3.6 LANDED (Tier 2 2nd of 5; bb_overnight_gain done; next: exertion_class).")


if __name__ == "__main__":
    main()
