"""Synthesis plots for trajectory/recovery_arc -- cross-channel headline views.

Reads summary.json (produced by run.py under the locked operationalisation in
README.md) and writes four cross-channel visualisations into plots/:

  plots/_synthesis_phase_medians_grid.png   -- per-channel CI95 grid by family
  plots/_synthesis_shift_from_healthy.png   -- normalised %-shift from healthy
  plots/_synthesis_detrend_survival.png     -- per-cell detrend-survives flag
  plots/_synthesis_block_length_grid.png    -- per-cell E[L]* + factor-of-2 flag

NOT under the locked operationalisation -- this is an auxiliary visualisation
layer over the already-computed summary.json. It changes no numbers.

Run with: python synthesis_plots.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
SUMMARY_PATH = HERE / "summary.json"
PLOTS_DIR = HERE / "plots"

PHASES = [
    "pre_illness_healthy",
    "acute_infection",
    "lc_pre_gevoelscore",
    "lc_with_gevoelscore",
]
PHASE_SHORT = {
    "pre_illness_healthy":  "healthy",
    "acute_infection":      "acute",
    "lc_pre_gevoelscore":   "LC-pre-gs",
    "lc_with_gevoelscore":  "Stratum 4",
}

FAMILIES = {
    "autonomic-load": [
        "stress_mean_sleep",
        "all_day_stress_avg",
        "stress_low_motion_min_count_S60_Mlow",
    ],
    "recovery": [
        "bb_lowest",
        "bb_overnight_gain",
    ],
    "cardiovascular": [
        "resting_hr",
    ],
    "felt-state": [
        "gevoelscore",
    ],
}
FAMILY_COLOURS = {
    "autonomic-load":  "#1f3a5f",   # deep blue (family base, used for grid borders)
    "recovery":        "#3a7d44",   # green
    "cardiovascular":  "#c46a3c",   # warm orange
    "felt-state":      "#7a4a8a",   # purple
}
# Per-channel hues used in the shift-from-healthy line plot only (so each line
# is visually distinct even within a family). Family base hue is preserved in
# the grid/heatmap plots where one cell per channel makes hue overload unnecessary.
CHANNEL_LINE_COLOURS = {
    "stress_mean_sleep":                    "#1f3a5f",   # autonomic-load: navy
    "all_day_stress_avg":                   "#3f6ea0",   # autonomic-load: mid-blue
    "stress_low_motion_min_count_S60_Mlow": "#7aaad6",   # autonomic-load: light blue
    "bb_lowest":                            "#3a7d44",   # recovery: green
    "bb_overnight_gain":                    "#7fb085",   # recovery: light green
    "resting_hr":                           "#c46a3c",   # cardiovascular: orange
    "gevoelscore":                          "#7a4a8a",   # felt-state: purple
}
PHASE_BG = {
    "pre_illness_healthy":  "#e8f4e2",
    "acute_infection":      "#fbe2d4",
    "lc_pre_gevoelscore":   "#fef3cf",
    "lc_with_gevoelscore":  "#e3eaf5",
}

CHANNEL_FAMILY = {ch: fam for fam, chs in FAMILIES.items() for ch in chs}
ALL_CHANNELS = [ch for chs in FAMILIES.values() for ch in chs]

CHANNEL_SHORT = {
    "stress_mean_sleep":                    "stress_mean_sleep",
    "all_day_stress_avg":                   "all_day_stress_avg",
    "stress_low_motion_min_count_S60_Mlow": "stress_low_motion_count",
    "bb_lowest":                            "bb_lowest",
    "bb_overnight_gain":                    "bb_overnight_gain",
    "resting_hr":                           "resting_hr",
    "gevoelscore":                          "gevoelscore",
}


def _load() -> dict:
    with SUMMARY_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _cell(summary: dict, channel: str, phase: str) -> dict:
    return summary["channels"][channel]["per_phase"][phase]


# ---------------------------------------------------------------------------
# Plot 1: per-channel CI95 grid by family
# ---------------------------------------------------------------------------


def plot_phase_medians_grid(summary: dict) -> Path:
    fig, axes = plt.subplots(2, 4, figsize=(15, 7.5))
    axes_flat = axes.flatten()

    for i, channel in enumerate(ALL_CHANNELS):
        ax = axes_flat[i]
        fam = CHANNEL_FAMILY[channel]
        fam_color = FAMILY_COLOURS[fam]

        medians, lowers, uppers, ns, x_positions = [], [], [], [], []
        for j, phase in enumerate(PHASES):
            cell = _cell(summary, channel, phase)
            med = cell["raw"]["median"]
            ci = cell["bootstrap_ci95_median_E_L7"]
            n = cell["raw"]["n"]
            ax.axvspan(j - 0.5, j + 0.5, color=PHASE_BG[phase], alpha=0.55, zorder=0)
            if med is None:
                ax.text(j, 0.5, "no data", ha="center", va="center",
                        transform=ax.get_xaxis_transform(),
                        fontsize=7, color="#888", style="italic")
                continue
            lo = ci.get("ci_lower")
            hi = ci.get("ci_upper")
            medians.append(med)
            lowers.append(med - lo if lo is not None else 0.0)
            uppers.append(hi - med if hi is not None else 0.0)
            ns.append(n)
            x_positions.append(j)

        if medians:
            ax.errorbar(
                x_positions, medians,
                yerr=[lowers, uppers],
                fmt="o", color=fam_color, ecolor=fam_color,
                elinewidth=1.4, capsize=4, markersize=6, zorder=3,
            )
            for x, m, n in zip(x_positions, medians, ns):
                ax.annotate(
                    f"n={n}", (x, m),
                    textcoords="offset points", xytext=(7, 0),
                    fontsize=6.5, color="#444", va="center",
                )

        ax.set_xticks(range(len(PHASES)))
        ax.set_xticklabels([PHASE_SHORT[p] for p in PHASES], fontsize=7.5, rotation=20)
        ax.set_xlim(-0.5, len(PHASES) - 0.5)
        ax.set_title(f"{CHANNEL_SHORT[channel]}  ({fam})",
                     fontsize=9, color=fam_color, fontweight="bold")
        ax.tick_params(axis="y", labelsize=7.5)
        ax.grid(axis="y", linewidth=0.4, alpha=0.4)
        for spine in ax.spines.values():
            spine.set_color(fam_color)
            spine.set_linewidth(1.2)

    # Hide unused subplot (8th cell)
    for k in range(len(ALL_CHANNELS), len(axes_flat)):
        axes_flat[k].axis("off")

    fig.suptitle(
        "Per-channel x per-phase median + CI95 (bootstrap E[L]=7) -- grouped by family\n"
        f"recovery_arc, per_day_master.csv as_of={summary['as_of_date']}",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out = PLOTS_DIR / "_synthesis_phase_medians_grid.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Plot 2: normalised shift from healthy
# ---------------------------------------------------------------------------


def plot_shift_from_healthy(summary: dict) -> Path:
    # Only channels with a healthy-phase median can be plotted relative to healthy.
    fig, ax = plt.subplots(figsize=(10.5, 5.5))

    for phase, _ in zip(PHASES, range(len(PHASES))):
        pass  # spacing only

    plotted = []
    for channel in ALL_CHANNELS:
        healthy = _cell(summary, channel, "pre_illness_healthy")["raw"]["median"]
        if healthy is None:
            continue  # gevoelscore + bb_overnight_gain skipped (no healthy reference)
        ys = []
        for phase in PHASES:
            med = _cell(summary, channel, phase)["raw"]["median"]
            if med is None:
                ys.append(np.nan)
                continue
            pct = 100.0 * (med - healthy) / abs(healthy)
            ys.append(pct)
        fam = CHANNEL_FAMILY[channel]
        ax.plot(
            range(len(PHASES)), ys,
            marker="o", color=CHANNEL_LINE_COLOURS[channel],
            linewidth=2.0, markersize=7, alpha=0.95,
            label=f"{CHANNEL_SHORT[channel]} ({fam})",
        )
        plotted.append(channel)

    ax.axhline(0.0, color="#444", linewidth=1.0, linestyle="--", alpha=0.7)
    ax.text(-0.35, 1.5, "healthy baseline = 0%", fontsize=8, color="#444",
            style="italic")

    for j, phase in enumerate(PHASES):
        ax.axvspan(j - 0.5, j + 0.5, color=PHASE_BG[phase], alpha=0.45, zorder=0)

    ax.set_xticks(range(len(PHASES)))
    ax.set_xticklabels([PHASE_SHORT[p] for p in PHASES], fontsize=9)
    ax.set_xlim(-0.5, len(PHASES) - 0.5)
    ax.set_ylabel("% shift in phase median vs healthy baseline", fontsize=9)
    ax.set_title(
        "Phase-shape comparison: shift from healthy baseline per channel\n"
        "(gevoelscore + bb_overnight_gain excluded -- no healthy-phase data)",
        fontsize=10,
    )
    ax.grid(axis="y", linewidth=0.4, alpha=0.4)
    ax.legend(loc="upper right", fontsize=8, framealpha=0.92)
    fig.tight_layout()
    out = PLOTS_DIR / "_synthesis_shift_from_healthy.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Plot 3: detrend-survival heatmap
# ---------------------------------------------------------------------------


def plot_detrend_survival(summary: dict) -> Path:
    n_ch = len(ALL_CHANNELS)
    n_ph = len(PHASES)

    fig, ax = plt.subplots(figsize=(8.5, 5.5))

    cell_colour = {
        "yes":   "#4f8a4d",
        "no":    "#b8434e",
        "na":    "#cccccc",
    }
    cell_text_colour = {"yes": "white", "no": "white", "na": "#666"}

    for i, channel in enumerate(ALL_CHANNELS):
        for j, phase in enumerate(PHASES):
            cell = _cell(summary, channel, phase)
            n = cell["raw"]["n"]
            if n == 0:
                state = "na"
                label = "no data"
            else:
                survives = cell.get("detrend_sensitivity", {}).get("survives_detrend")
                if survives is True:
                    state = "yes"
                    label = "yes"
                elif survives is False:
                    state = "no"
                    label = "no"
                else:
                    state = "na"
                    label = "n/a"
            ax.add_patch(plt.Rectangle(
                (j, n_ch - 1 - i), 1, 1,
                facecolor=cell_colour[state], edgecolor="white", linewidth=1.5,
            ))
            ax.text(
                j + 0.5, n_ch - 1 - i + 0.5, label,
                ha="center", va="center",
                fontsize=9, color=cell_text_colour[state], fontweight="bold",
            )

    ax.set_xlim(0, n_ph)
    ax.set_ylim(0, n_ch)
    ax.set_xticks([j + 0.5 for j in range(n_ph)])
    ax.set_xticklabels([PHASE_SHORT[p] for p in PHASES], fontsize=9)
    ax.set_yticks([n_ch - 1 - i + 0.5 for i in range(n_ch)])
    ax.set_yticklabels(
        [f"{CHANNEL_SHORT[ch]}  ({CHANNEL_FAMILY[ch]})" for ch in ALL_CHANNELS],
        fontsize=8,
    )
    ax.tick_params(axis="both", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(
        "Detrend survival per cell (CONVENTIONS §3.7)\n"
        "green = direction-vs-grand-median survives 90d rolling-median detrend",
        fontsize=10,
    )
    fig.tight_layout()
    out = PLOTS_DIR / "_synthesis_detrend_survival.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Plot 4: block-length E[L]* grid with factor-of-2 flags
# ---------------------------------------------------------------------------


def plot_block_length_grid(summary: dict) -> Path:
    n_ch = len(ALL_CHANNELS)
    n_ph = len(PHASES)

    fig, ax = plt.subplots(figsize=(8.5, 5.5))

    for i, channel in enumerate(ALL_CHANNELS):
        for j, phase in enumerate(PHASES):
            cell = _cell(summary, channel, phase)
            n = cell["raw"]["n"]
            e_l_star = cell.get("data_driven_E_L_star")
            flagged = cell.get("factor_of_2_deviation_flag", False)

            if n == 0:
                facecolour = "#cccccc"
                label = "no data"
                text_colour = "#666"
            elif e_l_star is None:
                facecolour = "#dddddd"
                label = f"n<30\n(n={n})"
                text_colour = "#444"
            elif flagged:
                facecolour = "#c46a3c"  # warm orange = flagged
                label = f"E[L]*={e_l_star:.1f}\n⚐"
                text_colour = "white"
            else:
                facecolour = "#a8c9a3"  # soft green = within range
                label = f"E[L]*={e_l_star:.1f}"
                text_colour = "#1f3a1f"

            ax.add_patch(plt.Rectangle(
                (j, n_ch - 1 - i), 1, 1,
                facecolor=facecolour, edgecolor="white", linewidth=1.5,
            ))
            ax.text(
                j + 0.5, n_ch - 1 - i + 0.5, label,
                ha="center", va="center",
                fontsize=8.5, color=text_colour, fontweight="bold",
            )

    ax.set_xlim(0, n_ph)
    ax.set_ylim(0, n_ch)
    ax.set_xticks([j + 0.5 for j in range(n_ph)])
    ax.set_xticklabels([PHASE_SHORT[p] for p in PHASES], fontsize=9)
    ax.set_yticks([n_ch - 1 - i + 0.5 for i in range(n_ch)])
    ax.set_yticklabels(
        [f"{CHANNEL_SHORT[ch]}  ({CHANNEL_FAMILY[ch]})" for ch in ALL_CHANNELS],
        fontsize=8,
    )
    ax.tick_params(axis="both", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(
        "Data-driven block length E[L]* per cell -- factor-of-2 deviation flag (⚐)\n"
        "warm orange = E[L]* deviates >2x from project default 7 (long memory within phase)",
        fontsize=10,
    )
    fig.tight_layout()
    out = PLOTS_DIR / "_synthesis_block_length_grid.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def main() -> None:
    summary = _load()
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    outs = [
        plot_phase_medians_grid(summary),
        plot_shift_from_healthy(summary),
        plot_detrend_survival(summary),
        plot_block_length_grid(summary),
    ]
    for p in outs:
        print(f"wrote {p}")


if __name__ == "__main__":
    main()
