"""HA-P7 -- recent-crash-density predicts crash risk (test script).

Implements the locked spec in hypothesis.md Section 10.

Loads per_day_master.csv from $GEVOELSCORE_DATA_PATH/unified, computes
crash_count_W for W in {7, 14, 30}, applies Sec 4.2 eligibility, derives
the citalopram phase per Sec 4.4, runs the Sec 4.5 logistic regression
with stationary-bootstrap 95% CI at E[L]=7 + block-permutation null +
binned tabulation + Sec 4.5.4 covariate sensitivity + Sec 3.4-binding
descriptive same-day Spearman, evaluates Sec 5 falsification criteria,
and emits result.md.

Usage:
  python test.py --dry-run    # eligible-n + Sec 7 sanity checks
  python test.py              # full run + result.md emission
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
from scipy.optimize import minimize


# === Locked constants per hypothesis.md ============================

LC_START = date(2022, 4, 4)                  # Sec 3 LC era start
COVERAGE_START = date(2022, 9, 3)            # Sec 3 crash_v2 coverage start
TRAIN_END = date(2023, 12, 31)               # Sec 1 train cutoff
VALIDATE_END = date(2026, 6, 5)              # Sec 1 validate cutoff (= coverage end)
ANALYSIS_END = VALIDATE_END

WINDOWS = (7, 14, 30)                        # Sec 4.1
PRIMARY_W = 14
SECONDARY_FORWARD = 4                        # Sec 4.3 any_crash_in_next_4d

# Sec 4.4 citalopram phases (boundaries from methodology MD Sec 3)
PHASE_BUILDUP_START = date(2024, 4, 9)
PHASE_CONSOL_START = date(2024, 6, 20)
PHASE_AFBOUW_START = date(2026, 3, 20)
PHASE_POST_START = date(2026, 6, 6)

# Sec 6 exclusion buffers
BOUNDARY_CLUSTER_START = date(2024, 4, 9)
BOUNDARY_CLUSTER_END = date(2024, 4, 16)      # inclusive
BUILDUP_BUFFER_LAST_EXCLUDED = date(2024, 4, 29)   # strictly before 2024-04-30

# Sec 4.5 resampling policy (per methodology/permutation_null_block_length.md)
E_BLOCK_LEN = 7                              # expected block length, days
B_HEADLINE = 10000                           # bootstrap + permutation replicates for headline + W-arms
B_DIAGNOSTIC = 2000                          # bootstrap replicates for per-phase diagnostic arms
B_BIN = 10000                                # binned tabulation CI replicates
RANDOM_SEED = 20260615                       # Sec 4.5.3 -- HA-P7-specific

# Sec 5 SUPPORTED bar parameters
MIN_POOLED_N = 200                           # Sec 5.3
MIN_BIN_DAYS = 5                             # Sec 5.3
REL_TOL = 0.50                               # Sec 5.1(b) relative-50% monotonicity tolerance

# Sec 7 sanity-check thresholds
SANITY_BIN0_LOW = 0.005                      # very-low-rate flag (expect 2-5%)
SANITY_BIN0_HIGH = 0.20                      # very-high-rate flag (suggests labels broken)
SANITY_BIN3_FRAC_HIGH = 0.20                 # bin-3+ share of eligible days > 20% -> flag

# Sec 4.5.1 data-driven block-length flag threshold
EL_STAR_FLAG_FACTOR = 0.5                    # |E[L]*-7|/7 > 0.5 -> flag

HERE = Path(__file__).resolve().parent
# HA-P7 -> hypotheses -> analyses -> research -> docs -> repo root
REPO_ROOT = HERE.parent.parent.parent.parent.parent
OUT_JSON = HERE / "result-data.json"
OUT_MD = HERE / "result.md"


# === Helpers ========================================================

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


def era_of(d: date) -> str:
    if d <= TRAIN_END:
        return "train"
    return "validate"


def load_master() -> pd.DataFrame:
    load_env()
    data_path = os.environ.get("GEVOELSCORE_DATA_PATH")
    if not data_path:
        print("ERROR: GEVOELSCORE_DATA_PATH not set.", file=sys.stderr)
        sys.exit(2)
    csv_path = Path(data_path) / "unified" / "per_day_master.csv"
    if not csv_path.exists():
        print(f"ERROR: {csv_path} not found.", file=sys.stderr)
        sys.exit(2)
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["is_crash"] = df["is_crash"].astype(str).str.lower() == "true"
    if "gevoelscore" in df.columns:
        df["gevoelscore"] = pd.to_numeric(df["gevoelscore"], errors="coerce")
    df = df.sort_values("date").reset_index(drop=True)
    return df


# === Predictor / covariate / outcome construction ===================

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute crash_count_W for W in WINDOWS, any_crash_next_4d, and
    gevoelscore_lagged_mean_14d. Returns the frame with added columns.

    Each crash-day counts as 1 toward density (Sec 4.1: a 5-day crash
    contributes 5).
    """
    dates = df["date"].tolist()
    n = len(df)
    is_crash = df["is_crash"].to_numpy()
    score = df["gevoelscore"].to_numpy() if "gevoelscore" in df.columns else np.full(n, np.nan)
    date_to_idx = {d: i for i, d in enumerate(dates)}

    feat = {f"crash_count_{W}d": np.zeros(n, dtype=int) for W in WINDOWS}
    feat["any_crash_next_4d"] = np.zeros(n, dtype=bool)
    feat["gevoelscore_lagged_mean_14d"] = np.full(n, np.nan)

    for i, d in enumerate(dates):
        for W in WINDOWS:
            cnt = 0
            for k in range(1, W + 1):
                j = date_to_idx.get(d - timedelta(days=k))
                if j is not None and is_crash[j]:
                    cnt += 1
            feat[f"crash_count_{W}d"][i] = cnt
        any_next = False
        for k in range(0, SECONDARY_FORWARD):
            j = date_to_idx.get(d + timedelta(days=k))
            if j is not None and is_crash[j]:
                any_next = True
                break
        feat["any_crash_next_4d"][i] = any_next
        vals = []
        for k in range(1, 15):
            j = date_to_idx.get(d - timedelta(days=k))
            if j is not None:
                v = score[j]
                if not np.isnan(v):
                    vals.append(v)
        if vals:
            feat["gevoelscore_lagged_mean_14d"][i] = float(np.mean(vals))

    out = df.copy()
    for k, v in feat.items():
        out[k] = v
    return out


def eligibility_mask(df: pd.DataFrame, W: int, *, for_phase: bool, phase: str | None = None) -> np.ndarray:
    """Compute the Sec 4.2 + Sec 6 eligibility mask for window W.

    Pooled-headline mask: for_phase=False -> drops boundary cluster only.
    Per-phase mask: for_phase=True + phase=<name> -> drops boundary cluster
    AND restricts to dates within phase boundary AND drops buildup CPAP
    buffer 2024-04-09..2024-04-29 from the buildup phase (i.e. buildup
    phase eligibility is restricted to dates >= 2024-04-30).
    """
    n = len(df)
    dates = df["date"].tolist()
    is_crash = df["is_crash"].to_numpy()
    date_to_idx = {d: i for i, d in enumerate(dates)}

    elig = np.zeros(n, dtype=bool)
    for i in range(n):
        d = dates[i]
        # Sec 4.2 condition 3: d in coverage range
        if not (COVERAGE_START <= d <= ANALYSIS_END):
            continue
        # Sec 4.2 condition 4: window [d-W, d-1] fully within coverage
        if d - timedelta(days=W) < COVERAGE_START:
            continue
        # Sec 4.2 condition 2: is_crash[d-1] == False
        j_prev = date_to_idx.get(d - timedelta(days=1))
        if j_prev is None or is_crash[j_prev]:
            continue
        # Sec 6: boundary cluster excluded from POOLED + PHASE
        if BOUNDARY_CLUSTER_START <= d <= BOUNDARY_CLUSTER_END:
            continue
        # Sec 6: phase-stratified arm exclusions
        if for_phase:
            if phase is not None and citalopram_phase(d) != phase:
                continue
            if phase == "buildup" and d <= BUILDUP_BUFFER_LAST_EXCLUDED:
                continue
        elig[i] = True
    return elig


# === Logistic regression (fast custom fit) ==========================

def fit_logistic(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, bool]:
    """Fit logistic regression with intercept. X has shape (n, k) WITHOUT
    intercept column. Returns (beta of shape (k+1,), converged_flag).
    First element of beta is the intercept.
    """
    n, k = X.shape
    Xi = np.hstack([np.ones((n, 1)), X])

    def neg_ll(beta: np.ndarray) -> float:
        z = Xi @ beta
        return float((-y * z + np.logaddexp(0.0, z)).sum())

    def grad(beta: np.ndarray) -> np.ndarray:
        z = Xi @ beta
        p = 1.0 / (1.0 + np.exp(-z))
        return Xi.T @ (p - y)

    beta0 = np.zeros(k + 1)
    try:
        res = minimize(neg_ll, beta0, jac=grad, method="BFGS",
                       options={"maxiter": 200, "gtol": 1e-6})
        return res.x, bool(res.success)
    except Exception:
        return np.full(k + 1, np.nan), False


# === Resampling primitives ===========================================

def stationary_bootstrap_indices(n: int, expected_block_len: int, rng: np.random.Generator) -> np.ndarray:
    """Generate n indices via stationary bootstrap (Politis-Romano):
    block starts uniform on [0, n), block lengths ~ Geometric(1/E[L]),
    circular wrap-around.
    """
    p = 1.0 / expected_block_len
    out = np.empty(n, dtype=np.int64)
    filled = 0
    while filled < n:
        start = int(rng.integers(0, n))
        L = int(rng.geometric(p))
        L = min(L, n - filled)
        idx = (start + np.arange(L)) % n
        out[filled:filled + L] = idx
        filled += L
    return out


def block_permute_series(arr: np.ndarray, expected_block_len: int, rng: np.random.Generator) -> np.ndarray:
    """Permute arr by partitioning into contiguous blocks of geometric
    length and shuffling block order. Preserves within-block autocorrelation.
    """
    n = len(arr)
    p = 1.0 / expected_block_len
    lengths = []
    s = 0
    while s < n:
        L = int(rng.geometric(p))
        L = min(L, n - s)
        lengths.append(L)
        s += L
    starts = np.concatenate([[0], np.cumsum(lengths)[:-1]])
    order = list(range(len(lengths)))
    rng.shuffle(order)
    out = np.empty_like(arr)
    pos = 0
    for bi in order:
        L = lengths[bi]
        out[pos:pos + L] = arr[starts[bi]:starts[bi] + L]
        pos += L
    return out


# === Data-driven E[L]* estimator =====================================

def estimate_block_length(x: np.ndarray, max_lag: int = 60) -> float:
    """Pragmatic data-driven block-length estimator: L_hat = 1 + 2 * sum
    of significant ACF lags (|rho_h| outside the Bartlett band 2/sqrt(n)).
    """
    n = len(x)
    if n < 30:
        return float("nan")
    xc = x - x.mean()
    var = (xc ** 2).sum()
    if var == 0:
        return float("nan")
    band = 2.0 / np.sqrt(n)
    rhos = []
    for h in range(1, min(max_lag, n - 1) + 1):
        rho = (xc[:-h] * xc[h:]).sum() / var
        if abs(rho) < band:
            break
        rhos.append(rho)
    if not rhos:
        return 1.0
    return float(1.0 + 2.0 * sum(rhos))


# === Bootstrap CI for a logistic =====================================

def bootstrap_logit_ci(
    Xy: tuple[np.ndarray, np.ndarray],
    n_boot: int,
    rng: np.random.Generator,
    expected_block_len: int = E_BLOCK_LEN,
    coef_idx: int = 1,
) -> dict:
    """Stationary-bootstrap 95% percentile CI on beta_{coef_idx}
    (default beta_1) of a logistic regression with Xy = (X, y).
    """
    X, y = Xy
    n = len(y)
    pt_beta, pt_ok = fit_logistic(X, y)
    point = float(pt_beta[coef_idx]) if pt_ok else float("nan")

    betas = np.empty(n_boot)
    n_ok = 0
    for b in range(n_boot):
        idx = stationary_bootstrap_indices(n, expected_block_len, rng)
        beta, ok = fit_logistic(X[idx], y[idx])
        betas[b] = beta[coef_idx] if ok else np.nan
        if ok:
            n_ok += 1

    valid = betas[~np.isnan(betas)]
    if len(valid) < 100:
        return {"point": point, "ci_lo": float("nan"), "ci_hi": float("nan"),
                "n_converged": n_ok, "n_boot": n_boot}
    lo, hi = np.percentile(valid, [2.5, 97.5])
    return {"point": point, "ci_lo": float(lo), "ci_hi": float(hi),
            "n_converged": n_ok, "n_boot": n_boot}


# === Block-permutation p-value =======================================

def block_permutation_pvalue(
    df: pd.DataFrame, W: int, n_perm: int, rng: np.random.Generator,
    expected_block_len: int = E_BLOCK_LEN,
) -> dict:
    """One-sided positive permutation p-value for beta_1 in the pooled-LC
    headline cell. Block-permutes is_crash across the whole frame,
    recomputes crash_count_W + eligibility + outcome, refits.
    """
    X_obs, y_obs = build_xy(df, W, for_phase=False, phase=None)
    if X_obs is None:
        return {"p_value": float("nan"), "observed_beta": float("nan"),
                "n_converged": 0, "n_perm": n_perm}
    beta_obs, _ = fit_logistic(X_obs, y_obs)
    obs = float(beta_obs[1])

    is_crash_orig = df["is_crash"].to_numpy()

    perm_betas = np.empty(n_perm)
    n_ok = 0
    for b in range(n_perm):
        perm_ic = block_permute_series(is_crash_orig, expected_block_len, rng)
        df_p = df.copy()
        df_p["is_crash"] = perm_ic
        feat = build_features_minimal(df_p, W)
        df_p["crash_count_W_inline"] = feat["crash_count_W"]
        X_p, y_p = build_xy(df_p, W, for_phase=False, phase=None,
                            predictors=("crash_count_W_inline",))
        if X_p is None or len(y_p) < 30:
            perm_betas[b] = np.nan
            continue
        beta_p, ok = fit_logistic(X_p, y_p)
        if ok:
            perm_betas[b] = beta_p[1]
            n_ok += 1
        else:
            perm_betas[b] = np.nan

    valid = perm_betas[~np.isnan(perm_betas)]
    if len(valid) == 0:
        return {"p_value": float("nan"), "observed_beta": obs,
                "n_converged": n_ok, "n_perm": n_perm}
    p = float((np.sum(valid >= obs) + 1) / (len(valid) + 1))
    return {"p_value": p, "observed_beta": obs, "n_converged": n_ok,
            "n_perm": n_perm}


def build_features_minimal(df: pd.DataFrame, W: int) -> dict[str, np.ndarray]:
    """Recompute crash_count_W only, given a (possibly permuted) is_crash."""
    dates = df["date"].tolist()
    is_crash = df["is_crash"].to_numpy()
    date_to_idx = {d: i for i, d in enumerate(dates)}
    n = len(df)
    cc = np.zeros(n, dtype=int)
    for i, d in enumerate(dates):
        cnt = 0
        for k in range(1, W + 1):
            j = date_to_idx.get(d - timedelta(days=k))
            if j is not None and is_crash[j]:
                cnt += 1
        cc[i] = cnt
    return {"crash_count_W": cc}


def build_xy(
    df: pd.DataFrame, W: int, *, for_phase: bool, phase: str | None,
    predictors: tuple[str, ...] = ("crash_count_W",),
    outcome: str = "is_crash",
    era_filter: str | None = None,
) -> tuple[np.ndarray | None, np.ndarray | None]:
    """Build (X, y) for a logistic fit on eligible rows.

    predictors:
      - ('crash_count_W',)            primary (uses df['crash_count_{W}d'])
      - ('crash_count_W_inline',)     permutation path
      - ('crash_count_W', 'gevoelscore_lagged_mean_14d')   covariate sensitivity
    outcome:
      - 'is_crash'                    primary outcome at d
      - 'any_crash_next_4d'           secondary forward window
    era_filter: 'train' | 'validate' | None (pooled)
    """
    mask = eligibility_mask(df, W, for_phase=for_phase, phase=phase)
    if era_filter is not None:
        dates = df["date"].to_numpy()
        if era_filter == "train":
            mask = mask & np.array([d <= TRAIN_END for d in dates])
        elif era_filter == "validate":
            mask = mask & np.array([d > TRAIN_END for d in dates])
    if mask.sum() == 0:
        return None, None
    sub = df.loc[mask].copy()
    cols = []
    for p in predictors:
        if p == "crash_count_W":
            cols.append(f"crash_count_{W}d")
        elif p == "crash_count_W_inline":
            cols.append("crash_count_W_inline")
        else:
            cols.append(p)
    sub = sub.dropna(subset=cols + [outcome])
    if len(sub) == 0:
        return None, None
    X = sub[cols].to_numpy(dtype=float)
    y = sub[outcome].to_numpy().astype(float)
    return X, y


# === Binned tabulation with block-bootstrap CIs ======================

def bin_index(cc: int) -> int:
    if cc >= 3:
        return 3
    return int(cc)


def binned_tab(
    df: pd.DataFrame, W: int, n_boot: int, rng: np.random.Generator,
    *, era_filter: str | None = None, for_phase: bool = False,
    phase: str | None = None,
) -> dict:
    """Per-bin (0,1,2,3+) rate of is_crash[d] with stationary-bootstrap CIs."""
    mask = eligibility_mask(df, W, for_phase=for_phase, phase=phase)
    if era_filter is not None:
        dates = df["date"].to_numpy()
        if era_filter == "train":
            mask = mask & np.array([d <= TRAIN_END for d in dates])
        elif era_filter == "validate":
            mask = mask & np.array([d > TRAIN_END for d in dates])
    sub = df.loc[mask, ["date", f"crash_count_{W}d", "is_crash"]].copy()
    sub["bin"] = sub[f"crash_count_{W}d"].map(bin_index)
    n_total = len(sub)
    if n_total == 0:
        return {"bins": {}, "n_total": 0}

    per_bin = {b: {"n": 0, "k": 0, "rate": float("nan"),
                   "ci_lo": float("nan"), "ci_hi": float("nan")}
               for b in (0, 1, 2, 3)}
    for b in (0, 1, 2, 3):
        sel = sub["bin"] == b
        n_b = int(sel.sum())
        k_b = int(sub.loc[sel, "is_crash"].sum())
        per_bin[b]["n"] = n_b
        per_bin[b]["k"] = k_b
        if n_b > 0:
            per_bin[b]["rate"] = k_b / n_b

    sub = sub.sort_values("date").reset_index(drop=True)
    bin_arr = sub["bin"].to_numpy()
    crash_arr = sub["is_crash"].to_numpy().astype(int)
    n = len(sub)
    rates_by_bin = {b: [] for b in (0, 1, 2, 3)}
    for _ in range(n_boot):
        idx = stationary_bootstrap_indices(n, E_BLOCK_LEN, rng)
        b_perm = bin_arr[idx]
        c_perm = crash_arr[idx]
        for b in (0, 1, 2, 3):
            sel = b_perm == b
            if sel.sum() > 0:
                rates_by_bin[b].append(c_perm[sel].mean())
    for b in (0, 1, 2, 3):
        if len(rates_by_bin[b]) >= 100:
            lo, hi = np.percentile(rates_by_bin[b], [2.5, 97.5])
            per_bin[b]["ci_lo"] = float(lo)
            per_bin[b]["ci_hi"] = float(hi)

    return {"bins": per_bin, "n_total": n_total}


def check_monotonicity_relative(bins: dict, min_n: int = MIN_BIN_DAYS,
                                rel_tol: float = REL_TOL) -> dict:
    """Sec 5.1(b) relative-tolerance gate. A violation in any consecutive
    pair sets violated=True. Bins with fewer than min_n days are excluded.
    """
    keys = [b for b in (0, 1, 2, 3) if bins[b]["n"] >= min_n]
    rates = [(b, bins[b]["rate"]) for b in keys]
    violations = []
    for (b1, r1), (b2, r2) in zip(rates, rates[1:]):
        if r1 > 0 and r2 < rel_tol * r1:
            violations.append({"from_bin": b1, "to_bin": b2,
                               "rate_from": r1, "rate_to": r2,
                               "threshold": rel_tol * r1})
    return {"violated": len(violations) > 0,
            "violations": violations,
            "bins_checked": keys}


def check_ci_overlap(bins: dict, min_n: int = MIN_BIN_DAYS) -> list[dict]:
    """Companion: consecutive-bin CI overlap > 50% of narrower interval."""
    keys = [b for b in (0, 1, 2, 3) if bins[b]["n"] >= min_n
            and not np.isnan(bins[b]["ci_lo"])]
    overlaps = []
    for b1, b2 in zip(keys, keys[1:]):
        lo1, hi1 = bins[b1]["ci_lo"], bins[b1]["ci_hi"]
        lo2, hi2 = bins[b2]["ci_lo"], bins[b2]["ci_hi"]
        ov_lo = max(lo1, lo2)
        ov_hi = min(hi1, hi2)
        ov = max(0.0, ov_hi - ov_lo)
        w1 = hi1 - lo1
        w2 = hi2 - lo2
        narrower = min(w1, w2) if w1 > 0 and w2 > 0 else 0.0
        frac = ov / narrower if narrower > 0 else 0.0
        overlaps.append({"pair": [b1, b2], "overlap_frac": float(frac),
                         "overlap_dominant": bool(frac > 0.50)})
    return overlaps


# === Same-day Spearman Sec 3.4 crash-drop sensitivity ================

def same_day_spearman(df: pd.DataFrame, W: int = PRIMARY_W,
                      era_filter: str | None = None) -> dict:
    """Spearman rho between crash_count_W and gevoelscore at d on eligible
    days (Sec 4.2). Report full + crash-drop (rows with is_crash==True
    removed) per Sec 3.4 audit hook."""
    mask = eligibility_mask(df, W, for_phase=False, phase=None)
    if era_filter is not None:
        dates = df["date"].to_numpy()
        if era_filter == "train":
            mask = mask & np.array([d <= TRAIN_END for d in dates])
        elif era_filter == "validate":
            mask = mask & np.array([d > TRAIN_END for d in dates])
    sub = df.loc[mask, [f"crash_count_{W}d", "gevoelscore", "is_crash"]].dropna(
        subset=[f"crash_count_{W}d", "gevoelscore"])
    if len(sub) < 10:
        return {"n_full": len(sub), "rho_full": float("nan"),
                "n_drop": 0, "rho_drop": float("nan"),
                "delta_rho": float("nan"), "flag": False}
    rho_full, _ = stats.spearmanr(sub[f"crash_count_{W}d"], sub["gevoelscore"])
    sub_drop = sub[~sub["is_crash"]]
    if len(sub_drop) < 10:
        return {"n_full": int(len(sub)), "rho_full": float(rho_full),
                "n_drop": int(len(sub_drop)), "rho_drop": float("nan"),
                "delta_rho": float("nan"), "flag": False}
    rho_drop, _ = stats.spearmanr(sub_drop[f"crash_count_{W}d"], sub_drop["gevoelscore"])
    delta = float(rho_full - rho_drop)
    return {"n_full": int(len(sub)), "rho_full": float(rho_full),
            "n_drop": int(len(sub_drop)), "rho_drop": float(rho_drop),
            "delta_rho": delta, "flag": abs(delta) > 0.10}


# === Sanity checks (Sec 7) ===========================================

def sanity_checks(df: pd.DataFrame) -> dict:
    """Sec 7 sanity checks evaluated on pooled-LC x W=14 primary."""
    mask = eligibility_mask(df, PRIMARY_W, for_phase=False, phase=None)
    sub = df.loc[mask].copy()
    sub["bin"] = sub[f"crash_count_{PRIMARY_W}d"].map(bin_index)
    n = len(sub)
    out: dict = {"n_eligible_pooled_W14": n}

    bin_n = {b: int((sub["bin"] == b).sum()) for b in (0, 1, 2, 3)}
    bin_k = {b: int(((sub["bin"] == b) & sub["is_crash"]).sum()) for b in (0, 1, 2, 3)}
    bin_rate = {b: (bin_k[b] / bin_n[b]) if bin_n[b] > 0 else float("nan")
                for b in (0, 1, 2, 3)}
    out["bin_n"] = bin_n
    out["bin_k"] = bin_k
    out["bin_rate"] = bin_rate

    bin3_share = bin_n[3] / n if n > 0 else float("nan")
    out["bin3plus_share"] = bin3_share
    out["bin3plus_flag"] = bool(bin3_share > SANITY_BIN3_FRAC_HIGH)

    out["bin0_rate"] = bin_rate[0]
    out["bin0_flag"] = bool(
        not np.isnan(bin_rate[0]) and (
            bin_rate[0] < SANITY_BIN0_LOW or bin_rate[0] > SANITY_BIN0_HIGH
        )
    )

    X, y = build_xy(df, PRIMARY_W, for_phase=False, phase=None)
    if X is None:
        out["convergence_flag"] = True
        out["pooled_beta1"] = float("nan")
    else:
        beta, ok = fit_logistic(X, y)
        out["convergence_flag"] = (not ok) or any(np.isnan(beta)) or any(np.abs(beta) > 50)
        out["pooled_beta1"] = float(beta[1]) if ok else float("nan")

    out["pooled_n_below_min"] = bool(n < MIN_POOLED_N)

    fires = []
    if out["bin3plus_flag"]:
        fires.append("bin-3+ share %.1f%% > 20%% (Sec 7)" % (bin3_share * 100))
    if out["bin0_flag"]:
        fires.append(
            "bin-0 rate %.3f%% outside [0.5%%, 20%%] expected band (Sec 7)" %
            (bin_rate[0] * 100)
        )
    if out["convergence_flag"]:
        fires.append("pooled-LC x W=14 logistic failed to converge (Sec 7)")
    if out["pooled_n_below_min"]:
        fires.append("pooled eligible n=%d < %d (Sec 5.3 inconclusive)" %
                     (n, MIN_POOLED_N))
    out["sanity_fires"] = fires
    out["sanity_pass"] = len(fires) == 0
    return out


# === Eligibility breakdown ===========================================

def eligibility_breakdown(df: pd.DataFrame) -> dict:
    """Eligible-day counts per phase x era x W."""
    breakdown: dict = {}
    for W in WINDOWS:
        per_W: dict = {}
        for era in ("pooled", "train", "validate"):
            era_filter = None if era == "pooled" else era
            mask = eligibility_mask(df, W, for_phase=False, phase=None)
            if era_filter:
                dates = df["date"].to_numpy()
                if era_filter == "train":
                    mask = mask & np.array([d <= TRAIN_END for d in dates])
                else:
                    mask = mask & np.array([d > TRAIN_END for d in dates])
            n_pool = int(mask.sum())
            per_W[era] = {"pooled": n_pool}
            for ph in ("unmedicated", "buildup", "consolidation", "afbouw", "post_afbouw"):
                ph_mask = eligibility_mask(df, W, for_phase=True, phase=ph)
                if era_filter:
                    dates = df["date"].to_numpy()
                    if era_filter == "train":
                        ph_mask = ph_mask & np.array([d <= TRAIN_END for d in dates])
                    else:
                        ph_mask = ph_mask & np.array([d > TRAIN_END for d in dates])
                per_W[era][ph] = int(ph_mask.sum())
        breakdown[f"W{W}d"] = per_W
    return breakdown


# === Dry-run =========================================================

def dry_run(df: pd.DataFrame) -> int:
    print("=== HA-P7 dry-run (per Sec 10.4) ===")
    print("")
    bd = eligibility_breakdown(df)
    print("--- Eligible day counts (n per phase x era x W) ---")
    for W in WINDOWS:
        print("  W=%dd:" % W)
        per_W = bd[f"W{W}d"]
        for era in ("pooled", "train", "validate"):
            c = per_W[era]
            print("    %-9s pooled=%5d  unmed=%4d  buildup=%3d  consol=%4d  afbouw=%3d  post=%3d" % (
                era, c["pooled"], c["unmedicated"], c["buildup"],
                c["consolidation"], c["afbouw"], c["post_afbouw"]))
    print("")
    sc = sanity_checks(df)
    print("--- Sec 7 sanity checks (pooled LC x W=14) ---")
    print("  n eligible: %d" % sc["n_eligible_pooled_W14"])
    print("  bin-0  n=%4d k=%3d rate=%.4f" % (sc["bin_n"][0], sc["bin_k"][0], sc["bin0_rate"]))
    print("  bin-1  n=%4d k=%3d rate=%.4f" % (sc["bin_n"][1], sc["bin_k"][1], sc["bin_rate"][1]))
    print("  bin-2  n=%4d k=%3d rate=%.4f" % (sc["bin_n"][2], sc["bin_k"][2], sc["bin_rate"][2]))
    print("  bin-3+ n=%4d k=%3d rate=%.4f" % (sc["bin_n"][3], sc["bin_k"][3], sc["bin_rate"][3]))
    print("  bin-3+ share of eligible: %.2f%%" % (sc["bin3plus_share"] * 100))
    if not np.isnan(sc["pooled_beta1"]):
        print("  observed pooled-LC x W=14 beta_1: %+.4f (OR=%.3f)" %
              (sc["pooled_beta1"], np.exp(sc["pooled_beta1"])))
    else:
        print("  observed pooled-LC x W=14 beta_1: nan (non-converged)")
    print("")
    if sc["sanity_fires"]:
        print("SANITY-CHECK FIRES:")
        for f in sc["sanity_fires"]:
            print("  - %s" % f)
        print("")
        print("Dry-run sanity check FAILED. Per Sec 7 and Sec 10.4, halt + revise spec -> HA-P7-v2.")
        return 1
    print("All sanity checks pass. Ready for full run.")
    return 0


# === Verdict evaluation per Sec 5 ====================================

def evaluate_verdict(cell: dict, bin_check: dict, w_ci_disagreement_count: int) -> dict:
    """Apply Sec 5.1 three-criterion bar to a single cell."""
    ci_lo = cell.get("ci_lo", float("nan"))
    ci_hi = cell.get("ci_hi", float("nan"))
    if np.isnan(ci_lo) or np.isnan(ci_hi):
        return {"verdict": "INCONCLUSIVE-no-CI",
                "crit_a_holds": None, "crit_b_holds": None,
                "crit_c_window_disagreement_count": int(w_ci_disagreement_count),
                "crit_c_holds": None}
    crit_a = (ci_lo <= 0 <= ci_hi)
    crit_b = bool(bin_check["violated"])
    crit_c = w_ci_disagreement_count >= 2

    if crit_a and crit_b and crit_c:
        verdict = "NOT-SUPPORTED"
    elif (not crit_a) and (not crit_b) and (w_ci_disagreement_count < 2):
        verdict = "SUPPORTED"
    elif (not crit_a):
        verdict = "INCONCLUSIVE-magnitude-present-companion-disagrees"
    else:
        verdict = "INCONCLUSIVE"
    return {"verdict": verdict, "crit_a_holds": bool(crit_a),
            "crit_b_holds": bool(crit_b),
            "crit_c_window_disagreement_count": int(w_ci_disagreement_count),
            "crit_c_holds": bool(crit_c)}


# === Full run ========================================================

def run_full(df: pd.DataFrame) -> dict:
    rng = np.random.default_rng(RANDOM_SEED)
    results: dict = {"seed": RANDOM_SEED, "e_block_len": E_BLOCK_LEN}

    mask_pool = eligibility_mask(df, PRIMARY_W, for_phase=False, phase=None)
    cc14 = df.loc[mask_pool, f"crash_count_{PRIMARY_W}d"].to_numpy(dtype=float)
    el_star = estimate_block_length(cc14)
    el_flag = (not np.isnan(el_star)) and abs(el_star - E_BLOCK_LEN) / E_BLOCK_LEN > EL_STAR_FLAG_FACTOR
    results["el_star"] = float(el_star) if not np.isnan(el_star) else None
    results["el_star_flag_factor2"] = bool(el_flag)

    print("  fitting bootstrap CIs (B=%d) for pooled x W in %s x era in pooled/train/validate ..." % (
        B_HEADLINE, WINDOWS))
    pooled_cells: dict = {}
    for W in WINDOWS:
        pooled_cells[f"W{W}d"] = {}
        for era in ("pooled", "train", "validate"):
            era_filter = None if era == "pooled" else era
            X, y = build_xy(df, W, for_phase=False, phase=None, era_filter=era_filter)
            if X is None or len(y) < 30:
                pooled_cells[f"W{W}d"][era] = {"n": int(len(y)) if y is not None else 0,
                                                "point": float("nan"),
                                                "ci_lo": float("nan"),
                                                "ci_hi": float("nan")}
                continue
            ci = bootstrap_logit_ci((X, y), B_HEADLINE, rng)
            ci["n"] = int(len(y))
            ci["positives"] = int(y.sum())
            ci["or_point"] = float(np.exp(ci["point"])) if not np.isnan(ci["point"]) else None
            ci["or_lo"] = float(np.exp(ci["ci_lo"])) if not np.isnan(ci["ci_lo"]) else None
            ci["or_hi"] = float(np.exp(ci["ci_hi"])) if not np.isnan(ci["ci_hi"]) else None
            pooled_cells[f"W{W}d"][era] = ci
    results["pooled_cells"] = pooled_cells

    w_disagreement: dict = {}
    for era in ("pooled", "train", "validate"):
        count = 0
        for W in WINDOWS:
            cell = pooled_cells[f"W{W}d"][era]
            ci_lo = cell.get("ci_lo", float("nan"))
            ci_hi = cell.get("ci_hi", float("nan"))
            if (not np.isnan(ci_lo)) and (not np.isnan(ci_hi)) and ci_lo <= 0 <= ci_hi:
                count += 1
        w_disagreement[era] = count
    results["window_ci_disagreement_per_era"] = w_disagreement

    print("  binned tabulation with block-bootstrap CIs (B=%d) ..." % B_BIN)
    binned: dict = {}
    bin_checks: dict = {}
    for era in ("pooled", "train", "validate"):
        era_filter = None if era == "pooled" else era
        b = binned_tab(df, PRIMARY_W, B_BIN, rng, era_filter=era_filter)
        binned[era] = b
        bin_checks[era] = {
            "monotonicity": check_monotonicity_relative(b["bins"]),
            "ci_overlap": check_ci_overlap(b["bins"]),
        }
    results["binned_W14"] = binned
    results["bin_monotonicity_W14"] = bin_checks

    print("  block-permutation null (B=%d, pooled x W=14) ..." % B_HEADLINE)
    perm = block_permutation_pvalue(df, PRIMARY_W, B_HEADLINE, rng)
    results["permutation_null_headline"] = perm

    print("  Sec 4.5.4 covariate-sensitivity logistic ...")
    cov_results: dict = {}
    for era in ("pooled", "train", "validate"):
        era_filter = None if era == "pooled" else era
        X, y = build_xy(df, PRIMARY_W, for_phase=False, phase=None,
                        predictors=("crash_count_W", "gevoelscore_lagged_mean_14d"),
                        era_filter=era_filter)
        if X is None or len(y) < 30:
            cov_results[era] = {"n": int(len(y)) if y is not None else 0,
                                 "beta1_point": float("nan"),
                                 "beta2_point": float("nan")}
            continue
        ci1 = bootstrap_logit_ci((X, y), B_HEADLINE, rng, coef_idx=1)
        ci2 = bootstrap_logit_ci((X, y), B_HEADLINE, rng, coef_idx=2)
        cov_results[era] = {
            "n": int(len(y)),
            "beta1_point": ci1["point"],
            "beta1_ci_lo": ci1["ci_lo"],
            "beta1_ci_hi": ci1["ci_hi"],
            "beta2_point": ci2["point"],
            "beta2_ci_lo": ci2["ci_lo"],
            "beta2_ci_hi": ci2["ci_hi"],
        }
    results["covariate_sensitivity_W14"] = cov_results

    spear: dict = {}
    for era in ("pooled", "train", "validate"):
        era_filter = None if era == "pooled" else era
        spear[era] = same_day_spearman(df, PRIMARY_W, era_filter=era_filter)
    results["spearman_same_day"] = spear

    print("  phase-stratified arms (B=%d, diagnostic) ..." % B_DIAGNOSTIC)
    phase_cells: dict = {}
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw", "post_afbouw"):
        phase_cells[ph] = {}
        for W in WINDOWS:
            phase_cells[ph][f"W{W}d"] = {}
            for era in ("pooled", "train", "validate"):
                era_filter = None if era == "pooled" else era
                X, y = build_xy(df, W, for_phase=True, phase=ph, era_filter=era_filter)
                if X is None or len(y) < 30:
                    phase_cells[ph][f"W{W}d"][era] = {
                        "n": int(len(y)) if y is not None else 0,
                        "point": float("nan"), "ci_lo": float("nan"),
                        "ci_hi": float("nan")}
                    continue
                ci = bootstrap_logit_ci((X, y), B_DIAGNOSTIC, rng)
                ci["n"] = int(len(y))
                ci["positives"] = int(y.sum())
                ci["or_point"] = float(np.exp(ci["point"])) if not np.isnan(ci["point"]) else None
                ci["or_lo"] = float(np.exp(ci["ci_lo"])) if not np.isnan(ci["ci_lo"]) else None
                ci["or_hi"] = float(np.exp(ci["ci_hi"])) if not np.isnan(ci["ci_hi"]) else None
                phase_cells[ph][f"W{W}d"][era] = ci
    results["phase_cells"] = phase_cells

    sec_results: dict = {}
    for era in ("pooled", "train", "validate"):
        era_filter = None if era == "pooled" else era
        X, y = build_xy(df, PRIMARY_W, for_phase=False, phase=None,
                        outcome="any_crash_next_4d", era_filter=era_filter)
        if X is None or len(y) < 30:
            sec_results[era] = {"n": int(len(y)) if y is not None else 0,
                                 "point": float("nan"), "ci_lo": float("nan"),
                                 "ci_hi": float("nan")}
            continue
        ci = bootstrap_logit_ci((X, y), B_DIAGNOSTIC, rng)
        ci["n"] = int(len(y))
        ci["positives"] = int(y.sum())
        ci["or_point"] = float(np.exp(ci["point"])) if not np.isnan(ci["point"]) else None
        ci["or_lo"] = float(np.exp(ci["ci_lo"])) if not np.isnan(ci["ci_lo"]) else None
        ci["or_hi"] = float(np.exp(ci["ci_hi"])) if not np.isnan(ci["ci_hi"]) else None
        sec_results[era] = ci
    results["secondary_outcome_W14"] = sec_results

    head_cell = pooled_cells["W14d"]["pooled"]
    head_bins = bin_checks["pooled"]["monotonicity"]
    train_cell = pooled_cells["W14d"]["train"]
    train_bins = bin_checks["train"]["monotonicity"]
    val_cell = pooled_cells["W14d"]["validate"]
    val_bins = bin_checks["validate"]["monotonicity"]
    results["verdict_pooled"] = evaluate_verdict(head_cell, head_bins, w_disagreement["pooled"])
    results["verdict_train"] = evaluate_verdict(train_cell, train_bins, w_disagreement["train"])
    results["verdict_validate"] = evaluate_verdict(val_cell, val_bins, w_disagreement["validate"])

    return results


# === result.md emission ==============================================

def fmt_ci(point, lo, hi, transform: str = "or") -> str:
    if point is None or (isinstance(point, float) and np.isnan(point)):
        return "--"
    if transform == "or":
        p = float(np.exp(point))
        lo_t = float(np.exp(lo)) if (lo is not None and not np.isnan(lo)) else None
        hi_t = float(np.exp(hi)) if (hi is not None and not np.isnan(hi)) else None
    else:
        p = float(point)
        lo_t = float(lo) if (lo is not None and not np.isnan(lo)) else None
        hi_t = float(hi) if (hi is not None and not np.isnan(hi)) else None
    if lo_t is None or hi_t is None or np.isnan(lo_t) or np.isnan(hi_t):
        return "%.3f [--]" % p
    return "%.3f [%.3f, %.3f]" % (p, lo_t, hi_t)


def emit_result_md(df: pd.DataFrame, results: dict) -> str:
    today = date.today().isoformat()
    L: list[str] = []

    head = results["verdict_pooled"]
    head_cell = results["pooled_cells"]["W14d"]["pooled"]
    train_cell = results["pooled_cells"]["W14d"]["train"]
    val_cell = results["pooled_cells"]["W14d"]["validate"]
    perm = results["permutation_null_headline"]

    L.append("# HA-P7 -- result: recent-crash-density predicts crash risk")
    L.append("")
    L.append("*Run %s by `test.py` against the locked pre-registration `hypothesis.md` "
             "(revision 2026-06-15-r3, status LOCKED). Random seed: %d; stationary-bootstrap "
             "+ block-permutation at E[L] = %d days per "
             "`methodology/permutation_null_block_length.md`.*" %
             (today, results["seed"], results["e_block_len"]))
    L.append("")

    L.append("## Headline verdict (pooled LC era x W=14 x primary outcome `is_crash at d`)")
    L.append("")
    L.append("**Verdict: %s**" % head["verdict"])
    L.append("")
    or_str = fmt_ci(head_cell.get("point"), head_cell.get("ci_lo"), head_cell.get("ci_hi"))
    L.append("- OR (per +1 crash-day in [d-14, d-1]): **%s** "
             "(stationary-bootstrap 95%% CI at E[L]=7, B = %s; point from MLE logistic)." %
             (or_str, head_cell.get("n_boot", "?")))
    L.append("- Block-permutation null p-value (one-sided positive): "
             "**p = %.4f** (B = %s; n_converged = %s)." %
             (perm.get("p_value", float("nan")),
              perm.get("n_perm", "?"), perm.get("n_converged", "?")))
    L.append("- n eligible days (pooled LC era x W=14): **%d** (positives: %d)." %
             (head_cell.get("n", 0), head_cell.get("positives", 0)))
    L.append("")
    L.append("Sec 5.1 three-criterion read:")
    L.append("")
    L.append("- (a) OR-CI contains 1: **%s** (%s)" % (
        head["crit_a_holds"],
        "CI EXCLUDES 1" if not head["crit_a_holds"] else "CI INCLUDES 1"))
    L.append("- (b) monotonicity violated under relative-50%% gate: **%s**" % head["crit_b_holds"])
    L.append("- (c) at least 2 of {W=7, W=14, W=30} CIs contain 1: **%s** (%d of 3 contain 1)" %
             (head["crit_c_holds"], head["crit_c_window_disagreement_count"]))
    L.append("")

    L.append("## Train / validate split (W=14 primary)")
    L.append("")
    L.append("| era | n | OR [95%% block-bootstrap CI] | verdict per Sec 5.1 |".replace("%%", "%"))
    L.append("|---|---:|---|---|")
    for era_lab, cell, v in [("pooled LC", head_cell, head),
                              ("train", train_cell, results["verdict_train"]),
                              ("validate", val_cell, results["verdict_validate"])]:
        L.append("| %s | %d | %s | %s |" % (
            era_lab, cell.get("n", 0),
            fmt_ci(cell.get("point"), cell.get("ci_lo"), cell.get("ci_hi")),
            v["verdict"]))
    L.append("")
    L.append("Per Sec 5.0 single-cell lock, only **pooled LC x W=14 x primary outcome** is "
             "the locked headline; train/validate are reported for transparency. The pooled-LC "
             "verdict above is the project-level headline.")
    L.append("")

    L.append("## Window sensitivity arms (diagnostic per Sec 5.0 -- not promotable)")
    L.append("")
    L.append("| W (days) | era | n | OR [95% block-bootstrap CI] | CI contains 1? |")
    L.append("|---:|---|---:|---|---|")
    for W in WINDOWS:
        for era in ("pooled", "train", "validate"):
            cell = results["pooled_cells"][f"W{W}d"][era]
            ci_lo = cell.get("ci_lo", float("nan"))
            ci_hi = cell.get("ci_hi", float("nan"))
            contains_1 = (
                (not np.isnan(ci_lo)) and (not np.isnan(ci_hi)) and ci_lo <= 0 <= ci_hi
            )
            L.append("| %d | %s | %d | %s | %s |" % (
                W, era, cell.get("n", 0),
                fmt_ci(cell.get("point"), cell.get("ci_lo"), cell.get("ci_hi")),
                "yes" if contains_1 else "no"))
    L.append("")
    L.append("Sec 5.1(c) window-CI disagreement count (>= 2 of 3 with CI containing 1 -> "
             "criterion (c) holds): pooled = %d; train = %d; validate = %d." %
             (results["window_ci_disagreement_per_era"]["pooled"],
              results["window_ci_disagreement_per_era"]["train"],
              results["window_ci_disagreement_per_era"]["validate"]))
    L.append("")

    L.append("## Phase-stratified sensitivity arms (diagnostic per Sec 5.0 -- not promotable)")
    L.append("")
    L.append("| phase | W | era | n | OR [95% block-bootstrap CI] |")
    L.append("|---|---:|---|---:|---|")
    for ph in ("unmedicated", "buildup", "consolidation", "afbouw", "post_afbouw"):
        for W in WINDOWS:
            for era in ("pooled", "train", "validate"):
                cell = results["phase_cells"][ph][f"W{W}d"][era]
                if cell.get("n", 0) == 0:
                    continue
                L.append("| %s | %d | %s | %d | %s |" % (
                    ph, W, era, cell.get("n", 0),
                    fmt_ci(cell.get("point"), cell.get("ci_lo"), cell.get("ci_hi"))))
    L.append("")
    L.append("Per-phase verdicts are **descriptive only** per Sec 5.0 hard rule; they do "
             "not promote to SUPPORTED. Buildup includes the Sec 6 CPAP-buffer exclusion "
             "(2024-04-09 to 2024-04-29 dropped from buildup-phase arms).")
    L.append("")

    L.append("## Binned tabulation (W=14, pooled LC era) with block-bootstrap CIs")
    L.append("")
    L.append("| bin | n | k crashes | rate | 95% block-bootstrap CI |")
    L.append("|---:|---:|---:|---|---|")
    pooled_b = results["binned_W14"]["pooled"]["bins"]
    for b in (0, 1, 2, 3):
        c = pooled_b[b]
        rate_str = "%.4f" % c["rate"] if not np.isnan(c["rate"]) else "--"
        ci_str = "[%.4f, %.4f]" % (c["ci_lo"], c["ci_hi"]) if not np.isnan(c["ci_lo"]) else "--"
        lab = "3+" if b == 3 else str(b)
        L.append("| %s | %d | %d | %s | %s |" % (lab, c["n"], c["k"], rate_str, ci_str))
    mc = results["bin_monotonicity_W14"]["pooled"]["monotonicity"]
    overlaps = results["bin_monotonicity_W14"]["pooled"]["ci_overlap"]
    L.append("")
    if mc["violations"]:
        viol_str = "; ".join(
            "bin %s -> bin %s: rate %.4f -> %.4f (threshold %.4f)" % (
                v["from_bin"], v["to_bin"], v["rate_from"], v["rate_to"], v["threshold"])
            for v in mc["violations"])
    else:
        viol_str = "(none)"
    L.append("Monotonicity (relative-50%% gate per Sec 5.1(b)): **%s** (bins checked: %s; "
             "violations: %s)." % (
                 "VIOLATED" if mc["violated"] else "satisfied",
                 mc["bins_checked"], viol_str))
    if overlaps:
        ov_str = "; ".join(
            "%s: %.1f%%%s" % (ov["pair"], ov["overlap_frac"] * 100,
                              " (dominant)" if ov["overlap_dominant"] else "")
            for ov in overlaps)
        L.append("Companion CI-overlap test: %s." % ov_str)
    L.append("")

    cov = results["covariate_sensitivity_W14"]
    L.append("## Sec 4.5.4 covariate sensitivity (secondary logistic adds `gevoelscore_lagged_mean_14d`)")
    L.append("")
    L.append("| era | n | beta_crash_count_14d (OR) [95% CI] | beta_gevoel_lag_mean_14d [95% CI] |")
    L.append("|---|---:|---|---|")
    for era in ("pooled", "train", "validate"):
        c = cov[era]
        if c.get("n", 0) == 0:
            continue
        beta1_or = fmt_ci(c.get("beta1_point"), c.get("beta1_ci_lo"), c.get("beta1_ci_hi"))
        beta2_lin = fmt_ci(c.get("beta2_point"), c.get("beta2_ci_lo"), c.get("beta2_ci_hi"),
                            transform="linear")
        L.append("| %s | %d | %s | %s |" % (era, c["n"], beta1_or, beta2_lin))
    L.append("")
    L.append("**Disambiguation read** (Sec 4.5.4): if beta_1 attenuates toward 0 while "
             "beta_2's CI excludes 0, the Sec 4.5.1 primary signal was a proxy for recent low "
             "gevoelscore -- the *recovery-debt* mechanism reading is NOT supported beyond "
             "the trivial label-density-tracks-gevoelscore reading. If beta_1 survives, the "
             "recovery-debt mechanism reading is supported by information beyond gevoelscore "
             "trajectory.")
    L.append("")

    sec = results["secondary_outcome_W14"]
    L.append("## Secondary outcome `any_crash_in_next_4d` (W=14, diagnostic per Sec 5.2)")
    L.append("")
    L.append("| era | n | OR [95% block-bootstrap CI] |")
    L.append("|---|---:|---|")
    for era in ("pooled", "train", "validate"):
        c = sec[era]
        if c.get("n", 0) == 0:
            continue
        L.append("| %s | %d | %s |" % (
            era, c["n"],
            fmt_ci(c.get("point"), c.get("ci_lo"), c.get("ci_hi"))))
    L.append("")

    sp = results["spearman_same_day"]
    L.append("## Same-day Spearman rho(crash_count_14d, gevoelscore at d) -- Sec 3.4 venue")
    L.append("")
    L.append("| era | n_full | rho_full | n_no_crash | rho_crash_dropped | abs_delta_rho | Sec 3.4 flag |")
    L.append("|---|---:|---:|---:|---:|---:|---|")
    for era in ("pooled", "train", "validate"):
        c = sp[era]
        rf = ("%+.4f" % c["rho_full"]) if not np.isnan(c["rho_full"]) else "--"
        rd = ("%+.4f" % c["rho_drop"]) if not np.isnan(c["rho_drop"]) else "--"
        dr = ("%.4f" % abs(c["delta_rho"])) if not np.isnan(c["delta_rho"]) else "--"
        flag = "FLAG" if c.get("flag") else "ok"
        L.append("| %s | %d | %s | %d | %s | %s | %s |" % (
            era, c["n_full"], rf, c["n_drop"], rd, dr, flag))
    L.append("")

    L.append("## Sec 4.5.1 data-driven E[L]* companion")
    L.append("")
    el = results.get("el_star")
    el_flag = results.get("el_star_flag_factor2")
    if el is None:
        L.append("E[L]* could not be estimated.")
    else:
        L.append("Data-driven E[L]* on pooled-LC `crash_count_14d` series: **%.2f days** "
                 "(project default = 7)." % el)
        if el_flag:
            L.append("**Factor-of-2 flag fired**: |E[L]* - 7| / 7 > 0.5. Per the methodology "
                     "MD Sec 2 operational consequence, FLAG for review before locking the verdict.")
        else:
            L.append("Factor-of-2 flag: not fired. The default E[L]=7 is consistent with the "
                     "data-driven estimate.")
    L.append("")

    L.append("## Caveats (per hypothesis.md Sec 8 -- must be acknowledged on every read)")
    L.append("")
    L.append("1. **Causal-attribution ambiguity is irreducible**. A positive result is "
             "consistent with the recovery-debt mechanism AND with a shared underlying "
             "cause (stressful period, infection, intervention transition). The design "
             "cannot adjudicate.")
    L.append("2. **Selection bias on conditioning**: the eligibility rule "
             "`is_crash[d-1] == False` concentrates the analysis on inter-crash gap days. "
             "These differ distributionally from arbitrary days.")
    L.append("3. **Self-reported crash labels** (crash_v2 = `gevoelscore <= 3` for >= 2 "
             "consecutive days). Single-rater coding; no physiological ground truth.")
    L.append("4. **`gevoelscore` is the SAME instrument** generating both the predictor "
             "(`crash_count_14d`) and the outcome (`is_crash at d`). Any systematic drift "
             "or mood-state-dependent reporting affects both.")
    L.append("5. **Protocol disturbs the test**. Operational pacing based on recent-crash "
             "awareness conflates 'recent-crash-aware-and-protective' vs "
             "'recent-crash-aware-but-still-crashed'.")
    L.append("6. **Phase dose-modulation** of `gevoelscore` per Session C's small "
             "detrend-surviving step at 2026-03-20. The per-phase arms address this; the "
             "pooled headline does not apply a Sec 5.B dose-adjustment because the predictor "
             "is a count.")
    L.append("7. **Sec 3.4 inapplicable-to-primary by construction** (dropping `is_crash` "
             "rows would eliminate every positive case); Sec 3.4 is honored on the "
             "descriptive same-day Spearman above.")
    L.append("8. **Per-phase ns are small for buildup + afbouw**; pooled-LC is the headline. "
             "Per-phase INCONCLUSIVE is expected, not promoted.")
    L.append("")

    L.append("---")
    L.append("")
    L.append("*Result emitted by `test.py` on the locked pre-registration. Raw result data "
             "(bootstrap CIs, beta arrays, per-phase cells) in `result-data.json` alongside "
             "this file. Any post-result modification of the spec creates HA-P7-v2 with this "
             "v1 archived.*")
    return "\n".join(L) + "\n"


# === main ============================================================

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Print eligible-n + Sec 7 sanity checks; halt before any "
                             "bootstrap or full run.")
    args = parser.parse_args()

    print("Loading per_day_master.csv ...")
    df = load_master()
    print("  rows: %d, dates %s -> %s" % (len(df), df["date"].min(), df["date"].max()))

    print("Building features (crash_count_W, secondary outcome, lagged gevoelscore) ...")
    df = build_features(df)

    if args.dry_run:
        return dry_run(df)

    sc = sanity_checks(df)
    if not sc["sanity_pass"]:
        print("Sanity check failed (per Sec 7). Refusing to run full evaluation.")
        for f in sc["sanity_fires"]:
            print("  - %s" % f)
        return 1

    print("")
    print("Running full evaluation ...")
    results = run_full(df)
    results["sanity_checks"] = sc

    OUT_JSON.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print("")
    print("Wrote %s" % OUT_JSON)

    md = emit_result_md(df, results)
    OUT_MD.write_text(md, encoding="utf-8")
    print("Wrote %s" % OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
