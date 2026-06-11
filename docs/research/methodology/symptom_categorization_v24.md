# v2.2 — symptoom_fysiek sub-categorisation

**Status**: shipped 2026-06-11. Built on top of locked v2 (categorize_v2.py
output stays untouched).

Adds a `symptoom_fysiek_subtype` column to the per-clause output, splitting
the (high-N) `symptoom_fysiek` category into specific symptom families.
This makes hypotheses like §3a brainfog-hidden-dip and muscle-pain-crash-
precursor testable on appropriate sub-populations rather than the
catch-all `symptoom_fysiek`.

## Why a downstream refinement instead of v3

- v2 is locked and stable; many analyses already reference its columns.
- Sub-classification has no negation / severity / polarity interaction —
  it's just a partition of which symptoom_fysiek-tagged clauses go in
  which bucket.
- Multi-tag is natural (a clause can be both hoofdpijn and systemisch_vermoeid).

The sub-classification only fires when v2 already tagged the clause
`symptoom_fysiek`. It is a refinement, not a re-classification.

## Sub-categories

For each clause tagged `symptoom_fysiek`, the script runs substring matching
against these phrase lists. Multi-tag is permitted; a single clause can
carry multiple sub-types.

### hoofdpijn
```
hoofdpijn, migraine, pijn in mijn hoofd, hoofd doet pijn
```
**Observed N**: 262 clauses (single largest sub-category)

### spier
```
spierpijn, zware benen, zere benen, benen zwaar, in mijn lijf,
zwaar in de benen, stijfheid, stramme spieren, spieren pijn,
zwaar lichaam, stijf
```
**Observed N**: 42 clauses (much more than initially estimated — the
"in mijn lijf" phrase contributes heavily)

### keel_respiratoir
```
keelpijn, verkouden, hoesten, loopneus, snot, snotneus,
snotterig, snotterige, koortslip, keel
```
**Observed N**: 33 clauses

### koorts
```
koorts, koortsig
```
**Observed N**: 10 clauses

### gastro
```
misselijk, misselijkheid, braken, overgeven, kotsen,
maagpijn, maag van streek, buikpijn, opgeblazen buik
```
**Observed N**: 8 clauses

### huid
```
jeuk, jeukt, jeuken
```
**Observed N**: 2 clauses

### neuro
```
tintelende, tintelend, duizelig, duizeligheid
```
**Observed N**: 5 clauses

### systemisch_vermoeid
```
moe, uitgeput, kapot, gesloopt, slap, zwakte,
weinig energie, geen energie
```
**Observed N**: 384 clauses (very large — and includes the bare "moe"
which is heavily used. Combine with state modifiers + polarity layer
to distinguish "lichte moeheid" from "kapot uitgeput".)

### slaap
```
slecht geslapen, matige nacht, matig geslapen, onrustig geslapen,
wakker geweest, veel wakker, slecht in slaap, laat in slaap,
veel hoofdpijn vannacht, vannacht onrustig,
opstaan valt niet mee, vroeger opstaan, vroeg opstaan,
moeite met opstaan, ochtendroutine, matige slaap
```
**Observed N**: 25 clauses

### generiek_lijf (auxiliary — promoted to `overig` when alone)
```
lijf, fit, energie
```
These three very general body/energy descriptors fire only when no
specific sub-category matched first. If `generiek_lijf` is the only
match for a clause, the script demotes it to `overig` (so we don't
inflate the body-descriptor bucket with vague mentions).

### overig
Clauses that v2 tagged `symptoom_fysiek` but none of the v2.2 sub-types
matched (after the generiek_lijf demotion). This bucket is the
spot-check surface for v2.2 dictionary gaps.

**Observed N**: 73 clauses

## How the script behaves

For each clause:
1. If v2 did NOT tag `symptoom_fysiek` → `symptoom_fysiek_subtype` left empty.
2. If v2 tagged `symptoom_fysiek`:
   - Substring-match each sub-category's phrase list.
   - Collect all matching sub-types.
   - Apply the `generiek_lijf` demotion rule:
     - alone → replace with `overig`
     - with a specific sub → drop `generiek_lijf`
   - If still empty → `overig`.

Result: every `symptoom_fysiek`-tagged clause gets at least one v2.2 sub-type.

## Observed distribution

| sub | N |
|---|---:|
| systemisch_vermoeid | 384 |
| hoofdpijn | 262 |
| overig | 73 |
| spier | 42 |
| keel_respiratoir | 33 |
| slaap | 25 |
| koorts | 10 |
| gastro | 8 |
| neuro | 5 |
| huid | 2 |

Multi-tag distribution across symptoom_fysiek clauses:
- 1 tag: 752 clauses
- 2 tags: 42 clauses
- 4 tags: 2 clauses

(Total 796 ≠ sum of sub-N because of multi-tag overlap.)

## Quality review process

After running `sub_categorize_v22_fysiek.py`, the companion script
`prepare_categorization_quality_review.py` produces
`categorization-quality-review.csv` — a stratified sample of clauses
likely to be borderline:

- short clauses per sub-type (test minimal-context classification)
- multi-tag clauses (test category-overlap correctness)
- overig clauses (surface possible gaps)
- negated clauses (test that `state=absent` was set)
- positive-polarity clauses with symptom mention (test polarity layer)

Researcher (the user) reviews this sample and fills the `correct`
column (`y` / `n` / `partial`) + `user_notes`. Dictionary gaps surfaced
during review feed v2.3 (or trigger a fix-in-place for the v2.2 phrase
lists, depending on scope).

## v2.3 patches (researcher review 2026-06-11)

After the first 106-sample researcher review, four patches were
applied. Patches 2 and 4 fit into the v2.2 sub-classifier (dict
adjustments); patches 1 and 3 needed a downstream patch layer
(`apply_v23_patches.py` → `notes-categorized-v23-clauses.csv`).

### Patch 1 — Severity broadening (v2.3)
The v2 modifier window catches "heel erg(e)" but missed bare "erg",
"heel", "fikse", "fiks" — common Dutch intensifiers. The patch layer
re-evaluates `symptom_states` for symptoom_fysiek clauses: if any of
`erg`, `heel`, `fiks`, `fikse`, `hele dag` appears in the clause AND
state is `present` or `mild` → promote to `severe`.

**Effect**: 83 clauses had state promoted from present/mild to severe.

### Patch 2 — Slaap vs systemisch_vermoeid split (v2.2 dict)
User feedback: "slecht geslapen doesnt say anything about energy
during the day so only tag sleep". Sleep phrases were also added to
the `slaap` sub-category positively (so "goed geslapen" now fires
`slaap`, not `systemisch_vermoeid` as countersignal).

**Effect**: `slaap` sub-category went 25 → 82 clauses (sleep phrases
that were previously absorbing into systemisch_vermoeid via the bare
"moe" pattern are now correctly captured in `slaap`).

### Patch 3 — Energy countersignal (v2.3)
Phrases like "energie over", "goede energie", "redelijke energie"
were marked `overig` because v2 tagged them symptoom_fysiek (via the
bare "energie") but v2.2 had no positive-energy phrase list. User
flagged these as systemisch_vermoeid counter-signals. The patch layer
adds:
- `symptom_states += symptoom_fysiek=absent`
- `polarity = positive`
- `symptoom_fysiek_subtype = systemisch_vermoeid`

**Effect**: 26 clauses upgraded from `overig` → `systemisch_vermoeid`
with state=absent.

### Patch 4 — Tintelende benen → spier (v2.2 dict)
User feedback: "not sure if tintelende benen is muscle or neuro.
maybe better under spier?" — moved.

**Effect**: `neuro` went 5 → 3 clauses; `spier` went 42 → 44.

## v2.4 patches (2026-06-11)

Three more patches landed in the same researcher-review session, after
clarification that `recovery_actie` IS the pacing category (so the
"pacing_reflectie" idea from v2 didn't need a new category — just
phrase expansion).

### Patch 5 — pacing patch (researcher correction 2026-06-11: split into 5a + 5b)

Researcher correction during the same session: **forward-looking pacing
is not pacing**. Phrases like "energie sparen" or "om donderdag energie
te hebben" are NEUTRAL NOTES (likely related to post-overdone-it
awareness), not pacing actions. Only present-tense / past-tense
rest-actions actually taken qualify as `recovery_actie`.

**Patch 5a — present-tense rest-actions taken → recovery_actie**
Dutch additions to recovery_actie scope:
- "rustdag" / "rust dag" (actual rest day taken)
- "wat geslapen" / "uur geslapen" / "even geslapen"
- "nog wel \w+ geslapen"

Logic: ADD `recovery_actie` to categories (multi-tag). Symptoom_fysiek
is NOT removed — these phrases still mention body/energy, so the
multi-tag correctly says "this clause is about taking rest AND about
energy".

**Effect**: 11 clauses got the recovery_actie tag added.

**Patch 5b — forward-looking intention → neutral_forward_looking flag**
Captured for traceability and later descriptive analysis:
- "energie sparen" / "energie proberen te sparen"
- "om energie te hebben" / "te sparen voor"
- "om morgen" / "om volgende week" / "om \w+dag"

Logic: set `neutral_forward_looking = y` column. Do NOT add recovery_actie
(it's intention, not action). Do NOT remove existing tags. This flag
makes the clauses findable for future descriptive question:
"are forward-looking pacing intentions predictive of post-overdone-it
crashes in the following days?"

**Effect**: 3 clauses got the neutral_forward_looking flag.

### Patch 6 — "redelijk" demote to neutral
v2 dictionary has `redelijk` in polarity_positive. User feedback (3
review rows): "redelijk is neutral in this case". Patch logic:
- If polarity=positive AND `redelijk` appears alone AND no
  compound-positive ("redelijk goed", "redelijk fijn", "redelijk fit",
  ...) AND no other v2 positive marker is in the clause → demote
  polarity to `neutral`.
- `redelijk goed` / `redelijk fit` etc. keep polarity=positive.

**Effect**: 34 clauses had polarity demoted from positive to neutral.

### Patch 7 — post-symptom negation
The v2 negation rule scans 3 words BEFORE a symptom phrase. Dutch
common pattern places the negation AFTER ("hoofdpijn is over",
"keelpijn weg", "geen hoofdpijn meer"). Patch scans ~4 words AFTER
each symptom phrase for: "is over", "is weg", "verdwenen",
"is voorbij", "niet meer", "geen X meer", "nog geen". When found, set
all symptoom_* states in the clause to `absent`.

**Effect**: 3 clauses had state corrected to absent via post-negation.

## File chain (after v2.2 + v2.3 + v2.4)

```
notes-categorized-v2-clauses.csv      (locked v2 output, untouched)
  -> sub_categorize_v22_fysiek.py
notes-categorized-v22-clauses.csv     (v2 + sub_type column,
                                       incorporates patches 2+4)
  -> apply_v23_patches.py
notes-categorized-v23-clauses.csv     (v2.2 + severity + countersignal
                                       + _v23_patch_applied audit)
  -> apply_v24_patches.py
notes-categorized-v24-clauses.csv     (v2.3 + pacing + redelijk
                                       + post-negation + _v24_patch_applied)
```

`notes-categorized-v24-clauses.csv` is the canonical output for all
downstream analyses (descriptive consolidation + eventual hypothesis
testing).

## Cross-references

- v2 dictionary: [category_dictionary_v2.md](category_dictionary_v2.md)
- v2 parser: [categorize_v2.py](categorize_v2.py)
- v2.2 sub-classifier: [sub_categorize_v22_fysiek.py](sub_categorize_v22_fysiek.py)
- v2.3 patch layer: [apply_v23_patches.py](apply_v23_patches.py)
- v2.4 patch layer: [apply_v24_patches.py](apply_v24_patches.py)
- Quality review prep: [prepare_categorization_quality_review.py](prepare_categorization_quality_review.py)
- Hypothesis context: timeline methodology §3a (brainfog-hidden-dip,
  muscle-pain-crash-precursor); queued_work Q1.
