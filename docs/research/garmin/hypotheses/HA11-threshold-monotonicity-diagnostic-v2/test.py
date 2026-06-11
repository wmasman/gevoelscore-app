"""HA11 v2 diagnostic — compute fine grid + apply v2 criteria.

HA11's locked primary direction is ONE-SIDED ELEVATED (not bidirectional).
Per HA11 diagnostic.md, v2 evaluates HA11's actual locked primary
direction, not artificially imposed as bidirectional. The v2 five-category
shape rule applies identically to one-sided arms as to bidirectional arms.
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

NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

N_STD_GRID = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5, 4.0]

LABELS_CSV = HERE.parent / "crash_v2-definition" / "labels_crash_v2.csv"
UDIP_CSV = HERE.parent / "HA11-stress-udip" / "udip_counts.csv"
OUT_JSON = HERE / "result-data.json"


def load_udip_counts():
    counts, valid = {}, {}
    with UDIP_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            counts[d] = int(r["u_dip_count"])
            valid[d] = r["valid"] == "1"
    return counts, valid


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


def compute_baseline(d, counts, valid):
    prior = []
    for i in range(LAGGED_WINDOW_START_DAYS+1, LAGGED_WINDOW_END_DAYS+1):
        wd = d - timedelta(days=i)
        if wd in counts and valid.get(wd, False):
            prior.append(float(counts[wd]))
    if len(prior) < MIN_LAGGED_DAYS: return None, None
    trimmed = trimmed_list(prior, TRIMMED_PCT)
    if len(trimmed) < 2: return None, None
    mu = statistics.mean(trimmed); sigma = statistics.stdev(trimmed)
    if sigma < MIN_BASELINE_STD: return None, None
    return mu, sigma


def per_day_z(d, counts, valid):
    if d not in counts or not valid.get(d, False): return None
    mu, sigma = compute_baseline(d, counts, valid)
    if mu is None: return None
    return (float(counts[d]) - mu) / sigma


def episode_profile(ref, counts, valid, leadup_days, min_valid):
    signed = []
    for i in range(1, leadup_days+1):
        z = per_day_z(ref - timedelta(days=i), counts, valid)
        if z is not None: signed.append(z)
    if len(signed) < min_valid: return None
    return {
        "max_abs_z": max(abs(s) for s in signed),
        "max_signed_z": max(signed),
        "min_signed_z": min(signed),
    }


def build_null_sample(counts, valid, crashes, leadup_days, min_valid):
    rng = random.Random(RANDOM_SEED)
    occupied = set()
    for ref in crashes:
        for i in range(1, leadup_days+1):
            occupied.add(ref - timedelta(days=i))
    all_dates = sorted(d for d in counts if valid.get(d, False)
                       and ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END)
    out, attempts = [], 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 20000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, leadup_days+1)}
        if leadup & occupied: continue
        prof = episode_profile(ref, counts, valid, leadup_days, min_valid)
        if prof is None: continue
        out.append(prof)
    return out


def trigger_one_sided_elevated(e, N_std):
    return e["max_signed_z"] >= N_std


def evaluate_one_sided_elevated(events, null, N_std):
    if len(events) < 10:
        return None
    fe = sum(1 for e in events if trigger_one_sided_elevated(e, N_std)) / len(events)
    fn = sum(1 for e in null if trigger_one_sided_elevated(e, N_std)) / len(null)
    return (fe - fn) * 100


def main():
    print("Loading U-dip counts (same as HA11)...")
    counts, valid = load_udip_counts()
    crashes = load_crashes()
    train = [c for c in crashes if c <= TRAIN_END]
    val = [c for c in crashes if c > TRAIN_END]
    print(f"  {sum(1 for d in counts if valid[d])} valid nights; {len(crashes)} crashes (train {len(train)}, validate {len(val)})")

    train_events = [e for e in (episode_profile(c, counts, valid, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY) for c in train) if e]
    val_events = [e for e in (episode_profile(c, counts, valid, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY) for c in val) if e]
    null = build_null_sample(counts, valid, crashes, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    print(f"  train_events: {len(train_events)}, val_events: {len(val_events)}, null: {len(null)}")
    print()

    print("=" * 70)
    print("HA11 v2 diagnostic — fine grid (ONE-SIDED ELEVATED primary)")
    print("=" * 70)

    train_disc = {}
    val_disc = {}
    print(f"  {'N_std':>6}  {'train':>8}  {'validate':>8}")
    for N_std in N_STD_GRID:
        td = evaluate_one_sided_elevated(train_events, null, N_std)
        vd = evaluate_one_sided_elevated(val_events, null, N_std)
        if td is not None: train_disc[N_std] = td
        if vd is not None: val_disc[N_std] = vd
        print(f"  {N_std:>6.2f}  {td if td is None else f'{td:+7.1f}':>8}  {vd if vd is None else f'{vd:+7.1f}':>8}")

    print()
    print("--- PRIMARY ARM (train one-sided elevated; HA11 train SUPPORTED at v1 primary) ---")
    v2_train = apply_v2_verdict(train_disc)
    _print_verdict(v2_train)

    print("\n--- Validate one-sided elevated (descriptive; HA11 validate was REFUTED inverse) ---")
    v2_val = apply_v2_verdict(val_disc)
    _print_verdict(v2_val)

    out = {
        "train_one_sided_elevated_disc": {str(k): v for k, v in train_disc.items()},
        "validate_one_sided_elevated_disc": {str(k): v for k, v in val_disc.items()},
        "v2_train_one_sided_elevated": v2_train,
        "v2_validate_one_sided_elevated": v2_val,
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
