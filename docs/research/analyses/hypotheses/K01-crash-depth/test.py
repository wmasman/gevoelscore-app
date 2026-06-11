"""K01 — Crash depth shifted across recovery eras.

Mirrors the protocol in hypothesis.md exactly. gevoelscore-only,
no Garmin data needed.
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
ERA_SPLIT = date(2023, 12, 31)  # ≤ this = early; > this = late
VALIDATE_END = date(2026, 6, 5)

LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3

PERMUTATIONS = 10_000
RANDOM_SEED = 20260605

CRIT_A_DELTA_MIN_POINTS = 0.3
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


def episode_nadir(ep: dict, day_scores: dict[date, int]) -> int | None:
    d = ep["start"]
    scores = []
    while d <= ep["end"]:
        if d in day_scores:
            scores.append(day_scores[d])
        d += timedelta(days=1)
    return min(scores) if scores else None


def summarise(values: list[int]) -> dict:
    if not values: return {"n": 0}
    s = sorted(values)
    n = len(s)
    return {
        "n": n,
        "min": s[0],
        "max": s[-1],
        "median": statistics.median(s),
        "mean": round(statistics.mean(s), 2),
        "p25": s[n // 4],
        "p75": s[(3 * n) // 4],
    }


def main() -> int:
    print("Loading day_entries…")
    day_scores = load_day_entries()
    print(f"  {len(day_scores)} day_entries with score")

    print("Detecting crash_v1 episodes…")
    episodes = find_crash_episodes(day_scores)
    print(f"  {len(episodes)} crash_v1 episodes")

    per_episode = []
    early_nadirs, late_nadirs = [], []
    for ep in episodes:
        n = episode_nadir(ep, day_scores)
        era = "early" if ep["start"] <= ERA_SPLIT else "late"
        per_episode.append({
            "episode_start": ep["start"].isoformat(),
            "episode_end": ep["end"].isoformat(),
            "span_days": (ep["end"] - ep["start"]).days + 1,
            "era": era,
            "nadir": n,
        })
        if n is None: continue
        if era == "early": early_nadirs.append(n)
        else: late_nadirs.append(n)

    print(f"\n  early-era episodes: {len(early_nadirs)}")
    print(f"  late-era episodes:  {len(late_nadirs)}")

    early_summary = summarise(early_nadirs)
    late_summary = summarise(late_nadirs)
    print(f"\n  early nadir summary: {early_summary}")
    print(f"  late nadir summary:  {late_summary}")

    # Verdict scaffolding
    if len(early_nadirs) < MIN_EPISODES_PER_ERA or len(late_nadirs) < MIN_EPISODES_PER_ERA:
        verdict = "inconclusive"
        delta_median = None
        p_value = None
        crit_a = crit_b = False
    else:
        delta_median = late_summary["median"] - early_summary["median"]
        # Permutation test (one-sided: how often does shuffling produce delta >= observed)
        rng = random.Random(RANDOM_SEED)
        all_nadirs = early_nadirs + late_nadirs
        n_early = len(early_nadirs)
        count_ge = 0
        for _ in range(PERMUTATIONS):
            shuf = all_nadirs[:]
            rng.shuffle(shuf)
            d_shuf = statistics.median(shuf[n_early:]) - statistics.median(shuf[:n_early])
            if d_shuf >= delta_median:
                count_ge += 1
        p_value = count_ge / PERMUTATIONS
        crit_a = delta_median >= CRIT_A_DELTA_MIN_POINTS
        crit_b = p_value <= CRIT_B_P_MAX
        if crit_a and crit_b: verdict = "supported"
        elif crit_a and not crit_b: verdict = "suggestive_underpowered"
        elif not crit_a and delta_median < 0: verdict = "inverse_or_refuted"
        else: verdict = "refuted"

    print(f"\n  delta_median (late - early): {delta_median}")
    print(f"  permutation p-value (one-sided): {p_value}")
    print(f"  crit_a (delta >= {CRIT_A_DELTA_MIN_POINTS}): {crit_a}")
    print(f"  crit_b (p <= {CRIT_B_P_MAX}): {crit_b}")
    print(f"  VERDICT: {verdict}")

    OUT_DATA.write_text(
        json.dumps({
            "params": {
                "low_threshold": LOW_THRESHOLD,
                "min_run_days": MIN_RUN_DAYS,
                "merge_within_days": MERGE_WITHIN_DAYS,
                "era_split": ERA_SPLIT.isoformat(),
                "crit_a_delta_min_points": CRIT_A_DELTA_MIN_POINTS,
                "crit_b_p_max": CRIT_B_P_MAX,
                "permutations": PERMUTATIONS,
                "random_seed": RANDOM_SEED,
            },
            "counts": {
                "day_entries": len(day_scores),
                "episodes": len(episodes),
                "early_n": len(early_nadirs),
                "late_n": len(late_nadirs),
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
        fig, ax = plt.subplots(figsize=(7, 4))
        bins = [0.5, 1.5, 2.5, 3.5]
        ax.hist([early_nadirs, late_nadirs], bins=bins,
                label=[f"early 2022-23 (n={len(early_nadirs)})", f"late 2024+ (n={len(late_nadirs)})"],
                alpha=0.7)
        ax.set_xticks([1, 2, 3])
        ax.set_xlabel("crash nadir (minimum score during episode)")
        ax.set_ylabel("episodes")
        ax.set_title("K01 — crash depth distribution by era")
        ax.legend()
        fig.tight_layout()
        fig.savefig(OUT_PNG)
        plt.close(fig)
    except ImportError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
