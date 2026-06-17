"""HA-P6 v3 -- post-crash window distinctive autonomic-recovery shape.

Implements the LOCKED v3 pre-registration at hypothesis.md (2026-06-17 lock).
v3 supersedes v2 (archived at hypothesis-v2-archived.md); v1 archived at
hypothesis-v1-archived.md / script-v1-archived.py.

v3 closures absorbed (per the v2 fresh-session audit
reviews/HA-P6-2026-06-17-v2.md, all 8 named closures):
  v2 carry-forward:
    (a) per-channel four-verdict E[L] policy (v3 splits PASS-fallback)
    (b) per-episode `completeness_per_episode` array threaded in cell
    (c) interpretation (ii) pooled-LC daily time series for E[L]*
  v3 NEW:
    #1 Series B unmedicated-stratum E[L]* sensitivity arm + FAIL rebind
    #2 PASS-fallback split into -degenerate (E[L]=7) vs -no-cutoff (E[L]=14)
    #3 Override magnitude cap at min(round(E[L]*), 21)
    #4 Paired-by-episode stationary bootstrap for §9 first-branch trigger
    #5 [3.5, 10.5] factor-of-2 verdict-range acknowledged (binding)
    #6 Eligible-day filter excludes is_crash days (conservative deviation)
    #7 §4.8.4 day-level-E[L]-on-per-episode-summary granularity mismatch
       acknowledged in §8 caveat (structural; deferred to v4)
    #8 §10.4 line-count arithmetic fix (typo; no impact on logic)

Usage:
  python script.py --dry-run    # Sec 10.4 step 1 (halt-on-narrower-set)
  python script.py              # Sec 10.4 step 2 (full run + result.md)

v3 narrower halt-set:
  - pooled n outside [25, 35]
  - bb_overnight_gain zero post-2024-09-18 episodes
  - FAIL on Series A AND Series B for any of:
    stress_mean_sleep / bb_overnight_gain / gevoelscore

Outputs into HA-P6 folder:
  script.py
  dry-run-report.md
  result.md
  result-data.json
  result.csv
  plots/   (per-channel x phase trajectory PNGs)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "docs" / "research" / "analyses"))

from _utils.inference import compute_data_driven_block_length  # noqa: E402
from _utils.frame import load_master  # noqa: E402


# === Locked constants per hypothesis.md v3 ===========================

LC_START = date(2022, 4, 4)
DATA_CUT = date(2026, 6, 5)

# v3 closure #1: Series B unmedicated-stratum upper bound
UNMEDICATED_END = date(2024, 4, 8)   # inclusive; buildup begins 2024-04-09

CHANNELS: tuple[str, ...] = (
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
    "bb_overnight_gain",
    "resting_hr",
    "gevoelscore",
    "stress_low_motion_min_count_S60_Mlow",
)

# v3 halt-discipline channel sets (§7 + §10.1)
HALT_ON_FAIL_CHANNELS: tuple[str, ...] = (
    "stress_mean_sleep", "bb_overnight_gain", "gevoelscore",
)

BB_OVERNIGHT_GAIN_START = date(2024, 9, 18)

PHASE_BUILDUP_START = date(2024, 4, 9)
PHASE_CONSOL_START = date(2024, 6, 20)
PHASE_AFBOUW_START = date(2026, 3, 20)
PHASE_POST_START = date(2026, 6, 6)

PHASES: tuple[str, ...] = (
    "unmedicated", "buildup", "consolidation", "afbouw", "post_afbouw",
)

BOUNDARY_CLUSTER_START = date(2024, 4, 9)
BOUNDARY_CLUSTER_END = date(2024, 4, 16)
BUILDUP_BUFFER_LAST_EXCLUDED = date(2024, 4, 29)

PRIMARY_WINDOW = tuple(range(1, 6))
LATE_WINDOW = tuple(range(6, 11))

BASELINE_BACK_FAR = 90
BASELINE_BACK_NEAR = 30
BASELINE_MIN_VALID = 40

ARM_A_PRE_BACK = 10
ARM_A_NEIGHBOURHOOD = (20, 10)
ARM_A_TOL_LADDER = (1.0, 1.5, 2.0)

E_BLOCK_DEFAULT = 7
E_BLOCK_NO_CUTOFF = 14         # v3 closure #2 PASS-fallback-no-cutoff override
E_BLOCK_OVERRIDE_CAP = 21      # v3 closure #3 cap
B_HEADLINE = 10000
B_DIAGNOSTIC = 2000
B_CORRELATION = 10000
RANDOM_SEED = 20260617

SANITY_N_LOW = 25
SANITY_N_HIGH = 35
SANITY_EL_STAR_LOW = 3.5       # v3 closure #5 factor-of-2 (binding)
SANITY_EL_STAR_HIGH = 10.5

CLASS_NMC_Z_THRESHOLD = 0.3
CLASS_NMC_SLOPE_THRESHOLD = 0.05
CLASS_STAIR_FLAT_DZ = 0.15
CLASS_RECOVERY_PROGRESS_MONO = 1.0
CLASS_RECOVERY_PROGRESS_STAIR = 0.5
CLASS_BASELINE_BAND = 0.5
CLASS_NOISY_CI_HALFWIDTH = 1.0

SIG_DAYS_PRIMARY = 2
SIG_DAYS_SENSITIVITY = 3
RECOVERY_COMPLETION_Z_THRESHOLD = 0.5

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


def date_to_idx_map(df: pd.DataFrame) -> dict[date, int]:
    arr = (df["date"].dt.date.to_numpy()
           if hasattr(df["date"].iloc[0], "date")
           else df["date"].to_numpy())
    return {d: i for i, d in enumerate(arr)}


# === Episode detection ===============================================


def detect_episodes(df: pd.DataFrame) -> list[dict]:
    df = df.reset_index(drop=True)
    n = len(df)
    ic = df["is_crash"].astype(bool).to_numpy()
    dates = (df["date"].dt.date.to_numpy()
             if hasattr(df["date"].iloc[0], "date")
             else df["date"].to_numpy())
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
            if ep_end_date < LC_START or ep_end_date > DATA_CUT:
                continue
            sub_scores = score[s : e + 1]
            valid = ~np.isnan(sub_scores)
            if valid.any():
                min_val = np.nanmin(sub_scores)
                tied = np.where(sub_scores == min_val)[0]
                last_below_date = dates[s + int(tied[-1])]
            else:
                last_below_date = ep_end_date
            episodes.append({
                "start_idx": s, "end_idx": e,
                "start_date": ep_start_date, "end_date": ep_end_date,
                "duration": e - s + 1,
                "episode_end_t0_date": ep_end_date,
                "last_below_threshold_date": last_below_date,
                "phase": citalopram_phase(ep_end_date),
            })
        else:
            i += 1
    return episodes


# === Lagged baseline (Arm B, §4.5) ===================================


def lagged_baseline_for_channel(
    df: pd.DataFrame, t0: date, channel: str, phase: str,
    dt_idx: dict[date, int],
) -> dict:
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
    df: pd.DataFrame, t0: date, channel: str, phase: str,
    dt_idx: dict[date, int],
) -> dict:
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
        pairs.append((-k, float(v)))
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


# === Arm A matching ==================================================


def find_arm_a_match(
    df: pd.DataFrame, episode: dict, dt_idx: dict[date, int],
    episode_dates: set[date], *, tolerance: float,
) -> date | None:
    t0 = episode["episode_end_t0_date"]
    phase = episode["phase"]
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
    pre_arr = np.array(pre[::-1])
    pre_back, post_fwd = ARM_A_NEIGHBOURHOOD
    candidates: list[tuple[date, float]] = []
    arr = (df["date"].dt.date.to_numpy()
           if hasattr(df["date"].iloc[0], "date")
           else df["date"].to_numpy())
    for j, d in enumerate(arr):
        if d < LC_START or d > DATA_CUT:
            continue
        if citalopram_phase(d) != phase:
            continue
        if abs((d - t0).days) <= max(pre_back, post_fwd):
            continue
        in_nbh = False
        for delta in range(-pre_back, post_fwd + 1):
            if (d + timedelta(days=delta)) in episode_dates:
                in_nbh = True
                break
        if in_nbh:
            continue
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
        diffs = np.abs(cand_arr - pre_arr)
        if np.any(diffs > tolerance):
            continue
        candidates.append((d, float(np.mean(diffs))))
    if not candidates:
        return None
    candidates.sort(key=lambda t: t[1])
    return candidates[0][0]


def build_arm_a_match_table(
    df: pd.DataFrame, episodes: list[dict], dt_idx: dict[date, int],
) -> list[dict]:
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
                    "match_date": match, "tol_used": tol_used})
    return out


# === Trajectory + detrend ============================================


def extract_trajectory(
    df: pd.DataFrame, anchor: date, channel: str,
    days: tuple[int, ...], dt_idx: dict[date, int],
) -> np.ndarray:
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
    if np.isnan(slope) or np.isnan(intercept):
        return np.full_like(raw_vals, np.nan)
    pred = slope * np.array(days, dtype=float) + intercept
    return raw_vals - pred


# === v3 E[L]* policy =================================================
# v3 closures #1, #2, #3, #5, #6


def build_lc_daily_series(
    df: pd.DataFrame, channel: str, *, unmedicated_only: bool,
) -> np.ndarray:
    """v2 closure (c) + v3 closure #6: pooled-LC daily series, ordered by
    date, eligible-day filter applied (LC era + non-crash days only).

    v3 closure #1 sensitivity arm: set unmedicated_only=True to restrict
    to [LC_START, UNMEDICATED_END] (no CPAP/Citalopram transitions).
    """
    dates = (df["date"].dt.date.to_numpy()
             if hasattr(df["date"].iloc[0], "date")
             else df["date"].to_numpy())
    is_crash = df["is_crash"].astype(bool).to_numpy()
    vals = df[channel].to_numpy()
    end = UNMEDICATED_END if unmedicated_only else DATA_CUT
    mask = np.array([
        (LC_START <= d <= end) and (not c) and (not pd.isna(v))
        for d, c, v in zip(dates, is_crash, vals)
    ])
    order = np.argsort(dates[mask])
    return vals[mask][order].astype(float)


_NOTE_NO_CUTOFF_RX = re.compile(
    r"no clear acf cutoff|all lags within max_lag are significant|all lags",
    re.IGNORECASE,
)
_NOTE_DEGENERATE_RX = re.compile(
    r"closed-form formula degenerate|zero variance|n=\d+ < 30|n<30",
    re.IGNORECASE,
)


def assign_verdict(el_star: float, note: str) -> str:
    """v3 closure #2: four-verdict logic. Returns one of:
      PASS-real, PASS-fallback-no-cutoff, PASS-fallback-degenerate, FAIL.

    The estimator's `note` field carries the fallback reason when the
    estimator could not compute; PASS-real / FAIL fire when note is absent.
    """
    if note and _NOTE_NO_CUTOFF_RX.search(note):
        return "PASS-fallback-no-cutoff"
    if note and _NOTE_DEGENERATE_RX.search(note):
        return "PASS-fallback-degenerate"
    if SANITY_EL_STAR_LOW <= el_star <= SANITY_EL_STAR_HIGH:
        return "PASS-real"
    return "FAIL"


def compute_el_verdicts(df: pd.DataFrame) -> dict[str, dict]:
    """v3 §4.8.1 four-verdict E[L] policy, run on Series A (pooled-LC) and
    Series B (unmedicated-stratum) per v3 closures #1 + #2.

    Returns dict[channel -> {verdict, el_star_pooled, el_star_unmedicated,
    el_used, binding_series, cap_binding, note_pooled, note_unmedicated,
    verdict_pooled, verdict_unmedicated}].
    """
    out: dict[str, dict] = {}
    for ch in CHANNELS:
        series_a = build_lc_daily_series(df, ch, unmedicated_only=False)
        series_b = build_lc_daily_series(df, ch, unmedicated_only=True)

        res_a = compute_data_driven_block_length(series_a)
        el_a = float(res_a["optimal_block_length"])
        note_a = str(res_a.get("note", ""))
        verdict_a = assign_verdict(el_a, note_a)

        res_b = compute_data_driven_block_length(series_b)
        el_b = float(res_b["optimal_block_length"])
        note_b = str(res_b.get("note", ""))
        verdict_b = assign_verdict(el_b, note_b)

        # Disposition per §4.8.1 table (Series A binds by default; v3
        # closure #1 cross-check only fires on Series-A-FAIL + Series-B-PASS)
        binding = "A"
        cap_binding = False

        if verdict_a == "PASS-real":
            el_used = E_BLOCK_DEFAULT
        elif verdict_a == "PASS-fallback-no-cutoff":
            el_used = E_BLOCK_NO_CUTOFF
        elif verdict_a == "PASS-fallback-degenerate":
            el_used = E_BLOCK_DEFAULT
        else:  # FAIL
            # v3 closure #1: Series B cross-check on Series-A-FAIL upper end
            if (el_a > SANITY_EL_STAR_HIGH
                    and verdict_b == "PASS-real"):
                el_used = min(int(round(el_b)), E_BLOCK_OVERRIDE_CAP)
                binding = "B"
                cap_binding = int(round(el_b)) > E_BLOCK_OVERRIDE_CAP
            else:
                el_used = min(int(round(el_a)), E_BLOCK_OVERRIDE_CAP)
                cap_binding = int(round(el_a)) > E_BLOCK_OVERRIDE_CAP

        out[ch] = {
            "verdict": verdict_a,           # headline verdict from Series A
            "verdict_pooled": verdict_a,
            "verdict_unmedicated": verdict_b,
            "el_star_pooled": el_a,
            "el_star_unmedicated": el_b,
            "el_used": int(el_used),
            "binding_series": binding,
            "cap_binding": bool(cap_binding),
            "note_pooled": note_a,
            "note_unmedicated": note_b,
            "n_pooled": int(len(series_a)),
            "n_unmedicated": int(len(series_b)),
        }
    return out


# === Bootstrap CIs ===================================================


def per_day_median_ci(
    per_episode_values: np.ndarray, *, n_boot: int, seed: int,
) -> tuple[float, float, float]:
    """Per-day median CI via plain bootstrap on per-episode values for a
    single day-offset (event-level resample; no within-day temporal
    structure to preserve). Per spec Sec 4.8.1 the per-day median bootstrap
    is event-level; the stationary bootstrap with E[L] is the
    day-resampling layer used in the paired-difference + Spearman cells.
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
    """Plain paired bootstrap CI for diagnostic per-day cells (Arm A non-
    headline). The headline §9 first-branch cell uses the paired
    stationary-bootstrap variant below per v3 closure #4.
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


def per_day_paired_stationary_diff_ci(
    crash_matrix: np.ndarray, control_matrix: np.ndarray,
    *, expected_block_length: int, n_boot: int, seed: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """v3 closure #4: paired-by-episode stationary-bootstrap CI on the
    per-day median DIFFERENCE for the §9 first-branch headline cell.

    Each bootstrap iteration resamples episode indices via stationary
    bootstrap on the paired-index sequence at the channel's `el_used`;
    per-day median DIFFERENCE is computed on the paired-resample
    distribution. Returns three arrays of length n_days: (median, ci_lo,
    ci_hi) on the day-by-day difference.

    Inputs: crash_matrix and control_matrix both shape (n_episodes,
    n_days); paired-by-episode (row i of crash matches row i of control).
    """
    n_eps, n_days = crash_matrix.shape
    # Drop rows where the pair is invalid on EVERY day
    row_valid = ~(
        np.isnan(crash_matrix).all(axis=1)
        | np.isnan(control_matrix).all(axis=1)
    )
    crash = crash_matrix[row_valid]
    control = control_matrix[row_valid]
    n = crash.shape[0]
    med = np.full(n_days, np.nan)
    lo = np.full(n_days, np.nan)
    hi = np.full(n_days, np.nan)
    if n < 2:
        return (med, lo, hi)

    diff = crash - control
    for k in range(n_days):
        col = diff[:, k]
        valid = ~np.isnan(col)
        if valid.sum() >= 2:
            med[k] = float(np.median(col[valid]))

    rng = np.random.default_rng(seed)
    p = 1.0 / max(1, int(expected_block_length))

    boots = np.full((n_boot, n_days), np.nan)
    for b in range(n_boot):
        idx = np.empty(n, dtype=int)
        i = 0
        while i < n:
            start = int(rng.integers(0, n))
            L = int(rng.geometric(p))
            for j in range(L):
                if i >= n:
                    break
                idx[i] = (start + j) % n
                i += 1
        resampled = diff[idx]
        for k in range(n_days):
            col = resampled[:, k]
            valid = ~np.isnan(col)
            if valid.sum() >= 2:
                boots[b, k] = float(np.median(col[valid]))

    for k in range(n_days):
        bcol = boots[:, k]
        bcol = bcol[~np.isnan(bcol)]
        if len(bcol) >= 100:
            lo[k] = float(np.percentile(bcol, 2.5))
            hi[k] = float(np.percentile(bcol, 97.5))
    return (med, lo, hi)


def spearman_block_bootstrap_ci(
    x: np.ndarray, y: np.ndarray, *, n_boot: int, seed: int,
    expected_block_length: int,
) -> dict:
    """Stationary-bootstrap CI on Spearman rho. Per-episode resampling.

    Per v3 caveat #7: the day-level `expected_block_length` is over-
    conservative for per-episode-summary resampling; result.md surfaces
    this in the §4.8.4 row header.
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
    p = 1.0 / max(1, int(expected_block_length))
    boots: list[float] = []
    for _ in range(n_boot):
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


# === Shape classifier (§4.8.3) =======================================


def classify_shape(
    z_trajectory: np.ndarray, ci_half_widths: np.ndarray,
    detrend_slope: float, ci_includes_zero: np.ndarray,
) -> tuple[str, str]:
    z = z_trajectory
    if np.any(np.isnan(z)):
        return ("noisy-inconclusive", "noisy-shape-driven")
    abs_z = np.abs(z)

    cond1a = bool(np.all(abs_z < CLASS_NMC_Z_THRESHOLD))
    cond1b = bool(np.all(ci_includes_zero))
    cond1c = bool(not np.isnan(detrend_slope)
                  and abs(detrend_slope) < CLASS_NMC_SLOPE_THRESHOLD)
    if cond1a and cond1b and cond1c:
        return ("no-meaningful-change", "")

    crossings = [k for k in range(4) if z[k] * z[k + 1] < 0]
    if crossings:
        cross_k = crossings[0]
        post = abs_z[cross_k + 1:]
        if np.all(post < CLASS_BASELINE_BAND):
            return ("overshoot-then-settle", "")

    dz = np.diff(z)
    if z[0] < 0:
        mono = bool(np.all(dz > 0))
    elif z[0] > 0:
        mono = bool(np.all(dz < 0))
    else:
        mono = bool(np.all(dz == 0))

    progress = abs_z[0] - abs_z[-1]
    if mono and (progress >= CLASS_RECOVERY_PROGRESS_MONO
                 or abs_z[-1] < CLASS_BASELINE_BAND):
        return ("monotonic-recovery", "")

    if progress >= CLASS_RECOVERY_PROGRESS_STAIR:
        flat_days = np.where(np.abs(dz) < CLASS_STAIR_FLAT_DZ)[0]
        if len(flat_days) >= 1:
            non_flat = np.array([d for d in dz
                                 if abs(d) >= CLASS_STAIR_FLAT_DZ])
            if (len(non_flat) == 0
                    or (z[0] < 0 and np.all(non_flat > 0))
                    or (z[0] > 0 and np.all(non_flat < 0))):
                return ("stair-step-recovery", "")

    if abs_z[-1] < abs_z[0] and abs_z[-1] >= CLASS_BASELINE_BAND:
        return ("slow-grind-incomplete", "")

    wide_ci_days = int(np.sum(ci_half_widths > CLASS_NOISY_CI_HALFWIDTH))
    if wide_ci_days >= 3:
        return ("noisy-inconclusive", "noisy-CI-driven")
    return ("noisy-inconclusive", "noisy-shape-driven")


def recovery_completion_day(
    z_per_episode: np.ndarray, days: tuple[int, ...] = PRIMARY_WINDOW,
    *, threshold: float = RECOVERY_COMPLETION_Z_THRESHOLD,
) -> dict:
    n_ep, n_days = z_per_episode.shape
    per_ep_day = np.full(n_ep, np.nan)
    for i in range(n_ep):
        for k in range(n_days):
            v = z_per_episode[i, k]
            if not np.isnan(v) and abs(v) < threshold:
                per_ep_day[i] = days[k]
                break
    valid = per_ep_day[~np.isnan(per_ep_day)]
    n_total = int(np.sum(~np.isnan(z_per_episode[:, -1])))
    if len(valid) == 0:
        med_t5 = z_per_episode[:, -1]
        med_t5 = med_t5[~np.isnan(med_t5)]
        return {"median_day": None, "n_recovered": 0, "n_total": n_total,
                "residual_at_t5_median":
                    float(np.median(med_t5)) if len(med_t5) else float("nan")}
    return {"median_day": float(np.median(valid)),
            "n_recovered": int(len(valid)), "n_total": n_total,
            "residual_at_t5_median": float("nan")}


# === Per-cell analysis ===============================================


def _eligible_episodes(episodes: list[dict], *,
                       channel: str, phase: str) -> list[int]:
    if phase == "pooled":
        eligible = list(range(len(episodes)))
    else:
        eligible = [i for i, ep in enumerate(episodes)
                    if ep["phase"] == phase]
        if phase == "buildup":
            eligible = [
                i for i in eligible
                if episodes[i]["episode_end_t0_date"] > BUILDUP_BUFFER_LAST_EXCLUDED
            ]
    if channel == "bb_overnight_gain":
        eligible = [
            i for i in eligible
            if episodes[i]["episode_end_t0_date"] >= BB_OVERNIGHT_GAIN_START
        ]
    return eligible


def run_cell(
    df: pd.DataFrame, episodes: list[dict], dt_idx: dict[date, int],
    arm_a_matches: list[dict], *,
    channel: str, phase: str,
    baseline_arm: str, detrend_arm: str,
    window_arm: str, t0_anchor: str,
    seed_offset: int, n_boot: int, el_used: int,
    paired_stationary_diff: bool = False,
) -> dict:
    """Compute trajectory + CIs + classification for a single cell.

    v2 closure (b) — per-episode completeness_per_episode is computed and
    stored in this cell during the §4.8.1 trajectory pass; baseline-source
    is ALWAYS Arm-B μ_ch (per the v2 disambiguation in §4.8.4).

    v3 closure #4 — paired_stationary_diff=True triggers the paired-by-
    episode stationary-bootstrap CI on the per-day median DIFFERENCE
    (used for the §9 first-branch headline cell only).
    """
    days = PRIMARY_WINDOW if window_arm == "primary" else LATE_WINDOW
    eligible_eps = _eligible_episodes(episodes, channel=channel, phase=phase)

    blank_cell = {
        "channel": channel, "phase": phase,
        "baseline_arm": baseline_arm, "detrend_arm": detrend_arm,
        "window_arm": window_arm, "t0_anchor": t0_anchor,
        "el_used": int(el_used),
        "n_episodes": 0, "n_with_baseline": 0,
        "n_undefined_completeness": 0,
        "per_day_median": [float("nan")] * len(days),
        "per_day_ci_lo": [float("nan")] * len(days),
        "per_day_ci_hi": [float("nan")] * len(days),
        "per_day_diff_median": [float("nan")] * len(days),
        "per_day_diff_ci_lo": [float("nan")] * len(days),
        "per_day_diff_ci_hi": [float("nan")] * len(days),
        "z_per_episode": [],
        "raw_per_episode": [],
        "control_per_episode": [],
        "completeness_per_episode": [],
        "category": "n/a", "annotation": "no eligible episodes",
        "recovery_completion": {"median_day": None, "n_recovered": 0,
                                "n_total": 0,
                                "residual_at_t5_median": float("nan")},
        "depth_median": float("nan"),
    }
    if not eligible_eps:
        return blank_cell

    n_eps = len(eligible_eps)
    raw_per_ep = np.full((n_eps, len(days)), np.nan)
    z_per_ep = np.full((n_eps, len(days)), np.nan)
    control_per_ep = np.full((n_eps, len(days)), np.nan)
    completeness_per_ep = np.full(n_eps, np.nan)
    depth_per_ep = np.full(n_eps, np.nan)

    n_with_baseline = 0
    n_undefined_completeness = 0

    for i_local, i_ep in enumerate(eligible_eps):
        ep = episodes[i_ep]
        anchor = (ep["episode_end_t0_date"]
                  if t0_anchor == "episode_end"
                  else ep["last_below_threshold_date"])

        raw_traj = extract_trajectory(df, anchor, channel, days, dt_idx)
        raw_per_ep[i_local] = raw_traj

        # v2 closure (b): completeness_per_episode binds to Arm-B μ_ch
        # REGARDLESS of named §1.1 baseline-arm. Compute Arm-B baseline
        # for every cell so completeness threading works on Arm-A cells
        # too (the secondary correlations Spearman reads the locked cell).
        baseline = lagged_baseline_for_channel(
            df, anchor, channel, ep["phase"], dt_idx,
        )

        # z-score trajectory uses Arm-B (lagged) baseline only when the
        # cell's named baseline_arm is "arm_b" (z is the §4.8.3 classifier
        # input); for Arm-A cells the per-day median operates on raw values
        # (the §9 first-branch trigger is on the median DIFFERENCE).
        if baseline["eligible"]:
            n_with_baseline += 1
            sigma = baseline["sigma"]
            if detrend_arm == "detrend":
                dt_result = lagged_baseline_for_detrend(
                    df, anchor, channel, ep["phase"], dt_idx,
                )
                slope, intercept = dt_result["slope"], dt_result["intercept"]
                if not np.isnan(slope) and sigma > 0:
                    adjusted = apply_detrend(raw_traj, days, slope, intercept)
                    z_per_ep[i_local] = adjusted / sigma
            elif sigma > 0:
                z_per_ep[i_local] = (raw_traj - baseline["mu"]) / sigma

            valid_z = z_per_ep[i_local][~np.isnan(z_per_ep[i_local])]
            if len(valid_z) > 0:
                depth_per_ep[i_local] = float(np.max(np.abs(valid_z)))

            # v2 closure (b) per-episode completeness — primary window
            # only; per §4.5 step 7 + v2 ε-undefined rule (ε = 0.5 × σ_ch)
            if window_arm == "primary":
                ch_t0_idx = dt_idx.get(anchor)
                if ch_t0_idx is not None:
                    ch_t0 = df[channel].iat[ch_t0_idx]
                    ch_t5 = raw_traj[-1]
                    if (not pd.isna(ch_t0)) and (not np.isnan(ch_t5)):
                        denom = abs(baseline["mu"] - float(ch_t0))
                        eps = 0.5 * sigma if sigma > 0 else float("inf")
                        if denom < eps:
                            n_undefined_completeness += 1
                            completeness_per_ep[i_local] = float("nan")
                        else:
                            completeness_per_ep[i_local] = (
                                abs(float(ch_t5) - float(ch_t0)) / denom
                            )

        if baseline_arm == "arm_a":
            match = arm_a_matches[i_ep]
            if match["match_date"] is not None:
                control_per_ep[i_local] = extract_trajectory(
                    df, match["match_date"], channel, days, dt_idx,
                )

    # Per-day median + CI on z (Arm B) or raw (Arm A)
    per_day_med = np.full(len(days), np.nan)
    per_day_lo = np.full(len(days), np.nan)
    per_day_hi = np.full(len(days), np.nan)
    per_day_diff_med = np.full(len(days), np.nan)
    per_day_diff_lo = np.full(len(days), np.nan)
    per_day_diff_hi = np.full(len(days), np.nan)

    for k in range(len(days)):
        seed = RANDOM_SEED + seed_offset + k
        day_vals = (z_per_ep[:, k] if baseline_arm == "arm_b"
                    else raw_per_ep[:, k])
        med, lo, hi = per_day_median_ci(
            day_vals, n_boot=n_boot, seed=seed,
        )
        per_day_med[k] = med
        per_day_lo[k] = lo
        per_day_hi[k] = hi

    # Paired difference CI (Arm A only). v3 closure #4: the headline
    # cell uses the paired stationary-bootstrap; all other Arm-A cells
    # use the diagnostic plain paired bootstrap.
    if baseline_arm == "arm_a":
        if paired_stationary_diff:
            med_d, lo_d, hi_d = per_day_paired_stationary_diff_ci(
                raw_per_ep, control_per_ep,
                expected_block_length=el_used,
                n_boot=n_boot,
                seed=RANDOM_SEED + seed_offset + 7919,
            )
            per_day_diff_med = med_d
            per_day_diff_lo = lo_d
            per_day_diff_hi = hi_d
        else:
            for k in range(len(days)):
                seed = RANDOM_SEED + seed_offset + 7919 + k
                dmed, dlo, dhi = per_day_difference_ci(
                    raw_per_ep[:, k], control_per_ep[:, k],
                    n_boot=n_boot, seed=seed,
                )
                per_day_diff_med[k] = dmed
                per_day_diff_lo[k] = dlo
                per_day_diff_hi[k] = dhi

    # Classification (Arm-B z-trajectory only per §4.8.3)
    if baseline_arm == "arm_b":
        ci_half = (per_day_hi - per_day_lo) / 2.0
        ci_includes_zero = np.array([
            (lo <= 0 <= hi) if not (np.isnan(lo) or np.isnan(hi)) else False
            for lo, hi in zip(per_day_lo, per_day_hi)
        ])
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
        "el_used": int(el_used),
        "n_episodes": n_eps, "n_with_baseline": n_with_baseline,
        "n_undefined_completeness": int(n_undefined_completeness),
        "per_day_median": per_day_med.tolist(),
        "per_day_ci_lo": per_day_lo.tolist(),
        "per_day_ci_hi": per_day_hi.tolist(),
        "per_day_diff_median": per_day_diff_med.tolist(),
        "per_day_diff_ci_lo": per_day_diff_lo.tolist(),
        "per_day_diff_ci_hi": per_day_diff_hi.tolist(),
        "z_per_episode": z_per_ep.tolist(),
        "raw_per_episode": raw_per_ep.tolist(),
        "control_per_episode": control_per_ep.tolist(),
        "completeness_per_episode": completeness_per_ep.tolist(),
        "category": category, "annotation": annotation,
        "recovery_completion": rc,
        "depth_median": (float(np.nanmedian(depth_per_ep))
                         if np.any(~np.isnan(depth_per_ep)) else float("nan")),
    }


# === §4.8.4 secondary correlations ===================================


def secondary_correlations(
    episodes: list[dict], cells: dict, *,
    channel: str, el_used: int,
) -> dict:
    """v2 closure (b): read completeness_per_episode from the locked cell.
    Single-cell lock: pooled-LC × Arm-B × no-detrend × episode-end ×
    primary-window. (Arm-B carries the completeness; the §9-head Arm-A
    cell is for the median-difference trigger only.)
    """
    key = ("arm_b", channel, "pooled", "none", "primary", "episode_end")
    cell = cells.get(key)
    if cell is None or cell["n_episodes"] == 0:
        nan_corr = {"rho": float("nan"), "ci_lo": float("nan"),
                    "ci_hi": float("nan"), "n": 0}
        return {"rate_vs_duration": nan_corr,
                "completeness_vs_next": nan_corr,
                "n_undefined_completeness": 0}

    eligible_eps = _eligible_episodes(
        episodes, channel=channel, phase="pooled",
    )

    # next-crash-interval per episode (days from t0 to next episode start)
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
    t0_to_next[sorted_eps[-1][0]["episode_end_t0_date"]] = float("nan")

    z_arr = np.array(cell["z_per_episode"])
    completeness_arr = np.array(cell["completeness_per_episode"])
    days_idx = np.array(PRIMARY_WINDOW, dtype=float)

    rates = []
    completes = []
    durations = []
    next_intervals = []
    for i_local, i_ep in enumerate(eligible_eps):
        ep = episodes[i_ep]
        z_row = z_arr[i_local]
        valid = ~np.isnan(z_row)
        slope = (float(np.polyfit(days_idx[valid], z_row[valid], 1)[0])
                 if valid.sum() >= 3 else float("nan"))
        rates.append(slope)
        completes.append(float(completeness_arr[i_local]))
        durations.append(float(ep["duration"]))
        next_intervals.append(
            t0_to_next.get(ep["episode_end_t0_date"], float("nan"))
        )

    rate_arr = np.array(rates)
    dur_arr = np.array(durations)
    comp_arr = np.array(completes)
    next_arr = np.array(next_intervals)

    rd = spearman_block_bootstrap_ci(
        rate_arr, dur_arr, n_boot=B_CORRELATION,
        seed=RANDOM_SEED + 100001, expected_block_length=el_used,
    )
    cn = spearman_block_bootstrap_ci(
        comp_arr, next_arr, n_boot=B_CORRELATION,
        seed=RANDOM_SEED + 100002, expected_block_length=el_used,
    )
    return {"rate_vs_duration": rd, "completeness_vs_next": cn,
            "n_undefined_completeness": int(cell["n_undefined_completeness"])}


# === Sanity checks (§7 v3) ===========================================


def sanity_checks(
    df: pd.DataFrame, episodes: list[dict],
    arm_a_matches: list[dict], el_verdicts: dict,
) -> dict:
    """v3 §7 narrower-halt logic:
      - pooled n outside [25, 35] → HALT
      - bb_overnight_gain zero post-2024-09-18 → HALT
      - FAIL on Series A AND Series B for any HALT_ON_FAIL_CHANNELS → HALT
      All other verdicts proceed-ready (PASS-fallback channels and the
      pre-spec'd-FAIL-override channels do NOT halt).
    """
    fires: list[str] = []
    n_eps = len(episodes)
    if not (SANITY_N_LOW <= n_eps <= SANITY_N_HIGH):
        fires.append(
            "pooled-LC episode count %d outside [%d, %d] (Sec 7)" %
            (n_eps, SANITY_N_LOW, SANITY_N_HIGH)
        )

    bb_eps = [ep for ep in episodes
              if ep["episode_end_t0_date"] >= BB_OVERNIGHT_GAIN_START]
    if len(bb_eps) == 0:
        fires.append(
            "bb_overnight_gain has zero post-2024-09-18 episodes (Sec 7)"
        )

    # v3 closure #1 + halt-discipline: FAIL on Series A AND Series B for
    # any of the three PASS-real-expected channels halts.
    for ch in HALT_ON_FAIL_CHANNELS:
        v = el_verdicts[ch]
        if v["verdict_pooled"] == "FAIL" and v["verdict_unmedicated"] == "FAIL":
            fires.append(
                "%s FAIL on Series A AND Series B "
                "(Series A E[L]*=%.2f; Series B E[L]*=%.2f) -- v3 halt-set"
                % (ch, v["el_star_pooled"], v["el_star_unmedicated"])
            )

    per_phase_n: dict = {}
    for phase in PHASES:
        ph_eps = [ep for ep in episodes if ep["phase"] == phase]
        if phase == "buildup":
            ph_eps = [ep for ep in ph_eps
                      if ep["episode_end_t0_date"] > BUILDUP_BUFFER_LAST_EXCLUDED]
        per_phase_n[phase] = len(ph_eps)
    per_phase_n["pooled"] = n_eps

    arm_a_n = sum(1 for m in arm_a_matches if m["match_date"] is not None)
    arm_a_tols = [m["tol_used"] for m in arm_a_matches
                  if m["match_date"] is not None]

    return {
        "n_episodes": n_eps,
        "el_verdicts": el_verdicts,
        "bb_overnight_n": len(bb_eps),
        "per_phase_n": per_phase_n,
        "arm_a_n_matched": arm_a_n,
        "arm_a_tol_distribution": dict(
            zip(*np.unique(arm_a_tols, return_counts=True))
        ) if arm_a_tols else {},
        "fires": fires,
        "pass": len(fires) == 0,
    }


# === Dry-run report (Sec 10.2 v3) ====================================


def emit_dry_run_report(sc: dict, episodes: list[dict]) -> str:
    today = date.today().isoformat()
    L: list[str] = []
    L.append("# HA-P6 v3 -- dry-run report")
    L.append("")
    L.append("*Generated %s by `script.py --dry-run` per spec Sec 10.4 step 1 "
             "of the v3 LOCKED pre-registration.*" % today)
    L.append("")
    L.append("## Episode counts")
    L.append("")
    L.append("- Pooled LC-era crash_v2 episodes: **%d**" % sc["n_episodes"])
    L.append("- Per-phase episode counts (after Sec 6 buildup CPAP buffer):")
    for ph in ("pooled",) + PHASES:
        L.append("  - %s: %d" % (ph, sc["per_phase_n"][ph]))
    L.append("- bb_overnight_gain post-2024-09-18 episodes: **%d**"
             % sc["bb_overnight_n"])
    L.append("- Arm A matches (within +/- 2.0 tolerance ladder): **%d / %d**"
             % (sc["arm_a_n_matched"], sc["n_episodes"]))
    if sc["arm_a_tol_distribution"]:
        tol_str = ", ".join(
            "+/-%.1f: %d" % (k, v)
            for k, v in sc["arm_a_tol_distribution"].items()
        )
        L.append("- Arm A tolerance ladder used: %s" % tol_str)
    L.append("")

    L.append("## v3 §4.8.1 four-verdict E[L]* policy (Series A + Series B)")
    L.append("")
    L.append("| channel | verdict (A) | E[L]\\* (A pooled-LC) | verdict (B) | "
             "E[L]\\* (B unmed) | E[L] used | binds | cap | note (A) |")
    L.append("|---|---|---:|---|---:|---:|:---:|:---:|---|")
    for ch in CHANNELS:
        v = sc["el_verdicts"][ch]
        L.append("| %s | %s | %.2f | %s | %.2f | %d | %s | %s | %s |" % (
            ch, v["verdict_pooled"], v["el_star_pooled"],
            v["verdict_unmedicated"], v["el_star_unmedicated"],
            v["el_used"], v["binding_series"],
            "yes" if v["cap_binding"] else "no",
            (v["note_pooled"][:60] + "...")
            if len(v["note_pooled"]) > 63 else (v["note_pooled"] or "--"),
        ))
    L.append("")
    L.append("Series A n (pooled-LC daily non-crash days): %d; Series B n "
             "(unmedicated stratum daily non-crash days): %d." % (
                 sc["el_verdicts"][CHANNELS[0]]["n_pooled"],
                 sc["el_verdicts"][CHANNELS[0]]["n_unmedicated"],
             ))
    L.append("")

    L.append("## v3 sanity-check verdict")
    L.append("")
    if sc["fires"]:
        L.append("**HALT** -- one or more v3 sanity checks fired:")
        for f in sc["fires"]:
            L.append("- %s" % f)
        L.append("")
        L.append("Per spec Sec 10.4 step 1 + Sec 7, the spec requires "
                 "revision before the full characterisation can run. No "
                 "spec edits in this session per Sec 3.9 step 4; the "
                 "implied next step is to draft HA-P6-v4.")
    else:
        L.append("**PASS** -- all v3 Sec 7 sanity checks satisfied. "
                 "Proceeding to full run per Sec 10.4 step 2.")
        L.append("")
        L.append("v3 dispositions (proceed-ready, no halt):")
        for ch in CHANNELS:
            v = sc["el_verdicts"][ch]
            if v["verdict_pooled"] == "PASS-real":
                continue
            L.append("- %s: %s (Series A E[L]*=%.2f → E[L]_used=%d, "
                     "binds Series %s%s)" % (
                         ch, v["verdict_pooled"], v["el_star_pooled"],
                         v["el_used"], v["binding_series"],
                         "; CAP-BINDING" if v["cap_binding"] else "",
                     ))
    L.append("")
    L.append("## Episode roster")
    L.append("")
    L.append("| # | start | end | duration (d) | phase | t0 (episode-end) | "
             "t0 (last-below) |")
    L.append("|---:|---|---|---:|---|---|---|")
    for i, ep in enumerate(episodes):
        L.append("| %d | %s | %s | %d | %s | %s | %s |" % (
            i + 1, ep["start_date"], ep["end_date"], ep["duration"],
            ep["phase"], ep["episode_end_t0_date"],
            ep["last_below_threshold_date"],
        ))
    L.append("")
    return "\n".join(L) + "\n"


# === Full run ========================================================


def run_full(df: pd.DataFrame, episodes: list[dict],
             arm_a_matches: list[dict], dt_idx: dict[date, int],
             el_verdicts: dict) -> dict:
    cells: dict = {}
    seed_off = 0
    print("  computing per-cell trajectories "
          "(channel x phase x baseline x detrend x window x t0)...")
    grand_total = len(CHANNELS) * (1 + len(PHASES)) * 2 * 2 * 2 * 2
    done = 0
    for channel in CHANNELS:
        el_used = int(el_verdicts[channel]["el_used"])
        for phase in ("pooled",) + PHASES:
            for baseline_arm in ("arm_a", "arm_b"):
                for detrend_arm in ("none", "detrend"):
                    for window_arm in ("primary", "late"):
                        for t0_anchor in ("episode_end", "last_below"):
                            is_headline_arm_b = (
                                phase == "pooled"
                                and baseline_arm == "arm_b"
                                and detrend_arm == "none"
                                and window_arm == "primary"
                                and t0_anchor == "episode_end"
                            )
                            is_first_branch_arm_a = (
                                phase == "pooled"
                                and baseline_arm == "arm_a"
                                and detrend_arm == "none"
                                and window_arm == "primary"
                                and t0_anchor == "episode_end"
                            )
                            n_boot = (B_HEADLINE
                                      if (is_headline_arm_b
                                          or is_first_branch_arm_a)
                                      else B_DIAGNOSTIC)
                            cell = run_cell(
                                df, episodes, dt_idx, arm_a_matches,
                                channel=channel, phase=phase,
                                baseline_arm=baseline_arm,
                                detrend_arm=detrend_arm,
                                window_arm=window_arm,
                                t0_anchor=t0_anchor,
                                seed_offset=seed_off,
                                n_boot=n_boot, el_used=el_used,
                                paired_stationary_diff=is_first_branch_arm_a,
                            )
                            seed_off += 7
                            cells[(baseline_arm, channel, phase,
                                   detrend_arm, window_arm, t0_anchor)] = cell
                            done += 1
                            if done % 50 == 0:
                                print("    %d / %d cells"
                                      % (done, grand_total))
    print("  done: %d cells" % done)

    print("  computing §4.8.4 secondary correlations (locked cell only)...")
    sec_corr: dict = {}
    for ch in CHANNELS:
        sec_corr[ch] = secondary_correlations(
            episodes, cells, channel=ch,
            el_used=int(el_verdicts[ch]["el_used"]),
        )

    print("  evaluating §9 propagations on the locked single cell...")
    sec9 = evaluate_sec9_propagations(cells, sec_corr)
    return {"cells": cells, "secondary_correlations": sec_corr,
            "sec9_propagations": sec9}


def evaluate_sec9_propagations(cells: dict, sec_corr: dict) -> dict:
    sig_per_channel: dict[str, dict] = {}
    sig_channel_count = 0
    sig_channel_count_strict = 0
    for ch in CHANNELS:
        key = ("arm_a", ch, "pooled", "none", "primary", "episode_end")
        cell = cells.get(key)
        if cell is None or cell["n_episodes"] == 0:
            sig_per_channel[ch] = {"n_days_excl_0": 0, "n_total": 0,
                                   "distinguishable": False,
                                   "distinguishable_strict": False}
            continue
        days_excl_0 = 0
        total = 0
        for lo, hi in zip(cell["per_day_diff_ci_lo"],
                          cell["per_day_diff_ci_hi"]):
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
    arm_a_match_count = 0
    total_cell_count = 0
    for ch in CHANNELS:
        for ph in ("pooled",) + PHASES:
            key = ("arm_a", ch, ph, "none", "primary", "episode_end")
            cell = cells.get(key)
            if cell is None or cell["n_episodes"] == 0:
                continue
            total_cell_count += 1
            all_include_0 = True
            had_valid_day = False
            for lo, hi in zip(cell["per_day_diff_ci_lo"],
                              cell["per_day_diff_ci_hi"]):
                if not (np.isnan(lo) or np.isnan(hi)):
                    had_valid_day = True
                    if not (lo <= 0 <= hi):
                        all_include_0 = False
                        break
            if had_valid_day and all_include_0:
                arm_a_match_count += 1

    locked_corr = {}
    for ch in CHANNELS:
        rd = sec_corr.get(ch, {}).get("rate_vs_duration",
                                      {"ci_lo": float("nan"),
                                       "ci_hi": float("nan")})
        cn = sec_corr.get(ch, {}).get("completeness_vs_next",
                                      {"ci_lo": float("nan"),
                                       "ci_hi": float("nan")})
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
            "fires": bool(sig_channel_count >= 3),
            "fires_strict": bool(sig_channel_count_strict >= 3),
            "per_channel": sig_per_channel,
        },
        "second_branch": {
            "arm_a_match_count": int(arm_a_match_count),
            "total_cell_count": int(total_cell_count),
            "fires": bool(
                total_cell_count > 0
                and arm_a_match_count >= 0.5 * total_cell_count
            ),
        },
        "locked_correlations": locked_corr,
    }


# === Outputs =========================================================


def emit_csv(cells: dict, path: Path) -> int:
    rows = []
    for key, cell in cells.items():
        ba, ch, ph, da, wa, t0a = key
        days = PRIMARY_WINDOW if wa == "primary" else LATE_WINDOW
        for k, d in enumerate(days):
            rows.append({
                "channel": ch, "phase": ph, "baseline_arm": ba,
                "detrend_arm": da, "window_arm": wa, "t0_anchor": t0a,
                "day_offset": d, "el_used": cell["el_used"],
                "n_episodes": cell["n_episodes"],
                "n_with_baseline": cell["n_with_baseline"],
                "n_undefined_completeness": cell["n_undefined_completeness"],
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


def emit_plots(cells: dict, plots_dir: Path) -> int:
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
            key = ("arm_b", ch, ph, "none", "primary", "episode_end")
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
            for row in z:
                if np.any(~np.isnan(row)):
                    ax.plot(days, row, color="grey",
                            alpha=0.30, linewidth=0.8)
            ax.fill_between(days, lo, hi, color="C0", alpha=0.25,
                            label="95% block-bootstrap CI")
            ax.plot(days, med, color="C0", linewidth=2.0,
                    label="median z (Arm B)")
            ax.axhline(0.0, linestyle="--", color="black", linewidth=0.7)
            ax.axhline(0.5, linestyle=":", color="grey", linewidth=0.5)
            ax.axhline(-0.5, linestyle=":", color="grey", linewidth=0.5)
            ax.set_xlabel("day-offset (t = episode-end)")
            ax.set_ylabel("z vs lagged baseline")
            ax.set_title("%s x %s (n=%d; E[L]=%d)" % (
                ch, ph, cell["n_episodes"], cell["el_used"],
            ))
            ax.legend(loc="best", fontsize=8)
            fig.tight_layout()
            outpath = plots_dir / ("%s__%s.png" % (ch, ph))
            fig.savefig(outpath, dpi=120)
            plt.close(fig)
            n_plots += 1
    return n_plots


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
    L.append("# HA-P6 v3 -- result: post-crash window distinctive autonomic-recovery shape")
    L.append("")
    L.append("*Run %s by `script.py` against the v3 LOCKED pre-registration "
             "`hypothesis.md` (lock 2026-06-17). Random seed: %d; "
             "per-channel E[L] from §4.8.1 four-verdict policy "
             "(table below).*" % (today, RANDOM_SEED))
    L.append("")
    L.append("**Layer 1 descriptive characterisation per CONVENTIONS §2.1. "
             "NO SUPPORTED / NOT-SUPPORTED bar.** §5 names this result.md "
             "as reporting the *findings shape* regardless of the data; "
             "§9 enumerates downstream propagations per observation shape.")
    L.append("")

    # Headline §1.1 table
    L.append("## Headline cell (pooled LC × Arm-B lagged baseline × no-detrend × episode-end-t0 × primary [t+1, t+5])")
    L.append("")
    L.append("| channel | n eps | n w/ baseline | n undef compl | E[L] used | category | annotation | recovery day | depth (median \\|z\\|) |")
    L.append("|---|---:|---:|---:|---:|---|---|---:|---:|")
    for ch in CHANNELS:
        cell = cells[("arm_b", ch, "pooled", "none", "primary", "episode_end")]
        rc = cell["recovery_completion"]
        rc_str = ("%.1f" % rc["median_day"]) if rc["median_day"] is not None else (
            "not within window (residual %.2f)" % rc["residual_at_t5_median"]
            if not np.isnan(rc["residual_at_t5_median"]) else "n/a"
        )
        L.append("| %s | %d | %d | %d | %d | %s | %s | %s | %s |" % (
            ch, cell["n_episodes"], cell["n_with_baseline"],
            cell["n_undefined_completeness"], cell["el_used"],
            cell["category"], cell["annotation"] or "--",
            rc_str,
            "%.2f" % cell["depth_median"] if not np.isnan(cell["depth_median"]) else "--",
        ))
    L.append("")
    L.append("Per-day median z (Arm B) with 95% bootstrap CI:")
    L.append("")
    L.append("| channel | t+1 | t+2 | t+3 | t+4 | t+5 |")
    L.append("|---|---|---|---|---|---|")
    for ch in CHANNELS:
        cell = cells[("arm_b", ch, "pooled", "none", "primary", "episode_end")]
        cols = [fmt_ci(cell["per_day_median"][k],
                       cell["per_day_ci_lo"][k], cell["per_day_ci_hi"][k])
                for k in range(5)]
        L.append("| %s | %s |" % (ch, " | ".join(cols)))
    L.append("")

    # v3 §4.8.1 E[L] verdict table (§5 #2)
    L.append("## §4.8.1 four-verdict E[L] policy table (v3; §5 #2)")
    L.append("")
    L.append("| channel | verdict (A) | E[L]\\* (A pooled-LC) | verdict (B) | "
             "E[L]\\* (B unmed) | binds | E[L] used | cap-binding | rationale |")
    L.append("|---|---|---:|---|---:|:---:|---:|:---:|---|")
    for ch in CHANNELS:
        v = sc["el_verdicts"][ch]
        rationale = {
            "PASS-real": "PASS-real → project default E[L]=7",
            "PASS-fallback-degenerate":
                "PASS-fallback-degenerate (note: %s) → default E[L]=7"
                % v["note_pooled"][:40],
            "PASS-fallback-no-cutoff":
                "PASS-fallback-no-cutoff (long-dep signal) → "
                "v3 closure #2 override E[L]=14",
            "FAIL":
                ("FAIL → v3 override min(round(E[L]*), 21) "
                 "binds Series %s%s" % (v["binding_series"],
                                        "; CAP" if v["cap_binding"] else "")),
        }[v["verdict_pooled"]]
        L.append("| %s | %s | %.2f | %s | %.2f | %s | %d | %s | %s |" % (
            ch, v["verdict_pooled"], v["el_star_pooled"],
            v["verdict_unmedicated"], v["el_star_unmedicated"],
            v["binding_series"], v["el_used"],
            "yes" if v["cap_binding"] else "no", rationale,
        ))
    L.append("")

    # Arm A median-difference table + §9 first-branch trigger
    L.append("## Arm A (matched-deep-trough non-crash days) -- the strict RTM control")
    L.append("")
    L.append("**Per §8 caveat 1, this is the LOAD-BEARING read for the RTM-vs-autonomic question.** "
             "Per-day median DIFFERENCE (crash trajectory minus matched-control trajectory) with "
             "95% **paired stationary-bootstrap** CI at the per-channel E[L] (v3 closure #4):")
    L.append("")
    L.append("| channel | E[L] | t+1 diff | t+2 diff | t+3 diff | t+4 diff | t+5 diff | days CI excludes 0 |")
    L.append("|---|---:|---|---|---|---|---|---:|")
    for ch in CHANNELS:
        cell = cells[("arm_a", ch, "pooled", "none", "primary", "episode_end")]
        cols = [fmt_ci(cell["per_day_diff_median"][k],
                       cell["per_day_diff_ci_lo"][k],
                       cell["per_day_diff_ci_hi"][k])
                for k in range(5)]
        excl = sec9["first_branch"]["per_channel"][ch]
        L.append("| %s | %d | %s | %d / %d |" % (
            ch, cell["el_used"], " | ".join(cols),
            excl["n_days_excl_0"], excl["n_total"],
        ))
    L.append("")
    L.append("§9 head operational binding (>= 2 of 5 primary-window days; CI on median diff excludes 0):")
    L.append("")
    L.append("- Channels statistically-distinguishable from matched control: **%d / %d** "
             "(§9 first-branch trigger fires if >= 3)." %
             (sec9["first_branch"]["n_sig_channels"], len(CHANNELS)))
    L.append("- Strict (>= 3 of 5 days) sensitivity: **%d / %d**." %
             (sec9["first_branch"]["n_sig_channels_strict"], len(CHANNELS)))
    L.append("")

    # §4.8.4 secondary correlations
    L.append("## §4.8.4 secondary correlations (locked headline cell -- pooled-LC × Arm-B × no-detrend × episode-end × primary)")
    L.append("")
    L.append("Spearman rho with 95%% block-bootstrap CI at per-channel E[L] (day-level; "
             "see §8 v3 caveat per closure #7 on the day-level-E[L]-on-per-episode-summary "
             "granularity mismatch); B=%d:" % B_CORRELATION)
    L.append("")
    L.append("| channel | E[L] | rate vs duration: rho [95% CI] (n) | completeness vs next-interval: rho [95% CI] (n) | n undef compl |")
    L.append("|---|---:|---|---|---:|")
    for ch in CHANNELS:
        rd = sec_corr[ch]["rate_vs_duration"]
        cn = sec_corr[ch]["completeness_vs_next"]
        el = int(sc["el_verdicts"][ch]["el_used"])
        L.append("| %s | %d | %s (n=%d) | %s (n=%d) | %d |" % (
            ch, el,
            fmt_ci(rd["rho"], rd["ci_lo"], rd["ci_hi"]), rd["n"],
            fmt_ci(cn["rho"], cn["ci_lo"], cn["ci_hi"]), cn["n"],
            sec_corr[ch]["n_undefined_completeness"],
        ))
    L.append("")
    L.append("**Reading discipline per §1.2 + §4.8.4**: NO SUPPORTED bar. CI containing 0 → "
             "null correlation read; otherwise report sign + magnitude.")
    L.append("")

    # Per-phase Arm-B table
    L.append("## Per-phase tables (Arm B z-trajectory)")
    L.append("")
    L.append("| channel | phase | n eps | E[L] | category | annotation | recovery day | depth |")
    L.append("|---|---|---:|---:|---|---|---:|---:|")
    for ch in CHANNELS:
        for ph in PHASES:
            cell = cells.get(("arm_b", ch, ph, "none", "primary", "episode_end"))
            if cell is None or cell["n_episodes"] == 0:
                continue
            rc = cell["recovery_completion"]
            rc_str = ("%.1f" % rc["median_day"]) if rc["median_day"] is not None else (
                "not within window" if not np.isnan(rc["residual_at_t5_median"]) else "n/a"
            )
            L.append("| %s | %s | %d | %d | %s | %s | %s | %s |" % (
                ch, ph, cell["n_episodes"], cell["el_used"], cell["category"],
                cell["annotation"] or "--", rc_str,
                "%.2f" % cell["depth_median"] if not np.isnan(cell["depth_median"]) else "--",
            ))
    L.append("")

    # §3.7 detrend
    L.append("## §3.7 detrend sensitivity (Arm B z-trajectory, detrended)")
    L.append("")
    L.append("| channel | phase | no-detrend category | detrended category | survives? |")
    L.append("|---|---|---|---|---|")
    for ch in CHANNELS:
        for ph in ("pooled",) + PHASES:
            raw = cells.get(("arm_b", ch, ph, "none", "primary", "episode_end"))
            dt = cells.get(("arm_b", ch, ph, "detrend", "primary", "episode_end"))
            if raw is None or dt is None or raw["n_episodes"] == 0:
                continue
            survives = (raw["category"] not in
                        ("no-meaningful-change", "noisy-inconclusive")
                        and dt["category"] == raw["category"])
            L.append("| %s | %s | %s | %s | %s |" % (
                ch, ph, raw["category"], dt["category"],
                "yes" if survives else "no",
            ))
    L.append("")

    # late-recovery
    L.append("## §1.3 late-recovery sensitivity ([t+6, t+10])")
    L.append("")
    L.append("| channel | late-window category | late-window depth | late-window recovery day |")
    L.append("|---|---|---:|---:|")
    for ch in CHANNELS:
        cell = cells.get(("arm_b", ch, "pooled", "none", "late", "episode_end"))
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

    # t0-sensitivity
    L.append("## t0-sensitivity (episode-end vs last-below-threshold-day)")
    L.append("")
    L.append("| channel | episode-end category | last-below category | concordant? |")
    L.append("|---|---|---|---|")
    for ch in CHANNELS:
        a = cells.get(("arm_b", ch, "pooled", "none", "primary", "episode_end"))
        b = cells.get(("arm_b", ch, "pooled", "none", "primary", "last_below"))
        if a is None or b is None or a["n_episodes"] == 0:
            continue
        conc = "yes" if a["category"] == b["category"] else "no"
        L.append("| %s | %s | %s | %s |" % (
            ch, a["category"], b["category"], conc,
        ))
    L.append("")

    # §9 evaluation
    L.append("## §9 observation-shape propagations -- evaluation on the locked headline cell")
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
        L.append("- **§4.8.4 secondary correlations excluding 0** on the locked cell:")
        for ch, c in sig_corr:
            parts = []
            if c["rate_vs_duration_excl_0"]:
                parts.append("rate vs duration")
            if c["completeness_vs_next_excl_0"]:
                parts.append("completeness vs next-interval")
            L.append("  - %s: %s" % (ch, ", ".join(parts)))
    else:
        L.append("- **§4.8.4 secondary correlations**: all CIs include 0 on the locked cell "
                 "(null correlation read per §1.2).")
    L.append("")

    # Caveats — v1 + v2 + v3 NEW
    L.append("## Caveats per §8 (must be acknowledged on every read)")
    L.append("")
    L.append("1. **Regression to the mean (RTM) is the central confound**. The Arm A "
             "median-difference table above is the load-bearing read.")
    L.append("2. **n=29 LC-era episodes is sparse**. Per-channel per-day CIs are wide "
             "by construction.")
    L.append("3. **Power-calc dispatch**: inapplicable per Daza 2018 within-subject design "
             "+ HA-P6 is Layer 1 descriptive per CONVENTIONS §2.1.")
    L.append("4. **Crash_v2 episode boundaries depend on the t0 definition**. The "
             "t0-sensitivity table above reports concordance.")
    L.append("5. **Self-reported crash labels** via crash_v2 -- instrument-level bias "
             "inherited by §4.8.4 secondary correlations.")
    L.append("6. **Intervention-baseline dose-response broadens P6's caveat** per register "
             "caveat 5: `stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest` CONFIRMED "
             "dose-modulated; §4.7 phase-stratified arm + §3.7 detrend per phase address.")
    L.append("7. **Channel coverage gaps**: `bb_overnight_gain` starts 2024-09-18; "
             "n=%d post-2024-09-18 episodes contribute." % sc["bb_overnight_n"])
    L.append("8. **CONVENTIONS §3.7 trajectory-detrend is binding** per §4.6. The "
             "detrend-sensitivity table above is the within-phase calibration check.")
    L.append("9. **§3.4 inapplicable-to-primary by construction**: the trajectory IS "
             "computed across crash episodes; inapplicable-to-secondary because the "
             "correlation operates on per-episode summary statistics.")
    L.append("10. **Matched-baseline construction (Arm A) is operational, not gold-standard**. "
             "The ±1 gevoelscore-point tolerance ladder (±1.5, ±2) is used. Arm B "
             "(lagged baseline) is the project-pattern complement.")
    L.append("11. **Mechanistic claims about recovery physiology are out of scope** -- "
             "this characterises the *shape*; the *why* is for downstream tests.")
    L.append("")
    L.append("### v2 caveat (a) -- per-channel E[L] honest autocorrelation framing")
    L.append("")
    L.append("Per the v3 §4.8.1 four-verdict table above, FAIL-override channels and "
             "PASS-fallback-no-cutoff channels (E[L]=14) have visibly wider per-day CIs "
             "than PASS-real channels. This is the honest reporting per the methodology "
             "MD's 'robustness to non-stationarity' weighting.")
    L.append("")
    L.append("### v2 caveat (b) -- completeness baseline-source disambiguation")
    L.append("")
    L.append("The §4.8.4 completeness Spearman binds to Arm-B μ_ch regardless of the cell's "
             "named §1.1 baseline-arm. Per-episode `completeness_per_episode` is threaded "
             "from the locked Arm-B × pooled × no-detrend × episode-end × primary cell. "
             "Undefined-completeness exclusions are per-channel (per the §4.5 step 7 "
             "ε = 0.5×σ_ch rule).")
    L.append("")
    L.append("### v3 caveat (#1) -- pooled-LC stationarity contamination + Series B sensitivity arm")
    L.append("")
    L.append("The pooled-LC daily series (~4 years) crosses CPAP + Citalopram intervention "
             "transitions documented as level shifts. Series B (unmedicated stratum "
             "2022-04-04 → 2024-04-08, n=%d days) is the cleaner ACF anchor when present; "
             "the v3 §4.8.1 table above surfaces both magnitudes alongside the binding "
             "choice (A or B)." %
             sc["el_verdicts"][CHANNELS[0]]["n_unmedicated"])
    L.append("")
    L.append("### v3 caveat (#3) -- override magnitude cap at E[L]=21")
    L.append("")
    cap_channels = [ch for ch in CHANNELS
                    if sc["el_verdicts"][ch]["cap_binding"]]
    if cap_channels:
        L.append("Cap-binding channels (data-driven E[L]\\* > 21; per-day CI at the n=29-"
                 "imposed resolution floor):")
        for ch in cap_channels:
            v = sc["el_verdicts"][ch]
            L.append("- **%s**: Series A E[L]\\*=%.2f, Series B E[L]\\*=%.2f; CAP-BINDING "
                     "→ E[L]=21." %
                     (ch, v["el_star_pooled"], v["el_star_unmedicated"]))
    else:
        L.append("No cap-binding channels in this run.")
    L.append("")
    L.append("### v3 caveat (#7) -- §4.8.4 day-level-E[L]-on-per-episode-summary granularity mismatch (structural; inherited from v1; deferred to v4)")
    L.append("")
    L.append("The §4.8.4 secondary Spearman CIs use the per-channel day-level E[L] from "
             "§4.8.1 at per-episode resampling within phase, but per-episode summaries are "
             "not autocorrelated within an episode in the same way daily values are. The "
             "day-level E[L] on per-episode resampling over-conservatively widens the "
             "per-episode-summary CIs. This is a structural choice for cross-cell "
             "comparability; the per-episode-summary-aware block length alternative is "
             "deferred to a methodology MD update + a v4 absorption.")
    L.append("")

    L.append("---")
    L.append("")
    L.append("*Result emitted by `script.py` on the v3 LOCKED pre-registration. Raw "
             "result data in `result-data.json`; full multi-arm per-day-per-cell trajectory "
             "data in `result.csv`; per-channel × phase trajectory PNGs in `plots/`. Any "
             "post-result modification of the spec creates HA-P6-v4 with this v3 archived.*")
    return "\n".join(L) + "\n"


# === Main ============================================================


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Sec 10.4 step 1; emit dry-run-report.md; halt "
                             "only on v3 narrower halt-set.")
    args = parser.parse_args()

    load_env()
    print("Loading per_day_master.csv (as_of_date=%s)..." % DATA_CUT)
    df = load_master(as_of_date=str(DATA_CUT), stratum_4_only=False)
    print("  rows: %d, dates %s -> %s" %
          (len(df), df["date"].min().date(), df["date"].max().date()))
    df = df.sort_values("date").reset_index(drop=True)
    df["is_crash"] = df["is_crash"].astype(bool)
    dt_idx = date_to_idx_map(df)

    print("Detecting crash_v2 episodes via contiguous is_crash==True runs...")
    episodes = detect_episodes(df)
    print("  found %d episodes in LC era" % len(episodes))

    print("Finding Arm A matched-deep-trough non-crash controls per episode...")
    arm_a_matches = build_arm_a_match_table(df, episodes, dt_idx)
    n_arm_a = sum(1 for m in arm_a_matches if m["match_date"] is not None)
    print("  Arm A matches: %d / %d episodes" % (n_arm_a, len(episodes)))

    print("Computing v3 §4.8.1 four-verdict E[L]* policy "
          "(Series A pooled-LC + Series B unmedicated-stratum)...")
    el_verdicts = compute_el_verdicts(df)
    for ch in CHANNELS:
        v = el_verdicts[ch]
        print("    %-44s A: %s E[L]*=%.2f | B: %s E[L]*=%.2f | used=%d (%s%s)" % (
            ch, v["verdict_pooled"], v["el_star_pooled"],
            v["verdict_unmedicated"], v["el_star_unmedicated"],
            v["el_used"], v["binding_series"],
            ", CAP" if v["cap_binding"] else "",
        ))

    print("Running v3 §7 sanity checks (narrower halt-set)...")
    sc = sanity_checks(df, episodes, arm_a_matches, el_verdicts)
    print("  sanity verdict: %s" % ("PASS" if sc["pass"] else "HALT"))
    if sc["fires"]:
        for f in sc["fires"]:
            print("    - %s" % f)

    OUT_DRY_RUN.write_text(emit_dry_run_report(sc, episodes), encoding="utf-8")
    print("Wrote %s" % OUT_DRY_RUN)

    if args.dry_run:
        return 0 if sc["pass"] else 1

    if not sc["pass"]:
        print("Sanity check failed (v3 §7 / §10.4 step 1). Halting before "
              "full run; no spec edits per §3.9 step 4.")
        return 1

    print("")
    print("Running full v3 characterisation...")
    results = run_full(df, episodes, arm_a_matches, dt_idx, el_verdicts)
    results["sanity_checks"] = sc

    # JSON output
    json_safe_cells = {}
    for key, cell in results["cells"].items():
        skey = "|".join(key)
        slim = {k: v for k, v in cell.items()
                if k not in ("z_per_episode", "raw_per_episode",
                             "control_per_episode")}
        json_safe_cells[skey] = slim
    json_payload = {
        "seed": RANDOM_SEED,
        "e_block_default": E_BLOCK_DEFAULT,
        "e_block_no_cutoff": E_BLOCK_NO_CUTOFF,
        "e_block_override_cap": E_BLOCK_OVERRIDE_CAP,
        "n_boot_headline": B_HEADLINE,
        "n_boot_diagnostic": B_DIAGNOSTIC,
        "n_boot_correlation": B_CORRELATION,
        "episode_count": len(episodes),
        "arm_a_match_count": n_arm_a,
        "el_verdicts": el_verdicts,
        "cells": json_safe_cells,
        "secondary_correlations": results["secondary_correlations"],
        "sec9_propagations": results["sec9_propagations"],
        "sanity_checks": {
            "n_episodes": sc["n_episodes"],
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
