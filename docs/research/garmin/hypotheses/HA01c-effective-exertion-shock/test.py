"""HA01c — Effective-exertion shock as crash precursor (per-axis
re-formulation of HA01b).

Pre-registered 2026-06-07 in hypothesis.md per the user-locked
Option A testing playbook section 9 compliance bar. Triggered by
HA01b per-axis diagnostic's both-eras SUPPORTED finding on
effective_exertion. This script tests the locked HA01c primary:

  effective_exertion_rank_lagged >= 0.75 in 4-day lead-up window

The locked HA01c bar (same as HA01b composite):
  (a) crash trigger frequency >= 60%
  (b) discrimination (crash - null) >= +15 pp
  (c) median rank on triggering episodes >= 0.875

Both-eras rule applies per playbook section 4.4.

This script is independent of the HA01b per-axis diagnostic
(re-uses no caches; re-runs the null sample construction with the
same seed `20260605` per playbook section 4.5). The result is a
clean re-test of the per-axis diagnostic finding.

Output:
- result-data.json: locked verdict per era, per-criterion pass/fail,
                    null/crash trigger counts, lead-up profiles
- stdout dry-run gate (3 train + 3 validate episodes) BEFORE full run
"""
from __future__ import annotations

import csv
import json
import random
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
GARMIN_ROOT = HERE.parent.parent
FEATURES_CSV = GARMIN_ROOT / "activity-labels" / "output" / "activity_features_daily.csv"
LABELS_CSV = GARMIN_ROOT / "hypotheses" / "crash_v2-definition" / "labels_crash_v2.csv"
OUT_JSON = HERE / "result-data.json"

# Locked per hypothesis.md section 4 and playbook section 4
ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
LEADUP_DAYS = 4
NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

# Locked 3-criterion bar (matches HA01b composite bar)
CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15
CRIT_C_MEDIAN_RANK_MIN = 0.875

# Locked per-axis primary
AXIS_LABEL = "effective_exertion"
AXIS_COL = "effective_exertion_rank_lagged"
AXIS_RANK_THRESHOLD = 0.75


def load_features() -> dict[date, dict]:
    out = {}
    for r in csv.DictReader(FEATURES_CSV.open(encoding="utf-8")):
        out[date.fromisoformat(r["date"])] = r
    return out


def load_crashes_v1() -> list[date]:
    crashes_by_id: dict[str, list[date]] = {}
    for r in csv.DictReader(LABELS_CSV.open(encoding="utf-8")):
        if r["label"] != "crash":
            continue
        d = date.fromisoformat(r["date"])
        crashes_by_id.setdefault(r["episode_id"], []).append(d)
    return sorted(min(ds) for ds in crashes_by_id.values())


def parse_float(v):
    if v in (None, "", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def axis_window(ref: date, features: dict[date, dict]) -> dict | None:
    """4-day lead-up window stats for effective_exertion_rank_lagged."""
    leadup_days = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    ranks = []
    for d in leadup_days:
        r = features.get(d)
        if not r:
            continue
        rv = parse_float(r.get(AXIS_COL))
        if rv is None:
            continue
        ranks.append(rv)
    if len(ranks) < 3:
        return None
    max_rank = max(ranks)
    return {
        "ranks": ranks,
        "max_rank": max_rank,
        "n_valid": len(ranks),
        "triggers": max_rank >= AXIS_RANK_THRESHOLD,
    }


def build_null_sample(features: dict[date, dict], crash_starts: list[date]) -> list[date]:
    rng = random.Random(RANDOM_SEED)
    occupied: set[date] = set()
    for ref in crash_starts:
        for i in range(1, LEADUP_DAYS + 1):
            occupied.add(ref - timedelta(days=i))
    all_dates = sorted(
        d for d in features
        if ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END
    )
    out = []
    attempts = 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 10000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)}
        if leadup & occupied:
            continue
        out.append(ref)
    return out


def evaluate_era(events: list[date], nulls: list[date],
                 features: dict[date, dict], era_label: str) -> dict:
    event_windows = []
    for d in events:
        w = axis_window(d, features)
        if w is not None:
            event_windows.append({"ref": d.isoformat(), **w})

    null_windows = []
    for d in nulls:
        w = axis_window(d, features)
        if w is not None:
            null_windows.append(w)

    if len(event_windows) < 10:
        return {
            "era": era_label,
            "verdict": "inconclusive",
            "n_clean": len(event_windows),
            "reason": f"n_clean={len(event_windows)} < 10",
        }

    frac_event = sum(1 for w in event_windows if w["triggers"]) / len(event_windows)
    frac_null = sum(1 for w in null_windows if w["triggers"]) / len(null_windows)
    disc_pp = (frac_event - frac_null) * 100

    triggering_max_ranks = [w["max_rank"] for w in event_windows if w["triggers"]]
    if triggering_max_ranks:
        median_rank = statistics.median(triggering_max_ranks)
        sorted_ranks = sorted(triggering_max_ranks)
        lq_rank = sorted_ranks[int(len(sorted_ranks) * 0.25)]
    else:
        median_rank = 0.0
        lq_rank = 0.0

    a = frac_event >= CRIT_A_FRAC
    b = disc_pp >= CRIT_B_DISC_PP
    c = median_rank >= CRIT_C_MEDIAN_RANK_MIN

    return {
        "era": era_label,
        "n_clean": len(event_windows),
        "n_null": len(null_windows),
        "frac_event_triggers": frac_event,
        "frac_null_triggers": frac_null,
        "discrimination_pp": disc_pp,
        "median_rank_on_triggering": median_rank,
        "lower_q_rank_on_triggering": lq_rank,
        "n_triggering_events": len(triggering_max_ranks),
        "crit_a_pass": a,
        "crit_b_pass": b,
        "crit_c_pass": c,
        "verdict": "supported" if (a and b and c) else "refuted",
        "event_profiles": event_windows,
    }


def dry_run_print(train: list[date], validate: list[date],
                  features: dict[date, dict]) -> dict:
    samples = []
    print("\n=== Dry-run gate (per playbook section 2.3) ===")
    for label, events in [("TRAIN", train[:3]), ("VALIDATE", validate[:3])]:
        print(f"\n--- {label} (first 3 crash starts) ---")
        for ref in events:
            print(f"\n  Crash start: {ref.isoformat()} (lead-up [{(ref - timedelta(days=4)).isoformat()} .. {(ref - timedelta(days=1)).isoformat()}])")
            leadup_days = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
            day_ranks = []
            for d in leadup_days:
                r = features.get(d)
                rv = parse_float(r.get(AXIS_COL)) if r else None
                day_ranks.append((d.isoformat(), rv))
            day_str = " ".join(
                f"{ds[5:]}={rv:.2f}" if rv is not None else f"{ds[5:]}=NA"
                for ds, rv in day_ranks
            )
            triggers = any(rv is not None and rv >= AXIS_RANK_THRESHOLD
                           for _, rv in day_ranks)
            marker = "  [trigger]" if triggers else ""
            print(f"    {AXIS_LABEL:22}: {day_str}{marker}")
            samples.append({
                "era": label.lower(),
                "ref": ref.isoformat(),
                "days": day_ranks,
                "triggers": triggers,
            })
    print()
    return {"samples": samples}


def main(dry_run_only: bool = False):
    features = load_features()
    crash_starts = load_crashes_v1()
    train = [d for d in crash_starts if d <= TRAIN_END]
    validate = [d for d in crash_starts if d > TRAIN_END]
    print(f"Loaded {len(features)} feature days | {len(crash_starts)} crash episodes")
    print(f"  train (<=2023-12-31):    {len(train)} crashes")
    print(f"  validate (2024-01-01+):  {len(validate)} crashes")

    nulls = build_null_sample(features, crash_starts)
    print(f"  null sample:             {len(nulls)} non-overlapping 4-day windows")

    dry_run_data = dry_run_print(train, validate, features)

    if dry_run_only:
        print("\n--dry-run-only flag set; not running full HA01c verdict.")
        return

    train_result = evaluate_era(train, nulls, features, "train")
    validate_result = evaluate_era(validate, nulls, features, "validate")

    # Both-eras rule per playbook section 4.4
    if train_result["verdict"] == "supported" and validate_result["verdict"] == "supported":
        overall = "supported"
    else:
        overall = "refuted"

    out = {
        "hypothesis": "HA01c-effective-exertion-shock",
        "pre_registered": "2026-06-07 in hypothesis.md (playbook section 9 compliance)",
        "config": {
            "analysis_start": ANALYSIS_START.isoformat(),
            "train_end": TRAIN_END.isoformat(),
            "validate_end": VALIDATE_END.isoformat(),
            "leadup_days": LEADUP_DAYS,
            "null_sample_size": NULL_SAMPLE_SIZE,
            "random_seed": RANDOM_SEED,
            "axis_label": AXIS_LABEL,
            "axis_col": AXIS_COL,
            "axis_rank_threshold": AXIS_RANK_THRESHOLD,
            "crit_a_frac": CRIT_A_FRAC,
            "crit_b_disc_pp": CRIT_B_DISC_PP,
            "crit_c_median_rank_min": CRIT_C_MEDIAN_RANK_MIN,
        },
        "counts": {
            "n_features": len(features),
            "n_crash_episodes": len(crash_starts),
            "n_train": len(train),
            "n_validate": len(validate),
            "n_null_target": NULL_SAMPLE_SIZE,
            "n_null_actual": len(nulls),
        },
        "train_result": train_result,
        "validate_result": validate_result,
        "overall_verdict": overall,
        "dry_run": dry_run_data,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")

    print("\n=== HA01c locked-threshold verdicts ===")
    for label, r in [("train", train_result), ("validate", validate_result)]:
        if r["verdict"] == "inconclusive":
            print(f"  {label:10} {r['verdict']:12}  ({r['reason']})")
        else:
            print(f"  {label:10} {r['verdict']:12}  "
                  f"disc={r['discrimination_pp']:+6.1f} pp  "
                  f"freq={r['frac_event_triggers']*100:5.1f}%  "
                  f"median_rank={r['median_rank_on_triggering']:.3f}")
            print(f"             crit (a) freq>=60%: {'PASS' if r['crit_a_pass'] else 'fail'} "
                  f"({r['frac_event_triggers']*100:.1f}%)")
            print(f"             crit (b) disc>=+15pp: {'PASS' if r['crit_b_pass'] else 'fail'} "
                  f"({r['discrimination_pp']:+.1f} pp)")
            print(f"             crit (c) median>=0.875: {'PASS' if r['crit_c_pass'] else 'fail'} "
                  f"({r['median_rank_on_triggering']:.3f})")
    print(f"\n=== Both-eras rule (playbook section 4.4) ===")
    print(f"  Overall HA01c verdict: {overall.upper()}")

    if overall == "supported":
        print(f"\nHA01c locked-threshold verdict: SUPPORTED both eras.")
        print(f"Pending: HA01c v2 threshold-monotonicity diagnostic must")
        print(f"also RESCUE before HA01c is treated as load-bearing.")
    else:
        print(f"\nHA01c locked-threshold verdict: REFUTED at the locked bar.")

    print(f"\nWrote {OUT_JSON}")


if __name__ == "__main__":
    dry = "--dry-run-only" in sys.argv
    main(dry_run_only=dry)
