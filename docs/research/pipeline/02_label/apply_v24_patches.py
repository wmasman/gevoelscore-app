"""v2.4 — apply researcher-feedback patches 5, 6, 7 to v2.3 output.

Reads:  notes-categorized-v23-clauses.csv
Writes: notes-categorized-v24-clauses.csv

Patches applied:

  Patch 5 — Recovery_actie phrase expansion (pacing = recovery_actie).
    User confirmed recovery_actie IS the pacing category. Researcher
    review surfaced clauses currently mis-classified as symptoom_fysiek
    that are forward-looking pacing strategies. Solution: scan each
    clause for additional Dutch pacing phrases that v2 dictionary
    missed, and add the recovery_actie tag (multi-tag with whatever else
    matched).

    Added phrases: "energie sparen", "rustdag", "om energie te hebben",
    "te sparen voor", "energie proberen te sparen", "wat geslapen",
    "uur geslapen", "even geslapen", "om dat ik".

    These are added as a *new* category match, not a re-classification.
    The original symptoom_fysiek tag stays (because "energie" was the
    trigger, and that's still a body-related word) — the multi-tag
    correctly says "this clause is about pacing AND about energy".

  Patch 6 — Demote "redelijk" alone from positive to neutral.
    Researcher review (3 vermeldingen): "redelijk is neutral in this
    case". v2 dictionary has "redelijk" in polarity_positive. This patch
    re-evaluates polarity for clauses where polarity=positive AND the
    only positive-trigger appears to be a bare "redelijk" (not
    "redelijk goed" / "redelijk fijn" etc.) — demote to neutral.

  Patch 7 — Post-symptom negation ("X is over", "X weg", "geen X meer").
    The 3-word-before-symptom window misses Dutch patterns where the
    negation comes AFTER the symptom phrase. Patch scans the 3 words
    AFTER each symptom phrase in the clause; if it finds "is over",
    "is weg", "verdwenen", "is voorbij", "geen X meer" — set state to
    absent for that symptom.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "notes-categorized-v23-clauses.csv"
OUTPUT = HERE / "notes-categorized-v24-clauses.csv"

# Patch 5 — present-tense rest-actions only (researcher correction 2026-06-11:
# forward-looking phrases like "energie sparen" / "om donderdag" are NEUTRAL
# notes, NOT recovery_actie. Only past/present-tense actions where rest was
# actually TAKEN belong in recovery_actie).
RECOVERY_PATCH5 = re.compile(
    r"\b(rustdag|rust\s+dag"
    r"|wat\s+geslapen|uur\s+geslapen|even\s+geslapen|nog\s+wel\s+\w+\s+geslapen)\b",
    re.IGNORECASE,
)

# Phrases that LOOK like pacing but are forward-looking intentions /
# strategy talk. Captured for traceability but NOT routed to recovery_actie.
# May become their own neutral sub-category later if descriptive analysis
# warrants. Per user 2026-06-11: "forward-looking pacing is not pacing,
# it is a neutral note probably related to having overdone it and thus,
# wanting to pace / recover actively in the coming days".
NEUTRAL_FORWARD_LOOKING = re.compile(
    r"\b(energie\s+sparen|energie\s+proberen\s+te\s+sparen"
    r"|om\s+energie\s+te\s+hebben|te\s+sparen\s+voor"
    r"|om\s+morgen|om\s+volgende\s+week|om\s+\w+dag)\b",
    re.IGNORECASE,
)

# Patch 6 — "redelijk" alone vs in a compound positive phrase
REDELIJK_COMPOUND_POSITIVE = re.compile(
    r"\bredelijk\s+(goed|fijn|fit|prima|top|heerlijk|beter)\b", re.IGNORECASE,
)
REDELIJK_BARE = re.compile(r"\bredelijk\b", re.IGNORECASE)

# Patch 6 — other positive markers v2 may have used (to confirm there's
# another reason for polarity=positive)
OTHER_POSITIVE_MARKERS = re.compile(
    r"\b(leuk|fijn|gezellig|mooi|heerlijk|geweldig|prima|top|super|"
    r"beter|opgeknapt|goed\s+gesprek|goed\s+gedaan|mooi\s+gedaan|"
    r"helemaal\s+goed|heel\s+goed|beter\s+dan\s+verwacht)\b",
    re.IGNORECASE,
)

# Patch 7 — post-symptom negation markers
POST_SYMPTOM_NEGATION = re.compile(
    r"\b(is\s+over|was\s+over|is\s+weg|was\s+weg|verdwenen|"
    r"is\s+voorbij|niet\s+meer|geen\s+\w+\s+meer|nog\s+geen)\b",
    re.IGNORECASE,
)

# Symptom phrase prefixes to look for (per v2 dict)
SYMPTOM_PREFIXES = re.compile(
    r"\b(hoofdpijn|keelpijn|spierpijn|migraine|koorts|verkouden|"
    r"hoesten|loopneus|moe|uitgeput|kapot|misselijk|duizelig|"
    r"jeuk|snot)\b",
    re.IGNORECASE,
)


def patch5_recovery_pacing(row: dict) -> dict:
    """Two-part patch (researcher correction 2026-06-11):

    A. RECOVERY_PATCH5 (present-tense rest-actions taken) -> add recovery_actie tag.
    B. NEUTRAL_FORWARD_LOOKING (intention / strategy talk) -> flag with
       neutral_forward_looking=y for later descriptive analysis (e.g.
       "is this language predictive of post-overdone-it crashes?"), but
       do NOT tag as recovery_actie.
    """
    clause = row.get("clause") or ""
    cats = row.get("categories") or ""
    patches = []

    # Part A — actual rest taken
    if RECOVERY_PATCH5.search(clause) and "recovery_actie" not in cats:
        if cats and cats != "context_neutraal":
            cats = cats + "|recovery_actie"
        else:
            cats = "recovery_actie"
        patches.append("patch5a_rest_taken")

    # Part B — flag forward-looking intention without retagging
    neutral_flag = "y" if NEUTRAL_FORWARD_LOOKING.search(clause) else ""
    if neutral_flag:
        patches.append("patch5b_forward_looking_flag")

    if not patches:
        return row

    new = {**row}
    new["categories"] = cats
    if neutral_flag:
        new["neutral_forward_looking"] = neutral_flag
    new["_v24_patch_applied"] = (row.get("_v24_patch_applied", "") + ";" + ";".join(patches)).strip(";")
    return new


def patch6_redelijk_demote(row: dict) -> dict:
    """If polarity=positive and the only positive marker is bare 'redelijk',
    demote polarity to neutral."""
    clause = row.get("clause") or ""
    polarity = row.get("polarity") or ""
    if polarity != "positive":
        return row
    if not REDELIJK_BARE.search(clause):
        return row
    # If a compound positive ("redelijk goed") matches, it's a real positive — keep
    if REDELIJK_COMPOUND_POSITIVE.search(clause):
        return row
    # If any other positive marker exists in the clause, the positive label has
    # another source — keep it
    if OTHER_POSITIVE_MARKERS.search(clause):
        return row
    # Otherwise: the bare "redelijk" was the only trigger — demote to neutral
    return {
        **row,
        "polarity": "neutral",
        "_v24_patch_applied": (row.get("_v24_patch_applied", "") + ";patch6_redelijk_neutral").strip(";"),
    }


def patch7_post_symptom_negation(row: dict) -> dict:
    """Scan for symptom phrases followed by post-negation; if found, set
    symptom_states for that family to absent."""
    clause = row.get("clause") or ""
    sym_states = row.get("symptom_states") or ""
    if not sym_states:
        return row
    # Tokenize symptom mentions in the clause
    tokens = list(SYMPTOM_PREFIXES.finditer(clause))
    if not tokens:
        return row
    # For each symptom occurrence, check if a post-negation pattern appears
    # within ~4 words after it (Dutch "X is over" / "X is weg" etc.).
    cl_lower = clause.lower()
    has_post_negation = False
    for m in tokens:
        end = m.end()
        # Look at the next ~30 chars (roughly 4 words)
        window = cl_lower[end:end + 35]
        if POST_SYMPTOM_NEGATION.search(window):
            has_post_negation = True
            break
    if not has_post_negation:
        return row
    # Set states for symptom families to absent
    new_states = []
    changed = False
    for token in sym_states.split(";"):
        token = token.strip()
        if not token:
            continue
        if "=" in token:
            sym, state = token.split("=", 1)
            if sym.startswith("symptoom_") and state in ("present", "mild", "severe"):
                new_states.append(f"{sym}=absent")
                changed = True
            else:
                new_states.append(token)
        else:
            new_states.append(token)
    if not changed:
        return row
    return {
        **row,
        "symptom_states": ";".join(new_states),
        "_v24_patch_applied": (row.get("_v24_patch_applied", "") + ";patch7_post_negation").strip(";"),
    }


def main():
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    print(f"Input: {len(rows)} clauses")

    n_p5a = n_p5b = n_p6 = n_p7 = 0
    out = []
    for r in rows:
        r = dict(r)
        r.setdefault("_v24_patch_applied", "")
        r.setdefault("neutral_forward_looking", "")
        before_cats = r.get("categories", "")
        before_polarity = r.get("polarity", "")
        before_states = r.get("symptom_states", "")
        before_neutral = r.get("neutral_forward_looking", "")

        r = patch5_recovery_pacing(r)
        if r.get("categories", "") != before_cats:
            n_p5a += 1
        if r.get("neutral_forward_looking", "") != before_neutral:
            n_p5b += 1

        r = patch6_redelijk_demote(r)
        if r.get("polarity", "") != before_polarity:
            n_p6 += 1

        r = patch7_post_symptom_negation(r)
        if r.get("symptom_states", "") != before_states:
            n_p7 += 1

        out.append(r)

    fields = list(rows[0].keys())
    if "_v24_patch_applied" not in fields:
        fields.append("_v24_patch_applied")
    if "neutral_forward_looking" not in fields:
        fields.append("neutral_forward_looking")
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in out:
            w.writerow({k: r.get(k, "") for k in fields})

    print(f"\nWrote {OUTPUT}")
    print(f"  Patch 5a (recovery_actie added for actual rest taken): {n_p5a} clauses")
    print(f"  Patch 5b (neutral_forward_looking flagged):            {n_p5b} clauses")
    print(f"  Patch 6 ('redelijk' polarity demoted to neutral):      {n_p6} clauses")
    print(f"  Patch 7 (post-symptom negation -> state=absent):       {n_p7} clauses")


if __name__ == "__main__":
    raise SystemExit(main())
