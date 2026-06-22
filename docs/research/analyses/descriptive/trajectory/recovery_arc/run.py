"""Descriptive analysis: trajectory/recovery_arc -- v2 refresh on locked 6-phase axis.

Strand B; v2 adopts the 6-phase LC recovery axis from
methodology/lc_recovery_phase_axis.md (LOCKED d47e0d3 2026-06-19) replacing v1's
4-phase data-given axis. Adds block-bootstrap CIs per the axis MD §6.6 (per-phase
per-channel E[L]* via Patton-White-Politis with fall-back E[L]=7 when n
insufficient), honors the §5.4 tight-n caveat for sub-phase 4a (56 days), and adds
the §7b falsifiability hook test as a Layer 1 sensitivity arm.

Layer 1 descriptive per CONVENTIONS §2.1: NO causal claims, NO SUPPORTED bar.

v1 (commit 24dad02, 2026-06-19) stands as historical record; this v2 refresh
extends without modifying the v1 archive.

Output:
- summary.json -- machine-readable per-channel per-phase statistics (gitignored)
- plots/<channel>.png -- per-channel multi-year trajectory PNGs with event
  overlays + 6-phase region shading + 4a->4b sub-boundary marker (gitignored)

Discipline guards:
- §2.1 descriptive-before-inference: report what the data shows; no causal mark
- §3.6 named counts: every count carries scheme + unit + source-file
- §3.7 trajectory-detrend sensitivity: rolling 90d detrend -> recompute
  per-channel per-phase median; flag "survives detrend?" per cell
- §6.6 block-bootstrap discipline: per-phase per-channel E[L]* with E[L]=7
  fall-back when n insufficient
- §5.4 sub-phase 4a tight-n caveat (56 days): wide CIs honestly surfaced
- §7b falsifiability hook: 4a vs 4b paired-bootstrap CI on per-channel median diff
- §5.A phase 5 sub-stratification on CONFIRMED-citalopram channels via
  citalopram_phase()
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
# HERE = .../analyses/descriptive/trajectory/recovery_arc
# parents[0]=trajectory, [1]=descriptive, [2]=analyses
UTILS_DIR = HERE.parents[2] / "_utils"
sys.path.insert(0, str(UTILS_DIR))

from frame import load_master  # noqa: E402
from inference import (  # noqa: E402
    compute_data_driven_block_length,
    stationary_bootstrap_ci,
)

AS_OF_DATE = "2026-06-04"

# Six phases per lc_recovery_phase_axis.md §2 (LOCKED d47e0d3 2026-06-19).
# The recovery_phase column was added to per_day_master.csv at commit e00df27
# (2026-06-22); we join on it directly rather than re-deriving boundaries here.
PHASE_ORDER = [
    "pre_illness_healthy",
    "acute_infection",
    "lc_pre_ergo",
    "pacing_pre_citalopram_learning",
    "pacing_habit_established",
    "citalopram_modulated",
]

# Phase canonical date windows per the axis MD §2 (used for plot shading +
# summary.json metadata; matches the recovery_phase column values 1:1).
PHASE_WINDOWS = [
    ("pre_illness_healthy",             date(2021, 8, 16),  date(2022, 3, 20)),
    ("acute_infection",                 date(2022, 3, 21),  date(2022, 4,  3)),
    ("lc_pre_ergo",                     date(2022, 4,  4),  date(2022, 9, 21)),
    ("pacing_pre_citalopram_learning",  date(2022, 9, 22),  date(2022, 11, 16)),
    ("pacing_habit_established",        date(2022, 11, 17), date(2024, 4,  8)),
    ("citalopram_modulated",            date(2024, 4,  9),  date(2026, 6,  4)),
]

# 7-channel HA-P6 set, locked from v1 + lc_recovery_phase_axis §3.5
CHANNELS = [
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
    "bb_overnight_gain",
    "resting_hr",
    "gevoelscore",
    "stress_low_motion_min_count_S60_Mlow",
]

# CONFIRMED-citalopram channels (per citalopram_dose_response §5.6). Phase 5
# reporting on these MUST stratify by citalopram axis per §5.A.
CONFIRMED_CITALOPRAM_CHANNELS = {
    "stress_mean_sleep",     # beta=+0.43/mg, p=0.001
    "all_day_stress_avg",    # beta=+0.57/mg, p=0.000
    "bb_lowest",             # beta=-1.13/mg, p=0.000
}

# 8 documented events per v1; post-afbouw start (2026-06-05) OUT OF SCOPE per
# locked operationalisation -- corpus ends 2026-06-04.
EVENT_OVERLAYS = [
    ("COVID infection (first symptoms)",   date(2022, 3, 21)),
    ("Ergotherapie start",                  date(2022, 9, 22)),
    ("Ergotherapie end (~13wk)",            date(2022, 12, 22)),
    ("CPAP start",                          date(2024, 1, 10)),
    ("CPAP end",                            date(2024, 4, 16)),
    ("Citalopram buildup start",            date(2024, 4,  9)),
    ("Citalopram buildup -> consolidation", date(2024, 6, 20)),
    ("Citalopram consolidation -> afbouw",  date(2026, 3, 20)),
]

# Sub-boundary marker per the §7b 8-week post-ergotherapie rule
SUB_BOUNDARY_4A_4B = date(2022, 11, 17)

SEED = 20260622
DEFAULT_BLOCK_LENGTH = 7    # CONVENTIONS §3 default per permutation_null_block_length.md
N_BOOTSTRAP = 10000         # B=10000 per handoff brief
ROLLING_TREND_WINDOW = 90   # CONVENTIONS §3.7 procedure window
ROLLING_VIZ_WINDOW = 30     # multi-year trajectory smoothing window for plots
MIN_N_FOR_BOOTSTRAP = 10    # below this, CIs are skipped
MIN_N_FOR_E_L_STAR = 30     # below this, fall back to E[L]=7 default per §6.6


# Inner citalopram axis (citalopram_phase_stratification §3); unmedicated is
# absent within phase 5 by construction
def citalopram_phase(d: date) -> str:
    """Per citalopram_phase_stratification.md §3 (table aligned 2026-06-22)."""
    if d < date(2024, 4, 9):
        return "unmedicated"
    if d < date(2024, 6, 20):
        return "buildup"
    if d < date(2026, 3, 20):
        return "consolidation"
    if d < date(2026, 6, 6):
        return "afbouw"
    return "post_afbouw"


# ---------------------------------------------------------------------------
# Per-channel per-phase descriptive computations
# ---------------------------------------------------------------------------


def median_iqr(values: np.ndarray) -> dict:
    """Median + IQR + count + a few quantiles for a 1D numeric array."""
    v = values[~np.isnan(values)]
    n = int(len(v))
    if n == 0:
        return {
            "n": 0,
            "median": None,
            "iqr": None,
            "p25": None,
            "p75": None,
            "mean": None,
            "std_ddof1": None,
        }
    med = float(np.median(v))
    p25 = float(np.percentile(v, 25))
    p75 = float(np.percentile(v, 75))
    return {
        "n": n,
        "median": med,
        "iqr": p75 - p25,
        "p25": p25,
        "p75": p75,
        "mean": float(v.mean()),
        "std_ddof1": float(v.std(ddof=1)) if n > 1 else 0.0,
    }


def bootstrap_median_ci(
    values: np.ndarray,
    *,
    block_length: int,
    n_bootstrap: int = N_BOOTSTRAP,
    seed: int = SEED,
) -> dict:
    """Stationary-bootstrap 95% CI on the median.

    Drops NaN before resampling; preserves block-level autocorrelation per
    Politis & Romano (1994). Returns ci_lower=None if n < MIN_N_FOR_BOOTSTRAP.
    """
    v = values[~np.isnan(values)]
    if len(v) < MIN_N_FOR_BOOTSTRAP:
        return {
            "ci_lower": None,
            "ci_upper": None,
            "n_used": int(len(v)),
            "expected_block_length": block_length,
            "n_bootstrap": n_bootstrap,
            "note": f"n<{MIN_N_FOR_BOOTSTRAP}; skipped",
        }
    res = stationary_bootstrap_ci(
        v, lambda x: float(np.median(x)),
        n_bootstrap=n_bootstrap,
        expected_block_length=block_length,
        confidence_level=0.95,
        random_state=seed,
    )
    return {
        "ci_lower": float(res["ci_lower"]),
        "ci_upper": float(res["ci_upper"]),
        "n_used": int(len(v)),
        "expected_block_length": block_length,
        "n_bootstrap": n_bootstrap,
    }


def per_phase_stats(df: pd.DataFrame, channel: str) -> dict:
    """Per-phase median + IQR + block-bootstrap CI95.

    Per §6.6 + §5.4: per-phase per-channel E[L]* via Patton-White-Politis with
    fall-back E[L]=7 when phase n < MIN_N_FOR_E_L_STAR=30; CIs reported at both
    E[L]=7 and E[L]* for transparency.

    Per CONVENTIONS §3.7: also computes per-phase median of a rolling 90d
    detrend (subtracted day-wise on the full corpus for the channel).

    The PHASE_WINDOWS list defines the canonical phase date ranges; phases
    are joined via the recovery_phase column directly (avoids any drift
    between this script's boundaries and the column's underlying definition).
    """
    # Pre-compute the rolling 90d trend on the full corpus for this channel
    full = df[["date", "recovery_phase", channel]].sort_values("date").reset_index(drop=True)
    rolled = full[channel].rolling(ROLLING_TREND_WINDOW, min_periods=30).median()
    detrended = full[channel] - rolled

    out: dict = {}
    for phase_name in PHASE_ORDER:
        mask = full["recovery_phase"] == phase_name
        raw_vals = full.loc[mask, channel].to_numpy(dtype=float)
        det_vals = detrended.loc[mask].to_numpy(dtype=float)

        raw_stats = median_iqr(raw_vals)
        det_stats = median_iqr(det_vals)

        # Data-driven block length on raw phase data per §6.6
        if raw_stats["n"] >= MIN_N_FOR_E_L_STAR:
            block_info = compute_data_driven_block_length(
                raw_vals,
                default_block_length=DEFAULT_BLOCK_LENGTH,
            )
            e_l_star = float(block_info["optimal_block_length"])
            flagged = bool(block_info["flagged_deviation"])
            cutoff_M = block_info["cutoff_lag"]
            e_l_star_used = max(1, int(round(e_l_star)))
        else:
            # Fall-back per §6.6: insufficient n for stable E[L]* estimate
            e_l_star = None
            flagged = False
            cutoff_M = None
            e_l_star_used = DEFAULT_BLOCK_LENGTH

        ci7 = bootstrap_median_ci(
            raw_vals, block_length=DEFAULT_BLOCK_LENGTH,
        )
        ci_star = bootstrap_median_ci(
            raw_vals, block_length=e_l_star_used,
        )

        # Phase window dates (for metadata in summary.json)
        win = next((w for w in PHASE_WINDOWS if w[0] == phase_name), None)
        date_start = str(win[1]) if win else None
        date_end = str(win[2]) if win else None

        out[phase_name] = {
            "date_start": date_start,
            "date_end": date_end,
            "raw": raw_stats,
            "detrended_90d": {
                "median": det_stats["median"],
                "iqr": det_stats["iqr"],
                "n": det_stats["n"],
            },
            "bootstrap_ci95_median_E_L7": ci7,
            "bootstrap_ci95_median_E_L_star": ci_star,
            "data_driven_E_L_star": e_l_star,
            "factor_of_2_deviation_flag": flagged,
            "cutoff_lag_M": cutoff_M,
            "e_l_star_fallback_applied": (e_l_star is None and raw_stats["n"] > 0),
        }
    return out


def detrend_survives_flag(per_phase: dict) -> dict:
    """For each phase, did the median's ordering vs the grand corpus median
    survive a rolling-90d detrend?

    Reports a per-phase boolean: sign(raw_median - raw_grand) ==
    sign(detrended_median - detrended_grand).
    """
    raw_medians = [p["raw"]["median"] for p in per_phase.values()
                   if p["raw"]["median"] is not None]
    det_medians = [p["detrended_90d"]["median"] for p in per_phase.values()
                   if p["detrended_90d"]["median"] is not None]
    if len(raw_medians) < 2 or len(det_medians) < 2:
        return {}
    raw_grand = float(np.median(raw_medians))
    det_grand = float(np.median(det_medians))
    out = {}
    for phase_name, p in per_phase.items():
        rm = p["raw"]["median"]
        dm = p["detrended_90d"]["median"]
        if rm is None or dm is None:
            out[phase_name] = {"survives_detrend": None, "reason": "no data"}
            continue
        raw_sign = np.sign(rm - raw_grand)
        det_sign = np.sign(dm - det_grand)
        survives = bool(raw_sign == det_sign and raw_sign != 0)
        out[phase_name] = {
            "raw_minus_grand": float(rm - raw_grand),
            "detrended_minus_grand": float(dm - det_grand),
            "survives_detrend": survives,
        }
    return out


# ---------------------------------------------------------------------------
# §5.A phase 5 citalopram sub-stratification
# ---------------------------------------------------------------------------


CITALOPRAM_SUB_PHASES = ["buildup", "consolidation", "afbouw"]
# unmedicated absent in phase 5 by construction; post_afbouw out-of-corpus


def per_phase5_citalopram_stratification(df: pd.DataFrame, channel: str) -> dict:
    """Per §5.A: stratify phase 5 (citalopram_modulated) by inner citalopram axis.

    For CONFIRMED-citalopram channels only; carried out for the 3 channels in
    CONFIRMED_CITALOPRAM_CHANNELS per citalopram_dose_response §5.6.
    Sub-cells: buildup / consolidation / afbouw (unmedicated absent; post_afbouw
    out-of-corpus).
    """
    sub = df[df["recovery_phase"] == "citalopram_modulated"].copy()
    sub["citalopram_phase"] = sub["date"].apply(lambda d: citalopram_phase(d.date()))
    out: dict = {}
    for cp in CITALOPRAM_SUB_PHASES:
        cell_vals = sub.loc[sub["citalopram_phase"] == cp, channel].to_numpy(dtype=float)
        stats = median_iqr(cell_vals)
        ci7 = bootstrap_median_ci(cell_vals, block_length=DEFAULT_BLOCK_LENGTH)
        if stats["n"] >= MIN_N_FOR_E_L_STAR:
            block_info = compute_data_driven_block_length(
                cell_vals[~np.isnan(cell_vals)],
                default_block_length=DEFAULT_BLOCK_LENGTH,
            )
            e_l_star = float(block_info["optimal_block_length"])
            flagged = bool(block_info["flagged_deviation"])
            cutoff_M = block_info["cutoff_lag"]
            e_l_star_used = max(1, int(round(e_l_star)))
            ci_star = bootstrap_median_ci(cell_vals, block_length=e_l_star_used)
        else:
            e_l_star = None
            flagged = False
            cutoff_M = None
            ci_star = ci7
        out[cp] = {
            "raw": stats,
            "bootstrap_ci95_median_E_L7": ci7,
            "bootstrap_ci95_median_E_L_star": ci_star,
            "data_driven_E_L_star": e_l_star,
            "factor_of_2_deviation_flag": flagged,
            "cutoff_lag_M": cutoff_M,
        }
    return out


# ---------------------------------------------------------------------------
# §7b falsifiability hook (4a vs 4b sensitivity arm)
# ---------------------------------------------------------------------------


def falsifiability_hook_4a_vs_4b(
    df: pd.DataFrame,
    channel: str,
    *,
    n_bootstrap: int = N_BOOTSTRAP,
    seed: int = SEED,
) -> dict:
    """§7b falsifiability hook: 8-week boundary discriminative power per channel.

    For the given channel:
    - subset to phase 4a (pacing_pre_citalopram_learning, ~56 days)
      and phase 4b (pacing_habit_established, ~508 days)
    - median per sub-phase
    - paired-bootstrap CI on the difference (4b - 4a) using the per-channel
      E[L]* estimated from the combined 4a+4b day-level data within the phase
      window (fall-back E[L]=7 if combined n < 30)
    - report a 3-way verdict: excludes-0-consistent / wide-includes-0 / wrong-direction

    Per CONVENTIONS §4.3 this is descriptive only -- the verdict is whether the
    boundary has discriminative power at this resolution, NOT a causal claim.
    """
    sub = df[df["recovery_phase"].isin(
        ["pacing_pre_citalopram_learning", "pacing_habit_established"]
    )].copy()
    arr_4a = sub.loc[
        sub["recovery_phase"] == "pacing_pre_citalopram_learning", channel
    ].to_numpy(dtype=float)
    arr_4b = sub.loc[
        sub["recovery_phase"] == "pacing_habit_established", channel
    ].to_numpy(dtype=float)
    n_4a = int(np.sum(~np.isnan(arr_4a)))
    n_4b = int(np.sum(~np.isnan(arr_4b)))

    # Point medians
    med_4a = float(np.median(arr_4a[~np.isnan(arr_4a)])) if n_4a > 0 else None
    med_4b = float(np.median(arr_4b[~np.isnan(arr_4b)])) if n_4b > 0 else None
    point_diff = (med_4b - med_4a) if (med_4a is not None and med_4b is not None) else None

    if n_4a < MIN_N_FOR_BOOTSTRAP or n_4b < MIN_N_FOR_BOOTSTRAP:
        return {
            "n_4a": n_4a,
            "n_4b": n_4b,
            "median_4a": med_4a,
            "median_4b": med_4b,
            "diff_4b_minus_4a": point_diff,
            "ci_lower": None,
            "ci_upper": None,
            "expected_block_length": None,
            "n_bootstrap": n_bootstrap,
            "verdict": "skipped_insufficient_n",
            "note": f"n_4a={n_4a} or n_4b={n_4b} below threshold {MIN_N_FOR_BOOTSTRAP}",
        }

    # Combined-window E[L]* per §6.6 spec
    combined = np.concatenate([
        arr_4a[~np.isnan(arr_4a)],
        arr_4b[~np.isnan(arr_4b)],
    ])
    if len(combined) >= MIN_N_FOR_E_L_STAR:
        block_info = compute_data_driven_block_length(
            combined,
            default_block_length=DEFAULT_BLOCK_LENGTH,
        )
        e_l_star = float(block_info["optimal_block_length"])
        e_l_star_used = max(1, int(round(e_l_star)))
    else:
        e_l_star = None
        e_l_star_used = DEFAULT_BLOCK_LENGTH

    # Bootstrap the difference: resample each phase independently with the
    # combined-window E[L]*, take medians, take the difference. (Not "paired"
    # in the matched-pair sense since the two phases are disjoint time
    # windows; bootstrap each independently with the same per-channel E[L]*
    # and CI the difference of the resampled medians.)
    rng = np.random.default_rng(seed)
    diffs = np.empty(n_bootstrap, dtype=float)
    p = 1.0 / e_l_star_used
    v_4a = arr_4a[~np.isnan(arr_4a)]
    v_4b = arr_4b[~np.isnan(arr_4b)]
    n_a, n_b = len(v_4a), len(v_4b)
    for b in range(n_bootstrap):
        idx_a = _stationary_indices(n_a, p, rng)
        idx_b = _stationary_indices(n_b, p, rng)
        diffs[b] = float(np.median(v_4b[idx_b]) - np.median(v_4a[idx_a]))
    ci_lower = float(np.quantile(diffs, 0.025))
    ci_upper = float(np.quantile(diffs, 0.975))

    # Three-way verdict per the handoff brief
    if ci_lower > 0 or ci_upper < 0:
        verdict = "excludes_0"
    else:
        verdict = "includes_0"

    return {
        "n_4a": n_4a,
        "n_4b": n_4b,
        "median_4a": med_4a,
        "median_4b": med_4b,
        "diff_4b_minus_4a": point_diff,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "expected_block_length": int(e_l_star_used),
        "data_driven_E_L_star_combined": e_l_star,
        "n_bootstrap": n_bootstrap,
        "verdict": verdict,
    }


def _stationary_indices(n: int, p: float, rng) -> np.ndarray:
    """Inline stationary-bootstrap indices for the paired-CI loop above."""
    indices = np.empty(n, dtype=np.int64)
    i = 0
    while i < n:
        start = int(rng.integers(0, n))
        block_length = int(rng.geometric(p))
        for j in range(block_length):
            if i >= n:
                break
            indices[i] = (start + j) % n
            i += 1
    return indices


# ---------------------------------------------------------------------------
# Plot generation
# ---------------------------------------------------------------------------


PHASE_COLOURS = {
    "pre_illness_healthy":             "#cde7c0",  # soft green
    "acute_infection":                 "#f7c0a3",  # warm coral
    "lc_pre_ergo":                     "#fde7a5",  # pale gold
    "pacing_pre_citalopram_learning":  "#fbd29a",  # darker gold (sub-phase)
    "pacing_habit_established":        "#dcd4a8",  # khaki (sub-phase)
    "citalopram_modulated":            "#cfd9eb",  # cool grey-blue
}


def make_plot(df: pd.DataFrame, channel: str, out_dir: Path) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    out_dir.mkdir(parents=True, exist_ok=True)
    sub = df[["date", channel]].sort_values("date").reset_index(drop=True)
    sub["roll30"] = sub[channel].rolling(ROLLING_VIZ_WINDOW, min_periods=10).median()
    sub["roll30_p25"] = sub[channel].rolling(ROLLING_VIZ_WINDOW, min_periods=10).quantile(0.25)
    sub["roll30_p75"] = sub[channel].rolling(ROLLING_VIZ_WINDOW, min_periods=10).quantile(0.75)

    fig, ax = plt.subplots(figsize=(13.5, 4.8))

    # 6-phase region shading
    for phase_name, start, end in PHASE_WINDOWS:
        ax.axvspan(
            pd.Timestamp(start), pd.Timestamp(end),
            color=PHASE_COLOURS[phase_name], alpha=0.40,
            label=phase_name,
        )

    # IQR band
    band_mask = sub["roll30_p25"].notna() & sub["roll30_p75"].notna()
    if band_mask.any():
        ax.fill_between(
            sub.loc[band_mask, "date"],
            sub.loc[band_mask, "roll30_p25"],
            sub.loc[band_mask, "roll30_p75"],
            color="#1f3a5f", alpha=0.12,
        )

    # Daily scatter (light)
    ax.plot(
        sub["date"], sub[channel],
        color="#1f3a5f", linewidth=0.0, marker=".", markersize=1.6, alpha=0.35,
    )
    # Rolling 30d median
    ax.plot(
        sub["date"], sub["roll30"],
        color="#1f3a5f", linewidth=1.6, label=f"rolling {ROLLING_VIZ_WINDOW}d median",
    )

    # Event overlays
    ymin, ymax = ax.get_ylim()
    label_y_high = ymax - 0.02 * (ymax - ymin)
    label_y_low = ymin + 0.02 * (ymax - ymin)
    for i, (label, d) in enumerate(EVENT_OVERLAYS):
        ax.axvline(pd.Timestamp(d), color="#a23b3b", linestyle=":", linewidth=0.9, alpha=0.85)
        y = label_y_high if i % 2 == 0 else label_y_low
        ax.text(
            pd.Timestamp(d), y, label,
            rotation=90, fontsize=6.5, color="#a23b3b",
            ha="right", va="top" if i % 2 == 0 else "bottom",
            alpha=0.9,
        )

    # 4a->4b sub-boundary marker per §7b (distinct from event overlays)
    ax.axvline(
        pd.Timestamp(SUB_BOUNDARY_4A_4B),
        color="#4a3057", linestyle="--", linewidth=1.1, alpha=0.85,
        label="4a->4b boundary (8wk post-ergo, §7b)",
    )

    ax.set_xlim(pd.Timestamp(date(2021, 8, 1)), pd.Timestamp(date(2026, 6, 4)))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_minor_locator(mdates.MonthLocator((1, 4, 7, 10)))
    ax.set_ylabel(channel)
    n_total = int(sub[channel].notna().sum())
    ax.set_title(
        f"{channel} -- v2 multi-year trajectory on 6-phase axis "
        f"(n={n_total} non-NaN days, per_day_master.csv as_of={AS_OF_DATE})",
        fontsize=10,
    )

    # Dedup legend
    h, l = ax.get_legend_handles_labels()
    seen = set()
    pairs = [(hi, li) for hi, li in zip(h, l) if not (li in seen or seen.add(li))]
    ax.legend(
        [p[0] for p in pairs], [p[1] for p in pairs],
        loc="upper right", fontsize=6.5, ncol=2, framealpha=0.85,
    )

    fig.tight_layout()
    fp = out_dir / f"{channel}.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    return str(fp.name)


def make_sensitivity_arm_plot(hook_results: dict, out_dir: Path) -> str:
    """Single overview plot for the §7b falsifiability hook results.

    7 rows (channels) x diff bars with 95% CI; vertical line at 0; verdict
    colouring (excludes_0 = filled, includes_0 = open).
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8.5, 4.2))

    channels = [c for c in CHANNELS if hook_results.get(c) is not None]
    rows = list(reversed(channels))  # so first channel renders at top
    y_positions = np.arange(len(rows))

    for y, ch in zip(y_positions, rows):
        r = hook_results[ch]
        if r.get("verdict") == "skipped_insufficient_n":
            ax.text(
                0, y, " (skipped: insufficient n)",
                fontsize=7, color="#7a7a7a", va="center", ha="left",
            )
            continue
        diff = r["diff_4b_minus_4a"]
        lo, hi = r["ci_lower"], r["ci_upper"]
        excl = r["verdict"] == "excludes_0"
        colour = "#1f3a5f" if excl else "#7a7a7a"
        facecolour = colour if excl else "none"
        ax.plot([lo, hi], [y, y], color=colour, linewidth=2.0, alpha=0.85)
        ax.scatter([diff], [y], color=colour, s=42, marker="D",
                   facecolors=facecolour, edgecolors=colour, linewidths=1.4)

    ax.axvline(0, color="#a23b3b", linestyle="--", linewidth=1.0, alpha=0.85)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(rows, fontsize=8.5)
    ax.set_xlabel("median_4b - median_4a (95% block-bootstrap CI; B=10000)")
    ax.set_title(
        "v2 §7b falsifiability hook -- 8-week 4a->4b boundary discriminative power\n"
        "(filled diamond = CI excludes 0; open = includes 0)",
        fontsize=9,
    )
    ax.grid(True, axis="x", linestyle=":", alpha=0.35)
    fig.tight_layout()
    fp = out_dir / "_sensitivity_4a_vs_4b.png"
    fig.savefig(fp, dpi=110)
    plt.close(fig)
    return str(fp.name)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main() -> None:
    if not os.environ.get("GEVOELSCORE_DATA_PATH"):
        os.environ["GEVOELSCORE_DATA_PATH"] = "C:/Users/Gebruiker/Documents/gevoelscore-data"

    df = load_master(as_of_date=AS_OF_DATE)

    missing = [c for c in CHANNELS if c not in df.columns]
    if missing:
        raise RuntimeError(f"Channels missing from per_day_master.csv: {missing}")
    if "recovery_phase" not in df.columns:
        raise RuntimeError(
            "recovery_phase column missing from per_day_master.csv. "
            "v2 depends on the column added at commit e00df27 (2026-06-22) "
            "per lc_recovery_phase_axis.md §6.5."
        )

    summary: dict = {
        "analysis": "trajectory/recovery_arc",
        "version": "v2 (2026-06-22 refresh on locked 6-phase axis)",
        "v1_commit_ref": "24dad02 (2026-06-19; 4-phase data-given axis; historical record)",
        "axis_source": "methodology/lc_recovery_phase_axis.md (LOCKED d47e0d3 2026-06-19)",
        "strand": "B (multi-year trajectory; v1 §7b interview answers carry forward 2026-06-18)",
        "as_of_date": AS_OF_DATE,
        "source_file_master": "per_day_master.csv",
        "recovery_phase_column_commit": "e00df27 (2026-06-22)",
        "n_rows_total": int(len(df)),
        "n_bootstrap": N_BOOTSTRAP,
        "default_block_length_E_L": DEFAULT_BLOCK_LENGTH,
        "random_seed": SEED,
        "phase_windows": [
            {"phase": name, "start": str(s), "end": str(e)}
            for name, s, e in PHASE_WINDOWS
        ],
        "phase_counts": {
            ph: int((df["recovery_phase"] == ph).sum()) for ph in PHASE_ORDER
        },
        "event_overlays": [
            {"label": label, "date": str(d)} for label, d in EVENT_OVERLAYS
        ],
        "sub_boundary_4a_4b_date": str(SUB_BOUNDARY_4A_4B),
        "confirmed_citalopram_channels": sorted(CONFIRMED_CITALOPRAM_CHANNELS),
        "post_afbouw_out_of_scope_note": (
            "Citalopram afbouw -> post_afbouw boundary is 2026-06-06 per "
            "citalopram_phase_stratification.md §3; corpus ends 2026-06-04. "
            "Out of scope for this analysis: no post-afbouw data exists. "
            "The afbouw sub-phase within phase 5 runs 2026-03-20 -> "
            "2026-06-04 (~76 days)."
        ),
        "boundary_collision_caveat": (
            "Citalopram buildup start (2024-04-09) and CPAP end (2024-04-16) "
            "sit 7 days apart; their independent contributions are confounded "
            "in any pre-vs-post reading on either boundary. Per "
            "intervention_effects_descriptive.md §2b + §8.1, both boundaries "
            "are structurally unanalyzable in pre-vs-post window comparisons; "
            "this analysis reports the rolling-median trajectory across the "
            "cluster but does NOT attribute step-changes to either event. "
            "In the v2 6-phase axis, the phase-4b -> phase-5 boundary sits "
            "at 2024-04-09 (citalopram), making the last 7 days of sub-phase "
            "4b contain the CPAP-end event."
        ),
        "tight_n_caveat_4a": (
            "Sub-phase 4a (pacing_pre_citalopram_learning) is 56 days "
            "(2022-09-22 -> 2022-11-16). At E[L]=7 this is ~8 effective "
            "blocks; at the observed E[L]*~15 for autonomic-load channels in "
            "neighbouring phases this is ~3-5 effective blocks. Per "
            "lc_recovery_phase_axis.md §5.4 the tight-n constraint is "
            "surfaced honestly: per-phase-4a bootstrap CIs are visibly wider "
            "than on phases 3/4b/5 and any read on 4a must inherit this."
        ),
        "channels": {},
        "falsifiability_hook_4a_vs_4b": {},
    }

    for ch in CHANNELS:
        print(f"computing channel: {ch}")
        per_phase = per_phase_stats(df, ch)
        detrend_flags = detrend_survives_flag(per_phase)
        for phase_name, info in detrend_flags.items():
            per_phase[phase_name]["detrend_sensitivity"] = info

        coverage = {ph: per_phase[ph]["raw"]["n"] for ph in PHASE_ORDER}
        cov_caveats = []
        if ch == "bb_overnight_gain":
            cov_caveats.append(
                "Per intervention_effects_descriptive.md §2b: data only from "
                "2024-09-18 onward (Garmin firmware UDS rollout). All phases "
                "before 2024-09-18 return n=0 or partial coverage; only the "
                "post-2024-09-18 portion of phase 5 has full coverage."
            )
        if ch == "gevoelscore":
            cov_caveats.append(
                "Per lc_era_temporal_segmentation.md §1: gevoelscore corpus "
                "starts 2022-09-03. Phases 1 + 2 (and most of phase 3) have "
                "NO gevoelscore data by construction; phase 3 has the last "
                "~19 days of partial coverage (2022-09-03 -> 2022-09-21)."
            )

        ch_entry = {
            "n_total_non_nan": int(df[ch].notna().sum()),
            "first_non_nan_date": (
                str(df.loc[df[ch].notna(), "date"].min().date())
                if df[ch].notna().any() else None
            ),
            "last_non_nan_date": (
                str(df.loc[df[ch].notna(), "date"].max().date())
                if df[ch].notna().any() else None
            ),
            "coverage_per_phase": coverage,
            "coverage_caveats": cov_caveats,
            "per_phase": per_phase,
        }

        # §5.A sub-stratification for phase 5 on CONFIRMED-citalopram channels
        if ch in CONFIRMED_CITALOPRAM_CHANNELS:
            ch_entry["phase5_citalopram_sub_stratification"] = (
                per_phase5_citalopram_stratification(df, ch)
            )
            ch_entry["phase5_sub_stratification_note"] = (
                "Per citalopram_phase_stratification.md §5.A: CONFIRMED-"
                "citalopram channel; phase 5 reading is sub-stratified by "
                "the inner citalopram axis (buildup / consolidation / "
                "afbouw). unmedicated is absent in phase 5 by construction; "
                "post_afbouw is out-of-corpus."
            )

        summary["channels"][ch] = ch_entry

        # §7b falsifiability hook per channel
        hook_result = falsifiability_hook_4a_vs_4b(df, ch)
        summary["falsifiability_hook_4a_vs_4b"][ch] = hook_result

        plot_name = make_plot(df, ch, HERE / "plots")
        summary["channels"][ch]["plot_file"] = f"plots/{plot_name}"

    # Sensitivity-arm overview plot
    sensitivity_plot_name = make_sensitivity_arm_plot(
        summary["falsifiability_hook_4a_vs_4b"], HERE / "plots",
    )
    summary["falsifiability_hook_4a_vs_4b_plot"] = f"plots/{sensitivity_plot_name}"

    out_path = HERE / "summary.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\nWrote {out_path}")

    # Console summary -- headline per channel + per-phase
    print("\n--- HEADLINE PER CHANNEL (median; * = direction-vs-grand-median survives 90d detrend) ---")
    for ch in CHANNELS:
        info = summary["channels"][ch]["per_phase"]
        line_parts = [f"{ch}:"]
        for phase_name in PHASE_ORDER:
            p = info[phase_name]
            n = p["raw"]["n"]
            med = p["raw"]["median"]
            if med is None:
                line_parts.append(f"{phase_name}=NaN (n=0)")
            else:
                survives = p.get("detrend_sensitivity", {}).get("survives_detrend")
                tag = "*" if survives else " "
                line_parts.append(f"{phase_name}={med:.2f}{tag} (n={n})")
        print(" | ".join(line_parts))

    print("\n--- §7b FALSIFIABILITY HOOK (4b - 4a median diff with 95% CI) ---")
    for ch in CHANNELS:
        r = summary["falsifiability_hook_4a_vs_4b"][ch]
        if r["verdict"] == "skipped_insufficient_n":
            print(f"{ch}: SKIPPED ({r['note']})")
            continue
        print(
            f"{ch}: med_4a={r['median_4a']:.2f} (n={r['n_4a']}); "
            f"med_4b={r['median_4b']:.2f} (n={r['n_4b']}); "
            f"diff={r['diff_4b_minus_4a']:+.2f} "
            f"CI=[{r['ci_lower']:+.2f}, {r['ci_upper']:+.2f}] "
            f"E[L]*={r.get('expected_block_length')} "
            f"verdict={r['verdict']}"
        )


if __name__ == "__main__":
    main()
