"""Plot 30-day rolling baseline trajectories for the core exertion metrics.

Surfaces the envelope shifts that z-scores / percentile ranks cancel out.
'Your typical max HR drifted from 115 in mid-2024 to 122 in early-2026' is
the kind of pattern this plot makes visible.

Earlier S01 work that this referenced has been archived; this
script's descriptive plot stands on its own.
"""
from __future__ import annotations

import csv
import statistics
from datetime import date, timedelta
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CSV_PATH = ROOT / "output" / "activity_features_daily.csv"
OUT_PNG = ROOT / "output" / "baseline_trajectories.png"

ROLLING_WINDOW = 30


def parse_num(v):
    if v in (None, "", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def rolling_median(values_by_date: dict[date, float | None], window: int) -> dict[date, float]:
    """For each date with enough prior valid data, compute median of last `window` days."""
    out = {}
    sorted_dates = sorted(values_by_date)
    for d in sorted_dates:
        prior = []
        for i in range(1, window + 1):
            wd = d - timedelta(days=i)
            v = values_by_date.get(wd)
            if v is not None:
                prior.append(v)
        if len(prior) >= window // 2:
            out[d] = statistics.median(prior)
    return out


def main():
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    print(f"Loaded {len(rows)} rows")

    # Build per-date dicts for each metric
    metrics = {
        "effective_exertion_min": [],
        "total_steps": [],
        "max_hr_uds": [],
        "vigorous_min_uds": [],
    }
    by_date = {m: {} for m in metrics}
    for r in rows:
        d = date.fromisoformat(r["date"])
        for m in metrics:
            v = parse_num(r.get(m))
            if v is not None:
                by_date[m][d] = v

    # Rolling baselines
    baselines = {m: rolling_median(by_date[m], ROLLING_WINDOW) for m in metrics}
    for m, b in baselines.items():
        print(f"  {m}: {len(b)} baseline days")

    fig, axes = plt.subplots(4, 1, figsize=(18, 12), sharex=True)
    titles = {
        "effective_exertion_min": "Effective exertion min (UDS vigorous + 0.5*moderate or recorded duration)",
        "total_steps": "Total steps",
        "max_hr_uds": "Daily peak HR (UDS)",
        "vigorous_min_uds": "Vigorous intensity minutes (UDS)",
    }
    colors = {
        "effective_exertion_min": "#cc3300",
        "total_steps": "#0066cc",
        "max_hr_uds": "#cc0066",
        "vigorous_min_uds": "#9933cc",
    }

    for ax, m in zip(axes, metrics):
        # Plot raw daily values (light scatter)
        sorted_d = sorted(by_date[m])
        ax.scatter(
            sorted_d, [by_date[m][d] for d in sorted_d],
            s=2, color="grey", alpha=0.3, zorder=1, label="daily",
        )
        # Plot rolling baseline (thick line)
        bd = sorted(baselines[m])
        ax.plot(
            bd, [baselines[m][d] for d in bd],
            color=colors[m], linewidth=2.2, zorder=3,
            label=f"{ROLLING_WINDOW}-day rolling median",
        )
        ax.set_ylabel(m, fontsize=9)
        ax.set_title(titles[m], loc="left", fontsize=10)
        ax.grid(True, alpha=0.25)
        ax.legend(loc="upper right", fontsize=8, framealpha=0.9)
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    # Mark gevoelscore analysis window start for reference
    for ax in axes:
        ax.axvline(date(2022, 9, 3), color="black", linestyle=":",
                   linewidth=0.6, alpha=0.6)

    fig.suptitle(
        "Baseline trajectories (30-day rolling median) of core exertion metrics\n"
        "Grey dots = daily values. Coloured line = rolling baseline. "
        "Dotted vertical = gevoelscore analysis window start (2022-09-03).",
        fontsize=11, y=1.0,
    )
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=130, bbox_inches="tight")
    print(f"Wrote {OUT_PNG}")


if __name__ == "__main__":
    main()
