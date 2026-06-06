"""H02b — Trajectory extension.

The original H02b verdict was binary: train SUPPORTED, validate REFUTED.
The S01 stabilisation trajectories show the underlying change is
gradual, not a cliff. So: compute the H02b discrimination metric on
rolling 12-month windows (anchored monthly) to show *how the
precursor signal fades over time* rather than as a yes/no.

For each anchor month from 2023-08 (the first month with a full prior
12 months of analysis window) through 2026-06:
  - Crash episodes whose start date falls in [anchor - 12mo, anchor]
  - For each: compute delta_spike per the same H02b protocol
  - Null sample of 100 random 3-day windows from the same 12-month
    range (disjoint from any crash lead-up)
  - Discrimination metric: (% crash ≥+10min) − (% null ≥+10min)

Output:
  - trajectory.csv with per-anchor stats
  - trajectory.png showing the curve over time
"""
from __future__ import annotations

import csv
import json
import random
import statistics
from datetime import date, timedelta
from pathlib import Path

ANALYSIS_START = date(2022, 9, 3)
WINDOW_END = date(2026, 6, 5)

LOW_THRESHOLD = 3
MIN_RUN_DAYS = 2
MERGE_WITHIN_DAYS = 3
LEADUP_DAYS = 3
BASELINE_WINDOW_DAYS = 90
TRIMMED_PCT = 0.10
MIN_LEADUP_VALID = 2
MIN_BASELINE_VALID = 30

ROLLING_WINDOW_MONTHS = 12
ANCHOR_STEP_MONTHS = 1

CRIT_A_DELTA_MIN = 10
NULL_SAMPLES_PER_ANCHOR = 100
RANDOM_SEED = 20260605

HERE = Path(__file__).resolve().parent
DAY_ENTRIES_CSV = HERE / "day_entries.csv"
SPIKE_CSV = HERE / "daily_max_spike.csv"
OUT_CSV = HERE / "trajectory.csv"
OUT_PNG = HERE / "trajectory.png"


# Lightweight reuse of H02b's logic (copied to keep this script standalone)
def load_day_entries() -> dict[date, int]:
    out: dict[date, int] = {}
    with DAY_ENTRIES_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            s = r["score"]
            if s in ("", "None", None):
                continue
            out[d] = int(s)
    return out


def load_spike_by_date() -> dict[date, float]:
    out = {}
    with SPIKE_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1":
                continue
            out[date.fromisoformat(r["date"])] = float(r["max_spike_minutes"])
    return out


def find_crash_episodes(day_scores: dict[date, int]) -> list[dict]:
    sorted_dates = sorted(d for d in day_scores if ANALYSIS_START <= d <= WINDOW_END)
    runs, cur = [], None
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
    merged = []
    for r in runs:
        if merged and (r["start"] - merged[-1]["end"]).days <= MERGE_WITHIN_DAYS:
            merged[-1]["end"] = r["end"]
            merged[-1]["days"] += r["days"]
        else:
            merged.append({"start": r["start"], "end": r["end"], "days": r["days"]})
    return merged


def trimmed_mean(values, pct):
    if not values:
        return None
    s = sorted(values); n = len(s); trim = int(n * pct)
    if n - 2 * trim < 1:
        return statistics.mean(s)
    return statistics.mean(s[trim : n - trim])


def compute_delta(ref: date, spike_by_date: dict[date, float]) -> float | None:
    leadup = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    baseline_start = ref - timedelta(days=BASELINE_WINDOW_DAYS + LEADUP_DAYS)
    baseline_end = ref - timedelta(days=LEADUP_DAYS + 1)
    baseline_days = []
    d = baseline_start
    while d <= baseline_end:
        baseline_days.append(d); d += timedelta(days=1)
    leadup_vals = [spike_by_date[d] for d in leadup if d in spike_by_date]
    baseline_vals = [spike_by_date[d] for d in baseline_days if d in spike_by_date]
    if len(leadup_vals) < MIN_LEADUP_VALID or len(baseline_vals) < MIN_BASELINE_VALID:
        return None
    return max(leadup_vals) - trimmed_mean(baseline_vals, TRIMMED_PCT)


def main() -> int:
    print("Loading data…")
    day_scores = load_day_entries()
    spike_by_date = load_spike_by_date()
    episodes = find_crash_episodes(day_scores)
    print(f"  episodes={len(episodes)}  spike_days={len(spike_by_date)}")

    # Build anchor dates: first day of each month from 2023-08 through 2026-06
    anchors = []
    y, m = 2023, 8
    while date(y, m, 1) <= WINDOW_END:
        anchors.append(date(y, m, 1))
        m += ANCHOR_STEP_MONTHS
        if m > 12:
            m -= 12; y += 1
    print(f"  anchors: {len(anchors)} (monthly, rolling 12-month window)")

    # Crash lead-up days across the full window (for null exclusion)
    all_leadup_days: set[date] = set()
    for ep in episodes:
        for i in range(1, LEADUP_DAYS + 1):
            all_leadup_days.add(ep["start"] - timedelta(days=i))

    rng = random.Random(RANDOM_SEED)
    rows = []

    for a in anchors:
        ws = a - timedelta(days=ROLLING_WINDOW_MONTHS * 30)
        # Episodes whose start is inside the rolling window
        eps_in_window = [ep for ep in episodes if ws <= ep["start"] <= a]
        crash_deltas = []
        for ep in eps_in_window:
            d = compute_delta(ep["start"], spike_by_date)
            if d is not None:
                crash_deltas.append(d)

        # Null sample from the same window
        candidate_dates = sorted(
            d for d in spike_by_date if ws <= d <= a
        )
        null_deltas = []
        attempts = 0
        max_attempts = NULL_SAMPLES_PER_ANCHOR * 50
        while len(null_deltas) < NULL_SAMPLES_PER_ANCHOR and attempts < max_attempts:
            attempts += 1
            if not candidate_dates: break
            ref = rng.choice(candidate_dates)
            leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)}
            if leadup & all_leadup_days:
                continue
            d = compute_delta(ref, spike_by_date)
            if d is not None:
                null_deltas.append(d)

        crash_n = len(crash_deltas)
        null_n = len(null_deltas)
        if crash_n == 0 or null_n == 0:
            rows.append({
                "anchor": a.isoformat(),
                "window_start": ws.isoformat(),
                "crash_n": crash_n,
                "null_n": null_n,
                "pct_crash_at_thr": "",
                "pct_null_at_thr": "",
                "discrimination_pp": "",
                "median_delta_crash": "",
                "median_delta_null": "",
            })
            continue
        crash_at = sum(1 for v in crash_deltas if v >= CRIT_A_DELTA_MIN) / crash_n
        null_at = sum(1 for v in null_deltas if v >= CRIT_A_DELTA_MIN) / null_n
        rows.append({
            "anchor": a.isoformat(),
            "window_start": ws.isoformat(),
            "crash_n": crash_n,
            "null_n": null_n,
            "pct_crash_at_thr": round(crash_at * 100, 1),
            "pct_null_at_thr": round(null_at * 100, 1),
            "discrimination_pp": round((crash_at - null_at) * 100, 1),
            "median_delta_crash": round(statistics.median(crash_deltas), 2),
            "median_delta_null": round(statistics.median(null_deltas), 2),
        })

    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT_CSV}")

    # Show key rows
    print("\nselected rows:")
    for r in rows[::4]:
        print(f"  {r['anchor']}  crash_n={r['crash_n']:>2}  pct_crash={r['pct_crash_at_thr']}%  pct_null={r['pct_null_at_thr']}%  discrim={r['discrimination_pp']}pp")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        xs = [date.fromisoformat(r["anchor"]) for r in rows if r["discrimination_pp"] != ""]
        disc = [r["discrimination_pp"] for r in rows if r["discrimination_pp"] != ""]
        crash_n = [r["crash_n"] for r in rows if r["discrimination_pp"] != ""]
        crash_pct = [r["pct_crash_at_thr"] for r in rows if r["discrimination_pp"] != ""]
        null_pct = [r["pct_null_at_thr"] for r in rows if r["discrimination_pp"] != ""]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

        ax1.plot(xs, crash_pct, label="% crash lead-ups with +10 min spike", color="#c0392b", linewidth=2)
        ax1.plot(xs, null_pct, label="% null windows with +10 min spike", color="#7f8c8d", linewidth=1.5, linestyle="--")
        ax1.axhline(60, color="black", linestyle=":", alpha=0.5)  # crit a bar
        ax1.set_ylabel("% windows with delta_spike ≥ +10 min")
        ax1.set_title("H02b — spike-precursor discrimination over time\n(rolling 12-month windows, anchored monthly)")
        ax1.legend(loc="upper right")
        ax1.grid(alpha=0.25)

        colors = ["#16a085" if d >= 15 else "#d68910" if d >= 0 else "#c0392b" for d in disc]
        ax2.bar(xs, disc, width=22, color=colors, alpha=0.8)
        ax2.axhline(15, color="black", linestyle=":", alpha=0.5, label="crit b threshold (+15 pp)")
        ax2.axhline(0, color="gray", linewidth=0.8)
        ax2.set_ylabel("discrimination (crash − null, pp)")
        ax2.set_xlabel("rolling-window anchor (right edge)")
        ax2.legend(loc="upper right")
        ax2.grid(alpha=0.25)
        ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")

        # Annotate crash_n on each bar
        for x, y, n in zip(xs, disc, crash_n):
            ax2.annotate(f"n={n}", xy=(x, y), xytext=(0, 3 if y >= 0 else -10),
                         textcoords="offset points", ha="center", fontsize=7, color="#555")

        fig.tight_layout()
        fig.savefig(OUT_PNG, dpi=110)
        plt.close(fig)
        print(f"wrote {OUT_PNG}")
    except ImportError:
        print("matplotlib not installed, skipping plot")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
