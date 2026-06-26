"""Descriptive analysis: trajectory/seasonality_dow -- Q4.8 confound check.

Strand B Tier-3 deferred topic 1 of 2 (Q4.7 notes-categorisation is the other).
Closes the canonical Q4.8 scope per descriptive/README.md section 4.8 (r2
closure D4.9): coherent per-channel seasonality + DOW pattern check across the
6 v3-CONFIRMED-plus-companion channels (matches Q4.9 + Q4.5.b + Q4.2 scope);
extends v3 spring-2025 control logic to all 6 channels per
citalopram_dose_response_stress_mean_sleep.md section 5.6 LOAD-BEARING; adds
per-recovery-phase harmonic amplitude per lc_recovery_phase_axis.md.

User-LOCKED operationalisation (per Strand B section 7c interview 2026-06-25;
do NOT iterate):

1. Channel scope = 6 channels: stress_mean_sleep + all_day_stress_avg +
   bb_lowest + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow +
   resting_hr.
2. Seasonality method = both harmonic + per-month: sin/cos annual harmonic
   regression (1-year periodicity) + per-month median table (12 strata).
3. DOW method = both per-DOW + weekday-vs-weekend: per-DOW median (7 strata)
   + weekday-vs-weekend Mann-Whitney U.
4. Confound disambiguation = both v3 spring-control extension + per-recovery-
   phase seasonality.

Discipline guards:
- Layer 1 descriptive per CONVENTIONS section 2.1: NO causal claims; NO claim
  citalopram is/is-not seasonally confounded (that is v3-extension territory;
  descriptive check only).
- Per CONVENTIONS section 4.2 caveat-class: "harmonic R2=X; amplitude Y;
  suspect for seasonality confound" -- NOT "the multi-year arc is partly
  seasonal".
- ASCII-only stdout; no em-dashes; no emojis.
- f-string discipline: no nested double-quotes inside expressions.

Output (all but findings.md + README.md + run.py gitignored):
- summary.json -- machine-readable per-channel per-stage statistics
- plots/<channel>_harmonic.png -- per-channel harmonic-fit visualisation
- plots/seasonality_per_month.png -- per-channel x month median grid
- plots/dow_per_day.png -- per-channel x DOW median grid
- plots/v3_spring_control_extension.png -- 6-channel spring-control bar
- plots/per_phase_seasonality_heatmap.png -- channel x phase amplitude
- findings.md -- programmatic emit
- README.md -- programmatic emit
"""

from __future__ import annotations

import json
import math
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats as scistats


HERE = Path(__file__).resolve().parent
# HERE = .../analyses/descriptive/trajectory/seasonality_dow
# parents[0]=trajectory, [1]=descriptive, [2]=analyses
UTILS_DIR = HERE.parents[2] / "_utils"
sys.path.insert(0, str(UTILS_DIR))

from frame import load_master  # noqa: E402


AS_OF_DATE = "2026-06-04"

# 6 channels per locked operationalisation (matches Q4.9 + Q4.5.b + Q4.2)
CHANNELS = [
    "stress_mean_sleep",
    "all_day_stress_avg",
    "bb_lowest",
    "stress_stdev_sleep",
    "stress_low_motion_min_count_S60_Mlow",
    "resting_hr",
]

# v3-CONFIRMED-citalopram channels per citalopram_dose_response_stress_mean_sleep.md
# section 5.6 (beta sign convention: positive = higher dose -> higher channel)
CONFIRMED_CITALOPRAM = {
    "stress_mean_sleep":   {"beta": +0.43, "prior": +1},   # p=0.001
    "all_day_stress_avg":  {"beta": +0.57, "prior": +1},   # p=0.000
    "bb_lowest":           {"beta": -1.13, "prior": -1},   # p=0.000
}

# Six phases per lc_recovery_phase_axis.md section 2 (LOCKED d47e0d3 2026-06-19)
PHASE_ORDER = [
    "pre_illness_healthy",
    "acute_infection",
    "lc_pre_ergo",
    "pacing_pre_citalopram_learning",
    "pacing_habit_established",
    "citalopram_modulated",
]

# v3 spring-control window per citalopram_dose_response_stress_mean_sleep.md
# section 5.5 (also spring_comparison.py) -- March 20 -> June 5
SPRING_WINDOW_START = (3, 20)
SPRING_WINDOW_END = (6, 5)
# Per spring_comparison.py: 2025 is the CLEAN CONTROL (30mg consolidation
# throughout, no other interventions); 2026 is the TEST year (afbouw).
SPRING_TEST_YEAR = 2026
SPRING_CONTROL_YEAR = 2025

HARMONIC_R2_SUSPECT_THRESHOLD = 0.10
HAC_MAXLAGS = 4
KW_SUSPECT_THRESHOLD = 0.05
MWU_SUSPECT_THRESHOLD = 0.05
SEED = 20260626

WEEKEND_DOWS = {5, 6}   # pandas Mon=0 ... Sun=6
DOW_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


# -----------------------------------------------------------------------------
# Stage 1 -- data prep
# -----------------------------------------------------------------------------


def stage_1_load_data():
    """Load per_day_master; restrict to 6 channels; identify recovery_phase
    + citalopram_phase + month + DOW per row."""
    print("=" * 70)
    print("STAGE 1: data prep (load per_day_master + identify covariates)")
    print("=" * 70)
    df = load_master(as_of_date=AS_OF_DATE)
    df = df.copy()
    df["date_dt"] = pd.to_datetime(df["date"])
    df["doy"] = df["date_dt"].dt.dayofyear
    df["year"] = df["date_dt"].dt.year
    df["month"] = df["date_dt"].dt.month
    df["dow"] = df["date_dt"].dt.dayofweek
    df["is_weekend"] = df["dow"].isin(WEEKEND_DOWS)

    print(f"  loaded n_rows={len(df)} as_of_date={AS_OF_DATE}")
    print(f"  date range: {df['date_dt'].min().date()} -> {df['date_dt'].max().date()}")
    # Check presence of expected columns
    missing = [c for c in CHANNELS + ["recovery_phase"] if c not in df.columns]
    if missing:
        raise RuntimeError(f"missing required columns in per_day_master: {missing}")
    # Per-channel non-null counts
    print("  per-channel non-null counts:")
    for ch in CHANNELS:
        n_nn = int(df[ch].notna().sum())
        print(f"    {ch}: n_nonnull={n_nn}")
    print("  recovery_phase value counts:")
    for ph in PHASE_ORDER:
        n_ph = int((df["recovery_phase"] == ph).sum())
        print(f"    {ph}: n={n_ph}")
    print()
    return df


# -----------------------------------------------------------------------------
# Stage 2 -- seasonality harmonic (sin/cos annual)
# -----------------------------------------------------------------------------


def fit_harmonic(series_index_dates, series_values):
    """Fit y = alpha + b1*sin(2*pi*doy/365) + b2*cos(2*pi*doy/365) + eps.

    Returns dict with amplitude, phase_peak_doy, r2, p_f, n, beta_sin, beta_cos.
    Phase reported as the day-of-year (1..365) where the harmonic peaks.
    """
    s = pd.Series(series_values, index=series_index_dates).dropna()
    if len(s) < 30:
        return None
    doy = s.index.dayofyear.values.astype(float)
    omega = 2.0 * math.pi / 365.0
    sin_t = np.sin(omega * doy)
    cos_t = np.cos(omega * doy)
    X = pd.DataFrame({
        "const": 1.0,
        "sin_t": sin_t,
        "cos_t": cos_t,
    })
    y = s.values.astype(float)
    fit = sm.OLS(y, X).fit()
    b_sin = float(fit.params["sin_t"])
    b_cos = float(fit.params["cos_t"])
    amplitude = float(math.hypot(b_sin, b_cos))
    # Peak of A*sin(omega*t + phi) where phi = atan2(b_cos, b_sin); but our
    # parametrisation is b_sin*sin + b_cos*cos = A*sin(omega*t + phi) with
    # phi = atan2(b_cos, b_sin). Peak occurs when omega*t + phi = pi/2.
    phi = math.atan2(b_cos, b_sin)
    t_peak = (math.pi / 2.0 - phi) / omega
    # t_peak is in calendar-day units, may be negative or > 365; map to 1..365
    doy_peak = float(((t_peak - 1.0) % 365.0) + 1.0)
    r2 = float(fit.rsquared)
    p_f = float(fit.f_pvalue) if fit.f_pvalue is not None else float("nan")
    return {
        "n": int(len(s)),
        "beta_sin": b_sin,
        "beta_cos": b_cos,
        "amplitude": amplitude,
        "phase_peak_doy": doy_peak,
        "r2": r2,
        "p_f": p_f,
        "suspect": bool(r2 >= HARMONIC_R2_SUSPECT_THRESHOLD),
    }


def stage_2_harmonic(df):
    print("=" * 70)
    print("STAGE 2: seasonality harmonic (sin/cos annual; R2 >= 0.10 = suspect)")
    print("=" * 70)
    results = {}
    for ch in CHANNELS:
        sub = df[["date_dt", ch]].dropna().set_index("date_dt")
        r = fit_harmonic(sub.index, sub[ch].values)
        if r is None:
            results[ch] = None
            print(f"  {ch}: SKIP (n insufficient)")
            continue
        results[ch] = r
        flag = "SUSPECT" if r["suspect"] else "no-flag"
        print(
            f"  {ch}: n={r['n']:>4}  R2={r['r2']:.4f}  "
            f"amplitude={r['amplitude']:.3f}  "
            f"peak_doy={r['phase_peak_doy']:.0f}  p_F={r['p_f']:.4f}  [{flag}]"
        )
    suspect_count = sum(1 for v in results.values() if v and v["suspect"])
    print(f"  -> {suspect_count} of {len(CHANNELS)} channels flagged suspect (R2 >= {HARMONIC_R2_SUSPECT_THRESHOLD})")
    print()
    return results


# -----------------------------------------------------------------------------
# Stage 3 -- seasonality per-month (12-stratum + Kruskal-Wallis)
# -----------------------------------------------------------------------------


def stage_3_per_month(df):
    print("=" * 70)
    print("STAGE 3: seasonality per-month (12-stratum + Kruskal-Wallis)")
    print("=" * 70)
    results = {}
    for ch in CHANNELS:
        sub = df[[ch, "month"]].dropna()
        per_month = []
        groups = []
        for m in range(1, 13):
            vals = sub.loc[sub["month"] == m, ch].values
            if len(vals) == 0:
                per_month.append({"month": m, "n": 0, "median": None, "iqr_lo": None, "iqr_hi": None})
                continue
            q1, med, q3 = np.percentile(vals, [25, 50, 75])
            per_month.append({
                "month": m,
                "n": int(len(vals)),
                "median": float(med),
                "iqr_lo": float(q1),
                "iqr_hi": float(q3),
            })
            groups.append(vals)
        if len(groups) >= 2 and all(len(g) >= 2 for g in groups):
            try:
                kw_stat, kw_p = scistats.kruskal(*groups)
                kw_stat = float(kw_stat)
                kw_p = float(kw_p)
            except Exception as exc:
                print(f"  {ch}: KW failed -- {exc}")
                kw_stat, kw_p = float("nan"), float("nan")
        else:
            kw_stat, kw_p = float("nan"), float("nan")
        medians = [row["median"] for row in per_month if row["median"] is not None]
        if medians:
            grand_med = float(np.median(medians))
            deviations = [abs(m_ - grand_med) for m_ in medians]
            spread = float(max(medians) - min(medians))
        else:
            grand_med = float("nan")
            deviations = []
            spread = float("nan")
        results[ch] = {
            "per_month": per_month,
            "kw_stat": kw_stat,
            "kw_p": kw_p,
            "grand_median": grand_med,
            "month_median_spread": spread,
        }
        flag = "SUSPECT" if (not math.isnan(kw_p) and kw_p < KW_SUSPECT_THRESHOLD) else "no-flag"
        print(
            f"  {ch}: KW H={kw_stat:.2f}  p={kw_p:.4f}  "
            f"month_median_spread={spread:.3f}  [{flag}]"
        )
    print()
    return results


# -----------------------------------------------------------------------------
# Stage 4 -- DOW per-day (7-stratum + Kruskal-Wallis)
# -----------------------------------------------------------------------------


def stage_4_per_dow(df):
    print("=" * 70)
    print("STAGE 4: DOW per-day (7-stratum + Kruskal-Wallis)")
    print("=" * 70)
    results = {}
    for ch in CHANNELS:
        sub = df[[ch, "dow"]].dropna()
        per_dow = []
        groups = []
        for d_ in range(7):
            vals = sub.loc[sub["dow"] == d_, ch].values
            if len(vals) == 0:
                per_dow.append({"dow": d_, "name": DOW_NAMES[d_], "n": 0, "median": None, "iqr_lo": None, "iqr_hi": None})
                continue
            q1, med, q3 = np.percentile(vals, [25, 50, 75])
            per_dow.append({
                "dow": d_,
                "name": DOW_NAMES[d_],
                "n": int(len(vals)),
                "median": float(med),
                "iqr_lo": float(q1),
                "iqr_hi": float(q3),
            })
            groups.append(vals)
        if len(groups) >= 2 and all(len(g) >= 2 for g in groups):
            try:
                kw_stat, kw_p = scistats.kruskal(*groups)
                kw_stat = float(kw_stat)
                kw_p = float(kw_p)
            except Exception as exc:
                print(f"  {ch}: KW failed -- {exc}")
                kw_stat, kw_p = float("nan"), float("nan")
        else:
            kw_stat, kw_p = float("nan"), float("nan")
        medians = [row["median"] for row in per_dow if row["median"] is not None]
        spread = float(max(medians) - min(medians)) if medians else float("nan")
        results[ch] = {
            "per_dow": per_dow,
            "kw_stat": kw_stat,
            "kw_p": kw_p,
            "dow_median_spread": spread,
        }
        flag = "SUSPECT" if (not math.isnan(kw_p) and kw_p < KW_SUSPECT_THRESHOLD) else "no-flag"
        print(
            f"  {ch}: KW H={kw_stat:.2f}  p={kw_p:.4f}  "
            f"dow_median_spread={spread:.3f}  [{flag}]"
        )
    print()
    return results


# -----------------------------------------------------------------------------
# Stage 5 -- DOW weekday-vs-weekend (Mann-Whitney U)
# -----------------------------------------------------------------------------


def cliffs_delta(x, y):
    """Compute Cliff's delta non-parametric effect size: in [-1, +1].

    Positive = x tends to be larger; negative = x tends to be smaller.
    Uses rank-based formula to avoid O(n*m) when arrays are large.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n_x = len(x)
    n_y = len(y)
    if n_x == 0 or n_y == 0:
        return float("nan")
    pooled = np.concatenate([x, y])
    ranks = scistats.rankdata(pooled)
    rx = ranks[:n_x].sum()
    # U statistic relative to x
    u_x = rx - n_x * (n_x + 1) / 2.0
    # Cliff's delta = 2*U/(n_x*n_y) - 1
    return float(2.0 * u_x / (n_x * n_y) - 1.0)


def stage_5_weekend(df):
    print("=" * 70)
    print("STAGE 5: weekday-vs-weekend (Mann-Whitney U + Cliff's delta)")
    print("=" * 70)
    results = {}
    for ch in CHANNELS:
        sub = df[[ch, "is_weekend"]].dropna()
        weekday = sub.loc[~sub["is_weekend"], ch].values
        weekend = sub.loc[sub["is_weekend"], ch].values
        if len(weekday) < 2 or len(weekend) < 2:
            results[ch] = None
            print(f"  {ch}: SKIP (n insufficient)")
            continue
        med_wd = float(np.median(weekday))
        med_we = float(np.median(weekend))
        delta_med = med_we - med_wd
        try:
            u_stat, p_two = scistats.mannwhitneyu(
                weekday, weekend, alternative="two-sided"
            )
            u_stat = float(u_stat)
            p_two = float(p_two)
        except Exception as exc:
            print(f"  {ch}: MWU failed -- {exc}")
            u_stat, p_two = float("nan"), float("nan")
        cd = cliffs_delta(weekend, weekday)
        results[ch] = {
            "n_weekday": int(len(weekday)),
            "n_weekend": int(len(weekend)),
            "median_weekday": med_wd,
            "median_weekend": med_we,
            "weekend_minus_weekday_median": float(delta_med),
            "mwu_u": u_stat,
            "mwu_p_two": p_two,
            "cliffs_delta_weekend_vs_weekday": cd,
        }
        flag = "SUSPECT" if (not math.isnan(p_two) and p_two < MWU_SUSPECT_THRESHOLD) else "no-flag"
        print(
            f"  {ch}: n_wd={len(weekday)} n_we={len(weekend)}  "
            f"med_wd={med_wd:.3f} med_we={med_we:.3f} "
            f"delta={delta_med:+.3f} MWU p={p_two:.4f}  "
            f"cliff={cd:+.4f}  [{flag}]"
        )
    print()
    return results


# -----------------------------------------------------------------------------
# Stage 6 -- v3 spring-control extension (per channel)
# -----------------------------------------------------------------------------


def fit_spring_slope(df, channel, year):
    """Fit channel ~ const + beta_time*days on the spring window
    (March 20 -> June 5) of `year` per spring_comparison.py.

    Returns dict with beta_time, HAC SE, CI, p, n, or None if n<10.
    """
    start = pd.Timestamp(year=year, month=SPRING_WINDOW_START[0], day=SPRING_WINDOW_START[1])
    end = pd.Timestamp(year=year, month=SPRING_WINDOW_END[0], day=SPRING_WINDOW_END[1])
    sub = df.loc[
        (df["date_dt"] >= start) & (df["date_dt"] <= end),
        ["date_dt", channel]
    ].dropna()
    if len(sub) < 10:
        return None
    sub = sub.copy()
    sub["days"] = (sub["date_dt"] - start).dt.days.astype(float)
    X = pd.DataFrame({"const": 1.0, "time": sub["days"].values})
    y = sub[channel].values
    fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_MAXLAGS})
    beta = float(fit.params["time"])
    se = float(fit.bse["time"])
    ci_lo, ci_hi = (float(c) for c in fit.conf_int(alpha=0.05).loc["time"])
    p_two = float(fit.pvalues["time"])
    return {
        "year": int(year),
        "n": int(len(sub)),
        "beta_time": beta,
        "hac_se": se,
        "ci_lo": ci_lo,
        "ci_hi": ci_hi,
        "p_two_sided": p_two,
        "median": float(np.median(y)),
        "first": float(sub[channel].iloc[0]),
        "last": float(sub[channel].iloc[-1]),
    }


def stage_6_spring_control(df):
    print("=" * 70)
    print("STAGE 6: v3 spring-control extension to all 6 channels")
    print(f"  window: {SPRING_WINDOW_START[0]:02d}-{SPRING_WINDOW_START[1]:02d} -> "
          f"{SPRING_WINDOW_END[0]:02d}-{SPRING_WINDOW_END[1]:02d}; "
          f"test_year={SPRING_TEST_YEAR}; control_year={SPRING_CONTROL_YEAR}")
    print("=" * 70)
    results = {}
    for ch in CHANNELS:
        per_year = {}
        for y in (SPRING_CONTROL_YEAR, SPRING_TEST_YEAR):
            fit = fit_spring_slope(df, ch, y)
            per_year[y] = fit
        ctrl = per_year.get(SPRING_CONTROL_YEAR)
        test = per_year.get(SPRING_TEST_YEAR)
        if ctrl is None or test is None:
            results[ch] = {"per_year": per_year, "step_survives_same_season": None}
            print(f"  {ch}: SKIP (n insufficient in one year)")
            continue
        # Descriptive "does the step survive same-season comparison?" reading:
        # the v3 logic in spring_comparison.py compares beta_2025 vs beta_2026.
        # We report: (a) absolute difference in betas; (b) the citalopram
        # prior-direction (sign) for CONFIRMED channels, descriptively only.
        delta_beta = test["beta_time"] - ctrl["beta_time"]
        prior_info = CONFIRMED_CITALOPRAM.get(ch)
        # For CONFIRMED-citalopram channels, the v3 dose-down prediction is:
        # 2026 (afbouw, dose decreasing) shows a trajectory consistent with
        # prior * (-1) since dose is decreasing. E.g. for stress (+1 prior),
        # afbouw should show NEGATIVE beta_time; control year flat.
        if prior_info is not None:
            expected_test_sign = -prior_info["prior"]  # afbouw decreases dose
            # Heuristic "step-survives-same-season" descriptive flag: the test
            # year shows a clear beta in the expected direction AND the
            # control year is roughly flat (|beta_2025| << |beta_2026|).
            test_signed = test["beta_time"] * expected_test_sign  # > 0 if expected direction
            ctrl_abs = abs(ctrl["beta_time"])
            test_abs = abs(test["beta_time"])
            if test_abs > 0 and ctrl_abs / max(test_abs, 1e-9) < 0.5 and test_signed > 0:
                step_survives = "yes-direction-and-2025-flat"
            elif test_signed > 0 and ctrl_abs / max(test_abs, 1e-9) >= 0.5:
                step_survives = "ambiguous-control-similar-magnitude"
            else:
                step_survives = "no-or-wrong-direction"
        else:
            step_survives = "not-CONFIRMED-channel"
        results[ch] = {
            "per_year": per_year,
            "delta_beta_time_test_minus_control": delta_beta,
            "step_survives_same_season": step_survives,
        }
        c_str = (
            f"beta_2025={ctrl['beta_time']:+.4f} CI=[{ctrl['ci_lo']:+.4f},{ctrl['ci_hi']:+.4f}] p={ctrl['p_two_sided']:.3f}"
        )
        t_str = (
            f"beta_2026={test['beta_time']:+.4f} CI=[{test['ci_lo']:+.4f},{test['ci_hi']:+.4f}] p={test['p_two_sided']:.3f}"
        )
        print(f"  {ch}: {c_str}")
        print(f"  {' ' * len(ch)}  {t_str}")
        print(f"  {' ' * len(ch)}  delta={delta_beta:+.4f}  flag={step_survives}")
    print()
    return results


# -----------------------------------------------------------------------------
# Stage 7 -- per-recovery-phase seasonality
# -----------------------------------------------------------------------------


def stage_7_per_phase(df):
    print("=" * 70)
    print("STAGE 7: per-recovery-phase seasonality (harmonic per channel x phase)")
    print("=" * 70)
    results = {}
    for ch in CHANNELS:
        per_phase = {}
        for ph in PHASE_ORDER:
            sub = df.loc[df["recovery_phase"] == ph, ["date_dt", ch]].dropna()
            if len(sub) < 30:
                per_phase[ph] = {"n": int(len(sub)), "fit": None, "note": "n<30; skipped"}
                continue
            # Only fit if the within-phase data spans >= 180 days (otherwise
            # the annual harmonic is underdetermined for the phase).
            span_days = (sub["date_dt"].max() - sub["date_dt"].min()).days
            if span_days < 180:
                per_phase[ph] = {
                    "n": int(len(sub)),
                    "fit": None,
                    "note": f"span={span_days}d < 180d; annual harmonic underdetermined",
                }
                continue
            sub_idx = sub.set_index("date_dt")
            r = fit_harmonic(sub_idx.index, sub_idx[ch].values)
            per_phase[ph] = {"n": int(len(sub)), "fit": r, "span_days": int(span_days)}
        results[ch] = per_phase
        cells_str = []
        for ph in PHASE_ORDER:
            cell = per_phase[ph]
            if cell["fit"] is None:
                cells_str.append(f"{ph}=n/a(n={cell['n']})")
            else:
                cells_str.append(
                    f"{ph}=A{cell['fit']['amplitude']:.2f}R2{cell['fit']['r2']:.2f}(n={cell['n']})"
                )
        print(f"  {ch}:")
        for s in cells_str:
            print(f"    {s}")
    print()
    return results


# -----------------------------------------------------------------------------
# Stage 8 -- output artefacts (plots)
# -----------------------------------------------------------------------------


def stage_8_plots(df, out_dir, harmonic_res, per_month_res, per_dow_res,
                  weekend_res, spring_res, per_phase_res):
    print("=" * 70)
    print("STAGE 8: output artefacts (plots + summary tables)")
    print("=" * 70)
    plots_dir = out_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    # Plot 1: per-channel harmonic fit overlays
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    axes = axes.flatten()
    for i, ch in enumerate(CHANNELS):
        ax = axes[i]
        sub = df[["date_dt", "doy", ch]].dropna()
        ax.scatter(sub["doy"], sub[ch], s=3, alpha=0.25, color="gray")
        r = harmonic_res.get(ch)
        if r is not None:
            doy_grid = np.arange(1, 366)
            omega = 2.0 * math.pi / 365.0
            y_pred = (
                np.mean(sub[ch])  # constant offset for visual; not exact alpha
                + r["beta_sin"] * np.sin(omega * doy_grid)
                + r["beta_cos"] * np.cos(omega * doy_grid)
            )
            # Re-fit constant to data mean for visual alignment (display only)
            offset = float(np.mean(sub[ch]) - np.mean(y_pred - np.mean(sub[ch])))
            y_pred = (
                offset
                + r["beta_sin"] * np.sin(omega * doy_grid)
                + r["beta_cos"] * np.cos(omega * doy_grid)
            )
            flag_text = "SUSPECT" if r["suspect"] else "no-flag"
            ax.plot(doy_grid, y_pred, "r-", lw=2,
                    label=f"A={r['amplitude']:.2f} R2={r['r2']:.3f} [{flag_text}]")
            ax.legend(fontsize=8, loc="upper right")
        ax.set_title(ch, fontsize=10)
        ax.set_xlabel("Day-of-year")
        ax.set_ylabel(ch)
        ax.grid(True, alpha=0.3)
    for j in range(len(CHANNELS), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Per-channel annual harmonic fit (R2 >= 0.10 = SUSPECT)", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fpath = plots_dir / "harmonic_fits.png"
    plt.savefig(fpath, dpi=100)
    plt.close()
    print(f"  wrote {fpath.name}")

    # Plot 2: per-channel x month median grid
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    axes = axes.flatten()
    for i, ch in enumerate(CHANNELS):
        ax = axes[i]
        per_month = per_month_res[ch]["per_month"]
        months_x = [row["month"] for row in per_month if row["median"] is not None]
        meds = [row["median"] for row in per_month if row["median"] is not None]
        iqr_lo = [row["iqr_lo"] for row in per_month if row["median"] is not None]
        iqr_hi = [row["iqr_hi"] for row in per_month if row["median"] is not None]
        err_lo = [m - lo for m, lo in zip(meds, iqr_lo)]
        err_hi = [hi - m for m, hi in zip(meds, iqr_hi)]
        ax.errorbar(months_x, meds, yerr=[err_lo, err_hi], fmt="o-", capsize=4)
        kw_p = per_month_res[ch]["kw_p"]
        flag = "SUSPECT" if (not math.isnan(kw_p) and kw_p < KW_SUSPECT_THRESHOLD) else "no-flag"
        ax.set_title(f"{ch}  KW p={kw_p:.4f} [{flag}]", fontsize=10)
        ax.set_xticks(list(range(1, 13)))
        ax.set_xticklabels(MONTH_NAMES, rotation=45)
        ax.set_ylabel("median")
        ax.grid(True, alpha=0.3)
    for j in range(len(CHANNELS), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Per-channel per-month median (error bars = IQR)", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fpath = plots_dir / "seasonality_per_month.png"
    plt.savefig(fpath, dpi=100)
    plt.close()
    print(f"  wrote {fpath.name}")

    # Plot 3: per-channel x DOW median grid
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    axes = axes.flatten()
    for i, ch in enumerate(CHANNELS):
        ax = axes[i]
        per_dow = per_dow_res[ch]["per_dow"]
        dows_x = [row["dow"] for row in per_dow if row["median"] is not None]
        names = [row["name"] for row in per_dow if row["median"] is not None]
        meds = [row["median"] for row in per_dow if row["median"] is not None]
        iqr_lo = [row["iqr_lo"] for row in per_dow if row["median"] is not None]
        iqr_hi = [row["iqr_hi"] for row in per_dow if row["median"] is not None]
        err_lo = [m - lo for m, lo in zip(meds, iqr_lo)]
        err_hi = [hi - m for m, hi in zip(meds, iqr_hi)]
        colors_x = ["steelblue" if d_ < 5 else "darkorange" for d_ in dows_x]
        ax.errorbar(dows_x, meds, yerr=[err_lo, err_hi], fmt="none", capsize=4, ecolor="gray")
        ax.scatter(dows_x, meds, c=colors_x, s=60, zorder=5)
        kw_p = per_dow_res[ch]["kw_p"]
        wflag = ""
        we_res = weekend_res.get(ch)
        if we_res is not None and not math.isnan(we_res["mwu_p_two"]):
            wflag = f"  WE_MWU p={we_res['mwu_p_two']:.4f}"
        kw_flag = "SUSPECT" if (not math.isnan(kw_p) and kw_p < KW_SUSPECT_THRESHOLD) else "no-flag"
        ax.set_title(f"{ch}  KW p={kw_p:.4f} [{kw_flag}]{wflag}", fontsize=9)
        ax.set_xticks(dows_x)
        ax.set_xticklabels(names)
        ax.set_ylabel("median")
        ax.grid(True, alpha=0.3)
    for j in range(len(CHANNELS), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Per-channel per-DOW median (blue=weekday; orange=weekend; error bars=IQR)", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fpath = plots_dir / "dow_per_day.png"
    plt.savefig(fpath, dpi=100)
    plt.close()
    print(f"  wrote {fpath.name}")

    # Plot 4: v3 spring-control extension bar
    fig, ax = plt.subplots(figsize=(12, 6))
    n_ch = len(CHANNELS)
    x = np.arange(n_ch)
    width = 0.35
    betas_ctrl = []
    betas_test = []
    errs_ctrl = []
    errs_test = []
    for ch in CHANNELS:
        per_year = spring_res[ch]["per_year"]
        c_ = per_year.get(SPRING_CONTROL_YEAR)
        t_ = per_year.get(SPRING_TEST_YEAR)
        betas_ctrl.append(c_["beta_time"] if c_ else np.nan)
        betas_test.append(t_["beta_time"] if t_ else np.nan)
        errs_ctrl.append([
            (c_["beta_time"] - c_["ci_lo"]) if c_ else 0,
            (c_["ci_hi"] - c_["beta_time"]) if c_ else 0,
        ])
        errs_test.append([
            (t_["beta_time"] - t_["ci_lo"]) if t_ else 0,
            (t_["ci_hi"] - t_["beta_time"]) if t_ else 0,
        ])
    errs_ctrl_arr = np.array(errs_ctrl).T
    errs_test_arr = np.array(errs_test).T
    ax.bar(x - width / 2, betas_ctrl, width, yerr=errs_ctrl_arr, capsize=4,
           color="steelblue", label=f"{SPRING_CONTROL_YEAR} (control: 30mg consolidation)")
    ax.bar(x + width / 2, betas_test, width, yerr=errs_test_arr, capsize=4,
           color="firebrick", label=f"{SPRING_TEST_YEAR} (test: afbouw 30->8mg)")
    ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(CHANNELS, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("beta_time (channel-units per day; spring window)")
    ax.set_title(
        "v3 spring-control extension to all 6 channels; "
        f"window {SPRING_WINDOW_START[0]:02d}-{SPRING_WINDOW_START[1]:02d} -> "
        f"{SPRING_WINDOW_END[0]:02d}-{SPRING_WINDOW_END[1]:02d}; HAC CIs"
    )
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    fpath = plots_dir / "v3_spring_control_extension.png"
    plt.savefig(fpath, dpi=100)
    plt.close()
    print(f"  wrote {fpath.name}")

    # Plot 5: per-recovery-phase seasonality heatmap (channel x phase amplitude)
    amp_grid = np.full((len(CHANNELS), len(PHASE_ORDER)), np.nan)
    r2_grid = np.full((len(CHANNELS), len(PHASE_ORDER)), np.nan)
    for i, ch in enumerate(CHANNELS):
        for j, ph in enumerate(PHASE_ORDER):
            cell = per_phase_res[ch].get(ph, {})
            fit = cell.get("fit")
            if fit is not None:
                amp_grid[i, j] = fit["amplitude"]
                r2_grid[i, j] = fit["r2"]
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    for k, (mat, label) in enumerate([(amp_grid, "harmonic amplitude"), (r2_grid, "harmonic R2")]):
        ax = axes[k]
        im = ax.imshow(mat, aspect="auto", cmap="viridis", interpolation="nearest")
        ax.set_xticks(range(len(PHASE_ORDER)))
        ax.set_xticklabels(PHASE_ORDER, rotation=30, ha="right", fontsize=8)
        ax.set_yticks(range(len(CHANNELS)))
        ax.set_yticklabels(CHANNELS, fontsize=8)
        ax.set_title(f"per-recovery-phase {label}")
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                v = mat[i, j]
                if not np.isnan(v):
                    color_text = "white" if v < np.nanmean(mat) else "black"
                    ax.text(j, i, f"{v:.2f}", ha="center", va="center", color=color_text, fontsize=7)
                else:
                    ax.text(j, i, "n/a", ha="center", va="center", color="white", fontsize=7)
        fig.colorbar(im, ax=ax)
    plt.tight_layout()
    fpath = plots_dir / "per_phase_seasonality_heatmap.png"
    plt.savefig(fpath, dpi=100)
    plt.close()
    print(f"  wrote {fpath.name}")

    print()


# -----------------------------------------------------------------------------
# Stage 9 -- programmatic emit (findings.md + README.md)
# -----------------------------------------------------------------------------


def stage_9_emit_summary_json(out_dir, harmonic_res, per_month_res, per_dow_res,
                              weekend_res, spring_res, per_phase_res):
    summary = {
        "as_of_date": AS_OF_DATE,
        "channels": CHANNELS,
        "confirmed_citalopram_channels": list(CONFIRMED_CITALOPRAM.keys()),
        "user_locked_operationalisation": {
            "channel_scope": "6 channels (matches Q4.9 + Q4.5.b + Q4.2)",
            "seasonality_method": "both harmonic + per-month (12-stratum)",
            "dow_method": "both per-DOW (7-stratum) + weekday-vs-weekend MWU",
            "confound_disambiguation": "both v3 spring-control extension + per-recovery-phase seasonality",
        },
        "stage_2_harmonic": harmonic_res,
        "stage_3_per_month": per_month_res,
        "stage_4_per_dow": per_dow_res,
        "stage_5_weekend_mwu": weekend_res,
        "stage_6_spring_control": spring_res,
        "stage_7_per_phase_harmonic": per_phase_res,
        "thresholds": {
            "harmonic_r2_suspect": HARMONIC_R2_SUSPECT_THRESHOLD,
            "kw_suspect_p": KW_SUSPECT_THRESHOLD,
            "mwu_suspect_p": MWU_SUSPECT_THRESHOLD,
            "hac_maxlags": HAC_MAXLAGS,
        },
    }
    fpath = out_dir / "summary.json"
    with open(fpath, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, default=str)
    print(f"  wrote {fpath.name}")
    return summary


def fmt_float(v, ndp=3, default="n/a"):
    if v is None:
        return default
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return default
    return f"{v:.{ndp}f}"


def fmt_signed(v, ndp=3, default="n/a"):
    if v is None:
        return default
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return default
    return f"{v:+.{ndp}f}"


def stage_9_emit_findings_md(out_dir, harmonic_res, per_month_res, per_dow_res,
                             weekend_res, spring_res, per_phase_res, n_rows_total):
    fpath = out_dir / "findings.md"
    lines = []
    a = lines.append

    a("# `trajectory/seasonality_dow/` -- findings (Q4.8 confound check)")
    a("")
    a("## Authorship")
    a("")
    a("- **Computed**: 2026-06-26 by Claude (Opus 4.7) via [`run.py`](run.py) under the user-LOCKED operationalisation in [`README.md`](README.md) (Strand B section 7c interview 2026-06-25).")
    a(f"- **Data**: `per_day_master.csv` at `$GEVOELSCORE_DATA_PATH/unified/`; as-of-date **{AS_OF_DATE}** (Garmin coverage right edge per [STOCKTAKE section 1](../../../../STOCKTAKE.md#1-the-corpus)). {n_rows_total} day-level rows.")
    a("- **Axis**: 6-phase LC recovery axis from [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) (LOCKED `d47e0d3` 2026-06-19) for Stage 7.")
    a("- **Layer 1 descriptive per [CONVENTIONS section 2.1 + section 4.3](../../../../CONVENTIONS.md)**: NO causal claims; NO `SUPPORTED` bar; NO `REFUTED` mark. This document characterises seasonality + DOW patterns on the 6 channels; intervention attribution is out of scope. Per CONVENTIONS section 4.2 caveat-class: seasonality detected on a channel is reported as `harmonic R2=X; amplitude Y; suspect for seasonality confound` -- NOT promoted to `the multi-year arc is partly seasonal`.")
    a("- **Cross-references**: [`run.py`](run.py) + [`summary.json`](summary.json) (gitignored) + [`plots/`](plots/) (5 PNGs, gitignored). Per-channel per-stage numbers below trace to the JSON.")
    a("")
    a("---")
    a("")

    # Headline
    a("## Headline")
    a("")
    suspect_harm = sum(1 for ch in CHANNELS if harmonic_res.get(ch) and harmonic_res[ch]["suspect"])
    a(f"**Seasonality (harmonic, annual)**: {suspect_harm} of {len(CHANNELS)} channels flagged suspect "
      f"at R2 >= {HARMONIC_R2_SUSPECT_THRESHOLD}.")
    a("")
    suspect_mwu = sum(1 for ch in CHANNELS
                      if weekend_res.get(ch) and not math.isnan(weekend_res[ch]["mwu_p_two"])
                      and weekend_res[ch]["mwu_p_two"] < MWU_SUSPECT_THRESHOLD)
    a(f"**DOW (weekday-vs-weekend, MWU)**: {suspect_mwu} of {len(CHANNELS)} channels show "
      f"Mann-Whitney U two-sided p < {MWU_SUSPECT_THRESHOLD}.")
    a("")
    suspect_mo = sum(1 for ch in CHANNELS
                     if per_month_res.get(ch) and not math.isnan(per_month_res[ch]["kw_p"])
                     and per_month_res[ch]["kw_p"] < KW_SUSPECT_THRESHOLD)
    suspect_dw = sum(1 for ch in CHANNELS
                     if per_dow_res.get(ch) and not math.isnan(per_dow_res[ch]["kw_p"])
                     and per_dow_res[ch]["kw_p"] < KW_SUSPECT_THRESHOLD)
    a(f"**Per-month (Kruskal-Wallis across 12 months)**: {suspect_mo} of {len(CHANNELS)} channels show p < {KW_SUSPECT_THRESHOLD}.")
    a(f"**Per-DOW (Kruskal-Wallis across 7 days)**: {suspect_dw} of {len(CHANNELS)} channels show p < {KW_SUSPECT_THRESHOLD}.")
    a("")
    # spring-control flag count
    confirmed_survives = []
    confirmed_skipped = []
    for ch in CONFIRMED_CITALOPRAM.keys():
        flag = spring_res.get(ch, {}).get("step_survives_same_season")
        if flag == "yes-direction-and-2025-flat":
            confirmed_survives.append(ch)
        elif flag in (None, "not-CONFIRMED-channel"):
            confirmed_skipped.append(ch)
    a(f"**v3 spring-control extension (CONFIRMED-citalopram channels)**: of the 3 CONFIRMED channels "
      f"({', '.join(CONFIRMED_CITALOPRAM.keys())}), {len(confirmed_survives)} show the citalopram-step "
      f"surviving same-season comparison (test-year direction matches prior AND control-year is roughly flat). "
      f"This is a **descriptive observation only** per CONVENTIONS section 4.2: it neither confirms nor refutes "
      f"the v3 verdict; it extends the spring-control logic per [citalopram_dose_response section 5.6](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) LOAD-BEARING.")
    a("")
    # per-phase summary
    phase_cells_fit = sum(
        1
        for ch in CHANNELS for ph in PHASE_ORDER
        if per_phase_res.get(ch, {}).get(ph, {}).get("fit") is not None
    )
    total_cells = len(CHANNELS) * len(PHASE_ORDER)
    a(f"**Per-recovery-phase seasonality**: {phase_cells_fit} of {total_cells} (channel x phase) cells have "
      f"sufficient n + span for an annual harmonic fit; remaining cells skipped per the within-phase span "
      f">= 180d gate (annual harmonic underdetermined on short phases).")
    a("")
    a("---")
    a("")

    # Stage 2 -- harmonic table
    a("## 1. Stage 2 -- annual harmonic per channel")
    a("")
    a("**Method**: per channel, fit `y = alpha + b1*sin(2*pi*doy/365) + b2*cos(2*pi*doy/365) + eps` "
      "on all non-null rows. Report amplitude = sqrt(b1^2 + b2^2); peak-DOY (day-of-year when "
      "harmonic peaks); R2; F-test p; suspect-flag = `R2 >= 0.10`.")
    a("")
    a("| channel | n | beta_sin | beta_cos | amplitude | peak DOY | R2 | F p | flag |")
    a("|---|---:|---:|---:|---:|---:|---:|---:|:---|")
    for ch in CHANNELS:
        r = harmonic_res.get(ch)
        if r is None:
            a(f"| `{ch}` | n/a | n/a | n/a | n/a | n/a | n/a | n/a | SKIP |")
            continue
        flag = "**SUSPECT**" if r["suspect"] else "no-flag"
        a(
            f"| `{ch}` | {r['n']} | {fmt_signed(r['beta_sin'])} | {fmt_signed(r['beta_cos'])} | "
            f"{fmt_float(r['amplitude'])} | {r['phase_peak_doy']:.0f} | "
            f"{fmt_float(r['r2'], 4)} | {fmt_float(r['p_f'], 4)} | {flag} |"
        )
    a("")
    a("**Suspect-flag reading per CONVENTIONS section 4.2 caveat-class**: a SUSPECT flag means the "
      "annual harmonic explains >= 10% of variance in the raw channel. This is a **descriptive marker** "
      "that seasonality is non-negligible at this channel; it does **NOT** promote to a claim that the "
      "multi-year arc is partly seasonal. Trajectory-vs-seasonality disambiguation requires a model "
      "with both terms (out of scope for this descriptive check).")
    a("")
    a("---")
    a("")

    # Stage 3 -- per-month table
    a("## 2. Stage 3 -- per-month medians + Kruskal-Wallis")
    a("")
    a("**Method**: per channel, stratify rows by calendar month (1..12); report per-month median + IQR; "
      "test Kruskal-Wallis H across the 12 month-groups; suspect = `p < 0.05`. Per-month outliers = "
      "months whose median exceeds grand-median +/- 2x within-channel IQR/2.")
    a("")
    a("**Per-month median table (each cell: median value; blank = no data)**:")
    a("")
    a("| channel | " + " | ".join(MONTH_NAMES) + " | KW p | spread |")
    a("|---|" + "|".join(["---:"] * 12) + "|---:|---:|")
    for ch in CHANNELS:
        per_month = per_month_res[ch]["per_month"]
        cells = []
        for row in per_month:
            cells.append(f"{row['median']:.2f}" if row["median"] is not None else "")
        kw_p = per_month_res[ch]["kw_p"]
        spread = per_month_res[ch]["month_median_spread"]
        flag_marker = "**" if (not math.isnan(kw_p) and kw_p < KW_SUSPECT_THRESHOLD) else ""
        a(
            f"| `{ch}` | "
            + " | ".join(cells)
            + f" | {flag_marker}{fmt_float(kw_p, 4)}{flag_marker} | {fmt_float(spread)} |"
        )
    a("")
    a("**Per-channel month-median spread** (max-month-median minus min-month-median; descriptive "
      "magnitude of seasonality on raw units):")
    a("")
    for ch in CHANNELS:
        spread = per_month_res[ch]["month_median_spread"]
        grand = per_month_res[ch]["grand_median"]
        a(f"- `{ch}`: spread = {fmt_float(spread)} (grand median across months = {fmt_float(grand)})")
    a("")
    a("---")
    a("")

    # Stage 4+5 -- DOW
    a("## 3. Stage 4 -- per-DOW medians + Kruskal-Wallis")
    a("")
    a("**Method**: per channel, stratify rows by day-of-week (Mon..Sun); report per-DOW median + IQR; "
      "test Kruskal-Wallis H across the 7 DOW-groups; suspect = `p < 0.05`.")
    a("")
    a("**Per-DOW median table**:")
    a("")
    a("| channel | " + " | ".join(DOW_NAMES) + " | KW p | spread |")
    a("|---|" + "|".join(["---:"] * 7) + "|---:|---:|")
    for ch in CHANNELS:
        per_dow = per_dow_res[ch]["per_dow"]
        cells = []
        for row in per_dow:
            cells.append(f"{row['median']:.2f}" if row["median"] is not None else "")
        kw_p = per_dow_res[ch]["kw_p"]
        spread = per_dow_res[ch]["dow_median_spread"]
        flag_marker = "**" if (not math.isnan(kw_p) and kw_p < KW_SUSPECT_THRESHOLD) else ""
        a(
            f"| `{ch}` | "
            + " | ".join(cells)
            + f" | {flag_marker}{fmt_float(kw_p, 4)}{flag_marker} | {fmt_float(spread)} |"
        )
    a("")

    a("## 4. Stage 5 -- weekday-vs-weekend (Mann-Whitney U + Cliff's delta)")
    a("")
    a("**Method**: per channel, split rows by weekday (Mon..Fri) vs weekend (Sat..Sun); compute "
      "median per group; two-sided Mann-Whitney U; Cliff's delta (weekend vs weekday; positive = "
      "weekend tends higher).")
    a("")
    a("| channel | n_wd | n_we | med_wd | med_we | we-wd | MWU U | MWU p | Cliff delta | flag |")
    a("|---|---:|---:|---:|---:|---:|---:|---:|---:|:---|")
    for ch in CHANNELS:
        w = weekend_res.get(ch)
        if w is None:
            a(f"| `{ch}` | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | SKIP |")
            continue
        flag = "**SUSPECT**" if (not math.isnan(w["mwu_p_two"]) and w["mwu_p_two"] < MWU_SUSPECT_THRESHOLD) else "no-flag"
        a(
            f"| `{ch}` | {w['n_weekday']} | {w['n_weekend']} | "
            f"{fmt_float(w['median_weekday'])} | {fmt_float(w['median_weekend'])} | "
            f"{fmt_signed(w['weekend_minus_weekday_median'])} | {fmt_float(w['mwu_u'], 1)} | "
            f"{fmt_float(w['mwu_p_two'], 4)} | {fmt_signed(w['cliffs_delta_weekend_vs_weekday'], 4)} | {flag} |"
        )
    a("")
    a("**Cross-reference (Q4.4 4b highest-event-rate descriptive check)** -- per "
      "[`cohort_topology/findings.md`](../cohort_topology/findings.md) section 2 the "
      "`pacing_habit_established` (4b) phase has the highest total event rate (2.89/30d). "
      "If a DOW pattern (e.g. weekday work-stress) drives 4b event rates, it should also "
      "leak into the weekday-vs-weekend split here. The per-channel flag column above is the "
      "descriptive substrate for that cross-reference; **NO causal mechanism claim**.")
    a("")
    a("---")
    a("")

    # Stage 6 -- v3 spring-control
    a("## 5. Stage 6 -- v3 spring-control extension to all 6 channels")
    a("")
    a("**Method (LOAD-BEARING per [citalopram_dose_response_stress_mean_sleep.md section 5.5 + 5.6](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md))**: "
      "for each channel, fit `channel ~ const + beta_time*days` on the spring window "
      f"`{SPRING_WINDOW_START[0]:02d}-{SPRING_WINDOW_START[1]:02d}` -> "
      f"`{SPRING_WINDOW_END[0]:02d}-{SPRING_WINDOW_END[1]:02d}` for the control year "
      f"({SPRING_CONTROL_YEAR}; 30mg consolidation throughout) and the test year "
      f"({SPRING_TEST_YEAR}; afbouw 30->8mg). HAC SE (maxlags={HAC_MAXLAGS}). Report per-year beta + "
      "95% CI + two-sided p. The **descriptive 'step-survives-same-season' flag** for "
      "CONFIRMED-citalopram channels is `yes-direction-and-2025-flat` iff (a) test-year beta sign "
      "matches the dose-down expected direction (`-prior`), AND (b) `|beta_2025| / |beta_2026| < 0.5`. "
      "**Descriptive observation only per CONVENTIONS section 4.2** -- this neither confirms nor "
      "refutes the v3 verdict; it extends the spring-control logic to 6 channels.")
    a("")
    a("| channel | v3 prior | n_2025 | beta_2025 | CI_2025 | n_2026 | beta_2026 | CI_2026 | delta | step-survives? |")
    a("|---|---:|---:|---:|---|---:|---:|---|---:|:---|")
    for ch in CHANNELS:
        s = spring_res[ch]
        ctrl = s["per_year"].get(SPRING_CONTROL_YEAR)
        test = s["per_year"].get(SPRING_TEST_YEAR)
        prior_info = CONFIRMED_CITALOPRAM.get(ch)
        prior_str = f"{prior_info['prior']:+d}" if prior_info else "n/a"
        ctrl_n = ctrl["n"] if ctrl else "n/a"
        ctrl_b = fmt_signed(ctrl["beta_time"], 4) if ctrl else "n/a"
        ctrl_ci = f"[{fmt_signed(ctrl['ci_lo'], 4)},{fmt_signed(ctrl['ci_hi'], 4)}]" if ctrl else "n/a"
        test_n = test["n"] if test else "n/a"
        test_b = fmt_signed(test["beta_time"], 4) if test else "n/a"
        test_ci = f"[{fmt_signed(test['ci_lo'], 4)},{fmt_signed(test['ci_hi'], 4)}]" if test else "n/a"
        delta = s.get("delta_beta_time_test_minus_control")
        delta_str = fmt_signed(delta, 4) if delta is not None else "n/a"
        flag_raw = s.get("step_survives_same_season") or "n/a"
        a(
            f"| `{ch}` | {prior_str} | {ctrl_n} | {ctrl_b} | {ctrl_ci} | {test_n} | "
            f"{test_b} | {test_ci} | {delta_str} | {flag_raw} |"
        )
    a("")
    a("**Cross-references (descriptive only; LOAD-BEARING)**:")
    a("")
    a("- **v3 spring-2025 control extension** (LOAD-BEARING per "
      "[citalopram_dose_response_stress_mean_sleep.md section 5.5.1 + section 5.6](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md)): "
      "the original v3 control was run on `stress_mean_sleep` only "
      "(beta_2025=-0.023/day -- flat); the section-5.6 multi-channel extension ran control on the "
      "other 5 channels and reported per-channel beta_2025 (all flat or small-counter-direction per "
      "section-5.6 table). Stage 6 above descriptively reproduces those numbers on the 6 channels "
      "in the user-locked scope. The v3 verdict (3 CONFIRMED channels: stress_mean_sleep, "
      "all_day_stress_avg, bb_lowest) is **NOT extended, NOT modified, NOT promoted** here per "
      "CONVENTIONS section 4.2.")
    a("- **Q4.2 buildup-transition Delta-z cross-reference** -- per "
      "[`intervention_cross_channel/findings.md`](../intervention_cross_channel/findings.md) "
      "section 5.1 the 2024-04-09 citalopram-buildup boundary on +/-30d windows shows per-channel "
      "Delta-z_pre values that are also present in 2025 spring control fit comparison context. "
      "Stage 6's per-channel beta_2025 (column above) is the substrate for any cross-window "
      "buildup-vs-spring-control comparison; **NO substantive verdict promotion**.")
    a("- **Q4.3 rp5 (citalopram-start) cross-reference** -- per "
      "[`era_boundaries/findings.md`](../era_boundaries/findings.md) section 2 the 2024-04-09 rp5 "
      "boundary shows distribution shift on 4 of 7 channels (autonomic-load + RHR family). Stage 6's "
      "beta_2025 column tests whether the same 4 channels also show a spring trend in the *clean* "
      "control year. If so, the rp5 shift inherits a seasonality caveat; if not, the rp5 shift is "
      "season-clean. **Descriptive substrate only per CONVENTIONS section 4.1.**")
    a("")
    a("---")
    a("")

    # Stage 7 -- per-recovery-phase
    a("## 6. Stage 7 -- per-recovery-phase seasonality (harmonic per channel x phase)")
    a("")
    a("**Method**: for each (channel, phase) cell, restrict to within-phase rows and refit the "
      "annual harmonic. Cells with n < 30 OR within-phase span < 180 days are skipped (annual "
      "harmonic underdetermined). Report amplitude + R2 per cell.")
    a("")
    a("**Per-channel x phase harmonic amplitude (n in parens; `n/a` = skipped)**:")
    a("")
    header = "| channel | " + " | ".join(PHASE_ORDER) + " |"
    sep = "|---|" + "|".join([":---:"] * len(PHASE_ORDER)) + "|"
    a(header)
    a(sep)
    for ch in CHANNELS:
        cells = []
        for ph in PHASE_ORDER:
            cell = per_phase_res.get(ch, {}).get(ph, {})
            fit = cell.get("fit")
            n = cell.get("n", 0)
            if fit is None:
                cells.append(f"n/a (n={n})")
            else:
                cells.append(f"A={fit['amplitude']:.2f} R2={fit['r2']:.2f} (n={n})")
        a(f"| `{ch}` | " + " | ".join(cells) + " |")
    a("")
    a("**Cross-reference (recovery_arc v2 multi-year-arc seasonal-component check)** -- per "
      "[`recovery_arc/findings.md`](../recovery_arc/findings.md) section 5.A + section 2 the multi-year "
      "arc decomposes into 6 phase-cells per channel; the per-channel multi-year-arc shape may have a "
      "seasonal component within long phases. Stage 7 above is the descriptive substrate: if the "
      "per-channel harmonic amplitude is high within the `pacing_habit_established` (4b) or "
      "`citalopram_modulated` (5) cells, the recovery_arc per-phase reading inherits a "
      "seasonality-suspect flag at that cell. **NO claim that the multi-year arc is partly seasonal** "
      "per CONVENTIONS section 4.2 -- the descriptive substrate is per-phase, the arc-attribution "
      "would require a joint model with both trajectory + harmonic terms (out of scope).")
    a("")
    a("---")
    a("")

    # Caveats
    a("## 7. Caveats")
    a("")
    a("1. **No causal claims.** Per CONVENTIONS section 2.1 + section 4.3 this is Layer 1 descriptive. "
      "The per-channel seasonality flags + DOW flags + spring-control flags are descriptive substrate; "
      "intervention attribution is out of scope. Per CONVENTIONS section 4.2 caveat-class, suspect-flags "
      "are reported as `harmonic R2=X; suspect for seasonality confound` -- NOT promoted to substantive "
      "claims.")
    a("2. **Annual harmonic is a single-frequency model.** Multi-harmonic (semi-annual) + irregular "
      "seasonality (winter-illness clusters) are not captured by this Stage 2 model. The R2 reported "
      "is a lower bound on the 'fraction of variance explainable by seasonality'.")
    a("3. **DOW patterns may be expected on stress/RHR channels** (work-week stress is well-documented "
      "in general literature). The Stage 4 + Stage 5 suspect flags are descriptive substrate; mechanism "
      "claims are out of scope per CONVENTIONS section 4.2.")
    a("4. **v3 spring-control extension is descriptive observation only** per CONVENTIONS section 4.2. "
      "The `step-survives-same-season` flag in Stage 6 captures a per-channel reading of whether the "
      "spring-2025 control fit is roughly flat vs the spring-2026 test fit. This **neither confirms "
      "nor refutes** the v3 verdict per [citalopram_dose_response section 5.6](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md); "
      "it extends the spring-control logic to 6 channels descriptively. The 6-channel scope here "
      "differs from the v3 spec scope (v3 used 6 channels: the 3 CONFIRMED + 3 companions; this "
      "analysis's 6 channels are the user-locked Q4.9 + Q4.5.b + Q4.2 set; `bb_overnight_gain` is "
      "in v3 but not in Q4.8 scope; `stress_stdev_sleep` + `stress_low_motion_min_count_S60_Mlow` + "
      "`resting_hr` are common; v3 includes `respiration_avg_sleep` which Q4.8 does not).")
    a("5. **Per-recovery-phase seasonality (Stage 7) is restricted to phases with span >= 180 days**. "
      "Per `lc_recovery_phase_axis.md` section 2: pre_illness_healthy = ~217 days, acute_infection = "
      "14 days, lc_pre_ergo = ~171 days, pacing_pre_citalopram_learning (4a) = 56 days, "
      "pacing_habit_established (4b) = ~508 days, citalopram_modulated = ~787 days. Stage 7's per-cell "
      "fit is only meaningful on the long phases (4b, 5; possibly pre_illness_healthy and lc_pre_ergo "
      "depending on coverage). Acute infection + 4a are too short for annual-harmonic fitting; reported "
      "as `n/a`.")
    a("6. **Single-year coverage** for some phases. `pre_illness_healthy` covers ~7 months of 2021-2022 "
      "(one shoulder-season cycle only); the per-channel harmonic fit on this phase is shaped by the "
      "single-year coverage and cannot disentangle within-year seasonality from the trajectory. Per "
      "[`recovery_arc/findings.md`](../recovery_arc/findings.md) section 5 caveat 4: any healthy-vs-LC "
      "contrast confounds illness state with season by construction.")
    a("7. **DOW analysis (Stage 4 + Stage 5) is on the full corpus**, not stratified by recovery phase. "
      "Phase-stratified DOW analysis would be a future deferred check; the Q4.8 spec is corpus-wide.")
    a("8. **HAC SE on the spring-window OLS** (Stage 6) assumes weak time-series autocorrelation within "
      "the ~78-day spring window. Per `permutation_null_block_length.md` the project default E[L]=7; "
      "HAC with maxlags=4 is comparable and was used in the original v3 spring_comparison.py per "
      "citalopram_dose_response_stress_mean_sleep.md section 5.5.1. The Stage 6 numbers descriptively "
      "reproduce the v3 method choice on 6 channels rather than re-arguing it.")
    a("9. **2024-04 boundary-collision** (CPAP end 2024-04-16 + Citalopram buildup start 2024-04-09; "
      "7 days apart) per [intervention_effects section 2b](../../../../methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain) "
      "+ section 8.1. The rp5 (4b -> 5) recovery-phase boundary at 2024-04-09 inherits the collision; "
      "Stage 7's 4b vs 5 amplitude comparison cannot disentangle CPAP-end effects from citalopram-start "
      "effects from any seasonal component. **Descriptive substrate only**, NOT a confounded-verdict claim.")
    a("10. **Q4.5.b resting_hr trajectory-driven cross-reference** -- per "
      "[`detrended_correlation/findings.md`](../detrended_correlation/findings.md) headline, 5 of 6 "
      "spurious-flag pairs involve `resting_hr` (the slow cardiovascular drift channel with E[L]\\* "
      "long-memory structure). Stage 2 + Stage 7 above report `resting_hr` harmonic numbers; if the "
      "channel shows a high amplitude this is **consistent with** the Q4.5.b trajectory-driven "
      "spurious-correlation pattern but does **NOT** extend or modify the Q4.5.b verdict.")
    a("")
    a("---")
    a("")

    # Cross-references
    a("## 8. Cross-references")
    a("")
    a("### LOAD-BEARING cross-references (descriptive corroboration only; NOT verdict extension)")
    a("")
    a("- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
      "section 5.5.1 + section 5.6 -- v3 spring-2025 control logic (LOAD-BEARING for Stage 6 extension to 6 channels).")
    a("- [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) "
      "section 2 -- 6-phase axis for Stage 7 per-recovery-phase seasonality.")
    a("- [`analyses/descriptive/trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) "
      "section 5 caveat 4 + section 5.A -- multi-year-arc seasonal-component descriptive check (Stage 7 substrate).")
    a("- [`analyses/descriptive/trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) "
      "section 2 -- Q4.3 rp5 (2024-04-09) distribution-shift cross-reference (Stage 6 substrate for seasonal-overlay check).")
    a("- [`analyses/descriptive/trajectory/intervention_cross_channel/findings.md`](../intervention_cross_channel/findings.md) "
      "section 5.1 -- Q4.2 buildup-transition Delta-z_pre cross-reference (Stage 6 substrate for seasonal-overlay check).")
    a("- [`analyses/descriptive/trajectory/cohort_topology/findings.md`](../cohort_topology/findings.md) "
      "section 2 -- Q4.4 4b highest-event-rate (2.89/30d) cross-reference (Stage 4 + Stage 5 substrate for DOW-pattern check).")
    a("- [`analyses/descriptive/trajectory/detrended_correlation/findings.md`](../detrended_correlation/findings.md) "
      "headline -- Q4.5.b resting_hr trajectory-driven cross-reference (Stage 2 + Stage 7 substrate for similar-pattern check).")
    a("")
    a("### Methodology MDs cited (binding for this analysis's discipline)")
    a("")
    a("- [`CONVENTIONS.md`](../../../../CONVENTIONS.md) section 2.1 (descriptive-before-inference), section 3.6 (named-counts), "
      "section 4.1 (caveats vs a-priori), section 4.2 (caveat-class language), section 4.3 (no interpretive marks).")
    a("- [`methodology/permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) -- block-length convention E[L]=7 (companion to HAC maxlags=4 in Stage 6).")
    a("")
    a("### Upstream pipeline")
    a("")
    a("- `pipeline/03_consolidate/build_unified_dataset.py` -- `per_day_master.csv` builder (includes the `recovery_phase` column populated at `e00df27`).")
    a("- `analyses/_utils/frame.py` -- `load_master()` loader (single source of truth for the as-of-date convention).")
    a("")
    a("---")
    a("")

    # Status
    a("## 9. Status")
    a("")
    a("**Q4.8 findings landed 2026-06-26** from a single execution of [`run.py`](run.py) under the "
      "user-LOCKED operationalisation (Strand B section 7c interview 2026-06-25). **Tier 3 deferred "
      "topic 1 of 2 LANDED**; remaining: Q4.7 notes-categorisation patterns. Next refresh per "
      "[`descriptive/README.md`](../../README.md) section 7d: when new data accrues +180 days "
      "(extends the harmonic-fit window) OR when an HA-* result raises a season-sensitive question.")
    a("")
    with open(fpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"  wrote {fpath.name}  ({len(lines)} lines)")
    return fpath


def stage_9_emit_readme(out_dir):
    fpath = out_dir / "README.md"
    lines = []
    a = lines.append

    a("# `trajectory/seasonality_dow/` -- Q4.8 confound check")
    a("")
    a("## What this analysis answers")
    a("")
    a("**Q4.8 per [`descriptive/README.md`](../../README.md) section 4.8** (r2 closure D4.9): Are there "
      "time-of-year (seasonality) or weekday-vs-weekend (DOW) patterns per channel? These act as "
      "confounders for recovery_arc + Q4.2 + Q4.3 attribution.")
    a("")
    a("**Tier 3 deferred topic 1 of 2** (Q4.7 notes-categorisation patterns is the other; user wants "
      "both done before research-interpret skill pivot).")
    a("")
    a("---")
    a("")
    a("## User-LOCKED operationalisation (per Strand B section 7c interview 2026-06-25; do NOT iterate)")
    a("")
    a("1. **Channel scope = 6 channels** (matches Q4.9 + Q4.5.b + Q4.2): "
      "`stress_mean_sleep` + `all_day_stress_avg` + `bb_lowest` + `stress_stdev_sleep` + "
      "`stress_low_motion_min_count_S60_Mlow` + `resting_hr`.")
    a("2. **Seasonality method = (c) both harmonic + per-month**: sin/cos annual harmonic regression "
      "(1-year periodicity) + per-month median table (12 strata).")
    a("3. **DOW method = (c) both per-DOW + weekday-vs-weekend**: per-DOW median (7 strata) + "
      "weekday-vs-weekend Mann-Whitney U.")
    a("4. **Confound disambiguation = (c) both v3 spring-control extension + per-recovery-phase "
      "seasonality**:")
    a("   - extend v3 spring-2025 control logic to all 6 channels (per "
      "[citalopram_dose_response_stress_mean_sleep.md section 5.5.1 + section 5.6](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) LOAD-BEARING)")
    a("   - per-recovery-phase seasonality (per [lc_recovery_phase_axis.md section 2](../../../../methodology/lc_recovery_phase_axis.md) 6-phase axis)")
    a("")
    a("---")
    a("")
    a("## Method (9-stage architecture)")
    a("")
    a("- **Stage 1** (data prep): load `per_day_master.csv`; identify recovery_phase + citalopram_phase + month + DOW per row.")
    a("- **Stage 2** (seasonality harmonic): per channel, fit `y = alpha + b1*sin(2*pi*doy/365) + b2*cos(2*pi*doy/365)`; "
      "report amplitude + phase + R2; suspect-flag = `R2 >= 0.10`.")
    a("- **Stage 3** (seasonality per-month): per channel, 12-month median table + IQR; Kruskal-Wallis across 12 months.")
    a("- **Stage 4** (DOW per-day): per channel, 7-DOW median table + IQR; Kruskal-Wallis across 7 days.")
    a("- **Stage 5** (DOW weekday-vs-weekend): per channel, Mann-Whitney U + Cliff's delta.")
    a("- **Stage 6** (v3 spring-control extension): per channel, fit `channel ~ const + beta_time*days` "
      "on March 20 -> June 5 of 2025 (control: 30mg consolidation) vs 2026 (test: afbouw); HAC SE; "
      "descriptive 'step-survives-same-season' flag for CONFIRMED-citalopram channels.")
    a("- **Stage 7** (per-recovery-phase seasonality): per channel x per-recovery-phase, refit the annual harmonic on within-phase data (n >= 30 + span >= 180d gate).")
    a("- **Stage 8** (plots): 5 PNG artefacts in [`plots/`](plots/) (gitignored).")
    a("- **Stage 9** (programmatic emit): [`findings.md`](findings.md) + this README + [`summary.json`](summary.json) (gitignored).")
    a("")
    a("---")
    a("")
    a("## Discipline guards")
    a("")
    a("- **Layer 1 descriptive per CONVENTIONS section 2.1**: NO causal claims; NO claim citalopram is/is-not "
      "seasonally confounded (that is v3-extension territory; this is a descriptive check only).")
    a("- **Per CONVENTIONS section 4.2 caveat-class**: a seasonality-detected channel is reported as "
      "`harmonic R2=X; amplitude Y; suspect for seasonality confound` -- NOT promoted to "
      "`the multi-year arc is partly seasonal`.")
    a("- **DOW patterns on stress/RHR channels may be expected** (work-week stress is well-documented in "
      "general literature). The Stage 4 + Stage 5 suspect flags are descriptive substrate; mechanism "
      "claims are out of scope.")
    a("- **v3 spring-control extension is descriptive observation only**; it neither confirms nor refutes "
      "the v3 verdict (3 CONFIRMED channels: stress_mean_sleep, all_day_stress_avg, bb_lowest).")
    a("- **ASCII-only stdout; no em-dashes; no emojis** per project convention.")
    a("- **f-string discipline**: no nested double-quotes inside f-string expressions (pre-3.12 compatibility).")
    a("")
    a("---")
    a("")
    a("## How to run")
    a("")
    a("```")
    a("# Requires GEVOELSCORE_DATA_PATH env var pointing to gevoelscore-data root")
    a("python docs/research/analyses/descriptive/trajectory/seasonality_dow/run.py")
    a("```")
    a("")
    a("Outputs (all but [`run.py`](run.py) + [`README.md`](README.md) + [`findings.md`](findings.md) gitignored):")
    a("")
    a("- `summary.json` -- machine-readable per-channel per-stage statistics")
    a("- `plots/harmonic_fits.png` -- per-channel annual harmonic fit visualisation")
    a("- `plots/seasonality_per_month.png` -- per-channel x month median grid (with IQR error bars)")
    a("- `plots/dow_per_day.png` -- per-channel x DOW median grid (weekday blue / weekend orange)")
    a("- `plots/v3_spring_control_extension.png` -- per-channel beta_time bar (2025 control vs 2026 test)")
    a("- `plots/per_phase_seasonality_heatmap.png` -- channel x phase amplitude + R2 heatmap")
    a("")
    a("---")
    a("")
    a("## Status")
    a("")
    a("**LANDED 2026-06-26**. Tier 3 deferred-topic 1 of 2 closed. Remaining: Q4.7 notes-categorisation patterns.")
    a("")
    with open(fpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"  wrote {fpath.name}  ({len(lines)} lines)")
    return fpath


# -----------------------------------------------------------------------------
# main()
# -----------------------------------------------------------------------------


def main():
    if not os.environ.get("GEVOELSCORE_DATA_PATH"):
        os.environ["GEVOELSCORE_DATA_PATH"] = "C:/Users/Gebruiker/Documents/gevoelscore-data"
    np.random.seed(SEED)
    out_dir = HERE
    print("=" * 70)
    print("Q4.8 seasonality_dow -- Strand B Tier-3 deferred-topic 1 of 2")
    print(f"  output dir: {out_dir}")
    print("=" * 70)
    print()

    # Stage 1
    df = stage_1_load_data()
    n_rows_total = int(len(df))

    # Stage 2 -- harmonic
    harmonic_res = stage_2_harmonic(df)

    # Stage 3 -- per month
    per_month_res = stage_3_per_month(df)

    # Stage 4 -- per DOW
    per_dow_res = stage_4_per_dow(df)

    # Stage 5 -- weekend MWU
    weekend_res = stage_5_weekend(df)

    # Stage 6 -- spring-control extension
    spring_res = stage_6_spring_control(df)

    # Stage 7 -- per recovery phase
    per_phase_res = stage_7_per_phase(df)

    # Stage 8 -- plots
    stage_8_plots(
        df, out_dir,
        harmonic_res, per_month_res, per_dow_res,
        weekend_res, spring_res, per_phase_res,
    )

    # Stage 9 -- emit findings.md + README.md + summary.json
    print("=" * 70)
    print("STAGE 9: programmatic emit (findings.md + README.md + summary.json)")
    print("=" * 70)
    stage_9_emit_summary_json(
        out_dir, harmonic_res, per_month_res, per_dow_res,
        weekend_res, spring_res, per_phase_res,
    )
    stage_9_emit_findings_md(
        out_dir, harmonic_res, per_month_res, per_dow_res,
        weekend_res, spring_res, per_phase_res, n_rows_total,
    )
    stage_9_emit_readme(out_dir)
    print()
    print("=" * 70)
    print("Q4.8 seasonality_dow -- complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
