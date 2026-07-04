# Gevoelscore — lived definitions per level

*Anchoring reference, authored by the participant 2026-06-26. **Indicative, not rigid.** These descriptions are the lived meaning the score is tracked against — what each level corresponds to in daily-functioning terms. They are NOT a scoring rubric (the participant does not consult this table when assigning a score; the score is interoceptive). They ARE the reference against which any analyst or reader can interpret what a "3" or a "5" actually means for this body.*

---

## Why this exists

Numerical scores on a 1-10 scale are meaningless without anchoring. A "3" on a clinical pain scale is not a "3" on a depression inventory is not a "3" on this participant's daily energy / functioning score. This document writes down what each value of the gevoelscore actually corresponds to in lived terms, so the rest of the research — and the public-facing site — can be interpreted against a stable reference.

The lived ceiling in four years (2022-09-03 → present) is **6**. Scores 7-10 have never been used. This is itself a finding: the upper register of this body's range tops out at "functional with active pacing constraints," not at anything resembling a healthy baseline.

---

## Levels 1-6 (lived definitions)

### 1 — Volledig uitgeschakeld

Op bed, slapen of met heftige hoofdpijn etc. Gordijnen dicht, geen prikkels aankunnen.

### 2 — Volledig uitgeschakeld

Kan van bed naar de bank, een kort gesprek voeren, korte stukjes van bed naar tafel oid lopen. Veel slapen overdag.

### 3 — Grootdeels uitgeschakeld

Bij lopen e.d., snel een verhoogde hartslag, misschien een vaatwasser inpakken, even douchen, een korte wandeling buiten. Kan korte gesprekken over eenvoudige dingen voeren. Maar heb ook klachten als hoofdpijn, brainfog, duizeligheid etc.

### 4 — Grootdeels uitgeschakeld

Het grootste deel van de dag geen pijn. Zowel in ochtend als middag, blokken van 1 of 2 uur waarin ik helder ben qua denken. Kan geen serieuze inspanningen leveren. Ik kan een korte afstand lopen zonder daar lang van bij te moeten komen. Heb na elke activiteit ook even lang rust nodig (op de bank, kalmeren, ogen dicht). Maar moet ook nog ~2 uur slapen / dieper rusten in de middag. Kan meedoen met avondeten en heel misschien kids naar bed brengen samen. Dan ga ik om 21:00 slapen.

### 5 — Deels uitgeschakeld

Geen pijn. Kan na het opstaan meedoen met het gezin. Maar koken einde dag is iets wat vooraf gepland moet worden ten koste van iets in de middag. Gedurende de dag elke 20 min tussendoor steeds rusten. Kan in de ochtend en middag, met rust tussendoor, in totaal ongeveer 4 uur iets doen met niet teveel prikkels of te zware inspanning (vb. licht werken achter computer, wandelen, koffiedrinken etc.). Lichamelijke inspanning met licht verhoogde hartslag kan kort, mits daarna voldoende rust en niet te vaak per week. Ga om 20:00 naar bed en om ongeveer 21:00 slapen.

### 6 — Deels uitgeschakeld

Zelfde als op niveau 5 maar dan aan het einde van de dag niet uitgeput. Waardoor of in de avond ook de mogelijkheid om rustige gesprekken te voeren, een film te kijken samen of andere rustige dingen te doen. En dan om 22:00 naar bed.

### 7-10 — never reached in the LC era

No lived definition exists. The participant has not used these values in 1,372+ scored days (2022-09-03 → present).

---

## Cluster structure

The lived definitions self-cluster into three states of two levels each:

| Cluster | Levels | Lived state |
|---|---|---|
| **Volledig uitgeschakeld** | 1, 2 | Fully shut down. Bed-based. Pain / extreme symptoms. Minimal motion possible at 2. |
| **Grootdeels uitgeschakeld** | 3, 4 | Largely shut down. Limited activity, with active symptoms at 3, with symptom-free windows of 1-2 hours at 4. Heavy rest required around any activity. |
| **Deels uitgeschakeld** | 5, 6 | Partially shut down. Pain-free. Family-functional with strict pacing windows. ~4 hours of light activity possible. Difference between 5 and 6 is end-of-day reserve. |

This is the same shape as the project's three-cluster framing applied elsewhere in the methodology. It is consistent with — but was not engineered to match — that framing.

---

## What this anchors

### crash_v2 thresholds

[crash_v2-definition.md](analyses/hypotheses/crash_v2-definition/definition.md) defines a **crash** as "score ≤ 3 for ≥ 2 consecutive days" and a **dip** as "isolated single day with score ≤ 3, neighbours ≥ 4". Reading the threshold against the lived definitions:

- **`crash` (≤ 3 for ≥ 2 days)** = "largely-or-fully shut down with active symptoms (headache, brainfog, dizziness, sometimes bed-bound) for at least two consecutive days." This is the lived phenomenology of PEM as described in the LC literature. The statistical threshold is anchored in lived experience, not arbitrary.

- **`dip` (single ≤ 3 day, neighbours ≥ 4)** = "an isolated bad day where activity was either impossible or accompanied by active symptoms, but the surrounding days had symptom-free windows." The lived definition of an acute bad day.

- **`normal` (everything else, including score-4 days)** = "score-4 days have ~1-2 symptom-free windows per day but still require heavy rest, deep afternoon nap, early bedtime." The crash_v2 definition correctly does NOT treat score-4 days as bad days, but they are also not what a healthy person would call good days — they are *functional within a narrow envelope*.

### The "no good day" caveat

Recently added to [crash_v2-definition.md §6](analyses/hypotheses/crash_v2-definition/definition.md) — that the gevoelscore distribution has no symmetric positive counter-pole, making a "good day" comparator structurally infeasible. The lived definitions confirm this directly: the lived ceiling at 6 corresponds to "level 5 but with end-of-day reserve for calm evening activities." A healthy person's baseline would be 7-10, never used in this corpus. The compressed upper register is not a measurement artefact — it is the lived experience.

### The score-watch correspondence

The graded autonomic-load story established by [cohort_topology/findings.md](analyses/descriptive/trajectory/cohort_topology/findings.md) (crash deeper than dip deeper than normal on autonomic channels) maps directly to the lived gradient: at levels 1-2 motion is minimal; at levels 3-4 activity attempts coincide with active symptoms (autonomic dysregulation visible); at levels 5-6 the body is functional but with strict pacing windows. The watch's severity scaling is detecting a graded lived state, not just a statistical category.

### Recalibration of "normal" downward

This is the canonical evidence for the recalibration-of-normal-downward framing referenced in conversation. The participant assigns scores against a personal scale where 5-6 is functional-with-strict-pacing — i.e. the personal sense of "OK day" sits where a healthy person would expect more. The score is internally consistent and meaningful for this body's range, but its absolute numbers are not commensurable with a healthy person's same-numbered scale.

---

## How to use this in interpretation

- **Reading any crash result**: a crash episode is at least 2 days in the levels 1-3 range — meaning at least 2 days where bed-to-couch motion is the ceiling, often with active symptoms. The autonomic-channel shifts cohort_topology reports are aligned to this lived reality.

- **Reading any dip result**: an isolated bad day in the levels 1-3 range with surrounding days at 4+ — an acute event against a functional-but-narrow envelope.

- **Reading any "normal day" baseline**: this includes score-4 days where the participant is largely shut down but pain-free, score-5 days where 4 hours of light activity is possible with constant rest, and score-6 days where evening calm activities are possible. The "normal" baseline in this corpus is NOT a healthy baseline.

- **Reading any "good vs crash" framing**: don't. The data has no good-day pole.

- **Reading any "improvement over time" framing**: improvement means more days at the upper end of this 1-6 range, not movement into 7-10 territory. Forward-collected data will continue to be interpreted against this same anchor unless the lived ceiling shifts (in which case this document would be revised, with the prior version retained as historical record).

---

## How to use this on the site

The [what-is-a-crash](https://github.com/wmasman/gevoelscore-app/blob/main/docs/research/gevoelscore_lived_definitions.md) page currently states *"The felt-state score runs 1 to 10, but in four years it never once rose above {ceiling}."* This document can serve as the deeper anchor for that sentence — readers can be shown WHAT each level corresponds to in lived terms, making the ceiling claim concrete rather than abstract.

The cluster structure (volledig / grootdeels / deels uitgeschakeld) also gives the site a natural way to talk about gradations without leaning on the bare numbers.

**Privacy note**: these are participant-authored lived definitions. They contain personal-functioning detail but no individually identifying information. They are publishable on the site as authored, in the participant's voice, in Dutch. If a translation for English-language readers is added, it should be paired with the Dutch original, not replace it.

---

## Provenance and revision discipline

- **Authored**: 2026-06-26 by the participant, mid-research, during a thinking session about site scope and score-watch correspondence.
- **Status**: indicative reference, not rigid scoring rubric. The participant does not consult this table when assigning a score; the score remains interoceptive.
- **Revision rule**: if the lived ceiling shifts (e.g. a sustained period of score 7 being reached), or if the meaning of any level meaningfully changes in the participant's experience, this document is revised with a dated update entry below. The prior version is retained as historical record. The numerical scores themselves remain comparable across time even if the lived definitions evolve — this is a property of interoceptive self-report and is acknowledged as such.
- **Not a pre-registration**: this document is not a hypothesis-precommitment. It is descriptive anchoring of what the score has meant for this body across the LC era so far.

---

## Cross-references

- [crash_v2-definition.md](analyses/hypotheses/crash_v2-definition/definition.md) — operational crash and dip definitions; this document anchors the lived meaning of the thresholds.
- [cohort_topology/findings.md](analyses/descriptive/trajectory/cohort_topology/findings.md) — watch-side severity gradient; this document anchors the lived-side gradient that grades into it.
- [lived_experience_garmin_pacing_2026-06-14.md](lived_experience_garmin_pacing_2026-06-14.md) — narrative-only lived-experience braindump on pacing protocols; this document is the more compact functioning-anchor counterpart.
- [note_2026-06-26_scope_clarification_and_step1_steelman.md](note_2026-06-26_scope_clarification_and_step1_steelman.md) — the session note from which this anchor emerged; logs why it exists and what it changes.
