---
name: research-interpret
description: Interview-engine skill operationalising the six LOCKED methodology guides (descriptive_precondition_audit, verdict_to_inference, internal_synthesis, external_contextualisation, actionability_translation, translation_to_audience) across stages D / I / S1 / S2 / A / T. Loads the relevant guide MD as data and walks the user through that stage's procedure. Use when drafting any results-analysis-layer artefact under `docs/research/analyses/{descriptive,interpretation,synthesis,contextualisation,actionability,translation}/`. Refuses on dependency-gate failures; never edits guide MDs in-session.
metadata:
  author: gevoelscore-app
  version: "0.1.0"
---

# /research-interpret -- results-analysis layer skill

**Status**: **LOCKED r4** by user acceptance 2026-06-25. r3 was
LOCKED 2026-06-25 absorbing five step-8 dry-run friction items; r4
absorbs five additional friction items from the §11 step 9
translation dry-run (per dispatch report 2026-06-25): codified
`DRAFT-ON-DRAFT-DRY-RUN` as fourth dispatch-mode placeholder
enabling Stage T to operate on DRAFT-r1 source artefacts in dry-run
mode (otherwise guide #6 §9.2 refusal-path #1 would halt all dry-
runs at the first stage past bootstrap); added four Stage T
operational clarifications (§5.11 ABSENT marker convention;
"Commentary not applicable" two-semantics distinction; dictionary-
update routing rule restricting appends to patient-audience track
first-draft only; visual cross-source sharing pattern between Stage
A construct + parent Stage S₂ topic). r2 was LOCKED 2026-06-25
(absorbed bootstrap ordering + Stage T skip-record location); r3
absorbed five friction items from the §11 step 8 dry-run
on C-stress-fatigue-shape (per dispatch report 2026-06-25):
codified three dispatch-mode placeholders (`DEFAULTED-PENDING-USER-
INPUT`, `SKIPPED-AS-DRY-RUN-DEFAULT`, `DEFAULTED-TO-PRESERVE-PENDING-
USER-INPUT`); added Stage S₁ coherence-call ambiguity clarification
(default-to-CONFLICT applies at disagreement boundary, NOT
agreement-label distinction); added Stage S₂ proxy-citation pattern
allowing literature-brief artefact reliance in dry-run mode; added
always-read-LOCKED-current-revision rule preventing inheritance of
cached interpretations of prior revisions. r1 authored 2026-06-25
per §11 step 7 of
[`../../../docs/research/methodology/_plan_results_analysis_layer.md`](../../../docs/research/methodology/_plan_results_analysis_layer.md)
(r5 LOCKED). r1 → r2 absorbed a fresh-session
`/research-methodology-review` (verdict REVISION RECOMMENDED (mild),
report at [`../../../docs/research/reviews/methodology-research-interpret-skill-2026-06-25.md`](../../../docs/research/reviews/methodology-research-interpret-skill-2026-06-25.md))
that confirmed: (a) skill-doesn't-weaken-guide check PASSED across
five spot-checked cross-references; (b) frontmatter discoverability
confirmed via system-reminder; (c) step-8 dry-run readiness YES.
Two required actions absorbed (R1: bootstrap ordering rule names
responsibility #6 `_open_inputs.md` scaffold FIRST when both files
absent at first invocation; R2: Stage T skip-research-internal
record location named at source artefact's §10 cross-references
section). Operationalises the six LOCKED methodology guides
(`descriptive_precondition_audit.md`, `verdict_to_inference.md`,
`internal_synthesis.md`, `external_contextualisation.md`,
`actionability_translation.md`, `translation_to_audience.md`).
**Layer ready for §11 step 8 (dry-run on HA-C4 stages D→A).**

This skill is an **engine, not a re-statement**. The six guides are
the source of truth for *what each stage's artefact must contain and
must refuse*; the skill's job is to *load the relevant guide as data,
walk its §8 interview seeds verbatim with the user, gate on the
guide's §9.6 refuse-to-lock checks, and produce the artefact at the
path the guide names*. Every rule belongs to a guide; this skill
points to it and enforces it. If a discrepancy ever appears between
this skill and a guide, the guide wins.

The skill spans six stages -- **D**escriptive precondition audit, verdict
to **I**nference, **S**₁ internal synthesis, **S**₂ external
contextualisation, **A**ctionability translation, and **T**ranslation to
audience -- per the locked-plan §3 stage map. Each invocation routes
to exactly one guide; the guides do not chain inside a single
invocation. Cross-stage dependency rules (per locked-plan §3) are
enforced as preconditions, not as auto-cascades.

## Invocation

```
/research-interpret <stage> <target>
```

Where `<stage>` is one of:

| Stage arg | Stage symbol | What it does |
|---|---|---|
| `descriptive` | D | Loads guide #1; produces a Stage D `descriptive_audit.md`. |
| `interpret` | I | Loads guide #2; produces a Stage I `interpretation.md`. |
| `synthesise` | S₁ | Loads guide #3; produces a Stage S₁ `cluster-*.md`. |
| `contextualise` | S₂ | Loads guide #4; produces a Stage S₂ `topic-*.md`. |
| `actionability` | A | Loads guide #5; produces a Stage A `construct-*.md`. |
| `translate` | T | Loads guide #6; produces both audience-track translation files. |

`<target>` semantics by stage (per locked-plan §3 + each guide's §3
output spec):

- `descriptive HA-XX` -- the HA ID (e.g. `HA-C4c`).
- `interpret HA-XX` -- the HA ID; same as Stage D.
- `synthesise cluster-XXX` -- the cluster name per the map's §3
  cluster-ID column (e.g. `C-bout-substance`); skill normalises the
  output filename to `cluster-XXX.md`.
- `contextualise topic-XXX` -- the topic name per the map's §4 topic-ID
  column.
- `actionability construct-XXX` -- the construct name per the map's §5
  construct-ID column.
- `translate <source-path>` -- the locked source artefact's path,
  relative to `docs/research/` (e.g. `analyses/interpretation/HA-C4c.md`
  or `analyses/actionability/construct-overnight-recovery.md`); the
  source's stage is inferred from the path.

Examples:

```
/research-interpret descriptive HA-C4c
/research-interpret interpret HA-C4c
/research-interpret synthesise C-bout-substance
/research-interpret contextualise topic-hrv-in-lc
/research-interpret actionability construct-overnight-recovery
/research-interpret translate analyses/interpretation/HA-C4c.md
```

**Helper invocation**:

```
/research-interpret --drift-check
```

Walks all locked artefacts in `analyses/{descriptive,interpretation,
synthesis,contextualisation,actionability,translation}/`, reads each
lock log's "Drift triggers registered" line, and surfaces those whose
§3.7 re-examination triggers have fired since the last walk.
Implementation per "§3.7 cadence helper" below.

## Six-stage routing table

| `<stage>` | Guide MD (binding source of truth) | Output path | Refusal preconditions (refuse-to-start) |
|---|---|---|---|
| `descriptive` | [`descriptive_precondition_audit.md`](../../../docs/research/methodology/descriptive_precondition_audit.md) | `docs/research/analyses/descriptive/HA-XX/descriptive_audit.md` (+ `plots/` subfolder) | Per guide #1 §9.1 -- `hypothesis.md`, `result.md`, `test.py` must all exist for the HA. |
| `interpret` | [`verdict_to_inference.md`](../../../docs/research/methodology/verdict_to_inference.md) | `docs/research/analyses/interpretation/HA-XX.md` | Per guide #2 §9.1 + §9.2 -- the HA's `descriptive_audit.md` must exist and must read **TRUSTED** (proceed), **DOWNGRADED-INCONCLUSIVE-PROVISIONAL** with explicit user acceptance (proceed-with-PROVISIONAL-flag), or block: REQUIRES-DESCRIPTIVE-WORK halts; STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED halts and routes to pre-reg revision per guide #1 §6.2. |
| `synthesise` | [`internal_synthesis.md`](../../../docs/research/methodology/internal_synthesis.md) | `docs/research/analyses/synthesis/cluster-XXX.md` | Per guide #3 §9.1 + §9.2 -- every cluster-member HA's `interpretation.md` must exist and be LOCKED; the cluster must appear in the map's §3 cluster table; cascade-arrow upstream `cluster-*.md` (where the map's §3 row declares a cascade precondition, e.g. C-bout-framework → C-bout-substance) must exist and be LOCKED. |
| `contextualise` | [`external_contextualisation.md`](../../../docs/research/methodology/external_contextualisation.md) | `docs/research/analyses/contextualisation/topic-XXX.md` | Per guide #4 §9.1 + §9.2 -- every constituent `cluster-*.md` must be LOCKED; the topic must appear in the map's §4 topic table; [`research_line_limitations.md`](../../../docs/research/methodology/research_line_limitations.md) must exist (per locked-plan §3.9). |
| `actionability` | [`actionability_translation.md`](../../../docs/research/methodology/actionability_translation.md) | `docs/research/analyses/actionability/construct-XXX.md` | Per guide #5 §9.1 + §9.2 -- every feeding `topic-*.md` must be LOCKED; the construct must appear in the map's §5 construct table; the tier aspiration in the map must permit the tier being claimed; **for tier-3 (predictive) reach**, a pre-registered forward-validation HA must exist in the registry with lock-date **before** the prediction-window start (locked-plan §3.10 hard predictive gate). |
| `translate` | [`translation_to_audience.md`](../../../docs/research/methodology/translation_to_audience.md) | Both: `docs/research/analyses/translation/research-audience/<source-name>.md` AND `docs/research/analyses/translation/patient-audience/<source-name>.md` (research-audience track may be skipped only via **explicit skip-research-internal record at the source artefact's §10 cross-references section** — per guide #6 §3 + source-guide convention: Stage A construct artefacts use §10 cross-refs per guide #5 §5.12; Stage S₂ topic artefacts use §4.10 per guide #4; Stage S₁ cluster artefacts use §4.10 per guide #3; Stage I interpretation artefacts use §4.10 per guide #2 — the skip-record syntax is one line `Stage T research-audience track: SKIPPED-AS-RESEARCH-INTERNAL — rationale: <one-sentence>` appended at the source's cross-refs section; commentary section per §3.12 is **patient-audience track only**) | Per guide #6 §9.1 + §9.2 -- source artefact at `<source-path>` must be LOCKED; `research_line_limitations.md` must exist; `plain_language_dictionary.md` must exist OR be scaffolded under the bootstrap responsibility (see §"Skill responsibilities" #7). |

For every stage the skill ALSO refuses if the upstream-stage dependency
chain has any unlocked artefact -- the chain is transitive (Stage T on
a Stage A source requires the Stage S₂ → Stage S₁ → Stage I → Stage D
upstream chain locked for the relevant HAs).

## Skill responsibilities

Per locked-plan §7 + the per-guide §9 agent-instruction outlines:

1. **Stage-routing.** Parse `<stage>` and load the corresponding guide
   MD from the routing table above. The guide is the source of truth;
   the skill is the engine. Never duplicate guide content; cite it.

2. **Dependency check.** Refuse to start if any upstream artefact in
   the routing table's "Refusal preconditions" column is missing or in
   the wrong state. On refusal: produce only the relevant `open_inputs`
   entries (per the failing guide's §4.9 / §5.6 / §5.7 refusal-path
   spec) and append them to `_open_inputs.md` (responsibility #6).
   Never silently soft-fail through to drafting.

3. **Interview execution.** Walk the guide's §8 interview seeds in
   the order the guide names (§8.1 → §8.2 → … ). Use the seed wording
   verbatim. For every judgment-call field the guide names (see the
   per-guide §9.4 "skill MUST NOT autonomously fill" lists), present
   the seed and record the user's articulation; never silently pick
   the answer. The guide's §9.3 extract phase pre-populates verbatim
   carry-forward fields (verdict labels, L-ID blocks from upstream
   artefacts, map row cells) so the user's interview time goes to
   judgment, not retyping.

4. **Artefact production.** Produce the output MD at the path named
   in the routing table, following the guide's §4 / §5 section
   outline. Status header records DRAFT r1 + the mode (reviewer-mode-
   with-authorization for I / S₁ / S₂ / A / T; producer-mode for D).
   Reviewer-mode-with-authorization artefacts carry the `## Authorship`
   block per CONVENTIONS §1.2.

5. **Refusal discipline.** At "user-accepts-as-ready-for-completion"
   time, walk the guide's §9.6 refuse-to-lock gate item-by-item. If
   any check would have to be ticked false, the skill refuses to mark
   the artefact ready for lock and lists the unmet items (with the
   guide-§-number that owns each check). The user may not override a
   §9.6 fire by force of argument; the remedy is to fix the
   underlying gap (more data, sharper wording, missing citation,
   missing L-ID, etc.) or to log the gap to `open_inputs` and accept
   a lower-tier / narrower / PROVISIONAL artefact.

6. **Missing-inputs queue maintenance** (per locked-plan §3.5). Every
   guide's output MD carries an `open_inputs` block (named §4.5 /
   §4.9 / §5.6 / §5.7 depending on the guide). On every invocation:
   - Read the existing `docs/research/methodology/_open_inputs.md`
     queue (scaffold it on first ever invocation if missing -- minimal
     header + empty table).
   - Surface the current queue length so the user can decide whether
     to attack the backlog before drafting moves forward.
   - On lock-event: append the artefact's new `open_inputs` entries
     to the queue, deduplicated against existing entries by
     (missing-input × blocked-target) key.
   - Each entry carries: missing-input description, blocked-stage /
     target / claim, cheapest acquisition path, fallback claim
     available without it -- per locked-plan §3.5 four-field shape.

7. **Bootstrap `plain_language_dictionary.md`** on first Stage T
   invocation when not present (per guide #6 §9.1 bootstrap
   responsibility). The skill writes a minimal header (status: live
   artefact, producer-mode, maintained by `/research-interpret
   translate` invocations) and an empty body table (one row per term:
   Dutch + English + source-scope note + date). Subsequent Stage T
   invocations load-and-append. The dictionary persists across
   sessions per normal producer-mode discipline; the bootstrap is a
   one-time skill responsibility per guide #6 §9.1.

   **Bootstrap ordering**: when both `_open_inputs.md` (responsibility
   #6) and `plain_language_dictionary.md` (responsibility #7) are
   absent at first invocation, **`_open_inputs.md` is scaffolded
   FIRST** (responsibility #6 precedes responsibility #7). Rationale:
   `_open_inputs.md` is referenced by every guide's §9 / §5 / §11; the
   dictionary is referenced only by Stage T. If the dictionary
   bootstrap somehow fired before the queue (e.g., a Stage T first-
   invocation that wrote an `open_inputs` entry as part of its draft
   refusal-path), the queue write would error on a missing file. The
   ordering rule fires only on first-ever invocation when both files
   are absent; once either is on disk, no ordering concern arises.

8. **Review handoff.** On user-accepted-as-ready-for-completion, the
   skill reminds the user that the next discipline gate is a
   fresh-session peer review:
   - **For Stage D** (`descriptive_audit.md`): producer-mode artefact,
     no fresh-session review required per locked-plan §4 row (audits
     are not verdicts); user explicit acceptance is the lock event.
   - **For Stages I / S₁ / S₂ / A / T** (reviewer-mode-with-
     authorization artefacts): fresh-session `/research-review`
     required (NOT `/research-methodology-review` -- see locked-plan
     §11 intro: methodology MDs use `/research-methodology-review`;
     reviewer-mode-with-authorization outputs use `/research-review`).
   - For Stage T patient-audience track: additional layperson-test
     gate per guide #6 §9.7 + locked-plan §4 row.
   The fresh-session review must run in a different conversation (no
   shared context with this drafting session) per CONVENTIONS §1.2.

9. **`--drift-check` helper** (per locked-plan §3.7 cadence walk).
   Implementation:
   - Walk all locked artefacts under
     `docs/research/analyses/{descriptive,interpretation,synthesis,
     contextualisation,actionability,translation}/`.
   - For each artefact, read the lock log's "Drift triggers
     registered" line (per the manual-pending-skill carry-forward in
     responsibility #10) to identify the registered re-examination
     triggers (per each guide's §9.8 trigger list).
   - For each registered trigger, check whether it has fired since
     the artefact's last lock or last CONFIRMED-NO-CHANGE entry:
     underlying-result-rerun checks `git log` on the cited
     `result.md`; methodology-MD-version-change checks lock-log
     versions on the cited methodology MDs; new-HA-joins-cluster
     checks the map's §3 row for cluster-member additions; ≥6-month
     cadence checks the lock-log date against today; literature-
     reference-lands checks `_pending_literature_fetch.md`; etc.
   - Surface the list of triggered artefacts to the user, sorted by
     downstream-blast-radius (Stage T artefacts last, Stage D
     artefacts first -- a fired D trigger cascades upward).
   - The user decides which to actually re-examine; the skill does
     NOT auto-re-examine. A re-examination produces either a
     CONFIRMED-NO-CHANGE lock-log entry (no artefact rewrite) or a
     REVISED artefact under the normal drafting + fresh-session-
     review cycle (per locked-plan §3.7).

10. **Drift-trigger registration manual-pending-skill carry-forward.**
    Until this skill lands, every guide's §9.8 acceptance step is
    maintained by hand: the artefact's lock log carries a "Drift
    triggers registered" line naming the trigger conditions (4 or 5
    depending on guide). Once the skill is in use, the skill walks
    those lock-log lines on `--drift-check`. The carry-forward
    pattern lets the skill bootstrap onto pre-existing locked
    artefacts without retrofitting them.

11. **Limitations-doc downstream-citation-count maintenance**
    (per [`research_line_limitations.md`](../../../docs/research/methodology/research_line_limitations.md)
    §8 manual-pending-skill pattern). On lock of any artefact whose
    output includes an L-ID citation block (Stage I §4.5; Stage S₁
    §4.5; Stage S₂ §4.7; Stage A §5.11; Stage T §5.5), the skill
    increments the limitations doc's §8 downstream-citation-count
    table for each cited L-ID. Manual carry-forward until the skill
    lands, per the limitations doc's §8 status note.

## Dispatch-mode placeholders (added r3)

For the three §9.4 "skill MUST NOT autonomously fill" interactions
where the dispatcher genuinely cannot articulate the field — e.g.
when the skill is dispatched headless in a dry-run agent that has no
user to interview — the skill codifies **three first-class
placeholders** with the §3.5 four-field `open_inputs` shape pre-
specified. Use these instead of inventing per-session placeholder
shapes:

- **`DEFAULTED-PENDING-USER-INPUT`** — Stage I §4.6 lived-experience
  prior reconciliation when the dispatcher cannot articulate the
  subject's prior. The artefact's §4.6 paragraph carries the
  placeholder with a one-sentence default-reading (e.g. "the user's
  prior on `<construct>` is recorded as `DEFAULTED-PENDING-USER-INPUT`
  pending interview confirmation"), and a corresponding `open_inputs`
  entry: missing = "user articulation of lived-experience prior on
  this HA's construct"; blocks = "§4.6 reconciliation completeness +
  any downstream Stage S₁ joint-claim that depends on it"; cheapest
  path = "interview seed §8.3 at next `/research-interpret interpret
  HA-XX` invocation"; fallback = "interpretation drafted with §4.6
  DEFAULTED-PENDING-USER-INPUT carried forward."

- **`SKIPPED-AS-DRY-RUN-DEFAULT`** — Stage A §5.9 subject-narrative
  commentary when the dispatcher cannot author commentary because
  §3.12's subject-attribution-every-sentence rule + L4 explicitly
  forbid the dispatcher from writing it. The §5.9 section carries
  the placeholder with a one-sentence skip-rationale, and an
  `open_inputs` entry: missing = "user-authored §3.12 subject-
  narrative commentary on this construct's tier-1/2 claim";
  blocks = "Stage T patient-audience-track §5.11 commentary
  translation when this construct's Stage A locks"; cheapest path =
  "user fills §5.9 directly OR records explicit SKIPPED-WITH-USER-
  RATIONALE at next `/research-interpret actionability` invocation";
  fallback = "construct locked at tier with §5.9 section marked
  SKIPPED-AS-DRY-RUN-DEFAULT; Stage T renders no commentary."

- **`DEFAULTED-TO-PRESERVE-PENDING-USER-INPUT`** — Stage S₁ §4.4
  coherence-call when the dispatcher is choosing between two
  agreement-band labels (CONCORDANT vs PARTIALLY CONCORDANT) and the
  per-guide §4.4 default-to-CONFLICT rule does NOT apply (see the
  coherence-call ambiguity clarification below). The artefact's §4.4
  carries the placeholder with the defaulted label + one-sentence
  rationale, and an `open_inputs` entry: missing = "user judgment
  call between `<label-A>` and `<label-B>`"; blocks = "Stage S₂
  positioning if it depends on the joint-claim shape"; cheapest path
  = "interview seed §8.2 at next `/research-interpret synthesise
  cluster-XXX` invocation"; fallback = "synthesis drafted at
  defaulted label with explicit DEFAULTED-TO-PRESERVE-PENDING-USER-
  INPUT marker."

These placeholders are valid lock-states; an artefact lock with any
of them is **legitimate-but-incomplete** — the artefact is LOCKED in
its structural shell, but the §3.5 `open_inputs` queue carries the
pending-user-input as an acquisition-path entry for the next live
interview session.

## Coherence-call ambiguity clarification (Stage S₁; added r3)

Per dry-run friction observed 2026-06-25 on C-stress-fatigue-shape:
guide #3 §4.4 names a default-to-CONFLICT rule for ambiguous
coherence calls, but the rule applies to **disagreement-boundary
ambiguity** (PARTIALLY CONCORDANT vs CONFLICT), NOT to
**agreement-label ambiguity** (CONCORDANT vs PARTIALLY CONCORDANT).
The two distinct cases:

- **Agreement-label ambiguity** (CONCORDANT vs PARTIALLY CONCORDANT)
  — both labels assert agreement on the construct; the question is
  whether the agreement is uniform (CONCORDANT) or carries
  substantive disagreement on effect-size / qualifier (PARTIALLY
  CONCORDANT). **Default: PARTIALLY CONCORDANT** (default-to-
  preserve discipline — the disagreement, if any, stays visible in
  §4.6 open-conflicts rather than being washed into a CONCORDANT
  claim).
- **Disagreement-boundary ambiguity** (PARTIALLY CONCORDANT vs
  CONFLICT) — the question is whether the cluster's HAs point the
  same direction (PARTIALLY CONCORDANT) or opposite directions
  (CONFLICT). **Default: CONFLICT** per guide #3 §4.4 (default-to-
  preserve discipline at the disagreement boundary).

The skill distinguishes the two ambiguity types when interview seed
§8.2 fires; the `DEFAULTED-TO-PRESERVE-PENDING-USER-INPUT`
placeholder above carries the per-ambiguity-type default.

## Stage S₂ proxy-citation pattern in dry-run (added r3)

Per dry-run friction observed 2026-06-25: Stage S₂ §7.1 anti-pattern
(alignment-by-title-or-abstract without reading the relevant section)
sits in tension with dispatched-headless dry-runs where the
dispatcher cannot re-read literature PDFs in-session at production
cost. The skill's resolution:

- **Production-mode Stage S₂**: full PDF re-read for every cited
  claim. §7.1 enforced absolutely.
- **Dry-run-mode Stage S₂**: the skill MAY rely on **existing
  in-corpus literature-brief artefacts** (e.g.
  [`literature/pais-pem-literature-review.md`](../../../docs/research/literature/pais-pem-literature-review.md);
  [`literature/pacing-and-crash-mitigation.md`](../../../docs/research/literature/pacing-and-crash-mitigation.md);
  HA pre-reg register-verification logs that quote external sources
  with section anchors) as proxy citations for the consensus-map and
  comparability checks, when the literature brief was itself
  produced by a prior PDF read. The dry-run artefact MUST mark
  affected §4.3 + §5 cites as **`PROXY-CITED-IN-DRY-RUN`** with the
  literature-brief path; an `open_inputs` entry records the "full
  PDF re-read pending for production-lock" follow-up. Production-
  lock cannot fire until the proxy cites resolve to direct cites OR
  the user explicitly accepts the proxy-cite as production-grade.

This is a dry-run-mode-only allowance; production-mode locks revert
to §7.1's full-read requirement.

## DRAFT-on-DRAFT dry-run discipline (added r4)

Per dry-run friction observed 2026-06-25 on step 9 translation
dry-run: source artefacts in a dry-run chain are typically DRAFT-r1
(not LOCKED), yet guide #6 §9.2 refusal-path #1 fires on "source
missing OR not locked." Without a dispatch-mode placeholder for
this, dry-runs would halt at the first stage past the bootstrap.

**`DRAFT-ON-DRAFT-DRY-RUN`** — fourth dispatch-mode placeholder
(joining the three named in §"Dispatch-mode placeholders" above).
When the skill is dispatched in dry-run mode and the source artefact
is DRAFT (not LOCKED), the skill MAY proceed if the dispatch carries
explicit dry-run authorization (typically a §11 step 8 / step 9
dispatch reference). The downstream artefact MUST mark its source
citation as `DRAFT-ON-DRAFT-DRY-RUN` and carry an `open_inputs`
entry: missing = "LOCKED revision of source artefact `<path>`";
blocks = "production-grade use of this downstream artefact";
cheapest path = "user interview to lock the source artefact at next
`/research-interpret <source-stage> <source-target>` invocation";
fallback = "downstream artefact remains DRAFT-r1; production-lock
deferred until source locks."

Production-mode dispatches (i.e., the normal user-driven invocation
chain) revert to guide #6 §9.2 refusal-path #1's hard rule: source
MUST be LOCKED. The `DRAFT-ON-DRAFT-DRY-RUN` placeholder is a
dry-run-mode-only allowance.

## Stage T operational clarifications (added r4)

Four smaller Stage-T-specific clarifications from the step 9
translation dry-run (2026-06-25). These supplement guide #6 LOCKED
r2 without revising it; guide #6 r3 absorption may codify them at
the guide level in a future revision pass:

1. **§5.11 ABSENT marker convention** — research-audience track may
   carry a one-line `[§5.11 ABSENT per §3.12 patient-audience-only
   hard separation]` marker header for audit-trail traceability;
   guide #6 §9.6 item #12 lock-gate fires only against §5.11-
   with-commentary-content, not against the marker line.
2. **"Commentary not applicable" two-semantics distinction** —
   patient-audience track §5.11 carries one of two distinct
   wordings depending on source state: (a) "Commentary section
   not applicable: source §5.9 SKIPPED-AS-DRY-RUN-DEFAULT or
   SKIPPED-WITH-USER-RATIONALE" (Stage A source case); (b)
   "Commentary section not applicable: source stage (Stage I /
   S₁ / S₂) does not carry §3.12 commentary by structural rule"
   (non-Stage-A source case). The two wordings preserve the
   semantic difference for downstream readers.
3. **Dictionary-update routing rule** — `plain_language_dictionary.md`
   append fires on **patient-audience track-file first-draft only**;
   research-audience track-file drafts do NOT trigger dictionary
   appends (research-audience preserves methodology vocabulary by
   design). The bootstrap (responsibility #7) still scaffolds on
   first Stage T invocation regardless of track order.
4. **Visual cross-source sharing** — when a Stage A construct
   translation derives from a single Stage S₂ topic translation,
   the §5.8 visual specifications MAY reference a shared underlying
   plot path; both §5.8 sections cite the same plot file with one-
   line shared-spec note ("§5.8 visual specification shared with
   `<sister-artefact-path>` §5.8"). Each translation artefact
   remains standalone-readable; the sharing is at the underlying-
   asset level only.

## Always-read-LOCKED-current-revision rule (added r3)

Per dry-run friction observed 2026-06-25: a future dispatcher who
reads a guide at a now-superseded revision (e.g. guide #3 r1's pre-
correction §5.2 worked example) could land a mis-reading the
LOCKED-current-revision specifically corrected. **The skill MUST
always load the LOCKED-current-revision** of each guide on every
invocation, verified by reading the guide's status header line for
the `**LOCKED r<N>**` marker. If a guide's status header shows
NOT LOCKED or DRAFT-only state, the skill HALTS that stage's
invocation and produces an `open_inputs` entry: missing = "LOCKED
revision of guide #X"; blocks = "Stage `<X>` invocations"; cheapest
path = "complete the guide's locked-revision absorption + user
acceptance"; fallback = "stage blocked entirely."

Cached interpretations of prior revisions are **never** inherited;
each invocation's interpretation derives only from the LOCKED-
current-revision text. This rule supplements the
`always-load-the-cited-section` discipline at §3.6 + §3.12
boundaries above.

## Anti-patterns the skill must refuse

The skill enforces three categories of anti-patterns: (a) per-guide
anti-patterns -- the skill refuses on the §9.6 fire-list of the loaded
guide, which is each guide's machine-checkable mapping of its §7
anti-patterns; (b) layer-level anti-patterns -- the locked plan §9
list, which spans all stages; (c) skill-specific anti-patterns -- the
three named in locked-plan §7 "What the skill must NOT do" plus
operational addenda from the per-guide §9.4 "skill MUST NOT
autonomously fill" lists.

**Per-guide anti-pattern refusal** -- see the §7 section of each guide
(skill refuses on the §9.6 mapped checks):

- Stage D: [`descriptive_precondition_audit.md` §7](../../../docs/research/methodology/descriptive_precondition_audit.md#7-anti-patterns-explicitly-forbidden)
  (assumption-passing-by-test-existence; cell-mismatched plot;
  post-hoc-generated backstop; the four added §7.4-§7.7 patterns).
- Stage I: [`verdict_to_inference.md` §7](../../../docs/research/methodology/verdict_to_inference.md)
  (REJECTED-as-falsified; SUPPORTED-as-mechanism; verdict reframing;
  prior-smuggling; PARTIAL-as-weak-SUPPORTED).
- Stage S₁: [`internal_synthesis.md` §7](../../../docs/research/methodology/internal_synthesis.md)
  (post-hoc cluster membership; weak-signal stacking; difference-
  splitting; cross-cluster smuggling; sister-cluster evidence
  promotion; seed-notes-as-constraints; post-hoc caveat invention;
  label invention; §3.12 commentary in S₁; predictive-quality
  measures in S₁).
- Stage S₂: [`external_contextualisation.md` §7](../../../docs/research/methodology/external_contextualisation.md)
  (title-citation; N-of-1-as-refutation; cherry-picked supportive
  refs; misquoted-source claim; the §5 mapping forbiddens).
- Stage A: [`actionability_translation.md` §7](../../../docs/research/methodology/actionability_translation.md)
  (retrospective-as-predictive; advice-form wording; presence-
  conditioned-as-prevalence; single-HA-as-monitoring; backdoor-
  predictive wording; bare-percentage; §7.7 commentary-wording-
  forbidden; §7.8 commentary-promotes-tier; §7.9 commentary-floats-
  unattached; §7.14 tier-3-commentary; the rest of §7).
- Stage T: [`translation_to_audience.md` §7](../../../docs/research/methodology/translation_to_audience.md)
  (tier-upgrading-in-wording; faux-balanced softening; uncertainty-
  stripping-for-accessibility; dictionary-as-optional; only-research-
  audience-without-skip; patronising tone; verbatim quoting as
  translation; the 23-item §9.6 list).

**Layer-level anti-pattern refusal** -- see
[`_plan_results_analysis_layer.md` §9](../../../docs/research/methodology/_plan_results_analysis_layer.md#9-layer-level-anti-patterns)
(verdict-as-finding; synthesis-as-counting; literature-confirmation;
actionability-by-narration; retroactive-constellation; skill-as-
judge; silent-narrowing; bare-percentage-actionability; unscoped-
follow-up; bare-narrative-as-actionability; commentary-promotion;
downstream-citation-of-commentary).

**Skill-specific anti-patterns** (per locked-plan §7 "What the skill
must NOT do" + operational addenda):

- **Pick an interpretation when the guide names it a judgment call.**
  Every per-guide §9.4 contains a "skill MUST NOT autonomously fill"
  list (§4.6 lived-experience prior in Stage I; §4.4 coherence call
  in Stage S₁; §4.5 positioning + §4.3 consensus existence in Stage
  S₂; §5.2 tier earned + §5.5 forward-validation shape + §5.9
  commentary in Stage A; §5.3 plain-language replacements + §5.7
  layperson-test pool + §5.11 commentary rendering in Stage T). The
  skill surfaces the §8 seed, records the user's articulation, and
  cross-checks against §5 mapping rules + §7 anti-patterns -- but
  the user picks the answer.
- **Promote a tier in Stage A by force of argument.** The hard
  predictive gate (locked-plan §3.10) is structural, not rhetorical.
  Tier-3 requires a registered forward-validation HA whose lock-date
  precedes the prediction-window start, full stop. No amount of
  user assertion (or guide-author intuition) unlocks it. See the
  Stage A row of the routing table and guide #5 §9.6.
- **Edit the guide MDs in-session.** Guides are producer-mode
  methodology MDs and change only via their own lock process (a
  separate drafting session + fresh-session `/research-methodology-
  review` + user acceptance). If the skill discovers a guide gap or
  conflict during execution, it halts, surfaces the gap to the user,
  and routes the fix to a separate session per the §6 conflict-rule
  pattern below. NEVER edit a guide MD inline.
- **Backdoor a §3.12 commentary into a higher tier or a
  research-audience track.** Per locked-plan §3.12 hard separations:
  commentary cannot promote actionability tier, cannot be cited
  downstream as analytical evidence, cannot float unattached, and
  is FORBIDDEN in research-audience track. Stage A §5.9 + Stage T
  §5.11 are the only legal commentary venues, and Stage T commentary
  is patient-audience track ONLY.
- **Skip the missing-inputs `open_inputs` entry when narrowing a
  claim** (silent-narrowing fallacy per locked-plan §9). Every
  degradation of a claim must produce an `open_inputs` entry naming
  what is missing and what claim it is blocking. Hedged wording
  without an accompanying `open_inputs` entry is forbidden.
- **Cross the producer / reviewer split.** Per CONVENTIONS §1.2,
  Stage I / S₁ / S₂ / A / T artefacts are reviewer-mode-with-
  authorization; their fresh-session review must run in a different
  conversation. The skill's review-handoff reminder (responsibility
  #8) is not optional.

## Interview-engine pattern

Once the routing table dispatches a stage and the dependency check
passes, the skill enters a six-phase loop driven by the loaded guide's
§9 agent-instruction outline. The phases are guide-uniform; only the
content the guide loads / extracts / interviews differs.

**Phase 1 -- Load** (per guide §9.1).
The skill loads the inputs the guide names: the upstream-stage
artefact(s), the map row for the target, the limitations doc's §5
citation row, the relevant methodology MDs, the literature methodology
anchors (Daza 2018 / CENT 2015 / SCRIBE 2016 / Natesan 2023; WWC 2022
for Stage S₂ +), and the guide-specific extras (PPV-with-base-rate
precedent for Stage A; plain-language dictionary for Stage T). If any
load fails (file missing at cited path), the skill defaults to the
guide's fail-safe (Stage D's §9.1 fail-safe is the canonical
example -- NOT BACKSTOPPED + `open_inputs` entry rather than silent
soft-fail).

**Phase 2 -- Gate** (per guide §9.2).
The skill checks the upstream-status chain per the routing table's
refusal-preconditions column. On gate-fail: halt; produce only the
`open_inputs` entry per the failing refusal-path; surface the gap to
the user; offer to invoke the upstream stage (e.g. "Stage D missing
on HA-C4c -- run `/research-interpret descriptive HA-C4c` first?")
or to log to queue and stop. On gate-pass: proceed to Phase 3.

**Phase 3 -- Extract** (per guide §9.3).
The skill mechanically pulls verbatim carry-forward fields from
upstream artefacts: verdicts from `result.md`, licensed-claim
sentences from §3 of `interpretation.md`, coherence calls from §4.4
of `cluster-*.md`, L-IDs from the map's per-row L-IDs column, tier
aspirations from the map's §5 row, source-claim sentences from the
named §-anchor of the source artefact for Stage T. Extract drift
checks (per guide §9.2 / §9.3 specifics) surface prose-vs-code
mismatches, citation-vs-source mismatches, or map-vs-artefact
mismatches as explicit input to the §8.1 interview seed.

**Phase 4 -- Interview** (per guide §9.4).
The skill walks the guide's §8 seeds in order, verbatim. For each
seed:
- Present the seed wording exactly as the guide states it.
- Receive the user's articulation.
- Cross-check the articulation against the guide's §5 mapping rules
  and §7 anti-pattern list.
- If a mismatch fires, surface it and seek the operationalisation-
  bound or anti-pattern-cleared rephrasing.
- Never silently fill a §9.4 "skill MUST NOT autonomously fill"
  field. The user picks; the skill records.

**Phase 5 -- Produce** (per guide §9.5).
The skill drafts the output MD at the path the routing table names,
following the guide's §4 / §5 section outline section by section.
All sections are filled or have an `open_inputs` entry naming what
is missing. The status header records DRAFT r1, the producer-mode /
reviewer-mode-with-authorization mode, and the `## Authorship` block
per CONVENTIONS §1.2 (reviewer-mode-with-authorization artefacts
only -- Stage D's producer-mode audit does not require the block).

**Phase 6 -- Refuse-to-lock gate** (per guide §9.6).
The skill walks the guide's §9.6 fire-list item-by-item. For each
fire, the skill names the unmet check with the guide-§-number, the
specific section / wording / citation that fired it, and the remedy
(more data, sharper wording, missing L-ID, etc.). If all checks
pass, the skill marks the artefact "ready for completion" and
proceeds to user-acceptance + Phase 7. Otherwise: report fires to
user; halt; offer to revise per the user's choice. The skill never
auto-locks; the user's explicit acceptance is the binding completion
event per locked-plan §3.8.

**Phase 7 -- Acceptance + handoff** (per guide §9.7 + §9.8).
On user explicit acceptance:
- Status header transitions DRAFT → LOCKED with a lock-log entry.
- `open_inputs` entries propagate to `_open_inputs.md` (skill
  responsibility #6).
- Drift triggers register in the lock log per the guide's §9.8
  trigger list (responsibility #10 -- manual-pending-skill carry-
  forward).
- Limitations-doc §8 downstream-citation-count increments for each
  cited L-ID (responsibility #11).
- Plain-language dictionary updates apply for Stage T (responsibility
  #7).
- The skill reminds the user of the review-handoff per the routing
  table + responsibility #8 (Stage D no review; Stages I / S₁ / S₂ /
  A / T fresh-session `/research-review`; Stage T patient-audience
  track also layperson-test).

## §3.6 map-conflict-resolution handling

Per locked-plan §3.6, if in-stage discovery during a `synthesise` /
`contextualise` / `actionability` invocation reveals that the
[`synthesis_structure_map.md`](../../../docs/research/methodology/synthesis_structure_map.md)
needs to change (an HA belongs in a different cluster; a new cluster
should exist; a topic boundary is wrong; a construct's tier aspiration
needs revising), the skill **halts the in-stage session immediately**
and routes per locked-plan §3.6 conflict-resolution rule:

1. Halt; do NOT edit the map in-session.
2. Record the proposed map change in `_open_inputs.md` with the
   target cluster / topic / construct named and the trigger
   described, per locked-plan §3.6 step 2.
3. Tell the user the in-stage session resumes only AFTER a separate
   producer-mode session updates the map and runs its own
   `/research-methodology-review` pass before re-lock.

The map is authoritative for cluster / topic / construct membership
and rollups; per-cluster §6.3 pre-declaration in guide #3 cannot add
or remove constituents without first triggering this pathway.

## §3.12 commentary discipline (cross-cutting)

Subject-narrative commentary per locked-plan §3.12 is a bounded
patient-facing nuance space. The skill enforces three propagation
points:

- **Stage A `construct-*.md` §5.9** -- optional commentary section,
  may attach to tier-1 or tier-2 formal claims only (NOT tier-3 --
  those carry the forward-validation HA per §3.10). Subject-attributed
  every sentence; permitted vs forbidden wording per guide #5 §5.9;
  cannot promote tier; cannot float unattached. Skipped-with-rationale
  is a valid completion state.
- **Stage T patient-audience track §5.11** -- when the source
  `construct-*.md` has a §5.9 commentary, the patient-audience track
  renders it in plain Dutch (or audience-appropriate language).
  Subject-attribution stays; permitted-wording discipline carries
  through; **layperson-test gate** (per guide #6 §5.7) is the binding
  test -- if the layperson reads commentary as a soft prediction or
  advice, the commentary is revised before lock per §3.12
  implementability check.
- **Stage T research-audience track** -- §5.11 commentary FORBIDDEN.
  Per locked-plan §3.12 hard separation, commentary lives only in
  patient-audience. Skill refuses to lock research-audience track
  with a §5.11 section present (guide #6 §9.6 item #12).

Commentary is never cited downstream as analytical evidence (no Stage
I / S₁ / S₂ / A interpretation or research-audience translation may
cite it). Commentary cannot promote a Stage A tier (guide #5 §6.4
conflict rule + §7.8 anti-pattern; locked-plan §9 commentary-
promotion fallacy). Tier promotion requires forward-validation per
§3.10, full stop.

## L-ID citation discipline (per
[`research_line_limitations.md`](../../../docs/research/methodology/research_line_limitations.md) §5)

Each stage's output carries the L-ID citation block at the depth the
limitations doc's §5 table specifies. The skill enforces this at the
§9.6 refuse-to-lock gate:

| Stage | L-ID citation requirement (per limitations doc §5) |
|---|---|
| D `descriptive_audit.md` | Cites L5 + L7 where the checklist depends on them (the §6.1 v24-presence-conditioning item → L5; the §6.1 missingness item → L7). |
| I `interpretation.md` | Cites every limitation that touches the HA's primary signals or operationalisation; one-sentence project-specific application per L-ID. |
| S₁ `cluster-*.md` | Cites every limitation that touches any cluster member; also cites L2 if cluster members are from different era strata. |
| S₂ `topic-*.md` | **MUST cite L1, L2, L4 unconditionally**; cite L3, L5, L6, L7 as they apply. |
| A `construct-*.md` | **MUST cite all seven L1-L7 with explicit applicability-or-NA per limitation** -- most rigorous L-ID discipline in the layer. |
| T translation artefacts | Patient-audience track translates applicable limitations into plain-language honest-uncertainty wording; research-audience track keeps the L-IDs as cross-references. |

A citation is not a copy-paste; it is a one-line acknowledgment with
the L-ID and one sentence on how the limitation applies to this
artefact's specific claim. The skill refuses to lock if the artefact's
L-ID block is missing an L-ID the map's per-row L-IDs column lists, or
if it adds an L-ID upstream did not cite (for Stage T -- source-
citation-fidelity).

## Cross-references

**Plan (the binding spec this skill implements)**:

- [`_plan_results_analysis_layer.md`](../../../docs/research/methodology/_plan_results_analysis_layer.md)
  -- r5 LOCKED 2026-06-24. §7 is the skill's binding spec
  (invocation shape, responsibilities, what-the-skill-must-not-do,
  instruction-MD requirements). §3 stage map + dependency rules; §3.5
  missing-inputs first-class; §3.6 map pre-registration + conflict-
  resolution rule; §3.7 drift & replication policy; §3.8 stopping &
  completion criteria; §3.9 research-line limitations binding; §3.10
  hard predictive gate; §3.11 follow-up suggestions own + external;
  §3.12 subject-narrative commentary; §4 producer/reviewer split;
  §9 layer-level anti-patterns; §11 step 7 (the implementation step
  this skill answers).

**Six guides (binding rule MDs this skill loads as data)**:

- Guide #1: [`descriptive_precondition_audit.md`](../../../docs/research/methodology/descriptive_precondition_audit.md) -- LOCKED r2 2026-06-24.
- Guide #2: [`verdict_to_inference.md`](../../../docs/research/methodology/verdict_to_inference.md) -- LOCKED r2 2026-06-24.
- Guide #3: [`internal_synthesis.md`](../../../docs/research/methodology/internal_synthesis.md) -- LOCKED r2 2026-06-24.
- Guide #4: [`external_contextualisation.md`](../../../docs/research/methodology/external_contextualisation.md) -- LOCKED r2 2026-06-24.
- Guide #5: [`actionability_translation.md`](../../../docs/research/methodology/actionability_translation.md) -- LOCKED r2 2026-06-24.
- Guide #6: [`translation_to_audience.md`](../../../docs/research/methodology/translation_to_audience.md) -- LOCKED r2 2026-06-24.

**Two supporting MDs (loaded as cross-cutting context)**:

- [`research_line_limitations.md`](../../../docs/research/methodology/research_line_limitations.md)
  -- LOCKED r3 2026-06-23. §3 seven L-IDs; §5 citation requirements
  table; §8 downstream-citation-count manual-pending-skill pattern.
- [`synthesis_structure_map.md`](../../../docs/research/methodology/synthesis_structure_map.md)
  -- LOCKED r3 2026-06-24. §3 cluster table; §4 topic table; §5
  construct table (with §3.12 commentary-eligibility notes); §6 lock
  log.

**Live artefacts the skill maintains**:

- `docs/research/methodology/_open_inputs.md` -- aggregated missing-
  inputs queue, scaffolded on first invocation per responsibility #6.
- `docs/research/methodology/plain_language_dictionary.md` --
  scaffolded on first Stage T invocation per responsibility #7 +
  guide #6 §9.1 bootstrap.

**Project conventions**:

- [`docs/research/CONVENTIONS.md`](../../../docs/research/CONVENTIONS.md)
  -- §1 role split; §1.2 reviewer-mode-with-authorization +
  fresh-session-review discipline; §2.1 descriptive before inference;
  §2.3 audit-before-push privacy gate (artefacts produced by this
  skill accumulate under `analyses/` and are subject to this gate at
  push time); §3 statistical-hygiene audit hooks; §4.1-§4.3
  descriptive-before-inference, caveats-vs-a-priori, prior-driven
  hypotheses as confirmatory.

**Adjacent skills**:

- [`../../commands/research-review.md`](../../commands/research-review.md)
  -- the fresh-session peer-review skill for reviewer-mode-with-
  authorization artefacts (Stages I / S₁ / S₂ / A / T outputs).
- [`../../commands/research-methodology-review.md`](../../commands/research-methodology-review.md)
  -- the fresh-session peer-review skill for producer-mode methodology
  MDs (including this skill itself, when it goes for review).
- [`../../commands/fetch-paper.md`](../../commands/fetch-paper.md) --
  for Stage S₂ literature-gap entries the skill routes via
  `_pending_literature_fetch.md`.

## Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-25 | Drafted r1 | Producer-mode by fresh agent per §11 step 7 of [`_plan_results_analysis_layer.md`](../../../docs/research/methodology/_plan_results_analysis_layer.md) (r5 LOCKED 2026-06-24). Operationalises six LOCKED guides as engine; guides remain source of truth. Seven inventions beyond §7: routing table; interview-engine seven-phase loop; cross-cutting §3.12 commentary section; L-ID discipline table; responsibility #11 downstream-citation-count maintenance; responsibilities #6+#7 explicit bootstrap for both `_open_inputs.md` AND `plain_language_dictionary.md`; skill-specific anti-patterns expanded 3→6. Project-convention: matches `.claude/skills/superdesign/SKILL.md` YAML frontmatter shape per plan §7 path mandate. Skill registered in user-invocable-skills list (verified via system reminder). |
| 2026-06-25 | Fresh-session `/research-methodology-review` | Verdict REVISION RECOMMENDED (mild). Report: [`../../../docs/research/reviews/methodology-research-interpret-skill-2026-06-25.md`](../../../docs/research/reviews/methodology-research-interpret-skill-2026-06-25.md). **Three critical confirmations all PASS**: (a) skill-doesn't-weaken-guide check passed across five spot-checked cross-references (Stage D refusal, Stage A hard predictive gate, anti-pattern #4 §3.12 separations, L-ID topic row, Phase 7 acceptance) — no paraphrasing weakening; (b) frontmatter discoverability confirmed via system-reminder showing skill in available-skills surface; (c) step-8 dry-run readiness YES with minor in-session-recoverable frictions. **Two required actions**: R1 — bootstrap race-condition between `_open_inputs.md` (responsibility #6) and `plain_language_dictionary.md` (responsibility #7); need ordering rule naming #6 FIRST; not blocking step 8 (only Stage T touches dictionary). R2 — Stage T skip-research-internal record location under-specified; one-sentence fix in Stage T row naming source artefact's §10 cross-refs as the location. |
| 2026-06-25 | Revised r1 → r2 | Both required absorbed: R1 — responsibility #7 added bootstrap-ordering rule: when both `_open_inputs.md` and `plain_language_dictionary.md` are absent at first invocation, `_open_inputs.md` is scaffolded FIRST (responsibility #6 precedes #7), since the queue is referenced from every guide while the dictionary is referenced only by Stage T. R2 — Stage T routing-table row explicitly names skip-record location at source artefact's §10 cross-references section, with one-line syntax (`Stage T research-audience track: SKIPPED-AS-RESEARCH-INTERNAL — rationale: <one-sentence>`) and per-source-stage cross-refs anchor (Stage A §5.12; Stage S₂ §4.10; Stage S₁ §4.10; Stage I §4.10). |
| 2026-06-25 | **LOCKED r2** | User acceptance ("Absorb R1+R2 (both one-sentence fixes), lock r2, proceed to step 8 dry-run on HA-C4"). Status of all sections LOCKED. **§11 step 7 closes — skill drafted and ready.** No second-pass review per established Option-γ pattern. |
| 2026-06-25 | §11 step 8 dry-run on C-stress-fatigue-shape | Agent dispatched per recommended option ("Dispatch agent to run dry-run end-to-end with sensible defaults + open_inputs for judgment calls"). Dry-run target swapped from plan §11.8a's HA-C4 to C-stress-fatigue-shape (HA-C3 v2 + HA-C3p) since the four-ready-set per stocktake §4 includes HA-C3 v2/p but not HA-C4; HA-C3 v2/p exercises two-member cluster logic + corrected concave-agreement framing without cascade-arrow complication. 7 artefacts produced (Stage D ×2 + Stage I ×2 + Stage S₁ + Stage S₂ + Stage A) + `_open_inputs.md` bootstrap. Verdicts landed: Stage S₁ → PARTIALLY CONCORDANT (defaulted per corrected r2 §5.2); Stage S₂ → DIVERGES + EXTENDS + CANNOT-SAY; Stage A → TIER-1 MONITORING (tier-3 STRUCTURALLY UNREACHABLE per §3.10 hard gate). 10 open_inputs entries logged. **Five skill→guide friction items surfaced** for r3 absorption: (1) §4.6 lived-experience-prior dispatcher tension; (2) §5.9 commentary dispatcher-cannot-articulate; (3) §4.4 coherence-call default-to-CONFLICT misroutes the agreement-label ambiguity; (4) Stage S₂ §7.1 read-section vs dispatched-headless tension; (5) need always-read-LOCKED-current-revision rule. |
| 2026-06-25 | Revised r2 → r3 | All five dry-run friction items absorbed: (1) added "Dispatch-mode placeholders" section codifying `DEFAULTED-PENDING-USER-INPUT` (Stage I §4.6) + `SKIPPED-AS-DRY-RUN-DEFAULT` (Stage A §5.9) + `DEFAULTED-TO-PRESERVE-PENDING-USER-INPUT` (Stage S₁ §4.4 agreement-label cases) each with §3.5 four-field open_inputs template pre-specified; (2) added "Coherence-call ambiguity clarification" section distinguishing agreement-label ambiguity (default: PARTIALLY CONCORDANT) from disagreement-boundary ambiguity (default: CONFLICT per guide #3 §4.4); (3) added "Stage S₂ proxy-citation pattern in dry-run" section allowing literature-brief artefact reliance in dry-run mode with `PROXY-CITED-IN-DRY-RUN` marker + production-lock follow-up requirement; (4) added "Always-read-LOCKED-current-revision rule" section requiring skill to verify `**LOCKED r<N>**` status header on every invocation; (5) — all four sections placed before §"Anti-patterns the skill must refuse" for visibility. The seven dry-run artefacts remain DRAFT-r1 in `analyses/` for user interview review; the r3 placeholders apply to future invocations. |
| 2026-06-25 | **LOCKED r3** | User acceptance ("Absorb 5 friction items into skill r3, then proceed to step 9 (translation dry-run)"). Status of all sections LOCKED including the four new r3-added sections. **Implementation proceeds to §11 step 9 (translation dry-run on the Stage A construct-stress-fatigue-monitoring.md actionability output from the step-8 dry-run).** No second-pass review per established Option-γ pattern. **Drift triggers registered** unchanged from r2 + observed-friction-from-dry-run as a new trigger class. |
| 2026-06-25 | §11 step 9 translation dry-run | Agent dispatched per recommended option. Stage T executed on two source artefacts (construct-stress-fatigue-monitoring + topic-stress-fatigue-pacing). 4 artefacts produced (2 research-audience + 2 patient-audience). `plain_language_dictionary.md` bootstrap fired correctly per skill r3 responsibility #7 ordering rule — 30 initial entries seeded covering signals, labels, L-ID renderings, external-literature concepts. 5 new entries (OI-011 through OI-015) appended to `_open_inputs.md`. **Five Stage-T-specific friction items surfaced** for r4 absorption: (1) §5.11 ABSENT marker convention under-specified; (2) DRAFT-on-DRAFT lock-state cascade under-specified (highest priority — guide #6 §9.2 would halt without explicit placeholder); (3) "Commentary not applicable" line conflates two distinct semantics; (4) cross-track dictionary-update routing under-specified; (5) visual cross-source sharing pattern under-specified. Agent's concrete r4 recommendation: codify `DRAFT-ON-DRAFT-DRY-RUN` as fourth dispatch-mode placeholder. |
| 2026-06-25 | Revised r3 → r4 | All five step-9 friction items absorbed: (1) `DRAFT-ON-DRAFT-DRY-RUN` codified as fourth dispatch-mode placeholder with §3.5 four-field open_inputs template; resolves the load-bearing friction enabling Stage T dry-runs to proceed on DRAFT-r1 sources. (2) Four Stage T operational clarifications added in new "Stage T operational clarifications" section: §5.11 ABSENT marker convention; "Commentary not applicable" two-wording distinction (Stage A SKIPPED vs Stage S₂ structural-rule); dictionary-update routing rule (patient-audience track first-draft only triggers appends; research-audience never triggers); visual cross-source sharing pattern between Stage A construct + parent Stage S₂ topic with one-line shared-spec note. All four operational clarifications supplement guide #6 LOCKED r2 without revising it; guide #6 r3 absorption may codify them at the guide level in a future revision pass. |
| 2026-06-25 | **LOCKED r4** | User acceptance ("Absorb 5 friction items into skill r4 + dispatch step 10 rollout-order interview"). Status of all sections LOCKED including the new r4-added DRAFT-on-DRAFT placeholder + Stage T operational clarifications section. **Implementation proceeds to §11 step 10 (rollout-order interview with user).** No second-pass review per established Option-γ pattern. **Drift triggers registered** unchanged from r3 + ongoing-dry-run-friction-observation as continued trigger class through step 11 rollout. |
