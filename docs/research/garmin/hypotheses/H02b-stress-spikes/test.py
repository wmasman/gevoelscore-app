"""H02b — Stage 2: evaluate the pre-registered criteria on
daily_max_spike.csv (produced by extract_daily_max_spike.py).

Same structural shape as H02/H03/H04 but with the spike-duration
metric. Lead-up = 3 days, take MAX of daily max-spike values across
those 3 days, compare against baseline trimmed mean of daily
max-spike values over the prior 90 days.
"""
from __future__ import annotations

import csv
import json
import random
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

# Locked params
ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)

LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3

LEADUP_DAYS = 3
BASELINE_WINDOW_DAYS = 90

MIN_LEADUP_VALID = 2  # of 3 (relaxed slightly per hypothesis.md §6)
MIN_BASELINE_VALID = 30
TRIMMED_PCT = 0.10

NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

CRIT_A_FRACTION = 0.60
CRIT_A_DELTA_MIN = 10  # 10 extra minutes of intense spike in lead-up max
CRIT_B_DISCRIMINATION_PP = 15
CRIT_C_MEDIAN_MIN = 5
CRIT_C_LOWER_QUARTILE_MIN = 0
MIN_EPISODES_PER_WINDOW = 10

HERE = Path(__file__).resolve().parent
DAY_ENTRIES_CSV = HERE / "day_entries.csv"
SPIKE_CSV = HERE / "daily_max_spike.csv"
OUT_DATA = HERE / "result-data.json"
OUT_TRAIN_PNG = HERE / "result-train.png"
OUT_VALIDATE_PNG = HERE / "result-validate.png"


def load_day_entries() -> dict[date, int]:
    if not DAY_ENTRIES_CSV.exists():
        sys.exit(f"\nERROR: {DAY_ENTRIES_CSV} not found.\n")
    out: dict[date, int] = {}
    with DAY_ENTRIES_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            s = r["score"]
            if s in ("", "None", None):
                continue
            out[d] = int(s)
    return out


def load_spike_by_date() -> dict[date, float]:
    """date -> max_spike_minutes, only for valid days."""
    if not SPIKE_CSV.exists():
        sys.exit(
            f"\nERROR: {SPIKE_CSV} not found.\n"
            f"Run extract_daily_max_spike.py first.\n"
        )
    out: dict[date, float] = {}
    with SPIKE_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1":
                continue
            d = date.fromisoformat(r["date"])
            out[d] = float(r["max_spike_minutes"])
    return out


def find_crash_episodes(day_scores: dict[date, int]) -> list[dict]:
    sorted_dates = sorted(d for d in day_scores if ANALYSIS_START <= d <= VALIDATE_END)
    runs: list[dict] = []
    cur = None
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
    merged: list[dict] = []
    for r in runs:
        if merged and (r["start"] - merged[-1]["end"]).days <= MERGE_WITHIN_DAYS:
            merged[-1]["end"] = r["end"]
            merged[-1]["days"] += r["days"]
        else:
            merged.append({"start": r["start"], "end": r["end"], "days": r["days"]})
    return merged


def trimmed_mean(values, trim_pct):
    if not values:
        return None
    vs = sorted(values)
    n = len(vs)
    trim = int(n * trim_pct)
    if n - 2 * trim < 1:
        return statistics.mean(vs)
    return statistics.mean(vs[trim : n - trim])


def compute_window(ref: date, spike_by_date: dict[date, float]) -> dict:
    leadup = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    baseline_start = ref - timedelta(days=BASELINE_WINDOW_DAYS + LEADUP_DAYS)
    baseline_end = ref - timedelta(days=LEADUP_DAYS + 1)
    baseline_days = []
    d = baseline_start
    while d <= baseline_end:
        baseline_days.append(d)
        d += timedelta(days=1)
    leadup_vals = [spike_by_date[d] for d in leadup if d in spike_by_date]
    baseline_vals = [spike_by_date[d] for d in baseline_days if d in spike_by_date]
    leadup_valid = len(leadup_vals) >= MIN_LEADUP_VALID
    baseline_valid = len(baseline_vals) >= MIN_BASELINE_VALID
    out = {
        "leadup_n": len(leadup_vals),
        "baseline_n": len(baseline_vals),
        "leadup_valid": leadup_valid,
        "baseline_valid": baseline_valid,
        "leadup_max": max(leadup_vals) if leadup_vals else None,
        "baseline_trimmed_mean": trimmed_mean(baseline_vals, TRIMMED_PCT),
        "delta": None,
    }
    if leadup_valid and baseline_valid:
        out["delta"] = out["leadup_max"] - out["baseline_trimmed_mean"]
    return out


def build_null_sample(spike_by_date, crash_lead_up_days, n):
    rng = random.Random(RANDOM_SEED)
    all_dates = sorted(d for d in spike_by_date if ANALYSIS_START <= d <= VALIDATE_END)
    deltas: list[float] = []
    attempts = 0
    max_attempts = n * 50
    while len(deltas) < n and attempts < max_attempts:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)}
        if leadup & crash_lead_up_days:
            continue
        prof = compute_window(ref, spike_by_date)
        if prof["delta"] is None:
            continue
        deltas.append(prof["delta"])
    return deltas


def evaluate(crash_deltas, null_deltas, label):
    if len(crash_deltas) < MIN_EPISODES_PER_WINDOW:
        return {
            "window": label,
            "verdict": "inconclusive",
            "reason": f"only {len(crash_deltas)} usable crash episodes (< {MIN_EPISODES_PER_WINDOW})",
            "crash_n": len(crash_deltas),
            "null_n": len(null_deltas),
        }
    crash_at_thr = sum(1 for v in crash_deltas if v >= CRIT_A_DELTA_MIN) / len(crash_deltas)
    null_at_thr = (
        sum(1 for v in null_deltas if v >= CRIT_A_DELTA_MIN) / len(null_deltas)
        if null_deltas
        else 0.0
    )
    median_delta = statistics.median(crash_deltas)
    lower_q = sorted(crash_deltas)[len(crash_deltas) // 4]
    crit_a = crash_at_thr >= CRIT_A_FRACTION
    crit_b = (crash_at_thr - null_at_thr) * 100 >= CRIT_B_DISCRIMINATION_PP
    crit_c = median_delta >= CRIT_C_MEDIAN_MIN and lower_q >= CRIT_C_LOWER_QUARTILE_MIN
    return {
        "window": label,
        "crash_n": len(crash_deltas),
        "null_n": len(null_deltas),
        "crash_pct_at_threshold": crash_at_thr,
        "null_pct_at_threshold": null_at_thr,
        "discrimination_pp": (crash_at_thr - null_at_thr) * 100,
        "median_delta_minutes": median_delta,
        "lower_quartile_delta_minutes": lower_q,
        "criterion_a_pass": crit_a,
        "criterion_b_pass": crit_b,
        "criterion_c_pass": crit_c,
        "verdict": "supported" if (crit_a and crit_b and crit_c) else "refuted",
    }


def maybe_plot(crash_deltas, null_deltas, out, title):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(7, 4))
    if not crash_deltas and not null_deltas:
        return
    lo = min([0] + null_deltas + crash_deltas)
    hi = max(null_deltas + crash_deltas + [60])
    bins = list(range(int(lo) - 1, int(hi) + 2, max(2, int((hi - lo) // 30))))
    ax.hist(
        [null_deltas, crash_deltas],
        bins=bins,
        label=[f"null (n={len(null_deltas)})", f"crash lead-ups (n={len(crash_deltas)})"],
        density=True,
        alpha=0.7,
    )
    ax.axvline(CRIT_A_DELTA_MIN, color="black", linestyle="--", alpha=0.5)
    ax.set_xlabel("delta_spike (minutes)  (lead-up MAX minus baseline trimmed mean)")
    ax.set_ylabel("density")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def main() -> int:
    print("Loading day_entries…")
    day_scores = load_day_entries()
    print(f"  {len(day_scores)} day_entries with score")

    print("Detecting crash_v1 episodes…")
    episodes = find_crash_episodes(day_scores)
    print(f"  {len(episodes)} crash_v1 episodes")

    print("Loading daily max-spike data…")
    spike_by_date = load_spike_by_date()
    print(f"  {len(spike_by_date)} valid days with stress coverage")

    all_leadup_days: set[date] = set()
    for ep in episodes:
        for i in range(1, LEADUP_DAYS + 1):
            all_leadup_days.add(ep["start"] - timedelta(days=i))

    print("Computing per-episode delta_spike…")
    per_episode = []
    excluded_missing = 0
    excluded_overlap = 0
    for ep in episodes:
        prof = compute_window(ep["start"], spike_by_date)
        leadup = {ep["start"] - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)}
        other_ep_days: set[date] = set()
        for other in episodes:
            if other["start"] == ep["start"]:
                continue
            d = other["start"]
            while d <= other["end"]:
                other_ep_days.add(d)
                d += timedelta(days=1)
        overlap = bool(leadup & other_ep_days)
        rec = {
            "episode_start": ep["start"].isoformat(),
            "episode_end": ep["end"].isoformat(),
            "in_train": ep["start"] <= TRAIN_END,
            "in_validate": TRAIN_END < ep["start"] <= VALIDATE_END,
            "overlap_with_other_episode": overlap,
            "leadup_valid": prof["leadup_valid"],
            "baseline_valid": prof["baseline_valid"],
            "leadup_max_spike_minutes": prof["leadup_max"],
            "baseline_mean_spike_minutes": prof["baseline_trimmed_mean"],
            "delta_spike_minutes": prof["delta"],
        }
        per_episode.append(rec)
        if not (prof["leadup_valid"] and prof["baseline_valid"]):
            excluded_missing += 1
        elif overlap:
            excluded_overlap += 1

    print(f"  excluded for missing data: {excluded_missing}")
    print(f"  excluded for lead-up overlap: {excluded_overlap}")

    print("Building null sample…")
    null_deltas = build_null_sample(spike_by_date, all_leadup_days, NULL_SAMPLE_SIZE)
    print(f"  {len(null_deltas)} null windows")

    train_clean = [
        r["delta_spike_minutes"]
        for r in per_episode
        if r["in_train"]
        and r["leadup_valid"]
        and r["baseline_valid"]
        and not r["overlap_with_other_episode"]
    ]
    validate_clean = [
        r["delta_spike_minutes"]
        for r in per_episode
        if r["in_validate"]
        and r["leadup_valid"]
        and r["baseline_valid"]
        and not r["overlap_with_other_episode"]
    ]
    print(f"  train clean episodes: {len(train_clean)}")
    print(f"  validate clean episodes: {len(validate_clean)}")

    train_eval = evaluate(train_clean, null_deltas, "train")
    validate_eval = evaluate(validate_clean, null_deltas, "validate")
    overall_verdict = (
        "supported"
        if train_eval["verdict"] == "supported" and validate_eval["verdict"] == "supported"
        else "inconclusive"
        if "inconclusive" in (train_eval["verdict"], validate_eval["verdict"])
        else "refuted"
    )

    print("\n=== VERDICT ===")
    print(f"  train:    {train_eval}")
    print(f"  validate: {validate_eval}")
    print(f"  overall:  {overall_verdict}")

    def summarise(values):
        if not values: return None
        s = sorted(values); n = len(s)
        return {
            "n": n, "median": statistics.median(s), "mean": round(statistics.mean(s), 2),
            "p25": s[n // 4], "p75": s[(3 * n) // 4], "min": s[0], "max": s[-1],
        }

    OUT_DATA.write_text(
        json.dumps(
            {
                "params": {
                    "leadup_days": LEADUP_DAYS, "baseline_window_days": BASELINE_WINDOW_DAYS,
                    "trimmed_pct": TRIMMED_PCT, "null_sample_size": NULL_SAMPLE_SIZE,
                    "crit_a_fraction": CRIT_A_FRACTION, "crit_a_delta_min": CRIT_A_DELTA_MIN,
                    "crit_b_discrimination_pp": CRIT_B_DISCRIMINATION_PP,
                    "crit_c_median_min": CRIT_C_MEDIAN_MIN,
                    "crit_c_lower_quartile_min": CRIT_C_LOWER_QUARTILE_MIN,
                    "analysis_start": ANALYSIS_START.isoformat(),
                    "train_end": TRAIN_END.isoformat(), "validate_end": VALIDATE_END.isoformat(),
                },
                "counts": {
                    "day_entries": len(day_scores), "valid_stress_days": len(spike_by_date),
                    "episodes": len(episodes),
                    "excluded_missing": excluded_missing, "excluded_overlap": excluded_overlap,
                    "train_clean": len(train_clean), "validate_clean": len(validate_clean),
                    "null_n": len(null_deltas),
                },
                "train": train_eval,
                "validate": validate_eval,
                "overall_verdict": overall_verdict,
                "null_summary": summarise(null_deltas),
                "per_episode": per_episode,
            },
            indent=2, default=str,
        ),
        encoding="utf-8",
    )
    print(f"\nwrote {OUT_DATA}")

    maybe_plot(train_clean, null_deltas, OUT_TRAIN_PNG, "H02b — delta max-spike (minutes), TRAIN")
    maybe_plot(validate_clean, null_deltas, OUT_VALIDATE_PNG, "H02b — delta max-spike (minutes), VALIDATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
