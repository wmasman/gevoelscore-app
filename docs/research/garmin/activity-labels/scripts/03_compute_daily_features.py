"""Build per-day exertion-feature table.

Merges daily UDS (passive intensity, steps, RHR) with activities
aggregated per day, joins gevoelscore, computes step z-scores, and
emits activity_features_daily.csv.

Locked feature definitions per definition.md §3.3.
"""
from __future__ import annotations

import csv
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent / "output"
DAILY_UDS_CSV = OUT_DIR / "daily_uds.csv"
ACTIVITIES_CSV = OUT_DIR / "activities.csv"
DAY_ENTRIES_CSV = (
    HERE.parent.parent / "hypotheses" / "H02b-stress-spikes" / "day_entries.csv"
)
OUT = OUT_DIR / "activity_features_daily.csv"

# Locked analysis window (matches gevoelscore corpus)
ANALYSIS_START = date(2022, 9, 3)
ANALYSIS_END = date(2026, 6, 5)

# Step-spike rule (definition.md §3.4)
STEP_Z_WINDOW_DAYS = 30
STEP_Z_MIN_PRIOR_DAYS = 20
STEP_SPIKE_Z_THRESHOLD = 1.5
STEP_SPIKE_ABS_FLOOR = 4000
MAD_SCALE = 1.4826  # MAD -> ~ stddev for normal dist


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def parse_int(v):
    if v in (None, "", "None"):
        return None
    try:
        return int(float(v))
    except ValueError:
        return None


def parse_float(v):
    if v in (None, "", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


# Alias for clarity in z-score code
parse_num = parse_float


def aggregate_activities_per_day(activities: list[dict]) -> dict[date, dict]:
    """Group activities by date and aggregate to per-day fields."""
    by_date: dict[date, list[dict]] = {}
    for a in activities:
        if a["activity_type"] == "incident_detected":
            continue  # fall-detection, not exertion
        d = date.fromisoformat(a["start_date"])
        by_date.setdefault(d, []).append(a)

    out = {}
    for d, acts in by_date.items():
        durations = [parse_float(a["duration_min"]) or 0 for a in acts]
        z4plus = [parse_float(a["time_in_zone_4plus_min"]) or 0 for a in acts]
        avg_hrs = [parse_int(a["avg_hr"]) for a in acts]
        max_hrs = [parse_int(a["max_hr"]) for a in acts]
        avg_hrs = [v for v in avg_hrs if v]
        max_hrs = [v for v in max_hrs if v]
        aerobic_tes = [parse_float(a["aerobic_te"]) for a in acts]
        aerobic_tes = [v for v in aerobic_tes if v is not None]
        anaerobic_tes = [parse_float(a["anaerobic_te"]) for a in acts]
        anaerobic_tes = [v for v in anaerobic_tes if v is not None]
        calories = [parse_float(a["calories"]) or 0 for a in acts]
        diff_stress = [parse_float(a["difference_stress"]) for a in acts]
        diff_stress = [v for v in diff_stress if v is not None]
        distances = [parse_float(a["distance_m"]) or 0 for a in acts]
        rpes = [parse_float(a["workout_rpe"]) for a in acts]
        rpes = [v for v in rpes if v is not None]
        feels = [parse_float(a["workout_feel"]) for a in acts]
        feels = [v for v in feels if v is not None]

        types = sorted({a["activity_type"] for a in acts})

        out[d] = {
            "n_activities": len(acts),
            "activity_types": ",".join(types),
            "total_activity_min": sum(durations),
            "max_activity_min": max(durations) if durations else 0,
            "total_calories": sum(calories),
            "max_aerobicTE": max(aerobic_tes) if aerobic_tes else None,
            "max_anaerobicTE": max(anaerobic_tes) if anaerobic_tes else None,
            "max_avgHr": max(avg_hrs) if avg_hrs else None,
            "max_maxHr": max(max_hrs) if max_hrs else None,
            "total_time_zone4plus_min": sum(z4plus),
            "max_differenceStress": (
                max(diff_stress, key=abs) if diff_stress else None
            ),
            "total_distance_km": round(sum(distances) / 1000, 2) if distances else 0,
            "avg_workoutRpe": (
                round(statistics.mean(rpes), 1) if rpes else None
            ),
            "avg_workoutFeel": (
                round(statistics.mean(feels), 1) if feels else None
            ),
        }
    return out


def compute_rolling_rank(
    rows: list[dict],
    source_key: str,
    out_key: str,
) -> None:
    """Add percentile rank column for `source_key` against 30-day baseline.

    For day d, percentile rank of today's value within days [d-30, d-1].
    Range 0-1. Uses midrank for ties (average of strict-below and
    at-or-below ranks), so a day at the median of a tied-zeros baseline
    gets 0.5, not 0 or 1.

    Robust to zero-heavy distributions (effective_exertion_min,
    vigorous_min) where z-score / MAD collapses.
    """
    by_date = {date.fromisoformat(r["date"]): r for r in rows}
    sorted_dates = sorted(by_date)

    for d in sorted_dates:
        prior_vals = []
        for i in range(1, STEP_Z_WINDOW_DAYS + 1):
            wd = d - timedelta(days=i)
            if wd in by_date:
                v = parse_num(by_date[wd].get(source_key))
                if v is not None:
                    prior_vals.append(v)
        if len(prior_vals) < STEP_Z_MIN_PRIOR_DAYS:
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


PUSH_RANK_THRESHOLD = 0.75  # day counts as "pushing" if effective_exertion_rank >= 0.75


def compute_push_burden(rows: list[dict]) -> None:
    """Add push_burden_7d and above_baseline_streak in place.

    push_burden_7d = count of days in [d-6, d] (inclusive of today)
                     with effective_exertion_rank_30d >= 0.75.
                     Range 0-7. A high value means sustained pushing.

    above_baseline_streak = consecutive prior days where rank > 0.5
                            (above-median day). Resets to 0 on the first
                            below-median day.
    """
    by_date = {date.fromisoformat(r["date"]): r for r in rows}
    sorted_dates = sorted(by_date)

    # push_burden_7d
    for d in sorted_dates:
        push_days = 0
        for i in range(7):
            wd = d - timedelta(days=i)
            if wd in by_date:
                r = parse_num(by_date[wd].get("effective_exertion_rank_30d"))
                if r is not None and r >= PUSH_RANK_THRESHOLD:
                    push_days += 1
        by_date[d]["push_burden_7d"] = push_days

    # above_baseline_streak
    streak = 0
    for d in sorted_dates:
        by_date[d]["above_baseline_streak"] = streak
        r_today = parse_num(by_date[d].get("effective_exertion_rank_30d"))
        if r_today is not None and r_today > 0.5:
            streak += 1
        else:
            streak = 0


def main():
    uds_rows = load_csv(DAILY_UDS_CSV)
    activities = load_csv(ACTIVITIES_CSV)
    print(f"Loaded {len(uds_rows)} UDS days, {len(activities)} activities")

    # Day entries (gevoelscore)
    day_scores: dict[date, int] = {}
    for r in load_csv(DAY_ENTRIES_CSV):
        s = r["score"]
        if s in ("", "None"):
            continue
        day_scores[date.fromisoformat(r["date"])] = int(s)
    print(f"  {len(day_scores)} scored days")

    activity_by_date = aggregate_activities_per_day(activities)
    print(f"  {len(activity_by_date)} unique activity-days")

    # Build merged rows for [ANALYSIS_START, ANALYSIS_END]
    uds_by_date: dict[date, dict] = {}
    for r in uds_rows:
        d = date.fromisoformat(r["date"])
        uds_by_date[d] = r

    n_days = (ANALYSIS_END - ANALYSIS_START).days + 1
    merged_rows: list[dict] = []
    for i in range(n_days):
        d = ANALYSIS_START + timedelta(days=i)
        uds = uds_by_date.get(d, {})
        act = activity_by_date.get(d, {})
        score = day_scores.get(d)

        # Passive from UDS
        steps = parse_int(uds.get("total_steps"))
        step_goal = parse_int(uds.get("daily_step_goal"))
        vig_uds = parse_int(uds.get("vigorous_min")) or 0
        mod_uds = parse_int(uds.get("moderate_min")) or 0
        highly_active = parse_int(uds.get("highly_active_sec")) or 0
        active = parse_int(uds.get("active_sec")) or 0
        max_hr_uds = parse_int(uds.get("max_hr"))
        max_avg_hr_uds = parse_int(uds.get("max_avg_hr"))
        is_vigorous_day_uds = uds.get("is_vigorous_day", "")

        # Effective exertion (definition.md §3.3)
        total_act_min = act.get("total_activity_min", 0)
        effective_exertion_min = max(
            total_act_min,
            vig_uds + 0.5 * mod_uds,
        )

        merged_rows.append({
            "date": d.isoformat(),
            "gevoelscore": score if score is not None else "",
            # recorded activities
            "n_activities": act.get("n_activities", 0),
            "activity_types": act.get("activity_types", ""),
            "total_activity_min": round(total_act_min, 1),
            "max_activity_min": round(act.get("max_activity_min", 0), 1),
            "total_calories": round(act.get("total_calories", 0), 0),
            "max_aerobicTE": act.get("max_aerobicTE", ""),
            "max_anaerobicTE": act.get("max_anaerobicTE", ""),
            "max_avgHr": act.get("max_avgHr", ""),
            "max_maxHr": act.get("max_maxHr", ""),
            "total_time_zone4plus_min": round(act.get("total_time_zone4plus_min", 0), 1),
            "max_differenceStress": act.get("max_differenceStress", ""),
            "total_distance_km": act.get("total_distance_km", 0),
            "avg_workoutRpe": act.get("avg_workoutRpe", ""),
            "avg_workoutFeel": act.get("avg_workoutFeel", ""),
            # passive UDS
            "total_steps": steps if steps is not None else "",
            "daily_step_goal": step_goal if step_goal is not None else "",
            "vigorous_min_uds": vig_uds,
            "moderate_min_uds": mod_uds,
            "highly_active_sec": highly_active,
            "active_sec": active,
            "max_hr_uds": max_hr_uds if max_hr_uds is not None else "",
            "max_avg_hr_uds": max_avg_hr_uds if max_avg_hr_uds is not None else "",
            "is_vigorous_day": is_vigorous_day_uds,
            # derived
            "effective_exertion_min": round(effective_exertion_min, 1),
            "step_rank_30d": "",                  # filled below
            "effective_exertion_rank_30d": "",    # filled below
            "max_hr_rank_30d": "",                # filled below
            "vigorous_min_rank_30d": "",          # filled below
            "step_z_30d": "",                     # for backward compat: legacy step_z
            "step_spike": "",                     # filled below
            "push_burden_7d": "",                 # filled below
            "above_baseline_streak": "",          # filled below
        })

    # Percentile ranks against 30-day rolling baseline
    compute_rolling_rank(merged_rows, "total_steps", "step_rank_30d")
    compute_rolling_rank(merged_rows, "effective_exertion_min",
                         "effective_exertion_rank_30d")
    compute_rolling_rank(merged_rows, "max_hr_uds", "max_hr_rank_30d")
    compute_rolling_rank(merged_rows, "vigorous_min_uds", "vigorous_min_rank_30d")

    # Legacy step z-score (kept for comparison / backward compat with step_spike rule)
    # Uses median + MAD on full baseline including zeros.
    by_date = {date.fromisoformat(r["date"]): r for r in merged_rows}
    sorted_dates = sorted(by_date)
    for d in sorted_dates:
        prior_steps = []
        for i in range(1, STEP_Z_WINDOW_DAYS + 1):
            wd = d - timedelta(days=i)
            if wd in by_date:
                s = parse_int(by_date[wd].get("total_steps"))
                if s is not None and s > 0:
                    prior_steps.append(s)
        if len(prior_steps) < STEP_Z_MIN_PRIOR_DAYS:
            continue
        med = statistics.median(prior_steps)
        deviations = [abs(s - med) for s in prior_steps]
        mad = statistics.median(deviations)
        if mad == 0:
            continue
        steps_today = parse_int(by_date[d].get("total_steps"))
        if steps_today is None:
            continue
        z = (steps_today - med) / (MAD_SCALE * mad)
        by_date[d]["step_z_30d"] = round(z, 2)

    # Push burden (uses effective_exertion_rank_30d, so must run after rank scores)
    compute_push_burden(merged_rows)

    # step_spike
    for r in merged_rows:
        z = r["step_z_30d"]
        steps = parse_int(r.get("total_steps"))
        if z == "" or steps is None:
            r["step_spike"] = ""
            continue
        if z >= STEP_SPIKE_Z_THRESHOLD and steps >= STEP_SPIKE_ABS_FLOOR:
            r["step_spike"] = "true"
        else:
            r["step_spike"] = "false"

    fields = list(merged_rows[0].keys())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in merged_rows:
            w.writerow(r)

    # Summary stats
    n_with_score = sum(1 for r in merged_rows if r["gevoelscore"] != "")
    n_with_steps = sum(1 for r in merged_rows if r["total_steps"] != "")
    n_with_z = sum(1 for r in merged_rows if r["step_z_30d"] != "")
    n_step_spikes = sum(1 for r in merged_rows if r["step_spike"] == "true")
    n_with_recorded = sum(
        1 for r in merged_rows if r["n_activities"] and int(r["n_activities"]) > 0
    )
    print(f"\nMerged rows: {len(merged_rows)} days")
    print(f"  with gevoelscore: {n_with_score}")
    print(f"  with UDS steps:   {n_with_steps}")
    print(f"  with step_z_30d:  {n_with_z}")
    print(f"  step_spike days:  {n_step_spikes}")
    print(f"  days with recorded activity: {n_with_recorded}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
