"""Timeline visualization combining gevoelscore + crash_v2 labels + exertion class.

For each calendar year row:
  - Score line + scatter (top)
  - Red bands for crash episodes
  - Orange bands for isolated dip days
  - Grey background bands for dip clusters
  - Thin colored strip at the bottom showing exertion_class per day

Helps visually answer: do heavy-exertion days cluster around crashes/dips?
"""
from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FEATURES_CSV = ROOT / "output" / "activity_features_daily.csv"
LABELS_CSV = (
    ROOT.parent / "hypotheses" / "crash_v2-definition" / "labels_crash_v2.csv"
)
OUT_PNG = ROOT / "output" / "timeline_with_activity.png"

EXERTION_COLORS = {
    "none": "#f5f5f5",       # very pale grey
    "light": "#cfe5cf",      # pale green
    "moderate": "#ffe699",   # pale yellow/amber
    "heavy": "#ff9966",      # orange-red
    "very_heavy": "#cc0000", # deep red
}


def load_labels() -> dict[date, str]:
    out = {}
    with LABELS_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[date.fromisoformat(r["date"])] = {
                "label": r["label"],
                "episode_id": r["episode_id"],
                "dip_cluster_id": r.get("dip_cluster_id", ""),
            }
    return out


def load_features() -> dict[date, dict]:
    out = {}
    with FEATURES_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[date.fromisoformat(r["date"])] = r
    return out


def main():
    labels = load_labels()
    features = load_features()
    print(f"Loaded {len(labels)} label rows, {len(features)} feature rows")

    # Crashes
    crash_episodes: dict[str, list[date]] = {}
    for d, lab in labels.items():
        if lab["label"] == "crash":
            crash_episodes.setdefault(lab["episode_id"], []).append(d)
    crashes = sorted((min(ds), max(ds)) for ds in crash_episodes.values())

    # Dips
    dips = sorted(d for d, lab in labels.items() if lab["label"] == "dip")

    # Clusters
    cluster_dates: dict[str, list[date]] = {}
    for d, lab in labels.items():
        cid = lab.get("dip_cluster_id", "")
        if lab["label"] == "dip" and cid:
            cluster_dates.setdefault(cid, []).append(d)
    clusters = sorted((min(ds), max(ds)) for ds in cluster_dates.values())

    # Scores
    score_by_date = {d: int(r["gevoelscore"]) for d, r in features.items()
                     if r["gevoelscore"]}

    # Per-year plot
    first = min(score_by_date)
    last = max(score_by_date)
    years = list(range(first.year, last.year + 1))
    fig, axes = plt.subplots(len(years), 1, figsize=(20, 3.2 * len(years)),
                             sharey=True)
    if len(years) == 1:
        axes = [axes]

    for ax, year in zip(axes, years):
        y_start = date(year, 1, 1)
        y_end = date(year, 12, 31)
        if year == first.year:
            y_start = first
        if year == last.year:
            y_end = last

        year_dates = sorted(d for d in score_by_date if y_start <= d <= y_end)
        ys = [score_by_date[d] for d in year_dates]

        # Cluster bands (light grey, zorder=0)
        first_label = True
        for cstart, cend in clusters:
            if cend < y_start or cstart > y_end:
                continue
            ax.axvspan(
                max(cstart, y_start),
                min(cend, y_end) + timedelta(days=1),
                color="grey", alpha=0.15, zorder=0,
                label="dip cluster" if first_label else None,
            )
            first_label = False

        # Crash bands
        first_label = True
        for cstart, cend in crashes:
            if cend < y_start or cstart > y_end:
                continue
            ax.axvspan(
                max(cstart, y_start),
                min(cend, y_end) + timedelta(days=1),
                color="red", alpha=0.22, zorder=1,
                label="crash" if first_label else None,
            )
            first_label = False

        # Dip markers
        first_label = True
        for d in dips:
            if d < y_start or d > y_end:
                continue
            ax.axvspan(
                d, d + timedelta(days=1),
                color="orange", alpha=0.5, zorder=1,
                label="dip" if first_label else None,
            )
            first_label = False

        # Exertion-class strip at the bottom of the panel
        # Each day is a thin colored bar at y=1.0 (just below score scale)
        strip_y_base = 0.4
        strip_height = 0.6
        for d in year_dates:
            cls = features[d].get("exertion_class", "")
            if cls and cls in EXERTION_COLORS:
                ax.axvspan(
                    d, d + timedelta(days=1),
                    ymin=0.0, ymax=0.08,  # bottom 8% of axis
                    color=EXERTION_COLORS[cls],
                    alpha=0.9, zorder=2,
                )

        # Score line + scatter
        ax.plot(year_dates, ys, color="black", linewidth=0.5, alpha=0.6, zorder=3)
        ax.scatter(year_dates, ys, color="black", s=5, alpha=0.7, zorder=4)

        # Reference lines
        ax.axhline(3, color="grey", linestyle="--", linewidth=0.6, zorder=2)
        ax.axhline(4, color="grey", linestyle=":", linewidth=0.4, zorder=2)

        ax.set_xlim(y_start, y_end + timedelta(days=1))
        ax.set_ylim(0.5, 10.5)
        ax.set_ylabel("score")
        ax.set_title(f"{year}", loc="left", fontsize=11)
        ax.grid(True, alpha=0.25, zorder=0)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

        if year == first.year:
            # Single combined legend
            handles = [
                Patch(color="red", alpha=0.22, label="crash"),
                Patch(color="orange", alpha=0.5, label="dip"),
                Patch(color="grey", alpha=0.15, label="dip cluster"),
            ] + [
                Patch(color=c, alpha=0.9, label=f"exertion: {cls}")
                for cls, c in EXERTION_COLORS.items()
            ]
            ax.legend(handles=handles, loc="lower right", fontsize=7,
                      framealpha=0.95, ncol=2)

    fig.suptitle(
        f"gevoelscore + crash_v2 labels + exertion class (bottom strip) | "
        f"{len(crashes)} crashes, {len(dips)} dips, {len(clusters)} clusters",
        fontsize=12, y=1.0,
    )
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=130, bbox_inches="tight")
    print(f"Wrote {OUT_PNG}")


if __name__ == "__main__":
    main()
