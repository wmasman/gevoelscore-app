"""H03 — Sleep efficiency drop before crashes.

Mirrors the protocol in hypothesis.md exactly. Structure follows
H01/H02; the metric and data loading are sleep-specific.
"""
from __future__ import annotations

import csv
import json
import random
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

# ─────────────────────────────────────────────────────────────────
# Locked parameters
# ─────────────────────────────────────────────────────────────────
ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)

LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3

LEADUP_NIGHTS = 7
BASELINE_WINDOW_DAYS = 90

MIN_LEADUP_VALID = 5  # of 7 (slightly more permissive than H02)
MIN_BASELINE_VALID = 30
TRIMMED_PCT = 0.10

MIN_TIB_SECONDS = 4 * 3600  # exclude < 4h nights
# Per hypothesis.md §6: blacklist of confirmation types that indicate
# unreliable measurement, not a whitelist. Anything not in this set is
# considered a confirmed night.
INVALID_CONFIRMATION_TYPES = {
    "UNCONFIRMED",
    "OFF_WRIST",
    "NOT_CONFIRMED",
}

NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

CRIT_A_FRACTION = 0.60
CRIT_A_DELTA_EFF = -0.05
CRIT_B_DISCRIMINATION_PP = 15
CRIT_C_MEDIAN_EFF = -0.03
CRIT_C_UPPER_QUARTILE_EFF = 0.0
MIN_EPISODES_PER_WINDOW = 10

# ─────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
DAY_ENTRIES_CSV = HERE / "day_entries.csv"
SLEEP_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Wellness"
)
OUT_DATA = HERE / "result-data.json"
OUT_TRAIN_PNG = HERE / "result-train.png"
OUT_VALIDATE_PNG = HERE / "result-validate.png"


# ─────────────────────────────────────────────────────────────────
# Helpers shared with H01/H02 (intentionally duplicated for clarity)
# ─────────────────────────────────────────────────────────────────
def load_day_entries() -> dict[date, int]:
    if not DAY_ENTRIES_CSV.exists():
        sys.exit(f"\nERROR: {DAY_ENTRIES_CSV} not found. Run fetch_day_entries.mjs first.\n")
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


# ─────────────────────────────────────────────────────────────────
# Sleep data loading
# ─────────────────────────────────────────────────────────────────
def load_sleep_efficiency_by_date() -> dict[date, dict]:
    """date -> { efficiency, tst_s, awake_s, unmeas_s, confirmation }"""
    out: dict[date, dict] = {}
    excluded_unconfirmed = 0
    excluded_short = 0
    for p in sorted(SLEEP_DIR.glob("*_sleepData.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            if not cd:
                continue
            conf = rec.get("sleepWindowConfirmationType")
            deep = int(rec.get("deepSleepSeconds") or 0)
            light = int(rec.get("lightSleepSeconds") or 0)
            rem = int(rec.get("remSleepSeconds") or 0)
            awake = int(rec.get("awakeSleepSeconds") or 0)
            unmeas = int(rec.get("unmeasurableSeconds") or 0)
            tst = deep + light + rem
            tib_like = tst + awake + unmeas
            if conf in INVALID_CONFIRMATION_TYPES:
                excluded_unconfirmed += 1
                continue
            if tib_like < MIN_TIB_SECONDS:
                excluded_short += 1
                continue
            d = date.fromisoformat(cd)
            efficiency = tst / tib_like if tib_like > 0 else None
            if efficiency is None:
                continue
            # de-dup across overlapping files
            if d in out and tib_like <= out[d]["_tib_like"]:
                continue
            out[d] = {
                "efficiency": efficiency,
                "tst_s": tst,
                "awake_s": awake,
                "unmeas_s": unmeas,
                "deep_s": deep,
                "light_s": light,
                "rem_s": rem,
                "confirmation": conf,
                "_tib_like": tib_like,
            }
    print(f"  excluded unconfirmed: {excluded_unconfirmed}")
    print(f"  excluded too-short (<4h TIB): {excluded_short}")
    return out


# ─────────────────────────────────────────────────────────────────
# Window math
# ─────────────────────────────────────────────────────────────────
def compute_window(
    ref: date,
    sleep_by_date: dict[date, dict],
) -> dict:
    leadup = [ref - timedelta(days=i) for i in range(1, LEADUP_NIGHTS + 1)]
    baseline_start = ref - timedelta(days=BASELINE_WINDOW_DAYS + LEADUP_NIGHTS)
    baseline_end = ref - timedelta(days=LEADUP_NIGHTS + 1)
    baseline_days = []
    d = baseline_start
    while d <= baseline_end:
        baseline_days.append(d)
        d += timedelta(days=1)

    leadup_vals = [sleep_by_date[d]["efficiency"] for d in leadup if d in sleep_by_date]
    baseline_vals = [sleep_by_date[d]["efficiency"] for d in baseline_days if d in sleep_by_date]
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
    }
    if leadup_valid and baseline_valid:
        out["delta"] = out["leadup_mean"] - out["baseline_trimmed_mean"]
    return out


def build_null_sample(sleep_by_date, crash_lead_up_days, n):
    rng = random.Random(RANDOM_SEED)
    all_dates = sorted(
        d for d in sleep_by_date if ANALYSIS_START <= d <= VALIDATE_END
    )
    deltas: list[float] = []
    attempts = 0
    max_attempts = n * 50
    while len(deltas) < n and attempts < max_attempts:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_NIGHTS + 1)}
        if leadup & crash_lead_up_days:
            continue
        prof = compute_window(ref, sleep_by_date)
        if prof["delta"] is None:
            continue
        deltas.append(prof["delta"])
    return deltas


def evaluate(crash_deltas, null_deltas, label):
    if len(crash_deltas) < MIN_EPISODES_PER_WINDOW:
        return {
            "window": label,
            "verdict": "inconclusive",
            "reason": f"only {len(crash_deltas)} usable crash episodes (< {MIN_EPISODES_PER_WINDOW})",
            "crash_n": len(crash_deltas),
            "null_n": len(null_deltas),
        }
    # Note: criterion direction is "at most", since efficiency dropping is bad
    crash_at_thr = sum(1 for v in crash_deltas if v <= CRIT_A_DELTA_EFF) / len(crash_deltas)
    null_at_thr = (
        sum(1 for v in null_deltas if v <= CRIT_A_DELTA_EFF) / len(null_deltas)
        if null_deltas
        else 0.0
    )
    median_delta = statistics.median(crash_deltas)
    upper_q = sorted(crash_deltas)[(3 * len(crash_deltas)) // 4]
    crit_a = crash_at_thr >= CRIT_A_FRACTION
    crit_b = (crash_at_thr - null_at_thr) * 100 >= CRIT_B_DISCRIMINATION_PP
    crit_c = median_delta <= CRIT_C_MEDIAN_EFF and upper_q <= CRIT_C_UPPER_QUARTILE_EFF
    return {
        "window": label,
        "crash_n": len(crash_deltas),
        "null_n": len(null_deltas),
        "crash_pct_at_threshold": crash_at_thr,
        "null_pct_at_threshold": null_at_thr,
        "discrimination_pp": (crash_at_thr - null_at_thr) * 100,
        "median_delta": median_delta,
        "upper_quartile_delta": upper_q,
        "criterion_a_pass": crit_a,
        "criterion_b_pass": crit_b,
        "criterion_c_pass": crit_c,
        "verdict": "supported" if (crit_a and crit_b and crit_c) else "refuted",
    }


def maybe_plot(crash_deltas, null_deltas, out, title):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(7, 4))
    bins = [-0.20 + i * 0.01 for i in range(41)]
    ax.hist(
        [null_deltas, crash_deltas],
        bins=bins,
        label=[f"null (n={len(null_deltas)})", f"crash lead-ups (n={len(crash_deltas)})"],
        density=True,
        alpha=0.7,
    )
    ax.axvline(CRIT_A_DELTA_EFF, color="black", linestyle="--", alpha=0.5)
    ax.set_xlabel("delta_efficiency  (lead-up mean minus baseline trimmed mean)")
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

    print("Loading sleep data…")
    sleep_by_date = load_sleep_efficiency_by_date()
    print(f"  {len(sleep_by_date)} usable sleep nights")

    all_leadup_days: set[date] = set()
    for ep in episodes:
        for i in range(1, LEADUP_NIGHTS + 1):
            all_leadup_days.add(ep["start"] - timedelta(days=i))

    print("Computing per-episode delta_efficiency…")
    per_episode = []
    excluded_missing = 0
    excluded_overlap = 0
    for ep in episodes:
        prof = compute_window(ep["start"], sleep_by_date)
        leadup = {ep["start"] - timedelta(days=i) for i in range(1, LEADUP_NIGHTS + 1)}
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
            "leadup_valid": prof["leadup_valid"],
            "baseline_valid": prof["baseline_valid"],
            "leadup_n": prof["leadup_n"],
            "baseline_n": prof["baseline_n"],
            "leadup_mean_eff": prof["leadup_mean"],
            "baseline_mean_eff": prof["baseline_trimmed_mean"],
            "delta_eff": prof["delta"],
        }
        per_episode.append(rec)
        if not (prof["leadup_valid"] and prof["baseline_valid"]):
            excluded_missing += 1
        elif overlap:
            excluded_overlap += 1

    print(f"  excluded for missing data: {excluded_missing}")
    print(f"  excluded for lead-up overlap: {excluded_overlap}")

    print("Building null sample…")
    null_deltas = build_null_sample(sleep_by_date, all_leadup_days, NULL_SAMPLE_SIZE)
    print(f"  {len(null_deltas)} null windows")

    train_clean = [
        r["delta_eff"]
        for r in per_episode
        if r["in_train"]
        and r["leadup_valid"]
        and r["baseline_valid"]
        and not r["overlap_with_other_episode"]
    ]
    validate_clean = [
        r["delta_eff"]
        for r in per_episode
        if r["in_validate"]
        and r["leadup_valid"]
        and r["baseline_valid"]
        and not r["overlap_with_other_episode"]
    ]
    print(f"  train clean episodes: {len(train_clean)}")
    print(f"  validate clean episodes: {len(validate_clean)}")

    train_eval = evaluate(train_clean, null_deltas, "train")
    validate_eval = evaluate(validate_clean, null_deltas, "validate")

    overall_verdict = (
        "supported"
        if train_eval["verdict"] == "supported" and validate_eval["verdict"] == "supported"
        else "inconclusive"
        if "inconclusive" in (train_eval["verdict"], validate_eval["verdict"])
        else "refuted"
    )

    print("\n=== VERDICT ===")
    print(f"  train:    {train_eval}")
    print(f"  validate: {validate_eval}")
    print(f"  overall:  {overall_verdict}")

    OUT_DATA.write_text(
        json.dumps(
            {
                "params": {
                    "leadup_nights": LEADUP_NIGHTS,
                    "baseline_window_days": BASELINE_WINDOW_DAYS,
                    "min_leadup_valid": MIN_LEADUP_VALID,
                    "min_baseline_valid": MIN_BASELINE_VALID,
                    "trimmed_pct": TRIMMED_PCT,
                    "null_sample_size": NULL_SAMPLE_SIZE,
                    "crit_a_fraction": CRIT_A_FRACTION,
                    "crit_a_delta_eff": CRIT_A_DELTA_EFF,
                    "crit_b_discrimination_pp": CRIT_B_DISCRIMINATION_PP,
                    "crit_c_median_eff": CRIT_C_MEDIAN_EFF,
                    "crit_c_upper_quartile_eff": CRIT_C_UPPER_QUARTILE_EFF,
                    "analysis_start": ANALYSIS_START.isoformat(),
                    "train_end": TRAIN_END.isoformat(),
                    "validate_end": VALIDATE_END.isoformat(),
                },
                "counts": {
                    "day_entries": len(day_scores),
                    "sleep_nights": len(sleep_by_date),
                    "episodes": len(episodes),
                    "excluded_missing": excluded_missing,
                    "excluded_overlap": excluded_overlap,
                    "train_clean": len(train_clean),
                    "validate_clean": len(validate_clean),
                    "null_n": len(null_deltas),
                },
                "train": train_eval,
                "validate": validate_eval,
                "overall_verdict": overall_verdict,
                "null_summary": {
                    "n": len(null_deltas),
                    "median": statistics.median(null_deltas) if null_deltas else None,
                    "mean": statistics.mean(null_deltas) if null_deltas else None,
                },
                "per_episode": per_episode,
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    print(f"\nwrote {OUT_DATA}")

    maybe_plot(train_clean, null_deltas, OUT_TRAIN_PNG, "H03 — delta sleep efficiency before crashes, TRAIN")
    maybe_plot(validate_clean, null_deltas, OUT_VALIDATE_PNG, "H03 — delta sleep efficiency before crashes, VALIDATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
