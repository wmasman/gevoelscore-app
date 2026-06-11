"""H05 — Recovery time after crashes (descriptive).

Implements hypothesis.md exactly. No train/validate split; outputs the
recovery-time distribution across all crash_v1 episodes and a secondary
era comparison.
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)

LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3

PRE_BASELINE_DAYS = 30
RECOVERY_GAP = 1  # within 1 point of pre-episode baseline
TRIMMED_PCT = 0.10
MIN_PRE_BASELINE_VALID = 20
MIN_POST_EPISODE_DAYS = 31  # exclude episodes too close to window end

HERE = Path(__file__).resolve().parent
DAY_ENTRIES_CSV = HERE / "day_entries.csv"
OUT_DATA = HERE / "result-data.json"
OUT_HIST_PNG = HERE / "result-histogram.png"


def load_day_entries() -> dict[date, int]:
    if not DAY_ENTRIES_CSV.exists():
        sys.exit(f"\nERROR: {DAY_ENTRIES_CSV} not found.\n")
    out: dict[date, int] = {}
    with DAY_ENTRIES_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            s = r["score"]
            if s in ("", "None", None):
                continue
            out[d] = int(s)
    return out


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


def trimmed_mean(values, trim_pct):
    if not values:
        return None
    vs = sorted(values)
    n = len(vs)
    trim = int(n * trim_pct)
    if n - 2 * trim < 1:
        return statistics.mean(vs)
    return statistics.mean(vs[trim : n - trim])


def main() -> int:
    print("Loading day_entries…")
    day_scores = load_day_entries()
    print(f"  {len(day_scores)} day_entries with score")

    print("Detecting crash_v1 episodes…")
    episodes = find_crash_episodes(day_scores)
    print(f"  {len(episodes)} crash_v1 episodes")

    per_episode = []
    excluded_endwindow = 0
    excluded_baseline = 0
    completed = []
    censored = []
    completed_train, completed_validate = [], []

    # For censoring, build a sorted set of all crash start days
    crash_starts_sorted = sorted(ep["start"] for ep in episodes)

    for ep in episodes:
        ep_start = ep["start"]
        ep_end = ep["end"]
        ep_span = (ep_end - ep_start).days + 1

        # Exclusion: too close to analysis window end
        if (VALIDATE_END - ep_end).days < MIN_POST_EPISODE_DAYS:
            per_episode.append({
                "episode_start": ep_start.isoformat(),
                "episode_end": ep_end.isoformat(),
                "episode_span_days": ep_span,
                "status": "excluded_too_close_to_window_end",
            })
            excluded_endwindow += 1
            continue

        # Pre-episode baseline
        baseline_start = ep_start - timedelta(days=PRE_BASELINE_DAYS)
        baseline_end = ep_start - timedelta(days=1)
        d = baseline_start
        baseline_scores = []
        while d <= baseline_end:
            if d in day_scores:
                baseline_scores.append(day_scores[d])
            d += timedelta(days=1)
        if len(baseline_scores) < MIN_PRE_BASELINE_VALID:
            per_episode.append({
                "episode_start": ep_start.isoformat(),
                "episode_end": ep_end.isoformat(),
                "episode_span_days": ep_span,
                "baseline_valid_n": len(baseline_scores),
                "status": "excluded_insufficient_baseline",
            })
            excluded_baseline += 1
            continue

        baseline = trimmed_mean(baseline_scores, TRIMMED_PCT)
        recovery_target = baseline - RECOVERY_GAP

        # Find next crash start (for censoring)
        next_crash_start = next(
            (cs for cs in crash_starts_sorted if cs > ep_end), None
        )

        # Walk forward day by day
        rec_day = ep_end + timedelta(days=1)
        recovery_days = None
        censored_by_next_crash = False
        while rec_day <= VALIDATE_END:
            if next_crash_start and rec_day >= next_crash_start:
                censored_by_next_crash = True
                break
            if rec_day in day_scores and day_scores[rec_day] >= recovery_target:
                recovery_days = (rec_day - ep_end).days - 1  # day_after_end → 0
                break
            rec_day += timedelta(days=1)

        rec = {
            "episode_start": ep_start.isoformat(),
            "episode_end": ep_end.isoformat(),
            "episode_span_days": ep_span,
            "baseline_valid_n": len(baseline_scores),
            "pre_baseline_score": round(baseline, 2),
            "recovery_target": round(recovery_target, 2),
            "in_train": ep_start <= TRAIN_END,
            "in_validate": TRAIN_END < ep_start <= VALIDATE_END,
        }
        if censored_by_next_crash:
            rec["status"] = "censored_by_next_crash"
            rec["recovery_days"] = None
            censored.append(rec)
        elif recovery_days is None:
            rec["status"] = "no_recovery_in_window"
            rec["recovery_days"] = None
            censored.append(rec)
        else:
            rec["status"] = "recovered"
            rec["recovery_days"] = recovery_days
            completed.append(recovery_days)
            if rec["in_train"]:
                completed_train.append(recovery_days)
            elif rec["in_validate"]:
                completed_validate.append(recovery_days)
        per_episode.append(rec)

    print(f"\n=== summary ===")
    print(f"  total episodes: {len(episodes)}")
    print(f"  excluded too-close-to-window-end: {excluded_endwindow}")
    print(f"  excluded insufficient baseline: {excluded_baseline}")
    print(f"  completed recoveries: {len(completed)}")
    print(f"  censored by next crash: {len(censored)}")
    if completed:
        print(f"\n  recovery time distribution (n={len(completed)}):")
        print(f"    median: {statistics.median(completed)} days")
        print(f"    mean:   {statistics.mean(completed):.1f} days")
        sorted_c = sorted(completed)
        n = len(sorted_c)
        p25 = sorted_c[n // 4]
        p75 = sorted_c[(3 * n) // 4]
        print(f"    IQR (p25-p75): {p25}-{p75} days")
        print(f"    range: {min(sorted_c)}-{max(sorted_c)} days")
        # histogram counts
        buckets = {"0 days": 0, "1-2 days": 0, "3-5 days": 0, "6-10 days": 0, "11+ days": 0}
        for v in completed:
            if v == 0: buckets["0 days"] += 1
            elif v <= 2: buckets["1-2 days"] += 1
            elif v <= 5: buckets["3-5 days"] += 1
            elif v <= 10: buckets["6-10 days"] += 1
            else: buckets["11+ days"] += 1
        for k, v in buckets.items():
            print(f"      {k}: {v}")

    def summarise(values):
        if not values: return None
        s = sorted(values)
        n = len(s)
        return {
            "n": n,
            "median": statistics.median(s),
            "mean": round(statistics.mean(s), 2),
            "p25": s[n // 4],
            "p75": s[(3 * n) // 4],
            "min": s[0],
            "max": s[-1],
        }

    # Era breakdown
    print(f"\n  --- by era (descriptive only) ---")
    print(f"  train (2022-2023, pre-cliff): n_completed={len(completed_train)}, summary={summarise(completed_train)}")
    print(f"  validate (2024+, post-cliff): n_completed={len(completed_validate)}, summary={summarise(completed_validate)}")

    OUT_DATA.write_text(
        json.dumps(
            {
                "params": {
                    "pre_baseline_days": PRE_BASELINE_DAYS,
                    "recovery_gap": RECOVERY_GAP,
                    "trimmed_pct": TRIMMED_PCT,
                    "min_pre_baseline_valid": MIN_PRE_BASELINE_VALID,
                    "min_post_episode_days": MIN_POST_EPISODE_DAYS,
                    "analysis_start": ANALYSIS_START.isoformat(),
                    "train_end": TRAIN_END.isoformat(),
                    "validate_end": VALIDATE_END.isoformat(),
                },
                "counts": {
                    "day_entries": len(day_scores),
                    "episodes": len(episodes),
                    "excluded_endwindow": excluded_endwindow,
                    "excluded_baseline": excluded_baseline,
                    "completed": len(completed),
                    "censored": len(censored),
                },
                "overall_distribution": summarise(completed),
                "train_era_distribution": summarise(completed_train),
                "validate_era_distribution": summarise(completed_validate),
                "per_episode": per_episode,
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    print(f"\nwrote {OUT_DATA}")

    # Histogram plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 4))
        bins = list(range(0, max(completed) + 2)) if completed else [0, 1]
        if completed_train:
            ax.hist(completed_train, bins=bins, alpha=0.6, label=f"train era 2022-23 (n={len(completed_train)})")
        if completed_validate:
            ax.hist(completed_validate, bins=bins, alpha=0.6, label=f"validate era 2024+ (n={len(completed_validate)})")
        ax.set_xlabel("recovery time (days)")
        ax.set_ylabel("episodes")
        ax.set_title("H05 — recovery-time distribution after crash_v1 episodes")
        ax.legend()
        fig.tight_layout()
        fig.savefig(OUT_HIST_PNG)
        plt.close(fig)
    except ImportError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
