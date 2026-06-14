"""
Spring-comparison test for the citalopram dose-response result.

Sibling to dose_response.py. Tests the seasonality alibi raised by
Sensitivity F in dose_response.py: if "spring is doing the work" rather
than "dose-down is doing the work", then OTHER spring periods (without
afbouw) should show a similar declining trajectory in stress_mean_sleep.

For each year 2022-2026, fit stress_mean_sleep ~ beta_0 + beta_time * days
across the calendar window March 20 -> June 5 (same window as the afbouw).
Compare beta_time across years with HAC SE.

Cleanest comparison:
  - 2025: same dose (30mg consolidation throughout), late-LC, no other interventions
          starting. THE control year.
  - 2024: confounded -- citalopram-buildup 2024-04-09 and CPAP-end 2024-04-16
          both inside the window.
  - 2023: mid-LC, steep recovery slope era; usable but messy.
  - 2022: spans pre-corona / corona-infection / LC-onset; NOT a clean control,
          included for visual completeness only.

Run:
    GEVOELSCORE_DATA_PATH=C:/Users/Gebruiker/Documents/gevoelscore-data python spring_comparison.py
"""

from pathlib import Path
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


DATA = Path(os.environ.get("GEVOELSCORE_DATA_PATH",
                           r"C:\Users\Gebruiker\Documents\gevoelscore-data"))
if not DATA.exists():
    print(f"ERROR: data path not found: {DATA}", file=sys.stderr)
    sys.exit(1)

OUT = DATA / "analyses" / "intervention_effects"
(OUT / "plots").mkdir(parents=True, exist_ok=True)


# Same calendar window as the afbouw: March 20 -> June 5
WINDOW_MONTH_DAY_START = (3, 20)
WINDOW_MONTH_DAY_END = (6, 5)
YEARS = [2022, 2023, 2024, 2025, 2026]

# Annotation: which year is the cleanest control / confounded with what
YEAR_LABELS = {
    2022: "early-LC (NOT clean: window spans corona->LC onset)",
    2023: "mid-LC (steep recovery slope era)",
    2024: "confounded: citalopram-buildup 04-09 + CPAP-end 04-16 IN window",
    2025: "30mg consolidation throughout, late-LC -- CLEAN CONTROL",
    2026: "afbouw 30->8mg (TEST year)",
}

HAC_MAXLAGS = 4

master = pd.read_csv(DATA / "unified" / "per_day_master.csv", parse_dates=["date"])
master = master.set_index("date").sort_index()


def fit_year_slope(year):
    """Fit stress_mean_sleep ~ b0 + b_time * days for the March 20 -> June 5
    window of `year`. Returns dict with beta, HAC SE, CI, p, n, window."""
    start = pd.Timestamp(year=year, month=WINDOW_MONTH_DAY_START[0], day=WINDOW_MONTH_DAY_START[1])
    end = pd.Timestamp(year=year, month=WINDOW_MONTH_DAY_END[0], day=WINDOW_MONTH_DAY_END[1])
    sub = master.loc[start:end, ["stress_mean_sleep"]].copy()
    sub = sub.dropna()
    if len(sub) < 10:
        return None
    sub["days"] = (sub.index - start).days.astype(float)

    X = pd.DataFrame({"const": 1.0, "time": sub["days"].values}, index=sub.index)
    y = sub["stress_mean_sleep"].values
    fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_MAXLAGS})
    beta = float(fit.params["time"])
    se = float(fit.bse["time"])
    ci_lo, ci_hi = (float(c) for c in fit.conf_int(alpha=0.05).loc["time"])
    p_two = float(fit.pvalues["time"])

    return {
        "year": year,
        "n": len(sub),
        "window_start": start.date(),
        "window_end": end.date(),
        "stress_first": float(sub["stress_mean_sleep"].iloc[0]),
        "stress_last": float(sub["stress_mean_sleep"].iloc[-1]),
        "stress_mean": float(sub["stress_mean_sleep"].mean()),
        "beta_time": beta,
        "hac_se": se,
        "ci_lo": ci_lo,
        "ci_hi": ci_hi,
        "p_two_sided": p_two,
        "label": YEAR_LABELS[year],
        "series": sub,
        "fit_intercept": float(fit.params["const"]),
    }


# ---------- Run per-year fits ----------

print(f"Spring-comparison: window {WINDOW_MONTH_DAY_START[0]:02d}-{WINDOW_MONTH_DAY_START[1]:02d}"
      f" to {WINDOW_MONTH_DAY_END[0]:02d}-{WINDOW_MONTH_DAY_END[1]:02d}, "
      f"HAC maxlags = {HAC_MAXLAGS}")
print()
results = []
for y in YEARS:
    r = fit_year_slope(y)
    if r is None:
        print(f"  {y}: SKIP (insufficient data)")
        continue
    results.append(r)
    print(f"  {y}  n={r['n']:>3}  "
          f"mean={r['stress_mean']:>5.2f}  "
          f"first={r['stress_first']:>5.2f}  last={r['stress_last']:>5.2f}  "
          f"beta_time={r['beta_time']:+.4f} per day  "
          f"95% CI=[{r['ci_lo']:+.4f},{r['ci_hi']:+.4f}]  "
          f"p={r['p_two_sided']:.4f}")
    print(f"        {r['label']}")
print()


# ---------- Comparison: dose-response model's beta_dose vs spring-only beta_time ----------

beta_2026 = next(r for r in results if r["year"] == 2026)["beta_time"]
beta_2025 = next((r for r in results if r["year"] == 2025), {}).get("beta_time")
beta_2023 = next((r for r in results if r["year"] == 2023), {}).get("beta_time")

print("KEY COMPARISON")
print(f"  2026 (afbouw)  beta_time = {beta_2026:+.4f} per day "
      f"(implied stress change across 77d: {beta_2026 * 77:+.2f} points)")
if beta_2025 is not None:
    print(f"  2025 (control) beta_time = {beta_2025:+.4f} per day "
          f"(implied stress change across 77d: {beta_2025 * 77:+.2f} points)")
    delta = beta_2026 - beta_2025
    print(f"  Delta 2026 vs 2025: {delta:+.4f} per day "
          f"({delta * 77:+.2f} points across 77d)")
if beta_2023 is not None:
    print(f"  2023 (mid-LC)  beta_time = {beta_2023:+.4f} per day "
          f"(implied stress change across 77d: {beta_2023 * 77:+.2f} points)")

# Reading rules:
# - If 2025 beta_time is comparable to 2026 -> seasonality alibi survives.
# - If 2025 beta_time is much less negative (or positive) than 2026 -> seasonality alibi weakens.
# - The dose-response signal in 2026 should be ATTRIBUTABLE to dose if 2025 doesn't show
#   a similar drop.


# ---------- Plots ----------

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel L: overlaid spring trajectories
ax_l = axes[0]
colors = {2022: "#aab", 2023: "#a7a", 2024: "#a73", 2025: "#37a", 2026: "#a37"}
for r in results:
    s = r["series"]
    # Use day-of-spring as x-axis so years overlay
    days_x = (s.index - pd.Timestamp(year=r["year"], month=3, day=20)).days
    is_test = r["year"] == 2026
    lw = 2.5 if is_test else 1.5
    alpha = 0.9 if is_test else 0.55
    label = f"{r['year']} (n={r['n']}, beta={r['beta_time']:+.3f})"
    ax_l.plot(days_x, s["stress_mean_sleep"], "o-", color=colors[r["year"]],
              ms=3, lw=lw, alpha=alpha, label=label)
    # Add the fitted line
    x_fit = np.arange(0, days_x.max() + 1)
    y_fit = r["fit_intercept"] + r["beta_time"] * x_fit
    ax_l.plot(x_fit, y_fit, "-", color=colors[r["year"]], lw=1.0, alpha=0.4)
ax_l.set_xlabel("Days from March 20 (year-aligned)")
ax_l.set_ylabel("stress_mean_sleep")
ax_l.set_title("Spring trajectories (March 20 -> June 5) per year")
ax_l.legend(fontsize=8, loc="upper left")
ax_l.grid(True, alpha=0.3)

# Panel R: coefficient panel -- beta_time per year with 95% CI
ax_r = axes[1]
xs = [r["year"] for r in results]
ys = [r["beta_time"] for r in results]
yerr_lo = [r["beta_time"] - r["ci_lo"] for r in results]
yerr_hi = [r["ci_hi"] - r["beta_time"] for r in results]
bar_colors = [colors[r["year"]] for r in results]
for x, y, lo, hi, c in zip(xs, ys, yerr_lo, yerr_hi, bar_colors):
    ax_r.errorbar(x, y, yerr=[[lo], [hi]], fmt="o", color=c, capsize=4, ms=10)
ax_r.axhline(0, color="gray", linestyle="--", alpha=0.5, label="beta_time = 0")
ax_r.set_xlabel("Year")
ax_r.set_ylabel("beta_time (stress per day)")
ax_r.set_title("Per-year spring slope with 95% HAC CI")
ax_r.set_xticks(xs)
ax_r.grid(True, alpha=0.3, axis="y")
ax_r.legend(fontsize=8)

fig.suptitle("Spring-comparison: does stress_mean_sleep generally rise / fall across spring?",
             fontsize=12)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plot_path = OUT / "plots" / "spring_comparison.png"
plt.savefig(plot_path, dpi=100)
plt.close()
print()
print(f"Wrote plot: {plot_path}")

# Summary CSV
summary_rows = [
    {k: v for k, v in r.items() if k not in ("series",)}
    for r in results
]
summary_df = pd.DataFrame(summary_rows)
summary_path = OUT / "spring_comparison_summary.csv"
summary_df.to_csv(summary_path, index=False)
print(f"Wrote summary: {summary_path}")


# ---------- Read-out ----------

print()
print("=" * 70)
print("READOUT")
print("=" * 70)
if beta_2025 is not None:
    if beta_2025 > 0 and beta_2026 <= 0:
        verdict = ("Seasonality alibi WEAKENS: 2025 (clean control) rises across "
                   "spring; 2026 (afbouw) doesn't. The 2026 'flatness or descent' "
                   "is the data fingerprint expected if dose-down attenuates an "
                   "otherwise-rising spring trend.")
    elif beta_2025 < 0 and beta_2026 < 0:
        if abs(beta_2026 - beta_2025) < 0.05:
            verdict = ("Seasonality alibi SURVIVES: 2025 and 2026 show similar "
                       "downward spring slopes. Dose-down is NOT distinguishable "
                       "from the underlying spring trend on this corpus.")
        else:
            verdict = (f"PARTIAL: both years trend downward but 2026 is "
                       f"{abs(beta_2026 - beta_2025):.4f} per day steeper than 2025. "
                       "The extra steepness is consistent with a dose-effect "
                       "on top of seasonality.")
    elif beta_2025 > 0 and beta_2026 > 0:
        if beta_2025 > beta_2026:
            verdict = ("Mixed: both years rise; 2026 rises LESS than 2025. The "
                       "attenuation in 2026 is consistent with dose-down "
                       "counteracting an otherwise-rising spring trend.")
        else:
            verdict = ("PUZZLE: both years rise and 2026 rises MORE than 2025. "
                       "Dose-down does NOT appear to attenuate spring rise.")
    else:
        verdict = "Atypical combination; read the numbers above directly."
    print(verdict)
print()
