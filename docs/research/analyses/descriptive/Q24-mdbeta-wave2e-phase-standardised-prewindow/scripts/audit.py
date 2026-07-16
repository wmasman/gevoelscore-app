"""Q24 MD-beta Wave 2E descriptive audit -- phase-standardised pre-window covariate operand.

Wave 2E sibling of parent Q24 MD-beta Wave 2D audit
(../Q24-mdbeta-wave2d-2024-residual-tension/audit.md LOCKED r1 2026-07-16).

Purpose: compute + validate a phase-standardised pre-window covariate
operand that MD-beta r2 will codify as R2C primary covariate for the
rest-adjacency arc. Wave 2D section 12.3 identified pre-window 30d
effective_exertion_min as a candidate covariate on the rest-adjacency
arc; Wave 2D section 10.3 flagged the citalopram phase-boundary at
2024-04-09 as creating a ~4x step-shift in pre-window absolute values.
Any operand cut-point applied on absolute values across the phase
boundary is fully phase-confounded.

Wave 2E computes two candidate operand definitions (definitional pair
per CONVENTIONS section 3.3):

  Candidate operand 1: PHASE-STANDARDISED
    phase_std_pre_window_load(D_end)
      = pre_window_load(D_end) - phase_mean_pre_window_load(P(D_end))
    where pre_window_load(D_end) = sum(effective_exertion_min[d]
                                       for d in [D_end - 30, D_end - 1])
    and phase_mean_pre_window_load(P) = mean(pre_window_load) across
    all heavy-episode-ends in phase P.

  Candidate operand 2: PHASE-STRATIFIED
    high_pre_window_p75(D_end)
      = (pre_window_load(D_end) > phase_p75_pre_window_load(P(D_end)))
    where phase_p75_pre_window_load(P) = 75th percentile of
    pre_window_load across all heavy-episode-ends in phase P.

Task: descriptive validation that either operand DISCRIMINATES the 2024
crash-vs-non-crash signal that Wave 2D section 9 surfaced on absolute
values. If YES -> operand is defensible for r2 codification. If NO ->
operand is not fit-for-purpose and r2 must codify differently or defer.

Outputs are written to ../output/ and consumed by the sibling audit.md
descriptive card. This script is idempotent and re-runnable.

Frame: LC-era stratum (lc_phase == 'lc'), matches parent Wave 2D
stratum. Heavy-day definition inherited (exertion_class_lagged_lcera in
{heavy, very_heavy}). Rest-day primary and PS-True (proactive-strategic
rest-after K=3) definitions inherited verbatim from parent Wave 2C
audit.

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
K_REST_AFTER = 3          # MD-beta section 3.2 primary K value
LOOKBACK_CRASH = 3        # rest-day quadrant: is_crash in [rest_day - 3, rest_day - 1]
PRIMARY_GS = 5
PRE_WINDOW_DAYS = 30
PRE_WINDOW_MIN_VALID = 15  # parent Q24 MD section 7.11 minimum-valid-points rule
RANDOM_SEED = 20260716    # declared per MD-beta section 3.6; unused.

# MD-alpha section 3.1 recovery_phase axis (4 buckets, ordered).
PHASE_ORDER = [
    "lc_pre_ergo",
    "pacing_pre_citalopram_learning",
    "pacing_habit_established",
    "citalopram_modulated",
]


# ---------------------------------------------------------------------------
# Data loading + rest-day + gevoelscore-bucket construction
# ---------------------------------------------------------------------------

def load_lc_stratum():
    """Load per_day_master.csv, filter to LC-era, add heavy/rest cols."""
    df = pd.read_csv(INPUT, parse_dates=["date"])
    df = df[df["lc_phase"] == "lc"].copy().reset_index(drop=True)
    df["is_heavy"] = df["exertion_class_lagged_lcera"].isin(HEAVY_CLASSES)
    df["is_very_heavy"] = df["exertion_class_lagged_lcera"] == "very_heavy"
    df["is_heavy_only"] = df["exertion_class_lagged_lcera"] == "heavy"
    df["is_crash"] = df["is_crash"].fillna(False).astype(bool)
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter

    diffs = df["date"].diff().dt.days.dropna()
    if not (diffs == 1).all():
        gap_count = int((diffs != 1).sum())
        raise RuntimeError(
            f"LC-era rows are not contiguous by day; {gap_count} gap(s) detected."
        )

    steps = df["total_steps"].astype(float)
    rolling_p25 = steps.rolling(window=30, min_periods=15).quantile(0.25)
    df["rest_day_p25"] = np.where(
        steps.isna() | rolling_p25.isna(),
        np.nan,
        (steps < rolling_p25).astype(float),
    )
    return df


# ---------------------------------------------------------------------------
# Episode construction (gap=0 contiguous heavy runs)
# ---------------------------------------------------------------------------

def build_episodes(df):
    """Emit episode table (one row per gap=0 heavy episode).

    Uses rolling-p25 rest-day operand (primary per MD-beta section 3.1).
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
        phase = str(end_row["recovery_phase"])

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
                val = df.loc[idx, "rest_day_p25"]
                if val == 1.0:
                    rest_indices.append(int(idx))
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
            "quarter_end": int(end_row["quarter"]),
            "end_class": end_class,
            "recovery_phase_end": phase,
            "crash_in_5d": crash_in_5d,
            "crash_window_full": has_window_data,
            "rest_after_3_primary": rest_after_indicator,
            "rest_indices_after_K3": rest_indices,
        })
        i = end + 1
    return pd.DataFrame(episodes)


# ---------------------------------------------------------------------------
# Pre-window load: [D_end - 30, D_end - 1] per Wave 2E task specification
# ---------------------------------------------------------------------------

def pre_window_load_at_end(df, D_end_idx, days=PRE_WINDOW_DAYS):
    """Compute pre-window 30d sum of effective_exertion_min in
    [D_end - days, D_end - 1]. Returns (sum, n_valid_days).

    Per parent Q24 MD section 7.11 minimum-valid-points rule: require at
    least PRE_WINDOW_MIN_VALID valid points. If < min, return NaN.
    """
    lo = max(int(D_end_idx) - days, 0)
    hi = int(D_end_idx) - 1
    if lo > hi:
        return float("nan"), 0
    win = df.iloc[lo:hi + 1]["effective_exertion_min"]
    n_valid = int(win.notna().sum())
    if n_valid < PRE_WINDOW_MIN_VALID:
        return float("nan"), n_valid
    return float(win.fillna(0).sum()), n_valid


# ---------------------------------------------------------------------------
# Wilson score CI + PS-episode helpers (inherited machinery)
# ---------------------------------------------------------------------------

def wilson_ci(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    denom = 1.0 + z ** 2 / n
    centre = (p + z ** 2 / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2))) / denom
    return (p, centre - half, centre + half)


def _crash_in_lookback(df, rest_idx, lookback=LOOKBACK_CRASH):
    lo = max(rest_idx - lookback, 0)
    hi = rest_idx - 1
    if lo > hi:
        return False
    return bool(df.iloc[lo:hi + 1]["is_crash"].any())


def _episode_proactive_strategic(df, ep, strategic_threshold=PRIMARY_GS):
    """Episode is proactive-strategic if any of its K=3 rest-days has NO
    crash in the 3d lookback AND gevoelscore >= strategic_threshold on the
    rest-day (per Wave 2C section 5)."""
    if not ep["rest_after_3_primary"]:
        return False
    for rest_idx in ep["rest_indices_after_K3"]:
        crash_before = _crash_in_lookback(df, rest_idx)
        gs_val = df.iloc[rest_idx]["gevoelscore"]
        if pd.isna(gs_val):
            continue
        if (not crash_before) and (gs_val >= strategic_threshold):
            return True
    return False


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
# Section 3: per-phase pre_window_load baselines
# ---------------------------------------------------------------------------

def compute_phase_baselines(df, episodes):
    """For each of the 4 phases, compute mean/median/p25/p75/std of
    pre_window_load across all heavy-episode-ends in that phase.

    Uses ALL 314 heavy-episode-ends on the LC-era (not restricted to
    rest-adjacent or PS-True). This is the reference baseline table for
    phase-standardisation.
    """
    per_ep = []
    for _, ep in episodes.iterrows():
        pw_sum, n_valid = pre_window_load_at_end(df, ep["D_end_idx"])
        per_ep.append({
            "episode_id": int(ep["episode_id"]),
            "D_end": pd.Timestamp(ep["D_end"]).strftime("%Y-%m-%d"),
            "recovery_phase_end": ep["recovery_phase_end"],
            "pre_window_load": pw_sum,
            "pre_window_n_valid_days": n_valid,
        })
    per_ep_df = pd.DataFrame(per_ep)

    rows = []
    for phase in PHASE_ORDER:
        s = per_ep_df[per_ep_df["recovery_phase_end"] == phase]
        vals = s["pre_window_load"].dropna()
        rows.append({
            "recovery_phase": phase,
            "n_episode_ends_in_phase": len(s),
            "n_valid_pre_window": len(vals),
            "pre_window_load_mean": (
                float(vals.mean()) if len(vals) > 0 else float("nan")
            ),
            "pre_window_load_median": (
                float(vals.median()) if len(vals) > 0 else float("nan")
            ),
            "pre_window_load_p25": (
                float(vals.quantile(0.25)) if len(vals) > 0 else float("nan")
            ),
            "pre_window_load_p75": (
                float(vals.quantile(0.75)) if len(vals) > 0 else float("nan")
            ),
            "pre_window_load_std": (
                float(vals.std(ddof=1)) if len(vals) > 1 else float("nan")
            ),
        })
    return pd.DataFrame(rows), per_ep_df


# ---------------------------------------------------------------------------
# Section 4/5: phase-standardised + phase-stratified operands on episodes
# ---------------------------------------------------------------------------

def attach_phase_operands(per_ep_df, baselines_df):
    """Attach phase-standardised residual + phase-p75 binary flag to each
    per-episode row using the baselines table."""
    phase_mean = dict(zip(
        baselines_df["recovery_phase"], baselines_df["pre_window_load_mean"],
    ))
    phase_p75 = dict(zip(
        baselines_df["recovery_phase"], baselines_df["pre_window_load_p75"],
    ))
    out = per_ep_df.copy()
    out["phase_mean_pre_window_load"] = out["recovery_phase_end"].map(phase_mean)
    out["phase_p75_pre_window_load"] = out["recovery_phase_end"].map(phase_p75)
    out["phase_std_pre_window_load"] = (
        out["pre_window_load"] - out["phase_mean_pre_window_load"]
    )
    # Compute binary flag as object dtype so NaN can be stored where the
    # pre_window_load is NaN (validity gate). If no NaN exists, the column
    # is effectively bool but object-typed for safety.
    hi_flag = (out["pre_window_load"] > out["phase_p75_pre_window_load"]).astype(object)
    hi_flag[out["pre_window_load"].isna()] = np.nan
    out["high_pre_window_p75"] = hi_flag
    return out


def build_ps_2024_frame(df, episodes, baselines_df, per_ep_baseline):
    """Return a per-episode DataFrame for 2024 heavy-episode-ends carrying
    raw + phase-standardised + phase-stratified operand values, along with
    crash_in_5d + PS-True + end_class + recovery_phase flags."""
    sub_all = prepare_ps_episodes(df, episodes)
    year_ep = sub_all[sub_all["year_end"] == 2024].copy()
    if len(year_ep) == 0:
        return pd.DataFrame()

    # Attach operand columns from per_ep_baseline (which covers all 314 eps).
    attached = attach_phase_operands(per_ep_baseline, baselines_df)
    attached_by_id = attached.set_index("episode_id")

    rows = []
    for _, ep in year_ep.iterrows():
        eid = int(ep["episode_id"])
        if eid not in attached_by_id.index:
            continue
        a = attached_by_id.loc[eid]
        rows.append({
            "episode_id": eid,
            "D_end": pd.Timestamp(ep["D_end"]).strftime("%Y-%m-%d"),
            "year_end": int(ep["year_end"]),
            "quarter_end": int(ep["quarter_end"]),
            "recovery_phase_end": ep["recovery_phase_end"],
            "end_class": ep["end_class"],
            "streak_length": int(ep["streak_length"]),
            "proactive_strategic": bool(ep["proactive_strategic"]),
            "crash_in_5d": bool(ep["crash_in_5d"]),
            "pre_window_load": float(a["pre_window_load"]) if pd.notna(a["pre_window_load"]) else float("nan"),
            "phase_mean_pre_window_load": float(a["phase_mean_pre_window_load"]),
            "phase_p75_pre_window_load": float(a["phase_p75_pre_window_load"]),
            "phase_std_pre_window_load": float(a["phase_std_pre_window_load"]) if pd.notna(a["phase_std_pre_window_load"]) else float("nan"),
            "high_pre_window_p75": (
                bool(a["high_pre_window_p75"])
                if pd.notna(a["high_pre_window_p75"]) else float("nan")
            ),
        })
    return pd.DataFrame(rows)


def build_ps_year_frame(df, episodes, baselines_df, per_ep_baseline, target_year):
    """Same shape as build_ps_2024_frame but for arbitrary target_year."""
    sub_all = prepare_ps_episodes(df, episodes)
    year_ep = sub_all[sub_all["year_end"] == target_year].copy()
    if len(year_ep) == 0:
        return pd.DataFrame()
    attached = attach_phase_operands(per_ep_baseline, baselines_df)
    attached_by_id = attached.set_index("episode_id")
    rows = []
    for _, ep in year_ep.iterrows():
        eid = int(ep["episode_id"])
        if eid not in attached_by_id.index:
            continue
        a = attached_by_id.loc[eid]
        rows.append({
            "episode_id": eid,
            "D_end": pd.Timestamp(ep["D_end"]).strftime("%Y-%m-%d"),
            "year_end": int(ep["year_end"]),
            "quarter_end": int(ep["quarter_end"]),
            "recovery_phase_end": ep["recovery_phase_end"],
            "end_class": ep["end_class"],
            "streak_length": int(ep["streak_length"]),
            "proactive_strategic": bool(ep["proactive_strategic"]),
            "crash_in_5d": bool(ep["crash_in_5d"]),
            "pre_window_load": float(a["pre_window_load"]) if pd.notna(a["pre_window_load"]) else float("nan"),
            "phase_std_pre_window_load": float(a["phase_std_pre_window_load"]) if pd.notna(a["phase_std_pre_window_load"]) else float("nan"),
            "high_pre_window_p75": (
                bool(a["high_pre_window_p75"])
                if pd.notna(a["high_pre_window_p75"]) else float("nan")
            ),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 2x2 contingency helpers
# ---------------------------------------------------------------------------

def emit_2x2(pool_label, ep_sub, exposure_col, outcome_col="crash_in_5d"):
    """Emit a 2x2 contingency + Wilson CI + RR + RD for the exposure_col
    vs outcome_col on ep_sub. exposure_col is bool True/False; NaN rows
    are dropped."""
    s = ep_sub.copy()
    s = s[s[exposure_col].notna()]
    arm_true = s[s[exposure_col] == True]
    arm_false = s[s[exposure_col] == False]
    n_t = len(arm_true)
    n_f = len(arm_false)
    k_t = int(arm_true[outcome_col].sum())
    k_f = int(arm_false[outcome_col].sum())
    p_t, lo_t, hi_t = wilson_ci(k_t, n_t)
    p_f, lo_f, hi_f = wilson_ci(k_f, n_f)
    if not math.isnan(p_f) and p_f > 0:
        rr = p_t / p_f
    else:
        rr = float("nan")
    rd = (p_t - p_f) if not (math.isnan(p_t) or math.isnan(p_f)) else float("nan")
    return {
        "pool": pool_label,
        "exposure_col": exposure_col,
        "n_used": len(s),
        "exposure_true_n": n_t,
        "exposure_false_n": n_f,
        "exposure_true_crash": k_t,
        "exposure_false_crash": k_f,
        "rate_exposure_true": p_t,
        "rate_exposure_true_wilson_lo": lo_t,
        "rate_exposure_true_wilson_hi": hi_t,
        "rate_exposure_false": p_f,
        "rate_exposure_false_wilson_lo": lo_f,
        "rate_exposure_false_wilson_hi": hi_f,
        "risk_ratio_true_over_false": rr,
        "risk_difference_true_minus_false": rd,
        "viable_n_min5": (n_t >= 5) and (n_f >= 5),
    }


# ---------------------------------------------------------------------------
# Alternative cut-points sensitivity
# ---------------------------------------------------------------------------

def emit_alternative_cutpoints(ps_year_df, baselines_df, target_year):
    """Emit 2x2 for 3 alternative phase-standardised cut-points:
      cut A: phase_std_pre_window_load > 0 (primary, above phase mean)
      cut B: phase_std > 0.5 * phase_std_dev
      cut C: phase_std > 1.0 * phase_std_dev
    All applied to PS-True episodes.
    """
    ps_only = ps_year_df[ps_year_df["proactive_strategic"] == True].copy()
    if len(ps_only) == 0:
        return pd.DataFrame()

    phase_std_dev = dict(zip(
        baselines_df["recovery_phase"], baselines_df["pre_window_load_std"],
    ))

    # cut A: phase_std > 0
    ps_only["_phase_std_dev"] = ps_only["recovery_phase_end"].map(phase_std_dev)
    a = (ps_only["phase_std_pre_window_load"] > 0).astype(object)
    b = (ps_only["phase_std_pre_window_load"] > 0.5 * ps_only["_phase_std_dev"]).astype(object)
    c = (ps_only["phase_std_pre_window_load"] > 1.0 * ps_only["_phase_std_dev"]).astype(object)
    na_mask = ps_only["phase_std_pre_window_load"].isna()
    a[na_mask] = np.nan
    b[na_mask] = np.nan
    c[na_mask] = np.nan
    ps_only["cut_A_above_mean"] = a
    ps_only["cut_B_above_half_sd"] = b
    ps_only["cut_C_above_full_sd"] = c

    rows = []
    for label in ["cut_A_above_mean", "cut_B_above_half_sd", "cut_C_above_full_sd"]:
        row = emit_2x2(
            f"year_{target_year}_PS_True_{label}", ps_only, label,
        )
        row["cut_label"] = label
        row["year"] = target_year
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Cross-operand agreement helper
# ---------------------------------------------------------------------------

def emit_operand_agreement(ps_year_df):
    """For PS-True episodes, emit per-episode agreement between
    (phase_std_pre_window_load > 0) and (high_pre_window_p75 == True)."""
    ps_only = ps_year_df[ps_year_df["proactive_strategic"] == True].copy()
    if len(ps_only) == 0:
        return pd.DataFrame()
    std_mean = (ps_only["phase_std_pre_window_load"] > 0).astype(object)
    std_mean[ps_only["phase_std_pre_window_load"].isna()] = np.nan
    ps_only["standardised_above_mean"] = std_mean

    agree = (
        ps_only["standardised_above_mean"] == ps_only["high_pre_window_p75"]
    ).astype(object)
    agree[
        ps_only["standardised_above_mean"].isna()
        | ps_only["high_pre_window_p75"].isna()
    ] = np.nan
    ps_only["operand_agree"] = agree
    return ps_only[[
        "episode_id", "D_end", "recovery_phase_end", "end_class",
        "crash_in_5d", "pre_window_load", "phase_std_pre_window_load",
        "standardised_above_mean", "high_pre_window_p75", "operand_agree",
    ]]


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

    episodes = build_episodes(df)
    print(f"[episodes] gap=0 heavy episodes: {len(episodes)}")

    # -- Section 3: per-phase pre_window_load baselines -------------------
    baselines_df, per_ep_baseline = compute_phase_baselines(df, episodes)
    baselines_df.to_csv(
        OUTPUT_DIR / "phase_pre_window_load_baselines.csv", index=False,
    )
    print(f"[section 3] phase baselines: {len(baselines_df)} rows")
    for _, r in baselines_df.iterrows():
        print(f"  {r['recovery_phase']}: n={int(r['n_episode_ends_in_phase'])} "
              f"mean={r['pre_window_load_mean']:.1f} "
              f"p75={r['pre_window_load_p75']:.1f} "
              f"std={r['pre_window_load_std']:.1f}")

    # -- Section 4: full 2024 distribution (all end-of-heavy-episodes) ----
    ps_2024 = build_ps_2024_frame(df, episodes, baselines_df, per_ep_baseline)
    ps_2024.to_csv(
        OUTPUT_DIR / "phase_std_pre_window_distribution_2024.csv", index=False,
    )
    print(f"[section 4] 2024 heavy-episode-ends: {len(ps_2024)} rows "
          f"(PS-True: {int(ps_2024['proactive_strategic'].sum())})")

    # -- 2024 PS-True subset for phase-standardised operand ---------------
    ps_2024_true = ps_2024[ps_2024["proactive_strategic"] == True].copy()
    ps_2024_true.to_csv(
        OUTPUT_DIR / "phase_std_pre_window_ps_true_2024.csv", index=False,
    )
    print(f"[section 4b] 2024 PS-True: {len(ps_2024_true)} rows "
          f"(crash-in-5d: {int(ps_2024_true['crash_in_5d'].sum())})")

    # -- Section 4c: ALL LC-era PS-True episodes with operand values ------
    all_years_ps_frames = []
    for y in [2022, 2023, 2024, 2025, 2026]:
        yf = build_ps_year_frame(df, episodes, baselines_df, per_ep_baseline, y)
        if len(yf) > 0:
            all_years_ps_frames.append(yf)
    all_ps = pd.concat(all_years_ps_frames, ignore_index=True) if all_years_ps_frames else pd.DataFrame()
    all_ps_true = all_ps[all_ps["proactive_strategic"] == True].copy() if len(all_ps) > 0 else pd.DataFrame()
    all_ps_true.to_csv(
        OUTPUT_DIR / "phase_std_pre_window_ps_true_all_years.csv", index=False,
    )
    print(f"[section 4c] LC-era PS-True: {len(all_ps_true)} rows")

    # -- Section 5: phase-stratified p75 thresholds -----------------------
    # Thresholds are per-phase p75 from baselines_df. Report + episode count above.
    thresh_rows = []
    for _, r in baselines_df.iterrows():
        phase = r["recovery_phase"]
        p75 = r["pre_window_load_p75"]
        n_above = int((per_ep_baseline["recovery_phase_end"] == phase).sum() and
                      ((per_ep_baseline["recovery_phase_end"] == phase) &
                       (per_ep_baseline["pre_window_load"] > p75)).sum())
        thresh_rows.append({
            "recovery_phase": phase,
            "p75_pre_window_load": p75,
            "n_episode_ends_in_phase": int(r["n_episode_ends_in_phase"]),
            "n_episodes_above_p75": n_above,
        })
    thresh_df = pd.DataFrame(thresh_rows)
    thresh_df.to_csv(
        OUTPUT_DIR / "phase_p75_pre_window_thresholds.csv", index=False,
    )
    print(f"[section 5] phase p75 thresholds: {len(thresh_df)} rows")

    # -- Section 5b: 2024 PS-True with phase-stratified high_pre_window_p75 --
    strat_2024_true = ps_2024_true[[
        "episode_id", "D_end", "recovery_phase_end", "end_class",
        "streak_length", "crash_in_5d", "pre_window_load",
        "phase_p75_pre_window_load", "high_pre_window_p75",
    ]].copy()
    strat_2024_true.to_csv(
        OUTPUT_DIR / "phase_stratified_high_pw_load_ps_true_2024.csv", index=False,
    )
    print(f"[section 5b] 2024 PS-True stratified: {len(strat_2024_true)} rows")

    # -- Section 6: cross-comparison of the two operands on 2024 PS-True --
    agreement_df = emit_operand_agreement(ps_2024)
    agreement_df.to_csv(
        OUTPUT_DIR / "phase_stratified_vs_standardised_2024_ps.csv", index=False,
    )
    print(f"[section 6] cross-operand agreement rows: {len(agreement_df)}")

    # -- Section 9: 2024 PS-True by end_class x standardised pre-window --
    def _attach_std_above_mean(frame):
        f = frame.copy()
        s = (f["phase_std_pre_window_load"] > 0).astype(object)
        s[f["phase_std_pre_window_load"].isna()] = np.nan
        f["standardised_above_mean"] = s
        return f

    end_class_rows = []
    for cls in ["heavy", "very_heavy"]:
        cls_sub = _attach_std_above_mean(
            ps_2024_true[ps_2024_true["end_class"] == cls]
        )
        row = emit_2x2(
            f"2024_PS_True_end_class_{cls}", cls_sub, "standardised_above_mean",
        )
        row["end_class"] = cls
        end_class_rows.append(row)
    # ALL row
    ps_2024_true_local = _attach_std_above_mean(ps_2024_true)
    row_all = emit_2x2(
        "2024_PS_True_end_class_ALL", ps_2024_true_local,
        "standardised_above_mean",
    )
    row_all["end_class"] = "ALL"
    end_class_rows.insert(0, row_all)
    end_class_df = pd.DataFrame(end_class_rows)
    end_class_df.to_csv(
        OUTPUT_DIR / "pre_window_by_end_class_2024_ps.csv", index=False,
    )
    print(f"[section 9] end-class stratification rows: {len(end_class_df)}")

    # -- Section 10: 2x2 contingency for phase-standardised on 2024 PS-True --
    sens_rows = [row_all]  # reuse standardised >0 row
    sens_df = pd.DataFrame(sens_rows)
    sens_df.to_csv(
        OUTPUT_DIR / "phase_std_pre_window_operand_sensitivity.csv", index=False,
    )
    print(f"[section 10] operand sensitivity 2x2 rows: {len(sens_df)}")

    # -- Section 11: neighbouring years 2023 + 2025 spot-check ------------
    neigh_rows = []
    for y in [2023, 2025]:
        yf = build_ps_year_frame(df, episodes, baselines_df, per_ep_baseline, y)
        if len(yf) == 0:
            continue
        yps = _attach_std_above_mean(
            yf[yf["proactive_strategic"] == True]
        )
        row = emit_2x2(
            f"year_{y}_PS_True_standardised_above_mean", yps,
            "standardised_above_mean",
        )
        row["year"] = y
        neigh_rows.append(row)
    neigh_df = pd.DataFrame(neigh_rows)
    neigh_df.to_csv(
        OUTPUT_DIR / "phase_std_pre_window_2023_2025_comparison.csv", index=False,
    )
    print(f"[section 11] neighbouring-year rows: {len(neigh_df)}")

    # -- Section 12: alternative cut-points on 2024 PS-True ---------------
    alt_df = emit_alternative_cutpoints(ps_2024, baselines_df, 2024)
    alt_df.to_csv(
        OUTPUT_DIR / "alternative_cutpoints_2024_ps.csv", index=False,
    )
    print(f"[section 12] alternative cut-points rows: {len(alt_df)}")

    print(f"\n[write] outputs in {OUTPUT_DIR}")
    for f in sorted(OUTPUT_DIR.glob("*.csv")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
