"""HA01c single-pool cross-check.

Re-runs the already-locked HA01c primary (effective_exertion_rank_lagged
>= 0.75 in the 4-day lead-up) under the single-pool framework:

  - full pool of all 29 crash_v1 episodes (no train/validate split)
  - block-bootstrap permutation null, stationary blocks E[L]=7
  - stationary bootstrap 95% CI on the discrimination, E[L]=7
  - data-driven block-length companion E[L]* + factor-of-2 flag

This is a validation-framework cross-check, NOT a new hypothesis. It
changes only the validation framework, not the claim/measurement/
threshold/window/direction, so it does not create an HA01d and does
not re-lock HA01c's on-record verdict. See pre-registration.md.

Locked verdict rule: single-pool SUPPORTED iff permutation p < 0.05
(primary alpha); NOT-SUPPORTED otherwise. Legacy 3-criterion bar and
the M3 train/validate overlay are reported descriptively only.

Pre-registered 2026-07-03 in pre-registration.md, before the derived
data was materialised. Pure stdlib; ASCII only.

Output:
- result-data.json
- stdout dry-run gate (3 earliest + 3 latest episodes) before full run
"""
from __future__ import annotations

import csv
import json
import math
import random
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANALYSES_ROOT = HERE.parent.parent  # .../docs/research/analyses
FEATURES_CSV = (ANALYSES_ROOT / "garmin_exploration" / "activity-labels"
                / "output" / "activity_features_daily.csv")
LABELS_CSV = (ANALYSES_ROOT / "hypotheses" / "crash_v2-definition"
              / "labels_crash_v2.csv")
OUT_JSON = HERE / "result-data.json"

# Locked window / stratum (inherited from HA01c)
ANALYSIS_START = date(2022, 9, 3)
SPLIT_BOUNDARY = date(2023, 12, 31)  # M3 overlay only, NOT primary
VALIDATE_END = date(2026, 6, 5)
LEADUP_DAYS = 4

# Locked per-axis primary (inherited from HA01c)
AXIS_LABEL = "effective_exertion"
AXIS_COL = "effective_exertion_rank_lagged"
AXIS_RANK_THRESHOLD = 0.75

# Single-pool framework knobs (this cross-check)
EXPECTED_BLOCK_LEN = 7          # E[L]=7 stationary bootstrap default
N_RESAMPLES = 10000             # B for permutation + bootstrap
RANDOM_SEED = 20260703
ALPHA_PRIMARY = 0.05
ALPHA_BONFERRONI = 0.0125       # effective-N ~ 4 context
BASE_RATE = 0.0211              # single-pool base (29/1372)
BASE_RATE_VALIDATE = 0.0169     # validate base, reported alongside

# Legacy 3-criterion bar (reported descriptively, not the verdict)
CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15
CRIT_C_MEDIAN_RANK_MIN = 0.875

N_CLEAN_FLOOR = 10


def load_features() -> dict[date, dict]:
    out = {}
    for r in csv.DictReader(FEATURES_CSV.open(encoding="utf-8")):
        out[date.fromisoformat(r["date"])] = r
    return out


def load_crash_starts() -> list[date]:
    by_id: dict[str, list[date]] = {}
    for r in csv.DictReader(LABELS_CSV.open(encoding="utf-8")):
        if r["label"] != "crash":
            continue
        by_id.setdefault(r["episode_id"], []).append(date.fromisoformat(r["date"]))
    return sorted(min(ds) for ds in by_id.values())


def parse_float(v):
    if v in (None, "", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def leadup_dates(ref: date) -> list[date]:
    return [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]


def window_stats(ref: date, features: dict[date, dict]) -> dict | None:
    """4-day lead-up stats. Returns None if fewer than 3 valid ranks."""
    ranks = []
    for d in leadup_dates(ref):
        r = features.get(d)
        if not r:
            continue
        rv = parse_float(r.get(AXIS_COL))
        if rv is None:
            continue
        ranks.append(rv)
    if len(ranks) < 3:
        return None
    max_rank = max(ranks)
    return {
        "max_rank": max_rank,
        "n_valid": len(ranks),
        "triggers": max_rank >= AXIS_RANK_THRESHOLD,
    }


def build_background_pool(features: dict[date, dict],
                          crash_starts: list[date]) -> list[tuple[date, int]]:
    """All valid candidate anchors whose lead-up does not overlap any
    crash lead-up window. Returns [(date, W)] in chronological order."""
    crash_leadup: set[date] = set()
    for c in crash_starts:
        crash_leadup.update(leadup_dates(c))
    pool = []
    d = ANALYSIS_START
    while d <= VALIDATE_END:
        overlaps = any(ld in crash_leadup for ld in leadup_dates(d))
        if not overlaps:
            w = window_stats(d, features)
            if w is not None:
                pool.append((d, 1 if w["triggers"] else 0))
        d += timedelta(days=1)
    return pool


def stationary_block_sample(values: list[int], n_out: int,
                            rng: random.Random) -> list[int]:
    """Stationary bootstrap: draw n_out items in geometric-length blocks
    (mean EXPECTED_BLOCK_LEN) from a circular view of `values`."""
    m = len(values)
    if m == 0:
        return []
    p_new = 1.0 / EXPECTED_BLOCK_LEN
    out: list[int] = []
    while len(out) < n_out:
        start = rng.randrange(m)
        out.append(values[start])
        pos = start
        while len(out) < n_out and rng.random() > p_new:
            pos = (pos + 1) % m
            out.append(values[pos])
    return out[:n_out]


def permutation_p(t_obs: float, bg_w: list[int], n_clean: int,
                  rng: random.Random) -> dict:
    """Block-bootstrap null: mean W over n_clean anchors sampled in
    stationary blocks from the background pool. p = P(T* >= T_obs)."""
    ge = 0
    null_means = []
    for _ in range(N_RESAMPLES):
        sample = stationary_block_sample(bg_w, n_clean, rng)
        t_star = sum(sample) / len(sample)
        null_means.append(t_star)
        if t_star >= t_obs:
            ge += 1
    p = (1 + ge) / (N_RESAMPLES + 1)
    null_means.sort()
    return {
        "p_value": p,
        "n_resamples": N_RESAMPLES,
        "null_mean_of_means": statistics.mean(null_means),
        "null_ci95": [null_means[int(0.025 * N_RESAMPLES)],
                      null_means[int(0.975 * N_RESAMPLES)]],
    }


def bootstrap_disc_ci(crash_w: list[int], bg_w: list[int],
                      rng: random.Random) -> dict:
    """Stationary bootstrap 95% CI on discrimination = p_crash - p_bg."""
    discs = []
    n_c = len(crash_w)
    n_b = len(bg_w)
    for _ in range(N_RESAMPLES):
        cs = stationary_block_sample(crash_w, n_c, rng)
        bs = stationary_block_sample(bg_w, n_b, rng)
        discs.append(sum(cs) / len(cs) - sum(bs) / len(bs))
    discs.sort()
    return {
        "disc_pp_ci95": [discs[int(0.025 * N_RESAMPLES)] * 100,
                         discs[int(0.975 * N_RESAMPLES)] * 100],
        "disc_pp_bootstrap_median": statistics.median(discs) * 100,
    }


def data_driven_block_len(features: dict[date, dict]) -> dict:
    """E[L]* proxy: first lag where |ACF| of the daily trigger indicator
    falls below the white-noise band 2/sqrt(N). Transparent proxy, not
    Politis-White."""
    series = []
    d = ANALYSIS_START
    while d <= VALIDATE_END:
        r = features.get(d)
        rv = parse_float(r.get(AXIS_COL)) if r else None
        if rv is not None:
            series.append(1 if rv >= AXIS_RANK_THRESHOLD else 0)
        d += timedelta(days=1)
    n = len(series)
    if n < 30:
        return {"e_l_star": None, "n": n, "flag_factor_of_2": None,
                "note": "series too short for ACF"}
    mean = sum(series) / n
    var = sum((x - mean) ** 2 for x in series) / n
    band = 2.0 / math.sqrt(n)
    e_l_star = None
    acf = []
    if var > 0:
        for k in range(1, min(31, n)):
            cov = sum((series[t] - mean) * (series[t + k] - mean)
                      for t in range(n - k)) / n
            r_k = cov / var
            acf.append(r_k)
            if e_l_star is None and abs(r_k) < band:
                e_l_star = k
    flag = None
    if e_l_star is not None:
        flag = abs(e_l_star - EXPECTED_BLOCK_LEN) / EXPECTED_BLOCK_LEN > 0.5
    return {
        "e_l_star": e_l_star,
        "n": n,
        "white_noise_band": band,
        "acf_lags_1_to_10": [round(x, 4) for x in acf[:10]],
        "flag_factor_of_2": flag,
        "note": ("E[L]* deviates from 7 by > factor of 2; flag for review"
                 if flag else "E[L]* within factor-of-2 of the E[L]=7 default"),
    }


def usability(p_crash: float, p_bg: float, base: float) -> dict:
    sens = p_crash
    spec = 1.0 - p_bg
    denom = base * sens + (1 - base) * (1 - spec)
    ppv = (base * sens / denom) if denom > 0 else 0.0
    lift = (ppv / base) if base > 0 else 0.0
    return {
        "base_rate": base,
        "sensitivity": sens,
        "specificity": spec,
        "ppv": ppv,
        "lift": lift,
        "tier": "C" if ppv < 0.05 else "B-or-better",
    }


def m3_overlay(clean_episodes: list[tuple[date, int]], p_bg: float) -> dict:
    """Descriptive train/validate discrimination. Number, not narrative."""
    def disc(sub):
        if not sub:
            return None
        pc = sum(w for _, w in sub) / len(sub)
        return {"n": len(sub), "p_crash": pc, "disc_pp": (pc - p_bg) * 100}
    train = [(d, w) for d, w in clean_episodes if d <= SPLIT_BOUNDARY]
    validate = [(d, w) for d, w in clean_episodes if d > SPLIT_BOUNDARY]
    return {
        "note": "Descriptive M3 overlay only. Number, not narrative. "
                "No per-era verdict, no per-era alpha.",
        "train": disc(train),
        "validate": disc(validate),
    }


def dry_run_print(crash_starts: list[date], features: dict[date, dict]) -> dict:
    samples = []
    print("\n=== Dry-run gate (3 earliest + 3 latest crash starts) ===")
    picks = crash_starts[:3] + crash_starts[-3:]
    for ref in picks:
        day_ranks = []
        for d in leadup_dates(ref):
            r = features.get(d)
            rv = parse_float(r.get(AXIS_COL)) if r else None
            day_ranks.append((d.isoformat(), rv))
        triggers = any(rv is not None and rv >= AXIS_RANK_THRESHOLD
                       for _, rv in day_ranks)
        day_str = " ".join(f"{ds[5:]}={rv:.2f}" if rv is not None
                           else f"{ds[5:]}=NA" for ds, rv in day_ranks)
        marker = "  [trigger]" if triggers else ""
        print(f"  {ref.isoformat()}: {day_str}{marker}")
        samples.append({"ref": ref.isoformat(), "days": day_ranks,
                        "triggers": triggers})
    print()
    return {"samples": samples}


def main(dry_run_only: bool = False):
    features = load_features()
    crash_starts = load_crash_starts()
    print(f"Loaded {len(features)} feature days | "
          f"{len(crash_starts)} crash_v1 episodes")

    dry = dry_run_print(crash_starts, features)
    if dry_run_only:
        print("--dry-run-only set; not running full single-pool verdict.")
        return

    # Clean episodes (>= 3 of 4 lead-up days valid)
    clean_episodes: list[tuple[date, int]] = []
    for c in crash_starts:
        w = window_stats(c, features)
        if w is not None:
            clean_episodes.append((c, 1 if w["triggers"] else 0))
    n_clean = len(clean_episodes)
    print(f"  n_clean (>=3/4 valid lead-up days): {n_clean}/{len(crash_starts)}")

    bg_pool = build_background_pool(features, crash_starts)
    bg_w = [w for _, w in bg_pool]
    print(f"  background pool (ordinary anchors): {len(bg_w)}")

    if n_clean < N_CLEAN_FLOOR:
        out = {"hypothesis": "HA01c-single-pool-crosscheck",
               "verdict": "inconclusive",
               "reason": f"n_clean={n_clean} < {N_CLEAN_FLOOR}"}
        OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
        print(f"\nINCONCLUSIVE (n_clean={n_clean}). Wrote {OUT_JSON}")
        return

    crash_w = [w for _, w in clean_episodes]
    p_crash = sum(crash_w) / n_clean
    p_bg = sum(bg_w) / len(bg_w)
    disc_pp = (p_crash - p_bg) * 100

    rng = random.Random(RANDOM_SEED)
    perm = permutation_p(p_crash, bg_w, n_clean, rng)
    boot = bootstrap_disc_ci(crash_w, bg_w, rng)
    elstar = data_driven_block_len(features)

    # Legacy 3-criterion bar (descriptive only)
    trig_ranks = []
    for c, w in clean_episodes:
        if w == 1:
            ws = window_stats(c, features)
            if ws:
                trig_ranks.append(ws["max_rank"])
    median_rank = statistics.median(trig_ranks) if trig_ranks else 0.0
    legacy = {
        "crit_a_freq_ge_60": p_crash >= CRIT_A_FRAC,
        "crit_b_disc_ge_15pp": disc_pp >= CRIT_B_DISC_PP,
        "crit_c_median_rank_ge_0875": median_rank >= CRIT_C_MEDIAN_RANK_MIN,
        "freq": p_crash, "disc_pp": disc_pp, "median_rank_on_triggering": median_rank,
        "note": "Legacy HA01c bar; reported for continuity, NOT the verdict.",
    }

    verdict = "supported" if perm["p_value"] < ALPHA_PRIMARY else "not-supported"

    out = {
        "hypothesis": "HA01c-single-pool-crosscheck",
        "is_new_hypothesis": False,
        "note": "Validation-framework cross-check of locked HA01c. "
                "Does not create HA01d; does not re-lock HA01c.",
        "pre_registered": "2026-07-03 in pre-registration.md",
        "config": {
            "analysis_start": ANALYSIS_START.isoformat(),
            "validate_end": VALIDATE_END.isoformat(),
            "leadup_days": LEADUP_DAYS,
            "axis_col": AXIS_COL,
            "axis_rank_threshold": AXIS_RANK_THRESHOLD,
            "expected_block_len": EXPECTED_BLOCK_LEN,
            "n_resamples": N_RESAMPLES,
            "random_seed": RANDOM_SEED,
            "alpha_primary": ALPHA_PRIMARY,
            "alpha_bonferroni": ALPHA_BONFERRONI,
        },
        "counts": {
            "n_crash_episodes": len(crash_starts),
            "n_clean": n_clean,
            "n_background_anchors": len(bg_w),
        },
        "point_estimates": {
            "p_crash": p_crash, "p_bg": p_bg, "discrimination_pp": disc_pp,
        },
        "permutation_null": perm,
        "bootstrap_ci": boot,
        "block_length_companion": elstar,
        "usability_base_2_11pct": usability(p_crash, p_bg, BASE_RATE),
        "usability_base_1_69pct": usability(p_crash, p_bg, BASE_RATE_VALIDATE),
        "legacy_3criterion_bar": legacy,
        "m3_overlay": m3_overlay(clean_episodes, p_bg),
        "verdict_rule": "SUPPORTED iff permutation p < 0.05 (primary alpha)",
        "single_pool_verdict": verdict,
        "significant_at_bonferroni": perm["p_value"] < ALPHA_BONFERRONI,
        "dry_run": dry,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")

    print("\n=== HA01c single-pool cross-check ===")
    print(f"  p_crash            : {p_crash*100:.1f}%  (n_clean={n_clean})")
    print(f"  p_bg (background)  : {p_bg*100:.1f}%  (n={len(bg_w)})")
    print(f"  discrimination     : {disc_pp:+.1f} pp  "
          f"CI95 [{boot['disc_pp_ci95'][0]:+.1f}, {boot['disc_pp_ci95'][1]:+.1f}]")
    print(f"  permutation p      : {perm['p_value']:.4f}  "
          f"(sig at 0.05: {perm['p_value'] < ALPHA_PRIMARY}; "
          f"at Bonf 0.0125: {perm['p_value'] < ALPHA_BONFERRONI})")
    print(f"  E[L]* companion    : {elstar['e_l_star']}  "
          f"({elstar['note']})")
    u = out["usability_base_2_11pct"]
    print(f"  usability @2.11%   : sens={u['sensitivity']*100:.1f}% "
          f"spec={u['specificity']*100:.1f}% ppv={u['ppv']*100:.2f}% "
          f"lift={u['lift']:.2f}x tier={u['tier']}")
    print(f"\n  SINGLE-POOL VERDICT: {verdict.upper()}")
    print(f"\nWrote {OUT_JSON}")


if __name__ == "__main__":
    main(dry_run_only="--dry-run-only" in sys.argv)
