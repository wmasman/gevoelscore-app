"""Lag profile + per-axis decomposition for HA01b's SUPPORTED finding.

Two analyses:
  1. Lag profile: sweep HA01 (single-day exertion shock) across lead-up
     window lengths 2-7 days. Identifies where the validate signal
     peaks and how train scales.
  2. Per-axis decomposition at the SUPPORTED 4-day window: restrict
     "shock" definition to one of A/B/C/D axes at a time and re-test
     discrimination. Tells us which axis drives HA01b's +17.3 pp.

Output: lag_profile_report.md + lag_profile_data.json.
"""
from __future__ import annotations

import csv
import json
import random
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FEATURES_CSV = ROOT / "output" / "activity_features_daily.csv"
LABELS_CSV = (
    ROOT.parent / "hypotheses" / "crash_v2-definition" / "labels_crash_v2.csv"
)
OUT_MD = ROOT / "output" / "lag_profile_report.md"
OUT_JSON = ROOT / "output" / "lag_profile_data.json"

ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

SHOCK_CLASSES = {"heavy", "very_heavy"}
LAG_WINDOWS = [2, 3, 4, 5, 6, 7]
PER_AXIS_WINDOW = 4  # the SUPPORTED window from HA01b

# Per-axis rank thresholds matching exertion_class
RANK_HEAVY_PLUS = 0.85  # heavy + very_heavy = rank >= 0.85

AXES = [
    ("A_effective", "effective_exertion_rank_30d"),
    ("B_steps", "step_rank_30d"),
    ("C_max_hr", "max_hr_rank_30d"),
    ("D_vigorous", "vigorous_min_rank_30d"),
]


def parse_num(v):
    if v in (None, "", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def load_features() -> dict[date, dict]:
    out = {}
    for r in csv.DictReader(FEATURES_CSV.open(encoding="utf-8")):
        out[date.fromisoformat(r["date"])] = r
    return out


def load_crashes_and_dips() -> tuple[list[date], list[date]]:
    crashes_by_id: dict[str, list[date]] = {}
    dips = []
    for r in csv.DictReader(LABELS_CSV.open(encoding="utf-8")):
        d = date.fromisoformat(r["date"])
        if r["label"] == "crash":
            crashes_by_id.setdefault(r["episode_id"], []).append(d)
        elif r["label"] == "dip":
            dips.append(d)
    return sorted(min(ds) for ds in crashes_by_id.values()), sorted(dips)


def has_shock_in_window(
    ref: date, window: int, features: dict, classes: set[str]
) -> bool | None:
    """True if any day in lead-up has exertion_class in classes. None if invalid."""
    valid = 0
    for i in range(1, window + 1):
        d = ref - timedelta(days=i)
        r = features.get(d)
        if r and r.get("exertion_class"):
            valid += 1
            if r["exertion_class"] in classes:
                return True
    if valid < 2:
        return None
    return False


def has_axis_heavy_in_window(
    ref: date, window: int, features: dict, axis_key: str
) -> bool | None:
    """True if any day in lead-up has axis rank >= 0.85. None if invalid."""
    valid = 0
    for i in range(1, window + 1):
        d = ref - timedelta(days=i)
        r = features.get(d)
        if r is None:
            continue
        rank = parse_num(r.get(axis_key))
        if rank is None:
            continue
        valid += 1
        if rank >= RANK_HEAVY_PLUS:
            return True
    if valid < 2:
        return None
    return False


def build_null_refs(
    features: dict, crash_starts: list[date], dip_dates: list[date], window: int
) -> list[date]:
    """Random refs disjoint from any crash/dip lead-up of the given window."""
    rng = random.Random(RANDOM_SEED)
    occupied: set[date] = set()
    for ref in crash_starts + dip_dates:
        for i in range(1, window + 1):
            occupied.add(ref - timedelta(days=i))
    all_dates = sorted(
        d for d in features if ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END
    )
    refs = []
    attempts = 0
    while len(refs) < NULL_SAMPLE_SIZE and attempts < 10000:
        attempts += 1
        r = rng.choice(all_dates)
        leadup = {r - timedelta(days=i) for i in range(1, window + 1)}
        if leadup & occupied:
            continue
        refs.append(r)
    return refs


def evaluate(refs: list[date], window: int, features: dict,
             check_fn) -> dict:
    """Run check_fn(ref, window, features) on each ref. Returns frac, n."""
    hits = 0
    valid = 0
    for r in refs:
        result = check_fn(r, window, features)
        if result is None:
            continue
        valid += 1
        if result:
            hits += 1
    if valid == 0:
        return {"frac": None, "n_valid": 0}
    return {"frac": hits / valid, "n_valid": valid, "n_hits": hits}


def main():
    features = load_features()
    crash_starts, dip_dates = load_crashes_and_dips()
    train_crashes = [d for d in crash_starts if d <= TRAIN_END]
    validate_crashes = [d for d in crash_starts if d > TRAIN_END]
    train_dips = [d for d in dip_dates if d <= TRAIN_END]
    validate_dips = [d for d in dip_dates if d > TRAIN_END]
    print(f"Loaded {len(features)} feature days")
    print(f"  train crashes: {len(train_crashes)} | validate crashes: {len(validate_crashes)}")
    print(f"  train dips: {len(train_dips)} | validate dips: {len(validate_dips)}")

    # ── Analysis 1: Lag profile (HA01 across windows 2..7) ──
    print("\n=== Analysis 1: Lag profile ===")
    lag_results = []
    for w in LAG_WINDOWS:
        null_refs = build_null_refs(features, crash_starts, dip_dates, w)
        # composite shock (any of heavy/very_heavy)
        train_crash_eval = evaluate(train_crashes, w, features,
                                    lambda r, ww, f: has_shock_in_window(r, ww, f, SHOCK_CLASSES))
        validate_crash_eval = evaluate(validate_crashes, w, features,
                                       lambda r, ww, f: has_shock_in_window(r, ww, f, SHOCK_CLASSES))
        train_dip_eval = evaluate(train_dips, w, features,
                                  lambda r, ww, f: has_shock_in_window(r, ww, f, SHOCK_CLASSES))
        validate_dip_eval = evaluate(validate_dips, w, features,
                                     lambda r, ww, f: has_shock_in_window(r, ww, f, SHOCK_CLASSES))
        null_eval = evaluate(null_refs, w, features,
                             lambda r, ww, f: has_shock_in_window(r, ww, f, SHOCK_CLASSES))

        record = {
            "window_days": w,
            "null_n": null_eval["n_valid"],
            "null_frac": null_eval["frac"],
            "train_crash_n": train_crash_eval["n_valid"],
            "train_crash_frac": train_crash_eval["frac"],
            "validate_crash_n": validate_crash_eval["n_valid"],
            "validate_crash_frac": validate_crash_eval["frac"],
            "train_dip_n": train_dip_eval["n_valid"],
            "train_dip_frac": train_dip_eval["frac"],
            "validate_dip_n": validate_dip_eval["n_valid"],
            "validate_dip_frac": validate_dip_eval["frac"],
            "train_crash_disc_pp": (train_crash_eval["frac"] - null_eval["frac"]) * 100
                                   if train_crash_eval["frac"] is not None else None,
            "validate_crash_disc_pp": (validate_crash_eval["frac"] - null_eval["frac"]) * 100
                                      if validate_crash_eval["frac"] is not None else None,
            "train_dip_disc_pp": (train_dip_eval["frac"] - null_eval["frac"]) * 100
                                 if train_dip_eval["frac"] is not None else None,
            "validate_dip_disc_pp": (validate_dip_eval["frac"] - null_eval["frac"]) * 100
                                    if validate_dip_eval["frac"] is not None else None,
        }
        lag_results.append(record)
        print(f"  window={w}d: train_crash disc {record['train_crash_disc_pp']:+.1f} pp | "
              f"validate_crash disc {record['validate_crash_disc_pp']:+.1f} pp | "
              f"validate_dip disc {record['validate_dip_disc_pp']:+.1f} pp")

    # ── Analysis 2: Per-axis decomposition at 4-day window ──
    print(f"\n=== Analysis 2: Per-axis decomposition at {PER_AXIS_WINDOW}-day window ===")
    null_refs_4d = build_null_refs(features, crash_starts, dip_dates, PER_AXIS_WINDOW)
    axis_results = []
    for axis_name, axis_key in AXES:
        null_eval = evaluate(null_refs_4d, PER_AXIS_WINDOW, features,
                             lambda r, ww, f, ak=axis_key: has_axis_heavy_in_window(r, ww, f, ak))
        train_crash_eval = evaluate(train_crashes, PER_AXIS_WINDOW, features,
                                    lambda r, ww, f, ak=axis_key: has_axis_heavy_in_window(r, ww, f, ak))
        validate_crash_eval = evaluate(validate_crashes, PER_AXIS_WINDOW, features,
                                       lambda r, ww, f, ak=axis_key: has_axis_heavy_in_window(r, ww, f, ak))

        record = {
            "axis": axis_name,
            "axis_key": axis_key,
            "null_frac": null_eval["frac"],
            "train_crash_frac": train_crash_eval["frac"],
            "validate_crash_frac": validate_crash_eval["frac"],
            "train_disc_pp": (train_crash_eval["frac"] - null_eval["frac"]) * 100
                             if train_crash_eval["frac"] is not None and null_eval["frac"] is not None else None,
            "validate_disc_pp": (validate_crash_eval["frac"] - null_eval["frac"]) * 100
                                if validate_crash_eval["frac"] is not None and null_eval["frac"] is not None else None,
        }
        axis_results.append(record)
        print(f"  {axis_name:14}: train disc {record['train_disc_pp']:+.1f} pp | "
              f"validate disc {record['validate_disc_pp']:+.1f} pp")

    # ── Output ──
    OUT_JSON.write_text(
        json.dumps({"lag_profile": lag_results, "per_axis_4day": axis_results},
                   indent=2, default=str),
        encoding="utf-8",
    )

    lines = []
    lines.append("# Lag profile + per-axis decomposition of HA01b\n")
    lines.append("Post-hoc analysis of HA01b's SUPPORTED finding (+17.3 pp validate "
                 "at 4-day window). Brackets the lag distribution and identifies "
                 "which exertion axis drives the signal.\n")

    lines.append("## 1. Lag profile (HA01 across windows 2-7 days)\n")
    lines.append("Each row: window-day count; null + train-crash + validate-crash + "
                 "validate-dip frequencies and discriminations.\n")
    lines.append("| window | null freq | train crash freq | train disc | "
                 "validate crash freq | **validate disc** | validate dip freq | validate dip disc |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in lag_results:
        lines.append(
            f"| {r['window_days']}d | "
            f"{r['null_frac']*100:.1f}% | "
            f"{r['train_crash_frac']*100:.1f}% | "
            f"{r['train_crash_disc_pp']:+.1f} pp | "
            f"{r['validate_crash_frac']*100:.1f}% | "
            f"**{r['validate_crash_disc_pp']:+.1f} pp** | "
            f"{r['validate_dip_frac']*100:.1f}% | "
            f"{r['validate_dip_disc_pp']:+.1f} pp |"
        )
    lines.append("")
    lines.append("**Reading**: validate disc identifies the window length where the "
                 "validate-era precursor signal is strongest. HA01b's locked window (4d) "
                 "is one of these data points.\n")

    lines.append(f"## 2. Per-axis decomposition at {PER_AXIS_WINDOW}-day window\n")
    lines.append("For each axis, restrict 'shock' definition to that axis alone "
                 "(rank ≥ 0.85 = heavy+ on that axis) and re-test discrimination.\n")
    lines.append("| axis | null freq | train crash freq | train disc | "
                 "validate crash freq | **validate disc** |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for r in axis_results:
        lines.append(
            f"| {r['axis']} | "
            f"{r['null_frac']*100:.1f}% | "
            f"{r['train_crash_frac']*100:.1f}% | "
            f"{r['train_disc_pp']:+.1f} pp | "
            f"{r['validate_crash_frac']*100:.1f}% | "
            f"**{r['validate_disc_pp']:+.1f} pp** |"
        )
    lines.append("")
    lines.append("**Reading**: which single axis contributes most to HA01b's "
                 f"+17.3 pp validate discrimination? Compare each axis's validate disc "
                 "vs the multi-axis composite (HA01b validate +17.3 pp).\n")

    lines.append("---\n")
    lines.append(f"*Run 2026-06-06. Seed `{RANDOM_SEED}`.*")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
