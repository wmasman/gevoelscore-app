# Verdict to inference — Stage I guide

**Status**: **LOCKED r2** by user acceptance 2026-06-24. r1 authored
2026-06-24 by a fresh agent per §11 step 6.2 of
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
(r5 LOCKED 2026-06-24). r1 → r2 absorbed a fresh-session
`/research-methodology-review` (verdict REVISION RECOMMENDED (mild),
report at
[`reviews/methodology-verdict_to_inference-2026-06-24.md`](../reviews/methodology-verdict_to_inference-2026-06-24.md))
that caught two required actions (R1: §4.6 agreement-direction
smuggling gap — agreement does not strengthen §3 licensed claim;
R2: §5.5 triad-derived/k-of-N qualifier handling — carry forward
verbatim) and four recommended actions (HA-C3p seed-notes pointer;
L4 meta-recursion paragraph in §4.6; §4.9 fourth refusal path
PROVISIONAL-not-yet-accepted; §4.3-§5 compression — last declined
for r2 preserving operational detail). All required + 3 of 4
recommended absorbed in r2. Implementation proceeds to §11 step 6.3
(guide #3 `internal_synthesis.md`).

This guide is the second of six binding methodology MDs for the
results-analysis layer. It governs **Stage I** (verdict-to-inference):
the per-HA artefact that translates a verdict label (REJECTED /
SUPPORTED / PARTIAL / INCONCLUSIVE, plus the triad-derived
verdicts the result.md ontology emits, e.g. HA-C4 v2's INCONCLUSIVE-
aware triad sum and HA11-bout-redo's "k-of-3 framework-validity bars
met") into a substantive claim about the hypothesis itself, the
operationalisation it was tested under, and the systemic envelope that
limits how far the claim reaches. It sits between Stage D's
`descriptive_audit.md` (the verdict-trust gate) and Stage S₁'s
`cluster-*.md` (the per-cluster coherence call). It refuses to start on
an HA whose Stage D audit is missing or REQUIRES-DESCRIPTIVE-WORK.

---

## 1. Purpose

> **A verdict label is not a finding. Stage I pins the verdict-to-
> claim mapping so interpretations across the corpus are
> commensurate.**

SUPPORTED does not mean "the hypothesis is true." REJECTED does not
mean "the hypothesis is false." PARTIAL does not mean "weak
SUPPORTED." INCONCLUSIVE does not mean "next time we'll see." Each
verdict label maps to a constrained inferential claim about the
hypothesis as it was tested — and to a larger set of claims it does
*not* license. Without an explicit guide that pins those mappings, the
same verdict gets translated three different ways by three different
sessions, and the layer's outputs stop being commensurable across HAs.

Stage I is the per-HA discipline gate that closes that drift. Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md) §3
stage-map: `D → I → S₁ → S₂ → A → T`. Stage I sits immediately
downstream of Stage D and immediately upstream of Stage S₁. Stage S₁
refuses to start on a cluster whose constituent HAs lack current
`interpretation.md` artefacts; every downstream synthesis,
contextualisation, actionability, and translation artefact builds on
the claim shapes Stage I produces. Stage I's commensurability across
HAs is the foundation that lets S₁ produce coherence calls that mean
the same thing across clusters.

**What Stage I does NOT do.**

- It does NOT re-test the hypothesis. The verdict comes from
  `result.md` and is copied verbatim; Stage I does not relabel, does
  not re-score, does not re-run.
- It does NOT produce predictive claims. The hard predictive gate in
  [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  §3.10 binds: predictive-tier claims live at Stage A and require a
  pre-registered forward-validation HA. Stage I produces no PPV, no
  base-rate framing, no diagnostic-quality measures, and no "forecasts
  Y" wording. The forward pointer is Stage A; this is not Stage I's
  surface.
- It does NOT carry subject-narrative commentary. Per
  [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  §3.12, commentary lives at Stage A `construct-*.md` (attached to
  tier-1 or tier-2 formal claim) and Stage T patient-audience-track
  only. Stage I artefacts are forbidden from carrying §3.12
  commentary. The lived-experience prior reconciliation in §4.6 of the
  Stage I outline below is **not** §3.12 commentary — it is the
  recording of a prior against the verdict with no auto-resolution
  (see §4.6 and §6.1 below for the operational distinction).
- It does NOT invent new caveats post-hoc. Stage I draws caveats from
  the Stage D `descriptive_audit.md` (load-bearing-assumption status,
  PROVISIONAL-flag if applicable) and from the HA pre-reg's own §8
  caveat list. New caveats invented at Stage I time — caveats that
  appear neither in pre-reg §8 nor in the audit — are forbidden by
  the anti-pattern §7.5 below.
- It does NOT re-frame the hypothesis. The pre-reg's §1 / §2 claim
  language is the binding statement of what the hypothesis was; Stage
  I does not paraphrase it into something more convenient for the
  verdict.

**Alternatives considered** (per CONVENTIONS §2.2 four-input bar
item 3: tradeoff vision). The natural alternative is to fold the
verdict-to-inference translation into each HA's `result.md` as a
self-contained §-Interpretation section. That was rejected for the
same two reasons guide #1 cited for descriptive backstop: (a)
self-interpretation by the same session that ran the test is
structurally weaker than a separate translation step (same-session
blind spots — the L4 limitations-doc mitigation reach applies), and
(b) per-HA self-interpretation makes commensurability across HAs
harder — the same verdict-to-claim mapping rules applied uniformly
across the corpus is the cheap commensurate discipline. A second
alternative — collapsing Stage I into Stage S₁ and producing only
cluster-level interpretation artefacts — was rejected because single-
HA clusters (per the synthesis-structure map at
[`synthesis_structure_map.md`](synthesis_structure_map.md)) would
otherwise skip the verdict-to-claim discipline entirely, and because
the per-HA interpretation surface is what downstream Stage S₂ and
Stage A artefacts cite when they need to point at a specific HA's
claim shape rather than at a cluster aggregate. The per-HA artefact
pattern matches the Stage D audit shape and the limitations and map
shapes: one MD per binding artefact, lock log per revision.

**Precondition: the `/research-interpret` skill must land first.**
This guide specifies *what* a Stage I interpretation must do; it does
not specify *how* the skill produces one. Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§11 step 7, the `/research-interpret` skill is built after the six
guides (this guide is #2 of six). **No Stage I interpretation
artefact can be drafted before §11 step 7 lands** — this guide alone
is necessary but not sufficient. The §9 agent-instruction outline
below is the skill's brief; the skill build (step 7) operationalises
it.

## 2. Inputs

The interpretation MUST load and use the following inputs, in this
order:

1. **The target HA's locked `hypothesis.md`** — in particular §1 / §2
   (the predicted-direction claim, the binding statement of what the
   hypothesis is), §4 (operationalisation; what test was actually
   run), §7 (locked-decisions block where present), §8 (caveats; the
   pre-reg's own self-declared narrowing). The pre-reg's §1 / §2
   language is what Stage I translates the verdict against; Stage I
   does not paraphrase or reframe.
2. **The target HA's locked `result.md`** — the headline verdict
   (verbatim; no relabeling), the per-cell statistics on the primary
   surface, any §-routing language the result emitted (e.g., HA-C4 v2
   §5.3's INCONCLUSIVE-aware triad sum routing producing REJECTED at
   triad-sum 0.0; HA-C3 v2's wrong-direction-override REJECTED;
   HA-C3p's "2-of-3 conditions MET" PARTIAL; HA11-bout-redo's "k-of-3
   framework-validity bars met" PARTIAL). The verdict label is the
   single string Stage I copies; the §-routing language is the
   per-channel / per-condition detail that Stage I's §3 ("what the
   verdict licenses") must respect when characterising the claim
   shape.
3. **The Stage D `descriptive_audit.md`** — for the same HA, under
   [`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
   §3 folder convention at
   `analyses/descriptive/HA-XX/descriptive_audit.md`. The audit's §4
   verdict-trust call is the binding gate per §6.2 below: TRUSTED
   unblocks; DOWNGRADED-INCONCLUSIVE-PROVISIONAL unblocks under
   explicit user acceptance of the PROVISIONAL flag carrying forward;
   REQUIRES-DESCRIPTIVE-WORK and STRUCTURALLY-UNTESTABLE-AS-
   CURRENTLY-SPECIFIED block. The audit's §3 per-assumption status
   rows and §5 `open_inputs` entries feed Stage I's §4.5 caveats
   section and §4.9 `open_inputs` carry-forward.
4. **The layer-level
   [`research_line_limitations.md`](research_line_limitations.md)** —
   in particular §3 (the seven L-IDs L1-L7) and §5 (citation
   requirements). The Stage I `interpretation.md` MUST cite every L-ID
   that touches the HA's primary signals or operationalisation, listed
   by L-ID with one-sentence project-specific application (see §3 and
   §4.5 below).
5. **The synthesis-structure map
   [`synthesis_structure_map.md`](synthesis_structure_map.md)** — in
   particular the §3 cluster row the HA participates in (the
   per-cluster L-IDs column tells Stage I which L-IDs the HA's
   downstream S₁ work will need; Stage I aligns its own §4.5 citation
   list with this), and the §4 topic row the cluster feeds (for the §8
   cross-references section pointing forward).
6. **CONVENTIONS** — in particular [§1](../CONVENTIONS.md#1-roles)
   (the reviewer-mode-with-authorization mode this artefact carries
   per
   [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
   §4 producer/reviewer split table); [§2.1](../CONVENTIONS.md#21-descriptive-before-inference)
   (descriptive-before-inference; Stage D gate inherits this);
   [§4.1](../CONVENTIONS.md#41-no-interpretive-marks-on-raw-layers)
   (no interpretive marks on raw descriptive layers — Stage I is the
   stage where interpretation enters the corpus, but it cites the raw
   descriptive layers without overlaying marks back onto them);
   [§4.2](../CONVENTIONS.md#42-caveats-vs-a-priori-claims) (caveats
   vs a-priori claims — caveat what we did not do, do not claim what
   we did not earn); [§4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory)
   (prior-driven hypotheses are confirmatory, not exploratory —
   crucial for §4.6 lived-experience reconciliation).
7. **Literature methodology anchors** — the four N-of-1 reporting and
   inference standards under
   [`literature/methodology/`](../literature/methodology/) that
   bound how an N-of-1 verdict speaks to its hypothesis:
   [Daza 2018](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)
   (self-tracked N-of-1 counterfactual framing; reach for hypothesis-
   generating priors and convergence-with-consensus claims);
   [Shamseer / CENT 2015](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf)
   (CONSORT extension for N-of-1; reporting items 21 and 22 on
   limitations and generalisability statements);
   [Tate / SCRIBE 2016](../literature/methodology/tate_2016_scribe_single_case_reporting.pdf)
   (single-case experimental design reporting; participant-as-
   researcher transparency item that L4 leans on);
   [Natesan 2023](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf)
   (systematic review of N-of-1 evidence reporting; the bar for what
   counts as a defensible single-case verdict-to-claim translation).
   Stage I cites these as inference-reach anchors when characterising
   the claim shape, not as descriptive-method anchors (those are
   Stage D's business).

The interpretation does NOT load: the HA's `test.py` (that was Stage
D's input; Stage I reads only the verdict the test emitted); per-day
per-cell values from `result-data.json` (Stage I works at the
verdict-and-effect-size summary level the result.md reports); raw
descriptive runs for new analyses (Stage I does not re-test; it cites
Stage D's audit for what is and is not BACKSTOPPED).

## 3. Output

The interpretation produces exactly one artefact per HA:

```
docs/research/analyses/interpretation/HA-XX.md
```

**Naming convention.** One file per HA at the top level of
`analyses/interpretation/` — **no per-HA subfolder**. This is
intentionally different from Stage D's per-HA folder convention (per
[`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
§3): Stage D may accumulate supporting plots under
`analyses/descriptive/HA-XX/plots/`; Stage I has no plot output and
produces only the single MD. The flat naming convention matches the
synthesis-structure map's §2 declared output path
(`analyses/interpretation/HA-XX.md`) and the locked plan's §5 output-
structure tree exactly.

The HA name in the filename is the HA's exact registry ID with no
revision suffix (e.g. `HA-C3.md` for HA-C3 v2 r2, `HA-C3p.md`,
`HA-C4c.md`, `HA11-bout-redo.md`). Revision history of the
interpretation lives in the file's own §10 lock log (per §10 below);
revisions to the underlying HA's `result.md` re-trigger this artefact
per the §3.7 drift policy from
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md).

For HAs with sister-HA companion structure (e.g. the
`C-stress-fatigue-shape` cluster's HA-C3 v2 + HA-C3p sister pair per
the synthesis-structure map's §3 row), **each sister HA gets its own
interpretation artefact** — Stage I does not merge sisters into a
joint interpretation. Cross-references between sister-HA
`interpretation.md` files live in the §8 cross-references section.
Joint reading of sister-HA verdicts is Stage S₁'s job, not Stage I's.

**Mode.** The artefact is **reviewer-mode-with-authorization** per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§4 producer/reviewer split table. It is drafted by Claude under user
authorization via the `/research-interpret interpret HA-XX` skill
invocation, and it carries a `## Authorship` block per
[CONVENTIONS §1.2](../CONVENTIONS.md#12-producer-vs-reviewer-mode).
It receives a fresh-session `/research-review` pass before lock per
the locked-plan §4 row for `interpretation.md` — this is different
from Stage D, whose audit artefacts are producer-mode and do NOT
receive a fresh-session review pass (the producer-mode discipline
plus user explicit acceptance is the binding completion event for
Stage D). Stage I's reviewer-mode-with-authorization status is what
the layer's downstream commensurability discipline rests on; the
fresh-session review check is the structural protection.

**L-ID citation discipline at the output level.** Per
[`research_line_limitations.md`](research_line_limitations.md) §5
table row for `interpretation.md`:

> *Cite every limitation that touches the HA's primary signals or
> operationalisation. List by L-ID with one-sentence project-specific
> application.*

This is binding on every Stage I artefact. The §4.5 section of the
interpretation outline below (Caveats narrowing the claim) is where
the L-ID citation block lives. Stage I does NOT cite limitations
freely — it draws from the seven L-IDs and applies each in one
sentence to the HA's specific surface. The synthesis-structure map's
§3 cluster row for the HA names the L-IDs the cluster will need;
Stage I cites the union of the cluster row's L-IDs PLUS any L-ID
the HA's primary-signal usage triggers independently (e.g. L5 v24-
presence-conditioned if the HA uses any `cat_*` / `state_*` /
`per_day_intensity` column as caveat-class, even if the cluster row
listed L5 as NA at the cluster aggregate).

## 4. Section outline for the produced `interpretation.md`

The artefact MUST contain nine sections in this order. Each section's
operational guidance follows.

### 4.1 Section 1 — Target HA + verdict

Mechanically copy from the HA's pre-reg + result + Stage D audit:

- HA ID (e.g. `HA-C3 v2 r2`), pre-reg lock date, result lock date,
  Stage D audit lock date.
- Headline verdict from `result.md` (verbatim; no relabeling — REJECTED
  stays REJECTED, PARTIAL stays PARTIAL, the parenthetical detail
  stays in place, e.g. "REJECTED (wrong-direction override)",
  "PARTIAL (2-of-3 conditions MET)", "PARTIAL (2 of 3 framework-
  validity bars met)", "REJECTED (triad sum = 0.0 / 3.0)").
- Stage D verdict-trust call (TRUSTED / DOWNGRADED-INCONCLUSIVE-
  PROVISIONAL / REQUIRES-DESCRIPTIVE-WORK / STRUCTURALLY-UNTESTABLE-
  AS-CURRENTLY-SPECIFIED). PROVISIONAL or REQUIRES-DESCRIPTIVE-WORK
  triggers the §6 conflict-rule routing; STRUCTURALLY-UNTESTABLE
  blocks Stage I entirely (the interpretation artefact is not drafted
  — the Stage D terminal-state entry is the routing).
- Operationalisation summary (one sentence, copying §4 of the
  pre-reg).
- Synthesis-structure map cluster the HA participates in (one row
  reference per
  [`synthesis_structure_map.md`](synthesis_structure_map.md) §3).

This section is a header, not analysis. Its purpose is to fix the
target so the rest of the interpretation is unambiguous about which
verdict it translates and under what verdict-trust call.

### 4.2 Section 2 — What the data shows

Descriptive layer; **no claim language**. This section paraphrases
what `result.md` reported in descriptive terms (effect-size point
estimates with directions, per-cell n, per-channel verdicts, any
INCONCLUSIVE / sub-30 cells, any sensitivity-arm divergences) without
translating any of it into a claim about the hypothesis.

The discipline per CONVENTIONS §4.1 (no interpretive marks on raw
descriptive layers) and §4.2 (caveats vs a-priori claims): this
section reports numbers and their direction; it does not call them
"strong evidence" or "weak signal" or "consistent with prior" — those
are §3 (verdict licenses) and §4.6 (lived-experience reconciliation)
language. Example for HA-C4 v2: "Triad sum = 0.0 of 3.0; Ch1
discrimination achieved in validate (Cliff's δ +0.238, p=0.0245) but
not in train (δ +0.056, p=0.18); Ch2 similar pattern (validate δ
+0.356; train δ +0.193 with p=0.0004 but sub-threshold magnitude);
Ch3 train REFUTED (δ -0.080) and Ch3 validate INCONCLUSIVE at n=25 <
30 per §5.4." That is descriptive paraphrase; it does NOT yet say
"this means the Wiggers C4 framework is wrong for this corpus" (that
is §3 territory).

**Hard rule.** No use of the verdict label in this section. The
verdict appears in §1 (the header) and §3 (what the verdict
licenses); §2 stays at the per-cell descriptive layer.

### 4.3 Section 3 — What the verdict licenses

The operationalisation-bound claim: what we can say about the
hypothesis given how it was tested.

Two binding rules apply per CONVENTIONS §4.3 (prior-driven
hypotheses are confirmatory):

1. **The claim is about *this operationalisation* of the hypothesis,
   not the hypothesis in the abstract** — unless replication across
   independent operationalisations justifies the broader claim. For
   Stage I (single-HA), the claim stays operationalisation-bound;
   broader claims are Stage S₁'s job (cross-operationalisation
   coherence) or Stage S₂'s job (cross-population reach). Example for
   HA-C3 v2 REJECTED: the verdict licenses "the Wiggers-verbatim 4-bin
   absolute-numerical operationalisation of the stress→fatigue
   convex-cost claim is REJECTED on this corpus's Stratum 4
   unmedicated cell, with wrong-direction override per result.md §X."
   It does NOT license "the Wiggers convex-cost claim is wrong" —
   that requires the cross-operationalisation read at Stage S₁, where
   HA-C3p's personal-baseline-binning PARTIAL would be brought
   alongside.
2. **Effect-size direction is part of every "what the verdict
   licenses" sentence.** A SUPPORTED verdict with a +0.05 Cliff's δ
   licenses a different claim from a SUPPORTED with +0.50; the
   licensed-claim sentence reports the effect size alongside the
   verdict label. Per [`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
   §5.7 (A7 effect-size direction reporting), the audit guarantees the
   effect size is in the result.md; Stage I uses it in the claim
   sentence.

For verdict labels the result.md ontology emits (per §2 input above),
the licensed-claim sentence respects the verdict's internal
structure:

- **SUPPORTED** licenses a within-operationalisation positive claim:
  "the HA's primary cell discriminated heavy-T from non-heavy-T at
  Cliff's δ=X (CI95 ...) under the locked operationalisation."
- **REJECTED** licenses a within-operationalisation negative or
  wrong-direction claim: "the operationalisation as specified did not
  detect the predicted signal at the pre-registered effect size; the
  observed direction was Y." For triad-derived REJECTED (e.g. HA-C4 v2
  triad sum 0.0), the licensed-claim sentence enumerates which
  per-channel verdicts contributed (Ch1 REFUTED, Ch2 REFUTED, Ch3
  REFUTED) — the triad structure is part of the operationalisation
  and the licensed claim respects it. For wrong-direction-override
  REJECTED (e.g. HA-C3 v2), the override clause IS the claim shape;
  Stage I cites the override explicitly.
- **PARTIAL** licenses a within-operationalisation partial-positive
  claim, naming the conditions met. For "k-of-N conditions MET"
  PARTIAL (e.g. HA-C3p 2-of-3, HA11-bout-redo 2-of-3), the
  licensed-claim sentence names which conditions were met and which
  were not. Stage I does NOT collapse a 2-of-3 PARTIAL into "broadly
  SUPPORTED"; the missing condition is part of the claim shape and is
  preserved.
- **INCONCLUSIVE** licenses no positive or negative claim about the
  hypothesis; it licenses a precondition statement ("the test did not
  reach a verdict under the locked operationalisation because [n
  shortfall / gate failure / power inadequacy], and the closure path
  is named in §7 below"). Pure-INCONCLUSIVE HA verdicts route to §4.4
  "what the verdict does NOT license" with the larger claim envelope
  (REJECTED-the-hypothesis is also NOT licensed under INCONCLUSIVE,
  even though it might be the user's prior intuition; INCONCLUSIVE
  means the test did not speak).

### 4.4 Section 4 — What the verdict does NOT license

The mirror of §3: claims this verdict does *not* warrant, especially
the easy overclaims. Per the locked plan §6.2 spec brief and §7
anti-patterns below, the easy overclaims are systematic and
predictable. Stage I makes them explicit so downstream synthesis,
contextualisation, actionability, and translation cannot inadvertently
import them.

The four predictable overclaim shapes Stage I MUST address explicitly
(one sentence each, even when the overclaim is obviously off-base for
the specific HA):

1. **"REJECTED therefore the underlying hypothesis is false."** The
   operationalisation may be inadequate; a different operationalisation
   might detect the predicted signal. For HA-C3 v2 REJECTED, Stage I
   states: "REJECTED of the Wiggers-verbatim 4-bin absolute-numerical
   operationalisation does NOT license REJECTED-of-the-Wiggers-convex-
   cost-claim as a whole; the sister HA-C3p personal-baseline-binning
   operationalisation produced PARTIAL on the same construct (per
   [`_synthesis_seed_notes_2026-06-23.md`](_synthesis_seed_notes_2026-06-23.md)
   §2 inverted-U candidate joint reading — caveat-class advisory,
   NOT a substantive Stage I output for this artefact), and the
   cluster-level reading is Stage S₁'s job per the synthesis-structure
   map's `C-stress-fatigue-shape` row."
2. **"SUPPORTED therefore the proposed mechanism is correct."**
   Correlation in the predicted direction is not mechanism. The
   licensed claim is descriptive shape; the mechanism that would
   explain the shape is a separate question (intervention study,
   physiological measurement, hypothesis-generating prior for group-
   level work per Daza 2018).
3. **"PARTIAL is a weak SUPPORTED."** PARTIAL is its own claim shape;
   the missing condition is informative and is preserved in §3's
   "licensed claim." Collapsing PARTIAL into SUPPORTED is the
   "synthesis-as-counting fallacy" the locked plan §9 prohibits.
4. **"INCONCLUSIVE means the result is leaning in some direction."**
   INCONCLUSIVE means the test did not speak; reading directional
   intuition into an INCONCLUSIVE cell is the §7.4 anti-pattern
   ("smuggling the lived-experience prior into the verdict reading").

For HAs whose verdict reaches farther than a single cell (e.g. HA-C4
v2's triad with one SUPPORTED + two REFUTED channels), the §4
section MUST address the partial-positive reading: "Ch1 validate's
SUPPORTED + Ch2 validate's SUPPORTED do NOT license a partial-Wiggers-
SUPPORTED claim at the hypothesis level, because the §5.3 triad
verdict band (REJECTED at triad-sum 0.0) is the operationalisation's
binding aggregation; cross-channel selective reading would bypass the
locked aggregation rule."

### 4.5 Section 5 — Caveats narrowing the claim (with L-ID citation block)

Two sub-blocks:

**5a. Pre-reg + audit caveats** — caveats drawn from the HA's pre-reg
§8 (the pre-reg's own self-declared narrowing) and from the Stage D
`descriptive_audit.md` §3 (per-assumption status rows, including any
NOT BACKSTOPPED rows that downgrade to PROVISIONAL per §6.2 of guide
#1) and §5 (the audit's `open_inputs` block, where each entry names a
narrowing condition the interpretation inherits). These are
**not new caveats invented at Stage I time**; they are the carry-
forward from upstream. Each caveat cites its source (pre-reg §X /
audit §Y / audit `open_inputs` entry Z).

**5b. L-ID citation block** — the binding output per
[`research_line_limitations.md`](research_line_limitations.md) §5
table row for `interpretation.md`. **Every limitation that touches
the HA's primary signals or operationalisation MUST be listed by L-ID
with one-sentence project-specific application.** The L-ID-to-HA
mapping is derived from:

- The synthesis-structure map's §3 cluster row "L-IDs S₁ will need to
  cite" column for the HA's cluster (this is the union the cluster
  will need; Stage I cites the subset that applies to this HA's
  primary signals).
- Plus any L-ID independently triggered by the HA's signal usage
  (e.g. L5 if the HA uses v24-derived columns even as caveat class,
  per limitations doc §3 L5 "usage in the HA corpus" guidance).
- Minus any L-ID the synthesis-structure map row marks NA for the
  cluster AND the HA does not independently trigger (e.g. L5 NA for
  HA-C3 v2 + HA-C3p in the `C-stress-fatigue-shape` cluster — no v24
  primary signals).

The citation format follows
[`research_line_limitations.md`](research_line_limitations.md) §5
worked examples — a one-line acknowledgment with the L-ID and one
sentence on how this limitation applies to *this artefact's specific
claim*. Example for HA-C3 v2's interpretation:

> *Cites L1 (single-subject reach)*: this verdict is about one
> subject's stress-fatigue dose-response shape; the Wiggers-verbatim
> operationalisation's REJECTED here does not refute the Wiggers
> convex-cost claim at the group level (per Daza 2018 N-of-1
> inference bounds).
>
> *Cites L2 (era confounds)*: HA-C3 v2 ran on Stratum 4 unmedicated
> only; the verdict does not project to the medicated Stratum 4
> sub-phase per the locked-pre-reg §4 scope.
>
> *Cites L3 (device generations)*: `all_day_stress_avg` is an FR245
> Elevate-V3-derived Garmin signal; the verdict is constrained to
> within-device-generation reach.
>
> *Cites L4 (analyst-is-subject)*: HA-C3 v2 is prior-driven by the
> Wiggers handbook reading; per CONVENTIONS §4.3 it is confirmatory,
> and the §4.6 lived-experience-prior reconciliation below records
> the prior explicitly.
>
> *Cites L6 (self-reporting)*: `gevoelscore` is the outcome; the
> verdict inherits the self-report noise floor described in
> limitations doc L6.
>
> *Cites L7 (survivorship)*: the n=581 effective coverage on the
> unmedicated primary cell represents ~42% of Stratum 4 calendar
> days; the verdict does not project to Garmin-coverage-gap days.
>
> *L5 (presence-conditioned data layer) NA — no v24 primary signals;
> daily_computed-only test* (per the synthesis-structure map's
> `C-stress-fatigue-shape` row).

**Hard rule.** A Stage I artefact whose §5b is empty (or whose §5b
omits an L-ID the cluster row lists) is incomplete and the skill
(per §9 refuse-to-lock gate) refuses to mark it complete. The L-ID
citation block is the layer's commensurability guarantee; an
artefact without it cannot be cited by downstream Stage S₁ as having
respected the systemic context.

**Hard rule.** Stage I MUST NOT cite an L-ID it does not apply to. A
citation that reads "L3 (device generations) NA" without an
explanation is forbidden; the NA call requires the same one-sentence
project-specific reason as the apply call.

### 4.6 Section 6 — Lived-experience prior reconciliation

Per CONVENTIONS §4.3 (prior-driven hypotheses are confirmatory) and
limitations doc L4 (analyst-is-subject), prior-driven HAs carry an
explicit lived-experience prior into the interpretation: the user
came into the test with a belief about what the result would look
like, formed from years of living with the underlying phenomenon. The
§4.6 section records that prior explicitly against the verdict.

Three required content items (each one paragraph):

1. **The prior** — what the user expected the verdict to look like
   before the test ran, in one sentence. This is recorded from
   interview (per the §8.3 seed below); it is NOT inferred from the
   pre-reg's framing (the pre-reg is the *test* of the prior, not the
   prior itself).
2. **The verdict** — what the result.md actually reports, in one
   sentence, in the same vocabulary the prior used.
3. **Whether they agree or diverge, and if diverge, both readings
   preserved with no auto-resolution.** Per the locked plan §6.2
   conflict rule (verdict vs lived-experience prior — log both, do
   not resolve in this artefact). The reconciliation paragraph does
   NOT pick a side. If the prior agrees with the verdict, the
   paragraph says so. If the prior diverges, the paragraph records
   both: the prior with its lived-experience grounding, the verdict
   with its operationalisation grounding, and a one-sentence
   acknowledgment that resolution is Stage S₁ work (if the divergence
   resolves at the cluster level via a sister-HA reading) or stays
   open (if no cluster-level path exists).

**Hard rule.** §4.6 is NOT §3.12 commentary. The distinction is
operational:

- §4.6 is **structured prior-vs-verdict reconciliation** — one prior
  recorded, one verdict cited, one paragraph stating agree-or-diverge
  with no auto-resolution. It is required on every prior-driven HA's
  interpretation. It carries no permitted-vs-forbidden-language
  vocabulary discipline; it carries the no-auto-resolution discipline
  instead.
- §3.12 commentary is **patient-facing subject-narrative** at Stage A
  and Stage T patient-audience track. It is optional, attached to a
  formal tier-1 or tier-2 claim, attribution-required ("I" / "the
  subject"), language-bounded (forbidden: "predicts", "forecasts",
  "X means Y"). It cannot live at Stage I.

The two distinctions: §4.6 is at the verdict-vs-prior epistemic
layer (what the analyst expected to find vs what the test found);
§3.12 is at the patient-facing-narrative layer (what the subject
notices about a formal claim in lived experience). The locked plan
§3.12's "hard separations" list explicitly forbids §3.12 commentary
from living anywhere except Stage A and Stage T patient-audience-
track; Stage I's §4.6 inhabits a different layer entirely.

**Smuggling check.** The §4.6 paragraph MUST stay at the prior-vs-
verdict level. The §7.4 anti-pattern (smuggling lived-experience
prior into §2 or §3) is enforced by Stage I's structural separation:
§2 is descriptive paraphrase, §3 is what-the-verdict-licenses, and the
prior enters only in §4.6 (and only as recorded prior + verdict +
agree-or-diverge, with no auto-resolution). The user's prior does not
get to override the verdict in §3 even if the user feels strongly
about it; the override path is sister-HA construction (which produces
a new verdict the cluster reads) or pre-reg revision (which retests
the construct), not Stage I prose.

**Agreement does not strengthen the licensed claim.** When the prior
agrees with the verdict, the §4.6 paragraph records the agreement but
**does NOT thereby strengthen the §3 licensed claim**. The §3 claim
is what §4.3 verdict-to-claim mapping says it is — bounded by
operationalisation, effect size, era stratum, and the upstream Stage
D audit's verdict-trust status. Lived-experience agreement is a
descriptive observation about the prior; it carries no inferential
weight that the operationalisation didn't already earn. This rule
exists because the L4 (analyst-is-subject) coupling makes prior-
verdict agreement systematically more likely than chance (the subject
formed the prior from the same lived experience that informed the
pre-reg's framing) — so treating agreement as confirmation would
double-count the same evidence. Both divergence and agreement land in
§4.6 with no §3 modification.

**L4 meta-recursion acknowledgment.** The §4.6 reconciliation is
itself authored by the same agent (Claude) and the same subject
(project author) whose L4 coupling §4.6 is designed to surface. The
recursion is bounded by: (a) the structural separation of §4.6 from
§2 / §3 (the prior cannot reach the licensed claim except via this
section); (b) the no-auto-resolution rule on divergent priors; (c)
the agreement-does-not-strengthen rule above; (d) the fresh-session
`/research-review` peer-check on the locked `interpretation.md`
artefact (per CONVENTIONS §1.2 reviewer-mode-with-authorization
discipline). None of these break the recursion; together they bound
it. Limitations doc L4 §3 ("crucial mitigation caveat") names this
same structural recursion at the layer level; §4.6 inherits that
framing.

### 4.7 Section 7 — Closure-path statement (for PARTIAL / INCONCLUSIVE verdicts)

PARTIAL and INCONCLUSIVE verdicts have an explicit statement of what
*would* upgrade them. This is operational, not aspirational:

- For **PARTIAL** with "k-of-N conditions MET" framing (HA-C3p
  2-of-3; HA11-bout-redo 2-of-3): name the unmet condition(s) and
  state what would make them MET (a tighter operationalisation, a
  larger n on the gated cell, a different threshold, a sister-HA
  with a related operand). Stage I does not pre-register the upgrade
  HA — that is §4.8's follow-up suggestions territory — but it names
  the upgrade path here so the §4.4 "what the verdict does NOT
  license" surface is operationally complete.
- For **PARTIAL** with "wrong-direction-override" or "sensitivity-
  arm divergence" framing: name what the divergence is and what would
  resolve it (typically a Stage S₁ cross-operationalisation reading
  on a sister-HA, or a descriptive deep-dive on the divergent cell).
- For **INCONCLUSIVE** cells inside a verdict (e.g. HA-C4 v2 Ch3
  validate INCONCLUSIVE at n=25 < 30): name what n threshold or gate
  relaxation would close the cell, and whether the closure can come
  from corpus accrual (more days) vs operationalisation revision
  (chain-T+1 rule relaxation per HA-C4 v2 §4.11.3, which is already
  reported as a descriptive sensitivity arm).
- For SUPPORTED and REJECTED verdicts: §4.7 is short ("the verdict is
  not PARTIAL or INCONCLUSIVE; closure-path is NA"). It is still a
  required section header so the artefact's structure is uniform
  across HAs; only the content collapses.

This section is the §4.4 "does not license" surface's mirror — §4.4
says what we cannot claim; §4.7 says what would let us claim it.

### 4.8 Section 8 — Follow-up suggestions (own-research + external-research tracks)

Per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.11, every reviewer-mode-with-authorization artefact closes with a
**Follow-up suggestions** section, separated into two tracks. Stage I
is the per-stage shape per the locked-plan §3.11 "Stage I" row:

- **Own-research track**: what HA would replicate this finding,
  refute it, or extend the operationalisation. Concrete pre-reg
  shapes, not vague directions. Examples per the four ready HAs:
  - For HA-C3 v2 REJECTED + HA-C3p PARTIAL sister pair: a third
    sister-HA testing the construct with a third bin scheme (e.g.,
    rolling-window-baseline binning, or median-split on the personal
    distribution) would tighten the cross-operationalisation cluster
    reading at Stage S₁.
  - For HA-C4c PARTIAL on cross-phase pooling: an unmedicated-only
    sister-HA running the same `bout_n_did_not_return_day` operand
    would isolate the cross-phase confound from the substantive
    bout-recovery signal.
  - For HA11-bout-redo PARTIAL framework-validity: a third
    framework-validity HA testing the operand on a different
    reference-date pool (e.g., extended-window vs HA11 v1's
    train-era pool) would isolate framework fitness from corpus-era
    fragility.
- **External-research track**: what group-level or comparable-
  population study would test the same hypothesis where our N=1
  setup cannot. Per the locked-plan §3.11 binding scoping discipline:
  **every external-research suggestion MUST explicitly name the N=1
  limit that prevents us from answering the question ourselves**.
  Naming "someone should run an RCT" without "we cannot because we
  have one subject and no comparator arm" is the locked-plan §9
  "unscoped-follow-up fallacy" and is forbidden. The scoping cites
  the relevant L-ID from §4.5 (typically L1 single-subject reach for
  group-level work, L4 analyst-is-subject for blinding-required
  designs, L3 device-generations for cross-device-platform work).

Each entry is one paragraph with: the proposed study; the L-ID that
prevents us from running it ourselves; and what the study would
contribute to the construct the HA tests.

**Distinct from `open_inputs`** (per locked-plan §3.5 vs §3.11). The
§4.9 `open_inputs` block is "what is missing to complete *this
current interpretation*." The §4.8 follow-up suggestions are "what
*next claims* could be built — for us or for others." Both are
required; neither substitutes for the other.

### 4.9 Section 9 — `open_inputs` block

Per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.5, every reviewer-mode-with-authorization artefact produces, alongside its
main content, a structured `open_inputs` block that names exactly:

1. **What is missing** — the descriptive artefact, the sister-HA, the
   lived-experience walk-through for a specific era, the literature
   reference. Use specific paths or proposed pre-reg slot names; do
   not say "more interpretation."
2. **What it is blocking** — typically Stage S₁ on the cluster this
   HA participates in, sometimes a tighter §3 licensed-claim shape on
   this same HA, sometimes a §4.6 reconciliation that could not be
   completed in-session.
3. **Cheapest acquisition path** — which sister-HA pre-reg shape (per
   §4.8 own-research track), which descriptive run (per Stage D
   `open_inputs` carry-forward), which `/fetch-paper` call (per the
   `_pending_literature_fetch.md` pattern). Effort estimate (S ≤ 2h,
   M = 3-8h, L > 8h) per the stocktake §3 convention.
4. **Fallback claim available without it** — always at most one tier
   narrower than the claim being blocked, per locked-plan §3.5 hard
   rule on no-silent-degradation.

Three Stage-I-specific refusal-to-proceed paths produce open_inputs
entries (per plan §3.5 hard rule that every refusal-to-proceed
produces an `open_inputs` entry):

- **Stage D audit missing**: Stage I refuses to start. The open_inputs
  entry names "Stage D `descriptive_audit.md` for HA-XX" as the
  missing input, "Stage I on HA-XX" as what it blocks, "run
  `/research-interpret descriptive HA-XX` per
  [`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
  §9" as the acquisition path, "none — Stage I cannot proceed without
  the audit" as the fallback claim.
- **Stage D audit REQUIRES-DESCRIPTIVE-WORK**: Stage I refuses to
  start. The open_inputs entry inherits the audit's own §5
  `open_inputs` entries (each NOT BACKSTOPPED row in the audit names
  what descriptive artefact would close it).
- **Lived-experience prior cannot be reconciled in-session**: the
  §4.6 paragraph records the prior and the verdict and the divergence,
  but the user identifies that the reconciliation requires a sister-HA
  reading at Stage S₁ that has not yet been pre-registered. The
  open_inputs entry names the proposed sister-HA, what it blocks
  (the §4.6 reconciliation completion at the cluster level, downstream
  Stage S₁), and the acquisition path (sister-HA pre-reg drafting per
  `hypothesis_lock_process.md`).
- **Stage D audit DOWNGRADED-INCONCLUSIVE-PROVISIONAL but user has
  not yet explicitly accepted the PROVISIONAL flag**: Stage I refuses
  to draft a TRUSTED-shape interpretation. The open_inputs entry
  names "explicit user acceptance of Stage D PROVISIONAL flag for
  HA-XX" as the missing input, "Stage I on HA-XX under PROVISIONAL
  carry-forward" as what it blocks, "user decision in the next
  `/research-interpret interpret HA-XX` session (per §6.2 conflict
  rule)" as the acquisition path, "none — Stage I cannot proceed
  silently under PROVISIONAL without explicit acceptance per locked-
  plan §3.5 no-silent-degradation hard rule" as the fallback claim.
  Distinct from "Stage D audit REQUIRES-DESCRIPTIVE-WORK" above
  because the audit's PROVISIONAL label permits Stage I under explicit
  acceptance; the audit's REQUIRES-DESCRIPTIVE-WORK label blocks until
  descriptive work closes the gap.

The skill (per §9 below) aggregates §4.9 entries across all per-HA
interpretations into the layer-wide
`docs/research/methodology/_open_inputs.md` queue. The per-HA entries
are the source rows; the queue is the aggregate.

**Open inputs do not block completion** per locked-plan §3.8: an
interpretation can be COMPLETE *and* carry open_inputs entries.
Completion means "this is the best interpretation with the inputs we
currently have, and we have logged what would improve it." The
exception is the three refusal-to-proceed paths above, where the
open_inputs entry IS the artefact (the interpretation itself is not
drafted — only the entry).

### 4.10 Section 10 — Cross-references

Links out to:

- The HA's `hypothesis.md` and `result.md` (the inputs §1's verdict
  was copied from).
- The Stage D `descriptive_audit.md` at
  `analyses/descriptive/HA-XX/descriptive_audit.md`.
- The synthesis-structure map's §3 cluster row the HA participates
  in (the row reference, not a paraphrase).
- Sister-HA `interpretation.md` files in the same cluster (e.g.
  HA-C3.md and HA-C3p.md cross-reference each other; HA-C4c.md and
  HA11-bout-redo.md if both are in cluster C-bout-framework /
  C-bout-substance per the map; etc.).
- The Stage S₁ `cluster-*.md` artefact this interpretation will feed
  into (forward pointer; the artefact may not yet exist).
- Limitations doc cross-refs for cited L-IDs.
- Literature methodology anchors cited in §3 / §4.5 for inference-
  reach bounds (Daza 2018, CENT, SCRIBE, Natesan 2023).

## 5. The verdict-to-claim mapping rules

This section pins the per-verdict-label translation rules with
worked examples from the four ready HAs (per the synthesis-structure
map's §2 initial-scope: HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo).

### 5.1 SUPPORTED

**Mapping rule.** SUPPORTED licenses a within-operationalisation
positive claim with effect-size-direction reporting. The licensed
claim is bounded by:

- The operationalisation as locked (signals, cell, threshold,
  gating).
- The effect-size magnitude (a SUPPORTED with δ=+0.05 licenses a
  weaker claim than δ=+0.50).
- The era and phase the test ran on (cross-era projection requires
  L2 citation; in particular, cross-phase pooling on the citalopram-
  phase axis requires the
  [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)
  warrant).
- The Stage D verdict-trust call (TRUSTED unblocks; PROVISIONAL
  narrows by one tier per §6.2).

**What SUPPORTED does NOT license.** Mechanism. Group-level
generalisation. Cross-operationalisation claims (those require Stage
S₁). Predictive claims (those require Stage A forward-validation HA).

**No worked example among the four ready HAs** — none of the four
verdicts is a clean SUPPORTED. The mapping rule applies when future
HAs land with SUPPORTED verdicts (e.g. a future Wave 6 retest).

### 5.2 REJECTED

**Mapping rule.** REJECTED licenses a within-operationalisation
negative or wrong-direction claim. The licensed claim is bounded by:

- The operationalisation as locked: REJECTED of operationalisation X
  does NOT license REJECTED of the hypothesis under
  operationalisation Y. The sister-HA cluster reading at Stage S₁ is
  where cross-operationalisation REJECTED converges (if it does).
- The direction of failure: a REJECTED with wrong-direction signal
  (e.g. HA-C3 v2's wrong-direction override) is a different claim
  shape from a REJECTED with null-effect signal. The wrong-direction
  REJECTED licenses "the test detected a signal in the inverse of
  the predicted direction," which is informative; the null-effect
  REJECTED licenses "the test did not detect a signal of the
  pre-registered magnitude in either direction."
- For triad-derived REJECTED (e.g. HA-C4 v2 triad sum 0.0): the
  licensed claim respects the triad's internal structure (Ch1
  REFUTED, Ch2 REFUTED, Ch3 REFUTED — each contributing 0.0 to the
  triad sum). The aggregated REJECTED is the locked aggregation;
  selective per-channel reading at the verdict level is the §4.4
  anti-pattern.

**Worked example — HA-C3 v2 REJECTED (wrong-direction override).**

> *Verdict licenses*: the Wiggers-verbatim 4-bin absolute-numerical
> operationalisation (bins anchored at 30 / 40 per Wiggers handbook
> lines 1357-1368) of the stress→fatigue convex-cost claim is
> REJECTED on this corpus's Stratum 4 unmedicated primary cell, with
> wrong-direction override: the observed signal points in the inverse
> of the Wiggers-predicted direction.
>
> *Does NOT license*: REJECTED of the Wiggers convex-cost claim as a
> whole; REJECTED of an alternative bin-scheme operationalisation;
> any claim about the mechanism that produced the inverse direction
> (that is hypothesis-generating prior for Stage S₁ + Stage S₂).
>
> *Cluster routing*: sister HA-C3p (personal-baseline-quintile binning)
> produces PARTIAL on the same construct, with §6 reporting a 4-cell
> agreement matrix that HA-C3p §6 itself marks as caveat-class post-
> hoc not substantive. Cross-operationalisation reading is Stage S₁'s
> job per the synthesis-structure map's `C-stress-fatigue-shape`
> cluster row.

**What REJECTED does NOT license.** The hypothesis is false (the
operationalisation is what got tested). The mechanism is wrong. A
broader REJECTED at the construct level (that requires the cluster).
That the inverse-direction reading at Stage S₁ should auto-promote
to a positive finding (the inverse direction is a hypothesis-
generating prior at best per Daza 2018; not a positive verdict).

### 5.3 PARTIAL

**Mapping rule.** PARTIAL licenses a within-operationalisation
partial-positive claim that names the conditions met. The licensed
claim is bounded by:

- The "k-of-N conditions MET" structure (or the equivalent verdict-
  internal structure the result.md emits). The unmet conditions are
  preserved in the claim shape.
- The §4.7 closure-path statement: what would upgrade PARTIAL to
  SUPPORTED, named operationally.

**Worked example — HA-C3p 2-of-3 PARTIAL.**

> *Verdict licenses*: the personal-baseline-quintile binning
> operationalisation of the stress→fatigue convex-cost claim is
> PARTIAL on this corpus's Stratum 4 unmedicated primary cell, with
> 2 of 3 pre-registered conditions MET. The two MET conditions are
> [as named in HA-C3p result.md]; the unmet condition is [as named].
>
> *Does NOT license*: collapsing PARTIAL into SUPPORTED; treating the
> 4-cell agreement matrix with HA-C3 v2 (per HA-C3p §6) as substantive
> finding (HA-C3p §6 itself marks the matrix caveat-class post-hoc);
> a broader "stress→fatigue convex-cost claim is partially supported
> at construct level" (that is the cluster-level reading at Stage S₁).
>
> *Closure path*: the unmet condition could be addressed by [a
> tighter operationalisation / a larger n / a sister-HA on a third
> bin scheme], named at §4.7.

**Worked example — HA-C4c PARTIAL.** Similar structure: the cross-
phase-pooled `bout_n_did_not_return_day` × heavy-T operand emits
PARTIAL with the per-condition detail in result.md; Stage I copies
the verdict, names the met-and-unmet conditions, and routes the
cross-phase confound as the closure-path question.

**Worked example — HA11-bout-redo 2-of-3 framework-validity bars
PARTIAL.** Per the synthesis-structure map's §3 row, this is a
methodology-validation (framework-validity) cluster, NOT a
substantive Wiggers cluster. The Stage I interpretation treats the
verdict as **operand fitness-for-purpose**, not as a substantive
finding about within-day recovery. The §3 licensed-claim sentence
reads: "the bout-extraction operand `bout_n_fast_recovery_day` met
2 of 3 framework-validity bars at HA11 v1's calm-day reference-date
pool, under the locked operationalisation. The 2 MET bars are [as
named]; the unmet bar is [as named]." The §4.4 "does not license"
explicitly: "this PARTIAL is operand fitness, NOT a substantive
within-day recovery claim." The cluster's cascade arrow (per the
map's §3 row) means HA-C4c's substantive verdict at cluster
C-bout-substance reads HA11-bout-redo's framework verdict as caveat-
class precondition, not as co-equal substantive evidence.

### 5.4 INCONCLUSIVE

**Mapping rule.** INCONCLUSIVE licenses no positive or negative
claim about the hypothesis. It licenses a precondition statement:

- The test did not reach a verdict under the locked operationalisation.
- The reason for non-verdict (n shortfall / gate failure / power
  inadequacy / sub-30 cell / gating-rule cascade).
- The closure path: what corpus accrual, operationalisation
  revision, or sister-HA construction would close the cell.

**Hard rule.** INCONCLUSIVE does NOT lean. The §4.4 anti-pattern
("INCONCLUSIVE means the result is leaning in some direction") is
explicitly forbidden. The user may have an intuition about which
direction the test would have leaned if the cell had n≥30; that
intuition is §4.6 lived-experience-prior material, not §3 licensed-
claim material.

**No worked example as a headline verdict among the four ready HAs**
— all four reach PARTIAL or REJECTED. INCONCLUSIVE cells inside a
verdict (e.g. HA-C4 v2's Ch3 validate cell at n=25 < 30) are
addressed at the per-cell level within §3's licensed-claim shape;
the INCONCLUSIVE cell does not promote to a verdict-label claim
itself.

### 5.5 Triad-derived and "k-of-N" verdicts

The result.md ontology emits verdict labels beyond the four basic
labels: HA-C4 v2's INCONCLUSIVE-aware triad sum routing (REJECTED at
0.0; PARTIAL at 1.0-1.5; SUPPORTED at 2.0-2.5; SUPPORTED-strong at
3.0); HA-C3 v2's wrong-direction override REJECTED; HA-C3p's
"2-of-3 conditions MET" PARTIAL; HA11-bout-redo's "k-of-3 framework-
validity bars met" PARTIAL.

**Mapping rule.** Triad-derived and k-of-N verdicts inherit the
mapping rule of their resolved label (REJECTED inherits §5.2;
PARTIAL inherits §5.3; SUPPORTED inherits §5.1), with one
additional discipline:

- The §3 licensed-claim sentence MUST respect the verdict's internal
  aggregation (the triad's per-channel verdicts; the k-of-N's per-
  condition met/unmet pattern; the wrong-direction override's
  direction-of-failure).
- The §4.4 "does not license" surface MUST address the per-channel /
  per-condition selective-reading overclaim explicitly: a Ch1+Ch2
  validate SUPPORTED + Ch3 REFUTED triad does NOT license "Wiggers
  validate-era partial-SUPPORTED" at the verdict level, because the
  triad band (REJECTED) is the locked aggregation.

**Stage I does NOT invent new verdict labels.** If the result.md
emits a label that does not fit the four basic labels' mapping
rules, Stage I copies the label and applies the mapping rule of the
resolved-label family (REJECTED / SUPPORTED / PARTIAL / INCONCLUSIVE)
that the result.md's verdict-band rule routed to. Stage I never
re-routes the band, re-scores the cells, or re-labels the verdict;
that is result.md's job and the audit at Stage D's job.

**Qualifier handling — verbatim carry-forward + effect-size
encoding.** When result.md emits a verdict with a strength qualifier
(e.g. HA-C4 v2's `SUPPORTED (strong)` at triad sum 3.0; HA11-bout-
redo's `2-of-3 framework-validity bars met` PARTIAL), the §3 licensed-
claim sentence carries the qualifier **verbatim** as it appears in
result.md — Stage I does NOT collapse it to a plain resolved-label.
The qualifier records the result.md's locked aggregation precision
and the reader (downstream S₁ / S₂ / A) needs it intact. **Strength
encoded twice — once in the verbatim qualifier, once in the §3
effect-size cite** — is correct and required:

- The verbatim qualifier (e.g. "SUPPORTED (strong)") records the
  verdict-band-level aggregation pattern.
- The effect-size cite (e.g. "Cliff's δ = +0.42, p = 0.0001") records
  the per-cell statistical magnitude.

The two are not redundant: a `SUPPORTED (strong)` triad at sum 3.0
can have heterogeneous per-channel effect sizes; the qualifier
records the aggregation pattern, the effect-size cite records the
per-channel signal strength. The §3 sentence cites both.

A future SUPPORTED-strong verdict (no current example among the four
ready HAs; HA-C4 v2's actual triad sum is 0.0 REJECTED) would read:
"HA-XX result.md emits `SUPPORTED (strong)` at triad sum 3.0; the
verdict licenses [the operationalisation-bound claim] with the
qualifier carried forward, recording that all three channels met
both (a) and (b) bars across both eras (effect sizes per channel:
Ch1 δ = X / Ch2 δ = Y / Ch3 δ = Z)."

**No qualifier collapse.** Stage I MUST NOT rewrite `SUPPORTED
(strong)` as "SUPPORTED" with the strength buried in prose; the
qualifier IS the verdict-band aggregation precision and downstream
artefacts read it as such.

## 6. Conflict rules

The interpretation MUST apply the following conflict rules when
verdict + audit-trust + lived-experience prior interact:

### 6.1 Verdict vs lived-experience prior

> Log both, do NOT resolve in this artefact.

Per locked-plan §6.2 spec conflict rule and CONVENTIONS §4.3
prior-driven-hypotheses-are-confirmatory: when the user's lived-
experience prior diverges from the verdict, the §4.6 paragraph
records both readings — the prior with its lived-experience
grounding, the verdict with its operationalisation grounding — and
explicitly names that the divergence is not resolved at Stage I.

Three resolution paths (NOT executed at Stage I):

1. **Stage S₁ cross-operationalisation reading**: a sister-HA on a
   different operationalisation may produce a verdict that, when
   read alongside the diverging HA at the cluster level, resolves
   the divergence. The §4.6 paragraph names the cluster (per the
   synthesis-structure map) and the sister-HA the cluster reading
   would draw on. Resolution happens at Stage S₁; Stage I records
   the pointer.
2. **Sister-HA construction**: if no sister-HA exists, the §4.8
   own-research follow-up names a candidate sister-HA pre-reg shape.
   The divergence remains open until the sister-HA is pre-registered,
   tested, and a fresh Stage I interpretation lands on it.
3. **Stays open**: some divergences have no cluster-level path. The
   §4.6 paragraph names that explicitly: "the prior and the verdict
   diverge; no cluster-level reconciliation path currently exists;
   the divergence is logged and remains open." This is a valid
   outcome; the open divergence is itself part of the corpus's
   epistemic state.

Stage I does NOT pick a side. Stage I does NOT downgrade the
verdict to fit the prior. Stage I does NOT downgrade the prior to
fit the verdict.

### 6.2 Verdict vs Stage D audit (PROVISIONAL flag)

> Refuse to draft as TRUSTED interpretation; proceed under explicit
> user acceptance of PROVISIONAL flag carrying forward.

Per
[`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
§4.4 verdict-trust call:

- **TRUSTED**: Stage I proceeds normally. The §1 header records
  "Stage D audit: TRUSTED" and the §4.5 caveats inherit the audit's
  §3 per-assumption BACKSTOPPED rows.
- **DOWNGRADED-INCONCLUSIVE-PROVISIONAL**: Stage I MAY proceed under
  explicit user acceptance of the PROVISIONAL flag carrying forward
  as a narrowing flag on the interpretation. The §1 header records
  "Stage D audit: DOWNGRADED-INCONCLUSIVE-PROVISIONAL; Stage I
  proceeding under user-accepted PROVISIONAL flag." The §3 licensed-
  claim sentence narrows by at most one tier per locked-plan §3.5
  hard rule (e.g., a SUPPORTED verdict's licensed claim narrows from
  "the operationalisation discriminated heavy-T from non-heavy-T at
  δ=X" to "the operationalisation discriminated heavy-T from non-
  heavy-T at δ=X under the PROVISIONAL-audit caveat that [the NOT
  BACKSTOPPED assumption] could not be confirmed"). The §4.5 caveats
  block cites the audit's §3 NOT BACKSTOPPED row and the audit's §5
  `open_inputs` entry that would close it.
- **REQUIRES-DESCRIPTIVE-WORK**: Stage I refuses to start. The
  §4.9 `open_inputs` entry inherits the audit's own §5
  `open_inputs` entries.
- **STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED**: Stage I is not
  drafted at all. The Stage D audit's §4.4 verdict-trust call routes
  to pre-reg revision, retirement, or shelve-blocked per the audit's
  §6.2; the interpretation artefact does not get a draft.

The user-accepted PROVISIONAL path is recorded in the §10 lock log
explicitly, not silently absorbed. The skill (per §9 below) refuses
to mark TRUSTED-interpretation when the audit is PROVISIONAL; user
override to PROVISIONAL-carrying-forward is the explicit user-accept
action recorded in the lock log.

### 6.3 Verdict vs cluster-level expectation

Stage I does NOT compare the verdict against what the cluster
"should" produce. The cluster reading is Stage S₁'s job. If a Stage
I interpretation finds that the verdict conflicts with the cluster's
other-HA verdicts (e.g., a HA-C3 v2 REJECTED vs HA-C3p PARTIAL on
the same construct), the conflict is recorded as a §4.10 cross-
reference and routed forward to Stage S₁ via the §4.8 own-research
follow-up track; Stage I does not pre-empt the cluster coherence
call.

## 7. Anti-patterns explicitly forbidden

The following moves are forbidden in any Stage I interpretation:

### 7.1 "REJECTED therefore the underlying hypothesis is false"

The most common failure mode of an unguided interpretation. The
operationalisation may be inadequate; a different operationalisation
might detect the predicted signal. REJECTED is always
operationalisation-bound at Stage I; broader REJECTED claims require
Stage S₁ cross-operationalisation reading. The §4.4 surface MUST
address this explicitly.

### 7.2 "SUPPORTED therefore the proposed mechanism is correct"

Correlation in the predicted direction is not mechanism. The
licensed claim is descriptive shape; the mechanism that would
explain the shape is a separate question. The §4.4 surface MUST
address this explicitly for every SUPPORTED verdict.

### 7.3 Reframing the hypothesis to fit the verdict

"What it really meant was..." is forbidden. The pre-reg's §1 / §2
language is the binding statement of what the hypothesis was; Stage
I does not paraphrase, re-scope, or re-interpret. If the verdict
suggests a more interesting question than the one the hypothesis
asked, that becomes a §4.8 own-research follow-up (a new HA pre-
registering the more interesting question), not a Stage I re-frame.

### 7.4 Smuggling the lived-experience prior into §2 or §3

The lived-experience prior lives in §4.6, and only in §4.6. The
descriptive paraphrase in §2 reports numbers and directions without
prior-informed reading. The licensed-claim sentence in §3 respects
the verdict the test emitted, not the verdict the user expected.
The §3 sentence MUST NOT read "as the participant expected, the test
detected..."; that smuggles the prior into the operationalisation-
bound claim, where it does not belong.

### 7.5 Inventing new caveats post-hoc

Caveats in §4.5 come from the pre-reg's §8 and the Stage D audit's
§3 / §5. New caveats invented at Stage I time — caveats that appear
neither in pre-reg §8 nor in the audit — are forbidden. If Stage I
identifies a caveat the pre-reg and audit missed, the
[`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
§7.5 anti-pattern routing applies (the caveat surfaces as a Stage D
audit gap and triggers a re-examination of the audit per the §3.7
drift policy); it does not enter the interpretation through Stage I
prose.

### 7.6 Conflating PARTIAL with weak SUPPORTED

PARTIAL is its own claim shape. "k-of-N conditions MET" is informative
in a way "weak SUPPORTED" is not; the unmet conditions are part of
the claim and are preserved in §3 and §4.7. The locked-plan §9
"synthesis-as-counting fallacy" warns against this at the synthesis
layer; Stage I prevents the fallacy from being seeded at the per-HA
layer.

### 7.7 Producing §3.12 subject-narrative commentary at Stage I

Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.12 hard separations: commentary lives at Stage A `construct-*.md`
(attached to tier-1 or tier-2 formal claim) and Stage T patient-
audience translation track only. Stage I MUST NOT carry §3.12
commentary. The §4.6 lived-experience prior reconciliation is NOT
§3.12 commentary (see §4.6 above for the operational distinction).
Wording that reads as subject-narrative — "I notice that...", "in my
experience..." — does not belong in §4.6 either; §4.6 carries
prior-vs-verdict reconciliation in third-person-or-recorded-prior
voice, not first-person narrative. The "bare-narrative-as-
actionability fallacy" (locked-plan §9) is the layer-level form of
this anti-pattern; Stage I's prohibition is the per-stage form.

### 7.8 Computing or citing predictive-quality measures

Per locked-plan §3.10: PPV, base rate, sensitivity, specificity,
false-alarm rate, lead time, reliability — these are Stage A's
output, required at tier-2+. Stage I does NOT compute, cite, or
forward-project any of these. The §3 licensed-claim sentence reports
effect-size magnitude and direction (per CONVENTIONS §2.1
descriptive-before-inference), not diagnostic-quality measures. The
forward pointer is Stage A; Stage I cites the synthesis-structure
map's §5 K-construct row to confirm which tier the construct may
reach if all required evidence lands, but Stage I does not produce
the tier's quality measures itself.

### 7.9 Inventing a new verdict label

Stage I does NOT invent verdict labels. If the result.md emits a
label outside the SUPPORTED / REJECTED / PARTIAL / INCONCLUSIVE
ontology + the triad-derived / k-of-N / wrong-direction-override
extensions, Stage I copies the label verbatim and applies §5.5's
"resolved-label family" mapping rule (REJECTED / SUPPORTED /
PARTIAL / INCONCLUSIVE family). Stage I does not relabel, re-route,
re-score, or re-aggregate; those are Stage D audit territory (for
audit-status relabeling) and result.md territory (for verdict
relabeling, which requires a re-run).

## 8. Interview-prompt seeds

The `/research-interpret interpret HA-XX` skill drives the
interpretation as an interview. Three required seeds per the locked-
plan §6.2 spec brief, plus an optional fourth:

### 8.1 Verdict-to-claim licensing

> "Given [verdict] under [operationalisation], what claim about the
> hypothesis itself does that license? What does it *not* license?"

**Use.** Drives §3 (what the verdict licenses) and §4.4 (what the
verdict does NOT license). The skill presents the verdict (copied
from result.md), the operationalisation (copied from pre-reg §4),
and asks the user to articulate the licensed claim and the easy
overclaim. The user's articulation is cross-checked against §5's
verdict-to-claim mapping rules and §7's anti-patterns; mismatches
are surfaced (e.g. the user articulates a REJECTED that licenses
"the Wiggers claim is wrong" — the skill flags §7.1 anti-pattern and
seeks the operationalisation-bound rephrasing).

### 8.2 Competing-operationalisation narrowing

> "Is there a competing operationalisation that, if also tested and
> REJECTED, would meaningfully narrow what we can say?"

**Use.** Surfaces the cross-operationalisation question for §4.8
own-research follow-up (sister-HA suggestions) and for §4.10 cross-
references to existing sister HAs. For sister-HA pairs (HA-C3 v2 +
HA-C3p; HA-C4c + HA11-bout-redo per the map), the answer is
typically "yes — sister X exists and produced verdict Y"; that
becomes the §4.10 cross-reference and the §4.6 reconciliation pointer
(if the sister-HA verdict reconciles the lived-experience-prior
divergence). For HAs without a sister, the answer is "no, but a
sister with operationalisation Z would tighten"; that becomes a §4.8
own-research follow-up.

### 8.3 Lived-experience reconciliation

> "How does this verdict sit against what you lived through during
> the relevant era? If there's tension, what is it?"

**Use.** Drives §4.6 (lived-experience prior reconciliation). The
skill presents the verdict and asks the user to articulate the prior
they came into the test with. The user's articulation is recorded
verbatim (per the §4.6 "do not infer from the pre-reg" rule). The
agree-or-diverge call is the user's; the skill does not auto-resolve
(per §6.1 conflict rule). If diverge with no cluster-level path, the
skill surfaces the "stays open" path explicitly and records it in
§4.6 and §4.9 `open_inputs`.

### 8.4 Optional seed — verdict-trust audit confirmation

> "The Stage D audit verdict-trust call is [TRUSTED / PROVISIONAL].
> If PROVISIONAL, do you accept the flag carrying forward as a
> narrowing on this interpretation?"

**Use.** Confirms §1 header (Stage D verdict-trust call recording)
and §6.2 conflict-rule routing. This is a confirmation seed, not a
discovery seed — by the time the skill reaches it, the §1 header
should mechanically record what the audit emitted. The user's
explicit acceptance of PROVISIONAL-carrying-forward is the binding
event for proceeding under PROVISIONAL; without it, the skill
refuses to draft and routes to the audit's `open_inputs` entries.

## 9. Agent-instruction outline

This section is what `/research-interpret interpret HA-XX` (produced
in §11 step 7 of the plan) will codify into its skill behavior. The
skill MUST follow these phases in order:

### 9.1 Load

The skill loads (in order): the HA's locked `hypothesis.md`,
`result.md`, the Stage D `descriptive_audit.md` at
`analyses/descriptive/HA-XX/descriptive_audit.md`, the synthesis-
structure map's §3 cluster row the HA participates in, the
limitations doc's §5 citation requirements row for
`interpretation.md`, and the four literature methodology anchors.

The skill MUST refuse to proceed if any of `hypothesis.md`,
`result.md`, or `descriptive_audit.md` is missing. Missing
`descriptive_audit.md` produces an `open_inputs` entry per §4.9
refusal path 1.

### 9.2 Gate

The skill reads the audit's §4 verdict-trust call:

- **TRUSTED** → proceed to §9.3.
- **DOWNGRADED-INCONCLUSIVE-PROVISIONAL** → present the PROVISIONAL
  flag to the user via §8.4 seed; on explicit user acceptance,
  proceed to §9.3 with the PROVISIONAL-carrying-forward flag set on
  the interpretation. On user rejection, halt and produce only the
  §4.9 `open_inputs` entries inheriting from the audit's §5.
- **REQUIRES-DESCRIPTIVE-WORK** → halt; produce only the §4.9
  `open_inputs` entries inheriting from the audit's §5.
- **STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED** → halt; do not
  draft the interpretation artefact; route to the audit's §6.2
  pre-reg revision / retirement / shelve-blocked pathway. The Stage I
  interpretation file is not produced at all.

### 9.3 Extract

The skill extracts the verdict (verbatim from result.md), the
operationalisation summary (from pre-reg §4), the per-cell
descriptive numbers (from result.md tables — for §2 paraphrase), the
pre-reg's §8 caveat list, and the audit's §3 per-assumption status
rows and §5 `open_inputs` entries (for §4.5 carry-forward). The
skill extracts the synthesis-structure map's L-IDs column for the
HA's cluster (for §4.5 L-ID citation block scoping).

### 9.4 Interview

The skill walks the §8 seeds in order — §8.1 (verdict-to-claim
licensing), §8.2 (competing-operationalisation narrowing), §8.3
(lived-experience reconciliation), §8.4 (verdict-trust audit
confirmation, if not already handled at §9.2). For each seed, the
skill records the user's articulation, cross-checks against §5
mapping rules and §7 anti-patterns, surfaces mismatches, and seeks
the operationalisation-bound or anti-pattern-cleared rephrasing.

The skill MUST NOT autonomously fill §4.6 (lived-experience prior
reconciliation); the prior comes from the user via §8.3 and is
recorded verbatim.

### 9.5 Produce

The skill drafts `analyses/interpretation/HA-XX.md` following the §4
outline. All nine sections (§4.1 through §4.10) are filled; §4.5
carries the L-ID citation block per the synthesis-structure map's
row PLUS independently-triggered L-IDs; §4.6 carries the lived-
experience prior recorded verbatim from §8.3; §4.7 collapses to "NA"
for SUPPORTED / REJECTED verdicts and expands for PARTIAL /
INCONCLUSIVE; §4.8 carries both tracks (own-research with concrete
pre-reg shapes; external-research with explicit N=1-limit scoping per
§3.11 binding); §4.9 carries `open_inputs` entries per the three
refusal paths plus any narrowing-input the interpretation surfaces.

The artefact's status header records DRAFT r1, reviewer-mode-with-
authorization, and the `## Authorship` block per CONVENTIONS §1.2.

### 9.6 Refuse-to-lock gate

The skill MUST refuse to mark the artefact ready for completion if
any of the following holds:

- A §4.5 L-ID is missing from the citation block that the synthesis-
  structure map's cluster row lists (the map row is binding minus the
  HA-specific subtractions per §4.5 scoping).
- §4.4 does not address the four predictable overclaim shapes
  explicitly (the four-bullet list is mandatory; presence of all
  four sentences is the structural check).
- §4.8 carries an external-research suggestion without explicit
  N=1-limit scoping (locked-plan §3.11 binding).
- §4.6 records a divergence without recording both readings or
  without naming the resolution path (Stage S₁ pointer / sister-HA
  proposal / stays-open).
- §3 / §2 contain verdict-overclaim language that violates §7 anti-
  patterns.

### 9.7 Review handoff

On user-accepted-as-ready-for-completion, the skill recommends a
fresh-session `/research-review` per locked-plan §4 producer/reviewer
split table for `interpretation.md` (reviewer-mode-with-authorization
artefacts get `/research-review`, not `/research-methodology-review`
— see locked-plan §11 intro for the discipline-gate routing). The
review report lands at
`docs/research/reviews/HA-XX-interpretation-YYYY-MM-DD.md` per the
existing review-folder convention.

### 9.8 Acceptance + drift-trigger registration

Per locked-plan §3.8, "user explicitly accepts" is the binding
completion event. On acceptance: the status header transitions to
LOCKED with a lock-log entry; §4.9 `open_inputs` entries propagate
to the layer-wide `_open_inputs.md` queue; the cluster the HA
participates in becomes eligible for Stage S₁ (when all cluster-
member interpretations are complete per the locked plan §3
dependency rule). Per §3.7 drift policy, the skill registers four
re-examination triggers at lock time:

1. The underlying HA's `result.md` re-runs.
2. The Stage D `descriptive_audit.md` is re-examined (per audit's
   own drift triggers).
3. A cited methodology MD changes lock-version (in particular
   [`research_line_limitations.md`](research_line_limitations.md),
   since L-ID citations propagate; and the cited operationalisation
   methodology MDs per the pre-reg).
4. ≥6 months elapse since lock (cadence check per locked-plan §3.7).

**Drift-trigger registration is manual-pending-skill.** Until the
§11 step 7 `/research-interpret` skill lands, drift-trigger
registration is maintained by hand: the interpretation's §10 lock
log carries a "Drift triggers registered" line naming the four
trigger conditions, and a future drift-check pass walks the lock
logs of every interpretation to identify HAs whose triggers have
fired. This parallels the audit's §9.6 and limitations doc's §8
downstream-citation-count manual-tracking patterns (all pending the
skill).

The skill also increments the limitations doc's §8 downstream-
citation-count table for each L-ID cited in the interpretation's
§4.5 block (manual until the skill lands per the limitations doc's
§8 tracking-mechanism status note).

## 10. Cross-references

- [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  — §6.2 (the spec brief this guide implements); §3.5 (missing-
  inputs flagging as first-class); §3.7 (drift and replication
  policy); §3.8 (stopping and completion criteria); §3.9 (research-
  line limitations binding); §3.10 (hard predictive gate — Stage A
  forward pointer; Stage I does not cross); §3.11 (follow-up
  research suggestions own + external tracks); §3.12 (subject-
  narrative commentary — Stage I does not carry); §4 (producer/
  reviewer split table; `interpretation.md` is reviewer-mode-with-
  authorization); §11 step 6.2 (the implementation step that produced
  this guide).
- [`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
  — guide #1, LOCKED r2 2026-06-24, the immediate upstream gate.
  §3 folder convention (`analyses/descriptive/HA-XX/descriptive_audit.md`);
  §4.4 verdict-trust call (four labels: TRUSTED / DOWNGRADED-
  INCONCLUSIVE-PROVISIONAL / REQUIRES-DESCRIPTIVE-WORK /
  STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED); §5 per-assumption
  status; §6.1 conflict rules feeding Stage I's §4.5 caveats; §7
  anti-patterns the audit refuses (Stage I inherits as upstream
  discipline).
- [`research_line_limitations.md`](research_line_limitations.md) —
  §3 the seven L-IDs L1-L7; §5 citation requirements table
  (`interpretation.md` row binds Stage I); §8 downstream-citation-
  count table (Stage I increments per L-ID cited).
- [`synthesis_structure_map.md`](synthesis_structure_map.md) — §2
  initial scope (the four ready HAs HA-C3 v2, HA-C3p, HA-C4c,
  HA11-bout-redo are Stage I's first-target corpus); §3 cluster
  table (per-cluster L-IDs column scopes Stage I's §4.5 citation
  block; cluster row is the §4.10 cross-reference); §4 topic table
  (forward pointer for §4.10); §5 construct table (forward pointer
  for Stage A — Stage I does not cross §3.10).
- [`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md)
  — §4 the four HAs ready for Stage D TRUSTED that Stage I will
  draft against first; §3 the gap list that informs the §4.5 caveats
  block when the audit is PROVISIONAL.
- [CONVENTIONS.md](../CONVENTIONS.md) — §1 (role split:
  interpretation.md is reviewer-mode-with-authorization, not
  producer-mode); §1.2 (fresh-session peer review for reviewer-mode-
  with-authorization artefacts; `## Authorship` block); §2.1
  (descriptive before inference); §4.1 (no interpretive marks on
  raw descriptive layers); §4.2 (caveats vs a-priori claims); §4.3
  (prior-driven hypotheses are confirmatory).
- Literature methodology anchors:
  [`literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf`](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)
  (N-of-1 inference reach for §3 + §4.4 + §4.5);
  [`literature/methodology/shamseer_2015_cent_consort_nof1.pdf`](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf)
  (CENT items 21 + 22 for limitations and generalisability;
  §4.5 + §4.8 external-research scoping);
  [`literature/methodology/tate_2016_scribe_single_case_reporting.pdf`](../literature/methodology/tate_2016_scribe_single_case_reporting.pdf)
  (SCRIBE participant-as-researcher transparency for §4.5 L4
  citation); [`literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf`](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf)
  (the bar for defensible single-case verdict-to-claim translation).
- [`hypothesis_lock_process.md`](hypothesis_lock_process.md) — for
  the §6.1 conflict rule's sister-HA construction routing (if the
  prior-vs-verdict divergence requires a new pre-reg).

## 11. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-24 | Drafted r1 | Producer-mode by fresh agent per §11 step 6.2 of [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md) (r5 LOCKED). The agent added operational detail beyond the §6.2 spec at five points (closure-path-statement section; §5 worked examples from the four ready HAs; §5.5 triad-derived/k-of-N verdict mapping rule; §6.2 PROVISIONAL "narrows by at most one tier" wording; §9.6 refuse-to-lock gate). Two §6.2 spec ambiguities resolved by interpretation: §6.2 §8 "per §3.11" interpreted as binding the N=1-scoping discipline; §6.2 §9 cross-references expanded to all forward + backward refs. |
| 2026-06-24 | Fresh-session `/research-methodology-review` | Verdict REVISION RECOMMENDED (mild). Report: [`reviews/methodology-verdict_to_inference-2026-06-24.md`](../reviews/methodology-verdict_to_inference-2026-06-24.md). Two required actions: R1 (§4.6 agreement-direction smuggling gap — prior-verdict agreement does not strengthen the §3 licensed claim); R2 (§5.5 triad-derived/k-of-N qualifier handling — carry forward verbatim, do not collapse). Four recommended: HA-C3p inverted-U seed-notes pointer; L4 meta-recursion paragraph in §4.6; §4.9 fourth refusal path PROVISIONAL-not-yet-accepted; §4.3-§5 ~80-line compression. Four-input bar: 4 PASS (stronger than guide #1's 3 PASS + 1 PARTIAL). All cross-cutting rules (§3.10 hard gate; §3.12 commentary boundary; §3.11 N=1 scoping; L-ID discipline; Stage D upstream gate) strongly enforced. §5 worked examples cross-check accurately against all four ready HAs' result.md files. All cross-reference spot-checks pass. |
| 2026-06-24 | Revised r1 → r2 | Both required actions absorbed: R1 — §4.6 added agreement-does-not-strengthen rule (L4 coupling makes prior-verdict agreement systematically more likely than chance; treating agreement as confirmation would double-count); R2 — §5.5 added verbatim qualifier carry-forward rule (qualifier records aggregation pattern; effect-size cite records per-cell magnitude; both required; no collapse). Three of four recommended actions absorbed: HA-C3p seed-notes pointer added to §7.1 anti-pattern HA-C3 v2 example; L4 meta-recursion paragraph added to §4.6 closing (bounded by structural separation + no-auto-resolution + agreement-does-not-strengthen + fresh-session review; same pattern as limitations doc L4 caveat); §4.9 added fourth refusal-to-proceed path PROVISIONAL-not-yet-accepted (distinct from REQUIRES-DESCRIPTIVE-WORK refusal). Fourth recommended (§4.3-§5 compression to save ~80 lines) declined for r2 — preserving operational detail; reviewer flagged as optional; future compression pass possible if friction surfaces during dry-run. |
| 2026-06-24 | **LOCKED r2** | User acceptance ("Yes — absorb all 6, lock r2, dispatch guide #3"). Status of all sections LOCKED. Implementation proceeds to §11 step 6.3 (guide #3 `internal_synthesis.md`). No second-pass review per established Option-γ pattern. **Drift triggers registered** (manual-pending-skill): underlying result.md re-runs; underlying descriptive_audit.md re-examined; cited methodology MD changes lock-version (especially research_line_limitations.md and pre-reg-cited operationalisation MDs); ≥6 months elapse since lock. |
