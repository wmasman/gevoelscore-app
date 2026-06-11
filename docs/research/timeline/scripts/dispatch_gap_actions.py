"""Dispatch gap-review actions from the filled review CSV.

Reads:  data/pwc_dossier_review_filled.csv  (user-filled gap review)
Writes (idempotent upserts) to:
  - data/sub_threshold_dips.csv     (for mark_dip actions)
  - data/triage_events.csv          (for add_event actions)
  - data/per_day_intensity.csv      (for add_cog_load:N actions)
Audit log:
  - data/dispatch_gap_actions.log   (one line per row: what was done)

The user filled `action_to_take` with `accept` (= use prescriptive default
for this gap_type) or one of the explicit vocabulary terms. This script
interprets each.

Prescriptive defaults (when action_to_take = 'accept'):
  illness_stretch + overlap=full  -> skip  (already covered in research labels)
  illness_stretch + overlap=partial -> mark_dip on the lowest-score day
  doctor_visit_missing            -> add_event category=medical
  work_heavy_no_load              -> add_cog_load auto-bin (4-5h=2, 5+h=3)
                                     + skip if pwc_note has 'vakantie' / 'vrij'
"""
from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

INPUT = DATA / "pwc_dossier_review_filled.csv"
SUB_DIPS = DATA / "sub_threshold_dips.csv"
TRIAGE_EVENTS = DATA / "triage_events.csv"
PER_DAY_INTENSITY = DATA / "per_day_intensity.csv"
REINTEG_HOURS = DATA / "reintegration_hours_2022-2024.csv"
AUDIT_LOG = DATA / "dispatch_gap_actions.log"

SOURCE_TAG = "pwc_cross_validation_2026-06-11"


def parse_iso(s):
    if not s:
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def parse_float(s):
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def read_csv(path: Path, key_field: str | tuple = "date") -> dict:
    """Load existing entries indexed by key (date string or tuple of fields)."""
    if not path.exists():
        return {}
    out = {}
    for r in csv.DictReader(path.open(encoding="utf-8")):
        if isinstance(key_field, tuple):
            k = tuple(r.get(f, "") for f in key_field)
        else:
            k = r.get(key_field, "")
        if any(k) if isinstance(k, tuple) else k:
            out[k] = r
    return out


def write_csv(path: Path, rows: list[dict], fields: list[str], date_key: str = "date"):
    sorted_rows = sorted(rows, key=lambda r: r.get(date_key, ""))
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in sorted_rows:
            w.writerow({k: r.get(k, "") for k in fields})


def auto_bin_cog_load(total_hours: float, pwc_note: str) -> str:
    """Returns '1'/'2'/'3' or '' (skip) based on hours + content."""
    note_lower = (pwc_note or "").lower()
    if any(kw in note_lower for kw in ("vakantie", "vrij", "kerstvakantie", "herfstvakantie")):
        return ""  # skip
    if total_hours >= 5:
        return "3"
    if total_hours >= 4:
        return "2"
    return "1"


def parse_action(action_raw: str, gap_type: str, row: dict) -> list[tuple[str, dict]]:
    """Returns list of (action_kind, action_args_dict).

    User wrote actions in the `notes` column in informal text. We parse it.
    A single row can yield MULTIPLE actions (compound: add_event + add_cog_load).

    action_kind: 'skip', 'mark_dip', 'add_event', 'add_cog_load', 'add_phy_load'
    action_args: {'value': '1'/'2'/'3', 'label': '...'} as applicable
    """
    raw = (row.get("notes") or "").strip().lower()
    if not raw:
        # Fallback to action_to_take column if notes is empty
        raw = (action_raw or "").strip().lower()

    if not raw or raw == "accept":
        return [("skip", {})]
    if raw == "skip":
        return [("skip", {})]

    actions = []

    # mark_dip
    if re.search(r"\bmark[_\s]?dip\b", raw):
        actions.append(("mark_dip", {}))

    # add_event with label hint
    m = re.search(r"add\s+event\s+(.+?)(?:also\s|$)", raw)
    if m:
        label = m.group(1).strip().rstrip(",.")
        actions.append(("add_event", {"label": label, "category": "medical"}))

    # "make this a to amsterdam ... reintegratie event" — special compound
    if re.search(r"to\s+amsterdam.*reintegrat", raw):
        actions.append(("add_event", {
            "label": "naar amsterdam PwC reintegratie",
            "category": "levensgebeurtenis",
        }))

    # add_cog_load N
    m = re.search(r"add\s*cog\s*load\s*[:=]?\s*([123])", raw)
    if m:
        actions.append(("add_cog_load", {"value": m.group(1)}))

    # add_phy_load N (compound rows)
    m = re.search(r"phy\w*\s*load\s*[:=]?\s*([123])", raw)
    if m:
        actions.append(("add_phy_load", {"value": m.group(1)}))

    if not actions:
        return [("skip", {})]
    return actions


def find_lowest_score_day_in_stretch(date_start: date, date_end: date,
                                      scores: dict[date, int]) -> date:
    """Pick the day with the lowest score in the stretch for mark_dip."""
    best_day = date_start
    best_score = scores.get(date_start, 99)
    d = date_start
    from datetime import timedelta
    while d <= date_end:
        s = scores.get(d, 99)
        if s < best_score:
            best_score = s
            best_day = d
        d += timedelta(days=1)
    return best_day


def load_scores() -> dict[date, int]:
    out: dict[date, int] = {}
    p = HERE.parent.parent / "garmin" / "hypotheses" / "crash_v2-definition" / "labels_crash_v2.csv"
    if not p.exists():
        return out
    for r in csv.DictReader(p.open(encoding="utf-8")):
        d = parse_iso(r.get("date"))
        s = r.get("score")
        if d and s and s != "None":
            try:
                out[d] = int(s)
            except ValueError:
                pass
    return out


def main():
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    scores = load_scores()
    audit_lines = []

    # Load existing files
    existing_dips = read_csv(SUB_DIPS, key_field="date")
    existing_events = read_csv(TRIAGE_EVENTS, key_field=("date_start", "label"))
    existing_intensity = read_csv(PER_DAY_INTENSITY, key_field="date")

    # Load PwC notes for label generation
    pwc_notes = {}
    if REINTEG_HOURS.exists():
        for r in csv.DictReader(REINTEG_HOURS.open(encoding="utf-8")):
            d = parse_iso(r.get("date"))
            if d:
                pwc_notes[d] = r.get("toelichting", "")

    counts = {"skip": 0, "mark_dip": 0, "add_event": 0,
              "add_cog_load": 0, "add_phy_load": 0}

    for r in rows:
        gt = r.get("gap_type", "")
        d_start = parse_iso(r.get("date_start"))
        d_end = parse_iso(r.get("date_end")) or d_start
        if d_start is None:
            audit_lines.append(f"skip (invalid date): {r}")
            continue

        actions = parse_action(r.get("action_to_take", ""), gt, r)
        for action, args in actions:
            counts[action] = counts.get(action, 0) + 1

            if action == "skip":
                audit_lines.append(f"{d_start.isoformat()} {gt}: skip (notes: {r.get('notes','')[:50]})")
                continue

            if action == "mark_dip":
                best = find_lowest_score_day_in_stretch(d_start, d_end, scores)
                existing_dips[best.isoformat()] = {
                    "date": best.isoformat(),
                    "score": str(scores.get(best, "")),
                    "user_dip_note": f"Illness stretch {d_start.isoformat()} -> {d_end.isoformat()} from PwC log",
                    "original_note": pwc_notes.get(best, ""),
                    "source": SOURCE_TAG,
                }
                audit_lines.append(f"{best.isoformat()} mark_dip (from stretch {d_start} -> {d_end})")
                continue

            if action == "add_event":
                label = args.get("label", "").strip()
                if not label:
                    label = r.get("context", "")[:60].strip(". ")
                category = args.get("category", "medical")
                existing_events[(d_start.isoformat(), label)] = {
                    "date_start": d_start.isoformat(),
                    "date_end": d_start.isoformat(),
                    "label": label,
                    "category": category,
                    "cognitive_load": "",
                    "physical_load": "",
                    "emotional_load": "",
                    "source": SOURCE_TAG,
                    "note": pwc_notes.get(d_start, ""),
                }
                audit_lines.append(f"{d_start.isoformat()} add_event [{category}]: {label}")
                continue

            if action in ("add_cog_load", "add_phy_load"):
                load_col = "cog" if action == "add_cog_load" else "phy"
                value = args.get("value", "")
                existing_entry = existing_intensity.get(d_start.isoformat(), {})
                # Don't overwrite an existing value for that axis
                if existing_entry.get(load_col):
                    audit_lines.append(f"{d_start.isoformat()} {action}:{value} SKIPPED (existing {load_col}={existing_entry.get(load_col)})")
                    continue
                merged = dict(existing_entry)
                merged.update({
                    "date": d_start.isoformat(),
                    load_col: value,
                    "source": SOURCE_TAG,
                })
                merged["notes"] = (existing_entry.get("notes") or "") + \
                    (" | " if existing_entry.get("notes") else "") + \
                    f"PwC-cross-val: {load_col}={value}"
                existing_intensity[d_start.isoformat()] = merged
                audit_lines.append(f"{d_start.isoformat()} {action}:{value}")
                continue

    # Write back
    write_csv(SUB_DIPS, list(existing_dips.values()),
              ["date", "score", "user_dip_note", "original_note", "source"])
    write_csv(TRIAGE_EVENTS, list(existing_events.values()),
              ["date_start", "date_end", "label", "category",
               "cognitive_load", "physical_load", "emotional_load",
               "source", "note"], date_key="date_start")
    write_csv(PER_DAY_INTENSITY, list(existing_intensity.values()),
              ["date", "cog", "phy", "emo", "source", "notes"])

    # Write audit log
    with AUDIT_LOG.open("w", encoding="utf-8") as f:
        f.write("\n".join(audit_lines))

    # Summary
    print(f"Dispatched {len(rows)} rows:")
    for k, n in counts.items():
        print(f"  {k}: {n}")
    print(f"\nFiles updated:")
    print(f"  sub_threshold_dips.csv: {len(existing_dips)} total")
    print(f"  triage_events.csv: {len(existing_events)} total")
    print(f"  per_day_intensity.csv: {len(existing_intensity)} total")
    print(f"\nAudit log: {AUDIT_LOG}")


if __name__ == "__main__":
    raise SystemExit(main())
