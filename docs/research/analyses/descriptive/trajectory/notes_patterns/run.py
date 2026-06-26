"""Descriptive analysis: trajectory/notes_patterns -- Q4.7 note-categorisation
patterns under the strict symptom-mention-asymmetry discipline per
methodology/symptom_mention_asymmetry.md LOCKED 2026-06-11.

Strand B Tier-3 deferred topic 2 of 2 (Q4.8 seasonality_dow is the other,
landed e4db6cc 2026-06-26). The FINAL Strand B topic before the
/research-interpret skill pivot.

User-LOCKED operationalisation (per Strand B section 7c interview
2026-06-26; do NOT iterate):

1. Scope = ALL v24 categorical columns (per data dictionary section 9 +
   section 10): 5 belasting clusters + 3 symptoom clusters + 3 state_symptoom
   categorical + 4 ancillary (medicatie, recovery_actie, triggers_extern,
   neutral_forward_looking_flag) + day_dominant_polarity + n_clauses +
   has_note (the daily_computed gating flag itself).
2. Write-rate dimensions = ALL: per-recovery-phase + per-citalopram-phase +
   per-DOW + per-month + has_note <-> gevoelscore correlation.
3. Stratifications = ALL: per-recovery-phase + per-citalopram-phase +
   per-event-class (crash vs dip vs normal per Q4.4) + per-Q4.3-boundary
   +/-30d windows on the 6 strong boundaries (rp1-rp5 + cp3).
4. Trajectory framing = conditional-on-note share ONLY (cleanest per the
   asymmetry discipline). Absolute mention-rate trajectories are EXCLUDED.

CRITICAL DISCIPLINE per symptom_mention_asymmetry.md (LOAD-BEARING):

- v24 cat_* columns are presence_conditioned_positive_evidence. A mention
  is high-specificity positive evidence; absence of mention is NOT evidence
  of absence (5 distinct causes; only one is symptom-absent).
- v24 CANNOT do prevalence trajectories (mention-rate confounded with
  note-writing-rate).
- v24 CAN do stratify-by-content + conditional-on-note share.
- has_note IS daily_computed -- its trajectory IS clean.

Layer A (write-rate; daily_computed; trajectory-clean):
- Stage 1: data prep (load per_day_master; restrict to gevoelscore-coverage
  era 2022-09-03 -> 2026-06-04; identify recovery_phase + citalopram_phase
  + month + DOW per row).
- Stage 2: write-rate per-recovery-phase.
- Stage 3: write-rate per-citalopram-phase.
- Stage 4: write-rate per-DOW + KW + weekday-vs-weekend MWU (Q4.8 sister).
- Stage 5: write-rate per-month + KW (Q4.8 sister).
- Stage 6: has_note <-> gevoelscore correlation (contingency + Spearman
  rho on shared-coverage days).

Layer B (within-note share; presence_conditioned; conditional-on-note ONLY):
- Stage 7: per-cluster within-note share per-recovery-phase.
- Stage 8: per-cluster within-note share per-citalopram-phase.
- Stage 9: per-cluster within-note share per-event-class (crash vs dip vs
  normal per Q4.4 is_crash + is_dip).
- Stage 10: per-cluster within-note share per-Q4.3-boundary +/-30d window
  (6 boundaries: rp1-rp5 + cp3).

Layer C (output + emit):
- Stage 11: 4+ output artefacts (write-rate summary + conditional-share
  heatmap + per-event-class table + per-boundary +/-30d table).
- Stage 12: programmatic emit findings.md + README.md + summary.json.

Discipline guards:
- ASCII-only stdout; no em-dashes; no emojis.
- f-string discipline: no nested double-quotes inside expressions; use
  format() or extract-to-variable.
- Per CONVENTIONS section 2.1 + section 4.2: Layer-B findings reported as
  'share-of-clauses on cluster X is Y conditional-on-note in phase Z' --
  NEVER 'cluster X is more prevalent in phase Z'.
- The 5-cause-of-absence rule (per asymmetry MD section 2) invoked at every
  Layer-B reading.
- NO causal claims; NO prevalence claims; NO HA verdict promotion.

Output (all but findings.md + README.md + run.py gitignored):
- summary.json -- machine-readable per-stage statistics
- plots/write_rate_per_phase.png -- Layer A bar (recovery + citalopram phases)
- plots/write_rate_dow_month.png -- Layer A DOW + month grid
- plots/conditional_share_heatmap.png -- Layer B cluster x phase
- plots/per_event_class_table.png -- Layer B crash vs dip vs normal
- plots/per_boundary_pre_post.png -- Layer B per-Q4.3-boundary +/-30d
- findings.md -- programmatic emit
- README.md -- programmatic emit
"""

from __future__ import annotations

import json
import math
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats as scistats


HERE = Path(__file__).resolve().parent
# HERE = .../analyses/descriptive/trajectory/notes_patterns
# parents[0]=trajectory, [1]=descriptive, [2]=analyses
UTILS_DIR = HERE.parents[2] / "_utils"
sys.path.insert(0, str(UTILS_DIR))

from frame import load_master  # noqa: E402


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


AS_OF_DATE = "2026-06-04"
GEVOELSCORE_COVERAGE_START = "2022-09-03"  # Stratum 4 left edge
# has_note first non-zero date in corpus: 2022-10-18 (within Stratum 4)

# Six phases per lc_recovery_phase_axis.md section 2 (LOCKED d47e0d3 2026-06-19)
RECOVERY_PHASE_ORDER = [
    "pre_illness_healthy",
    "acute_infection",
    "lc_pre_ergo",
    "pacing_pre_citalopram_learning",
    "pacing_habit_established",
    "citalopram_modulated",
]

# Citalopram phase order per citalopram_phase_stratification.md section 3
CITALOPRAM_PHASE_ORDER = [
    "unmedicated",
    "buildup",
    "consolidation",
    "afbouw",
    "post_afbouw",
]

# Q4.3 6 strong boundaries per era_boundaries/findings.md section 1
Q43_BOUNDARIES = [
    ("rp1_pre_illness_to_acute", "2022-03-21"),
    ("rp2_acute_to_lc_pre_ergo", "2022-04-04"),
    ("rp3_lc_pre_ergo_to_4a", "2022-09-22"),
    ("rp4_4a_to_4b", "2022-11-17"),
    ("rp5_4b_to_citalopram_modulated", "2024-04-09"),
    ("cp3_consolidation_to_afbouw", "2026-03-20"),
]
BOUNDARY_HALF_WINDOW_DAYS = 30

# v24 categorical columns per data dictionary section 9 + section 10.
# Layer B operates ONLY on numeric count clusters (we need shares = count
# / n_clauses). day_dominant_polarity + state_symptoom_* are categorical
# (positive/neutral/negative/mixed; absent/mild/present/severe) so they
# receive a separate within-note CATEGORICAL distribution table.
# neutral_forward_looking_flag is boolean -> rate-conditional-on-note.

V24_COUNT_CLUSTERS = [
    # 5 belasting clusters
    "cat_belasting_cognitief",
    "cat_belasting_emotioneel",
    "cat_belasting_fysiek",
    "cat_belasting_gezin",
    "cat_belasting_sociaal",
    # 3 symptoom clusters
    "cat_symptoom_cognitief",
    "cat_symptoom_emotioneel",
    "cat_symptoom_fysiek",
    # 3 ancillary count clusters
    "cat_medicatie",
    "cat_recovery_actie",
    "cat_triggers_extern",
    # context residual (descriptive substrate)
    "cat_context_neutraal",
]

V24_STATE_CATEGORICAL = [
    # 3 state_symptoom severity categoricals
    # categories: absent / mild / present / severe
    "state_symptoom_cognitief",
    "state_symptoom_emotioneel",
    "state_symptoom_fysiek",
]
STATE_CATEGORIES = ["absent", "mild", "present", "severe"]

V24_DAY_DOMINANT = "day_dominant_polarity"
DAY_DOMINANT_CATEGORIES = ["positive", "neutral", "negative", "mixed"]

V24_BOOLEAN_FLAG = "neutral_forward_looking_flag"

V24_AUXILIARY = ["n_clauses", "has_note"]

WEEKEND_DOWS = {5, 6}
DOW_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

# Thresholds (descriptive flags only, NOT verdicts)
KW_SUSPECT_THRESHOLD = 0.05
MWU_SUSPECT_THRESHOLD = 0.05
SPEARMAN_SUSPECT_THRESHOLD = 0.05
SEED = 20260626


# -----------------------------------------------------------------------------
# Helpers (citalopram_phase per citalopram_phase_stratification.md section 3;
# event-class derivation per Q4.4)
# -----------------------------------------------------------------------------


def citalopram_phase(d: pd.Timestamp) -> str:
    """Per citalopram_phase_stratification.md section 3."""
    py = d.to_pydatetime().date() if hasattr(d, "to_pydatetime") else d
    if py < date(2024, 4, 9):
        return "unmedicated"
    if py < date(2024, 6, 20):
        return "buildup"
    if py < date(2026, 3, 20):
        return "consolidation"
    if py < date(2026, 6, 6):
        return "afbouw"
    return "post_afbouw"


def event_class(row) -> str:
    """Per Q4.4 cohort_topology event-class definitions.

    is_crash + is_dip are mutually exclusive (crash_v2 section 2.2: dips are
    single-day events DISTINCT from crash episodes).
    """
    if bool(row.get("is_crash", False)):
        return "crash"
    if bool(row.get("is_dip", False)):
        return "dip"
    return "normal"


def fmt_float(v, ndp=3, default="n/a"):
    if v is None:
        return default
    try:
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return default
    except (TypeError, ValueError):
        return default
    fmt = "{:." + str(ndp) + "f}"
    return fmt.format(v)


def fmt_pct(v, ndp=1, default="n/a"):
    if v is None:
        return default
    try:
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return default
    except (TypeError, ValueError):
        return default
    fmt = "{:." + str(ndp) + "f}"
    return fmt.format(100.0 * v) + "%"


# -----------------------------------------------------------------------------
# Stage 1 -- data prep
# -----------------------------------------------------------------------------


def stage_1_load_data():
    print("=" * 70)
    print("STAGE 1: data prep (load per_day_master + identify covariates)")
    print("=" * 70)
    df = load_master(as_of_date=AS_OF_DATE)
    df = df.copy()
    df["date_dt"] = pd.to_datetime(df["date"])
    # Restrict to gevoelscore-coverage era (Stratum 4 start; has_note era is
    # a subset and starts within Stratum 4 at 2022-10-18 first non-zero).
    cov_start = pd.Timestamp(GEVOELSCORE_COVERAGE_START)
    df = df[df["date_dt"] >= cov_start].copy()
    df["has_note"] = df["has_note"].astype(bool)
    df["month"] = df["date_dt"].dt.month
    df["dow"] = df["date_dt"].dt.dayofweek
    df["is_weekend"] = df["dow"].isin(WEEKEND_DOWS)
    df["citalopram_phase"] = df["date_dt"].apply(citalopram_phase)
    df["event_class"] = df.apply(event_class, axis=1)

    print(f"  loaded n_rows={len(df)} (Stratum 4: {GEVOELSCORE_COVERAGE_START} -> {AS_OF_DATE})")
    n_has_note = int(df["has_note"].sum())
    print(f"  has_note=True: {n_has_note} / {len(df)} ({100.0*n_has_note/len(df):.1f}%)")
    print(f"  first has_note=True date: {df.loc[df['has_note'], 'date_dt'].min().date()}")
    print(f"  last  has_note=True date: {df.loc[df['has_note'], 'date_dt'].max().date()}")
    print("  recovery_phase distribution:")
    for ph in RECOVERY_PHASE_ORDER:
        n_ph = int((df["recovery_phase"] == ph).sum())
        n_ph_note = int(((df["recovery_phase"] == ph) & df["has_note"]).sum())
        print(f"    {ph}: n_days={n_ph} n_notes={n_ph_note}")
    print("  citalopram_phase distribution:")
    for ph in CITALOPRAM_PHASE_ORDER:
        n_ph = int((df["citalopram_phase"] == ph).sum())
        n_ph_note = int(((df["citalopram_phase"] == ph) & df["has_note"]).sum())
        print(f"    {ph}: n_days={n_ph} n_notes={n_ph_note}")
    print("  event_class distribution:")
    for ec in ("crash", "dip", "normal"):
        n_ec = int((df["event_class"] == ec).sum())
        n_ec_note = int(((df["event_class"] == ec) & df["has_note"]).sum())
        print(f"    {ec}: n_days={n_ec} n_notes={n_ec_note}")
    print()
    return df


# -----------------------------------------------------------------------------
# Stage 2 -- write-rate per-recovery-phase (Layer A; daily_computed)
# -----------------------------------------------------------------------------


def write_rate_by_group(df, group_col, group_order):
    """Per group: P(has_note=True), n_days, n_notes."""
    rows = []
    for g in group_order:
        sub = df[df[group_col] == g]
        n_days = int(len(sub))
        n_notes = int(sub["has_note"].sum())
        rate = float(n_notes / n_days) if n_days > 0 else float("nan")
        rows.append({"group": g, "n_days": n_days, "n_notes": n_notes, "write_rate": rate})
    return rows


def stage_2_writerate_recovery(df):
    print("=" * 70)
    print("STAGE 2: write-rate per-recovery-phase (Layer A; daily_computed)")
    print("=" * 70)
    rows = write_rate_by_group(df, "recovery_phase", RECOVERY_PHASE_ORDER)
    for r in rows:
        print(
            f"  {r['group']}: P(has_note)={fmt_pct(r['write_rate'])} "
            f"(n_notes={r['n_notes']} / n_days={r['n_days']})"
        )
    print()
    return rows


# -----------------------------------------------------------------------------
# Stage 3 -- write-rate per-citalopram-phase (Layer A)
# -----------------------------------------------------------------------------


def stage_3_writerate_citalopram(df):
    print("=" * 70)
    print("STAGE 3: write-rate per-citalopram-phase (Layer A; daily_computed)")
    print("=" * 70)
    rows = write_rate_by_group(df, "citalopram_phase", CITALOPRAM_PHASE_ORDER)
    for r in rows:
        print(
            f"  {r['group']}: P(has_note)={fmt_pct(r['write_rate'])} "
            f"(n_notes={r['n_notes']} / n_days={r['n_days']})"
        )
    print()
    return rows


# -----------------------------------------------------------------------------
# Stage 4 -- write-rate per-DOW (Layer A; Q4.8 sister)
# -----------------------------------------------------------------------------


def stage_4_writerate_dow(df):
    print("=" * 70)
    print("STAGE 4: write-rate per-DOW (Layer A; Q4.8 sister on has_note)")
    print("=" * 70)
    # Per-DOW rate
    per_dow = []
    for d_ in range(7):
        sub = df[df["dow"] == d_]
        n_days = int(len(sub))
        n_notes = int(sub["has_note"].sum())
        rate = float(n_notes / n_days) if n_days > 0 else float("nan")
        per_dow.append({
            "dow": d_, "name": DOW_NAMES[d_], "n_days": n_days,
            "n_notes": n_notes, "write_rate": rate,
        })
    # KW across 7 groups -- each group is a Bernoulli sample of length n_days;
    # use chi-square contingency 2x7 instead of KW (more natural for binary).
    contingency = np.zeros((2, 7), dtype=int)  # row 0 = no_note; row 1 = note
    for d_ in range(7):
        sub = df[df["dow"] == d_]
        contingency[1, d_] = int(sub["has_note"].sum())
        contingency[0, d_] = int(len(sub) - sub["has_note"].sum())
    try:
        chi2_stat, chi2_p, dof, _expected = scistats.chi2_contingency(contingency)
        chi2_stat = float(chi2_stat)
        chi2_p = float(chi2_p)
        dof = int(dof)
    except Exception as exc:
        print(f"  chi2 failed -- {exc}")
        chi2_stat, chi2_p, dof = float("nan"), float("nan"), -1
    # Weekday-vs-weekend MWU (treating has_note as 0/1 Bernoulli, this is
    # equivalent to a proportion test; we use chi-square 2x2 for clarity)
    we_contingency = np.zeros((2, 2), dtype=int)
    for is_we in (False, True):
        sub = df[df["is_weekend"] == is_we]
        idx = 1 if is_we else 0
        we_contingency[1, idx] = int(sub["has_note"].sum())
        we_contingency[0, idx] = int(len(sub) - sub["has_note"].sum())
    try:
        we_chi2, we_p, _, _ = scistats.chi2_contingency(we_contingency)
        we_chi2 = float(we_chi2)
        we_p = float(we_p)
    except Exception as exc:
        print(f"  weekend chi2 failed -- {exc}")
        we_chi2, we_p = float("nan"), float("nan")
    n_wd = int(df.loc[~df["is_weekend"]].shape[0])
    n_we = int(df.loc[df["is_weekend"]].shape[0])
    rate_wd = float(df.loc[~df["is_weekend"], "has_note"].mean())
    rate_we = float(df.loc[df["is_weekend"], "has_note"].mean())

    for r in per_dow:
        print(
            f"  {r['name']}: P(has_note)={fmt_pct(r['write_rate'])} "
            f"(n_notes={r['n_notes']} / n_days={r['n_days']})"
        )
    kw_flag = "SUSPECT" if (not math.isnan(chi2_p) and chi2_p < KW_SUSPECT_THRESHOLD) else "no-flag"
    print(
        f"  chi2 across 7 days: chi2={fmt_float(chi2_stat, 2)} dof={dof} "
        f"p={fmt_float(chi2_p, 4)} [{kw_flag}]"
    )
    we_flag = "SUSPECT" if (not math.isnan(we_p) and we_p < MWU_SUSPECT_THRESHOLD) else "no-flag"
    print(
        f"  weekday-vs-weekend (chi2 2x2): P(weekday)={fmt_pct(rate_wd)} "
        f"(n={n_wd}) vs P(weekend)={fmt_pct(rate_we)} (n={n_we}) "
        f"chi2={fmt_float(we_chi2, 2)} p={fmt_float(we_p, 4)} [{we_flag}]"
    )
    print()
    return {
        "per_dow": per_dow,
        "kw_chi2": chi2_stat, "kw_p": chi2_p, "kw_dof": dof,
        "weekend_chi2": we_chi2, "weekend_p": we_p,
        "rate_weekday": rate_wd, "rate_weekend": rate_we,
        "n_weekday": n_wd, "n_weekend": n_we,
    }


# -----------------------------------------------------------------------------
# Stage 5 -- write-rate per-month (Layer A; Q4.8 sister)
# -----------------------------------------------------------------------------


def stage_5_writerate_month(df):
    print("=" * 70)
    print("STAGE 5: write-rate per-month (Layer A; Q4.8 sister on has_note)")
    print("=" * 70)
    per_month = []
    for m in range(1, 13):
        sub = df[df["month"] == m]
        n_days = int(len(sub))
        n_notes = int(sub["has_note"].sum())
        rate = float(n_notes / n_days) if n_days > 0 else float("nan")
        per_month.append({
            "month": m, "name": MONTH_NAMES[m - 1], "n_days": n_days,
            "n_notes": n_notes, "write_rate": rate,
        })
    contingency = np.zeros((2, 12), dtype=int)
    for m in range(1, 13):
        sub = df[df["month"] == m]
        contingency[1, m - 1] = int(sub["has_note"].sum())
        contingency[0, m - 1] = int(len(sub) - sub["has_note"].sum())
    try:
        chi2_stat, chi2_p, dof, _exp = scistats.chi2_contingency(contingency)
        chi2_stat = float(chi2_stat)
        chi2_p = float(chi2_p)
        dof = int(dof)
    except Exception as exc:
        print(f"  chi2 failed -- {exc}")
        chi2_stat, chi2_p, dof = float("nan"), float("nan"), -1
    for r in per_month:
        print(
            f"  {r['name']}: P(has_note)={fmt_pct(r['write_rate'])} "
            f"(n_notes={r['n_notes']} / n_days={r['n_days']})"
        )
    kw_flag = "SUSPECT" if (not math.isnan(chi2_p) and chi2_p < KW_SUSPECT_THRESHOLD) else "no-flag"
    print(
        f"  chi2 across 12 months: chi2={fmt_float(chi2_stat, 2)} dof={dof} "
        f"p={fmt_float(chi2_p, 4)} [{kw_flag}]"
    )
    print()
    return {
        "per_month": per_month,
        "kw_chi2": chi2_stat, "kw_p": chi2_p, "kw_dof": dof,
    }


# -----------------------------------------------------------------------------
# Stage 6 -- has_note <-> gevoelscore correlation (Layer A)
# -----------------------------------------------------------------------------


def stage_6_correlation(df):
    print("=" * 70)
    print("STAGE 6: has_note <-> gevoelscore correlation (Layer A)")
    print("=" * 70)
    # has_score is daily_computed too; condition on has_score=True for clean
    # gevoelscore values (otherwise gevoelscore is NaN by definition).
    df_score = df[df["has_score"].astype(bool)].copy()
    print(f"  shared-coverage rows (has_score=True): {len(df_score)} / {len(df)}")
    # Contingency: rows of score values vs has_note bool
    if len(df_score) < 30:
        print("  insufficient n for correlation; skipping")
        print()
        return None
    # Score quantile bins per CONVENTIONS section 4.2 caveat-class
    # (descriptive ordinal vs binary; bin score 1-2 / 3 / 4-5 for table)
    bins = [(0.5, 2.5, "low_1_2"), (2.5, 3.5, "mid_3"), (3.5, 5.5, "high_4_5")]
    cont_rows = []
    for lo, hi, name in bins:
        sub = df_score[(df_score["gevoelscore"] >= lo) & (df_score["gevoelscore"] < hi)]
        n = int(len(sub))
        n_note = int(sub["has_note"].sum())
        rate = float(n_note / n) if n > 0 else float("nan")
        cont_rows.append({"bin": name, "n_days": n, "n_notes": n_note, "write_rate": rate})
        print(
            f"  score {name}: P(has_note)={fmt_pct(rate)} "
            f"(n_notes={n_note} / n_days={n})"
        )
    # Spearman rho of gevoelscore vs has_note (0/1) on shared-coverage rows
    try:
        rho, p_rho = scistats.spearmanr(
            df_score["gevoelscore"].astype(float),
            df_score["has_note"].astype(int),
        )
        rho = float(rho)
        p_rho = float(p_rho)
    except Exception as exc:
        print(f"  Spearman failed -- {exc}")
        rho, p_rho = float("nan"), float("nan")
    # Chi-square 2x3 (no_note/note x low/mid/high)
    cont_2x3 = np.zeros((2, len(bins)), dtype=int)
    for i, (lo, hi, _name) in enumerate(bins):
        sub = df_score[(df_score["gevoelscore"] >= lo) & (df_score["gevoelscore"] < hi)]
        cont_2x3[1, i] = int(sub["has_note"].sum())
        cont_2x3[0, i] = int(len(sub) - sub["has_note"].sum())
    try:
        chi2, p_chi, dof, _exp = scistats.chi2_contingency(cont_2x3)
        chi2 = float(chi2)
        p_chi = float(p_chi)
        dof = int(dof)
    except Exception as exc:
        print(f"  chi2 failed -- {exc}")
        chi2, p_chi, dof = float("nan"), float("nan"), -1
    sp_flag = "SUSPECT" if (not math.isnan(p_rho) and p_rho < SPEARMAN_SUSPECT_THRESHOLD) else "no-flag"
    chi_flag = "SUSPECT" if (not math.isnan(p_chi) and p_chi < KW_SUSPECT_THRESHOLD) else "no-flag"
    print(
        f"  Spearman rho(gevoelscore, has_note) = {fmt_float(rho, 4)}  "
        f"p={fmt_float(p_rho, 4)}  [{sp_flag}]"
    )
    print(
        f"  chi2 2x3 (note x score-tertile): chi2={fmt_float(chi2, 2)} "
        f"dof={dof} p={fmt_float(p_chi, 4)} [{chi_flag}]"
    )
    print(
        "  reading: DESCRIPTIVE only; does NOT imply low-score causes "
        "writing or vice versa per CONVENTIONS section 4.2."
    )
    print()
    return {
        "n_shared": int(len(df_score)),
        "per_score_bin": cont_rows,
        "spearman_rho": rho, "spearman_p": p_rho,
        "chi2": chi2, "chi2_p": p_chi, "chi2_dof": dof,
    }


# -----------------------------------------------------------------------------
# Stage 7 + 8 + 9 + 10 -- Layer B: conditional-on-note share helpers
# -----------------------------------------------------------------------------


def within_note_share_table(df_notes, group_col, group_order, count_clusters):
    """For each group: mean(count_cluster / n_clauses) over has_note=True rows.

    Returns dict[group][cluster] -> {mean_share, n_notes, mean_count}.
    Per the asymmetry MD: 'share-of-clauses on cluster X is Y conditional-on-
    note in group Z'. Does NOT imply prevalence of cluster X in group Z.
    """
    out = {}
    for g in group_order:
        sub = df_notes[df_notes[group_col] == g]
        n = int(len(sub))
        per_cluster = {}
        for c in count_clusters:
            if n == 0 or sub["n_clauses"].sum() == 0:
                per_cluster[c] = {
                    "mean_share": float("nan"),
                    "n_notes": n,
                    "mean_count": float("nan"),
                    "total_count": 0,
                }
                continue
            # mean of per-day share (each day weighted equally), per asymmetry MD
            shares = sub[c].astype(float) / sub["n_clauses"].astype(float)
            shares = shares.replace([np.inf, -np.inf], np.nan).dropna()
            mean_share = float(shares.mean()) if len(shares) > 0 else float("nan")
            mean_count = float(sub[c].mean())
            total = int(sub[c].sum())
            per_cluster[c] = {
                "mean_share": mean_share,
                "n_notes": n,
                "mean_count": mean_count,
                "total_count": total,
            }
        out[g] = per_cluster
    return out


def within_note_categorical_distribution(df_notes, group_col, group_order, cat_col, cat_levels):
    """For each group: P(cat_col == level) over has_note=True rows.

    cat_col is presence_conditioned (only defined on has_note=True days).
    """
    out = {}
    for g in group_order:
        sub = df_notes[df_notes[group_col] == g]
        # Drop NaN cat_col rows (asymmetry: state-symptoom categorical is
        # presence-conditioned on note + on whether the note mentioned a
        # state. Where it's NaN, the cluster wasn't mentioned at all in
        # the note; per the 5-cause rule we can't equate that to 'absent'.)
        s = sub[cat_col].dropna()
        n_with_value = int(len(s))
        n_notes_in_group = int(len(sub))
        per_level = {}
        if n_with_value == 0:
            for lvl in cat_levels:
                per_level[lvl] = {"count": 0, "share_of_with_value": float("nan"), "share_of_notes": float("nan")}
        else:
            for lvl in cat_levels:
                count = int((s == lvl).sum())
                per_level[lvl] = {
                    "count": count,
                    "share_of_with_value": float(count / n_with_value),
                    "share_of_notes": float(count / n_notes_in_group) if n_notes_in_group else float("nan"),
                }
        out[g] = {
            "n_notes": n_notes_in_group,
            "n_with_value": n_with_value,
            "per_level": per_level,
        }
    return out


def within_note_bool_rate(df_notes, group_col, group_order, bool_col):
    """For each group: P(bool_col == True) over has_note=True rows."""
    out = {}
    for g in group_order:
        sub = df_notes[df_notes[group_col] == g]
        s = sub[bool_col].dropna()
        if len(s) == 0:
            out[g] = {"n_notes": int(len(sub)), "n_with_value": 0, "rate": float("nan"), "n_true": 0}
            continue
        n_true = int(s.astype(bool).sum())
        out[g] = {
            "n_notes": int(len(sub)),
            "n_with_value": int(len(s)),
            "rate": float(n_true / len(s)),
            "n_true": n_true,
        }
    return out


# -----------------------------------------------------------------------------
# Stage 7 -- per-recovery-phase within-note share (Layer B)
# -----------------------------------------------------------------------------


def stage_7_share_recovery(df):
    print("=" * 70)
    print("STAGE 7: within-note share per-recovery-phase (Layer B; conditional-on-note)")
    print("  Per asymmetry MD: 'share-of-clauses on cluster X is Y conditional-on-")
    print("  note in phase Z' -- NEVER 'cluster X is more prevalent in phase Z'.")
    print("=" * 70)
    df_notes = df[df["has_note"]].copy()
    # Restrict to phases that actually have notes (pre_illness_healthy +
    # acute_infection have 0 notes per Stage 1; lc_pre_ergo has small n)
    counts_table = within_note_share_table(
        df_notes, "recovery_phase", RECOVERY_PHASE_ORDER, V24_COUNT_CLUSTERS,
    )
    state_table = {
        col: within_note_categorical_distribution(
            df_notes, "recovery_phase", RECOVERY_PHASE_ORDER, col, STATE_CATEGORIES,
        )
        for col in V24_STATE_CATEGORICAL
    }
    polarity_table = within_note_categorical_distribution(
        df_notes, "recovery_phase", RECOVERY_PHASE_ORDER, V24_DAY_DOMINANT, DAY_DOMINANT_CATEGORIES,
    )
    bool_table = within_note_bool_rate(
        df_notes, "recovery_phase", RECOVERY_PHASE_ORDER, V24_BOOLEAN_FLAG,
    )
    # Compact printout of count-share table
    print("  conditional-on-note mean share per cluster x phase:")
    header = "  cluster".ljust(34) + " | " + " | ".join(p[:8] for p in RECOVERY_PHASE_ORDER)
    print(header)
    for c in V24_COUNT_CLUSTERS:
        row = "  " + c.ljust(32) + " | "
        cells = []
        for ph in RECOVERY_PHASE_ORDER:
            cell = counts_table[ph][c]
            if math.isnan(cell["mean_share"]) or cell["n_notes"] == 0:
                cells.append("n/a    ")
            else:
                cells.append(fmt_pct(cell["mean_share"], 1).rjust(7))
        print(row + " | ".join(cells))
    # boolean flag
    print("  conditional-on-note rate for neutral_forward_looking_flag:")
    for ph in RECOVERY_PHASE_ORDER:
        c = bool_table[ph]
        if c["n_with_value"] == 0:
            print(f"    {ph}: n/a (n_notes={c['n_notes']})")
        else:
            print(
                f"    {ph}: rate={fmt_pct(c['rate'])} "
                f"(n_true={c['n_true']} / n_with_value={c['n_with_value']})"
            )
    print()
    return {
        "count_clusters": counts_table,
        "state_categorical": state_table,
        "day_dominant_polarity": polarity_table,
        "boolean_flag": bool_table,
    }


# -----------------------------------------------------------------------------
# Stage 8 -- per-citalopram-phase within-note share (Layer B)
# -----------------------------------------------------------------------------


def stage_8_share_citalopram(df):
    print("=" * 70)
    print("STAGE 8: within-note share per-citalopram-phase (Layer B; conditional-on-note)")
    print("=" * 70)
    df_notes = df[df["has_note"]].copy()
    counts_table = within_note_share_table(
        df_notes, "citalopram_phase", CITALOPRAM_PHASE_ORDER, V24_COUNT_CLUSTERS,
    )
    state_table = {
        col: within_note_categorical_distribution(
            df_notes, "citalopram_phase", CITALOPRAM_PHASE_ORDER, col, STATE_CATEGORIES,
        )
        for col in V24_STATE_CATEGORICAL
    }
    polarity_table = within_note_categorical_distribution(
        df_notes, "citalopram_phase", CITALOPRAM_PHASE_ORDER, V24_DAY_DOMINANT, DAY_DOMINANT_CATEGORIES,
    )
    bool_table = within_note_bool_rate(
        df_notes, "citalopram_phase", CITALOPRAM_PHASE_ORDER, V24_BOOLEAN_FLAG,
    )
    print("  conditional-on-note mean share per cluster x citalopram_phase:")
    for c in V24_COUNT_CLUSTERS:
        row = "  " + c.ljust(32) + " | "
        cells = []
        for ph in CITALOPRAM_PHASE_ORDER:
            cell = counts_table[ph][c]
            if math.isnan(cell["mean_share"]) or cell["n_notes"] == 0:
                cells.append("n/a    ")
            else:
                cells.append(fmt_pct(cell["mean_share"], 1).rjust(7))
        print(row + " | ".join(cells))
    print()
    return {
        "count_clusters": counts_table,
        "state_categorical": state_table,
        "day_dominant_polarity": polarity_table,
        "boolean_flag": bool_table,
    }


# -----------------------------------------------------------------------------
# Stage 9 -- per-event-class within-note share (Layer B; Q4.4 sister)
# -----------------------------------------------------------------------------


def stage_9_share_event_class(df):
    print("=" * 70)
    print("STAGE 9: within-note share per-event-class (Layer B; conditional-on-note)")
    print("  Q4.4 sister: stratify by is_crash + is_dip (mutually exclusive per crash_v2 sec 2.2)")
    print("=" * 70)
    df_notes = df[df["has_note"]].copy()
    classes = ["crash", "dip", "normal"]
    counts_table = within_note_share_table(
        df_notes, "event_class", classes, V24_COUNT_CLUSTERS,
    )
    state_table = {
        col: within_note_categorical_distribution(
            df_notes, "event_class", classes, col, STATE_CATEGORIES,
        )
        for col in V24_STATE_CATEGORICAL
    }
    polarity_table = within_note_categorical_distribution(
        df_notes, "event_class", classes, V24_DAY_DOMINANT, DAY_DOMINANT_CATEGORIES,
    )
    bool_table = within_note_bool_rate(
        df_notes, "event_class", classes, V24_BOOLEAN_FLAG,
    )
    print("  conditional-on-note mean share per cluster x event_class:")
    header = "  cluster".ljust(34) + " | " + " | ".join(c.rjust(7) for c in classes)
    print(header)
    for c in V24_COUNT_CLUSTERS:
        row = "  " + c.ljust(32) + " | "
        cells = []
        for ec in classes:
            cell = counts_table[ec][c]
            if math.isnan(cell["mean_share"]) or cell["n_notes"] == 0:
                cells.append("n/a    ")
            else:
                cells.append(fmt_pct(cell["mean_share"], 1).rjust(7))
        print(row + " | ".join(cells))
    print("  conditional-on-note categorical: day_dominant_polarity:")
    for ec in classes:
        cell = polarity_table[ec]
        if cell["n_with_value"] == 0:
            print(f"    {ec}: n/a (n_notes={cell['n_notes']})")
            continue
        parts = []
        for lvl in DAY_DOMINANT_CATEGORIES:
            v = cell["per_level"][lvl]["share_of_with_value"]
            parts.append(f"{lvl}={fmt_pct(v)}")
        print(f"    {ec} (n={cell['n_with_value']}): " + " | ".join(parts))
    print("  conditional-on-note boolean flag (neutral_forward_looking):")
    for ec in classes:
        c = bool_table[ec]
        if c["n_with_value"] == 0:
            print(f"    {ec}: n/a (n_notes={c['n_notes']})")
        else:
            print(
                f"    {ec}: rate={fmt_pct(c['rate'])} "
                f"(n_true={c['n_true']} / n_with_value={c['n_with_value']})"
            )
    print()
    return {
        "count_clusters": counts_table,
        "state_categorical": state_table,
        "day_dominant_polarity": polarity_table,
        "boolean_flag": bool_table,
    }


# -----------------------------------------------------------------------------
# Stage 10 -- per-Q4.3-boundary +/-30d within-note share (Layer B)
# -----------------------------------------------------------------------------


def stage_10_share_per_boundary(df):
    print("=" * 70)
    print("STAGE 10: within-note share per Q4.3-boundary +/-30d (Layer B)")
    print(f"  half-window = {BOUNDARY_HALF_WINDOW_DAYS}d each side")
    print("=" * 70)
    df_notes = df[df["has_note"]].copy()
    out = {}
    for bname, bdate in Q43_BOUNDARIES:
        bt = pd.Timestamp(bdate)
        pre_start = bt - pd.Timedelta(days=BOUNDARY_HALF_WINDOW_DAYS)
        post_end = bt + pd.Timedelta(days=BOUNDARY_HALF_WINDOW_DAYS)
        window = df_notes[
            (df_notes["date_dt"] >= pre_start) & (df_notes["date_dt"] <= post_end)
        ].copy()
        window["side"] = window["date_dt"].apply(lambda d: "pre" if d < bt else "post")
        counts_table = within_note_share_table(
            window, "side", ["pre", "post"], V24_COUNT_CLUSTERS,
        )
        state_table = {
            col: within_note_categorical_distribution(
                window, "side", ["pre", "post"], col, STATE_CATEGORIES,
            )
            for col in V24_STATE_CATEGORICAL
        }
        polarity_table = within_note_categorical_distribution(
            window, "side", ["pre", "post"], V24_DAY_DOMINANT, DAY_DOMINANT_CATEGORIES,
        )
        bool_table = within_note_bool_rate(
            window, "side", ["pre", "post"], V24_BOOLEAN_FLAG,
        )
        n_pre = int((window["side"] == "pre").sum())
        n_post = int((window["side"] == "post").sum())
        out[bname] = {
            "boundary_date": bdate,
            "n_notes_pre": n_pre,
            "n_notes_post": n_post,
            "count_clusters": counts_table,
            "state_categorical": state_table,
            "day_dominant_polarity": polarity_table,
            "boolean_flag": bool_table,
        }
        print(f"  {bname} ({bdate}): n_notes_pre={n_pre} n_notes_post={n_post}")
        if n_pre == 0 or n_post == 0:
            print("    (skip detail: one side has no notes)")
            continue
        # Surface top-3 cluster share shifts by abs delta
        deltas = []
        for c in V24_COUNT_CLUSTERS:
            pre_v = counts_table["pre"][c]["mean_share"]
            post_v = counts_table["post"][c]["mean_share"]
            if math.isnan(pre_v) or math.isnan(post_v):
                continue
            deltas.append((c, post_v - pre_v, pre_v, post_v))
        deltas.sort(key=lambda x: abs(x[1]), reverse=True)
        for c, d_, p_, q_ in deltas[:3]:
            print(
                f"    top shift: {c}: pre={fmt_pct(p_)} post={fmt_pct(q_)} "
                f"delta={fmt_pct(d_)}"
            )
    print()
    return out


# -----------------------------------------------------------------------------
# Stage 11 -- output artefacts (plots)
# -----------------------------------------------------------------------------


def stage_11_plots(out_dir, layer_a, layer_b, layer_b_event, layer_b_boundary):
    print("=" * 70)
    print("STAGE 11: output artefacts (plots)")
    print("=" * 70)
    plots_dir = out_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(SEED)

    # Plot 1 -- write-rate per-phase bars (recovery + citalopram side-by-side)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    # Recovery
    ax = axes[0]
    rec_rows = layer_a["recovery"]
    names = [r["group"] for r in rec_rows]
    rates = [r["write_rate"] if not math.isnan(r["write_rate"]) else 0.0 for r in rec_rows]
    ns = [r["n_days"] for r in rec_rows]
    ax.bar(range(len(names)), rates, color="steelblue")
    for i, (n_, r_) in enumerate(zip(ns, rates)):
        ax.text(i, r_ + 0.01, f"n={n_}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("P(has_note)")
    ax.set_ylim(0, 1.0)
    ax.set_title("Write-rate per-recovery-phase (Layer A; daily_computed)")
    ax.grid(True, alpha=0.3, axis="y")
    # Citalopram
    ax = axes[1]
    cit_rows = layer_a["citalopram"]
    names = [r["group"] for r in cit_rows]
    rates = [r["write_rate"] if not math.isnan(r["write_rate"]) else 0.0 for r in cit_rows]
    ns = [r["n_days"] for r in cit_rows]
    ax.bar(range(len(names)), rates, color="darkorange")
    for i, (n_, r_) in enumerate(zip(ns, rates)):
        ax.text(i, r_ + 0.01, f"n={n_}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("P(has_note)")
    ax.set_ylim(0, 1.0)
    ax.set_title("Write-rate per-citalopram-phase (Layer A; daily_computed)")
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    fpath = plots_dir / "write_rate_per_phase.png"
    plt.savefig(fpath, dpi=100)
    plt.close()
    print(f"  wrote {fpath.name}")

    # Plot 2 -- write-rate per-DOW + per-month grid
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    dow_rows = layer_a["dow"]["per_dow"]
    dow_rates = [r["write_rate"] for r in dow_rows]
    colors = ["steelblue" if r["dow"] < 5 else "darkorange" for r in dow_rows]
    ax.bar(range(7), dow_rates, color=colors)
    ax.set_xticks(range(7))
    ax.set_xticklabels([r["name"] for r in dow_rows])
    ax.set_ylabel("P(has_note)")
    ax.set_ylim(0, 1.0)
    chi_p = layer_a["dow"]["kw_p"]
    ax.set_title(f"Write-rate per-DOW (chi2 p={fmt_float(chi_p, 4)}; blue=wk, orange=we)")
    ax.grid(True, alpha=0.3, axis="y")
    ax = axes[1]
    month_rows = layer_a["month"]["per_month"]
    month_rates = [r["write_rate"] for r in month_rows]
    ax.bar(range(1, 13), month_rates, color="cornflowerblue")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([r["name"] for r in month_rows], rotation=45)
    ax.set_ylabel("P(has_note)")
    ax.set_ylim(0, 1.0)
    chi_pm = layer_a["month"]["kw_p"]
    ax.set_title(f"Write-rate per-month (chi2 p={fmt_float(chi_pm, 4)})")
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    fpath = plots_dir / "write_rate_dow_month.png"
    plt.savefig(fpath, dpi=100)
    plt.close()
    print(f"  wrote {fpath.name}")

    # Plot 3 -- conditional-share heatmap (cluster x recovery_phase + cluster x citalopram_phase)
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    # Recovery heatmap
    ax = axes[0]
    rec_mat = np.full((len(V24_COUNT_CLUSTERS), len(RECOVERY_PHASE_ORDER)), np.nan)
    for i, c in enumerate(V24_COUNT_CLUSTERS):
        for j, ph in enumerate(RECOVERY_PHASE_ORDER):
            cell = layer_b["recovery"]["count_clusters"][ph][c]
            if not math.isnan(cell["mean_share"]) and cell["n_notes"] > 0:
                rec_mat[i, j] = cell["mean_share"]
    im = ax.imshow(rec_mat, aspect="auto", cmap="viridis", interpolation="nearest")
    ax.set_xticks(range(len(RECOVERY_PHASE_ORDER)))
    ax.set_xticklabels(RECOVERY_PHASE_ORDER, rotation=30, ha="right", fontsize=8)
    ax.set_yticks(range(len(V24_COUNT_CLUSTERS)))
    ax.set_yticklabels(V24_COUNT_CLUSTERS, fontsize=8)
    ax.set_title("Layer B: conditional-on-note share x recovery_phase")
    for i in range(rec_mat.shape[0]):
        for j in range(rec_mat.shape[1]):
            v = rec_mat[i, j]
            if not np.isnan(v):
                txt_col = "white" if v < 0.15 else "black"
                ax.text(j, i, f"{v*100:.1f}", ha="center", va="center",
                        color=txt_col, fontsize=7)
            else:
                ax.text(j, i, "n/a", ha="center", va="center", color="white", fontsize=7)
    fig.colorbar(im, ax=ax)
    # Citalopram heatmap
    ax = axes[1]
    cit_mat = np.full((len(V24_COUNT_CLUSTERS), len(CITALOPRAM_PHASE_ORDER)), np.nan)
    for i, c in enumerate(V24_COUNT_CLUSTERS):
        for j, ph in enumerate(CITALOPRAM_PHASE_ORDER):
            cell = layer_b["citalopram"]["count_clusters"][ph][c]
            if not math.isnan(cell["mean_share"]) and cell["n_notes"] > 0:
                cit_mat[i, j] = cell["mean_share"]
    im = ax.imshow(cit_mat, aspect="auto", cmap="viridis", interpolation="nearest")
    ax.set_xticks(range(len(CITALOPRAM_PHASE_ORDER)))
    ax.set_xticklabels(CITALOPRAM_PHASE_ORDER, rotation=30, ha="right", fontsize=8)
    ax.set_yticks(range(len(V24_COUNT_CLUSTERS)))
    ax.set_yticklabels(V24_COUNT_CLUSTERS, fontsize=8)
    ax.set_title("Layer B: conditional-on-note share x citalopram_phase")
    for i in range(cit_mat.shape[0]):
        for j in range(cit_mat.shape[1]):
            v = cit_mat[i, j]
            if not np.isnan(v):
                txt_col = "white" if v < 0.15 else "black"
                ax.text(j, i, f"{v*100:.1f}", ha="center", va="center",
                        color=txt_col, fontsize=7)
            else:
                ax.text(j, i, "n/a", ha="center", va="center", color="white", fontsize=7)
    fig.colorbar(im, ax=ax)
    fig.suptitle(
        "Layer B conditional-on-note mean cluster-share (values shown as %, "
        "NOT a prevalence claim per asymmetry_MD sec 3)", fontsize=11,
    )
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fpath = plots_dir / "conditional_share_heatmap.png"
    plt.savefig(fpath, dpi=100)
    plt.close()
    print(f"  wrote {fpath.name}")

    # Plot 4 -- per-event-class table grid
    fig, ax = plt.subplots(figsize=(12, 7))
    classes = ["crash", "dip", "normal"]
    ec_mat = np.full((len(V24_COUNT_CLUSTERS), len(classes)), np.nan)
    for i, c in enumerate(V24_COUNT_CLUSTERS):
        for j, ec in enumerate(classes):
            cell = layer_b_event["count_clusters"][ec][c]
            if not math.isnan(cell["mean_share"]) and cell["n_notes"] > 0:
                ec_mat[i, j] = cell["mean_share"]
    im = ax.imshow(ec_mat, aspect="auto", cmap="plasma", interpolation="nearest")
    ax.set_xticks(range(len(classes)))
    ax.set_xticklabels(classes)
    ax.set_yticks(range(len(V24_COUNT_CLUSTERS)))
    ax.set_yticklabels(V24_COUNT_CLUSTERS, fontsize=9)
    ax.set_title(
        "Layer B per-event-class conditional-on-note mean cluster-share "
        "(Q4.4 sister; NOT prevalence)", fontsize=10,
    )
    for i in range(ec_mat.shape[0]):
        for j in range(ec_mat.shape[1]):
            v = ec_mat[i, j]
            if not np.isnan(v):
                txt_col = "white" if v < 0.15 else "black"
                ax.text(j, i, f"{v*100:.1f}%", ha="center", va="center",
                        color=txt_col, fontsize=8)
            else:
                ax.text(j, i, "n/a", ha="center", va="center", color="white", fontsize=8)
    fig.colorbar(im, ax=ax)
    plt.tight_layout()
    fpath = plots_dir / "per_event_class_table.png"
    plt.savefig(fpath, dpi=100)
    plt.close()
    print(f"  wrote {fpath.name}")

    # Plot 5 -- per-Q4.3-boundary +/-30d delta grid
    fig, ax = plt.subplots(figsize=(14, 7))
    bnames = [b[0] for b in Q43_BOUNDARIES]
    delta_mat = np.full((len(V24_COUNT_CLUSTERS), len(bnames)), np.nan)
    for i, c in enumerate(V24_COUNT_CLUSTERS):
        for j, bname in enumerate(bnames):
            b = layer_b_boundary[bname]
            if b["n_notes_pre"] == 0 or b["n_notes_post"] == 0:
                continue
            pre_v = b["count_clusters"]["pre"][c]["mean_share"]
            post_v = b["count_clusters"]["post"][c]["mean_share"]
            if math.isnan(pre_v) or math.isnan(post_v):
                continue
            delta_mat[i, j] = post_v - pre_v
    max_abs = float(np.nanmax(np.abs(delta_mat))) if not np.isnan(delta_mat).all() else 0.01
    im = ax.imshow(delta_mat, aspect="auto", cmap="RdBu_r", interpolation="nearest",
                   vmin=-max_abs, vmax=max_abs)
    short_bnames = [b.split("_to_")[0].replace("_pre_illness", "rp1").replace("_acute", "")
                    for b in bnames]
    short_bnames = [
        "rp1_2022-03-21", "rp2_2022-04-04", "rp3_2022-09-22",
        "rp4_2022-11-17", "rp5_2024-04-09", "cp3_2026-03-20",
    ]
    ax.set_xticks(range(len(bnames)))
    ax.set_xticklabels(short_bnames, rotation=30, ha="right", fontsize=8)
    ax.set_yticks(range(len(V24_COUNT_CLUSTERS)))
    ax.set_yticklabels(V24_COUNT_CLUSTERS, fontsize=9)
    ax.set_title(
        f"Layer B per-Q4.3-boundary +/-{BOUNDARY_HALF_WINDOW_DAYS}d delta share "
        "(post minus pre; conditional-on-note; NOT prevalence)", fontsize=10,
    )
    for i in range(delta_mat.shape[0]):
        for j in range(delta_mat.shape[1]):
            v = delta_mat[i, j]
            if not np.isnan(v):
                txt_col = "black"
                ax.text(j, i, f"{v*100:+.1f}", ha="center", va="center",
                        color=txt_col, fontsize=7)
            else:
                ax.text(j, i, "n/a", ha="center", va="center", color="gray", fontsize=7)
    fig.colorbar(im, ax=ax)
    plt.tight_layout()
    fpath = plots_dir / "per_boundary_pre_post.png"
    plt.savefig(fpath, dpi=100)
    plt.close()
    print(f"  wrote {fpath.name}")
    print()


# -----------------------------------------------------------------------------
# Stage 12 -- emit findings.md + README.md + summary.json
# -----------------------------------------------------------------------------


def emit_summary_json(out_dir, layer_a, layer_b, layer_b_event, layer_b_boundary, n_rows_total, n_notes_total):
    fpath = out_dir / "summary.json"
    summary = {
        "as_of_date": AS_OF_DATE,
        "coverage_window": {
            "start": GEVOELSCORE_COVERAGE_START,
            "end": AS_OF_DATE,
            "n_days_total": n_rows_total,
            "n_notes_total": n_notes_total,
        },
        "user_locked_operationalisation": {
            "scope": "ALL v24 categorical columns (12 count clusters + 3 state categorical + day_dominant_polarity + neutral_forward_looking_flag + n_clauses + has_note)",
            "write_rate_dims": "per-recovery-phase + per-citalopram-phase + per-DOW + per-month + has_note<->gevoelscore",
            "stratifications": "per-recovery-phase + per-citalopram-phase + per-event-class + per-Q4.3-boundary +/-30d",
            "trajectory_framing": "conditional-on-note share ONLY (absolute mention-rate EXCLUDED per asymmetry MD)",
        },
        "v24_count_clusters": V24_COUNT_CLUSTERS,
        "v24_state_categorical": V24_STATE_CATEGORICAL,
        "v24_day_dominant_polarity_categories": DAY_DOMINANT_CATEGORIES,
        "layer_a_write_rate": {
            "stage_2_per_recovery": layer_a["recovery"],
            "stage_3_per_citalopram": layer_a["citalopram"],
            "stage_4_per_dow": layer_a["dow"],
            "stage_5_per_month": layer_a["month"],
            "stage_6_score_correlation": layer_a["correlation"],
        },
        "layer_b_within_note_share": {
            "stage_7_per_recovery": layer_b["recovery"],
            "stage_8_per_citalopram": layer_b["citalopram"],
            "stage_9_per_event_class": layer_b_event,
            "stage_10_per_boundary": layer_b_boundary,
        },
        "thresholds": {
            "kw_suspect_p": KW_SUSPECT_THRESHOLD,
            "mwu_suspect_p": MWU_SUSPECT_THRESHOLD,
            "spearman_suspect_p": SPEARMAN_SUSPECT_THRESHOLD,
        },
        "q43_boundaries": [{"name": b[0], "date": b[1]} for b in Q43_BOUNDARIES],
        "boundary_half_window_days": BOUNDARY_HALF_WINDOW_DAYS,
    }
    with open(fpath, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, default=str)
    print(f"  wrote {fpath.name}")
    return summary


def emit_findings_md(out_dir, layer_a, layer_b, layer_b_event, layer_b_boundary, n_rows_total, n_notes_total):
    fpath = out_dir / "findings.md"
    lines = []
    a = lines.append

    a("# `trajectory/notes_patterns/` -- findings (Q4.7 note-categorisation patterns)")
    a("")
    a("## Authorship")
    a("")
    a("- **Computed**: 2026-06-26 by Claude (Opus 4.7) via [`run.py`](run.py) under the user-LOCKED operationalisation in [`README.md`](README.md) (Strand B section 7c interview 2026-06-26).")
    a(f"- **Data**: `per_day_master.csv` at `$GEVOELSCORE_DATA_PATH/unified/`; as-of-date **{AS_OF_DATE}**; coverage window **{GEVOELSCORE_COVERAGE_START}** -> **{AS_OF_DATE}** (Stratum 4; gevoelscore corpus start). **{n_rows_total} day-level rows**; **{n_notes_total} has_note=True rows** (write-rate {100.0*n_notes_total/n_rows_total:.1f}% over the window).")
    a("- **Axes**: 6-phase LC recovery axis from [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) (LOCKED `d47e0d3` 2026-06-19) + 5-phase citalopram axis from [`methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) section 3.")
    a("- **BINDING discipline**: [`methodology/symptom_mention_asymmetry.md`](../../../../methodology/symptom_mention_asymmetry.md) LOCKED 2026-06-11 -- LOAD-BEARING for every framing in this document. Per the rule (asymmetry MD section 1): **a mention is high-specificity positive evidence; absence of mention is NOT evidence of absence** (5 distinct causes per asymmetry MD section 2; only one is symptom-absent). Per asymmetry MD section 3: v24 CANNOT do prevalence trajectories; v24 CAN do stratify-by-content + conditional-on-note share. `has_note` IS daily_computed -- its trajectory IS clean (Layer A); v24 cat_* columns are presence_conditioned (Layer B; conditional-on-note share only per user-locked choice 4).")
    a("- **Layer 1 descriptive per [CONVENTIONS section 2.1 + section 4.3](../../../../CONVENTIONS.md)**: NO causal claims; NO `SUPPORTED` bar; NO `REFUTED` mark. Per CONVENTIONS section 4.2 caveat-class: Layer-B findings reported as `share-of-clauses on cluster X is Y conditional-on-note in phase Z` -- **NEVER** `cluster X is more prevalent in phase Z`. The 5-cause-of-absence rule is invoked at every Layer-B reading.")
    a("- **Cross-references**: [`run.py`](run.py) + [`summary.json`](summary.json) (gitignored) + [`plots/`](plots/) (5 PNGs, gitignored). Per-stage numbers below trace to the JSON.")
    a("")
    a("---")
    a("")

    # ---- Headline ----
    a("## Headline")
    a("")
    # Layer A
    a("**Layer A (write-rate; daily_computed; trajectory-clean)**:")
    a("")
    rec_rows = layer_a["recovery"]
    pieces = []
    for r in rec_rows:
        if r["n_days"] > 0:
            pieces.append(f"`{r['group']}`={fmt_pct(r['write_rate'])} (n={r['n_days']})")
    a("- Per-recovery-phase write-rate: " + "; ".join(pieces) + ".")
    cit_rows = layer_a["citalopram"]
    pieces = []
    for r in cit_rows:
        if r["n_days"] > 0:
            pieces.append(f"`{r['group']}`={fmt_pct(r['write_rate'])} (n={r['n_days']})")
    a("- Per-citalopram-phase write-rate: " + "; ".join(pieces) + ".")
    dow = layer_a["dow"]
    a(
        f"- Per-DOW write-rate: chi2 across 7 days p={fmt_float(dow['kw_p'], 4)} "
        f"(dof={dow['kw_dof']}); weekday={fmt_pct(dow['rate_weekday'])} vs "
        f"weekend={fmt_pct(dow['rate_weekend'])} (chi2 2x2 p={fmt_float(dow['weekend_p'], 4)}). "
        f"**SISTER to Q4.8 Stage 4 on Garmin channels**."
    )
    mon = layer_a["month"]
    a(
        f"- Per-month write-rate: chi2 across 12 months p={fmt_float(mon['kw_p'], 4)} "
        f"(dof={mon['kw_dof']}). **SISTER to Q4.8 Stage 3 on Garmin channels**."
    )
    cor = layer_a["correlation"]
    if cor is not None:
        a(
            f"- has_note <-> gevoelscore correlation (on n={cor['n_shared']} shared-coverage rows): "
            f"Spearman rho={fmt_float(cor['spearman_rho'], 4)} (p={fmt_float(cor['spearman_p'], 4)}); "
            f"chi2 2x3 across score-tertiles p={fmt_float(cor['chi2_p'], 4)}. "
            f"**Descriptive only** per CONVENTIONS section 4.2; does NOT imply low score causes writing."
        )
    a("")
    a("**Layer B (within-note share; presence_conditioned; conditional-on-note ONLY per user-locked choice 4)**:")
    a("")
    # Find top-3 cluster-share differentials per axis
    def top_diffs(table, group_order, k=3):
        rows = []
        for c in V24_COUNT_CLUSTERS:
            vals = []
            for g in group_order:
                cell = table[g][c]
                if not math.isnan(cell["mean_share"]) and cell["n_notes"] > 0:
                    vals.append((g, cell["mean_share"]))
            if len(vals) < 2:
                continue
            spread = max(v for _, v in vals) - min(v for _, v in vals)
            rows.append((c, spread, vals))
        rows.sort(key=lambda r: r[1], reverse=True)
        return rows[:k]
    rec_top = top_diffs(layer_b["recovery"]["count_clusters"], RECOVERY_PHASE_ORDER, 3)
    if rec_top:
        a("- Per-recovery-phase top-3 cluster-share spreads (conditional-on-note):")
        for c, sp, vals in rec_top:
            parts = ", ".join(f"{g}={fmt_pct(v)}" for g, v in vals)
            a(f"  - `{c}`: spread={fmt_pct(sp)} ({parts}).")
    cit_top = top_diffs(layer_b["citalopram"]["count_clusters"], CITALOPRAM_PHASE_ORDER, 3)
    if cit_top:
        a("- Per-citalopram-phase top-3 cluster-share spreads (conditional-on-note):")
        for c, sp, vals in cit_top:
            parts = ", ".join(f"{g}={fmt_pct(v)}" for g, v in vals)
            a(f"  - `{c}`: spread={fmt_pct(sp)} ({parts}).")
    ec_top = top_diffs(layer_b_event["count_clusters"], ["crash", "dip", "normal"], 3)
    if ec_top:
        a("- Per-event-class top-3 cluster-share spreads (conditional-on-note; **Q4.4 sister**):")
        for c, sp, vals in ec_top:
            parts = ", ".join(f"{g}={fmt_pct(v)}" for g, v in vals)
            a(f"  - `{c}`: spread={fmt_pct(sp)} ({parts}).")
    # Per-boundary top deltas across all 6
    bdry_top = []
    for bname, bdate in Q43_BOUNDARIES:
        b = layer_b_boundary[bname]
        if b["n_notes_pre"] == 0 or b["n_notes_post"] == 0:
            continue
        deltas = []
        for c in V24_COUNT_CLUSTERS:
            pre_v = b["count_clusters"]["pre"][c]["mean_share"]
            post_v = b["count_clusters"]["post"][c]["mean_share"]
            if math.isnan(pre_v) or math.isnan(post_v):
                continue
            deltas.append((c, post_v - pre_v, pre_v, post_v))
        deltas.sort(key=lambda x: abs(x[1]), reverse=True)
        if deltas:
            c0, d0, p0, q0 = deltas[0]
            bdry_top.append((bname, bdate, b["n_notes_pre"], b["n_notes_post"], c0, d0, p0, q0))
    if bdry_top:
        a("- Per-Q4.3-boundary top conditional-share delta (post minus pre, +/-30d window):")
        for bname, bdate, npre, npost, c0, d0, p0, q0 in bdry_top:
            a(
                f"  - `{bname}` ({bdate}; n_pre={npre} n_post={npost}): "
                f"top shift = `{c0}` delta={fmt_pct(d0)} (pre={fmt_pct(p0)} post={fmt_pct(q0)})."
            )
    a("")
    a("**CRITICAL FRAMING per asymmetry MD section 3 + CONVENTIONS section 4.2**: every Layer-B number above is a `share-of-clauses-conditional-on-note`. A higher cluster share in phase Z relative to phase Y does **NOT** support the claim that the corresponding symptom/topic is more prevalent in phase Z. The 5-cause-of-absence rule (asymmetry MD section 2) applies: a lower share could equally reflect (1) symptom absent, (2) symptom present but unworthy of writing, (3) symptom present but crowded out by another topic, (4) symptom present but routine/habituated, or (5) the day's note simply did not exist (which the Layer-A write-rate analysis exposes is itself unequally distributed across phases).")
    a("")
    a("---")
    a("")

    # ---- Section 1: Layer A Stage 2 -- per-recovery-phase ----
    a("## 1. Layer A Stage 2 -- write-rate per-recovery-phase")
    a("")
    a("**Method**: per phase, count `has_note=True` rows / total rows in phase. `has_note` is daily_computed; the trajectory is CLEAN per asymmetry MD section 3 (the daily_computed family that includes `gevoelscore`, Garmin biometric channels, coverage flags).")
    a("")
    a("| phase | n_days | n_notes | P(has_note) |")
    a("|---|---:|---:|---:|")
    for r in layer_a["recovery"]:
        a(
            f"| `{r['group']}` | {r['n_days']} | {r['n_notes']} | "
            f"{fmt_pct(r['write_rate'])} |"
        )
    a("")
    a("**Reading**: write-rate trajectory across the 6-phase recovery axis is fair to characterise (this is a daily_computed signal). `pre_illness_healthy` + `acute_infection` predate the notes corpus (user started writing 2022-10-18, within `lc_pre_ergo`); these phases show 0% write-rate by construction, NOT because the user was healthier or because nothing was worth writing about.")
    a("")
    a("---")
    a("")

    # ---- Section 2: Layer A Stage 3 -- per-citalopram-phase ----
    a("## 2. Layer A Stage 3 -- write-rate per-citalopram-phase")
    a("")
    a("**Method**: per phase, count `has_note=True` rows / total rows in phase. Phase boundaries per [`citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) section 3.")
    a("")
    a("| phase | n_days | n_notes | P(has_note) |")
    a("|---|---:|---:|---:|")
    for r in layer_a["citalopram"]:
        a(
            f"| `{r['group']}` | {r['n_days']} | {r['n_notes']} | "
            f"{fmt_pct(r['write_rate'])} |"
        )
    a("")
    a("---")
    a("")

    # ---- Section 3: Layer A Stage 4 -- per-DOW ----
    a("## 3. Layer A Stage 4 -- write-rate per-DOW (Q4.8 sister on `has_note`)")
    a("")
    a("**Method**: per day-of-week, count `has_note=True` rows / total rows on that DOW. Chi-square 2x7 contingency test across the 7 day-groups (more natural than KW for a binary outcome). Weekday-vs-weekend chi-square 2x2. **Sister analysis** to [`trajectory/seasonality_dow/`](../seasonality_dow/findings.md) Stage 4 on the 6 Garmin channels.")
    a("")
    a("| DOW | n_days | n_notes | P(has_note) |")
    a("|---|---:|---:|---:|")
    for r in layer_a["dow"]["per_dow"]:
        a(
            f"| {r['name']} | {r['n_days']} | {r['n_notes']} | "
            f"{fmt_pct(r['write_rate'])} |"
        )
    a("")
    dow = layer_a["dow"]
    flag = "**SUSPECT**" if (not math.isnan(dow["kw_p"]) and dow["kw_p"] < KW_SUSPECT_THRESHOLD) else "no-flag"
    a(
        f"**Across 7 days**: chi2 statistic = {fmt_float(dow['kw_chi2'], 2)} "
        f"(dof={dow['kw_dof']}), p = {fmt_float(dow['kw_p'], 4)} ({flag} at p<{KW_SUSPECT_THRESHOLD})."
    )
    a("")
    we_flag = "**SUSPECT**" if (not math.isnan(dow["weekend_p"]) and dow["weekend_p"] < MWU_SUSPECT_THRESHOLD) else "no-flag"
    a(
        f"**Weekday vs weekend**: P(weekday)={fmt_pct(dow['rate_weekday'])} (n={dow['n_weekday']}) "
        f"vs P(weekend)={fmt_pct(dow['rate_weekend'])} (n={dow['n_weekend']}); chi2 2x2 "
        f"p={fmt_float(dow['weekend_p'], 4)} ({we_flag} at p<{MWU_SUSPECT_THRESHOLD})."
    )
    a("")
    a("**Reading per CONVENTIONS section 4.2 caveat-class**: a SUSPECT flag indicates a non-uniform write-rate across DOWs at p < 0.05. This is a DESCRIPTIVE substrate; mechanism (e.g. weekend habit shift, work-week structuring) is out of scope.")
    a("")
    a("---")
    a("")

    # ---- Section 4: Layer A Stage 5 -- per-month ----
    a("## 4. Layer A Stage 5 -- write-rate per-month (Q4.8 sister)")
    a("")
    a("**Method**: per calendar-month, count `has_note=True` rows / total rows in that month. Chi-square 2x12 contingency. **Sister analysis** to [`trajectory/seasonality_dow/`](../seasonality_dow/findings.md) Stage 3.")
    a("")
    a("| month | n_days | n_notes | P(has_note) |")
    a("|---|---:|---:|---:|")
    for r in layer_a["month"]["per_month"]:
        a(
            f"| {r['name']} | {r['n_days']} | {r['n_notes']} | "
            f"{fmt_pct(r['write_rate'])} |"
        )
    a("")
    mon = layer_a["month"]
    flag = "**SUSPECT**" if (not math.isnan(mon["kw_p"]) and mon["kw_p"] < KW_SUSPECT_THRESHOLD) else "no-flag"
    a(
        f"**Across 12 months**: chi2 statistic = {fmt_float(mon['kw_chi2'], 2)} "
        f"(dof={mon['kw_dof']}), p = {fmt_float(mon['kw_p'], 4)} ({flag} at p<{KW_SUSPECT_THRESHOLD})."
    )
    a("")
    a("---")
    a("")

    # ---- Section 5: Layer A Stage 6 -- score correlation ----
    a("## 5. Layer A Stage 6 -- has_note <-> gevoelscore correlation")
    a("")
    a("**Method**: on rows where both `has_score=True` and `has_note` is defined (it is defined for all rows in Stratum 4; the gate is on `has_score`). Score-bin contingency (low=1-2, mid=3, high=4-5) + Spearman rho. **In the same family as Q4.6 MCAR diagnostic**: missingness in v24 is structured, not random; this stage characterises one specific dimension of the structure (score-conditional write-rate).")
    a("")
    cor = layer_a["correlation"]
    if cor is None:
        a("Insufficient n for the correlation; skipped.")
    else:
        a(f"**Shared-coverage rows (has_score=True)**: {cor['n_shared']}.")
        a("")
        a("| score bin | n_days | n_notes | P(has_note) |")
        a("|---|---:|---:|---:|")
        for r in cor["per_score_bin"]:
            a(
                f"| {r['bin']} | {r['n_days']} | {r['n_notes']} | "
                f"{fmt_pct(r['write_rate'])} |"
            )
        a("")
        sp_flag = "**SUSPECT**" if (not math.isnan(cor["spearman_p"]) and cor["spearman_p"] < SPEARMAN_SUSPECT_THRESHOLD) else "no-flag"
        chi_flag = "**SUSPECT**" if (not math.isnan(cor["chi2_p"]) and cor["chi2_p"] < KW_SUSPECT_THRESHOLD) else "no-flag"
        a(
            f"**Spearman rho(gevoelscore, has_note)** = {fmt_float(cor['spearman_rho'], 4)}; "
            f"p = {fmt_float(cor['spearman_p'], 4)} ({sp_flag} at p<{SPEARMAN_SUSPECT_THRESHOLD})."
        )
        a(
            f"**Chi-square 2x3 (note x score-tertile)**: chi2 = {fmt_float(cor['chi2'], 2)} "
            f"(dof={cor['chi2_dof']}), p = {fmt_float(cor['chi2_p'], 4)} ({chi_flag} at p<{KW_SUSPECT_THRESHOLD})."
        )
    a("")
    a("**Reading per CONVENTIONS section 4.2**: a SUSPECT correlation is a DESCRIPTIVE observation that write-propensity covaries with self-reported felt-state. It does NOT imply (a) low score causes writing, (b) writing causes low score, or (c) the underlying symptom prevalence at low-score-days differs from high-score-days. Per Q4.6 the MAR/MNAR character of v24 missingness is structured; this stage characterises one dimension of the structure.")
    a("")
    a("---")
    a("")

    # ---- Section 6: Layer B Stage 7 -- per-recovery-phase ----
    a("## 6. Layer B Stage 7 -- within-note share per-recovery-phase")
    a("")
    a("**Method**: filter to `has_note=True` rows. For each (cluster, phase) cell, compute `mean(cluster_count / n_clauses)` across days in the phase (each note weighted equally). The number is the **conditional-on-note mean cluster-share**; per asymmetry MD section 3 it does NOT estimate prevalence. The state_symptoom categorical columns + day_dominant_polarity get separate categorical distributions; neutral_forward_looking_flag gets a boolean rate.")
    a("")
    a("**Conditional-on-note mean cluster-share x recovery_phase** (values as percent of clauses):")
    a("")
    a(
        "| cluster | "
        + " | ".join(ph for ph in RECOVERY_PHASE_ORDER)
        + " |"
    )
    a("|---|" + "|".join(["---:"] * len(RECOVERY_PHASE_ORDER)) + "|")
    for c in V24_COUNT_CLUSTERS:
        cells = []
        for ph in RECOVERY_PHASE_ORDER:
            cell = layer_b["recovery"]["count_clusters"][ph][c]
            if math.isnan(cell["mean_share"]) or cell["n_notes"] == 0:
                cells.append("n/a")
            else:
                cells.append(fmt_pct(cell["mean_share"]))
        a(f"| `{c}` | " + " | ".join(cells) + " |")
    a("")
    # n_notes per phase footer
    n_strs = []
    for ph in RECOVERY_PHASE_ORDER:
        # take from first cluster's n_notes (consistent across clusters)
        nph = layer_b["recovery"]["count_clusters"][ph][V24_COUNT_CLUSTERS[0]]["n_notes"]
        n_strs.append(f"`{ph}` n_notes={nph}")
    a("**n_notes per phase**: " + "; ".join(n_strs) + ".")
    a("")
    # boolean flag table
    a("**Conditional-on-note boolean flag `neutral_forward_looking_flag` x recovery_phase**:")
    a("")
    a("| phase | n_notes | n_with_value | n_true | rate (conditional) |")
    a("|---|---:|---:|---:|---:|")
    for ph in RECOVERY_PHASE_ORDER:
        c = layer_b["recovery"]["boolean_flag"][ph]
        rate_s = fmt_pct(c["rate"]) if c["n_with_value"] > 0 else "n/a"
        a(
            f"| `{ph}` | {c['n_notes']} | {c['n_with_value']} | "
            f"{c['n_true']} | {rate_s} |"
        )
    a("")
    # day_dominant_polarity table
    a("**Conditional-on-note categorical `day_dominant_polarity` x recovery_phase**:")
    a("")
    a("| phase | n_with_value | " + " | ".join(DAY_DOMINANT_CATEGORIES) + " |")
    a("|---|---:|" + "|".join(["---:"] * len(DAY_DOMINANT_CATEGORIES)) + "|")
    for ph in RECOVERY_PHASE_ORDER:
        cell = layer_b["recovery"]["day_dominant_polarity"][ph]
        parts = []
        for lvl in DAY_DOMINANT_CATEGORIES:
            v = cell["per_level"][lvl]["share_of_with_value"]
            parts.append(fmt_pct(v) if not math.isnan(v) else "n/a")
        a(f"| `{ph}` | {cell['n_with_value']} | " + " | ".join(parts) + " |")
    a("")
    a("**Reading per asymmetry MD section 3**: each cell is a `share-of-clauses-conditional-on-note`. The 5-cause-of-absence rule applies: a cluster's share dropping from phase X to phase Y could reflect any of (1) symptom absent, (2) routine, (3) crowded out by other topics, (4) habituated, or (5) the note didn't exist (the write-rate Layer A documents this systematically). NOT a prevalence claim.")
    a("")
    a("---")
    a("")

    # ---- Section 7: Layer B Stage 8 -- per-citalopram-phase ----
    a("## 7. Layer B Stage 8 -- within-note share per-citalopram-phase")
    a("")
    a("**Method**: same as Stage 7, on the 5-phase citalopram axis.")
    a("")
    a(
        "| cluster | "
        + " | ".join(ph for ph in CITALOPRAM_PHASE_ORDER)
        + " |"
    )
    a("|---|" + "|".join(["---:"] * len(CITALOPRAM_PHASE_ORDER)) + "|")
    for c in V24_COUNT_CLUSTERS:
        cells = []
        for ph in CITALOPRAM_PHASE_ORDER:
            cell = layer_b["citalopram"]["count_clusters"][ph][c]
            if math.isnan(cell["mean_share"]) or cell["n_notes"] == 0:
                cells.append("n/a")
            else:
                cells.append(fmt_pct(cell["mean_share"]))
        a(f"| `{c}` | " + " | ".join(cells) + " |")
    a("")
    n_strs = []
    for ph in CITALOPRAM_PHASE_ORDER:
        nph = layer_b["citalopram"]["count_clusters"][ph][V24_COUNT_CLUSTERS[0]]["n_notes"]
        n_strs.append(f"`{ph}` n_notes={nph}")
    a("**n_notes per phase**: " + "; ".join(n_strs) + ".")
    a("")
    a("---")
    a("")

    # ---- Section 8: Layer B Stage 9 -- per-event-class ----
    a("## 8. Layer B Stage 9 -- within-note share per-event-class (Q4.4 sister)")
    a("")
    a("**Method**: filter to `has_note=True`; stratify by `is_crash` + `is_dip` + `normal` (mutually exclusive per [`crash_v2-definition`](../../../hypotheses/crash_v2-definition/) section 2.2). **Q4.4 sister**: cohort_topology defines the event classes; this stage answers the asymmetry MD's worked example -- 'of crash-day notes, what fraction of clauses are on cluster X conditional-on-note?'")
    a("")
    a("**`is_crash` per-day vs Q4.4 episode count**: Q4.4 reports 29 crash *episodes* (mean duration 3.55 days, max 14 days); per-day `is_crash=True` rows therefore total ~103 (29 episodes x mean duration). The Stage 9 counts use the per-day flag (each day in a multi-day crash counted independently). This is the natural unit for per-day-note stratification but the day-count is NOT directly comparable to the episode-count.")
    a("")
    classes = ["crash", "dip", "normal"]
    a("| cluster | " + " | ".join(classes) + " |")
    a("|---|" + "|".join(["---:"] * 3) + "|")
    for c in V24_COUNT_CLUSTERS:
        cells = []
        for ec in classes:
            cell = layer_b_event["count_clusters"][ec][c]
            if math.isnan(cell["mean_share"]) or cell["n_notes"] == 0:
                cells.append("n/a")
            else:
                cells.append(fmt_pct(cell["mean_share"]))
        a(f"| `{c}` | " + " | ".join(cells) + " |")
    a("")
    n_strs = []
    for ec in classes:
        nec = layer_b_event["count_clusters"][ec][V24_COUNT_CLUSTERS[0]]["n_notes"]
        n_strs.append(f"`{ec}` n_notes={nec}")
    a("**n_notes per class**: " + "; ".join(n_strs) + ".")
    a("")
    a("**Conditional-on-note categorical `day_dominant_polarity` x event_class**:")
    a("")
    a("| class | n_with_value | " + " | ".join(DAY_DOMINANT_CATEGORIES) + " |")
    a("|---|---:|" + "|".join(["---:"] * len(DAY_DOMINANT_CATEGORIES)) + "|")
    for ec in classes:
        cell = layer_b_event["day_dominant_polarity"][ec]
        parts = []
        for lvl in DAY_DOMINANT_CATEGORIES:
            v = cell["per_level"][lvl]["share_of_with_value"]
            parts.append(fmt_pct(v) if not math.isnan(v) else "n/a")
        a(f"| `{ec}` | {cell['n_with_value']} | " + " | ".join(parts) + " |")
    a("")
    a("**Cross-corroboration but NOT promotion** (per handoff section 3.4): if a per-event-class finding 'lines up with' a HA-* finding (e.g. crash-day notes show a higher share of `cat_symptoom_cognitief` than normal-day notes, and HA01b is about cognitive load), surface as descriptive cross-reference. The corroboration does NOT extend HA01b's verdict here; HA01b operationalises at a different layer.")
    a("")
    a("---")
    a("")

    # ---- Section 9: Layer B Stage 10 -- per-Q4.3-boundary +/-30d ----
    a("## 9. Layer B Stage 10 -- within-note share per Q4.3-boundary +/-30d")
    a("")
    a(f"**Method**: for each of the 6 strong Q4.3 boundaries (per [`era_boundaries/findings.md`](../era_boundaries/findings.md) section 1), restrict to the +/-{BOUNDARY_HALF_WINDOW_DAYS}d window around the boundary date; filter to `has_note=True`; compute pre vs post side cluster-share table. Delta = post share minus pre share. **Q4.3 substrate**: 6 boundaries (rp1, rp2, rp3, rp4, rp5, cp3) each get an independent pre/post comparison.")
    a("")
    for bname, bdate in Q43_BOUNDARIES:
        b = layer_b_boundary[bname]
        a(f"### 9.{bname.split('_')[0]} `{bname}` ({bdate}; n_notes_pre={b['n_notes_pre']}; n_notes_post={b['n_notes_post']})")
        a("")
        if b["n_notes_pre"] == 0 or b["n_notes_post"] == 0:
            a("Skipped: one side has 0 notes in the +/-30d window (typical for early-LC boundaries before the user started writing notes 2022-10-18).")
            a("")
            continue
        a("| cluster | pre share | post share | delta (post - pre) |")
        a("|---|---:|---:|---:|")
        deltas = []
        for c in V24_COUNT_CLUSTERS:
            pre_cell = b["count_clusters"]["pre"][c]
            post_cell = b["count_clusters"]["post"][c]
            pre_v = pre_cell["mean_share"]
            post_v = post_cell["mean_share"]
            if math.isnan(pre_v) or math.isnan(post_v):
                continue
            d_ = post_v - pre_v
            deltas.append((c, pre_v, post_v, d_))
        # Sort by abs delta
        deltas.sort(key=lambda x: abs(x[3]), reverse=True)
        for c, p_, q_, d_ in deltas:
            a(f"| `{c}` | {fmt_pct(p_)} | {fmt_pct(q_)} | {fmt_pct(d_)} |")
        a("")
        a("**Reading per asymmetry MD section 3**: delta in share at boundary does NOT mean delta in prevalence. Could reflect (a) a real shift in what the user wrote about across the boundary (note-content shift), OR (b) the 5-cause-of-absence rule. The boundary substrate is Q4.3 (descriptive) and the conditional-share shift is descriptive.")
        a("")
    a("---")
    a("")

    # ---- Section 10: Caveats ----
    a("## 10. Caveats (CRITICAL -- per asymmetry MD + CONVENTIONS section 4.2 caveat-class)")
    a("")
    a("1. **Asymmetry discipline (LOAD-BEARING)**: every Layer-B number is `share-of-clauses-conditional-on-note`. A higher share in phase Z is NEVER a claim that the corresponding symptom/topic is more prevalent in phase Z. Five distinct causes of absence-of-mention per asymmetry MD section 2: only one is 'symptom absent'.")
    a("2. **Layer A vs Layer B asymmetry**: Layer A (write-rate per-phase/per-DOW/per-month/per-score) is trajectory-clean because `has_note` is daily_computed (asymmetry MD section 3 + DATA_DICTIONARY section 14). Layer B (within-note cluster shares) is asymmetry-conditional and EXCLUDES absolute mention-rate trajectories per user-locked choice 4.")
    a("3. **Q4.6 MCAR-rejection family**: per Q4.6 coverage_overview, all 89 tested-eligible channels reject MCAR (missingness depends on other channels). Stage 6 (has_note <-> gevoelscore correlation) is in the same family -- it characterises one specific dimension of that structured missingness.")
    a("4. **Cross-corroboration but NOT verdict promotion**: even if a Stage 7-10 finding lines up with a HA-* result (e.g. higher `cat_symptoom_cognitief` share on crash days lines up with cognitive-load HAs), this is a DESCRIPTIVE cross-reference at a different operationalisation -- it does NOT extend the HA's verdict.")
    a("5. **Wrong-shape claims that this analysis MUST avoid** (per asymmetry MD section 3 Right-vs-Wrong table): 'brainfog prevalence in 2024 was X%'; 'in 2025 the user had less muscle pain'; 'on the day before a crash, cat_symptoom_cognitief=0 therefore no brainfog'. All forbidden.")
    a("6. **5-cause-of-absence applies to state_symptoom categoricals too**: `state_symptoom_cognitief=absent` is itself presence-conditioned positive ('geen brainfog was mentioned') and is distinct from no-mention. The categorical distribution on `has_note=True` rows where `state_symptoom_cognitief` is non-NaN is reported; NaN cells indicate the note did not contain a state-mention for that family.")
    a("7. **Write-rate per-phase Layer A includes phases the user predates writing**: `pre_illness_healthy` + `acute_infection` show 0% write-rate by construction (user started writing notes 2022-10-18, within `lc_pre_ergo`). NOT a substantive interpretation of those phases.")
    a("8. **Per-Q4.3-boundary windows around early boundaries**: rp1 + rp2 + rp3 + rp4 fall before or near the start of the notes corpus; n_notes_pre is often 0, in which case the boundary is skipped per the n_pre > 0 + n_post > 0 gate.")
    a("9. **Statistical tests are descriptive markers, not falsification bars**: Layer A chi-square + Spearman flags are at the 0.05 conventional threshold (CONVENTIONS section 4.2 caveat-class), not multiple-comparison-corrected, not falsification-bar locked.")
    a("")
    a("---")
    a("")

    # ---- Section 11: Cross-references ----
    a("## 11. Cross-references")
    a("")
    a("### LOAD-BEARING (binding for this analysis's discipline)")
    a("")
    a("- [`methodology/symptom_mention_asymmetry.md`](../../../../methodology/symptom_mention_asymmetry.md) LOCKED 2026-06-11 -- **the binding methodological MD for Q4.7**. Section 1 (the rule) + section 2 (5 causes of absence) + section 3 (what v24 IS and IS NOT) cited at every framing decision.")
    a("- [`DATA_DICTIONARY.md`](../../../../DATA_DICTIONARY.md) section 9 (presence-conditioned preamble) + section 10 (state_symptoom + sub-tags) -- column-level types + the `has_note=True` gating-flag convention.")
    a("- [`CONVENTIONS.md`](../../../../CONVENTIONS.md) section 2.1 (descriptive-before-inference) + section 4.2 (caveat-class language) + section 4.3 (no interpretive marks).")
    a("")
    a("### Descriptive corroboration (NOT verdict extension)")
    a("")
    a("- [`trajectory/coverage_overview/findings.md`](../coverage_overview/findings.md) section 6.2 -- Q4.6 MCAR diagnostic family (89 of 89 numeric channels reject MCAR at alpha=0.05); Stage 6 is in the same family.")
    a("- [`trajectory/seasonality_dow/findings.md`](../seasonality_dow/findings.md) Stage 3 + Stage 4 -- Q4.8 per-month + per-DOW patterns on Garmin channels; Stage 4 + Stage 5 here are SISTERS on `has_note`.")
    a("- [`trajectory/cohort_topology/findings.md`](../cohort_topology/findings.md) section 1 + section 5 -- Q4.4 event-class definitions (29 crashes + 79 dips + crash-vs-dip distinction at autonomic-load layer); Stage 9 uses these.")
    a("- [`trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) section 1 + section 2 -- Q4.3 6 strong boundaries; Stage 10 uses these as substrate for +/-30d windows.")
    a("")
    a("### Queued-primitive substrate (NOT promotion)")
    a("")
    a("- **HA-C4b v3 section 8 queued primitive** on emotional/cognitive triggers + state_symptoom_* proxies: Stage 7 + Stage 8 + Stage 9 + Stage 10 provide DESCRIPTIVE substrate for that queued primitive. **NO promotion to that primitive's MD** per CONVENTIONS section 4.2.")
    a("")
    a("### Methodology MDs cited")
    a("")
    a("- [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) section 2 -- 6-phase recovery axis (LOCKED `d47e0d3` 2026-06-19).")
    a("- [`methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) section 3 -- 5-phase citalopram axis.")
    a("")
    a("### Upstream pipeline")
    a("")
    a("- `pipeline/03_consolidate/build_unified_dataset.py` -- `per_day_master.csv` builder (includes `has_note` + `cat_*` + `state_symptoom_*` + `day_dominant_polarity` + `neutral_forward_looking_flag`).")
    a("- `analyses/_utils/frame.py` -- `load_master()` loader (single source of truth for the as-of-date convention).")
    a("")
    a("---")
    a("")

    # ---- Section 12: Status ----
    a("## 12. Status")
    a("")
    a("**Q4.7 findings landed 2026-06-26** from a single execution of [`run.py`](run.py) under the user-LOCKED operationalisation (Strand B section 7c interview 2026-06-26). **Tier 3 deferred-topic 2 of 2 LANDED**; Q4.8 sister landed at `e4db6cc` + STOCKTAKE at `09b9177`. **Strand B 8 of 8 CLOSED**. Foundation now in place for `/research-interpret` skill pivot per user's earlier sequencing: 'before we start using the research interpret skill, i want to make sure we finished all basic and foundational descriptive research'.")
    a("")
    a("Next refresh per [`descriptive/README.md`](../../README.md) section 7d: when new note-corpus data accrues +90 days OR when an HA-* result raises a write-rate-sensitive or conditional-share-sensitive question (e.g. the user-noted hypothesis that crash-day notes show distinctive within-note content).")
    a("")

    with open(fpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"  wrote {fpath.name} ({len(lines)} lines)")


def emit_readme_md(out_dir, n_rows_total, n_notes_total):
    fpath = out_dir / "README.md"
    lines = []
    a = lines.append

    a("# `trajectory/notes_patterns/` -- Q4.7 note-categorisation patterns")
    a("")
    a("## What this analysis answers")
    a("")
    a("**Q4.7 per [`descriptive/README.md`](../../README.md) section 4.7**: What's the symptom-mention asymmetry profile? When does the user write vs not? How does the categorisation distribution shift across LC eras?")
    a("")
    a("**Tier 3 deferred topic 2 of 2** (Q4.8 seasonality_dow is the other; landed at `e4db6cc` 2026-06-26). **The FINAL Strand B topic before the `/research-interpret` skill pivot**.")
    a("")
    a("---")
    a("")
    a("## BINDING methodological discipline")
    a("")
    a("[`methodology/symptom_mention_asymmetry.md`](../../../../methodology/symptom_mention_asymmetry.md) LOCKED 2026-06-11 is LOAD-BEARING for every framing decision in this analysis:")
    a("")
    a("- v24 cat_* columns are **presence_conditioned_positive_evidence**. A mention is high-specificity positive evidence; **absence of mention is NOT evidence of absence** (5 distinct causes per asymmetry MD section 2; only one is 'symptom absent').")
    a("- v24 CANNOT do prevalence trajectories (mention-rate is confounded with note-writing-rate).")
    a("- v24 CAN do **stratify-by-content** + **conditional-on-note share** (the user-locked framing here).")
    a("- `has_note` IS daily_computed -- its trajectory IS clean.")
    a("")
    a("---")
    a("")
    a("## User-LOCKED operationalisation (per Strand B section 7c interview 2026-06-26; do NOT iterate)")
    a("")
    a("1. **Scope = ALL v24 categorical columns** (per data dictionary section 9 + section 10): 5 belasting + 3 symptoom + 3 state_symptoom + 4 ancillary (medicatie, recovery_actie, triggers_extern, neutral_forward_looking_flag) + day_dominant_polarity + n_clauses + has_note (the daily_computed gating flag).")
    a("2. **Write-rate dimensions = ALL**: per-recovery-phase + per-citalopram-phase + per-DOW (Q4.8 sister) + per-month (Q4.8 sister) + has_note <-> gevoelscore correlation.")
    a("3. **Stratifications = ALL**: per-recovery-phase + per-citalopram-phase + per-event-class (crash vs dip vs normal per Q4.4) + per-Q4.3-boundary +/-30d (6 strong boundaries: rp1-rp5 + cp3).")
    a("4. **Trajectory framing = conditional-on-note share ONLY** (cleanest per the asymmetry discipline). **Absolute mention-rate trajectories are EXCLUDED**.")
    a("")
    a("---")
    a("")
    a("## Method (12-stage architecture; 2 analytic layers)")
    a("")
    a("**Layer A -- write-rate (daily_computed; trajectory-clean per asymmetry MD section 3)**:")
    a("")
    a(f"- **Stage 1** (data prep): load `per_day_master.csv`; restrict to {GEVOELSCORE_COVERAGE_START} -> {AS_OF_DATE}; identify recovery_phase + citalopram_phase + month + DOW per row.")
    a("- **Stage 2** (write-rate per-recovery-phase): per phase, P(has_note=True) + n_days + n_notes.")
    a("- **Stage 3** (write-rate per-citalopram-phase): same shape on 5-phase citalopram axis.")
    a("- **Stage 4** (write-rate per-DOW): 7-DOW table + chi2 2x7 + weekday-vs-weekend chi2 2x2 (**SISTER TO Q4.8 Stage 4** on Garmin channels).")
    a("- **Stage 5** (write-rate per-month): 12-month table + chi2 2x12 (**SISTER TO Q4.8 Stage 3**).")
    a("- **Stage 6** (has_note <-> gevoelscore correlation): score-bin contingency + Spearman rho on `has_score=True` shared-coverage rows. **In the same family as Q4.6 MCAR diagnostic**.")
    a("")
    a("**Layer B -- within-note share (presence_conditioned; conditional-on-note ONLY per user lock 4)**:")
    a("")
    a("- **Stage 7** (per-cluster within-note share, per-recovery-phase): filter `has_note=True`; per (cluster, phase) cell compute mean(cluster_count / n_clauses). Categorical state_symptoom + day_dominant_polarity + boolean neutral_forward_looking_flag get separate distributions.")
    a("- **Stage 8** (per-cluster within-note share, per-citalopram-phase): same shape, 5-phase citalopram axis.")
    a("- **Stage 9** (per-cluster within-note share, per-event-class): stratify by `is_crash` + `is_dip` + `normal` per Q4.4. **Q4.4 sister + asymmetry MD's worked example**.")
    a("- **Stage 10** (per-cluster within-note share, per-Q4.3-boundary +/-30d): for each of the 6 strong Q4.3 boundaries (rp1-rp5 + cp3), compute pre vs post share table within +/-30d window.")
    a("")
    a("**Layer C -- output + emit**:")
    a("")
    a("- **Stage 11** (output artefacts): 5 PNG plots.")
    a("- **Stage 12** (programmatic emit): [`findings.md`](findings.md) + this README + [`summary.json`](summary.json) (gitignored).")
    a("")
    a("---")
    a("")
    a("## Discipline guards")
    a("")
    a("- **Layer 1 descriptive per CONVENTIONS section 2.1**: NO causal claims; NO `SUPPORTED` bar; NO `REFUTED` mark.")
    a("- **Per CONVENTIONS section 4.2 caveat-class**: Layer-B findings reported as `share-of-clauses on cluster X is Y conditional-on-note in phase Z` -- NEVER `cluster X is more prevalent in phase Z`. The 5-cause-of-absence rule is invoked at every Layer-B reading.")
    a("- **NO absolute mention-rate trajectories** (user-locked choice 4: conditional-on-note share only; absolute mention-rate is EXCLUDED per asymmetry MD section 3).")
    a("- **NO claim that absence-of-mention is absence-of-symptom** (asymmetry MD section 2: 5 causes).")
    a("- **NO HA verdict promotion** (cross-corroboration only; HA-C4b v3 section 8 queued primitive substrate ONLY, NO promotion to that primitive's MD).")
    a("- **ASCII-only stdout; no em-dashes; no emojis** per project convention.")
    a("- **f-string discipline**: no nested double-quotes inside expressions (pre-3.12 compatibility); use format() or extract-to-variable.")
    a("")
    a("---")
    a("")
    a("## How to run")
    a("")
    a("```")
    a("# Requires GEVOELSCORE_DATA_PATH env var pointing to gevoelscore-data root")
    a("python docs/research/analyses/descriptive/trajectory/notes_patterns/run.py")
    a("```")
    a("")
    a(f"Outputs (all but [`run.py`](run.py) + [`README.md`](README.md) + [`findings.md`](findings.md) gitignored). Computed on `per_day_master.csv` as-of-date `{AS_OF_DATE}` over the {GEVOELSCORE_COVERAGE_START} -> {AS_OF_DATE} window (Stratum 4): {n_rows_total} day-level rows; {n_notes_total} has_note=True rows ({100.0*n_notes_total/n_rows_total:.1f}%).")
    a("")
    a("- `summary.json` -- machine-readable per-stage statistics")
    a("- `plots/write_rate_per_phase.png` -- Layer A: recovery + citalopram phase bars")
    a("- `plots/write_rate_dow_month.png` -- Layer A: DOW + month grids")
    a("- `plots/conditional_share_heatmap.png` -- Layer B: cluster x recovery/citalopram phases")
    a("- `plots/per_event_class_table.png` -- Layer B: cluster x crash/dip/normal")
    a("- `plots/per_boundary_pre_post.png` -- Layer B: cluster x boundary delta (post - pre)")
    a("")
    a("---")
    a("")
    a("## Status")
    a("")
    a("**LANDED 2026-06-26**. Tier 3 deferred-topic 2 of 2 closed. **Strand B 8 of 8 CLOSED**. Foundation in place for `/research-interpret` skill pivot per user's earlier sequencing.")
    a("")

    with open(fpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"  wrote {fpath.name} ({len(lines)} lines)")


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------


def main():
    print()
    print("#" * 70)
    print("# Q4.7 notes_patterns -- Strand B Tier-3 deferred topic 2 of 2")
    print("# BINDING discipline: symptom_mention_asymmetry.md LOCKED 2026-06-11")
    print("#" * 70)
    print()

    out_dir = HERE
    df = stage_1_load_data()
    n_rows_total = int(len(df))
    n_notes_total = int(df["has_note"].sum())

    # Layer A
    a_recovery = stage_2_writerate_recovery(df)
    a_citalopram = stage_3_writerate_citalopram(df)
    a_dow = stage_4_writerate_dow(df)
    a_month = stage_5_writerate_month(df)
    a_corr = stage_6_correlation(df)

    layer_a = {
        "recovery": a_recovery,
        "citalopram": a_citalopram,
        "dow": a_dow,
        "month": a_month,
        "correlation": a_corr,
    }

    # Layer B
    b_recovery = stage_7_share_recovery(df)
    b_citalopram = stage_8_share_citalopram(df)
    b_event = stage_9_share_event_class(df)
    b_boundary = stage_10_share_per_boundary(df)

    layer_b = {
        "recovery": b_recovery,
        "citalopram": b_citalopram,
    }

    # Layer C
    stage_11_plots(out_dir, layer_a, layer_b, b_event, b_boundary)
    print("=" * 70)
    print("STAGE 12: programmatic emit (summary.json + findings.md + README.md)")
    print("=" * 70)
    emit_summary_json(out_dir, layer_a, layer_b, b_event, b_boundary, n_rows_total, n_notes_total)
    emit_findings_md(out_dir, layer_a, layer_b, b_event, b_boundary, n_rows_total, n_notes_total)
    emit_readme_md(out_dir, n_rows_total, n_notes_total)
    print()
    print("#" * 70)
    print("# Q4.7 notes_patterns RUN COMPLETE")
    print("#" * 70)
    print()


if __name__ == "__main__":
    main()
