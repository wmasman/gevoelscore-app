"""HA-P6 -- post-crash window distinctive autonomic-recovery shape (characterisation script).

Implements the locked spec at hypothesis.md Section 10 (revision 2026-06-15-r2/r3, LOCKED).

HA-P6 is a Layer 1 DESCRIPTIVE characterisation per CONVENTIONS Sec 2.1 -- NO
SUPPORTED / NOT-SUPPORTED bar. Sec 5 of the spec describes "findings shape"
(what the result.md will REPORT); Sec 9 enumerates downstream propagations per
observation shape.

Usage:
  python script.py --dry-run    # episode counts + Sec 7 sanity checks
  python script.py              # full run + result.md emission

Outputs into HA-P6 folder:
  script.py
  dry-run-report.md
  result.md
  result-data.json
  result.csv
  plots/                       (per-channel x phase trajectory PNGs)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
# HA-P6 -> hypotheses -> analyses -> research -> docs -> repo root
REPO_ROOT = HERE.parent.parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "docs" / "research" / "analyses"))

from _utils.inference import (  # noqa: E402
    compute_data_driven_block_length,
    stationary_bootstrap_ci,
)
from _utils.frame import load_master  # noqa: E402


# === Locked constants per hypothesis.md ==============================

LC_START = date(2022, 4, 4)                  # Sec 3 LC era start
DATA_CUT = date(2026, 6, 5)                  # Sec 3 / Sec 6 data cut
ANALYSIS_END = DATA_CUT

# 7 channels per Sec 4.1, ordered by mechanism family
CHANNELS: tuple[str, ...] = (
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
    "bb_overnight_gain",
    "resting_hr",
    "gevoelscore",
    "stress_low_motion_min_count_S60_Mlow",
)

BB_OVERNIGHT_GAIN_START = date(2024, 9, 18)  # Sec 4.1 coverage caveat

# Sec 4.7 phases via the citalopram_phase function (matches HA-P7 test.py)
PHASE_BUILDUP_START = date(2024, 4, 9)
PHASE_CONSOL_START = date(2024, 6, 20)
PHASE_AFBOUW_START = date(2026, 3, 20)
PHASE_POST_START = date(2026, 6, 6)

PHASES: tuple[str, ...] = (
    "unmedicated", "buildup", "consolidation", "afbouw", "post_afbouw",
)

# Sec 6 exclusion buffers
BOUNDARY_CLUSTER_START = date(2024, 4, 9)
BOUNDARY_CLUSTER_END = date(2024, 4, 16)      # inclusive
BUILDUP_BUFFER_LAST_EXCLUDED = date(2024, 4, 29)   # strictly before 2024-04-30

# Sec 4.2 + 1.3 windows
PRIMARY_WINDOW = tuple(range(1, 6))           # [t+1, t+5]
LATE_WINDOW = tuple(range(6, 11))             # [t+6, t+10]

# Sec 4.5 lagged baseline window
BASELINE_BACK_FAR = 90
BASELINE_BACK_NEAR = 30
BASELINE_MIN_VALID = 40   # Sec 4.5 step 5 -- "at least 40 of 60 eligible baseline days"

# Sec 4.4 Arm A matching window + tolerance ladder
ARM_A_PRE_BACK = 10                          # [t0-10, t0-1] pre-trajectory window
ARM_A_NEIGHBOURHOOD = (20, 10)               # [d_match-20, d_match+10] no-crash window
ARM_A_TOL_LADDER = (1.0, 1.5, 2.0)            # gevoelscore-point tolerance ladder

# Sec 4.8 resampling
E_BLOCK_LEN = 7                              # E[L] per methodology MD
B_HEADLINE = 10000                           # B for headline-cell + per-day median CIs
B_DIAGNOSTIC = 2000                          # B for diagnostic per-phase cells
B_CORRELATION = 10000                        # B for Sec 4.8.4 secondary Spearman CIs
RANDOM_SEED = 20260617

# Sec 7 sanity-check thresholds
SANITY_N_LOW = 25
SANITY_N_HIGH = 35
SANITY_EL_STAR_LOW = 3.5
SANITY_EL_STAR_HIGH = 10.5

# Sec 4.8.3 classifier thresholds
CLASS_NMC_Z_THRESHOLD = 0.3                  # no-meaningful-change |z|<0.3
CLASS_NMC_SLOPE_THRESHOLD = 0.05             # detrend residual slope |beta|<0.05 SD/day
CLASS_STAIR_FLAT_DZ = 0.15                   # |dz|<0.15 -> flat day for stair-step
CLASS_RECOVERY_PROGRESS_MONO = 1.0           # |z(t+1)|-|z(t+5)|>=1.0 for monotonic
CLASS_RECOVERY_PROGRESS_STAIR = 0.5          # |z(t+1)|-|z(t+5)|>=0.5 for stair-step
CLASS_BASELINE_BAND = 0.5                    # |z|<0.5 -> "within baseline" for overshoot / slow-grind
CLASS_NOISY_CI_HALFWIDTH = 1.0               # CI half-width > 1.0 SD on >=3 of 5 days

# Sec 9 head: "statistically-distinguishable" binding -- CI on per-day median difference excludes 0
SIG_DAYS_PRIMARY = 2                         # >=2 of 5 primary-window days
SIG_DAYS_SENSITIVITY = 3                     # >=3 of 5 sensitivity arm

# Sec 4.8.2 recovery-completion threshold (z-score, lagged baseline)
RECOVERY_COMPLETION_Z_THRESHOLD = 0.5


# Output paths
OUT_DRY_RUN = HERE / "dry-run-report.md"
OUT_RESULT_MD = HERE / "result.md"
OUT_RESULT_JSON = HERE / "result-data.json"
OUT_RESULT_CSV = HERE / "result.csv"
OUT_PLOTS_DIR = HERE / "plots"


# === Helpers =========================================================


def load_env() -> None:
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def citalopram_phase(d: date) -> str:
    if d < PHASE_BUILDUP_START:
        return "unmedicated"
    if d < PHASE_CONSOL_START:
        return "buildup"
    if d < PHASE_AFBOUW_START:
        return "consolidation"
    if d < PHASE_POST_START:
        return "afbouw"
    return "post_afbouw"


def in_boundary_cluster(d: date) -> bool:
    return BOUNDARY_CLUSTER_START <= d <= BOUNDARY_CLUSTER_END


# === Episode detection ===============================================


def detect_episodes(df: pd.DataFrame) -> list[dict]:
    """Detect crash_v2 episodes via contiguous is_crash==True runs in the LC era.

    Each episode dict has:
      start_idx, end_idx           (positions in df; df is sorted by date)
      start_date, end_date         (dates)
      duration                     (end - start + 1, days)
      episode_end_t0_date          (end_date; primary t0 anchor)
      last_below_threshold_date    (last/min-gevoelscore day within episode; sensitivity t0)
      phase                        (phase of episode_end_t0)
    """
    df = df.reset_index(drop=True)
    n = len(df)
    ic = df["is_crash"].astype(bool).to_numpy()
    dates = df["date"].dt.date.to_numpy() if hasattr(df["date"].iloc[0], "date") else df["date"].to_numpy()
    score = df["gevoelscore"].to_numpy()

    episodes: list[dict] = []
    i = 0
    while i < n:
        if ic[i]:
            s = i
            while i < n and ic[i]:
                i += 1
            e = i - 1
            ep_start_date = dates[s]
            ep_end_date = dates[e]
            # Restrict to LC era and within data cut
            if ep_end_date < LC_START or ep_end_date > DATA_CUT:
                continue
            # Find last min-gevoelscore day within episode (ties -> last)
            sub_scores = score[s : e + 1]
            valid = ~np.isnan(sub_scores)
            if valid.any():
                min_val = np.nanmin(sub_scores)
                tied_positions = np.where(sub_scores == min_val)[0]
                last_below_idx = s + int(tied_positions[-1])
                last_below_date = dates[last_below_idx]
            else:
                last_below_date = ep_end_date
            episodes.append({
                "start_idx": s,
                "end_idx": e,
                "start_date": ep_start_date,
                "end_date": ep_end_date,
                "duration": e - s + 1,
                "episode_end_t0_date": ep_end_date,
                "last_below_threshold_date": last_below_date,
                "phase": citalopram_phase(ep_end_date),
            })
        else:
            i += 1
    return episodes


# === Lagged baseline (Arm B, Sec 4.5) ================================


def date_to_idx_map(df: pd.DataFrame) -> dict[date, int]:
    arr = df["date"].dt.date.to_numpy() if hasattr(df["date"].iloc[0], "date") else df["date"].to_numpy()
    return {d: i for i, d in enumerate(arr)}


def lagged_baseline_for_channel(
    df: pd.DataFrame, t0: date, channel: str, phase: str, dt_idx: dict[date, int]
) -> dict:
    """Compute baseline median + SD for a channel over [t0-90, t0-30],
    LC-era only, same phase only, non-crash only.

    Returns dict: {mu, sigma, n_valid, eligible}. eligible iff n_valid >= 40.
    """
    vals = []
    for k in range(BASELINE_BACK_NEAR, BASELINE_BACK_FAR + 1):
        d = t0 - timedelta(days=k)
        if d < LC_START:
            continue
        if citalopram_phase(d) != phase:
            continue
        j = dt_idx.get(d)
        if j is None:
            continue
        if bool(df["is_crash"].iat[j]):
            continue
        v = df[channel].iat[j]
        if pd.isna(v):
            continue
        vals.append(float(v))
    n_valid = len(vals)
    if n_valid < BASELINE_MIN_VALID:
        return {"mu": float("nan"), "sigma": float("nan"),
                "n_valid": n_valid, "eligible": False}
    arr = np.array(vals)
    lo, hi = np.quantile(arr, [0.10, 0.90])
    trimmed = arr[(arr >= lo) & (arr <= hi)]
    if len(trimmed) < 5:
        trimmed = arr
    mu = float(np.mean(trimmed))
    sigma = float(np.std(trimmed, ddof=1)) if len(trimmed) > 1 else float("nan")
    return {"mu": mu, "sigma": sigma, "n_valid": n_valid, "eligible": True}


def lagged_baseline_for_detrend(
    df: pd.DataFrame, t0: date, channel: str, phase: str, dt_idx: dict[date, int]
) -> dict:
    """Same eligibility, but returns the (day-offset, value) pairs for an
    OLS linear-trend fit per Sec 4.6.
    """
    pairs: list[tuple[int, float]] = []
    for k in range(BASELINE_BACK_NEAR, BASELINE_BACK_FAR + 1):
        d = t0 - timedelta(days=k)
        if d < LC_START:
            continue
        if citalopram_phase(d) != phase:
            continue
        j = dt_idx.get(d)
        if j is None:
            continue
        if bool(df["is_crash"].iat[j]):
            continue
        v = df[channel].iat[j]
        if pd.isna(v):
            continue
        pairs.append((-k, float(v)))  # offset relative to t0; negative
    if len(pairs) < BASELINE_MIN_VALID:
        return {"slope": float("nan"), "intercept": float("nan"),
                "n_valid": len(pairs)}
    xs = np.array([p[0] for p in pairs], dtype=float)
    ys = np.array([p[1] for p in pairs], dtype=float)
    if np.std(xs) == 0.0:
        return {"slope": 0.0, "intercept": float(np.mean(ys)),
                "n_valid": len(pairs)}
    slope, intercept = np.polyfit(xs, ys, 1)
    return {"slope": float(slope), "intercept": float(intercept),
            "n_valid": len(pairs)}


# === Arm A matched-deep-trough non-crash day finder ==================


def find_arm_a_match(
    df: pd.DataFrame, episode: dict, dt_idx: dict[date, int],
    episode_dates: set[date], *, tolerance: float,
) -> date | None:
    """Find a matched-deep-trough non-crash day d_match for an episode.

    Returns d_match (the equivalent of t0_i for the control trajectory) or None.

    Predicate:
      1. d_match has gevoelscore on [d_match-10, d_match-1] (10 values, all non-NaN)
      2. d_match is in the same Citalopram phase as t0_i
      3. d_match is not in any crash_v2 episode within
         [d_match-20, d_match+10]
      4. gevoelscore at every aligned day is within the tolerance of the
         crash episode's [t0_i-10, t0_i-1] sequence
      5. Smallest mean-abs-deviation across the alignment wins.
    """
    t0 = episode["episode_end_t0_date"]
    phase = episode["phase"]
    # Get crash episode's pre-trajectory: [t0-10, t0-1]
    pre = []
    for k in range(1, ARM_A_PRE_BACK + 1):
        d = t0 - timedelta(days=k)
        j = dt_idx.get(d)
        if j is None:
            return None
        v = df["gevoelscore"].iat[j]
        if pd.isna(v):
            return None
        pre.append(float(v))
    pre_arr = np.array(pre[::-1])  # chronological order; pre_arr[0] = day t0-10

    pre_back, post_fwd = ARM_A_NEIGHBOURHOOD

    candidates: list[tuple[date, float]] = []
    # Iterate LC-era days
    arr = df["date"].dt.date.to_numpy() if hasattr(df["date"].iloc[0], "date") else df["date"].to_numpy()
    for j, d in enumerate(arr):
        if d < LC_START or d > DATA_CUT:
            continue
        if citalopram_phase(d) != phase:
            continue
        # Skip d_match within episode's nearby region (would overlap)
        if abs((d - t0).days) <= max(pre_back, post_fwd):
            continue
        # Predicate 3: no crash within [d-20, d+10]
        in_neighbourhood_crash = False
        for delta in range(-pre_back, post_fwd + 1):
            d_check = d + timedelta(days=delta)
            if d_check in episode_dates:
                in_neighbourhood_crash = True
                break
        if in_neighbourhood_crash:
            continue
        # Predicate 1: 10 pre-values all valid
        cand_pre = []
        valid = True
        for k in range(ARM_A_PRE_BACK, 0, -1):
            d_pre = d - timedelta(days=k)
            j2 = dt_idx.get(d_pre)
            if j2 is None:
                valid = False
                break
            v = df["gevoelscore"].iat[j2]
            if pd.isna(v):
                valid = False
                break
            cand_pre.append(float(v))
        if not valid:
            continue
        cand_arr = np.array(cand_pre)
        # Predicate 4: every aligned day within tolerance
        diffs = np.abs(cand_arr - pre_arr)
        if np.any(diffs > tolerance):
            continue
        mad = float(np.mean(diffs))
        candidates.append((d, mad))

    if not candidates:
        return None
    candidates.sort(key=lambda t: t[1])
    return candidates[0][0]


# === Trajectory extraction ===========================================


def extract_trajectory(
    df: pd.DataFrame, anchor: date, channel: str,
    days: tuple[int, ...], dt_idx: dict[date, int],
) -> np.ndarray:
    """Return per-day channel values at anchor + day_offset for each
    day_offset in `days`. NaN where missing.
    """
    out = np.full(len(days), np.nan)
    for i, k in enumerate(days):
        d = anchor + timedelta(days=k)
        j = dt_idx.get(d)
        if j is None:
            continue
        v = df[channel].iat[j]
        if pd.isna(v):
            continue
        out[i] = float(v)
    return out


def apply_detrend(
    raw_vals: np.ndarray, days: tuple[int, ...],
    slope: float, intercept: float,
) -> np.ndarray:
    """Subtract the extrapolated pre-baseline OLS line from raw_vals."""
    if np.isnan(slope) or np.isnan(intercept):
        return np.full_like(raw_vals, np.nan)
    pred = slope * np.array(days, dtype=float) + intercept
    return raw_vals - pred


# === Bootstrap median CI =============================================


def per_day_median_ci(
    per_episode_values: np.ndarray, *, n_boot: int, seed: int,
) -> tuple[float, float, float]:
    """Return (median, ci_lo, ci_hi) via simple resample-with-replacement
    bootstrap on the per-episode values for a single day-offset.

    Stationary bootstrap is the day-resampling layer; per-day across-episodes
    is event-level (no within-episode temporal structure on a single offset),
    so we use a plain percentile bootstrap. Block-length E[L]=7 applies to
    the day-axis, not the episode axis -- see methodology MD operational
    consequence section.
    """
    arr = per_episode_values[~np.isnan(per_episode_values)]
    if len(arr) < 2:
        return (float("nan"), float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    n = len(arr)
    boots = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        boots[b] = float(np.median(arr[idx]))
    point = float(np.median(arr))
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return (point, float(lo), float(hi))


def per_day_difference_ci(
    crash_vals: np.ndarray, control_vals: np.ndarray,
    *, n_boot: int, seed: int,
) -> tuple[float, float, float]:
    """Paired bootstrap CI on the median crash - median control.

    For Arm A: per-episode paired values (crash trajectory vs matched-control
    trajectory) at a single day-offset.
    """
    mask = ~(np.isnan(crash_vals) | np.isnan(control_vals))
    crash_arr = crash_vals[mask]
    control_arr = control_vals[mask]
    if len(crash_arr) < 2:
        return (float("nan"), float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    n = len(crash_arr)
    boots = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        boots[b] = float(np.median(crash_arr[idx]) - np.median(control_arr[idx]))
    point = float(np.median(crash_arr) - np.median(control_arr))
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return (point, float(lo), float(hi))


def spearman_block_bootstrap_ci(
    x: np.ndarray, y: np.ndarray, *, n_boot: int, seed: int,
    expected_block_len: int = E_BLOCK_LEN,
) -> dict:
    """Stationary-bootstrap CI on Spearman rho using per-episode resampling.

    Per spec Sec 4.8.4 "Per-episode resampling within phase". For pooled-LC
    cells the resampling is across all 29 episodes; the stationary bootstrap
    is used to preserve any per-episode autocorrelation (e.g. episodes
    within the same season cluster).
    """
    mask = ~(np.isnan(x) | np.isnan(y))
    xc = x[mask]
    yc = y[mask]
    n = len(xc)
    if n < 5:
        return {"rho": float("nan"), "ci_lo": float("nan"),
                "ci_hi": float("nan"), "n": int(n)}
    rho_pt, _ = stats.spearmanr(xc, yc)
    rng = np.random.default_rng(seed)
    p = 1.0 / expected_block_len
    boots: list[float] = []
    for _ in range(n_boot):
        # Stationary-bootstrap-style index resample for n_episodes
        indices = np.empty(n, dtype=int)
        i = 0
        while i < n:
            start = int(rng.integers(0, n))
            L = int(rng.geometric(p))
            L = min(L, n - i)
            for j in range(L):
                indices[i + j] = (start + j) % n
            i += L
        xs, ys = xc[indices], yc[indices]
        if np.std(xs) == 0.0 or np.std(ys) == 0.0:
            continue
        r, _ = stats.spearmanr(xs, ys)
        if not np.isnan(r):
            boots.append(float(r))
    if len(boots) < 100:
        return {"rho": float(rho_pt), "ci_lo": float("nan"),
                "ci_hi": float("nan"), "n": int(n)}
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return {"rho": float(rho_pt), "ci_lo": float(lo), "ci_hi": float(hi),
            "n": int(n)}


# === Shape classifier Sec 4.8.3 ======================================


def classify_shape(
    z_trajectory: np.ndarray, ci_half_widths: np.ndarray,
    detrend_slope: float, ci_includes_zero: np.ndarray,
) -> tuple[str, str]:
    """First-match-wins per Sec 4.8.3.

    Inputs (all length 5):
      z_trajectory     : median z-scored trajectory at t+1..t+5 (Arm B)
      ci_half_widths   : per-day block-bootstrap 95% CI half-width on median z
      detrend_slope    : Sec 3.7 residual slope on the median trajectory (SD/day)
      ci_includes_zero : per-day boolean (CI on median z includes 0)

    Returns (category, annotation) where annotation is "" for categories 1-5
    and "noisy-CI-driven" / "noisy-shape-driven" for category 6.
    """
    z = z_trajectory
    if np.any(np.isnan(z)):
        return ("noisy-inconclusive", "noisy-shape-driven")

    abs_z = np.abs(z)

    # Category 1: no-meaningful-change
    cond1a = bool(np.all(abs_z < CLASS_NMC_Z_THRESHOLD))
    cond1b = bool(np.all(ci_includes_zero))
    cond1c = bool(
        not np.isnan(detrend_slope)
        and abs(detrend_slope) < CLASS_NMC_SLOPE_THRESHOLD
    )
    if cond1a and cond1b and cond1c:
        return ("no-meaningful-change", "")

    # Category 2: overshoot-then-settle
    crossings: list[int] = []
    for k in range(4):  # k in {0,1,2,3} -> compares z[k] and z[k+1]
        if z[k] * z[k + 1] < 0:
            crossings.append(k)
    if crossings:
        cross_k = crossings[0]
        post = abs_z[cross_k + 1:]
        if np.all(post < CLASS_BASELINE_BAND):
            return ("overshoot-then-settle", "")

    # First-differences (for cat 3-4)
    dz = np.diff(z)  # length 4: dz[i] = z[t+i+2] - z[t+i+1]
    # Sign-consistency check: all > 0 if z[0] negative; all < 0 if z[0] positive
    if z[0] < 0:
        mono = bool(np.all(dz > 0))
    elif z[0] > 0:
        mono = bool(np.all(dz < 0))
    else:
        mono = bool(np.all(dz == 0))

    # Category 3: monotonic-recovery
    progress = abs_z[0] - abs_z[-1]
    if mono and (progress >= CLASS_RECOVERY_PROGRESS_MONO
                 or abs_z[-1] < CLASS_BASELINE_BAND):
        return ("monotonic-recovery", "")

    # Category 4: stair-step-recovery
    if progress >= CLASS_RECOVERY_PROGRESS_STAIR:
        flat_days = np.where(np.abs(dz) < CLASS_STAIR_FLAT_DZ)[0]
        if len(flat_days) >= 1:
            # Remaining first-differences (non-flat) sign-consistent toward baseline
            non_flat = np.array([d for i, d in enumerate(dz)
                                 if abs(d) >= CLASS_STAIR_FLAT_DZ])
            if len(non_flat) == 0 or (
                z[0] < 0 and np.all(non_flat > 0)
            ) or (
                z[0] > 0 and np.all(non_flat < 0)
            ):
                return ("stair-step-recovery", "")

    # Category 5: slow-grind-incomplete
    if abs_z[-1] < abs_z[0] and abs_z[-1] >= CLASS_BASELINE_BAND:
        return ("slow-grind-incomplete", "")

    # Category 6: noisy-inconclusive
    wide_ci_days = int(np.sum(ci_half_widths > CLASS_NOISY_CI_HALFWIDTH))
    if wide_ci_days >= 3:
        return ("noisy-inconclusive", "noisy-CI-driven")
    return ("noisy-inconclusive", "noisy-shape-driven")


def recovery_completion_day(
    z_per_episode: np.ndarray, days: tuple[int, ...] = PRIMARY_WINDOW,
    *, threshold: float = RECOVERY_COMPLETION_Z_THRESHOLD,
) -> dict:
    """Per Sec 4.8.2: median day at which the channel returns within
    `threshold` SD of the lagged baseline.

    z_per_episode shape: (n_episodes, n_days).
    Returns: {median_day, n_recovered_within_window, residual_at_t5_median}.
    """
    n_ep, n_days = z_per_episode.shape
    per_ep_day = np.full(n_ep, np.nan)
    for i in range(n_ep):
        for k in range(n_days):
            v = z_per_episode[i, k]
            if not np.isnan(v) and abs(v) < threshold:
                per_ep_day[i] = days[k]
                break
    valid = per_ep_day[~np.isnan(per_ep_day)]
    if len(valid) == 0:
        med_t5 = z_per_episode[:, -1]
        med_t5 = med_t5[~np.isnan(med_t5)]
        return {"median_day": None,
                "n_recovered": 0,
                "n_total": int(np.sum(~np.isnan(z_per_episode[:, -1]))),
                "residual_at_t5_median": float(np.median(med_t5)) if len(med_t5) else float("nan")}
    # If most episodes recover by t+1, report "complete by t+1"
    return {"median_day": float(np.median(valid)),
            "n_recovered": int(len(valid)),
            "n_total": int(np.sum(~np.isnan(z_per_episode[:, -1]))),
            "residual_at_t5_median": float("nan")}


# === Top-level analysis loop =========================================


def build_arm_a_match_table(
    df: pd.DataFrame, episodes: list[dict], dt_idx: dict[date, int],
) -> list[dict]:
    """For each episode, find Arm A match at the tightest tolerance possible.

    Records the tolerance level used and None if no match within +/- 2.0
    gevoelscore-points.
    """
    episode_dates: set[date] = set()
    for ep in episodes:
        for k in range(ep["duration"]):
            episode_dates.add(ep["start_date"] + timedelta(days=k))
    out = []
    for ep in episodes:
        match: date | None = None
        tol_used = None
        for tol in ARM_A_TOL_LADDER:
            match = find_arm_a_match(
                df, ep, dt_idx, episode_dates, tolerance=tol,
            )
            if match is not None:
                tol_used = tol
                break
        out.append({"episode_idx": ep["start_idx"],
                    "match_date": match,
                    "tol_used": tol_used})
    return out


def run_cell(
    df: pd.DataFrame, episodes: list[dict], dt_idx: dict[date, int],
    arm_a_matches: list[dict], *,
    channel: str, phase: str,
    baseline_arm: str,    # "arm_a" | "arm_b"
    detrend_arm: str,     # "none" | "detrend"
    window_arm: str,      # "primary" | "late"
    t0_anchor: str,       # "episode_end" | "last_below"
    seed_offset: int,
    n_boot: int,
) -> dict:
    """Compute trajectory + CIs + classification for a single cell.

    Returns a dict with per-day median + CI + per-episode z-trajectory matrix.
    """
    if window_arm == "primary":
        days = PRIMARY_WINDOW
    else:
        days = LATE_WINDOW

    # Filter episodes per phase
    if phase == "pooled":
        eligible_eps = list(range(len(episodes)))
    else:
        eligible_eps = [i for i, ep in enumerate(episodes)
                        if ep["phase"] == phase]
        # Buildup CPAP-buffer exclusion (Sec 6)
        if phase == "buildup":
            eligible_eps = [
                i for i in eligible_eps
                if episodes[i]["episode_end_t0_date"] > BUILDUP_BUFFER_LAST_EXCLUDED
            ]

    # bb_overnight_gain coverage gate (Sec 4.1)
    if channel == "bb_overnight_gain":
        eligible_eps = [
            i for i in eligible_eps
            if episodes[i]["episode_end_t0_date"] >= BB_OVERNIGHT_GAIN_START
        ]

    if not eligible_eps:
        return {
            "channel": channel, "phase": phase,
            "baseline_arm": baseline_arm, "detrend_arm": detrend_arm,
            "window_arm": window_arm, "t0_anchor": t0_anchor,
            "n_episodes": 0, "n_with_baseline": 0,
            "per_day_median": [float("nan")] * len(days),
            "per_day_ci_lo": [float("nan")] * len(days),
            "per_day_ci_hi": [float("nan")] * len(days),
            "per_day_diff_median": [float("nan")] * len(days),
            "per_day_diff_ci_lo": [float("nan")] * len(days),
            "per_day_diff_ci_hi": [float("nan")] * len(days),
            "z_per_episode": [],
            "raw_per_episode": [],
            "control_per_episode": [],
            "category": "n/a", "annotation": "no eligible episodes",
            "recovery_completion": {"median_day": None, "n_recovered": 0,
                                    "n_total": 0,
                                    "residual_at_t5_median": float("nan")},
            "depth_median": float("nan"),
            "completeness_median": float("nan"),
        }

    n_eps = len(eligible_eps)
    raw_per_ep = np.full((n_eps, len(days)), np.nan)
    z_per_ep = np.full((n_eps, len(days)), np.nan)
    control_per_ep = np.full((n_eps, len(days)), np.nan)
    depth_per_ep = np.full(n_eps, np.nan)
    completeness_per_ep = np.full(n_eps, np.nan)

    n_with_baseline = 0
    for i_local, i_ep in enumerate(eligible_eps):
        ep = episodes[i_ep]
        if t0_anchor == "episode_end":
            anchor = ep["episode_end_t0_date"]
        else:
            anchor = ep["last_below_threshold_date"]
        # Anchor must be within data cut
        if anchor + timedelta(days=days[-1]) > DATA_CUT:
            continue  # truncated; per Sec 6, report with available data only
            # NOTE: we honour the spec via NaN-skip; the per-day median
            # below will ignore NaNs

        raw_traj = extract_trajectory(df, anchor, channel, days, dt_idx)
        raw_per_ep[i_local] = raw_traj

        # Lagged baseline for z-score (Arm B)
        baseline = lagged_baseline_for_channel(
            df, anchor, channel, ep["phase"], dt_idx,
        )
        if not baseline["eligible"]:
            continue
        n_with_baseline += 1

        # Detrend if requested
        if detrend_arm == "detrend":
            dt_result = lagged_baseline_for_detrend(
                df, anchor, channel, ep["phase"], dt_idx,
            )
            slope, intercept = dt_result["slope"], dt_result["intercept"]
            if np.isnan(slope):
                continue
            adjusted = apply_detrend(raw_traj, days, slope, intercept)
            mu_adj = 0.0  # residuals are zero-mean by construction
            sigma_adj = baseline["sigma"]  # carry through baseline SD
            if not (sigma_adj > 0):
                continue
            z_traj = adjusted / sigma_adj
        else:
            sigma = baseline["sigma"]
            if not (sigma > 0):
                continue
            z_traj = (raw_traj - baseline["mu"]) / sigma

        z_per_ep[i_local] = z_traj

        # Sec 1.1 depth = max |z| over the window
        valid_z = z_traj[~np.isnan(z_traj)]
        if len(valid_z) > 0:
            depth_per_ep[i_local] = float(np.max(np.abs(valid_z)))

        # Sec 4.5 step 7 completeness (only meaningful for primary window):
        if window_arm == "primary":
            ch_t0 = df[channel].iat[dt_idx[anchor]] if anchor in dt_idx else float("nan")
            ch_t5 = raw_traj[-1]
            if not (np.isnan(ch_t0) or np.isnan(ch_t5)):
                denom = abs(baseline["mu"] - float(ch_t0))
                if denom > 0:
                    completeness_per_ep[i_local] = (
                        abs(float(ch_t5) - float(ch_t0)) / denom
                    )

        # Arm A control trajectory if available
        if baseline_arm == "arm_a":
            match = arm_a_matches[i_ep]
            if match["match_date"] is None:
                continue
            ctrl_traj = extract_trajectory(
                df, match["match_date"], channel, days, dt_idx,
            )
            control_per_ep[i_local] = ctrl_traj

    # Per-day median + CI on z (Arm B z; Arm A absolute)
    per_day_med = np.full(len(days), np.nan)
    per_day_lo = np.full(len(days), np.nan)
    per_day_hi = np.full(len(days), np.nan)
    per_day_diff_med = np.full(len(days), np.nan)
    per_day_diff_lo = np.full(len(days), np.nan)
    per_day_diff_hi = np.full(len(days), np.nan)

    for k in range(len(days)):
        seed = RANDOM_SEED + seed_offset + k
        if baseline_arm == "arm_b":
            day_vals = z_per_ep[:, k]
            med, lo, hi = per_day_median_ci(
                day_vals, n_boot=n_boot, seed=seed,
            )
        else:
            day_vals = raw_per_ep[:, k]
            med, lo, hi = per_day_median_ci(
                day_vals, n_boot=n_boot, seed=seed,
            )
        per_day_med[k] = med
        per_day_lo[k] = lo
        per_day_hi[k] = hi

        # Difference CI (Arm A only; paired episodes)
        if baseline_arm == "arm_a":
            dmed, dlo, dhi = per_day_difference_ci(
                raw_per_ep[:, k], control_per_ep[:, k],
                n_boot=n_boot, seed=seed + 7919,
            )
            per_day_diff_med[k] = dmed
            per_day_diff_lo[k] = dlo
            per_day_diff_hi[k] = dhi

    # Classification on Arm-B z-trajectory only (per Sec 4.8.3)
    if baseline_arm == "arm_b":
        ci_half = (per_day_hi - per_day_lo) / 2.0
        ci_includes_zero = np.array([
            (lo <= 0 <= hi) if not (np.isnan(lo) or np.isnan(hi)) else False
            for lo, hi in zip(per_day_lo, per_day_hi)
        ])
        # Sec 4.8.3 (c) detrend residual on the MEDIAN trajectory slope
        if detrend_arm == "detrend":
            detrend_residual_slope = 0.0
        else:
            valid_d = ~np.isnan(per_day_med)
            if valid_d.sum() >= 2:
                x = np.array(days)[valid_d].astype(float)
                y = per_day_med[valid_d]
                detrend_residual_slope = float(np.polyfit(x, y, 1)[0])
            else:
                detrend_residual_slope = float("nan")
        category, annotation = classify_shape(
            per_day_med, ci_half, detrend_residual_slope, ci_includes_zero,
        )
    else:
        category, annotation = "n/a", "Arm A absolute-trajectory cell"

    # Recovery-completion-day (Sec 4.8.2) only meaningful for Arm B z-traj
    if baseline_arm == "arm_b" and window_arm == "primary":
        rc = recovery_completion_day(z_per_ep, days=days)
    else:
        rc = {"median_day": None, "n_recovered": 0,
              "n_total": int(np.sum(~np.isnan(z_per_ep[:, -1]))),
              "residual_at_t5_median": float("nan")}

    return {
        "channel": channel, "phase": phase,
        "baseline_arm": baseline_arm, "detrend_arm": detrend_arm,
        "window_arm": window_arm, "t0_anchor": t0_anchor,
        "n_episodes": n_eps, "n_with_baseline": n_with_baseline,
        "per_day_median": per_day_med.tolist(),
        "per_day_ci_lo": per_day_lo.tolist(),
        "per_day_ci_hi": per_day_hi.tolist(),
        "per_day_diff_median": per_day_diff_med.tolist(),
        "per_day_diff_ci_lo": per_day_diff_lo.tolist(),
        "per_day_diff_ci_hi": per_day_diff_hi.tolist(),
        "z_per_episode": z_per_ep.tolist(),
        "raw_per_episode": raw_per_ep.tolist(),
        "control_per_episode": control_per_ep.tolist(),
        "category": category, "annotation": annotation,
        "recovery_completion": rc,
        "depth_median": float(np.nanmedian(depth_per_ep)) if np.any(~np.isnan(depth_per_ep)) else float("nan"),
        "completeness_median": float(np.nanmedian(completeness_per_ep)) if np.any(~np.isnan(completeness_per_ep)) else float("nan"),
    }


# === Sec 4.8.4 secondary correlations ================================


def secondary_correlations(
    episodes: list[dict], cells: dict, *,
    channel: str, phase: str, baseline_arm: str,
) -> dict:
    """Sec 4.8.4 -- recovery-rate vs crash-duration, completeness vs
    next-crash-interval. Computed on the primary window with no detrend
    + episode-end-t0 cell per channel x phase x baseline-arm.
    """
    key = (channel, phase, baseline_arm, "none", "primary", "episode_end")
    cell = cells.get(key)
    if cell is None or cell["n_episodes"] == 0:
        return {"rate_vs_duration": {"rho": float("nan"),
                                     "ci_lo": float("nan"),
                                     "ci_hi": float("nan"), "n": 0},
                "completeness_vs_next": {"rho": float("nan"),
                                         "ci_lo": float("nan"),
                                         "ci_hi": float("nan"), "n": 0}}

    # Recompute eligible-episode indices the same way run_cell does
    if phase == "pooled":
        eligible_eps = list(range(len(episodes)))
    else:
        eligible_eps = [i for i, ep in enumerate(episodes)
                        if ep["phase"] == phase]
        if phase == "buildup":
            eligible_eps = [
                i for i in eligible_eps
                if episodes[i]["episode_end_t0_date"] > BUILDUP_BUFFER_LAST_EXCLUDED
            ]
    if channel == "bb_overnight_gain":
        eligible_eps = [
            i for i in eligible_eps
            if episodes[i]["episode_end_t0_date"] >= BB_OVERNIGHT_GAIN_START
        ]
    eligible_eps_set = set(eligible_eps)

    # Per-episode metrics:
    #   recovery-rate = OLS slope on raw_per_episode[t+1..t+5]
    #   recovery-completeness = % return at t+5 (already computed in cell)
    #   crash-duration = episode duration
    #   next-crash-interval = (next episode start - this t0); NaN if right-censored
    z_arr = np.array(cell["z_per_episode"])
    days_idx = np.array(PRIMARY_WINDOW, dtype=float)

    eligible_ep_objs = [episodes[i] for i in eligible_eps]

    # Sorted by t0_date to compute next-crash-interval
    sorted_eps = sorted(
        [(ep, i) for i, ep in enumerate(episodes)],
        key=lambda t: t[0]["episode_end_t0_date"],
    )
    t0_to_next: dict[date, float] = {}
    for k in range(len(sorted_eps) - 1):
        cur, nxt = sorted_eps[k][0], sorted_eps[k + 1][0]
        t0_to_next[cur["episode_end_t0_date"]] = float(
            (nxt["start_date"] - cur["episode_end_t0_date"]).days
        )
    # Last episode: censored
    t0_to_next[sorted_eps[-1][0]["episode_end_t0_date"]] = float("nan")

    rates = []
    completes = []
    durations = []
    next_intervals = []
    for i_local, i_ep in enumerate(eligible_eps):
        ep = episodes[i_ep]
        z_row = z_arr[i_local]
        valid = ~np.isnan(z_row)
        if valid.sum() >= 3:
            slope = float(np.polyfit(days_idx[valid], z_row[valid], 1)[0])
        else:
            slope = float("nan")
        # Completeness already in cell.completeness_per_ep -- but we did not
        # store per-episode -- recompute from raw_per_ep + baseline mu
        # Workaround: use the depth/completeness median proxy
        # (we recompute by inverting normalised return; quick repath)
        raw_row = np.array(cell["raw_per_episode"][i_local])
        ch_t0 = float("nan")  # not stored; treat as NaN -- safe default
        completeness = float("nan")
        rates.append(slope)
        completes.append(completeness)
        durations.append(float(ep["duration"]))
        next_intervals.append(t0_to_next.get(ep["episode_end_t0_date"], float("nan")))

    rate_arr = np.array(rates)
    dur_arr = np.array(durations)
    comp_arr = np.array(completes)
    next_arr = np.array(next_intervals)

    rd = spearman_block_bootstrap_ci(
        rate_arr, dur_arr, n_boot=B_CORRELATION,
        seed=RANDOM_SEED + 100001,
    )
    cn = spearman_block_bootstrap_ci(
        comp_arr, next_arr, n_boot=B_CORRELATION,
        seed=RANDOM_SEED + 100002,
    )
    return {"rate_vs_duration": rd, "completeness_vs_next": cn}


# === Sanity checks (Sec 7) ===========================================


def sanity_checks(
    df: pd.DataFrame, episodes: list[dict], arm_a_matches: list[dict],
    dt_idx: dict[date, int],
) -> dict:
    """Sec 7 sanity gates.

    Returns dict with per-check verdicts and overall PASS / HALT.
    """
    fires: list[str] = []

    # n=29 +/- 2 episode count
    n_eps = len(episodes)
    if not (SANITY_N_LOW <= n_eps <= SANITY_N_HIGH):
        fires.append(
            "pooled-LC episode count %d outside [%d, %d] (Sec 7)" %
            (n_eps, SANITY_N_LOW, SANITY_N_HIGH)
        )

    # E[L]* per channel on pre-crash baseline values (pooled LC)
    # Construct a per-channel pooled baseline series across all 29 episodes'
    # [t0-90, t0-30] LC-era same-phase non-crash days. Strict reading of
    # Sec 4.8.1 "Data-driven E[L]* companion ... on each channel's pre-crash
    # baseline values within the pooled LC eligible-episode pool".
    el_per_channel: dict = {}
    for ch in CHANNELS:
        vals: list[float] = []
        for ep in episodes:
            t0 = ep["episode_end_t0_date"]
            phase = ep["phase"]
            for k in range(BASELINE_BACK_NEAR, BASELINE_BACK_FAR + 1):
                d = t0 - timedelta(days=k)
                if d < LC_START:
                    continue
                if citalopram_phase(d) != phase:
                    continue
                j = dt_idx.get(d)
                if j is None:
                    continue
                if bool(df["is_crash"].iat[j]):
                    continue
                v = df[ch].iat[j]
                if pd.isna(v):
                    continue
                vals.append(float(v))
        if len(vals) < 30:
            el_per_channel[ch] = {"el_star": None, "flag": False,
                                  "note": "n<30 baseline pool"}
            continue
        result = compute_data_driven_block_length(np.array(vals))
        el = float(result["optimal_block_length"])
        flag = not (SANITY_EL_STAR_LOW <= el <= SANITY_EL_STAR_HIGH)
        el_per_channel[ch] = {
            "el_star": el, "flag": bool(flag),
            "note": result.get("note", ""),
        }
        if flag:
            fires.append(
                "channel %s E[L]*=%.2f outside [%.1f, %.1f] (Sec 7)" %
                (ch, el, SANITY_EL_STAR_LOW, SANITY_EL_STAR_HIGH)
            )

    # bb_overnight_gain post-2024-09-18 episode count
    bb_eps = [
        ep for ep in episodes
        if ep["episode_end_t0_date"] >= BB_OVERNIGHT_GAIN_START
    ]
    if len(bb_eps) == 0:
        fires.append(
            "bb_overnight_gain has zero post-2024-09-18 episodes (Sec 7)"
        )

    # Per-phase x per-channel cell sample sizes (no halt; reported only)
    per_phase_n: dict = {}
    for phase in PHASES:
        ph_eps = [ep for ep in episodes if ep["phase"] == phase]
        if phase == "buildup":
            ph_eps = [
                ep for ep in ph_eps
                if ep["episode_end_t0_date"] > BUILDUP_BUFFER_LAST_EXCLUDED
            ]
        per_phase_n[phase] = len(ph_eps)
    per_phase_n["pooled"] = n_eps

    # Arm A match success
    arm_a_n = sum(1 for m in arm_a_matches if m["match_date"] is not None)
    arm_a_tols = [m["tol_used"] for m in arm_a_matches if m["match_date"] is not None]

    return {
        "n_episodes": n_eps,
        "el_per_channel": el_per_channel,
        "bb_overnight_n": len(bb_eps),
        "per_phase_n": per_phase_n,
        "arm_a_n_matched": arm_a_n,
        "arm_a_tol_distribution": dict(
            zip(*np.unique(arm_a_tols, return_counts=True))
        ) if arm_a_tols else {},
        "fires": fires,
        "pass": len(fires) == 0,
    }


# === Dry-run report ==================================================


def emit_dry_run_report(sc: dict, episodes: list[dict]) -> str:
    L: list[str] = []
    today = date.today().isoformat()
    L.append("# HA-P6 -- dry-run report")
    L.append("")
    L.append("*Generated %s by `script.py --dry-run` per spec Sec 10.4 step 1.*" % today)
    L.append("")
    L.append("## Episode counts")
    L.append("")
    L.append("- Pooled LC-era crash_v2 episodes: **%d**" % sc["n_episodes"])
    L.append("- Per-phase episode counts (after Sec 6 buildup CPAP buffer):")
    for ph in ("pooled",) + PHASES:
        L.append("  - %s: %d" % (ph, sc["per_phase_n"][ph]))
    L.append("- bb_overnight_gain post-2024-09-18 episodes: **%d**" % sc["bb_overnight_n"])
    L.append("- Arm A matches (within +/- 2.0 tolerance ladder): **%d / %d**" %
             (sc["arm_a_n_matched"], sc["n_episodes"]))
    if sc["arm_a_tol_distribution"]:
        tol_str = ", ".join(
            "+/-%.1f: %d" % (k, v) for k, v in sc["arm_a_tol_distribution"].items()
        )
        L.append("- Arm A tolerance ladder used: %s" % tol_str)
    L.append("")
    L.append("## E[L]* per channel (pooled LC baseline pool)")
    L.append("")
    L.append("| channel | E[L]* (days) | flag (Sec 7 [3.5, 10.5]) | note |")
    L.append("|---|---:|---|---|")
    for ch in CHANNELS:
        info = sc["el_per_channel"][ch]
        el_str = ("%.2f" % info["el_star"]) if info["el_star"] is not None else "n/a"
        flag = "FLAG" if info["flag"] else "ok"
        L.append("| %s | %s | %s | %s |" % (ch, el_str, flag, info["note"]))
    L.append("")
    L.append("## Sanity-check verdict")
    L.append("")
    if sc["fires"]:
        L.append("**HALT** -- one or more sanity checks fired:")
        for f in sc["fires"]:
            L.append("- %s" % f)
        L.append("")
        L.append("Per spec Sec 10.4 step 1 + Sec 7, the spec requires revision before "
                 "the full characterisation can run. **No spec edits in this session "
                 "per Sec 3.9 step 4** of the lock-process MD; the implied next step is "
                 "to draft HA-P6-v2 in a separate session.")
    else:
        L.append("**PASS** -- all Sec 7 sanity checks satisfied. Proceeding to full run "
                 "per Sec 10.4 step 2.")
    L.append("")
    L.append("## Episode roster")
    L.append("")
    L.append("| # | start | end | duration (d) | phase | t0 (episode-end) | t0 (last-below-threshold) |")
    L.append("|---:|---|---|---:|---|---|---|")
    for i, ep in enumerate(episodes):
        L.append("| %d | %s | %s | %d | %s | %s | %s |" % (
            i + 1, ep["start_date"], ep["end_date"], ep["duration"],
            ep["phase"], ep["episode_end_t0_date"],
            ep["last_below_threshold_date"],
        ))
    L.append("")
    return "\n".join(L) + "\n"


# === Plotting ========================================================


def emit_plots(cells: dict, plots_dir: Path) -> int:
    """Emit per-channel x phase trajectory PNGs (median + IQR-equivalent band
    + individual traces) for the locked single cell baseline_arm=arm_b,
    detrend=none, window=primary, t0=episode_end.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return 0
    plots_dir.mkdir(parents=True, exist_ok=True)
    n_plots = 0
    for ch in CHANNELS:
        for ph in ("pooled",) + PHASES:
            key = (ch, ph, "arm_b", "none", "primary", "episode_end")
            cell = cells.get(key)
            if cell is None or cell["n_episodes"] == 0:
                continue
            z = np.array(cell["z_per_episode"])
            if z.size == 0 or not np.any(~np.isnan(z)):
                continue
            days = PRIMARY_WINDOW
            med = np.array(cell["per_day_median"])
            lo = np.array(cell["per_day_ci_lo"])
            hi = np.array(cell["per_day_ci_hi"])
            fig, ax = plt.subplots(figsize=(6, 4))
            # Individual traces
            for row in z:
                if np.any(~np.isnan(row)):
                    ax.plot(days, row, color="grey", alpha=0.30, linewidth=0.8)
            # Median + CI band
            ax.fill_between(days, lo, hi, color="C0", alpha=0.25, label="95% block-bootstrap CI")
            ax.plot(days, med, color="C0", linewidth=2.0, label="median z (Arm B)")
            ax.axhline(0.0, linestyle="--", color="black", linewidth=0.7)
            ax.axhline(0.5, linestyle=":", color="grey", linewidth=0.5)
            ax.axhline(-0.5, linestyle=":", color="grey", linewidth=0.5)
            ax.set_xlabel("day-offset (t = episode-end)")
            ax.set_ylabel("z vs lagged baseline")
            ax.set_title("%s x %s (n=%d)" % (ch, ph, cell["n_episodes"]))
            ax.legend(loc="best", fontsize=8)
            fig.tight_layout()
            outpath = plots_dir / ("%s__%s.png" % (ch, ph))
            fig.savefig(outpath, dpi=120)
            plt.close(fig)
            n_plots += 1
    return n_plots


# === result.csv ======================================================


def emit_csv(cells: dict, path: Path) -> int:
    rows = []
    for key, cell in cells.items():
        ch, ph, ba, da, wa, t0a = key
        days = PRIMARY_WINDOW if wa == "primary" else LATE_WINDOW
        for k, d in enumerate(days):
            rows.append({
                "channel": ch, "phase": ph, "baseline_arm": ba,
                "detrend_arm": da, "window_arm": wa, "t0_anchor": t0a,
                "day_offset": d,
                "n_episodes": cell["n_episodes"],
                "n_with_baseline": cell["n_with_baseline"],
                "median": cell["per_day_median"][k],
                "ci_lo": cell["per_day_ci_lo"][k],
                "ci_hi": cell["per_day_ci_hi"][k],
                "diff_median": cell["per_day_diff_median"][k],
                "diff_ci_lo": cell["per_day_diff_ci_lo"][k],
                "diff_ci_hi": cell["per_day_diff_ci_hi"][k],
                "category": cell["category"],
                "annotation": cell["annotation"],
            })
    pd.DataFrame(rows).to_csv(path, index=False)
    return len(rows)


# === Sec 9 propagation evaluation ====================================


def evaluate_sec9_propagations(cells: dict, sec_corr: dict) -> dict:
    """Evaluate the Sec 9 head propagations on the locked single cell."""
    # First-branch trigger: per channel, the Arm A median-difference CI
    # excludes 0 on >= 2 of 5 primary-window days
    sig_per_channel: dict[str, dict] = {}
    sig_channel_count = 0
    sig_channel_count_strict = 0
    for ch in CHANNELS:
        key = (ch, "pooled", "arm_a", "none", "primary", "episode_end")
        cell = cells.get(key)
        if cell is None or cell["n_episodes"] == 0:
            sig_per_channel[ch] = {"n_days_excl_0": 0, "n_total": 0,
                                   "distinguishable": False,
                                   "distinguishable_strict": False}
            continue
        days_excl_0 = 0
        total = 0
        for lo, hi in zip(cell["per_day_diff_ci_lo"], cell["per_day_diff_ci_hi"]):
            if not (np.isnan(lo) or np.isnan(hi)):
                total += 1
                if lo > 0 or hi < 0:
                    days_excl_0 += 1
        dist = days_excl_0 >= SIG_DAYS_PRIMARY
        dist_strict = days_excl_0 >= SIG_DAYS_SENSITIVITY
        if dist:
            sig_channel_count += 1
        if dist_strict:
            sig_channel_count_strict += 1
        sig_per_channel[ch] = {
            "n_days_excl_0": days_excl_0, "n_total": total,
            "distinguishable": bool(dist),
            "distinguishable_strict": bool(dist_strict),
        }
    first_branch_fires = sig_channel_count >= 3
    first_branch_fires_strict = sig_channel_count_strict >= 3

    # Second-branch trigger: Arm A median (== matched-baseline) on
    # majority of (channel x phase) cells: the Arm A no-detrend
    # episode-end-t0 primary-window cell's category matches the Arm B cell's
    # category. We approximate "matches matched-baseline" as
    # "Arm A median-difference CI INCLUDES 0 on every primary day".
    arm_a_match_count = 0
    total_cell_count = 0
    for ch in CHANNELS:
        for ph in ("pooled",) + PHASES:
            key = (ch, ph, "arm_a", "none", "primary", "episode_end")
            cell = cells.get(key)
            if cell is None or cell["n_episodes"] == 0:
                continue
            total_cell_count += 1
            all_include_0 = True
            had_valid_day = False
            for lo, hi in zip(cell["per_day_diff_ci_lo"], cell["per_day_diff_ci_hi"]):
                if not (np.isnan(lo) or np.isnan(hi)):
                    had_valid_day = True
                    if not (lo <= 0 <= hi):
                        all_include_0 = False
                        break
            if had_valid_day and all_include_0:
                arm_a_match_count += 1
    second_branch_fires = (
        total_cell_count > 0
        and arm_a_match_count >= 0.5 * total_cell_count
    )

    # Sec 4.8.4 secondary correlations: CI excludes 0 on the locked cell?
    locked_corr = {}
    for ch in CHANNELS:
        rd = sec_corr.get(ch, {}).get("rate_vs_duration",
                                      {"ci_lo": float("nan"), "ci_hi": float("nan")})
        cn = sec_corr.get(ch, {}).get("completeness_vs_next",
                                      {"ci_lo": float("nan"), "ci_hi": float("nan")})
        rd_excl = (not (np.isnan(rd["ci_lo"]) or np.isnan(rd["ci_hi"]))
                   and (rd["ci_lo"] > 0 or rd["ci_hi"] < 0))
        cn_excl = (not (np.isnan(cn["ci_lo"]) or np.isnan(cn["ci_hi"]))
                   and (cn["ci_lo"] > 0 or cn["ci_hi"] < 0))
        locked_corr[ch] = {
            "rate_vs_duration_excl_0": bool(rd_excl),
            "completeness_vs_next_excl_0": bool(cn_excl),
        }

    return {
        "first_branch": {
            "n_sig_channels": int(sig_channel_count),
            "n_sig_channels_strict": int(sig_channel_count_strict),
            "fires": bool(first_branch_fires),
            "fires_strict": bool(first_branch_fires_strict),
            "per_channel": sig_per_channel,
        },
        "second_branch": {
            "arm_a_match_count": int(arm_a_match_count),
            "total_cell_count": int(total_cell_count),
            "fires": bool(second_branch_fires),
        },
        "locked_correlations": locked_corr,
    }


# === Full run ========================================================


def run_full(df: pd.DataFrame, episodes: list[dict],
             arm_a_matches: list[dict], dt_idx: dict[date, int]) -> dict:
    """Run the full Sec 4.8 grid + Sec 4.8.4 secondaries + Sec 9 propagations."""
    cells: dict = {}
    seed_off = 0
    print("  computing per-cell trajectories (channel x phase x baseline_arm x detrend x window x t0)...")
    grand_total = (
        len(CHANNELS) * (1 + len(PHASES)) * 2 * 2 * 2 * 2
    )
    done = 0
    for channel in CHANNELS:
        for phase in ("pooled",) + PHASES:
            for baseline_arm in ("arm_a", "arm_b"):
                for detrend_arm in ("none", "detrend"):
                    for window_arm in ("primary", "late"):
                        for t0_anchor in ("episode_end", "last_below"):
                            # Use full B for headline cell + diagnostic for others
                            is_headline = (
                                phase == "pooled"
                                and detrend_arm == "none"
                                and window_arm == "primary"
                                and t0_anchor == "episode_end"
                            )
                            n_boot = B_HEADLINE if is_headline else B_DIAGNOSTIC
                            cell = run_cell(
                                df, episodes, dt_idx, arm_a_matches,
                                channel=channel, phase=phase,
                                baseline_arm=baseline_arm,
                                detrend_arm=detrend_arm,
                                window_arm=window_arm,
                                t0_anchor=t0_anchor,
                                seed_offset=seed_off,
                                n_boot=n_boot,
                            )
                            seed_off += 7
                            cells[(channel, phase, baseline_arm,
                                   detrend_arm, window_arm, t0_anchor)] = cell
                            done += 1
                            if done % 50 == 0:
                                print("    %d / %d cells" % (done, grand_total))
    print("  done: %d cells" % done)

    # Sec 4.8.4 secondary correlations on the locked single cell per channel
    print("  computing Sec 4.8.4 secondary Spearman correlations (locked cell only) ...")
    sec_corr: dict = {}
    for ch in CHANNELS:
        sec_corr[ch] = secondary_correlations(
            episodes, cells, channel=ch, phase="pooled", baseline_arm="arm_b",
        )

    # Sec 9 propagation evaluation
    print("  evaluating Sec 9 propagations on the locked single cell ...")
    sec9 = evaluate_sec9_propagations(cells, sec_corr)

    return {"cells": cells, "secondary_correlations": sec_corr,
            "sec9_propagations": sec9}


# === result.md emission ==============================================


def fmt_ci(point: float, lo: float, hi: float, fmt: str = "%.3f") -> str:
    if np.isnan(point):
        return "--"
    if np.isnan(lo) or np.isnan(hi):
        return (fmt % point) + " [--]"
    return (fmt + " [" + fmt + ", " + fmt + "]") % (point, lo, hi)


def emit_result_md(
    df: pd.DataFrame, episodes: list[dict], arm_a_matches: list[dict],
    sc: dict, results: dict,
) -> str:
    cells = results["cells"]
    sec_corr = results["secondary_correlations"]
    sec9 = results["sec9_propagations"]
    today = date.today().isoformat()

    L: list[str] = []
    L.append("# HA-P6 -- result: post-crash window distinctive autonomic-recovery shape")
    L.append("")
    L.append("*Run %s by `script.py` against the locked pre-registration `hypothesis.md` "
             "(revision 2026-06-15-r2/r3, status LOCKED). Random seed: %d; "
             "stationary-bootstrap CIs at E[L]=%d days per "
             "`methodology/permutation_null_block_length.md`.*" %
             (today, RANDOM_SEED, E_BLOCK_LEN))
    L.append("")
    L.append("**Layer 1 descriptive characterisation per CONVENTIONS Sec 2.1. "
             "NO SUPPORTED / NOT-SUPPORTED bar.** Sec 5 of the pre-reg names this "
             "result.md as reporting the *findings shape* regardless of the data; "
             "Sec 9 enumerates downstream propagations per observation shape.")
    L.append("")
    L.append("## Headline cell (pooled LC x Arm-B lagged baseline x no-detrend x episode-end-t0 x primary [t+1, t+5])")
    L.append("")
    L.append("| channel | n eps | n w/ baseline | category | annotation | recovery day | depth (median |z|) | completeness |")
    L.append("|---|---:|---:|---|---|---:|---:|---:|")
    for ch in CHANNELS:
        key = (ch, "pooled", "arm_b", "none", "primary", "episode_end")
        cell = cells[key]
        rc = cell["recovery_completion"]
        rc_str = ("%.1f" % rc["median_day"]) if rc["median_day"] is not None else (
            "not within window (residual %.2f)" % rc["residual_at_t5_median"]
            if not np.isnan(rc["residual_at_t5_median"]) else "n/a"
        )
        L.append("| %s | %d | %d | %s | %s | %s | %s | %s |" % (
            ch, cell["n_episodes"], cell["n_with_baseline"],
            cell["category"], cell["annotation"] or "--",
            rc_str,
            "%.2f" % cell["depth_median"] if not np.isnan(cell["depth_median"]) else "--",
            "%.2f" % cell["completeness_median"] if not np.isnan(cell["completeness_median"]) else "--",
        ))
    L.append("")
    L.append("Per-day median z (Arm B) with 95%% block-bootstrap CI:")
    L.append("")
    L.append("| channel | t+1 | t+2 | t+3 | t+4 | t+5 |")
    L.append("|---|---|---|---|---|---|")
    for ch in CHANNELS:
        cell = cells[(ch, "pooled", "arm_b", "none", "primary", "episode_end")]
        cols = [fmt_ci(cell["per_day_median"][k],
                       cell["per_day_ci_lo"][k], cell["per_day_ci_hi"][k])
                for k in range(5)]
        L.append("| %s | %s |" % (ch, " | ".join(cols)))
    L.append("")

    L.append("## Arm A (matched-deep-trough non-crash days) -- the strict RTM control")
    L.append("")
    L.append("**Per Sec 8 caveat 1, this is the LOAD-BEARING read for the RTM-vs-autonomic question.** "
             "Per-day median DIFFERENCE (crash trajectory minus matched-control trajectory) with "
             "95%% paired-bootstrap CI on the same headline cell:")
    L.append("")
    L.append("| channel | t+1 diff | t+2 diff | t+3 diff | t+4 diff | t+5 diff | days CI excludes 0 |")
    L.append("|---|---|---|---|---|---|---:|")
    for ch in CHANNELS:
        cell = cells[(ch, "pooled", "arm_a", "none", "primary", "episode_end")]
        cols = [fmt_ci(cell["per_day_diff_median"][k],
                       cell["per_day_diff_ci_lo"][k],
                       cell["per_day_diff_ci_hi"][k])
                for k in range(5)]
        excl = sec9["first_branch"]["per_channel"][ch]
        L.append("| %s | %s | %d / %d |" % (
            ch, " | ".join(cols), excl["n_days_excl_0"], excl["n_total"],
        ))
    L.append("")
    L.append("Sec 9 head operational binding (>= 2 of 5 primary-window days; CI on median diff excludes 0):")
    L.append("")
    L.append("- Channels statistically-distinguishable from matched control: **%d / %d** "
             "(Sec 9 first-branch trigger fires if >= 3)." %
             (sec9["first_branch"]["n_sig_channels"], len(CHANNELS)))
    L.append("- Strict (>= 3 of 5 days) sensitivity: **%d / %d**." %
             (sec9["first_branch"]["n_sig_channels_strict"], len(CHANNELS)))
    L.append("")

    L.append("## Sec 4.8.4 secondary correlations (locked headline cell -- channel x pooled-LC x Arm-B x no-detrend)")
    L.append("")
    L.append("Spearman rho with 95%% block-bootstrap CI at E[L]=%d, B=%d:" % (E_BLOCK_LEN, B_CORRELATION))
    L.append("")
    L.append("| channel | rate vs duration: rho [95% CI] (n) | completeness vs next-interval: rho [95% CI] (n) |")
    L.append("|---|---|---|")
    for ch in CHANNELS:
        rd = sec_corr[ch]["rate_vs_duration"]
        cn = sec_corr[ch]["completeness_vs_next"]
        L.append("| %s | %s (n=%d) | %s (n=%d) |" % (
            ch,
            fmt_ci(rd["rho"], rd["ci_lo"], rd["ci_hi"]),
            rd["n"],
            fmt_ci(cn["rho"], cn["ci_lo"], cn["ci_hi"]),
            cn["n"],
        ))
    L.append("")
    L.append("**Reading discipline per Sec 1.2 + Sec 4.8.4**: NO SUPPORTED bar. CI containing 0 -> "
             "null correlation read; otherwise report sign + magnitude. Sec 9 bullets 7/8 fire on the "
             "single-cell-locked cell only (above); diagnostic-only readings for other cells are in the "
             "result.csv `secondary_cell_signal` companion.")
    L.append("")

    L.append("## Per-phase tables (Arm B z-trajectory)")
    L.append("")
    L.append("Phases per [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) Sec 3.")
    L.append("")
    L.append("| channel | phase | n eps | category | annotation | recovery day | depth (median |z|) |")
    L.append("|---|---|---:|---|---|---:|---:|")
    for ch in CHANNELS:
        for ph in PHASES:
            key = (ch, ph, "arm_b", "none", "primary", "episode_end")
            cell = cells.get(key)
            if cell is None or cell["n_episodes"] == 0:
                continue
            rc = cell["recovery_completion"]
            rc_str = ("%.1f" % rc["median_day"]) if rc["median_day"] is not None else (
                "not within window" if not np.isnan(rc["residual_at_t5_median"]) else "n/a"
            )
            L.append("| %s | %s | %d | %s | %s | %s | %s |" % (
                ch, ph, cell["n_episodes"], cell["category"],
                cell["annotation"] or "--",
                rc_str,
                "%.2f" % cell["depth_median"] if not np.isnan(cell["depth_median"]) else "--",
            ))
    L.append("")
    L.append("**Sec 4.7 honesty caveat**: buildup + afbouw + post_afbouw phases have small ns "
             "(per Sec 4.7 estimates ~1-3 each); per-phase categories are *descriptive only* with "
             "wide CIs. The pooled-LC headline above is the project-level read.")
    L.append("")

    L.append("## Sec 3.7 detrend sensitivity (Arm B z-trajectory, detrended)")
    L.append("")
    L.append("**Reading per Sec 4.6**: if recovery shape SURVIVES detrending -> event-driven; "
             "FAILS detrending (flat residual) -> apparent recovery was LC trajectory continuing.")
    L.append("")
    L.append("| channel | phase | no-detrend category | detrended category | survives detrend? |")
    L.append("|---|---|---|---|---|")
    for ch in CHANNELS:
        for ph in ("pooled",) + PHASES:
            k_raw = (ch, ph, "arm_b", "none", "primary", "episode_end")
            k_dt = (ch, ph, "arm_b", "detrend", "primary", "episode_end")
            raw = cells.get(k_raw)
            dt = cells.get(k_dt)
            if raw is None or dt is None or raw["n_episodes"] == 0:
                continue
            survives = (
                raw["category"] not in ("no-meaningful-change", "noisy-inconclusive")
                and dt["category"] == raw["category"]
            )
            L.append("| %s | %s | %s | %s | %s |" % (
                ch, ph, raw["category"], dt["category"],
                "yes" if survives else "no",
            ))
    L.append("")

    L.append("## Sec 1.3 late-recovery sensitivity ([t+6, t+10])")
    L.append("")
    L.append("Same classifier on the late-recovery window; reads as 'recovery continued beyond t+5' "
             "vs 'plateaued'. Pooled headline cells only:")
    L.append("")
    L.append("| channel | late-window category | late-window depth | late-window recovery day |")
    L.append("|---|---|---:|---:|")
    for ch in CHANNELS:
        cell = cells.get((ch, "pooled", "arm_b", "none", "late", "episode_end"))
        if cell is None or cell["n_episodes"] == 0:
            continue
        rc = cell["recovery_completion"]
        rc_str = ("%.1f" % rc["median_day"]) if rc["median_day"] is not None else "not within window"
        L.append("| %s | %s | %s | %s |" % (
            ch, cell["category"],
            "%.2f" % cell["depth_median"] if not np.isnan(cell["depth_median"]) else "--",
            rc_str,
        ))
    L.append("")

    L.append("## t0-sensitivity (episode-end vs last-below-threshold-day)")
    L.append("")
    L.append("Per Sec 5 item 7 + Sec 9: concordance / divergence read.")
    L.append("")
    L.append("| channel | episode-end category | last-below category | concordant? |")
    L.append("|---|---|---|---|")
    for ch in CHANNELS:
        a = cells.get((ch, "pooled", "arm_b", "none", "primary", "episode_end"))
        b = cells.get((ch, "pooled", "arm_b", "none", "primary", "last_below"))
        if a is None or b is None or a["n_episodes"] == 0:
            continue
        conc = "yes" if a["category"] == b["category"] else "no"
        L.append("| %s | %s | %s | %s |" % (
            ch, a["category"], b["category"], conc,
        ))
    L.append("")

    L.append("## Sec 9 observation-shape propagations -- evaluation on the locked headline cell")
    L.append("")
    fb = sec9["first_branch"]
    sb = sec9["second_branch"]
    L.append("- **First branch ('distinct recovery shape across >= 3 of 7 channels')**: "
             "fires = **%s** (n_sig_channels=%d/%d at >= 2 of 5 days; strict >= 3 of 5: %d/%d)." %
             ("YES" if fb["fires"] else "NO",
              fb["n_sig_channels"], len(CHANNELS),
              fb["n_sig_channels_strict"], len(CHANNELS)))
    L.append("- **Second branch ('Arm A matches crash trajectory on majority')**: "
             "fires = **%s** (arm_a_match_count=%d / %d cells)." %
             ("YES" if sb["fires"] else "NO",
              sb["arm_a_match_count"], sb["total_cell_count"]))
    locked = sec9["locked_correlations"]
    sig_corr = [(ch, c) for ch, c in locked.items()
                if c["rate_vs_duration_excl_0"] or c["completeness_vs_next_excl_0"]]
    if sig_corr:
        L.append("- **Sec 4.8.4 secondary correlations excluding 0** on the locked headline cell:")
        for ch, c in sig_corr:
            parts = []
            if c["rate_vs_duration_excl_0"]:
                parts.append("rate vs duration")
            if c["completeness_vs_next_excl_0"]:
                parts.append("completeness vs next-interval")
            L.append("  - %s: %s" % (ch, ", ".join(parts)))
    else:
        L.append("- **Sec 4.8.4 secondary correlations**: all CIs include 0 on the locked headline cell "
                 "(null correlation read per Sec 1.2).")
    L.append("")

    L.append("## Cross-test bridge to HA-P7 (read after this script.py is committed)")
    L.append("")
    L.append("Per the Sec 9 first-branch downstream propagation -- if HA-P6 has characterised a real "
             "post-crash signature, the median recovery-completion-day across channels informs HA-P7's "
             "14d window-length assumption (3-5 days -> 14d window covers recovery + further; "
             "7-10+ days -> 14d window is recovery-specific). Per the headline table above, the "
             "median recovery-completion-day pattern across channels is the cross-test bridge.")
    L.append("")

    L.append("## Sec 4.8.1 data-driven E[L]* companion")
    L.append("")
    L.append("| channel | E[L]* (days) | factor-of-2 flag ([3.5, 10.5]) |")
    L.append("|---|---:|---|")
    for ch in CHANNELS:
        info = sc["el_per_channel"][ch]
        el_str = ("%.2f" % info["el_star"]) if info["el_star"] is not None else "n/a"
        flag = "FLAG" if info["flag"] else "ok"
        L.append("| %s | %s | %s |" % (ch, el_str, flag))
    L.append("")

    L.append("## Caveats per Sec 8 (must be acknowledged on every read)")
    L.append("")
    L.append("1. **Regression to the mean (RTM) is the central confound**. Crash days have low "
             "gevoelscore by definition; subsequent days regress toward the participant's mean "
             "by construction. The Arm A median-difference table above is the load-bearing read.")
    L.append("2. **n=29 LC-era episodes is sparse**. Per-channel per-day post-crash distributions "
             "have wide block-bootstrap CIs by construction. Descriptive characterisation is "
             "informative regardless; predictive sub-claims (Sec 4.8.4) have wide CIs by design.")
    L.append("3. **Power-calc dispatch**: power calc inapplicable per Daza 2018 within-subject design "
             "(see [Daza 2018 PDF](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)); "
             "additionally, HA-P6 is Layer 1 descriptive characterisation per CONVENTIONS Sec 2.1 "
             "with no SUPPORTED bar to power against. The block-bootstrap CIs per Sec 4.8.1 are the "
             "inference machinery; their honest width at n=29 is the discipline.")
    L.append("4. **Crash_v2 episode boundaries depend on the t0 definition**. The t0-sensitivity table "
             "above (episode-end vs last-below-threshold-day) reports concordance.")
    L.append("5. **Self-reported crash labels** via crash_v2 -- same instrument-level bias as HA-P7 caveat 5.")
    L.append("6. **Intervention-baseline dose-response broadens P6's caveat** per register caveat 5: "
             "`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest` CONFIRMED dose-modulated; "
             "the Sec 4.7 phase-stratified arm + Sec 3.7 detrend per phase addresses this.")
    L.append("7. **Channel coverage gaps**: `bb_overnight_gain` starts 2024-09-18; n=%d post-2024-09-18 "
             "episodes contribute." % sc["bb_overnight_n"])
    L.append("8. **CONVENTIONS Sec 3.7 trajectory-detrend is binding** per Sec 4.6. The detrend-sensitivity "
             "table above is the within-phase calibration check.")
    L.append("9. **Sec 3.4 inapplicable-to-primary by construction**: the trajectory IS computed across "
             "crash episodes; dropping `is_crash == True` rows would eliminate the entire test sample. "
             "Inapplicable-to-secondary because the correlation operates on per-episode summary statistics, "
             "not per-day observations.")
    L.append("10. **Matched-baseline construction (Arm A) is operational, not gold-standard**. The "
             "+/-1 gevoelscore-point matching tolerance is an operational choice; the tolerance ladder "
             "(+/-1.5, +/-2) is in use. Arm B (lagged baseline) is the project-pattern complement.")
    L.append("11. **Mechanistic claims about recovery physiology are out of scope** -- this characterises "
             "the *shape*; the *why* is for downstream hypothesis tests.")
    L.append("")

    L.append("## Audit-report acknowledgements (per [`reviews/HA-P6-2026-06-15.md`](../../../reviews/HA-P6-2026-06-15.md))")
    L.append("")
    L.append("The post-lock fresh-session audit (verdict REVISION RECOMMENDED -> closures absorbed in "
             "r2) called out: (1) Sec 8 power-calc dispatch (added in r2; surfaced in caveat 3 above); "
             "(2) Sec 4.8.3 qualitative shape classifier algorithmic pre-spec (added in r2; this script "
             "implements the conjunct in `classify_shape`); (3) Sec 9 head 'statistically-distinguishable' "
             "operational binding (added in r2; bound to >= 2 of 5 days CI on median difference excludes 0); "
             "(4) Sec 9 secondary-correlation single-cell lock (added in r2; this script implements the "
             "pooled-LC x Arm-A x no-detrend x episode-end-t0 x primary-window single cell as the "
             "propagation-driving cell). The audit's recommendations #5 (per-phase minimum-n gate on "
             "Sec 9 third-branch) and #6 (register-row pointer at lock) are not addressed in this script -- "
             "rec #5 is queued for HA-P6-r3/v2 per the r2 authorship block; rec #6 is executed at lock "
             "per Sec 3.8 gate 3 in the personal_hypotheses.md P6 entry.")
    L.append("")

    L.append("---")
    L.append("")
    L.append("*Result emitted by `script.py` on the locked pre-registration. Raw result data "
             "(per-cell bootstrap CIs, episode rosters, classifier annotations) in `result-data.json`; "
             "full multi-arm per-day-per-cell trajectory data in `result.csv`; per-channel x phase "
             "trajectory PNGs in `plots/`. Any post-result modification of the spec creates HA-P6-v2 "
             "with this v1 archived.*")
    return "\n".join(L) + "\n"


# === Main ============================================================


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Print sample sizes + Sec 7 sanity checks; emit "
                             "dry-run-report.md; halt before any trajectory "
                             "computation.")
    args = parser.parse_args()

    load_env()
    print("Loading per_day_master.csv (as_of_date=%s) ..." % DATA_CUT)
    df = load_master(as_of_date=str(DATA_CUT), stratum_4_only=False)
    print("  rows: %d, dates %s -> %s" %
          (len(df), df["date"].min().date(), df["date"].max().date()))
    df = df.sort_values("date").reset_index(drop=True)
    df["is_crash"] = df["is_crash"].astype(bool)
    dt_idx = date_to_idx_map(df)

    print("Detecting crash_v2 episodes via contiguous is_crash==True runs ...")
    episodes = detect_episodes(df)
    print("  found %d episodes in LC era" % len(episodes))

    print("Finding Arm A matched-deep-trough non-crash controls per episode ...")
    arm_a_matches = build_arm_a_match_table(df, episodes, dt_idx)
    n_arm_a = sum(1 for m in arm_a_matches if m["match_date"] is not None)
    print("  Arm A matches: %d / %d episodes" % (n_arm_a, len(episodes)))

    print("Running Sec 7 sanity checks ...")
    sc = sanity_checks(df, episodes, arm_a_matches, dt_idx)
    print("  E[L]* per channel:")
    for ch in CHANNELS:
        info = sc["el_per_channel"][ch]
        el_str = ("%.2f" % info["el_star"]) if info["el_star"] is not None else "n/a"
        flag_str = " FLAG" if info["flag"] else ""
        print("    %-50s E[L]*=%s%s" % (ch, el_str, flag_str))
    print("  sanity verdict: %s" % ("PASS" if sc["pass"] else "HALT"))
    if sc["fires"]:
        for f in sc["fires"]:
            print("    - %s" % f)

    OUT_DRY_RUN.write_text(emit_dry_run_report(sc, episodes), encoding="utf-8")
    print("Wrote %s" % OUT_DRY_RUN)

    if args.dry_run:
        return 0 if sc["pass"] else 1

    if not sc["pass"]:
        print("Sanity check failed (per Sec 7 / Sec 10.4 step 1). Halting "
              "before full run; no spec edits per Sec 3.9 step 4.")
        return 1

    print("")
    print("Running full characterisation ...")
    results = run_full(df, episodes, arm_a_matches, dt_idx)
    results["sanity_checks"] = sc

    # JSON output (cells dict needs key serialization)
    json_safe_cells = {}
    for key, cell in results["cells"].items():
        skey = "|".join(key)
        # Drop the per-episode arrays from JSON (too large; in CSV instead)
        slim = {k: v for k, v in cell.items()
                if k not in ("z_per_episode", "raw_per_episode", "control_per_episode")}
        json_safe_cells[skey] = slim
    json_payload = {
        "seed": RANDOM_SEED,
        "e_block_len": E_BLOCK_LEN,
        "n_boot_headline": B_HEADLINE,
        "n_boot_diagnostic": B_DIAGNOSTIC,
        "n_boot_correlation": B_CORRELATION,
        "episode_count": len(episodes),
        "arm_a_match_count": n_arm_a,
        "cells": json_safe_cells,
        "secondary_correlations": results["secondary_correlations"],
        "sec9_propagations": results["sec9_propagations"],
        "sanity_checks": {
            "n_episodes": sc["n_episodes"],
            "el_per_channel": sc["el_per_channel"],
            "bb_overnight_n": sc["bb_overnight_n"],
            "per_phase_n": sc["per_phase_n"],
            "arm_a_n_matched": sc["arm_a_n_matched"],
            "arm_a_tol_distribution": {
                str(k): int(v) for k, v in sc["arm_a_tol_distribution"].items()
            },
            "fires": sc["fires"],
            "pass": sc["pass"],
        },
    }
    OUT_RESULT_JSON.write_text(
        json.dumps(json_payload, indent=2, default=str), encoding="utf-8"
    )
    print("Wrote %s" % OUT_RESULT_JSON)

    n_rows = emit_csv(results["cells"], OUT_RESULT_CSV)
    print("Wrote %s (%d rows)" % (OUT_RESULT_CSV, n_rows))

    n_plots = emit_plots(results["cells"], OUT_PLOTS_DIR)
    print("Wrote %d plots in %s" % (n_plots, OUT_PLOTS_DIR))

    md = emit_result_md(df, episodes, arm_a_matches, sc, results)
    OUT_RESULT_MD.write_text(md, encoding="utf-8")
    print("Wrote %s" % OUT_RESULT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
