"""HA07d v2 diagnostic — re-evaluate HA07d v1 fine-grid data under v2 criteria."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
METHODOLOGY_DIR = HERE.parent.parent / "methodology"
sys.path.insert(0, str(METHODOLOGY_DIR))
from v2_criteria import apply_v2_verdict  # noqa: E402

V1_RESULT = HERE.parent / "HA07d-threshold-monotonicity-diagnostic" / "result-data.json"
OUT_JSON = HERE / "result-data.json"


def main():
    if not V1_RESULT.exists():
        print(f"ERROR: v1 result-data not found at {V1_RESULT}", file=sys.stderr)
        return 1
    v1 = json.loads(V1_RESULT.read_text(encoding="utf-8"))
    table = v1["table"]

    print("=" * 70)
    print("HA07d v2 diagnostic — apply v2 criteria to v1 fine-grid data")
    print("=" * 70)

    results = {}
    for direction in ["bidirectional", "one_sided_elevated", "one_sided_lowered"]:
        results[direction] = {}
        for era in ["train", "validate"]:
            era_table = table[direction][era]
            disc_by_n_std = {}
            for n_std_key, entry in era_table.items():
                if "disc_pp" in entry:
                    disc_by_n_std[float(n_std_key)] = entry["disc_pp"]
            v2 = apply_v2_verdict(disc_by_n_std)
            results[direction][era] = v2

    for era in ["train", "validate"]:
        print(f"\n--- PRIMARY ARM ({era} bidirectional) ---")
        _print_verdict(results["bidirectional"][era])

    OUT_JSON.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}")
    return 0


def _print_verdict(v2):
    print(f"Verdict: {v2['verdict']}")
    print(f"Rule applied: {v2['rule_applied']}")
    s = v2["shape_stats"]
    print(f"Shape stats (meaningful range [1.0, 3.0]):")
    print(f"  n_meaningful_tiers: {s['n_meaningful_tiers']}")
    print(f"  peak_n_std: {s['peak_n_std']}; peak_disc: {s['peak_disc']:.1f}")
    print(f"  sign_changes (zero-crossings): {s['sign_changes']}")
    print(f"  direction_reversals (descriptive): {s['direction_reversals']}")
    print(f"  spearman_rho: {s['spearman_rho']:+.3f}")
    print(f"  max_neg_disc: {s['max_neg_disc']:.1f}")
    for cat_name in ["cat1_canonical_decline", "cat2_stable_plateau",
                     "cat3_rising_late_peak", "cat4_bumpy_sign_changes",
                     "cat5_loose_tail_noise"]:
        cat = v2[cat_name]
        if "pass" in cat:
            status = "PASS" if cat["pass"] else "no"
        else:
            status = "FAIL TRIGGERED" if cat["fail_triggered"] else "no"
        print(f"  {cat_name}: {status}")
        print(f"    detail: {cat['detail']}")


if __name__ == "__main__":
    raise SystemExit(main())
