"""
Multi-channel extension of the citalopram dose-response analysis.

Tests whether the stress_mean_sleep dose-response generalises to other
parent MD section 3 baseline channels (resting_hr, bb_overnight_gain,
bb_lowest, all_day_stress_avg, respiration_avg_sleep). Each channel
gets the same three-pronged test pattern that confirmed stress_mean_sleep:

  P1. Afbouw 2026 primary: stress ~ b0 + b_dose*plasma + b_time*days, HAC SE
      (one-sided H1: b_dose > 0; higher plasma -> higher channel value)
  P2. Buildup 2024 post-CPAP-buffer: same regression on the 2024-05-01 ->
      2024-06-19 window (CPAP-equilibration 14d after 2024-04-16 excluded)
  P3. Spring 2025 control: stress ~ b0 + b_time on the same 2025 calendar slot
      (April 9 -> June 19; same calendar window as the buildup) with dose
      constant at 30mg (no buildup, no afbouw)

For each channel we ask:
  - Are afbouw and buildup b_dose signs concordant (positive in both)?
  - Does the spring control show a flat slope (seasonality alibi weak)?
  - How does the channel-specific magnitude compare to stress_mean_sleep?

Skipped:
  - sleep_efficiency: NOT in per_day_master.csv (confirmed 2026-06-14)
  - bb_overnight_gain in buildup window: 0 observations (parent MD section 2b);
    afbouw + spring control only.

Run:
    GEVOELSCORE_DATA_PATH=C:/Users/Gebruiker/Documents/gevoelscore-data python multi_channel_check.py
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


# ---------- Constants (shared with dose_response.py and buildup_check.py) ----------

T_HALF_DAYS = 35.0 / 24.0
DECAY_K = np.log(2.0) / T_HALF_DAYS
HAC_MAXLAGS = 4

AFBOUW_START = pd.Timestamp("2026-03-20")
AFBOUW_END = pd.Timestamp("2026-06-05")
AFBOUW_DOSE_INITIAL = 30.0
AFBOUW_STEPS = [
    (pd.Timestamp("2026-03-20"), -10.0),
    (pd.Timestamp("2026-04-17"), -10.0),
    (pd.Timestamp("2026-05-27"),  -2.0),
]

BUILDUP_START = pd.Timestamp("2024-04-09")
BUILDUP_END = pd.Timestamp("2024-06-19")
CPAP_END = pd.Timestamp("2024-04-16")
POST_CPAP_BUFFER_DAYS = 14
POST_CPAP_START = CPAP_END + pd.Timedelta(days=POST_CPAP_BUFFER_DAYS + 1)
BUILDUP_DOSE_INITIAL = 0.0
BUILDUP_STEPS = [
    (pd.Timestamp("2024-04-09"), +10.0),
    (pd.Timestamp("2024-05-05"), +10.0),
]

# 2025 control window: same calendar slot as the buildup (April 9 -> June 19)
# during 30mg consolidation; dose constant so b_dose unidentifiable.
SPRING_2025_START = pd.Timestamp("2025-04-09")
SPRING_2025_END = pd.Timestamp("2025-06-19")


# Channels under test (parent MD section 3 baseline channels)
# Direction: +1 means H1 is "higher plasma -> higher channel value"; -1 means
# "higher plasma -> LOWER channel value" (so H1: b_dose < 0). Mechanism-driven
# from the SSRI / autonomic literature anchors queued at QUEUED-WORK Tier 3.
CHANNELS = [
    # channel name           expected_sign  rationale
    ("stress_mean_sleep",    +1, "SSRI elevates nocturnal autonomic load"),
    ("all_day_stress_avg",   +1, "SSRI elevates daytime autonomic load (HRV reduction)"),
    ("resting_hr",           +1, "SSRI raises RHR (HRV reduction; Licht/Kemp)"),
    ("respiration_avg_sleep",+1, "SSRI alters sleep architecture; respiration rate"),
    ("bb_overnight_gain",    -1, "Worse recovery on SSRI -> lower BB gain overnight"),
    ("bb_lowest",            -1, "Worse recovery on SSRI -> lower BB nadir"),
]


def plasma_dose_mg(d, initial, steps):
    val = initial
    for step_date, delta in steps:
        if d >= step_date:
            days_since = (d - step_date).days
            val += delta * (1.0 - np.exp(-DECAY_K * days_since))
    return val


master = pd.read_csv(DATA / "unified" / "per_day_master.csv", parse_dates=["date"])
master = master.set_index("date").sort_index()


def fit_dose_window(start, end, channel, dose_initial, dose_steps,
                    drop_pre=None, expected_sign=+1):
    """Fit channel ~ b0 + b_dose*plasma + b_time*days with HAC SE.
    drop_pre: optional date below which rows are excluded.
    expected_sign: +1 if H1 is b_dose > 0; -1 if H1 is b_dose < 0.
    Returns dict with beta, CI, p_one_sided, n, etc."""
    win = master.loc[start:end, [channel]].copy()
    if drop_pre is not None:
        win = win.loc[win.index >= drop_pre]
    win = win.dropna()
    if len(win) < 10:
        return None
    win["days"] = (win.index - start).days.astype(float)
    win["dose"] = [plasma_dose_mg(d, dose_initial, dose_steps) for d in win.index]
    X = pd.DataFrame({
        "const": 1.0, "dose": win["dose"].values, "time": win["days"].values,
    }, index=win.index)
    y = win[channel].values
    fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_MAXLAGS})
    beta = float(fit.params["dose"])
    ci = fit.conf_int(alpha=0.05).loc["dose"]
    p_two = float(fit.pvalues["dose"])
    # One-sided p for the prior-direction (set by expected_sign)
    if expected_sign > 0:
        p_one = p_two / 2.0 if beta > 0 else 1.0 - p_two / 2.0
    else:
        p_one = p_two / 2.0 if beta < 0 else 1.0 - p_two / 2.0
    # CI excludes zero on the prior-direction side?
    if expected_sign > 0:
        ci_excludes_zero_prior_side = ci[0] > 0
    else:
        ci_excludes_zero_prior_side = ci[1] < 0
    return {
        "channel": channel, "n": len(win),
        "window_start": win.index.min().date(), "window_end": win.index.max().date(),
        "channel_mean": float(win[channel].mean()),
        "channel_sd": float(win[channel].std()),
        "beta_dose": beta, "ci_lo": float(ci[0]), "ci_hi": float(ci[1]),
        "hac_p_two_sided": p_two, "hac_p_one_sided_prior": p_one,
        "ci_excludes_zero_prior_side": ci_excludes_zero_prior_side,
        "expected_sign": expected_sign,
        "sign_match_prior": (beta > 0 if expected_sign > 0 else beta < 0),
    }


def fit_spring_control(channel):
    """2025 April 9 -> June 19, 30mg consolidation throughout. Fit
    channel ~ b0 + b_time only. Returns dict with beta_time, CI."""
    win = master.loc[SPRING_2025_START:SPRING_2025_END, [channel]].dropna()
    if len(win) < 10:
        return None
    win["days"] = (win.index - SPRING_2025_START).days.astype(float)
    X = pd.DataFrame({"const": 1.0, "time": win["days"].values}, index=win.index)
    y = win[channel].values
    fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_MAXLAGS})
    beta = float(fit.params["time"])
    ci = fit.conf_int(alpha=0.05).loc["time"]
    return {
        "channel": channel, "n": len(win),
        "channel_mean": float(win[channel].mean()),
        "beta_time": beta, "ci_lo": float(ci[0]), "ci_hi": float(ci[1]),
        "hac_p": float(fit.pvalues["time"]),
    }


# ---------- Run all channels ----------

print(f"Multi-channel dose-response check across {len(CHANNELS)} channels.")
print(f"  Afbouw: {AFBOUW_START.date()} -> {AFBOUW_END.date()}")
print(f"  Buildup post-CPAP: {POST_CPAP_START.date()} -> {BUILDUP_END.date()}")
print(f"  Spring 2025 control: {SPRING_2025_START.date()} -> {SPRING_2025_END.date()}")
print()

results = []
for channel, sign, rationale in CHANNELS:
    if channel not in master.columns:
        print(f"  [{channel}] NOT IN MASTER -- skipping")
        continue
    print(f"--- {channel} (expected sign: {'+' if sign > 0 else '-'}1; {rationale})")

    afbouw = fit_dose_window(AFBOUW_START, AFBOUW_END, channel,
                             AFBOUW_DOSE_INITIAL, AFBOUW_STEPS,
                             expected_sign=sign)
    buildup = fit_dose_window(BUILDUP_START, BUILDUP_END, channel,
                              BUILDUP_DOSE_INITIAL, BUILDUP_STEPS,
                              drop_pre=POST_CPAP_START, expected_sign=sign)
    spring = fit_spring_control(channel)

    if afbouw:
        print(f"  Afbouw 2026:        n={afbouw['n']}  b_dose={afbouw['beta_dose']:+.4f}  "
              f"CI=[{afbouw['ci_lo']:+.4f}, {afbouw['ci_hi']:+.4f}]  "
              f"p_one={afbouw['hac_p_one_sided_prior']:.4f}  "
              f"sign_match={afbouw['sign_match_prior']}")
    else:
        print(f"  Afbouw 2026:        SKIP (insufficient data)")
    if buildup:
        print(f"  Buildup post-CPAP:  n={buildup['n']}  b_dose={buildup['beta_dose']:+.4f}  "
              f"CI=[{buildup['ci_lo']:+.4f}, {buildup['ci_hi']:+.4f}]  "
              f"p_one={buildup['hac_p_one_sided_prior']:.4f}  "
              f"sign_match={buildup['sign_match_prior']}")
    else:
        print(f"  Buildup post-CPAP:  SKIP (insufficient data; e.g. bb_overnight_gain missing in 2024)")
    if spring:
        print(f"  Spring 2025 control: n={spring['n']}  b_time={spring['beta_time']:+.4f}/day  "
              f"CI=[{spring['ci_lo']:+.4f}, {spring['ci_hi']:+.4f}]")
    else:
        print(f"  Spring 2025 control: SKIP")
    print()

    # Three-pronged verdict
    if afbouw and buildup:
        afbouw_supports = afbouw["sign_match_prior"]
        buildup_supports = buildup["sign_match_prior"] and buildup["ci_excludes_zero_prior_side"]
        if afbouw_supports and buildup_supports:
            verdict = "CONFIRMED (sign match + buildup CI excludes zero)"
        elif afbouw_supports and buildup["sign_match_prior"]:
            verdict = "consistent (sign match, but buildup CI brushes zero)"
        elif not afbouw_supports and not buildup["sign_match_prior"]:
            verdict = "REJECTED (both phases contradict prior direction)"
        elif afbouw_supports != buildup["sign_match_prior"]:
            verdict = "INCONSISTENT (afbouw and buildup signs disagree)"
        else:
            verdict = "ambiguous"
    elif afbouw and not buildup:
        verdict = (f"partial -- afbouw only, no buildup data ("
                   f"{'sign match' if afbouw['sign_match_prior'] else 'sign mismatch'})")
    else:
        verdict = "SKIP -- insufficient data"

    results.append({
        "channel": channel, "expected_sign": sign, "rationale": rationale,
        "verdict": verdict,
        "afbouw": afbouw, "buildup": buildup, "spring": spring,
    })
    print(f"  Verdict: {verdict}")
    print()


# ---------- Build summary table ----------

rows = []
for r in results:
    row = {
        "channel": r["channel"],
        "expected_sign": r["expected_sign"],
        "verdict": r["verdict"],
        "afbouw_beta": r["afbouw"]["beta_dose"] if r["afbouw"] else None,
        "afbouw_ci_lo": r["afbouw"]["ci_lo"] if r["afbouw"] else None,
        "afbouw_ci_hi": r["afbouw"]["ci_hi"] if r["afbouw"] else None,
        "afbouw_p_one": r["afbouw"]["hac_p_one_sided_prior"] if r["afbouw"] else None,
        "afbouw_n": r["afbouw"]["n"] if r["afbouw"] else None,
        "buildup_beta": r["buildup"]["beta_dose"] if r["buildup"] else None,
        "buildup_ci_lo": r["buildup"]["ci_lo"] if r["buildup"] else None,
        "buildup_ci_hi": r["buildup"]["ci_hi"] if r["buildup"] else None,
        "buildup_p_one": r["buildup"]["hac_p_one_sided_prior"] if r["buildup"] else None,
        "buildup_n": r["buildup"]["n"] if r["buildup"] else None,
        "spring_2025_beta_time": r["spring"]["beta_time"] if r["spring"] else None,
        "spring_2025_n": r["spring"]["n"] if r["spring"] else None,
    }
    rows.append(row)

summary_df = pd.DataFrame(rows)
summary_path = OUT / "multi_channel_summary.csv"
summary_df.to_csv(summary_path, index=False)
print(f"Wrote summary: {summary_path}")


# ---------- Plot: per-channel coefficient panels (afbouw + buildup side by side) ----------

n_channels = len(results)
fig, axes = plt.subplots(2, 1, figsize=(13, 10))

# Panel 1: Afbouw + Buildup beta_dose per channel (in channel-native units, normalised to SD)
ax = axes[0]
xs = np.arange(n_channels)
width = 0.35
afbouw_y, afbouw_lo, afbouw_hi = [], [], []
buildup_y, buildup_lo, buildup_hi = [], [], []
labels_x = []
for r in results:
    # Normalise to channel SD so different channels are comparable
    sd = r["afbouw"]["channel_sd"] if r["afbouw"] else 1.0
    af = r["afbouw"]
    bu = r["buildup"]
    afbouw_y.append(af["beta_dose"] / sd if af else np.nan)
    afbouw_lo.append((af["beta_dose"] - af["ci_lo"]) / sd if af else 0)
    afbouw_hi.append((af["ci_hi"] - af["beta_dose"]) / sd if af else 0)
    buildup_y.append(bu["beta_dose"] / sd if bu else np.nan)
    buildup_lo.append((bu["beta_dose"] - bu["ci_lo"]) / sd if bu else 0)
    buildup_hi.append((bu["ci_hi"] - bu["beta_dose"]) / sd if bu else 0)
    labels_x.append(f"{r['channel']}\n(prior {'+' if r['expected_sign']>0 else '-'})")

ax.errorbar(xs - width/2, afbouw_y, yerr=[afbouw_lo, afbouw_hi], fmt="o", color="#a37",
            capsize=4, ms=8, label="Afbouw 2026")
ax.errorbar(xs + width/2, buildup_y, yerr=[buildup_lo, buildup_hi], fmt="s", color="#7a3",
            capsize=4, ms=8, label="Buildup 2024 post-CPAP")
ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
ax.set_xticks(xs)
ax.set_xticklabels(labels_x, fontsize=9)
ax.set_ylabel("beta_dose / channel_SD (per mg)")
ax.set_title("Per-channel dose-response (normalised to channel SD)")
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, axis="y")
# Mark verdict
for x, r in zip(xs, results):
    color = "green" if "CONFIRMED" in r["verdict"] else \
            "blue" if "consistent" in r["verdict"] else \
            "orange" if "partial" in r["verdict"] or "ambiguous" in r["verdict"] else \
            "red"
    ax.text(x, ax.get_ylim()[1] * 0.92, r["verdict"].split(" ")[0],
            ha="center", fontsize=7, color=color,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, ec=color))

# Panel 2: Sign-concordance summary heatmap-style
ax2 = axes[1]
verdict_color_map = {
    "CONFIRMED": "#2a7",
    "consistent": "#37a",
    "partial": "#a93",
    "ambiguous": "#a93",
    "INCONSISTENT": "#a55",
    "REJECTED": "#a33",
    "SKIP": "#888",
}
for i, r in enumerate(results):
    v = r["verdict"].split(" ")[0]
    color = verdict_color_map.get(v, "#888")
    af_sign_str = ""
    bu_sign_str = ""
    sp_sign_str = ""
    if r["afbouw"]:
        af_sign = "+" if r["afbouw"]["beta_dose"] > 0 else "-"
        prior_sign = "+" if r["expected_sign"] > 0 else "-"
        af_sign_str = f"{af_sign} (prior {prior_sign}) p={r['afbouw']['hac_p_one_sided_prior']:.3f}"
    if r["buildup"]:
        bu_sign = "+" if r["buildup"]["beta_dose"] > 0 else "-"
        bu_sign_str = f"{bu_sign} p={r['buildup']['hac_p_one_sided_prior']:.3f}"
    if r["spring"]:
        sp_sign_str = f"b_time = {r['spring']['beta_time']:+.4f}/day"
    summary_line = (f"{r['channel']:<25} | afbouw: {af_sign_str:<25} | "
                    f"buildup: {bu_sign_str:<20} | spring 2025: {sp_sign_str}")
    ax2.text(0.01, 1.0 - (i + 1) * 0.13, summary_line,
             fontsize=9, family="monospace", color=color,
             transform=ax2.transAxes)
    ax2.text(0.01, 1.0 - (i + 1) * 0.13 - 0.05,
             f"    verdict: {r['verdict']}",
             fontsize=8, family="monospace", color=color, style="italic",
             transform=ax2.transAxes)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis("off")
ax2.set_title("Per-channel three-pronged read summary", loc="left", fontsize=11)

fig.suptitle("Multi-channel extension of the citalopram dose-response", fontsize=12)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plot_path = OUT / "plots" / "multi_channel_check.png"
plt.savefig(plot_path, dpi=100)
plt.close()
print(f"Wrote plot: {plot_path}")


# ---------- Final readout ----------

print()
print("=" * 70)
print("MULTI-CHANNEL READOUT")
print("=" * 70)
n_confirmed = sum(1 for r in results if "CONFIRMED" in r["verdict"])
n_consistent = sum(1 for r in results if "consistent" in r["verdict"])
n_inconsistent = sum(1 for r in results if "INCONSISTENT" in r["verdict"])
n_rejected = sum(1 for r in results if "REJECTED" in r["verdict"])
n_partial = sum(1 for r in results if "partial" in r["verdict"] or "ambiguous" in r["verdict"])
print(f"Channels tested: {len(results)}")
print(f"  CONFIRMED       (sign+CI):  {n_confirmed}")
print(f"  consistent      (sign only): {n_consistent}")
print(f"  partial/ambig:               {n_partial}")
print(f"  INCONSISTENT  (signs differ): {n_inconsistent}")
print(f"  REJECTED (both contradict):   {n_rejected}")
print()
for r in results:
    print(f"  {r['channel']:<25}  {r['verdict']}")
