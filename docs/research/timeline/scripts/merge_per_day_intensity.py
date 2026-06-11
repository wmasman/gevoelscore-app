"""Merge per-year triaged per_day_intensity_YYYY.csv files into per_day_intensity.csv.

Reads:
  - data/per_day_intensity_YYYY.csv (for each year specified or all years found)
  - data/per_day_intensity.csv (existing source of truth)

Writes:
  - data/per_day_intensity.csv (updated, sorted by date)

Merge rule:
  - A row in a per-year CSV is considered TRIAGED if any of
    cog_load / phy_load / emo_load / notes is non-empty.
  - For each triaged row, replace any existing entry with the same date.
    Untriaged rows do not overwrite existing entries.

Usage:
  python merge_per_day_intensity.py            # merge all per_day_intensity_*.csv
  python merge_per_day_intensity.py 2026 2025  # merge specific years only
"""
from __future__ import annotations

import csv
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMELINE_ROOT = HERE.parent
DATA = TIMELINE_ROOT / "data"

MASTER = DATA / "per_day_intensity.csv"
MASTER_FIELDS = ["date", "cog", "phy", "emo", "source", "notes"]


def parse_date(s) -> date | None:
    if not s:
        return None
    try:
        return date.fromisoformat(str(s))
    except ValueError:
        return None


def load_master() -> dict[date, dict]:
    """Returns date -> row dict for existing per_day_intensity.csv."""
    if not MASTER.exists():
        return {}
    out = {}
    for r in csv.DictReader(MASTER.open(encoding="utf-8")):
        d = parse_date(r.get("date"))
        if d:
            out[d] = {k: r.get(k, "") for k in MASTER_FIELDS}
    return out


def is_triaged(r: dict) -> bool:
    """A per-year row is triaged if any of cog/phy/emo OR notes is non-empty."""
    for k in ("cog_load", "phy_load", "emo_load", "notes"):
        if (r.get(k) or "").strip():
            return True
    return False


def merge_year_csv(csv_path: Path, master: dict[date, dict], source_tag: str) -> tuple[int, int, int]:
    """Returns (n_rows, n_triaged, n_merged)."""
    if not csv_path.exists():
        return 0, 0, 0
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    n_triaged = 0
    n_merged = 0
    for r in rows:
        if not is_triaged(r):
            continue
        n_triaged += 1
        d = parse_date(r.get("date"))
        if d is None:
            continue
        existing = master.get(d)
        new_entry = {
            "date": d.isoformat(),
            "cog": (r.get("cog_load") or "").strip(),
            "phy": (r.get("phy_load") or "").strip(),
            "emo": (r.get("emo_load") or "").strip(),
            "source": source_tag,
            "notes": (r.get("notes") or "").strip(),
        }
        # If existing entry is from an EARLIER source (e.g. consolidation_2026-06-10
        # vs bulk_triage_2026), the new entry from the bulk triage wins because
        # the user explicitly re-touched it. Preserve the source tag of the new
        # round.
        master[d] = new_entry
        n_merged += 1
    return len(rows), n_triaged, n_merged


def write_master(master: dict[date, dict]):
    sorted_rows = sorted(master.values(), key=lambda r: r["date"])
    with MASTER.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=MASTER_FIELDS)
        w.writeheader()
        for r in sorted_rows:
            w.writerow({k: r.get(k, "") for k in MASTER_FIELDS})


def main():
    args = sys.argv[1:]
    if args:
        years = [int(a) for a in args]
        csvs = [DATA / f"per_day_intensity_{y}.csv" for y in years]
        csvs = [p for p in csvs if p.exists()]
    else:
        csvs = sorted([p for p in DATA.glob("per_day_intensity_*.csv")
                       if re.match(r"per_day_intensity_\d{4}\.csv$", p.name)])

    if not csvs:
        print("No per_day_intensity_YYYY.csv files found.")
        return

    print(f"Loading master ({MASTER.name})...")
    master = load_master()
    print(f"  existing entries: {len(master)}")
    print()

    for csv_path in csvs:
        m = re.search(r"per_day_intensity_(\d{4})\.csv", csv_path.name)
        year = m.group(1) if m else "unknown"
        source_tag = f"bulk_triage_{year}_2026-06-10"
        n_rows, n_triaged, n_merged = merge_year_csv(csv_path, master, source_tag)
        print(f"  {csv_path.name}: {n_rows} rows | {n_triaged} triaged | {n_merged} merged into master")

    write_master(master)
    print()
    print(f"Wrote {MASTER}")
    print(f"  total entries now: {len(master)}")


if __name__ == "__main__":
    main()
