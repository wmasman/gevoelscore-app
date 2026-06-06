"""H01 — Resting heart rate drift before crashes.

Implements the protocol pre-registered in hypothesis.md exactly.
Reads gevoelscore day_entries from a local snapshot CSV (produced by
fetch_day_entries.mjs run in the same folder) and RHR from the Garmin
GDPR UDS files. Cross-references the two; computes per-episode
delta_rhr; compares against a random null sample; evaluates the
pre-registered (a)/(b)/(c) criteria on train and validate halves.

Outputs:
  - result-data.json : structured numbers for result.md to consume
  - result-train.png : delta_rhr distribution, train window
  - result-validate.png : delta_rhr distribution, validate window

Run:
  python docs/research/garmin/hypotheses/H01-rhr-drift/test.py

The day_entries snapshot is fetched by a companion mjs script that
uses the project's standard DIRECTUS_TOKEN wrapper, so this Python
script doesn't need direct Directus access.
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
# Locked parameters (mirror hypothesis.md exactly — do not adjust)
# ─────────────────────────────────────────────────────────────────
ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)

LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3

LEADUP_DAYS = 7
BASELINE_WINDOW_DAYS = 90  # ending 7 days before episode

MIN_LEADUP_VALID = 6  # of 7
MIN_BASELINE_VALID = 30  # of 90
TRIMMED_PCT = 0.10  # 10/90 trim for baseline

NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

# Pre-registered thresholds
CRIT_A_FRACTION = 0.60  # ≥60% of episodes show delta_rhr ≥ 3
CRIT_A_DELTA_BPM = 3
CRIT_B_DISCRIMINATION_PP = 15  # crash rate ≥ null rate + 15 pp
CRIT_C_MEDIAN_BPM = 2
CRIT_C_LOWER_QUARTILE_BPM = 0
MIN_EPISODES_PER_WINDOW = 10

# ─────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
DAY_ENTRIES_CSV = HERE / "day_entries.csv"  # produced by fetch_day_entries.mjs
GARMIN_UDS_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Aggregator"
)
OUT_DATA = HERE / "result-data.json"
OUT_TRAIN_PNG = HERE / "result-train.png"
OUT_VALIDATE_PNG = HERE / "result-validate.png"


# ─────────────────────────────────────────────────────────────────
# Step 1 — load gevoelscore day_entries
# ─────────────────────────────────────────────────────────────────
def load_day_entries() -> dict[date, int]:
    if not DAY_ENTRIES_CSV.exists():
        sys.exit(
            f"\nERROR: {DAY_ENTRIES_CSV} not found.\n"
            f"Run the companion fetcher first:\n"
            f"  powershell -ExecutionPolicy Bypass -File scripts/run-directus-script.ps1 "
            f"-Script docs/research/garmin/hypotheses/H01-rhr-drift/fetch_day_entries.mjs\n"
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
# Step 2 — crash_v1 episode detection (mirrors count.mjs exactly)
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
# Step 3 — load Garmin daily RHR from UDS files
# ─────────────────────────────────────────────────────────────────
def load_rhr_by_date() -> dict[date, int]:
    """Returns date -> restingHeartRate. Loads every UDSFile_*.json under
    DI-Connect-Aggregator and indexes by calendarDate.
    """
    out: dict[date, int] = {}
    for p in sorted(GARMIN_UDS_DIR.glob("UDSFile_*.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            rhr = rec.get("restingHeartRate")
            if not cd or rhr in (None, 0):
                continue
            d = date.fromisoformat(cd)
            # If duplicates across files (overlap windows), keep the higher
            # (Garmin sometimes writes a placeholder 0 / partial value)
            if d in out and rhr <= out[d]:
                continue
            out[d] = int(rhr)
    return out


# ─────────────────────────────────────────────────────────────────
# Step 4 — compute delta_rhr for a window
# ─────────────────────────────────────────────────────────────────
def trimmed_mean(values: list[float], trim_pct: float) -> float | None:
    if not values:
        return None
    vs = sorted(values)
    n = len(vs)
    trim = int(n * trim_pct)
    if n - 2 * trim < 1:
        return statistics.mean(vs)
    return statistics.mean(vs[trim : n - trim])


def compute_delta_rhr(
    episode_start: date,
    rhr_by_date: dict[date, int],
) -> dict:
    """Return per-episode dict with delta_rhr and validity flags."""
    leadup = [episode_start - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    baseline_start = episode_start - timedelta(days=BASELINE_WINDOW_DAYS + LEADUP_DAYS)
    baseline_end = episode_start - timedelta(days=LEADUP_DAYS + 1)
    baseline_days = []
    d = baseline_start
    while d <= baseline_end:
        baseline_days.append(d)
        d += timedelta(days=1)

    leadup_vals = [rhr_by_date[d] for d in leadup if d in rhr_by_date]
    baseline_vals = [rhr_by_date[d] for d in baseline_days if d in rhr_by_date]

    leadup_valid = len(leadup_vals) >= MIN_LEADUP_VALID
    baseline_valid = len(baseline_vals) >= MIN_BASELINE_VALID

    out = {
        "leadup_n": len(leadup_vals),
        "baseline_n": len(baseline_vals),
        "leadup_valid": leadup_valid,
        "baseline_valid": baseline_valid,
        "leadup_mean_rhr": statistics.mean(leadup_vals) if leadup_vals else None,
        "baseline_trimmed_mean_rhr": trimmed_mean(baseline_vals, TRIMMED_PCT),
        "delta_rhr": None,
    }
    if leadup_valid and baseline_valid:
        out["delta_rhr"] = out["leadup_mean_rhr"] - out["baseline_trimmed_mean_rhr"]
    return out


# ─────────────────────────────────────────────────────────────────
# Step 5 — build a null sample of non-crash 7-day windows
# ─────────────────────────────────────────────────────────────────
def build_null_sample(
    rhr_by_date: dict[date, int],
    crash_lead_up_days: set[date],
    n: int,
) -> list[float]:
    """Pick N random reference dates whose lead-up window is disjoint from
    any crash lead-up. Returns the list of delta_rhr values for those windows.
    """
    rng = random.Random(RANDOM_SEED)
    all_dates = sorted(
        d for d in rhr_by_date if ANALYSIS_START <= d <= VALIDATE_END
    )
    deltas: list[float] = []
    attempts = 0
    max_attempts = n * 50
    while len(deltas) < n and attempts < max_attempts:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)}
        if leadup & crash_lead_up_days:
            continue
        prof = compute_delta_rhr(ref, rhr_by_date)
        if prof["delta_rhr"] is None:
            continue
        deltas.append(prof["delta_rhr"])
    return deltas


# ─────────────────────────────────────────────────────────────────
# Step 6 — evaluate pre-registered criteria on a window
# ─────────────────────────────────────────────────────────────────
def evaluate(crash_deltas: list[float], null_deltas: list[float], label: str) -> dict:
    if len(crash_deltas) < MIN_EPISODES_PER_WINDOW:
        return {
            "window": label,
            "verdict": "inconclusive",
            "reason": f"only {len(crash_deltas)} usable crash episodes (< {MIN_EPISODES_PER_WINDOW})",
            "crash_n": len(crash_deltas),
            "null_n": len(null_deltas),
        }
    crash_at_thr = sum(1 for v in crash_deltas if v >= CRIT_A_DELTA_BPM) / len(crash_deltas)
    null_at_thr = (
        sum(1 for v in null_deltas if v >= CRIT_A_DELTA_BPM) / len(null_deltas)
        if null_deltas
        else 0.0
    )
    median_delta = statistics.median(crash_deltas)
    lower_q = sorted(crash_deltas)[len(crash_deltas) // 4]
    crit_a = crash_at_thr >= CRIT_A_FRACTION
    crit_b = (crash_at_thr - null_at_thr) * 100 >= CRIT_B_DISCRIMINATION_PP
    crit_c = median_delta >= CRIT_C_MEDIAN_BPM and lower_q >= CRIT_C_LOWER_QUARTILE_BPM
    return {
        "window": label,
        "crash_n": len(crash_deltas),
        "null_n": len(null_deltas),
        "crash_pct_at_threshold": crash_at_thr,
        "null_pct_at_threshold": null_at_thr,
        "discrimination_pp": (crash_at_thr - null_at_thr) * 100,
        "median_delta_rhr": median_delta,
        "lower_quartile_delta_rhr": lower_q,
        "criterion_a_pass": crit_a,
        "criterion_b_pass": crit_b,
        "criterion_c_pass": crit_c,
        "verdict": "supported" if (crit_a and crit_b and crit_c) else "refuted",
    }


# ─────────────────────────────────────────────────────────────────
# Step 7 — plot
# ─────────────────────────────────────────────────────────────────
def maybe_plot(crash_deltas: list[float], null_deltas: list[float], out: Path, title: str):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print(f"  (matplotlib not installed, skipping {out.name})")
        return
    fig, ax = plt.subplots(figsize=(7, 4))
    bins = list(range(-15, 16))
    ax.hist(
        [null_deltas, crash_deltas],
        bins=bins,
        label=[f"null (n={len(null_deltas)})", f"crash lead-ups (n={len(crash_deltas)})"],
        density=True,
        alpha=0.7,
    )
    ax.axvline(CRIT_A_DELTA_BPM, color="black", linestyle="--", alpha=0.5)
    ax.set_xlabel("delta_rhr  (lead-up mean minus baseline trimmed mean, bpm)")
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

    print("Loading Garmin RHR…")
    rhr_by_date = load_rhr_by_date()
    print(f"  {len(rhr_by_date)} days with RHR")

    print("Computing per-episode delta_rhr…")
    per_episode = []
    excluded_missing = 0
    excluded_overlap = 0
    # Build set of all crash lead-up days for overlap detection
    all_leadup_days: set[date] = set()
    for ep in episodes:
        for i in range(1, LEADUP_DAYS + 1):
            all_leadup_days.add(ep["start"] - timedelta(days=i))

    for ep in episodes:
        prof = compute_delta_rhr(ep["start"], rhr_by_date)
        # Overlap check: does this episode's lead-up contain another episode's days?
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
            **prof,
            "delta_rhr": prof["delta_rhr"],
        }
        per_episode.append(rec)
        if not (prof["leadup_valid"] and prof["baseline_valid"]):
            excluded_missing += 1
        elif overlap:
            excluded_overlap += 1
    print(f"  excluded for missing data: {excluded_missing}")
    print(f"  excluded for lead-up overlap: {excluded_overlap}")

    print("Building null sample…")
    null_deltas = build_null_sample(rhr_by_date, all_leadup_days, NULL_SAMPLE_SIZE)
    print(f"  {len(null_deltas)} null windows")

    # Split into train / validate, primary analysis (clean episodes only)
    train_clean = [
        r["delta_rhr"]
        for r in per_episode
        if r["in_train"]
        and r["leadup_valid"]
        and r["baseline_valid"]
        and not r["overlap_with_other_episode"]
    ]
    validate_clean = [
        r["delta_rhr"]
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

    # Persist structured result
    OUT_DATA.write_text(
        json.dumps(
            {
                "params": {
                    "low_threshold": LOW_THRESHOLD,
                    "min_run_days": MIN_RUN_DAYS,
                    "merge_within_days": MERGE_WITHIN_DAYS,
                    "leadup_days": LEADUP_DAYS,
                    "baseline_window_days": BASELINE_WINDOW_DAYS,
                    "min_leadup_valid": MIN_LEADUP_VALID,
                    "min_baseline_valid": MIN_BASELINE_VALID,
                    "trimmed_pct": TRIMMED_PCT,
                    "null_sample_size": NULL_SAMPLE_SIZE,
                    "crit_a_fraction": CRIT_A_FRACTION,
                    "crit_a_delta_bpm": CRIT_A_DELTA_BPM,
                    "crit_b_discrimination_pp": CRIT_B_DISCRIMINATION_PP,
                    "crit_c_median_bpm": CRIT_C_MEDIAN_BPM,
                    "crit_c_lower_quartile_bpm": CRIT_C_LOWER_QUARTILE_BPM,
                    "analysis_start": ANALYSIS_START.isoformat(),
                    "train_end": TRAIN_END.isoformat(),
                    "validate_end": VALIDATE_END.isoformat(),
                },
                "counts": {
                    "day_entries": len(day_scores),
                    "rhr_days": len(rhr_by_date),
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
                "per_episode": per_episode,
                "null_deltas_summary": {
                    "n": len(null_deltas),
                    "median": statistics.median(null_deltas) if null_deltas else None,
                    "mean": statistics.mean(null_deltas) if null_deltas else None,
                    "p10": sorted(null_deltas)[int(len(null_deltas) * 0.10)] if null_deltas else None,
                    "p90": sorted(null_deltas)[int(len(null_deltas) * 0.90)] if null_deltas else None,
                },
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    print(f"\nwrote {OUT_DATA}")

    maybe_plot(train_clean, null_deltas, OUT_TRAIN_PNG, "H01 — delta RHR before crashes, TRAIN")
    maybe_plot(validate_clean, null_deltas, OUT_VALIDATE_PNG, "H01 — delta RHR before crashes, VALIDATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
