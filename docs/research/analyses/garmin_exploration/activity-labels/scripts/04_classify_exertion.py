"""Apply the proposed exertion_class cutoffs from spec/severity_spec.md.

Computes class from 4 axes (effective_exertion_min, step_z_30d,
total_steps, max_hr_uds), takes the max, writes back to
activity_features_daily.csv with a new `exertion_class` column and
per-axis breakdown columns for transparency.

Prints class distribution + per-axis attribution so the cutoffs can
be verified before locking.
"""
from __future__ import annotations

import csv
import collections
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSV_PATH = HERE.parent / "output" / "activity_features_daily.csv"

# Ordering
CLASSES = ["none", "light", "moderate", "heavy", "very_heavy"]
CLASS_RANK = {c: i for i, c in enumerate(CLASSES)}


def parse_num(v):
    if v in (None, "", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def rank_to_class(rank: float | None) -> str:
    """Universal rank -> class mapping. Same thresholds for all axes."""
    if rank is None:
        return "none"
    if rank < 0.5:
        return "none"
    if rank < 0.75:
        return "light"
    if rank < 0.85:
        return "moderate"
    if rank < 0.95:
        return "heavy"
    return "very_heavy"


def push_burden_to_class(n_push_days: float | None) -> str:
    """push_burden_7d count of days at rank >= 0.75 in last 7."""
    if n_push_days is None:
        return "none"
    if n_push_days < 1:
        return "none"
    if n_push_days < 2:
        return "light"
    if n_push_days < 3:
        return "moderate"
    if n_push_days < 5:
        return "heavy"
    return "very_heavy"


def composite(*classes) -> str:
    return max(classes, key=lambda c: CLASS_RANK[c])


def main():
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    print(f"Loaded {len(rows)} rows from {CSV_PATH.name}")

    # Add columns
    for r in rows:
        eff_rank = parse_num(r.get("effective_exertion_rank_30d"))
        step_rank = parse_num(r.get("step_rank_30d"))
        max_hr_rank = parse_num(r.get("max_hr_rank_30d"))
        vig_rank = parse_num(r.get("vigorous_min_rank_30d"))
        push_n = parse_num(r.get("push_burden_7d"))

        a = rank_to_class(eff_rank)
        b = rank_to_class(step_rank)
        c = rank_to_class(max_hr_rank)
        d = rank_to_class(vig_rank)
        r["exertion_class"] = composite(a, b, c, d)
        r["class_axis_A_eff"] = a
        r["class_axis_B_step"] = b
        r["class_axis_C_maxhr"] = c
        r["class_axis_D_vig"] = d
        # Push burden as a separate orthogonal class
        r["push_burden_class"] = push_burden_to_class(push_n)

    # Distribution
    class_counts = collections.Counter(r["exertion_class"] for r in rows)
    print("\n=== Composite exertion_class distribution ===")
    for c in CLASSES:
        n = class_counts.get(c, 0)
        pct = 100 * n / len(rows)
        print(f"  {c:>11}: {n:>4} days ({pct:>4.1f}%)")

    # Per-axis attribution: which axis drove the class for each day?
    print("\n=== Driving axis (which axis dictated the composite class) ===")
    drivers = collections.Counter()
    for r in rows:
        cls = r["exertion_class"]
        axes_at_max = []
        if r["class_axis_A_eff"] == cls:
            axes_at_max.append("A_eff")
        if r["class_axis_B_step"] == cls:
            axes_at_max.append("B_step")
        if r["class_axis_C_maxhr"] == cls:
            axes_at_max.append("C_maxhr")
        if r["class_axis_D_vig"] == cls:
            axes_at_max.append("D_vig")
        drivers[(cls, "+".join(axes_at_max))] += 1
    for (cls, axes), n in sorted(drivers.items(), key=lambda x: (CLASS_RANK[x[0][0]], -x[1])):
        if n >= 3:
            print(f"  {cls:>11} via {axes:30}: {n}")

    print("\n=== push_burden_class distribution (independent from exertion_class) ===")
    push_counts = collections.Counter(r["push_burden_class"] for r in rows)
    for c in CLASSES:
        n = push_counts.get(c, 0)
        pct = 100 * n / len(rows)
        print(f"  {c:>11}: {n:>4} days ({pct:>4.1f}%)")

    # Write back
    fields = list(rows[0].keys())
    with CSV_PATH.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nWrote exertion_class + per-axis columns back to {CSV_PATH}")


if __name__ == "__main__":
    main()
