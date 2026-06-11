"""Prepare a quality-review CSV for spot-checking v2 / v2.2 categorisation.

The v2 dictionary uses substring matching on lowercased Dutch text.
For short, descriptive, or context-dependent clauses, the deterministic
matching may misfire. This script samples clauses likely to be borderline
and produces a review CSV the researcher can spot-check.

Sampling strategy (per category):
  - 10 short clauses (≤ 8 words): test if minimal context still classifies right
  - 5 multi-category clauses: test category-overlap correctness
  - 5 overig clauses: surface possible dictionary gaps
  - 5 negated-symptom clauses ("geen X"): test that absent state is set
  - 5 polarity-positive clauses with symptom mention ("redelijk fit"): test
    that polarity layer doesn't flip the category-state interaction

Output: categorization-quality-review.csv with the user's `correct` column
for spot-checking.
"""
from __future__ import annotations

import csv
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "notes-categorized-v22-clauses.csv"
OUTPUT = HERE / "categorization-quality-review.csv"

# Deterministic sampling
random.seed(42)

NEGATION_RE = re.compile(r"\b(geen|niet|zonder|nauwelijks|amper|nooit)\b", re.IGNORECASE)
POLARITY_POSITIVE = ["leuk", "fijn", "goed", "redelijk", "beter", "prima", "top", "heerlijk"]


def n_words(s):
    return len(re.findall(r"\S+", s or ""))


def pick_n(pool, n):
    if not pool:
        return []
    if len(pool) <= n:
        return pool
    return random.sample(pool, n)


def main():
    if not INPUT.exists():
        print(f"ERROR: {INPUT} does not exist. Run sub_categorize_v22_fysiek.py first.")
        return 1

    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    print(f"Input: {len(rows)} clauses")

    samples = []

    # 1. Short clauses per sub-category
    short_by_sub = defaultdict(list)
    for r in rows:
        cl = r.get("clause", "")
        sub = (r.get("symptoom_fysiek_subtype") or "").strip()
        if not sub:
            continue
        if n_words(cl) <= 8:
            # Use first sub-tag for grouping
            primary_sub = sub.split(";")[0]
            short_by_sub[primary_sub].append(r)
    for sub, pool in short_by_sub.items():
        for r in pick_n(pool, 10):
            samples.append((r, f"short_in_{sub}",
                           f"Short clause classified as {sub} — does the {sub}-classification still fit with so little context?"))

    # 2. Multi-tag clauses (>=2 sub-types)
    multi = [r for r in rows if (r.get("symptoom_fysiek_subtype") or "").count(";") >= 1]
    for r in pick_n(multi, 8):
        sub = r.get("symptoom_fysiek_subtype", "")
        samples.append((r, f"multi_tag",
                       f"Multi-tagged ({sub}) — are all tags justified for this clause?"))

    # 3. Overig clauses (no specific sub matched but symptoom_fysiek was tagged)
    overig = [r for r in rows if r.get("symptoom_fysiek_subtype", "") == "overig"]
    for r in pick_n(overig, 10):
        samples.append((r, "overig",
                       "v2 said symptoom_fysiek but no v2.2 sub matched — is symptoom_fysiek the right v2 tag here, OR is there a sub we missed?"))

    # 4. Negated symptom clauses ("geen X")
    negated = [r for r in rows
               if (r.get("symptoom_fysiek_subtype") or "")
               and NEGATION_RE.search(r.get("clause", ""))]
    for r in pick_n(negated, 8):
        sub = r.get("symptoom_fysiek_subtype", "")
        state = r.get("symptom_states", "")
        samples.append((r, "negated",
                       f"Clause has negation ('geen/niet') — symptom_states says {state!r}. Is state correctly 'absent'?"))

    # 5. Polarity-positive clauses with symptom mention
    pos_with_sym = []
    for r in rows:
        sub = r.get("symptoom_fysiek_subtype") or ""
        if not sub:
            continue
        cl = (r.get("clause", "") or "").lower()
        if any(p in cl for p in POLARITY_POSITIVE):
            pos_with_sym.append(r)
    for r in pick_n(pos_with_sym, 6):
        pol = r.get("polarity", "")
        sub = r.get("symptoom_fysiek_subtype", "")
        samples.append((r, "positive_polarity_with_symptom",
                       f"Clause has positive polarity marker AND symptoom_fysiek ({sub}) — polarity says {pol!r}. Did the polarity layer flip correctly?"))

    # Dedupe by clause text + reason (sometimes the same clause shows up in multiple
    # filter buckets, especially short + overig).
    seen = set()
    out_rows = []
    for r, reason, question in samples:
        key = (r.get("date", ""), r.get("clause_idx", ""), reason)
        if key in seen:
            continue
        seen.add(key)
        out_rows.append({
            "date": r.get("date", ""),
            "clause_idx": r.get("clause_idx", ""),
            "clause": r.get("clause", ""),
            "v2_categories": r.get("categories", ""),
            "v2_symptom_states": r.get("symptom_states", ""),
            "v2_polarity": r.get("polarity", ""),
            "v22_sub_type": r.get("symptoom_fysiek_subtype", ""),
            "sample_reason": reason,
            "review_question": question,
            "correct": "",  # user fills: y / n / partial
            "user_notes": "",
        })

    fields = ["date", "clause_idx", "clause",
              "v2_categories", "v2_symptom_states", "v2_polarity",
              "v22_sub_type", "sample_reason", "review_question",
              "correct", "user_notes"]
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print(f"\nWrote {OUTPUT}")
    print(f"Total samples for review: {len(out_rows)}")
    by_reason = Counter(r["sample_reason"] for r in out_rows)
    print("\nBreakdown by sample reason:")
    for r, n in by_reason.most_common():
        print(f"  {r}: {n}")


if __name__ == "__main__":
    raise SystemExit(main())
