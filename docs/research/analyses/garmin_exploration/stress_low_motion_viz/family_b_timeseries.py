"""Family B — multi-year time-series plots of the stress_low_motion primitive.

B1 — primary column per day, 7d rolling median, with anchor lines + crash strip
B2 — primary column split by Citalopram phase (4 post-LC phases) with median+IQR
B3 — all 9 stress_low_motion cells overlaid (sensitivity to thresholds)
B4a — primary vs stress_high_duration_min (HA11-substitute sibling)
B4b — primary vs stress_mean_sleep (dose-confirmed channel sibling)
B5 — respiration companions over time
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from _master_loader import (
    ALL_NINE, LC_ONSET, CPAP_START, CPAP_END, PHASE_BOUNDARIES,
    PHASES_POST_BUILDUP, PLOTS_DIR, PRIMARY, RESP_ABOVE_18, RESP_REST_BAND,
    add_phase, lc_era, load_master, phase_color,
)
from _plot_utils import savefig, stamp_footer


ROLL_WINDOW = 7   # per interview answer


def _rolling_median(series: pd.Series, window: int = ROLL_WINDOW) -> pd.Series:
    return series.rolling(window, min_periods=max(2, window // 3)).median()


def _add_anchor_lines(ax) -> None:
    anchors = [
        (LC_ONSET, "LC onset",          "#5a4d42", "-"),
        (CPAP_START, "CPAP start",      "#3f6b6e", "--"),
        (CPAP_END,   "CPAP end",        "#3f6b6e", "--"),
        (pd.Timestamp("2024-04-09"), "buildup start",       "#c89770", ":"),
        (PHASE_BOUNDARIES["buildup_end"], "consolidation start", "#3f6b6e", ":"),
        (PHASE_BOUNDARIES["consolidation_end"], "afbouw start",  "#b04a32", ":"),
    ]
    ymin, ymax = ax.get_ylim()
    for dt, label, color, style in anchors:
        ax.axvline(dt, color=color, linestyle=style, linewidth=0.7, alpha=0.7)
        ax.text(dt, ymax * 0.98, label,
                rotation=90, ha="right", va="top",
                fontsize=7, color=color, alpha=0.85)
    ax.set_ylim(ymin, ymax)


def _add_crash_strip(ax, df: pd.DataFrame) -> None:
    """Add red dots below the x-axis for crash days."""
    crashes = df[df["is_crash"] == True]
    if crashes.empty:
        return
    ymin = ax.get_ylim()[0]
    ax.scatter(crashes["date"], [ymin - (ax.get_ylim()[1] - ymin) * 0.04] * len(crashes),
               s=8, color="#b04a32", clip_on=False, zorder=5,
               label=f"crash ({len(crashes)} days)")


def b1_primary_over_time(df: pd.DataFrame) -> None:
    """B1 — primary column per day + 7d rolling median + anchors + crash strip."""
    fig, ax = plt.subplots(figsize=(14, 5))
    s = df.set_index("date")[PRIMARY]
    ax.scatter(s.index, s.values, s=3, color="#3f6b6e", alpha=0.3,
               label="per day")
    ax.plot(s.index, _rolling_median(s), color="#b04a32", linewidth=1.4,
            label=f"{ROLL_WINDOW}d rolling median")

    ax.set_title(f"B1 — {PRIMARY} per day (2021-08 → 2026-06)")
    ax.set_ylabel("minutes / day")
    ax.set_xlabel("")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
    _add_anchor_lines(ax)
    _add_crash_strip(ax, df)
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / "B1_primary_over_time.png")


def b2_primary_by_phase(df: pd.DataFrame) -> None:
    """B2 — primary column rolling median per Citalopram phase + IQR band.
    4 post-LC phases (per interview: skip pre-citalopram pre-LC era; we still
    include pre_cit since that is the LC-era-but-unmedicated phase)."""
    df_lc = lc_era(df)
    df_lc = add_phase(df_lc)

    fig, ax = plt.subplots(figsize=(14, 5))
    for phase_name, _, _, color in PHASES_POST_BUILDUP[:0] or [("pre_cit", None, None, "#8a7b6e")]:
        pass  # placeholder so linter sees the structure; real loop below

    # plot the raw rolling median per phase across the whole timeline
    for name, start, end, color in [
        ("pre_cit", LC_ONSET, PHASE_BOUNDARIES["unmedicated_end"], "#8a7b6e"),
        ("buildup", pd.Timestamp("2024-04-09"), PHASE_BOUNDARIES["buildup_end"], "#c89770"),
        ("consolidation", pd.Timestamp("2024-06-20"), PHASE_BOUNDARIES["consolidation_end"], "#3f6b6e"),
        ("afbouw", pd.Timestamp("2026-03-20"), pd.Timestamp("2026-06-05"), "#b04a32"),
    ]:
        sub = df_lc[(df_lc["date"] >= start) & (df_lc["date"] <= end)].copy()
        if sub.empty:
            continue
        sub = sub.set_index("date").sort_index()
        med = _rolling_median(sub[PRIMARY])
        q1 = sub[PRIMARY].rolling(ROLL_WINDOW, min_periods=2).quantile(0.25)
        q3 = sub[PRIMARY].rolling(ROLL_WINDOW, min_periods=2).quantile(0.75)
        ax.fill_between(med.index, q1, q3, color=color, alpha=0.18)
        ax.plot(med.index, med, color=color, linewidth=1.6, label=name)

    ax.set_title(f"B2 — primary by Citalopram phase, {ROLL_WINDOW}d rolling median + IQR band")
    ax.set_ylabel("minutes / day")
    ax.set_xlabel("")
    ax.legend(loc="upper left", fontsize=8)
    _add_anchor_lines(ax)
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / "B2_primary_by_phase.png")


def b3_all_nine_cells(df: pd.DataFrame) -> None:
    """B3 — all 9 stress_low_motion cells, 7d rolling median, sensitivity ladder."""
    df = df.set_index("date").sort_index()
    fig, ax = plt.subplots(figsize=(14, 5.5))

    # color: stress threshold -> hue; motion class -> saturation
    palette = {
        50: "#a7b6a5", 60: "#3f6b6e", 75: "#b04a32",
    }
    styles = {
        "strict": "-", "low": "--", "below_mod": ":",
    }
    for col in ALL_NINE:
        # parse threshold + motion from name: stress_low_motion_min_count_S60_Mlow
        parts = col.replace("stress_low_motion_min_count_", "").split("_M")
        thresh = int(parts[0][1:])
        motion = parts[1]
        roll = _rolling_median(df[col])
        ax.plot(roll.index, roll, color=palette[thresh],
                linestyle=styles[motion], linewidth=1.0, alpha=0.85,
                label=f"S{thresh}/M{motion}")

    ax.set_title(f"B3 — all 9 stress_low_motion cells, {ROLL_WINDOW}d rolling median (sensitivity ladder)")
    ax.set_ylabel("minutes / day")
    ax.legend(loc="upper left", fontsize=7, ncol=3, framealpha=0.9)
    _add_anchor_lines(ax)
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / "B3_all_nine_cells.png")


def _b4_twin(df: pd.DataFrame, sibling_col: str, sibling_label: str,
             out_path: str, title: str) -> None:
    if sibling_col not in df.columns:
        print(f"  skipping {out_path}: column {sibling_col} missing")
        return
    df = df.set_index("date").sort_index()
    fig, ax1 = plt.subplots(figsize=(14, 5))
    ax2 = ax1.twinx()

    p_roll = _rolling_median(df[PRIMARY])
    s_roll = _rolling_median(df[sibling_col])
    l1, = ax1.plot(p_roll.index, p_roll, color="#3f6b6e", linewidth=1.4,
                   label=f"{PRIMARY} ({ROLL_WINDOW}d)")
    l2, = ax2.plot(s_roll.index, s_roll, color="#b04a32", linewidth=1.4,
                   alpha=0.9, label=f"{sibling_label} ({ROLL_WINDOW}d)")

    ax1.set_ylabel("primary — minutes / day", color="#3f6b6e")
    ax2.set_ylabel(sibling_label, color="#b04a32")
    ax1.tick_params(axis="y", colors="#3f6b6e")
    ax2.tick_params(axis="y", colors="#b04a32")
    ax2.grid(False)

    # twin axis breaks anchor-line ymax read; use ax1 for anchors
    _add_anchor_lines(ax1)
    ax1.set_title(title)
    ax1.legend(handles=[l1, l2], loc="upper left", fontsize=8)
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / out_path)


def b4_primary_vs_siblings(df: pd.DataFrame) -> None:
    _b4_twin(df, "stress_high_duration_min", "stress_high_duration_min",
             "B4a_primary_vs_stress_high_duration.png",
             "B4a — primary vs stress_high_duration_min (HA11-substitute sibling)")
    _b4_twin(df, "stress_mean_sleep", "stress_mean_sleep",
             "B4b_primary_vs_stress_mean_sleep.png",
             "B4b — primary vs stress_mean_sleep (dose-confirmed channel)")
    _b4_twin(df, "u_dip_count", "u_dip_count",
             "B4c_primary_vs_u_dip_count.png",
             "B4c — primary vs u_dip_count (HA11 canonical sibling, MD reports rho=0.556)")


def b5_respiration_companions(df: pd.DataFrame) -> None:
    df = df.set_index("date").sort_index()
    fig, ax = plt.subplots(figsize=(14, 5))

    above = _rolling_median(df[RESP_ABOVE_18])
    rest  = _rolling_median(df[RESP_REST_BAND])
    ax.plot(above.index, above, color="#c89770", linewidth=1.4,
            label=f"{RESP_ABOVE_18} ({ROLL_WINDOW}d)")
    ax.plot(rest.index, rest, color="#3f6b6e", linewidth=1.4,
            label=f"{RESP_REST_BAND} ({ROLL_WINDOW}d)")

    ax.set_title("B5 — respiration companion columns over time")
    ax.set_ylabel("minutes / day")
    ax.legend(loc="upper left", fontsize=8)
    _add_anchor_lines(ax)
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / "B5_respiration_companions.png")


def main(df: pd.DataFrame | None = None) -> None:
    df = df if df is not None else load_master()
    print("Family B - time series")
    b1_primary_over_time(df)
    b2_primary_by_phase(df)
    b3_all_nine_cells(df)
    b4_primary_vs_siblings(df)
    b5_respiration_companions(df)


if __name__ == "__main__":
    main()
