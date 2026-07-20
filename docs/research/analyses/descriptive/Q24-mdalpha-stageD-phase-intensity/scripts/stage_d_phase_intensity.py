"""
Q24 MD-alpha Stage D descriptive audit -- phase-stratified pacing + dose-response.

Executes the operand locked at
`docs/research/methodology/post_heavy_day_pacing_learning.md` (MD-alpha, LOCKED
r1 2026-07-16), which extends the parent Q24 MD
`post_heavy_day_compensatory_rest.md` (LOCKED r1, commit 58b7723) by adding two
stratification axes on top of the identical trajectory machine:

  - Sub-part 3 (MD-alpha section 3): recovery_phase axis (4 buckets), late-pair
    vs early-pair |AUC| contrast + the section 3.5 rescue metric.
  - Dose-response (MD-alpha section 4): intensity strata (very_heavy vs heavy
    episode-end), |AUC| + slope contrast.

NO RE-DERIVATION (MD-alpha section 2): the episode-end identification,
matched-ordinary comparator, nine trajectory summary stats, linear_detrend_on_pre,
and bootstrap are IMPORTED verbatim from the parent Wave-1 script, following the
sign_flipper_diagnostic.py precedent. This file only adds the phase/intensity
pre-filter wrapper + the rescue metric + the mandatory level-vs-change companion.

Discipline (inherited): descriptive-before-inference (CONVENTIONS 2.1); zero-vs-NaN
(never fillna(0)); sample-floor n<10 => descriptive without bootstrap CIs; 5
structurally-unavailable cells emit NaN, never zero (MD-alpha precursor section 5.4);
phase-stratified naming NEVER "learned-pacing" (MD-alpha section 3.6). No em-dash,
no emoji in output.

Idempotent: fixed seed; re-running produces byte-identical output CSVs.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

# --- Import parent Wave-1 trajectory machinery (no re-derivation) ------------
# Parent scripts live at ../../Q24-post-heavy-trajectory/scripts relative to this file.
PARENT_SCRIPTS = (
    Path(__file__).resolve().parent.parent.parent
    / "Q24-post-heavy-trajectory"
    / "scripts"
)
sys.path.insert(0, str(PARENT_SCRIPTS))
from audit import (  # noqa: E402
    BOOTSTRAP_B,
    bootstrap_all,
    build_matched_ordinary_pool,
    build_trigger_pools,
    compute_first_crossing_day,
    compute_per_day_mean_and_delta,
    compute_per_day_n_valid,
    compute_scalar_summaries,
    extract_trajectory_matrix,
    has_crash_in_post_window,
    identify_heavy_episode_ends,
    load_master,
)
from detrend import PRE_WINDOW_DAYS  # noqa: E402

# ---------------------------------------------------------------------------
# Constants (MD-alpha locked design)
# ---------------------------------------------------------------------------

RANDOM_SEED = 20260720  # per orchestrator brief; per-analysis seed (MD-alpha Stage D)

OUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

WINDOWS = [3, 5, 10]
OVERLAPS = ["strict_clean", "inclusive"]
POOLS = ["compensatory_success", "compensatory_failure"]
ARMS = ["raw", "detrended"]

# MD-alpha section 3.1 phase axis (ordinal, early -> late)
PHASES = [
    "lc_pre_ergo",
    "pacing_pre_citalopram_learning",
    "pacing_habit_established",
    "citalopram_modulated",
]
EARLY_PAIR = PHASES[:2]   # section 3.3 early-phase pair
LATE_PAIR = PHASES[2:]    # section 3.3 late-phase pair

# MD-alpha section 3.2 primary outcome family = activity axes (direction -1 per
# parent section 7.7: below matched-ordinary is the compensatory direction).
ACTIVITY_OUTCOMES = [
    ("total_steps", -1),
    ("effective_exertion_min", -1),
    ("vigorous_min", -1),
    ("active_min", -1),
]

# Sample-floor tiers (MD-alpha precursor section 5 / parent section 7.10).
FLOOR_BOOTSTRAP = 10   # n >= 10 -> bootstrap-CI viable
FLOOR_DESCRIPTIVE = 5  # 5 <= n < 10 -> descriptive-only; 1..4 narrative; 0 unavailable


def viability_tier(n: int) -> str:
    if n == 0:
        return "unavailable"
    if n < FLOOR_DESCRIPTIVE:
        return "narrative"
    if n < FLOOR_BOOTSTRAP:
        return "descriptive"
    return "bootstrap"


# ---------------------------------------------------------------------------
# Added machinery: inclusive-overlap pool + phase/intensity pre-filters
# ---------------------------------------------------------------------------


def build_trigger_pools_inclusive(df, episode_ends, w):
    """Inclusive-overlap variant of the parent build_trigger_pools.

    Parent Wave 1 was strict-clean only; MD-alpha (parent section 5.2) requires
    strict-clean + inclusive side-by-side. Inclusive = do NOT drop episode-ends
    that have an intervening heavy day in the window; split only by crash.
    Reuses the imported has_crash_in_post_window (no re-derivation of crash logic).
    """
    success, failure = [], []
    for D in episode_ends:
        if has_crash_in_post_window(df, D, w):
            failure.append(D)
        else:
            success.append(D)
    return success, failure


def anchors_in_phases(df, anchors, phases):
    """Restrict a list of anchor dates to those whose recovery_phase is in `phases`."""
    return [D for D in anchors if df.loc[D, "recovery_phase"] in phases]


def anchors_of_intensity(df, anchors, intensity):
    """Restrict episode-end anchors by last-day exertion class (dose-response)."""
    if intensity == "combined":
        return list(anchors)
    return [D for D in anchors if df.loc[D, "exertion_class_lagged_lcera"] == intensity]


def prewindow_mean_level(df, anchors, outcome_col):
    """Mean of the raw outcome over the [D-30, D-1] pre-window, averaged across
    anchors. The mandatory level-vs-change companion (MD-alpha section 3.5 +
    precursor section 8): a phase |AUC| trend can be an absolute-envelope shift
    rather than compensation strengthening, so per-phase pre-window levels are
    reported alongside every phase contrast.
    """
    per_anchor = []
    for D in anchors:
        start = D - pd.Timedelta(days=PRE_WINDOW_DAYS)
        end = D - pd.Timedelta(days=1)
        s = df.loc[start:end, outcome_col]
        if len(s) > 0:
            with np.errstate(all="ignore"):
                per_anchor.append(np.nanmean(s.to_numpy(dtype=float)))
    if not per_anchor:
        return np.nan, 0
    arr = np.array(per_anchor, dtype=float)
    with np.errstate(all="ignore"):
        return float(np.nanmean(arr)), int(np.sum(~np.isnan(arr)))


def monotonicity_score(abs_auc_by_phase):
    """Fraction of consecutive-phase-pair |AUC| increases (denominator 3), on the
    ordinal early->late axis. Undefined (NaN) if any phase is missing (MD-alpha
    section 3.5)."""
    v = np.array(abs_auc_by_phase, dtype=float)
    if np.any(np.isnan(v)):
        return np.nan
    incr = np.sum(np.diff(v) > 0)
    return float(incr) / 3.0


# ---------------------------------------------------------------------------
# One trajectory cell: trigger anchors vs phase/full comparator anchors
# ---------------------------------------------------------------------------


def trajectory_cell(df, trigger_anchors, comparator_anchors, outcome_col, w, dsign, arm, rng):
    """Compute one trajectory-summary cell reusing the parent machinery.

    Returns a dict of the reported quantities (auc, abs_auc, slope, rtbt,
    below_baseline_days, first_crossing, effective n, CIs, tier).
    """
    detrended = arm == "detrended"
    trig_mat = extract_trajectory_matrix(df, trigger_anchors, outcome_col, w, detrended=detrended)
    comp_mat = extract_trajectory_matrix(df, comparator_anchors, outcome_col, w, detrended=detrended)

    if detrended:
        trig_mat = trig_mat[~np.all(np.isnan(trig_mat), axis=1)]
        comp_mat = comp_mat[~np.all(np.isnan(comp_mat), axis=1)]
    n_trig = int(trig_mat.shape[0])
    n_comp = int(comp_mat.shape[0])

    mean_t, mean_c, delta = compute_per_day_mean_and_delta(trig_mat, comp_mat)
    scalars = compute_scalar_summaries(delta, dsign)

    tier = viability_tier(n_trig)
    if n_trig >= FLOOR_BOOTSTRAP and n_comp >= 2:
        cis, _, _, delta_lo, delta_hi = bootstrap_all(trig_mat, comp_mat, dsign, rng, B=BOOTSTRAP_B)
        first_crossing = compute_first_crossing_day(delta, delta_lo, delta_hi)
    else:
        # Below the bootstrap floor: descriptive point estimate only, no CI.
        cis = {k: (np.nan, np.nan) for k in [
            "auc", "slope", "peak_k", "peak_magnitude", "rtbt",
            "below_baseline_days", "variability"]}
        first_crossing = np.nan

    auc = scalars["auc"]
    abs_auc = abs(auc) if not (auc is None or (isinstance(auc, float) and np.isnan(auc))) else np.nan
    return {
        "n_trigger": n_trig,
        "n_comparator": n_comp,
        "tier": tier,
        "auc": auc,
        "abs_auc": abs_auc,
        "auc_ci_lo": cis["auc"][0],
        "auc_ci_hi": cis["auc"][1],
        "slope": scalars["slope"],
        "slope_ci_lo": cis["slope"][0],
        "slope_ci_hi": cis["slope"][1],
        "rtbt": scalars["rtbt"],
        "below_baseline_days": scalars["below_baseline_days"],
        "first_crossing_day": first_crossing,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    t0 = time.time()
    print(f"[MD-alpha Stage D] loading {load_master.__module__} master CSV...")
    df = load_master()
    print(f"[MD-alpha Stage D] LC-era rows: {len(df)}")
    if "recovery_phase" not in df.columns:
        raise SystemExit("recovery_phase column absent -- cannot phase-stratify")

    episode_ends = identify_heavy_episode_ends(df)
    print(f"[MD-alpha Stage D] gap=0 episode-ends: {len(episode_ends)}")

    rng = np.random.default_rng(RANDOM_SEED)

    # --- Availability cross-checks (reproduce precursor / MD-alpha anchors) ---
    avail_rows = []
    phase_counts = {p: int(sum(df.loc[D, "recovery_phase"] == p for D in episode_ends)) for p in PHASES}
    for p in PHASES:
        avail_rows.append({"axis": "phase", "bucket": p, "n_episode_ends": phase_counts[p]})
    avail_rows.append({"axis": "phase", "bucket": "ALL", "n_episode_ends": len(episode_ends)})
    for inten in ["heavy", "very_heavy"]:
        for p in PHASES:
            n = int(sum(
                (df.loc[D, "recovery_phase"] == p) and (df.loc[D, "exertion_class_lagged_lcera"] == inten)
                for D in episode_ends))
            avail_rows.append({"axis": f"intensity:{inten}", "bucket": p, "n_episode_ends": n})
    pd.DataFrame(avail_rows).to_csv(OUT_DIR / "availability.csv", index=False)
    print(f"[MD-alpha Stage D] phase episode-ends: {phase_counts}")

    # --- PART B: level-vs-change companion (pre-window levels on ALL episode-ends
    # per phase; reproduces MD-alpha precursor section 8 locked numbers exactly.
    # MD-alpha section 3.5: a phase |AUC| trend can be an absolute-envelope shift
    # rather than compensation strengthening, so report levels alongside AUC). ---
    level_rows = []
    level_groups = [(p, [p]) for p in PHASES] + [("early_pair", EARLY_PAIR), ("late_pair", LATE_PAIR)]
    for outcome, _ in ACTIVITY_OUTCOMES:
        for gname, gphases in level_groups:
            anchors = anchors_in_phases(df, list(episode_ends), gphases)
            lvl, n_lvl = prewindow_mean_level(df, anchors, outcome)
            level_rows.append({
                "outcome": outcome, "group": gname,
                "prewindow_mean_level": lvl, "n_episode_ends": n_lvl,
            })
    pd.DataFrame(level_rows).to_csv(OUT_DIR / "prewindow_levels.csv", index=False)

    # --- PART A: phase-stratified trajectory ---
    phase_rows = []
    # groups: 4 individual phases (for rescue metric) + early_pair + late_pair (headline contrast)
    phase_groups = [(p, [p], "phase") for p in PHASES] + [
        ("early_pair", EARLY_PAIR, "pair"),
        ("late_pair", LATE_PAIR, "pair"),
    ]
    for overlap in OVERLAPS:
        for w in WINDOWS:
            if overlap == "strict_clean":
                succ, fail = build_trigger_pools(df, episode_ends, w)
            else:
                succ, fail = build_trigger_pools_inclusive(df, episode_ends, w)
            pools = {"compensatory_success": succ, "compensatory_failure": fail}
            for outcome, dsign in ACTIVITY_OUTCOMES:
                comp_all = build_matched_ordinary_pool(df, w, outcome)
                for pool_name in POOLS:
                    trig_all = pools[pool_name]
                    for gname, gphases, gtype in phase_groups:
                        trig = anchors_in_phases(df, trig_all, gphases)
                        comp = anchors_in_phases(df, comp_all, gphases)
                        for arm in ARMS:
                            cell = trajectory_cell(df, trig, comp, outcome, w, dsign, arm, rng)
                            phase_rows.append({
                                "overlap": overlap, "window": w, "pool": pool_name,
                                "outcome": outcome, "group": gname, "group_type": gtype,
                                "arm": arm, "direction_sign": dsign, **cell,
                            })
    phase_df = pd.DataFrame(phase_rows)
    phase_df.to_csv(OUT_DIR / "phase_trajectory_summary.csv", index=False)

    # --- PART C: rescue metric (Spearman rho of |AUC| + monotonicity on 4 phases) ---
    rescue_rows = []
    for overlap in OVERLAPS:
        for w in WINDOWS:
            for outcome, _ in ACTIVITY_OUTCOMES:
                for pool_name in POOLS:
                    for arm in ARMS:
                        sub = phase_df[
                            (phase_df.overlap == overlap) & (phase_df.window == w)
                            & (phase_df.outcome == outcome) & (phase_df.pool == pool_name)
                            & (phase_df.arm == arm) & (phase_df.group_type == "phase")]
                        abs_auc_by_phase = [
                            sub[sub.group == p]["abs_auc"].iloc[0] if len(sub[sub.group == p]) else np.nan
                            for p in PHASES]
                        n_by_phase = [
                            sub[sub.group == p]["n_trigger"].iloc[0] if len(sub[sub.group == p]) else 0
                            for p in PHASES]
                        v = np.array(abs_auc_by_phase, dtype=float)
                        if np.any(np.isnan(v)):
                            rho, rho_p, defined = np.nan, np.nan, False
                        else:
                            rho, rho_p = spearmanr([1, 2, 3, 4], v)
                            defined = True
                        mono = monotonicity_score(abs_auc_by_phase)
                        if defined and rho >= 0.50:
                            call = "rescue_eligible"
                        elif defined and rho >= 0.20:
                            call = "weak_flag"
                        elif defined:
                            call = "no_rescue"
                        else:
                            call = "undefined_incomplete_phases"
                        rescue_rows.append({
                            "overlap": overlap, "window": w, "outcome": outcome,
                            "pool": pool_name, "arm": arm,
                            "abs_auc_lc_pre_ergo": abs_auc_by_phase[0],
                            "abs_auc_pacing_pre_cital": abs_auc_by_phase[1],
                            "abs_auc_pacing_habit": abs_auc_by_phase[2],
                            "abs_auc_citalopram_mod": abs_auc_by_phase[3],
                            "n_by_phase": ";".join(str(n) for n in n_by_phase),
                            "spearman_rho": rho, "spearman_p": rho_p,
                            "monotonicity_score": mono, "rescue_call": call,
                        })
    pd.DataFrame(rescue_rows).to_csv(OUT_DIR / "rescue_metrics.csv", index=False)

    # --- PART D: dose-response (intensity strata; NOT phase-stratified) ---
    dr_rows = []
    for w in WINDOWS:
        # dose-response uses strict-clean success pool per MD-alpha section 4 (parent section 9)
        succ, _ = build_trigger_pools(df, episode_ends, w)
        for outcome, dsign in ACTIVITY_OUTCOMES:
            comp_all = build_matched_ordinary_pool(df, w, outcome)
            for inten in ["combined", "very_heavy", "heavy"]:
                trig = anchors_of_intensity(df, succ, inten)
                for arm in ARMS:
                    cell = trajectory_cell(df, trig, comp_all, outcome, w, dsign, arm, rng)
                    dr_rows.append({
                        "window": w, "outcome": outcome, "intensity": inten,
                        "arm": arm, "direction_sign": dsign, **cell,
                    })
    pd.DataFrame(dr_rows).to_csv(OUT_DIR / "doseresponse_summary.csv", index=False)

    t1 = time.time()
    print(f"[MD-alpha Stage D] wall-clock: {t1 - t0:.1f}s; outputs in {OUT_DIR}")


if __name__ == "__main__":
    main()
