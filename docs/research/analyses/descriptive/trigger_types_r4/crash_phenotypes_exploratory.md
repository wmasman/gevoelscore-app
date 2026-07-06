# Crash phenotypes: do emotional and physical crashes look different? (EXPLORATORY)

**Status**: producer-mode **EXPLORATORY, hypothesis-generating** note for R4. NOT
a locked test and NOT a confirmatory result. It characterises whether crashes sort
into recognisable phenotypes, and proposes a convergence rule as the
operationalisation for a FUTURE phenotype-validation test. Every number is
reproduced by [`crash_phenotypes.py`](crash_phenotypes.py). Drafted 2026-07-06 by
Claude (Opus 4.8), producer-mode, for the participant-researcher (repo owner). n=1,
tiny per-bucket n, self-report, reverse-causation-prone: read as a lead, never a
verdict.

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress.

---

## 0. Why we started this (the origin story)

R4 asks whether crashes can be tied to a *kind* of exertion. The guide (Wiggers)
frames all load as one **energy envelope** -- physical, cognitive, and emotional
each draw on it and each can trigger PEM -- and warns that a step-counter misses
the non-physical ones ("the watch can't see mental PEM"). The question the repo
owner posed was the sharp one: **how much of each load type does the Garmin
actually pick up?** That produced, in order: (1) a data-availability check (the
self-reported 1-3 load triage is well-covered but *presence* is degenerate); (2)
the **autonomic fingerprints of load** (physical shows in cardiac/activity;
emotional shows in stress/battery but not heart rate; cognitive is invisible),
which refine Wiggers' mental-PEM concession
([`../../garmin_exploration/cards/autonomic-fingerprints-of-load-export.md`](../../garmin_exploration/cards/autonomic-fingerprints-of-load-export.md));
(3) a crash-specificity read ([`analysis.md`](analysis.md)) where emotional load
was the only suggestive pre-crash signal. This note is the natural next question:
**do the crashes themselves sort into types, and do the emotional ones look
different -- in the watch and in the notes -- from the physical ones?**

## 1. Three independently-measured axes

- **Trigger** (self-report): which 1-3 load dominated the pre-onset run-up
  `[start-5..start-1]` -- emotional, physical, or none/mixed.
- **Fingerprint** (wearable): the acute-window `[nadir-1..+1]` autonomic
  *loudness* -- overnight + daytime stress and resting HR up, body-battery floor
  down = loud; the storm absent = quiet.
- **Content** (de-identified note tags, no raw text): interpersonal / cognitive
  (family + social + emotional load + brainfog) vs physical-illness (respiratory +
  fever + muscle + infection).

These three come from **different data sources**, so their agreement is not
circular within a source.

## 2. The tendency (group means, more generous than the strict rule)

| dominant trigger | sleep-stress | daytime stress | battery floor | resting HR | interpersonal content | physical-illness content | n |
|---|---|---|---|---|---|---|---|
| **emotional** | +0.45 | -0.29 | **+0.73** | -0.20 | **3.50** | **0.00** | 6 |
| **physical** | **+1.10** | +0.77 | -0.20 | **+0.84** | 0.50 | 1.60 | 10 |
| none/mixed | +2.87 | +1.07 | -0.37 | +0.49 | 1.62 | 1.08 | 13 |

Read as a tendency, the picture is coherent and striking: **emotional-dominant
crashes are autonomically quiet** (battery floor *up*, resting HR *down*, daytime
stress *below* baseline) with **purely interpersonal content and zero
physical-illness content**; **physical-dominant crashes are autonomically loud**
(the stress + RHR storm, battery depleted) with **illness-leaning content**. Depth
and duration are similar across groups (both are equally "real" crashes). So the
emotional crashes are the **quiet / activity-invisible** crashes the guide names
(Wiggers H2), and the physical group carries an illness-adjacent, autonomically
loud signature (closer to the guide's H3 acute-illness pattern).

## 3. The convergence rule (the honest floor)

Requiring **all three axes to agree** shrinks the labelled set sharply and makes
the unclear bucket explicit:

| phenotype (all three agree) | n |
|---|---|
| convergent-quiet (emotional) | **1** |
| convergent-loud (physical / illness) | **4** |
| **unclear** | **24** |

So under a strict tri-axis rule, **only 5 of 29 crashes get a clean label, and 24
(83%) are unclear.** This is the load-bearing honesty: the phenotypes exist as
*tendencies* (section 2) but as a strict *classification* they confidently label
very few crashes. "Unclear" is not a failure to report -- it is the largest and
most honest category, and it reinforces R32(a) (the record cannot cleanly attribute
a trigger to most crashes).

## 4. What we can and cannot claim (the labelling epistemics)

- **Phenotype, not trigger.** "Emotional-dominant, autonomically quiet,
  interpersonal-content crash" is a **descriptive type**, not "a crash caused by
  emotional stress." Association, not causation; reverse causation (a prodrome
  raising emotional-load logging before the felt drop) is not excluded.
- **The convergence count is a description, not a test.** The rule was found in
  these data, and its three axes were chosen *because* they line up, so the bucket
  counts are a picture of the data, never a p-value. It must never be reported as
  confirmation on these 29 crashes.
- **The strict rule under-counts on purpose.** Its value is exactly that it is
  conservative: it puts a floor on what we can confidently label and refuses to
  force the ambiguous majority into a bin.

## 5. The household-illness de-confounder: right idea, data absent

The repo owner proposed a clean de-confounder for viral crashes: since the
participant's *own* symptoms (runny nose, cough, feeling feverish) cannot separate
a real virus from severe PEM (they look the same), label viral crashes by an
**external** marker -- mentions of *others in the household* being ill. Feasibility
check (de-identified, `crash_phenotypes.py`): the whole corpus has **18 note-dates
with any illness mention, 0** pairing an illness term with a household member in the
same clause, and **2** with any loose same-date co-occurrence. The illness mentions
that exist are tagged as the participant's *own* physical symptoms -- exactly the
PEM-mimic signal the de-confounder was meant to avoid. **Verdict: the external
household-illness marker is essentially absent from the record**, so viral crashes
cannot be cleanly separated from PEM here. The methodology is sound; the fix is
**prospective** -- start logging household illness (a one-field addition) so future
crashes can carry this external marker. Logged as a data-collection suggestion in
[`../../../methodology/queued_work.md`](../../../methodology/queued_work.md).

## 6. Operationalisation proposal for a FUTURE phenotype-validation test

The convergence rule is a strong **operationalisation** for a future test, but only
in one of two non-circular forms (it is NOT usable as a test on these data, and NOT
part of the emotional-*trigger* pre-reg, where the fingerprint is outcome-adjacent
and cannot enter the exposure definition):

1. **Prospective lock.** Freeze the convergence definition (the three axes + their
   thresholds) now; apply it to crashes that occur *after* the lock date. The
   phenotype either recurs cleanly or dissolves. This also de-confounds the era
   issue (future crashes are one medication era).
2. **External validator.** Use the convergence-defined phenotype to predict an
   outcome *not used to define it* -- e.g. recovery-trajectory shape, recurrence
   spacing, or differential response to a pacing vs emotion-regulation strategy. An
   external, held-out outcome breaks the circularity even on partly-retrospective
   data.

Either would need its own methodology MD + pre-registration (drafted and reviewed
in different sessions), with thresholds locked before any outcome look. Logged as a
proposed test in `queued_work.md`.

## 7. Caveats

- **n=1, tiny buckets** (convergent-quiet = 1, convergent-loud = 4); no CIs on the
  buckets; the group means (section 2) are 6 vs 10 crashes with no error bars.
- **Self-report + presence-conditioned** trigger axis; **reverse causation** not
  excluded; the fingerprint thresholds (median split) and content tags are one
  reasonable descriptive operationalisation, and the counts depend on them.
- **Descriptive, no causal / interpretive marks** (CONVENTIONS section 4.1): "the
  emotional-dominant crashes co-occurred with a quiet fingerprint and interpersonal
  notes," never "emotional stress caused a quiet crash."

## 8. Cross-references

- Precondition + concordance + Wiggers timing: [`precondition.md`](precondition.md);
  crash-specificity: [`analysis.md`](analysis.md); scripts
  [`crash_phenotypes.py`](crash_phenotypes.py),
  [`crash_specificity_analysis.py`](crash_specificity_analysis.py),
  [`precondition_analysis.py`](precondition_analysis.py).
- Site card: [`../../garmin_exploration/cards/autonomic-fingerprints-of-load-export.md`](../../garmin_exploration/cards/autonomic-fingerprints-of-load-export.md).
- Guide anchors: `../../../wiggers_testable_hypotheses.md` (H2 activity-invisible /
  mental PEM; H3 acute-illness signature).
- Site register R4, R32 (no visible trigger-into-crash signal), R33 (load response):
  the site's `docs/research-requests.md` (external repo `wiggers_research_story`).
- CONVENTIONS: single-pool primacy; section 4.1 (no interpretive marks); section 4.3
  (prior-driven direction from the guide = confirmatory for a future test).
