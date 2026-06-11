"""HA01c v2 threshold-monotonicity diagnostic.

Pre-registered 2026-06-07 in diagnostic.md per the user-locked
Option A testing playbook section 9 compliance bar. Co-locked with
HA01c. Tests how HA01c's discrimination curve behaves across a
fine grid of rank thresholds, per the locked five-category shape
rule (adapted for rank thresholds, not N_std).

Threshold grid (locked per diagnostic.md section 4.1):
  tau in {0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95}

Locked five-category rank-adapted criteria (per diagnostic.md section
4.4):
- Cat 1 canonical decline: peak in [0.50, 0.70], monotone decline
  beyond peak, peak_disc >= +7 pp at any threshold >= 0.75
- Cat 2 stable plateau: disc(tau) ranges over <= 5 pp across
  meaningful range, all values >= +5 pp
- Cat 3 rising / late-peak: peak at tau >= 0.80, monotone rise to
  peak, peak_disc >= +15 pp, 0 sign-changes in [0.60, 0.90]
- Cat 4 bumpy with sign-changes: >= 1 sign-change in [0.60, 0.90]
- Cat 5 loose-tail noise: peak_disc < +5 pp

Cat 1, 2, 3 -> RESCUE (HA01c locked verdict stands load-bearing).
Cat 4, 5 -> CLOSE (HA01c locked verdict honest at locked tau but
not load-bearing without further work).

Output:
- result-data.json: 8-threshold x 2-era discrimination table + shape
                    categorisation per era + sign-change count +
                    peak tau + peak_disc + cat 1-5 evaluations
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

ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
LEADUP_DAYS = 4
NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

AXIS_COL = "effective_exertion_rank_lagged"

# Locked threshold grid per diagnostic.md section 4.1
THRESHOLDS = [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]

# Locked meaningful range for sign-changes per diagnostic.md section 4.3
SIGN_CHANGE_MIN_TAU = 0.60
SIGN_CHANGE_MAX_TAU = 0.90

# Locked rank-adapted bounds per diagnostic.md section 4.4
CAT1_PEAK_MIN = 0.50
CAT1_PEAK_MAX = 0.70
CAT3_PEAK_MIN = 0.80


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
    """4-day lead-up max-rank for effective_exertion_rank_lagged."""
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
    return {"ranks": ranks, "max_rank": max(ranks), "n_valid": len(ranks)}


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


def discrimination_at_threshold(event_windows: list[dict],
                                 null_windows: list[dict],
                                 tau: float) -> float:
    """Discrimination pp at threshold tau."""
    if not event_windows or not null_windows:
        return 0.0
    frac_event = sum(1 for w in event_windows if w["max_rank"] >= tau) / len(event_windows)
    frac_null = sum(1 for w in null_windows if w["max_rank"] >= tau) / len(null_windows)
    return (frac_event - frac_null) * 100


def compute_shape_stats(disc_by_tau: dict[float, float]) -> dict:
    """Compute shape stats for the rank-threshold sweep.

    Sign-changes counted only in [SIGN_CHANGE_MIN_TAU, SIGN_CHANGE_MAX_TAU]
    per diagnostic.md section 4.3.
    Peak / peak_disc / spearman computed over full grid (all 8 thresholds).
    """
    items = sorted(disc_by_tau.items())
    taus = [t for t, _ in items]
    discs = [d for _, d in items]

    peak_idx = max(range(len(discs)), key=lambda i: discs[i])
    peak_tau = taus[peak_idx]
    peak_disc = discs[peak_idx]
    max_neg_disc = min(discs)

    # Sign-changes in the meaningful sign-change range
    sign_changes = 0
    prev_sign = None
    for t, d in items:
        if not (SIGN_CHANGE_MIN_TAU <= t <= SIGN_CHANGE_MAX_TAU):
            continue
        if d > 0:
            sign = 1
        elif d < 0:
            sign = -1
        else:
            continue
        if prev_sign is not None and sign != prev_sign:
            sign_changes += 1
        prev_sign = sign

    # Direction reversals (descriptive only)
    direction_reversals = 0
    slopes = [discs[i + 1] - discs[i] for i in range(len(discs) - 1)]
    prev_slope_sign = None
    for s in slopes:
        if s > 0:
            sign = 1
        elif s < 0:
            sign = -1
        else:
            continue
        if prev_slope_sign is not None and sign != prev_slope_sign:
            direction_reversals += 1
        prev_slope_sign = sign

    # Spearman rank correlation
    def rank(vs):
        srt = sorted(enumerate(vs), key=lambda kv: kv[1])
        ranks = [0.0] * len(vs)
        i = 0
        while i < len(srt):
            j = i
            while j + 1 < len(srt) and srt[j + 1][1] == srt[i][1]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                ranks[srt[k][0]] = avg
            i = j + 1
        return ranks
    rx, ry = rank(taus), rank(discs)
    n = len(rx)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    denx = (sum((rx[i] - mx) ** 2 for i in range(n))) ** 0.5
    deny = (sum((ry[i] - my) ** 2 for i in range(n))) ** 0.5
    rho = num / (denx * deny) if denx and deny else 0.0

    return {
        "n_thresholds": len(items),
        "peak_tau": peak_tau,
        "peak_disc": peak_disc,
        "sign_changes_in_meaningful_range": sign_changes,
        "direction_reversals_full_grid": direction_reversals,
        "spearman_rho": rho,
        "max_neg_disc": max_neg_disc,
    }


def evaluate_cat1(disc_by_tau: dict[float, float], stats: dict) -> tuple[bool, str]:
    """Cat 1 canonical decline: peak in [0.50, 0.70], monotone decline beyond,
    peak_disc >= +7 pp at any threshold >= 0.75."""
    peak_tau = stats["peak_tau"]
    items = sorted(disc_by_tau.items())
    cond_peak = CAT1_PEAK_MIN <= peak_tau <= CAT1_PEAK_MAX
    # Monotone decline beyond peak
    beyond_peak = [(t, d) for t, d in items if t > peak_tau]
    cond_monotone = all(
        beyond_peak[i + 1][1] <= beyond_peak[i][1]
        for i in range(len(beyond_peak) - 1)
    ) if len(beyond_peak) > 1 else True
    # peak_disc >= +7 pp at any tau >= 0.75
    above_075 = [d for t, d in items if t >= 0.75]
    cond_disc_floor = any(d >= 7 for d in above_075) if above_075 else False
    cond_signs = stats["sign_changes_in_meaningful_range"] <= 1
    passed = all([cond_peak, cond_monotone, cond_disc_floor, cond_signs])
    detail = (
        f"peak={peak_tau} in [{CAT1_PEAK_MIN},{CAT1_PEAK_MAX}]={cond_peak}; "
        f"monotone_beyond_peak={cond_monotone}; "
        f"any_disc>=+7@tau>=0.75={cond_disc_floor}; "
        f"signs<=1={cond_signs}"
    )
    return passed, detail


def evaluate_cat2(disc_by_tau: dict[float, float], stats: dict) -> tuple[bool, str]:
    """Cat 2 stable plateau: disc range <= 5 pp across meaningful range,
    all >= +5 pp."""
    items = sorted(disc_by_tau.items())
    discs = [d for _, d in items]
    if not discs:
        return False, "no thresholds"
    plateau_max = max(discs)
    plateau_min = min(discs)
    plateau_range = plateau_max - plateau_min
    cond_range = plateau_range <= 5
    cond_all_positive = all(d >= 5 for d in discs)
    cond_signs = stats["sign_changes_in_meaningful_range"] == 0
    passed = all([cond_range, cond_all_positive, cond_signs])
    detail = (
        f"plateau_range={plateau_range:.1f}<=5={cond_range}; "
        f"all_disc>=+5={cond_all_positive}; "
        f"signs==0={cond_signs}"
    )
    return passed, detail


def evaluate_cat3(disc_by_tau: dict[float, float], stats: dict) -> tuple[bool, str]:
    """Cat 3 rising / late-peak: peak at tau >= 0.80, monotone rise to peak,
    peak_disc >= +15 pp, 0 sign-changes in [0.60, 0.90]."""
    peak_tau = stats["peak_tau"]
    peak_disc = stats["peak_disc"]
    items = sorted(disc_by_tau.items())
    cond_peak = peak_tau >= CAT3_PEAK_MIN
    cond_peak_disc = peak_disc >= 15
    # Monotone rise to peak
    rise = [(t, d) for t, d in items if t <= peak_tau]
    cond_monotone = all(
        rise[i + 1][1] >= rise[i][1]
        for i in range(len(rise) - 1)
    ) if len(rise) > 1 else True
    cond_signs = stats["sign_changes_in_meaningful_range"] == 0
    passed = all([cond_peak, cond_peak_disc, cond_monotone, cond_signs])
    detail = (
        f"peak={peak_tau}>={CAT3_PEAK_MIN}={cond_peak}; "
        f"peak_disc={peak_disc:.1f}>=+15={cond_peak_disc}; "
        f"monotone_rise_to_peak={cond_monotone}; "
        f"signs==0={cond_signs}"
    )
    return passed, detail


def evaluate_cat4(disc_by_tau: dict[float, float], stats: dict) -> tuple[bool, str]:
    """Cat 4 bumpy with sign-changes: >= 1 sign-change in [0.60, 0.90]."""
    cond_signs = stats["sign_changes_in_meaningful_range"] >= 1
    passed = cond_signs
    detail = f"signs={stats['sign_changes_in_meaningful_range']}>=1={cond_signs}"
    return passed, detail


def evaluate_cat5(disc_by_tau: dict[float, float], stats: dict) -> tuple[bool, str]:
    """Cat 5 loose-tail noise: peak_disc < +5 pp."""
    cond = stats["peak_disc"] < 5
    detail = f"peak_disc={stats['peak_disc']:.1f}<+5={cond}"
    return cond, detail


def apply_v2_verdict(disc_by_tau: dict[float, float], stats: dict) -> dict:
    """Apply the locked five-category rule. Cat 1/2/3 -> RESCUE; Cat 4/5 -> CLOSE."""
    cat1_pass, cat1_detail = evaluate_cat1(disc_by_tau, stats)
    cat2_pass, cat2_detail = evaluate_cat2(disc_by_tau, stats)
    cat3_pass, cat3_detail = evaluate_cat3(disc_by_tau, stats)
    cat4_pass, cat4_detail = evaluate_cat4(disc_by_tau, stats)
    cat5_pass, cat5_detail = evaluate_cat5(disc_by_tau, stats)

    rescue_cats = []
    if cat1_pass: rescue_cats.append("Cat 1")
    if cat2_pass: rescue_cats.append("Cat 2")
    if cat3_pass: rescue_cats.append("Cat 3")
    close_cats = []
    if cat4_pass: close_cats.append("Cat 4")
    if cat5_pass: close_cats.append("Cat 5")

    if rescue_cats:
        verdict = "RESCUE"
        reason = f"via {', '.join(rescue_cats)}"
    elif close_cats:
        verdict = "CLOSE"
        reason = f"via {', '.join(close_cats)}"
    else:
        verdict = "AMBIGUOUS"
        reason = "no category triggered (unexpected; review shape)"

    return {
        "verdict": verdict,
        "reason": reason,
        "rescue_categories": rescue_cats,
        "close_categories": close_cats,
        "cat1": {"pass": cat1_pass, "detail": cat1_detail},
        "cat2": {"pass": cat2_pass, "detail": cat2_detail},
        "cat3": {"pass": cat3_pass, "detail": cat3_detail},
        "cat4": {"pass": cat4_pass, "detail": cat4_detail},
        "cat5": {"pass": cat5_pass, "detail": cat5_detail},
    }


def evaluate_era(events: list[date], nulls: list[date],
                 features: dict[date, dict], era_label: str) -> dict:
    event_windows = []
    for d in events:
        w = axis_window(d, features)
        if w is not None:
            event_windows.append(w)
    null_windows = []
    for d in nulls:
        w = axis_window(d, features)
        if w is not None:
            null_windows.append(w)

    disc_by_tau = {}
    freq_by_tau = {}
    for tau in THRESHOLDS:
        disc = discrimination_at_threshold(event_windows, null_windows, tau)
        disc_by_tau[tau] = disc
        freq_by_tau[tau] = sum(
            1 for w in event_windows if w["max_rank"] >= tau
        ) / max(1, len(event_windows))

    stats = compute_shape_stats(disc_by_tau)
    v2_verdict = apply_v2_verdict(disc_by_tau, stats)

    return {
        "era": era_label,
        "n_clean": len(event_windows),
        "n_null": len(null_windows),
        "disc_by_tau": disc_by_tau,
        "freq_by_tau": freq_by_tau,
        "shape_stats": stats,
        "v2_verdict": v2_verdict,
    }


def dry_run_print(train: list[date], validate: list[date],
                  features: dict[date, dict]) -> dict:
    samples = []
    print("\n=== Dry-run gate (per playbook section 2.3) ===")
    print("\nPer-episode max_rank across 4-day lead-up; trigger at each threshold.")
    for label, events in [("TRAIN", train[:3]), ("VALIDATE", validate[:3])]:
        print(f"\n--- {label} (first 3 crash starts) ---")
        for ref in events:
            w = axis_window(ref, features)
            if w is None:
                print(f"  {ref.isoformat()}: NA (insufficient lagged-rank data)")
                continue
            max_rank = w["max_rank"]
            triggers = " ".join(
                f"{tau:.2f}={'1' if max_rank >= tau else '0'}"
                for tau in THRESHOLDS
            )
            print(f"  {ref.isoformat()}: max_rank={max_rank:.3f}  {triggers}")
            samples.append({"era": label.lower(), "ref": ref.isoformat(),
                           "max_rank": max_rank})
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
        print("\n--dry-run-only flag set; not running full v2 sweep.")
        return

    train_result = evaluate_era(train, nulls, features, "train")
    validate_result = evaluate_era(validate, nulls, features, "validate")

    out = {
        "diagnostic": "HA01c-v2-threshold-monotonicity",
        "pre_registered": "2026-06-07 in diagnostic.md",
        "config": {
            "analysis_start": ANALYSIS_START.isoformat(),
            "train_end": TRAIN_END.isoformat(),
            "validate_end": VALIDATE_END.isoformat(),
            "leadup_days": LEADUP_DAYS,
            "null_sample_size": NULL_SAMPLE_SIZE,
            "random_seed": RANDOM_SEED,
            "axis_col": AXIS_COL,
            "thresholds": THRESHOLDS,
            "sign_change_range": [SIGN_CHANGE_MIN_TAU, SIGN_CHANGE_MAX_TAU],
            "cat1_peak_range": [CAT1_PEAK_MIN, CAT1_PEAK_MAX],
            "cat3_peak_min": CAT3_PEAK_MIN,
        },
        "train_result": train_result,
        "validate_result": validate_result,
        "dry_run": dry_run_data,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")

    print("\n=== Discrimination curves ===")
    for label, r in [("TRAIN", train_result), ("VALIDATE", validate_result)]:
        print(f"\n{label} (n_clean={r['n_clean']}, n_null={r['n_null']}):")
        print(f"  {'tau':>6} {'disc_pp':>10} {'freq_event':>11}")
        for tau in THRESHOLDS:
            print(f"  {tau:>6.2f} {r['disc_by_tau'][tau]:>+9.1f}  {r['freq_by_tau'][tau]*100:>10.1f}%")
        s = r["shape_stats"]
        print(f"  Shape: peak_tau={s['peak_tau']}, peak_disc={s['peak_disc']:+.1f} pp, "
              f"sign_changes_in_[{SIGN_CHANGE_MIN_TAU},{SIGN_CHANGE_MAX_TAU}]={s['sign_changes_in_meaningful_range']}, "
              f"rho={s['spearman_rho']:+.3f}, max_neg={s['max_neg_disc']:+.1f}")

    print("\n=== v2 verdicts per era ===")
    for label, r in [("TRAIN", train_result), ("VALIDATE", validate_result)]:
        v = r["v2_verdict"]
        print(f"  {label:10} {v['verdict']:10} {v['reason']}")
        for cat in ["cat1", "cat2", "cat3", "cat4", "cat5"]:
            marker = "PASS" if v[cat]["pass"] else "    "
            print(f"             {cat.upper()}: {marker}  {v[cat]['detail']}")

    print(f"\nWrote {OUT_JSON}")

    train_v = train_result["v2_verdict"]["verdict"]
    val_v = validate_result["v2_verdict"]["verdict"]
    print(f"\n=== Overall (both-eras) framing ===")
    print(f"  train v2: {train_v}; validate v2: {val_v}")
    if train_v == "RESCUE" and val_v == "RESCUE":
        print("  HA01c locked verdict graduates to LOAD-BEARING under v2.")
    elif train_v == "CLOSE" and val_v == "CLOSE":
        print("  HA01c locked verdict stays REFUTED-ON-STABILITY both eras.")
    else:
        print("  Mixed v2 verdict; HA01c stays SUPPORTED-with-stability-mixed (both-eras rule blocks load-bearing).")


if __name__ == "__main__":
    dry = "--dry-run-only" in sys.argv
    main(dry_run_only=dry)
