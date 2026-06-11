"""Classify the 2026 triage notes from per_day_intensity_2026.csv into actionable buckets.

Buckets:
  - new_events            potential event annotations not in calendar/notes
  - data_quality          observations about missing tags or data gaps
  - quasi_crash_context   score<=4 days with crash-like symptoms in triage notes
  - boilerplate           "triaged no loads" type non-informative
  - other                 informative but doesn't fit above

This is a surfacing tool, not an automatic categorizer. The user reviews
each bucket and decides what to do with each row.

Output: stdout summary + data/triage_notes_classified.csv for sheet upload.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

import sys

_year_arg = next((a for a in sys.argv[1:] if a.isdigit() and len(a) == 4), "2026")
INPUT_CSV = DATA / f"per_day_intensity_{_year_arg}.csv"
OUTPUT_CSV = DATA / f"triage_notes_classified_{_year_arg}.csv"


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


# Heuristic classifier patterns
BOILERPLATE = re.compile(
    r"^\s*(triaged\s*)?no\s*(specific\s*)?loads?\b"
    r"|^\s*no\s+data\s+that\s+signifies\s+loads?\b"
    r"|^\s*no\s+loads?\s+identified\b"
    r"|^\s*no\s+additional\s+loads?\s+data\b",
    re.IGNORECASE,
)

DATA_QUALITY = re.compile(
    r"\b(tag|category|categor|reference|cross[-\s]?ref|need\s+a\s+tag"
    r"|need\s+to\s+tag|add\s+to\s+events|missing|add\s+a\s+|adjust|change)\b",
    re.IGNORECASE,
)

CRASH_CONTEXT = re.compile(
    r"\b(gepusht|teveel|te\s*veel|kapot|uitgeput|moe|hoofdpijn|brainfog"
    r"|crash|dip|terugslag|groggy|niet\s+lekker|slecht\s+geslapen"
    r"|pushed\s+(too\s+)?hard|overdaan|naproxen|paracetamol|pijnstil)\b",
    re.IGNORECASE,
)

# A "potential new event" is a short triage note that looks like an event
# label and is not boilerplate / data-quality / crash-context.
EVENT_HINT = re.compile(
    r"\b(koffie|meeting|met\s+\w+|verjaardag|borrel|gesprek|brainstorm"
    r"|interview|sessie|consult|naar\s+|in\s+de\s+(auto|trein)"
    r"|preparing\s+for|in\s+the\s+car|bestuur|congres|uitje|uit\s+eten"
    r"|kennismaking|reintegratie|breinvoeding|huisarts|tandarts|opvoedcoach"
    r"|open\s+dag|conversation|conversations|werk\s+|busy\s+day|sessions?"
    r"|event\s+for\s+the\s+day|add\s+to\s+events|happens?\s+today"
    r"|birthday|family|family\s+(dinner|day)|familie)\b",
    re.IGNORECASE,
)

# Explicit "dip" or sub-threshold-crash language from the user.
USER_DIP_LABEL = re.compile(
    r"\b(dip\s+day|despite\s+the\s+\d|sub.?threshold|quasi.?crash"
    r"|hidden\s+crash|probably\s+a\s+dip)\b",
    re.IGNORECASE,
)


def classify(triage: str, orig: str, score: str) -> str:
    triage = (triage or "").strip()
    if not triage:
        return "boilerplate"
    if BOILERPLATE.search(triage):
        return "boilerplate"

    # User explicit dip language overrides everything else
    if USER_DIP_LABEL.search(triage):
        return "user_marked_dip"

    # Crash context: only count if score is 3-4 AND triage note has crash signal
    is_low_score = False
    try:
        is_low_score = int(score) <= 4
    except (TypeError, ValueError):
        pass
    triage_has_crash_signal = CRASH_CONTEXT.search(triage) is not None
    orig_has_crash_signal = CRASH_CONTEXT.search(orig or "") is not None

    has_dq = DATA_QUALITY.search(triage)
    has_event = EVENT_HINT.search(triage)

    if has_dq:
        return "data_quality"
    if is_low_score and (triage_has_crash_signal or orig_has_crash_signal):
        return "quasi_crash_context"
    if has_event:
        return "new_events"
    return "other"


def main():
    rows = list(csv.DictReader(INPUT_CSV.open(encoding="utf-8")))
    out_rows = []
    counts = {"new_events": 0, "data_quality": 0,
              "quasi_crash_context": 0, "user_marked_dip": 0,
              "boilerplate": 0, "other": 0}

    for r in rows:
        triage = (r.get("notes") or "").strip()
        if not triage:
            continue
        orig = (r.get("note_full") or "").strip()
        score = (r.get("score") or "").strip()
        bucket = classify(triage, orig, score)
        counts[bucket] += 1
        out_rows.append({
            "date": r["date"],
            "score": score,
            "bucket": bucket,
            "cog_load": (r.get("cog_load") or "").strip(),
            "phy_load": (r.get("phy_load") or "").strip(),
            "emo_load": (r.get("emo_load") or "").strip(),
            "triage_note": clean(triage),
            "original_note": clean(orig),
            "events_on_day": clean((r.get("events_on_day") or ""))[:100],
            "action_to_take": "",  # user fills: add_event / refine_tags / mark_dip / skip
        })

    # Write classified CSV
    fields = ["date", "score", "bucket", "cog_load", "phy_load", "emo_load",
              "triage_note", "original_note", "events_on_day", "action_to_take"]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        # Order: non-boilerplate first, then by date within bucket
        bucket_order = ["user_marked_dip", "quasi_crash_context", "data_quality",
                        "new_events", "other", "boilerplate"]
        out_rows.sort(key=lambda r: (bucket_order.index(r["bucket"]), r["date"]))
        for r in out_rows:
            w.writerow(r)

    print(f"Classified {sum(counts.values())} triage notes from {INPUT_CSV.name}:")
    for b, n in counts.items():
        print(f"  {b:25}: {n}")
    print()
    print(f"Wrote {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
