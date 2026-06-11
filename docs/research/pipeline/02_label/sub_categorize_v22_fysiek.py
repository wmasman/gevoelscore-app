"""v2.2 sub-categorisation of symptoom_fysiek clauses.

Reads:  notes-categorized-v2-clauses.csv (locked v2 output)
Writes: notes-categorized-v22-clauses.csv (v2 output + new symptoom_fysiek_subtype column)

Multi-tag: a clause can carry multiple sub-types
(e.g. "hoofdpijn en moe" -> hoofdpijn;systemisch_vermoeid).

The v2 dictionary stays locked. This is a downstream refinement.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "notes-categorized-v2-clauses.csv"
OUTPUT = HERE / "notes-categorized-v22-clauses.csv"

# Sub-category phrase lists. Substring matching on lowercased clause.
# Order matters slightly: more specific patterns first, then generic.
SUB_FYSIEK_PATTERNS = {
    "hoofdpijn": [
        "hoofdpijn", "migraine", "pijn in mijn hoofd", "hoofd doet pijn",
    ],
    "spier": [
        "spierpijn", "zware benen", "zere benen", "benen zwaar",
        "in mijn lijf", "zwaar in de benen", "stijfheid", "stramme spieren",
        "spieren pijn", "zwaar lichaam", "stijf",
        # v2.2-patch4: tintelende benen moved from neuro (user feedback)
        "tintelende benen", "tintelend gevoel",
    ],
    "keel_respiratoir": [
        "keelpijn", "verkouden", "hoesten", "loopneus", "snot",
        "snotneus", "snotterig", "snotterige", "koortslip", "keel",
    ],
    "koorts": [
        "koorts", "koortsig",
    ],
    "gastro": [
        "misselijk", "misselijkheid", "braken", "overgeven", "kotsen",
        "maagpijn", "maag van streek", "buikpijn", "opgeblazen buik",
    ],
    "huid": [
        "jeuk", "jeukt", "jeuken",
    ],
    # v2.2-patch4 (2026-06-11): tintelende benen moved from neuro to spier
    # (user feedback: it's a limb sensation, fits muscle/limb cluster better)
    "neuro": [
        "duizelig", "duizeligheid",
    ],
    "spier_extra_neuro_moved": [],  # placeholder for clarity
    # systemisch_vermoeid: v2.2-patch2 (2026-06-11): all sleep phrases moved
    # OUT of this bucket — sleep ≠ daytime fatigue per user review.
    "systemisch_vermoeid": [
        "moe", "uitgeput", "kapot", "gesloopt", "slap", "zwakte",
        "weinig energie", "geen energie",
    ],
    # slaap: v2.2-patch2 also adds "goed geslapen" / "diep geslapen" / etc.
    # so positive sleep mentions fire slaap (not systemisch_vermoeid).
    "slaap": [
        "slecht geslapen", "goed geslapen", "diep geslapen", "heerlijk geslapen",
        "matige nacht", "matig geslapen", "matige slaap",
        "onrustig geslapen", "wakker geweest", "veel wakker",
        "slecht in slaap", "laat in slaap", "moeilijk in slaap",
        "veel hoofdpijn vannacht", "vannacht onrustig",
        "opstaan valt niet mee", "vroeger opstaan", "vroeg opstaan",
        "moeite met opstaan", "ochtendroutine",
    ],
    # General body / energy descriptors — caught only if no other sub matches
    "generiek_lijf": [
        "lijf", "fit", "energie",  # very generic; polarity layer disambiguates
    ],
}


def classify_clause(clause: str) -> list[str]:
    """Return list of sub-types that match the clause."""
    s = (clause or "").lower()
    hits = []
    for sub, patterns in SUB_FYSIEK_PATTERNS.items():
        for p in patterns:
            if p in s:
                hits.append(sub)
                break  # don't add same sub multiple times
    # If only generiek_lijf hit and nothing specific, demote it to overig
    if hits == ["generiek_lijf"]:
        return ["overig"]
    # If both generiek and something specific, drop the generic
    if "generiek_lijf" in hits and len(hits) > 1:
        hits = [h for h in hits if h != "generiek_lijf"]
    if not hits:
        return ["overig"]
    return hits


def main():
    if not INPUT.exists():
        print(f"ERROR: {INPUT} does not exist.")
        return 1

    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    print(f"Input: {len(rows)} clauses")

    out = []
    from collections import Counter
    sub_counter = Counter()
    sub_per_clause_counter = Counter()

    for r in rows:
        categories = (r.get("categories") or "")
        clause = r.get("clause") or ""
        sub_types = ""
        if "symptoom_fysiek" in categories:
            subs = classify_clause(clause)
            sub_types = ";".join(subs)
            sub_per_clause_counter[len(subs)] += 1
            for s in subs:
                sub_counter[s] += 1
        out.append({
            **r,
            "symptoom_fysiek_subtype": sub_types,
        })

    fields = list(rows[0].keys()) + ["symptoom_fysiek_subtype"]
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in out:
            w.writerow(r)

    print(f"\nWrote {OUTPUT}")
    print()
    print("Sub-category distribution (over symptoom_fysiek clauses):")
    for k, n in sub_counter.most_common():
        print(f"  {k}: {n}")
    print()
    print("Sub-tags per clause (multi-tag distribution):")
    for k in sorted(sub_per_clause_counter.keys()):
        print(f"  {k} tag(s): {sub_per_clause_counter[k]} clauses")


if __name__ == "__main__":
    raise SystemExit(main())
