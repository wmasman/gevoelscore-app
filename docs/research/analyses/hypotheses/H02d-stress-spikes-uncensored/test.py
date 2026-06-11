"""H02d Stage 2 — evaluate pre-registered criteria on
daily_max_spike_v2.csv (produced by extract_daily_max_spike_v2.py).

Runs 4 evaluations: {imputed primary, bridge sensitivity} x {4-day
primary window, 5-day secondary window}. Each evaluation runs train +
validate independently against the same falsification bar as H02b
(60% / +15 pp / +5 min). The PRIMARY VERDICT is imputed × 4-day. All
others are reported alongside as diagnostic.
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

# H02d evaluates at two windows in parallel (primary 4d, secondary 5d)
WINDOWS = [
    {"label": "4d", "leadup_days": 4, "min_leadup_valid": 3},
    {"label": "5d", "leadup_days": 5, "min_leadup_valid": 4},
]
PRIMARY_WINDOW_LABEL = "4d"
BASELINE_WINDOW_DAYS = 90
MIN_BASELINE_VALID = 30
TRIMMED_PCT = 0.10

NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

CRIT_A_FRACTION = 0.60
CRIT_A_DELTA_MIN = 10
CRIT_B_DISCRIMINATION_PP = 15
CRIT_C_MEDIAN_MIN = 5
CRIT_C_LOWER_QUARTILE_MIN = 0
MIN_EPISODES_PER_WINDOW = 10

# Both arms processed in parallel
ARMS = [
    {"label": "imputed", "column": "max_spike_minutes_imputed"},
    {"label": "bridge", "column": "max_spike_minutes_bridge"},
]
PRIMARY_ARM_LABEL = "imputed"

HERE = Path(__file__).resolve().parent
DAY_ENTRIES_CSV = HERE / "day_entries.csv"
SPIKE_CSV = HERE / "daily_max_spike_v2.csv"
OUT_DATA = HERE / "result-data.json"


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


def load_spike_by_date(column: str) -> dict[date, float]:
    """date -> max_spike_minutes from given column, only for valid days."""
    if not SPIKE_CSV.exists():
        sys.exit(
            f"\nERROR: {SPIKE_CSV} not found.\n"
            f"Run extract_daily_max_spike_v2.py first.\n"
        )
    out: dict[date, float] = {}
    with SPIKE_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1":
                continue
            d = date.fromisoformat(r["date"])
            out[d] = float(r[column])
    return out


def load_v2_csv_full() -> list[dict]:
    rows = []
    with SPIKE_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    return rows


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


def compute_window(
    ref: date,
    spike_by_date: dict[date, float],
    leadup_days: int,
    min_leadup_valid: int,
) -> dict:
    leadup = [ref - timedelta(days=i) for i in range(1, leadup_days + 1)]
    baseline_start = ref - timedelta(days=BASELINE_WINDOW_DAYS + leadup_days)
    baseline_end = ref - timedelta(days=leadup_days + 1)
    baseline_days = []
    d = baseline_start
    while d <= baseline_end:
        baseline_days.append(d)
        d += timedelta(days=1)
    leadup_vals = [spike_by_date[d] for d in leadup if d in spike_by_date]
    baseline_vals = [spike_by_date[d] for d in baseline_days if d in spike_by_date]
    leadup_valid = len(leadup_vals) >= min_leadup_valid
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


def build_null_sample(spike_by_date, crash_lead_up_days, n, leadup_days, min_leadup_valid):
    rng = random.Random(RANDOM_SEED)
    all_dates = sorted(d for d in spike_by_date if ANALYSIS_START <= d <= VALIDATE_END)
    deltas: list[float] = []
    attempts = 0
    max_attempts = n * 50
    while len(deltas) < n and attempts < max_attempts:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, leadup_days + 1)}
        if leadup & crash_lead_up_days:
            continue
        prof = compute_window(ref, spike_by_date, leadup_days, min_leadup_valid)
        if prof["delta"] is None:
            continue
        deltas.append(prof["delta"])
    return deltas


def evaluate(crash_deltas, null_deltas, label):
    if len(crash_deltas) < MIN_EPISODES_PER_WINDOW:
        return {
            "split": label,
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
        "split": label,
        "crash_n": len(crash_deltas),
        "null_n": len(null_deltas),
        "crash_pct_at_threshold": round(crash_at_thr, 3),
        "null_pct_at_threshold": round(null_at_thr, 3),
        "discrimination_pp": round((crash_at_thr - null_at_thr) * 100, 1),
        "median_delta_minutes": round(median_delta, 1),
        "lower_quartile_delta_minutes": round(lower_q, 1),
        "criterion_a_pass": crit_a,
        "criterion_b_pass": crit_b,
        "criterion_c_pass": crit_c,
        "verdict": "supported" if (crit_a and crit_b and crit_c) else "refuted",
    }


def run_one_arm_window(arm: dict, window: dict, day_scores, episodes):
    spike_by_date = load_spike_by_date(arm["column"])
    leadup_days = window["leadup_days"]
    min_leadup_valid = window["min_leadup_valid"]

    all_leadup_days: set[date] = set()
    for ep in episodes:
        for i in range(1, leadup_days + 1):
            all_leadup_days.add(ep["start"] - timedelta(days=i))

    per_episode = []
    excluded_missing = 0
    excluded_overlap = 0
    for ep in episodes:
        prof = compute_window(ep["start"], spike_by_date, leadup_days, min_leadup_valid)
        leadup = {ep["start"] - timedelta(days=i) for i in range(1, leadup_days + 1)}
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

    null_deltas = build_null_sample(
        spike_by_date, all_leadup_days, NULL_SAMPLE_SIZE, leadup_days, min_leadup_valid
    )

    def clean(in_train: bool):
        return [
            r["delta_spike_minutes"]
            for r in per_episode
            if (r["in_train"] if in_train else r["in_validate"])
            and r["leadup_valid"]
            and r["baseline_valid"]
            and not r["overlap_with_other_episode"]
        ]

    train_clean = clean(True)
    validate_clean = clean(False)

    train_eval = evaluate(train_clean, null_deltas, "train")
    validate_eval = evaluate(validate_clean, null_deltas, "validate")

    if train_eval["verdict"] == "supported" and validate_eval["verdict"] == "supported":
        verdict = "supported"
    elif "inconclusive" in (train_eval["verdict"], validate_eval["verdict"]):
        verdict = "inconclusive"
    else:
        verdict = "refuted"

    return {
        "arm": arm["label"],
        "window": window["label"],
        "leadup_days": leadup_days,
        "train_clean_n": len(train_clean),
        "validate_clean_n": len(validate_clean),
        "excluded_missing": excluded_missing,
        "excluded_overlap": excluded_overlap,
        "train": train_eval,
        "validate": validate_eval,
        "overall_verdict": verdict,
        "null_n": len(null_deltas),
        "per_episode": per_episode,
    }


def main() -> int:
    print("Loading day_entries...")
    day_scores = load_day_entries()
    print(f"  {len(day_scores)} day_entries with score")

    print("Detecting crash_v1 episodes...")
    episodes = find_crash_episodes(day_scores)
    print(f"  {len(episodes)} crash_v1 episodes")

    # Diagnostic: how much did sentinel imputation change things?
    full = load_v2_csv_full()
    valid_full = [r for r in full if r["valid"] == "1"]
    n_changed = sum(
        1 for r in valid_full
        if float(r["max_spike_minutes_imputed"]) != float(r["max_spike_minutes_bridge"])
    )
    n_too_active_days = sum(1 for r in valid_full if int(r["too_active_count"]) > 0)
    total_too_active_samples = sum(int(r["too_active_count"]) for r in valid_full)
    print(f"\nSentinel diagnostic across {len(valid_full)} valid days:")
    print(f"  days where imputed != bridge max-spike: {n_changed}")
    print(f"  days with >=1 too_active sample: {n_too_active_days}")
    print(f"  total too_active samples across valid days: {total_too_active_samples}")

    # Run all four arm x window combinations
    results = {}
    for arm in ARMS:
        for window in WINDOWS:
            key = f"{arm['label']}__{window['label']}"
            print(f"\n=== Running {key} ===")
            results[key] = run_one_arm_window(arm, window, day_scores, episodes)
            r = results[key]
            print(f"  train  ({r['train_clean_n']}): {r['train'].get('verdict')} "
                  f"(crash {r['train'].get('crash_pct_at_threshold')}, "
                  f"null {r['train'].get('null_pct_at_threshold')}, "
                  f"disc {r['train'].get('discrimination_pp')} pp, "
                  f"median {r['train'].get('median_delta_minutes')})")
            print(f"  valid ({r['validate_clean_n']}): {r['validate'].get('verdict')} "
                  f"(crash {r['validate'].get('crash_pct_at_threshold')}, "
                  f"null {r['validate'].get('null_pct_at_threshold')}, "
                  f"disc {r['validate'].get('discrimination_pp')} pp, "
                  f"median {r['validate'].get('median_delta_minutes')})")
            print(f"  overall: {r['overall_verdict']}")

    primary_key = f"{PRIMARY_ARM_LABEL}__{PRIMARY_WINDOW_LABEL}"
    primary_verdict = results[primary_key]["overall_verdict"]

    print(f"\n=== PRIMARY VERDICT (H02d) ===")
    print(f"  primary key: {primary_key}")
    print(f"  verdict: {primary_verdict}")

    OUT_DATA.write_text(
        json.dumps(
            {
                "params": {
                    "windows": WINDOWS,
                    "primary_window_label": PRIMARY_WINDOW_LABEL,
                    "arms": [{"label": a["label"], "column": a["column"]} for a in ARMS],
                    "primary_arm_label": PRIMARY_ARM_LABEL,
                    "baseline_window_days": BASELINE_WINDOW_DAYS,
                    "trimmed_pct": TRIMMED_PCT,
                    "null_sample_size": NULL_SAMPLE_SIZE,
                    "crit_a_fraction": CRIT_A_FRACTION,
                    "crit_a_delta_min": CRIT_A_DELTA_MIN,
                    "crit_b_discrimination_pp": CRIT_B_DISCRIMINATION_PP,
                    "crit_c_median_min": CRIT_C_MEDIAN_MIN,
                    "crit_c_lower_quartile_min": CRIT_C_LOWER_QUARTILE_MIN,
                    "analysis_start": ANALYSIS_START.isoformat(),
                    "train_end": TRAIN_END.isoformat(),
                    "validate_end": VALIDATE_END.isoformat(),
                },
                "counts": {
                    "day_entries": len(day_scores),
                    "valid_stress_days": len(valid_full),
                    "episodes": len(episodes),
                    "days_imputed_neq_bridge": n_changed,
                    "days_with_too_active_samples": n_too_active_days,
                    "total_too_active_samples": total_too_active_samples,
                },
                "results": results,
                "primary_key": primary_key,
                "primary_verdict": primary_verdict,
            },
            indent=2, default=str,
        ),
        encoding="utf-8",
    )
    print(f"\nwrote {OUT_DATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
