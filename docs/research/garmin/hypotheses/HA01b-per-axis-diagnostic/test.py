"""HA01b per-axis decomposition diagnostic.

Pre-registered 2026-06-07 in diagnostic.md per the user-locked Option A
testing-playbook compliance bar (playbook section 9 checklist).

What this script does
---------------------
Tests each of the 4 axes that compose HA01b's `exertion_class` composite
(MAX percentile rank across 4 input axes), asking: "If HA01b had been
pre-registered on each individual axis as primary (rather than on the
composite), would any single axis have produced a SUPPORTED verdict
under the same locked bar?"

Diagnostic.md naming -> CSV column name mapping
-----------------------------------------------
Per playbook section 2.5 (audit-trail preservation), the diagnostic.md
uses descriptive labels; the actual CSV columns (computed by
11_compute_lagged_baseline.py) use slightly shorter names. The
physical quantities are identical:

  diagnostic.md label             | actual CSV column
  --------------------------------|--------------------------------
  effective_exertion_min_rank_lag | effective_exertion_rank_lagged
  step_burden_rank_lagged         | step_rank_lagged
  max_hr_peak_rank_lagged         | max_hr_rank_lagged
  vigorous_min_rank_lagged        | vigorous_min_rank_lagged

This script uses the actual column names; result.md documents the
mapping for any reader cross-referencing diagnostic.md.

Locked bar (matches HA01b composite bar)
----------------------------------------
- crit (a) frequency >= 60% of crash episodes trigger
- crit (b) discrimination >= +15 pp above null
- crit (c) median rank on triggering episodes >= 0.875
            (halfway from 0.75 threshold to 1.0)

Per-axis trigger
----------------
  A_rank_lagged >= 0.75 for at least 1 day in the 4-day lead-up window
  [C-4, C-3, C-2, C-1]. Mirrors HA01b composite "heavy+" threshold.

Output
------
- result-data.json: per-axis discrimination table (4 axes x 2 eras),
                    composite control verdict, cross-axis correlation
                    matrix, dry-run sample.
- stdout dry-run gate output (3 train + 3 validate episodes' per-axis
  per-day ranks) BEFORE the full evaluation runs.
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

# Locked per diagnostic.md and playbook section 4
ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
LEADUP_DAYS = 4
NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

# Locked 3-criterion bar (matches HA01b composite)
CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15
CRIT_C_MEDIAN_RANK_MIN = 0.875

# Per-axis trigger threshold (matches "heavy+" rank threshold)
AXIS_RANK_THRESHOLD = 0.75

# Locked axis set (4 per-axis components of HA01b's composite)
# Order matters for output stability.
AXES = [
    ("effective_exertion", "effective_exertion_rank_lagged"),
    ("step_burden",        "step_rank_lagged"),
    ("max_hr_peak",        "max_hr_rank_lagged"),
    ("vigorous_min",       "vigorous_min_rank_lagged"),
]

# Composite control column (HA01b's actual composite, lagged)
COMPOSITE_CLASS_COL = "exertion_class_lagged"
SHOCK_CLASSES = {"heavy", "very_heavy"}


def load_features() -> dict[date, dict]:
    out = {}
    for r in csv.DictReader(FEATURES_CSV.open(encoding="utf-8")):
        out[date.fromisoformat(r["date"])] = r
    return out


def load_crashes_v1() -> list[date]:
    """crash_v1 episode starts (one date per episode_id)."""
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


def axis_window(ref: date, features: dict[date, dict], col: str) -> dict | None:
    """Per-axis lead-up window stats.

    Returns dict with:
      ranks      : list of valid rank values across lead-up days
      max_rank   : max valid rank in the window (or None if no valid days)
      n_valid    : number of valid lead-up days
      triggers   : whether any lead-up day has rank >= AXIS_RANK_THRESHOLD
    Returns None if validity < 3 of 4 days (matches HA01b validity rule).
    """
    leadup_days = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    ranks = []
    for d in leadup_days:
        r = features.get(d)
        if not r:
            continue
        rv = parse_float(r.get(col))
        if rv is None:
            continue
        ranks.append(rv)
    if len(ranks) < 3:
        return None
    max_rank = max(ranks)
    return {
        "ranks": ranks,
        "max_rank": max_rank,
        "n_valid": len(ranks),
        "triggers": max_rank >= AXIS_RANK_THRESHOLD,
    }


def composite_window(ref: date, features: dict[date, dict]) -> dict | None:
    """Composite control: HA01b's exertion_class_lagged in the same window."""
    leadup_days = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    valid_classes = []
    for d in leadup_days:
        r = features.get(d)
        if r and r.get(COMPOSITE_CLASS_COL):
            valid_classes.append(r[COMPOSITE_CLASS_COL])
    if len(valid_classes) < 2:
        return None
    n_shock = sum(1 for c in valid_classes if c in SHOCK_CLASSES)
    return {"n_shock_days": n_shock, "has_shock": n_shock >= 1}


def build_null_sample(features: dict[date, dict], crash_starts: list[date]) -> list[date]:
    """Build N=200 non-overlapping 4-day null windows; seed 20260605."""
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


def evaluate_axis(
    axis_label: str,
    axis_col: str,
    events: list[date],
    nulls: list[date],
    features: dict[date, dict],
    era_label: str,
) -> dict:
    """Per-axis SUPPORTED/REFUTED at the locked 3-criterion bar."""
    event_windows = []
    for d in events:
        w = axis_window(d, features, axis_col)
        if w is not None:
            event_windows.append(w)

    null_windows = []
    for d in nulls:
        w = axis_window(d, features, axis_col)
        if w is not None:
            null_windows.append(w)

    if len(event_windows) < 10:
        return {
            "axis": axis_label, "axis_col": axis_col, "era": era_label,
            "verdict": "inconclusive",
            "n_clean": len(event_windows),
            "reason": f"n_clean={len(event_windows)} < 10",
        }

    frac_event = sum(1 for w in event_windows if w["triggers"]) / len(event_windows)
    frac_null = sum(1 for w in null_windows if w["triggers"]) / len(null_windows)
    disc_pp = (frac_event - frac_null) * 100

    triggering_max_ranks = [w["max_rank"] for w in event_windows if w["triggers"]]
    if triggering_max_ranks:
        median_rank = statistics.median(triggering_max_ranks)
        triggering_max_ranks_sorted = sorted(triggering_max_ranks)
        lq_rank = triggering_max_ranks_sorted[
            int(len(triggering_max_ranks_sorted) * 0.25)
        ]
    else:
        median_rank = 0.0
        lq_rank = 0.0

    a = frac_event >= CRIT_A_FRAC
    b = disc_pp >= CRIT_B_DISC_PP
    c = median_rank >= CRIT_C_MEDIAN_RANK_MIN

    return {
        "axis": axis_label,
        "axis_col": axis_col,
        "era": era_label,
        "n_clean": len(event_windows),
        "n_null": len(null_windows),
        "frac_event_triggers": frac_event,
        "frac_null_triggers": frac_null,
        "discrimination_pp": disc_pp,
        "median_rank_on_triggering": median_rank,
        "lower_q_rank_on_triggering": lq_rank,
        "crit_a_pass": a,
        "crit_b_pass": b,
        "crit_c_pass": c,
        "verdict": "supported" if (a and b and c) else "refuted",
    }


def evaluate_composite_control(
    events: list[date],
    nulls: list[date],
    features: dict[date, dict],
    era_label: str,
) -> dict:
    event_windows = []
    for d in events:
        w = composite_window(d, features)
        if w is not None:
            event_windows.append(w)
    null_windows = []
    for d in nulls:
        w = composite_window(d, features)
        if w is not None:
            null_windows.append(w)
    if len(event_windows) < 10:
        return {
            "test": "composite_control",
            "era": era_label,
            "verdict": "inconclusive",
            "n_clean": len(event_windows),
        }
    frac_event = sum(1 for w in event_windows if w["has_shock"]) / len(event_windows)
    frac_null = sum(1 for w in null_windows if w["has_shock"]) / len(null_windows)
    disc_pp = (frac_event - frac_null) * 100
    shock_counts = sorted(w["n_shock_days"] for w in event_windows)
    median_count = statistics.median(shock_counts)
    a = frac_event >= CRIT_A_FRAC
    b = disc_pp >= CRIT_B_DISC_PP
    c = median_count >= 1
    return {
        "test": "composite_control",
        "era": era_label,
        "n_clean": len(event_windows),
        "n_null": len(null_windows),
        "frac_event_triggers": frac_event,
        "frac_null_triggers": frac_null,
        "discrimination_pp": disc_pp,
        "median_n_shock_days": median_count,
        "crit_a_pass": a, "crit_b_pass": b, "crit_c_pass": c,
        "verdict": "supported" if (a and b and c) else "refuted",
    }


def cross_axis_correlation(features: dict[date, dict]) -> dict:
    """Pearson + Spearman correlation matrix across the 4 axes.

    Computed over all valid days where ALL 4 axes have a value (pairwise
    complete on all 4). Per playbook section 6.1.
    """
    rows = []
    for d, r in features.items():
        if d < ANALYSIS_START or d > VALIDATE_END:
            continue
        vals = []
        ok = True
        for _, col in AXES:
            v = parse_float(r.get(col))
            if v is None:
                ok = False
                break
            vals.append(v)
        if ok:
            rows.append(vals)

    n_days = len(rows)
    if n_days < 30:
        return {
            "n_days": n_days,
            "error": "fewer than 30 fully-valid days; correlation matrix omitted",
        }

    n_axes = len(AXES)
    cols = [[row[j] for row in rows] for j in range(n_axes)]

    def pearson(x, y):
        mx = sum(x) / len(x)
        my = sum(y) / len(y)
        num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
        denx = (sum((xi - mx) ** 2 for xi in x)) ** 0.5
        deny = (sum((yi - my) ** 2 for yi in y)) ** 0.5
        if denx == 0 or deny == 0:
            return None
        return num / (denx * deny)

    def rank(values):
        """Average-rank for ties."""
        indexed = sorted(enumerate(values), key=lambda kv: kv[1])
        ranks = [0.0] * len(values)
        i = 0
        while i < len(indexed):
            j = i
            while j + 1 < len(indexed) and indexed[j + 1][1] == indexed[i][1]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                ranks[indexed[k][0]] = avg
            i = j + 1
        return ranks

    rank_cols = [rank(c) for c in cols]

    pearson_matrix = [[None] * n_axes for _ in range(n_axes)]
    spearman_matrix = [[None] * n_axes for _ in range(n_axes)]
    for i in range(n_axes):
        for j in range(n_axes):
            pearson_matrix[i][j] = pearson(cols[i], cols[j])
            spearman_matrix[i][j] = pearson(rank_cols[i], rank_cols[j])

    axis_labels = [a[0] for a in AXES]
    return {
        "n_days": n_days,
        "axis_labels": axis_labels,
        "pearson": pearson_matrix,
        "spearman": spearman_matrix,
    }


def dry_run_print(events_train: list[date], events_validate: list[date],
                  features: dict[date, dict]) -> dict:
    """Per playbook section 2.3: print first 3 train + 3 validate per-axis
    per-day rank values BEFORE the full run.

    Returns a dict for inclusion in result-data.json.
    """
    samples = []
    print("\n=== Dry-run gate (per playbook section 2.3) ===")
    for label, events in [("TRAIN", events_train[:3]), ("VALIDATE", events_validate[:3])]:
        print(f"\n--- {label} (first 3 crash starts) ---")
        for ref in events:
            print(f"\n  Crash start: {ref.isoformat()} (lead-up [{(ref - timedelta(days=4)).isoformat()} .. {(ref - timedelta(days=1)).isoformat()}])")
            episode_axes = {}
            for axis_label, axis_col in AXES:
                leadup_days = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
                day_ranks = []
                for d in leadup_days:
                    r = features.get(d)
                    rv = parse_float(r.get(axis_col)) if r else None
                    day_ranks.append((d.isoformat(), rv))
                day_str = " ".join(
                    f"{ds[5:]}={rv:.2f}" if rv is not None else f"{ds[5:]}=NA"
                    for ds, rv in day_ranks
                )
                triggers = any(rv is not None and rv >= AXIS_RANK_THRESHOLD
                               for _, rv in day_ranks)
                marker = "  [trigger]" if triggers else ""
                print(f"    {axis_label:22}: {day_str}{marker}")
                episode_axes[axis_label] = {
                    "days": day_ranks,
                    "triggers": triggers,
                }
            samples.append({
                "era": label.lower(),
                "ref": ref.isoformat(),
                "axes": episode_axes,
            })
    print()

    # Pathology checks per diagnostic.md section 5
    pathologies = []
    print("=== Pathology checks ===")
    for axis_label, axis_col in AXES:
        sample_vals = []
        for d, r in features.items():
            if d < ANALYSIS_START or d > VALIDATE_END:
                continue
            v = parse_float(r.get(axis_col))
            if v is not None:
                sample_vals.append(v)
        if not sample_vals:
            pathologies.append(f"{axis_label}: NO valid values in analysis window")
            print(f"  {axis_label:22}: NO VALID VALUES")
            continue
        n = len(sample_vals)
        n_zero = sum(1 for v in sample_vals if v == 0.0)
        n_one = sum(1 for v in sample_vals if v == 1.0)
        n_at_threshold = sum(1 for v in sample_vals if v >= AXIS_RANK_THRESHOLD)
        pct_at_threshold = 100.0 * n_at_threshold / n
        msg = (f"  {axis_label:22}: n={n}, range=[{min(sample_vals):.3f}, "
               f"{max(sample_vals):.3f}], all-zero={n_zero}, all-one={n_one}, "
               f">={AXIS_RANK_THRESHOLD}: {pct_at_threshold:.1f}%")
        print(msg)
        if n_zero / n > 0.5:
            pathologies.append(f"{axis_label}: >50% all-zero values")
        if n_one / n > 0.5:
            pathologies.append(f"{axis_label}: >50% all-one values")
    if pathologies:
        print("\nPATHOLOGIES DETECTED:")
        for p in pathologies:
            print(f"  - {p}")
    else:
        print("\nNo pathologies detected; full run safe to proceed.")
    print()

    return {"samples": samples, "pathologies": pathologies}


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

    if dry_run_data["pathologies"]:
        print("STOPPING: dry-run surfaced pathologies; review diagnostic.md before re-running.")
        sys.exit(1)

    if dry_run_only:
        print("\n--dry-run-only flag set; not running full diagnostic.")
        return

    per_axis_results = []
    for axis_label, axis_col in AXES:
        for era_label, events in [("train", train), ("validate", validate)]:
            res = evaluate_axis(axis_label, axis_col, events, nulls, features, era_label)
            per_axis_results.append(res)

    composite_results = [
        evaluate_composite_control(train, nulls, features, "train"),
        evaluate_composite_control(validate, nulls, features, "validate"),
    ]

    correlation_matrix = cross_axis_correlation(features)

    out = {
        "diagnostic": "HA01b-per-axis-decomposition",
        "pre_registered": "2026-06-07 in diagnostic.md (playbook section 9 compliance)",
        "config": {
            "analysis_start": ANALYSIS_START.isoformat(),
            "train_end": TRAIN_END.isoformat(),
            "validate_end": VALIDATE_END.isoformat(),
            "leadup_days": LEADUP_DAYS,
            "null_sample_size": NULL_SAMPLE_SIZE,
            "random_seed": RANDOM_SEED,
            "axis_rank_threshold": AXIS_RANK_THRESHOLD,
            "crit_a_frac": CRIT_A_FRAC,
            "crit_b_disc_pp": CRIT_B_DISC_PP,
            "crit_c_median_rank_min": CRIT_C_MEDIAN_RANK_MIN,
            "axes": [{"label": a[0], "csv_col": a[1]} for a in AXES],
        },
        "counts": {
            "n_features": len(features),
            "n_crash_episodes": len(crash_starts),
            "n_train": len(train),
            "n_validate": len(validate),
            "n_null_target": NULL_SAMPLE_SIZE,
            "n_null_actual": len(nulls),
        },
        "per_axis_results": per_axis_results,
        "composite_control": composite_results,
        "cross_axis_correlation": correlation_matrix,
        "dry_run": dry_run_data,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")

    print("\n=== Per-axis verdicts ===")
    print(f"{'axis':22} {'era':10} {'verdict':12} {'disc_pp':>8} {'freq':>7} {'med_rank':>9}")
    for r in per_axis_results:
        if r["verdict"] == "inconclusive":
            print(f"{r['axis']:22} {r['era']:10} {r['verdict']:12} "
                  f"{'NA':>8} {'NA':>7} {'NA':>9}  ({r['reason']})")
        else:
            print(f"{r['axis']:22} {r['era']:10} {r['verdict']:12} "
                  f"{r['discrimination_pp']:+8.1f} "
                  f"{r['frac_event_triggers']*100:6.1f}% "
                  f"{r['median_rank_on_triggering']:9.3f}")

    print("\n=== Composite control (should reproduce HA01b REFUTED both eras) ===")
    for r in composite_results:
        if r["verdict"] == "inconclusive":
            print(f"  {r['era']:10} {r['verdict']}")
        else:
            print(f"  {r['era']:10} {r['verdict']:12}  disc={r['discrimination_pp']:+.1f} pp  "
                  f"freq={r['frac_event_triggers']*100:.1f}%  "
                  f"median_shock_days={r['median_n_shock_days']}")

    print("\n=== Cross-axis correlation (Spearman) ===")
    if "error" in correlation_matrix:
        print(f"  {correlation_matrix['error']}")
    else:
        labels = correlation_matrix["axis_labels"]
        m = correlation_matrix["spearman"]
        header = " " * 22 + " ".join(f"{lab[:7]:>8}" for lab in labels)
        print(header)
        for i, lab in enumerate(labels):
            row = " ".join(f"{m[i][j]:>8.3f}" if m[i][j] is not None else f"{'NA':>8}"
                           for j in range(len(labels)))
            print(f"  {lab:20} {row}")

    print(f"\nWrote {OUT_JSON}")

    n_supported = sum(1 for r in per_axis_results if r["verdict"] == "supported")
    print(f"\n=== Decision-rule branch (per diagnostic.md section 6) ===")
    print(f"  Total per-axis SUPPORTED verdicts: {n_supported}")
    if n_supported == 0:
        print("  --> section 6.1: NO axis SUPPORTED -- confirms HA01b REFUTED, no follow-up.")
    elif n_supported == 1:
        print("  --> section 6.2: ONE axis SUPPORTED -- diagnostic finding; HA01c pre-reg + v2 threshold-monotonicity follow-up needed.")
    else:
        print("  --> section 6.3: MULTIPLE axes SUPPORTED -- cross-axis correlation determines independence; multi-comparison concern quantified honestly.")


if __name__ == "__main__":
    dry = "--dry-run-only" in sys.argv
    main(dry_run_only=dry)
