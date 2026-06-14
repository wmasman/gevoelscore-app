"""
Symmetric buildup-phase falsification check for the citalopram dose-response.

Sibling to dose_response.py + spring_comparison.py. Tests the symmetric
prediction of the dose-response hypothesis: if lowering citalopram dose
in the afbouw lowers stress_mean_sleep, then RAISING citalopram dose in
the buildup should RAISE stress_mean_sleep. Same beta_dose > 0 sign in
both phases (because the regressor is plasma mg).

Buildup window: 2024-04-09 (start 10mg) -> 2024-06-19 (last day before
30mg consolidation phase starts 2024-06-20). 72 days.

Buildup dose schedule (from annotations.yaml verified earlier):
  - 2024-04-09: 0 -> 10mg  (citalopram first dose; phase 1)
  - 2024-05-05: 10 -> 20mg (phase 2 starts; verified from notes 30-04-2024)
  - End of window 2024-06-19 (phase 3 / consolidation starts next day)

CONFOUND (binding): CPAP-end at 2024-04-16 is 7 days INSIDE the buildup
window. CPAP-off would tend to RAISE nighttime stress (worse sleep
apnea after stopping CPAP). Both interventions point the same direction
on stress_mean_sleep in the first ~14 days, indistinguishable here.

We fit three specs:
  S1. Full buildup window, raw       -- inherits the CPAP-end confound
  S2. Post-CPAP-buffer (start 2024-05-01 onward, dropping the first 22d) --
      first day after CPAP-equilibration window of 14d from CPAP-end
  S3. 2025 calendar-window control (2025-04-09 -> 2025-06-19) at 30mg
      consolidation; same calendar slot, no buildup -- the seasonality
      sanity check at the buildup-calendar position

Run:
    GEVOELSCORE_DATA_PATH=C:/Users/Gebruiker/Documents/gevoelscore-data python buildup_check.py
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


# ---------- Buildup PK model ----------
# Initial dose 0 (no citalopram before 2024-04-09). Mirror image of afbouw.

BUILDUP_START = pd.Timestamp("2024-04-09")
BUILDUP_END = pd.Timestamp("2024-06-19")
CPAP_END = pd.Timestamp("2024-04-16")
POST_CPAP_BUFFER_DAYS = 14
POST_CPAP_START = CPAP_END + pd.Timedelta(days=POST_CPAP_BUFFER_DAYS + 1)

INITIAL_DOSE_MG = 0.0
DOSE_STEPS_BUILDUP = [
    (pd.Timestamp("2024-04-09"), +10.0),  # 0 -> 10mg
    (pd.Timestamp("2024-05-05"), +10.0),  # 10 -> 20mg
]

T_HALF_HOURS = 35.0
T_HALF_DAYS = T_HALF_HOURS / 24.0
DECAY_K = np.log(2.0) / T_HALF_DAYS
HAC_MAXLAGS = 4


def dose_plasma_mg(d, initial=INITIAL_DOSE_MG, steps=DOSE_STEPS_BUILDUP):
    val = initial
    for step_date, delta in steps:
        if d >= step_date:
            days_since = (d - step_date).days
            val += delta * (1.0 - np.exp(-DECAY_K * days_since))
    return val


master = pd.read_csv(DATA / "unified" / "per_day_master.csv", parse_dates=["date"])
master = master.set_index("date").sort_index()


def fit_buildup_spec(start, end, label, drop_pre_cpap=False):
    """Fit stress_mean_sleep ~ b0 + b_dose*plasma + b_time*days for the
    given window. drop_pre_cpap: if True, drop rows with date < POST_CPAP_START
    even if they fall inside [start, end]."""
    win = master.loc[start:end, ["stress_mean_sleep", "is_crash"]].copy()
    if drop_pre_cpap:
        win = win.loc[win.index >= POST_CPAP_START]
    win = win.dropna(subset=["stress_mean_sleep"])
    if len(win) < 10:
        return None
    win["days"] = (win.index - start).days.astype(float)
    win["dose_plasma_mg"] = [dose_plasma_mg(d) for d in win.index]
    X = pd.DataFrame({
        "const": 1.0, "dose": win["dose_plasma_mg"].values, "time": win["days"].values,
    }, index=win.index)
    y = win["stress_mean_sleep"].values
    fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_MAXLAGS})
    beta_dose = float(fit.params["dose"])
    se_dose = float(fit.bse["dose"])
    ci = fit.conf_int(alpha=0.05).loc["dose"]
    p_two = float(fit.pvalues["dose"])
    # One-sided H1: beta_dose > 0 (higher dose -> higher stress, mirror of afbouw)
    p_one = p_two / 2.0 if beta_dose > 0 else 1.0 - p_two / 2.0

    # Simple no-dose linear-time slope for comparison
    X_time = pd.DataFrame({"const": 1.0, "time": win["days"].values}, index=win.index)
    fit_time = sm.OLS(y, X_time).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_MAXLAGS})
    beta_time_only = float(fit_time.params["time"])

    n_crash = int((win["is_crash"] == True).sum())

    return {
        "label": label, "n": len(win),
        "window_start": win.index.min().date(), "window_end": win.index.max().date(),
        "stress_first": float(win["stress_mean_sleep"].iloc[0]),
        "stress_last": float(win["stress_mean_sleep"].iloc[-1]),
        "stress_mean": float(win["stress_mean_sleep"].mean()),
        "beta_dose": beta_dose, "hac_se_dose": se_dose,
        "ci_lo_dose": float(ci[0]), "ci_hi_dose": float(ci[1]),
        "hac_p_two_sided_dose": p_two, "hac_p_one_sided_dose": p_one,
        "beta_time_with_dose": float(fit.params["time"]),
        "beta_time_only_naive": beta_time_only,
        "n_crash": n_crash,
        "series": win,
    }


def fit_control_2025(start, end, label):
    """2025 calendar-window control: same calendar slot, dose constant 30mg
    throughout, no buildup. Fit stress ~ b0 + b_time only (dose is constant
    so b_dose is unidentifiable)."""
    s = start.replace(year=2025)
    e = end.replace(year=2025)
    win = master.loc[s:e, ["stress_mean_sleep", "is_crash"]].dropna(subset=["stress_mean_sleep"])
    if len(win) < 10:
        return None
    win["days"] = (win.index - s).days.astype(float)
    X = pd.DataFrame({"const": 1.0, "time": win["days"].values}, index=win.index)
    y = win["stress_mean_sleep"].values
    fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_MAXLAGS})
    beta_time = float(fit.params["time"])
    ci = fit.conf_int(alpha=0.05).loc["time"]
    return {
        "label": label, "n": len(win),
        "window_start": win.index.min().date(), "window_end": win.index.max().date(),
        "stress_first": float(win["stress_mean_sleep"].iloc[0]),
        "stress_last": float(win["stress_mean_sleep"].iloc[-1]),
        "stress_mean": float(win["stress_mean_sleep"].mean()),
        "beta_time": beta_time,
        "ci_lo": float(ci[0]), "ci_hi": float(ci[1]),
        "series": win,
    }


# ---------- Run all specs ----------

print(f"Buildup window: {BUILDUP_START.date()} -> {BUILDUP_END.date()}  "
      f"(72 days; CPAP-end at {CPAP_END.date()} is INSIDE)")
print()

s1 = fit_buildup_spec(BUILDUP_START, BUILDUP_END, "S1: full buildup (raw, CPAP-confounded)")
s2 = fit_buildup_spec(BUILDUP_START, BUILDUP_END,
                      f"S2: post-CPAP-buffer (drop pre {POST_CPAP_START.date()}, "
                      f"{POST_CPAP_BUFFER_DAYS}d after CPAP-end)",
                      drop_pre_cpap=True)
s3 = fit_control_2025(BUILDUP_START, BUILDUP_END,
                      "S3: 2025 calendar-window control (30mg throughout)")


def report_buildup(r):
    print(f"  {r['label']}")
    print(f"    n={r['n']}  window {r['window_start']} -> {r['window_end']}")
    print(f"    stress first={r['stress_first']:.2f}  last={r['stress_last']:.2f}  "
          f"mean={r['stress_mean']:.2f}  n_crash={r['n_crash']}")
    print(f"    beta_dose (per mg plasma)  = {r['beta_dose']:+.4f}")
    print(f"      HAC 95% CI               = [{r['ci_lo_dose']:+.4f}, "
          f"{r['ci_hi_dose']:+.4f}]")
    print(f"      one-sided p (H1: beta>0) = {r['hac_p_one_sided_dose']:.4f}")
    print(f"    beta_time (with dose)      = {r['beta_time_with_dose']:+.4f} per day")
    print(f"    beta_time (no-dose naive)  = {r['beta_time_only_naive']:+.4f} per day")
    print()


def report_control(r):
    print(f"  {r['label']}")
    print(f"    n={r['n']}  window {r['window_start']} -> {r['window_end']}")
    print(f"    stress first={r['stress_first']:.2f}  last={r['stress_last']:.2f}  "
          f"mean={r['stress_mean']:.2f}")
    print(f"    beta_time = {r['beta_time']:+.4f} per day  "
          f"(95% CI [{r['ci_lo']:+.4f}, {r['ci_hi']:+.4f}])")
    print()


print("BUILDUP RESULTS")
report_buildup(s1)
if s2:
    report_buildup(s2)
print("CONTROL (same calendar slot, 2025)")
if s3:
    report_control(s3)


# ---------- Symmetry comparison with afbouw 2026 ----------

print()
print("=" * 70)
print("SYMMETRY READOUT")
print("=" * 70)
print()
print("Afbouw 2026 (from dose_response.py): beta_dose = +0.246 per mg "
      "(p_one = 0.144, CI [-0.209, +0.702])")
print()
print(f"Buildup 2024 (S1, raw):              beta_dose = {s1['beta_dose']:+.4f} per mg "
      f"(p_one = {s1['hac_p_one_sided_dose']:.4f}, "
      f"CI [{s1['ci_lo_dose']:+.4f}, {s1['ci_hi_dose']:+.4f}])")
if s2:
    print(f"Buildup 2024 (S2, post-CPAP):        beta_dose = {s2['beta_dose']:+.4f} per mg "
          f"(p_one = {s2['hac_p_one_sided_dose']:.4f}, "
          f"CI [{s2['ci_lo_dose']:+.4f}, {s2['ci_hi_dose']:+.4f}])")
print()
sign_match = (
    "MATCH" if s1["beta_dose"] > 0 else "MISMATCH (counter-prior)"
)
print(f"Sign of buildup beta_dose vs afbouw beta_dose (both should be > 0): {sign_match}")
print()


# ---------- Plot ----------

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel L: buildup S1 trajectory + fitted lines + 2025 control overlay
ax = axes[0]
s_s1 = s1["series"]
days_x_s1 = (s_s1.index - BUILDUP_START).days
ax.plot(days_x_s1, s_s1["stress_mean_sleep"], "o-", color="#a73", ms=3, lw=1.5,
        alpha=0.8, label=f"2024 buildup (n={s1['n']})")
# Overlay PK dose on secondary axis
ax_dose = ax.twinx()
ax_dose.plot(days_x_s1, s_s1["dose_plasma_mg"], "-", color="#a33", lw=2, alpha=0.6,
             label="dose_plasma_mg (PK)")
ax_dose.set_ylabel("citalopram plasma (mg)", color="#a33")
ax_dose.tick_params(axis="y", labelcolor="#a33")

# CPAP-end marker
cpap_x = (CPAP_END - BUILDUP_START).days
ax.axvline(cpap_x, color="#555", linestyle=":", alpha=0.7, label=f"CPAP-end (day {cpap_x})")
# Post-CPAP buffer start
buf_x = (POST_CPAP_START - BUILDUP_START).days
ax.axvline(buf_x, color="#555", linestyle="--", alpha=0.4,
           label=f"S2 buffer start (day {buf_x})")

# 2025 control overlay
if s3:
    s_s3 = s3["series"]
    days_x_s3 = (s_s3.index - s_s3.index.min()).days
    ax.plot(days_x_s3, s_s3["stress_mean_sleep"], "o-", color="#37a", ms=3, lw=1.2,
            alpha=0.55, label=f"2025 control (n={s3['n']})")

ax.set_xlabel("Days from 2024-04-09 (year-aligned with 2025 control)")
ax.set_ylabel("stress_mean_sleep")
ax.set_title("Buildup 2024 + CPAP-end + 2025 calendar control")
lines_l, labels_l = ax.get_legend_handles_labels()
lines_r, labels_r = ax_dose.get_legend_handles_labels()
ax.legend(lines_l + lines_r, labels_l + labels_r, fontsize=7, loc="upper left")
ax.grid(True, alpha=0.3)

# Panel R: symmetry coefficient panel
ax2 = axes[1]
labels = ["Afbouw 2026\n(dose_response.py)",
          "Buildup S1\n(raw)",
          "Buildup S2\n(post-CPAP)"]
betas = [+0.2463, s1["beta_dose"], s2["beta_dose"] if s2 else np.nan]
ci_lo = [-0.2090, s1["ci_lo_dose"], s2["ci_lo_dose"] if s2 else np.nan]
ci_hi = [+0.7017, s1["ci_hi_dose"], s2["ci_hi_dose"] if s2 else np.nan]
xs = np.arange(len(labels))
colors_panel = ["#a37", "#a73", "#7a3"]
for x, b, lo, hi, c in zip(xs, betas, ci_lo, ci_hi, colors_panel):
    if np.isnan(b):
        continue
    ax2.errorbar(x, b, yerr=[[b - lo], [hi - b]], fmt="o", color=c, capsize=4, ms=10)
ax2.axhline(0, color="gray", linestyle="--", alpha=0.5, label="beta_dose = 0")
ax2.set_xticks(xs)
ax2.set_xticklabels(labels, fontsize=9)
ax2.set_ylabel("beta_dose (per mg of plasma)")
ax2.set_title("Symmetric prediction: beta_dose > 0 in BOTH phases")
ax2.grid(True, alpha=0.3, axis="y")
ax2.legend(fontsize=8)

fig.suptitle("Symmetric buildup-phase check of the dose-response", fontsize=12)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plot_path = OUT / "plots" / "buildup_check.png"
plt.savefig(plot_path, dpi=100)
plt.close()
print(f"Wrote plot: {plot_path}")

# CSV summary
rows = []
for r in [s1, s2]:
    if r is None:
        continue
    row = {k: v for k, v in r.items() if k != "series"}
    rows.append(row)
if s3:
    rows.append({k: v for k, v in s3.items() if k != "series"})
pd.DataFrame(rows).to_csv(OUT / "buildup_check_summary.csv", index=False)
print(f"Wrote summary: {OUT / 'buildup_check_summary.csv'}")
