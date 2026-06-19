"""Descriptive analysis: trajectory/recovery_arc -- three-phase multi-year shape.

Strand B; implements the locked operationalisation in recovery_arc/README.md
(LOCKED 2026-06-18 per the descriptive/README §7b interview discipline). All
operationalisation choices are pre-locked in the README -- NO on-the-fly
choices in this script.

Layer 1 descriptive per CONVENTIONS §2.1: NO causal claims, NO SUPPORTED bar.

Output:
- summary.json -- machine-readable per-channel × per-phase statistics
- plots/<channel>.png -- per-channel multi-year trajectory PNGs with event
  overlays + phase-region shading

Discipline guards:
- §2.1 descriptive-before-inference: report what the data shows; no causal mark
- §3.6 named counts: every count carries scheme + unit + source-file
- §3.7 trajectory-detrend sensitivity: rolling 90d detrend -> recompute
  per-channel × per-phase median; flag "survives detrend?" per cell
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

PHASE_BOUNDARIES = [
    ("pre_illness_healthy",   date(2021, 8, 16), date(2022, 3, 20)),
    ("acute_infection",       date(2022, 3, 21), date(2022, 4,  3)),
    ("lc_pre_gevoelscore",    date(2022, 4,  4), date(2022, 9,  2)),
    ("lc_with_gevoelscore",   date(2022, 9,  3), date(2026, 6,  4)),
]

CHANNELS = [
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
    "bb_overnight_gain",
    "resting_hr",
    "gevoelscore",
    "stress_low_motion_min_count_S60_Mlow",
]

# 8 documented events; post-afbouw start (2026-06-05) OUT OF SCOPE per
# locked operationalisation -- corpus ends 2026-06-04, no post-afbouw data.
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

SEED = 20260618
ROLLING_TREND_WINDOW = 90  # CONVENTIONS §3.7 procedure window
ROLLING_VIZ_WINDOW = 30     # multi-year trajectory smoothing window for plots


# ---------------------------------------------------------------------------
# Per-channel × per-phase descriptive computations
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


def bootstrap_median_ci(values: np.ndarray, *, block_length: int = 7,
                       n_bootstrap: int = 5000, seed: int = SEED) -> dict:
    """Stationary-bootstrap 95% CI on the median.

    Drops NaN before resampling; preserves block-level autocorrelation.
    """
    v = values[~np.isnan(values)]
    if len(v) < 10:
        return {
            "ci_lower": None,
            "ci_upper": None,
            "n_used": int(len(v)),
            "expected_block_length": block_length,
            "note": "n<10; skipped",
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
    }


def per_phase_stats(df: pd.DataFrame, channel: str) -> dict:
    """Per-phase median + IQR + bootstrap CI95 at E[L]=7 and E[L]*.

    Per CONVENTIONS §3.7, also computes the detrended median (using a
    rolling 90d trend computed on the FULL corpus for the channel,
    then subtracted day-wise within the phase window).
    """
    # Pre-compute the rolling 90d trend on the full corpus for this channel
    full = df[["date", channel]].sort_values("date").reset_index(drop=True)
    rolled = full[channel].rolling(ROLLING_TREND_WINDOW, min_periods=30).median()
    detrended = full[channel] - rolled

    out: dict = {}
    for phase_name, start, end in PHASE_BOUNDARIES:
        mask = (full["date"] >= pd.Timestamp(start)) & (full["date"] <= pd.Timestamp(end))
        raw_vals = full.loc[mask, channel].to_numpy(dtype=float)
        det_vals = detrended.loc[mask].to_numpy(dtype=float)

        raw_stats = median_iqr(raw_vals)
        det_stats = median_iqr(det_vals)

        # Data-driven block length on raw phase data (single estimate per cell)
        if raw_stats["n"] >= 30:
            block_info = compute_data_driven_block_length(
                raw_vals, default_block_length=7,
            )
            e_l_star = float(block_info["optimal_block_length"])
            flagged = bool(block_info["flagged_deviation"])
            cutoff_M = block_info["cutoff_lag"]
        else:
            e_l_star = None
            flagged = False
            cutoff_M = None

        # Bootstrap CI on the median at E[L]=7 (project default)
        if raw_stats["n"] >= 10:
            ci7 = bootstrap_median_ci(raw_vals, block_length=7)
            ci_star = bootstrap_median_ci(
                raw_vals,
                block_length=max(1, int(round(e_l_star))) if e_l_star else 7,
            )
        else:
            ci7 = {"ci_lower": None, "ci_upper": None, "n_used": raw_stats["n"], "expected_block_length": 7, "note": "n<10; skipped"}
            ci_star = ci7

        out[phase_name] = {
            "date_start": str(start),
            "date_end": str(end),
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
        }
    return out


def detrend_survives_flag(per_phase: dict) -> dict:
    """For each phase, did the median's ordering vs the grand corpus
    median survive a rolling-90d detrend?

    Reports a per-phase boolean: sign(raw_median - raw_grand) ==
    sign(detrended_median - detrended_grand). True = the phase's
    direction-vs-corpus survives detrend.
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
# Plot generation
# ---------------------------------------------------------------------------


PHASE_COLOURS = {
    "pre_illness_healthy":  "#cde7c0",  # soft green
    "acute_infection":      "#f7c0a3",  # warm coral
    "lc_pre_gevoelscore":   "#fde7a5",  # pale gold
    "lc_with_gevoelscore":  "#cfd9eb",  # cool grey-blue
}


def make_plot(df: pd.DataFrame, channel: str, out_dir: Path) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    out_dir.mkdir(parents=True, exist_ok=True)
    sub = df[["date", channel]].sort_values("date").reset_index(drop=True)
    sub["roll30"] = sub[channel].rolling(ROLLING_VIZ_WINDOW, min_periods=10).median()
    # IQR band from rolling 30d quantiles
    sub["roll30_p25"] = sub[channel].rolling(ROLLING_VIZ_WINDOW, min_periods=10).quantile(0.25)
    sub["roll30_p75"] = sub[channel].rolling(ROLLING_VIZ_WINDOW, min_periods=10).quantile(0.75)

    fig, ax = plt.subplots(figsize=(13, 4.6))

    # Phase shading
    for phase_name, start, end in PHASE_BOUNDARIES:
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

    ax.set_xlim(pd.Timestamp(date(2021, 8, 1)), pd.Timestamp(date(2026, 6, 4)))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_minor_locator(mdates.MonthLocator((1, 4, 7, 10)))
    ax.set_ylabel(channel)
    n_total = int(sub[channel].notna().sum())
    ax.set_title(
        f"{channel} -- multi-year trajectory (n={n_total} non-NaN days, "
        f"per_day_master.csv as_of={AS_OF_DATE})",
        fontsize=10,
    )

    # Dedup legend
    h, l = ax.get_legend_handles_labels()
    seen = set()
    pairs = [(hi, li) for hi, li in zip(h, l) if not (li in seen or seen.add(li))]
    ax.legend(
        [p[0] for p in pairs], [p[1] for p in pairs],
        loc="upper right", fontsize=7, ncol=2, framealpha=0.85,
    )

    fig.tight_layout()
    fp = out_dir / f"{channel}.png"
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

    summary: dict = {
        "analysis": "trajectory/recovery_arc",
        "strand": "B (multi-year trajectory, locked operationalisation interview 2026-06-18)",
        "as_of_date": AS_OF_DATE,
        "source_file_master": "per_day_master.csv",
        "n_rows_total": int(len(df)),
        "phase_boundaries": [
            {"phase": name, "start": str(s), "end": str(e)}
            for name, s, e in PHASE_BOUNDARIES
        ],
        "event_overlays": [
            {"label": label, "date": str(d)} for label, d in EVENT_OVERLAYS
        ],
        "post_afbouw_out_of_scope_note": (
            "Citalopram afbouw -> post_afbouw boundary is 2026-06-05 per "
            "citalopram_phase_stratification.md §3; corpus ends 2026-06-04. "
            "Out of scope for this analysis: no post-afbouw data exists. "
            "The afbouw segment runs 2026-03-20 -> 2026-06-04 (~76 days)."
        ),
        "boundary_collision_caveat": (
            "Citalopram buildup start (2024-04-09) and CPAP end (2024-04-16) "
            "sit 7 days apart; their independent contributions are confounded "
            "in any pre-vs-post reading on either boundary. Per "
            "intervention_effects_descriptive.md §2b + §8.1, both boundaries "
            "are structurally unanalyzable in pre-vs-post window comparisons; "
            "this analysis reports the rolling-median trajectory across the "
            "cluster but does NOT attribute step-changes to either event."
        ),
        "channels": {},
    }

    for ch in CHANNELS:
        print(f"computing channel: {ch}")
        per_phase = per_phase_stats(df, ch)
        detrend_flags = detrend_survives_flag(per_phase)
        # Annotate per-phase entries with the detrend-survives flag
        for phase_name, info in detrend_flags.items():
            per_phase[phase_name]["detrend_sensitivity"] = info

        # Coverage caveats (per locked operationalisation §2.2 of README)
        coverage = {}
        for phase_name, _, _ in PHASE_BOUNDARIES:
            n = per_phase[phase_name]["raw"]["n"]
            coverage[phase_name] = n
        cov_caveats = []
        if ch == "bb_overnight_gain":
            cov_caveats.append(
                "Per intervention_effects_descriptive.md §2b: data only from "
                "2024-09-18 onward (Garmin firmware UDS rollout). All phases "
                "before 2024-09-18 return n=0 or partial coverage; only the "
                "tail of lc_with_gevoelscore has full coverage."
            )
        if ch == "gevoelscore":
            cov_caveats.append(
                "Per lc_era_temporal_segmentation.md §1: gevoelscore corpus "
                "starts 2022-09-03 (Stratum 4 left edge). Pre-illness, acute, "
                "and lc_pre_gevoelscore phases have NO gevoelscore data by "
                "construction."
            )

        summary["channels"][ch] = {
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

        plot_name = make_plot(df, ch, HERE / "plots")
        summary["channels"][ch]["plot_file"] = f"plots/{plot_name}"

    out_path = HERE / "summary.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\nWrote {out_path}")

    # Console summary -- headline per channel
    print("\n--- HEADLINE PER CHANNEL ---")
    for ch in CHANNELS:
        info = summary["channels"][ch]["per_phase"]
        line_parts = [f"{ch}:"]
        for phase_name, _, _ in PHASE_BOUNDARIES:
            p = info[phase_name]
            n = p["raw"]["n"]
            med = p["raw"]["median"]
            if med is None:
                line_parts.append(f"{phase_name}=NaN (n=0)")
            else:
                survives = p.get("detrend_sensitivity", {}).get("survives_detrend")
                tag = "*" if survives else " "
                line_parts.append(f"{phase_name}={med:.2f}{tag} (n={n})")
        print(" ".join(line_parts))
    print("(* = direction-vs-grand-median survives 90d detrend per CONVENTIONS §3.7)")


if __name__ == "__main__":
    main()
