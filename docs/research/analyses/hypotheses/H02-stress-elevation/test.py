"""H02 — Sustained stress elevation before crashes.

Mirrors the protocol in hypothesis.md exactly. Reuses much of H01's
structure but on Garmin's daily averageStressLevel instead of RHR, with
a tighter 3-day lead-up window. Also reports highDuration (seconds in
HIGH stress band) as a secondary metric for result.md, without using
it in the verdict.
"""
from __future__ import annotations

import csv
import json
import random
import statistics
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# ─────────────────────────────────────────────────────────────────
# Locked parameters (mirror hypothesis.md exactly)
# ─────────────────────────────────────────────────────────────────
ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)

LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3

LEADUP_DAYS = 3  # tighter than H01's 7
BASELINE_WINDOW_DAYS = 90

MIN_LEADUP_VALID = 3  # of 3 (no slack — window is small)
MIN_BASELINE_VALID = 30  # of 90
TRIMMED_PCT = 0.10

NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

# Pre-registered thresholds
CRIT_A_FRACTION = 0.60
CRIT_A_DELTA_STRESS = 3  # stress points (0-100 scale)
CRIT_B_DISCRIMINATION_PP = 15
CRIT_C_MEDIAN_STRESS = 2
CRIT_C_LOWER_QUARTILE_STRESS = 0
MIN_EPISODES_PER_WINDOW = 10

# ─────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
DAY_ENTRIES_CSV = HERE / "day_entries.csv"
GARMIN_UDS_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Aggregator"
)
OUT_DATA = HERE / "result-data.json"
OUT_TRAIN_PNG = HERE / "result-train.png"
OUT_VALIDATE_PNG = HERE / "result-validate.png"


# ─────────────────────────────────────────────────────────────────
# Step 1 — day_entries (identical to H01)
# ─────────────────────────────────────────────────────────────────
def load_day_entries() -> dict[date, int]:
    if not DAY_ENTRIES_CSV.exists():
        sys.exit(
            f"\nERROR: {DAY_ENTRIES_CSV} not found.\n"
            f"Run fetch_day_entries.mjs first via run-directus-script.ps1.\n"
        )
    out: dict[date, int] = {}
    with DAY_ENTRIES_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            s = r["score"]
            if s in ("", "None", None):
                continue
            out[d] = int(s)
    return out


# ─────────────────────────────────────────────────────────────────
# Step 2 — crash_v1 detection (identical to H01)
# ─────────────────────────────────────────────────────────────────
def find_crash_episodes(day_scores: dict[date, int]) -> list[dict]:
    sorted_dates = sorted(d for d in day_scores if ANALYSIS_START <= d <= VALIDATE_END)
    runs: list[dict] = []
    cur = None
    for d in sorted_dates:
        is_low = day_scores[d] <= LOW_THRESHOLD
        if not is_low:
            if cur and cur["days"] >= MIN_RUN_DAYS:
                runs.append(cur)
            cur = None
            continue
        if not cur:
            cur = {"start": d, "end": d, "days": 1}
            continue
        if (d - cur["end"]).days == 1:
            cur["end"] = d
            cur["days"] += 1
        else:
            if cur["days"] >= MIN_RUN_DAYS:
                runs.append(cur)
            cur = {"start": d, "end": d, "days": 1}
    if cur and cur["days"] >= MIN_RUN_DAYS:
        runs.append(cur)

    merged: list[dict] = []
    for r in runs:
        if merged and (r["start"] - merged[-1]["end"]).days <= MERGE_WITHIN_DAYS:
            merged[-1]["end"] = r["end"]
            merged[-1]["days"] += r["days"]
        else:
            merged.append({"start": r["start"], "end": r["end"], "days": r["days"]})
    return merged


# ─────────────────────────────────────────────────────────────────
# Step 3 — load daily stress aggregates
# ─────────────────────────────────────────────────────────────────
def load_stress_by_date() -> dict[date, dict]:
    """date -> { avg_stress, high_duration_s, off_wrist_count }"""
    out: dict[date, dict] = {}
    for p in sorted(GARMIN_UDS_DIR.glob("UDSFile_*.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            stress = rec.get("allDayStress") or {}
            agg = stress.get("aggregatorList") or []
            total = next((a for a in agg if a.get("type") == "TOTAL"), None)
            if not cd or not total:
                continue
            avg = total.get("averageStressLevel")
            if avg in (None, -1, -2):  # Garmin uses -1 for off-wrist, -2 for too-active
                continue
            d = date.fromisoformat(cd)
            new_rec = {
                "avg_stress": int(avg),
                "high_duration_s": int(total.get("highDuration", 0) or 0),
                "medium_duration_s": int(total.get("mediumDuration", 0) or 0),
                "off_wrist_count": int(total.get("stressOffWristCount", 0) or 0),
                "max_stress": int(total.get("maxStressLevel", 0) or 0),
            }
            # de-dup across overlapping files: keep the higher-coverage one
            if d in out:
                existing_total = out[d]["high_duration_s"] + out[d]["medium_duration_s"]
                new_total = new_rec["high_duration_s"] + new_rec["medium_duration_s"]
                if new_total <= existing_total:
                    continue
            out[d] = new_rec
    return out


# ─────────────────────────────────────────────────────────────────
# Step 4 — delta_stress for a window
# ─────────────────────────────────────────────────────────────────
def trimmed_mean(values, trim_pct):
    if not values:
        return None
    vs = sorted(values)
    n = len(vs)
    trim = int(n * trim_pct)
    if n - 2 * trim < 1:
        return statistics.mean(vs)
    return statistics.mean(vs[trim : n - trim])


def compute_window(
    ref: date,
    stress_by_date: dict[date, dict],
    field: str,
) -> dict:
    leadup = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    baseline_start = ref - timedelta(days=BASELINE_WINDOW_DAYS + LEADUP_DAYS)
    baseline_end = ref - timedelta(days=LEADUP_DAYS + 1)
    baseline_days = []
    d = baseline_start
    while d <= baseline_end:
        baseline_days.append(d)
        d += timedelta(days=1)

    leadup_vals = [stress_by_date[d][field] for d in leadup if d in stress_by_date]
    baseline_vals = [stress_by_date[d][field] for d in baseline_days if d in stress_by_date]
    leadup_off_wrist = [
        stress_by_date[d]["off_wrist_count"] for d in leadup if d in stress_by_date
    ]
    leadup_valid = len(leadup_vals) >= MIN_LEADUP_VALID
    baseline_valid = len(baseline_vals) >= MIN_BASELINE_VALID
    out = {
        "leadup_n": len(leadup_vals),
        "baseline_n": len(baseline_vals),
        "leadup_valid": leadup_valid,
        "baseline_valid": baseline_valid,
        "leadup_mean": statistics.mean(leadup_vals) if leadup_vals else None,
        "baseline_trimmed_mean": trimmed_mean(baseline_vals, TRIMMED_PCT),
        "delta": None,
        "leadup_mean_off_wrist": (
            statistics.mean(leadup_off_wrist) if leadup_off_wrist else None
        ),
    }
    if leadup_valid and baseline_valid:
        out["delta"] = out["leadup_mean"] - out["baseline_trimmed_mean"]
    return out


# ─────────────────────────────────────────────────────────────────
# Step 5 — null sample
# ─────────────────────────────────────────────────────────────────
def build_null_sample(
    stress_by_date: dict[date, dict],
    crash_lead_up_days: set[date],
    field: str,
    n: int,
) -> list[float]:
    rng = random.Random(RANDOM_SEED)
    all_dates = sorted(
        d for d in stress_by_date if ANALYSIS_START <= d <= VALIDATE_END
    )
    deltas: list[float] = []
    max_attempts = n * 50
    attempts = 0
    while len(deltas) < n and attempts < max_attempts:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)}
        if leadup & crash_lead_up_days:
            continue
        prof = compute_window(ref, stress_by_date, field)
        if prof["delta"] is None:
            continue
        deltas.append(prof["delta"])
    return deltas


# ─────────────────────────────────────────────────────────────────
# Step 6 — evaluate
# ─────────────────────────────────────────────────────────────────
def evaluate(crash_deltas, null_deltas, label):
    if len(crash_deltas) < MIN_EPISODES_PER_WINDOW:
        return {
            "window": label,
            "verdict": "inconclusive",
            "reason": f"only {len(crash_deltas)} usable crash episodes (< {MIN_EPISODES_PER_WINDOW})",
            "crash_n": len(crash_deltas),
            "null_n": len(null_deltas),
        }
    crash_at_thr = sum(1 for v in crash_deltas if v >= CRIT_A_DELTA_STRESS) / len(crash_deltas)
    null_at_thr = (
        sum(1 for v in null_deltas if v >= CRIT_A_DELTA_STRESS) / len(null_deltas)
        if null_deltas
        else 0.0
    )
    median_delta = statistics.median(crash_deltas)
    lower_q = sorted(crash_deltas)[len(crash_deltas) // 4]
    crit_a = crash_at_thr >= CRIT_A_FRACTION
    crit_b = (crash_at_thr - null_at_thr) * 100 >= CRIT_B_DISCRIMINATION_PP
    crit_c = (
        median_delta >= CRIT_C_MEDIAN_STRESS and lower_q >= CRIT_C_LOWER_QUARTILE_STRESS
    )
    return {
        "window": label,
        "crash_n": len(crash_deltas),
        "null_n": len(null_deltas),
        "crash_pct_at_threshold": crash_at_thr,
        "null_pct_at_threshold": null_at_thr,
        "discrimination_pp": (crash_at_thr - null_at_thr) * 100,
        "median_delta": median_delta,
        "lower_quartile_delta": lower_q,
        "criterion_a_pass": crit_a,
        "criterion_b_pass": crit_b,
        "criterion_c_pass": crit_c,
        "verdict": "supported" if (crit_a and crit_b and crit_c) else "refuted",
    }


# ─────────────────────────────────────────────────────────────────
# Step 7 — plot
# ─────────────────────────────────────────────────────────────────
def maybe_plot(crash_deltas, null_deltas, out, title):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print(f"  (matplotlib not installed, skipping {out.name})")
        return
    fig, ax = plt.subplots(figsize=(7, 4))
    bins = list(range(-20, 21))
    ax.hist(
        [null_deltas, crash_deltas],
        bins=bins,
        label=[f"null (n={len(null_deltas)})", f"crash lead-ups (n={len(crash_deltas)})"],
        density=True,
        alpha=0.7,
    )
    ax.axvline(CRIT_A_DELTA_STRESS, color="black", linestyle="--", alpha=0.5)
    ax.set_xlabel("delta_stress  (lead-up mean minus baseline trimmed mean, 0-100 scale)")
    ax.set_ylabel("density")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────
def main() -> int:
    print("Loading day_entries…")
    day_scores = load_day_entries()
    print(f"  {len(day_scores)} day_entries with score")

    print("Detecting crash_v1 episodes…")
    episodes = find_crash_episodes(day_scores)
    print(f"  {len(episodes)} crash_v1 episodes")

    print("Loading Garmin stress aggregates…")
    stress_by_date = load_stress_by_date()
    print(f"  {len(stress_by_date)} days with stress")

    all_leadup_days: set[date] = set()
    for ep in episodes:
        for i in range(1, LEADUP_DAYS + 1):
            all_leadup_days.add(ep["start"] - timedelta(days=i))

    print("Computing per-episode delta_stress (primary: avg_stress)…")
    per_episode = []
    excluded_missing = 0
    excluded_overlap = 0
    for ep in episodes:
        prof_avg = compute_window(ep["start"], stress_by_date, "avg_stress")
        prof_high = compute_window(ep["start"], stress_by_date, "high_duration_s")
        leadup = {ep["start"] - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)}
        other_ep_days: set[date] = set()
        for other in episodes:
            if other["start"] == ep["start"]:
                continue
            d = other["start"]
            while d <= other["end"]:
                other_ep_days.add(d)
                d += timedelta(days=1)
        overlap = bool(leadup & other_ep_days)
        rec = {
            "episode_start": ep["start"].isoformat(),
            "episode_end": ep["end"].isoformat(),
            "in_train": ep["start"] <= TRAIN_END,
            "in_validate": TRAIN_END < ep["start"] <= VALIDATE_END,
            "overlap_with_other_episode": overlap,
            "delta_avg_stress": prof_avg["delta"],
            "delta_high_duration_s": prof_high["delta"],
            "leadup_mean_off_wrist": prof_avg["leadup_mean_off_wrist"],
            "leadup_valid": prof_avg["leadup_valid"],
            "baseline_valid": prof_avg["baseline_valid"],
            "leadup_mean_avg_stress": prof_avg["leadup_mean"],
            "baseline_mean_avg_stress": prof_avg["baseline_trimmed_mean"],
        }
        per_episode.append(rec)
        if not (prof_avg["leadup_valid"] and prof_avg["baseline_valid"]):
            excluded_missing += 1
        elif overlap:
            excluded_overlap += 1

    print(f"  excluded for missing data: {excluded_missing}")
    print(f"  excluded for lead-up overlap: {excluded_overlap}")

    print("Building null sample for avg_stress…")
    null_deltas_avg = build_null_sample(
        stress_by_date, all_leadup_days, "avg_stress", NULL_SAMPLE_SIZE
    )
    print(f"  {len(null_deltas_avg)} null windows")

    # Also high duration for secondary reporting
    print("Building null sample for high_duration_s (secondary)…")
    null_deltas_high = build_null_sample(
        stress_by_date, all_leadup_days, "high_duration_s", NULL_SAMPLE_SIZE
    )

    train_clean = [
        r["delta_avg_stress"]
        for r in per_episode
        if r["in_train"]
        and r["leadup_valid"]
        and r["baseline_valid"]
        and not r["overlap_with_other_episode"]
    ]
    validate_clean = [
        r["delta_avg_stress"]
        for r in per_episode
        if r["in_validate"]
        and r["leadup_valid"]
        and r["baseline_valid"]
        and not r["overlap_with_other_episode"]
    ]
    print(f"  train clean episodes: {len(train_clean)}")
    print(f"  validate clean episodes: {len(validate_clean)}")

    train_eval = evaluate(train_clean, null_deltas_avg, "train")
    validate_eval = evaluate(validate_clean, null_deltas_avg, "validate")

    overall_verdict = (
        "supported"
        if train_eval["verdict"] == "supported" and validate_eval["verdict"] == "supported"
        else "inconclusive"
        if "inconclusive" in (train_eval["verdict"], validate_eval["verdict"])
        else "refuted"
    )

    # Secondary metric stats (descriptive only, not used in verdict)
    train_high = [
        r["delta_high_duration_s"]
        for r in per_episode
        if r["in_train"]
        and r["leadup_valid"]
        and r["baseline_valid"]
        and not r["overlap_with_other_episode"]
        and r["delta_high_duration_s"] is not None
    ]
    validate_high = [
        r["delta_high_duration_s"]
        for r in per_episode
        if r["in_validate"]
        and r["leadup_valid"]
        and r["baseline_valid"]
        and not r["overlap_with_other_episode"]
        and r["delta_high_duration_s"] is not None
    ]

    def summarise(values):
        if not values:
            return None
        return {
            "n": len(values),
            "median": statistics.median(values),
            "mean": statistics.mean(values),
            "p25": sorted(values)[len(values) // 4],
            "p75": sorted(values)[(3 * len(values)) // 4],
        }

    print("\n=== VERDICT ===")
    print(f"  train:    {train_eval}")
    print(f"  validate: {validate_eval}")
    print(f"  overall:  {overall_verdict}")

    OUT_DATA.write_text(
        json.dumps(
            {
                "params": {
                    "leadup_days": LEADUP_DAYS,
                    "baseline_window_days": BASELINE_WINDOW_DAYS,
                    "min_leadup_valid": MIN_LEADUP_VALID,
                    "min_baseline_valid": MIN_BASELINE_VALID,
                    "trimmed_pct": TRIMMED_PCT,
                    "null_sample_size": NULL_SAMPLE_SIZE,
                    "crit_a_fraction": CRIT_A_FRACTION,
                    "crit_a_delta_stress": CRIT_A_DELTA_STRESS,
                    "crit_b_discrimination_pp": CRIT_B_DISCRIMINATION_PP,
                    "crit_c_median_stress": CRIT_C_MEDIAN_STRESS,
                    "crit_c_lower_quartile_stress": CRIT_C_LOWER_QUARTILE_STRESS,
                    "analysis_start": ANALYSIS_START.isoformat(),
                    "train_end": TRAIN_END.isoformat(),
                    "validate_end": VALIDATE_END.isoformat(),
                },
                "counts": {
                    "day_entries": len(day_scores),
                    "stress_days": len(stress_by_date),
                    "episodes": len(episodes),
                    "excluded_missing": excluded_missing,
                    "excluded_overlap": excluded_overlap,
                    "train_clean": len(train_clean),
                    "validate_clean": len(validate_clean),
                    "null_n_avg": len(null_deltas_avg),
                    "null_n_high": len(null_deltas_high),
                },
                "train": train_eval,
                "validate": validate_eval,
                "overall_verdict": overall_verdict,
                "secondary_high_duration_delta_s": {
                    "train": summarise(train_high),
                    "validate": summarise(validate_high),
                    "null_summary": summarise(null_deltas_high),
                },
                "null_avg_stress_summary": summarise(null_deltas_avg),
                "per_episode": per_episode,
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    print(f"\nwrote {OUT_DATA}")

    maybe_plot(train_clean, null_deltas_avg, OUT_TRAIN_PNG, "H02 — delta avgStress before crashes, TRAIN")
    maybe_plot(
        validate_clean, null_deltas_avg, OUT_VALIDATE_PNG, "H02 — delta avgStress before crashes, VALIDATE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
