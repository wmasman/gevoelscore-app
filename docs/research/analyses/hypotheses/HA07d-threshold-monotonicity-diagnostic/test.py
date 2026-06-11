"""HA07d threshold-monotonicity diagnostic.

Re-runs HA07d's locked test machinery across the 13-tier fine N_std
grid (0.5 -> 4.0). Locked rescue/close/ambiguous criteria applied
to BOTH eras since HA07d was the project's first overall-SUPPORTED
test.

Same input data as HA07d: sleep_stress_nightly.csv (stress_stdev
column). Same null seed, same lagged-baseline machinery.
"""
from __future__ import annotations

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
MIN_BASELINE_STD = 0.5

LEADUP_PRIMARY = 4
MIN_LEADUP_VALID_PRIMARY = 3

NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15

N_STD_GRID = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5, 4.0]

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABELS_CSV = ROOT / "crash_v2-definition" / "labels_crash_v2.csv"
NIGHTLY_CSV = (
    Path(__file__).resolve().parents[2]
    / "scripts" / "sleep_stress_extract" / "sleep_stress_nightly.csv"
)
OUT_JSON = HERE / "result-data.json"


def load_stress_stdevs():
    out = {}
    with NIGHTLY_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1" or not r["stress_stdev"]:
                continue
            out[date.fromisoformat(r["date"])] = float(r["stress_stdev"])
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


def compute_delta_dod(d, stdevs):
    if d not in stdevs: return None
    prev = d - timedelta(days=1)
    if prev not in stdevs: return None
    return stdevs[d] - stdevs[prev]


def compute_baseline_mu_sigma(d, stdevs):
    prior = []
    for i in range(LAGGED_WINDOW_START_DAYS+1, LAGGED_WINDOW_END_DAYS+1):
        delta = compute_delta_dod(d - timedelta(days=i), stdevs)
        if delta is not None:
            prior.append(delta)
    if len(prior) < MIN_LAGGED_DAYS: return None, None
    trimmed = trimmed_list(prior, TRIMMED_PCT)
    if len(trimmed) < 2: return None, None
    mu = statistics.mean(trimmed); sigma = statistics.stdev(trimmed)
    if sigma < MIN_BASELINE_STD: return None, None
    return mu, sigma


def per_day_z(d, stdevs):
    delta = compute_delta_dod(d, stdevs)
    if delta is None: return None
    mu, sigma = compute_baseline_mu_sigma(d, stdevs)
    if mu is None: return None
    return (delta - mu) / sigma


def episode_profile(ref, stdevs, leadup_days, min_valid):
    signed = []
    for i in range(1, leadup_days+1):
        z = per_day_z(ref - timedelta(days=i), stdevs)
        if z is not None: signed.append(z)
    if len(signed) < min_valid: return None
    return {
        "max_abs_z": max(abs(s) for s in signed),
        "max_signed_z": max(signed),
        "min_signed_z": min(signed),
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
        out.append(prof)
    return out


def trigger(e, N_std, mode):
    if mode == "bidirectional": return e["max_abs_z"] >= N_std
    if mode == "one_sided_elevated": return e["max_signed_z"] >= N_std
    return e["min_signed_z"] <= -N_std


def evaluate(events, null, N_std, mode):
    if len(events) < 10:
        return {"verdict": "inconclusive", "n": len(events)}
    fe = sum(1 for e in events if trigger(e, N_std, mode)) / len(events)
    fn = sum(1 for e in null if trigger(e, N_std, mode)) / len(null)
    disc = (fe - fn) * 100
    if mode == "bidirectional":
        mags = sorted(e["max_abs_z"] for e in events)
    elif mode == "one_sided_elevated":
        mags = sorted(e["max_signed_z"] for e in events)
    else:
        mags = sorted(abs(e["min_signed_z"]) for e in events)
    median = statistics.median(mags)
    a = fe >= CRIT_A_FRAC; b = disc >= CRIT_B_DISC_PP; c = median >= N_std/2
    return {
        "verdict": "supported" if (a and b and c) else "refuted",
        "freq": fe, "null_freq": fn, "disc_pp": disc, "median": median,
        "crit_a": a, "crit_b": b, "crit_c": c,
    }


def spearman_rho(xs, ys):
    n = len(xs)
    def rank(vs):
        idx = sorted(range(len(vs)), key=lambda i: vs[i])
        ranks = [0.0]*len(vs); i = 0
        while i < len(vs):
            j = i
            while j+1 < len(vs) and vs[idx[j+1]] == vs[idx[i]]: j += 1
            avg = (i+j)/2 + 1
            for k in range(i, j+1): ranks[idx[k]] = avg
            i = j+1
        return ranks
    rx, ry = rank(xs), rank(ys)
    mx, my = sum(rx)/n, sum(ry)/n
    num = sum((rx[i]-mx)*(ry[i]-my) for i in range(n))
    denx = (sum((rx[i]-mx)**2 for i in range(n)))**0.5
    deny = (sum((ry[i]-my)**2 for i in range(n)))**0.5
    return num/(denx*deny) if denx and deny else 0.0


def count_sign_changes(values):
    count = 0; prev = None
    for v in values:
        if v > 0: sign = 1
        elif v < 0: sign = -1
        else: continue
        if prev is not None and sign != prev: count += 1
        prev = sign
    return count


def compute_shape_stats(disc_by_N_std):
    grid = sorted(disc_by_N_std.keys())
    discs = [disc_by_N_std[n] for n in grid]
    peak_idx = max(range(len(discs)), key=lambda i: discs[i])
    peak_N_std = grid[peak_idx]; peak_disc = discs[peak_idx]
    target = peak_N_std + 0.5
    target_idx = min(range(len(grid)), key=lambda i: abs(grid[i]-target))
    decay = discs[target_idx]/peak_disc if peak_disc != 0 else float("nan")
    rho = spearman_rho(grid, discs)
    signs = count_sign_changes(discs)
    return {
        "peak_N_std": peak_N_std, "peak_disc": peak_disc,
        "decay_ratio_at_peak_plus_0.5": decay,
        "spearman_rho_Nstd_vs_disc": rho,
        "sign_changes_count": signs,
    }


def apply_verdict_criteria(stats, disc_2_0, disc_2_5):
    rescue = (
        1.0 <= stats["peak_N_std"] <= 1.5
        and disc_2_0 >= 10.0 and disc_2_5 >= 5.0
        and stats["spearman_rho_Nstd_vs_disc"] <= -0.3
        and stats["sign_changes_count"] <= 1
    )
    close = (
        stats["peak_N_std"] > 1.5 or stats["peak_N_std"] < 0.75
        or disc_2_0 < 5.0 or disc_2_5 < 0.0
        or stats["spearman_rho_Nstd_vs_disc"] > -0.1
        or stats["sign_changes_count"] >= 2
    )
    if rescue and not close: return "RESCUE"
    elif close: return "CLOSE"
    else: return "AMBIGUOUS"


def ascii_curve(disc_by_N_std, label, width=60):
    grid = sorted(disc_by_N_std.keys())
    discs = [disc_by_N_std[n] for n in grid]
    lo = min(min(discs), -20); hi = max(max(discs), 30)
    def pos(v): return int((v-lo)/(hi-lo)*(width-1))
    zero = pos(0)
    lines = [f"\n{label}:"]
    lines.append(f"  {'N_std':>6}  {'disc pp':>8}  " + " "*zero + "|" + " "*(width-zero-1))
    for n, d in zip(grid, discs):
        bar = [" "]*width; bar[zero] = "|"
        p = pos(d)
        if p >= zero:
            for i in range(zero, p+1): bar[i] = "#"
        else:
            for i in range(p, zero+1): bar[i] = "#"
        lines.append(f"  {n:>6.2f}  {d:>+7.1f}  " + "".join(bar))
    return "\n".join(lines)


def main():
    print("Loading sleep stress STDEV (same as HA07d)...")
    stdevs = load_stress_stdevs()
    print(f"  {len(stdevs)} valid nights")
    crashes = load_crashes()
    train = [c for c in crashes if c <= TRAIN_END]
    val = [c for c in crashes if c > TRAIN_END]
    print(f"  {len(crashes)} crashes; train {len(train)} validate {len(val)}")

    train_events = [e for e in (episode_profile(c, stdevs, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY) for c in train) if e]
    val_events = [e for e in (episode_profile(c, stdevs, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY) for c in val) if e]
    null = build_null_sample(stdevs, crashes, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    print(f"  train_events: {len(train_events)}, val_events: {len(val_events)}, null: {len(null)}")
    print()

    table = {}
    for direction in ["bidirectional", "one_sided_elevated", "one_sided_lowered"]:
        table[direction] = {}
        for era, events in [("train", train_events), ("validate", val_events)]:
            table[direction][era] = {}
            for N_std in N_STD_GRID:
                table[direction][era][N_std] = evaluate(events, null, N_std, direction)

    print("=" * 70)
    print("FINE GRID DISCRIMINATION TABLE")
    print("=" * 70)
    for direction in ["bidirectional", "one_sided_elevated", "one_sided_lowered"]:
        print(f"\n--- {direction} ---")
        print(f"  {'N_std':>6}  {'train_disc':>10}  {'val_disc':>9}  "
              f"{'train_freq':>10}  {'val_freq':>9}  {'null_freq':>9}")
        for N_std in N_STD_GRID:
            t = table[direction]["train"][N_std]; v = table[direction]["validate"][N_std]
            print(f"  {N_std:>6.2f}  "
                  f"{t.get('disc_pp', 0):>+9.1f}  {v.get('disc_pp', 0):>+8.1f}  "
                  f"{t.get('freq', 0)*100:>9.1f}%  {v.get('freq', 0)*100:>8.1f}%  "
                  f"{t.get('null_freq', 0)*100:>8.1f}%")

    print("\n" + "=" * 70)
    print("SHAPE STATISTICS")
    print("=" * 70)
    shape_results = {}
    for direction in ["bidirectional", "one_sided_elevated", "one_sided_lowered"]:
        shape_results[direction] = {}
        for era in ["train", "validate"]:
            disc_by_N_std = {N_std: table[direction][era][N_std].get("disc_pp", 0) for N_std in N_STD_GRID}
            stats = compute_shape_stats(disc_by_N_std)
            shape_results[direction][era] = stats
            print(f"\n[{direction} / {era}]")
            print(f"  peak at N_std={stats['peak_N_std']}, value={stats['peak_disc']:+.1f} pp")
            print(f"  decay at peak+0.5: {stats['decay_ratio_at_peak_plus_0.5']:.3f}")
            print(f"  Spearman rho(N_std, disc): {stats['spearman_rho_Nstd_vs_disc']:+.3f}")
            print(f"  sign-changes in disc curve: {stats['sign_changes_count']}")

    print("\n" + "=" * 70)
    print("PRE-COMMITTED VERDICTS (HA07d bidirectional primary, both eras)")
    print("=" * 70)
    verdicts = {}
    for era in ["train", "validate"]:
        stats = shape_results["bidirectional"][era]
        disc_2_0 = table["bidirectional"][era][2.0].get("disc_pp", 0)
        disc_2_5 = table["bidirectional"][era][2.5].get("disc_pp", 0)
        verdict = apply_verdict_criteria(stats, disc_2_0, disc_2_5)
        verdicts[era] = verdict
        print(f"\n{era.upper()} 4d bidirectional: {verdict}")
        print(f"  peak N_std: {stats['peak_N_std']}")
        print(f"  disc at N_std=2.0: {disc_2_0:+.1f} pp")
        print(f"  disc at N_std=2.5: {disc_2_5:+.1f} pp")
        print(f"  Spearman rho: {stats['spearman_rho_Nstd_vs_disc']:+.3f}")
        print(f"  sign-changes: {stats['sign_changes_count']}")

    print("\n" + "=" * 70)
    print("ASCII DISCRIMINATION CURVES")
    print("=" * 70)
    for direction in ["bidirectional", "one_sided_elevated", "one_sided_lowered"]:
        for era in ["train", "validate"]:
            disc_by_N_std = {N_std: table[direction][era][N_std].get("disc_pp", 0) for N_std in N_STD_GRID}
            print(ascii_curve(disc_by_N_std, f"{direction} / {era}"))

    out = {
        "table": {
            direction: {era: {str(N_std): r for N_std, r in inner.items()}
                       for era, inner in d_table.items()}
            for direction, d_table in table.items()
        },
        "shape_stats": shape_results,
        "primary_verdicts": verdicts,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
