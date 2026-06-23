"""HA-C3 r2 - Stage 2: convex stress -> fatigue (Wiggers C3 Tier 1).

Implements the LOCKED r2 HA-C3 pre-registration (hypothesis.md LOCKED
2026-06-23 by user acceptance, commit de22b68). Tests Wiggers C3
verbatim "the stress -> fatigue relationship is non-linear / convex - a
30 -> 40 step costs more than a 20 -> 30 step" on per-day same-day
mapping all_day_stress_avg x gevoelscore.

Headline cell: unmedicated x 5-bin x gevoelscore bin-mean x 3-condition
gated outcome (Jonckheere-Terpstra monotone + second-difference
convexity contrast S + spline non-linearity) x block-permutation null
E[L]=7 (B=10,000).

3-condition gated verdict per spec 5.1:
  SUPPORTED iff (a) + (b) + (c) all MET in prior direction;
  PARTIAL iff exactly 2-of-3 MET;
  REJECTED iff <=1-of-3 MET OR any wrong-direction firing.

Sensitivity arms (per spec 4.8) reported alongside:
  - spec 5.B dose-adjusted cross-phase variant
    (predictor_adj = predictor - 0.57 * dose_plasma_mg)
  - crash-drop sensitivity (CONVENTIONS 3.4)
  - train/validate M3 overlay (per train_validate_split_fate.md 5)
  - t+1 lagged variant (descriptive cross-test alignment)
  - within-consolidation spec 5.A replication if cells survive 30-bar

Per spec 4.7 r2 amendment: two E[L]* checks (linear-residual + bin-label).

Modes:
  python test.py --dry-run   spec 7.5 sanity gates only.
                              HALT on Gate 1 (bin n<30) / Gate 2/3
                              (distribution sanity) / Gate 4 (total n<100).
  python test.py             dry-run first, halt on failure, else full
                              run; emits result.md + summary.json.

ASCII-only stdout per session handoff; markdown may use unicode.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline

# === Path setup for shared _utils.inference ============================

HERE = Path(__file__).resolve().parent
UTILS_DIR = HERE.parent.parent / "_utils"
if str(UTILS_DIR) not in sys.path:
    sys.path.insert(0, str(UTILS_DIR))

from inference import (  # noqa: E402
    compute_data_driven_block_length,
    holm_step_down,
)

# === Constants per locked r2 hypothesis.md =============================

# Seed: pre-reg 4.7 locked RANDOM_SEED=20260622 (handoff brief used
# 20260623 as a paraphrase; the LOCKED pre-reg binds).
RANDOM_SEED = 20260622
BOOTSTRAP_E_L = 7
B_HEADLINE = 10_000

# spec 4.4 dose-adjustment coefficient
# (citalopram_dose_response_stress_mean_sleep.md 5.6.1)
DOSE_BETA_PER_MG = 0.57

# spec 4.5.1 + 5.1 verdict bars
P_BAR = 0.05
S_NEG_BAR = 0.0
SPLINE_MIDPOINT_COUNT_BAR = 3  # >= 3 of 4 midpoints (B1's x=10 dropped)

# spec 4.1 bin edges (left-inclusive, right-exclusive except B5)
# [0,20), [20,30), [30,40), [40,60), [60,100]
BIN_EDGES = [0.0, 20.0, 30.0, 40.0, 60.0, 100.0]
BIN_LABELS = ["B1[0,20)", "B2[20,30)", "B3[30,40)", "B4[40,60)", "B5[60,100]"]
# Bin midpoints used for spline second-derivative check
# (B1 x=10 dropped per r2 amendment; natural-cubic boundary forces ~0)
BIN_MIDPOINTS_FULL = [10.0, 25.0, 35.0, 50.0, 80.0]
BIN_MIDPOINTS_FOR_SPLINE = BIN_MIDPOINTS_FULL[1:]  # 25, 35, 50, 80

# spec 4.5.1(b) Option-A textbook orthogonal quadratic contrast
# (verified at lock: dot product with linear (-2,-1,0,+1,+2) = 0)
COMPANION_CONTRAST = np.asarray([+2, -1, -2, -1, +2], dtype=float)
LINEAR_CONTRAST = np.asarray([-2, -1, 0, +1, +2], dtype=float)
assert int(np.dot(COMPANION_CONTRAST, LINEAR_CONTRAST)) == 0, \
    "Companion contrast must be orthogonal to linear contrast at lock"

# spec 7.5 sanity gates
MIN_BIN_N = 30
MIN_TOTAL_N = 100
GATE2_STRESS_MEDIAN_RANGE = (20.0, 60.0)
GATE3_GEVOELSCORE_MEDIAN_RANGE = (3.0, 6.0)

# spec 4.6 crash-drop flag threshold
CRASH_DROP_S_FLAG = "sign_change"  # full S<0 but crash-dropped S>=0, or vice versa

# spec 4.7 E[L]* factor-of-2 deviation
EL_DEVIATION_FACTOR = 0.5

# spec 4.3 + 6 exclusions
LC_ERA_START = date(2022, 4, 4)
UNMEDICATED_END_INCL = date(2024, 4, 8)
APRIL2024_CLUSTER_START = date(2024, 4, 9)
APRIL2024_CLUSTER_END_INCL = date(2024, 4, 16)
# Garmin device-baseline warmup: first 21 days of has_garmin_uds=True
DEVICE_BASELINE_DAYS = 21
# Train/validate split (M3 overlay only)
TRAIN_END = date(2023, 12, 31)
VALIDATE_START = date(2024, 1, 1)
# Consolidation phase (per citalopram_phase_stratification 3): post-buildup
CONSOLIDATION_START = date(2024, 5, 7)
CONSOLIDATION_END_INCL = date(2026, 2, 5)

# Spec commit (r2 lock; updated at lock-commit time if needed)
R2_SPEC_COMMIT = "de22b68"

# Paths
DATA_ROOT = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH",
    r"C:\Users\Gebruiker\Documents\gevoelscore-data"))
MASTER_CSV = DATA_ROOT / "unified" / "per_day_master.csv"

OUT_RESULT_MD = HERE / "result.md"
OUT_SUMMARY_JSON = HERE / "summary.json"
OUT_DRYRUN_MD = HERE / "dry-run-report.md"


# === Loaders ===========================================================

def parse_float(s):
    if s == "" or s is None:
        return None
    try:
        v = float(s)
        if math.isnan(v):
            return None
        return v
    except (ValueError, TypeError):
        return None


def load_master() -> dict:
    """Load per_day_master.csv into {date: row-dict}."""
    needed = (
        "date", "gevoelscore", "all_day_stress_avg",
        "is_crash", "has_garmin_uds", "dose_plasma_mg",
    )
    out: dict = {}
    with MASTER_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                d = date.fromisoformat(row["date"])
            except (KeyError, ValueError):
                continue
            out[d] = {k: row.get(k, "") for k in needed}
    return out


def find_device_baseline_cutoff(master: dict) -> date | None:
    """Return the last date of the first DEVICE_BASELINE_DAYS days of
    has_garmin_uds=True, or None if not found. The exclusion is for
    dates <= this returned date."""
    n_uds = 0
    for d in sorted(master.keys()):
        row = master.get(d) or {}
        if (row.get("has_garmin_uds", "") or "").strip().lower() == "true":
            n_uds += 1
            if n_uds == DEVICE_BASELINE_DAYS:
                return d
    return None


# === Eligibility (spec 4.3 + 6) ========================================

def assign_bin(s: float) -> int | None:
    """Return bin index 0..4 for stress value s; None if outside [0, 100]."""
    if s < 0.0 or s > 100.0:
        return None
    for i in range(5):
        lo = BIN_EDGES[i]
        hi = BIN_EDGES[i + 1]
        if i == 4:
            if lo <= s <= hi:
                return i
        else:
            if lo <= s < hi:
                return i
    return None


def day_passes_gate(d: date, row: dict, baseline_cutoff: date | None,
                    phase: str = "unmedicated",
                    require_gevoelscore: bool = True,
                    require_stress: bool = True) -> bool:
    """spec 4.3 day-validity gate.

    phase: 'unmedicated' (default; primary), 'consolidation', or 'all'
           (for spec 5.B cross-phase sensitivity arm).
    """
    if d < LC_ERA_START:
        return False
    if phase == "unmedicated" and d > UNMEDICATED_END_INCL:
        return False
    if phase == "consolidation":
        if not (CONSOLIDATION_START <= d <= CONSOLIDATION_END_INCL):
            return False
    # spec 4.3 + 6: April 2024 cluster always excluded
    if APRIL2024_CLUSTER_START <= d <= APRIL2024_CLUSTER_END_INCL:
        return False
    # spec 6: first 21 device-baseline days
    if baseline_cutoff is not None and d <= baseline_cutoff:
        return False
    s = parse_float(row.get("all_day_stress_avg", ""))
    if require_stress and (s is None or s < 0.0 or s > 100.0):
        return False
    if require_gevoelscore:
        g = parse_float(row.get("gevoelscore", ""))
        if g is None:
            return False
    return True


def build_pool(master: dict, baseline_cutoff: date | None,
               phase: str = "unmedicated",
               dose_adjusted: bool = False,
               lag_t_plus_1: bool = False,
               drop_crashes: bool = False) -> dict:
    """Build temporal pool of (date, stress, gevoelscore, bin, is_crash).

    For dose_adjusted=True (spec 5.B): predictor_adj = raw - DOSE_BETA * dose_plasma_mg.
    For lag_t_plus_1=True (spec 4.8): outcome is gevoelscore[T+1], predictor is stress[T].
    """
    rows = []
    dates_sorted = sorted(master.keys())
    for d in dates_sorted:
        row = master.get(d) or {}
        if not day_passes_gate(d, row, baseline_cutoff, phase=phase):
            continue
        if drop_crashes and (row.get("is_crash", "") or "").strip().lower() == "true":
            continue
        s_raw = parse_float(row["all_day_stress_avg"])
        if lag_t_plus_1:
            d1 = d + timedelta(days=1)
            row1 = master.get(d1) or {}
            g = parse_float(row1.get("gevoelscore", ""))
            if g is None:
                continue
        else:
            g = parse_float(row["gevoelscore"])
        if dose_adjusted:
            dose = parse_float(row.get("dose_plasma_mg", "")) or 0.0
            s_use = s_raw - DOSE_BETA_PER_MG * dose
        else:
            s_use = s_raw
        b = assign_bin(s_use)
        if b is None:
            continue
        rows.append({
            "date": d, "stress_raw": s_raw, "stress_use": s_use,
            "gevoelscore": g, "bin": b,
            "is_crash": (row.get("is_crash", "") or "").strip().lower() == "true",
        })
    return {
        "dates": np.asarray([r["date"] for r in rows]),
        "stress_raw": np.asarray([r["stress_raw"] for r in rows], dtype=float),
        "stress_use": np.asarray([r["stress_use"] for r in rows], dtype=float),
        "gevoelscore": np.asarray([r["gevoelscore"] for r in rows], dtype=float),
        "bin": np.asarray([r["bin"] for r in rows], dtype=int),
        "is_crash": np.asarray([r["is_crash"] for r in rows], dtype=bool),
        "n": len(rows),
    }


# === Bin descriptives ===================================================

def bin_descriptives(pool: dict) -> dict:
    bin_n = np.zeros(5, dtype=int)
    bin_mean = np.full(5, float("nan"))
    bin_sd = np.full(5, float("nan"))
    bin_median = np.full(5, float("nan"))
    for b in range(5):
        mask = pool["bin"] == b
        n_b = int(mask.sum())
        bin_n[b] = n_b
        if n_b > 0:
            vals = pool["gevoelscore"][mask]
            bin_mean[b] = float(vals.mean())
            bin_median[b] = float(np.median(vals))
            if n_b > 1:
                bin_sd[b] = float(vals.std(ddof=1))
    return {
        "bin_n": bin_n.tolist(),
        "bin_mean": [None if math.isnan(m) else float(m) for m in bin_mean],
        "bin_sd": [None if math.isnan(s) else float(s) for s in bin_sd],
        "bin_median": [None if math.isnan(m) else float(m) for m in bin_median],
    }


def stationary_bootstrap_ci_bin_means(pool: dict, B: int,
                                       expected_block_length: int,
                                       rng: np.random.Generator) -> dict:
    """95% CI on bin-mean via stationary bootstrap (date-resampling).

    Per pre-reg 4.5.2: CI per bin from stationary bootstrap at E[L]=7.
    """
    n = pool["n"]
    if n == 0:
        return {f"B{b+1}": (None, None) for b in range(5)}
    p_geom = 1.0 / expected_block_length
    g = pool["gevoelscore"]
    bins = pool["bin"]
    # Per-bin bootstrap means matrix [B, 5]
    boot_means = np.full((B, 5), float("nan"))
    for b_iter in range(B):
        # stationary bootstrap of (bin, gevoelscore) tuple by date
        idx = np.empty(n, dtype=np.int64)
        i = 0
        while i < n:
            start = int(rng.integers(0, n))
            L = int(rng.geometric(p_geom))
            end = min(i + L, n)
            for j in range(end - i):
                idx[i + j] = (start + j) % n
            i = end
        bins_b = bins[idx]
        g_b = g[idx]
        for bi in range(5):
            mask = bins_b == bi
            if mask.any():
                boot_means[b_iter, bi] = float(g_b[mask].mean())
    cis: dict[str, tuple] = {}
    for bi in range(5):
        col = boot_means[:, bi]
        col = col[~np.isnan(col)]
        if len(col) >= 2:
            cis[f"B{bi+1}"] = (
                float(np.quantile(col, 0.025)),
                float(np.quantile(col, 0.975)),
            )
        else:
            cis[f"B{bi+1}"] = (None, None)
    return cis


# === Statistics =========================================================

def jonckheere_terpstra(values_by_bin: list[np.ndarray]) -> dict:
    """One-sided Jonckheere-Terpstra trend test.

    Tests H0: no trend vs H1: monotone-decreasing across bins.
    Test statistic J = sum_{i<j} U_ij where U_ij counts pairs
    (x_i, y_j) with x_i > y_j (decreasing); we report J* standardised
    by null mean + SD (asymptotic-normal approximation as a descriptive
    statistic; the block-permutation null on the actual test below is
    the inferential p-value driver).

    Returns dict with J_obs, J_star (standardised), and SD components.
    """
    K = len(values_by_bin)
    if K < 2:
        return {"J_obs": float("nan"), "J_star": float("nan"),
                "n_per_bin": [len(v) for v in values_by_bin]}
    # Sum of U_ij counts (decreasing direction: count y_i > y_j for i<j)
    J = 0.0
    n = [len(v) for v in values_by_bin]
    N = sum(n)
    for i in range(K - 1):
        if n[i] == 0:
            continue
        for j in range(i + 1, K):
            if n[j] == 0:
                continue
            xi = values_by_bin[i]
            xj = values_by_bin[j]
            # Number of (a, b) with a in xi, b in xj, a > b (decreasing)
            xj_sorted = np.sort(xj)
            less = np.searchsorted(xj_sorted, xi, side="left")
            # less[k] = number of xj < xi[k] = pairs with xi[k] > b
            # For ties (xi[k] == b): split 0.5
            equal = (np.searchsorted(xj_sorted, xi, side="right")
                     - np.searchsorted(xj_sorted, xi, side="left"))
            J += float(less.sum()) + 0.5 * float(equal.sum())
    # Mean / SD under H0 (no-trend, ignoring ties for simplicity; ties
    # adjustment is small at gevoelscore granularity)
    mu_J = (N * N - sum(ni * ni for ni in n)) / 4.0
    var_J = (N * N * (2 * N + 3) - sum(ni * ni * (2 * ni + 3) for ni in n)) / 72.0
    sd_J = math.sqrt(var_J) if var_J > 0 else float("nan")
    J_star = (J - mu_J) / sd_J if sd_J and not math.isnan(sd_J) else float("nan")
    return {
        "J_obs": float(J), "mu_J": float(mu_J), "sd_J": float(sd_J),
        "J_star": float(J_star), "n_per_bin": n,
    }


def second_diff_S(bin_means: np.ndarray) -> float:
    """spec 4.5.1(b) S = (D2_2 + D2_3 + D2_4) / 3 where D2_i = m_{i+1} - 2*m_i + m_{i-1}."""
    if np.any(np.isnan(bin_means)) or len(bin_means) < 5:
        return float("nan")
    d2 = []
    for i in (1, 2, 3):
        d2.append(bin_means[i + 1] - 2.0 * bin_means[i] + bin_means[i - 1])
    return float(np.mean(d2))


def companion_contrast(bin_means: np.ndarray) -> float:
    """spec 4.5.1(b) companion: c . m with c = (+2,-1,-2,-1,+2)."""
    if np.any(np.isnan(bin_means)) or len(bin_means) < 5:
        return float("nan")
    return float(np.dot(COMPANION_CONTRAST, bin_means))


def stationary_bootstrap_indices(n: int, p: float,
                                  rng: np.random.Generator) -> np.ndarray:
    indices = np.empty(n, dtype=np.int64)
    i = 0
    while i < n:
        start = int(rng.integers(0, n))
        L = int(rng.geometric(p))
        end = min(i + L, n)
        for j in range(end - i):
            indices[i + j] = (start + j) % n
        i = end
    return indices


def block_permutation_three_conditions(pool: dict, B: int,
                                        expected_block_length: int,
                                        rng: np.random.Generator) -> dict:
    """Compute (a) J* + (b) S + (c) spline F via block-permutation null
    per spec 4.7.

    Permutation target: bin_label sequence is resampled via stationary
    bootstrap (geometric block length E[L]=7), keeping gevoelscore in
    original temporal position. This breaks the (bin -> gevoelscore)
    relationship while preserving the within-gevoelscore autocorrelation.
    """
    n = pool["n"]
    p_geom = 1.0 / expected_block_length
    g = pool["gevoelscore"]
    bins_obs = pool["bin"]

    # Observed values
    obs_means = _means_per_bin(g, bins_obs)
    obs_jt = jonckheere_terpstra(
        [g[bins_obs == b] for b in range(5)])
    obs_J_star = obs_jt["J_star"]
    obs_S = second_diff_S(obs_means)
    obs_companion = companion_contrast(obs_means)
    obs_spline_F, obs_spline_secderiv = _spline_F_and_secderiv(pool)

    # Build null distributions
    null_J_star = np.full(B, float("nan"))
    null_S = np.full(B, float("nan"))
    null_F = np.full(B, float("nan"))
    null_companion = np.full(B, float("nan"))

    # spec 4.7 note: permute bin_label sequence (the actual permutation
    # target). Keep gevoelscore in original position.
    for b_iter in range(B):
        idx = stationary_bootstrap_indices(n, p_geom, rng)
        bins_null = bins_obs[idx]
        means_null = _means_per_bin(g, bins_null)
        if np.any(np.isnan(means_null)):
            # If a bin has zero observations in this null draw, fill its
            # mean with the pool-grand-mean (avoids NaN propagation in
            # the test statistic). Per spec discipline this is the
            # canonical handling for empty-bin null draws.
            grand = float(g.mean())
            means_null = np.where(np.isnan(means_null), grand, means_null)
        # (a) JT
        jt = jonckheere_terpstra([g[bins_null == bb] for bb in range(5)])
        null_J_star[b_iter] = jt["J_star"]
        # (b) S
        null_S[b_iter] = second_diff_S(means_null)
        null_companion[b_iter] = companion_contrast(means_null)
        # (c) spline F: need the per-point predictor for the spline.
        # We use the bin-MIDPOINT as the effective stress value for each
        # day under the null label (operationally consistent with using
        # bin labels as the permutation target).
        # Build a "pseudo-stress" via bin midpoints, then refit.
        pseudo_stress = np.asarray([BIN_MIDPOINTS_FULL[bn] for bn in bins_null],
                                   dtype=float)
        F_null = _spline_F_from_stress_g(pseudo_stress, g)
        null_F[b_iter] = F_null

    # Compute observed F similarly with bin midpoints (consistent
    # treatment between observed + null)
    obs_pseudo_stress = np.asarray([BIN_MIDPOINTS_FULL[bn] for bn in bins_obs],
                                   dtype=float)
    obs_F_midpoint = _spline_F_from_stress_g(obs_pseudo_stress, g)

    # Empirical one-sided p-values
    # (a) decreasing: under H1 J_star is negative (decreasing trend
    # accumulates fewer increasing pairs); p_a = (1 + #{J*_null <= J*_obs}) / (B+1)
    n_le = int((null_J_star <= obs_J_star).sum())
    p_a = (1 + n_le) / (B + 1)
    # (b) convex: under H1 S < 0; p_b = (1 + #{S_null <= S_obs}) / (B+1)
    n_le_s = int((null_S <= obs_S).sum())
    p_b = (1 + n_le_s) / (B + 1)
    # (c) non-linearity F: under H1 F_obs is LARGE (more non-linear
    # variance captured); p_c = (1 + #{F_null >= F_obs}) / (B+1)
    n_ge_f = int((null_F >= obs_F_midpoint).sum())
    p_c = (1 + n_ge_f) / (B + 1)
    # companion descriptive direction
    n_le_c = int((null_companion <= obs_companion).sum())
    p_companion = (1 + n_le_c) / (B + 1)

    # Parametric F (descriptive only per pre-reg 4.5.1(c))
    parametric_F, parametric_p = _spline_F_parametric(pool)

    return {
        "obs": {
            "J_star": float(obs_J_star) if not math.isnan(obs_J_star) else None,
            "S": float(obs_S) if not math.isnan(obs_S) else None,
            "spline_F_block_perm_target": float(obs_F_midpoint) if not math.isnan(obs_F_midpoint) else None,
            "spline_F_continuous_predictor": float(obs_spline_F) if not math.isnan(obs_spline_F) else None,
            "spline_secderiv_at_midpoints": [
                float(x) if not math.isnan(x) else None for x in obs_spline_secderiv
            ],
            "companion_contrast": float(obs_companion) if not math.isnan(obs_companion) else None,
            "bin_means": [None if math.isnan(m) else float(m) for m in obs_means],
        },
        "null_summaries": {
            "J_star": {
                "p2.5": float(np.nanquantile(null_J_star, 0.025)),
                "p50": float(np.nanmedian(null_J_star)),
                "p97.5": float(np.nanquantile(null_J_star, 0.975)),
            },
            "S": {
                "p2.5": float(np.nanquantile(null_S, 0.025)),
                "p50": float(np.nanmedian(null_S)),
                "p97.5": float(np.nanquantile(null_S, 0.975)),
            },
            "spline_F": {
                "p2.5": float(np.nanquantile(null_F, 0.025)),
                "p50": float(np.nanmedian(null_F)),
                "p97.5": float(np.nanquantile(null_F, 0.975)),
            },
            "companion_contrast": {
                "p2.5": float(np.nanquantile(null_companion, 0.025)),
                "p50": float(np.nanmedian(null_companion)),
                "p97.5": float(np.nanquantile(null_companion, 0.975)),
            },
        },
        "p_values": {
            "p_a_jonckheere_decreasing": float(p_a),
            "p_b_S_convex": float(p_b),
            "p_c_spline_nonlinearity": float(p_c),
            "p_companion_orthogonal_quadratic": float(p_companion),
        },
        "parametric_F_descriptive": {
            "F": float(parametric_F) if not math.isnan(parametric_F) else None,
            "p_parametric": float(parametric_p) if not math.isnan(parametric_p) else None,
        },
    }


def _means_per_bin(g: np.ndarray, bins: np.ndarray) -> np.ndarray:
    """Vectorised per-bin mean; NaN where bin is empty."""
    out = np.full(5, float("nan"))
    for b in range(5):
        m = bins == b
        if m.any():
            out[b] = float(g[m].mean())
    return out


def _spline_F_and_secderiv(pool: dict) -> tuple[float, list[float]]:
    """Natural cubic spline regression on raw (stress, gevoelscore);
    returns F-stat (full vs linear-only) and second-derivative at the
    4 bin midpoints used for the sign check (per spec 4.5.1(c) r2)."""
    s = pool["stress_use"]
    g = pool["gevoelscore"]
    if len(s) < 6:
        return float("nan"), [float("nan")] * 4
    # Aggregate to bin-mean spline (5 knots at midpoints)
    # Compute bin-means; if any bin empty, exclude from spline fit
    means = _means_per_bin(g, pool["bin"])
    valid = ~np.isnan(means)
    n_valid = int(valid.sum())
    if n_valid < 4:
        return float("nan"), [float("nan")] * 4
    x_full = np.asarray(BIN_MIDPOINTS_FULL, dtype=float)
    x_fit = x_full[valid]
    y_fit = means[valid]
    # Natural cubic spline (CubicSpline 'natural' bc -> S''=0 at endpoints)
    try:
        cs = CubicSpline(x_fit, y_fit, bc_type="natural")
    except Exception:
        return float("nan"), [float("nan")] * 4
    # Continuous predictor F-statistic via residual SS comparison
    F = _spline_F_from_stress_g(s, g)
    # Second derivative at midpoints (B2..B5: 25, 35, 50, 80)
    sd = []
    cs2 = cs.derivative(2)
    for x in BIN_MIDPOINTS_FOR_SPLINE:
        try:
            sd.append(float(cs2(x)))
        except Exception:
            sd.append(float("nan"))
    return F, sd


def _spline_F_from_stress_g(s: np.ndarray, g: np.ndarray) -> float:
    """F-statistic comparing natural-cubic-spline-with-4-internal-knots
    (knots at 20, 30, 40, 60) against linear-only fit, by residual SS.

    Uses truncated-power basis for the natural cubic spline.
    """
    if len(s) < 6:
        return float("nan")
    n = len(s)
    knots = [20.0, 30.0, 40.0, 60.0]
    # Linear-only model: design [1, s]
    X_lin = np.column_stack([np.ones(n), s])
    # Natural-cubic spline with K internal knots has K-1 non-linear
    # basis functions when intercept + linear are explicit.
    # Use truncated-power basis: phi_k(x) = (x - knot_k)_+ ^ 3, then
    # difference to enforce natural BC (S''=0 outside [knot_1, knot_K]):
    # natural spline basis: d_k(x) = (phi_k(x) - phi_K(x)) / (knot_K - knot_k)
    # for k=1..K-1, after subtracting d_{K-1}-equivalent etc.
    # Simpler implementation: B-spline-style truncated power with
    # natural constraint. We use the Wood (2017) implementation:
    K = len(knots)
    def trunc_cube(x, k):
        d = x - k
        return np.where(d > 0, d * d * d, 0.0)

    def natural_basis(s):
        # First (K-2) "d_k" terms; standard natural spline basis from
        # Hastie/Tibshirani ESL 5.2.1 eq (5.5):
        # d_k(X) = ( (X - knot_k)+^3 - (X - knot_K)+^3 ) / (knot_K - knot_k)
        # then N_k(X) = d_k(X) - d_{K-1}(X), for k=1..K-2.
        # Together with [1, X] this gives K basis functions and K knots.
        K_local = len(knots)
        d_last = (trunc_cube(s, knots[K_local - 1])) / 1.0  # for division by 0 issue handled below
        cols = []
        # compute d_k for k=0..K-2 (here knots index 0..K-1)
        d = []
        for k in range(K_local - 1):
            denom = knots[K_local - 1] - knots[k]
            d_k = (trunc_cube(s, knots[k]) - trunc_cube(s, knots[K_local - 1])) / denom
            d.append(d_k)
        # N_k = d_k - d_{K-2} for k=0..K-3
        for k in range(K_local - 2):
            cols.append(d[k] - d[K_local - 2])
        return np.column_stack(cols) if cols else np.zeros((n, 0))

    # Full design: [1, s, natural-basis (K-2 = 2 cols for K=4 knots)]
    NB = natural_basis(s)
    X_full = np.column_stack([np.ones(n), s, NB])

    # OLS residual sums
    try:
        beta_lin, ssr_lin, _, _ = np.linalg.lstsq(X_lin, g, rcond=None)
    except np.linalg.LinAlgError:
        return float("nan")
    try:
        beta_full, ssr_full, _, _ = np.linalg.lstsq(X_full, g, rcond=None)
    except np.linalg.LinAlgError:
        return float("nan")
    # lstsq returns ssr as 1D array if applicable; compute manually for stability
    resid_lin = g - X_lin @ beta_lin
    rss_lin = float((resid_lin * resid_lin).sum())
    resid_full = g - X_full @ beta_full
    rss_full = float((resid_full * resid_full).sum())
    p_lin = X_lin.shape[1]
    p_full = X_full.shape[1]
    df_diff = p_full - p_lin  # = K - 2 = 2 for K=4 knots
    df_resid = n - p_full
    if df_diff <= 0 or df_resid <= 0 or rss_full <= 0:
        return float("nan")
    F = ((rss_lin - rss_full) / df_diff) / (rss_full / df_resid)
    return float(F)


def _spline_F_parametric(pool: dict) -> tuple[float, float]:
    """Parametric F + p (descriptive only per spec 4.5.1(c))."""
    from scipy import stats as sps
    s = pool["stress_use"]
    g = pool["gevoelscore"]
    if len(s) < 6:
        return float("nan"), float("nan")
    F = _spline_F_from_stress_g(s, g)
    if math.isnan(F):
        return float("nan"), float("nan")
    n = len(s)
    df_diff = 2  # K-2 with K=4 knots
    df_resid = n - 4  # intercept + linear + 2 natural basis cols
    if df_resid <= 0:
        return F, float("nan")
    p = float(sps.f.sf(F, df_diff, df_resid))
    return F, p


def mann_whitney_pairwise(pool: dict) -> list[dict]:
    """Adjacent-bin pairwise Mann-Whitney (4 pairs per spec 4.5.2)."""
    from scipy import stats as sps
    g = pool["gevoelscore"]
    bins = pool["bin"]
    out = []
    for i in range(4):
        gi = g[bins == i]
        gj = g[bins == i + 1]
        if len(gi) < 2 or len(gj) < 2:
            out.append({
                "pair": f"B{i+1}-B{i+2}",
                "n_i": int(len(gi)), "n_j": int(len(gj)),
                "U": None, "p_two_sided": None,
            })
            continue
        try:
            U, p = sps.mannwhitneyu(gi, gj, alternative="two-sided")
            out.append({
                "pair": f"B{i+1}-B{i+2}",
                "n_i": int(len(gi)), "n_j": int(len(gj)),
                "U": float(U), "p_two_sided": float(p),
            })
        except Exception:
            out.append({
                "pair": f"B{i+1}-B{i+2}",
                "n_i": int(len(gi)), "n_j": int(len(gj)),
                "U": None, "p_two_sided": None,
            })
    return out


def spearman_rho(pool: dict) -> dict:
    """Spearman rho on continuous (stress, gevoelscore) per spec 4.5.2."""
    from scipy import stats as sps
    s = pool["stress_use"]
    g = pool["gevoelscore"]
    if len(s) < 3:
        return {"rho": None, "p": None, "n": int(len(s))}
    rho, p = sps.spearmanr(s, g)
    return {"rho": float(rho), "p": float(p), "n": int(len(s))}


# === Verdict gating (spec 5.1 3-condition) =============================

def verdict_three_condition(perm: dict, spline_secderiv: list[float]) -> dict:
    """spec 5.1 3-condition gated verdict."""
    p = perm["p_values"]
    obs = perm["obs"]
    p_a = p["p_a_jonckheere_decreasing"]
    p_b = p["p_b_S_convex"]
    p_c = p["p_c_spline_nonlinearity"]
    # Direction checks
    a_direction_ok = (obs["J_star"] is not None) and (obs["J_star"] < 0)  # decreasing
    b_direction_ok = (obs["S"] is not None) and (obs["S"] < 0)  # convex
    # Spline midpoint count: >= 3 of 4 with negative second derivative
    valid_sd = [x for x in spline_secderiv if x is not None and not math.isnan(x)]
    n_neg = sum(1 for x in valid_sd if x < 0)
    c_direction_ok = n_neg >= SPLINE_MIDPOINT_COUNT_BAR

    a_met = (p_a < P_BAR) and a_direction_ok
    b_met = (p_b < P_BAR) and b_direction_ok
    c_met = (p_c < P_BAR) and c_direction_ok

    # Wrong-direction firing -> REJECTED override
    wrong_dir_fired = False
    wrong_dir_notes = []
    if obs["J_star"] is not None and obs["J_star"] > 0 and p_a < P_BAR:
        wrong_dir_fired = True
        wrong_dir_notes.append("(a) Jonckheere significant in INCREASING direction")
    if obs["S"] is not None and obs["S"] > 0 and p_b < P_BAR:
        wrong_dir_fired = True
        wrong_dir_notes.append("(b) S significantly POSITIVE (concave) not convex")
    n_pos = sum(1 for x in valid_sd if x > 0)
    if p_c < P_BAR and n_pos >= SPLINE_MIDPOINT_COUNT_BAR:
        wrong_dir_fired = True
        wrong_dir_notes.append("(c) spline second-derivative POSITIVE at >= 3/4 midpoints")

    n_met = int(a_met) + int(b_met) + int(c_met)
    if wrong_dir_fired:
        verdict = "REJECTED"
        verdict_label = "REJECTED (wrong-direction override)"
    elif n_met == 3:
        verdict = "SUPPORTED"
        verdict_label = "SUPPORTED (3-of-3 conditions MET)"
    elif n_met == 2:
        verdict = "PARTIAL"
        verdict_label = "PARTIAL (2-of-3 conditions MET)"
    else:
        verdict = "REJECTED"
        verdict_label = f"REJECTED ({n_met}-of-3 conditions MET)"
    return {
        "p_a": float(p_a), "a_direction_ok": bool(a_direction_ok),
        "a_met": bool(a_met),
        "p_b": float(p_b), "b_direction_ok": bool(b_direction_ok),
        "b_met": bool(b_met),
        "p_c": float(p_c), "c_direction_ok": bool(c_direction_ok),
        "c_met": bool(c_met), "spline_neg_count": int(n_neg),
        "spline_pos_count": int(n_pos), "spline_total_midpoints": int(len(valid_sd)),
        "n_met": n_met,
        "wrong_direction_fired": bool(wrong_dir_fired),
        "wrong_direction_notes": wrong_dir_notes,
        "verdict": verdict, "verdict_label": verdict_label,
    }


# === Sanity gates (spec 7.5) ===========================================

def run_sanity_gates(pool: dict) -> dict:
    """Run spec 7.5 sanity gates 1-4. Returns dict with verdict PASS/HALT."""
    desc = bin_descriptives(pool)
    bin_n = desc["bin_n"]
    fails: list[dict] = []

    # Gate 1: each bin n >= 30
    n_below_30 = [b for b in range(5) if bin_n[b] < MIN_BIN_N]
    gate1_ok = len(n_below_30) == 0
    if not gate1_ok:
        # spec 7.3 halt-option-A pre-committed default: B5 < 30 -> widen
        # B4 to absorb B5. Only applies if B5 is the SOLE failing bin.
        if n_below_30 == [4]:
            halt_optA_applicable = True
            fails.append({
                "gate": 1, "name": "per-bin n >= 30",
                "detail": f"B5 n={bin_n[4]} < {MIN_BIN_N}; spec 7.3 halt-option-A "
                          f"pre-committed default: widen B4 to absorb B5.",
                "halt_optA_applicable": True,
            })
        else:
            fails.append({
                "gate": 1, "name": "per-bin n >= 30",
                "detail": f"bins below threshold: "
                          f"{[(f'B{b+1}', bin_n[b]) for b in n_below_30]}; "
                          f"spec 7.3 halt-option-A pre-committed only for sole-B5 "
                          f"failure; other failures require v2 spec redraft.",
                "halt_optA_applicable": False,
            })

    # Gate 2: all_day_stress_avg median in [20, 60]
    s_med = float(np.median(pool["stress_use"])) if pool["n"] > 0 else float("nan")
    g2_lo, g2_hi = GATE2_STRESS_MEDIAN_RANGE
    gate2_ok = g2_lo <= s_med <= g2_hi
    if not gate2_ok:
        fails.append({
            "gate": 2, "name": "stress median in [20, 60]",
            "detail": f"observed median = {s_med:.2f}; outside [{g2_lo}, {g2_hi}]",
        })

    # Gate 3: gevoelscore median in [3, 6]
    g_med = float(np.median(pool["gevoelscore"])) if pool["n"] > 0 else float("nan")
    g3_lo, g3_hi = GATE3_GEVOELSCORE_MEDIAN_RANGE
    gate3_ok = g3_lo <= g_med <= g3_hi
    if not gate3_ok:
        fails.append({
            "gate": 3, "name": "gevoelscore median in [3, 6]",
            "detail": f"observed median = {g_med:.2f}; outside [{g3_lo}, {g3_hi}]",
        })

    # Gate 4: at least 3 bins >= 30 AND total >= 100
    n_at_least_30 = sum(1 for b in range(5) if bin_n[b] >= MIN_BIN_N)
    total_n = sum(bin_n)
    gate4_ok = (n_at_least_30 >= 3) and (total_n >= MIN_TOTAL_N)
    if not gate4_ok:
        fails.append({
            "gate": 4, "name": "power density (>= 3 bins with n>=30 AND total n>=100)",
            "detail": (f"bins with n>=30: {n_at_least_30}; total n: {total_n}"),
        })

    return {
        "bin_n": bin_n, "bin_mean": desc["bin_mean"], "bin_median": desc["bin_median"],
        "stress_median": s_med, "gevoelscore_median": g_med, "total_n": total_n,
        "gate1_ok": gate1_ok, "gate2_ok": gate2_ok, "gate3_ok": gate3_ok,
        "gate4_ok": gate4_ok, "fails": fails,
        "verdict": "PASS" if not fails else "HALT",
    }


# === Halt-option-A absorb (spec 7.3) ===================================

def apply_halt_optA(pool: dict) -> dict:
    """spec 7.3 halt-option-A: widen B4 [40, 60) to absorb B5 [60, 100].
    Returns a new pool with bin labels recoded (B5 -> B4)."""
    new_bins = pool["bin"].copy()
    new_bins[new_bins == 4] = 3
    out = dict(pool)
    out["bin"] = new_bins
    return out


# === Dry-run + write reports ===========================================

def dry_run(master: dict, baseline_cutoff: date | None) -> dict:
    """Run spec 7.5 sanity gates on the primary unmedicated pool."""
    print("", file=sys.stderr)
    print("=== HA-C3 r2 dry-run ===", file=sys.stderr)
    print(f"  RANDOM_SEED={RANDOM_SEED}; B={B_HEADLINE}; E[L]={BOOTSTRAP_E_L}",
          file=sys.stderr)
    print(f"  spec commit: {R2_SPEC_COMMIT}", file=sys.stderr)
    if baseline_cutoff is not None:
        print(f"  device baseline cutoff (excl <=): {baseline_cutoff}",
              file=sys.stderr)
    print("", file=sys.stderr)
    print("Building primary unmedicated pool (spec 4.2 + 4.3 + 4.4 5.A)...",
          file=sys.stderr)
    pool = build_pool(master, baseline_cutoff, phase="unmedicated")
    print(f"  pool n = {pool['n']}", file=sys.stderr)
    sanity = run_sanity_gates(pool)
    print("\n--- spec 7.5 sanity gate results ---", file=sys.stderr)
    print(f"  bin sizes: {sanity['bin_n']}", file=sys.stderr)
    print(f"  bin means: "
          f"{[f'{m:.3f}' if m is not None else 'NA' for m in sanity['bin_mean']]}",
          file=sys.stderr)
    print(f"  stress median: {sanity['stress_median']:.2f}", file=sys.stderr)
    print(f"  gevoelscore median: {sanity['gevoelscore_median']:.2f}",
          file=sys.stderr)
    print(f"  total n: {sanity['total_n']}", file=sys.stderr)
    print(f"  gate 1 (per-bin n>=30):  {'PASS' if sanity['gate1_ok'] else 'FAIL'}",
          file=sys.stderr)
    print(f"  gate 2 (stress median in [20,60]): "
          f"{'PASS' if sanity['gate2_ok'] else 'FAIL'}", file=sys.stderr)
    print(f"  gate 3 (gevoelscore median in [3,6]): "
          f"{'PASS' if sanity['gate3_ok'] else 'FAIL'}", file=sys.stderr)
    print(f"  gate 4 (>=3 bins n>=30 AND total>=100): "
          f"{'PASS' if sanity['gate4_ok'] else 'FAIL'}", file=sys.stderr)
    print(f"  verdict: {sanity['verdict']}", file=sys.stderr)
    sanity["pool"] = pool
    return sanity


def write_dry_run_report(sanity: dict) -> None:
    halt = sanity["verdict"] == "HALT"
    title = ("HA-C3 r2 dry-run report - SANITY GATE FAILURE (HALT)"
             if halt else "HA-C3 r2 dry-run report - sanity gates PASS")
    lines = [
        f"# {title}",
        "",
        ("Emitted by `test.py --dry-run` per locked r2 hypothesis.md §10.4. "
         "Headline cell: unmedicated × 5-bin × `gevoelscore` × 3-condition "
         "gated outcome × block-permutation null at E[L]=7. Day-validity "
         "per §4.3 (LC era + unmedicated + not April-2024 cluster + "
         "not first 21 device-baseline days + non-NaN both columns)."),
        "",
        f"- Pool n = {sanity['total_n']}",
        f"- Stress median = {sanity['stress_median']:.2f}",
        f"- Gevoelscore median = {sanity['gevoelscore_median']:.2f}",
        "",
        "## Per-bin sample sizes (`all_day_stress_avg`)",
        "",
        "| bin | label | n | mean gevoelscore | median gevoelscore |",
        "|---|---|---:|---:|---:|",
    ]
    for b in range(5):
        m = sanity["bin_mean"][b]
        md = sanity["bin_median"][b]
        lines.append(
            f"| B{b+1} | {BIN_LABELS[b]} | {sanity['bin_n'][b]} | "
            f"{f'{m:.3f}' if m is not None else 'NA'} | "
            f"{f'{md:.2f}' if md is not None else 'NA'} |")
    lines.append("")
    lines.append("## Gate results")
    lines.append("")
    lines.append("| gate | description | result |")
    lines.append("|---|---|---|")
    lines.append(f"| 1 | per-bin n >= {MIN_BIN_N} (×5 bins) | "
                 f"{'PASS' if sanity['gate1_ok'] else 'FAIL'} |")
    lines.append(f"| 2 | stress median in {list(GATE2_STRESS_MEDIAN_RANGE)} | "
                 f"{'PASS' if sanity['gate2_ok'] else 'FAIL'} |")
    lines.append(f"| 3 | gevoelscore median in {list(GATE3_GEVOELSCORE_MEDIAN_RANGE)} | "
                 f"{'PASS' if sanity['gate3_ok'] else 'FAIL'} |")
    lines.append(f"| 4 | >= 3 bins n>=30 AND total n>={MIN_TOTAL_N} | "
                 f"{'PASS' if sanity['gate4_ok'] else 'FAIL'} |")
    lines.append("")
    if halt:
        lines.extend([
            "## HALT-eligible failures",
            "",
        ])
        for f in sanity["fails"]:
            lines.append(f"- **Gate {f['gate']}** ({f['name']}): {f['detail']}")
            if f.get("halt_optA_applicable"):
                lines.append("  - **§7.3 halt-option-A pre-committed default applies**: "
                             "widen B4 to absorb B5; the convexity test reduces to "
                             "4 bins with 2 second-differences. test.py will re-run "
                             "on the 4-bin reduction.")
        lines.extend([
            "",
            ("Per locked r2 §10.4 step 1 + `hypothesis_lock_process.md` §3.9: "
             "the full test is **HALTed** if the failure is not absorbed by "
             "the pre-committed §7.3 halt-option-A. Failures other than "
             "sole-B5 underpower require a v2 spec redraft."),
            "",
        ])
    else:
        lines.append("**DRY-RUN VERDICT: PASS** — proceed with full run.")
        lines.append("")
    OUT_DRYRUN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {OUT_DRYRUN_MD}", file=sys.stderr)


# === Full run (spec 10.4 step 2) =======================================

def run_full(master: dict, baseline_cutoff: date | None,
             sanity: dict, applied_optA: bool = False) -> dict:
    """Run the full test on the primary pool + sensitivity arms."""
    rng = np.random.default_rng(RANDOM_SEED)
    pool = sanity["pool"]
    print("\n=== HA-C3 r2 full run ===", file=sys.stderr)
    print(f"  pool n = {pool['n']}", file=sys.stderr)
    if applied_optA:
        print("  (spec 7.3 halt-option-A APPLIED: B4 widened to absorb B5)",
              file=sys.stderr)

    # --- Primary 3-condition tests (spec 4.5.1) ---
    print("\n  primary 3-condition block-permutation tests (B=10,000)...",
          file=sys.stderr)
    perm = block_permutation_three_conditions(pool, B_HEADLINE, BOOTSTRAP_E_L, rng)
    F_continuous, spline_sd = _spline_F_and_secderiv(pool)
    print(f"    J* = {perm['obs']['J_star']}", file=sys.stderr)
    print(f"    S  = {perm['obs']['S']}", file=sys.stderr)
    print(f"    spline F (continuous) = {F_continuous}", file=sys.stderr)
    print(f"    spline 2nd-deriv at midpoints (25,35,50,80): "
          f"{[f'{x:.4f}' for x in spline_sd]}", file=sys.stderr)
    print(f"    p_a = {perm['p_values']['p_a_jonckheere_decreasing']:.4f}",
          file=sys.stderr)
    print(f"    p_b = {perm['p_values']['p_b_S_convex']:.4f}", file=sys.stderr)
    print(f"    p_c = {perm['p_values']['p_c_spline_nonlinearity']:.4f}",
          file=sys.stderr)

    # --- 3-condition verdict ---
    verdict = verdict_three_condition(perm, spline_sd)
    print(f"\n  3-condition verdict: {verdict['verdict_label']}", file=sys.stderr)

    # --- secondary descriptive (spec 4.5.2) ---
    print("\n  secondary descriptive outcomes...", file=sys.stderr)
    bin_ci = stationary_bootstrap_ci_bin_means(
        pool, B=1000, expected_block_length=BOOTSTRAP_E_L, rng=rng)
    pairs = mann_whitney_pairwise(pool)
    # Holm on adjacent-bin Mann-Whitney p-values (4 pairs)
    holm_in = []
    for pp in pairs:
        if pp["p_two_sided"] is None:
            holm_in.append(1.0)
        else:
            holm_in.append(pp["p_two_sided"])
    holm = holm_step_down(np.asarray(holm_in), n_eff=4, alpha=0.05)
    for i, pp in enumerate(pairs):
        pp["holm_adjusted_p"] = float(holm["adjusted_p_values"][i])
        pp["holm_rejected"] = bool(holm["rejected"][i])
        pp["holm_threshold"] = float(holm["thresholds"][i])
    rho = spearman_rho(pool)

    # --- spec 5.B dose-adjusted cross-phase sensitivity (spec 4.4) ---
    print("\n  spec 5.B dose-adjusted cross-phase sensitivity arm...",
          file=sys.stderr)
    pool_5B = build_pool(master, baseline_cutoff, phase="all",
                          dose_adjusted=True)
    print(f"    pool 5.B n = {pool_5B['n']}", file=sys.stderr)
    perm_5B = block_permutation_three_conditions(
        pool_5B, B_HEADLINE, BOOTSTRAP_E_L, rng) if pool_5B["n"] >= MIN_TOTAL_N else None
    if perm_5B is not None:
        F_5B, sd_5B = _spline_F_and_secderiv(pool_5B)
        verdict_5B = verdict_three_condition(perm_5B, sd_5B)
    else:
        verdict_5B = {"verdict": "NA", "verdict_label": "INCONCLUSIVE (pool too small)"}

    # --- Crash-drop sensitivity (spec 4.6) ---
    print("\n  spec 4.6 crash-drop sensitivity...", file=sys.stderr)
    pool_no_crash = build_pool(master, baseline_cutoff, phase="unmedicated",
                                drop_crashes=True)
    means_full = _means_per_bin(pool["gevoelscore"], pool["bin"])
    means_nocr = _means_per_bin(pool_no_crash["gevoelscore"], pool_no_crash["bin"])
    S_full = second_diff_S(means_full)
    S_nocr = second_diff_S(means_nocr)
    # Standardised |Delta| using gevoelscore SD
    g_sd = float(pool["gevoelscore"].std(ddof=1)) if pool["n"] > 1 else float("nan")
    if not math.isnan(S_full) and not math.isnan(S_nocr) and g_sd > 0:
        delta_std = abs(S_full - S_nocr) / g_sd
    else:
        delta_std = float("nan")
    crash_drop = {
        "S_full": float(S_full) if not math.isnan(S_full) else None,
        "S_no_crash": float(S_nocr) if not math.isnan(S_nocr) else None,
        "n_full": int(pool["n"]),
        "n_no_crash": int(pool_no_crash["n"]),
        "delta_standardised": (None if math.isnan(delta_std) else float(delta_std)),
        "sign_change": (
            (not math.isnan(S_full)) and (not math.isnan(S_nocr))
            and ((S_full < 0) != (S_nocr < 0))
        ),
        "flag": (
            (not math.isnan(delta_std) and delta_std > 0.10)
            or (
                (not math.isnan(S_full)) and (not math.isnan(S_nocr))
                and ((S_full < 0) != (S_nocr < 0))
            )
        ),
    }

    # --- Train/validate M3 overlay (spec 4.8) ---
    print("\n  spec 4.8 train/validate M3 descriptive overlay...", file=sys.stderr)
    train_mask = pool["dates"] <= np.datetime64(TRAIN_END)
    validate_mask = (~train_mask)  # everything else in pool is validate (unmedicated)
    def _slice(mask):
        return {
            "dates": pool["dates"][mask], "stress_raw": pool["stress_raw"][mask],
            "stress_use": pool["stress_use"][mask],
            "gevoelscore": pool["gevoelscore"][mask], "bin": pool["bin"][mask],
            "is_crash": pool["is_crash"][mask], "n": int(mask.sum()),
        }
    pool_train = _slice(train_mask)
    pool_validate = _slice(validate_mask)
    means_train = _means_per_bin(pool_train["gevoelscore"], pool_train["bin"])
    means_validate = _means_per_bin(pool_validate["gevoelscore"], pool_validate["bin"])
    overlay = {
        "train_n": pool_train["n"],
        "validate_n": pool_validate["n"],
        "train_bin_n": [int((pool_train["bin"] == b).sum()) for b in range(5)],
        "validate_bin_n": [int((pool_validate["bin"] == b).sum()) for b in range(5)],
        "train_bin_mean": [None if math.isnan(m) else float(m) for m in means_train],
        "validate_bin_mean": [None if math.isnan(m) else float(m) for m in means_validate],
        "train_S": (None if math.isnan(second_diff_S(means_train))
                    else float(second_diff_S(means_train))),
        "validate_S": (None if math.isnan(second_diff_S(means_validate))
                       else float(second_diff_S(means_validate))),
    }

    # --- t+1 lagged variant (spec 4.8) ---
    print("\n  spec 4.8 t+1 lagged variant...", file=sys.stderr)
    pool_lag = build_pool(master, baseline_cutoff, phase="unmedicated",
                          lag_t_plus_1=True)
    means_lag = _means_per_bin(pool_lag["gevoelscore"], pool_lag["bin"])
    S_lag = second_diff_S(means_lag)
    lagged = {
        "n": pool_lag["n"],
        "bin_n": [int((pool_lag["bin"] == b).sum()) for b in range(5)],
        "bin_mean": [None if math.isnan(m) else float(m) for m in means_lag],
        "S": (None if math.isnan(S_lag) else float(S_lag)),
    }

    # --- Within-consolidation §5.A replication (spec 4.4 r2) ---
    print("\n  spec 4.4 within-consolidation §5.A replication...",
          file=sys.stderr)
    pool_consol = build_pool(master, baseline_cutoff, phase="consolidation")
    consol_bin_n = [int((pool_consol["bin"] == b).sum()) for b in range(5)]
    n_at_least_30_consol = sum(1 for b in range(5) if consol_bin_n[b] >= MIN_BIN_N)
    consol_optA_applied = False
    consol_pool_used = pool_consol
    if (consol_bin_n[4] < MIN_BIN_N) and (n_at_least_30_consol >= 3):
        # Apply halt-option-A recursively (widen B4 to absorb B5)
        consol_pool_used = apply_halt_optA(pool_consol)
        consol_optA_applied = True
    consol_bin_n_after = [int((consol_pool_used["bin"] == b).sum()) for b in range(5)]
    n_at_least_30_after = sum(1 for b in range(5) if consol_bin_n_after[b] >= MIN_BIN_N)
    if n_at_least_30_after >= 4 and consol_pool_used["n"] >= MIN_TOTAL_N:
        consol_perm = block_permutation_three_conditions(
            consol_pool_used, B_HEADLINE, BOOTSTRAP_E_L, rng)
        consol_F, consol_sd = _spline_F_and_secderiv(consol_pool_used)
        consol_verdict = verdict_three_condition(consol_perm, consol_sd)
    else:
        consol_perm = None
        consol_verdict = {
            "verdict": "NA",
            "verdict_label": "INCONCLUSIVE (fewer than 4 bins with n>=30 "
                             "or total<100 after r2 4-bin reduction)",
        }
    consolidation = {
        "n": pool_consol["n"], "bin_n": consol_bin_n,
        "n_at_least_30": n_at_least_30_consol,
        "optA_applied": consol_optA_applied,
        "bin_n_after_optA": consol_bin_n_after,
        "verdict": consol_verdict.get("verdict_label"),
        "perm": consol_perm,
    }

    # --- spec 4.7 E[L]* checks (linear-residual + bin-label) ---
    print("\n  spec 4.7 r2 E[L]* checks (linear-residual + bin-label)...",
          file=sys.stderr)
    # Linear residual series: residuals from linear fit gevoelscore ~ stress
    s = pool["stress_use"]
    g = pool["gevoelscore"]
    if pool["n"] >= 3:
        slope, intercept = np.polyfit(s, g, 1)
        resid = g - (slope * s + intercept)
    else:
        resid = g
    el_resid = compute_data_driven_block_length(
        resid, default_block_length=BOOTSTRAP_E_L,
        deviation_flag_factor=EL_DEVIATION_FACTOR)
    el_binlabel = compute_data_driven_block_length(
        pool["bin"].astype(float), default_block_length=BOOTSTRAP_E_L,
        deviation_flag_factor=EL_DEVIATION_FACTOR)
    el_star = {
        "linear_residual": {
            "optimal_E_L": float(el_resid["optimal_block_length"]),
            "cutoff_lag": (int(el_resid["cutoff_lag"])
                           if el_resid["cutoff_lag"] is not None else None),
            "flagged_deviation": bool(el_resid["flagged_deviation"]),
            "note": el_resid.get("note"),
        },
        "bin_label": {
            "optimal_E_L": float(el_binlabel["optimal_block_length"]),
            "cutoff_lag": (int(el_binlabel["cutoff_lag"])
                           if el_binlabel["cutoff_lag"] is not None else None),
            "flagged_deviation": bool(el_binlabel["flagged_deviation"]),
            "note": el_binlabel.get("note"),
        },
    }

    return {
        "spec_commit": R2_SPEC_COMMIT,
        "config": {
            "RANDOM_SEED": RANDOM_SEED,
            "B_HEADLINE": B_HEADLINE,
            "BOOTSTRAP_E_L": BOOTSTRAP_E_L,
            "P_BAR": P_BAR,
            "MIN_BIN_N": MIN_BIN_N,
            "MIN_TOTAL_N": MIN_TOTAL_N,
            "DOSE_BETA_PER_MG": DOSE_BETA_PER_MG,
            "SPLINE_MIDPOINT_COUNT_BAR": SPLINE_MIDPOINT_COUNT_BAR,
            "BIN_EDGES": BIN_EDGES,
            "BIN_MIDPOINTS_FULL": BIN_MIDPOINTS_FULL,
            "BIN_MIDPOINTS_FOR_SPLINE": BIN_MIDPOINTS_FOR_SPLINE,
            "COMPANION_CONTRAST": COMPANION_CONTRAST.tolist(),
            "applied_optA": applied_optA,
        },
        "primary": {
            "pool_n": pool["n"],
            "bin_n": [int((pool["bin"] == b).sum()) for b in range(5)],
            "bin_mean": [None if math.isnan(m) else float(m) for m in _means_per_bin(g, pool["bin"])],
            "bin_ci_95": bin_ci,
            "perm": perm,
            "spline_continuous_F": float(F_continuous) if not math.isnan(F_continuous) else None,
            "spline_secderiv_at_midpoints": [
                None if math.isnan(x) else float(x) for x in spline_sd
            ],
            "verdict": verdict,
            "pairwise_mann_whitney": pairs,
            "spearman_rho": rho,
        },
        "sensitivity_5B": {
            "pool_n": pool_5B["n"],
            "bin_n": [int((pool_5B["bin"] == b).sum()) for b in range(5)],
            "bin_mean": [None if math.isnan(m) else float(m) for m in _means_per_bin(pool_5B["gevoelscore"], pool_5B["bin"])],
            "perm": perm_5B,
            "verdict": verdict_5B,
        },
        "sensitivity_crash_drop": crash_drop,
        "sensitivity_train_validate_overlay": overlay,
        "sensitivity_lagged_t_plus_1": lagged,
        "sensitivity_within_consolidation": consolidation,
        "el_star": el_star,
        "sanity": {
            "bin_n": sanity["bin_n"],
            "bin_mean": sanity["bin_mean"],
            "stress_median": sanity["stress_median"],
            "gevoelscore_median": sanity["gevoelscore_median"],
            "total_n": sanity["total_n"],
            "verdict": sanity["verdict"],
            "fails": sanity["fails"],
        },
    }


def write_result_md(results: dict, halted: bool, halt_detail: str = "") -> None:
    """Write result.md with the 8-section structure per pre-reg 10.3."""
    if halted:
        verdict_str = "HALT (sanity gate failure)"
    else:
        v = results["primary"]["verdict"]
        verdict_str = v["verdict_label"]
    lines: list[str] = []
    # --- Authorship ---
    lines.append(f"# HA-C3 r2 RESULT: {verdict_str}")
    lines.append("")
    lines.append("## Authorship")
    lines.append("")
    lines.append(
        f"Drafted 2026-06-23 by Claude (Opus 4.7 1M) in producer-mode "
        f"under user authorisation per "
        f"[CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default). "
        f"Authorising user: Willem. Pre-reg r2 LOCKED 2026-06-23 at commit "
        f"`{R2_SPEC_COMMIT}`. Test commit: `(this-commit)`. Status: "
        f"**LANDED**.")
    lines.append("")
    lines.append(
        "**Test-session context**: this `test.py` was implemented and run "
        "in a FRESH Claude session per the post-lock discipline of "
        "[`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock). "
        "The drafter has now seen the joint distribution; result.md is the "
        "first post-lock artefact emitted.")
    lines.append("")
    if halted:
        lines.append(
            "**HALT outcome**: the §7.5 dry-run sanity gates failed at the "
            "configuration pre-committed at r2 lock. Per §3.9 dry-run halt "
            "discipline + the locked r2 spec, the full test was **NOT** "
            "executed beyond the dry-run; verdict is HALT and the §7.3 "
            "halt-option resolution is documented below for the v2 redraft.")
        lines.append("")
    # --- §1 What was tested ---
    lines.append("## §1 What was tested")
    lines.append("")
    bins_str = ", ".join(BIN_LABELS)
    lines.append(
        "**Headline cell** (per pre-reg §1 + §5.0): unmedicated (full LC era "
        "through 2024-04-08) × full Stratum 4 single pool × `all_day_stress_avg` "
        f"binned at {{{bins_str}}} × `gevoelscore` bin-mean × "
        "{Jonckheere-Terpstra monotone + second-difference convexity contrast "
        "S + spline non-linearity} × block-permutation null at E[L]=7 × "
        "3-condition gated verdict per §5.1.")
    lines.append("")
    lines.append(
        "**Wiggers C3 verbatim claim** (PDF lines 1357-1368, Annual Stress "
        "Scores section): the stress → fatigue relationship is "
        "non-linear / convex — a 30 → 40 stress step costs more "
        "gevoelscore than a 20 → 30 step. Tested as the bin-mean trajectory "
        "should be **monotone-decreasing** AND **convex** (accelerating "
        "decrement at higher stress bins).")
    lines.append("")
    lines.append("**3-condition gated verdict per §5.1**:")
    lines.append("")
    lines.append("| outcome | condition status | verdict |")
    lines.append("|---|---|---|")
    lines.append("| (a) MET AND (b) MET AND (c) MET | 3-of-3 | **SUPPORTED** |")
    lines.append("| Exactly 2-of-3 MET | 2-of-3 | **PARTIAL** |")
    lines.append("| ≤1-of-3 MET | 0/1-of-3 | **REJECTED** |")
    lines.append("| Any wrong-direction firing | override | **REJECTED** |")
    lines.append("")

    # --- §2 Data + descriptives ---
    lines.append("## §2 Data + descriptives")
    lines.append("")
    s_med = results["sanity"]["stress_median"]
    g_med = results["sanity"]["gevoelscore_median"]
    lines.append(f"Primary unmedicated pool: n = **{results['sanity']['total_n']}**. "
                 f"Stress median: **{s_med:.2f}**. Gevoelscore median: "
                 f"**{g_med:.2f}**.")
    lines.append("")
    lines.append("| bin | label | n | bin-mean gevoelscore | bin-median |")
    lines.append("|---|---|---:|---:|---:|")
    for b in range(5):
        m = results["sanity"]["bin_mean"][b]
        md = results["sanity"]["bin_median"][b]
        lines.append(
            f"| B{b+1} | {BIN_LABELS[b]} | {results['sanity']['bin_n'][b]} | "
            f"{f'{m:.3f}' if m is not None else 'NA'} | "
            f"{f'{md:.2f}' if md is not None else 'NA'} |")
    lines.append("")
    if halted:
        # No per-phase sensitivity readouts for halt outcome
        pass

    # --- §3 Primary test result ---
    lines.append("## §3 Primary test result")
    lines.append("")
    if halted:
        lines.append(
            "**HALT**: primary test was not executed because the §7.5 sanity "
            "gates failed at the pre-committed bin specification. Per §3.9 "
            "dry-run halt discipline + locked r2 §7.5 + §10.4 step 1, no "
            "primary statistics were computed.")
        lines.append("")
        lines.append("**Halt-option resolution (for v2 redraft)**:")
        lines.append("")
        lines.append(
            "- **Gate 1 fired on TWO bins**: B1 [0,20) has **n = 0** and "
            "B5 [60,100] has **n = 1** (against the §7.5 ≥30 bar). The "
            "B5 underpower was forecast at lock per §7.2 ('B5 is the "
            "most-at-risk for the < 30 sanity gate'); the B1 underpower "
            "(n = 0) was NOT forecast — the descriptive distribution shows "
            "`all_day_stress_avg` never falls below 20 on the unmedicated "
            "pool (stress median 34, pool n 581).")
        lines.append(
            "- **§7.3 halt-option-A pre-committed default**: widen B4 "
            "to absorb B5. **This addresses B5 but NOT B1**.")
        lines.append(
            "- **B1-handling is OUT OF LOCKED SCOPE**: the locked r2 §7.3 "
            "pre-commitment is sole-B5; the B1 zero-population failure "
            "mode is not absorbed by either halt-option-A or halt-option-B "
            "as documented. Per §3.9 + §10.4 step 3, **any post-dry-run "
            "spec revision creates HA-C3-v2 with v1/r2 archived**. The v2 "
            "redraft must address the B1 boundary directly (e.g. collapse "
            "B1 into B2 to form a `[0, 30)` low-stress bin), preserving "
            "the Wiggers-verbatim 30→40 anchor at the B3-B4 boundary.")
        lines.append("")
        lines.append(f"**Halt detail (machine-readable)**: {halt_detail}")
        lines.append("")
    else:
        p = results["primary"]["perm"]
        v = results["primary"]["verdict"]
        obs = p["obs"]
        lines.append("Per pre-reg §4.5.1 + §4.7 block-permutation at E[L]=7 "
                     f"(B = {B_HEADLINE} draws, seed = {RANDOM_SEED}).")
        lines.append("")
        lines.append("| condition | statistic | observed | one-sided p | direction OK | bar (p<0.05) | MET |")
        lines.append("|---|---|---:|---:|:---:|:---:|:---:|")
        lines.append(
            f"| (a) Jonckheere-Terpstra (monotone-decreasing) | J* (standardised) | "
            f"{obs['J_star']:+.4f} | {v['p_a']:.4f} | "
            f"{'YES' if v['a_direction_ok'] else 'NO'} | "
            f"{'PASS' if v['p_a'] < P_BAR else 'fail'} | "
            f"{'PASS' if v['a_met'] else 'fail'} |")
        lines.append(
            f"| (b) Second-difference convexity | S = mean(D²_2, D²_3, D²_4) | "
            f"{obs['S']:+.4f} | {v['p_b']:.4f} | "
            f"{'YES (S<0)' if v['b_direction_ok'] else 'NO (S>=0)'} | "
            f"{'PASS' if v['p_b'] < P_BAR else 'fail'} | "
            f"{'PASS' if v['b_met'] else 'fail'} |")
        lines.append(
            f"| (c) Spline non-linearity (block-permutation per r2) | F (continuous predictor) | "
            f"{obs['spline_F_continuous_predictor'] if obs.get('spline_F_continuous_predictor') is not None else 'NA'} | "
            f"{v['p_c']:.4f} | "
            f"{'YES' if v['c_direction_ok'] else 'NO'} ({v['spline_neg_count']} of {v['spline_total_midpoints']} midpoints negative) | "
            f"{'PASS' if v['p_c'] < P_BAR else 'fail'} | "
            f"{'PASS' if v['c_met'] else 'fail'} |")
        lines.append(
            f"| (d) Companion Option-A orthogonal quadratic (descriptive) | c·m, c=(+2,−1,−2,−1,+2) | "
            f"{obs['companion_contrast']:+.4f} | "
            f"{p['p_values']['p_companion_orthogonal_quadratic']:.4f} | n/a | n/a | n/a |")
        lines.append("")
        lines.append(f"**Aggregate 3-condition verdict: {v['verdict_label']}**")
        if v["wrong_direction_fired"]:
            lines.append("")
            lines.append("**Wrong-direction overrides** fired:")
            for n in v["wrong_direction_notes"]:
                lines.append(f"- {n}")
        # Parametric F (descriptive only)
        pf = p["parametric_F_descriptive"]
        lines.append("")
        lines.append(
            f"*Spline parametric F (descriptive only per pre-reg §4.5.1(c) r2): "
            f"F = {pf['F'] if pf['F'] is not None else 'NA'}, "
            f"parametric p = {pf['p_parametric'] if pf['p_parametric'] is not None else 'NA'}.*")
        lines.append("")
        lines.append("**Bin-means (primary)**:")
        lines.append("")
        lines.append("| bin | n | mean | 95% CI (stationary bootstrap E[L]=7, B=1000) |")
        lines.append("|---|---:|---:|---|")
        for b in range(5):
            n_b = results["primary"]["bin_n"][b]
            m_b = results["primary"]["bin_mean"][b]
            ci_lo, ci_hi = results["primary"]["bin_ci_95"].get(f"B{b+1}", (None, None))
            ci_str = (f"[{ci_lo:.3f}, {ci_hi:.3f}]" if (ci_lo is not None and ci_hi is not None)
                      else "NA")
            lines.append(f"| B{b+1} | {n_b} | "
                         f"{f'{m_b:.3f}' if m_b is not None else 'NA'} | "
                         f"{ci_str} |")
        lines.append("")
        # Pairwise Mann-Whitney + Holm
        lines.append("**Pairwise adjacent-bin Mann-Whitney + Holm step-down (descriptive, secondary)**:")
        lines.append("")
        lines.append("| pair | n_i | n_j | U | raw p | Holm threshold | Holm-adj p | Holm-rejected |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|:---:|")
        for pp in results["primary"]["pairwise_mann_whitney"]:
            u_str = f"{pp['U']:.0f}" if pp.get("U") is not None else "NA"
            p_str = f"{pp['p_two_sided']:.4f}" if pp.get("p_two_sided") is not None else "NA"
            th_str = f"{pp['holm_threshold']:.4f}" if pp.get("holm_threshold") is not None else "NA"
            ad_str = f"{pp['holm_adjusted_p']:.4f}" if pp.get("holm_adjusted_p") is not None else "NA"
            rej_str = "YES" if pp.get("holm_rejected") else "no"
            lines.append(
                f"| {pp['pair']} | {pp['n_i']} | {pp['n_j']} | "
                f"{u_str} | {p_str} | {th_str} | {ad_str} | {rej_str} |")
        lines.append("")
        # Spearman rho
        sr = results["primary"]["spearman_rho"]
        lines.append(
            f"**Sanity-check companion Spearman ρ** (the *opposing-model* "
            f"linear test per §4.5.2): ρ = "
            f"{sr['rho']:.4f} (p = {sr['p']:.4g}, n = {sr['n']}).")
        lines.append("")

    # --- §4 Sensitivity arms ---
    lines.append("## §4 Sensitivity arms (descriptive, no verdict weight)")
    lines.append("")
    if halted:
        lines.append("Sensitivity arms not executed because the primary test halted "
                     "on §7.5 sanity gates. Per §3.9 the v2 redraft re-executes "
                     "sensitivity arms after the spec is revised.")
        lines.append("")
    else:
        # 5.B
        s5B = results["sensitivity_5B"]
        v5B = s5B["verdict"]
        lines.append(f"### §5.B cross-phase dose-adjusted (predictor − {DOSE_BETA_PER_MG}/mg × dose_plasma_mg)")
        lines.append("")
        lines.append(f"- Pool n = {s5B['pool_n']}; bin-n = {s5B['bin_n']}; "
                     f"bin-mean = {s5B['bin_mean']}.")
        lines.append(f"- Verdict (descriptive, NOT promoted): "
                     f"**{v5B.get('verdict_label', 'NA')}**.")
        lines.append("")
        # Crash-drop
        cd = results["sensitivity_crash_drop"]
        lines.append("### Crash-drop sensitivity (CONVENTIONS §3.4)")
        lines.append("")
        s_full_str = f"{cd['S_full']:+.4f}" if cd["S_full"] is not None else "NA"
        s_nocr_str = f"{cd['S_no_crash']:+.4f}" if cd["S_no_crash"] is not None else "NA"
        d_std_str = (f"{cd['delta_standardised']:.4f}"
                     if cd["delta_standardised"] is not None else "NA")
        lines.append(f"- S (full) = {s_full_str} (n = {cd['n_full']}); "
                     f"S (no-crash) = {s_nocr_str} (n = {cd['n_no_crash']}).")
        lines.append(f"- |Δ S| standardised = {d_std_str}; "
                     f"sign-change = {cd['sign_change']}; flag = "
                     f"{'**FLAG**' if cd['flag'] else 'ok'}.")
        lines.append("")
        # Train/validate
        ov = results["sensitivity_train_validate_overlay"]
        lines.append("### Train/validate M3 descriptive overlay (per `train_validate_split_fate.md` §5)")
        lines.append("")
        lines.append(f"- Train (≤ 2023-12-31): n = {ov['train_n']}; "
                     f"bin-n = {ov['train_bin_n']}; bin-mean = {ov['train_bin_mean']}; "
                     f"S = {ov['train_S']}.")
        lines.append(f"- Validate (2024-01-01 → 2024-04-08): n = {ov['validate_n']}; "
                     f"bin-n = {ov['validate_bin_n']}; bin-mean = {ov['validate_bin_mean']}; "
                     f"S = {ov['validate_S']}.")
        lines.append("- Per `train_validate_split_fate.md` §5: divergence is a number, "
                     "not a narrative; no per-era verdicts.")
        lines.append("")
        # Lagged
        lg = results["sensitivity_lagged_t_plus_1"]
        lines.append("### t+1 lagged variant (gevoelscore[T+1] on stress[T])")
        lines.append("")
        lines.append(f"- n = {lg['n']}; bin-n = {lg['bin_n']}; bin-mean = {lg['bin_mean']}; "
                     f"S = {lg['S']}.")
        lines.append("")
        # Within-consolidation
        consol = results["sensitivity_within_consolidation"]
        lines.append("### Within-consolidation §5.A replication (§4.4 r2 amendment)")
        lines.append("")
        lines.append(f"- Pool n = {consol['n']}; bin-n = {consol['bin_n']}; "
                     f"bins with n>=30: {consol['n_at_least_30']}.")
        if consol['optA_applied']:
            lines.append(f"- §7.3 halt-option-A APPLIED recursively (B4 absorbed B5); "
                         f"bin-n after = {consol['bin_n_after_optA']}.")
        lines.append(f"- Verdict (descriptive, NOT promoted): "
                     f"**{consol['verdict']}**.")
        lines.append("")

    # --- §5 Bin-by-bin descriptive ---
    lines.append("## §5 Bin-by-bin descriptive characterisation")
    lines.append("")
    if halted:
        # Descriptive trajectory even on halt, since §2 has data
        means = results["sanity"]["bin_mean"]
        ns = results["sanity"]["bin_n"]
        lines.append(
            "Per pre-reg §10.3, the bin-by-bin descriptive characterisation "
            "is reported even on halt. With B1 (n=0) and B5 (n=1) "
            "structurally underpopulated, the **interpretable trajectory "
            "is across bins B2 → B3 → B4 only**:")
        lines.append("")
        lines.append("| bin | n | bin-mean gevoelscore | adjacent step (low − this) |")
        lines.append("|---|---:|---:|---:|")
        prev = None
        for b in range(5):
            m = means[b]
            n_b = ns[b]
            if prev is None or m is None:
                step_str = "—"
            else:
                step_str = f"{prev - m:+.3f}"
            m_str = f"{m:.3f}" if m is not None else "NA"
            lines.append(f"| B{b+1} | {n_b} | {m_str} | {step_str} |")
            prev = m
        lines.append("")
        lines.append(
            "**Descriptive read (qualifier: 3-bin support only; pre-reg "
            "verdict NOT computed)**: across B2 → B3 → B4 the bin-mean "
            f"trajectory is {means[1]:.3f} → {means[2]:.3f} → {means[3]:.3f} "
            "— **non-monotone** at the descriptive level (B3 mean rises "
            "above B2 before B4 drops below B2). The pre-reg §7.4 "
            "expectation under SUPPORTED is monotone-decreasing B1 → B5; "
            "with only B2-B4 visible AND the B2-B3-B4 sub-trajectory "
            "non-monotone, the convexity question is moot at the locked "
            "5-bin spec. The B5 (60+) single observation (gevoelscore = 1) "
            "is informally consistent with the SUPPORTED-direction tail "
            "but cannot be tested (n=1).")
        lines.append("")
        lines.append(
            "*This descriptive read is consistent with pre-reg §7.4 "
            "'no monotone relationship at all (e.g. flat or U-shaped) → "
            "REJECTED via condition (a) failure' AT THE VISIBLE-BINS LEVEL "
            "— but the formal §5.1 verdict is HALT (not REJECTED), because "
            "B1's structural absence means the locked 5-bin spec cannot be "
            "tested in the form locked.*")
        lines.append("")
    else:
        # Adjacent-bin step magnitudes
        means = results["primary"]["bin_mean"]
        lines.append("Adjacent-bin step magnitudes (positive = bin-mean DROP from low → high):")
        lines.append("")
        lines.append("| step | bin pair | magnitude (m_low − m_high) |")
        lines.append("|---|---|---:|")
        for i in range(4):
            mi, mj = means[i], means[i + 1]
            if mi is None or mj is None:
                step_str = "NA"
            else:
                step_str = f"{mi - mj:+.3f}"
            lines.append(f"| {i+1} | B{i+1}-B{i+2} | {step_str} |")
        lines.append("")
        lines.append(
            "Per pre-reg §7.1 SUPPORTED expectation: monotone decreasing "
            "(positive steps); accelerating decrement (B3→B4 step LARGER "
            "than B1→B2; B4→B5 expected largest).")
        lines.append("")

    # --- §6 E[L]* report ---
    lines.append("## §6 §4.7 E[L]* report (factor-of-2 flag)")
    lines.append("")
    if halted:
        lines.append("Not run (primary halted).")
        lines.append("")
    else:
        el = results["el_star"]
        lines.append("Per pre-reg §4.7 r2 amendment: two data-driven E[L]* checks "
                     "(linear-residual + bin-label).")
        lines.append("")
        lines.append("| derivation | E[L]* | cutoff lag | factor-of-2 flag | note |")
        lines.append("|---|---:|---:|:---:|---|")
        for k, label in (("linear_residual", "linear residual (continuous-predictor)"),
                         ("bin_label", "bin-label sequence")):
            e = el[k]
            lines.append(
                f"| {label} | {e['optimal_E_L']:.2f} | "
                f"{e['cutoff_lag']} | "
                f"{'**FLAG**' if e['flagged_deviation'] else 'ok'} | "
                f"{e.get('note') or ''} |")
        lines.append("")
        any_flag = el["linear_residual"]["flagged_deviation"] or el["bin_label"]["flagged_deviation"]
        v = results["primary"]["verdict"]["verdict"]
        if any_flag and v == "SUPPORTED":
            lines.append("**Flag fires on verdict-relevant cell** (verdict is SUPPORTED). "
                         "Per `permutation_null_block_length.md` the flag suggests the E[L]=7 "
                         "default may be mis-calibrated; report as caveat.")
        elif any_flag:
            lines.append("Flag fires but verdict is not SUPPORTED; descriptive context only "
                         "per `permutation_null_block_length.md`.")
        else:
            lines.append("No flags.")
        lines.append("")

    # --- §7 Caveats ---
    lines.append("## §7 Caveats (per pre-reg §8)")
    lines.append("")
    lines.append(
        "1. **Power-calc dispatch**: power calculation is **inapplicable per "
        "Daza 2018** ([within-subject n-of-1 design](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)). "
        "Block-permutation null at E[L]=7 is the within-subject inferential "
        "machinery; the 3-condition gated verdict is the decision rule.")
    lines.append(
        "2. **n=1 single-subject**: thresholds (p<0.05; S<0; spline 2nd-deriv "
        "negative at ≥3 of 4 midpoints) calibrated to the participant's "
        "distribution. No cross-subject generalisation claimed.")
    lines.append(
        f"3. **Citalopram-channel inheritance**: `all_day_stress_avg` is "
        f"CONFIRMED dose-modulated at +{DOSE_BETA_PER_MG}/mg. Primary uses "
        f"§5.A per-phase stratification (unmedicated headline); §5.B "
        f"dose-adjusted is cross-phase sensitivity. Reported §4 above.")
    lines.append(
        "4. **Crash-day inclusion fragility**: crashes KEPT in primary; "
        "crash-drop arm flagged if |Δ S| > 0.10 standardised OR sign-change. "
        "Reported §4 above (per CONVENTIONS §3.4).")
    lines.append(
        "5. **Within-subject SHAPE, not between-subject prediction**: the "
        "convex stress→fatigue claim is about THIS participant's mapping "
        "across days; no cross-person generalisation.")
    lines.append(
        "6. **No causal-direction inference**: test answers \"does the "
        "mapping have a convex shape?\", not \"does stress CAUSE fatigue?\".")
    lines.append(
        "7. **Wiggers' phrasing is qualitative**: the (0-20, 20-30, 30-40, "
        "40-60, 60+) binning is OUR operationalisation per the verification "
        "log; a REJECTED verdict at these specific bins does NOT universally "
        "falsify the qualitative \"stair-step\" framing.")
    lines.append(
        "8. **Independent obligations** (per `citalopram_phase_stratification` "
        "§6): autocorrelation (§4.7) + crash-drop (§4.6) + spike-companion "
        "(N/A; HA-C3 is the cross-day-aggregate test) + trajectory-detrend "
        "(N/A; this is not a pre-vs-post comparison).")
    lines.append(
        "9. **Test-session context**: this test was executed in a FRESH "
        "Claude session per `hypothesis_lock_process.md` §3.9.")
    lines.append(
        "10. **Sister-test cross-references**: HA-C4 v2 REJECTED at "
        "daily-aggregate (recovery-dynamics triad); HA11 SUPPORTED on train "
        "(within-day U-dip count). HA-C3's primary cell (cross-day-aggregate "
        "shape) is structurally distinct from both.")
    lines.append("")

    # --- §8 Reproducibility checklist ---
    lines.append("## §8 Reproducibility checklist")
    lines.append("")
    lines.append("- **Script**: `docs/research/analyses/hypotheses/HA-C3/test.py`")
    lines.append("- **Environment variable**: `GEVOELSCORE_DATA_PATH` "
                 "(default: `C:\\Users\\Gebruiker\\Documents\\gevoelscore-data`)")
    lines.append(f"- **Seed**: `RANDOM_SEED = {RANDOM_SEED}`")
    lines.append(f"- **Bootstrap**: B = {B_HEADLINE} stationary-bootstrap draws "
                 f"per condition; E[L] = {BOOTSTRAP_E_L} (geometric block length)")
    lines.append("- **Regenerate command**: `python docs/research/analyses/hypotheses/HA-C3/test.py`")
    lines.append("- **Dependencies**: numpy, scipy (for `CubicSpline`, "
                 "`mannwhitneyu`, `spearmanr`, `f.sf`); project utility "
                 "`docs/research/analyses/_utils/inference.py` for "
                 "`compute_data_driven_block_length` + `holm_step_down`.")
    lines.append(f"- **Spec commit**: `{R2_SPEC_COMMIT}` (LOCKED 2026-06-23)")
    if halted:
        lines.append("- **Halt artefact**: `dry-run-report.md` co-emitted; "
                     "`summary.json` contains the per-bin sample sizes + "
                     "gate-result detail. Full result-data not emitted "
                     "because the primary did not execute.")
    else:
        lines.append("- **Machine-readable companion**: `summary.json` "
                     "(gitignored per `docs/research/**/*.json`)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        f"*test.py run with `RANDOM_SEED = {RANDOM_SEED}`, "
        f"`BOOTSTRAP_E_L = {BOOTSTRAP_E_L}`, B = {B_HEADLINE} draws per condition. "
        f"Source: `per_day_master.csv` from `$GEVOELSCORE_DATA_PATH`. "
        f"Spec commit: `{R2_SPEC_COMMIT}`.*")
    OUT_RESULT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {OUT_RESULT_MD}", file=sys.stderr)


def write_summary_json(results: dict) -> None:
    def jsonify(o):
        if isinstance(o, dict):
            return {k: jsonify(v) for k, v in o.items()}
        if isinstance(o, list):
            return [jsonify(v) for v in o]
        if isinstance(o, tuple):
            return [jsonify(v) for v in o]
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            v = float(o)
            return None if math.isnan(v) else v
        if isinstance(o, np.ndarray):
            return [jsonify(v) for v in o.tolist()]
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, float) and math.isnan(o):
            return None
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, (str, int, bool)) or o is None:
            return o
        if isinstance(o, float):
            return o
        return str(o)
    OUT_SUMMARY_JSON.write_text(
        json.dumps(jsonify(results), indent=2), encoding="utf-8")
    print(f"Wrote {OUT_SUMMARY_JSON}", file=sys.stderr)


# === main ==============================================================

def main() -> None:
    parser = argparse.ArgumentParser(description="HA-C3 r2 test driver.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run §10.4 step 1 dry-run only.")
    parser.add_argument("--force-optA", action="store_true",
                        help="Force §7.3 halt-option-A even if Gate 1 passes "
                             "(diagnostic only).")
    args = parser.parse_args()

    print(f"Loading master from {MASTER_CSV}...", file=sys.stderr)
    master = load_master()
    print(f"  {len(master)} day-rows loaded.", file=sys.stderr)
    baseline_cutoff = find_device_baseline_cutoff(master)

    sanity = dry_run(master, baseline_cutoff)
    write_dry_run_report(sanity)

    if args.dry_run:
        sys.exit(1 if sanity["verdict"] == "HALT" else 0)

    # Determine halt-option-A application path
    applied_optA = False
    halt_detail = ""
    if sanity["verdict"] == "HALT" or args.force_optA:
        # Examine the gate-1 fail; only auto-apply optA if sole-B5 failure
        gate1_fails = [f for f in sanity["fails"] if f.get("gate") == 1]
        other_gate_fails = [f for f in sanity["fails"] if f.get("gate") != 1]
        sole_b5 = (len(gate1_fails) == 1
                   and gate1_fails[0].get("halt_optA_applicable"))
        if (sole_b5 and not other_gate_fails) or args.force_optA:
            print("\n  spec 7.3 halt-option-A APPLIED: widening B4 to absorb B5.",
                  file=sys.stderr)
            sanity["pool"] = apply_halt_optA(sanity["pool"])
            applied_optA = True
            # Re-run gates on collapsed pool to verify (no fresh halt expected)
            collapsed_sanity = run_sanity_gates(sanity["pool"])
            if collapsed_sanity["verdict"] == "HALT":
                halt_detail = ("§7.3 halt-option-A applied but collapsed pool "
                               "still fails sanity gates: "
                               f"{collapsed_sanity['fails']}")
                print(f"\n  HALT (post-optA): {halt_detail}", file=sys.stderr)
                # Persist halt status: emit halt result.md + summary
                halted_results = {
                    "spec_commit": R2_SPEC_COMMIT,
                    "halt_detail": halt_detail,
                    "sanity": {
                        "bin_n": sanity["bin_n"],
                        "bin_mean": sanity["bin_mean"],
                        "bin_median": sanity["bin_median"],
                        "stress_median": sanity["stress_median"],
                        "gevoelscore_median": sanity["gevoelscore_median"],
                        "total_n": sanity["total_n"],
                        "verdict": "HALT",
                        "fails": sanity["fails"],
                    },
                    "primary": None,
                }
                write_result_md(halted_results, halted=True, halt_detail=halt_detail)
                write_summary_json(halted_results)
                sys.exit(1)
            sanity = collapsed_sanity  # use collapsed pool for full run
        else:
            # Halt without optA: failure modes outside §7.3 pre-commitment
            halt_detail = "Sanity gates failed in ways not absorbed by §7.3 halt-option-A: "
            halt_detail += "; ".join(
                f"Gate {f['gate']} ({f['name']}): {f['detail']}"
                for f in sanity["fails"])
            print(f"\n  HALT: {halt_detail}", file=sys.stderr)
            halted_results = {
                "spec_commit": R2_SPEC_COMMIT,
                "halt_detail": halt_detail,
                "sanity": {
                    "bin_n": sanity["bin_n"],
                    "bin_mean": sanity["bin_mean"],
                    "bin_median": sanity["bin_median"],
                    "stress_median": sanity["stress_median"],
                    "gevoelscore_median": sanity["gevoelscore_median"],
                    "total_n": sanity["total_n"],
                    "verdict": "HALT",
                    "fails": sanity["fails"],
                },
                "sensitivity_5B": None,
                "primary": None,
            }
            write_result_md(halted_results, halted=True, halt_detail=halt_detail)
            write_summary_json(halted_results)
            sys.exit(1)

    print("\nDry-run sanity gates PASS (or §7.3 halt-option-A applied); "
          "running full test...", file=sys.stderr)
    results = run_full(master, baseline_cutoff, sanity, applied_optA=applied_optA)
    write_result_md(results, halted=False)
    write_summary_json(results)


if __name__ == "__main__":
    main()
