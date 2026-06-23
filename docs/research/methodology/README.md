# methodology/ — binding rules and dictionaries

The documents in this folder are the **interpretive rules** that bind
every analysis on the corpus. They're not advice; they're decisions
that analysts must respect to get correct answers from the data.

---

## Discipline note: methodology drafted after corpus engagement

The methodology decisions in this folder were drafted after substantial
corpus engagement (multiple Garmin extractions, descriptive analyses,
locked HA-numbered pre-regs). They are **pre-registration discipline
going forward** — every future hypothesis test runs under the rules
these MDs articulate — and **not** a pretence that the corpus has
never been examined.

The operative safeguard is the "decision frozen at pre-reg time, no
re-tuning" rule that every MD in this folder upholds. Historical
findings (HA01b, HA02c, HA08, HA11, H05) remain as the historical
record; new hypothesis files cite the relevant methodology MD and
follow its rules. Cross-checks between historical verdicts and the
new framework are descriptive, never automatic re-locks.

This framing is also embedded in
[[feedback_methodology_decisions_documented_reasoning]]
and [[feedback_caveats_vs_apriori]]: caveat what
we haven't done, don't claim methods we haven't earned.

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

6. **[lc_era_temporal_segmentation.md](lc_era_temporal_segmentation.md)** —
   data-given strata (pre-corona / corona-infection / LC-pre-gevoelscore
   / LC-with-gevoelscore-and-crash-labels = Stratum 4) vs methodological
   sub-segmentation. **Stratum 4 is the primary analytic surface** for
   Wiggers pre-regs. No default sub-segmentation inside Stratum 4;
   M1/M2/M3 warrant required.

7. **[permutation_null_block_length.md](permutation_null_block_length.md)** —
   block-length policy for stationary bootstrap + permutation null
   tests on the day-resampling layer. Default **E[L] = 7 days**;
   data-driven companion + pre-registered override rule. Event-level
   permutation (n=29) is a separate layer with its own combinatorics.

8. **[train_validate_split_fate.md](train_validate_split_fate.md)** —
   **single-pool primary** for new Wiggers pre-regs; the historical
   2023-12-31 split is preserved as a reproducibility artefact only;
   optional M3 descriptive overlay. HA01b train-vs-validate divergence
   is a number, not a narrative.

9. **[_pending_literature_fetch.md](_pending_literature_fetch.md)** —
   self-contained brief for a future agent to acquire, verify, and
   integrate the statistical-methodology citations currently deferred
   in MDs 6-8.

10. **[research_line_limitations.md](research_line_limitations.md)** —
    binding enumeration of the seven systemic limitations of the
    research line (single-subject reach, era confounds, device
    generations, analyst-is-subject, presence-conditioned data layer,
    self-reporting, survivorship). Authored 2026-06-23 per
    [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
    §3.9 + §11 step 4. **Per-topic contextualisation MDs and per-
    construct actionability MDs MUST cite the relevant limitations
    from this doc.**

---

## Results-analysis layer (in development)

The following docs scaffold the results-analysis methodology layer
that takes locked HA verdicts through interpretation → synthesis →
contextualisation → actionability → audience translation:

- **[_plan_results_analysis_layer.md](_plan_results_analysis_layer.md)** —
  layer-level plan (r4 LOCKED 2026-06-23). Specifies six guides + one
  skill + two supporting MDs (this list will populate as drafting
  progresses per the plan's §11 implementation order).
- **[_descriptive_stocktake_2026-06-23.md](_descriptive_stocktake_2026-06-23.md)** —
  step 3 of §11. Per-HA assumption-backstop matrix + decisions on
  HA fate (retire / shelve / supersede / proceed).
- **[research_line_limitations.md](research_line_limitations.md)** —
  step 4 of §11. The binding systemic-limitations enumeration above.

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
