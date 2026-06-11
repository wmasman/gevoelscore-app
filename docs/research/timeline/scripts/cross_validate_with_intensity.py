"""Cross-validate reintegration hours against existing per_day_intensity + annotations.

Identifies gaps where the objective PwC reintegration record (work hours +
illness notes) disagrees with the user's retrospective triage decisions:

  - Multi-day illness stretches (3+ consecutive ziek days) not present in
    sub_threshold_dips.csv, labels_crash_v2.csv, or annotations.yaml.
  - Days with significant work hours (4+ primary hours) where
    per_day_intensity.csv has no cog_load assigned.
  - Doctor visits (bedrijfsarts/huisarts/casemanager/etc.) not present in
    annotations.yaml as medical events.

Output: data/reintegration_gaps.csv for user review (one row per gap,
same workflow as the triage rounds).
"""
from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
RESEARCH_ROOT = HERE.parent.parent

REINTEG = DATA / "reintegration_hours_2022-2024.csv"
PER_DAY_INTENSITY = DATA / "per_day_intensity.csv"
SUB_THRESHOLD_DIPS = DATA / "sub_threshold_dips.csv"
ANNOTATIONS = DATA / "annotations.yaml"
TRIAGE_EVENTS = DATA / "triage_events.csv"
LABELS_CRASH_V2 = RESEARCH_ROOT / "garmin" / "hypotheses" / "crash_v2-definition" / "labels_crash_v2.csv"
OUTPUT = DATA / "reintegration_gaps.csv"


def parse_iso(s):
    if not s:
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def load_existing_dip_dates() -> set[date]:
    """Set of dates already marked as dip / crash in any of our sources."""
    out: set[date] = set()
    if SUB_THRESHOLD_DIPS.exists():
        for r in csv.DictReader(SUB_THRESHOLD_DIPS.open(encoding="utf-8")):
            d = parse_iso(r.get("date"))
            if d:
                out.add(d)
    if LABELS_CRASH_V2.exists():
        for r in csv.DictReader(LABELS_CRASH_V2.open(encoding="utf-8")):
            d = parse_iso(r.get("date"))
            if d and r.get("label") in ("dip", "crash"):
                out.add(d)
    return out


def load_existing_loaded_dates() -> set[date]:
    """Set of dates with any cog/phy/emo load in per_day_intensity.csv."""
    out: set[date] = set()
    if PER_DAY_INTENSITY.exists():
        for r in csv.DictReader(PER_DAY_INTENSITY.open(encoding="utf-8")):
            d = parse_iso(r.get("date"))
            if not d:
                continue
            if any((r.get(k) or "").strip() for k in ("cog", "phy", "emo")):
                out.add(d)
    return out


def load_existing_medical_dates() -> set[date]:
    """Dates with a medical span in annotations.yaml or triage_events.csv."""
    out: set[date] = set()
    if ANNOTATIONS.exists():
        raw = yaml.safe_load(ANNOTATIONS.read_text(encoding="utf-8")) or {}
        for s in (raw.get("spans") or []):
            if s.get("category") != "medical":
                continue
            d_start = parse_iso(s.get("start"))
            d_end = parse_iso(s.get("end")) or d_start
            if d_start:
                d = d_start
                while d <= d_end:
                    out.add(d)
                    d += timedelta(days=1)
    if TRIAGE_EVENTS.exists():
        for r in csv.DictReader(TRIAGE_EVENTS.open(encoding="utf-8")):
            if r.get("category") != "medical":
                continue
            d_start = parse_iso(r.get("date_start"))
            d_end = parse_iso(r.get("date_end")) or d_start
            if d_start:
                d = d_start
                while d <= d_end:
                    out.add(d)
                    d += timedelta(days=1)
    return out


def find_illness_stretches(rows: list[dict], min_length: int = 3) -> list[dict]:
    """Returns list of {start, end, length, dates} for consecutive illness days."""
    sorted_rows = sorted(rows, key=lambda r: r["date"])
    stretches = []
    current_dates: list[date] = []
    for r in sorted_rows:
        d = date.fromisoformat(r["date"])
        if r.get("illness_flag") in ("1", 1):
            if current_dates and (d - current_dates[-1]).days <= 2:
                # Same stretch (allow weekends as gaps)
                current_dates.append(d)
            else:
                if len(current_dates) >= min_length:
                    stretches.append({
                        "start": current_dates[0],
                        "end": current_dates[-1],
                        "length": len(current_dates),
                        "dates": list(current_dates),
                    })
                current_dates = [d]
        else:
            if len(current_dates) >= min_length:
                stretches.append({
                    "start": current_dates[0],
                    "end": current_dates[-1],
                    "length": len(current_dates),
                    "dates": list(current_dates),
                })
            current_dates = []
    if len(current_dates) >= min_length:
        stretches.append({
            "start": current_dates[0],
            "end": current_dates[-1],
            "length": len(current_dates),
            "dates": list(current_dates),
        })
    return stretches


def main():
    rows = list(csv.DictReader(REINTEG.open(encoding="utf-8")))
    existing_dips = load_existing_dip_dates()
    existing_loaded = load_existing_loaded_dates()
    existing_medical = load_existing_medical_dates()

    gaps = []

    # 1. Multi-day illness stretches not in existing dip records
    stretches = find_illness_stretches(rows, min_length=3)
    for s in stretches:
        # Already covered if at least one date in stretch is in existing_dips
        overlap = sum(1 for d in s["dates"] if d in existing_dips)
        gaps.append({
            "gap_type": "illness_stretch",
            "date_start": s["start"].isoformat(),
            "date_end": s["end"].isoformat(),
            "length": s["length"],
            "context": f"{s['length']}-dag ziekteperiode uit PwC-data",
            "overlap_with_existing": f"{overlap} of {s['length']} dgn al gemarkeerd als dip/crash",
            "needs_review": "y" if overlap < s["length"] / 2 else "n",
        })

    # 2. Days with >=4 work hours where no cog_load is assigned
    for r in rows:
        try:
            total = float(r.get("total_hours") or 0)
        except ValueError:
            total = 0
        d = date.fromisoformat(r["date"])
        if total >= 4 and d not in existing_loaded:
            gaps.append({
                "gap_type": "work_heavy_no_load",
                "date_start": d.isoformat(),
                "date_end": d.isoformat(),
                "length": 1,
                "context": f"{total}h werk, geen per_day_intensity load. Note: {(r.get('toelichting') or '')[:80]}",
                "overlap_with_existing": "",
                "needs_review": "y",
            })

    # 3. Doctor visits not in annotations
    for r in rows:
        if r.get("doctor_visit_flag") not in ("1", 1):
            continue
        d = date.fromisoformat(r["date"])
        if d in existing_medical:
            continue
        gaps.append({
            "gap_type": "doctor_visit_missing",
            "date_start": d.isoformat(),
            "date_end": d.isoformat(),
            "length": 1,
            "context": f"doctor visit: {(r.get('toelichting') or '')[:80]}",
            "overlap_with_existing": "",
            "needs_review": "y",
        })

    fields = ["gap_type", "date_start", "date_end", "length",
              "needs_review", "context", "overlap_with_existing"]
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for g in gaps:
            w.writerow({k: g.get(k, "") for k in fields})

    # Summary
    n_stretches = sum(1 for g in gaps if g["gap_type"] == "illness_stretch")
    n_work = sum(1 for g in gaps if g["gap_type"] == "work_heavy_no_load")
    n_doc = sum(1 for g in gaps if g["gap_type"] == "doctor_visit_missing")
    print(f"Found {len(gaps)} gaps:")
    print(f"  illness stretches (>=3 dgn): {n_stretches}")
    print(f"  work-heavy days without cog_load: {n_work}")
    print(f"  doctor visits missing from annotations: {n_doc}")
    print()
    print("Top 10 illness stretches:")
    for g in [g for g in gaps if g["gap_type"] == "illness_stretch"][:10]:
        print(f"  {g['date_start']} -> {g['date_end']} ({g['length']}d): {g['overlap_with_existing']}")
    print(f"\nWrote {OUTPUT}")


if __name__ == "__main__":
    main()
