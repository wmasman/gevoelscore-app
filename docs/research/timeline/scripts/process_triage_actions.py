"""Process action_to_take decisions from triage_notes_classified.csv.

Distributes rows into the appropriate side files / annotations layer:

  add_event       -> appended to annotations.yaml via a new
                     `data/triage_events.csv` (acts like a hand-curated
                     event list, merged by merge_calendar_triage.py)
  add_to_context  -> appended to `data/per_day_extra_context.csv`
  mark_dip        -> appended to `data/sub_threshold_dips.csv`
  refine_tags     -> appended to `data/v2_tag_refinements_queue.csv`

All side files are idempotent: rerunning replaces entries for the same
date+source-tag rather than duplicating them.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

import sys

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

# Optional CLI argument: a year, defaults to plain triage_notes_classified.csv.
# Supports per-year files like triage_notes_classified_2025.csv.
_year_arg = next((a for a in sys.argv[1:] if a.isdigit() and len(a) == 4), None)
if _year_arg:
    INPUT = DATA / f"triage_notes_classified_{_year_arg}.csv"
else:
    INPUT = DATA / "triage_notes_classified.csv"

TRIAGE_EVENTS_CSV = DATA / "triage_events.csv"
PER_DAY_CONTEXT_CSV = DATA / "per_day_extra_context.csv"
SUB_THRESHOLD_DIPS_CSV = DATA / "sub_threshold_dips.csv"
V2_REFINEMENTS_CSV = DATA / "v2_tag_refinements_queue.csv"


# Regex patterns to auto-detect action when the user wrote it inline
# in the triage note (rather than using the action_to_take column).
ACTION_INLINE_PATTERNS = [
    (re.compile(r"\b(add[_\s]events?|add\s+as\s+events?|event\s+for\s+the\s+day"
                r"|add\s+devent|add\s+evet|add\s+\w+\s+day\s+event"
                r"|add\s+multi.?day\s+event)\b", re.IGNORECASE),
     "add_event"),
    (re.compile(r"\b(mark\s+as\s+dip|self.?reported\s+dip|dip\s+above\s+treshold"
                r"|dip\s+above\s+threshold|despite\s+the\s+\d.*dip|probably\s+a\s+dip"
                r"|in\s+a\s+dip|definitely\s+a\s+dip|is\s+a\s+dip"
                r"|dip\s+day|add\s+(?:pre\s+)?dip\b|^\s*dip\s*$)\b", re.IGNORECASE),
     "mark_dip"),
    (re.compile(r"\b(add\s+(?:a\s+)?tag|should\s+be\s+labeled\s+as|add\s+\w+\s+tag\s+for"
                r"|need\s+to\s+tag|tag\s+\w+\s+for\s+this\s+day"
                r"|add\s+to\s+symptoms?|add\s+as\s+symptom|is\s+brainfog"
                r"|is\s+pacing(\s+actie)?|symptom\s+nachtzweten)\b", re.IGNORECASE),
     "refine_tags"),
    (re.compile(r"\b(add\s+context\s+notes?|add\s+as\s+context|add\s+notes?\b|^\s*notes?:)\b", re.IGNORECASE),
     "add_to_context"),
    (re.compile(r"\b(no\s+(?:specific\s+)?loads?\s+needed|no\s+sepecific\s+loads"
                r"|triaged\s+no\s+loads)\b", re.IGNORECASE),
     "none"),
]


def detect_inline_action(triage_note: str) -> str:
    """Returns the action string if the user wrote it inline in the triage note,
    or empty string if no pattern matched."""
    s = (triage_note or "").lower()
    for pat, action in ACTION_INLINE_PATTERNS:
        if pat.search(s):
            return action
    return ""


def strip_action_prefix(triage_note: str, action: str) -> str:
    """For add_event rows, the triage note is typically 'add_event <label text>'.
    Strip the action keyword to get a clean event label."""
    if action != "add_event":
        return triage_note
    s = re.sub(
        r"^\s*(add[_\s]events?|add\s+as\s+events?|add\s+devent|add\s+evet"
        r"|add\s+multi.?day\s+event|add\s+\w+\s+day\s+event)[\s:,-]*",
        "", triage_note, flags=re.IGNORECASE)
    s = re.sub(r"\s+event\s+for\s+the\s+day\s*", "", s, flags=re.IGNORECASE)
    return s.strip()


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


def label_from_triage(triage: str, fallback: str = "untitled") -> str:
    """Derive a short event label from a triage note."""
    s = clean(triage)
    # Drop common boilerplate trailing notes
    s = re.sub(r"\b(one\s+day\s+event|add\s+to\s+events|event\s+for\s+the\s+day)\b",
               "", s, flags=re.IGNORECASE)
    s = clean(s)
    # Truncate to a useful event-label length
    if len(s) > 60:
        s = s[:60].rsplit(" ", 1)[0] + "..."
    return s.strip(".,;:") or fallback


def read_existing(path: Path, date_col: str = "date",
                  label_col: str | None = None) -> dict:
    """Returns existing-rows index (if file exists).

    `date_col` is the column to read the date from. When `label_col` is given,
    the key becomes (date, label) so multiple events on the same day can coexist
    (e.g. triage_events.csv 2025-04-30 has both 'sailing with jantine' AND
    'tijmen logeren' AND 'tobias in parijs'). Otherwise key is the bare date.
    """
    if not path.exists():
        return {}
    out: dict = {}
    for r in csv.DictReader(path.open(encoding="utf-8")):
        d = r.get(date_col, "")
        if not d:
            continue
        if label_col:
            out[(d, r.get(label_col, ""))] = r
        else:
            out[d] = r
    return out


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    sorted_rows = sorted(rows, key=lambda r: r.get("date", ""))
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in sorted_rows:
            w.writerow({k: r.get(k, "") for k in fields})


def main():
    if not INPUT.exists():
        print(f"ERROR: {INPUT} does not exist.")
        return 1

    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    buckets: dict[str, list[dict]] = {
        "add_event": [],
        "add_to_context": [],
        "mark_dip": [],
        "refine_tags": [],
    }
    inline_count = 0
    for r in rows:
        action = (r.get("action_to_take") or "").strip().lower()
        if action not in buckets:
            # Try to detect inline action from triage note text
            detected = detect_inline_action(r.get("triage_note", ""))
            if detected in buckets:
                action = detected
                # If add_event, strip the action prefix from the note so the label
                # is cleaner.
                if action == "add_event":
                    r["triage_note"] = strip_action_prefix(r["triage_note"], action)
                inline_count += 1
        if action in buckets:
            buckets[action].append(r)
    if inline_count:
        print(f"  (detected {inline_count} inline actions from triage notes)")

    # 1. add_event -> triage_events.csv (consumed by merge_calendar_triage.py)
    # Keyed by (date_start, label) so multiple events on the same date coexist
    # (manually-curated multi-day spans + auto-detected single events).
    event_fields = ["date_start", "date_end", "label", "category",
                    "cognitive_load", "physical_load", "emotional_load",
                    "source", "note"]
    existing_events = read_existing(TRIAGE_EVENTS_CSV, date_col="date_start",
                                    label_col="label")
    new_events: dict = {**existing_events}
    for r in buckets["add_event"]:
        d = r["date"]
        label = label_from_triage(r.get("triage_note", ""))
        c = (r.get("cog_load") or "").strip()
        p = (r.get("phy_load") or "").strip()
        e = (r.get("emo_load") or "").strip()
        any_load = any(x for x in (c, p, e))
        category = "high_intensity" if (c == "3" or p == "3" or e == "3") else \
                   "levensgebeurtenis" if any_load else "levensgebeurtenis"
        new_events[(d, label)] = {
            "date_start": d, "date_end": d, "label": label,
            "category": category,
            "cognitive_load": c, "physical_load": p, "emotional_load": e,
            "source": "triage_notes_classified",
            "note": clean(r.get("triage_note", "")),
        }
    triage_events_rows = list(new_events.values())
    write_csv(TRIAGE_EVENTS_CSV, triage_events_rows, event_fields)
    print(f"  add_event       : {len(buckets['add_event'])} new -> {TRIAGE_EVENTS_CSV.name} (total {len(triage_events_rows)})")

    # 2. add_to_context -> per_day_extra_context.csv
    ctx_fields = ["date", "score", "extra_context", "triage_loads", "source"]
    existing_ctx = read_existing(PER_DAY_CONTEXT_CSV)
    new_ctx: dict[str, dict] = {**existing_ctx}
    for r in buckets["add_to_context"]:
        d = r["date"]
        c = (r.get("cog_load") or "").strip()
        p = (r.get("phy_load") or "").strip()
        e = (r.get("emo_load") or "").strip()
        loads = f"c{c or '-'}/p{p or '-'}/e{e or '-'}"
        new_ctx[d] = {
            "date": d,
            "score": r.get("score", ""),
            "extra_context": clean(r.get("triage_note", "")),
            "triage_loads": loads,
            "source": "triage_notes_classified",
        }
    write_csv(PER_DAY_CONTEXT_CSV, list(new_ctx.values()), ctx_fields)
    print(f"  add_to_context  : {len(buckets['add_to_context'])} new -> {PER_DAY_CONTEXT_CSV.name} (total {len(new_ctx)})")

    # 3. mark_dip -> sub_threshold_dips.csv
    dip_fields = ["date", "score", "user_dip_note", "original_note", "source"]
    existing_dip = read_existing(SUB_THRESHOLD_DIPS_CSV)
    new_dip: dict[str, dict] = {**existing_dip}
    for r in buckets["mark_dip"]:
        d = r["date"]
        new_dip[d] = {
            "date": d,
            "score": r.get("score", ""),
            "user_dip_note": clean(r.get("triage_note", "")),
            "original_note": clean(r.get("original_note", "")),
            "source": "triage_notes_classified",
        }
    write_csv(SUB_THRESHOLD_DIPS_CSV, list(new_dip.values()), dip_fields)
    print(f"  mark_dip        : {len(buckets['mark_dip'])} new -> {SUB_THRESHOLD_DIPS_CSV.name} (total {len(new_dip)})")

    # 4. refine_tags -> v2_tag_refinements_queue.csv
    ref_fields = ["date", "issue", "triage_note", "original_note", "source"]
    existing_ref = read_existing(V2_REFINEMENTS_CSV)
    new_ref: dict[str, dict] = {**existing_ref}
    for r in buckets["refine_tags"]:
        d = r["date"]
        new_ref[d] = {
            "date": d,
            "issue": "v2 model needs additional/refined tag (see triage note)",
            "triage_note": clean(r.get("triage_note", "")),
            "original_note": clean(r.get("original_note", "")),
            "source": "triage_notes_classified",
        }
    write_csv(V2_REFINEMENTS_CSV, list(new_ref.values()), ref_fields)
    print(f"  refine_tags     : {len(buckets['refine_tags'])} new -> {V2_REFINEMENTS_CSV.name} (total {len(new_ref)})")


if __name__ == "__main__":
    raise SystemExit(main())
