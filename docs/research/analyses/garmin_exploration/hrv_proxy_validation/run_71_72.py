"""HRV proxy validation - descriptive Checks 7.1, 7.2, 7.3.

Implements the in-corpus descriptive checks from
docs/research/methodology/hrv_proxy_via_stress.md section 7.

Purpose: characterise whether `stress_mean_sleep` is a usable HRV
proxy on the Forerunner 245 / Elevate V3 sensor by checking three
necessary conditions:

  7.1 Does sleep-stress carry the expected exertion signal?
      (heavy-exertion days should show higher sleep-stress than rest
      days; if not, the proxy is dead).
  7.2 Is sleep-stress separable from the HR confound?
      (if `stress_mean_sleep ~ resting_hr` R-squared is very high,
      sleep-stress carries no HRV-specific information; it is just
      a windowed HR signal).
  7.3 Does sleep-stress associate with crash events?
      (per-event mean on crash episodes vs base-rate of normal
      days; episode-level primary, day-level supplementary).

This script is descriptive-only. It reports effect sizes with
bootstrap 95 percent confidence intervals. It does NOT make
hypothesis-testing decisions, does NOT recommend pre-reg revisions,
and does NOT impose a story on the numbers. Output is a table for
the user / reviewer to read.

Validated-era discipline (per project_lc_era_boundaries memory):
The LC era (2022-04-04 onward) is treated as one regime; no
internal subsplit. Pre-covid baseline reported as a sanity-check
endpoint only.

Crash-distortion sensitivity (per feedback_crash_distortion_sensitivity
memory): Check 7.2 is run twice, with and without crash days
included.

Usage:
    python run_71_72.py

Outputs to the script directory:
    result-data.json      -- machine-readable results
    result-table.txt      -- human-readable table

Dependencies: pandas, numpy, scipy.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LC_START = pd.Timestamp("2022-04-04")
INFECTION_START = pd.Timestamp("2022-03-21")

N_BOOTSTRAP = 5000
BOOTSTRAP_SEED = 20260612
CI_LOW = 2.5
CI_HIGH = 97.5

# Heavy-exertion classes per the v3.2 lagged exertion taxonomy.
HEAVY_CLASSES = {"heavy", "very_heavy"}
REST_CLASSES = {"none", "light"}

# Z-score baseline window for resting_hr (per [[feedback_relative_not_absolute]]).
# Matches the v3.2 lagged convention used elsewhere in the project
# (HA07c sleep-stress-mean-delta etc): trailing window [d-90, d-31].
Z_WINDOW_START_DAYS = 30  # exclusive lower (days d-1 .. d-30 are EXCLUDED)
Z_WINDOW_END_DAYS = 90    # inclusive upper (d-90 is included)
Z_MIN_LAGGED_DAYS = 40    # min valid days in window
Z_TRIMMED_PCT = 0.10      # 10% trim each end for robust mean
Z_MIN_BASELINE_STD = 1.0  # bpm; below this z is unstable

HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "result-data.json"
OUT_TXT = HERE / "result-table.txt"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def resolve_data_path() -> Path:
    """Resolve GEVOELSCORE_DATA_PATH from env or repo .env."""
    p = os.environ.get("GEVOELSCORE_DATA_PATH")
    if p:
        return Path(p)
    env_file = Path(__file__).resolve().parents[5] / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("GEVOELSCORE_DATA_PATH="):
                return Path(line.split("=", 1)[1].strip())
    sys.exit("ERROR: GEVOELSCORE_DATA_PATH not found in env or .env.")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load per_day_master.csv and labels_crash_v2.csv, filter to LC era."""
    data = resolve_data_path()
    master_path = data / "unified" / "per_day_master.csv"
    labels_path = data / "processed" / "crash_labels" / "labels_crash_v2.csv"
    if not master_path.exists():
        sys.exit(f"ERROR: {master_path} not found.")
    if not labels_path.exists():
        sys.exit(f"ERROR: {labels_path} not found.")
    df = pd.read_csv(master_path, low_memory=False)
    df["date"] = pd.to_datetime(df["date"])
    lab = pd.read_csv(labels_path)
    lab["date"] = pd.to_datetime(lab["date"])
    return df, lab


# ---------------------------------------------------------------------------
# Statistical helpers (bootstrap, partial correlation)
# ---------------------------------------------------------------------------


def bootstrap_ci_mean(
    x: np.ndarray, n_boot: int = N_BOOTSTRAP, seed: int = BOOTSTRAP_SEED
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(n_boot, len(x)))
    samples = x[idx].mean(axis=1)
    return float(np.percentile(samples, CI_LOW)), float(
        np.percentile(samples, CI_HIGH)
    )


def bootstrap_ci_diff(
    a: np.ndarray, b: np.ndarray, n_boot: int = N_BOOTSTRAP, seed: int = BOOTSTRAP_SEED
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    diffs = np.empty(n_boot)
    for i in range(n_boot):
        ai = rng.integers(0, len(a), size=len(a))
        bi = rng.integers(0, len(b), size=len(b))
        diffs[i] = a[ai].mean() - b[bi].mean()
    return float(np.percentile(diffs, CI_LOW)), float(np.percentile(diffs, CI_HIGH))


def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    """Pooled-SD Cohen's d for two independent samples."""
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return float("nan")
    va = a.var(ddof=1)
    vb = b.var(ddof=1)
    pooled = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    if pooled == 0:
        return float("nan")
    return float((a.mean() - b.mean()) / pooled)


def partial_correlation(
    x: np.ndarray, y: np.ndarray, z: np.ndarray
) -> tuple[float, float]:
    """Partial Pearson r and Spearman rho between x and y, controlling for z.

    Residualises both x and y on z via OLS, returns r(resid_x, resid_y).
    """
    mask = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    x, y, z = x[mask], y[mask], z[mask]
    if len(x) < 4:
        return float("nan"), float("nan")
    Z = np.column_stack([np.ones_like(z), z])
    beta_x, *_ = np.linalg.lstsq(Z, x, rcond=None)
    beta_y, *_ = np.linalg.lstsq(Z, y, rcond=None)
    rx = x - Z @ beta_x
    ry = y - Z @ beta_y
    r_p = stats.pearsonr(rx, ry)
    r_s = stats.spearmanr(rx, ry)
    return float(r_p.statistic), float(r_s.statistic)


def _trimmed_mean_std(vals: np.ndarray, trim_pct: float) -> tuple[float, float]:
    """Symmetrically trimmed mean and std (sample, ddof=1)."""
    v = np.sort(vals)
    n = len(v)
    trim = int(n * trim_pct)
    if n - 2 * trim < 2:
        return float("nan"), float("nan")
    v = v[trim:n - trim]
    return float(v.mean()), float(v.std(ddof=1))


def compute_resting_hr_z(df: pd.DataFrame) -> pd.DataFrame:
    """Add a resting_hr_z column to df.

    z[d] = (resting_hr[d] - trimmed_mean(window)) / std(window)
    where window = days [d-Z_WINDOW_END_DAYS, d-Z_WINDOW_START_DAYS-1]
    (inclusive lower, exclusive upper of the most-recent days).

    Per [[feedback_relative_not_absolute]] the proxy is the z-score
    against a personal rolling baseline, not the raw value.
    """
    df = df.sort_values("date").reset_index(drop=True).copy()
    rhr = df["resting_hr"].to_numpy(dtype=float)
    dates = df["date"].to_numpy()
    z = np.full(len(df), np.nan)
    # Build a date -> index map for O(1) lookups
    idx_by_date = {d: i for i, d in enumerate(dates)}
    for i, d in enumerate(dates):
        # Collect the trailing-window resting_hr values
        window_vals = []
        for k in range(Z_WINDOW_START_DAYS + 1, Z_WINDOW_END_DAYS + 1):
            wd = d - pd.Timedelta(days=k)
            j = idx_by_date.get(wd)
            if j is None:
                continue
            v = rhr[j]
            if np.isfinite(v):
                window_vals.append(v)
        if len(window_vals) < Z_MIN_LAGGED_DAYS:
            continue
        mu, sigma = _trimmed_mean_std(
            np.array(window_vals), Z_TRIMMED_PCT
        )
        if not np.isfinite(sigma) or sigma < Z_MIN_BASELINE_STD:
            continue
        if not np.isfinite(rhr[i]):
            continue
        z[i] = (rhr[i] - mu) / sigma
    df["resting_hr_z"] = z
    return df


def logistic_irls(
    X: np.ndarray, y: np.ndarray, max_iter: int = 50, tol: float = 1e-7
) -> tuple[np.ndarray, np.ndarray]:
    """Hand-rolled IRLS for logistic regression. Returns (beta, se)."""
    beta = np.zeros(X.shape[1])
    for _ in range(max_iter):
        z = X @ beta
        z = np.clip(z, -30, 30)
        p = 1.0 / (1.0 + np.exp(-z))
        W = p * (1.0 - p)
        XW = X * W[:, None]
        H = X.T @ XW
        g = X.T @ (y - p)
        try:
            delta = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            break
        beta = beta + delta
        if np.max(np.abs(delta)) < tol:
            break
    # Approx SE from inverse Hessian diagonal
    try:
        cov = np.linalg.inv(H)
        se = np.sqrt(np.clip(np.diag(cov), 0, None))
    except np.linalg.LinAlgError:
        se = np.full(X.shape[1], np.nan)
    return beta, se


def auc_score(y: np.ndarray, scores: np.ndarray) -> float:
    """Mann-Whitney U formulation of ROC AUC."""
    mask = np.isfinite(scores) & np.isfinite(y)
    y = y[mask]
    s = scores[mask]
    pos = s[y == 1]
    neg = s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    all_scores = np.concatenate([pos, neg])
    ranks = stats.rankdata(all_scores)
    rank_sum_pos = ranks[: len(pos)].sum()
    return float(
        (rank_sum_pos - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))
    )


# ---------------------------------------------------------------------------
# Check 7.1 - exertion signal
# ---------------------------------------------------------------------------


def check_71(df_lc: pd.DataFrame) -> dict:
    """Compare stress_mean_sleep on heavy vs rest exertion days (LC era)."""
    sub = df_lc.dropna(
        subset=["stress_mean_sleep", "exertion_class_lagged_lcera"]
    ).copy()
    heavy = sub[sub["exertion_class_lagged_lcera"].isin(HEAVY_CLASSES)][
        "stress_mean_sleep"
    ].to_numpy()
    rest = sub[sub["exertion_class_lagged_lcera"].isin(REST_CLASSES)][
        "stress_mean_sleep"
    ].to_numpy()
    # Also report moderate as a sanity in-between band.
    moderate = sub[sub["exertion_class_lagged_lcera"] == "moderate"][
        "stress_mean_sleep"
    ].to_numpy()

    heavy_lo, heavy_hi = bootstrap_ci_mean(heavy) if len(heavy) else (float("nan"),) * 2
    rest_lo, rest_hi = bootstrap_ci_mean(rest) if len(rest) else (float("nan"),) * 2
    diff_lo, diff_hi = (
        bootstrap_ci_diff(heavy, rest)
        if len(heavy) >= 2 and len(rest) >= 2
        else (float("nan"), float("nan"))
    )

    # Non-parametric two-sample test as supplementary context (not a decision).
    if len(heavy) >= 2 and len(rest) >= 2:
        u = stats.mannwhitneyu(heavy, rest, alternative="two-sided")
        u_stat, u_p = float(u.statistic), float(u.pvalue)
    else:
        u_stat, u_p = float("nan"), float("nan")

    return {
        "n_heavy": int(len(heavy)),
        "n_moderate": int(len(moderate)),
        "n_rest": int(len(rest)),
        "mean_heavy": float(heavy.mean()) if len(heavy) else float("nan"),
        "mean_moderate": float(moderate.mean()) if len(moderate) else float("nan"),
        "mean_rest": float(rest.mean()) if len(rest) else float("nan"),
        "ci_heavy": [heavy_lo, heavy_hi],
        "ci_rest": [rest_lo, rest_hi],
        "mean_diff_heavy_minus_rest": (
            float(heavy.mean() - rest.mean())
            if len(heavy) and len(rest)
            else float("nan")
        ),
        "ci_diff": [diff_lo, diff_hi],
        "cohens_d": cohens_d(heavy, rest),
        "mann_whitney_u": u_stat,
        "mann_whitney_p": u_p,
        "labeling_scheme": "exertion_class_lagged_lcera (v3.2)",
        "predictor_source": "per_day_master.csv",
    }


# ---------------------------------------------------------------------------
# Check 7.2 - HR confound separability
# ---------------------------------------------------------------------------


def check_72(df_lc: pd.DataFrame, df_lc_no_crash: pd.DataFrame) -> dict:
    """Quantify how much of stress_mean_sleep is explained by resting_hr."""
    out = {}
    for label, sub in [("all_lc", df_lc), ("lc_no_crash_days", df_lc_no_crash)]:
        s = sub.dropna(subset=["stress_mean_sleep", "resting_hr"])
        x = s["resting_hr"].to_numpy(dtype=float)
        y = s["stress_mean_sleep"].to_numpy(dtype=float)
        if len(x) < 4:
            out[label] = {"n": int(len(x)), "note": "n < 4, skipped"}
            continue
        # Linear fit: y ~ a + b*x
        slope, intercept, r, p, se = stats.linregress(x, y)
        rho_s = stats.spearmanr(x, y)
        # Variance explained = r^2
        out[label] = {
            "n": int(len(x)),
            "pearson_r": float(r),
            "pearson_p": float(p),
            "spearman_rho": float(rho_s.statistic),
            "spearman_p": float(rho_s.pvalue),
            "r_squared": float(r * r),
            "unique_variance_in_stress_mean_sleep": float(1 - r * r),
            "slope_stress_per_bpm": float(slope),
            "intercept": float(intercept),
            "slope_se": float(se),
        }
    out["crash_distortion_sensitivity_applied"] = True
    out["sensitivity_memory"] = "feedback_crash_distortion_sensitivity"
    return out


# ---------------------------------------------------------------------------
# Check 7.3 - sleep-stress on crash events (episode-level primary)
# ---------------------------------------------------------------------------


def check_73(df_lc: pd.DataFrame, lab_lc: pd.DataFrame) -> dict:
    """Compare sleep-stress on crash episodes vs normal-day base rate."""
    out = {}

    # ----- Episode-level primary -----
    crash_lab = lab_lc[lab_lc["label"] == "crash"].copy()
    episode_ids = crash_lab["episode_id"].unique()
    episode_means = []
    for eid in episode_ids:
        ep_dates = crash_lab[crash_lab["episode_id"] == eid]["date"]
        vals = df_lc.loc[
            df_lc["date"].isin(ep_dates), "stress_mean_sleep"
        ].dropna()
        if len(vals):
            episode_means.append(
                {
                    "episode_id": eid,
                    "n_days": int(len(ep_dates)),
                    "n_sleep_days_populated": int(len(vals)),
                    "mean_stress_mean_sleep": float(vals.mean()),
                }
            )
    ep_means_arr = np.array([e["mean_stress_mean_sleep"] for e in episode_means])

    # Normal-day base rate from labels_crash_v2 (label == 'normal').
    normal_dates = lab_lc[lab_lc["label"] == "normal"]["date"]
    normal_vals = (
        df_lc.loc[df_lc["date"].isin(normal_dates), "stress_mean_sleep"]
        .dropna()
        .to_numpy()
    )

    if len(ep_means_arr) >= 2 and len(normal_vals) >= 2:
        ep_lo, ep_hi = bootstrap_ci_mean(ep_means_arr)
        nm_lo, nm_hi = bootstrap_ci_mean(normal_vals)
        diff_lo, diff_hi = bootstrap_ci_diff(ep_means_arr, normal_vals)
        d = cohens_d(ep_means_arr, normal_vals)
        u = stats.mannwhitneyu(
            ep_means_arr, normal_vals, alternative="two-sided"
        )
    else:
        ep_lo = ep_hi = nm_lo = nm_hi = diff_lo = diff_hi = d = float("nan")
        u = type("U", (), {"statistic": float("nan"), "pvalue": float("nan")})()

    out["episode_level_primary"] = {
        "n_crash_episodes": int(len(ep_means_arr)),
        "n_normal_days_base_rate": int(len(normal_vals)),
        "mean_crash_episode_stress_mean_sleep": (
            float(ep_means_arr.mean()) if len(ep_means_arr) else float("nan")
        ),
        "mean_normal_day_stress_mean_sleep": (
            float(normal_vals.mean()) if len(normal_vals) else float("nan")
        ),
        "ci_crash_episodes": [ep_lo, ep_hi],
        "ci_normal_days": [nm_lo, nm_hi],
        "mean_diff_crash_minus_normal": (
            float(ep_means_arr.mean() - normal_vals.mean())
            if len(ep_means_arr) and len(normal_vals)
            else float("nan")
        ),
        "ci_diff": [diff_lo, diff_hi],
        "cohens_d": d,
        "mann_whitney_u": float(u.statistic),
        "mann_whitney_p": float(u.pvalue),
        "labeling_scheme": "crash_v2",
        "source_file": "labels_crash_v2.csv",
        "unit": "episode (mean across episode days)",
    }

    # ----- Day-level supplementary -----
    crash_dates = crash_lab["date"]
    crash_vals = (
        df_lc.loc[df_lc["date"].isin(crash_dates), "stress_mean_sleep"]
        .dropna()
        .to_numpy()
    )

    if len(crash_vals) >= 2 and len(normal_vals) >= 2:
        cd_lo, cd_hi = bootstrap_ci_mean(crash_vals)
        diff_lo_d, diff_hi_d = bootstrap_ci_diff(crash_vals, normal_vals)
        d_day = cohens_d(crash_vals, normal_vals)
        u_day = stats.mannwhitneyu(
            crash_vals, normal_vals, alternative="two-sided"
        )
    else:
        cd_lo = cd_hi = diff_lo_d = diff_hi_d = d_day = float("nan")
        u_day = type("U", (), {"statistic": float("nan"), "pvalue": float("nan")})()

    out["day_level_supplementary"] = {
        "n_crash_days": int(len(crash_vals)),
        "n_normal_days": int(len(normal_vals)),
        "mean_crash_day_stress_mean_sleep": (
            float(crash_vals.mean()) if len(crash_vals) else float("nan")
        ),
        "mean_normal_day_stress_mean_sleep": (
            float(normal_vals.mean()) if len(normal_vals) else float("nan")
        ),
        "ci_crash_days": [cd_lo, cd_hi],
        "mean_diff_crash_minus_normal": (
            float(crash_vals.mean() - normal_vals.mean())
            if len(crash_vals) and len(normal_vals)
            else float("nan")
        ),
        "ci_diff": [diff_lo_d, diff_hi_d],
        "cohens_d": d_day,
        "mann_whitney_u": float(u_day.statistic),
        "mann_whitney_p": float(u_day.pvalue),
        "labeling_scheme": "crash_v2",
        "source_file": "labels_crash_v2.csv",
        "unit": "day",
        "caveat": "consecutive within-episode days are autocorrelated; "
                  "treat n=crash-days as effective sample inflated vs n=episodes",
    }

    return out


# ---------------------------------------------------------------------------
# Bonus - stress_stdev_sleep independence sanity-check
# ---------------------------------------------------------------------------


def stdev_independence(df_lc: pd.DataFrame) -> dict:
    """Regress stress_stdev_sleep ~ stress_mean_sleep; report R-squared."""
    s = df_lc.dropna(subset=["stress_mean_sleep", "stress_stdev_sleep"])
    x = s["stress_mean_sleep"].to_numpy(dtype=float)
    y = s["stress_stdev_sleep"].to_numpy(dtype=float)
    if len(x) < 4:
        return {"n": int(len(x)), "note": "n < 4, skipped"}
    slope, intercept, r, p, se = stats.linregress(x, y)
    rho_s = stats.spearmanr(x, y)
    return {
        "n": int(len(x)),
        "pearson_r": float(r),
        "spearman_rho": float(rho_s.statistic),
        "r_squared": float(r * r),
        "interpretation_guide": (
            "R-squared > 0.5: SD is largely redundant with mean. "
            "R-squared < 0.3: SD genuinely independent channel. "
            "Between: partial."
        ),
    }


# ---------------------------------------------------------------------------
# Tier 1 extensions: resting_hr_z + stress_stdev_sleep as proxy channels
# Plus composite logistic regression for two-channel discrimination
# ---------------------------------------------------------------------------


def _two_group_compare(
    a: np.ndarray, b: np.ndarray, label_a: str, label_b: str
) -> dict:
    """Bootstrap CI + Cohen's d + Mann-Whitney for two samples."""
    out = {f"n_{label_a}": int(len(a)), f"n_{label_b}": int(len(b))}
    if len(a) >= 2 and len(b) >= 2:
        a_lo, a_hi = bootstrap_ci_mean(a)
        b_lo, b_hi = bootstrap_ci_mean(b)
        d_lo, d_hi = bootstrap_ci_diff(a, b)
        u = stats.mannwhitneyu(a, b, alternative="two-sided")
        out.update({
            f"mean_{label_a}": float(a.mean()),
            f"mean_{label_b}": float(b.mean()),
            f"ci_{label_a}": [a_lo, a_hi],
            f"ci_{label_b}": [b_lo, b_hi],
            "mean_diff": float(a.mean() - b.mean()),
            "ci_diff": [d_lo, d_hi],
            "cohens_d": cohens_d(a, b),
            "mann_whitney_p": float(u.pvalue),
        })
    return out


def check_71_b_resting_hr_z(df_lc: pd.DataFrame) -> dict:
    """resting_hr_z on heavy-exertion vs rest days (LC era)."""
    sub = df_lc.dropna(
        subset=["resting_hr_z", "exertion_class_lagged_lcera"]
    ).copy()
    heavy = sub[sub["exertion_class_lagged_lcera"].isin(HEAVY_CLASSES)][
        "resting_hr_z"
    ].to_numpy()
    rest = sub[sub["exertion_class_lagged_lcera"].isin(REST_CLASSES)][
        "resting_hr_z"
    ].to_numpy()
    out = _two_group_compare(heavy, rest, "heavy", "rest")
    out["channel"] = "resting_hr_z"
    out["predictor"] = "exertion_class_lagged_lcera"
    out["baseline_window"] = (
        f"[d-{Z_WINDOW_END_DAYS}, d-{Z_WINDOW_START_DAYS+1}]; "
        f"min_n={Z_MIN_LAGGED_DAYS}, trim={Z_TRIMMED_PCT:.0%}"
    )
    return out


def check_71_c_stress_stdev(df_lc: pd.DataFrame) -> dict:
    """stress_stdev_sleep on heavy-exertion vs rest days (LC era)."""
    sub = df_lc.dropna(
        subset=["stress_stdev_sleep", "exertion_class_lagged_lcera"]
    ).copy()
    heavy = sub[sub["exertion_class_lagged_lcera"].isin(HEAVY_CLASSES)][
        "stress_stdev_sleep"
    ].to_numpy()
    rest = sub[sub["exertion_class_lagged_lcera"].isin(REST_CLASSES)][
        "stress_stdev_sleep"
    ].to_numpy()
    out = _two_group_compare(heavy, rest, "heavy", "rest")
    out["channel"] = "stress_stdev_sleep"
    out["predictor"] = "exertion_class_lagged_lcera"
    return out


def _episode_mean_channel(
    df_lc: pd.DataFrame, lab_lc: pd.DataFrame, channel: str
) -> tuple[np.ndarray, np.ndarray]:
    """Returns (per-episode means on crash episodes, per-day normal-day values)."""
    crash_lab = lab_lc[lab_lc["label"] == "crash"]
    episode_means = []
    for eid in crash_lab["episode_id"].unique():
        ep_dates = crash_lab[crash_lab["episode_id"] == eid]["date"]
        vals = df_lc.loc[df_lc["date"].isin(ep_dates), channel].dropna()
        if len(vals):
            episode_means.append(float(vals.mean()))
    normal_dates = lab_lc[lab_lc["label"] == "normal"]["date"]
    normal_vals = (
        df_lc.loc[df_lc["date"].isin(normal_dates), channel]
        .dropna()
        .to_numpy()
    )
    return np.array(episode_means), normal_vals


def check_73_b_resting_hr_z(df_lc: pd.DataFrame, lab_lc: pd.DataFrame) -> dict:
    """resting_hr_z per crash episode vs normal-day base rate (LC era)."""
    ep_means, normal_vals = _episode_mean_channel(df_lc, lab_lc, "resting_hr_z")
    out = _two_group_compare(ep_means, normal_vals, "crash_ep", "normal")
    out["channel"] = "resting_hr_z"
    out["unit"] = "episode (mean across episode days)"
    out["labeling_scheme"] = "crash_v2"
    return out


def check_73_c_stress_stdev(
    df_lc: pd.DataFrame, lab_lc: pd.DataFrame
) -> dict:
    """stress_stdev_sleep per crash episode vs normal-day base rate (LC era)."""
    ep_means, normal_vals = _episode_mean_channel(
        df_lc, lab_lc, "stress_stdev_sleep"
    )
    out = _two_group_compare(ep_means, normal_vals, "crash_ep", "normal")
    out["channel"] = "stress_stdev_sleep"
    out["unit"] = "episode (mean across episode days)"
    out["labeling_scheme"] = "crash_v2"
    return out


def check_75_composite(df_lc: pd.DataFrame) -> dict:
    """Multi-model composite comparison for crash discrimination.

    Day-level logistic regression on a single common sample (all
    channels populated), so AUCs are apples-to-apples.

    Models:
      m1: is_crash ~ resting_hr_z
      m2: is_crash ~ stress_mean_sleep
      m3: is_crash ~ resting_hr_z + stress_mean_sleep      (original Tier 1)
      m4: is_crash ~ stress_stdev_sleep
      m5: is_crash ~ stress_mean_sleep + stress_stdev_sleep (mean+SD)
      m6: is_crash ~ resting_hr_z + stress_mean_sleep
          + stress_stdev_sleep                              (full Tier 1)
    """
    sub = df_lc.dropna(
        subset=[
            "resting_hr_z",
            "stress_mean_sleep",
            "stress_stdev_sleep",
            "is_crash",
        ]
    ).copy()
    if len(sub) < 50:
        return {"note": f"insufficient sample after dropna (n={len(sub)})"}
    y = sub["is_crash"].astype(int).to_numpy()
    rhz = sub["resting_hr_z"].to_numpy(dtype=float)
    sms = sub["stress_mean_sleep"].to_numpy(dtype=float)
    sss = sub["stress_stdev_sleep"].to_numpy(dtype=float)
    intercept = np.ones(len(y))

    def _fit(cols: list[np.ndarray], names: list[str]) -> dict:
        X = np.column_stack([intercept, *cols])
        b, se = logistic_irls(X, y)
        scores = X @ b
        auc = auc_score(y, scores)
        d = {"beta_intercept": float(b[0]), "se_intercept": float(se[0])}
        for i, name in enumerate(names, start=1):
            d[f"beta_{name}"] = float(b[i])
            d[f"se_{name}"] = float(se[i])
        d["auc"] = auc
        return d

    m1 = _fit([rhz], ["resting_hr_z"])
    m2 = _fit([sms], ["stress_mean_sleep"])
    m3 = _fit([rhz, sms], ["resting_hr_z", "stress_mean_sleep"])
    m4 = _fit([sss], ["stress_stdev_sleep"])
    m5 = _fit([sms, sss], ["stress_mean_sleep", "stress_stdev_sleep"])
    m6 = _fit(
        [rhz, sms, sss],
        ["resting_hr_z", "stress_mean_sleep", "stress_stdev_sleep"],
    )

    return {
        "n_days": int(len(y)),
        "n_crash_days": int(y.sum()),
        "sample_subset": (
            "all 4 channels populated: resting_hr_z + stress_mean_sleep + "
            "stress_stdev_sleep + is_crash"
        ),
        "m1_resting_hr_z": m1,
        "m2_stress_mean_sleep": m2,
        "m3_joint_rhz_sms": m3,
        "m4_stress_stdev_sleep": m4,
        "m5_joint_sms_sss": m5,
        "m6_joint_all_three": m6,
        "incremental_auc": {
            "m3_over_best_single_of_m1m2": float(
                m3["auc"] - max(m1["auc"], m2["auc"])
            ),
            "m5_over_best_single_of_m2m4": float(
                m5["auc"] - max(m2["auc"], m4["auc"])
            ),
            "m6_over_m3": float(m6["auc"] - m3["auc"]),
            "m6_over_m5": float(m6["auc"] - m5["auc"]),
            "m6_over_best_single": float(
                m6["auc"] - max(m1["auc"], m2["auc"], m4["auc"])
            ),
        },
        "note": (
            "Day-level. Within-episode autocorrelation inflates effective n. "
            "AUC is in-sample (no walk-forward). Use as descriptive "
            "comparison of single-channel vs joint discrimination only."
        ),
    }


# ---------------------------------------------------------------------------
# Pre-covid sanity-check endpoint
# ---------------------------------------------------------------------------


def precovid_endpoint(df: pd.DataFrame) -> dict:
    """Report mean stress_mean_sleep in pre-covid era as healthy-baseline."""
    pre = df[df["date"] < INFECTION_START].dropna(subset=["stress_mean_sleep"])
    lc_normal_mean = (
        df[(df["date"] >= LC_START) & (df.get("is_crash", False) == False)][
            "stress_mean_sleep"
        ]
        .dropna()
        .mean()
    )
    if len(pre) < 2:
        return {"n": int(len(pre)), "note": "insufficient pre-covid coverage"}
    x = pre["stress_mean_sleep"].to_numpy()
    lo, hi = bootstrap_ci_mean(x)
    return {
        "n_pre_covid_days": int(len(pre)),
        "mean_stress_mean_sleep_pre_covid": float(x.mean()),
        "ci_pre_covid": [lo, hi],
        "mean_stress_mean_sleep_lc_non_crash": float(lc_normal_mean),
        "note": (
            "Pre-covid is a sanity-check endpoint only (no crash labels). "
            "Comparison to LC non-crash days indicates whether overall "
            "autonomic state differs between healthy and LC regimes."
        ),
    }


# ---------------------------------------------------------------------------
# Output rendering
# ---------------------------------------------------------------------------


def render_table(results: dict) -> str:
    lines = []
    add = lines.append

    add("=" * 78)
    add("HRV PROXY VALIDATION - DESCRIPTIVE CHECKS 7.1 / 7.2 / 7.3")
    add("=" * 78)
    add("Source: per_day_master.csv (LC era 2022-04-04 onward unless noted)")
    add("Labeling scheme for crash events: crash_v2 in labels_crash_v2.csv")
    add(f"Bootstrap iterations for CIs: {N_BOOTSTRAP} (seed {BOOTSTRAP_SEED})")
    add("")
    add(f"Run summary: {results['run_summary']}")
    add("")

    # Coverage
    cov = results["coverage"]
    add("-" * 78)
    add("COVERAGE (LC era only)")
    add("-" * 78)
    add(f"  LC days total: {cov['lc_days_total']}")
    add(f"  stress_mean_sleep populated: {cov['stress_mean_sleep_populated']}")
    add(f"  resting_hr populated:        {cov['resting_hr_populated']}")
    add(f"  exertion_class_lagged_lcera populated: "
        f"{cov['exertion_class_populated']}")
    add(
        f"  is_crash=True days (crash_v2 label=='crash'): "
        f"{cov['is_crash_days']}"
    )
    add(f"  crash episodes (crash_v2 unique crash-NNN ids): "
        f"{cov['n_crash_episodes']}")
    add("")

    # Check 7.1
    r71 = results["check_71"]
    add("-" * 78)
    add("CHECK 7.1 - Sleep-stress on heavy-exertion vs rest days (LC era)")
    add("           Predictor: exertion_class_lagged_lcera (v3.2)")
    add("           Outcome:   stress_mean_sleep")
    add("-" * 78)
    add(f"  n heavy + very_heavy days: {r71['n_heavy']}")
    add(f"  n moderate days:            {r71['n_moderate']}")
    add(f"  n light + none days:        {r71['n_rest']}")
    add(f"  mean stress_mean_sleep (heavy):    "
        f"{r71['mean_heavy']:.2f}  CI95 [{r71['ci_heavy'][0]:.2f}, "
        f"{r71['ci_heavy'][1]:.2f}]")
    add(f"  mean stress_mean_sleep (moderate): "
        f"{r71['mean_moderate']:.2f}")
    add(f"  mean stress_mean_sleep (rest):     "
        f"{r71['mean_rest']:.2f}  CI95 [{r71['ci_rest'][0]:.2f}, "
        f"{r71['ci_rest'][1]:.2f}]")
    add(f"  mean diff (heavy - rest):  "
        f"{r71['mean_diff_heavy_minus_rest']:+.2f}  "
        f"CI95 [{r71['ci_diff'][0]:+.2f}, {r71['ci_diff'][1]:+.2f}]")
    add(f"  Cohen's d:                 {r71['cohens_d']:+.3f}")
    add(f"  Mann-Whitney U p (context): {r71['mann_whitney_p']:.4f}")
    add("")

    # Check 7.1b
    r71b = results["check_71b_resting_hr_z"]
    add("-" * 78)
    add("CHECK 7.1b - resting_hr_z on heavy-exertion vs rest days (LC era)")
    add("            Per [[feedback_relative_not_absolute]] — z-scored vs")
    add(f"            personal baseline: {r71b.get('baseline_window', 'n/a')}")
    add("-" * 78)
    if "mean_diff" in r71b:
        add(f"  n heavy: {r71b['n_heavy']}    n rest: {r71b['n_rest']}")
        add(f"  mean resting_hr_z (heavy): {r71b['mean_heavy']:+.3f}  "
            f"CI95 [{r71b['ci_heavy'][0]:+.3f}, "
            f"{r71b['ci_heavy'][1]:+.3f}]")
        add(f"  mean resting_hr_z (rest):  {r71b['mean_rest']:+.3f}  "
            f"CI95 [{r71b['ci_rest'][0]:+.3f}, "
            f"{r71b['ci_rest'][1]:+.3f}]")
        add(f"  mean diff (heavy - rest):  {r71b['mean_diff']:+.3f}  "
            f"CI95 [{r71b['ci_diff'][0]:+.3f}, "
            f"{r71b['ci_diff'][1]:+.3f}]")
        add(f"  Cohen's d: {r71b['cohens_d']:+.3f}")
        add(f"  Mann-Whitney U p (context): {r71b['mann_whitney_p']:.4f}")
    else:
        add("  insufficient sample sizes")
    add("")

    # Check 7.1c
    r71c = results["check_71c_stress_stdev_sleep"]
    add("-" * 78)
    add("CHECK 7.1c - stress_stdev_sleep on heavy-exertion vs rest days (LC era)")
    add("-" * 78)
    if "mean_diff" in r71c:
        add(f"  n heavy: {r71c['n_heavy']}    n rest: {r71c['n_rest']}")
        add(f"  mean stress_stdev_sleep (heavy): "
            f"{r71c['mean_heavy']:.2f}  "
            f"CI95 [{r71c['ci_heavy'][0]:.2f}, "
            f"{r71c['ci_heavy'][1]:.2f}]")
        add(f"  mean stress_stdev_sleep (rest):  "
            f"{r71c['mean_rest']:.2f}  "
            f"CI95 [{r71c['ci_rest'][0]:.2f}, "
            f"{r71c['ci_rest'][1]:.2f}]")
        add(f"  mean diff (heavy - rest): {r71c['mean_diff']:+.3f}  "
            f"CI95 [{r71c['ci_diff'][0]:+.3f}, "
            f"{r71c['ci_diff'][1]:+.3f}]")
        add(f"  Cohen's d: {r71c['cohens_d']:+.3f}")
    else:
        add("  insufficient sample sizes")
    add("")

    # Check 7.2
    r72 = results["check_72"]
    add("-" * 78)
    add("CHECK 7.2 - HR-confound separability (LC era)")
    add("           Question: how much of stress_mean_sleep is unique vs RHR?")
    add("           Run twice: all LC, and LC with crash days dropped")
    add("           (crash_distortion_sensitivity)")
    add("-" * 78)
    for label in ["all_lc", "lc_no_crash_days"]:
        b = r72[label]
        if "note" in b:
            add(f"  [{label}] {b['note']} (n={b['n']})")
            continue
        add(f"  [{label}]  n = {b['n']}")
        add(f"    Pearson r (stress_mean_sleep vs resting_hr):  "
            f"{b['pearson_r']:+.3f}  (p={b['pearson_p']:.4f})")
        add(f"    Spearman rho:                                  "
            f"{b['spearman_rho']:+.3f}  (p={b['spearman_p']:.4f})")
        add(f"    R-squared (linear, y~x):                       "
            f"{b['r_squared']:.3f}")
        add(f"    Unique variance in stress_mean_sleep:          "
            f"{b['unique_variance_in_stress_mean_sleep']:.3f}")
        add(f"    Slope (stress points per bpm):                 "
            f"{b['slope_stress_per_bpm']:+.3f}  (SE {b['slope_se']:.3f})")
        add("")

    # Check 7.3
    r73 = results["check_73"]
    add("-" * 78)
    add("CHECK 7.3 - Sleep-stress on crash events (LC era)")
    add("           Primary unit: crash EPISODE (crash_v2 unique crash-NNN)")
    add("           Supplementary: crash DAY (autocorrelation-inflated)")
    add("-" * 78)
    ep = r73["episode_level_primary"]
    add(f"  [episode-level primary]")
    add(f"    n crash-episodes: {ep['n_crash_episodes']}")
    add(f"    n normal-day base rate: {ep['n_normal_days_base_rate']}")
    add(f"    mean per-episode stress_mean_sleep:  "
        f"{ep['mean_crash_episode_stress_mean_sleep']:.2f}  "
        f"CI95 [{ep['ci_crash_episodes'][0]:.2f}, "
        f"{ep['ci_crash_episodes'][1]:.2f}]")
    add(f"    mean normal-day stress_mean_sleep:    "
        f"{ep['mean_normal_day_stress_mean_sleep']:.2f}  "
        f"CI95 [{ep['ci_normal_days'][0]:.2f}, "
        f"{ep['ci_normal_days'][1]:.2f}]")
    add(f"    mean diff (crash episodes - normal):  "
        f"{ep['mean_diff_crash_minus_normal']:+.2f}  "
        f"CI95 [{ep['ci_diff'][0]:+.2f}, {ep['ci_diff'][1]:+.2f}]")
    add(f"    Cohen's d:                            {ep['cohens_d']:+.3f}")
    add(f"    Mann-Whitney U p (context):           "
        f"{ep['mann_whitney_p']:.4f}")
    add("")
    dy = r73["day_level_supplementary"]
    add(f"  [day-level supplementary]")
    add(f"    n crash-days: {dy['n_crash_days']}")
    add(f"    n normal-days: {dy['n_normal_days']}")
    add(f"    mean crash-day stress_mean_sleep:     "
        f"{dy['mean_crash_day_stress_mean_sleep']:.2f}  "
        f"CI95 [{dy['ci_crash_days'][0]:.2f}, "
        f"{dy['ci_crash_days'][1]:.2f}]")
    add(f"    mean diff (crash days - normal):      "
        f"{dy['mean_diff_crash_minus_normal']:+.2f}  "
        f"CI95 [{dy['ci_diff'][0]:+.2f}, {dy['ci_diff'][1]:+.2f}]")
    add(f"    Cohen's d:                            {dy['cohens_d']:+.3f}")
    add(f"    NOTE: {dy['caveat']}")
    add("")

    # Check 7.3b
    r73b = results["check_73b_resting_hr_z"]
    add("-" * 78)
    add("CHECK 7.3b - resting_hr_z per crash episode vs normal-day base rate")
    add("-" * 78)
    if "mean_diff" in r73b:
        add(f"  n crash episodes: {r73b['n_crash_ep']}    "
            f"n normal days: {r73b['n_normal']}")
        add(f"  mean resting_hr_z (crash episodes): "
            f"{r73b['mean_crash_ep']:+.3f}  "
            f"CI95 [{r73b['ci_crash_ep'][0]:+.3f}, "
            f"{r73b['ci_crash_ep'][1]:+.3f}]")
        add(f"  mean resting_hr_z (normal days):    "
            f"{r73b['mean_normal']:+.3f}  "
            f"CI95 [{r73b['ci_normal'][0]:+.3f}, "
            f"{r73b['ci_normal'][1]:+.3f}]")
        add(f"  mean diff (crash - normal): {r73b['mean_diff']:+.3f}  "
            f"CI95 [{r73b['ci_diff'][0]:+.3f}, "
            f"{r73b['ci_diff'][1]:+.3f}]")
        add(f"  Cohen's d: {r73b['cohens_d']:+.3f}")
        add(f"  Mann-Whitney U p (context): {r73b['mann_whitney_p']:.4f}")
    else:
        add("  insufficient sample sizes")
    add("")

    # Check 7.3c
    r73c = results["check_73c_stress_stdev_sleep"]
    add("-" * 78)
    add("CHECK 7.3c - stress_stdev_sleep per crash episode vs normal-day base")
    add("-" * 78)
    if "mean_diff" in r73c:
        add(f"  n crash episodes: {r73c['n_crash_ep']}    "
            f"n normal days: {r73c['n_normal']}")
        add(f"  mean stress_stdev_sleep (crash episodes): "
            f"{r73c['mean_crash_ep']:.2f}  "
            f"CI95 [{r73c['ci_crash_ep'][0]:.2f}, "
            f"{r73c['ci_crash_ep'][1]:.2f}]")
        add(f"  mean stress_stdev_sleep (normal days):    "
            f"{r73c['mean_normal']:.2f}  "
            f"CI95 [{r73c['ci_normal'][0]:.2f}, "
            f"{r73c['ci_normal'][1]:.2f}]")
        add(f"  mean diff (crash - normal): {r73c['mean_diff']:+.3f}  "
            f"CI95 [{r73c['ci_diff'][0]:+.3f}, "
            f"{r73c['ci_diff'][1]:+.3f}]")
        add(f"  Cohen's d: {r73c['cohens_d']:+.3f}")
    else:
        add("  insufficient sample sizes")
    add("")

    # Check 7.5 composite
    r75 = results["check_75_composite"]
    add("-" * 78)
    add("CHECK 7.5 - Composite logistic discrimination of is_crash (LC era)")
    add("           Day-level. Common sample across all 6 models.")
    add("-" * 78)
    if "note" in r75 and "n_days" not in r75:
        add(f"  {r75['note']}")
    else:
        add(f"  n_days = {r75['n_days']}  (crash days: {r75['n_crash_days']})")
        add(f"  sample: {r75['sample_subset']}")
        add("")
        add(f"  {'model':40} {'AUC':>6}  details")
        m1 = r75["m1_resting_hr_z"]
        m2 = r75["m2_stress_mean_sleep"]
        m3 = r75["m3_joint_rhz_sms"]
        m4 = r75["m4_stress_stdev_sleep"]
        m5 = r75["m5_joint_sms_sss"]
        m6 = r75["m6_joint_all_three"]
        add(f"  {'M1: resting_hr_z':40} {m1['auc']:>6.3f}  "
            f"b={m1['beta_resting_hr_z']:+.3f} (SE {m1['se_resting_hr_z']:.3f})")
        add(f"  {'M2: stress_mean_sleep':40} {m2['auc']:>6.3f}  "
            f"b={m2['beta_stress_mean_sleep']:+.4f} "
            f"(SE {m2['se_stress_mean_sleep']:.4f})")
        add(f"  {'M3: rhz + stress_mean_sleep':40} {m3['auc']:>6.3f}  "
            f"b_rhz={m3['beta_resting_hr_z']:+.3f}, "
            f"b_sms={m3['beta_stress_mean_sleep']:+.4f}")
        add(f"  {'M4: stress_stdev_sleep':40} {m4['auc']:>6.3f}  "
            f"b={m4['beta_stress_stdev_sleep']:+.4f} "
            f"(SE {m4['se_stress_stdev_sleep']:.4f})")
        add(f"  {'M5: stress_mean + stress_stdev':40} {m5['auc']:>6.3f}  "
            f"b_sms={m5['beta_stress_mean_sleep']:+.4f}, "
            f"b_sss={m5['beta_stress_stdev_sleep']:+.4f}")
        add(f"  {'M6: rhz + sms + sss (full Tier 1)':40} {m6['auc']:>6.3f}  "
            f"b_rhz={m6['beta_resting_hr_z']:+.3f}, "
            f"b_sms={m6['beta_stress_mean_sleep']:+.4f}, "
            f"b_sss={m6['beta_stress_stdev_sleep']:+.4f}")
        inc = r75["incremental_auc"]
        add("")
        add(f"  Incremental AUC:")
        add(f"    M3 over best single of {{M1,M2}}: "
            f"{inc['m3_over_best_single_of_m1m2']:+.4f}")
        add(f"    M5 over best single of {{M2,M4}}: "
            f"{inc['m5_over_best_single_of_m2m4']:+.4f}")
        add(f"    M6 over M3:                       {inc['m6_over_m3']:+.4f}")
        add(f"    M6 over M5:                       {inc['m6_over_m5']:+.4f}")
        add(f"    M6 over best single overall:      "
            f"{inc['m6_over_best_single']:+.4f}")
        add(f"  NOTE: {r75['note']}")
    add("")

    # Bonus
    bz = results["stdev_independence"]
    add("-" * 78)
    add("BONUS - stress_stdev_sleep independence sanity-check (LC era)")
    add("        Question: does stress_stdev_sleep carry information")
    add("        independent of stress_mean_sleep, or is it just")
    add("        heteroscedasticity?")
    add("-" * 78)
    if "note" in bz:
        add(f"  {bz['note']}")
    else:
        add(f"  n = {bz['n']}")
        add(f"  Pearson r: {bz['pearson_r']:+.3f}")
        add(f"  Spearman rho: {bz['spearman_rho']:+.3f}")
        add(f"  R-squared: {bz['r_squared']:.3f}")
        add(f"  {bz['interpretation_guide']}")
    add("")

    # Pre-covid endpoint
    pc = results["precovid_endpoint"]
    add("-" * 78)
    add("PRE-COVID ENDPOINT (sanity-check; no crash labels)")
    add("-" * 78)
    if "note" in pc and "insufficient" in pc["note"]:
        add(f"  {pc['note']}")
    else:
        add(f"  n pre-covid days: {pc['n_pre_covid_days']}")
        add(f"  mean stress_mean_sleep (pre-covid):    "
            f"{pc['mean_stress_mean_sleep_pre_covid']:.2f}  "
            f"CI95 [{pc['ci_pre_covid'][0]:.2f}, "
            f"{pc['ci_pre_covid'][1]:.2f}]")
        add(f"  mean stress_mean_sleep (LC non-crash): "
            f"{pc['mean_stress_mean_sleep_lc_non_crash']:.2f}")
        add(f"  {pc['note']}")
    add("")
    add("=" * 78)
    add("END OF REPORT")
    add("=" * 78)
    add("")
    add("Reading guide:")
    add("  - This is a descriptive characterisation. No verdicts on")
    add("    whether the HRV proxy 'works' are made here.")
    add("  - Use the effect sizes + CIs to judge whether each check's")
    add("    direction supports the proxy, with the explicit caveats")
    add("    in hrv_proxy_via_stress.md section 7.")
    add("  - Decision rules for proxy unblock live in the methodology")
    add("    doc section 9, not in this script.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    print("Loading data...")
    df, lab = load_data()
    df_lc = df[df["date"] >= LC_START].copy()
    lab_lc = lab[lab["date"] >= LC_START].copy()
    df_lc_no_crash = df_lc[df_lc["is_crash"] == False].copy()

    cov = {
        "lc_days_total": int(len(df_lc)),
        "stress_mean_sleep_populated": int(df_lc["stress_mean_sleep"].notna().sum()),
        "resting_hr_populated": int(df_lc["resting_hr"].notna().sum()),
        "exertion_class_populated": int(
            df_lc["exertion_class_lagged_lcera"].notna().sum()
        ),
        "is_crash_days": int(df_lc["is_crash"].sum()),
        "n_crash_episodes": int(
            lab_lc.loc[lab_lc["label"] == "crash", "episode_id"].nunique()
        ),
    }

    print("Computing resting_hr_z (trailing-window personal baseline)...")
    df = compute_resting_hr_z(df)
    df_lc = df[df["date"] >= LC_START].copy()
    df_lc_no_crash = df_lc[df_lc["is_crash"] == False].copy()
    n_rhz = int(df_lc["resting_hr_z"].notna().sum())
    print(f"  resting_hr_z populated in LC: {n_rhz} / {len(df_lc)}")

    print("Running Check 7.1...")
    r71 = check_71(df_lc)
    print("Running Check 7.1b (resting_hr_z on heavy vs rest)...")
    r71b = check_71_b_resting_hr_z(df_lc)
    print("Running Check 7.1c (stress_stdev_sleep on heavy vs rest)...")
    r71c = check_71_c_stress_stdev(df_lc)
    print("Running Check 7.2 (with crash-distortion sensitivity)...")
    r72 = check_72(df_lc, df_lc_no_crash)
    print("Running Check 7.3 (episode-level primary)...")
    r73 = check_73(df_lc, lab_lc)
    print("Running Check 7.3b (resting_hr_z per crash episode)...")
    r73b = check_73_b_resting_hr_z(df_lc, lab_lc)
    print("Running Check 7.3c (stress_stdev_sleep per crash episode)...")
    r73c = check_73_c_stress_stdev(df_lc, lab_lc)
    print("Running Check 7.5 (two-channel composite logistic)...")
    r75 = check_75_composite(df_lc)
    print("Running stress_stdev_sleep independence sanity-check...")
    bz = stdev_independence(df_lc)
    print("Running pre-covid endpoint sanity...")
    pc = precovid_endpoint(df)

    cov["resting_hr_z_populated"] = n_rhz

    results = {
        "run_summary": (
            f"LC era 2022-04-04 onward; n_days={len(df_lc)}; "
            f"crash_episodes={cov['n_crash_episodes']}; "
            f"crash_days={cov['is_crash_days']}"
        ),
        "coverage": cov,
        "check_71": r71,
        "check_71b_resting_hr_z": r71b,
        "check_71c_stress_stdev_sleep": r71c,
        "check_72": r72,
        "check_73": r73,
        "check_73b_resting_hr_z": r73b,
        "check_73c_stress_stdev_sleep": r73c,
        "check_75_composite": r75,
        "stdev_independence": bz,
        "precovid_endpoint": pc,
    }

    txt = render_table(results)
    print()
    print(txt)
    OUT_JSON.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    OUT_TXT.write_text(txt, encoding="utf-8")
    print(f"\nWrote {OUT_JSON.name}")
    print(f"Wrote {OUT_TXT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
