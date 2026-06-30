"""R22 descriptive binned stress->felt-state curve for the Wiggers site.

Replicates the HA-C3p unmedicated x full-Stratum-4 cell (n=581) exactly, then
re-bins all_day_stress_avg into higher-resolution EQUAL-N bands, computes per-band
mean gevoelscore with p25/p75 spread + 95% CI of the mean, a real least-squares
fit line, and a LOESS smooth. Crash-drop sensitivity per CONVENTIONS section 3.4.

Descriptive ONLY. No p-values, no verdict. Aggregated bin-means only.
"""
import os
import math
import json
from datetime import date, datetime
from pathlib import Path

import numpy as np

DATA_ROOT = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH", r"C:\Users\Gebruiker\Documents\gevoelscore-data"))
MASTER_CSV = DATA_ROOT / "unified" / "per_day_master.csv"

LC_ERA_START = date(2022, 4, 4)
UNMEDICATED_END_INCL = date(2024, 4, 8)
APRIL2024_CLUSTER_START = date(2024, 4, 9)
APRIL2024_CLUSTER_END_INCL = date(2024, 4, 16)
DEVICE_BASELINE_DAYS = 21

N_BANDS = 10  # decile equal-N scheme


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


def parse_date(s):
    s = (s or "").strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s[:len(fmt) + 2], fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(s).date()
    except ValueError:
        return None


def load_master():
    import csv
    master = {}
    with open(MASTER_CSV, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            d = parse_date(row.get("date", ""))
            if d is not None:
                master[d] = row
    return master


def find_device_baseline_cutoff(master):
    n_uds = 0
    for d in sorted(master.keys()):
        row = master.get(d) or {}
        if (row.get("has_garmin_uds", "") or "").strip().lower() == "true":
            n_uds += 1
            if n_uds == DEVICE_BASELINE_DAYS:
                return d
    return None


def day_passes_gate(d, row, baseline_cutoff):
    if d < LC_ERA_START:
        return False
    if d > UNMEDICATED_END_INCL:
        return False
    if APRIL2024_CLUSTER_START <= d <= APRIL2024_CLUSTER_END_INCL:
        return False
    if baseline_cutoff is not None and d <= baseline_cutoff:
        return False
    s = parse_float(row.get("all_day_stress_avg", ""))
    if s is None or s < 0.0 or s > 100.0:
        return False
    g = parse_float(row.get("gevoelscore", ""))
    if g is None:
        return False
    return True


def build_pool(master, baseline_cutoff, drop_crashes=False):
    stress, gevoel, crash = [], [], []
    for d in sorted(master.keys()):
        row = master.get(d) or {}
        if not day_passes_gate(d, row, baseline_cutoff):
            continue
        is_crash = (row.get("is_crash", "") or "").strip().lower() == "true"
        if drop_crashes and is_crash:
            continue
        stress.append(parse_float(row["all_day_stress_avg"]))
        gevoel.append(parse_float(row["gevoelscore"]))
        crash.append(is_crash)
    return (np.asarray(stress, dtype=float),
            np.asarray(gevoel, dtype=float),
            np.asarray(crash, dtype=bool))


def equal_n_bins(stress, gevoel, n_bands):
    """Assign each day to one of n_bands equal-N quantile bands of stress.

    Returns list of dicts per band: x_label, n, mean, median, lo (p25), hi (p75),
    ci_lo, ci_hi (95% CI of the mean), x_center (mean stress in band).
    """
    n = len(stress)
    order = np.argsort(stress, kind="mergesort")
    s_sorted = stress[order]
    g_sorted = gevoel[order]
    # equal-N split by index (handles ties deterministically by position)
    splits = np.array_split(np.arange(n), n_bands)
    bands = []
    for idx in splits:
        s_band = s_sorted[idx]
        g_band = g_sorted[idx]
        nb = len(g_band)
        mean = float(np.mean(g_band))
        sd = float(np.std(g_band, ddof=1)) if nb > 1 else 0.0
        se = sd / math.sqrt(nb) if nb > 0 else 0.0
        ci = 1.96 * se
        s_lo = float(s_band.min())
        s_hi = float(s_band.max())
        bands.append({
            "x_lo_stress": round(s_lo, 1),
            "x_hi_stress": round(s_hi, 1),
            "x_center": round(float(np.mean(s_band)), 2),
            "n": int(nb),
            "mean": round(mean, 3),
            "median": round(float(np.median(g_band)), 2),
            "p25": round(float(np.percentile(g_band, 25)), 3),
            "p75": round(float(np.percentile(g_band, 75)), 3),
            "ci_lo": round(mean - ci, 3),
            "ci_hi": round(mean + ci, 3),
        })
    return bands


def least_squares_fit(stress, gevoel):
    """Real OLS fit; return endpoints at min/max observed stress."""
    A = np.vstack([stress, np.ones_like(stress)]).T
    slope, intercept = np.linalg.lstsq(A, gevoel, rcond=None)[0]
    x0 = float(stress.min())
    x1 = float(stress.max())
    return {
        "x0": round(x0, 2), "y0": round(float(slope * x0 + intercept), 3),
        "x1": round(x1, 2), "y1": round(float(slope * x1 + intercept), 3),
        "slope": round(float(slope), 5), "intercept": round(float(intercept), 4),
    }


def loess(stress, gevoel, n_points=25, frac=0.5):
    """Simple tricube-weighted local linear LOESS over an evenly spaced grid."""
    order = np.argsort(stress)
    xs = stress[order]
    ys = gevoel[order]
    n = len(xs)
    k = max(2, int(frac * n))
    grid = np.linspace(xs.min(), xs.max(), n_points)
    out = []
    for x0 in grid:
        dist = np.abs(xs - x0)
        idx = np.argsort(dist)[:k]
        d = dist[idx]
        dmax = d.max() if d.max() > 0 else 1.0
        w = (1 - (d / dmax) ** 3) ** 3
        xw = xs[idx]
        yw = ys[idx]
        # weighted local linear
        W = np.diag(w)
        X = np.vstack([np.ones_like(xw), xw]).T
        try:
            beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ yw)
            yhat = beta[0] + beta[1] * x0
        except np.linalg.LinAlgError:
            yhat = float(np.average(yw, weights=w))
        out.append({"x": round(float(x0), 2), "y": round(float(yhat), 3)})
    return out


def main():
    master = load_master()
    cutoff = find_device_baseline_cutoff(master)
    stress, gevoel, crash = build_pool(master, cutoff, drop_crashes=False)
    n_full = len(gevoel)
    n_crash = int(crash.sum())

    bands = equal_n_bins(stress, gevoel, N_BANDS)
    fit = least_squares_fit(stress, gevoel)
    smooth = loess(stress, gevoel)

    # crash-drop sensitivity
    s_nc, g_nc, _ = build_pool(master, cutoff, drop_crashes=True)
    bands_nc = equal_n_bins(s_nc, g_nc, N_BANDS)
    fit_nc = least_squares_fit(s_nc, g_nc)
    n_nocrash = len(g_nc)

    result = {
        "device_baseline_cutoff": str(cutoff),
        "n_full": n_full,
        "n_crash": n_crash,
        "n_nocrash": n_nocrash,
        "stress_min": round(float(stress.min()), 2),
        "stress_max": round(float(stress.max()), 2),
        "gevoel_median": round(float(np.median(gevoel)), 2),
        "bands_full": bands,
        "fit_full": fit,
        "smooth_full": smooth,
        "bands_nocrash": bands_nc,
        "fit_nocrash": fit_nc,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
