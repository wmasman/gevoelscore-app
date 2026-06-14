---
description: Peer-review a methodology MD (producer-mode artefact) against CONVENTIONS §2.2's four-input bar (best-practices standards, established literature, tradeoff vision, research limitations + objectives) plus the applicable items from the 4-layer checklist. Produces a dated reasoned report in docs/research/reviews/ with the methodology- prefix. NEVER edits the target. Use when reviewing methodology/*.md.
---

# Research Methodology Review

Sister command to [`/research-review`](research-review.md). Where
`/research-review` audits **reviewer-mode artefacts** (HA results,
synthesis docs, addenda) against the 4-layer checklist, this command
audits **producer-mode methodology MDs** against the §2.2 four-input
bar that methodology MDs are themselves supposed to clear.

**Reads from**:
[../../docs/research/CONVENTIONS.md](../../docs/research/CONVENTIONS.md)
(§2.2 four-input requirement is the spine),
[../../docs/research/reviews/README.md](../../docs/research/reviews/README.md)
(the layer structure + verdict format applies adapted),
[../../docs/research/literature/methodology/README.md](../../docs/research/literature/methodology/README.md)
(the source standards), and the specific methodology MD under review.

**Why this exists**: methodology MDs are out of scope for
`/research-review` per its "Do NOT use this command for" list. But
methodology choices lock cascading downstream consequences — they
deserve a peer-review pass at their own bar. The bar is §2.2's four
inputs (best-practices standards, established literature only where
material, our own tradeoff vision, our research limitations +
objectives). The 4-layer checklist still applies in adapted form,
because methodology choices must respect the same discipline that
results are reviewed against.

## When to use

- A methodology MD has been drafted or updated and needs an
  independent §2.2 pass:
  - `docs/research/methodology/*.md`
  - `docs/research/analyses/garmin_exploration/methodology/*.md`
  - Any methodology MD elsewhere under `docs/research/`
- A methodology MD is being relied on by a downstream pre-reg or
  result and you want to audit whether the methodology choice
  itself holds before the downstream work locks.

**Do NOT use this command for**:

- HA results, synthesis docs, addenda — use [`/research-review`](research-review.md)
  instead.
- Pipeline scripts, descriptive cards, DATA_DICTIONARY edits — these
  are producer-mode but not methodology MDs; they don't have the
  §2.2 four-input bar by design.
- App-engineering methodology — use `/code-review` instead.

## Inputs

One of:

- A path: `/research-methodology-review docs/research/methodology/intervention_effects_descriptive.md`
- A relative path: `/research-methodology-review methodology/permutation_null_block_length.md`
- A methodology MD slug: `/research-methodology-review train_validate_split_fate`
- No argument → ask which MD.

If the path resolves to a non-methodology MD (a result, a synthesis,
a pipeline script), stop and route to the correct command.

---

## Phase 1: Load context

### 1.1 Read the methodology MD end-to-end

Don't skim. Note:

- **The methodological choice being locked.** Is it a null model
  construction? A phase boundary? A train/validate split? An
  operationalisation? A validation strategy? A windowing rule?
- **The framing.** Does the MD bill itself as locking the choice or
  characterising it descriptively (Layer 1 descriptive vs §2.2
  methodology MD proper)? This matters for the bar.
- **Cited standards / literature** — what's named, what isn't.
- **Sister methodology MDs** referenced — they may have been audited
  separately or jointly.
- **Columns referenced** from per_day_master.csv — note them for
  Layer 4 applicability.
- **Commit hash on disk** (`git log -1 --format=%H -- <target-path>`)
  + working-tree changes past that commit (per [`/research-review`](research-review.md)
  §1.1 honesty rule).

### 1.2 Read the supporting context

For a methodology MD:

- Any sister methodology MD it cites or is cited by (cross-reference
  consistency).
- The downstream analyses / pre-regs / results that depend on this
  choice — if any are already in flight, the methodology fire
  cascades.
- The audit script if one exists (`docs/research/pipeline/...`).
- The relevant chapters in [`docs/research/literature/methodology/`](../../docs/research/literature/methodology/)
  — SCRIBE, CENT, STROBE, Daza, WWC, Natesan — to know what
  state-of-art the MD should be measuring against.

If the methodology MD addresses a question with an established
state-of-art (intervention effects → ITS; block bootstrap → Politis
& Romano / Künsch; phase boundaries → change-point detection;
multiplicity → BH / Holm / effective N), confirm you know the
state-of-art *before* writing the review. See "State-of-art pointers"
at the end of this file for common question types.

### 1.3 Re-read CONVENTIONS §2.2

Open [../../docs/research/CONVENTIONS.md](../../docs/research/CONVENTIONS.md)
§2.2 and confirm the four inputs are fresh in mind:

1. Best-practices standards in time-series research, statistics,
   and our subdomain. Anchor to current state of the art, not
   historical convention.
2. Established literature, cited only where the reference
   materially supports the choice. Each citation gets a sentence on
   what it actually contributes.
3. Our own vision on tradeoffs. Which dimension is being weighted
   and why.
4. Our research limitations + objectives. n=1, single-subject,
   observational, multi-source.

The spine of Phase 2 walks these four inputs.

---

## Phase 2: Walk the §2.2 four-input bar + applicable layer items

### Spine — §2.2 four-input bar

Each input is a fire-able check. Magnitudes: *minor* (a wording
fix), *substantive* (the choice's defensibility is weakened),
*blocking* (the choice may not hold at all).

**I1 — Best-practices standards**

- I1.1 — Is the state-of-art for the question this MD addresses
  *named*? (e.g. ITS for intervention effects, change-point for
  boundaries, BH/Holm for multiplicity).
- I1.2 — Is it adopted, or explicitly rejected with reason? Either
  is fine; silence is the fire.
- I1.3 — If adopted, is the standard's published guidance honoured
  in the operationalisation (e.g. ITS includes both level-change
  β2 and trend-change β3; permutation null uses a block length
  matched to autocorrelation)?
- I1.4 — If rejected, is the reason tied to the corpus's specific
  constraints (n=1, observational, etc.) rather than convenience?

**I2 — Established literature**

- I2.1 — For each material choice (threshold, window width,
  cutoff, method), is there relevant literature?
- I2.2 — Where literature is cited, is the citation *material*
  (the paper's reasoning or evidence supports the choice) or
  *ornamental* ("they did it that way")? Ornamental cites are a
  fire per §2.2's "never cite a paper because they did it that way".
- I2.3 — Where the choice has clinical / pharmacological /
  physiological grounding (e.g. transition buffers around drug
  start, autonomic effects of CPAP), is the relevant literature
  named?
- I2.4 — Where literature exists but isn't consulted, fire (with
  the specific paper that would have helped).

**I3 — Tradeoff vision**

- I3.1 — For each binary or multi-way choice (which test, which
  window, which baseline), are the alternatives named?
- I3.2 — Is the chosen path's tradeoff explicit (reproducibility
  vs honesty about n, power vs Type-I control, simplicity vs
  per-metric tailoring)?
- I3.3 — Are the rejected alternatives' weaknesses tied to the
  specific question, not boilerplate?
- I3.4 — Implicit tradeoffs are a fire. The whole point of §2.2
  is that picking from a binary list in chat is the failure mode.

**I4 — Research limitations + objectives**

- I4.1 — Is n=1 acknowledged where it bites (effective sample
  size, power, generalisability claim)?
- I4.2 — Is the observational design acknowledged (no
  randomisation, confounding by unmodeled co-occurring events)?
- I4.3 — Is the corpus-specific objective stated (descriptive vs
  inferential vs decision-gating)?
- I4.4 — Are corpus-specific constraints (LC recovery trajectory,
  device-change-free FR245 throughout, single-rater triage,
  retrospective coding) acknowledged where they affect the choice?

### Applicable layer checks (adapted from `/research-review`)

Not all layer items translate to methodology MDs. Walk the ones
that do.

#### Layer 1 — Discipline gates (inherits from CONVENTIONS §2.1, §4.1-§4.3)

- L1.1 — **§2.1 descriptive-before-inference**: does this MD lock
  inferential machinery before descriptive characterisation is
  complete? A methodology MD for a confirmatory test is a fire if
  the gating descriptive work isn't done.
- L1.2 — **§4.1 no interpretive marks**: does the measurement
  procedure bake an imputed mechanism into a measurement (e.g.
  "stress-stuck = sympathetic dysregulation" instead of just
  defining the operational measurement)?
- L1.3 — **§4.2 caveats vs a-priori**: does the methodology
  choice presuppose what it's measuring (e.g. naming a "phase"
  before the existence of phases has been characterised)?
- L1.4 — **§4.3 prior-driven framing**: is the framing aligned
  with the methodology question's prior source? A
  literature-grounded methodology can be framed confirmatorily; a
  corpus-derived one needs descriptive framing.

#### Layer 2 — Observational n=1 (inherits from Daza 2018)

- L2.1 — Within-subject counterfactual framing for the
  measurement procedure stated?
- L2.2 — Stationarity assumption acknowledged where the
  methodology assumes pre/post or train/validate samples are
  exchangeable?
- L2.3 — Calendar-time vs subject-time framing clear?
- L2.4 — Data provenance for the choice's inputs (which version
  of which column, which extract date) traceable?

#### Layer 3 — Time-series specific (inherits from Natesan 2023 / WWC / CENT)

These bite hardest on analysis-method methodology MDs.

- L3.1 — **Autocorrelation**: does the chosen method address
  serial dependence? Mann-Whitney U / t-test on day-level series
  assumes independence and is a fire if not justified.
- L3.2 — **Lag-carryover / window sizing**: if the method
  involves pre/post windows, transition buffers, or lead-up
  windows, are they sized appropriately for the corpus's
  carryover (drug pharmacokinetics, PEM lag, etc.)?
- L3.3 — **Multiplicity**: if the methodology produces multiple
  sub-tests, is the correction policy named?
- L3.4 — **Level vs trend**: where relevant, does the method
  distinguish a level step from a slope inflection?
- L3.5 — **State-of-art for the specific time-series question**:
  is the discipline-specific best-practices method named?

#### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3)

Walk only the items that apply to the methodology choice.

- L4.1 — §3.1 personal baseline.
- L4.2 — §3.2 lagged-lcera variant where the MD touches
  PEM-pacing columns.
- L4.3 — §3.3 one column per definitional pair where the MD
  selects columns.
- L4.4 — §3.4 crash-drop sensitivity where the MD specifies
  correlation / regression.
- L4.5 — §3.5 spike-detecting metrics for acute-arousal
  measurements.
- L4.6 — §3.6 named counts in any descriptive output the MD
  produces.

#### Methodology-specific elements (Type A: by MD type; Type B: cross-cutting)

This is where the §2.2 spine and the layer checks get teeth on
specific methodology machinery. Identify the MD's type from the
list below and walk the type-specific checks; then walk the
cross-cutting checks regardless of type.

##### Type A — By methodology MD type

**A1. Phase boundary / regime segmentation MD** (e.g.
`lc_era_temporal_segmentation`, `intervention_baseline_segmentation`)

- A1.1 — Each boundary date traceable to a documented source
  (calendar event, intervention onset, hardware change)?
- A1.2 — Change-point detection (PELT [Killick 2012], Bayesian
  online [Adams & MacKay 2007]) named — adopted or rejected with
  reason? Visual-inspection-only is fine at n=1 but the algorithmic
  alternative should be named and rejected explicitly.
- A1.3 — Boundary effect on downstream analyses traced (which
  pre-regs, results, columns inherit the segmentation)?
- A1.4 — Sensitivity to ±N days around proposed boundary specified
  as an output column or sweep?
- A1.5 — Transition / washout windows justified by carryover
  literature (drug pharmacokinetics, intervention onset literature),
  not arbitrary?

**A2. Null model / permutation MD** (e.g.
`permutation_null_block_length`)

- A2.1 — Block length specified with reasoning?
- A2.2 — Block bootstrap variant named (moving-block [Künsch 1989],
  stationary [Politis & Romano 1994], circular)?
- A2.3 — Number of permutations specified (≥1000 for descriptive,
  ≥10000 for confirmatory)?
- A2.4 — Exchangeability conditions checked (Chung & Romano 2013)?
- A2.5 — Block-length sensitivity sweep planned (typically 5d / 7d
  / 14d on PEM-pacing data)?
- A2.6 — Effective sample size computed under the autocorrelation
  structure, not n raw?

**A3. Train/validate split MD** (e.g. `train_validate_split_fate`)

- A3.1 — Split date justified or, if pre-spec, source of pre-spec
  documented?
- A3.2 — Walk-forward / blocked-CV considered (Bergmeir & Benítez
  2012) and adopted or rejected with reason?
- A3.3 — **Continuous-awareness leakage** explicitly addressed —
  the subject has been *living through* the post-split window;
  per `project_garmin_research_bias_boundary`, the held-out
  framing must distinguish tactical-vs-analytical use, not regress
  to "user has been continuously analysing the data"?
- A3.4 — Both-eras rule vs single-pool framework named?
- A3.5 — M3-style descriptive overlay (train-vs-validate
  discrimination as a *number, not a narrative*) handled in line
  with the framing memory?

**A4. Operationalisation MD** (how to compute a specific column —
e.g. `lagged_baseline`, `severity_spec`, `hrv_proxy_via_stress`)

- A4.1 — Window length + reference window stated as concrete
  parameters?
- A4.2 — Personal baseline (z-score / percentile rank), not
  absolute thresholds (CONVENTIONS §3.1)?
- A4.3 — Lagged baseline (`_lagged_lcera`) used where applicable
  (CONVENTIONS §3.2)?
- A4.4 — Carryover / transient handling spec'd (buffer days,
  exclusion windows)?
- A4.5 — NaN policy on missing data (drop, impute, gate on
  `_valid_flag`)?
- A4.6 — Sensitivity to choice via the `_lagged` vs
  `_lagged_lcera` variant family, or to window-length sweep?
- A4.7 — If the column is presence-conditioned (v24-derived,
  per_day_intensity), is the `has_note` / `intensity_source`
  companion required (CONVENTIONS §4.4)?

**A5. Effect-size / metric choice MD**

- A5.1 — Effect-size measure named (Cohen's d, Hedges' g for
  small N, Tau-U, NAP, IRD, log-response-ratio for SCED) —
  WWC 2022 SCED Handbook §V is the menu.
- A5.2 — CI method named (parametric, bootstrap, bias-corrected
  bootstrap)?
- A5.3 — Autocorrelation accounted for in the CI (effective N or
  block bootstrap)?
- A5.4 — Small-N correction applied (Hedges' g over Cohen's d at
  n < 20)?

**A6. Threshold / cutoff rescue MD** (e.g.
`threshold-sweep-rescue-criteria-v2`)

- A6.1 — Source of threshold (external population literature,
  project-derived calibration, mechanistic literature)?
- A6.2 — Pre-spec of rescue criteria (when does a near-miss survive
  / die)?
- A6.3 — Symmetric application — same criteria applied to all
  tests in the family, not selectively to ones the analyst likes?
- A6.4 — v1 → v2 methodology revision: is the v1 defect named, the
  v2 fix anchored, the symmetric re-application discipline
  documented?

**A7. Intervention-effect MD** (e.g.
`intervention_effects_descriptive`)

- A7.1 — Interrupted Time Series (ITS) [Bernal et al. 2017 BMJ]
  named — adopted (with β2 level + β3 trend), or rejected for
  descriptive purposes with reason?
- A7.2 — Pharmacokinetic literature cited for transition-window
  width (SSRI steady-state ~7-10d; clinical effect 2-4w; CPAP
  autonomic effects within 2-4w per Marin 2010)?
- A7.3 — Confounder enumeration covers: (a) other concurrent
  interventions, (b) the LC recovery trajectory documented in
  `registry.md`, (c) seasonality, (d) device-change (none on
  FR245), (e) life events not in corpus?
- A7.4 — Sensitivity to underlying trend (detrend before window
  comparison, or use a long pre-window that captures slope)?
- A7.5 — Blinded coding for any human-judgement step
  (transition_shape, near-miss-classification)?
- A7.6 — Pre-spec of "no visible change" criterion (rule, not
  rater intuition)?
- A7.7 — Outcome-contamination check separate from
  baseline-channel check (the §3 / §3b distinction in the
  worked-example MD)?

**A8. Validation framework MD** (e.g.
`wiggers_test_design_on_chained_regime`)

- A8.1 — Faithfulness rubric per claim type (CCF lead-lag /
  within-event / dose-response / non-linearity)?
- A8.2 — Chained-regime adjustment specified (correction for
  family-wise multiplicity across chained tests)?
- A8.3 — Operationalisation classes mapped to source-doc claim
  types (Wiggers' verbatim phrasing → our operational measure)?
- A8.4 — Cross-cutting statistical hygiene (multiplicity method,
  block length, etc.) referenced from sister methodology MDs?

##### Type B — Cross-cutting methodology elements (every MD)

Walk these regardless of MD type:

- **B1. Pre-spec of "no finding" criterion** — what would make
  the analyst stop pursuing the question? Without this, motivated
  drift is invisible.
- **B2. Sensitivity sweep on key parameters** — at least one
  parameter (window width, threshold, baseline length) tested
  across a small grid so the result's robustness to the choice
  is visible.
- **B3. Confounder enumeration specific to this corpus** — not
  boilerplate. Must name: LC recovery trajectory (registry.md
  documents ~10/year → ~2/year crash drop), seasonality
  (winter blues / hayfever / daylight), device-stability (FR245
  throughout — no device-change confound here), calendar-coverage
  gaps, life-events-outside-corpus, tracking-compliance dropping
  during crash periods.
- **B4. Stationarity assumption acknowledged** — even when the
  method doesn't formally check stationarity, the violation
  consequence must be stated.
- **B5. Autocorrelation handling** — block bootstrap, Newey-West
  HAC SE, AR-corrected effective N, or explicit acknowledgment
  that p-values are inflated. Silent i.i.d. assumption on
  day-level data is the Natesan Batley 2023 failure mode (83.8%).
- **B6. Multiplicity policy** — if the MD spawns multiple
  sub-tests (channels × interventions, lags × thresholds), the
  correction is named (BH FDR / Holm step-down with effective N
  per the chained-regime MD).
- **B7. Effect size + CI together** — never report a p-value
  without an effect-size estimate with CI. p-value alone is the
  Natesan 2023 65.8% distributional-assumption failure mode.
- **B8. Visual + statistical paired** — at n=1 SCED, visual
  inspection is primary (WWC); statistical is corroborating, not
  replacing. An MD that's all numerical or all visual is weaker
  than one that pairs them.
- **B9. Causal language honestly distinguished from correlational**
  — descriptive MDs report co-occurrence; causal claims require
  the explicit hypothesis-testing layer (CONVENTIONS §4.1).
- **B10. Reproducibility hook** — script path, output path, seed
  (where relevant), data-source path. The MD should be runnable
  from its own spec.

#### Side observations

Same shape as `/research-review` Phase 2 side-observations: numerical
inconsistencies, broken cross-refs, stale citations. Prefix `**Side**`.

---

## Phase 3: Compose the 5-section reasoned body

Same five sections as `/research-review` Phase 3, retuned for methodology
MDs:

### Section 1 — What the MD specifies

Restate the methodological choice in plain terms. One paragraph.
What is being locked? Under what framing (Layer 1 descriptive vs
methodology-MD-proper)? What downstream artefacts depend on this
choice?

### Section 2 — What fired and why

Grouped by:

- **Spine: §2.2 four-input bar** (I1.x, I2.x, I3.x, I4.x fires)
- **Layer 1** discipline gates
- **Layer 2** observational n=1
- **Layer 3** time-series specific
- **Layer 4** project audit hooks
- **Side observations** (optional)

For each fire: rule line, the specific reading that triggered it,
magnitude (minor / substantive / blocking), and a sentence on *why
the convention or standard exists* with citation where applicable.

Order within section by magnitude.

### Section 3 — What does not fire (selective)

Non-trivial passes only. Examples:

- "I3 tradeoff vision passes on the 3-phase citalopram decision
  — sub-truncation rationale stated, alternatives (6 dose steps,
  1 umbrella boundary) explicitly rejected with reason."
- "L1.3 (caveats vs a-priori) passes — MD explicitly cites §4.2
  and stays in caveat mode throughout."

Skip trivial passes. Padding dilutes signal.

### Section 4 — What would strengthen this MD

Constructive close. Concrete, named, ideally pointing at:

- A specific paper to cite (with what it materially contributes
  to the choice).
- A specific state-of-art method to adopt or to explicitly reject.
- A specific corpus-confound to acknowledge.
- A specific sensitivity analysis or sensitivity column to add.

Format each suggestion:

- The specific addition / revision.
- The convention or standard or paper it inherits from.
- The expected effect on the choice's defensibility.

Bad: "Consider citing the literature."
Good: "Cite Bernal et al. 2017 BMJ ITS guidance in §1, naming
segmented regression as the state-of-art alternative being deferred
to the follow-up segmentation MD — closes the I1.1 fire and signals
that the level-only Mann-Whitney is a deliberate descriptive choice
rather than methodological unawareness."

### Section 5 — Verdict + one-sentence reasoning

Three-tier:

- **DEFENSIBLE** — §2.2's four inputs are adequately addressed; the
  applicable layer checks are clean. The choice can lock as
  specified.
- **DEFENSIBLE with revision** — substantive fires require
  disclosure or minor revision, but the methodology doesn't
  collapse. Lock with the suggested revisions folded in.
- **REVISIT** — substantive fires suggest the choice may not
  survive a §2.2 pass as currently specified. Sit with the fires
  before locking; consider re-specifying.

The label is never the body. The one-sentence reasoning names the
highest-priority §2.2 input or layer fire (or, for DEFENSIBLE, the
strongest evidence the bar was cleared).

---

## Phase 4: Write the report

Target path:

```
docs/research/reviews/methodology-<md-slug>-YYYY-MM-DD.md
```

The `methodology-` prefix distinguishes these from peer-review
reports (which use `<target-id>-YYYY-MM-DD.md` directly).

### Report skeleton

```markdown
# Methodology review: <MD title> (methodology/<md-slug>.md)

**Target**: [path/to/methodology.md](../methodology/<md-slug>.md)
**Target commit**: <hash> (`git rev-parse --short HEAD` at the time of
review, or working-tree-state with date + scope per Phase 1.1)
**Reviewer mode**: Claude (independent methodology peer reviewer
per CONVENTIONS §1.2; producer-mode MD under §2.2 four-input bar)
**Review date**: YYYY-MM-DD

## 1. What the MD specifies

<one paragraph: what's being locked, under what framing, what
downstream artefacts depend on this choice>

## 2. What fired and why

### Spine — §2.2 four-input bar (inherits from CONVENTIONS §2.2)

#### I1 — Best-practices standards

<fires grouped here, or "no fires">

#### I2 — Established literature

<fires here, or "no fires">

#### I3 — Tradeoff vision

<fires here, or "no fires">

#### I4 — Research limitations + objectives

<fires here, or "no fires">

### Layer 1 — Discipline gates (inherits from CONVENTIONS §2.1, §4.1-§4.3)

<fires, or "no fires">

### Layer 2 — Observational n=1 (inherits from Daza 2018)

<fires, or "no fires">

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

<fires, or "no fires">

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3)

<fires, or "no fires">

### Side observations (optional)

<one-line items prefixed **Side**; omit subsection if none>

## 3. What does not fire (selective)

<non-trivial passes only>

## 4. What would strengthen this MD

<concrete, named, with expected effect>

## 5. Verdict

**<DEFENSIBLE / DEFENSIBLE with revision / REVISIT>** — <one
sentence naming the highest-priority §2.2 fire (or strongest
evidence for DEFENSIBLE)>.

---

## Methodology

This methodology review walks CONVENTIONS §2.2 four-input bar plus the
applicable items from the 4-layer checklist defined in
[../reviews/README.md](README.md), anchored in:

- SCRIBE 2016 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/))
- CENT 2015 ([shamseer_2015_cent_consort_nof1.pdf](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf))
- STROBE 2007 ([vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf))
- Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf))
- WWC 2022 SCED standards ([wwc_2022_standards_handbook_v5_0.pdf](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf))
- Natesan Batley 2023 ([natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf))

Plus the state-of-art literature specific to this methodology
question (named in Section 2's I1 / I2 cells with material citation).

Project-specific audit hooks from [../CONVENTIONS.md](../CONVENTIONS.md)
§2.2 (four-input bar), §2.1 / §3 / §4 (discipline gates + audit hooks
that apply to methodology choices).
```

### Writing rules

- Quote sparingly. One short quote per fire is enough.
- Cite paragraph references in the target MD by section number,
  never by fuzzy paraphrase.
- For column references, link to DATA_DICTIONARY.
- For state-of-art methods, name the method + the canonical
  citation in I1 / I2 cells. Without a name, the fire is just
  "feels under-specified" rather than auditable.

### Do NOT

- Edit the methodology MD. Even for typos. The role-split holds
  for methodology MDs even though they're producer-mode — review
  recommendations land in Section 4, not in the target file.
- Overwrite an existing methodology review at the same target-date
  path. Append `-v2` if reviewing the same MD on the same day.
- Produce a label-only verdict.

---

## Phase 5: Report back in chat

- Filename + size.
- Verdict label + the Section 5 sentence.
- Highest-priority §2.2 input fire (or "all four pass" if so).
- Highest-priority layer fire per layer that fired (one line each).
- A reminder that the user (or the producer agent) acts on the
  *body* — not the label — to revise the methodology MD.

If the review surfaces a structural concern about the
methodology-review process itself (e.g. a new state-of-art
question type that isn't in the pointers below), flag it as a
final paragraph to the user, not by editing this command file or
CONVENTIONS on the spot.

---

## Anti-patterns to avoid

- Reviewing the methodology MD against the *hypothesis-test bar*
  instead of the *methodology bar*. The spine is §2.2 four inputs,
  not the 3-criterion (frequency / discrimination / magnitude)
  bar from HA pre-regs.
- Treating ornamental citations as I2 passes. "Wiggers said X"
  isn't material; "Wiggers said X *because of* Y *and Y supports
  our choice because of* Z" is material.
- Letting a "Layer 1 descriptive" framing absolve §2.2 entirely.
  The four-input bar is lower for a descriptive MD (objectives in
  I4 weigh more, standards in I1 weigh less) but not zero. The
  intervention-effects MD is the worked example.
- Demanding randomisation, control groups, or large-N
  power-calculations from an n=1 corpus. The bar adjusts for the
  design.
- Skipping the state-of-art name. If you don't know what the
  state-of-art is for the methodology question, *figure it out
  before writing the review*. See pointers below.
- Editing the methodology MD silently. Recommend in Section 4;
  let the producer agent (or the user) revise.

---

## State-of-art pointers by methodology question type

When the methodology MD addresses one of these common questions,
the relevant state-of-art literature is named below. Use this to
confirm I1 / I2 fires.

| Methodology question | State-of-art (named in I1) | Canonical reference |
|---|---|---|
| Observational intervention effect on a single subject | Interrupted Time Series (ITS) with segmented regression — pre-intervention level + pre-intervention trend + level change β2 + trend change β3 | Bernal, Cummins, Gasparrini 2017 *Int J Epidemiol* (BMJ guidance); Wagner et al. 2002 *J Clin Pharm Ther*; Cochrane EPOC ITS guidance |
| Block bootstrap / block length selection | Moving-block bootstrap (Künsch 1989), stationary bootstrap (Politis & Romano 1994), block-length selection (Politis & White 2004) | [kunsch_1989_jackknife_bootstrap_stationary.pdf](../../docs/research/literature/methodology/kunsch_1989_jackknife_bootstrap_stationary.pdf), [carlstein_1986_subseries_variance.pdf](../../docs/research/literature/methodology/carlstein_1986_subseries_variance.pdf) |
| Permutation test validity under serial dependence | Exchangeability conditions for permutation tests | [chung_romano_2013_permutation_tests.pdf](../../docs/research/literature/methodology/chung_romano_2013_permutation_tests.pdf) |
| Phase / regime boundary detection in time series | Change-point detection — PELT (Killick et al. 2012), Bayesian online (Adams & MacKay 2007), `ruptures` library | Killick, Fearnhead, Eckley 2012 *JASA*; Adams & MacKay 2007 *arXiv* |
| SCED effect size (for graphical / non-parametric data) | Tau-U (Parker), NAP, IRD, log-response-ratio | WWC 2022 SCED Standards Handbook §V; Parker, Vannest, Davis 2011 |
| Multiplicity correction across families of tests | Benjamini-Hochberg FDR; Holm step-down; effective N for correlated tests | Benjamini & Hochberg 1995; Holm 1979; project's own `methodology/wiggers_test_design_on_chained_regime.md` § Cross-cutting statistical hygiene |
| Train / validate / cross-validation in time series | Blocked time-series CV; walk-forward; no shuffle in time. Avoid hold-out leakage from continuous-awareness subjects | Bergmeir & Benítez 2012; project's own `methodology/train_validate_split_fate.md` |
| Observational confounding in n-of-1 self-tracking | Counterfactual framework (Daza 2018); stationarity assumption check; explicit confounder enumeration | [daza_2018_self_tracked_n_of_1_counterfactual.pdf](../../docs/research/literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) |
| Drug-effect transition windows (pharmacokinetics) | Drug-specific steady-state literature; class-effect autonomic literature | SSRI / citalopram autonomic: Licht et al. 2010; Kemp et al. 2010 *Biol Psychiatry*. CPAP autonomic: Marin et al. 2010 *Lancet*; Tantucci et al. 2003 *Chest* |
| Sleep architecture under intervention | Sleep medicine reference + AASM scoring conventions | Berry et al. AASM Manual; intervention-specific (SSRI: Wichniak et al. 2017; CPAP: extensive) |
| Operationalisation choice (composite vs per-axis, mean vs spike) | Project-internal precedent + measurement-theory principles | `methodology/wiggers_test_design_on_chained_regime.md`; `methodology/permutation_null_block_length.md` |

For methodology questions not in this table: do a focused literature
search (1-2 keyword searches via WebSearch) before writing the
review. Name the state-of-art you found, even if it doesn't fit the
n=1 corpus cleanly — the review's job is to make the adaptation
explicit, not to claim the question is uncharted.

If you discover a methodology question type that recurs across
multiple reviews, surface to the user — it belongs in this table.

---

## Worked example

Target: `docs/research/methodology/intervention_effects_descriptive.md`

Review path: `docs/research/reviews/methodology-intervention_effects_descriptive-2026-06-14.md`

Phase 1 finds: a Layer 1 descriptive MD for pre-vs-post window
comparison around documented interventions (citalopram, CPAP,
ergotherapie). Mann-Whitney U with 14-day transition buffer,
neighbour-truncated windows, human-coded transition shape.

Phase 2 fires (highlights — full review elsewhere):

- **I1 substantive** — Interrupted Time Series (ITS) with segmented
  regression is the state-of-art for observational intervention
  effects (Bernal et al. 2017 BMJ). MD does not name ITS or justify
  Mann-Whitney U as a deliberate descriptive simplification.
- **I2 substantive** — CPAP autonomic effects (Marin 2010) and SSRI
  autonomic effects (Licht 2010) are documented per channel; MD
  says "plausibly affected" without citation.
- **L1.4 substantive** — Underlying recovery-trajectory confound on
  this corpus (crash frequency ~10/year → ~2/year across the
  2024-Q1 intervention window) not acknowledged. Mann-Whitney U
  will read trajectory as step-change.
- **L3.1 substantive** — Mann-Whitney U on day-level series assumes
  independent observations; days are autocorrelated. The Natesan
  Batley 2023 failure mode (83.8%).
- **L3.4 substantive** — Method is level-only; cannot distinguish
  level shift from slope inflection.

Phase 3 verdict: REVISION RECOMMENDED — §2.2 inputs I1 + I2 are
absent, but the descriptive framing partly absolves them; the
underlying-trajectory confound is the highest-priority methodological
gap on this corpus specifically.

Phase 4 writes the file. Phase 5 reports back in chat with the
verdict + I1 / I2 / L1.4 / L3.1 / L3.4 one-liners.

---

## Cross-references

- [`/research-review`](research-review.md) — sister command for
  reviewer-mode artefacts (HA results, syntheses).
- [reviews/README.md](../../docs/research/reviews/README.md) — layer
  structure + verdict format (peer-review version; methodology
  reviews adapt it).
- [CONVENTIONS.md §2.2](../../docs/research/CONVENTIONS.md) — the
  four-input requirement methodology MDs are supposed to clear.
- [literature/methodology/README.md](../../docs/research/literature/methodology/README.md)
  — local PDFs of the standards.
