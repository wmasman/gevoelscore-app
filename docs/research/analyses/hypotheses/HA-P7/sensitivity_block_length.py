#!/usr/bin/env python3
"""
HA-P7 block-length sensitivity addendum (post-result, factor-of-2 review).

Context:
  The locked test.py run (2026-06-15, result.md) fired the data-driven
  E[L]* factor-of-2 flag: E[L]* on `crash_count_14d` = 11.97 days vs the
  locked default E[L] = 7. Per
  methodology/permutation_null_block_length.md Sec 2 operational
  consequence, a review is required before locking the verdict.

  The locked verdict at E[L]=7 is NOT-SUPPORTED on all three Sec 5.1
  criteria (OR CI 1.130 [0.875, 1.266] contains 1; monotonicity violated;
  3-of-3 W-window CIs contain 1; perm p = 0.1682).

  This script recomputes the HEADLINE CELL ONLY (pooled-LC x W=14 x
  primary outcome `is_crash at d`) at three block lengths to verify the
  verdict is robust:
    - E[L] = 7   (locked spec; should reproduce result.md's headline,
                  modulo RNG-resampling differences at lower B)
    - E[L] = 12  (rounded data-driven E[L]*)
    - E[L] = 14  (2x locked; further sensitivity / cap of the factor-of-2
                  range)

  For each, reports OR + 95% CI + block-permutation p-value.

  Locked test.py uses B = 10,000 for the headline. This sensitivity
  addendum uses B = 2000 (per-cell) to keep runtime manageable; the
  purpose is to verify the NOT-SUPPORTED verdict is structurally robust
  to longer block lengths, not to re-emit the headline. CI half-widths at
  B=2000 are wider than at B=10,000 but adequate for a robustness check.

  Output: sensitivity_block_length.json alongside the script.

Run from anywhere:
    python docs/research/analyses/hypotheses/HA-P7/sensitivity_block_length.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import test as _test  # noqa: E402  (intentional: relative import after sys.path)


B_SENSITIVITY = 2000
EL_VALUES = [7, 12, 14]


def main() -> int:
    print("Loading per_day_master.csv via test.py routines ...")
    _test.load_env()
    df = _test.load_master()
    print("  rows: %d, dates %s -> %s" % (len(df), df["date"].min(), df["date"].max()))

    print("Building features ...")
    df = _test.build_features(df)

    W = _test.PRIMARY_W
    print("  primary window W = %d days" % W)

    X, y = _test.build_xy(df, W, for_phase=False, phase=None, era_filter=None)
    n = int(len(y))
    n_pos = int(y.sum())
    print("  pooled-LC x W=%d cell: n=%d, positives=%d" % (W, n, n_pos))

    results: dict = {
        "headline_cell": f"pooled-LC x W={W} x primary outcome is_crash at d",
        "n": n,
        "positives": n_pos,
        "B": int(B_SENSITIVITY),
        "el_star_observed_in_result_md": 11.97,
        "el_locked_in_spec": int(_test.E_BLOCK_LEN),
        "rng_seed_base": int(_test.RANDOM_SEED),
        "by_block_length": {},
    }

    for el in EL_VALUES:
        print("")
        print("E[L] = %d:" % el)
        print("  bootstrap CI (B=%d) ..." % B_SENSITIVITY)
        rng_b = np.random.default_rng(_test.RANDOM_SEED + el)
        ci = _test.bootstrap_logit_ci((X, y), B_SENSITIVITY, rng_b, expected_block_len=el)
        or_point = float(np.exp(ci["point"])) if not np.isnan(ci["point"]) else float("nan")
        or_lo = float(np.exp(ci["ci_lo"])) if not np.isnan(ci["ci_lo"]) else float("nan")
        or_hi = float(np.exp(ci["ci_hi"])) if not np.isnan(ci["ci_hi"]) else float("nan")
        ci_contains_1 = bool((ci["ci_lo"] <= 0.0 <= ci["ci_hi"])) if (
            not np.isnan(ci["ci_lo"]) and not np.isnan(ci["ci_hi"])
        ) else None
        print("    OR = %.3f [%.3f, %.3f]   CI contains 1: %s   n_converged=%d/%d" % (
            or_point, or_lo, or_hi,
            "YES" if ci_contains_1 else ("NO" if ci_contains_1 is False else "n/a"),
            ci["n_converged"], ci["n_boot"]))

        print("  block-permutation null (B=%d) ..." % B_SENSITIVITY)
        rng_p = np.random.default_rng(_test.RANDOM_SEED + el + 1000)
        perm = _test.block_permutation_pvalue(df, W, B_SENSITIVITY, rng_p, expected_block_len=el)
        p = float(perm["p_value"]) if not np.isnan(perm["p_value"]) else float("nan")
        print("    p (one-sided positive) = %.4f   n_converged=%d/%d" % (
            p, perm["n_converged"], perm["n_perm"]))

        results["by_block_length"][f"EL_{el}"] = {
            "expected_block_len": int(el),
            "or_point": or_point,
            "or_lo": or_lo,
            "or_hi": or_hi,
            "ci_contains_1": ci_contains_1,
            "n_converged_boot": int(ci["n_converged"]),
            "p_value_one_sided_positive": p,
            "n_converged_perm": int(perm["n_converged"]),
        }

    out_json = HERE / "sensitivity_block_length.json"
    out_json.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print("")
    print("Wrote %s" % out_json)
    print("")
    print("Summary table:")
    print("  E[L]  OR      95% CI            contains 1  p (one-sided positive)")
    for el in EL_VALUES:
        r = results["by_block_length"][f"EL_{el}"]
        print("  %4d  %.3f   [%.3f, %.3f]   %s         %.4f" % (
            el, r["or_point"], r["or_lo"], r["or_hi"],
            "YES" if r["ci_contains_1"] else ("NO " if r["ci_contains_1"] is False else "n/a"),
            r["p_value_one_sided_positive"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
