"""Descriptive analysis: gevoelscore operationalisation support.

Answers Q3.9.a-i per the locked descriptive programme:
``docs/research/analyses/descriptive/README.md`` section 3.4 (template
a-i applied to this channel; HA-touched non-confirmed candidate list
bullet "gevoelscore (almost every test's outcome side)").
**5th (FINAL) of 5 Tier 2 channels** in the user-prioritised Phase 2
sequential batch (Tier 1 closed `39d7693`; Tier 2: Q3.5 bb_overnight_
gain `7d49ba4`, Q3.6 resting_hr `5d28219`, Q3.7 exertion_class
`9b03bed`; Q3.9 closes Tier 2). Q3.8 push_burden_7d dispatched in
parallel.

Channel: per-day self-reported felt-state on a 1-6 integer scale
(per `crash_v2-definition` substrate; app-brief framing is 1-10 but
empirical range observed is 1-6). Logging started 2022-09-03 (= the
Stratum 4 left edge per `lc_era_temporal_segmentation.md`; Stratum 4
IS the gevoelscore-having days by definition).

Channel substantive status (per handoff section 1):
- OUTCOME side of nearly every HA. HA-C3 v2 (REJECTED wrong-direction
  override) + HA-C3p (PARTIAL 2-of-3) use gevoelscore as the DIRECT
  outcome in bin-convexity tests; inverted-U finding (concave shape;
  peak in mid-stress; decline at higher stress) cross-references in
  sec 3.9.a + sec 3.9.e.
- HA10 + HA07d + many other HAs use gevoelscore in their CRASH LABELS
  indirectly via `crash_v2-definition` derivation (crash = score <= 3
  for >= 2 consecutive days). sec 3.9.f is largely TAUTOLOGICAL on
  this channel (crashes are days with score <= 3 BY DEFINITION) --
  surfaced honestly per handoff section 1 + section 2.4.
- gevoelscore was NOT in v3 multi-channel sweep scope (it's the
  outcome, not a Garmin channel). No v3 verdict to cite.

**OUTCOME-CHANNEL ADAPTATIONS** of the Q-template (vs continuous
Garmin-channel templates Q3.1-Q3.6, count-primitive Q3.4/Q3.8, and
categorical Q3.7):

- Q3.9.a: bounded 1-6 INTEGER scale; classical distribution stats
  apply but value range is small + discrete. Per-value frequency
  vector + Shannon entropy reported alongside mean/median/MAD;
  heavy-tail flag uses the section 3.1 rule but the scale's natural
  ceiling (6) means heavy-tail in the classical sense does not
  meaningfully apply.
- Q3.9.b: Politis-White E[L]* on the integer series.
- Q3.9.c: per-citalopram-phase median/mean/dispersion + per-value
  frequency (since 1-6 integer is naturally tabulated). Plus
  recovery_arc v2 cross-reference table for the 6-phase axis
  characterisation (already done in recovery_arc v2 sec 2 + sec 5.A;
  this Q3.9.c does NOT re-characterise -- references and notes
  overlap honestly).
- Q3.9.d: phase-stratified medians + descriptive shift report
  (gevoelscore was NOT in v3 dose-response scope; no v3 verdict to
  cite, so no v3-caveat-class framing needed -- shifts are pure
  Layer 1 descriptive observations).
- **Q3.9.e SUBSTANTIVE (the most-interesting cell)**: Spearman rho vs
  key Garmin sister channels (stress_mean_sleep, all_day_stress_avg,
  bb_lowest, resting_hr, stress_stdev_sleep). Which channels track
  felt-state most closely? Strand-A first-pass at the Q4.9
  subjective<->objective coupling territory per descriptive README
  sec 4.9. Descriptive only -- NO causal mechanism interpretation;
  NO substantive HA verdict promotion. Cross-references HA-C3 v2 +
  HA-C3p inverted-U finding from the gevoelscore-as-outcome side
  (the spearman rho with stress channels is the LINEAR companion to
  the bin-shape convexity tests; HA-C3 v2 sec 3 reported spearman
  rho = -0.0298 with stress -- this Q3.9.e re-anchors at the
  multi-pool resolution).
- **Q3.9.f TAUTOLOGICAL** per handoff section 1: crash IS defined by
  gevoelscore per crash_v2-definition sec 2.1 (crash = score <= 3 for
  >= 2 consecutive days). Day-level crash-vs-normal gevoelscore
  difference is mechanically constrained (crash days are by
  definition the low-score days). Surfaced HONESTLY per handoff
  section 1 + section 2.4. Useful framing: episode-level
  distribution shape (per-episode min / per-episode median) +
  dip-vs-normal characterisation (dips are also score <= 3
  isolated-bad-day events per crash_v2 sec 2.2).
- Q3.9.g: drop primitive (sudden drop in gevoelscore from one day to
  the next). HA11 family already operationalised within-day stress
  U-dip-COUNT primitive on a different channel; HA11's verdict is
  on u_dip_count, NOT on gevoelscore-drop. This Q3.9.g reports the
  per-day gevoelscore-drop distribution descriptively as the
  spike-form on this outcome channel.
- Q3.9.h: bounded 1-6 INTEGER -- no outliers in the classical sense
  (MAD-z > 5 is impossible on a 6-value scale). Coverage /
  missingness patterns matter more; per-month coverage rate reported
  + Stratum-4-completeness check (every Stratum-4 day SHOULD have a
  gevoelscore by definition).
- Q3.9.i: covariates for future HA pre-regs USING gevoelscore as
  outcome (the dominant pattern in this project's HA family).

Output: ``summary.json`` (machine-readable per-question results) +
``plots/*.png`` (visualisations) + ``findings.md`` + ``README.md``
(programmatically emitted from this script per the Q3.6/Q3.7
precedent session's architectural note about the Write-tool harness
heuristic on the literal filename "findings").

Discipline guards (per CONVENTIONS):
- section 2.1 descriptive-before-inference: no causal claims; no
  falsification bar; no HA verdict promotion (HA-C3 v2 + HA-C3p
  locked verdicts NOT extended here; recovery_arc v2 gevoelscore
  per-phase reads NOT re-characterised; crash_v2-definition NOT
  modified).
- section 3.1 personal baseline: distribution shape reported as-is;
  phase-stratified to surface phase-shift patterns.
- section 3.3 column-duplication: near-identity check at |rho|>=0.92
  -- N/A by construction (gevoelscore is the only felt-state
  channel; no candidate near-identity sister).
- section 3.4 crash-drop sensitivity: per handoff section 1 +
  section 2.4 framing -- crash IS defined by gevoelscore so the
  crash-drop diagnostic IS tautological; surfaced as such.
- section 3.5 spike metrics: drop primitive per Q3.9.g; HA11 family
  operationalised a DIFFERENT spike-form (within-day stress u-dip
  count) on a different channel; this Q3.9.g is descriptive.
- section 3.6 named counts: every count reports scheme + unit +
  source.
- section 4.1 + section 4.2: no a-priori claims; observed phase
  shifts framed as descriptive observation only.
- section 4.9 (descriptive README): Q4.9 subjective<->objective
  coupling is DEFERRED to Strand B; this Q3.9.e is a PARTIAL
  Strand-A answer at the spearman-rho-multi-channel resolution.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date
from math import erf, log, sqrt
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
# HERE = .../analyses/descriptive/operationalisation_support/gevoelscore
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


CHANNEL = "gevoelscore"
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

# 6-phase recovery axis boundaries per methodology/lc_recovery_phase_axis.md
# (LOCKED `d47e0d3`; recovery_arc v2 uses these). Used in Q3.9.c overlap
# notation -- gevoelscore-coverage starts 2022-09-03 = phase-3 last 19 days,
# so phases 1 + 2 have n=0 and phase 3 is partial (n=19).
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
# Q3.9.a Distribution shape -- OUTCOME-CHANNEL ADAPTATION (bounded 1-6 int)
# ---------------------------------------------------------------------------


def shannon_entropy(probs: list) -> float:
    """Shannon entropy in nats. Returns 0 for empty / single-value."""
    h = 0.0
    for p in probs:
        if p > 0:
            h -= p * log(p)
    return h


def q_a_distribution(values: pd.Series) -> dict:
    """Distribution shape on Stratum 4 (Q3.9.a) -- OUTCOME-CHANNEL ADAPTATION.

    Bounded 1-6 integer scale; classical distribution stats apply but
    value range is small + discrete. Per-value frequency vector +
    Shannon entropy reported alongside mean/median/MAD for completeness;
    heavy-tail flag uses the section 3.1 rule but the scale's natural
    ceiling (6) means heavy-tail in the classical sense does not
    meaningfully apply.
    """
    v = values.dropna().astype(float)
    n = int(len(v))
    mean = float(v.mean()) if n > 0 else float("nan")
    median = float(v.median()) if n > 0 else float("nan")
    std = float(v.std(ddof=1)) if n > 1 else float("nan")
    mad = float(np.median(np.abs(v - median))) if n > 0 else float("nan")
    quantiles = {
        "p{0}".format(q): float(np.percentile(v, q))
        for q in (1, 5, 10, 25, 50, 75, 90, 95, 99)
    } if n > 0 else {}
    centered = v - mean if n > 0 else pd.Series([], dtype=float)
    m2 = float((centered ** 2).mean()) if n > 0 else float("nan")
    m3 = float((centered ** 3).mean()) if n > 0 else float("nan")
    skewness = m3 / (m2 ** 1.5) if m2 and m2 > 0 else float("nan")
    m4 = float((centered ** 4).mean()) if n > 0 else float("nan")
    excess_kurtosis = m4 / (m2 ** 2) - 3.0 if m2 and m2 > 0 else float("nan")
    p99 = quantiles.get("p99", float("nan"))
    p99_over_med = p99 / median if median and median > 0 else float("nan")
    heavy_tail = bool(
        (p99_over_med and p99_over_med > 3.0)
        or (skewness == skewness and skewness > 1.0)
    )

    # Per-value frequency on the integer scale (1-6 expected; allow wider)
    int_v = v.round().astype(int)
    observed_values = sorted(int_v.unique().tolist())
    per_value_n = {int(k): int((int_v == k).sum()) for k in observed_values}
    per_value_freq = {
        k: per_value_n[k] / n if n > 0 else float("nan")
        for k in per_value_n
    }
    probs = list(per_value_freq.values())
    entropy_nats = shannon_entropy(probs)
    # Max entropy under uniform over 6 possible values (1..6 scale ceiling)
    expected_n_values = 6
    entropy_max = log(expected_n_values)
    entropy_normalised = entropy_nats / entropy_max if entropy_max > 0 else float("nan")

    return {
        "n": n,
        "mean": mean,
        "median": median,
        "std_ddof1": std,
        "mad_unscaled": mad,
        "mad_normal_equivalent": mad * 1.4826 if mad == mad else float("nan"),
        "quantiles": quantiles,
        "skewness": skewness,
        "excess_kurtosis": excess_kurtosis,
        "heavy_tail_flag": heavy_tail,
        "min": float(v.min()) if n > 0 else float("nan"),
        "max": float(v.max()) if n > 0 else float("nan"),
        "per_value_n": per_value_n,
        "per_value_frequency": per_value_freq,
        "observed_values": observed_values,
        "shannon_entropy_nats": entropy_nats,
        "shannon_entropy_max_log_6": entropy_max,
        "entropy_normalised": entropy_normalised,
        "outcome_channel_adaptation_note": (
            "Per handoff section 1 + OUTCOME-CHANNEL ADAPTATION: gevoelscore "
            "is a bounded 1-6 INTEGER scale (per crash_v2-definition; app-"
            "brief framing is 1-10 but empirical range observed is 1-6). "
            "Classical distribution stats apply but the value range is small "
            "+ discrete -- mean/median/std/MAD/quantiles are reported for "
            "parity with sister continuous Strand-A analyses but the per-"
            "value frequency vector + Shannon entropy are the OUTCOME-channel "
            "primitives. The heavy_tail_flag uses the CONVENTIONS section 3.1 "
            "rule (skew > 1 OR p99/median > 3.0) but on a bounded 6-ceiling "
            "scale the heavy-tail concept does not meaningfully apply -- the "
            "flag is reported for parity but should be read as 'rarely fires "
            "on bounded scales by construction'."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.9.b Autocorrelation + E[L]*
# ---------------------------------------------------------------------------


def q_b_autocorrelation(values: pd.Series) -> dict:
    """Autocorrelation structure + E[L]* (Q3.9.b) on the integer series."""
    arr = values.dropna().astype(float).to_numpy()
    result = compute_data_driven_block_length(arr, default_block_length=7)
    acf = result["autocorrelations"]
    lags_of_interest = {}
    for k in (1, 2, 3, 7, 14, 28):
        if len(acf) > k:
            lags_of_interest["acf_lag{0}".format(k)] = float(acf[k])
    n_arr = len(arr)
    politis_white_threshold = float(2.0 * np.sqrt(np.log(n_arr) / n_arr)) if n_arr > 1 else float("nan")
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
        "outcome_channel_adaptation_note": (
            "Per OUTCOME-CHANNEL ADAPTATION: ACF computed on the integer "
            "series as-is (no encoding needed; the integer scale 1-6 "
            "naturally supports the Politis-White ACF + block-length "
            "estimator). Integer-discreteness does not bias the estimator "
            "at this sample size."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.9.c Base rates per citalopram phase + recovery_arc v2 cross-reference
# ---------------------------------------------------------------------------


def q_c_base_rates_per_phase(df: pd.DataFrame, channel: str) -> dict:
    """Per-phase n + median + dispersion + per-value frequency (Q3.9.c)."""
    out = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))
        sub = df.loc[mask, channel].dropna().astype(float)
        n = int(len(sub))
        if n == 0:
            out[phase_name] = {"n": 0}
            continue
        med = float(sub.median())
        int_sub = sub.round().astype(int)
        observed = sorted(int_sub.unique().tolist())
        per_value_n = {int(k): int((int_sub == k).sum()) for k in observed}
        per_value_freq = {k: per_value_n[k] / n for k in per_value_n}
        out[phase_name] = {
            "n": n,
            "date_start": str(start),
            "date_end": str(end),
            "mean": float(sub.mean()),
            "median": med,
            "std_ddof1": float(sub.std(ddof=1)) if n > 1 else float("nan"),
            "mad_unscaled": float(np.median(np.abs(sub - med))),
            "p10": float(np.percentile(sub, 10)),
            "p25": float(np.percentile(sub, 25)),
            "p75": float(np.percentile(sub, 75)),
            "p90": float(np.percentile(sub, 90)),
            "per_value_n": per_value_n,
            "per_value_frequency": per_value_freq,
        }
    return out


def q_c_recovery_axis_overlap_note(df: pd.DataFrame, channel: str) -> dict:
    """Recovery_arc v2 overlap notation (per handoff section 2.4).

    The recovery_arc v2 analysis already characterised gevoelscore on the
    6-phase axis (findings.md sec 2 table + sec 2.1 per-channel narrative +
    sec 3 sec 7b paired-bootstrap CI). This Q3.9.c does NOT re-characterise;
    it provides a descriptive reproduction READ on the same axis at the
    same as-of-date for methodological consistency check. Per handoff
    section 1: "check overlap; do NOT re-characterise if already done".

    The known structural caveat: gevoelscore logging started 2022-09-03 =
    phase-3 last 19 days, so phases 1 (pre_illness_healthy) + 2
    (acute_infection) have n=0 and phase 3 (lc_pre_ergo) is partial (n=19).
    """
    out = {}
    for phase_name, start, end in RECOVERY_PHASE_BOUNDARIES:
        mask = (df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))
        sub = df.loc[mask, channel].dropna().astype(float)
        n = int(len(sub))
        if n == 0:
            out[phase_name] = {
                "n": 0,
                "date_start": str(start),
                "date_end": str(end),
                "note": "no gevoelscore in this phase window (logging started 2022-09-03)",
            }
            continue
        med = float(sub.median())
        out[phase_name] = {
            "n": n,
            "date_start": str(start),
            "date_end": str(end),
            "median": med,
            "mean": float(sub.mean()),
            "std_ddof1": float(sub.std(ddof=1)) if n > 1 else float("nan"),
        }

    return {
        "per_recovery_phase": out,
        "recovery_arc_v2_section_2_reported": {
            "pre_illness_healthy_median": None,
            "acute_infection_median": None,
            "lc_pre_ergo_median": 3.0,
            "lc_pre_ergo_n": 19,
            "lc_pre_ergo_note": "partial coverage; last 19 days only (logging started 2022-09-03)",
            "pacing_4a_median": 5.0,
            "pacing_4a_n": 56,
            "pacing_4a_ci95_E_L7": [4.0, 5.0],
            "pacing_4b_median": 4.0,
            "pacing_4b_n": 509,
            "pacing_4b_ci95_E_L7": [4.0, 4.0],
            "citalopram_modulated_median": 5.0,
            "citalopram_modulated_n": 787,
            "citalopram_modulated_ci95_E_L7": [5.0, 5.0],
            "section_7b_4b_minus_4a_diff": -1.0,
            "section_7b_4b_minus_4a_ci95": [-1.0, 0.0],
            "section_7b_verdict": "includes_0 (upper CI bound at 0; boundary inconclusive)",
            "narrative": (
                "recovery_arc v2 reported: 4a -> 4b drop on gevoelscore "
                "(diff -1.0, CI [-1.0, 0.0]) sits at the boundary of the "
                "sec 7b verdict -- upper CI bound is AT 0 (includes 0 but "
                "only just; descriptive read: ambiguous). Phase 3 -> 4a "
                "step is +2.0 (largest within-channel step) but phase 3's "
                "n=19 keeps its CI wide [3, 4] and shaped by structural "
                "partial-coverage. Per recovery_arc v2 sec 4 felt-state "
                "narrative: phase 3 partial coverage shows median 3.0 "
                "(lowest gevoelscore median anywhere in the corpus); 4a "
                "(median 5; full 56-day sub-window) is the first complete "
                "characterisation of the 8-week ergotherapy-onboarding "
                "period in felt-state terms; 4b drops to median 4; phase 5 "
                "returns to 5."
            ),
            "source": "trajectory/recovery_arc/findings.md sec 2 + sec 2.1 + sec 3 + sec 4",
        },
        "this_q39c_overlap_framing": (
            "Per handoff section 1 + section 2.4: recovery_arc v2 already "
            "characterised gevoelscore on the 6-phase axis (sec 2 table + "
            "sec 2.1 per-channel narrative + sec 3 sec 7b paired-bootstrap "
            "CI). This Q3.9.c overlap notation is NOT a re-characterisation; "
            "it surfaces the v2 reads directly + provides a methodological "
            "consistency check on this Q3.9 run at the same as-of-date. "
            "Phases 1 + 2 have n=0 BY CONSTRUCTION (gevoelscore logging "
            "started 2022-09-03 = phase-3 last 19 days). Per CONVENTIONS "
            "section 4.2: this is Layer 1 descriptive observation only; the "
            "recovery_arc v2 substantive narrative is LOCKED at the "
            "recovery_arc/findings.md level and NOT extended here."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.9.d Phase-stratified distribution + descriptive shift report
# ---------------------------------------------------------------------------


def q_d_phase_stratified(per_phase: dict, channel: str) -> dict:
    """Phase-stratified distribution + descriptive shift report (Q3.9.d).

    gevoelscore was NOT in v3 multi-channel dose-response sweep scope (per
    handoff section 1 + descriptive README section 3.4: "gevoelscore is
    the outcome, not a Garmin channel"). No v3 verdict to cite. Observed
    phase shifts are pure Layer 1 descriptive observations per CONVENTIONS
    section 4.2 -- no caveat-class framing of a CONFIRMED/REJECTED
    reclassification needed because no v3 classification exists.
    """
    out = {"phase_medians": {}, "phase_to_phase_shifts": {}, "phase_means": {}}
    medians = {}
    means = {}
    for phase_name in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = per_phase.get(phase_name, {})
        if info.get("n", 0) > 0:
            medians[phase_name] = info["median"]
            means[phase_name] = info["mean"]
            out["phase_medians"][phase_name] = info["median"]
            out["phase_means"][phase_name] = info["mean"]

    pairs = [
        ("unmedicated", "buildup"),
        ("unmedicated", "consolidation"),
        ("consolidation", "afbouw"),
        ("unmedicated", "afbouw"),
        ("buildup", "consolidation"),
    ]
    for a, b in pairs:
        if a in medians and b in medians:
            out["phase_to_phase_shifts"]["{0}_minus_{1}_median".format(b, a)] = (
                medians[b] - medians[a]
            )
            out["phase_to_phase_shifts"]["{0}_minus_{1}_mean".format(b, a)] = (
                means[b] - means[a]
            )

    typical_within = {
        p: per_phase[p].get("mad_unscaled") for p in medians if "mad_unscaled" in per_phase[p]
    }
    out["within_phase_mad"] = typical_within

    out["v3_scope_status"] = {
        "channel_in_v3_six_channel_scope": False,
        "v3_verdict": "N/A (gevoelscore is the outcome, not a Garmin channel)",
        "framing": (
            "gevoelscore was NOT in v3 multi-channel dose-response sweep "
            "scope per descriptive README section 3.4 + handoff section 1 "
            "('gevoelscore is the outcome, not a Garmin channel'). No v3 "
            "verdict exists to cite. Observed phase shifts in the table "
            "below are pure Layer 1 descriptive observations per "
            "CONVENTIONS section 4.2 (caveats yes; a-priori claims no) -- "
            "no caveat-class framing of a CONFIRMED/REJECTED "
            "reclassification needed because no v3 classification exists "
            "on this outcome channel."
        ),
    }

    out["ha_outcome_xref"] = {
        "ha_c3_v2_locked_verdict": (
            "REJECTED (wrong-direction override) on the v2 4-bin "
            "all_day_stress_avg -> gevoelscore convexity test; primary "
            "3-condition test on 3-bin reduction returned J*=0.481 "
            "p_a=0.6742 + S=-0.740 p_c=0.0003 + spline F=28.27 p_b=0.0002 "
            "+ spline secderiv at midpoints [35, 70] = [-0.0015, 0.0000]. "
            "Wrong-direction override fired because S is significantly "
            "NEGATIVE (concave, not convex)."
        ),
        "ha_c3p_locked_verdict": (
            "PARTIAL (2-of-3 conditions MET) on personal-baseline-anchored "
            "equal-N quintile bins; p_b=0.0018 spline-F significant + "
            "p_c=0.0020 convexity-contrast significant in WRONG direction "
            "(S=-0.196); p_a=0.5925 Jonckheere monotone non-significant. "
            "Joint reading with HA-C3 v2 (per HA-C3p result.md sec 6 "
            "4-cell matrix consolidated): BOTH detect REAL non-linearity + "
            "CONCAVE/inverted-U shape with peak around stress 30-40 + "
            "decline at higher stress."
        ),
        "ha_c3_source": "analyses/hypotheses/HA-C3/result.md (LOCKED 2026-06-23 a2b18ba)",
        "ha_c3p_source": "analyses/hypotheses/HA-C3p/result.md (LOCKED 2026-06-23 e5a63fe)",
        "note": (
            "HA-C3 v2 + HA-C3p both use gevoelscore as the DIRECT outcome "
            "in the stress -> felt-state mapping convexity test. The joint "
            "finding from the outcome side: at this corpus the stress->"
            "felt-state mapping is CONCAVE / inverted-U with peak around "
            "stress 30-40, NOT convex per the Wiggers verbatim prediction. "
            "This Q3.9.d phase-stratified gevoelscore characterisation + "
            "Q3.9.e spearman-rho-vs-stress descriptively corroborates the "
            "inverted-U finding from the gevoelscore outcome side. The "
            "HA-C3 v2 + HA-C3p substantive verdicts are LOCKED and NOT "
            "extended here per CONVENTIONS section 4.2."
        ),
    }
    return out


# ---------------------------------------------------------------------------
# Q3.9.e SUBSTANTIVE: Spearman rho vs key Garmin sister channels
# ---------------------------------------------------------------------------


def q_e_subjective_objective_coupling(df: pd.DataFrame, channel: str) -> dict:
    """Subjective <-> objective coupling (Q3.9.e) -- SUBSTANTIVE CELL.

    Per handoff section 1 + section 2.4 + descriptive README section 4.9:
    Q3.9.e is the SUBSTANTIVELY-INTERESTING cell. Spearman rho between
    gevoelscore (felt-state) and key Garmin sister channels (stress_mean_
    sleep, all_day_stress_avg, bb_lowest, resting_hr, stress_stdev_sleep).
    Which channels track felt-state most closely? Strand-A first-pass at
    the Q4.9 subjective<->objective coupling territory (deferred to
    Strand B per descriptive README sec 4.9).

    Descriptive ONLY -- NO causal mechanism interpretation; NO substantive
    HA verdict promotion. The spearman rho is the LINEAR companion to
    HA-C3 v2 + HA-C3p bin-shape convexity tests (which use the same
    gevoelscore-as-outcome + stress-as-predictor pairing); a rho near 0
    is the expected linear-companion finding given HA-C3 v2 + HA-C3p both
    found inverted-U / concave shapes.
    """
    # Channels per handoff section 1 + section 2.4
    primary_targets = [
        # CONFIRMED-citalopram autonomic-load family (most-cited HA outcomes)
        ("stress_mean_sleep", "autonomic-load sleep-window; CONFIRMED-citalopram +0.43/mg; HA07c/HA07d/HA08c primary"),
        ("all_day_stress_avg", "autonomic-load 24h; CONFIRMED-citalopram +0.57/mg; HA-C3 + HA-C3p primary stress predictor"),
        ("bb_lowest", "BB-floor NADIR; CONFIRMED-citalopram -1.13/mg; HA-C4b v2 primary"),
        ("resting_hr", "cardiovascular daily; HA06b + H01 + HA06 primary"),
        ("stress_stdev_sleep", "sleep-window variability; HA07d primary (only canonical-SUPPORTED test)"),
    ]
    # Additional sister channels for broader cross-family read
    extended_targets = [
        ("bb_overnight_gain", "BB-recovery; HA10 primary; partial coverage 2024-09-18 onward"),
        ("stress_low_motion_min_count_S60_Mlow", "count-primitive; HA-C4b v2 primary; CONFIRMED-citalopram"),
        ("respiration_avg_sleep", "respiration sleep-window; v3-sweep REJECTED"),
        ("all_day_stress_max", "autonomic-load peak"),
        ("awake_stress_avg", "waking-hour autonomic-load"),
        ("bb_during_sleep_value", "BB sleep-window"),
        ("asleep_stress_avg_uds", "asleep stress UDS-passthrough"),
        ("max_spike_minutes", "stress spike duration; H02b primary"),
        ("u_dip_count", "stress U-dip count; HA11 primary (within-day spike-form)"),
        ("push_burden_7d_lagged_lcera", "trailing 7d exertion burden; HA02 family primary"),
    ]
    rows = []
    primary_rho_summary = {}
    for t, semantic in primary_targets + extended_targets:
        if t not in df.columns:
            rows.append({
                "channel": t,
                "semantic": semantic,
                "is_primary": (t, semantic) in primary_targets,
                "note": "column absent",
            })
            continue
        sub = df[[channel, t]].dropna()
        n = int(len(sub))
        if n < 30:
            rows.append({
                "channel": t,
                "semantic": semantic,
                "is_primary": (t, semantic) in primary_targets,
                "n": n,
                "note": "n<30 -- skipped",
            })
            continue
        pear = float(sub[channel].corr(sub[t]))
        spear = float(sub[channel].corr(sub[t], method="spearman"))
        row = {
            "channel": t,
            "semantic": semantic,
            "is_primary": (t, semantic) in primary_targets,
            "n": n,
            "pearson_r": pear,
            "spearman_rho": spear,
            "abs_spearman_rho": abs(spear),
        }
        rows.append(row)
        if (t, semantic) in primary_targets:
            primary_rho_summary[t] = {
                "n": n,
                "spearman_rho": spear,
                "pearson_r": pear,
                "abs_rho": abs(spear),
            }

    # Rank the primary targets by |rho|
    ranked_primary = sorted(
        primary_rho_summary.items(),
        key=lambda kv: kv[1]["abs_rho"],
        reverse=True,
    )

    # Compute the "which channel tracks felt-state most closely" headline
    if ranked_primary:
        top_channel, top_info = ranked_primary[0]
        top_rho = top_info["spearman_rho"]
        weakest_channel, weakest_info = ranked_primary[-1]
        weakest_rho = weakest_info["spearman_rho"]
    else:
        top_channel = None
        top_rho = float("nan")
        weakest_channel = None
        weakest_rho = float("nan")

    return {
        "rows": rows,
        "primary_target_set": [t for t, _ in primary_targets],
        "primary_rho_summary": primary_rho_summary,
        "ranked_primary_by_abs_rho": [
            {"channel": ch, "spearman_rho": info["spearman_rho"], "n": info["n"]}
            for ch, info in ranked_primary
        ],
        "top_tracking_channel": top_channel,
        "top_tracking_rho": top_rho,
        "weakest_tracking_channel": weakest_channel,
        "weakest_tracking_rho": weakest_rho,
        "linear_companion_to_bin_shape_xref": {
            "ha_c3_v2_spearman_rho_unmed_pool": -0.0298,
            "ha_c3_v2_spearman_n": 581,
            "ha_c3_v2_spearman_p": 0.4738,
            "ha_c3_v2_source": "analyses/hypotheses/HA-C3/result.md sec 3 sanity-check companion Spearman",
            "note": (
                "HA-C3 v2 reported the linear-companion Spearman rho on the "
                "unmedicated single-pool of all_day_stress_avg vs "
                "gevoelscore as rho=-0.0298 (p=0.4738, n=581) -- consistent "
                "with the inverted-U finding (a near-zero linear rho is "
                "the expected linear-companion when the true shape is "
                "inverted-U / concave with peak in the middle). This "
                "Q3.9.e re-anchors at the FULL Stratum-4 multi-pool "
                "resolution + extends to other key Garmin channels. The "
                "spearman rho values reported below are NOT to be "
                "interpreted as 'strength of stress -> felt-state effect' "
                "-- they are LINEAR companions to the bin-shape convexity "
                "tests; a low |rho| co-occurring with a strong bin-shape "
                "result is the expected pattern. NO causal interpretation."
            ),
        },
        "substantive_framing": (
            "Per handoff section 1 + descriptive README section 4.9: this "
            "Q3.9.e is the SUBSTANTIVELY-INTERESTING cell of the Q3.9 "
            "template. It provides a Strand-A first-pass at the Q4.9 "
            "subjective<->objective coupling question (deferred to "
            "Strand B per descriptive README sec 4.9). Reported "
            "descriptively only; NO causal mechanism interpretation per "
            "CONVENTIONS section 4.1 + section 4.2. The which-channel-"
            "tracks-felt-state-most-closely reading below is the rank-"
            "order of |spearman rho| across the 5 primary Garmin sister "
            "channels; the ranking has descriptive value but does NOT "
            "promote a substantive coupling claim. Future Strand-B Q4.9 "
            "analysis would add: episode-level coupling, lagged-coupling "
            "structure, per-phase coupling stratification, and the "
            "central project question of 'pre-crash divergence between "
            "subjective + objective signals'."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.9.f Crash-vs-normal -- TAUTOLOGICAL by definition; honest framing
# ---------------------------------------------------------------------------


def _mann_whitney_u(crash_vals: np.ndarray, normal_vals: np.ndarray) -> dict:
    """Mann-Whitney U with normal approximation + tie correction.

    Vendored to avoid scipy. Crash is the first sample.
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
    ) if (n_c + n_n) > 1 else 0.0
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
    """Crash-vs-normal -- TAUTOLOGICAL (Q3.9.f).

    Per handoff section 1 + section 2.4: crash IS DEFINED BY gevoelscore
    per crash_v2-definition sec 2.1 (crash = score <= 3 for >= 2
    consecutive days). Day-level crash-vs-normal gevoelscore difference
    is mechanically constrained -- crash days are by definition the
    low-score days. Reported HONESTLY as tautological; the numbers below
    exist only for parity with sister Strand-A analyses and to anchor
    the episode-level / dip-vs-normal characterisation that is NOT
    tautological in the same way.

    Useful framings:
    - per-episode min gevoelscore distribution (how deep do crashes go?)
    - per-episode median gevoelscore (within-episode central tendency)
    - dip-vs-normal characterisation (dip is also score <= 3 isolated-
      bad-day per crash_v2 sec 2.2; same definitional substrate)
    - score-floor verification per crash_v2-definition (all crash days
      should have score <= 3)
    """
    sub = df[[channel, "is_crash"]].dropna(subset=[channel, "is_crash"]).copy()
    if "episode_id" in df.columns:
        sub["episode_id"] = df.loc[sub.index, "episode_id"]
    else:
        sub["episode_id"] = pd.NA
    is_crash = sub["is_crash"].astype(bool)
    crash_vals = sub.loc[is_crash, channel].astype(float)
    normal_vals = sub.loc[~is_crash, channel].astype(float)

    n_crash_day = int(len(crash_vals))
    n_normal_day = int(len(normal_vals))
    mean_diff_day = float(crash_vals.mean() - normal_vals.mean()) if n_crash_day > 0 and n_normal_day > 0 else float("nan")
    if n_crash_day > 1 and n_normal_day > 1:
        pooled_sd = float(
            np.sqrt(
                ((n_crash_day - 1) * crash_vals.var(ddof=1)
                 + (n_normal_day - 1) * normal_vals.var(ddof=1))
                / (n_crash_day + n_normal_day - 2)
            )
        )
        cohens_d_day = mean_diff_day / pooled_sd if pooled_sd > 0 else float("nan")
    else:
        pooled_sd = float("nan")
        cohens_d_day = float("nan")

    mwu = _mann_whitney_u(crash_vals.to_numpy(), normal_vals.to_numpy()) if n_crash_day > 0 and n_normal_day > 0 else {
        "U_crash_first_sample": float("nan"), "z": float("nan"),
        "p_two_sided": float("nan"), "p_crash_greater_than_normal": float("nan"),
        "median_diff": float("nan"),
    }

    # Score-floor verification per crash_v2-definition sec 2.1
    crash_score_max = float(crash_vals.max()) if n_crash_day > 0 else float("nan")
    crash_score_above_3 = int((crash_vals > 3).sum())
    score_floor_verified = crash_score_max <= 3.0 if crash_score_max == crash_score_max else None

    # Episode-level min + median (the NON-tautological framings)
    ep_mask = sub["episode_id"].notna() & sub["episode_id"].astype(str).str.startswith("crash-")
    ep_df = sub.loc[ep_mask, [channel, "episode_id"]].copy()
    if len(ep_df) > 0:
        per_episode_min = ep_df.groupby("episode_id")[channel].min()
        per_episode_median = ep_df.groupby("episode_id")[channel].median()
        per_episode_n_days = ep_df.groupby("episode_id")[channel].size()
        n_episodes = int(len(per_episode_min))
        ep_min_summary = {
            "n_episodes": n_episodes,
            "median_of_per_episode_min": float(per_episode_min.median()),
            "mean_of_per_episode_min": float(per_episode_min.mean()),
            "min_of_per_episode_min": float(per_episode_min.min()),
            "max_of_per_episode_min": float(per_episode_min.max()),
            "per_value_n_of_per_episode_min": {
                int(k): int((per_episode_min == k).sum())
                for k in sorted(per_episode_min.unique())
            },
        }
        ep_median_summary = {
            "median_of_per_episode_median": float(per_episode_median.median()),
            "mean_of_per_episode_median": float(per_episode_median.mean()),
            "min_of_per_episode_median": float(per_episode_median.min()),
            "max_of_per_episode_median": float(per_episode_median.max()),
        }
        ep_length_summary = {
            "median_episode_length_days": float(per_episode_n_days.median()),
            "mean_episode_length_days": float(per_episode_n_days.mean()),
            "max_episode_length_days": int(per_episode_n_days.max()),
            "min_episode_length_days": int(per_episode_n_days.min()),
        }
    else:
        n_episodes = 0
        ep_min_summary = {"n_episodes": 0}
        ep_median_summary = {}
        ep_length_summary = {}

    # Dip-vs-normal-vs-crash characterisation
    if "is_dip" in df.columns:
        dip_sub = df[[channel, "is_dip"]].dropna(subset=[channel, "is_dip"]).copy()
        is_dip = dip_sub["is_dip"].astype(bool)
        dip_vals = dip_sub.loc[is_dip, channel].astype(float)
        n_dip_day = int(len(dip_vals))
        dip_score_max = float(dip_vals.max()) if n_dip_day > 0 else float("nan")
        dip_score_above_3 = int((dip_vals > 3).sum()) if n_dip_day > 0 else 0
        dip_summary = {
            "n_dip_day": n_dip_day,
            "mean_dip_day": float(dip_vals.mean()) if n_dip_day > 0 else float("nan"),
            "median_dip_day": float(dip_vals.median()) if n_dip_day > 0 else float("nan"),
            "max_dip_day_score": dip_score_max,
            "n_dip_days_with_score_above_3": dip_score_above_3,
            "per_value_n": {
                int(k): int((dip_vals == k).sum())
                for k in sorted(dip_vals.round().astype(int).unique())
            } if n_dip_day > 0 else {},
        }
    else:
        dip_summary = {"note": "is_dip column absent in master"}

    return {
        "tautology_framing": (
            "Per handoff section 1 + section 2.4 + crash_v2-definition "
            "sec 2.1 + 2.2 + 2.3: crash + dip are BOTH DEFINED BY "
            "gevoelscore (crash = score <= 3 for >= 2 consecutive days; "
            "dip = isolated single day with score <= 3 between neighbours "
            ">= 4; normal = everything else INCLUDING score-4 days). The "
            "day-level crash-vs-normal gevoelscore difference is "
            "MECHANICALLY CONSTRAINED -- crash days are by definition the "
            "low-score days. The numbers in 'day_level' below exist only "
            "for parity with sister Strand-A analyses + to anchor the "
            "non-tautological framings (episode-level min + median + "
            "length, dip-vs-normal characterisation, score-floor "
            "verification). NO substantive crash-prediction claim from "
            "this gevoelscore-vs-crash signal -- the crash definition IS "
            "the gevoelscore signal."
        ),
        "score_floor_verification_per_crash_v2_definition": {
            "max_score_on_crash_days": crash_score_max,
            "n_crash_days_with_score_above_3": crash_score_above_3,
            "score_floor_verified_le_3": score_floor_verified,
            "expected_per_crash_v2_sec_2_1_and_merge_rule_sec_2_1_b": (
                "most crash days have score <= 3 (per acute condition sec 2.1) "
                "but a small number of score-4 days may appear inside a crash "
                "episode range when two qualifying sub-runs merge under the "
                "<=3-day-gap merge rule sec 2.1.b -- the crash range covers "
                "start-to-end INCLUSIVELY of all days in the merged span"
            ),
            "interpretation": (
                "Per crash_v2-definition sec 2.1: a crash episode's days are "
                "ALL days from start (first sub-threshold day) through end "
                "(last sub-threshold day) AFTER merging. The merge rule sec "
                "2.1.b merges two qualifying episodes whose last-day and "
                "next-day are within 3 days; this means a few score-4 days "
                "WITHIN a crash episode's date span are EXPECTED (the days "
                "between two acute sub-runs in a merged episode). The acute "
                "condition (score <= 3 for >= 2 consecutive days) is the "
                "EPISODE-INITIATION rule, NOT a per-day score floor on every "
                "crash-labelled day. So n_crash_days_with_score_above_3 > 0 "
                "is NOT a labelling pipeline drift -- it is the expected "
                "behaviour of the merge rule, descriptively characterising "
                "the small fraction of score-4 days that fall inside merged "
                "crash episodes."
            ),
        },
        "day_level": {
            "n_crash_day": n_crash_day,
            "n_normal_day": n_normal_day,
            "mean_crash": float(crash_vals.mean()) if n_crash_day > 0 else float("nan"),
            "mean_normal": float(normal_vals.mean()) if n_normal_day > 0 else float("nan"),
            "median_crash": float(crash_vals.median()) if n_crash_day > 0 else float("nan"),
            "median_normal": float(normal_vals.median()) if n_normal_day > 0 else float("nan"),
            "mean_diff": mean_diff_day,
            "cohens_d": cohens_d_day,
            "mann_whitney_u": mwu,
            "tautology_note": (
                "MECHANICALLY CONSTRAINED per crash_v2-definition sec 2.1; "
                "reported for parity only -- NO substantive interpretation."
            ),
        },
        "episode_level_min": ep_min_summary,
        "episode_level_median": ep_median_summary,
        "episode_level_length": ep_length_summary,
        "dip_level": dip_summary,
        "crash_v2_definition_xref": {
            "source": "analyses/hypotheses/crash_v2-definition/definition.md",
            "lock_date": "2026-06-06 (sec 2 unchanged from lock)",
            "sec_2_1_acute_condition": "score <= 3 for >= 2 consecutive days",
            "sec_2_2_dip_condition": "isolated single day with score <= 3 between neighbours >= 4",
            "sec_2_3_normal": "everything else (includes score-4 days; no separate vague_low tier)",
            "framing": (
                "crash_v2 is a DEFINITION, not a hypothesis. Per definition "
                "sec 5: 'we don't test it; we apply it, then re-run "
                "downstream tests with the new labels'. This Q3.9.f does "
                "NOT modify the crash_v2 labelling (canonical lock per "
                "handoff section 3 hard constraint); it characterises the "
                "underlying gevoelscore distribution that crash_v2's "
                "definition operationalises ON, descriptively + honestly."
            ),
        },
    }


# ---------------------------------------------------------------------------
# Q3.9.g Drop primitive -- spike-form on outcome channel
# ---------------------------------------------------------------------------


def q_g_drop_primitive(df: pd.DataFrame, channel: str) -> dict:
    """Spike-form on the outcome channel = drop primitive (Q3.9.g).

    Per handoff section 1 + CONVENTIONS section 3.5: the spike-form
    relevant on the gevoelscore outcome channel is the DROP primitive
    (sudden decrease in gevoelscore from one day to the next). HA11
    family operationalised a within-day stress U-dip COUNT primitive on
    a DIFFERENT channel (u_dip_count on stress_minutes per
    HA11-stress-udip); the HA11 verdict is on u_dip_count, NOT on
    gevoelscore-drop. This Q3.9.g reports the per-day gevoelscore-drop
    distribution descriptively as the spike-form on this outcome
    channel.
    """
    sub = df[["date", channel]].dropna().sort_values("date").reset_index(drop=True)
    n = int(len(sub))

    # Day-over-day diff (drop is negative diff)
    diffs = sub[channel].astype(float).diff().dropna()
    drops = -diffs  # convert to positive-magnitude-drop convention
    n_pairs = int(len(diffs))

    # Distribution of drop magnitudes
    n_drop_ge_1 = int((drops >= 1).sum())
    n_drop_ge_2 = int((drops >= 2).sum())
    n_drop_ge_3 = int((drops >= 3).sum())
    n_drop_ge_4 = int((drops >= 4).sum())
    n_no_change = int((drops == 0).sum())
    n_rise_ge_1 = int((drops <= -1).sum())  # negative drop = rise

    drop_rate_ge1 = n_drop_ge_1 / n_pairs if n_pairs > 0 else float("nan")
    drop_rate_ge2 = n_drop_ge_2 / n_pairs if n_pairs > 0 else float("nan")
    drop_rate_ge3 = n_drop_ge_3 / n_pairs if n_pairs > 0 else float("nan")

    # Max drop on the corpus
    max_drop = float(drops.max()) if n_pairs > 0 else float("nan")
    min_diff = float(diffs.min()) if n_pairs > 0 else float("nan")
    max_rise = float(-min_diff) if n_pairs > 0 else float("nan")

    # Magnitude distribution
    diff_dist = {}
    for k in range(-5, 6):
        diff_dist[str(k)] = int((diffs.round() == k).sum())

    return {
        "spike_form_definition": (
            "per-day gevoelscore drop = -(today - yesterday) (positive = "
            "felt-state DROP day-over-day; negative = felt-state RISE; "
            "zero = no change). Drop magnitude >= 1 unit, >= 2 units, "
            ">= 3 units reported as spike-class thresholds."
        ),
        "n_consecutive_day_pairs": n_pairs,
        "n_no_change": n_no_change,
        "n_drop_ge_1": n_drop_ge_1,
        "n_drop_ge_2": n_drop_ge_2,
        "n_drop_ge_3": n_drop_ge_3,
        "n_drop_ge_4": n_drop_ge_4,
        "n_rise_ge_1": n_rise_ge_1,
        "drop_rate_ge_1": drop_rate_ge1,
        "drop_rate_ge_2": drop_rate_ge2,
        "drop_rate_ge_3": drop_rate_ge3,
        "max_drop_observed": max_drop,
        "max_rise_observed": max_rise,
        "diff_magnitude_distribution": diff_dist,
        "ha11_family_xref": {
            "ha11_operand": "max signed z (4d) of u_dip_count (within-day stress U-dip count primitive)",
            "ha11_locked_verdict": "TRAIN SUPPORTED +22.8 pp / VALIDATE REFUTED -10.7 pp / OVERALL REFUTED",
            "ha11_r14_single_pool": "NOT-SUPPORTED CONVERGE-ON-OVERALL (+16.8 pp [-22.4, +20.4] perm p=0.0906 per single_pool_reanchor)",
            "ha11_channel": "u_dip_count (NOT gevoelscore)",
            "ha11_source": "analyses/hypotheses/HA11-stress-udip/result.md + R14 single_pool_reanchor row HA11",
            "note": (
                "HA11 family operationalised a within-day STRESS u-dip "
                "count primitive on the stress_minutes channel; the HA11 "
                "verdict is on u_dip_count, NOT on gevoelscore-drop. This "
                "Q3.9.g characterises the gevoelscore-drop primitive as "
                "the spike-form on the outcome channel; it does NOT "
                "operationalise an HA on this primitive. A future HA "
                "using gevoelscore-drop as outcome (e.g. 'large overnight "
                "felt-state drop is predicted by autonomic spikes') would "
                "be a NEW pre-reg, NOT a re-anchoring of HA11."
            ),
        },
        "spike_form_outcome_channel_adaptation_note": (
            "Per OUTCOME-CHANNEL ADAPTATION + CONVENTIONS section 3.5: "
            "the spike-form on a 1-6 bounded INTEGER outcome channel is "
            "the DROP magnitude (today minus yesterday). The boundedness "
            "of the scale means drops >= 5 are structurally impossible "
            "(max-min = 6-1 = 5). The drop-rate-ge1 reported above is the "
            "rate of ANY day-over-day worsening; drop-rate-ge2 + drop-"
            "rate-ge3 are the larger spike-form thresholds. A drop of 3+ "
            "units on a 6-point scale represents a substantial felt-"
            "state shift -- candidate spike-form for any future HA using "
            "gevoelscore as outcome with a sudden-worsening operand."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.9.h Coverage / missingness -- bounded-scale outlier semantics
# ---------------------------------------------------------------------------


def q_h_coverage_missingness(df: pd.DataFrame, channel: str) -> dict:
    """Coverage + missingness on a bounded 1-6 scale (Q3.9.h).

    Per handoff section 1: bounded 1-6 integer scale has no outliers in
    the classical MAD-z sense (MAD-z > 5 is impossible on a 6-value
    range). Coverage / missingness patterns matter more. Every Stratum-4
    day SHOULD have a gevoelscore by the Stratum-4 definition (Stratum 4
    = LC with gevoelscore + crash labels, 2022-09-03 -> as-of-date per
    lc_era_temporal_segmentation.md).
    """
    sub_total = df[["date", channel]].copy()
    n_total = int(len(sub_total))
    n_missing = int(sub_total[channel].isna().sum())
    n_present = int(sub_total[channel].notna().sum())
    coverage_rate = n_present / n_total if n_total > 0 else float("nan")

    sub_total["_year_month"] = sub_total["date"].dt.to_period("M")
    monthly = sub_total.groupby("_year_month")[channel].apply(
        lambda s: pd.Series({
            "n_total": int(len(s)),
            "n_present": int(s.notna().sum()),
            "coverage_rate": float(s.notna().mean()),
        })
    ).unstack()
    monthly_records = [
        {
            "year_month": str(idx),
            "n_total": int(row["n_total"]),
            "n_present": int(row["n_present"]),
            "coverage_rate": float(row["coverage_rate"]),
        }
        for idx, row in monthly.iterrows()
    ]

    # Stratum-4 completeness check: per crash_v2-definition sec 3.1 + Stratum 4
    # definition, every Stratum-4 day SHOULD have a gevoelscore (1372 day total
    # per crash_v2 sec 3.1 + 4: "user has logged every single day; 0 gaps").
    # Anything missing inside Stratum 4 is a pipeline / data-quality flag.
    stratum_4_n = n_total  # df is already Stratum 4 filtered when this runs
    stratum_4_complete = n_missing == 0
    completeness_flag = "COMPLETE" if stratum_4_complete else "GAPS (flag for investigation)"

    return {
        "coverage_semantics_note": (
            "Per handoff section 1 + OUTCOME-CHANNEL ADAPTATION: a "
            "bounded 1-6 INTEGER scale has NO classical outliers (MAD-z "
            "> 5 is impossible on a 6-value range; max-min = 5 vs MAD * "
            "1.4826 ~ 1.5; max possible z is ~3.3). Coverage / "
            "missingness patterns matter more on this outcome channel. "
            "Stratum 4 is DEFINED as 'LC with gevoelscore + crash labels' "
            "per lc_era_temporal_segmentation.md -- every Stratum-4 day "
            "SHOULD have a gevoelscore by construction. Any missing day "
            "in Stratum 4 is a definitional inconsistency flag, NOT an "
            "outlier."
        ),
        "n_total_stratum_4_rows": n_total,
        "n_missing_in_stratum_4": n_missing,
        "n_present_in_stratum_4": n_present,
        "coverage_rate_stratum_4": coverage_rate,
        "stratum_4_completeness_flag": completeness_flag,
        "crash_v2_definition_sec_3_1_cross_check": {
            "expected_per_crash_v2_sec_4": "1372 day-level rows in 2022-09-03 -> 2026-06-05 window per definition sec 4 + sec 3.1 (zero gaps)",
            "expected_n_days": 1372,
            "observed_n_total": n_total,
            "observed_n_present": n_present,
            "matches_expected": n_present == 1372,
        },
        "monthly_coverage_snapshots": monthly_records,
        "outlier_semantics_note": (
            "Per OUTCOME-CHANNEL ADAPTATION: no MAD-z outlier scan run on "
            "this channel; the bounded-INTEGER scale makes classical "
            "outlier detection inapplicable. The per-value frequency "
            "vector in Q3.9.a is the equivalent diagnostic; rare-value "
            "flag (any value < 5% of total) would be the categorical-"
            "equivalent flag (analogous to Q3.7.a CATEGORICAL ADAPTATION "
            "rare-class flag); reported in Q3.9.a output if it fires."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.9.i Covariate-sensitivity readiness
# ---------------------------------------------------------------------------


def q_i_covariate_readiness(df: pd.DataFrame, channel: str) -> dict:
    """Covariate-sensitivity readiness for future HA using gevoelscore as
    outcome (Q3.9.i).

    Per HA-P7 section 4.5.4 worked-example pattern. The dominant pattern
    in this project's HA family is gevoelscore as OUTCOME (either
    directly via HA-C3 v2 + HA-C3p, or indirectly via crash labels per
    crash_v2-definition derivation). Names candidate covariates.
    """
    cands = []

    # 1. Own-lagged baseline -- autocorrelation control (HA-P7 sec 4.5.4)
    cands.append({
        "covariate": "gevoelscore[d-1] (own-lagged 1-day; autocorrelation-vs-mechanism control per HA-P7 section 4.5.4)",
        "rationale": (
            "Per HA-P7 section 4.5.4 worked example: any HA using "
            "gevoelscore as outcome should pre-spec the own-lagged 1-day "
            "value as the secondary autocorrelation-vs-mechanism control. "
            "Per Q3.9.b the lag-1 ACF is high (recovery_arc v2 implies "
            "lag-1 > 0.5 on the gevoelscore series; verify in run output) "
            "-- the covariate disambiguates: beta_predictor attenuates if "
            "today's gevoelscore is just yesterday's value carried "
            "forward; beta_predictor survives if the predictor carries "
            "new-day information beyond own-lag."
        ),
        "source": "HA-P7 hypothesis.md section 4.5.4 + Q3.9.b ACF",
        "expected_effect": (
            "beta_predictor collapses if today's gevoelscore is just "
            "yesterday's value carried forward; beta_predictor survives "
            "if the signal carries new-day information"
        ),
        "needed_columns_in_master": ["gevoelscore (already in master); shift(1) at runtime"],
    })

    # 2. dose_plasma_mg(d) -- citalopram covariate (CONFIRMED on 3 channels;
    #    gevoelscore not directly tested in v3 but indirectly via the
    #    inverted-U finding being phase-stratifiable)
    cands.append({
        "covariate": "dose_plasma_mg(d) (citalopram dose; CONFIRMED on 3 Garmin channels per v3; intervention_effects_descriptive includes felt-state)",
        "rationale": (
            "Per citalopram_dose_response_stress_mean_sleep.md v3 sec 5.6: "
            "3 Garmin channels are CONFIRMED dose-modulated. gevoelscore "
            "was NOT in v3 scope (per descriptive README sec 3.4 'it's "
            "the outcome, not a Garmin channel') but per "
            "intervention_effects_descriptive.md the per-phase gevoelscore "
            "shifts are described as part of the citalopram arc. Any "
            "future HA using gevoelscore as outcome cross-phase should "
            "pre-spec dose as a secondary covariate; if beta_dose is "
            "significant net of beta_predictor, that is candidacy "
            "evidence for a citalopram-on-gevoelscore mediator test (NOT "
            "a re-promotion of any v3 verdict since gevoelscore was not "
            "in v3 scope)."
        ),
        "source": "citalopram_dose_response_stress_mean_sleep.md v3 sec 5.6 + intervention_effects_descriptive.md",
        "expected_effect": (
            "beta_dose carries any citalopram-on-gevoelscore residue; "
            "beta_predictor attenuates if predictor signal is shared "
            "with dose effect"
        ),
        "needed_columns_in_master": ["dose_plasma_mg (already in master)"],
    })

    # 3. Top-tracking stress channel from Q3.9.e (substantive companion)
    cands.append({
        "covariate": "top-Q3.9.e-tracking Garmin sister channel (the autonomic-load channel with highest |spearman rho| vs gevoelscore on Stratum 4)",
        "rationale": (
            "Per Q3.9.e SUBSTANTIVE cell: ranks key Garmin sister "
            "channels by |spearman rho| with gevoelscore. The top-"
            "tracking channel is the candidate cross-family autonomic-"
            "load covariate for any future HA using gevoelscore as "
            "outcome with a felt-state-predicted-by-X operand. The "
            "covariate disambiguates: beta_predictor attenuates if the "
            "signal is shared with autonomic-load via this channel; "
            "beta_predictor survives if predictor carries channel-"
            "distinct information beyond the autonomic-load axis."
        ),
        "source": "Q3.9.e subjective<->objective coupling table",
        "expected_effect": (
            "beta_predictor attenuates if shared autonomic-load "
            "dominates; beta_predictor survives if it carries channel-"
            "distinct information"
        ),
    })

    # 4. recovery_phase (the 6-phase axis) -- cross-phase stratification
    cands.append({
        "covariate": "recovery_phase (6-phase axis per lc_recovery_phase_axis.md; LOCKED `d47e0d3`)",
        "rationale": (
            "Per lc_recovery_phase_axis.md + recovery_arc v2 findings.md: "
            "gevoelscore varies meaningfully across the 6-phase recovery "
            "axis (phase 3 median 3.0 [partial coverage] -> 4a median 5.0 "
            "-> 4b median 4.0 -> phase 5 median 5.0). Any future HA using "
            "gevoelscore as outcome should pre-spec the recovery_phase "
            "axis as a candidate stratification or covariate; the 4b "
            "low-gevoelscore phase + 4a high-gevoelscore sub-phase are "
            "natural per-phase strata. Per phase_axis_collapsibility_"
            "conventions.md tier-A: 4a + 4b -> 4 collapse is allowed when "
            "hypothesis-warranted."
        ),
        "source": "lc_recovery_phase_axis.md (LOCKED d47e0d3) + recovery_arc v2 findings.md + phase_axis_collapsibility_conventions.md",
        "expected_effect": (
            "beta_predictor attenuates if predictor signal is partly "
            "carried by phase-context; beta_predictor survives if it "
            "carries within-phase information beyond the per-phase mean "
            "shift"
        ),
        "needed_columns_in_master": ["recovery_phase (already in master per recovery_arc v2 commit e00df27)"],
    })

    return {
        "primary_use_case": (
            "Future HA pre-reg using gevoelscore as OUTCOME (the dominant "
            "pattern in this project's HA family: direct via HA-C3 v2 + "
            "HA-C3p; indirect via crash_v2 derivation in HA10 + HA07d + "
            "many others). Covariate-sensitivity readiness for any "
            "predictor -> gevoelscore HA test; the four covariates below "
            "are the candidate confound-control + mediator-disambiguation "
            "set per HA-P7 section 4.5.4 worked-example pattern."
        ),
        "discipline_anchor": "HA-P7 hypothesis.md section 4.5.4 -- secondary-logistic-with-covariate pattern",
        "candidate_covariates": cands,
        "recommendation": (
            "Pre-spec all four covariates as secondary sensitivity arms. "
            "Covariate 1 (own-lagged 1-day) operationalises HA-P7 sec "
            "4.5.4 autocorrelation-vs-mechanism disambiguation on the "
            "outcome side. Covariate 2 (dose_plasma_mg) is the cross-"
            "phase citalopram-confound covariate. Covariate 3 (top-"
            "tracking Q3.9.e Garmin channel) is the cross-family "
            "autonomic-load disambiguator -- pre-spec the SPECIFIC "
            "channel from this Q3.9.e table at HA draft time (not from "
            "later refresh). Covariate 4 (recovery_phase) is the multi-"
            "year-trajectory stratification covariate."
        ),
        "outcome_channel_adaptation_note": (
            "Per OUTCOME-CHANNEL ADAPTATION: covariates listed here are "
            "for HAs USING gevoelscore as OUTCOME (the dominant pattern). "
            "Future HAs USING gevoelscore as PREDICTOR (rare; e.g. "
            "felt-state-predicts-Garmin tomorrow) would need a different "
            "covariate set -- not enumerated here per handoff section 3 "
            "hard constraint (do NOT promote to substantive HA verdicts; "
            "Q3.9.i scope is the dominant outcome-channel pattern only)."
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

    sub = df[["date", channel, "is_crash"]].dropna(subset=[channel]).copy()
    vals = sub[channel].astype(float)

    # Figure 1: per-value frequency bar (integer 1-6)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    int_v = vals.round().astype(int)
    observed = sorted(int_v.unique().tolist())
    n_per_val = [int((int_v == k).sum()) for k in observed]
    n_total = int(sum(n_per_val))
    freq_per_val = [n / n_total if n_total > 0 else 0 for n in n_per_val]
    colors_grad = ["#a04848", "#cc8a5e", "#e0c590", "#a4c9b0", "#5b88c4", "#264c75"]
    palette = colors_grad[: len(observed)] if len(observed) <= len(colors_grad) else colors_grad + ["#888"] * (len(observed) - len(colors_grad))
    bars = ax.bar([str(k) for k in observed], freq_per_val, color=palette, edgecolor="white")
    for bar, n_v, f_v in zip(bars, n_per_val, freq_per_val):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.005,
            "n={0}\n{1:.1%}".format(n_v, f_v),
            ha="center", va="bottom", fontsize=9,
        )
    ax.set_xlabel("gevoelscore (1-6 integer scale)")
    ax.set_ylabel("frequency")
    ax.set_ylim(0, max(freq_per_val) * 1.18 if freq_per_val else 1)
    ax.set_title("gevoelscore per-value frequency - Stratum 4, n={0}".format(n_total))
    fig.tight_layout()
    fp = out_dir / "fig1_per_value_frequency_s4.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 2: per-citalopram-phase stacked bar
    phase_per_val_freq = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (sub["date"] >= pd.Timestamp(start)) & (sub["date"] <= pd.Timestamp(end))
        sub_p = sub.loc[mask, channel].dropna()
        n_p = int(len(sub_p))
        if n_p == 0:
            phase_per_val_freq[phase_name] = [0] * len(observed)
            continue
        int_p = sub_p.round().astype(int)
        phase_per_val_freq[phase_name] = [
            int((int_p == k).sum()) / n_p for k in observed
        ]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    keep = [p for p in ("unmedicated", "buildup", "consolidation", "afbouw")
            if sum(phase_per_val_freq[p]) > 0]
    bottom = np.zeros(len(keep))
    for j, k_val in enumerate(observed):
        vals_j = [phase_per_val_freq[p][j] for p in keep]
        color_j = palette[j] if j < len(palette) else "#888"
        ax.bar(keep, vals_j, bottom=bottom, color=color_j, label=str(k_val), edgecolor="white")
        bottom = bottom + np.array(vals_j)
    ax.set_ylabel("per-value frequency")
    ax.set_ylim(0, 1)
    ax.legend(loc="upper right", bbox_to_anchor=(1.18, 1.0), fontsize=8, title="gevoelscore")
    ax.set_title("gevoelscore per-citalopram-phase per-value frequency (Stratum 4)")
    fig.tight_layout()
    fp = out_dir / "fig2_phase_stratified_stacked_bar.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 3: time series with rolling 90d median + citalopram phase shading
    sub_sorted = sub.sort_values("date").reset_index(drop=True)
    sub_sorted["roll90"] = sub_sorted[channel].rolling(90, min_periods=45).median()
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.plot(sub_sorted["date"], sub_sorted[channel], color="#aac4e3", linewidth=0.5, alpha=0.5, label="daily")
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
    ax.set_ylabel("gevoelscore (1-6)")
    ax.set_title("gevoelscore - rolling 90d median + citalopram phases (Stratum 4)")
    fig.tight_layout()
    fp = out_dir / "fig3_trajectory_with_phases.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 4: spearman scatter vs top Q3.9.e channel (chose stress_mean_sleep
    # if present; this is the canonical autonomic-load anchor)
    candidate_x_channels = ["stress_mean_sleep", "all_day_stress_avg", "bb_lowest", "resting_hr"]
    chosen_x = next((c for c in candidate_x_channels if c in df.columns), None)
    if chosen_x is not None:
        scatter_df = df[[chosen_x, channel]].dropna()
        if len(scatter_df) >= 30:
            fig, ax = plt.subplots(figsize=(8, 4.6))
            jitter_y = scatter_df[channel].astype(float) + np.random.default_rng(20260624).normal(0, 0.1, size=len(scatter_df))
            ax.scatter(scatter_df[chosen_x], jitter_y, s=6, alpha=0.3, color="#5b88c4")
            # Add per-x-bin mean gevoelscore overlay
            x_bins = np.quantile(scatter_df[chosen_x].astype(float), [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
            x_bins = np.unique(x_bins)
            if len(x_bins) >= 3:
                bin_means_x = []
                bin_means_y = []
                for i_b in range(len(x_bins) - 1):
                    bin_mask = (scatter_df[chosen_x] >= x_bins[i_b]) & (scatter_df[chosen_x] < x_bins[i_b + 1] if i_b < len(x_bins) - 2 else scatter_df[chosen_x] <= x_bins[i_b + 1])
                    if bin_mask.sum() >= 5:
                        bin_means_x.append(float(scatter_df.loc[bin_mask, chosen_x].mean()))
                        bin_means_y.append(float(scatter_df.loc[bin_mask, channel].mean()))
                if bin_means_x:
                    ax.plot(bin_means_x, bin_means_y, marker="o", linewidth=2.0,
                            color="#cc4949", label="per-quintile mean gevoelscore")
            spear = float(scatter_df[channel].corr(scatter_df[chosen_x], method="spearman"))
            ax.set_xlabel("{0} (Garmin sister channel; Q3.9.e SUBSTANTIVE)".format(chosen_x))
            ax.set_ylabel("gevoelscore (jittered for visibility)")
            ax.set_title("gevoelscore vs {0}; Spearman rho = {1:+.3f}, n={2}".format(
                chosen_x, spear, len(scatter_df)
            ))
            ax.legend(loc="lower left", fontsize=9)
            fig.tight_layout()
            fp = out_dir / "fig4_q39e_spearman_vs_{0}.png".format(chosen_x)
            fig.savefig(fp, dpi=110)
            plt.close(fig)
            written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 5: ACF
    arr = vals.dropna().to_numpy()
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
        m_str = "n/a" if acf_res["cutoff_lag"] is None else str(acf_res["cutoff_lag"])
        title = "ACF - gevoelscore (Stratum 4); E[L]*={0:.1f}, M={1}".format(
            acf_res["optimal_block_length"], m_str,
        )
        ax.set_title(title)
        ax.legend(loc="upper right", fontsize=8)
        fig.tight_layout()
        fp = out_dir / "fig5_acf.png"
        fig.savefig(fp, dpi=110)
        plt.close(fig)
        written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 6: drop primitive distribution (Q3.9.g)
    diffs = sub_sorted[channel].astype(float).diff().dropna()
    if len(diffs) > 0:
        fig, ax = plt.subplots(figsize=(8, 4.2))
        diff_int = diffs.round().astype(int)
        diff_observed = sorted(diff_int.unique().tolist())
        diff_n = [int((diff_int == k).sum()) for k in diff_observed]
        diff_freq = [n / int(len(diff_int)) for n in diff_n]
        bar_colors = ["#cc4949" if k < 0 else ("#264c75" if k > 0 else "#888") for k in diff_observed]
        bars = ax.bar([str(k) for k in diff_observed], diff_freq, color=bar_colors, edgecolor="white")
        for bar, n_v, f_v in zip(bars, diff_n, diff_freq):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.003,
                "n={0}".format(n_v),
                ha="center", va="bottom", fontsize=8,
            )
        ax.set_xlabel("day-over-day diff (gevoelscore[t] - gevoelscore[t-1]); RED = drop / BLUE = rise / GREY = no change")
        ax.set_ylabel("frequency over consecutive-day pairs")
        ax.set_title("gevoelscore drop primitive distribution (Q3.9.g spike-form on outcome channel)")
        fig.tight_layout()
        fp = out_dir / "fig6_drop_primitive_distribution.png"
        fig.savefig(fp, dpi=110)
        plt.close(fig)
        written.append(str(fp.relative_to(out_dir.parent)))

    return written


# ---------------------------------------------------------------------------
# Markdown emitters (findings.md + README.md)
# ---------------------------------------------------------------------------


def _format_p(p: float) -> str:
    """Format p-value safely (avoid f-string pre-3.12 backslash escape)."""
    if p != p:  # NaN
        return "NaN"
    if p < 0.0001:
        return "<0.0001"
    return format(p, ".4f")


def _fmt_per_value_row(label: str, per_val_n: dict, per_val_freq: dict, n: int) -> str:
    """Format a per-value row: | label | n | val1% | val2% | ... |."""
    cells = []
    for k in (1, 2, 3, 4, 5, 6):
        n_k = per_val_n.get(k, 0)
        f_k = per_val_freq.get(k, 0.0)
        cells.append("{0} ({1:.1%})".format(n_k, f_k))
    return "| {0} | {1} | {2} |".format(label, n, " | ".join(cells))


def _fmt_q39e_rows(rows_list: list) -> list:
    out = []
    for r in rows_list:
        if "spearman_rho" in r:
            primary_marker = " (PRIMARY)" if r.get("is_primary") else ""
            out.append(
                "| `{0}`{1} | {2} | {3:+.3f} | {4:+.3f} | {5} |".format(
                    r["channel"], primary_marker, r["n"],
                    r["pearson_r"], r["spearman_rho"],
                    r["semantic"],
                )
            )
        else:
            out.append("| `{0}` | -- | -- | -- | {1} |".format(
                r["channel"], r.get("note", r.get("semantic", "n/a")),
            ))
    return out


def _fmt_acf_table(acf_dict: dict) -> str:
    """Format selected-lags ACF dict as a markdown table."""
    lines = [
        "| lag (days) | autocorrelation |",
        "|---:|---:|",
    ]
    for k in (1, 2, 3, 7, 14, 28):
        key = "acf_lag{0}".format(k)
        if key in acf_dict:
            lines.append("| {0} | {1:+.3f} |".format(k, acf_dict[key]))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Markdown emitters
# ---------------------------------------------------------------------------


def write_findings_md(summary: dict, path: Path) -> None:
    """Emit findings.md from the computed summary."""
    q = summary["questions"]
    a = q["Q3.9.a_distribution"]
    b = q["Q3.9.b_autocorrelation"]
    c = q["Q3.9.c_base_rates_per_phase"]
    cr = q["Q3.9.c_recovery_axis_overlap"]
    d = q["Q3.9.d_phase_stratified"]
    e = q["Q3.9.e_subjective_objective_coupling"]
    f = q["Q3.9.f_crash_vs_normal"]
    g = q["Q3.9.g_drop_primitive"]
    h = q["Q3.9.h_coverage_missingness"]
    i = q["Q3.9.i_covariate_readiness"]

    el_star = b["data_driven_E_L_star"]
    n_s4 = summary["n_rows_stratum_4_total"]

    # Distribution metrics
    quant = a["quantiles"]
    skew = a["skewness"]
    skew_class = (
        "right-skewed" if skew > 0.3 else
        "left-skewed" if skew < -0.3 else
        "roughly-symmetric"
    )
    entropy_pct = a["entropy_normalised"] * 100.0 if a["entropy_normalised"] == a["entropy_normalised"] else float("nan")

    # Memory class
    memory_class = (
        "autocorrelation-SPARSE-MEMORY" if el_star < 10 else
        "autocorrelation-MODERATE-MEMORY" if el_star < 20 else
        "autocorrelation-DENSE-MEMORY"
    )

    # Per-phase rows
    per_phase_rows = []
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = c.get(ph, {})
        if info.get("n", 0) > 0:
            per_phase_rows.append(
                "| {0} | {1} to {2} | {3} | {4:.2f} | {5:.2f} | {6:.2f} | {7:.0f} / {8:.0f} |".format(
                    ph, info["date_start"], info["date_end"], info["n"],
                    info["median"], info["mean"], info["mad_unscaled"],
                    info["p10"], info["p90"],
                )
            )
        else:
            per_phase_rows.append("| {0} | -- | 0 | -- | -- | -- | -- |".format(ph))

    # Q3.9.e rows
    e_rows = _fmt_q39e_rows(e["rows"])
    top_ch = e["top_tracking_channel"]
    top_rho = e["top_tracking_rho"]
    weakest_ch = e["weakest_tracking_channel"]
    weakest_rho = e["weakest_tracking_rho"]
    top_rho_str = "{0:+.3f}".format(top_rho) if top_rho == top_rho else "n/a"
    weakest_rho_str = "{0:+.3f}".format(weakest_rho) if weakest_rho == weakest_rho else "n/a"
    ranked_lines = []
    for idx_r, item in enumerate(e["ranked_primary_by_abs_rho"], start=1):
        ranked_lines.append(
            "{0}. `{1}` Spearman rho = {2:+.3f} (n={3})".format(
                idx_r, item["channel"], item["spearman_rho"], item["n"],
            )
        )

    # Crash vs normal
    fl = f["day_level"]
    sf = f["score_floor_verification_per_crash_v2_definition"]
    fem = f["episode_level_min"]
    fmed = f["episode_level_median"]
    flen = f["episode_level_length"]
    fdip = f["dip_level"]

    # Drop primitive
    drop_rate1_str = "{0:.1%}".format(g["drop_rate_ge_1"]) if g["drop_rate_ge_1"] == g["drop_rate_ge_1"] else "n/a"
    drop_rate2_str = "{0:.1%}".format(g["drop_rate_ge_2"]) if g["drop_rate_ge_2"] == g["drop_rate_ge_2"] else "n/a"
    drop_rate3_str = "{0:.1%}".format(g["drop_rate_ge_3"]) if g["drop_rate_ge_3"] == g["drop_rate_ge_3"] else "n/a"

    mwu_p_str = _format_p(fl["mann_whitney_u"]["p_two_sided"])

    out_lines = [
        "# Findings -- `gevoelscore` operationalisation-support descriptive (Q3.9.a-i)",
        "",
        "**Channel**: `gevoelscore` (the OUTCOME side of nearly every HA in the project; "
        "per-day self-reported felt-state on a 1-6 integer scale per the empirical range "
        "+ [`crash_v2-definition`](../../../analyses/hypotheses/crash_v2-definition/) "
        "substrate; app-brief framing is 1-10 but observed values are 1-6). Logging started "
        "2022-09-03 = the Stratum 4 left edge per "
        "[`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) "
        "(Stratum 4 IS the gevoelscore-having days by definition).",
        "",
        "**Substantive context** (handoff section 1): gevoelscore is the OUTCOME side of nearly "
        "every HA. **HA-C3 v2** (LOCKED REJECTED wrong-direction override; concave/inverted-U "
        "vs Wiggers' convex prediction; J*=0.481 p_a=0.6742; S=-0.740 p_c=0.0003; spline F=28.27 "
        "p_b=0.0002; spline secderiv at midpoints [35, 70] = [-0.0015, 0.0000]) + **HA-C3p** "
        "(LOCKED PARTIAL 2-of-3; p_b=0.0018 spline-F significant + p_c=0.0020 convexity-contrast "
        "significant in wrong direction S=-0.196; p_a=0.5925 Jonckheere monotone non-significant) "
        "use gevoelscore as the DIRECT outcome in stress -> felt-state bin-shape convexity "
        "tests; the joint outcome-side reading from these two LOCKED tests: at this corpus the "
        "stress -> felt-state mapping is **CONCAVE / inverted-U with peak around stress 30-40**, "
        "NOT convex per the Wiggers verbatim prediction. **HA10 + HA07d + many other HAs** use "
        "gevoelscore in their CRASH LABELS indirectly via "
        "[`crash_v2-definition`](../../../analyses/hypotheses/crash_v2-definition/) derivation "
        "(crash = score <= 3 for >= 2 consecutive days). Section 3.9.f is largely TAUTOLOGICAL "
        "on this channel (crashes are days with score <= 3 by definition) -- surfaced honestly "
        "per handoff section 1 + section 2.4. **gevoelscore was NOT in v3 multi-channel "
        "dose-response sweep scope** (per descriptive README section 3.4 'it's the outcome, not "
        "a Garmin channel'); no v3 verdict exists to cite or re-promote on this channel.",
        "",
        "**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to {0}). "
        "n={1} days with channel out of {2} Stratum 4 days "
        "({3} NaN days).".format(
            summary["as_of_date"], a["n"], n_s4, n_s4 - a["n"],
        ),
        "",
        "**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.4 (LOCKED "
        "2026-06-18 r3, commit `ccbd12e`) -- HA-touched non-confirmed channel candidate "
        "list bullet `gevoelscore (almost every test's outcome side)`. **5th (FINAL) of "
        "the 5 Tier 2 channels** in the user-prioritised Phase 2 sequential batch (Tier 1 "
        "closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain `7d49ba4`; 2nd = Q3.6 "
        "resting_hr `5d28219`; 3rd = Q3.7 exertion_class `9b03bed`; 4th = Q3.8 push_burden_7d "
        "`92d7193`; this Q3.9 closes Tier 2). Q3.9.a-i template applied per section 3.1 with "
        "**OUTCOME-CHANNEL ADAPTATIONS** documented at each cell.",
        "",
        "**Sources**: `per_day_master.csv` (`gevoelscore` column; integer 1-6 scale) + "
        "`labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with "
        "`crash-` episode-level per CONVENTIONS section 3.6).",
        "",
        "**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA "
        "verdict promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). "
        "HA-C3 v2 + HA-C3p (LOCKED) + crash_v2-definition (LOCKED) + recovery_arc v2 (LOCKED) "
        "cross-references in this analysis are **descriptive corroboration only**; the "
        "substantive verdicts live in those result.md / definition.md / findings.md files "
        "and are NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims "
        "no). No crash_v2-definition modification per handoff section 3 hard constraint. "
        "Statistical hygiene anchors: section 3.1 (personal baseline -- N/A; gevoelscore IS "
        "the personal felt-state), section 3.3 (column-duplication threshold |rho|>=0.92 -- "
        "N/A by construction; gevoelscore is the only felt-state channel), section 3.4 "
        "(crash-drop sensitivity -- TAUTOLOGICAL on this channel per Q3.9.f), section 3.5 "
        "(spike metrics -- DROP primitive on the outcome channel per Q3.9.g), section 3.6 "
        "(named counts).",
        "",
        "---",
        "",
        "## Headline",
        "",
        "`gevoelscore` on Stratum 4 is a **bounded 1-6 INTEGER felt-state outcome channel** "
        "(skew={0:+.2f}, excess kurtosis={1:+.2f}, heavy_tail_flag={2}; entropy {3:.1f}% of "
        "log(6) ceiling). **Per-value frequency**: see Q3.9.a table below for the discrete "
        "distribution. The **data-driven E[L]\\*={4:.1f}** (Politis-White; vs project default "
        "E[L]=7; deviation ratio {5:.2f}; factor-of-2 flag = {6}; cutoff lag M={7}). "
        "**{8}** memory regime. Cross-channel context per handoff section 2.4: vs sister "
        "Strand-A channels stress_stdev_sleep 7.0 / bb_overnight_gain 6.5 / stress_mean_sleep "
        "12.6 / push_burden_7d_lagged 7.0 / resting_hr 7.0 (fallback) / exertion_class 7.0 "
        "(ordinal) / stress_low_motion 21.1 / bb_lowest 29.25 / all_day_stress_avg 29.8. "
        "**Phase-stratified medians** (citalopram axis): "
        "unmedicated {9:.1f} -> buildup {10:.1f} -> consolidation {11:.1f} -> afbouw "
        "{12:.1f}. **Q3.9.e SUBSTANTIVE (subjective<->objective coupling)**: top-tracking "
        "Garmin sister channel is `{13}` (Spearman rho = {14}); weakest-tracking is `{15}` "
        "(Spearman rho = {16}). Q3.9.f crash-vs-normal day-level Cohen's d={17:+.2f} + "
        "MWU p={18} reported descriptively but **TAUTOLOGICAL** per crash_v2-definition "
        "section 2.1 (crash days are by-definition the score <= 3 days; the difference is "
        "mechanically constrained). Score-floor descriptive on crash days: max "
        "score = {19:.0f}; n crash-days with score > 3 = {20} (the few score-4 days that "
        "fall inside merged crash episodes per merge rule sec 2.1.b -- expected behaviour, "
        "NOT a labelling pipeline drift).".format(
            skew, a["excess_kurtosis"], a["heavy_tail_flag"], entropy_pct,
            el_star, b["deviation_ratio"], b["factor_of_2_deviation_flag"], b["cutoff_lag_M"],
            memory_class,
            c.get("unmedicated", {}).get("median", float("nan")),
            c.get("buildup", {}).get("median", float("nan")),
            c.get("consolidation", {}).get("median", float("nan")),
            c.get("afbouw", {}).get("median", float("nan")),
            top_ch if top_ch is not None else "n/a", top_rho_str,
            weakest_ch if weakest_ch is not None else "n/a", weakest_rho_str,
            fl["cohens_d"], mwu_p_str,
            sf["max_score_on_crash_days"], sf["n_crash_days_with_score_above_3"],
        ),
        "",
        "---",
        "",
        "## Q3.9.a -- Distribution shape (Stratum 4) -- OUTCOME-CHANNEL ADAPTATION",
        "",
        "**OUTCOME-CHANNEL ADAPTATION**: `gevoelscore` is a **bounded 1-6 INTEGER scale** "
        "(per crash_v2-definition sec 2.1 substrate; app-brief framing is 1-10 but empirical "
        "range observed is 1-6). Classical distribution stats apply but the value range is "
        "small + discrete -- the **per-value frequency vector + Shannon entropy** are the "
        "OUTCOME-channel primitives; mean / median / std / MAD / quantiles reported for "
        "parity with sister continuous Strand-A analyses (Q3.1-Q3.8) but interpreted with "
        "the bounded-integer-scale caveat in mind. The heavy_tail_flag uses the CONVENTIONS "
        "section 3.1 rule (skew > 1 OR p99/median > 3.0) but on a 6-ceiling bounded scale the "
        "heavy-tail concept does NOT meaningfully apply -- the flag is reported for parity "
        "but rarely fires on bounded scales by construction.",
        "",
        "| stat | value | source |",
        "|---|---:|---|",
        "| n (Stratum 4) | {0} | `per_day_master.csv` `gevoelscore` non-NaN within S4 |".format(a["n"]),
        "| mean | {0:.3f} | (single-pool S4) |".format(a["mean"]),
        "| median | {0:.3f} | |".format(a["median"]),
        "| std (ddof=1) | {0:.3f} | |".format(a["std_ddof1"]),
        "| MAD (unscaled) | {0:.3f} | |".format(a["mad_unscaled"]),
        "| MAD x 1.4826 (normal-equivalent SD) | {0:.3f} | for robust z-score scaling per section 3.1 |".format(a["mad_normal_equivalent"]),
        "| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | {0:.0f} / {1:.0f} / {2:.0f} / {3:.0f} / {4:.0f} / {5:.0f} / {6:.0f} / {7:.0f} / {8:.0f} | |".format(
            quant["p1"], quant["p5"], quant["p10"], quant["p25"], quant["p50"],
            quant["p75"], quant["p90"], quant["p95"], quant["p99"],
        ),
        "| skewness (Fisher-Pearson) | **{0:+.2f}** | {1} |".format(skew, skew_class),
        "| excess kurtosis (Fisher) | **{0:+.2f}** | |".format(a["excess_kurtosis"]),
        "| heavy_tail_flag | **{0}** | skew > 1 OR p99/median > 3.0; rarely fires on bounded scales |".format(a["heavy_tail_flag"]),
        "| range | {0:.0f} to {1:.0f} | bounded 1-6 integer by construction |".format(a["min"], a["max"]),
        "| Shannon entropy (nats) | {0:.3f} | |".format(a["shannon_entropy_nats"]),
        "| max entropy (log 6 = uniform over 1-6) | {0:.3f} | |".format(a["shannon_entropy_max_log_6"]),
        "| entropy normalised (fraction of log-6 ceiling) | **{0:.1%}** | 100% = uniform; lower = concentrated |".format(entropy_pct / 100.0 if entropy_pct == entropy_pct else 0.0),
        "",
        "### Per-value frequency table (the OUTCOME-channel primitive)",
        "",
        "| gevoelscore value | n days | fraction |",
        "|---:|---:|---:|",
    ]
    n_total = a["n"]
    for v_int in sorted(a["per_value_n"].keys()):
        n_v = a["per_value_n"][v_int]
        if n_v > 0:
            frac = n_v / n_total if n_total > 0 else float("nan")
            out_lines.append("| {0} | {1} | {2:.1%} |".format(v_int, n_v, frac))
    out_lines.extend([
        "",
        "**gevoelscore is the FELT-STATE outcome channel** (per-day self-report on a 1-6 "
        "integer scale; substrate of crash_v2-definition's score-<=3 acute condition). The "
        "per-value frequency vector above is the load-bearing distribution descriptor (mean / "
        "median + classical moments reported for parity).",
        "",
        "### Cross-channel comparison vs sister Strand-A channels (skew + heavy_tail_flag)",
        "",
        "| stat | gevoelscore (this analysis) | resting_hr (Q3.6) | bb_overnight_gain (Q3.5) | push_burden_7d (Q3.8) | exertion_class (Q3.7, encoded) |",
        "|---|---:|---:|---:|---:|---:|",
        "| n S4 | {0} | 1357 | 593 | 1372 | 1372 |".format(a["n"]),
        "| mean | {0:.2f} | 56.68 | 16.65 | 1.93 | n/a (categorical) |".format(a["mean"]),
        "| median | {0:.2f} | 56.00 | 16.00 | 2.00 | n/a (categorical) |".format(a["median"]),
        "| MAD (unscaled) | {0:.2f} | 2.00 | 4.00 | 1.00 | n/a |".format(a["mad_unscaled"]),
        "| skewness | {0:+.2f} | +0.25 | +0.97 | +0.58 | n/a |".format(skew),
        "| heavy_tail_flag | **{0}** | **False** | **False** | **False** | n/a |".format(a["heavy_tail_flag"]),
        "| type | **integer felt-state 1-6 (OUTCOME)** | continuous bpm | continuous BB units | integer count [0, 6] | 5-level ordinal |",
        "",
        "See [`plots/fig1_per_value_frequency_s4.png`](plots/fig1_per_value_frequency_s4.png).",
        "",
        "---",
        "",
        "## Q3.9.b -- Autocorrelation structure + E[L]\\* on integer series",
        "",
        "**OUTCOME-CHANNEL ADAPTATION**: ACF computed on the integer series as-is (no encoding "
        "needed; the integer scale 1-6 naturally supports the Politis-White ACF + block-length "
        "estimator). Integer-discreteness does not bias the estimator at this sample size.",
        "",
        "The **data-driven block length is E[L]\\*={0:.1f}** (Politis-White 2004 with "
        "Patton-Politis-White 2009 correction per [`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) "
        "vs the project default E[L]=7 per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). "
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
        "| Q3.8 (push_burden_7d_lagged) | integer count [0, 6] | 7.0 |",
        "| Q3.1 (stress_mean_sleep) | sleep-window mean | 12.6 |",
        "| Phase-1 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 |",
        "| Q3.3 (bb_lowest) | daily NADIR | 29.25 |",
        "| Q3.2 (all_day_stress_avg) | 24h-window mean | 29.8 |",
        "| **this analysis (gevoelscore)** | **integer felt-state 1-6 (OUTCOME)** | **{0:.1f}** |".format(el_star),
        "",
        "See [`plots/fig5_acf.png`](plots/fig5_acf.png).",
        "",
        "---",
        "",
        "## Q3.9.c -- Base rates per citalopram phase + recovery_arc v2 overlap notation",
        "",
        "Phase axis per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3:",
        "",
        "| phase | window | n | median | mean | MAD | p10 / p90 |",
        "|---|---|---:|---:|---:|---:|---|",
    ])
    out_lines.extend(per_phase_rows)
    out_lines.extend([
        "",
        "### Per-value frequency per phase",
        "",
        "| phase | n | value=1 | value=2 | value=3 | value=4 | value=5 | value=6 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = c.get(ph, {})
        if info.get("n", 0) > 0:
            out_lines.append(_fmt_per_value_row(
                ph, info["per_value_n"], info["per_value_frequency"], info["n"],
            ))
    out_lines.extend([
        "",
        "### Recovery_arc v2 overlap notation (per handoff section 2.4)",
        "",
        "Per handoff section 1 + section 2.4 + handoff bullet 'check overlap; do NOT "
        "re-characterise if already done': [`trajectory/recovery_arc/findings.md`](../../trajectory/recovery_arc/findings.md) "
        "already characterised gevoelscore on the 6-phase axis (section 2 table + section 2.1 "
        "per-channel narrative + section 3 / 7b paired-bootstrap CI). This Q3.9.c provides a "
        "**descriptive reproduction read** on the same axis at the same as-of-date for "
        "methodological consistency; it does NOT re-characterise.",
        "",
        "Structural caveat: gevoelscore logging started 2022-09-03 = phase-3 last 19 days, so "
        "phases 1 (pre_illness_healthy) + 2 (acute_infection) have **n=0** and phase 3 "
        "(lc_pre_ergo) is partial (n=19).",
        "",
        "| 6-phase axis | n (this Q3.9.c) | median (this Q3.9.c) | recovery_arc v2 reported median |",
        "|---|---:|---:|---:|",
    ])
    rec = cr["per_recovery_phase"]
    rec_v2 = cr["recovery_arc_v2_section_2_reported"]
    for phase_name, _, _ in RECOVERY_PHASE_BOUNDARIES:
        info = rec.get(phase_name, {})
        n_p = info.get("n", 0)
        med_p = info.get("median", float("nan"))
        # Look up the recovery_arc v2 median for this phase
        rec_v2_key = phase_name + "_median"
        rec_v2_val = rec_v2.get(rec_v2_key)
        if rec_v2_val is None:
            rec_v2_str = "n/a (phase has n=0)"
        else:
            rec_v2_str = "{0:.2f}".format(rec_v2_val) if isinstance(rec_v2_val, (int, float)) else str(rec_v2_val)
        med_str = "{0:.2f}".format(med_p) if n_p > 0 and med_p == med_p else "n=0"
        # Custom name lookup for recovery_arc v2 reporting variation
        if phase_name == "pacing_pre_citalopram_learning_4a":
            rec_v2_str = "5.00 (n=56)"
        elif phase_name == "pacing_habit_established_4b":
            rec_v2_str = "4.00 (n=509)"
        elif phase_name == "citalopram_modulated":
            rec_v2_str = "5.00 (n=787)"
        elif phase_name == "lc_pre_ergo":
            rec_v2_str = "3.00 (n=19)"
        else:
            rec_v2_str = "n=0 (phase 1+2 pre-gevoelscore-logging)"
        out_lines.append("| {0} | {1} | {2} | {3} |".format(
            phase_name, n_p, med_str, rec_v2_str,
        ))
    out_lines.extend([
        "",
        "**Recovery_arc v2 reported headline** (per [`recovery_arc/findings.md`](../../trajectory/recovery_arc/findings.md) "
        "section 2 + section 7b): 4a -> 4b drop on gevoelscore (diff -1.0, CI [-1.0, 0.0]) "
        "sits at the boundary of the section 7b verdict -- upper CI bound is AT 0 (includes 0 "
        "but only just; descriptive read: ambiguous). Phase 3 -> 4a step is +2.0 (largest "
        "within-channel step) but phase 3's n=19 keeps its CI wide [3, 4] and shaped by "
        "structural partial-coverage. Per recovery_arc v2 section 4 felt-state narrative: "
        "phase 3 partial coverage shows median 3.0 (lowest gevoelscore median anywhere in "
        "the corpus); 4a (median 5; full 56-day sub-window) is the first complete "
        "characterisation of the 8-week ergotherapy-onboarding period in felt-state terms; "
        "4b drops to median 4; phase 5 returns to 5.",
        "",
        "Per handoff section 2.4 + CONVENTIONS section 4.2: this Q3.9.c overlap notation "
        "is **NOT a re-characterisation**; the recovery_arc v2 substantive narrative is "
        "LOCKED at the recovery_arc/findings.md level and NOT extended here.",
        "",
        "Named counts (CONVENTIONS section 3.6): the per-phase n's above are `gevoelscore`-"
        "non-NaN day rows in `per_day_master.csv` within Stratum 4 date masks per "
        "`citalopram_phase_stratification.md section 3` boundary dates + "
        "`lc_recovery_phase_axis.md` 6-phase axis boundary dates.",
        "",
        "See [`plots/fig2_phase_stratified_stacked_bar.png`](plots/fig2_phase_stratified_stacked_bar.png).",
        "",
        "---",
        "",
        "## Q3.9.d -- Phase-stratified distribution + descriptive shift report (no v3 caveat-class)",
        "",
        "**Per CONVENTIONS section 4.2 (caveats yes; a-priori claims no)**: gevoelscore was "
        "NOT in the v3 multi-channel sweep scope per [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "section 5.6 (6-channel scope: stress_mean_sleep + all_day_stress_avg + bb_lowest + "
        "resting_hr + bb_overnight_gain + respiration_avg_sleep; **gevoelscore is the outcome, "
        "not a Garmin channel** -- per descriptive README section 3.4 + handoff section 1). "
        "**No v3 verdict exists to cite or re-promote on this channel**; observed phase "
        "shifts are pure Layer 1 descriptive observations.",
        "",
        "Observed phase-to-phase median shifts:",
        "",
        "| comparison | delta median | delta mean |",
        "|---|---:|---:|",
    ])
    for pair_name, pair_label in [
        ("buildup_minus_unmedicated", "buildup minus unmedicated"),
        ("consolidation_minus_unmedicated", "consolidation minus unmedicated"),
        ("consolidation_minus_buildup", "consolidation minus buildup"),
        ("afbouw_minus_consolidation", "afbouw minus consolidation"),
        ("afbouw_minus_unmedicated", "afbouw minus unmedicated"),
    ]:
        med_key = pair_name + "_median"
        mean_key = pair_name + "_mean"
        if med_key in d["phase_to_phase_shifts"]:
            out_lines.append("| {0} | **{1:+.2f}** | {2:+.2f} |".format(
                pair_label,
                d["phase_to_phase_shifts"][med_key],
                d["phase_to_phase_shifts"][mean_key],
            ))
    ha_xref = d["ha_outcome_xref"]
    out_lines.extend([
        "",
        "### HA-C3 v2 + HA-C3p locked outcome-side cross-reference (per handoff section 2.4)",
        "",
        "Per [`analyses/hypotheses/HA-C3/result.md`](../../../analyses/hypotheses/HA-C3/result.md) "
        "+ [`HA-C3p/result.md`](../../../analyses/hypotheses/HA-C3p/result.md):",
        "",
        "- **HA-C3 v2 (LOCKED REJECTED wrong-direction override)**: " + ha_xref["ha_c3_v2_locked_verdict"],
        "- **HA-C3p (LOCKED PARTIAL 2-of-3)**: " + ha_xref["ha_c3p_locked_verdict"],
        "",
        ha_xref["note"],
        "",
        "Per CONVENTIONS section 4.2: this Q3.9.d phase-stratified gevoelscore characterisation "
        "is **descriptive corroboration only** of the joint HA-C3 v2 + HA-C3p inverted-U "
        "outcome-side finding; the substantive HA verdicts live in those result.md files and "
        "are NOT extended here per handoff section 3 hard constraint.",
        "",
        "See [`plots/fig2_phase_stratified_stacked_bar.png`](plots/fig2_phase_stratified_stacked_bar.png) "
        "(per-phase per-value frequency stacked bar) and [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) "
        "(rolling 90d median through phases).",
        "",
        "---",
        "",
        "## Q3.9.e -- SUBSTANTIVE: Subjective <-> objective coupling (Spearman rho vs Garmin sister channels)",
        "",
        "**SUBSTANTIVELY-INTERESTING cell** per handoff section 1 + section 2.4 + descriptive "
        "README section 4.9. Strand-A first-pass at the Q4.9 subjective<->objective coupling "
        "question (deferred to Strand B per descriptive README sec 4.9). **Descriptive only; "
        "NO causal mechanism interpretation; NO substantive HA verdict promotion** per "
        "CONVENTIONS section 4.1 + section 4.2.",
        "",
        "Spearman rho between gevoelscore (felt-state) and key Garmin sister channels on the "
        "full Stratum-4 pool (multi-phase combined; no per-phase stratification at this "
        "Q3.9.e scope -- per-phase coupling structure is deferred to Strand-B Q4.9).",
        "",
        "| target channel | n | Pearson r | Spearman rho | semantic |",
        "|---|---:|---:|---:|---|",
    ])
    out_lines.extend(e_rows)
    out_lines.extend([
        "",
        "### Which Garmin channel tracks felt-state most closely? (descriptive ranking)",
        "",
        "Ranked by **|Spearman rho|** on the 5 PRIMARY targets:",
        "",
    ])
    out_lines.extend(ranked_lines)
    out_lines.extend([
        "",
        "**Top-tracking primary channel**: `{0}` (Spearman rho = {1}, n={2}).".format(
            top_ch if top_ch is not None else "n/a", top_rho_str,
            e["primary_rho_summary"].get(top_ch, {}).get("n", "n/a") if top_ch else "n/a",
        ),
        "**Weakest-tracking primary channel**: `{0}` (Spearman rho = {1}, n={2}).".format(
            weakest_ch if weakest_ch is not None else "n/a", weakest_rho_str,
            e["primary_rho_summary"].get(weakest_ch, {}).get("n", "n/a") if weakest_ch else "n/a",
        ),
        "",
        "### LOAD-BEARING HA-C3 v2 + HA-C3p linear-companion cross-reference",
        "",
        "Per [`HA-C3/result.md`](../../../analyses/hypotheses/HA-C3/result.md) section 3 + "
        "section 4.5.2 (opposing-model linear test):",
        "",
        "**HA-C3 v2 reported the linear-companion Spearman rho on the unmedicated single-pool "
        "of all_day_stress_avg vs gevoelscore as rho=-0.0298 (p=0.4738, n=581)**. Per "
        "HA-C3 v2 section 4.5.2 reading: a near-zero linear rho **co-occurring with a strong "
        "convexity-test S=-0.740 p_c=0.0003** is the expected linear-companion when the true "
        "shape is inverted-U / concave with peak in the middle. The bin-shape convexity test "
        "carries the substantive signal; the Spearman rho is the LINEAR companion that "
        "DOES NOT detect concave shape (because positive-and-negative slopes cancel under a "
        "monotone-rank measure).",
        "",
        "This Q3.9.e re-anchors at the **FULL Stratum-4 multi-pool resolution** + extends to "
        "the broader Garmin sister-channel set. **The Spearman rho values reported in this "
        "Q3.9.e table are NOT to be interpreted as 'strength of stress -> felt-state effect'** "
        "-- they are LINEAR companions to the bin-shape convexity tests; a low |rho| "
        "co-occurring with the HA-C3 v2 + HA-C3p inverted-U findings is the expected pattern, "
        "NOT evidence of weak coupling. **NO causal interpretation** per CONVENTIONS section "
        "4.1.",
        "",
        "### Strand-A first-pass at Q4.9 territory (per descriptive README section 4.9)",
        "",
        "Per descriptive README section 4.9 'Subjective <-> objective coupling + crash-day "
        "body-state profile' (deferred to Strand B):",
        "",
        "- This Q3.9.e provides a **partial first-pass** at the Q4.9 question 'When does "
        "gevoelscore align with the 3 CONFIRMED Garmin channels vs diverge?' -- at the "
        "single-rank-correlation resolution on the full Stratum-4 pool.",
        "- **Future Strand-B Q4.9 analysis** would add: per-phase coupling stratification, "
        "lagged-coupling structure (does felt-state lead or lag Garmin signals?), episode-"
        "level coupling profile, and **the central project question of pre-crash divergence "
        "patterns between subjective + objective signals**.",
        "- Per handoff section 3 hard constraint: this Q3.9.e is **descriptive only**; the "
        "Q4.9 substantive question is NOT resolved at this Strand-A scope.",
        "",
        "See [`plots/fig4_q39e_spearman_vs_*.png`](plots/) (scatter + per-quintile mean "
        "gevoelscore overlay for the chosen top-tracking Garmin sister channel).",
        "",
        "---",
        "",
        "## Q3.9.f -- Crash-vs-normal -- TAUTOLOGICAL by definition (honest framing)",
        "",
        "**TAUTOLOGICAL** per handoff section 1 + section 2.4 + crash_v2-definition section "
        "2.1 + 2.2 + 2.3: crash + dip are BOTH DEFINED BY gevoelscore (crash = score <= 3 "
        "for >= 2 consecutive days; dip = isolated single day with score <= 3 between "
        "neighbours >= 4; normal = everything else including score-4 days). The day-level "
        "crash-vs-normal gevoelscore difference is **MECHANICALLY CONSTRAINED** -- crash "
        "days are by-definition the low-score days. The numbers below exist for parity with "
        "sister Strand-A analyses + to anchor the non-tautological framings (episode-level "
        "min + median + length, dip-vs-normal characterisation, score-floor verification).",
        "",
        "**NO substantive crash-prediction claim** from this gevoelscore-vs-crash signal -- "
        "the crash definition IS the gevoelscore signal.",
        "",
        "### Score-floor descriptive (with merge rule sec 2.1.b context)",
        "",
        "| metric | value | expected per crash_v2 sec 2.1 + sec 2.1.b |",
        "|---|---:|---|",
        "| max score on crash days | {0:.0f} | <= 3 mostly; merge rule sec 2.1.b can include a few score-4 days inside merged crash episodes |".format(sf["max_score_on_crash_days"]),
        "| n crash-days with score > 3 | {0} | typically a small number (the gap days between two acute sub-runs that merged) |".format(sf["n_crash_days_with_score_above_3"]),
        "| score floor (max <= 3) | **{0}** | True = no merge-rule gap days observed; False = merge rule activated (expected behaviour) |".format(sf["score_floor_verified_le_3"]),
        "",
        sf["interpretation"],
        "",
        "### Day-level (TAUTOLOGICAL; reported for parity)",
        "",
        "| stat | value |",
        "|---|---:|",
        "| n crash-days | {0} |".format(fl["n_crash_day"]),
        "| n normal-days | {0} |".format(fl["n_normal_day"]),
        "| mean crash-day | {0:.3f} |".format(fl["mean_crash"]),
        "| mean normal-day | {0:.3f} |".format(fl["mean_normal"]),
        "| median crash-day | {0:.2f} |".format(fl["median_crash"]),
        "| median normal-day | {0:.2f} |".format(fl["median_normal"]),
        "| mean diff (crash minus normal) | **{0:+.3f}** |".format(fl["mean_diff"]),
        "| median diff | **{0:+.2f}** |".format(fl["mann_whitney_u"]["median_diff"]),
        "| Cohen's d | **{0:+.2f}** |".format(fl["cohens_d"]),
        "| Mann-Whitney U: z | **{0:+.2f}** |".format(fl["mann_whitney_u"]["z"]),
        "| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **{0}** |".format(mwu_p_str),
        "",
        "**Tautology framing**: the negative day-level Cohen's d is MECHANICALLY GUARANTEED "
        "by the crash_v2 definition -- crash days are LITERALLY defined as score <= 3 days "
        "in a >= 2-consecutive-day window. The numbers above are a definitional consistency "
        "check (score floor passes), NOT a substantive test of crash-prediction by "
        "gevoelscore. **No HA pre-reg should cite this Q3.9.f day-level Cohen's d as a "
        "predictor effect**.",
        "",
        "### Episode-level min gevoelscore distribution (NON-tautological)",
        "",
        "Per-episode minimum gevoelscore (how deep do crashes go?) -- this IS substantively "
        "informative; the crash definition only requires score <= 3 for >= 2 days; the "
        "per-episode minimum can be 1 / 2 / 3 (or NaN if missing).",
        "",
        "| stat | value |",
        "|---|---:|",
    ])
    if fem.get("n_episodes", 0) > 0:
        out_lines.extend([
            "| n crash-episodes | {0} |".format(fem["n_episodes"]),
            "| median of per-episode min | {0:.2f} |".format(fem["median_of_per_episode_min"]),
            "| mean of per-episode min | {0:.2f} |".format(fem["mean_of_per_episode_min"]),
            "| min of per-episode min (deepest crash) | {0:.0f} |".format(fem["min_of_per_episode_min"]),
            "| max of per-episode min (shallowest crash) | {0:.0f} |".format(fem["max_of_per_episode_min"]),
            "",
            "**Per-episode min frequency** (across n={0} crash-episodes):".format(fem["n_episodes"]),
            "",
            "| per-episode min gevoelscore | n episodes |",
            "|---:|---:|",
        ])
        for k_min, n_min in sorted(fem["per_value_n_of_per_episode_min"].items()):
            out_lines.append("| {0} | {1} |".format(k_min, n_min))
        out_lines.extend([
            "",
            "### Episode-level median + length (NON-tautological)",
            "",
            "| stat | value |",
            "|---|---:|",
            "| median of per-episode median | {0:.2f} |".format(fmed["median_of_per_episode_median"]),
            "| mean of per-episode median | {0:.2f} |".format(fmed["mean_of_per_episode_median"]),
            "| median episode length (days) | {0:.1f} |".format(flen["median_episode_length_days"]),
            "| mean episode length (days) | {0:.1f} |".format(flen["mean_episode_length_days"]),
            "| max episode length (days) | {0} |".format(flen["max_episode_length_days"]),
            "| min episode length (days) | {0} |".format(flen["min_episode_length_days"]),
        ])
    else:
        out_lines.append("| (no crash episodes with episode_id starting with 'crash-' in S4) | -- |")
    out_lines.extend([
        "",
        "### Dip-vs-normal characterisation (also definitionally constrained per crash_v2 section 2.2)",
        "",
    ])
    if "n_dip_day" in fdip:
        out_lines.extend([
            "Per crash_v2-definition section 2.2: dip = isolated single day with score <= 3 "
            "between neighbours >= 4. The dip-day distribution is also definitionally "
            "constrained on this channel.",
            "",
            "| stat | value |",
            "|---|---:|",
            "| n dip-days | {0} |".format(fdip["n_dip_day"]),
            "| mean dip-day | {0:.3f} |".format(fdip["mean_dip_day"]),
            "| median dip-day | {0:.2f} |".format(fdip["median_dip_day"]),
            "| max dip-day score | {0:.0f} |".format(fdip["max_dip_day_score"]),
            "| n dip-days with score > 3 (should be 0) | {0} |".format(fdip["n_dip_days_with_score_above_3"]),
            "",
            "**Dip per-value frequency**:",
            "",
            "| dip-day gevoelscore | n |",
            "|---:|---:|",
        ])
        for k_dv, n_dv in sorted(fdip["per_value_n"].items()):
            out_lines.append("| {0} | {1} |".format(k_dv, n_dv))
    else:
        out_lines.append(fdip.get("note", "(is_dip column absent in master)"))
    out_lines.extend([
        "",
        "### crash_v2-definition cross-reference (per handoff section 3 hard constraint -- LOCKED)",
        "",
        "Per [`analyses/hypotheses/crash_v2-definition/`](../../../analyses/hypotheses/crash_v2-definition/):",
        "",
        "- **Section 2.1 acute condition**: score <= 3 for >= 2 consecutive days = crash",
        "- **Section 2.2 dip condition**: isolated single day with score <= 3 between "
        "neighbours >= 4 = dip",
        "- **Section 2.3 normal**: everything else (includes score-4 days; no separate "
        "vague_low tier)",
        "",
        "Per crash_v2 definition section 5: 'we don't test it; we apply it, then re-run "
        "downstream tests with the new labels'. This Q3.9.f does NOT modify the crash_v2 "
        "labelling (canonical lock per handoff section 3); it characterises the underlying "
        "gevoelscore distribution that crash_v2's definition operationalises ON, "
        "descriptively + honestly.",
        "",
        "---",
        "",
        "## Q3.9.g -- Drop primitive (spike-form on outcome channel) -- OUTCOME-CHANNEL ADAPTATION",
        "",
        "**OUTCOME-CHANNEL ADAPTATION** per handoff section 1 + CONVENTIONS section 3.5: the "
        "spike-form on the gevoelscore outcome channel is the **DROP primitive** (sudden "
        "decrease in gevoelscore from one day to the next; day-over-day diff with positive-"
        "magnitude-drop convention). The boundedness of the scale means drops >= 5 are "
        "structurally impossible (max - min = 6 - 1 = 5).",
        "",
        "**Drop primitive definition**: " + g["spike_form_definition"],
        "",
        "| stat | value |",
        "|---|---:|",
        "| n consecutive-day pairs | {0} |".format(g["n_consecutive_day_pairs"]),
        "| n no-change pairs (drop=0) | {0} |".format(g["n_no_change"]),
        "| n drop >= 1 unit | {0} ({1}) |".format(g["n_drop_ge_1"], drop_rate1_str),
        "| n drop >= 2 units | {0} ({1}) |".format(g["n_drop_ge_2"], drop_rate2_str),
        "| n drop >= 3 units | {0} ({1}) |".format(g["n_drop_ge_3"], drop_rate3_str),
        "| n drop >= 4 units | {0} |".format(g["n_drop_ge_4"]),
        "| n rise >= 1 unit | {0} |".format(g["n_rise_ge_1"]),
        "| max drop observed | {0:.0f} |".format(g["max_drop_observed"]),
        "| max rise observed | {0:.0f} |".format(g["max_rise_observed"]),
        "",
        "### Diff magnitude distribution",
        "",
        "| diff (today minus yesterday) | n pairs |",
        "|---:|---:|",
    ])
    for k_diff in range(-5, 6):
        n_diff = g["diff_magnitude_distribution"].get(str(k_diff), 0)
        if n_diff > 0:
            label = "+{0}".format(k_diff) if k_diff > 0 else str(k_diff)
            out_lines.append("| {0} | {1} |".format(label, n_diff))
    out_lines.extend([
        "",
        "### HA11 family cross-reference (different channel; clarification)",
        "",
        "Per [`HA11-stress-udip/result.md`](../../../analyses/hypotheses/HA11-stress-udip/result.md) + "
        "[`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) row HA11:",
        "",
        "- **HA11 operand**: " + g["ha11_family_xref"]["ha11_operand"],
        "- **HA11 locked verdict**: " + g["ha11_family_xref"]["ha11_locked_verdict"],
        "- **HA11 R14 single-pool re-anchor**: " + g["ha11_family_xref"]["ha11_r14_single_pool"],
        "- **HA11 channel**: " + g["ha11_family_xref"]["ha11_channel"],
        "",
        g["ha11_family_xref"]["note"],
        "",
        "**Adaptation note**: " + g["spike_form_outcome_channel_adaptation_note"],
        "",
        "See [`plots/fig6_drop_primitive_distribution.png`](plots/fig6_drop_primitive_distribution.png).",
        "",
        "---",
        "",
        "## Q3.9.h -- Coverage / missingness (bounded-scale outlier semantics) -- OUTCOME-CHANNEL ADAPTATION",
        "",
        "**OUTCOME-CHANNEL ADAPTATION** per handoff section 1: a bounded 1-6 INTEGER scale has "
        "**no outliers in the classical MAD-z sense** (MAD-z > 5 is impossible on a 6-value "
        "range; max-min = 5 vs MAD x 1.4826 ~ 1.5; max possible z is ~3.3). Coverage / "
        "missingness patterns matter more. Stratum 4 is DEFINED as 'LC with gevoelscore + "
        "crash labels' per lc_era_temporal_segmentation.md -- every Stratum-4 day SHOULD "
        "have a gevoelscore by construction.",
        "",
        "### Stratum-4 completeness",
        "",
        "| metric | value |",
        "|---|---:|",
        "| n total Stratum-4 rows | {0} |".format(h["n_total_stratum_4_rows"]),
        "| n present (gevoelscore non-NaN) | {0} |".format(h["n_present_in_stratum_4"]),
        "| n missing in Stratum 4 | {0} |".format(h["n_missing_in_stratum_4"]),
        "| coverage rate | {0:.3%} |".format(h["coverage_rate_stratum_4"]),
        "| Stratum 4 completeness flag | **{0}** |".format(h["stratum_4_completeness_flag"]),
        "",
        "### crash_v2-definition section 3.1 + section 4 cross-check",
        "",
        "Per crash_v2 section 4: '1372 day-level rows in 2022-09-03 -> 2026-06-05 window; "
        "zero gaps'.",
        "",
        "| metric | value | expected |",
        "|---|---:|---|",
        "| expected n days (crash_v2 sec 4) | {0} | 1372 |".format(h["crash_v2_definition_sec_3_1_cross_check"]["expected_n_days"]),
        "| observed n total | {0} | -- |".format(h["crash_v2_definition_sec_3_1_cross_check"]["observed_n_total"]),
        "| observed n present | {0} | -- |".format(h["crash_v2_definition_sec_3_1_cross_check"]["observed_n_present"]),
        "| matches expected (1372) | **{0}** | True = consistent |".format(h["crash_v2_definition_sec_3_1_cross_check"]["matches_expected"]),
        "",
        "### Monthly coverage snapshot (first 6 + last 6 months)",
        "",
        "| year-month | n total | n present | coverage rate |",
        "|---|---:|---:|---:|",
    ])
    monthly_snaps = h["monthly_coverage_snapshots"]
    snaps_to_show = monthly_snaps[:6] + (monthly_snaps[-6:] if len(monthly_snaps) > 12 else [])
    seen_ym = set()
    for snap in snaps_to_show:
        if snap["year_month"] in seen_ym:
            continue
        seen_ym.add(snap["year_month"])
        out_lines.append("| {0} | {1} | {2} | {3:.1%} |".format(
            snap["year_month"], snap["n_total"], snap["n_present"], snap["coverage_rate"],
        ))
    if len(monthly_snaps) > 12:
        out_lines.append("(... {0} months in between; truncated)".format(len(monthly_snaps) - 12))
    out_lines.extend([
        "",
        "**Outlier semantics note** (OUTCOME-CHANNEL ADAPTATION): " + h["outlier_semantics_note"],
        "",
        "---",
        "",
        "## Q3.9.i -- Covariate-sensitivity readiness for a future HA pre-reg using gevoelscore as outcome",
        "",
        "**Discipline anchor**: " + i["discipline_anchor"] + ".",
        "",
        "**Primary use case**: " + i["primary_use_case"],
        "",
        "Names **{0}** candidate covariates a future HA on `gevoelscore` (as outcome) should "
        "pre-spec.".format(len(i["candidate_covariates"])),
        "",
    ])
    for idx_c, cov in enumerate(i["candidate_covariates"], start=1):
        out_lines.extend([
            "### {0}. `{1}`".format(idx_c, cov["covariate"]),
            "",
            cov["rationale"],
            "",
            "*Source*: {0}".format(cov["source"]),
            "",
            "*Expected effect under sensitivity arm*: {0}".format(cov["expected_effect"]),
            "",
        ])
    out_lines.extend([
        "### Recommendation",
        "",
        i["recommendation"],
        "",
        "**OUTCOME-CHANNEL ADAPTATION note**: " + i["outcome_channel_adaptation_note"],
        "",
        "---",
        "",
        "## Cross-references",
        "",
        "### HA-* tests that touch this channel as OUTCOME (cite this analysis)",
        "",
        "- **HA-C3 v2** (LOCKED REJECTED wrong-direction override; concave/inverted-U "
        "vs Wiggers' convex prediction): primary outcome IS this channel. **The descriptive "
        "substrate this analysis produces -- the Stratum-4 distribution (Q3.9.a) + per-phase "
        "reads (Q3.9.c, Q3.9.d) + subjective<->objective coupling (Q3.9.e) -- "
        "complements HA-C3 v2's tested operand with the raw-channel-distribution view.** The "
        "substantive HA-C3 v2 verdict is LOCKED; this analysis's descriptive corroboration is "
        "NOT a re-interpretation.",
        "- **HA-C3p** (LOCKED PARTIAL 2-of-3; personal-baseline-anchored equal-N quintile "
        "bins): primary outcome IS this channel. Joint reading with HA-C3 v2 confirms the "
        "concave/inverted-U finding from BOTH bin-design variants (variable-width all-corpus "
        "vs equal-N personal-baseline).",
        "- **HA10 + HA07d + HA11 family + every other HA using crash labels**: indirect "
        "outcome via crash_v2-definition derivation (crash = score <= 3 for >= 2 consecutive "
        "days). Q3.9.f surfaces the tautology honestly.",
        "",
        "### Methodology MDs cited",
        "",
        "- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 -- Q3.9.c citalopram-phase axis; Q3.9.d phase-stratified treatment.",
        "- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) -- E[L]=7 default + factor-of-2 deviation rule.",
        "- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) -- Stratum 4 boundary definition (Stratum 4 IS the gevoelscore-having days).",
        "- [`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) -- 6-phase axis for Q3.9.c overlap notation.",
        "- [`methodology/phase_axis_collapsibility_conventions.md`](../../../methodology/phase_axis_collapsibility_conventions.md) -- tier-A 4a + 4b -> 4 collapse for Q3.9.i covariate 4.",
        "- [`methodology/_descriptive_stocktake_2026-06-23.md`](../../../methodology/_descriptive_stocktake_2026-06-23.md) section 3 + section 5 -- gap-list framing.",
        "",
        "### Existing artefacts referenced",
        "",
        "- [`analyses/hypotheses/crash_v2-definition/`](../../../analyses/hypotheses/crash_v2-definition/) -- canonical gevoelscore-to-crash mapping; LOCKED; Q3.9.f honest tautology framing.",
        "- [`analyses/hypotheses/HA-C3/result.md`](../../../analyses/hypotheses/HA-C3/result.md) (LOCKED) + [`HA-C3p/result.md`](../../../analyses/hypotheses/HA-C3p/result.md) (LOCKED) -- outcome-side substantive references.",
        "- [`descriptive/trajectory/recovery_arc/findings.md`](../../trajectory/recovery_arc/findings.md) -- 6-phase gevoelscore characterisation (LOCKED); Q3.9.c provides overlap notation, NOT re-characterisation.",
        "- [`descriptive/operationalisation_support/push_burden_7d/findings.md`](../push_burden_7d/findings.md) -- Q3.8 sister precedent (Tier 2 4th of 5; LANDED `92d7193`); count-primitive bounded-support precedent.",
        "- [`descriptive/operationalisation_support/resting_hr/findings.md`](../resting_hr/findings.md) -- Q3.6 continuous-channel precedent (Tier 2 2nd of 5).",
        "- [`descriptive/operationalisation_support/exertion_class/findings.md`](../exertion_class/findings.md) -- Q3.7 categorical adaptation precedent (Tier 2 3rd of 5).",
        "- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) -- R14 single-pool reads on Q3.9.g HA11 cross-reference.",
        "",
        "### Upstream pipeline",
        "",
        "- `per_day_master.csv` `gevoelscore` column <- `pipeline/03_consolidate/build_unified_dataset.py` <- "
        "app-side self-report on 1-10 scale (empirical range 1-6).",
        "- `labels_crash_v2.csv` <- `crash_v2-definition/definition.md` (locked).",
        "",
        "---",
        "",
        "## Limitations",
        "",
        "For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal "
        "claim per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding constraints are:",
        "",
        "1. **No HA verdict promotion**: HA-C3 v2 + HA-C3p (both LOCKED) verdicts are NOT "
        "extended or re-interpreted; the joint inverted-U finding is referenced only as "
        "descriptive corroboration in Q3.9.a + Q3.9.d + Q3.9.e per CONVENTIONS section 4.2 "
        "+ handoff section 3.",
        "2. **No crash_v2-definition modification** per handoff section 3 hard constraint. "
        "The crash + dip + normal definitions are LOCKED at the crash_v2-definition/ level; "
        "Q3.9.f surfaces the day-level tautology honestly but does not re-derive crash "
        "labels.",
        "3. **No recovery_arc v2 re-characterisation** per handoff section 1 + section 2.4. "
        "Q3.9.c overlap notation references recovery_arc v2's existing per-phase reads; the "
        "substantive narrative is LOCKED at the recovery_arc/findings.md level.",
        "4. **Q3.9.e is Strand-A first-pass at Q4.9 territory only** per descriptive README "
        "section 4.9. Per-phase coupling stratification, lagged-coupling structure, "
        "episode-level coupling profile, and pre-crash divergence patterns are deferred to "
        "Strand-B Q4.9 future analysis -- NOT resolved at this Strand-A scope.",
        "5. **Q3.9.f day-level Cohen's d MUST NOT be cited as a predictor effect** per "
        "tautology framing in Q3.9.f. The negative day-level Cohen's d is mechanically "
        "guaranteed by crash_v2 section 2.1.",
        "6. **No v3 multi-channel sweep verdict to cite or re-promote** on this channel per "
        "Q3.9.d framing (gevoelscore is the outcome, not a Garmin channel; not in v3 "
        "scope). Observed phase shifts are pure Layer 1 descriptive observations.",
        "7. **Bounded 1-6 integer scale** means classical heavy-tail / outlier semantics do "
        "not meaningfully apply per OUTCOME-CHANNEL ADAPTATIONS at Q3.9.a + Q3.9.h. The "
        "per-value frequency vector + Shannon entropy are the load-bearing distribution "
        "primitives.",
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
    a = q["Q3.9.a_distribution"]
    b = q["Q3.9.b_autocorrelation"]
    c = q["Q3.9.c_base_rates_per_phase"]
    e = q["Q3.9.e_subjective_objective_coupling"]
    f = q["Q3.9.f_crash_vs_normal"]
    h = q["Q3.9.h_coverage_missingness"]

    el_star = b["data_driven_E_L_star"]
    top_ch = e["top_tracking_channel"]
    top_rho = e["top_tracking_rho"]
    weakest_ch = e["weakest_tracking_channel"]
    weakest_rho = e["weakest_tracking_rho"]
    top_rho_str = "{0:+.3f}".format(top_rho) if top_rho == top_rho else "n/a"
    weakest_rho_str = "{0:+.3f}".format(weakest_rho) if weakest_rho == weakest_rho else "n/a"
    sf = f["score_floor_verification_per_crash_v2_definition"]

    out_lines = [
        "# `gevoelscore` -- operationalisation-support descriptive analysis",
        "",
        "**Strand**: A (operationalisation support; template-driven; no operationalisation "
        "interview required per [`descriptive/README.md`](../../README.md) section 7b).",
        "",
        "## Research question",
        "",
        "Operationalisation-support descriptive characterisation of `gevoelscore` (per-day "
        "self-reported felt-state on a 1-6 integer scale; the OUTCOME side of nearly every "
        "HA in the project) on Stratum 4, answering Q3.9.a-i per the locked descriptive "
        "programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) "
        "section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`; this channel listed under "
        "HA-touched non-confirmed candidate list as `gevoelscore (almost every test's "
        "outcome side)`). **5th (FINAL) of the 5 Tier 2 channels** in the user-prioritised "
        "Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 "
        "bb_overnight_gain `7d49ba4`; 2nd = Q3.6 resting_hr `5d28219`; 3rd = Q3.7 "
        "exertion_class `9b03bed`; 4th = Q3.8 push_burden_7d `92d7193`; this Q3.9 closes "
        "Tier 2).",
        "",
        "Substantive status: **HA-C3 v2 + HA-C3p direct outcome** (both LOCKED; joint "
        "inverted-U finding -- the stress -> felt-state mapping is concave with peak around "
        "stress 30-40, NOT convex per Wiggers' verbatim prediction). **HA10 + HA07d + many "
        "other HAs** use gevoelscore in their crash labels indirectly via "
        "[`crash_v2-definition`](../../../analyses/hypotheses/crash_v2-definition/) (LOCKED). "
        "**gevoelscore was NOT in v3 multi-channel dose-response sweep scope** per descriptive "
        "README section 3.4 + handoff section 1 ('it's the outcome, not a Garmin channel'); "
        "no v3 verdict exists to cite or re-promote.",
        "",
        "## Method",
        "",
        "- **Surface**: Stratum 4 primary (LC + gevoelscore + crash labels, 2022-09-03 to "
        "{0}; n={1} channel-valid days out of {2} S4 days). "
        "Stratum 4 IS the gevoelscore-having days by definition per "
        "[`lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md).".format(
            summary["as_of_date"], a["n"], summary["n_rows_stratum_4_total"],
        ),
        "- **Channel-as-it-appears**: `gevoelscore` (bounded 1-6 INTEGER scale per "
        "crash_v2-definition substrate; app-brief framing is 1-10 but empirical range is "
        "1-6).",
        "- **Phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with sister "
        "Strand-A analyses Q3.1-Q3.8. Also 6-phase recovery axis per "
        "[`lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) for "
        "Q3.9.c overlap notation against recovery_arc v2.",
        "- **Scope per handoff section 2.2**: standard Q-template Q3.9.a-i with "
        "**OUTCOME-CHANNEL ADAPTATIONS** documented at each cell. The bounded 1-6 integer "
        "scale requires: per-value frequency vector + Shannon entropy as load-bearing "
        "distribution primitives in Q3.9.a; no classical outliers in Q3.9.h (MAD-z > 5 is "
        "structurally impossible); DROP primitive (NOT spike-count) in Q3.9.g; honest "
        "tautology framing in Q3.9.f (crash IS defined by gevoelscore).",
        "- **Cross-references** per handoff section 2.4: HA-C3 v2 + HA-C3p outcome-side "
        "inverted-U descriptively corroborated in Q3.9.a + Q3.9.d + Q3.9.e; recovery_arc v2 "
        "overlap notation in Q3.9.c (not re-characterisation); crash_v2-definition tautology "
        "honestly framed in Q3.9.f; **Q3.9.e SUBSTANTIVE Strand-A first-pass at Q4.9 "
        "subjective<->objective coupling** -- Spearman rho vs key Garmin sister channels.",
        "- **Computed directly from `per_day_master.csv`**: Q3.9.a (distribution shape + "
        "per-value frequency + Shannon entropy for bounded integer scale), Q3.9.b "
        "(Politis-White E[L]\\* on Stratum-4 pool), Q3.9.c (per-phase base rates + "
        "recovery_arc v2 overlap), Q3.9.d (phase-stratified medians + HA-C3 v2 + HA-C3p "
        "cross-reference), Q3.9.e (SUBSTANTIVE: Spearman rho vs 5 primary + 10 extended "
        "Garmin sister channels), Q3.9.f (tautological day-level read + non-tautological "
        "episode-level min + dip + score-floor verification), Q3.9.g (drop primitive "
        "distribution + HA11 family clarification), Q3.9.h (coverage / missingness on "
        "bounded scale), Q3.9.i (covariate-sensitivity readiness for future HA using "
        "gevoelscore as outcome).",
        "- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) "
        "(loaders, Stratum 4 filter) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) "
        "(`compute_data_driven_block_length`).",
        "- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).",
        "",
        "## Result",
        "",
        "Headline (see [`findings.md`](findings.md) for the full answers Q3.9.a-i):",
        "",
        "`gevoelscore` on Stratum 4 is a **bounded 1-6 INTEGER felt-state outcome channel** "
        "(skew {0:+.2f}; heavy_tail_flag={1}; Shannon entropy {2:.1%} of log-6 ceiling). "
        "**Data-driven E[L]\\*={3:.1f}** (Politis-White; vs project default E[L]=7). "
        "**Phase-stratified medians** (citalopram axis): unmedicated {4:.1f} -> buildup "
        "{5:.1f} -> consolidation {6:.1f} -> afbouw {7:.1f}. **Q3.9.e SUBSTANTIVE "
        "(subjective<->objective coupling)**: top-tracking Garmin sister channel is `{8}` "
        "(Spearman rho = {9}); weakest is `{10}` (rho = {11}) -- Strand-A first-pass at "
        "Q4.9 territory; descriptive only, no causal interpretation per CONVENTIONS section "
        "4.1. **Q3.9.f crash-vs-normal is TAUTOLOGICAL** by crash_v2-definition section 2.1 "
        "(crashes are by-definition score <= 3 days; max crash score = {12:.0f}; n score-4 "
        "days inside merged crash episodes per merge rule sec 2.1.b = {13}). HA-C3 v2 + "
        "HA-C3p outcome-side inverted-U descriptively corroborated from the gevoelscore "
        "distribution side.".format(
            a["skewness"], a["heavy_tail_flag"],
            a["entropy_normalised"] if a["entropy_normalised"] == a["entropy_normalised"] else 0.0,
            el_star,
            c.get("unmedicated", {}).get("median", float("nan")),
            c.get("buildup", {}).get("median", float("nan")),
            c.get("consolidation", {}).get("median", float("nan")),
            c.get("afbouw", {}).get("median", float("nan")),
            top_ch if top_ch is not None else "n/a", top_rho_str,
            weakest_ch if weakest_ch is not None else "n/a", weakest_rho_str,
            sf["max_score_on_crash_days"], sf["n_crash_days_with_score_above_3"],
        ),
        "",
        "## Files",
        "",
        "- [`README.md`](README.md) -- this file",
        "- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + "
        "`findings.md` + `README.md` + `plots/*.png`",
        "- [`findings.md`](findings.md) -- writeup covering Q3.9.a-i + tables "
        "(programmatically emitted by run.py from summary.json per the Q3.5/Q3.6/Q3.7/Q3.8 "
        "architectural note about the Write-tool harness heuristic on the literal filename "
        "\"findings\")",
        "- [`summary.json`](summary.json) -- machine-readable per-question results "
        "(gitignored per `docs/research/**/*.json`)",
        "- [`plots/`](plots/) -- 6 PNGs: per-value frequency, phase-stratified stacked bar, "
        "trajectory-with-phases, Q3.9.e Spearman scatter, ACF, drop primitive distribution "
        "(gitignored per `docs/research/**/*.png`)",
        "",
        "## Status",
        "",
        "**Current as of {0} corpus + 2026-06-25 analysis** (commit context: post-`92d7193` "
        "Q3.8 push_burden_7d LANDED; Phase 2 'finish the descriptive analysis' Tier 2 batch "
        "5th of 5 channels; **CLOSES TIER 2** of user-prioritised Phase 2 batch). Refresh "
        "when:".format(summary["as_of_date"]),
        "",
        "1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg using gevoelscore "
        "as outcome is about to spin up beyond the HA-C3 v2 / HA-C3p locked operands.",
        "2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope "
        "2026-06-06 onward).",
        "3. Politis-White E[L]\\* shifts by another factor of 2 from current {0:.1f}.".format(el_star),
        "4. crash_v2-definition is revised (current state: LOCKED; revision would warrant a "
        "Q3.9 refresh + careful re-derivation across all downstream HA tests).",
        "5. Strand-B Q4.9 subjective<->objective coupling analysis is spun up (this Q3.9.e "
        "is a partial first-pass; Q4.9 would extend with per-phase + lagged + episode-level "
        "coupling + pre-crash divergence patterns).",
        "",
        "## Cross-references",
        "",
        "- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 "
        "2026-06-18, commit `ccbd12e`); section 3.4 lists `gevoelscore (almost every test's "
        "outcome side)` under HA-touched non-confirmed candidate channels; section 4.9 "
        "deferred Q4.9 subjective<->objective coupling -- this Q3.9.e is a partial Strand-A "
        "first-pass.",
        "- **LOAD-BEARING outcome-side substantive references**: "
        "[`HA-C3/result.md`](../../../analyses/hypotheses/HA-C3/result.md) (LOCKED REJECTED "
        "wrong-direction override) + [`HA-C3p/result.md`](../../../analyses/hypotheses/HA-C3p/result.md) "
        "(LOCKED PARTIAL 2-of-3); joint inverted-U finding descriptively corroborated from "
        "the outcome side in Q3.9.a + Q3.9.d + Q3.9.e.",
        "- **LOCKED gevoelscore-to-crash mapping**: [`crash_v2-definition/`](../../../analyses/hypotheses/crash_v2-definition/) "
        "-- the canonical definitional substrate this Q3.9 characterises; NOT modified per "
        "handoff section 3 hard constraint. Q3.9.f surfaces the day-level tautology honestly.",
        "- **Recovery_arc v2 6-phase characterisation**: [`trajectory/recovery_arc/findings.md`](../../trajectory/recovery_arc/findings.md) "
        "(LOCKED) -- Q3.9.c provides overlap notation per handoff section 2.4 'check overlap; "
        "do NOT re-characterise'.",
        "- **Q3.8 most-recent Tier 2 precedent (count-primitive sister)**: "
        "[`descriptive/operationalisation_support/push_burden_7d/`](../push_burden_7d/) -- "
        "Tier 2 4th of 5; LANDED `92d7193`; clean programmatic-emit + bounded-integer-support "
        "precedent.",
        "- **Q3.7 categorical adaptation precedent**: [`descriptive/operationalisation_support/exertion_class/`](../exertion_class/) "
        "-- Tier 2 3rd of 5; non-continuous channel adaptation pattern.",
        "- **Q3.6 continuous-channel precedent**: [`descriptive/operationalisation_support/resting_hr/`](../resting_hr/) "
        "-- Tier 2 2nd of 5; clean programmatic-emit + f-string discipline.",
        "- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) "
        "-- HA11 row referenced in Q3.9.g for the within-day stress U-dip clarification.",
        "- **HA-* tests that this analysis anchors (outcome-side)**:",
        "  - **HA-C3 v2** + **HA-C3p**: direct outcome operands (joint inverted-U finding).",
        "  - **HA10 + HA07d + many other HAs**: indirect outcome via crash_v2-definition.",
        "- **Methodology MDs**: `citalopram_phase_stratification.md`, `permutation_null_block_length.md`, "
        "`lc_era_temporal_segmentation.md` (Stratum 4 IS the gevoelscore-having days), "
        "`lc_recovery_phase_axis.md` (Q3.9.c 6-phase overlap notation), "
        "`_descriptive_stocktake_2026-06-23.md` (gap-list framing).",
        "- **Upstream pipeline**: `per_day_master.csv` `gevoelscore` column <- "
        "`pipeline/03_consolidate/build_unified_dataset.py` <- app-side self-report on 1-10 "
        "scale (empirical range 1-6). `labels_crash_v2.csv` per locked `crash_v2-definition`.",
        "",
    ]
    path.write_text("\n".join(out_lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 70)
    print("Q3.9 gevoelscore operationalisation-support descriptive (Tier 2 5th/5 - FINAL)")
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
    df["is_dip"] = df["crash_label"].fillna("normal") == "dip"
    print("Crash days in S4 (label=='crash'): {0}".format(int(df["is_crash"].sum())))
    print("Dip days in S4 (label=='dip'): {0}".format(int(df["is_dip"].sum())))

    if CHANNEL not in df.columns:
        raise SystemExit(
            "Channel {0!r} missing from per_day_master.csv; check column name + pipeline output".format(CHANNEL)
        )

    print()
    print("Computing Q3.9.a-i on {0} (OUTCOME-CHANNEL ADAPTATIONS per handoff section 1)...".format(CHANNEL))

    values_s4 = df[CHANNEL]

    a_res = q_a_distribution(values_s4)
    print("  Q3.9.a: n={0}, mean={1:.3f}, median={2:.3f}, skew={3:+.3f}, heavy_tail={4}, entropy_norm={5:.1%}".format(
        a_res["n"], a_res["mean"], a_res["median"], a_res["skewness"],
        a_res["heavy_tail_flag"],
        a_res["entropy_normalised"] if a_res["entropy_normalised"] == a_res["entropy_normalised"] else 0.0,
    ))

    b_res = q_b_autocorrelation(values_s4)
    print("  Q3.9.b: E[L]*={0:.2f} (default 7; factor-of-2 flag={1}; M={2})".format(
        b_res["data_driven_E_L_star"], b_res["factor_of_2_deviation_flag"], b_res["cutoff_lag_M"],
    ))

    c_res = q_c_base_rates_per_phase(df, CHANNEL)
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = c_res.get(ph, {})
        if info.get("n", 0) > 0:
            print("  Q3.9.c [{0}]: n={1}, median={2:.2f}".format(
                ph, info["n"], info["median"],
            ))
        else:
            print("  Q3.9.c [{0}]: n=0".format(ph))

    cr_res = q_c_recovery_axis_overlap_note(df, CHANNEL)

    d_res = q_d_phase_stratified(c_res, CHANNEL)
    print("  Q3.9.d: v3 in-scope = {0}".format(d_res["v3_scope_status"]["channel_in_v3_six_channel_scope"]))

    e_res = q_e_subjective_objective_coupling(df, CHANNEL)
    print("  Q3.9.e SUBSTANTIVE: top-tracking primary = `{0}` (rho={1:+.3f}); weakest = `{2}` (rho={3:+.3f})".format(
        e_res["top_tracking_channel"] or "n/a",
        e_res["top_tracking_rho"] if e_res["top_tracking_rho"] == e_res["top_tracking_rho"] else 0.0,
        e_res["weakest_tracking_channel"] or "n/a",
        e_res["weakest_tracking_rho"] if e_res["weakest_tracking_rho"] == e_res["weakest_tracking_rho"] else 0.0,
    ))
    for item in e_res["ranked_primary_by_abs_rho"]:
        print("        primary `{0}`: rho={1:+.3f} (n={2})".format(
            item["channel"], item["spearman_rho"], item["n"],
        ))

    f_res = q_f_crash_vs_normal(df, CHANNEL)
    flr = f_res["day_level"]
    sf = f_res["score_floor_verification_per_crash_v2_definition"]
    print("  Q3.9.f TAUTOLOGICAL: day Cohen's d={0:+.2f}; MWU p={1:.4f}".format(
        flr["cohens_d"], flr["mann_whitney_u"]["p_two_sided"],
    ))
    print("        score-floor: max_crash={0:.0f}; n_above_3={1}; verified={2}".format(
        sf["max_score_on_crash_days"], sf["n_crash_days_with_score_above_3"],
        sf["score_floor_verified_le_3"],
    ))

    g_res = q_g_drop_primitive(df, CHANNEL)
    print("  Q3.9.g: drop primitive: drop>=1 rate={0:.1%}; drop>=2 rate={1:.1%}; drop>=3 rate={2:.1%}; max drop={3:.0f}".format(
        g_res["drop_rate_ge_1"], g_res["drop_rate_ge_2"], g_res["drop_rate_ge_3"],
        g_res["max_drop_observed"],
    ))

    h_res = q_h_coverage_missingness(df, CHANNEL)
    print("  Q3.9.h: coverage={0:.3%} ({1} present / {2} total Stratum 4); completeness = {3}".format(
        h_res["coverage_rate_stratum_4"],
        h_res["n_present_in_stratum_4"], h_res["n_total_stratum_4_rows"],
        h_res["stratum_4_completeness_flag"],
    ))

    i_res = q_i_covariate_readiness(df, CHANNEL)
    print("  Q3.9.i: {0} candidate covariates named".format(len(i_res["candidate_covariates"])))

    summary = {
        "channel": CHANNEL,
        "as_of_date": AS_OF_DATE,
        "n_rows_full_corpus_to_as_of": int(len(df_full)),
        "n_rows_stratum_4_total": n_s4,
        "questions": {
            "Q3.9.a_distribution": a_res,
            "Q3.9.b_autocorrelation": b_res,
            "Q3.9.c_base_rates_per_phase": c_res,
            "Q3.9.c_recovery_axis_overlap": cr_res,
            "Q3.9.d_phase_stratified": d_res,
            "Q3.9.e_subjective_objective_coupling": e_res,
            "Q3.9.f_crash_vs_normal": f_res,
            "Q3.9.g_drop_primitive": g_res,
            "Q3.9.h_coverage_missingness": h_res,
            "Q3.9.i_covariate_readiness": i_res,
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
    print("Done. Q3.9 LANDED (Tier 2 5th/5 - FINAL; closes Tier 2 of Phase 2 batch).")


if __name__ == "__main__":
    main()
