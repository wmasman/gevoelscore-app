"""Re-tag the H02b specificity-check false-positive windows with crash_v2 labels.

The original specificity check used `near_miss` = any score-3 day in window
to categorize false-positive spike windows. With crash_v2 labels, we can now
ask:
  - How many `near_miss` false positives actually contain a v2 `dip`?
  - How many `unexplained` ones do?
  - Does the near_miss -> v2_dip mapping confirm crash_v2 explains the
    false positives?

Reproduces the same null sample (same seed 20260605) and adds a new tag
`v2_dip_in_window` = True if any day in [d-3, d-1, ref] has label='dip'.

Output: specificity_retag.md.
"""
from __future__ import annotations

import collections
import csv
import json
import random
import statistics
from datetime import date, datetime, timedelta
from pathlib import Path

# Identical constants to H02b specificity_check.py
ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3
LEADUP_DAYS = 3
BASELINE_WINDOW_DAYS = 90
MIN_LEADUP_VALID = 2
MIN_BASELINE_VALID = 30
TRIMMED_PCT = 0.10
NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605
CRIT_A_DELTA_MIN = 10
NEAR_MISS_SCORE = 3
CLOSE_TO_CRASH_DAYS = 14

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABELS_CSV = ROOT / "labels_crash_v2.csv"
DAY_ENTRIES_CSV = ROOT.parent / "H02b-stress-spikes" / "day_entries.csv"
SPIKE_CSV = ROOT.parent / "H02b-stress-spikes" / "daily_max_spike.csv"
OUT_MD = ROOT / "specificity_retag.md"


def load_day_entries() -> dict[date, int]:
    out = {}
    with DAY_ENTRIES_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            s = r["score"]
            if s in ("", "None"):
                continue
            out[date.fromisoformat(r["date"])] = int(s)
    return out


def load_v2_labels() -> dict[date, str]:
    out = {}
    with LABELS_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[date.fromisoformat(r["date"])] = r["label"]
    return out


def load_spike_by_date() -> dict[date, float]:
    out = {}
    with SPIKE_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1":
                continue
            out[date.fromisoformat(r["date"])] = float(r["max_spike_minutes"])
    return out


def find_crash_episodes(day_scores):
    sorted_dates = sorted(d for d in day_scores
                          if ANALYSIS_START <= d <= VALIDATE_END)
    runs, cur = [], None
    for d in sorted_dates:
        is_low = day_scores[d] <= LOW_THRESHOLD
        if not is_low:
            if cur and cur["days"] >= MIN_RUN_DAYS:
                runs.append(cur)
            cur = None
            continue
        if not cur:
            cur = {"start": d, "end": d, "days": 1}
            continue
        if (d - cur["end"]).days == 1:
            cur["end"] = d
            cur["days"] += 1
        else:
            if cur["days"] >= MIN_RUN_DAYS:
                runs.append(cur)
            cur = {"start": d, "end": d, "days": 1}
    if cur and cur["days"] >= MIN_RUN_DAYS:
        runs.append(cur)
    merged = []
    for r in runs:
        if merged and (r["start"] - merged[-1]["end"]).days <= MERGE_WITHIN_DAYS:
            merged[-1]["end"] = r["end"]
            merged[-1]["days"] += r["days"]
        else:
            merged.append({"start": r["start"], "end": r["end"], "days": r["days"]})
    return merged


def trimmed_mean(vals, pct):
    if not vals:
        return None
    s = sorted(vals)
    n = len(s)
    trim = int(n * pct)
    if n - 2 * trim < 1:
        return statistics.mean(s)
    return statistics.mean(s[trim : n - trim])


def compute_window(ref, spike_by_date):
    leadup = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    baseline_start = ref - timedelta(days=BASELINE_WINDOW_DAYS + LEADUP_DAYS)
    baseline_end = ref - timedelta(days=LEADUP_DAYS + 1)
    bds = []
    d = baseline_start
    while d <= baseline_end:
        bds.append(d)
        d += timedelta(days=1)
    leadup_vals = [(d, spike_by_date[d]) for d in leadup if d in spike_by_date]
    baseline_vals = [spike_by_date[d] for d in bds if d in spike_by_date]
    if len(leadup_vals) < MIN_LEADUP_VALID or len(baseline_vals) < MIN_BASELINE_VALID:
        return {"delta": None}
    leadup_max = max(v for _, v in leadup_vals)
    baseline_mean = trimmed_mean(baseline_vals, TRIMMED_PCT)
    peak_day = max(leadup_vals, key=lambda x: x[1])[0]
    return {
        "leadup_dates": [d for d, _ in leadup_vals],
        "leadup_max": leadup_max,
        "baseline_mean": baseline_mean,
        "peak_day": peak_day,
        "delta": leadup_max - baseline_mean,
    }


def build_null_sample(spike_by_date, crash_lead_up_days, n):
    """Mirrors H02b/specificity_check.py exactly."""
    rng = random.Random(RANDOM_SEED)
    all_dates = sorted(d for d in spike_by_date
                       if ANALYSIS_START <= d <= VALIDATE_END)
    out = []
    attempts = 0
    max_attempts = n * 50
    while len(out) < n and attempts < max_attempts:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)}
        if leadup & crash_lead_up_days:
            continue
        prof = compute_window(ref, spike_by_date)
        if prof["delta"] is None:
            continue
        out.append({"ref": ref, **prof})
    return out


def categorize_window(w, day_scores, v2_labels, episodes):
    ref = w["ref"]
    leadup = w["leadup_dates"]
    days_to_check = [*leadup, ref]
    scores = [(d, day_scores.get(d)) for d in days_to_check]
    near_miss = any(s == NEAR_MISS_SCORE for _, s in scores if s is not None)
    v2_dip_days = [d for d in days_to_check if v2_labels.get(d) == "dip"]
    v2_dip_in_window = bool(v2_dip_days)

    crash_starts = [ep["start"] for ep in episodes]
    nearest = min(crash_starts, key=lambda c: abs((c - ref).days))
    days_to_crash = (nearest - ref).days
    close_to_crash = (abs(days_to_crash) <= CLOSE_TO_CRASH_DAYS and not
                      (-LEADUP_DAYS <= days_to_crash <= 0))

    tags = []
    if near_miss:
        tags.append("near_miss")
    if v2_dip_in_window:
        tags.append("v2_dip")
    if close_to_crash:
        tags.append("close_to_crash")
    if not (near_miss or close_to_crash):
        tags.append("unexplained")

    return {
        "ref": ref,
        "delta": w["delta"],
        "scores": scores,
        "near_miss": near_miss,
        "v2_dip_in_window": v2_dip_in_window,
        "v2_dip_days": v2_dip_days,
        "close_to_crash": close_to_crash,
        "days_to_crash": days_to_crash,
        "tags": tags,
    }


def main():
    print("Loading data…")
    day_scores = load_day_entries()
    v2_labels = load_v2_labels()
    spike_by_date = load_spike_by_date()
    episodes = find_crash_episodes(day_scores)
    print(f"  {len(day_scores)} scored days | {len(v2_labels)} labels | "
          f"{len(spike_by_date)} valid stress days | {len(episodes)} crashes")

    all_leadup_days = set()
    for ep in episodes:
        for i in range(1, LEADUP_DAYS + 1):
            all_leadup_days.add(ep["start"] - timedelta(days=i))

    print(f"Reproducing the H02b null sample (seed {RANDOM_SEED})…")
    null = build_null_sample(spike_by_date, all_leadup_days, NULL_SAMPLE_SIZE)
    print(f"  null sample: {len(null)}")

    fp = [w for w in null if w["delta"] >= CRIT_A_DELTA_MIN]
    print(f"  false positives (delta >= +{CRIT_A_DELTA_MIN}): {len(fp)} "
          f"({100*len(fp)/len(null):.0f}%)")

    enriched = [categorize_window(w, day_scores, v2_labels, episodes) for w in fp]

    # Cross-tab near_miss vs v2_dip
    crosstab = collections.Counter()
    for e in enriched:
        nm = e["near_miss"]
        vd = e["v2_dip_in_window"]
        crosstab[(nm, vd)] += 1

    print("\n=== near_miss vs v2_dip cross-tab ===")
    print(f"  near_miss=True,  v2_dip=True:  {crosstab[(True, True)]}")
    print(f"  near_miss=True,  v2_dip=False: {crosstab[(True, False)]}")
    print(f"  near_miss=False, v2_dip=True:  {crosstab[(False, True)]}")
    print(f"  near_miss=False, v2_dip=False: {crosstab[(False, False)]}")

    # Write MD
    lines = []
    lines.append("# Specificity re-tag — H02b false positives under crash_v2\n")
    lines.append("Reproduces H02b's specificity-check null sample (seed "
                 f"`{RANDOM_SEED}`) and re-tags each false-positive window "
                 "(delta >= +10 min) with crash_v2 labels.\n")
    lines.append("**Key question:** the original specificity check tagged "
                 "32/83 false positives as `near_miss` (any score-3 day in "
                 "window). With crash_v2, those score-3 days should now be "
                 "labelled `dip`. Does the mapping hold?\n")
    lines.append("## Counts\n")
    lines.append(f"- Null sample size: **{len(null)}**\n")
    lines.append(f"- False positives (delta >= +{CRIT_A_DELTA_MIN}): "
                 f"**{len(enriched)}** ({100*len(enriched)/len(null):.0f}%)\n")
    lines.append("\n### Cross-tab: `near_miss` (orig) vs `v2_dip_in_window` (new)\n")
    lines.append("| | v2_dip=True | v2_dip=False | total |\n"
                 "|---|---:|---:|---:|\n"
                 f"| **near_miss=True**  | {crosstab[(True, True)]} | "
                 f"{crosstab[(True, False)]} | "
                 f"{crosstab[(True, True)]+crosstab[(True, False)]} |\n"
                 f"| **near_miss=False** | {crosstab[(False, True)]} | "
                 f"{crosstab[(False, False)]} | "
                 f"{crosstab[(False, True)]+crosstab[(False, False)]} |\n"
                 f"| **total** | "
                 f"{crosstab[(True, True)]+crosstab[(False, True)]} | "
                 f"{crosstab[(True, False)]+crosstab[(False, False)]} | "
                 f"{len(enriched)} |\n")
    lines.append("**How to read:** the (True, True) cell counts windows where "
                 "the old `near_miss` tag is now confirmed by a v2 dip label. "
                 "(True, False) = old `near_miss` but no v2 dip — these are "
                 "score-3 days that are part of a crash episode (tier-1) or "
                 "in a crash recovery shadow. (False, True) = NEW dips that "
                 "weren't near_miss (likely v2 dip with score 1 or 2, which "
                 "the old NEAR_MISS_SCORE=3 rule missed).\n")
    lines.append("\n## Per-window detail (sorted by delta, descending)\n")
    lines.append("| ref | delta | scores [d-3,d-2,d-1,ref] | near_miss (orig) | "
                 "v2_dip_in_window | v2_dip_days | days_to_crash | tags |")
    lines.append("|---|---:|---|---|---|---|---:|---|")
    for e in sorted(enriched, key=lambda x: -x["delta"]):
        scores_str = ",".join(str(s) if s is not None else "?" for _, s in e["scores"])
        v2_days_str = ", ".join(d.isoformat() for d in e["v2_dip_days"]) or "—"
        lines.append(
            f"| {e['ref'].isoformat()} | {e['delta']:+.1f} | {scores_str} | "
            f"{'YES' if e['near_miss'] else '—'} | "
            f"{'YES' if e['v2_dip_in_window'] else '—'} | "
            f"{v2_days_str} | {e['days_to_crash']:+d} | "
            f"{', '.join(e['tags'])} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated 2026-06-06. Same null sample as "
                 "H02b/specificity-check.md.*")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {OUT_MD}")


if __name__ == "__main__":
    main()
