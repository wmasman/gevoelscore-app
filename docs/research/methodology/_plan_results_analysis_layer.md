# Plan — results-analysis methodology layer

**Status**: **LOCKED r5** by user acceptance 2026-06-24. r4 was
LOCKED 2026-06-23 and implementation started (steps 3-5 complete:
stocktake at [`_descriptive_stocktake_2026-06-23.md`](_descriptive_stocktake_2026-06-23.md);
limitations doc LOCKED r3 at [`research_line_limitations.md`](research_line_limitations.md);
synthesis-structure map LOCKED r3 at [`synthesis_structure_map.md`](synthesis_structure_map.md)
— map r2 → r3 propagated §3.12 commentary-eligible notes to K-cells).
r5 absorbed a user-requested mid-implementation refinement: §3.10
hard predictive gate stays inviolable for formal claims; new §3.12
sibling rule opens bounded patient-facing nuance space (subject-
narrative commentary at tier-1 and tier-2 attached, patient-audience
translation track only). Implementation proceeds to §11 step 6
(draft six guides). See §12 revision history for the r4 → r5 diff.

**Mode note**: This plan is a planning artefact that specifies
methodology MDs. r1 / r2 carried `reviewer-mode-with-authorization`
status; r3 reclassifies to **producer-mode** per the r2 review's
finding that planning artefacts are producer-mode infrastructure
(the reviewer-mode-with-authorization category is for individual
reviewer-mode artefacts drafted under user authorization, not for
planning scaffolds that specify them).

This plan is a **planning artefact**, not a binding methodology MD. The
binding outputs are the six guides this plan specifies plus two layer-
level supporting artefacts (`synthesis_structure_map.md` and
`research_line_limitations.md`). Once those land (each through its own
drafting + fresh-session review cycle), this plan becomes a historical
scaffold and can be archived under `_archive/`.

The underscore-prefix follows the existing convention for non-binding
planning artefacts in this folder (`_pending_literature_fetch.md`).

---

## 0. Purpose

The existing [methodology/](.) folder governs the **interpretive rules
upstream of any hypothesis test** — what the data means before any
verdict is produced. The corpus now contains 30+ locked pre-regs with
verdicts (REJECTED / SUPPORTED / PARTIAL / INCONCLUSIVE), plus an
[Addendum](../RESEARCH-REPORT-ADDENDUM.md) chain that has begun
synthesising. What is missing is a **declared, binding layer for the
work downstream of those verdicts**:

1. **Descriptive precondition audit** — evidence that each verdict's
   load-bearing assumptions actually held on its inputs.
2. **Verdict → hypothesis interpretation** — what each verdict
   substantively claims about the underlying hypothesis (and what it
   cannot claim).
3. **Internal cross-result synthesis** — how to reconcile when related
   HAs converge, diverge, or conflict.
4. **External-literature contextualisation** — where the corpus's
   findings sit relative to the published consensus (or lack of one)
   for each construct.
5. **Actionability translation** — when, if at all, a finding becomes
   usable for the patient-user's daily life or predictive of what is
   coming up. Under a **hard predictive gate**: no predictive claim
   without forward-validated replication. **Plus** a bounded
   **subject-narrative commentary layer** (per §3.12) that opens
   patient-facing nuance space at tier-1 and tier-2 attached
   commentary, with discipline rules that prevent the gate from
   being backdoored.
6. **Translation to audience** — translating findings into audience-
   targeted artefacts on two tracks: research-audience (peer-style
   reading) and patient-audience (laymen, especially PAIS patients).
   Plain-language discipline, narrative arc, visual summary, honest
   uncertainty calibration, patient-relevance test.

Two supporting artefacts at the methodology layer also fall in scope:

- **Synthesis-structure map** (`methodology/synthesis_structure_map.md`)
  pre-registers which HAs cluster, which clusters feed which topics,
  which topics feed which actionability constructs — before any S₁/S₂/A
  drafting begins. This is the layer-level analogue of pre-registering
  an HA: the structural choices are themselves story-shaping and must
  be locked in advance.
- **Research-line limitations** (`methodology/research_line_limitations.md`)
  enumerates the systemic limitations of the research line (single-
  subject reach, era confounds, device generations, analyst-is-subject,
  presence-conditioned data layer, self-reporting, survivorship). Per-
  topic and per-construct artefacts cite from this doc rather than
  inventing or omitting limitations independently.

The interview-style human-agent collaboration the user named in the
request lives in a **single skill** (`/research-interpret`), not in the
guides themselves. Guides are declarative rules an agent must respect;
the skill is the interview engine that loads a guide and walks the user
through its procedure step by step.

## 1. Scope and out-of-scope

**In scope.** Producing the six guide MDs + two layer-level supporting
artefacts + one skill that together let any future session take an
existing HA result (or cluster of results) from verdict to interpretive
claim to placed-in-context to (optionally) actionable signal to
audience-targeted translation, under the same producer-vs-reviewer
discipline already established in [CONVENTIONS.md](../CONVENTIONS.md).

**Out of scope.** Re-interpreting any specific HA. The plan and the
guides it produces are *infrastructure*; the act of interpreting
HA-C4 (or any other result) happens in a separate session that loads
the relevant guide via `/research-interpret`.

**Also out of scope.** Re-litigating methodology decisions already
locked in this folder. If a guide produces a finding that depends on a
methodology decision being wrong, the conflict-resolution rule routes
back through the existing lock-process discipline, not through
ad-hoc revision.

## 2. Locked decisions from the planning session

These three decisions came from the user in the planning conversation
that produced this draft. They are locked at the plan level and inherit
into every guide.

| Decision | Value | Consequence |
|---|---|---|
| Output location | One folder per stage | New folders: `analyses/interpretation/`, `analyses/synthesis/`, `analyses/contextualisation/`, `analyses/actionability/`. Existing `analyses/descriptive/` already covers Stage D. |
| Predictive-claim gate | Hard | Retrospective-only evidence caps at tier "informative pattern." "Predictive use" tier requires forward-validated replication via a pre-registered prediction-window test against unseen days. |
| Skill shape | Single skill, guide chosen from args | `/research-interpret <guide> <target>` loads the guide MD as data, walks the procedure as interview. No duplication of rule content between skill and guide. |
| Artefact naming inside per-stage folders | By HA when single-HA, by cluster/topic otherwise | `interpretation/HA-C4.md`; `synthesis/cluster-stress-load.md`; `contextualisation/topic-hrv-in-lc.md`; `actionability/by-construct.md`. |
| Plan review discipline | r1/r2: reviewer-mode-with-authorization → r3: producer-mode (per r2 review finding) | Fresh-session `/research-methodology-review` runs against this plan before any guide is drafted (completed for r2). Guides themselves are producer-mode (binding methodology MDs reviewed by `/research-methodology-review`); their *outputs* (interpretation, synthesis, contextualisation, actionability, translation MDs) are reviewer-mode-with-authorization and reviewed by `/research-review`. |

## 3. Stage map and dependencies

```
                                          ┌────────────────────────┐
                                          │  D. Descriptive        │
                                          │     precondition audit │
                                          │  (analyses/descriptive)│
                                          └───────────┬────────────┘
                                                      │ must complete per HA
                                                      ▼
                                          ┌────────────────────────┐
                                          │  I. Verdict →           │
                                          │     interpretation      │
                                          │  (analyses/interpret…)  │
                                          └───────────┬────────────┘
                                                      │ per cluster
                                                      ▼
                                          ┌────────────────────────┐
                                          │  S₁. Internal synthesis │
                                          │   (analyses/synthesis)  │
                                          └───────────┬────────────┘
                                                      │ per construct/topic
                                                      ▼
                                          ┌────────────────────────┐
                                          │  S₂. External           │
                                          │      contextualisation  │
                                          │   (analyses/context…)   │
                                          └───────────┬────────────┘
                                                      │ per construct
                                                      ▼
                                          ┌────────────────────────┐
                                          │  A. Actionability       │
                                          │     translation         │
                                          │   (analyses/actionab…)  │
                                          └───────────┬────────────┘
                                                      │ per artefact to be
                                                      │ communicated outward
                                                      ▼
                                          ┌────────────────────────┐
                                          │  T. Translation         │
                                          │     to audience         │
                                          │  (analyses/translation) │
                                          └────────────────────────┘
                                          ▲ A: hard predictive gate
                                          │ (forward-validation only)
                                          ▲ T: both audience tracks
                                          │ (research + patient)
```

**Dependency rules** the skill must enforce when invoked:

- `I` on a given HA refuses to start without a `descriptive_audit.md`
  for that HA backing each load-bearing assumption.
- `S₁` on a cluster refuses to start until every HA in the cluster has
  a current `interpretation.md`, AND the cluster appears in the
  pre-registered `synthesis_structure_map.md` (per §3.6).
- `S₂` on a topic refuses to start until `S₁` for the relevant
  cluster(s) is complete, AND the topic appears in the pre-registered
  synthesis-structure map, AND `research_line_limitations.md` exists
  (per §3.9 — topic-level contextualisation cites from it).
- `A` on a construct refuses to start until `S₂` for the relevant
  topic(s) is complete AND the construct appears in the pre-registered
  synthesis-structure map AND the actionability tier being claimed is
  permitted by the evidence layer (forward-validation required for
  predictive tier).
- `T` on a target refuses to start until the source-stage artefact is
  locked AND `research_line_limitations.md` exists. `T` may target any
  prior stage's output (interpretation, synthesis, contextualisation,
  or actionability); it is not strictly serial after `A`.

Skipping is allowed only when the skipped stage is **structurally
trivial** for the target (e.g. a single-HA cluster's `S₁` collapses to
"see interpretation.md") — and even then, an explicit
`stage_skipped.md` stub must record why. `T` is the one stage that is
optional: research-internal scaffolding (audits, raw interpretations
not intended for outward communication) does not require a translation
artefact. The decision to skip `T` for a given target is recorded
explicitly so the skip is intentional, not accidental.

## 3.5 Missing-inputs flagging is first-class

The point of every refusal-to-proceed in this layer is not to block
work; it is to **make the missing-input pathway productive**. The
dataset has hard boundaries — coverage gaps, presence-conditioned
signals, era spans the corpus does not reach — and the layer must
surface what is missing as work-to-do rather than silently widening
claim language to fit what is present.

Mechanism: **every guide produces, alongside its main artefact, a
structured `open_inputs` block** that names exactly:

1. What input is missing (artefact, signal, descriptive run,
   literature reference, forward-validation HA, lived-experience
   reconciliation).
2. What stage / target / claim it is blocking.
3. The cheapest path to acquire it (which script, which `/fetch-paper`
   call, which descriptive run, which pre-reg shape).
4. The fallback claim available without it (always at most one tier
   narrower than the claim being blocked).

The skill aggregates these across stages into a single
`docs/research/methodology/_open_inputs.md` queue, sortable by what
unblocks the most downstream work. This becomes a routable
work-list: each entry is either an acquire-task (descriptive,
literature, new HA pre-reg) or a downgrade-and-proceed acceptance
recorded by the user.

**Hard rule.** The skill never silently degrades a claim to fit
available inputs. If a tier requires forward-validation and none
exists, the skill produces the lower-tier artefact AND an
`open_inputs` entry naming the missing forward-validation HA, never
the higher-tier artefact with weakened wording.

**Hard rule.** Acquiring a missing input via a path that contaminates
later inference (e.g. running a descriptive analysis whose results
are visible to a session that will then draft a result claim on them)
violates the fresh-session discipline per
[CONVENTIONS §1.2](../CONVENTIONS.md) and is forbidden. Missing inputs
get acquired under producer-mode discipline appropriate to their
type.

## 3.6 Synthesis-structure pre-registration

The clusters, topics, and actionability constructs that `S₁` / `S₂` /
`A` operate on must be **pre-declared as a layer-wide map** *before*
any guide-driven drafting begins on those stages. The choice of which
HAs cluster together, which clusters feed which topic, which topics
feed which construct is itself story-shaping. Producing that map
reactively (per-cluster as drafting begins) lets the same cherry-pick
that pre-registration protects against re-enter at the synthesis layer.

**Artefact.** `methodology/synthesis_structure_map.md`. Sections:

- **Cluster table** — cluster name → constituent HA IDs → shared
  construct → operationalisation-overlap note (independent tests vs
  same-signal multi-takes) → declared by + date.
- **Topic table** — topic name → constituent clusters → construct →
  relevant literature topic for Stage S₂ → declared by + date.
- **Construct table** — construct name → topics that feed it → tier
  aspiration (monitoring / informative / predictive) → declared by +
  date.
- **Lock log** — each row carries a lock entry; additions, removals,
  or re-scoping are appended with date and reason, not silently
  edited.

**Rules.**
- The map is read by `/research-interpret` before `S₁` / `S₂` / `A`
  invocations; the dependency rule in §3 refuses to start if the
  target is not in the map.
- The map can grow over time. New HAs land → new rows are *appended*
  with explicit lock entries, never silently merged into existing
  clusters.
- The map is producer-mode (Claude drafts under interview) and gets a
  fresh-session `/research-methodology-review` like other methodology
  MDs before lock.
- A cluster/topic/construct moves from "proposed" to "locked" only by
  explicit user acceptance.

**Conflict-resolution rule (vs §6.3 per-cluster pre-declaration).**
§6.3 requires per-cluster pre-declaration by constituent HAs before
that cluster's `S₁` synthesis begins. The two layers are
**complementary, not redundant**: §3.6 owns the layer-wide
constellation; §6.3 owns the per-cluster sign-off the user gives
immediately before drafting begins. When per-cluster S₁ work reveals
that the §3.6 map needs to change (an HA belongs in a different
cluster, a new cluster should exist, a topic boundary is wrong):

1. **Halt the S₁ session immediately.** Do not edit the map in-session;
   that would couple the map's structure to the very synthesis
   results that are about to be drafted from it.
2. **Record the proposed map change** in the open_inputs ledger with
   the target cluster/topic/construct named and the trigger described.
3. **Resume S₁ on the affected cluster** only after a separate
   producer-mode session updates the map (with its own
   `/research-methodology-review` pass before re-lock).
4. **The §3.6 map is authoritative** for the cluster name, constituent
   HA list, and topic/construct rollup. §6.3 per-cluster pre-
   declaration confirms what §3.6 already says; it cannot add or
   remove constituents without first triggering the map-update
   pathway above.

**Why this rule.** Without it, the same session that would discover a
clustering problem during S₁ would be tempted to fix it in flight,
collapsing the layer-wide map's pre-registration discipline back into
the per-cluster ad-hoc decisions §3.6 exists to prevent.

**Why this is binding.** Without §3.6 itself, every Stage S₁ session
re-invents the clustering, every Stage S₂ session re-invents the topic
boundary, and the layer's outputs stop being commensurable across
constructs.

## 3.7 Drift and replication policy

Locked artefacts decay. New data arrives every day; methodology MDs
evolve; the v24 categorisation may be replaced; HA results may be
re-run. A locked interpretation, synthesis, contextualisation,
actionability, or translation artefact has a **stated re-examination
condition**.

| Artefact type | Re-examination trigger |
|---|---|
| `descriptive_audit.md` | Underlying HA's `result.md` re-runs; OR cited methodology MD changes lock-version. |
| `interpretation.md` | Underlying `descriptive_audit.md` is re-examined; OR the HA's `result.md` re-runs; OR a cited methodology MD changes lock-version; OR ≥ 6 months elapse since lock (cadence check). |
| `cluster-*.md` | Any constituent `interpretation.md` re-examined or downgraded; OR a new HA joins the cluster (per synthesis-structure map update). |
| `topic-*.md` | Any constituent `cluster-*.md` re-examined; OR a new literature reference of moderate-or-higher relevance lands; OR `research_line_limitations.md` is updated. |
| `construct-*.md` (actionability) | Any constituent `topic-*.md` re-examined; OR a forward-validation HA produces a new verdict; OR a tier-affecting methodology change. |
| Translation artefacts | Any source-stage artefact is re-examined; OR plain-language dictionary terms shift meaning. |

A re-examination produces one of two outcomes, both recorded:

1. **CONFIRMED-NO-CHANGE** — timestamped entry in the artefact's lock
   log; nothing about the artefact changes. This *is itself an artefact*,
   not a silent decision.
2. **REVISED** — produces a new version of the artefact under the
   normal drafting + fresh-session-review cycle. The prior version is
   archived under `_archive/` with a note pointing to the new one.

**Cadence check.** Every six months, the skill (or a periodic
session) walks all locked artefacts and surfaces those whose
re-examination trigger conditions have fired since the last check.
The user then decides which to actually re-examine in priority order.

## 3.8 Stopping and completion criteria

Each artefact has an explicit "done for now" condition. Without this,
the layer loops on increasingly small refinements and never produces
a usable surface.

| Artefact | Completion condition |
|---|---|
| `descriptive_audit.md` | All load-bearing assumptions BACKSTOPPED or downgraded with `open_inputs` entries logged; verdict-trust call made; user explicitly accepts. |
| `interpretation.md` | All section-outline fields filled; checklist ticked or `open_inputs` entries logged for each unticked item; lived-experience prior reconciliation done (even if conflict is left open); follow-up suggestions section filled (own + external tracks per §3.11); user explicitly accepts. |
| `cluster-*.md` | All HAs in the pre-declared cluster have current `interpretation.md`; coherence call made; joint claim narrowed appropriately; `open_inputs` logged; follow-up suggestions section filled (own + external tracks per §3.11); user explicitly accepts. |
| `topic-*.md` | All constituent clusters synthesised; positioning call made (CANNOT-SAY is valid); every external claim cited or in literature-gap log; per-topic limitations cited from `research_line_limitations.md`; follow-up suggestions section filled (own + external tracks per §3.11); user explicitly accepts. |
| `construct-*.md` | Tier claim made; tier no higher than evidence layer permits; forward-validation pathway specified if tier 3 wanted but unearned; tier-2-or-above claims report PPV + base-rate in plain-language frame per §3.10 (or have tier downgraded); follow-up suggestions section filled (own + external tracks per §3.11); **optional subject-narrative commentary section** per §3.12 either filled (with attach-citation, subject-attribution, language-discipline) or recorded-as-skipped; user explicitly accepts. |
| Translation artefacts | Both audience tracks produced (or skip-research-internal recorded); plain-language dictionary updated; visual summary present or specified; patient-relevance test passed; quality-measure translation present where source artefact is tier-2+ per §3.10; follow-up communication section filled per §3.11; **patient-audience track only** carries §3.12 subject-narrative commentary (if the source `construct-*.md` has one; commentary is forbidden in research-audience track); user explicitly accepts. |

**"User explicitly accepts"** is the binding event for completion. The
skill marks an artefact as "ready for completion review" when its
checklist is fully ticked or fully open-inputs-logged, but it never
auto-completes. The user's acceptance is the lock event.

**Open inputs do not block completion.** An artefact can be COMPLETE
*and* carry open_inputs entries. Completion means "this is the best
version with the inputs we currently have, and we have logged what
would improve it." It does not mean "no further work is possible."

## 3.9 Research-line limitations binding

A layer-level `methodology/research_line_limitations.md` MUST exist
before any topic-level contextualisation or actionability artefact is
locked. It enumerates the **systemic** limitations of the research
line — limitations that apply across all findings and that no per-HA
caveat can absorb. Initial coverage:

- **Single-subject reach** — N-of-1; group-level inference reach bounded
  by Daza 2018, CENT, Natesan 2023.
- **Era confounds** — COVID variants, vaccination history, medication
  phases, life circumstances. Eras are not interchangeable.
- **Device generations** — Garmin model changes across years;
  calibration drift; firmware-version effects on derived signals.
- **Analyst-is-subject** — the user is both researcher and study
  participant; not blindable; introspection-laden.
- **Presence-conditioned data layer** — v24 semantics; no prevalence
  claims from these signals; cited from `symptom_mention_asymmetry.md`.
- **Self-reporting** — gevoelscore is subjective; affected by
  interoception, mood, time-of-entry, recall artefacts.
- **Survivorship** — only days where data was collected; missingness
  patterns biased toward functional days for some signals.

**Binding rule.** Per-topic contextualisation MDs and per-construct
actionability MDs MUST cite the relevant limitations from this doc;
they are not free to invent or omit limitations independently. New
systemic limitations get added via the same producer-mode lock process
as other methodology MDs.

**Why this is binding at the layer level.** Per-HA caveats live inside
individual interpretation MDs and are tied to that operationalisation.
Systemic limitations apply across the entire corpus and would otherwise
be re-stated (inconsistently) in every topic or construct artefact, or
worse, omitted from some.

## 3.10 Predictive-quality measures, base-rate framed

Tier-2-or-above actionability claims (informative pattern, predictive
use) must report diagnostic-quality measures calibrated against the
relevant base rate. The project's existing precedent for this style is
[RESEARCH-REPORT §5.2](../RESEARCH-REPORT.md): *"The positive predictive
value of any such alert, even computing optimistically from H02b's
train-window evidence, is ~4% at the residual-crash base rate of ~2
per year. A predictive alert card would be wrong 24 times out of 25."*
Number plus what-it-means-in-everyday-frequencies. That is the
discipline.

**Required at tier-2 and tier-3:**

- **PPV** (positive predictive value) — when the signal fires, how
  often the predicted outcome actually follows.
- **Base rate** of the outcome in the relevant population (own data,
  era-stratified per §3.9 limitations — not aggregated across eras).
- **Plain-language frame** — "right N out of M when it fires" / "wrong
  M-N out of M when it fires," in line with RESEARCH-REPORT §5.2 style.

**Optional at tier-2 and tier-3** (encouraged where computable):

- NPV (negative predictive value) — when the signal is quiet, how
  often the outcome correctly does not follow.
- Sensitivity (true positive rate) — what fraction of real events the
  signal catches.
- Specificity (true negative rate) — what fraction of non-events the
  signal correctly stays quiet on.
- False-alarm rate (1 − specificity, in everyday language).
- Lead time — how far in advance the signal precedes the event
  ("a day," "an hour," "in the moment").
- Reliability — test-retest stability of the signal itself; how often
  similar days produce similar signal values.

**Tier-3 (predictive use) additional discipline.** Lead time and
reliability are strongly encouraged. A predictive claim that does not
specify "a day in advance" vs "an hour in advance" is operationally
meaningless; one that does not check whether the signal is stable
across similar days has no defence against random-walk artefacts.

**Forbidden at the HA-test level** per
[`personal_hypotheses.md`](../personal_hypotheses.md) §32 ("Descriptive
characterisation, not classifier discrimination — no AUCs, no logistic
regression, no joint-model verdicts. Means, CIs, effect sizes only."):
classifier-discrimination measures stay out of HA test specs and HA
result.md files. Diagnostic measures enter only at the actionability
layer, where the question is "how usable is this in life," not "is the
underlying relationship real." The HA layer establishes reality; Stage
A measures usability.

**Conflict rule.** If a tier-2-or-above claim cannot be calibrated to
a base rate (no clear denominator, sparse outcome, base rate not
stable within an era), the tier downgrades to monitoring (tier-1) and
the missing base-rate is logged in `open_inputs`. The skill never
lets an uncalibrated quasi-predictive claim pass with hedged wording.

**Why this is binding.** Without it, a tier-2 or tier-3 claim is a
label without a number — the reader cannot judge whether to trust it.
RESEARCH-REPORT §5.2 saved the app design from a bad feature (the
daily-aggregate alert card) precisely by reporting PPV-with-base-rate;
that precedent generalises.

## 3.11 Follow-up research suggestions — own + external tracks

Every reviewer-mode-with-authorization artefact (interpretation,
synthesis, contextualisation, actionability, translation) closes with
a **Follow-up suggestions** section, separated into two tracks:

- **Own-research track** — what HAs we should pre-register next given
  this finding. Pre-reg shapes, not vague directions. Includes
  forward-validation HAs (for actionability tier promotion), tie-
  breaker HAs (for cluster conflicts), descriptive deep-dives (for
  unbacked assumptions), and replication HAs (for re-running an
  operationalisation on new data).
- **External-research track** — what someone with a different setup
  should test, *scoped by our N=1 constraints*. Examples: group-level
  confirmation (requires N >> 1); intervention or RCT study (requires
  randomisation we cannot perform on ourselves); different-population
  test (requires demographic spread); different-measurement test
  (requires alternative wearable / clinical instrument).

**Distinct from `open_inputs`** (per §3.5). `open_inputs` is "what is
missing to complete *this current claim*." Follow-up suggestions are
"what *next claims* could be built — for us or for others." Both are
required; neither substitutes for the other.

**Required scoping discipline for the external-research track.** Every
external-research suggestion must explicitly state which aspect of our
N=1 limits (per `research_line_limitations.md`, §3.9) prevents us from
answering the question ourselves. "Someone should run an RCT" without
"we cannot because we have one subject and no comparator arm" is hand-
waving. Honest scoping is what distinguishes a follow-up suggestion
from a wishlist.

**Per-stage shape.**

- Stage I (interpretation): own = what HA would replicate / refute /
  extend this operationalisation. External = what would test the
  hypothesis in a comparable population.
- Stage S₁ (synthesis): own = tie-breaker HAs for conflicts;
  independence checks across operationalisations. External = group-
  level cluster studies on the same construct.
- Stage S₂ (contextualisation): own = HAs that would tighten our
  positioning vs the literature; literature-gap entries fed via
  `/fetch-paper`. External = study designs that would settle a
  divergence with consensus.
- Stage A (actionability): own = forward-validation HA shape for tier
  promotion (already partially specified in §6.5; framed here as
  own-research follow-up). External = intervention or RCT study that
  could test causality vs association.
- Stage T (translation): own = what aspects of "still unknown" the
  next research session should target. External (patient-audience
  variant) = what the patient could ask a clinician; what observation
  they could make themselves.

**Why this is binding.** Without it, every artefact ends at "here is
what we know"; the natural next move ("what next") is left to memory
across sessions and decays. The follow-up section is the routable
next-work for the research line beyond completing the current claim.

## 3.12 Subject-narrative commentary — bounded reading-of-tea-leaves space

The §3.10 hard predictive gate protects **the research's external
defensibility**: no formal predictive claim without forward-validated
replication. But real patient use of a tier-1 or tier-2 finding
necessarily involves the subject interpreting the signal in lived
context, and that interpretation has utility worth recording. The
two are different epistemic categories:

- The §3.10 gate is about *what claims the research can make about
  predictive validity* (external defensibility, peer-review-ready).
- This §3.12 commentary layer is about *what the subject is allowed
  to say about the signal in lived experience* (patient-facing
  nuance, subject-attributed, not a forecast).

By naming them separately, the layer prevents silent slippage from
"I notice X often precedes Y in my experience" (legitimate subject-
commentary) into "X predicts Y" (illegitimate predictive overclaim).

**Where commentary lives.** Optional section in Stage A `construct-*.md`
artefacts (titled "Subject-narrative commentary — §3.12-bounded")
and optional section in Stage T **patient-audience track only**.
Commentary may attach to a **tier-1 monitoring** or **tier-2
informative-pattern** formal claim — not to a tier-3 predictive
claim (those carry the forward-validation HA and don't need
commentary nuance), nor to claims absent (commentary cannot float
unattached).

**Required discipline.**

- **Cite the attached claim**: every commentary section opens with
  "attached to: K-XXX tier-N claim per §X.Y".
- **Subject-attribution every sentence**: "I", "the subject", "in
  this subject's experience" — never bare third-person assertion.
- **Permitted language**: "I notice", "in my experience", "in
  retrospect", "I sometimes", "the pattern hints at / suggests-not-
  confirms / reads as", "worth attention", "I lean toward".
- **Forbidden language**: "predicts", "forecasts", "will happen",
  "tomorrow", "X means Y", "this signals that...", any causal-claim
  or forecast-claim wording.

**Hard separations** (these keep the §3.10 gate inviolable):

- Commentary **cannot promote actionability tier**. A construct
  artefact with rich commentary stays at its formal tier; commentary
  does not count toward tier-2 → tier-3 promotion. Only a
  pre-registered forward-validation HA per §3.10 unlocks tier-3.
- Commentary **cannot be cited as evidence** in HAs, interpretations,
  syntheses, contextualisations, or research-audience translations.
  It is patient-facing nuance, not analytical input.
- Commentary **cannot float unattached**. Every commentary section
  attaches to a formal claim (tier-1 or tier-2). "Subject suspects a
  thing nobody tested" is forbidden — that belongs in the §3.11
  follow-up-suggestions track as a candidate own-research HA.
- Commentary is **forbidden in research-audience translation track**
  per the locked decision. The research-audience reader sees the
  formal claim + caveats; the subject's narrative belongs only at
  patient-audience track.

**Layperson-test propagation.** Per §6.6 translation discipline, the
patient-audience track is layperson-tested. If commentary wording
fails the test (e.g., a layperson reads "I lean toward resting on
those days" as a soft prediction), the commentary is revised before
lock — the revision-trigger is the layperson's actual interpretation,
not the drafter's intent.

**Why this works without breaking the gate.** The gate prevents the
research from claiming predictive validity it has not earned. The
commentary layer allows the subject to use the signal interpretively
in daily life without the research overstating what it can defend
externally. The discipline rules (attached, attributed, tier-bound,
non-promoting, non-citable, language-bounded) make commentary a
first-class but operationally constrained space — useful but
unable to backdoor into formal claims.

## 4. Producer / reviewer split

| Artefact | Mode | Drafting session | Review session |
|---|---|---|---|
| Guide MDs (6×) | Producer | Claude drafts each guide MD in turn | Fresh-session `/research-methodology-review` (binding methodology MDs) |
| `synthesis_structure_map.md` | Producer | Claude drafts under interview with user | Fresh-session `/research-methodology-review` (binding methodology MD) |
| `research_line_limitations.md` | Producer | Claude drafts under interview with user | Fresh-session `/research-methodology-review` (binding methodology MD) |
| `plain_language_dictionary.md` | Producer | Maintained by `/research-interpret` translate stage; one term added per technical term encountered | None (live document) |
| `/research-interpret` skill | Producer | Claude builds | Skill-test session: dry-run on one HA per guide |
| `descriptive_audit.md` (per HA) | Producer | Claude under interview | None (audit, not verdict) |
| `interpretation.md` (per HA) | Reviewer-mode-with-authorization | Skill-driven; user authorizes | Fresh-session `/research-review` |
| `cluster-*.md` synthesis | Reviewer-mode-with-authorization | Skill-driven | Fresh-session `/research-review` |
| `topic-*.md` contextualisation | Reviewer-mode-with-authorization | Skill-driven | Fresh-session `/research-review` |
| Actionability tier claims | Reviewer-mode-with-authorization | Skill-driven, with **hard gate** | Fresh-session `/research-review`; tier downgrades on review concerns |
| Translation artefacts (research-audience + patient-audience) | Reviewer-mode-with-authorization | Skill-driven | Fresh-session `/research-review` plus layperson-test where patient-audience track exists |

This preserves [CONVENTIONS §1.2](../CONVENTIONS.md) — the same
fresh-session-review discipline that protects HA pre-regs and result
docs extends to every interpretive artefact this layer produces.

## 5. Output structure

```
docs/research/
├── analyses/
│   ├── descriptive/              ← existing; Stage D outputs land here
│   │   ├── HA-C4/                ← per-HA audit folders
│   │   │   └── descriptive_audit.md
│   │   └── ...
│   ├── interpretation/           ← NEW; Stage I outputs
│   │   ├── HA-C4.md              ← by-HA naming
│   │   └── ...
│   ├── synthesis/                ← NEW; Stage S₁ outputs
│   │   ├── cluster-stress-load.md     ← by-cluster naming
│   │   ├── cluster-recovery-rhr.md
│   │   └── ...
│   ├── contextualisation/        ← NEW; Stage S₂ outputs
│   │   ├── topic-hrv-in-lc.md         ← by-topic naming
│   │   ├── topic-pem-pacing.md
│   │   └── ...
│   ├── actionability/            ← NEW; Stage A outputs
│   │   ├── construct-overnight-recovery.md
│   │   └── ...
│   └── translation/              ← NEW; Stage T outputs
│       ├── research-audience/         ← peer-style track
│       │   ├── HA-C4.md               ← named by source artefact
│       │   ├── cluster-stress-load.md
│       │   └── ...
│       └── patient-audience/          ← laymen / PAIS patient track
│           ├── HA-C4.md
│           ├── construct-overnight-recovery.md
│           └── ...
└── methodology/
    ├── _plan_results_analysis_layer.md    ← this file (deletable post-launch)
    ├── _open_inputs.md                    ← live queue (per §3.5)
    ├── synthesis_structure_map.md         ← NEW supporting MD (per §3.6)
    ├── research_line_limitations.md       ← NEW supporting MD (per §3.9)
    ├── plain_language_dictionary.md       ← NEW live document (maintained by Stage T)
    ├── descriptive_precondition_audit.md  ← guide #1
    ├── verdict_to_inference.md            ← guide #2
    ├── internal_synthesis.md              ← guide #3
    ├── external_contextualisation.md      ← guide #4
    ├── actionability_translation.md       ← guide #5
    └── translation_to_audience.md         ← guide #6
```

The skill lives at the standard skill location (likely
`.claude/skills/research-interpret/SKILL.md`) and is invoked as
`/research-interpret`.

## 6. The six guides — per-guide spec

Each subsection below is the **brief for a single guide MD**. Future
sessions drafting these guides should be able to write each one
mechanically from its subsection, applying the conventions in
[CONVENTIONS.md](../CONVENTIONS.md) and the existing methodology MD
shape (status header, one-paragraph rule, why, operationalisation,
cross-refs).

---

### 6.1 `descriptive_precondition_audit.md` — Stage D

**Purpose.** Before any interpretation is built on a verdict, prove
the verdict's load-bearing assumptions held. Statistical interpretation
piggybacks silently on assumptions (block-length validity, era
integrity, sample-size adequacy, missingness pattern, presence-
conditioned semantics for v24 derivatives, distributional shape where
tests are non-rank-based). When an assumption is silently violated,
the verdict is structurally untrustworthy — independently of its
internal logic.

**Inputs.**
- The target HA's `hypothesis.md` (locked) and `result.md`.
- The methodology MDs the hypothesis cites in its §1 / §4 sections.
- `analyses/descriptive/` artefacts already produced for this corpus.
- The HA's `test.py` (to enumerate which assumptions the code path
  actually relies on, not just which the prose claims).

**Output.** `analyses/descriptive/HA-XX/descriptive_audit.md` —
one file per HA. Per-HA folder may also accumulate supporting plots
under `analyses/descriptive/HA-XX/figures/`.

**Section outline** for the produced `descriptive_audit.md`:

1. Target HA + result reference.
2. Load-bearing assumptions enumerated (one row per assumption, with
   source — pre-reg §X / methodology MD §Y / test.py line range).
3. Per-assumption status: BACKSTOPPED (citing the descriptive artefact)
   / NOT BACKSTOPPED (citing what is missing) / NOT APPLICABLE (with
   reason).
4. Verdict-trust call: TRUSTED / DOWNGRADED-INCONCLUSIVE-PROVISIONAL /
   REQUIRES-DESCRIPTIVE-WORK.
5. **`open_inputs` block** (per §3.5): each NOT-BACKSTOPPED row maps
   to an entry naming the missing descriptive artefact, what
   downstream stage it is blocking, the cheapest acquisition path
   (which script under `analyses/descriptive/` to run, or which new
   one to write), and the fallback claim available without it.

**Checklist sketch** (what an audit must tick):

- [ ] Sample size on every reported cell ≥ pre-registered floor.
- [ ] Missingness pattern is MCAR/MAR-compatible with the test, OR a
      missingness-aware operationalisation was used and is documented.
- [ ] For block-permutation tests: stationarity assumption checked or
      block-length sensitivity-tested per
      [`permutation_null_block_length.md`](permutation_null_block_length.md).
- [ ] For era-stratified tests: era boundaries match
      [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md);
      Stratum 4 primary surface honored.
- [ ] For v24-derived signals: presence-conditioned semantics respected
      per [`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md);
      no prevalence claim made on a presence-conditioned signal.
- [ ] For nightly/recovery signals: wake-up-date attribution per
      [`nightly_attribution.md`](nightly_attribution.md).
- [ ] Effect-size direction reported alongside p-values, never alone.
- [ ] Where train/validate split was used: per
      [`train_validate_split_fate.md`](train_validate_split_fate.md),
      single-pool primary preserved.

**Conflict rules.**
- Descriptive contradicts the test's assumption → verdict is
  downgraded to INCONCLUSIVE-PROVISIONAL. No interpretation may be
  built on it until the descriptive issue is resolved (either by new
  test, new operationalisation, or by accepting a narrower claim).
- Descriptive cannot be produced because data does not exist → the
  HA is flagged for "structurally untestable as currently specified"
  and routed back to pre-reg revision.

**Anti-patterns explicitly forbidden.**
- "The test ran, therefore the assumptions held."
- Citing a single descriptive plot as evidence the assumption held
  globally when it only shows one cell.
- Backstopping an assumption with a descriptive artefact that was
  generated *after* the test and whose generation peeked at the
  test's per-day values.

**Interview-prompt seeds** the skill must ask:
- "Which assumptions in this HA's §4 do you read as load-bearing?"
- "For [assumption], does the descriptive artefact at [path] cover
  the same cells the test reports? If not, what's the gap?"
- "Did this descriptive artefact exist before the test ran, or was
  it generated to backstop?"

**Agent-instruction outline** (for `/research-interpret descriptive
HA-XX`):
- Load: pre-reg, result, test.py, cited methodology MDs.
- Extract: assumption list from test.py + pre-reg + methodology cites.
- Walk: per-assumption interview using the seeds above.
- Produce: `descriptive_audit.md` draft.
- Refuse to mark TRUSTED if any assumption is NOT BACKSTOPPED — user
  must explicitly accept REQUIRES-DESCRIPTIVE-WORK to proceed.

---

### 6.2 `verdict_to_inference.md` — Stage I

**Purpose.** A verdict label is not a finding. SUPPORTED does not mean
"the hypothesis is true"; REJECTED does not mean "the hypothesis is
false." Each label maps to a constrained inferential claim — and to a
larger set of claims it does *not* license. This guide pins that
mapping down so interpretation MDs across the corpus are commensurate.

**Inputs.**
- The HA's locked `hypothesis.md` (in particular the operationalisation
  in §4 and the predicted-direction claim in §1/§2).
- The HA's `result.md` (including any §-routing caveats like HA-C4 v2's
  §5.3 INCONCLUSIVE-aware triad logic).
- The Stage D `descriptive_audit.md` — must exist and not be
  REQUIRES-DESCRIPTIVE-WORK.
- [CONVENTIONS §4.1-§4.3](../CONVENTIONS.md) — descriptive-before-
  inference and confirmatory-vs-exploratory framing.
- Literature on N-of-1 inference standards under
  [`literature/methodology/`](../literature/methodology/) (Daza 2018,
  CENT, SCRIBE, Natesan 2023).

**Output.** `analyses/interpretation/HA-XX.md` — one per HA.

**Section outline** for the produced `interpretation.md`:

1. Target HA + verdict (mechanically copied from `result.md`).
2. **What the data shows** (descriptive layer; no claim language).
3. **What the verdict licenses** (operationalisation-bound claim;
   what we can say about the hypothesis given how it was tested).
4. **What the verdict does NOT license** (claims this verdict *does
   not* warrant, especially the easy overclaims).
5. **Caveats narrowing the claim** (drawn from Stage D audit +
   pre-reg's own caveats; not new caveats invented post-hoc).
6. **Lived-experience prior reconciliation** (if user's prior conflicts
   with the verdict, both are recorded; no auto-resolution).
7. **`open_inputs` block** (per §3.5): missing inputs that would
   strengthen or narrow the interpretation — e.g. a sister-HA on a
   competing operationalisation, a descriptive run on a borderline
   cell, a lived-experience walk-through for a divergent era.
8. **Follow-up suggestions** (per §3.11), two tracks:
   - *Own-research* — what HA would replicate this finding, refute it,
     or extend the operationalisation (sister tests with different
     measurement choices, different windows, different era strata).
   - *External-research* — what group-level or comparable-population
     study would test the same hypothesis where our N=1 setup cannot
     (e.g. ME/CFS cohort with the same wearable signal; intervention
     study testing the proposed mechanism). Each external-research
     suggestion explicitly names the N=1 limit that prevents us from
     answering it ourselves.
9. Cross-references to related HAs that will figure in Stage S₁.

**Checklist sketch.**

- [ ] Verdict copied verbatim from `result.md` (no relabelling).
- [ ] Operationalisation language preserved (the claim is about
      *this operationalisation* of the hypothesis, not the hypothesis
      in the abstract — unless replication justifies the broader
      claim).
- [ ] Effect size reported alongside any "supported" claim.
- [ ] For PARTIAL / INCONCLUSIVE verdicts: explicit statement of what
      *would* upgrade them.
- [ ] No new post-hoc framing of the hypothesis (compare to locked
      `hypothesis.md` §1/§2).
- [ ] Confirmatory vs exploratory status from the pre-reg carried
      through.
- [ ] Lived-experience prior, if it conflicts, is logged in §6 without
      resolving the conflict.

**Conflict rules.**
- Verdict vs lived-experience prior: log both, do not resolve in this
  artefact. Resolution is a Stage S₁ activity (more evidence) or stays
  open.
- Verdict vs descriptive audit pending: refuse to draft until audit is
  TRUSTED or user explicitly accepts a PROVISIONAL interpretation
  flagged as such.

**Anti-patterns explicitly forbidden.**
- "REJECTED therefore the underlying hypothesis is false." (The
  operationalisation may be inadequate.)
- "SUPPORTED therefore the proposed mechanism is correct."
  (Correlation in the predicted direction is not mechanism.)
- Reframing the hypothesis to fit the verdict ("what it really meant
  was...").
- Smuggling the lived-experience prior into the §2 / §3 reading
  (it lives in §6 and only §6).
- Conflating PARTIAL with weak SUPPORTED.

**Interview-prompt seeds.**
- "Given [verdict] under [operationalisation], what claim about the
  hypothesis itself does that license? What does it *not* license?"
- "Is there a competing operationalisation that, if also tested and
  REJECTED, would meaningfully narrow what we can say?"
- "How does this verdict sit against what you lived through during
  the relevant era? If there's tension, what is it?"

**Agent-instruction outline.**
- Load: pre-reg, result, Stage D audit, related-HA list.
- Refuse: to start if Stage D audit is missing or
  REQUIRES-DESCRIPTIVE-WORK.
- Walk: section by section with the seeds above. Never silently fill
  §6 — always ask the user.
- Produce: `interpretation.md` draft under reviewer-mode-with-
  authorization (carries `## Authorship` block per CONVENTIONS §1.2).
- Recommend: a `/research-review` in a fresh session before lock.

---

### 6.3 `internal_synthesis.md` — Stage S₁

**Purpose.** Many HAs touch overlapping constructs (e.g. multiple HAs
on overnight recovery, multiple on stress/spike behaviour, multiple
on RHR drift). Treating each as independent loses information; treating
them as a single chorus risks averaging away meaningful conflicts.
This guide governs how a cluster's interpretations combine into a
synthesis call.

**Inputs.**
- The cluster's constituent HA `interpretation.md` files (all must
  exist; Stage I gating enforced).
- The relevant methodology MDs governing the construct(s).
- Any `RESEARCH-REPORT-ADDENDUM` entries that already touch the
  cluster (these become inputs, not arbiters).

**Output.** `analyses/synthesis/cluster-XXX.md` — one per construct
cluster. Cluster names are pre-declared (see §6.3 below); ad-hoc
cluster creation while drafting is forbidden.

**Section outline.**

1. Cluster name + constituent HAs (with verdicts).
2. **Pre-declared constellation**: which HAs were grouped, when, and
   why. (Forbids retroactive grouping that conveniently makes the
   story work.)
3. **Per-HA verdict + interpretation** (one-row summary per HA).
4. **Coherence call**: CONCORDANT / PARTIALLY CONCORDANT / CONFLICT /
   ORTHOGONAL. Definitions in the guide.
5. **What the cluster jointly licenses** (claim narrower or wider than
   any single HA, with rationale).
6. **What the cluster does NOT license** (especially: do not stack
   weak signals into a strong claim).
7. **Open conflicts** preserved with both readings, no resolution.
8. **`open_inputs` block** (per §3.5): missing inputs that would
   resolve a CONFLICT call, tighten a PARTIALLY CONCORDANT call to
   CONCORDANT, or expose whether two HAs in the cluster are
   genuinely independent vs running on the same signal — typically
   tie-breaker HAs, descriptive deep-dives on borderline cells, or
   independence checks across operationalisations.
9. **Follow-up suggestions** (per §3.11), two tracks:
   - *Own-research* — tie-breaker HAs for unresolved CONFLICT calls;
     independence-check HAs to verify multiple operationalisations are
     not running on the same underlying signal; replication HAs as new
     data accrues.
   - *External-research* — group-level cluster studies on the same
     construct in comparable populations; meta-analytic synthesis where
     enough single-case studies exist. Each entry names the N=1 limit
     that prevents us from answering it ourselves.
10. Cross-refs out to Stage S₂ topic(s) this cluster feeds.

**Cluster pre-declaration rule.** A cluster must be pre-declared by
constituent HAs *before* any HA's `interpretation.md` is read for
synthesis. The user signs off on the cluster definition. The skill
records the timestamp. This prevents the post-hoc "let's add HA-X
because it agrees" pattern.

**Checklist sketch.**

- [ ] All HAs in the cluster have current `interpretation.md`.
- [ ] Cluster was pre-declared and signed off before synthesis began.
- [ ] Coherence call is supported by the per-HA rows, not by a
      narrative override.
- [ ] CONFLICT findings are preserved, not resolved.
- [ ] Joint claim is no wider than the narrowest constituent
      claim allows, unless replication-pattern rationale is given.

**Conflict rules.**
- Two HAs in the cluster give opposite-direction findings → CONFLICT,
  both preserved; the joint claim defaults to "the construct shows
  conflicting signal under different operationalisations" and lists
  what would resolve it (a tie-breaker HA, a descriptive deep-dive).
- A single HA in the cluster has a much larger effect than others →
  it does not dominate; coherence is about agreement of direction
  and consistency of effect across operationalisations.

**Anti-patterns explicitly forbidden.**
- Cherry-picking which HAs count for a cluster after seeing
  interpretations.
- "Most HAs agree, therefore the construct is established" without
  attending to operationalisation overlap (three HAs running on the
  same signal are one piece of evidence, not three).
- Splitting the difference between conflicting findings to produce a
  "middle" claim that neither HA supports.

**Interview-prompt seeds.**
- "Which HAs belong in this cluster? What's the shared construct?"
- "Do these HAs share an operationalisation, or are they independent
  tests of the same construct?" (Latter is much stronger evidence.)
- "Where the verdicts diverge, is the divergence informative
  (different operationalisations exposing different aspects) or
  contradictory (same construct, opposite reading)?"

**Agent-instruction outline.**
- Load: cluster definition + all member `interpretation.md` files.
- Refuse: to proceed without pre-declared, signed-off cluster.
- Walk: per-HA row-fill, then coherence call interview, then joint-
  claim narrowing.
- Produce: `cluster-XXX.md` draft under reviewer-mode-with-
  authorization.
- Recommend: fresh-session `/research-review` before lock.

---

### 6.4 `external_contextualisation.md` — Stage S₂

**Purpose.** Place each synthesised cluster against the external
literature for its construct. Three substages: consensus map, comparability
check, positioning. The deliverable is honest about where N-of-1
evidence can and cannot speak to group-level published consensus.

**Inputs.**
- The Stage S₁ `cluster-*.md` for the construct.
- Existing literature artefacts under
  [`literature/`](../literature/) (PDFs + notes).
- N-of-1 reporting and inference standards under
  [`literature/methodology/`](../literature/methodology/) (Daza 2018,
  CENT, SCRIBE, Natesan 2023, WWC handbooks). These govern *how* the
  N-of-1 finding can speak to group-level results, not whether.
- Literature-gap log (per
  [`_pending_literature_fetch.md`](_pending_literature_fetch.md)
  pattern) — when a needed reference is missing, log it for
  fetch-via-`/fetch-paper`.

**Output.** `analyses/contextualisation/topic-XXX.md` — one per
topic. Topics are construct-level (e.g. HRV in LC, overnight recovery
in ME/CFS, stress reactivity in PEM-prone populations), pre-declared
similarly to S₁ clusters.

**Section outline.**

1. Topic name + constituent S₁ clusters.
2. **Consensus map.** For each subclaim in our cluster: does external
   consensus exist? What is it? If competing positions exist, what
   are they and who holds them?
3. **Comparability check.** Is the external population /
   measurement / era close enough to ours that "in line" / "divergent"
   is a coherent claim? Decision: COMPARABLE / PARTIALLY COMPARABLE
   / NOT COMPARABLE. Includes the N-of-1-to-group inference reach
   per Daza 2018 / CENT.
4. **Positioning.** AGREES / EXTENDS / DIVERGES / CANNOT-SAY. Definitions
   in the guide.
5. **Citations** — every external claim has a `literature/`-relative
   path or a literature-gap log entry; no uncited external claim.
6. **Caveats specific to N-of-1 → group comparison.**
7. **Per-topic limitations** — cited from
   [`research_line_limitations.md`](research_line_limitations.md) (per
   §3.9) plus any topic-specific systemic limitations (e.g.
   construct-specific measurement-validity concerns). The topic MD
   does not invent limitations independently; it cites and supplements.
8. **`open_inputs` block** (per §3.5): missing literature references
   (handed off via `/fetch-paper`), missing comparability evidence
   (population/measurement/era detail not present in current refs),
   and any case where positioning was forced to CANNOT-SAY because
   external evidence is insufficient. Each entry names what would
   unlock a tighter positioning call.
9. **Follow-up suggestions** (per §3.11), two tracks:
   - *Own-research* — HAs that would tighten our positioning vs the
     literature (e.g. testing the same construct with the same
     operationalisation an external study used, then comparing).
   - *External-research* — study designs that would settle a divergence
     with consensus (different population, intervention arm,
     instrumentation change); consensus gaps that would benefit from
     group-level work. The existing literature-gap log (§5) feeds this
     track. Each entry names the N=1 limit that prevents us from
     answering it ourselves.
10. Cross-refs out to Stage A if any actionable signal might follow.

**Checklist sketch.**

- [ ] Every external claim cites a specific source.
- [ ] Missing sources are entered in the literature-gap log.
- [ ] Comparability decision is explicit; CANNOT-SAY is a valid and
      preferred outcome over forced positioning.
- [ ] The N-of-1-to-group inference reach is stated using the
      reporting standards in `literature/methodology/`.
- [ ] DIVERGES findings do not auto-claim "our N-of-1 finds the truth";
      both positions are preserved with attribution.

**Conflict rules.**
- We diverge from external consensus → record divergence with
  attribution, no auto-resolution. List candidate explanations
  (different population, different measurement, different era,
  individual variation, methodological difference).
- External consensus does not exist → state that, name the competing
  positions, place our finding among them.
- Comparability fails → CANNOT-SAY; do not force a positioning call.

**Anti-patterns explicitly forbidden.**
- Claiming alignment with external literature based on titles or
  abstracts without reading the relevant section.
- Treating an N-of-1 finding as a refutation of group-level consensus.
- "Cherry-picking" supportive references while ignoring
  non-supportive ones.
- Citing a paper for a claim it does not actually make.

**Interview-prompt seeds.**
- "Is there published consensus on this construct in LC / ME/CFS /
  PEM populations? What is it?"
- "How close is the external population to your situation —
  age/sex/duration/severity? Where does comparability break?"
- "If our finding diverges from external consensus, what's the most
  charitable explanation for both sides?"

**Agent-instruction outline.**
- Load: cluster MD(s), literature/ contents listing, methodology
  references.
- Walk: consensus-map fill, comparability check, positioning call.
- Produce: `topic-XXX.md` draft + any literature-gap log entries.
- Refuse: to lock if any external claim lacks a citation or
  literature-gap entry.

---

### 6.5 `actionability_translation.md` — Stage A (hard predictive gate)

**Purpose.** Translate (or refuse to translate) findings into something
usable for the patient-user's daily life or for prediction. This is
the highest-risk surface in the layer; the hard predictive gate is
intentionally severe.

**Inputs.**
- The Stage S₂ `topic-XXX.md` for the construct in question.
- Lived-experience priors from the user (recorded in the §6 of relevant
  `interpretation.md` files).
- The hard predictive gate (this section's §gate).

**Output.** `analyses/actionability/construct-XXX.md` — one per
construct that warrants an actionability call.

**The three tiers.**

| Tier | Claim shape | Required evidence |
|---|---|---|
| **Monitoring signal** | "[signal X] tracks [construct Y] descriptively." | S₁ CONCORDANT or PARTIAL synthesis + comparability check passed at S₂. |
| **Informative pattern** | "[signal X] historically associated with [pattern Y] under [conditions Z]." | All of monitoring tier + replicated across operationalisations (two-or-more independent HAs in the cluster, not three on the same column). |
| **Predictive use** | "[signal X] forecasts [outcome Y] in advance." | All of informative tier + a **pre-registered forward-validation HA** (predict on unseen days, check after the fact). Retrospective-only fit does NOT qualify. |

**The hard gate, stated explicitly.** A predictive claim requires a
named forward-validation HA in the registry, locked before the
prediction window begins, and a verdict on its result.md. Until that
HA exists and SUPPORTS the predictive claim, the construct is capped
at "informative pattern." This is non-negotiable at the layer level;
guide drafts may not weaken it.

**Section outline.**

1. Target construct + originating S₂ topic.
2. Evidence layer (which tiers' requirements are met / unmet).
3. **Tier claim** + the wording the user may safely use about the
   signal in daily life.
4. **What the user may NOT do with this signal** (the easy overclaims
   to refuse).
5. Forward-validation pathway (if tier 3 wanted but not earned): the
   shape of the HA pre-reg that would unlock it.
6. **`open_inputs` block** (per §3.5): the named forward-validation
   HA(s) required to unlock predictive tier, plus any monitoring- or
   informative-tier shortfall (e.g. comparability gap at S₂ blocking
   even a monitoring-tier claim). Each entry includes the fallback
   tier the artefact has therefore been capped at, so the user sees
   exactly what acquiring the missing input would unlock.
7. **Predictive-quality measures** (per §3.10) — required at tier-2+.
   PPV + base rate are mandatory; NPV, sensitivity, specificity,
   false-alarm rate, lead time, reliability are optional but
   strongly encouraged. Each measure is reported in the plain-language
   "right N out of M / wrong M-N out of M" frame from RESEARCH-REPORT
   §5.2. If PPV-with-base-rate cannot be computed, the tier downgrades
   to monitoring per §3.10 conflict rule; the missing base-rate logs
   in `open_inputs`.
8. **Follow-up suggestions** (per §3.11), two tracks:
   - *Own-research* — the forward-validation HA pre-reg shape from §5
     above is framed here as the own-research follow-up for tier-3
     promotion; also includes own-research pre-regs that would tighten
     the quality measures (e.g. a sensitivity-vs-specificity tradeoff
     test at a different threshold).
   - *External-research* — intervention or RCT studies that could test
     causality (vs the association we can observe); group-level studies
     that could establish a population-level base rate to compare ours
     against. Each entry names the N=1 limit that prevents us from
     answering it ourselves.
9. **Optional: Subject-narrative commentary** (per §3.12). May attach
   to tier-1 or tier-2 formal claim (not tier-3 — those carry
   forward-validation HA and don't need commentary nuance). When
   present, opens with "attached to: K-XXX tier-N claim per §X.Y".
   Every sentence subject-attributed ("I" / "the subject" / "in this
   subject's experience"). Permitted wording: "I notice", "in my
   experience", "in retrospect", "I sometimes", "the pattern hints
   at / suggests-not-confirms / reads as", "worth attention", "I
   lean toward". Forbidden wording: "predicts", "forecasts", "will
   happen", "tomorrow", "X means Y", any causal-claim or forecast-
   claim phrasing. Cannot promote tier; cannot be cited downstream;
   cannot float unattached. If commentary skipped, record-as-skipped
   explicitly.
10. Open downgrades from review (this section gets filled at
    `/research-review` time).

**Checklist sketch.**

- [ ] Tier claim is no higher than the evidence layer permits.
- [ ] Wording does not drift toward advice / prescription.
- [ ] Predictive claim, if made, names the forward-validation HA by
      ID.
- [ ] Easy overclaims are explicitly refused (§4).
- [ ] Connection to gevoelscore-app v1.5+ features (if any) is framed
      as a request, never as an auto-promotion.

**Conflict rules.**
- Tier requirements unmet → tier downgrades. The user cannot override
  the downgrade by asserting confidence; the gate is structural.
- Forward-validation HA REJECTED → predictive claim is removed; the
  construct caps at informative pattern.
- Lived-experience prior says "this signal is reliable for me" without
  forward-validation HA → recorded but does not promote the tier.

**Anti-patterns explicitly forbidden.**
- Promoting a retrospective fit into a predictive claim.
- Framing actionability as advice ("you should...").
- Collapsing presence-conditioned signals (v24-derived) into
  prevalence statements when offering an actionability call.
- Treating a single HA as enough to license a monitoring tier claim.
- Backdoor predictive claims via wording ("watch for X" can be a
  predictive claim in disguise — gate applies).

**Interview-prompt seeds.**
- "What tier are you reaching for, and why?"
- "If this is a predictive claim, where is the forward-validation
  HA? If none exists, would you like to pre-register one?"
- "What is the harm scenario if this actionability claim turns out
  to be wrong in your daily use?"

**Agent-instruction outline.**
- Load: S₂ topic MD, related interpretation/synthesis MDs.
- Refuse: any predictive claim without a forward-validation HA in
  the registry.
- Walk: tier-selection interview, wording-discipline check,
  forbidden-pattern check.
- Produce: `construct-XXX.md` draft, including a forward-validation
  pre-reg shape if tier 3 was wanted but unearned.

---

### 6.6 `translation_to_audience.md` — Stage T

**Purpose.** Translate findings from earlier stages into audience-
targeted artefacts on two tracks: **research-audience** (peer-style
prose for researchers, clinicians familiar with N-of-1 methodology)
and **patient-audience** (laymen, especially PAIS patients, possibly
their non-specialist clinicians). Findings that exist only as
technical MDs do not reach the people they could most help; findings
translated badly mislead. This guide governs both risks.

**Inputs.**
- The source-stage artefact being translated (any of:
  `interpretation.md`, `cluster-*.md`, `topic-*.md`,
  `construct-*.md`).
- [`research_line_limitations.md`](research_line_limitations.md) for
  honest uncertainty wording.
- [`plain_language_dictionary.md`](plain_language_dictionary.md) —
  the live dictionary maintained by this stage; every technical term
  used in the source artefact must have an entry here before the
  patient-audience track is produced.
- The Stage A tier (if the source touches actionability) — drives the
  wording calibration in the patient-audience track.

**Output.** Two files per translated source:
- `analyses/translation/research-audience/<source-name>.md`
- `analyses/translation/patient-audience/<source-name>.md`

Both named after the source artefact (e.g. translating
`interpretation/HA-C4.md` produces
`translation/research-audience/HA-C4.md` and
`translation/patient-audience/HA-C4.md`).

**Section outline** (same for both tracks; content differs by
audience):

1. **Source artefact reference** + the single claim being translated.
2. **Audience definition** — specific subgroup (not "general public").
   Research track: e.g. "LC researcher familiar with wearable data";
   patient track: e.g. "PAIS patient ≥2 years post-onset, comfortable
   reading Dutch lay-press health articles." What prior knowledge is
   assumed; what questions this audience is likely to bring.
3. **Narrative arc** — what was unknown → method used (in this
   audience's vocabulary) → what's now known → what remains uncertain
   → what to do with it (or "nothing yet, here's why").
4. **Plain-language body** — jargon expanded; one-line definitions
   inline or footnoted; every term not in the audience's expected
   vocabulary is either defined or replaced.
5. **Visual summary** — one image. Either references an existing plot
   from `analyses/.../figures/` or specifies a to-be-produced plot
   (axes, what it shows, what the reader should see in it). Patient-
   audience track: image is mandatory and primary; prose supplements.
   Research-audience track: image strongly preferred but optional if
   the claim is fundamentally non-visual.
6. **Honest uncertainty statement** — calibrated to the audience.
   Research track: uses the source artefact's verdict/tier language
   directly. Patient track: rephrases in everyday Dutch (or English
   per audience), citing limitations from
   `research_line_limitations.md` in plain terms. **Hard rule**: the
   patient-track uncertainty statement never reads more confident
   than the source artefact's verdict/tier.
7. **Patient-relevance test** (patient-audience track only) — explicit
   answers to: (a) what question is a PAIS patient likely to ask
   after reading this? (b) could this language be used by a patient
   in a clinic conversation tomorrow? If either answer is "no" or
   "unclear," revise the draft.
8. **`open_inputs` block** (per §3.5): missing inputs — typically a
   needed visual not yet produced, a plain-language term not yet
   dictionary-defined, a layperson-tester not yet recruited.
9. **Predictive-quality measure translation** (required when source
   artefact is actionability tier-2+, per §3.10):
   - *Research-audience track*: keep the technical measure names (PPV,
     base rate, lead time) alongside the plain-language gloss.
   - *Patient-audience track*: plain-language frame only — "when this
     fires, it's right N out of M times, in a context where N
     happens M times a year." No bare percentages without their
     base-rate context. The RESEARCH-REPORT §5.2 wording
     ("wrong 24 times out of 25") is the model.
10. **Follow-up communication** (per §3.11):
    - *Research-audience track*: the own-research and external-
      research follow-up tracks from the source artefact, rendered in
      technical language for a researcher reader.
    - *Patient-audience track*: "what is still unknown" framed plainly;
      what the patient could observe themselves (own-research analogue
      at patient scale); what they could ask a clinician about
      (external-research analogue). Avoids both false hope ("research
      will soon answer this") and counsel-of-despair ("nothing more is
      known") — honest framing of the open questions.
11. **Optional: Subject-narrative commentary translation** (per §3.12,
    patient-audience track ONLY — commentary is forbidden in research-
    audience track per the §3.12 locked decision):
    - When the source `construct-*.md` has a §3.12 commentary section,
      the patient-audience track renders it in plain Dutch (or audience-
      appropriate language). Subject-attribution stays in the rendering
      ("ik merk op dat..." / "in mijn ervaring..."); permitted /
      forbidden language discipline carries through the translation.
    - **Layperson-test gate**: if the layperson reads the commentary
      as a soft prediction or as advice, the commentary is revised
      before lock — the layperson's interpretation is the binding test,
      not the drafter's intent. This is the §3.12 implementability
      check.
    - When the source has no commentary or has skip-recorded it, the
      translation simply omits this section.

**Checklist sketch.**

- [ ] Audience explicitly defined; not "general."
- [ ] Plain-language dictionary updated with every technical term
      used in the source artefact (the dictionary entry is the
      pre-requisite for the patient-track translation of that term).
- [ ] Visual summary present (patient track) or specified (research
      track).
- [ ] Honest uncertainty matches the source artefact's tier; no
      upgrading; no inappropriate softening either.
- [ ] Patient-relevance test passed (patient track).
- [ ] Source artefact's claim is not exceeded; nor reduced past
      meaningfulness.
- [ ] Both tracks produced, OR an explicit skip-research-internal
      record exists.

**Conflict rules.**
- Translation would require a stronger claim than the source allows
  → refuse the translation; log to `open_inputs`. The remedy is more
  evidence (re-run, new HA, forward-validation), not stronger wording.
- Source artefact has CANNOT-SAY positioning → patient track must say
  "we cannot tell you whether..." not "evidence is mixed" or other
  softening that implies more than CANNOT-SAY warrants.
- Source artefact and earlier-translated terms in the dictionary
  conflict on meaning → the source artefact wins; the dictionary is
  updated to match and prior translations re-examined (per §3.7
  drift policy).
- Layperson-test fails → patient track is revised before lock; the
  fail-reason is recorded in `open_inputs` so the next translation
  benefits.

**Anti-patterns explicitly forbidden.**
- **Tier upgrading in wording** — using predictive-sounding language
  for a monitoring-tier finding ("watch for X" can be predictive in
  disguise; "X has historically appeared alongside Y" is the
  monitoring-tier phrasing). The Stage A backdoor-predictive-claims
  anti-pattern propagates here.
- **Faux-balanced wording** ("evidence is mixed", "more research is
  needed") used to soften an honest call. If the source artefact made
  a clear call, the translation states the call clearly; if the
  source said CANNOT-SAY, the translation says CANNOT-SAY.
- **Stripping uncertainty for "accessibility"** — laymen handle
  uncertainty when it is framed honestly; removing it patronises and
  misleads.
- **Treating the plain-language dictionary as optional** — undefined
  jargon in patient-audience track is a failure mode, not a stylistic
  choice.
- **Producing only the research-audience track** — "the patient
  version can come later" is how the patient track never gets written.
  Both tracks are produced or the skip is explicit.
- **Patronising tone** toward the patient audience — laymen are not
  children; PAIS patients in particular have often spent years
  reading their own medical literature.
- **Quoting the source artefact's prose unchanged** as the
  "translation." Translation is rewriting for the audience, not
  excerpting.

**Interview-prompt seeds.**
- "Who specifically is this for? What do they already know? What will
  they ask after reading the first paragraph?"
- "What is the single most important sentence this audience needs to
  take away? If they remember only one thing, what is it?"
- "What is the most honest way to say what we do not yet know — in
  this audience's everyday vocabulary?"
- "Could a PAIS patient use this language in a clinic conversation
  tomorrow without sounding either overconfident or apologetic?"
- "Which technical term from the source artefact does this audience
  not have? What is the plain-language replacement?"

**Agent-instruction outline.**
- Load: source artefact, `research_line_limitations.md`,
  `plain_language_dictionary.md`.
- Refuse: to start if source artefact is not locked.
- Refuse: to lock patient-track output if any technical term used is
  not in the dictionary.
- Walk: audience-definition interview → narrative-arc draft →
  plain-language body draft → visual specification → uncertainty
  calibration → patient-relevance interview (patient track only).
- Produce: both audience tracks (or record skip explicitly); append
  new terms to `plain_language_dictionary.md`.
- Recommend: fresh-session `/research-review` before lock; for
  patient-audience track, also recommend a real-layperson test (hand
  the draft to someone outside the project; observe what they ask).

---

## 7. The skill — `/research-interpret`

**Invocation shape.**

```
/research-interpret <stage> <target>
```

Where `<stage>` is one of `descriptive | interpret | synthesise |
contextualise | actionability | translate` and `<target>` is the HA ID,
cluster name, topic name, construct name, or source-artefact path as
appropriate to the stage.

Examples:
- `/research-interpret descriptive HA-C4`
- `/research-interpret interpret HA-C4`
- `/research-interpret synthesise cluster-stress-load`
- `/research-interpret contextualise topic-hrv-in-lc`
- `/research-interpret actionability construct-overnight-recovery`
- `/research-interpret translate interpretation/HA-C4`
- `/research-interpret translate construct-overnight-recovery`

**Skill responsibilities.**

1. **Stage-routing.** Choose the right guide MD based on `<stage>`;
   load it as data. The guide is the source of truth; the skill is
   the engine.
2. **Dependency check.** Refuse to start if the upstream stage's
   artefact is missing or in REQUIRES-* state for the target.
3. **Interview execution.** Walk the guide's procedure section by
   section. Use the guide's interview-prompt seeds verbatim; never
   silently fill a judgment-call field.
4. **Artefact production.** Produce the output MD at the named path,
   with `## Authorship` block, reviewer-mode-with-authorization
   marking, and not-locked status.
5. **Refusal discipline.** If any of the guide's checklist items
   would have to be ticked false, the skill refuses to mark the
   artefact ready for lock and lists the open items.
6. **Missing-inputs queue maintenance.** Per §3.5, every stage
   produces an `open_inputs` block. The skill appends those entries
   to `methodology/_open_inputs.md`, deduplicates against existing
   entries, and at every invocation surfaces the current queue
   length so the user can decide whether to attack the backlog before
   moving forward. Entries name the missing input, what it blocks,
   the cheapest acquisition path, and the fallback claim available
   without it.
7. **Review handoff.** On completion, remind the user that a fresh-
   session `/research-review` is the next discipline gate.

**Skill instruction MD** (at `.claude/skills/research-interpret/SKILL.md`)
needs:

- A header pointing to this plan + the six guides + the two supporting
  MDs (`synthesis_structure_map.md`, `research_line_limitations.md`)
  + the live `plain_language_dictionary.md`.
- A stage-routing table mapping `<stage>` arg → guide MD path → output
  folder (six rows, one per stage).
- Per-stage refusal preconditions (one block per stage), including
  Stage T's "source artefact must be locked" and "every technical
  term used must be in the dictionary before patient track locks."
- The interview-engine pattern: load guide, parse section outline,
  iterate sections, ask seeds, fill, gate on checklist.
- A `## Anti-patterns the skill must refuse` block consolidating the
  forbidden patterns from all six guides.
- Drift-check helper: a flag (`--drift-check`) that, instead of running
  a stage, walks all locked artefacts and surfaces those whose §3.7
  re-examination triggers have fired since last check.
- A pointer to the fresh-session-review discipline.

**What the skill must NOT do.**
- Pick an interpretation when the guide names it a judgment call.
- Promote a tier in Stage A by force of argument.
- Edit the guide MDs in-session (those are producer-mode and change
  via their own lock process).

## 7.5 Candidate skills to lift later (with triggers)

This layer keeps the skill surface deliberately lean: one
`/research-interpret` engine driven by guide MDs as data, plus the
existing `/research-review` and `/fetch-paper`. The candidates below
have been considered and **not** built. Each has a stated trigger
condition. If the trigger fires, lift the skill; until then, doing the
work manually is preferred because the manual pass tells us what the
skill should contain. Premature skill-building drifts more than its
absence costs.

| Candidate skill | What it would do | Trigger to lift | Covered today by |
|---|---|---|---|
| `/research-stocktake-descriptive` | Walk all HAs and produce a coverage matrix (assumption × backstop-status × cell). | Triggered when a new methodology MD or new HA family forces a re-stocktake more than twice. One-off scripts handle the first two passes. | Manual stocktake (todo #5 in §11). |
| `/research-open-inputs` | View, prioritise, route entries in `_open_inputs.md` (sort by what unblocks most downstream work, group by acquisition path). | Queue grows past where reading and eyeballing remains reliable — practically, once entries cross ~20 and the user starts mis-routing. | `Read` + manual filtering of `_open_inputs.md`. |
| `/research-forward-validation-template` | Generate the skeleton pre-reg for a forward-validation HA, given a Stage A construct and its evidence layer. | Triggered on the **second** time a forward-validation HA is drafted by hand. The first draft is the spec for what the template should contain. | Manual pre-reg drafting via existing `hypothesis_lock_process.md` discipline. |
| `/research-literature-search` | Topic-driven literature search → candidate paper list → handoff to `/fetch-paper`. | Triggered when Stage S₂ contextualisation becomes a regular activity (multiple topics per month) rather than per-construct ad-hoc. | WebSearch + WebFetch + `/fetch-paper`. |
| Stage-A-specific skill (`/research-actionability-gate`) | A dedicated interview engine for Stage A that hard-codes the tier-gating mechanics (vs the generic engine loading the guide as data). | Triggered if the generic `/research-interpret` engine demonstrably fails to enforce the hard predictive gate on a Stage A draft, AND the failure is traceable to engine-vs-guide separation rather than a guide-content bug. Update the guide first; lift to a dedicated skill only if the failure recurs after the guide fix. | `/research-interpret actionability <target>` loading `actionability_translation.md`. |
| `/research-translate-visual` | Generate a one-image visual summary from a Stage T translation artefact's visual specification (axes, layered annotations, finding-band overlays on timelines). | Triggered when ≥5 translation artefacts request the same visual shape (e.g. timeline-with-finding-band) and the user has produced them manually. The fifth manual run is the spec for the skill. | Manual plot generation via existing `analyses/.../figures/` scripts. |
| `/research-layperson-test` | Structured layperson-test runner — present the patient-audience track to a non-project person, record observed questions, surface revision triggers. | Triggered when patient-audience translation becomes regular (≥monthly) and informal testing starts to drift. | Manual: hand the draft to a real person, observe, revise. |

**Revisit cadence.** This table is checked at every implementation
order step in §11 — when starting any guide draft or building the
skill, the drafter re-reads this section and asks whether any trigger
has fired since the previous step. If so, lift the candidate before
proceeding. If not, proceed and note the no-op in the session.

**Adding new candidates.** If a future session identifies another
candidate skill that should *not* be built today, append a row here
with the same shape (what it would do / trigger to lift / covered
today by). Documenting the candidate is the way the project remembers
to revisit; an undocumented candidate is one we will rediscover from
scratch later and waste a session re-deciding.

**Retiring a candidate.** When a candidate is lifted (becomes a real
skill) or judged permanently unnecessary, move its row to a "Retired
candidates" subsection below this table with a one-line note on
which outcome and the date.

## 8. Cross-cutting constraints

These apply to every guide; the skill enforces them at every stage.

- **Descriptive-before-inference** per CONVENTIONS §2.1.
- **No interpretive marks in raw descriptive layer** per CONVENTIONS §4.1.
- **Caveats vs a-priori** per CONVENTIONS §4.2 — caveat what we did
  not do, do not claim what we did not earn.
- **Prior-driven hypotheses are confirmatory** per CONVENTIONS §4.3
  — when a finding traces to a pre-existing user prior, the
  hypothesis is confirmatory and its evidence reach is constrained
  accordingly.
- **Presence-conditioned semantics** for any v24-derived signal per
  [`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md).
- **Era integrity** per
  [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)
  — Stratum 4 is primary; M1/M2/M3 sub-segmentation requires warrant.
- **N-of-1 inference reach** bounded by Daza 2018 + CENT + SCRIBE +
  Natesan 2023 standards under
  [`literature/methodology/`](../literature/methodology/).
- **Fresh-session peer review** for every reviewer-mode-with-
  authorization artefact per CONVENTIONS §1.2.

## 9. Layer-level anti-patterns

Independent of any single guide:

- **The verdict-as-finding fallacy** (skipping Stage I).
- **The synthesis-as-counting fallacy** (treating "3 of 5 HAs
  supported" as stronger than "1 of 5 well-operationalised HAs
  supported with descriptive backstopping").
- **The literature-confirmation fallacy** (citing an external paper
  for our positioning without reading whether the paper actually
  supports our claim direction).
- **The actionability-by-narration fallacy** (writing wording that
  reads predictive while claiming only "informative pattern" status).
- **The retroactive constellation fallacy** (declaring a cluster's
  membership only after seeing which HAs agree).
- **The skill-as-judge fallacy** (letting the interview engine pick
  the answer when the guide names a judgment call).
- **The silent-narrowing fallacy** (degrading a claim's wording to
  fit available inputs without producing an `open_inputs` entry that
  names what is missing and what claim it is blocking). Per §3.5,
  every degradation is logged so the missing-input pathway stays
  productive rather than disappearing into hedged prose.
- **The bare-percentage actionability fallacy** (reporting a tier-2+
  claim with a percentage but no base-rate context). "PPV is 60%"
  with no denominator is meaningless. "PPV is 60% at a 5% base rate,
  so when it fires it's right 3 in 5 times but it only fires about
  once a month" is informative. Per §3.10, base-rate framing is
  required, not optional.
- **The unscoped-follow-up fallacy** (proposing an external-research
  follow-up without naming which N=1 limit prevents us from answering
  it ourselves). "Someone should run an RCT" without "we cannot
  because we have one subject and no comparator arm" is hand-waving
  dressed as research suggestion. Per §3.11, honest scoping is what
  distinguishes a follow-up suggestion from a wishlist.
- **The bare-narrative-as-actionability fallacy** (using §3.12
  subject-narrative commentary wording to escape the §3.10 hard
  predictive gate). Variant: "we couldn't claim prediction, but the
  subject's narrative shows the signal is predictive in lived
  experience..." — this routes a backdoor predictive claim through
  commentary language and is exactly the slippage §3.12 is designed
  to prevent. Per §3.12 hard separations: commentary cannot promote
  actionability tier; only a pre-registered forward-validation HA
  per §3.10 unlocks tier-3.
- **The commentary-promotion fallacy** (letting accumulated
  commentary across multiple lock cycles justify tier promotion
  without forward-validation HA). "We've seen this pattern hold up
  across three commentary rounds; that's evidence" — no, that's
  retrospective consistency of the subject's own narrative, which is
  what L4 (analyst-is-subject) and §3.10 (hard predictive gate) both
  caution against treating as analytical evidence. Tier promotion
  requires forward-validation, not narrative durability.
- **The downstream-citation-of-commentary fallacy** (citing §3.12
  commentary content in HA result.md / interpretation.md /
  cluster-*.md / topic-*.md / research-audience translation as if it
  were analytical input or finding). Commentary is patient-facing
  nuance, not research evidence; citing it downstream blurs the
  epistemic categories §3.12 keeps separate.

## 10. Open questions deferred to guide-drafting time

These are intentionally not resolved here. They will be resolved
when each guide is drafted, by user decision at that time.

1. **Cluster naming convention.** Construct keyword vs HA-ID-anchored
   vs free-form. Resolve when drafting `internal_synthesis.md`.
2. **Topic-vs-cluster boundary.** Some constructs may collapse a
   1:1 cluster→topic, others fan out. Resolve when drafting
   `external_contextualisation.md`.
3. **Forward-validation HA pre-reg shape.** What sections, what
   prediction-window mechanics, what locks-when. Resolve when drafting
   `actionability_translation.md`.
4. **Skill behavior on legacy HAs.** Some HAs predate this layer's
   conventions. Does the skill accept them as-is, or does it require
   a brought-up-to-spec pre-reg? Resolve when building the skill.
5. **Audit-before-push integration.** Should `audit_for_publication.py`
   be extended to gate on Stage A actionability claims (e.g. refuse
   to push if a predictive tier claim lacks a registered forward-
   validation HA)? Resolve when building the skill.
6. **Plain-language base language.** Dutch (the user's daily-life
   language for clinic conversations) or English (the project's
   default written-research language)? May depend on per-construct
   audience choice. Resolve when drafting `translation_to_audience.md`.
7. **Layperson-test recruitment.** Who plays the layperson in the
   patient-relevance test? A specific PAIS-patient peer, a non-PAIS
   layperson, both? Resolve when drafting `translation_to_audience.md`.
8. **Drift-check cadence.** Six months is the §3.7 default; whether
   that's the right cadence for *this* corpus' velocity needs revisit
   after the first cadence cycle.
9. **Synthesis-structure-map seed.** Does the map seed itself from
   the existing RESEARCH-REPORT-ADDENDUM groupings, or start empty
   and grow as drafting reveals natural clusters? Resolve when
   authoring `synthesis_structure_map.md`.

## 11. Implementation order

Once this plan is reviewed and locked, the order of work is the
12 steps below. Each guide draft and each supporting-MD draft (which
together are methodology MDs) is its own session, followed by a
fresh-session **`/research-methodology-review`** against
[CONVENTIONS](../CONVENTIONS.md). The reviewer-mode-with-authorization
artefacts those guides produce (interpretation, synthesis,
contextualisation, actionability, translation outputs) get
`/research-review` instead — see §4 producer/reviewer split for the
mapping. The candidate-skills table in §7.5 is re-checked before each
step in case any trigger has fired.

1. **Review the plan in a fresh session.** Fresh-session reviewer
   reads the plan + CONVENTIONS + existing methodology MDs cold;
   produces a review report under `docs/research/reviews/` named
   `methodology-_plan_results_analysis_layer-YYYY-MM-DD.md`.

2. **Address review, lock the plan.** User accepts revisions or as-is.
   Plan moves from DRAFT to LOCKED.

3. **Stocktake descriptive coverage** (descriptive-before-inference
   per CONVENTIONS §2.1; the stocktake must precede any
   inference-shaping decision including the synthesis-structure
   map). Walk existing `analyses/descriptive/` artefacts and compare
   to what the 30+ HAs' `test.py` files actually lean on. Output:
   a gap list of descriptive backstops that don't yet exist. This
   sizes Stage D's downstream backlog AND informs which HAs have
   trustworthy verdicts to even consider clustering in step 5.

4. **Author the research-line limitations doc** —
   `methodology/research_line_limitations.md` (per §3.9). Producer-mode
   drafting under interview. Initial coverage per §3.9. Fresh-session
   `/research-methodology-review` before lock.

5. **Pre-register the synthesis-structure map** —
   `methodology/synthesis_structure_map.md` (per §3.6). Producer-mode
   drafting under interview, informed by the step-3 stocktake (HAs
   without descriptive backstopping are flagged in the map; clusters
   are not built on un-backstopped HAs). Initial scope: seed from
   existing RESEARCH-REPORT-ADDENDUM groupings (or start empty —
   open question §10.9). Fresh-session `/research-methodology-review`
   before lock.

6. **Draft the six guides, one per session.** In order:
   - 6.1 `descriptive_precondition_audit.md` (guide #1)
   - 6.2 `verdict_to_inference.md` (guide #2)
   - 6.3 `internal_synthesis.md` (guide #3)
   - 6.4 `external_contextualisation.md` (guide #4)
   - 6.5 `actionability_translation.md` (guide #5)
   - 6.6 `translation_to_audience.md` (guide #6)

   Each guide-drafting session ends with the §10 open questions
   relevant to that guide being resolved by user decision.

7. **Build `/research-interpret` skill** with six-stage routing per
   §7. Includes the `--drift-check` helper.

8. **Dry-run end-to-end stages D → A on one HA.** Likely target:
   HA-C4 (freshly verdicted, well-documented, isolated enough that
   single-HA cluster is reasonable for the initial pass).
   - 8a. **Pick the dry-run target.** Criteria: well-documented
     pre-reg + result; recent verdict; HA either single-HA-cluster
     or with at most one obvious sister-HA.
   - 8b. **Define dry-run success criteria up front** (before any
     stage runs): each stage produces an artefact that meets its
     checklist OR generates a coherent `open_inputs` ledger; user can
     read back the resulting finding in plain words; no stage
     silently failed.
   - 8c. **Run stages D → I → S₁ → S₂ → A on the target,** in order.
   - 8d. **If a plan or guide bug surfaces:** stop, revise the
     affected artefact (with re-lock if it's a guide), then resume.
     A dry-run that exposes bugs is a successful dry-run, not a
     failed one.

9. **Translation dry-run.** Take the dry-run's outputs and produce
   both audience tracks via Stage T.
   - 9a. **Pick which source-stage artefact(s) to translate.** Likely
     the interpretation MD (always present) and the actionability MD
     if Stage A produced a tier-X-or-above claim.
   - 9b. **Run stage T on the chosen source(s).**
   - 9c. **Layperson test the patient-audience track.** Hand the
     draft to a real layperson; observe questions; record in
     `open_inputs`.
   - 9d. **Revise `translation_to_audience.md` if the layperson test
     exposes a guide gap.**

10. **Decide rollout order across the corpus** — locked in writing,
    not improvised during rollout.
    - 10a. **Sort criteria options** (user decides which to apply
      and how to weight): by-cluster (synthesis-coherence first),
      by-recency (freshness first), by-tractability (build momentum),
      by-topic-priority (where does the user most want answers).
    - 10b. **Lock the rollout order** with a one-line rationale per
      cluster.
    - 10c. **Deviations from the locked order require explicit user
      decision** in-session, not drift.

11. **Roll out across the corpus, cluster by cluster.** Per
    locked-order cluster:
    - 11a. Stage D on every member HA.
    - 11b. Stage I on every member HA.
    - 11c. Stage S₁ on the cluster.
    - 11d. Stage S₂ on the relevant topic(s).
    - 11e. Stage A on the relevant construct(s) — only if S₂ supports
      it.
    - 11f. Stage T on every tier-X-or-above output — both audience
      tracks.

12. **Periodic drift check** — ongoing, no end state. At the §3.7
    cadence (default six months) or on methodology-MD update, run
    `/research-interpret --drift-check`, surface re-examination
    triggers fired since last check, produce CONFIRMED-NO-CHANGE
    entries or revise artefacts. The layer is never "done"; step 12
    is its steady state.

## 12. Authorship

- **Drafted by**: Claude (this session), at user authorization, on
  2026-06-23.
- **Authorising user**: Willem.
- **Mode**: producer-mode (r3 reclassification per r2 review finding;
  prior r1/r2 carried reviewer-mode-with-authorization).
- **Status**: r5 **LOCKED 2026-06-24** by user acceptance. r4 was
  LOCKED 2026-06-23; r5 absorbed a user-requested mid-implementation
  refinement to the §3.10 hard predictive gate tradeoff (the hard
  gate stays; §3.12 opens a bounded patient-facing nuance space
  alongside it). No second-pass review per user pattern (scope of
  r3 / r4 / r5 absorption is named below). Implementation proceeds
  to §11 step 6.
- **On lock**: the six guides in §6 + the two supporting MDs in §3.6
  and §3.9 become drafting tasks per the §11 implementation order.
  This plan is preserved as historical scaffold; it can be moved to
  `_archive/` once all six guides + two supporting MDs + the skill
  are landed and reviewed.
- **Revision history**:
  - 2026-06-23 r1: initial draft (5 guides + 1 skill).
  - 2026-06-23 r2: absorbed seven additions before audit per user
    direction — added guide #6 (`translation_to_audience.md`); added
    §3.6 synthesis-structure pre-registration; added §3.7 drift &
    replication policy; added §3.8 stopping & completion criteria;
    added §3.9 research-line limitations binding; expanded §11
    implementation order from 8 steps to 12 with dry-run + rollout
    sub-steps; added supporting MDs `synthesis_structure_map.md`,
    `research_line_limitations.md`, `plain_language_dictionary.md`;
    expanded §10 deferred questions; added §7.5 translation-related
    candidate skills.
  - 2026-06-23 r3: absorbed three required actions from the r2
    fresh-session `/research-methodology-review` (report at
    [`reviews/methodology-_plan_results_analysis_layer-2026-06-23.md`](../reviews/methodology-_plan_results_analysis_layer-2026-06-23.md))
    plus the recommended producer-mode reclassification. R1:
    swapped §11 step 3 (synthesis-structure map) with step 5
    (descriptive stocktake), so stocktake informs the map per
    CONVENTIONS §2.1 descriptive-before-inference. R2: added
    conflict-resolution rule in §3.6 between layer-wide map and
    §6.3 per-cluster pre-declaration — when S₁ work reveals the
    map needs changing, halt S₁, route the change to a separate
    producer-mode map-revision session with its own
    `/research-methodology-review` pass, then resume. R3: renamed
    `/research-review` to `/research-methodology-review` in §3.6,
    §4 (guide / map / limitations rows), §11 intro and steps 3-5
    — for methodology MDs only; reviewer-mode-with-authorization
    artefacts (interpretation, synthesis, contextualisation,
    actionability, translation outputs) keep `/research-review`
    per §4. Recommended-but-deferred from r2 review (per user
    decision): four missing anti-patterns (stocktake-as-pilot,
    cluster-correlation-vs-causation, translation-selection,
    exclusion-by-omission), negative-finding translation
    discipline in §6.6, drift-check ownership in §3.7, cross-HA
    multiplicity correction at the layer level. These can be
    addressed in a future revision if friction surfaces during
    implementation.
  - 2026-06-23 r4: scope expansion before lock per user request — the
    user noted that "no predictive claim without forward-validation"
    (the r1+ hard gate) needed a companion mechanism for
    communicating *how* predictive or actionable a finding actually is,
    citing the project's existing PPV-with-base-rate precedent in
    RESEARCH-REPORT §5.2; also noted that follow-up research
    suggestions belong in scope. Added §3.10 predictive-quality
    measures layer rule (required PPV + base rate + plain-language
    frame at actionability tier-2+; optional NPV / sensitivity /
    specificity / false-alarm-rate / lead-time / reliability;
    classifier-discrimination measures remain forbidden at the
    HA-test level per `personal_hypotheses.md` §32). Added §3.11
    follow-up-research-suggestions layer rule (every reviewer-mode-
    with-authorization artefact closes with own-research +
    external-research tracks; external-research must explicitly name
    the N=1 limit preventing self-answer; distinct from
    `open_inputs`). Added follow-up-suggestions section to §6.2
    interpretation, §6.3 synthesis, §6.4 contextualisation, §6.5
    actionability, §6.6 translation outlines. Added quality-measures
    section to §6.5 actionability outline. Added quality-measure-
    translation + follow-up-communication sections to §6.6
    translation outline. Added six new completion criteria to §3.8
    stopping-criteria table (follow-up section filled across five
    artefact types; quality measures reported at actionability
    tier-2+; quality-measure translation in patient track).
    Added two layer-level anti-patterns to §9: bare-percentage
    actionability fallacy; unscoped-follow-up fallacy.
  - 2026-06-24 r5: mid-implementation refinement per user request
    during step 5 lock. User identified tradeoff #4 (the §3.10 hard
    predictive gate) as the one she wanted to revise — accepting the
    hard gate for formal claims while opening "reading tea leaves"
    nuance space after it. Added §3.12 subject-narrative commentary
    layer (sibling to §3.10 and §3.11). Design choices locked in
    interview: (a) layer-level rule §3.12 not buried in §6.5
    actionability guide; (b) commentary permitted at tier-1 AND
    tier-2 attached (not just tier-2); (c) patient-audience track
    only (forbidden in research-audience translation). Hard
    separations preserved: commentary cannot promote actionability
    tier, cannot be cited as downstream evidence, cannot float
    unattached, cannot use predictive/causal language. Updated §0
    purpose list item 5; updated §3.8 stopping criteria (actionability
    + translation rows); updated §6.5 actionability outline (new
    section 9 — optional commentary); updated §6.6 translation
    outline (new section 11 — patient-audience-only commentary
    translation with layperson-test gate); added three §9 anti-
    patterns (bare-narrative-as-actionability; commentary-promotion;
    downstream-citation-of-commentary). Map K-stress-fatigue-monitoring
    and K-bout-recovery-signal cells will gain commentary-eligible
    notes in separate map-revision (r2 → r3).
