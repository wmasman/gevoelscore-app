"""HA07d - Sleep stress stdev delta night-over-night (z-score).

Bidirectional primary. The physiological direction is ambiguous
a priori; either elevated or lowered variability shift could
precede crashes.
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
MIN_BASELINE_STD = 0.5  # stress-points; lower than HA07c's 2.0

LEADUP_PRIMARY = 4
LEADUP_SECONDARY = 5
MIN_LEADUP_VALID_PRIMARY = 3
MIN_LEADUP_VALID_SECONDARY = 4

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


def load_stress_stdevs() -> dict[date, float]:
    """Load per-night sleep stress STDEV values from extracted CSV."""
    out: dict[date, float] = {}
    with NIGHTLY_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1" or not r["stress_stdev"]:
                continue
            out[date.fromisoformat(r["date"])] = float(r["stress_stdev"])
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


def trimmed_list(values, trim_pct):
    if not values: return []
    vs = sorted(values); n = len(vs); trim = int(n * trim_pct)
    if n - 2*trim < 1: return vs
    return vs[trim:n-trim]


def compute_delta_dod(d: date, stdevs: dict[date, float]) -> float | None:
    if d not in stdevs: return None
    prev = d - timedelta(days=1)
    if prev not in stdevs: return None
    return stdevs[d] - stdevs[prev]


def compute_baseline_delta_mu_sigma(d, stdevs):
    prior = []
    for i in range(LAGGED_WINDOW_START_DAYS+1, LAGGED_WINDOW_END_DAYS+1):
        delta = compute_delta_dod(d - timedelta(days=i), stdevs)
        if delta is not None: prior.append(delta)
    if len(prior) < MIN_LAGGED_DAYS: return None, None
    trimmed = trimmed_list(prior, TRIMMED_PCT)
    if len(trimmed) < 2: return None, None
    mu, sigma = statistics.mean(trimmed), statistics.stdev(trimmed)
    if sigma < MIN_BASELINE_STD: return None, None
    return mu, sigma


def per_day_z(d, stdevs):
    delta = compute_delta_dod(d, stdevs)
    if delta is None: return None, None
    mu, sigma = compute_baseline_delta_mu_sigma(d, stdevs)
    if mu is None or sigma is None: return None, None
    signed = (delta - mu) / sigma
    return signed, abs(signed)


def episode_profile(ref, stdevs, leadup_days, min_valid):
    signed_zs = []
    for i in range(1, leadup_days+1):
        wd = ref - timedelta(days=i)
        signed, _ = per_day_z(wd, stdevs)
        if signed is None: continue
        signed_zs.append((wd, signed))
    if len(signed_zs) < min_valid: return None
    abs_pairs = [(d, abs(s)) for d, s in signed_zs]
    max_abs_pair = max(abs_pairs, key=lambda x: x[1])
    max_signed_at_max_abs = dict(signed_zs)[max_abs_pair[0]]
    return {
        "leadup_n": len(signed_zs),
        "max_abs_z": max_abs_pair[1],
        "max_signed_at_max_abs": max_signed_at_max_abs,
        "max_signed_z": max(s for _,s in signed_zs),
        "min_signed_z": min(s for _,s in signed_zs),
    }


def build_null_sample(stdevs, crashes, leadup_days, min_valid):
    rng = random.Random(RANDOM_SEED)
    occupied = set()
    for ref in crashes:
        for i in range(1, leadup_days+1):
            occupied.add(ref - timedelta(days=i))
    all_dates = sorted(d for d in stdevs if ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END)
    out, attempts = [], 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 20000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, leadup_days+1)}
        if leadup & occupied: continue
        prof = episode_profile(ref, stdevs, leadup_days, min_valid)
        if prof is None: continue
        out.append({"ref": ref, **prof})
    return out


def evaluate_arm(events, null, N_std, mode):
    if len(events) < 10:
        return {"verdict": "inconclusive", "n_clean": len(events)}
    def trigger(e):
        if mode == "bidirectional": return e["max_abs_z"] >= N_std
        if mode == "one_sided_elevated": return e["max_signed_z"] >= N_std
        return e["min_signed_z"] <= -N_std
    frac_event = sum(1 for e in events if trigger(e)) / len(events)
    frac_null = sum(1 for e in null if trigger(e)) / len(null)
    disc_pp = (frac_event - frac_null) * 100
    if mode == "bidirectional": mags = sorted(e["max_abs_z"] for e in events)
    elif mode == "one_sided_elevated": mags = sorted(e["max_signed_z"] for e in events)
    else: mags = sorted(abs(e["min_signed_z"]) for e in events)
    med = statistics.median(mags)
    a, b, c = frac_event >= CRIT_A_FRAC, disc_pp >= CRIT_B_DISC_PP, med >= N_std/2
    triggered = [e for e in events if trigger(e)]
    n_elev = sum(1 for e in triggered if e["max_signed_at_max_abs"] >= N_std)
    n_lo = sum(1 for e in triggered if e["max_signed_at_max_abs"] <= -N_std)
    return {
        "verdict": "supported" if (a and b and c) else "refuted",
        "n_clean": len(events), "n_null": len(null),
        "frac_event": frac_event, "frac_null": frac_null,
        "discrimination_pp": disc_pp, "median_magnitude": med,
        "crit_a_pass": a, "crit_b_pass": b, "crit_c_pass": c,
        "n_triggering": len(triggered),
        "n_elevated_at_max_abs": n_elev, "n_lowered_at_max_abs": n_lo,
    }


def dry_run(stdevs, crashes, k=3):
    train = [c for c in crashes if c <= TRAIN_END][:k]
    valid_c = [c for c in crashes if c > TRAIN_END][:k]
    print(f"\n=== DRY-RUN ===\n")
    n_low_var = n_no_delta = n_total = 0
    for ref in train + valid_c:
        era = "TRAIN" if ref <= TRAIN_END else "VALIDATE"
        print(f"--- {era} {ref} ---")
        print(f"  {'date':12} {'stdev':>6} {'delta':>7} {'mu':>7} {'sigma':>7} {'z':>7}")
        for i in range(1, LEADUP_SECONDARY+1):
            wd = ref - timedelta(days=i); n_total += 1
            sv = stdevs.get(wd); delta = compute_delta_dod(wd, stdevs)
            mu, sigma = compute_baseline_delta_mu_sigma(wd, stdevs)
            if sv is None:
                print(f"  {wd.isoformat():12} {'N/A':>6}")
                continue
            if delta is None:
                n_no_delta += 1
                print(f"  {wd.isoformat():12} {sv:>6.2f} {'NO PRIOR':>7}")
                continue
            if mu is None:
                n_low_var += 1
                print(f"  {wd.isoformat():12} {sv:>6.2f} {delta:>+7.2f} {'LOW VAR':>7}")
                continue
            signed = (delta - mu) / sigma
            print(f"  {wd.isoformat():12} {sv:>6.2f} {delta:>+7.2f} {mu:>+7.3f} {sigma:>7.3f} {signed:>+7.3f}")
        prof = episode_profile(ref, stdevs, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
        if prof:
            print(f"  4d max|z|={prof['max_abs_z']:.3f} (at-max-signed={prof['max_signed_at_max_abs']:+.3f})")
        print()
    print(f"=== END (low-var: {n_low_var}; no-delta: {n_no_delta}; total: {n_total}) ===")


def collect_events(refs, stdevs, leadup_days, min_valid):
    out = []
    for ref in refs:
        prof = episode_profile(ref, stdevs, leadup_days, min_valid)
        if prof is None: continue
        out.append({"ref": ref, **prof})
    return out


def main():
    p = argparse.ArgumentParser(); p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    stdevs = load_stress_stdevs()
    print(f"Loaded {len(stdevs)} valid nights")
    crashes = load_crashes()
    print(f"Loaded {len(crashes)} crashes")
    if args.dry_run:
        dry_run(stdevs, crashes); return 0
    train = [c for c in crashes if c <= TRAIN_END]
    val = [c for c in crashes if c > TRAIN_END]
    train_4d = collect_events(train, stdevs, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    val_4d = collect_events(val, stdevs, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    train_5d = collect_events(train, stdevs, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    val_5d = collect_events(val, stdevs, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    null_4d = build_null_sample(stdevs, crashes, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    null_5d = build_null_sample(stdevs, crashes, LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY)
    print(f"4d: train {len(train_4d)}/{len(train)}, validate {len(val_4d)}/{len(val)}")

    results = {}
    print("\n=== Evaluating ===")
    print(f"  {'arm':55} {'verdict':>11} {'frac':>9} {'null':>9} {'disc':>8} {'med':>7}")
    for wl, t_ev, v_ev, ns in [("4d_primary", train_4d, val_4d, null_4d), ("5d_secondary", train_5d, val_5d, null_5d)]:
        for N_std in [N_STD_PRIMARY, N_STD_SECONDARY, N_STD_SENSITIVITY]:
            for mode in ["bidirectional", "one_sided_elevated", "one_sided_lowered"]:
                for era, evs in [("train", t_ev), ("validate", v_ev)]:
                    key = f"{wl}_Nstd{N_std}_{mode}_{era}"
                    r = evaluate_arm(evs, ns, N_std, mode)
                    results[key] = r
                    if "frac_event" in r:
                        print(f"  {key:55} {r['verdict']:>11} "
                              f"{r['frac_event']*100:>8.1f}% {r['frac_null']*100:>8.1f}% "
                              f"{r['discrimination_pp']:>+7.1f} {r['median_magnitude']:>6.3f}")

    print("\n=== HEADLINE (primary 4d, N_std=1.5, BIDIRECTIONAL) ===")
    t = results["4d_primary_Nstd1.5_bidirectional_train"]
    v = results["4d_primary_Nstd1.5_bidirectional_validate"]
    print(f"  train:    {t['verdict']} (freq={t.get('frac_event',0)*100:.1f}%, disc={t.get('discrimination_pp',0):+.1f} pp)")
    print(f"  validate: {v['verdict']} (freq={v.get('frac_event',0)*100:.1f}%, disc={v.get('discrimination_pp',0):+.1f} pp)")

    OUT_JSON.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
