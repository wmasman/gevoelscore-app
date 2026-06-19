"""Family C — event-aligned crash windows.

Per interview: crash_v2 (is_crash column), 4-day pre-window aligned with P2.

C1 — Pre-crash window. For all LC-era crash days, primary on days t-4..t_crash.
     Show median + IQR + faint individual lines.
C2 — Post-crash window. Days t_crash..t+5. Recovery shape.
C3 — C1 + C2 stratified by Citalopram phase.
C4 — Scatter: recent-14-day crash count (P7 proxy) vs primary, per phase.
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from _master_loader import (
    LC_ONSET, PHASES_FULL, PLOTS_DIR, PRIMARY,
    add_phase, lc_era, load_master,
)
from _plot_utils import savefig, stamp_footer


PRE_WINDOW = 4   # per interview answer
POST_WINDOW = 5  # default
PHASE_LIST = [(n, c) for n, _, _, c in PHASES_FULL]


def _crash_days(df: pd.DataFrame) -> pd.Series:
    return df[df["is_crash"] == True]["date"]


def _window_matrix(df: pd.DataFrame, crash_dates: pd.Series,
                   pre: int, post: int) -> tuple[np.ndarray, np.ndarray]:
    """Return (offsets, matrix[crash, offset]) where matrix[i, j] is the primary
    value on day (crash_i + offsets[j]) — NaN if missing."""
    df_idx = df.set_index("date")[PRIMARY]
    offsets = np.arange(-pre, post + 1)
    mat = np.full((len(crash_dates), len(offsets)), np.nan)
    for i, t0 in enumerate(crash_dates.tolist()):
        for j, off in enumerate(offsets):
            d = t0 + pd.Timedelta(days=int(off))
            if d in df_idx.index:
                mat[i, j] = df_idx.loc[d]
    return offsets, mat


def _plot_band(ax, offsets, mat, color, label) -> None:
    med = np.nanmedian(mat, axis=0)
    q1  = np.nanquantile(mat, 0.25, axis=0)
    q3  = np.nanquantile(mat, 0.75, axis=0)
    ax.fill_between(offsets, q1, q3, color=color, alpha=0.2)
    ax.plot(offsets, med, color=color, linewidth=2.0, marker="o",
            markersize=4, label=label)


def c1_pre_crash(df: pd.DataFrame) -> None:
    df_lc = lc_era(df)
    crashes = _crash_days(df_lc)
    if crashes.empty:
        print("  skipping C1: no crashes")
        return
    offsets, mat = _window_matrix(df_lc, crashes, PRE_WINDOW, 0)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    # faint individual day lines
    for row in mat:
        ax.plot(offsets, row, color="#8a7b6e", linewidth=0.4, alpha=0.18)
    _plot_band(ax, offsets, mat, "#b04a32",
               f"crash days median + IQR (n={len(crashes)})")

    # matched non-crash baseline: random sample of non-crash days
    non_crash = df_lc[df_lc["is_crash"] == False]
    if not non_crash.empty:
        sample_size = min(len(crashes) * 3, len(non_crash))
        sample = non_crash.sample(n=sample_size, random_state=42)
        _, base_mat = _window_matrix(df_lc, sample["date"], PRE_WINDOW, 0)
        med = np.nanmedian(base_mat, axis=0)
        ax.plot(offsets, med, color="#3f6b6e", linewidth=1.4, linestyle="--",
                label=f"non-crash baseline median (n={len(sample)})")

    ax.axvline(0, color="#5a4d42", linestyle=":", linewidth=0.7)
    ax.text(0, ax.get_ylim()[1] * 0.95, "  crash day", fontsize=8, color="#5a4d42")
    ax.set_title(f"C1 — Pre-crash {PRE_WINDOW}-day window (primary, LC era)")
    ax.set_xlabel("days relative to crash")
    ax.set_ylabel(PRIMARY)
    ax.legend(fontsize=8)
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / "C1_pre_crash_window.png")


def c2_post_crash(df: pd.DataFrame) -> None:
    df_lc = lc_era(df)
    crashes = _crash_days(df_lc)
    if crashes.empty:
        return
    offsets, mat = _window_matrix(df_lc, crashes, 0, POST_WINDOW)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    for row in mat:
        ax.plot(offsets, row, color="#8a7b6e", linewidth=0.4, alpha=0.18)
    _plot_band(ax, offsets, mat, "#b04a32",
               f"crash days median + IQR (n={len(crashes)})")
    ax.axvline(0, color="#5a4d42", linestyle=":", linewidth=0.7)
    ax.text(0, ax.get_ylim()[1] * 0.95, "  crash day", fontsize=8, color="#5a4d42")
    ax.set_title(f"C2 — Post-crash {POST_WINDOW}-day window (primary, LC era)")
    ax.set_xlabel("days relative to crash")
    ax.set_ylabel(PRIMARY)
    ax.legend(fontsize=8)
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / "C2_post_crash_window.png")


def c3_by_phase(df: pd.DataFrame) -> None:
    df_lc = add_phase(lc_era(df))
    crashes = df_lc[df_lc["is_crash"] == True]
    if crashes.empty:
        return

    fig, axes = plt.subplots(1, len(PHASE_LIST), figsize=(4 * len(PHASE_LIST), 5), sharey=True)
    if len(PHASE_LIST) == 1:
        axes = [axes]
    for ax, (name, color) in zip(axes, PHASE_LIST):
        ph_crashes = crashes[crashes["phase"] == name]["date"]
        if ph_crashes.empty:
            ax.text(0.5, 0.5, f"{name}\nno crashes",
                    ha="center", va="center", transform=ax.transAxes,
                    color="#888", fontsize=10)
            ax.set_title(name)
            continue
        offsets, mat = _window_matrix(df_lc, ph_crashes, PRE_WINDOW, POST_WINDOW)
        _plot_band(ax, offsets, mat, color, f"n={len(ph_crashes)}")
        ax.axvline(0, color="#5a4d42", linestyle=":", linewidth=0.7)
        ax.set_title(f"{name}")
        ax.set_xlabel("days rel. crash")
        ax.legend(fontsize=8)
    axes[0].set_ylabel(PRIMARY)
    fig.suptitle("C3 — Crash window per Citalopram phase  "
                 f"(t-{PRE_WINDOW} → t+{POST_WINDOW})", y=1.02)
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / "C3_crash_window_by_phase.png")


def c4_crash_density_scatter(df: pd.DataFrame) -> None:
    df_lc = add_phase(lc_era(df)).set_index("date").sort_index()
    # P7 proxy: rolling 14-day count of crash days
    df_lc["crash_14d"] = (
        df_lc["is_crash"].astype(float).rolling(14, min_periods=3).sum()
    )
    sub = df_lc[[PRIMARY, "crash_14d", "phase"]].dropna()
    if sub.empty:
        return

    fig, ax = plt.subplots(figsize=(9, 7))
    for name, color in PHASE_LIST:
        s = sub[sub["phase"] == name]
        if s.empty:
            continue
        ax.scatter(s["crash_14d"], s[PRIMARY], s=8, color=color, alpha=0.5,
                   edgecolors="none", label=f"{name} (n={len(s)})")
    rho = sub[PRIMARY].corr(sub["crash_14d"], method="spearman")
    ax.text(0.02, 0.98, f"Spearman ρ = {rho:.3f}",
            transform=ax.transAxes, va="top", fontsize=9,
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="#d8cdb9"))
    ax.set_xlabel("rolling 14-day crash count (P7 proxy)")
    ax.set_ylabel(PRIMARY)
    ax.set_title("C4 — primary vs recent crash density, per phase")
    ax.legend(fontsize=8, loc="upper right")
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / "C4_crash_density_scatter.png")


def main(df: pd.DataFrame | None = None) -> None:
    df = df if df is not None else load_master()
    print("Family C - event-aligned")
    c1_pre_crash(df)
    c2_post_crash(df)
    c3_by_phase(df)
    c4_crash_density_scatter(df)


if __name__ == "__main__":
    main()
