"""K02 — Crash duration shifted across recovery eras.

Mirrors K01 structurally; the metric is episode span instead of nadir.
"""
from __future__ import annotations

import csv
import json
import random
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

ANALYSIS_START = date(2022, 9, 3)
ERA_SPLIT = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)

LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3

PERMUTATIONS = 10_000
RANDOM_SEED = 20260605

CRIT_A_DELTA_MIN_DAYS = 1
CRIT_B_P_MAX = 0.10
MIN_EPISODES_PER_ERA = 8

HERE = Path(__file__).resolve().parent
DAY_ENTRIES_CSV = HERE / "day_entries.csv"
OUT_DATA = HERE / "result-data.json"
OUT_PNG = HERE / "result-histogram.png"


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


def summarise(values):
    if not values: return {"n": 0}
    s = sorted(values); n = len(s)
    return {
        "n": n, "min": s[0], "max": s[-1],
        "median": statistics.median(s),
        "mean": round(statistics.mean(s), 2),
        "p25": s[n // 4], "p75": s[(3 * n) // 4],
    }


def main() -> int:
    print("Loading day_entries…")
    day_scores = load_day_entries()
    print(f"  {len(day_scores)} day_entries with score")

    print("Detecting crash_v1 episodes…")
    episodes = find_crash_episodes(day_scores)
    print(f"  {len(episodes)} crash_v1 episodes")

    per_episode = []
    early_spans, late_spans = [], []
    for ep in episodes:
        span = (ep["end"] - ep["start"]).days + 1
        era = "early" if ep["start"] <= ERA_SPLIT else "late"
        per_episode.append({
            "episode_start": ep["start"].isoformat(),
            "episode_end": ep["end"].isoformat(),
            "span_days": span,
            "era": era,
        })
        if era == "early": early_spans.append(span)
        else: late_spans.append(span)

    print(f"\n  early-era episodes: {len(early_spans)}")
    print(f"  late-era episodes:  {len(late_spans)}")

    early_summary = summarise(early_spans)
    late_summary = summarise(late_spans)
    print(f"\n  early span summary: {early_summary}")
    print(f"  late span summary:  {late_summary}")

    if len(early_spans) < MIN_EPISODES_PER_ERA or len(late_spans) < MIN_EPISODES_PER_ERA:
        verdict = "inconclusive"
        delta_median = None
        p_value = None
        crit_a = crit_b = False
    else:
        delta_median = late_summary["median"] - early_summary["median"]
        # one-sided: how often does shuffling produce delta <= observed (i.e., late at least as much shorter)
        rng = random.Random(RANDOM_SEED)
        all_spans = early_spans + late_spans
        n_early = len(early_spans)
        count_le = 0
        for _ in range(PERMUTATIONS):
            shuf = all_spans[:]
            rng.shuffle(shuf)
            d_shuf = statistics.median(shuf[n_early:]) - statistics.median(shuf[:n_early])
            if d_shuf <= delta_median:
                count_le += 1
        p_value = count_le / PERMUTATIONS
        # crit_a: late shorter than early by at least CRIT_A_DELTA_MIN_DAYS → delta_median <= -CRIT_A_DELTA_MIN_DAYS
        crit_a = delta_median <= -CRIT_A_DELTA_MIN_DAYS
        crit_b = p_value <= CRIT_B_P_MAX
        if crit_a and crit_b: verdict = "supported"
        elif crit_a and not crit_b: verdict = "suggestive_underpowered"
        elif not crit_a and delta_median > 0: verdict = "inverse_or_refuted"
        else: verdict = "refuted"

    print(f"\n  delta_median (late - early): {delta_median} (negative = late shorter, supportive)")
    print(f"  permutation p-value (one-sided, late <= early): {p_value}")
    print(f"  crit_a (delta <= -{CRIT_A_DELTA_MIN_DAYS}): {crit_a}")
    print(f"  crit_b (p <= {CRIT_B_P_MAX}): {crit_b}")
    print(f"  VERDICT: {verdict}")

    OUT_DATA.write_text(
        json.dumps({
            "params": {
                "era_split": ERA_SPLIT.isoformat(),
                "crit_a_delta_min_days": CRIT_A_DELTA_MIN_DAYS,
                "crit_b_p_max": CRIT_B_P_MAX,
                "permutations": PERMUTATIONS,
                "random_seed": RANDOM_SEED,
            },
            "counts": {
                "day_entries": len(day_scores),
                "episodes": len(episodes),
                "early_n": len(early_spans),
                "late_n": len(late_spans),
            },
            "early_summary": early_summary,
            "late_summary": late_summary,
            "delta_median": delta_median,
            "permutation_p_value": p_value,
            "criterion_a_pass": crit_a,
            "criterion_b_pass": crit_b,
            "verdict": verdict,
            "per_episode": per_episode,
        }, indent=2, default=str),
        encoding="utf-8",
    )
    print(f"\nwrote {OUT_DATA}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 4))
        max_span = max(max(early_spans, default=0), max(late_spans, default=0))
        bins = list(range(0, max_span + 2))
        ax.hist([early_spans, late_spans], bins=bins,
                label=[f"early 2022-23 (n={len(early_spans)})", f"late 2024+ (n={len(late_spans)})"],
                alpha=0.7)
        ax.set_xlabel("crash span (calendar days)")
        ax.set_ylabel("episodes")
        ax.set_title("K02 — crash span distribution by era")
        ax.legend()
        fig.tight_layout()
        fig.savefig(OUT_PNG)
        plt.close(fig)
    except ImportError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
