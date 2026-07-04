# Internal synthesis — Stage S₁ guide

**Status**: **LOCKED r2** by user acceptance 2026-06-24. r1 authored
2026-06-24 by a fresh agent per §11 step 6.3 of
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
(r5 LOCKED 2026-06-24). r1 → r2 absorbed a fresh-session
`/research-methodology-review` (verdict REVISION RECOMMENDED, report at
[`reviews/methodology-internal_synthesis-2026-06-24.md`](../reviews/methodology-internal_synthesis-2026-06-24.md))
that caught two fact-bug required actions (R1: §5.2 + §5.3 worked
examples mischaracterised HA-C3 v2 as "monotone-inverse" when actual
result.md detects same inverted-U as HA-C3p; R2: §3 L-ID worked
example for cluster-bout-substance.md over-extended the "if cluster
members are from different era strata" rule to within-member cross-
phase pooling) and four recommended/optional actions (single-member
trivial-ORTHOGONAL semantic clarification; per-cluster thin-S₁-vs-
skip-with-stub determination; length compression; prefix-drop
naming-translation sentence). All required + recommended absorbed
in r2. Implementation proceeds to §11 step 6.4 (guide #4
`external_contextualisation.md`).

This guide is the third of six binding methodology MDs for the
results-analysis layer. It governs **Stage S₁** (internal synthesis):
the per-cluster artefact that takes the locked `interpretation.md`
files of a cluster's constituent HAs and produces a single
**coherence call** at the cluster level, drawn from a fixed label
set (CONCORDANT / PARTIALLY CONCORDANT / CONFLICT / ORTHOGONAL).
It sits between Stage I's per-HA `interpretation.md` files (its
direct upstream gate) and Stage S₂'s per-topic `topic-*.md`
contextualisation artefacts (its direct downstream consumer). It
refuses to start on a cluster whose constituent HAs lack locked
`interpretation.md` artefacts, on a cluster that is not pre-declared
in the synthesis-structure map, and on a cluster whose upstream
cascade-arrow precondition (where one exists) is not yet locked.

---

## 1. Purpose

> **A cluster of related HA verdicts is not a chorus. Stage S₁
> produces a single coherence call, drawn from a fixed label set,
> that says how the cluster's per-HA interpretations sit against
> each other at the construct level — preserving conflicts where
> they exist, refusing to average them into a "middle" reading.**

Many HAs touch overlapping constructs (stress-fatigue shape across
two bin-scheme operationalisations; within-day recovery substance
sitting downstream of a framework-validity precondition). Treating
each HA as independent loses information: two HAs running on the
same underlying signal under different operationalisations are two
pieces of evidence about that construct, and the cluster reading is
the layer's commensurate vehicle for that. Treating a cluster as a
single chorus risks the opposite failure: averaging away a
substantive disagreement to produce a "middle" claim neither
constituent HA supports.

Stage S₁ is the per-cluster discipline gate that closes both
failure modes at once. Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3 stage-map: `D → I → S₁ → S₂ → A → T`. Stage S₁ sits immediately
downstream of Stage I and immediately upstream of Stage S₂. Stage
S₂ refuses to start on a topic whose constituent clusters lack
locked `cluster-*.md` artefacts; Stage A inherits the cluster-level
reading via the construct → topic → cluster rollup in the synthesis-
structure map. The commensurability discipline Stage I establishes
across HAs is what lets Stage S₁ produce coherence calls that mean
the same thing across clusters; the coherence-call discipline Stage
S₁ establishes is what lets Stage S₂ position the project's findings
against external literature without smuggling cluster-internal
disagreement into the comparison.

**What Stage S₁ does NOT do.**

- It does NOT re-test the hypothesis or any cluster member's
  verdict. The verdicts come from each member HA's `result.md` (via
  Stage D's verdict-trust gate and Stage I's licensed-claim
  translation) and are read as fixed inputs; Stage S₁ does not
  relabel, does not re-score, does not re-run.
- It does NOT produce predictive claims. Per
  [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  §3.10 hard predictive gate: predictive-tier claims live at Stage
  A and require a pre-registered forward-validation HA. Stage S₁
  produces no PPV, no base-rate framing, no diagnostic-quality
  measures, and no "forecasts Y" wording. The forward pointer is
  Stage A via the synthesis-structure map's §4 topic → §5 construct
  rollup; this is not Stage S₁'s surface.
- It does NOT carry subject-narrative commentary. Per
  [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  §3.12, commentary lives at Stage A `construct-*.md` (attached to
  a tier-1 or tier-2 formal claim) and Stage T patient-audience-
  track only. Stage S₁ artefacts are forbidden from carrying §3.12
  commentary; the same epistemic-category-separation discipline
  guide #2 enforces at Stage I carries through here.
- It does NOT invent new caveats post-hoc. Stage S₁ draws caveats
  from each member HA's locked `interpretation.md` §4.5 (the L-ID
  citation block + pre-reg + audit caveats) and from the synthesis-
  structure map's §3 cluster row's L-IDs column. New caveats
  invented at Stage S₁ time — caveats that appear neither in any
  member interpretation nor in the map row — are forbidden by §7.4
  below.
- It does NOT re-route HAs to different clusters in-stage. Per the
  locked plan's §3.6 conflict-resolution rule (map vs §6.3 per-
  cluster pre-declaration): if Stage S₁ work reveals the map needs
  changing, Stage S₁ **HALTS** and routes to a separate producer-
  mode map-revision session with its own
  `/research-methodology-review` pass before re-lock. The map is
  authoritative for cluster name, constituent-HA list, and topic/
  construct rollup; Stage S₁'s job is to read what the map declared,
  not to revise it. §6.1 below operationalises the halt-criteria
  and route-out instructions.
- It does NOT operate on more than one cluster per session. The
  cluster-bounded scope is what keeps coherence calls commensurate
  across clusters. Cross-cluster cross-references belong at Stage
  S₂ (against external-literature topic) or beyond.

**Alternatives considered** (per CONVENTIONS §2.2 four-input bar
item 3: tradeoff vision). The natural alternative is to fold the
cluster-level synthesis into the [RESEARCH-REPORT-ADDENDUM](../RESEARCH-REPORT-ADDENDUM.md)
chain (every new HA appends a section to the addendum which then
discusses how it sits against prior HAs). That was rejected for the
same two reasons guides #1 and #2 cited for their respective
upstream stages: (a) addendum-as-synthesis collapses the producer-
vs-reviewer-mode split (the addendum is a running narrative
producer artefact; the cluster coherence call is a reviewer-mode-
with-authorization claim that gets a fresh-session `/research-
review` peer check per the locked-plan §4 split), and (b) addendum-
embedded synthesis makes commensurability across clusters harder —
the same coherence-call mapping rules applied uniformly across the
corpus is the cheap commensurate discipline. A second alternative
— producing only at-the-construct-level Stage S₂ outputs and
skipping S₁ entirely (treating every multi-HA cluster as the
cluster + topic + construct contextualisation chain reading
together) — was rejected because Stage S₂ would then have to do
two jobs at once: cluster-internal coherence AND external-
literature positioning. Separating those is what lets Stage S₂'s
CANNOT-SAY (a valid positioning outcome per locked-plan §6.4) be
a comment on external-literature coverage, not a comment on
cluster-internal disagreement; cluster-internal disagreement is
S₁'s CONFLICT call, which is a different epistemic category.

**Precondition: the `/research-interpret` skill must land first.**
This guide specifies *what* a Stage S₁ synthesis must do; it does
not specify *how* the skill produces one. Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§11 step 7, the `/research-interpret` skill is built after the six
guides (this guide is #3 of six). **No Stage S₁ synthesis artefact
can be drafted before §11 step 7 lands** — this guide alone is
necessary but not sufficient. The §9 agent-instruction outline
below is the skill's brief; the skill build (step 7) operationalises
it.

## 2. Inputs

The synthesis MUST load and use the following inputs, in this order:

1. **The cluster's constituent HA `interpretation.md` files** — all
   of them, all locked (per locked-plan §3 dependency rule: "`S₁`
   on a cluster refuses to start until every HA in the cluster has
   a current `interpretation.md`"). The interpretations are the
   layer's commensurate licensed-claim surface: their §3 ("what the
   verdict licenses"), §4 ("what the verdict does NOT license"),
   §5 (caveats narrowing the claim, including the L-ID citation
   block), §6 (lived-experience prior reconciliation), §7 (closure-
   path statement for PARTIAL / INCONCLUSIVE), and §8 (follow-up
   suggestions, own + external tracks) feed Stage S₁ directly.
   Stage S₁ reads each interpretation as a fixed input — it does
   NOT renegotiate the licensed claim, the caveats, or the prior
   reconciliation.
2. **The synthesis-structure map
   [`synthesis_structure_map.md`](synthesis_structure_map.md)'s §3
   cluster row for the target cluster** — the row encodes the
   cluster name, the constituent-HA list, the shared construct, the
   operationalisation-overlap note (the cluster's evidence-strength
   rationale: independent operationalisations vs same-signal multi-
   takes), the L-IDs column (the limitations every member's
   interpretation cited that Stage S₁ MUST cite at the cluster
   level), the literature anchor (for cluster-row context, not for
   Stage S₂'s external-literature positioning), the cascade-arrow
   language where applicable (per the map's `C-bout-framework →
   C-bout-substance` cascade in r3), and the row's declared-date +
   lock-version (which §4.2 of the produced `cluster-*.md` cites
   verbatim — the pre-declared constellation is read from the map,
   not re-derived in-stage). Plus the §4 topic row the cluster
   feeds, for the §4.9 cross-references section pointing forward.
3. **The relevant methodology MDs** — at minimum
   [`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
   (guide #1, the upstream verdict-trust chain),
   [`verdict_to_inference.md`](verdict_to_inference.md) (guide #2,
   the immediate upstream gate),
   [`research_line_limitations.md`](research_line_limitations.md)
   (the L-ID source), and any cluster-specific methodology MD the
   constituent HAs' interpretations cite (e.g.
   [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md)
   for C-bout-substance / C-bout-framework;
   [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)
   for HA-C4c's cross-phase pooling; the Wiggers handbook for
   C-stress-fatigue-shape per the map's §3 literature-anchor cell).
4. **The cascade-arrow upstream cluster's `cluster-*.md` artefact,
   where one exists** — per the map's §3 cascade-arrow language,
   C-bout-substance reads C-bout-framework as caveat-class
   precondition (not co-equal verdict). Stage S₁ on C-bout-substance
   refuses to start without C-bout-framework's locked `cluster-*.md`
   in hand (§6.2 conflict rule below). For clusters without a
   cascade-arrow precondition (C-stress-fatigue-shape; C-bout-
   framework itself), this input is NA and the §4.5 "what the
   cluster jointly licenses" section omits the cascade-precondition
   sub-paragraph.
5. **Any prior synthesis seed notes** — currently
   [`_synthesis_seed_notes_2026-06-23.md`](_synthesis_seed_notes_2026-06-23.md),
   which carries the r1 map-drafter's candidate joint-reading
   sketches for C-stress-fatigue-shape and C-bout-substance.
   **Advisory only**, per that file's own status header AND per the
   synthesis-structure map's §3 note relocating the sketches out of
   the map's structural pre-registration. Stage S₁ MAY use these
   notes as caveat-class context OR ignore them entirely; either
   choice is methodologically correct. They are **not constraints
   on the coherence call**. §7.5 below makes this discipline an
   explicit anti-pattern (treating seed-notes sketches as
   constraints).
6. **The Stage D `descriptive_audit.md` files** for every cluster
   member HA, via the verdict-trust status chain Stage I inherited.
   Stage S₁ does NOT re-read the audit's per-assumption rows; that
   was Stage I's job (and Stage I refused to start if the audit was
   missing or REQUIRES-DESCRIPTIVE-WORK). Stage S₁ reads only the
   §1 header line of each member interpretation that records the
   Stage D verdict-trust call (TRUSTED / DOWNGRADED-INCONCLUSIVE-
   PROVISIONAL with explicit user acceptance), and uses that as
   the cluster-level upstream-trust status (the cluster cannot
   reach CONCORDANT or PARTIALLY CONCORDANT with confidence if
   one or more members are running on a PROVISIONAL audit; §5
   below operationalises this).
7. **CONVENTIONS** — in particular [§1](../CONVENTIONS.md#1-roles)
   (the reviewer-mode-with-authorization mode this artefact carries
   per the locked-plan §4 producer/reviewer split table);
   [§2.1](../CONVENTIONS.md#21-descriptive-before-inference)
   (descriptive-before-inference; the Stage D → Stage I → Stage S₁
   chain inherits this); [§3.4](../CONVENTIONS.md#34-crash-drop-sensitivity-row-on-every-layer-4-correlation)
   (crash-drop sensitivity row — relevant to cluster-level reading
   when cluster members' verdicts diverge on the crash-included vs
   crash-dropped frame; Stage S₁ surfaces such divergences as
   cluster-internal evidence rather than averaging them away);
   [§4.1](../CONVENTIONS.md#41-no-interpretive-marks-on-raw-layers)
   (no interpretive marks on raw descriptive layers — Stage S₁
   cites Stage I's licensed claims, never reaches back through to
   the raw descriptive layer to overlay marks); [§4.2](../CONVENTIONS.md#42-caveats-vs-a-priori-claims)
   (caveats vs a-priori claims — caveat what the cluster did not
   do, do not claim what the cluster did not earn); [§4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory)
   (prior-driven hypotheses are confirmatory — when a cluster's
   members are prior-driven, Stage S₁ inherits the confirmatory
   reach-bound from each member's Stage I §4.6 reconciliation, and
   the cluster's joint claim respects that bound).
8. **Literature methodology anchors** — the four N-of-1 reporting
   and inference standards under
   [`literature/methodology/`](../literature/methodology/) that
   bound how an N-of-1 cluster speaks to a construct.
   [Daza 2018](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)
   is the **primary anchor for Stage S₁** because its N-of-1
   multi-test synthesis discipline directly addresses the question
   Stage S₁ asks: how do multiple within-subject tests on the same
   construct combine into a single statement at the within-subject-
   construct level (not a group-level claim — that is Stage S₂'s
   external-literature positioning surface)?
   [Shamseer / CENT 2015](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf)
   item 21 (limitations stated explicitly) and item 22
   (generalisability) feed the §4.5 and §4.8 sections.
   [Tate / SCRIBE 2016](../literature/methodology/tate_2016_scribe_single_case_reporting.pdf)
   participant-as-researcher transparency feeds the L4 citation at
   §4.5. [Natesan 2023](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf)
   sets the bar for what counts as a defensible cluster-level
   coherence call when within-subject multi-test evidence is the
   substrate.

The synthesis does NOT load: any member HA's `test.py` or `result-
data.json` (those were Stage D and Stage I inputs; Stage S₁ works at
the licensed-claim summary level the interpretations report); the
raw descriptive runs that backstopped the audits (those were Stage
D inputs; Stage S₁ inherits the verdict-trust call chain via the
interpretation §1 header); other clusters' `cluster-*.md` artefacts
beyond the cascade-arrow upstream precondition (cross-cluster
reading is Stage S₂ or beyond).

## 3. Output

The synthesis produces exactly one artefact per cluster:

```
docs/research/analyses/synthesis/cluster-XXX.md
```

**Naming convention.** One file per cluster at the top level of
`analyses/synthesis/` — **no per-cluster subfolder**. The cluster
name in the filename is the cluster's exact ID from the synthesis-
structure map's §3 row (e.g. `cluster-stress-fatigue-shape.md`,
`cluster-bout-framework.md`, `cluster-bout-substance.md` for the
three active clusters in the map's r3). The flat naming matches the
locked plan's §5 output-structure tree exactly:
`analyses/synthesis/cluster-XXX.md`. Revision history of the
synthesis lives in the file's own §11 lock log (per §11 below);
revisions to any constituent member HA's `interpretation.md`
re-trigger this artefact per the §3.7 drift policy from the
locked plan.

For clusters that contain a single member HA today and may grow
later (RESERVED-slot clusters in the map's r3 — C-h05-successor,
C-hrv-proxy), Stage S₁ does NOT draft a synthesis until the cluster
has at least one member HA whose `interpretation.md` is locked AND
the cluster's status in the map has transitioned RESERVED → LOCKED.
A single-member cluster's S₁ may collapse to a thin synthesis whose
coherence call is structurally trivial (a one-HA cluster cannot
have inter-HA coherence; §5.6 below describes the trivial case),
but it is still produced — the cluster-level L-ID citation block,
the cascade-arrow handling if applicable, and the topic-cross-
reference still need to land for downstream Stage S₂ to consume.
Per the locked plan §3 dependency rule: skipping S₁ is allowed only
when "structurally trivial" AND an explicit `stage_skipped.md` stub
records why. For single-member clusters, the choice between "thin
S₁" and "skipped-with-stub" is the user's at the moment the cluster
becomes eligible — both options are valid; the choice is recorded
in the §11 lock log.

**Mode.** The artefact is **reviewer-mode-with-authorization** per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§4 producer/reviewer split table. It is drafted by Claude under
user authorization via the `/research-interpret synthesise cluster-
XXX` skill invocation, and it carries a `## Authorship` block per
[CONVENTIONS §1.2](../CONVENTIONS.md#12-producer-vs-reviewer-mode).
It receives a fresh-session `/research-review` pass before lock per
the locked-plan §4 row for `cluster-*.md` — this is the same
reviewer-mode-with-authorization discipline Stage I's
`interpretation.md` files carry, and is distinct from Stage D's
producer-mode audits (which receive no fresh-session review pass).
The fresh-session review check is the structural protection that
lets the cluster's coherence call land as a layer-level commensurate
output.

**L-ID citation discipline at the output level.** Per
[`research_line_limitations.md`](research_line_limitations.md) §5
table row for `cluster-*.md`:

> *Cite every limitation that touches any cluster member; also cite
> L2 if cluster members are from different era strata.*

This is binding on every Stage S₁ artefact. The §4.5 section of the
synthesis outline below (cluster-level caveats narrowing the joint
claim) is where the L-ID citation block lives. Stage S₁ does NOT
cite limitations freely — it draws from the seven L-IDs and applies
each in one sentence to the **cluster-level** specific claim (not
the per-HA specific claim, which Stage I already cited). The
cluster-row L-IDs in the synthesis-structure map's §3 are the
union of L-IDs the constituent HAs' interpretations cited; Stage
S₁ cites that union PLUS the L2-era-strata-mismatch citation when
the cluster spans different era strata (per the limitations-doc §5
binding's "also cite L2" clause for cluster artefacts).

**Worked example for the three active clusters in the map's r3.**
- `cluster-stress-fatigue-shape.md` cites L1, L2, L3, L4, L6, L7
  (the C-stress-fatigue-shape row's L-IDs column; L5 NA — no v24
  primary signals). Members HA-C3 v2 + HA-C3p both run Stratum 4
  unmedicated only, so no extra L2 era-strata-mismatch citation
  is triggered beyond the per-HA L2 each interpretation already
  cited.
- `cluster-bout-framework.md` cites L1, L2, L3, L4, L6, L7 (L5
  NA). Single member HA11-bout-redo runs unmedicated × train; no
  era-strata-mismatch within the cluster.
- `cluster-bout-substance.md` cites L1, L2, L3, L4, L7 (L5 NA;
  L6 NA — gevoelscore not in primary cell). Single member HA-C4c
  runs cross-phase pooled (unmedicated + buildup + consolidation
  + afbouw + post_afbouw), §4.10 unmedicated-only sensitivity
  arm. Per the per-HA L-ID Stage I already cited, the cluster's
  L2 citation flows through HA-C4c's interpretation.md cite —
  **no extra L2-era-strata-mismatch cluster-level citation is
  triggered**. The limitations-doc r3 §5 "also cite L2 if cluster
  **members** are from different era strata" clause applies when
  **plural HA members** sit in different era strata at the cluster
  level — it does NOT extend to within-member cross-phase pooling
  inside a single HA. C-bout-substance is single-member; the
  cross-phase pooling is HA-C4c's own L2-era-confound surface
  (Stage I already cites it per the per-HA L-ID block), not a
  cluster-level L2 extension. The cluster row's operationalisation-
  overlap-note flags the cross-phase pooling as "structural to
  each cluster's question, not a confound to reconcile away" —
  reading this as a cluster-level L2 trigger would over-extend
  the limitations-doc binding. If a future revision wants to
  capture within-member sub-strata as a cluster-level L2 surface,
  that requires an explicit limitations-doc lock-version bump
  amending §5, not an interpretive stretch at Stage S₁.

**Hard rule.** A Stage S₁ artefact whose §4.5 L-ID block is empty
(or whose §4.5 omits an L-ID the map's cluster row lists) is
incomplete and the skill (per §9 refuse-to-lock gate below) refuses
to mark it complete. The L-ID citation block is the layer's
commensurability guarantee at the cluster level; an artefact
without it cannot be cited by downstream Stage S₂ as having
respected the systemic context.

**Hard rule.** Stage S₁ MUST NOT cite an L-ID it does not apply
to. A citation that reads "L5 (presence-conditioned data layer)
NA" without an explanation is forbidden; the NA call requires the
same one-sentence cluster-level project-specific reason as the
apply call.

## 4. Section outline for the produced `cluster-XXX.md`

The artefact MUST contain nine sections in this order, plus the
§4.5 L-ID citation block (which is operationally a sub-section of
§4.5 caveats) and the §4.7 follow-up-suggestions block. Each
section's operational guidance follows.

### 4.1 Section 1 — Cluster name + constituent HAs (with verdicts)

Mechanically copy from the synthesis-structure map's §3 cluster
row + each member HA's `interpretation.md` §1 header:

- Cluster ID + cluster name (verbatim from map's §3 row).
- Member HA list (verbatim from map's §3 "Constituent HAs" cell).
- For each member HA: HA ID + the headline verdict from the
  member's `interpretation.md` §1 (which itself was copied verbatim
  from result.md; no relabeling at this stage). For verdicts with
  qualifiers (HA-C4 v2's "REJECTED (triad sum = 0.0 / 3.0)",
  HA-C3 v2's "REJECTED (wrong-direction override)", HA-C3p's
  "PARTIAL (2-of-3 conditions MET)", HA11-bout-redo's "PARTIAL
  (2 of 3 framework-validity bars met)"), carry the qualifier
  verbatim per guide #2 §5.5 verbatim-qualifier rule.
- For each member HA: the Stage D verdict-trust call from the
  member's `interpretation.md` §1 (TRUSTED / DOWNGRADED-
  INCONCLUSIVE-PROVISIONAL).
- The cluster's shared construct cell from the map's §3 row
  (verbatim).
- The cluster's operationalisation-overlap-note cell (verbatim;
  this is the cluster's evidence-strength rationale and feeds §5
  coherence-call rules below).
- Where applicable, the cascade-arrow language from the map's §3
  row (e.g. for C-bout-substance: "C-bout-framework's verdict
  propagates as caveat-class precondition; see §4.5 below").

This section is a header, not analysis. Its purpose is to fix the
cluster target so the rest of the synthesis is unambiguous about
which cluster, which members, which verdicts, and which upstream-
trust statuses it operates on.

### 4.2 Section 2 — Pre-declared constellation

Cite the synthesis-structure map's §3 cluster row directly, naming
the row's **declared date** and **lock version**. The cluster's
constituent-HA list is read from the map's §3 row at this version;
Stage S₁ does NOT re-decide the constellation in-stage. The §4.2
paragraph reads (template):

> *Pre-declared constellation* (per
> [`synthesis_structure_map.md`](synthesis_structure_map.md) §3
> row `<cluster-id>`, declared `<YYYY-MM-DD>`, lock version
> `<rN>`): the cluster groups HA-`<X>`, HA-`<Y>`, ... on the shared
> construct `<construct>` because `<one-sentence overlap-note
> rationale from the map's row>`. The constellation was locked at
> the layer-wide map's §7 lock-log entry `<date>` and has not
> changed since. This Stage S₁ session reads the constellation
> from the map row; it does not propose a constellation change.

For clusters with cascade-arrow language (currently C-bout-
substance, which reads C-bout-framework as caveat-class
precondition per the map's §3 row), the §4.2 paragraph adds a
second sentence naming the cascade:

> *Cascade-arrow precondition* (per the map's §3 row for
> C-bout-substance): C-bout-framework's `cluster-bout-framework.md`
> verdict propagates as caveat-class precondition into this
> cluster's coherence call (not as a co-equal verdict S₁
> reconciles against). See §4.5 below for the cascade-precondition
> sub-paragraph and §5.5 below for the cascade-handling rule in
> the coherence-call mapping.

**Hard rule.** The §4.2 paragraph cites the map row's declared-date
and lock-version verbatim. It does NOT re-derive the constellation,
does NOT add or remove constituents, and does NOT propose a re-
clustering. If Stage S₁ work reveals a re-clustering need, the
session HALTS per §6.1 below; the §4.2 paragraph cannot be the
surface where a re-cluster lands in-stage.

### 4.3 Section 3 — Per-HA verdict + interpretation row

One row per cluster member HA. Each row carries:

- HA ID.
- Verdict (verbatim from §4.1).
- Operationalisation summary (one sentence, copied from the
  member's `interpretation.md` §1 / pre-reg §4 paraphrase).
- "What the verdict licenses" — one sentence, copied verbatim or
  near-verbatim from the member's `interpretation.md` §3 (the
  licensed-claim sentence Stage I produced). Stage S₁ does NOT
  re-derive the licensed claim; it copies what Stage I emitted.
- "What the verdict does NOT license" — one sentence, capturing
  the most salient cluster-relevant overclaim refusal from the
  member's `interpretation.md` §4 (typically the operationalisation-
  vs-construct distinction, or the PARTIAL-is-not-weak-SUPPORTED
  refusal).
- Effect-size summary — verbatim from the member's `interpretation.md`
  §3 (per guide #2 §4.3 binding rule: effect-size direction is
  part of every licensed-claim sentence).
- L-ID citations the member's interpretation made (the L-IDs the
  member's §4.5 listed — Stage S₁ uses this to compute the union
  for §4.5 below).
- For PARTIAL or INCONCLUSIVE verdicts: the closure-path statement
  from the member's `interpretation.md` §4.7 (what would upgrade
  the verdict, in one sentence).

This row format makes the cluster-level reading auditable: a reader
can verify the coherence call in §4.4 by walking the per-HA rows
in §4.3 and checking that the call respects what each member's
licensed-claim and effect-size + closure-path actually say. The §7
anti-pattern "narrative override" (the coherence call inconsistent
with the per-HA rows) is structurally prevented by the row-then-
call ordering.

**Worked example for C-stress-fatigue-shape** (the cluster's two
members per the map's r3 row):

| HA | Verdict | Licensed claim (from Stage I §3) | Effect-size | L-IDs cited (from Stage I §4.5) | Closure-path (§4.7) |
|---|---|---|---|---|---|
| HA-C3 v2 | REJECTED (wrong-direction override) | The Wiggers-verbatim 4-bin absolute-numerical operationalisation is REJECTED on Stratum 4 unmedicated; observed direction inverse of predicted. | Inverse-direction signal on Stratum 4 unmedicated primary cell (per result.md). | L1, L2, L3, L4, L6, L7 (L5 NA) | Closure via sister-HA Stage S₁ cross-operationalisation reading (this synthesis), or new sister with third bin scheme. |
| HA-C3p | PARTIAL (2-of-3 conditions MET) | The personal-baseline-quintile binning operationalisation is PARTIAL on Stratum 4 unmedicated; conditions (b)+(c) PASSED; (a) FAILED. | Curvature detected (PARTIAL on b+c machinery); inverted-U trajectory peaks at Q4 (a FAILED). | L1, L2, L3, L4, L6, L7 (L5 NA) | Closure of (a) via sister-HA on a third bin scheme, or larger n on the gated cell. |

The row format is the same shape for all clusters; the worked
example above is illustrative. **For clusters with cascade-arrow
language** (C-bout-substance reading C-bout-framework as caveat-
class precondition), the §4.3 row table contains ONLY C-bout-
substance's members (HA-C4c); the C-bout-framework verdict
propagates via the §4.5 caveats + the §5.5 cascade-handling rule
in the coherence-call mapping, NOT as a co-equal row in §4.3.

### 4.4 Section 4 — Coherence call

Exactly one of **four labels**, with rationale paragraph:

- **CONCORDANT** — all HAs in the cluster point the same direction
  on the shared construct, with effect-size magnitudes consistent
  across operationalisations.
- **PARTIALLY CONCORDANT** — HAs point same direction on the shared
  construct, but with substantive disagreement on effect-size
  magnitude or on a qualifier (e.g. one HA PARTIAL on a condition
  another HA's framing does not have).
- **CONFLICT** — HAs point opposite directions on the shared
  construct; both readings preserved with no auto-resolution.
- **ORTHOGONAL** — HAs address different aspects of the shared
  construct and do not speak to each other directly (single-member
  cluster trivial-ORTHOGONAL is permitted per §5.6 below).

**Mapping rules and worked examples are in §5 below.** §4.4 is the
output surface; §5 is the operational guidance for which label
fits.

The rationale paragraph (one paragraph, two-to-four sentences)
states which label applies and **why, drawn from the §4.3 per-HA
rows + the map's §3 operationalisation-overlap-note**. The rationale
does NOT introduce evidence not in §4.3; if a cluster-level reading
requires evidence beyond what the per-HA rows + the map row
surface, that evidence lives in §4.8 follow-up suggestions (own-
research track) as a candidate sister-HA, OR in §4.6 open conflicts
as an unresolved gap, NOT in the §4.4 rationale paragraph.

**Hard rule.** The §4.4 label is drawn from the four-label set
above. Stage S₁ does NOT invent new labels (e.g. "WEAKLY
CONCORDANT" or "MOSTLY CONFLICT" are forbidden); the four labels
are exhaustive for the cluster-coherence question Stage S₁
addresses. If no label fits cleanly, the cluster is CONFLICT (the
default-to-preserve discipline) or the cluster needs map revision
per §6.1 below.

### 4.5 Section 5 — Cluster-level caveats narrowing the joint claim (with L-ID citation block)

Three sub-blocks:

**5a. Cluster-level caveats from member interpretations.** The
union of caveat content from each member's `interpretation.md` §4.5
(both the 5a pre-reg + audit caveats sub-block and the 5b L-ID
citation sub-block of Stage I). These are **not new caveats invented
at Stage S₁ time**; they are the carry-forward from upstream.
Stage S₁ may **synthesise** the caveats (e.g. naming a caveat that
applies to two cluster members in one paragraph rather than two,
when the caveat's substance is the same) but does NOT add caveats
the member interpretations did not carry. If Stage S₁ identifies a
cluster-level caveat that no member interpretation carried, §7.4
anti-pattern routing applies (the caveat surfaces as an upstream
Stage I gap and triggers a re-examination of the relevant member's
interpretation per the §3.7 drift policy); it does not enter the
cluster synthesis through Stage S₁ prose.

**5b. Cluster-level L-ID citation block.** The binding output per
[`research_line_limitations.md`](research_line_limitations.md) §5
table row for `cluster-*.md`. **Every limitation that touches any
cluster member MUST be listed by L-ID with one-sentence project-
specific application at the CLUSTER level.** The L-ID-to-cluster
mapping is derived from:

- The synthesis-structure map's §3 cluster row "L-IDs S₁ will need
  to cite" column for the target cluster (the binding source).
- Plus the L2-era-strata-mismatch citation when the cluster spans
  different era strata (per the limitations-doc §5 binding's "also
  cite L2 if cluster members are from different era strata" clause).
  For C-bout-substance (which spans citalopram-phase sub-strata
  within Stratum 4 via HA-C4c's cross-phase pooling), this triggers
  the L2 cluster-level citation naming the cross-phase pooling as
  the era-strata-mismatch surface.
- Minus L-IDs that no cluster member's interpretation cited AND the
  map's §3 row lists as NA at the cluster level.

The citation format follows
[`research_line_limitations.md`](research_line_limitations.md) §5
worked examples — a one-line acknowledgment with the L-ID and one
sentence on how this limitation applies to *this cluster's specific
joint claim*. The §5 worked-example in the limitations doc itself
includes a cluster-level multi-cite template:

> *Cross-cutting multi-cite at the cluster level (e.g. a
> `cluster-*.md` synthesising HAs whose members touch crash days,
> era boundaries, and lived-experience priors):*
> Cites L1+L2+L4: this cluster's joint claim is single-subject
> (L1 inference reach per Daza 2018 bounds it); all member HAs run
> on Stratum 4 unmedicated only (L2 forbids cross-phase pooling
> without warrant; none added here); the cluster's coherence call
> relied on lived-experience-prior reconciliation of a discordant
> HA pair (L4 — recorded transparently per the synthesis guide
> §6.3).

Stage S₁ produces a similar block for each active cluster, drawing
from the map row's L-IDs and the cluster-level era-strata-mismatch
clause where it triggers.

**5c. Cascade-arrow precondition sub-paragraph.** For clusters
with cascade-arrow language in the map's §3 row (currently
C-bout-substance), this sub-paragraph cites the upstream cluster's
locked `cluster-*.md` verdict and states explicitly that it
propagates as caveat-class precondition into this cluster's joint
claim, NOT as co-equal verdict. The sub-paragraph reads (template):

> *Cascade-arrow precondition* (per the map's §3 row for
> `<cluster-id>`): the upstream `cluster-<upstream-id>.md` reached
> coherence call `<LABEL>` on its construct of `<framework /
> calibration / methodology>`. This propagates into the current
> cluster's joint claim as caveat-class precondition: the joint
> claim assumes the upstream framework / calibration is fit-for-
> purpose to the degree the upstream cluster's `<LABEL>` warrants,
> and inherits the upstream cluster's open conflicts as cluster-
> level caveats. Per §5.5 below, this is NOT a co-equal verdict
> reconciliation; the upstream verdict bounds what the current
> cluster's substantive verdict may claim, but the upstream verdict
> does not enter the coherence call as a third "vote" alongside
> the current cluster's members.

For clusters without cascade-arrow language (C-stress-fatigue-shape;
C-bout-framework as itself the upstream), this sub-paragraph is
omitted.

**Hard rule.** The §4.5 L-ID block (sub-block 5b) and the cascade-
arrow sub-paragraph (sub-block 5c, where applicable) are the
layer's commensurability guarantee at the cluster level. An
artefact missing either (when triggered by the map row) cannot be
locked.

### 4.6 Section 6 — Open conflicts preserved with both readings

When the §4.4 coherence call is CONFLICT (or PARTIALLY CONCORDANT
with substantive disagreement on a qualifier), this section
preserves the conflict. **No auto-resolution.** The section reads:

- One paragraph per HA whose reading conflicts with another
  cluster member's: naming the conflicting reading, the HA it
  conflicts with, the operationalisation basis of the conflict,
  and the L4 (analyst-is-subject) acknowledgment that the conflict
  is not silently resolved at Stage S₁.
- The conflict's resolution paths (NOT executed at Stage S₁):
  - A tie-breaker HA (typically a sister-HA on a third
    operationalisation that would distinguish between the
    conflicting readings); listed in §4.8 own-research follow-up.
  - A descriptive deep-dive on the cluster's primary cell that
    would expose which reading is artifactual; listed in §4.8
    own-research follow-up AND in §4.9 `open_inputs`.
  - Stage S₂ external-literature positioning (where literature
    consensus on the construct's mechanism would inform which
    reading converges with established findings — but per locked-
    plan §3.10 hard predictive gate, the convergence-with-
    consensus is hypothesis-generating-prior at most, not
    auto-resolution).
- The conflict stays open: the cluster's joint claim defaults to
  "the construct shows conflicting signal under different
  operationalisations" and the §4.4 coherence call records this
  as CONFLICT (or PARTIALLY CONCORDANT-with-conflict).

For CONCORDANT calls with no conflict: this section reads "No open
conflicts at the cluster level; all member HAs point the same
direction with consistent effect-size magnitudes per §4.3."

For ORTHOGONAL calls (typically single-member or independent-aspects
clusters): this section reads "Cluster members address different
aspects of the shared construct; no conflict at the cluster level
because the members do not speak to each other directly."

### 4.7 Section 7 — What the cluster jointly licenses + does NOT license

**Two sub-blocks:**

**7a. What the cluster jointly licenses.** The cluster-level
claim, drawn from the per-HA licensed claims in §4.3 and the
coherence call in §4.4. The joint claim is bounded by the **width
discipline**: it is no wider than the narrowest member's licensed
claim allows, **unless** the cross-operationalisation replication
pattern explicitly warrants the broader claim. For independent-
operationalisation clusters (like C-stress-fatigue-shape's two-bin-
scheme sister pair per the map's §3 evidence-strength rationale),
cross-operationalisation convergence MAY warrant a broader claim
at the construct level (e.g. "the construct shows non-monotonicity
across two independent bin-scheme operationalisations" is wider
than either HA's individual licensed claim — but narrower than
"the Wiggers convex-cost claim is wrong," which would require
group-level work per L1). For same-signal multi-take clusters
(three HAs on the same column under different gating choices),
the joint claim is bounded by the narrowest member's licensed
claim — width does not increase with member count when the members
are not independent.

**7b. What the cluster jointly does NOT license.** The mirror of
7a: claims the cluster does NOT warrant, especially the easy
overclaims. Stage S₁ MUST address explicitly:

1. **"The construct's mechanism is established."** Cluster-level
   coherence on a direction is not mechanism. A CONCORDANT call
   on direction is hypothesis-generating prior for mechanistic
   research, not a mechanism claim itself.
2. **"The construct's group-level reach is established."** Per L1
   (single-subject reach), cluster-level coherence in this N=1
   corpus is bounded by Daza 2018 / CENT / SCRIBE / Natesan 2023
   N-of-1-to-group reach. The cluster speaks about this subject;
   group-level positioning is Stage S₂'s job.
3. **"The construct is predictive."** Per locked-plan §3.10 hard
   predictive gate, predictive claims live at Stage A and require
   forward-validation HAs. Cluster-level coherence does NOT
   promote any tier.
4. **"The cluster's joint claim averages the conflict."** For
   CONFLICT or PARTIALLY CONCORDANT calls, the joint claim does
   NOT split the difference between conflicting readings to produce
   a "middle" claim. The conflict is preserved per §4.6; the joint
   claim names the conflict as the cluster's primary substantive
   finding rather than papering over it.

### 4.8 Section 8 — Follow-up suggestions (own + external tracks)

Per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.11, every reviewer-mode-with-authorization artefact closes with
a **Follow-up suggestions** section, separated into two tracks.
Stage S₁ is the per-stage shape per the locked-plan §3.11 "Stage
S₁" row:

- **Own-research track**: tie-breaker HAs for unresolved CONFLICT
  calls; independence-check HAs to verify multiple operationalisations
  are not running on the same underlying signal (especially relevant
  for same-signal multi-take clusters where the joint-claim width
  discipline depends on independence); replication HAs as new data
  accrues. Concrete pre-reg shapes, not vague directions. Examples
  per the three active clusters:
  - For C-stress-fatigue-shape (likely PARTIALLY CONCORDANT or
    CONFLICT call per §5 worked examples): a third sister-HA on a
    rolling-window-baseline binning OR a median-split-on-personal-
    distribution binning would tighten the cluster-level reading
    by adding a third independent operationalisation. If the third
    sister also fails monotonicity in the same inverted-U direction
    as HA-C3p, the cluster's joint claim strengthens; if it
    reverts to monotone, the cluster's CONFLICT call sharpens.
  - For C-bout-framework (single-member cluster, methodology-
    validation per the map's §3 row): a third framework-validity
    HA testing the bout-extraction operand on a different
    reference-date pool (e.g. extended-window vs HA11 v1's train-
    era pool) would isolate framework fitness from corpus-era
    fragility. This is the same pre-reg shape Stage I §4.8 named
    for HA11-bout-redo's own follow-up; Stage S₁ inherits and
    consolidates rather than duplicates.
  - For C-bout-substance (single-member cluster with cascade-arrow
    precondition to C-bout-framework): an unmedicated-only sister-
    HA running the same `bout_n_did_not_return_day` operand would
    isolate the cross-phase confound from the substantive bout-
    recovery signal — distinguishing the "cross-phase pooling
    diluting an unmedicated-only signal" reading from the "genuine
    smallness of heavy-T discrimination" reading per the seed-notes
    §3 caveat list.
- **External-research track**: what group-level or comparable-
  population study would test the same cluster-level construct
  where our N=1 setup cannot. Per the locked-plan §3.11 binding
  scoping discipline: **every external-research suggestion MUST
  explicitly name the N=1 limit that prevents us from answering
  the question ourselves**. Naming "someone should run an RCT"
  without "we cannot because we have one subject and no comparator
  arm" is the locked-plan §9 "unscoped-follow-up fallacy" and is
  forbidden. The scoping cites the relevant L-ID from §4.5
  (typically L1 single-subject reach for group-level cluster
  studies, L4 analyst-is-subject for blinding-required designs,
  L3 device-generations for cross-device-platform work).

Each entry is one paragraph with: the proposed study; the L-ID
that prevents us from running it ourselves; and what the study
would contribute to the cluster's joint claim.

**Distinct from `open_inputs`** (per locked-plan §3.5 vs §3.11).
The §4.9 `open_inputs` block is "what is missing to complete *this
current cluster synthesis*." The §4.8 follow-up suggestions are
"what *next claims* could be built — for us or for others." Both
are required; neither substitutes for the other.

### 4.9 Section 9 — `open_inputs` block

Per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.5, every reviewer-mode-with-authorization artefact produces,
alongside its main content, a structured `open_inputs` block that
names exactly:

1. **What is missing** — the descriptive deep-dive on a cluster-
   primary cell, the tie-breaker sister-HA, the lived-experience
   walk-through for a divergent cluster member's era, the literature
   reference. Use specific paths or proposed pre-reg slot names;
   do not say "more synthesis."
2. **What it is blocking** — typically Stage S₂ on the topic this
   cluster feeds (per the map's §4 topic row), sometimes a tighter
   §4.4 coherence call on this same cluster (PARTIALLY CONCORDANT
   → CONCORDANT, CONFLICT → CONCORDANT-after-tie-breaker), sometimes
   a Stage A construct artefact's tier-claim downstream (per the
   map's §5 construct row).
3. **Cheapest acquisition path** — which sister-HA pre-reg shape
   (per §4.8 own-research track), which descriptive run (per Stage
   D `open_inputs` carry-forward; if the cluster's `open_inputs`
   names a descriptive run that closes the cluster reading AND
   would also close a member HA's audit gap, the entry references
   the audit's existing entry rather than duplicating), which
   `/fetch-paper` call (per the `_pending_literature_fetch.md`
   pattern). Effort estimate (S ≤ 2h, M = 3-8h, L > 8h) per the
   stocktake §3 convention.
4. **Fallback claim available without it** — always at most one
   tier narrower than the claim being blocked, per locked-plan
   §3.5 hard rule on no-silent-degradation.

Three Stage-S₁-specific refusal-to-proceed paths produce
open_inputs entries (per plan §3.5 hard rule that every refusal-
to-proceed produces an `open_inputs` entry):

- **Member HA `interpretation.md` missing**: Stage S₁ refuses to
  start. The open_inputs entry names "Stage I `interpretation.md`
  for HA-XX" as the missing input, "Stage S₁ on cluster-`<id>`"
  as what it blocks, "run `/research-interpret interpret HA-XX`
  per [`verdict_to_inference.md`](verdict_to_inference.md) §9" as
  the acquisition path, "none — Stage S₁ cannot proceed without
  every member's interpretation in hand" as the fallback claim.
- **Cluster not in the synthesis-structure map**: Stage S₁ refuses
  to start. The open_inputs entry names "synthesis-structure map
  row for cluster-`<id>`" as the missing input, "Stage S₁ on the
  un-mapped cluster" as what it blocks, "producer-mode map-update
  session per the locked plan's §3.6 conflict-resolution rule"
  as the acquisition path, "none — Stage S₁ cannot proceed on
  a cluster the layer-wide map does not declare" as the fallback
  claim. This path is structurally identical to the §6.1 map-
  change-needed halt; both feed the same `open_inputs` entry
  shape because both represent map-vs-stage misalignment.
- **Cascade-arrow upstream cluster's `cluster-*.md` not yet
  locked**: Stage S₁ refuses to start (for cascade-downstream
  clusters only — currently C-bout-substance, which reads C-bout-
  framework as upstream). The open_inputs entry names "upstream
  `cluster-<upstream-id>.md`" as the missing input, "Stage S₁ on
  the cascade-downstream cluster `<id>`" as what it blocks, "Stage
  S₁ on the upstream cluster first" as the acquisition path,
  "none — the cascade-arrow precondition is a hard upstream gate"
  as the fallback claim.

The skill (per §9 below) aggregates §4.9 entries across all per-
cluster syntheses into the layer-wide
`docs/research/methodology/_open_inputs.md` queue. The per-cluster
entries are the source rows; the queue is the aggregate.

**Open inputs do not block completion** per locked-plan §3.8: a
cluster synthesis can be COMPLETE *and* carry open_inputs entries.
Completion means "this is the best cluster reading with the inputs
we currently have, and we have logged what would improve it." The
exception is the three refusal-to-proceed paths above, where the
open_inputs entry IS the artefact (the synthesis itself is not
drafted — only the entry).

### 4.10 Section 10 — Cross-references

Links out to:

- Each member HA's `interpretation.md` (the inputs the cluster
  synthesis was built on).
- The synthesis-structure map's §3 cluster row (the structural
  pre-registration row reference, not a paraphrase).
- The synthesis-structure map's §4 topic row the cluster feeds
  (forward pointer for Stage S₂).
- The synthesis-structure map's §5 construct row the cluster
  participates in (forward pointer for Stage A; Stage S₁ does NOT
  cross the §3.10 hard predictive gate, only points forward).
- For cascade-downstream clusters: the upstream cluster's
  `cluster-*.md` (verbatim citation of the upstream coherence
  call as caveat-class precondition).
- Limitations doc cross-refs for cited L-IDs (per §4.5).
- The non-binding seed notes
  [`_synthesis_seed_notes_2026-06-23.md`](_synthesis_seed_notes_2026-06-23.md)
  — cite only if the synthesis explicitly drew on (or explicitly
  rejected) one of the seed sketches as caveat-class context. If
  the synthesis ignored the seed notes entirely, the cross-
  reference may be omitted; the §4.5 caveats sub-block records
  no inheritance from them either way.
- Literature methodology anchors cited in §4.4 / §4.5 / §4.8 for
  inference-reach bounds (especially Daza 2018 for the multi-test
  synthesis discipline; CENT items 21+22 for cluster-level
  limitations and generalisability statements; SCRIBE for L4
  participant-as-researcher transparency at the cluster level;
  Natesan 2023 for the bar on cluster-level coherence-call
  defensibility).
- CONVENTIONS §3.4 crash-drop sensitivity (where applicable to
  the cluster's reading; see §5.7 below for the cluster-level
  crash-drop discipline operationalisation).
- The locked plan §3.6 (conflict-resolution rule); §3.5 (missing-
  inputs flagging); §3.7 (drift policy); §3.8 (completion
  criteria); §3.9 (limitations binding); §3.10 (hard predictive
  gate forward pointer); §3.11 (follow-up suggestions); §3.12
  (commentary boundary — Stage S₁ does not carry); §4 (producer/
  reviewer split table); §6.3 (the spec brief this guide
  implements).

## 5. The coherence-call mapping rules

This section pins the per-label rules with worked examples from
the three active clusters in the synthesis-structure map's r3
(C-stress-fatigue-shape, C-bout-framework, C-bout-substance).

### 5.1 CONCORDANT

**Mapping rule.** All HAs in the cluster point the same direction
on the shared construct, with effect-size magnitudes consistent
across operationalisations. "Same direction" is defined at the
licensed-claim level (each member's Stage I §3 sentence agrees on
direction); "consistent magnitude" is defined at the effect-size
level (the member effect sizes overlap within a factor reasonable
for cross-operationalisation variation, typically a factor of 2-3
at the same construct level).

**The CONCORDANT call is bounded by:**

- The map's §3 cluster row's operationalisation-overlap-note. For
  independent-operationalisation clusters (the higher-evidence
  case), CONCORDANT licenses a cluster-level joint claim broader
  than any single member's licensed claim (cross-operationalisation
  convergence is positive multi-test evidence per Daza 2018). For
  same-signal multi-take clusters (the lower-evidence case),
  CONCORDANT licenses only a tightened single-claim — the multi-
  take agreement does NOT broaden because the members are not
  independent observations.
- The upstream Stage D verdict-trust status chain (all members
  TRUSTED unblocks CONCORDANT; a PROVISIONAL member narrows the
  joint claim by one tier per the locked-plan §3.5 no-silent-
  degradation hard rule).
- The cascade-arrow precondition where applicable (for cascade-
  downstream clusters, CONCORDANT on substance requires the
  upstream cluster's coherence call to license the framework /
  calibration as fit-for-purpose; if the upstream is CONFLICT or
  PARTIALLY CONCORDANT, the downstream's CONCORDANT call carries
  the upstream-instability caveat).

**What CONCORDANT does NOT license.** Mechanism (cluster-level
direction agreement is hypothesis-generating prior, not mechanism;
§4.7b first overclaim refusal). Group-level reach (per L1; §4.7b
second). Predictive tier (per §3.10; §4.7b third). Cross-cluster
construct claims (those are Stage S₂ or beyond).

**No worked example among the three active clusters in the map's
r3.** None of the three reaches CONCORDANT cleanly. The mapping
rule applies when future clusters land with all-same-direction
verdicts.

### 5.2 PARTIALLY CONCORDANT

**Mapping rule.** HAs in the cluster point the same direction on
the shared construct, but with substantive disagreement on effect-
size magnitude OR on a qualifier (e.g. one HA PARTIAL on a
condition another HA's framing does not have; one HA's effect
size larger by a factor inconsistent with cross-operationalisation
variation reasonable bounds).

**The PARTIALLY CONCORDANT call is bounded by:**

- The same operationalisation-overlap and verdict-trust constraints
  as CONCORDANT, but with the disagreement preserved in the joint
  claim per §4.7a width discipline ("the construct shows
  `<direction>` under both operationalisations, with substantive
  disagreement on `<magnitude / qualifier>`").
- The §4.6 open-conflicts section names the disagreement explicitly,
  even though the call is "partially" (not full) CONFLICT.

**Worked example — likely C-stress-fatigue-shape call.** The
cluster's two members (per the map's §3 row) are HA-C3 v2
(REJECTED, wrong-direction-override) and HA-C3p (PARTIAL, 2-of-3
conditions MET). Per [HA-C3 v2 result.md](../analyses/hypotheses/HA-C3/result.md)
§5 cross-test reading row and [HA-C3p result.md](../analyses/hypotheses/HA-C3p/result.md)
§6 4-cell agreement matrix, both HAs detect the **same inverse-
direction non-linearity finding** — the stress-fatigue mapping is
**concave / inverted-U** peaking around stress 30-40, not Wiggers-
monotone-convex. The verdict-bands differ only because of how each
spec handles the wrong-direction-override condition: HA-C3 v2 v2-spec
carries the override (any wrong-direction firing → REJECTED), while
HA-C3p's spec lets the (b)+(c) PASSED conditions stand alongside the
(a) FAILED Jonckheere-Terpstra without the override fire (yielding
PARTIAL 2-of-3 MET).

> *Likely PARTIALLY CONCORDANT reading*: both HAs agree on
> direction (inverse non-linearity, concave / inverted-U shape
> peaking around stress 30-40, NOT Wiggers-monotone-convex) and
> agree on the underlying shape detection (HA-C3 v2's wrong-
> direction override is the v2-spec mechanism for flagging the
> inverted-U; HA-C3p's (b) PASS + (c) PASS is the direct curvature-
> machinery detection of the same shape). The verdict-band
> disagreement (REJECTED vs PARTIAL) is **spec-mechanism, not
> shape-substance**: HA-C3 v2's spec routes inverse-direction
> firings to REJECTED; HA-C3p's spec does not. The §4.7a width
> discipline applies: "the construct's stress-fatigue mapping is
> concave / inverted-U under both Wiggers-verbatim and personal-
> baseline-anchored bin schemes, with verdict-band disagreement
> driven by spec-mechanism handling of wrong-direction firings,
> not by shape disagreement." The §4.6 open-conflicts section
> notes the verdict-band asymmetry as a spec-discipline
> observation — not as an unresolved substantive conflict.

**Worked example alternative — possible C-stress-fatigue-shape
CONCORDANT reading.** A synthesist could legitimately read this as
CONCORDANT (not PARTIALLY CONCORDANT) on the grounds that the
verdict-band asymmetry is purely spec-mechanism and the shape-
substance is uniformly inverted-U across both HAs. **The choice
between CONCORDANT and PARTIALLY CONCORDANT for this cluster is a
judgment call the user makes during the §8 interview**; the
PARTIALLY-CONCORDANT default-to-preserve reading honours the
verdict-band asymmetry as worth recording even when the underlying
shape agreement is strong. CONFLICT is NOT a defensible reading for
this cluster on current evidence — both HAs detect the same shape;
no opposite-direction-on-the-construct disagreement exists at the
licensed-claim level.

### 5.3 CONFLICT

**Mapping rule.** HAs in the cluster point opposite directions on
the shared construct; both readings preserved with no auto-
resolution. "Opposite directions" is defined at the licensed-claim
level (each member's Stage I §3 sentence asserts a direction that
the other member's §3 sentence contradicts).

**The CONFLICT call is bounded by:**

- **Both readings preserved.** The cluster's joint claim defaults
  to "the construct shows conflicting signal under different
  operationalisations" and the §4.6 open-conflicts section names
  both readings with their operationalisation grounding.
- **No auto-resolution.** Stage S₁ does NOT pick a winning side;
  does NOT downgrade one HA to fit the other; does NOT split the
  difference. The §4.7b fourth overclaim refusal ("the cluster's
  joint claim averages the conflict") is explicitly prevented at
  this label.
- **Resolution paths in §4.6 + §4.8.** Tie-breaker sister-HAs
  (own-research follow-up); descriptive deep-dives on the
  cluster's primary cell (open_inputs); Stage S₂ external-
  literature positioning (forward pointer, not resolution in
  this stage).

**Worked example — none in the current corpus**: per the §5.2
worked-example correction, neither C-stress-fatigue-shape (where
both HAs detect the same inverted-U shape; verdict-band asymmetry
is spec-mechanism only) nor C-bout-framework (single-member) nor
C-bout-substance (single-member with C-bout-framework as caveat-
class precondition, not opposite-direction co-equal) presents a
clean CONFLICT reading on current evidence. CONFLICT is a real
mapping rule the layer supports — it would apply to a future
cluster where two HAs on the same construct produce opposite-
direction licensed claims at the §3 sentence level — but no
current cluster realises this case. When a future cluster does,
the §6.3 verdict vs cluster-level-expectation conflict rule below
governs (default to CONFLICT on ambiguity per §4.4 hard rule;
no auto-resolution; tie-breaker sister-HA + descriptive deep-dive
named in §4.6 + §4.8 + §4.9).

### 5.4 ORTHOGONAL

**Mapping rule.** HAs in the cluster address different aspects of
the shared construct and do not speak to each other directly. The
construct is shared at the map's §3 row level, but the
operationalisations address distinct facets that don't license a
cross-HA reading.

**The ORTHOGONAL call is bounded by:**

- **Different-aspects-of-construct, NOT different-constructs.** If
  the HAs address different constructs entirely, the map row is
  wrong and the §6.1 map-change-needed halt applies; ORTHOGONAL
  is for HAs that share a construct but address distinct facets
  the joint claim cannot synthesise across.
- **No joint claim beyond per-HA claims.** The cluster's joint
  claim is the union of per-HA licensed claims; there is no
  cross-HA inference. §4.7a width discipline reads "joint claim is
  the union of per-HA licensed claims, no cross-aspect inference."

**Trivial-ORTHOGONAL for single-member clusters.** Per §5.6 below,
a single-member cluster's coherence call defaults to ORTHOGONAL
(trivial), with the cluster's joint claim collapsing to the
single member's Stage I §3 licensed claim. This is the structurally-
trivial case the locked plan §3 dependency rule permits skipping
(via `stage_skipped.md` stub) OR thin-S₁-ing per §3 above.

### 5.5 Cascade-arrow handling

This is the rule that distinguishes the C-bout-framework →
C-bout-substance cascade per the map's §3 r3 row from any co-
equal-verdict reconciliation. **The cascade-upstream cluster's
verdict propagates into the cascade-downstream cluster's coherence
call as caveat-class precondition, NOT as a co-equal verdict.**

**Operational rule for cascade-downstream clusters' coherence
call.** Stage S₁ on the cascade-downstream cluster reads ONLY the
downstream cluster's member HAs to compute the §4.4 coherence
call. The upstream cluster's verdict does NOT enter §4.4 as a
"third vote" or as a member of the cluster. The upstream verdict
enters §4.5 (cluster-level caveats) and §5 (this section's
cascade-handling rule) as a precondition that bounds what the
downstream coherence call may claim about the construct:

- If the upstream cluster reached **CONCORDANT** (the framework /
  calibration is fit-for-purpose with consistent multi-test
  evidence), the downstream coherence call MAY claim its substantive
  reading at full strength, subject only to its own member HAs'
  effect-size and verdict-trust constraints.
- If the upstream cluster reached **PARTIALLY CONCORDANT** or
  **CONFLICT** (the framework / calibration is partially fit-for-
  purpose, or under genuine conflict), the downstream coherence
  call MUST narrow its substantive claim accordingly: the §4.7a
  joint claim carries an explicit "subject to the upstream
  cluster's <PARTIALLY CONCORDANT / CONFLICT> caveat on framework
  fitness" qualifier. The downstream call does NOT auto-downgrade
  to PARTIALLY CONCORDANT or CONFLICT itself — the downstream
  members' agreement on direction is independent of the upstream
  framework's fitness call. But the joint claim's strength is
  bounded by the upstream's caveat.
- If the upstream cluster reached **ORTHOGONAL** (trivial single-
  member or distinct-aspects-of-construct), the downstream's
  cascade-precondition reads the upstream member's licensed claim
  directly rather than a cluster-level coherence call; the
  precondition status is "the upstream framework's fitness is
  bounded by HA-`<upstream-id>`'s Stage I §3 licensed claim with
  effect-size <e> and verdict-trust <status>".

**Worked example — C-bout-substance reading C-bout-framework as
caveat-class precondition.** Per the map's §3 r3 row, C-bout-
framework consists of HA11-bout-redo (PARTIAL, 2-of-3 framework-
validity bars met; bars 1+2 PASSED on direction + effect-size
reproduction at +20.26 pp, bar 3 FAILED on block-permutation p =
0.2609 per the seed notes §3). C-bout-framework's own Stage S₁
coherence call is **trivial-ORTHOGONAL** (single-member cluster
per §5.6 below) with joint claim collapsing to HA11-bout-redo's
licensed claim: "the bout-extraction operand `bout_n_fast_recovery_
day` met 2 of 3 framework-validity bars at HA11 v1's calm-day
reference-date pool, under the locked operationalisation; this is
operand fitness-for-purpose, NOT a substantive within-day recovery
claim."

C-bout-substance's Stage S₁ reads this upstream as caveat-class
precondition. The §4.5 cascade-precondition sub-paragraph reads
(template):

> *Cascade-arrow precondition* (per the map's §3 row for
> C-bout-substance): `cluster-bout-framework.md` reached trivial-
> ORTHOGONAL coherence call (single-member cluster), with HA11-
> bout-redo's licensed claim of 2-of-3 framework-validity bars
> met — bars 1+2 PASSED, bar 3 FAILED. This propagates into the
> current cluster's joint claim as caveat-class precondition: the
> bout-extraction operand's framework fitness is partially
> established (bars 1+2 PASSED indicate direction + effect-size
> reproduction at +20.26 pp; bar 3 FAILED leaves the block-
> permutation discrimination at corpus detection limits per the
> seed notes §3 caveat). The current cluster's substantive
> coherence call on heavy-T vs non-heavy-T differentiation
> inherits the 2-of-3 framework caveat: the substantive claim
> carries the "operand fitness partially established" qualifier
> explicitly. Per §5.5 above, this is NOT a co-equal verdict
> reconciliation; the upstream verdict does not enter §4.4.

C-bout-substance's own §4.4 coherence call (its sole member is
HA-C4c, PARTIAL with bar (a) PASSED p=0.0001 + bar (b) FAILED
Cliff's δ=+0.120 below the +0.20 threshold) is itself **trivial-
ORTHOGONAL** per §5.6 below, with joint claim collapsing to
HA-C4c's licensed claim PLUS the cascade-precondition qualifier
from C-bout-framework.

**Hard rule.** A cascade-downstream cluster's S₁ MUST NOT enter
§4.4 with the upstream verdict as a member. The upstream verdict
is precondition (§4.5 + §5.5 cascade-handling), not co-equal
member. Treating it as co-equal would conflate framework-validity
(methodology-validation) with substantive (within-day recovery)
verdicts — exactly the conflation the map's r1 → r2 split (per
the map's §7 lock-log entry 2026-06-23) was designed to prevent.

### 5.6 Trivial coherence calls for single-member clusters

A single-member cluster's coherence call defaults to **trivial-
ORTHOGONAL** with the cluster's joint claim collapsing to the
single member's Stage I §3 licensed claim. The §4.4 paragraph
reads (template):

> *Trivial ORTHOGONAL coherence call* (single-member cluster per
> the synthesis-structure map's §3 row): the cluster contains a
> single constituent HA, so there is no cross-HA coherence to
> assess. The joint claim collapses to HA-`<id>`'s Stage I §3
> licensed claim: `<verbatim copy>`. The cluster-level reading
> adds the §4.5 L-ID citation block at the cluster level (per
> the limitations-doc §5 binding's cluster-level citation rule)
> and the cascade-arrow precondition handling per §5.5 where
> applicable, but does NOT add cross-HA coherence the single-
> member structure cannot support.

**Worked examples (per the map's r3).** C-bout-framework
(HA11-bout-redo) and C-bout-substance (HA-C4c) are both single-
member clusters in r3. Both default to trivial-ORTHOGONAL with
joint claim collapsing to the single member's Stage I §3
licensed claim. C-bout-substance additionally carries the
cascade-precondition handling per §5.5 above; C-bout-framework
does not (no upstream cluster).

**Per locked plan §3 dependency rule.** A single-member cluster's
S₁ may be SKIPPED with an explicit `stage_skipped.md` stub
recording the structural-triviality justification, OR THIN-S₁-d
producing the trivial-ORTHOGONAL synthesis above. The choice is
the user's at the moment the cluster becomes eligible; the §11
lock log records which path was taken and why. The thin-S₁
option is preferred when the cluster carries cascade-arrow
language (because the cascade-precondition handling needs an
artefact to live in); the skip-with-stub option is permitted
when the cluster does not carry cascade-arrow language and the
downstream Stage S₂ topic can cite the member HA's `interpretation.md`
directly without going through a cluster wrapper.

### 5.7 Cluster-level crash-drop sensitivity discipline

Per CONVENTIONS §3.4 (crash-drop sensitivity row on every Layer
4+ correlation): when cluster member HAs report verdicts that
diverge on the crash-included vs crash-dropped frame (or when
one member ran the crash-drop sensitivity and another did not),
the cluster-level reading MUST surface the divergence rather than
average it away.

**Operational rule.** If any member HA's `result.md` (per
guide #1 Stage D audit chain) reports a crash-drop sensitivity row
with |Δ| > 0.10 between the full LC frame and the crash-dropped
frame, Stage S₁ inherits the crash-drop divergence as a cluster-
level caveat-class observation:

- Cited in §4.5 (5a sub-block, cluster-level caveats) naming the
  member HA whose crash-drop sensitivity surfaced the divergence
  and the magnitude of the divergence.
- Cited in §4.6 (open conflicts) if the divergence changes which
  side of CONCORDANT-vs-CONFLICT the cluster lands on (e.g. the
  cluster reads CONCORDANT on the full LC frame but CONFLICT on
  the crash-dropped frame — the cluster-level call inherits the
  divergence as an open conflict per the §3.4 "the contrast itself
  is informative" rule).
- NOT averaged away into a "middle" cluster claim.

**Worked example for C-bout-substance.** HA-C4c's primary cell is
heavy-T vs non-heavy-T differentiation at bout resolution. If
HA-C4c's result.md includes a crash-drop sensitivity row showing
|Δ| > 0.10 in the Cliff's δ between crash-included and crash-
dropped frames, the cluster-level reading surfaces this in §4.5
naming the crash-day load on the substantive verdict, AND in
§4.6 if it changes the cluster's coherence-call direction.

This rule operationalises CONVENTIONS §3.4 at the cluster level;
it does NOT introduce a new crash-drop discipline beyond what the
convention already binds. The cluster-level surfacing is the
layer-level manifestation of the per-HA convention.

## 6. Conflict rules

The synthesis MUST apply the following conflict rules when
upstream-status and cluster-internal-evidence interact:

### 6.1 Map-change-needed (§3.6 conflict-resolution rule)

> Halt the S₁ session immediately. Do NOT edit the map in-session.
> Route the proposed change to a separate producer-mode map-
> revision session with its own `/research-methodology-review`
> pass before re-lock.

This is the **single most important discipline rule of Stage S₁**.
Per locked-plan §3.6 conflict-resolution rule (map vs §6.3 per-
cluster pre-declaration): when per-cluster S₁ work reveals that
the §3.6 layer-wide map needs to change (an HA belongs in a
different cluster, a new cluster should exist, a topic boundary
is wrong, an operationalisation-overlap-note is inadequate), Stage
S₁ HALTS and routes to a separate map-revision session.

**Concrete halt-criteria.** Stage S₁ halts and routes to map
revision when any of the following surfaces during the cluster
synthesis:

1. **A cluster member's interpretation makes a substantive
   licensed claim that places the HA on a different construct**
   than the map's §3 row's "shared construct" cell declares. The
   §3 row's shared-construct declaration is binding for the
   cluster's membership; if Stage I's licensed claim drifts to a
   different construct, the cluster-vs-HA relationship is misaligned.
2. **The cluster's coherence call would require evidence from an
   HA not in the map's §3 row** to make sense. If Stage S₁ finds
   that a sister-HA in a different cluster (or no cluster) carries
   evidence the current cluster's coherence call cannot work
   without, the constellation is wrong — either the sister-HA
   should be in this cluster (map-update path) or the cluster's
   constellation needs to add a member (also map-update path).
3. **The operationalisation-overlap-note cell is inadequate.** If
   Stage S₁ finds that the map's §3 row's overlap-note cell
   misrepresents the cluster's evidence-strength rationale (e.g.
   the cell claims "two independent operationalisations" but
   Stage S₁'s reading reveals they share more structure than the
   cell acknowledges, or vice versa), the cell needs revision —
   the cluster cannot land its coherence call on an inaccurate
   evidence-strength rationale.
4. **The cascade-arrow language is wrong.** If Stage S₁ finds
   that the map's §3 row's cascade-arrow language misrepresents
   the upstream-downstream relationship (e.g. the cell declares
   caveat-class precondition but Stage S₁'s reading reveals the
   upstream should be co-equal, or vice versa), the cell needs
   revision.

**Route-out instructions.** When Stage S₁ halts per any of the
above criteria:

1. **Stop drafting the cluster-XXX.md artefact mid-session.** Do
   NOT save a partial synthesis to the analyses/synthesis/ folder;
   do NOT edit the map in-session.
2. **Produce only the §4.9 `open_inputs` entry** naming the
   proposed map change. The entry follows the standard four-field
   shape: what is missing (specific map-row change proposed); what
   it blocks (Stage S₁ on the affected cluster, plus any downstream
   stages dependent on this cluster); cheapest acquisition path
   (a separate producer-mode map-revision session per the locked
   plan §3.6); fallback claim available (none — Stage S₁ cannot
   proceed silently on a misaligned cluster).
3. **Hand off to the user.** Surface the halt with the specific
   halt-criterion that triggered (one of the four above) and the
   proposed map change. The user decides whether to authorize the
   map-revision session immediately, defer it, or revise the per-
   cluster sign-off question (if the user disagrees that the
   misalignment surfaces a map issue).
4. **Resume Stage S₁ only after a separate producer-mode session
   updates the map (with its own
   `/research-methodology-review` pass before re-lock).** The
   resumption is its own §11 step session; the halted Stage S₁
   session does NOT auto-resume.

**Why this rule.** Without it, the same session that discovers a
clustering problem during S₁ would be tempted to fix it in flight,
collapsing the layer-wide map's pre-registration discipline back
into the per-cluster ad-hoc decisions §3.6 exists to prevent. The
halt-and-route discipline is what makes the map authoritative; the
map-revision-in-separate-session discipline is what keeps the
re-clustering decision from being coupled to the very synthesis
results that would be drafted from it.

### 6.2 Cascade-arrow upstream not yet locked

> Refuse to start the cascade-downstream cluster's S₁ until the
> upstream cluster's `cluster-*.md` is locked.

For cascade-downstream clusters (currently C-bout-substance, which
reads C-bout-framework as caveat-class precondition per the map's
§3 r3 row), Stage S₁ refuses to start if the upstream cluster's
`cluster-*.md` is missing or unlocked. The §4.9 `open_inputs`
entry per refusal-path-3 above carries the open-input shape.

The refusal is structural: the §5.5 cascade-handling rule requires
a locked upstream coherence call as the precondition input. A
draft upstream `cluster-*.md` cannot serve as cascade-precondition
because the upstream coherence call may shift during the upstream's
own lock cycle; coupling the downstream to a moving upstream would
defeat the cascade-arrow discipline.

### 6.3 Member-HA interpretation status mismatch with cluster-trust

> If any member's Stage D verdict-trust call is DOWNGRADED-
> INCONCLUSIVE-PROVISIONAL, narrow the cluster's coherence-call
> licensed claim by at most one tier per locked-plan §3.5 hard
> rule; record the PROVISIONAL chain in the §4.4 rationale
> paragraph + §11 lock log.

Per guide #2 §6.2 (verdict vs Stage D audit PROVISIONAL flag):
Stage I MAY proceed under explicit user acceptance of the
PROVISIONAL flag carrying forward as a narrowing flag on the
interpretation. The cluster-level inheritance is the same: a
cluster with any PROVISIONAL member carries the PROVISIONAL flag
forward into the §4.7a joint claim, narrowing by at most one tier.

For multi-PROVISIONAL clusters (rare: two-or-more members both
PROVISIONAL), the narrowing tier-count is capped at one — i.e.,
the cluster does NOT narrow by two-tiers-because-two-members-are-
PROVISIONAL. The narrowing discipline is structural (PROVISIONAL
presence → one-tier narrower joint claim), not compounding.
Compounding the narrowing would create perverse incentive to push
a member's audit to REQUIRES-DESCRIPTIVE-WORK rather than
PROVISIONAL to avoid the multi-PROVISIONAL inflation.

### 6.4 Cluster vs lived-experience prior reconciliation

Stage S₁ does NOT carry a §4.6-equivalent lived-experience prior
reconciliation. Per guide #2 §4.6, the lived-experience prior
reconciliation lives at the per-HA Stage I level, where each
member's interpretation records the prior vs verdict at the HA
level. Stage S₁ inherits the reconciliations as caveats (per §4.5
5a sub-block) but does NOT re-litigate them at the cluster level.

If a cluster's coherence call surfaces a tension with the user's
lived-experience prior that is genuinely at the cluster level (not
inheritable from any individual member's Stage I §4.6), the
tension lives in §4.6 (open conflicts) as a cluster-level open
conflict, with the §4.8 own-research follow-up naming a sister-HA
shape that would resolve the cluster-level tension. The cluster-
level prior tension is NOT §3.12 subject-narrative commentary
(which is forbidden at Stage S₁ per §1 above); it is the same
structured prior-vs-verdict reconciliation discipline guide #2
§4.6 carries, applied at the cluster level rather than the per-HA
level.

## 7. Anti-patterns explicitly forbidden

The following moves are forbidden in any Stage S₁ synthesis:

### 7.1 Re-routing HAs to different clusters in-stage

The §3.6 layer-wide map is authoritative for cluster membership.
Stage S₁ does NOT propose constituent additions or removals during
the synthesis; that is map-revision-session territory. If in-stage
work reveals a re-clustering need, the §6.1 halt-and-route rule
applies. Editing the map in-session (or silently treating an HA
as if it were in a different cluster than the map declares) is
forbidden.

### 7.2 Collapsing CONFLICT to a "middle" reading

The CONFLICT label is the layer's no-auto-resolution discipline.
Stage S₁ does NOT split the difference between conflicting
readings to produce a "middle" claim neither HA supports. The
§4.7b fourth overclaim refusal ("the cluster's joint claim
averages the conflict") is explicitly the surface where this
anti-pattern would otherwise hide.

The locked plan §9 layer-level anti-pattern list includes the
"synthesis-as-counting fallacy" (treating "3 of 5 HAs supported"
as stronger than "1 of 5 well-operationalised HAs supported with
descriptive backstopping"); the CONFLICT-collapsing anti-pattern
is the same fallacy applied at the cluster level. Counting does
not produce coherence; preservation produces coherence.

### 7.3 Treating cascade-arrow caveat-class precondition as co-equal verdict

Per §5.5 above: the cascade-upstream cluster's verdict is
precondition (§4.5 + §5.5), NOT a co-equal member of the
downstream cluster's §4.4 coherence call. Treating it as co-equal
would conflate framework-validity (methodology-validation) with
substantive verdicts — exactly the conflation the map's r1 → r2
split was designed to prevent (per the map's §7 lock log).

### 7.4 Smuggling sister-cluster context into the current cluster's reading

Stage S₁ operates on one cluster per session. Cross-cluster
context — even when the user has a candidate cross-cluster
reading (per the seed notes §4 cross-cluster cross-reference,
which is explicitly out of scope for S₁) — does NOT enter the
current cluster's §4.4 coherence call, §4.7a joint claim, or §4.5
caveats.

Cross-cluster reading belongs to Stage S₂ (external-literature
contextualisation across constructs that span multiple clusters)
or beyond. Importing it at S₁ collapses the cluster-bounded scope
that keeps coherence calls commensurate across clusters.

### 7.5 Promoting one cluster's reading using another cluster's evidence

Variant of §7.4. Stage S₁ does NOT use evidence from another
cluster's `cluster-*.md` to strengthen or weaken the current
cluster's coherence call. The cluster's §4.4 call is bounded by
the per-HA rows in §4.3 PLUS the cascade-arrow precondition where
applicable (per §5.5); no other cluster's evidence enters.

The seed notes §4 cross-cluster speculation (the bimodal-arousal-
mechanism reading linking C-stress-fatigue-shape's inverted-U to
C-bout-substance's modest effect size) is the canonical example
of what this anti-pattern is. The seed notes themselves flag this
as out of scope for S₁; Stage S₁ refuses to import the speculation
even if a user articulates it during the §8 interview.

### 7.6 Treating seed-notes sketches as constraints on the coherence call

The non-binding seed notes at
[`_synthesis_seed_notes_2026-06-23.md`](_synthesis_seed_notes_2026-06-23.md)
are advisory only per the file's own status header AND per the
synthesis-structure map's §3 note relocating them out of the map's
structural pre-registration. Stage S₁ MAY use the sketches as
caveat-class context OR ignore them entirely.

Treating a seed-notes sketch as a constraint on the §4.4 coherence
call — e.g., reading "the r1 drafter sketched PARTIALLY CONCORDANT
for C-stress-fatigue-shape, so the coherence call must be PARTIALLY
CONCORDANT" — is forbidden. The sketch is a colleague's notes-on-
the-data per the seed notes §5 self-description; not a structural
pre-decision the synthesis is bound to.

If the synthesis lands a coherence call that contradicts the seed-
notes sketch, the contradiction is itself useful (per the seed
notes §5 self-description) and should be logged in the §4.9
`open_inputs` block as descriptive context.

### 7.7 Inventing new caveats post-hoc

Caveats in §4.5 come from the union of cluster-member
`interpretation.md` §4.5 content (both 5a pre-reg+audit caveats
and 5b L-ID citations) + the synthesis-structure map's §3 cluster
row's L-IDs column + the L2-era-strata-mismatch cluster-level
binding where it triggers. New caveats invented at Stage S₁ time
— caveats that appear neither in any member interpretation nor in
the map row — are forbidden.

If Stage S₁ identifies a caveat the member interpretations and
the map row missed, the
[`verdict_to_inference.md`](verdict_to_inference.md) §7.5 anti-
pattern routing applies at the upstream level (the caveat surfaces
as a Stage I gap and triggers a re-examination of the relevant
member's interpretation per the §3.7 drift policy); it does not
enter the cluster synthesis through Stage S₁ prose.

### 7.8 Producing §3.12 subject-narrative commentary at Stage S₁

Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.12 hard separations: commentary lives at Stage A `construct-*.md`
(attached to tier-1 or tier-2 formal claim) and Stage T patient-
audience translation track only. Stage S₁ MUST NOT carry §3.12
commentary. Wording that reads as subject-narrative — "I notice
that...", "in my experience..." — does not belong in §4.4 / §4.5
/ §4.6 / §4.7. The §4.6 open-conflicts section inherits prior-vs-
verdict reconciliation from member interpretations' §4.6 sections;
it does NOT add cluster-level subject-narrative.

The "bare-narrative-as-actionability fallacy" (locked-plan §9) is
the layer-level form of this anti-pattern; Stage S₁'s prohibition
is the per-stage form, parallel to guide #2 §7.7's per-stage
prohibition at Stage I.

### 7.9 Computing or citing predictive-quality measures

Per locked-plan §3.10: PPV, base rate, sensitivity, specificity,
false-alarm rate, lead time, reliability — these are Stage A's
output, required at tier-2+. Stage S₁ does NOT compute, cite, or
forward-project any of these. The §4.7a joint claim reports
cluster-level direction and effect-size envelope (per CONVENTIONS
§2.1 descriptive-before-inference), not diagnostic-quality
measures. The forward pointer is Stage A; Stage S₁ cites the
synthesis-structure map's §5 K-construct row to confirm which
tier the construct may reach if all required evidence lands, but
Stage S₁ does not produce the tier's quality measures itself.

### 7.10 Inventing new coherence-call labels

The §4.4 label is drawn from the four-label set (CONCORDANT /
PARTIALLY CONCORDANT / CONFLICT / ORTHOGONAL). Stage S₁ does NOT
invent new labels. If no label fits cleanly, the cluster is
CONFLICT (the default-to-preserve discipline) or the cluster
needs map revision per §6.1. Labels like "WEAKLY CONCORDANT",
"MOSTLY CONFLICT", "INCONCLUSIVE-AT-CLUSTER-LEVEL" are forbidden;
the four labels are exhaustive for the question Stage S₁
addresses.

### 7.11 Auto-resolving open conflicts in subsequent re-examinations

Per locked plan §3.7 drift policy: a `cluster-*.md` is re-examined
when a constituent interpretation is re-examined or downgraded, OR
when a new HA joins the cluster (per map update). The re-
examination produces either CONFIRMED-NO-CHANGE or REVISED. A
REVISED re-examination MUST NOT silently resolve an open conflict
(per §4.6) without naming the new evidence that would warrant
resolution. The default-to-preserve discipline carries through
drift re-examinations: open conflicts stay open unless explicit
new evidence (a tie-breaker HA verdict, a descriptive deep-dive
that exposes one reading as artifactual) lands and is named in
the REVISED artefact's §4.6 update.

## 8. Interview-prompt seeds

The `/research-interpret synthesise cluster-XXX` skill drives the
synthesis as an interview. Three required seeds per the locked-
plan §6.3 spec brief, plus an optional fourth:

### 8.1 Cluster pre-declaration check

> "Which HAs belong in this cluster per the synthesis-structure
> map's §3 row for `<cluster-id>`? What's the shared construct?
> Do you agree with the map's declared constellation, or does
> your reading of the cluster's members suggest the map needs
> revision?"

**Use.** Opens §4.2 of the synthesis (pre-declared constellation
citation) AND triggers the §6.1 map-change-needed halt criterion
1 check. The skill presents the map's §3 row verbatim (constituent
HA list, shared construct, operationalisation-overlap note) and
asks the user to confirm the constellation OR surface a proposed
map change. If the user surfaces a proposed change, the skill
halts per §6.1 and produces only the §4.9 open_inputs entry; if
the user confirms, the skill proceeds to §8.2.

**Hard rule.** The user's confirmation at §8.1 is the cluster-
level analogue of guide #1 §8.4 (verdict-trust audit confirmation)
and guide #2 §8.4 (verdict-trust audit confirmation) — a
**confirmation seed**, not a discovery seed. By the time the
skill reaches §8.1, the cluster's constellation should mechanically
match the map's §3 row; the seed exists to surface map-vs-stage
misalignment if it exists, not to re-decide the constellation in-
stage.

### 8.2 Coherence-call interview

> "Walking the §4.3 per-HA rows: do the member HAs point the same
> direction on the shared construct? Are the effect-size magnitudes
> consistent across operationalisations? Where they disagree, is
> the disagreement on direction (CONFLICT), magnitude/qualifier
> (PARTIALLY CONCORDANT), or facet-of-construct (ORTHOGONAL)?"

**Use.** Drives §4.4 (coherence call) and §4.6 (open conflicts).
The skill presents the §4.3 per-HA rows (built from each member's
`interpretation.md` §3 + §4 + §4.7 + §4.5) and asks the user to
articulate the cluster-level reading. The user's articulation is
cross-checked against §5's coherence-call mapping rules; if the
articulation matches a label cleanly, the skill records it as the
§4.4 call; if the articulation is ambiguous between labels (e.g.
PARTIALLY CONCORDANT vs CONFLICT for C-stress-fatigue-shape per
§5.2 + §5.3 alternative worked examples), the skill defaults to
CONFLICT per §4.4 hard rule and surfaces the choice explicitly.

For cascade-downstream clusters, the skill includes the cascade-
precondition handling per §5.5 in the interview before computing
§4.4 — surfacing the upstream cluster's coherence call as caveat-
class precondition and asking the user whether the cascade-
precondition changes the downstream's joint claim strength (per
§5.5 narrowing rule).

### 8.3 Joint-claim narrowing

> "Given the §4.4 coherence call, what does the cluster jointly
> license? What does it NOT license? Is the joint claim wider or
> narrower than any single member's licensed claim, and what
> justifies the width? Are any of the four predictable overclaim
> shapes (mechanism / group-level / predictive / averaging-the-
> conflict) live at the cluster level and need explicit refusal?"

**Use.** Drives §4.7a (what the cluster jointly licenses) and
§4.7b (what the cluster jointly does NOT license). The skill
presents the §4.4 coherence call + the §4.3 per-HA rows + the
map's §3 operationalisation-overlap-note (the cluster's evidence-
strength rationale) and asks the user to articulate the joint
claim's width and the four predictable overclaim refusals. The
articulation is cross-checked against §4.7a width discipline (no
wider than the narrowest member's claim unless cross-
operationalisation replication warrants it; independent vs same-
signal multi-take distinction) and §4.7b four-overclaim-refusal
list (mechanism, group-level, predictive, averaging-the-conflict).

### 8.4 Optional seed — cluster-trust upstream confirmation

> "The cluster's member HAs have Stage D verdict-trust calls of
> [TRUSTED / PROVISIONAL]. Cascade-arrow precondition (if
> applicable): the upstream cluster reached [LABEL]. Do you accept
> the cluster-trust chain carrying forward into the §4.7a joint
> claim's tier-narrowing (per §6.3) and the cascade-precondition
> qualifier (per §5.5)?"

**Use.** Confirms the §6.3 PROVISIONAL-narrowing rule and the
§5.5 cascade-precondition handling. This is a confirmation seed,
not a discovery seed — by the time the skill reaches it, the §4.5
cluster-level caveats sub-block and the §5.5 cascade-handling
sub-paragraph should mechanically reflect the upstream-trust chain.
The user's explicit acceptance of PROVISIONAL-carrying-forward (if
applicable) and cascade-precondition-handling (if applicable) is
the binding event for proceeding under the narrowed joint claim;
without it, the skill refuses to lock and routes to the upstream
gap.

## 9. Agent-instruction outline

This section is what `/research-interpret synthesise cluster-XXX`
(produced in §11 step 7 of the plan) will codify into its skill
behavior. The skill MUST follow these phases in order:

### 9.1 Load

The skill loads (in order): the synthesis-structure map's §3
cluster row for the target cluster, each cluster member HA's
locked `interpretation.md`, the cascade-arrow upstream cluster's
locked `cluster-*.md` (where applicable per the map's §3 cascade-
arrow language), the limitations doc's §5 citation requirements
row for `cluster-*.md`, the relevant methodology MDs (guides #1
and #2, and any cluster-specific methodology MDs the constituent
HAs cite), the four literature methodology anchors, and the non-
binding seed notes (loaded as advisory context only).

The skill MUST refuse to proceed if any of the following is
missing: any cluster member's `interpretation.md`; the map's §3
row for the target cluster; the cascade-arrow upstream cluster's
locked `cluster-*.md` (where the map's §3 row declares a cascade
precondition).

### 9.2 Gate

The skill checks the upstream status chain:

- **All members `interpretation.md` locked + cluster in map +
  cascade-upstream locked (where applicable)** → proceed to §9.3.
- **Any member's `interpretation.md` missing or unlocked** →
  halt; produce only the §4.9 `open_inputs` entry per refusal-
  path 1.
- **Cluster not in map** → halt; produce only the §4.9
  `open_inputs` entry per refusal-path 2.
- **Cascade-arrow upstream cluster's `cluster-*.md` missing or
  unlocked** (cascade-downstream clusters only) → halt; produce
  only the §4.9 `open_inputs` entry per refusal-path 3.

### 9.3 Extract

The skill extracts (per member HA): the verdict + qualifier
verbatim from the member's `interpretation.md` §1; the licensed-
claim sentence from §3; the most salient cluster-relevant
overclaim refusal from §4; the effect-size summary from §3; the
L-IDs cited from §4.5 5b; the closure-path statement from §4.7
where the verdict is PARTIAL or INCONCLUSIVE; the Stage D verdict-
trust call from §1.

The skill extracts (cluster-level): the map's §3 row cells
(shared construct, operationalisation-overlap-note, L-IDs column,
literature anchor, cascade-arrow language where applicable,
declared-date, lock-version).

The skill extracts (cascade-upstream, where applicable): the
upstream cluster's §4.4 coherence call + §4.7a joint claim
sentence, for the §4.5 cascade-precondition sub-paragraph
template.

### 9.4 Interview

The skill walks the §8 seeds in order — §8.1 (cluster pre-
declaration check, which doubles as the §6.1 halt-criterion-1
check), §8.2 (coherence-call interview), §8.3 (joint-claim
narrowing), §8.4 (cluster-trust upstream confirmation, if not
already handled at §9.2).

For each seed, the skill records the user's articulation, cross-
checks against §5 mapping rules and §7 anti-patterns, surfaces
mismatches, and seeks the operationalisation-bound or anti-pattern-
cleared rephrasing.

The skill MUST NOT autonomously fill §4.4 (coherence call) when
the §8.2 interview surfaces ambiguity; the user picks the label
per §4.4 hard rule (default-to-CONFLICT on ambiguity). The skill
MUST NOT autonomously fill §4.6 (open conflicts) without §8.2's
explicit conflict articulation.

### 9.5 Produce

The skill drafts `analyses/synthesis/cluster-XXX.md` following
the §4 outline. All ten sections (§4.1 through §4.10) are filled;
§4.5 carries the L-ID citation block per the map's §3 row PLUS
the L2-era-strata-mismatch cluster-level binding where it triggers
PLUS the cascade-precondition sub-paragraph where applicable; §4.6
carries open conflicts preserved per §4.4 label; §4.7a respects
the width discipline; §4.7b addresses the four predictable
overclaim refusals; §4.8 carries both tracks (own-research with
concrete pre-reg shapes; external-research with explicit N=1-
limit scoping per §3.11 binding); §4.9 carries `open_inputs`
entries per the three refusal paths plus any narrowing-input the
synthesis surfaces.

The artefact's status header records DRAFT r1, reviewer-mode-with-
authorization, and the `## Authorship` block per CONVENTIONS §1.2.

### 9.6 Refuse-to-lock gate

The skill MUST refuse to mark the artefact ready for completion
if any of the following holds:

- The §4.5 L-ID block is missing an L-ID the map's §3 cluster row
  lists (the map row is binding minus the HA-specific subtractions
  per §3 above).
- The cluster spans different era strata (per the limitations-doc
  §5 binding's "also cite L2" clause) and the L2-era-strata-
  mismatch citation is missing from §4.5 5b.
- The cascade-arrow precondition sub-paragraph (§4.5 5c) is
  missing on a cascade-downstream cluster.
- §4.4 carries an invented label outside the four-label set
  (CONCORDANT / PARTIALLY CONCORDANT / CONFLICT / ORTHOGONAL).
- §4.6 reads CONFLICT or PARTIALLY CONCORDANT but the open-
  conflict-preservation discipline is not honored (no both-readings
  paragraph, or auto-resolution-style language).
- §4.7b does not address the four predictable overclaim shapes
  explicitly (the four-bullet list is mandatory; presence of all
  four sentences is the structural check).
- §4.8 carries an external-research suggestion without explicit
  N=1-limit scoping (locked-plan §3.11 binding).
- §4.7a joint claim width exceeds the narrowest member's licensed
  claim without independent-operationalisation cross-
  operationalisation replication warrant per §4.7a width
  discipline.
- §4.3 / §4.4 / §4.5 / §4.6 / §4.7 contain anti-pattern violations
  per §7 (cross-cluster smuggling, sister-cluster evidence
  promotion, seed-notes-as-constraints, post-hoc caveat invention,
  §3.12 commentary, predictive-quality measures, label invention).

### 9.7 Review handoff

On user-accepted-as-ready-for-completion, the skill recommends a
fresh-session `/research-review` per locked-plan §4 producer/
reviewer split table for `cluster-*.md` (reviewer-mode-with-
authorization artefacts get `/research-review`, not `/research-
methodology-review` — see locked-plan §11 intro for the
discipline-gate routing). The review report lands at
`docs/research/reviews/cluster-XXX-synthesis-YYYY-MM-DD.md` per
the existing review-folder convention.

### 9.8 Acceptance + drift-trigger registration

Per locked-plan §3.8, "user explicitly accepts" is the binding
completion event. On acceptance: the status header transitions
to LOCKED with a lock-log entry; §4.9 `open_inputs` entries
propagate to the layer-wide `_open_inputs.md` queue; the topic
the cluster feeds (per the map's §4 row) becomes eligible for
Stage S₂ (when all topic-member clusters have locked `cluster-
*.md` per the locked plan §3 dependency rule). Per §3.7 drift
policy, the skill registers four re-examination triggers at lock
time:

1. Any constituent member's `interpretation.md` is re-examined or
   downgraded.
2. A new HA joins the cluster (per synthesis-structure map
   update).
3. A cited methodology MD changes lock-version (in particular
   [`research_line_limitations.md`](research_line_limitations.md),
   since L-ID citations propagate; and guides #1 + #2; and any
   cluster-specific methodology MDs).
4. ≥6 months elapse since lock (cadence check per locked-plan
   §3.7).

For cascade-downstream clusters, a fifth re-examination trigger
applies: the cascade-upstream cluster's `cluster-*.md` is re-
examined or revised. The cascade-precondition handling depends on
the upstream's coherence call; an upstream revision changes the
downstream's cascade-precondition sub-paragraph and may change
the joint-claim's strength.

**Drift-trigger registration is manual-pending-skill.** Until the
§11 step 7 `/research-interpret` skill lands, drift-trigger
registration is maintained by hand: the synthesis's §11 lock log
carries a "Drift triggers registered" line naming the four (or
five for cascade-downstream) trigger conditions, and a future
drift-check pass walks the lock logs of every synthesis to
identify clusters whose triggers have fired. This parallels the
audit's §9.6, the interpretation's §9.8, and the limitations
doc's §8 downstream-citation-count manual-tracking patterns (all
pending the skill).

The skill also increments the limitations doc's §8 downstream-
citation-count table for each L-ID cited in the synthesis's §4.5
block (manual until the skill lands per the limitations doc's §8
tracking-mechanism status note).

## 10. Cross-references

- [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  — §6.3 (the spec brief this guide implements); §3 (stage-map
  dependency rule for Stage S₁); §3.5 (missing-inputs flagging
  as first-class; the three refusal-to-proceed paths producing
  open_inputs entries); §3.6 (synthesis-structure pre-registration
  + map-vs-§6.3 conflict-resolution rule which is the §6.1
  halt-and-route discipline); §3.7 (drift and replication policy
  — four re-examination triggers, five for cascade-downstream);
  §3.8 (stopping and completion criteria for `cluster-*.md`);
  §3.9 (research-line limitations binding); §3.10 (hard predictive
  gate — Stage A forward pointer; Stage S₁ does not cross);
  §3.11 (follow-up research suggestions own + external tracks);
  §3.12 (subject-narrative commentary — Stage S₁ does not carry);
  §4 (producer/reviewer split table; `cluster-*.md` is reviewer-
  mode-with-authorization); §9 layer-level anti-patterns
  (synthesis-as-counting fallacy; retroactive constellation
  fallacy; the cluster-correlation-vs-causation, narrative-
  override, and related fallacies); §11 step 6.3 (the
  implementation step that produced this guide).
- [`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
  — guide #1, LOCKED r2 2026-06-24, the upstream-most discipline
  gate; the four-label verdict-trust call (TRUSTED / DOWNGRADED-
  INCONCLUSIVE-PROVISIONAL / REQUIRES-DESCRIPTIVE-WORK /
  STRUCTURALLY-UNTESTABLE) chain that Stage S₁ inherits via the
  member interpretation §1 headers.
- [`verdict_to_inference.md`](verdict_to_inference.md) — guide
  #2, LOCKED r2 2026-06-24, the immediate upstream gate. §3
  output convention (`analyses/interpretation/HA-XX.md`); §4
  nine-section outline (each member's interpretation feeds Stage
  S₁'s §4.3 per-HA rows); §5.5 verbatim-qualifier rule (Stage
  S₁ carries qualifiers verbatim into §4.1); §6.2 PROVISIONAL-
  carrying-forward rule (which Stage S₁ inherits per §6.3 above);
  §7 anti-patterns (Stage S₁ inherits as upstream discipline,
  especially §7.5 post-hoc caveat invention which §7.7 of this
  guide mirrors at the cluster level).
- [`research_line_limitations.md`](research_line_limitations.md)
  — §3 the seven L-IDs L1-L7; §5 citation requirements table
  (`cluster-*.md` row binds Stage S₁: "cite every limitation that
  touches any cluster member; also cite L2 if cluster members are
  from different era strata"); §8 downstream-citation-count
  table (Stage S₁ increments per L-ID cited).
- [`synthesis_structure_map.md`](synthesis_structure_map.md) —
  §2 initial scope (the three active clusters in the map's r3:
  C-stress-fatigue-shape, C-bout-framework, C-bout-substance);
  §3 cluster table (Stage S₁'s primary input — cluster name,
  constituent-HA list, shared construct, operationalisation-
  overlap-note, L-IDs column, cascade-arrow language); §4 topic
  table (forward pointer for §4.10 cross-references); §5
  construct table (forward pointer for Stage A — Stage S₁ does
  not cross §3.10).
- [`_synthesis_seed_notes_2026-06-23.md`](_synthesis_seed_notes_2026-06-23.md)
  — non-binding advisory; the r1 map-drafter's candidate joint-
  reading sketches for C-stress-fatigue-shape and C-bout-substance.
  Advisory only per §7.6 anti-pattern (treating sketches as
  constraints is forbidden).
- [`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md)
  — §4 the four HAs ready for Stage D TRUSTED that feed into
  the three active clusters' member interpretations; §9 user
  decisions on stocktake findings shaping the registry and
  reserved-slot work.
- [CONVENTIONS.md](../CONVENTIONS.md) — §1 (role split:
  `cluster-*.md` is reviewer-mode-with-authorization, not
  producer-mode); §1.2 (fresh-session peer review for reviewer-
  mode-with-authorization artefacts; `## Authorship` block);
  §2.1 (descriptive before inference); §3.4 (crash-drop
  sensitivity row on every Layer 4+ correlation — §5.7 operation-
  alises at the cluster level); §4.1 (no interpretive marks on
  raw descriptive layers); §4.2 (caveats vs a-priori claims);
  §4.3 (prior-driven hypotheses are confirmatory).
- Literature methodology anchors:
  [`literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf`](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)
  (primary anchor for Stage S₁'s multi-test synthesis discipline
  — the framing of how multiple within-subject tests on a shared
  construct combine into a single within-subject statement);
  [`literature/methodology/shamseer_2015_cent_consort_nof1.pdf`](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf)
  (CENT items 21 + 22 for cluster-level limitations and
  generalisability; §4.5 + §4.8 external-research scoping);
  [`literature/methodology/tate_2016_scribe_single_case_reporting.pdf`](../literature/methodology/tate_2016_scribe_single_case_reporting.pdf)
  (SCRIBE participant-as-researcher transparency for §4.5 L4
  citation at the cluster level);
  [`literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf`](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf)
  (the bar for defensible cluster-level coherence-call when
  within-subject multi-test evidence is the substrate).
- [`hypothesis_lock_process.md`](hypothesis_lock_process.md) —
  for §4.8 own-research follow-up tie-breaker sister-HA pre-reg
  drafting routing.
- [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md)
  — cluster-specific methodology MD for C-bout-framework /
  C-bout-substance member HAs.
- [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)
  — cluster-specific methodology MD for HA-C4c's cross-phase
  pooling discipline (which triggers the L2-era-strata-mismatch
  cluster-level citation at C-bout-substance's §4.5 5b).

## 11. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-24 | Drafted r1 | Producer-mode by fresh agent per §11 step 6.3 of [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md) (r5 LOCKED 2026-06-24). The agent added operational detail beyond the §6.3 spec at six points: (1) §5.5 cascade-arrow handling rule with concrete worked example for C-bout-substance reading C-bout-framework; (2) §5.6 trivial-ORTHOGONAL coherence call for single-member clusters (covering C-bout-framework and C-bout-substance as currently single-member in the map's r3); (3) §5.7 cluster-level crash-drop sensitivity discipline operationalising CONVENTIONS §3.4; (4) §6.3 cluster-trust PROVISIONAL inheritance + multi-PROVISIONAL non-compounding rule; (5) §6.4 cluster vs lived-experience prior reconciliation handling (cluster-level open conflicts vs §4.6 inheritance from member interpretations); (6) §9.6 phased refuse-to-lock gate with seven structural checks. Two §6.3 spec ambiguities resolved by interpretation: (a) the §6.3 spec's "operationalisation-overlap-note" feeding §4.4 was operationalised by reading from the map's §3 row cell verbatim and citing as evidence-strength rationale in §4.7a width discipline; (b) the §6.3 spec's "open conflicts preserved with both readings, no resolution" was operationalised by §4.6 paragraph-per-conflict shape + the §4.4 default-to-CONFLICT-on-ambiguity hard rule + §7.2 collapsing-CONFLICT-to-middle-reading anti-pattern. Two named-inventions-beyond-spec deserve user review: the §6.1 four halt-criteria for the map-change-needed halt (the locked plan §3.6 conflict-resolution rule names the discipline; the four concrete criteria are this guide's operationalisation); the §6.4 cluster-level prior reconciliation handling (the locked plan §6.3 spec does not address cluster-level prior tension explicitly; this guide's handling extends guide #2 §4.6 to the cluster level by analogy). |
