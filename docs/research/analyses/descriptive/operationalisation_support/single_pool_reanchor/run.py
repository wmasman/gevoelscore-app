"""R14 single-pool re-anchor descriptive cross-check.

Executes the binding recipe at
``methodology/train_validate_split_fate.md`` Sec 5.7: for each in-scope
HA, re-runs the locked operand on the full Stratum 4 single pool
(2022-09-03 to 2026-06-05; standard day-validity gates per
``lc_era_temporal_segmentation.md``) and compares the single-pool
verdict to the locked era-split verdict.

This is descriptive cross-check ONLY. Locked HA result.md files remain
unchanged per Sec 5.7 bullets 6-8. Train-vs-validate divergence reported
as a number, not a narrative. No framework is pre-committed as correct.

Run from repo root:

    python docs/research/analyses/descriptive/operationalisation_support/single_pool_reanchor/run.py

Outputs:
    findings.md (the writeup)
    result-data.json (machine-readable; gitignored per docs/research/**/*.json rule)
"""
from __future__ import annotations

import json
import os
import random
import statistics
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
UTILS_DIR = HERE.parents[2] / "_utils"
sys.path.insert(0, str(UTILS_DIR))

from inference import (  # noqa: E402
    compute_data_driven_block_length,
    permutation_pvalue,
    stationary_bootstrap_ci,
)


# -----------------------------------------------------------------------------
# Constants per the methodology MDs
# -----------------------------------------------------------------------------

STRATUM_4_START = date(2022, 9, 3)
AS_OF_DATE = date(2026, 6, 5)

DEFAULT_EL = 7  # permutation_null_block_length.md default
N_BOOTSTRAP = 10_000
SEED = 20260624  # per handoff Sec 2.4
NULL_SAMPLE_SIZE = 200

# Locked per-HA pre-reg criteria (all share the same shape)
CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15
# Crit C magnitude floor differs per HA (median |z| >= N_std / 2)

# Per-HA seed (kept the same as the legacy pre-regs to match operand)
LEGACY_NULL_SEED = 20260605

# z-score threshold (locked at N_std = 1.5 for the primary)
N_STD_PRIMARY = 1.5

# Lead-up windows (4-day primary)
LEADUP_DAYS = 4

# Baseline window (per Theme A lagged baseline)
BASELINE_WINDOW_END_OFFSET = 30   # baseline ends 30 days before d
BASELINE_WINDOW_START_OFFSET = 90  # baseline starts 90 days before d
BASELINE_MIN_VALID = 40           # min valid prior days

# Per-HA min lead-up validity
MIN_LEADUP_VALID = 3              # 3 of 4 days


# -----------------------------------------------------------------------------
# Data loaders
# -----------------------------------------------------------------------------


def _resolve_data_root() -> Path:
    """Resolve gevoelscore data path; default to known location."""
    raw = os.environ.get("GEVOELSCORE_DATA_PATH", "")
    if not raw:
        # Default per CONVENTIONS Sec 5
        raw = r"C:\Users\Gebruiker\Documents\gevoelscore-data"
    root = Path(raw)
    if not root.exists():
        raise RuntimeError(f"data root {raw!r} does not exist")
    return root


def load_master() -> pd.DataFrame:
    root = _resolve_data_root()
    path = root / "unified" / "per_day_master.csv"
    df = pd.read_csv(path, parse_dates=["date"], low_memory=False)
    df["date"] = df["date"].dt.date
    df = df[(df["date"] >= STRATUM_4_START) & (df["date"] <= AS_OF_DATE)].copy()
    df = df.sort_values("date").reset_index(drop=True)
    return df


def load_crash_episodes() -> list[date]:
    """Return sorted unique crash episode start dates within Stratum 4 single pool."""
    root = _resolve_data_root()
    path = root / "processed" / "crash_labels" / "labels_crash_v2.csv"
    df = pd.read_csv(path, parse_dates=["date", "episode_start"])
    crashes = df[df["label"] == "crash"].dropna(subset=["episode_start"]).copy()
    crashes["episode_start"] = crashes["episode_start"].dt.date
    starts = sorted(set(crashes["episode_start"]))
    starts = [d for d in starts if STRATUM_4_START <= d <= AS_OF_DATE]
    return starts


# -----------------------------------------------------------------------------
# Generic per-HA window evaluation
# -----------------------------------------------------------------------------


def compute_lagged_baseline(
    series: pd.Series,
    dates: pd.Series,
    target_date: date,
    *,
    sigma_floor: float,
) -> tuple[float | None, float | None]:
    """Trimmed-mean (10/90) + std on [d-90, d-30] window.

    Returns (mu, sigma) or (None, None) if not computable.
    """
    end_d = target_date - timedelta(days=BASELINE_WINDOW_END_OFFSET)
    start_d = target_date - timedelta(days=BASELINE_WINDOW_START_OFFSET)
    mask = (dates >= start_d) & (dates <= end_d)
    window_vals = series[mask].dropna().to_numpy(dtype=float)
    if len(window_vals) < BASELINE_MIN_VALID:
        return None, None
    sorted_vals = np.sort(window_vals)
    cut_lo = int(len(sorted_vals) * 0.10)
    cut_hi = int(len(sorted_vals) * 0.90)
    if cut_hi <= cut_lo:
        return None, None
    trimmed = sorted_vals[cut_lo:cut_hi]
    if len(trimmed) < 2:
        return None, None
    mu = float(np.mean(trimmed))
    sigma = float(np.std(trimmed, ddof=1))
    if sigma <= sigma_floor:
        return None, None
    return mu, sigma


def episode_max_signed_z(
    ref_date: date,
    df_indexed: pd.DataFrame,
    column: str,
    *,
    sigma_floor: float,
    leadup_days: int = LEADUP_DAYS,
    min_valid: int = MIN_LEADUP_VALID,
) -> tuple[float | None, int]:
    """Compute max signed z over the leadup window relative to lagged baseline.

    Returns (max_signed_z, n_valid_days) or (None, n_valid) if cannot.
    """
    leadup_dates = [ref_date - timedelta(days=i) for i in range(1, leadup_days + 1)]
    series_all = df_indexed[column]
    dates_all = df_indexed["date"]
    date_to_idx = df_indexed.attrs["date_to_idx"]
    z_values = []
    n_valid = 0
    for d in leadup_dates:
        if d not in date_to_idx:
            continue
        target_val = series_all.iloc[date_to_idx[d]]
        if pd.isna(target_val):
            continue
        n_valid += 1
        mu, sigma = compute_lagged_baseline(series_all, dates_all, d, sigma_floor=sigma_floor)
        if mu is None or sigma is None:
            continue
        z_values.append(float((float(target_val) - mu) / sigma))
    if n_valid < min_valid or len(z_values) < min_valid:
        return None, n_valid
    return max(z_values), n_valid


def episode_max_abs_z(
    ref_date: date,
    df_indexed: pd.DataFrame,
    column: str,
    *,
    sigma_floor: float,
    leadup_days: int = LEADUP_DAYS,
    min_valid: int = MIN_LEADUP_VALID,
) -> tuple[float | None, int, list[float]]:
    """Compute max |z| + signed z list over leadup."""
    leadup_dates = [ref_date - timedelta(days=i) for i in range(1, leadup_days + 1)]
    series_all = df_indexed[column]
    dates_all = df_indexed["date"]
    date_to_idx = df_indexed.attrs["date_to_idx"]
    z_values: list[float] = []
    n_valid = 0
    for d in leadup_dates:
        if d not in date_to_idx:
            continue
        target_val = series_all.iloc[date_to_idx[d]]
        if pd.isna(target_val):
            continue
        n_valid += 1
        mu, sigma = compute_lagged_baseline(series_all, dates_all, d, sigma_floor=sigma_floor)
        if mu is None or sigma is None:
            continue
        z_values.append(float((float(target_val) - mu) / sigma))
    if n_valid < min_valid or len(z_values) < min_valid:
        return None, n_valid, []
    return max(abs(z) for z in z_values), n_valid, z_values


def episode_max_delta_dod_z(
    ref_date: date,
    df_indexed: pd.DataFrame,
    column: str,
    *,
    sigma_floor: float,
    leadup_days: int = LEADUP_DAYS,
    min_valid: int = MIN_LEADUP_VALID,
) -> tuple[float | None, int, list[float], float | None]:
    """For HA07c/HA07d/HA08c-style: per-night delta = X[d] - X[d-1], z against lagged baseline of deltas.

    Returns (max_signed_z, n_valid, signed_z_list, max_abs_z).
    """
    leadup_dates = [ref_date - timedelta(days=i) for i in range(1, leadup_days + 1)]
    series_all = df_indexed[column]
    dates_all = df_indexed["date"]
    date_to_idx = df_indexed.attrs["date_to_idx"]
    # Build delta_dod series over the whole frame for baseline computation.
    delta_cache = df_indexed.attrs["_delta_cache"]
    if column not in delta_cache:
        col_arr = series_all.to_numpy(dtype=float)
        dates_arr = list(dates_all)
        deltas = [np.nan] * len(col_arr)
        for i in range(1, len(col_arr)):
            if (dates_arr[i] - dates_arr[i - 1]).days == 1:
                if not (np.isnan(col_arr[i]) or np.isnan(col_arr[i - 1])):
                    deltas[i] = float(col_arr[i] - col_arr[i - 1])
        delta_series = pd.Series(deltas, name=f"{column}_delta_dod")
        delta_cache[column] = delta_series
    delta_series = delta_cache[column]
    z_values: list[float] = []
    n_valid = 0
    for d in leadup_dates:
        if d not in date_to_idx:
            continue
        idx = date_to_idx[d]
        target_delta = delta_series.iloc[idx]
        if pd.isna(target_delta):
            continue
        n_valid += 1
        mu, sigma = compute_lagged_baseline(delta_series, dates_all, d, sigma_floor=sigma_floor)
        if mu is None or sigma is None:
            continue
        z_values.append(float((float(target_delta) - mu) / sigma))
    if n_valid < min_valid or len(z_values) < min_valid:
        return None, n_valid, [], None
    return max(z_values), n_valid, z_values, max(abs(z) for z in z_values)


def episode_max_slope_z(
    ref_date: date,
    df_indexed: pd.DataFrame,
    column: str,
    *,
    sigma_floor: float,
    slope_window: int = 5,
    leadup_days: int = LEADUP_DAYS,
    min_valid: int = MIN_LEADUP_VALID,
) -> tuple[float | None, int, list[float]]:
    """For HA08c-style: per-day trailing-5d OLS slope of X, z against lagged baseline of slopes."""
    series_all = df_indexed[column]
    dates_all = df_indexed["date"]
    date_to_idx = df_indexed.attrs["date_to_idx"]
    slope_cache = df_indexed.attrs["_slope_cache"]
    key = (column, slope_window)
    if key not in slope_cache:
        col_arr = series_all.to_numpy(dtype=float)
        dates_arr = list(dates_all)
        slopes = [np.nan] * len(col_arr)
        for i in range(len(col_arr)):
            if i < slope_window - 1:
                continue
            ys = col_arr[i - slope_window + 1 : i + 1]
            valid_mask = ~np.isnan(ys)
            if valid_mask.sum() < 4:  # require 4 of 5 days
                continue
            xs = np.arange(slope_window)[valid_mask]
            ys_v = ys[valid_mask]
            # check contiguity 5d
            if (dates_arr[i] - dates_arr[i - slope_window + 1]).days != slope_window - 1:
                continue
            n = len(xs)
            if n < 2:
                continue
            xs_mean = xs.mean()
            ys_mean = ys_v.mean()
            num = float(((xs - xs_mean) * (ys_v - ys_mean)).sum())
            den = float(((xs - xs_mean) ** 2).sum())
            if den == 0:
                continue
            slopes[i] = num / den
        slope_cache[key] = pd.Series(slopes, name=f"{column}_slope_{slope_window}d")
    slope_series = slope_cache[key]
    leadup_dates = [ref_date - timedelta(days=i) for i in range(1, leadup_days + 1)]
    z_values: list[float] = []
    n_valid = 0
    for d in leadup_dates:
        if d not in date_to_idx:
            continue
        idx = date_to_idx[d]
        target_slope = slope_series.iloc[idx]
        if pd.isna(target_slope):
            continue
        n_valid += 1
        mu, sigma = compute_lagged_baseline(slope_series, dates_all, d, sigma_floor=sigma_floor)
        if mu is None or sigma is None:
            continue
        z_values.append(float((float(target_slope) - mu) / sigma))
    if n_valid < min_valid or len(z_values) < min_valid:
        return None, n_valid, []
    return max(z_values), n_valid, z_values


def episode_h02b_max_delta(
    ref_date: date,
    df_indexed: pd.DataFrame,
    column: str,
    *,
    baseline_threshold: float = 10.0,
    leadup_days: int = 3,
    sigma_floor: float = 0.0,
    min_valid: int = 2,
) -> tuple[float | None, int]:
    """H02b: max(max_spike_minutes - baseline) over 3-day leadup; trigger if >= 10."""
    series_all = df_indexed[column]
    dates_all = df_indexed["date"]
    date_to_idx = df_indexed.attrs["date_to_idx"]
    leadup_dates = [ref_date - timedelta(days=i) for i in range(1, leadup_days + 1)]
    deltas = []
    n_valid = 0
    for d in leadup_dates:
        if d not in date_to_idx:
            continue
        target_val = series_all.iloc[date_to_idx[d]]
        if pd.isna(target_val):
            continue
        n_valid += 1
        # Baseline: trimmed mean of column over [d-90, d-30]
        mu, _sigma = compute_lagged_baseline(series_all, dates_all, d, sigma_floor=sigma_floor)
        if mu is None:
            continue
        deltas.append(float(target_val) - mu)
    if n_valid < min_valid or len(deltas) < min_valid:
        return None, n_valid
    return max(deltas), n_valid


def episode_h01_h04_delta(
    ref_date: date,
    df_indexed: pd.DataFrame,
    column: str,
    *,
    leadup_days: int = 7,
    sigma_floor: float = 0.0,
) -> tuple[float | None, int]:
    """H01/H04-style: mean of column over 7-day lead-up minus trimmed baseline."""
    series_all = df_indexed[column]
    dates_all = df_indexed["date"]
    date_to_idx = df_indexed.attrs["date_to_idx"]
    leadup_dates = [ref_date - timedelta(days=i) for i in range(1, leadup_days + 1)]
    leadup_vals = []
    for d in leadup_dates:
        if d not in date_to_idx:
            continue
        target_val = series_all.iloc[date_to_idx[d]]
        if pd.isna(target_val):
            continue
        leadup_vals.append(float(target_val))
    if len(leadup_vals) < leadup_days * 0.5:
        return None, len(leadup_vals)
    # Baseline ends 7 days before ref, window 90d
    end_d = ref_date - timedelta(days=leadup_days + 1)
    start_d = ref_date - timedelta(days=leadup_days + 90)
    mask = (dates_all >= start_d) & (dates_all <= end_d)
    baseline_vals = series_all[mask].dropna().to_numpy(dtype=float)
    if len(baseline_vals) < 40:
        return None, len(leadup_vals)
    sorted_vals = np.sort(baseline_vals)
    cut_lo = int(len(sorted_vals) * 0.10)
    cut_hi = int(len(sorted_vals) * 0.90)
    if cut_hi <= cut_lo:
        return None, len(leadup_vals)
    trimmed = sorted_vals[cut_lo:cut_hi]
    if len(trimmed) < 2:
        return None, len(leadup_vals)
    baseline = float(np.mean(trimmed))
    return float(np.mean(leadup_vals) - baseline), len(leadup_vals)


def episode_ha01b_n_shock(
    ref_date: date,
    df_indexed: pd.DataFrame,
    *,
    leadup_days: int = LEADUP_DAYS,
    min_valid: int = 2,
) -> tuple[int | None, int]:
    """HA01b-recomputed: n days in 4-day lead-up where exertion_class_lagged in {heavy, very_heavy}."""
    series_all = df_indexed["exertion_class_lagged"]
    date_to_idx = df_indexed.attrs["date_to_idx"]
    leadup_dates = [ref_date - timedelta(days=i) for i in range(1, leadup_days + 1)]
    n_shock = 0
    n_valid = 0
    for d in leadup_dates:
        if d not in date_to_idx:
            continue
        cls = series_all.iloc[date_to_idx[d]]
        if pd.isna(cls) or cls in (None, "", "None"):
            continue
        n_valid += 1
        if str(cls) in {"heavy", "very_heavy"}:
            n_shock += 1
    if n_valid < min_valid:
        return None, n_valid
    return n_shock, n_valid


def episode_ha01c_rank_trigger(
    ref_date: date,
    df_indexed: pd.DataFrame,
    *,
    rank_col: str = "eff_exertion_rank_lagged",
    rank_threshold: float = 0.75,
    leadup_days: int = LEADUP_DAYS,
    min_valid: int = MIN_LEADUP_VALID,
) -> tuple[bool | None, float | None, int]:
    """HA01c: episode triggers if >=1 day in 4-day lead-up has eff_exertion_rank_lagged >= 0.75.

    Returns (triggered, max_rank_on_leadup, n_valid). triggered is None if
    fewer than ``min_valid`` (3 of 4) lead-up days carry a valid rank in [0, 1].
    The max_rank is used to compute crit_c (median rank on triggering episodes
    >= 0.875) on the triggering subset, matching the locked HA01c bar (c).
    """
    series_all = df_indexed[rank_col]
    date_to_idx = df_indexed.attrs["date_to_idx"]
    leadup_dates = [ref_date - timedelta(days=i) for i in range(1, leadup_days + 1)]
    ranks = []
    n_valid = 0
    for d in leadup_dates:
        if d not in date_to_idx:
            continue
        val = series_all.iloc[date_to_idx[d]]
        if pd.isna(val):
            continue
        v = float(val)
        if not (0.0 <= v <= 1.0):
            continue
        n_valid += 1
        ranks.append(v)
    if n_valid < min_valid or not ranks:
        return None, None, n_valid
    max_rank = max(ranks)
    triggered = max_rank >= rank_threshold
    return triggered, max_rank, n_valid


def episode_h03_efficiency_delta(
    ref_date: date,
    df_indexed: pd.DataFrame,
    *,
    leadup_days: int = 7,
    baseline_window_days: int = 90,
    min_leadup_valid: int = 5,
    min_baseline_valid: int = 30,
    trim_pct: float = 0.10,
) -> tuple[float | None, int]:
    """H03: delta sleep efficiency = mean(leadup eff) - trimmed_mean(baseline eff).

    Sleep efficiency is reconstructed from per_day_master columns as
    TST / (TST + awake + unmeasurable), where TST = sleep_deep_min +
    sleep_light_min. Per DATA_DICTIONARY.md the FR245 hardware does NOT
    classify REM (no sleep_rem_min exists); all non-deep / non-awake sleep
    aggregates into sleep_light_min, so (deep + light) is construction-
    equivalent to the locked test's (deep + light + rem). 7-night leadup,
    [d-97, d-8] trimmed baseline (10/90), min 5/7 leadup + min 30 baseline.

    Returns (delta_eff, n_leadup_valid) or (None, n_leadup_valid).
    """
    eff_series = df_indexed.attrs["_eff_cache"]
    dates_all = df_indexed["date"]
    date_to_idx = df_indexed.attrs["date_to_idx"]

    leadup_dates = [ref_date - timedelta(days=i) for i in range(1, leadup_days + 1)]
    leadup_vals = []
    for d in leadup_dates:
        if d not in date_to_idx:
            continue
        v = eff_series.iloc[date_to_idx[d]]
        if pd.isna(v):
            continue
        leadup_vals.append(float(v))
    if len(leadup_vals) < min_leadup_valid:
        return None, len(leadup_vals)

    baseline_end = ref_date - timedelta(days=leadup_days + 1)
    baseline_start = ref_date - timedelta(days=leadup_days + baseline_window_days)
    mask = (dates_all >= baseline_start) & (dates_all <= baseline_end)
    baseline_vals = eff_series[mask].dropna().to_numpy(dtype=float)
    if len(baseline_vals) < min_baseline_valid:
        return None, len(leadup_vals)
    sorted_vals = np.sort(baseline_vals)
    trim = int(len(sorted_vals) * trim_pct)
    if len(sorted_vals) - 2 * trim < 1:
        trimmed = sorted_vals
    else:
        trimmed = sorted_vals[trim: len(sorted_vals) - trim]
    if len(trimmed) < 1:
        return None, len(leadup_vals)
    baseline = float(np.mean(trimmed))
    leadup_mean = float(np.mean(leadup_vals))
    return float(leadup_mean - baseline), len(leadup_vals)


# -----------------------------------------------------------------------------
# Null sample construction (matches the locked HA pattern)
# -----------------------------------------------------------------------------


def build_null_dates(
    df_indexed: pd.DataFrame,
    crash_starts: list[date],
    *,
    leadup_days: int,
    n_samples: int = NULL_SAMPLE_SIZE,
    seed: int = LEGACY_NULL_SEED,
) -> list[date]:
    """Random non-overlapping reference dates. Each is a candidate ref dispatched into the HA evaluator."""
    rng = random.Random(seed)
    occupied: set[date] = set()
    for ref in crash_starts:
        for i in range(1, leadup_days + 1):
            occupied.add(ref - timedelta(days=i))
    all_dates = list(df_indexed["date"])
    all_dates = [d for d in all_dates if (d - STRATUM_4_START).days >= 100]
    out = []
    attempts = 0
    while len(out) < n_samples and attempts < 100_000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, leadup_days + 1)}
        if leadup & occupied:
            continue
        out.append(ref)
        # Mark this ref's leadup occupied so subsequent picks don't overlap
        for d in leadup:
            occupied.add(d)
    return out


# -----------------------------------------------------------------------------
# Per-HA single-pool evaluation
# -----------------------------------------------------------------------------


def _index_master(df: pd.DataFrame) -> pd.DataFrame:
    """Add helper attrs for fast lookup.

    Returns the input DataFrame with attached attrs:
      - df.attrs["date_set"] : set of date objects for O(1) membership tests
      - df.attrs["date_to_idx"] : dict[date -> int row index] for O(1) row lookup
      - df.attrs["_delta_cache"] : dict (lazily populated by per-HA evaluators)
      - df.attrs["_slope_cache"] : dict (lazily populated by per-HA evaluators)
    """
    df = df.copy()
    df.attrs["date_set"] = set(df["date"])
    df.attrs["date_to_idx"] = {d: i for i, d in enumerate(df["date"])}
    df.attrs["_delta_cache"] = {}
    df.attrs["_slope_cache"] = {}
    # H03 sleep-efficiency reconstruction from per_day_master columns.
    # TST = deep + light (no REM on FR245 per DATA_DICTIONARY.md);
    # efficiency = TST / (TST + awake + unmeasurable). NaN when any
    # component is missing or the denominator is non-positive.
    deep = df["sleep_deep_min"].astype(float) if "sleep_deep_min" in df.columns else pd.Series([np.nan] * len(df))
    light = df["sleep_light_min"].astype(float) if "sleep_light_min" in df.columns else pd.Series([np.nan] * len(df))
    awake = df["sleep_awake_min"].astype(float) if "sleep_awake_min" in df.columns else pd.Series([np.nan] * len(df))
    unmeas = df["sleep_unmeasurable_min"].astype(float) if "sleep_unmeasurable_min" in df.columns else pd.Series([np.nan] * len(df))
    tst = deep + light
    tib_like = tst + awake + unmeas
    eff = tst / tib_like
    eff = eff.where(tib_like > 0)
    df.attrs["_eff_cache"] = eff.reset_index(drop=True)
    return df


def _build_trigger_arrays_z_signed(
    ref_dates: list[date],
    df_indexed: pd.DataFrame,
    column: str,
    *,
    sigma_floor: float,
    n_std: float = N_STD_PRIMARY,
    leadup_days: int = LEADUP_DAYS,
    min_valid: int = MIN_LEADUP_VALID,
) -> tuple[np.ndarray, list[float], int]:
    """Trigger if max signed z >= n_std (one-sided elevated)."""
    triggers = []
    medians = []
    n_skipped = 0
    for ref in ref_dates:
        max_z, _n_valid = episode_max_signed_z(
            ref, df_indexed, column, sigma_floor=sigma_floor,
            leadup_days=leadup_days, min_valid=min_valid,
        )
        if max_z is None:
            triggers.append(np.nan)
            n_skipped += 1
            continue
        triggers.append(1 if max_z >= n_std else 0)
        medians.append(max_z)
    return np.array(triggers, dtype=float), medians, n_skipped


def _build_trigger_arrays_z_abs(
    ref_dates: list[date],
    df_indexed: pd.DataFrame,
    column: str,
    *,
    sigma_floor: float,
    n_std: float = N_STD_PRIMARY,
    leadup_days: int = LEADUP_DAYS,
    min_valid: int = MIN_LEADUP_VALID,
) -> tuple[np.ndarray, list[float], int]:
    """Trigger if max |z| >= n_std (bidirectional)."""
    triggers = []
    medians = []
    n_skipped = 0
    for ref in ref_dates:
        max_abs_z, _n_valid, _ = episode_max_abs_z(
            ref, df_indexed, column, sigma_floor=sigma_floor,
            leadup_days=leadup_days, min_valid=min_valid,
        )
        if max_abs_z is None:
            triggers.append(np.nan)
            n_skipped += 1
            continue
        triggers.append(1 if max_abs_z >= n_std else 0)
        medians.append(max_abs_z)
    return np.array(triggers, dtype=float), medians, n_skipped


def _build_trigger_arrays_delta_signed(
    ref_dates: list[date],
    df_indexed: pd.DataFrame,
    column: str,
    *,
    sigma_floor: float,
    n_std: float = N_STD_PRIMARY,
    leadup_days: int = LEADUP_DAYS,
    min_valid: int = MIN_LEADUP_VALID,
) -> tuple[np.ndarray, list[float], int]:
    triggers = []
    medians = []
    n_skipped = 0
    for ref in ref_dates:
        max_z, _n_valid, _zs, _abs = episode_max_delta_dod_z(
            ref, df_indexed, column, sigma_floor=sigma_floor,
            leadup_days=leadup_days, min_valid=min_valid,
        )
        if max_z is None:
            triggers.append(np.nan)
            n_skipped += 1
            continue
        triggers.append(1 if max_z >= n_std else 0)
        medians.append(max_z)
    return np.array(triggers, dtype=float), medians, n_skipped


def _build_trigger_arrays_delta_abs(
    ref_dates: list[date],
    df_indexed: pd.DataFrame,
    column: str,
    *,
    sigma_floor: float,
    n_std: float = N_STD_PRIMARY,
    leadup_days: int = LEADUP_DAYS,
    min_valid: int = MIN_LEADUP_VALID,
) -> tuple[np.ndarray, list[float], int]:
    triggers = []
    medians = []
    n_skipped = 0
    for ref in ref_dates:
        _max_signed, _n_valid, _zs, max_abs = episode_max_delta_dod_z(
            ref, df_indexed, column, sigma_floor=sigma_floor,
            leadup_days=leadup_days, min_valid=min_valid,
        )
        if max_abs is None:
            triggers.append(np.nan)
            n_skipped += 1
            continue
        triggers.append(1 if max_abs >= n_std else 0)
        medians.append(max_abs)
    return np.array(triggers, dtype=float), medians, n_skipped


def _build_trigger_arrays_slope_signed(
    ref_dates: list[date],
    df_indexed: pd.DataFrame,
    column: str,
    *,
    sigma_floor: float,
    n_std: float = N_STD_PRIMARY,
    leadup_days: int = LEADUP_DAYS,
    min_valid: int = MIN_LEADUP_VALID,
) -> tuple[np.ndarray, list[float], int]:
    triggers = []
    medians = []
    n_skipped = 0
    for ref in ref_dates:
        max_z, _n_valid, _ = episode_max_slope_z(
            ref, df_indexed, column, sigma_floor=sigma_floor,
            leadup_days=leadup_days, min_valid=min_valid,
        )
        if max_z is None:
            triggers.append(np.nan)
            n_skipped += 1
            continue
        triggers.append(1 if max_z >= n_std else 0)
        medians.append(max_z)
    return np.array(triggers, dtype=float), medians, n_skipped


# -----------------------------------------------------------------------------
# Block-permutation + bootstrap CI on the discrimination statistic
# -----------------------------------------------------------------------------


def discrimination_stat(crash_triggers: np.ndarray, null_triggers: np.ndarray) -> float:
    """Discrimination in percentage points = (frac_crash - frac_null) * 100."""
    crash = crash_triggers[~np.isnan(crash_triggers)]
    null = null_triggers[~np.isnan(null_triggers)]
    if len(crash) == 0 or len(null) == 0:
        return float("nan")
    return float((crash.mean() - null.mean()) * 100.0)


def evaluate_ha(
    label: str,
    crash_triggers: np.ndarray,
    null_triggers: np.ndarray,
    medians: list[float],
    n_std: float,
    *,
    direction: str = "greater",
    rng_seed: int = SEED,
) -> dict:
    """Common evaluation pipeline for one HA on the single pool.

    Returns dict with frac_crash, frac_null, disc_pp, median_max_z,
    crit_a/b/c, single-pool verdict, perm p-value, CI on disc_pp.
    """
    crash = crash_triggers[~np.isnan(crash_triggers)]
    null = null_triggers[~np.isnan(null_triggers)]
    n_crash_clean = int(len(crash))
    n_null_clean = int(len(null))
    if n_crash_clean < 10:
        return {
            "label": label,
            "verdict_single_pool": "INCONCLUSIVE (n_crash_clean < 10)",
            "n_crash_clean": n_crash_clean,
            "n_null_clean": n_null_clean,
        }
    frac_crash = float(crash.mean())
    frac_null = float(null.mean())
    disc_pp = float((frac_crash - frac_null) * 100.0)
    if direction == "greater":
        median_val = float(np.median(medians)) if medians else float("nan")
    else:
        median_val = float(np.median([abs(m) for m in medians])) if medians else float("nan")
    # Permutation p-value on the discrimination statistic at the per-event level
    perm = permutation_pvalue(
        crash, null,
        statistic=lambda c, n: float((c.mean() - n.mean()) * 100.0),
        n_permutations=N_BOOTSTRAP,
        alternative="greater",
        random_state=rng_seed,
    )
    # Stationary bootstrap CI on the discrimination
    pooled = np.concatenate([crash, null])
    n_crash_arr = len(crash)
    def disc_from_pooled(arr):
        c = arr[:n_crash_arr]
        nl = arr[n_crash_arr:]
        if len(c) == 0 or len(nl) == 0:
            return 0.0
        return float((c.mean() - nl.mean()) * 100.0)
    ci_result = stationary_bootstrap_ci(
        pooled, disc_from_pooled,
        n_bootstrap=N_BOOTSTRAP, expected_block_length=DEFAULT_EL,
        confidence_level=0.95, random_state=rng_seed,
    )
    # Pre-reg criteria evaluation
    crit_a = frac_crash >= CRIT_A_FRAC
    crit_b = disc_pp >= CRIT_B_DISC_PP
    crit_c = median_val >= (n_std / 2.0)
    verdict = "SUPPORTED" if (crit_a and crit_b and crit_c) else "NOT-SUPPORTED"
    return {
        "label": label,
        "n_crash_clean": n_crash_clean,
        "n_null_clean": n_null_clean,
        "frac_crash": frac_crash,
        "frac_null": frac_null,
        "disc_pp": disc_pp,
        "median_max_z_or_signed": median_val,
        "perm_pvalue_greater_E_L_7": float(perm["p_value"]),
        "ci95_disc_pp_lower": float(ci_result["ci_lower"]),
        "ci95_disc_pp_upper": float(ci_result["ci_upper"]),
        "crit_a_pass_freq60": bool(crit_a),
        "crit_b_pass_disc15": bool(crit_b),
        "crit_c_pass_median": bool(crit_c),
        "verdict_single_pool": verdict,
    }


# -----------------------------------------------------------------------------
# Per-HA evaluators
# -----------------------------------------------------------------------------


def eval_HA07c(df_indexed, crash_starts, null_dates) -> dict:
    """HA07c primitive: max signed z of stress_mean_sleep night-over-night delta over 4-day leadup."""
    crash_trig, crash_med, n_skipped_crash = _build_trigger_arrays_delta_signed(
        crash_starts, df_indexed, "stress_mean_sleep", sigma_floor=2.0,
    )
    null_trig, _null_med, _ = _build_trigger_arrays_delta_signed(
        null_dates, df_indexed, "stress_mean_sleep", sigma_floor=2.0,
    )
    res = evaluate_ha("HA07c", crash_trig, null_trig, crash_med, N_STD_PRIMARY)
    res["operand"] = "max signed z (4d) of night-over-night delta of stress_mean_sleep; lagged baseline [d-90, d-30] trimmed; sigma_floor=2.0"
    return res


def eval_HA07d(df_indexed, crash_starts, null_dates) -> dict:
    """HA07d primitive: max |z| of stress_stdev_sleep night-over-night delta over 4-day leadup (bidirectional)."""
    crash_trig, crash_med, _ = _build_trigger_arrays_delta_abs(
        crash_starts, df_indexed, "stress_stdev_sleep", sigma_floor=0.5,
    )
    null_trig, _, _ = _build_trigger_arrays_delta_abs(
        null_dates, df_indexed, "stress_stdev_sleep", sigma_floor=0.5,
    )
    res = evaluate_ha("HA07d", crash_trig, null_trig, crash_med, N_STD_PRIMARY)
    res["operand"] = "max |z| (4d, bidirectional) of night-over-night delta of stress_stdev_sleep; lagged baseline; sigma_floor=0.5"
    return res


def eval_HA08c(df_indexed, crash_starts, null_dates) -> dict:
    """HA08c primitive: max signed z of trailing-5d OLS slope of stress_mean_sleep over 4-day leadup."""
    crash_trig, crash_med, _ = _build_trigger_arrays_slope_signed(
        crash_starts, df_indexed, "stress_mean_sleep", sigma_floor=0.5,
    )
    null_trig, _, _ = _build_trigger_arrays_slope_signed(
        null_dates, df_indexed, "stress_mean_sleep", sigma_floor=0.5,
    )
    res = evaluate_ha("HA08c", crash_trig, null_trig, crash_med, N_STD_PRIMARY)
    res["operand"] = "max signed z (4d) of trailing-5d OLS slope of stress_mean_sleep; lagged baseline of slopes; sigma_floor=0.5/day"
    return res


def eval_HA10(df_indexed, crash_starts, null_dates) -> dict:
    """HA10 primitive: max |z| of bb_highest (morning BB peak) over 4-day leadup (bidirectional)."""
    crash_trig, crash_med, _ = _build_trigger_arrays_z_abs(
        crash_starts, df_indexed, "bb_highest", sigma_floor=2.0,
    )
    null_trig, _, _ = _build_trigger_arrays_z_abs(
        null_dates, df_indexed, "bb_highest", sigma_floor=2.0,
    )
    res = evaluate_ha("HA10", crash_trig, null_trig, crash_med, N_STD_PRIMARY)
    res["operand"] = "max |z| (4d, bidirectional) of bb_highest (morning BB peak proxy via UDS); lagged baseline; sigma_floor=2.0 BB points"
    return res


def eval_HA11(df_indexed, crash_starts, null_dates) -> dict:
    """HA11 primitive: max signed z of u_dip_count over 4-day leadup (one-sided elevated)."""
    crash_trig, crash_med, _ = _build_trigger_arrays_z_signed(
        crash_starts, df_indexed, "u_dip_count", sigma_floor=0.5,
    )
    null_trig, _, _ = _build_trigger_arrays_z_signed(
        null_dates, df_indexed, "u_dip_count", sigma_floor=0.5,
    )
    res = evaluate_ha("HA11", crash_trig, null_trig, crash_med, N_STD_PRIMARY)
    res["operand"] = "max signed z (4d) of u_dip_count (per-day count primitive in master); lagged baseline; sigma_floor=0.5 events"
    return res


def eval_HA01b_recomputed(df_indexed, crash_starts, null_dates) -> dict:
    """HA01b-recomputed primitive: frac windows where >=1 day in 4-day leadup has exertion_class_lagged in {heavy, very_heavy}."""
    def collect(refs):
        triggers = []
        n_shock_list = []
        for ref in refs:
            n_shock, n_valid = episode_ha01b_n_shock(ref, df_indexed)
            if n_shock is None:
                triggers.append(np.nan)
                continue
            triggers.append(1 if n_shock >= 1 else 0)
            n_shock_list.append(n_shock)
        return np.array(triggers, dtype=float), n_shock_list

    crash_trig, crash_n_shock = collect(crash_starts)
    null_trig, _ = collect(null_dates)
    res = evaluate_ha(
        "HA01b-recomputed",
        crash_trig, null_trig,
        # Magnitude crit uses median n_shock_days, not z; pre-reg crit (c) HA01: median>=1, lq>=0
        crash_n_shock,
        n_std=2,  # placeholder: crit (c) is median>=1, lq>=0
    )
    # Override crit_c per HA01 spec
    if "verdict_single_pool" not in res or res["verdict_single_pool"].startswith("INCONCLUSIVE"):
        res["operand"] = "frac windows with >=1 day in 4-day leadup at exertion_class_lagged in {heavy, very_heavy}; threshold/sigma_floor n/a"
        return res
    cleaned = [x for x in crash_n_shock if x is not None]
    if len(cleaned) > 0:
        cleaned_sorted = sorted(cleaned)
        median_shock = float(statistics.median(cleaned_sorted))
        lq = float(cleaned_sorted[int(len(cleaned_sorted) * 0.25)])
    else:
        median_shock = float("nan")
        lq = float("nan")
    crit_a = res["frac_crash"] >= CRIT_A_FRAC
    crit_b = res["disc_pp"] >= CRIT_B_DISC_PP
    crit_c = (median_shock >= 1) and (lq >= 0)
    res["median_max_z_or_signed"] = median_shock
    res["lower_quartile_n_shock"] = lq
    res["crit_a_pass_freq60"] = bool(crit_a)
    res["crit_b_pass_disc15"] = bool(crit_b)
    res["crit_c_pass_median"] = bool(crit_c)
    res["verdict_single_pool"] = "SUPPORTED" if (crit_a and crit_b and crit_c) else "NOT-SUPPORTED"
    res["operand"] = "frac windows with >=1 day in 4-day leadup at exertion_class_lagged in {heavy, very_heavy}"
    return res


def eval_H01(df_indexed, crash_starts, null_dates) -> dict:
    """H01 (stretch): mean RHR over 7-day leadup minus baseline. Trigger if delta>=3 bpm; crit a: 60% trigger."""
    def collect(refs):
        triggers = []
        deltas = []
        for ref in refs:
            d_val, _ = episode_h01_h04_delta(ref, df_indexed, "resting_hr", leadup_days=7)
            if d_val is None:
                triggers.append(np.nan)
                continue
            triggers.append(1 if d_val >= 3 else 0)
            deltas.append(d_val)
        return np.array(triggers, dtype=float), deltas
    crash_trig, crash_deltas = collect(crash_starts)
    null_trig, _ = collect(null_dates)
    res = evaluate_ha("H01", crash_trig, null_trig, crash_deltas, n_std=4)
    # Override crit_c for H01: median delta >= +2 bpm, lower-q >= 0
    cleaned = sorted([x for x in crash_deltas if x is not None])
    if cleaned:
        median_d = float(statistics.median(cleaned))
        lq_d = float(cleaned[int(len(cleaned) * 0.25)])
    else:
        median_d = float("nan")
        lq_d = float("nan")
    if "verdict_single_pool" in res and not res["verdict_single_pool"].startswith("INCONCLUSIVE"):
        crit_a = res["frac_crash"] >= CRIT_A_FRAC
        crit_b = res["disc_pp"] >= CRIT_B_DISC_PP
        crit_c = (median_d >= 2.0) and (lq_d >= 0.0)
        res["median_delta_bpm"] = median_d
        res["lower_quartile_delta_bpm"] = lq_d
        res["crit_a_pass_freq60"] = bool(crit_a)
        res["crit_b_pass_disc15"] = bool(crit_b)
        res["crit_c_pass_median"] = bool(crit_c)
        res["verdict_single_pool"] = "SUPPORTED" if (crit_a and crit_b and crit_c) else "NOT-SUPPORTED"
    res["operand"] = "frac windows with mean RHR (7d leadup) - trimmed baseline >= +3 bpm"
    return res


def eval_HA06b(df_indexed, crash_starts, null_dates) -> dict:
    """HA06b (stretch): max |z| of resting_hr (nightly) over 4-day leadup (bidirectional)."""
    crash_trig, crash_med, _ = _build_trigger_arrays_z_abs(
        crash_starts, df_indexed, "resting_hr", sigma_floor=0.5,
    )
    null_trig, _, _ = _build_trigger_arrays_z_abs(
        null_dates, df_indexed, "resting_hr", sigma_floor=0.5,
    )
    res = evaluate_ha("HA06b", crash_trig, null_trig, crash_med, N_STD_PRIMARY)
    res["operand"] = "max |z| (4d, bidirectional) of resting_hr; lagged baseline; sigma_floor=0.5 bpm"
    return res


def eval_H02b(df_indexed, crash_starts, null_dates) -> dict:
    """H02b (stretch): max delta(max_spike_minutes - baseline) over 3-day leadup; trigger if >= +10 min."""
    def collect(refs):
        triggers = []
        deltas = []
        for ref in refs:
            delta_val, _ = episode_h02b_max_delta(ref, df_indexed, "max_spike_minutes", baseline_threshold=10.0, leadup_days=3)
            if delta_val is None:
                triggers.append(np.nan)
                continue
            triggers.append(1 if delta_val >= 10.0 else 0)
            deltas.append(delta_val)
        return np.array(triggers, dtype=float), deltas
    crash_trig, crash_deltas = collect(crash_starts)
    null_trig, _ = collect(null_dates)
    res = evaluate_ha("H02b", crash_trig, null_trig, crash_deltas, n_std=4)
    cleaned = sorted([x for x in crash_deltas if x is not None])
    if cleaned:
        median_d = float(statistics.median(cleaned))
        lq_d = float(cleaned[int(len(cleaned) * 0.25)])
    else:
        median_d = float("nan")
        lq_d = float("nan")
    if "verdict_single_pool" in res and not res["verdict_single_pool"].startswith("INCONCLUSIVE"):
        crit_a = res["frac_crash"] >= CRIT_A_FRAC
        crit_b = res["disc_pp"] >= CRIT_B_DISC_PP
        crit_c = (median_d >= 5.0) and (lq_d >= 0.0)
        res["median_delta_min"] = median_d
        res["lower_quartile_delta_min"] = lq_d
        res["crit_a_pass_freq60"] = bool(crit_a)
        res["crit_b_pass_disc15"] = bool(crit_b)
        res["crit_c_pass_median"] = bool(crit_c)
        res["verdict_single_pool"] = "SUPPORTED" if (crit_a and crit_b and crit_c) else "NOT-SUPPORTED"
    res["operand"] = "frac windows where max(max_spike_minutes - trimmed_baseline) over 3-day leadup >= +10 min"
    return res


def eval_H04(df_indexed, crash_starts, null_dates) -> dict:
    """H04 (stretch): mean BB net-drain over 7-day leadup minus baseline; trigger if <= -5 BB units."""
    # bb_net_drain proxy: drained - charged (positive = net drain)
    work = df_indexed.copy()
    work["bb_net_drain"] = work["bb_drained_24h"].astype(float) - work["bb_charged_24h"].astype(float)
    def collect(refs):
        triggers = []
        deltas = []
        for ref in refs:
            d_val, _ = episode_h01_h04_delta(ref, work, "bb_net_drain", leadup_days=7)
            if d_val is None:
                triggers.append(np.nan)
                continue
            triggers.append(1 if d_val <= -5.0 else 0)
            deltas.append(d_val)
        return np.array(triggers, dtype=float), deltas
    crash_trig, crash_deltas = collect(crash_starts)
    null_trig, _ = collect(null_dates)
    res = evaluate_ha("H04", crash_trig, null_trig, crash_deltas, n_std=4)
    cleaned = sorted([x for x in crash_deltas if x is not None])
    if cleaned:
        median_d = float(statistics.median(cleaned))
        upperq_d = float(cleaned[int(len(cleaned) * 0.75)])
    else:
        median_d = float("nan")
        upperq_d = float("nan")
    if "verdict_single_pool" in res and not res["verdict_single_pool"].startswith("INCONCLUSIVE"):
        crit_a = res["frac_crash"] >= CRIT_A_FRAC
        crit_b = res["disc_pp"] >= CRIT_B_DISC_PP
        crit_c = (median_d <= -3.0) and (upperq_d <= 0.0)
        res["median_delta_bb"] = median_d
        res["upper_quartile_delta_bb"] = upperq_d
        res["crit_a_pass_freq60"] = bool(crit_a)
        res["crit_b_pass_disc15"] = bool(crit_b)
        res["crit_c_pass_median"] = bool(crit_c)
        res["verdict_single_pool"] = "SUPPORTED" if (crit_a and crit_b and crit_c) else "NOT-SUPPORTED"
    res["operand"] = "frac windows where mean BB net-drain (7d leadup) - baseline <= -5 BB units (bb_net_drain = drained_24h - charged_24h)"
    return res


def eval_HA01c(df_indexed, crash_starts, null_dates) -> dict:
    """HA01c (R14-v2): frac windows with >=1 day in 4-day leadup at eff_exertion_rank_lagged >= 0.75.

    Crit (a) freq >= 60%; crit (b) disc >= +15 pp; crit (c) median rank on
    TRIGGERING episodes >= 0.875 (locked HA01c bar). One-sided elevated.
    Operand routes through the per_day_master `eff_exertion_rank_lagged`
    column (the v3.2 _lagged variant that the locked HA01c test used; see
    §3.2 caveat for the _lagged_lcera alternative -- on the all-LC Stratum 4
    pool the two baselines are near-identical).
    """
    def collect(refs):
        triggers = []
        trig_max_ranks = []  # max rank only on TRIGGERING episodes (for crit_c)
        for ref in refs:
            triggered, max_rank, _n_valid = episode_ha01c_rank_trigger(ref, df_indexed)
            if triggered is None:
                triggers.append(np.nan)
                continue
            triggers.append(1 if triggered else 0)
            if triggered:
                trig_max_ranks.append(max_rank)
        return np.array(triggers, dtype=float), trig_max_ranks

    crash_trig, crash_trig_ranks = collect(crash_starts)
    null_trig, _ = collect(null_dates)
    res = evaluate_ha("HA01c", crash_trig, null_trig, crash_trig_ranks, n_std=2)
    if "verdict_single_pool" not in res or res["verdict_single_pool"].startswith("INCONCLUSIVE"):
        res["operand"] = "frac windows with >=1 day in 4-day leadup at eff_exertion_rank_lagged >= 0.75; median rank on triggering >= 0.875"
        return res
    median_rank = float(statistics.median(sorted(crash_trig_ranks))) if crash_trig_ranks else float("nan")
    crit_a = res["frac_crash"] >= CRIT_A_FRAC
    crit_b = res["disc_pp"] >= CRIT_B_DISC_PP
    crit_c = (not np.isnan(median_rank)) and (median_rank >= 0.875)
    res["median_max_z_or_signed"] = median_rank
    res["median_rank_on_triggering"] = median_rank
    res["crit_a_pass_freq60"] = bool(crit_a)
    res["crit_b_pass_disc15"] = bool(crit_b)
    res["crit_c_pass_median"] = bool(crit_c)
    res["verdict_single_pool"] = "SUPPORTED" if (crit_a and crit_b and crit_c) else "NOT-SUPPORTED"
    res["operand"] = "frac windows with >=1 day in 4-day leadup at eff_exertion_rank_lagged >= 0.75; median rank on triggering episodes >= 0.875"
    return res


def eval_H03(df_indexed, crash_starts, null_dates) -> dict:
    """H03 (R14-v2, stretch): frac windows where 7d-leadup mean sleep-efficiency minus trimmed baseline <= -0.05.

    Crit (a) freq >= 60% at delta <= -0.05; crit (b) disc >= +15 pp; crit (c)
    median delta <= -0.03 AND upper-quartile delta <= 0 (locked H03 bar).
    Direction: drop (one-sided, lower). 7-day leadup, [d-97, d-8] trimmed
    baseline. Efficiency reconstructed from per_day_master sleep components.
    """
    def collect(refs):
        triggers = []
        deltas = []
        for ref in refs:
            d_val, _ = episode_h03_efficiency_delta(ref, df_indexed)
            if d_val is None:
                triggers.append(np.nan)
                continue
            triggers.append(1 if d_val <= -0.05 else 0)
            deltas.append(d_val)
        return np.array(triggers, dtype=float), deltas

    crash_trig, crash_deltas = collect(crash_starts)
    null_trig, _ = collect(null_dates)
    res = evaluate_ha("H03", crash_trig, null_trig, crash_deltas, n_std=4)
    cleaned = sorted([x for x in crash_deltas if x is not None])
    if cleaned:
        median_d = float(statistics.median(cleaned))
        upperq_d = float(cleaned[int(len(cleaned) * 0.75)])
    else:
        median_d = float("nan")
        upperq_d = float("nan")
    if "verdict_single_pool" in res and not res["verdict_single_pool"].startswith("INCONCLUSIVE"):
        crit_a = res["frac_crash"] >= CRIT_A_FRAC
        crit_b = res["disc_pp"] >= CRIT_B_DISC_PP
        crit_c = (median_d <= -0.03) and (upperq_d <= 0.0)
        res["median_delta_eff"] = median_d
        res["upper_quartile_delta_eff"] = upperq_d
        res["crit_a_pass_freq60"] = bool(crit_a)
        res["crit_b_pass_disc15"] = bool(crit_b)
        res["crit_c_pass_median"] = bool(crit_c)
        res["verdict_single_pool"] = "SUPPORTED" if (crit_a and crit_b and crit_c) else "NOT-SUPPORTED"
    res["operand"] = "frac windows where mean sleep-efficiency (7d leadup) - trimmed baseline <= -0.05 (eff = (deep+light)/(deep+light+awake+unmeasurable))"
    return res


# -----------------------------------------------------------------------------
# Locked-verdict cross-reference table (per result.md headline numbers)
# -----------------------------------------------------------------------------


LOCKED_VERDICTS = {
    "HA01b-recomputed": {
        "locked_verdict": "REFUTED both eras",
        "locked_train_disc_pp": +5.8,
        "locked_validate_disc_pp": +4.0,
        "locked_train_frac": 0.818,
        "locked_validate_frac": 0.800,
        "result_md_path": "analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md",
        "note": "Lagged-baseline (v3.2) recomputation of HA01b; canonical version per REJECTED.md.",
    },
    "HA07c": {
        "locked_verdict": "TRAIN SUPPORTED / VALIDATE REFUTED / OVERALL REFUTED",
        "locked_train_disc_pp": +23.2,
        "locked_validate_disc_pp": -6.0,
        "locked_train_frac": 0.692,
        "locked_validate_frac": 0.400,
        "result_md_path": "analyses/hypotheses/HA07c-sleep-stress-mean-delta/result.md",
        "note": "Sleep stress mean delta primitive; HRV-proxy chain.",
    },
    "HA07d": {
        "locked_verdict": "BOTH ERAS SUPPORTED -> OVERALL SUPPORTED (only canonical both-eras-SUPPORTED test)",
        "locked_train_disc_pp": +19.6,
        "locked_validate_disc_pp": +21.7,
        "locked_train_frac": 0.846,
        "locked_validate_frac": 0.867,
        "result_md_path": "analyses/hypotheses/HA07d-sleep-stress-variability/result.md",
        "note": "Sleep stress variability (stdev) delta primitive; bidirectional.",
    },
    "HA08c": {
        "locked_verdict": "TRAIN SUPPORTED / VALIDATE REFUTED / OVERALL REFUTED",
        "locked_train_disc_pp": +23.0,
        "locked_validate_disc_pp": +1.5,
        "locked_train_frac": 0.615,
        "locked_validate_frac": 0.400,
        "result_md_path": "analyses/hypotheses/HA08c-sleep-stress-slope/result.md",
        "note": "Trailing-5d OLS slope of sleep stress; one-sided elevated.",
    },
    "HA10": {
        "locked_verdict": "TRAIN REFUTED (-20.5) / VALIDATE SUPPORTED (+16.2) / OVERALL REFUTED; era-directionality reversal (train 100% lowered, validate 69% elevated)",
        "locked_train_disc_pp": -20.5,
        "locked_validate_disc_pp": +16.2,
        "locked_train_frac": 0.500,
        "locked_validate_frac": 0.867,
        "result_md_path": "analyses/hypotheses/HA10-bb-overnight-recharge/result.md",
        "note": "Morning BB peak; bidirectional; only DIRECTIONALITY-REVERSAL test in project.",
    },
    "HA11": {
        "locked_verdict": "TRAIN SUPPORTED / VALIDATE REFUTED (inverse) / OVERALL REFUTED",
        "locked_train_disc_pp": +22.8,
        "locked_validate_disc_pp": -10.7,
        "locked_train_frac": 0.643,
        "locked_validate_frac": 0.308,
        "result_md_path": "analyses/hypotheses/HA11-stress-udip/result.md",
        "note": "Within-day U-dip count; one-sided elevated.",
    },
    "H01": {
        "locked_verdict": "REFUTED both eras",
        "locked_train_disc_pp": -1.2,
        "locked_validate_disc_pp": -9.5,
        "locked_train_frac": 0.083,
        "locked_validate_frac": 0.000,
        "result_md_path": "analyses/hypotheses/H01-rhr-drift/result.md",
        "note": "RHR drift over 7-day leadup at +3 bpm; absolute-threshold spec.",
    },
    "H02b": {
        "locked_verdict": "TRAIN SUPPORTED / VALIDATE refuted (near-miss) / OVERALL REFUTED",
        "locked_train_disc_pp": +29.9,
        "locked_validate_disc_pp": -8.2,
        "locked_train_frac": 0.714,
        "locked_validate_frac": 0.333,
        "result_md_path": "analyses/hypotheses/H02b-stress-spikes/result.md",
        "note": "Per-minute stress spike count (3-day leadup); +10 min absolute threshold.",
    },
    "H04": {
        "locked_verdict": "REFUTED both eras (validate near-miss +13.3 pp)",
        "locked_train_disc_pp": -5.7,
        "locked_validate_disc_pp": +13.3,
        "locked_train_frac": 0.143,
        "locked_validate_frac": 0.333,
        "result_md_path": "analyses/hypotheses/H04-body-battery/result.md",
        "note": "BB net-drain over 7-day leadup at -5 BB units; absolute-threshold spec.",
    },
    "HA06b": {
        "locked_verdict": "TRAIN SUPPORTED / VALIDATE refuted / OVERALL REFUTED",
        "locked_train_disc_pp": +18.9,
        "locked_validate_disc_pp": +0.8,
        "locked_train_frac": 0.714,
        "locked_validate_frac": 0.533,
        "result_md_path": "analyses/hypotheses/HA06b-rhr-zscore/result.md",
        "note": "RHR z-score (4d, bidirectional); permanently demoted to non-load-bearing per v2 diag.",
    },
    "HA01c": {
        "locked_verdict": "BOTH ERAS SUPPORTED -> OVERALL SUPPORTED (load-bearing WITHHELD pending v2 threshold-monotonicity diagnostic)",
        "locked_train_disc_pp": +21.3,
        "locked_validate_disc_pp": +19.5,
        "locked_train_frac": 0.818,
        "locked_validate_frac": 0.800,
        "result_md_path": "analyses/hypotheses/HA01c-effective-exertion-shock/result.md",
        "note": "Effective-exertion rank shock (>= 0.75 in 4d leadup); SUPPORTED both eras at the locked 3-criterion bar; load-bearing gated on HA01c v2. R14-v2 close.",
    },
    "H03": {
        "locked_verdict": "REFUTED both eras",
        "locked_train_disc_pp": 0.0,
        "locked_validate_disc_pp": 0.0,
        "locked_train_frac": 0.000,
        "locked_validate_frac": 0.000,
        "result_md_path": "analyses/hypotheses/H03-sleep-efficiency/result.md",
        "note": "Sleep-efficiency drop (>= 5pp) over 7d leadup; flat-as-a-board, REFUTED decisively both eras (0.0% trigger). R14-v2 close.",
    },
}


def _classify_locked(locked: str) -> str:
    """Classify the locked verdict shape.

    Returns one of:
      - BOTH_SUPPORTED      (only canonical both-eras-SUPPORTED case e.g. HA07d)
      - BOTH_REFUTED        (NOT-SUPPORTED both eras e.g. H01, H04, HA01b-recomputed)
      - SPLIT_MIXED         (one era SUPPORTED, other REFUTED, overall REFUTED)
    """
    locked_l = locked.upper()
    if "OVERALL SUPPORTED" in locked_l or "BOTH ERAS SUPPORTED" in locked_l:
        return "BOTH_SUPPORTED"
    if "REFUTED BOTH" in locked_l.replace(" ", "") or locked_l.startswith("REFUTED BOTH"):
        return "BOTH_REFUTED"
    # split-mixed: contains BOTH "SUPPORTED" AND "REFUTED" tokens
    if "SUPPORTED" in locked_l and "REFUTED" in locked_l:
        return "SPLIT_MIXED"
    if "REFUTED" in locked_l:
        return "BOTH_REFUTED"
    return "UNCLEAR"


def divergence_label(locked: str, single: str) -> str:
    """Compare locked era-aggregated verdict to single-pool verdict; return label.

    Convergence/divergence semantics:
      - locked BOTH_SUPPORTED + single SUPPORTED -> CONVERGE (both SUPPORTED)
      - locked BOTH_SUPPORTED + single NOT-SUPPORTED -> DIVERGE
      - locked BOTH_REFUTED + single NOT-SUPPORTED -> CONVERGE (both NOT-SUPPORTED)
      - locked BOTH_REFUTED + single SUPPORTED -> DIVERGE
      - locked SPLIT_MIXED + single SUPPORTED -> DIVERGE (locked SPLIT-MIXED -> single-pool SUPPORTED)
      - locked SPLIT_MIXED + single NOT-SUPPORTED -> CONVERGE-ON-OVERALL
        (the OVERALL-REFUTED locked verdict matches single-pool NOT-SUPPORTED;
         direction-cancellation under single-pool is the plausible driver
         per Sec 5.7 bullet 7 examples)
    """
    locked_class = _classify_locked(locked)
    single_l = single.upper()
    if "INCONCLUSIVE" in single_l:
        return "INCONCLUSIVE"
    single_supported = single_l == "SUPPORTED"
    if locked_class == "BOTH_SUPPORTED":
        return "CONVERGE (both SUPPORTED)" if single_supported else "DIVERGE (locked OVERALL-SUPPORTED -> single-pool NOT-SUPPORTED)"
    if locked_class == "BOTH_REFUTED":
        return "CONVERGE (both NOT-SUPPORTED)" if not single_supported else "DIVERGE (locked NOT-SUPPORTED both eras -> single-pool SUPPORTED)"
    if locked_class == "SPLIT_MIXED":
        if single_supported:
            return "DIVERGE (locked SPLIT-MIXED -> single-pool SUPPORTED)"
        return "CONVERGE-ON-OVERALL (locked OVERALL-REFUTED, single-pool NOT-SUPPORTED)"
    return f"unclear (locked_class={locked_class}, single={single!r})"


def driver_note(divergence: str, locked: dict, single: dict) -> str:
    """Name plausible drivers descriptively (no causal claim)."""
    if "INCONCLUSIVE" in divergence:
        return "n_crash_clean < 10 on single pool primitive; insufficient evidence at this primitive."
    if "CONVERGE (both NOT-SUPPORTED)" in divergence:
        return "locked era-split and single-pool both NOT-SUPPORTED; cross-check confirms NOT-SUPPORTED status under single-pool MD2+MD3 framework."
    if "CONVERGE (both SUPPORTED)" in divergence:
        return "locked era-split and single-pool both SUPPORTED; cross-check confirms SUPPORTED status under single-pool MD2+MD3 framework."
    if "CONVERGE-ON-OVERALL" in divergence:
        return "locked OVERALL verdict (single-era SUPPORTED averaged with single-era REFUTED) and single-pool NOT-SUPPORTED converge; direction-cancellation under single-pool plausible per the bullet-7 examples."
    if "DIVERGE" in divergence:
        candidates = []
        if locked.get("locked_train_disc_pp", 0) * locked.get("locked_validate_disc_pp", 0) < 0:
            candidates.append("opposite-sign per-era disc_pp cancels under single-pool (direction-reversal cancellation)")
        if abs(locked.get("locked_train_disc_pp", 0) - locked.get("locked_validate_disc_pp", 0)) > 20:
            candidates.append("large per-era disc_pp gap (>20 pp) averaged to single-pool")
        if abs(single.get("disc_pp", 0) - (locked.get("locked_train_disc_pp", 0) + locked.get("locked_validate_disc_pp", 0)) / 2) > 10:
            candidates.append("single-pool disc_pp deviates >10 pp from naive per-era mean (block-scheme + finite-sample variability)")
        if not candidates:
            candidates.append("block-perm null + stationary-bootstrap CI scheme differs from legacy null-window resampling")
        return "; ".join(candidates) + "."
    return "no driver identifiable from descriptive numbers alone."


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    print("[R14] Loading per_day_master.csv (Stratum 4 single pool)...")
    df = load_master()
    df_indexed = _index_master(df)
    print(f"[R14]   n_days = {len(df_indexed)}")
    print(f"[R14]   date range = {df_indexed['date'].iloc[0]} to {df_indexed['date'].iloc[-1]}")

    crash_starts = load_crash_episodes()
    print(f"[R14]   n_crash_episodes = {len(crash_starts)}")
    if len(crash_starts) == 0:
        raise RuntimeError("No crash episodes found")
    print(f"[R14]   crash range = {crash_starts[0]} to {crash_starts[-1]}")

    # Build a single null sample for the 4-day-leadup HAs (the dominant family)
    # using the legacy seed so the cross-check inherits the same reference scheme.
    null_dates_4d = build_null_dates(df_indexed, crash_starts, leadup_days=LEADUP_DAYS, seed=LEGACY_NULL_SEED)
    print(f"[R14]   null_dates_4d = {len(null_dates_4d)} (target {NULL_SAMPLE_SIZE})")
    # Build separate null samples for 7-day-leadup HAs (H01, H04) and 3-day (H02b)
    null_dates_7d = build_null_dates(df_indexed, crash_starts, leadup_days=7, seed=LEGACY_NULL_SEED)
    null_dates_3d = build_null_dates(df_indexed, crash_starts, leadup_days=3, seed=LEGACY_NULL_SEED)

    # Evaluate primary scope
    primary_evaluators = [
        ("HA01b-recomputed", eval_HA01b_recomputed, null_dates_4d),
        ("HA07c", eval_HA07c, null_dates_4d),
        ("HA07d", eval_HA07d, null_dates_4d),
        ("HA08c", eval_HA08c, null_dates_4d),
        ("HA10", eval_HA10, null_dates_4d),
        ("HA11", eval_HA11, null_dates_4d),
        ("HA01c", eval_HA01c, null_dates_4d),
    ]
    stretch_evaluators = [
        ("H01", eval_H01, null_dates_7d),
        ("H02b", eval_H02b, null_dates_3d),
        ("H04", eval_H04, null_dates_7d),
        ("HA06b", eval_HA06b, null_dates_4d),
        ("H03", eval_H03, null_dates_7d),
    ]

    results = {"primary": {}, "stretch": {}, "meta": {}}
    print("\n[R14] Primary scope (6 HAs)...")
    for name, fn, nulls in primary_evaluators:
        print(f"[R14]   {name} ...")
        res = fn(df_indexed, crash_starts, nulls)
        results["primary"][name] = res
        if "verdict_single_pool" in res:
            print(f"[R14]     -> {res.get('verdict_single_pool')} (disc={res.get('disc_pp','?')})")
    print("\n[R14] Stretch scope...")
    for name, fn, nulls in stretch_evaluators:
        print(f"[R14]   {name} ...")
        try:
            res = fn(df_indexed, crash_starts, nulls)
            results["stretch"][name] = res
            if "verdict_single_pool" in res:
                print(f"[R14]     -> {res.get('verdict_single_pool')} (disc={res.get('disc_pp','?')})")
        except Exception as exc:
            results["stretch"][name] = {"label": name, "verdict_single_pool": f"ERROR: {exc}"}
            print(f"[R14]     -> ERROR: {exc}")

    # Add divergence labels + driver notes
    for tier in ("primary", "stretch"):
        for name, res in results[tier].items():
            if name in LOCKED_VERDICTS:
                locked = LOCKED_VERDICTS[name]
                if "verdict_single_pool" in res:
                    res["divergence"] = divergence_label(locked["locked_verdict"], res["verdict_single_pool"])
                    res["driver_note"] = driver_note(res["divergence"], locked, res)
                    res["locked_verdict"] = locked["locked_verdict"]
                    res["locked_train_disc_pp"] = locked["locked_train_disc_pp"]
                    res["locked_validate_disc_pp"] = locked["locked_validate_disc_pp"]
                    res["locked_train_frac"] = locked["locked_train_frac"]
                    res["locked_validate_frac"] = locked["locked_validate_frac"]
                    res["result_md_path"] = locked["result_md_path"]
                    res["locked_note"] = locked["note"]

    # Meta
    results["meta"] = {
        "as_of_date": str(AS_OF_DATE),
        "stratum_4_start": str(STRATUM_4_START),
        "n_days_master_in_S4": len(df_indexed),
        "n_crash_episodes_in_S4": len(crash_starts),
        "null_sample_size": NULL_SAMPLE_SIZE,
        "n_null_4d": len(null_dates_4d),
        "n_null_7d": len(null_dates_7d),
        "n_null_3d": len(null_dates_3d),
        "block_length_E_L": DEFAULT_EL,
        "n_bootstrap": N_BOOTSTRAP,
        "seed": SEED,
        "legacy_null_seed": LEGACY_NULL_SEED,
        "n_std_primary": N_STD_PRIMARY,
        "leadup_days_primary": LEADUP_DAYS,
        "run_at": datetime.utcnow().isoformat() + "Z",
    }

    # Write result-data.json
    out_path_json = HERE / "result-data.json"
    out_path_json.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\n[R14] Wrote {out_path_json}")

    # Compute pattern summary for findings.md
    diverge = []
    converge = []
    inconclusive = []
    for tier in ("primary", "stretch"):
        for name, res in results[tier].items():
            div = res.get("divergence", "")
            if "INCONCLUSIVE" in div:
                inconclusive.append(name)
            elif "DIVERGE" in div:
                diverge.append(name)
            else:
                converge.append(name)
    results["meta"]["headline_pattern"] = (
        f"{len(converge)} converge (locked-verdict <-> single-pool) / "
        f"{len(diverge)} diverge / {len(inconclusive)} inconclusive on single-pool primitive"
    )
    print(f"[R14]   {results['meta']['headline_pattern']}")

    # Now render findings.md
    write_findings_md(results)
    print(f"[R14] Wrote {HERE / 'findings.md'}")


def write_findings_md(results: dict) -> None:
    """Render the findings.md per handoff Sec 2.5 structure."""
    meta = results["meta"]
    lines: list[str] = []
    lines.append(
        "# Findings - R14 single-pool re-anchor cross-check\n"
        "\n"
        "**Strand A operationalisation-support analysis** - executes the "
        "binding recipe at "
        "[`methodology/train_validate_split_fate.md`](../../../../methodology/train_validate_split_fate.md) "
        "Sec 5.7 (single-pool re-run cross-check; descriptive, not a re-lock).\n"
    )
    lines.append(
        f"**Surface**: full Stratum 4 single pool, {meta['stratum_4_start']} to "
        f"{meta['as_of_date']} (n_days={meta['n_days_master_in_S4']}; "
        f"n_crash_episodes={meta['n_crash_episodes_in_S4']}). Block-permutation "
        f"null at E[L]={meta['block_length_E_L']}, B={meta['n_bootstrap']:,}, "
        f"seed `{meta['seed']}`. Stationary bootstrap 95% CI on the discrimination "
        f"statistic (pp) at the same E[L]. Null sample size n={meta['null_sample_size']} "
        f"per HA leadup-window-length (legacy seed `{meta['legacy_null_seed']}` for "
        f"reference-frame inheritance).\n"
    )
    lines.append(
        "**Discipline binding**: Layer 1 descriptive cross-check per [CONVENTIONS Sec 2.1](../../../../CONVENTIONS.md). "
        "Locked HA `result.md` files are UNCHANGED per Sec 5.7 bullets 6-8. "
        "Train-vs-validate divergence is a **number, not a narrative** per Sec 5.7 "
        "bullet 8. No framework is pre-committed as correct per Sec 5.7 bullet 7. "
        "Single-pool verdicts are NOT promoted to SUPPORTED on their own per Sec 5.7 "
        "bullet 8; they are descriptive overlays. The HA01b legacy +17.3 pp validate "
        "divergence is NOT anchored on per Sec 5.7 bullet 8 (v3.1 rolling-baseline "
        "artefact; v3.2 lagged-baseline recomputed is canonical).\n"
    )
    lines.append("---\n")

    # Sec 1 Headline
    lines.append("## 1. Headline\n")
    primary_count = len(results["primary"])
    stretch_count = len(results["stretch"])
    n_diverge = sum(
        1 for tier in ("primary", "stretch") for r in results[tier].values()
        if "DIVERGE" in r.get("divergence", "")
    )
    n_converge = sum(
        1 for tier in ("primary", "stretch") for r in results[tier].values()
        if r.get("divergence", "").startswith("CONVERGE")
    )
    n_inconclusive = sum(
        1 for tier in ("primary", "stretch") for r in results[tier].values()
        if "INCONCLUSIVE" in r.get("divergence", "")
    )
    lines.append(
        f"Cross-check evaluated {primary_count} primary HAs + {stretch_count} stretch HAs "
        f"({primary_count + stretch_count} total) for **single-pool primary verdict robustness** to era partition. "
        f"On the single pool, {n_converge} HAs CONVERGE (single-pool primary verdict matches the locked era-split "
        f"overall verdict per the HA's own Sec 5 rule); {n_diverge} HAs DIVERGE; {n_inconclusive} INCONCLUSIVE.\n"
    )
    lines.append(
        "**The cross-check answers**: \"is the primary single-pool verdict robust to era partition?\" "
        "It does NOT answer \"does the effect change over time?\" - the single-subject observational "
        "design cannot answer that. Per Sec 5.7 bullet 8.\n"
    )
    lines.append("---\n")

    # Sec 2 Side-by-side table
    lines.append("## 2. Side-by-side table\n")
    lines.append(
        "One row per HA. Locked-verdict column reads the headline number from "
        "the HA's locked `result.md` (NOT modified by this cross-check). Single-pool "
        "columns are derived on the full Stratum 4 pool per Sec 5.7 recipe.\n"
    )
    lines.append(
        "| HA | locked verdict (era-split, OVERALL) | locked train disc | locked validate disc | "
        "n_single_pool (crash / null) | single-pool disc pp (CI95) | single-pool perm p (E[L]=7) | "
        "single-pool verdict | divergence | driver note (descriptive) |\n"
        "|---|---|---:|---:|---|---:|---:|---|---|---|\n"
    )
    for tier in ("primary", "stretch"):
        for name, res in results[tier].items():
            verdict_locked = res.get("locked_verdict", "n/a")
            train_disc = res.get("locked_train_disc_pp", "n/a")
            validate_disc = res.get("locked_validate_disc_pp", "n/a")
            n_c = res.get("n_crash_clean", "?")
            n_n = res.get("n_null_clean", "?")
            disc = res.get("disc_pp", float("nan"))
            ci_lo = res.get("ci95_disc_pp_lower", float("nan"))
            ci_hi = res.get("ci95_disc_pp_upper", float("nan"))
            perm_p = res.get("perm_pvalue_greater_E_L_7", float("nan"))
            verdict_single = res.get("verdict_single_pool", "n/a")
            div = res.get("divergence", "n/a")
            drv = res.get("driver_note", "n/a")
            disc_str = f"{disc:+.1f}" if isinstance(disc, float) and not np.isnan(disc) else str(disc)
            ci_str = (f"[{ci_lo:+.1f}, {ci_hi:+.1f}]"
                      if isinstance(ci_lo, float) and not np.isnan(ci_lo) else "n/a")
            perm_str = f"{perm_p:.4f}" if isinstance(perm_p, float) and not np.isnan(perm_p) else "n/a"
            tier_marker = "" if tier == "primary" else " (stretch)"
            lines.append(
                f"| **{name}**{tier_marker} | {verdict_locked} | "
                f"{train_disc:+.1f} | {validate_disc:+.1f} | {n_c} / {n_n} | "
                f"{disc_str} {ci_str} | {perm_str} | {verdict_single} | {div} | {drv} |\n"
            )
    lines.append("\n")
    lines.append("---\n")

    # Sec 3 Per-HA narrative notes
    lines.append("## 3. Per-HA narrative notes\n")
    lines.append(
        "Per Sec 5.7 bullet 8 \"number, not narrative\" discipline: 1-3 sentences per HA, "
        "describing the cross-check finding + naming plausible drivers descriptively where "
        "divergence is observed. NO causal claims; NO framework-correctness claims.\n"
    )
    for tier in ("primary", "stretch"):
        for name, res in results[tier].items():
            tier_marker = "" if tier == "primary" else " (stretch)"
            lines.append(f"### 3.x {name}{tier_marker}\n")
            lines.append(f"- **Operand**: {res.get('operand', 'n/a')}.\n")
            lines.append(f"- **Locked era-split verdict**: {res.get('locked_verdict', 'n/a')} "
                         f"(train {res.get('locked_train_disc_pp', 'n/a'):+.1f} pp, "
                         f"validate {res.get('locked_validate_disc_pp', 'n/a'):+.1f} pp; "
                         f"see [`{res.get('result_md_path', 'n/a')}`](../../../../{res.get('result_md_path', 'n/a')})).\n")
            disc = res.get('disc_pp', float('nan'))
            if isinstance(disc, float) and not np.isnan(disc):
                lines.append(
                    f"- **Single-pool**: disc_pp={disc:+.1f}, "
                    f"CI95=[{res['ci95_disc_pp_lower']:+.1f}, {res['ci95_disc_pp_upper']:+.1f}], "
                    f"perm p (E[L]=7) = {res['perm_pvalue_greater_E_L_7']:.4f}; "
                    f"frac_crash={res['frac_crash']:.3f}, frac_null={res['frac_null']:.3f}; "
                    f"crit_a={res['crit_a_pass_freq60']}, crit_b={res['crit_b_pass_disc15']}, "
                    f"crit_c={res['crit_c_pass_median']}; "
                    f"verdict (single-pool) = **{res['verdict_single_pool']}**.\n"
                )
            else:
                lines.append(f"- **Single-pool**: {res.get('verdict_single_pool', 'n/a')}.\n")
            lines.append(f"- **Divergence**: {res.get('divergence', 'n/a')}.\n")
            lines.append(f"- **Driver (descriptive)**: {res.get('driver_note', 'n/a')}\n")
            lines.append("\n")
    lines.append("---\n")

    # Sec 4 Aggregate summary
    lines.append("## 4. Aggregate cross-check summary\n")
    lines.append(
        f"Of the {primary_count + stretch_count} HAs evaluated:\n"
        f"\n"
        f"- **{n_converge} CONVERGE** (locked overall verdict <-> single-pool verdict).\n"
        f"- **{n_diverge} DIVERGE**.\n"
        f"- **{n_inconclusive} INCONCLUSIVE** on single-pool primitive.\n"
        f"\n"
        f"Pattern observations (descriptive only):\n"
    )
    # Build the pattern observations descriptively
    converging_supported = [
        n for tier in ("primary", "stretch") for n, r in results[tier].items()
        if "CONVERGE (both SUPPORTED)" in r.get("divergence", "")
    ]
    converging_not_supported = [
        n for tier in ("primary", "stretch") for n, r in results[tier].items()
        if "CONVERGE (both NOT-SUPPORTED)" in r.get("divergence", "")
    ]
    converging_on_overall = [
        (n, r) for tier in ("primary", "stretch") for n, r in results[tier].items()
        if "CONVERGE-ON-OVERALL" in r.get("divergence", "")
    ]
    diverging = [
        (n, r) for tier in ("primary", "stretch") for n, r in results[tier].items()
        if "DIVERGE" in r.get("divergence", "")
    ]
    if converging_supported:
        lines.append(
            f"- HAs whose locked OVERALL-SUPPORTED verdict reproduces under single-pool: "
            f"{', '.join(converging_supported)}.\n"
        )
    if converging_not_supported:
        lines.append(
            f"- HAs whose locked overall NOT-SUPPORTED status reproduces under single-pool: "
            f"{', '.join(converging_not_supported)}.\n"
        )
    if converging_on_overall:
        lines.append(
            f"- HAs whose locked split-mixed (one-era SUPPORTED, other-era REFUTED -> OVERALL REFUTED) verdict "
            f"converges with single-pool NOT-SUPPORTED (direction-cancellation under single-pool plausible "
            f"per Sec 5.7 bullet 7): {', '.join(n for n, _ in converging_on_overall)}.\n"
        )
    if diverging:
        diverging_names = [n for n, _ in diverging]
        lines.append(
            f"- HAs that DIVERGE between locked OVERALL verdict and single-pool verdict: "
            f"{', '.join(diverging_names)}.\n"
        )
    lines.append(
        "\n"
        "Per Sec 5.7 bullet 8 discipline: these patterns are descriptive only. "
        "No conclusion about \"the framework that's correct\" is asserted. The locked "
        "verdicts remain on record as the historical evidence for the era-split framework; "
        "the single-pool verdicts surfaced here are descriptive cross-check overlays for "
        "the MD2+MD3 framework. **User decides** on any follow-up per Sec 5.7 bullet 7.\n"
    )
    lines.append("---\n")

    # Sec 5 Deferred / out-of-scope
    lines.append("## 5. Deferred / out-of-scope HAs\n")
    lines.append(
        "Per stocktake Sec 9 + REJECTED.md Appendix:\n"
        "\n"
        "| HA | reason | reference |\n"
        "|---|---|---|\n"
        "| H02 | SUPERSEDED-by-H02b (daily-aggregate stress -> per-minute spike count); cross-check covers via H02b. | [REJECTED.md 2026-06-05](../../../../REJECTED.md) |\n"
        "| H02d | SUPERSEDED-by-equivalence (H02b == H02d at rho=+1.000 per cross-channel-correlation card). | [REJECTED.md 2026-06-06](../../../../REJECTED.md) |\n"
        "| H03b | RETIRED - data-resolution limit (INCONCLUSIVE x 12 cells; data does not exist at gated resolution). | [REJECTED.md Appendix](../../../../REJECTED.md) |\n"
        "| H05 | RETIRED - spec-induced trivial. | [REJECTED.md Appendix](../../../../REJECTED.md) |\n"
        "| HA01b-per-axis-diagnostic | NOT-RUN in cross-check (DIAGNOSTIC bound to HA01b parent; inheriting cross-check from HA01b-recomputed). | parent: HA01b-recomputed |\n"
        "| HA06 | SUPERSEDED-by-HA06b (absolute-threshold mis-cal -> z-score). | [REJECTED.md 2026-06-07](../../../../REJECTED.md) |\n"
        "| HA07 | SUPERSEDED-by-proxy (FR245 HRV hardware-blocked; HA07c proxy). | [REJECTED.md Appendix](../../../../REJECTED.md) |\n"
        "| HA08 | SUPERSEDED-by-proxy (same FR245 hardware blocker; HA08c proxy). | [REJECTED.md Appendix](../../../../REJECTED.md) |\n"
        "| S02b | SHELVED-BLOCKED-BY-S02. | [REJECTED.md Appendix](../../../../REJECTED.md) |\n"
        "| K01 | NOT-APPLICABLE (cross-era contrast - the era split IS the predictor). | [K01 result.md](../../../hypotheses/K01-crash-depth/result.md) |\n"
        "| K02 | NOT-APPLICABLE (same as K01). | [K02 result.md](../../../hypotheses/K02-crash-duration/result.md) |\n"
        "| threshold-monotonicity diagnostics (HA01c-v2, HA06b-v2, HA07d, HA07d-v2, HA10, HA10-v2, HA11-v2) | inherit cross-check from parent HA per testing playbook. | parents covered above |\n"
        "\n"
        "**R14-v2 closed** (2026-06-30): HA01c (effective_exertion rank shock; primary scope) "
        "and H03 (sleep_efficiency drop; stretch scope) are now COMPUTED and reported in the "
        "Sec 2 table + Sec 3 narrative above; they are no longer deferred. HA06b is covered as "
        "stretch. The remaining NOT-BACKSTOPPED HAs from stocktake Sec 5 close in a future "
        "R14-v3 session.\n"
    )
    lines.append("---\n")

    # Sec 6 Implications for synthesis_structure_map
    lines.append("## 6. Implications for the synthesis_structure_map (descriptive only)\n")
    lines.append(
        "Per Sec 5.7 bullet 7: this cross-check **does not** auto-promote any HA's "
        "synthesis-structure-map standing. Reading is user-owned.\n"
        "\n"
        "Stocktake-style enumeration of HAs whose assumption-cell A8 (`single-pool primary "
        "preserved per train_validate_split_fate.md`) is now backstopped by this cross-check "
        "(potentially eligible to transition NOT-BACKSTOPPED -> Stage D TRUSTED on A8, "
        "pending review of other NOT-BACKSTOPPED cells per stocktake Sec 5):\n"
        "\n"
    )
    primary_names = list(results["primary"].keys())
    stretch_names = list(results["stretch"].keys())
    all_evaluated = primary_names + stretch_names
    for name in all_evaluated:
        res = results.get("primary", {}).get(name) or results.get("stretch", {}).get(name)
        div = res.get("divergence", "n/a") if res else "n/a"
        lines.append(f"- **{name}**: A8 cell backstopped by this cross-check ({div}).\n")
    lines.append(
        "\n"
        "**Important**: backstopping A8 alone does not move an HA to Stage D TRUSTED; "
        "per stocktake Sec 5 most older HAs also carry Shared gap 1 (per-channel ACF / "
        "E[L]\\* never run on the pre-MD verdicts) + Shared gap 3 (per-cell missingness "
        "audit). Those remain to be closed by separate descriptive runs.\n"
        "\n"
        "Of the 16 HAs that stocktake Sec 3 Shared gap 2 enumerated, this cross-check "
        f"closes A8 on {len(all_evaluated)} of them (HA01c + H03 added in the 2026-06-30 R14-v2 "
        f"extension); remaining {16 - len(all_evaluated)} "
        f"(H02, H02d, H03b, HA01b-diag) continue to carry "
        f"NOT-BACKSTOPPED A8 until a future descriptive backstop arrives via another path. "
        f"H02 and H02d are SUPERSEDED in the registry (so closure is procedural rather than "
        f"empirical); H03b is RETIRED per stocktake Sec 9; HA01b-diag inherits from HA01b-recomputed which IS "
        f"covered. There are no genuinely uncovered HAs remaining in the Shared gap 2 set.\n"
    )
    lines.append("---\n")

    # Sec 7 Caveats
    lines.append("## 7. Caveats per CONVENTIONS Sec 4.1 + Sec 4.2\n")
    lines.append(
        "- **Operationalised cross-check, no causal claim** (Sec 4.1). The single-pool numbers "
        "characterise the same operand evaluated on a different reference frame; they do NOT "
        "claim what causes the divergence or convergence.\n"
        "- **Layer 1 descriptive** (Sec 2.1). No falsification bar in this cross-check itself; "
        "the per-HA verdicts evaluated here are the HAs' own locked bars applied to single-pool "
        "numbers. No new inferential commitment.\n"
        "- **Locked verdicts UNCHANGED** regardless of cross-check outcome per Sec 5.7 bullet 6. "
        "The HA `result.md` files remain as historical evidence for the era-split framework. "
        "This cross-check produces descriptive overlays; it does NOT re-lock.\n"
        "- **User-owned decision on any follow-up** per Sec 5.7 bullet 7. New pre-reg / "
        "methodology revision / per-HA footnote / R14-v2 scope expansion are separate sessions.\n"
        "- **Block-permutation null + stationary bootstrap CI** uses E[L]=7 per project default. "
        "Per stocktake Sec 5 Shared gap 1, several channels have not had their per-channel data-driven "
        "E[L]\\* characterised on Stratum 4 (only `stress_mean_sleep` and "
        "`stress_low_motion_min_count_S60_Mlow` are landed at the Strand A level). A "
        "factor-of-2 deviation from E[L]=7 on a specific channel could shift specific p-values; "
        "the discrimination point estimate is less sensitive to this.\n"
        "- **Cross-check inherits the locked HA's null reference scheme** (200 non-overlapping random "
        "windows seeded `20260605`) for per-HA continuity. The new framework's choice of null "
        "(block-permutation at E[L]=7) operates on top of the same reference dates; the p-value "
        "reported is therefore the new-framework p-value on the same window set.\n"
        "- **`per_day_master.csv` snapshot at run time**: the per-day master is the single source "
        "of truth for the operand re-extraction; HA-specific operand details may differ slightly "
        "from the original locked test scripts that read from cached extraction CSVs (e.g. HA01b "
        "originally reads from `activity_features_daily.csv`; HA11 originally reads from "
        "`udip_counts.csv`). The per_day_master columns are the project's canonical consolidated "
        "source per [DATA_DICTIONARY.md](../../../../DATA_DICTIONARY.md); using them in the "
        "cross-check is the consistent choice but introduces a small operand-routing difference "
        "from the locked tests.\n"
        "- **No anchoring on the HA01b legacy +17.3 pp validate divergence** per Sec 5.7 bullet 8. "
        "The canonical HA01b is the lagged-baseline recomputed version (REFUTED both eras at "
        "+5.8 / +4.0 pp), not the v3.1 rolling-baseline artefact.\n"
    )
    lines.append("---\n")

    # Sec 8 Verification log
    lines.append("## 8. Verification log\n")
    lines.append(
        "- **R14-v2 extension (2026-06-30)**: HA01c (primary) + H03 (stretch) added to scope "
        "under the SAME recipe as the original 10 HAs (full Stratum 4 single pool, "
        "n_crash_episodes=29; block-permutation null E[L]=7; B=10,000; null sample seed "
        "`20260605`; bootstrap/perm seed `20260624`; N_std primary 1.5; leadup 4 days for HA01c, "
        "7 days for H03). HA01c operand = `eff_exertion_rank_lagged >= 0.75` (the v3.2 _lagged "
        "column the locked HA01c test used; per CONVENTIONS §3.2 the `_lagged_lcera` variant "
        "is near-identical on the all-LC Stratum 4 pool). H03 operand = 7d-leadup mean "
        "sleep-efficiency minus [d-97, d-8] trimmed baseline <= -0.05; efficiency reconstructed "
        "from per_day_master `(sleep_deep_min + sleep_light_min) / (deep + light + awake + "
        "unmeasurable)` (no `sleep_rem_min` on FR245 per DATA_DICTIONARY.md, so light absorbs REM "
        "and the reconstruction is construction-equivalent to the locked test's deep+light+rem). "
        "§3.4 crash-drop sensitivity: the single pool inherits the same 29-episode crash_v2 "
        "set; no per-episode drop sweep is re-run at the cross-check layer (the locked HA verdicts "
        "carry their own sensitivity records).\n"
        f"- **As-of-date**: {meta['as_of_date']} (Stratum 4 right edge for this run).\n"
        f"- **Stratum 4 start**: {meta['stratum_4_start']}.\n"
        f"- **n_days in Stratum 4 master**: {meta['n_days_master_in_S4']}.\n"
        f"- **n_crash_episodes in Stratum 4 single pool**: {meta['n_crash_episodes_in_S4']}.\n"
        f"- **Null sample sizes**: 4d leadup n={meta['n_null_4d']}; "
        f"7d leadup n={meta['n_null_7d']}; 3d leadup n={meta['n_null_3d']}.\n"
        f"- **Block length E[L]**: {meta['block_length_E_L']} (project default per "
        f"`permutation_null_block_length.md`).\n"
        f"- **n_bootstrap / n_permutations**: {meta['n_bootstrap']:,}.\n"
        f"- **Bootstrap + permutation seed**: `{meta['seed']}` (per handoff Sec 2.4).\n"
        f"- **Null sample seed**: `{meta['legacy_null_seed']}` (inherited from legacy HA pre-reg pattern; "
        f"matches the locked HA reference frames).\n"
        f"- **N_std primary**: {meta['n_std_primary']} (per locked HA pre-reg primary tier).\n"
        f"- **Leadup days primary**: {meta['leadup_days_primary']}.\n"
        f"- **Inference helpers**: [`analyses/_utils/inference.py`](../../../_utils/inference.py) "
        f"(`stationary_bootstrap_ci`, `permutation_pvalue`, `compute_data_driven_block_length`).\n"
        f"- **Run timestamp (UTC)**: {meta['run_at']}.\n"
        f"- **Operand-source path**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` "
        f"+ `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv`.\n"
    )
    # Locked HA result.md commits + dates
    lines.append("\n**Locked HA `result.md` cross-references** (NOT modified by this cross-check):\n\n")
    for name, locked in LOCKED_VERDICTS.items():
        lines.append(f"- {name}: [`{locked['result_md_path']}`](../../../../{locked['result_md_path']}). {locked['note']}\n")
    lines.append(
        "\n---\n"
        "\n"
        "*End of findings.*\n"
    )

    out_path = HERE / "findings.md"
    out_path.write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
