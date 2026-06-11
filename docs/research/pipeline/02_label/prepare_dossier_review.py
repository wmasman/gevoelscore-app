"""Prepare pwc_dossier_2022-2024.csv for per-entry user review.

Reads:  data/pwc_dossier_2022-2024.csv (the user-curated dossier extract)
Writes: data/pwc_dossier_review.csv (review-ready format, one row per entry)

Applies the agreed mapping (dossier category/type -> annotations category)
to suggest a target. The user can override per row via the action_to_take
column. Admin-only rows (ondertekening + document types) are pre-filtered
out per user decision (these are paper-trail signatures, not timeline events).
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

INPUT = DATA / "pwc_dossier_2022-2024.csv"
OUTPUT = DATA / "pwc_dossier_review.csv"

# Rows that are paper-trail-only (signatures, doc creation) - skip per user decision.
SKIP_TYPES = {"ondertekening", "document"}

# Category mapping: (dossier_category, dossier_type) -> annotations_category
# When type is not in the mapping, fall back on category default.
CATEGORY_MAP = {
    # Health events
    ("health_event", "crash_period"): "crash",
    ("health_event", "crash"): "crash",
    ("health_event", "crash_start"): "marker",  # paired with crash_period, skip standalone
    ("health_event", "crash_end"): "marker",    # ditto
    ("health_event", "terugslag"): "dip",
    ("health_event", "terugval"): "dip",        # monthly-precision terugval -> dip
    ("health_event", "first_episode"): "high_intensity",  # initial illness
    ("health_event", "onset"): "marker",
    ("health_event", "uitval"): "marker",
    ("health_event", "herstart"): "marker",
    ("health_event", "opbouw"): "marker",
    # Bedrijfsarts
    ("bedrijfsarts", "consult"): "medical",
    ("bedrijfsarts", "telefonisch"): "medical",
    ("bedrijfsarts", "videoconsult"): "medical",
    ("bedrijfsarts", "IZP"): "medical",
    ("bedrijfsarts", "actueel_oordeel"): "medical",
    # Arbeidsdeskundig
    ("arbeidsdeskundig", "onderzoek"): "medical",
    ("arbeidsdeskundig", "rapportage"): "medical",
    ("arbeidsdeskundig", "concept"): "marker",
    ("arbeidsdeskundig", "opbouwschema"): "interventie",  # multi-day umbrella
    # PwC intern
    ("pwc_intern", "meeting"): "levensgebeurtenis",
    ("pwc_intern", "contact"): "levensgebeurtenis",
    ("pwc_intern", "actie"): "levensgebeurtenis",
    ("pwc_intern", "milestone"): "marker",
    ("pwc_intern", "vakantie"): "levensgebeurtenis",        # multi-day rest period
    ("pwc_intern", "wachttijd_loondoorbetaling"): "levensgebeurtenis",  # 24-month umbrella
    # Spoor 2
    ("spoor_2", "intake"): "medical",
    ("spoor_2", "sessie"): "medical",
    ("spoor_2", "trajectduur"): "interventie",  # multi-day umbrella
    ("spoor_2", "ziekmelding"): "dip",
    # UWV
    ("uwv", "upload"): "marker",
}


def clean(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def main():
    if not INPUT.exists():
        print(f"ERROR: {INPUT} does not exist.")
        return 1

    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    rows = [r for r in rows if r.get("date_start")]  # skip blank rows

    out = []
    n_skipped = 0
    for r in rows:
        if r.get("type", "") in SKIP_TYPES:
            n_skipped += 1
            continue
        key = (r.get("category", ""), r.get("type", ""))
        suggested = CATEGORY_MAP.get(key, "")
        if not suggested:
            # Fallback: category-level default
            suggested = {
                "health_event": "high_intensity",
                "bedrijfsarts": "medical",
                "arbeidsdeskundig": "medical",
                "pwc_intern": "levensgebeurtenis",
                "spoor_2": "medical",
                "uwv": "marker",
            }.get(r.get("category", ""), "levensgebeurtenis")

        # Notice: crash_start/crash_end paired with a crash_period: we suggest skipping
        # standalone (paired entries are redundant if the crash_period span is added)
        suggested_action = "accept"
        if r.get("type") in ("crash_start", "crash_end"):
            suggested_action = "skip"  # redundant with crash_period span

        # Multi-day flag preserved
        out.append({
            "date_start": r["date_start"],
            "date_end": r["date_end"],
            "multi_day": r.get("multi_day", "no"),
            "date_precision": r.get("date_precision", "day"),
            "dossier_category": r["category"],
            "dossier_type": r["type"],
            "title": r["title"],
            "person": r.get("person", ""),
            "source_pdf": r.get("source_pdf", ""),
            "suggested_annotations_category": suggested,
            "suggested_action": suggested_action,
            "action_to_take": "",  # USER FILLS: accept / skip / change_category:X / change_label:X
            "user_label_override": "",
            "user_notes": "",
            "dossier_notes": clean(r.get("notes", ""))[:200],
        })

    out.sort(key=lambda r: (r["date_start"], r["dossier_category"]))

    fields = ["date_start", "date_end", "multi_day", "date_precision",
              "dossier_category", "dossier_type",
              "title", "person", "source_pdf",
              "suggested_annotations_category", "suggested_action",
              "action_to_take", "user_label_override", "user_notes",
              "dossier_notes"]
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in out:
            w.writerow(r)

    print(f"Wrote {OUTPUT}")
    print(f"  Total rows for review: {len(out)}")
    print(f"  Skipped (admin/paper-trail): {n_skipped}")
    print()
    print("By suggested category:")
    from collections import Counter
    cats = Counter(r["suggested_annotations_category"] for r in out)
    for k, n in cats.most_common():
        print(f"  {k}: {n}")
    print()
    print("By suggested action:")
    acts = Counter(r["suggested_action"] for r in out)
    for k, n in acts.most_common():
        print(f"  {k}: {n}")


if __name__ == "__main__":
    raise SystemExit(main())
