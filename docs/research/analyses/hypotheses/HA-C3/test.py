"""HA-C3 v2 r2 - Stage 2: convex stress -> fatigue (Wiggers C3 Tier 1, 4-bin redraft).

Implements the LOCKED v2 r2 HA-C3 pre-registration (hypothesis.md LOCKED
2026-06-23 by user acceptance, commit 2a0b0df). Tests Wiggers C3 verbatim
"the stress -> fatigue relationship is non-linear / convex - a 30 -> 40
step costs more than it looks" on per-day same-day mapping
all_day_stress_avg x gevoelscore. v2 collapses v1's B1 [0,20) (n=0 on
this corpus) into the new B1 [0,30); preserves the Wiggers 30->40 anchor
at the new B2-B3 boundary; pre-commits halt-option-A on B4.

Headline cell: unmedicated x 4-bin x gevoelscore bin-mean x 3-condition
gated outcome (Jonckheere-Terpstra monotone + second-difference convexity
contrast S + spline non-linearity) x block-permutation null E[L]=7
(B=10,000).

3-condition gated verdict per spec section 5.1:
  SUPPORTED iff (a) + (b) + (c) all MET in prior direction;
  PARTIAL iff exactly 2-of-3 MET;
  REJECTED iff <=1-of-3 MET OR any wrong-direction firing.

Sensitivity arms (per spec section 4.8) reported alongside:
  - spec section 5.B dose-adjusted cross-phase variant
    (predictor_adj = predictor - 0.57 * dose_plasma_mg)
  - crash-drop sensitivity (CONVENTIONS section 3.4)
  - train/validate M3 overlay (per train_validate_split_fate.md)
  - t+1 lagged variant (descriptive cross-test alignment)
  - within-consolidation spec section 5.A replication if cells survive 30-bar

Per spec section 4.7: two E[L]* checks (linear-residual + bin-label).

Modes:
  python test.py --dry-run   spec section 7.5 sanity gates only.
                              HALT on Gate 1 (B1/B2/B3 n<30; B4 absorbs
                              automatically per spec section 7.3 halt-
                              option-A pre-commit) / Gate 2/3 (distribution
                              sanity) / Gate 4 (total n<100).
  python test.py             dry-run first, halt on failure, else full
                              run; emits result.md + result-data.json.

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

# === Constants per locked v2 r2 hypothesis.md ==========================

# Seed: pre-reg section 10.2 + section 10.5 locks RANDOM_SEED=20260623
# (v2 seed; distinct from v1's 20260622).
RANDOM_SEED = 20260623
BOOTSTRAP_E_L = 7
B_HEADLINE = 10_000

# spec section 4.4 dose-adjustment coefficient
# (citalopram_dose_response_stress_mean_sleep section 5.6.1)
DOSE_BETA_PER_MG = 0.57

# spec section 4.5.1 + 5.1 verdict bars
P_BAR = 0.05
S_NEG_BAR = 0.0
# v2 spec section 4.5.1(c): >=2 of 3 segment midpoints (B1 [0,30) at x=15
# dropped due to natural-cubic boundary condition).
SPLINE_MIDPOINT_COUNT_BAR_4BIN = 2
# Post-halt-option-A 3-bin reduction (spec section 7.3): >=1 of 2 segment
# midpoints (B1 [0,30) at x=15 dropped same reason).
SPLINE_MIDPOINT_COUNT_BAR_3BIN = 1

# spec section 4.1 v2 bin edges (left-inclusive, right-exclusive except B4)
# [0,30), [30,40), [40,60), [60,100]
BIN_EDGES_4BIN = [0.0, 30.0, 40.0, 60.0, 100.0]
BIN_LABELS_4BIN = ["B1[0,30)", "B2[30,40)", "B3[40,60)", "B4[60,100]"]
# Bin midpoints: x=15, x=35, x=50, x=80. Per spec section 4.5.1(c) +
# Locked decision 4: x=15 dropped (natural-cubic boundary forces ~0
# throughout leftmost segment); spline-sign count over {35, 50, 80}.
BIN_MIDPOINTS_FULL_4BIN = [15.0, 35.0, 50.0, 80.0]
BIN_MIDPOINTS_FOR_SPLINE_4BIN = BIN_MIDPOINTS_FULL_4BIN[1:]  # 35, 50, 80

# Post-halt-option-A 3-bin reduction (B3 absorbs B4 -> new B3' [40,100])
BIN_EDGES_3BIN = [0.0, 30.0, 40.0, 100.0]
BIN_LABELS_3BIN = ["B1[0,30)", "B2[30,40)", "B3'[40,100]"]
BIN_MIDPOINTS_FULL_3BIN = [15.0, 35.0, 70.0]
BIN_MIDPOINTS_FOR_SPLINE_3BIN = BIN_MIDPOINTS_FULL_3BIN[1:]  # 35, 70

# spec section 4.5.1(b) Locked decision 6 — 4-bin orthogonal quadratic
# c = (+1, -1, -1, +1) for evenly-spaced points; verified at lock:
# sum = 0, dot with linear (-3, -1, +1, +3) = 0 (orthogonal).
COMPANION_CONTRAST_4BIN = np.asarray([+1, -1, -1, +1], dtype=float)
LINEAR_CONTRAST_4BIN = np.asarray([-3, -1, +1, +3], dtype=float)
assert int(np.dot(COMPANION_CONTRAST_4BIN, LINEAR_CONTRAST_4BIN)) == 0, \
    "Companion contrast must be orthogonal to linear contrast at lock"
# Post-halt-option-A 3-bin reduction: standard 3-point quadratic
# orthogonal contrast c = (+1, -2, +1); sum = 0, dot with (-1,0,+1) = 0.
COMPANION_CONTRAST_3BIN = np.asarray([+1, -2, +1], dtype=float)
LINEAR_CONTRAST_3BIN = np.asarray([-1, 0, +1], dtype=float)
assert int(np.dot(COMPANION_CONTRAST_3BIN, LINEAR_CONTRAST_3BIN)) == 0, \
    "3-bin companion contrast must be orthogonal to linear contrast"

# spec section 7.5 sanity gates
MIN_BIN_N = 30
MIN_TOTAL_N = 100
GATE2_STRESS_MEDIAN_RANGE = (20.0, 60.0)
GATE3_GEVOELSCORE_MEDIAN_RANGE = (3.0, 6.0)

# spec section 4.6 crash-drop flag threshold (standardised |Delta S|)
CRASH_DROP_STANDARDISED_THRESHOLD = 0.10

# spec section 4.7 E[L]* factor-of-2 deviation
EL_DEVIATION_FACTOR = 0.5

# spec section 4.3 + 6 exclusions
LC_ERA_START = date(2022, 4, 4)
UNMEDICATED_END_INCL = date(2024, 4, 8)
APRIL2024_CLUSTER_START = date(2024, 4, 9)
APRIL2024_CLUSTER_END_INCL = date(2024, 4, 16)
# Garmin device-baseline warmup: first 21 days of has_garmin_uds=True
DEVICE_BASELINE_DAYS = 21
# Train/validate split (M3 overlay only)
TRAIN_END = date(2023, 12, 31)
VALIDATE_START = date(2024, 1, 1)
# Consolidation phase (per citalopram_phase_stratification section 3)
CONSOLIDATION_START = date(2024, 6, 20)
CONSOLIDATION_END_INCL = date(2026, 3, 19)

# Spec commit (v2 r2 lock)
V2_R2_SPEC_COMMIT = "2a0b0df"

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


# === Eligibility (spec section 4.3 + 6) ================================

def assign_bin_4bin(s: float) -> int | None:
    """Return bin index 0..3 for stress value s on the v2 4-bin scheme.

    Bins (left-inclusive, right-exclusive except B4 closed-above):
      B1=[0,30), B2=[30,40), B3=[40,60), B4=[60,100]
    Returns None for stress outside [0, 100].
    """
    if s < 0.0 or s > 100.0:
        return None
    for i in range(4):
        lo = BIN_EDGES_4BIN[i]
        hi = BIN_EDGES_4BIN[i + 1]
        if i == 3:
            if lo <= s <= hi:
                return i
        else:
            if lo <= s < hi:
                return i
    return None


def assign_bin_3bin(s: float) -> int | None:
    """Return bin index 0..2 for stress value s on the 3-bin reduction
    (post-halt-option-A absorption):
      B1=[0,30), B2=[30,40), B3'=[40,100]
    Returns None for stress outside [0, 100].
    """
    if s < 0.0 or s > 100.0:
        return None
    for i in range(3):
        lo = BIN_EDGES_3BIN[i]
        hi = BIN_EDGES_3BIN[i + 1]
        if i == 2:
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

    phase: 'unmedicated' (default; primary), 'consolidation', or 'all'
           (for spec section 5.B cross-phase sensitivity arm).
    """
    if d < LC_ERA_START:
        return False
    if phase == "unmedicated" and d > UNMEDICATED_END_INCL:
        return False
    if phase == "consolidation":
        if not (CONSOLIDATION_START <= d <= CONSOLIDATION_END_INCL):
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
               n_bins: int = 4) -> dict:
    """Build temporal pool of (date, stress, gevoelscore, bin, is_crash).

    For dose_adjusted=True (spec section 5.B): predictor_adj = raw -
    DOSE_BETA * dose_plasma_mg.
    For lag_t_plus_1=True (spec section 4.8): outcome is gevoelscore[T+1],
    predictor is stress[T].
    n_bins: 4 for the v2 primary; 3 for the halt-option-A reduction.
    """
    assign_fn = assign_bin_4bin if n_bins == 4 else assign_bin_3bin
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
        b = assign_fn(s_use)
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
        "n_bins": n_bins,
    }


# === Bin descriptives ===================================================

def bin_descriptives(pool: dict) -> dict:
    n_bins = pool["n_bins"]
    bin_n = np.zeros(n_bins, dtype=int)
    bin_mean = np.full(n_bins, float("nan"))
    bin_sd = np.full(n_bins, float("nan"))
    bin_median = np.full(n_bins, float("nan"))
    for b in range(n_bins):
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

    Per pre-reg section 4.5.2: CI per bin from stationary bootstrap at
    E[L]=7.
    """
    n = pool["n"]
    n_bins = pool["n_bins"]
    if n == 0:
        return {f"B{b+1}": (None, None) for b in range(n_bins)}
    p_geom = 1.0 / expected_block_length
    g = pool["gevoelscore"]
    bins = pool["bin"]
    boot_means = np.full((B, n_bins), float("nan"))
    for b_iter in range(B):
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
        for bi in range(n_bins):
            mask = bins_b == bi
            if mask.any():
                boot_means[b_iter, bi] = float(g_b[mask].mean())
    cis: dict[str, tuple] = {}
    for bi in range(n_bins):
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
    For decreasing direction: pair count of (a in bin i, b in bin j>i,
    a > b). We report J* standardised by null mean + SD (asymptotic-
    normal approximation as a descriptive statistic; the block-
    permutation null on the actual test below is the inferential
    p-value driver).
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


def second_diff_S(bin_means: np.ndarray, n_bins: int) -> float:
    """v2 spec section 4.5.1(b) convexity contrast.

    For n_bins == 4: S = (D2_2 + D2_3) / 2, where D2_i = m_{i+1} - 2*m_i
    + m_{i-1} for interior bins i in {2, 3} (0-indexed: i in {1, 2}).
    For n_bins == 3: S = m_3 - 2*m_2 + m_1 = single second-difference.
    """
    if np.any(np.isnan(bin_means)) or len(bin_means) < n_bins:
        return float("nan")
    if n_bins == 4:
        d2 = []
        for i in (1, 2):  # interior bins, 0-indexed
            d2.append(bin_means[i + 1] - 2.0 * bin_means[i] + bin_means[i - 1])
        return float(np.mean(d2))
    elif n_bins == 3:
        return float(bin_means[2] - 2.0 * bin_means[1] + bin_means[0])
    else:
        return float("nan")


def companion_contrast(bin_means: np.ndarray, n_bins: int) -> float:
    """v2 spec section 4.5.1(b) Locked decision 6 companion contrast.

    For n_bins == 4: c = (+1, -1, -1, +1).
    For n_bins == 3: c = (+1, -2, +1).
    """
    if np.any(np.isnan(bin_means)) or len(bin_means) < n_bins:
        return float("nan")
    if n_bins == 4:
        return float(np.dot(COMPANION_CONTRAST_4BIN, bin_means))
    elif n_bins == 3:
        return float(np.dot(COMPANION_CONTRAST_3BIN, bin_means))
    else:
        return float("nan")


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


def _means_per_bin(g: np.ndarray, bins: np.ndarray, n_bins: int) -> np.ndarray:
    """Vectorised per-bin mean; NaN where bin is empty."""
    out = np.full(n_bins, float("nan"))
    for b in range(n_bins):
        m = bins == b
        if m.any():
            out[b] = float(g[m].mean())
    return out


def _spline_F_and_secderiv(pool: dict) -> tuple[float, list[float]]:
    """Natural cubic spline regression on (stress, gevoelscore).

    Returns F-stat (full vs linear-only) and second-derivative at the
    spline-evaluation midpoints (per spec section 4.5.1(c) v2):
      - 4-bin: midpoints {35, 50, 80} (B1 x=15 dropped)
      - 3-bin: midpoints {35, 70} (B1 x=15 dropped)
    """
    n_bins = pool["n_bins"]
    s = pool["stress_use"]
    g = pool["gevoelscore"]
    midpoints_for_spline = (BIN_MIDPOINTS_FOR_SPLINE_4BIN if n_bins == 4
                            else BIN_MIDPOINTS_FOR_SPLINE_3BIN)
    n_midpoints = len(midpoints_for_spline)
    if len(s) < 6:
        return float("nan"), [float("nan")] * n_midpoints
    # Aggregate to bin-mean spline for second-derivative evaluation
    means = _means_per_bin(g, pool["bin"], n_bins)
    valid = ~np.isnan(means)
    n_valid = int(valid.sum())
    if n_valid < 4 if n_bins == 4 else n_valid < 3:
        return float("nan"), [float("nan")] * n_midpoints
    midpoints_full = (BIN_MIDPOINTS_FULL_4BIN if n_bins == 4
                      else BIN_MIDPOINTS_FULL_3BIN)
    x_full = np.asarray(midpoints_full, dtype=float)
    x_fit = x_full[valid]
    y_fit = means[valid]
    try:
        cs = CubicSpline(x_fit, y_fit, bc_type="natural")
    except Exception:
        return float("nan"), [float("nan")] * n_midpoints
    F = _spline_F_from_stress_g(s, g, n_bins)
    sd_list = []
    cs2 = cs.derivative(2)
    for x in midpoints_for_spline:
        try:
            sd_list.append(float(cs2(x)))
        except Exception:
            sd_list.append(float("nan"))
    return F, sd_list


def _spline_F_from_stress_g(s: np.ndarray, g: np.ndarray, n_bins: int) -> float:
    """F-statistic comparing natural-cubic-spline against linear-only fit.

    For n_bins == 4: knots at (30, 40, 60); 3 internal knots; K-2 = 1
                     non-linear basis col? No: K=3 knots; basis cols
                     = K-2 with [1, X]; for K=3 that's 1 col. Need to
                     redo per spec section 4.5.1(c).
    Actually per pre-reg section 4.5.1(c) and section 10.2 step 5(c):
    natural cubic spline regression with 3 internal knots at (30, 40, 60).
    For 3 internal knots, the natural-cubic basis has K-2 = 1 non-linear
    basis col when intercept + linear are explicit per Hastie/Tibshirani
    ESL 5.2.1 eq (5.5): N_k(X) = d_k(X) - d_{K-2}(X), for k=0..K-3.
    For K=3 (3 internal knots), K-3 = 0 cols. That would be degenerate.

    Correction: per spec section 4.5.1(c) "degrees of freedom = number
    of non-linear basis terms = 2 for a natural cubic spline with 3
    internal knots". The interpretation: total basis cols incl. linear =
    K+1 = 4 (1 intercept + 1 linear + K-1 nonlinear); the "nonlinear"
    df is K-1 = 2. Match v1 form: K knots => K-1 nonlinear basis cols.

    For n_bins == 3 (post-absorption): 2 internal knots at (30, 40);
    K-1 = 1 nonlinear basis col.
    """
    if len(s) < 6:
        return float("nan")
    n = len(s)
    if n_bins == 4:
        knots = [30.0, 40.0, 60.0]
    elif n_bins == 3:
        knots = [30.0, 40.0]
    else:
        return float("nan")
    K = len(knots)
    if K < 2:
        return float("nan")

    X_lin = np.column_stack([np.ones(n), s])

    def trunc_cube(x, k):
        d = x - k
        return np.where(d > 0, d * d * d, 0.0)

    def natural_basis(s_arr):
        # Per Hastie/Tibshirani ESL 5.2.1 eq (5.5):
        # d_k(X) = ((X - knot_k)+^3 - (X - knot_K)+^3) / (knot_K - knot_k)
        # N_k(X) = d_k(X) - d_{K-2}(X), for k=0..K-3.
        # Together with [1, X] this gives K basis functions over K knots.
        K_local = len(knots)
        d_cols = []
        for k in range(K_local - 1):
            denom = knots[K_local - 1] - knots[k]
            if denom == 0:
                d_cols.append(np.zeros(n))
            else:
                d_k = (trunc_cube(s_arr, knots[k])
                       - trunc_cube(s_arr, knots[K_local - 1])) / denom
                d_cols.append(d_k)
        cols = []
        for k in range(K_local - 2):
            cols.append(d_cols[k] - d_cols[K_local - 2])
        return np.column_stack(cols) if cols else np.zeros((n, 0))

    NB = natural_basis(s)
    if NB.shape[1] == 0:
        # Degenerate (K=2 knots gives 0 nonlinear basis cols). Add a
        # single truncated-power col as the nonlinear basis surrogate.
        # For 2 knots, the truncated-cube at knot 1 IS the only
        # nonlinear basis function under the natural BC.
        NB = trunc_cube(s, knots[0]).reshape(-1, 1)
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


def _spline_F_parametric(pool: dict) -> tuple[float, float]:
    """Parametric F + p (descriptive only per spec section 4.5.1(c))."""
    from scipy import stats as sps
    n_bins = pool["n_bins"]
    s = pool["stress_use"]
    g = pool["gevoelscore"]
    if len(s) < 6:
        return float("nan"), float("nan")
    F = _spline_F_from_stress_g(s, g, n_bins)
    if math.isnan(F):
        return float("nan"), float("nan")
    n = len(s)
    if n_bins == 4:
        # 3 knots -> 1 NL basis col from ESL formula; surrogate adds 0
        # because K-2=1>0. df_diff = 1; df_resid = n - 3.
        df_diff = 1
        df_resid = n - 3
    elif n_bins == 3:
        # 2 knots -> 0 NL basis cols from ESL formula -> 1 surrogate col.
        df_diff = 1
        df_resid = n - 3
    else:
        return F, float("nan")
    if df_resid <= 0:
        return F, float("nan")
    p = float(sps.f.sf(F, df_diff, df_resid))
    return F, p


def block_permutation_three_conditions(pool: dict, B: int,
                                        expected_block_length: int,
                                        rng: np.random.Generator) -> dict:
    """Compute (a) J* + (b) S + (c) spline F via block-permutation null
    per spec section 4.7.

    Permutation target: bin_label sequence is resampled via stationary
    bootstrap (geometric block length E[L]=7), keeping gevoelscore in
    original temporal position. This breaks the (bin -> gevoelscore)
    relationship while preserving the within-gevoelscore autocorrelation.
    """
    n = pool["n"]
    n_bins = pool["n_bins"]
    p_geom = 1.0 / expected_block_length
    g = pool["gevoelscore"]
    bins_obs = pool["bin"]
    midpoints_full = (BIN_MIDPOINTS_FULL_4BIN if n_bins == 4
                      else BIN_MIDPOINTS_FULL_3BIN)

    # Observed values
    obs_means = _means_per_bin(g, bins_obs, n_bins)
    obs_jt = jonckheere_terpstra(
        [g[bins_obs == b] for b in range(n_bins)])
    obs_J_star = obs_jt["J_star"]
    obs_S = second_diff_S(obs_means, n_bins)
    obs_companion = companion_contrast(obs_means, n_bins)
    obs_spline_F, obs_spline_secderiv = _spline_F_and_secderiv(pool)

    # Build null distributions
    null_J_star = np.full(B, float("nan"))
    null_S = np.full(B, float("nan"))
    null_F = np.full(B, float("nan"))
    null_companion = np.full(B, float("nan"))

    for b_iter in range(B):
        idx = stationary_bootstrap_indices(n, p_geom, rng)
        bins_null = bins_obs[idx]
        means_null = _means_per_bin(g, bins_null, n_bins)
        if np.any(np.isnan(means_null)):
            # If a bin has zero observations in this null draw, fill its
            # mean with the pool-grand-mean (avoids NaN propagation).
            grand = float(g.mean())
            means_null = np.where(np.isnan(means_null), grand, means_null)
        # (a) JT
        jt = jonckheere_terpstra(
            [g[bins_null == bb] for bb in range(n_bins)])
        null_J_star[b_iter] = jt["J_star"]
        # (b) S
        null_S[b_iter] = second_diff_S(means_null, n_bins)
        null_companion[b_iter] = companion_contrast(means_null, n_bins)
        # (c) spline F: use bin-midpoint as pseudo-stress for each day
        # under the null label (consistent treatment with using bin
        # labels as the permutation target).
        pseudo_stress = np.asarray([midpoints_full[bn] for bn in bins_null],
                                   dtype=float)
        F_null = _spline_F_from_stress_g(pseudo_stress, g, n_bins)
        null_F[b_iter] = F_null

    # Observed F via same bin-midpoint pseudo-stress (consistent
    # treatment between observed + null)
    obs_pseudo_stress = np.asarray([midpoints_full[bn] for bn in bins_obs],
                                   dtype=float)
    obs_F_midpoint = _spline_F_from_stress_g(obs_pseudo_stress, g, n_bins)

    # Empirical one-sided p-values
    # (a) decreasing: under H1 J_star is negative; p_a = (1 + #{J*_null <= J*_obs}) / (B+1)
    n_le = int((null_J_star <= obs_J_star).sum())
    p_a = (1 + n_le) / (B + 1)
    # (b) convex: under H1 S < 0; p_b = (1 + #{S_null <= S_obs}) / (B+1)
    n_le_s = int((null_S <= obs_S).sum())
    p_b = (1 + n_le_s) / (B + 1)
    # (c) non-linearity F: under H1 F_obs is LARGE; p_c = (1 + #{F_null >= F_obs}) / (B+1)
    n_ge_f = int((null_F >= obs_F_midpoint).sum())
    p_c = (1 + n_ge_f) / (B + 1)
    # companion descriptive direction
    n_le_c = int((null_companion <= obs_companion).sum())
    p_companion = (1 + n_le_c) / (B + 1)

    # Parametric F (descriptive only per pre-reg section 4.5.1(c))
    parametric_F, parametric_p = _spline_F_parametric(pool)

    return {
        "obs": {
            "J_star": float(obs_J_star) if not math.isnan(obs_J_star) else None,
            "S": float(obs_S) if not math.isnan(obs_S) else None,
            "spline_F_block_perm_target": (float(obs_F_midpoint)
                                            if not math.isnan(obs_F_midpoint)
                                            else None),
            "spline_F_continuous_predictor": (float(obs_spline_F)
                                               if not math.isnan(obs_spline_F)
                                               else None),
            "spline_second_derivative_at_midpoints": [
                float(x) if not math.isnan(x) else None
                for x in obs_spline_secderiv
            ],
            "companion_contrast": (float(obs_companion)
                                    if not math.isnan(obs_companion)
                                    else None),
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
            "p_parametric": (float(parametric_p)
                              if not math.isnan(parametric_p) else None),
        },
    }


def mann_whitney_pairwise(pool: dict) -> list[dict]:
    """Adjacent-bin pairwise Mann-Whitney per spec section 4.5.2.

    For n_bins == 4: 3 adjacent pairs (B1-B2, B2-B3, B3-B4).
    For n_bins == 3: 2 adjacent pairs (B1-B2, B2-B3').
    """
    from scipy import stats as sps
    n_bins = pool["n_bins"]
    g = pool["gevoelscore"]
    bins = pool["bin"]
    out = []
    for i in range(n_bins - 1):
        gi = g[bins == i]
        gj = g[bins == i + 1]
        if len(gi) < 2 or len(gj) < 2:
            out.append({
                "pair": f"B{i+1}-B{i+2}" if (n_bins == 4 or i == 0)
                        else f"B{i+1}-B{i+2}'",
                "n_i": int(len(gi)), "n_j": int(len(gj)),
                "U": None, "p_two_sided": None,
            })
            continue
        try:
            U, p = sps.mannwhitneyu(gi, gj, alternative="two-sided")
            label = f"B{i+1}-B{i+2}"
            if n_bins == 3 and i == 1:
                label = "B2-B3'"
            out.append({
                "pair": label,
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
    """Spearman rho on continuous (stress, gevoelscore)."""
    from scipy import stats as sps
    s = pool["stress_use"]
    g = pool["gevoelscore"]
    if len(s) < 3:
        return {"rho": None, "p": None, "n": int(len(s))}
    rho, p = sps.spearmanr(s, g)
    return {"rho": float(rho), "p": float(p), "n": int(len(s))}


# === Verdict gating (spec section 5.1 3-condition) =====================

def verdict_three_condition(perm: dict, spline_secderiv: list[float],
                             n_bins: int) -> dict:
    """spec section 5.1 3-condition gated verdict.

    Spline gate per spec section 4.5.1(c) Locked decision 4:
      - n_bins == 4: >= 2 of 3 segment midpoints negative {35, 50, 80}
      - n_bins == 3: >= 1 of 2 segment midpoints negative {35, 70}
    With strict sign agreement (positive-sign midpoint does NOT count
    toward the threshold).
    """
    p = perm["p_values"]
    obs = perm["obs"]
    p_a = p["p_a_jonckheere_decreasing"]
    p_b = p["p_b_S_convex"]
    p_c = p["p_c_spline_nonlinearity"]
    # Direction checks
    a_direction_ok = (obs["J_star"] is not None) and (obs["J_star"] < 0)
    b_direction_ok = (obs["S"] is not None) and (obs["S"] < 0)
    valid_sd = [x for x in spline_secderiv if x is not None and not math.isnan(x)]
    n_neg = sum(1 for x in valid_sd if x < 0)
    n_pos = sum(1 for x in valid_sd if x > 0)
    if n_bins == 4:
        spline_count_bar = SPLINE_MIDPOINT_COUNT_BAR_4BIN
    else:
        spline_count_bar = SPLINE_MIDPOINT_COUNT_BAR_3BIN
    c_direction_ok = n_neg >= spline_count_bar

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
    if p_c < P_BAR and n_pos >= spline_count_bar:
        wrong_dir_fired = True
        wrong_dir_notes.append(
            f"(c) spline second-derivative POSITIVE at >= {spline_count_bar} "
            "midpoints (positive sign at majority of contributing midpoints)")

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
        "spline_pos_count": int(n_pos),
        "spline_total_midpoints": int(len(valid_sd)),
        "spline_count_bar": int(spline_count_bar),
        "n_met": n_met,
        "wrong_direction_fired": bool(wrong_dir_fired),
        "wrong_direction_notes": wrong_dir_notes,
        "verdict": verdict, "verdict_label": verdict_label,
    }


# === Sanity gates (spec section 7.5) ===================================

def run_sanity_gates(pool: dict) -> dict:
    """Run spec section 7.5 sanity gates 1-4. Returns dict with verdict.

    v2 specifics per section 7.3 + 7.5:
      - Gate 1 evaluated per-bin. B4 underpower (n < 30) auto-absorbs
        via halt-option-A (widen B3 to absorb B4); B1/B2/B3 underpower
        requires v3 redraft (HALT).
      - All other gates (2, 3, 4) HALT if failing.
    """
    n_bins = pool["n_bins"]
    desc = bin_descriptives(pool)
    bin_n = desc["bin_n"]
    fails: list[dict] = []

    # Gate 1: each bin n >= 30
    n_below_30 = [b for b in range(n_bins) if bin_n[b] < MIN_BIN_N]
    gate1_ok = len(n_below_30) == 0
    if not gate1_ok:
        # v2 section 7.3 halt-option-A: pre-committed for B4 (last bin
        # on 4-bin scheme). If B4 is the sole failing bin, absorption
        # is applied automatically; no halt.
        if n_bins == 4 and n_below_30 == [3]:
            fails.append({
                "gate": 1, "name": "per-bin n >= 30",
                "detail": (f"B4 n={bin_n[3]} < {MIN_BIN_N}; v2 spec section "
                           f"7.3 halt-option-A PRE-COMMITTED at lock: widen "
                           f"B3 to absorb B4."),
                "halt_optA_applicable": True,
            })
        else:
            fails.append({
                "gate": 1, "name": "per-bin n >= 30",
                "detail": (f"bins below threshold: "
                           f"{[(f'B{b+1}', bin_n[b]) for b in n_below_30]}; "
                           f"v2 spec section 7.3 halt-option-A "
                           f"PRE-COMMITTED only for sole-B4 failure; other "
                           f"failures require v3 spec redraft."),
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
            "halt_optA_applicable": False,
        })

    # Gate 3: gevoelscore median in [3, 6]
    g_med = float(np.median(pool["gevoelscore"])) if pool["n"] > 0 else float("nan")
    g3_lo, g3_hi = GATE3_GEVOELSCORE_MEDIAN_RANGE
    gate3_ok = g3_lo <= g_med <= g3_hi
    if not gate3_ok:
        fails.append({
            "gate": 3, "name": "gevoelscore median in [3, 6]",
            "detail": f"observed median = {g_med:.2f}; outside [{g3_lo}, {g3_hi}]",
            "halt_optA_applicable": False,
        })

    # Gate 4: total n >= 100 (per v2 section 7.5 simplified) AND
    # at least 2 bins with n>=30 (per v2 section 7.5 power-density form)
    n_at_least_30 = sum(1 for b in range(n_bins) if bin_n[b] >= MIN_BIN_N)
    total_n = sum(bin_n)
    gate4_ok = (n_at_least_30 >= 2) and (total_n >= MIN_TOTAL_N)
    if not gate4_ok:
        fails.append({
            "gate": 4, "name": "power density (>= 2 bins with n>=30 AND total n>=100)",
            "detail": f"bins with n>=30: {n_at_least_30}; total n: {total_n}",
            "halt_optA_applicable": False,
        })

    return {
        "n_bins": n_bins,
        "bin_n": bin_n, "bin_mean": desc["bin_mean"],
        "bin_median": desc["bin_median"],
        "stress_median": s_med, "gevoelscore_median": g_med,
        "total_n": total_n,
        "gate1_ok": gate1_ok, "gate2_ok": gate2_ok,
        "gate3_ok": gate3_ok, "gate4_ok": gate4_ok,
        "fails": fails,
        "verdict": "PASS" if not fails else "HALT",
    }


# === Halt-option-A absorb (spec section 7.3) ===========================

def apply_halt_optA(pool: dict, master: dict,
                    baseline_cutoff: date | None,
                    phase: str = "unmedicated",
                    dose_adjusted: bool = False,
                    lag_t_plus_1: bool = False,
                    drop_crashes: bool = False) -> dict:
    """v2 spec section 7.3 halt-option-A: widen B3 [40, 60) to absorb
    B4 [60, 100]. Returns a fresh pool rebuilt on the 3-bin scheme."""
    return build_pool(master, baseline_cutoff, phase=phase,
                      dose_adjusted=dose_adjusted,
                      lag_t_plus_1=lag_t_plus_1,
                      drop_crashes=drop_crashes,
                      n_bins=3)


# === Dry-run + write reports ===========================================

def dry_run(master: dict, baseline_cutoff: date | None) -> dict:
    """Run spec section 7.5 sanity gates on the primary unmedicated pool."""
    print("", file=sys.stderr)
    print("=== HA-C3 v2 r2 dry-run ===", file=sys.stderr)
    print(f"  RANDOM_SEED={RANDOM_SEED}; B={B_HEADLINE}; E[L]={BOOTSTRAP_E_L}",
          file=sys.stderr)
    print(f"  spec commit: {V2_R2_SPEC_COMMIT}", file=sys.stderr)
    if baseline_cutoff is not None:
        print(f"  device baseline cutoff (excl <=): {baseline_cutoff}",
              file=sys.stderr)
    print("", file=sys.stderr)
    print("Building primary unmedicated pool (spec section 4.2 + 4.3 + 4.4 5.A)...",
          file=sys.stderr)
    pool = build_pool(master, baseline_cutoff, phase="unmedicated", n_bins=4)
    print(f"  pool n = {pool['n']}", file=sys.stderr)
    sanity = run_sanity_gates(pool)
    print("\n--- spec section 7.5 sanity gate results ---", file=sys.stderr)
    print(f"  bin sizes (4-bin): {sanity['bin_n']}", file=sys.stderr)
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
    print(f"  gate 4 (>=2 bins n>=30 AND total>=100): "
          f"{'PASS' if sanity['gate4_ok'] else 'FAIL'}", file=sys.stderr)
    print(f"  verdict: {sanity['verdict']}", file=sys.stderr)
    sanity["pool"] = pool
    return sanity


def write_dry_run_report(sanity: dict, applied_optA: bool = False,
                         sanity_after_optA: dict | None = None) -> None:
    halt = sanity["verdict"] == "HALT" and not applied_optA
    if applied_optA:
        title = ("HA-C3 v2 r2 dry-run report - section 7.3 halt-option-A "
                 "triggered (PRE-COMMITTED absorb; proceeding)")
    elif halt:
        title = ("HA-C3 v2 r2 dry-run report - sanity gate FAILURE "
                 "outside halt-option-A scope (HALT)")
    else:
        title = "HA-C3 v2 r2 dry-run report - sanity gates PASS"
    lines = [
        f"# {title}",
        "",
        ("Emitted by `test.py --dry-run` per locked v2 r2 hypothesis.md "
         "section 10.4. Headline cell: unmedicated x 4-bin x `gevoelscore` "
         "x 3-condition gated outcome x block-permutation null at E[L]=7. "
         "Day-validity per section 4.3 (LC era + unmedicated + not "
         "April-2024 cluster + not first 21 device-baseline days + non-NaN "
         "both columns)."),
        "",
        f"- Pool n = {sanity['total_n']}",
        f"- Stress median = {sanity['stress_median']:.2f}",
        f"- Gevoelscore median = {sanity['gevoelscore_median']:.2f}",
        "",
        "## Per-bin sample sizes (`all_day_stress_avg`, v2 4-bin scheme)",
        "",
        "| bin | label | n | mean gevoelscore | median gevoelscore |",
        "|---|---|---:|---:|---:|",
    ]
    for b in range(4):
        m = sanity["bin_mean"][b]
        md = sanity["bin_median"][b]
        lines.append(
            f"| B{b+1} | {BIN_LABELS_4BIN[b]} | {sanity['bin_n'][b]} | "
            f"{f'{m:.3f}' if m is not None else 'NA'} | "
            f"{f'{md:.2f}' if md is not None else 'NA'} |")
    lines.append("")
    lines.append("## Gate results")
    lines.append("")
    lines.append("| gate | description | result |")
    lines.append("|---|---|---|")
    lines.append(f"| 1 | per-bin n >= {MIN_BIN_N} (4 bins) | "
                 f"{'PASS' if sanity['gate1_ok'] else 'FAIL'} |")
    lines.append(f"| 2 | stress median in {list(GATE2_STRESS_MEDIAN_RANGE)} | "
                 f"{'PASS' if sanity['gate2_ok'] else 'FAIL'} |")
    lines.append(f"| 3 | gevoelscore median in {list(GATE3_GEVOELSCORE_MEDIAN_RANGE)} | "
                 f"{'PASS' if sanity['gate3_ok'] else 'FAIL'} |")
    lines.append(f"| 4 | >= 2 bins n>=30 AND total n>={MIN_TOTAL_N} | "
                 f"{'PASS' if sanity['gate4_ok'] else 'FAIL'} |")
    lines.append("")
    if applied_optA:
        lines.extend([
            "## section 7.3 halt-option-A APPLIED (PRE-COMMITTED absorb)",
            "",
            ("Per v2 r2 LOCKED spec section 7.3 + section 4.1: B4 [60,100] "
             "underpower (n < 30) triggers automatic absorption into B3 "
             "[40,60), producing the 3-bin reduction "
             "`{B1 [0,30), B2 [30,40), B3' [40,100]}`. The test runs on "
             "the 3-bin reduction with the contrast reduced to a single "
             "second-difference `S = m_3 - 2*m_2 + m_1` and the spline "
             "reduced to 2 internal knots at (30, 40); visual-gating count "
             "reduces to >= 1 of 2 segment midpoints from {35, 70}. "
             "This is NOT a halt; the LOCKED spec PRE-COMMITS to this "
             "absorption as the default for B4 underpower."),
            "",
            "**3-bin reduction descriptives (post-absorption)**:",
            "",
            "| bin | label | n | mean gevoelscore | median gevoelscore |",
            "|---|---|---:|---:|---:|",
        ])
        for b in range(3):
            m = sanity_after_optA["bin_mean"][b]
            md = sanity_after_optA["bin_median"][b]
            lines.append(
                f"| B{b+1} | {BIN_LABELS_3BIN[b]} | "
                f"{sanity_after_optA['bin_n'][b]} | "
                f"{f'{m:.3f}' if m is not None else 'NA'} | "
                f"{f'{md:.2f}' if md is not None else 'NA'} |")
        lines.append("")
        lines.append("**Dry-run verdict: PASS (after section 7.3 absorption)** "
                     "-- proceeding with full run on the 3-bin reduction.")
        lines.append("")
    elif halt:
        lines.extend([
            "## HALT-eligible failures (outside halt-option-A scope)",
            "",
        ])
        for f in sanity["fails"]:
            lines.append(f"- **Gate {f['gate']}** ({f['name']}): {f['detail']}")
            if f.get("halt_optA_applicable"):
                lines.append("  - **section 7.3 halt-option-A absorption applies**.")
        lines.extend([
            "",
            ("Per locked v2 r2 section 10.4 step 1 + `hypothesis_lock_process.md` "
             "section 3.9: the full test is **HALTed** if the failure is not "
             "absorbed by the pre-committed section 7.3 halt-option-A. Failures "
             "other than sole-B4 underpower require a v3 spec redraft."),
            "",
        ])
    else:
        lines.append("**Dry-run verdict: PASS** -- proceed with full run.")
        lines.append("")
    OUT_DRYRUN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {OUT_DRYRUN_MD}", file=sys.stderr)


# === Full run (spec section 10.4 step 2) ===============================

def run_full(master: dict, baseline_cutoff: date | None,
             sanity: dict, applied_optA: bool = False,
             sanity_original: dict | None = None) -> dict:
    """Run the full test on the primary pool + sensitivity arms."""
    rng = np.random.default_rng(RANDOM_SEED)
    pool = sanity["pool"]
    n_bins = pool["n_bins"]
    print("\n=== HA-C3 v2 r2 full run ===", file=sys.stderr)
    print(f"  pool n = {pool['n']}; n_bins = {n_bins}", file=sys.stderr)
    if applied_optA:
        print("  (section 7.3 halt-option-A APPLIED: B3 widened to "
              "absorb B4)", file=sys.stderr)

    # --- Primary 3-condition tests (spec section 4.5.1) ---
    print("\n  primary 3-condition block-permutation tests "
          f"(B={B_HEADLINE})...", file=sys.stderr)
    perm = block_permutation_three_conditions(
        pool, B_HEADLINE, BOOTSTRAP_E_L, rng)
    F_continuous, spline_sd = _spline_F_and_secderiv(pool)
    print(f"    J* = {perm['obs']['J_star']}", file=sys.stderr)
    print(f"    S  = {perm['obs']['S']}", file=sys.stderr)
    print(f"    spline F (continuous) = {F_continuous}", file=sys.stderr)
    midpoint_labels = (BIN_MIDPOINTS_FOR_SPLINE_4BIN if n_bins == 4
                       else BIN_MIDPOINTS_FOR_SPLINE_3BIN)
    print(f"    spline 2nd-deriv at midpoints {midpoint_labels}: "
          f"{[f'{x:.4f}' for x in spline_sd]}", file=sys.stderr)
    print(f"    p_a = {perm['p_values']['p_a_jonckheere_decreasing']:.4f}",
          file=sys.stderr)
    print(f"    p_b = {perm['p_values']['p_b_S_convex']:.4f}", file=sys.stderr)
    print(f"    p_c = {perm['p_values']['p_c_spline_nonlinearity']:.4f}",
          file=sys.stderr)

    # --- 3-condition verdict ---
    verdict = verdict_three_condition(perm, spline_sd, n_bins)
    print(f"\n  3-condition verdict: {verdict['verdict_label']}",
          file=sys.stderr)

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
    n_pairs = n_bins - 1  # 3 for 4-bin, 2 for 3-bin
    holm = holm_step_down(np.asarray(holm_in), n_eff=n_pairs, alpha=0.05)
    for i, pp in enumerate(pairs):
        pp["holm_adjusted_p"] = float(holm["adjusted_p_values"][i])
        pp["holm_rejected"] = bool(holm["rejected"][i])
        pp["holm_threshold"] = float(holm["thresholds"][i])
    rho = spearman_rho(pool)

    # --- spec section 5.A unmedicated headline result is the PRIMARY ---
    # (already done above; the primary pool IS the unmedicated phase pool)

    # --- spec section 5.B dose-adjusted cross-phase sensitivity arm ---
    print("\n  spec section 5.B dose-adjusted cross-phase sensitivity "
          "arm...", file=sys.stderr)
    pool_5B = build_pool(master, baseline_cutoff, phase="all",
                          dose_adjusted=True, n_bins=4)
    # Apply halt-option-A recursively if needed on 5B
    bin_n_5B = [int((pool_5B["bin"] == b).sum()) for b in range(4)]
    optA_applied_5B = False
    if bin_n_5B[3] < MIN_BIN_N and all(bin_n_5B[b] >= MIN_BIN_N for b in range(3)):
        pool_5B = build_pool(master, baseline_cutoff, phase="all",
                              dose_adjusted=True, n_bins=3)
        optA_applied_5B = True
    print(f"    pool 5.B n = {pool_5B['n']}; n_bins = {pool_5B['n_bins']}; "
          f"optA_applied = {optA_applied_5B}",
          file=sys.stderr)
    if pool_5B["n"] >= MIN_TOTAL_N:
        # Check whether each bin meets the threshold; require all bins
        # have n >= 30 for the test to proceed.
        bin_n_after_5B = [int((pool_5B["bin"] == b).sum())
                          for b in range(pool_5B["n_bins"])]
        if all(n >= MIN_BIN_N for n in bin_n_after_5B):
            perm_5B = block_permutation_three_conditions(
                pool_5B, B_HEADLINE, BOOTSTRAP_E_L, rng)
            F_5B, sd_5B = _spline_F_and_secderiv(pool_5B)
            verdict_5B = verdict_three_condition(perm_5B, sd_5B,
                                                  pool_5B["n_bins"])
        else:
            perm_5B = None
            verdict_5B = {
                "verdict": "INCONCLUSIVE",
                "verdict_label": ("INCONCLUSIVE (a bin has n < 30 even "
                                  "after halt-option-A)"),
            }
    else:
        perm_5B = None
        verdict_5B = {
            "verdict": "INCONCLUSIVE",
            "verdict_label": "INCONCLUSIVE (pool too small)",
        }
    bin_n_5B_after = [int((pool_5B["bin"] == b).sum())
                      for b in range(pool_5B["n_bins"])]
    bin_mean_5B = _means_per_bin(pool_5B["gevoelscore"], pool_5B["bin"],
                                  pool_5B["n_bins"])

    # --- Crash-drop sensitivity (spec section 4.6) ---
    print("\n  spec section 4.6 crash-drop sensitivity...", file=sys.stderr)
    pool_no_crash = build_pool(master, baseline_cutoff, phase="unmedicated",
                                drop_crashes=True, n_bins=n_bins)
    means_full = _means_per_bin(pool["gevoelscore"], pool["bin"], n_bins)
    means_nocr = _means_per_bin(pool_no_crash["gevoelscore"],
                                 pool_no_crash["bin"], n_bins)
    S_full = second_diff_S(means_full, n_bins)
    S_nocr = second_diff_S(means_nocr, n_bins)
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
        "delta_standardised": (None if math.isnan(delta_std)
                                else float(delta_std)),
        "sign_change": (
            (not math.isnan(S_full)) and (not math.isnan(S_nocr))
            and ((S_full < 0) != (S_nocr < 0))
        ),
        "flag": (
            (not math.isnan(delta_std)
             and delta_std > CRASH_DROP_STANDARDISED_THRESHOLD)
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
            "n_bins": n_bins,
        }
    pool_train = _slice(train_mask)
    pool_validate = _slice(validate_mask)
    means_train = _means_per_bin(pool_train["gevoelscore"],
                                  pool_train["bin"], n_bins)
    means_validate = _means_per_bin(pool_validate["gevoelscore"],
                                     pool_validate["bin"], n_bins)
    overlay = {
        "train_n": pool_train["n"],
        "validate_n": pool_validate["n"],
        "train_bin_n": [int((pool_train["bin"] == b).sum())
                         for b in range(n_bins)],
        "validate_bin_n": [int((pool_validate["bin"] == b).sum())
                            for b in range(n_bins)],
        "train_bin_mean": [None if math.isnan(m) else float(m)
                            for m in means_train],
        "validate_bin_mean": [None if math.isnan(m) else float(m)
                               for m in means_validate],
        "train_S": (None if math.isnan(second_diff_S(means_train, n_bins))
                    else float(second_diff_S(means_train, n_bins))),
        "validate_S": (None if math.isnan(second_diff_S(means_validate, n_bins))
                       else float(second_diff_S(means_validate, n_bins))),
    }

    # --- t+1 lagged variant (spec section 4.8) ---
    print("\n  spec section 4.8 t+1 lagged variant...", file=sys.stderr)
    pool_lag = build_pool(master, baseline_cutoff, phase="unmedicated",
                          lag_t_plus_1=True, n_bins=n_bins)
    means_lag = _means_per_bin(pool_lag["gevoelscore"], pool_lag["bin"],
                                n_bins)
    S_lag = second_diff_S(means_lag, n_bins)
    lagged = {
        "n": pool_lag["n"],
        "bin_n": [int((pool_lag["bin"] == b).sum()) for b in range(n_bins)],
        "bin_mean": [None if math.isnan(m) else float(m) for m in means_lag],
        "S": (None if math.isnan(S_lag) else float(S_lag)),
    }

    # --- Within-consolidation section 5.A replication (spec 4.4 / 4.8) ---
    print("\n  spec section 4.4 within-consolidation section 5.A "
          "replication...", file=sys.stderr)
    pool_consol = build_pool(master, baseline_cutoff, phase="consolidation",
                              n_bins=4)
    consol_bin_n = [int((pool_consol["bin"] == b).sum()) for b in range(4)]
    consol_optA_applied = False
    consol_pool_used = pool_consol
    if consol_bin_n[3] < MIN_BIN_N and all(consol_bin_n[b] >= MIN_BIN_N
                                            for b in range(3)):
        consol_pool_used = build_pool(master, baseline_cutoff,
                                       phase="consolidation", n_bins=3)
        consol_optA_applied = True
    consol_bin_n_after = [int((consol_pool_used["bin"] == b).sum())
                           for b in range(consol_pool_used["n_bins"])]
    n_at_least_30_after = sum(1 for b in range(consol_pool_used["n_bins"])
                              if consol_bin_n_after[b] >= MIN_BIN_N)
    if (n_at_least_30_after >= consol_pool_used["n_bins"]
            and consol_pool_used["n"] >= MIN_TOTAL_N):
        consol_perm = block_permutation_three_conditions(
            consol_pool_used, B_HEADLINE, BOOTSTRAP_E_L, rng)
        consol_F, consol_sd = _spline_F_and_secderiv(consol_pool_used)
        consol_verdict = verdict_three_condition(consol_perm, consol_sd,
                                                  consol_pool_used["n_bins"])
    else:
        consol_perm = None
        consol_verdict = {
            "verdict": "INCONCLUSIVE",
            "verdict_label": ("INCONCLUSIVE (fewer than all bins have n>=30 "
                              "or total<100 after halt-option-A reduction)"),
        }
    consolidation = {
        "n": pool_consol["n"], "bin_n": consol_bin_n,
        "optA_applied": consol_optA_applied,
        "bin_n_after_optA": consol_bin_n_after,
        "n_bins_used": consol_pool_used["n_bins"],
        "verdict": consol_verdict.get("verdict_label"),
        "perm": consol_perm,
    }

    # --- spec section 4.7 E[L]* checks (linear-residual + bin-label) ---
    print("\n  spec section 4.7 E[L]* checks (linear-residual + "
          "bin-label)...", file=sys.stderr)
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
        "spec_commit": V2_R2_SPEC_COMMIT,
        "applied_optA": applied_optA,
        "n_bins": n_bins,
        "config": {
            "RANDOM_SEED": RANDOM_SEED,
            "B_HEADLINE": B_HEADLINE,
            "BOOTSTRAP_E_L": BOOTSTRAP_E_L,
            "P_BAR": P_BAR,
            "MIN_BIN_N": MIN_BIN_N,
            "MIN_TOTAL_N": MIN_TOTAL_N,
            "DOSE_BETA_PER_MG": DOSE_BETA_PER_MG,
            "SPLINE_MIDPOINT_COUNT_BAR_4BIN": SPLINE_MIDPOINT_COUNT_BAR_4BIN,
            "SPLINE_MIDPOINT_COUNT_BAR_3BIN": SPLINE_MIDPOINT_COUNT_BAR_3BIN,
            "BIN_EDGES_4BIN": BIN_EDGES_4BIN,
            "BIN_EDGES_3BIN": BIN_EDGES_3BIN,
            "BIN_MIDPOINTS_FULL_4BIN": BIN_MIDPOINTS_FULL_4BIN,
            "BIN_MIDPOINTS_FULL_3BIN": BIN_MIDPOINTS_FULL_3BIN,
            "BIN_MIDPOINTS_FOR_SPLINE_4BIN": BIN_MIDPOINTS_FOR_SPLINE_4BIN,
            "BIN_MIDPOINTS_FOR_SPLINE_3BIN": BIN_MIDPOINTS_FOR_SPLINE_3BIN,
            "COMPANION_CONTRAST_4BIN": COMPANION_CONTRAST_4BIN.tolist(),
            "COMPANION_CONTRAST_3BIN": COMPANION_CONTRAST_3BIN.tolist(),
            "applied_optA": applied_optA,
        },
        "primary": {
            "pool_n": pool["n"],
            "bin_n": [int((pool["bin"] == b).sum()) for b in range(n_bins)],
            "bin_mean": [None if math.isnan(m) else float(m)
                          for m in _means_per_bin(g, pool["bin"], n_bins)],
            "bin_ci_95": bin_ci,
            "perm": perm,
            "spline_continuous_F": (float(F_continuous)
                                     if not math.isnan(F_continuous) else None),
            "spline_second_derivative_at_midpoints": [
                None if math.isnan(x) else float(x) for x in spline_sd
            ],
            "spline_midpoint_x_values": (BIN_MIDPOINTS_FOR_SPLINE_4BIN
                                          if n_bins == 4
                                          else BIN_MIDPOINTS_FOR_SPLINE_3BIN),
            "verdict": verdict,
            "pairwise_mann_whitney": pairs,
            "spearman_rho": rho,
        },
        "sensitivity_5B": {
            "pool_n": pool_5B["n"],
            "n_bins_used": pool_5B["n_bins"],
            "optA_applied": optA_applied_5B,
            "bin_n": bin_n_5B_after,
            "bin_mean": [None if math.isnan(m) else float(m)
                          for m in bin_mean_5B],
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
            "bin_median": sanity.get("bin_median", [None] * len(sanity["bin_n"])),
            "stress_median": sanity["stress_median"],
            "gevoelscore_median": sanity["gevoelscore_median"],
            "total_n": sanity["total_n"],
            "verdict": sanity["verdict"],
            "fails": sanity["fails"],
        },
        "sanity_original": {
            "bin_n": (sanity_original or sanity)["bin_n"],
            "bin_mean": (sanity_original or sanity)["bin_mean"],
            "bin_median": (sanity_original or sanity).get("bin_median", [None] * len((sanity_original or sanity)["bin_n"])),
            "stress_median": (sanity_original or sanity)["stress_median"],
            "gevoelscore_median": (sanity_original or sanity)["gevoelscore_median"],
            "total_n": (sanity_original or sanity)["total_n"],
            "verdict": (sanity_original or sanity)["verdict"],
            "fails": (sanity_original or sanity)["fails"],
        },
    }


def write_result_md(results: dict, halted: bool, halt_detail: str = "") -> None:
    """Write result.md per pre-reg section 10.3 11-section template."""
    n_bins = results.get("n_bins", 4)
    applied_optA = results.get("applied_optA", False)
    bin_labels = BIN_LABELS_4BIN if n_bins == 4 else BIN_LABELS_3BIN
    midpoints_for_spline = (BIN_MIDPOINTS_FOR_SPLINE_4BIN if n_bins == 4
                            else BIN_MIDPOINTS_FOR_SPLINE_3BIN)

    if halted:
        verdict_str = "HALT (sanity gate failure outside halt-option-A scope)"
    else:
        v = results["primary"]["verdict"]
        verdict_str = v["verdict_label"]
    lines: list[str] = []
    # --- Title + Authorship ---
    lines.append(f"# HA-C3 v2 r2 RESULT: {verdict_str}")
    lines.append("")
    lines.append("## Authorship")
    lines.append("")
    lines.append(
        f"Drafted 2026-06-23 by Claude (Opus 4.7, 1M context) in producer-mode "
        f"under user authorisation per "
        f"[CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default). "
        f"Authorising user: Willem. Pre-reg v2 r2 LOCKED 2026-06-23 at commit "
        f"`{V2_R2_SPEC_COMMIT}`. Test execution session per "
        f"[`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock).")
    lines.append("")
    lines.append(
        "**v1 lineage**: HA-C3 v1 r2 LOCKED 2026-06-23 at `de22b68` "
        "(archived as `hypothesis-v1-archived.md`); test-executed 2026-06-23 "
        "at `a9423af` and **HALTed on §7.5 Gate 1** because B1 [0,20) had "
        "n=0 on this corpus (`all_day_stress_avg` never falls below 20 in "
        "Stratum 4 unmedicated pool). Per "
        "[`hypothesis_lock_process §10.4 step 3`](../../../methodology/hypothesis_lock_process.md#104-five-stage-arc-iteration-policy) "
        "no-iteration-post-dry-run discipline, the v2 redraft created the new "
        "bin spec `[0,30), [30,40), [40,60), [60,100]` with the Wiggers verbatim "
        "30→40 anchor preserved at the new B2-B3 boundary, plus §7.3 halt-"
        "option-A PRE-COMMITTED for B4. This is a CLEAN RETEST at the revised "
        "bin spec; the v1 partial-pool trajectory (B2-B3-B4 = 3.958 → 4.265 → "
        "3.860 across v1 bins) enters as §8 caveat 9 caveat-class prior per "
        "[CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no), "
        "NOT promoted to a substantive v2 output.")
    lines.append("")
    if applied_optA:
        lines.append(
            "**§7.3 halt-option-A APPLIED (PRE-COMMITTED absorb)**: B4 [60,100] "
            "had n < 30 at dry-run; per the LOCKED v2 r2 spec §7.3, B3 [40,60) "
            "was automatically widened to absorb B4, producing the 3-bin "
            "reduction `{B1 [0,30), B2 [30,40), B3' [40,100]}`. The test runs "
            "on the 3-bin reduction with the contrast reduced to a single "
            "second-difference `S = m_3 − 2·m_2 + m_1` and the spline reduced "
            "to 2 internal knots at (30, 40); visual-gating count reduces to "
            "≥ 1 of 2 segment midpoints from {35, 70}. **This is NOT a halt** "
            "— the LOCKED spec PRE-COMMITS to this absorption.")
        lines.append("")
    if halted:
        lines.append(
            "**HALT outcome**: the §7.5 dry-run sanity gates failed in ways "
            "NOT absorbed by the PRE-COMMITTED §7.3 halt-option-A. Per §3.9 "
            "dry-run halt discipline + locked v2 r2 §10.4 step 1, the full "
            "test was NOT executed beyond the dry-run; a v3 redraft would be "
            "the recovery path (handled in a separate session).")
        lines.append("")

    # --- §1 What was tested ---
    lines.append("## §1 What was tested")
    lines.append("")
    bins_str = ", ".join(bin_labels)
    lines.append(
        f"**Headline cell** (per pre-reg §1 + §5.0): unmedicated (full LC era "
        f"through 2024-04-08) × full Stratum 4 single pool × `all_day_stress_avg` "
        f"binned at {{{bins_str}}} × `gevoelscore` bin-mean × "
        "{Jonckheere-Terpstra monotone-decreasing + second-difference convexity "
        "contrast S + spline non-linearity F-test with sign-gated second-"
        "derivative check} × block-permutation null at E[L]=7 × 3-condition "
        "gated verdict per §5.1.")
    lines.append("")
    lines.append(
        "**Wiggers C3 verbatim claim** (PDF lines 1357-1368, Annual Stress "
        "Scores section): the stress → fatigue relationship is "
        "non-linear / convex — a 30 → 40 stress step costs more gevoelscore "
        "than the steps preceding it. **v2 preserves the verbatim 30→40 "
        "anchor at the new B2-B3 boundary**. Tested as the bin-mean trajectory "
        "should be **monotone-decreasing** AND **convex** (accelerating "
        "decrement at higher stress bins).")
    lines.append("")
    lines.append("**3-condition gated verdict per §5.1**:")
    lines.append("")
    lines.append("| outcome | condition status | verdict |")
    lines.append("|---|---|---|")
    lines.append("| (a) MET AND (b) MET AND (c) MET | 3-of-3 | **SUPPORTED** |")
    lines.append("| Exactly 2-of-3 MET | 2-of-3 | **PARTIAL** |")
    lines.append("| ≤ 1-of-3 MET | 0/1-of-3 | **REJECTED** |")
    lines.append("| Any wrong-direction firing | override | **REJECTED** |")
    lines.append("")
    lines.append(
        "**STROBE-Item-12 forward-reference** (per pre-reg §1 + §8 caveat 7): "
        "operationalised measures sourced per [DATA_DICTIONARY](../../../DATA_DICTIONARY.md) "
        "§C (`all_day_stress_avg`) + §S (`gevoelscore`); computation paths "
        "traceable to [pipeline](../../../pipeline/).")
    lines.append("")

    # --- §2 Data + descriptives ---
    lines.append("## §2 Data + descriptives")
    lines.append("")
    s_med = results["sanity"]["stress_median"]
    g_med = results["sanity"]["gevoelscore_median"]
    lines.append(
        f"Primary unmedicated pool (post-§4.3 day-validity gate): "
        f"n = **{results['sanity']['total_n']}**. Stress median: "
        f"**{s_med:.2f}**. Gevoelscore median: **{g_med:.2f}**.")
    lines.append("")
    lines.append("### 4-bin descriptive sanity (pre-§7.3 absorption check)")
    lines.append("")
    lines.append("| bin | label | n | bin-mean gevoelscore | bin-median |")
    lines.append("|---|---|---:|---:|---:|")
    sanity_orig_for_md = results.get("sanity_original", results["sanity"])
    for b in range(4):
        m = sanity_orig_for_md["bin_mean"][b]
        md = sanity_orig_for_md["bin_median"][b]
        lines.append(
            f"| B{b+1} | {BIN_LABELS_4BIN[b]} | "
            f"{sanity_orig_for_md['bin_n'][b]} | "
            f"{f'{m:.3f}' if m is not None else 'NA'} | "
            f"{f'{md:.2f}' if md is not None else 'NA'} |")
    lines.append("")
    if applied_optA:
        lines.append(
            "**Note**: B4 underpower triggered §7.3 halt-option-A "
            "PRE-COMMITTED absorb at dry-run; subsequent test runs on the "
            "3-bin reduction below.")
        lines.append("")
        lines.append("### 3-bin reduction descriptives (post-§7.3 absorption)")
        lines.append("")
        lines.append("| bin | label | n | bin-mean gevoelscore |")
        lines.append("|---|---|---:|---:|")
        for b in range(n_bins):
            n_b = results["primary"]["bin_n"][b]
            m_b = results["primary"]["bin_mean"][b]
            lines.append(
                f"| B{b+1} | {BIN_LABELS_3BIN[b]} | {n_b} | "
                f"{f'{m_b:.3f}' if m_b is not None else 'NA'} |")
        lines.append("")

    # --- §3 Primary test result ---
    lines.append("## §3 Primary test result")
    lines.append("")
    if halted:
        lines.append(
            "**HALT**: primary test was not executed because the §7.5 sanity "
            "gates failed at the pre-committed bin specification. Per §3.9 "
            "dry-run halt discipline, no primary statistics were computed.")
        lines.append("")
        lines.append(f"**Halt detail (machine-readable)**: {halt_detail}")
        lines.append("")
    else:
        p = results["primary"]["perm"]
        v = results["primary"]["verdict"]
        obs = p["obs"]
        lines.append(f"Per pre-reg §4.5.1 + §4.7 block-permutation at E[L]=7 "
                     f"(B = {B_HEADLINE} draws, seed = {RANDOM_SEED}).")
        lines.append("")
        lines.append("| condition | statistic | observed | one-sided p | "
                     "direction OK | bar (p<0.05) | MET |")
        lines.append("|---|---|---:|---:|:---:|:---:|:---:|")
        j_obs = obs["J_star"]
        s_obs = obs["S"]
        sf_obs = obs.get("spline_F_continuous_predictor")
        if n_bins == 4:
            s_label = "S = mean(D²_2, D²_3)"
        else:
            s_label = "S = D²_2 = m_3 − 2·m_2 + m_1"
        lines.append(
            f"| (a) Jonckheere-Terpstra (monotone-decreasing) | J* (standardised) | "
            f"{j_obs:+.4f} | {v['p_a']:.4f} | "
            f"{'YES' if v['a_direction_ok'] else 'NO'} | "
            f"{'PASS' if v['p_a'] < P_BAR else 'fail'} | "
            f"{'**PASS**' if v['a_met'] else 'fail'} |")
        lines.append(
            f"| (b) Second-difference convexity | {s_label} | "
            f"{s_obs:+.4f} | {v['p_b']:.4f} | "
            f"{'YES (S<0)' if v['b_direction_ok'] else 'NO (S>=0)'} | "
            f"{'PASS' if v['p_b'] < P_BAR else 'fail'} | "
            f"{'**PASS**' if v['b_met'] else 'fail'} |")
        sf_str = f"{sf_obs:+.4f}" if sf_obs is not None else "NA"
        midpoints_str = "/".join(str(int(x)) for x in midpoints_for_spline)
        lines.append(
            f"| (c) Spline non-linearity ({len(midpoints_for_spline)} "
            f"segment midpoints: x={midpoints_str}) | F (continuous predictor) | "
            f"{sf_str} | {v['p_c']:.4f} | "
            f"{'YES' if v['c_direction_ok'] else 'NO'} "
            f"({v['spline_neg_count']} of {v['spline_total_midpoints']} "
            f"midpoints negative; bar ≥ {v['spline_count_bar']}) | "
            f"{'PASS' if v['p_c'] < P_BAR else 'fail'} | "
            f"{'**PASS**' if v['c_met'] else 'fail'} |")
        # Companion (descriptive)
        c_obs = obs["companion_contrast"]
        c_p = p["p_values"]["p_companion_orthogonal_quadratic"]
        if n_bins == 4:
            c_lbl = "c·m, c=(+1,−1,−1,+1)"
        else:
            c_lbl = "c·m, c=(+1,−2,+1)"
        lines.append(
            f"| (d) Companion orthogonal quadratic (descriptive) | "
            f"{c_lbl} | {c_obs:+.4f} | {c_p:.4f} | n/a | n/a | n/a |")
        lines.append("")
        lines.append(f"**Aggregate 3-condition verdict: "
                     f"{v['verdict_label']}**")
        if v["wrong_direction_fired"]:
            lines.append("")
            lines.append("**Wrong-direction overrides** fired:")
            for n in v["wrong_direction_notes"]:
                lines.append(f"- {n}")
        # Spline second-derivative values
        sd_vals = results["primary"]["spline_second_derivative_at_midpoints"]
        sd_x = results["primary"]["spline_midpoint_x_values"]
        lines.append("")
        lines.append("**Spline second-derivative at segment midpoints**:")
        lines.append("")
        lines.append("| midpoint x | spline second-derivative | sign |")
        lines.append("|---:|---:|:---:|")
        for x, val in zip(sd_x, sd_vals):
            sign_str = "—" if val is None else ("NEG" if val < 0
                                                  else ("POS" if val > 0
                                                        else "0"))
            val_str = "NA" if val is None else f"{val:+.5f}"
            lines.append(f"| {x:.0f} | {val_str} | {sign_str} |")
        lines.append("")
        # Parametric F (descriptive only)
        pf = p["parametric_F_descriptive"]
        lines.append(
            f"*Spline parametric F (descriptive only per pre-reg §4.5.1(c)): "
            f"F = {pf['F'] if pf['F'] is not None else 'NA'}, "
            f"parametric p = {pf['p_parametric'] if pf['p_parametric'] is not None else 'NA'}.*")
        lines.append("")
        lines.append("**Bin-means (primary)**:")
        lines.append("")
        lines.append("| bin | n | mean | 95% CI (stationary bootstrap "
                     "E[L]=7, B=1000) |")
        lines.append("|---|---:|---:|---|")
        for b in range(n_bins):
            n_b = results["primary"]["bin_n"][b]
            m_b = results["primary"]["bin_mean"][b]
            ci_lo, ci_hi = results["primary"]["bin_ci_95"].get(
                f"B{b+1}", (None, None))
            ci_str = (f"[{ci_lo:.3f}, {ci_hi:.3f}]"
                      if (ci_lo is not None and ci_hi is not None)
                      else "NA")
            lines.append(f"| B{b+1} ({bin_labels[b]}) | {n_b} | "
                         f"{f'{m_b:.3f}' if m_b is not None else 'NA'} | "
                         f"{ci_str} |")
        lines.append("")
        # Pairwise Mann-Whitney + Holm
        n_pairs = n_bins - 1
        lines.append(f"**Pairwise adjacent-bin Mann-Whitney + Holm step-down "
                     f"({n_pairs} pairs; descriptive, secondary)**:")
        lines.append("")
        lines.append("| pair | n_i | n_j | U | raw p | Holm threshold | "
                     "Holm-adj p | Holm-rejected |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|:---:|")
        for pp in results["primary"]["pairwise_mann_whitney"]:
            u_str = f"{pp['U']:.0f}" if pp.get("U") is not None else "NA"
            p_str = (f"{pp['p_two_sided']:.4f}"
                     if pp.get("p_two_sided") is not None else "NA")
            th_str = (f"{pp['holm_threshold']:.4f}"
                      if pp.get("holm_threshold") is not None else "NA")
            ad_str = (f"{pp['holm_adjusted_p']:.4f}"
                      if pp.get("holm_adjusted_p") is not None else "NA")
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
            f"{sr['rho']:.4f} (p = {sr['p']:.4g}, n = {sr['n']}). Reading: "
            "a positive Spearman alongside a failing convexity test would "
            "indicate roughly linear-or-concave monotone-decreasing — i.e. "
            "against C3.")
        lines.append("")

    # --- §4 §4.4 citalopram approach results (§5.A unmed + §5.B dose-adj) ---
    lines.append("## §4 §4.4 citalopram approach results")
    lines.append("")
    if halted:
        lines.append("Citalopram-approach sensitivity arms not executed because "
                     "the primary test halted on §7.5 sanity gates.")
        lines.append("")
    else:
        lines.append("### §5.A unmedicated headline (PRIMARY)")
        lines.append("")
        lines.append(
            "Per §4.4 LOCKED + Locked decision 8: the §5.A unmedicated phase "
            "headline IS the primary cell reported in §3 above. CONFIRMED-"
            "channel inheritance per [`citalopram_phase_stratification §4`](../../../methodology/citalopram_phase_stratification.md#4-per-channel-inheritance-rules): "
            "`all_day_stress_avg` is dose-modulated at +0.57/mg per "
            "[`citalopram_dose_response §5.6.1`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read); "
            "§5.A per-phase stratification with the unmedicated phase as the "
            "headline pool is the load-bearing choice. **No separate §5.A "
            "result is reported; §3 above IS the §5.A result**.")
        lines.append("")
        lines.append("### §5.B dose-adjusted cross-phase sensitivity arm")
        lines.append("")
        s5B = results["sensitivity_5B"]
        v5B = s5B["verdict"]
        lines.append(
            f"Per §4.4 + Locked decision 8: §5.B cross-phase test with "
            f"predictor adjusted as `all_day_stress_avg − {DOSE_BETA_PER_MG}/mg "
            f"× dose_plasma_mg(d)` per [`citalopram_phase_stratification §5.B`](../../../methodology/citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests).")
        lines.append("")
        lines.append(
            f"- Pool n = {s5B['pool_n']}; n_bins = {s5B['n_bins_used']}; "
            f"optA_applied = {s5B['optA_applied']}; bin-n = {s5B['bin_n']}; "
            f"bin-mean = {[None if m is None else round(m, 3) for m in s5B['bin_mean']]}.")
        lines.append(
            f"- **Verdict (descriptive, NOT promoted to primary)**: "
            f"**{v5B.get('verdict_label', 'NA')}**.")
        lines.append("")
        # Within-consolidation
        consol = results["sensitivity_within_consolidation"]
        lines.append("### Within-consolidation §5.A replication (§4.4 secondary)")
        lines.append("")
        lines.append(f"- Pool n = {consol['n']}; bin-n (initial 4-bin) = "
                     f"{consol['bin_n']}.")
        if consol['optA_applied']:
            lines.append(
                f"- §7.3 halt-option-A APPLIED recursively on the "
                f"consolidation arm (B3 absorbed B4); bin-n after = "
                f"{consol['bin_n_after_optA']}; n_bins_used = "
                f"{consol['n_bins_used']}.")
        lines.append(f"- **Verdict (descriptive, NOT promoted)**: "
                     f"**{consol['verdict']}**.")
        lines.append("")

    # --- §5 Sensitivity arms (per §4.8) ---
    lines.append("## §5 Sensitivity arms (per §4.8; descriptive, no verdict weight)")
    lines.append("")
    if halted:
        lines.append("Sensitivity arms not executed because the primary test "
                     "halted on §7.5 sanity gates.")
        lines.append("")
    else:
        # Crash-drop
        cd = results["sensitivity_crash_drop"]
        lines.append("### §4.6 Crash-drop sensitivity (CONVENTIONS §3.4)")
        lines.append("")
        s_full_str = f"{cd['S_full']:+.4f}" if cd["S_full"] is not None else "NA"
        s_nocr_str = (f"{cd['S_no_crash']:+.4f}"
                      if cd["S_no_crash"] is not None else "NA")
        d_std_str = (f"{cd['delta_standardised']:.4f}"
                     if cd["delta_standardised"] is not None else "NA")
        lines.append(f"- S (full) = {s_full_str} (n = {cd['n_full']}); "
                     f"S (no-crash) = {s_nocr_str} (n = {cd['n_no_crash']}).")
        lines.append(f"- |Δ S| standardised = {d_std_str}; "
                     f"sign-change = {cd['sign_change']}; flag = "
                     f"{'**FLAG**' if cd['flag'] else 'ok'}.")
        lines.append(
            "- Per pre-reg §4.6 + CONVENTIONS §3.4: flag is informative "
            "for interpretation; does NOT modify the §5.1 verdict.")
        lines.append("")
        # Train/validate
        ov = results["sensitivity_train_validate_overlay"]
        lines.append("### §4.8 Train/validate M3 descriptive overlay")
        lines.append("")
        train_S_str = f"{ov['train_S']:+.4f}" if ov['train_S'] is not None else "NA"
        validate_S_str = f"{ov['validate_S']:+.4f}" if ov['validate_S'] is not None else "NA"
        lines.append(
            f"- Train (≤ 2023-12-31): n = {ov['train_n']}; "
            f"bin-n = {ov['train_bin_n']}; bin-mean = "
            f"{[None if m is None else round(m, 3) for m in ov['train_bin_mean']]}; "
            f"S = {train_S_str}.")
        lines.append(
            f"- Validate (2024-01-01 → 2024-04-08): n = {ov['validate_n']}; "
            f"bin-n = {ov['validate_bin_n']}; bin-mean = "
            f"{[None if m is None else round(m, 3) for m in ov['validate_bin_mean']]}; "
            f"S = {validate_S_str}.")
        lines.append("- Per `train_validate_split_fate.md`: divergence is "
                     "a number, not a narrative; no per-era verdicts.")
        lines.append("")
        # Lagged
        lg = results["sensitivity_lagged_t_plus_1"]
        lines.append("### §4.8 t+1 lagged variant (gevoelscore[T+1] on stress[T])")
        lines.append("")
        s_lag_str = f"{lg['S']:+.4f}" if lg['S'] is not None else "NA"
        lines.append(f"- n = {lg['n']}; bin-n = {lg['bin_n']}; bin-mean = "
                     f"{[None if m is None else round(m, 3) for m in lg['bin_mean']]}; "
                     f"S = {s_lag_str}.")
        lines.append("")

    # --- §6 Sister-test cross-reference table ---
    lines.append("## §6 Sister-test cross-reference (descriptive context per §8 caveat 12)")
    lines.append("")
    lines.append("| sister test | verdict | one-line context | commit |")
    lines.append("|---|---|---|---|")
    lines.append(
        "| **HA-C3p** (personal-baseline-anchored sister; equal-N quintile bins) | "
        "**verdict pending; consolidation in HA-C3p result.md §6 4-cell agreement matrix** | "
        "personal-baseline equal-N quintile bins on full Stratum 4 pool; running in "
        "parallel session; 4-cell agreement matrix lives in HA-C3p result.md §6 "
        "per LOCKED HA-C3p decision | `c0148ca` (LOCKED) |")
    lines.append(
        "| HA-C4 v2 | **REJECTED** | daily-aggregate triad sum 0.0/3.0; Ch1+Ch2 "
        "validate SUPPORTED but train REFUTED -> mixed-era cancellation | `52bddb5` |")
    lines.append(
        "| HA-C4c | **PARTIAL** | bout-level recovery dynamics; bar (a) PASS "
        "p=0.0001 / bar (b) FAIL δ=+0.120 at cross-phase-pooled n=465/n=809; "
        "weak-effect-but-real positive pattern | `a69a8ed` |")
    lines.append(
        "| HA-P6 | (informational) | per cross-test register; substantively "
        "distinct from C3 daily-aggregate shape | -- |")
    lines.append(
        "| HA11 v1 | SUPPORTED-on-train | within-day U-dip count +22.8 pp "
        "(calm-day sister channel); structurally distinct from cross-day-"
        "aggregate shape | (per register) |")
    lines.append("")
    lines.append(
        "**Reading**: HA-C3 v2 tests Wiggers' verbatim 30→40 numerical anchor "
        "on the v2 4-bin scheme (or 3-bin reduction post-§7.3 absorption). "
        "The sister pre-reg HA-C3p tests the underlying convex-shape mechanism "
        "on personal-baseline-anchored quintile bins per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds). "
        "The 4-cell agreement matrix between HA-C3 v2 and HA-C3p verdicts is "
        "consolidated in HA-C3p result.md §6 by the dispatcher post-parallel-"
        "session completion; this result.md does NOT populate that matrix.")
    lines.append("")

    # --- §7 §4.7 E[L]* report (factor-of-2 flag) ---
    lines.append("## §7 §4.7 E[L]* report (factor-of-2 flag)")
    lines.append("")
    if halted:
        lines.append("Not run (primary halted).")
        lines.append("")
    else:
        el = results["el_star"]
        lines.append("Per pre-reg §4.7 r2 amendment: two data-driven E[L]* "
                     "checks (linear-residual + bin-label) per "
                     "[`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md).")
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
        any_flag = (el["linear_residual"]["flagged_deviation"]
                    or el["bin_label"]["flagged_deviation"])
        v = results["primary"]["verdict"]["verdict"]
        if any_flag and v == "SUPPORTED":
            lines.append("**Flag fires on verdict-relevant cell** (verdict is "
                         "SUPPORTED). Per `permutation_null_block_length.md` "
                         "the flag suggests the E[L]=7 default may be "
                         "mis-calibrated; report as caveat.")
        elif any_flag:
            lines.append("Flag fires but verdict is not SUPPORTED; descriptive "
                         "context only per `permutation_null_block_length.md`.")
        else:
            lines.append("No flags.")
        lines.append("")

    # --- §8 Caveats (per pre-reg §8; surfaced prominently) ---
    lines.append("## §8 Caveats (per pre-reg §8; surfaced prominently)")
    lines.append("")
    lines.append(
        "1. **Power-calc dispatch**: inapplicable per Daza 2018 within-subject "
        "n-of-1 design ([within-subject Methods Inf Med citation](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)). "
        "Block-permutation null at E[L]=7 is the within-subject inferential "
        "machinery; the 3-condition gated verdict is the decision rule. "
        "INCONCLUSIVE per §5.2 is the operational definition of 'underpowered "
        "for this cell'.")
    lines.append(
        "2. **n=1 single-subject caveats** per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-population-norm): "
        "thresholds (p<0.05; S<0; spline 2nd-deriv negative at ≥ "
        f"{SPLINE_MIDPOINT_COUNT_BAR_4BIN if n_bins == 4 else SPLINE_MIDPOINT_COUNT_BAR_3BIN} "
        f"of {len(midpoints_for_spline)} segment midpoints) calibrated to "
        "the participant's distribution. No cross-subject generalisation.")
    lines.append(
        f"3. **Citalopram-channel inheritance**: `all_day_stress_avg` is "
        f"CONFIRMED dose-modulated at +{DOSE_BETA_PER_MG}/mg "
        f"([dose-response §5.6.1](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read)). "
        f"Primary uses §5.A per-phase stratification (unmedicated headline); "
        f"§5.B dose-adjusted is cross-phase sensitivity. §4 above.")
    lines.append(
        "4. **Crash-day inclusion structural fragility** per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-for-correlations-and-regressions): "
        "crashes KEPT in primary; §4.6 crash-drop arm flagged if "
        f"|Δ S| > {CRASH_DROP_STANDARDISED_THRESHOLD:.2f} standardised OR "
        "sign-change. §5 above. Flag is informative; does NOT modify §5.1 "
        "verdict.")
    lines.append(
        "5. **Within-subject shape, NOT between-subject prediction**: the "
        "convex stress→fatigue claim is about THIS participant's mapping; "
        "no cross-person generalisation claimed.")
    lines.append(
        "6. **No causal-direction inference**: the test answers \"does the "
        "mapping have a convex shape?\" — it does NOT answer \"does stress "
        "CAUSE fatigue?\". Per [CONVENTIONS §4.1-§4.3](../../../CONVENTIONS.md#4-statistical-discipline): "
        "descriptive characterisation of mapping shape, not causal claim.")
    lines.append(
        "7. **v2 scope is corpus-stress-range AS-REPRESENTED, NOT Wiggers' "
        "abstract register range** (NEW in v2 per the v1 HALT lineage). "
        "v1 r2 was test-executed and HALTed at §7.5 Gate 1 because B1 [0,20) "
        "had n = 0 on the unmedicated pool. v2 responds by collapsing v1's "
        "B1 [0,20) into v1's B2 [20,30) to form v2's new B1 [0,30). The v2 "
        "verdict scope is therefore the corpus-represented stress range "
        "(effectively [20, 100]), NOT the abstract Wiggers register range. "
        "A SUPPORTED v2 verdict would mean: the convex shape is empirically "
        "confirmed on this participant's `all_day_stress_avg` distribution "
        "AS REPRESENTED, with the explicit caveat that the low-stress "
        "register (< 20) is structurally absent and therefore not tested. "
        "**STROBE-Item-12 source-file traceability inventory**: operationalised "
        "measures sourced per [DATA_DICTIONARY](../../../DATA_DICTIONARY.md) §C + §S; "
        "computation paths traceable to [pipeline](../../../pipeline/) per "
        "CONVENTIONS STROBE-Item-12 inheritance.")
    lines.append(
        "8. **Wiggers' phrasing is qualitative**: the (0-30, 30-40, 40-60, "
        "60+) binning is OUR operationalisation; a REJECTED verdict at "
        "these specific bins does NOT universally falsify the qualitative "
        "stair-step framing per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no).")
    lines.append(
        "9. **v1 partial-pool non-monotone trajectory as caveat-class prior "
        "informing v2 interpretation** (NEW in v2). v1's HALT-time partial-"
        "pool descriptive trajectory across the 3 populated bins was "
        "**B2-B3-B4 = 3.958 → 4.265 → 3.860**, peak at v1 B3 = stress 30-40, "
        "**non-monotone** at the descriptive level. This is a **caveat-class "
        "prior informing v2 interpretation, NOT a quasi-result and NOT a "
        "substantive v2 output**. v2 does NOT pre-commit to an inverted-U / "
        "threshold-pattern alternative claim; promoting that observation to "
        "a SUPPORTED-of-inverted-U claim would require a separate §3.2 "
        "fresh-session redraft to HA-C3-v3 with the alternative-shape claim "
        "as the primary.")
    lines.append(
        "10. **Independent-obligations block** per [`citalopram_phase_stratification §6`](../../../methodology/citalopram_phase_stratification.md#6-pre-registration-template-for-new-hypothesis-mds) — "
        "autocorrelation (§4.7) + crash-drop (§4.6) + spike-companion (N/A; "
        "HA-C3 is the cross-day-aggregate test, not within-day) + trajectory-"
        "detrend (N/A; not a pre-vs-post comparison) all handled per §4.")
    lines.append(
        "11. **Drafting-context disclosure** (NEW in v2 + operational "
        "consequence in v2 r2): v2 r1 was drafted in a fresh worktree-isolated "
        "session 2026-06-23. The drafter had seen v1 partial-pool descriptives "
        "(pool n=581, stress median 34, gevoelscore median 4, populated-bins "
        "trajectory 3.958 → 4.265 → 3.860); the §4.1 v2 bin spec was chosen "
        "with knowledge of this distribution. **Operational consequence per "
        "[CONVENTIONS §4.3](../../../CONVENTIONS.md#43-confirmatory-vs-exploratory-distinction)**: "
        "the substantive Wiggers C3 convex-shape question stays **confirmatory** "
        "per the source-verified prior (Wiggers PDF 1357-1368); the v2 "
        "**operationalisation choice** (4-bin scheme collapsing v1's empty B1 "
        "into the new low-stress bin) is **exploratory-with-caveat** per the "
        "corpus-conditional redraft trigger. The distinction matters for §5.1 "
        "verdict interpretation: SUPPORTED supports the confirmatory question; "
        "PARTIAL or REJECTED carries the additional operationalisation-choice "
        "uncertainty.")
    lines.append(
        "12. **Sister-test cross-references** (extended in v2 r2): HA-C4 v2 "
        "REJECTED + HA-C4c PARTIAL + HA11 SUPPORTED-on-train are sister "
        "Wiggers-cluster results at structurally-distinct operationalisations; "
        "no direct cross-test prior import on the convex-shape claim. "
        "**Sister pre-reg [HA-C3p](../HA-C3p/hypothesis.md)** is the "
        "personal-baseline operationalisation per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-population-norm) "
        "(equal-N quintile bins on the participant's `all_day_stress_avg` "
        "distribution); HA-C3p tests the underlying convex-shape claim on "
        "the participant's actual stress range, while HA-C3 v2 tests Wiggers' "
        "verbatim 30→40 numerical anchor. The 4-cell agreement matrix lives "
        "in HA-C3p result.md §6.")
    lines.append("")

    # --- §9 Downstream actions (per pre-reg §9) ---
    lines.append("## §9 Downstream actions (per pre-reg §9 verdict branch)")
    lines.append("")
    if halted:
        lines.append("**HALT branch**: v3 spec redraft required (out of "
                     "scope for this session).")
        lines.append("")
    else:
        v = results["primary"]["verdict"]["verdict"]
        if v == "SUPPORTED":
            lines.append(
                "**§9.1 SUPPORTED branch**: the Wiggers C3 verbatim claim is "
                "empirically confirmed at the corpus-stress-range-AS-"
                "REPRESENTED scope per §8 caveat 7. Downstream implications: "
                "high-stress days carry disproportionate cost; stress-budgeting "
                "models for pacing-behaviour analyses should treat the high-"
                "stress register as carrying convex (not linear) cost; budget-"
                "allocation heuristics that linearly weight stress-units are "
                "mis-specified for this participant within the corpus-"
                "represented range. Scope-limited confirmation per §8 "
                "caveat 7. No causal direction claim per §8 caveat 6.")
        elif v == "PARTIAL":
            lines.append(
                "**§9.2 PARTIAL branch** (2-of-3 conditions MET): "
                "descriptively informative but does NOT carry the SUPPORTED-"
                "bar weight for downstream pacing-behaviour analytic claims. "
                "The §3 verdict table above names which 2 of 3 conditions "
                "fired; see pre-reg §9.2 for the three operationally "
                "distinguishable PARTIAL configurations.")
        else:  # REJECTED
            lines.append(
                "**§9.3 REJECTED branch**: the C3 verbatim claim is NOT "
                "empirically confirmed at the chosen v2 operationalisation "
                "within the §8 caveat 7 scope. See pre-reg §9.3 for the "
                "three distinguishable REJECTED configurations (wrong-"
                "direction firings; 0/1 conditions met). Under the 0-or-1-"
                "conditions branch with no wrong-direction firing, the mapping "
                "is roughly linear-or-flat OR non-monotone in the v1-partial-"
                "pool-trajectory direction. **Cross-reference downstream**: "
                "HA-C3 v2 REJECTED + HA-C4 v2 REJECTED would mean the Wiggers "
                "C-family at daily-aggregate is exhaustively-tested-and-not-"
                "supported on this corpus.")
        lines.append("")

    # --- §10 §7.5 dry-run gate results table ---
    lines.append("## §10 §7.5 dry-run gate results")
    lines.append("")
    lines.append("| gate | description | result |")
    lines.append("|---|---|---|")
    bin_n_sanity = results["sanity"]["bin_n"]
    gate1_str = "PASS" if all(n >= MIN_BIN_N for n in bin_n_sanity) else (
        "**§7.3 halt-option-A absorbed**" if applied_optA
        else "FAIL")
    lines.append(f"| 1 | per-bin n >= {MIN_BIN_N} (4 bins) | {gate1_str} |")
    s_med_pass = (GATE2_STRESS_MEDIAN_RANGE[0] <=
                  results["sanity"]["stress_median"] <=
                  GATE2_STRESS_MEDIAN_RANGE[1])
    lines.append(f"| 2 | stress median in {list(GATE2_STRESS_MEDIAN_RANGE)} | "
                 f"{'PASS' if s_med_pass else 'FAIL'} |")
    g_med_pass = (GATE3_GEVOELSCORE_MEDIAN_RANGE[0] <=
                  results["sanity"]["gevoelscore_median"] <=
                  GATE3_GEVOELSCORE_MEDIAN_RANGE[1])
    lines.append(f"| 3 | gevoelscore median in {list(GATE3_GEVOELSCORE_MEDIAN_RANGE)} | "
                 f"{'PASS' if g_med_pass else 'FAIL'} |")
    n_ge_30 = sum(1 for n in bin_n_sanity if n >= MIN_BIN_N)
    gate4_pass = n_ge_30 >= 2 and sum(bin_n_sanity) >= MIN_TOTAL_N
    lines.append(f"| 4 | >= 2 bins n>=30 AND total n>={MIN_TOTAL_N} | "
                 f"{'PASS' if gate4_pass else 'FAIL'} |")
    lines.append("")
    if applied_optA:
        lines.append("**§7.3 halt-option-A status**: **TRIGGERED at dry-run "
                     "as PRE-COMMITTED** — B4 [60,100] underpower (n < 30) "
                     "auto-absorbed into B3 [40,60), producing 3-bin "
                     "reduction `{B1 [0,30), B2 [30,40), B3' [40,100]}`. Per "
                     "the LOCKED v2 r2 spec §7.3 this is NOT a halt.")
        lines.append("")

    # --- §11 Reproducibility ---
    lines.append("## §11 Reproducibility")
    lines.append("")
    lines.append("- **Script**: `docs/research/analyses/hypotheses/HA-C3/test.py`")
    lines.append("- **Environment variable**: `GEVOELSCORE_DATA_PATH` "
                 "(default: `C:\\Users\\Gebruiker\\Documents\\gevoelscore-data`)")
    lines.append(f"- **Seed**: `RANDOM_SEED = {RANDOM_SEED}`")
    lines.append(f"- **Bootstrap**: B = {B_HEADLINE} stationary-bootstrap "
                 f"draws per condition; E[L] = {BOOTSTRAP_E_L} (geometric "
                 f"block length).")
    lines.append("- **Regenerate command**: "
                 "`python docs/research/analyses/hypotheses/HA-C3/test.py`")
    lines.append("- **Dependencies**: numpy, scipy (`CubicSpline`, "
                 "`mannwhitneyu`, `spearmanr`, `f.sf`); project utility "
                 "`docs/research/analyses/_utils/inference.py` for "
                 "`compute_data_driven_block_length` + `holm_step_down`.")
    lines.append(f"- **Spec commit**: `{V2_R2_SPEC_COMMIT}` (LOCKED 2026-06-23)")
    lines.append("- **Machine-readable companion**: `result-data.json` "
                 "(gitignored per `docs/research/**/*.json`).")
    lines.append("- **Pipeline-trust**: `per_day_master.csv` snapshot read at "
                 "run-time from `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        f"*test.py run with `RANDOM_SEED = {RANDOM_SEED}`, "
        f"`BOOTSTRAP_E_L = {BOOTSTRAP_E_L}`, B = {B_HEADLINE} draws per "
        f"condition. Source: `per_day_master.csv` from "
        f"`$GEVOELSCORE_DATA_PATH`. Spec commit: `{V2_R2_SPEC_COMMIT}`.*")
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
    parser = argparse.ArgumentParser(description="HA-C3 v2 r2 test driver.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run spec section 10.4 step 1 dry-run only.")
    args = parser.parse_args()

    print(f"Loading master from {MASTER_CSV}...", file=sys.stderr)
    master = load_master()
    print(f"  {len(master)} day-rows loaded.", file=sys.stderr)
    baseline_cutoff = find_device_baseline_cutoff(master)

    # --- Dry-run on 4-bin scheme ---
    sanity = dry_run(master, baseline_cutoff)
    sanity_original = sanity  # preserve original 4-bin for write_dry_run_report; sanity may be reassigned to sanity_after_optA below

    # --- Detect halt-option-A trigger condition (B4 sole failure) ---
    applied_optA = False
    sanity_after_optA = None
    if sanity["verdict"] == "HALT":
        # Examine which gates failed; only auto-apply optA if B4-only Gate 1
        gate1_fails = [f for f in sanity["fails"]
                       if f.get("gate") == 1
                       and f.get("halt_optA_applicable")]
        other_fails = [f for f in sanity["fails"]
                       if not f.get("halt_optA_applicable")]
        sole_b4 = len(gate1_fails) == 1 and not other_fails
        if sole_b4:
            print("\n  spec section 7.3 halt-option-A APPLIED: widening B3 "
                  "to absorb B4 (PRE-COMMITTED at v2 r2 lock).",
                  file=sys.stderr)
            pool_3bin = apply_halt_optA(sanity["pool"], master,
                                         baseline_cutoff, phase="unmedicated")
            sanity_after_optA = run_sanity_gates(pool_3bin)
            sanity_after_optA["pool"] = pool_3bin
            applied_optA = True
            if sanity_after_optA["verdict"] == "HALT":
                halt_detail = ("section 7.3 halt-option-A applied but 3-bin "
                               f"reduction still fails sanity gates: "
                               f"{sanity_after_optA['fails']}")
                print(f"\n  HALT (post-optA): {halt_detail}", file=sys.stderr)
                write_dry_run_report(sanity, applied_optA=False)
                halted_results = {
                    "spec_commit": V2_R2_SPEC_COMMIT,
                    "n_bins": 4,
                    "applied_optA": False,
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
                write_result_md(halted_results, halted=True,
                                halt_detail=halt_detail)
                write_result_json(halted_results)
                sys.exit(1)
            # Use the 3-bin sanity going forward
            sanity = sanity_after_optA

    write_dry_run_report(
        sanity_original,
        applied_optA=applied_optA,
        sanity_after_optA=sanity_after_optA)

    if args.dry_run:
        sys.exit(0 if (sanity.get("verdict") == "PASS" or applied_optA) else 1)

    # Halt if dry-run fails outside section 7.3 scope
    if sanity.get("verdict") == "HALT" and not applied_optA:
        halt_detail = "Sanity gates failed in ways not absorbed by section 7.3 halt-option-A: "
        halt_detail += "; ".join(
            f"Gate {f['gate']} ({f['name']}): {f['detail']}"
            for f in sanity["fails"])
        print(f"\n  HALT: {halt_detail}", file=sys.stderr)
        halted_results = {
            "spec_commit": V2_R2_SPEC_COMMIT,
            "n_bins": 4,
            "applied_optA": False,
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
        write_result_json(halted_results)
        sys.exit(1)

    print("\nDry-run gates PASS (or section 7.3 halt-option-A absorbed); "
          "running full test...", file=sys.stderr)
    results = run_full(master, baseline_cutoff, sanity,
                       applied_optA=applied_optA,
                       sanity_original=sanity_original)
    write_result_md(results, halted=False)
    write_result_json(results)


if __name__ == "__main__":
    main()
