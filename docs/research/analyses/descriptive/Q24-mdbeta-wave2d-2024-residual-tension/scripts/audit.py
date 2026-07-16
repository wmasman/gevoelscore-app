"""Q24 MD-beta Wave 2D descriptive audit -- 2024 residual tension.

Wave 2D sibling of parent Q24 MD-beta Wave 2C audit
(../Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md LOCKED r1
2026-07-16).

Investigates the 2024 exception surfaced by Wave 2C section 5.1: the
per-year proactive-strategic (PS) rest-after crash-in-5d risk-ratio flips
cleanly to < 1 in 2023 (RR = 0.22), 2025 (RR = 0.00), and 2026 partial
(RR = 0.00), but stays ~ 1 in 2024 (RR = 0.93, 3 crashes on 15 PS
episodes). Wave 2C flagged this as a sign-flip PAUSE and reviewer
recommended a formal Wave 2D investigation before Stage H pre-registration
on the rest-adjacency arc.

Wave 2C candidate readings for the 2024 exception (audit.md section 5.3 +
reviewer L10.5 extension):

  (a) Small-n artefact -- 2024 PS-True arm is n=15 with 3 crashes; Wilson
      CI [7.0, 45.2] does not credibly rule out RR ~ 1 or RR ~ 2. Test:
      threshold sensitivity on the gevoelscore boundary should stay wide
      if it is just noise.
  (b) Partial-mitigation only -- gevoelscore >= 5 does not fully isolate
      calibrated pacing in 2024. Residual endogeneity may operate through
      a mechanism not captured by gevoelscore-on-rest-day (e.g. cumulative
      load in the pre-window, forward-window compensatory failure). Test:
      per-episode diagnostic on the 3 crash-in-5d events should share
      features.
  (c) Transition-year mid-shift -- 2024 sits between crisis-dominant
      (2023) and strategic-dominant (2025+) composition; the shift may
      have happened mid-2024 rather than at year boundaries. Test:
      per-quarter or per-half-year proactive-strategic RR within 2024
      should show the shift happening within the year.
  (d) Real endogeneity residual specific to 2024 -- some 2024-specific
      factor (medication titration mid-year, seasonal effect, life-event
      stress cluster) drives the 3 crash-in-5d events beyond what
      gevoelscore captures. Test: per-episode diagnostic should surface
      common features (dates, seasonal cluster, other exposures).
  (e) Intensity-interaction residual -- Wave 2B section 10 found
      heavy-terminal episodes drove the whole-corpus sign-inversion
      (heavy RR = 2.07 vs very_heavy RR = 0.96). If 2024 PS-True arm is
      disproportionately heavy-terminal, that could explain the residual.
      Test: cross-tab 2024 PS episodes by end_class.

Outputs are written to ../output/ and consumed by the sibling audit.md
descriptive card. This script is idempotent and re-runnable.

Frame: LC-era stratum (lc_phase == 'lc'), matches parent Wave 2B stratum.
Heavy-day definition: exertion_class_lagged_lcera in {heavy, very_heavy}.
Rest-day primary: total_steps < rolling_percentile_25(total_steps, 30d,
  min_periods=15).
Rest-day absolute-step companion: total_steps < 3000 (per Wave 2C section
  5.5 recommendation).
Episode: gap=0 contiguous heavy-day run.
crash_in_5d(D_end) = any(is_crash[d] for d in [D_end+1, D_end+5]).

Stage -1 descriptive audit only. NO inferential tests; no verdicts.
Wilson 95% CI on rates; RR reported with per-arm cell counts.
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
CRASH_WINDOW = 5
K_REST_AFTER = 3       # MD-beta section 3.2 primary K value
LOOKBACK_CRASH = 3     # rest-day quadrant: is_crash in [rest_day - 3, rest_day - 1]
ABS_STEP_THRESHOLD = 3000   # Wave 2C section 5.5 companion operand
STRICT_GS = 6
PRIMARY_GS = 5
LOOSE_GS = 4
RANDOM_SEED = 20260716   # declared per MD-beta section 3.6; unused.
YEAR_TARGET = 2024
NEIGHBOUR_YEARS = (2023, 2025)
PRE_WINDOW_DAYS = 30


# ---------------------------------------------------------------------------
# Data loading + rest-day + gevoelscore-bucket construction
# ---------------------------------------------------------------------------

def load_lc_stratum():
    """Load per_day_master.csv, filter to LC-era, add heavy/rest/bucket cols.

    Adds rolling-p25 rest-day operand + absolute-step rest-day operand.
    """
    df = pd.read_csv(INPUT, parse_dates=["date"])
    df = df[df["lc_phase"] == "lc"].copy().reset_index(drop=True)
    df["is_heavy"] = df["exertion_class_lagged_lcera"].isin(HEAVY_CLASSES)
    df["is_very_heavy"] = df["exertion_class_lagged_lcera"] == "very_heavy"
    df["is_heavy_only"] = df["exertion_class_lagged_lcera"] == "heavy"
    df["is_crash"] = df["is_crash"].fillna(False).astype(bool)
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["year_quarter"] = df["year"].astype(str) + "Q" + df["quarter"].astype(str)

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
    # Absolute-step rest-day (Wave 2C section 5.5 companion).
    df["rest_day_abs3k"] = np.where(
        steps.isna(),
        np.nan,
        (steps < ABS_STEP_THRESHOLD).astype(float),
    )
    return df


# ---------------------------------------------------------------------------
# Episode construction (gap=0 contiguous heavy runs)
# ---------------------------------------------------------------------------

def build_episodes(df, rest_col="rest_day_p25"):
    """Emit episode table (one row per gap=0 heavy episode).

    Parameterised on rest_col so we can build parallel episode tables under
    the rolling-p25 vs absolute-step rest-day operand.
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

        # K=3 rest-after: list of rest-day indices in [end+1, end+3].
        r_lo = end + 1
        r_hi = min(end + K_REST_AFTER, n - 1)
        rest_indices = []
        rest_after_undefined = False
        if r_lo > n - 1:
            rest_after_undefined = True
        else:
            window = df.iloc[r_lo:r_hi + 1]
            for idx in window.index:
                val = df.loc[idx, rest_col]
                if val == 1.0:
                    rest_indices.append(int(idx))
            if len(rest_indices) == 0:
                truncated = (end + K_REST_AFTER) > n - 1
                any_nan = window[rest_col].isna().any()
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
            "quarter_end": int(end_row["quarter"]),
            "year_quarter_end": str(end_row["year_quarter"]),
            "end_class": end_class,
            "crash_in_5d": crash_in_5d,
            "crash_window_full": has_window_data,
            "rest_after_3_primary": rest_after_indicator,
            "rest_indices_after_K3": rest_indices,
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
# Rest-day helpers
# ---------------------------------------------------------------------------

def _crash_in_lookback(df, rest_idx, lookback=LOOKBACK_CRASH):
    lo = max(rest_idx - lookback, 0)
    hi = rest_idx - 1
    if lo > hi:
        return False
    return bool(df.iloc[lo:hi + 1]["is_crash"].any())


def _bucket_from_gs(gs_value, strategic_threshold=PRIMARY_GS):
    """Bucket a gevoelscore into strategic / borderline / crisis / nan.

    Parameterised by strategic_threshold so we can run threshold sensitivity.
    Crisis is fixed at <= 3; borderline is anything below strategic_threshold
    and above 3; NaN is preserved as its own bucket.
    """
    if pd.isna(gs_value):
        return "nan"
    if gs_value >= strategic_threshold:
        return "strategic"
    if gs_value <= 3:
        return "crisis"
    return "borderline"


def _episode_proactive_strategic(df, ep, strategic_threshold=PRIMARY_GS):
    """Episode is proactive-strategic if any of its K=3 rest-days has NO
    crash in the 3d lookback AND gevoelscore >= strategic_threshold on the
    rest-day."""
    if not ep["rest_after_3_primary"]:
        return False
    for rest_idx in ep["rest_indices_after_K3"]:
        crash_before = _crash_in_lookback(df, rest_idx)
        gs_val = df.iloc[rest_idx]["gevoelscore"]
        bucket = _bucket_from_gs(gs_val, strategic_threshold)
        if (not crash_before) and (bucket == "strategic"):
            return True
    return False


def _select_ps_rest_index(df, ep, strategic_threshold=PRIMARY_GS):
    """Return the FIRST proactive-strategic rest-day index for the episode,
    or None if no rest-day meets the criteria. Used by per-episode diagnostic
    to attribute one rest-day per PS episode.
    """
    if not ep["rest_after_3_primary"]:
        return None
    for rest_idx in ep["rest_indices_after_K3"]:
        crash_before = _crash_in_lookback(df, rest_idx)
        gs_val = df.iloc[rest_idx]["gevoelscore"]
        bucket = _bucket_from_gs(gs_val, strategic_threshold)
        if (not crash_before) and (bucket == "strategic"):
            return rest_idx
    return None


# ---------------------------------------------------------------------------
# Generic 2x2 emitter for proactive-strategic-rest vs complement
# ---------------------------------------------------------------------------

def _ps_2x2_row(pool_label, ep_sub):
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
    return {
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
    }


def prepare_ps_episodes(df, episodes, strategic_threshold=PRIMARY_GS):
    """Filter to episodes with full crash-window + non-NaN rest-after; flag
    proactive_strategic per strategic_threshold."""
    sub = episodes[
        (episodes["crash_window_full"] == True)
        & (episodes["rest_after_3_primary"].notna())
    ].copy()
    sub["rest_after_3_primary"] = sub["rest_after_3_primary"].astype(bool)
    sub["proactive_strategic"] = sub.apply(
        lambda ep: _episode_proactive_strategic(df, ep, strategic_threshold),
        axis=1,
    )
    return sub


# ---------------------------------------------------------------------------
# Section 3 -- 2024 per-quarter proactive-strategic 2x2
# ---------------------------------------------------------------------------

def ps_2x2_per_quarter_within_year(df, episodes, target_year):
    """Per-quarter proactive-strategic-rest 2x2 within a target year.

    Also emits the target-year all-quarters row for direct cross-check with
    Wave 2C section 5.1.
    """
    sub = prepare_ps_episodes(df, episodes)
    year_sub = sub[sub["year_end"] == target_year].copy()

    rows = []
    rows.append({**_ps_2x2_row(f"year_{target_year}_ALL", year_sub),
                 "quarter": "ALL", "year": target_year})
    for q in sorted(year_sub["quarter_end"].unique()):
        q_sub = year_sub[year_sub["quarter_end"] == q]
        row = _ps_2x2_row(f"year_{target_year}_Q{int(q)}", q_sub)
        row["quarter"] = f"Q{int(q)}"
        row["year"] = target_year
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 4 -- 2024 by-intensity proactive-strategic 2x2
# ---------------------------------------------------------------------------

def ps_2x2_by_intensity_within_year(df, episodes, target_year):
    """Per-end-class (heavy vs very_heavy) proactive-strategic 2x2 within
    target year. Compare to Wave 2B section 10 whole-corpus intensity
    stratification."""
    sub = prepare_ps_episodes(df, episodes)
    year_sub = sub[sub["year_end"] == target_year].copy()

    rows = []
    rows.append({**_ps_2x2_row(f"year_{target_year}_ALL_intensity", year_sub),
                 "end_class": "ALL", "year": target_year})
    for cls in ["heavy", "very_heavy"]:
        cls_sub = year_sub[year_sub["end_class"] == cls]
        row = _ps_2x2_row(f"year_{target_year}_{cls}", cls_sub)
        row["end_class"] = cls
        row["year"] = target_year
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 5 -- per-episode diagnostic on 2024 PS-True episodes
# ---------------------------------------------------------------------------

def _pre_window_load_metrics(df, D_start_idx, days=PRE_WINDOW_DAYS):
    """Compute pre-window cumulative load metrics in [D_start - days, D_start - 1]."""
    lo = max(int(D_start_idx) - days, 0)
    hi = int(D_start_idx) - 1
    if lo > hi:
        return {
            "pre_window_days_available": 0,
            "pre_effective_exertion_min_sum": float("nan"),
            "pre_total_steps_sum": float("nan"),
            "pre_vigorous_min_sum": float("nan"),
            "pre_effective_exertion_min_mean": float("nan"),
            "pre_total_steps_mean": float("nan"),
            "pre_vigorous_min_mean": float("nan"),
        }
    win = df.iloc[lo:hi + 1]
    return {
        "pre_window_days_available": len(win),
        "pre_effective_exertion_min_sum": float(win["effective_exertion_min"].fillna(0).sum()),
        "pre_total_steps_sum": float(win["total_steps"].fillna(0).sum()),
        "pre_vigorous_min_sum": float(win["vigorous_min"].fillna(0).sum()),
        "pre_effective_exertion_min_mean": float(win["effective_exertion_min"].mean()),
        "pre_total_steps_mean": float(win["total_steps"].mean()),
        "pre_vigorous_min_mean": float(win["vigorous_min"].mean()),
    }


def _cumulative_prior(df, D_end_idx, days):
    """Sum of effective_exertion_min over [D_end - days + 1, D_end] (inclusive
    of episode-end day). Returns nan-tolerant sum."""
    lo = max(int(D_end_idx) - days + 1, 0)
    hi = int(D_end_idx)
    if lo > hi:
        return float("nan")
    return float(df.iloc[lo:hi + 1]["effective_exertion_min"].fillna(0).sum())


def _subsequent_7d_exertion(df, D_end_idx):
    n = len(df)
    lo = int(D_end_idx) + 1
    hi = min(int(D_end_idx) + 7, n - 1)
    if lo > hi:
        return float("nan")
    return float(df.iloc[lo:hi + 1]["effective_exertion_min"].fillna(0).sum())


def _days_since_previous_crash(df, D_end_idx):
    """Days from most recent is_crash True at idx <= D_end_idx back to
    D_end_idx. Returns NaN if no prior crash exists on LC-era."""
    idx = int(D_end_idx)
    hits = df.iloc[: idx + 1]
    crash_hits = hits[hits["is_crash"] == True]
    if len(crash_hits) == 0:
        return float("nan")
    last_crash_idx = int(crash_hits.index[-1])
    return float(idx - last_crash_idx)


def _prior_30d_crash_count(df, D_end_idx):
    lo = max(int(D_end_idx) - 30, 0)
    hi = int(D_end_idx)
    if lo > hi:
        return 0
    return int(df.iloc[lo:hi + 1]["is_crash"].sum())


def _first_crash_offset_in_5d(df, D_end_idx):
    """Days-from-episode-end-to-first-crash within [D_end+1, D_end+5].
    Returns int or NaN if no crash."""
    n = len(df)
    lo = int(D_end_idx) + 1
    hi = min(int(D_end_idx) + CRASH_WINDOW, n - 1)
    if lo > hi:
        return float("nan")
    for i in range(lo, hi + 1):
        if bool(df.iloc[i]["is_crash"]):
            return float(i - int(D_end_idx))
    return float("nan")


def per_episode_diagnostic_2024(df, episodes, target_year):
    """Emit per-episode diagnostic for 2024 PS-True episodes.

    Returns two DataFrames:
      crash_events -- one row per crash-in-5d PS-True 2024 episode
      noncrash_baseline -- one row per non-crash PS-True 2024 episode
    """
    sub = prepare_ps_episodes(df, episodes)
    year_ps = sub[
        (sub["year_end"] == target_year) & (sub["proactive_strategic"] == True)
    ].copy()

    crash_rows = []
    noncrash_rows = []
    for _, ep in year_ps.iterrows():
        ps_rest_idx = _select_ps_rest_index(df, ep)
        # ps_rest_idx should never be None here because the ep is PS-True by
        # construction; but guard anyway.
        if ps_rest_idx is None:
            continue
        rest_row = df.iloc[ps_rest_idx]
        row = {
            "episode_id": int(ep["episode_id"]),
            "episode_start_date": pd.Timestamp(ep["D_start"]).strftime("%Y-%m-%d"),
            "episode_end_date": pd.Timestamp(ep["D_end"]).strftime("%Y-%m-%d"),
            "streak_length": int(ep["streak_length"]),
            "end_class": ep["end_class"],
            "quarter_end": int(ep["quarter_end"]),
            "rest_day_date": pd.Timestamp(rest_row["date"]).strftime("%Y-%m-%d"),
            "gevoelscore_on_rest_day": (
                float(rest_row["gevoelscore"])
                if pd.notna(rest_row["gevoelscore"]) else float("nan")
            ),
            "days_from_episode_end_to_first_crash": _first_crash_offset_in_5d(
                df, ep["D_end_idx"],
            ),
            "cumulative_effective_exertion_min_prior_7d": _cumulative_prior(
                df, ep["D_end_idx"], 7,
            ),
            "cumulative_effective_exertion_min_prior_14d": _cumulative_prior(
                df, ep["D_end_idx"], 14,
            ),
            "cumulative_effective_exertion_min_prior_30d": _cumulative_prior(
                df, ep["D_end_idx"], 30,
            ),
            "days_since_previous_crash": _days_since_previous_crash(
                df, ep["D_end_idx"],
            ),
            "prior_30d_crash_count": _prior_30d_crash_count(
                df, ep["D_end_idx"],
            ),
            "subsequent_7d_effective_exertion_min": _subsequent_7d_exertion(
                df, ep["D_end_idx"],
            ),
        }
        if bool(ep["crash_in_5d"]):
            crash_rows.append(row)
        else:
            noncrash_rows.append(row)

    return pd.DataFrame(crash_rows), pd.DataFrame(noncrash_rows)


# ---------------------------------------------------------------------------
# Section 6 -- gevoelscore threshold sensitivity within 2024
# ---------------------------------------------------------------------------

def threshold_sensitivity_within_year(df, episodes, target_year):
    """Recompute proactive-strategic 2x2 within target year under 3 gevoelscore
    thresholds: primary >= 5, strict >= 6, loose >= 4."""
    rows = []
    for label, thr in [
        ("primary_gs_ge_5", PRIMARY_GS),
        ("strict_gs_ge_6", STRICT_GS),
        ("loose_gs_ge_4", LOOSE_GS),
    ]:
        sub = prepare_ps_episodes(df, episodes, strategic_threshold=thr)
        year_sub = sub[sub["year_end"] == target_year]
        row = _ps_2x2_row(f"year_{target_year}_{label}", year_sub)
        row["strategic_threshold"] = label
        row["threshold_value"] = thr
        row["year"] = target_year
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 7 -- absolute-step-threshold companion 2x2
# ---------------------------------------------------------------------------

def abs_step_companion_2x2(df, target_year):
    """Rebuild episodes under absolute-step rest-day operand (total_steps < 3000)
    and recompute proactive-strategic 2x2 for target year, pooled, and 2023."""
    ep_abs = build_episodes(df, rest_col="rest_day_abs3k")
    sub = prepare_ps_episodes(df, ep_abs)

    rows = []
    # Pooled all years
    rows.append({**_ps_2x2_row("ALL_ERA_POOLED_abs3k", sub),
                 "year": "ALL", "operand": "abs_steps_lt_3000"})
    # Target year
    year_sub = sub[sub["year_end"] == target_year]
    rows.append({**_ps_2x2_row(f"year_{target_year}_abs3k", year_sub),
                 "year": target_year, "operand": "abs_steps_lt_3000"})
    # 2023 for reference
    ref_sub = sub[sub["year_end"] == 2023]
    rows.append({**_ps_2x2_row("year_2023_abs3k", ref_sub),
                 "year": 2023, "operand": "abs_steps_lt_3000"})

    # For comparison, also emit the rolling-p25 versions for the same pools
    # (recomputed here so the CSV is self-contained side-by-side).
    ep_p25 = build_episodes(df, rest_col="rest_day_p25")
    sub_p25 = prepare_ps_episodes(df, ep_p25)
    rows.append({**_ps_2x2_row("ALL_ERA_POOLED_p25", sub_p25),
                 "year": "ALL", "operand": "rolling_p25"})
    rows.append({**_ps_2x2_row(f"year_{target_year}_p25",
                                sub_p25[sub_p25["year_end"] == target_year]),
                 "year": target_year, "operand": "rolling_p25"})
    rows.append({**_ps_2x2_row("year_2023_p25",
                                sub_p25[sub_p25["year_end"] == 2023]),
                 "year": 2023, "operand": "rolling_p25"})

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 8 -- per-quarter proactive-strategic RR in 2023 + 2025
# ---------------------------------------------------------------------------

def ps_2x2_per_quarter_multiple_years(df, episodes, years):
    """Per-quarter PS 2x2 for multiple years. Concatenated for context
    comparison to 2024."""
    sub = prepare_ps_episodes(df, episodes)
    rows = []
    for y in years:
        year_sub = sub[sub["year_end"] == y].copy()
        rows.append({**_ps_2x2_row(f"year_{y}_ALL", year_sub),
                     "quarter": "ALL", "year": y})
        for q in sorted(year_sub["quarter_end"].unique()):
            q_sub = year_sub[year_sub["quarter_end"] == q]
            row = _ps_2x2_row(f"year_{y}_Q{int(q)}", q_sub)
            row["quarter"] = f"Q{int(q)}"
            row["year"] = y
            rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 9 -- pre-window load comparison, crash vs non-crash 2024 PS
# ---------------------------------------------------------------------------

def pre_window_load_comparison_2024(df, episodes, target_year):
    """Compare pre-window (30d) cumulative load between 2024 PS-True crash
    and non-crash episodes."""
    sub = prepare_ps_episodes(df, episodes)
    year_ps = sub[
        (sub["year_end"] == target_year) & (sub["proactive_strategic"] == True)
    ].copy()

    per_ep_rows = []
    for _, ep in year_ps.iterrows():
        m = _pre_window_load_metrics(df, ep["D_start_idx"], days=PRE_WINDOW_DAYS)
        per_ep_rows.append({
            "episode_id": int(ep["episode_id"]),
            "crash_in_5d": bool(ep["crash_in_5d"]),
            **m,
        })
    per_ep_df = pd.DataFrame(per_ep_rows)

    rows = []
    for label, mask in [
        ("crash_in_5d_TRUE", per_ep_df["crash_in_5d"] == True),
        ("crash_in_5d_FALSE", per_ep_df["crash_in_5d"] == False),
        ("ALL", per_ep_df.index == per_ep_df.index),
    ]:
        s = per_ep_df[mask]
        if len(s) == 0:
            rows.append({"group": label, "n_episodes": 0})
            continue
        row = {"group": label, "n_episodes": len(s)}
        for col in [
            "pre_effective_exertion_min_sum",
            "pre_total_steps_sum",
            "pre_vigorous_min_sum",
            "pre_effective_exertion_min_mean",
            "pre_total_steps_mean",
            "pre_vigorous_min_mean",
        ]:
            vals = s[col].dropna()
            if len(vals) == 0:
                row[f"{col}_mean"] = float("nan")
                row[f"{col}_median"] = float("nan")
                row[f"{col}_std"] = float("nan")
                continue
            row[f"{col}_mean"] = float(vals.mean())
            row[f"{col}_median"] = float(vals.median())
            row[f"{col}_std"] = (
                float(vals.std(ddof=1)) if len(vals) > 1 else float("nan")
            )
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 10 -- neighbouring-year PS-arm composition
# ---------------------------------------------------------------------------

def neighbouring_year_composition(df, episodes, years):
    """Per-year PS-arm composition: mean gevoelscore-on-rest-day, mean
    pre-window activity, mean streak length. For 2023 / 2024 / 2025."""
    sub = prepare_ps_episodes(df, episodes)
    ps_only = sub[sub["proactive_strategic"] == True].copy()

    rows = []
    for y in years:
        year_ps = ps_only[ps_only["year_end"] == y]
        if len(year_ps) == 0:
            rows.append({"year": y, "n_ps_episodes": 0})
            continue
        gs_on_rest = []
        pre_ex = []
        pre_steps = []
        for _, ep in year_ps.iterrows():
            r_idx = _select_ps_rest_index(df, ep)
            if r_idx is not None:
                g = df.iloc[r_idx]["gevoelscore"]
                if pd.notna(g):
                    gs_on_rest.append(float(g))
            m = _pre_window_load_metrics(df, ep["D_start_idx"], days=PRE_WINDOW_DAYS)
            if not math.isnan(m["pre_effective_exertion_min_mean"]):
                pre_ex.append(m["pre_effective_exertion_min_mean"])
            if not math.isnan(m["pre_total_steps_mean"]):
                pre_steps.append(m["pre_total_steps_mean"])
        streaks = year_ps["streak_length"].astype(float).tolist()
        end_heavy = int((year_ps["end_class"] == "heavy").sum())
        end_vh = int((year_ps["end_class"] == "very_heavy").sum())
        rows.append({
            "year": y,
            "n_ps_episodes": len(year_ps),
            "mean_gs_on_ps_rest_day": (
                float(np.mean(gs_on_rest)) if gs_on_rest else float("nan")
            ),
            "median_gs_on_ps_rest_day": (
                float(np.median(gs_on_rest)) if gs_on_rest else float("nan")
            ),
            "n_gs_on_rest_valid": len(gs_on_rest),
            "mean_pre_window_effective_exertion_min_day_mean": (
                float(np.mean(pre_ex)) if pre_ex else float("nan")
            ),
            "mean_pre_window_total_steps_day_mean": (
                float(np.mean(pre_steps)) if pre_steps else float("nan")
            ),
            "mean_streak_length": (
                float(np.mean(streaks)) if streaks else float("nan")
            ),
            "median_streak_length": (
                float(np.median(streaks)) if streaks else float("nan")
            ),
            "n_end_class_heavy": end_heavy,
            "n_end_class_very_heavy": end_vh,
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
    print(f"[stratum] rest_day_abs3k True: {int((df['rest_day_abs3k'] == 1.0).sum())} "
          f"NaN: {int(df['rest_day_abs3k'].isna().sum())}")

    episodes = build_episodes(df, rest_col="rest_day_p25")
    print(f"[episodes] gap=0 heavy episodes (p25 rest-op): {len(episodes)}")

    # Section 3: 2024 per-quarter PS 2x2.
    q2024 = ps_2x2_per_quarter_within_year(df, episodes, YEAR_TARGET)
    q2024.to_csv(OUTPUT_DIR / "pssubset_per_quarter_2024.csv", index=False)

    # Section 4: 2024 by-intensity PS 2x2.
    i2024 = ps_2x2_by_intensity_within_year(df, episodes, YEAR_TARGET)
    i2024.to_csv(OUTPUT_DIR / "pssubset_2024_by_intensity.csv", index=False)

    # Section 5: per-episode diagnostic on 2024 PS-True episodes.
    crash_df, noncrash_df = per_episode_diagnostic_2024(df, episodes, YEAR_TARGET)
    crash_df.to_csv(
        OUTPUT_DIR / "pssubset_2024_crash_events_diagnostic.csv", index=False,
    )
    noncrash_df.to_csv(
        OUTPUT_DIR / "pssubset_2024_noncrash_baseline_diagnostic.csv", index=False,
    )
    print(f"[section 5] 2024 PS-True crash-events: {len(crash_df)} "
          f"| non-crash: {len(noncrash_df)}")

    # Section 6: gevoelscore threshold sensitivity within 2024.
    ts2024 = threshold_sensitivity_within_year(df, episodes, YEAR_TARGET)
    ts2024.to_csv(OUTPUT_DIR / "pssubset_threshold_sensitivity_2024.csv", index=False)

    # Section 7: absolute-step-threshold companion.
    abs2024 = abs_step_companion_2x2(df, YEAR_TARGET)
    abs2024.to_csv(
        OUTPUT_DIR / "pssubset_absolute_step_threshold_2024.csv", index=False,
    )

    # Section 8: per-quarter PS RR in 2023 + 2025.
    q_neigh = ps_2x2_per_quarter_multiple_years(df, episodes, NEIGHBOUR_YEARS)
    q_neigh.to_csv(OUTPUT_DIR / "pssubset_per_quarter_all_years.csv", index=False)

    # Section 9: pre-window load crash-vs-non-crash 2024 PS.
    pw2024 = pre_window_load_comparison_2024(df, episodes, YEAR_TARGET)
    pw2024.to_csv(OUTPUT_DIR / "pssubset_2024_pre_window_load.csv", index=False)

    # Section 10: neighbouring-year PS-arm composition (2023, 2024, 2025).
    ncomp = neighbouring_year_composition(df, episodes, (2023, 2024, 2025))
    ncomp.to_csv(OUTPUT_DIR / "pssubset_2024_neighbouring_context.csv", index=False)

    print(f"\n[write] outputs in {OUTPUT_DIR}")
    for f in sorted(OUTPUT_DIR.glob("*.csv")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
