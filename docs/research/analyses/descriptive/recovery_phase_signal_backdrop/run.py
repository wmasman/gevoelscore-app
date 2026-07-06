"""R19 recovery-phase signal backdrop: each scorecard signal read along the
lived recovery-phase axis, DESCRIPTIVELY.

Site request R19 ("each primary signal read along the recovery-phase axis").
Per the framing locked with the participant-researcher (2026-07-06), this is
the **level + crash-count backdrop**: per-phase median levels (all crash-bearing
phases) plus per-phase crash counts, framed as descriptive phase-to-phase
variation - NOT a per-phase verdict and NOT a split. Per-phase discrimination is
declined-with-reason (see findings.md section on why): the only two phases that
could carry a discrimination number (4b, 5) straddle the citalopram-onset
boundary, so a per-phase discrimination read collapses to the medication-era
contrast that R14 retired under single-pool primacy and R20 already characterised.

Axis: `recovery_phase` column of per_day_master (per
methodology/lc_recovery_phase_axis.md section 2). Within Stratum 4 the crash
corpus spans four phases: lc_pre_ergo (3), pacing_pre_citalopram_learning (4a),
pacing_habit_established (4b), citalopram_modulated (5). Phases 1-2 are pre-corpus
(Garmin-only, no crashes) and omitted.

Robust central tendency (median + p25/p75) per CONVENTIONS section 3.1; named
counts per section 3.6; Layer-1 descriptive, no causal marks per section 4.1.

Run from repo root:
    python docs/research/analyses/descriptive/recovery_phase_signal_backdrop/run.py

Outputs:
    summary.json (machine-readable; gitignored per docs/research/**/*.json rule)
    prints per-phase level + crash-count tables to stdout
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent

STRATUM_4_START = date(2022, 9, 3)
AS_OF_DATE = date(2026, 6, 5)

# Ordered crash-bearing recovery phases within Stratum 4 (col value -> (id, label)).
PHASES = [
    ("lc_pre_ergo", "3", "lc_pre_ergo"),
    ("pacing_pre_citalopram_learning", "4a", "pacing_pre_citalopram_learning"),
    ("pacing_habit_established", "4b", "pacing_habit_established"),
    ("citalopram_modulated", "5", "citalopram_modulated"),
]

# Per scorecard signal: (signal, channel column, kind). kind drives the level read.
#   numeric  -> median / p25 / p75 of the channel
#   fraction -> fraction of days at a heavy/very_heavy exertion class
SIGNAL_CHANNELS = [
    ("HA07d", "stress_stdev_sleep", "numeric"),
    ("HA07c", "stress_mean_sleep", "numeric"),
    ("H02b", "max_spike_minutes", "numeric"),
    ("HA11", "u_dip_count", "numeric"),
    ("HA10", "bb_highest", "numeric"),
    ("HA06b", "resting_hr", "numeric"),
    ("HA01b", "exertion_class_lagged", "fraction"),
]

HEAVY_CLASSES = {"heavy", "very_heavy"}
MIN_CRASHES_FOR_DISCRIMINATION = 10  # the evaluate_ha bar; below this = honest-limit


def _data_root() -> Path:
    raw = os.environ.get("GEVOELSCORE_DATA_PATH", "") or r"C:\Users\Gebruiker\Documents\gevoelscore-data"
    root = Path(raw)
    if not root.exists():
        raise RuntimeError(f"data root {raw!r} does not exist")
    return root


def load_master() -> pd.DataFrame:
    df = pd.read_csv(_data_root() / "unified" / "per_day_master.csv",
                     parse_dates=["date"], low_memory=False)
    df["date"] = df["date"].dt.date
    df = df[(df["date"] >= STRATUM_4_START) & (df["date"] <= AS_OF_DATE)].copy()
    return df.sort_values("date").reset_index(drop=True)


def load_crash_starts() -> list[date]:
    df = pd.read_csv(_data_root() / "processed" / "crash_labels" / "labels_crash_v2.csv",
                     parse_dates=["date", "episode_start"])
    crashes = df[df["label"] == "crash"].dropna(subset=["episode_start"]).copy()
    crashes["episode_start"] = crashes["episode_start"].dt.date
    starts = sorted(set(crashes["episode_start"]))
    return [d for d in starts if STRATUM_4_START <= d <= AS_OF_DATE]


def numeric_level(series: pd.Series) -> dict:
    vals = series.dropna().to_numpy(dtype=float)
    n = int(len(vals))
    if n == 0:
        return {"n": 0, "median": None, "p25": None, "p75": None}
    return {
        "n": n,
        "median": round(float(np.median(vals)), 3),
        "p25": round(float(np.percentile(vals, 25)), 3),
        "p75": round(float(np.percentile(vals, 75)), 3),
    }


def fraction_level(series: pd.Series) -> dict:
    vals = series.dropna().astype(str)
    n = int(len(vals))
    if n == 0:
        return {"n": 0, "frac_heavy_plus": None}
    frac = float(vals.isin(HEAVY_CLASSES).mean())
    return {"n": n, "frac_heavy_plus": round(frac, 3)}


def main():
    df = load_master()
    crash_starts = load_crash_starts()
    date_to_phase = dict(zip(df["date"], df["recovery_phase"]))

    # ---- Per-phase crash counts + base rates ----
    phase_days = {ph: int((df["recovery_phase"] == ph).sum()) for ph, _, _ in PHASES}
    phase_crashes = {ph: 0 for ph, _, _ in PHASES}
    for cd in crash_starts:
        ph = date_to_phase.get(cd)
        if ph in phase_crashes:
            phase_crashes[ph] += 1

    crash_backdrop = []
    for ph, pid, label in PHASES:
        d = phase_days[ph]
        c = phase_crashes[ph]
        crash_backdrop.append({
            "phase_id": pid, "phase": label, "n_days": d, "n_crashes": c,
            "base_rate_pct": round(100.0 * c / d, 2) if d else None,
            "discrimination_computable": c >= MIN_CRASHES_FOR_DISCRIMINATION,
        })

    # ---- Per-signal per-phase level backdrop ----
    signals = []
    for sig, col, kind in SIGNAL_CHANNELS:
        if col not in df.columns:
            signals.append({"signal": sig, "channel": col, "kind": kind,
                            "error": "column absent", "phases": []})
            continue
        per_phase = []
        for ph, pid, label in PHASES:
            sub = df[df["recovery_phase"] == ph][col]
            lvl = numeric_level(sub) if kind == "numeric" else fraction_level(sub)
            per_phase.append({"phase_id": pid, "phase": label,
                              "n_crashes": phase_crashes[ph], **lvl})
        signals.append({"signal": sig, "channel": col, "kind": kind, "phases": per_phase})

    meta = {
        "stratum_4_start": str(STRATUM_4_START),
        "as_of_date": str(AS_OF_DATE),
        "n_days": len(df),
        "n_crash_episodes": len(crash_starts),
        "axis_source": "methodology/lc_recovery_phase_axis.md section 2 (recovery_phase column)",
        "min_crashes_for_discrimination": MIN_CRASHES_FOR_DISCRIMINATION,
        "run_at": datetime.now().isoformat(timespec="seconds"),
    }
    result = {"crash_backdrop": crash_backdrop, "signals": signals, "meta": meta}
    (HERE / "summary.json").write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")

    # ---- stdout ----
    print("[R19] Per-phase crash backdrop (Stratum 4):\n")
    print(f"{'phase':30} {'days':>5} {'crashes':>8} {'base%':>7} {'disc?':>6}")
    for row in crash_backdrop:
        disc = "yes" if row["discrimination_computable"] else "honest-limit"
        print(f"{row['phase_id']+' '+row['phase']:30} {row['n_days']:>5} {row['n_crashes']:>8} "
              f"{row['base_rate_pct']:>7} {disc:>6}")
    print("\n[R19] Per-signal per-phase level backdrop:\n")
    for s in signals:
        if s.get("error"):
            print(f"  {s['signal']:7} {s['channel']:22} -- {s['error']}")
            continue
        print(f"  {s['signal']:7} {s['channel']:22} ({s['kind']})")
        for p in s["phases"]:
            if s["kind"] == "numeric":
                med = p["median"]
                cell = f"median {med:>7} [p25 {p['p25']}, p75 {p['p75']}]  n_days={p['n']}" if med is not None else "no data"
            else:
                fr = p["frac_heavy_plus"]
                cell = f"frac_heavy+ {fr}  n_days={p['n']}" if fr is not None else "no data"
            print(f"      {p['phase_id']:3} {p['phase']:32} {cell}  (crashes={p['n_crashes']})")
    print(f"\n[R19] Wrote {HERE / 'summary.json'}")


if __name__ == "__main__":
    main()
