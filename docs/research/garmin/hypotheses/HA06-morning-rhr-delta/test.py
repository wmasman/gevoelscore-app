"""HA06 — Bidirectional nightly RHR delta as crash precursor.

Implements the protocol pre-registered in hypothesis.md exactly.

Reads:
- restingHeartRate from Garmin UDS files (same field + path as H01).
- crash_v1 episode labels from crash_v2-definition/labels_crash_v2.csv.

Computes for each crash episode:
- Lagged baseline (Theme A): trimmed mean of RHR over [d-90, d-30]
  per lead-up day; min 40 of 60 prior valid days.
- |delta| per lead-up day; max over 4-day primary / 5-day secondary
  windows.
- Episode trigger flag (bidirectional |delta| >= N for N in 5/10/15).
- Sensitivity arm: one-sided delta >= N (elevated only).

Same null sample seed (20260605) and machinery as scripts 08/09/12.
Both-era evaluation per D7 reframe pre-commitment.

Usage:
  # Pre-lock check (prints first 3 episodes' raw values, doesn't run
  # the full test):
  python test.py --dry-run

  # Full run (only after dry-run check passes):
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

# Locked parameters - mirror hypothesis.md exactly
ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)

# Lagged baseline (Theme A)
LAGGED_WINDOW_START_DAYS = 30
LAGGED_WINDOW_END_DAYS = 90
LAGGED_WINDOW_LEN = LAGGED_WINDOW_END_DAYS - LAGGED_WINDOW_START_DAYS  # 60
MIN_LAGGED_DAYS = 40
TRIMMED_PCT = 0.10

# Lead-up windows
LEADUP_PRIMARY = 4
LEADUP_SECONDARY = 5
MIN_LEADUP_VALID_PRIMARY = 3   # of 4
MIN_LEADUP_VALID_SECONDARY = 4  # of 5

# Thresholds (bpm)
N_PRIMARY = 5    # Wiggers 5-10 floor
N_SECONDARY = 10  # Workwell 10-15 lower bound
N_SENSITIVITY = 15  # Workwell upper bound

# RHR validity range (preserves chronic-illness ranges)
RHR_MIN_VALID = 30
RHR_MAX_VALID = 130

# Null sample
NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

# Pre-registered SUPPORTED bar
CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABELS_CSV = ROOT / "crash_v2-definition" / "labels_crash_v2.csv"
GARMIN_UDS_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Aggregator"
)
OUT_MD = HERE / "result.md"
OUT_JSON = HERE / "result-data.json"


def load_rhr_by_date() -> dict[date, int]:
    """Load nightly restingHeartRate from all UDS files. Same field
    and extraction logic as H01.
    """
    out: dict[date, int] = {}
    files = sorted(GARMIN_UDS_DIR.glob("UDSFile_*.json"))
    for p in files:
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            rhr = rec.get("restingHeartRate")
            if not cd or rhr in (None, 0):
                continue
            try:
                rhr_int = int(rhr)
            except (TypeError, ValueError):
                continue
            if rhr_int < RHR_MIN_VALID or rhr_int > RHR_MAX_VALID:
                continue
            d = date.fromisoformat(cd)
            # Dedup across overlapping files: keep the higher value
            # (Garmin sometimes writes a placeholder lower value)
            if d in out and rhr_int <= out[d]:
                continue
            out[d] = rhr_int
    return out


def load_crashes() -> list[date]:
    """Load crash episode start dates from labels_crash_v2.csv."""
    crashes_by_id: dict[str, list[date]] = {}
    with LABELS_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["label"] != "crash":
                continue
            d = date.fromisoformat(r["date"])
            crashes_by_id.setdefault(r["episode_id"], []).append(d)
    return sorted(min(ds) for ds in crashes_by_id.values())


def trimmed_mean(values: list[float], trim_pct: float) -> float | None:
    if not values:
        return None
    vs = sorted(values)
    n = len(vs)
    trim = int(n * trim_pct)
    if n - 2 * trim < 1:
        return statistics.mean(vs)
    return statistics.mean(vs[trim : n - trim])


def compute_lagged_baseline(
    d: date, rhr_by_date: dict[date, int]
) -> float | None:
    """Trimmed-mean RHR over [d-90, d-30]. Returns None if fewer than
    40 of 60 prior days have valid RHR.
    """
    prior_vals: list[float] = []
    for i in range(LAGGED_WINDOW_START_DAYS + 1, LAGGED_WINDOW_END_DAYS + 1):
        wd = d - timedelta(days=i)
        if wd in rhr_by_date:
            prior_vals.append(float(rhr_by_date[wd]))
    if len(prior_vals) < MIN_LAGGED_DAYS:
        return None
    return trimmed_mean(prior_vals, TRIMMED_PCT)


def per_day_delta(
    d: date, rhr_by_date: dict[date, int]
) -> tuple[float | None, float | None]:
    """Returns (signed_delta, abs_delta) for date d. Either may be
    None if RHR or baseline is undefined.
    """
    if d not in rhr_by_date:
        return None, None
    baseline = compute_lagged_baseline(d, rhr_by_date)
    if baseline is None:
        return None, None
    signed = float(rhr_by_date[d]) - baseline
    return signed, abs(signed)


def episode_profile(
    ref: date,
    rhr_by_date: dict[date, int],
    leadup_days: int,
    min_valid: int,
) -> dict | None:
    """Compute per-episode profile for the given reference date and
    lead-up window length. Returns None if too few valid lead-up days.

    Profile fields:
      - leadup_n: count of valid lead-up days (with RHR + baseline)
      - max_abs_delta: max |delta| across valid lead-up days
      - max_signed_delta: signed delta on the day where |delta| was max
      - all_signed_deltas: list of signed deltas for valid days
      - triggering_signs: per threshold N, list of sign chars
    """
    signed_deltas: list[tuple[date, float]] = []
    for i in range(1, leadup_days + 1):
        wd = ref - timedelta(days=i)
        signed, abs_d = per_day_delta(wd, rhr_by_date)
        if signed is None:
            continue
        signed_deltas.append((wd, signed))
    if len(signed_deltas) < min_valid:
        return None
    abs_pairs = [(d, abs(s)) for d, s in signed_deltas]
    max_abs_pair = max(abs_pairs, key=lambda x: x[1])
    max_signed = dict(signed_deltas)[max_abs_pair[0]]
    return {
        "leadup_n": len(signed_deltas),
        "max_abs_delta": max_abs_pair[1],
        "max_signed_delta": max_signed,
        "all_signed_deltas": [s for _, s in signed_deltas],
    }


def build_null_sample(
    rhr_by_date: dict[date, int],
    crash_starts: list[date],
    leadup_days: int,
    min_valid: int,
) -> list[dict]:
    """200 random non-overlapping reference dates, lagged-baseline-defined
    profile. Seed 20260605 (matches scripts 08/09/12).
    """
    rng = random.Random(RANDOM_SEED)
    occupied: set[date] = set()
    for ref in crash_starts:
        for i in range(1, leadup_days + 1):
            occupied.add(ref - timedelta(days=i))
    all_dates = sorted(
        d for d in rhr_by_date if ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END
    )
    out: list[dict] = []
    attempts = 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 10000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, leadup_days + 1)}
        if leadup & occupied:
            continue
        prof = episode_profile(ref, rhr_by_date, leadup_days, min_valid)
        if prof is None:
            continue
        out.append({"ref": ref, **prof})
    return out


def evaluate_arm(
    events: list[dict],
    null: list[dict],
    N: float,
    bidirectional: bool,
) -> dict:
    """Evaluate the 3-criterion bar for one (events x N x direction) combo.
    bidirectional=True uses |delta| >= N; False uses delta >= N.
    """
    if len(events) < 10:
        return {"verdict": "inconclusive", "n_clean": len(events)}

    def trigger(e: dict) -> bool:
        if bidirectional:
            return e["max_abs_delta"] >= N
        return e["max_signed_delta"] >= N

    frac_event = sum(1 for e in events if trigger(e)) / len(events)
    frac_null = sum(1 for e in null if trigger(e)) / len(null)
    disc_pp = (frac_event - frac_null) * 100
    abs_deltas = sorted(e["max_abs_delta"] for e in events)
    median_abs = statistics.median(abs_deltas)

    a = frac_event >= CRIT_A_FRAC
    b = disc_pp >= CRIT_B_DISC_PP
    c = median_abs >= N / 2

    # Directionality split (over triggering events only)
    triggered = [e for e in events if trigger(e)]
    n_elev = sum(1 for e in triggered if e["max_signed_delta"] >= N)
    n_lowered = sum(1 for e in triggered if e["max_signed_delta"] <= -N)
    n_other = len(triggered) - n_elev - n_lowered

    return {
        "verdict": "supported" if (a and b and c) else "refuted",
        "n_clean": len(events),
        "n_null": len(null),
        "frac_event": frac_event,
        "frac_null": frac_null,
        "discrimination_pp": disc_pp,
        "median_abs_delta": median_abs,
        "crit_a_pass": a,
        "crit_b_pass": b,
        "crit_c_pass": c,
        "n_triggering": len(triggered),
        "n_elevated": n_elev,
        "n_lowered": n_lowered,
        "n_other_direction": n_other,
    }


def dry_run(rhr_by_date: dict[date, int], crashes: list[date], k: int = 3) -> None:
    """Print first k crash episodes' computed values without running
    the full pipeline. Methodology lesson from H03/H05.
    """
    print(f"\n=== DRY-RUN: first {k} crash episodes ===\n")
    train_crashes = [c for c in crashes if c <= TRAIN_END]
    validate_crashes = [c for c in crashes if c > TRAIN_END]
    sample = train_crashes[:k] + validate_crashes[:k]
    for ref in sample:
        era = "TRAIN" if ref <= TRAIN_END else "VALIDATE"
        print(f"--- {era} crash starting {ref} ---")
        # Show the per-day values for the 5-day window (covers both primary 4d and secondary 5d)
        print(
            f"  {'date':12} {'rhr':>5} {'baseline':>10} {'delta':>8} {'|delta|':>8}"
        )
        for i in range(1, LEADUP_SECONDARY + 1):
            wd = ref - timedelta(days=i)
            rhr_val = rhr_by_date.get(wd)
            baseline = compute_lagged_baseline(wd, rhr_by_date)
            if rhr_val is None or baseline is None:
                print(f"  {wd.isoformat():12} {'N/A' if rhr_val is None else rhr_val:>5} "
                      f"{'N/A' if baseline is None else f'{baseline:.1f}':>10} "
                      f"{'N/A':>8} {'N/A':>8}")
                continue
            signed = rhr_val - baseline
            print(f"  {wd.isoformat():12} {rhr_val:>5} {baseline:>10.1f} "
                  f"{signed:>+8.2f} {abs(signed):>8.2f}")
        prof_4d = episode_profile(ref, rhr_by_date, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
        prof_5d = episode_profile(ref, rhr_by_date, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
        if prof_4d:
            print(f"  primary 4d: max|delta|={prof_4d['max_abs_delta']:.2f} "
                  f"(signed={prof_4d['max_signed_delta']:+.2f}); "
                  f"n_valid={prof_4d['leadup_n']}/{LEADUP_PRIMARY}")
        else:
            print(f"  primary 4d: insufficient data (need {MIN_LEADUP_VALID_PRIMARY} valid days)")
        if prof_5d:
            print(f"  secondary 5d: max|delta|={prof_5d['max_abs_delta']:.2f} "
                  f"(signed={prof_5d['max_signed_delta']:+.2f}); "
                  f"n_valid={prof_5d['leadup_n']}/{LEADUP_SECONDARY}")
        else:
            print(f"  secondary 5d: insufficient data (need {MIN_LEADUP_VALID_SECONDARY} valid days)")
        print()
    print("=== DRY-RUN END ===")
    print("Eyeball check: do per-day RHR + baseline + delta values look")
    print("plausible? If yes, re-run without --dry-run.")


def collect_events(
    refs: list[date],
    rhr_by_date: dict[date, int],
    leadup_days: int,
    min_valid: int,
) -> list[dict]:
    out: list[dict] = []
    for ref in refs:
        prof = episode_profile(ref, rhr_by_date, leadup_days, min_valid)
        if prof is None:
            continue
        out.append({"ref": ref, **prof})
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print("Loading nightly RHR from UDS...")
    rhr_by_date = load_rhr_by_date()
    print(f"  {len(rhr_by_date)} days with valid RHR")

    print("Loading crash labels...")
    crashes = load_crashes()
    print(f"  {len(crashes)} crash episodes total")
    train_crashes = [c for c in crashes if c <= TRAIN_END]
    validate_crashes = [c for c in crashes if c > TRAIN_END]
    print(f"  train: {len(train_crashes)}; validate: {len(validate_crashes)}")

    # Coverage report
    in_window_dates = [d for d in rhr_by_date if ANALYSIS_START <= d <= VALIDATE_END]
    total_days = (VALIDATE_END - ANALYSIS_START).days + 1
    train_days = (TRAIN_END - ANALYSIS_START).days + 1
    validate_days = total_days - train_days
    train_with_rhr = sum(1 for d in in_window_dates if d <= TRAIN_END)
    validate_with_rhr = sum(1 for d in in_window_dates if d > TRAIN_END)
    print(f"  night coverage: train {train_with_rhr}/{train_days} "
          f"({100*train_with_rhr/train_days:.1f}%); "
          f"validate {validate_with_rhr}/{validate_days} "
          f"({100*validate_with_rhr/validate_days:.1f}%)")

    if args.dry_run:
        dry_run(rhr_by_date, crashes)
        return 0

    print("\nCollecting per-episode profiles...")
    train_events_4d = collect_events(train_crashes, rhr_by_date, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    validate_events_4d = collect_events(validate_crashes, rhr_by_date, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    train_events_5d = collect_events(train_crashes, rhr_by_date, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    validate_events_5d = collect_events(validate_crashes, rhr_by_date, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    print(f"  4d primary: train {len(train_events_4d)}/{len(train_crashes)}, "
          f"validate {len(validate_events_4d)}/{len(validate_crashes)}")
    print(f"  5d secondary: train {len(train_events_5d)}/{len(train_crashes)}, "
          f"validate {len(validate_events_5d)}/{len(validate_crashes)}")

    print("\nBuilding null samples...")
    null_4d = build_null_sample(rhr_by_date, crashes, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    null_5d = build_null_sample(rhr_by_date, crashes, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    print(f"  null_4d: {len(null_4d)}; null_5d: {len(null_5d)}")

    results: dict[str, dict] = {}
    print("\n=== Evaluating all combinations ===")
    print(f"  {'arm':40} {'verdict':>11} {'frac_event':>11} {'frac_null':>11} "
          f"{'disc_pp':>9} {'median':>8}")
    for window_label, train_evt, validate_evt, null_sample in [
        ("4d_primary", train_events_4d, validate_events_4d, null_4d),
        ("5d_secondary", train_events_5d, validate_events_5d, null_5d),
    ]:
        for N in [N_PRIMARY, N_SECONDARY, N_SENSITIVITY]:
            for direction_label, bidirectional in [("bidirectional", True), ("one_sided", False)]:
                for era_label, events in [("train", train_evt), ("validate", validate_evt)]:
                    key = f"{window_label}_N{int(N)}_{direction_label}_{era_label}"
                    r = evaluate_arm(events, null_sample, N, bidirectional)
                    results[key] = r
                    verdict = r["verdict"]
                    if "frac_event" in r:
                        print(f"  {key:40} {verdict:>11} "
                              f"{r['frac_event']*100:>10.1f}% "
                              f"{r['frac_null']*100:>10.1f}% "
                              f"{r['discrimination_pp']:>+8.1f} "
                              f"{r['median_abs_delta']:>7.2f}")
                    else:
                        print(f"  {key:40} {verdict:>11}  (insufficient n)")

    # Headline: primary 4d, N=5, bidirectional, both eras must support
    print("\n=== HEADLINE VERDICT (primary 4d, N=5, bidirectional) ===")
    headline_train = results["4d_primary_N5_bidirectional_train"]
    headline_val = results["4d_primary_N5_bidirectional_validate"]
    one_sided_train = results["4d_primary_N5_one_sided_train"]
    one_sided_val = results["4d_primary_N5_one_sided_validate"]
    train_v = headline_train["verdict"]
    val_v = headline_val["verdict"]
    if train_v == "supported" and val_v == "supported":
        overall = "SUPPORTED (both eras)"
    elif train_v == "supported" or val_v == "supported":
        overall = f"PARTIAL (train={train_v}, validate={val_v})"
    elif "inconclusive" in (train_v, val_v):
        overall = "INCONCLUSIVE"
    else:
        overall = "REFUTED (both eras)"
    print(f"  train:    {train_v} "
          f"(freq={headline_train.get('frac_event', 0)*100:.1f}%, "
          f"disc={headline_train.get('discrimination_pp', 0):+.1f} pp)")
    print(f"  validate: {val_v} "
          f"(freq={headline_val.get('frac_event', 0)*100:.1f}%, "
          f"disc={headline_val.get('discrimination_pp', 0):+.1f} pp)")
    print(f"  overall:  {overall}")

    print("\n=== SENSITIVITY ARM (one-sided elevated only) ===")
    print(f"  train:    {one_sided_train['verdict']} "
          f"(freq={one_sided_train.get('frac_event', 0)*100:.1f}%, "
          f"disc={one_sided_train.get('discrimination_pp', 0):+.1f} pp)")
    print(f"  validate: {one_sided_val['verdict']} "
          f"(freq={one_sided_val.get('frac_event', 0)*100:.1f}%, "
          f"disc={one_sided_val.get('discrimination_pp', 0):+.1f} pp)")
    if headline_train.get("frac_event", 0) > 0 and one_sided_train.get("frac_event", 0) > 0:
        swing_train = (headline_train["frac_event"] - one_sided_train["frac_event"]) * 100
        print(f"  train bidirectional excess over one-sided: "
              f"{swing_train:+.1f} pp (parasympathetic-swing contribution)")
    if headline_val.get("frac_event", 0) > 0 and one_sided_val.get("frac_event", 0) > 0:
        swing_val = (headline_val["frac_event"] - one_sided_val["frac_event"]) * 100
        print(f"  validate bidirectional excess over one-sided: "
              f"{swing_val:+.1f} pp (parasympathetic-swing contribution)")

    print("\n=== DIRECTIONALITY SPLIT (over triggering events, primary) ===")
    for era_label, r in [("train", headline_train), ("validate", headline_val)]:
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
