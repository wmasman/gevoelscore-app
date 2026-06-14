"""S01 — Stabilisation trajectories.

Plot the pendulum literally. Rolling 90-day trimmed-mean of four
metrics across the full Garmin window (2021-08-16 → 2026-06-04),
anchored every 7 days. Shows how each metric drifts across the
LC-onset and stabilisation phases.

Metrics:
  1. RHR (UDS daily restingHeartRate)
  2. Avg daily stress (UDS allDayStress averageStressLevel)
  3. Sleep efficiency (TST / (TST + awake + unmeasurable))
  4. Daily max-spike-minutes (from H02b's daily_max_spike.csv)

No hypothesis test. Pure trajectory description for the
stabilisation-arc card concept.
"""
from __future__ import annotations

import csv
import json
import statistics
from datetime import date, datetime, timedelta
from pathlib import Path

# ─── Reference dates ──────────────────────────────────────────────
GARMIN_START = date(2021, 8, 16)
WINDOW_END = date(2026, 6, 5)
LC_DIAGNOSIS = date(2022, 5, 6)
GEVOELSCORE_START = date(2022, 9, 3)
ANALYTICAL_SPLIT = date(2023, 12, 31)  # the analytical convenience, NOT a real phase boundary

# ─── Rolling-window parameters ────────────────────────────────────
WINDOW_DAYS = 90
ANCHOR_STEP_DAYS = 7
TRIMMED_PCT = 0.10
MIN_VALID_IN_WINDOW = 30  # need at least this many days of data per metric in the window

# ─── Paths ────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
UDS_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Aggregator"
)
SLEEP_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Wellness"
)
SPIKE_CSV = HERE.parent / "H02b-stress-spikes" / "daily_max_spike.csv"
OUT_CSV = HERE / "trajectories.csv"
OUT_PNG = HERE / "stabilisation-arc.png"

INVALID_SLEEP_TYPES = {"UNCONFIRMED", "OFF_WRIST", "NOT_CONFIRMED"}


def load_uds() -> tuple[dict[date, int], dict[date, int]]:
    """Returns (rhr_by_date, avg_stress_by_date)."""
    rhr, stress = {}, {}
    for p in sorted(UDS_DIR.glob("UDSFile_*.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            if not cd:
                continue
            d = date.fromisoformat(cd)
            v_rhr = rec.get("restingHeartRate")
            if v_rhr not in (None, 0):
                # Keep higher (Garmin sometimes writes partial 0s in overlapping files)
                if d not in rhr or int(v_rhr) > rhr[d]:
                    rhr[d] = int(v_rhr)
            ad = rec.get("allDayStress") or {}
            agg = ad.get("aggregatorList") or []
            total = next((a for a in agg if a.get("type") == "TOTAL"), None)
            if total:
                v_stress = total.get("averageStressLevel")
                if v_stress not in (None, -1, -2):
                    if d not in stress or int(v_stress) > stress[d]:
                        stress[d] = int(v_stress)
    return rhr, stress


def load_sleep_efficiency() -> dict[date, float]:
    out = {}
    for p in sorted(SLEEP_DIR.glob("*_sleepData.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            if not cd:
                continue
            conf = rec.get("sleepWindowConfirmationType")
            if conf in INVALID_SLEEP_TYPES:
                continue
            deep = int(rec.get("deepSleepSeconds") or 0)
            light = int(rec.get("lightSleepSeconds") or 0)
            rem = int(rec.get("remSleepSeconds") or 0)
            awake = int(rec.get("awakeSleepSeconds") or 0)
            unmeas = int(rec.get("unmeasurableSeconds") or 0)
            tst = deep + light + rem
            tib = tst + awake + unmeas
            if tib < 4 * 3600:
                continue
            d = date.fromisoformat(cd)
            eff = tst / tib if tib > 0 else None
            if eff is None:
                continue
            if d not in out or tib > out[d][1]:
                out[d] = (eff, tib)
    return {d: e for d, (e, _) in out.items()}


def load_max_spike() -> dict[date, float]:
    if not SPIKE_CSV.exists():
        print(f"  WARN: {SPIKE_CSV} not found; spike trajectory will be empty.")
        return {}
    out = {}
    with SPIKE_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1":
                continue
            out[date.fromisoformat(r["date"])] = float(r["max_spike_minutes"])
    return out


def trimmed_mean(values, pct):
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    trim = int(n * pct)
    if n - 2 * trim < 1:
        return statistics.mean(s)
    return statistics.mean(s[trim : n - trim])


def rolling_trajectory(metric_by_date: dict, anchor_dates: list[date]) -> list[tuple]:
    """Returns [(anchor_date, trimmed_mean_or_none, n_in_window), ...]"""
    out = []
    for a in anchor_dates:
        ws = a - timedelta(days=WINDOW_DAYS)
        vals = [v for d, v in metric_by_date.items() if ws <= d < a]
        if len(vals) >= MIN_VALID_IN_WINDOW:
            out.append((a, trimmed_mean(vals, TRIMMED_PCT), len(vals)))
        else:
            out.append((a, None, len(vals)))
    return out


def main() -> int:
    print("Loading UDS (RHR + stress)…")
    rhr, stress = load_uds()
    print(f"  RHR days: {len(rhr)}  stress days: {len(stress)}")

    print("Loading sleep efficiency…")
    sleep_eff = load_sleep_efficiency()
    print(f"  sleep nights: {len(sleep_eff)}")

    print("Loading spike-duration (from H02b)…")
    max_spike = load_max_spike()
    print(f"  spike days: {len(max_spike)}")

    # Anchor dates: every 7 days from GARMIN_START + WINDOW_DAYS to WINDOW_END
    anchors = []
    a = GARMIN_START + timedelta(days=WINDOW_DAYS)
    while a <= WINDOW_END:
        anchors.append(a)
        a += timedelta(days=ANCHOR_STEP_DAYS)
    print(f"  anchor dates: {len(anchors)}")

    traj_rhr = rolling_trajectory(rhr, anchors)
    traj_stress = rolling_trajectory(stress, anchors)
    traj_sleep = rolling_trajectory(sleep_eff, anchors)
    traj_spike = rolling_trajectory(max_spike, anchors)

    # Write consolidated CSV
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([
            "anchor_date",
            "rhr_90d_trimmed_mean", "rhr_n",
            "avg_stress_90d_trimmed_mean", "avg_stress_n",
            "sleep_efficiency_90d_trimmed_mean", "sleep_efficiency_n",
            "max_spike_minutes_90d_trimmed_mean", "max_spike_n",
        ])
        for i, a in enumerate(anchors):
            w.writerow([
                a.isoformat(),
                f"{traj_rhr[i][1]:.2f}" if traj_rhr[i][1] is not None else "",
                traj_rhr[i][2],
                f"{traj_stress[i][1]:.2f}" if traj_stress[i][1] is not None else "",
                traj_stress[i][2],
                f"{traj_sleep[i][1]:.4f}" if traj_sleep[i][1] is not None else "",
                traj_sleep[i][2],
                f"{traj_spike[i][1]:.2f}" if traj_spike[i][1] is not None else "",
                traj_spike[i][2],
            ])
    print(f"\nwrote {OUT_CSV}")

    # ─── Plot the 2x2 grid ───
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates

        fig, axes = plt.subplots(2, 2, figsize=(14, 8), sharex=True)
        ax_list = axes.ravel()

        def plot_one(ax, traj, label, ylabel, color):
            xs = [a for a, v, n in traj if v is not None]
            ys = [v for a, v, n in traj if v is not None]
            ax.plot(xs, ys, color=color, linewidth=1.6)
            ax.set_ylabel(ylabel)
            ax.set_title(label)
            # Reference vertical lines
            ax.axvline(LC_DIAGNOSIS, color="gray", linestyle=":", alpha=0.7)
            ax.axvline(GEVOELSCORE_START, color="gray", linestyle="--", alpha=0.5)
            ax.axvline(ANALYTICAL_SPLIT, color="gray", linestyle=":", alpha=0.4)
            ax.xaxis.set_major_locator(mdates.YearLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
            ax.grid(alpha=0.25)

        plot_one(ax_list[0], traj_rhr, "Resting Heart Rate (90-day rolling mean, bpm)", "RHR (bpm)", "#c0392b")
        plot_one(ax_list[1], traj_stress, "Average daily stress (90-day rolling mean, 0-100)", "avg stress", "#d68910")
        plot_one(ax_list[2], traj_sleep, "Sleep efficiency (90-day rolling mean)", "efficiency", "#16a085")
        plot_one(ax_list[3], traj_spike, "Daily max stress-spike duration (90-day rolling mean, min)", "max spike (min)", "#8e44ad")

        # Single shared legend at the top
        from matplotlib.lines import Line2D
        legend_handles = [
            Line2D([0], [0], color="gray", linestyle=":", label="LC diagnosis 2022-05-06"),
            Line2D([0], [0], color="gray", linestyle="--", label="gevoelscore tracking start 2022-09-03"),
            Line2D([0], [0], color="gray", linestyle=":", alpha=0.5, label="analytical era split 2023-12-31"),
        ]
        fig.legend(handles=legend_handles, loc="upper center", ncol=3, frameon=False, fontsize=9)
        fig.suptitle("S01 — Stabilisation trajectories (the pendulum)", fontsize=13, y=0.99)
        fig.tight_layout(rect=[0, 0, 1, 0.93])
        fig.savefig(OUT_PNG, dpi=110)
        plt.close(fig)
        print(f"wrote {OUT_PNG}")
    except ImportError:
        print("  matplotlib not installed, skipping plot")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
