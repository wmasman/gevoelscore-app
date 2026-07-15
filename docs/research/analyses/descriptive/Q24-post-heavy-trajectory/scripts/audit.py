"""
Q24 post-heavy compensatory-rest trajectory descriptive audit — Stage D Wave 1.

Executes the operand definition locked at
`docs/research/methodology/post_heavy_day_compensatory_rest.md` (LOCKED r1
2026-07-15, commit 58b7723).

Wave 1 SCOPE (per orchestrator brief):
- Unit: episode-end (gap=0 contiguous) per Q24 MD §3.1
- Intensity trigger: COMBINED only (heavy ∪ very_heavy); intensity-stratified
  arms deferred to Wave 2
- Overlap policy: STRICT-CLEAN only per Q24 MD §5.2; inclusive deferred to
  Wave 2
- Windows: +3d, +5d, +10d (all three) per Q24 MD §5.1
- Pools per Q24 MD §3.5: compensatory-success (primary) AND
  compensatory-failure (sub-arm) — reported side-by-side
- Outcomes: ~20 per Q24 MD §6 (activity + sleep architecture +
  sleep autonomic + day autonomic + subjective; §6.2.3 sensitivity)
- 9 trajectory summary statistics per (outcome, window, pool, raw/detrended)
  per Q24 MD §7.1-§7.9
- Trajectory-detrend companion per Q24 MD §7.11 (linear_detrend_on_pre
  adapted from sister intervention_effects_descriptive.md)
- §8 decision-tree branch verdicts: 5 autonomic channels × 3 windows ×
  subjective screen. Peak-based decay per §8.1: |Δ(w)| / |Δ(k*)| < 0.5
- Comparator per §4.1: matched-ordinary = not heavy + no heavy in [D, D+w]
  + no crash in [D, D+w] + valid outcome across window;
  per-outcome pool recomputed per Q24 MD §4.2
- Bootstrap per Q24 MD §7.10: B=10,000, per-episode resampling,
  block length=1 (episode-ends independent under strict-clean),
  percentile-CI [2.5, 97.5]
- Multiplicity per Q24 MD §7.10: descriptive-only at Stage D; no correction

Producer-mode per CONVENTIONS §1.1 + §2.1 descriptive-before-inference.
Zero-vs-NaN discipline per Q24 MD §11: NEVER `.fillna(0)`; missing = missing.
Determinism: RANDOM_SEED fixed; bootstrap draws reproducible.

Idempotent: re-running produces byte-identical output CSVs.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

# Make sibling detrend.py importable
sys.path.insert(0, str(Path(__file__).parent))
from detrend import linear_detrend_on_pre_trajectory, raw_trajectory  # noqa: E402

# ---------------------------------------------------------------------------
# Constants (all pinned by Q24 MD)
# ---------------------------------------------------------------------------

RANDOM_SEED = 20260715  # per orchestrator brief; fixed for bootstrap reproducibility

DATA_PATH = Path(
    os.environ.get(
        "GEVOELSCORE_DATA_PATH",
        "C:/Users/Gebruiker/Documents/gevoelscore-data",
    )
)
MASTER_CSV = DATA_PATH / "unified" / "per_day_master.csv"

OUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Q24 MD §5.1 window ladder — Wave 1: all three windows
WINDOWS = [3, 5, 10]

# Q24 MD §7.10 bootstrap parameters
BOOTSTRAP_B = 10_000
BOOTSTRAP_CI_LO = 2.5
BOOTSTRAP_CI_HI = 97.5

# Q24 MD §8.1 peak-based decay threshold
DECAY_THRESHOLD = 0.5

# Q24 MD §6 outcome operand catalogue (Wave 1 scope; ~20 outcomes)
# Direction pre-commits per Q24 MD §7.7 (used only for below-baseline count
# direction; +1 = "above matched-ordinary is the physiologically-meaningful
# direction", -1 = "below matched-ordinary is the physiologically-meaningful
# direction"). Sign-inversion findings are themselves findings per §7.7.
OUTCOMES = [
    # (column, group, direction_sign, restricted_windows_or_None)
    # --- §6.1 activity ---
    ("total_steps", "activity", -1, None),
    ("effective_exertion_min", "activity", -1, None),
    ("vigorous_min", "activity", -1, None),
    ("active_min", "activity", -1, None),  # derived from active_sec/60
    # --- §6.2 sleep architecture ---
    ("sleep_duration_min", "sleep_architecture", +1, None),
    ("sleep_deep_min", "sleep_architecture", +1, None),
    ("sleep_light_min", "sleep_architecture", 0, None),
    # 0 = report but no signed direction pre-commit for light-sleep
    ("sleep_rem_min", "sleep_architecture", +1, None),  # REM-rebound reading
    ("sleep_awake_min", "sleep_architecture", +1, None),
    ("sleep_efficiency_tib", "sleep_architecture", -1, None),
    # --- §6.2 sleep autonomic (PRIMARY) ---
    ("stress_mean_sleep", "sleep_autonomic", +1, None),
    ("sleep_hr_avg_spo2", "sleep_autonomic", +1, None),  # from §6.2.3 sensitivity, but
    # per §8.1 it's one of the 5 primary autonomic channels
    # --- §6.2 day autonomic ---
    ("all_day_stress_avg", "day_autonomic", +1, None),
    ("bb_lowest", "day_autonomic", -1, None),
    ("hr_median_waking", "day_autonomic", +1, None),
    # --- §6.2.1 bb_overnight_gain at +3d ONLY ---
    ("bb_overnight_gain", "sleep_autonomic_sparse", -1, [3]),
    # --- §6.2.3 sensitivity ---
    ("sleep_efficiency_staged", "sensitivity", -1, None),
    ("bb_overnight_gain_frac", "sensitivity", -1, [3]),
    ("spo2_avg_sleep", "sensitivity", 0, None),
    ("asleep_stress_max_uds", "sensitivity", +1, None),
    # --- §6.3 subjective ---
    ("gevoelscore", "subjective", -1, None),
]

# Q24 MD §8.1 the 5 autonomic channels for the decision-tree per-channel screens
AUTONOMIC_CHANNELS = [
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
    "hr_median_waking",
    "sleep_hr_avg_spo2",
]
SUBJECTIVE_CHANNEL = "gevoelscore"


# ---------------------------------------------------------------------------
# Data loading + heavy-episode identification (Q24 MD §2, §3)
# ---------------------------------------------------------------------------


def load_master() -> pd.DataFrame:
    """Load per_day_master.csv, restrict to LC-era, derive active_min."""
    df = pd.read_csv(MASTER_CSV, parse_dates=["date"])
    lc = df[df["lc_phase"] == "lc"].copy()
    lc = lc.sort_values("date").reset_index(drop=True)
    # Derive active_min from active_sec (Q24 MD §6.1)
    if "active_sec" in lc.columns:
        lc["active_min"] = lc["active_sec"] / 60.0
    lc = lc.set_index("date")
    return lc


def identify_heavy_episode_ends(df: pd.DataFrame) -> pd.DatetimeIndex:
    """
    Identify episode-ends (gap=0 contiguous) per Q24 MD §3.1.

    A heavy day is a day where `exertion_class_lagged_lcera ∈ {heavy, very_heavy}`.
    An episode is a run of consecutive heavy days (gap=0 = no non-heavy days
    between). An episode-end is the last calendar day of that run.

    Missing `exertion_class_lagged_lcera` (~4.6% bootstrap/gap days) breaks
    contiguity; those days are treated as non-heavy for episode-boundary
    detection (Q24 MD §11 exertion_class_lagged_lcera missing-data policy).
    """
    heavy_mask = df["exertion_class_lagged_lcera"].isin(["heavy", "very_heavy"])
    # Sort by date and identify contiguous runs
    dates = df.index[heavy_mask].sort_values()
    if len(dates) == 0:
        return pd.DatetimeIndex([])

    episode_ends = []
    for i, d in enumerate(dates):
        # d is an episode-end if the next calendar day is not a heavy day.
        # This handles both the last heavy day in a run and single-day episodes.
        next_day = d + pd.Timedelta(days=1)
        if next_day not in dates:
            episode_ends.append(d)
    return pd.DatetimeIndex(episode_ends)


def has_crash_in_post_window(df: pd.DataFrame, D: pd.Timestamp, w: int) -> bool:
    """Return True if any crash day in [D+1, D+w]. Uses `is_crash` column."""
    start = D + pd.Timedelta(days=1)
    end = D + pd.Timedelta(days=w)
    slice_ = df.loc[start:end, "is_crash"]
    return bool(slice_.any())


def has_heavy_in_post_window(
    df: pd.DataFrame, D: pd.Timestamp, w: int, exclude_D: bool = True
) -> bool:
    """
    Return True if any heavy day in [D+1, D+w].

    Under strict-clean filter (Q24 MD §5.2), an episode-end at D that has any
    other heavy day in [+1, +w] is NOT strict-clean.
    """
    start = D + pd.Timedelta(days=1) if exclude_D else D
    end = D + pd.Timedelta(days=w)
    slice_ = df.loc[start:end, "exertion_class_lagged_lcera"]
    return bool(slice_.isin(["heavy", "very_heavy"]).any())


# ---------------------------------------------------------------------------
# Pool construction (Q24 MD §3.5 + §4.1)
# ---------------------------------------------------------------------------


def build_trigger_pools(
    df: pd.DataFrame, episode_ends: pd.DatetimeIndex, w: int
) -> tuple[list[pd.Timestamp], list[pd.Timestamp]]:
    """
    Build the two trigger pools at window w per Q24 MD §3.5:

    - compensatory-success (primary): strict-clean AND no crash in [+1, +w]
    - compensatory-failure (sub-arm): strict-clean AND crash in [+1, +w]

    Strict-clean per Q24 MD §5.2: no other heavy day in [+1, +w].

    Returns (success_pool, failure_pool) as lists of anchor dates.
    """
    success = []
    failure = []
    for D in episode_ends:
        if has_heavy_in_post_window(df, D, w, exclude_D=True):
            continue  # not strict-clean
        if has_crash_in_post_window(df, D, w):
            failure.append(D)
        else:
            success.append(D)
    return success, failure


def build_matched_ordinary_pool(
    df: pd.DataFrame, w: int, outcome_col: str
) -> list[pd.Timestamp]:
    """
    Build the per-outcome matched-ordinary comparator pool per Q24 MD §4.1.

    Conditions:
    1. D_ord is not a heavy day
    2. No heavy day in [D_ord, D_ord + w]  (Q24 MD §4.1 condition 2:
       symmetric with heavy-episode-end clean filter — includes D_ord itself
       for symmetry with 'the heavy day is heavy in its own [D, D+w] slice')
    3. No crash day in [D_ord, D_ord + w]
    4. Valid outcome data across the window (post d+1..d+w) for `outcome_col`

    Q24 MD §4.2: comparator pool recomputed per outcome.
    """
    dates = df.index
    heavy_mask = df["exertion_class_lagged_lcera"].isin(["heavy", "very_heavy"])
    crash_mask = df["is_crash"].astype(bool)

    candidates = []
    for D_ord in dates:
        # Condition 1: D_ord is not a heavy day
        if heavy_mask.loc[D_ord]:
            continue
        # Condition 2: no heavy in [D_ord, D_ord + w]
        end = D_ord + pd.Timedelta(days=w)
        slice_h = df.loc[D_ord:end, "exertion_class_lagged_lcera"]
        if slice_h.isin(["heavy", "very_heavy"]).any():
            continue
        # Condition 3: no crash in [D_ord, D_ord + w]
        slice_c = df.loc[D_ord:end, "is_crash"]
        if slice_c.astype(bool).any():
            continue
        # Condition 4: valid outcome data at every d+k, k=1..w
        outcome_vals = raw_trajectory(df[outcome_col], D_ord, w)
        if np.isnan(outcome_vals).any():
            continue
        candidates.append(D_ord)
    return candidates


# ---------------------------------------------------------------------------
# Trajectory extraction (Q24 MD §7)
# ---------------------------------------------------------------------------


def extract_trajectory_matrix(
    df: pd.DataFrame,
    anchors: list[pd.Timestamp],
    outcome_col: str,
    w: int,
    detrended: bool = False,
) -> np.ndarray:
    """
    Extract a (n_anchors, w) matrix of trajectory values.

    If detrended=True, applies the per-anchor linear_detrend_on_pre_trajectory
    per Q24 MD §7.11. Anchors with insufficient pre-window data will produce
    all-NaN rows for that outcome (dropped from detrended-arm summaries but
    counted separately).

    Missing observations at any d+k remain NaN (no fillna(0) per §11).
    """
    series = df[outcome_col]
    n = len(anchors)
    mat = np.full((n, w), np.nan)
    for i, D in enumerate(anchors):
        if detrended:
            mat[i, :] = linear_detrend_on_pre_trajectory(series, D, w)
        else:
            mat[i, :] = raw_trajectory(series, D, w)
    return mat


# ---------------------------------------------------------------------------
# Trajectory summary statistics (Q24 MD §7.1-§7.9)
# ---------------------------------------------------------------------------


def compute_per_day_mean_and_delta(
    trigger_mat: np.ndarray, comparator_mat: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Per Q24 MD §7.1-§7.2.

    Returns (mean_trigger_per_k, mean_comparator_per_k, delta_per_k)
    where delta = trigger - comparator (Q24 MD §7.2).

    Uses nanmean (missing observations at a given d+k excluded from that k's
    mean; per-arm-n reported separately).
    """
    with np.errstate(all="ignore"):
        mean_t = np.nanmean(trigger_mat, axis=0)
        mean_c = np.nanmean(comparator_mat, axis=0)
    delta = mean_t - mean_c
    return mean_t, mean_c, delta


def compute_scalar_summaries(delta: np.ndarray, direction_sign: int) -> dict:
    """
    Compute the scalar Q24 MD §7 statistics from a delta trajectory vector.

    Returns dict with keys:
        auc                 — §7.3 sum of delta over window
        slope               — §7.4 linear fit slope of delta on k
        peak_k              — §7.5 k where |delta(k)| is max
        peak_magnitude      — §7.5 |delta(k*)|
        rtbt                — §7.6 first k where delta crosses zero (from
                              non-zero start); censored at w+1 if no crossing
        below_baseline_days — §7.7 count of days below matched-ordinary
                              (or above, per direction_sign)
        variability         — §7.8 std(delta) across k
        first_crossing_day  — §7.9 first k where |delta| exceeds a CI-band;
                              here reported as first-k-where-nonzero-and-signed
                              (CI-band added separately in bootstrap loop)
    """
    if np.all(np.isnan(delta)):
        return {
            "auc": np.nan,
            "slope": np.nan,
            "peak_k": np.nan,
            "peak_magnitude": np.nan,
            "rtbt": np.nan,
            "below_baseline_days": np.nan,
            "variability": np.nan,
        }
    w = len(delta)
    # §7.3 AUC
    with np.errstate(all="ignore"):
        auc = np.nansum(delta)
    # §7.4 slope
    k_axis = np.arange(1, w + 1, dtype=float)
    valid = ~np.isnan(delta)
    if valid.sum() >= 2:
        slope = float(np.polyfit(k_axis[valid], delta[valid], deg=1)[0])
    else:
        slope = np.nan
    # §7.5 peak
    abs_delta = np.abs(delta)
    if np.all(np.isnan(abs_delta)):
        peak_k = np.nan
        peak_magnitude = np.nan
    else:
        peak_k = int(np.nanargmax(abs_delta)) + 1  # 1-based
        peak_magnitude = float(abs_delta[peak_k - 1])
    # §7.6 RTBT — first k where delta crosses matched-ordinary median (=0 in
    # delta space); censored at w+1 if never crosses
    rtbt = w + 1
    initial_sign = np.sign(delta[0]) if valid[0] else 0
    if initial_sign != 0:
        for i in range(1, w):
            if valid[i]:
                if np.sign(delta[i]) != initial_sign or delta[i] == 0:
                    rtbt = i + 1
                    break
    # §7.7 below-baseline day count (direction-signed)
    if direction_sign == -1:
        # "compensatory response" direction is negative
        below_count = int((delta < 0).sum())
    elif direction_sign == +1:
        # "cost of heavy load" direction is positive
        below_count = int((delta > 0).sum())
    else:
        # no direction pre-commit; report count-of-either as NaN-safe zero
        below_count = int((delta != 0).sum())
    # §7.8 variability
    with np.errstate(all="ignore"):
        variability = float(np.nanstd(delta, ddof=1)) if valid.sum() >= 2 else np.nan

    return {
        "auc": float(auc),
        "slope": float(slope),
        "peak_k": peak_k,
        "peak_magnitude": peak_magnitude,
        "rtbt": rtbt,
        "below_baseline_days": below_count,
        "variability": variability,
    }


# ---------------------------------------------------------------------------
# Bootstrap CIs (Q24 MD §7.10)
# ---------------------------------------------------------------------------


def _scalars_from_delta_vec(delta_boot: np.ndarray, direction_sign: int) -> dict:
    """Vectorised scalar summary stats over B bootstrap replicates.

    delta_boot has shape (B, w). Returns dict of arrays of shape (B,) for
    each summary stat.
    """
    B, w = delta_boot.shape
    valid_mask = ~np.isnan(delta_boot)

    with np.errstate(all="ignore"):
        auc = np.nansum(delta_boot, axis=1)

    # slope — need per-b polyfit; polyfit is not vectorised over multiple
    # y-arrays with NaN masks, so we fall back to a loop but keep it tight.
    k_axis = np.arange(1, w + 1, dtype=float)
    slope = np.full(B, np.nan)
    for b in range(B):
        v = valid_mask[b]
        if v.sum() >= 2:
            slope[b] = np.polyfit(k_axis[v], delta_boot[b, v], deg=1)[0]

    abs_delta = np.abs(delta_boot)
    with np.errstate(all="ignore"):
        # nanargmax raises on all-NaN rows; guard by replacing all-NaN rows first
        row_has_valid = valid_mask.any(axis=1)
        peak_k = np.full(B, np.nan)
        peak_mag = np.full(B, np.nan)
        if row_has_valid.any():
            filled = np.where(np.isnan(abs_delta), -np.inf, abs_delta)
            peak_idx = np.argmax(filled, axis=1)
            peak_k_full = peak_idx + 1
            peak_mag_full = np.take_along_axis(
                abs_delta, peak_idx[:, None], axis=1
            ).squeeze(axis=1)
            peak_k[row_has_valid] = peak_k_full[row_has_valid]
            peak_mag[row_has_valid] = peak_mag_full[row_has_valid]

    # RTBT — first k where sign flips from delta[0] sign
    rtbt = np.full(B, w + 1, dtype=float)
    first_col = delta_boot[:, 0]
    first_sign = np.sign(np.where(np.isnan(first_col), 0.0, first_col))
    for b in range(B):
        if first_sign[b] == 0:
            continue
        for i in range(1, w):
            if valid_mask[b, i]:
                if np.sign(delta_boot[b, i]) != first_sign[b] or delta_boot[b, i] == 0:
                    rtbt[b] = i + 1
                    break

    # below-baseline day count (direction-signed)
    if direction_sign == -1:
        below_count = (delta_boot < 0).sum(axis=1).astype(float)
    elif direction_sign == +1:
        below_count = (delta_boot > 0).sum(axis=1).astype(float)
    else:
        below_count = (delta_boot != 0).sum(axis=1).astype(float)

    with np.errstate(all="ignore"):
        variability = np.nanstd(delta_boot, axis=1, ddof=1)

    return {
        "auc": auc,
        "slope": slope,
        "peak_k": peak_k,
        "peak_magnitude": peak_mag,
        "rtbt": rtbt,
        "below_baseline_days": below_count,
        "variability": variability,
    }


def bootstrap_all(
    trigger_mat: np.ndarray,
    comparator_mat: np.ndarray,
    direction_sign: int,
    rng: np.random.Generator,
    B: int = BOOTSTRAP_B,
) -> tuple[dict, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Single bootstrap loop that returns both scalar-stat CIs and per-day CIs.

    Per Q24 MD §7.10: per-episode resampling, block length=1 (strict-clean
    episode-ends approximately independent), comparator-side likewise
    per-day resampled. B=10,000, percentile-CI [2.5, 97.5].

    Returns:
        cis_dict — {stat_name: (lo, hi)} for the 7 scalar summaries
        mean_t_lo, mean_t_hi — per-k trigger-mean CI
        delta_lo, delta_hi — per-k delta CI
    """
    n_t = trigger_mat.shape[0]
    n_c = comparator_mat.shape[0]
    w = trigger_mat.shape[1]
    ci_keys = [
        "auc",
        "slope",
        "peak_k",
        "peak_magnitude",
        "rtbt",
        "below_baseline_days",
        "variability",
    ]
    if n_t < 2 or n_c < 2:
        return (
            {k: (np.nan, np.nan) for k in ci_keys},
            np.full(w, np.nan),
            np.full(w, np.nan),
            np.full(w, np.nan),
            np.full(w, np.nan),
        )

    # Draw all resample indices at once
    t_idx_mat = rng.integers(0, n_t, size=(B, n_t))
    c_idx_mat = rng.integers(0, n_c, size=(B, n_c))

    mean_t_boot = np.empty((B, w))
    delta_boot = np.empty((B, w))
    with np.errstate(all="ignore"):
        for b in range(B):
            t_boot = trigger_mat[t_idx_mat[b]]
            c_boot = comparator_mat[c_idx_mat[b]]
            mt = np.nanmean(t_boot, axis=0)
            mc = np.nanmean(c_boot, axis=0)
            mean_t_boot[b, :] = mt
            delta_boot[b, :] = mt - mc

    # If EVERY resample yields all-NaN delta (i.e. no valid overlap between
    # trigger and comparator on this outcome), scalar summaries collapse to
    # constants (below-baseline count = 0 by construction on all-NaN, etc).
    # Detect that condition and emit NaN CIs to avoid misleading (0, 0).
    all_delta_nan = np.all(np.isnan(delta_boot), axis=1)
    all_nan_share = float(all_delta_nan.mean())
    scalars = _scalars_from_delta_vec(delta_boot, direction_sign)
    cis_dict = {}
    for key in ci_keys:
        arr = scalars[key]
        arr_clean = arr[~np.isnan(arr)]
        # If >95% of bootstrap replicates produce all-NaN delta (i.e. the
        # trigger arm has effectively no data on this outcome), emit NaN
        # rather than a degenerate CI on the below_baseline_days = 0 constant.
        if len(arr_clean) < 2 or all_nan_share > 0.95:
            cis_dict[key] = (np.nan, np.nan)
        else:
            lo = float(np.percentile(arr_clean, BOOTSTRAP_CI_LO))
            hi = float(np.percentile(arr_clean, BOOTSTRAP_CI_HI))
            cis_dict[key] = (lo, hi)

    with np.errstate(all="ignore"):
        mean_t_lo = np.nanpercentile(mean_t_boot, BOOTSTRAP_CI_LO, axis=0)
        mean_t_hi = np.nanpercentile(mean_t_boot, BOOTSTRAP_CI_HI, axis=0)
        delta_lo = np.nanpercentile(delta_boot, BOOTSTRAP_CI_LO, axis=0)
        delta_hi = np.nanpercentile(delta_boot, BOOTSTRAP_CI_HI, axis=0)

    return cis_dict, mean_t_lo, mean_t_hi, delta_lo, delta_hi


def compute_first_crossing_day(delta: np.ndarray, delta_lo: np.ndarray, delta_hi: np.ndarray) -> int:
    """
    Q24 MD §7.9: first d+k where delta falls outside the matched-ordinary
    arm's bootstrap 95% CI (equivalently: where the delta-CI itself excludes
    zero). Integer ∈ {1..w, w+1}; w+1 = censored (never diverges).
    """
    w = len(delta)
    for k in range(w):
        if not np.isnan(delta_lo[k]) and not np.isnan(delta_hi[k]):
            # CI excludes zero if lo > 0 or hi < 0
            if delta_lo[k] > 0 or delta_hi[k] < 0:
                return k + 1
    return w + 1


# ---------------------------------------------------------------------------
# Per-day valid n reporting (Q24 MD §11)
# ---------------------------------------------------------------------------


def compute_per_day_n_valid(mat: np.ndarray) -> np.ndarray:
    """Count non-NaN observations per k (per Q24 MD §11)."""
    return np.sum(~np.isnan(mat), axis=0)


# ---------------------------------------------------------------------------
# Main audit loop
# ---------------------------------------------------------------------------


def main():
    t0 = time.time()
    print(f"[Q24 Stage D Wave 1] loading {MASTER_CSV}...")
    df = load_master()
    print(f"[Q24 Stage D Wave 1] LC-era rows: {len(df)}")

    episode_ends = identify_heavy_episode_ends(df)
    print(f"[Q24 Stage D Wave 1] gap=0 episode-ends: {len(episode_ends)}")

    rng = np.random.default_rng(RANDOM_SEED)

    # --- Pool sample sizes (per window × pool) ---
    pool_rows = []
    pools_by_window: dict[int, tuple[list[pd.Timestamp], list[pd.Timestamp]]] = {}
    for w in WINDOWS:
        succ, fail = build_trigger_pools(df, episode_ends, w)
        pools_by_window[w] = (succ, fail)
        pool_rows.append(
            {
                "window": w,
                "pool": "compensatory_success",
                "n_episodes": len(succ),
            }
        )
        pool_rows.append(
            {
                "window": w,
                "pool": "compensatory_failure",
                "n_episodes": len(fail),
            }
        )
        print(
            f"[Q24 Stage D Wave 1] w=+{w}d  success={len(succ)}  failure={len(fail)}"
        )
    pd.DataFrame(pool_rows).to_csv(OUT_DIR / "compensatory_pool_sizes.csv", index=False)

    # --- Trajectory summaries + per-day trajectories ---
    summary_rows = []
    per_day_rows = []

    for outcome_col, group, direction_sign, restricted_windows in OUTCOMES:
        outcome_windows = restricted_windows if restricted_windows else WINDOWS
        for w in outcome_windows:
            succ_anchors, fail_anchors = pools_by_window[w]
            comp_anchors = build_matched_ordinary_pool(df, w, outcome_col)
            n_comp = len(comp_anchors)

            for pool_name, trigger_anchors in [
                ("compensatory_success", succ_anchors),
                ("compensatory_failure", fail_anchors),
            ]:
                n_trigger = len(trigger_anchors)

                for arm_type in ["raw", "detrended"]:
                    detrended = arm_type == "detrended"

                    # Extract trajectory matrices
                    trig_mat = extract_trajectory_matrix(
                        df, trigger_anchors, outcome_col, w, detrended=detrended
                    )
                    comp_mat = extract_trajectory_matrix(
                        df, comp_anchors, outcome_col, w, detrended=detrended
                    )

                    # Drop rows that are all-NaN (insufficient pre-window under
                    # detrended arm; comparator-side may also lose rows)
                    if detrended:
                        trig_valid = ~np.all(np.isnan(trig_mat), axis=1)
                        comp_valid = ~np.all(np.isnan(comp_mat), axis=1)
                        trig_mat = trig_mat[trig_valid]
                        comp_mat = comp_mat[comp_valid]
                        n_trig_eff = int(trig_valid.sum())
                        n_comp_eff = int(comp_valid.sum())
                    else:
                        n_trig_eff = n_trigger
                        n_comp_eff = n_comp

                    # Compute per-day means + delta
                    mean_t, mean_c, delta = compute_per_day_mean_and_delta(
                        trig_mat, comp_mat
                    )

                    # Compute scalar summaries
                    scalars = compute_scalar_summaries(delta, direction_sign)

                    # Bootstrap CIs (skipped if too few episodes to bootstrap)
                    if n_trig_eff >= 2 and n_comp_eff >= 2:
                        cis, mean_t_lo, mean_t_hi, delta_lo, delta_hi = bootstrap_all(
                            trig_mat, comp_mat, direction_sign, rng, B=BOOTSTRAP_B
                        )
                        first_crossing = compute_first_crossing_day(delta, delta_lo, delta_hi)
                    else:
                        cis = {
                            k: (np.nan, np.nan)
                            for k in [
                                "auc",
                                "slope",
                                "peak_k",
                                "peak_magnitude",
                                "rtbt",
                                "below_baseline_days",
                                "variability",
                            ]
                        }
                        w_arr = w
                        mean_t_lo = np.full(w_arr, np.nan)
                        mean_t_hi = np.full(w_arr, np.nan)
                        delta_lo = np.full(w_arr, np.nan)
                        delta_hi = np.full(w_arr, np.nan)
                        first_crossing = np.nan

                    n_valid_t = compute_per_day_n_valid(trig_mat)
                    n_valid_c = compute_per_day_n_valid(comp_mat)

                    # Emit summary row
                    row = {
                        "outcome": outcome_col,
                        "group": group,
                        "direction_sign": direction_sign,
                        "window": w,
                        "pool": pool_name,
                        "arm_type": arm_type,
                        "n_trigger_episodes": n_trig_eff,
                        "n_comparator_days": n_comp_eff,
                        "auc": scalars["auc"],
                        "auc_ci_lo": cis["auc"][0],
                        "auc_ci_hi": cis["auc"][1],
                        "slope": scalars["slope"],
                        "slope_ci_lo": cis["slope"][0],
                        "slope_ci_hi": cis["slope"][1],
                        "peak_k": scalars["peak_k"],
                        "peak_magnitude": scalars["peak_magnitude"],
                        "peak_magnitude_ci_lo": cis["peak_magnitude"][0],
                        "peak_magnitude_ci_hi": cis["peak_magnitude"][1],
                        "rtbt": scalars["rtbt"],
                        "rtbt_ci_lo": cis["rtbt"][0],
                        "rtbt_ci_hi": cis["rtbt"][1],
                        "below_baseline_days": scalars["below_baseline_days"],
                        "below_baseline_days_ci_lo": cis["below_baseline_days"][0],
                        "below_baseline_days_ci_hi": cis["below_baseline_days"][1],
                        "trajectory_variability": scalars["variability"],
                        "trajectory_variability_ci_lo": cis["variability"][0],
                        "trajectory_variability_ci_hi": cis["variability"][1],
                        "first_crossing_day": first_crossing,
                    }
                    summary_rows.append(row)

                    # Emit per-day rows
                    for k in range(w):
                        per_day_rows.append(
                            {
                                "outcome": outcome_col,
                                "group": group,
                                "window": w,
                                "pool": pool_name,
                                "arm_type": arm_type,
                                "day_k": k + 1,
                                "mean_trigger": (
                                    float(mean_t[k]) if not np.isnan(mean_t[k]) else np.nan
                                ),
                                "mean_comparator": (
                                    float(mean_c[k]) if not np.isnan(mean_c[k]) else np.nan
                                ),
                                "delta": (
                                    float(delta[k]) if not np.isnan(delta[k]) else np.nan
                                ),
                                "mean_trigger_ci_lo": (
                                    float(mean_t_lo[k])
                                    if not np.isnan(mean_t_lo[k])
                                    else np.nan
                                ),
                                "mean_trigger_ci_hi": (
                                    float(mean_t_hi[k])
                                    if not np.isnan(mean_t_hi[k])
                                    else np.nan
                                ),
                                "delta_ci_lo": (
                                    float(delta_lo[k])
                                    if not np.isnan(delta_lo[k])
                                    else np.nan
                                ),
                                "delta_ci_hi": (
                                    float(delta_hi[k])
                                    if not np.isnan(delta_hi[k])
                                    else np.nan
                                ),
                                "n_valid_trigger": int(n_valid_t[k]),
                                "n_valid_comparator": int(n_valid_c[k]),
                            }
                        )

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT_DIR / "trajectory_summary.csv", index=False)
    per_day_df = pd.DataFrame(per_day_rows)
    per_day_df.to_csv(OUT_DIR / "per_day_trajectories.csv", index=False)

    # --- §8 branch verdicts ---
    branch_rows = []
    # Subjective decay screen per channel per window per pool
    for w in WINDOWS:
        for pool_name in ["compensatory_success", "compensatory_failure"]:
            # Subjective (gevoelscore)
            subj_row = summary_df[
                (summary_df["outcome"] == SUBJECTIVE_CHANNEL)
                & (summary_df["window"] == w)
                & (summary_df["pool"] == pool_name)
                & (summary_df["arm_type"] == "raw")
            ]
            if len(subj_row) == 0:
                continue
            subj_peak = subj_row["peak_magnitude"].iloc[0]
            # Get per-day delta at k=w for subjective
            subj_per_day = per_day_df[
                (per_day_df["outcome"] == SUBJECTIVE_CHANNEL)
                & (per_day_df["window"] == w)
                & (per_day_df["pool"] == pool_name)
                & (per_day_df["arm_type"] == "raw")
                & (per_day_df["day_k"] == w)
            ]
            subj_delta_w = (
                float(abs(subj_per_day["delta"].iloc[0]))
                if len(subj_per_day) and not pd.isna(subj_per_day["delta"].iloc[0])
                else np.nan
            )
            if pd.isna(subj_peak) or subj_peak == 0 or pd.isna(subj_delta_w):
                subj_decays = None  # cannot decide
            else:
                subj_decays = (subj_delta_w / subj_peak) < DECAY_THRESHOLD

            for ch in AUTONOMIC_CHANNELS:
                ch_row = summary_df[
                    (summary_df["outcome"] == ch)
                    & (summary_df["window"] == w)
                    & (summary_df["pool"] == pool_name)
                    & (summary_df["arm_type"] == "raw")
                ]
                if len(ch_row) == 0:
                    continue
                ch_peak = ch_row["peak_magnitude"].iloc[0]
                ch_per_day = per_day_df[
                    (per_day_df["outcome"] == ch)
                    & (per_day_df["window"] == w)
                    & (per_day_df["pool"] == pool_name)
                    & (per_day_df["arm_type"] == "raw")
                    & (per_day_df["day_k"] == w)
                ]
                ch_delta_w = (
                    float(abs(ch_per_day["delta"].iloc[0]))
                    if len(ch_per_day) and not pd.isna(ch_per_day["delta"].iloc[0])
                    else np.nan
                )
                if pd.isna(ch_peak) or ch_peak == 0 or pd.isna(ch_delta_w):
                    ch_decays = None
                else:
                    ch_decays = (ch_delta_w / ch_peak) < DECAY_THRESHOLD

                # Branch classification per §8.2
                if ch_decays is None or subj_decays is None:
                    branch = "INDETERMINATE"
                elif ch_decays and subj_decays:
                    branch = "BOTH_decay"
                elif ch_decays and not subj_decays:
                    branch = "ONLY_autonomic_decays"
                elif not ch_decays and subj_decays:
                    branch = "ONLY_subjective_decays"
                else:
                    branch = "NEITHER_decays"
                branch_rows.append(
                    {
                        "autonomic_channel": ch,
                        "window": w,
                        "pool": pool_name,
                        "subjective_peak_magnitude": (
                            float(subj_peak) if not pd.isna(subj_peak) else np.nan
                        ),
                        "subjective_delta_at_w": subj_delta_w,
                        "subjective_decays": subj_decays,
                        "autonomic_peak_magnitude": (
                            float(ch_peak) if not pd.isna(ch_peak) else np.nan
                        ),
                        "autonomic_delta_at_w": ch_delta_w,
                        "autonomic_decays": ch_decays,
                        "branch": branch,
                    }
                )
    branch_df = pd.DataFrame(branch_rows)
    branch_df.to_csv(OUT_DIR / "branch_verdicts.csv", index=False)

    t1 = time.time()
    print(f"[Q24 Stage D Wave 1] wall-clock time: {t1 - t0:.1f}s")
    print(f"[Q24 Stage D Wave 1] outputs in {OUT_DIR}")


if __name__ == "__main__":
    main()
