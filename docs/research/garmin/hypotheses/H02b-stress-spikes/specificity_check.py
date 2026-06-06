"""H02b — Specificity check.

Reproduce the same 200-window null sample H02b used (seed 20260605),
filter to those that fired the +10 min spike criterion ("false
positives" from a predictor's point of view), and inspect what those
non-crash spike-windows actually contain.

For each false-positive window we check:
  1. The 3 lead-up days + the reference day: gevoelscore, written note
  2. Which day had the peak spike
  3. Whether a workout was recorded on the peak-spike day (activity-induced spike?)
  4. Distance to nearest crash episode (within an extended window?)

Then categorize each false positive into:
  - near_miss        : a day in window or just after had score = 3
                       (sub-threshold dip — crash_v1 was too strict)
  - activity_induced : workout overlaps the peak-spike day
  - close_to_crash   : within 7–14 days of an actual crash episode
                       (extended-window precursor v1 missed)
  - unexplained      : none of the above

This tells us what the false positives actually mean, which in turn
tells us whether crash_v1 is too strict, the spike extractor needs
activity filtering, or the signal is just noisy.
"""
from __future__ import annotations

import csv
import json
import random
import statistics
from datetime import date, datetime, timedelta
from pathlib import Path

# Mirror H02b test.py constants exactly
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

NEAR_MISS_SCORE = 3   # day with score = 3 in or just after the window
CLOSE_TO_CRASH_DAYS = 14  # any crash within ±14 days flagged
ACTIVITY_LONG_MIN = 30   # activity ≥ 30 min on the spike day = "significant"

HERE = Path(__file__).resolve().parent
DAY_ENTRIES_CSV = HERE / "day_entries.csv"
SPIKE_CSV = HERE / "daily_max_spike.csv"
NOTES_JSON = HERE.parent.parent.parent / "notes" / "01-language-around-crashes" / "day_entries_with_notes.json"
GARMIN_ACTIVITIES = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Fitness\user@example.com_0_summarizedActivities.json"
)
OUT_MD = HERE / "specificity-check.md"


# ─── Shared utilities (copied from test.py to keep this script standalone) ───
def load_day_entries() -> dict[date, int]:
    out: dict[date, int] = {}
    with DAY_ENTRIES_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            s = r["score"]
            if s in ("", "None", None):
                continue
            out[d] = int(s)
    return out


def load_day_notes() -> dict[date, str]:
    if not NOTES_JSON.exists():
        return {}
    out = {}
    for e in json.loads(NOTES_JSON.read_text(encoding="utf-8")):
        if e.get("note") and e["note"].strip():
            out[date.fromisoformat(e["date"])] = e["note"].strip()
    return out


def load_spike_by_date() -> dict[date, float]:
    out: dict[date, float] = {}
    with SPIKE_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1":
                continue
            out[date.fromisoformat(r["date"])] = float(r["max_spike_minutes"])
    return out


def load_activities() -> list[dict]:
    """Return list of {date, type, duration_min, name}."""
    out = []
    with GARMIN_ACTIVITIES.open(encoding="utf-8") as fh:
        data = json.load(fh)
    acts = data[0]["summarizedActivitiesExport"]
    for a in acts:
        ts = a.get("startTimeGmt")
        if ts is None:
            continue
        d = datetime.utcfromtimestamp(ts / 1000).date()
        out.append({
            "date": d,
            "type": a.get("activityType", "?"),
            "duration_min": round((a.get("duration") or 0) / 60, 1),
            "name": a.get("name", "-"),
        })
    return out


def find_crash_episodes(day_scores: dict[date, int]) -> list[dict]:
    sorted_dates = sorted(d for d in day_scores if ANALYSIS_START <= d <= VALIDATE_END)
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


def trimmed_mean(values, pct):
    if not values: return None
    s = sorted(values); n = len(s); trim = int(n * pct)
    if n - 2 * trim < 1: return statistics.mean(s)
    return statistics.mean(s[trim : n - trim])


def compute_window(ref: date, spike_by_date: dict[date, float]) -> dict:
    leadup = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    baseline_start = ref - timedelta(days=BASELINE_WINDOW_DAYS + LEADUP_DAYS)
    baseline_end = ref - timedelta(days=LEADUP_DAYS + 1)
    bds = []
    d = baseline_start
    while d <= baseline_end:
        bds.append(d); d += timedelta(days=1)
    leadup_vals = [(d, spike_by_date[d]) for d in leadup if d in spike_by_date]
    baseline_vals = [spike_by_date[d] for d in bds if d in spike_by_date]
    if len(leadup_vals) < MIN_LEADUP_VALID or len(baseline_vals) < MIN_BASELINE_VALID:
        return {"delta": None}
    leadup_max = max(v for _, v in leadup_vals)
    baseline_mean = trimmed_mean(baseline_vals, TRIMMED_PCT)
    peak_day = max(leadup_vals, key=lambda x: x[1])[0]
    return {
        "leadup_dates": [d for d, _ in leadup_vals],
        "leadup_values": [(d, v) for d, v in leadup_vals],
        "leadup_max": leadup_max,
        "baseline_mean": baseline_mean,
        "peak_day": peak_day,
        "delta": leadup_max - baseline_mean,
    }


def build_null_sample(spike_by_date, crash_lead_up_days, n):
    """Mirrors H02b test.py exactly so we get the same 200 windows."""
    rng = random.Random(RANDOM_SEED)
    all_dates = sorted(d for d in spike_by_date if ANALYSIS_START <= d <= VALIDATE_END)
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


def main():
    print("Loading data…")
    day_scores = load_day_entries()
    day_notes = load_day_notes()
    spike_by_date = load_spike_by_date()
    activities = load_activities()
    episodes = find_crash_episodes(day_scores)
    print(f"  {len(day_scores)} day_entries, {len(day_notes)} notes, {len(spike_by_date)} spike-days, {len(activities)} activities, {len(episodes)} episodes")

    # Crash days + lead-up days (for null-window exclusion)
    crash_days: set[date] = set()
    for ep in episodes:
        d = ep["start"]
        while d <= ep["end"]:
            if d in day_scores and day_scores[d] <= LOW_THRESHOLD:
                crash_days.add(d)
            d += timedelta(days=1)
    all_leadup_days: set[date] = set()
    for ep in episodes:
        for i in range(1, LEADUP_DAYS + 1):
            all_leadup_days.add(ep["start"] - timedelta(days=i))

    # Reproduce null sample
    print("Reproducing the H02b null sample (seed 20260605)…")
    null = build_null_sample(spike_by_date, all_leadup_days, NULL_SAMPLE_SIZE)
    print(f"  null sample size: {len(null)}")

    # Filter to false positives
    fp = [w for w in null if w["delta"] >= CRIT_A_DELTA_MIN]
    print(f"  null windows firing +10-min spike (false positives): {len(fp)}  ({100*len(fp)/len(null):.0f}%)")

    # Index activities by date for quick lookup
    activities_by_date: dict[date, list[dict]] = {}
    for a in activities:
        activities_by_date.setdefault(a["date"], []).append(a)

    # For each false positive, categorize
    enriched = []
    for w in fp:
        ref = w["ref"]
        peak = w["peak_day"]
        # Score on each of the 4 days
        scores = []
        for d in [*w["leadup_dates"], ref]:
            scores.append((d, day_scores.get(d)))
        # Near-miss: any of these 4 days has score == NEAR_MISS_SCORE
        near_miss = any(s == NEAR_MISS_SCORE for _, s in scores if s is not None)
        # Activity on peak day?
        peak_acts = activities_by_date.get(peak, [])
        long_peak_acts = [a for a in peak_acts if a["duration_min"] >= ACTIVITY_LONG_MIN]
        # Distance to nearest crash
        crash_starts = [ep["start"] for ep in episodes]
        nearest_crash = min(crash_starts, key=lambda c: abs((c - ref).days))
        days_to_crash = (nearest_crash - ref).days
        close_to_crash = abs(days_to_crash) <= CLOSE_TO_CRASH_DAYS and not (-LEADUP_DAYS <= days_to_crash <= 0)
        # Note on peak day
        peak_note = day_notes.get(peak, "")

        # Categorize (multi-label allowed)
        tags = []
        if near_miss: tags.append("near_miss")
        if long_peak_acts: tags.append("activity_induced")
        if close_to_crash: tags.append("close_to_crash")
        if not tags: tags.append("unexplained")

        enriched.append({
            "ref": ref,
            "peak_day": peak,
            "peak_spike_minutes": w["leadup_max"],
            "baseline_mean": w["baseline_mean"],
            "delta": w["delta"],
            "leadup_dates": w["leadup_dates"],
            "scores": scores,
            "near_miss": near_miss,
            "long_peak_acts": long_peak_acts,
            "days_to_crash": days_to_crash,
            "close_to_crash": close_to_crash,
            "peak_note": peak_note,
            "tags": tags,
        })

    # Tally
    import collections
    tag_counts = collections.Counter()
    multi_label_counts = collections.Counter()
    for e in enriched:
        for t in e["tags"]:
            tag_counts[t] += 1
        multi_label_counts[tuple(sorted(e["tags"]))] += 1

    print("\n=== false-positive categorization ===")
    print(f"  total false positives: {len(enriched)}")
    print(f"  by tag (multi-label):")
    for t, n in tag_counts.most_common():
        print(f"    {t}: {n} ({100*n/len(enriched):.0f}%)")
    print(f"  by combination:")
    for combo, n in multi_label_counts.most_common():
        print(f"    {'+'.join(combo)}: {n}")

    # Write markdown
    md = ["# H02b — Specificity check: what are the spike-firing non-crash windows?", ""]
    md.append("Reproduction of the H02b null sample (seed 20260605), filtered to the ~41% of windows")
    md.append("that fired the +10-min spike criterion. For each: 3 lead-up day scores + reference day score,")
    md.append("peak-spike day, workout overlap, distance to nearest crash, and the note on the peak day.")
    md.append("")
    md.append("## Counts")
    md.append("")
    md.append(f"- null sample size: **{len(null)}**")
    md.append(f"- false-positive windows (delta ≥ +10 min): **{len(enriched)}** ({100*len(enriched)/len(null):.0f}%)")
    md.append("")
    md.append("**Categorization (multi-label, each window can carry several tags):**")
    md.append("")
    md.append("| tag | count | % of false positives |")
    md.append("|-----|------:|---------------------:|")
    for t, n in tag_counts.most_common():
        md.append(f"| `{t}` | {n} | {100*n/len(enriched):.0f}% |")
    md.append("")
    md.append("Tag meanings:")
    md.append(f"- `near_miss`: any day in window or reference had score = {NEAR_MISS_SCORE} (a sub-threshold dip crash_v1 missed)")
    md.append(f"- `activity_induced`: a recorded workout ≥ {ACTIVITY_LONG_MIN} min on the peak-spike day")
    md.append(f"- `close_to_crash`: within ±{CLOSE_TO_CRASH_DAYS} days of an actual crash (but outside our 3-day lead-up window)")
    md.append("- `unexplained`: none of the above")
    md.append("")
    md.append("**Combination counts:**")
    md.append("")
    md.append("| combination | count |")
    md.append("|-------------|------:|")
    for combo, n in multi_label_counts.most_common():
        md.append(f"| {'+'.join(combo)} | {n} |")
    md.append("")

    # Detailed table
    md.append("## Per-window detail")
    md.append("")
    md.append("Sorted by spike duration (largest first).")
    md.append("")
    md.append("| ref date | scores [d-3,d-2,d-1,ref] | peak day | peak spike | baseline | days to crash | tags | activity on peak day | peak-day note |")
    md.append("|----------|--------------------------|----------|-----------:|---------:|-------------:|------|---------------------|---------------|")
    for e in sorted(enriched, key=lambda x: -x["peak_spike_minutes"]):
        score_str = ",".join(str(s) if s is not None else "?" for _, s in e["scores"])
        peak_str = e["peak_day"].isoformat()
        acts_str = "; ".join(f"{a['type']} {a['duration_min']}min" for a in e["long_peak_acts"]) if e["long_peak_acts"] else "—"
        note_str = (e["peak_note"][:80] + "…") if len(e["peak_note"]) > 80 else (e["peak_note"] or "—")
        note_str = note_str.replace("|", "/").replace("\n", " ")
        tags_str = ", ".join(e["tags"])
        md.append(
            f"| {e['ref'].isoformat()} | {score_str} | {peak_str} | {e['peak_spike_minutes']:.0f} | "
            f"{e['baseline_mean']:.1f} | {e['days_to_crash']:+d} | {tags_str} | {acts_str} | {note_str} |"
        )
    md.append("")

    # Interpretation prompt
    md.append("## How to read this")
    md.append("")
    md.append("**If most false positives are `near_miss`**: crash_v1 is too strict. The spike metric is")
    md.append("genuinely detecting physiological strain that didn't manifest as a 2-day score-3 episode.")
    md.append("Argues for a `crash_v2` with a softer threshold OR a `dip_v1` for sub-threshold events.")
    md.append("")
    md.append("**If most are `activity_induced`**: the spike extractor needs to filter on activity-overlap")
    md.append("days. Garmin generally suppresses stress samples during recorded activities (`stressTooActiveCount`),")
    md.append("but a long unrecorded effort could leak through.")
    md.append("")
    md.append("**If most are `close_to_crash`**: the 3-day lead-up window is too narrow. The signal is")
    md.append("real but lives in a wider window than we tested. Argues for an H02d with 7-day lead-up.")
    md.append("")
    md.append("**If most are `unexplained`**: the spike is a necessary-but-not-sufficient signal. Days")
    md.append("with the spike pattern usually pass without becoming a crash; only some combination of")
    md.append("the spike plus other factors precipitates one. Surfacing the spike standalone as a")
    md.append("predictor card would be misleading. Confirms the 'NOT to build' decision in the stocktake.")
    md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"\nwrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
