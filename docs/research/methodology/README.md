# methodology/ — binding rules and dictionaries

The documents in this folder are the **interpretive rules** that bind
every analysis on the corpus. They're not advice; they're decisions
that analysts must respect to get correct answers from the data.

---

## Read these in order

1. **[methodology.md](methodology.md)** — overall research methodology
   (load scale, triage decision rules, validation lenses, history of
   decisions). The umbrella doc.

2. **[symptom_mention_asymmetry.md](symptom_mention_asymmetry.md)** —
   the v24 clause CSV is a **presence-conditioned positive evidence
   layer, NOT a symptom-prevalence panel**. Binding rule for all
   note-derived columns (`cat_*`, `state_*`, `day_dominant_polarity`,
   etc.) and for `per_day_intensity` loads (also presence-conditioned).
   Trajectories use daily-computed signals only.

3. **[nightly_attribution.md](nightly_attribution.md)** — the
   wake-up-date convention for sleep + RHR + any nocturnal data.
   Aligns with Garmin's `calendarDate` and avoids double-counting.

4. **[garmin_indicators_audit.md](garmin_indicators_audit.md)** —
   per-column provenance map for Garmin signals + known issues
   catalogue (e.g. push_burden's rolling-baseline contamination)
   + inventory of available-but-not-yet-extracted signals.

5. **[queued_work.md](queued_work.md)** — research follow-ups
   deferred from triage sessions (Q1 brainfog/spierpijn HA pre-reg,
   Q2 hidden-dip review, Q3a allocation shift, Q3b umbrella review,
   Q5 cross-validation lens guidance).

---

## Symptom-categorisation dictionaries

- **[symptom_categorization_v24.md](symptom_categorization_v24.md)** —
  the v2 / v2.2 / v2.3 / v2.4 categorisation chain. Multi-tag rules,
  sub-types for `symptoom_fysiek`, patches applied (slaap split,
  countersignal handling, severity broadening, pacing distinction,
  redelijk neutral, post-symptom negation).
- **[symptom_categorization_quality_review.md](symptom_categorization_quality_review.md)**
  — inter-coder review process. The v2.4 categorisation was sample-
  validated at ~90% accuracy.

The actual phrase dictionaries used by `categorize_v2.py` live at
`docs/research/notes/02-categorize-clauses/category_dictionary_v2.md`
(gitignored; the file is code-adjacent input but the existing rule
keeps it out of the repo as a privacy precaution — change that rule
if a future revisit re-classifies the phrases as publishable).

---

## When a new methodology decision needs to land

Add a new `.md` file here with the same shape:

1. **Status / locked date** at the top.
2. **The rule** in one paragraph.
3. **Why** (rationale).
4. **Operationalisation** (which columns / scripts implement it).
5. **Cross-references** to related docs.

Then link the new file from the root [README.md](../README.md) §7 and
from this README's "Read these in order" list.

If the methodology decision changes interpretation of existing data,
also add an entry to the relevant column's row in
[DATA_DICTIONARY.md](../DATA_DICTIONARY.md) update log.
