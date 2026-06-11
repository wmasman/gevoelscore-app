"""v2.3 — apply researcher-feedback patches to v2.2 output.

Reads:  notes-categorized-v22-clauses.csv (after v2.2 patches 2+4 in
        sub_categorize_v22_fysiek.py)
Writes: notes-categorized-v23-clauses.csv

Patches applied here (the ones that need richer-than-dict logic):

  Patch 1 — Severity broadening.
    The v2 modifier window (3 words before symptom phrase) catches
    "heel erge hoofdpijn" via "heel erg(e)" but misses bare "erg moe",
    "heel moe", "fikse hoofdpijn". This patch re-evaluates state for
    symptoom_fysiek clauses by also matching ['erg', 'heel', 'fiks',
    'fikse'] within the same 3-word window. When matched, state is
    promoted to `severe`.

  Patch 3 — Energy countersignal.
    Phrases like "goede energie", "veel energie", "redelijk energie",
    "lekker fris" — currently fall into v2 `context_neutraal` or were
    sub-classified as `overig`. User feedback: these are positive
    counter-signals for systemisch_vermoeid; they belong as
    symptoom_fysiek with subtype=systemisch_vermoeid and state=absent.
    Polarity is set positive.

v2 file is NOT touched. v2.2 sub-classifier was updated separately for
patches 2 (slaap split) and 4 (tintelende benen → spier).
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "notes-categorized-v22-clauses.csv"
OUTPUT = HERE / "notes-categorized-v23-clauses.csv"

# Patch 1 — additional severity_severe markers (researcher review 2026-06-11)
SEVERITY_PATCH1 = re.compile(
    r"\b(erg|heel|fiks|fikse|hele\s+dag)\b", re.IGNORECASE
)

# Patch 3 — energy countersignal patterns (from researcher review 2026-06-11)
# Phrases describing positive energy state that should fire systemisch_vermoeid
# with state=absent (the antonym of fatigue).
ENERGY_COUNTERSIGNAL = re.compile(
    r"\b(goede\s+energie|veel\s+energie|redelijk\s+energie|redelijke\s+energie"
    r"|energie\s+over|energie\s+gaat\s+wel|energie\s+gaat\s+ok"
    r"|lekker\s+fris|veel\s+fitter|energiek|vol\s+energie|fitter\s+dan"
    r"|heerlijk\s+fit|goede\s+conditie|fris\s+gevoel|nog\s+energie)\b",
    re.IGNORECASE,
)


def patch1_severity(clause: str, symptom_states: str, fysiek_subtype: str) -> str:
    """If clause has any symptoom_fysiek subtype AND symptom_states is
    'present' or 'mild', and a Patch1 severity marker appears within
    the first half of the clause (proxy for 'before the symptom phrase'),
    promote state to 'severe'."""
    if not fysiek_subtype:
        return symptom_states
    # symptom_states is a semicolon-separated list like 'symptoom_fysiek=present'
    if "symptoom_fysiek=" not in symptom_states:
        return symptom_states
    # Cheap heuristic: if severity patch1 marker appears anywhere in clause,
    # and current state is present/mild, upgrade to severe.
    if not SEVERITY_PATCH1.search(clause or ""):
        return symptom_states
    new_states = []
    for token in symptom_states.split(";"):
        token = token.strip()
        if not token:
            continue
        if token.startswith("symptoom_fysiek="):
            state = token.split("=", 1)[1]
            if state in ("present", "mild"):
                new_states.append("symptoom_fysiek=severe")
            else:
                new_states.append(token)
        else:
            new_states.append(token)
    return ";".join(new_states)


def patch3_countersignal(row: dict) -> dict:
    """Handle energy-countersignal phrases.

    Two cases:
      A. v2 did NOT tag symptoom_fysiek -> add the tag + state=absent + polarity=positive
      B. v2 tagged symptoom_fysiek but sub_type is 'overig' (or empty) ->
         promote sub_type to systemisch_vermoeid + ensure state=absent + polarity=positive

    Both express that the clause is a positive counter-signal for fatigue.
    """
    clause = row.get("clause") or ""
    if not ENERGY_COUNTERSIGNAL.search(clause):
        return row
    cats = row.get("categories") or ""
    sub = row.get("symptoom_fysiek_subtype") or ""

    in_fysiek = "symptoom_fysiek" in cats
    sub_is_overig = sub in ("", "overig")

    # Skip only if v2 tagged symptoom_fysiek AND sub is already a specific one
    if in_fysiek and not sub_is_overig:
        return row

    new_row = {**row}

    if not in_fysiek:
        if cats and cats != "context_neutraal":
            new_row["categories"] = cats + "|symptoom_fysiek"
        else:
            new_row["categories"] = "symptoom_fysiek"

    # Set state=absent for symptoom_fysiek
    sym_states = row.get("symptom_states") or ""
    parts = [p.strip() for p in sym_states.split(";") if p.strip()]
    parts = [p for p in parts if not p.startswith("symptoom_fysiek=")]
    parts.append("symptoom_fysiek=absent")
    new_row["symptom_states"] = ";".join(parts)

    # Polarity positive
    new_row["polarity"] = "positive"

    # Sub: systemisch_vermoeid
    new_row["symptoom_fysiek_subtype"] = "systemisch_vermoeid"

    new_row["_v23_patch_applied"] = "patch3_countersignal"
    return new_row


def main():
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    print(f"Input: {len(rows)} clauses")

    n_p1 = 0
    n_p3 = 0
    out = []
    for r in rows:
        r = dict(r)  # copy
        before_polarity = r.get("polarity", "")
        before_sub = r.get("symptoom_fysiek_subtype", "")

        # Patch 3 first (may add a new symptoom_fysiek tag)
        r = patch3_countersignal(r)
        # Detect change on any of: polarity, sub, symptom_states (covers all
        # patch3 mutations whether v2 already had symptoom_fysiek or not)
        if (r.get("polarity", "") != before_polarity
                or r.get("symptoom_fysiek_subtype", "") != before_sub):
            n_p3 += 1

        # Patch 1 — severity promotion
        new_states = patch1_severity(
            r.get("clause", ""),
            r.get("symptom_states", ""),
            r.get("symptoom_fysiek_subtype", ""),
        )
        if new_states != r.get("symptom_states", ""):
            r["symptom_states"] = new_states
            r["_v23_patch_applied"] = (r.get("_v23_patch_applied", "") +
                                       ";patch1_severity").strip(";")
            n_p1 += 1

        out.append(r)

    # Preserve original column order; add _v23_patch_applied at end
    fields = list(rows[0].keys()) + ["_v23_patch_applied"]
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in out:
            w.writerow({k: r.get(k, "") for k in fields})

    print(f"\nWrote {OUTPUT}")
    print(f"  Patch 1 (severity promoted to severe): {n_p1} clauses")
    print(f"  Patch 3 (energy countersignal added):  {n_p3} clauses")


if __name__ == "__main__":
    raise SystemExit(main())
