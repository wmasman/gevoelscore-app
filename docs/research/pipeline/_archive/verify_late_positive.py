"""Verify the v2 finding: 50% of late-era crash days are
polarity-positive-dominant. Pull the actual notes + clause breakdown
to distinguish the three plausible readings:
  1. Active reframing (writing about the good parts of a bad day)
  2. Crashes embedded in functional days with positive content around them
  3. Common positive words firing on neutral content (noise)
"""
from __future__ import annotations

import collections
import csv
import json
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLAUSE_CSV = HERE / "notes-categorized-v2-clauses.csv"
DAY_CSV = HERE / "notes-categorized-v2.csv"
NOTES_JSON = HERE.parent / "01-language-around-crashes" / "day_entries_with_notes.json"
OUT_MD = HERE / "verification-late-positive.md"

ERA_SPLIT = date(2023, 12, 31)


def main():
    # Load clauses
    clauses_by_day = collections.defaultdict(list)
    with CLAUSE_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            clauses_by_day[d].append(r)

    # Load day meta
    days = {}
    with DAY_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            days[d] = r

    full_notes = json.loads(NOTES_JSON.read_text(encoding="utf-8"))
    full_notes_by_day = {date.fromisoformat(e["date"]): e["note"].strip()
                         for e in full_notes if e.get("note") and e["note"].strip()}

    # Find LATE-era crash days, classify by the SAME rule the analysis used:
    # pos > neg (ignoring neutral). This is the rule that produced the 50% figure.
    # (The per-day CSV's day_dominant_polarity uses a stricter pos > neg AND pos > neu rule —
    # which is why filtering on that field returned 0 hits. Same script, two different
    # 'dominant' definitions — caught by this verify step, should be reconciled later.)
    late_crash_days = [d for d, r in days.items()
                       if r["in_crash"] == "True" and r["era"] == "late"]

    def loose_class(d):
        r = days[d]
        pos = int(r["n_pos_clauses"]); neg = int(r["n_neg_clauses"])
        if pos > neg: return "positive"
        if neg > pos: return "negative"
        return "tied"

    pos_dominant = [d for d in late_crash_days if loose_class(d) == "positive"]
    neg_dominant = [d for d in late_crash_days if loose_class(d) == "negative"]
    mixed = []  # not produced by the loose rule
    neutral = [d for d in late_crash_days if loose_class(d) == "tied"]

    print(f"late-era crash days: {len(late_crash_days)}")
    print(f"  positive-dominant: {len(pos_dominant)}")
    print(f"  negative-dominant: {len(neg_dominant)}")
    print(f"  mixed-dominant: {len(mixed)}")
    print(f"  neutral-dominant: {len(neutral)}")

    md = ["# Verification — what's behind the 50% positive-dominant late crashes?", ""]
    md.append("v2 found that 50% of late-era crash days end up polarity-positive-dominant (vs 11% early).")
    md.append("Three plausible readings:")
    md.append("1. **Reframing** — user writes about positive parts even on bad days")
    md.append("2. **Functional days with crash moments** — crash embedded in otherwise-okay context")
    md.append("3. **Noise** — common positive words ('goed', 'redelijk') firing on neutral content")
    md.append("")
    md.append(f"This script pulls every late-era positive-dominant crash day, full note + per-clause breakdown, so you can read which is true.")
    md.append("")
    md.append(f"## Counts")
    md.append("")
    md.append(f"- late-era crash days with note: **{len(late_crash_days)}**")
    md.append(f"- positive-dominant: **{len(pos_dominant)}**")
    md.append(f"- negative-dominant: **{len(neg_dominant)}**")
    md.append(f"- mixed-dominant: **{len(mixed)}**")
    md.append(f"- neutral-dominant: **{len(neutral)}**")
    md.append("")

    def show_day_block(md, d, label):
        meta = days[d]
        full = full_notes_by_day.get(d, "")
        md.append(f"### {d.isoformat()} ({label})")
        md.append(f"- score: **{meta['score']}**  |  state_symptoom_fysiek: **{meta.get('state_symptoom_fysiek', '?')}**")
        md.append(f"- clause polarity counts: positive={meta['n_pos_clauses']} | negative={meta['n_neg_clauses']} | mixed={meta['n_mixed_clauses']} | neutral={meta['n_neutral_clauses']}")
        md.append(f"- full note:")
        md.append(f"  > {full}")
        md.append("- clause breakdown:")
        for c in clauses_by_day[d]:
            pol = c["polarity"]
            cats = c["categories"]
            ss = c["symptom_states"]
            tag = ""
            if pol == "positive": tag = " ✚"
            elif pol == "negative": tag = " ✖"
            elif pol == "mixed": tag = " ⇆"
            md.append(f"    - [{pol}{tag}] _{c['clause']}_ — cats: `{cats}`" + (f"; states: `{ss}`" if ss else ""))
        md.append("")

    md.append("## All late-era positive-dominant crash days")
    md.append("")
    for d in sorted(pos_dominant):
        show_day_block(md, d, "positive-dominant")

    md.append("## All late-era negative-dominant crash days (for contrast)")
    md.append("")
    for d in sorted(neg_dominant):
        show_day_block(md, d, "negative-dominant")

    md.append("## All late-era mixed-dominant crash days (for contrast)")
    md.append("")
    for d in sorted(mixed):
        show_day_block(md, d, "mixed-dominant")

    md.append("## Sample of late-era neutral-dominant crash days (first 5, for contrast)")
    md.append("")
    for d in sorted(neutral)[:5]:
        show_day_block(md, d, "neutral-dominant")

    md.append("---")
    md.append("")
    md.append("## How to read this")
    md.append("")
    md.append("Look at each **positive-dominant** day. For each, ask:")
    md.append("")
    md.append("- Is the positive content describing a separate functional part of the day (reading 2)? E.g. 'leuk gesprek met [Naam]' on a day where the user was also lying down with hoofdpijn — both true, the day had a positive moment AND a crash.")
    md.append("- Is the positive content reframing the negative (reading 1)? E.g. 'wel een goede dag ondanks alles' or 'beter dan gisteren'.")
    md.append("- Is the positive content a noisy match on a common word with no real positive content (reading 3)? E.g. 'goed' or 'redelijk' appearing as a self-rating that's actually quite low.")
    md.append("")
    md.append("Counts of which reading fits each day, written by hand:")
    md.append("- _(fill in after reading)_")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
