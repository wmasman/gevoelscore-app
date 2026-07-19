"""Q24 MD-beta Stage D descriptive audit -- rest-adjacency arc under LOCKED r2.

Reproduces every count, every 2x2 contingency, every RR + Wilson 95% CI + RD +
bootstrap 95% CI + Fisher's exact p-value in the sibling descriptive_audit.md.

Anchor: docs/research/methodology/heavy_day_crash_risk_prediction.md LOCKED r2
2026-07-17. Headline cell per section 6.9 is:

    rest_day_p25_physical_strategic x heavy end_class x K=3 rest-after
    x crash-in-5d, era-pooled

with immediate era-stratified companions (pre-cital 2022-04-04 -> 2024-04-08,
post-cital 2024-04-09 -> 2026-06-05), plus companion families for:

    - very_heavy end_class sensitivity (per section 3.5.1 sensitivity cell 1)
    - crisis-rest x end_class stratified (endogeneity diagnostic;
      reciprocal definitional-pair split; NOT independent test)
    - borderline-rest x end_class stratified (descriptive-only)
    - omnibus rest_day_p25 x end_class stratified (composition-shift caveat)
    - absolute-step operand rest_day_abs_3k (moves-with-envelope artefact test)
    - K-ladder rest-after at K=1 and K=2 (tightness sensitivity)
    - rest-BEFORE-K=3 headline cell (symmetry check + endogeneity asymmetry)

Statistical machinery per MD-beta section 3.6:

    - Wilson score 95% CI on per-arm rates (small-sample-appropriate).
    - Fisher's exact two-sided p-value (reported for completeness, NOT verdict).
    - Bootstrap 95% CI on RR + RD: B = 10000 resamples, episode-level, block
      length = 1, seed = 20260716, percentile 2.5 / 97.5.
    - Haldane-Anscombe correction (+0.5 to all cells) applied to RR only when
      any cell = 0 in the raw 2x2; the raw counts + rate CIs are unchanged.

Sample-floor preflight per user Option B endorsement: informal Wilson-viable
threshold of ~10 exposed on each arm. Cells that fail are marked
NEEDS-MORE-DATA and reported as narrative-only in the audit.

Discipline: Stage D descriptive audit only per CONVENTIONS section 2.1;
descriptive-with-CI framing, no verdicts, no inferential closure. Reciprocal
definitional-pair discipline preserved per MD-beta section 3.7: strategic +
crisis reads are ONE split, not two independent tests.

Idempotent + re-runnable. Outputs land in ../output/.
"""
import math
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact
from statsmodels.stats.proportion import proportion_confint


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DATA_PATH = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH",
    "C:/Users/Gebruiker/Documents/gevoelscore-data",
))
INPUT = DATA_PATH / "unified" / "per_day_master.csv"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEAVY_CLASSES = {"heavy", "very_heavy"}
CRASH_WINDOW = 5
K_PRIMARY = 3
K_LADDER = [1, 2, 3]
RANDOM_SEED = 20260716
BOOTSTRAP_B = 10000
ALPHA = 0.05

# Era boundary per MD-beta section 5 confound 7 revision.
CITAL_BOUNDARY = pd.Timestamp("2024-04-09")

# Sample floor per user Option B.
WILSON_VIABLE_FLOOR = 10


# ---------------------------------------------------------------------------
# Data loading + operand construction
# ---------------------------------------------------------------------------

def load_lc_stratum():
    """Load per_day_master.csv, filter to LC-era, add operand columns.

    Adds:
      is_heavy, is_very_heavy, is_crash,
      rest_day_p25 (float; NaN if steps or 30d-p25 undefined),
      rest_day_abs_3k (bool; total_steps < 3000),
      gs_bucket (strategic / borderline / crisis / nan),
      rest_day_p25_physical_strategic  (True iff rest_day_p25 == 1.0 AND gs >= 5),
      rest_day_p25_physical_crisis     (True iff rest_day_p25 == 1.0 AND gs <= 3),
      rest_day_p25_physical_borderline (True iff rest_day_p25 == 1.0 AND gs == 4),
      year, era (pre_cital / post_cital).
    """
    df = pd.read_csv(INPUT, parse_dates=["date"])
    df = df[df["lc_phase"] == "lc"].copy().reset_index(drop=True)
    df["is_heavy"] = df["exertion_class_lagged_lcera"].isin(HEAVY_CLASSES)
    df["is_very_heavy"] = df["exertion_class_lagged_lcera"] == "very_heavy"
    df["is_crash"] = df["is_crash"].fillna(False).astype(bool)
    df["year"] = df["date"].dt.year

    diffs = df["date"].diff().dt.days.dropna()
    if not (diffs == 1).all():
        gap_count = int((diffs != 1).sum())
        raise RuntimeError(
            f"LC-era rows not contiguous by day; {gap_count} gap(s) detected."
        )

    steps = df["total_steps"].astype(float)
    rolling_p25 = steps.rolling(window=30, min_periods=15).quantile(0.25)
    df["rest_day_p25"] = np.where(
        steps.isna() | rolling_p25.isna(),
        np.nan,
        (steps < rolling_p25).astype(float),
    )
    df["rest_day_abs_3k"] = np.where(
        steps.isna(), np.nan, (steps < 3000).astype(float),
    )

    gs = df["gevoelscore"]
    df["gs_bucket"] = np.where(
        gs.isna(),
        "nan",
        np.where(gs >= 5, "strategic",
                 np.where(gs <= 3, "crisis", "borderline")),
    )

    is_rest_p25 = df["rest_day_p25"] == 1.0
    is_rest_abs = df["rest_day_abs_3k"] == 1.0
    df["is_physical_strategic"] = (is_rest_p25 & (df["gs_bucket"] == "strategic"))
    df["is_physical_crisis"] = (is_rest_p25 & (df["gs_bucket"] == "crisis"))
    df["is_physical_borderline"] = (is_rest_p25 & (df["gs_bucket"] == "borderline"))
    df["is_physical_strategic_abs"] = (is_rest_abs & (df["gs_bucket"] == "strategic"))

    # Wave 2C proactive-strategic reproducibility hook: strategic AND no
    # is_crash in [d-3, d-1]. This is NOT the MD-beta section 3.1.1 primary
    # operand; it is the Wave 2C 'proactive_strategic' flavour used for the
    # RR = 0.354 empirical anchor cited in MD-beta section 3.7. See Section 2
    # of the sibling audit for the operand-scope note.
    crash_arr = df["is_crash"].values
    n_rows = len(df)
    no_crash_before_3d = np.ones(n_rows, dtype=bool)
    for i in range(n_rows):
        lo = max(i - 3, 0)
        hi = i - 1
        if lo <= hi and crash_arr[lo:hi + 1].any():
            no_crash_before_3d[i] = False
    df["no_crash_before_3d"] = no_crash_before_3d
    df["is_physical_strategic_proactive"] = (
        df["is_physical_strategic"] & df["no_crash_before_3d"]
    )

    df["era"] = np.where(df["date"] < CITAL_BOUNDARY, "pre_cital", "post_cital")

    return df


# ---------------------------------------------------------------------------
# Episode construction (gap=0 contiguous heavy runs)
# ---------------------------------------------------------------------------

def build_episodes(df):
    """Emit episode table (one row per gap=0 heavy episode).

    For each K in K_LADDER, computes rest-AFTER + rest-BEFORE presence flags
    for each of five operand families:
      - omnibus p25 (rest_day_p25 == 1.0)
      - physical_strategic
      - physical_crisis
      - physical_borderline
      - absolute-step + strategic (rest_day_abs_3k == 1.0 AND gs strategic)
    """
    n = len(df)
    heavy = df["is_heavy"].values
    episodes = []
    ep_id = 0
    i = 0
    while i < n:
        if not heavy[i]:
            i += 1
            continue
        ep_id += 1
        start = i
        while i + 1 < n and heavy[i + 1]:
            i += 1
        end = i
        length = end - start + 1
        end_row = df.iloc[end]
        end_class = "very_heavy" if bool(end_row["is_very_heavy"]) else "heavy"
        d_start = df.iloc[start]["date"]
        d_end = df.iloc[end]["date"]

        # Crash-in-5d window: [end+1, end+5].
        c_lo = end + 1
        c_hi = min(end + CRASH_WINDOW, n - 1)
        if c_lo > n - 1:
            crash_in_5d = False
            crash_window_full = False
        else:
            crash_slice = df.iloc[c_lo:c_hi + 1]["is_crash"]
            crash_in_5d = bool(crash_slice.any())
            crash_window_full = (c_hi - c_lo + 1) == CRASH_WINDOW

        # Era at episode end.
        era = "pre_cital" if d_end < CITAL_BOUNDARY else "post_cital"

        record = {
            "episode_id": ep_id,
            "D_start_idx": start,
            "D_end_idx": end,
            "D_start": d_start,
            "D_end": d_end,
            "streak_length": length,
            "year_end": int(end_row["year"]),
            "end_class": end_class,
            "era": era,
            "crash_in_5d": crash_in_5d,
            "crash_window_full": crash_window_full,
        }

        for K in K_LADDER:
            record.update(_rest_flags(df, start, end, K, n))

        episodes.append(record)
        i = end + 1

    return pd.DataFrame(episodes)


def _rest_flags(df, start, end, K, n):
    """Compute rest-AFTER and rest-BEFORE presence flags at window K.

    Emits per (K, direction, operand):
      _true  -> True iff any qualifying day in window
      _undef -> True iff window truncated OR (no True found AND any NaN in
                p25 window). Follows the parent Wave 2B/2C discipline.

    For _abs_3k operand, the NaN condition rests on rest_day_abs_3k NaN
    (i.e. total_steps NaN); analogous rule.
    """
    out = {}

    # --- AFTER window [end+1, end+K] ---
    r_lo = end + 1
    r_hi = min(end + K, n - 1)
    if r_lo > n - 1:
        after_window = df.iloc[0:0]
        truncated_after = True
    else:
        after_window = df.iloc[r_lo:r_hi + 1]
        truncated_after = (end + K) > n - 1

    out.update(_flags_for_window(
        after_window, "after", K, truncated_after, has_window=(r_lo <= n - 1),
    ))

    # --- BEFORE window [start-K, start-1] ---
    b_lo = max(start - K, 0)
    b_hi = start - 1
    if b_hi < 0:
        before_window = df.iloc[0:0]
        truncated_before = True
    else:
        before_window = df.iloc[b_lo:b_hi + 1]
        truncated_before = (start - K) < 0

    out.update(_flags_for_window(
        before_window, "before", K, truncated_before, has_window=(b_hi >= 0),
    ))
    return out


def _flags_for_window(window, direction, K, truncated, has_window):
    """Emit per-operand flags for a rest-window slice.

    _true is bool for the observed-True case; _undef is bool for truncated OR
    (no True found AND any NaN in the p25 operand within the window). We treat
    _undef as True only when we cannot rule out that the window contains a
    rest-day. This matches the parent Wave 2B / Wave 2C discipline.
    """
    flags = {}
    if not has_window or len(window) == 0:
        flags[f"rest_{direction}_{K}_p25_true"] = False
        flags[f"rest_{direction}_{K}_p25_undef"] = True
        flags[f"rest_{direction}_{K}_strategic_true"] = False
        flags[f"rest_{direction}_{K}_strategic_undef"] = True
        flags[f"rest_{direction}_{K}_crisis_true"] = False
        flags[f"rest_{direction}_{K}_crisis_undef"] = True
        flags[f"rest_{direction}_{K}_borderline_true"] = False
        flags[f"rest_{direction}_{K}_borderline_undef"] = True
        flags[f"rest_{direction}_{K}_abs3k_strategic_true"] = False
        flags[f"rest_{direction}_{K}_abs3k_strategic_undef"] = True
        flags[f"rest_{direction}_{K}_strategic_proactive_true"] = False
        flags[f"rest_{direction}_{K}_strategic_proactive_undef"] = True
        return flags

    p25_col = window["rest_day_p25"]
    abs_col = window["rest_day_abs_3k"]
    strategic_col = window["is_physical_strategic"]
    crisis_col = window["is_physical_crisis"]
    borderline_col = window["is_physical_borderline"]
    abs_strat_col = window["is_physical_strategic_abs"]
    strat_proactive_col = window["is_physical_strategic_proactive"]

    # Omnibus p25.
    p25_true = bool((p25_col == 1.0).any())
    p25_any_nan = bool(p25_col.isna().any())
    flags[f"rest_{direction}_{K}_p25_true"] = p25_true
    flags[f"rest_{direction}_{K}_p25_undef"] = (
        (not p25_true) and (truncated or p25_any_nan)
    )

    # Strategic (physical rest AND gs >= 5).
    strat_true = bool(strategic_col.any())
    flags[f"rest_{direction}_{K}_strategic_true"] = strat_true
    flags[f"rest_{direction}_{K}_strategic_undef"] = (
        (not strat_true) and (truncated or p25_any_nan)
    )

    # Crisis.
    crisis_true = bool(crisis_col.any())
    flags[f"rest_{direction}_{K}_crisis_true"] = crisis_true
    flags[f"rest_{direction}_{K}_crisis_undef"] = (
        (not crisis_true) and (truncated or p25_any_nan)
    )

    # Borderline.
    border_true = bool(borderline_col.any())
    flags[f"rest_{direction}_{K}_borderline_true"] = border_true
    flags[f"rest_{direction}_{K}_borderline_undef"] = (
        (not border_true) and (truncated or p25_any_nan)
    )

    # Absolute-step strategic.
    abs_any_nan = bool(abs_col.isna().any())
    abs_strat_true = bool(abs_strat_col.any())
    flags[f"rest_{direction}_{K}_abs3k_strategic_true"] = abs_strat_true
    flags[f"rest_{direction}_{K}_abs3k_strategic_undef"] = (
        (not abs_strat_true) and (truncated or abs_any_nan)
    )

    # Wave 2C proactive-strategic (strategic AND no crash in prior 3d on the
    # rest-day). Used for the RR = 0.354 anchor reproduction only.
    strat_proactive_true = bool(strat_proactive_col.any())
    flags[f"rest_{direction}_{K}_strategic_proactive_true"] = strat_proactive_true
    flags[f"rest_{direction}_{K}_strategic_proactive_undef"] = (
        (not strat_proactive_true) and (truncated or p25_any_nan)
    )

    return flags


# ---------------------------------------------------------------------------
# Statistical machinery
# ---------------------------------------------------------------------------

def wilson_ci(k, n):
    """Wilson 95% CI via statsmodels."""
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    lo, hi = proportion_confint(k, n, alpha=ALPHA, method="wilson")
    return (k / n, float(lo), float(hi))


def _rr_rd(k_t, n_t, k_f, n_f, haldane_if_zero=True):
    """Compute RR + RD; apply Haldane if any raw cell is 0 AND haldane requested.

    Returns dict with:
      rate_t, rate_f, rr, rd, haldane_applied.
    Cell interpretation: exposed arm (T) with k_t crashes out of n_t; unexposed
    arm (F) with k_f crashes out of n_f.
    """
    a = k_t
    b = n_t - k_t
    c = k_f
    d = n_f - k_f
    haldane = False
    if haldane_if_zero and (a == 0 or b == 0 or c == 0 or d == 0):
        haldane = True
        a_h, b_h, c_h, d_h = a + 0.5, b + 0.5, c + 0.5, d + 0.5
        rate_t_h = a_h / (a_h + b_h)
        rate_f_h = c_h / (c_h + d_h)
        rr = rate_t_h / rate_f_h if rate_f_h > 0 else float("nan")
    else:
        rate_t_h = a / (a + b) if (a + b) > 0 else float("nan")
        rate_f_h = c / (c + d) if (c + d) > 0 else float("nan")
        rr = (rate_t_h / rate_f_h) if (rate_f_h and rate_f_h > 0) else float("nan")
    rate_t = a / n_t if n_t > 0 else float("nan")
    rate_f = c / n_f if n_f > 0 else float("nan")
    rd = (rate_t - rate_f) if not (math.isnan(rate_t) or math.isnan(rate_f)) else float("nan")
    return {
        "rate_t": rate_t,
        "rate_f": rate_f,
        "rr": rr,
        "rd": rd,
        "haldane_applied": haldane,
    }


def fisher_p(k_t, n_t, k_f, n_f):
    """Two-sided Fisher's exact p-value on the 2x2. Descriptive-only per
    CONVENTIONS section 2.1; not a verdict."""
    a = k_t
    b = n_t - k_t
    c = k_f
    d = n_f - k_f
    try:
        _, p = fisher_exact([[a, b], [c, d]], alternative="two-sided")
        return float(p)
    except Exception:
        return float("nan")


def bootstrap_rr_rd_ci(exposed_flags, crash_flags, B=BOOTSTRAP_B, seed=RANDOM_SEED):
    """Episode-level bootstrap 95% CI on RR + RD.

    Block length = 1 per parent MD section 7.10 argument that episode-ends are
    approximately independent under the strict-clean policy; the Stage D
    primary contrast uses the all-episodes pool per MD section 3.10 primary.

    Resamples n=n_episodes with replacement each round; computes RR + RD each
    round; percentile 2.5 / 97.5. Rounds where either arm has 0 exposed or 0
    unexposed are skipped in the RR percentile (RD is still valid at 0-arm),
    but flagged in count. If < 100 valid rounds accumulate, CI is NaN + flagged.
    """
    exposed_flags = np.asarray(exposed_flags, dtype=bool)
    crash_flags = np.asarray(crash_flags, dtype=bool)
    n = len(exposed_flags)
    if n == 0:
        return {
            "rr_lo": float("nan"), "rr_hi": float("nan"),
            "rd_lo": float("nan"), "rd_hi": float("nan"),
            "rr_valid_rounds": 0, "rd_valid_rounds": 0,
        }
    rng = np.random.default_rng(seed)
    rrs = []
    rds = []
    for _ in range(B):
        idx = rng.integers(0, n, size=n)
        exp_b = exposed_flags[idx]
        crash_b = crash_flags[idx]
        n_t = int(exp_b.sum())
        n_f = n - n_t
        k_t = int(crash_b[exp_b].sum())
        k_f = int(crash_b[~exp_b].sum())
        if n_t > 0 and n_f > 0:
            rate_t = k_t / n_t
            rate_f = k_f / n_f
            rds.append(rate_t - rate_f)
            if rate_f > 0:
                rrs.append(rate_t / rate_f)
    if len(rrs) >= 100:
        rr_lo, rr_hi = np.percentile(rrs, [2.5, 97.5])
    else:
        rr_lo, rr_hi = float("nan"), float("nan")
    if len(rds) >= 100:
        rd_lo, rd_hi = np.percentile(rds, [2.5, 97.5])
    else:
        rd_lo, rd_hi = float("nan"), float("nan")
    return {
        "rr_lo": float(rr_lo), "rr_hi": float(rr_hi),
        "rd_lo": float(rd_lo), "rd_hi": float(rd_hi),
        "rr_valid_rounds": len(rrs), "rd_valid_rounds": len(rds),
    }


# ---------------------------------------------------------------------------
# Cell reporting scaffold
# ---------------------------------------------------------------------------

def compute_cell(episodes, exposed_col, cell_label, extra_meta=None,
                 undef_col=None):
    """Compute the full 2x2 + RR + Wilson CIs + bootstrap CI + Fisher p for one
    cell definition. Filters episodes to those with full crash window + not-NaN
    exposed indicator + defined exposed operand (undef_col == False when
    supplied). Returns dict ready to write as a CSV row.

    exposed_col: bool column name on `episodes` (True = exposed).
    undef_col:   bool column name (True = operand undefined for this episode).
                 If provided, episodes where undef_col == True AND
                 exposed_col == False are dropped (undef-True cases remain,
                 because a True observed rest-day resolves the ambiguity).
    """
    n_input = len(episodes)
    sub = episodes.dropna(subset=[exposed_col]).copy()
    sub = sub[sub["crash_window_full"] == True].copy()
    if undef_col is not None and undef_col in sub.columns:
        drop_mask = (sub[undef_col] == True) & (sub[exposed_col] == False)
        sub = sub[~drop_mask].copy()
    exp = sub[exposed_col].astype(bool).values
    crash = sub["crash_in_5d"].astype(bool).values

    n_t = int(exp.sum())
    n_f = int(len(exp) - n_t)
    k_t = int(crash[exp].sum())
    k_f = int(crash[~exp].sum())

    rate_t, lo_t, hi_t = wilson_ci(k_t, n_t)
    rate_f, lo_f, hi_f = wilson_ci(k_f, n_f)
    rrrd = _rr_rd(k_t, n_t, k_f, n_f)
    fp = fisher_p(k_t, n_t, k_f, n_f)

    floor_pass = (n_t >= WILSON_VIABLE_FLOOR) and (n_f >= WILSON_VIABLE_FLOOR)
    if floor_pass:
        boot = bootstrap_rr_rd_ci(exp, crash)
    else:
        boot = {
            "rr_lo": float("nan"), "rr_hi": float("nan"),
            "rd_lo": float("nan"), "rd_hi": float("nan"),
            "rr_valid_rounds": 0, "rd_valid_rounds": 0,
        }

    row = {
        "cell": cell_label,
        "n_episodes_input": n_input,
        "n_episodes_used": len(sub),
        "exposed_true_n": n_t,
        "exposed_false_n": n_f,
        "exposed_true_crash": k_t,
        "exposed_false_crash": k_f,
        "rate_exposed_true": rate_t,
        "rate_exposed_true_wilson_lo": lo_t,
        "rate_exposed_true_wilson_hi": hi_t,
        "rate_exposed_false": rate_f,
        "rate_exposed_false_wilson_lo": lo_f,
        "rate_exposed_false_wilson_hi": hi_f,
        "risk_ratio": rrrd["rr"],
        "risk_ratio_boot_lo": boot["rr_lo"],
        "risk_ratio_boot_hi": boot["rr_hi"],
        "risk_ratio_boot_valid_rounds": boot["rr_valid_rounds"],
        "risk_difference": rrrd["rd"],
        "risk_difference_boot_lo": boot["rd_lo"],
        "risk_difference_boot_hi": boot["rd_hi"],
        "risk_difference_boot_valid_rounds": boot["rd_valid_rounds"],
        "haldane_applied": rrrd["haldane_applied"],
        "fisher_exact_p_two_sided": fp,
        "wilson_viable_floor_pass": floor_pass,
    }
    if extra_meta:
        row.update(extra_meta)
    return row


# ---------------------------------------------------------------------------
# Reporting sections
# ---------------------------------------------------------------------------

def _era_filter(episodes, era):
    """Filter episodes on era column (pre_cital / post_cital / ALL)."""
    if era == "ALL":
        return episodes
    return episodes[episodes["era"] == era]


def _end_class_filter(episodes, end_class):
    if end_class == "ALL":
        return episodes
    return episodes[episodes["end_class"] == end_class]


def _write_rows(rows, path):
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return df


def preflight_probe(episodes):
    """Enumerate expected n per cell across headline + all companion families,
    apply the Wilson-viable floor, and emit the preflight table.

    One row per (family, cell) with:
      n_episodes_input, exposed_true_n, exposed_false_n, floor_pass.
    """
    rows = []

    def _add(family, cell_label, sub, exposed_col):
        s = sub.dropna(subset=[exposed_col])
        s = s[s["crash_window_full"] == True]
        exp = s[exposed_col].astype(bool)
        n_t = int(exp.sum())
        n_f = int((~exp).sum())
        k_t = int(s.loc[exp, "crash_in_5d"].sum()) if n_t else 0
        k_f = int(s.loc[~exp, "crash_in_5d"].sum()) if n_f else 0
        floor_pass = (n_t >= WILSON_VIABLE_FLOOR) and (n_f >= WILSON_VIABLE_FLOOR)
        rows.append({
            "family": family,
            "cell": cell_label,
            "n_episodes_available": len(s),
            "exposed_true_n": n_t,
            "exposed_false_n": n_f,
            "exposed_true_crash": k_t,
            "exposed_false_crash": k_f,
            "wilson_viable_floor_pass": floor_pass,
        })

    for era in ["ALL", "pre_cital", "post_cital"]:
        for ec in ["heavy", "very_heavy"]:
            sub = _end_class_filter(_era_filter(episodes, era), ec)
            for op_name, col in [
                ("strategic_p25", "rest_after_3_strategic_true"),
                ("crisis_p25", "rest_after_3_crisis_true"),
                ("borderline_p25", "rest_after_3_borderline_true"),
                ("omnibus_p25", "rest_after_3_p25_true"),
                ("strategic_abs3k", "rest_after_3_abs3k_strategic_true"),
            ]:
                _add(
                    op_name,
                    f"K=3 rest-after, era={era}, end_class={ec}",
                    sub, col,
                )

    for K in K_LADDER:
        for ec in ["heavy"]:
            sub = _end_class_filter(episodes, ec)
            _add(
                "strategic_p25",
                f"K={K} rest-after, era=ALL, end_class={ec}",
                sub, f"rest_after_{K}_strategic_true",
            )

    for era in ["ALL", "pre_cital", "post_cital"]:
        for ec in ["heavy"]:
            sub = _end_class_filter(_era_filter(episodes, era), ec)
            _add(
                "strategic_p25",
                f"K=3 rest-BEFORE, era={era}, end_class={ec}",
                sub, "rest_before_3_strategic_true",
            )

    return _write_rows(rows, OUTPUT_DIR / "preflight_sample_floor.csv")


def headline_cell_and_era_stratified(episodes):
    """Section 3 + Section 4: strategic x heavy x K=3 rest-after x crash-in-5d
    era-pooled + immediate pre-cital + post-cital companions."""
    rows = []
    for era_label in ["ALL", "pre_cital", "post_cital"]:
        sub = _era_filter(episodes, era_label)
        sub = _end_class_filter(sub, "heavy")
        rows.append(compute_cell(
            sub, "rest_after_3_strategic_true",
            f"headline_strategic_heavy_K3_after_era_{era_label}",
            extra_meta={
                "era": era_label,
                "end_class": "heavy",
                "operand": "rest_day_p25_physical_strategic",
                "K": 3,
                "direction": "after",
            },
            undef_col="rest_after_3_strategic_undef",
        ))
    return _write_rows(rows, OUTPUT_DIR / "headline_strategic_heavy_K3_after.csv")


def very_heavy_sensitivity(episodes):
    """Section 5: strategic x very_heavy end_class x K=3 x crash-in-5d,
    era-pooled + stratified."""
    rows = []
    for era_label in ["ALL", "pre_cital", "post_cital"]:
        sub = _era_filter(episodes, era_label)
        sub = _end_class_filter(sub, "very_heavy")
        rows.append(compute_cell(
            sub, "rest_after_3_strategic_true",
            f"sens_strategic_very_heavy_K3_after_era_{era_label}",
            extra_meta={
                "era": era_label,
                "end_class": "very_heavy",
                "operand": "rest_day_p25_physical_strategic",
                "K": 3,
                "direction": "after",
            },
            undef_col="rest_after_3_strategic_undef",
        ))
    return _write_rows(rows, OUTPUT_DIR / "sens_strategic_very_heavy_K3_after.csv")


def crisis_by_end_class(episodes):
    """Section 6: crisis-rest x {heavy, very_heavy} x K=3 rest-after
    x crash-in-5d, era-pooled + stratified.

    Reciprocal-attestation reminder: strategic + crisis are ONE
    definitional-pair split per MD-beta section 3.7, NOT two independent tests.
    """
    rows = []
    for ec in ["heavy", "very_heavy"]:
        for era_label in ["ALL", "pre_cital", "post_cital"]:
            sub = _era_filter(episodes, era_label)
            sub = _end_class_filter(sub, ec)
            rows.append(compute_cell(
                sub, "rest_after_3_crisis_true",
                f"crisis_{ec}_K3_after_era_{era_label}",
                extra_meta={
                    "era": era_label,
                    "end_class": ec,
                    "operand": "rest_day_p25_physical_crisis",
                    "K": 3,
                    "direction": "after",
                },
                undef_col="rest_after_3_crisis_undef",
            ))
    return _write_rows(rows, OUTPUT_DIR / "crisis_by_end_class_K3_after.csv")


def borderline_by_end_class(episodes):
    """Section 7: borderline-rest x {heavy, very_heavy} x K=3 rest-after
    x crash-in-5d, era-pooled. Descriptive-only per MD-beta section 3.1.1."""
    rows = []
    for ec in ["heavy", "very_heavy"]:
        sub = _end_class_filter(episodes, ec)
        rows.append(compute_cell(
            sub, "rest_after_3_borderline_true",
            f"borderline_{ec}_K3_after_era_ALL",
            extra_meta={
                "era": "ALL",
                "end_class": ec,
                "operand": "rest_day_p25_physical_borderline",
                "K": 3,
                "direction": "after",
            },
            undef_col="rest_after_3_borderline_undef",
        ))
    return _write_rows(rows, OUTPUT_DIR / "borderline_by_end_class_K3_after.csv")


def omnibus_by_end_class(episodes):
    """Section 8: omnibus rest_day_p25 x {heavy, very_heavy} x K=3 rest-after
    x crash-in-5d, era-pooled + stratified.

    Emits an era=ALL, end_class=ALL 'whole-pool' anchor row to reproduce
    MD-beta section 6.6 K=3 rest-after 2x2 byte-for-byte (100/12/168/34,
    RR = 1.57)."""
    rows = []
    for ec in ["heavy", "very_heavy", "ALL"]:
        for era_label in ["ALL", "pre_cital", "post_cital"]:
            sub = _era_filter(episodes, era_label)
            sub = _end_class_filter(sub, ec)
            rows.append(compute_cell(
                sub, "rest_after_3_p25_true",
                f"omnibus_{ec}_K3_after_era_{era_label}",
                extra_meta={
                    "era": era_label,
                    "end_class": ec,
                    "operand": "rest_day_p25 (omnibus, NaN=False per MD-beta 3.10)",
                    "K": 3,
                    "direction": "after",
                },
                # MD-beta 6.6 baseline uses NaN=False convention per 3.10;
                # do NOT drop undef so the 100/12/168/34 anchor reproduces
                # byte-for-byte.
                undef_col=None,
            ))
    return _write_rows(rows, OUTPUT_DIR / "omnibus_by_end_class_K3_after.csv")


def abs_step_operand(episodes):
    """Section 9: absolute-step operand sensitivity. rest_day_abs_3k AND
    gs strategic; heavy end_class; K=3 rest-after; era-pooled."""
    rows = []
    for era_label in ["ALL"]:
        sub = _era_filter(episodes, era_label)
        sub = _end_class_filter(sub, "heavy")
        rows.append(compute_cell(
            sub, "rest_after_3_abs3k_strategic_true",
            f"abs3k_strategic_heavy_K3_after_era_{era_label}",
            extra_meta={
                "era": era_label,
                "end_class": "heavy",
                "operand": "rest_day_abs_3k (steps<3000) AND gs strategic",
                "K": 3,
                "direction": "after",
            },
            undef_col="rest_after_3_abs3k_strategic_undef",
        ))
    return _write_rows(rows, OUTPUT_DIR / "abs3k_strategic_heavy_K3_after.csv")


def k_ladder(episodes):
    """Section 10: strategic x heavy x K in {1,2,3} rest-after x crash-in-5d,
    era-pooled. Reads the tightness-of-adjacency sensitivity per MD-beta
    section 3.2."""
    rows = []
    for K in K_LADDER:
        sub = _end_class_filter(episodes, "heavy")
        rows.append(compute_cell(
            sub, f"rest_after_{K}_strategic_true",
            f"kladder_strategic_heavy_K{K}_after_era_ALL",
            extra_meta={
                "era": "ALL",
                "end_class": "heavy",
                "operand": "rest_day_p25_physical_strategic",
                "K": K,
                "direction": "after",
            },
            undef_col=f"rest_after_{K}_strategic_undef",
        ))
    return _write_rows(rows, OUTPUT_DIR / "kladder_strategic_heavy_after.csv")


def rest_before(episodes):
    """Section 11: rest-BEFORE-heavy K=3 companion. strategic x heavy x K=3
    rest-BEFORE x crash-in-5d, era-pooled + stratified."""
    rows = []
    for era_label in ["ALL", "pre_cital", "post_cital"]:
        sub = _era_filter(episodes, era_label)
        sub = _end_class_filter(sub, "heavy")
        rows.append(compute_cell(
            sub, "rest_before_3_strategic_true",
            f"restbefore_strategic_heavy_K3_before_era_{era_label}",
            extra_meta={
                "era": era_label,
                "end_class": "heavy",
                "operand": "rest_day_p25_physical_strategic",
                "K": 3,
                "direction": "before",
            },
            undef_col="rest_before_3_strategic_undef",
        ))
    return _write_rows(rows, OUTPUT_DIR / "restbefore_strategic_heavy_K3.csv")


def wave2c_reproduction_check(episodes):
    """Spot-check: reproduce Wave 2C proactive-strategic pooled RR = 0.354 on
    the strategic pool restricted to ALL end_class (not just heavy).

    Note on operand-scope: MD-beta section 3.1.1 defines the primary operand
    `rest_day_p25_physical_strategic` as (rest_day_p25 True AND gs >= 5). The
    Wave 2C empirical anchor of RR = 0.354 was computed against the Wave 2C
    'proactive_strategic' flavour, which layers an additional 'no is_crash in
    [rest_day - 3, rest_day - 1]' filter on top. Both variants are reported
    here: the pure-strategic (matches MD-beta section 3.1.1 operand
    definition) and the proactive-strategic (matches Wave 2C script and the
    MD-beta section 3.7 empirical anchor citation)."""
    sub = _end_class_filter(episodes, "ALL")
    rows = []
    rows.append(compute_cell(
        sub, "rest_after_3_strategic_true",
        "wave2c_spot_pure_strategic_ALL_endclass_K3_after_era_ALL",
        extra_meta={
            "era": "ALL",
            "end_class": "ALL",
            "operand": "rest_day_p25_physical_strategic (MD-beta 3.1.1)",
            "K": 3,
            "direction": "after",
            "anchor": "MD-beta 3.1.1 pure-strategic operand definition",
        },
        undef_col="rest_after_3_strategic_undef",
    ))
    rows.append(compute_cell(
        sub, "rest_after_3_strategic_proactive_true",
        "wave2c_spot_proactive_strategic_ALL_endclass_K3_after_era_ALL",
        extra_meta={
            "era": "ALL",
            "end_class": "ALL",
            "operand": "proactive_strategic (Wave 2C: strategic AND no is_crash in [d-3, d-1])",
            "K": 3,
            "direction": "after",
            "anchor": "wave2c/output/proactive_strategic_rest_crash_2x2.csv ALL_ERA_POOLED (RR=0.3537)",
        },
        undef_col="rest_after_3_strategic_proactive_undef",
    ))
    return _write_rows(rows, OUTPUT_DIR / "wave2c_reproduction_spotcheck.csv")


def aggregated_summary(all_dfs, headline_row):
    """Aggregate one row per cell across all sections into a single summary
    CSV. Used by the descriptive_audit.md to walk headline + companions in
    one glance."""
    frames = []
    for df in all_dfs:
        frames.append(df)
    agg = pd.concat(frames, ignore_index=True)
    agg.to_csv(OUTPUT_DIR / "aggregated_summary.csv", index=False)
    return agg


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    df = load_lc_stratum()
    print(f"[stratum] LC-era rows: {len(df)}")
    print(f"[stratum] heavy: {int(df['is_heavy'].sum())} "
          f"(vh={int(df['is_very_heavy'].sum())}); "
          f"crash: {int(df['is_crash'].sum())}; "
          f"gs valid: {int(df['gevoelscore'].notna().sum())} / {len(df)}")
    print(f"[stratum] rest_day_p25 True: "
          f"{int((df['rest_day_p25'] == 1.0).sum())} "
          f"NaN: {int(df['rest_day_p25'].isna().sum())}")

    episodes = build_episodes(df)
    print(f"[episodes] gap=0 heavy episodes: {len(episodes)}")
    print(f"[episodes] end_class heavy: "
          f"{int((episodes['end_class'] == 'heavy').sum())}; "
          f"very_heavy: {int((episodes['end_class'] == 'very_heavy').sum())}")
    print(f"[episodes] era pre_cital: "
          f"{int((episodes['era'] == 'pre_cital').sum())}; "
          f"post_cital: {int((episodes['era'] == 'post_cital').sum())}")
    print(f"[episodes] crash_in_5d True: "
          f"{int(episodes['crash_in_5d'].sum())} / {len(episodes)}")

    # Persist episode table for audit hooks.
    episodes.drop(columns=["D_start_idx", "D_end_idx"]).to_csv(
        OUTPUT_DIR / "episode_table.csv", index=False,
    )

    # Preflight sample-floor probe (Section 1 of the audit).
    preflight = preflight_probe(episodes)
    print(f"[preflight] {len(preflight)} cells; "
          f"pass: {int(preflight['wilson_viable_floor_pass'].sum())}; "
          f"fail: {int((~preflight['wilson_viable_floor_pass']).sum())}")

    # Full 2x2 computations.
    headline = headline_cell_and_era_stratified(episodes)
    print(f"[headline] {len(headline)} cells written")

    vh_sens = very_heavy_sensitivity(episodes)
    crisis = crisis_by_end_class(episodes)
    borderline = borderline_by_end_class(episodes)
    omnibus = omnibus_by_end_class(episodes)
    abs_step = abs_step_operand(episodes)
    kladder = k_ladder(episodes)
    before = rest_before(episodes)

    # Wave 2C reproduction spot-check.
    w2c = wave2c_reproduction_check(episodes)

    # Aggregated summary.
    agg = aggregated_summary(
        [headline, vh_sens, crisis, borderline, omnibus, abs_step, kladder, before, w2c],
        headline_row=headline.iloc[0].to_dict(),
    )
    print(f"[aggregated] {len(agg)} cell rows across all sections")

    # Reproduce MD-beta section 6.6 baseline 2x2 for byte-for-byte check.
    baseline_row = omnibus[
        (omnibus["end_class"] == "ALL") & (omnibus["era"] == "ALL")
    ].iloc[0]
    print(f"[md_beta_6.6_baseline] "
          f"exposed_true(rest_after) n={int(baseline_row['exposed_true_n'])} "
          f"crash={int(baseline_row['exposed_true_crash'])}; "
          f"exposed_false n={int(baseline_row['exposed_false_n'])} "
          f"crash={int(baseline_row['exposed_false_crash'])}; "
          f"RR={baseline_row['risk_ratio']:.4f}")

    hl = headline[headline["era"] == "ALL"].iloc[0]
    print(f"[headline_cell] "
          f"strategic n={int(hl['exposed_true_n'])} "
          f"crash={int(hl['exposed_true_crash'])} "
          f"rate={hl['rate_exposed_true']:.4f} "
          f"[{hl['rate_exposed_true_wilson_lo']:.4f}, "
          f"{hl['rate_exposed_true_wilson_hi']:.4f}]; "
          f"complement n={int(hl['exposed_false_n'])} "
          f"crash={int(hl['exposed_false_crash'])} "
          f"rate={hl['rate_exposed_false']:.4f} "
          f"[{hl['rate_exposed_false_wilson_lo']:.4f}, "
          f"{hl['rate_exposed_false_wilson_hi']:.4f}]; "
          f"RR={hl['risk_ratio']:.4f} "
          f"boot[{hl['risk_ratio_boot_lo']}, {hl['risk_ratio_boot_hi']}]; "
          f"RD={hl['risk_difference']:.4f}")

    print(f"\n[write] outputs in {OUTPUT_DIR}")
    for f in sorted(OUTPUT_DIR.glob("*.csv")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
