"""v2 threshold-sweep rescue/close/ambiguous criteria — shared module.

Implements the locked five-category shape rule from
threshold-sweep-rescue-criteria-v2.md. Used by all four v2
diagnostics: HA10, HA07d, HA06b, HA11.

The criteria are locked; this code is the only place the rule
logic lives. No diagnostic.md file should re-implement the rule.

Definitions (per v2 methodology doc §3.0):

  meaningful_range: N_std in [1.0, 3.0] inclusive
  sign_changes: count of zero-crossings in meaningful range
  direction_reversals: count of slope sign changes (reported only)
  peak: argmax of disc in meaningful range
  spearman_rho: rank correlation in meaningful range
  max_neg: minimum disc in meaningful range
"""
from __future__ import annotations

from typing import Mapping


MEANINGFUL_MIN = 1.0
MEANINGFUL_MAX = 3.0


def _meaningful_grid(disc_by_n_std: Mapping[float, float]) -> list[tuple[float, float]]:
    """Return (n_std, disc) pairs in meaningful range, sorted by n_std."""
    return sorted(
        ((n, d) for n, d in disc_by_n_std.items() if MEANINGFUL_MIN <= n <= MEANINGFUL_MAX),
        key=lambda x: x[0],
    )


def _spearman(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return 0.0

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


def compute_shape_stats(disc_by_n_std: Mapping[float, float]) -> dict:
    """Compute shape statistics over the meaningful range [1.0, 3.0]."""
    meaningful = _meaningful_grid(disc_by_n_std)
    if not meaningful:
        return {
            "n_meaningful_tiers": 0,
            "peak_n_std": None,
            "peak_disc": None,
            "sign_changes": None,
            "direction_reversals": None,
            "spearman_rho": None,
            "max_neg_disc": None,
        }

    n_stds = [n for n, _ in meaningful]
    discs = [d for _, d in meaningful]

    peak_idx = max(range(len(discs)), key=lambda i: discs[i])
    peak_n_std = n_stds[peak_idx]
    peak_disc = discs[peak_idx]

    # Sign changes (zero-crossings)
    sign_changes = 0
    prev_sign = None
    for d in discs:
        if d > 0:
            sign = 1
        elif d < 0:
            sign = -1
        else:
            continue
        if prev_sign is not None and sign != prev_sign:
            sign_changes += 1
        prev_sign = sign

    # Direction reversals (slope sign changes; descriptive only)
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

    rho = _spearman(n_stds, discs)
    max_neg = min(discs)

    return {
        "n_meaningful_tiers": len(meaningful),
        "peak_n_std": peak_n_std,
        "peak_disc": peak_disc,
        "sign_changes": sign_changes,
        "direction_reversals": direction_reversals,
        "spearman_rho": rho,
        "max_neg_disc": max_neg,
    }


def _disc_at(disc_by_n_std: Mapping[float, float], n_std: float) -> float | None:
    """Look up disc at a specific n_std tier; tolerates float key types."""
    # Try exact match first
    if n_std in disc_by_n_std:
        return disc_by_n_std[n_std]
    # Tolerate string-keyed dicts (from JSON)
    s_key = str(n_std)
    if s_key in disc_by_n_std:
        return disc_by_n_std[s_key]
    # Approximate match within float tolerance
    for k, v in disc_by_n_std.items():
        try:
            if abs(float(k) - n_std) < 1e-6:
                return v
        except (TypeError, ValueError):
            continue
    return None


def _normalised(disc_by_n_std) -> dict[float, float]:
    """Convert all keys to float for consistent lookup."""
    out = {}
    for k, v in disc_by_n_std.items():
        try:
            fk = float(k)
        except (TypeError, ValueError):
            continue
        out[fk] = float(v)
    return out


def evaluate_cat1(disc_by_n_std, stats) -> tuple[bool, str]:
    """Canonical decline — PASS if all required criteria met."""
    d = _normalised(disc_by_n_std)
    if stats["peak_n_std"] is None:
        return False, "no meaningful range data"
    cond_peak = 1.0 <= stats["peak_n_std"] <= 1.5
    cond_rho = stats["spearman_rho"] <= -0.3
    cond_signs = stats["sign_changes"] <= 1
    cond_disc20 = (_disc_at(d, 2.0) or -999) >= 10
    cond_disc25 = (_disc_at(d, 2.5) or -999) >= 7
    passed = all([cond_peak, cond_rho, cond_signs, cond_disc20, cond_disc25])
    detail = (
        f"peak={stats['peak_n_std']} in [1.0,1.5]={cond_peak}; "
        f"rho={stats['spearman_rho']:.3f}<=-0.3={cond_rho}; "
        f"signs={stats['sign_changes']}<=1={cond_signs}; "
        f"disc@2.0={_disc_at(d, 2.0)}>=10={cond_disc20}; "
        f"disc@2.5={_disc_at(d, 2.5)}>=7={cond_disc25}"
    )
    return passed, detail


def evaluate_cat2(disc_by_n_std, stats) -> tuple[bool, str]:
    """Stable plateau — PASS if all required criteria met."""
    d = _normalised(disc_by_n_std)
    meaningful = _meaningful_grid(d)
    if not meaningful:
        return False, "no meaningful range data"
    n_stds = [n for n, _ in meaningful]
    discs = [v for _, v in meaningful]
    # Find longest contiguous run of disc > +15 pp
    longest_run_start = -1
    longest_run_end = -1
    cur_start = -1
    for i, v in enumerate(discs):
        if v > 15:
            if cur_start == -1:
                cur_start = i
            if (i - cur_start) > (longest_run_end - longest_run_start):
                longest_run_start = cur_start
                longest_run_end = i
        else:
            cur_start = -1
    run_len = longest_run_end - longest_run_start + 1 if longest_run_start != -1 else 0
    cond_run = run_len >= 4
    # Must include at least one tier in [1.0, 1.5] AND one in [2.0, 2.5]
    if longest_run_start != -1:
        run_n_stds = n_stds[longest_run_start:longest_run_end + 1]
        cond_loose = any(1.0 <= n <= 1.5 for n in run_n_stds)
        cond_strict = any(2.0 <= n <= 2.5 for n in run_n_stds)
        run_discs = discs[longest_run_start:longest_run_end + 1]
        plateau_max = max(run_discs)
        plateau_min = min(run_discs)
        cond_variation = (plateau_max - plateau_min) <= 0.5 * plateau_max
    else:
        cond_loose = cond_strict = cond_variation = False
        run_n_stds = []
    cond_signs = stats["sign_changes"] <= 1
    passed = all([cond_run, cond_loose, cond_strict, cond_variation, cond_signs])
    detail = (
        f"run_len={run_len}>=4={cond_run}; "
        f"run={run_n_stds}; "
        f"includes_loose=[1.0,1.5]={cond_loose}; includes_strict=[2.0,2.5]={cond_strict}; "
        f"variation_<=50%={cond_variation}; signs<=1={cond_signs}"
    )
    return passed, detail


def evaluate_cat3(disc_by_n_std, stats) -> tuple[bool, str]:
    """Rising / late-peak — PASS if all required criteria met."""
    d = _normalised(disc_by_n_std)
    if stats["peak_n_std"] is None:
        return False, "no meaningful range data"
    meaningful = _meaningful_grid(d)
    cond_peak_gt_15 = stats["peak_n_std"] > 1.5
    cond_peak_disc = stats["peak_disc"] >= 15
    cond_disc20 = (_disc_at(d, 2.0) or -999) >= 10
    cond_signs = stats["sign_changes"] <= 1
    # Positive across [1.0, peak] inclusive
    rise_range = [(n, v) for n, v in meaningful if 1.0 <= n <= stats["peak_n_std"]]
    cond_positive = all(v > 0 for _, v in rise_range)
    passed = all([cond_peak_gt_15, cond_peak_disc, cond_disc20, cond_signs, cond_positive])
    detail = (
        f"peak={stats['peak_n_std']}>1.5={cond_peak_gt_15}; "
        f"peak_disc={stats['peak_disc']:.1f}>=15={cond_peak_disc}; "
        f"disc@2.0={_disc_at(d, 2.0)}>=10={cond_disc20}; "
        f"signs={stats['sign_changes']}<=1={cond_signs}; "
        f"positive_across_rise={cond_positive}"
    )
    return passed, detail


def evaluate_cat4(disc_by_n_std, stats) -> tuple[bool, str]:
    """Bumpy with sign changes — FAIL if any trigger fires."""
    d = _normalised(disc_by_n_std)
    if stats["sign_changes"] is None:
        return False, "no meaningful range data"
    meaningful = _meaningful_grid(d)
    discs = [v for _, v in meaningful]
    cond_signs2 = stats["sign_changes"] >= 2
    cond_spearman_flat = -0.1 <= stats["spearman_rho"] <= 0.1
    cond_any_neg5 = any(v <= -5 for v in discs)
    trigger_flat_neg = cond_spearman_flat and cond_any_neg5
    cond_max_neg = stats["max_neg_disc"] <= -10
    triggered = cond_signs2 or trigger_flat_neg or cond_max_neg
    detail = (
        f"signs>=2={cond_signs2}; "
        f"(rho in [-0.1,0.1] AND any disc<=-5)={trigger_flat_neg}; "
        f"max_neg={stats['max_neg_disc']:.1f}<=-10={cond_max_neg}"
    )
    return triggered, detail


def evaluate_cat5(disc_by_n_std, stats) -> tuple[bool, str]:
    """Loose-tail noise — FAIL if all triggers fire."""
    d = _normalised(disc_by_n_std)
    if stats["peak_n_std"] is None:
        return False, "no meaningful range data"
    cond_peak_low = stats["peak_n_std"] <= 1.0
    # disc at peak + 1.0
    target = stats["peak_n_std"] + 1.0
    disc_at_target = _disc_at(d, target)
    if disc_at_target is None or stats["peak_disc"] == 0:
        cond_drop = False
    else:
        cond_drop = disc_at_target <= 0.25 * stats["peak_disc"]
    cond_disc20_low = (_disc_at(d, 2.0) or 999) <= 5
    triggered = cond_peak_low and cond_drop and cond_disc20_low
    detail = (
        f"peak<=1.0={cond_peak_low}; "
        f"disc@peak+1={disc_at_target}<=25%_of_peak={cond_drop}; "
        f"disc@2.0<=5={cond_disc20_low}"
    )
    return triggered, detail


def apply_v2_verdict(disc_by_n_std: Mapping[float, float]) -> dict:
    """Apply v2 criteria to a disc-vs-N_std curve.

    Returns dict with verdict (RESCUE/CLOSE/AMBIGUOUS), category
    matches per cat, shape stats, and detail trace.
    """
    stats = compute_shape_stats(disc_by_n_std)
    cat1_pass, cat1_detail = evaluate_cat1(disc_by_n_std, stats)
    cat2_pass, cat2_detail = evaluate_cat2(disc_by_n_std, stats)
    cat3_pass, cat3_detail = evaluate_cat3(disc_by_n_std, stats)
    cat4_fail, cat4_detail = evaluate_cat4(disc_by_n_std, stats)
    cat5_fail, cat5_detail = evaluate_cat5(disc_by_n_std, stats)

    any_pass = cat1_pass or cat2_pass or cat3_pass
    any_fail = cat4_fail or cat5_fail

    # Rule (i): PASS + FAIL = CLOSE wins
    # Rule (ii): only PASS = RESCUE
    # Rule (iii): only FAIL = CLOSE
    # Rule (iv): neither = AMBIGUOUS (defaults to CLOSE)
    if any_pass and any_fail:
        verdict = "CLOSE"
        rule = "Rule (i): PASS+FAIL -> CLOSE wins"
    elif any_pass:
        verdict = "RESCUE"
        rule = "Rule (ii): PASS only -> RESCUE"
    elif any_fail:
        verdict = "CLOSE"
        rule = "Rule (iii): FAIL only -> CLOSE"
    else:
        verdict = "AMBIGUOUS"
        rule = "Rule (iv): no category matched -> AMBIGUOUS (defaults to CLOSE)"

    return {
        "verdict": verdict,
        "rule_applied": rule,
        "shape_stats": stats,
        "cat1_canonical_decline": {"pass": cat1_pass, "detail": cat1_detail},
        "cat2_stable_plateau": {"pass": cat2_pass, "detail": cat2_detail},
        "cat3_rising_late_peak": {"pass": cat3_pass, "detail": cat3_detail},
        "cat4_bumpy_sign_changes": {"fail_triggered": cat4_fail, "detail": cat4_detail},
        "cat5_loose_tail_noise": {"fail_triggered": cat5_fail, "detail": cat5_detail},
    }
