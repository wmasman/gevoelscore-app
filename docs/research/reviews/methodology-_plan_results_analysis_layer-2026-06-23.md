# Methodology review — _plan_results_analysis_layer.md (r2, 2026-06-23)

**Reviewer mode**: fresh-session peer review. Reviewer is independent of the drafting session. Fresh session, no exposure to the drafting context; doc-only knowledge.
**Target**: docs/research/methodology/_plan_results_analysis_layer.md (r2, 2026-06-23)
**Review date**: 2026-06-23
**Standards applied**: CONVENTIONS §1.2, §2.2, §3, §4; CENT 2015, SCRIBE 2016, STROBE 2007, Daza 2018, Natesan Batley 2023, WWC 2022 SCED — present in `docs/research/literature/methodology/` and verified during this review.

---

## 1. Overall verdict

**REVISION RECOMMENDED** — substantive plan, methodologically literate, and faithful to the CONVENTIONS §1.2 / §2.2 / §3 / §4 discipline that already binds the corpus. The six-stage decomposition (D → I → S₁ → S₂ → A → T) is well-motivated, the §3.5 "missing-inputs are first-class" mechanism is genuinely novel, and the §3.6 / §3.7 / §3.8 / §3.9 absorptions are mostly load-bearing rather than ornamental. However, three concerns prevent ACCEPT-as-is: (1) the §3.6 layer-wide synthesis-structure map and §6.3 per-cluster pre-declaration are nominally redundant and the conflict-resolution rule is not specified; (2) the §11 implementation order locks the synthesis-structure map (step 3) *before* the descriptive stocktake (step 5), which inverts the descriptive-before-inference discipline this layer is supposed to honour; (3) at least four coverage gaps are non-trivial (multiple-comparison correction across HAs, negative-findings discipline, power/sensitivity at the layer level, provenance/versioning of artefacts). Same-session absorption shows in a small number of cross-reference and orphan-pointer issues that a fresh-session drafter would not have made. Once these are addressed, the plan is ready for lock and the §11 cadence can begin.

---

## 2. Structural findings

### 2.1 The plan is a hybrid artefact and should declare which lens binds

The target opens with `**Status**: DRAFT, reviewer-mode-with-authorization` (line 3) but most of its content is methodology specification — six guide briefs, two supporting-MD specs, one skill spec, dependency rules, cross-cutting constraints, anti-patterns. Under CONVENTIONS §1.1, methodology MDs are producer-mode (Claude writes/edits/runs). Under §1.2, hypothesis-test artefacts and synthesis docs that carry verdicts are reviewer-mode. The plan is neither: it is a planning document for *future producer-mode methodology MDs*.

The "reviewer-mode-with-authorization" self-classification is therefore a category mismatch. The planning-of-methodology activity does not produce a verdict; nothing in this plan needs the §1.2 fresh-session-review independence guarantee in the way an HA pre-reg does. What it does need is the §2.2 four-input bar (best-practices standards, literature, tradeoff vision, research limitations + objectives), because each of the six guides this plan specifies is itself a methodology MD subject to §2.2 at draft time.

Recommendation: re-label the plan as **producer-mode planning artefact for downstream producer-mode methodology MDs**. Keep the fresh-session review (this report). Drop the "reviewer-mode-with-authorization" framing as inapplicable — and note this decision in §12 Authorship so the next planning artefact does not inherit the mis-classification. The answer to "does it matter" is yes: the §1.2 framing would oblige Claude to defer all edits to the user, whereas a producer-mode planning artefact under §2.2 lets the user delegate revision-drafting back to Claude in the same session that absorbs review findings. The plan's r2 absorption pattern already implicitly assumed producer-mode authority.

### 2.2 Dependency consistency between §3 and the r2 additions

§3 lists five dependency rules. §3.6 adds the requirement that S₁/S₂/A targets must appear in the pre-registered synthesis-structure map. §3.9 adds that S₂ also requires `research_line_limitations.md` to exist. The dependency rules in §3 *were* updated to absorb these (e.g. the S₁ rule reads "AND the cluster appears in the pre-registered `synthesis_structure_map.md` (per §3.6)"; the S₂ rule cites both §3.6 and §3.9). This part of the absorption is clean.

However, the §3 dependency graph is still under-specified on three edges:
- **T's preconditions**: §3 says "`T` may target any prior stage's output (interpretation, synthesis, contextualisation, or actionability)" but does not specify whether T requires the synthesis-structure-map presence when targeting an interpretation artefact. Per §6.6, Stage T inputs include the source artefact, `research_line_limitations.md`, and `plain_language_dictionary.md` — but not the synthesis-structure map. This may be deliberate (T translates whatever is already locked, and the structure map's role is upstream); it should be stated explicitly so the skill's refusal logic is unambiguous.
- **Stage-skipping**: §3 allows skipping for "structurally trivial" cases (e.g. single-HA cluster) with a `stage_skipped.md` stub. §3.6's hard rule that "S₁ refuses to start without cluster in map" appears to forbid the skip pathway, because a single-HA cluster still has to be declared in the map. Either §3.6 needs an explicit accommodation ("a single-HA cluster is declared in the map as such and S₁'s `stage_skipped.md` stub references the map row") or §3 needs to drop the structural-skip clause for S₁. The current text is internally inconsistent.
- **Re-examination cascade**: §3.7 says "Any constituent `interpretation.md` re-examined or downgraded" re-examines the cluster MD. But it does not specify whether a CONFIRMED-NO-CHANGE outcome at the interpretation layer triggers any cluster-level work (presumably no), nor what happens when an interpretation is REVISED but the joint claim does not change. Spell this out so the cadence-check skill of §3.7 has unambiguous logic.

### 2.3 Ordering issue in §11: the synthesis-structure map locks before the descriptive stocktake

§11 step 3 locks `synthesis_structure_map.md` (per §3.6). Step 4 locks `research_line_limitations.md`. Step 5 is "stocktake descriptive coverage" — walk existing `analyses/descriptive/` artefacts and compare to what HA `test.py` files lean on, producing a gap list. Step 6 is the six guides.

This inverts CONVENTIONS §2.1 (descriptive-before-inference) at the layer level. The synthesis-structure map declares clusters, topics, and constructs that are inferential groupings — they are stories about how the corpus's HAs combine. Locking that map before knowing where the *descriptive* backstopping is solid is the same data-peeking-by-absence pattern §2.1 protects against. A cluster whose Stage D audit will turn out REQUIRES-DESCRIPTIVE-WORK for half its members should not be in a locked map *yet*; locking it pre-stocktake commits to a synthesis structure whose preconditions are unverified.

Two concrete failure modes that this ordering hides:
- The map declares cluster X = {HA-A, HA-B, HA-C} based on the user's intuition about shared construct. The stocktake then reveals HA-A has unbackstopped assumptions that will downgrade it to DOWNGRADED-INCONCLUSIVE-PROVISIONAL. The map now contains a cluster whose centre of mass shifts as soon as Stage D runs — but the map is locked.
- The stocktake reveals HA-D (not yet considered for clustering) shares the same construct as HA-A/B/C through a descriptive backstop that the user did not previously see as load-bearing. The map needs to add a row; under §3.6 this is allowed ("the map can grow over time"), but the *initial* clustering would have been different had stocktake-information been available.

Recommendation: swap §11 steps 3 and 5. Order: review (1) → lock plan (2) → **stocktake descriptive (was 5)** → research-line limitations (was 4) → **synthesis-structure map (was 3)** → guides (6) → skill (7). The descriptive stocktake is itself a producer-mode descriptive activity that does not require the guides or the skill; running it first gives the synthesis-structure map a defensible factual base and respects the discipline §2.1 imposes on the rest of the corpus.

If the user has a reason to lock the map first (e.g. they want the map to reflect their substantive prior, independent of where descriptive backstops happen to be solid), state that reason explicitly in §11 and accept that the map will likely need revision after stocktake. Document the cadence at which this is expected.

---

## 3. Per-section findings

### §0 Purpose
The six-bullet decomposition (descriptive audit / verdict → interpretation / internal synthesis / external contextualisation / actionability / translation) is cleaner than the upstream methodology corpus and worth preserving. The two-supporting-MD insert (synthesis-structure map + research-line limitations) is well-motivated. **Minor**: the bullet on "Translation to audience" mentions PAIS patients in passing; consider naming "Long COVID / ME-CFS-adjacent" since PAIS is a broader umbrella that includes conditions where the corpus's findings may not transfer (e.g. post-cancer fatigue). The patient-audience scope deserves to be explicit, not implicit.

### §1 Scope and out-of-scope
Clean. The "out-of-scope: re-interpreting any specific HA" disclaimer is exactly the discipline barrier between methodology and result-production that CONVENTIONS §1 wants preserved.

### §2 Locked decisions from the planning session
Five rows. Row 4 ("Artefact naming inside per-stage folders") seems to belong in §5 (Output structure), not §2 (locked planning-session decisions); it is a naming convention, not a methodological commitment from the planning conversation. Consider moving or marking it as a deferral that §5 will operationalise.

Row 5 ("Plan review discipline") is internally inconsistent with the producer-vs-reviewer split — see §2.1 of this review. Either drop "reviewer-mode-with-authorization" or restate it.

### §3 Stage map and dependencies
Dependency-graph concerns covered in §2.2 above. The ASCII diagram is clear and worth keeping; consider adding an explicit "open-inputs loop" line showing how §3.5's queue interacts with the stages (it currently looks linear, but §3.5 + §3.7 + §3.8 make it recursive).

The skipping clause needs reconciliation with §3.6 — see §2.2 above.

### §3.5 Missing-inputs flagging is first-class
**This is the strongest section of the plan.** The "every guide produces an `open_inputs` block" mechanism is precisely the discipline that prevents the silent-narrowing failure mode CONVENTIONS §4.2 protects against at the upstream layer. The two hard rules ("never silently degrade" / "acquisition may not contaminate later inference") are correctly framed and load-bearing.

**One nit**: the `_open_inputs.md` queue lives at `docs/research/methodology/_open_inputs.md`. This puts a live working queue inside `methodology/`, which is the folder of locked binding rules. Consider `docs/research/_open_inputs.md` (sibling to `methodology/`, not inside it) so the convention "files in methodology/ are locked rules" is preserved. The `_` prefix is consistent either way.

### §3.6 Synthesis-structure pre-registration
The motivation ("clustering is story-shaping; reactive declaration lets cherry-pick re-enter") is sound. But this section is in tension with §6.3 — see §4.1 of this review.

**Substantive concern**: §3.6 says the map is producer-mode but also requires "fresh-session `/research-review` like other methodology MDs before lock." `/research-review` is for reviewer-mode artefacts; methodology MDs use `/research-methodology-review` per CONVENTIONS §7 (the listed slash command) and per `methodology/README.md`. Fix this cross-reference. (Same fix applies in §4 row 2 for `research_line_limitations.md` and in §11 steps 3 and 4.)

### §3.7 Drift and replication policy
The six-month cadence is the load-bearing question — see §4.6 below for full treatment. The two-outcome split (CONFIRMED-NO-CHANGE / REVISED) and the "no silent decisions" rule are correctly framed.

**Gap**: there is no specification of *who* runs the cadence check. The skill (§7) gets a `--drift-check` flag, but does the user have to invoke it? Is it run on every session? Is there a calendar reminder? In practice, "every six months the skill walks all locked artefacts" is an automation claim that needs an automation owner. If the answer is "the user runs it when they remember," then it is a recommendation, not a binding mechanism — say so.

### §3.8 Stopping and completion criteria
Clean specification. The "user explicitly accepts" binding-event and "open_inputs do not block completion" distinction together solve a real failure mode (perfectionism preventing any artefact from finalising). This is good. **Add**: a clarifying line that re-examination (§3.7) does not require a new lock event unless REVISED outcome — CONFIRMED-NO-CHANGE is its own outcome, not a re-lock. This is implicit in §3.7 but worth restating in §3.8.

### §3.9 Research-line limitations binding
The seven-item initial coverage is well-chosen and tracks CONVENTIONS §3 and §4 + memory pointers. **Missing**: the upstream `_lagged_lcera` family-vs-v3.1 backstop concern (CONVENTIONS §3.2) is a baseline-construction limitation; should be in the list or explicitly framed as upstream-already-handled. Similarly, the train/validate-split-fate constraint (CONVENTIONS-cited `train_validate_split_fate.md`) is a single-pool-vs-held-out limitation that affects how the corpus can speak; surfacing it here keeps Stage S₂ honest about the inference reach of N-of-1 findings.

The "binding rule" that per-topic / per-construct artefacts MUST cite from this doc is correct and aligned with how `symptom_mention_asymmetry.md` already binds every v24-derived analysis.

### §4 Producer / reviewer split
The table is correct in shape. Three notes:
- The guide MDs (row 1) are listed as "optional `/research-review`" — but they are methodology MDs and would be subject to `/research-methodology-review`, not `/research-review`. Same fix as §3.6.
- The `plain_language_dictionary.md` row says "None (live document)". For a live document that affects patient-audience translations, "no review" is a real risk surface — a term silently shifting meaning across versions can break the consistency this layer is supposed to enforce. Consider a periodic cadence-check (§3.7-style) on the dictionary, even if individual term-additions are not reviewed.
- The `descriptive_audit.md` row says producer-mode, "None (audit, not verdict)". This is correct — an audit is structurally a descriptive artefact. But the audit *gates* downstream reviewer-mode work (Stage I refuses without it). If the audit has a bug, the downstream verdicts inherit it. Consider listing the audit as "subject to spot-check during the next cadence cycle" — not full review, but not zero either.

### §5 Output structure
The folder tree is clear and follows existing conventions. **One concern**: `analyses/translation/research-audience/HA-C4.md` and `analyses/translation/patient-audience/HA-C4.md` carry the same base name as different artefacts. This is parallel-folder-disambiguation; it works. But the skill's per-stage routing (§7) takes `<target>` as an HA ID or path — does `translate HA-C4` mean both tracks, or one? The §6.6 outline says both tracks are produced together; consider explicit invocation forms like `translate HA-C4 --research-only` for the optional single-track skip case.

### §6.1 `descriptive_precondition_audit.md` — Stage D
The checklist sketch is well-anchored in the upstream MDs. Two missing rows worth considering:
- **Trajectory-detrend sensitivity** per CONVENTIONS §3.7: any HA test that uses raw pre-vs-post window comparisons (not lagged-baseline z-scores) needs a detrended sensitivity row. The audit should check whether this is present, OR whether the HA explicitly dispatches §3.7 as inapplicable (because the test uses lagged-baseline). The check is binary and mechanically auditable.
- **Boundary-spacing minimum** per CONVENTIONS §3.8: for any HA using pre-vs-post window design with sequential boundary dates, check that `boundary_gap ≥ 2·B + min_window_days` holds and that unanalysable boundaries are recorded as NaN rows rather than silent drops. Mechanically auditable from the result CSV.

Both are recent additions to CONVENTIONS §3 and a stocktake-pass audit should catch them.

**Anti-pattern addition**: "Citing the upstream methodology MD without checking whether the HA's `test.py` actually implements the rule the MD requires." (The §3.2 `_lagged_lcera` audit hook is a worked example — `hypothesis_lock_process.md` §4.1 notes pre-MD HA families silently inherit the wrong block-length policy.) An audit that just confirms "MD is cited" rather than "MD is followed" misses this.

### §6.2 `verdict_to_inference.md` — Stage I
The four-section structure (what data shows / what verdict licenses / what it does NOT license / caveats narrowing) is the right shape. The "lived-experience prior reconciliation" section (#6) is unusual and worth keeping; n=1 research has a unique audit constraint where the participant *is* a reasoning agent with priors and the protocol of preserving rather than resolving the conflict is correct (per CONVENTIONS §4 framing).

**Substantive concern**: §6.2's checklist row "Confirmatory vs exploratory status from the pre-reg carried through" relies on the HA pre-reg having that status explicitly. Older HAs may not. The audit should distinguish (a) the pre-reg explicitly named the status, (b) the pre-reg is silent and the status is inferable from CONVENTIONS §4.3's three-question check, (c) the pre-reg is silent and the status is not safely inferable. Case (c) should route to `open_inputs` rather than guessing.

**Anti-pattern missing**: "Treating a single-cell-headline-locked verdict as evidence on a sensitivity-arm cell." Hypothesis_lock_process.md §4.2 makes this discipline explicit (sensitivity arms cannot promote to SUPPORTED). Stage I interpretations need to inherit this — a headline-cell SUPPORTED verdict does not license claims about the sensitivity-arm cells, even if the sensitivity arm showed the same direction.

### §6.3 `internal_synthesis.md` — Stage S₁
This is where the §3.6 vs §6.3 tension lives — see §4.1 of this review.

The CONCORDANT / PARTIALLY CONCORDANT / CONFLICT / ORTHOGONAL taxonomy is good but needs operational definitions in the guide itself (currently flagged "Definitions in the guide"). The same is true for AGREES / EXTENDS / DIVERGES / CANNOT-SAY in §6.4. These are the load-bearing classification calls; ambiguity here translates directly into cross-cluster inconsistency.

**Anti-pattern strengthening**: §6.3 already names "three HAs running on the same signal are one piece of evidence, not three." Make this measurable: include an operationalisation-overlap matrix in the cluster MD (rows = HAs, columns = signals used) so the reader can see at a glance whether the HAs are independent operationalisations or the same signal in different statistical dress.

### §6.4 `external_contextualisation.md` — Stage S₂
Sound spec. The CANNOT-SAY-is-valid-and-preferred discipline is correctly stated.

**Coverage gap**: the comparability check (COMPARABLE / PARTIALLY COMPARABLE / NOT COMPARABLE) needs explicit guidance on how to handle the case where the external evidence base itself disagrees internally. Many LC / ME-CFS topics have competing camps (e.g. HRV-as-prognostic vs HRV-as-confound debates). The plan currently says "if competing positions exist, what are they and who holds them"; it should add that the project's positioning does not adjudicate the external dispute — it positions against each camp and lets them stand.

### §6.5 `actionability_translation.md` — Stage A (hard predictive gate)
See §4.2 of this review for the full hard-gate calibration discussion. The three-tier ladder (Monitoring signal / Informative pattern / Predictive use) is well-defined and the forward-validation requirement for tier 3 is correctly anchored.

**Anti-pattern addition**: "Treating a Stage A claim as falsifiable by absence of negative evidence." A predictive claim that has not been forward-validated cannot be defended by saying "no contradictory daily-use experience has surfaced." Absence of negative lived-experience is not corroboration; only the pre-registered forward-validation HA is.

### §6.6 `translation_to_audience.md` — Stage T
See §4.3 of this review for the one-vs-two-guide discussion.

The anti-patterns block here is the most thorough of the six guides — that is appropriate given how high-risk translation is. The "tier upgrading in wording" anti-pattern, with its concrete example ("watch for X" is predictive in disguise; "X has historically appeared alongside Y" is monitoring-phrasing), is exactly right and reusable.

**Coverage gap**: no specification of how to handle the case where the source artefact is later revised under §3.7 drift policy. Does the patient-audience translation auto-archive when its source REVISES? Does it stay live with a deprecation warning? Does it block until re-translation? The cadence-check sweep needs to know.

### §7 The skill — `/research-interpret`
See §4.5 of this review for the skill-as-engine vs guide-as-data architectural discussion.

**Substantive concern**: the skill's "refusal discipline" (responsibility #5) is correctly framed but lacks a specification of *what counts as user override*. Currently, the user "explicitly accepts REQUIRES-DESCRIPTIVE-WORK to proceed" (§6.1 agent-instruction outline). Does an override pollute the artefact's status downstream? An interpretation built on a not-yet-backstopped audit is structurally weaker than one built on a TRUSTED audit; this difference should propagate into the artefact's metadata and into the Stage I checklist (which already requires the audit to be TRUSTED or user-accepted PROVISIONAL — make this explicit in the artefact body, not just in the skill's runtime check).

### §7.5 Candidate skills to lift later
Excellent section. The "triggers to lift" discipline is the right way to manage premature optimisation in skill-building. The Stage-A-specific skill candidate is appropriately scoped — see §4.5.

### §8 Cross-cutting constraints
Clean. The list correctly inherits the binding rules from CONVENTIONS without restating them.

**Add**: CONVENTIONS §3.4 (crash-drop sensitivity) belongs in this list — it is a layer-binding rule that every Stage D audit needs to confirm was applied or explicitly dispatched at the upstream HA. Currently buried in §6.1's checklist; should be surfaced as a layer-level constraint.

### §9 Layer-level anti-patterns
Seven items. See §4.7 of this review for additions.

### §10 Open questions deferred to guide-drafting time
Nine items, all reasonable. The decision to defer them is correct — they are guide-specific operational details that benefit from being resolved with the guide's full context.

**One concern**: item 5 ("Audit-before-push integration: should `audit_for_publication.py` be extended to gate on Stage A actionability claims") is not a guide-drafting question, it is a project-infrastructure question. Resolve at the §7 skill-building step, not deferred to a guide.

### §11 Implementation order
See §2.3 of this review for the ordering concern (synthesis-structure map vs descriptive stocktake).

The §11 structure is otherwise sound. The dry-run-on-HA-C4 (steps 8-9) is the right choice — HA-C4 is well-documented, recently verdicted (REJECTED at triad sum 0.0), and the result.md is rich with the kind of caveats Stage D will need to audit.

**Substantive concern**: step 12 ("Periodic drift check — ongoing, no end state") is fine but vague. Add: "First drift check fires N weeks after step 11 begins, even if all rollout is complete or not." Without a calendar anchor, this becomes "we'll do it when we remember," which is what §3.7 protects against.

### §12 Authorship
Clean. The revision-history bullet for r2 is honest about which seven additions were absorbed.

---

## 4. Cross-cutting concerns

### 4.1 §3.6 (layer-wide map) vs §6.3 (per-cluster pre-declaration) — redundant, complementary, or in tension?

**Verdict: complementary in intent, redundant in mechanism, and currently under-specified about which wins on conflict.**

§3.6 declares the *whole layer's* clusters/topics/constructs upfront. §6.3 declares the *individual cluster's* membership immediately before the S₁ session runs. Both are designed to prevent cherry-picking; both leave a paper trail.

Why they are not in tension on a clean run: §3.6's pre-declared map names cluster X = {HA-A, HA-B, HA-C}. The S₁ session for cluster X opens, §6.3's per-cluster pre-declaration step re-asserts {HA-A, HA-B, HA-C} and the user signs off. No conflict.

Where they are in tension: when the §6.3 step reveals that HA-D should be in the cluster (e.g. the user remembers it shares the construct) — does adding HA-D to cluster X require (a) a synthesis-structure-map revision and lock cycle before S₁ can proceed, or (b) a §6.3-level appendation that the map then absorbs at the next cadence? Without specification, the skill cannot enforce either; the user makes the call inconsistently across sessions.

**Recommendation**: keep both, but specify the conflict resolution. Proposed text for the plan: *"§3.6 is the project-level commitment; §6.3 is the just-in-time confirmation. If §6.3 reveals a needed change to the §3.6 map, the §6.3 session stops, the §3.6 map is revised (drafting + fresh-session review + lock), and the §6.3 session resumes. The S₁ session never proceeds against a map that does not reflect its membership."*

This makes the redundancy productive: §6.3 is a structural integrity check on §3.6, not a duplicate of it.

### 4.2 Hard predictive gate calibration (§6.5)

**Verdict: correctly calibrated against the literature; one wording tightening recommended.**

The hard gate ("predictive claim requires a pre-registered forward-validation HA; retrospective fit does NOT qualify") is defensible and arguably understated against the N-of-1 standards in `literature/methodology/`. Specifically:

- **Daza 2018** (counterfactual framework for N-of-1) sets out exactly this distinction. Retrospective fit on self-tracked time-series data establishes association under a counterfactual framing only if the stationarity / no-unmeasured-confounding assumptions hold; a *predictive* claim further requires forward-looking validation because the counterfactual evidence is about what would have happened in a different past, not what will happen in a different future.
- **Natesan Batley 2023** documents that 83.8% of n-of-1 medical studies ignore autocorrelation entirely; only 3.48% meet WWC SCED evidence standards. The hard gate is doing exactly what the literature says needs doing.
- **CENT 2015** (CONSORT for n-of-1) explicitly requires that prediction-relevant analyses pre-register their forecast windows. The hard gate operationalises this for a single-subject observational corpus.
- **WWC 2022 SCED standards** (single-case design) require replication across phases / conditions / participants. The corpus has neither cross-participant replication nor intervention-imposed phases; the forward-validation HA is the closest available analogue and is required by the standards' replication discipline.

The plan's framing of the gate as "non-negotiable at the layer level; guide drafts may not weaken it" is appropriate. The literature does not support a softer gate; the field-wide failure rate (Natesan) suggests anything softer would put this project in the failing 96.5%.

**One tightening**: §6.5's third anti-pattern says "Backdoor predictive claims via wording ('watch for X' can be a predictive claim in disguise — gate applies)." This is correct but soft. Strengthen: *"Any wording that frames a signal as *forward-looking* — including imperative phrases ('watch for'), aspirational phrases ('signals that prepare you for'), causal-prospective phrases ('leads to'), or temporal-forward phrases ('precedes', 'predicts', 'warns of') — is treated as a predictive claim and gated. Re-phrase as past-tense association ('historically appeared alongside') or refuse the translation."* This makes the anti-pattern mechanically auditable.

### 4.3 Two-track translation guide (§6.6) — one guide or two?

**Recommendation: one guide (as currently specified) with explicit per-track sections; do not split.**

Arguments for splitting:
- Research-audience and patient-audience are different audiences with different conventions, vocabulary norms, and review standards (e.g. patient track needs layperson testing; research track does not).
- A single guide risks treating both as variations on the same theme, when they are structurally different communication acts.
- Easier to evolve independently (e.g. the patient-track might gain new requirements when a real PAIS-patient peer is recruited).

Arguments for one guide:
- The two tracks share the upstream source artefact, the uncertainty calibration, the visual-summary requirement, the no-tier-upgrading anti-pattern, and the dictionary-maintenance discipline. Splitting duplicates these.
- Translation is itself one act with two outputs; the most dangerous failure mode (a tier-upgrading research-track claim quietly drifting into the patient-track) is easier to catch when both tracks are governed by one rule-set.
- The "both tracks produced or skip-research-internal explicit" rule (§6.6 checklist) requires a single guide to enforce; splitting would invite "produce one, defer the other" drift.
- The existing methodology MDs (symptom_mention_asymmetry.md, nightly_attribution.md) bind multiple downstream uses from one rule-set; the project pattern is one binding doc per construct.

**Decisive consideration**: the failure mode the plan most needs to prevent is *the patient-track lagging the research-track*. A single guide whose "both tracks or skip" rule binds both at the same lock event is the right tool. If the patient-track evolves new requirements later, add them to §6.6 rather than forking.

The one structural change worth making: in §6.6 itself, format the section outline as parallel per-track columns (or as one canonical outline with per-track-specific subsection notes inline) rather than the current "same outline for both, content differs." This makes the divergences mechanically visible.

### 4.4 Same-session absorption — what r2 missed

Per the dispatching instructions, r2 added seven things in the same session as r1. The following are artefacts of that absorption that a fresh-session drafter would not have made:

1. **`/research-review` vs `/research-methodology-review` confusion** — §3.6, §4 (row 2), §11 (steps 3 and 4) cite the wrong slash command for methodology MDs. The drafter knew both commands existed (CONVENTIONS §7 lists them) but absorbed the new sections using the more-recently-mentioned name.
2. **§3.6 vs §6.3 conflict-resolution rule missing** — see §4.1 above. A fresh-session reviewer reading both sections cold would have flagged immediately.
3. **§11 ordering of synthesis-structure map vs descriptive stocktake** — see §2.3 above. The §2.1 descriptive-before-inference principle is internalised in the drafter; the absorption-into-existing-§11 step put the map at step 3 because that was the natural place for new content, not because the ordering survives the §2.1 check.
4. **Cross-references between new sections** — §3.6 cites §3, §3.5, §3.7; §3.7 cites §3.6, §3.8; §3.8 cites §3.7; §3.9 cites §3.6 and §3.5. The web is dense but not actually broken — the cross-refs hold. This is the part of the absorption that did integrate cleanly. Credit where due.
5. **Guide #6 anti-patterns inherit from Stage A but no reciprocal pointer in Stage A** — §6.6 says "the Stage A backdoor-predictive-claims anti-pattern propagates here." §6.5 does not mention that the wording-discipline issue will reappear at Stage T. Add a forward pointer in §6.5 to §6.6.
6. **The §10 deferred questions grew from ~5 to 9** — items 6-9 are translation-related and added in r2. Item 8 ("Drift-check cadence — six months is the §3.7 default; whether that's the right cadence for *this* corpus' velocity needs revisit after the first cadence cycle") essentially admits the §3.7 cadence is provisional. Surface this in §3.7 itself rather than burying it in §10.

### 4.5 Skill-as-engine vs guide-as-data architecture (§7)

**Verdict: holds for Stages D / I / S₁ / S₂ / T as currently specified; warrants concern for Stage A's hard-gate mechanics.**

The generic skill works when the per-stage logic is *interview-driven* (load guide, walk sections, ask seeds, gate on checklist). Stages D / I / S₁ / S₂ are all in this shape. Stage T is two-track but both tracks follow the same interview pattern; the two-track logic is in the guide itself.

Stage A is structurally different. The hard predictive gate is not an interview question — it is a structural refusal. The skill must:
1. Inspect the registry for a forward-validation HA whose target matches the construct.
2. If found, check its `result.md` for a verdict on the predictive claim.
3. If SUPPORTED, allow tier-3 claim wording; otherwise cap at informative-pattern.

This is *executable logic*, not interview logic. Loading the guide as data and walking through the seeds will not, by itself, enforce the gate — the skill needs hard-coded inspection of the registry. The plan's §7 spec gives the skill responsibility "refuse any predictive claim without a forward-validation HA in the registry," but does not specify the registry-inspection mechanics.

**Recommendation**: keep the single skill for now, but include in §7's skill-instruction MD an explicit registry-inspection sub-routine for Stage A that the generic engine calls. Treat this as the first candidate for §7.5's "lift to dedicated skill" if the inspection logic accretes — the §7.5 candidate `/research-actionability-gate` is correctly anticipated.

The architecture holds; the spec needs to acknowledge that Stage A's enforcement requires more than interview-pattern execution.

### 4.6 Drift policy cadence (§3.7) — six months defensible?

**Verdict: arbitrary; defensible as a starting heuristic; needs explicit revisit condition.**

No published reporting standard fixes a drift-check cadence for n-of-1 longitudinal research. The closest published guidance:
- **CENT 2015**: addresses reporting at conclusion-of-trial; does not specify post-trial drift cadence.
- **SCRIBE 2016**: same.
- **Daza 2018**: implies that stationarity assumptions need rechecking as new data arrives, but does not set a calendar cadence.
- **WWC 2022 SCED**: requires phase-level stability documentation; not a calendar cadence.
- **Natesan Batley 2023**: documents reporting gaps; does not address drift cadence.

So six months is not defended by literature. It is also not arbitrary in a bad sense — it tracks the corpus's natural rhythm (the project has averaged roughly one wave of HA pre-regs and one Garmin re-extraction per six-month window across the visible history). For a corpus with this velocity, six months is the timescale at which "things have moved enough to warrant a structural sweep" is plausibly true.

**Recommendation**: keep the six-month default, but add an explicit revisit trigger to §3.7: *"The six-month default is provisional. After the first cadence cycle, evaluate (i) what proportion of locked artefacts had re-examination triggers fire, (ii) of those, how many produced CONFIRMED-NO-CHANGE vs REVISED, (iii) whether the cadence felt too frequent (CONFIRMED-NO-CHANGE dominant, churn cost > value) or too slow (multiple downstream surprises between cycles). Revise the default if needed; document the revision and rationale."* This makes the cadence falsifiable rather than ritual.

§10 item 8 already gestures at this; promote it into §3.7 itself.

### 4.7 Anti-pattern completeness

Per the dispatching instructions, I checked for: data-snooping at stocktake, correlation-vs-causation slippage at I/S₁, survivorship bias at translation, selection effects at cluster definition.

- **Data-snooping at stocktake**: not explicitly named. The §3.5 hard rule covers it indirectly ("acquiring a missing input via a path that contaminates later inference... is forbidden"). Strengthen by adding to §9 a layer-level anti-pattern: *"The stocktake-as-pilot fallacy — running the descriptive stocktake (§11 step 5) with knowledge of which downstream interpretations are wanted, and shaping the descriptive cells to confirm those interpretations. The stocktake is a producer-mode descriptive activity; its outputs must be independent of any interpretive aspiration."*
- **Correlation-vs-causation slippage at I/S₁**: §6.2 anti-patterns name "REJECTED therefore the hypothesis is false" and "SUPPORTED therefore the mechanism is correct." The second is correlation-vs-causation. Good. §6.3 should add: *"Cluster-level correlation does not license cluster-level causation — even if all HAs in a cluster show the same direction, the joint claim is associational, not mechanistic, unless an external mechanism warrant exists."*
- **Survivorship bias at translation**: not named. §3.9 lists survivorship at the research-line level (only days where data was collected). At translation, the relevant survivorship is *which findings made it to translation* — the loudest claims are over-represented because the muted / inconclusive / refuted findings are less likely to be picked for patient-audience output. Add to §9: *"The translation-selection fallacy — translating only SUPPORTED / SUPPORTED-strong findings leaves the patient-audience corpus systematically over-confident about what is known. Negative or null findings warrant their own translation pass when they refute a common-belief claim (especially around pacing, recovery, or signal-reliability)."*
- **Selection effects at cluster definition**: §6.3 already names retroactive constellation cherry-picking. Strengthen: *"The exclusion-by-omission fallacy — declaring a cluster without explicitly listing the HAs that touch the construct but are not included, and why. An HA that 'doesn't fit the cluster's story' may be the most informative one."*

### 4.8 Coverage gaps

Per the dispatching instructions, I considered: power/sensitivity at the layer level, multiple-comparison correction across HAs, auto-versioning / provenance tracking for artefacts, explicit treatment of negative findings, user-facing summary aggregating across constructs.

**Power / sensitivity at the layer level — not covered.** The plan gates per-HA power-calc dispatch via the upstream `hypothesis_lock_process.md` §3.8 gate. But the layer itself has a meta-power question: across 30+ HAs with varying n and effect-size sensitivity, can the layer make a defensible aggregated claim about the corpus's reach? CONVENTIONS §2.2 requires four-input reasoning for methodology MDs; one of the four is "our research limitations + objectives" which includes n. Stage S₂ (external contextualisation) should require a per-topic statement of the corpus's *effective* sample size and detectable-effect-size floor; otherwise topic-level positioning is vulnerable to "we don't see X" claims that are actually "we lack power for X."

Recommendation: add to §6.4 checklist: *"Per-topic effective n and minimum detectable effect size stated explicitly; CANNOT-SAY positioning is the default when this is below the comparability bar."*

**Multiple-comparison correction across HAs — not covered at the layer.** Per-HA, the discipline is single-cell headline lock or Bonferroni (CONVENTIONS via `hypothesis_lock_process.md` §4.2). But the layer aggregates 30+ verdicts. Reporting "we have 12 SUPPORTED, 11 REJECTED, 7 PARTIAL, 5 INCONCLUSIVE" without stating the cross-HA multiplicity inflates the apparent SUPPORTED rate by chance. The plan should require Stage S₂ or layer-level synthesis to state the cross-HA multiplicity discount, even if just as a sensitivity overlay.

Recommendation: add to §6.4 or §6.5 a rule: *"Cross-HA cluster claims may not promote a fraction-of-SUPPORTED-HAs reading to a tier-2 informative claim without a multiplicity-adjusted denominator (effective N of independent HAs after collapsing operationalisation-overlap)."*

**Provenance / versioning of artefacts — partially covered.** §3.7's lock-log captures CONFIRMED-NO-CHANGE / REVISED outcomes. But each artefact's content does not have a per-paragraph version pointer. When `cluster-stress-load.md` is REVISED, a downstream `construct-overnight-recovery.md` that cites a specific claim from the cluster may need to know whether that specific claim survived. Add: *"Every cited claim in a downstream artefact carries the source-artefact version stamp it was cited against; on §3.7 revision of the source, the downstream artefact is flagged for paragraph-level re-examination, not full re-translation."*

**Negative findings — under-covered.** The plan's anti-patterns guard against over-claiming on SUPPORTED, but the translation guide does not require negative findings (REJECTED at the verdict level, or REFUTED at the cluster level) to be translated. This is its own kind of bias — patient-audience material that only ever speaks to positives systematically misleads.

Recommendation: add to §6.6 a section-outline item: *"Negative-finding translation discipline — REJECTED / REFUTED / NOT-COMPARABLE / CANNOT-SAY source artefacts get translated under the same dual-track rule when they refute a commonly-held belief or recommendation. The 'skip-research-internal-only' exception applies only to genuine null findings, not to refutations of common claims."*

**User-facing summary across constructs — not covered.** The corpus will eventually have ~10-30 construct-level artefacts. A reader wanting "what does this body of research show overall?" has no entry point. Translation is per-source, not aggregated. This is the same gap that the existing `RESEARCH-REPORT.md` + addenda chain partially fills upstream, but at the layer's outputs the plan provides no equivalent.

Recommendation: add to §11 a step 13 or a §6.6-extension: *"Layer-level synthesis report — once N construct artefacts are translated, produce a layer-level synthesis (research-audience + patient-audience) that gives the reader an aggregated view. This is itself reviewer-mode-with-authorization and gets fresh-session review."*

---

## 5. What the plan does not cover

Beyond the four coverage gaps in §4.8:

1. **Reconciliation with `RESEARCH-REPORT-ADDENDUM` chain** — the addendum-chain is already doing some of what Stage S₁ / S₂ will do. The plan mentions addenda as inputs (§6.3 inputs) but does not specify whether the layer's outputs *replace* the addenda or coexist with them. Without a migration rule, the corpus accumulates two parallel synthesis surfaces (addenda + analyses/synthesis/). State the boundary explicitly: e.g. *"Addenda are the historical record up to lock date X; analyses/synthesis/ replaces addenda for new synthesis from lock date X forward. Addenda are not revised post-X."*
2. **Skill failure modes** — what if `/research-interpret` hangs, misroutes, or produces a corrupted artefact? The plan specifies the skill's responsibilities but not its error-recovery. For a layer that gates downstream stages on artefact presence, a corrupted artefact in `analyses/interpretation/` could falsely unblock S₁.
3. **Lock event for the layer plan itself** — the plan says it will become a historical scaffold after the six guides land, and may be archived. But the lock event is ambiguous: is the plan locked when all guides land, when all supporting MDs land, or when the skill is built? Specify the trigger.
4. **External-collaborator handling** — if a co-author or external reviewer wants to contribute to the patient-audience track, what is their interaction with the plain-language dictionary, the layperson-test, and the fresh-session-review discipline? The plan is single-user-implicit.
5. **Audit hooks integration with `audit_for_publication.py`** — §10 item 5 defers this. It is not actually a guide-drafting decision; it is a privacy-gate decision. Surface it.

---

## 6. Required actions (must fix before lock)

1. **Resolve §3.6 vs §6.3 conflict-resolution rule** (per §4.1) — specify which wins on conflict and how the §3.6 map is revised when §6.3 reveals a needed change. Without this, the skill cannot enforce either consistently.
2. **Swap §11 steps 3 and 5** so descriptive stocktake precedes synthesis-structure map (per §2.3). Or, if the user wants to keep the current order, add an explicit "synthesis-structure map is expected to revise after stocktake" clause to §3.6 and §11.
3. **Fix `/research-review` vs `/research-methodology-review` references** in §3.6, §4 (row 2), §11 (steps 3 and 4). Methodology MDs use the methodology-review skill per CONVENTIONS §7 and `methodology/README.md`.
4. **Reconcile §3 skipping clause with §3.6 mandate** (per §2.2) — either §3.6 accommodates single-HA-cluster skips, or §3 drops the skip clause for S₁.
5. **Re-classify the plan from "reviewer-mode-with-authorization" to producer-mode planning artefact** (per §2.1). Update §0, §2 row 5, §4 row 1, and §12 Authorship accordingly.
6. **Specify drift-check ownership in §3.7** — who runs the cadence check, by what trigger.
7. **Add the four missing anti-patterns to §9** (per §4.7) — stocktake-as-pilot, cluster-correlation-vs-causation, translation-selection, exclusion-by-omission.
8. **Add negative-finding translation discipline to §6.6** (per §4.8).

## 7. Recommended actions (should consider)

1. **Move `_open_inputs.md` out of `methodology/`** so the locked-rules folder stays clean (per §3.5 nit).
2. **Promote §10 item 8 (cadence revisit) into §3.7** so the cadence is falsifiable, not deferred (per §4.6).
3. **Strengthen §6.5 Stage A wording-discipline anti-pattern** with the expanded predictive-phrasing list (per §4.2).
4. **Add per-topic effective-n and minimum-detectable-effect-size requirement to §6.4** (per §4.8).
5. **Add cross-HA multiplicity-adjusted denominator requirement to §6.4 or §6.5** (per §4.8).
6. **Add per-paragraph version-stamp provenance to downstream artefacts** so §3.7 REVISIONs propagate at paragraph granularity (per §4.8).
7. **Add §11 step 13 (or §6.6-extension) for layer-level cross-construct synthesis** (per §4.8).
8. **Add reconciliation rule with `RESEARCH-REPORT-ADDENDUM` chain** (per §5 item 1).
9. **Specify lock event for the plan itself** (per §5 item 3).
10. **Add CONCORDANT/PARTIALLY/CONFLICT/ORTHOGONAL operational definitions in §6.3 itself** rather than deferring to the guide (per §6.3 finding).
11. **Add §3.4 crash-drop sensitivity to §8 cross-cutting constraints** (per §8 finding).
12. **Move §10 item 5 (audit_for_publication integration) to §11 step 7** as a skill-building task (per §10 finding).
13. **Add `descriptive_audit.md` to the §3.7 drift-cadence sweep** even at low intensity (per §4 row 6 finding).

## 8. What is fine as-is

- **§0 Purpose** — the six-bullet decomposition is the cleanest framing of the post-verdict pipeline the corpus has had.
- **§1 Scope and out-of-scope** — the discipline boundary between methodology specification and per-HA interpretation is correctly drawn.
- **§3 stage map (excluding the issues called out)** — the ASCII diagram, the per-stage routing, and the dependency-enforcement framing are sound.
- **§3.5 Missing-inputs as first-class** — the strongest section of the plan; the two hard rules and the open-inputs queue mechanism are genuinely load-bearing.
- **§3.8 Stopping criteria** — the user-explicitly-accepts binding event and the open-inputs-do-not-block-completion rule together solve a real failure mode.
- **§3.9 Research-line limitations** — the seven-item initial coverage and the binding-rule discipline are correctly framed.
- **§6.1 Stage D checklist** — well-anchored in upstream MDs; the interview-prompt seeds are concrete and reusable.
- **§6.2 Lived-experience prior reconciliation section** — the no-auto-resolution discipline is exactly right for an n=1 corpus where the participant has substantive priors.
- **§6.5 hard predictive gate** — correctly calibrated against Daza 2018, CENT, Natesan Batley 2023, and WWC SCED standards; the field-wide failure rate justifies the severity.
- **§6.6 anti-patterns** — the most thorough block in the plan; the tier-upgrading-in-wording example with concrete contrast is reusable across guides.
- **§7.5 Candidate skills with triggers** — the "trigger to lift" discipline is the right way to manage premature skill-building.
- **§8 Cross-cutting constraints** — correctly inherits without restating.
- **§10 Open questions deferred** — the deferral discipline is appropriate for guide-specific operational details.
- **§11 Implementation order, steps 1-2 and 6-12** — the per-guide drafting + fresh-session-review cadence and the dry-run before rollout are correctly structured. Only the step-3-vs-step-5 ordering needs fixing.
- **§12 Authorship and revision history** — honest about r2's seven-addition absorption.

---

*Reviewer: Claude (Opus 4.7, 1M context), fresh-session peer review, 2026-06-23. Doc-only knowledge; no exposure to the drafting context. Standards verified against `docs/research/literature/methodology/` PDFs (all five N-of-1 standards present and read-cited above). CONVENTIONS §1.2 / §2.2 / §3 / §4 read in full before drafting this report. HA-C4 hypothesis.md and result.md verified — plan's claim that HA-C4 is "freshly verdicted, well-documented, isolated enough that single-HA cluster is reasonable for the initial pass" is accurate (REJECTED at triad sum 0.0, INCONCLUSIVE-aware verdict bands, rich §4.11 sensitivity content for Stage D to audit).*
