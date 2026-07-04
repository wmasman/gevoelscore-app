"""R4 crash-specificity: does load INTENSITY (not presence) precede crashes?

Follow-up to precondition_analysis.py. The precondition showed that load
PRESENCE is degenerate (ambient base rate 48-74%, no crash contrast). This asks
the intensity-graded question: do SEVERE (level-3) or MODERATE+ (level-2+) loads
of each type elevate in the pre-onset run-up of a crash, versus ordinary windows?

Design (all pre-committed here, descriptive):
  - Trigger window = [episode-start - 5 .. episode-start - 1], i.e. the five days
    BEFORE the crash begins. Excludes the crash days themselves, so a load is a
    pre-onset trigger candidate, not the crash being logged.
  - Crash units: the 29 crash-episode starts (min date per crash_episode_id with
    an is_crash day).
  - Ordinary comparison: LC-corpus days at least 7 days from ANY crash day
    (so ordinary run-ups do not overlap a crash).
  - Statistics: for each load type, the crash-vs-ordinary difference in
    P(severe >= 3 in run-up), P(moderate+ >= 2), and mean run-up max-load, each
    with a two-group bootstrap 95% CI and a label-permutation p-analogue.
  - Confound reads: recovery_phase-stratified severe rate (era/note-density
    control), and infection (cat_triggers_extern) in a wider pre-onset window.

"stress" is not used here (this is self-report load vs crash timing). No PII.
ASCII only. Descriptive; no causal marks. Seed 20260704.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

RNG = np.random.default_rng(20260704)
MASTER = r"C:\Users\Gebruiker\Documents\gevoelscore-data\unified\per_day_master.csv"
LC_CORPUS_START = "2022-09-03"
W0, W1 = -5, -1          # pre-onset run-up window
INF_W0, INF_W1 = -14, -1  # wider pre-onset window for infection (incubation)
CRASH_BUFFER = 7         # ordinary days must be >= this many days from any crash day
N_BOOT = 4000
N_PERM = 10000
LINE = "-" * 74


def load():
    df = pd.read_csv(MASTER, low_memory=False)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["is_crash"] = df["is_crash"].astype(bool)
    return df


def main():
    df = load()
    alld = set(df["date"])
    by = {d: r for d, r in zip(df["date"], df.to_dict("records"))}
    phase = {d: p for d, p in zip(df["date"], df["recovery_phase"])}
    lc = df[df["date"] >= LC_CORPUS_START]

    # crash episode START day + the set of all crash-episode days
    starts, crash_days = [], set()
    for eid, g in df[df["crash_episode_id"].notna()].groupby("crash_episode_id"):
        if not g["is_crash"].any():
            continue
        starts.append(g["date"].min())
        crash_days.update(g["date"].tolist())
    starts = sorted(starts)

    def near_crash(d):
        return any(abs((d - cd).days) <= CRASH_BUFFER for cd in crash_days)

    ordinary = [d for d in lc["date"] if not near_crash(d)]

    def maxlev(t0, col, w0=W0, w1=W1):
        vals = [by[t0 + pd.Timedelta(days=k)].get(col)
                for k in range(w0, w1 + 1) if (t0 + pd.Timedelta(days=k)) in alld]
        vals = [v for v in vals if pd.notna(v)]
        return max(vals) if vals else 0.0

    print(LINE)
    print("R4 CRASH-SPECIFICITY BY LOAD INTENSITY (pre-onset run-up)")
    print(f"crash episodes: {len(starts)}   ordinary anchor days (>= {CRASH_BUFFER}d from any crash): {len(ordinary)}")
    print(f"run-up window: [start{W0}..start{W1}]   boot {N_BOOT}   perm {N_PERM}   seed 20260704")
    print(LINE)

    def boot_ci_diff(cv, ov, fn):
        cv = np.asarray(cv, float); ov = np.asarray(ov, float)
        obs = fn(cv) - fn(ov)
        ds = np.empty(N_BOOT)
        for i in range(N_BOOT):
            ds[i] = fn(RNG.choice(cv, len(cv), replace=True)) - fn(RNG.choice(ov, len(ov), replace=True))
        return obs, float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5))

    def perm_p(cv, ov, fn):
        cv = np.asarray(cv, float); ov = np.asarray(ov, float)
        obs = fn(cv) - fn(ov)
        pool = np.concatenate([cv, ov]); nC = len(cv); ge = 0
        for _ in range(N_PERM):
            RNG.shuffle(pool)
            if (fn(pool[:nC]) - fn(pool[nC:])) >= obs:
                ge += 1
        return (ge + 1) / (N_PERM + 1)

    LOADS = [("phy_load", "physical"), ("emo_load", "emotional"), ("cog_load", "cognitive")]
    sev = lambda a: (a >= 3).mean()
    mod = lambda a: (a >= 2).mean()
    avg = lambda a: a.mean()

    for col, nm in LOADS:
        cv = np.array([maxlev(t0, col) for t0 in starts])
        ov = np.array([maxlev(t0, col) for t0 in ordinary])
        print(f"\n{nm.upper()}  (crash n={len(cv)}, ordinary n={len(ov)})")
        for label, fn, fmt in [("P(severe >=3)", sev, "pp"), ("P(moderate+ >=2)", mod, "pp"),
                               ("mean max-load", avg, "raw")]:
            obs, lo, hi = boot_ci_diff(cv, ov, fn)
            p = perm_p(cv, ov, fn)
            cval, oval = fn(cv), fn(ov)
            if fmt == "pp":
                star = "*" if (lo > 0 or hi < 0) else " "
                print(f"    {label:18s}: crash {100*cval:4.0f}%  ord {100*oval:4.0f}%  "
                      f"diff {100*obs:+4.0f}pp [{100*lo:+.0f},{100*hi:+.0f}]{star}  perm-p {p:.3f}")
            else:
                star = "*" if (lo > 0 or hi < 0) else " "
                print(f"    {label:18s}: crash {cval:4.2f}   ord {oval:4.2f}   "
                      f"diff {obs:+.2f} [{lo:+.2f},{hi:+.2f}]{star}  perm-p {p:.3f}")

    # recovery_phase-stratified severe rate (era / note-density control)
    print(f"\n{LINE}\nPHASE-STRATIFIED P(severe >=3) [crash vs ordinary], nC = crashes in phase:")
    phases = [p for p in sorted(set(v for v in phase.values() if pd.notna(v)))]
    for col, nm in LOADS:
        cells = []
        for ph in phases:
            cs = [maxlev(t0, col) >= 3 for t0 in starts if phase.get(t0) == ph]
            os_ = [maxlev(t0, col) >= 3 for t0 in ordinary if phase.get(t0) == ph]
            if len(cs) >= 2 and len(os_) >= 5:
                cells.append(f"{ph}:{100*np.mean(cs):.0f}v{100*np.mean(os_):.0f}(nC{len(cs)})")
        print(f"    {nm:10s}: " + "   ".join(cells))
    print("    (single-pool primacy: these are numbers, not per-phase verdicts.)")

    # infection pre-onset (wider window)
    def has_inf(t0):
        return any((by[t0 + pd.Timedelta(days=k)].get("cat_triggers_extern") or 0) >= 1
                   for k in range(INF_W0, INF_W1 + 1) if (t0 + pd.Timedelta(days=k)) in alld)
    ci = np.mean([has_inf(t0) for t0 in starts]); oi = np.mean([has_inf(t0) for t0 in ordinary])
    print(f"\nINFECTION (cat_triggers_extern >=1) in [start{INF_W0}..start{INF_W1}]: "
          f"crash {100*ci:.0f}%  vs ordinary {100*oi:.0f}%  "
          f"(pre-onset; contrast with the nadir-inclusive 7% which co-occurs with the crash)")
    print(LINE)


if __name__ == "__main__":
    main()
