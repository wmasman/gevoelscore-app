"""HA10 - Body Battery overnight recharge coarse proxy (z-score).

Implements the protocol pre-registered in hypothesis.md exactly.

Per-day metric: morning_peak = HIGHEST BB anchor's statsValue when
its timestamp falls in 03:00-10:00 local. Z-scored against lagged
baseline [d-90, d-30]. Bidirectional |z| threshold; one-sided
"lowered only" sensitivity arm (Wiggers direction).

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
from datetime import date, datetime, time, timedelta
from pathlib import Path

ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)

# Lagged baseline (Theme A) - same as HA06b
LAGGED_WINDOW_START_DAYS = 30
LAGGED_WINDOW_END_DAYS = 90
LAGGED_WINDOW_LEN = LAGGED_WINDOW_END_DAYS - LAGGED_WINDOW_START_DAYS  # 60
MIN_LAGGED_DAYS = 40
TRIMMED_PCT = 0.10
MIN_BASELINE_STD = 2.0  # BB points; higher than HA06b's 0.5 bpm

# Lead-up windows - same as HA06b
LEADUP_PRIMARY = 4
LEADUP_SECONDARY = 5
MIN_LEADUP_VALID_PRIMARY = 3   # of 4
MIN_LEADUP_VALID_SECONDARY = 4  # of 5

# Z-score thresholds (same as HA06b / HA07 planned)
N_STD_PRIMARY = 1.5
N_STD_SECONDARY = 2.0
N_STD_SENSITIVITY = 2.5

# Morning-peak time window (local time on the calendar day)
MORNING_START = time(3, 0)
MORNING_END = time(10, 0)

# BB validity range
BB_MIN_VALID = 0
BB_MAX_VALID = 100

# Null sample
NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

# Pre-registered SUPPORTED bar - same as HA06b
CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABELS_CSV = ROOT / "crash_v2-definition" / "labels_crash_v2.csv"
GARMIN_UDS_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Aggregator"
)
OUT_JSON = HERE / "result-data.json"


def parse_anchor_ts(s: str) -> datetime | None:
    """Parse Garmin's anchor timestamp string. Returns None on failure."""
    try:
        return datetime.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def load_morning_peak_by_date() -> tuple[dict[date, int], dict[str, int]]:
    """Load morning_peak (HIGHEST BB anchor when timestamp in 03:00-10:00).

    Returns (mapping date -> bb_value, stats dict for diagnostics).
    """
    out: dict[date, int] = {}
    stats = {
        "files_scanned": 0,
        "records_with_bb": 0,
        "no_highest": 0,
        "no_timestamp": 0,
        "daytime_peak_excluded": 0,
        "out_of_range": 0,
        "valid": 0,
    }
    for p in sorted(GARMIN_UDS_DIR.glob("UDSFile_*.json")):
        stats["files_scanned"] += 1
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            bb = rec.get("bodyBattery")
            if not cd or not bb:
                continue
            stats["records_with_bb"] += 1
            stat_list = bb.get("bodyBatteryStatList", [])
            highest = next(
                (s for s in stat_list if s.get("bodyBatteryStatType") == "HIGHEST"),
                None,
            )
            if not highest:
                stats["no_highest"] += 1
                continue
            ts = parse_anchor_ts(highest.get("statTimestamp", ""))
            if ts is None:
                stats["no_timestamp"] += 1
                continue
            # Time-window filter: 03:00 to 10:00 local on the calendar date
            ts_time = ts.time()
            if not (MORNING_START <= ts_time < MORNING_END):
                stats["daytime_peak_excluded"] += 1
                continue
            val = highest.get("statsValue")
            try:
                val_int = int(val)
            except (TypeError, ValueError):
                continue
            if val_int < BB_MIN_VALID or val_int > BB_MAX_VALID:
                stats["out_of_range"] += 1
                continue
            d = date.fromisoformat(cd)
            # If multiple records (rare), prefer the higher value
            if d in out and val_int <= out[d]:
                continue
            out[d] = val_int
            stats["valid"] += 1
    return out, stats


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
    d: date, peak_by_date: dict[date, int]
) -> tuple[float | None, float | None]:
    """Trimmed-mean + std of morning_peak over [d-90, d-30].
    Returns (mu, sigma) or (None, None) if insufficient prior days or
    sigma below floor.
    """
    prior_vals: list[float] = []
    for i in range(LAGGED_WINDOW_START_DAYS + 1, LAGGED_WINDOW_END_DAYS + 1):
        wd = d - timedelta(days=i)
        if wd in peak_by_date:
            prior_vals.append(float(peak_by_date[wd]))
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
    d: date, peak_by_date: dict[date, int]
) -> tuple[float | None, float | None]:
    """Returns (signed_z, abs_z) for date d. None if peak or (mu, sigma)
    undefined."""
    if d not in peak_by_date:
        return None, None
    mu, sigma = compute_baseline_mu_sigma(d, peak_by_date)
    if mu is None or sigma is None:
        return None, None
    signed = (float(peak_by_date[d]) - mu) / sigma
    return signed, abs(signed)


def episode_profile(
    ref: date,
    peak_by_date: dict[date, int],
    leadup_days: int,
    min_valid: int,
) -> dict | None:
    signed_zs: list[tuple[date, float]] = []
    for i in range(1, leadup_days + 1):
        wd = ref - timedelta(days=i)
        signed, _ = per_day_z(wd, peak_by_date)
        if signed is None:
            continue
        signed_zs.append((wd, signed))
    if len(signed_zs) < min_valid:
        return None
    abs_pairs = [(d, abs(s)) for d, s in signed_zs]
    max_abs_pair = max(abs_pairs, key=lambda x: x[1])
    max_signed = dict(signed_zs)[max_abs_pair[0]]
    return {
        "leadup_n": len(signed_zs),
        "max_abs_z": max_abs_pair[1],
        "max_signed_z": max_signed,
        "all_signed_zs": [s for _, s in signed_zs],
    }


def build_null_sample(
    peak_by_date: dict[date, int],
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
        d for d in peak_by_date if ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END
    )
    out: list[dict] = []
    attempts = 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 10000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, leadup_days + 1)}
        if leadup & occupied:
            continue
        prof = episode_profile(ref, peak_by_date, leadup_days, min_valid)
        if prof is None:
            continue
        out.append({"ref": ref, **prof})
    return out


def evaluate_arm(
    events: list[dict],
    null: list[dict],
    N_std: float,
    bidirectional: bool,
    one_sided_dir: str = "lowered",
) -> dict:
    """Evaluate an arm. bidirectional=True uses |z| >= N_std.
    bidirectional=False with one_sided_dir='lowered' uses z <= -N_std
    (Wiggers direction); 'elevated' uses z >= +N_std.
    """
    if len(events) < 10:
        return {"verdict": "inconclusive", "n_clean": len(events)}

    def trigger(e: dict) -> bool:
        if bidirectional:
            return e["max_abs_z"] >= N_std
        if one_sided_dir == "lowered":
            return e["max_signed_z"] <= -N_std
        return e["max_signed_z"] >= N_std

    frac_event = sum(1 for e in events if trigger(e)) / len(events)
    frac_null = sum(1 for e in null if trigger(e)) / len(null)
    disc_pp = (frac_event - frac_null) * 100
    abs_zs = sorted(e["max_abs_z"] for e in events)
    median_abs = statistics.median(abs_zs)

    a = frac_event >= CRIT_A_FRAC
    b = disc_pp >= CRIT_B_DISC_PP
    c = median_abs >= N_std / 2

    triggered = [e for e in events if trigger(e)]
    n_elev = sum(1 for e in triggered if e["max_signed_z"] >= N_std)
    n_lowered = sum(1 for e in triggered if e["max_signed_z"] <= -N_std)
    n_other = len(triggered) - n_elev - n_lowered

    return {
        "verdict": "supported" if (a and b and c) else "refuted",
        "n_clean": len(events),
        "n_null": len(null),
        "frac_event": frac_event,
        "frac_null": frac_null,
        "discrimination_pp": disc_pp,
        "median_abs_z": median_abs,
        "crit_a_pass": a,
        "crit_b_pass": b,
        "crit_c_pass": c,
        "n_triggering": len(triggered),
        "n_elevated": n_elev,
        "n_lowered": n_lowered,
        "n_other_direction": n_other,
    }


def dry_run(
    peak_by_date: dict[date, int],
    crashes: list[date],
    loader_stats: dict[str, int],
    k: int = 3,
) -> None:
    print(f"\n=== DRY-RUN: first {k} crash episodes per era ===\n")
    print("Loader stats:")
    for key, v in loader_stats.items():
        print(f"  {key}: {v}")
    print()
    train_crashes = [c for c in crashes if c <= TRAIN_END]
    validate_crashes = [c for c in crashes if c > TRAIN_END]
    sample = train_crashes[:k] + validate_crashes[:k]
    n_low_var = 0
    n_total_lookups = 0
    for ref in sample:
        era = "TRAIN" if ref <= TRAIN_END else "VALIDATE"
        print(f"--- {era} crash starting {ref} ---")
        print(f"  {'date':12} {'peak':>5} {'mu':>6} {'sigma':>6} "
              f"{'z':>7} {'|z|':>6}")
        for i in range(1, LEADUP_SECONDARY + 1):
            wd = ref - timedelta(days=i)
            n_total_lookups += 1
            val = peak_by_date.get(wd)
            mu, sigma = compute_baseline_mu_sigma(wd, peak_by_date)
            if val is None:
                print(f"  {wd.isoformat():12} {'N/A':>5} {'N/A':>6} {'N/A':>6} "
                      f"{'N/A':>7} {'N/A':>6}")
                continue
            if mu is None or sigma is None:
                n_low_var += 1
                print(f"  {wd.isoformat():12} {val:>5} {'LOW':>6} {'VAR':>6} "
                      f"{'N/A':>7} {'N/A':>6}")
                continue
            signed = (val - mu) / sigma
            print(f"  {wd.isoformat():12} {val:>5} {mu:>6.2f} {sigma:>6.3f} "
                  f"{signed:>+7.3f} {abs(signed):>6.3f}")
        prof_4d = episode_profile(ref, peak_by_date, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
        prof_5d = episode_profile(ref, peak_by_date, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
        if prof_4d:
            print(f"  primary 4d: max|z|={prof_4d['max_abs_z']:.3f} "
                  f"(signed={prof_4d['max_signed_z']:+.3f}); "
                  f"n_valid={prof_4d['leadup_n']}/{LEADUP_PRIMARY}")
        else:
            print(f"  primary 4d: insufficient data")
        if prof_5d:
            print(f"  secondary 5d: max|z|={prof_5d['max_abs_z']:.3f} "
                  f"(signed={prof_5d['max_signed_z']:+.3f}); "
                  f"n_valid={prof_5d['leadup_n']}/{LEADUP_SECONDARY}")
        else:
            print(f"  secondary 5d: insufficient data")
        print()
    print(f"=== DRY-RUN END (low-variability skips: {n_low_var}/{n_total_lookups}) ===")


def collect_events(
    refs: list[date],
    peak_by_date: dict[date, int],
    leadup_days: int,
    min_valid: int,
) -> list[dict]:
    out: list[dict] = []
    for ref in refs:
        prof = episode_profile(ref, peak_by_date, leadup_days, min_valid)
        if prof is None:
            continue
        out.append({"ref": ref, **prof})
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print("Loading nightly BB morning peak from UDS...")
    peak_by_date, loader_stats = load_morning_peak_by_date()
    print(f"  {len(peak_by_date)} days with valid morning peak")
    print(f"  loader stats: {loader_stats}")
    crashes = load_crashes()
    print(f"  {len(crashes)} crash episodes; "
          f"train: {sum(1 for c in crashes if c <= TRAIN_END)}; "
          f"validate: {sum(1 for c in crashes if c > TRAIN_END)}")

    if args.dry_run:
        dry_run(peak_by_date, crashes, loader_stats)
        return 0

    train_crashes = [c for c in crashes if c <= TRAIN_END]
    validate_crashes = [c for c in crashes if c > TRAIN_END]

    print("\nCollecting per-episode profiles...")
    train_4d = collect_events(train_crashes, peak_by_date, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    validate_4d = collect_events(validate_crashes, peak_by_date, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    train_5d = collect_events(train_crashes, peak_by_date, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    validate_5d = collect_events(validate_crashes, peak_by_date, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    print(f"  4d primary: train {len(train_4d)}/{len(train_crashes)}, "
          f"validate {len(validate_4d)}/{len(validate_crashes)}")
    print(f"  5d secondary: train {len(train_5d)}/{len(train_crashes)}, "
          f"validate {len(validate_5d)}/{len(validate_crashes)}")

    null_4d = build_null_sample(peak_by_date, crashes, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    null_5d = build_null_sample(peak_by_date, crashes, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    print(f"  null_4d: {len(null_4d)}; null_5d: {len(null_5d)}")

    results: dict[str, dict] = {}
    print("\n=== Evaluating all combinations ===")
    print(f"  {'arm':50} {'verdict':>11} {'frac_event':>11} {'frac_null':>11} "
          f"{'disc_pp':>9} {'median':>8}")
    for window_label, train_evt, validate_evt, null_sample in [
        ("4d_primary", train_4d, validate_4d, null_4d),
        ("5d_secondary", train_5d, validate_5d, null_5d),
    ]:
        for N_std in [N_STD_PRIMARY, N_STD_SECONDARY, N_STD_SENSITIVITY]:
            for direction_label, bidirectional, one_sided_dir in [
                ("bidirectional", True, "lowered"),
                ("one_sided_lowered", False, "lowered"),
                ("one_sided_elevated", False, "elevated"),
            ]:
                for era_label, events in [("train", train_evt), ("validate", validate_evt)]:
                    key = f"{window_label}_Nstd{N_std}_{direction_label}_{era_label}"
                    r = evaluate_arm(events, null_sample, N_std, bidirectional, one_sided_dir)
                    results[key] = r
                    verdict = r["verdict"]
                    if "frac_event" in r:
                        print(f"  {key:50} {verdict:>11} "
                              f"{r['frac_event']*100:>10.1f}% "
                              f"{r['frac_null']*100:>10.1f}% "
                              f"{r['discrimination_pp']:>+8.1f} "
                              f"{r['median_abs_z']:>7.3f}")
                    else:
                        print(f"  {key:50} {verdict:>11}")

    print("\n=== HEADLINE (primary 4d, N_std=1.5, bidirectional) ===")
    train_v = results["4d_primary_Nstd1.5_bidirectional_train"]
    val_v = results["4d_primary_Nstd1.5_bidirectional_validate"]
    one_sided_lo_train = results["4d_primary_Nstd1.5_one_sided_lowered_train"]
    one_sided_lo_val = results["4d_primary_Nstd1.5_one_sided_lowered_validate"]
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
          f"median|z|={train_v.get('median_abs_z', 0):.3f})")
    print(f"  validate: {val_verdict} "
          f"(freq={val_v.get('frac_event', 0)*100:.1f}%, "
          f"disc={val_v.get('discrimination_pp', 0):+.1f} pp, "
          f"median|z|={val_v.get('median_abs_z', 0):.3f})")
    print(f"  overall:  {overall}")

    print("\n=== SENSITIVITY ARM (one-sided lowered = Wiggers direction) ===")
    print(f"  train:    {one_sided_lo_train['verdict']} "
          f"(freq={one_sided_lo_train.get('frac_event', 0)*100:.1f}%, "
          f"disc={one_sided_lo_train.get('discrimination_pp', 0):+.1f} pp)")
    print(f"  validate: {one_sided_lo_val['verdict']} "
          f"(freq={one_sided_lo_val.get('frac_event', 0)*100:.1f}%, "
          f"disc={one_sided_lo_val.get('discrimination_pp', 0):+.1f} pp)")

    print("\n=== DIRECTIONALITY SPLIT (over triggering events, primary) ===")
    for era_label, r in [("train", train_v), ("validate", val_v)]:
        n_t = r.get("n_triggering", 0)
        if n_t == 0:
            print(f"  {era_label}: no triggering events")
            continue
        n_e = r.get("n_elevated", 0)
        n_l = r.get("n_lowered", 0)
        print(f"  {era_label}: {n_t} triggering | "
              f"{n_e} elevated ({100*n_e/n_t:.0f}%) | "
              f"{n_l} lowered ({100*n_l/n_t:.0f}%)")

    OUT_JSON.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
