"""HA08c - Multi-day sleep stress mean slope (z-score).

Trailing-5-day OLS slope of nightly stress_mean, z-scored against
lagged personal baseline of slopes. One-sided ELEVATED primary
(sustained upward sleep-stress trend = sustained HRV proxy decline
= Wiggers' canonical "creep" direction).

Usage:
  python test.py --dry-run
  python test.py
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)

LAGGED_WINDOW_START_DAYS = 30
LAGGED_WINDOW_END_DAYS = 90
MIN_LAGGED_DAYS = 40
TRIMMED_PCT = 0.10
MIN_BASELINE_STD = 0.5  # stress-points/day; locked in hypothesis.md §4.3

LEADUP_PRIMARY = 4
LEADUP_SECONDARY = 5
MIN_LEADUP_VALID_PRIMARY = 3
MIN_LEADUP_VALID_SECONDARY = 4

SLOPE_WINDOW = 5  # days
MIN_SLOPE_POINTS = 4

N_STD_PRIMARY = 1.5
N_STD_SECONDARY = 2.0
N_STD_SENSITIVITY = 2.5

NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABELS_CSV = ROOT / "crash_v2-definition" / "labels_crash_v2.csv"
NIGHTLY_CSV = (
    Path(__file__).resolve().parents[2]
    / "scripts" / "sleep_stress_extract" / "sleep_stress_nightly.csv"
)
OUT_JSON = HERE / "result-data.json"


def load_stress_means() -> dict[date, float]:
    means: dict[date, float] = {}
    with NIGHTLY_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1" or not r["stress_mean"]:
                continue
            means[date.fromisoformat(r["date"])] = float(r["stress_mean"])
    return means


def load_crashes() -> list[date]:
    crashes_by_id: dict[str, list[date]] = {}
    with LABELS_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["label"] != "crash":
                continue
            d = date.fromisoformat(r["date"])
            crashes_by_id.setdefault(r["episode_id"], []).append(d)
    return sorted(min(ds) for ds in crashes_by_id.values())


def trimmed_list(values: list[float], trim_pct: float) -> list[float]:
    if not values:
        return []
    vs = sorted(values)
    n = len(vs)
    trim = int(n * trim_pct)
    if n - 2 * trim < 1:
        return vs
    return vs[trim : n - trim]


def compute_slope_5d(d: date, means: dict[date, float]) -> float | None:
    """OLS slope of stress_mean vs day-index over [d-4, d]."""
    xs, ys = [], []
    for i in range(SLOPE_WINDOW):  # 0..4 -> days d-4..d
        wd = d - timedelta(days=SLOPE_WINDOW - 1 - i)
        if wd in means:
            xs.append(float(i))
            ys.append(means[wd])
    if len(xs) < MIN_SLOPE_POINTS:
        return None
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
    den = sum((xs[i] - mean_x) ** 2 for i in range(n))
    if den == 0:
        return None
    return num / den


def compute_baseline_slope_mu_sigma(
    d: date, means: dict[date, float]
) -> tuple[float | None, float | None]:
    prior_slopes: list[float] = []
    for i in range(LAGGED_WINDOW_START_DAYS + 1, LAGGED_WINDOW_END_DAYS + 1):
        wd = d - timedelta(days=i)
        s = compute_slope_5d(wd, means)
        if s is not None:
            prior_slopes.append(s)
    if len(prior_slopes) < MIN_LAGGED_DAYS:
        return None, None
    trimmed = trimmed_list(prior_slopes, TRIMMED_PCT)
    if len(trimmed) < 2:
        return None, None
    mu = statistics.mean(trimmed)
    sigma = statistics.stdev(trimmed)
    if sigma < MIN_BASELINE_STD:
        return None, None
    return mu, sigma


def per_day_z(d: date, means: dict[date, float]) -> tuple[float | None, float | None]:
    slope = compute_slope_5d(d, means)
    if slope is None:
        return None, None
    mu, sigma = compute_baseline_slope_mu_sigma(d, means)
    if mu is None or sigma is None:
        return None, None
    signed = (slope - mu) / sigma
    return signed, abs(signed)


def episode_profile(
    ref: date, means: dict[date, float], leadup_days: int, min_valid: int
) -> dict | None:
    signed_zs: list[tuple[date, float]] = []
    for i in range(1, leadup_days + 1):
        wd = ref - timedelta(days=i)
        signed, _ = per_day_z(wd, means)
        if signed is None:
            continue
        signed_zs.append((wd, signed))
    if len(signed_zs) < min_valid:
        return None
    abs_pairs = [(d, abs(s)) for d, s in signed_zs]
    max_abs_pair = max(abs_pairs, key=lambda x: x[1])
    max_signed_at_max_abs = dict(signed_zs)[max_abs_pair[0]]
    max_signed_z = max(s for _, s in signed_zs)
    min_signed_z = min(s for _, s in signed_zs)
    return {
        "leadup_n": len(signed_zs),
        "max_abs_z": max_abs_pair[1],
        "max_signed_at_max_abs": max_signed_at_max_abs,
        "max_signed_z": max_signed_z,
        "min_signed_z": min_signed_z,
    }


def build_null_sample(
    means: dict[date, float], crash_starts: list[date],
    leadup_days: int, min_valid: int,
) -> list[dict]:
    rng = random.Random(RANDOM_SEED)
    occupied: set[date] = set()
    for ref in crash_starts:
        for i in range(1, leadup_days + 1):
            occupied.add(ref - timedelta(days=i))
    all_dates = sorted(
        d for d in means if ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END
    )
    out: list[dict] = []
    attempts = 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 20000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, leadup_days + 1)}
        if leadup & occupied:
            continue
        prof = episode_profile(ref, means, leadup_days, min_valid)
        if prof is None:
            continue
        out.append({"ref": ref, **prof})
    return out


def evaluate_arm(
    events: list[dict], null: list[dict], N_std: float, mode: str
) -> dict:
    if len(events) < 10:
        return {"verdict": "inconclusive", "n_clean": len(events)}

    def trigger(e: dict) -> bool:
        if mode == "bidirectional":
            return e["max_abs_z"] >= N_std
        if mode == "one_sided_elevated":
            return e["max_signed_z"] >= N_std
        return e["min_signed_z"] <= -N_std

    frac_event = sum(1 for e in events if trigger(e)) / len(events)
    frac_null = sum(1 for e in null if trigger(e)) / len(null)
    disc_pp = (frac_event - frac_null) * 100

    if mode == "bidirectional":
        magnitudes = sorted(e["max_abs_z"] for e in events)
    elif mode == "one_sided_elevated":
        magnitudes = sorted(e["max_signed_z"] for e in events)
    else:
        magnitudes = sorted(abs(e["min_signed_z"]) for e in events)
    median_magnitude = statistics.median(magnitudes)

    a = frac_event >= CRIT_A_FRAC
    b = disc_pp >= CRIT_B_DISC_PP
    c = median_magnitude >= N_std / 2

    triggered = [e for e in events if trigger(e)]
    n_elev = sum(1 for e in triggered if e["max_signed_at_max_abs"] >= N_std)
    n_lowered = sum(1 for e in triggered if e["max_signed_at_max_abs"] <= -N_std)

    return {
        "verdict": "supported" if (a and b and c) else "refuted",
        "n_clean": len(events),
        "n_null": len(null),
        "frac_event": frac_event,
        "frac_null": frac_null,
        "discrimination_pp": disc_pp,
        "median_magnitude": median_magnitude,
        "crit_a_pass": a, "crit_b_pass": b, "crit_c_pass": c,
        "n_triggering": len(triggered),
        "n_elevated_at_max_abs": n_elev,
        "n_lowered_at_max_abs": n_lowered,
    }


def dry_run(means: dict[date, float], crashes: list[date], k: int = 3) -> None:
    print(f"\n=== DRY-RUN: first {k} crash episodes per era ===\n")
    train_crashes = [c for c in crashes if c <= TRAIN_END]
    validate_crashes = [c for c in crashes if c > TRAIN_END]
    sample = train_crashes[:k] + validate_crashes[:k]
    n_low_var = 0
    n_no_slope = 0
    n_total = 0
    for ref in sample:
        era = "TRAIN" if ref <= TRAIN_END else "VALIDATE"
        print(f"--- {era} crash starting {ref} ---")
        print(f"  {'date':12} {'slope':>7} {'mu':>7} {'sigma':>7} {'z':>7}")
        for i in range(1, LEADUP_SECONDARY + 1):
            wd = ref - timedelta(days=i)
            n_total += 1
            slope = compute_slope_5d(wd, means)
            mu, sigma = compute_baseline_slope_mu_sigma(wd, means)
            if slope is None:
                n_no_slope += 1
                print(f"  {wd.isoformat():12} {'NO SLOPE':>7} {'':>7} {'':>7} {'':>7}")
                continue
            if mu is None or sigma is None:
                n_low_var += 1
                print(f"  {wd.isoformat():12} {slope:>+7.3f} {'LOW':>7} {'VAR':>7} {'':>7}")
                continue
            signed = (slope - mu) / sigma
            print(f"  {wd.isoformat():12} {slope:>+7.3f} {mu:>+7.3f} {sigma:>7.3f} {signed:>+7.3f}")
        prof_4d = episode_profile(ref, means, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
        if prof_4d:
            print(f"  primary 4d: max|z|={prof_4d['max_abs_z']:.3f} "
                  f"(at-max-signed={prof_4d['max_signed_at_max_abs']:+.3f}); "
                  f"n_valid={prof_4d['leadup_n']}/{LEADUP_PRIMARY}")
        print()
    print(f"=== DRY-RUN END (low-var: {n_low_var}; no-slope: {n_no_slope}; total: {n_total}) ===")


def collect_events(
    refs: list[date], means: dict[date, float], leadup_days: int, min_valid: int
) -> list[dict]:
    out: list[dict] = []
    for ref in refs:
        prof = episode_profile(ref, means, leadup_days, min_valid)
        if prof is None:
            continue
        out.append({"ref": ref, **prof})
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print("Loading sleep stress means...")
    means = load_stress_means()
    print(f"  {len(means)} valid nights")
    crashes = load_crashes()
    print(f"  {len(crashes)} crash episodes")

    if args.dry_run:
        dry_run(means, crashes)
        return 0

    train_crashes = [c for c in crashes if c <= TRAIN_END]
    validate_crashes = [c for c in crashes if c > TRAIN_END]

    print("\nCollecting per-episode profiles...")
    train_4d = collect_events(train_crashes, means, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    validate_4d = collect_events(validate_crashes, means, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    train_5d = collect_events(train_crashes, means, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    validate_5d = collect_events(validate_crashes, means, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    print(f"  4d: train {len(train_4d)}/{len(train_crashes)}, "
          f"validate {len(validate_4d)}/{len(validate_crashes)}")

    null_4d = build_null_sample(means, crashes, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    null_5d = build_null_sample(means, crashes, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)

    results: dict[str, dict] = {}
    print("\n=== Evaluating all combinations ===")
    print(f"  {'arm':55} {'verdict':>11} {'frac':>9} {'null':>9} {'disc':>8} {'med':>7}")
    for window_label, train_evt, validate_evt, null_sample in [
        ("4d_primary", train_4d, validate_4d, null_4d),
        ("5d_secondary", train_5d, validate_5d, null_5d),
    ]:
        for N_std in [N_STD_PRIMARY, N_STD_SECONDARY, N_STD_SENSITIVITY]:
            for mode in ["one_sided_elevated", "bidirectional", "one_sided_lowered"]:
                for era_label, events in [("train", train_evt), ("validate", validate_evt)]:
                    key = f"{window_label}_Nstd{N_std}_{mode}_{era_label}"
                    r = evaluate_arm(events, null_sample, N_std, mode)
                    results[key] = r
                    if "frac_event" in r:
                        print(f"  {key:55} {r['verdict']:>11} "
                              f"{r['frac_event']*100:>8.1f}% {r['frac_null']*100:>8.1f}% "
                              f"{r['discrimination_pp']:>+7.1f} {r['median_magnitude']:>6.3f}")

    print("\n=== HEADLINE (primary 4d, N_std=1.5, one-sided elevated) ===")
    train_v = results["4d_primary_Nstd1.5_one_sided_elevated_train"]
    val_v = results["4d_primary_Nstd1.5_one_sided_elevated_validate"]
    print(f"  train:    {train_v['verdict']} (freq={train_v.get('frac_event',0)*100:.1f}%, "
          f"disc={train_v.get('discrimination_pp',0):+.1f} pp, median={train_v.get('median_magnitude',0):.3f})")
    print(f"  validate: {val_v['verdict']} (freq={val_v.get('frac_event',0)*100:.1f}%, "
          f"disc={val_v.get('discrimination_pp',0):+.1f} pp, median={val_v.get('median_magnitude',0):.3f})")

    OUT_JSON.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
