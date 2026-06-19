"""Family D — distributional + diagnostic plots.

D1  — histogram + KDE of primary per phase
D2a — scatter primary vs stress_high_duration_min (HA11-substitute), per phase
D2b — scatter primary vs stress_mean_sleep, per phase
D3  — scatter primary vs n_minutes_resp_above_18, per phase (orthogonality check)
D4  — coverage diagnostic: fraction of valid days per month
D5  — intensity-record-gap proxy: median primary count vs sample-size proxy
D6  — dose-response sanity: primary vs dose_plasma_mg, full citalopram-traject, per phase
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from _master_loader import (
    LC_ONSET, PHASES_FULL, PLOTS_DIR, PRIMARY,
    RESP_ABOVE_18, add_phase, lc_era, load_master, phase_color,
)
from _plot_utils import savefig, stamp_footer


def d1_hist_by_phase(df: pd.DataFrame) -> None:
    df_lc = add_phase(lc_era(df))
    fig, ax = plt.subplots(figsize=(12, 5))
    bins = np.linspace(0, df_lc[PRIMARY].quantile(0.99), 35)
    for name, _, _, color in PHASES_FULL:
        sub = df_lc[df_lc["phase"] == name][PRIMARY].dropna()
        if sub.empty:
            continue
        ax.hist(sub, bins=bins, alpha=0.5, color=color,
                label=f"{name} (n={len(sub)})", histtype="stepfilled",
                edgecolor=color, linewidth=1.2)
    ax.set_title(f"D1 — histogram of {PRIMARY} per Citalopram phase")
    ax.set_xlabel("minutes / day")
    ax.set_ylabel("count of days")
    ax.legend(fontsize=8)
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / "D1_hist_by_phase.png")


def _scatter_by_phase(df: pd.DataFrame, sibling: str, title: str, out: str,
                      x_label: str | None = None) -> None:
    if sibling not in df.columns:
        print(f"  skipping {out}: column {sibling} missing")
        return
    df_lc = add_phase(lc_era(df))
    sub = df_lc[[PRIMARY, sibling, "phase"]].dropna()
    if sub.empty:
        return

    fig, ax = plt.subplots(figsize=(9, 7))
    for name, _, _, color in PHASES_FULL:
        s = sub[sub["phase"] == name]
        if s.empty:
            continue
        ax.scatter(s[sibling], s[PRIMARY], s=10, color=color, alpha=0.55,
                   edgecolors="none", label=f"{name} (n={len(s)})")
    # add rank correlation across full sample
    rho = sub[PRIMARY].corr(sub[sibling], method="spearman")
    pearson = sub[PRIMARY].corr(sub[sibling])
    ax.text(0.02, 0.98, f"Spearman ρ = {rho:.3f}\nPearson r = {pearson:.3f}",
            transform=ax.transAxes, va="top", fontsize=9,
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="#d8cdb9"))
    ax.set_xlabel(x_label or sibling)
    ax.set_ylabel(PRIMARY)
    ax.set_title(title)
    ax.legend(fontsize=8, loc="lower right")
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / out)


def d2_scatter_siblings(df: pd.DataFrame) -> None:
    _scatter_by_phase(df, "stress_high_duration_min",
                      "D2a — primary vs stress_high_duration_min (HA11-substitute)",
                      "D2a_primary_vs_stress_high_duration.png")
    _scatter_by_phase(df, "stress_mean_sleep",
                      "D2b — primary vs stress_mean_sleep",
                      "D2b_primary_vs_stress_mean_sleep.png")
    _scatter_by_phase(df, "u_dip_count",
                      "D2c — primary vs u_dip_count (HA11 canonical sibling, MD reports rho=0.556)",
                      "D2c_primary_vs_u_dip_count.png")


def d3_orthogonality(df: pd.DataFrame) -> None:
    _scatter_by_phase(df, RESP_ABOVE_18,
                      "D3 — primary vs n_minutes_resp_above_18 (orthogonality check)",
                      "D3_primary_vs_resp_above_18.png")


def d4_coverage(df: pd.DataFrame) -> None:
    df_lc = lc_era(df).copy()
    # treat presence of primary value as "valid" (the extract sets to 0 on invalid,
    # but a value of 0 alongside zero respiration totals is the practical invalid
    # signal). use sample_count if available; fallback to value notnull.
    if "sample_count" in df_lc.columns:
        df_lc["valid"] = df_lc["sample_count"] >= 600
    else:
        df_lc["valid"] = df_lc[PRIMARY].notna()
    df_lc["yyyy_mm"] = df_lc["date"].dt.to_period("M").dt.to_timestamp()
    monthly = df_lc.groupby("yyyy_mm")["valid"].mean()

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.bar(monthly.index, monthly.values, width=20, color="#3f6b6e", alpha=0.85)
    ax.axhline(1.0, color="#888", linestyle=":", linewidth=0.7)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("fraction of days flagged valid")
    ax.set_title("D4 — per-month fraction of days with sufficient stress sampling (≥600 in-range mins)")
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / "D4_coverage_per_month.png")


def d5_intensity_gap_proxy(df: pd.DataFrame) -> None:
    """The MD reports an 81% intensity-record gap. The master CSV doesn't carry
    a per-day gap metric directly. Closest available proxy: per-day primary
    count broken down by the motion-class ladder (Mstrict vs Mlow vs Mbelow_mod)
    at the same stress threshold. If most minutes default to "no-record" (=low
    motion), then Mstrict (intensity == 0 explicitly) should be a small fraction
    of Mlow. Plot the ratio Mstrict / Mlow over time at S60.
    """
    df_lc = lc_era(df).copy().set_index("date").sort_index()
    strict = "stress_low_motion_min_count_S60_Mstrict"
    low    = "stress_low_motion_min_count_S60_Mlow"
    if strict not in df_lc.columns or low not in df_lc.columns:
        print("  skipping D5: required Mstrict/Mlow columns missing")
        return
    # avoid div-by-zero by masking days where low == 0
    ratio = df_lc[strict] / df_lc[low].where(df_lc[low] > 0)
    roll = ratio.rolling(14, min_periods=4).median()

    fig, ax = plt.subplots(figsize=(14, 4.5))
    ax.scatter(ratio.index, ratio.values, s=2, color="#8a7b6e", alpha=0.35,
               label="per day")
    ax.plot(roll.index, roll.values, color="#b04a32", linewidth=1.4,
            label="14d rolling median")
    ax.set_title("D5 — Mstrict / Mlow ratio at S60 over time (intensity-record-gap proxy)")
    ax.set_ylabel("ratio  (lower = more no-record minutes drove the count)")
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=8)
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / "D5_intensity_record_gap_proxy.png")


def d6_dose_response(df: pd.DataFrame) -> None:
    """D6 — primary vs dose_plasma_mg, full citalopram-traject (per interview)."""
    df_lc = add_phase(lc_era(df))
    sub = df_lc[df_lc["date"] >= pd.Timestamp("2024-04-09")][
        [PRIMARY, "dose_plasma_mg", "phase"]
    ].dropna()
    if sub.empty:
        print("  skipping D6: no usable rows")
        return

    fig, ax = plt.subplots(figsize=(9, 7))
    for name, _, _, color in PHASES_FULL:
        s = sub[sub["phase"] == name]
        if s.empty:
            continue
        ax.scatter(s["dose_plasma_mg"], s[PRIMARY], s=12, color=color, alpha=0.6,
                   edgecolors="none", label=f"{name} (n={len(s)})")
    # phase-pooled OLS on the full traject
    x = sub["dose_plasma_mg"].values.astype(float)
    y = sub[PRIMARY].values.astype(float)
    if len(x) >= 5 and x.std() > 0:
        b, a = np.polyfit(x, y, 1)
        xs = np.linspace(x.min(), x.max(), 50)
        ax.plot(xs, a + b * xs, color="#5a4d42", linewidth=1.2, linestyle="--",
                label=f"OLS  β = {b:+.2f} min / mg")
    rho = sub[PRIMARY].corr(sub["dose_plasma_mg"], method="spearman")
    ax.text(0.02, 0.98, f"Spearman ρ = {rho:.3f}",
            transform=ax.transAxes, va="top", fontsize=9,
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="#d8cdb9"))
    ax.set_xlabel("dose_plasma_mg (PK-smoothed)")
    ax.set_ylabel(PRIMARY)
    ax.set_title("D6 — primary vs dose_plasma_mg, full citalopram-traject (2024-04-09 →)")
    ax.legend(fontsize=8)
    stamp_footer(fig)
    savefig(fig, PLOTS_DIR / "D6_dose_response_full_traject.png")


def main(df: pd.DataFrame | None = None) -> None:
    df = df if df is not None else load_master()
    print("Family D - diagnostics")
    d1_hist_by_phase(df)
    d2_scatter_siblings(df)
    d3_orthogonality(df)
    d4_coverage(df)
    d5_intensity_gap_proxy(df)
    d6_dose_response(df)


if __name__ == "__main__":
    main()
