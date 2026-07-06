"""R4 trigger-types descriptive precondition: reproducible analysis.

Produces every number cited in precondition.md. Two threads:

  A. Trigger-data availability + crash-run-up specificity (the R4 precondition
     proper): do we have enough self-reported trigger data, and is it
     crash-specific?
  B. Garmin autonomic concordance (a data-description finding in its own right):
     does each self-reported load type (physical / emotional / cognitive) leave
     a distinct autonomic fingerprint in the wearable channels?

Trigger data (per DATA_DICTIONARY.md):
  - Section 2 "manual load triage": cog_load / phy_load / emo_load, each 1/2/3
    (mild / moderate / severe event intensity), presence-conditioned, gated on
    has_intensity_triage (intensity_source != ""). A blank load on a reviewed
    day = no such event noted; NaN off-triage = not reviewed.
  - Section 9 "note categorisation rollup": cat_belasting_* clause counts
    (fysiek / emotioneel / cognitief / gezin / sociaal), note-derived (gate
    has_note), and cat_triggers_extern (corona / griep / infectie).

"stress" throughout = Garmin HRV-derived Stress Score (GSS), never mental
stress. No PII. ASCII only. Descriptive; no causal marks.

Seed 20260704 (only the bootstrap CIs use it).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

RNG = np.random.default_rng(20260704)
MASTER = r"C:\Users\Gebruiker\Documents\gevoelscore-data\unified\per_day_master.csv"
LC_CORPUS_START = "2022-09-03"  # gevoelscore logging start (Stratum-4 surface)
LINE = "-" * 74

# Garmin channels grouped by what they plausibly reflect. Lagged-lcera ranks
# (0-1) or personal-baseline z-scores, so each is already baseline-relative.
CH = {
    "max_hr_rank": "max_hr_rank_lagged_lcera",           # peak cardiac strain
    "eff_exertion_rank": "eff_exertion_rank_lagged_lcera",  # activity volume
    "daytime_stress_z": "all_day_stress_avg_lagged_lcera_z",  # daytime GSS
    "sleep_stress_z": "stress_mean_sleep_lagged_lcera_z",    # overnight GSS
    "bb_lowest_z": "bb_lowest_lagged_lcera_z",           # body-battery floor
    "resting_hr_z": "resting_hr_lagged_lcera_z",         # RHR
}
LOADS = ["phy_load", "emo_load", "cog_load"]


def load_lc():
    df = pd.read_csv(MASTER, low_memory=False)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["is_crash"] = df["is_crash"].astype(bool)
    df["is_dip"] = df["is_dip"].astype(bool)
    lc = df[df["date"] >= LC_CORPUS_START].copy()
    for l in LOADS:
        lc[l + "_ev"] = lc[l].notna()
    return df, lc


def boot_delta(a, b, nb=4000):
    a = pd.Series(a).dropna().values
    b = pd.Series(b).dropna().values
    if len(a) < 3 or len(b) < 3:
        return (np.nan, np.nan, np.nan)
    d = a.mean() - b.mean()
    ds = [RNG.choice(a, len(a), replace=True).mean() - RNG.choice(b, len(b), replace=True).mean()
          for _ in range(nb)]
    return d, float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5))


def main():
    df, lc = load_lc()
    n = len(lc)
    alld = set(df["date"])
    by = {d: r for d, r in zip(df["date"], df.to_dict("records"))}

    print(LINE)
    print("R4 TRIGGER-TYPES DESCRIPTIVE PRECONDITION")
    print(f"LC corpus (>= {LC_CORPUS_START}): {n} days   full record: {len(df)} days")
    print(LINE)

    # ========================================================================
    # A. TRIGGER-DATA AVAILABILITY
    # ========================================================================
    print("A1. Section-2 manual load-triage coverage (the 1-3 scores):")
    for c in ["phy_load", "emo_load", "cog_load"]:
        k = lc[c].notna().sum()
        print(f"    {c:10s}: {k:4d} / {n} = {100 * k / n:4.1f}% of days carry an event")
    src = lc["intensity_source"].fillna("")
    triaged = int((src != "").sum())
    no_info = int(src.str.contains("no_info", na=False).sum())
    print(f"    has_intensity_triage (reviewed): {triaged} = {100 * triaged / n:.1f}%   "
          f"_no_info (reviewed, no signal): {no_info}   context-sufficient: {triaged - no_info}")
    print("    intensity distribution (1/2/3):")
    for c in ["phy_load", "emo_load", "cog_load"]:
        vc = lc[c].value_counts(dropna=True).sort_index()
        print(f"      {c:10s}: " + ", ".join(f"L{int(k)}:{int(v)}" for k, v in vc.items()))

    print("\nA2. Section-9 note-layer coverage (cat_belasting_* + cat_triggers_extern):")
    for c in ["cat_belasting_fysiek", "cat_belasting_emotioneel", "cat_belasting_cognitief",
              "cat_belasting_gezin", "cat_belasting_sociaal", "cat_triggers_extern"]:
        k = lc[c].notna().sum()
        print(f"    {c:26s}: {k:4d} / {n} = {100 * k / n:4.1f}% note-categorised")

    print("\nA3. Load-event co-occurrence (LC days):")
    p, e, c = lc.phy_load_ev, lc.emo_load_ev, lc.cog_load_ev
    print(f"    phy-only {int((p & ~e & ~c).sum())}   emo-only {int((~p & e & ~c).sum())}   "
          f"cog-only {int((~p & ~e & c).sum())}   any-two+ {int(((p.astype(int)+e+c) >= 2).sum())}   "
          f"none {int((~p & ~e & ~c).sum())}")

    # ------------------------------------------------------------------
    # A4. Peri-crash coverage + base-rate specificity
    # ------------------------------------------------------------------
    nadirs = []
    for eid, g in df[df["crash_episode_id"].notna()].groupby("crash_episode_id"):
        if not g["is_crash"].any():
            continue
        gg = g.dropna(subset=["gevoelscore"])
        if len(gg):
            nadirs.append(gg.loc[gg["gevoelscore"].idxmin(), "date"])
    nadirs = sorted(nadirs)

    def win_has(t0, col, back=5, thresh=None):
        for k in range(-back, 1):
            d = t0 + pd.Timedelta(days=k)
            if d not in alld:
                continue
            v = by[d].get(col)
            if thresh is None:
                if pd.notna(v):
                    return True
            else:
                if (v or 0) >= thresh:
                    return True
        return False

    def crash_rate(col, thresh=None):
        return np.mean([win_has(t0, col, 5, thresh) for t0 in nadirs])

    def base_rate(col, thresh=None):
        return np.mean([win_has(t0, col, 5, thresh) for t0 in lc["date"]])

    print(f"\nA4. Peri-crash run-up [nadir-5..nadir], {len(nadirs)} crashes:")
    any3 = np.mean([(win_has(t0, "phy_load") or win_has(t0, "emo_load") or win_has(t0, "cog_load"))
                    for t0 in nadirs])
    ctx = np.mean([any((str(by[t0 + pd.Timedelta(days=k)].get("intensity_source") or "") != ""
                        and "no_info" not in str(by[t0 + pd.Timedelta(days=k)].get("intensity_source") or ""))
                       for k in range(-5, 1) if (t0 + pd.Timedelta(days=k)) in alld) for t0 in nadirs])
    print(f"    any structured load in run-up: {100*any3:.0f}%   context-reviewed run-ups: {100*ctx:.0f}%")
    print("    crash-run-up rate vs random-window base rate (elevation = specificity):")
    for c in ["phy_load", "emo_load", "cog_load"]:
        print(f"      {c:10s}: crash {100*crash_rate(c):3.0f}%  vs base {100*base_rate(c):3.0f}%  "
              f"(per-day base {100*lc[c].notna().mean():4.1f}%)")
    print(f"      infection : crash {100*crash_rate('cat_triggers_extern',1):3.0f}%  "
          f"vs base {100*base_rate('cat_triggers_extern',1):3.0f}%  "
          f"(per-day base {100*(lc['cat_triggers_extern'].fillna(0)>=1).mean():4.1f}%)")

    # ========================================================================
    # B. GARMIN AUTONOMIC CONCORDANCE
    # ========================================================================
    print("\n" + LINE)
    print("B. GARMIN AUTONOMIC CONCORDANCE (self-reported load vs wearable channels)")
    print(LINE)

    print("B1. Good-day confound: mean gevoelscore [load present vs absent]:")
    for l in LOADS:
        pp = lc.loc[lc[l].notna(), "gevoelscore"].mean()
        aa = lc.loc[lc[l].isna(), "gevoelscore"].mean()
        print(f"    {l:9s}: present {pp:.2f}  absent {aa:.2f}  delta {pp-aa:+.2f}")
    ie = lc[lc.emo_load_ev & ~lc.phy_load_ev]
    nn = lc[~lc.emo_load_ev & ~lc.phy_load_ev]
    print(f"    emo-isolated (emo & ~phy) gevoelscore {ie.gevoelscore.mean():.2f} "
          f"vs neither {nn.gevoelscore.mean():.2f}  delta {ie.gevoelscore.mean()-nn.gevoelscore.mean():+.2f}")

    def contrast(mask_a, mask_b, label):
        print(f"\n{label}   (raw delta [95% CI]  |  felt-state-adjusted delta [95% CI]; * = CI excludes 0)")
        A, B = lc[mask_a], lc[mask_b]
        AB = lc[mask_a | mask_b]
        for nm, col in CH.items():
            d, lo, hi = boot_delta(A[col], B[col])
            dd = AB[[col, "gevoelscore"]].dropna()
            if len(dd) >= 10:
                b1 = np.polyfit(dd["gevoelscore"], dd[col], 1)
                r = AB[col] - np.polyval(b1, AB["gevoelscore"])
                da, loa, hia = boot_delta(r[AB.index.isin(A.index)], r[AB.index.isin(B.index)])
            else:
                da = loa = hia = np.nan
            fr = "*" if (pd.notna(lo) and (lo > 0 or hi < 0)) else " "
            fa = "*" if (pd.notna(loa) and (loa > 0 or hia < 0)) else " "
            print(f"    {nm:18s}: raw {d:+.3f}[{lo:+.2f},{hi:+.2f}]{fr}  adj {da:+.3f}[{loa:+.2f},{hia:+.2f}]{fa}")

    contrast(lc.phy_load_ev, ~lc.phy_load_ev,
             "B2. PHYSICAL present vs absent")
    contrast(lc.cog_load_ev & ~lc.phy_load_ev, ~lc.cog_load_ev & ~lc.phy_load_ev,
             "B3. COGNITIVE isolated (cog & ~phy) vs neither")
    contrast(lc.emo_load_ev & ~lc.phy_load_ev, ~lc.emo_load_ev & ~lc.phy_load_ev,
             "B4. EMOTIONAL isolated (emo & ~phy) vs neither")

    # B5. Wiggers "HRV drops that night OR the following night" timing test.
    # Wiggers (handleiding, mental-PEM concession, PDF lines 1448-1457): excessive
    # mental activity is undetected in the activity view but "will cause your HRV to
    # drop that night or the following night." Overnight stress (GSS) is the
    # HRV-derived proxy (higher stress = lower HRV). Test cognitive (her example) and
    # emotional load at lag 0 (that night) and lag +1 (the following night).
    SLEEP = {"sleep_stress_z": "stress_mean_sleep_lagged_lcera_z", "bb_lowest_z": "bb_lowest_lagged_lcera_z"}

    def chan_at(d, col, lag):
        dd = d + pd.Timedelta(days=lag)
        return by[dd].get(col) if dd in alld else np.nan

    def lag_contrast(mask_a, mask_b, label):
        print(f"\n{label}   (that-night lag+0 / following-night lag+1; * = 95% CI excludes 0)")
        A, B = lc[mask_a], lc[mask_b]
        for nm, col in SLEEP.items():
            for lag in (0, 1):
                a = [chan_at(d, col, lag) for d in A["date"]]
                b = [chan_at(d, col, lag) for d in B["date"]]
                d, lo, hi = boot_delta(a, b)
                tag = "that-night " if lag == 0 else "next-night "
                star = "*" if (pd.notna(lo) and (lo > 0 or hi < 0)) else " "
                print(f"    {nm:14s} {tag}(lag+{lag}): diff {d:+.3f} [{lo:+.2f},{hi:+.2f}]{star}")

    print(f"\n{LINE}\nB5. WIGGERS 'HRV drop that night OR the following night' TIMING TEST")
    lag_contrast(lc.cog_load_ev & ~lc.phy_load_ev, ~lc.cog_load_ev & ~lc.phy_load_ev,
                 "COGNITIVE isolated (Wiggers' own 'laptop / writing' example)")
    lag_contrast((lc.cog_load == 3) & ~lc.phy_load_ev, lc.cog_load.isna() & ~lc.phy_load_ev,
                 "COGNITIVE severe L3 only ('excessive mental activity')")
    lag_contrast(lc.emo_load_ev & ~lc.phy_load_ev, ~lc.emo_load_ev & ~lc.phy_load_ev,
                 "EMOTIONAL isolated")

    print("\n(CIs are day-level bootstrap; autocorrelation not modelled -> treat as approximate/optimistic.)")
    print(LINE)


if __name__ == "__main__":
    main()
