"""HA-C3p - Stage 2: convex stress -> fatigue on personal-baseline quintile bins.

Implements the LOCKED r2 HA-C3p pre-registration (hypothesis.md LOCKED
2026-06-23 at commit c0148ca). Sister pre-reg to HA-C3 v2 r1 - tests the
underlying convex stress -> fatigue shape claim on personal-baseline-anchored
equal-N quintile bins per CONVENTIONS section 3.1, rather than Wiggers'
verbatim 30 -> 40 numerical anchor (HA-C3 v2 carries that operationalisation).

Headline cell (per spec sections 1 + 5.0): unmedicated x 5-quintile-bin x
gevoelscore bin-mean x 3-condition gated outcome (Jonckheere-Terpstra monotone +
second-difference convexity contrast S = mean(D2_2, D2_3, D2_4) + spline
non-linearity with 4 internal knots at quintile bin boundaries) x
block-permutation null E[L]=7 (B=10,000).

3-condition gated verdict per spec section 5.1:
  SUPPORTED iff (a) + (b) + (c) all MET in prior direction;
  PARTIAL iff exactly 2-of-3 MET;
  REJECTED iff <=1-of-3 MET OR any wrong-direction firing.

Bins (per spec section 4.1, locked at draft time on per_day_master.csv SHA
d0ff9253):
  Q1 [0, 28), Q2 [28, 31), Q3 [31, 34), Q4 [34, 37), Q5 [37, 100]

Per-bin n forecast (per spec section 7.2):
  Full Stratum 4 pool: [248, 253, 294, 251, 305], total 1351
  Section 5.A unmedicated sub-arm: [45, 80, 129, 138, 189], total 581

Sensitivity arms (per spec section 4.8) reported alongside:
  - Section 5.B dose-adjusted cross-phase (predictor_adj = stress - 0.57 * dose_plasma_mg)
  - Crash-drop sensitivity (CONVENTIONS section 3.4)
  - Train/validate M3 overlay (per train_validate_split_fate.md section 5)
  - t+1 lagged variant (descriptive cross-test alignment)
  - z-scored vs 28d-lagged-baseline sensitivity (per Locked decision 2 +
    CONVENTIONS section 3.1)

Per spec section 4.7 (E[L]* checks): two derivations (linear-residual + bin-label).

Modes:
  python test.py --dry-run   spec section 7.5 sanity gates only (includes
                              Gate 5 snapshot SHA consistency check).
  python test.py             dry-run first, halt on failure, else full
                              run; emits result.md + result-data.json
                              (the JSON file is gitignored per
                              docs/research/**/*.json).

ASCII-only stdout per session handoff; markdown may use unicode.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
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
# Project layout: docs/research/analyses/_utils/inference.py
UTILS_DIR = HERE.parent.parent / "_utils"
if str(UTILS_DIR) not in sys.path:
    sys.path.insert(0, str(UTILS_DIR))

from inference import (  # noqa: E402
    compute_data_driven_block_length,
    holm_step_down,
)

# === Constants per LOCKED r2 hypothesis.md =============================

# spec section 10.2 + section 10.5: HA-C3p seed
RANDOM_SEED = 20260624
BOOTSTRAP_E_L = 7
B_HEADLINE = 10_000

# spec section 4.4 dose-adjustment coefficient (citalopram_dose_response section 5.6.1)
DOSE_BETA_PER_MG = 0.57

# spec section 4.5.1 + section 5.1 verdict bars
P_BAR = 0.05
S_NEG_BAR = 0.0
SPLINE_MIDPOINT_COUNT_BAR = 3  # >= 3 of 4 contributing midpoints (Q1 x=14 dropped)

# spec section 4.1 quintile bin edges (left-inclusive, right-exclusive except Q5)
# Q1 [0, 28), Q2 [28, 31), Q3 [31, 34), Q4 [34, 37), Q5 [37, 100]
BIN_EDGES = [0.0, 28.0, 31.0, 34.0, 37.0, 100.0]
BIN_LABELS = [
    "Q1[0,28)", "Q2[28,31)", "Q3[31,34)", "Q4[34,37)", "Q5[37,100]"
]
# spec section 4.1 bin midpoints; Q1 (x=14) dropped per spec section 4.5.1(c)
# natural-cubic boundary condition forces near-zero secderiv on leftmost segment.
BIN_MIDPOINTS_FULL = [14.0, 29.5, 32.5, 35.5, 68.5]
BIN_MIDPOINTS_FOR_SPLINE = BIN_MIDPOINTS_FULL[1:]  # 29.5, 32.5, 35.5, 68.5

# spec section 4.5.1.5 companion contrast (5-bin orthogonal quadratic per v1 r2 form)
COMPANION_CONTRAST = np.asarray([+2, -1, -2, -1, +2], dtype=float)
LINEAR_CONTRAST = np.asarray([-2, -1, 0, +1, +2], dtype=float)
assert int(np.dot(COMPANION_CONTRAST, LINEAR_CONTRAST)) == 0, \
    "Companion contrast must be orthogonal to linear contrast at lock"

# Spline internal knots = bin boundaries (28, 31, 34, 37) per spec section 4.5.1(c)
SPLINE_INTERNAL_KNOTS = [28.0, 31.0, 34.0, 37.0]

# spec section 7.5 sanity gates
MIN_BIN_N = 30
MIN_TOTAL_N = 100
GATE2_STRESS_MEDIAN_RANGE = (20.0, 60.0)
GATE3_GEVOELSCORE_MEDIAN_RANGE = (3.0, 6.0)

# spec section 7.5 Gate 5: snapshot SHA consistency check
EXPECTED_SNAPSHOT_SHA = (
    "d0ff9253f7199a40165b6d229a4a68534b4a36b7de87bfbe8a18c23bb9ab189d"
)
GATE5_BOUNDARY_TOLERANCE_STRESS_UNITS = 1.0
EXPECTED_QUINTILE_BOUNDARIES = (28.0, 31.0, 34.0, 37.0)

# spec section 4.7 E[L]* factor-of-2 deviation
EL_DEVIATION_FACTOR = 0.5

# spec section 4.3 + section 6 exclusions
LC_ERA_START = date(2022, 4, 4)
UNMEDICATED_END_INCL = date(2024, 4, 8)
APRIL2024_CLUSTER_START = date(2024, 4, 9)
APRIL2024_CLUSTER_END_INCL = date(2024, 4, 16)
DEVICE_BASELINE_DAYS = 21
# Train/validate split (M3 overlay only)
TRAIN_END = date(2023, 12, 31)
VALIDATE_START = date(2024, 1, 1)

# z-score sensitivity arm baseline window (Locked decision 2; HA01b-recomputed
# precedent + CONVENTIONS section 3.1 prototype)
Z_SCORE_LAGGED_WINDOW_DAYS = 28

# Pre-reg lock commit
R2_SPEC_COMMIT = "c0148ca"

# Paths
DATA_ROOT = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH",
    r"C:\Users\Gebruiker\Documents\gevoelscore-data"))
MASTER_CSV = DATA_ROOT / "unified" / "per_day_master.csv"

OUT_RESULT_MD = HERE / "result.md"
OUT_RESULT_JSON = HERE / "result-data.json"
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


def sha256_path(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while True:
            blk = fh.read(1 << 16)
            if not blk:
                break
            h.update(blk)
    return h.hexdigest()


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
    """Last date of the first DEVICE_BASELINE_DAYS days of has_garmin_uds=True."""
    n_uds = 0
    for d in sorted(master.keys()):
        row = master.get(d) or {}
        if (row.get("has_garmin_uds", "") or "").strip().lower() == "true":
            n_uds += 1
            if n_uds == DEVICE_BASELINE_DAYS:
                return d
    return None


# === Eligibility (spec section 4.3 + 6) ================================

def assign_bin(s: float, edges=BIN_EDGES) -> int | None:
    """Return bin index 0..4 for value s; None if outside [edges[0], edges[-1]]."""
    n_bins = len(edges) - 1
    if s < edges[0] or s > edges[-1]:
        return None
    for i in range(n_bins):
        lo = edges[i]
        hi = edges[i + 1]
        if i == n_bins - 1:
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
    """spec section 4.3 day-validity gate.

    phase: 'unmedicated' (primary section 5.A), 'all' (cross-phase section 5.B),
           'stratum4' (full Stratum 4 = all LC era).
    """
    if d < LC_ERA_START:
        return False
    if phase == "unmedicated" and d > UNMEDICATED_END_INCL:
        return False
    # spec section 4.3 + 6: April 2024 cluster always excluded
    if APRIL2024_CLUSTER_START <= d <= APRIL2024_CLUSTER_END_INCL:
        return False
    # spec section 6: first 21 device-baseline days
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
               drop_crashes: bool = False,
               edges: list = BIN_EDGES) -> dict:
    """Build temporal pool of (date, stress, gevoelscore, bin, is_crash).

    For dose_adjusted=True: predictor_adj = raw - DOSE_BETA * dose_plasma_mg.
    For lag_t_plus_1=True: outcome is gevoelscore[T+1], predictor is stress[T].
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
        b = assign_bin(s_use, edges=edges)
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


def build_zscore_pool(master: dict, baseline_cutoff: date | None,
                      phase: str = "unmedicated") -> dict | None:
    """Build z-scored-vs-28d-lagged-baseline pool per spec section 4.8(b) +
    Locked decision 2.

    Computes stress_z_28d_lagged(d) = (s[d] - median(s[d-28:d])) / MAD(s[d-28:d])
    on the LC-era + non-NaN time series. Then re-bins into quintiles of the
    z-score distribution on the *Stratum 4 full pool* (per spec section 4.8b,
    "Re-bin into quintiles of the stress_z_28d_lagged distribution on the
    full Stratum 4 pool"). Sub-arm restriction to `phase` is applied after
    binning so the bin edges remain stationary across sub-arms.

    Returns None if z-score quintile computation fails (insufficient data).
    """
    # Build full LC time series (no phase restriction) for the lagged baseline
    rows_lc = []
    dates_sorted = sorted(master.keys())
    for d in dates_sorted:
        row = master.get(d) or {}
        # Only require LC era + non-NaN stress + non-NaN gevoelscore (rest of
        # the gates apply later when sub-arm is filtered)
        if d < LC_ERA_START:
            continue
        s = parse_float(row.get("all_day_stress_avg", ""))
        if s is None or s < 0.0 or s > 100.0:
            continue
        g = parse_float(row.get("gevoelscore", ""))
        if g is None:
            continue
        rows_lc.append({
            "date": d, "stress_raw": s, "gevoelscore": g,
            "is_crash": (row.get("is_crash", "") or "").strip().lower() == "true",
        })
    if len(rows_lc) < 2 * Z_SCORE_LAGGED_WINDOW_DAYS:
        return None

    # Build per-date map of stress values for the lagged baseline lookup
    stress_by_date = {r["date"]: r["stress_raw"] for r in rows_lc}

    # Compute z_28d_lagged for each row
    z_rows = []
    for r in rows_lc:
        d = r["date"]
        # lagged baseline window: [d - 28, d - 1] inclusive (excludes day d)
        baseline_vals = []
        for k in range(1, Z_SCORE_LAGGED_WINDOW_DAYS + 1):
            d_k = d - timedelta(days=k)
            if d_k in stress_by_date and d_k >= LC_ERA_START:
                baseline_vals.append(stress_by_date[d_k])
        if len(baseline_vals) < Z_SCORE_LAGGED_WINDOW_DAYS // 2:
            # Insufficient baseline; skip
            continue
        baseline_arr = np.asarray(baseline_vals, dtype=float)
        med = float(np.median(baseline_arr))
        mad = float(np.median(np.abs(baseline_arr - med)))
        if mad == 0:
            # All baseline values identical; z undefined. Use 1.0 as MAD floor
            # (a robust analog of the std=0 fallback; avoids div-by-zero).
            mad = 1.0
        z = (r["stress_raw"] - med) / (1.4826 * mad)  # 1.4826 normalises MAD to sd
        z_rows.append({
            "date": d, "z": z, "stress_raw": r["stress_raw"],
            "gevoelscore": r["gevoelscore"], "is_crash": r["is_crash"],
        })

    if len(z_rows) < 100:
        return None

    # Build Stratum 4 z-distribution + quintile edges (spec section 4.8b:
    # quintiles of z on the *full Stratum 4 pool*, applied to the LC era +
    # excluding April 2024 cluster + device-baseline-warmup)
    baseline_cutoff_local = baseline_cutoff
    z_strat4 = []
    for r in z_rows:
        d = r["date"]
        if APRIL2024_CLUSTER_START <= d <= APRIL2024_CLUSTER_END_INCL:
            continue
        if baseline_cutoff_local is not None and d <= baseline_cutoff_local:
            continue
        z_strat4.append(r["z"])
    if len(z_strat4) < 100:
        return None
    z_strat4_arr = np.asarray(z_strat4, dtype=float)
    z_qs = np.quantile(z_strat4_arr, [0.2, 0.4, 0.6, 0.8])
    z_edges = [float(-1e9)] + [float(x) for x in z_qs.tolist()] + [float(1e9)]

    # Now apply sub-arm filtering + bin assignment using the stationary z_edges
    filtered = []
    for r in z_rows:
        d = r["date"]
        if APRIL2024_CLUSTER_START <= d <= APRIL2024_CLUSTER_END_INCL:
            continue
        if baseline_cutoff_local is not None and d <= baseline_cutoff_local:
            continue
        if phase == "unmedicated" and d > UNMEDICATED_END_INCL:
            continue
        b = assign_bin(r["z"], edges=z_edges)
        if b is None:
            continue
        filtered.append({
            "date": d, "z": r["z"], "stress_raw": r["stress_raw"],
            "gevoelscore": r["gevoelscore"], "bin": b,
            "is_crash": r["is_crash"],
        })

    return {
        "dates": np.asarray([r["date"] for r in filtered]),
        "z": np.asarray([r["z"] for r in filtered], dtype=float),
        "stress_raw": np.asarray([r["stress_raw"] for r in filtered], dtype=float),
        # spline uses z as predictor in this arm; populate stress_use as z
        "stress_use": np.asarray([r["z"] for r in filtered], dtype=float),
        "gevoelscore": np.asarray([r["gevoelscore"] for r in filtered], dtype=float),
        "bin": np.asarray([r["bin"] for r in filtered], dtype=int),
        "is_crash": np.asarray([r["is_crash"] for r in filtered], dtype=bool),
        "n": len(filtered),
        "z_quintile_edges": z_edges,
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

    Per spec section 4.5.2: CI per bin from stationary bootstrap at E[L]=7.
    """
    n = pool["n"]
    if n == 0:
        return {f"Q{b+1}": (None, None) for b in range(5)}
    p_geom = 1.0 / expected_block_length
    g = pool["gevoelscore"]
    bins = pool["bin"]
    boot_means = np.full((B, 5), float("nan"))
    for b_iter in range(B):
        idx = stationary_bootstrap_indices(n, p_geom, rng)
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
            cis[f"Q{bi+1}"] = (
                float(np.quantile(col, 0.025)),
                float(np.quantile(col, 0.975)),
            )
        else:
            cis[f"Q{bi+1}"] = (None, None)
    return cis


# === Statistics =========================================================

def jonckheere_terpstra(values_by_bin: list[np.ndarray]) -> dict:
    """One-sided Jonckheere-Terpstra trend test.

    Tests H0: no trend vs H1: monotone-decreasing across bins.
    Test statistic J counts pairs with bin_i sample > bin_j sample for i<j;
    standardised J* reported alongside.
    """
    K = len(values_by_bin)
    if K < 2:
        return {"J_obs": float("nan"), "J_star": float("nan"),
                "n_per_bin": [len(v) for v in values_by_bin]}
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
            xj_sorted = np.sort(xj)
            less = np.searchsorted(xj_sorted, xi, side="left")
            equal = (np.searchsorted(xj_sorted, xi, side="right")
                     - np.searchsorted(xj_sorted, xi, side="left"))
            J += float(less.sum()) + 0.5 * float(equal.sum())
    mu_J = (N * N - sum(ni * ni for ni in n)) / 4.0
    var_J = (N * N * (2 * N + 3) - sum(ni * ni * (2 * ni + 3) for ni in n)) / 72.0
    sd_J = math.sqrt(var_J) if var_J > 0 else float("nan")
    J_star = (J - mu_J) / sd_J if sd_J and not math.isnan(sd_J) else float("nan")
    return {
        "J_obs": float(J), "mu_J": float(mu_J), "sd_J": float(sd_J),
        "J_star": float(J_star), "n_per_bin": n,
    }


def second_diff_S(bin_means: np.ndarray) -> float:
    """spec section 4.5.1(b) S = (D2_2 + D2_3 + D2_4) / 3, 5-bin form."""
    if np.any(np.isnan(bin_means)) or len(bin_means) < 5:
        return float("nan")
    d2 = []
    for i in (1, 2, 3):
        d2.append(bin_means[i + 1] - 2.0 * bin_means[i] + bin_means[i - 1])
    return float(np.mean(d2))


def companion_contrast(bin_means: np.ndarray) -> float:
    """spec section 4.5.1.5 c . m with c = (+2,-1,-2,-1,+2)."""
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


def _means_per_bin(g: np.ndarray, bins: np.ndarray) -> np.ndarray:
    out = np.full(5, float("nan"))
    for b in range(5):
        m = bins == b
        if m.any():
            out[b] = float(g[m].mean())
    return out


def _spline_F_from_stress_g(s: np.ndarray, g: np.ndarray) -> float:
    """F-statistic comparing natural-cubic-spline-with-4-internal-knots
    (knots at SPLINE_INTERNAL_KNOTS = [28, 31, 34, 37]) against linear-only.

    Uses Hastie/Tibshirani ESL section 5.2.1 eq (5.5) natural-spline basis.
    """
    if len(s) < 6:
        return float("nan")
    n = len(s)
    knots = SPLINE_INTERNAL_KNOTS
    X_lin = np.column_stack([np.ones(n), s])
    K = len(knots)

    def trunc_cube(x, k):
        d = x - k
        return np.where(d > 0, d * d * d, 0.0)

    def natural_basis(s):
        K_local = len(knots)
        d = []
        for k in range(K_local - 1):
            denom = knots[K_local - 1] - knots[k]
            d_k = (trunc_cube(s, knots[k]) - trunc_cube(s, knots[K_local - 1])) / denom
            d.append(d_k)
        cols = []
        for k in range(K_local - 2):
            cols.append(d[k] - d[K_local - 2])
        return np.column_stack(cols) if cols else np.zeros((n, 0))

    NB = natural_basis(s)
    X_full = np.column_stack([np.ones(n), s, NB])
    try:
        beta_lin, _, _, _ = np.linalg.lstsq(X_lin, g, rcond=None)
    except np.linalg.LinAlgError:
        return float("nan")
    try:
        beta_full, _, _, _ = np.linalg.lstsq(X_full, g, rcond=None)
    except np.linalg.LinAlgError:
        return float("nan")
    resid_lin = g - X_lin @ beta_lin
    rss_lin = float((resid_lin * resid_lin).sum())
    resid_full = g - X_full @ beta_full
    rss_full = float((resid_full * resid_full).sum())
    p_lin = X_lin.shape[1]
    p_full = X_full.shape[1]
    df_diff = p_full - p_lin
    df_resid = n - p_full
    if df_diff <= 0 or df_resid <= 0 or rss_full <= 0:
        return float("nan")
    F = ((rss_lin - rss_full) / df_diff) / (rss_full / df_resid)
    return float(F)


def _spline_F_and_secderiv(pool: dict) -> tuple[float, list[float]]:
    """Natural cubic spline regression on (stress, gevoelscore); returns
    F-stat (full vs linear-only) and second-derivative at the 4 contributing
    bin midpoints per spec section 4.5.1(c).

    For the secderiv, we fit a CubicSpline through the 5 bin-mean knots at
    BIN_MIDPOINTS_FULL with natural BC; evaluate cs''(x) at the 4
    contributing midpoints.
    """
    s = pool["stress_use"]
    g = pool["gevoelscore"]
    if len(s) < 6:
        return float("nan"), [float("nan")] * 4
    means = _means_per_bin(g, pool["bin"])
    valid = ~np.isnan(means)
    n_valid = int(valid.sum())
    if n_valid < 4:
        return float("nan"), [float("nan")] * 4
    x_full = np.asarray(BIN_MIDPOINTS_FULL, dtype=float)
    x_fit = x_full[valid]
    y_fit = means[valid]
    try:
        cs = CubicSpline(x_fit, y_fit, bc_type="natural")
    except Exception:
        return float("nan"), [float("nan")] * 4
    F = _spline_F_from_stress_g(s, g)
    sd = []
    cs2 = cs.derivative(2)
    for x in BIN_MIDPOINTS_FOR_SPLINE:
        try:
            sd.append(float(cs2(x)))
        except Exception:
            sd.append(float("nan"))
    return F, sd


def _spline_F_parametric(pool: dict) -> tuple[float, float]:
    """Parametric F + p (descriptive only per spec section 4.5.1(c))."""
    from scipy import stats as sps
    s = pool["stress_use"]
    g = pool["gevoelscore"]
    if len(s) < 6:
        return float("nan"), float("nan")
    F = _spline_F_from_stress_g(s, g)
    if math.isnan(F):
        return float("nan"), float("nan")
    n = len(s)
    df_diff = 2  # K - 2 with K = 4 internal knots
    df_resid = n - 4
    if df_resid <= 0:
        return F, float("nan")
    p = float(sps.f.sf(F, df_diff, df_resid))
    return F, p


def block_permutation_three_conditions(pool: dict, B: int,
                                        expected_block_length: int,
                                        rng: np.random.Generator) -> dict:
    """spec section 4.7 block-permutation null for the 3 primary conditions.

    Permutation target: bin_label sequence is resampled via stationary
    bootstrap (geometric block length E[L]=7), keeping gevoelscore in
    original temporal position.
    """
    n = pool["n"]
    p_geom = 1.0 / expected_block_length
    g = pool["gevoelscore"]
    bins_obs = pool["bin"]

    obs_means = _means_per_bin(g, bins_obs)
    obs_jt = jonckheere_terpstra(
        [g[bins_obs == b] for b in range(5)])
    obs_J_star = obs_jt["J_star"]
    obs_S = second_diff_S(obs_means)
    obs_companion = companion_contrast(obs_means)
    obs_spline_F, obs_spline_secderiv = _spline_F_and_secderiv(pool)

    null_J_star = np.full(B, float("nan"))
    null_S = np.full(B, float("nan"))
    null_F = np.full(B, float("nan"))
    null_companion = np.full(B, float("nan"))

    for b_iter in range(B):
        idx = stationary_bootstrap_indices(n, p_geom, rng)
        bins_null = bins_obs[idx]
        means_null = _means_per_bin(g, bins_null)
        if np.any(np.isnan(means_null)):
            grand = float(g.mean())
            means_null = np.where(np.isnan(means_null), grand, means_null)
        jt = jonckheere_terpstra([g[bins_null == bb] for bb in range(5)])
        null_J_star[b_iter] = jt["J_star"]
        null_S[b_iter] = second_diff_S(means_null)
        null_companion[b_iter] = companion_contrast(means_null)
        pseudo_stress = np.asarray([BIN_MIDPOINTS_FULL[bn] for bn in bins_null],
                                   dtype=float)
        F_null = _spline_F_from_stress_g(pseudo_stress, g)
        null_F[b_iter] = F_null

    obs_pseudo_stress = np.asarray([BIN_MIDPOINTS_FULL[bn] for bn in bins_obs],
                                   dtype=float)
    obs_F_midpoint = _spline_F_from_stress_g(obs_pseudo_stress, g)

    # Empirical one-sided p-values
    n_le = int((null_J_star <= obs_J_star).sum())
    p_a = (1 + n_le) / (B + 1)
    n_le_s = int((null_S <= obs_S).sum())
    p_b = (1 + n_le_s) / (B + 1)
    n_ge_f = int((null_F >= obs_F_midpoint).sum())
    p_c = (1 + n_ge_f) / (B + 1)
    n_le_c = int((null_companion <= obs_companion).sum())
    p_companion = (1 + n_le_c) / (B + 1)

    parametric_F, parametric_p = _spline_F_parametric(pool)

    return {
        "obs": {
            "J_star": float(obs_J_star) if not math.isnan(obs_J_star) else None,
            "S": float(obs_S) if not math.isnan(obs_S) else None,
            "spline_F_block_perm_target": float(obs_F_midpoint) if not math.isnan(obs_F_midpoint) else None,
            "spline_F_continuous_predictor": float(obs_spline_F) if not math.isnan(obs_spline_F) else None,
            "spline_second_derivative_at_midpoints": [
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


def mann_whitney_pairwise(pool: dict) -> list[dict]:
    """Adjacent-bin pairwise Mann-Whitney (4 pairs per spec section 4.5.2)."""
    from scipy import stats as sps
    g = pool["gevoelscore"]
    bins = pool["bin"]
    out = []
    for i in range(4):
        gi = g[bins == i]
        gj = g[bins == i + 1]
        if len(gi) < 2 or len(gj) < 2:
            out.append({
                "pair": f"Q{i+1}-Q{i+2}",
                "n_i": int(len(gi)), "n_j": int(len(gj)),
                "U": None, "p_two_sided": None,
            })
            continue
        try:
            U, p = sps.mannwhitneyu(gi, gj, alternative="two-sided")
            out.append({
                "pair": f"Q{i+1}-Q{i+2}",
                "n_i": int(len(gi)), "n_j": int(len(gj)),
                "U": float(U), "p_two_sided": float(p),
            })
        except Exception:
            out.append({
                "pair": f"Q{i+1}-Q{i+2}",
                "n_i": int(len(gi)), "n_j": int(len(gj)),
                "U": None, "p_two_sided": None,
            })
    return out


def spearman_rho(pool: dict) -> dict:
    """Spearman rho on continuous (stress, gevoelscore) per spec section 4.5.2."""
    from scipy import stats as sps
    s = pool["stress_use"]
    g = pool["gevoelscore"]
    if len(s) < 3:
        return {"rho": None, "p": None, "n": int(len(s))}
    rho, p = sps.spearmanr(s, g)
    return {"rho": float(rho), "p": float(p), "n": int(len(s))}


# === Verdict gating (spec section 5.1 3-condition) =====================

def verdict_three_condition(perm: dict, spline_secderiv: list[float]) -> dict:
    """spec section 5.1 3-condition gated verdict."""
    p = perm["p_values"]
    obs = perm["obs"]
    p_a = p["p_a_jonckheere_decreasing"]
    p_b = p["p_b_S_convex"]
    p_c = p["p_c_spline_nonlinearity"]
    a_direction_ok = (obs["J_star"] is not None) and (obs["J_star"] < 0)
    b_direction_ok = (obs["S"] is not None) and (obs["S"] < 0)
    valid_sd = [x for x in spline_secderiv if x is not None and not math.isnan(x)]
    n_neg = sum(1 for x in valid_sd if x < 0)
    c_direction_ok = n_neg >= SPLINE_MIDPOINT_COUNT_BAR

    a_met = (p_a < P_BAR) and a_direction_ok
    b_met = (p_b < P_BAR) and b_direction_ok
    c_met = (p_c < P_BAR) and c_direction_ok

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


# === Sanity gates (spec section 7.5) ===================================

def run_sanity_gates(pool: dict, full_stratum4_pool: dict | None = None,
                     snapshot_sha: str | None = None) -> dict:
    """spec section 7.5 Gates 1-5.

    Gate 5: snapshot SHA + quintile-boundary consistency check (verify
    per_day_master.csv SHA matches d0ff9253 AND recomputed quintile
    boundaries on the full Stratum 4 pool shift by no more than 1
    stress-unit from the locked draft-time edges (28, 31, 34, 37)).
    """
    desc = bin_descriptives(pool)
    bin_n = desc["bin_n"]
    fails: list[dict] = []

    # Gate 1: each bin n >= 30
    n_below_30 = [b for b in range(5) if bin_n[b] < MIN_BIN_N]
    gate1_ok = len(n_below_30) == 0
    if not gate1_ok:
        fails.append({
            "gate": 1, "name": "per-bin n >= 30",
            "detail": f"bins below threshold: "
                      f"{[(f'Q{b+1}', bin_n[b]) for b in n_below_30]}; "
                      f"HA-C3p has NO halt-option-A pre-commit per spec "
                      f"section 7.3 (equal-N quintile design eliminates "
                      f"structurally-absent bin failure mode at draft-time "
                      f"forecast). Any failure here requires HA-C3p-v2 redraft.",
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

    # Gate 4: total n >= 100 AND all 5 bins n >= 30 (spec section 7.5 Gate 4)
    total_n = sum(bin_n)
    n_at_least_30 = sum(1 for b in range(5) if bin_n[b] >= MIN_BIN_N)
    gate4_ok = (n_at_least_30 == 5) and (total_n >= MIN_TOTAL_N)
    if not gate4_ok:
        fails.append({
            "gate": 4, "name": "power density (all 5 bins n>=30 AND total n>=100)",
            "detail": (f"bins with n>=30: {n_at_least_30}/5; total n: {total_n}"),
        })

    # Gate 5: snapshot SHA + quintile-boundary consistency
    gate5_sha_ok = None
    gate5_boundary_ok = None
    gate5_observed_sha = snapshot_sha
    gate5_observed_boundaries = None
    if snapshot_sha is not None:
        gate5_sha_ok = (snapshot_sha == EXPECTED_SNAPSHOT_SHA)
        if not gate5_sha_ok:
            fails.append({
                "gate": 5, "name": "snapshot SHA-256 matches locked d0ff9253",
                "detail": (f"observed SHA = {snapshot_sha}; "
                           f"expected = {EXPECTED_SNAPSHOT_SHA}. Data drift "
                           f"between draft and execution would invalidate the "
                           f"locked bin boundaries. HALT immediately."),
            })
    if full_stratum4_pool is not None and full_stratum4_pool.get("n", 0) > 0:
        # Re-compute quintile boundaries on the full Stratum 4 stress series
        # (this requires the *raw* full-pool stress series; the pool was
        # built with the locked edges, but we can still extract the raw
        # stress values from `stress_use`).
        s4 = full_stratum4_pool["stress_use"]
        qs = np.quantile(s4, [0.2, 0.4, 0.6, 0.8])
        gate5_observed_boundaries = [float(x) for x in qs.tolist()]
        max_shift = max(
            abs(qs[i] - EXPECTED_QUINTILE_BOUNDARIES[i]) for i in range(4)
        )
        gate5_boundary_ok = max_shift <= GATE5_BOUNDARY_TOLERANCE_STRESS_UNITS
        if not gate5_boundary_ok:
            fails.append({
                "gate": 5, "name": "quintile boundary shift <= 1 stress-unit",
                "detail": (f"recomputed boundaries (q=0.2,0.4,0.6,0.8) = "
                           f"{gate5_observed_boundaries}; locked = "
                           f"{list(EXPECTED_QUINTILE_BOUNDARIES)}; "
                           f"max shift = {max_shift:.3f} > "
                           f"{GATE5_BOUNDARY_TOLERANCE_STRESS_UNITS} stress-units. "
                           f"Locked bin boundaries are invalidated by the new "
                           f"snapshot; HA-C3p-v2 redraft required."),
            })

    return {
        "bin_n": bin_n, "bin_mean": desc["bin_mean"], "bin_median": desc["bin_median"],
        "stress_median": s_med, "gevoelscore_median": g_med, "total_n": total_n,
        "gate1_ok": gate1_ok, "gate2_ok": gate2_ok, "gate3_ok": gate3_ok,
        "gate4_ok": gate4_ok,
        "gate5_sha_ok": gate5_sha_ok,
        "gate5_boundary_ok": gate5_boundary_ok,
        "gate5_observed_sha": gate5_observed_sha,
        "gate5_observed_boundaries": gate5_observed_boundaries,
        "fails": fails,
        "verdict": "PASS" if not fails else "HALT",
    }


# === Dry-run + write reports ===========================================

def dry_run(master: dict, baseline_cutoff: date | None,
            snapshot_sha: str) -> dict:
    print("", file=sys.stderr)
    print("=== HA-C3p r2 dry-run ===", file=sys.stderr)
    print(f"  RANDOM_SEED={RANDOM_SEED}; B={B_HEADLINE}; E[L]={BOOTSTRAP_E_L}",
          file=sys.stderr)
    print(f"  spec commit: {R2_SPEC_COMMIT}", file=sys.stderr)
    print(f"  snapshot SHA-256: {snapshot_sha}", file=sys.stderr)
    print(f"  expected SHA-256: {EXPECTED_SNAPSHOT_SHA}", file=sys.stderr)
    if baseline_cutoff is not None:
        print(f"  device baseline cutoff (excl <=): {baseline_cutoff}",
              file=sys.stderr)
    print("", file=sys.stderr)

    # spec section 7.5 Gate 5 (snapshot SHA) FIRST - HALT immediately if drift.
    if snapshot_sha != EXPECTED_SNAPSHOT_SHA:
        print(f"  Gate 5 (snapshot SHA): FAIL - HALT immediately. "
              f"Data drift invalidates locked bin boundaries.",
              file=sys.stderr)

    # Build pools
    print("Building full Stratum 4 pool (for Gate 5 boundary recomputation)...",
          file=sys.stderr)
    pool_s4 = build_pool(master, baseline_cutoff, phase="all")
    print(f"  full Stratum 4 pool n = {pool_s4['n']}", file=sys.stderr)

    print("Building primary unmedicated pool (spec section 4.2 + 4.3 + section "
          "5.A)...", file=sys.stderr)
    pool = build_pool(master, baseline_cutoff, phase="unmedicated")
    print(f"  pool n = {pool['n']}", file=sys.stderr)

    sanity = run_sanity_gates(pool, full_stratum4_pool=pool_s4,
                              snapshot_sha=snapshot_sha)
    print("\n--- spec section 7.5 sanity gate results ---", file=sys.stderr)
    print(f"  bin sizes (unmedicated): {sanity['bin_n']}", file=sys.stderr)
    print(f"  full Stratum 4 bin sizes: "
          f"{[int((pool_s4['bin'] == b).sum()) for b in range(5)]}",
          file=sys.stderr)
    print(f"  bin means: "
          f"{[f'{m:.3f}' if m is not None else 'NA' for m in sanity['bin_mean']]}",
          file=sys.stderr)
    print(f"  stress median (unmedicated): {sanity['stress_median']:.2f}",
          file=sys.stderr)
    print(f"  gevoelscore median (unmedicated): {sanity['gevoelscore_median']:.2f}",
          file=sys.stderr)
    print(f"  total n (unmedicated): {sanity['total_n']}", file=sys.stderr)
    print(f"  gate 1 (per-bin n>=30): "
          f"{'PASS' if sanity['gate1_ok'] else 'FAIL'}", file=sys.stderr)
    print(f"  gate 2 (stress median in [20,60]): "
          f"{'PASS' if sanity['gate2_ok'] else 'FAIL'}", file=sys.stderr)
    print(f"  gate 3 (gevoelscore median in [3,6]): "
          f"{'PASS' if sanity['gate3_ok'] else 'FAIL'}", file=sys.stderr)
    print(f"  gate 4 (all 5 bins n>=30 AND total>=100): "
          f"{'PASS' if sanity['gate4_ok'] else 'FAIL'}", file=sys.stderr)
    g5_sha = sanity['gate5_sha_ok']
    g5_bnd = sanity['gate5_boundary_ok']
    print(f"  gate 5 (snapshot SHA matches d0ff9253): "
          f"{'PASS' if g5_sha else 'FAIL' if g5_sha is False else 'NA'}",
          file=sys.stderr)
    print(f"  gate 5 (boundary shift <=1 stress-unit): "
          f"{'PASS' if g5_bnd else 'FAIL' if g5_bnd is False else 'NA'}",
          file=sys.stderr)
    print(f"  gate 5 recomputed boundaries: "
          f"{sanity['gate5_observed_boundaries']}", file=sys.stderr)
    print(f"  verdict: {sanity['verdict']}", file=sys.stderr)
    sanity["pool"] = pool
    sanity["pool_stratum4"] = pool_s4
    return sanity


def write_dry_run_report(sanity: dict) -> None:
    halt = sanity["verdict"] == "HALT"
    title = ("HA-C3p r2 dry-run report - SANITY GATE FAILURE (HALT)"
             if halt else "HA-C3p r2 dry-run report - sanity gates PASS")
    lines = [
        f"# {title}",
        "",
        ("Emitted by `test.py --dry-run` per LOCKED r2 hypothesis.md section "
         "10.4. **Headline cell**: unmedicated x 5-quintile-bin x `gevoelscore` "
         "x 3-condition gated outcome x block-permutation null at E[L]=7. "
         "Day-validity per section 4.3 (LC era + unmedicated + not "
         "April-2024 cluster + not first 21 device-baseline days + non-NaN "
         "both columns)."),
        "",
        f"- Unmedicated pool n = {sanity['total_n']}",
        f"- Stress median = {sanity['stress_median']:.2f}",
        f"- Gevoelscore median = {sanity['gevoelscore_median']:.2f}",
        "",
        "## Per-bin sample sizes (unmedicated, `all_day_stress_avg` quintile bins)",
        "",
        "| bin | label | n | mean gevoelscore | median gevoelscore |",
        "|---|---|---:|---:|---:|",
    ]
    for b in range(5):
        m = sanity["bin_mean"][b]
        md = sanity["bin_median"][b]
        lines.append(
            f"| Q{b+1} | {BIN_LABELS[b]} | {sanity['bin_n'][b]} | "
            f"{f'{m:.3f}' if m is not None else 'NA'} | "
            f"{f'{md:.2f}' if md is not None else 'NA'} |")
    lines.append("")
    lines.append("## Gate results")
    lines.append("")
    lines.append("| gate | description | result |")
    lines.append("|---|---|---|")
    lines.append(f"| 1 | per-bin n >= {MIN_BIN_N} (x5 bins) | "
                 f"{'PASS' if sanity['gate1_ok'] else 'FAIL'} |")
    lines.append(f"| 2 | stress median in {list(GATE2_STRESS_MEDIAN_RANGE)} | "
                 f"{'PASS' if sanity['gate2_ok'] else 'FAIL'} |")
    lines.append(f"| 3 | gevoelscore median in {list(GATE3_GEVOELSCORE_MEDIAN_RANGE)} | "
                 f"{'PASS' if sanity['gate3_ok'] else 'FAIL'} |")
    lines.append(f"| 4 | all 5 bins n>=30 AND total n>={MIN_TOTAL_N} | "
                 f"{'PASS' if sanity['gate4_ok'] else 'FAIL'} |")
    g5_sha = sanity['gate5_sha_ok']
    g5_bnd = sanity['gate5_boundary_ok']
    g5_sha_str = 'PASS' if g5_sha else ('FAIL' if g5_sha is False else 'NA')
    g5_bnd_str = 'PASS' if g5_bnd else ('FAIL' if g5_bnd is False else 'NA')
    lines.append(f"| 5 (SHA) | snapshot SHA-256 matches `d0ff9253` | {g5_sha_str} |")
    lines.append(f"| 5 (boundaries) | quintile boundary shift <= 1 stress-unit | "
                 f"{g5_bnd_str} |")
    lines.append("")
    if sanity['gate5_observed_boundaries'] is not None:
        lines.append(f"**Gate 5 recomputed boundaries** (q=0.2,0.4,0.6,0.8 on "
                     f"the full Stratum 4 pool): "
                     f"{sanity['gate5_observed_boundaries']}; "
                     f"locked = {list(EXPECTED_QUINTILE_BOUNDARIES)}.")
        lines.append("")
    if halt:
        lines.extend([
            "## HALT-eligible failures",
            "",
        ])
        for f in sanity["fails"]:
            lines.append(f"- **Gate {f['gate']}** ({f['name']}): {f['detail']}")
        lines.extend([
            "",
            ("Per LOCKED r2 section 10.4 step 1 + `hypothesis_lock_process.md` "
             "section 3.9: the full test is **HALTed** on any gate failure. "
             "HA-C3p has NO halt-option-A pre-commit (equal-N quintile design "
             "eliminates structurally-absent-bin failure mode). Any spec "
             "revision creates HA-C3p-v2 with r2 archived per spec section 7.3."),
            "",
        ])
    else:
        lines.append("**DRY-RUN VERDICT: PASS** - proceed with full run.")
        lines.append("")
    OUT_DRYRUN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {OUT_DRYRUN_MD}", file=sys.stderr)


# === Full run (spec section 10.4 step 2) ===============================

def run_full(master: dict, baseline_cutoff: date | None,
             sanity: dict, snapshot_sha: str) -> dict:
    rng = np.random.default_rng(RANDOM_SEED)
    pool = sanity["pool"]
    pool_s4 = sanity["pool_stratum4"]
    print("\n=== HA-C3p r2 full run ===", file=sys.stderr)
    print(f"  unmedicated pool n = {pool['n']}", file=sys.stderr)
    print(f"  full Stratum 4 pool n = {pool_s4['n']}", file=sys.stderr)

    # --- Primary 3-condition tests (spec section 4.5.1) ---
    print("\n  primary 3-condition block-permutation tests (B=10,000)...",
          file=sys.stderr)
    perm = block_permutation_three_conditions(pool, B_HEADLINE, BOOTSTRAP_E_L, rng)
    F_continuous, spline_sd = _spline_F_and_secderiv(pool)
    print(f"    J* = {perm['obs']['J_star']}", file=sys.stderr)
    print(f"    S  = {perm['obs']['S']}", file=sys.stderr)
    print(f"    spline F (continuous) = {F_continuous}", file=sys.stderr)
    print(f"    spline 2nd-deriv at midpoints (29.5,32.5,35.5,68.5): "
          f"{[f'{x:.4f}' for x in spline_sd]}", file=sys.stderr)
    print(f"    p_a = {perm['p_values']['p_a_jonckheere_decreasing']:.4f}",
          file=sys.stderr)
    print(f"    p_b = {perm['p_values']['p_b_S_convex']:.4f}", file=sys.stderr)
    print(f"    p_c = {perm['p_values']['p_c_spline_nonlinearity']:.4f}",
          file=sys.stderr)

    # --- 3-condition verdict ---
    verdict = verdict_three_condition(perm, spline_sd)
    print(f"\n  3-condition verdict: {verdict['verdict_label']}", file=sys.stderr)

    # --- secondary descriptive (spec section 4.5.2) ---
    print("\n  secondary descriptive outcomes...", file=sys.stderr)
    bin_ci = stationary_bootstrap_ci_bin_means(
        pool, B=1000, expected_block_length=BOOTSTRAP_E_L, rng=rng)
    pairs = mann_whitney_pairwise(pool)
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

    # --- spec section 5.B dose-adjusted cross-phase sensitivity (spec section 4.4) ---
    print("\n  spec section 5.B dose-adjusted cross-phase sensitivity arm...",
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

    # --- Crash-drop sensitivity (spec section 4.6) ---
    print("\n  spec section 4.6 crash-drop sensitivity...", file=sys.stderr)
    pool_no_crash = build_pool(master, baseline_cutoff, phase="unmedicated",
                                drop_crashes=True)
    means_full = _means_per_bin(pool["gevoelscore"], pool["bin"])
    means_nocr = _means_per_bin(pool_no_crash["gevoelscore"], pool_no_crash["bin"])
    S_full = second_diff_S(means_full)
    S_nocr = second_diff_S(means_nocr)
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

    # --- Train/validate M3 overlay (spec section 4.8) ---
    print("\n  spec section 4.8 train/validate M3 descriptive overlay...",
          file=sys.stderr)
    train_mask = pool["dates"] <= np.datetime64(TRAIN_END)
    validate_mask = (~train_mask)
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

    # --- t+1 lagged variant (spec section 4.8) ---
    print("\n  spec section 4.8 t+1 lagged variant...", file=sys.stderr)
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

    # --- z-scored sensitivity at 28d-lagged baseline (spec section 4.8(b)) ---
    print("\n  spec section 4.8(b) z-scored vs 28d-lagged baseline sensitivity arm...",
          file=sys.stderr)
    pool_z = build_zscore_pool(master, baseline_cutoff, phase="unmedicated")
    zscore_arm = None
    if pool_z is None or pool_z["n"] < MIN_TOTAL_N:
        zscore_arm = {
            "n": (pool_z["n"] if pool_z is not None else 0),
            "verdict": "NA",
            "verdict_label": "INCONCLUSIVE (z-score pool too small or could not be built)",
        }
    else:
        z_bin_n = [int((pool_z["bin"] == b).sum()) for b in range(5)]
        n_at_least_30_z = sum(1 for b in range(5) if z_bin_n[b] >= MIN_BIN_N)
        if n_at_least_30_z < 5:
            zscore_arm = {
                "n": pool_z["n"],
                "bin_n": z_bin_n,
                "z_quintile_edges": pool_z["z_quintile_edges"],
                "verdict": "NA",
                "verdict_label": f"INCONCLUSIVE ({n_at_least_30_z}/5 bins n>=30)",
            }
        else:
            perm_z = block_permutation_three_conditions(
                pool_z, B_HEADLINE, BOOTSTRAP_E_L, rng)
            F_z, sd_z = _spline_F_and_secderiv(pool_z)
            verdict_z = verdict_three_condition(perm_z, sd_z)
            z_means = _means_per_bin(pool_z["gevoelscore"], pool_z["bin"])
            zscore_arm = {
                "n": pool_z["n"],
                "bin_n": z_bin_n,
                "z_quintile_edges": pool_z["z_quintile_edges"],
                "bin_mean": [None if math.isnan(m) else float(m) for m in z_means],
                "verdict": verdict_z["verdict"],
                "verdict_label": verdict_z["verdict_label"],
                "p_a": verdict_z["p_a"],
                "p_b": verdict_z["p_b"],
                "p_c": verdict_z["p_c"],
                "S": (None if perm_z["obs"]["S"] is None
                      else float(perm_z["obs"]["S"])),
                "J_star": (None if perm_z["obs"]["J_star"] is None
                           else float(perm_z["obs"]["J_star"])),
                "spline_F": (None if F_z is None or math.isnan(F_z) else float(F_z)),
                "spline_secderiv": [
                    None if math.isnan(x) else float(x) for x in sd_z
                ],
            }
            print(f"    z-arm verdict: {verdict_z['verdict_label']}",
                  file=sys.stderr)

    # --- spec section 4.7 E[L]* checks (linear-residual + bin-label) ---
    print("\n  spec section 4.7 E[L]* checks (linear-residual + bin-label)...",
          file=sys.stderr)
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
        "snapshot_sha": snapshot_sha,
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
            "SPLINE_INTERNAL_KNOTS": SPLINE_INTERNAL_KNOTS,
            "COMPANION_CONTRAST": COMPANION_CONTRAST.tolist(),
            "EXPECTED_SNAPSHOT_SHA": EXPECTED_SNAPSHOT_SHA,
            "EXPECTED_QUINTILE_BOUNDARIES": list(EXPECTED_QUINTILE_BOUNDARIES),
        },
        "primary": {
            "pool_n": pool["n"],
            "bin_n": [int((pool["bin"] == b).sum()) for b in range(5)],
            "bin_mean": [None if math.isnan(m) else float(m)
                         for m in _means_per_bin(g, pool["bin"])],
            "bin_ci_95": bin_ci,
            "perm": perm,
            "spline_continuous_F": (float(F_continuous)
                                    if not math.isnan(F_continuous) else None),
            "spline_second_derivative_at_midpoints": [
                None if math.isnan(x) else float(x) for x in spline_sd
            ],
            "verdict": verdict,
            "pairwise_mann_whitney": pairs,
            "spearman_rho": rho,
        },
        "full_stratum4": {
            "pool_n": pool_s4["n"],
            "bin_n": [int((pool_s4["bin"] == b).sum()) for b in range(5)],
            "bin_mean": [None if math.isnan(m) else float(m)
                         for m in _means_per_bin(pool_s4["gevoelscore"], pool_s4["bin"])],
        },
        "sensitivity_5B": {
            "pool_n": pool_5B["n"],
            "bin_n": [int((pool_5B["bin"] == b).sum()) for b in range(5)],
            "bin_mean": [None if math.isnan(m) else float(m)
                         for m in _means_per_bin(pool_5B["gevoelscore"], pool_5B["bin"])],
            "perm": perm_5B,
            "verdict": verdict_5B,
        },
        "sensitivity_crash_drop": crash_drop,
        "sensitivity_train_validate_overlay": overlay,
        "sensitivity_lagged_t_plus_1": lagged,
        "sensitivity_zscore_28d_lagged": zscore_arm,
        "el_star": el_star,
        "sanity": {
            "bin_n": sanity["bin_n"],
            "bin_mean": sanity["bin_mean"],
            "bin_median": sanity.get("bin_median", [None] * len(sanity["bin_n"])),
            "stress_median": sanity["stress_median"],
            "gevoelscore_median": sanity["gevoelscore_median"],
            "total_n": sanity["total_n"],
            "verdict": sanity["verdict"],
            "fails": sanity["fails"],
            "gate5_observed_sha": sanity["gate5_observed_sha"],
            "gate5_observed_boundaries": sanity["gate5_observed_boundaries"],
            "gate5_sha_ok": sanity["gate5_sha_ok"],
            "gate5_boundary_ok": sanity["gate5_boundary_ok"],
        },
    }


def write_result_md(results: dict, halted: bool, halt_detail: str = "") -> None:
    """Write result.md per spec section 10.3 template."""
    if halted:
        verdict_str = "HALT (sanity gate failure)"
    else:
        v = results["primary"]["verdict"]
        verdict_str = v["verdict_label"]
    lines: list[str] = []

    # --- Title + Authorship ---
    lines.append(f"# HA-C3p r2 RESULT: {verdict_str}")
    lines.append("")
    lines.append("## Authorship")
    lines.append("")
    lines.append(
        f"Drafted 2026-06-23 by Claude (Opus 4.7, 1M context) in producer-mode "
        f"under user authorisation per "
        f"[CONVENTIONS section 1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default). "
        f"Authorising user: Willem. Pre-reg r2 LOCKED 2026-06-23 at commit "
        f"`{R2_SPEC_COMMIT}`. Test commit: `(this-commit)`. Status: "
        f"**LANDED**.")
    lines.append("")
    lines.append(
        "**Test-session context**: this `test.py` was implemented and run "
        "in a FRESH Claude session per the post-lock discipline of "
        "[`hypothesis_lock_process.md` section 3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock). "
        "Sister-session note: HA-C3 v2 r2 test execution runs in parallel; "
        "section 6 4-cell agreement matrix populates HA-C3p's column only; "
        "HA-C3 v2's column is marked TBD (dispatcher consolidates).")
    lines.append("")
    if halted:
        lines.append(
            "**HALT outcome**: the section 7.5 dry-run sanity gates failed "
            "at the configuration pre-committed at r2 lock. Per section 3.9 "
            "dry-run halt discipline + the locked r2 spec, the full test was "
            "**NOT** executed beyond the dry-run.")
        lines.append("")

    # --- Section 1 What was tested ---
    lines.append("## Section 1 - What was tested")
    lines.append("")
    bins_str = ", ".join(BIN_LABELS)
    lines.append(
        "**Headline cell** (per pre-reg section 1 + section 5.0): unmedicated "
        "(full LC era through 2024-04-08) x full Stratum 4 single pool x "
        f"`all_day_stress_avg` binned at equal-N quintile bins {{{bins_str}}} x "
        "`gevoelscore` bin-mean x {Jonckheere-Terpstra monotone-decreasing + "
        "second-difference convexity contrast S = mean(D2_2, D2_3, D2_4) + "
        "spline non-linearity with 4 internal knots at quintile boundaries} x "
        "block-permutation null at E[L]=7 x 3-condition gated verdict per "
        "section 5.1.")
    lines.append("")
    lines.append(
        "**Substantive question** (per pre-reg section 2(a) Wiggers source + "
        "section 1 sister-pre-reg framing): does the underlying convex "
        "stress -> fatigue shape Wiggers describes (PDF lines 1357-1368, "
        "Annual Stress Scores, 'stair-step' qualitative reading) fire on the "
        "participant's **personal-baseline-anchored quintile bins** per "
        "[CONVENTIONS section 3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds), "
        "rather than at Wiggers' verbatim 30 -> 40 numerical anchor (HA-C3 "
        "v2 carries that operationalisation)? The user's framing per the "
        "session handoff: HA-C3 v2 stays honest against the original Wiggers "
        "document; **HA-C3p goes further to see if we can find the mechanism "
        "Wiggers is describing besides the numbers she uses**.")
    lines.append("")
    lines.append("**3-condition gated verdict per section 5.1**:")
    lines.append("")
    lines.append("| outcome | condition status | verdict |")
    lines.append("|---|---|---|")
    lines.append("| (a) MET AND (b) MET AND (c) MET | 3-of-3 | **SUPPORTED** |")
    lines.append("| Exactly 2-of-3 MET | 2-of-3 | **PARTIAL** |")
    lines.append("| <=1-of-3 MET | 0/1-of-3 | **REJECTED** |")
    lines.append("| Any wrong-direction firing | override | **REJECTED** |")
    lines.append("")

    # --- Section 2 Data + descriptives ---
    lines.append("## Section 2 - Data + descriptives")
    lines.append("")
    s_med = results["sanity"]["stress_median"]
    g_med = results["sanity"]["gevoelscore_median"]
    lines.append(f"Primary unmedicated pool: n = **{results['sanity']['total_n']}**. "
                 f"Stress median: **{s_med:.2f}**. Gevoelscore median: "
                 f"**{g_med:.2f}**.")
    if not halted:
        lines.append(f"Full Stratum 4 pool (for cross-arm bin-edge cleanliness): "
                     f"n = {results['full_stratum4']['pool_n']}.")
    lines.append("")
    lines.append("### Unmedicated per-bin distribution")
    lines.append("")
    lines.append("| bin | label | n | bin-mean gevoelscore | bin-median |")
    lines.append("|---|---|---:|---:|---:|")
    for b in range(5):
        m = results["sanity"]["bin_mean"][b]
        md = results["sanity"]["bin_median"][b]
        lines.append(
            f"| Q{b+1} | {BIN_LABELS[b]} | {results['sanity']['bin_n'][b]} | "
            f"{f'{m:.3f}' if m is not None else 'NA'} | "
            f"{f'{md:.2f}' if md is not None else 'NA'} |")
    lines.append("")

    if not halted:
        # Full Stratum 4 distribution
        lines.append("### Full Stratum 4 per-bin distribution (descriptive)")
        lines.append("")
        lines.append("| bin | label | n | bin-mean gevoelscore |")
        lines.append("|---|---|---:|---:|")
        for b in range(5):
            n_b = results["full_stratum4"]["bin_n"][b]
            m_b = results["full_stratum4"]["bin_mean"][b]
            lines.append(
                f"| Q{b+1} | {BIN_LABELS[b]} | {n_b} | "
                f"{f'{m_b:.3f}' if m_b is not None else 'NA'} |")
        lines.append("")

        # Right-shift unmed bin observation per section 8 caveat 4
        un_bin_n = results["sanity"]["bin_n"]
        s4_bin_n = results["full_stratum4"]["bin_n"]
        un_total = sum(un_bin_n)
        s4_total = sum(s4_bin_n)
        un_pct_q1 = 100.0 * un_bin_n[0] / un_total if un_total > 0 else 0.0
        s4_pct_q1 = 100.0 * s4_bin_n[0] / s4_total if s4_total > 0 else 0.0
        un_pct_q5 = 100.0 * un_bin_n[4] / un_total if un_total > 0 else 0.0
        s4_pct_q5 = 100.0 * s4_bin_n[4] / s4_total if s4_total > 0 else 0.0
        lines.append("### Right-shift unmedicated bin observation (per spec section 8 caveat 4)")
        lines.append("")
        lines.append(
            f"The unmedicated stratum is **right-shifted** relative to the "
            f"full Stratum 4 pool: unmedicated [Q1={un_bin_n[0]}, Q2={un_bin_n[1]}, "
            f"Q3={un_bin_n[2]}, Q4={un_bin_n[3]}, Q5={un_bin_n[4]}] vs full-pool "
            f"[Q1={s4_bin_n[0]}, Q2={s4_bin_n[1]}, Q3={s4_bin_n[2]}, Q4={s4_bin_n[3]}, "
            f"Q5={s4_bin_n[4]}]. "
            f"Q1 share: {un_pct_q1:.1f}% (unmed) vs {s4_pct_q1:.1f}% (full pool); "
            f"Q5 share: {un_pct_q5:.1f}% (unmed) vs {s4_pct_q5:.1f}% (full pool). "
            "The unmedicated pool concentrates mass at higher quintiles relative "
            "to the full Stratum 4 pool. This is **consistent with citalopram's "
            "CONFIRMED +0.57/mg `all_day_stress_avg` beta per "
            "[`citalopram_dose_response_stress_mean_sleep.md` section 5.6.1]"
            "(../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read)**: "
            "medication (consolidation + afbouw phases of Stratum 4) compresses "
            "the stress range; unmedicated days populate the higher quintiles "
            "disproportionately. This is a **substantive cross-test validation "
            "of the recalibration finding at a different operationalisation** "
            "(bin distribution rather than mean beta).")
        lines.append("")

    # --- Section 3 Primary test result ---
    lines.append("## Section 3 - Primary test result")
    lines.append("")
    if halted:
        lines.append(
            "**HALT**: primary test was not executed because the section 7.5 "
            "sanity gates failed at the pre-committed bin specification.")
        lines.append("")
        lines.append(f"**Halt detail (machine-readable)**: {halt_detail}")
        lines.append("")
    else:
        p = results["primary"]["perm"]
        v = results["primary"]["verdict"]
        obs = p["obs"]
        lines.append(f"Per pre-reg section 4.5.1 + section 4.7 block-permutation "
                     f"at E[L]=7 (B = {B_HEADLINE} draws, seed = {RANDOM_SEED}).")
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
            f"| (b) Second-difference convexity | S = mean(D2_2, D2_3, D2_4) | "
            f"{obs['S']:+.4f} | {v['p_b']:.4f} | "
            f"{'YES (S<0)' if v['b_direction_ok'] else 'NO (S>=0)'} | "
            f"{'PASS' if v['p_b'] < P_BAR else 'fail'} | "
            f"{'PASS' if v['b_met'] else 'fail'} |")
        f_str = (f"{obs['spline_F_continuous_predictor']:+.4f}"
                 if obs.get('spline_F_continuous_predictor') is not None else 'NA')
        lines.append(
            f"| (c) Spline non-linearity (block-permutation) | F (continuous predictor) | "
            f"{f_str} | "
            f"{v['p_c']:.4f} | "
            f"{'YES' if v['c_direction_ok'] else 'NO'} ({v['spline_neg_count']} of "
            f"{v['spline_total_midpoints']} midpoints negative) | "
            f"{'PASS' if v['p_c'] < P_BAR else 'fail'} | "
            f"{'PASS' if v['c_met'] else 'fail'} |")
        lines.append(
            f"| (d) Companion orthogonal quadratic (descriptive) | c.m, c=(+2,-1,-2,-1,+2) | "
            f"{obs['companion_contrast']:+.4f} | "
            f"{p['p_values']['p_companion_orthogonal_quadratic']:.4f} | n/a | n/a | n/a |")
        lines.append("")
        lines.append(f"**Aggregate 3-condition verdict: {v['verdict_label']}**")
        if v["wrong_direction_fired"]:
            lines.append("")
            lines.append("**Wrong-direction overrides** fired:")
            for n in v["wrong_direction_notes"]:
                lines.append(f"- {n}")
        pf = p["parametric_F_descriptive"]
        lines.append("")
        lines.append(
            f"*Spline parametric F (descriptive only per pre-reg section 4.5.1(c)): "
            f"F = {pf['F'] if pf['F'] is not None else 'NA'}, "
            f"parametric p = {pf['p_parametric'] if pf['p_parametric'] is not None else 'NA'}.*")
        lines.append("")
        lines.append("**Bin-means (primary, unmedicated)**:")
        lines.append("")
        lines.append("| bin | n | mean | 95% CI (stationary bootstrap E[L]=7, B=1000) |")
        lines.append("|---|---:|---:|---|")
        for b in range(5):
            n_b = results["primary"]["bin_n"][b]
            m_b = results["primary"]["bin_mean"][b]
            ci_lo, ci_hi = results["primary"]["bin_ci_95"].get(f"Q{b+1}", (None, None))
            ci_str = (f"[{ci_lo:.3f}, {ci_hi:.3f}]" if (ci_lo is not None and ci_hi is not None)
                      else "NA")
            lines.append(f"| Q{b+1} | {n_b} | "
                         f"{f'{m_b:.3f}' if m_b is not None else 'NA'} | "
                         f"{ci_str} |")
        lines.append("")
        # Pairwise Mann-Whitney + Holm
        lines.append("**Pairwise adjacent-bin Mann-Whitney + Holm step-down (per spec section 4.5.2 + section 5.1 PARTIAL-band multiplicity disclosure)**:")
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
        sr = results["primary"]["spearman_rho"]
        lines.append(
            f"**Sanity-check companion Spearman rho** (the *opposing-model* "
            f"linear test per section 4.5.2): rho = "
            f"{sr['rho']:.4f} (p = {sr['p']:.4g}, n = {sr['n']}).")
        lines.append("")

    # --- Section 4 Sensitivity arms ---
    lines.append("## Section 4 - Sensitivity arms (descriptive, no verdict weight)")
    lines.append("")
    if halted:
        lines.append("Sensitivity arms not executed because the primary test halted "
                     "on section 7.5 sanity gates.")
        lines.append("")
    else:
        # 5.B
        s5B = results["sensitivity_5B"]
        v5B = s5B["verdict"]
        lines.append(f"### Section 5.B - cross-phase dose-adjusted (predictor - "
                     f"{DOSE_BETA_PER_MG}/mg x dose_plasma_mg; REUSES locked quintile boundaries)")
        lines.append("")
        lines.append(f"- Pool n = {s5B['pool_n']}; bin-n = {s5B['bin_n']}; "
                     f"bin-mean = {s5B['bin_mean']}.")
        lines.append(f"- Verdict (descriptive, NOT promoted): "
                     f"**{v5B.get('verdict_label', 'NA')}**.")
        lines.append("")
        # z-scored at 28d-lagged
        zarm = results["sensitivity_zscore_28d_lagged"]
        lines.append("### z-scored vs 28d-lagged baseline (per Locked decision 2 + CONVENTIONS section 3.1)")
        lines.append("")
        if zarm.get("bin_n") is not None:
            lines.append(f"- Pool n = {zarm['n']}; bin-n = {zarm['bin_n']}.")
            if zarm.get("z_quintile_edges") is not None:
                lines.append(f"- z-score quintile edges (q=0.2,0.4,0.6,0.8): "
                             f"{[round(x, 3) for x in zarm['z_quintile_edges'][1:5]]}.")
            if zarm.get("bin_mean") is not None:
                lines.append(f"- bin-mean = {zarm['bin_mean']}.")
            if zarm.get("S") is not None:
                lines.append(f"- S = {zarm['S']:+.4f}; J* = "
                             f"{zarm['J_star']:+.4f}; "
                             f"p_a={zarm['p_a']:.4f}, p_b={zarm['p_b']:.4f}, "
                             f"p_c={zarm['p_c']:.4f}.")
        else:
            lines.append(f"- Pool n = {zarm['n']}.")
        lines.append(f"- Verdict (descriptive, NOT promoted): "
                     f"**{zarm.get('verdict_label', 'NA')}**.")
        lines.append("")
        # Crash-drop
        cd = results["sensitivity_crash_drop"]
        lines.append("### Crash-drop sensitivity (CONVENTIONS section 3.4)")
        lines.append("")
        s_full_str = f"{cd['S_full']:+.4f}" if cd["S_full"] is not None else "NA"
        s_nocr_str = f"{cd['S_no_crash']:+.4f}" if cd["S_no_crash"] is not None else "NA"
        d_std_str = (f"{cd['delta_standardised']:.4f}"
                     if cd["delta_standardised"] is not None else "NA")
        lines.append(f"- S (full) = {s_full_str} (n = {cd['n_full']}); "
                     f"S (no-crash) = {s_nocr_str} (n = {cd['n_no_crash']}).")
        lines.append(f"- |Delta S| standardised = {d_std_str}; "
                     f"sign-change = {cd['sign_change']}; flag = "
                     f"{'**FLAG**' if cd['flag'] else 'ok'}.")
        lines.append("")
        # Train/validate
        ov = results["sensitivity_train_validate_overlay"]
        lines.append("### Train/validate M3 descriptive overlay (per `train_validate_split_fate.md` section 5)")
        lines.append("")
        lines.append(f"- Train (<= 2023-12-31): n = {ov['train_n']}; "
                     f"bin-n = {ov['train_bin_n']}; bin-mean = {ov['train_bin_mean']}; "
                     f"S = {ov['train_S']}.")
        lines.append(f"- Validate (2024-01-01 -> 2024-04-08): n = {ov['validate_n']}; "
                     f"bin-n = {ov['validate_bin_n']}; bin-mean = {ov['validate_bin_mean']}; "
                     f"S = {ov['validate_S']}.")
        lines.append("- Per `train_validate_split_fate.md` section 5: divergence is a number, "
                     "not a narrative; no per-era verdicts.")
        lines.append("")
        # Lagged
        lg = results["sensitivity_lagged_t_plus_1"]
        lines.append("### t+1 lagged variant (gevoelscore[T+1] on stress[T])")
        lines.append("")
        lines.append(f"- n = {lg['n']}; bin-n = {lg['bin_n']}; bin-mean = {lg['bin_mean']}; "
                     f"S = {lg['S']}.")
        lines.append("")

    # --- Section 5 Bin-by-bin descriptive ---
    lines.append("## Section 5 - Bin-by-bin descriptive characterisation")
    lines.append("")
    if halted:
        means = results["sanity"]["bin_mean"]
        ns = results["sanity"]["bin_n"]
        lines.append(
            "Per pre-reg section 10.3, the bin-by-bin descriptive characterisation "
            "is reported even on halt:")
        lines.append("")
        lines.append("| bin | n | bin-mean gevoelscore | adjacent step (low - this) |")
        lines.append("|---|---:|---:|---:|")
        prev = None
        for b in range(5):
            m = means[b]
            n_b = ns[b]
            if prev is None or m is None:
                step_str = "--"
            else:
                step_str = f"{prev - m:+.3f}"
            m_str = f"{m:.3f}" if m is not None else "NA"
            lines.append(f"| Q{b+1} | {n_b} | {m_str} | {step_str} |")
            prev = m
        lines.append("")
    else:
        means = results["primary"]["bin_mean"]
        lines.append("Adjacent-bin step magnitudes (positive = bin-mean DROP from low -> high):")
        lines.append("")
        lines.append("| step | bin pair | magnitude (m_low - m_high) |")
        lines.append("|---|---|---:|")
        for i in range(4):
            mi, mj = means[i], means[i + 1]
            if mi is None or mj is None:
                step_str = "NA"
            else:
                step_str = f"{mi - mj:+.3f}"
            lines.append(f"| {i+1} | Q{i+1}-Q{i+2} | {step_str} |")
        lines.append("")
        lines.append(
            "Per pre-reg section 7.1 SUPPORTED expectation: monotone decreasing "
            "(positive steps); accelerating decrement (Q4 -> Q5 step LARGEST in "
            "magnitude because Q5 has width 63 vs Q2-Q4 widths 3).")
        lines.append("")

    # --- Section 6 - 4-cell agreement matrix with HA-C3 v2 ---
    lines.append("## Section 6 - Cross-test reading: 4-cell agreement matrix with HA-C3 v2")
    lines.append("")
    lines.append(
        "Per pre-reg Locked decision 5 + section 1 sister-pre-reg framing, "
        "HA-C3p's result.md section 6 carries the 4-cell agreement-matrix "
        "interpretation with HA-C3 v2 (Wiggers-verbatim sister test). HA-C3 "
        "v2 r2 test execution runs in **parallel** with this HA-C3p session; "
        "its verdict is **TBD** at this result-emission time. The dispatcher "
        "consolidates the matrix in a follow-up commit after both sessions return.")
    lines.append("")
    if halted:
        hac3p_v_label = "HALT (sanity-gate failure)"
    else:
        hac3p_v_label = results["primary"]["verdict"]["verdict"]
    lines.append("### 4-cell matrix (HA-C3p column populated; HA-C3 v2 column TBD)")
    lines.append("")
    lines.append("| HA-C3 v2 (Wiggers) v / HA-C3p (personal) > | SUPPORTED | REJECTED |")
    lines.append("|---|---|---|")
    lines.append(
        "| SUPPORTED | strong (both agree on convexity) | bin-edge artefact "
        "(v2 anchors happen to fall on a peak HA-C3p smooths) |")
    lines.append(
        "| REJECTED | Wiggers' numbers wrong-for-this-participant but underlying "
        "shape real | informative null (no convexity at either operationalisation) |")
    lines.append("")
    lines.append(
        f"**HA-C3p verdict**: **{hac3p_v_label}**. **HA-C3 v2 axis**: "
        f"**TBD (parallel session pending; dispatcher consolidates)**.")
    lines.append("")
    if not halted and hac3p_v_label == "SUPPORTED":
        lines.append(
            "**HA-C3p column cells under SUPPORTED**: matrix row {SUPPORTED, REJECTED} "
            "x HA-C3p=SUPPORTED. If HA-C3 v2 also SUPPORTED -> 'strong (both "
            "agree on convexity)'. If HA-C3 v2 REJECTED -> 'Wiggers' numbers "
            "wrong-for-this-participant but underlying shape real' (the centerpiece "
            "'mechanism besides numbers' finding per the user's framing in the "
            "session handoff section 1).")
    elif not halted and hac3p_v_label == "REJECTED":
        lines.append(
            "**HA-C3p column cells under REJECTED**: matrix row {SUPPORTED, REJECTED} "
            "x HA-C3p=REJECTED. If HA-C3 v2 SUPPORTED -> 'bin-edge artefact "
            "(v2 anchors happen to fall on a peak HA-C3p smooths)'. If HA-C3 "
            "v2 also REJECTED -> 'informative null (no convexity at either "
            "operationalisation)'.")
    elif not halted and hac3p_v_label == "PARTIAL":
        lines.append(
            "**HA-C3p column under PARTIAL** (note: matrix shown above is 2x2 "
            "SUPPORTED/REJECTED; PARTIAL is the intermediate state). The "
            "PARTIAL verdict is 2-of-3 conditions MET; downstream interpretation "
            "follows pre-reg section 9.2's three operationally-distinguishable "
            "PARTIAL configurations. Cross-test reading: PARTIAL is interpreted "
            "as 'evidence of some convex structure but not the full 3-condition "
            "headline'; the HA-C3 v2 cross-test consolidation will frame the "
            "PARTIAL-vs-v2-verdict reading at dispatcher-consolidation time.")
    lines.append("")

    # Sister-test cross-reference table
    lines.append("### Sister-test cross-reference table")
    lines.append("")
    lines.append("| pre-reg | verdict | venue | cited per |")
    lines.append("|---|---|---|---|")
    lines.append("| **HA-C3p (this test)** | **" + hac3p_v_label + "** | "
                 "personal-baseline quintile bins | pre-reg section 5.1 |")
    lines.append("| HA-C3 v2 r2 (Wiggers-verbatim sister; running in parallel) | "
                 "**PENDING** (parallel session) | bins [0,30), [30,40), [40,60), [60,100] | "
                 "pre-reg section 1 sister-test framing; dispatcher consolidates |")
    lines.append("| HA-C4 v2 (daily-aggregate recovery-dynamics triad) | "
                 "REJECTED at triad sum 0/3 | commit `52bddb5` 2026-06-18 | "
                 "structurally distinct (recovery dynamics, not same-day shape) |")
    lines.append("| HA-C4c (bout-level cross-phase) | PARTIAL (bar (b) effect-size "
                 "failing; bar (a) PASS p=0.0001, delta=+0.120 at "
                 "n_heavy=465/n_non=809) | commit `a69a8ed` 2026-06-23 | "
                 "structurally distinct (bout-level, not bin-shape) |")
    lines.append("| HA-P6 v3 (post-crash autonomic recovery shape) | "
                 "noisy-inconclusive / mixed per-channel | 2026-06-17 | "
                 "structurally distinct (event-anchored recovery, not cross-day shape) |")
    lines.append("| HA11 v1 (within-day stress U-dip count) | SUPPORTED on train, "
                 "REFUTED on validate (overall REFUTED) | committed in HA11-stress-udip | "
                 "structurally distinct (within-day pattern, not cross-day shape) |")
    lines.append("")

    # --- Section 7 E[L]* report ---
    lines.append("## Section 7 - Section 4.7 E[L]* report (factor-of-2 flag)")
    lines.append("")
    if halted:
        lines.append("Not run (primary halted).")
        lines.append("")
    else:
        el = results["el_star"]
        lines.append("Per pre-reg section 4.7: two data-driven E[L]* checks "
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
        v_v = results["primary"]["verdict"]["verdict"]
        if any_flag and v_v == "SUPPORTED":
            lines.append("**Flag fires on verdict-relevant cell** (verdict is SUPPORTED). "
                         "Per `permutation_null_block_length.md` the flag suggests the E[L]=7 "
                         "default may be mis-calibrated; report as caveat.")
        elif any_flag:
            lines.append("Flag fires but verdict is not SUPPORTED; descriptive context only "
                         "per `permutation_null_block_length.md`.")
        else:
            lines.append("No flags.")
        lines.append("")

    # --- Section 8 Caveats ---
    lines.append("## Section 8 - Caveats (per pre-reg section 8)")
    lines.append("")
    lines.append(
        "1. **Power-calc dispatch**: power calculation is **inapplicable per "
        "Daza 2018** within-subject n-of-1 design. Block-permutation null at "
        "E[L]=7 is the within-subject inferential machinery; the 3-condition "
        "gated verdict is the decision rule. Equal-N quintile-bin design "
        "eliminates structural-underpower from the bin-design dimension.")
    lines.append(
        "2. **Sister-pre-reg framing**: HA-C3p tests the underlying convex-shape "
        "claim Wiggers describes on **personal-baseline-anchored bins** per "
        "CONVENTIONS section 3.1; HA-C3 v2 tests Wiggers' verbatim 30->40 "
        "numerical anchor. The 4-cell agreement matrix lives in section 6 "
        "above (HA-C3 v2 axis TBD pending parallel-session consolidation).")
    lines.append(
        "3. **CONVENTIONS section 3.1 personal-baseline framing**: HA-C3p's "
        "quintile bins are pool-anchored (equal-N quintiles on the full "
        "Stratum 4 distribution at the locked draft-time snapshot). The "
        "z-scored-against-personal-rolling-baseline variant is reported as "
        "the section 4.8(b) sensitivity arm; raw quintiles are primary because "
        "the rolling-baseline z-score has edges that drift in raw stress-units "
        "over time, complicating cross-arm bin-edge cleanliness.")
    lines.append(
        f"4. **Citalopram-channel inheritance** (load-bearing for the right-shift "
        f"unmedicated bin observation surfaced in section 2): `all_day_stress_avg` "
        f"is CONFIRMED dose-modulated at +{DOSE_BETA_PER_MG}/mg per "
        f"`citalopram_dose_response_stress_mean_sleep.md` section 5.6.1. "
        f"The unmedicated stratum's right-shifted bin distribution (see section 2 "
        f"above) is a **cross-test validation of this recalibration finding at "
        f"a different operationalisation** (bin distribution rather than mean beta).")
    lines.append(
        "5. **HA-C3 v1 partial-pool non-monotone observation as caveat-class "
        "prior**: v1's HALT-time partial-pool descriptive trajectory (B2-B3-B4 = "
        "3.958 -> 4.265 -> 3.860, peak at v1 B3 = stress 30-40) was descriptively "
        "non-monotone. Caveat-class prior informing HA-C3p's interpretation; not "
        "promoted to a substantive HA-C3p output. HA-C3p does NOT pre-commit "
        "to an inverted-U / threshold-pattern alternative claim.")
    lines.append(
        "6. **n=1 single-subject** per CONVENTIONS section 3.1: thresholds in "
        "section 5.1 calibrated against the participant's distribution. The "
        "block-permutation null is the within-subject inferential anchor.")
    lines.append(
        "7. **Operational vs mechanistic** per CONVENTIONS section 4.1-4.3: the "
        "convex shape is the operationalised pattern; the 'stress-cost asymmetry' "
        "mechanism Wiggers describes is the substantive interpretation but not "
        "the operational measure. A SUPPORTED verdict means the operationalised "
        "convex-shape pattern fires on the personal-range bins; it does NOT "
        "prove the substantive Wiggers stress-cost-asymmetry mechanism causally.")
    lines.append(
        "8. **Crash-day inclusion structural fragility** (CONVENTIONS section 3.4): "
        "crashes KEPT in primary; section 4.6 crash-drop arm reported in section 4 "
        "above (sign-boundary flag if |Delta S| > 0.10 standardised OR sign-change).")
    lines.append(
        "9. **No causal-direction inference**: test answers 'does the gevoelscore-vs-"
        "stress-quintile mapping have a convex shape?', not 'does stress CAUSE fatigue?'.")
    lines.append(
        "10. **Bin-edge snapshot pinning** (NEW in HA-C3p): the section 4.1 "
        "quintile boundaries are pre-committed at draft time to "
        "`per_day_master.csv` SHA-256 `d0ff9253`. Section 7.5 Gate 5 verifies "
        "the boundaries have not shifted by > 1 stress-unit on the test-time "
        "snapshot. **Gate 5 status at run-time** (see section 9.5 below).")
    lines.append(
        "11. **Independent-obligations block** per `citalopram_phase_stratification "
        "section 6`: autocorrelation (section 4.7) + crash-drop (section 4.6) + "
        "spike-companion (N/A; HA-C3p is cross-day-aggregate) + trajectory-detrend "
        "(N/A; not a pre-vs-post comparison).")
    lines.append(
        "12. **Drafting context disclosure**: the drafter saw the bin boundaries "
        "(28, 31, 34, 37) and per-bin n on both pools at draft time, but NOT the "
        "per-bin gevoelscore means on the quintile-binned distribution. The joint "
        "bin-mean trajectory was the post-lock deferred artefact.")
    lines.append(
        "13. **Wiggers' phrasing is qualitative**: the verbatim 'stair-step' "
        "language is qualitative. HA-C3 v2's (0,30,40,60,100) bins are ONE "
        "operationalisation; HA-C3p's quintile bins are a DIFFERENT operationalisation. "
        "A REJECTED verdict on either does not falsify the qualitative Wiggers "
        "framing universally.")
    lines.append(
        "14. **Sister-test cross-references**: see section 6 cross-reference table above.")
    lines.append("")

    # --- Section 9 Gate results + reproducibility ---
    lines.append("## Section 9 - Section 7.5 gate results + reproducibility")
    lines.append("")
    san = results["sanity"]
    lines.append("### Section 7.5 sanity gates")
    lines.append("")
    lines.append("| gate | description | result |")
    lines.append("|---|---|---|")
    # Hand-derive PASS/FAIL from fails
    gate_fails = {f["gate"]: f for f in san["fails"]}
    lines.append(f"| 1 | per-bin n >= 30 (x5 quintile bins) | "
                 f"{'FAIL' if 1 in gate_fails else 'PASS'} |")
    lines.append(f"| 2 | stress median in [20, 60] | "
                 f"{'FAIL' if 2 in gate_fails else 'PASS'} |")
    lines.append(f"| 3 | gevoelscore median in [3, 6] | "
                 f"{'FAIL' if 3 in gate_fails else 'PASS'} |")
    lines.append(f"| 4 | all 5 bins n>=30 AND total n>=100 | "
                 f"{'FAIL' if 4 in gate_fails else 'PASS'} |")
    g5_sha_str = 'PASS' if san["gate5_sha_ok"] else ('FAIL' if san["gate5_sha_ok"] is False else 'NA')
    g5_bnd_str = 'PASS' if san["gate5_boundary_ok"] else ('FAIL' if san["gate5_boundary_ok"] is False else 'NA')
    lines.append(f"| 5 (SHA) | snapshot SHA-256 matches `d0ff9253` | {g5_sha_str} |")
    lines.append(f"| 5 (bound) | quintile boundary shift <= 1 stress-unit | {g5_bnd_str} |")
    lines.append("")
    lines.append(f"**Gate 5 observed SHA**: `{san['gate5_observed_sha']}`. "
                 f"**Expected SHA**: `{EXPECTED_SNAPSHOT_SHA}`. "
                 f"**Recomputed quintile boundaries**: "
                 f"{san['gate5_observed_boundaries']}. "
                 f"**Locked boundaries**: {list(EXPECTED_QUINTILE_BOUNDARIES)}.")
    lines.append("")
    lines.append("### Reproducibility checklist")
    lines.append("")
    lines.append("- **Script**: `docs/research/analyses/hypotheses/HA-C3p/test.py`")
    lines.append("- **Environment variable**: `GEVOELSCORE_DATA_PATH` "
                 "(default: `C:\\Users\\Gebruiker\\Documents\\gevoelscore-data`)")
    lines.append(f"- **Seed**: `RANDOM_SEED = {RANDOM_SEED}`")
    lines.append(f"- **Bootstrap**: B = {B_HEADLINE} stationary-bootstrap draws "
                 f"per condition; E[L] = {BOOTSTRAP_E_L} (geometric block length)")
    lines.append("- **Regenerate command**: `python docs/research/analyses/hypotheses/HA-C3p/test.py`")
    lines.append("- **Dependencies**: numpy, scipy (for `CubicSpline`, "
                 "`mannwhitneyu`, `spearmanr`, `f.sf`); project utility "
                 "`docs/research/analyses/_utils/inference.py` for "
                 "`compute_data_driven_block_length` + `holm_step_down`.")
    lines.append(f"- **Spec commit**: `{R2_SPEC_COMMIT}` (LOCKED 2026-06-23)")
    lines.append(f"- **Snapshot SHA-256 at run-time**: `{san['gate5_observed_sha']}`")
    lines.append("- **Machine-readable companion**: `result-data.json` "
                 "(gitignored per `docs/research/**/*.json`)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        f"*test.py run with `RANDOM_SEED = {RANDOM_SEED}`, "
        f"`BOOTSTRAP_E_L = {BOOTSTRAP_E_L}`, B = {B_HEADLINE} draws per condition. "
        f"Source: `per_day_master.csv` from `$GEVOELSCORE_DATA_PATH`. "
        f"Spec commit: `{R2_SPEC_COMMIT}`. Snapshot SHA-256: "
        f"`{san['gate5_observed_sha']}`.*")
    OUT_RESULT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {OUT_RESULT_MD}", file=sys.stderr)


def write_result_json(results: dict) -> None:
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
    OUT_RESULT_JSON.write_text(
        json.dumps(jsonify(results), indent=2), encoding="utf-8")
    print(f"Wrote {OUT_RESULT_JSON}", file=sys.stderr)


# === main ==============================================================

def main() -> None:
    parser = argparse.ArgumentParser(description="HA-C3p r2 test driver.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run section 10.4 step 1 dry-run only.")
    args = parser.parse_args()

    print(f"Loading master from {MASTER_CSV}...", file=sys.stderr)
    snapshot_sha = sha256_path(MASTER_CSV)
    master = load_master()
    print(f"  {len(master)} day-rows loaded.", file=sys.stderr)
    baseline_cutoff = find_device_baseline_cutoff(master)

    sanity = dry_run(master, baseline_cutoff, snapshot_sha)
    write_dry_run_report(sanity)

    if args.dry_run:
        sys.exit(1 if sanity["verdict"] == "HALT" else 0)

    if sanity["verdict"] == "HALT":
        # Halt without optA: HA-C3p has no halt-option-A pre-commit
        halt_detail = "Sanity gates failed: " + "; ".join(
            f"Gate {f['gate']} ({f['name']}): {f['detail']}"
            for f in sanity["fails"])
        print(f"\n  HALT: {halt_detail}", file=sys.stderr)
        halted_results = {
            "spec_commit": R2_SPEC_COMMIT,
            "snapshot_sha": snapshot_sha,
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
                "gate5_observed_sha": sanity["gate5_observed_sha"],
                "gate5_observed_boundaries": sanity["gate5_observed_boundaries"],
                "gate5_sha_ok": sanity["gate5_sha_ok"],
                "gate5_boundary_ok": sanity["gate5_boundary_ok"],
            },
            "primary": None,
        }
        write_result_md(halted_results, halted=True, halt_detail=halt_detail)
        write_result_json(halted_results)
        sys.exit(1)

    print("\nDry-run sanity gates PASS; running full test...", file=sys.stderr)
    results = run_full(master, baseline_cutoff, sanity, snapshot_sha)
    write_result_md(results, halted=False)
    write_result_json(results)


if __name__ == "__main__":
    main()
