"""Descriptive analysis: exertion_class operationalisation support.

Answers Q3.7.a-i per the locked descriptive programme:
``docs/research/analyses/descriptive/README.md`` section 3.4 (template
a-i applied to this channel; HA-touched non-confirmed candidate list
bullet "exertion_class + push_burden_7d (HA01b/HA01c primaries) --
partially covered by activity-labels/"). **3rd of the 5 Tier 2
channels** in the user-prioritised Phase 2 sequential batch (Tier 1
closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain `7d49ba4`; Tier
2 2nd = Q3.6 resting_hr `5d28219`; this Q3.7 closes Tier 2 3rd; then
Q3.8 push_burden_7d, Q3.9 gevoelscore).

Channel: per-day categorical exertion class derived from steps +
moderate-VPA + Garmin activity-labels per
``analyses/garmin_exploration/activity-labels/definition.md``;
5-level ordinal {none, light, moderate, heavy, very_heavy}.

Channel substantive status (per handoff section 1):
- HA01b-recomputed (v3.2 lagged) primary operand: REFUTED both eras
  (train +5.8 pp / validate +4.0 pp); R14 single-pool +5.1 pp [-14.7,
  +13.3] perm p (E[L]=7) = 0.3689 NOT-SUPPORTED CONVERGE (both
  NOT-SUPPORTED). The original v3.1 rolling-baseline validate +17.3
  pp "first SUPPORTED" headline was a baseline-construction artefact
  (REJECTED.md HA01b-recomputed row). v3.1 -> v3.2 lagged-baseline
  correction is the canonical project example of why lagged-baseline
  matters per CONVENTIONS section 3.2.
- HA01b-per-axis-diagnostic: SUPPORTED both eras at locked tau=0.75
  per cell; load-bearing WITHHELD due to v2 threshold-monotonicity-
  diagnostic AMBIGUOUS.
- HA01c-effective-exertion-shock primary operand: SUPPORTED both
  eras at locked tau=0.75 (train +21.3 / validate +19.5); also
  load-bearing WITHHELD per the same v2 diagnostic ambiguity
  (REJECTED.md HA01c row).
- HA-C4c heavy-T classifier substrate: HA-C4c uses
  `exertion_class_lagged_lcera in {heavy, very_heavy}` on T as the
  heavy-T classifier; the un-lagged primary `exertion_class` (this
  Q3.7 scope) is the underlying raw signal.

**CATEGORICAL ADAPTATIONS** of the Q-template (vs continuous-channel
template stress_mean_sleep + count-primitive template
stress_low_motion):

- Q3.7.a: per-category frequencies + marginal Shannon entropy
  (instead of mean/median/skewness); ordinal-encoded mean/median
  reported for downstream-utility but the distribution-shape
  primitive IS the per-category frequency vector.
- Q3.7.b: autocorrelation on ordinal encoding {none:0, light:1,
  moderate:2, heavy:3, very_heavy:4} (Politis-White E[L]* on the
  encoded series); transition-rate analysis (P(state_t != state_{t-1}))
  reported alongside.
- Q3.7.c: per-citalopram-phase frequency distribution + per-phase
  marginal entropy.
- Q3.7.d: per-phase frequency shifts + chi-square test of
  independence across phases (descriptive read of whether the
  categorical distribution shifts across the citalopram axis).
- Q3.7.e: rank-correlation (Spearman on ordinal encoding) with
  sibling activity-axis primitives; near-identity check at
  |rho|>=0.92 against eff_exertion_rank_lagged + composite +
  push_burden_7d + step_z_30d as the candidate activity-axis
  neighbours; v3.1 vs v3.2 lagged variants noted but NOT folded into
  scope per handoff section 1 ("focus this Strand-A analysis on the
  un-lagged primary").
- Q3.7.f: chi-square 2x5 (crash vs normal x 5 categories) AND
  Mann-Whitney U on ordinal encoding (per handoff section 1
  "chi-square or Mann-Whitney U on ordinal encoding for crash-vs-
  normal").
- Q3.7.g: spike-form = HEAVY/VERY_HEAVY burst frequency (fraction
  of days at heavy or very_heavy + within-7d burst-rate); HA-C4c
  heavy-T classifier framing cited descriptively.
- Q3.7.h: outlier semantics differ for categorical -- no MAD-z;
  rare-class flag (very_heavy fraction) + per-month rare-class
  rate-drift snapshots; activity-labels partial-coverage descriptive
  cross-reference.
- Q3.7.i: covariate-sensitivity readiness for future HA pre-regs.

Output: ``summary.json`` (machine-readable per-question results) +
``plots/*.png`` (visualisations) + ``findings.md`` + ``README.md``
(programmatically emitted from this script per the Q3.2/Q3.3/Q3.4/
Q3.5/Q3.6 precedent session's architectural note about the Write-
tool harness heuristic on the literal filename "findings").

Discipline guards (per CONVENTIONS):
- section 2.1 descriptive-before-inference: no causal claims; no
  falsification bar; no HA verdict promotion (HA01b-recomputed +
  HA01b-per-axis-diagnostic + HA01c + HA-C4c locked verdicts NOT
  extended here).
- section 3.1 personal baseline: distribution shape (per-category
  frequencies) reported as-is; phase-stratified to surface citalopram
  threshold confound where observable.
- section 3.2 lagged-baseline discipline: v3.1 -> v3.2 lagged-baseline
  correction is the canonical project example; this Q3.7.b
  autocorrelation discussion cites it descriptively (per handoff
  section 2.4); does NOT re-litigate.
- section 3.3 column-duplication: near-identity check at |rho|>=0.92.
- section 3.4 crash-drop sensitivity: |Delta|>0.10 flag surfaced.
- section 3.5 spike metrics: heavy/very_heavy burst frequency IS the
  spike-form on this categorical channel per Q3.7.g; HA-C4c heavy-T
  classifier `exertion_class_lagged_lcera in {heavy, very_heavy}` is
  the substantive consumer of this spike-form on the lagged variant.
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
from math import erf, sqrt, log

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
# HERE = .../analyses/descriptive/operationalisation_support/exertion_class
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


CHANNEL = "exertion_class"
AS_OF_DATE = "2026-06-05"  # parity with R14 + Q3.1-Q3.6 prior Strand-A analyses

# Ordinal encoding per activity-labels definition.md
CATEGORY_ORDER = ["none", "light", "moderate", "heavy", "very_heavy"]
CATEGORY_TO_ORDINAL = {c: i for i, c in enumerate(CATEGORY_ORDER)}

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


def encode_ordinal(series: pd.Series) -> pd.Series:
    """Map categorical labels to ordinal integers per CATEGORY_TO_ORDINAL."""
    return series.map(CATEGORY_TO_ORDINAL)


# ---------------------------------------------------------------------------
# Q3.7.a Distribution shape -- CATEGORICAL ADAPTATION
# ---------------------------------------------------------------------------


def shannon_entropy(probs: list) -> float:
    """Shannon entropy in nats (natural log). Returns 0 for empty / single-class."""
    h = 0.0
    for p in probs:
        if p > 0:
            h -= p * log(p)
    return h


def q_a_distribution(values: pd.Series) -> dict:
    """Distribution shape on Stratum 4 (Q3.7.a) -- CATEGORICAL ADAPTATION.

    The distribution-shape primitive IS the per-category frequency vector;
    ordinal-encoded median/mean reported as auxiliary summaries (the channel
    has a natural ordering none < light < moderate < heavy < very_heavy).
    """
    v = values.dropna().astype(str)
    n = int(len(v))
    counts = v.value_counts()
    # Ensure all 5 categories appear in output even if frequency is 0
    per_category_n = {c: int(counts.get(c, 0)) for c in CATEGORY_ORDER}
    per_category_freq = {c: per_category_n[c] / n if n > 0 else float("nan")
                         for c in CATEGORY_ORDER}
    probs = [per_category_freq[c] for c in CATEGORY_ORDER]
    entropy_nats = shannon_entropy(probs)
    entropy_max = log(5)  # max entropy = log(k) for k uniform classes
    entropy_normalised = entropy_nats / entropy_max if entropy_max > 0 else float("nan")

    # Ordinal-encoded mean / median for downstream utility
    ord_v = encode_ordinal(v).astype(float)
    ord_mean = float(ord_v.mean()) if n > 0 else float("nan")
    ord_median = float(ord_v.median()) if n > 0 else float("nan")
    ord_mode = max(per_category_n, key=per_category_n.get) if n > 0 else None

    # Heavy/very_heavy combined fraction = the spike-class fraction
    heavy_plus_fraction = (per_category_n["heavy"] + per_category_n["very_heavy"]) / n if n > 0 else float("nan")
    # None fraction = the at-rest fraction
    none_fraction = per_category_n["none"] / n if n > 0 else float("nan")
    # Rare-class flag per CATEGORICAL adaptation (no heavy-tail-MAD applicable)
    rare_class_flag = bool(min(per_category_freq.values()) < 0.05)
    return {
        "n": n,
        "per_category_n": per_category_n,
        "per_category_frequency": per_category_freq,
        "shannon_entropy_nats": entropy_nats,
        "shannon_entropy_max_log_k": entropy_max,
        "entropy_normalised": entropy_normalised,
        "ordinal_encoding": CATEGORY_TO_ORDINAL,
        "ordinal_mean": ord_mean,
        "ordinal_median": ord_median,
        "ordinal_mode_label": ord_mode,
        "heavy_or_very_heavy_fraction": heavy_plus_fraction,
        "none_fraction": none_fraction,
        "rare_class_flag_min_freq_lt_0p05": rare_class_flag,
        "min_category_frequency": min(per_category_freq.values()) if per_category_freq else float("nan"),
        "max_category_frequency": max(per_category_freq.values()) if per_category_freq else float("nan"),
        "categorical_adaptation_note": (
            "Per handoff section 1 + CATEGORICAL ADAPTATION: distribution-"
            "shape primitive IS the per-category frequency vector + marginal "
            "Shannon entropy (instead of mean/median/skewness applicable to "
            "continuous channels). Ordinal-encoded mean/median reported as "
            "auxiliary summaries (the channel has natural ordering none < "
            "light < moderate < heavy < very_heavy)."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.7.b Autocorrelation -- CATEGORICAL ADAPTATION via ordinal encoding +
# transition rate; descriptive citation of v3.1 -> v3.2 lagged-baseline
# correction per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed
# ---------------------------------------------------------------------------


def q_b_autocorrelation(values: pd.Series) -> dict:
    """Autocorrelation + Politis-White E[L]* on ordinal-encoded channel
    (Q3.7.b) -- CATEGORICAL ADAPTATION.

    Per handoff section 1 + section 2.4: ordinal encoding (none=0, ...,
    very_heavy=4) used for the Politis-White block-length estimator;
    transition-rate (P(state_t != state_{t-1})) reported alongside as the
    additional categorical autocorrelation primitive. v3.1 -> v3.2 lagged-
    baseline correction descriptively cited per CONVENTIONS section 3.2
    + REJECTED.md HA01b-recomputed canonical example (do NOT re-litigate;
    descriptive citation only).
    """
    v = values.dropna().astype(str)
    ord_v = encode_ordinal(v).astype(float)
    arr = ord_v.to_numpy()
    result = compute_data_driven_block_length(arr, default_block_length=7)
    acf = result["autocorrelations"]
    lags_of_interest = {}
    for k in (1, 2, 3, 7, 14, 28):
        if len(acf) > k:
            lags_of_interest["acf_lag{0}".format(k)] = float(acf[k])
    n_arr = len(arr)
    politis_white_threshold = float(2.0 * np.sqrt(np.log(n_arr) / n_arr))

    # Transition-rate analysis: probability that today's class differs
    # from yesterday's (categorical autocorrelation primitive)
    raw_labels = v.to_numpy()
    transitions = int((raw_labels[1:] != raw_labels[:-1]).sum())
    n_pairs = int(len(raw_labels) - 1)
    transition_rate = transitions / n_pairs if n_pairs > 0 else float("nan")

    # Same-class persistence: P(state_t == state_{t-1})
    persistence_rate = 1.0 - transition_rate if n_pairs > 0 else float("nan")

    # Per-category persistence (P(state_t == c | state_{t-1} == c))
    per_class_persistence = {}
    for c in CATEGORY_ORDER:
        prev_is_c = raw_labels[:-1] == c
        n_prev = int(prev_is_c.sum())
        if n_prev == 0:
            per_class_persistence[c] = {"n_prev_day_in_class": 0, "next_day_same_class_rate": float("nan")}
            continue
        same_next = int((raw_labels[1:][prev_is_c] == c).sum())
        per_class_persistence[c] = {
            "n_prev_day_in_class": n_prev,
            "next_day_same_class_count": same_next,
            "next_day_same_class_rate": same_next / n_prev,
        }

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
        "transition_rate_day_over_day": transition_rate,
        "persistence_rate_day_over_day": persistence_rate,
        "n_day_pairs": n_pairs,
        "n_transitions": transitions,
        "per_class_persistence": per_class_persistence,
        "v3_1_to_v3_2_lagged_baseline_correction_xref": (
            "Descriptive citation per CONVENTIONS section 3.2 + REJECTED.md "
            "HA01b-recomputed canonical example: v3.1 exertion_class uses a "
            "30-day TRAILING rolling baseline that includes the candidate day "
            "itself; in sustained-push periods the baseline creeps up with "
            "the pushes and rebases into its own reference frame. v3.2 fixes "
            "this with a [d-90, d-30] lagged window. Original HA01b validate "
            "+17.3 pp 'first SUPPORTED' headline was a v3.1 rolling-baseline "
            "artefact; HA01b-recomputed (v3.2 lagged) showed REFUTED both "
            "eras (train +5.8 / validate +4.0; delta vs original validate = "
            "-13.3 pp). This Q3.7.b autocorrelation analysis is on the un-"
            "lagged primary `exertion_class` (NOT on the rolling-baseline-"
            "computed pre-classifier signal); the autocorrelation observed "
            "here characterises the raw categorical day-to-day class signal."
        ),
        "categorical_adaptation_note": (
            "Per handoff section 1 + CATEGORICAL ADAPTATION: ACF computed "
            "on ordinal-encoded series (none=0 ... very_heavy=4); transition-"
            "rate (P(state_t != state_{t-1})) reported alongside as the "
            "categorical autocorrelation primitive distinct from the "
            "ordinal-encoded ACF (which leverages the ordering)."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.7.c Base rates per citalopram phase -- CATEGORICAL ADAPTATION:
# per-phase per-category frequency distribution + per-phase entropy
# ---------------------------------------------------------------------------


def q_c_base_rates_per_phase(df: pd.DataFrame, channel: str) -> dict:
    """Per-phase per-category n + frequency + entropy (Q3.7.c) --
    CATEGORICAL ADAPTATION.
    """
    out = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))
        sub = df.loc[mask, channel].dropna().astype(str)
        n = int(len(sub))
        if n == 0:
            out[phase_name] = {"n": 0}
            continue
        counts = sub.value_counts()
        per_category_n = {c: int(counts.get(c, 0)) for c in CATEGORY_ORDER}
        per_category_freq = {c: per_category_n[c] / n for c in CATEGORY_ORDER}
        probs = [per_category_freq[c] for c in CATEGORY_ORDER]
        ent = shannon_entropy(probs)
        ord_v = encode_ordinal(sub).astype(float)
        out[phase_name] = {
            "n": n,
            "date_start": str(start),
            "date_end": str(end),
            "per_category_n": per_category_n,
            "per_category_frequency": per_category_freq,
            "shannon_entropy_nats": ent,
            "entropy_normalised": ent / log(5),
            "ordinal_mean": float(ord_v.mean()),
            "ordinal_median": float(ord_v.median()),
            "heavy_or_very_heavy_fraction": (
                per_category_n["heavy"] + per_category_n["very_heavy"]
            ) / n,
            "none_fraction": per_category_n["none"] / n,
        }
    return out


# ---------------------------------------------------------------------------
# Q3.7.d Phase-stratified distribution + chi-square test of independence
# ---------------------------------------------------------------------------


def _chi_square_independence(table: np.ndarray) -> dict:
    """Chi-square test of independence on a contingency table.

    Vendored to avoid scipy. Returns chi2, df, p-value (chi-square
    survival via Wilson-Hilferty approximation).
    """
    table = np.asarray(table, dtype=float)
    if table.ndim != 2:
        raise ValueError("Contingency table must be 2D")
    row_sums = table.sum(axis=1, keepdims=True)
    col_sums = table.sum(axis=0, keepdims=True)
    grand_total = float(table.sum())
    if grand_total == 0:
        return {"chi2": float("nan"), "df": 0, "p_value": float("nan")}
    expected = row_sums * col_sums / grand_total
    # Avoid div-by-zero for empty cells
    mask = expected > 0
    chi2 = float(((table[mask] - expected[mask]) ** 2 / expected[mask]).sum())
    df = int((table.shape[0] - 1) * (table.shape[1] - 1))
    # Wilson-Hilferty chi-square -> normal approximation; valid for df >= 1
    if df == 0:
        return {"chi2": chi2, "df": 0, "p_value": float("nan")}
    z = ((chi2 / df) ** (1.0 / 3.0) - (1.0 - 2.0 / (9.0 * df))) / sqrt(2.0 / (9.0 * df))
    # Upper-tail p (since chi2 is one-sided)
    p_upper = 0.5 * (1.0 - erf(z / sqrt(2.0)))
    return {"chi2": chi2, "df": df, "p_value": float(max(0.0, min(1.0, p_upper)))}


def q_d_phase_stratified(per_phase: dict, channel: str) -> dict:
    """Phase-stratified distribution + chi-square test (Q3.7.d) --
    CATEGORICAL ADAPTATION.

    Per handoff section 1 + CONVENTIONS section 4.2: report observed
    per-phase frequency shifts descriptively; chi-square test of
    independence reports whether the categorical distribution differs
    across the 4 citalopram phases at all. No verdict promotion; no
    a-priori claim; the chi-square p is a descriptive nominal-null
    indicator only.
    """
    # Build 4x5 contingency table (phases x categories) using only phases with n>0
    phase_names_present = [p for p in ("unmedicated", "buildup", "consolidation", "afbouw")
                           if per_phase.get(p, {}).get("n", 0) > 0]
    table = np.zeros((len(phase_names_present), 5), dtype=float)
    for i, p in enumerate(phase_names_present):
        for j, c in enumerate(CATEGORY_ORDER):
            table[i, j] = per_phase[p]["per_category_n"][c]

    chi_result = _chi_square_independence(table) if len(phase_names_present) >= 2 else {
        "chi2": float("nan"), "df": 0, "p_value": float("nan"),
    }

    # Pairwise frequency shifts (frequency of each class in each phase pair)
    pair_shifts = {}
    pairs = [
        ("unmedicated", "buildup"),
        ("unmedicated", "consolidation"),
        ("consolidation", "afbouw"),
        ("unmedicated", "afbouw"),
        ("buildup", "consolidation"),
    ]
    for a, b in pairs:
        if a in per_phase and b in per_phase and per_phase[a].get("n", 0) > 0 and per_phase[b].get("n", 0) > 0:
            pair_shifts["{0}_minus_{1}_freq".format(b, a)] = {
                c: per_phase[b]["per_category_frequency"][c] - per_phase[a]["per_category_frequency"][c]
                for c in CATEGORY_ORDER
            }

    # Heavy+very_heavy fraction shifts across phases (the spike-class)
    heavy_frac_by_phase = {p: per_phase[p].get("heavy_or_very_heavy_fraction")
                           for p in phase_names_present}
    # None fraction shifts (the at-rest class)
    none_frac_by_phase = {p: per_phase[p].get("none_fraction")
                          for p in phase_names_present}
    # Ordinal-encoded median shifts
    ord_median_by_phase = {p: per_phase[p].get("ordinal_median")
                           for p in phase_names_present}
    # Per-phase entropy
    ent_by_phase = {p: per_phase[p].get("shannon_entropy_nats")
                    for p in phase_names_present}

    return {
        "phases_with_data": phase_names_present,
        "contingency_table_phases_x_categories": [
            [int(table[i, j]) for j in range(5)] for i in range(len(phase_names_present))
        ],
        "chi_square_test": chi_result,
        "per_phase_heavy_or_very_heavy_fraction": heavy_frac_by_phase,
        "per_phase_none_fraction": none_frac_by_phase,
        "per_phase_ordinal_median": ord_median_by_phase,
        "per_phase_shannon_entropy_nats": ent_by_phase,
        "pairwise_frequency_shifts": pair_shifts,
        "framing": (
            "Per CONVENTIONS section 4.2: observed per-phase categorical "
            "distribution shifts reported descriptively. The chi-square "
            "p-value is a nominal-null indicator only -- the channel is "
            "the un-lagged primary `exertion_class` whose phase shifts may "
            "reflect (i) genuine activity-pattern change, (ii) categorical-"
            "boundary calibration drift on the v3.1 rolling-baseline "
            "definition of the upstream classifier per CONVENTIONS section "
            "3.2, or (iii) co-temporal trajectory effects. The lagged "
            "variants `exertion_class_lagged` + `exertion_class_lagged_lcera` "
            "are out of Strand-A scope per handoff section 1; this Q3.7.d "
            "characterises the un-lagged primary as-is."
        ),
        "categorical_adaptation_note": (
            "Per handoff section 1 + CATEGORICAL ADAPTATION: phase shift "
            "primitive IS per-phase per-category frequency vector + entropy "
            "(instead of mean/median delta as in continuous-channel "
            "templates Q3.1.d ... Q3.6.d). Chi-square test of independence "
            "(4 phases x 5 categories) is the global-null descriptive "
            "indicator; pairwise per-category frequency deltas are the "
            "per-pair descriptive details."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.7.e Near-identity check -- CATEGORICAL ADAPTATION via ordinal encoding
# ---------------------------------------------------------------------------

NEAR_IDENTITY_THRESHOLD = 0.92  # CONVENTIONS section 3.3


def q_e_near_identity(df: pd.DataFrame, channel: str) -> dict:
    """Near-identity check vs sibling activity-axis primitives (Q3.7.e) --
    CATEGORICAL ADAPTATION.

    Per handoff section 1 + CATEGORICAL ADAPTATION: rank-correlation
    (Spearman) on ordinal-encoded primary vs continuous siblings;
    Cramer's V analogue is NOT computed since the candidate companion
    channels are continuous-form derivatives (effective_exertion_min,
    eff_exertion_rank_lagged, etc.). Lagged variants of the channel
    itself (exertion_class_lagged / exertion_class_lagged_lcera) ARE
    checked since they are categorical with the same 5-level ordinal
    encoding -- the relationship between un-lagged and lagged forms is
    methodologically informative for any consumer choosing between them.
    """
    ord_primary = encode_ordinal(df[channel].astype("object")).astype(float)
    df_aug = df.copy()
    df_aug["_ord_primary"] = ord_primary

    # Sibling activity-axis primitives (continuous + categorical-lagged)
    targets = [
        # Same-channel lagged variants (categorical, ordinal-encoded)
        "exertion_class_lagged",
        "exertion_class_lagged_lcera",
        # Continuous activity-axis primitives derived from the same exertion concept
        "effective_exertion_min",
        "eff_exertion_rank_lagged",
        "eff_exertion_rank_lagged_lcera",
        "exertion_rank_composite_lagged",
        "exertion_rank_composite_lagged_lcera",
        "effective_exertion_slope_28d",
        # Other activity-axis siblings per descriptive README section 3.4
        "push_burden_7d",
        # Steps-axis primitive (if present)
        "step_z_30d",
        "steps_total",
        "steps",
        # Moderate-to-vigorous PA primitives (if present)
        "mvpa_minutes",
        "moderate_intensity_minutes",
        "vigorous_intensity_minutes",
    ]
    rows = []
    flags = []
    for t in targets:
        if t not in df_aug.columns:
            rows.append({"channel": t, "note": "column absent"})
            continue
        if t in ("exertion_class_lagged", "exertion_class_lagged_lcera"):
            # Categorical -- encode ordinal and treat as continuous for Spearman
            t_ord = encode_ordinal(df_aug[t].astype("object")).astype(float)
            sub = pd.DataFrame({"_ord_primary": df_aug["_ord_primary"], "_ord_target": t_ord}).dropna()
            if len(sub) < 30:
                rows.append({"channel": t, "n": int(len(sub)), "note": "n<30 - skipped"})
                continue
            pear = float(sub["_ord_primary"].corr(sub["_ord_target"]))
            spear = float(sub["_ord_primary"].corr(sub["_ord_target"], method="spearman"))
        else:
            sub = df_aug[["_ord_primary", t]].dropna()
            if len(sub) < 30:
                rows.append({"channel": t, "n": int(len(sub)), "note": "n<30 - skipped"})
                continue
            pear = float(sub["_ord_primary"].corr(sub[t]))
            spear = float(sub["_ord_primary"].corr(sub[t], method="spearman"))
        flagged = max(abs(pear), abs(spear)) >= NEAR_IDENTITY_THRESHOLD
        rows.append({
            "channel": t,
            "n": int(len(sub)),
            "pearson_r": pear,
            "spearman_rho": spear,
            "near_identity_flag": flagged,
            "is_categorical_sibling": t in ("exertion_class_lagged", "exertion_class_lagged_lcera"),
        })
        if flagged:
            flags.append(t)
    return {
        "threshold": NEAR_IDENTITY_THRESHOLD,
        "rows": rows,
        "flagged_pairs": flags,
        "note": (
            "Spearman on ordinal-encoded primary vs continuous-form activity-"
            "axis sibling primitives. The two lagged categorical variants "
            "(exertion_class_lagged + exertion_class_lagged_lcera) are "
            "ordinal-encoded with the same 5-level mapping; expected high "
            "rho with the un-lagged primary by construction since they "
            "share the underlying classifier with shifted baseline windows. "
            "Per CONVENTIONS section 3.3: the threshold is |rho|>=0.92. "
            "Per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed: "
            "downstream PEM-pacing consumers prefer the v3.2 lagged variant; "
            "any near-identity between un-lagged primary and a lagged "
            "variant reflects categorical-classifier overlap, NOT operand "
            "equivalence (the baseline window differs)."
        ),
        "categorical_adaptation_note": (
            "Per handoff section 1 + CATEGORICAL ADAPTATION: Spearman on "
            "ordinal encoding {none:0, light:1, moderate:2, heavy:3, "
            "very_heavy:4}; Cramer's V analogue not reported since the "
            "candidate companions are continuous-form (the categorical-vs-"
            "categorical comparison would be the lagged-variant pairs "
            "above; reported as Spearman on ordinal encoding for "
            "comparability with the continuous-form rows)."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.7.f Crash-vs-normal -- CATEGORICAL ADAPTATION: chi-square 2x5 + MWU
# on ordinal encoding + R14 HA01b-recomputed single-pool cross-reference
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
    }


def q_f_crash_vs_normal(df: pd.DataFrame, channel: str, seed: int = 20260624) -> dict:
    """Crash-vs-normal -- CATEGORICAL ADAPTATION (Q3.7.f).

    Per handoff section 1 + section 2.4: chi-square 2x5 (crash x 5
    categories) AND Mann-Whitney U on ordinal encoding (per handoff
    section 1 "chi-square or Mann-Whitney U on ordinal encoding for
    crash-vs-normal"). Both reported for triangulation. R14 HA01b-
    recomputed single-pool +5.1 pp [-14.7, +13.3] perm p=0.3689
    NOT-SUPPORTED + HA01c SUPPORTED-both-eras-load-bearing-WITHHELD
    descriptively cross-referenced.
    """
    sub = df[[channel, "is_crash", "episode_id"]].dropna(subset=[channel, "is_crash"])
    is_crash = sub["is_crash"].astype(bool)
    crash_labels = sub.loc[is_crash, channel].astype(str)
    normal_labels = sub.loc[~is_crash, channel].astype(str)

    n_crash_day = int(len(crash_labels))
    n_normal_day = int(len(normal_labels))

    # Per-category frequency on crash vs normal
    crash_counts = crash_labels.value_counts()
    normal_counts = normal_labels.value_counts()
    crash_per_cat_n = {c: int(crash_counts.get(c, 0)) for c in CATEGORY_ORDER}
    normal_per_cat_n = {c: int(normal_counts.get(c, 0)) for c in CATEGORY_ORDER}
    crash_per_cat_freq = {c: crash_per_cat_n[c] / n_crash_day if n_crash_day > 0 else float("nan")
                          for c in CATEGORY_ORDER}
    normal_per_cat_freq = {c: normal_per_cat_n[c] / n_normal_day if n_normal_day > 0 else float("nan")
                           for c in CATEGORY_ORDER}

    # Chi-square 2x5 (crash row + normal row)
    table = np.array(
        [[crash_per_cat_n[c] for c in CATEGORY_ORDER],
         [normal_per_cat_n[c] for c in CATEGORY_ORDER]], dtype=float,
    )
    chi_result = _chi_square_independence(table)

    # Mann-Whitney U on ordinal encoding
    crash_ord = encode_ordinal(crash_labels).astype(float).to_numpy()
    normal_ord = encode_ordinal(normal_labels).astype(float).to_numpy()
    mwu = _mann_whitney_u(crash_ord, normal_ord) if n_crash_day > 0 and n_normal_day > 0 else {
        "U_crash_first_sample": float("nan"), "z": float("nan"),
        "p_two_sided": float("nan"), "p_crash_greater_than_normal": float("nan"),
    }
    # Median diff on ordinal encoding
    median_diff_ord = float(np.median(crash_ord) - np.median(normal_ord)) if n_crash_day > 0 and n_normal_day > 0 else float("nan")
    mean_diff_ord = float(np.mean(crash_ord) - np.mean(normal_ord)) if n_crash_day > 0 and n_normal_day > 0 else float("nan")

    # Heavy+very_heavy fraction shift (crash - normal)
    heavy_frac_crash = (crash_per_cat_n["heavy"] + crash_per_cat_n["very_heavy"]) / n_crash_day if n_crash_day > 0 else float("nan")
    heavy_frac_normal = (normal_per_cat_n["heavy"] + normal_per_cat_n["very_heavy"]) / n_normal_day if n_normal_day > 0 else float("nan")
    heavy_frac_diff = heavy_frac_crash - heavy_frac_normal if not (np.isnan(heavy_frac_crash) or np.isnan(heavy_frac_normal)) else float("nan")

    # None fraction shift
    none_frac_crash = crash_per_cat_n["none"] / n_crash_day if n_crash_day > 0 else float("nan")
    none_frac_normal = normal_per_cat_n["none"] / n_normal_day if n_normal_day > 0 else float("nan")
    none_frac_diff = none_frac_crash - none_frac_normal if not (np.isnan(none_frac_crash) or np.isnan(none_frac_normal)) else float("nan")

    # Episode-level: per-episode ordinal mean
    ep_mask = sub["episode_id"].notna() & sub["episode_id"].astype(str).str.startswith("crash-")
    ep_df = sub.loc[ep_mask, [channel, "episode_id"]].copy()
    ep_df["_ord"] = encode_ordinal(ep_df[channel].astype("object")).astype(float)
    per_episode_mean = ep_df.groupby("episode_id")["_ord"].mean()
    n_episodes = int(len(per_episode_mean))

    if n_episodes >= 2 and n_normal_day >= 2:
        ep_mean_val = float(per_episode_mean.mean())
        ep_sd = float(per_episode_mean.std(ddof=1)) if n_episodes > 1 else float("nan")
        normal_mean_val = float(normal_ord.mean())
        normal_sd = float(normal_ord.std(ddof=1)) if n_normal_day > 1 else float("nan")
        ep_diff_val = ep_mean_val - normal_mean_val
        pooled_sd = float(np.sqrt(
            ((n_episodes - 1) * ep_sd ** 2 + (n_normal_day - 1) * normal_sd ** 2)
            / (n_episodes + n_normal_day - 2)
        )) if (n_episodes > 1 and n_normal_day > 1) else float("nan")
        cohens_d_ep = ep_diff_val / pooled_sd if pooled_sd and pooled_sd > 0 else float("nan")
        rng = np.random.default_rng(seed)
        ep_arr = per_episode_mean.to_numpy()
        boot_diffs = np.empty(5000)
        for i in range(5000):
            b_ep = rng.choice(ep_arr, size=n_episodes, replace=True)
            b_normal = rng.choice(normal_ord, size=n_normal_day, replace=True)
            boot_diffs[i] = b_ep.mean() - b_normal.mean()
        ci_low = float(np.quantile(boot_diffs, 0.025))
        ci_high = float(np.quantile(boot_diffs, 0.975))
    else:
        ep_mean_val = float("nan")
        ep_diff_val = float("nan")
        cohens_d_ep = float("nan")
        ci_low = float("nan")
        ci_high = float("nan")

    # Crash-drop sensitivity on Spearman vs gevoelscore (ordinal-encoded)
    crash_drop_info = None
    if "gevoelscore" in df.columns:
        d2 = df[[channel, "gevoelscore", "is_crash"]].dropna()
        d2 = d2.copy()
        d2["_ord"] = encode_ordinal(d2[channel].astype("object")).astype(float)
        d2["is_crash"] = d2["is_crash"].astype(bool)
        d2 = d2.dropna(subset=["_ord"])
        if d2["is_crash"].sum() > 1 and (~d2["is_crash"]).sum() > 1:
            def spearman_stat(d):
                return float(d["_ord"].corr(d["gevoelscore"], method="spearman"))
            crash_drop_info = crash_drop_sensitivity(spearman_stat, d2)

    return {
        "day_level": {
            "n_crash_day": n_crash_day,
            "n_normal_day": n_normal_day,
            "crash_per_category_n": crash_per_cat_n,
            "crash_per_category_frequency": crash_per_cat_freq,
            "normal_per_category_n": normal_per_cat_n,
            "normal_per_category_frequency": normal_per_cat_freq,
            "heavy_or_very_heavy_fraction_crash": heavy_frac_crash,
            "heavy_or_very_heavy_fraction_normal": heavy_frac_normal,
            "heavy_or_very_heavy_fraction_diff_crash_minus_normal": heavy_frac_diff,
            "none_fraction_crash": none_frac_crash,
            "none_fraction_normal": none_frac_normal,
            "none_fraction_diff_crash_minus_normal": none_frac_diff,
            "ordinal_mean_diff_crash_minus_normal": mean_diff_ord,
            "ordinal_median_diff_crash_minus_normal": median_diff_ord,
            "chi_square_2x5_test": chi_result,
            "mann_whitney_u_on_ordinal": mwu,
        },
        "episode_level": {
            "n_crash_episodes": n_episodes,
            "n_normal_day_base_rate": n_normal_day,
            "mean_per_episode_ordinal": ep_mean_val,
            "mean_normal_day_ordinal": float(normal_ord.mean()) if n_normal_day > 0 else float("nan"),
            "mean_diff_episode_vs_normal_day_ordinal": ep_diff_val,
            "cohens_d_episode_vs_normal_day_ordinal": cohens_d_ep,
            "bootstrap_ci95_mean_diff_ordinal": [ci_low, ci_high],
            "n_bootstrap": 5000,
            "seed": seed,
        },
        "crash_drop_sensitivity_on_spearman_vs_gevoelscore_ordinal": (
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
        "ha01b_recomputed_ha01c_xref": {
            "ha01b_recomputed_operand": (
                "frac windows with >=1 day in 4-day leadup at exertion_class_"
                "lagged in {heavy, very_heavy} (v3.2 lagged baseline)"
            ),
            "ha01b_recomputed_locked_verdict": "REFUTED both eras (train +5.8 pp / validate +4.0 pp)",
            "ha01b_recomputed_r14_disc_pp": +5.1,
            "ha01b_recomputed_r14_ci95": [-14.7, +13.3],
            "ha01b_recomputed_r14_perm_p": 0.3689,
            "ha01b_recomputed_r14_verdict": "NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED)",
            "ha01c_operand": (
                "Effective-exertion shock at locked tau=0.75 per cell on the "
                "lagged effective-exertion-rank channel (eff_exertion_rank_"
                "lagged); 4-day leadup window."
            ),
            "ha01c_locked_verdict": "SUPPORTED both eras at tau=0.75 (train +21.3 pp / validate +19.5 pp); load-bearing WITHHELD due to v2 threshold-monotonicity-diagnostic AMBIGUOUS",
            "ha01b_per_axis_diag_locked_verdict": "SUPPORTED both eras at locked tau=0.75 per cell; load-bearing WITHHELD due to v2 threshold-monotonicity-diagnostic AMBIGUOUS",
            "v3_1_to_v3_2_correction_descriptive_xref": (
                "Original HA01b validate +17.3 pp 'first SUPPORTED' headline "
                "softened by -13.3 pp on v3.2 lagged-baseline recomputation. "
                "Canonical project example of why lagged-baseline matters "
                "per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed. "
                "Q3.7.b autocorrelation discussion cites descriptively; "
                "Q3.7.f crash-vs-normal descriptively re-anchors at the day "
                "+ episode levels on the un-lagged primary."
            ),
            "ha01b_source": "analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md",
            "ha01c_source": "analyses/hypotheses/HA01c-effective-exertion-shock/result.md",
            "r14_source": "descriptive/operationalisation_support/single_pool_reanchor/findings.md row HA01b-recomputed",
            "rejected_md_source": "docs/research/REJECTED.md HA01b-recomputed row (canonical correction example)",
            "note": (
                "HA01b-recomputed (v3.2 lagged): un-lagged primary + lagged "
                "variant differ in the baseline window of the upstream "
                "classifier per CONVENTIONS section 3.2. This Q3.7.f is on "
                "the un-lagged primary (the underlying raw signal) -- a "
                "first-order day-level descriptive complement to the "
                "lagged-operand HA01b/HA01c tested constructs. The HA01b-"
                "recomputed + HA01c + HA-C4c substantive verdicts are "
                "LOCKED and NOT extended here per CONVENTIONS section 4.2."
            ),
        },
        "categorical_adaptation_note": (
            "Per handoff section 1 + CATEGORICAL ADAPTATION: chi-square 2x5 "
            "(crash x normal x 5 categories) AND Mann-Whitney U on ordinal "
            "encoding both reported; Cohen's d computed on the ordinal "
            "encoding (an approximation -- for ordinal data the standardised "
            "rank-biserial r is also a defensible effect size; Cohen's d "
            "reported for parity with sister continuous Strand-A analyses). "
            "Heavy+very_heavy spike-class fraction shift IS the spike-form "
            "crash-vs-normal primitive on this categorical channel."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.7.g Spike-detecting primitive availability -- CATEGORICAL ADAPTATION:
# heavy/very_heavy burst frequency + HA-C4c heavy-T classifier framing
# ---------------------------------------------------------------------------


def q_g_spike_primitive(df: pd.DataFrame, channel: str) -> dict:
    """Spike-primitive on the categorical channel (Q3.7.g) --
    CATEGORICAL ADAPTATION.

    Per handoff section 1 + section 2.4 + CONVENTIONS section 3.5: the
    spike-form on this categorical channel is heavy/very_heavy burst
    frequency. HA-C4c uses `exertion_class_lagged_lcera in {heavy,
    very_heavy}` on T as the heavy-T classifier on the lagged variant;
    the un-lagged primary (this Q3.7) is the underlying raw signal that
    drives the lagged construct after baseline-window adjustment per
    CONVENTIONS section 3.2.
    """
    sub = df[["date", channel]].dropna().sort_values("date").reset_index(drop=True)
    labels = sub[channel].astype(str).to_numpy()
    n = int(len(labels))

    # Heavy/very_heavy spike days (point primitive)
    is_heavy_spike = np.isin(labels, ["heavy", "very_heavy"])
    n_heavy_spike = int(is_heavy_spike.sum())
    heavy_spike_rate = n_heavy_spike / n if n > 0 else float("nan")

    # Very_heavy alone (the extreme tail)
    is_very_heavy = labels == "very_heavy"
    n_very_heavy = int(is_very_heavy.sum())
    very_heavy_rate = n_very_heavy / n if n > 0 else float("nan")

    # Burst-rate: per 7-day rolling window count of heavy_spike days
    if n > 0:
        rolling_window = 7
        burst_counts = np.array([
            int(is_heavy_spike[max(0, i - rolling_window + 1): i + 1].sum())
            for i in range(n)
        ])
        # Fraction of days where >=2 heavy_spike days occurred in the
        # trailing 7-day window (within-7d burst-form per CONVENTIONS
        # section 3.5)
        burst_rate_ge2 = float((burst_counts >= 2).mean())
        burst_rate_ge3 = float((burst_counts >= 3).mean())
        # Distribution of 7d-window burst counts
        burst_count_dist = {
            str(k): int((burst_counts == k).sum()) for k in range(rolling_window + 1)
        }
    else:
        burst_rate_ge2 = float("nan")
        burst_rate_ge3 = float("nan")
        burst_count_dist = {}

    # Run-length distribution: consecutive runs of heavy_spike days
    run_lengths = []
    i = 0
    while i < n:
        if is_heavy_spike[i]:
            j = i + 1
            while j < n and is_heavy_spike[j]:
                j += 1
            run_lengths.append(j - i)
            i = j
        else:
            i += 1
    run_dist = {
        "n_runs": len(run_lengths),
        "max_run_length_days": int(max(run_lengths)) if run_lengths else 0,
        "median_run_length_days": float(np.median(run_lengths)) if run_lengths else float("nan"),
        "mean_run_length_days": float(np.mean(run_lengths)) if run_lengths else float("nan"),
    }

    # Lagged variant coverage in master
    lagged_in_master = {}
    for c in ("exertion_class_lagged", "exertion_class_lagged_lcera"):
        if c in df.columns:
            n_lag = int(df[c].notna().sum())
            lagged_in_master[c] = {"n_non_nan": n_lag, "n_total": int(len(df))}

    return {
        "channel_resolution": (
            "per-day categorical class derived from steps + moderate-VPA + "
            "Garmin activity-labels per analyses/garmin_exploration/activity-"
            "labels/definition.md; 5-level ordinal {none, light, moderate, "
            "heavy, very_heavy}"
        ),
        "spike_form_definition": (
            "heavy/very_heavy class fraction (binary collapse of the 5-level "
            "ordinal to {0=none/light/moderate, 1=heavy/very_heavy}); the "
            "within-7d burst-rate (>=2 heavy_spike days in trailing 7d "
            "window) is the within-week sustained-exertion primitive"
        ),
        "n_heavy_spike_days": n_heavy_spike,
        "heavy_or_very_heavy_rate": heavy_spike_rate,
        "n_very_heavy_days": n_very_heavy,
        "very_heavy_rate": very_heavy_rate,
        "burst_rate_ge2_in_trailing_7d": burst_rate_ge2,
        "burst_rate_ge3_in_trailing_7d": burst_rate_ge3,
        "burst_count_distribution_per_7d_window": burst_count_dist,
        "consecutive_heavy_run_distribution": run_dist,
        "lagged_variants_in_master": lagged_in_master,
        "ha_c4c_heavy_t_classifier_xref": {
            "classifier": "exertion_class_lagged_lcera in {heavy, very_heavy} on T",
            "source": "analyses/hypotheses/HA-C4c/hypothesis.md section 4.1 + section 4.3",
            "coverage_within_lc_era": "approx 83% per HA-C4c hypothesis.md section 4.4",
            "note": (
                "HA-C4c uses the LAGGED variant (exertion_class_lagged_lcera) "
                "as the heavy-T classifier per CONVENTIONS section 3.2 "
                "lagged-baseline discipline (the v3.2 _lagged_lcera form "
                "uses a [d-90, d-30] window restricted to LC-era days). "
                "The un-lagged primary `exertion_class` (this Q3.7 scope) "
                "is the underlying raw 5-level signal; the lagged variant "
                "applies the lagged-baseline correction per CONVENTIONS "
                "section 3.2 + REJECTED.md HA01b-recomputed canonical "
                "example. Per handoff section 3 hard constraint: HA-C4c "
                "result is LOCKED PARTIAL (just landed `a69a8ed`; cross-"
                "phase pooled with bar (b) failing); this Q3.7.g does NOT "
                "extend or re-anchor HA-C4c."
            ),
        },
        "categorical_adaptation_note": (
            "Per handoff section 1 + CONVENTIONS section 3.5 spike metrics: "
            "the spike-form on a 5-level ordinal channel is the heavy/very_"
            "heavy class fraction (rare-class point primitive) + the within-"
            "7d burst-rate (sustained-exertion primitive). These mirror the "
            "spike-form for count primitives (stress_low_motion_min_count_"
            "S60_Mlow Q3.4.g) and the per-4-day MAX |z| spike-form for "
            "daily-aggregate continuous channels (resting_hr Q3.6.g). Per "
            "CONVENTIONS section 3.5: this categorical spike-form is the "
            "operationalisation substrate for HA-C4c's heavy-T classifier "
            "construct on the lagged variant."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.7.h Outlier detection + calibration drift -- CATEGORICAL ADAPTATION
# ---------------------------------------------------------------------------


def q_h_outliers_calibration(df: pd.DataFrame, channel: str) -> dict:
    """Outliers + calibration-drift -- CATEGORICAL ADAPTATION (Q3.7.h).

    Per handoff section 1: outlier semantics differ for categorical; no
    MAD-z applicable. Rare-class flag (very_heavy fraction) + per-month
    rate-drift snapshots are the categorical equivalents. activity-labels
    partial-coverage descriptive cross-reference per handoff section 2.4.
    """
    sub = df[["date", channel]].dropna().sort_values("date").reset_index(drop=True)
    sub["_label"] = sub[channel].astype(str)
    n = int(len(sub))

    # Per-month rare-class rate snapshots
    sub["_year_month"] = sub["date"].dt.to_period("M")
    monthly = sub.groupby("_year_month")["_label"].apply(
        lambda s: pd.Series({
            "n": int(len(s)),
            "very_heavy_rate": float((s == "very_heavy").mean()),
            "heavy_or_very_heavy_rate": float(((s == "heavy") | (s == "very_heavy")).mean()),
            "none_rate": float((s == "none").mean()),
        })
    ).unstack()
    monthly_records = [
        {
            "year_month": str(idx),
            "n": int(row["n"]),
            "very_heavy_rate": float(row["very_heavy_rate"]),
            "heavy_or_very_heavy_rate": float(row["heavy_or_very_heavy_rate"]),
            "none_rate": float(row["none_rate"]),
        }
        for idx, row in monthly.iterrows()
    ]

    # Coverage check: any days with missing exertion_class in S4?
    n_missing = int(df[channel].isna().sum())
    n_present = int(df[channel].notna().sum())

    # Boundary-step reads: very_heavy_rate + heavy_or_very_heavy_rate
    # pre/post 30d at the 3 citalopram boundaries
    boundary_reads = {}
    for label, step_date_str in (
        ("citalopram_boundary_2024_04_09", "2024-04-09"),
        ("consolidation_boundary_2024_06_20", "2024-06-20"),
        ("afbouw_boundary_2026_03_20", "2026-03-20"),
    ):
        step_date = pd.Timestamp(step_date_str)
        pre = sub.loc[
            (sub["date"] >= step_date - pd.Timedelta(days=30))
            & (sub["date"] < step_date),
            "_label",
        ]
        post = sub.loc[
            (sub["date"] >= step_date)
            & (sub["date"] < step_date + pd.Timedelta(days=30)),
            "_label",
        ]
        if len(pre) > 0 and len(post) > 0:
            pre_heavy_rate = float(((pre == "heavy") | (pre == "very_heavy")).mean())
            post_heavy_rate = float(((post == "heavy") | (post == "very_heavy")).mean())
            pre_none_rate = float((pre == "none").mean())
            post_none_rate = float((post == "none").mean())
            boundary_reads[label] = {
                "n_pre": int(len(pre)),
                "n_post": int(len(post)),
                "heavy_or_very_heavy_rate_pre": pre_heavy_rate,
                "heavy_or_very_heavy_rate_post": post_heavy_rate,
                "heavy_or_very_heavy_rate_diff": post_heavy_rate - pre_heavy_rate,
                "none_rate_pre": pre_none_rate,
                "none_rate_post": post_none_rate,
                "none_rate_diff": post_none_rate - pre_none_rate,
            }

    return {
        "outlier_semantics_note": (
            "Per handoff section 1 + CATEGORICAL ADAPTATION: outlier "
            "semantics differ for categorical channels -- no MAD-z "
            "applicable (the channel is a 5-level ordinal, not a "
            "continuous magnitude). The categorical-equivalent diagnostics "
            "are (i) rare-class flag (any class < 5%) reported in Q3.7.a, "
            "(ii) per-month rate-drift snapshots for the rare-class "
            "(very_heavy) and the spike-class (heavy/very_heavy combined) "
            "reported below, and (iii) boundary-step reads at the "
            "citalopram phase boundaries (where a categorical-classifier "
            "calibration drift would surface as a step change in class "
            "frequencies)."
        ),
        "n_total_s4_rows_with_label": n,
        "n_missing_label_in_input": n_missing,
        "n_present_label_in_input": n_present,
        "monthly_rate_snapshots": monthly_records,
        "boundary_step_reads": boundary_reads,
        "activity_labels_partial_coverage_xref": {
            "source_folder": "docs/research/analyses/garmin_exploration/activity-labels/",
            "scope": (
                "Existing primitive validation + visualisation runs on this "
                "channel family (definition.md severity cutoffs + scripts/ "
                "produced ha_results_4day_lagged.md). Coverage is PARTIAL "
                "per descriptive README section 3.4: existing artefact does "
                "primitive-spec + HA-test validation but does NOT cover "
                "the Q3.x.a-i operationalisation-support per-channel "
                "template. This Q3.7 provides the per-channel substrate "
                "the activity-labels artefact does NOT have."
            ),
            "definition_md_severity_note": (
                "Per activity-labels/definition.md (cited descriptively): "
                "'severity cutoffs for exertion_class are NOT locked' -- "
                "this is the upstream-classifier discipline note. Q3.7.h's "
                "per-month rate-drift snapshots reported below characterise "
                "the categorical-distribution stability across the multi-"
                "year window AS-IS for the v3.1 un-lagged primary; any "
                "calibration-drift signature in the snapshot table is a "
                "Layer 1 descriptive observation, NOT a re-promotion of "
                "the v3.1 cutoff lock."
            ),
            "note": (
                "Per CONVENTIONS section 2.1: Layer 1 descriptive only; "
                "the activity-labels artefact's HA-test validation results "
                "are LOCKED in their own result.md files (HA01b, HA01b-"
                "recomputed, HA02b, HA02c, HA05b) and are NOT extended here."
            ),
        },
        "categorical_adaptation_note": (
            "Per handoff section 1 + CATEGORICAL ADAPTATION: per-month "
            "very_heavy rate + heavy/very_heavy combined rate are the "
            "rare-class and spike-class drift diagnostics; boundary-step "
            "reads characterise step changes in class frequencies at "
            "documented intervention boundaries."
        ),
    }


# ---------------------------------------------------------------------------
# Q3.7.i Covariate-sensitivity readiness
# ---------------------------------------------------------------------------


def q_i_covariate_readiness(df: pd.DataFrame, channel: str) -> dict:
    """Covariate-sensitivity readiness (Q3.7.i).

    Per HA-P7 section 4.5.4 worked-example pattern. Names candidate
    covariates a future HA on exertion_class as predictor could add.
    """
    cands = []

    # 1. The v3.2 lagged variant -- THE covariate to disambiguate v3.1 vs v3.2
    cands.append({
        "covariate": "exertion_class_lagged_lcera (v3.2 lagged variant; LC-era-restricted baseline window)",
        "rationale": (
            "Per CONVENTIONS section 3.2 lagged-baseline discipline + "
            "REJECTED.md HA01b-recomputed canonical example: any future HA "
            "on the un-lagged primary `exertion_class` should pre-spec the "
            "v3.2 lagged variant as a parallel-arm sensitivity check (the "
            "v3.1 -> v3.2 correction was load-bearing on HA01b's original "
            "validate +17.3 pp 'first SUPPORTED' headline that softened to "
            "+4.0 pp). If both arms produce concordant verdicts, the "
            "baseline-construction choice is not load-bearing; divergence "
            "is the load-bearing flag."
        ),
        "source": "CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed + analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md",
        "expected_effect": (
            "Verdict concordance = baseline-construction choice not load-"
            "bearing. Divergence = the lagged baseline is doing real work "
            "and the un-lagged primary is contaminated by rebasing per "
            "CONVENTIONS section 3.2."
        ),
        "needed_columns_in_master": ["exertion_class_lagged_lcera (already in master)"],
    })

    # 2. effective_exertion_min -- the continuous-form sibling
    eff_corr = None
    if "effective_exertion_min" in df.columns:
        ord_v = encode_ordinal(df[channel].astype("object")).astype(float)
        d = pd.DataFrame({"_ord": ord_v, "eff": df["effective_exertion_min"]}).dropna()
        if len(d) > 30:
            eff_corr = {
                "spearman_rho": float(d["_ord"].corr(d["eff"], method="spearman")),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "effective_exertion_min (continuous-form sibling)",
        "rationale": (
            "Per descriptive README section 3.4 + handoff section 1: the "
            "continuous-form sibling effective_exertion_min carries the "
            "pre-discretisation magnitude information that the 5-level "
            "categorical encoding compresses. The covariate disambiguates: "
            "beta_channel attenuates if the categorical encoding is just a "
            "coarsening of the continuous magnitude (the continuous form "
            "carries the signal); beta_channel survives if the categorical "
            "encoding carries discrete-class-boundary information beyond "
            "the continuous form (e.g. the heavy/very_heavy cutoff IS the "
            "operationally relevant boundary)."
        ),
        "source": "DATA_DICTIONARY.md effective_exertion_min + descriptive README section 3.4 HA-touched candidates",
        "observed_spearman_on_S4": eff_corr,
        "expected_effect": (
            "beta_channel attenuates if continuous form dominates; beta_"
            "channel survives if the discrete heavy/very_heavy cutoff "
            "carries operationally distinct information"
        ),
    })

    # 3. push_burden_7d -- the sustained-exertion sibling
    pb_corr = None
    if "push_burden_7d" in df.columns:
        ord_v = encode_ordinal(df[channel].astype("object")).astype(float)
        d = pd.DataFrame({"_ord": ord_v, "pb": df["push_burden_7d"]}).dropna()
        if len(d) > 30:
            pb_corr = {
                "spearman_rho": float(d["_ord"].corr(d["pb"], method="spearman")),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "push_burden_7d (rolling 7d sustained-exertion sibling; HA02 family primary)",
        "rationale": (
            "Per descriptive README section 3.4 + Q3.7.g spike-form note: "
            "push_burden_7d captures the trailing 7d cumulative exertion "
            "while exertion_class is the per-day point measurement. The "
            "covariate disambiguates: beta_channel attenuates if same-day "
            "exertion is just a marker for ongoing accumulated burden "
            "(push_burden_7d carries the signal); beta_channel survives if "
            "the day-level class encodes acute-day information beyond the "
            "rolling burden."
        ),
        "source": "DATA_DICTIONARY.md push_burden_7d + descriptive README section 3.4",
        "observed_spearman_on_S4": pb_corr,
        "expected_effect": (
            "beta_channel attenuates if sustained burden dominates; beta_"
            "channel survives if acute-day class encodes distinct information"
        ),
    })

    # 4. resting_hr -- cross-family autonomic anchor
    rhr_corr = None
    if "resting_hr" in df.columns:
        ord_v = encode_ordinal(df[channel].astype("object")).astype(float)
        d = pd.DataFrame({"_ord": ord_v, "rhr": df["resting_hr"]}).dropna()
        if len(d) > 30:
            rhr_corr = {
                "spearman_rho": float(d["_ord"].corr(d["rhr"], method="spearman")),
                "n": int(len(d)),
            }
    cands.append({
        "covariate": "resting_hr (cross-family cardiovascular anchor)",
        "rationale": (
            "Per Q3.6 sister analysis (resting_hr LANDED `5d28219`): "
            "cardiovascular state vs activity-axis state are conceptually "
            "distinct mechanisms. The covariate disambiguates: beta_channel "
            "attenuates if exertion-class signal is shared cardiovascular-"
            "tone (high RHR co-occurs with heavy exertion); beta_channel "
            "survives if exertion-class encodes activity-axis information "
            "beyond cardiovascular state."
        ),
        "source": "Q3.6 resting_hr Strand-A sister analysis",
        "observed_spearman_on_S4": rhr_corr,
        "expected_effect": (
            "beta_channel attenuates if shared cardiovascular-arousal "
            "dominates; beta_channel survives if activity-axis encodes "
            "distinct exertion-state information"
        ),
    })

    return {
        "primary_use_case": (
            "Future HA pre-reg using exertion_class as predictor of a "
            "crash-related outcome (HA01b-recomputed + HA01c + HA-C4c "
            "substantive verdicts already LOCKED at the noted statuses; "
            "further HAs can use the channel in different operands -- e.g. "
            "different threshold collapses, different leadup windows, "
            "different lagged-variant choices -- without re-anchoring the "
            "locked verdicts). Per CONVENTIONS section 3.2: any new HA "
            "should default to the v3.2 _lagged_lcera variant for PEM-"
            "pacing tests gated on lc_phase == 'lc'; un-lagged primary is "
            "for cross-era trajectory work or descriptive characterisation."
        ),
        "discipline_anchor": "HA-P7 hypothesis.md section 4.5.4 -- secondary-logistic-with-covariate pattern",
        "candidate_covariates": cands,
        "recommendation": (
            "Pre-spec all four covariates as secondary sensitivity arms. "
            "Covariate 1 (v3.2 lagged variant) is the CONVENTIONS section "
            "3.2 audit-hook compliance covariate; covariates 2 + 3 are the "
            "within-family operationalisation disambiguators; covariate 4 "
            "is the cross-family cardiovascular disambiguator. Per "
            "CONVENTIONS section 3.2: any draft analysis touching un-"
            "lagged exertion_class MUST stop and ask whether the v3.2 "
            "lagged variant is what's meant -- this Q3.7.i covariate 1 "
            "operationalises that audit hook for downstream HA pre-regs."
        ),
        "categorical_adaptation_note": (
            "Per CATEGORICAL ADAPTATION: covariates evaluated against "
            "ordinal-encoded primary using Spearman rho. Cohen's d / "
            "Pearson r equivalents are not load-bearing on the categorical "
            "5-level channel."
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
    sub["_label"] = sub[channel].astype(str)

    # Figure 1: per-category frequency bar
    fig, ax = plt.subplots(figsize=(8, 4.2))
    counts = sub["_label"].value_counts()
    cat_n = [int(counts.get(c, 0)) for c in CATEGORY_ORDER]
    n_total = int(sum(cat_n))
    cat_freq = [n / n_total if n_total > 0 else 0 for n in cat_n]
    colors = ["#cfe5d4", "#a4c9b0", "#e0c590", "#cc8a5e", "#a04848"]
    bars = ax.bar(CATEGORY_ORDER, cat_freq, color=colors, edgecolor="white")
    for bar, n, f in zip(bars, cat_n, cat_freq):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.005,
            "n={0}\n{1:.1%}".format(n, f),
            ha="center", va="bottom", fontsize=9,
        )
    ax.set_xlabel("exertion_class")
    ax.set_ylabel("frequency")
    ax.set_ylim(0, max(cat_freq) * 1.18 if cat_freq else 1)
    ax.set_title("exertion_class per-category frequency - Stratum 4, n={0}".format(n_total))
    fig.tight_layout()
    fp = out_dir / "fig1_per_category_frequency_s4.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 2: per-citalopram-phase stacked bar (categorical adaptation of violin)
    phase_freqs = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (sub["date"] >= pd.Timestamp(start)) & (sub["date"] <= pd.Timestamp(end))
        sub_p = sub.loc[mask, "_label"]
        n_p = len(sub_p)
        if n_p == 0:
            phase_freqs[phase_name] = [0] * len(CATEGORY_ORDER)
            continue
        cts = sub_p.value_counts()
        phase_freqs[phase_name] = [int(cts.get(c, 0)) / n_p for c in CATEGORY_ORDER]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    keep = [p for p in ("unmedicated", "buildup", "consolidation", "afbouw")
            if sum(phase_freqs[p]) > 0]
    bottom = np.zeros(len(keep))
    for j, c in enumerate(CATEGORY_ORDER):
        vals = [phase_freqs[p][j] for p in keep]
        ax.bar(keep, vals, bottom=bottom, color=colors[j], label=c, edgecolor="white")
        bottom = bottom + np.array(vals)
    ax.set_ylabel("category frequency")
    ax.set_ylim(0, 1)
    ax.legend(loc="upper right", bbox_to_anchor=(1.18, 1.0), fontsize=8, title="class")
    ax.set_title("exertion_class per-citalopram-phase frequency (Stratum 4)")
    fig.tight_layout()
    fp = out_dir / "fig2_phase_stratified_stacked_bar.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 3: per-month heavy/very_heavy spike-class rate trajectory + phase shading
    sub_sorted = sub.sort_values("date").reset_index(drop=True)
    sub_sorted["_year_month"] = sub_sorted["date"].dt.to_period("M")
    monthly = sub_sorted.groupby("_year_month").apply(
        lambda g: pd.Series({
            "month_mid": g["date"].min(),
            "heavy_or_very_heavy_rate": float(((g["_label"] == "heavy") | (g["_label"] == "very_heavy")).mean()),
            "very_heavy_rate": float((g["_label"] == "very_heavy").mean()),
            "none_rate": float((g["_label"] == "none").mean()),
        })
    ).reset_index()
    fig, ax = plt.subplots(figsize=(11, 4.6))
    phase_colors = {
        "unmedicated": "#ffffff",
        "buildup": "#fde0a3",
        "consolidation": "#ffd680",
        "afbouw": "#fdbf6f",
    }
    for phase_name, start, end in PHASE_BOUNDARIES:
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end),
                   color=phase_colors[phase_name], alpha=0.18, label=phase_name)
    ax.plot(monthly["month_mid"], monthly["heavy_or_very_heavy_rate"],
            color="#a04848", linewidth=1.8, marker="o", markersize=3, label="heavy+very_heavy rate")
    ax.plot(monthly["month_mid"], monthly["very_heavy_rate"],
            color="#7a1f1f", linewidth=1.2, linestyle="--", label="very_heavy rate")
    ax.plot(monthly["month_mid"], monthly["none_rate"],
            color="#5b88c4", linewidth=1.2, linestyle=":", label="none rate")
    ax.set_ylabel("monthly rate")
    ax.set_ylim(0, 1)
    ax.set_title("exertion_class monthly rates - spike-class + at-rest-class + citalopram phases")
    h, l = ax.get_legend_handles_labels()
    seen = set()
    pairs = [(hi, li) for hi, li in zip(h, l) if not (li in seen or seen.add(li))]
    ax.legend([p[0] for p in pairs], [p[1] for p in pairs],
              loc="upper right", fontsize=8, ncol=2)
    fig.tight_layout()
    fp = out_dir / "fig3_monthly_rate_trajectory.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 4: crash-vs-normal per-category frequency bar
    sub["is_crash_b"] = sub["is_crash"].astype(bool)
    crash_counts = sub.loc[sub["is_crash_b"], "_label"].value_counts()
    normal_counts = sub.loc[~sub["is_crash_b"], "_label"].value_counts()
    n_crash = int(sub["is_crash_b"].sum())
    n_normal = int((~sub["is_crash_b"]).sum())
    crash_freq = [int(crash_counts.get(c, 0)) / n_crash if n_crash > 0 else 0 for c in CATEGORY_ORDER]
    normal_freq = [int(normal_counts.get(c, 0)) / n_normal if n_normal > 0 else 0 for c in CATEGORY_ORDER]
    x = np.arange(len(CATEGORY_ORDER))
    width = 0.4
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.bar(x - width / 2, normal_freq, width, color="#9dc1e0", label="normal n={0}".format(n_normal))
    ax.bar(x + width / 2, crash_freq, width, color="#cc4949", label="crash n={0}".format(n_crash))
    ax.set_xticks(x)
    ax.set_xticklabels(CATEGORY_ORDER)
    ax.set_xlabel("exertion_class")
    ax.set_ylabel("within-group frequency")
    ax.set_title("exertion_class - crash-day vs normal-day per-category frequency (Stratum 4)")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    fp = out_dir / "fig4_crash_vs_normal_per_category.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    written.append(str(fp.relative_to(out_dir.parent)))

    # Figure 5: ACF on ordinal encoding
    ord_arr = encode_ordinal(sub["_label"]).astype(float).to_numpy()
    if len(ord_arr) >= 30:
        acf_res = compute_data_driven_block_length(ord_arr, default_block_length=7)
        acf = acf_res["autocorrelations"]
        fig, ax = plt.subplots(figsize=(8, 3.6))
        lags = np.arange(len(acf))
        ax.bar(lags, acf, width=0.7, color="#5b88c4", edgecolor="white")
        ax.axhline(0, color="#222", linewidth=0.5)
        threshold = 2.0 * np.sqrt(np.log(len(ord_arr)) / len(ord_arr))
        thresh_label = "|rho|={0:.3f} (Politis-White 2-sigma)".format(threshold)
        ax.axhline(threshold, color="#cc4949", linestyle="--", linewidth=0.8, label=thresh_label)
        ax.axhline(-threshold, color="#cc4949", linestyle="--", linewidth=0.8)
        ax.set_xlabel("lag (days)")
        ax.set_ylabel("autocorrelation (ordinal-encoded)")
        m_str = "n/a" if acf_res["cutoff_lag"] is None else str(acf_res["cutoff_lag"])
        title = "ACF - exertion_class ordinal encoding (Stratum 4); E[L]*={0:.1f}, M={1}".format(
            acf_res["optimal_block_length"], m_str,
        )
        ax.set_title(title)
        ax.legend(loc="upper right", fontsize=8)
        fig.tight_layout()
        fp = out_dir / "fig5_acf_ordinal.png"
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


def _fmt_per_category_row(label: str, per_cat_n: dict, per_cat_freq: dict, n: int) -> str:
    """Format a per-category row: | label | n | none% | light% | ... |."""
    return "| {0} | {1} | {2} | {3} | {4} | {5} | {6} |".format(
        label, n,
        "{0} ({1:.1%})".format(per_cat_n["none"], per_cat_freq["none"]),
        "{0} ({1:.1%})".format(per_cat_n["light"], per_cat_freq["light"]),
        "{0} ({1:.1%})".format(per_cat_n["moderate"], per_cat_freq["moderate"]),
        "{0} ({1:.1%})".format(per_cat_n["heavy"], per_cat_freq["heavy"]),
        "{0} ({1:.1%})".format(per_cat_n["very_heavy"], per_cat_freq["very_heavy"]),
    )


def _fmt_near_id_rows(rows_list: list) -> list:
    out = []
    for r in rows_list:
        if "pearson_r" in r:
            flag = "no" if not r["near_identity_flag"] else "**YES**"
            cat_marker = " (categorical sibling)" if r.get("is_categorical_sibling") else ""
            out.append(
                "| `{0}`{1} | {2} | {3:+.3f} | {4:+.3f} | {5} |".format(
                    r["channel"], cat_marker, r["n"],
                    r["pearson_r"], r["spearman_rho"], flag,
                )
            )
        else:
            out.append("| `{0}` | -- | -- | -- | {1} |".format(
                r["channel"], r.get("note", "n/a"),
            ))
    return out


def write_findings_md(summary: dict, path: Path) -> None:
    """Emit findings.md from the computed summary."""
    q = summary["questions"]
    a = q["Q3.7.a_distribution"]
    b = q["Q3.7.b_autocorrelation"]
    c = q["Q3.7.c_base_rates_per_phase"]
    d = q["Q3.7.d_phase_stratified_distribution"]
    e = q["Q3.7.e_near_identity"]
    fr = q["Q3.7.f_crash_vs_normal"]
    fl = fr["day_level"]
    fe = fr["episode_level"]
    g = q["Q3.7.g_spike_primitive"]
    h = q["Q3.7.h_outliers_calibration"]
    i = q["Q3.7.i_covariate_readiness"]

    el_star = b["data_driven_E_L_star"]
    chi_d = d["chi_square_test"]
    chi_f = fl["chi_square_2x5_test"]
    mwu = fl["mann_whitney_u_on_ordinal"]
    cd = fr["crash_drop_sensitivity_on_spearman_vs_gevoelscore_ordinal"]

    pcn = a["per_category_n"]
    pcf = a["per_category_frequency"]
    n_s4 = a["n"]

    near_id_rows = _fmt_near_id_rows(e["rows"])

    # Per-phase rows
    per_phase_rows = []
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = c.get(ph, {})
        if info.get("n", 0) > 0:
            per_phase_rows.append(
                _fmt_per_category_row(
                    "{0} ({1} to {2})".format(ph, info["date_start"], info["date_end"]),
                    info["per_category_n"], info["per_category_frequency"], info["n"],
                )
            )

    # Heavy+very_heavy fraction per phase
    heavy_per_phase = d["per_phase_heavy_or_very_heavy_fraction"]
    none_per_phase = d["per_phase_none_fraction"]
    ord_med_per_phase = d["per_phase_ordinal_median"]
    ent_per_phase = d["per_phase_shannon_entropy_nats"]

    # Monthly rate snapshots: just show selected dates (avoid huge table)
    monthly_records = h["monthly_rate_snapshots"]
    # Show ~ every 6 months
    if len(monthly_records) > 12:
        step = max(1, len(monthly_records) // 12)
        monthly_show = monthly_records[::step] + [monthly_records[-1]]
    else:
        monthly_show = monthly_records

    boundary_reads = h["boundary_step_reads"]

    # Run-length distribution
    run_dist = g["consecutive_heavy_run_distribution"]

    # Build the findings.md
    headline_class_str = ", ".join(
        "{0} {1:.1%}".format(c_name, pcf[c_name]) for c_name in CATEGORY_ORDER
    )
    headline_entropy = a["shannon_entropy_nats"]
    headline_entropy_norm = a["entropy_normalised"]
    chi_d_p_str = _format_p(chi_d["p_value"])
    chi_f_p_str = _format_p(chi_f["p_value"])
    mwu_p_str = _format_p(mwu["p_two_sided"])

    heavy_frac = a["heavy_or_very_heavy_fraction"]
    none_frac = a["none_fraction"]

    # Crash-vs-normal class shifts
    heavy_frac_diff = fl["heavy_or_very_heavy_fraction_diff_crash_minus_normal"]
    none_frac_diff = fl["none_fraction_diff_crash_minus_normal"]
    ord_mean_diff = fl["ordinal_mean_diff_crash_minus_normal"]
    ord_median_diff = fl["ordinal_median_diff_crash_minus_normal"]

    out_lines = [
        "# Findings -- `exertion_class` operationalisation-support descriptive (Q3.7.a-i)",
        "",
        "**Channel**: `exertion_class` (HA01b-recomputed + HA01b-per-axis-diagnostic + HA01c primary "
        "operand; HA-C4c heavy-T classifier substrate via the lagged variant; per-day categorical "
        "5-level ordinal {none, light, moderate, heavy, very_heavy} derived from steps + moderate-"
        "VPA + Garmin activity-labels per "
        "[`analyses/garmin_exploration/activity-labels/definition.md`](../../../analyses/garmin_exploration/activity-labels/definition.md)). "
        "Column semantics: [DATA_DICTIONARY.md activity-axis section](../../../DATA_DICTIONARY.md).",
        "",
        "**Substantive context**: HA01b-recomputed (v3.2 lagged baseline) is LOCKED REFUTED both eras "
        "(train +5.8 pp / validate +4.0 pp); R14 single-pool **+5.1 pp [-14.7, +13.3] perm p (E[L]=7) "
        "= 0.3689 NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED)** per "
        "[`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) row HA01b-"
        "recomputed. HA01b-per-axis-diagnostic SUPPORTED both eras at locked tau=0.75 per cell; "
        "load-bearing WITHHELD due to v2 threshold-monotonicity-diagnostic AMBIGUOUS. HA01c-effective-"
        "exertion-shock SUPPORTED both eras (train +21.3 / validate +19.5) at locked tau=0.75; also "
        "load-bearing WITHHELD per the same v2 diagnostic ambiguity per "
        "[REJECTED.md HA01c row](../../../REJECTED.md). HA-C4c (LANDED PARTIAL `a69a8ed`) uses "
        "`exertion_class_lagged_lcera in {heavy, very_heavy}` as the heavy-T classifier per "
        "[HA-C4c hypothesis.md section 4.1](../../../analyses/hypotheses/HA-C4c/hypothesis.md); the "
        "un-lagged primary `exertion_class` (this Q3.7 scope) is the underlying raw 5-level signal.",
        "",
        "**v3.1 -> v3.2 lagged-baseline correction context**: per "
        "[REJECTED.md HA01b-recomputed](../../../REJECTED.md) + "
        "[CONVENTIONS section 3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses): "
        "the original HA01b validate +17.3 pp 'first SUPPORTED' headline was a v3.1 rolling-baseline "
        "artefact that did NOT survive v3.2 lagged-baseline recomputation (softened by -13.3 pp to "
        "+4.0 pp). This is the **canonical project example of why lagged-baseline matters** per "
        "CONVENTIONS section 3.2. Q3.7.b autocorrelation discussion below cites descriptively; this "
        "Q3.7 is on the **un-lagged primary** `exertion_class` and does NOT re-litigate the v3.1 -> "
        "v3.2 correction per handoff section 3 hard constraint.",
        "",
        "**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to {0}). n={1} days "
        "with channel out of {2} Stratum 4 days ({3} NaN days).".format(
            summary["as_of_date"], n_s4,
            summary["n_rows_stratum_4_total"],
            summary["n_rows_stratum_4_total"] - n_s4,
        ),
        "",
        "**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 "
        "r3, commit `ccbd12e`) -- HA-touched non-confirmed channel candidate list bullet `exertion_"
        "class + push_burden_7d (HA01b/HA01c primaries) -- partially covered by activity-labels/`. "
        "**3rd of the 5 Tier 2 channels** in the user-prioritised Phase 2 sequential batch (Tier 1 "
        "closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain `7d49ba4`; Tier 2 2nd = Q3.6 resting_"
        "hr `5d28219`; this Q3.7 closes Tier 2 3rd; next: Q3.8 push_burden_7d, Q3.9 gevoelscore). "
        "**Q3.7.a-i template applied with explicit CATEGORICAL ADAPTATIONS** documented per question "
        "(per handoff section 1 + the stress_low_motion_min_count_S60_Mlow count-primitive adaptation "
        "precedent).",
        "",
        "**Sources**: `per_day_master.csv` (exertion_class column derived from activity-axis upstream "
        "extractor) + `labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with "
        "`crash-` episode-level per CONVENTIONS section 3.6).",
        "",
        "**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict "
        "promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). "
        "HA01b-recomputed + HA01b-per-axis-diagnostic + HA01c + HA-C4c (LOCKED) + R14 single-pool "
        "re-anchor (LOCKED `badd04a`) cross-references in this analysis are **descriptive "
        "corroboration only**; the substantive verdicts live in those result.md files and are NOT "
        "extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). The v3.1 -> "
        "v3.2 lagged-baseline correction is descriptively cited in Q3.7.b per handoff section 2.4; "
        "NOT re-litigated. Statistical hygiene anchors: section 3.1 (personal baseline), section 3.2 "
        "(lagged-baseline discipline; this analysis is on the un-lagged primary by handoff scope), "
        "section 3.3 (column-duplication threshold |rho|>=0.92), section 3.4 (crash-drop sensitivity "
        "|delta|>0.10), section 3.5 (spike metrics -- heavy/very_heavy class fraction IS the spike-"
        "form on this categorical channel), section 3.6 (named counts).",
        "",
        "---",
        "",
        "## Headline",
        "",
        "`exertion_class` on Stratum 4 is a **5-level categorical activity-axis channel** "
        "(distribution: {0}; Shannon entropy = {1:.3f} nats = {2:.1%} of max log(5)={3:.3f}; "
        "heavy+very_heavy spike-class fraction = {4:.1%}; at-rest none-class fraction = {5:.1%}). "
        "**Data-driven E[L]\\*={6:.1f} on ordinal-encoded series** (Politis-White; cutoff lag M={7}; "
        "factor-of-2 flag={8}; day-to-day transition rate = {9:.1%}; same-class persistence rate = "
        "{10:.1%}). **Per-phase frequency shifts** (citalopram axis): chi-square(df={11}) = {12:.2f}, "
        "p={13}; per-phase heavy+very_heavy fraction unmedicated {14:.1%} -> consolidation {15:.1%} "
        "-> afbouw {16:.1%}. **Crash-vs-normal**: chi-square 2x5 = {17:.2f} p={18}; Mann-Whitney U "
        "on ordinal encoding z={19:+.2f} p={20} P(crash > normal) = {21:.3f}; heavy+very_heavy "
        "fraction crash {22:.1%} vs normal {23:.1%} (diff {24:+.1%}); none fraction crash {25:.1%} "
        "vs normal {26:.1%} (diff {27:+.1%}); ordinal median diff = {28:+.1f} -- descriptively "
        "re-anchors HA01b-recomputed locked-REFUTED + R14 +5.1 pp NOT-SUPPORTED and HA01c locked-"
        "SUPPORTED-load-bearing-WITHHELD signals at the un-lagged-primary day-level read (HA01b/HA01c "
        "tested operand is on the v3.2 lagged variant; this Q3.7.f is the first-order day-level "
        "descriptive complement). Near-identity check: **{29}** pair(s) fire at the |rho|>=0.92 "
        "CONVENTIONS section 3.3 threshold. **Spike-form**: heavy+very_heavy burst-rate (>=2 spike "
        "days in trailing 7d) = {30:.1%} of days; max consecutive heavy/very_heavy run = {31} days; "
        "HA-C4c uses the lagged variant for its heavy-T classifier.".format(
            headline_class_str,
            headline_entropy, headline_entropy_norm, log(5),
            heavy_frac, none_frac,
            el_star, b["cutoff_lag_M"] if b["cutoff_lag_M"] is not None else "n/a",
            b["factor_of_2_deviation_flag"],
            b["transition_rate_day_over_day"], b["persistence_rate_day_over_day"],
            chi_d["df"], chi_d["chi2"], chi_d_p_str,
            heavy_per_phase.get("unmedicated", float("nan")),
            heavy_per_phase.get("consolidation", float("nan")),
            heavy_per_phase.get("afbouw", float("nan")),
            chi_f["chi2"], chi_f_p_str,
            mwu["z"], mwu_p_str, mwu["p_crash_greater_than_normal"],
            fl["heavy_or_very_heavy_fraction_crash"],
            fl["heavy_or_very_heavy_fraction_normal"],
            heavy_frac_diff,
            fl["none_fraction_crash"], fl["none_fraction_normal"], none_frac_diff,
            ord_median_diff,
            "Zero" if not e["flagged_pairs"] else "{0}".format(len(e["flagged_pairs"])),
            g["burst_rate_ge2_in_trailing_7d"],
            run_dist["max_run_length_days"],
        ),
        "",
        "---",
        "",
        "## Q3.7.a -- Distribution shape (Stratum 4) -- CATEGORICAL ADAPTATION",
        "",
        "**CATEGORICAL ADAPTATION**: The distribution-shape primitive IS the per-category frequency "
        "vector + marginal Shannon entropy (instead of mean/median/skewness applicable to continuous "
        "channels). Ordinal-encoded mean/median reported as auxiliary summaries (the channel has "
        "natural ordering none < light < moderate < heavy < very_heavy). No heavy-tail flag (not "
        "meaningful on a 5-level ordinal); rare-class flag (any class < 5%) used instead.",
        "",
        "### Per-category frequencies",
        "",
        "| category | n | frequency |",
        "|---|---:|---:|",
        "| none | {0} | {1:.1%} |".format(pcn["none"], pcf["none"]),
        "| light | {0} | {1:.1%} |".format(pcn["light"], pcf["light"]),
        "| moderate | {0} | {1:.1%} |".format(pcn["moderate"], pcf["moderate"]),
        "| heavy | {0} | {1:.1%} |".format(pcn["heavy"], pcf["heavy"]),
        "| very_heavy | {0} | {1:.1%} |".format(pcn["very_heavy"], pcf["very_heavy"]),
        "| **total** | **{0}** | **100%** |".format(n_s4),
        "",
        "### Entropy + auxiliary ordinal summaries",
        "",
        "| stat | value | source |",
        "|---|---:|---|",
        "| n (Stratum 4) | {0} | `per_day_master.csv` `exertion_class` non-NaN within S4 |".format(n_s4),
        "| Shannon entropy (nats) | **{0:.3f}** | -sum p log p over 5 categories |".format(a["shannon_entropy_nats"]),
        "| Max entropy log(5) | {0:.3f} | uniform 5-class baseline |".format(a["shannon_entropy_max_log_k"]),
        "| Normalised entropy | **{0:.1%}** | observed / log(5); near 100% = near-uniform |".format(a["entropy_normalised"]),
        "| Ordinal mean (none=0, ..., very_heavy=4) | {0:.3f} | auxiliary summary on ordinal encoding |".format(a["ordinal_mean"]),
        "| Ordinal median | {0:.1f} | auxiliary summary on ordinal encoding |".format(a["ordinal_median"]),
        "| Ordinal mode | **{0}** | most-frequent category |".format(a["ordinal_mode_label"]),
        "| heavy + very_heavy fraction (spike-class) | **{0:.1%}** | binary collapse for Q3.7.g spike-form |".format(a["heavy_or_very_heavy_fraction"]),
        "| none fraction (at-rest class) | **{0:.1%}** | |".format(a["none_fraction"]),
        "| min category frequency | {0:.1%} | rare-class flag if < 5% |".format(a["min_category_frequency"]),
        "| max category frequency | {0:.1%} | |".format(a["max_category_frequency"]),
        "| rare-class flag (any class < 5%) | **{0}** | CATEGORICAL ADAPTATION equivalent of heavy-tail flag |".format(a["rare_class_flag_min_freq_lt_0p05"]),
        "",
        "**Interpretation**: the 5-level distribution is **{0}** (normalised entropy {1:.1%}); the "
        "**spike-class (heavy + very_heavy) covers {2:.1%} of days** on Stratum 4 -- this fraction "
        "is the rate that drives HA01b-recomputed's operand (frac windows with >=1 day in 4-day "
        "leadup at lagged-class in {{heavy, very_heavy}}) on the lagged variant. The **at-rest class "
        "(none) covers {3:.1%}** -- the complement-rate informative for any future HA pre-reg "
        "operationalising 'low-activity day' on this channel.".format(
            "near-uniform across 5 classes" if a["entropy_normalised"] > 0.92 else (
                "moderately concentrated" if a["entropy_normalised"] > 0.85 else "concentrated"
            ),
            a["entropy_normalised"], a["heavy_or_very_heavy_fraction"], a["none_fraction"],
        ),
        "",
        "See [`plots/fig1_per_category_frequency_s4.png`](plots/fig1_per_category_frequency_s4.png).",
        "",
        "---",
        "",
        "## Q3.7.b -- Autocorrelation structure -- CATEGORICAL ADAPTATION + v3.1 -> v3.2 lagged-baseline correction citation",
        "",
        "**CATEGORICAL ADAPTATION**: Politis-White E[L]\\* computed on the **ordinal-encoded series** "
        "(none=0, light=1, moderate=2, heavy=3, very_heavy=4); transition-rate analysis "
        "(P(state_t != state_{t-1})) reported alongside as the additional categorical autocorrelation "
        "primitive distinct from the ordinal-encoded ACF (which leverages the ordering).",
        "",
        "### Ordinal-encoded ACF + Politis-White E[L]\\*",
        "",
        "The **data-driven block length is E[L]\\*={0:.1f}** (Politis-White 2004 with Patton-Politis-"
        "White 2009 correction per "
        "[`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) "
        "vs the project default E[L]=7 per "
        "[`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). "
        "The **factor-of-2 deviation flag = {1}** (deviation ratio = {2:.2f}). Cutoff lag M={3}.".format(
            el_star, b["factor_of_2_deviation_flag"], b["deviation_ratio"],
            b["cutoff_lag_M"] if b["cutoff_lag_M"] is not None else "n/a (no cutoff within max_lag)",
        ),
        "",
        "| lag (days) | autocorrelation (ordinal) |",
        "|---:|---:|",
    ]
    for lag_label in ("acf_lag1", "acf_lag2", "acf_lag3", "acf_lag7", "acf_lag14"):
        if lag_label in b["selected_acf_lags"]:
            v_lag = b["selected_acf_lags"][lag_label]
            sign = "+" if v_lag >= 0 else ""
            out_lines.append("| {0} | {1}{2:.3f} |".format(
                lag_label.replace("acf_lag", ""), sign, v_lag,
            ))
    out_lines.extend([
        "",
        "Politis-White 2-sigma significance threshold (n={0}): |rho| = {1:.3f}.".format(
            b["n_non_nan"], b["politis_white_significance_threshold_2sigma"],
        ),
        "",
        "### Transition-rate analysis (categorical autocorrelation primitive)",
        "",
        "Over **{0}** consecutive-day pairs in Stratum 4: **{1} transitions** (day-over-day class "
        "change). **Transition rate P(state_t != state_{{t-1}}) = {2:.1%}** "
        "(equivalently, same-class persistence rate = {3:.1%}). Per-class previous-day persistence "
        "(P(state_t = c | state_{{t-1}} = c)):".format(
            b["n_day_pairs"], b["n_transitions"],
            b["transition_rate_day_over_day"], b["persistence_rate_day_over_day"],
        ),
        "",
        "| previous-day class | n prev in class | next-day same-class count | next-day same-class rate |",
        "|---|---:|---:|---:|",
    ])
    for c_name in CATEGORY_ORDER:
        info = b["per_class_persistence"].get(c_name, {})
        if info.get("n_prev_day_in_class", 0) > 0:
            out_lines.append("| `{0}` | {1} | {2} | {3:.1%} |".format(
                c_name, info["n_prev_day_in_class"],
                info["next_day_same_class_count"], info["next_day_same_class_rate"],
            ))
    out_lines.extend([
        "",
        "### v3.1 -> v3.2 lagged-baseline correction descriptive citation (per handoff section 2.4)",
        "",
        "Per [CONVENTIONS section 3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses) "
        "+ [REJECTED.md HA01b-recomputed](../../../REJECTED.md): the v3.1 `exertion_class` uses a "
        "30-day **trailing rolling baseline that includes the candidate day itself**. In sustained-"
        "push periods the baseline creeps up with the pushes and a slow grind rebases into its own "
        "reference frame and stops looking heavy. v3.2 fixes this with a `[d-90, d-30]` window. "
        "The `_lagged_lcera` variant additionally restricts the baseline to LC-era days only.",
        "",
        "The original HA01b validate +17.3 pp 'first SUPPORTED' headline was substantially a v3.1 "
        "rolling-baseline artefact; HA01b-recomputed (v3.2 lagged) showed **REFUTED both eras** "
        "(train +5.8 pp / validate +4.0 pp); the delta vs original validate was **-13.3 pp**. This "
        "is the **canonical project example of why lagged-baseline matters** per CONVENTIONS section "
        "3.2 + REJECTED.md HA01b-recomputed.",
        "",
        "**This Q3.7.b autocorrelation analysis is on the un-lagged primary `exertion_class`** "
        "(NOT on the rolling-baseline-derived pre-classifier signal -- the categorical class IS the "
        "downstream operand of the v3.1 classifier). The autocorrelation observed here characterises "
        "the raw categorical day-to-day class signal AS-IS; per handoff section 3 hard constraint, "
        "this analysis does **NOT re-litigate the v3.1 -> v3.2 correction**. The lagged variants "
        "`exertion_class_lagged` + `exertion_class_lagged_lcera` are out of Strand-A scope per "
        "handoff section 1; any future HA pre-reg on this channel should default to the v3.2 "
        "lagged variant per CONVENTIONS section 3.2 audit hook.",
        "",
        "See [`plots/fig5_acf_ordinal.png`](plots/fig5_acf_ordinal.png).",
        "",
        "---",
        "",
        "## Q3.7.c -- Base rates per citalopram phase -- CATEGORICAL ADAPTATION",
        "",
        "**CATEGORICAL ADAPTATION**: Per-phase per-category frequency distribution + per-phase "
        "Shannon entropy (instead of per-phase median + dispersion as in continuous templates). "
        "Phase axis per "
        "[`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3:",
        "",
        "| phase (window) | n | none | light | moderate | heavy | very_heavy |",
        "|---|---:|---|---|---|---|---|",
        *per_phase_rows,
        "",
        "### Per-phase summary statistics",
        "",
        "| phase | n | heavy+very_heavy fraction | none fraction | ordinal median | Shannon entropy (nats) |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = c.get(ph, {})
        if info.get("n", 0) > 0:
            out_lines.append("| {0} | {1} | **{2:.1%}** | {3:.1%} | {4:.1f} | {5:.3f} |".format(
                ph, info["n"],
                info["heavy_or_very_heavy_fraction"],
                info["none_fraction"],
                info["ordinal_median"],
                info["shannon_entropy_nats"],
            ))
    out_lines.extend([
        "",
        "The two **transition phases** (buildup n={0}; afbouw n={1}) have **n<75 each**; the two "
        "**steady-state phases** (unmedicated n={2}; consolidation n={3}) are an order of magnitude "
        "larger. Any HA test that wants per-phase verdicts on this channel faces a ~10x n disadvantage "
        "vs the steady-state phases (same pattern as sister channels Q3.1.c / ... / Q3.6.c).".format(
            c.get("buildup", {}).get("n", 0),
            c.get("afbouw", {}).get("n", 0),
            c.get("unmedicated", {}).get("n", 0),
            c.get("consolidation", {}).get("n", 0),
        ),
        "",
        "Named counts (CONVENTIONS section 3.6): the per-phase per-category n's above are `exertion_"
        "class`-non-NaN day rows in `per_day_master.csv` within Stratum 4 date masks per "
        "`citalopram_phase_stratification.md section 3` boundary dates.",
        "",
        "See [`plots/fig2_phase_stratified_stacked_bar.png`](plots/fig2_phase_stratified_stacked_bar.png) "
        "(citalopram-phase stacked-frequency bars).",
        "",
        "---",
        "",
        "## Q3.7.d -- Phase-stratified distribution + chi-square test -- CATEGORICAL ADAPTATION",
        "",
        "**CATEGORICAL ADAPTATION**: Per handoff section 1 + CONVENTIONS section 4.2: phase shift "
        "primitive IS per-phase per-category frequency vector + entropy (instead of mean/median delta "
        "as in continuous-channel templates Q3.1.d ... Q3.6.d). Chi-square test of independence "
        "(4 phases x 5 categories) is the global-null descriptive indicator; pairwise per-category "
        "frequency deltas are the per-pair descriptive details.",
        "",
        "### Global chi-square test of independence",
        "",
        "| stat | value |",
        "|---|---:|",
        "| Chi-square statistic | **{0:.2f}** |".format(chi_d["chi2"]),
        "| Degrees of freedom | {0} |".format(chi_d["df"]),
        "| p-value (Wilson-Hilferty approx) | **{0}** |".format(chi_d_p_str),
        "",
        "**Descriptive reading**: the chi-square p-value is a nominal-null indicator only (CONVENTIONS "
        "section 4.2). Per handoff section 1 + 3 hard constraint: this Q3.7.d does NOT promote a "
        "substantive HA verdict; observed phase shifts may reflect (i) genuine activity-pattern "
        "change, (ii) categorical-boundary calibration drift on the v3.1 rolling-baseline definition "
        "of the upstream classifier per CONVENTIONS section 3.2, or (iii) co-temporal trajectory "
        "effects. The lagged variants `exertion_class_lagged` + `exertion_class_lagged_lcera` are "
        "out of Strand-A scope per handoff section 1; this Q3.7.d characterises the un-lagged primary "
        "as-is.",
        "",
        "### Pairwise frequency shifts (per category, between selected phase pairs)",
        "",
    ])
    pairs_to_show = [
        ("consolidation", "unmedicated"),
        ("afbouw", "consolidation"),
        ("afbouw", "unmedicated"),
    ]
    pair_shifts = d["pairwise_frequency_shifts"]
    for b_phase, a_phase in pairs_to_show:
        key = "{0}_minus_{1}_freq".format(b_phase, a_phase)
        if key in pair_shifts:
            sh = pair_shifts[key]
            out_lines.append("**{0} minus {1}** (frequency-points):".format(b_phase, a_phase))
            out_lines.append("")
            out_lines.append("| category | delta frequency (pp) |")
            out_lines.append("|---|---:|")
            for c_name in CATEGORY_ORDER:
                out_lines.append("| `{0}` | **{1:+.1%}** |".format(c_name, sh[c_name]))
            out_lines.append("")

    out_lines.extend([
        "### HA01b-recomputed + HA01c + HA-C4c locked-verdict cross-reference",
        "",
        "Per handoff section 1 + section 2.4 + section 3 hard constraint: HA01b-recomputed (v3.2 "
        "lagged baseline) LOCKED REFUTED both eras (train +5.8 / validate +4.0 pp); R14 single-pool "
        "+5.1 pp [-14.7, +13.3] perm p=0.3689 NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED). HA01b-"
        "per-axis-diagnostic SUPPORTED both eras at locked tau=0.75 per cell; load-bearing WITHHELD "
        "due to v2 threshold-monotonicity-diagnostic AMBIGUOUS. HA01c SUPPORTED both eras at locked "
        "tau=0.75 (train +21.3 / validate +19.5); also load-bearing WITHHELD per the same v2 "
        "diagnostic ambiguity. HA-C4c (LANDED PARTIAL `a69a8ed`) uses the lagged variant "
        "`exertion_class_lagged_lcera in {heavy, very_heavy}` as the heavy-T classifier on T; the "
        "cross-phase pooled with bar (b) failing per HA-C4c result.md. These are LOCKED and the "
        "observed phase shifts in Q3.7.d above are NOT a re-interpretation per CONVENTIONS section "
        "4.2.",
        "",
        "See [`plots/fig2_phase_stratified_stacked_bar.png`](plots/fig2_phase_stratified_stacked_bar.png) "
        "(stacked bars) and "
        "[`plots/fig3_monthly_rate_trajectory.png`](plots/fig3_monthly_rate_trajectory.png) "
        "(monthly heavy+very_heavy and none rate trajectory across the multi-year window).",
        "",
        "---",
        "",
        "## Q3.7.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3) -- CATEGORICAL ADAPTATION",
        "",
        "**CATEGORICAL ADAPTATION**: Spearman on ordinal-encoded primary vs continuous-form activity-"
        "axis sibling primitives. The two lagged categorical variants (`exertion_class_lagged` + "
        "`exertion_class_lagged_lcera`) are ordinal-encoded with the same 5-level mapping; expected "
        "high rho with the un-lagged primary by construction since they share the underlying "
        "classifier with shifted baseline windows. Per CONVENTIONS section 3.3: threshold is "
        "|rho|>=0.92. Per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed: downstream PEM-"
        "pacing consumers prefer the v3.2 lagged variant; any near-identity between un-lagged "
        "primary and a lagged variant reflects categorical-classifier overlap, NOT operand "
        "equivalence (the baseline window differs).",
        "",
        "| target channel | n | Pearson r | Spearman rho | near-identity flag? |",
        "|---|---:|---:|---:|---|",
        *near_id_rows,
        "",
        "**{0}** near-identity pair(s) fire at the |rho|>=0.92 CONVENTIONS section 3.3 threshold.".format(
            "Zero" if not e["flagged_pairs"] else len(e["flagged_pairs"]),
        ),
        "",
        "**Note**: any near-identity flag on the lagged variants is *expected* by construction (same "
        "classifier with shifted baseline window) and is **not a duplication finding** -- the operand "
        "differs even when the categorical encoding correlates highly. Per CONVENTIONS section 3.2 "
        "audit hook: any draft analysis touching `exertion_class` (un-lagged) must stop and ask "
        "whether the v3.2 lagged variant is what's meant; this Q3.7.e quantifies the operand-overlap "
        "rho descriptively.",
        "",
        "---",
        "",
        "## Q3.7.f -- Crash-day vs normal-day (Stratum 4) -- CATEGORICAL ADAPTATION + R14 HA01b-recomputed cross-reference",
        "",
        "**CATEGORICAL ADAPTATION**: Per handoff section 1 + section 2.4: chi-square 2x5 (crash x "
        "normal x 5 categories) AND Mann-Whitney U on ordinal encoding both reported (per handoff "
        "section 1 'chi-square or Mann-Whitney U on ordinal encoding for crash-vs-normal'); Cohen's "
        "d computed on ordinal encoding for parity with sister continuous Strand-A analyses (the "
        "rank-biserial r is also defensible on ordinal data; Cohen's d reported for cross-analysis "
        "consistency). Heavy+very_heavy spike-class fraction shift IS the spike-form crash-vs-normal "
        "primitive on this categorical channel.",
        "",
        "Per CONVENTIONS section 3.6 named counts: **{0}** crash-episodes (crash_v2 episode-level via "
        "`labels_crash_v2.csv` unique `episode_id` starting with `crash-`); **{1}** crash-days "
        "(day-level, `label=='crash'`); **{2}** non-crash days (the complement within Stratum 4 "
        "channel-valid days).".format(
            fe["n_crash_episodes"], fl["n_crash_day"], fl["n_normal_day"],
        ),
        "",
        "### Day-level per-category frequencies (crash vs normal)",
        "",
        "| category | crash freq | normal freq | crash minus normal (pp) |",
        "|---|---:|---:|---:|",
    ])
    for c_name in CATEGORY_ORDER:
        cf = fl["crash_per_category_frequency"][c_name]
        nf = fl["normal_per_category_frequency"][c_name]
        out_lines.append("| `{0}` | {1:.1%} | {2:.1%} | **{3:+.1%}** |".format(
            c_name, cf, nf, cf - nf,
        ))
    out_lines.extend([
        "",
        "### Day-level shifts on collapsed bins + ordinal-encoded summaries",
        "",
        "| stat | value |",
        "|---|---:|",
        "| heavy + very_heavy fraction crash | **{0:.1%}** |".format(fl["heavy_or_very_heavy_fraction_crash"]),
        "| heavy + very_heavy fraction normal | **{0:.1%}** |".format(fl["heavy_or_very_heavy_fraction_normal"]),
        "| diff (crash minus normal) | **{0:+.1%}** |".format(heavy_frac_diff),
        "| none fraction crash | **{0:.1%}** |".format(fl["none_fraction_crash"]),
        "| none fraction normal | **{0:.1%}** |".format(fl["none_fraction_normal"]),
        "| diff (crash minus normal) | **{0:+.1%}** |".format(none_frac_diff),
        "| ordinal mean diff (crash - normal) | **{0:+.3f}** |".format(ord_mean_diff),
        "| ordinal median diff (crash - normal) | **{0:+.1f}** |".format(ord_median_diff),
        "",
        "### Chi-square 2x5 (crash x normal x 5 categories)",
        "",
        "| stat | value |",
        "|---|---:|",
        "| Chi-square statistic | **{0:.2f}** |".format(chi_f["chi2"]),
        "| Degrees of freedom | {0} |".format(chi_f["df"]),
        "| p-value (Wilson-Hilferty approx) | **{0}** |".format(chi_f_p_str),
        "",
        "### Mann-Whitney U on ordinal encoding",
        "",
        "| stat | value |",
        "|---|---:|",
        "| U (crash as first sample) | {0:.1f} |".format(mwu["U_crash_first_sample"]),
        "| z (normal approx, tie-corrected) | **{0:+.2f}** |".format(mwu["z"]),
        "| p (two-sided) | **{0}** |".format(mwu_p_str),
        "| P(crash > normal) | **{0:.3f}** |".format(mwu["p_crash_greater_than_normal"]),
        "",
        "### Episode-level (per CONVENTIONS section 3.6)",
        "",
        "| stat | value |",
        "|---|---:|",
        "| n crash-episodes | {0} |".format(fe["n_crash_episodes"]),
        "| n normal-day base rate | {0} |".format(fe["n_normal_day_base_rate"]),
        "| mean per-episode ordinal value | {0:.3f} |".format(fe["mean_per_episode_ordinal"]),
        "| mean normal-day ordinal value | {0:.3f} |".format(fe["mean_normal_day_ordinal"]),
        "| mean diff (episode minus normal-day) | **{0:+.3f}** |".format(fe["mean_diff_episode_vs_normal_day_ordinal"]),
        "| Cohen's d (episode-level vs normal-day pooled, ordinal-encoded) | **{0:+.2f}** |".format(fe["cohens_d_episode_vs_normal_day_ordinal"]),
        "| Bootstrap 95% CI on mean diff (ordinal) | **[{0:+.3f}, {1:+.3f}]** ({2} iters, seed={3}) |".format(
            fe["bootstrap_ci95_mean_diff_ordinal"][0],
            fe["bootstrap_ci95_mean_diff_ordinal"][1],
            fe["n_bootstrap"], fe["seed"],
        ),
        "",
        "### LOAD-BEARING HA01b-recomputed R14 single-pool + HA01c locked descriptive cross-reference (per handoff section 2.4)",
        "",
        "Per [single_pool_reanchor/findings.md](../single_pool_reanchor/findings.md) row HA01b-"
        "recomputed: R14 single-pool **+5.1 pp [CI -14.7, +13.3] perm p=0.3689 NOT-SUPPORTED "
        "CONVERGE (both NOT-SUPPORTED)** (`badd04a`). Per "
        "[REJECTED.md HA01c](../../../REJECTED.md): HA01c SUPPORTED both eras at locked tau=0.75 "
        "(train +21.3 / validate +19.5); load-bearing WITHHELD due to v2 threshold-monotonicity-"
        "diagnostic AMBIGUOUS. This Q3.7.f's day-level chi-square + Mann-Whitney U + episode-level "
        "Cohen's d on the un-lagged primary **descriptively re-anchor** the HA01b-recomputed locked-"
        "REFUTED + R14 NOT-SUPPORTED signal and the HA01c locked-SUPPORTED-load-bearing-WITHHELD "
        "signal at the first-order day-level read on the categorical primary -- the HA tests use "
        "the v3.2 lagged variant operand (exertion_class_lagged in {heavy, very_heavy} OR "
        "eff_exertion_rank_lagged at tau=0.75); this Q3.7.f reports the day-level descriptive "
        "complement on the un-lagged categorical primary. **The HA01b-recomputed + HA01b-per-axis-"
        "diagnostic + HA01c + R14 single-pool substantive verdicts are LOCKED**; this Q3.7.f "
        "observation is descriptive corroboration only, NOT a re-interpretation of either, and NOT "
        "a re-litigation of the v3.1 -> v3.2 correction (Q3.7.b citation is the descriptive cite per "
        "handoff section 2.4).",
        "",
        "### Crash-drop sensitivity (CONVENTIONS section 3.4) on Spearman vs gevoelscore (ordinal-encoded)",
        "",
    ])

    if cd is not None:
        out_lines.extend([
            "| frame | Spearman rho (ordinal vs gevoelscore) | n |",
            "|---|---:|---:|",
            "| full Stratum 4 | {0:+.3f} | {1} |".format(cd["full_frame_value"], cd["n_full"]),
            "| crash-days dropped | {0:+.3f} | {1} |".format(cd["crash_dropped_value"], cd["n_crash_dropped"]),
            "| \\|delta\\| | **{0:.3f}** | -- |".format(cd["abs_delta"]),
            "| section 3.4 threshold (0.10) crossed? | **{0}** | -- |".format(
                "yes" if cd["exceeds_threshold_0p10"] else "no",
            ),
            "",
        ])
    else:
        out_lines.extend([
            "Crash-drop sensitivity uncomputable (insufficient n in crash/normal subsets).",
            "",
        ])

    out_lines.extend([
        "See [`plots/fig4_crash_vs_normal_per_category.png`](plots/fig4_crash_vs_normal_per_category.png).",
        "",
        "---",
        "",
        "## Q3.7.g -- Spike-detecting primitive availability -- CATEGORICAL ADAPTATION + HA-C4c heavy-T classifier framing",
        "",
        "**CATEGORICAL ADAPTATION**: Per handoff section 1 + CONVENTIONS section 3.5 spike metrics: "
        "the spike-form on a 5-level ordinal channel is the **heavy/very_heavy class fraction** "
        "(rare-class point primitive) + the **within-7d burst-rate** (sustained-exertion primitive). "
        "These mirror the spike-form for count primitives (stress_low_motion_min_count_S60_Mlow "
        "Q3.4.g) and the per-4-day MAX |z| spike-form for daily-aggregate continuous channels "
        "(resting_hr Q3.6.g). Per CONVENTIONS section 3.5: this categorical spike-form IS the "
        "operationalisation substrate for HA-C4c's heavy-T classifier construct on the lagged "
        "variant.",
        "",
        "### Spike-class point primitive",
        "",
        "| stat | value |",
        "|---|---:|",
        "| n heavy/very_heavy spike days | {0} |".format(g["n_heavy_spike_days"]),
        "| heavy + very_heavy day rate | **{0:.1%}** |".format(g["heavy_or_very_heavy_rate"]),
        "| n very_heavy days (extreme tail) | {0} |".format(g["n_very_heavy_days"]),
        "| very_heavy day rate | {0:.1%} |".format(g["very_heavy_rate"]),
        "",
        "### Within-7d burst-rate primitive",
        "",
        "| stat | value |",
        "|---|---:|",
        "| burst-rate (>=2 spike days in trailing 7d) | **{0:.1%}** |".format(g["burst_rate_ge2_in_trailing_7d"]),
        "| burst-rate (>=3 spike days in trailing 7d) | {0:.1%} |".format(g["burst_rate_ge3_in_trailing_7d"]),
        "",
        "### Consecutive heavy/very_heavy run distribution",
        "",
        "| stat | value |",
        "|---|---:|",
        "| n runs | {0} |".format(run_dist["n_runs"]),
        "| max run length (days) | **{0}** |".format(run_dist["max_run_length_days"]),
        "| median run length (days) | {0:.1f} |".format(run_dist["median_run_length_days"]),
        "| mean run length (days) | {0:.2f} |".format(run_dist["mean_run_length_days"]),
        "",
        "### HA-C4c heavy-T classifier framing (per handoff section 2.4)",
        "",
        "Per [HA-C4c hypothesis.md section 4.1](../../../analyses/hypotheses/HA-C4c/hypothesis.md) "
        "(LANDED PARTIAL `a69a8ed`): HA-C4c uses **`exertion_class_lagged_lcera in {heavy, very_heavy}` "
        "on T as the heavy-T classifier**. The un-lagged primary `exertion_class` (this Q3.7 scope) "
        "is the underlying raw 5-level signal; the lagged variant applies the lagged-baseline "
        "correction per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed canonical example "
        "(the v3.2 _lagged_lcera form uses a [d-90, d-30] window restricted to LC-era days). "
        "Coverage within LC era ~83% per HA-C4c hypothesis.md section 4.4. **Per handoff section 3 "
        "hard constraint**: HA-C4c result is LOCKED PARTIAL (cross-phase pooled with bar (b) "
        "failing); this Q3.7.g does **NOT extend or re-anchor HA-C4c** -- the substrate "
        "characterisation here is descriptive only.",
        "",
        "Lagged variant coverage in master:",
        "",
    ])
    for c_name, info in g["lagged_variants_in_master"].items():
        out_lines.append("- `{0}`: n non-NaN = {1} / total {2} ({3:.1%})".format(
            c_name, info["n_non_nan"], info["n_total"],
            info["n_non_nan"] / info["n_total"] if info["n_total"] > 0 else 0,
        ))

    out_lines.extend([
        "",
        "---",
        "",
        "## Q3.7.h -- Outlier detection + calibration-drift check -- CATEGORICAL ADAPTATION + activity-labels partial-coverage xref",
        "",
        "**CATEGORICAL ADAPTATION**: Per handoff section 1: outlier semantics differ for categorical "
        "channels -- no MAD-z applicable (the channel is a 5-level ordinal, not a continuous "
        "magnitude). The categorical-equivalent diagnostics are (i) rare-class flag (any class < 5%) "
        "reported in Q3.7.a, (ii) per-month rate-drift snapshots for the rare-class (very_heavy) and "
        "the spike-class (heavy/very_heavy combined) reported below, and (iii) boundary-step reads "
        "at the citalopram phase boundaries (where a categorical-classifier calibration drift would "
        "surface as a step change in class frequencies).",
        "",
        "### activity-labels partial-coverage descriptive cross-reference (per handoff section 2.4)",
        "",
        "Per "
        "[`garmin_exploration/activity-labels/`](../../../analyses/garmin_exploration/activity-labels/): "
        "existing primitive-validation + visualisation runs on this channel family (definition.md "
        "severity cutoffs + scripts/ produced ha_results_4day_lagged.md). **Coverage is PARTIAL** "
        "per descriptive README section 3.4: the existing artefact does primitive-spec + HA-test "
        "validation but does NOT cover the Q3.x.a-i operationalisation-support per-channel template. "
        "This Q3.7 provides the per-channel substrate the activity-labels artefact does NOT have. "
        "Per activity-labels/definition.md (cited descriptively): 'severity cutoffs for exertion_"
        "class are NOT locked' -- this is the upstream-classifier discipline note. Q3.7.h's per-"
        "month rate-drift snapshots below characterise the categorical-distribution stability AS-IS "
        "for the v3.1 un-lagged primary; any calibration-drift signature in the snapshot table is a "
        "Layer 1 descriptive observation, NOT a re-promotion of the v3.1 cutoff lock per handoff "
        "section 3 hard constraint.",
        "",
        "### Per-month rate snapshots (selected; full table available in summary.json)",
        "",
        "| year_month | n | very_heavy rate | heavy+very_heavy rate | none rate |",
        "|---|---:|---:|---:|---:|",
    ])
    for rec in monthly_show:
        out_lines.append("| {0} | {1} | {2:.1%} | {3:.1%} | {4:.1%} |".format(
            rec["year_month"], rec["n"], rec["very_heavy_rate"],
            rec["heavy_or_very_heavy_rate"], rec["none_rate"],
        ))
    out_lines.extend([
        "",
        "### Boundary-step reads (pre/post 30d at citalopram phase boundaries)",
        "",
        "| boundary | n_pre | n_post | heavy+very_heavy rate pre | rate post | diff | none rate pre | rate post | diff |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for label, br in boundary_reads.items():
        out_lines.append("| {0} | {1} | {2} | {3:.1%} | {4:.1%} | **{5:+.1%}** | {6:.1%} | {7:.1%} | **{8:+.1%}** |".format(
            label, br["n_pre"], br["n_post"],
            br["heavy_or_very_heavy_rate_pre"], br["heavy_or_very_heavy_rate_post"], br["heavy_or_very_heavy_rate_diff"],
            br["none_rate_pre"], br["none_rate_post"], br["none_rate_diff"],
        ))

    out_lines.extend([
        "",
        "See [`plots/fig3_monthly_rate_trajectory.png`](plots/fig3_monthly_rate_trajectory.png) "
        "(monthly trajectory with citalopram-phase shading).",
        "",
        "---",
        "",
        "## Q3.7.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel",
        "",
        "Discipline anchor: "
        "[HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) "
        "(secondary-logistic-with-covariate pattern; beta disambiguation between primary-signal and "
        "candidate alternative readings). Names **four** candidate covariates a future HA on "
        "`exertion_class` as predictor should pre-spec.",
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
        obs = cand.get("observed_spearman_on_S4")
        if obs:
            out_lines.append("*Observed Spearman rho on S4 (ordinal-encoded primary vs covariate)*: "
                             "rho={0:+.3f} (n={1}).".format(obs["spearman_rho"], obs["n"]))
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
        "- **HA01b-recomputed** (v3.2 lagged composite at exertion_class_lagged in {{heavy, very_heavy}}; "
        "LOCKED REFUTED both eras +5.8 / +4.0 pp; R14 single-pool NOT-SUPPORTED CONVERGE `badd04a`): "
        "primary operand IS this channel on the **lagged** variant. **The descriptive substrate "
        "this analysis produces -- the per-category frequencies (Q3.7.a) + ordinal autocorrelation "
        "E[L]\\*={0:.1f} + transition-rate {1:.1%} (Q3.7.b) + per-citalopram-phase frequency "
        "distribution + chi-square (Q3.7.c+d) + first-order day-level crash-vs-normal chi-square + "
        "Mann-Whitney U + per-class shifts (Q3.7.f) -- complements HA01b-recomputed's tested operand "
        "with the un-lagged categorical-channel distribution view.** The substantive HA01b-recomputed "
        "verdict + the R14 single-pool verdict are LOCKED; this analysis's descriptive corroboration "
        "in Q3.7.f is NOT a re-interpretation and NOT a re-litigation of the v3.1 -> v3.2 correction "
        "(descriptive citation only per Q3.7.b + handoff section 2.4).".format(
            el_star, b["transition_rate_day_over_day"],
        ),
        "- **HA01b-per-axis-diagnostic** (locked SUPPORTED both eras at tau=0.75 per cell; load-"
        "bearing WITHHELD due to v2 threshold-monotonicity-diagnostic AMBIGUOUS): the per-axis "
        "diagnostic operand reduces to this channel's per-category structure on the lagged variant; "
        "Q3.7.c+d descriptively characterise the un-lagged-primary per-phase structure.",
        "- **HA01c-effective-exertion-shock** (locked SUPPORTED both eras at tau=0.75; load-bearing "
        "WITHHELD; uses eff_exertion_rank_lagged at tau=0.75): Q3.7.f day-level descriptively re-"
        "anchors at the un-lagged categorical-primary read.",
        "- **HA-C4c** (LANDED PARTIAL `a69a8ed`; cross-phase pooled with bar (b) failing): uses "
        "`exertion_class_lagged_lcera in {heavy, very_heavy}` as the heavy-T classifier on T per "
        "hypothesis.md section 4.1; this Q3.7 characterises the un-lagged primary `exertion_class` "
        "as the underlying raw 5-level signal substrate.",
        "",
        "### Methodology MDs cited",
        "",
        "- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3 -- Q3.7.c phase axis; Q3.7.d phase-stratified treatment.",
        "- [`CONVENTIONS.md` section 3.2 lagged-baseline](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses) "
        "+ [`REJECTED.md` HA01b-recomputed row](../../../REJECTED.md) -- canonical project example "
        "of why lagged-baseline matters; cited descriptively in Q3.7.b (NOT re-litigated per "
        "handoff section 3 hard constraint).",
        "- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) "
        "-- E[L]=7 default + factor-of-2 deviation rule; Q3.7.b reports E[L]\\*={0:.1f}.".format(el_star),
        "- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) "
        "-- Stratum 4 boundary definition.",
        "- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) "
        "-- Q3.7.h cross-reference framing (the activity-axis classifier itself is upstream of UDS "
        "passthrough; Q3.7.h's per-month rate-drift snapshots are the categorical-equivalent "
        "calibration-drift diagnostic).",
        "",
        "### Existing artefacts referenced",
        "",
        "- [`analyses/garmin_exploration/activity-labels/`](../../../analyses/garmin_exploration/activity-labels/) "
        "**partial-coverage** descriptive cross-reference in Q3.7.h: existing primitive-spec + HA-"
        "test validation; does NOT cover Q3.x.a-i operationalisation-support per-channel template "
        "(this Q3.7 closes the gap).",
        "- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) "
        "-- R14 HA01b-recomputed row (LANDED `badd04a`); descriptively corroborated in Q3.7.f.",
        "- [`descriptive/operationalisation_support/resting_hr/findings.md`](../resting_hr/findings.md) "
        "-- Q3.6 most-recent Tier 2 precedent; programmatic-emit pattern + clean f-string discipline.",
        "- [`descriptive/operationalisation_support/bb_overnight_gain/findings.md`](../bb_overnight_gain/findings.md) "
        "-- Q3.5 Tier 2 first precedent; coverage-discipline.",
        "- [`descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/findings.md`](../stress_low_motion_min_count_S60_Mlow/findings.md) "
        "-- Phase 1 third precedent; non-continuous primitive (count) adaptation precedent for "
        "this Q3.7's CATEGORICAL ADAPTATION discipline.",
        "- [`analyses/hypotheses/HA-C4c/hypothesis.md`](../../../analyses/hypotheses/HA-C4c/hypothesis.md) "
        "-- heavy-T classifier framing cited in Q3.7.g (LANDED PARTIAL `a69a8ed`).",
        "- [`REJECTED.md`](../../../REJECTED.md) HA01b-recomputed row -- canonical v3.1 -> v3.2 "
        "lagged-baseline correction example cited descriptively in Q3.7.b.",
        "",
        "### Upstream pipeline",
        "",
        "- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- activity-"
        "axis upstream classifier producing exertion_class per `analyses/garmin_exploration/activity-"
        "labels/definition.md` severity cutoffs.",
        "- `labels_crash_v2.csv` <- `analyses/hypotheses/crash_v2-definition/definition.md` (locked).",
        "",
        "---",
        "",
        "## Limitations",
        "",
        "For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per "
        "[CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the "
        "binding constraints are:",
        "",
        "1. **No HA verdict promotion**: HA01b-recomputed + HA01b-per-axis-diagnostic + HA01c + HA-"
        "C4c + R14 single-pool verdicts are LOCKED; this analysis's descriptive observations are "
        "NOT re-interpretations or re-promotions per CONVENTIONS section 4.2 + handoff section 3.",
        "2. **No re-litigation of v3.1 -> v3.2 lagged-baseline correction** per handoff section 3 "
        "hard constraint. The Q3.7.b descriptive citation acknowledges the correction as the "
        "canonical project example per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed; the "
        "load-bearing correction story lives in those artefacts and is the canonical reference, NOT "
        "extended or restated here.",
        "3. **Un-lagged primary scope per handoff section 1**: this Q3.7 covers the un-lagged "
        "primary `exertion_class` only; the lagged variants `exertion_class_lagged` + `exertion_"
        "class_lagged_lcera` are derivatives used in HA pre-reg contexts and are out of Strand-A "
        "scope. Any future HA pre-reg should default to the v3.2 lagged variant per CONVENTIONS "
        "section 3.2 audit hook (Q3.7.i covariate 1 operationalises that).",
        "4. **Categorical adaptations explicitly documented per question** per handoff section 1 + 3 "
        "hard constraint: each Q3.7.x section flags its categorical adaptation deviation from the "
        "continuous-template precedents (mean/median/skewness -> per-category frequencies + entropy; "
        "ACF -> ordinal-encoded ACF + transition rate; near-identity -> Spearman on ordinal encoding "
        "+ explicit categorical-sibling marking; crash-vs-normal -> chi-square 2x5 + MWU on ordinal "
        "+ heavy/very_heavy spike-class fraction; spike-form -> heavy/very_heavy burst frequency; "
        "outlier -> rare-class flag + per-month rate-drift). Per handoff section 1: 'document "
        "adaptations explicitly in narrative + flag any deviations from continuous-template "
        "precedents.'",
        "5. **First-order day-level read distinct from HA01b/HA01c tested operands**: HA01b-"
        "recomputed's operand is the 4-day-window composite on the lagged variant; HA01c's is the "
        "effective-exertion-rank shock at tau=0.75 on the lagged rank; HA-C4c's is the heavy-T "
        "classifier on the lagged-lcera variant. This Q3.7.f's first-order day-level chi-square + "
        "Mann-Whitney U on the un-lagged categorical primary is the descriptive complement at a "
        "coarser resolution -- NOT a re-anchoring of the locked HA verdicts.",
        "",
        "---",
        "",
        "*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` "
        "(gitignored per `docs/research/**/*.json`). To refresh: ``python run.py``.*",
        "",
    ])

    path.write_text("\n".join(out_lines), encoding="utf-8")


def write_readme_md(summary: dict, path: Path) -> None:
    """Emit README.md from the computed summary."""
    q = summary["questions"]
    a = q["Q3.7.a_distribution"]
    b = q["Q3.7.b_autocorrelation"]
    d = q["Q3.7.d_phase_stratified_distribution"]
    fr = q["Q3.7.f_crash_vs_normal"]
    fl = fr["day_level"]
    fe = fr["episode_level"]
    g = q["Q3.7.g_spike_primitive"]
    el_star = b["data_driven_E_L_star"]
    chi_f = fl["chi_square_2x5_test"]
    mwu = fl["mann_whitney_u_on_ordinal"]
    n_near_id_flags = len(q["Q3.7.e_near_identity"].get("flagged_pairs", []))

    el_match = (
        "Politis-White E[L]\\*={0:.1f} (vs project default 7); factor-of-2 deviation flag = {1}".format(
            el_star, b["factor_of_2_deviation_flag"],
        )
    )

    pcf = a["per_category_frequency"]
    headline_class_str = ", ".join(
        "{0} {1:.1%}".format(c_name, pcf[c_name]) for c_name in CATEGORY_ORDER
    )

    chi_f_p_str = _format_p(chi_f["p_value"])
    mwu_p_str = _format_p(mwu["p_two_sided"])

    out_lines = [
        "# `exertion_class` -- operationalisation-support descriptive analysis",
        "",
        "**Strand**: A (operationalisation support; template-driven with CATEGORICAL ADAPTATIONS "
        "documented per Q3.7.a-i; no operationalisation interview required per "
        "[`descriptive/README.md`](../../README.md) section 7b).",
        "",
        "## Research question",
        "",
        "Operationalisation-support descriptive characterisation of `exertion_class` on Stratum 4, "
        "answering Q3.7.a-i per the locked descriptive programme spec at "
        "[`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.4 (LOCKED "
        "2026-06-18 r3, commit `ccbd12e`; this channel listed as HA01b/HA01c primary, partially "
        "covered by activity-labels/). **3rd of the 5 Tier 2 channels** in the user-prioritised "
        "Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain "
        "`7d49ba4`; Tier 2 2nd = Q3.6 resting_hr `5d28219`; this Q3.7 closes Tier 2 3rd; next: "
        "Q3.8 push_burden_7d, Q3.9 gevoelscore).",
        "",
        "Substantive status: **HA01b-recomputed primary operand** on the lagged variant (v3.2 "
        "lagged composite at exertion_class_lagged in {heavy, very_heavy}; LOCKED REFUTED both "
        "eras +5.8 / +4.0 pp per "
        "[activity-labels/output/ha_results_4day_lagged.md](../../../analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md); "
        "R14 single-pool **+5.1 pp [-14.7, +13.3] perm p=0.3689 NOT-SUPPORTED CONVERGE (both NOT-"
        "SUPPORTED)** `badd04a`). Also **HA01b-per-axis-diagnostic primary** (SUPPORTED both eras "
        "at locked tau=0.75; load-bearing WITHHELD due to v2 threshold-monotonicity-diagnostic "
        "AMBIGUOUS) and **HA01c-effective-exertion-shock primary** on eff_exertion_rank_lagged "
        "(SUPPORTED both eras train +21.3 / validate +19.5; load-bearing WITHHELD per the same v2 "
        "diagnostic ambiguity per [REJECTED.md HA01c](../../../REJECTED.md)). HA-C4c (LANDED "
        "PARTIAL `a69a8ed`) uses `exertion_class_lagged_lcera in {heavy, very_heavy}` as the "
        "heavy-T classifier on T per "
        "[HA-C4c hypothesis.md section 4.1](../../../analyses/hypotheses/HA-C4c/hypothesis.md). "
        "**v3.1 -> v3.2 lagged-baseline correction is the canonical project example** per "
        "CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed; the original HA01b validate +17.3 "
        "pp 'first SUPPORTED' headline was a v3.1 rolling-baseline artefact (softened by -13.3 pp "
        "on v3.2 recomputation). Q3.7.b cites the correction descriptively per handoff section "
        "2.4; this Q3.7 does NOT re-litigate per handoff section 3 hard constraint.",
        "",
        "## Method",
        "",
        "- **Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to {0}; n={1} "
        "channel-valid days out of {2} S4 days).".format(
            summary["as_of_date"], a["n"], summary["n_rows_stratum_4_total"],
        ),
        "- **Primary phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) "
        "section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with sister Strand-A "
        "analyses Q3.1 / Q3.2 / Q3.3 / Q3.4 / Q3.5 / Q3.6.",
        "- **Scope per handoff section 1**: focus on **un-lagged primary `exertion_class`**; "
        "lagged variants (`exertion_class_lagged` + `exertion_class_lagged_lcera`) are derivatives "
        "used in HA pre-reg contexts (HA01b-recomputed, HA-C4c heavy-T classifier) and are out of "
        "Strand-A scope.",
        "- **CATEGORICAL ADAPTATIONS** of the Q-template (per handoff section 1, modelled on the "
        "stress_low_motion count-primitive adaptation precedent) documented explicitly per Q3.7.x "
        "section: Q3.7.a per-category frequencies + Shannon entropy (no mean/median/skewness); "
        "Q3.7.b autocorrelation on **ordinal encoding** + transition-rate analysis; Q3.7.c per-"
        "phase per-category frequency distribution + per-phase entropy; Q3.7.d chi-square test of "
        "independence (4 phases x 5 categories) + pairwise frequency shifts; Q3.7.e Spearman on "
        "ordinal encoding vs continuous-form sibling activity-axis primitives + categorical-sibling "
        "marking on lagged variants; Q3.7.f **chi-square 2x5 AND Mann-Whitney U on ordinal** + "
        "Cohen's d on ordinal; Q3.7.g heavy/very_heavy class fraction + within-7d burst-rate + "
        "consecutive-run distribution; Q3.7.h rare-class flag + per-month rate-drift snapshots + "
        "boundary-step reads (no MAD-z; outlier semantics differ for categorical); Q3.7.i "
        "covariate-sensitivity readiness.",
        "- **Computed directly from `per_day_master.csv`**: Q3.7.a (per-category frequencies + "
        "entropy + auxiliary ordinal summaries), Q3.7.b (Politis-White E[L]\\* on ordinal + "
        "transition rate + per-class persistence + v3.1 -> v3.2 lagged-baseline correction "
        "descriptive citation), Q3.7.c (per-phase per-category frequencies + entropy), Q3.7.d "
        "(global chi-square + pairwise frequency shifts + HA01b-recomputed/HA01c/HA-C4c locked-"
        "verdict cross-reference), Q3.7.e (Spearman on ordinal vs activity-axis sibling panel), "
        "Q3.7.f (chi-square 2x5 + Mann-Whitney U + ordinal Cohen's d + LOAD-BEARING R14 HA01b-"
        "recomputed single-pool descriptive cross-reference), Q3.7.g (heavy/very_heavy spike-form "
        "+ burst-rate + run distribution + HA-C4c heavy-T classifier framing), Q3.7.h (rare-class "
        "+ per-month rate-drift + boundary-step reads + activity-labels partial-coverage xref), "
        "Q3.7.i (covariate readiness with v3.2 lagged variant as the CONVENTIONS section 3.2 "
        "audit-hook compliance covariate).",
        "- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, "
        "Stratum 4 filter, crash-drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) "
        "(`compute_data_driven_block_length`, `stationary_bootstrap_ci`).",
        "- **Load-bearing cross-references** per handoff section 2.4: v3.1 -> v3.2 lagged-baseline "
        "correction descriptively cited in Q3.7.b per CONVENTIONS section 3.2 + REJECTED.md HA01b-"
        "recomputed; R14 HA01b-recomputed NOT-SUPPORTED single-pool descriptively corroborated in "
        "Q3.7.f; HA-C4c heavy-T classifier framing in Q3.7.g; activity-labels partial-coverage "
        "descriptively referenced in Q3.7.h. NO substantive HA verdict promotion per CONVENTIONS "
        "section 2.1; NO re-litigation of v3.1 -> v3.2 correction per handoff section 3 hard "
        "constraint.",
        "- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).",
        "",
        "## Result",
        "",
        "Headline (see [`findings.md`](findings.md) for the full answers Q3.7.a-i):",
        "",
        "`exertion_class` on Stratum 4 is a **5-level categorical activity-axis channel** "
        "(distribution: {0}; Shannon entropy = {1:.3f} nats = {2:.1%} of max log(5); "
        "heavy+very_heavy spike-class fraction = {3:.1%}; at-rest none-class fraction = {4:.1%}). "
        "**{5}** on ordinal-encoded series (transition rate = {6:.1%}). **Per-citalopram-phase**: "
        "chi-square(df={7}) = {8:.2f}, p={9}; heavy+very_heavy fraction unmedicated {10:.1%} -> "
        "consolidation {11:.1%} -> afbouw {12:.1%}. **Crash-vs-normal**: chi-square 2x5 = {13:.2f} "
        "p={14}; MWU on ordinal z={15:+.2f} p={16}; heavy+very_heavy fraction diff = {17:+.1%}; "
        "ordinal median diff = {18:+.1f}; episode-level Cohen's d on ordinal = {19:+.2f} -- "
        "descriptively re-anchors HA01b-recomputed locked-REFUTED + R14 +5.1 pp NOT-SUPPORTED and "
        "HA01c locked-SUPPORTED-load-bearing-WITHHELD signals at the un-lagged-primary day-level "
        "read. **Spike-form**: heavy+very_heavy burst-rate (>=2 spike days in trailing 7d) = "
        "{20:.1%}; max consecutive heavy+very_heavy run = {21} days; HA-C4c uses the lagged "
        "variant for its heavy-T classifier per hypothesis.md section 4.1. Near-identity check: "
        "**{22}** pair(s) fire at the |rho|>=0.92 CONVENTIONS section 3.3 threshold.".format(
            headline_class_str,
            a["shannon_entropy_nats"], a["entropy_normalised"],
            a["heavy_or_very_heavy_fraction"], a["none_fraction"],
            el_match, b["transition_rate_day_over_day"],
            d["chi_square_test"]["df"], d["chi_square_test"]["chi2"], _format_p(d["chi_square_test"]["p_value"]),
            d["per_phase_heavy_or_very_heavy_fraction"].get("unmedicated", float("nan")),
            d["per_phase_heavy_or_very_heavy_fraction"].get("consolidation", float("nan")),
            d["per_phase_heavy_or_very_heavy_fraction"].get("afbouw", float("nan")),
            chi_f["chi2"], chi_f_p_str,
            mwu["z"], mwu_p_str,
            fl["heavy_or_very_heavy_fraction_diff_crash_minus_normal"],
            fl["ordinal_median_diff_crash_minus_normal"],
            fe["cohens_d_episode_vs_normal_day_ordinal"],
            g["burst_rate_ge2_in_trailing_7d"],
            g["consecutive_heavy_run_distribution"]["max_run_length_days"],
            n_near_id_flags,
        ),
        "",
        "## Files",
        "",
        "- [`README.md`](README.md) -- this file",
        "- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + "
        "`README.md` + `plots/*.png`",
        "- [`findings.md`](findings.md) -- writeup covering Q3.7.a-i + tables (programmatically "
        "emitted by run.py from summary.json per the Q3.2/Q3.3/Q3.4/Q3.5/Q3.6 architectural note "
        "about the Write-tool harness heuristic on the literal filename \"findings\")",
        "- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per "
        "`docs/research/**/*.json`)",
        "- [`plots/`](plots/) -- 5 PNGs: per-category frequency, phase-stratified stacked bars, "
        "monthly rate trajectory with phase shading, crash-vs-normal per-category bars, ACF on "
        "ordinal encoding (gitignored per `docs/research/**/*.png`)",
        "",
        "## Status",
        "",
        "**Current as of {0} corpus + 2026-06-24 analysis** (commit context: post-`5d28219` Q3.6 "
        "resting_hr LANDED; Phase 2 'finish the descriptive analysis' Tier 2 batch 3rd of 5 "
        "channels). Refresh when:".format(summary["as_of_date"]),
        "",
        "1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is "
        "about to spin up beyond the HA01b-recomputed-locked + HA-C4c-locked operands.",
        "2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 "
        "onward).",
        "3. Politis-White E[L]\\* on ordinal encoding shifts by another factor of 2 from current "
        "{0:.1f}.".format(el_star),
        "4. activity-labels classifier definition.md severity cutoffs change (current state: cutoffs "
        "NOT locked per definition.md; Q3.7.h per-month rate-drift snapshots characterise stability "
        "AS-IS).",
        "5. A v3.3 baseline-correction or any further upstream-classifier revision lands (current "
        "state: v3.2 lagged is canonical for downstream PEM-pacing consumers per CONVENTIONS "
        "section 3.2).",
        "",
        "## Cross-references",
        "",
        "- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 "
        "2026-06-18, commit `ccbd12e`)",
        "- **LOAD-BEARING canonical correction example**: [`REJECTED.md`](../../../REJECTED.md) "
        "HA01b-recomputed row + [CONVENTIONS section 3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses); "
        "Q3.7.b cites descriptively (NOT re-litigated per handoff section 3 hard constraint).",
        "- **Q3.6 most-recent Tier 2 precedent**: [`descriptive/operationalisation_support/resting_hr/`](../resting_hr/) "
        "-- Tier 2 2nd of 5; programmatic-emit pattern + clean f-string discipline.",
        "- **Q3.5 Tier 2 first precedent**: [`descriptive/operationalisation_support/bb_overnight_gain/`](../bb_overnight_gain/) "
        "-- Tier 2 1st of 5; load-bearing cross-reference template.",
        "- **Non-continuous-primitive adaptation precedent**: [`descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/`](../stress_low_motion_min_count_S60_Mlow/) "
        "-- count-primitive adaptation precedent; model for CATEGORICAL ADAPTATION discipline in "
        "this Q3.7.",
        "- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) "
        "-- HA01b-recomputed row descriptively corroborated in Q3.7.f.",
        "- **Partial-coverage activity-labels artefact**: [`analyses/garmin_exploration/activity-labels/`](../../../analyses/garmin_exploration/activity-labels/) "
        "-- existing primitive validation + visualisation; descriptively referenced in Q3.7.h.",
        "- **HA-* tests that this analysis anchors**:",
        "  - **HA01b-recomputed** (LOCKED REFUTED both eras +5.8 / +4.0; R14 single-pool NOT-"
        "SUPPORTED CONVERGE); primary operand on lagged variant of this channel.",
        "  - **HA01b-per-axis-diagnostic** (LOCKED SUPPORTED both eras at tau=0.75; load-bearing "
        "WITHHELD); per-axis read on lagged variant of this channel.",
        "  - **HA01c-effective-exertion-shock** (LOCKED SUPPORTED both eras at tau=0.75; load-"
        "bearing WITHHELD); uses eff_exertion_rank_lagged.",
        "  - **HA-C4c** (LANDED PARTIAL `a69a8ed`): uses exertion_class_lagged_lcera in {heavy, "
        "very_heavy} as heavy-T classifier on T.",
        "- **Methodology MDs**: `citalopram_phase_stratification.md`, `permutation_null_block_length.md`, "
        "`lc_era_temporal_segmentation.md`, `garmin_indicators_audit.md`, `_descriptive_stocktake_"
        "2026-06-23.md` (gap-list framing).",
        "- **Upstream pipeline**: `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_"
        "dataset.py` <- activity-axis upstream classifier producing exertion_class per `analyses/"
        "garmin_exploration/activity-labels/definition.md` severity cutoffs. `labels_crash_v2.csv` "
        "per locked `crash_v2-definition`.",
        "",
    ]

    path.write_text("\n".join(out_lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 70)
    print("Q3.7 exertion_class operationalisation-support descriptive (Tier 2 3rd of 5)")
    print("=" * 70)
    print()

    df_full = load_master(as_of_date=AS_OF_DATE, stratum_4_only=False)
    print("Loaded per_day_master.csv: {0} rows total (as_of {1})".format(
        len(df_full), AS_OF_DATE,
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

    if CHANNEL not in df.columns:
        raise SystemExit(
            "Channel {0!r} missing from per_day_master.csv; check column name + pipeline output".format(CHANNEL),
        )

    print()
    print("Computing Q3.7.a-i (CATEGORICAL ADAPTATIONS)...")

    values_s4 = df[CHANNEL]
    a_res = q_a_distribution(values_s4)
    print("  Q3.7.a: n={0}, entropy={1:.3f} nats ({2:.1%} of log5); heavy+very_heavy={3:.1%}".format(
        a_res["n"], a_res["shannon_entropy_nats"], a_res["entropy_normalised"],
        a_res["heavy_or_very_heavy_fraction"],
    ))

    b_res = q_b_autocorrelation(values_s4)
    print("  Q3.7.b: E[L]*={0:.2f} (ordinal); transition_rate={1:.1%}; M={2}".format(
        b_res["data_driven_E_L_star"], b_res["transition_rate_day_over_day"],
        b_res["cutoff_lag_M"],
    ))

    c_res = q_c_base_rates_per_phase(df, CHANNEL)
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw"):
        info = c_res.get(ph, {})
        if info.get("n", 0) > 0:
            print("  Q3.7.c [{0}]: n={1}, heavy+vh={2:.1%}, entropy={3:.3f}".format(
                ph, info["n"], info["heavy_or_very_heavy_fraction"],
                info["shannon_entropy_nats"],
            ))
        else:
            print("  Q3.7.c [{0}]: n=0".format(ph))

    d_res = q_d_phase_stratified(c_res, CHANNEL)
    chi = d_res["chi_square_test"]
    print("  Q3.7.d: chi-square = {0:.2f} (df={1}), p={2}".format(
        chi["chi2"], chi["df"], _format_p(chi["p_value"]),
    ))

    e_res = q_e_near_identity(df, CHANNEL)
    print("  Q3.7.e: {0} near-identity pairs at |rho|>={1}".format(
        len(e_res["flagged_pairs"]), e_res["threshold"],
    ))

    f_res = q_f_crash_vs_normal(df, CHANNEL)
    fl = f_res["day_level"]
    fe = f_res["episode_level"]
    chi_f = fl["chi_square_2x5_test"]
    mwu = fl["mann_whitney_u_on_ordinal"]
    print("  Q3.7.f: chi-sq 2x5 = {0:.2f} p={1}; MWU z={2:+.2f} p={3}; heavy+vh diff = {4:+.1%}".format(
        chi_f["chi2"], _format_p(chi_f["p_value"]),
        mwu["z"], _format_p(mwu["p_two_sided"]),
        fl["heavy_or_very_heavy_fraction_diff_crash_minus_normal"],
    ))
    print("           episode d (ordinal) = {0:+.2f} CI95 [{1:+.2f}, {2:+.2f}]".format(
        fe["cohens_d_episode_vs_normal_day_ordinal"],
        fe["bootstrap_ci95_mean_diff_ordinal"][0],
        fe["bootstrap_ci95_mean_diff_ordinal"][1],
    ))

    g_res = q_g_spike_primitive(df, CHANNEL)
    print("  Q3.7.g: heavy+vh rate = {0:.1%}; burst rate >=2/7d = {1:.1%}; max run = {2} days".format(
        g_res["heavy_or_very_heavy_rate"], g_res["burst_rate_ge2_in_trailing_7d"],
        g_res["consecutive_heavy_run_distribution"]["max_run_length_days"],
    ))

    h_res = q_h_outliers_calibration(df, CHANNEL)
    print("  Q3.7.h: rare-class flag = {0}; {1} monthly snapshots".format(
        a_res["rare_class_flag_min_freq_lt_0p05"],
        len(h_res["monthly_rate_snapshots"]),
    ))

    i_res = q_i_covariate_readiness(df, CHANNEL)
    print("  Q3.7.i: {0} candidate covariates named".format(len(i_res["candidate_covariates"])))

    summary = {
        "channel": CHANNEL,
        "as_of_date": AS_OF_DATE,
        "n_rows_full_corpus_to_as_of": int(len(df_full)),
        "n_rows_stratum_4_total": n_s4,
        "questions": {
            "Q3.7.a_distribution": a_res,
            "Q3.7.b_autocorrelation": b_res,
            "Q3.7.c_base_rates_per_phase": c_res,
            "Q3.7.d_phase_stratified_distribution": d_res,
            "Q3.7.e_near_identity": e_res,
            "Q3.7.f_crash_vs_normal": f_res,
            "Q3.7.g_spike_primitive": g_res,
            "Q3.7.h_outliers_calibration": h_res,
            "Q3.7.i_covariate_readiness": i_res,
        },
    }

    summary_path = HERE / "summary.json"

    # Make JSON-serialisable (numpy types + numpy arrays -> Python types)
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
    print("Done. Q3.7 LANDED (Tier 2 3rd of 5; resting_hr done; next: push_burden_7d).")


if __name__ == "__main__":
    main()
