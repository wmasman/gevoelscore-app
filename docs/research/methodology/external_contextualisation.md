# External contextualisation — Stage S₂ guide

**Status**: **LOCKED r3** by user acceptance 2026-06-26. r2 → r3
absorbed the 2026-06-26 Phase A re-open's construct-validity-of-
named-metric miss on `topic-stress-fatigue-pacing.md` — adds NEW
§4.3.5 Construct-identity check interpolated between §4.3 and §4.4
(no renumbering of §4.4-§4.10 to preserve LOCKED-r2 cross-references
in downstream artefacts), wires the §4.3.5 verdict into §4.4
Measurement fault-line constraint via a §4.4 lead-in cross-reference,
and adds NEW §7.13 anti-pattern. Wiggers-stress-score × Garmin-
`all_day_stress_avg` is the §4.3.5 worked example anchor (cautionary
tale + corrected CONSTRUCT-IDENTICAL verdict). r3 absorbed a fresh-
session `/research-methodology-review` (verdict REVISION RECOMMENDED
(mild), report at
[`reviews/methodology-external_contextualisation-r2-to-r3-2026-06-26.md`](../reviews/methodology-external_contextualisation-r2-to-r3-2026-06-26.md))
that caught one required (R1: dispatch-mode placeholder vocabulary
realignment to SKILL.md r4 locked names) and two recommended (A1:
hard rule 2 default-divergence rationale sentence; A2: worked-example
L3-expansion-vs-L8 flag sentence). All three absorbed pre-lock. See
§11 lock log for the full change summary.

**r2 history (preserved for context)**: r1 authored 2026-06-24 by a
fresh agent per §11 step 6.4 of
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
(r5 LOCKED 2026-06-24). r1 → r2 absorbed a fresh-session
`/research-methodology-review` (verdict REVISION RECOMMENDED (mild),
report at
[`reviews/methodology-external_contextualisation-2026-06-24.md`](../reviews/methodology-external_contextualisation-2026-06-24.md))
that caught two required actions (R1: §6.5 load-bearing operational
definition + disambiguation from §4.4-sense; R2: §5.5 mixed-CANNOT-
SAY-with-other-labels case) and four recommended (A1 ~100-line
density compression — deferred per reviewer "for a future revision
pass" framing; A2 §4.4 per-label inference-reach citation; A3 §4.7
parallel T-stress-fatigue-pacing worked example; A4 §11 lock-log
scannability). All required + A2+A3+A4 absorbed; A1 deferred.
Implementation proceeds to §11 step 6.5 (guide #5
`actionability_translation.md`).

This guide is the fourth of six binding methodology MDs for the
results-analysis layer. It governs **Stage S₂** (external
contextualisation): the per-topic artefact that takes a topic's
locked `cluster-*.md` constituent files, walks them against the
external published literature for the topic's construct, and emits a
**positioning call** drawn from a fixed label set (AGREES / EXTENDS
/ DIVERGES / CANNOT-SAY). It sits between Stage S₁'s per-cluster
coherence calls (its direct upstream gate) and Stage A's per-
construct actionability artefacts (its direct downstream consumer).
It refuses to start on a topic whose constituent clusters lack
locked `cluster-*.md` artefacts, on a topic that is not pre-
declared in the synthesis-structure map, and on a topic whose
external-literature claims are uncited (literature-gap-log routing
applies).

---

## 1. Purpose

> **A cluster's coherence call is a within-subject reading. Stage
> S₂ places that reading against external published literature for
> the topic's construct — producing a positioning call (AGREES /
> EXTENDS / DIVERGES / CANNOT-SAY) drawn from a fixed label set
> after an honest comparability check. CANNOT-SAY is a valid and
> often preferred outcome when comparability fails or external
> consensus does not exist.**

A cluster-level coherence call (per
[`internal_synthesis.md`](internal_synthesis.md) §4.4) says how
the project's HAs sit against each other at the construct level
for this subject across this corpus. It does NOT say how this
subject's finding sits against the broader scientific consensus —
that is a different epistemic operation. The cluster's within-
subject signal may converge with the consensus, extend it into a
corner the consensus has not measured, diverge from it (for any
of several reasons: population, instrumentation, era, individual
variation, methodological difference), or the comparison may not
be coherent at all because the literature has not measured this
construct in this population.

Stage S₂ is the per-topic discipline gate that closes that drift.
Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3 stage-map: `D → I → S₁ → S₂ → A → T`. Stage A refuses to start
on a construct whose topic's `topic-*.md` is missing; the synthesis-
structure map's §5 K-construct rollup inherits the Stage S₂
positioning into Stage A's tier-aspiration ceiling. The
comparability-and-positioning discipline Stage S₂ establishes is
what lets Stage A's actionability claims rest on an honest "where
this finding sits in the world" reading rather than a self-
confirming "we found something interesting" assertion.

**What Stage S₂ does NOT do.**

- It does NOT re-test the hypothesis or the cluster's coherence
  call. The cluster reading comes from each constituent's
  `cluster-*.md` and is read as fixed input. Cluster-reading
  revision is a Stage S₁ drift trigger (per
  [`internal_synthesis.md`](internal_synthesis.md) §9.8 + locked
  plan §3.7), not a Stage S₂ activity.
- It does NOT produce predictive claims. Per
  [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  §3.10 hard predictive gate: predictive-tier claims live at
  Stage A and require a pre-registered forward-validation HA.
  Stage S₂ produces no PPV, no base-rate framing, no diagnostic-
  quality measures, and no "forecasts Y" wording. The forward
  pointer is Stage A via the map's §4 topic → §5 construct
  rollup.
- It does NOT carry §3.12 subject-narrative commentary. Commentary
  lives at Stage A `construct-*.md` (attached to a tier-1 or
  tier-2 formal claim) and Stage T patient-audience-track only.
  Same epistemic-category-separation discipline guide #2 enforces
  at Stage I and guide #3 enforces at Stage S₁ carries through;
  §7.7 below operationalises.
- It does NOT refute external published consensus with a single
  N=1 finding. Per L1 (single-subject reach; see
  [`research_line_limitations.md`](research_line_limitations.md)
  §3 L1 "Forbids" row) and Daza 2018 / CENT N-of-1-to-group
  inference-reach bounds: an N=1 DIVERGES finding does NOT auto-
  claim "our N-of-1 finds the truth." Both readings preserved
  with attribution; divergence recorded with candidate
  explanations; no auto-resolution. §6 conflict rules + §7.2
  anti-pattern operationalise.
- It does NOT invent new caveats post-hoc. Stage S₂ draws caveats
  from each cluster's locked `cluster-*.md` §4.5, from
  [`research_line_limitations.md`](research_line_limitations.md)
  §3, and from the synthesis-structure map's §4 topic row's
  L-IDs column. New caveats invented at Stage S₂ time are
  forbidden by §7.6 below.
- It does NOT re-decide which clusters feed which topic. Per the
  locked plan's §3.6 conflict-resolution rule (the same rule
  guide #3 §6.1 operationalises at Stage S₁): if Stage S₂ work
  reveals the map needs changing, Stage S₂ **HALTS** and routes
  to a separate producer-mode map-revision session with its own
  `/research-methodology-review` pass before re-lock. §6.1 below
  operationalises the halt criteria.
- It does NOT operate on more than one topic per session. The
  topic-bounded scope is what keeps positioning calls
  commensurate across topics. Cross-topic reading belongs at
  Stage A (where multiple topics may roll up into a single
  construct per the map's §5) or beyond.

**Alternatives considered** (per CONVENTIONS §2.2 four-input bar
item 3: tradeoff vision). The natural alternative is to fold the
external-literature contextualisation into the [RESEARCH-REPORT
ADDENDUM](../RESEARCH-REPORT-ADDENDUM.md) chain by hand at the
addendum-author's discretion, or to skip Stage S₂ entirely and go
directly from Stage S₁ to Stage A. Both rejected for the same
reasons guides #1, #2 and #3 cite for their respective upstream
stages: (a) addendum-embedded contextualisation collapses the
producer-vs-reviewer-mode split (the topic positioning call is a
reviewer-mode-with-authorization claim that gets a fresh-session
`/research-review` peer check per the locked-plan §4 split); (b)
commensurability across topics requires uniform comparability-
check + positioning-call mapping rules; (c) Stage A's tier
aspiration assumes the cluster signal generalises beyond the
subject, which is exactly what L1's N=1 reach bound forbids
without explicit external positioning — Stage S₂ is the discipline
that surfaces that question rather than allowing it to be assumed
silently.

**Precondition: the `/research-interpret` skill must land first.**
Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§11 step 7, the `/research-interpret` skill is built after the
six guides (this guide is #4 of six). **No Stage S₂ artefact can
be drafted before §11 step 7 lands** — this guide alone is
necessary but not sufficient. The §9 agent-instruction outline
below is the skill's brief; the skill build (step 7)
operationalises it.

## 2. Inputs

The contextualisation MUST load and use the following inputs, in
this order:

1. **The topic's constituent `cluster-*.md` files** — all locked
   (per locked-plan §3 dependency rule: "`S₂` on a topic refuses
   to start until `S₁` for the relevant cluster(s) is complete,
   AND the topic appears in the pre-registered synthesis-structure
   map, AND `research_line_limitations.md` exists"). Each
   cluster's §4.4 coherence call, §4.5 cluster-level caveats +
   L-ID block, §4.6 open conflicts, §4.7a/b joint claim, and §4.8
   follow-up tracks feed Stage S₂ as fixed input — Stage S₂ does
   NOT renegotiate the coherence call, joint claim, or cluster-
   level caveats.
2. **The synthesis-structure map's §4 topic row** for the target
   topic at
   [`synthesis_structure_map.md`](synthesis_structure_map.md) —
   topic name, constituent-cluster list, shared construct, external-
   literature scope cell, L-IDs column (the L-IDs Stage S₂ MUST
   cite at the topic level: L1+L2+L4 unconditionally per the
   limitations doc r3 §5 binding, plus the cluster-derived L3 /
   L5 / L6 / L7 as they apply), declared-date + lock-version.
   Plus the §5 construct row the topic feeds, for §4.10 forward-
   pointer cross-references.
3. **The external-literature PDFs and notes** named by the map's
   §4 row's external-literature-scope cell, under
   [`literature/`](../literature/). For the two active topics in
   the map's r3 §4: T-stress-fatigue-pacing's primary literature
   is [`wiggers_pacing_handleiding.pdf`](../literature/wiggers_pacing_handleiding.pdf)
   (lines 1357-1368 convex-cost claim), with broader PEM-pacing
   literature ([`appelman_2024_muscle_pem_long_covid.pdf`](../literature/appelman_2024_muscle_pem_long_covid.pdf)
   + the pacing / push-crash notes); T-within-day-recovery's
   primary literature is
   [`marques_2023_lc_cardiovascular_autonomic_dysfunction.pdf`](../literature/marques_2023_lc_cardiovascular_autonomic_dysfunction.pdf),
   [`mooren_2023_postcovid_hrv_autonomic_dysregulation.pdf`](../literature/mooren_2023_postcovid_hrv_autonomic_dysregulation.pdf),
   [`ryabkova_2024_mecfs_lc_dysautonomia_patterns.pdf`](../literature/ryabkova_2024_mecfs_lc_dysautonomia_patterns.pdf),
   and
   [`vancampen_2022_mecfs_rhr_elevated.pdf`](../literature/vancampen_2022_mecfs_rhr_elevated.pdf).
   Stage S₂ MUST read the **relevant section** of each cited PDF
   (not the title, not the abstract); §7.1 anti-pattern below
   forbids title-only / abstract-only alignment. Missing
   references route to the literature-gap log per
   [`_pending_literature_fetch.md`](_pending_literature_fetch.md)
   (§6.5 conflict rule below).
4. **N-of-1 reporting and inference standards** under
   [`literature/methodology/`](../literature/methodology/). These
   govern *how* an N-of-1 finding can speak to group-level
   results, not whether.
   [Daza 2018](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)
   is the **primary anchor for Stage S₂** — its N-of-1-to-group
   inference-reach framing directly addresses the comparability-
   check question (when can a within-subject finding speak to
   group-level consensus, and when can it not?).
   [Shamseer / CENT 2015](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf)
   items 21+22 (limitations + generalisability) bind §4.6 and
   §4.7.
   [Tate / SCRIBE 2016](../literature/methodology/tate_2016_scribe_single_case_reporting.pdf)
   participant-as-researcher transparency feeds L4 at §4.7.
   [Natesan 2023](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf)
   sets the defensibility bar.
   [WWC 2022 SCED v5.0](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf)
   codifies the SCED evidence-quality framing the §4.4
   comparability call adapts (meets / meets-with-reservations /
   does-not-meet standards, applied to the cross-population
   comparison rather than to the single-case evidence itself).
5. **The layer-level
   [`research_line_limitations.md`](research_line_limitations.md)**
   — §3 (seven L-IDs L1-L7) and §5 citation requirements row for
   `topic-*.md`: **MUST cite L1, L2, L4 unconditionally; cite L3,
   L5, L6, L7 as they apply**. §3 (output) and §4.7 (per-topic
   limitations) of this guide make the rule operational.
6. **The literature-gap log** per
   [`_pending_literature_fetch.md`](_pending_literature_fetch.md).
   Stage S₂ refuses to lock with uncited external claims floating
   (§9.6 gate); every external claim either cites a
   `literature/`-relative path-and-section the drafter has read,
   or the gap is logged.
7. **CONVENTIONS** — [§1](../CONVENTIONS.md#1-roles) (reviewer-
   mode-with-authorization mode per locked-plan §4);
   [§2.1](../CONVENTIONS.md#21-descriptive-before-inference)
   (descriptive-before-inference; D → I → S₁ → S₂ chain inherits);
   [§4.1](../CONVENTIONS.md#41-no-interpretive-marks-on-raw-layers)
   (no interpretive marks on raw layers — Stage S₂ cites Stage
   S₁'s coherence calls, never reaches back to raw descriptive);
   [§4.2](../CONVENTIONS.md#42-caveats-vs-a-priori-claims)
   (caveat what the positioning did not do; do not claim what it
   did not earn); [§4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory)
   (prior-driven hypotheses confirmatory — positioning inherits
   the confirmatory reach-bound from Stage I reconciliation).

The contextualisation does NOT load: constituent clusters' member-
HA `interpretation.md` files (those were Stage S₁ inputs); raw
descriptive runs (those were Stage D inputs); other topics'
`topic-*.md` artefacts (cross-topic reading is Stage A or beyond).

## 3. Output

The contextualisation produces exactly one artefact per topic:

```
docs/research/analyses/contextualisation/topic-XXX.md
```

**Naming convention.** One file per topic at the top level of
`analyses/contextualisation/` — **no per-topic subfolder**. The
topic name in the filename is the topic's exact ID from the
synthesis-structure map's §4 row (e.g.
`topic-stress-fatigue-pacing.md`, `topic-within-day-recovery.md`
for the two active topics in the map's r3). Flat naming matches
the locked plan's §5 output-structure tree exactly. Revision
history lives in the file's own §11 lock log; revisions to any
constituent cluster's `cluster-*.md` re-trigger this artefact per
the §3.7 drift policy, as does any moderate-or-higher-relevance
literature update.

For topics with a single constituent cluster (currently both
T-stress-fatigue-pacing and T-within-day-recovery sit on one
primary cluster each per the map's r3), Stage S₂ still produces
the topic artefact: the topic-level positioning is a **distinct
epistemic operation** from the cluster-level coherence call (the
topic places the cluster against external literature, which is
not what the cluster does). There is no thin-topic-skip option
analogous to guide #3 §5.6's trivial-ORTHOGONAL skip for single-
member clusters; every topic with locked constituent(s) gets its
own §4.1-§4.10 artefact.

**Mode.** Reviewer-mode-with-authorization per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§4 producer/reviewer split table. Drafted by Claude under user
authorization via `/research-interpret contextualise topic-XXX`,
carrying a `## Authorship` block per
[CONVENTIONS §1.2](../CONVENTIONS.md#12-producer-vs-reviewer-mode).
Receives a fresh-session `/research-review` pass before lock per
the locked-plan §4 row for `topic-*.md` (same discipline Stage I's
`interpretation.md` and Stage S₁'s `cluster-*.md` carry; distinct
from Stage D producer-mode audits).

**L-ID citation discipline at the output level.** Per
[`research_line_limitations.md`](research_line_limitations.md) §5
table row for `topic-*.md`:

> ***MUST cite L1, L2, L4 unconditionally*** (every topic-level
> positioning sits inside the single-subject + era-stratified +
> analyst-is-subject envelope). *Cite L3, L5, L6, L7 as they
> apply.*

Binding on every Stage S₂ artefact. §4.7 below carries the L-ID
block: L1+L2+L4 each in one sentence applied to *this topic's
specific positioning claim* (not per-cluster — Stage S₁ cited
that; not per-HA — Stage I cited that), plus L3/L5/L6/L7 when
the constituent clusters' member-HA signals trigger them per the
map's §4 row L-IDs column.

**Worked-example anchors** (the two active topics in map r3):

- `topic-stress-fatigue-pacing.md` cites L1+L2+L4 unconditionally,
  plus L3 (Garmin `all_day_stress_avg`), L6 (gevoelscore as
  outcome), L7 (gating dropouts in the unmedicated cell). L5 NA
  (constituent cluster C-stress-fatigue-shape has no v24 primary
  signals per the map's §3 row). The unconditional L4 lands
  operationally on the Wiggers-handbook prior-driven structure:
  HA-C3 v2 + HA-C3p both pre-registered with the Wiggers convex-
  cost claim as prior; the L4 mitigation caveat applies because
  the subject + analyst is also the person who chose the prior
  anchor.
- `topic-within-day-recovery.md` cites L1+L2+L4 unconditionally,
  plus L3 (bout-derived Garmin), L7 (gating + cross-phase
  coverage per HA-C4c's pooled cell). L5 NA (no v24); L6 NA
  (gevoelscore not in the primary cell of C-bout-substance per
  the map's §3 row). The unconditional L2 lands operationally on
  the cross-phase pooling specific to HA-C4c's primary cell: the
  topic's within-subject finding spans the citalopram phase axis
  which external-literature comparison populations may not span;
  the cross-era comparability question is part of the topic's
  positioning surface.

**Hard rule.** A Stage S₂ artefact missing L1, L2, or L4 from
§4.7 is incomplete and §9.6 refuses to lock it. The unconditional
L1+L2+L4 block is the layer's commensurability guarantee at the
topic level.

**Hard rule.** Stage S₂ MUST NOT cite an L-ID it does not apply
to. A bare "L5 NA" without explanation is forbidden; the NA call
requires the same one-sentence topic-level project-specific
reason as the apply call (e.g. "L5 NA: the constituent cluster
C-stress-fatigue-shape has no v24 primary signals per the map's
§3 row").

## 4. Section outline for the produced `topic-XXX.md`

The artefact MUST contain ten sections in this order. Each
section's operational guidance follows, kept terse where the
upstream guides' sections already cover the pattern (especially
guide #3's §4 for sections that mirror by structure).

### 4.1 Section 1 — Topic name + constituent clusters

Mechanically copy from the map's §4 topic row + each constituent
cluster's `cluster-*.md` §4.1 header: topic ID + name (verbatim);
constituent cluster list (verbatim); for each cluster, cluster
ID + §4.4 coherence call with any qualifier (e.g. "trivial-
ORTHOGONAL" per guide #3 §5.6; "PARTIALLY CONCORDANT (spec-
mechanism disagreement, shape agreement)" per guide #3 §5.2) +
§4.7a joint-claim sentence verbatim; topic's shared construct
cell (verbatim); external-literature-scope cell (verbatim — the
binding scope for §4.3-§4.5 + §6.5 routing). Header, not
analysis; its purpose is to fix the topic target.

### 4.2 Section 2 — Pre-declared topic membership

Cite the map's §4 topic row directly with declared-date + lock-
version. Membership is read from the map; Stage S₂ does NOT
re-decide in-stage. Template:

> *Pre-declared topic membership* (per
> [`synthesis_structure_map.md`](synthesis_structure_map.md) §4
> row `<topic-id>`, declared `<YYYY-MM-DD>`, lock version
> `<rN>`): the topic groups `cluster-<X>`, `cluster-<Y>`, ... on
> the shared construct `<construct>` and positions against the
> external-literature scope `<scope sentence>`. Locked at the
> map's §7 lock-log entry `<date>`, unchanged since.

**Hard rule.** The §4.2 paragraph cites declared-date + lock-
version verbatim. Does NOT re-derive membership, add/remove
constituent clusters, or propose re-mapping. Re-mapping need →
§6.1 HALT.

### 4.3 Section 3 — Consensus map

For each subclaim in the topic's constituent clusters' joint
claims: does external consensus exist? If yes, what does it
say? If competing positions exist, who holds them?

Per-subclaim block structure:

1. **Subclaim** — one sentence; copied from a constituent
   cluster's §4.7a joint-claim with within-subject scope
   explicit.
2. **External-consensus status** — exactly one of: **CONSENSUS-
   EXISTS** (one-sentence consensus statement + primary
   `literature/`-relative path + section); **COMPETING-POSITIONS**
   (one sentence each position + primary citation each);
   **CONSENSUS-DOES-NOT-EXIST** (what the literature has said
   and why no consensus formed — sparseness, methodological
   disagreement, mixed findings; citation list shows the
   surveyed scope); **LITERATURE-GAP** (relevant section not
   read OR paper not in `literature/` — routed to literature-
   gap log per §6.5; subclaim's consensus-map block does not
   complete until gap closes).
3. **Position-holders** (when applicable for COMPETING-POSITIONS
   or contested CONSENSUS-EXISTS) — named authors / groups /
   guideline bodies, one sentence per holder.

**Hard rule.** Every external claim has either a
`literature/`-relative path-and-section citation OR a literature-
gap log entry. Uncited claims forbidden; §9.6 enforces. Per
§7.1, citation requires reading the *relevant section*, not
title or abstract.

**Worked-example anchor (T-within-day-recovery).** For "bout-
level recovery from heavy exertion is impaired in LC / ME/CFS
populations relative to controls" (from C-bout-substance's
§4.7a narrowed for the topic's external-literature scope):
**CONSENSUS-EXISTS** per the four within-day-recovery anchors
([Marques 2023](../literature/marques_2023_lc_cardiovascular_autonomic_dysfunction.pdf),
[Mooren 2023](../literature/mooren_2023_postcovid_hrv_autonomic_dysregulation.pdf),
[Ryabkova 2024](../literature/ryabkova_2024_mecfs_lc_dysautonomia_patterns.pdf),
[van Campen 2022](../literature/vancampen_2022_mecfs_rhr_elevated.pdf))
once relevant sections are read. The drafting session opens
each PDF to the relevant within-day-recovery / autonomic-
dysregulation section, extracts the consensus statement, cites
paper-and-section. If not yet read, LITERATURE-GAP applies and
routes via §6.5 — Stage S₂ does NOT manufacture a consensus
statement from the abstract.

### 4.3.5 Section 3.5 — Construct-identity check

**Why this section exists.** §4.4 Comparability assumes the
external source and the project are operationalising the **same
construct** on related-or-comparable instruments. That
assumption can fail silently when the external source uses a
named metric that LOOKS like a different substrate but is in
fact the same instrument family the project uses (e.g., Wiggers
handleiding's "stress score" is the Garmin Connect UI metric,
not a subjective rating — same Firstbeat HRV-derived index the
project's `all_day_stress_avg` aggregates). When that
verification is skipped, §4.4 can record a substrate-mismatch
fault-line that does not exist in fact, propagating an invented
construct-validity caveat through §4.5 positioning, §4.6
caveats, and downstream Stage A + Stage T artefacts. Adding the
check as a discrete §4.3.5 closes that drift. **Origin**: the
2026-06-26 Phase A re-open of `topic-stress-fatigue-pacing.md`
absorbed exactly this miss; the worked-example anchor below
records the corrected verdict as a permanent cautionary
reference.

For each named metric the external source cites that the project
also has a named operationalisation for, Stage S₂ produces a
construct-identity verdict drawn from exactly three labels:

- **CONSTRUCT-IDENTICAL** — source and project operationalise
  the same construct on the same instrument family. The source's
  named metric and the project's named metric refer to the same
  underlying measured quantity (same algorithm family, same UI
  metric, same sensor-derived signal). The §4.4 Measurement
  dimension does NOT carry substrate-mismatch as a fault-line;
  remaining fault-lines are calibration-level (device-generation
  L3, vendor algorithm-version drift, population-calibration of
  proprietary algorithm).
- **CONSTRUCT-RELATED** — source and project measure
  related-but-distinct constructs on different instruments (e.g.,
  source uses a validated subjective fatigue inventory; project
  uses gevoelscore on a 1-10 scale). The §4.4 Measurement
  dimension carries the substrate-mismatch fault-line and routes
  to PARTIALLY COMPARABLE; whether the fault-line is load-bearing
  for the specific subclaim is the §5 mapping question.
- **CONSTRUCT-DIFFERENT** — source's named metric and project's
  same-or-similarly-named metric refer to different underlying
  measured quantities (e.g., source's "HRV" = nightly RMSSD vs
  project's `stress_mean_sleep` HRV-proxy — different substrates
  for related-but-distinct autonomic constructs). The §4.4
  Measurement dimension typically routes to NOT COMPARABLE on
  that subclaim; §4.5 typically routes to CANNOT-SAY unless the
  subclaim is about a dimension orthogonal to the construct
  difference.

**Procedure** (one named-metric pass per source-subclaim pair):

1. Identify each named metric the source's relevant section
   (per §4.3 citation) uses. Skip metrics the project does not
   measure; those become NOT COMPARABLE on Measurement at §4.4
   without needing a construct-identity verdict.
2. Read the source's operational definition of the metric (or
   the source's UI / instrument citation if the metric is
   wearable-derived). The source's metric description goes in
   one sentence.
3. Cite the project's operational definition of the
   corresponding metric (one-line reference to the project's
   pre-reg, methodology MD, or — when the eventual
   `helpers/construct_lexicon/` folder exists per
   [[feedback-helpers-design-reactively]] — that helper). The
   project's metric description goes in one sentence.
4. Compare: same construct + same instrument family →
   CONSTRUCT-IDENTICAL; related construct + different instrument
   → CONSTRUCT-RELATED; different construct (whether or not
   instrument differs) → CONSTRUCT-DIFFERENT.
5. Record the verdict + the two one-sentence descriptions as a
   per-subclaim-per-metric block. The §4.4 Measurement dimension
   call inherits and cites this verdict.

**Hard rules**:

- §4.3.5 fires whenever §4.3 records CONSENSUS-EXISTS or
  COMPETING-POSITIONS with at least one named metric cross-cited
  with the project. §4.3.5 does NOT fire for LITERATURE-GAP or
  CONSENSUS-DOES-NOT-EXIST subclaims (no source-side metric to
  check).
- The verdict is drawn from the three-label set; new labels are
  forbidden ("MOSTLY IDENTICAL", "PARTIALLY DIFFERENT"). If no
  label fits cleanly, defaults to CONSTRUCT-RELATED (conservative
  middle — preserves a substrate caveat at §4.4 without
  asserting the source measures a wholly different construct).
  Unlike [`internal_synthesis.md`](internal_synthesis.md) §4.4's
  default-to-CONFLICT (the most-conservative-divergence-
  preserving label), §4.3.5 defaults to the middle CONSTRUCT-
  RELATED because the §7.13 failure mode is bidirectional —
  defaulting to CONSTRUCT-DIFFERENT would recreate substrate-
  mismatch-by-default in the opposite direction; the substrate-
  caveat-without-different-construct-assertion compromise is the
  right resting point for construct-identity ambiguity
  specifically.
- "Substrate mismatch" is NOT a default assumption. If the
  source uses a named UI / instrument metric the project also
  uses, the verdict is CONSTRUCT-IDENTICAL unless evidence in
  the source's text explicitly establishes the source's metric
  refers to a different construct. Per §7.13: asserting
  substrate-mismatch on the inference that "the source's wording
  sounds qualitative" is the failure mode this section closes.
- The §4.4 Measurement dimension MUST cite the §4.3.5 verdict
  per subclaim per metric. The §4.4 PARTIALLY COMPARABLE
  fault-line list is constrained by the §4.3.5 verdict: substrate
  mismatch enters only when the verdict is CONSTRUCT-RELATED or
  CONSTRUCT-DIFFERENT.

**Dispatch-mode placeholders** (reuses the locked vocabulary in
the [`/research-interpret`](../../.claude/skills/research-interpret/SKILL.md)
r4 dispatch-mode framework — no §4.3.5-specific placeholder
names; SKILL.md is the single source of truth):

- **§4.3 `LITERATURE-GAP` status inherits upstream** — when the
  source's relevant section has not been read (§4.3 records
  `LITERATURE-GAP` for the subclaim per its four-label set),
  §4.3.5 does not fire for that subclaim (per hard rule 1) and
  the literature-gap log routing at §6.5 applies upstream of
  §4.3.5. No separate §4.3.5 placeholder name needed.
- **`PROXY-CITED-IN-DRY-RUN`** (SKILL.md r4 Stage S₂ vocabulary)
  — when the source's named-metric mapping has been user-
  accepted via a prior literature brief, register-anchor
  verification log, or a constituent cluster's
  USER-VERIFIED-VIA-REGISTER-ANCHOR-VERIFICATION-{date} cite,
  §4.3.5 cites that provenance (with the verification date in
  the accompanying one-sentence cite) and proceeds with the
  bound verdict.
- **`DEFAULTED-PENDING-USER-INPUT`** (SKILL.md r4 vocabulary) —
  when the source's text is ambiguous on the metric's
  operational definition (e.g., the word appears without a
  clear instrument or scale anchor), the verdict defaults to
  CONSTRUCT-RELATED (per hard rule 2) with the
  `DEFAULTED-PENDING-USER-INPUT` placeholder; user input at
  rollout interview (or fresh-session review) resolves to a
  bound verdict.
- **`SKIPPED-AS-DRY-RUN-DEFAULT`** (SKILL.md r4 vocabulary) —
  **disallowed at §4.3.5**; the check is small and binding
  enough that even dry-run dispatches must produce one of
  {bound verdict, inherited `LITERATURE-GAP`,
  `PROXY-CITED-IN-DRY-RUN`, `DEFAULTED-PENDING-USER-INPUT`}.
  The 2026-06-26 miss was precisely a silent skip; the
  placeholder discipline closes that door.

**Worked-example anchor (T-stress-fatigue-pacing × Wiggers
stress score) — cautionary tale**.

The 2026-06-26 Phase A re-open absorbed a misframing in the
LOCKED r1 `topic-stress-fatigue-pacing.md`'s §4.4 Subclaim 1
Measurement call. The dry-run drafter recorded:

> "Wiggers' framing in the handleiding uses subjective stress
> rating ('a day with a score of 40') without naming a specific
> instrument" — implying a CONSTRUCT-RELATED verdict by
> presumption.

The corrected reading (per
[`wiggers_testable_hypotheses.md` §C C3 verbatim](../wiggers_testable_hypotheses.md#L490),
USER-VERIFIED-VIA-REGISTER-ANCHOR-VERIFICATION-2026-06-12, full
cite in [`literature/wiggers_pacing_handleiding.pdf`](../literature/wiggers_pacing_handleiding.pdf)
lines 1357-1368, Annual Stress Scores section):

> "Your **annual stress overview** includes a **stress score
> line**. If you've paid attention to your own **stress
> scores**, you might know that a day with a score of 40 is much
> more tiring than a day with a score of 30..."

Wiggers's "stress score" unambiguously refers to the Garmin
Connect UI's Annual Stress Scores dashboard line — the same
Firstbeat HRV-derived stress score the project's
`all_day_stress_avg` aggregates as a daily mean.

**Corrected §4.3.5 verdict**:

- **Subclaim**: Wiggers monotone-convex stress-fatigue mapping
  direction.
- **Named metric**: Wiggers's "stress score" / "score of 40".
- **Source's operational definition**: Garmin Connect Annual
  Stress Scores UI line (Firstbeat HRV-derived stress score,
  0-100 scale, daily aggregate; per the source's section title
  "Annual Stress Scores" + UI reference).
- **Project's operational definition**: `all_day_stress_avg` =
  daily mean of the Garmin Firstbeat per-minute stress score
  (0-100 scale; per
  [`wiggers_testable_hypotheses.md` §C cell map](../wiggers_testable_hypotheses.md#L42)).
- **Verdict**: **CONSTRUCT-IDENTICAL**. Same instrument family
  (Garmin Firstbeat stress score), same UI metric, same scale.
  The §4.4 Measurement dimension does not enumerate
  substrate-mismatch as a fault-line; remaining fault-lines are
  device-generation (L3: FR245 vs Wiggers's source-data device
  pool), Firstbeat algorithm-version drift (within-vendor
  calibration scope), and population-Firstbeat-calibration
  (validated in athletes / healthy populations; LC-cohort
  response to a given Garmin-stress reading may differ from the
  typical Garmin-user baseline the algorithm targets). These
  three sub-issues sit under L3 literally per its "underlying
  algorithm updates" + "calibration drift" framing, but stretch
  L3 past its hardware-upgrade-triggered project-specific
  manifestation; whether to expand L3 or add an L8 (vendor-
  algorithm-population-validity) is flagged to the
  [`research_line_limitations.md`](research_line_limitations.md)
  maintainer as a separate decision (tracked separately from
  this r3 lock cycle).

The corrected verdict allows the §4.4 Measurement call to land
**COMPARABLE on construct + instrument family** with the
remaining caveats named per dimension (not as substrate
mismatch); §4.5 DIVERGES on Subclaim 1 remains the substantive
finding, now correctly attributed to within-vendor /
within-population calibration scope rather than to an invented
substrate-mismatch.

### 4.4 Section 4 — Comparability check

**Upstream input from §4.3.5**: each subclaim's §4.4 Measurement
dimension call presupposes the §4.3.5 construct-identity verdict
for each named metric. The §4.4 PARTIALLY COMPARABLE fault-line
list is constrained by the §4.3.5 verdict — substrate-mismatch
fault-lines enter only when §4.3.5 lands CONSTRUCT-RELATED or
CONSTRUCT-DIFFERENT; CONSTRUCT-IDENTICAL forbids substrate-
mismatch in the §4.4 fault-line enumeration.

For each subclaim with CONSENSUS-EXISTS or COMPETING-POSITIONS
from §4.3 (and a §4.3.5 verdict per named metric): is the
external population / measurement / era close enough that "in
line" or "divergent" is a coherent claim?
Produces exactly one of three labels per subclaim, drawing on
Daza 2018 / CENT 2015 / Natesan 2023 / WWC 2022 N-of-1-to-group
inference-reach standards:

- **COMPARABLE** — population (PAIS / ME/CFS / post-COVID LC
  with comparable duration + severity), measurement (cited
  paper's instrument in the same family as the project's
  wearable / self-report), and era (variant + vaccination +
  treatment-availability context) are close enough for the
  positioning to land cleanly. The call cites the specific
  match per dimension in one sentence each. **Inference-reach
  citation**: Daza 2018 convergence-or-divergence-data-point
  reach (this N=1 finding adds a data point that confirms or
  contests the group-level claim without claiming to settle it).
- **PARTIALLY COMPARABLE** — at least one dimension matches and
  at least one does not. The call cites which match and which
  do not in one sentence each, names the fault-line. MAY still
  land AGREES / EXTENDS / DIVERGES (with partial-comparability
  caveat carried into §4.5 + §4.6), OR land CANNOT-SAY if the
  fault-line is load-bearing (§5 mapping rules). **Inference-
  reach citation**: Daza 2018 hypothesis-generating-only-for-
  unmatched-dimensions reach (the unmatched dimensions narrow
  the inference into a hypothesis the group-level work would
  need to test); CENT 2015 item 22 generalisability framing
  binds the partial-comparability caveat language.
- **NOT COMPARABLE** — population / measurement / era too
  different for a coherent positioning. Auto-routes to CANNOT-
  SAY at §4.5 (per §5.4). **Inference-reach citation**: Daza
  2018 no-inference-bridge reach (no defensible mapping between
  the N=1 finding and the group-level construct); WWC 2022 SCED
  does-not-meet-standards framing binds the cross-population
  comparability refusal where the SCED methodology is the right
  meta-context.

**Each comparability call MUST cite the N-of-1-to-group reach
bound it leans on.** Per Daza 2018: N-of-1 can serve as
hypothesis-generating prior and as convergence-data-point when
dimensions match; it cannot, on its own, refute group-level
consensus. COMPARABLE cites the convergence-or-divergence-data-
point reach; PARTIALLY COMPARABLE cites hypothesis-generating-
only reach for the unmatched dimensions; NOT COMPARABLE cites
the no-inference-bridge reach. CENT 2015 item 22 binds the
generalisability statement; Natesan 2023 the defensibility bar.

**Hard rule.** The §4.4 label is drawn from the three-label set;
new labels forbidden ("MOSTLY COMPARABLE", "MARGINALLY
COMPARABLE"). If no label fits cleanly, defaults to NOT
COMPARABLE (conservative discipline analogous to guide #3 §4.4
default-to-CONFLICT-on-ambiguity); §4.5 positioning routes to
CANNOT-SAY accordingly.

### 4.5 Section 5 — Positioning

For each subclaim with a §4.3 consensus-map status and a §4.4
comparability call, Stage S₂ produces exactly one of four
positioning labels:

- **AGREES** — subject's finding matches external consensus on
  direction (and on shape / magnitude within the COMPARABLE
  bound). AGREES adds an N=1 reach caveat per §6 caveat 1 (one
  convergence data point per Daza 2018, not a settlement).
- **EXTENDS** — subject's finding adds shape / detail beyond
  what the consensus has measured (a new operationalisation
  reaches a construct corner the literature has not; a within-
  subject finer-grained pattern beyond the group-level
  aggregation level). Recorded as hypothesis-generating-only
  per Daza 2018; does NOT auto-promote to a strong broader-
  population claim.
- **DIVERGES** — subject's finding contradicts external
  consensus on direction (or on shape / magnitude unreconciled
  by the comparability bound). Both readings preserved with
  attribution per §6; no auto-resolution; candidate
  explanations enumerated (population, measurement, era,
  individual variation, methodological difference). DIVERGES
  does NOT refute consensus (per L1 + Daza 2018); it adds a
  within-subject data point that diverges, and the divergence
  is itself the substantive finding for this subclaim.
- **CANNOT-SAY** — comparability fails (§4.4 NOT COMPARABLE OR
  PARTIALLY COMPARABLE with load-bearing fault-line) OR no
  consensus exists (§4.3 CONSENSUS-DOES-NOT-EXIST and the
  subject's finding does not map cleanly among competing
  positions) OR the comparability gap blocks a clean call.
  **CANNOT-SAY is a valid and often preferred outcome** over
  forced positioning per the locked-plan §6.4 spec. The
  CANNOT-SAY positioning records what would unlock a tighter
  call (literature-gap fill; sister-HA on different
  operationalisation; comparability-bridge descriptive run).

The §4.5 section closes with a **topic-level positioning summary
paragraph** (one paragraph, two-to-four sentences) aggregating
the per-subclaim positionings. Aggregation rules in §5.5; the
key constraint is that any DIVERGES subclaim is named explicitly
as the topic's primary substantive finding — not averaged into
AGREES subclaims (per §7.12 anti-pattern).

**Mapping rules and worked examples are in §5 below.**

**Hard rule.** The §4.5 label is drawn from the four-label set;
new labels are forbidden ("WEAKLY AGREES", "MOSTLY DIVERGES").
If no label fits cleanly, the call defaults to CANNOT-SAY (the
default-to-preserve discipline, analogous to guide #3 §4.4
default-to-CONFLICT-on-ambiguity).

### 4.6 Section 6 — Caveats specific to N-of-1 → group comparison

This section carries the structural caveats that apply to **any
N-of-1-to-group positioning**, drawn from the locked plan §3.10
N-of-1 inference-reach binding (L1 + Daza 2018 + CENT + Natesan
+ WWC). The caveats inherit from the limitations doc's L1 row's
Forbids + Permits bullets, expressed at the positioning level.
Three caveats MUST appear in every §4.6 section, even when the
topic's positioning is AGREES (AGREES does not erase the N=1
reach bound):

1. **The positioning call is one data point, not a settlement.**
   AGREES adds a convergence observation, not a confirmation.
   DIVERGES adds a divergence data point, not a refutation.
   EXTENDS is hypothesis-generating-only, not a population-level
   extension claim.
2. **The comparability bound is the reach bound.** Even at
   COMPARABLE, reach is bounded by which dimensions matched
   (population, measurement, era). PARTIALLY COMPARABLE
   positionings carry the additional caveat on unmatched
   dimensions; NOT COMPARABLE routes to CANNOT-SAY.
3. **External consensus is not external truth.** Where §4.3
   identified COMPETING-POSITIONS, the §4.6 caveat names that
   the positioning is against *the consensus as the topic-row's
   external-literature scope reflects it*, not against an
   unstated "settled truth." Recent consensus shifts or older
   literature get explicit caveat language.

The §4.6 section is **separate from** §4.7: §4.6 carries the
structural N-of-1-to-group caveats specific to positioning;
§4.7 carries the L-ID citations binding at the topic level per
the limitations doc §5. Together they are the topic's complete
caveat surface.

### 4.7 Section 7 — Per-topic limitations (L-ID citation block)

Per
[`research_line_limitations.md`](research_line_limitations.md) §5
row for `topic-*.md`: **MUST cite L1, L2, L4 unconditionally;
cite L3, L5, L6, L7 as they apply.** This section is the binding
L-ID citation block at the topic level.

Each L-ID is one paragraph: opening "Cites L`<N>` (`<short
name>`)" line plus one sentence applying the limitation to *this
topic's specific positioning claim*. The unconditional L1+L2+L4
paragraphs always appear. The L3/L5/L6/L7 paragraphs appear when
the constituent clusters' member-HA signals trigger them per the
map's §4 row L-IDs column; when an L-ID is NA at the topic
level, the section records "L`<N>` NA: `<one-sentence reason>`"
rather than omitting silently (per §3 hard rule).

**Worked-example sketch for T-within-day-recovery** (the topic's
L-IDs per the map's r3 §4 row plus unconditional L1+L2+L4):

> *Cites L1 (single-subject reach):* per Daza 2018 the AGREES
> call (if reached) converges with the external consensus on
> within-day autonomic recovery impairment as one data point,
> not a settlement; DIVERGES adds a divergence data point that
> does not refute the consensus. Group-level confirmation
> requires N >> 1 (§4.9 external-research track).
>
> *Cites L2 (era confounds):* C-bout-substance runs cross-phase
> pooled on the citalopram-phase axis per HA-C4c's primary cell;
> external-literature populations (Marques, Mooren, Ryabkova,
> van Campen) may not span an analogous medication-phase axis;
> §4.4 comparability names the fault-line where it shows up.
>
> *Cites L4 (analyst-is-subject):* positioning call was made by
> the subject + analyst against published work the subject
> identified as the topic's external-literature scope; the L4
> mitigation reach is the fresh-session `/research-review` pass
> bounded by the limitations-doc r3 §3 L4 meta-recursion caveat.
>
> *Cites L3 (device generations):* FR245-derived bout signals vs
> external-literature CPET / HRV instruments; §4.4 names this
> fault-line.
>
> *Cites L7 (survivorship):* HA-C4c's primary cell gating + the
> external-literature populations' own missingness patterns; the
> positioning bridges across two missingness patterns which §4.4
> respects.
>
> *L5 NA:* constituent cluster has no v24 primary signals (map's
> §3 row).
>
> *L6 NA:* gevoelscore not in C-bout-substance's primary cell
> (map's §3 row).

**Parallel worked-example sketch for T-stress-fatigue-pacing**
(the topic's L-IDs per the map's r3 §4 row plus unconditional
L1+L2+L4):

> *Cites L1 (single-subject reach):* per Daza 2018 the topic's
> PARTIALLY CONCORDANT subject-level reading (concave / inverted-
> U direction across both HA-C3 v2 and HA-C3p per guide #3 r2)
> adds one data point to the Wiggers convex-cost-claim's external
> position; the AGREES / EXTENDS / DIVERGES call lands within
> N=1 reach bound, not as group-level settlement. Group-level
> confirmation requires comparable PEM-pacing cohort studies
> (§4.9 external-research track).
>
> *Cites L2 (era confounds):* C-stress-fatigue-shape's two
> member HAs both run Stratum 4 unmedicated only (HA-C3 v2 + HA-
> C3p per the map's §3 row); external pacing literature
> (Wiggers handleiding, broader PEM-pacing sources) typically
> does not span an analogous medication-phase axis; §4.4
> comparability names the medication-phase comparability where
> it shows up. The era-confound bound on the topic's positioning
> is "within-Stratum-4-unmedicated."
>
> *Cites L4 (analyst-is-subject):* HA-C3 v2 + HA-C3p were both
> pre-registered with the Wiggers convex-cost-claim as the
> explicit prior. The topic's positioning call (whether the
> subject's concave / inverted-U finding AGREES or DIVERGES from
> Wiggers' convex-cost) is structurally an L4 question — the
> analyst's Wiggers-prior framing was the test's framing. L4
> mitigation per the limitations-doc r3 §3 L4 caveat: producer-
> mode review + fresh-session `/research-review` bound the L4
> reach; the §6.2 we-diverge-from-consensus conflict rule
> applies if the subject's finding contradicts Wiggers.
>
> *Cites L3 (device generations):* Garmin FR245-derived
> `all_day_stress_avg` operationalises stress vs Wiggers'
> subjective-stress framing in the handleiding (no specific
> instrument named in the source); §4.4 comparability names this
> instrumentation fault-line as a load-bearing or non-load-
> bearing dimension per the §4.5 mapping.
>
> *Cites L6 (self-reporting):* gevoelscore outcome is self-
> reported per L6's binding; external PEM-pacing literature
> typically uses standardized fatigue inventories (CFQ, FSS,
> MFI); §4.4 comparability names this measurement-mismatch as a
> fault-line.
>
> *Cites L7 (survivorship):* HA-C3 v2 + HA-C3p both gate on
> `all_day_stress_avg` non-NaN and `gevoelscore` non-NaN within
> the Stratum 4 unmedicated cell; the gating drops a meaningful
> fraction of unmedicated days; external-literature populations'
> own missingness patterns differ. §4.4 comparability respects
> the missingness-pattern bridge.
>
> *L5 NA:* C-stress-fatigue-shape has no v24 primary signals per
> the map's §3 row (HA-C3 v2 + HA-C3p both use `all_day_stress_avg`
> as predictor and `gevoelscore` as outcome, no v24-derived columns).

**Hard rule.** Artefact missing L1+L2+L4 cannot be locked (§9.6).
Artefact silently omitting an L-ID the map's §4 row lists as
applicable cannot be locked.

### 4.8 Section 8 — Open conflicts preserved with both readings

When any §4.5 positioning is DIVERGES (or CANNOT-SAY with a
substantively-loaded literature-gap), this section preserves the
divergence. **No auto-resolution.**

One paragraph per DIVERGES subclaim: subject's within-subject
reading (cite constituent cluster's joint claim); external-
literature reading (cite consensus position with
`literature/`-relative path-and-section); comparability bound
the call rested on (§4.4 COMPARABLE or PARTIALLY COMPARABLE
with fault-line); candidate explanations (population,
measurement, era, individual variation, methodological
difference — one sentence each with attribution to its
dimension). Resolution paths (NOT executed at Stage S₂): a
literature-gap fill (logged per §6.5 + §4.9 own-research), a
sister-HA moving comparability toward COMPARABLE (§4.9 own-
research), a group-level external-research study (§4.9
external-research with N=1 scoping per §3.11). The divergence
stays open; the §4.5 topic-level summary names it as the
topic's primary substantive finding.

For all-AGREES topic positionings: "No open positioning
conflicts at the topic level; all subclaims converge with
external consensus within the §4.4 comparability bound."

For mixed AGREES + EXTENDS (no DIVERGES subclaim): "No open
positioning conflicts at the topic level; EXTENDS subclaims are
hypothesis-generating-only extensions per §4.5, not divergences."

### 4.9 Section 9 — Follow-up suggestions (own + external tracks) + `open_inputs`

Per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.11, every reviewer-mode-with-authorization artefact closes
with **Follow-up suggestions** in two tracks. Stage S₂'s per-
stage shape per the locked-plan §3.11 "Stage S₂" row:

- **Own-research track**: HAs that would tighten the topic's
  positioning vs the literature; literature-gap entries fed via
  `/fetch-paper`. Concrete pre-reg shapes, not vague directions.
  Worked-example sketch — for T-stress-fatigue-pacing (likely
  positioning DIVERGES against Wiggers monotone-convex per
  guide #3 §5.2's PARTIALLY CONCORDANT cluster reading): a
  third sister-HA on rolling-window-baseline binning would
  tighten C-stress-fatigue-shape; reading Wiggers' convex-cost
  derivation in full (not just summary) would tighten §4.3
  consensus routing. For T-within-day-recovery (likely AGREES
  with within-day-recovery impairment consensus per guide #3
  §5.6's trivial-ORTHOGONAL cluster reading): an unmedicated-
  only sister-HA on `bout_n_did_not_return_day` would move
  comparability toward COMPARABLE on the era dimension; reading
  the relevant within-day-recovery sections of all four primary
  anchors in full is the prerequisite for the topic-level
  positioning to land cleanly.
- **External-research track**: study designs that would settle a
  divergence with consensus (different population, intervention
  arm, instrumentation); consensus gaps that would benefit from
  group-level work. Per locked-plan §3.11 binding scoping
  discipline: **every external-research suggestion MUST
  explicitly name the N=1 limit** (per
  [`research_line_limitations.md`](research_line_limitations.md)
  §3) that prevents us from answering the question ourselves.
  Scoping cites the relevant L-ID from §4.7 (typically L1 for
  group-level confirmation studies; L4 for blinding-required
  designs; L3 for cross-instrumentation work).

Each entry is one paragraph: proposed study; L-ID(s) preventing
self-answer; what the study would contribute to the topic's
positioning.

**The `open_inputs` sub-block** per locked-plan §3.5. Each entry
names: (1) what is missing — literature reference with paper-and-
section, comparability-bridge descriptive run, sister-HA pre-reg,
cross-population data; specific paths / proposed pre-reg slot
names, not vague "more contextualisation"; (2) what it is
blocking — typically Stage A on the construct the topic feeds,
sometimes a tighter §4.5 positioning on this same topic (CANNOT-
SAY → AGREES/EXTENDS/DIVERGES after gap close), sometimes a
tighter §4.3 consensus map (LITERATURE-GAP → CONSENSUS-* after
literature-gap fill); (3) cheapest acquisition path — `/fetch-
paper`, read-the-paper follow-up, sister-HA pre-reg shape,
descriptive run (with effort estimate S ≤ 2h / M = 3-8h / L >
8h per stocktake §3); (4) fallback claim available — at most
one tier narrower per locked-plan §3.5 no-silent-degradation;
for CANNOT-SAY positioning the fallback is "no positioning
recorded; the topic stays at constituent clusters' joint claims
for downstream Stage A."

**Four Stage-S₂-specific refusal-to-proceed paths** produce
`open_inputs` entries (per plan §3.5):

1. **Constituent cluster `cluster-*.md` missing or unlocked** —
   Stage S₂ refuses to start; entry: "Stage S₁ cluster-`<id>`"
   missing → "Stage S₂ on topic-`<id>`" blocked → "run
   `/research-interpret synthesise cluster-<id>`" → fallback
   "none."
2. **Topic not in the synthesis-structure map** — Stage S₂
   refuses to start; entry: "map row for topic-`<id>`" missing
   → blocked → "producer-mode map-update session per locked-
   plan §3.6" → fallback "none." Structurally identical to the
   §6.1 map-change-needed halt.
3. **Literature gap blocks positioning on a load-bearing
   subclaim** — Stage S₂ proceeds with CANNOT-SAY for the
   affected subclaim AND logs to the literature-gap log per
   §6.5; entry: specific paper-and-section missing → "tighter
   §4.5 positioning on subclaim `<X>`" blocked → "/fetch-paper
   + read relevant section" → fallback "CANNOT-SAY recorded."
4. **Comparability cannot be assessed without missing
   literature** — variant of (3). §4.4 cannot land cleanly
   because population/measurement/era detail is not in the
   surveyed literature; Stage S₂ proceeds with NOT COMPARABLE
   (conservative default) → CANNOT-SAY at §4.5; entry: the
   comparability-relevant detail → "tighter §4.4 call" blocked
   → "/fetch-paper for the comparability-relevant reference OR
   read the population-and-methods section of an existing
   reference" → fallback "NOT COMPARABLE / CANNOT-SAY."

The skill aggregates §4.9 `open_inputs` entries into the layer-
wide
[`_open_inputs.md`](_open_inputs.md) queue. Literature-gap
entries additionally propagate to
[`_pending_literature_fetch.md`](_pending_literature_fetch.md).

**Distinct from `open_inputs`** (per locked-plan §3.5 vs §3.11):
`open_inputs` is "what is missing to complete *this current
contextualisation*"; follow-up suggestions are "what *next
claims* could be built — for us or for others." Both required.

**Open inputs do not block completion** per locked-plan §3.8.
Exception: the four refusal-to-proceed paths above produce only
the `open_inputs` entry; the contextualisation itself is not
drafted.

### 4.10 Section 10 — Cross-references

Links out to:

- Each constituent cluster's `cluster-*.md` (the inputs the topic
  contextualisation was built on).
- The synthesis-structure map's §4 topic row (the structural
  pre-registration row reference, not a paraphrase).
- The synthesis-structure map's §5 construct row the topic feeds
  (forward pointer for Stage A; Stage S₂ does NOT cross the
  §3.10 hard predictive gate, only points forward).
- Limitations doc cross-refs for cited L-IDs (per §4.7).
- The literature anchors cited in §4.3 / §4.4 / §4.5 / §4.6 /
  §4.8 with `literature/`-relative paths.
- Literature methodology anchors cited for inference-reach
  bounds — especially Daza 2018 for the N-of-1-to-group reach
  framing (the primary anchor for Stage S₂'s comparability check
  and positioning call); CENT 2015 items 21+22 for the
  limitations and generalisability statements; SCRIBE 2016 for
  L4 participant-as-researcher transparency at the topic level;
  Natesan 2023 for the bar on defensible N-of-1-to-group
  positioning calls; WWC 2022 SCED Standards Handbook for the
  evidence-quality framing the comparability call adapts.
- The literature-gap log
  [`_pending_literature_fetch.md`](_pending_literature_fetch.md)
  for any literature-gap entry the topic surfaced.
- The locked plan §3.6 (conflict-resolution rule); §3.5 (missing-
  inputs flagging); §3.7 (drift policy); §3.8 (completion
  criteria); §3.9 (limitations binding); §3.10 (hard predictive
  gate forward pointer); §3.11 (follow-up suggestions); §3.12
  (commentary boundary — Stage S₂ does not carry); §4 (producer/
  reviewer split table); §6.4 (the spec brief this guide
  implements).
- Guide #1 [`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
  for the upstream verdict-trust chain; guide #2
  [`verdict_to_inference.md`](verdict_to_inference.md) for the
  upstream licensed-claim chain; guide #3
  [`internal_synthesis.md`](internal_synthesis.md) for the
  immediate upstream coherence-call chain.

## 5. The positioning-call mapping rules

This section pins the per-label rules. One worked example per
call rule, drawn from the two active topics in the synthesis-
structure map's r3 (T-stress-fatigue-pacing, T-within-day-
recovery). Per the brief's density-discipline guidance: one
worked example per mapping rule, not multiple alternatives.

### 5.1 AGREES

**Mapping rule.** AGREES applies when: §4.3 is CONSENSUS-EXISTS
(or COMPETING-POSITIONS with the positioning landing on one
position with attribution named); §4.4 is COMPARABLE (or
PARTIALLY COMPARABLE with unmatched dimensions cited as
remaining-reach caveat); the subject's within-subject reading
matches external consensus on direction (and shape / magnitude
within the COMPARABLE bound).

**Bounded by:** §6 caveat 1 (N=1 reach — convergence
observation, not confirmation); §6 caveat 2 (comparability bound
is reach bound); the upstream cluster's coherence call (an
AGREES topic positioning resting on a CONFLICT cluster reading
must name the cluster-level disagreement in §4.6).

**Worked example — T-within-day-recovery AGREES subclaim.** For
the subclaim "bout-level recovery from heavy exertion is
impaired in LC / ME/CFS populations relative to controls" (drawn
from C-bout-substance's joint claim narrowed for the topic):

> §4.3 **CONSENSUS-EXISTS** per the four within-day-recovery
> anchors (Marques 2023, Mooren 2023, Ryabkova 2024, van Campen
> 2022 — relevant sections read in full; LITERATURE-GAP routes
> via §6.5 if not yet).
>
> §4.4 **COMPARABLE** on population (LC subject; anchors cover
> LC + ME/CFS with comparable duration); **PARTIALLY COMPARABLE**
> on measurement (FR245 bout signal vs anchors' CPET / clinical-
> HRV — L3 fault-line cited in §4.7) and era (cross-phase
> pooled vs anchors' typically single-medication-phase cohorts —
> L2 cited in §4.7). Per Daza 2018, PARTIALLY COMPARABLE on
> measurement + era still allows AGREES on direction.
>
> §4.5 **AGREES** on direction; the subject's bout-recovery
> impairment converges with the external consensus as one data
> point (N=1 reach caveat per §6 caveat 1; convergence at the
> functional-impairment level, not at the instrumentation-
> matched level — PARTIALLY COMPARABLE-on-measurement caveat
> carried).

### 5.2 EXTENDS

**Mapping rule.** EXTENDS applies when: §4.3 is CONSENSUS-EXISTS
on a partial / aggregate-level reading; §4.4 is COMPARABLE (or
PARTIALLY COMPARABLE); the subject's within-subject reading
adds shape / detail beyond what the consensus has measured —
typically a finer-grained pattern (within-day / bout-level /
personal-baseline) that the group-level consensus has not
measured at its aggregation level (daily / cohort-average /
single-instrument).

**Bounded by:** hypothesis-generating-only reach per Daza 2018
(does NOT auto-promote to a strong broader-population claim);
§6 caveat 1 applies with extra force (the extension has not
been measured at the group level, so the subject's pattern is
the only evidence for the extension's existence); §4.9 MUST
name follow-up work (own: sister-HA confirming the extension
within-subject; external: group-level study at the extended
resolution).

**Worked example — T-within-day-recovery EXTENDS subclaim.** For
a subclaim derived from C-bout-substance's bout-resolution
finding: "bout-level within-day recovery dynamics show heavy-T-
vs-non-heavy-T discrimination at within-day temporal resolution":

> §4.3 **CONSENSUS-EXISTS** on day-level within-day recovery
> impairment per the four anchors; consensus measures at daily /
> cohort-average resolution (CPET / HRV / RHR), NOT at within-
> day bout resolution.
>
> §4.4 **PARTIALLY COMPARABLE** — population COMPARABLE;
> measurement NOT COMPARABLE at within-day bout resolution
> (consensus has not measured at this temporal resolution); era
> PARTIALLY COMPARABLE (cross-phase pooled). Per Daza 2018,
> measurement-resolution mismatch shifts reach from convergence
> to hypothesis-generating-only-extension.
>
> §4.5 **EXTENDS** — the subject's within-day bout-resolution
> pattern adds a finer-grained measurement of within-day
> recovery dynamics than the consensus has measured.
> Hypothesis-generating-only per Daza 2018. §4.9 own-research:
> sister-HA replicating within-day bout pattern on non-heavy-T
> baseline. §4.9 external-research: group-level study at
> within-day temporal resolution (L1 N=1 limit scoped).

### 5.3 DIVERGES

**Mapping rule.** DIVERGES applies when: §4.3 is CONSENSUS-
EXISTS (or COMPETING-POSITIONS with the positioning
contradicting the dominant or cited position); §4.4 is
COMPARABLE (or PARTIALLY COMPARABLE with unmatched dimensions
not load-bearing for the divergence — if load-bearing,
positioning routes to CANNOT-SAY instead); the subject's
reading contradicts external consensus on direction (or on
shape / magnitude unreconciled by the comparability bound).

**Bounded by:** both readings preserved per §4.8 (subject's
within-subject + external consensus, with attribution, no
auto-resolution); §6 caveat 1 with extra force (DIVERGES does
NOT refute consensus per L1 + Daza 2018, it adds a divergence
data point; reading DIVERGES as refutation is the §7.2 anti-
pattern); candidate explanations enumerated per §4.8 (the five-
dimension list: population, measurement, era, individual
variation, methodological difference — Stage S₂ does not pick
which is correct; enumeration is the substantive output).

**Worked example — T-stress-fatigue-pacing DIVERGES subclaim.**
For a subclaim derived from C-stress-fatigue-shape's PARTIALLY
CONCORDANT inverted-U coherence call (per guide #3 §5.2): "the
stress-fatigue dose-response shape is concave / inverted-U
peaking around mid-stress, NOT the monotone-convex Wiggers
shape":

> §4.3 **CONSENSUS-EXISTS** per Wiggers handbook
> ([wiggers_pacing_handleiding.pdf](../literature/wiggers_pacing_handleiding.pdf)
> lines 1357-1368) on the convex-cost claim (fatigue rises
> monotonically with stress, accelerating at higher values).
> Broader PEM-pacing literature (Appelman 2024; energy-envelope
> literature) carries the weaker energy-envelope framing
> compatible with multiple shapes including inverted-U.
>
> §4.4 **PARTIALLY COMPARABLE** — population COMPARABLE
> (Wiggers addresses LC/PAIS); measurement PARTIALLY COMPARABLE
> (Wiggers' subjective stress vs Garmin `all_day_stress_avg` —
> L3); era PARTIALLY COMPARABLE (no medication-phase
> stratification in Wiggers; HA-C3 v2 + HA-C3p Stratum 4
> unmedicated only — L2). PARTIALLY-COMPARABLE-on-measurement
> is NOT load-bearing for the direction divergence (the
> inverted-U vs convex question is about curvature direction,
> not absolute-value calibration); positioning lands DIVERGES
> rather than routing to CANNOT-SAY.
>
> §4.5 **DIVERGES** on shape — the subject's dose-response is
> inverted-U, NOT monotone-convex. Both readings preserved per
> §4.8 (Wiggers' convex claim with handbook citation AND the
> subject's inverted-U with the cluster's joint claim).
> Candidate explanations enumerated (one sentence each):
> (a) population — Wiggers' observation base may mix LC
> severity profiles with average convex shape but individual
> inverted-U variants; (b) measurement — Garmin sympathetic-
> arousal-load may capture a different construct than Wiggers'
> subjective-stress-rating, with construct-specific dose-
> response; (c) era — Wiggers may predate the energy-envelope
> framing compatible with multiple shapes; (d) individual
> variation — the subject may be in a tail of the dose-response
> distribution; (e) methodological — the binning
> operationalisations may capture a non-linearity Wiggers'
> narrative abstracted away. §4.9 follow-up tracks name what
> would distinguish.

### 5.4 CANNOT-SAY

**Mapping rule.** CANNOT-SAY applies when, for a given subclaim,
any of the following hold:

- The §4.3 consensus-map status is CONSENSUS-DOES-NOT-EXIST AND
  the subject's reading does not align cleanly with any
  competing position (so AGREES / EXTENDS / DIVERGES cannot
  cleanly map).
- The §4.4 comparability-check call is NOT COMPARABLE (auto-
  routes to CANNOT-SAY per §4.4).
- The §4.4 comparability-check call is PARTIALLY COMPARABLE AND
  the unmatched dimensions are load-bearing for the positioning
  (the AGREES / EXTENDS / DIVERGES call would require the
  unmatched dimensions to be COMPARABLE to land cleanly).
- The §4.3 consensus-map status is LITERATURE-GAP — the relevant
  paper has not been read for the specific subclaim, or the
  relevant paper is not yet in `literature/`.

**The CANNOT-SAY call is the layer's no-forced-positioning
discipline.** Per the locked-plan §6.4 spec brief: "CANNOT-SAY is
a valid and preferred outcome over forced positioning." It is
not a failure mode of Stage S₂; it is the correct positioning
when the inputs do not support a cleaner call. The §4.9 follow-
up tracks (own-research and external-research) name what would
unlock a tighter call; the literature-gap log routes the
literature-gap variant via §6.

**Worked example — T-stress-fatigue-pacing CANNOT-SAY subclaim
(literature-gap variant).** For "the inverted-U dose-response
peaks at stress level X (mid-stress) in this subject":

> §4.3 **LITERATURE-GAP** — Wiggers addresses the convex-cost
> shape but not peak-location of any non-monotone alternative;
> broader PEM-pacing literature not yet read for explicit
> peak-location claims. Gap routes to §6.5.
>
> §4.4 N/A pending literature-gap fill.
>
> §4.5 **CANNOT-SAY** pending literature-gap fill. §4.9
> `open_inputs` entry: "read PEM-pacing literature's dose-
> response peak-location claims if any; if none, the gap is
> structural and CANNOT-SAY persists." §4.5 topic-level
> summary carries this subclaim's CANNOT-SAY into the topic
> aggregation.

### 5.5 Multi-subclaim aggregation

When the topic carries multiple subclaims with mixed labels,
the §4.5 topic-level summary paragraph aggregates without
averaging:

- **All-AGREES**: "AGREES with external consensus on `<scope>`
  within the N=1 reach bound."
- **AGREES + EXTENDS**: "AGREES with consensus on `<core
  direction>` and EXTENDS into `<additional shape>` per the
  subject's within-subject pattern, hypothesis-generating-only."
- **Any DIVERGES**: the summary names the divergent subclaim
  explicitly and carries it forward as the topic's primary
  substantive finding; NOT averaged with AGREES into a "mostly
  agrees" label (per §7.12 anti-pattern).
- **All-CANNOT-SAY or majority-CANNOT-SAY**: "CANNOT-SAY on
  `<scope>` pending literature-gap fills and / or
  comparability bridges per §4.9 `open_inputs`."
- **Mixed CANNOT-SAY with other labels** (operationally common):
  the summary names the CANNOT-SAY subclaim(s) explicitly
  alongside the other labels (AGREES, EXTENDS, DIVERGES) — for
  example: "AGREES on `<core direction>` per `<cited consensus>`;
  CANNOT-SAY on `<peak-location subclaim>` pending `<named
  literature gap>`." The literature-gap or comparability gap that
  drove each CANNOT-SAY is recorded as visible to downstream Stage
  A (per §4.9 `open_inputs` block + §6.5 deferred-vs-proceed
  routing). **CANNOT-SAY does NOT wash out** into a topic-level
  call dominated by AGREES / EXTENDS / DIVERGES subclaims — it
  stays named at the topic-summary level, preserving the §6.4
  spec's "CANNOT-SAY is valid and preferred" framing at the
  aggregation layer just as the per-subclaim layer does.

The summary respects the §4.5 hard rule at the per-subclaim
level and does NOT invent a new topic-level label.

## 6. Conflict rules

The contextualisation MUST apply the following conflict rules
when upstream-cluster status, external-literature consensus, and
comparability-bound interact:

### 6.1 Map-change-needed (§3.6 conflict-resolution rule)

> Halt the S₂ session immediately. Do NOT edit the map in-
> session. Route the proposed change to a separate producer-
> mode map-revision session with its own
> `/research-methodology-review` pass before re-lock.

This is the **single most important discipline rule of Stage S₂**,
parallel to guide #3 §6.1's identical rule at Stage S₁. Per
locked-plan §3.6: when per-topic S₂ work reveals the map needs
changing, Stage S₂ HALTS and routes to a separate map-revision
session.

**Concrete halt-criteria.** Stage S₂ halts when any surfaces:

1. **A constituent cluster's coherence call lands the cluster on
   a different construct** than the map's §4 row's shared-
   construct cell declares.
2. **The topic's positioning call would require evidence from a
   cluster not in the map's §4 row** — either the cluster
   belongs in this topic, or the topic membership needs another
   cluster.
3. **The external-literature scope cell is inadequate** — e.g.
   the cell lists Wiggers as primary but the relevant consensus
   lives in literature Wiggers only references peripherally; or
   the cell omits an essential anchor.
4. **The topic-vs-cluster boundary is wrong** — multiple
   clusters grouped in one topic but speaking to different
   consensuses that should be separate topics.

**Route-out instructions.** Stop drafting mid-session; do NOT
save a partial artefact; do NOT edit the map in-session.
Produce only the §4.9 `open_inputs` entry naming the proposed
map change. Hand off to the user with the halt-criterion that
triggered and the proposed change. Resume only after a separate
producer-mode session updates the map with its own
`/research-methodology-review` pass before re-lock. The same
why-this-rule rationale guide #3 §6.1 carries applies here
verbatim at the topic level (the halt-and-route discipline is
what makes the map authoritative; the separate-session
revision is what keeps the re-mapping decision from being
coupled to the very contextualisation results that would be
drafted from it).

### 6.2 We diverge from external consensus

> Record divergence with attribution, no auto-resolution. List
> candidate explanations (population, measurement, era,
> individual variation, methodological difference).

Per locked-plan §6.4: a §4.5 DIVERGES subclaim preserves both
readings (consensus's group-level + subject's within-subject)
with attribution; divergence recorded with the five-dimension
candidate-explanation enumeration; no auto-resolution. §4.8
operationalises both-readings-preservation; §5.3 the DIVERGES
mapping rule; §7.2 explicitly forbids reading DIVERGES as
refutation.

### 6.3 External consensus does not exist

> State that, name the competing positions, place our finding
> among them.

Per locked-plan §6.4: when §4.3 returns CONSENSUS-DOES-NOT-
EXIST (or COMPETING-POSITIONS without a clear dominant
position), Stage S₂ does NOT manufacture a consensus to
position against. §4.3 records the absence-of-consensus status
and names competing positions with citations. §4.5 places the
subject's reading: matching one position → AGREES with
position-attribution explicit; matching none cleanly →
CANNOT-SAY per §5.4; adding shape beyond all positions →
EXTENDS with "extends beyond all current positions" framing.

### 6.4 Comparability fails

> CANNOT-SAY; do not force a positioning call.

Per locked-plan §6.4: §4.4 NOT COMPARABLE auto-routes to
CANNOT-SAY per §5.4. §4.4 PARTIALLY COMPARABLE with load-
bearing unmatched dimensions also routes to CANNOT-SAY as the
conservative default. §4.9 `open_inputs` names the comparability-
bridge that would unlock a tighter call.

### 6.5 Literature-gap blocks positioning

> Log to literature-gap log per
> [`_pending_literature_fetch.md`](_pending_literature_fetch.md);
> defer positioning until acquired OR proceed under CANNOT-SAY.

When §4.3 requires a paper not yet acquired (or not yet read
for the specific subclaim), Stage S₂ logs the gap to the
literature-gap log per the `_pending_literature_fetch.md`
"Candidate paper list" shape (citation, candidate-claim, where
to look, MD section using it). §4.5 on the affected subclaim
routes to CANNOT-SAY pending acquisition; §4.9 `open_inputs`
names the gap.

**Two paths after logging** — the user chooses at §8 interview
or §9.6 gate:

- **Defer positioning until acquired**: §4.5 blocks on the
  affected subclaim; whole topic does not lock until the gap
  is filled. Appropriate when the gap is on a load-bearing
  subclaim where CANNOT-SAY would substantively misrepresent
  the topic's external-positioning surface.
- **Proceed under CANNOT-SAY**: §4.5 records CANNOT-SAY on the
  affected subclaim; the rest of the artefact proceeds. The
  gap is logged for `/fetch-paper`; on acquisition the §9.8
  drift trigger fires and the topic is re-examined.
  Appropriate when the gap is on a non-load-bearing subclaim.

**Operational definition of "load-bearing" at §6.5.** A subclaim
is **load-bearing** here if its consensus map closing would
substantively change the topic's §5 summary-level positioning
between AGREES / EXTENDS / DIVERGES and CANNOT-SAY. That is: if
acquiring the missing literature could move the topic-level call
out of CANNOT-SAY into one of the three positive labels (or vice
versa), the subclaim is load-bearing → defer-until-acquired.
If the topic-level call would stay the same regardless of how the
missing literature lands, the subclaim is non-load-bearing →
proceed-under-CANNOT-SAY on this subclaim while the topic-level
call rests on the other (non-gapped) subclaims.

**Disambiguation from §4.4-sense load-bearing.** The §4.4
comparability check uses "load-bearing" in a different sense —
there it refers to **fault-line dimensions** (age / sex / duration /
severity / device generation) where mismatch between subject and
external population *forces* a comparability-call demotion. The
§6.5-sense is about **subclaim contribution to topic positioning**.
A subclaim can be §4.4-load-bearing (its comparability call drives
the §4.4 COMPARABLE / PARTIALLY / NOT COMPARABLE label) while
being §6.5-non-load-bearing (its CANNOT-SAY wouldn't move the
§5 topic call). The two senses are orthogonal; an audit / drafter
keeps them separate by always citing the section number when
saying "load-bearing."

**Worked examples** for the two active topics:

- *T-stress-fatigue-pacing peak-location subclaim* (where exactly
  the inverted-U peaks for ME/CFS populations vs the subject's
  observed peak around stress 30-40): non-load-bearing at §6.5
  level — the topic-level §5 call (likely PARTIALLY CONCORDANT
  per guide #3 r2's corrected reading) does not pivot on the
  exact peak-location consensus; proceed under CANNOT-SAY on the
  peak-location subclaim; topic locks on the other subclaims
  (inverse-non-monotonicity direction; Wiggers convex-cost
  positioning).
- *Hypothetical Wiggers-direction-divergence subclaim* (does the
  external pacing literature actually claim the convex direction
  Wiggers' handleiding asserts, or do other pacing sources hold
  competing positions?): load-bearing at §6.5 level — if external
  consensus diverges from Wiggers' direction, the topic-level §5
  call shifts substantively (DIVERGES from Wiggers vs AGREES with
  alternative-pacing-tradition); defer-until-acquired; literature-
  gap log for `/fetch-paper` cites the needed papers.

## 7. Anti-patterns explicitly forbidden

The following moves are forbidden in any Stage S₂
contextualisation. One paragraph each per the brief's density-
discipline guidance.

### 7.1 Alignment-by-title-or-abstract without reading the relevant section

Claiming alignment with external literature based on a paper's
title or abstract — without reading the section that actually
addresses the construct — is forbidden. Per the locked-plan §6.4
anti-pattern list and per the broader research-discipline
binding: every external citation in §4.3 / §4.4 / §4.5 must
cite a `literature/`-relative path AND a section reference (e.g.
`marques_2023_lc_cardiovascular_autonomic_dysfunction.pdf §X`).
The drafter is expected to have read the relevant section in
full. The §9.6 refuse-to-lock gate below enforces this through
the citation-format check; the fresh-session
`/research-review` pass is the structural protection against
title-only / abstract-only alignment claims slipping through.

### 7.2 Treating N=1 as refutation of group-level consensus

A DIVERGES finding does NOT refute the external consensus. Per
L1 (single-subject reach; limitations doc §3 L1 "Forbids" row)
and per Daza 2018 N-of-1-to-group inference-reach bounds: an
N=1 finding can add a within-subject data point that diverges
from the consensus, but it cannot, on its own, settle the
consensus question. Reading DIVERGES as "our N-of-1 finds the
truth" is the anti-pattern; both readings stay preserved per
§4.8; candidate explanations stay enumerated per §6.2; the §4.5
DIVERGES positioning records the divergence as a within-subject
data point, not as a refutation. The same anti-pattern variant
appears in the locked-plan §9 layer-level anti-pattern list
("the literature-confirmation fallacy" applied inversely as a
literature-disconfirmation fallacy); the discipline is symmetric:
N=1 cannot confirm and cannot refute group-level consensus on
its own.

### 7.3 Cherry-picking supportive references

Citing only references that support the topic's positioning
while ignoring non-supportive references is forbidden. Per the
locked-plan §6.4 anti-pattern list: the §4.3 consensus map MUST
survey the cited literature scope fully (per the map's §4
external-literature scope cell), not selectively. When the
surveyed scope contains references that support a different
positioning than the one Stage S₂ landed on, those references
are cited in §4.3 (as part of the consensus map's competing-
positions or recent-revision context) and addressed in §4.6
caveats (as part of the structural N-of-1-to-group caveats).
Cherry-picking is the "literature-confirmation fallacy" the
locked-plan §9 layer-level anti-patterns names directly.

### 7.4 Citing a paper for a claim it does not actually make

Citing a paper as supporting a claim that the paper does not
actually make is forbidden. This is the strongest form of the
§7.1 anti-pattern (title-only alignment is one mechanism for
this failure; even after reading the relevant section, the
drafter may misread the paper's claim and cite it for a claim
the paper does not make). The discipline: every citation must
correspond to a claim the paper makes in the cited section,
read in full. The fresh-session `/research-review` pass is the
structural protection (the reviewer re-reads the cited section
cold and checks the claim correspondence); the user's lock
acceptance is the final check.

### 7.5 Smuggling cross-topic context into the current topic's reading

Stage S₂ operates on one topic per session. Cross-topic context —
even when the user has a candidate cross-topic reading (per the
seed notes' cross-cluster speculation, which is explicitly out of
scope for S₁ and remains out of scope for S₂) — does NOT enter
the current topic's §4.3 consensus map, §4.5 positioning, or
§4.7 limitations. Cross-topic reading belongs to Stage A (where
multiple topics may roll up into a single construct per the
map's §5) or beyond. Importing it at S₂ collapses the topic-
bounded scope that keeps positioning calls commensurate across
topics. This is the topic-level analogue of guide #3 §7.4's
cluster-level cross-cluster smuggling anti-pattern.

### 7.6 Inventing new caveats post-hoc

Caveats in §4.6 and §4.7 come from the locked plan §3.10 N-of-1
inference-reach binding (for §4.6) and from the limitations doc
§5 binding's L1+L2+L4 unconditional + L3/L5/L6/L7 as-they-apply
rule (for §4.7). New caveats invented at Stage S₂ time — caveats
that appear neither in the limitations doc, the map row, nor any
constituent cluster's §4.5 — are forbidden. If Stage S₂
identifies a caveat the upstream sources missed, the
[`internal_synthesis.md`](internal_synthesis.md) §7.7 anti-
pattern routing applies at the upstream level (the caveat
surfaces as a Stage S₁ gap and triggers a re-examination of the
relevant cluster's coherence call per the §3.7 drift policy); it
does not enter the topic contextualisation through Stage S₂
prose.

### 7.7 Producing §3.12 subject-narrative commentary at Stage S₂

Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.12 hard separations: commentary lives at Stage A
`construct-*.md` (attached to tier-1 or tier-2 formal claim) and
Stage T patient-audience translation track only. Stage S₂ MUST
NOT carry §3.12 commentary. Wording that reads as subject-
narrative — "I notice that...", "in my experience..." — does not
belong in §4.3 / §4.4 / §4.5 / §4.6 / §4.7. The "bare-narrative-
as-actionability fallacy" (locked-plan §9) is the layer-level
form of this anti-pattern; Stage S₂'s prohibition is the per-
stage form, parallel to guide #2 §7.7 and guide #3 §7.8.

### 7.8 Computing or citing predictive-quality measures

Per locked-plan §3.10: PPV, base rate, sensitivity, specificity,
false-alarm rate, lead time, reliability — these are Stage A's
output, required at tier-2+. Stage S₂ does NOT compute, cite, or
forward-project any of these. The §4.5 positioning records
direction (AGREES / EXTENDS / DIVERGES / CANNOT-SAY), not
diagnostic-quality measures. The forward pointer is Stage A;
Stage S₂ cites the synthesis-structure map's §5 K-construct row
to confirm which tier the construct may reach if all required
evidence lands, but Stage S₂ does not produce the tier's quality
measures itself.

### 7.9 Inventing new positioning or comparability labels

The §4.5 positioning label is drawn from the four-label set
(AGREES / EXTENDS / DIVERGES / CANNOT-SAY). The §4.4 comparability
label is drawn from the three-label set (COMPARABLE / PARTIALLY
COMPARABLE / NOT COMPARABLE). Stage S₂ does NOT invent new
labels. If no label fits cleanly: the §4.5 positioning defaults
to CANNOT-SAY (the default-to-preserve discipline); the §4.4
comparability defaults to NOT COMPARABLE (the conservative
default, which routes positioning to CANNOT-SAY). Labels like
"WEAKLY AGREES", "MOSTLY DIVERGES", "MARGINALLY COMPARABLE" are
forbidden; the fixed label sets are exhaustive for the questions
Stage S₂ addresses.

### 7.10 Uncited external claims floating in the artefact

Every external claim in the topic contextualisation MUST be
either cited (with a `literature/`-relative path-and-section) OR
in the literature-gap log per §6.5. An external claim with no
citation and no literature-gap log entry is forbidden; the §9.6
refuse-to-lock gate below enforces this. This anti-pattern is
the operational form of §7.1 (no alignment from titles /
abstracts) and §7.4 (no citing for unmade claims) — both
underlying disciplines manifest as the no-uncited-floating-
claims requirement at the artefact level.

### 7.11 Re-routing clusters to different topics in-stage

The §3.6 layer-wide map is authoritative for topic membership.
Stage S₂ does NOT propose membership additions or removals during
the contextualisation; that is map-revision-session territory. If
in-stage work reveals a re-mapping need, the §6.1 halt-and-route
rule applies. Editing the map in-session (or silently treating a
cluster as if it were in a different topic than the map
declares) is forbidden. This is the topic-level analogue of
guide #3 §7.1's cluster-level re-routing anti-pattern.

### 7.12 Averaging the divergence in the topic-level summary

When the topic has multiple subclaims with mixed AGREES + DIVERGES
positionings, the §4.5 topic-level summary paragraph does NOT
average them into a "mostly agrees" or "partially diverges"
topic-level label. Per §5.5 multi-subclaim aggregation rule: any
DIVERGES subclaim is carried forward as the topic's primary
substantive finding; the AGREES subclaims appear in the summary
explicitly alongside the DIVERGES, but the divergence is not
averaged away. This is the topic-level analogue of guide #3
§7.2's cluster-level collapsing-CONFLICT anti-pattern.

### 7.13 Asserting substrate-mismatch without verifying the source's named instrument

Recording a §4.4 Measurement substrate-mismatch fault-line (or a
§4.3.5 CONSTRUCT-RELATED / CONSTRUCT-DIFFERENT verdict) on the
inference "the source's wording sounds qualitative" or "the
source does not name a specific instrument" without actually
reading the source's relevant section to verify what instrument
the named metric refers to. The 2026-06-26 Phase A re-open of
`topic-stress-fatigue-pacing.md` absorbed exactly this failure
mode: the dry-run drafter recorded Wiggers's "stress score" as a
subjective rating without verifying that the section in question
(Annual Stress Scores, PDF lines 1357-1368) explicitly names the
Garmin Connect UI metric. Operational binding: §4.3.5 hard rule
3 ("substrate mismatch is NOT a default assumption") plus the
§4.3.5 procedure's step 2 (read the source's operational
definition or UI / instrument citation). Detection: when §4.4
asserts a substrate fault-line, the corresponding §4.3.5 block
must contain the source's instrument-or-UI citation that
warrants the verdict; if absent, the §4.3.5 verdict is
unsupported and routes back to either re-read or
DEFAULTED-PENDING-USER-INPUT.

## 8. Interview-prompt seeds

The `/research-interpret contextualise topic-XXX` skill drives
the contextualisation as an interview. Three required seeds per
the locked-plan §6.4 spec brief, plus an optional fourth.

### 8.1 Consensus existence check

> "Is there published consensus on this construct in LC / ME/CFS
> / PEM populations? What is it? If competing positions exist,
> what are they and who holds them? Which `literature/` paper-
> and-section can you cite, and have you read that section in
> full?"

**Use.** Drives §4.3. Skill presents the map's §4 external-
literature scope cell and walks the user through each subclaim.
For each subclaim: record the consensus-existence call
(CONSENSUS-EXISTS / COMPETING-POSITIONS / CONSENSUS-DOES-NOT-
EXIST / LITERATURE-GAP) and the cited paper-and-section.
LITERATURE-GAP routes to §6.5 and proceeds with CANNOT-SAY-
pending-acquisition or defers per user choice.

### 8.2 Comparability check

> "How close is the external population to your situation
> (age, sex, LC duration, severity, medication phase,
> intervention exposure)? How close is the measurement
> (wearable model, clinical instrument, self-report scale)?
> How close is the era (variant, vaccination, treatment-
> availability)? Where does comparability break, and is the
> break load-bearing for the positioning?"

**Use.** Drives §4.4. Skill presents the §4.3 consensus
statement and walks the user through each dimension
(population, measurement, era). For each: record COMPARABLE /
PARTIALLY COMPARABLE / NOT COMPARABLE with one-sentence cite.
Overall call is the user's; skill defaults to NOT COMPARABLE
on ambiguity per §4.4 hard rule. Skill flags the load-bearing
question explicitly per §5 mapping rules.

### 8.3 Charitable-explanations interview for divergence

> "If our finding diverges from external consensus, what's the
> most charitable explanation for both sides? Which of
> population / measurement / era / individual variation /
> methodological difference do you read as most likely? What
> evidence would distinguish them?"

**Use.** Drives §4.8 where §4.5 positioning is DIVERGES. Skill
presents both readings (subject's within-subject from the
constituent cluster's joint claim AND the external consensus
from §4.3) and walks through the five candidate dimensions.
User's articulation recorded verbatim; skill does NOT auto-pick
(per §6.2). Skill also surfaces the §4.9 follow-up tracks the
enumeration suggests.

### 8.4 Optional seed — topic-trust upstream confirmation

> "The constituent clusters have §4.4 coherence calls of
> [LABEL]. Does the topic's positioning rest on these as fixed
> input, or do you read any cluster's coherence call as needing
> revision before the positioning can land?"

**Use.** Confirmation seed (not discovery) — §4.1 header rows
should mechanically reflect the coherence calls by the time the
skill reaches it. If user articulates upstream-cluster revision
need, skill halts and routes to the Stage S₁ drift trigger (per
guide #3 §9.8); §4.9 `open_inputs` entry carries the request.

## 9. Agent-instruction outline

What `/research-interpret contextualise topic-XXX` (produced in
§11 step 7) codifies into skill behavior. Compact phase-list
form per the brief's density-discipline guidance.

### 9.1 Load

In order: the map's §4 topic row; each constituent cluster's
locked `cluster-*.md`; the external-literature PDFs named in
the map's §4 scope cell; the four N-of-1 methodology anchors
(Daza 2018 / CENT 2015 / SCRIBE 2016 / Natesan 2023) and WWC
2022 SCED; the limitations doc §5 row for `topic-*.md`; the
literature-gap log
[`_pending_literature_fetch.md`](_pending_literature_fetch.md);
upstream guides #1, #2, #3.

### 9.2 Gate

All constituent `cluster-*.md` locked → §9.3. Any missing or
unlocked → halt; produce only §4.9 `open_inputs` entry per
refusal-path 1. Topic not in map → halt; produce only §4.9
entry per refusal-path 2.

### 9.3 Extract

Per cluster: §4.4 coherence call + qualifier verbatim from
`cluster-*.md` §4.1; §4.7a joint-claim sentence verbatim.
Topic-level: map's §4 cells (shared construct, external-
literature scope, L-IDs column, declared-date, lock-version).
Per literature subclaim: relevant section of each cited PDF; if
not yet read, log to literature-gap log and proceed with
LITERATURE-GAP at §4.3.

### 9.4 Interview

Walk §8 seeds in order: §8.1 (consensus existence per subclaim
+ §6.5 literature-gap routing check), §8.2 (comparability check
per subclaim + §4.4 default-to-NOT-COMPARABLE check), §8.3
(charitable-explanations per DIVERGES subclaim), §8.4 (topic-
trust upstream confirmation, if not already at §9.2). For each
seed, record articulation, cross-check against §5 mapping rules
+ §7 anti-patterns, surface mismatches, seek operationalisation-
bound or anti-pattern-cleared rephrasing.

Skill MUST NOT autonomously fill §4.5 (positioning) when §8.2 /
§8.3 surface ambiguity; user picks per §4.5 hard rule (default-
to-CANNOT-SAY). Skill MUST NOT autonomously fill §4.3
consensus-existence; user names the consensus and cites paper-
and-section verbatim, with skill cross-checking against loaded
literature.

### 9.5 Produce

Draft `analyses/contextualisation/topic-XXX.md` following §4.
All ten sections filled; §4.3 consensus map per subclaim with
citations; §4.4 comparability per subclaim; §4.5 positioning
per subclaim + topic-level summary; §4.6 three structural N-of-
1-to-group caveats; §4.7 L1+L2+L4 unconditional + L3/L5/L6/L7
as applicable; §4.8 open conflicts per §4.5 DIVERGES; §4.9 both
follow-up tracks (own + external with N=1 scoping) + the
`open_inputs` sub-block. Status header: DRAFT r1, reviewer-
mode-with-authorization, `## Authorship` per CONVENTIONS §1.2.

### 9.6 Refuse-to-lock gate

Skill refuses to mark ready for completion if any of:

- §4.7 missing L1, L2, or L4.
- §4.7 silently omits an applicable L3/L5/L6/L7 (no NA-with-
  justification).
- §4.3 carries an uncited external claim.
- §4.4 carries an invented label outside three-label set.
- §4.5 carries an invented label outside four-label set.
- §4.8 reads DIVERGES without both-readings preservation (or
  auto-resolution-style language).
- §4.6 missing the three N-of-1-to-group caveats.
- §4.9 external-research suggestion lacks N=1-limit scoping.
- §4.5 topic-level summary averages DIVERGES into AGREES
  without naming divergence as primary finding (§5.5 + §7.12).
- Any §4 section contains anti-pattern violations per §7.

### 9.7 Review handoff

On user-accepted-as-ready-for-completion: recommend fresh-
session `/research-review` per locked-plan §4 (reviewer-mode-
with-authorization artefacts get `/research-review`, not
`/research-methodology-review`). Report lands at
`docs/research/reviews/topic-XXX-contextualisation-YYYY-MM-DD.md`.

### 9.8 Acceptance + drift-trigger registration

Per locked-plan §3.8, "user explicitly accepts" is the binding
completion event. On acceptance: status transitions to LOCKED
with a lock-log entry; §4.9 `open_inputs` entries propagate to
the layer-wide `_open_inputs.md`; literature-gap entries
propagate to
[`_pending_literature_fetch.md`](_pending_literature_fetch.md);
the construct the topic feeds (per map's §5) becomes eligible
for Stage A when all construct-member topics have locked
`topic-*.md`. Per §3.7 drift policy, four re-examination
triggers register at lock:

1. Any constituent cluster's `cluster-*.md` re-examined or
   revised.
2. A new literature reference of moderate-or-higher relevance
   lands (or an existing reference is read in full for a
   previously LITERATURE-GAP subclaim).
3. A cited methodology MD changes lock-version (especially the
   limitations doc; guides #1, #2, #3; any topic-specific
   methodology MDs).
4. ≥6 months elapse since lock.

**Drift-trigger registration is manual-pending-skill.** Until
§11 step 7 lands, the §11 lock log carries a "Drift triggers
registered" line naming the four trigger conditions; a future
drift-check pass walks the lock logs of every contextualisation
to identify triggered topics. Parallels the audit's §9.6,
interpretation's §9.8, synthesis's §9.8, and limitations doc's
§8 patterns (all pending the skill). The skill also increments
the limitations doc's §8 downstream-citation-count table for
each L-ID cited in §4.7 (manual until skill lands).

## 10. Cross-references

- [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  — §6.4 (the spec brief this guide implements); §3 (stage-map
  dependency rule); §3.5 (missing-inputs first-class — four
  refusal-to-proceed paths); §3.6 (map pre-registration + the
  conflict-resolution rule §6.1 here operationalises); §3.7
  (drift policy — four re-examination triggers); §3.8
  (completion criteria for `topic-*.md`); §3.9 (limitations
  binding); §3.10 (hard predictive gate — Stage A forward
  pointer); §3.11 (follow-up suggestions own + external);
  §3.12 (commentary boundary — Stage S₂ does not carry); §4
  (producer/reviewer split table); §9 layer-level anti-patterns
  (literature-confirmation fallacy, unscoped-follow-up fallacy,
  silent-narrowing fallacy); §11 step 6.4 (implementation step
  that produced this guide).
- [`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
  — guide #1, LOCKED r2 2026-06-24; verdict-trust chain Stage
  S₂ inherits via S₁ via I.
- [`verdict_to_inference.md`](verdict_to_inference.md) — guide
  #2, LOCKED r2 2026-06-24; per-HA licensed-claim chain Stage
  S₂ inherits via S₁.
- [`internal_synthesis.md`](internal_synthesis.md) — guide #3,
  LOCKED r2 2026-06-24, the immediate upstream gate. §4
  outline (cluster coherence call feeds §4.1 + §4.3); §4.4
  four-label coherence call Stage S₂ reads as fixed input;
  §4.5 5b cluster L-ID block (Stage S₂'s §4.7 builds on it
  plus unconditional L1+L2+L4); §5 mapping rules (worked
  examples the positioning maps against); §7 anti-patterns
  (especially §7.7 post-hoc caveat invention, which §7.6 here
  mirrors at the topic level).
- [`research_line_limitations.md`](research_line_limitations.md)
  — §3 seven L-IDs; §5 citation requirements for `topic-*.md`
  (L1+L2+L4 unconditional; L3/L5/L6/L7 as they apply); §8
  downstream-citation-count.
- [`synthesis_structure_map.md`](synthesis_structure_map.md) —
  §2 initial scope (two active topics in r3); §3 cluster table
  (constituent clusters as fixed input); §4 topic table
  (Stage S₂'s primary input); §5 construct table (Stage A
  forward pointer).
- [`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md)
  — §4 (four ready HAs feeding the two active topics); §9
  (user decisions shaping the registry).
- [CONVENTIONS.md](../CONVENTIONS.md) §1, §1.2, §2.1, §4.1,
  §4.2, §4.3 as cited throughout this guide.
- Literature methodology anchors at
  [`literature/methodology/`](../literature/methodology/):
  Daza 2018 (primary anchor — N-of-1-to-group reach for §4.4
  + §4.5 + §6); CENT 2015 items 21+22 (limitations +
  generalisability for §4.6 + §4.7 + §4.9); SCRIBE 2016 (L4
  participant-as-researcher transparency for §4.7); Natesan
  2023 (defensibility bar); WWC 2022 SCED v5.0 (evidence-
  quality framing §4.4 adapts).
- Literature anchors for the two active topics — paths cited
  inline in §2 input 3, §4.3 worked example, §5.1-§5.3 worked
  examples.
- [`_pending_literature_fetch.md`](_pending_literature_fetch.md)
  — literature-gap log pattern for §6.5 routing.
- [`hypothesis_lock_process.md`](hypothesis_lock_process.md) —
  §4.9 own-research follow-up sister-HA pre-reg drafting.

## 11. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-24 | Drafted r1 | Producer-mode by fresh agent per §11 step 6.4 of [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md) (r5 LOCKED). Five inventions beyond §6.4 spec: §4.3 four-label consensus-existence status; §4.4 three-label comparability check with Daza 2018 per-label citation; §5.5 multi-subclaim aggregation rule (homogeneous cases only); §6.1 four halt-criteria for map-change-needed halt; §9.6 ten-item refuse-to-lock gate. Two §6.4 ambiguity interpretations: comparability-fails → CANNOT-SAY auto-route + conservative-default; literature-gap two-paths-after-logging with load-bearing-vs-non-load-bearing criterion. Agent flagged §6.5 load-bearing-criterion as strongest invention for reviewer. |
| 2026-06-24 | Fresh-session `/research-methodology-review` | Verdict REVISION RECOMMENDED (mild). Report: [`reviews/methodology-external_contextualisation-2026-06-24.md`](../reviews/methodology-external_contextualisation-2026-06-24.md). Two required (R1: §6.5 load-bearing operational definition + disambiguation from §4.4-sense; R2: §5.5 mixed-CANNOT-SAY-with-other-labels case missing). Four recommended (A1: ~100-line density compression — flagged "for a future revision pass"; A2: §4.4 per-label inference-reach citation refinement; A3: §4.7 parallel T-stress-fatigue-pacing worked example; A4: §11 lock-log scannability + §9.6 count fix). All literature anchors verified; L-ID discipline correct; Daza/CENT framing accurate; CANNOT-SAY-as-preferred enforced; §5.3 DIVERGES example accurate against guide #3 r2's corrected concave-agreement framing. Density discipline partially succeeded (1551 lines vs 1500 upper bound; trajectory reversed ~20% from guide #3's 1939). |
| 2026-06-24 | Revised r1 → r2 | Both required absorbed (R1: §6.5 added operational definition + §4.4-sense disambiguation + two worked examples; R2: §5.5 added mixed-CANNOT-SAY-with-other-labels bullet preserving CANNOT-SAY visibility at the aggregation layer). Three of four recommended absorbed (A2: §4.4 per-label Daza/CENT/WWC inference-reach citations made explicit per COMPARABLE/PARTIALLY/NOT; A3: §4.7 parallel T-stress-fatigue-pacing L-ID worked example added with all six L-IDs plus L5 NA; A4: this lock-log split + clarification). A1 density compression deferred per reviewer's "for a future revision pass (not blocking)" framing; future r3 may execute the ~100-line compression if friction surfaces during dry-run. §9.6 count clarified as ten structural checks. |
| 2026-06-24 | **LOCKED r2** | User acceptance ("Absorb all (2 required + 4 recommended), lock r2, dispatch guide #5 with density signal"). Status of all sections LOCKED. Implementation proceeds to §11 step 6.5 (guide #5 `actionability_translation.md`). No second-pass review per established Option-γ pattern. **Drift triggers registered** (manual-pending-skill): constituent `cluster-*.md` re-examined; new literature-gap fill via `/fetch-paper`; cited methodology MD changes lock-version (especially research_line_limitations.md, synthesis_structure_map.md); ≥6 months elapse since lock. |
| 2026-06-26 | Drafted r2 → r3 | Addition cycle absorbing the 2026-06-26 Phase A re-open's construct-validity-of-named-metric miss on `topic-stress-fatigue-pacing.md`. Three changes: (1) NEW §4.3.5 Construct-identity check interpolated between §4.3 Consensus map and §4.4 Comparability check — three-label verdict set CONSTRUCT-IDENTICAL / CONSTRUCT-RELATED / CONSTRUCT-DIFFERENT with hard rules, dispatch-mode placeholders, and the Wiggers-stress-score × Garmin-`all_day_stress_avg` worked example as cautionary tale + corrected verdict; (2) §4.4 lead-in cross-reference sentence wiring §4.3.5 verdict into §4.4 Measurement fault-line constraint; (3) NEW §7.13 anti-pattern "Asserting substrate-mismatch without verifying the source's named instrument" pointing back to §4.3.5 hard rule 3 + procedure step 2. No renumbering of §4.4-§4.10 (interpolated as §4.3.5 to preserve all downstream cross-references in artefacts citing the LOCKED-r2 anchors). Origin: 2026-06-26 user-flagged miss on the patient-audience translation's hedge wording surfaced a misframing in the LOCKED-r1 `topic-stress-fatigue-pacing.md` §4.4 Subclaim 1 Measurement call; root cause was the absence of a construct-identity verification step between §4.3 and §4.4. |
| 2026-06-26 | Fresh-session `/research-methodology-review` (scoped to r2→r3 diff) | Verdict REVISION RECOMMENDED (mild). Report: [`reviews/methodology-external_contextualisation-r2-to-r3-2026-06-26.md`](../reviews/methodology-external_contextualisation-r2-to-r3-2026-06-26.md). One required (R1: §4.3.5 dispatch-mode placeholder names diverged from SKILL.md r4's locked vocabulary — invented `LITERATURE-GAP-FROM-§4.3` and `PROXY-CITED-USER-ACCEPTED-{date}` instead of reusing `LITERATURE-GAP` upstream-inherit and `PROXY-CITED-IN-DRY-RUN`). Two recommended (A1: hard rule 2's default-to-CONSTRUCT-RELATED cites internal_synthesis §4.4 as analogue but that analogue defaults to CONFLICT — the design-divergence warrants one explicit sentence; A2: worked-example's L3 attribution covers three semantically distinct fault-lines that stretch L3's hardware-upgrade-triggered scope — flag as L3-expansion-vs-L8 decision for limitations-doc maintainer). Reviewer independently verified the Wiggers-stress = Garmin-Connect-UI claim via three textual anchors in the §C C3 verbatim; CONSTRUCT-IDENTICAL verdict warranted. All five design-choice rulings: 4 sound + 1 sound-with-concern (the A1 default-divergence). |
| 2026-06-26 | Revised r2 → r3 (post-review) | All three findings absorbed. R1: renamed §4.3.5 dispatch-mode placeholder block to reuse SKILL.md r4 vocabulary verbatim — `LITERATURE-GAP-FROM-§4.3` → `LITERATURE-GAP` (upstream-inherit from §4.3 fourth-label status; no §4.3.5-specific name); `PROXY-CITED-USER-ACCEPTED-{date}` → `PROXY-CITED-IN-DRY-RUN` (SKILL.md Stage S₂ vocabulary; verification date moved to accompanying one-sentence cite); `DEFAULTED-PENDING-USER-INPUT` + `SKIPPED-AS-DRY-RUN-DEFAULT` retained verbatim. Block lead-in explicitly names "no §4.3.5-specific placeholder names; SKILL.md is the single source of truth" to prevent future vocabulary drift. A1: hard rule 2 expanded with one-sentence rationale acknowledging the divergence from internal_synthesis §4.4's most-conservative default and naming the bidirectional §7.13 failure mode as the reason the middle is right for construct-identity specifically. A2: worked-example L3 enumeration expanded with one sentence flagging L3-expansion-vs-L8 (vendor-algorithm-population-validity) decision to the limitations-doc maintainer as separate from this r3 lock cycle. |
| 2026-06-26 | **LOCKED r3** | User acceptance ("all" — absorb all three findings, lock r3). Status of all sections LOCKED including the three r3 additions (§4.3.5, §4.4 lead-in cross-ref, §7.13). **Drift triggers registered** (manual-pending-skill r5 absorption): SKILL.md r5+ dispatch-mode vocabulary changes (R1 absorption pinned §4.3.5 to SKILL.md r4 names — vocabulary drift re-opens §4.3.5); `research_line_limitations.md` L3 expansion or L8 addition lands (A2 worked-example attribution re-evaluates); constituent `cluster-*.md` re-examined; new literature-gap fill via `/fetch-paper`; ≥6 months elapse since lock. **Next action downstream**: Phase A re-open of `topic-stress-fatigue-pacing.md` (+ inheriting artefacts) using §4.3.5 as the authority for the construct-validity correction; skill r5 absorption queues a fourth friction item — "before introducing dispatch-mode placeholders in any methodology MD, grep SKILL.md for locked vocabulary and reuse names verbatim" (the R1 failure mode). |
