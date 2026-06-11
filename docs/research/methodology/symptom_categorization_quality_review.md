# How to triage `categorization-quality-review.csv`

106 stratified samples from the v2 + v2.2 categorisation output, chosen
to surface where the deterministic Dutch substring matching may be off.

## Why this review matters

The v2 categoriser uses substring matching on a fixed phrase dictionary.
For Dutch text that is **short, descriptive, or context-dependent**, this
can misfire in a few ways:

- A phrase appears but the meaning is reversed by context outside the
  3-word negation window ("vandaag eindelijk geen hoofdpijn meer" — the
  meaning is positive but the "geen" is more than 3 words from "hoofdpijn").
- A clause is short enough that the polarity layer has too little to work
  with ("kapot" alone — symptom or pacing reflection?).
- Multi-tag fires where only one tag is justified ("een leuk gesprek met
  hoofdpijn" — symptoom_fysiek is right, but is belasting_emotioneel?).
- The v2.2 sub-classification picks a misleading sub-type when the
  clause is genuinely ambiguous.

This is **not** a re-triage. The fix is at the dictionary level (add a
phrase, refine a polarity marker), not at the per-clause level.

## Workflow

1. Open
   [categorization-quality-review.csv](categorization-quality-review.csv)
   in a Google Sheet (or your editor of choice).
2. For each row, read the `clause` and the assigned tags
   (`v2_categories`, `v2_symptom_states`, `v2_polarity`, `v22_sub_type`).
3. Read the `sample_reason` and `review_question` — they explain why
   this row was selected for review.
4. Fill the `correct` column with one of:
   - `y` — categorisation is correct
   - `n` — categorisation is wrong (please add a note)
   - `partial` — partially right (e.g. category is right but
     sub-type is wrong)
5. Use `user_notes` for any clarification — especially for `n` /
   `partial` rows, indicate what the right answer would be.

## Sample reasons

| reason | what it tests |
|---|---|
| `short_in_X` | Short clauses (≤ 8 words) tagged as sub-type X. Tests whether minimal context still gives correct classification. |
| `multi_tag` | Clauses with multiple sub-types. Tests whether all tags are justified. |
| `overig` | Clauses that v2 tagged `symptoom_fysiek` but no v2.2 sub matched. Tests whether v2 was right + whether we missed a phrase. |
| `negated` | Clauses with negation markers ("geen", "niet"). Tests whether `symptom_states` was correctly set to `absent`. |
| `positive_polarity_with_symptom` | Clauses with positive polarity ("redelijk", "fijn") AND a symptom mention. Tests whether the polarity layer correctly flipped state or polarity. |

## Sample breakdown

- 64 `short_in_*` (per sub-type — 10 each for the bigger sub-types)
- 10 `overig`
- 8 `multi_tag`
- 8 `negated`
- 6 `positive_polarity_with_symptom`

**Total: 106 rows.**

## Expected effort

~45 min for 106 rows. Most will resolve in seconds (a quick read of the
clause + tags). The attention is on:

- `overig` clauses: are these v2 false positives, or v2.2 gaps?
- `negated` clauses: did the 3-word window catch them?
- `multi_tag` clauses with surprising combinations.

## What happens after you share

1. Share the filled-in CSV (Google Sheets link or path to a saved CSV).
2. I aggregate:
   - **Overall accuracy** (% `y` / `partial` / `n`).
   - **Per-sub accuracy** (where does v2.2 perform best / worst).
   - **Negation accuracy** (does the 3-word window work for Dutch?).
3. If accuracy is acceptable (say ≥ 90% on the non-overig samples):
   v2.2 is locked. Q1 hypothesis pre-registration can proceed.
4. If specific failure modes surface (negation window too narrow,
   `overig` clauses that should have matched, etc.): we patch the
   dictionary or add v2.3 rules and re-classify before Q1 starts.

## What this is NOT

- **Not a re-triage of the underlying notes.** The day-entry text stays
  as is. We're checking whether the auto-categorisation matched it
  correctly.
- **Not a full audit.** 106 rows out of 2410 is a stratified spot-check.
  If issues surface, we can expand the audit (sample more from the
  failing buckets).
- **Not authoritative against the dictionary.** A `correct=n` row
  doesn't change the dictionary by itself; it triggers a dictionary
  decision (add a phrase? change the negation window? accept the
  edge case?).

## Cross-references

- v2 dictionary: [category_dictionary_v2.md](category_dictionary_v2.md)
- v2.2 sub-classification: [category_dictionary_v2.2_sub_fysiek.md](category_dictionary_v2.2_sub_fysiek.md)
- Hypothesis context: [../../timeline/methodology.md](../../timeline/methodology.md) §3a
- Queued work: [../../timeline/queued_work.md](../../timeline/queued_work.md) Q1
