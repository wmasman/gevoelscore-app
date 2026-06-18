"""HA-C4 v2 - Stage 2: 3-channel Wiggers C4 confirmatory triad test
(INCONCLUSIVE-aware verdict, chain-relaxed Ch3 validate sensitivity arm).

Implements the LOCKED HA-C4 v2 r2 pre-registration (hypothesis.md
LOCKED 2026-06-18 by user acceptance). Tests Wiggers C4 "stress fails to
drop during rest periods after overexertion / stuck sympathetic" via a
3-channel confirmatory triad: Channel 1 (same-day decay failure,
stress_post_peak_time_to_rest_min on T, NaN -> 1080 per spec 4.5);
Channel 2 (walls of orange, stress_high_duration_min on T); Channel 3
(t+1 reactivity, awake_stress_avg on T+1 with chain-T+1 exclusion per
spec 4.7).

Per channel x per era (train, validate): Mann-Whitney U + Cliff's delta
+ block-permutation null at E[L]=7 (B=10,000). Per v2 spec 5.1, 5.2, 5.3:
3-state per-cell verdict (SUPPORTED / REFUTED / INCONCLUSIVE);
per-channel aggregation CONFIRMED (1.0) / CONFIRMED-PARTIAL (0.5) /
REFUTED (0); triad sum bands 3.0=SUPPORTED strong, 2.0-2.5=SUPPORTED,
1.0-1.5=PARTIAL, <1.0=REJECTED.

v2 deltas from v1 (test.py-level):
  - INCONCLUSIVE-aware aggregation per spec 5.3 (replaces v1's binary
    confirmed/not-confirmed labels).
  - dry-run gate 2 routes sub-30 cells to INCONCLUSIVE per spec 5.4
    (NOT halt); only gates 1 + 3 still HALT on failure.
  - spec 4.11.3 chain-relaxed Ch3 validate sensitivity arm: re-compute
    the Ch3 validate cell with the spec 4.7 chain-T+1 exclusion relaxed
    for the heavy-T arm only (n=41 vs primary n=25). Non-heavy-T arm is
    byte-identical to primary. Descriptive only; does NOT modify the
    spec 5.3 verdict.
  - spec 5.5 Holm fewer-comparisons disclosure: when a cell is
    INCONCLUSIVE, the per-era Holm step-down operates on fewer
    comparisons (e.g. 2-of-2); result.md Holm column annotates this
    explicitly.
  - RANDOM_SEED = 20260618 (v2 seed; distinct from v1's 20260617).

Modes:
  python test.py --dry-run    print spec 7.5 sanity gates only.
                              Halt on gate 1 (full-pool median outside
                              +/-30%% of spec 7.1) OR gate 3 (Ch1 NaN
                              fraction outside [12%%, 25%%]); sub-30
                              cells reported as INCONCLUSIVE (no halt).
  python test.py              dry-run first (gates on sanity, halt only
                              on gates 1 or 3); then full run emits
                              result.md + result-data.json.

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

# === Constants per locked v2 hypothesis.md ==============================

# Random seed and bootstrap config (spec 4.9 + 10.2)
# v2 seed: distinct from v1's 20260617 to keep null distributions
# independently reproducible.
RANDOM_SEED = 20260618
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

# Spec 7.5 sanity gate (+/-30% of spec 7.1 reference; from v1 r2 audit)
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
V2_SPEC_COMMIT = "(unmerged-working-tree)"

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

    Per spec 4.11.3 (v2 NEW): channel_key 'Ch3_chain_relaxed' uses CH3_COL
    on T+1 but does NOT apply the spec 4.7 chain-T+1 exclusion for the
    heavy-T arm. Non-heavy-T arm is byte-identical to Ch3 primary (the
    chain rule was always heavy-T-only by construction). Descriptive
    sensitivity only; does NOT modify the spec 5.3 verdict per spec
    4.11.3 reporting rule.
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
        elif channel_key == "Ch3_chain_relaxed":
            # spec 4.11.3 (v2): identical to Ch3 EXCEPT the chain-T+1
            # exclusion is NOT applied for the heavy-T arm. The
            # non-heavy-T arm is naturally byte-identical to Ch3 primary
            # because the spec 4.7 chain rule never excluded non-heavy-T
            # days (the rule is "EXCLUDE heavy-T days T where T+1 is
            # heavy").
            d1 = d + timedelta(days=1)
            # NO chain-T+1 exclusion for heavy-T arm here.
            # spec 4.3 rule 4: T+1 must be in unmed + not in April cluster
            if not in_unmedicated_lc(d1):
                continue
            v = parse_float((master.get(d1) or {}).get(CH3_COL, ""))
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


# === Per-cell evaluation (spec 5.1 + v2 5.3 3-state verdict) ============

def evaluate_channel_era(channel_key: str, era: str, master,
                          rng: np.random.Generator,
                          B: int = B_HEADLINE,
                          crash_drop: bool = False) -> dict:
    """Compute U + Cliff's delta + block-permutation p for (channel, era).

    Returns dict with 'verdict' in {'supported', 'refuted', 'inconclusive'}
    per v2 spec 5.1 + 5.3:
      - 'inconclusive': either arm n < MIN_ARM_N (sample-size shortfall).
      - 'supported':    n >= MIN_ARM_N both arms AND p < P_BAR AND
                        Cliff's delta > +CLIFF_BAR.
      - 'refuted':      n >= MIN_ARM_N both arms AND (p >= P_BAR OR
                        Cliff's delta <= +CLIFF_BAR or wrong direction).
    """
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
    # spec 5.1: cell SUPPORTED iff p < 0.05 AND delta > +0.20 in
    # predicted direction. Else REFUTED.
    discrimination_pass = p_info["p_value"] < P_BAR
    effect_size_pass = delta > CLIFF_BAR
    supported = discrimination_pass and effect_size_pass
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
        "supported": supported,
        "verdict": "supported" if supported else "refuted",
    })
    return out


# === Per-channel aggregation + triad verdict (v2 spec 5.2 + 5.3) ========

def aggregate_channel(train_cell: dict, validate_cell: dict) -> dict:
    """Per v2 spec 5.2: aggregate two per-era cells into a per-channel
    verdict and contribution.

    - CONFIRMED (1.0): SUPPORTED in BOTH eras.
    - CONFIRMED-PARTIAL (0.5): SUPPORTED in ONE era AND INCONCLUSIVE in
      the OTHER era. (SUPPORTED + REFUTED still = REFUTED, NOT
      CONFIRMED-PARTIAL.)
    - REFUTED (0): any other combination (both REFUTED; SUPPORTED +
      REFUTED; both INCONCLUSIVE; REFUTED + INCONCLUSIVE).
    """
    t = train_cell.get("verdict")
    v = validate_cell.get("verdict")
    if t == "supported" and v == "supported":
        return {
            "channel_verdict": "CONFIRMED",
            "contribution": 1.0,
            "label": "CONFIRMED (supported both eras)",
            "train_verdict": t, "validate_verdict": v,
        }
    if (t == "supported" and v == "inconclusive") or \
       (t == "inconclusive" and v == "supported"):
        which = "train" if t == "supported" else "validate"
        return {
            "channel_verdict": "CONFIRMED-PARTIAL",
            "contribution": 0.5,
            "label": (f"CONFIRMED-PARTIAL (supported {which}, "
                      f"inconclusive other era)"),
            "train_verdict": t, "validate_verdict": v,
        }
    # All other combinations = REFUTED.
    if t == "inconclusive" and v == "inconclusive":
        label = "REFUTED (inconclusive both eras)"
    elif t == "inconclusive" or v == "inconclusive":
        label = "REFUTED (one era refuted, other inconclusive)"
    elif t == "supported" or v == "supported":
        label = "REFUTED (supported one era, refuted other)"
    else:
        label = "REFUTED (refuted both eras)"
    return {
        "channel_verdict": "REFUTED",
        "contribution": 0.0,
        "label": label,
        "train_verdict": t, "validate_verdict": v,
    }


def triad_verdict(per_channel_per_era: dict) -> dict:
    """v2 spec 5.3: 3-state per-channel aggregation + triad sum bands.

    Bands:
      - 3.0       -> SUPPORTED (strong)
      - 2.0, 2.5  -> SUPPORTED
      - 1.0, 1.5  -> PARTIAL
      - < 1.0     -> REJECTED
    """
    score = 0.0
    breakdown: dict[str, dict] = {}
    for ch in ("Ch1", "Ch2", "Ch3"):
        train_cell = per_channel_per_era[ch].get("train", {})
        validate_cell = per_channel_per_era[ch].get("validate", {})
        agg = aggregate_channel(train_cell, validate_cell)
        breakdown[ch] = agg
        score += agg["contribution"]
    # v2 spec 5.3 bands
    if score >= 3.0:
        verdict, strength = "SUPPORTED", "strong (3-of-3 channels CONFIRMED both eras)"
    elif score >= 2.0:
        verdict, strength = "SUPPORTED", "clears triad bar"
    elif score >= 1.0:
        verdict, strength = "PARTIAL", "partial signal"
    else:
        verdict, strength = "REJECTED", "no triad signal"
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
    """Run v2 spec 7.5 sanity-gate checks.

    Returns dict with 'verdict' in {'PASS', 'HALT'} per v2 7.5 routing:
      - Gate 1 (full-pool median +/-30%): FAIL -> HALT.
      - Gate 2 (per-channel x per-era arm sizes >= 30): FAIL -> route
        cell to INCONCLUSIVE per v2 spec 5.4 + 5.3 (NOT halt).
      - Gate 3 (Ch1 NaN fraction in [12%, 25%]): FAIL -> HALT.

    Sub-30 cells DO NOT halt the test (v2 disposition of v1 halt
    condition); only distribution-sanity failures (gates 1, 3) halt.
    """
    print("\n=== HA-C4 v2 dry-run ===\n")
    print("(headline cell: unmedicated x {Ch1, Ch2, Ch3} x heavy-T-vs-non-heavy-T")
    print(" x Mann-Whitney U + Cliff's delta x block-permutation null E[L]=7")
    print(" x v2 INCONCLUSIVE-aware verdict bands per spec 5.3.)")
    print("(day-validity per spec 4.3: LC era + unmedicated + not April-2024")
    print(" cluster + non-empty exertion classification + channel-value")
    print(" handling per spec 4.5/4.6/4.7.)")
    print("(v2 spec 7.5 routing: gate 1 + gate 3 HALT on failure; gate 2")
    print(" sub-30 cells route to spec 5.4 INCONCLUSIVE per spec 5.3, NOT halt.)")

    sanity_fails: list[str] = []  # only HALT-eligible gate 1 + gate 3
    inconclusive_cells: list[str] = []  # gate 2 sub-30 cells (descriptive)

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
                f"Gate 1: {k} full-pool median = {med:.2f} outside "
                f"[{lo:.2f}, {hi:.2f}] (spec 7.1 ref {ref}, +/-30%%)")

    # --- Gate 2 (v2 routing): per-channel x per-era arm sizes ---
    print("\n--- spec 7.5 gate 2 (v2: sub-30 -> INCONCLUSIVE per spec 5.4, NOT halt) ---")
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
            status = "PASS" if ds["passes_min_arm"] else "INCONCLUSIVE"
            print(f"  {ch} {era:8}: n_heavy={ds['n_heavy']:>4} "
                  f"n_non={ds['n_non_heavy']:>4} "
                  f"-> {status}{extra}")
            if not ds["passes_min_arm"]:
                inconclusive_cells.append(
                    f"{ch} {era}: heavy n={ds['n_heavy']}, "
                    f"non-heavy n={ds['n_non_heavy']} "
                    f"(MIN_ARM_N={MIN_ARM_N}) -> INCONCLUSIVE per spec 5.4"
                )

    # --- v2 spec 4.11.3: chain-relaxed Ch3 validate cell sizes ---
    print("\n--- spec 4.11.3: Ch3 validate chain-relaxed sensitivity cell sizes ---")
    ds_relaxed = build_ch_dataset("Ch3_chain_relaxed", "validate", master)
    ch3_relaxed_sizes = {
        "n_heavy": ds_relaxed["n_heavy"],
        "n_non": ds_relaxed["n_non_heavy"],
        "n_total": ds_relaxed["n_total"],
        "passes": ds_relaxed["passes_min_arm"],
    }
    print(f"  Ch3_chain_relaxed validate: n_heavy={ch3_relaxed_sizes['n_heavy']} "
          f"n_non={ch3_relaxed_sizes['n_non']} -> descriptive only, no verdict bar")

    # --- Gate 3: Ch1 full-pool NaN fraction in [12%, 25%] ---
    print("\n--- spec 7.5 gate 3: Ch1 full-pool NaN fraction in [12%%, 25%%] ---")
    ch1_info = pool_meds["Ch1"]
    nan_frac = (ch1_info["n_nan"] / ch1_info["n_total"]
                if ch1_info["n_total"] else float("nan"))
    lo, hi = CH1_NAN_FRAC_RANGE
    ok = (not math.isnan(nan_frac)) and lo <= nan_frac <= hi
    print(f"  Ch1 NaN fraction = {nan_frac:.4f} "
          f"({ch1_info['n_nan']}/{ch1_info['n_total']}); "
          f"range [{lo}, {hi}] -> {'PASS' if ok else 'FAIL'}")
    if not ok:
        sanity_fails.append(
            f"Gate 3: Ch1 NaN fraction = {nan_frac:.4f} outside [{lo}, {hi}]")

    print("")
    if sanity_fails:
        print(f"--- DRY-RUN VERDICT: HALT ({len(sanity_fails)} HALT-eligible "
              f"failure{'s' if len(sanity_fails) > 1 else ''}) ---")
        for f in sanity_fails:
            print(f"  - {f}")
        print(f"\nPer v2 spec 10.4 step 1 + hypothesis_lock_process.md 3.9: "
              f"DO NOT run the full test. HA-C4-v3 revision required.")
    else:
        print("--- DRY-RUN VERDICT: PASS (proceed with `python test.py`) ---")
        if inconclusive_cells:
            print(f"  Note: {len(inconclusive_cells)} cell(s) flagged INCONCLUSIVE")
            print(f"  per v2 spec 5.4 + 5.3 (NOT halt-triggering):")
            for c in inconclusive_cells:
                print(f"    - {c}")

    return {
        "pool_medians": pool_meds,
        "arm_sizes": arm_sizes,
        "ch3_relaxed_sizes": ch3_relaxed_sizes,
        "ch1_nan_fraction": nan_frac,
        "ch1_nan_count": ch1_info["n_nan"],
        "ch1_pool_total": ch1_info["n_total"],
        "sanity_fails": sanity_fails,
        "inconclusive_cells": inconclusive_cells,
        "verdict": "HALT" if sanity_fails else "PASS",
    }


# === dry-run-report.md emitter ==========================================

def write_dry_run_report(dry: dict) -> None:
    halt = dry["verdict"] == "HALT"
    n_inc = len(dry["inconclusive_cells"])
    if halt:
        title = "HA-C4 v2 dry-run report — SANITY-GATE FAILURE (HALT)"
    elif n_inc:
        title = (f"HA-C4 v2 dry-run report — sanity gates 1 + 3 PASS "
                 f"(gate 2: {n_inc} cell(s) routed to INCONCLUSIVE per spec 5.4)")
    else:
        title = "HA-C4 v2 dry-run report — sanity gates PASS"
    lines: list[str] = [
        f"# {title}",
        "",
        ("Emitted by `test.py --dry-run` per locked v2 hypothesis.md §10.4. "
         "Headline cell: unmedicated × {Ch1, Ch2, Ch3} × "
         "heavy-T-vs-non-heavy-T × Mann-Whitney U + Cliff's δ × "
         "block-permutation null E[L]=7 × v2 INCONCLUSIVE-aware verdict "
         "bands per §5.3. Day-validity per §4.3 (LC era + unmedicated + "
         "not April-2024 cluster + non-empty exertion classification + "
         "channel-value handling per §4.5/§4.6/§4.7)."),
        "",
        ("**v2 disposition of sub-30 cells**: per locked v2 §5.4 + §5.3, "
         "any channel × era cell with n < 30 per arm routes to "
         "INCONCLUSIVE at the per-channel aggregation layer (CONFIRMED-PARTIAL "
         "if the other era is SUPPORTED, else REFUTED). Sub-30 cells DO NOT "
         "halt the test. Only distribution-sanity gates 1 + 3 halt on "
         "failure."),
        "",
    ]
    if halt:
        lines.extend([
            "## §7.5 sanity-gate HALT-eligible failures",
            "",
        ])
        for f in dry["sanity_fails"]:
            lines.append(f"- {f}")
        lines.extend([
            "",
            ("Per v2 §9.6 + §10.4 step 1 + the locked-pre-reg discipline "
             "(`hypothesis_lock_process.md` §3.9), the full test is NOT "
             "run and `result.md` is NOT emitted. The spec must be revised "
             "before any further test run; the revision creates HA-C4-v3 "
             "with v2 archived as v2."),
            "",
        ])

    if dry["inconclusive_cells"]:
        lines.extend([
            "## §7.5 gate 2: cells routed to INCONCLUSIVE (descriptive, not halt)",
            "",
        ])
        for c in dry["inconclusive_cells"]:
            lines.append(f"- {c}")
        lines.append("")

    lines.extend([
        "## §7.5 gate 1: full-pool median (±30% of §7.1 reference)",
        "",
        ("All four anchors computed from `per_day_master.csv` on the "
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
        "## §7.5 gate 2 (v2 routing): per-channel × per-era arm sizes",
        "",
        ("Per v2 §5.4 + §5.3, cells with n < 30 per arm route to "
         "INCONCLUSIVE (NOT halt). v2 §7.3 anchors (chain-T+1-corrected): "
         "Ch1/Ch2 train n=171, validate n=41; Ch3 train n=117 (171 − 54 "
         "chain-dropped), Ch3 validate n=25 (41 − 16 chain-dropped). "
         "Non-heavy-T arms: train n=361, validate n=58."),
        "",
        "| channel | era | n_heavy | n_non_heavy | n_total | gate routing |",
        "|---|---|---:|---:|---:|---|",
    ])
    for ch in ("Ch1", "Ch2", "Ch3"):
        for era in ("train", "validate"):
            info = dry["arm_sizes"][ch][era]
            routing = "PASS" if info["passes"] else "INCONCLUSIVE (per §5.4)"
            lines.append(
                f"| {ch} | {era} | {info['n_heavy']} | {info['n_non']} | "
                f"{info['n_total']} | {routing} |")
    lines.append("")

    # v2 spec 4.11.3 chain-relaxed Ch3 validate cell sizes
    cr = dry["ch3_relaxed_sizes"]
    lines.extend([
        "## §4.11.3 chain-relaxed Ch3 validate sensitivity cell (v2 NEW)",
        "",
        ("Per v2 §4.11.3, descriptive sensitivity arm computing the Ch3 "
         "validate cell with the §4.7 chain-T+1 exclusion **relaxed for "
         "the heavy-T arm only**. Non-heavy-T arm is byte-identical to the "
         "Ch3 primary validate cell (the §4.7 chain rule was always "
         "heavy-T-only by construction). Descriptive only; does NOT modify "
         "the §5.3 verdict per §4.11.3."),
        "",
        f"- Ch3_chain_relaxed validate: n_heavy={cr['n_heavy']}, "
        f"n_non_heavy={cr['n_non']} (expected per §7.3 anchors: "
        f"n_heavy=41, n_non_heavy=58).",
        "",
    ])

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
            ("Per the locked-pre-reg discipline (`hypothesis.md` v2 §10.4 + "
             "§9.6), the spec must be revised before any further test run; "
             "the revision creates HA-C4-v3 with v2 archived. Fresh-session "
             "v3-draft per `hypothesis_lock_process.md` §3.2."),
            "",
        ])
    else:
        lines.extend([
            "## Next step (PASS branch)",
            "",
            ("Sanity gates 1 + 3 passed; the full test runs after the "
             "dry-run inside the same `python test.py` invocation, emitting "
             "`result.md` + `result-data.json`. Per §10.4 step 3: **no "
             "iteration on the spec after the dry-run passes** — any "
             "post-dry-run revision creates HA-C4-v3."),
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


def _holm_per_era_v2(per_channel_per_era: dict, alpha: float = 0.05) -> dict:
    """v2 spec 5.5 Holm step-down per era with INCONCLUSIVE-aware
    fewer-comparisons disclosure.

    INCONCLUSIVE cells are OMITTED from the per-era Holm ordering; the
    Holm n_eff = number of non-INCONCLUSIVE channels in that era. The
    annotation string surfaces the reduced comparison count.
    """
    out: dict[str, dict] = {}
    channels = ("Ch1", "Ch2", "Ch3")
    for era in ("train", "validate"):
        eligible: list[tuple[str, float]] = []
        inconclusive: list[str] = []
        for ch in channels:
            cell = per_channel_per_era[ch].get(era, {})
            if cell.get("verdict") == "inconclusive":
                inconclusive.append(ch)
                continue
            p = cell.get("p_value")
            if p is None or (isinstance(p, float) and math.isnan(p)):
                # Defensive: missing p falls back to 1.0
                eligible.append((ch, 1.0))
            else:
                eligible.append((ch, float(p)))
        if not eligible:
            out[era] = {
                "channels_included": [],
                "channels_inconclusive": inconclusive,
                "n_eff": 0,
                "raw_p_values": {},
                "adjusted_p_values": {},
                "rejected": {},
                "annotation": (
                    "Holm (0-of-3 comparisons; all channels INCONCLUSIVE)"),
            }
            continue
        ps_arr = np.asarray([p for _, p in eligible], dtype=float)
        n_eff = len(eligible)
        h = holm_step_down(ps_arr, n_eff=n_eff, alpha=alpha)
        raw_p = {ch: float(p) for ch, p in eligible}
        adj_p = {eligible[i][0]: float(h["adjusted_p_values"][i])
                 for i in range(n_eff)}
        rejected = {eligible[i][0]: bool(h["rejected"][i])
                    for i in range(n_eff)}
        if inconclusive:
            annotation = (
                f"Holm ({n_eff}-of-{n_eff} comparisons; "
                f"{', '.join(f'{c} INCONCLUSIVE' for c in inconclusive)})"
            )
        else:
            annotation = f"Holm (3-of-3 comparisons)"
        out[era] = {
            "channels_included": [ch for ch, _ in eligible],
            "channels_inconclusive": inconclusive,
            "n_eff": int(h["n_eff_used"]),
            "raw_p_values": raw_p,
            "adjusted_p_values": adj_p,
            "rejected": rejected,
            "annotation": annotation,
        }
    return out


def run_full(master, dry: dict) -> dict:
    rng = np.random.default_rng(RANDOM_SEED)

    # --- Primary per-channel x per-era ---
    print("\n=== HA-C4 v2 full run ===\n", file=sys.stderr)
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
                print(f"    -> verdict={cell['verdict']} "
                      f"delta={cell['cliffs_delta']:+.3f} "
                      f"p={cell['p_value']:.4f}", file=sys.stderr)

    # --- Triad verdict (v2 spec 5.3) ---
    triad = triad_verdict(per_channel_per_era)
    print(f"\n  TRIAD: score={triad['score']} verdict={triad['verdict']} "
          f"({triad['strength']})", file=sys.stderr)
    for ch in ("Ch1", "Ch2", "Ch3"):
        b = triad["breakdown"][ch]
        print(f"    {ch}: {b['channel_verdict']} ({b['contribution']}) - {b['label']}",
              file=sys.stderr)

    # --- Holm step-down per era (v2 spec 5.5 fewer-comparisons aware) ---
    holm_per_era = _holm_per_era_v2(per_channel_per_era, alpha=0.05)

    # --- v2 spec 4.11.3 chain-relaxed Ch3 validate sensitivity arm ---
    print("\n  --- v2 spec 4.11.3 chain-relaxed Ch3 validate ---", file=sys.stderr)
    ch3_chain_relaxed_validate = evaluate_channel_era(
        "Ch3_chain_relaxed", "validate", master, rng, B=B_HEADLINE)
    crv = ch3_chain_relaxed_validate
    if crv.get("verdict") == "inconclusive":
        print(f"    -> INCONCLUSIVE (n_heavy={crv['n_heavy']}, "
              f"n_non={crv['n_non_heavy']})", file=sys.stderr)
    else:
        print(f"    -> verdict={crv['verdict']} "
              f"delta={crv['cliffs_delta']:+.3f} p={crv['p_value']:.4f}",
              file=sys.stderr)

    # --- §4.11.1 crash-drop sensitivity arm ---
    print("\n  --- spec 4.11.1 crash-drop sensitivity ---", file=sys.stderr)
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
    print("\n  --- spec 4.11.2 Ch3 spike companion ---", file=sys.stderr)
    ch3_spike_per_era: dict[str, dict] = {}
    for era in ("train", "validate"):
        print(f"  evaluating Ch3_spike_companion {era}...", file=sys.stderr)
        ch3_spike_per_era[era] = evaluate_channel_era(
            "Ch3_spike_companion", era, master, rng, B=B_HEADLINE)

    # --- §4.11 other companions ---
    print("\n  --- spec 4.11 Ch1 secondary companions (drop_avg, recovery_pct) ---",
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
    print("\n  --- spec 4.9 data-driven E[L]* companion ---", file=sys.stderr)
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
        "spec_commit": V2_SPEC_COMMIT,
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
        "ch3_chain_relaxed_validate": ch3_chain_relaxed_validate,
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


def _cell_glyph(cell: dict) -> str:
    v = cell.get("verdict")
    if v == "supported":
        return "SUPPORTED"
    if v == "refuted":
        return "REFUTED"
    if v == "inconclusive":
        return "INCONCLUSIVE"
    return "NA"


def write_result_md(results: dict) -> None:
    triad = results["triad"]
    pcpe = results["per_channel_per_era"]
    verdict_label = triad["verdict"]
    score = triad["score"]
    strength = triad["strength"]
    lines: list[str] = []

    lines.append(
        f"# HA-C4 v2 — RESULT: {verdict_label} (triad sum = {score} / 3.0)")
    lines.append("")
    lines.append(
        f"Emitted by `test.py` per locked v2 hypothesis.md §10.3. "
        f"**Headline cell**: unmedicated × {{Ch1, Ch2, Ch3}} × "
        f"heavy-T-vs-non-heavy-T × Mann-Whitney U + Cliff's δ × "
        f"block-permutation null E[L]=7 × v2 §5.3 INCONCLUSIVE-aware "
        f"triad verdict bands. **Random seed**: "
        f"`RANDOM_SEED = {RANDOM_SEED}`; **B** = {B_HEADLINE} bootstrap "
        f"draws per cell. **Strength**: {strength}.")
    lines.append("")

    # --- v2-specific caveats prominent at top (per §8 v2 caveats) ---
    lines.append("## v2-specific caveats (prominent per §10.3 + §8)")
    lines.append("")
    lines.append(
        "1. **v1 → v2 transition disclosure**: v1 (LOCKED 2026-06-17 r2 "
        "commit `da79387`) was dry-run-halted on Ch3 validate n=25 < 30 "
        "(per §4.7 chain-T+1 exclusion dropping 16 of 41 validate heavy-T "
        "days); v1 §5.3 had no explicit INCONCLUSIVE-handling rule so the "
        "cell broke the binary triad logic. **v2 §5.3 introduces explicit "
        "handling**: INCONCLUSIVE cells contribute 0.5 (CONFIRMED-PARTIAL) "
        "at the per-channel aggregation layer when the OTHER era is "
        "SUPPORTED, blocking full credit but not refuting. The Wiggers "
        "3-channel triad structure is preserved; Ch3 is NOT dropped from "
        "the triad. The v1 halt was the locked-pre-reg discipline working "
        "exactly as designed; v2 is the corrective draft.")
    lines.append("")
    lines.append(
        "2. **§7.3 arithmetic spec-bug fix (honest disclosure)**: v1 §7.3 "
        "implicitly assumed the 35-day pre-train buffer (Apr–Aug 2022 "
        "unmedicated heavy-T days) was already excluded from the heavy-T "
        "count; it asserted train heavy-T n = 206 when the correct value "
        "is n = 171. v2 §7.3 corrects this AND adds the per-channel "
        "chain-T+1 decomposition (Ch3 train n=117, Ch3 validate n=25). "
        "The bug-fix does NOT change the v1 halt verdict (the binding "
        "§7.5 gate-2 failure was on Ch3 validate, not on train Ch1/Ch2 at "
        "the corrected n=171, which comfortably clears the ≥30 bar).")
    lines.append("")
    lines.append(
        "3. **§4.11.3 sensitivity arm framing (chain-T+1 relaxation)**: "
        "the v2 §4.11.3 chain-relaxed Ch3 validate cell (n=41) is "
        "**descriptive sensitivity only**; it does NOT promote to the "
        "primary verdict. The §4.7 chain-T+1 rule is preserved for the "
        "headline because asymmetric chain-discipline (relaxing for "
        "validate only) is methodologically awkward as a primary. The "
        "reader sees what the cell would look like without the chain "
        "rule, but the primary verdict honors the chain rule.")
    lines.append("")
    lines.append(
        "4. **Audit Layer-2.5 v2 disposition (pragmatic pre-registration "
        "acknowledgment)**: v2 was drafted with knowledge that Ch3 "
        "validate has the n=25 boundary issue + Ch3 train passes at "
        "n=117. The triage analysis (which option to choose from the five "
        "identified in the v1 dry-run report) was done in a separate "
        "fresh session per `hypothesis_lock_process.md` §3.2; this "
        "drafting session was given only the composite-path recommendation "
        "and no per-day data values from the v1 test (the v1 full run "
        "never executed because of the halt). The §3.2-clause "
        "shared-context concern from v1 r2 (user-accepted as priced-in "
        "per audit L2.5 disposition) remains the documented boundary; v2 "
        "does not introduce new exposure to per-day per-channel values. "
        "Per L2.5 lock-stage call, the v1 r2 priced-in disposition "
        "carries forward to v2.")
    lines.append("")
    lines.append(
        "5. **L4.5 minor inherited carry-forward (Ch3 mean-vs-spike)**: "
        "the v2 audit flagged that Channel 3's `awake_stress_avg` is a "
        "mean while the Wiggers wording (\"stress spikes much faster\") "
        "suggests a spike-reading; the §4.11.2 spike-companion "
        "(`stress_high_duration_min` on T+1) is the descriptive "
        "companion. If the primary Ch3 and spike-companion diverge, "
        "the divergence is informative for §9 interpretation.")
    lines.append("")

    # --- Data-exposure context preserved from v1 ---
    lines.append("## Data-exposure context (inherited from v1 §Authorship)")
    lines.append("")
    lines.append(
        "HA-C4 v1 r2 was drafted, audited (fresh-session, verdict "
        "`REVISION RECOMMENDED`), revised, and **LOCKED 2026-06-17 by "
        "user acceptance** in a session that had already executed sister "
        "test HA-C4b (v1 → v2 → v3, NOT-SUPPORTED). The v1 drafter knew "
        "the identity of 10 unmedicated heavy-T crash days, but NOT the "
        "per-day per-channel values for the HA-C4 channels (different "
        "aggregations of the same underlying monitoring_b data). The "
        "fresh-session v1 audit verified no operational choices in §4 / "
        "§5 were biased by knowledge of the 10 crash-day identities; the "
        "L2.5 substantive concern was **priced-in by user acceptance**. "
        "The §4.11.1 crash-drop sensitivity arm (added v1 r2) further "
        "insulates the spec; readings reported below. **v2 drafted "
        "2026-06-18 fresh-session**, audited fresh-session "
        "(PASS-with-caveats), and **LOCKED 2026-06-18 by user "
        "acceptance** at r2.")
    lines.append("")
    lines.append(
        "**Test execution session**: this `test.py` was implemented and "
        "run in a FRESH Claude session per the locked-pre-reg discipline. "
        "The session received only the LOCKED v2 spec + the v1 archive + "
        "the dry-run-report cell counts + the audit reports — not the "
        "per-day per-channel values, which become visible only when "
        "test.py executes.")
    lines.append("")

    # --- §7.5 sanity-gate compliance summary ---
    lines.append("## §7.5 sanity-gate compliance (top-of-report, v2 routing)")
    lines.append("")
    n_inc_dry = len(results["sanity"]["inconclusive_cells"])
    lines.append(
        f"Gates 1 + 3 (HALT-eligible) passed at dry-run. Gate 2 (sub-30 "
        f"cells per arm) flagged {n_inc_dry} cell(s) as INCONCLUSIVE per "
        f"v2 §5.4 + §5.3 (not halt). See `dry-run-report.md` for per-gate "
        f"detail.")
    lines.append("")
    lines.append("| gate | result | v2 routing |")
    lines.append("|---|---|---|")
    lines.append(
        "| Full-pool median within ±30% of §7.1 (×4 channels) | PASS | "
        "halt on failure |")
    lines.append(
        f"| Per-channel × per-era arm sizes ≥ 30 (×6 cells) | "
        f"{6 - n_inc_dry} PASS / {n_inc_dry} INCONCLUSIVE | "
        f"sub-30 → §5.4 INCONCLUSIVE (not halt) |")
    lines.append(
        f"| Ch1 NaN fraction in [12%, 25%] | PASS (observed "
        f"{results['sanity']['ch1_nan_fraction']:.4f}) | halt on failure |")
    lines.append("")

    # --- Triad verdict block ---
    lines.append("## §5.3 triad verdict (v2 INCONCLUSIVE-aware bands)")
    lines.append("")
    lines.append(
        f"**Verdict: {verdict_label}** "
        f"(triad sum = {score} of 3.0; {strength}).")
    lines.append("")
    lines.append(
        "| channel | train | validate | channel verdict | contribution | label |")
    lines.append(
        "|---|---|---|---|---:|---|")
    for ch in ("Ch1", "Ch2", "Ch3"):
        b = triad["breakdown"][ch]
        t_lbl = {"supported": "SUPPORTED", "refuted": "REFUTED",
                 "inconclusive": "INCONCLUSIVE"}.get(b["train_verdict"], "NA")
        v_lbl = {"supported": "SUPPORTED", "refuted": "REFUTED",
                 "inconclusive": "INCONCLUSIVE"}.get(b["validate_verdict"], "NA")
        lines.append(
            f"| {ch} | {t_lbl} | {v_lbl} | {b['channel_verdict']} | "
            f"{b['contribution']} | {b['label']} |")
    lines.append("")
    lines.append(
        "Per v2 §5.2 + §5.3 scoring rule: CONFIRMED (SUPPORTED both "
        "eras) → 1.0; CONFIRMED-PARTIAL (SUPPORTED one era + "
        "INCONCLUSIVE the other) → 0.5; REFUTED (any other combination, "
        "including SUPPORTED+REFUTED) → 0.0. Triad sum bands: 3.0 → "
        "**SUPPORTED (strong)**; 2.0–2.5 → **SUPPORTED**; 1.0–1.5 → "
        "**PARTIAL**; < 1.0 → **REJECTED**.")
    lines.append("")

    # --- §5.1 + §5.2 per-channel × per-era contingency table ---
    lines.append(
        "## §5.1 + §5.2 per-channel × per-era contingency table (primary)")
    lines.append("")
    lines.append(
        "Per-cell: Mann-Whitney U + Cliff's δ + block-permutation null "
        "at E[L]=7. **(a) discrimination**: empirical p < 0.05. "
        "**(b) effect size**: δ > +0.20 in predicted direction "
        "(heavy-T > non-heavy-T). Channel × era verdict: "
        "**SUPPORTED** iff (a) AND (b); **REFUTED** iff (a) fails or "
        "(b) fails (or wrong direction); **INCONCLUSIVE** iff either "
        "arm n < 30.")
    lines.append("")
    lines.append(
        "| ch | era | n_heavy | n_non | heavy med [p25–p75] | non med [p25–p75] | "
        "Cliff's δ | p-value | (a) | (b) | verdict |")
    lines.append(
        "|---|---|---:|---:|---|---|---:|---:|:---:|:---:|:---:|")
    for ch in ("Ch1", "Ch2", "Ch3"):
        for era in ("train", "validate"):
            cell = pcpe[ch][era]
            if cell.get("verdict") == "inconclusive":
                lines.append(
                    f"| {ch} | {era} | {cell['n_heavy']} | "
                    f"{cell['n_non_heavy']} | — | — | — | — | — | — | "
                    f"INCONCLUSIVE |")
                continue
            heavy_iqr = (f"{cell['heavy_median']:.2f} "
                         f"[{cell['heavy_p25']:.2f}–{cell['heavy_p75']:.2f}]")
            non_iqr = (f"{cell['non_heavy_median']:.2f} "
                       f"[{cell['non_heavy_p25']:.2f}–{cell['non_heavy_p75']:.2f}]")
            lines.append(
                f"| {ch} | {era} | {cell['n_heavy']} | {cell['n_non_heavy']} | "
                f"{heavy_iqr} | {non_iqr} | "
                f"{cell['cliffs_delta']:+.3f} | {cell['p_value']:.4f} | "
                f"{'PASS' if cell['discrimination_pass'] else 'fail'} | "
                f"{'PASS' if cell['effect_size_pass'] else 'fail'} | "
                f"{_cell_glyph(cell)} |")
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

    # --- §4.11.3 chain-relaxed Ch3 validate sensitivity arm (v2 NEW) ---
    lines.append(
        "## §4.11.3 Ch3 validate chain-relaxed sensitivity arm (v2 NEW, descriptive)")
    lines.append("")
    lines.append(
        "Per v2 §4.11.3: re-compute the Ch3 validate cell with the §4.7 "
        "chain-T+1 exclusion **relaxed for the heavy-T arm only** (n=41 "
        "vs primary n=25). Non-heavy-T arm is byte-identical to the "
        "primary (n=58; the §4.7 chain rule was always heavy-T-only by "
        "construction). **Descriptive sensitivity only; does NOT modify "
        "the §5.3 verdict** per §4.11.3 reporting rule.")
    lines.append("")
    crv = results["ch3_chain_relaxed_validate"]
    ch3_primary = pcpe["Ch3"]["validate"]
    primary_delta = ch3_primary.get("cliffs_delta")
    primary_p = ch3_primary.get("p_value")
    primary_verdict_lbl = _cell_glyph(ch3_primary)
    relaxed_verdict_lbl = _cell_glyph(crv)
    lines.append(
        "| variant | n_heavy | n_non | Cliff's δ | p-value | verdict |")
    lines.append(
        "|---|---:|---:|---:|---:|:---:|")
    lines.append(
        f"| Ch3 validate (primary, §4.7 chain applied) | "
        f"{ch3_primary['n_heavy']} | {ch3_primary['n_non_heavy']} | "
        f"{fmt(primary_delta, '{:+.3f}')} | {fmt(primary_p)} | "
        f"{primary_verdict_lbl} |")
    if crv.get("verdict") == "inconclusive":
        lines.append(
            f"| Ch3 validate (chain-relaxed §4.11.3) | "
            f"{crv['n_heavy']} | {crv['n_non_heavy']} | — | — | "
            f"INCONCLUSIVE |")
    else:
        lines.append(
            f"| Ch3 validate (chain-relaxed §4.11.3) | "
            f"{crv['n_heavy']} | {crv['n_non_heavy']} | "
            f"{crv['cliffs_delta']:+.3f} | {crv['p_value']:.4f} | "
            f"{relaxed_verdict_lbl} |")
    lines.append("")
    # Reader rule per §4.11.3
    if (crv.get("verdict") != "inconclusive"
            and ch3_primary.get("verdict") != "inconclusive"):
        agree = (crv.get("verdict") == ch3_primary.get("verdict"))
        agree_str = ("agrees in direction/magnitude" if agree
                     else "diverges from primary")
        lines.append(
            f"**Reading**: chain-relaxed cell {agree_str} with primary "
            f"Ch3 validate. Per §4.11.3, this is descriptive context; "
            f"the §5.3 verdict uses the primary cell's verdict.")
    else:
        # Primary is INCONCLUSIVE (the expected case under v1 cell
        # counts); reading rule is direction-vs-Ch1+Ch2-validate.
        ch1_val = pcpe["Ch1"]["validate"]
        ch2_val = pcpe["Ch2"]["validate"]
        ch1_dir = (ch1_val.get("cliffs_delta") if ch1_val.get("verdict") != "inconclusive"
                   else None)
        ch2_dir = (ch2_val.get("cliffs_delta") if ch2_val.get("verdict") != "inconclusive"
                   else None)
        if crv.get("verdict") != "inconclusive" and ch1_dir is not None and ch2_dir is not None:
            crv_d = crv.get("cliffs_delta", float("nan"))
            agree_dir = (crv_d > 0 and ch1_dir > 0 and ch2_dir > 0)
            agree_str = ("agrees in sign with Ch1 + Ch2 validate (confirming "
                         "descriptive context)"
                         if agree_dir else
                         "diverges from Ch1 + Ch2 validate (conflicting "
                         "descriptive context)")
            lines.append(
                f"**Reading**: primary Ch3 validate is INCONCLUSIVE "
                f"(n_heavy=25 < 30 per §5.4). Chain-relaxed cell "
                f"{agree_str}. Per §4.11.3, descriptive context only; the "
                f"§5.3 verdict applies CONFIRMED-PARTIAL to Ch3 if Ch3 "
                f"train is SUPPORTED.")
        else:
            lines.append(
                "**Reading**: at least one of the primary Ch3 validate / "
                "chain-relaxed cell / Ch1 validate / Ch2 validate is "
                "INCONCLUSIVE; full directional read deferred to per-cell "
                "values above. Per §4.11.3, descriptive only.")
    lines.append("")

    # --- §5.5 Holm step-down per era (v2 fewer-comparisons aware) ---
    lines.append(
        "## §5.5 Holm step-down per era (multiplicity sensitivity, secondary)")
    lines.append("")
    lines.append(
        "Holm step-down at α=0.05 on the per-era p-values. Per v2 §5.5, "
        "**INCONCLUSIVE cells are omitted from the per-era Holm ordering** "
        "— a 2-of-2-comparison Holm uses cutoffs α/2 and α/1 (vs. "
        "3-of-3's α/3, α/2, α/1) and is therefore less stringent. The "
        "annotation column surfaces the reduced-comparisons disclosure. "
        "**Per §5.0, Holm is a secondary report**; the §5.3 verdict uses "
        "the uncorrected per-channel p-values.")
    lines.append("")
    lines.append(
        "| era | Ch1 raw p | Ch2 raw p | Ch3 raw p | Ch1 adj p | "
        "Ch2 adj p | Ch3 adj p | Holm-rejected | annotation |")
    lines.append(
        "|---|---:|---:|---:|---:|---:|---:|---|---|")
    for era in ("train", "validate"):
        h = results["holm_per_era"][era]
        raw = h["raw_p_values"]
        adj = h["adjusted_p_values"]
        rej = h["rejected"]
        def show(ch, src):
            if ch in src:
                return f"{src[ch]:.4f}"
            return "INC"
        rej_chans = [ch for ch in ("Ch1", "Ch2", "Ch3")
                     if rej.get(ch, False)]
        rej_str = ", ".join(rej_chans) or "(none)"
        lines.append(
            f"| {era} | "
            f"{show('Ch1', raw)} | {show('Ch2', raw)} | {show('Ch3', raw)} | "
            f"{show('Ch1', adj)} | {show('Ch2', adj)} | {show('Ch3', adj)} | "
            f"{rej_str} | {h['annotation']} |")
    lines.append("")

    # --- §4.11.1 crash-drop sensitivity ---
    lines.append("## §4.11.1 Crash-drop sensitivity (CONVENTIONS §3.4)")
    lines.append("")
    lines.append(
        "Per §4.11.1 + audit L4.4 closure: re-run the Mann-Whitney + "
        "Cliff's δ with `is_crash == True` dropped from BOTH arms. Flag "
        f"if |Δ Cliff's δ| > {CRASH_DROP_FLAG} on any channel (\"the "
        "channel's signal is crash-driven, not robust across the broader "
        "heavy-T pool\").")
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
    lines.append(
        "## §4.11.2 Channel 3 spike-metric companion (CONVENTIONS §3.5)")
    lines.append("")
    lines.append(
        "Per §4.11.2 + audit L4.5 closure: parallel Mann-Whitney on "
        "`stress_high_duration_min` on T+1 (spike-count companion) "
        "alongside the primary `awake_stress_avg` on T+1 (mean). If both "
        "agree (same verdict direction and approximate effect size), the "
        "average-vs-spike question is closed; if they diverge, the "
        "divergence is informative for §9 interpretation.")
    lines.append("")
    lines.append(
        "| era | primary Ch3 (awake-mean T+1) δ | spike companion "
        "(high_dur T+1) δ | primary p | spike p | primary verdict | "
        "spike verdict |")
    lines.append(
        "|---|---:|---:|---:|---:|:---:|:---:|")
    for era in ("train", "validate"):
        c3 = pcpe["Ch3"][era]
        sp = results["ch3_spike_per_era"][era]
        d3 = c3.get("cliffs_delta")
        ds = sp.get("cliffs_delta")
        lines.append(
            f"| {era} | "
            f"{fmt(d3, '{:+.3f}')} | {fmt(ds, '{:+.3f}')} | "
            f"{fmt(c3.get('p_value'))} | {fmt(sp.get('p_value'))} | "
            f"{_cell_glyph(c3)} | {_cell_glyph(sp)} |")
    lines.append("")

    # --- §4.11 Ch1 secondary companions + NaN-fraction ---
    lines.append(
        "## §4.11 Channel 1 secondary companions + NaN-fraction contrast")
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
        "| companion | era | n_heavy | n_non | Cliff's δ | p-value | verdict |")
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
                f"{_cell_glyph(cell)} |")
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
        h_str = (f"{h_frac:.4f} ({c['heavy_nan']}/{c['heavy_n']})"
                 if not math.isnan(h_frac) else "NA")
        n_str = (f"{n_frac:.4f} ({c['non_heavy_nan']}/{c['non_heavy_n']})"
                 if not math.isnan(n_frac) else "NA")
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
    lines.append("| hypothesis | status | one-line note |")
    lines.append("|---|---|---|")
    lines.append(
        "| HA-C4b v3 | NOT-SUPPORTED (2026-06-17) | motion-filter "
        "crash-precursor framing; (a)=40%, (b)=−10pp, (c)=+1.21 |")
    lines.append(
        "| HA11 | SUPPORTED on train (+22.8 pp) | U-dip sister channel "
        "(calm-day signal); validate inconclusive on original spec |")
    lines.append("")
    lines.append(
        "Per §9 cross-references: **HA-C4 SUPPORTED + HA-C4b "
        "NOT-SUPPORTED** supports the protective-rather-than-predictive "
        "reading from HA-C4b §9 (the Wiggers pattern IS real on this "
        "corpus, but the participant's real-time use of it as a pacing "
        "trigger prevents the crashes the precursor test would have "
        "caught). **HA-C4 REJECTED + HA-C4b NOT-SUPPORTED + HA11 "
        "SUPPORTED** would mean the Wiggers C4 framework doesn't "
        "operationalise cleanly on this corpus at either the descriptive "
        "or precursor level, but the U-dip (HA11) sister channel does — "
        "C4 mechanism would need different operationalisation (e.g. "
        "bout-level recovery curves) to be testable. **HA-C4 PARTIAL** "
        "outcomes name the specific channel(s) that confirmed; the "
        "substantive read follows the channel-set.")
    lines.append("")

    # --- §8 Caveats ---
    lines.append("## §8 Caveats (v1 inherited)")
    lines.append("")
    lines.append(
        "- **Power-calc dispatch**: power calculation is inapplicable per "
        "[Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) "
        "within-subject design. The block-permutation null at E[L]=7 "
        "(§4.9) is the within-subject inferential machinery; the §5.1 "
        "(a) + (b) gates determine per-cell verdict rather than a "
        "power-thresholded p-value. The v2 §5.3 INCONCLUSIVE handling "
        "does NOT introduce a separate power-calc requirement: the "
        "≥30-per-arm bar (§5.4) inherits from v1.")
    lines.append(
        "- **NaN-as-positive encoding for Channel 1** (§4.5): the "
        "1080-min coding is one operationalisation; the NaN-fraction "
        "descriptive contrast (table above) is the alternative. If the "
        "verdict depends on the encoding choice, flag as "
        "encoding-fragile. Per §7.2 the unmedicated baseline shows "
        "essentially tied NaN fractions across arms (~18% both), so the "
        "encoding's impact on the Mann-Whitney verdict is small.")
    lines.append(
        "- **Chained-regime adjustment for Channel 3** (§4.7): "
        "heavy-T-followed-by-heavy-T+1 days are excluded from the Channel "
        "3 primary arm (train: 117 of 171; validate: 25 of 41). v2 §5.3 "
        "+ §4.11.3 explicitly handle the validate sub-30 case "
        "(CONFIRMED-PARTIAL contribution at the channel-aggregation "
        "layer; chain-relaxed descriptive sensitivity arm above).")
    lines.append(
        "- **Citalopram dose-modulation** (§4.4): the primary scope is "
        "unmedicated only specifically to avoid the dose-confound on the "
        "stress channel "
        "([`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md)). "
        "Cross-phase sensitivity arms are not run in this v2 — that "
        "scope is queued.")
    lines.append(
        "- **No motion filter** (unlike HA-C4b): HA-C4 tests channels "
        "without conditioning on motion. Garmin stress is partly "
        "motion-sensitive per "
        "[`hrv_proxy_via_stress.md`](../../../methodology/hrv_proxy_via_stress.md). "
        "Some channel signal may be motion-artefact rather than true "
        "sympathetic load; cross-reference HA-C4b's motion-filter "
        "result.")
    lines.append(
        "- **Unmedicated = pre-citalopram corpus, not 'no medication "
        "overall'**: participant had other lived-experience "
        "interventions in the 2022-04 → 2024-04 window (CPAP started "
        "2024-01-10; ergotherapy 2022-06-17 → 2023-03-10; PWC "
        "reintegratie 2023-03-06 → 2023-11-28). The unmedicated headline "
        "is 'no SSRI' not 'no intervention'.")
    lines.append(
        "- **Pacing-behaviour confounder** (inherited from HA-C4b v3 "
        "§8): `exertion_class_lagged_lcera` captures physical exertion "
        "only. Cognitive, emotional, and orthostatic exertion are not in "
        "the classification. A 'non-heavy-T' day in this test could "
        "include high cognitive / emotional load days that are "
        "physiologically demanding. Mis-classifying them as non-heavy-T "
        "arm would dilute the contrast (directional bias toward "
        "false-NOT-SUPPORTED).")
    lines.append(
        "- **Single-subject n=1**: thresholds in §5.1 (p < 0.05, |δ| > "
        "0.20) are calibrated to the participant's distribution. The "
        "Mann-Whitney is non-parametric so the threshold-on-effect-size "
        "choice is the binding decision; a stricter Cliff's δ threshold "
        "(e.g. 0.33 for 'medium' effect) would shift the gate.")
    lines.append(
        "- **HA11 / HA-C4b cross-references**: see sister-test table "
        "above.")
    lines.append(
        "- **Block-permutation under stationary bootstrap of labels**: "
        "the bootstrap does not preserve the marginal n_heavy count "
        "(observed mean n_heavy_null is reported in `result-data.json` "
        f"per cell). At B = {B_HEADLINE} the empirical-p noise from this "
        "shift is small.")
    lines.append("")

    # --- Provenance footer ---
    lines.append("---")
    lines.append("")
    lines.append(
        f"*test.py run with `RANDOM_SEED = {RANDOM_SEED}`, "
        f"`BOOTSTRAP_E_L = {BOOTSTRAP_E_L}`, B = {B_HEADLINE} draws per "
        f"cell. Source data: `per_day_master.csv` from "
        f"`$GEVOELSCORE_DATA_PATH`. Spec commit: `{V2_SPEC_COMMIT}`. "
        f"`result-data.json` is the machine-readable companion "
        f"(gitignored per `docs/research/**/*.json`).*")
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
    parser = argparse.ArgumentParser(description="HA-C4 v2 test driver.")
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
        print("\nDry-run sanity gates 1 or 3 FAILED; refusing to run full test.",
              file=sys.stderr)
        print("See dry-run-report.md for failure analysis + v3 recommendation.",
              file=sys.stderr)
        sys.exit(1)

    print("\nDry-run sanity gates 1 + 3 PASSED; running full test...",
          file=sys.stderr)
    results = run_full(master, dry)
    write_result_md(results)
    write_result_json(results)


if __name__ == "__main__":
    main()
