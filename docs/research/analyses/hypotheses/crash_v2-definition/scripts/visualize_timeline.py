"""Visualize the full gevoelscore timeline with crash_v1 / crash_v2 bands.

Output: timeline_v1_v2.png — multi-row plot, one calendar year per row,
with crash episodes shaded red and isolated dips marked as orange vertical lines.

For sanity-checking: every red band should correspond to a visible
sustained low (score <= 3) stretch; every orange line should sit on
an isolated score <= 3 day with score >= 4 neighbours.
"""
from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABELS_CSV = ROOT / "labels_crash_v2.csv"
OUT_PNG = ROOT / "timeline_v1_v2.png"


def load_labels() -> list[dict]:
    with LABELS_CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["date"] = date.fromisoformat(r["date"])
        r["score"] = int(r["score"])
    return rows


def crash_episode_ranges(rows: list[dict]) -> list[tuple[date, date]]:
    """Returns list of (start_date, end_date) for crash episodes."""
    by_episode: dict[str, list[date]] = {}
    for r in rows:
        if r["label"] == "crash":
            by_episode.setdefault(r["episode_id"], []).append(r["date"])
    out = []
    for eid, dates_ in by_episode.items():
        out.append((min(dates_), max(dates_)))
    return sorted(out)


def dip_dates(rows: list[dict]) -> list[date]:
    return sorted(r["date"] for r in rows if r["label"] == "dip")


def dip_cluster_ranges(rows: list[dict]) -> list[tuple[date, date, int]]:
    """Returns list of (first_dip_date, last_dip_date, n_dips) per cluster."""
    by_cluster: dict[str, list[date]] = {}
    for r in rows:
        cid = r.get("dip_cluster_id", "")
        if r["label"] == "dip" and cid:
            by_cluster.setdefault(cid, []).append(r["date"])
    out = []
    for cid, dates_ in by_cluster.items():
        out.append((min(dates_), max(dates_), len(dates_)))
    return sorted(out)


def main():
    rows = load_labels()
    crashes = crash_episode_ranges(rows)
    dips = dip_dates(rows)
    clusters = dip_cluster_ranges(rows)
    print(f"Loaded {len(rows)} day rows | "
          f"{len(crashes)} crash episodes | {len(dips)} isolated dips | "
          f"{len(clusters)} dip clusters")

    # Build per-year ranges
    first = min(r["date"] for r in rows)
    last = max(r["date"] for r in rows)
    years = list(range(first.year, last.year + 1))

    fig, axes = plt.subplots(
        len(years), 1,
        figsize=(20, 2.4 * len(years)),
        sharey=True,
    )
    if len(years) == 1:
        axes = [axes]

    for ax, year in zip(axes, years):
        y_start = date(year, 1, 1)
        y_end = date(year, 12, 31)
        # Trim partial first / last year to actual data
        if year == first.year:
            y_start = first
        if year == last.year:
            y_end = last

        year_rows = [r for r in rows if y_start <= r["date"] <= y_end]
        xs = [r["date"] for r in year_rows]
        ys = [r["score"] for r in year_rows]

        # Score line + scatter
        ax.plot(xs, ys, color="black", linewidth=0.5, alpha=0.6, zorder=2)
        ax.scatter(xs, ys, color="black", s=5, alpha=0.7, zorder=3)

        # Dip cluster overlays (light grey background bands, drawn first / zorder=0)
        cluster_labeled = False
        for cstart, cend, n in clusters:
            if cend < y_start or cstart > y_end:
                continue
            band_start = max(cstart, y_start)
            band_end = min(cend, y_end) + timedelta(days=1)
            label = "dip cluster (>=2 dips in 7d window)" if not cluster_labeled else None
            ax.axvspan(band_start, band_end, color="grey", alpha=0.15, zorder=0,
                       label=label)
            cluster_labeled = True

        # Crash bands (red)
        crash_labeled = False
        for cstart, cend in crashes:
            if cend < y_start or cstart > y_end:
                continue
            band_start = max(cstart, y_start)
            band_end = min(cend, y_end) + timedelta(days=1)  # inclusive end
            label = "crash (v1 = v2 tier 1)" if not crash_labeled else None
            ax.axvspan(band_start, band_end, color="red", alpha=0.22, zorder=1,
                       label=label)
            crash_labeled = True

        # Dip markers (orange vertical lines spanning the day)
        dip_labeled = False
        for d in dips:
            if d < y_start or d > y_end:
                continue
            label = "dip (v2 tier 2, isolated bad day)" if not dip_labeled else None
            ax.axvspan(d, d + timedelta(days=1), color="orange",
                       alpha=0.50, zorder=1, label=label)
            dip_labeled = True

        # Reference lines
        ax.axhline(3, color="grey", linestyle="--", linewidth=0.6, zorder=2,
                   label="score = 3 threshold" if year == first.year else None)
        ax.axhline(4, color="grey", linestyle=":", linewidth=0.4, zorder=2,
                   label="score = 4 (dip neighbour bar)" if year == first.year else None)

        # Axis formatting
        ax.set_xlim(y_start, y_end + timedelta(days=1))
        ax.set_ylim(0.5, 10.5)
        ax.set_ylabel("score")
        ax.set_title(f"{year}", loc="left", fontsize=11)
        ax.grid(True, alpha=0.25, zorder=0)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator())

        if year == first.year:
            ax.legend(loc="lower right", fontsize=8, framealpha=0.9)

    fig.suptitle(
        "gevoelscore timeline | red = crash (v1 = v2 tier 1) | "
        f"orange = isolated dip | grey = dip cluster (>=2 dips in 7d) | "
        f"{len(crashes)} crashes, {len(dips)} dips, {len(clusters)} clusters, "
        f"{first} -> {last}",
        fontsize=12, y=1.0,
    )
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=130, bbox_inches="tight")
    print(f"Wrote {OUT_PNG}")


if __name__ == "__main__":
    main()
