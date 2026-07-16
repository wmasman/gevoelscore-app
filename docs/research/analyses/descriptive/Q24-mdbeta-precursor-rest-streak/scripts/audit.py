"""Q24 MD-beta precursor: rest-adjacency + streak-length descriptive audit.

Descriptive audit of the heavy-day rest-adjacency + consecutive-heavy-days
streak structure with binary crash-in-5d outcome, to inform Stage D
readiness for the MD-beta operand
(docs/research/methodology/heavy_day_crash_risk_prediction.md LOCKED r1
2026-07-16).

Outputs are written to ../output/ and consumed by the sibling audit.md
descriptive card. This script is idempotent and re-runnable.

Frame: LC-era stratum (lc_phase == 'lc'), matches MD-beta stratum.
Heavy-day definition: exertion_class_lagged_lcera in {heavy, very_heavy}.
Episode unit: gap=0 contiguous heavy-day runs, episode-end = last day.
Streak length: number of days in the contiguous heavy-day run ending at D_end.
Rest-day operands (definitional pair per CONVENTIONS 3.3):
    primary   = total_steps < rolling_percentile_25(total_steps, 30d, min_periods=15)
    sensitivity = exertion_class_lagged_lcera in {none, light}
Rest-after-K(D_end) = any(rest_day(d) for d in [D_end+1, D_end+K])
Rest-before-K(D_start) = any(rest_day(d) for d in [D_start-K, D_start-1])
crash_in_5d(D_end) = any(is_crash[d] for d in [D_end+1, D_end+5])

Stage -1 descriptive audit only. NO inferential tests (Fisher exact +
Cochran-Armitage + bootstrap null are Stage D concerns).
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
K_LADDER = [1, 2, 3]
CRASH_WINDOW = 5
RANDOM_SEED = 20260716  # per MD-beta section 3.6; not used in Stage -1.


# ---------------------------------------------------------------------------
# Data loading + rest-day operand construction
# ---------------------------------------------------------------------------

def load_lc_stratum():
    """Load per_day_master.csv, filter to LC-era, add heavy / rest / crash cols."""
    df = pd.read_csv(INPUT, parse_dates=["date"])
    df = df[df["lc_phase"] == "lc"].copy().reset_index(drop=True)
    df["is_heavy"] = df["exertion_class_lagged_lcera"].isin(HEAVY_CLASSES)
    df["is_very_heavy"] = df["exertion_class_lagged_lcera"] == "very_heavy"
    df["is_heavy_only"] = df["exertion_class_lagged_lcera"] == "heavy"
    df["is_crash"] = df["is_crash"].fillna(False).astype(bool)
    df["year"] = df["date"].dt.year

    # Rest-day PRIMARY: total_steps < 30d rolling p25, min_periods=15.
    # Use a rolling window keyed on the row index (LC-era is contiguous, so
    # index-based rolling matches calendar rolling here). Guard: check for
    # any calendar gaps and fail loudly if present.
    diffs = df["date"].diff().dt.days.dropna()
    if not (diffs == 1).all():
        gap_count = int((diffs != 1).sum())
        raise RuntimeError(
            f"LC-era rows are not contiguous by day; {gap_count} gap(s) detected. "
            "Refactor rolling operand to calendar-anchored before proceeding."
        )
    steps = df["total_steps"].astype(float)
    # NaN in total_steps propagates through the quantile; treat NaN steps as
    # "no reading" -> rest_day undefined (NaN). Fillna avoided deliberately.
    rolling_p25 = steps.rolling(window=30, min_periods=15).quantile(0.25)
    df["rest_day_p25_threshold"] = rolling_p25
    df["rest_day_p25"] = np.where(
        steps.isna() | rolling_p25.isna(),
        np.nan,
        (steps < rolling_p25).astype(float),
    )
    # Store as float so NaN sentinel is preserved; convert to bool per-use.

    # Rest-day SENSITIVITY: exertion_class_lagged_lcera in {none, light}.
    # NaN class -> rest_day undefined.
    df["rest_day_class"] = np.where(
        df["exertion_class_lagged_lcera"].isna(),
        np.nan,
        df["exertion_class_lagged_lcera"].isin(REST_CLASSES).astype(float),
    )
    return df


# ---------------------------------------------------------------------------
# Episode construction (gap=0 contiguous) with streak length + intensity fingerprint
# ---------------------------------------------------------------------------

def build_episodes(df):
    """Emit an episode table (one row per gap=0 contiguous heavy episode).

    Columns:
        episode_id, D_start, D_end, streak_length, L_bin, year_end,
        vh_count, vh_frac, end_class (heavy vs very_heavy on D_end),
        crash_in_5d, has_crash_in_5d_window_data,
        overlap_strict_clean (no other heavy day in [D_end+1, D_end+5]),
        rest_after_K, rest_before_K per K in K_LADDER x operand in {primary, sensitivity}.
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
        vh_slice = df.iloc[start:end + 1]["is_very_heavy"].astype(int)
        vh_count = int(vh_slice.sum())
        vh_frac = float(vh_count / length)
        # Bin streak length.
        if length == 1:
            L_bin = "1"
        elif length == 2:
            L_bin = "2"
        elif length == 3:
            L_bin = "3"
        else:
            L_bin = "4+"
        # Episode-end intensity stratum: heavy vs very_heavy on D_end.
        end_class = "very_heavy" if bool(end_row["is_very_heavy"]) else "heavy"
        # crash_in_5d: any is_crash in [D_end+1, D_end+5].
        c_lo = end + 1
        c_hi = min(end + CRASH_WINDOW, n - 1)
        if c_lo > n - 1:
            crash_in_5d = False
            has_window_data = False
        else:
            crash_slice = df.iloc[c_lo:c_hi + 1]["is_crash"]
            crash_in_5d = bool(crash_slice.any())
            has_window_data = (c_hi - c_lo + 1) == CRASH_WINDOW
        # Overlap-clean flag (parent MD 5.2 strict-clean at +5d):
        # no other heavy day in [D_end+1, D_end+5].
        if c_lo > n - 1:
            overlap_strict_clean = False
            overlap_data_ok = False
        else:
            heavy_after_slice = df.iloc[c_lo:c_hi + 1]["is_heavy"]
            overlap_strict_clean = not bool(heavy_after_slice.any())
            overlap_data_ok = (c_hi - c_lo + 1) == CRASH_WINDOW
        row = {
            "episode_id": ep_id,
            "D_start": df.iloc[start]["date"],
            "D_end": df.iloc[end]["date"],
            "streak_length": length,
            "L_bin": L_bin,
            "year_end": int(end_row["year"]),
            "vh_count": vh_count,
            "vh_frac": vh_frac,
            "end_class": end_class,
            "crash_in_5d": crash_in_5d,
            "crash_window_full": has_window_data,
            "overlap_strict_clean": overlap_strict_clean,
            "overlap_window_full": overlap_data_ok,
        }
        # Rest-after and rest-before indicators for each K x operand.
        for K in K_LADDER:
            row[f"rest_after_{K}_primary"] = _rest_indicator(
                df, "rest_day_p25", end + 1, end + K, n,
            )
            row[f"rest_after_{K}_sensitivity"] = _rest_indicator(
                df, "rest_day_class", end + 1, end + K, n,
            )
            row[f"rest_before_{K}_primary"] = _rest_indicator(
                df, "rest_day_p25", start - K, start - 1, n,
            )
            row[f"rest_before_{K}_sensitivity"] = _rest_indicator(
                df, "rest_day_class", start - K, start - 1, n,
            )
        episodes.append(row)
        i = end + 1
    ep_df = pd.DataFrame(episodes)
    return ep_df


def _rest_indicator(df, col, lo_idx, hi_idx, n):
    """Return True/False/NaN for any(rest_day) in [lo_idx, hi_idx] inclusive.

    NaN if the window falls outside the corpus at either end AND no rest-True
    is observed inside the available slice (per CONVENTIONS 5 zero-vs-NaN:
    missing != False). If any observed rest-True is in the window we return
    True even if the window is partially clipped.
    """
    lo = max(lo_idx, 0)
    hi = min(hi_idx, n - 1)
    if lo > hi:
        return np.nan
    window = df.iloc[lo:hi + 1][col]
    # Any observed True -> True.
    observed_true = (window == 1.0).any()
    if observed_true:
        return True
    # No True observed. If any NaN OR window truncated at either end -> NaN.
    truncated = (lo_idx < 0) or (hi_idx > n - 1)
    any_nan = window.isna().any()
    if truncated or any_nan:
        return np.nan
    return False


# ---------------------------------------------------------------------------
# Wilson score CI for a proportion (small-sample-appropriate; hand-computed)
# ---------------------------------------------------------------------------

def wilson_ci(k, n, z=1.96):
    """Return (p_hat, lower, upper) Wilson score 95% CI. NaN when n == 0."""
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    denom = 1.0 + z ** 2 / n
    centre = (p + z ** 2 / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2))) / denom
    return (p, centre - half, centre + half)


# ---------------------------------------------------------------------------
# Section 6.1 -- rest-day distribution
# ---------------------------------------------------------------------------

def rest_day_distribution(df):
    n_lc = len(df)
    primary_true = int((df["rest_day_p25"] == 1.0).sum())
    primary_false = int((df["rest_day_p25"] == 0.0).sum())
    primary_nan = int(df["rest_day_p25"].isna().sum())
    sens_true = int((df["rest_day_class"] == 1.0).sum())
    sens_false = int((df["rest_day_class"] == 0.0).sum())
    sens_nan = int(df["rest_day_class"].isna().sum())
    # exertion_class breakdown (LC-era)
    class_counts = df["exertion_class_lagged_lcera"].value_counts(dropna=False)
    rows = [
        {
            "operand": "primary_p25",
            "definition": "total_steps < 30d rolling p25 (min_periods=15)",
            "n_true": primary_true,
            "n_false": primary_false,
            "n_nan": primary_nan,
            "n_total": n_lc,
            "rate_over_total": primary_true / n_lc,
            "rate_over_non_nan": primary_true / (primary_true + primary_false)
                if (primary_true + primary_false) > 0 else float("nan"),
        },
        {
            "operand": "sensitivity_class",
            "definition": "exertion_class_lagged_lcera in {none, light}",
            "n_true": sens_true,
            "n_false": sens_false,
            "n_nan": sens_nan,
            "n_total": n_lc,
            "rate_over_total": sens_true / n_lc,
            "rate_over_non_nan": sens_true / (sens_true + sens_false)
                if (sens_true + sens_false) > 0 else float("nan"),
        },
    ]
    for cls in ["none", "light", "moderate", "heavy", "very_heavy"]:
        n = int(class_counts.get(cls, 0))
        rows.append({
            "operand": f"class_breakdown_{cls}",
            "definition": f"exertion_class_lagged_lcera == '{cls}'",
            "n_true": n,
            "n_false": n_lc - n,
            "n_nan": 0,
            "n_total": n_lc,
            "rate_over_total": n / n_lc,
            "rate_over_non_nan": float("nan"),
        })
    n_nan_class = int(class_counts.get(np.nan, 0)) \
        if np.nan in class_counts.index else \
        int(df["exertion_class_lagged_lcera"].isna().sum())
    rows.append({
        "operand": "class_breakdown_NaN",
        "definition": "exertion_class_lagged_lcera is NaN",
        "n_true": n_nan_class,
        "n_false": n_lc - n_nan_class,
        "n_nan": 0,
        "n_total": n_lc,
        "rate_over_total": n_nan_class / n_lc,
        "rate_over_non_nan": float("nan"),
    })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 6.2 -- streak-length distribution
# ---------------------------------------------------------------------------

def streak_length_distribution(episodes):
    rows = []
    n_total = len(episodes)
    for L_bin in ["1", "2", "3", "4+"]:
        n = int((episodes["L_bin"] == L_bin).sum())
        rows.append({
            "L_bin": L_bin,
            "n_episodes": n,
            "rate": n / n_total if n_total > 0 else float("nan"),
        })
    # sub-bins within 4+
    for L in sorted(episodes[episodes["L_bin"] == "4+"]["streak_length"].unique()):
        n = int((episodes["streak_length"] == L).sum())
        rows.append({
            "L_bin": f"sub_{int(L)}",
            "n_episodes": n,
            "rate": n / n_total if n_total > 0 else float("nan"),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 6.3 -- streak-length x intensity cross-tab
# ---------------------------------------------------------------------------

def streak_intensity_crosstab(episodes):
    rows = []
    for L_bin in ["1", "2", "3", "4+"]:
        sub = episodes[episodes["L_bin"] == L_bin]
        rows.append({
            "L_bin": L_bin,
            "n_episodes": int(len(sub)),
            "mean_vh_frac": float(sub["vh_frac"].mean()) if len(sub) else float("nan"),
            "median_vh_frac": float(sub["vh_frac"].median()) if len(sub) else float("nan"),
            "mean_vh_count": float(sub["vh_count"].mean()) if len(sub) else float("nan"),
            "median_vh_count": float(sub["vh_count"].median()) if len(sub) else float("nan"),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 6.4 -- streak-length x era cross-tab
# ---------------------------------------------------------------------------

def streak_era_crosstab(episodes):
    ct = pd.crosstab(episodes["year_end"], episodes["L_bin"], dropna=False)
    for L_bin in ["1", "2", "3", "4+"]:
        if L_bin not in ct.columns:
            ct[L_bin] = 0
    ct = ct[["1", "2", "3", "4+"]]
    ct["n_episodes"] = ct.sum(axis=1)
    ct = ct.reset_index()
    return ct


# ---------------------------------------------------------------------------
# Section 6.5 -- rest-adjacent prevalence (all 12 cells: K x direction x operand)
# ---------------------------------------------------------------------------

def rest_adjacent_prevalence(episodes):
    rows = []
    n_ep = len(episodes)
    for K in K_LADDER:
        for direction in ["after", "before"]:
            for operand in ["primary", "sensitivity"]:
                col = f"rest_{direction}_{K}_{operand}"
                s = episodes[col]
                n_true = int((s == True).sum())
                n_false = int((s == False).sum())
                n_nan = int(s.isna().sum())
                rows.append({
                    "K": K,
                    "direction": direction,
                    "operand": operand,
                    "n_rest_true": n_true,
                    "n_rest_false": n_false,
                    "n_rest_nan": n_nan,
                    "n_episodes_total": n_ep,
                    "rate_over_total": n_true / n_ep if n_ep > 0 else float("nan"),
                    "rate_over_non_nan": (n_true / (n_true + n_false))
                        if (n_true + n_false) > 0 else float("nan"),
                })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 6.6 (extended) -- full 2x2 grid: K x direction x operand x crash-in-5d
# ---------------------------------------------------------------------------

def rest_adjacency_crash_2x2_full_grid(episodes, nan_policy="drop"):
    """Emit the 12-cell grid under a chosen NaN-handling policy.

    nan_policy:
        "drop"     -- Drop episodes where the rest indicator is NaN
                      (CONVENTIONS 5 zero-vs-NaN discipline; PRIMARY for
                      this Stage -1 audit).
        "nan_false" -- Coerce NaN to False (matches MD-beta section 6.6
                      implicit convention; emitted as a verification
                      companion so the parent MD-beta numbers reproduce
                      byte-for-byte at K=3 primary).
    """
    rows = []
    for K in K_LADDER:
        for direction in ["after", "before"]:
            for operand in ["primary", "sensitivity"]:
                col = f"rest_{direction}_{K}_{operand}"
                sub = episodes.copy()
                if nan_policy == "drop":
                    sub = sub[sub[col].notna()].copy()
                    sub[col] = sub[col].astype(bool)
                elif nan_policy == "nan_false":
                    sub[col] = sub[col].fillna(False).astype(bool)
                else:
                    raise ValueError(f"unknown nan_policy: {nan_policy}")
                # Also drop episodes without a full +5d crash window observation.
                sub = sub[sub["crash_window_full"] == True]
                n_ra_true_crash_true = int(((sub[col] == True) & (sub["crash_in_5d"] == True)).sum())
                n_ra_true_crash_false = int(((sub[col] == True) & (sub["crash_in_5d"] == False)).sum())
                n_ra_false_crash_true = int(((sub[col] == False) & (sub["crash_in_5d"] == True)).sum())
                n_ra_false_crash_false = int(((sub[col] == False) & (sub["crash_in_5d"] == False)).sum())
                n_true = n_ra_true_crash_true + n_ra_true_crash_false
                n_false = n_ra_false_crash_true + n_ra_false_crash_false
                p_true, lo_t, hi_t = wilson_ci(n_ra_true_crash_true, n_true)
                p_false, lo_f, hi_f = wilson_ci(n_ra_false_crash_true, n_false)
                if p_false and not math.isnan(p_false) and p_false > 0:
                    rr = p_true / p_false
                else:
                    rr = float("nan")
                rd = p_true - p_false if not (math.isnan(p_true) or math.isnan(p_false)) else float("nan")
                rows.append({
                    "K": K,
                    "direction": direction,
                    "operand": operand,
                    "n_episodes_used": len(sub),
                    "rest_true_crash_true": n_ra_true_crash_true,
                    "rest_true_crash_false": n_ra_true_crash_false,
                    "rest_false_crash_true": n_ra_false_crash_true,
                    "rest_false_crash_false": n_ra_false_crash_false,
                    "n_rest_true": n_true,
                    "n_rest_false": n_false,
                    "crash_rate_rest_true": p_true,
                    "crash_rate_rest_true_wilson_lo": lo_t,
                    "crash_rate_rest_true_wilson_hi": hi_t,
                    "crash_rate_rest_false": p_false,
                    "crash_rate_rest_false_wilson_lo": lo_f,
                    "crash_rate_rest_false_wilson_hi": hi_f,
                    "risk_ratio_rest_true_over_false": rr,
                    "risk_difference_rest_true_minus_false": rd,
                    "sign": ("inverted" if (not math.isnan(rr)) and rr > 1.0
                             else ("match_pre_commit" if (not math.isnan(rr)) and rr < 1.0
                                   else "unity_or_undefined")),
                })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Streak-length x crash-in-5d (both pools)
# ---------------------------------------------------------------------------

def streak_length_crash_table(episodes):
    rows = []
    # All-episodes pool.
    full = episodes[episodes["crash_window_full"] == True]
    # Strict-clean subset.
    clean = full[full["overlap_strict_clean"] == True]
    for pool_label, pool_df in [("all_episodes", full), ("strict_clean", clean)]:
        for L_bin in ["1", "2", "3", "4+"]:
            sub = pool_df[pool_df["L_bin"] == L_bin]
            n = len(sub)
            k = int(sub["crash_in_5d"].sum())
            p, lo, hi = wilson_ci(k, n)
            rows.append({
                "pool": pool_label,
                "L_bin": L_bin,
                "n_episodes": n,
                "n_crash_in_5d": k,
                "crash_rate": p,
                "wilson_lo": lo,
                "wilson_hi": hi,
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 9 -- rest-adjacency x crash x era 3-way (primary p25 rest-after K=3)
# ---------------------------------------------------------------------------

def rest_adjacency_by_era(episodes):
    col = "rest_after_3_primary"
    sub = episodes[(episodes[col].notna()) & (episodes["crash_window_full"] == True)].copy()
    sub[col] = sub[col].astype(bool)
    rows = []
    for year in sorted(sub["year_end"].unique()):
        year_sub = sub[sub["year_end"] == year]
        for rest_val in [True, False]:
            arm = year_sub[year_sub[col] == rest_val]
            n = len(arm)
            k = int(arm["crash_in_5d"].sum())
            p, lo, hi = wilson_ci(k, n)
            rows.append({
                "year": int(year),
                "rest_after_3_primary": rest_val,
                "n_episodes": n,
                "n_crash_in_5d": k,
                "crash_rate": p,
                "wilson_lo": lo,
                "wilson_hi": hi,
            })
        # per-year RR + RD
        arm_t = year_sub[year_sub[col] == True]
        arm_f = year_sub[year_sub[col] == False]
        p_t = int(arm_t["crash_in_5d"].sum()) / len(arm_t) if len(arm_t) else float("nan")
        p_f = int(arm_f["crash_in_5d"].sum()) / len(arm_f) if len(arm_f) else float("nan")
        rr = p_t / p_f if (p_f and not math.isnan(p_f) and p_f > 0) else float("nan")
        rd = p_t - p_f if not (math.isnan(p_t) or math.isnan(p_f)) else float("nan")
        rows.append({
            "year": int(year),
            "rest_after_3_primary": "RR_true_over_false",
            "n_episodes": len(arm_t) + len(arm_f),
            "n_crash_in_5d": int(arm_t["crash_in_5d"].sum()) + int(arm_f["crash_in_5d"].sum()),
            "crash_rate": rr,
            "wilson_lo": float("nan"),
            "wilson_hi": float("nan"),
        })
        rows.append({
            "year": int(year),
            "rest_after_3_primary": "RD_true_minus_false",
            "n_episodes": len(arm_t) + len(arm_f),
            "n_crash_in_5d": int(arm_t["crash_in_5d"].sum()) + int(arm_f["crash_in_5d"].sum()),
            "crash_rate": rd,
            "wilson_lo": float("nan"),
            "wilson_hi": float("nan"),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 10 -- rest-adjacency x crash x intensity (heavy vs very_heavy end)
# ---------------------------------------------------------------------------

def rest_adjacency_by_intensity(episodes):
    col = "rest_after_3_primary"
    sub = episodes[(episodes[col].notna()) & (episodes["crash_window_full"] == True)].copy()
    sub[col] = sub[col].astype(bool)
    rows = []
    for stratum in ["heavy", "very_heavy"]:
        stratum_sub = sub[sub["end_class"] == stratum]
        for rest_val in [True, False]:
            arm = stratum_sub[stratum_sub[col] == rest_val]
            n = len(arm)
            k = int(arm["crash_in_5d"].sum())
            p, lo, hi = wilson_ci(k, n)
            rows.append({
                "end_class": stratum,
                "rest_after_3_primary": rest_val,
                "n_episodes": n,
                "n_crash_in_5d": k,
                "crash_rate": p,
                "wilson_lo": lo,
                "wilson_hi": hi,
            })
        arm_t = stratum_sub[stratum_sub[col] == True]
        arm_f = stratum_sub[stratum_sub[col] == False]
        p_t = int(arm_t["crash_in_5d"].sum()) / len(arm_t) if len(arm_t) else float("nan")
        p_f = int(arm_f["crash_in_5d"].sum()) / len(arm_f) if len(arm_f) else float("nan")
        rr = p_t / p_f if (p_f and not math.isnan(p_f) and p_f > 0) else float("nan")
        rd = p_t - p_f if not (math.isnan(p_t) or math.isnan(p_f)) else float("nan")
        rows.append({
            "end_class": stratum,
            "rest_after_3_primary": "RR_true_over_false",
            "n_episodes": len(arm_t) + len(arm_f),
            "n_crash_in_5d": int(arm_t["crash_in_5d"].sum()) + int(arm_f["crash_in_5d"].sum()),
            "crash_rate": rr,
            "wilson_lo": float("nan"),
            "wilson_hi": float("nan"),
        })
        rows.append({
            "end_class": stratum,
            "rest_after_3_primary": "RD_true_minus_false",
            "n_episodes": len(arm_t) + len(arm_f),
            "n_crash_in_5d": int(arm_t["crash_in_5d"].sum()) + int(arm_f["crash_in_5d"].sum()),
            "crash_rate": rd,
            "wilson_lo": float("nan"),
            "wilson_hi": float("nan"),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 11 -- overlap-policy sensitivity 2x2 (K=3 primary rest-after, strict-clean)
# ---------------------------------------------------------------------------

def overlap_policy_sensitivity_2x2(episodes):
    col = "rest_after_3_primary"
    full = episodes[
        (episodes[col].notna())
        & (episodes["crash_window_full"] == True)
        & (episodes["overlap_strict_clean"] == True)
    ].copy()
    full[col] = full[col].astype(bool)
    n_ra_true_crash_true = int(((full[col] == True) & (full["crash_in_5d"] == True)).sum())
    n_ra_true_crash_false = int(((full[col] == True) & (full["crash_in_5d"] == False)).sum())
    n_ra_false_crash_true = int(((full[col] == False) & (full["crash_in_5d"] == True)).sum())
    n_ra_false_crash_false = int(((full[col] == False) & (full["crash_in_5d"] == False)).sum())
    n_true = n_ra_true_crash_true + n_ra_true_crash_false
    n_false = n_ra_false_crash_true + n_ra_false_crash_false
    p_true, lo_t, hi_t = wilson_ci(n_ra_true_crash_true, n_true)
    p_false, lo_f, hi_f = wilson_ci(n_ra_false_crash_true, n_false)
    rr = p_true / p_false if (p_false and not math.isnan(p_false) and p_false > 0) else float("nan")
    rd = p_true - p_false if not (math.isnan(p_true) or math.isnan(p_false)) else float("nan")
    rows = [{
        "pool": "strict_clean",
        "K": 3,
        "direction": "after",
        "operand": "primary",
        "n_episodes_used": len(full),
        "rest_true_crash_true": n_ra_true_crash_true,
        "rest_true_crash_false": n_ra_true_crash_false,
        "rest_false_crash_true": n_ra_false_crash_true,
        "rest_false_crash_false": n_ra_false_crash_false,
        "n_rest_true": n_true,
        "n_rest_false": n_false,
        "crash_rate_rest_true": p_true,
        "crash_rate_rest_true_wilson_lo": lo_t,
        "crash_rate_rest_true_wilson_hi": hi_t,
        "crash_rate_rest_false": p_false,
        "crash_rate_rest_false_wilson_lo": lo_f,
        "crash_rate_rest_false_wilson_hi": hi_f,
        "risk_ratio_rest_true_over_false": rr,
        "risk_difference_rest_true_minus_false": rd,
    }]
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Section 12 -- streak-length x era x crash-in-5d
# ---------------------------------------------------------------------------

def streak_length_by_era_crash(episodes):
    sub = episodes[episodes["crash_window_full"] == True].copy()
    rows = []
    for year in sorted(sub["year_end"].unique()):
        year_sub = sub[sub["year_end"] == year]
        for L_bin in ["1", "2", "3", "4+"]:
            arm = year_sub[year_sub["L_bin"] == L_bin]
            n = len(arm)
            k = int(arm["crash_in_5d"].sum())
            p, lo, hi = wilson_ci(k, n)
            rows.append({
                "year": int(year),
                "L_bin": L_bin,
                "n_episodes": n,
                "n_crash_in_5d": k,
                "crash_rate": p,
                "wilson_lo": lo,
                "wilson_hi": hi,
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# main -- drive all outputs
# ---------------------------------------------------------------------------

def main():
    df = load_lc_stratum()
    print(f"[stratum] LC-era rows: {len(df)}")
    print(f"[stratum] heavy days: {int(df['is_heavy'].sum())}; very_heavy: {int(df['is_very_heavy'].sum())}")
    print(f"[stratum] crash days: {int(df['is_crash'].sum())}")
    print(f"[stratum] rest_day_p25 true: {int((df['rest_day_p25'] == 1.0).sum())} "
          f"nan: {int(df['rest_day_p25'].isna().sum())}")
    print(f"[stratum] rest_day_class true: {int((df['rest_day_class'] == 1.0).sum())} "
          f"nan: {int(df['rest_day_class'].isna().sum())}")

    # Build episode table.
    episodes = build_episodes(df)
    print(f"[episodes] gap=0 heavy episodes on LC-era: {len(episodes)}")
    print(f"[episodes] streak-length distribution: "
          f"1={int((episodes['L_bin'] == '1').sum())}, "
          f"2={int((episodes['L_bin'] == '2').sum())}, "
          f"3={int((episodes['L_bin'] == '3').sum())}, "
          f"4+={int((episodes['L_bin'] == '4+').sum())}")

    # 6.1
    rest_day_distribution(df).to_csv(
        OUTPUT_DIR / "rest_day_distribution.csv", index=False,
    )
    # 6.2
    streak_length_distribution(episodes).to_csv(
        OUTPUT_DIR / "streak_length_distribution.csv", index=False,
    )
    # 6.3
    streak_intensity_crosstab(episodes).to_csv(
        OUTPUT_DIR / "streak_intensity_crosstab.csv", index=False,
    )
    # 6.4
    streak_era_crosstab(episodes).to_csv(
        OUTPUT_DIR / "streak_era_crosstab.csv", index=False,
    )
    # 6.5
    rest_adjacent_prevalence(episodes).to_csv(
        OUTPUT_DIR / "rest_adjacent_prevalence.csv", index=False,
    )
    # Extended 6.6 -- 12-cell grid
    rest_adjacency_crash_2x2_full_grid(episodes, nan_policy="drop").to_csv(
        OUTPUT_DIR / "rest_adjacency_crash_2x2_full_grid.csv", index=False,
    )
    # Companion CSV: NaN-as-False policy to reproduce MD-beta 6.6 numbers
    # byte-for-byte at K=3 primary. Documented in audit.md section 7.
    rest_adjacency_crash_2x2_full_grid(episodes, nan_policy="nan_false").to_csv(
        OUTPUT_DIR / "rest_adjacency_crash_2x2_full_grid_naneqfalse.csv", index=False,
    )
    # Streak-length x crash table
    streak_length_crash_table(episodes).to_csv(
        OUTPUT_DIR / "streak_length_crash_table.csv", index=False,
    )
    # Rest-adjacency x era
    rest_adjacency_by_era(episodes).to_csv(
        OUTPUT_DIR / "rest_adjacency_by_era.csv", index=False,
    )
    # Rest-adjacency x intensity
    rest_adjacency_by_intensity(episodes).to_csv(
        OUTPUT_DIR / "rest_adjacency_by_intensity.csv", index=False,
    )
    # Overlap-policy sensitivity 2x2 (K=3 primary, strict-clean)
    overlap_policy_sensitivity_2x2(episodes).to_csv(
        OUTPUT_DIR / "overlap_policy_sensitivity_2x2.csv", index=False,
    )
    # Streak-length x era x crash
    streak_length_by_era_crash(episodes).to_csv(
        OUTPUT_DIR / "streak_length_by_era_crash.csv", index=False,
    )

    print(f"\n[write] outputs in {OUTPUT_DIR}")
    for f in sorted(OUTPUT_DIR.glob("*.csv")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
