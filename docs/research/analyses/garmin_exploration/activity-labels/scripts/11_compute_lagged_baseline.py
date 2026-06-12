"""Compute lagged-baseline ranks + trend slope (Theme A baseline fix).

Addresses the rolling-baseline contamination identified in user's
Part 1 critique (2026-06-06): the 30-day rolling rank computed by
03_compute_daily_features.py absorbs sustained creeps into its own
reference frame. A slow push rebases itself, so push_burden's
discriminative power is least where the risk is highest, which is
the exact failure mode push_burden is meant to catch.

Two complementary metrics, each picked on theoretical grounds for
its own role (not a horse race between competing fixes):

A.1 - Lagged baseline.
   Each of the 4 axes' rank is recomputed against days [d-90, d-30]:
   a 60-day window ending 30 days ago. Excludes the recent candidate
   region. Push burden becomes meaningful again because the reference
   frame doesn't include the recent push it's trying to detect.

A.2 - Trend slope.
   OLS slope of log(1 + effective_exertion_min) regressed on day
   index over the trailing 28 days. Surfaces the creeping-floor
   pattern as a first-class signal rather than letting it absorb
   into the baseline. Units: log-units per day.

Extends activity_features_daily.csv in place with new columns
(parallel to script 03 + script 04 conventions).

Adopted on 2026-06-06 in response to user's Part 1 critique
dated BEFORE any HA02c or HA01b-recomputed rerun. Audit trail
recorded in registry.md sec 4b. Pre-committed SUPPORTED bar
for HA01b-recomputed on the lagged baseline: same as original
(frequency >= 60%, discrimination >= +15 pp). See severity_spec.md
sec Lagged baseline (v3.2) for the full pre-commitment.
"""
from __future__ import annotations

import collections
import csv
import math
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSV_PATH = HERE.parent / "output" / "activity_features_daily.csv"

# A.1 lagged baseline window
LAGGED_WINDOW_START_DAYS = 30  # earliest excluded day (recent candidate region)
LAGGED_WINDOW_END_DAYS = 90    # oldest included day
LAGGED_WINDOW_LEN = LAGGED_WINDOW_END_DAYS - LAGGED_WINDOW_START_DAYS  # 60
MIN_LAGGED_DAYS = 40           # require ~2/3 of 60 days

# LC-era boundary for the LC-era-only lagged variant (added 2026-06-12).
# Date = Monday after the 2022-04-01 to 2022-04-03 "Fietsweekend Ardennen" span
# (annotations.yaml), which followed the corona-ziek-week 2022-03-21 to 2022-03-27
# (per Training-periode span note). User-locked factual marker for the post-corona
# / LC-symptom-onset window — earlier than the LC dx (2022-05-06) and earlier than
# gevoelscore corpus start (2022-09-03). Used to restrict the lagged-baseline
# window for `*_lagged_lcera` columns: only days >= this date contribute to the
# baseline. For days before LCERA_START + 30 + 60 = 2022-08-03, the LC-era window
# is not yet full and the LC-era ranks will be NaN.
LCERA_START = date(2022, 4, 4)

# A.2 trend slope window
SLOPE_WINDOW_DAYS = 28
MIN_SLOPE_DAYS = 21            # require ~3/4 of 28 days

# Class cutoffs (same as 04_classify_exertion.py)
CLASSES = ["none", "light", "moderate", "heavy", "very_heavy"]
CLASS_RANK = {c: i for i, c in enumerate(CLASSES)}

# Push-burden threshold (same as 03_compute_daily_features.py)
PUSH_RANK_THRESHOLD = 0.75

# Sustained-creep flag threshold for slope summary
SLOPE_CREEP_THRESHOLD = 0.05  # ~5% daily growth, doubling in ~14 days


def parse_num(v):
    if v in (None, "", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def rank_to_class(rank: float | None) -> str:
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


def composite(*classes) -> str:
    return max(classes, key=lambda c: CLASS_RANK[c])


def compute_lagged_rank(
    by_date: dict[date, dict],
    sorted_dates: list[date],
    source_key: str,
    out_key: str,
    min_window_date: date | None = None,
) -> int:
    """Percentile rank within days [d-90, d-30].

    Same midrank-for-ties logic as compute_rolling_rank in script 03.
    Returns the number of days that got a valid rank.

    If `min_window_date` is set, baseline window dates earlier than this
    boundary are excluded from `prior_vals`. Used for the LC-era-only
    variant (see LCERA_START) so the lagged baseline does not draw on
    the user's pre-LC healthy-capacity days. Days early enough that the
    filtered window has < MIN_LAGGED_DAYS valid entries still emit "".
    """
    n_valid = 0
    for d in sorted_dates:
        prior_vals: list[float] = []
        for i in range(LAGGED_WINDOW_START_DAYS + 1, LAGGED_WINDOW_END_DAYS + 1):
            wd = d - timedelta(days=i)
            if min_window_date is not None and wd < min_window_date:
                continue
            if wd in by_date:
                v = parse_num(by_date[wd].get(source_key))
                if v is not None:
                    prior_vals.append(v)
        if len(prior_vals) < MIN_LAGGED_DAYS:
            by_date[d][out_key] = ""
            continue
        today = parse_num(by_date[d].get(source_key))
        if today is None:
            by_date[d][out_key] = ""
            continue
        below = sum(1 for v in prior_vals if v < today)
        at_or_below = sum(1 for v in prior_vals if v <= today)
        rank = (below + at_or_below) / (2 * len(prior_vals))
        by_date[d][out_key] = round(rank, 3)
        n_valid += 1
    return n_valid


def compute_slope(
    by_date: dict[date, dict],
    sorted_dates: list[date],
    source_key: str,
    out_key: str,
) -> int:
    """OLS slope of log(1+value) regressed on day index over the
    trailing 28 days (excluding today).

    Returns the number of days with a valid slope.
    """
    n_valid = 0
    for d in sorted_dates:
        xs: list[float] = []
        ys: list[float] = []
        for i in range(1, SLOPE_WINDOW_DAYS + 1):
            wd = d - timedelta(days=i)
            if wd in by_date:
                v = parse_num(by_date[wd].get(source_key))
                if v is not None:
                    xs.append(float(-i))  # negative so most recent has highest x
                    ys.append(math.log1p(v))
        if len(xs) < MIN_SLOPE_DAYS:
            by_date[d][out_key] = ""
            continue
        n = len(xs)
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        num = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
        den = sum((xs[i] - mean_x) ** 2 for i in range(n))
        if den == 0:
            by_date[d][out_key] = ""
            continue
        slope = num / den
        by_date[d][out_key] = round(slope, 5)
        n_valid += 1
    return n_valid


def compute_push_burden_lagged(
    by_date: dict[date, dict],
    sorted_dates: list[date],
    source_rank_key: str = "effective_exertion_rank_lagged",
    out_key: str = "push_burden_7d_lagged",
) -> None:
    """Count of last 7 days (including today) with `source_rank_key` >= 0.75.

    Generalised so the same logic can produce `push_burden_7d_lagged` (from
    the all-era rank) and `push_burden_7d_lagged_lcera` (from the LC-era rank).
    """
    for d in sorted_dates:
        push_days = 0
        for i in range(7):
            wd = d - timedelta(days=i)
            if wd in by_date:
                r = parse_num(by_date[wd].get(source_rank_key))
                if r is not None and r >= PUSH_RANK_THRESHOLD:
                    push_days += 1
        by_date[d][out_key] = push_days


def main():
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    print(f"Loaded {len(rows)} rows from {CSV_PATH.name}")

    by_date = {date.fromisoformat(r["date"]): r for r in rows}
    sorted_dates = sorted(by_date)

    new_cols = [
        "effective_exertion_rank_lagged",
        "step_rank_lagged",
        "max_hr_rank_lagged",
        "vigorous_min_rank_lagged",
        "exertion_class_lagged",
        "class_axis_A_eff_lagged",
        "class_axis_B_step_lagged",
        "class_axis_C_maxhr_lagged",
        "class_axis_D_vig_lagged",
        "push_burden_7d_lagged",
        "effective_exertion_slope_28d",
        # LC-era-only variants (baseline restricted to dates >= LCERA_START).
        # See LCERA_START constant for rationale. Slope is not duplicated:
        # its 28-day window slides into LC era within ~4 weeks of LCERA_START
        # so a separate variant would not differ except at the boundary.
        "effective_exertion_rank_lagged_lcera",
        "step_rank_lagged_lcera",
        "max_hr_rank_lagged_lcera",
        "vigorous_min_rank_lagged_lcera",
        "exertion_class_lagged_lcera",
        "class_axis_A_eff_lagged_lcera",
        "class_axis_B_step_lagged_lcera",
        "class_axis_C_maxhr_lagged_lcera",
        "class_axis_D_vig_lagged_lcera",
        "push_burden_7d_lagged_lcera",
    ]
    for r in rows:
        for col in new_cols:
            if col not in r:
                r[col] = ""

    print(
        f"\n=== A.1 lagged baseline ranks "
        f"(days [d-{LAGGED_WINDOW_END_DAYS}, d-{LAGGED_WINDOW_START_DAYS}], "
        f"min {MIN_LAGGED_DAYS} of {LAGGED_WINDOW_LEN}) ==="
    )
    n_eff = compute_lagged_rank(
        by_date, sorted_dates, "effective_exertion_min", "effective_exertion_rank_lagged"
    )
    n_step = compute_lagged_rank(
        by_date, sorted_dates, "total_steps", "step_rank_lagged"
    )
    n_mhr = compute_lagged_rank(
        by_date, sorted_dates, "max_hr_uds", "max_hr_rank_lagged"
    )
    n_vig = compute_lagged_rank(
        by_date, sorted_dates, "vigorous_min_uds", "vigorous_min_rank_lagged"
    )
    print(f"  effective_exertion_rank_lagged: {n_eff}/{len(rows)} valid")
    print(f"  step_rank_lagged:               {n_step}/{len(rows)} valid")
    print(f"  max_hr_rank_lagged:             {n_mhr}/{len(rows)} valid")
    print(f"  vigorous_min_rank_lagged:       {n_vig}/{len(rows)} valid")

    # Composite class on lagged ranks
    n_classed = 0
    for r in rows:
        eff = parse_num(r.get("effective_exertion_rank_lagged"))
        step = parse_num(r.get("step_rank_lagged"))
        mhr = parse_num(r.get("max_hr_rank_lagged"))
        vig = parse_num(r.get("vigorous_min_rank_lagged"))
        if all(v is None for v in (eff, step, mhr, vig)):
            r["exertion_class_lagged"] = ""
            r["class_axis_A_eff_lagged"] = ""
            r["class_axis_B_step_lagged"] = ""
            r["class_axis_C_maxhr_lagged"] = ""
            r["class_axis_D_vig_lagged"] = ""
            continue
        a = rank_to_class(eff)
        b = rank_to_class(step)
        c = rank_to_class(mhr)
        dcls = rank_to_class(vig)
        r["class_axis_A_eff_lagged"] = a
        r["class_axis_B_step_lagged"] = b
        r["class_axis_C_maxhr_lagged"] = c
        r["class_axis_D_vig_lagged"] = dcls
        r["exertion_class_lagged"] = composite(a, b, c, dcls)
        n_classed += 1

    # Push burden on all-era lagged baseline
    compute_push_burden_lagged(by_date, sorted_dates)

    # === LC-era-only variants (baseline window restricted to dates >= LCERA_START) ===
    print(
        f"\n=== A.1 LC-era-only lagged baseline ranks "
        f"(LCERA_START={LCERA_START}, window [d-{LAGGED_WINDOW_END_DAYS}, d-{LAGGED_WINDOW_START_DAYS}], "
        f"min {MIN_LAGGED_DAYS} of {LAGGED_WINDOW_LEN}) ==="
    )
    n_eff_l = compute_lagged_rank(
        by_date, sorted_dates, "effective_exertion_min",
        "effective_exertion_rank_lagged_lcera", min_window_date=LCERA_START,
    )
    n_step_l = compute_lagged_rank(
        by_date, sorted_dates, "total_steps",
        "step_rank_lagged_lcera", min_window_date=LCERA_START,
    )
    n_mhr_l = compute_lagged_rank(
        by_date, sorted_dates, "max_hr_uds",
        "max_hr_rank_lagged_lcera", min_window_date=LCERA_START,
    )
    n_vig_l = compute_lagged_rank(
        by_date, sorted_dates, "vigorous_min_uds",
        "vigorous_min_rank_lagged_lcera", min_window_date=LCERA_START,
    )
    print(f"  effective_exertion_rank_lagged_lcera: {n_eff_l}/{len(rows)} valid")
    print(f"  step_rank_lagged_lcera:               {n_step_l}/{len(rows)} valid")
    print(f"  max_hr_rank_lagged_lcera:             {n_mhr_l}/{len(rows)} valid")
    print(f"  vigorous_min_rank_lagged_lcera:       {n_vig_l}/{len(rows)} valid")

    # Classify the LC-era-only variant
    n_classed_l = 0
    for r in rows:
        eff = parse_num(r.get("effective_exertion_rank_lagged_lcera"))
        step = parse_num(r.get("step_rank_lagged_lcera"))
        mhr = parse_num(r.get("max_hr_rank_lagged_lcera"))
        vig = parse_num(r.get("vigorous_min_rank_lagged_lcera"))
        if all(v is None for v in (eff, step, mhr, vig)):
            r["exertion_class_lagged_lcera"] = ""
            r["class_axis_A_eff_lagged_lcera"] = ""
            r["class_axis_B_step_lagged_lcera"] = ""
            r["class_axis_C_maxhr_lagged_lcera"] = ""
            r["class_axis_D_vig_lagged_lcera"] = ""
            continue
        a = rank_to_class(eff)
        b = rank_to_class(step)
        c = rank_to_class(mhr)
        dcls = rank_to_class(vig)
        r["class_axis_A_eff_lagged_lcera"] = a
        r["class_axis_B_step_lagged_lcera"] = b
        r["class_axis_C_maxhr_lagged_lcera"] = c
        r["class_axis_D_vig_lagged_lcera"] = dcls
        r["exertion_class_lagged_lcera"] = composite(a, b, c, dcls)
        n_classed_l += 1
    print(f"  exertion_class_lagged_lcera classified: {n_classed_l}/{len(rows)}")

    # Push burden from the LC-era effective_exertion rank
    compute_push_burden_lagged(
        by_date, sorted_dates,
        source_rank_key="effective_exertion_rank_lagged_lcera",
        out_key="push_burden_7d_lagged_lcera",
    )

    print(
        f"\n=== A.2 trend slope "
        f"(trailing {SLOPE_WINDOW_DAYS} days, min {MIN_SLOPE_DAYS}, "
        f"log(1+effective_exertion_min)) ==="
    )
    n_slope = compute_slope(
        by_date, sorted_dates, "effective_exertion_min", "effective_exertion_slope_28d"
    )
    print(f"  effective_exertion_slope_28d:   {n_slope}/{len(rows)} valid")

    # Distributions
    print(f"\n=== Distribution: exertion_class_lagged (classified: {n_classed}) ===")
    cls_counts = collections.Counter(
        r["exertion_class_lagged"] for r in rows if r["exertion_class_lagged"]
    )
    total_classed = sum(cls_counts.values())
    for c in CLASSES:
        n = cls_counts.get(c, 0)
        pct = 100 * n / total_classed if total_classed else 0
        print(f"  {c:>11}: {n:>4} days ({pct:>4.1f}%)")
    print(f"  empty (boundary): {len(rows) - total_classed}")

    # Compare original vs lagged class
    print("\n=== Concordance: exertion_class vs exertion_class_lagged (where both valid) ===")
    pairs = collections.Counter()
    for r in rows:
        a = r.get("exertion_class", "")
        b = r.get("exertion_class_lagged", "")
        if a and b:
            pairs[(a, b)] += 1
    same = sum(n for (a, b), n in pairs.items() if a == b)
    total = sum(pairs.values())
    if total:
        print(f"  Same class:      {same}/{total} ({100*same/total:.1f}%)")
        print(f"  Different class: {total - same}/{total} ({100*(total - same)/total:.1f}%)")
        # Heavy+ on lagged but lighter on original (the cases A.1 should catch)
        upshift = sum(
            n for (a, b), n in pairs.items()
            if CLASS_RANK[b] > CLASS_RANK[a]
        )
        downshift = sum(
            n for (a, b), n in pairs.items()
            if CLASS_RANK[b] < CLASS_RANK[a]
        )
        print(f"  Lagged class HIGHER than rolling: {upshift} ({100*upshift/total:.1f}%) <- the A.1 fix surfaces these")
        print(f"  Lagged class LOWER than rolling:  {downshift} ({100*downshift/total:.1f}%)")

    print("\n=== Distribution: push_burden_7d_lagged ===")
    burden_counts = collections.Counter(r.get("push_burden_7d_lagged", "") for r in rows)
    for n in range(8):
        count = burden_counts.get(n, 0)
        pct = 100 * count / len(rows) if rows else 0
        print(f"  {n}: {count:>4} days ({pct:>4.1f}%)")

    # Compare push burden distributions
    print("\n=== Push burden: rolling vs lagged (where both valid) ===")
    burden_pairs = []
    for r in rows:
        a = parse_num(r.get("push_burden_7d"))
        b = parse_num(r.get("push_burden_7d_lagged"))
        if a is not None and b is not None:
            burden_pairs.append((a, b))
    if burden_pairs:
        same = sum(1 for a, b in burden_pairs if a == b)
        higher_lagged = sum(1 for a, b in burden_pairs if b > a)
        lower_lagged = sum(1 for a, b in burden_pairs if b < a)
        n = len(burden_pairs)
        print(f"  Same:                {same}/{n} ({100*same/n:.1f}%)")
        print(f"  Lagged HIGHER:       {higher_lagged}/{n} ({100*higher_lagged/n:.1f}%) <- the A.1 fix surfaces these")
        print(f"  Lagged LOWER:        {lower_lagged}/{n} ({100*lower_lagged/n:.1f}%)")

    # Slope distribution
    slopes = [parse_num(r.get("effective_exertion_slope_28d")) for r in rows]
    slopes = [s for s in slopes if s is not None]
    if slopes:
        slopes_sorted = sorted(slopes)
        n = len(slopes)
        print(f"\n=== Distribution: effective_exertion_slope_28d (n={n}, log-units/day) ===")
        print(f"  min:    {min(slopes):+.4f}")
        print(f"  p10:    {slopes_sorted[n // 10]:+.4f}")
        print(f"  p25:    {slopes_sorted[n // 4]:+.4f}")
        print(f"  median: {statistics.median(slopes):+.4f}")
        print(f"  p75:    {slopes_sorted[3 * n // 4]:+.4f}")
        print(f"  p90:    {slopes_sorted[9 * n // 10]:+.4f}")
        print(f"  max:    {max(slopes):+.4f}")
        n_positive = sum(1 for s in slopes if s > 0)
        n_creep = sum(1 for s in slopes if s > SLOPE_CREEP_THRESHOLD)
        n_decay = sum(1 for s in slopes if s < -SLOPE_CREEP_THRESHOLD)
        print(f"  positive (any creep up): {n_positive}/{n} ({100*n_positive/n:.1f}%)")
        print(
            f"  > +{SLOPE_CREEP_THRESHOLD:.2f} (sustained creep up):   "
            f"{n_creep:>4} days ({100*n_creep/n:.1f}%)"
        )
        print(
            f"  < -{SLOPE_CREEP_THRESHOLD:.2f} (sustained decay down): "
            f"{n_decay:>4} days ({100*n_decay/n:.1f}%)"
        )

    # Write back
    fields = list(rows[0].keys())
    with CSV_PATH.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nWrote lagged + slope columns back to {CSV_PATH}")


if __name__ == "__main__":
    main()
