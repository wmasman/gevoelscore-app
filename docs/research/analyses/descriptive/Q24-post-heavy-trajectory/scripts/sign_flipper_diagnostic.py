"""
Q24 Wave 2 sign-flipper diagnostic — Stage D r3 close.

Investigates the 2 sign-flipper cells surfaced by the r2 audit §6.3 Class B:

    1) effective_exertion_min +3d compensatory_success
       raw AUC = +3.55 [+0.25, +7.17]; detrended AUC = -6.49 [-12.88, -0.47]

    2) spo2_avg_sleep +3d compensatory_failure
       raw AUC = +1.01 [+0.01, +2.03]; detrended AUC = -1.36 [-2.49, -0.19]

Hypothesis (per orchestrator brief):
    Raw signal and underlying drift are strongly co-varying. Test by fitting
    the same linear_detrend_on_pre trend on the outcome column over the 30d
    pre-window [D-30, D-1] for each episode-end AND for the matched-ordinary
    comparator days, and compare pre-episode slope distributions.

    If heavy-arm pre-episode slopes are systematically different from
    matched-ordinary pre-episode slopes, that IS the "raw signal and drift
    co-varying" mechanism the flip inherits from.

Method:
    - Reproduce the same pool construction as audit.py (strict-clean +
      compensatory-success/failure at +3d).
    - For each anchor in each pool + each matched-ordinary comparator:
        * Fit the linear pre-window trend (30d, min 15 valid points) via
          detrend.linear_detrend_on_pre_trajectory's underlying polyfit.
        * Extract the slope (units-per-day).
    - Report distribution stats (n, mean, median, std, IQR) and permutation
      test of slope-difference between heavy-arm and comparator-arm.
    - Also report the observed-outcome-value stats at k=1..3 (post-window
      means, raw + detrended).

Idempotent; RANDOM_SEED = 20260715. Output CSV is regenerable and gitignored
per project convention.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Reuse the audit's helpers to guarantee identical pool construction
sys.path.insert(0, str(Path(__file__).parent))
from audit import (  # noqa: E402
    build_matched_ordinary_pool,
    build_trigger_pools,
    identify_heavy_episode_ends,
    load_master,
)
from detrend import MIN_PRE_POINTS, PRE_WINDOW_DAYS  # noqa: E402

RANDOM_SEED = 20260715

OUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = OUT_DIR / "sign_flipper_diagnostic.csv"

# The two sign-flipper cells surfaced by r2 §6.3 Class B
SIGN_FLIPPERS = [
    # (outcome, pool_name, window)
    ("effective_exertion_min", "compensatory_success", 3),
    ("spo2_avg_sleep", "compensatory_failure", 3),
]

N_PERMUTATIONS = 10_000  # for slope-difference permutation test


def pre_window_slope(
    series: pd.Series,
    anchor_date: pd.Timestamp,
    pre_window_days: int = PRE_WINDOW_DAYS,
    min_pre_points: int = MIN_PRE_POINTS,
) -> float:
    """
    Fit y = a + b*t on the pre-window [D-pre_window_days, D-1] and return b.

    Mirrors detrend.linear_detrend_on_pre_trajectory's slope extraction. NaN
    if fewer than min_pre_points valid observations.
    """
    pre_start = anchor_date - pd.Timedelta(days=pre_window_days)
    pre_end = anchor_date - pd.Timedelta(days=1)
    pre = series.loc[pre_start:pre_end].dropna()
    if len(pre) < min_pre_points:
        return np.nan
    pre_x = np.array([(idx - anchor_date).days for idx in pre.index], dtype=float)
    slope, _intercept = np.polyfit(pre_x, pre.values, deg=1)
    return float(slope)


def summarise_distribution(values: np.ndarray, label: str) -> dict:
    """Return descriptive stats for a slope distribution."""
    valid = values[~np.isnan(values)]
    if len(valid) == 0:
        return {
            "label": label,
            "n": 0,
            "mean": np.nan,
            "median": np.nan,
            "std": np.nan,
            "q25": np.nan,
            "q75": np.nan,
            "min": np.nan,
            "max": np.nan,
        }
    return {
        "label": label,
        "n": int(len(valid)),
        "mean": float(np.mean(valid)),
        "median": float(np.median(valid)),
        "std": float(np.std(valid, ddof=1)) if len(valid) >= 2 else np.nan,
        "q25": float(np.percentile(valid, 25)),
        "q75": float(np.percentile(valid, 75)),
        "min": float(np.min(valid)),
        "max": float(np.max(valid)),
    }


def permutation_test_slope_diff(
    trigger_slopes: np.ndarray,
    comparator_slopes: np.ndarray,
    n_perm: int,
    rng: np.random.Generator,
) -> dict:
    """
    Two-sample permutation test on mean-slope difference (trigger - comparator).

    Returns dict with observed_diff and two-sided p-value.
    """
    t_valid = trigger_slopes[~np.isnan(trigger_slopes)]
    c_valid = comparator_slopes[~np.isnan(comparator_slopes)]
    if len(t_valid) < 2 or len(c_valid) < 2:
        return {"observed_diff": np.nan, "p_two_sided": np.nan}
    observed_diff = float(np.mean(t_valid) - np.mean(c_valid))
    combined = np.concatenate([t_valid, c_valid])
    n_t = len(t_valid)
    ge = 0
    for _ in range(n_perm):
        rng.shuffle(combined)
        perm_t = combined[:n_t]
        perm_c = combined[n_t:]
        perm_diff = np.mean(perm_t) - np.mean(perm_c)
        if abs(perm_diff) >= abs(observed_diff):
            ge += 1
    p = (ge + 1) / (n_perm + 1)
    return {"observed_diff": observed_diff, "p_two_sided": float(p)}


def diagnose_cell(
    df: pd.DataFrame,
    outcome_col: str,
    pool_name: str,
    window: int,
    trigger_anchors: list[pd.Timestamp],
    comparator_anchors: list[pd.Timestamp],
    rng: np.random.Generator,
) -> list[dict]:
    """
    Run the pre-window-slope diagnostic for one (outcome, pool, window) cell.

    Returns a list of summary rows suitable for CSV output.
    """
    series = df[outcome_col]

    trigger_slopes = np.array(
        [pre_window_slope(series, D) for D in trigger_anchors]
    )
    comparator_slopes = np.array(
        [pre_window_slope(series, D) for D in comparator_anchors]
    )

    trig_stats = summarise_distribution(trigger_slopes, "trigger_pre_slope")
    comp_stats = summarise_distribution(comparator_slopes, "comparator_pre_slope")

    perm = permutation_test_slope_diff(
        trigger_slopes, comparator_slopes, N_PERMUTATIONS, rng
    )

    base = {
        "outcome": outcome_col,
        "pool": pool_name,
        "window": window,
    }
    rows = []
    for stats in (trig_stats, comp_stats):
        row = {**base, **stats}
        rows.append(row)
    # Permutation-test summary row
    rows.append(
        {
            **base,
            "label": "permutation_slope_diff",
            "n": np.nan,
            "mean": perm["observed_diff"],
            "median": np.nan,
            "std": np.nan,
            "q25": np.nan,
            "q75": np.nan,
            "min": np.nan,
            "max": perm["p_two_sided"],  # abusing column: p in max slot
        }
    )
    return rows


def print_cell_report(
    outcome_col: str,
    pool_name: str,
    window: int,
    trigger_slopes: np.ndarray,
    comparator_slopes: np.ndarray,
    perm: dict,
) -> None:
    """Console read for orchestrator eyes."""
    trig_stats = summarise_distribution(trigger_slopes, "trigger_pre_slope")
    comp_stats = summarise_distribution(comparator_slopes, "comparator_pre_slope")
    print(f"\n=== {outcome_col} / {pool_name} / +{window}d ===")
    print(
        f"  trigger n={trig_stats['n']:>4}  mean={trig_stats['mean']:+.5f}  "
        f"median={trig_stats['median']:+.5f}  IQR=[{trig_stats['q25']:+.5f}, "
        f"{trig_stats['q75']:+.5f}]"
    )
    print(
        f"  compar. n={comp_stats['n']:>4}  mean={comp_stats['mean']:+.5f}  "
        f"median={comp_stats['median']:+.5f}  IQR=[{comp_stats['q25']:+.5f}, "
        f"{comp_stats['q75']:+.5f}]"
    )
    print(
        f"  observed slope-diff (trig - comp) = {perm['observed_diff']:+.5f}  "
        f"two-sided permutation p = {perm['p_two_sided']:.4f} "
        f"(B={N_PERMUTATIONS})"
    )


def main() -> None:
    print(f"[sign-flipper diagnostic] loading master CSV, RANDOM_SEED={RANDOM_SEED}")
    df = load_master()
    episode_ends = identify_heavy_episode_ends(df)
    print(f"[sign-flipper diagnostic] LC-era rows: {len(df)}, episode-ends: {len(episode_ends)}")

    all_rows: list[dict] = []
    rng = np.random.default_rng(RANDOM_SEED)

    for outcome_col, pool_name, window in SIGN_FLIPPERS:
        # Reproduce the r2 audit's pool split at this window
        succ, fail = build_trigger_pools(df, episode_ends, window)
        if pool_name == "compensatory_success":
            trigger_anchors = succ
        elif pool_name == "compensatory_failure":
            trigger_anchors = fail
        else:
            raise ValueError(f"Unknown pool: {pool_name}")
        comparator_anchors = build_matched_ordinary_pool(df, window, outcome_col)

        series = df[outcome_col]
        trigger_slopes = np.array(
            [pre_window_slope(series, D) for D in trigger_anchors]
        )
        comparator_slopes = np.array(
            [pre_window_slope(series, D) for D in comparator_anchors]
        )
        perm = permutation_test_slope_diff(
            trigger_slopes, comparator_slopes, N_PERMUTATIONS, rng
        )
        print_cell_report(
            outcome_col, pool_name, window, trigger_slopes, comparator_slopes, perm
        )

        cell_rows = diagnose_cell(
            df,
            outcome_col,
            pool_name,
            window,
            trigger_anchors,
            comparator_anchors,
            np.random.default_rng(RANDOM_SEED),  # fresh RNG per cell for determinism
        )
        all_rows.extend(cell_rows)

    out_df = pd.DataFrame(all_rows)
    out_df.to_csv(OUT_CSV, index=False)
    print(f"\n[sign-flipper diagnostic] wrote {OUT_CSV}")


if __name__ == "__main__":
    main()
