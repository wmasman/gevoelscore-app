"""HA11 - Stage 2: precursor test on per-day U-dip event counts.

Loads udip_counts.csv (Stage 1 output), z-scores against lagged
baseline [d-90, d-30], evaluates one-sided ELEVATED primary +
bidirectional sensitivity arm, runs both 4d primary and 5d
secondary windows at N_std = 1.5 / 2.0 / 2.5.

Also reports the secondary descriptive outcome (same-day
correlation between u_dip_count and gevoelscore).

Usage:
  python test.py --dry-run    # first-3-episodes raw values
  python test.py              # full evaluation
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

# Lagged baseline (Theme A) - same as HA06b / HA10
LAGGED_WINDOW_START_DAYS = 30
LAGGED_WINDOW_END_DAYS = 90
LAGGED_WINDOW_LEN = LAGGED_WINDOW_END_DAYS - LAGGED_WINDOW_START_DAYS  # 60
MIN_LAGGED_DAYS = 40
TRIMMED_PCT = 0.10
MIN_BASELINE_STD = 0.5  # events; locked in hypothesis.md §4.5

# Lead-up windows - same as HA06b / HA10
LEADUP_PRIMARY = 4
LEADUP_SECONDARY = 5
MIN_LEADUP_VALID_PRIMARY = 3
MIN_LEADUP_VALID_SECONDARY = 4

# Z-score thresholds - same as HA06b / HA10
N_STD_PRIMARY = 1.5
N_STD_SECONDARY = 2.0
N_STD_SENSITIVITY = 2.5

# Null sample
NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

# Pre-registered SUPPORTED bar - same as HA06b / HA10
CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABELS_CSV = ROOT / "crash_v2-definition" / "labels_crash_v2.csv"
UDIP_CSV = HERE / "udip_counts.csv"
DAY_ENTRIES_CSV = ROOT / "H02b-stress-spikes" / "day_entries.csv"
OUT_JSON = HERE / "result-data.json"


def load_udip_counts() -> tuple[dict[date, int], dict[date, bool]]:
    """Returns (date -> u_dip_count, date -> valid)."""
    if not UDIP_CSV.exists():
        print(f"ERROR: {UDIP_CSV} not found. Run extract_udip_counts.py first.",
              file=sys.stderr)
        sys.exit(1)
    counts: dict[date, int] = {}
    valid: dict[date, bool] = {}
    with UDIP_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            counts[d] = int(r["u_dip_count"])
            valid[d] = r["valid"] == "1"
    return counts, valid


def load_gevoelscore() -> dict[date, int]:
    out: dict[date, int] = {}
    if not DAY_ENTRIES_CSV.exists():
        return out
    with DAY_ENTRIES_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                out[date.fromisoformat(r["date"])] = int(r["score"])
            except (KeyError, ValueError):
                continue
    return out


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


def compute_baseline_mu_sigma(
    d: date,
    counts: dict[date, int],
    valid: dict[date, bool],
) -> tuple[float | None, float | None]:
    """Trimmed-mean + std of u_dip_count over [d-90, d-30] for valid prior days.
    Returns (mu, sigma) or (None, None) if insufficient prior days or
    sigma below floor.
    """
    prior_vals: list[float] = []
    for i in range(LAGGED_WINDOW_START_DAYS + 1, LAGGED_WINDOW_END_DAYS + 1):
        wd = d - timedelta(days=i)
        if wd in counts and valid.get(wd, False):
            prior_vals.append(float(counts[wd]))
    if len(prior_vals) < MIN_LAGGED_DAYS:
        return None, None
    trimmed = trimmed_list(prior_vals, TRIMMED_PCT)
    if len(trimmed) < 2:
        return None, None
    mu = statistics.mean(trimmed)
    sigma = statistics.stdev(trimmed)
    if sigma < MIN_BASELINE_STD:
        return None, None
    return mu, sigma


def per_day_z(
    d: date,
    counts: dict[date, int],
    valid: dict[date, bool],
) -> tuple[float | None, float | None]:
    """Returns (signed_z, abs_z) for date d. None if u_dip_count or
    (mu, sigma) undefined, or day is itself invalid."""
    if d not in counts or not valid.get(d, False):
        return None, None
    mu, sigma = compute_baseline_mu_sigma(d, counts, valid)
    if mu is None or sigma is None:
        return None, None
    signed = (float(counts[d]) - mu) / sigma
    return signed, abs(signed)


def episode_profile(
    ref: date,
    counts: dict[date, int],
    valid: dict[date, bool],
    leadup_days: int,
    min_valid: int,
) -> dict | None:
    signed_zs: list[tuple[date, float]] = []
    for i in range(1, leadup_days + 1):
        wd = ref - timedelta(days=i)
        signed, _ = per_day_z(wd, counts, valid)
        if signed is None:
            continue
        signed_zs.append((wd, signed))
    if len(signed_zs) < min_valid:
        return None
    abs_pairs = [(d, abs(s)) for d, s in signed_zs]
    max_abs_pair = max(abs_pairs, key=lambda x: x[1])
    max_signed = dict(signed_zs)[max_abs_pair[0]]
    # max signed z (for one-sided elevated direction)
    max_signed_z = max(s for _, s in signed_zs)
    min_signed_z = min(s for _, s in signed_zs)
    return {
        "leadup_n": len(signed_zs),
        "max_abs_z": max_abs_pair[1],
        "max_signed_at_maxabs": max_signed,  # signed value at the max-|z| day
        "max_signed_z": max_signed_z,        # most-positive z in lead-up
        "min_signed_z": min_signed_z,        # most-negative z in lead-up
        "all_signed_zs": [s for _, s in signed_zs],
    }


def build_null_sample(
    counts: dict[date, int],
    valid: dict[date, bool],
    crash_starts: list[date],
    leadup_days: int,
    min_valid: int,
) -> list[dict]:
    rng = random.Random(RANDOM_SEED)
    occupied: set[date] = set()
    for ref in crash_starts:
        for i in range(1, leadup_days + 1):
            occupied.add(ref - timedelta(days=i))
    all_dates = sorted(
        d for d in counts
        if valid.get(d, False)
        and ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END
    )
    out: list[dict] = []
    attempts = 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 10000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, leadup_days + 1)}
        if leadup & occupied:
            continue
        prof = episode_profile(ref, counts, valid, leadup_days, min_valid)
        if prof is None:
            continue
        out.append({"ref": ref, **prof})
    return out


def evaluate_arm(
    events: list[dict],
    null: list[dict],
    N_std: float,
    mode: str,  # 'one_sided_elevated' (primary), 'bidirectional', 'one_sided_lowered'
) -> dict:
    if len(events) < 10:
        return {"verdict": "inconclusive", "n_clean": len(events)}

    def trigger(e: dict) -> bool:
        if mode == "bidirectional":
            return e["max_abs_z"] >= N_std
        if mode == "one_sided_elevated":
            return e["max_signed_z"] >= N_std
        # one_sided_lowered
        return e["min_signed_z"] <= -N_std

    frac_event = sum(1 for e in events if trigger(e)) / len(events)
    frac_null = sum(1 for e in null if trigger(e)) / len(null)
    disc_pp = (frac_event - frac_null) * 100

    # For magnitude criterion, use max_abs_z when bidirectional; for one-sided
    # arms, use the corresponding signed extreme.
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
    # For directionality, count using the max-|z| day's signed value
    n_elev = sum(1 for e in triggered if e["max_signed_at_maxabs"] >= N_std)
    n_lowered = sum(1 for e in triggered if e["max_signed_at_maxabs"] <= -N_std)
    n_other = len(triggered) - n_elev - n_lowered

    return {
        "verdict": "supported" if (a and b and c) else "refuted",
        "n_clean": len(events),
        "n_null": len(null),
        "frac_event": frac_event,
        "frac_null": frac_null,
        "discrimination_pp": disc_pp,
        "median_magnitude": median_magnitude,
        "crit_a_pass": a,
        "crit_b_pass": b,
        "crit_c_pass": c,
        "n_triggering": len(triggered),
        "n_elevated_at_maxabs": n_elev,
        "n_lowered_at_maxabs": n_lowered,
        "n_other_at_maxabs": n_other,
    }


def dry_run(
    counts: dict[date, int],
    valid: dict[date, bool],
    crashes: list[date],
    k: int = 3,
) -> None:
    print(f"\n=== DRY-RUN: first {k} crash episodes per era ===\n")
    train_crashes = [c for c in crashes if c <= TRAIN_END]
    validate_crashes = [c for c in crashes if c > TRAIN_END]
    sample = train_crashes[:k] + validate_crashes[:k]
    n_low_var = 0
    n_invalid_day = 0
    n_total_lookups = 0
    for ref in sample:
        era = "TRAIN" if ref <= TRAIN_END else "VALIDATE"
        print(f"--- {era} crash starting {ref} ---")
        print(f"  {'date':12} {'cnt':>5} {'mu':>6} {'sigma':>6} "
              f"{'z':>7} {'|z|':>6} {'valid':>5}")
        for i in range(1, LEADUP_SECONDARY + 1):
            wd = ref - timedelta(days=i)
            n_total_lookups += 1
            cnt = counts.get(wd)
            v = valid.get(wd, False)
            mu, sigma = (None, None)
            if v:
                mu, sigma = compute_baseline_mu_sigma(wd, counts, valid)
            if cnt is None:
                print(f"  {wd.isoformat():12} {'N/A':>5} {'N/A':>6} {'N/A':>6} "
                      f"{'N/A':>7} {'N/A':>6} {'N/A':>5}")
                continue
            if not v:
                n_invalid_day += 1
                print(f"  {wd.isoformat():12} {cnt:>5} {'-':>6} {'-':>6} "
                      f"{'-':>7} {'-':>6} {'NO':>5}")
                continue
            if mu is None or sigma is None:
                n_low_var += 1
                print(f"  {wd.isoformat():12} {cnt:>5} {'LOW':>6} {'VAR':>6} "
                      f"{'N/A':>7} {'N/A':>6} {'yes':>5}")
                continue
            signed = (cnt - mu) / sigma
            print(f"  {wd.isoformat():12} {cnt:>5} {mu:>6.2f} {sigma:>6.3f} "
                  f"{signed:>+7.3f} {abs(signed):>6.3f} {'yes':>5}")
        prof_4d = episode_profile(ref, counts, valid, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
        prof_5d = episode_profile(ref, counts, valid, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
        if prof_4d:
            print(f"  primary 4d: max|z|={prof_4d['max_abs_z']:.3f} "
                  f"(at-max-signed={prof_4d['max_signed_at_maxabs']:+.3f}, "
                  f"max-signed={prof_4d['max_signed_z']:+.3f}, "
                  f"min-signed={prof_4d['min_signed_z']:+.3f}); "
                  f"n_valid={prof_4d['leadup_n']}/{LEADUP_PRIMARY}")
        else:
            print(f"  primary 4d: insufficient data")
        if prof_5d:
            print(f"  secondary 5d: max|z|={prof_5d['max_abs_z']:.3f} "
                  f"(at-max-signed={prof_5d['max_signed_at_maxabs']:+.3f}, "
                  f"max-signed={prof_5d['max_signed_z']:+.3f}, "
                  f"min-signed={prof_5d['min_signed_z']:+.3f}); "
                  f"n_valid={prof_5d['leadup_n']}/{LEADUP_SECONDARY}")
        else:
            print(f"  secondary 5d: insufficient data")
        print()
    print(f"=== DRY-RUN END (low-var skips: {n_low_var}; "
          f"invalid-day skips: {n_invalid_day}/{n_total_lookups}) ===")


def collect_events(
    refs: list[date],
    counts: dict[date, int],
    valid: dict[date, bool],
    leadup_days: int,
    min_valid: int,
) -> list[dict]:
    out: list[dict] = []
    for ref in refs:
        prof = episode_profile(ref, counts, valid, leadup_days, min_valid)
        if prof is None:
            continue
        out.append({"ref": ref, **prof})
    return out


def secondary_descriptive(
    counts: dict[date, int],
    valid: dict[date, bool],
    scores: dict[date, int],
) -> dict:
    """§4.10 same-day correlation between u_dip_count and gevoelscore."""
    out: dict = {}
    for era_label, end in [("train", TRAIN_END), ("validate", VALIDATE_END)]:
        start = ANALYSIS_START
        days = [d for d in counts
                if valid.get(d, False)
                and d in scores
                and start <= d <= end
                and (era_label != "validate" or d > TRAIN_END)]
        if not days:
            continue
        # Median u_dip_count per gevoelscore
        by_score: dict[int, list[int]] = {}
        for d in days:
            by_score.setdefault(scores[d], []).append(counts[d])
        med_by_score = {s: statistics.median(v) for s, v in sorted(by_score.items())}
        # Spearman correlation (manual implementation: rank both, then Pearson on ranks)
        xs = [counts[d] for d in days]
        ys = [scores[d] for d in days]
        n = len(xs)
        # Rank with average for ties
        def rank(vals: list[float]) -> list[float]:
            sorted_idx = sorted(range(len(vals)), key=lambda i: vals[i])
            ranks = [0.0] * len(vals)
            i = 0
            while i < len(vals):
                j = i
                while j + 1 < len(vals) and vals[sorted_idx[j+1]] == vals[sorted_idx[i]]:
                    j += 1
                avg_rank = (i + j) / 2 + 1
                for k in range(i, j + 1):
                    ranks[sorted_idx[k]] = avg_rank
                i = j + 1
            return ranks
        rx = rank(xs)
        ry = rank(ys)
        mx = sum(rx) / n
        my = sum(ry) / n
        num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
        denx = (sum((rx[i] - mx) ** 2 for i in range(n))) ** 0.5
        deny = (sum((ry[i] - my) ** 2 for i in range(n))) ** 0.5
        rho = num / (denx * deny) if denx and deny else 0.0
        out[era_label] = {
            "n_days": n,
            "median_udip_by_score": {str(k): v for k, v in med_by_score.items()},
            "spearman_rho": rho,
        }
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print("Loading u_dip counts and gevoelscore...")
    counts, valid = load_udip_counts()
    scores = load_gevoelscore()
    n_valid = sum(1 for d in counts if valid[d])
    print(f"  {len(counts)} days in CSV; {n_valid} valid (>=600 samples)")
    print(f"  {len(scores)} days with gevoelscore")
    crashes = load_crashes()
    print(f"  {len(crashes)} crash episodes; "
          f"train: {sum(1 for c in crashes if c <= TRAIN_END)}; "
          f"validate: {sum(1 for c in crashes if c > TRAIN_END)}")

    if args.dry_run:
        dry_run(counts, valid, crashes)
        return 0

    train_crashes = [c for c in crashes if c <= TRAIN_END]
    validate_crashes = [c for c in crashes if c > TRAIN_END]

    print("\nCollecting per-episode profiles...")
    train_4d = collect_events(train_crashes, counts, valid, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    validate_4d = collect_events(validate_crashes, counts, valid, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    train_5d = collect_events(train_crashes, counts, valid, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    validate_5d = collect_events(validate_crashes, counts, valid, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    print(f"  4d primary: train {len(train_4d)}/{len(train_crashes)}, "
          f"validate {len(validate_4d)}/{len(validate_crashes)}")
    print(f"  5d secondary: train {len(train_5d)}/{len(train_crashes)}, "
          f"validate {len(validate_5d)}/{len(validate_crashes)}")

    null_4d = build_null_sample(counts, valid, crashes, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    null_5d = build_null_sample(counts, valid, crashes, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    print(f"  null_4d: {len(null_4d)}; null_5d: {len(null_5d)}")

    results: dict[str, dict] = {}
    print("\n=== Evaluating all combinations ===")
    print(f"  {'arm':55} {'verdict':>11} {'frac_event':>11} {'frac_null':>11} "
          f"{'disc_pp':>9} {'median':>8}")
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
                    verdict = r["verdict"]
                    if "frac_event" in r:
                        print(f"  {key:55} {verdict:>11} "
                              f"{r['frac_event']*100:>10.1f}% "
                              f"{r['frac_null']*100:>10.1f}% "
                              f"{r['discrimination_pp']:>+8.1f} "
                              f"{r['median_magnitude']:>7.3f}")
                    else:
                        print(f"  {key:55} {verdict:>11}")

    print("\n=== HEADLINE (primary 4d, N_std=1.5, one-sided elevated) ===")
    train_v = results["4d_primary_Nstd1.5_one_sided_elevated_train"]
    val_v = results["4d_primary_Nstd1.5_one_sided_elevated_validate"]
    train_verdict = train_v["verdict"]
    val_verdict = val_v["verdict"]
    if train_verdict == "supported" and val_verdict == "supported":
        overall = "SUPPORTED (both eras)"
    elif train_verdict == "supported" or val_verdict == "supported":
        overall = f"PARTIAL (train={train_verdict}, validate={val_verdict})"
    elif "inconclusive" in (train_verdict, val_verdict):
        overall = "INCONCLUSIVE"
    else:
        overall = "REFUTED (both eras)"
    print(f"  train:    {train_verdict} "
          f"(freq={train_v.get('frac_event', 0)*100:.1f}%, "
          f"disc={train_v.get('discrimination_pp', 0):+.1f} pp, "
          f"median_signed_z={train_v.get('median_magnitude', 0):.3f})")
    print(f"  validate: {val_verdict} "
          f"(freq={val_v.get('frac_event', 0)*100:.1f}%, "
          f"disc={val_v.get('discrimination_pp', 0):+.1f} pp, "
          f"median_signed_z={val_v.get('median_magnitude', 0):.3f})")
    print(f"  overall:  {overall}")

    print("\n=== SENSITIVITY ARM (4d, N_std=1.5, bidirectional) ===")
    bi_train = results["4d_primary_Nstd1.5_bidirectional_train"]
    bi_val = results["4d_primary_Nstd1.5_bidirectional_validate"]
    print(f"  train:    {bi_train['verdict']} "
          f"(freq={bi_train.get('frac_event', 0)*100:.1f}%, "
          f"disc={bi_train.get('discrimination_pp', 0):+.1f} pp)")
    print(f"  validate: {bi_val['verdict']} "
          f"(freq={bi_val.get('frac_event', 0)*100:.1f}%, "
          f"disc={bi_val.get('discrimination_pp', 0):+.1f} pp)")

    print("\n=== DIRECTIONALITY SPLIT (over triggering events, primary one-sided elevated) ===")
    for era_label, r in [("train", train_v), ("validate", val_v)]:
        n_t = r.get("n_triggering", 0)
        if n_t == 0:
            print(f"  {era_label}: no triggering events")
            continue
        n_e = r.get("n_elevated_at_maxabs", 0)
        n_l = r.get("n_lowered_at_maxabs", 0)
        print(f"  {era_label}: {n_t} triggering | "
              f"{n_e} elevated-at-maxabs ({100*n_e/n_t:.0f}%) | "
              f"{n_l} lowered-at-maxabs ({100*n_l/n_t:.0f}%)")

    # Secondary descriptive outcome
    print("\n=== SECONDARY DESCRIPTIVE (§4.10): same-day udip count vs gevoelscore ===")
    desc = secondary_descriptive(counts, valid, scores)
    for era_label, d in desc.items():
        print(f"  {era_label}: n_days={d['n_days']}, spearman_rho={d['spearman_rho']:+.3f}")
        print(f"    median u_dip_count by gevoelscore:")
        for k, v in d["median_udip_by_score"].items():
            print(f"      score {k}: {v}")
    results["_secondary_descriptive"] = desc

    OUT_JSON.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
