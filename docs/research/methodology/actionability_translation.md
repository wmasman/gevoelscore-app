# Actionability translation — Stage A guide

**Status**: **LOCKED r2** by user acceptance 2026-06-25. r1 authored
2026-06-24 by a fresh agent per §11 step 6.5 of
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
(r5 LOCKED 2026-06-24). r1 → r2 absorbed a fresh-session
`/research-methodology-review` (verdict REVISION RECOMMENDED (mild),
report at
[`reviews/methodology-actionability_translation-2026-06-24.md`](../reviews/methodology-actionability_translation-2026-06-24.md))
that caught two required actions (R1: §5.5 needs a seventh PPV-floor
anchoring discipline element to prevent trivially-passable floor
backdooring the §3.10 gate; R2: §5.10 cross-reference to §6.1 + §6.2
+ §6.4 downgrade-mechanics) and three recommended (A1 ~50-80-line
density compression — deferred per reviewer "for a future revision
pass" framing; A2 §5.7 → §7.4 binding-loop completion; A3 §11 lock-
log scannability). Hard predictive gate per §3.10 preserved at five
enforcement layers without weakening; §3.12 commentary discipline
fully implemented. Implementation proceeds to §11 step 6.6 (guide #6
`translation_to_audience.md` — the last guide).

This guide is the fifth of six binding methodology MDs for the
results-analysis layer. It governs **Stage A** (actionability
translation): the per-construct artefact that takes a topic's locked
`topic-*.md` and produces — or refuses to produce — a daily-life-signal
claim about the construct, drawn from a fixed three-tier set
(monitoring / informative-pattern / predictive-use). It sits between
Stage S₂'s per-topic positioning calls (its direct upstream gate)
and Stage T's audience-targeted translation artefacts (its direct
downstream consumer). It refuses to start on a construct whose
feeding topics lack locked `topic-*.md` artefacts, on a construct
that is not pre-declared in the synthesis-structure map, and on any
predictive-tier claim that lacks a pre-registered forward-validation
HA per the §3.10 hard predictive gate.

Stage A is the **highest-risk surface in the layer**. Where Stages
I / S₁ / S₂ license claims about hypothesis / cluster / topic-vs-
literature, Stage A licenses claims about **what the subject may
say about the signal in lived experience** — where research output
meets the patient-user's daily decisions. The §3.10 hard
predictive gate is severe here because the cost of an unearned
predictive claim lands on the subject's daily life, not on a peer
reader. The §3.12 commentary layer is the sibling discipline:
bounded patient-facing nuance space without backdooring the gate.

---

## 1. Purpose

> **A construct's topic-level positioning is a within-subject finding
> placed against external literature. Stage A produces — or refuses
> to produce — a daily-life-signal claim at one of three tiers
> (monitoring / informative-pattern / predictive-use), drawn from a
> fixed three-tier set, where each tier's wording is what the subject
> may safely say about the signal. Predictive-tier claims require a
> pre-registered forward-validation HA per §3.10; this is non-
> negotiable. Optional subject-narrative commentary per §3.12 may
> attach to tier-1 or tier-2 formal claims with discipline rules
> that prevent the §3.10 gate from being backdoored.**

Many constructs in the map have a tier aspiration recorded in the
§5 K-row as the **most the construct could reach if all required
evidence lands**. Stage A is the per-construct discipline gate
that turns the aspiration into either an earned tier claim or an
explicit downgrade. Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3 stage-map: `D → I → S₁ → S₂ → A → T`. Stage A sits between
Stage S₂'s positioning and Stage T's audience-targeted
translation; §3.12 commentary (when produced) propagates into
Stage T's patient-audience-track only. The tier-claim discipline
is what lets Stage T's translation rest on an honest reading of
"what the signal can be used for in daily life," rather than
letting wording-drift do the tier-promotion work no evidence has
earned.

**What Stage A does NOT do.**

- **NOT re-test the hypothesis or any verdict.** Verdicts come from
  each HA's `result.md` via D → I → S₁ → S₂ and are read as fixed
  inputs through the feeding `topic-*.md`.
- **NOT predict without a pre-registered forward-validation HA.**
  Per §3.10: predictive claims require a forward-validation HA
  locked before its prediction window, with a SUPPORTED
  `result.md`. **Until that HA exists, the construct is capped at
  informative pattern.** Non-negotiable; this guide may not weaken
  it. §4, §5.5, §6.1 + §6.2, §7.1 operationalise.
- **NOT invent new caveats post-hoc.** Caveats come from the
  feeding topic's §4.6 + §4.7 + §4.8, the chain back to member
  `interpretation.md` files, and the limitations doc §3 with the
  per-`construct-*.md` binding from §5 (all seven L-IDs with
  applicability-or-NA). §7.6 enforces.
- **NOT frame claims as advice.** The artefact licenses what the
  subject may safely **say about the signal**, not what to **do**
  with it. §7.2 enforces; §4 permitted-wording lists carry the
  per-tier discipline.
- **NOT use §3.12 commentary to escape the §3.10 gate.** Commentary
  is patient-facing nuance attached to tier-1 or tier-2 formal
  claims; it CANNOT promote tier, CANNOT be cited downstream,
  CANNOT float unattached. §5.9 + §6.4 + §7.7 + §7.8 + §7.9
  operationalise.
- **NOT re-decide which topics feed which constructs.** Per §3.6:
  map-change-needed → Stage A HALTS and routes to a separate
  producer-mode map-revision session per §6.5.
- **NOT operate on more than one construct per session.**
  Construct-bounded scope keeps tier claims commensurate.

**Alternatives considered** (per CONVENTIONS §2.2 item 3). The
natural alternatives are folding actionability into Stage T
translation OR skipping a formal Stage A and emitting only
audience-targeted translation. Both rejected for: (a) **gate-
discipline placement** — §3.10 is structurally easier to enforce
as a discrete per-construct artefact than as wording inside a
translation; (b) **commensurability** — uniform three-tier set +
§3.10 framing + §3.12 commentary discipline let downstream readers
read tier claims as commensurable across constructs; (c)
**RESEARCH-REPORT §5.2 precedent** — the project has already
learned PPV-with-base-rate framing saved a bad feature design;
that lesson deserves its own per-construct discipline gate.

**Precondition: the `/research-interpret` skill must land first.**
Per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§11 step 7, the `/research-interpret` skill is built after the six
guides (this guide is #5 of six). **No Stage A artefact can be
drafted before §11 step 7 lands** — this guide alone is necessary
but not sufficient. The §9 agent-instruction outline below is the
skill's brief; the skill build (step 7) operationalises it.

## 2. Inputs

The actionability translation MUST load and use the following
inputs, in this order:

1. **The feeding `topic-*.md` files for the construct** — all of
   them, all locked (per locked-plan §3 dependency rule: "`A` on a
   construct refuses to start until `S₂` for the relevant topic(s)
   is complete AND the construct appears in the pre-registered
   synthesis-structure map AND the actionability tier being claimed
   is permitted by the evidence layer"). For each topic: §4.5
   positioning summary (the topic-level call drawn from AGREES /
   EXTENDS / DIVERGES / CANNOT-SAY); §4.5 per-subclaim positionings
   (including any DIVERGES subclaim carried as the topic's primary
   substantive finding per §4.5 + §7.12 of guide #4); §4.6 N-of-1-
   to-group caveats; §4.7 L-ID block; §4.8 open conflicts; §4.9
   follow-up tracks. Stage A reads each topic as a fixed input —
   it does NOT renegotiate positioning, caveats, or open conflicts.
2. **The synthesis-structure map's §5 construct row** for the target
   construct at
   [`synthesis_structure_map.md`](synthesis_structure_map.md) —
   construct name; topics feeding (the §4 rows that feed this
   construct); **tier aspiration** (the most the construct could
   reach if all required evidence lands — monitoring / informative-
   pattern / predictive-use); the **predictive-claim feasibility
   note** (the map's current-state assessment of what blocks
   predictive-tier, including the forward-validation HA requirement
   per §3.10 and the §3.12 commentary-tier-promotion prohibition);
   the **L-ID notes column** (all seven evaluated with applicability-
   or-NA per limitation, per the map r3 §5 binding); the **§3.12
   commentary-eligibility note** (per the map r3 §5 added paragraph:
   every tier-1 or tier-2 active construct is commentary-eligible
   with the discipline rules cited inline); declared-date + lock-
   version. Plus the §3 cluster rows the topics roll up from, for
   §4.10 cross-references.
3. **The contributing `cluster-*.md` files via the topic chain** —
   upstream context only; Stage A does NOT re-read each cluster's
   §4.4 coherence call directly (those entered the topic via Stage
   S₂). Documented in §5.12 cross-references for reader-traceability.
4. **[`research_line_limitations.md`](research_line_limitations.md)**
   — §3 (seven L-IDs L1-L7); §5 row for `construct-*.md`: **MUST
   cite all seven L-IDs with explicit applicability-or-NA per
   limitation**. The **most rigorous L-ID discipline of any
   artefact type** — construct-level claims are the downstream-most
   and inherit all systemic context. §3 (output) and §5.11 below
   operationalise.
5. **The map's §5 row's tier aspiration as the upper bound.** The
   tier aspiration is a structural pre-decision; Stage A reads it
   as the ceiling AND independently re-evaluates whether the §3.10
   conditions have been met at Stage A time (a forward-validation
   HA may have landed; PPV-with-base-rate may now be computable;
   the feeding topic's positioning may have shifted via drift).
   Aspiration is upper bound, not earned tier.
6. **Any forward-validation HAs in the registry** that target this
   construct — per §3.10, a predictive claim requires a **named**
   forward-validation HA, **locked before the prediction window
   begins**, with a **verdict on its `result.md`**. Stage A loads
   the HA's `hypothesis.md` + `result.md` (where they exist). For
   the two active constructs in map r3, no forward-validation HA
   has been pre-registered as of this guide; Stage A on those caps
   at tier-1 / tier-2, with the forward-validation HA shape
   recorded in §5.5 + §5.8.
7. **The relevant methodology MDs** — guides #1-#4 (the upstream
   chain); any construct-specific methodology MD the topic chain
   cites (e.g.
   [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md);
   [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)).
8. **[`RESEARCH-REPORT.md`](../RESEARCH-REPORT.md) §5.2 PPV-with-
   base-rate precedent** — *"The positive predictive value... is
   ~4% at the residual-crash base rate of ~2 per year. A
   predictive alert card would be wrong 24 times out of 25."* The
   §5.7 plain-language frame draws directly from this precedent.
9. **The hard predictive gate from §3.10** as a binding rule: *"A
   predictive claim requires a named forward-validation HA in the
   registry, locked before the prediction window begins, and a
   verdict on its result.md. Until that HA exists and SUPPORTS the
   predictive claim, the construct is capped at 'informative
   pattern.' This is non-negotiable at the layer level; guide
   drafts may not weaken it."* The **load-bearing constraint of
   the entire stage**.
10. **The §3.12 commentary-eligibility status from the map's r3 §5
    row** — every tier-1 or tier-2 active construct is commentary-
    eligible per the map r3 §5 added paragraph. Tier-3 constructs
    are NOT commentary-eligible (per §3.12 hard separations: tier-3
    carries forward-validation HA evidence and does not need
    commentary nuance).
11. **Lived-experience priors from the user** — recorded in §6 of
    relevant `interpretation.md` files. Per §3.12 hard separations:
    "reliable for me" priors cannot promote the tier without
    forward-validation HA. Recorded as commentary candidates per
    §5.9; do not license a higher tier. §6.3 conflict rule
    operationalises.
12. **CONVENTIONS** — §1 (reviewer-mode-with-authorization mode);
    §1.2 (fresh-session peer review; `## Authorship` block); §2.1
    (descriptive-before-inference; chain inherits); §4.2 (caveat
    what was not earned); §4.3 (prior-driven hypotheses
    confirmatory).

The translation does NOT load: raw descriptive runs (those were
Stage D inputs; Stage A inherits via the chain); member HAs' `test.py`
or `result-data.json` (those were Stage D / Stage I inputs); other
constructs' `construct-*.md` artefacts (cross-construct reading is
out of scope for Stage A — that belongs at Stage T or beyond).

## 3. Output

The translation produces exactly one artefact per construct:

```
docs/research/analyses/actionability/construct-XXX.md
```

**Naming convention.** One file per construct at the top level of
`analyses/actionability/` — **no per-construct subfolder**. The
construct name in the filename is the construct's exact ID from the
synthesis-structure map's §5 row (e.g.
`construct-stress-fatigue-monitoring.md`,
`construct-bout-recovery-signal.md` for the two active K-rows in
the map's r3). Flat naming matches the locked plan's §5 output-
structure tree exactly. Revision history lives in the file's own
§11 lock log; revisions to any feeding `topic-*.md` re-trigger this
artefact per the §3.7 drift policy, as does a forward-validation HA
landing or a §3.10-affecting methodology change.

**Mode.** Reviewer-mode-with-authorization per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§4 producer/reviewer split table. Drafted by Claude under user
authorization via `/research-interpret actionability construct-XXX`,
carrying a `## Authorship` block per
[CONVENTIONS §1.2](../CONVENTIONS.md#12-producer-vs-reviewer-mode).
Receives a fresh-session `/research-review` pass before lock per the
locked-plan §4 row for actionability-tier-claim artefacts (same
discipline Stages I, S₁, S₂ outputs carry; tier downgrades on review
concerns are explicit in the plan's §4 row).

**L-ID citation discipline at the output level.** Per
[`research_line_limitations.md`](research_line_limitations.md) §5
table row for `construct-*.md`:

> ***MUST cite all seven L-IDs with explicit applicability-or-NA per
> limitation*** (actionability is the downstream-most claim and
> inherits all systemic context).

This is the **most rigorous L-ID discipline of any artefact type in
the layer**. Where `interpretation.md` cites the limitations that
touch the HA, `cluster-*.md` cites the union touching members,
`topic-*.md` cites L1+L2+L4 unconditionally plus L3/L5/L6/L7 as they
apply — `construct-*.md` cites **all seven**, with each L-ID either
**applied** (one sentence on how it bounds this specific construct-
level claim) or **explicitly NA** (one sentence on why this
construct's tier claim is exempt from the limitation, drawn from
the map's §5 L-ID-notes column). §5.11 below carries the L-ID
citation block.

**Hard rule.** A Stage A artefact missing any of L1-L7 from §5.11
is incomplete and §9.6 refuses to lock it. The all-seven binding is
the layer's commensurability guarantee at the construct level — every
construct-level tier claim sits inside the same seven-L-ID envelope,
read out explicitly per construct.

**Hard rule.** Stage A MUST NOT cite an L-ID without a project-
specific application or NA reason. A bare "L5 NA" without one
sentence on why the construct's tier claim is exempt is forbidden;
the NA call requires the same single-sentence project-specific
reason as the apply call.

**Worked-example anchors** (two active constructs in map r3):

- `construct-stress-fatigue-monitoring.md` — L1/L2/L3/L4/L6/L7
  apply; L5 NA (no v24 per map §5). Tier-1 aspiration (PPV-
  exempt); §3.12 commentary-eligible.
- `construct-bout-recovery-signal.md` — L1/L2/L3/L4/L7 apply; L5
  NA; L6 NA (gevoelscore not in primary cell). Tier-2 aspiration
  (PPV-required); §3.12 commentary-eligible.

## 4. The three tiers (binding mapping rules)

This section pins the per-tier rules. Each tier's claim shape is
fixed; each tier's required evidence is fixed; each tier's permitted
wording is bounded. One worked example per tier, drawn from the two
active constructs in the map's r3 (K-stress-fatigue-monitoring tier-1
aspiration; K-bout-recovery-signal tier-2 aspiration). The hard
predictive gate at tier-3 is the load-bearing constraint and is
operationalised in §5.5 (forward-validation pathway), §6.1 + §6.2
(conflict rules), and §7.1 (the predictive-overclaim anti-pattern).

### 4.1 Tier 1 — Monitoring signal

**Claim shape.** "[signal X] tracks [construct Y] descriptively."
The signal moves with the construct; tracking the signal lets the
subject observe the construct's state but does NOT license claims
about what the construct will do next.

**Required evidence.** S₁ CONCORDANT or PARTIALLY CONCORDANT
synthesis on the cluster(s) feeding the construct, AND comparability
check passed at S₂ (the topic's §4.4 COMPARABLE or PARTIALLY
COMPARABLE call with the topic's §4.5 positioning at AGREES /
EXTENDS / DIVERGES on direction — NOT CANNOT-SAY at the topic
level, which would block even tier-1). Tier-1 does NOT require
PPV-with-base-rate per §3.10 (the §3.10 binding starts at tier-2);
descriptive shape is sufficient.

**§3.10 PPV-with-base-rate status.** PPV-exempt at tier-1. The
descriptive monitoring claim does not require diagnostic-quality
measures; it is a "watch this together with that, they move
together" claim, not a "this signals that" claim.

**Permitted wording.** "When [signal X] is at [range], [construct
Y] tends to be at [range] too." "Tracking [signal X] gives a
daily view of [construct Y]." "Higher / lower values correspond
to higher / lower [construct Y] across the window." Descriptive,
correspondence-framed; NOT forecast-framed; NOT advice-framed.

**Forbidden wording at tier-1.** Forecast ("predicts",
"forecasts", "will", "tomorrow"); causal ("causes", "drives",
"makes"); advice ("should", "must", "recommended"); predictive in
disguise ("watch for [signal X] dropping" — §7.5 anti-pattern).
The §3.12 commentary section may use subject-attributed soft-hint
wording per §5.9; the formal tier-1 claim may not.

**§3.12 commentary eligibility.** Tier-1 monitoring claims ARE
commentary-eligible per the map r3 §5 row. The optional §5.9
section may attach to the tier-1 formal claim with the §3.12
discipline rules in full.

**Worked example — K-stress-fatigue-monitoring tier-1 claim.** Map
§5 tier-1 aspiration; feeding T-stress-fatigue-pacing topic on
C-stress-fatigue-shape cluster (HA-C3 v2 REJECTED + HA-C3p
PARTIAL, both detecting inverted-U per guide #3 r2). Topic likely
PARTIALLY CONCORDANT cluster + DIVERGES from Wiggers on shape per
guide #4 §5.3.

> §4.1 tier-1 claim: "Daily `all_day_stress_avg` tracks daily
> `gevoelscore` descriptively across the Stratum 4 unmedicated
> window. The two signals move together with an inverted-U shape
> peaking around mid-stress; tracking daily Garmin stress gives
> the subject a same-day window onto the day's gevoelscore range."

Tier-1 wording deliberately omits "tomorrow's gevoelscore," "alert
when stress crosses X," or any forecast frame. Forecast would
require tier-2 (PPV-with-base-rate) and then tier-3 (forward-
validation HA) on top.

### 4.2 Tier 2 — Informative pattern

**Claim shape.** "[signal X] historically associated with [pattern Y]
under [conditions Z]." The signal has shown a reliable association
with a pattern (a crash, a recovery, a bout, a state) in past data;
seeing the signal raises the subject's reasonable expectation that
the pattern has occurred or is occurring. Tier-2 is association-with-
context, NOT forecast.

**Required evidence.** All of tier-1's requirements, PLUS:

1. **Replicated across operationalisations** — two-or-more
   **independent** HAs in the cluster, **NOT three on the same
   column**. The map's §3 row "Operationalisation overlap note"
   cell carries the project's evidence-strength rationale for this
   independence judgment (per the locked plan §6.3 anti-pattern:
   "three HAs on the same signal are one piece of evidence, not
   three"). Independence at tier-2 means cross-operationalisation
   replication — different bin schemes, different windows, different
   era strata, different cohort cells — not the same signal tested
   three ways.
2. **PPV-with-base-rate per §3.10 required** — computed in the
   RESEARCH-REPORT §5.2 plain-language frame ("right N out of M
   when it fires" / "wrong M-N out of M when it fires"), with the
   base rate stated for the era (per §3.9 limitations binding — not
   aggregated across eras). Per §3.10 conflict rule: if PPV-with-
   base-rate cannot be computed, the tier downgrades to monitoring
   (tier-1) and the missing base-rate logs in §5.6 `open_inputs`.
3. The constructed-claim must pass the §3.10 base-rate framing
   check at §5.7 quality measures. A tier-2 claim whose PPV is
   stated without its base-rate context is forbidden per §3.10 and
   §7.4 anti-pattern (bare-percentage actionability).

**§3.10 PPV-with-base-rate status.** **Required at tier-2.** §5.7
below operationalises the quality-measures section in full. The
plain-language frame is mandatory; optional measures (NPV,
sensitivity, specificity, false-alarm rate, lead time, reliability)
are encouraged but not required at tier-2.

**Permitted wording.** "When [signal X] was at [range] in past
data, [pattern Y] was observed N out of M times, where [pattern
Y] happens M times per year." "Past observations show [signal X]
associated with [pattern Y] under [conditions Z]." Past-tense
association-framed with base-rate context; NOT forecast-framed.

**Forbidden wording at tier-2.** All of tier-1's forbidden list,
plus: bare-percentage without base-rate ("60% PPV" without "out
of N expected events per year" — §7.4); prospective forecast
disguised as past-tense ("has historically forecast [Y]" —
preferred: "associated with"); absolute claim ("X means Y" reads
deterministic; preferred: "associated with under conditions").

**§3.12 commentary eligibility.** Tier-2 informative-pattern claims
ARE commentary-eligible per the map r3 §5 row. The optional §5.9
section may attach to the tier-2 formal claim with the §3.12
discipline rules in full.

**Worked example — K-bout-recovery-signal tier-2 claim.** Map §5
tier-2 aspiration; feeding T-within-day-recovery topic on
C-bout-substance cluster (HA-C4c; Cliff's δ = +0.120; +20.26 pp
discrimination per map §5). C-bout-framework cascade-precondition
applies. Topic likely AGREES with within-day-recovery impairment
consensus per the four anchors.

> §4.2 tier-2 claim *(if §5.7 PPV-with-base-rate computes)*: "When
> `bout_n_did_not_return_day` exceeded the heavy-T-day threshold
> in past cross-phase pooled data, a crash day followed within
> the observation window N out of M times, where crash days occur
> ~2 per year residual base rate per RESEARCH-REPORT §5.2. Past
> observations show bout-level recovery-impairment associated
> with crash-day occurrence under cross-phase pooled conditions."

The "associated with under conditions" framing is the tier-2
discipline; base-rate context is non-negotiable. If PPV cannot
compute against the residual-crash base rate, §3.10 conflict rule
routes the tier to tier-1; §5.6 logs the missing PPV; §5.7
records the downgrade explicitly.

### 4.3 Tier 3 — Predictive use

**Claim shape.** "[signal X] forecasts [outcome Y] in advance."
The signal predicts the outcome before the outcome occurs; seeing
the signal lets the subject anticipate the outcome with quantified
quality measures (PPV, lead time, reliability) calibrated against
forward-validated unseen-data evidence.

**Required evidence.** All of tier-2 (tier-1 + cross-op
replication + PPV-with-base-rate), PLUS:

**A pre-registered forward-validation HA.** Per §3.10: the HA
must be **named in the registry**, **locked before the prediction
window begins**, predict on **unseen days** (no retrospective fit),
and produce a **SUPPORTED verdict on its `result.md`**.
Retrospective-only fit does **NOT** qualify.

**§3.10 status.** PPV + base rate REQUIRED, plus REQUIRED lead
time + reliability per §3.10 tier-3 discipline: *"A predictive
claim that does not specify 'a day in advance' vs 'an hour in
advance' is operationally meaningless; one that does not check
whether the signal is stable across similar days has no defence
against random-walk artefacts."* §5.7 carries the requirements.

**Permitted wording.** "When [signal X] reaches [range] today,
[outcome Y] follows [lead-time later] with PPV N out of M at the
residual base rate of M events per year; signal is test-retest
stable across [similar-day reference]." Forecast wording permitted
because the forward-validation HA earned it, with quality measures
attached — NOT bare forecast.

**Forbidden wording at tier-3.** Bare forecast ("[X] predicts [Y]")
without PPV + base rate + lead time + reliability is forbidden per
§3.10 + §7.4. Advice wording remains forbidden per §7.2.

**§3.12 commentary eligibility.** **NOT eligible** per §3.12 hard
separations. Tier-3 carries forward-validation HA evidence and
does not need commentary nuance.

**Worked example — none active in the map's r3.**

Neither K-stress-fatigue-monitoring (tier-1 aspiration) nor
K-bout-recovery-signal (tier-2 aspiration) reaches tier-3 in the
map's r3. The map's §5 predictive-claim-feasibility cells for both
constructs say "Predictive-use tier **blocked**" with the §3.10
hard predictive gate reason. Tier-3 worked examples would only
arise once a forward-validation HA pre-reg lands and produces a
SUPPORTED verdict for one of the constructs — at which point Stage
A would re-examine the construct per §3.7 drift trigger and
potentially produce a tier-3 claim. §5.5 forward-validation pathway
below records the HA shape that would unlock the tier-3
re-examination for each of the two active constructs.

### 4.4 Tier mapping — summary table

The three tiers and their core distinguishing features:

| Tier | Claim shape | Evidence floor | §3.10 PPV | Forward-validation HA | §3.12 commentary |
|---|---|---|---|---|---|
| 1 — Monitoring | "tracks [Y] descriptively" | S₁ CONCORDANT/PARTIAL + S₂ comparability passed | NOT required | NOT required | **ELIGIBLE** |
| 2 — Informative pattern | "historically associated with [Y] under [Z]" | tier-1 + cross-op replication + PPV-with-base-rate computable | **REQUIRED** | NOT required | **ELIGIBLE** |
| 3 — Predictive use | "forecasts [Y] in advance" | tier-2 + pre-registered forward-validation HA SUPPORTED | **REQUIRED + lead-time + reliability** | **REQUIRED** | NOT eligible |

The discipline cascade: monitoring is descriptive, informative-
pattern is historical-association, predictive-use is forecast. Each
tier's wording stays bounded to what its evidence floor licenses;
tier promotion requires the higher evidence floor, not stronger
wording.

## 5. Section outline for the produced `construct-XXX.md`

The artefact MUST contain twelve sections in this order. Each
section's operational guidance follows. Sections that mirror
upstream guides' shape are kept terse; sections specific to Stage A
(§5.5 forward-validation pathway, §5.7 quality measures, §5.9
commentary, §5.11 all-seven L-IDs) carry the full operational
detail per the §6.5 spec brief.

### 5.1 Section 1 — Target construct + originating topic(s)

Mechanically copy from the map's §5 construct row + each feeding
topic's `topic-*.md` §4.1 header: construct ID + name (verbatim);
topics feeding (verbatim); for each topic, topic ID + §4.5
positioning summary verbatim + any per-subclaim positionings
relevant to the construct's tier evidence (especially DIVERGES
subclaim if the topic has one); tier aspiration from the map's §5
row (verbatim); §3.12 commentary-eligibility status from the map's
§5 row (verbatim); declared-date + lock-version of the construct
row. Header, not analysis; its purpose is to fix the construct
target and the upstream chain.

### 5.2 Section 2 — Evidence layer (tier requirements met / unmet)

Per tier (monitoring / informative-pattern / predictive-use), one
paragraph stating whether the tier's evidence floor is met. The
paragraph maps to the §4 binding mapping rules:

- **Tier-1 evidence check** — Are the feeding topic's positioning
  conditions met (S₂ comparability passed with positioning at
  AGREES / EXTENDS / DIVERGES, NOT CANNOT-SAY)? Are the underlying
  clusters' S₁ coherence calls at CONCORDANT or PARTIALLY
  CONCORDANT (not CONFLICT or ORTHOGONAL at the construct-relevant
  cluster)? If met: tier-1 evidence floor reached. If not: which
  condition fails, and what is logged to §5.6 `open_inputs`.
- **Tier-2 evidence check** — Beyond tier-1, are the constituent
  HAs cross-operationalisation independent (two or more, NOT three-
  on-same-column)? Is the §3.10 PPV-with-base-rate computable
  against the relevant residual-event base rate for the era? If
  met: tier-2 evidence floor reached. If not: which condition
  fails, and the §3.10 conflict rule applies (PPV-uncomputable →
  downgrade to tier-1, base rate logged to §5.6 `open_inputs`).
- **Tier-3 evidence check** — Beyond tier-2, does a pre-registered
  forward-validation HA exist in the registry, locked before the
  prediction window, with a SUPPORTED verdict on its `result.md`?
  Are lead-time and reliability measures computable? **The §3.10
  hard predictive gate**: if any of the forward-validation HA
  conditions fail, **tier-3 is structurally unreachable** and the
  construct caps at tier-2 (or tier-1 if tier-2 also fails). The
  forward-validation HA shape that would unlock tier-3 is recorded
  in §5.5 below.

The §5.2 section closes with the **tier earned at this Stage A
time**: one of tier-1 monitoring / tier-2 informative-pattern /
tier-3 predictive-use / no tier (if even tier-1 fails). The earned
tier is the binding output; the map's aspiration is the ceiling but
NOT the earned tier.

### 5.3 Section 3 — Tier claim + permitted wording

The earned-tier claim sentence, written in the §4 permitted-wording
discipline for that tier. One paragraph per claim. For the worked
examples in §4:

- *K-stress-fatigue-monitoring tier-1 claim* (per §4.1 example).
- *K-bout-recovery-signal tier-2 claim* (per §4.2 example, if §5.7
  PPV computes; tier-1 fallback if not).

Each claim names the signal explicitly (column / measurement-
operationalisation), names the construct explicitly, names the
era / cohort / condition scope explicitly (per the upstream chain's
positioning), and stays within the tier's permitted-wording bounds
per §4.

The §5.3 section also records the **permitted-wording list for the
subject** at the claim's tier (drawn from §4 per the earned tier).
This is the subject-facing wording the construct artefact licenses
for daily use; downstream Stage T patient-audience translation
draws on this list as the wording-discipline source.

### 5.4 Section 4 — What the subject may NOT do with this signal

The easy overclaims, explicitly refused per the earned tier. One
paragraph per overclaim; categories below are mandatory minimum;
the section may add construct-specific overclaims the upstream
chain surfaced (topic §4.6 caveats; cluster §4.7b refusals; member
§4 interpretation refusals).

**At tier-1 (monitoring) — mandatory refusal categories.**

1. **Predictive-use overclaim**: "The subject may NOT use [signal X]
   to predict [construct Y]." The tier-1 descriptive correspondence
   is past-window observation, not forecast.
2. **Causal overclaim**: "The subject may NOT infer that [signal X]
   causes [construct Y] from this monitoring claim." Correspondence
   in the predicted direction is not mechanism (per guide #2 §7.2
   anti-pattern).
3. **Group-level overclaim**: "The subject may NOT generalise the
   monitoring claim to 'people like me' without group-level
   confirmation." Per L1 single-subject reach.
4. **Advice overclaim**: "The subject may NOT use [signal X] as a
   prescriptive trigger ('rest when X drops'). The signal does not
   license action; it licenses observation." (Stage A does NOT
   produce advice per §7.2 anti-pattern.)

**At tier-2 (informative pattern) — add to the tier-1 refusals.**

5. **Forecast overclaim**: "The subject may NOT read the tier-2
   association as a forecast. The past-data association under
   [conditions Z] does not license forward-looking forecast wording;
   forecast requires tier-3 (forward-validation HA)."
6. **Bare-percentage overclaim**: "The subject may NOT cite the PPV
   without its base-rate context. '60% accurate when it fires' is
   meaningless without 'fires N times in M expected events' per
   §3.10 + §7.4 anti-pattern."

**At tier-3 (predictive use) — add to tier-1+2 refusals.**

7. **Lead-time-implicit overclaim**: "The subject may NOT use a tier-3
   forecast claim without its specified lead time. A 'predicts X' frame
   without 'a day in advance vs an hour in advance' is operationally
   meaningless per §3.10 tier-3 discipline."
8. **Reliability-implicit overclaim**: "The subject may NOT use a
   tier-3 forecast claim without its reliability bound. A signal that
   forecasts X on unseen days but is test-retest unstable has no
   defence against random-walk artefacts per §3.10 tier-3 discipline."

**Worked example — K-stress-fatigue-monitoring tier-1 §5.4 block.**

> Subject may NOT use daily `all_day_stress_avg` to predict
> tomorrow's gevoelscore (predictive-use overclaim — descriptive
> correspondence does not license forecast). Subject may NOT infer
> stress causes gevoelscore from this monitoring claim (causal
> overclaim — correspondence in predicted direction is not
> mechanism per guide #2 §7.2). Subject may NOT generalise to
> "people like me" without group-level confirmation (per L1).
> Subject may NOT use Garmin stress as a prescriptive trigger
> ("rest when stress crosses 40") — signal licenses observation,
> not action; advice would require intervention-study methodology
> the research line cannot run on itself per L4.

### 5.5 Section 5 — Forward-validation pathway

The shape of the pre-registered forward-validation HA that would
unlock tier-3 promotion (or, for constructs that earned tier-3, the
forward-validation HA that earned it, cited as the registry entry).
This section is mandatory when:

- Tier-3 was wanted but not earned (the §5.2 evidence check ruled
  it out via the §3.10 forward-validation HA condition); OR
- Tier-3 was earned (and the section cites the registry HA that
  earned it, including its prediction-window dates, the SUPPORTED
  verdict reference, and the §3.10 plain-language PPV-with-base-
  rate from its `result.md`).

When tier-3 was not wanted (the construct's aspiration in the
map's §5 row is tier-1 or tier-2 with no path to tier-3 in the
current evidence regime), this section records "Tier-3 not
aspired; forward-validation pathway not specified at this Stage A
time; if tier-3 aspiration emerges later, this section is added
under §3.7 drift re-examination."

**The forward-validation HA shape (when specified).** Per
[`hypothesis_lock_process.md`](hypothesis_lock_process.md) discipline,
a forward-validation HA pre-reg carries:

1. **Target construct + signal** (the signal whose predictive
   claim is being tested; the construct whose tier promotion would
   be unlocked).
2. **Prediction window** (specific dates — typically a future
   N-day or N-week unseen-data window, locked before the window
   begins so the data is genuinely unseen at lock time).
3. **Prediction rule** (the operationalisation: "when [signal X]
   exceeds [threshold T] on day D, predict [outcome Y] occurs
   within day D+L lead-time window"). Threshold T and lead-time L
   are pre-registered, not chosen post-hoc on the unseen-window
   data.
4. **Outcome operationalisation** (the same outcome definition the
   tier-2 evidence rests on — no operationalisation switch at the
   forward-validation step, which would smuggle a different
   construct into the predictive claim).
5. **Verdict criteria** — SUPPORTED if PPV ≥ pre-registered floor
   AND lead-time matches pre-registration AND reliability bound
   computable. PARTIAL / INCONCLUSIVE / REJECTED per the
   project's standard verdict-labelling discipline (the verdict
   choice rules from [`personal_hypotheses.md`](../personal_hypotheses.md)).
6. **Pre-registration lock date** — before the prediction window
   begins. The lock date is the anti-cherry-pick discipline at the
   tier-3 evidence floor.
7. **PPV floor anchoring discipline** — the pre-registered PPV
   floor (named in element 5 verdict criteria) is anchored at the
   relevant base rate **by default** (the null base rate that the
   prediction rule must exceed to demonstrate predictive value
   over chance); when the cross-op tier-2 evidence produced a
   point estimate, the floor MAY instead anchor **at or above the
   tier-2 point estimate** (the prediction rule must demonstrate
   predictive value on unseen days that meets or exceeds the
   in-sample tier-2 evidence). **Hard rule**: the floor CANNOT be
   set at or below the null base rate without justifying-the-
   tier-3-question-itself — doing so backdoors the §3.10 gate via
   a trivially-passable floor (any signal correlated above zero
   would "pass"). The forward-validation HA pre-reg MUST cite
   which anchor the floor uses (null base rate, OR tier-2 point
   estimate, OR a higher floor) with one-sentence rationale.

**Worked-example sketch — K-stress-fatigue-monitoring forward-
validation HA shape.** Target: K-stress-fatigue-monitoring;
predictor `all_day_stress_avg`; outcome next-day `gevoelscore`.
Prediction window: ~90-day Stratum 4 unmedicated window starting
after HA lock. Prediction rule: when stress falls within the
inverted-U-peak bin (per HA-C3p's personal-baseline bins), predict
next-day gevoelscore falls within corresponding-bin's historical
mean ± 1 SD on D+1. Verdict criteria: SUPPORTED if PPV ≥ pre-
registered floor; PARTIAL if floor met only on same-day D+0
correspondence (which is tier-1, not tier-3); REJECTED otherwise.
**PPV floor anchoring** (per element 7): the floor anchors at the
**uniform-three-bin null base rate (~0.33)** — the prediction rule
must demonstrate PPV materially above chance for the three-bin
classification. Lock date: must precede window start.

**Worked-example sketch — K-bout-recovery-signal forward-validation
HA shape.** Target: K-bout-recovery-signal; predictor
`bout_n_did_not_return_day` cross-phase pooled; outcome crash-day
within N-day window. Prediction window: ~180-day cross-phase
pooled window starting after HA lock. Prediction rule: when signal
exceeds heavy-T threshold T on D, predict crash-day within D+0 to
D+L (L pre-registered per C-bout-substance's S₁ mechanism
evidence). Verdict criteria: SUPPORTED if PPV ≥ pre-registered
floor; REJECTED otherwise. **PPV floor anchoring** (per element 7):
the floor anchors **at or above the cross-op tier-2 evidence point
estimate** (Cliff's δ = +0.120 and +20.26 pp discrimination per
map r3 §5 + HA-C4c — translated into a PPV equivalent against the
~2/year residual-crash base rate per RESEARCH-REPORT §5.2). The
prediction rule must demonstrate predictive value on unseen days
that meets or exceeds the in-sample tier-2 evidence; a trivially-
passable floor at the bare ~0.4% base rate is forbidden as it
would not distinguish tier-3 from a coin-flip. Lock date: must
precede window start.

Both sketches are illustrative; the exact PPV-floor numeric value
belongs in the actual pre-reg, but the **anchoring choice** (null
base rate vs tier-2 point estimate vs higher floor) MUST be made
at pre-reg time per element 7 above, not deferred to interpretation.

### 5.6 Section 6 — `open_inputs` block

Per locked-plan §3.5. Each entry names: (1) what is missing —
forward-validation HA pre-reg, PPV-base-rate computation, sister-
HA for tier-2 cross-operationalisation replication, topic-level
positioning that the construct's tier evidence depends on; specific
paths / proposed pre-reg slot names, not vague "more evidence";
(2) what it is blocking — typically the tier promotion to the next
higher tier (with the named target tier in the entry), sometimes a
constituent tier-evidence-condition gap that caps the construct
below its aspiration; (3) cheapest acquisition path — forward-
validation HA pre-reg draft (with `hypothesis_lock_process.md`
routing), PPV-base-rate computation script, sister-HA pre-reg
shape, upstream `topic-*.md` re-examination via Stage S₂ drift; (4)
**the fallback tier** the artefact has therefore been capped at —
this is the §5.6-specific framing per the §6.5 spec brief: the
user sees exactly what acquiring the missing input would unlock.

**Construct-specific refusal-to-proceed paths** produce
`open_inputs` entries (per §3.5):

1. **Feeding `topic-*.md` missing/unlocked** → halt; entry: "S₂
   topic-`<id>`" missing → "Stage A on construct-`<id>`" blocked
   → "run `/research-interpret contextualise topic-<id>`" →
   fallback "none."
2. **Construct not in map** → halt; entry: "map row for
   construct-`<id>`" missing → "producer-mode map-update per
   §3.6" → fallback "none." Same as §6.5 map-change halt.
3. **Tier-3 wanted but forward-validation HA missing** → proceed
   at tier-2 (or tier-1 if tier-2 also fails); entry: §5.5 HA
   shape → tier-3 blocked → "draft forward-validation HA pre-reg
   per `hypothesis_lock_process.md`; lock before window; run
   window; verdict on result.md" → fallback "tier-2 informative-
   pattern" (or tier-1 if PPV-uncomputable also fires).
4. **Tier-2 wanted but PPV cannot be computed** → proceed at
   tier-1; entry: missing base-rate computation OR sparse outcome
   cell → tier-2 blocked → "era-stratified descriptive base-rate
   run per §3.9 — NOT cross-era aggregation; OR more outcome
   events if cell sparse for structural reasons" → fallback
   "tier-1 monitoring."
5. **Constructed-claim cannot pass §3.10 base-rate framing** →
   proceed at tier-1 with claim re-cast in monitoring frame;
   entry: typically outcome base rate not stable within era →
   tier-2 blocked → "find era where base rate stable AND tier-2
   association replicates, OR accept tier-1 frame" → fallback
   "tier-1 monitoring."

The skill aggregates §5.6 `open_inputs` entries into the layer-wide
[`_open_inputs.md`](_open_inputs.md) queue.

**Distinct from `open_inputs`** (per locked-plan §3.5 vs §3.11):
`open_inputs` is "what is missing to complete *this current tier
claim*"; §5.8 follow-up suggestions are "what *next claims* could
be built — for us or for others." Both required.

**Open inputs do not block completion** per locked-plan §3.8.
Exception: the five refusal-to-proceed paths above produce only
the `open_inputs` entry; the construct artefact itself is not
drafted when refusal-paths 1 or 2 fire, and is drafted at the
fallback tier when refusal-paths 3 / 4 / 5 fire.

### 5.7 Section 7 — Predictive-quality measures per §3.10

**Required at tier-2 and tier-3.** Per locked-plan §3.10, the
quality-measures section reports PPV + base rate in the RESEARCH-
REPORT §5.2 plain-language frame ("right N out of M when it fires"
/ "wrong M-N out of M when it fires"). Optional measures (NPV,
sensitivity, specificity, false-alarm rate, lead time, reliability)
are encouraged at tier-2 and required at tier-3 for lead time and
reliability per §3.10 tier-3 discipline.

**The §5.2 precedent.** *"The positive predictive value of any such
alert, even computing optimistically from H02b's train-window
evidence, is ~4% at the residual-crash base rate of ~2 per year. A
predictive alert card would be wrong 24 times out of 25."* The
frame is number + what-it-means-in-everyday-frequencies. Bare
percentages without the base-rate context are forbidden per §7.4
anti-pattern.

**Required at tier-2+** (one paragraph each):

1. **PPV** — when the signal fires, the outcome follows N out of M
   times. Plain-language frame: "right N out of M when it fires" /
   "wrong M-N out of M when it fires." Cited against base rate.
2. **Base rate** — per-era base rate (events per year in the
   relevant era; per §3.9 — NOT aggregated across eras). Bare PPV
   without base rate is forbidden per §3.10 + §7.4.
3. **Plain-language combined frame** — the §5.2 style: "PPV is N%
   at the base rate of M events per year; when it fires it's right
   K out of L times in a world where L events happen per year."
   The wording the subject reads, not the bare PPV.

**§7.4 anti-pattern enforces.** Bare-percentage actionability
without the combined plain-language frame is forbidden per §7.4;
items 1-3 above are the construct-level operationalisation of the
§7.4 prohibition. The binding loop closes: §3.10 layer rule → §5.7
required outputs → §7.4 anti-pattern enforcement at lock-gate.

**Optional at tier-2; required-where-noted at tier-3:**

4. **NPV** — when signal is quiet, outcome correctly does not
   follow N of M times. "No alarm = no concern" reasoning;
   base-rate bound.
5. **Sensitivity** (TPR) — fraction of real events the signal
   catches. Per §5.2: sensitivity 0.95 + PPV 0.04 means false-
   alarm dominance operationally.
6. **Specificity** (TNR) — fraction of non-events the signal
   correctly stays quiet on. Cited with false-alarm rate.
7. **False-alarm rate** — (1 − specificity) in everyday
   frequency. "Out of M non-event days, signal fired on K."
8. **Lead time** (REQUIRED at tier-3 per §3.10) — how far in
   advance ("a day" / "an hour" / "in the moment"). A tier-3
   forecast without lead time is operationally meaningless.
9. **Reliability** (REQUIRED at tier-3 per §3.10) — test-retest
   stability across similar days. A tier-3 forecast without
   reliability bound has no defence against random-walk artefacts.

**§3.10 conflict rule applied here.** If PPV-with-base-rate cannot
be computed at tier-2+ (no clear denominator, sparse outcome cell,
base rate not stable within an era), the tier downgrades to tier-1
(monitoring) per §3.10 conflict rule. The §5.6 `open_inputs` block
logs the missing base-rate computation; the §5.2 evidence-layer
section records the tier downgrade. **The skill never lets an
uncalibrated quasi-predictive claim pass with hedged wording** —
this is the load-bearing discipline at §5.7.

**Forbidden at the HA-test level (per `personal_hypotheses.md` §32),
required at the actionability layer.** Diagnostic measures (PPV,
NPV, sensitivity, specificity, false-alarm rate, lead time,
reliability) stay OUT of HA pre-regs and HA `result.md` files
(classifier-discrimination measures are forbidden at the HA test
level per the personal_hypotheses §32 binding). They ENTER only at
Stage A, where the question is "how usable is this signal in life,"
not "is the underlying relationship real." The HA layer
establishes reality; Stage A measures usability. This is the
locked-plan §3.10 binding restated at the per-stage level; §7.10
anti-pattern below enforces.

**Worked example — K-bout-recovery-signal §5.7** (tier-2 claim per
§4.2 example; if PPV computes against residual-crash base rate):

> *PPV*: when `bout_n_did_not_return_day` exceeded the heavy-T-day
> threshold in past cross-phase pooled data, a crash day followed
> within the observation window N out of M times. [Stage-A-time
> computation against cross-phase pooled cell.]
>
> *Base rate*: ~2/year residual per RESEARCH-REPORT §5.2; per-era
> base rates reported separately where pooling crosses an era
> boundary the base rate is not stable across (§3.9 binding).
>
> *Plain-language combined frame*: "When the bout-recovery signal
> fires, a crash day followed within the window N out of M times
> in past data; crash days occur about 2 per year residual. 'Fires'
> events are infrequent; predictive value depends sensitively on
> base-rate stability — per RESEARCH-REPORT §5.2 precedent." [Stage
> A fills N/M from the source HA's `result.md`.]
>
> *Lead time / reliability*: NOT specified at tier-2 (both tier-3-
> required per §3.10).

If PPV-with-base-rate does NOT compute, §3.10 conflict rule fires:
tier downgrades to tier-1; §5.6 logs missing computation; §5.3
claim re-cast as tier-1 monitoring; downgrade explicit, NOT
disguised as hedged tier-2.

### 5.8 Section 8 — Follow-up suggestions (own + external tracks)

Per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3.11, every reviewer-mode-with-authorization artefact closes with
**Follow-up suggestions** in two tracks. Stage A's per-stage shape
per the locked-plan §3.11 "Stage A" row:

- **Own-research track** — the forward-validation HA pre-reg shape
  from §5.5 above, framed here as the own-research follow-up for
  tier-3 promotion (the cross-reference to §5.5 makes the two
  sections consistent — §5.5 carries the shape spec; §5.8 routes it
  as own-research). Plus own-research pre-regs that would tighten
  the §5.7 quality measures (e.g., a sensitivity-vs-specificity
  tradeoff test at a different threshold; an era-restricted base-
  rate computation; a reliability descriptive run for the same
  signal across similar-day pairs). Each entry is one paragraph:
  proposed pre-reg shape; what tier promotion or quality-measure
  tightening it would unlock; the routing through
  [`hypothesis_lock_process.md`](hypothesis_lock_process.md).
- **External-research track** — intervention or RCT studies that
  could test causality (vs the association the corpus can observe);
  group-level studies that could establish a population-level base
  rate to compare ours against; clinical-instrument studies that
  could validate the Garmin-derived signal against a gold-standard
  measurement. Per locked-plan §3.11 binding scoping discipline:
  **every external-research suggestion MUST explicitly name the N=1
  limit** (per
  [`research_line_limitations.md`](research_line_limitations.md) §3)
  that prevents us from answering the question ourselves. Scoping
  cites the relevant L-ID from §5.11 (typically L1 for group-level
  confirmation studies; L4 for blinding-required designs including
  intervention RCTs; L3 for cross-instrumentation validation).

Each entry is one paragraph: proposed study; L-ID(s) preventing
self-answer; what the study would contribute to the construct's
tier evidence or quality measures.

**Worked-example sketches** for the two active constructs:

- *K-stress-fatigue-monitoring* — own: §5.5 forward-validation HA
  for tier-3; third sister-HA on rolling-window-baseline binning
  to tighten C-stress-fatigue-shape's cross-bin-scheme
  independence; era-restricted descriptive run computing the
  inverted-U-peak base-rate for the medicated Stratum 4 cell.
  External: PEM-pacing cohort study testing the inverted-U at
  group level (L1-scoped); intervention study randomising stress-
  load against gevoelscore (L4-scoped).
- *K-bout-recovery-signal* — own: §5.5 forward-validation HA for
  tier-3; unmedicated-only sister-HA on
  `bout_n_did_not_return_day` to move comparability toward
  COMPARABLE on era dimension (L2); reliability descriptive run
  on the signal across similar-day pairs. External: CPET-based
  bout-recovery study in a comparable LC cohort (L1 + L3 scoped);
  intervention RCT testing within-day rest as a recovery modifier
  (L1 + L4 scoped).

### 5.9 Section 9 — Optional subject-narrative commentary (§3.12)

**Per §3.12:** commentary is OPTIONAL. It may attach to a tier-1
or tier-2 formal claim per the construct's map r3 §5 eligibility
status. It does NOT attach to tier-3 (tier-3 carries forward-
validation HA evidence; §7.14 anti-pattern enforces). When
skipped: "Commentary skipped at this Stage A time" + one-line
rationale. When filled: §3.12 discipline in full.

**Required discipline when filled** (per §3.12):

1. **Cite the attached claim.** Opens with one line: "attached
   to: K-XXX tier-N claim per §5.3". Scope-bounded; not floating.
2. **Subject-attribution every sentence.** "I", "the subject",
   "in this subject's experience", "in my experience", "I
   notice", "in retrospect". Bare third-person assertion ("the
   signal means X") forbidden.
3. **Permitted language** (per §3.12): "I notice", "in my
   experience", "in retrospect", "I sometimes", "the pattern
   hints at / suggests-not-confirms / reads as", "worth
   attention", "I lean toward". Floor only; equivalent subject-
   attributed-hint shapes also permitted.
4. **Forbidden language** (per §3.12): "predicts", "forecasts",
   "will happen", "tomorrow", "X means Y", "this signals
   that...", any causal-claim or forecast-claim wording. Non-
   negotiable; reverted before lock.

**Hard separations** (these keep the §3.10 gate inviolable, per
§3.12):

1. **Cannot promote tier.** Rich commentary stays at the formal
   tier; only a pre-registered forward-validation HA per §3.10
   unlocks tier-3. §7.8 enforces.
2. **Cannot be cited as evidence** in HAs, interpretations,
   syntheses, contextualisations, or research-audience
   translations. Patient-audience translation track only per
   the map's §5 note. §7.9 enforces.
3. **Cannot float unattached.** Every commentary section
   attaches to a formal claim. "Subject suspects a thing nobody
   tested" belongs at §5.8 follow-up as a candidate own-research
   HA. §7.7 enforces.
4. **Forbidden in research-audience translation track** per
   locked decision. Guide #6 (Stage T) routes commentary to
   patient-audience track only.
5. **Layperson-test propagation** (per §3.12 + §6.6). If
   commentary fails the layperson test at Stage T downstream
   (e.g., "I lean toward resting on those days" read as soft
   prediction), the commentary is revised before lock; revision-
   trigger is the layperson's actual interpretation. Propagates
   back to §5.9 per §3.7 drift.

**Worked example — K-stress-fatigue-monitoring §5.9 commentary**
(tier-1 monitoring claim per §4.1; commentary-eligible per map r3
§5):

> *Attached to: K-stress-fatigue-monitoring tier-1 claim per §5.3.*
>
> I notice that on days where my Garmin all-day stress sits in
> the mid-band (~30-40), my gevoelscore tends to land in the
> higher third more often than I'd guess from the low-stress
> bands alone — the pattern hints at the inverted-U the HAs
> detected. In retrospect, very-low-stress days were often "I'm
> conserving everything" days where the gevoelscore was lower
> than a simple low-stress = high-gevoelscore relationship would
> suggest. I lean toward treating Garmin stress as a daily
> reflection-prompt rather than a forecast input.

Every sentence carries subject-attribution ("I notice"; "in
retrospect"; "I lean toward"). No forbidden wording. Commentary
attaches to the tier-1 claim.

**Worked example — K-bout-recovery-signal §5.9 commentary** (tier-2
informative-pattern claim per §4.2, assuming PPV computes;
commentary-eligible per map r3 §5):

> *Attached to: K-bout-recovery-signal tier-2 claim per §5.3.*
>
> In my experience, when the bout-level Garmin signal shows
> repeated failure-to-return on a heavy-task day, I sometimes
> notice a crash within the next several days — but the
> association is one I read in retrospect, not a forecast I act
> on in the moment. The RESEARCH-REPORT §5.2 base-rate framing
> matches my felt sense: crash days are rare enough that the
> signal "firing" is itself rare. I lean toward treating the bout
> signal as a "post-hoc honesty check on what kind of day that
> was" rather than an actionable prospective alert.

### 5.10 Section 10 — Open downgrades from review

Per the locked-plan §4 producer/reviewer split table row for
actionability-tier-claim artefacts: "Skill-driven, with **hard
gate** / Fresh-session `/research-review`; tier downgrades on
review concerns." Stage A's `/research-review` pass may surface
review concerns that downgrade the tier; this section gets filled
at review time with the per-concern downgrade.

When no downgrades fire: "No open downgrades from review at this
lock cycle." When downgrades fire: one paragraph per concern,
naming the concern, the tier-evidence-condition it identifies as
unmet, and the resulting tier downgrade (typically tier-2 → tier-1,
or tier-3 → tier-2). The downgrade is recorded; the §5.2 evidence
layer + §5.3 tier claim + §5.6 `open_inputs` + §5.7 quality
measures are updated to reflect the downgraded tier.

**Downgrade-mechanics rule book.** Per §6 conflict rules: **§6.1**
governs tier-condition-unmet downgrades (typically tier-2 → tier-1
when cross-op evidence or PPV-with-base-rate fails); **§6.2**
governs forward-validation-HA-REJECTED downgrades (tier-3 → tier-2,
with the §5.5 forward-validation HA shape addendum recording the
REJECTED verdict + the original tier-2 evidence inherited);
**§6.4** governs commentary-vs-evidence conflicts (no tier change;
commentary is revised per §3.12 binding to remove any wording that
implied stronger evidence than the tier supports). The §5.10
review-time fill records the per-concern downgrade with the §6
conflict-rule reference.

This section is **filled at `/research-review` time** (per the
locked-plan §4 row), NOT at drafting time. The draft carries an
empty §5.10 placeholder; the review pass produces the §5.10 entries
if any fire.

### 5.11 Section 11 — L-ID citation block (all seven)

Per [`research_line_limitations.md`](research_line_limitations.md) §5
row for `construct-*.md`: **MUST cite all seven L-IDs with explicit
applicability-or-NA per limitation.** This section is the binding
L-ID citation block at the construct level.

Each L-ID is one paragraph: opening "Cites L`<N>` (`<short name>`):"
line plus one sentence applying the limitation to *this construct's
specific tier claim* — OR "L`<N>` NA: `<one-sentence project-
specific reason from the map's §5 L-ID-notes column>`". All seven
appear; silent omission is forbidden per the §3 hard rule.

**Worked-example sketch for K-stress-fatigue-monitoring** (map r3
§5 row L-IDs; all seven cited with applies-or-NA):

> *Cites L1 (single-subject reach):* tier-1 monitoring claim is
> within-subject correspondence across Stratum 4 unmedicated; per
> Daza 2018, does not generalise to "people like me"; §5.8 names
> the group-level study.
>
> *Cites L2 (era confounds):* scope bounded to Stratum 4
> unmedicated per the feeding topic's positioning (guide #4 §4.7
> T-stress-fatigue-pacing example); cross-era projection out of
> scope.
>
> *Cites L3 (device generations):* rests on FR245 Elevate V3
> `all_day_stress_avg`; device upgrade triggers §3.7 drift re-
> examination per limitations doc r3 §7.
>
> *Cites L4 (analyst-is-subject):* HA-C3 v2 + HA-C3p both pre-
> registered with Wiggers convex-cost prior; L4 mitigation reach
> is fresh-session `/research-review` + §5.10 review-time tier-
> downgrade gate; advice forms forbidden per §5.4 + §7.2 because
> L4 prevents the intervention-study design advice would require.
>
> *L5 NA:* feeding cluster C-stress-fatigue-shape has no v24
> primary signals per map §3; tier-1 claim does not touch any
> presence-conditioned derivative.
>
> *Cites L6 (self-reporting):* gevoelscore is the outcome; the
> tier-1 claim respects the subjective-reporting noise floor —
> works at bin-level range, not per-point.
>
> *Cites L7 (survivorship):* HA-C3 v2 + HA-C3p gate on
> `all_day_stress_avg` non-NaN and `gevoelscore` non-NaN within
> Stratum 4 unmedicated; effective coverage is the gated subset;
> ungated days out of scope.

**Worked-example sketch for K-bout-recovery-signal** (map r3 §5
row L-IDs; all seven cited with applies-or-NA):

> *Cites L1:* tier-2 informative-pattern claim (if PPV computes
> per §5.7) is within-subject association across cross-phase
> pooled cell; per Daza 2018, does not refute group-level
> consensus on within-day recovery impairment (guide #4 §4.7
> T-within-day-recovery example, topic AGREES with consensus on
> direction within COMPARABLE bound); §5.8 names the CPET-based
> group-level study.
>
> *Cites L2:* scope is cross-phase pooled per HA-C4c's primary
> operationalisation; cross-phase pooling carries explicit
> warrant + per-phase reporting + `citalopram_phase_
> stratification.md` §5 correction discipline (all in HA-C4c);
> §5.8 own-research names the unmedicated-only sister-HA that
> would move comparability toward COMPARABLE on era dimension.
>
> *Cites L3:* rests on FR245-derived bout signal
> (`bout_n_did_not_return_day`); device upgrade triggers §3.7
> drift re-examination.
>
> *Cites L4:* HA-C4c pre-registered with Wiggers within-day-
> recovery prior; L4 mitigation reach is fresh-session
> `/research-review` + §5.10; cross-phase pooling itself is an
> L4-aware methodology choice (pooling chosen to address a prior,
> not maximise effect size).
>
> *L5 NA:* C-bout-substance has no v24 primary signals per map §3.
>
> *L6 NA:* gevoelscore not in C-bout-substance's primary cell per
> map §5 (primary cell uses `exertion_class_lagged_lcera` +
> `bout_n_did_not_return_day`; gevoelscore enters only as
> caveat/sensitivity at upstream HA); tier-2 claim does not rest
> on gevoelscore as outcome.
>
> *Cites L7:* HA-C4c gates on cross-phase pooled cell + heavy-T
> classifier coverage; effective coverage is the gated subset;
> §5.8 own-research names the unmedicated-only sister-HA that
> would test the gating's downstream effect.

**Hard rule.** Artefact missing any of L1-L7 cannot be locked
(§9.6). Artefact silently omitting an L-ID without project-
specific NA-with-justification cannot be locked.

### 5.12 Section 12 — Cross-references

Links out to:

- Each feeding `topic-*.md` (the inputs the construct artefact
  was built on).
- The synthesis-structure map's §5 construct row (the structural
  pre-registration row reference; the tier-aspiration cell; the
  §3.12 commentary-eligibility status; the L-ID notes column —
  all binding inputs to this artefact).
- The synthesis-structure map's §3 cluster rows the topics roll
  up from (upstream chain reference for downstream reader-
  traceability).
- The synthesis-structure map's §4 topic rows the construct feeds
  from (the same as the first bullet but cited via the map for
  the topic-construct rollup).
- The contributing `cluster-*.md` files via the topic chain
  (upstream chain reference).
- The forward-validation HA's `hypothesis.md` and `result.md`
  (where one exists for tier-3 promotion).
- Limitations doc cross-refs for cited L-IDs (per §5.11; all
  seven L-IDs cite).
- [`RESEARCH-REPORT.md`](../RESEARCH-REPORT.md) §5.2 (the PPV-with-
  base-rate precedent that §5.7 cites; explicit cross-reference
  required when §5.7 quality measures are produced at tier-2+).
- The locked plan §3.5 (missing-inputs flagging); §3.6 (map
  conflict-resolution rule + §6.5 below); §3.7 (drift policy);
  §3.8 (completion criteria); §3.9 (limitations binding); §3.10
  (hard predictive gate — the load-bearing constraint of this
  guide); §3.11 (follow-up suggestions); §3.12 (commentary
  layer — the binding rule for §5.9); §4 (producer/reviewer
  split table); §6.5 (the spec brief this guide implements).
- Guide #1 [`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
  for the upstream-most verdict-trust chain; guide #2
  [`verdict_to_inference.md`](verdict_to_inference.md) for the
  upstream licensed-claim chain; guide #3
  [`internal_synthesis.md`](internal_synthesis.md) for the
  upstream coherence-call chain; guide #4
  [`external_contextualisation.md`](external_contextualisation.md)
  for the immediate upstream positioning chain.
- [`hypothesis_lock_process.md`](hypothesis_lock_process.md) for
  the forward-validation HA pre-reg discipline (§5.5 + §5.8
  own-research routing).
- [`personal_hypotheses.md`](../personal_hypotheses.md) §32 for
  the HA-test-level prohibition on classifier-discrimination
  measures (§5.7 cites for the stay-out-of-HA-pre-reg binding).
- Literature methodology anchors: Daza 2018 for N-of-1-to-group
  reach (cited at §5.11 L1 worked example); CENT 2015 for
  generalisability framing; SCRIBE 2016 for L4 transparency;
  Natesan 2023 for defensibility bar.

## 6. Conflict rules

Per the §6.5 spec brief and the §3.10 + §3.12 + §3.6 layer
bindings, Stage A's conflict rules:

### 6.1 Tier requirements unmet → tier downgrades

> Tier requirements unmet → tier downgrades. User cannot override
> the downgrade by asserting confidence; the gate is structural.

Per locked-plan §6.5. If §5.2 identifies a tier-condition gap
(topic CANNOT-SAY blocks tier-1; cross-op independence fails
blocks tier-2; PPV-with-base-rate uncomputable blocks tier-2),
the tier downgrades to the next-lower met floor. §5.6 logs what
would unlock the higher tier; §5.2 + §5.3 update to the
downgraded tier.

### 6.2 Forward-validation HA REJECTED → predictive claim removed

> Forward-validation HA REJECTED → predictive claim is removed;
> the construct caps at informative pattern.

Per locked-plan §6.5. If a forward-validation HA that earned
tier-3 is re-examined (per §3.7) and produces REJECTED, the
predictive claim is **removed** and the construct caps at tier-2
(or tier-1 if tier-2 also fails). §5.10 records the downgrade;
§5.3 rewrites in tier-2 wording; §5.5 records the additional
forward-validation HA shape that would re-attempt tier-3 (if
user chooses). Per §3.10: the gate is non-negotiable for
promotion AND for maintenance — tier-3 evidence must remain
SUPPORTED at every drift re-examination; no tier-3 inertia.

### 6.3 Lived-experience prior without forward-validation HA

> Lived-experience prior says "reliable for me" without forward-
> validation HA → recorded but does not promote the tier.

Per locked-plan §6.5. A feeding `interpretation.md` §6 prior
that says "reliable for me as a daily forecast" without a
forward-validation HA is recorded as a §5.9 commentary candidate
(subject to §3.12) and a §5.8 own-research follow-up (the prior
motivates the pre-reg). Does NOT promote the tier. Per §3.12:
commentary cannot promote tier; only forward-validation HA
unlocks tier-3.

### 6.4 Commentary-vs-forward-validation conflict

When §5.9 commentary content would, if read as analytical input,
suggest a higher tier than §5.2 earned: commentary stays at
language-bounded form per §3.12, tier stays at §5.2 level. The
two epistemic categories (patient-facing nuance vs research-
defensible claim) do not arithmetic-combine. If commentary
surfaces a candidate own-research HA the §5.8 track missed, the
candidate is added to §5.8 (routing through
`hypothesis_lock_process.md`); commentary does not double as
own-research entry.

### 6.5 Map-change-needed (§3.6 conflict-resolution rule)

> Halt the Stage A session immediately. Do NOT edit the map in-
> session. Route the proposed change to a separate producer-mode
> map-revision session with its own `/research-methodology-review`
> pass before re-lock.

Per locked-plan §3.6 (the same rule guides #3 §6.1 and #4 §6.1
operationalise at Stages S₁ and S₂). When per-construct Stage A
work reveals the map needs changing, Stage A HALTS and routes to
a separate map-revision session.

**Concrete halt-criteria.** Stage A halts when any of these
surfaces:

1. **A feeding topic's positioning lands the topic on a different
   construct** than the map's §5 row's topics-feeding cell
   declares.
2. **The construct's tier evidence would require evidence from a
   topic not in the map's §5 row** — either the topic belongs in
   this construct's feeding, or the construct membership needs
   another topic.
3. **The construct's tier aspiration in the map's §5 row is
   incompatible with the §5.2 evidence layer** — e.g., the map
   declares tier-2 aspiration but the §5.2 evidence layer
   identifies that tier-2 is structurally unreachable (no cross-
   operationalisation independence possible because the cluster
   has only single-operationalisation evidence); the map's
   aspiration ceiling needs revising.
4. **The §3.12 commentary-eligibility status in the map's §5 row
   is wrong** — e.g., the map declares commentary-eligible but
   the §5.2 evidence layer earns only tier-3 (commentary not
   eligible at tier-3 per §3.12 hard separations); OR the map
   declares commentary-not-eligible but the §5.2 evidence layer
   earns tier-1 or tier-2 (commentary-eligible per the §3.12
   binding). The map needs to be re-evaluated for the construct.

**Route-out instructions.** Stop drafting mid-session; do NOT
save a partial artefact; do NOT edit the map in-session. Produce
only the §5.6 `open_inputs` entry naming the proposed map change.
Hand off to the user with the halt-criterion that triggered and
the proposed change. Resume only after a separate producer-mode
session updates the map with its own `/research-methodology-
review` pass before re-lock. The why-this-rule rationale guide
#3 §6.1 and guide #4 §6.1 carry applies here verbatim at the
construct level.

## 7. Anti-patterns explicitly forbidden

The following moves are forbidden in any Stage A actionability
translation. One paragraph each per the brief's density-discipline
guidance.

### 7.1 Promoting retrospective fit to predictive claim

Per locked-plan §6.5 + §3.10: retrospective-only fit does NOT
license a predictive claim. Predictive claims require a pre-
registered forward-validation HA locked before the prediction
window, predicting on unseen days, with a SUPPORTED verdict.
Reading high past-data PPV as forecast is the most common path to
overclaim; the gate is what prevents it. The locked plan §9
names this the "actionability-by-narration fallacy" at tier-3.
No exceptions for "the signal is too good to require forward-
validation" — that is precisely the wording the gate refuses.

### 7.2 Framing actionability as advice

Per locked-plan §6.5: actionability claims are NOT advice. The
artefact licenses what the subject may safely **say about the
signal**, not what to **do** with it. Advice ("you should...",
"rest when X drops") carries causal-mechanism assumption the tier
evidence does not license (tier-1 descriptive, tier-2 association,
tier-3 forecast — none causal-mechanism). Per L4: advice would
require intervention-study methodology with comparator arm and
blinding the research line cannot run on itself; §5.8 external-
research names the intervention RCT.

### 7.3 Collapsing presence-conditioned signals into prevalence

Per locked-plan §6.5 + §9: any v24-derived signal carries
presence-conditioned semantics per L5 — absence in notes does NOT
mean absence of experience. Tier-claim wording that collapses a
presence-conditioned signal into prevalence ("symptom occurs N%
of days when [signal X] fires") is forbidden. Both active
constructs in map r3 cite L5 NA; future v24-using constructs
must bind this anti-pattern at §5.11 L5 paragraph with the
presence-conditioned semantics explicit.

### 7.4 Bare-percentage actionability (locked-plan §9)

"PPV is 60%" with no denominator is meaningless. "PPV is 60% at a
5% base rate; right 3 in 5 when it fires, fires about once a
month" is informative. RESEARCH-REPORT §5.2 *"wrong 24 times out
of 25"* is the load-bearing model. §5.3 + §5.7 carry the frame
consistently; §7.4 ensures the frame is not stripped at the
wording-rephrasing step.

### 7.5 Backdoor predictive claims via wording

Per locked-plan §6.5 + §9: wording that reads predictive while
claiming only "monitoring" or "informative pattern" tier is
forbidden. "Watch for X" can be predictive in disguise; "track X"
is the monitoring frame; "X has historically appeared alongside
Y" is the informative-pattern frame. The §3.10 gate applies to
**the wording**, not just to the tier-label: tier-1 wording with
predictive content is structurally a tier-3 claim per the gate,
which requires the forward-validation HA the tier-1 claim does
not have. §4 permitted-wording lists per tier carry the
discipline.

### 7.6 Inventing new caveats post-hoc

Caveats in §5.4, §5.10, §5.11 come from the locked upstream
chain (feeding topic; cluster; member HAs; limitations doc §3;
map's §5 L-ID notes). New caveats invented at Stage A — neither
in the upstream chain nor in the limitations doc — are forbidden.
If Stage A identifies an upstream-missing caveat, the guide #4
§7.6 routing applies (the caveat surfaces as a Stage S₂ gap and
triggers re-examination per §3.7); it does not enter the
construct artefact through Stage A prose. **Exception**: §5.4
tier-specific overclaim refusals may add tier-specific categories
the upstream chain could not produce (no tier claim existed
yet); these are not "new caveats" in the §7.6 sense.

### 7.7 Bare-narrative-as-actionability (commentary-floats-unattached)

Per locked-plan §9. Using §3.12 commentary wording to escape the
§3.10 gate is forbidden. Variant: "we couldn't claim prediction,
but the subject's narrative shows the signal is predictive in
lived experience..." — backdoor predictive claim through
commentary language, exactly the slippage §3.12 prevents. §5.9
discipline + §3.12 hard separations enforce: commentary attaches
to a formal tier-1 / tier-2 claim; cannot float unattached;
permitted wording only. "In my experience this predicts..."
breaks both §3.12 forbidden-wording AND §7.7 at the same time;
reverted before lock.

### 7.8 Commentary-promotion fallacy

Per locked-plan §9. Letting accumulated commentary across lock
cycles justify tier promotion without forward-validation HA is
forbidden. Variant: "we've seen this pattern hold up across three
commentary rounds; that's evidence" — no, that's retrospective
consistency of the subject's own narrative, which L4 and §3.10
both caution against treating as analytical evidence. Tier
promotion requires forward-validation, not narrative durability;
§6.4 operationalises.

### 7.9 Downstream-citation-of-commentary fallacy

Per locked-plan §9. Citing §3.12 commentary content in HA
`result.md` / `interpretation.md` / `cluster-*.md` / `topic-*.md`
/ research-audience translation as if it were analytical input or
finding is forbidden. Commentary is patient-facing nuance, not
research evidence; citing it downstream blurs the epistemic
categories §3.12 keeps separate. Stage A's `construct-*.md` is
the **one place commentary lives in research artefacts**, and
even there it is attached-and-bounded per §3.12.

### 7.10 Computing predictive-quality measures at the HA-test level

Per locked-plan §3.10 + `personal_hypotheses.md` §32. Diagnostic
measures (PPV / NPV / sensitivity / specificity / false-alarm
rate / lead time / reliability) stay OUT of HA pre-regs and
`result.md` files; they enter only at Stage A. A future HA pre-
reg that wants to compute PPV at HA-test level is forbidden.
Reverse — Stage A tier-2+ artefact WITHOUT §3.10 quality measures
— is forbidden per §5.7 + §6.1. Two-direction discipline: HA-test
= reality of relationship; Stage A = usability of relationship in
life.

### 7.11 Treating single HA as enough to license a tier-1 claim

Per locked-plan §6.5. A single HA does NOT license tier-1 by
itself; tier-1 requires the cluster-level S₁ coherence call AND
the topic-level S₂ positioning with comparability passed. Both
active constructs in map r3 have ≥2 constituent HAs per their
feeding cluster (C-stress-fatigue-shape: HA-C3 v2 + HA-C3p;
C-bout-substance: HA-C4c with C-bout-framework cascade-
precondition). Future single-HA-cluster constructs require the
"single-member trivial-CONCORDANT" qualifier (guide #3 §5.6) AND
topic positioning at AGREES / EXTENDS / DIVERGES (not CANNOT-SAY)
for the tier-1 claim to land.

### 7.12 Inventing new tier labels

The three-tier set is exhaustive. Labels like "weak monitoring",
"strong informative pattern", "soft predictive", "tier-1.5" are
forbidden. If no tier fits cleanly, the call defaults to the
next-lower tier (conservative default, analogous to guide #3
§4.4 default-to-CONFLICT and guide #4 §4.5 default-to-CANNOT-
SAY). New labels would weaken the §3.10 gate by introducing
intermediate-tier wording the gate cannot enforce.

### 7.13 Re-routing topics to different constructs in-stage

The §3.6 map is authoritative for construct membership. Stage A
does NOT propose membership changes in-stage; §6.5 halt-and-route
rule applies if work reveals re-mapping need. Editing the map
in-session (or silently treating a topic as if in a different
construct) is forbidden. Construct-level analogue of guide #3
§7.1 and guide #4 §7.11.

### 7.14 Producing §3.12 commentary at a tier-3 construct

Per §3.12 hard separations: commentary cannot attach to tier-3
claims. A tier-3-earning artefact MUST NOT carry a §5.9
commentary section; §5.9 records "Commentary not applicable at
tier-3 per §3.12 hard separations: tier-3 carries forward-
validation HA evidence and does not need commentary nuance."
Tier-3 claims are forecast-bounded by the forward-validation
HA's quality measures; adding commentary would either repeat
what the forecast already quantifies or — worse — extend the
forecast beyond what the HA's `result.md` supports.

## 8. Interview-prompt seeds

The `/research-interpret actionability construct-XXX` skill drives
the actionability translation as an interview. Three required
seeds per the locked-plan §6.5 spec brief, plus an optional fourth.

### 8.1 Tier-reach interview

> "What tier are you reaching for, and why? Walk the §4 evidence
> floors: tier-1 monitoring (S₁ CONCORDANT/PARTIAL + S₂
> comparability passed); tier-2 informative-pattern (tier-1 +
> cross-op replication + PPV-with-base-rate computable); tier-3
> predictive-use (tier-2 + forward-validation HA SUPPORTED).
> Which floors does the upstream chain support at this Stage A
> time?"

**Use.** Drives §5.2 + §5.3. Skill presents the map's §5 K-row
(tier aspiration) and walks each tier's evidence floor against
the upstream chain (topic positioning; cluster coherence call;
member verdicts). Skill records articulation; cross-checks
against §4 mapping rules; defaults to next-lower tier on
ambiguity per §7.12.

For tier-3 reach: skill surfaces the §3.10 gate explicitly and
asks for the forward-validation HA ID. If none exists: skill
records §5.5 sketch and proceeds at tier-2 (or tier-1 if tier-2
fails); §6.1 + §5.6 operationalise.

### 8.2 Forward-validation interview (for tier-3 reach)

> "If this is a predictive claim, where is the forward-validation
> HA? If none exists, would you like to pre-register one? What
> prediction window, what prediction rule, what verdict criteria,
> what lock date — sketched at the §5.5 forward-validation pathway
> shape?"

**Use.** Drives §5.5. Skill walks the six-element forward-
validation HA shape (target + signal; prediction window;
prediction rule; outcome operationalisation; verdict criteria;
lock date) and records as §5.5 + §5.8 own-research. Skill MUST
NOT autonomously fill any element (pre-reg is the user's
discipline gate). Cross-checks against §3.10 binding — flags if
proposed lock date postdates window start.

### 8.3 Harm-scenario interview

> "What is the harm scenario if this actionability claim turns
> out to be wrong in your daily use? What would the subject do
> based on the tier-claim wording, and what cost would they
> incur if the claim does not hold?"

**Use.** Drives §5.4 + §7.2 anti-pattern check. Skill walks the
harm-scenario per the earned tier's permitted wording, surfacing
where wording could be misread as advice (tier-1 "track" → "act
on" prescription; tier-2 "associated with" → forecast; tier-3
forecast without lead-time/reliability). Populates §5.4
construct-specific overclaims beyond mandatory minimum. Skill
also asks "is any §5.3 / §5.4 / §5.9 wording readable as
advice?"; if yes, rephrase before lock.

### 8.4 Optional seed — commentary-shape interview

> "Per the map r3 §5 row, this construct is §3.12 commentary-
> eligible at the earned tier-N. Would you like to add a §5.9
> subject-narrative commentary section attached to the §5.3
> tier-N claim? If yes, what is the patient-facing nuance about
> how you read this signal in lived experience — using the §3.12
> permitted-wording list ('I notice', 'in my experience', 'in
> retrospect', 'I lean toward')? If no, the section is recorded
> as skipped with a one-line rationale."

**Use.** Drives §5.9 (optional). Skill skips this seed if tier-3
(commentary not eligible per §7.14) or if user declines. When
user proceeds, skill walks the §3.12 discipline: attached-to
citation; subject-attribution every sentence; permitted-wording-
only; forbidden-wording flagging; hard-separations reminder.
Skill refuses to lock if commentary suggests tier promotion per
§6.4 + §7.8.

§5.9 commentary is drafted in advance of the Stage T patient-
audience layperson test (per §3.12 + §6.6). Downstream test
failure on commentary wording propagates back to Stage A's §5.9
per §3.7 drift.

## 9. Agent-instruction outline

What `/research-interpret actionability construct-XXX` (produced in
§11 step 7) codifies into skill behavior. Compact phase-list form
per the brief's density-discipline guidance.

### 9.1 Load

In order: the map's §5 construct row for the target construct;
each feeding topic's locked `topic-*.md`; the contributing
cluster's `cluster-*.md` files via the topic chain (for upstream
chain reference); any forward-validation HAs in the registry
that target this construct (`hypothesis.md` + `result.md` if a
verdict has landed); the limitations doc §3 (all seven L-IDs)
+ §5 row for `construct-*.md`; the RESEARCH-REPORT §5.2 PPV-with-
base-rate precedent; the relevant methodology MDs (guides #1, #2,
#3, #4 + any construct-specific methodology MDs); `personal_
hypotheses.md` §32 for the HA-test-level prohibition on
classifier-discrimination measures; `hypothesis_lock_process.md`
for the forward-validation HA pre-reg discipline.

### 9.2 Gate

All feeding `topic-*.md` locked + construct in map → §9.3. Any
missing or unlocked → halt; produce only §5.6 `open_inputs` entry
per refusal-path 1 (topic missing) or refusal-path 2 (construct
not in map). Map-change-needed surfaces (per §6.5 halt-criteria)
→ halt; produce only §5.6 entry per refusal-path 2.

### 9.3 Extract

Per feeding topic: §4.5 positioning summary + per-subclaim
positionings (especially DIVERGES) verbatim from `topic-*.md`;
§4.7 L-ID block verbatim. Construct-level: map's §5 row cells
(tier aspiration; §3.12 commentary-eligibility; L-ID notes
column; declared-date; lock-version). Forward-validation HA (if
any exists): `hypothesis.md` pre-reg shape; `result.md` verdict
+ quality measures.

### 9.4 Interview

Walk §8 seeds in order: §8.1 (tier-reach + §5.2 + §5.3 + §6.1
checks); §8.2 (forward-validation for tier-3 + §5.5 + §5.8); §8.3
(harm-scenario + §5.4 + §7.2 check); §8.4 (optional commentary if
eligible + §5.9 + §3.12 checks). For each seed: record
articulation; cross-check against §4 mapping rules + §6 conflict
rules + §7 anti-patterns; surface mismatches; seek rephrasing.

Skill MUST NOT autonomously fill §5.2 tier earned (user picks per
§4; default-to-next-lower-tier per §7.12), §5.5 forward-validation
shape (user articulates per §8.2), or §5.9 commentary (user
articulates per §3.12 permitted wording; skill flags forbidden
wording).

### 9.5 Produce

Draft `analyses/actionability/construct-XXX.md` per §5. All twelve
sections filled (§5.10 empty placeholder until `/research-review`
time): §5.2 evidence-layer earned tier per §4; §5.3 tier claim in
permitted-wording for tier; §5.4 NOT-DO refusals (mandatory
minimum + construct-specific); §5.5 forward-validation pathway
(sketch for tier-3 reach; cited registry HA for earned tier-3;
"not aspired" otherwise); §5.6 `open_inputs` per the five
refusal-to-proceed paths; §5.7 quality measures per §3.10
(REQUIRED at tier-2+); §5.8 follow-up tracks own + external with
N=1 scoping; §5.9 optional commentary per §3.12 (skipped-with-
rationale OR filled-with-attribution-and-permitted-wording);
§5.10 placeholder; §5.11 L-ID block (all seven, applies-or-NA);
§5.12 cross-refs. Status: DRAFT r1, reviewer-mode-with-
authorization, `## Authorship` per CONVENTIONS §1.2.

### 9.6 Refuse-to-lock gate

Skill refuses to mark ready for completion if any of:

- §5.11 missing any of L1-L7 (all-seven binding per §3 + §5.11
  hard rule).
- §5.11 silently omits an L-ID without project-specific NA-with-
  justification.
- §5.2 evidence-layer earns tier-2+ but §5.7 quality measures
  missing the §3.10 PPV-with-base-rate (PPV + base rate + plain-
  language combined frame).
- §5.3 tier-claim wording uses forbidden language for its tier
  (§4 permitted-wording lists per tier + §7.5 anti-pattern).
- §5.3 / §5.4 / §5.9 contain advice-form wording (§7.2 anti-
  pattern).
- §5.4 missing the mandatory minimum NOT-DO refusal categories
  for the earned tier.
- §5.5 missing for tier-3 reach (whether earned or sketched).
- §5.5 forward-validation HA's pre-registration lock date does
  NOT precede the prediction window start (§3.10 hard predictive
  gate violation).
- §5.7 reports bare-percentage without base-rate context (§7.4
  anti-pattern).
- §5.9 commentary section attached to tier-3 (§7.14 anti-
  pattern + §3.12 hard separations).
- §5.9 commentary uses forbidden wording (§3.12 + §7.7 anti-
  pattern).
- §5.9 commentary suggests tier promotion (§6.4 conflict rule +
  §7.8 anti-pattern).
- §5.9 commentary floats unattached (no "attached to" citation;
  §7.7 anti-pattern).
- §5.8 external-research suggestion lacks N=1-limit scoping
  (locked-plan §3.11 binding).
- Any §5 section contains anti-pattern violations per §7.

### 9.7 Review handoff

On user-accepted-as-ready-for-completion: recommend fresh-
session `/research-review` per locked-plan §4 (actionability-
tier-claim artefacts get `/research-review`, with the locked-
plan §4 row's "tier downgrades on review concerns" discipline).
Report lands at `docs/research/reviews/construct-XXX-
actionability-YYYY-MM-DD.md`. The §5.10 open-downgrades-from-
review section is filled at review time, not at drafting time.

### 9.8 Acceptance + drift-trigger registration

Per §3.8: "user explicitly accepts" is the binding completion
event. On acceptance: status → LOCKED; §5.6 `open_inputs`
propagate to layer-wide `_open_inputs.md`; §5.5 + §5.8 forward-
validation sketches propagate to the registry candidate queue;
construct becomes eligible for Stage T per §3 dependency rule.
Per §3.7, four re-examination triggers register at lock:

1. Any feeding `topic-*.md` re-examined or revised.
2. A forward-validation HA produces a new verdict (SUPPORTED
   unlocks tier-3 re-examination per §5.2; REJECTED triggers
   §6.2 tier removal).
3. A tier-affecting methodology change (§3.10 update — should
   never happen per §3.10 binding; §3.12 update; §3.9
   limitations doc update; map's §5 K-row update; guides #1-#4
   lock-version change).
4. ≥6 months elapse since lock.

Commentary-carrying constructs add a fifth trigger: Stage T
patient-audience layperson test fails on commentary wording (per
§3.12 + §6.6). Fail-reason propagates back to §5.9 revision per
§3.7.

**Drift-trigger registration is manual-pending-skill.** Until
§11 step 7 lands, the §11 lock log carries a "Drift triggers
registered" line. The skill also increments the limitations
doc's §8 downstream-citation-count for each of the seven L-IDs
in §5.11 (manual until skill lands).

## 10. Cross-references

- [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  — §6.5 (spec brief); §3 (stage-map dependency); §3.5 (missing-
  inputs — five refusal-to-proceed paths); §3.6 (map pre-reg +
  conflict-resolution rule §6.5 operationalises); §3.7 (drift —
  four triggers, five for commentary-carrying constructs); §3.8
  (completion criteria); §3.9 (limitations binding — all-seven
  discipline); §3.10 (**hard predictive gate** — load-bearing;
  tier-2+ PPV REQUIRED; tier-3 forward-validation HA + lead-time
  + reliability REQUIRED); §3.11 (follow-up own + external);
  §3.12 (commentary layer — §5.9 + §6.4 + §7.7 + §7.8 + §7.9 +
  §7.14 operationalise); §4 (producer/reviewer split — tier
  downgrades on review concerns); §9 layer anti-patterns;
  §11 step 6.5.
- [`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
  — guide #1 LOCKED r2; verdict-trust chain via S₂/S₁/I.
- [`verdict_to_inference.md`](verdict_to_inference.md) — guide #2
  LOCKED r2; per-HA licensed-claim chain via S₂/S₁.
- [`internal_synthesis.md`](internal_synthesis.md) — guide #3
  LOCKED r2; cluster coherence-call chain via S₂.
- [`external_contextualisation.md`](external_contextualisation.md)
  — guide #4 LOCKED r2; **immediate upstream gate**. §4.5
  positioning Stage A reads as fixed input (must not be CANNOT-SAY
  for tier-1 reach); §4.6 N-of-1-to-group caveats; §4.7 L-ID
  block (§5.11 here extends to all seven); §4.8 open conflicts;
  §4.9 follow-up; §7 anti-patterns (§7.6 mirror; §7.8 mirror at
  HA-test-level).
- [`research_line_limitations.md`](research_line_limitations.md)
  — §3 seven L-IDs; §5 binding (**MUST cite all seven with
  applies-or-NA** — most rigorous L-ID discipline in the layer);
  §8 downstream-citation-count.
- [`synthesis_structure_map.md`](synthesis_structure_map.md) — §2
  scope; §3 cluster table; §4 topic table (feeding topics); §5
  construct table (Stage A's primary input — tier aspiration,
  §3.12 commentary-eligibility, L-ID notes, predictive-feasibility).
- [`RESEARCH-REPORT.md`](../RESEARCH-REPORT.md) §5.2 — the
  PPV-with-base-rate precedent (*"wrong 24 times out of 25"*);
  load-bearing for §5.7.
- [`personal_hypotheses.md`](../personal_hypotheses.md) §32 — the
  HA-test-level prohibition on classifier-discrimination measures
  (no AUCs / logistic regression / joint-model verdicts at HA
  level); §5.7 + §7.10 operationalise.
- [`hypothesis_lock_process.md`](hypothesis_lock_process.md) —
  forward-validation HA pre-reg discipline (§5.5 + §5.8); locked-
  before-window-begins discipline §3.10 rests on.
- [CONVENTIONS.md](../CONVENTIONS.md) §1, §1.2, §2.1, §4.2, §4.3
  as cited throughout.
- Literature methodology anchors at
  [`literature/methodology/`](../literature/methodology/): Daza
  2018 (N-of-1-to-group reach — §5.11 L1); CENT 2015 (L1);
  Natesan 2023 (defensibility bar — L1); SCRIBE 2016 (L4);
  WWC 2022 SCED (inherited via S₂'s §4.4).
- [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md)
  — construct-specific methodology for K-bout-recovery-signal.
- [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)
  — cross-phase pooling discipline (K-bout-recovery-signal L2).
- [`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md)
  — L5 presence-conditioned semantics (§7.3); relevant for
  future v24-using constructs.

## 11. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-24 | Drafted r1 | Producer-mode by fresh agent per §11 step 6.5 of [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md) (r5 LOCKED). **Eight inventions beyond §6.5 spec**: §4.4 tier mapping summary table; §5.2 three-paragraph evidence-layer structure; §5.5 six-element forward-validation HA shape spec; §5.6 five refusal-to-proceed paths; §5.7 per-measure block structure; §6.4 commentary-vs-forward-validation conflict rule; §6.5 four halt-criteria for map-change-needed halt; §9.6 fifteen-item refuse-to-lock gate. **Worked examples**: K-stress-fatigue-monitoring tier-1 + K-bout-recovery-signal tier-2 threaded through §4 + §5.4 + §5.5 + §5.7 + §5.9 + §5.11. **Two §6.5 ambiguity interpretations**: (a) "constructed-claim cannot pass §3.10 base-rate framing" routed as §5.6 refusal-path-5 (tier-1 fallback with re-cast monitoring); (b) §5.10 "open downgrades from review" interpreted as fill-at-review-time. Agent flagged §5.6 refusal-path-5 routing as strongest invention for reviewer. **Skill-precondition note** (per §11 step 7 dependency): the `/research-interpret actionability` skill must land at step 7 before any Stage A artefact can be drafted; this guide alone is necessary but not sufficient. |
| 2026-06-24 | Fresh-session `/research-methodology-review` | Verdict REVISION RECOMMENDED (mild). Report: [`reviews/methodology-actionability_translation-2026-06-24.md`](../reviews/methodology-actionability_translation-2026-06-24.md). Two required (R1: §5.5 needs seventh PPV-floor anchoring discipline element to prevent trivially-passable floor backdooring §3.10 gate; R2: §5.10 cross-ref to §6.1+§6.2+§6.4 downgrade-mechanics). Three recommended (A1: ~50-80-line density compression — flagged "for future revision pass"; A2: §5.7 → §7.4 binding-loop completion; A3: §11 lock-log scannability). **Hard predictive gate preserved at 5 enforcement layers** without weakening; **§3.12 commentary discipline** with all four hard separations operationalised across §5.9 + §6.4 + §7.7-§7.9 + §7.14 + §9.6 gates 10-13. Both worked examples handle upstream state correctly. **All-seven L-ID discipline** (most rigorous in layer) spot-checked verbatim against limitations doc r3 §3 + map r3 §5. |
| 2026-06-25 | Revised r1 → r2 | Both required absorbed: **R1** — §5.5 added seventh element "PPV floor anchoring discipline" requiring the floor anchor to null base rate by default OR tier-2 point estimate when cross-op evidence exists; floor cannot sit at or below null base rate without backdooring the §3.10 gate; both worked examples updated with explicit anchoring (K-stress-fatigue-monitoring at uniform-three-bin null ~0.33; K-bout-recovery-signal at-or-above cross-op tier-2 point estimate per RESEARCH-REPORT §5.2 base-rate frame). **R2** — §5.10 added downgrade-mechanics rule book cross-referencing §6.1 (tier-condition-unmet → tier downgrade), §6.2 (forward-validation REJECTED → tier-3 → tier-2), §6.4 (commentary-vs-evidence → commentary revised, no tier change). Two of three recommended absorbed: A2 — §5.7 closing paragraph added explicit "§7.4 anti-pattern enforces" binding-loop language; A3 — this lock-log split into per-event paragraphs. **A1 density compression deferred** per reviewer's "for a future revision pass (not blocking)" framing; future r3 may execute the ~50-80-line compression if friction surfaces during dry-run. |
| 2026-06-25 | **LOCKED r2** | User acceptance ("Absorb all (2 required + 3 recommended), lock r2, dispatch guide #6 with density signal"). Status of all sections LOCKED. Implementation proceeds to §11 step 6.6 (guide #6 `translation_to_audience.md` — the last guide). No second-pass review per established Option-γ pattern. **Drift triggers registered** (manual-pending-skill): constituent `topic-*.md` re-examined; forward-validation HA verdict landing; cited methodology MD changes lock-version (especially research_line_limitations.md, synthesis_structure_map.md); ≥6 months elapse since lock. |
