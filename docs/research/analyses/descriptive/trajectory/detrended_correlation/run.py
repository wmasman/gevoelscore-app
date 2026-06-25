"""Q4.5.b -- detrended_correlation: methodological sanity check on Q3.9.e + Q4.9 rho findings.

METHODOLOGICAL SANITY CHECK per descriptive README sec 4.5.b (r2 closure
D3.4) + CONVENTIONS sec 3.7 trajectory-detrend sensitivity discipline.
For each pair where both channels show a multi-year trajectory, how much
of the raw rho is within-window co-variation vs shared trajectory?

USER-LOCKED OPERATIONALISATION (per Strand B sec 7c interview 2026-06-25;
do NOT iterate):

1. Detrend method = (d) ALL 3 methods + sensitivity:
   - Linear OLS (CONVENTIONS sec 3.7 default)
   - LOESS / rolling-median (90d window)
   - Per-recovery-phase residual (subtract phase mean per row)

2. Channel-pair scope = (b) 7x7 matrix (21 unique pairs):
   - stress_mean_sleep
   - all_day_stress_avg
   - bb_lowest
   - stress_stdev_sleep
   - stress_low_motion_min_count_S60_Mlow
   - resting_hr
   - gevoelscore

3. Detrend granularity = (c) both full-corpus + per-recovery-phase

4. Spurious-correlation flag threshold = |delta_rho| >= 0.1 per
   CONVENTIONS sec 3.7 + HA precedent

OUTPUTS (3 artefacts per handoff sec 3.2 Stage 7):

- Rho matrix side-by-side (raw vs 3 detrended methods x per-phase variant)
- Spurious-correlation flag table (pairs with |delta_rho| >= 0.1 in any
  method + which method drove the flag)
- Methodology-sensitivity report (does detrend method choice
  systematically alter conclusions?)

CROSS-REFERENCES LOAD-BEARING (per handoff sec 3.3):

- Q3.9.e + Q4.9 method (c) rho ranking REPRODUCED in Stage 2 (verification
  check): stress_mean_sleep -0.194 / stress_stdev_sleep -0.121 /
  all_day_stress_avg -0.056 / resting_hr +0.020 / bb_lowest +0.010
- Q4.3 rp5 finding: rp5 (citalopram start) is strongest boundary; the
  multi-year arc carries substantial citalopram-step component; therefore
  linear OLS detrend on full corpus may cancel multi-year-arc structure
  but per-recovery-phase detrend would preserve within-phase content
- Tier 1+2 E[L]* spread: long-memory channels (4 with ~29-30d) are MORE
  likely to have trajectory-driven rho; short-memory channels (4 with
  ~6-7d) LESS likely
- HA07d stress_stdev_sleep (E[L]*=7.0 short-memory) is the cleanest test
  of within-window-real for the HA07d both-eras-SUPPORTED finding

DISCIPLINE GUARDS (per CONVENTIONS):

- sec 2.1 descriptive-before-inference: NO causal claims; NO falsification
  bar; NO HA verdict promotion (HA07d, HA-C3 v2, HA-C3p, crash_v2-definition,
  HA-P6 v3, recovery_arc v2 are all LOCKED and NOT extended here)
- sec 3.7 trajectory-detrend discipline: if a pair's rho collapses under
  detrend, surface as "rho_raw=X collapses to rho_detrended~0; flag
  SPURIOUS_TRAJECTORY_DRIVEN" -- do NOT claim raw rho was wrong (detrend
  is a sensitivity arm, NOT a correction)
- sec 4.1 + sec 4.2: descriptive framing only; observations land as
  "rho_raw=X, rho_detrended=Y, |delta_rho|=Z, flag=SPURIOUS/WITHIN-WINDOW-REAL"
- sec 4.9 (descriptive README): closes canonical Q4.5.b scope
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
# HERE = .../analyses/descriptive/trajectory/detrended_correlation
# parents[0]=trajectory; [1]=descriptive; [2]=analyses
UTILS_DIR = HERE.parents[2] / "_utils"
sys.path.insert(0, str(UTILS_DIR))

from frame import filter_to_stratum_4, load_master  # noqa: E402


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


AS_OF_DATE = "2026-06-05"  # parity with Q3.9 Strand-A precedent + Q4.9

# 7 channels per user-locked operationalisation (handoff sec 2)
CHANNELS = [
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
    "stress_stdev_sleep",
    "stress_low_motion_min_count_S60_Mlow",
    "resting_hr",
    "gevoelscore",
]

# E[L]* memory regime per Q3.x analyses + Q4.9 cross-channel context
CHANNEL_MEMORY = {
    "stress_mean_sleep": ("mid", 12.6),
    "all_day_stress_avg": ("long", 29.8),
    "bb_lowest": ("long", 29.25),
    "stress_stdev_sleep": ("short", 7.0),
    "stress_low_motion_min_count_S60_Mlow": ("long", 21.1),
    "resting_hr": ("short", 7.0),
    "gevoelscore": ("mid", 15.1),
}

# Long-memory channels (>=21d E[L]*); short-memory (<=10d); mid otherwise
LONG_MEMORY_CHANNELS = {
    c for c, (_, el) in CHANNEL_MEMORY.items() if el >= 21
}
SHORT_MEMORY_CHANNELS = {
    c for c, (_, el) in CHANNEL_MEMORY.items() if el <= 10
}

# LOESS / rolling-median window per handoff sec 2.1 (90d)
ROLLING_MEDIAN_WINDOW = 90

# Spurious-flag threshold per handoff sec 2.4 + CONVENTIONS sec 3.7
SPURIOUS_FLAG_THRESHOLD = 0.10

# Recovery-phase axis boundaries per methodology/lc_recovery_phase_axis.md sec 2.1
# (6 phases: pre_illness_healthy / acute_infection / lc_pre_ergo / 4a /
# 4b / citalopram_modulated). Stratum 4 starts 2022-09-03 so phases 1 + 2
# are mostly excluded; included here for full-corpus runs.
PHASE_BOUNDARIES = [
    ("pre_illness_healthy", date(2021, 8, 16), date(2022, 3, 20)),
    ("acute_infection", date(2022, 3, 21), date(2022, 4, 3)),
    ("lc_pre_ergo", date(2022, 4, 4), date(2022, 9, 21)),
    ("pacing_pre_citalopram_learning", date(2022, 9, 22), date(2022, 11, 16)),
    ("pacing_habit_established", date(2022, 11, 17), date(2024, 4, 8)),
    ("citalopram_modulated", date(2024, 4, 9), date(2026, 6, 5)),
]


# ---------------------------------------------------------------------------
# Phase helper
# ---------------------------------------------------------------------------


def recovery_phase(d) -> str:
    if not isinstance(d, date):
        d = pd.Timestamp(d).date()
    for name, start, end in PHASE_BOUNDARIES:
        if start <= d <= end:
            return name
    return "out_of_scope"


# ---------------------------------------------------------------------------
# Spearman helper (no scipy dependency)
# ---------------------------------------------------------------------------


def _rank_avg(arr):
    """Average-rank (1-based) handling ties."""
    arr = np.asarray(arr, dtype=float)
    order = np.argsort(arr, kind="mergesort")
    ranks = np.empty_like(arr, dtype=float)
    i = 0
    n = len(arr)
    while i < n:
        j = i
        while j + 1 < n and arr[order[j + 1]] == arr[order[i]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    return ranks


def spearman_rho(x, y) -> float:
    """Simple Spearman rho; ties handled via average-rank.

    Returns NaN if fewer than 3 pairs available.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = ~np.isnan(x) & ~np.isnan(y)
    if mask.sum() < 3:
        return float("nan")
    xi = x[mask]
    yi = y[mask]
    rx = _rank_avg(xi)
    ry = _rank_avg(yi)
    rx_mean = rx.mean()
    ry_mean = ry.mean()
    num = ((rx - rx_mean) * (ry - ry_mean)).sum()
    den_x = np.sqrt(((rx - rx_mean) ** 2).sum())
    den_y = np.sqrt(((ry - ry_mean) ** 2).sum())
    if den_x == 0 or den_y == 0:
        return float("nan")
    return float(num / (den_x * den_y))


def n_pairs(x, y) -> int:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    return int((~np.isnan(x) & ~np.isnan(y)).sum())


# ---------------------------------------------------------------------------
# Stage 1 -- data prep
# ---------------------------------------------------------------------------


def stage1_data_prep() -> dict:
    """Load per_day_master; restrict to Stratum 4 (gevoelscore-having days);
    identify recovery_phase per row; restrict to 7 channels.
    """
    master = load_master(as_of_date=AS_OF_DATE)
    df = filter_to_stratum_4(master, as_of_date=AS_OF_DATE).copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["recovery_phase"] = df["date"].dt.date.apply(recovery_phase)
    # Time index for OLS detrend (days from first row)
    t0 = df["date"].iloc[0]
    df["t_days"] = (df["date"] - t0).dt.days.astype(float)

    keep = ["date", "t_days", "recovery_phase"] + CHANNELS
    df = df[keep].copy()
    return {
        "df": df,
        "n_s4": int(len(df)),
        "as_of_date": AS_OF_DATE,
    }


# ---------------------------------------------------------------------------
# Stage 2 -- raw rho matrix (Spearman; 21 pairs)
# ---------------------------------------------------------------------------


def all_pairs():
    out = []
    for i in range(len(CHANNELS)):
        for j in range(i + 1, len(CHANNELS)):
            out.append((CHANNELS[i], CHANNELS[j]))
    return out


def stage2_raw_rho(df: pd.DataFrame) -> dict:
    """Compute raw Spearman rho for all 21 pairs.

    REPRODUCES Q3.9.e + Q4.9 method (c) numbers as verification (the
    5 PRIMARY targets at full Stratum 4 with the gevoelscore-vs-X pairs).
    """
    results = {}
    for a, b in all_pairs():
        x = df[a].to_numpy(dtype=float)
        y = df[b].to_numpy(dtype=float)
        results[(a, b)] = {
            "n": n_pairs(x, y),
            "rho": spearman_rho(x, y),
        }
    return results


# ---------------------------------------------------------------------------
# Stage 3 -- linear OLS detrend per channel; residuals; rho on residuals
# ---------------------------------------------------------------------------


def linear_ols_residual(values, t) -> np.ndarray:
    """Fit linear OLS values ~ t on non-NaN pairs; return residuals same
    length as values (NaN where values is NaN).
    """
    v = np.asarray(values, dtype=float)
    t = np.asarray(t, dtype=float)
    mask = ~np.isnan(v) & ~np.isnan(t)
    if mask.sum() < 3:
        return v.copy()
    slope, intercept = np.polyfit(t[mask], v[mask], 1)
    out = np.full(len(v), np.nan)
    out[mask] = v[mask] - (slope * t[mask] + intercept)
    return out


def stage3_linear_ols_detrend(df: pd.DataFrame) -> dict:
    """For each channel: fit linear OLS vs time; compute residuals.
    For each pair: Spearman rho on residuals.
    """
    residuals = {}
    for chan in CHANNELS:
        residuals[chan] = linear_ols_residual(
            df[chan].to_numpy(dtype=float),
            df["t_days"].to_numpy(dtype=float),
        )

    results = {}
    for a, b in all_pairs():
        results[(a, b)] = {
            "n": n_pairs(residuals[a], residuals[b]),
            "rho": spearman_rho(residuals[a], residuals[b]),
        }
    return {"pair_rhos": results, "residuals": residuals}


# ---------------------------------------------------------------------------
# Stage 4 -- LOESS / rolling-median detrend (90d); residuals; rho on residuals
# ---------------------------------------------------------------------------


def rolling_median_residual(values, window: int) -> np.ndarray:
    """Centred rolling median (window days); subtract from values. Edge
    handling: window shrinks at edges (min_periods=1 effectively, but only
    valid where enough data; we require >=window//2 to avoid edge bias).
    """
    v = pd.Series(np.asarray(values, dtype=float))
    half = window // 2
    rolling = v.rolling(
        window=window, center=True, min_periods=max(1, half)
    ).median()
    return (v - rolling).to_numpy()


def stage4_rolling_median_detrend(df: pd.DataFrame) -> dict:
    """For each channel: 90d centred rolling-median; subtract to get
    residuals. For each pair: Spearman rho on residuals.
    """
    residuals = {}
    for chan in CHANNELS:
        residuals[chan] = rolling_median_residual(
            df[chan].to_numpy(dtype=float),
            ROLLING_MEDIAN_WINDOW,
        )

    results = {}
    for a, b in all_pairs():
        results[(a, b)] = {
            "n": n_pairs(residuals[a], residuals[b]),
            "rho": spearman_rho(residuals[a], residuals[b]),
        }
    return {"pair_rhos": results, "residuals": residuals}


# ---------------------------------------------------------------------------
# Stage 5 -- per-recovery-phase detrend (subtract phase mean per row)
# ---------------------------------------------------------------------------


def per_phase_residual(values, phases) -> np.ndarray:
    """For each row, subtract the per-phase mean. Returns residuals same
    length as values.
    """
    v = np.asarray(values, dtype=float)
    phases = np.asarray(phases)
    out = np.full(len(v), np.nan)
    for ph in np.unique(phases):
        mask = phases == ph
        vals = v[mask]
        valid = ~np.isnan(vals)
        if valid.sum() < 2:
            continue
        ph_mean = float(np.nanmean(vals))
        out[mask] = vals - ph_mean
    return out


def stage5_per_phase_detrend(df: pd.DataFrame) -> dict:
    """For each channel: subtract per-recovery-phase mean to get residuals.
    For each pair: Spearman rho on residuals.
    """
    phases = df["recovery_phase"].to_numpy()
    residuals = {}
    for chan in CHANNELS:
        residuals[chan] = per_phase_residual(
            df[chan].to_numpy(dtype=float),
            phases,
        )

    results = {}
    for a, b in all_pairs():
        results[(a, b)] = {
            "n": n_pairs(residuals[a], residuals[b]),
            "rho": spearman_rho(residuals[a], residuals[b]),
        }
    return {"pair_rhos": results, "residuals": residuals}


# ---------------------------------------------------------------------------
# Stage 5b -- per-recovery-phase granularity: per-phase rho on raw +
# per-phase rho on linear-OLS-within-phase residuals
# ---------------------------------------------------------------------------


def stage5b_per_phase_granularity(df: pd.DataFrame) -> dict:
    """Per the user-locked granularity choice (both full + per-phase):
    for each phase (with n>=30 rows), compute the per-pair raw rho on the
    in-phase subset. Per-phase = the "per-phase detrend granularity" tier
    (within-phase drift cancellation).

    Output structure: per_phase[phase_name] = {pair: {n, rho}}
    """
    out = {}
    for ph_name, _, _ in PHASE_BOUNDARIES:
        sub = df[df["recovery_phase"] == ph_name]
        if len(sub) < 30:
            out[ph_name] = {"n": int(len(sub)), "skipped": True}
            continue
        pair_rhos = {}
        for a, b in all_pairs():
            x = sub[a].to_numpy(dtype=float)
            y = sub[b].to_numpy(dtype=float)
            pair_rhos[(a, b)] = {
                "n": n_pairs(x, y),
                "rho": spearman_rho(x, y),
            }
        out[ph_name] = {
            "n": int(len(sub)),
            "skipped": False,
            "pair_rhos": pair_rhos,
        }
    return out


# ---------------------------------------------------------------------------
# Stage 6 -- sensitivity comparison + spurious-flag table
# ---------------------------------------------------------------------------


def stage6_sensitivity(
    raw: dict,
    ols: dict,
    rolling: dict,
    phase: dict,
) -> dict:
    """Per pair: compute |delta_rho| vs raw for each of 3 methods.
    Flag spurious if any |delta_rho| >= SPURIOUS_FLAG_THRESHOLD.
    """
    rows = []
    flagged_pairs = []
    for a, b in all_pairs():
        rho_raw = raw[(a, b)]["rho"]
        n_raw = raw[(a, b)]["n"]
        rho_ols = ols["pair_rhos"][(a, b)]["rho"]
        rho_rolling = rolling["pair_rhos"][(a, b)]["rho"]
        rho_phase = phase["pair_rhos"][(a, b)]["rho"]

        deltas = {}
        for label, rho_d in [
            ("ols", rho_ols),
            ("rolling", rho_rolling),
            ("phase", rho_phase),
        ]:
            if np.isnan(rho_raw) or np.isnan(rho_d):
                deltas[label] = float("nan")
            else:
                deltas[label] = float(rho_d - rho_raw)

        abs_deltas = {
            k: abs(v) if not np.isnan(v) else float("nan")
            for k, v in deltas.items()
        }

        method_max = max(
            (k for k in abs_deltas if not np.isnan(abs_deltas[k])),
            key=lambda k: abs_deltas[k],
            default=None,
        )
        max_abs_delta = (
            float("nan") if method_max is None else float(abs_deltas[method_max])
        )

        # SPURIOUS_TRAJECTORY_DRIVEN if any |delta_rho| >= 0.1
        is_spurious = (
            False
            if np.isnan(max_abs_delta)
            else max_abs_delta >= SPURIOUS_FLAG_THRESHOLD
        )

        # Per-method individual flags
        per_method_spurious = {
            k: (
                False
                if np.isnan(v)
                else v >= SPURIOUS_FLAG_THRESHOLD
            )
            for k, v in abs_deltas.items()
        }

        row = {
            "pair": (a, b),
            "n": int(n_raw),
            "rho_raw": float(rho_raw) if not np.isnan(rho_raw) else float("nan"),
            "rho_ols": float(rho_ols) if not np.isnan(rho_ols) else float("nan"),
            "rho_rolling": float(rho_rolling) if not np.isnan(rho_rolling) else float("nan"),
            "rho_phase": float(rho_phase) if not np.isnan(rho_phase) else float("nan"),
            "delta_ols": deltas["ols"],
            "delta_rolling": deltas["rolling"],
            "delta_phase": deltas["phase"],
            "abs_delta_ols": abs_deltas["ols"],
            "abs_delta_rolling": abs_deltas["rolling"],
            "abs_delta_phase": abs_deltas["phase"],
            "max_abs_delta": max_abs_delta,
            "method_driving_max_delta": method_max,
            "flag_spurious": bool(is_spurious),
            "per_method_spurious_flag": per_method_spurious,
        }
        rows.append(row)
        if is_spurious:
            flagged_pairs.append((a, b))

    # Group-level pattern: long-memory vs short-memory ρ-collapse rate
    long_mem_pairs = [
        r for r in rows
        if r["pair"][0] in LONG_MEMORY_CHANNELS
        or r["pair"][1] in LONG_MEMORY_CHANNELS
    ]
    short_mem_pairs = [
        r for r in rows
        if r["pair"][0] in SHORT_MEMORY_CHANNELS
        and r["pair"][1] in SHORT_MEMORY_CHANNELS
    ]
    long_collapsed = [r for r in long_mem_pairs if r["flag_spurious"]]
    short_collapsed = [r for r in short_mem_pairs if r["flag_spurious"]]

    # Per-method spurious counts across 21 pairs
    per_method_spurious_counts = {
        m: sum(1 for r in rows if r["per_method_spurious_flag"][m])
        for m in ["ols", "rolling", "phase"]
    }

    return {
        "rows": rows,
        "n_pairs_total": len(rows),
        "n_pairs_spurious": len(flagged_pairs),
        "spurious_pairs": flagged_pairs,
        "long_memory_pairs_total": len(long_mem_pairs),
        "long_memory_pairs_spurious": len(long_collapsed),
        "short_memory_pairs_total": len(short_mem_pairs),
        "short_memory_pairs_spurious": len(short_collapsed),
        "per_method_spurious_counts": per_method_spurious_counts,
    }


# ---------------------------------------------------------------------------
# Stage 7 -- output artefacts (plots) + summary tables already computed
# ---------------------------------------------------------------------------


def stage7_make_plots(summary: dict, out_dir: Path) -> list:
    """Plots:
    1. Rho matrix side-by-side heatmap (raw vs 3 detrended methods)
    2. Spurious-flag summary bar chart per method
    3. Per-pair |delta_rho| scatter (raw rho on x; max |delta| on y;
       flagged pairs highlighted)
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    written = []

    # ----- Plot 1: rho matrix side-by-side (raw + 3 detrended) --------------
    rows = summary["stage6_sensitivity"]["rows"]
    n_pairs_v = len(rows)

    fig, ax = plt.subplots(figsize=(10, max(5, n_pairs_v * 0.32)))
    methods = ["rho_raw", "rho_ols", "rho_rolling", "rho_phase"]
    method_labels = [
        "raw",
        "linear OLS",
        "rolling-median 90d",
        "per-phase",
    ]
    matrix = np.full((n_pairs_v, len(methods)), np.nan)
    for i, r in enumerate(rows):
        for j, m in enumerate(methods):
            matrix[i, j] = r[m]
    vmax = float(np.nanmax(np.abs(matrix))) if not np.all(np.isnan(matrix)) else 0.5
    vmax = max(vmax, 0.1)
    im = ax.imshow(matrix, aspect="auto", cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    ax.set_xticks(range(len(methods)))
    ax.set_xticklabels(method_labels)
    ax.set_yticks(range(n_pairs_v))
    pair_labels = [
        "{} x {}".format(r["pair"][0], r["pair"][1])
        for r in rows
    ]
    ax.set_yticklabels(pair_labels, fontsize=7)
    ax.set_title(
        "Q4.5.b raw vs detrended Spearman rho (21 pairs, 4 methods)\n"
        "red = positive rho; blue = negative rho"
    )
    fig.colorbar(im, ax=ax, label="Spearman rho")
    fig.tight_layout()
    p1 = out_dir / "fig1_rho_matrix_side_by_side.png"
    fig.savefig(p1, dpi=120)
    plt.close(fig)
    written.append(str(p1))

    # ----- Plot 2: per-method spurious-flag count bar chart -----------------
    counts = summary["stage6_sensitivity"]["per_method_spurious_counts"]
    fig, ax = plt.subplots(figsize=(6, 4))
    methods_p = ["ols", "rolling", "phase"]
    method_labels_p = [
        "linear OLS",
        "rolling-median 90d",
        "per-phase",
    ]
    counts_v = [counts[m] for m in methods_p]
    bars = ax.bar(method_labels_p, counts_v, color=["#c66", "#6a6", "#69c"])
    ax.set_ylabel("n pairs flagged SPURIOUS (|delta rho| >= {})".format(
        SPURIOUS_FLAG_THRESHOLD
    ))
    ax.set_title(
        "Q4.5.b spurious-flag count per detrend method (n=21 pairs total)"
    )
    ax.set_ylim(0, max(max(counts_v, default=1) + 2, n_pairs_v))
    for bar, c in zip(bars, counts_v):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            str(c),
            ha="center",
            va="bottom",
            fontsize=10,
        )
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    p2 = out_dir / "fig2_per_method_spurious_count.png"
    fig.savefig(p2, dpi=120)
    plt.close(fig)
    written.append(str(p2))

    # ----- Plot 3: per-pair scatter: raw rho vs max |delta| -----------------
    fig, ax = plt.subplots(figsize=(8, 6))
    xs = [r["rho_raw"] for r in rows]
    ys = [r["max_abs_delta"] for r in rows]
    colors = [
        "#d33" if r["flag_spurious"] else "#999" for r in rows
    ]
    ax.scatter(xs, ys, c=colors, s=80, edgecolor="black", linewidth=0.6)
    ax.axhline(SPURIOUS_FLAG_THRESHOLD, color="black", linestyle="--", alpha=0.5)
    ax.text(
        ax.get_xlim()[1] * 0.99,
        SPURIOUS_FLAG_THRESHOLD + 0.005,
        "spurious-flag threshold",
        ha="right",
        va="bottom",
        fontsize=8,
        color="black",
    )
    # Annotate flagged pairs
    for r, x_v, y_v in zip(rows, xs, ys):
        if r["flag_spurious"] and not (
            np.isnan(x_v) or np.isnan(y_v)
        ):
            short_label = "{} x {}".format(
                r["pair"][0][:6], r["pair"][1][:6]
            )
            ax.annotate(
                short_label,
                xy=(x_v, y_v),
                fontsize=6,
                xytext=(3, 3),
                textcoords="offset points",
            )
    ax.set_xlabel("rho_raw (Spearman, full Stratum 4)")
    ax.set_ylabel("max |delta rho| across 3 detrend methods")
    ax.set_title(
        "Q4.5.b sensitivity scatter: raw rho vs max |delta| under detrend\n"
        "(red = SPURIOUS_TRAJECTORY_DRIVEN; grey = WITHIN-WINDOW-REAL)"
    )
    ax.grid(alpha=0.3)
    fig.tight_layout()
    p3 = out_dir / "fig3_sensitivity_scatter.png"
    fig.savefig(p3, dpi=120)
    plt.close(fig)
    written.append(str(p3))

    return written


# ---------------------------------------------------------------------------
# Stage 8 -- programmatic emit findings.md + README.md
# ---------------------------------------------------------------------------


def _fmt_rho(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "n/a"
    return "{:+.3f}".format(v)


def _fmt_delta(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "n/a"
    return "{:+.3f}".format(v)


def _fmt_abs(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "n/a"
    return "{:.3f}".format(v)


def stage8_emit_findings(summary: dict, path: Path) -> None:
    """Programmatic emit of findings.md from summary results."""
    s = summary
    lines = []
    A = lines.append

    sens = s["stage6_sensitivity"]
    rows = sens["rows"]
    n_pairs_v = sens["n_pairs_total"]

    A("# Findings -- Q4.5.b detrended_correlation (methodological sanity check)")
    A("")
    A(
        "**Strand**: B (multi-year trajectory; descriptive sanity check). "
        "Closes the canonical Q4.5.b scope per "
        "[`analyses/descriptive/README.md`](../../README.md) section 4.5.b "
        "(r2 closure D3.4) -- detrended-companion correlation matrix per "
        "[CONVENTIONS section 3.7](../../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) "
        "trajectory-detrend sensitivity discipline."
    )
    A("")
    A(
        "**Surface**: Stratum 4 (LC + gevoelscore + crash labels, "
        "2022-09-03 to " + AS_OF_DATE + "). n=" + str(s["n_s4"]) + " day-level rows."
    )
    A("")
    A(
        "**Programme spec**: [`descriptive/README.md`](../../README.md) "
        "section 4.5.b (LOCKED 2026-06-18 r3, commit `ccbd12e`) -- "
        "'detrended-companion correlation matrix; spurious-correlation flag "
        "for time-trended pairs'."
    )
    A("")
    A(
        "**User-LOCKED operationalisation** (per Strand B section 7c "
        "interview 2026-06-25; do NOT iterate):"
    )
    A("")
    A(
        "1. **Detrend method = ALL 3 methods + sensitivity**: linear OLS "
        "(CONVENTIONS section 3.7 default) + rolling-median 90d + "
        "per-recovery-phase residual."
    )
    A(
        "2. **Channel-pair scope = 7x7 matrix (21 unique pairs)**: "
        "stress_mean_sleep + all_day_stress_avg + bb_lowest + stress_stdev_sleep "
        "+ stress_low_motion_min_count_S60_Mlow + resting_hr + gevoelscore."
    )
    A(
        "3. **Detrend granularity = both full + per-phase**: full-corpus "
        "single detrend tells you about multi-year arc cancellation; "
        "per-recovery-phase detrend tells you about within-phase drift "
        "cancellation."
    )
    A(
        "4. **Spurious-correlation flag threshold = |delta rho| >= "
        + str(SPURIOUS_FLAG_THRESHOLD) + "** per CONVENTIONS section 3.7 + "
        "HA precedent. Pairs where detrend changes rho by >= " + str(SPURIOUS_FLAG_THRESHOLD)
        + " in any method get SPURIOUS_TRAJECTORY_DRIVEN flag; otherwise "
        "WITHIN-WINDOW-REAL."
    )
    A("")
    A(
        "**Discipline**: Layer 1 descriptive sanity-check (no causal claims; "
        "no falsification bar; no HA verdict promotion; **not a claim that "
        "raw rho was wrong** -- detrend is a sensitivity arm per CONVENTIONS "
        "section 3.7) per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) "
        "+ section 3.7 + section 4.1 + section 4.2. HA07d both-eras-SUPPORTED + "
        "HA-C3 v2 + HA-C3p + crash_v2-definition + HA-P6 v3 + recovery_arc v2 "
        "LOCKED references are descriptive corroboration only; NONE are "
        "extended here."
    )
    A("")
    A("---")
    A("")
    A("## Headline")
    A("")
    A(
        "**Spurious-flag verdict**: " + str(sens["n_pairs_spurious"])
        + " of " + str(n_pairs_v) + " pairs flagged SPURIOUS_TRAJECTORY_DRIVEN "
        "in >=1 method; the remaining " + str(n_pairs_v - sens["n_pairs_spurious"])
        + " survive all 3 detrend methods within the |delta rho| < "
        + str(SPURIOUS_FLAG_THRESHOLD) + " threshold (WITHIN-WINDOW-REAL)."
    )
    A("")
    A(
        "**Per-method spurious-flag counts** (of " + str(n_pairs_v) + " pairs):"
    )
    A("")
    A("| method | n pairs flagged SPURIOUS | rate |")
    A("|---|---:|---:|")
    counts = sens["per_method_spurious_counts"]
    for m_key, m_label in [
        ("ols", "linear OLS"),
        ("rolling", "rolling-median 90d"),
        ("phase", "per-recovery-phase"),
    ]:
        cnt = counts[m_key]
        A(
            "| " + m_label
            + " | " + str(cnt)
            + " | " + "{:.1%}".format(cnt / n_pairs_v)
            + " |"
        )
    A("")
    A(
        "**Long-memory vs short-memory rho-collapse pattern** (per "
        "Tier 1+2 E[L]* spread per handoff section 3.3): long-memory "
        "channels (E[L]* >= 21d: all_day_stress_avg / bb_lowest / "
        "stress_low_motion_min_count_S60_Mlow) are more likely to carry "
        "trajectory-driven rho; short-memory channels (E[L]* <= 10d: "
        "stress_stdev_sleep / resting_hr) less so."
    )
    A("")
    A("| pair group | n pairs total | n flagged SPURIOUS | rate |")
    A("|---|---:|---:|---:|")
    A(
        "| pairs involving any long-memory channel | "
        + str(sens["long_memory_pairs_total"])
        + " | " + str(sens["long_memory_pairs_spurious"])
        + " | " + "{:.1%}".format(
            sens["long_memory_pairs_spurious"]
            / max(1, sens["long_memory_pairs_total"])
        )
        + " |"
    )
    A(
        "| short-memory x short-memory pairs only | "
        + str(sens["short_memory_pairs_total"])
        + " | " + str(sens["short_memory_pairs_spurious"])
        + " | " + (
            "{:.1%}".format(
                sens["short_memory_pairs_spurious"]
                / max(1, sens["short_memory_pairs_total"])
            ) if sens["short_memory_pairs_total"] > 0 else "n/a"
        )
        + " |"
    )
    A("")
    A(
        "**HA07d-relevant pair** (stress_stdev_sleep x gevoelscore; E[L]*=7.0 "
        "short-memory channel; clean test of within-window-real per handoff "
        "section 3.3):"
    )
    A("")
    ha07d_row = next(
        (
            r for r in rows
            if set(r["pair"]) == {"stress_stdev_sleep", "gevoelscore"}
        ),
        None,
    )
    if ha07d_row is not None:
        A(
            "- rho_raw = " + _fmt_rho(ha07d_row["rho_raw"])
            + " (n=" + str(ha07d_row["n"]) + ")"
        )
        A(
            "- rho_ols = " + _fmt_rho(ha07d_row["rho_ols"])
            + " (delta = " + _fmt_delta(ha07d_row["delta_ols"]) + ")"
        )
        A(
            "- rho_rolling90d = " + _fmt_rho(ha07d_row["rho_rolling"])
            + " (delta = " + _fmt_delta(ha07d_row["delta_rolling"]) + ")"
        )
        A(
            "- rho_phase = " + _fmt_rho(ha07d_row["rho_phase"])
            + " (delta = " + _fmt_delta(ha07d_row["delta_phase"]) + ")"
        )
        A(
            "- **flag**: " + (
                "SPURIOUS_TRAJECTORY_DRIVEN (method driving max delta = "
                + str(ha07d_row["method_driving_max_delta"]) + ")"
                if ha07d_row["flag_spurious"]
                else "WITHIN-WINDOW-REAL (survives all 3 detrend methods)"
            )
        )
    A("")
    A(
        "**Methodology sensitivity**: per-method spurious-flag counts above "
        "are the descriptive measure of method-sensitivity. If the 3 methods "
        "produce systematically different counts, detrend method choice is "
        "load-bearing for the substantive read; if counts align, the rho "
        "values are robust to method choice."
    )
    A("")
    A("---")
    A("")

    # ---- Section 2: raw rho verification ----
    A("## 2. Stage 2 -- raw rho matrix (21 pairs) -- VERIFICATION CHECK")
    A("")
    A(
        "**Method**: Spearman rho on the full Stratum 4 single-pool (matching "
        "Q3.9.e + Q4.9 method (c) full-pool resolution). 21 unique pairs from "
        "the 7-channel set (7-choose-2)."
    )
    A("")
    A(
        "**REPRODUCES Q3.9.e rho ranking** per handoff section 3.3 (verification "
        "check): the 5 PRIMARY pairs involving `gevoelscore` (per Q3.9.e "
        "Strand-A first-pass) appear in this matrix and should match Q3.9.e "
        "reported values (stress_mean_sleep -0.194 / stress_stdev_sleep -0.121 "
        "/ all_day_stress_avg -0.056 / resting_hr +0.020 / bb_lowest +0.010)."
    )
    A("")
    A("**Q3.9.e + Q4.9 method (c) verification table** (gevoelscore-vs-X pairs):")
    A("")
    A("| pair | n | rho_raw (this analysis) | Q3.9.e reported | match? |")
    A("|---|---:|---:|---:|---|")
    q39e_targets = {
        "stress_mean_sleep": -0.194,
        "stress_stdev_sleep": -0.121,
        "all_day_stress_avg": -0.056,
        "resting_hr": 0.020,
        "bb_lowest": 0.010,
    }
    for chan, q39e_val in q39e_targets.items():
        row = next(
            (
                r for r in rows
                if set(r["pair"]) == {chan, "gevoelscore"}
            ),
            None,
        )
        if row is None:
            continue
        rho_v = row["rho_raw"]
        match = (
            "YES (within 0.005)"
            if (not np.isnan(rho_v)) and abs(rho_v - q39e_val) < 0.005
            else "DRIFT (|delta| = {:.3f})".format(
                abs(rho_v - q39e_val) if not np.isnan(rho_v) else float("nan")
            )
        )
        A(
            "| " + chan + " x gevoelscore"
            + " | " + str(row["n"])
            + " | " + _fmt_rho(rho_v)
            + " | " + "{:+.3f}".format(q39e_val)
            + " | " + match
            + " |"
        )
    A("")

    A("**Full 21-pair raw rho matrix**:")
    A("")
    A("| pair | n | rho_raw |")
    A("|---|---:|---:|")
    for r in rows:
        A(
            "| " + r["pair"][0] + " x " + r["pair"][1]
            + " | " + str(r["n"])
            + " | " + _fmt_rho(r["rho_raw"])
            + " |"
        )
    A("")
    A("---")
    A("")

    # ---- Sections 3-5: detrend method results ----
    A("## 3. Stage 3 -- linear OLS detrend (CONVENTIONS section 3.7 default)")
    A("")
    A(
        "**Method**: per channel, fit linear OLS of value ~ days-from-start; "
        "compute residual = value - (slope x t + intercept). Then for each "
        "pair, Spearman rho on residuals. This is the canonical detrend per "
        "[CONVENTIONS section 3.7](../../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) "
        "(adapted from the pre-vs-post-window precedent to the cross-channel "
        "correlation use-case)."
    )
    A("")
    A(
        "**Honest framing per CONVENTIONS section 3.7**: if a pair's rho "
        "collapses under linear OLS detrend (|delta rho| >= "
        + str(SPURIOUS_FLAG_THRESHOLD) + "), the raw rho is "
        "characterised SPURIOUS_TRAJECTORY_DRIVEN -- the multi-year arc was "
        "carrying the rank correlation. **Not a claim the raw rho was wrong**; "
        "the raw rho honestly describes the rank correlation on raw data + "
        "the detrended rho honestly describes the rank correlation on "
        "trajectory-removed residuals. Both are valid descriptions of "
        "different layers of structure."
    )
    A("")
    A("| pair | n | rho_raw | rho_ols | delta_ols | |delta| | flag |")
    A("|---|---:|---:|---:|---:|---:|---|")
    for r in rows:
        A(
            "| " + r["pair"][0] + " x " + r["pair"][1]
            + " | " + str(r["n"])
            + " | " + _fmt_rho(r["rho_raw"])
            + " | " + _fmt_rho(r["rho_ols"])
            + " | " + _fmt_delta(r["delta_ols"])
            + " | " + _fmt_abs(r["abs_delta_ols"])
            + " | " + (
                "SPURIOUS"
                if r["per_method_spurious_flag"]["ols"]
                else "WITHIN-WINDOW-REAL"
            )
            + " |"
        )
    A("")
    A("---")
    A("")

    A("## 4. Stage 4 -- rolling-median 90d detrend")
    A("")
    A(
        "**Method**: per channel, centred 90d rolling median; subtract from "
        "raw values to get residuals. Then for each pair, Spearman rho on "
        "residuals. The 90d window is wider than every channel's E[L]* "
        "(longest = all_day_stress_avg ~30d) so it preserves seasonal-to-"
        "trajectory structure while damping noise; complements linear OLS "
        "(which assumes constant slope across the corpus)."
    )
    A("")
    A("| pair | n | rho_raw | rho_rolling90d | delta_rolling | |delta| | flag |")
    A("|---|---:|---:|---:|---:|---:|---|")
    for r in rows:
        A(
            "| " + r["pair"][0] + " x " + r["pair"][1]
            + " | " + str(r["n"])
            + " | " + _fmt_rho(r["rho_raw"])
            + " | " + _fmt_rho(r["rho_rolling"])
            + " | " + _fmt_delta(r["delta_rolling"])
            + " | " + _fmt_abs(r["abs_delta_rolling"])
            + " | " + (
                "SPURIOUS"
                if r["per_method_spurious_flag"]["rolling"]
                else "WITHIN-WINDOW-REAL"
            )
            + " |"
        )
    A("")
    A("---")
    A("")

    A("## 5. Stage 5 -- per-recovery-phase residual detrend")
    A("")
    A(
        "**Method**: per channel, subtract the per-recovery-phase mean from "
        "each row. Phases from "
        "[`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) "
        "section 2 (6 phases; Stratum 4 contains last 19 days of "
        "`lc_pre_ergo` + 4a + 4b + 5). Then for each pair, Spearman rho on "
        "residuals."
    )
    A("")
    A(
        "**LOAD-BEARING Q4.3 rp5 cross-reference (descriptive only)** per "
        "handoff section 3.3: Q4.3 found rp5 (citalopram start, "
        "2024-04-09) is the strongest boundary on 5 of 6 channels -- the "
        "multi-year arc carries substantial citalopram-step component. "
        "Therefore linear OLS detrend on the full corpus may CANCEL "
        "multi-year-arc structure (including the citalopram step), but "
        "per-recovery-phase detrend PRESERVES within-phase content (the "
        "citalopram step is absorbed into the per-phase mean shift). Pairs "
        "that flag SPURIOUS under linear OLS but survive under per-phase "
        "detrend are particularly interesting: the multi-year arc was "
        "carrying the rho but the within-phase drift wasn't. The Q4.3 rp5 "
        "substantive finding is LOCKED and NOT extended here."
    )
    A("")
    A("| pair | n | rho_raw | rho_phase | delta_phase | |delta| | flag |")
    A("|---|---:|---:|---:|---:|---:|---|")
    for r in rows:
        A(
            "| " + r["pair"][0] + " x " + r["pair"][1]
            + " | " + str(r["n"])
            + " | " + _fmt_rho(r["rho_raw"])
            + " | " + _fmt_rho(r["rho_phase"])
            + " | " + _fmt_delta(r["delta_phase"])
            + " | " + _fmt_abs(r["abs_delta_phase"])
            + " | " + (
                "SPURIOUS"
                if r["per_method_spurious_flag"]["phase"]
                else "WITHIN-WINDOW-REAL"
            )
            + " |"
        )
    A("")
    A("---")
    A("")

    # ---- Section 6: sensitivity comparison + spurious-flag table ----
    A("## 6. Stage 6 -- sensitivity comparison + spurious-flag table")
    A("")
    A(
        "**Method**: per pair, compute |delta rho| vs raw for each of 3 "
        "detrend methods; flag SPURIOUS_TRAJECTORY_DRIVEN if any |delta rho| "
        ">= " + str(SPURIOUS_FLAG_THRESHOLD) + " (CONVENTIONS section 3.7 "
        "default + HA precedent)."
    )
    A("")
    A(
        "**Spurious-flag count**: " + str(sens["n_pairs_spurious"]) + " of "
        + str(n_pairs_v) + " pairs flagged SPURIOUS in >=1 detrend method."
    )
    A("")
    A("**Flagged pair table** (sorted by max |delta|):")
    A("")
    A(
        "| pair | n | rho_raw | rho_ols | rho_rolling | rho_phase | "
        "max |delta| | method driving max delta |"
    )
    A(
        "|---|---:|---:|---:|---:|---:|---:|---|"
    )
    flagged_sorted = sorted(
        [r for r in rows if r["flag_spurious"]],
        key=lambda r: -r["max_abs_delta"]
        if not np.isnan(r["max_abs_delta"])
        else 0,
    )
    if not flagged_sorted:
        A("| (none flagged) | | | | | | | |")
    else:
        for r in flagged_sorted:
            A(
                "| " + r["pair"][0] + " x " + r["pair"][1]
                + " | " + str(r["n"])
                + " | " + _fmt_rho(r["rho_raw"])
                + " | " + _fmt_rho(r["rho_ols"])
                + " | " + _fmt_rho(r["rho_rolling"])
                + " | " + _fmt_rho(r["rho_phase"])
                + " | " + _fmt_abs(r["max_abs_delta"])
                + " | " + str(r["method_driving_max_delta"])
                + " |"
            )
    A("")

    A("**Surviving pair table (WITHIN-WINDOW-REAL across all 3 methods)**:")
    A("")
    A("| pair | n | rho_raw | rho_ols | rho_rolling | rho_phase | max |delta| |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    surviving = [r for r in rows if not r["flag_spurious"]]
    if not surviving:
        A("| (none surviving) | | | | | | |")
    else:
        for r in surviving:
            A(
                "| " + r["pair"][0] + " x " + r["pair"][1]
                + " | " + str(r["n"])
                + " | " + _fmt_rho(r["rho_raw"])
                + " | " + _fmt_rho(r["rho_ols"])
                + " | " + _fmt_rho(r["rho_rolling"])
                + " | " + _fmt_rho(r["rho_phase"])
                + " | " + _fmt_abs(r["max_abs_delta"])
                + " |"
            )
    A("")

    A("**Particularly-interesting pairs** (SPURIOUS under linear OLS but "
      "survive under per-phase detrend; multi-year arc was carrying rho "
      "but within-phase drift wasn't):")
    A("")
    interesting = [
        r for r in rows
        if r["per_method_spurious_flag"]["ols"]
        and not r["per_method_spurious_flag"]["phase"]
    ]
    if not interesting:
        A("- none in this corpus.")
    else:
        for r in interesting:
            A(
                "- **" + r["pair"][0] + " x " + r["pair"][1] + "**: "
                + "rho_raw = " + _fmt_rho(r["rho_raw"])
                + "; rho_ols = " + _fmt_rho(r["rho_ols"])
                + " (delta = " + _fmt_delta(r["delta_ols"]) + " collapsed)"
                + "; rho_phase = " + _fmt_rho(r["rho_phase"])
                + " (delta = " + _fmt_delta(r["delta_phase"]) + " preserved)"
            )
    A("")

    # ---- Section 7: per-phase granularity tables ----
    A("---")
    A("")
    A("## 7. Stage 5b -- per-recovery-phase granularity tables (within-phase rho)")
    A("")
    A(
        "**Method**: per recovery phase with n>=30 rows, compute the per-pair "
        "Spearman rho on the in-phase subset. This is the **per-phase "
        "granularity** tier of the user-locked operationalisation choice 3 "
        "(both full + per-phase); complements Stage 5's per-phase mean-residual "
        "detrend by showing the within-phase rho directly."
    )
    A("")
    phase_gran = s["stage5b_per_phase_granularity"]
    A(
        "**Per-phase n** (rows with `recovery_phase` matching; Stratum 4 "
        "right edge " + AS_OF_DATE + "):"
    )
    A("")
    A("| phase | n | included in per-phase granularity? |")
    A("|---|---:|---|")
    for ph_name, _, _ in PHASE_BOUNDARIES:
        ph = phase_gran.get(ph_name, {})
        n_ph = ph.get("n", 0)
        included = (
            "YES" if not ph.get("skipped", True) and n_ph >= 30 else "no (n<30)"
        )
        A(
            "| " + ph_name
            + " | " + str(n_ph)
            + " | " + included
            + " |"
        )
    A("")

    # Per-phase per-pair tables -- only emit phases with n>=30
    for ph_name, _, _ in PHASE_BOUNDARIES:
        ph = phase_gran.get(ph_name, {})
        if ph.get("skipped", True):
            continue
        if ph.get("n", 0) < 30:
            continue
        A("### Phase: `" + ph_name + "` (n=" + str(ph["n"]) + ")")
        A("")
        A("| pair | n | rho_within_phase |")
        A("|---|---:|---:|")
        for (a, b), info in ph["pair_rhos"].items():
            A(
                "| " + a + " x " + b
                + " | " + str(info["n"])
                + " | " + _fmt_rho(info["rho"])
                + " |"
            )
        A("")

    # ---- Section 8: methodology sensitivity report ----
    A("---")
    A("")
    A("## 8. Methodology sensitivity report")
    A("")
    A(
        "**Question**: does detrend method choice systematically alter "
        "conclusions? Compare per-method spurious counts and per-pair |delta| "
        "patterns."
    )
    A("")
    A(
        "**Per-method spurious counts** (recap from headline): "
        + ", ".join(
            "{} = {}".format(m, counts[m_key])
            for m, m_key in [
                ("linear OLS", "ols"),
                ("rolling-median 90d", "rolling"),
                ("per-phase", "phase"),
            ]
        ) + "."
    )
    A("")
    # Compute aggregate methodology-sensitivity metrics
    abs_deltas_ols = [
        r["abs_delta_ols"] for r in rows if not np.isnan(r["abs_delta_ols"])
    ]
    abs_deltas_rolling = [
        r["abs_delta_rolling"]
        for r in rows
        if not np.isnan(r["abs_delta_rolling"])
    ]
    abs_deltas_phase = [
        r["abs_delta_phase"]
        for r in rows
        if not np.isnan(r["abs_delta_phase"])
    ]
    A("**Per-method aggregate |delta| statistics** (across 21 pairs):")
    A("")
    A("| method | mean |delta| | median |delta| | max |delta| | n with |delta|>=0.1 |")
    A("|---|---:|---:|---:|---:|")
    for label, vals, m_key in [
        ("linear OLS", abs_deltas_ols, "ols"),
        ("rolling-median 90d", abs_deltas_rolling, "rolling"),
        ("per-recovery-phase", abs_deltas_phase, "phase"),
    ]:
        if vals:
            A(
                "| " + label
                + " | " + "{:.3f}".format(float(np.mean(vals)))
                + " | " + "{:.3f}".format(float(np.median(vals)))
                + " | " + "{:.3f}".format(float(np.max(vals)))
                + " | " + str(counts[m_key])
                + " |"
            )
        else:
            A("| " + label + " | n/a | n/a | n/a | " + str(counts[m_key]) + " |")
    A("")

    A(
        "**Method-sensitivity narrative** (descriptive only per CONVENTIONS "
        "section 4.1): if the three method counts agree closely, the "
        "spurious/within-window-real verdict is robust to method choice. "
        "If the per-phase method flags substantially fewer pairs than linear "
        "OLS, the within-phase content survives even when the multi-year arc "
        "is removed (cf. Q4.3 rp5 citalopram-step finding -- per-phase detrend "
        "leaves the within-phase drift intact). If rolling-median 90d falls "
        "between OLS and per-phase, the slow trajectory + per-phase shift "
        "BOTH carry meaningful structure; method choice has gradient sensitivity."
    )
    A("")
    A(
        "**Long-memory vs short-memory pattern**: long-memory channels "
        "(E[L]* >= 21d) are structurally more prone to trajectory-driven "
        "rho because their slow drift dominates the variance budget; "
        "short-memory channels (E[L]* <= 10d) have weaker trajectory weight. "
        "The pair-group rates above descriptively surface this expectation."
    )
    A("")
    A("---")
    A("")

    # ---- Cross-references ----
    A("## Cross-references")
    A("")
    A("### LOAD-BEARING cross-references (descriptive corroboration only; NOT verdict extension)")
    A("")
    A(
        "- **Q3.9.e Strand-A first-pass** at "
        "[`descriptive/operationalisation_support/gevoelscore/findings.md`](../../operationalisation_support/gevoelscore/findings.md) "
        "section 3.9.e: linear-rank Spearman rho ranking on the full Stratum-4 "
        "pool. Stage 2 above REPRODUCES the 5 PRIMARY gevoelscore-vs-X pairs "
        "as a verification check."
    )
    A(
        "- **Q4.9 method (c) rolling-Spearman precedent** at "
        "[`descriptive/trajectory/subjective_objective_coupling/findings.md`](../subjective_objective_coupling/findings.md) "
        "section 4: rolling-window rho approach for the time-varying-structure "
        "complement; Q4.9 stays on raw rho across rolling windows -- this "
        "Q4.5.b complements with full-pool detrended rho across 3 methods."
    )
    A(
        "- **Q4.3 era_boundaries finding** at "
        "[`descriptive/trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) "
        "section 2-3: rp5 citalopram-start is the strongest boundary (5 of 6 "
        "channels). The multi-year arc carries substantial citalopram-step "
        "component; this contextualises why linear OLS detrend (which cancels "
        "the arc) can collapse pairs that per-phase detrend (which absorbs "
        "the step into the per-phase mean) preserves."
    )
    A(
        "- **Q4.6 coverage_overview finding** at "
        "[`descriptive/trajectory/coverage_overview/findings.md`](../coverage_overview/findings.md): "
        "bb_overnight_gain only available from 2024-09-18 onward (excluded "
        "from this 7-channel scope per user-locked operationalisation, which "
        "uses bb_lowest in its place). bb_lowest itself has full coverage in "
        "Stratum 4."
    )
    A(
        "- **HA07d both-eras-SUPPORTED finding** at "
        "[`analyses/hypotheses/HA07d-sleep-stress-variability/result.md`](../../../hypotheses/HA07d-sleep-stress-variability/result.md) "
        "(LOCKED): stress_stdev_sleep is the channel; E[L]*=7.0 short-memory "
        "makes the gevoelscore x stress_stdev_sleep pair the cleanest test "
        "of within-window-real (low trajectory loading by E[L]* metric). The "
        "HA07d substantive verdict is LOCKED and NOT extended here."
    )
    A(
        "- **CONVENTIONS section 3.7** trajectory-detrend sensitivity discipline "
        "[`CONVENTIONS.md`](../../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons): "
        "binding precedent for the |delta rho| >= " + str(SPURIOUS_FLAG_THRESHOLD)
        + " threshold + the linear-on-pre-window-form-is-conservative framing "
        "+ the empirical-validation paragraph (Session C "
        "intervention_effects MD found 2 of 7 raw-test findings were "
        "trajectory artifacts under detrend; the pattern is not hypothetical)."
    )
    A("")
    A("### Methodology MDs cited (binding for this analysis's discipline)")
    A("")
    A(
        "- [CONVENTIONS section 3.7](../../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) "
        "trajectory-detrend sensitivity for raw comparisons."
    )
    A(
        "- [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) "
        "(6-phase axis for per-recovery-phase detrend in Stage 5)."
    )
    A(
        "- [`methodology/permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) "
        "(E[L]=7 default + factor-of-2 deviation rule; per-channel E[L]* "
        "informs the long-memory vs short-memory rho-collapse rate framing)."
    )
    A(
        "- [`methodology/lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md) "
        "(Stratum 4 boundary; surface for primary analysis)."
    )
    A(
        "- [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) "
        "+ section 4.1 + section 4.2 (descriptive-only framing discipline)."
    )
    A("")
    A("### Upstream pipeline")
    A("")
    A(
        "- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` "
        "(7 channel columns + recovery_phase)."
    )
    A("")
    A("---")
    A("")
    A("## Limitations")
    A("")
    A(
        "For a producer-mode Layer-1 descriptive Strand B sanity-check analysis "
        "(no falsification bar; no causal claim per "
        "[CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) "
        "+ section 3.7 sensitivity-arm framing), the binding constraints are:"
    )
    A("")
    A(
        "1. **Detrend is a sensitivity arm, NOT a correction** per CONVENTIONS "
        "section 3.7. The raw rho honestly describes the rank correlation "
        "on raw data; the detrended rho honestly describes the rank "
        "correlation on trajectory-removed residuals. **Not a claim the raw "
        "rho was wrong**. Pairs flagged SPURIOUS surface as 'rho_raw "
        "collapses to rho_detrended ~0 under method X' -- a structural "
        "observation, not a correction."
    )
    A(
        "2. **No HA verdict promotion**: HA07d both-eras-SUPPORTED + HA-C3 v2 "
        "+ HA-C3p + HA-P6 v3 + recovery_arc v2 + crash_v2-definition LOCKED "
        "verdicts are referenced as descriptive context only; NONE are "
        "extended or re-interpreted per CONVENTIONS section 4.2 + handoff "
        "section 4 hard constraint."
    )
    A(
        "3. **No crash_v2-definition modification** + no methodology MD "
        "modification + no per_day_master.csv modification per handoff "
        "section 4 hard constraint."
    )
    A(
        "4. **No iteration on the 4 user-locked operationalisation choices** "
        "per Strand B section 7c discipline."
    )
    A(
        "5. **Linear OLS assumes constant slope across Stratum 4** -- if the "
        "true trajectory is non-linear (e.g. logistic recovery), linear OLS "
        "may under-detrend (residuals still carry curvature) or over-detrend "
        "(residuals contain spurious sub-trajectory). The rolling-median 90d "
        "and per-phase methods complement by allowing non-linear / piecewise "
        "trajectory shapes."
    )
    A(
        "6. **Rolling-median 90d edge effects**: centred 90d rolling median "
        "shrinks at the corpus edges (first and last ~45 days). Residuals "
        "near edges may be unstable; per CONVENTIONS section 3.6 named-count "
        "discipline, the |delta| values for rolling-median include the edge "
        "regions if data is present."
    )
    A(
        "7. **Per-phase detrend reduces variance more aggressively when phase "
        "n is small** (e.g. pacing_pre_citalopram_learning n=56 in Stratum 4). "
        "Per-pair rho on tiny in-phase subsets is high-variance; the per-phase "
        "granularity tables in section 7 skip phases with n<30 for "
        "robustness."
    )
    A(
        "8. **Recovery-phase axis is the 6-phase axis from "
        "`lc_recovery_phase_axis.md`** (LOCKED 2026-06-19 d47e0d3). Stratum 4 "
        "spans last 19 days of `lc_pre_ergo` + 4a + 4b + 5; phases 1 + 2 "
        "(pre_illness_healthy, acute_infection) have zero rows in Stratum 4 "
        "by construction (gevoelscore logging started 2022-09-03)."
    )
    A(
        "9. **Spurious-flag threshold = " + str(SPURIOUS_FLAG_THRESHOLD)
        + " inherits CONVENTIONS section 3.7 + HA precedent**. Alternative "
        "thresholds (0.05 stricter; 0.15 looser) would yield different "
        "flagged-pair counts; the " + str(SPURIOUS_FLAG_THRESHOLD)
        + " value is the locked precedent and is not re-negotiated here."
    )
    A(
        "10. **gevoelscore is bounded 1-6 integer** per Q3.9.a + Q4.9. "
        "Spearman rho handles this via average-rank ties; linear OLS detrend "
        "subtracts a continuous trend from a discrete series (residuals are "
        "no longer integer). The Spearman rho on those residuals is "
        "mathematically well-defined; the interpretation as 'within-window "
        "rho structure on a 1-6 felt-state channel after multi-year arc "
        "removal' is the appropriate framing."
    )
    A("")
    A("---")
    A("")
    A(
        "*Generated programmatically by [`run.py`](run.py) from the resolved "
        "`summary.json` (gitignored per `docs/research/**/*.json`). To "
        "refresh: `python run.py`.*"
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def stage8_emit_readme(summary: dict, path: Path) -> None:
    """Programmatic emit of README.md from summary."""
    s = summary
    sens = s["stage6_sensitivity"]

    lines = []
    A = lines.append

    A("# `detrended_correlation/` -- Q4.5.b (methodological sanity check)")
    A("")
    A(
        "**Strand**: B (multi-year trajectory; descriptive sanity check). "
        "First-time-in-any-artefact closure of the canonical Q4.5.b scope "
        "per [`analyses/descriptive/README.md`](../../README.md) section 4.5.b."
    )
    A("")
    A("## Research question")
    A("")
    A(
        "For each pair where both channels show a multi-year trajectory, "
        "how much of the raw Spearman rho is within-window co-variation vs "
        "shared trajectory? Do the rho values from Q3.9.e + Q4.9 method (c) "
        "survive trajectory detrend per CONVENTIONS section 3.7? Per the "
        "locked descriptive programme spec at "
        "[`docs/research/analyses/descriptive/README.md`](../../README.md) "
        "section 4.5.b (LOCKED 2026-06-18 r3, commit `ccbd12e`)."
    )
    A("")
    A("## Method (user-LOCKED operationalisation; do NOT iterate per Strand B section 7c discipline)")
    A("")
    A(
        "- **Surface**: Stratum 4 primary (LC + gevoelscore + crash labels, "
        "2022-09-03 to " + AS_OF_DATE + "; n=" + str(s["n_s4"])
        + " day-level rows)."
    )
    A(
        "- **7 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest "
        "+ stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + "
        "resting_hr + gevoelscore (Q4.9 6-channel set + outcome). 21 unique "
        "pairs (7-choose-2)."
    )
    A(
        "- **3 detrend methods + sensitivity**: (1) linear OLS (CONVENTIONS "
        "section 3.7 default), (2) rolling-median 90d, (3) per-recovery-phase "
        "residual (subtract phase mean per row)."
    )
    A(
        "- **Both full-corpus + per-recovery-phase granularity** per "
        "user-locked choice 3: full-corpus tells you about multi-year arc "
        "cancellation; per-phase tells you about within-phase drift "
        "cancellation."
    )
    A(
        "- **Spurious-correlation flag threshold = |delta rho| >= "
        + str(SPURIOUS_FLAG_THRESHOLD) + "** per CONVENTIONS section 3.7 + HA "
        "precedent."
    )
    A(
        "- **Shared utilities**: [`_utils/frame.py`](../../../_utils/frame.py) "
        "(loaders; Stratum 4 filter). NO new statistical machinery; uses "
        "numpy + pandas (Spearman rho vendored inline; no scipy dep)."
    )
    A(
        "- **No causal claims; no falsification bar; not a claim that raw "
        "rho was wrong** per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) "
        "+ section 3.7 + section 4.1 + section 4.2."
    )
    A("")
    A("## Result")
    A("")
    A("Headline (see [`findings.md`](findings.md) for full per-pair + per-method tables + cross-references):")
    A("")
    A(
        "**Spurious-flag count**: " + str(sens["n_pairs_spurious"]) + " of "
        + str(sens["n_pairs_total"]) + " pairs flagged "
        "SPURIOUS_TRAJECTORY_DRIVEN in >=1 detrend method; remaining "
        + str(sens["n_pairs_total"] - sens["n_pairs_spurious"])
        + " pairs survive all 3 detrend methods (WITHIN-WINDOW-REAL)."
    )
    A("")
    counts = sens["per_method_spurious_counts"]
    A(
        "**Per-method spurious counts**: linear OLS = " + str(counts["ols"])
        + "; rolling-median 90d = " + str(counts["rolling"])
        + "; per-recovery-phase = " + str(counts["phase"])
        + " (of " + str(sens["n_pairs_total"]) + " pairs each)."
    )
    A("")
    A(
        "**Long-memory channels** (E[L]* >= 21d: all_day_stress_avg / "
        "bb_lowest / stress_low_motion_min_count_S60_Mlow) are more likely "
        "to carry trajectory-driven rho; **short-memory channels** "
        "(E[L]* <= 10d: stress_stdev_sleep / resting_hr) less so. "
        "Pair-group rates: " + str(sens["long_memory_pairs_spurious"])
        + " of " + str(sens["long_memory_pairs_total"])
        + " long-memory-touching pairs flagged SPURIOUS; "
        + str(sens["short_memory_pairs_spurious"]) + " of "
        + str(sens["short_memory_pairs_total"])
        + " short-memory-only pairs."
    )
    A("")
    A(
        "**Layer 1 descriptive sanity-check only**. NO causal claims. NO "
        "HA verdict promotion. **NOT a claim that raw rho was wrong** "
        "(detrend is a sensitivity arm per CONVENTIONS section 3.7). HA07d "
        "+ HA-C3 v2 + HA-C3p + HA-P6 v3 + recovery_arc v2 + crash_v2-definition "
        "LOCKED references are descriptive context only."
    )
    A("")
    A("## Files")
    A("")
    A("- [`README.md`](README.md) -- this file")
    A(
        "- [`run.py`](run.py) -- 8-stage analysis script; outputs "
        "`summary.json` + `findings.md` + `README.md` + `plots/*.png`"
    )
    A(
        "- [`findings.md`](findings.md) -- writeup covering Stages 2-6 + "
        "per-phase granularity tables + methodology sensitivity report + "
        "cross-references + limitations (programmatically emitted by run.py)"
    )
    A(
        "- [`summary.json`](summary.json) -- machine-readable per-stage "
        "results (gitignored per `docs/research/**/*.json`)"
    )
    A(
        "- [`plots/`](plots/) -- 3 PNGs: rho matrix side-by-side, per-method "
        "spurious-flag count, sensitivity scatter (gitignored per "
        "`docs/research/**/*.png`)"
    )
    A("")
    A("## Status")
    A("")
    A(
        "**Current as of " + AS_OF_DATE + " corpus + 2026-06-25 analysis**. "
        "Closes Q4.5.b (descriptive README sec 4.5.b r2 closure D3.4; "
        "previously had no home in any artefact). **Tier 3 Core 5 4th of 5 "
        "LANDED** (Q4.9 + Q4.6 + Q4.3 + this Q4.5.b; remaining Q4.4 cohort "
        "topology + Q4.2 intervention cross-channel)."
    )
    A("")
    A("Refresh when:")
    A(
        "1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg "
        "using a pair from this 7-channel set as primary is about to spin up."
    )
    A(
        "2. lc_recovery_phase_axis is amended (e.g. phase 6 post_afbouw "
        "added when corpus first acquires post-2026-06-05 data)."
    )
    A(
        "3. CONVENTIONS section 3.7 trajectory-detrend discipline is amended."
    )
    A("")
    A("## Cross-references")
    A("")
    A(
        "- **Programme spec** (parent): "
        "[`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, "
        "commit `ccbd12e`); section 4.5.b 'Detrended-companion correlation '"
        "'(spurious-correlation flag)' (r2 closure D3.4) -- this analysis closes it."
    )
    A(
        "- **Q3.9.e Strand-A first-pass**: "
        "[`descriptive/operationalisation_support/gevoelscore/findings.md`](../../operationalisation_support/gevoelscore/findings.md) "
        "section 3.9.e -- linear-rank Spearman rho on the full Stratum-4 "
        "pool; REPRODUCED in this Q4.5.b Stage 2 as verification check."
    )
    A(
        "- **Q4.9 method (c) rolling-Spearman precedent**: "
        "[`descriptive/trajectory/subjective_objective_coupling/findings.md`](../subjective_objective_coupling/findings.md) "
        "section 4 -- complementary view (rolling rho over time) vs Q4.5.b's "
        "full-pool-rho-on-detrended-residuals view."
    )
    A(
        "- **Q4.3 era_boundaries**: "
        "[`descriptive/trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) "
        "-- rp5 citalopram-start strongest-boundary finding contextualises "
        "why per-recovery-phase detrend can preserve content that linear OLS "
        "cancels."
    )
    A(
        "- **Q4.6 coverage_overview**: "
        "[`descriptive/trajectory/coverage_overview/findings.md`](../coverage_overview/findings.md) "
        "-- channel coverage; bb_lowest used in place of bb_overnight_gain "
        "for full Stratum-4 coverage."
    )
    A(
        "- **HA07d both-eras-SUPPORTED**: "
        "[`analyses/hypotheses/HA07d-sleep-stress-variability/result.md`](../../../hypotheses/HA07d-sleep-stress-variability/result.md) "
        "(LOCKED) -- stress_stdev_sleep channel; short-memory makes the "
        "gevoelscore x stress_stdev_sleep pair the cleanest within-window-real "
        "test."
    )
    A(
        "- **Methodology MDs**: "
        "[`CONVENTIONS section 3.7`](../../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) "
        "+ [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) "
        "+ [`permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) "
        "+ [`lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md)."
    )
    A(
        "- **Upstream pipeline**: `per_day_master.csv` <- "
        "`pipeline/03_consolidate/build_unified_dataset.py`."
    )
    A("")
    A("## Discipline guards (per CONVENTIONS)")
    A("")
    A(
        "- **section 2.1 descriptive-before-inference**: NO causal claims; NO "
        "falsification bar; NO HA verdict promotion. The LOCKED HA references "
        "(HA07d, HA-C3 v2, HA-C3p, HA-P6 v3, recovery_arc v2, crash_v2-definition) "
        "are descriptive context only; NONE are extended."
    )
    A(
        "- **section 3.7 trajectory-detrend discipline**: |delta rho| >= "
        + str(SPURIOUS_FLAG_THRESHOLD) + " threshold inherits the HA precedent; "
        "detrend is a sensitivity arm, NOT a correction; **not a claim that "
        "raw rho was wrong**."
    )
    A(
        "- **section 3.6 named counts**: every n in findings.md tables "
        "names scheme (Stratum 4 day-level rows) + unit (pair-wise non-NaN) "
        "+ source (per_day_master.csv)."
    )
    A(
        "- **section 4.1 + section 4.2**: descriptive framing only; "
        "observations land as 'rho_raw = X, rho_detrended = Y, |delta| = Z, "
        "flag = SPURIOUS/WITHIN-WINDOW-REAL'; NO a-priori claims; NO "
        "mechanism interpretation."
    )
    A(
        "- **section 4.5.b (descriptive README)**: this analysis closes the "
        "canonical Q4.5.b scope for the first time in any artefact per the "
        "LOCKED programme spec."
    )
    A("")

    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------


def _convert_for_json(x):
    if isinstance(x, dict):
        return {
            str(k): _convert_for_json(v) for k, v in x.items()
        }
    if isinstance(x, (list, tuple)):
        return [_convert_for_json(v) for v in x]
    if isinstance(x, np.ndarray):
        return [_convert_for_json(v) for v in x.tolist()]
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        v = float(x)
        if np.isnan(v):
            return None
        return v
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, pd.Timestamp):
        return str(x.date())
    if isinstance(x, float) and np.isnan(x):
        return None
    return x


def _serialize_pair_rhos(d: dict) -> dict:
    """Convert tuple-keyed pair_rhos to string-keyed for JSON serialisation."""
    out = {}
    for k, v in d.items():
        if isinstance(k, tuple):
            key = " x ".join(k)
        else:
            key = str(k)
        out[key] = v
    return out


def _serialize_rows(rows: list) -> list:
    out = []
    for r in rows:
        copy = dict(r)
        copy["pair"] = " x ".join(r["pair"])
        out.append(copy)
    return out


def main() -> None:
    print("Q4.5.b detrended_correlation -- Strand B sanity check")
    print("=" * 70)

    # Stage 1: data prep
    print("Stage 1: load + filter Stratum 4 + compute recovery_phase + t_days...")
    prep = stage1_data_prep()
    df = prep["df"]
    print("  n_s4=" + str(prep["n_s4"]))
    print("  channels=" + ", ".join(CHANNELS))
    # Per-phase n
    for ph_name, _, _ in PHASE_BOUNDARIES:
        n_ph = int((df["recovery_phase"] == ph_name).sum())
        print("  phase " + ph_name + ": n=" + str(n_ph))

    # Stage 2: raw rho
    print("Stage 2: raw rho matrix (21 pairs; Spearman; verification of Q3.9.e)...")
    raw = stage2_raw_rho(df)
    # Verify the 5 PRIMARY Q3.9.e targets
    q39e_targets = {
        "stress_mean_sleep": -0.194,
        "stress_stdev_sleep": -0.121,
        "all_day_stress_avg": -0.056,
        "resting_hr": 0.020,
        "bb_lowest": 0.010,
    }
    print("  Q3.9.e verification (gevoelscore x X pairs):")
    for chan, q39e in q39e_targets.items():
        key = None
        for k in raw:
            if set(k) == {chan, "gevoelscore"}:
                key = k
                break
        if key is None:
            print("    " + chan + ": pair not found")
            continue
        rho_v = raw[key]["rho"]
        n_v = raw[key]["n"]
        match = (
            "OK"
            if (not np.isnan(rho_v)) and abs(rho_v - q39e) < 0.005
            else "DRIFT"
        )
        rho_str = "n/a" if np.isnan(rho_v) else "{:+.3f}".format(rho_v)
        print(
            "    " + chan + " x gevoelscore: rho=" + rho_str
            + "; n=" + str(n_v)
            + "; vs Q3.9.e {:+.3f}: ".format(q39e) + match
        )

    # Stage 3: linear OLS detrend
    print("Stage 3: linear OLS detrend per channel; rho on residuals...")
    ols = stage3_linear_ols_detrend(df)

    # Stage 4: rolling-median 90d
    print(
        "Stage 4: rolling-median 90d centred detrend; rho on residuals..."
    )
    rolling = stage4_rolling_median_detrend(df)

    # Stage 5: per-recovery-phase detrend
    print("Stage 5: per-recovery-phase residual detrend; rho on residuals...")
    phase = stage5_per_phase_detrend(df)

    # Stage 5b: per-phase granularity (within-phase raw rho)
    print(
        "Stage 5b: per-recovery-phase granularity (within-phase raw rho for n>=30 phases)..."
    )
    phase_granularity = stage5b_per_phase_granularity(df)

    # Stage 6: sensitivity
    print("Stage 6: sensitivity comparison + spurious-flag table...")
    sens = stage6_sensitivity(raw, ols, rolling, phase)
    print(
        "  n_pairs_total=" + str(sens["n_pairs_total"])
        + "; n_pairs_spurious=" + str(sens["n_pairs_spurious"])
    )
    print(
        "  per-method counts: ols=" + str(sens["per_method_spurious_counts"]["ols"])
        + "; rolling=" + str(sens["per_method_spurious_counts"]["rolling"])
        + "; phase=" + str(sens["per_method_spurious_counts"]["phase"])
    )
    print(
        "  long-memory pairs: " + str(sens["long_memory_pairs_spurious"])
        + " spurious of " + str(sens["long_memory_pairs_total"])
    )
    print(
        "  short-memory pairs: " + str(sens["short_memory_pairs_spurious"])
        + " spurious of " + str(sens["short_memory_pairs_total"])
    )

    # Compose summary
    summary = {
        "as_of_date": AS_OF_DATE,
        "n_s4": prep["n_s4"],
        "channels": CHANNELS,
        "channel_memory": CHANNEL_MEMORY,
        "long_memory_channels": sorted(LONG_MEMORY_CHANNELS),
        "short_memory_channels": sorted(SHORT_MEMORY_CHANNELS),
        "rolling_median_window": ROLLING_MEDIAN_WINDOW,
        "spurious_flag_threshold": SPURIOUS_FLAG_THRESHOLD,
        "stage2_raw_rho": _serialize_pair_rhos(raw),
        "stage3_ols_detrend": {
            "pair_rhos": _serialize_pair_rhos(ols["pair_rhos"]),
        },
        "stage4_rolling_median_detrend": {
            "pair_rhos": _serialize_pair_rhos(rolling["pair_rhos"]),
        },
        "stage5_per_phase_detrend": {
            "pair_rhos": _serialize_pair_rhos(phase["pair_rhos"]),
        },
        "stage5b_per_phase_granularity": {
            ph: (
                {
                    "n": info["n"],
                    "skipped": info.get("skipped", False),
                    "pair_rhos": _serialize_pair_rhos(info["pair_rhos"]),
                }
                if not info.get("skipped", True)
                else {"n": info["n"], "skipped": True}
            )
            for ph, info in phase_granularity.items()
        },
        "stage6_sensitivity": {
            "rows": _serialize_rows(sens["rows"]),
            "n_pairs_total": sens["n_pairs_total"],
            "n_pairs_spurious": sens["n_pairs_spurious"],
            "spurious_pairs": [
                " x ".join(p) for p in sens["spurious_pairs"]
            ],
            "long_memory_pairs_total": sens["long_memory_pairs_total"],
            "long_memory_pairs_spurious": sens["long_memory_pairs_spurious"],
            "short_memory_pairs_total": sens["short_memory_pairs_total"],
            "short_memory_pairs_spurious": sens["short_memory_pairs_spurious"],
            "per_method_spurious_counts": sens["per_method_spurious_counts"],
        },
    }

    # Build a Python-native summary for findings.md emit (keep tuple keys
    # for stage6 + use unrolled pair_rhos for stages 2-5).
    findings_summary = {
        "as_of_date": AS_OF_DATE,
        "n_s4": prep["n_s4"],
        "stage6_sensitivity": sens,
        "stage5b_per_phase_granularity": phase_granularity,
    }

    # Stage 7: plots
    print("Stage 7: emitting plots...")
    plots_dir = HERE / "plots"
    written = stage7_make_plots(findings_summary, plots_dir)
    for p in written:
        print("  " + p)

    # Persist summary.json
    summary_path = HERE / "summary.json"
    summary_path.write_text(
        json.dumps(_convert_for_json(summary), indent=2, default=str),
        encoding="utf-8",
    )
    print()
    print("Wrote " + str(summary_path))

    # Stage 8: emit findings.md + README.md
    print("Stage 8: emitting findings.md + README.md...")
    findings_path = HERE / "findings.md"
    stage8_emit_findings(findings_summary, findings_path)
    print("  " + str(findings_path))

    readme_path = HERE / "README.md"
    stage8_emit_readme(findings_summary, readme_path)
    print("  " + str(readme_path))

    print()
    print(
        "Done. Q4.5.b LANDED (Tier 3 Core 5 4th of 5; methodological sanity "
        "check on Q3.9.e + Q4.9 rho findings)."
    )


if __name__ == "__main__":
    main()
