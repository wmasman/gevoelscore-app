"""R30 net-of-slow-confounders per-phase re-read (R19 audit).

Audits the absolute per-phase LEVELS from R19
(analyses/descriptive/recovery_phase_signal_backdrop/) against the slow
confounders (weight, deconditioning tail, aging). Per the framing locked with
the participant-researcher (2026-07-06), this is the RHR-FOCUSED read:

  PART A (rigorous): the per-phase resting_hr level decomposed with the EXACT
    locked model from analyses/longrun_rhr_trend/decomposition.py (reused by
    import, not re-derived), so a phase level-gap is split into
    weight / citalopram / aging / season / residual contributions. The honest
    core is that the STATIC per-phase level partition is NOT cleanly
    identifiable (longrun findings B9); we report the fitted split AND the
    2x-b_weight bound that collapses the residual, so the illness-attributable
    portion of the RHR rise is given as a BOUND, not a point.

  PART B (brief bound): the other exposed channels (stress_mean_sleep,
    all_day_stress_avg, bb_lowest, stress_low_motion) are cross-phase
    DOMINATED by citalopram (a step at phase 5), which is R20's territory, NOT
    a slow drift. We report per-phase raw vs LC-era-linear-detrended median as a
    supplementary bound, with the explicit caveat that a linear detrend on these
    channels partly absorbs the citalopram step.

  R28 pairing: per-phase p25/p75 (box strip) for resting_hr raw and residual.

Only the physiological channels are audited; felt-state (gevoelscore) is the
clean self-report axis and needs no correction. Layer-4 method note; no causal
marks per CONVENTIONS section 4.1.

Run from repo root:
    python docs/research/analyses/descriptive/recovery_phase_confounder_bound/run.py

Outputs:
    summary.json (machine-readable; gitignored per docs/research/**/*.json rule)
    prints the per-phase decomposition + detrend tables to stdout
"""
from __future__ import annotations

import importlib.util
import json
import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DC_PATH = HERE.parents[1] / "longrun_rhr_trend" / "decomposition.py"

_spec = importlib.util.spec_from_file_location("longrun_decomposition", DC_PATH)
dc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dc)

TAU_YEARS_REPRESENTATIVE = 4.0 / 12.0  # literature tau=4 months (findings B1 representative fit)

# Ordered recovery phases (recovery_phase value -> (id, label)). Phase 1 is the
# fit / lighter / younger pre-illness reference the register names.
PHASES = [
    ("pre_illness_healthy", "1", "pre_illness_healthy"),
    ("acute_infection", "2", "acute_infection"),
    ("lc_pre_ergo", "3", "lc_pre_ergo"),
    ("pacing_pre_citalopram_learning", "4a", "pacing_pre_citalopram_learning"),
    ("pacing_habit_established", "4b", "pacing_habit_established"),
    ("citalopram_modulated", "5", "citalopram_modulated"),
]

PART_B_CHANNELS = [
    ("stress_mean_sleep", "stress_mean_sleep"),
    ("all_day_stress_avg", "all_day_stress_avg"),
    ("bb_lowest", "bb_lowest"),
    ("stress_low_motion", "stress_low_motion_min_count_S60_Mlow"),
]

LC_ERA_START = pd.Timestamp("2022-04-04")


def _data_root() -> Path:
    raw = os.environ.get("GEVOELSCORE_DATA_PATH", "") or r"C:\Users\Gebruiker\Documents\gevoelscore-data"
    return Path(raw)


def load_phase_map() -> pd.Series:
    """date (Timestamp) -> recovery_phase, from per_day_master."""
    df = pd.read_csv(_data_root() / "unified" / "per_day_master.csv",
                     usecols=["date", "recovery_phase"], parse_dates=["date"])
    return df.set_index("date")["recovery_phase"]


def part_a():
    """Per-phase resting_hr decomposition using the reused longrun fit."""
    df = dc.load_master()
    wt = dc.load_weight_series()
    vo = dc.load_vo2_series()
    d = dc.build_daily_frame(df, wt, vo)

    y = d["resting_hr"].values.astype(float)
    shape = dc.decond_lit(d["t_cess"].values, TAU_YEARS_REPRESENTATIVE)
    X, names = dc.design_matrix(d, shape)
    beta = dc.fit_robust(X, y)
    beta_map = dict(zip(names, beta))

    # Per-day additive contributions (means add exactly; medians are for the box strip).
    idx = {nm: j for j, nm in enumerate(names)}
    contrib = {
        "intercept": np.full(len(d), beta[idx["intercept"]]),
        "decond": X[:, idx["decond_amp"]] * beta[idx["decond_amp"]],
        "weight": X[:, idx["b_weight"]] * beta[idx["b_weight"]],
        "citalopram": X[:, idx["b_dose"]] * beta[idx["b_dose"]],
        "season": X[:, idx["b_sin"]] * beta[idx["b_sin"]] + X[:, idx["b_cos"]] * beta[idx["b_cos"]],
        "aging": X[:, idx["b_age"]] * beta[idx["b_age"]],
    }
    modelled = X @ beta
    residual = y - modelled  # LC/aging residual (phase-specific)

    # residual under 2x b_weight (B9 non-identifiability bound)
    beta_2w = beta.copy()
    beta_2w[idx["b_weight"]] = beta[idx["b_weight"]] * 2.0
    residual_2w = y - (X @ beta_2w)

    work = pd.DataFrame({"date": pd.DatetimeIndex(d["date"]), "rhr": y, "residual": residual,
                         "residual_2w": residual_2w})
    for k, v in contrib.items():
        work[k] = v
    pmap = load_phase_map()
    work["phase"] = work["date"].map(pmap)

    per_phase = []
    for ph, pid, label in PHASES:
        sub = work[work["phase"] == ph]
        if len(sub) == 0:
            continue
        per_phase.append({
            "phase_id": pid, "phase": label, "n_days": int(len(sub)),
            "rhr_mean": round(float(sub["rhr"].mean()), 2),
            "rhr_median": round(float(sub["rhr"].median()), 2),
            "rhr_p25": round(float(sub["rhr"].quantile(0.25)), 2),
            "rhr_p75": round(float(sub["rhr"].quantile(0.75)), 2),
            # additive contributions (mean; sum to rhr_mean)
            "c_intercept": round(float(sub["intercept"].mean()), 2),
            "c_weight": round(float(sub["weight"].mean()), 2),
            "c_citalopram": round(float(sub["citalopram"].mean()), 2),
            "c_aging": round(float(sub["aging"].mean()), 2),
            "c_season": round(float(sub["season"].mean()), 2),
            "c_decond": round(float(sub["decond"].mean()), 2),
            "c_residual": round(float(sub["residual"].mean()), 2),
            # residual level (intercept + residual = the slow-driver-removed RHR level)
            "resid_level_mean": round(float((sub["intercept"] + sub["residual"]).mean()), 2),
            "resid_level_median": round(float((sub["intercept"] + sub["residual"]).median()), 2),
            "resid_level_p25": round(float((sub["intercept"] + sub["residual"]).quantile(0.25)), 2),
            "resid_level_p75": round(float((sub["intercept"] + sub["residual"]).quantile(0.75)), 2),
            # bound: residual level under 2x weight coefficient
            "resid_level_mean_2xweight": round(float((sub["intercept"] + sub["residual_2w"]).mean()), 2),
        })
    return {"beta": {k: round(float(v), 4) for k, v in beta_map.items()},
            "tau_years": TAU_YEARS_REPRESENTATIVE, "per_phase": per_phase,
            "n_days_fit": int(len(d))}


def part_b():
    """Per-phase raw vs LC-era-linear-detrended median for the exposed non-RHR channels."""
    cols = ["date", "recovery_phase"] + [c for _, c in PART_B_CHANNELS]
    df = pd.read_csv(_data_root() / "unified" / "per_day_master.csv",
                     usecols=cols, parse_dates=["date"])
    lc = df[df["date"] >= LC_ERA_START].copy()
    t = (lc["date"] - LC_ERA_START).dt.days.values.astype(float)

    out = []
    for name, col in PART_B_CHANNELS:
        s = lc[col].astype(float)
        mask = s.notna().values
        if mask.sum() < 40:
            out.append({"channel": name, "column": col, "error": "insufficient coverage"})
            continue
        # robust-ish linear trend via OLS on LC-era days (the aggregate slow-drift proxy)
        tt, yy = t[mask], s.values[mask]
        b1, b0 = np.polyfit(tt, yy, 1)
        detr_full = s.values - (b0 + b1 * t)  # residual about the LC-era linear trend
        lc["_detr"] = detr_full
        phases = []
        for ph, pid, label in PHASES:
            sp = lc[lc["recovery_phase"] == ph]
            raw = sp[col].dropna()
            det = sp["_detr"].dropna()
            if len(raw) == 0:
                continue
            phases.append({
                "phase_id": pid, "phase": label, "n": int(len(raw)),
                "raw_median": round(float(raw.median()), 3),
                "detrended_median": round(float(det.median()), 3),
            })
        out.append({"channel": name, "column": col,
                    "lc_era_trend_per_year": round(float(b1 * 365.25), 4), "phases": phases})
    return out


def main():
    print("[R30] Part A: reused longrun RHR decomposition, aggregating by recovery phase...")
    a = part_a()
    print(f"[R30]   reproduced beta: b_weight={a['beta']['b_weight']} (longrun 0.322), "
          f"b_dose={a['beta']['b_dose']} (longrun -0.038), "
          f"decond_amp={a['beta']['decond_amp']} (longrun 0.00), "
          f"b_age={a['beta']['b_age']} (longrun 0.50)")
    print("\n[R30] Per-phase resting_hr additive decomposition (mean bpm):\n")
    hdr = (f"{'ph':3} {'rhr':>6} {'=inter':>7} {'+weight':>8} {'+cital':>7} {'+age':>6} "
           f"{'+seas':>6} {'+resid':>7} | {'residLvl':>9} {'2xWt':>7}")
    print(hdr)
    print("-" * len(hdr))
    for p in a["per_phase"]:
        print(f"{p['phase_id']:3} {p['rhr_mean']:>6} {p['c_intercept']:>7} {p['c_weight']:>+8} "
              f"{p['c_citalopram']:>+7} {p['c_aging']:>+6} {p['c_season']:>+6} {p['c_residual']:>+7} | "
              f"{p['resid_level_mean']:>9} {p['resid_level_mean_2xweight']:>7}")

    print("\n[R30] Part B: per-phase raw vs LC-era-detrended median (citalopram-dominated -- bound only):\n")
    b = part_b()
    for ch in b:
        if ch.get("error"):
            print(f"  {ch['channel']:20} -- {ch['error']}")
            continue
        print(f"  {ch['channel']:20} (LC-era linear trend {ch['lc_era_trend_per_year']:+}/yr)")
        for p in ch["phases"]:
            print(f"      {p['phase_id']:3} raw {p['raw_median']:>8}   detrended {p['detrended_median']:>8}   n={p['n']}")

    meta = {
        "part_a_model": "reused analyses/longrun_rhr_trend/decomposition.py (literature tau=4mo representative fit)",
        "part_b_method": "per-phase median raw vs residual about an LC-era linear trend (aggregate slow-drift proxy)",
        "lc_era_start": str(LC_ERA_START.date()),
        "run_at": datetime.now().isoformat(timespec="seconds"),
    }
    result = {"part_a_rhr_decomposition": a, "part_b_detrend_bound": b, "meta": meta}
    (HERE / "summary.json").write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\n[R30] Wrote {HERE / 'summary.json'}")


if __name__ == "__main__":
    main()
