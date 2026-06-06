"""H04 — Body battery net-drain elevated before crashes.

Mirrors the protocol in hypothesis.md exactly. Structure follows
H02/H03; the metric is body-battery net delta from the UDS daily
aggregates.
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

LEADUP_DAYS = 3
BASELINE_WINDOW_DAYS = 90

MIN_LEADUP_VALID = 3  # of 3
MIN_BASELINE_VALID = 30
TRIMMED_PCT = 0.10

NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

CRIT_A_FRACTION = 0.60
CRIT_A_DELTA_BB = -5  # body battery points
CRIT_B_DISCRIMINATION_PP = 15
CRIT_C_MEDIAN_BB = -3
CRIT_C_UPPER_QUARTILE_BB = 0
MIN_EPISODES_PER_WINDOW = 10

HERE = Path(__file__).resolve().parent
DAY_ENTRIES_CSV = HERE / "day_entries.csv"
GARMIN_UDS_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Aggregator"
)
OUT_DATA = HERE / "result-data.json"
OUT_TRAIN_PNG = HERE / "result-train.png"
OUT_VALIDATE_PNG = HERE / "result-validate.png"


# ─────────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────────
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


# ─────────────────────────────────────────────────────────────────
# Body battery loading
# ─────────────────────────────────────────────────────────────────
def load_body_battery_by_date() -> dict[date, dict]:
    """date -> { net_delta, charged, drained }"""
    out: dict[date, dict] = {}
    excluded_zero = 0
    for p in sorted(GARMIN_UDS_DIR.glob("UDSFile_*.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            bb = rec.get("bodyBattery") or {}
            charged = bb.get("chargedValue")
            drained = bb.get("drainedValue")
            if not cd or charged is None or drained is None:
                continue
            if charged == 0 and drained == 0:
                excluded_zero += 1
                continue
            d = date.fromisoformat(cd)
            net = int(charged) - int(drained)
            if d in out and (out[d]["charged"] + out[d]["drained"]) >= (charged + drained):
                continue
            out[d] = {
                "net_delta": net,
                "charged": int(charged),
                "drained": int(drained),
            }
    print(f"  excluded all-zero (off-wrist) days: {excluded_zero}")
    return out


# ─────────────────────────────────────────────────────────────────
# Window math (matches H02/H03 shape)
# ─────────────────────────────────────────────────────────────────
def compute_window(ref: date, bb_by_date: dict[date, dict]) -> dict:
    leadup = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    baseline_start = ref - timedelta(days=BASELINE_WINDOW_DAYS + LEADUP_DAYS)
    baseline_end = ref - timedelta(days=LEADUP_DAYS + 1)
    baseline_days = []
    d = baseline_start
    while d <= baseline_end:
        baseline_days.append(d)
        d += timedelta(days=1)

    leadup_vals = [bb_by_date[d]["net_delta"] for d in leadup if d in bb_by_date]
    baseline_vals = [bb_by_date[d]["net_delta"] for d in baseline_days if d in bb_by_date]
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


def build_null_sample(bb_by_date, crash_lead_up_days, n):
    rng = random.Random(RANDOM_SEED)
    all_dates = sorted(d for d in bb_by_date if ANALYSIS_START <= d <= VALIDATE_END)
    deltas: list[float] = []
    attempts = 0
    max_attempts = n * 50
    while len(deltas) < n and attempts < max_attempts:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)}
        if leadup & crash_lead_up_days:
            continue
        prof = compute_window(ref, bb_by_date)
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
    # Direction: "at most -5" since drainage is bad
    crash_at_thr = sum(1 for v in crash_deltas if v <= CRIT_A_DELTA_BB) / len(crash_deltas)
    null_at_thr = (
        sum(1 for v in null_deltas if v <= CRIT_A_DELTA_BB) / len(null_deltas)
        if null_deltas
        else 0.0
    )
    median_delta = statistics.median(crash_deltas)
    upper_q = sorted(crash_deltas)[(3 * len(crash_deltas)) // 4]
    crit_a = crash_at_thr >= CRIT_A_FRACTION
    crit_b = (crash_at_thr - null_at_thr) * 100 >= CRIT_B_DISCRIMINATION_PP
    crit_c = median_delta <= CRIT_C_MEDIAN_BB and upper_q <= CRIT_C_UPPER_QUARTILE_BB
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
    bins = list(range(-40, 41, 2))
    ax.hist(
        [null_deltas, crash_deltas],
        bins=bins,
        label=[f"null (n={len(null_deltas)})", f"crash lead-ups (n={len(crash_deltas)})"],
        density=True,
        alpha=0.7,
    )
    ax.axvline(CRIT_A_DELTA_BB, color="black", linestyle="--", alpha=0.5)
    ax.set_xlabel("delta_bb_net  (lead-up mean minus baseline trimmed mean, body battery points)")
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

    print("Loading body battery daily aggregates…")
    bb_by_date = load_body_battery_by_date()
    print(f"  {len(bb_by_date)} days with body battery data")

    all_leadup_days: set[date] = set()
    for ep in episodes:
        for i in range(1, LEADUP_DAYS + 1):
            all_leadup_days.add(ep["start"] - timedelta(days=i))

    print("Computing per-episode delta_bb_net…")
    per_episode = []
    excluded_missing = 0
    excluded_overlap = 0
    for ep in episodes:
        prof = compute_window(ep["start"], bb_by_date)
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
            "in_train": ep["start"] <= TRAIN_END,
            "in_validate": TRAIN_END < ep["start"] <= VALIDATE_END,
            "overlap_with_other_episode": overlap,
            "leadup_valid": prof["leadup_valid"],
            "baseline_valid": prof["baseline_valid"],
            "leadup_mean_net": prof["leadup_mean"],
            "baseline_mean_net": prof["baseline_trimmed_mean"],
            "delta_bb_net": prof["delta"],
        }
        per_episode.append(rec)
        if not (prof["leadup_valid"] and prof["baseline_valid"]):
            excluded_missing += 1
        elif overlap:
            excluded_overlap += 1

    print(f"  excluded for missing data: {excluded_missing}")
    print(f"  excluded for lead-up overlap: {excluded_overlap}")

    print("Building null sample…")
    null_deltas = build_null_sample(bb_by_date, all_leadup_days, NULL_SAMPLE_SIZE)
    print(f"  {len(null_deltas)} null windows")

    train_clean = [
        r["delta_bb_net"]
        for r in per_episode
        if r["in_train"]
        and r["leadup_valid"]
        and r["baseline_valid"]
        and not r["overlap_with_other_episode"]
    ]
    validate_clean = [
        r["delta_bb_net"]
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
                    "leadup_days": LEADUP_DAYS,
                    "baseline_window_days": BASELINE_WINDOW_DAYS,
                    "trimmed_pct": TRIMMED_PCT,
                    "null_sample_size": NULL_SAMPLE_SIZE,
                    "crit_a_fraction": CRIT_A_FRACTION,
                    "crit_a_delta_bb": CRIT_A_DELTA_BB,
                    "crit_b_discrimination_pp": CRIT_B_DISCRIMINATION_PP,
                    "crit_c_median_bb": CRIT_C_MEDIAN_BB,
                    "crit_c_upper_quartile_bb": CRIT_C_UPPER_QUARTILE_BB,
                    "analysis_start": ANALYSIS_START.isoformat(),
                    "train_end": TRAIN_END.isoformat(),
                    "validate_end": VALIDATE_END.isoformat(),
                },
                "counts": {
                    "day_entries": len(day_scores),
                    "bb_days": len(bb_by_date),
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

    maybe_plot(train_clean, null_deltas, OUT_TRAIN_PNG, "H04 — delta body-battery net before crashes, TRAIN")
    maybe_plot(validate_clean, null_deltas, OUT_VALIDATE_PNG, "H04 — delta body-battery net before crashes, VALIDATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
