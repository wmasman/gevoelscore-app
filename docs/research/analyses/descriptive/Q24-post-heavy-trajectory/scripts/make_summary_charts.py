"""Generate the summary charts for descriptive_findings_summary.md.

Reads the (gitignored) output CSVs produced by audit.py + detrend.py and writes
PNGs into ../charts/ (also gitignored, regenerable). Idempotent; no data mutation.

Run from the analysis folder:
    python scripts/make_summary_charts.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

RANDOM_SEED = 20260715  # matches audit.py bootstrap seed

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUT = os.path.join(BASE, "output")
CHARTS = os.path.join(BASE, "charts")
os.makedirs(CHARTS, exist_ok=True)

# Master per-day data (gitignored, outside the repo) — same resolution as audit.py
DATA_PATH = os.environ.get(
    "GEVOELSCORE_DATA_PATH", "C:/Users/Gebruiker/Documents/gevoelscore-data"
)
MASTER_CSV = os.path.join(DATA_PATH, "unified", "per_day_master.csv")

traj = pd.read_csv(os.path.join(OUT, "per_day_trajectories.csv"))
summ = pd.read_csv(os.path.join(OUT, "trajectory_summary.csv"))

C_SUCCESS = "#3a7ca5"   # calm blue
C_FAILURE = "#c1543a"   # warm rust
C_SLEEP = "#5a8f3d"     # green
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def dtraj(outcome, window, pool, arm="raw"):
    d = traj[(traj.outcome == outcome) & (traj.window == window)
             & (traj.pool == pool) & (traj.arm_type == arm)].sort_values("day_k")
    return d


# ---- Chart 1: gevoelscore success vs failure (the headline) ----
fig, ax = plt.subplots(figsize=(7.2, 4.4))
for pool, color, label in [
    ("compensatory_success", C_SUCCESS, "compensatory-success (no crash in window, n=43)"),
    ("compensatory_failure", C_FAILURE, "compensatory-failure (crash in window, n=9)"),
]:
    d = dtraj("gevoelscore", 5, pool)
    ax.plot(d.day_k, d.delta, "-o", color=color, label=label, lw=2)
    ax.fill_between(d.day_k, d.delta_ci_lo, d.delta_ci_hi, color=color, alpha=0.15)
ax.axhline(0, color="k", lw=0.8)
ax.set_xlabel("days after heavy episode-end (k)")
ax.set_ylabel("gevoelscore delta vs matched-ordinary")
ax.set_title("Felt-state trajectory: the pool that crashes stays low; the pool that\n"
             "does not crash recovers toward baseline (+5d window, raw)", fontsize=11)
ax.set_xticks([1, 2, 3, 4, 5])
ax.legend(fontsize=8, loc="lower right")
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "01_gevoelscore_success_vs_failure.png"), dpi=130)
plt.close(fig)

# ---- Chart 2: activity + sleep compensation (success pool, +5d) ----
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
d = dtraj("total_steps", 5, "compensatory_success")
axes[0].plot(d.day_k, d.delta, "-o", color=C_SUCCESS, lw=2)
axes[0].fill_between(d.day_k, d.delta_ci_lo, d.delta_ci_hi, color=C_SUCCESS, alpha=0.15)
axes[0].axhline(0, color="k", lw=0.8)
axes[0].set_title("Steps drop below matched-ordinary\n(behavioural compensation)", fontsize=10)
axes[0].set_xlabel("days after (k)"); axes[0].set_ylabel("total_steps delta")
axes[0].set_xticks([1, 2, 3, 4, 5])

d = dtraj("sleep_duration_min", 5, "compensatory_success")
axes[1].plot(d.day_k, d.delta, "-o", color=C_SLEEP, lw=2)
axes[1].fill_between(d.day_k, d.delta_ci_lo, d.delta_ci_hi, color=C_SLEEP, alpha=0.15)
axes[1].axhline(0, color="k", lw=0.8)
axes[1].set_title("Sleep runs longer than matched-ordinary\n(rebound)", fontsize=10)
axes[1].set_xlabel("days after (k)"); axes[1].set_ylabel("sleep_duration_min delta")
axes[1].set_xticks([1, 2, 3, 4, 5])
fig.suptitle("Compensatory-success pool: less activity, more sleep after a heavy episode-end (+5d, raw)",
             fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(os.path.join(CHARTS, "02_activity_sleep_compensation.png"), dpi=130)
plt.close(fig)

# ---- Chart 3: autonomic divergence between pools (all_day_stress_avg, +5d) ----
fig, ax = plt.subplots(figsize=(7.2, 4.4))
for pool, color, label in [
    ("compensatory_success", C_SUCCESS, "success: stress trends BELOW matched-ordinary"),
    ("compensatory_failure", C_FAILURE, "failure: stress trends ABOVE matched-ordinary"),
]:
    d = dtraj("all_day_stress_avg", 5, pool)
    ax.plot(d.day_k, d.delta, "-o", color=color, label=label, lw=2)
    ax.fill_between(d.day_k, d.delta_ci_lo, d.delta_ci_hi, color=color, alpha=0.15)
ax.axhline(0, color="k", lw=0.8)
ax.set_xlabel("days after heavy episode-end (k)")
ax.set_ylabel("all_day_stress_avg delta vs matched-ordinary")
ax.set_title("Autonomic (Garmin stress) splits by pool: the two pools show\n"
             "opposite-signed post-heavy stress trajectories (+5d, raw)", fontsize=11)
ax.set_xticks([1, 2, 3, 4, 5])
ax.legend(fontsize=8, loc="best")
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "03_autonomic_pool_divergence.png"), dpi=130)
plt.close(fig)

# ---- Chart 4: detrend survival (headline cells) ----
cells = [
    ("total_steps", 3, "compensatory_success", "total_steps +3d succ"),
    ("total_steps", 5, "compensatory_success", "total_steps +5d succ"),
    ("vigorous_min", 5, "compensatory_success", "vigorous_min +5d succ"),
    ("sleep_duration_min", 3, "compensatory_success", "sleep_duration +3d succ"),
    ("sleep_duration_min", 5, "compensatory_success", "sleep_duration +5d succ"),
    ("sleep_light_min", 3, "compensatory_success", "sleep_light +3d succ"),
    ("all_day_stress_avg", 5, "compensatory_success", "all_day_stress +5d succ"),
    ("hr_median_waking", 3, "compensatory_success", "hr_median_waking +3d succ"),
    ("gevoelscore", 3, "compensatory_success", "gevoelscore +3d succ"),
    ("gevoelscore", 3, "compensatory_failure", "gevoelscore +3d FAIL"),
    ("gevoelscore", 5, "compensatory_failure", "gevoelscore +5d FAIL"),
    ("total_steps", 3, "compensatory_failure", "total_steps +3d FAIL"),
    ("sleep_awake_min", 3, "compensatory_failure", "sleep_awake +3d FAIL"),
]
rows = []
for outc, win, pool, label in cells:
    raw = summ[(summ.outcome == outc) & (summ.window == win) & (summ.pool == pool)
               & (summ.arm_type == "raw")]
    det = summ[(summ.outcome == outc) & (summ.window == win) & (summ.pool == pool)
               & (summ.arm_type == "detrended")]
    if raw.empty or det.empty:
        continue
    raw_auc = raw.auc.iloc[0]
    det_auc = det.auc.iloc[0]
    det_lo, det_hi = det.auc_ci_lo.iloc[0], det.auc_ci_hi.iloc[0]
    det_sig = not (det_lo <= 0 <= det_hi)
    ratio = det_auc / raw_auc if raw_auc != 0 else 0
    rows.append((label, ratio, det_sig))

rows = rows[::-1]
labels = [r[0] for r in rows]
ratios = [r[1] for r in rows]
colors = []
for _, ratio, det_sig in rows:
    if ratio < 0:
        colors.append("#7a3b8f")       # sign-flip (purple)
    elif det_sig:
        colors.append(C_SLEEP)         # survives detrend (green)
    else:
        colors.append(C_FAILURE)       # erased by detrend (rust)

fig, ax = plt.subplots(figsize=(8.4, 5.4))
ax.barh(labels, ratios, color=colors)
ax.axvline(1.0, color=C_SLEEP, lw=1, ls="--")
ax.axvline(0.0, color="k", lw=0.8)
ax.set_xlabel("detrended AUC / raw AUC   (1.0 = fully survives, 0 = fully erased, <0 = sign-flip)")
ax.set_title("Detrend fragility: how much of each raw signal survives removing envelope drift\n"
             "green = detrended CI still excludes zero; rust = erased; purple = sign-flip", fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "04_detrend_survival.png"), dpi=130)
plt.close(fig)

# ---- Chart 5: LC-era timeline — exertion intensity + gevoelscore + events ----
# Combines both requested views: an event raster (all heavy / very_heavy / crash
# days) plus the intensity and gevoelscore line graphs, on one shared time axis.
INTENSITY_ORDER = {"none": 0, "light": 1, "moderate": 2, "heavy": 3, "very_heavy": 4}
INTENSITY_LABELS = ["none", "light", "moderate", "heavy", "very_heavy"]

m = pd.read_csv(MASTER_CSV, parse_dates=["date"])
m = m[m["lc_phase"] == "lc"].sort_values("date").reset_index(drop=True)
m = m.set_index("date")
m["intensity"] = m["exertion_class_lagged_lcera"].map(INTENSITY_ORDER)

# continuous daily index so rolling means respect real calendar gaps
full_idx = pd.date_range(m.index.min(), m.index.max(), freq="D")
mi = m.reindex(full_idx)
intensity_roll = mi["intensity"].rolling("14D", min_periods=4).mean()
gscore_roll = mi["gevoelscore"].rolling("14D", min_periods=4).mean()

heavy_days = m.index[m["exertion_class_lagged_lcera"] == "heavy"]
vheavy_days = m.index[m["exertion_class_lagged_lcera"] == "very_heavy"]
crash_days = m.index[m["is_crash"] == True]  # noqa: E712

fig, (axE, axI, axG) = plt.subplots(
    3, 1, figsize=(15.5, 9.2), sharex=True,
    gridspec_kw={"height_ratios": [1.1, 1.5, 1.5]},
)

# Panel 1 — event raster
axE.scatter(vheavy_days, [3] * len(vheavy_days), marker="|", s=140,
            color="#7a1f10", linewidths=1.4, label=f"very_heavy day (n={len(vheavy_days)})")
axE.scatter(heavy_days, [2] * len(heavy_days), marker="|", s=140,
            color="#e08a2e", linewidths=1.4, label=f"heavy day (n={len(heavy_days)})")
axE.scatter(crash_days, [1] * len(crash_days), marker="x", s=42,
            color="#c1543a", linewidths=1.4, label=f"crash day (n={len(crash_days)})")
axE.set_yticks([1, 2, 3])
axE.set_yticklabels(["crash", "heavy", "very_heavy"])
axE.set_ylim(0.5, 3.5)
axE.set_title("LC-era timeline: every heavy / very_heavy day and every crash, "
              "with exertion intensity and felt-state trends below", fontsize=12)
axE.legend(fontsize=8, loc="upper right", ncol=3)
axE.grid(axis="x", alpha=0.25); axE.grid(axis="y", alpha=0)

# Panel 2 — exertion intensity
axI.scatter(mi.index, mi["intensity"], s=6, color="#e08a2e", alpha=0.28)
axI.plot(intensity_roll.index, intensity_roll, color="#7a1f10", lw=2,
         label="14-day rolling mean")
axI.set_yticks(range(5)); axI.set_yticklabels(INTENSITY_LABELS)
axI.set_ylim(-0.3, 4.3)
axI.set_ylabel("exertion intensity")
axI.legend(fontsize=8, loc="upper right")
axI.grid(alpha=0.25)

# Panel 3 — gevoelscore
axG.scatter(mi.index, mi["gevoelscore"], s=6, color="#3a7ca5", alpha=0.30)
axG.plot(gscore_roll.index, gscore_roll, color="#1f4e6b", lw=2,
         label="14-day rolling mean")
axG.scatter(crash_days, m.loc[crash_days, "gevoelscore"], s=26, color="#c1543a",
            zorder=5, label="crash day")
axG.set_ylim(0.5, 6.5)
axG.set_ylabel("gevoelscore (1-6)")
axG.set_xlabel("date")
axG.legend(fontsize=8, loc="lower right")
axG.grid(alpha=0.25)

# year gridlines across all panels
for ax in (axE, axI, axG):
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator((1, 4, 7, 10)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
axG.set_xlim(mi.index.min(), mi.index.max())
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "05_lc_era_timeline.png"), dpi=130)
plt.close(fig)

# ---- Chart 6: lagged-baseline drift over the LC era, all 4 axes ----
# exertion_class_lagged_lcera is a COMPOSITE: each day is percentile-ranked on
# four axes against a LAGGED window [d-90, d-31] (60 days, LC-era only, min 40
# valid), each axis mapped to a class, and the day's class is the WORST of the
# four. The class cutoffs are the window's own percentiles: heavy = 85th,
# very_heavy = 95th. Plotting those percentile curves per axis shows the whole
# reference frame drifting -- what counts as "heavy" is a moving, personal target.
LAG_OLD = 90   # oldest included day (d-90)
LAG_NEW = 31   # newest included day (d-31); recent 30 days excluded
MIN_LAGGED = 40

AXES = [
    ("effective_exertion_min", "Axis A - effective_exertion_min", "min"),
    ("total_steps", "Axis B - total_steps", "steps"),
    ("max_hr", "Axis C - max_hr", "bpm"),
    ("vigorous_min", "Axis D - vigorous_min", "min"),
]

rng = np.random.default_rng(RANDOM_SEED)
B = 3000

fig, axarr = plt.subplots(2, 2, figsize=(14.5, 8.4), sharex=True)
for ax, (col, label, unit) in zip(axarr.flat, AXES):
    s = m[col].dropna()
    med, p85, p95, vd = [], [], [], []
    for d in s.index:
        win = s.loc[d - pd.Timedelta(days=LAG_OLD): d - pd.Timedelta(days=LAG_NEW)]
        if len(win) < MIN_LAGGED:
            continue
        vd.append(d)
        med.append(win.median()); p85.append(win.quantile(0.85)); p95.append(win.quantile(0.95))
    med = pd.Series(med, index=vd); p85 = pd.Series(p85, index=vd); p95 = pd.Series(p95, index=vd)

    ci_x, ci_lo, ci_hi = [], [], []
    for a in pd.date_range(med.index.min(), med.index.max(), freq="MS"):
        d = med.index[med.index.get_indexer([a], method="nearest")[0]]
        win = s.loc[d - pd.Timedelta(days=LAG_OLD): d - pd.Timedelta(days=LAG_NEW)].values
        if len(win) < MIN_LAGGED:
            continue
        boot = np.median(rng.choice(win, size=(B, len(win)), replace=True), axis=1)
        ci_x.append(d); ci_lo.append(np.percentile(boot, 2.5)); ci_hi.append(np.percentile(boot, 97.5))

    ax.scatter(s.index, s.values, s=5, color="#3a7ca5", alpha=0.12)
    ax.plot(p95.index, p95, color="#7a1f10", lw=1.7, ls="--", label="very_heavy (95th pct)")
    ax.plot(p85.index, p85, color="#e08a2e", lw=1.7, ls="--", label="heavy (85th pct)")
    ax.plot(med.index, med, color="#1f4e6b", lw=2.0, label="baseline median (50th)")
    ax.fill_between(ci_x, ci_lo, ci_hi, color="#1f4e6b", alpha=0.25, label="median 95% CI")
    cap = float(np.nanpercentile(s.values, 97))
    lo = 0 if col != "max_hr" else float(np.nanpercentile(s.values, 3))
    ax.set_ylim(lo, cap * 1.08)
    ax.set_title(label, fontsize=10)
    ax.set_ylabel(unit)
    ax.grid(alpha=0.25)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
axarr.flat[0].legend(fontsize=7.5, loc="upper right")
fig.suptitle("Lagged baseline drifts across all four exertion axes (class = worst of the four): the "
             "'heavy'/'very_heavy'\nabsolute bar falls after 2023 on steps, effective-exertion and "
             "vigorous minutes; max_hr (a physiological ceiling) barely moves", fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(os.path.join(CHARTS, "06_lagged_baseline_drift.png"), dpi=130)
plt.close(fig)

# ---- Chart 7: full smartwatch period (healthy -> infection -> LC) ----
# Extends the timeline back over the whole consolidated record. The exertion
# CLASS (_lcera) is undefined pre-LC and gevoelscore self-tracking starts
# 2022-09-03, so this view uses RAW signals in absolute units -- which is what
# makes the deconditioning across the infection legible.
full = pd.read_csv(MASTER_CSV, parse_dates=["date"]).sort_values("date").set_index("date")
fidx = pd.date_range(full.index.min(), full.index.max(), freq="D")
fr = full.reindex(fidx)

phase_spans = []  # (start, end, color, label)
for ph, color, label in [
    ("pre_corona", "#5a8f3d", "healthy (pre-corona)"),
    ("corona_infection", "#c1543a", "infection"),
    ("lc", None, "Long COVID"),
]:
    g = full.index[full["lc_phase"] == ph]
    if len(g):
        phase_spans.append((g.min(), g.max(), color, label))

crash_days_full = full.index[full["is_crash"] == True]  # noqa: E712

PANELS = [
    ("vigorous_min", "vigorous minutes/day", "#7a1f10"),
    ("effective_exertion_min", "effective exertion min/day", "#3a7ca5"),
    ("total_steps", "total steps/day", "#1f6f6f"),
    ("gevoelscore", "gevoelscore (1-6)", "#1f4e6b"),
]
fig, axes = plt.subplots(4, 1, figsize=(15.5, 10.5), sharex=True)
for ax, (col, ylabel, color) in zip(axes, PANELS):
    ax.scatter(fr.index, fr[col], s=6, color=color, alpha=0.22)
    roll = fr[col].rolling("21D", min_periods=5).mean()
    ax.plot(roll.index, roll, color=color, lw=2, label="21-day rolling mean")
    if col == "gevoelscore":
        ax.scatter(crash_days_full, full.loc[crash_days_full, "gevoelscore"],
                   s=22, color="#c1543a", zorder=5, label="crash day")
        ax.set_ylim(0.5, 6.5)
    else:
        cap = float(np.nanpercentile(full[col].dropna(), 97))
        ax.set_ylim(0, cap * 1.08)
    # phase shading
    for start, end, pc, plabel in phase_spans:
        if pc is not None:
            ax.axvspan(start, end, color=pc, alpha=0.08, lw=0)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.legend(fontsize=7.5, loc="upper right")
    ax.grid(alpha=0.22)

# phase boundary lines + labels on the top axis
for start, end, pc, plabel in phase_spans:
    for ax in axes:
        ax.axvline(start, color="#555", lw=0.8, ls=":")
    axes[0].text(start, axes[0].get_ylim()[1] * 0.92, "  " + plabel,
                 fontsize=8, color="#333", va="top")
axes[0].set_title("Full smartwatch period (2021-08 to 2026-06): activity collapses across the "
                  "infection into LC.\nVigorous minutes are near-zero only from LC onset; "
                  "gevoelscore tracking starts 2022-09 (blank before). Crashes are LC-only.",
                  fontsize=11)
axes[-1].set_xlabel("date")
for ax in axes:
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator((1, 4, 7, 10)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
axes[-1].set_xlim(fr.index.min(), fr.index.max())
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "07_full_period_timeline.png"), dpi=130)
plt.close(fig)

print("charts written to", CHARTS)
for f in sorted(os.listdir(CHARTS)):
    print(" ", f)
