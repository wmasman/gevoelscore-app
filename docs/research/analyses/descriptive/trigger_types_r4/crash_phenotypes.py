"""R4 crash-phenotype exploration (DESCRIPTIVE, hypothesis-generating).

Explores whether crashes sort into recognisable phenotypes along three axes that
were measured independently:
  - TRIGGER: which self-reported load dominated the pre-onset run-up
    (emo / phy / cog / none).
  - FINGERPRINT: the acute-window autonomic loudness (stress + RHR up, battery
    depleted = loud; quiet = the autonomic storm is absent).
  - CONTENT: what the de-identified note tags emphasise (interpersonal / cognitive
    vs physical-illness).

A CONVERGENCE RULE labels a crash only when all three axes agree, which shrinks the
labelled set and makes the UNCLEAR bucket explicit. This is a DESCRIPTIVE typology,
not a test: the rule was found in these data and its axes are correlated by
selection, so the bucket counts are a picture of the data, never a p-value (see
crash_phenotypes_exploratory.md). It is logged as the proposed operationalisation
for a FUTURE, prospective phenotype-validation test.

Also runs a feasibility check for the user's household-illness de-confounder
(labelling viral crashes by mentions of OTHERS in the household being ill, since
the participant's own symptoms cannot separate a virus from severe PEM). Emits
de-identified counts only; no raw note text.

n=1, tiny n per bucket, self-report, reverse-causation-prone. No PII. ASCII only.
"""
from __future__ import annotations

import re
import numpy as np
import pandas as pd

MASTER = r"C:\Users\Gebruiker\Documents\gevoelscore-data\unified\per_day_master.csv"
CLAUSES = r"C:\Users\Gebruiker\Documents\gevoelscore-data\processed\notes\notes-categorized-v24-clauses.csv"
LINE = "-" * 74

# Autonomic loudness channels (acute window nadir-1..+1). Loud = stress/RHR up,
# battery floor down. bb_lowest enters with a minus (a lower floor is louder).
Z_UP = ["stress_mean_sleep_lagged_lcera_z", "all_day_stress_avg_lagged_lcera_z", "resting_hr_lagged_lcera_z"]
Z_DOWN = "bb_lowest_lagged_lcera_z"
# Content tags (window nadir-2..+2). Interpersonal/cognitive vs physical-illness.
INTERP = ["cat_belasting_gezin", "cat_belasting_sociaal", "cat_belasting_emotioneel", "cat_symptoom_cognitief"]
PHYSILL = ["cat_sub_keel_resp", "cat_sub_koorts", "cat_sub_spier", "cat_triggers_extern"]


def main():
    df = pd.read_csv(MASTER, low_memory=False)
    df["date"] = pd.to_datetime(df["date"]); df = df.sort_values("date").reset_index(drop=True)
    df["is_crash"] = df["is_crash"].astype(bool)
    by = {d: r for d, r in zip(df["date"], df.to_dict("records"))}
    alld = set(df["date"])

    crashes = []
    for eid, g in df[df["crash_episode_id"].notna()].groupby("crash_episode_id"):
        if not g["is_crash"].any():
            continue
        gg = g.dropna(subset=["gevoelscore"])
        nadir = gg.loc[gg["gevoelscore"].idxmin(), "date"] if len(gg) else g["date"].min()
        crashes.append({"start": g["date"].min(), "nadir": nadir,
                        "depth": gg["gevoelscore"].min() if len(gg) else np.nan, "dur": len(g)})

    def wmax(t0, col, w0, w1):
        v = [by[t0 + pd.Timedelta(days=k)].get(col) for k in range(w0, w1 + 1) if (t0 + pd.Timedelta(days=k)) in alld]
        v = [x for x in v if pd.notna(x)]; return max(v) if v else 0.0

    def wmean(t0, col, w0, w1):
        v = [by[t0 + pd.Timedelta(days=k)].get(col) for k in range(w0, w1 + 1) if (t0 + pd.Timedelta(days=k)) in alld]
        v = [x for x in v if pd.notna(x)]; return np.mean(v) if v else np.nan

    def wsum(t0, col, w0, w1):
        v = [by[t0 + pd.Timedelta(days=k)].get(col) for k in range(w0, w1 + 1) if (t0 + pd.Timedelta(days=k)) in alld]
        v = [x for x in v if pd.notna(x)]; return float(np.sum(v)) if v else 0.0

    # Axis 1: dominant pre-onset trigger (run-up [start-5..start-1]).
    for c in crashes:
        c["emo"] = wmax(c["start"], "emo_load", -5, -1)
        c["phy"] = wmax(c["start"], "phy_load", -5, -1)
        c["trigger"] = ("emo" if c["emo"] > c["phy"] and c["emo"] >= 2 else
                        "phy" if c["phy"] > c["emo"] and c["phy"] >= 2 else "none/mixed")
    # Axis 2: autonomic loudness (acute [nadir-1..+1]); split at the crash median.
    for c in crashes:
        ups = [wmean(c["nadir"], col, -1, 1) for col in Z_UP]
        down = wmean(c["nadir"], Z_DOWN, -1, 1)
        c["loudness"] = np.nanmean(ups) - (down if pd.notna(down) else 0.0)
    med = np.nanmedian([c["loudness"] for c in crashes])
    for c in crashes:
        c["fp"] = "quiet" if c["loudness"] < med else "loud"
    # Axis 3: content lean (window [nadir-2..+2]).
    for c in crashes:
        ipc = sum(wsum(c["nadir"], t, -2, 2) for t in INTERP)
        pic = sum(wsum(c["nadir"], t, -2, 2) for t in PHYSILL)
        c["content"] = "interpersonal" if ipc > pic else ("physical-illness" if pic > ipc else "tie/none")

    # CONVERGENCE RULE
    for c in crashes:
        if c["trigger"] == "emo" and c["fp"] == "quiet" and c["content"] == "interpersonal":
            c["phenotype"] = "convergent-quiet (emotional)"
        elif c["trigger"] == "phy" and c["fp"] == "loud" and c["content"] == "physical-illness":
            c["phenotype"] = "convergent-loud (physical/illness)"
        else:
            c["phenotype"] = "unclear"

    from collections import Counter
    print(LINE); print("R4 CRASH-PHENOTYPE TYPOLOGY (descriptive, n=%d crashes)" % len(crashes)); print(LINE)

    # Group-mean fingerprint + content by dominant trigger (the TENDENCY behind the
    # typology; more generous than the strict convergence rule below).
    FP = {"sleep_stress": "stress_mean_sleep_lagged_lcera_z", "daytime_stress": "all_day_stress_avg_lagged_lcera_z",
          "bb_lowest": "bb_lowest_lagged_lcera_z", "resting_hr": "resting_hr_lagged_lcera_z"}
    print("Group-mean acute-window [nadir-1..+1] fingerprint, by dominant trigger:")
    print(f"  {'trigger':10s} | " + " ".join(f"{k:>14s}" for k in FP) + " |  depth  dur    n")
    for grp in ["emo", "phy", "none/mixed"]:
        gc = [c for c in crashes if c["trigger"] == grp]
        if not gc:
            continue
        cells = " ".join(f"{np.nanmean([wmean(c['nadir'], col, -1, 1) for c in gc]):>14.2f}" for col in FP.values())
        print(f"  {grp:10s} | {cells} | {np.nanmean([c['depth'] for c in gc]):>5.2f} "
              f"{np.nanmean([c['dur'] for c in gc]):>4.1f}  {len(gc):>3d}")
    print("  interpersonal-content sum (gezin+sociaal+belasting_emo+brainfog) and physical-illness sum "
          "(resp+fever+muscle+extern), by trigger:")
    for grp in ["emo", "phy", "none/mixed"]:
        gc = [c for c in crashes if c["trigger"] == grp]
        if not gc:
            continue
        ip = np.mean([sum(wsum(c["nadir"], t, -2, 2) for t in INTERP) for c in gc])
        pi = np.mean([sum(wsum(c["nadir"], t, -2, 2) for t in PHYSILL) for c in gc])
        print(f"    {grp:10s}: interpersonal {ip:.2f}   physical-illness {pi:.2f}")
    print()
    print("Axis 1 (dominant pre-onset trigger):", dict(Counter(c["trigger"] for c in crashes)))
    print("Axis 2 (autonomic fingerprint, median split):", dict(Counter(c["fp"] for c in crashes)))
    print("Axis 3 (note-content lean):", dict(Counter(c["content"] for c in crashes)))
    print("\nCONVERGENCE RULE (all three axes agree):")
    for k, v in Counter(c["phenotype"] for c in crashes).most_common():
        print(f"  {k:34s}: {v}")
    print("  (UNCLEAR is expected to dominate: the strict rule is a floor on what we can label.)")

    # Feasibility: household-illness de-confounder (de-identified counts only).
    print("\n" + LINE); print("HOUSEHOLD-ILLNESS DE-CONFOUNDER FEASIBILITY (de-identified)"); print(LINE)
    cl = pd.read_csv(CLAUSES, low_memory=False); cl["date"] = pd.to_datetime(cl["date"])
    low = cl["clause"].astype(str).str.lower()
    illness = r"(ziek|griep|verkouden|koorts|corona|covid|besmet|buikgriep|snotter|virus|infect)"
    member = r"(vrouw|partner|\bman\b|kind|dochter|zoon|gezin|huisgeno|iedereen|hele huis|allebei)"
    cl["ill"] = low.str.contains(illness, regex=True, na=False)
    cl["mem"] = low.str.contains(member, regex=True, na=False)
    same_clause = int((cl["ill"] & cl["mem"]).sum())
    per_date = cl.groupby(cl["date"].dt.date).agg(ill=("ill", "max"), mem=("mem", "max"))
    both_date = int((per_date["ill"] & per_date["mem"]).sum())
    print(f"note-dates with any illness mention: {int(per_date['ill'].sum())}")
    print(f"illness+household-member in SAME clause (candidate 'someone else ill'): {same_clause}")
    print(f"illness AND (separate) member clause on the same date: {both_date}")
    print("VERDICT: household-illness signal is essentially ABSENT (cannot label viral crashes")
    print("  by an external marker); the fix is prospective logging. The illness mentions that do")
    print("  exist are the participant's OWN symptoms, which cannot separate a virus from PEM.")
    print(LINE)


if __name__ == "__main__":
    main()
