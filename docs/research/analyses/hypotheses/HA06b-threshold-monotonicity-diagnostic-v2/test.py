"""HA06b v2 diagnostic — compute fine grid + apply v2 criteria.

HA06b had no v1 diagnostic. This is the first threshold-monotonicity
diagnostic on HA06b. Uses HA06b's test machinery (nightly RHR z-score
against lagged baseline) over the 13-tier fine N_std grid.
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
METHODOLOGY_DIR = HERE.parent.parent / "methodology"
sys.path.insert(0, str(METHODOLOGY_DIR))
from v2_criteria import apply_v2_verdict  # noqa: E402

ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)

LAGGED_WINDOW_START_DAYS = 30
LAGGED_WINDOW_END_DAYS = 90
MIN_LAGGED_DAYS = 40
TRIMMED_PCT = 0.10
MIN_BASELINE_STD = 0.5

LEADUP_PRIMARY = 4
MIN_LEADUP_VALID_PRIMARY = 3

RHR_MIN_VALID = 30
RHR_MAX_VALID = 130

NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

N_STD_GRID = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5, 4.0]

LABELS_CSV = HERE.parent / "crash_v2-definition" / "labels_crash_v2.csv"
GARMIN_UDS_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Aggregator"
)
OUT_JSON = HERE / "result-data.json"


def load_rhr_by_date():
    out = {}
    for p in sorted(GARMIN_UDS_DIR.glob("UDSFile_*.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            rhr = rec.get("restingHeartRate")
            if not cd or rhr in (None, 0):
                continue
            try:
                v = int(rhr)
            except (TypeError, ValueError):
                continue
            if v < RHR_MIN_VALID or v > RHR_MAX_VALID:
                continue
            d = date.fromisoformat(cd)
            if d in out and v <= out[d]:
                continue
            out[d] = v
    return out


def load_crashes():
    crashes_by_id = {}
    with LABELS_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["label"] != "crash":
                continue
            d = date.fromisoformat(r["date"])
            crashes_by_id.setdefault(r["episode_id"], []).append(d)
    return sorted(min(ds) for ds in crashes_by_id.values())


def trimmed_list(values, pct):
    if not values: return []
    vs = sorted(values); n = len(vs); trim = int(n * pct)
    if n - 2*trim < 1: return vs
    return vs[trim:n-trim]


def compute_baseline(d, rhr_by_date):
    prior = []
    for i in range(LAGGED_WINDOW_START_DAYS+1, LAGGED_WINDOW_END_DAYS+1):
        wd = d - timedelta(days=i)
        if wd in rhr_by_date:
            prior.append(float(rhr_by_date[wd]))
    if len(prior) < MIN_LAGGED_DAYS: return None, None
    trimmed = trimmed_list(prior, TRIMMED_PCT)
    if len(trimmed) < 2: return None, None
    mu = statistics.mean(trimmed); sigma = statistics.stdev(trimmed)
    if sigma < MIN_BASELINE_STD: return None, None
    return mu, sigma


def per_day_z(d, rhr_by_date):
    if d not in rhr_by_date: return None
    mu, sigma = compute_baseline(d, rhr_by_date)
    if mu is None: return None
    return (float(rhr_by_date[d]) - mu) / sigma


def episode_profile(ref, rhr_by_date, leadup_days, min_valid):
    signed = []
    for i in range(1, leadup_days+1):
        z = per_day_z(ref - timedelta(days=i), rhr_by_date)
        if z is not None: signed.append(z)
    if len(signed) < min_valid: return None
    return {
        "max_abs_z": max(abs(s) for s in signed),
        "max_signed_z": max(signed),
        "min_signed_z": min(signed),
    }


def build_null_sample(rhr_by_date, crashes, leadup_days, min_valid):
    rng = random.Random(RANDOM_SEED)
    occupied = set()
    for ref in crashes:
        for i in range(1, leadup_days+1):
            occupied.add(ref - timedelta(days=i))
    all_dates = sorted(d for d in rhr_by_date if ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END)
    out, attempts = [], 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 10000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, leadup_days+1)}
        if leadup & occupied: continue
        prof = episode_profile(ref, rhr_by_date, leadup_days, min_valid)
        if prof is None: continue
        out.append(prof)
    return out


def trigger_bidir(e, N_std):
    return e["max_abs_z"] >= N_std


def evaluate(events, null, N_std):
    if len(events) < 10:
        return None
    fe = sum(1 for e in events if trigger_bidir(e, N_std)) / len(events)
    fn = sum(1 for e in null if trigger_bidir(e, N_std)) / len(null)
    return (fe - fn) * 100


def main():
    print("Loading RHR (same as HA06b)...")
    rhr_by_date = load_rhr_by_date()
    crashes = load_crashes()
    train = [c for c in crashes if c <= TRAIN_END]
    val = [c for c in crashes if c > TRAIN_END]
    print(f"  {len(rhr_by_date)} valid days; {len(crashes)} crashes (train {len(train)}, validate {len(val)})")

    train_events = [e for e in (episode_profile(c, rhr_by_date, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY) for c in train) if e]
    val_events = [e for e in (episode_profile(c, rhr_by_date, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY) for c in val) if e]
    null = build_null_sample(rhr_by_date, crashes, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    print(f"  train_events: {len(train_events)}, val_events: {len(val_events)}, null: {len(null)}")
    print()

    print("=" * 70)
    print("HA06b v2 diagnostic — fine grid (bidirectional primary)")
    print("=" * 70)

    train_disc = {}
    val_disc = {}
    print(f"  {'N_std':>6}  {'train':>8}  {'validate':>8}")
    for N_std in N_STD_GRID:
        td = evaluate(train_events, null, N_std)
        vd = evaluate(val_events, null, N_std)
        if td is not None: train_disc[N_std] = td
        if vd is not None: val_disc[N_std] = vd
        print(f"  {N_std:>6.2f}  {td if td is None else f'{td:+7.1f}':>8}  {vd if vd is None else f'{vd:+7.1f}':>8}")

    print()
    print("--- PRIMARY ARM (train bidirectional; HA06b train SUPPORTED at v1 primary) ---")
    v2_train = apply_v2_verdict(train_disc)
    _print_verdict(v2_train)

    print("\n--- Validate bidirectional (descriptive; HA06b validate was REFUTED) ---")
    v2_val = apply_v2_verdict(val_disc)
    _print_verdict(v2_val)

    out = {
        "train_bidirectional_disc": {str(k): v for k, v in train_disc.items()},
        "validate_bidirectional_disc": {str(k): v for k, v in val_disc.items()},
        "v2_train_bidirectional": v2_train,
        "v2_validate_bidirectional": v2_val,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}")
    return 0


def _print_verdict(v2):
    print(f"Verdict: {v2['verdict']}")
    print(f"Rule applied: {v2['rule_applied']}")
    s = v2["shape_stats"]
    print(f"Shape stats (meaningful range [1.0, 3.0]):")
    print(f"  peak_n_std: {s['peak_n_std']}; peak_disc: {s['peak_disc']:.1f}")
    print(f"  sign_changes: {s['sign_changes']}; direction_reversals (descriptive): {s['direction_reversals']}")
    print(f"  spearman_rho: {s['spearman_rho']:+.3f}; max_neg_disc: {s['max_neg_disc']:.1f}")
    for cat_name in ["cat1_canonical_decline", "cat2_stable_plateau",
                     "cat3_rising_late_peak", "cat4_bumpy_sign_changes",
                     "cat5_loose_tail_noise"]:
        cat = v2[cat_name]
        status = ("PASS" if cat.get("pass") else "no") if "pass" in cat else ("FAIL TRIGGERED" if cat.get("fail_triggered") else "no")
        print(f"  {cat_name}: {status}")


if __name__ == "__main__":
    raise SystemExit(main())
