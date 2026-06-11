"""HA10 threshold-monotonicity diagnostic.

Re-runs HA10's locked test machinery across a 13-tier fine N_std
grid and computes shape statistics per the locked diagnostic.md.

Outputs:
  result-data.json     full table for downstream analysis
  ASCII curve printed  for quick shape inspection

Usage:
  python test.py
"""
from __future__ import annotations

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

LAGGED_WINDOW_START_DAYS = 30
LAGGED_WINDOW_END_DAYS = 90
MIN_LAGGED_DAYS = 40
TRIMMED_PCT = 0.10
MIN_BASELINE_STD = 2.0

LEADUP_PRIMARY = 4
MIN_LEADUP_VALID_PRIMARY = 3

MORNING_START = time(3, 0)
MORNING_END = time(10, 0)
BB_MIN_VALID = 0
BB_MAX_VALID = 100

NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15

# THE diagnostic grid - 13 tiers
N_STD_GRID = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5, 4.0]

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABELS_CSV = ROOT / "crash_v2-definition" / "labels_crash_v2.csv"
GARMIN_UDS_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Aggregator"
)
OUT_JSON = HERE / "result-data.json"


def parse_anchor_ts(s: str) -> datetime | None:
    try:
        return datetime.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def load_morning_peak_by_date() -> dict[date, int]:
    out: dict[date, int] = {}
    for p in sorted(GARMIN_UDS_DIR.glob("UDSFile_*.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            bb = rec.get("bodyBattery")
            if not cd or not bb:
                continue
            stat_list = bb.get("bodyBatteryStatList", [])
            highest = next(
                (s for s in stat_list if s.get("bodyBatteryStatType") == "HIGHEST"),
                None,
            )
            if not highest:
                continue
            ts = parse_anchor_ts(highest.get("statTimestamp", ""))
            if ts is None:
                continue
            if not (MORNING_START <= ts.time() < MORNING_END):
                continue
            val = highest.get("statsValue")
            try:
                v = int(val)
            except (TypeError, ValueError):
                continue
            if v < BB_MIN_VALID or v > BB_MAX_VALID:
                continue
            d = date.fromisoformat(cd)
            if d in out and v <= out[d]:
                continue
            out[d] = v
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


def trimmed_list(values, pct):
    if not values:
        return []
    vs = sorted(values)
    n = len(vs)
    trim = int(n * pct)
    if n - 2 * trim < 1:
        return vs
    return vs[trim : n - trim]


def compute_baseline(d, peak_by_date):
    prior = []
    for i in range(LAGGED_WINDOW_START_DAYS + 1, LAGGED_WINDOW_END_DAYS + 1):
        wd = d - timedelta(days=i)
        if wd in peak_by_date:
            prior.append(float(peak_by_date[wd]))
    if len(prior) < MIN_LAGGED_DAYS:
        return None, None
    trimmed = trimmed_list(prior, TRIMMED_PCT)
    if len(trimmed) < 2:
        return None, None
    mu = statistics.mean(trimmed)
    sigma = statistics.stdev(trimmed)
    if sigma < MIN_BASELINE_STD:
        return None, None
    return mu, sigma


def per_day_z(d, peak_by_date):
    if d not in peak_by_date:
        return None
    mu, sigma = compute_baseline(d, peak_by_date)
    if mu is None or sigma is None:
        return None
    return (float(peak_by_date[d]) - mu) / sigma


def episode_profile(ref, peak_by_date, leadup_days, min_valid):
    signed = []
    for i in range(1, leadup_days + 1):
        wd = ref - timedelta(days=i)
        z = per_day_z(wd, peak_by_date)
        if z is not None:
            signed.append(z)
    if len(signed) < min_valid:
        return None
    return {
        "max_abs_z": max(abs(s) for s in signed),
        "max_signed_z": max(signed),
        "min_signed_z": min(signed),
    }


def build_null_sample(peak_by_date, crash_starts, leadup_days, min_valid):
    rng = random.Random(RANDOM_SEED)
    occupied = set()
    for ref in crash_starts:
        for i in range(1, leadup_days + 1):
            occupied.add(ref - timedelta(days=i))
    all_dates = sorted(
        d for d in peak_by_date if ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END
    )
    out, attempts = [], 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 10000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, leadup_days + 1)}
        if leadup & occupied:
            continue
        prof = episode_profile(ref, peak_by_date, leadup_days, min_valid)
        if prof is None:
            continue
        out.append(prof)
    return out


def trigger(e, N_std, mode):
    if mode == "bidirectional":
        return e["max_abs_z"] >= N_std
    if mode == "one_sided_elevated":
        return e["max_signed_z"] >= N_std
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
    a = fe >= CRIT_A_FRAC
    b = disc >= CRIT_B_DISC_PP
    c = median >= N_std / 2
    return {
        "verdict": "supported" if (a and b and c) else "refuted",
        "freq": fe,
        "null_freq": fn,
        "disc_pp": disc,
        "median": median,
        "crit_a": a,
        "crit_b": b,
        "crit_c": c,
    }


def spearman_rho(xs, ys):
    """Spearman rank correlation."""
    n = len(xs)
    def rank(vs):
        sorted_idx = sorted(range(len(vs)), key=lambda i: vs[i])
        ranks = [0.0] * len(vs)
        i = 0
        while i < len(vs):
            j = i
            while j + 1 < len(vs) and vs[sorted_idx[j + 1]] == vs[sorted_idx[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[sorted_idx[k]] = avg
            i = j + 1
        return ranks
    rx, ry = rank(xs), rank(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    denx = (sum((rx[i] - mx) ** 2 for i in range(n))) ** 0.5
    deny = (sum((ry[i] - my) ** 2 for i in range(n))) ** 0.5
    return num / (denx * deny) if denx and deny else 0.0


def count_sign_changes(values):
    """Count number of sign changes in a sequence."""
    count = 0
    prev_sign = None
    for v in values:
        if v > 0:
            sign = 1
        elif v < 0:
            sign = -1
        else:
            continue
        if prev_sign is not None and sign != prev_sign:
            count += 1
        prev_sign = sign
    return count


def compute_shape_stats(disc_by_N_std):
    """Compute shape statistics for one (era, direction) pair."""
    grid = sorted(disc_by_N_std.keys())
    discs = [disc_by_N_std[n] for n in grid]
    peak_idx = max(range(len(discs)), key=lambda i: discs[i])
    peak_N_std = grid[peak_idx]
    peak_disc = discs[peak_idx]
    # decay from peak: ratio of disc at peak+0.5 to peak
    target = peak_N_std + 0.5
    target_idx = min(range(len(grid)), key=lambda i: abs(grid[i] - target))
    decay_ratio = discs[target_idx] / peak_disc if peak_disc != 0 else float("nan")
    rho = spearman_rho(grid, discs)
    signs = count_sign_changes(discs)
    return {
        "peak_N_std": peak_N_std,
        "peak_disc": peak_disc,
        "decay_ratio_at_peak_plus_0.5": decay_ratio,
        "spearman_rho_Nstd_vs_disc": rho,
        "sign_changes_count": signs,
    }


def ascii_curve(disc_by_N_std, label, width=60):
    grid = sorted(disc_by_N_std.keys())
    discs = [disc_by_N_std[n] for n in grid]
    lo = min(min(discs), -20)
    hi = max(max(discs), 30)
    def pos(v):
        return int((v - lo) / (hi - lo) * (width - 1))
    zero_pos = pos(0)
    lines = [f"\n{label}:"]
    lines.append(f"  {'N_std':>6}  {'disc pp':>8}  " + " " * zero_pos + "|" + " " * (width - zero_pos - 1) + "  ")
    for n, d in zip(grid, discs):
        bar = [" "] * width
        bar[zero_pos] = "|"
        p = pos(d)
        if p >= zero_pos:
            for i in range(zero_pos, p + 1):
                bar[i] = "#"
        else:
            for i in range(p, zero_pos + 1):
                bar[i] = "#"
        lines.append(f"  {n:>6.2f}  {d:>+7.1f}  " + "".join(bar))
    return "\n".join(lines)


def apply_verdict_criteria(stats, disc_2_0, disc_2_5):
    """Apply the locked rescue/close/ambiguous criteria from diagnostic.md."""
    rescue = (
        1.0 <= stats["peak_N_std"] <= 1.5
        and disc_2_0 >= 10.0
        and disc_2_5 >= 5.0
        and stats["spearman_rho_Nstd_vs_disc"] <= -0.3
        and stats["sign_changes_count"] <= 1
    )
    close = (
        stats["peak_N_std"] > 1.5 or stats["peak_N_std"] < 0.75
        or disc_2_0 < 5.0
        or disc_2_5 < 0.0
        or stats["spearman_rho_Nstd_vs_disc"] > -0.1
        or stats["sign_changes_count"] >= 2
    )
    if rescue and not close:
        return "RESCUE"
    elif close:
        return "CLOSE"
    else:
        return "AMBIGUOUS"


def main():
    print("Loading morning BB peak (same as HA10)...")
    peak_by_date = load_morning_peak_by_date()
    print(f"  {len(peak_by_date)} valid days")
    crashes = load_crashes()
    train = [c for c in crashes if c <= TRAIN_END]
    val = [c for c in crashes if c > TRAIN_END]
    print(f"  {len(crashes)} crashes; train {len(train)} validate {len(val)}")

    train_events = [e for e in (episode_profile(c, peak_by_date, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY) for c in train) if e]
    val_events = [e for e in (episode_profile(c, peak_by_date, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY) for c in val) if e]
    null = build_null_sample(peak_by_date, crashes, LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
    print(f"  train_events: {len(train_events)}, val_events: {len(val_events)}, null: {len(null)}")
    print()

    # Build full table
    table = {}
    for direction in ["bidirectional", "one_sided_elevated", "one_sided_lowered"]:
        table[direction] = {}
        for era, events in [("train", train_events), ("validate", val_events)]:
            table[direction][era] = {}
            for N_std in N_STD_GRID:
                r = evaluate(events, null, N_std, direction)
                table[direction][era][N_std] = r

    # Print combined per-direction-and-era curves
    print("=" * 70)
    print("FINE GRID DISCRIMINATION TABLE")
    print("=" * 70)
    for direction in ["bidirectional", "one_sided_elevated", "one_sided_lowered"]:
        print(f"\n--- {direction} ---")
        print(f"  {'N_std':>6}  {'train_disc':>10}  {'val_disc':>9}  "
              f"{'train_freq':>10}  {'val_freq':>9}  {'null_freq':>9}")
        for N_std in N_STD_GRID:
            t = table[direction]["train"][N_std]
            v = table[direction]["validate"][N_std]
            print(f"  {N_std:>6.2f}  "
                  f"{t.get('disc_pp', 0):>+9.1f}  "
                  f"{v.get('disc_pp', 0):>+8.1f}  "
                  f"{t.get('freq', 0) * 100:>9.1f}%  "
                  f"{v.get('freq', 0) * 100:>8.1f}%  "
                  f"{t.get('null_freq', 0) * 100:>8.1f}%")

    # Compute shape stats for each (era, direction)
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

    # Apply verdict to validate bidirectional primary (HA10's headline)
    print("\n" + "=" * 70)
    print("PRE-COMMITTED VERDICT")
    print("=" * 70)
    val_bidir_stats = shape_results["bidirectional"]["validate"]
    disc_2_0 = table["bidirectional"]["validate"][2.0].get("disc_pp", 0)
    disc_2_5 = table["bidirectional"]["validate"][2.5].get("disc_pp", 0)
    verdict = apply_verdict_criteria(val_bidir_stats, disc_2_0, disc_2_5)
    print(f"\nValidate 4d bidirectional (HA10's primary): {verdict}")
    print(f"  peak N_std: {val_bidir_stats['peak_N_std']}")
    print(f"  disc at N_std=2.0: {disc_2_0:+.1f} pp")
    print(f"  disc at N_std=2.5: {disc_2_5:+.1f} pp")
    print(f"  Spearman rho: {val_bidir_stats['spearman_rho_Nstd_vs_disc']:+.3f}")
    print(f"  sign-changes: {val_bidir_stats['sign_changes_count']}")

    # ASCII curves
    print("\n" + "=" * 70)
    print("ASCII DISCRIMINATION CURVES")
    print("=" * 70)
    for direction in ["bidirectional", "one_sided_elevated", "one_sided_lowered"]:
        for era in ["train", "validate"]:
            disc_by_N_std = {N_std: table[direction][era][N_std].get("disc_pp", 0) for N_std in N_STD_GRID}
            print(ascii_curve(disc_by_N_std, f"{direction} / {era}"))

    # Save
    out = {
        "table": {
            direction: {
                era: {str(N_std): r for N_std, r in inner.items()}
                for era, inner in d_table.items()
            }
            for direction, d_table in table.items()
        },
        "shape_stats": shape_results,
        "primary_verdict": verdict,
        "primary_verdict_inputs": {
            "peak_N_std": val_bidir_stats["peak_N_std"],
            "peak_disc": val_bidir_stats["peak_disc"],
            "disc_at_2_0": disc_2_0,
            "disc_at_2_5": disc_2_5,
            "spearman_rho": val_bidir_stats["spearman_rho_Nstd_vs_disc"],
            "sign_changes": val_bidir_stats["sign_changes_count"],
        },
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
