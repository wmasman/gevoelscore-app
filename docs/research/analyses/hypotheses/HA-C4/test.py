"""HA-C4 v1 - Stage 2: 3-channel Wiggers C4 confirmatory triad test.

Implements the LOCKED HA-C4 v1 r2 pre-registration (hypothesis.md
LOCKED 2026-06-17 by user acceptance). Tests Wiggers C4 "stress fails to
drop during rest periods after overexertion / stuck sympathetic" via a
3-channel confirmatory triad: Channel 1 (same-day decay failure,
stress_post_peak_time_to_rest_min on T, NaN -> 1080 per spec 4.5);
Channel 2 (walls of orange, stress_high_duration_min on T); Channel 3
(t+1 reactivity, awake_stress_avg on T+1 with chain-T+1 exclusion per
spec 4.7). Per channel x per era (train, validate): Mann-Whitney U +
Cliff's delta + block-permutation null at E[L]=7 (B=10,000). Per spec
5.3 triad rule: pass-2-of-3 -> SUPPORTED.

Modes:
  python test.py --dry-run    print spec 7.5 sanity gates only (full-pool
                              medians within +/- 30%% of spec 7.1
                              reference; per-channel x per-era arm sizes
                              >= 30; Ch1 NaN fraction in [12%%, 25%%]).
                              If any sanity fails -> halt + write
                              dry-run-report.md + recommend HA-C4-v2 per
                              hypothesis_lock_process.md 3.9.
  python test.py              dry-run first (gates on sanity); then full
                              run emits result.md + result-data.json.

Sister-test cross-reference (informational): HA-C4b v3 NOT-SUPPORTED on
the motion-filter crash-precursor framing (a=40%%, b=-10pp, c=+1.21);
HA11 SUPPORTED on train (+22.8 pp) on the U-dip calm-day channel.

ASCII-only stdout per session handoff (no em-dash, no emojis); markdown
output may use unicode for readability.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np

# === Path setup so we can import the shared _utils.inference helper. ===

HERE = Path(__file__).resolve().parent
UTILS_DIR = HERE.parent.parent / "_utils"
if str(UTILS_DIR) not in sys.path:
    sys.path.insert(0, str(UTILS_DIR))

from inference import (  # noqa: E402
    compute_data_driven_block_length,
    holm_step_down,
)

# === Constants per locked v1 hypothesis.md ==============================

# Random seed and bootstrap config (spec 4.9 + 10.2)
RANDOM_SEED = 20260617
BOOTSTRAP_E_L = 7
B_HEADLINE = 10_000

# Eras per spec 4.10 (within unmedicated phase)
ANALYSIS_START = date(2022, 9, 3)        # train start
TRAIN_END = date(2023, 12, 31)
VALIDATE_START = date(2024, 1, 1)
VALIDATE_END = date(2024, 4, 8)          # unmedicated end inclusive

# Spec 4.3 + 6 exclusions
LC_ERA_START = date(2022, 4, 4)
UNMEDICATED_END_INCL = date(2024, 4, 8)
APRIL2024_CLUSTER_START = date(2024, 4, 9)
APRIL2024_CLUSTER_END_INCL = date(2024, 4, 16)

# Spec 4.1 + 4.2 + 4.5 channel definitions
HEAVY_CLASSES = {"heavy", "very_heavy"}
NON_HEAVY_CLASSES = {"none", "light", "moderate"}
NAN_TO_REST_CAP_MIN = 1080  # spec 4.5: NaN-as-positive -> 18h cap

CH1_PRIMARY_COL = "stress_post_peak_time_to_rest_min"
CH1_DROP_AVG_COL = "stress_post_peak_drop_avg"
CH1_RECOVERY_PCT_COL = "stress_recovery_pct_within_2h"
CH2_COL = "stress_high_duration_min"
CH3_COL = "awake_stress_avg"
CH3_SPIKE_COMPANION_COL = "stress_high_duration_min"  # on T+1 per spec 4.11.2

# Spec 5.1 per-channel confirmation bars
P_BAR = 0.05
CLIFF_BAR = 0.20

# Spec 5.4 inconclusive bar (per-arm minimum)
MIN_ARM_N = 30

# Spec 7.5 sanity gate (tightened from +/-50% to +/-30% at r2 per audit
# recommendation 1; computed at r2 from per_day_master.csv on the
# 2022-04-04 <= date <= 2024-04-08 unmedicated filter).
SANITY_TOL = 0.30
ANCHOR_71_MEDIAN = {
    "Ch1": 81.0,
    "Ch1_drop_avg": 61.0,
    "Ch2": 73.0,
    "Ch3": 46.0,
}
# Spec 7.5 Ch1 NaN-fraction sanity range
CH1_NAN_FRAC_RANGE = (0.12, 0.25)

# Spec 4.11.1 crash-drop sensitivity flag threshold (CONVENTIONS 3.4)
CRASH_DROP_FLAG = 0.10

# Spec 4.9 E[L]* deviation flag (factor-of-2 -> |E[L]* - 7| / 7 > 0.5)
EL_DEVIATION_FACTOR = 0.5

# Spec commit (lock-commit; updated at lock time if needed)
V1_SPEC_COMMIT = "(unmerged-working-tree)"

# Paths
DATA_ROOT = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH",
    r"C:\Users\Gebruiker\Documents\gevoelscore-data"))
MASTER_CSV = DATA_ROOT / "unified" / "per_day_master.csv"

OUT_RESULT_MD = HERE / "result.md"
OUT_RESULT_JSON = HERE / "result-data.json"
OUT_DRYRUN_MD = HERE / "dry-run-report.md"


# === Loaders ============================================================

def load_master() -> dict[date, dict]:
    """Load per_day_master.csv into {date: row-dict}."""
    needed = (
        "date", "is_crash", "exertion_class_lagged_lcera",
        CH1_PRIMARY_COL, CH1_DROP_AVG_COL, CH1_RECOVERY_PCT_COL,
        CH2_COL, CH3_COL,
    )
    out: dict[date, dict] = {}
    with MASTER_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                d = date.fromisoformat(row["date"])
            except (KeyError, ValueError):
                continue
            out[d] = {k: row.get(k, "") for k in needed}
    return out


def parse_float(s) -> float | None:
    """Parse a CSV string to float; treat empty/NaN as None."""
    if s == "" or s is None:
        return None
    try:
        v = float(s)
        if math.isnan(v):
            return None
        return v
    except ValueError:
        return None


# === Eligibility (spec 4.1 + 4.3 + 6) ===================================

def in_unmedicated_lc(d: date) -> bool:
    """LC era + unmedicated + not in April-2024 cluster (spec 4.3 + 6)."""
    if d < LC_ERA_START:
        return False
    if d > UNMEDICATED_END_INCL:
        return False
    if APRIL2024_CLUSTER_START <= d <= APRIL2024_CLUSTER_END_INCL:
        return False
    return True


def era_of(d: date) -> str | None:
    if ANALYSIS_START <= d <= TRAIN_END:
        return "train"
    if VALIDATE_START <= d <= VALIDATE_END:
        return "validate"
    return None


def exertion_class(d: date, master) -> str:
    return (master.get(d) or {}).get("exertion_class_lagged_lcera", "").strip()


def is_heavy_T(d: date, master) -> bool | None:
    """spec 4.1: True if heavy/very_heavy; False if none/light/moderate;
    None if missing-or-unrecognised (excluded per spec 4.6)."""
    cls = exertion_class(d, master)
    if not cls:
        return None
    if cls in HEAVY_CLASSES:
        return True
    if cls in NON_HEAVY_CLASSES:
        return False
    return None


# === Channel dataset construction (spec 4.2 + 4.5 + 4.6 + 4.7) ==========

def build_ch_dataset(channel_key: str, era: str, master,
                     crash_drop: bool = False) -> dict:
    """For (channel, era) return temporal sequence + arms.

    Per spec 4.2 + 4.5 + 4.6 + 4.7. For Ch1 NaN -> 1080 per spec 4.5
    (NaN-as-positive). For Ch3 + Ch3_spike_companion apply chain-T+1
    exclusion per spec 4.7 (drop heavy-T days where T+1 is also heavy).

    Per spec 4.11.1 crash-drop sensitivity: if crash_drop=True, days with
    is_crash == True are dropped from BOTH arms.
    """
    dates_in_era = sorted(d for d in master.keys()
                          if in_unmedicated_lc(d) and era_of(d) == era)
    values: list[float] = []
    labels: list[int] = []
    dates_kept: list[date] = []
    n_ch1_nan_encoded = 0

    for d in dates_in_era:
        h = is_heavy_T(d, master)
        if h is None:
            continue  # spec 4.6: missing/unrecognised exertion -> exclude
        row = master.get(d) or {}
        if crash_drop and row.get("is_crash", "") == "True":
            continue

        if channel_key == "Ch1":
            v = parse_float(row.get(CH1_PRIMARY_COL, ""))
            if v is None:
                v = float(NAN_TO_REST_CAP_MIN)  # spec 4.5
                n_ch1_nan_encoded += 1
        elif channel_key == "Ch1_drop_avg":
            v = parse_float(row.get(CH1_DROP_AVG_COL, ""))
            if v is None:
                continue
        elif channel_key == "Ch1_recovery_pct":
            v = parse_float(row.get(CH1_RECOVERY_PCT_COL, ""))
            if v is None:
                continue
        elif channel_key == "Ch2":
            v = parse_float(row.get(CH2_COL, ""))
            if v is None:
                continue
        elif channel_key in ("Ch3", "Ch3_spike_companion"):
            d1 = d + timedelta(days=1)
            # spec 4.7: chain-T+1 exclusion for heavy-T arm only
            if h is True:
                h1 = is_heavy_T(d1, master)
                if h1 is True:
                    continue
            # spec 4.3 rule 4: T+1 must be in unmed + not in April cluster
            if not in_unmedicated_lc(d1):
                continue
            col = CH3_COL if channel_key == "Ch3" else CH3_SPIKE_COMPANION_COL
            v = parse_float((master.get(d1) or {}).get(col, ""))
            if v is None:
                continue
        else:
            raise ValueError(f"unknown channel_key: {channel_key}")

        values.append(v)
        labels.append(1 if h else 0)
        dates_kept.append(d)

    n_heavy = sum(labels)
    n_non = len(labels) - n_heavy
    return {
        "dates": dates_kept,
        "values": np.asarray(values, dtype=float),
        "labels": np.asarray(labels, dtype=int),
        "n_heavy": n_heavy,
        "n_non_heavy": n_non,
        "n_total": len(labels),
        "ch1_nan_encoded": n_ch1_nan_encoded,
        "passes_min_arm": n_heavy >= MIN_ARM_N and n_non >= MIN_ARM_N,
    }


# === Statistics =========================================================

def _rankdata(a: np.ndarray) -> np.ndarray:
    """Rank with mid-rank for ties (vendored to avoid hard scipy dep)."""
    n = len(a)
    order = np.argsort(a, kind="mergesort")
    sorted_a = a[order]
    ranks = np.empty(n, dtype=float)
    i = 0
    while i < n:
        j = i + 1
        while j < n and sorted_a[j] == sorted_a[i]:
            j += 1
        avg_rank = (i + j + 1) / 2.0
        for k in range(i, j):
            ranks[order[k]] = avg_rank
        i = j
    return ranks


def mann_whitney_u_heavy_first(values: np.ndarray,
                                labels: np.ndarray,
                                ranks: np.ndarray | None = None) -> float:
    """U = R_heavy - n_heavy * (n_heavy + 1) / 2."""
    if ranks is None:
        ranks = _rankdata(values)
    mask = labels == 1
    n_heavy = int(mask.sum())
    if n_heavy == 0:
        return 0.0
    R = float(ranks[mask].sum())
    return R - n_heavy * (n_heavy + 1) / 2.0


def cliffs_delta(values: np.ndarray, labels: np.ndarray) -> float:
    """Cliff's delta = (#{heavy>non} - #{heavy<non}) / (n_heavy * n_non)."""
    heavy = values[labels == 1]
    non = values[labels == 0]
    n_h = len(heavy)
    n_n = len(non)
    if n_h == 0 or n_n == 0:
        return float("nan")
    non_sorted = np.sort(non)
    less = np.searchsorted(non_sorted, heavy, side="left")
    greater = n_n - np.searchsorted(non_sorted, heavy, side="right")
    return float((less.sum() - greater.sum()) / (n_h * n_n))


def stationary_bootstrap_indices(n: int, p: float,
                                  rng: np.random.Generator) -> np.ndarray:
    """Stationary-bootstrap index draw: concatenate blocks of length
    Geom(p) (E[L] = 1/p) starting at uniform-random positions, wrapping
    circularly. Returns a length-n int64 ndarray. Per inference.py."""
    indices = np.empty(n, dtype=np.int64)
    i = 0
    while i < n:
        start = int(rng.integers(0, n))
        L = int(rng.geometric(p))
        end = min(i + L, n)
        for j in range(end - i):
            indices[i + j] = (start + j) % n
        i = end
    return indices


def block_permutation_p_value(values: np.ndarray,
                                labels: np.ndarray,
                                B: int,
                                expected_block_length: int,
                                rng: np.random.Generator) -> dict:
    """Empirical one-sided p = (1 + #{U_null >= U_obs}) / (B + 1).

    Per spec 4.9: keep channel values in original temporal positions;
    resample the is_heavy_T label sequence via stationary bootstrap
    (E[L]=7); recompute U per draw. The bootstrap may produce
    n_heavy_null != n_heavy_obs (the label-count is not preserved by
    stationary bootstrap); this is the spec'd procedure per spec 4.9
    step 2 and 4.8 step 3 (U statistic comparison).
    """
    n = len(values)
    p = 1.0 / expected_block_length
    ranks = _rankdata(values)
    U_obs = mann_whitney_u_heavy_first(values, labels, ranks=ranks)
    U_null = np.empty(B)
    n_heavy_null = np.empty(B, dtype=int)
    for b in range(B):
        idx = stationary_bootstrap_indices(n, p, rng)
        perm_labels = labels[idx]
        mask = perm_labels == 1
        n_h = int(mask.sum())
        R = float(ranks[mask].sum()) if n_h > 0 else 0.0
        U_null[b] = R - n_h * (n_h + 1) / 2.0
        n_heavy_null[b] = n_h
    n_ge = int((U_null >= U_obs).sum())
    p_value = (1 + n_ge) / (B + 1)
    return {
        "U_obs": float(U_obs),
        "p_value": float(p_value),
        "U_null_median": float(np.median(U_null)),
        "U_null_p025": float(np.quantile(U_null, 0.025)),
        "U_null_p975": float(np.quantile(U_null, 0.975)),
        "n_heavy_obs": int((labels == 1).sum()),
        "n_heavy_null_mean": float(n_heavy_null.mean()),
        "n_heavy_null_std": float(n_heavy_null.std()),
    }


# === Per-cell evaluation (spec 5.1) =====================================

def evaluate_channel_era(channel_key: str, era: str, master,
                          rng: np.random.Generator,
                          B: int = B_HEADLINE,
                          crash_drop: bool = False) -> dict:
    """Compute U + Cliff's delta + block-permutation p for (channel, era).
    Returns {'verdict': 'inconclusive'} if either arm has < MIN_ARM_N."""
    ds = build_ch_dataset(channel_key, era, master, crash_drop=crash_drop)
    out: dict = {
        "channel": channel_key,
        "era": era,
        "crash_drop": crash_drop,
        "n_heavy": ds["n_heavy"],
        "n_non_heavy": ds["n_non_heavy"],
        "n_total": ds["n_total"],
        "ch1_nan_encoded": ds["ch1_nan_encoded"],
    }
    if not ds["passes_min_arm"]:
        out["verdict"] = "inconclusive"
        return out
    values, labels = ds["values"], ds["labels"]
    delta = cliffs_delta(values, labels)
    p_info = block_permutation_p_value(
        values, labels, B=B, expected_block_length=BOOTSTRAP_E_L, rng=rng)
    heavy_med = float(np.median(values[labels == 1]))
    non_med = float(np.median(values[labels == 0]))
    heavy_p25 = float(np.percentile(values[labels == 1], 25))
    heavy_p75 = float(np.percentile(values[labels == 1], 75))
    non_p25 = float(np.percentile(values[labels == 0], 25))
    non_p75 = float(np.percentile(values[labels == 0], 75))
    # spec 5.1: channel x era confirmed if p < 0.05 AND delta > +0.20
    discrimination_pass = p_info["p_value"] < P_BAR
    effect_size_pass = delta > CLIFF_BAR
    confirmed = discrimination_pass and effect_size_pass
    out.update({
        "cliffs_delta": delta,
        "U_obs": p_info["U_obs"],
        "p_value": p_info["p_value"],
        "U_null_median": p_info["U_null_median"],
        "U_null_p025": p_info["U_null_p025"],
        "U_null_p975": p_info["U_null_p975"],
        "n_heavy_null_mean": p_info["n_heavy_null_mean"],
        "n_heavy_null_std": p_info["n_heavy_null_std"],
        "heavy_median": heavy_med,
        "heavy_p25": heavy_p25,
        "heavy_p75": heavy_p75,
        "non_heavy_median": non_med,
        "non_heavy_p25": non_p25,
        "non_heavy_p75": non_p75,
        "discrimination_pass": discrimination_pass,
        "effect_size_pass": effect_size_pass,
        "confirmed": confirmed,
        "verdict": "confirmed" if confirmed else "not_confirmed",
    })
    return out


# === Triad verdict (spec 5.3) ===========================================

def triad_verdict(per_channel_per_era: dict) -> dict:
    """spec 5.3 with fractional accounting: confirmed both eras = 1.0;
    one era = 0.5; neither = 0. Sum across 3 channels. Thresholds:
    >= 2.0 SUPPORTED; 1.5 PARTIAL+; 1.0 PARTIAL; 0.5 PARTIAL-; 0 REJECTED."""
    score = 0.0
    breakdown: dict[str, dict] = {}
    for ch in ("Ch1", "Ch2", "Ch3"):
        train_cell = per_channel_per_era[ch].get("train", {})
        validate_cell = per_channel_per_era[ch].get("validate", {})
        train_ok = bool(train_cell.get("confirmed", False))
        validate_ok = bool(validate_cell.get("confirmed", False))
        train_inc = train_cell.get("verdict") == "inconclusive"
        validate_inc = validate_cell.get("verdict") == "inconclusive"
        if train_ok and validate_ok:
            ch_score = 1.0
            label = "confirmed both eras"
        elif train_ok or validate_ok:
            ch_score = 0.5
            label = ("confirmed train only" if train_ok
                     else "confirmed validate only")
        else:
            ch_score = 0.0
            if train_inc and validate_inc:
                label = "inconclusive both eras"
            elif train_inc or validate_inc:
                label = ("not confirmed (one era inconclusive)")
            else:
                label = "not confirmed either era"
        breakdown[ch] = {
            "score": ch_score, "label": label,
            "train_confirmed": train_ok,
            "validate_confirmed": validate_ok,
            "train_inconclusive": train_inc,
            "validate_inconclusive": validate_inc,
        }
        score += ch_score
    if score >= 3.0:
        verdict, strength = "SUPPORTED", "strong (3-of-3 channels both eras)"
    elif score >= 2.0:
        verdict, strength = "SUPPORTED", "clears triad bar"
    elif score == 1.5:
        verdict, strength = "PARTIAL+", "partial with extra signal"
    elif score == 1.0:
        verdict, strength = "PARTIAL", ""
    elif score == 0.5:
        verdict, strength = "PARTIAL-", "minimal signal"
    else:
        verdict, strength = "REJECTED", ""
    return {"score": score, "verdict": verdict, "strength": strength,
            "breakdown": breakdown}


# === Sanity-gate / dry-run descriptives (spec 7.5) ======================

def full_pool_median(channel_key: str, master) -> dict:
    """Full unmedicated-only pool median for spec 7.5 gate-1 anchor.

    Uses non-NaN values for each channel (matches spec 7.1 'n (non-NaN)'
    column). For Ch1 the NaN-as-positive encoding is NOT applied here,
    because the spec 7.1 reference itself was computed on the non-NaN
    pool (n=603).
    """
    col_map = {
        "Ch1": CH1_PRIMARY_COL,
        "Ch1_drop_avg": CH1_DROP_AVG_COL,
        "Ch2": CH2_COL,
        "Ch3": CH3_COL,
    }
    col = col_map[channel_key]
    vals: list[float] = []
    n_total = 0
    n_nan = 0
    for d, row in master.items():
        if not in_unmedicated_lc(d):
            continue
        n_total += 1
        v = parse_float(row.get(col, ""))
        if v is None:
            n_nan += 1
            continue
        vals.append(v)
    return {
        "median": float(np.median(vals)) if vals else float("nan"),
        "n_used": len(vals),
        "n_nan": n_nan,
        "n_total": n_total,
    }


def dry_run(master) -> dict:
    """Run spec 7.5 sanity-gate checks. Returns dict with 'verdict' in
    {'PASS', 'HALT'} and per-gate detail. Prints to stdout."""
    print("\n=== HA-C4 v1 dry-run ===\n")
    print("(headline cell: unmedicated x {Ch1, Ch2, Ch3} x heavy-T-vs-non-heavy-T")
    print(" x Mann-Whitney U + Cliff's delta x block-permutation null E[L]=7")
    print(" x pass-2-of-3 verdict rule applied within each era.)")
    print("(day-validity per spec 4.3: LC era + unmedicated + not April-2024")
    print(" cluster + non-empty exertion classification + channel-value")
    print(" handling per spec 4.5/4.6/4.7.)")
    print("(spec 7.5 sanity gate: full-pool medians within +/-30%% of spec 7.1")
    print(" reference; per-channel x per-era arm sizes >= 30; Ch1 NaN fraction")
    print(" in [12%%, 25%%].)")

    sanity_fails: list[str] = []

    # --- Gate 1: full-pool median check (+/-30% of spec 7.1) ---
    print("\n--- spec 7.5 gate 1: full-pool median check (+/-30%% of spec 7.1) ---")
    pool_meds: dict[str, dict] = {}
    for k, ref in ANCHOR_71_MEDIAN.items():
        info = full_pool_median(k, master)
        pool_meds[k] = info
        med = info["median"]
        lo, hi = ref * (1 - SANITY_TOL), ref * (1 + SANITY_TOL)
        ok = (not math.isnan(med)) and lo <= med <= hi
        print(f"  {k:14}: full_pool_median={med:>7.2f} "
              f"(ref={ref}, [+/-30%%] = [{lo:.2f}, {hi:.2f}]) "
              f"n_used={info['n_used']:>4} n_total={info['n_total']:>4} "
              f"-> {'PASS' if ok else 'FAIL'}")
        if not ok:
            sanity_fails.append(
                f"{k} full-pool median = {med:.2f} outside "
                f"[{lo:.2f}, {hi:.2f}] (spec 7.1 ref {ref}, +/-30%%)")

    # --- Gate 2: per-channel x per-era arm sizes (>= 30 both) ---
    print("\n--- spec 7.5 gate 2: per-channel x per-era arm sizes "
          "(>= 30 each arm) ---")
    arm_sizes: dict[str, dict[str, dict]] = {}
    for ch in ("Ch1", "Ch2", "Ch3"):
        arm_sizes[ch] = {}
        for era in ("train", "validate"):
            ds = build_ch_dataset(ch, era, master)
            arm_sizes[ch][era] = {
                "n_heavy": ds["n_heavy"],
                "n_non": ds["n_non_heavy"],
                "n_total": ds["n_total"],
                "ch1_nan_encoded": ds["ch1_nan_encoded"],
                "passes": ds["passes_min_arm"],
            }
            extra = ""
            if ch == "Ch1":
                extra = f" (ch1_nan_encoded={ds['ch1_nan_encoded']})"
            print(f"  {ch} {era:8}: n_heavy={ds['n_heavy']:>4} "
                  f"n_non={ds['n_non_heavy']:>4} "
                  f"-> {'PASS' if ds['passes_min_arm'] else 'FAIL'}{extra}")
            if not ds["passes_min_arm"]:
                sanity_fails.append(
                    f"{ch} {era}: heavy n={ds['n_heavy']}, "
                    f"non-heavy n={ds['n_non_heavy']} "
                    f"(both must be >= {MIN_ARM_N})")

    # --- Gate 3: Ch1 full-pool NaN fraction in [12%, 25%] ---
    print("\n--- spec 7.5 gate 3: Ch1 full-pool NaN fraction in [12%%, 25%%] ---")
    ch1_info = pool_meds["Ch1"]
    nan_frac = ch1_info["n_nan"] / ch1_info["n_total"] if ch1_info["n_total"] else float("nan")
    lo, hi = CH1_NAN_FRAC_RANGE
    ok = (not math.isnan(nan_frac)) and lo <= nan_frac <= hi
    print(f"  Ch1 NaN fraction = {nan_frac:.4f} "
          f"({ch1_info['n_nan']}/{ch1_info['n_total']}); "
          f"range [{lo}, {hi}] -> {'PASS' if ok else 'FAIL'}")
    if not ok:
        sanity_fails.append(
            f"Ch1 NaN fraction = {nan_frac:.4f} outside [{lo}, {hi}]")

    print("")
    if sanity_fails:
        print(f"--- DRY-RUN VERDICT: HALT ({len(sanity_fails)} sanity "
              f"failure{'s' if len(sanity_fails) > 1 else ''}) ---")
        for f in sanity_fails:
            print(f"  - {f}")
        print(f"\nPer spec 10.4 step 1 + hypothesis_lock_process.md 3.9: "
              f"DO NOT run the full test. HA-C4-v2 revision required.")
    else:
        print("--- DRY-RUN VERDICT: PASS (proceed with `python test.py`) ---")

    return {
        "pool_medians": pool_meds,
        "arm_sizes": arm_sizes,
        "ch1_nan_fraction": nan_frac,
        "ch1_nan_count": ch1_info["n_nan"],
        "ch1_pool_total": ch1_info["n_total"],
        "sanity_fails": sanity_fails,
        "verdict": "HALT" if sanity_fails else "PASS",
    }


# === dry-run-report.md emitter ==========================================

def write_dry_run_report(dry: dict) -> None:
    halt = dry["verdict"] == "HALT"
    title = ("HA-C4 v1 dry-run report — SANITY-GATE FAILURE (HALT)" if halt
             else "HA-C4 v1 dry-run report — sanity gates PASS")
    lines: list[str] = [
        f"# {title}",
        "",
        ("Emitted by `test.py --dry-run` per locked v1 hypothesis.md §10.4. "
         "Headline cell: unmedicated × {Ch1, Ch2, Ch3} × "
         "heavy-T-vs-non-heavy-T × Mann-Whitney U + Cliff's δ × "
         "block-permutation null E[L]=7 × pass-2-of-3 verdict rule applied "
         "within each era. Day-validity per §4.3 (LC era + unmedicated + "
         "not April-2024 cluster + non-empty exertion classification + "
         "channel-value handling per §4.5/§4.6/§4.7)."),
        "",
    ]
    if halt:
        lines.extend([
            "## §7.5 sanity-gate failures",
            "",
        ])
        for f in dry["sanity_fails"]:
            lines.append(f"- {f}")
        lines.extend([
            "",
            ("Per v1 §9.5 + §10.4 step 1 + the locked-pre-reg discipline "
             "(`hypothesis_lock_process.md` §3.9), the full test is NOT "
             "run and `result.md` is NOT emitted. The spec must be revised "
             "before any further test run; the revision creates HA-C4-v2 "
             "with v1 archived."),
            "",
        ])

    lines.extend([
        "## §7.5 gate 1: full-pool median (±30% of §7.1 reference)",
        "",
        ("All four anchors computed at r2 from `per_day_master.csv` on the "
         "`2022-04-04 ≤ date ≤ 2024-04-08` unmedicated filter (see "
         "hypothesis.md §7.1)."),
        "",
        "| channel | full-pool median | §7.1 ref | tol [±30%] | n_used | n_total | gate |",
        "|---|---:|---:|---|---:|---:|---|",
    ])
    for k, ref in ANCHOR_71_MEDIAN.items():
        info = dry["pool_medians"][k]
        med = info["median"]
        lo, hi = ref * (1 - SANITY_TOL), ref * (1 + SANITY_TOL)
        ok = (not math.isnan(med)) and lo <= med <= hi
        med_s = "NA" if math.isnan(med) else f"{med:.2f}"
        lines.append(
            f"| {k} | {med_s} | {ref} | "
            f"[{lo:.2f}, {hi:.2f}] | {info['n_used']} | {info['n_total']} | "
            f"{'PASS' if ok else 'FAIL'} |")
    lines.append("")

    lines.extend([
        "## §7.5 gate 2: per-channel × per-era arm sizes (≥30 each arm)",
        "",
        "| channel | era | n_heavy | n_non_heavy | n_total | gate |",
        "|---|---|---:|---:|---:|---|",
    ])
    for ch in ("Ch1", "Ch2", "Ch3"):
        for era in ("train", "validate"):
            info = dry["arm_sizes"][ch][era]
            lines.append(
                f"| {ch} | {era} | {info['n_heavy']} | {info['n_non']} | "
                f"{info['n_total']} | "
                f"{'PASS' if info['passes'] else 'FAIL'} |")
    lines.append("")

    lines.extend([
        "## §7.5 gate 3: Ch1 full-pool NaN fraction (per §4.5 + §7.5)",
        "",
        f"- Observed Ch1 NaN fraction (unmedicated only): "
        f"**{dry['ch1_nan_fraction']:.4f}** "
        f"({dry['ch1_nan_count']}/{dry['ch1_pool_total']}).",
        f"- §7.5 sanity range: [{CH1_NAN_FRAC_RANGE[0]}, {CH1_NAN_FRAC_RANGE[1]}].",
        ("- Semantically per [DATA_DICTIONARY §C4]"
         "(../../../DATA_DICTIONARY.md#c4--stress-decay-after-daily-peak-4-columns):"
         " NaN = 'stress never returned to rest that day' (C4-positive case). "
         "The §4.5 1080-min encoding applies in the channel-arm test."),
        "",
    ])
    if halt:
        lines.extend([
            "## Next step (HALT branch)",
            "",
            ("Per the locked-pre-reg discipline (`hypothesis.md` v1 §10.4 + "
             "§9.5), the spec must be revised before any further test run; "
             "the revision creates HA-C4-v2 with v1 archived. Fresh-session "
             "v2-draft per `hypothesis_lock_process.md` §3.2."),
            "",
        ])
    else:
        lines.extend([
            "## Next step (PASS branch)",
            "",
            ("Sanity gates passed; the full test runs after the dry-run "
             "inside the same `python test.py` invocation, emitting "
             "`result.md` + `result-data.json`. Per §10.4 step 3: **no "
             "iteration on the spec after the dry-run passes** — any "
             "post-dry-run revision creates HA-C4-v2."),
            "",
        ])
    OUT_DRYRUN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {OUT_DRYRUN_MD}", file=sys.stderr)


# === Full run (spec 10.4 step 2) ========================================

def _ch1_nan_fraction_per_arm_per_era(master) -> dict:
    """Per-era heavy-T vs non-heavy-T Ch1 NaN-fraction contrast
    (spec 4.11 NaN-fraction descriptive contrast)."""
    out: dict[str, dict] = {}
    for era in ("train", "validate"):
        n_h_total = 0
        n_h_nan = 0
        n_n_total = 0
        n_n_nan = 0
        for d in sorted(master.keys()):
            if not in_unmedicated_lc(d):
                continue
            if era_of(d) != era:
                continue
            h = is_heavy_T(d, master)
            if h is None:
                continue
            v = parse_float((master.get(d) or {}).get(CH1_PRIMARY_COL, ""))
            if h:
                n_h_total += 1
                if v is None:
                    n_h_nan += 1
            else:
                n_n_total += 1
                if v is None:
                    n_n_nan += 1
        hf = n_h_nan / n_h_total if n_h_total else float("nan")
        nf = n_n_nan / n_n_total if n_n_total else float("nan")
        pp = (hf - nf) * 100 if (n_h_total and n_n_total) else float("nan")
        out[era] = {
            "heavy_n": n_h_total, "heavy_nan": n_h_nan, "heavy_nan_frac": hf,
            "non_heavy_n": n_n_total, "non_heavy_nan": n_n_nan,
            "non_heavy_nan_frac": nf, "pp_contrast": pp,
        }
    return out


def run_full(master, dry: dict) -> dict:
    rng = np.random.default_rng(RANDOM_SEED)

    # --- Primary per-channel x per-era ---
    print("\n=== HA-C4 v1 full run ===\n", file=sys.stderr)
    print(f"  RANDOM_SEED={RANDOM_SEED}; B={B_HEADLINE}; E[L]={BOOTSTRAP_E_L}",
          file=sys.stderr)
    per_channel_per_era: dict[str, dict[str, dict]] = {
        ch: {} for ch in ("Ch1", "Ch2", "Ch3")
    }
    for ch in ("Ch1", "Ch2", "Ch3"):
        for era in ("train", "validate"):
            print(f"  evaluating {ch} {era}...", file=sys.stderr)
            cell = evaluate_channel_era(ch, era, master, rng, B=B_HEADLINE)
            per_channel_per_era[ch][era] = cell
            if cell.get("verdict") == "inconclusive":
                print(f"    -> INCONCLUSIVE (n_heavy={cell['n_heavy']}, "
                      f"n_non={cell['n_non_heavy']})", file=sys.stderr)
            else:
                print(f"    -> delta={cell['cliffs_delta']:+.3f} "
                      f"p={cell['p_value']:.4f} "
                      f"confirmed={cell['confirmed']}", file=sys.stderr)

    # --- Triad verdict ---
    triad = triad_verdict(per_channel_per_era)
    print(f"\n  TRIAD: score={triad['score']} verdict={triad['verdict']} "
          f"{triad['strength']}", file=sys.stderr)

    # --- Holm step-down per era (spec 5.5; n_eff = 3) ---
    holm_per_era: dict[str, dict] = {}
    for era in ("train", "validate"):
        ps = [per_channel_per_era[ch][era].get("p_value", float("nan"))
              for ch in ("Ch1", "Ch2", "Ch3")]
        ps_clean = np.asarray([p if not math.isnan(p) else 1.0 for p in ps],
                              dtype=float)
        h = holm_step_down(ps_clean, n_eff=3, alpha=0.05)
        holm_per_era[era] = {
            "raw_p_values": ps,
            "thresholds": h["thresholds"].tolist(),
            "rejected": [bool(x) for x in h["rejected"].tolist()],
            "adjusted_p_values": h["adjusted_p_values"].tolist(),
            "n_eff_used": int(h["n_eff_used"]),
        }

    # --- §4.11.1 crash-drop sensitivity arm ---
    print("\n  --- §4.11.1 crash-drop sensitivity ---", file=sys.stderr)
    crash_drop_per_channel_per_era: dict[str, dict[str, dict]] = {
        ch: {} for ch in ("Ch1", "Ch2", "Ch3")
    }
    for ch in ("Ch1", "Ch2", "Ch3"):
        for era in ("train", "validate"):
            print(f"  evaluating {ch} {era} (crash-dropped)...", file=sys.stderr)
            cell = evaluate_channel_era(
                ch, era, master, rng, B=B_HEADLINE, crash_drop=True)
            crash_drop_per_channel_per_era[ch][era] = cell

    crash_drop_deltas: dict[str, dict[str, dict]] = {}
    for ch in ("Ch1", "Ch2", "Ch3"):
        crash_drop_deltas[ch] = {}
        for era in ("train", "validate"):
            primary = per_channel_per_era[ch][era].get("cliffs_delta")
            cd_cell = crash_drop_per_channel_per_era[ch][era]
            cd = cd_cell.get("cliffs_delta")
            if (primary is None or cd is None or
                    (isinstance(primary, float) and math.isnan(primary)) or
                    (isinstance(cd, float) and math.isnan(cd))):
                crash_drop_deltas[ch][era] = {
                    "primary_delta": primary, "crash_dropped_delta": cd,
                    "delta_change": None, "flag": None,
                }
                continue
            d_change = cd - primary
            crash_drop_deltas[ch][era] = {
                "primary_delta": float(primary),
                "crash_dropped_delta": float(cd),
                "delta_change": float(d_change),
                "n_heavy_dropped": cd_cell.get("n_heavy", None),
                "n_non_dropped": cd_cell.get("n_non_heavy", None),
                "flag": abs(d_change) > CRASH_DROP_FLAG,
            }

    # --- §4.11.2 Ch3 spike companion ---
    print("\n  --- §4.11.2 Ch3 spike companion ---", file=sys.stderr)
    ch3_spike_per_era: dict[str, dict] = {}
    for era in ("train", "validate"):
        print(f"  evaluating Ch3_spike_companion {era}...", file=sys.stderr)
        ch3_spike_per_era[era] = evaluate_channel_era(
            "Ch3_spike_companion", era, master, rng, B=B_HEADLINE)

    # --- §4.11 other companions ---
    print("\n  --- §4.11 Ch1 secondary companions (drop_avg, recovery_pct) ---",
          file=sys.stderr)
    ch1_dropavg_per_era: dict[str, dict] = {}
    ch1_recpct_per_era: dict[str, dict] = {}
    for era in ("train", "validate"):
        print(f"  evaluating Ch1_drop_avg {era}...", file=sys.stderr)
        ch1_dropavg_per_era[era] = evaluate_channel_era(
            "Ch1_drop_avg", era, master, rng, B=B_HEADLINE)
        print(f"  evaluating Ch1_recovery_pct {era}...", file=sys.stderr)
        ch1_recpct_per_era[era] = evaluate_channel_era(
            "Ch1_recovery_pct", era, master, rng, B=B_HEADLINE)

    # --- Ch1 NaN-fraction descriptive contrast per arm per era ---
    nan_frac_contrast = _ch1_nan_fraction_per_arm_per_era(master)

    # --- §4.9 data-driven E[L]* companion (factor-of-2 flag) ---
    print("\n  --- §4.9 data-driven E[L]* companion ---", file=sys.stderr)
    el_star: dict[str, dict[str, dict]] = {}
    for ch in ("Ch1", "Ch2", "Ch3"):
        el_star[ch] = {}
        for era in ("train", "validate"):
            ds = build_ch_dataset(ch, era, master)
            v_res = compute_data_driven_block_length(
                ds["values"], default_block_length=BOOTSTRAP_E_L,
                deviation_flag_factor=EL_DEVIATION_FACTOR)
            l_res = compute_data_driven_block_length(
                ds["labels"].astype(float),
                default_block_length=BOOTSTRAP_E_L,
                deviation_flag_factor=EL_DEVIATION_FACTOR)
            el_star[ch][era] = {
                "values": {
                    "optimal_block_length": float(v_res["optimal_block_length"]),
                    "cutoff_lag": (int(v_res["cutoff_lag"])
                                   if v_res["cutoff_lag"] is not None else None),
                    "flagged_deviation": bool(v_res["flagged_deviation"]),
                    "note": v_res.get("note"),
                },
                "labels": {
                    "optimal_block_length": float(l_res["optimal_block_length"]),
                    "cutoff_lag": (int(l_res["cutoff_lag"])
                                   if l_res["cutoff_lag"] is not None else None),
                    "flagged_deviation": bool(l_res["flagged_deviation"]),
                    "note": l_res.get("note"),
                },
            }
    any_flag = any(
        el_star[ch][era][k]["flagged_deviation"]
        for ch in ("Ch1", "Ch2", "Ch3")
        for era in ("train", "validate")
        for k in ("values", "labels")
    )
    el_flag_fires = triad["verdict"].startswith("SUPPORTED") and any_flag

    return {
        "spec_commit": V1_SPEC_COMMIT,
        "config": {
            "B": B_HEADLINE,
            "BOOTSTRAP_E_L": BOOTSTRAP_E_L,
            "RANDOM_SEED": RANDOM_SEED,
            "P_BAR": P_BAR,
            "CLIFF_BAR": CLIFF_BAR,
            "MIN_ARM_N": MIN_ARM_N,
            "NAN_TO_REST_CAP_MIN": NAN_TO_REST_CAP_MIN,
            "SANITY_TOL": SANITY_TOL,
            "CRASH_DROP_FLAG": CRASH_DROP_FLAG,
            "EL_DEVIATION_FACTOR": EL_DEVIATION_FACTOR,
        },
        "per_channel_per_era": per_channel_per_era,
        "triad": triad,
        "holm_per_era": holm_per_era,
        "crash_drop_per_channel_per_era": crash_drop_per_channel_per_era,
        "crash_drop_deltas": crash_drop_deltas,
        "ch3_spike_per_era": ch3_spike_per_era,
        "ch1_dropavg_per_era": ch1_dropavg_per_era,
        "ch1_recpct_per_era": ch1_recpct_per_era,
        "nan_frac_contrast": nan_frac_contrast,
        "el_star": el_star,
        "el_any_flag": any_flag,
        "el_flag_fires_for_verdict": el_flag_fires,
        "sanity": dry,
    }


# === result.md emitter (spec 10.3) ======================================

def fmt(x, fmt_spec: str = "{:.4f}") -> str:
    if x is None:
        return "NA"
    try:
        if isinstance(x, float) and math.isnan(x):
            return "NA"
        return fmt_spec.format(x)
    except Exception:
        return str(x)


def write_result_md(results: dict) -> None:
    triad = results["triad"]
    pcpe = results["per_channel_per_era"]
    verdict_label = triad["verdict"]
    score = triad["score"]
    lines: list[str] = []

    lines.append(f"# HA-C4 v1 — RESULT: {verdict_label} (channel score = {score} / 3)")
    lines.append("")
    lines.append(
        f"Emitted by `test.py` per locked v1 hypothesis.md §10.3. "
        f"**Headline cell**: unmedicated × {{Ch1, Ch2, Ch3}} × "
        f"heavy-T-vs-non-heavy-T × Mann-Whitney U + Cliff's δ × "
        f"block-permutation null E[L]=7 × pass-2-of-3 verdict rule "
        f"applied within each era. **Random seed**: "
        f"`RANDOM_SEED = {RANDOM_SEED}`; **B** = {B_HEADLINE} bootstrap "
        f"draws per cell.")
    lines.append("")

    # --- Data-exposure caveat block at top (spec 10.3 + §8) ---
    lines.append("## Data-exposure context (prominent per §10.3 caveat-at-top rule)")
    lines.append("")
    lines.append(
        "HA-C4 v1 r2 was drafted, audited (fresh-session, verdict "
        "`REVISION RECOMMENDED`), revised, and **LOCKED 2026-06-17 by user "
        "acceptance** in a session that had already executed sister test "
        "HA-C4b (v1 → v2 → v3, NOT-SUPPORTED). The drafter knows the "
        "identity of 10 unmedicated heavy-T crash days, but NOT the "
        "per-day per-channel values for the HA-C4 channels (different "
        "aggregations of the same underlying monitoring_b data). The §3.4 "
        "fresh-session audit verified no operational choices in §4 / §5 "
        "were biased by knowledge of the 10 crash-day identities. The L2.5 "
        "substantive concern about shared-context drafting is "
        "**priced-in by user acceptance** per audit Section 4 item-6 "
        "option (a). The §4.11.1 crash-drop sensitivity arm (added r2) "
        "further insulates the spec from 'silent crash-channel-driving' "
        "concerns; the sensitivity readings are reported below.")
    lines.append("")
    lines.append(
        "**Test execution session**: this `test.py` was implemented and run "
        "in a FRESH Claude session with no prior knowledge of how "
        "Mann-Whitney + Cliff's δ + block-permutation would land on the "
        "four HA-C4 channels — the conservative choice per the "
        "locked-pre-reg discipline.")
    lines.append("")

    # --- spec 7.5 sanity-gate compliance summary at top ---
    lines.append("## §7.5 sanity-gate compliance (top-of-report, per §10.3)")
    lines.append("")
    lines.append(
        "All sanity gates passed at dry-run (see `dry-run-report.md` for "
        "per-gate detail).")
    lines.append("")
    lines.append("| gate | result |")
    lines.append("|---|---|")
    lines.append("| Full-pool median within ±30% of §7.1 (×4 channels) | PASS |")
    lines.append("| Per-channel × per-era arm sizes ≥ 30 (×6 cells) | PASS |")
    lines.append(
        f"| Ch1 NaN fraction in [12%, 25%] | PASS (observed "
        f"{results['sanity']['ch1_nan_fraction']:.4f}) |")
    lines.append("")

    # --- Triad verdict block (first substantive section per §10.3) ---
    lines.append("## §5.3 triad verdict")
    lines.append("")
    strength_str = f"; {triad['strength']}" if triad["strength"] else ""
    lines.append(
        f"**Verdict: {verdict_label}** "
        f"(channel-confirmation score = {score} of 3{strength_str}).")
    lines.append("")
    lines.append("| channel | train confirmed | validate confirmed | channel score | label |")
    lines.append("|---|---|---|---:|---|")
    for ch in ("Ch1", "Ch2", "Ch3"):
        b = triad["breakdown"][ch]
        t = "✓" if b["train_confirmed"] else (
            "INC" if b["train_inconclusive"] else "✗")
        v = "✓" if b["validate_confirmed"] else (
            "INC" if b["validate_inconclusive"] else "✗")
        lines.append(
            f"| {ch} | {t} | {v} | {b['score']} | {b['label']} |")
    lines.append("")
    lines.append(
        "Per §5.3 scoring rule: confirmed in BOTH eras → 1.0; confirmed in "
        "only ONE era → 0.5; not confirmed → 0.0. Verdict thresholds: "
        "≥ 2.0 → **SUPPORTED**; 1.5 → **PARTIAL+**; 1.0 → **PARTIAL**; "
        "0.5 → **PARTIAL−**; 0 → **REJECTED**.")
    lines.append("")

    # --- §5.1 + §5.2 per-channel × per-era contingency table ---
    lines.append("## §5.1 + §5.2 per-channel × per-era contingency table (primary)")
    lines.append("")
    lines.append(
        "Per-cell: Mann-Whitney U + Cliff's δ + block-permutation null at "
        "E[L]=7. **(a) discrimination**: empirical p < 0.05. "
        "**(b) effect size**: δ > +0.20 in predicted direction "
        "(heavy-T > non-heavy-T). Channel × era **confirmed** iff (a) AND "
        "(b) both hold.")
    lines.append("")
    lines.append(
        "| ch | era | n_heavy | n_non | heavy med [p25–p75] | non med [p25–p75] | "
        "Cliff's δ | p-value | (a) | (b) | confirmed |")
    lines.append(
        "|---|---|---:|---:|---|---|---:|---:|:---:|:---:|:---:|")
    for ch in ("Ch1", "Ch2", "Ch3"):
        for era in ("train", "validate"):
            cell = pcpe[ch][era]
            if cell.get("verdict") == "inconclusive":
                lines.append(
                    f"| {ch} | {era} | {cell['n_heavy']} | {cell['n_non_heavy']} | "
                    f"— | — | — | — | — | — | INCONCLUSIVE |")
                continue
            heavy_iqr = (f"{cell['heavy_median']:.2f} "
                         f"[{cell['heavy_p25']:.2f}–{cell['heavy_p75']:.2f}]")
            non_iqr = (f"{cell['non_heavy_median']:.2f} "
                       f"[{cell['non_heavy_p25']:.2f}–{cell['non_heavy_p75']:.2f}]")
            lines.append(
                f"| {ch} | {era} | {cell['n_heavy']} | {cell['n_non_heavy']} | "
                f"{heavy_iqr} | {non_iqr} | "
                f"{cell['cliffs_delta']:+.3f} | {cell['p_value']:.4f} | "
                f"{'✓' if cell['discrimination_pass'] else '✗'} | "
                f"{'✓' if cell['effect_size_pass'] else '✗'} | "
                f"{'✓' if cell['confirmed'] else '✗'} |")
    lines.append("")
    if any(
        pcpe[ch][era].get("ch1_nan_encoded", 0) > 0
        for ch in ("Ch1",)
        for era in ("train", "validate")
    ):
        nan_enc_train = pcpe["Ch1"]["train"].get("ch1_nan_encoded", 0)
        nan_enc_validate = pcpe["Ch1"]["validate"].get("ch1_nan_encoded", 0)
        lines.append(
            f"*Channel 1 NaN-as-positive encoding (§4.5)*: "
            f"{nan_enc_train} train + {nan_enc_validate} validate days "
            f"had `stress_post_peak_time_to_rest_min` NaN and were "
            f"recoded to {NAN_TO_REST_CAP_MIN} min for the Mann-Whitney + "
            f"Cliff's δ computation.")
        lines.append("")

    # --- §5.5 Holm step-down per era (secondary) ---
    lines.append("## §5.5 Holm step-down per era (multiplicity sensitivity, secondary)")
    lines.append("")
    lines.append(
        "Holm step-down at α=0.05 on the 3 per-channel p-values within "
        "each era. **Per §5.5, the Holm result is a stricter sensitivity "
        "report; the §5.3 verdict uses the uncorrected per-channel "
        "p-values.** If the verdict survives Holm correction, that is "
        "stronger; if not, that is a multiplicity-fragility flag.")
    lines.append("")
    lines.append(
        "| era | Ch1 raw p | Ch2 raw p | Ch3 raw p | "
        "Ch1 adj p | Ch2 adj p | Ch3 adj p | Holm-rejected channels |")
    lines.append(
        "|---|---:|---:|---:|---:|---:|---:|---|")
    for era in ("train", "validate"):
        h = results["holm_per_era"][era]
        ps = h["raw_p_values"]
        adj = h["adjusted_p_values"]
        rej = h["rejected"]
        rej_str = ", ".join(
            ch for i, ch in enumerate(("Ch1", "Ch2", "Ch3")) if rej[i]
        ) or "(none)"
        lines.append(
            f"| {era} | "
            f"{fmt(ps[0])} | {fmt(ps[1])} | {fmt(ps[2])} | "
            f"{fmt(adj[0])} | {fmt(adj[1])} | {fmt(adj[2])} | "
            f"{rej_str} |")
    lines.append("")

    # --- §4.11.1 crash-drop sensitivity ---
    lines.append("## §4.11.1 Crash-drop sensitivity (CONVENTIONS §3.4)")
    lines.append("")
    lines.append(
        "Per §4.11.1 + audit L4.4 closure: re-run the Mann-Whitney + Cliff's δ "
        f"with `is_crash == True` dropped from BOTH arms. Flag if "
        f"|Δ Cliff's δ| > {CRASH_DROP_FLAG} on any channel "
        "(\"the channel's signal is crash-driven, not robust across the "
        "broader heavy-T pool\").")
    lines.append("")
    lines.append(
        "| channel | era | primary δ | crash-dropped δ | Δ δ "
        "(dropped − primary) | n_heavy (dropped) | flag |")
    lines.append(
        "|---|---|---:|---:|---:|---:|:---:|")
    for ch in ("Ch1", "Ch2", "Ch3"):
        for era in ("train", "validate"):
            cd = results["crash_drop_deltas"][ch][era]
            if cd.get("delta_change") is None:
                lines.append(
                    f"| {ch} | {era} | "
                    f"{fmt(cd.get('primary_delta'), '{:+.3f}')} | "
                    f"{fmt(cd.get('crash_dropped_delta'), '{:+.3f}')} | "
                    f"— | — | NA |")
                continue
            lines.append(
                f"| {ch} | {era} | "
                f"{cd['primary_delta']:+.3f} | "
                f"{cd['crash_dropped_delta']:+.3f} | "
                f"{cd['delta_change']:+.3f} | "
                f"{cd['n_heavy_dropped']} | "
                f"{'**FLAG**' if cd['flag'] else 'ok'} |")
    lines.append("")

    # --- §4.11.2 Ch3 spike companion ---
    lines.append("## §4.11.2 Channel 3 spike-metric companion (CONVENTIONS §3.5)")
    lines.append("")
    lines.append(
        "Per §4.11.2 + audit L4.5 closure: parallel Mann-Whitney on "
        "`stress_high_duration_min` on T+1 (spike-count companion) "
        "alongside the primary `awake_stress_avg` on T+1 (mean). "
        "If both readings agree (same verdict direction and approximate "
        "effect-size), the average-vs-spike question is closed; if they "
        "diverge, the divergence is informative for §9 interpretation.")
    lines.append("")
    lines.append(
        "| era | primary Ch3 (awake-mean T+1) δ | spike companion "
        "(high_dur T+1) δ | primary p | spike p | agree? |")
    lines.append(
        "|---|---:|---:|---:|---:|:---:|")
    for era in ("train", "validate"):
        c3 = pcpe["Ch3"][era]
        sp = results["ch3_spike_per_era"][era]
        d3 = c3.get("cliffs_delta")
        ds = sp.get("cliffs_delta")
        c3conf = c3.get("confirmed")
        spconf = sp.get("confirmed")
        if c3.get("verdict") == "inconclusive" or sp.get("verdict") == "inconclusive":
            agree = "INCONCLUSIVE"
        else:
            agree = "yes" if c3conf == spconf else "no"
        lines.append(
            f"| {era} | "
            f"{fmt(d3, '{:+.3f}')} | {fmt(ds, '{:+.3f}')} | "
            f"{fmt(c3.get('p_value'))} | {fmt(sp.get('p_value'))} | "
            f"{agree} |")
    lines.append("")

    # --- §4.11 Ch1 secondary companions + NaN-fraction ---
    lines.append("## §4.11 Channel 1 secondary companions + NaN-fraction contrast")
    lines.append("")
    lines.append(
        "Per §4.11: parallel Mann-Whitney on `stress_post_peak_drop_avg` "
        "(Ch1 secondary aggregate) and `stress_recovery_pct_within_2h` "
        "(direct rate-of-recovery metric). The Ch1 NaN-fraction "
        "descriptive contrast (heavy-T vs non-heavy-T) is the alternative "
        "to the §4.5 1080-min encoding; per §7.2 the unmedicated baseline "
        "shows these are essentially tied at ~18% — companion reported "
        "anyway as the encoding-fragility check.")
    lines.append("")
    lines.append(
        "| companion | era | n_heavy | n_non | Cliff's δ | p-value | confirmed |")
    lines.append(
        "|---|---|---:|---:|---:|---:|:---:|")
    for label, table in (
        ("drop_avg", results["ch1_dropavg_per_era"]),
        ("recovery_pct_within_2h", results["ch1_recpct_per_era"]),
    ):
        for era in ("train", "validate"):
            cell = table[era]
            if cell.get("verdict") == "inconclusive":
                lines.append(
                    f"| {label} | {era} | {cell['n_heavy']} | "
                    f"{cell['n_non_heavy']} | — | — | INCONCLUSIVE |")
                continue
            lines.append(
                f"| {label} | {era} | {cell['n_heavy']} | "
                f"{cell['n_non_heavy']} | "
                f"{cell['cliffs_delta']:+.3f} | "
                f"{cell['p_value']:.4f} | "
                f"{'✓' if cell['confirmed'] else '✗'} |")
    lines.append("")
    lines.append("### Ch1 NaN-fraction contrast (heavy-T vs non-heavy-T)")
    lines.append("")
    lines.append(
        "| era | heavy-T NaN frac | non-heavy-T NaN frac | pp contrast |")
    lines.append(
        "|---|---|---|---:|")
    for era in ("train", "validate"):
        c = results["nan_frac_contrast"][era]
        h_frac = c["heavy_nan_frac"]
        n_frac = c["non_heavy_nan_frac"]
        pp = c["pp_contrast"]
        h_str = f"{h_frac:.4f} ({c['heavy_nan']}/{c['heavy_n']})" if not math.isnan(h_frac) else "NA"
        n_str = f"{n_frac:.4f} ({c['non_heavy_nan']}/{c['non_heavy_n']})" if not math.isnan(n_frac) else "NA"
        lines.append(
            f"| {era} | {h_str} | {n_str} | "
            f"{fmt(pp, '{:+.2f}')} |")
    lines.append("")
    lines.append(
        "Per §4.11: if heavy-T NaN fraction is > 10 pp higher than "
        "non-heavy-T, that is direct C4-positive descriptive evidence "
        "independent of the 1080-encoded Mann-Whitney result. Per §7.2 "
        "the unmedicated baseline is essentially tied — the directional "
        "signal (if any) comes from the non-NaN distribution shift.")
    lines.append("")

    # --- §4.9 E[L]* companion ---
    lines.append("## §4.9 Data-driven E[L]* companion (factor-of-2 flag)")
    lines.append("")
    lines.append(
        "Per §4.9 + audit L3.1 closure: data-driven `E[L]*` "
        "(Politis-White automatic block-length, Patton-Politis-White "
        "correction for the stationary bootstrap) computed on BOTH "
        "(a) each channel's value series AND (b) the heavy-T label "
        "sequence. Flag fires if `|E[L]* − 7| / 7 > 0.5` on either. "
        "**Per the methodology MD, the flag is verdict-relevant only on "
        "SUPPORTED verdicts; for PARTIAL or REJECTED, the flag is "
        "descriptive context only.**")
    lines.append("")
    flag_summary = (
        "**verdict-relevant flag fires**" if results["el_flag_fires_for_verdict"]
        else (
            "no verdict-relevant flag (any flag below is descriptive only)"
            if results["el_any_flag"]
            else "no flags"
        )
    )
    lines.append(
        f"Triad verdict: **{verdict_label}**. Flag status: {flag_summary}.")
    lines.append("")
    lines.append(
        "| channel | era | E[L]* on values | flag (values) | "
        "E[L]* on labels | flag (labels) |")
    lines.append(
        "|---|---|---:|:---:|---:|:---:|")
    for ch in ("Ch1", "Ch2", "Ch3"):
        for era in ("train", "validate"):
            r = results["el_star"][ch][era]
            v = r["values"]
            l_ = r["labels"]
            lines.append(
                f"| {ch} | {era} | {v['optimal_block_length']:.2f} | "
                f"{'**FLAG**' if v['flagged_deviation'] else 'ok'} | "
                f"{l_['optimal_block_length']:.2f} | "
                f"{'**FLAG**' if l_['flagged_deviation'] else 'ok'} |")
    lines.append("")

    # --- Sister-test cross-reference ---
    lines.append("## Sister-test cross-reference")
    lines.append("")
    lines.append(
        "| hypothesis | status | one-line note |")
    lines.append(
        "|---|---|---|")
    lines.append(
        "| HA-C4b v3 | NOT-SUPPORTED (2026-06-17) | motion-filter "
        "crash-precursor framing; (a)=40%, (b)=−10pp, (c)=+1.21 |")
    lines.append(
        "| HA11 | SUPPORTED on train (+22.8 pp) | U-dip sister channel "
        "(calm-day signal); validate inconclusive on the original spec |")
    lines.append("")
    lines.append(
        "Per §9 cross-references: **HA-C4 SUPPORTED + HA-C4b NOT-SUPPORTED** "
        "supports the protective-rather-than-predictive reading from "
        "HA-C4b §9 (the Wiggers pattern IS real on this corpus, but the "
        "participant's real-time use of it as a pacing trigger prevents the "
        "crashes the precursor test would have caught). **HA-C4 REJECTED + "
        "HA-C4b NOT-SUPPORTED + HA11 SUPPORTED** would mean the Wiggers C4 "
        "framework doesn't operationalise cleanly on this corpus at either "
        "the descriptive or precursor level, but the U-dip (HA11) sister "
        "channel does — C4 mechanism would need different operationalisation "
        "(e.g. bout-level recovery curves) to be testable.")
    lines.append("")

    # --- §8 Caveats (verbatim per spec) ---
    lines.append("## §8 Caveats")
    lines.append("")
    lines.append(
        "- **Power-calc dispatch**: power calculation is inapplicable per "
        "[Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) "
        "within-subject design — the n-of-1 corpus does not have separate "
        "treatment and control arms in the classical sense. The "
        "block-permutation null at E[L]=7 (§4.9) is the within-subject "
        "inferential machinery; the §5.1 (a) + (b) gates determine "
        "per-channel confirmation rather than a power-thresholded p-value.")
    lines.append(
        "- **NaN-as-positive encoding for Channel 1** (§4.5): the 1080-min "
        "coding is one operationalisation; the NaN-fraction descriptive "
        "contrast (table above) is the alternative. If the verdict depends "
        "on the encoding choice, flag as encoding-fragile. Per §7.2 the "
        "unmedicated baseline shows essentially tied NaN fractions across "
        "arms (~18% both), so the encoding's impact on the Mann-Whitney "
        "verdict is small.")
    lines.append(
        "- **Chained-regime adjustment for Channel 3** (§4.7): "
        "heavy-T-followed-by-heavy-T+1 days are excluded from the Channel 3 "
        "primary arm. The n-loss is reflected in Ch3's n_heavy count above "
        "(lower than Ch1/Ch2 by the chain-T+1-exclusion count + the T+1 "
        "NaN drop).")
    lines.append(
        "- **Citalopram dose-modulation** (§4.4): the primary scope is "
        "unmedicated only specifically to avoid the dose-confound on the "
        "stress channel "
        "([`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) "
        "shows β = +0.57/mg on `all_day_stress_avg`; +0.43/mg on "
        "`stress_mean_sleep`). Cross-phase sensitivity arms are not run "
        "in this v1 — that scope is queued.")
    lines.append(
        "- **No motion filter** (unlike HA-C4b): HA-C4 tests "
        "`awake_stress_avg`, `stress_high_duration_min`, and "
        "`stress_post_peak_time_to_rest_min` without conditioning on "
        "motion. Garmin stress is partly motion-sensitive per "
        "[`hrv_proxy_via_stress.md`](../../../methodology/hrv_proxy_via_stress.md). "
        "Some channel signal may be motion-artefact rather than true "
        "sympathetic load; cross-reference HA-C4b's motion-filter result.")
    lines.append(
        "- **Unmedicated = pre-citalopram corpus, not 'no medication "
        "overall'**: participant had other lived-experience interventions "
        "in the 2022-04 → 2024-04 window (CPAP started 2024-01-10; "
        "ergotherapy 2022-06-17 → 2023-03-10; PWC reintegratie 2023-03-06 "
        "→ 2023-11-28). The unmedicated headline is 'no SSRI' not 'no "
        "intervention'.")
    lines.append(
        "- **Pacing-behaviour confounder** (inherited from HA-C4b v3 §8): "
        "`exertion_class_lagged_lcera` captures physical exertion only. "
        "Cognitive, emotional, and orthostatic exertion are not in the "
        "classification. A 'non-heavy-T' day in this test could include "
        "high cognitive / emotional load days that are physiologically "
        "demanding. Mis-classifying them as non-heavy-T arm would dilute "
        "the contrast (directional bias toward false-NOT-SUPPORTED).")
    lines.append(
        "- **Single-subject n=1**: thresholds in §5.1 (p < 0.05, |δ| > "
        "0.20) are calibrated to the participant's distribution. The "
        "Mann-Whitney is non-parametric so the threshold-on-effect-size "
        "choice is the binding decision; a stricter Cliff's δ threshold "
        "(e.g. 0.33 for 'medium' effect) would shift the gate.")
    lines.append(
        "- **HA11 / HA-C4b cross-references**: see sister-test table above.")
    lines.append(
        "- **Block-permutation null preserves the heavy-T autocorrelation "
        "structure but breaks the heavy-T → channel relationship**: "
        "under the null, the heavy-T labels are reshuffled in blocks while "
        "channel values stay fixed; this tests \"is the observed difference "
        "larger than what random block-permutation produces?\" The empirical "
        "p-value is the appropriate within-subject inferential statistic.")
    lines.append(
        "- **Block-permutation under stationary bootstrap of labels**: "
        "the bootstrap does not preserve the marginal n_heavy count "
        "(observed mean n_heavy_null is reported in `result-data.json` per "
        "cell). U-statistic comparison across slightly drifting label "
        "counts is per spec §4.8 step 3 + §4.9 step 4; at B = "
        f"{B_HEADLINE} the empirical-p noise from this shift is small.")
    lines.append("")

    # --- Provenance footer ---
    lines.append("---")
    lines.append("")
    lines.append(
        f"*test.py run with `RANDOM_SEED = {RANDOM_SEED}`, "
        f"`BOOTSTRAP_E_L = {BOOTSTRAP_E_L}`, B = {B_HEADLINE} draws per "
        f"cell. Source data: `per_day_master.csv` from "
        f"`$GEVOELSCORE_DATA_PATH`. Spec commit: `{V1_SPEC_COMMIT}`. "
        f"`result-data.json` is the machine-readable companion (gitignored "
        f"per `docs/research/**/*.json`).*")
    OUT_RESULT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {OUT_RESULT_MD}", file=sys.stderr)


def write_result_json(results: dict) -> None:
    def jsonify(o):
        if isinstance(o, dict):
            return {k: jsonify(v) for k, v in o.items()}
        if isinstance(o, list):
            return [jsonify(v) for v in o]
        if isinstance(o, tuple):
            return [jsonify(v) for v in o]
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            v = float(o)
            return None if math.isnan(v) else v
        if isinstance(o, np.ndarray):
            return [jsonify(v) for v in o.tolist()]
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, float) and math.isnan(o):
            return None
        if isinstance(o, (str, int, bool)) or o is None:
            return o
        if isinstance(o, float):
            return o
        # Fallback: try to JSON-encode via str()
        return str(o)
    OUT_RESULT_JSON.write_text(
        json.dumps(jsonify(results), indent=2),
        encoding="utf-8")
    print(f"Wrote {OUT_RESULT_JSON}", file=sys.stderr)


# === main ===============================================================

def main() -> None:
    parser = argparse.ArgumentParser(description="HA-C4 v1 test driver.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run spec 10.4 step 1 dry-run only.")
    args = parser.parse_args()

    print(f"Loading master from {MASTER_CSV}...", file=sys.stderr)
    master = load_master()
    print(f"  {len(master)} day-rows loaded.", file=sys.stderr)

    dry = dry_run(master)
    write_dry_run_report(dry)

    if args.dry_run:
        sys.exit(1 if dry["verdict"] == "HALT" else 0)

    if dry["verdict"] == "HALT":
        print("\nDry-run sanity gates FAILED; refusing to run full test.",
              file=sys.stderr)
        print("See dry-run-report.md for failure analysis + v2 recommendation.",
              file=sys.stderr)
        sys.exit(1)

    print("\nDry-run sanity gates PASSED; running full test...", file=sys.stderr)
    results = run_full(master, dry)
    write_result_md(results)
    write_result_json(results)


if __name__ == "__main__":
    main()
