"""Extract notes-based candidates for triage into annotations.

Reads day_entries_with_notes.json and produces three topic-targeted CSVs:
  - notes_medical_triage.csv         medical milestones (huisarts, specialist, meds, etc.)
  - notes_overload_triage.csv        heavy-exhaustion / overload days
  - notes_events_triage.csv          non-calendar events (wedstrijden, reizen, deadlines)

CSV structure (similar to calendar_*_triage.csv):
  date_start (= note date), date_end (= note date by default; user can change),
  score (the gevoelscore on that day, read-only context),
  note_full (the full note text, read-only context),
  matched_keyword (which keyword triggered the match),
  keep_yn (user fills),
  event_label (user fills if y),
  category (user fills if y: high_intensity / interventie / levensgebeurtenis / medical),
  cognitive_load / physical_load / emotional_load (user fills),
  notes (user adds context)

Re-running is safe: it overwrites the CSVs (but only if no triage data exists;
if keep_yn columns are non-empty, the user has triaged, and we refuse to overwrite).
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMELINE_ROOT = HERE.parent
DATA = TIMELINE_ROOT / "data"
RESEARCH_ROOT = TIMELINE_ROOT.parent
NOTES_JSON = RESEARCH_ROOT / "notes" / "01-language-around-crashes" / "day_entries_with_notes.json"

OUT_MEDICAL = DATA / "notes_medical_triage.csv"
OUT_OVERLOAD = DATA / "notes_overload_triage.csv"
OUT_EVENTS = DATA / "notes_events_triage.csv"


# Keyword sets (Dutch; case-insensitive; word-boundary aware).
TOPIC_KEYWORDS = {
    "medical": [
        # Medical institutions
        r"huisart", r"specialist", r"ziekenhuis", r"polikliniek",
        # Procedures / tests
        r"diagnose", r"\bmri\b", r"\bct[- ]scan", r"echo\b", r"bloedprik",
        r"x-ray", r"r[oö]ntgen",
        # Medications (extending citalopram coverage)
        r"\bssri", r"naproxen", r"paracetamol", r"ibuprofen", r"melatonine",
        r"magnesium", r"medicat", r"tabletje", r"druppel",
        # Practitioners (excluding things already covered by ergo/fysio calendar pins)
        r"\barts\b", r"\bdokter", r"cardio", r"neuro\b", r"endocrino",
        r"poh-ggz", r"psycholoog", r"psychiater",
        # LC-specific
        r"c-support", r"long covid", r"lc\b",
        # Cpap / apneu (we already have a span but more mentions may indicate followups)
        r"\bcpap", r"apneu", r"masker",
        # Mental health / breath / interventions on body
        r"breinvoeding", r"coherence", r"ademhal", r"hrv-coach",
        # Vaccinations
        r"vaccinatie", r"prik\b", r"booster",
    ],
    "overload": [
        # Direct exhaustion
        r"\bkapot\b", r"uitgeput", r"\bleeg\b", r"te veel",
        r"overprikkel", r"overload", r"overdaan",
        r"overweldig", r"opgebrand",
        # Crash / dip language (note: this may overlap with research labels)
        r"instort", r"ineen.*gezakt", r"\bcrash\b", r"\bdip\b",
        r"pem\b", r"post.?exertion",
        # End-of-day exhaustion patterns
        r"einde dag.*moe", r"helemaal eraan", r"helemaal.*kapot",
        r"helemaal.*klaar",
        # Energy-specific
        r"geen energie", r"weinig energie",
    ],
    "events": [
        # Work / professional
        r"wedstrijd", r"examen", r"presentatie", r"audit",
        r"deadline", r"keynote", r"interview", r"sollicit",
        r"\bborrel\b", r"diner", r"feestje",  # social events not covered by calendar
        # Life events
        r"sterf", r"begrafenis", r"overlijden", r"crematie",
        r"bruiloft", r"huwelijk", r"verlov",
        r"geboorte", r"baby\b", r"bevallen",
        # Travel
        r"vliegtuig", r"vlucht\b", r"paspoort",
        r"hotel\b", r"geboekt", r"vakantie",
        r"reisje", r"\btrip\b", r"vertrokken",
        r"\bweekend\b",  # generic, but useful when paired with location
        # Specific intense activity
        r"hardlopen", r"fietsen.*km", r"\d+\s?km",  # cycling/running mentions
        r"klimm", r"zwem.*wedstrijd",
    ],
}


def has_any_match(text: str, patterns: list[str]) -> list[str]:
    """Return list of patterns that matched."""
    matched = []
    for p in patterns:
        try:
            if re.search(p, text, re.IGNORECASE):
                matched.append(p)
        except re.error:
            continue
    return matched


def load_notes() -> list[dict]:
    if not NOTES_JSON.exists():
        print(f"ERROR: notes JSON not found at {NOTES_JSON}", file=sys.stderr)
        sys.exit(1)
    return json.loads(NOTES_JSON.read_text(encoding="utf-8"))


def check_existing_csv(p: Path) -> int:
    """Returns number of triaged (non-empty keep_yn) rows in existing CSV, or -1 if file does not exist."""
    if not p.exists():
        return -1
    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    return sum(1 for r in rows if (r.get("keep_yn") or "").strip())


def write_csv(p: Path, rows: list[dict]):
    fields = [
        "date_start", "date_end", "score", "note_full",
        "matched_keyword",
        "keep_yn", "event_label", "category",
        "cognitive_load", "physical_load", "emotional_load", "notes",
    ]
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def main():
    force = "--force" in sys.argv
    notes = load_notes()
    print(f"Loaded {len(notes)} day_entries from notes export.")

    # Refuse to overwrite if user has already triaged
    for p in (OUT_MEDICAL, OUT_OVERLOAD, OUT_EVENTS):
        n_triaged = check_existing_csv(p)
        if n_triaged > 0 and not force:
            print(f"ERROR: {p.name} already has {n_triaged} triaged rows.", file=sys.stderr)
            print(f"  Rerun with --force to overwrite (your triage data will be LOST).",
                  file=sys.stderr)
            sys.exit(1)

    buckets: dict[str, list[dict]] = {topic: [] for topic in TOPIC_KEYWORDS}
    for entry in notes:
        note = entry.get("note") or ""
        if not note.strip():
            continue
        for topic, patterns in TOPIC_KEYWORDS.items():
            matched = has_any_match(note, patterns)
            if not matched:
                continue
            buckets[topic].append({
                "date_start": entry["date"],
                "date_end": entry["date"],  # default single-day; user can edit
                "score": entry.get("score", ""),
                "note_full": note.replace("\n", " ").strip(),
                "matched_keyword": ", ".join(matched[:5]),
                "keep_yn": "",
                "event_label": "",
                "category": "",
                "cognitive_load": "",
                "physical_load": "",
                "emotional_load": "",
                "notes": "",
            })

    print()
    out_map = {
        "medical": OUT_MEDICAL,
        "overload": OUT_OVERLOAD,
        "events": OUT_EVENTS,
    }
    for topic, rows in buckets.items():
        p = out_map[topic]
        write_csv(p, rows)
        print(f"  {topic:10}: {len(rows):4} candidates -> {p.name}")

    # Cross-topic overlap stats
    print()
    print("Cross-topic overlap (same date matched in multiple topics):")
    by_date: dict[str, set[str]] = {}
    for topic, rows in buckets.items():
        for r in rows:
            by_date.setdefault(r["date_start"], set()).add(topic)
    overlaps = {tuple(sorted(t)): 0 for t in [
        ("medical", "overload"),
        ("medical", "events"),
        ("overload", "events"),
        ("medical", "overload", "events"),
    ]}
    for d, topics in by_date.items():
        key = tuple(sorted(topics))
        if len(key) > 1 and key in overlaps:
            overlaps[key] += 1
    for key, n in overlaps.items():
        print(f"  {' + '.join(key):40} {n}")


if __name__ == "__main__":
    main()
