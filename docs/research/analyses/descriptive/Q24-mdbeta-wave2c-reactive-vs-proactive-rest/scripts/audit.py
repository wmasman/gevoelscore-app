"""Q24 MD-beta Wave 2C descriptive audit -- reactive vs proactive rest.

Wave 2C sibling of the parent Q24 MD-beta Stage -1 audit
(../Q24-mdbeta-precursor-rest-streak/audit.md LOCKED r1 2026-07-16).

Tests two substantive interpretations of the parent Wave 2B era-stratified
sign-inversion finding:

  Interpretation A -- the 2023-24 sign-inversion (RR = 2.02 / 1.56) vs
    2025-26 sign-flip (RR = 0.78 / 0.57) reflects a shift in rest-day
    composition from crisis-dominant early to strategic-dominant late.
    Gevoelscore-on-rest-day is the discriminator (>= 5 strategic; <= 3
    crisis; 4 borderline). Confounding-by-indication mechanism (Salas
    2001; Kyriacou & Lewis 2016 JAMA) predicts crisis-rest carries the
    endogeneity signature; strategic-rest is a partial mitigation.

  Interpretation D -- the 2025-26 crash-rate collapse reflects load-
    envelope shrinkage (fewer very-heavy days) and narrower step
    envelopes over time (tactical Garmin use improvement proxy).

Semantic constraint per memory project_rest_day_operand_semantics: the
MD-beta rest_day_p25 operand measures physical rest only
(total_steps < 30d rolling p25). Gevoelscore modulates the interpretation
of the rest-day but does NOT change what the operand measures. Every
rest-day is a low-step day by definition.

Outputs are written to ../output/ and consumed by the sibling audit.md
descriptive card. This script is idempotent and re-runnable.

Frame: LC-era stratum (lc_phase == 'lc'), matches parent Wave 2B stratum.
Heavy-day definition: exertion_class_lagged_lcera in {heavy, very_heavy}.
Rest-day primary: total_steps < rolling_percentile_25(total_steps, 30d,
  min_periods=15).
Episode: gap=0 contiguous heavy-day run.
crash_in_5d(D_end) = any(is_crash[d] for d in [D_end+1, D_end+5]).

Stage -1 descriptive audit only. NO inferential tests; no verdicts.
Wilson 95% CI on rates; RR + RD reported with per-arm arms context.
"""
import os
import math
from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH",
    "C:/Users/Gebruiker/Documents/gevoelscore-data",
))
INPUT = DATA_PATH / "unified" / "per_day_master.csv"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEAVY_CLASSES = {"heavy", "very_heavy"}
REST_CLASSES = {"none", "light"}
CRASH_WINDOW = 5
K_REST_AFTER = 3     # MD-beta section 3.2 primary K value
LOOKBACK_CRASH = 3   # rest-day quadrant: is_crash in [rest_day - 3, rest_day - 1]
RANDOM_SEED = 20260716  # per MD-beta section 3.6; unused in Wave 2C.


# ---------------------------------------------------------------------------
# Data loading + rest-day + gevoelscore-bucket construction
# ---------------------------------------------------------------------------

def load_lc_stratum():
    """Load per_day_master.csv, filter to LC-era, add heavy / rest / bucket cols."""
    df = pd.read_csv(INPUT, parse_dates=["date"])
    df = df[df["lc_phase"] == "lc"].copy().reset_index(drop=True)
    df["is_heavy"] = df["exertion_class_lagged_lcera"].isin(HEAVY_CLASSES)
    df["is_very_heavy"] = df["exertion_class_lagged_lcera"] == "very_heavy"
    df["is_heavy_only"] = df["exertion_class_lagged_lcera"] == "heavy"
    df["is_crash"] = df["is_crash"].fillna(False).astype(bool)
    df["year"] = df["date"].dt.year

    # Guard: LC-era must be contiguous (parent audit assumption).
    diffs = df["date"].diff().dt.days.dropna()
    if not (diffs == 1).all():
        gap_count = int((diffs != 1).sum())
        raise RuntimeError(
            f"LC-era rows are not contiguous by day; {gap_count} gap(s) detected."
        )

    steps = df["total_steps"].astype(float)
    rolling_p25 = steps.rolling(window=30, min_periods=15).quantile(0.25)
    df["rest_day_p25_threshold"] = rolling_p25
    df["rest_day_p25"] = np.where(
        steps.isna() | rolling_p25.isna(),
        np.nan,
        (steps < rolling_p25).astype(float),
    )

    # Gevoelscore bucket per memory project_rest_day_operand_semantics:
    #   >= 5 -> strategic; == 4 -> borderline; <= 3 -> crisis; NaN -> nan.
    gs = df["gevoelscore"]
    df["gs_bucket"] = np.where(
        gs.isna(),
        "nan",
        np.where(gs >= 5, "strategic",
                 np.where(gs <= 3, "crisis", "borderline")),
    )
    return df


# ---------------------------------------------------------------------------
# Episode construction (gap=0 contiguous heavy runs)
# ---------------------------------------------------------------------------

def build_episodes(df):
    """Emit episode table (one row per gap=0 heavy episode).

    Columns include D_start, D_end, streak_length, year_end, end_class,
    crash_in_5d, crash_window_full, and for K=3 rest-after primary: the
    list of rest-day indices in the [D_end+1, D_end+3] window (used by the
    quadrant + strategic-subset builders below).
    """
    heavy = df["is_heavy"].values
    n = len(df)
    episodes = []
    i = 0
    ep_id = 0
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

        # crash_in_5d + crash_window_full flag.
        c_lo = end + 1
        c_hi = min(end + CRASH_WINDOW, n - 1)
        if c_lo > n - 1:
            crash_in_5d = False
            has_window_data = False
        else:
            crash_slice = df.iloc[c_lo:c_hi + 1]["is_crash"]
            crash_in_5d = bool(crash_slice.any())
            has_window_data = (c_hi - c_lo + 1) == CRASH_WINDOW

        # K=3 rest-after primary: list of rest-day *indices* in [end+1, end+3].
        r_lo = end + 1
        r_hi = min(end + K_REST_AFTER, n - 1)
        rest_indices = []
        rest_after_undefined = False
        if r_lo > n - 1:
            rest_after_undefined = True
        else:
            window = df.iloc[r_lo:r_hi + 1]
            # Rest-day True indices.
            for idx in window.index:
                val = df.loc[idx, "rest_day_p25"]
                if val == 1.0:
                    rest_indices.append(int(idx))
            # If window truncated OR any NaN in operand and no True found,
            # the rest-after indicator is NaN per parent-audit discipline.
            if len(rest_indices) == 0:
                truncated = (end + K_REST_AFTER) > n - 1
                any_nan = window["rest_day_p25"].isna().any()
                if truncated or any_nan:
                    rest_after_undefined = True

        rest_after_true = len(rest_indices) > 0
        rest_after_indicator = (
            np.nan if rest_after_undefined and not rest_after_true
            else bool(rest_after_true)
        )

        episodes.append({
            "episode_id": ep_id,
            "D_start_idx": start,
            "D_end_idx": end,
            "D_start": df.iloc[start]["date"],
            "D_end": df.iloc[end]["date"],
            "streak_length": length,
            "year_end": int(end_row["year"]),
            "end_class": end_class,
            "crash_in_5d": crash_in_5d,
            "crash_window_full": has_window_data,
            "rest_after_3_primary": rest_after_indicator,
            "rest_indices_after_K3": rest_indices,  # list; may be empty
        })
        i = end + 1
    return pd.DataFrame(episodes)


# ---------------------------------------------------------------------------
# Wilson score CI for a proportion
# ---------------------------------------------------------------------------

def wilson_ci(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    denom = 1.0 + z ** 2 / n
    centre = (p + z ** 2 / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2))) / denom
    return (p, centre - half, centre + half)


# ---------------------------------------------------------------------------
# Rest-day quadrant classifier (crash-before-3d x gevoelscore-bucket)
# ---------------------------------------------------------------------------

def _crash_in_lookback(df, rest_idx, lookback=LOOKBACK_CRASH):
    """True if is_crash in [rest_idx - lookback, rest_idx - 1] (inclusive)."""
    lo = max(rest_idx - lookback, 0)
    hi = rest_idx - 1
    if lo > hi:
        return False
    return bool(df.iloc[lo:hi + 1]["is_crash"].any())


def _gs_bucket_on(df, rest_idx):
    return df.iloc[rest_idx]["gs_bucket"]


# ---------------------------------------------------------------------------
# Section 3 -- rest-day gevoelscore-conditioned quadrants per year
# ---------------------------------------------------------------------------
# For each rest-day inside a [D_start - 3, D_end + 3] window around one of
# the 314 heavy episodes, cross-tab crash-before-3d (from that rest-day) x
# gevoelscore bucket, split per year.

def collect_heavy_adjacent_rest_days(df, episodes):
    """Return DataFrame of rest-days adjacent to a heavy episode.

    Adjacency window: [D_start - 3, D_end + 3] around each of the 314
    episodes. Rest-day defined per rest_day_p25 primary operand (True = 1.0).
    De-duplicated: same rest-day-index appears once even if adjacent to
    multiple episodes.
    """
    n = len(df)
    seen = set()
    rows = []
    for _, ep in episodes.iterrows():
        lo = max(int(ep["D_start_idx"]) - LOOKBACK_CRASH, 0)
        hi = min(int(ep["D_end_idx"]) + LOOKBACK_CRASH, n - 1)
        for idx in range(lo, hi + 1):
            if idx in seen:
                continue
            if df.iloc[idx]["rest_day_p25"] == 1.0:
                seen.add(idx)
                rows.append({
                    "rest_idx": idx,
                    "rest_date": df.iloc[idx]["date"],
                    "year": int(df.iloc[idx]["year"]),
                    "gs_bucket": _gs_bucket_on(df, idx),
                    "gevoelscore": df.iloc[idx]["gevoelscore"],
                    "crash_before_3d": _crash_in_lookback(df, idx),
                })
    return pd.DataFrame(rows)


def rest_day_gevoelscore_quadrants_per_year(rest_day_df):
    """Cross-tab per (year x crash_before x gs_bucket) with count + fraction.

    Also emits an all-years pool row per (crash_before x gs_bucket).
    """
    rows = []
    years = sorted(rest_day_df["year"].unique().tolist())
    buckets = ["strategic", "borderline", "crisis", "nan"]
    for year in years:
        year_sub = rest_day_df[rest_day_df["year"] == year]
        n_year = len(year_sub)
        for crash_before in [False, True]:
            for bucket in buckets:
                n = int(((year_sub["crash_before_3d"] == crash_before)
                        & (year_sub["gs_bucket"] == bucket)).sum())
                rows.append({
                    "year": year,
                    "crash_before_3d": crash_before,
                    "gs_bucket": bucket,
                    "n_rest_days": n,
                    "n_year_rest_days": n_year,
                    "fraction_of_year_rest_days": (
                        n / n_year if n_year > 0 else float("nan")
                    ),
                })
    # All-years pool.
    n_all = len(rest_day_df)
    for crash_before in [False, True]:
        for bucket in buckets:
            n = int(((rest_day_df["crash_before_3d"] == crash_before)
                    & (rest_day_df["gs_bucket"] == bucket)).sum())
            rows.append({
                "year": "ALL",
                "crash_before_3d": crash_before,
                "gs_bucket": bucket,
                "n_rest_days": n,
                "n_year_rest_days": n_all,
                "fraction_of_year_rest_days": (
                    n / n_all if n_all > 0 else float("nan")
                ),
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 4 -- mean gevoelscore on rest-day per year (heavy-adjacent + all)
# ---------------------------------------------------------------------------

def rest_day_mean_gevoelscore_per_year(df, rest_day_df):
    """Mean + median + n_valid of gevoelscore on rest-days.

    Two pools:
      (A) heavy-adjacent rest-days (rest_day_df from Section 3 builder).
      (B) all-corpus rest-days on LC-era (rest_day_p25 == 1.0 anywhere).
    Also emits an all-years pool row per pool.
    """
    rows = []

    def _emit(pool_label, sub, year_label):
        gs = sub["gevoelscore"] if "gevoelscore" in sub.columns else sub
        n_total = len(sub)
        n_valid = int(gs.notna().sum())
        mean = float(gs.mean()) if n_valid > 0 else float("nan")
        median = float(gs.median()) if n_valid > 0 else float("nan")
        rows.append({
            "pool": pool_label,
            "year": year_label,
            "n_rest_days_total": n_total,
            "n_gevoelscore_valid": n_valid,
            "n_gevoelscore_nan": n_total - n_valid,
            "mean_gevoelscore": mean,
            "median_gevoelscore": median,
        })

    # (A) heavy-adjacent pool per year + ALL.
    years = sorted(rest_day_df["year"].unique().tolist())
    for year in years:
        sub = rest_day_df[rest_day_df["year"] == year]
        _emit("heavy_adjacent", sub, year)
    _emit("heavy_adjacent", rest_day_df, "ALL")

    # (B) all-corpus rest-days pool per year + ALL.
    all_rest_df = df[df["rest_day_p25"] == 1.0].copy()
    all_rest_df["year_v"] = all_rest_df["date"].dt.year.astype(int)
    for year in sorted(all_rest_df["year_v"].unique().tolist()):
        sub = all_rest_df[all_rest_df["year_v"] == year]
        _emit("all_corpus_rest_days", sub, year)
    _emit("all_corpus_rest_days", all_rest_df, "ALL")

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 5 -- proactive-strategic-rest-after-K3 -> crash-in-5d 2x2
# ---------------------------------------------------------------------------
# Restrict the rest-after-K3-True subset to episodes where the adjacent
# rest-day is proactive-strategic:
#   (a) NO is_crash in [rest_day - 3, rest_day - 1]  AND
#   (b) gevoelscore >= 5 on rest_day (bucket == "strategic").
# If multiple rest-days in [D_end+1, D_end+3], episode is proactive-strategic
# if ANY of those rest-days is proactive-strategic.

def _episode_proactive_strategic(df, ep):
    if not ep["rest_after_3_primary"]:
        return False
    for rest_idx in ep["rest_indices_after_K3"]:
        crash_before = _crash_in_lookback(df, rest_idx)
        bucket = _gs_bucket_on(df, rest_idx)
        if (not crash_before) and (bucket == "strategic"):
            return True
    return False


def _episode_crisis_reactive(df, ep):
    """Episode is crisis-reactive if any rest-day in [D_end+1, D_end+3] has
    a crash in the 3d lookback OR a crisis-bucket gevoelscore (<= 3)."""
    if not ep["rest_after_3_primary"]:
        return False
    for rest_idx in ep["rest_indices_after_K3"]:
        crash_before = _crash_in_lookback(df, rest_idx)
        bucket = _gs_bucket_on(df, rest_idx)
        if crash_before or (bucket == "crisis"):
            return True
    return False


def proactive_strategic_rest_crash_2x2(df, episodes):
    """K=3 rest-after primary 2x2, restricted to proactive-strategic subset.

    Arm A (proactive_strategic_rest_after): True iff rest_after_3_primary
    True AND at least one of the K=3 rest-days is proactive-strategic.
    Arm B (complement): all other episodes with rest-after indicator not
    NaN, including rest_after_3_primary True but no strategic rest-day, and
    rest_after_3_primary False.

    Outcome: crash_in_5d.
    Report all-era pool + per-year if per-year cells viable at n >= 5.
    """
    rows = []
    # Drop episodes without full +5d crash window OR NaN rest-after indicator.
    sub = episodes[
        (episodes["crash_window_full"] == True)
        & (episodes["rest_after_3_primary"].notna())
    ].copy()
    sub["rest_after_3_primary"] = sub["rest_after_3_primary"].astype(bool)

    # Flag proactive-strategic subset.
    sub["proactive_strategic"] = sub.apply(
        lambda ep: _episode_proactive_strategic(df, ep), axis=1,
    )

    def _emit(pool_label, ep_sub, n_min=1):
        arm_true = ep_sub[ep_sub["proactive_strategic"] == True]
        arm_false = ep_sub[ep_sub["proactive_strategic"] == False]
        n_t = len(arm_true)
        n_f = len(arm_false)
        k_t = int(arm_true["crash_in_5d"].sum())
        k_f = int(arm_false["crash_in_5d"].sum())
        p_t, lo_t, hi_t = wilson_ci(k_t, n_t)
        p_f, lo_f, hi_f = wilson_ci(k_f, n_f)
        if p_f and not math.isnan(p_f) and p_f > 0:
            rr = p_t / p_f
        else:
            rr = float("nan")
        rd = (p_t - p_f) if not (math.isnan(p_t) or math.isnan(p_f)) else float("nan")
        rows.append({
            "pool": pool_label,
            "n_episodes_used": len(ep_sub),
            "proactive_strategic_true_n": n_t,
            "proactive_strategic_false_n": n_f,
            "proactive_strategic_true_crash": k_t,
            "proactive_strategic_false_crash": k_f,
            "rate_proactive_strategic": p_t,
            "rate_proactive_strategic_wilson_lo": lo_t,
            "rate_proactive_strategic_wilson_hi": hi_t,
            "rate_complement": p_f,
            "rate_complement_wilson_lo": lo_f,
            "rate_complement_wilson_hi": hi_f,
            "risk_ratio_strategic_over_complement": rr,
            "risk_difference_strategic_minus_complement": rd,
            "viable_n_min5": (n_t >= 5) and (n_f >= 5),
        })

    _emit("ALL_ERA_POOLED", sub)
    for year in sorted(sub["year_end"].unique()):
        year_sub = sub[sub["year_end"] == year]
        _emit(f"year_{int(year)}", year_sub)

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 6 -- crisis-reactive-rest-after-K3 -> crash-in-5d 2x2 (companion)
# ---------------------------------------------------------------------------

def crisis_reactive_rest_crash_2x2(df, episodes):
    """K=3 rest-after primary 2x2, restricted to crisis-reactive subset.

    Arm A (crisis_reactive_rest_after): True iff rest_after_3_primary
    True AND at least one of the K=3 rest-days is crisis-reactive.
    Arm B (complement): all other episodes with rest-after indicator not NaN.
    Outcome: crash_in_5d.
    Prediction: STRONG sign-inversion (endogeneity signature isolated).
    """
    rows = []
    sub = episodes[
        (episodes["crash_window_full"] == True)
        & (episodes["rest_after_3_primary"].notna())
    ].copy()
    sub["rest_after_3_primary"] = sub["rest_after_3_primary"].astype(bool)

    sub["crisis_reactive"] = sub.apply(
        lambda ep: _episode_crisis_reactive(df, ep), axis=1,
    )

    def _emit(pool_label, ep_sub):
        arm_true = ep_sub[ep_sub["crisis_reactive"] == True]
        arm_false = ep_sub[ep_sub["crisis_reactive"] == False]
        n_t = len(arm_true)
        n_f = len(arm_false)
        k_t = int(arm_true["crash_in_5d"].sum())
        k_f = int(arm_false["crash_in_5d"].sum())
        p_t, lo_t, hi_t = wilson_ci(k_t, n_t)
        p_f, lo_f, hi_f = wilson_ci(k_f, n_f)
        if p_f and not math.isnan(p_f) and p_f > 0:
            rr = p_t / p_f
        else:
            rr = float("nan")
        rd = (p_t - p_f) if not (math.isnan(p_t) or math.isnan(p_f)) else float("nan")
        rows.append({
            "pool": pool_label,
            "n_episodes_used": len(ep_sub),
            "crisis_reactive_true_n": n_t,
            "crisis_reactive_false_n": n_f,
            "crisis_reactive_true_crash": k_t,
            "crisis_reactive_false_crash": k_f,
            "rate_crisis_reactive": p_t,
            "rate_crisis_reactive_wilson_lo": lo_t,
            "rate_crisis_reactive_wilson_hi": hi_t,
            "rate_complement": p_f,
            "rate_complement_wilson_lo": lo_f,
            "rate_complement_wilson_hi": hi_f,
            "risk_ratio_crisis_over_complement": rr,
            "risk_difference_crisis_minus_complement": rd,
            "viable_n_min5": (n_t >= 5) and (n_f >= 5),
        })

    _emit("ALL_ERA_POOLED", sub)
    for year in sorted(sub["year_end"].unique()):
        year_sub = sub[sub["year_end"] == year]
        _emit(f"year_{int(year)}", year_sub)

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 7 -- very-heavy day frequency per year (Interpretation D test 1)
# ---------------------------------------------------------------------------

def very_heavy_frequency_per_year(df):
    rows = []
    years = sorted(df["year"].unique().tolist())
    for year in years:
        sub = df[df["year"] == year]
        n_total = len(sub)
        n_vh = int(sub["is_very_heavy"].sum())
        n_heavy_only = int(sub["is_heavy_only"].sum())
        n_heavy_all = int(sub["is_heavy"].sum())
        # Activity-days: non-NaN exertion class.
        n_activity = int(sub["exertion_class_lagged_lcera"].notna().sum())
        rows.append({
            "year": year,
            "n_days_total": n_total,
            "n_activity_days_classified": n_activity,
            "n_heavy_only_days": n_heavy_only,
            "n_very_heavy_days": n_vh,
            "n_heavy_all_days": n_heavy_all,
            "vh_fraction_of_activity_days": (
                n_vh / n_activity if n_activity > 0 else float("nan")
            ),
            "vh_fraction_of_heavy_all_days": (
                n_vh / n_heavy_all if n_heavy_all > 0 else float("nan")
            ),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 8 -- step-envelope variance per year (Interpretation D test 2)
# ---------------------------------------------------------------------------

def step_envelope_variance_per_year(df):
    rows = []
    years = sorted(df["year"].unique().tolist())
    for year in years:
        sub = df[df["year"] == year]
        steps = sub["total_steps"].astype(float).dropna()
        n = len(steps)
        if n == 0:
            rows.append({
                "year": year,
                "n_days_with_steps": 0,
                "mean_total_steps": float("nan"),
                "median_total_steps": float("nan"),
                "std_total_steps": float("nan"),
                "coefficient_of_variation": float("nan"),
                "iqr_total_steps": float("nan"),
                "p25_total_steps": float("nan"),
                "p75_total_steps": float("nan"),
            })
            continue
        mean = float(steps.mean())
        median = float(steps.median())
        std = float(steps.std(ddof=1)) if n > 1 else float("nan")
        cv = (std / mean) if (mean and not math.isnan(std)) else float("nan")
        p25 = float(steps.quantile(0.25))
        p75 = float(steps.quantile(0.75))
        iqr = p75 - p25
        rows.append({
            "year": year,
            "n_days_with_steps": n,
            "mean_total_steps": mean,
            "median_total_steps": median,
            "std_total_steps": std,
            "coefficient_of_variation": cv,
            "iqr_total_steps": iqr,
            "p25_total_steps": p25,
            "p75_total_steps": p75,
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 9 -- heavy-episode-end to next rest-day gap per year (D test 3)
# ---------------------------------------------------------------------------

def heavy_gap_to_next_rest_per_year(df, episodes):
    """Per-year median + mean gap in days from D_end to next rest-day.

    Next rest-day = smallest idx > D_end_idx with rest_day_p25 == 1.0.
    Right-censored if no rest-day found before corpus end (episode dropped
    from stats but counted separately).
    """
    n = len(df)
    rows_per_ep = []
    for _, ep in episodes.iterrows():
        end_idx = int(ep["D_end_idx"])
        # Search forward for next rest-day.
        next_gap = None
        for idx in range(end_idx + 1, n):
            val = df.iloc[idx]["rest_day_p25"]
            if val == 1.0:
                next_gap = idx - end_idx
                break
        rows_per_ep.append({
            "episode_id": ep["episode_id"],
            "year_end": ep["year_end"],
            "gap_days": next_gap,     # None if right-censored
            "censored": next_gap is None,
        })
    gap_df = pd.DataFrame(rows_per_ep)

    rows = []
    for year in sorted(gap_df["year_end"].unique().tolist()):
        year_sub = gap_df[gap_df["year_end"] == year]
        observed = year_sub[year_sub["censored"] == False]["gap_days"]
        n_obs = len(observed)
        n_cens = int((year_sub["censored"] == True).sum())
        rows.append({
            "year": year,
            "n_episodes_year": len(year_sub),
            "n_gap_observed": n_obs,
            "n_censored": n_cens,
            "mean_gap_days": float(observed.mean()) if n_obs > 0 else float("nan"),
            "median_gap_days": float(observed.median()) if n_obs > 0 else float("nan"),
            "p25_gap_days": float(observed.quantile(0.25)) if n_obs > 0 else float("nan"),
            "p75_gap_days": float(observed.quantile(0.75)) if n_obs > 0 else float("nan"),
        })
    # ALL pool row.
    observed = gap_df[gap_df["censored"] == False]["gap_days"]
    n_obs = len(observed)
    rows.append({
        "year": "ALL",
        "n_episodes_year": len(gap_df),
        "n_gap_observed": n_obs,
        "n_censored": int((gap_df["censored"] == True).sum()),
        "mean_gap_days": float(observed.mean()) if n_obs > 0 else float("nan"),
        "median_gap_days": float(observed.median()) if n_obs > 0 else float("nan"),
        "p25_gap_days": float(observed.quantile(0.25)) if n_obs > 0 else float("nan"),
        "p75_gap_days": float(observed.quantile(0.75)) if n_obs > 0 else float("nan"),
    })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# main -- drive all outputs
# ---------------------------------------------------------------------------

def main():
    df = load_lc_stratum()
    print(f"[stratum] LC-era rows: {len(df)}")
    print(f"[stratum] heavy: {int(df['is_heavy'].sum())} "
          f"(vh={int(df['is_very_heavy'].sum())}); "
          f"crash: {int(df['is_crash'].sum())}; "
          f"gs valid: {int(df['gevoelscore'].notna().sum())} / {len(df)}")
    print(f"[stratum] rest_day_p25 True: {int((df['rest_day_p25'] == 1.0).sum())} "
          f"NaN: {int(df['rest_day_p25'].isna().sum())}")

    episodes = build_episodes(df)
    print(f"[episodes] gap=0 heavy episodes: {len(episodes)}")

    # Section 3: rest-day quadrants per year.
    rest_day_df = collect_heavy_adjacent_rest_days(df, episodes)
    print(f"[section 3] heavy-adjacent rest-days (dedup): {len(rest_day_df)}")
    quadrants = rest_day_gevoelscore_quadrants_per_year(rest_day_df)
    quadrants.to_csv(
        OUTPUT_DIR / "rest_day_gevoelscore_quadrants_per_year.csv", index=False,
    )

    # Section 4: mean gevoelscore on rest-day per year.
    mean_gs = rest_day_mean_gevoelscore_per_year(df, rest_day_df)
    mean_gs.to_csv(
        OUTPUT_DIR / "rest_day_mean_gevoelscore_per_year.csv", index=False,
    )

    # Section 5: proactive-strategic-rest -> crash-in-5d 2x2.
    ps = proactive_strategic_rest_crash_2x2(df, episodes)
    ps.to_csv(
        OUTPUT_DIR / "proactive_strategic_rest_crash_2x2.csv", index=False,
    )

    # Section 6: crisis-reactive-rest -> crash-in-5d 2x2.
    cr = crisis_reactive_rest_crash_2x2(df, episodes)
    cr.to_csv(
        OUTPUT_DIR / "crisis_reactive_rest_crash_2x2.csv", index=False,
    )

    # Section 7: very-heavy frequency per year.
    vhf = very_heavy_frequency_per_year(df)
    vhf.to_csv(
        OUTPUT_DIR / "very_heavy_frequency_per_year.csv", index=False,
    )

    # Section 8: step-envelope variance per year.
    sev = step_envelope_variance_per_year(df)
    sev.to_csv(
        OUTPUT_DIR / "step_envelope_variance_per_year.csv", index=False,
    )

    # Section 9: heavy-end -> next rest gap per year.
    gap = heavy_gap_to_next_rest_per_year(df, episodes)
    gap.to_csv(
        OUTPUT_DIR / "heavy_gap_to_next_rest_per_year.csv", index=False,
    )

    print(f"\n[write] outputs in {OUTPUT_DIR}")
    for f in sorted(OUTPUT_DIR.glob("*.csv")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
