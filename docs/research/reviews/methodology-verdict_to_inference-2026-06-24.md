# Methodology review — verdict_to_inference.md (r1, 2026-06-24)

**Reviewer mode**: fresh-session peer review. Reviewer is independent of the drafting session. Fresh session — no exposure to the drafting context; doc-only knowledge.
**Target**: [`docs/research/methodology/verdict_to_inference.md`](../methodology/verdict_to_inference.md) (r1, 2026-06-24)
**Review date**: 2026-06-24
**Standards applied**: [CONVENTIONS](../CONVENTIONS.md) §1, §2.1, §2.2, §3, §4 (esp. §4.3); [plan](../methodology/_plan_results_analysis_layer.md) r5 §6.2 spec + §3.5 + §3.7 + §3.8 + §3.9 + §3.10 + §3.11 + §3.12; [limitations doc](../methodology/research_line_limitations.md) r3; [synthesis map](../methodology/synthesis_structure_map.md) r3; [Stage D guide](../methodology/descriptive_precondition_audit.md) r2 LOCKED; [stocktake](../methodology/_descriptive_stocktake_2026-06-23.md).

---

## 1. Overall verdict

**REVISION RECOMMENDED (mild).** The draft is structurally faithful to plan §6.2, implements all nine sections (the spec's 8 plus the §3.5-mandated §4.9 `open_inputs`), and the five inventions beyond the spec are methodologically sound and operationally implementable. The §4.5 L-ID citation discipline correctly translates limitations doc r3 §5 into binding form (list-by-L-ID, one-sentence-per-application, NA-with-reason mandatory), and the §6.2 verdict-vs-Stage-D-audit conflict block correctly handles all four Stage D labels — including STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED, which it routes to "do not draft," matching guide #1's r2 absorption. The §7 anti-patterns are distinct from upstream plan §9 anti-patterns and from guide #1's §7. §4.6 lived-experience reconciliation is the section the guide should sweat hardest over; it does — three required content items, hard rule that it is not §3.12 commentary, smuggling check at §7.4, and structural separation enforced by §2 / §3 sectioning. The §9 phased agent-instruction outline is concrete and includes a §9.6 refuse-to-lock gate enumerating five operational checks.

Six findings drive the REVISION RECOMMENDED verdict rather than ACCEPT. Two are required (R1, R2); four are recommended (A1–A4). None blocks the §11 step 6.3 (guide #3) launch; all six are one-revision-cycle fixes.

- **R1.** §4.6's "Three required content items" describes the lived-experience prior reconciliation faithfully but the smuggling-check paragraph at the bottom of §4.6 and the §7.4 anti-pattern together do not fully cover the §6.2 spec's "lived-experience prior, if it conflicts, is logged in §6 without resolving the conflict" — specifically, the case where the prior **agrees** with the verdict needs an explicit anti-overclaim rule (an "agreement does not strengthen the claim" rule). As written, the draft implies the prior may strengthen interpretation when it agrees; this re-opens the smuggling boundary in the agreement direction. (See §4 below.)
- **R2.** The §5.5 mapping rule for triad-derived and k-of-N verdicts ("Stage I does NOT invent new verdict labels") is sound, but it gives no operational rule for the case where `result.md` emits a SUPPORTED-strong band (HA-C4 v2 §5.3 band at triad sum = 3.0 produces `SUPPORTED (strong)`). The "resolved-label family" wording would route SUPPORTED-strong to §5.1's plain SUPPORTED mapping, which is correct, but the licensed-claim sentence in §3 should preserve the "strong" qualifier — the draft does not say whether the qualifier carries forward or collapses. A Stage I dry-run on a future SUPPORTED-strong verdict would hit this. One-sentence fix.

Recommended:

- **A1.** §5's worked examples for HA-C3 v2 and HA-C3p are accurate and well-grounded in the result.md files; HA-C4c's worked example correctly characterises the (a)PASS p=0.0001 / (b)FAIL δ=+0.120 pattern as "weak-effect-but-real"; HA11-bout-redo's framing as operand fitness rather than substantive Wiggers is accurate. But HA-C3p's inverted-U / concave reading (recorded in result.md §6's 4-cell agreement matrix) is not in the draft's §5.3 worked example — only the 2-of-3 conditions framing. The result.md §6 cell that fires is a load-bearing piece of the cluster reading (Stage S₁'s job, per the draft) and a fresh Stage I drafter would benefit from a one-sentence pointer that the §6 4-cell matrix in HA-C3p is caveat-class per HA-C3p's own §6 framing.
- **A2.** §4.6's distinction between "lived-experience prior reconciliation" and §3.12 commentary is correctly framed in the operational sense, but the meta-recursion (the L4 manifestation that the LLM-assistant authors both the prior-elicitation seeds and the interpretation) is not surfaced. The limitations doc r3 explicitly carries this in L4's meta-recursion paragraph; the draft would benefit from a one-sentence acknowledgment in §4.6 that the §8.3 interview seed and the recording-verbatim discipline are the L4 mitigation reach (not a full mitigation; the §1.2 fresh-session reviewer reading the recorded prior is the structural protection).
- **A3.** The §4.9 `open_inputs` block's three refusal-to-proceed paths are well-named but one operationally important case is missing: **Stage D verdict-trust is PROVISIONAL and user has not yet accepted the PROVISIONAL-carrying-forward flag**. The §6.2 + §9.2 flow says "on user rejection, halt and produce only the §4.9 open_inputs entries inheriting from the audit's §5" — this is a fourth refusal-to-proceed path that the §4.9 enumeration does not name. Add as a fourth bullet for symmetry with §9.2's halt-and-produce-open_inputs branch.
- **A4.** Length and density. 1399 lines is operationally necessary given the nine-section outline + §5 mapping rules + §6 conflict rules + §7 anti-patterns + §8 interview seeds + §9 agent-instruction outline + §10 cross-references — every section pulls weight. But §4.3 (what the verdict licenses) and §5 (verdict-to-claim mapping rules) overlap substantially; §4.3's SUPPORTED/REJECTED/PARTIAL/INCONCLUSIVE rules and §5.1–§5.4's mapping rules say the same thing twice with different framings. Either §4.3 could be compressed to "see §5 for the per-label mapping rules" or §5 could be made shorter by cross-referencing §4.3. Not load-bearing; recommend the §4.3-points-at-§5 form for the next revision pass.

## 2. Four-input bar findings (CONVENTIONS §2.2)

This MD is producer-mode infrastructure (per §3 of the target, per plan §4 row "Guide MDs (6×)") rather than a methodology MD locking a substantive analytical choice; the four-input bar applies in lighter form. Two of the four inputs apply directly; two apply indirectly.

| Input | Status | Reasoning |
|---|---|---|
| 1. Best-practices standards | PASS | The verdict-to-claim mapping shape (per-label licensed/not-licensed surfaces; operationalisation-bound default; effect-size-direction in every licensed-claim sentence) traces to N-of-1 inference standards (Daza 2018 within-subject inference reach; CENT items 21+22 limitations + generalisability; SCRIBE participant-as-researcher transparency; Natesan 2023 defensible-single-case bar). The cited PDFs all exist at the named paths. |
| 2. Established literature | PASS | The §2 inputs list cites all four literature methodology anchors with one-sentence operational role per anchor (Daza for inference reach; CENT for limitations + generalisability; SCRIBE for analyst-is-subject transparency; Natesan for defensible verdict-to-claim translation). The body of the guide uses the anchors (§3 cites Daza on hypothesis-generating prior; §4.5 example cites Daza on N-of-1 inference bounds; §4.8 cites the discipline behind external-research scoping). This is stronger than guide #1's use of the same anchors. |
| 3. Tradeoff vision | PASS | §1 carries an explicit "Alternatives considered" paragraph (per CONVENTIONS §2.2 item 3) naming two rejected paths — self-interpretation in result.md (rejected for same-session blind-spots + commensurability cost) and collapsing Stage I into Stage S₁ (rejected because single-HA clusters skip the verdict-to-claim discipline). This is stronger than guide #1's r1 framing (which absorbed an alternatives paragraph only at r2). |
| 4. Research limitations + objectives | PASS | The §5 worked examples draw from the four ready HAs per the synthesis-structure map's §2 initial scope; the §6.2 conflict block handles all four Stage D verdict-trust labels including STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED; the §4.5 L-ID citation discipline matches the synthesis-structure map's §3 per-cluster L-IDs columns. Designed-for-this-corpus is unambiguous. |

Overall: 4 PASS. The four-input compliance is the strongest aspect of the draft. The "alternatives considered" framing in particular shows that the §11 step 6.1 review-absorption discipline propagated into this guide as a drafting convention.

## 3. Faithfulness to §6.2 spec

§6.2 has nine listed elements (purpose, inputs, output, 8-section outline, checklist, conflict rules, anti-patterns, interview seeds, agent-instruction outline) plus the cross-reference forward pointer. Mapping:

| §6.2 element | Implementation | Faithfulness |
|---|---|---|
| Purpose | §1 (purpose + where it sits + what it does not do) | **Faithful with extension.** The extension is the "What Stage I does NOT do" five-bullet list (re-test / predictive claims / commentary / new caveats / re-framing), which operationalises §6.2's purpose paragraph into anti-pattern preview. Sound. |
| Inputs | §2 (seven numbered inputs) | **Faithful with extension.** §6.2 names five inputs (hypothesis.md, result.md, Stage D audit, CONVENTIONS §4.1-§4.3, literature methodology). §2 expands to seven by adding limitations doc + synthesis-structure map. Both extensions are sound and binding (the limitations doc r3 §5 requires §4.5 L-ID citation; the map r3 §3 scopes the L-ID list). |
| Output | §3 (path + naming convention + flat-no-subfolder + mode + L-ID citation discipline) | **Faithful with extension.** §6.2 specifies `analyses/interpretation/HA-XX.md` (by-HA, flat naming per plan §2 + §5). §3 specifies the flat-no-per-HA-subfolder convention explicitly and justifies the difference from Stage D's per-HA folder. Sister-HA discipline (each sister gets its own interpretation) added — sound. The §3 closing block translates limitations doc §5 binding into the output-level discipline. |
| Section outline | §4 (9 sub-sections, §4.1–§4.10 with §4.4 misnumbered) | **Faithful with extension.** §6.2 names 8 sections; §4 implements 8 + §4.9 `open_inputs` (added per §3.5 plan binding) + §4.7 closure-path-statement section (the §6.2 spec mentioned "explicit statement of what would upgrade" PARTIAL/INCONCLUSIVE in the checklist — the draft hoisted it to a section). Both extensions sound. **Minor numbering inconsistency**: §4 sub-section count is 10 sub-headers (§4.1 through §4.10), but the section count claim is "nine sections." The §4.10 cross-references section is the ninth content-section + the §10 cross-references at the doc level; the draft labels both the "cross-references inside the per-HA interpretation MD" and the "cross-references inside this guide MD" by similar names, which is confusing. (See §6 below.) |
| Checklist | Folded into §4 sub-sections + §5 mapping rules | **Faithful.** The §6.2 checklist's seven bullets are implemented across the §4 sub-sections — verdict-verbatim (§4.1), operationalisation-language-preserved (§4.3), effect-size-reported (§4.3 rule 2), PARTIAL/INCONCLUSIVE upgrade statement (§4.7), no-new-post-hoc-framing (§7.3 anti-pattern), confirmatory-vs-exploratory-from-pre-reg (§4.3 + §4.6 + §4.5 L4 citation), lived-experience-prior-in-§6-without-resolving (§4.6 + §6.1). This is the right place to fold them; a separate §-checklist section would be redundant. |
| Conflict rules | §6 (3 rules) | **Faithful with extension.** §6.2 names 2 conflict rules (verdict vs prior; verdict vs descriptive audit). §6 implements both (§6.1, §6.2) and adds §6.3 (verdict vs cluster-level expectation; Stage I does NOT pre-empt the cluster coherence call). Extension sound — it prevents Stage I from leaking into Stage S₁'s territory. |
| Anti-patterns | §7 (9 anti-patterns) | **Faithful with extension.** §6.2 names 5 anti-patterns (REJECTED→hypothesis false; SUPPORTED→mechanism correct; reframing the hypothesis; smuggling the prior; PARTIAL as weak SUPPORTED). §7 implements all 5 (§7.1, §7.2, §7.3, §7.4, §7.6) and adds 4 more (§7.5 inventing-new-caveats; §7.7 producing §3.12 commentary; §7.8 computing predictive-quality measures; §7.9 inventing-new-verdict-labels). All four additions sound — see §4 below. |
| Interview seeds | §8 (3 required + 1 optional) | **Faithful with extension.** §6.2 names 3 seeds (verdict-to-claim licensing; competing-operationalisation narrowing; lived-experience reconciliation). §8 implements all 3 (§8.1, §8.2, §8.3) and adds §8.4 (verdict-trust audit confirmation). Sound and operationally cheap, matches guide #1's §8.4 pattern. |
| Agent-instruction outline | §9 (8 phases) | **Faithful with extension.** §6.2 names 5 bullets (Load / Refuse / Walk / Produce / Recommend). §9 expands to 8 phases (Load / Gate / Extract / Interview / Produce / Refuse-to-lock-gate / Review-handoff / Acceptance+drift). The Acceptance+drift phase implements §3.7 + §3.8 (drift triggers, user-acceptance-as-lock) absent from §6.2's outline; the Refuse-to-lock gate enumerates five operational checks. Both extensions correct because the relevant plan rules post-date §6.2's sketch. |

No §6.2 element is missing or substantively altered. Spec faithfulness is high — higher than guide #1 r1 (which had the L-ID-citation tension and the figures-vs-plots collision and the label-count contradiction). The drafter's self-report of having followed every discipline lesson from guide #1's review absorption is borne out in the draft.

## 4. The five inventions beyond §6.2

### Invention 1 — §4.7 closure-path-statement hoisted to its own section header

**Sound.** The §6.2 spec mentioned "explicit statement of what would upgrade" PARTIAL / INCONCLUSIVE in the checklist; the draft hoists it to a section header with operational guidance for each verdict-band combination. The structural uniformity argument is correct — every Stage I artefact has the same nine sub-section count, with §4.7 collapsing to "NA" for SUPPORTED / REJECTED verdicts. This is the same belt-and-suspenders pattern guide #1 used for the §4.5 `open_inputs` block (every audit has the section even when empty). No conflict with locked layer rules. The closure-path framing for INCONCLUSIVE cells inside a verdict (e.g. HA-C4 v2 Ch3 validate at n=25 < 30) is operationally correct: the closure path is corpus accrual vs operationalisation revision, and the draft cites the §4.11.3 chain-relaxed sensitivity arm as an example of the latter that already exists as descriptive.

### Invention 2 — §5 worked examples drawn from the four ready HAs

**Sound and accurate.** Spot-checked against result.md files:

- **HA-C3 v2 (§5.2)**: "REJECTED (wrong-direction override)" — matches result.md §1 verdict ("REJECTED (wrong-direction override)") + §3 verdict block. The "S is significantly NEGATIVE (concave, not convex)" mechanism in result.md §6 is correctly summarised as "the observed signal points in the inverse of the Wiggers-predicted direction." Operationalisation-bound framing ("Wiggers-verbatim 4-bin absolute-numerical operationalisation on Stratum 4 unmedicated primary cell") matches §1 headline cell. Sister-HA cross-reference to HA-C3p PARTIAL is named with the correct cluster routing pointer.
- **HA-C3p (§5.3)**: "PARTIAL (2-of-3 conditions MET)" — matches result.md §1 verdict + §3 verdict block. The 2-of-3 framing ("p_b spline-F + p_c convexity-contrast MET; p_a Jonckheere monotone NOT MET") is correctly preserved as part of the claim shape. But A1 above: the result.md §6 4-cell agreement matrix cell that fires is "Wiggers' numbers wrong-for-this-participant but the underlying SHAPE IS REAL (non-linear) in the INVERSE direction (concave / inverted-U)" — this lived inverted-U reading is what the cluster-level coherence call at Stage S₁ will wrestle with, and a fresh Stage I drafter on HA-C3p would benefit from a one-sentence pointer to it (with the caveat that HA-C3p's §6 itself marks the matrix as caveat-class post-hoc).
- **HA-C4c (§5.3)**: "PARTIAL" — matches result.md §1 verdict. The "(a)PASS p=0.0001 / (b)FAIL δ=+0.120" pattern is correctly characterised as "weak-effect-but-real" in the §5 framing language. The cross-phase-pooling caveat is correctly named as the closure-path question. The cascade-precondition relationship to HA11-bout-redo is correctly preserved.
- **HA11-bout-redo (§5.3)**: "PARTIAL (2 of 3 framework-validity bars met)" — matches result.md §1 verdict. The framework-validity-NOT-substantive framing is correctly preserved (result.md §7 caveat 3 is the binding source; the draft's §5.3 worked example reads it cleanly). The operand-fitness vs substantive-claim distinction is preserved in the §4.4 "does not license" pointer. The cascade arrow to HA-C4c is correctly framed as caveat-class precondition rather than co-equal evidence.

The worked examples are the strongest section of the draft. No HA mischaracterisation; no verdict relabeling; the operationalisation-bound discipline of §4.3 is enforced uniformly across the four examples.

### Invention 3 — §5.5 triad-derived and k-of-N verdict mapping rule

**Sound, with one operational gap (R2 above).** The "resolved-label family" mapping rule (REJECTED inherits §5.2; PARTIAL inherits §5.3; SUPPORTED inherits §5.1; INCONCLUSIVE inherits §5.4) is the right reduction discipline — Stage I does not need to invent per-shape rules for every possible result.md verdict-band ontology. The rule that the §3 licensed-claim sentence MUST respect the verdict's internal aggregation (per-channel verdicts for triad; per-condition met/unmet pattern for k-of-N; direction-of-failure for wrong-direction-override) is correct.

But the rule does not cover SUPPORTED-strong (HA-C4 v2 §5.3 band at triad sum = 3.0 produces `SUPPORTED (strong)`). The "resolved-label family" wording would route SUPPORTED-strong to §5.1's plain SUPPORTED mapping, but the licensed-claim sentence in §3 should preserve the "strong" qualifier. The draft does not say whether the qualifier carries forward (i.e. the licensed-claim sentence reads "SUPPORTED (strong)" with the "(strong)" preserved verbatim) or whether it collapses to plain SUPPORTED with the strength encoded in the effect-size magnitude. A Stage I dry-run on any future SUPPORTED-strong verdict would hit this; a one-sentence fix ("qualifier preserves verbatim in the §3 licensed-claim sentence") closes it.

### Invention 4 — §6.2 PROVISIONAL conflict rule "narrows by at most one tier"

**Sound.** The §6.2 spec said "PROVISIONAL interpretation flagged as such" without specifying the narrowing tier discipline; the draft cross-references plan §3.5's hard rule on no-silent-degradation ("always at most one tier narrower than the claim being blocked"). This is the right cross-reference — the PROVISIONAL narrowing is structurally identical to the §3.5 fallback-claim discipline, and naming the tier rule explicitly prevents PROVISIONAL from becoming a vague "we narrowed it a bit" hedge. The worked example in §6.2 ("a SUPPORTED verdict's licensed claim narrows from 'the operationalisation discriminated heavy-T from non-heavy-T at δ=X' to 'the operationalisation discriminated heavy-T from non-heavy-T at δ=X under the PROVISIONAL-audit caveat that [the NOT BACKSTOPPED assumption] could not be confirmed'") is concrete enough that a Stage I drafter will know what "narrows by one tier" means in practice.

### Invention 5 — §9.6 refuse-to-lock gate enumerating five operational checks

**Sound.** The five checks (L-ID missing from §4.5 citation block per map row; §4.4 missing one of four predictable overclaim shapes; §4.8 external-research suggestion without N=1-limit scoping; §4.6 divergence without both readings or resolution-path; §3/§2 verdict-overclaim language violating §7 anti-patterns) are the right structural gates. Each maps to a §4 sub-section requirement, so the gate is implementable as a skill-level check rather than as judgment. The "explicit user-accept-PROVISIONAL" action recorded in the lock log (per §6.2) is the right escape hatch for the third gate.

One refinement: the fifth gate ("§3 / §2 contain verdict-overclaim language that violates §7 anti-patterns") is text-pattern detection and harder to enforce as a skill-level check than the first four. The skill will need a heuristic for this (e.g. presence of "predicts", "forecasts", "X means Y" in §3 / §2 triggers the gate). The draft does not specify the heuristic. Not blocking; a §9.6-level refinement could add "the skill applies pattern detection on the forbidden language list from §7.7 + §7.8 to §3 / §2 text."

## 5. Per-section findings

### §1 Purpose

Sound. The block-quote framing ("A verdict label is not a finding. Stage I pins the verdict-to-claim mapping so interpretations across the corpus are commensurate") matches plan §6.2's opening exactly. The five-bullet "what Stage I does NOT do" is helpful scope-clarification — particularly the §3.12 commentary boundary and the §3.10 predictive-claim boundary, both of which Stage I is structurally exposed to crossing. The "alternatives considered" paragraph satisfies CONVENTIONS §2.2 item 3 explicitly. The skill-precondition note ("no Stage I interpretation artefact can be drafted before §11 step 7 lands") matches guide #1's r2 framing and is operationally important.

### §2 Inputs

Sound. The seven numbered inputs are right, with §6.2's five plus the layer-level limitations doc + synthesis-structure map as binding additions. The closing "what the interpretation does NOT load" paragraph (test.py / per-day per-cell values / raw descriptive runs for new analyses) is the right negative-space discipline.

**Minor framing concern.** Input #3 (the Stage D audit) cites "TRUSTED unblocks; DOWNGRADED-INCONCLUSIVE-PROVISIONAL unblocks under explicit user acceptance; REQUIRES-DESCRIPTIVE-WORK and STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED block." The third state (STRUCTURALLY-UNTESTABLE) is described as "block" but §6.2 of the draft and §9.2 of the agent-instruction outline say the interpretation is **not drafted at all** (the artefact never gets a draft, vs REQUIRES-DESCRIPTIVE-WORK which produces an open_inputs-entries-only artefact). The Input #3 framing is correct as a verdict label but slightly under-specifies the two different routing paths; suggest one extra sentence distinguishing them.

### §3 Output

Sound on the artefact path + flat naming convention + mode + L-ID citation discipline.

The justification for the flat naming convention ("Stage I has no plot output and produces only the single MD") matches the map r3 §2 declared output path (`analyses/interpretation/HA-XX.md`) and the locked plan §5 output-structure tree exactly. The contrast with Stage D's per-HA folder convention is correctly framed as intentional, not as oversight.

The "L-ID citation discipline at the output level" closing block is the right place to bind the limitations doc r3 §5 row into the output spec. The "union of the cluster row's L-IDs PLUS any L-ID the HA's primary-signal usage triggers independently" rule is operationally correct and matches the L5 surface paragraph in guide #1's §5.5.

### §4 Section outline for the produced interpretation.md

Sound. The nine sub-sections cover §6.2's eight plus the §4.9 open_inputs (§3.5-mandated) plus the §4.7 closure-path-statement (the §6.2 checklist mention hoisted).

**§4.1 (target HA + verdict)**: sound; the verbatim-copy rule + Stage D audit lock-date reference is the right header discipline. The four Stage D verdict-trust labels are correctly enumerated.

**§4.2 (what the data shows)**: sound; the "no use of the verdict label in this section" hard rule is the right belt-and-suspenders discipline against §4.4 anti-pattern smuggling. The worked example for HA-C4 v2 is descriptive paraphrase without claim language — correctly demonstrates the discipline.

**§4.3 (what the verdict licenses)**: sound; the two binding rules (operationalisation-bound default; effect-size-direction in every licensed-claim sentence) are right. The per-verdict-label sub-rules (SUPPORTED / REJECTED / PARTIAL / INCONCLUSIVE) overlap with §5 — recommend the §4.3-points-at-§5 form for the next revision (A4 above).

**§4.4 (what the verdict does NOT license)**: sound; the four predictable overclaim shapes (REJECTED→hypothesis false; SUPPORTED→mechanism correct; PARTIAL as weak SUPPORTED; INCONCLUSIVE as leaning) are the right four. The HA-C4 v2 partial-positive worked example correctly addresses the selective-reading overclaim. The §6.2 spec listed 5 §6.2-explicit overclaims (the four + the smuggling-prior anti-pattern §7.4); the draft routes the prior-smuggling to §4.6 / §7.4 rather than §4.4, which is the right separation.

**§4.5 (caveats narrowing the claim, with L-ID citation block)**: this is the most operationally important section and the draft executes it well. The two sub-blocks (pre-reg + audit caveats vs L-ID citation block) are the right separation. The HA-C3 v2 worked example correctly cites L1 + L2 + L3 + L4 + L6 + L7 with L5 NA — and the L-ID list matches the synthesis-structure map's `C-stress-fatigue-shape` row exactly. The hard rule that NA citations require a one-sentence project-specific reason is correctly enforced. The hard rule that the §5b L-ID citation block cannot be empty (or missing an L-ID the cluster row lists) is enforced at §9.6 gate 1.

**§4.6 (lived-experience prior reconciliation)**: this is the section most at risk per the L4 limitation, and the draft sweats it. Three required content items, hard rule that it is NOT §3.12 commentary, smuggling check that the prior does not get to override the verdict in §3 even if the user feels strongly. The structural separation (§2 descriptive paraphrase, §3 what-the-verdict-licenses, prior enters only in §4.6) is the right discipline. **But R1 above**: the draft does not handle the agreement case explicitly. The §6.1 conflict rule "Log both, do NOT resolve in this artefact" and the §4.6 paragraph "If the prior agrees with the verdict, the paragraph says so" together leave a gap: the prior's agreement does not strengthen the licensed claim in §3 (which would be the smuggling-in-the-agreement-direction). The hard rule should make this explicit: "agreement does not strengthen the licensed claim; the licensed claim is what §4.3 says, regardless of whether §4.6 records agreement or divergence."

**§4.7 (closure-path statement)**: sound; the per-verdict-band guidance (PARTIAL k-of-N, PARTIAL wrong-direction, INCONCLUSIVE cells, SUPPORTED/REJECTED NA) is operationally complete.

**§4.8 (follow-up suggestions, own + external)**: sound; the four-HA worked examples (HA-C3 v2 + HA-C3p sister; HA-C4c unmedicated-only sister; HA11-bout-redo extended-window) are concrete pre-reg shapes rather than vague directions. The external-research-N=1-scoping requirement is correctly inherited from plan §3.11 + the §9 unscoped-follow-up-fallacy from the locked plan. Per the agent's self-report, the "per §3.11" reference in §6.2 spec was interpreted as binding the external-research-N=1-scoping requirement; this interpretation is **correct** — the plan §3.11 explicitly says "every external-research suggestion must explicitly state which aspect of our N=1 limits prevents us from answering the question ourselves."

**§4.9 (open_inputs block)**: sound; the three refusal-to-proceed paths (Stage D audit missing; Stage D audit REQUIRES-DESCRIPTIVE-WORK; lived-experience prior cannot be reconciled in-session) are operationally distinct. **A3 above**: a fourth refusal-to-proceed path (Stage D PROVISIONAL + user has not yet accepted PROVISIONAL-carrying-forward) should be added for symmetry with §9.2.

**§4.10 (cross-references)**: sound; the seven destinations (hypothesis.md + result.md; Stage D audit; map row; sister-HA interpretations; Stage S₁ forward pointer; limitations cross-refs; literature methodology anchors) are the right scope.

### §5 The verdict-to-claim mapping rules

Sound (with R2 above on SUPPORTED-strong handling). The per-label mapping rules + worked examples are well-executed. The §5.5 "Stage I does NOT invent new verdict labels" rule + "resolved-label family" mapping is the right reduction discipline.

**Suggested swap (A1)**: the HA-C3p §5.3 worked example would benefit from a one-sentence pointer to the result.md §6 4-cell matrix's inverted-U / concave reading (with the caveat that HA-C3p's own §6 marks it as caveat-class post-hoc not substantive). This is the cell that fires at the cluster-level reading at Stage S₁; flagging it at Stage I level helps the downstream synthesis drafter.

### §6 Conflict rules

Sound. §6.1 (verdict vs lived-experience prior) is the §6.2 spec rule + three resolution paths (Stage S₁ cross-operationalisation, sister-HA construction, stays open) — operationally complete. §6.2 (verdict vs Stage D audit PROVISIONAL flag) correctly handles all four Stage D labels including STRUCTURALLY-UNTESTABLE (route to "do not draft" — matches guide #1 r2 absorption). §6.3 (verdict vs cluster-level expectation; Stage I does NOT pre-empt the cluster coherence call) is the right boundary — Stage I cites the cluster routing in §4.10 + §4.8 but does not pre-empt.

### §7 Anti-patterns

Sound. The nine anti-patterns + the §6.2 spec's five are correctly mapped (§7.1 = REJECTED→hypothesis false; §7.2 = SUPPORTED→mechanism correct; §7.3 = reframing the hypothesis; §7.4 = smuggling the prior; §7.6 = PARTIAL as weak SUPPORTED). The four additions (§7.5 inventing new caveats; §7.7 §3.12 commentary at Stage I; §7.8 predictive-quality measures; §7.9 inventing new verdict labels) are the right boundary-enforcement anti-patterns for the layer-cross-cutting rules §3.10 + §3.12.

The §7.7 anti-pattern (producing §3.12 subject-narrative commentary at Stage I) is the right defence against the §3.12 commentary boundary; the wording "first-person narrative ... does not belong in §4.6 either" correctly extends the boundary to §4.6 itself. The §7.8 anti-pattern (computing or citing predictive-quality measures) is the right defence against the §3.10 hard predictive gate. Both anti-patterns map cleanly to plan §3.10 + §3.12 binding rules.

### §8 Interview-prompt seeds

Sound. The three required seeds (verdict-to-claim licensing; competing-operationalisation narrowing; lived-experience reconciliation) match §6.2 spec verbatim. The optional fourth (verdict-trust audit confirmation) is operationally cheap and parallels guide #1's §8.4. The cross-check discipline in §8.1 (user articulates licensed claim, skill cross-checks against §5 mapping rules + §7 anti-patterns, mismatches surfaced) is the right belt-and-suspenders for the §9.6 refuse-to-lock gate.

### §9 Agent-instruction outline

Sound. The eight phases (Load / Gate / Extract / Interview / Produce / Refuse-to-lock-gate / Review-handoff / Acceptance + drift-trigger registration) are concrete and operationally implementable. The §9.6 refuse-to-lock gate (five specific checks) is the right structural-protection layer.

**One operational gap on §9.2**: the four Stage D verdict-trust labels are correctly routed (TRUSTED → §9.3; PROVISIONAL → user-accept-or-halt; REQUIRES-DESCRIPTIVE-WORK → halt; STRUCTURALLY-UNTESTABLE → do-not-draft). But the boundary between "halt and produce open_inputs entries" (REQUIRES-DESCRIPTIVE-WORK) and "do not draft" (STRUCTURALLY-UNTESTABLE) is operationally subtle — under STRUCTURALLY-UNTESTABLE, does the interpretation MD exist at all (perhaps as a stub naming the routing) or is the absence of the artefact itself the routing record? Guide #1's §6.2 r2 absorption added a "terminal-state entry" pattern for the audit's STRUCTURALLY-UNTESTABLE case; Stage I should mirror that pattern explicitly. The draft's §9.2 reads "the Stage I interpretation file is not produced at all" — this is the right call, but it should explicitly cross-reference where the routing IS recorded (presumably the Stage D audit's terminal-state entry per guide #1).

### §10 Cross-references

Spot-checked links (per request 11):

- `_plan_results_analysis_layer.md` § references (6.2, 3.5, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 4, 11 step 6.2) — all exist in the plan (verified).
- `descriptive_precondition_audit.md` § references (3, 4.4, 5, 6.1, 7) — all exist in the locked guide r2 (verified).
- `research_line_limitations.md` § references (3, 5, 8) — all exist in the locked doc r3 (verified).
- `synthesis_structure_map.md` § references (2, 3, 4, 5) — all exist in the locked map r3 (verified; r3's per-cluster L-IDs columns match the §4.5 worked example for HA-C3 v2).
- `_descriptive_stocktake_2026-06-23.md` § references (3, 4) — verified to exist.
- `hypothesis_lock_process.md` — referenced for sister-HA construction; verified to exist.
- Four literature methodology PDFs (Daza 2018, Shamseer / CENT 2015, Tate / SCRIBE 2016, Natesan 2023) — all exist at the named paths under `literature/methodology/` (verified via Glob).
- Five HA result.md references (HA-C3 v2, HA-C3p, HA-C4 v2, HA-C4c, HA11-bout-redo) — all exist at the named paths under `analyses/hypotheses/` (verified).

The cross-reference layer is in good shape; no broken links found in the spot-check.

### §11 Lock log

Sound. Single entry recording the r1 draft, the five inventions, the two §6.2-spec ambiguities resolved by interpretation, and the four drift triggers (manual-pending-skill per guide #1's pattern). Matches the lock-log convention established by the limitations doc r3, map r3, and Stage D guide r2.

## 6. Cross-cutting concerns

### §3.10 hard predictive gate boundary

Strongly enforced. The §1 "what Stage I does NOT do" list, §4.4 anti-pattern #4 (INCONCLUSIVE as leaning), §5 mapping rules (no predictive language in any licensed-claim sentence), §7.8 anti-pattern (no PPV, base rate, sensitivity, specificity, false-alarm rate, lead time, reliability), §9.6 refuse-to-lock gate check 5 (verdict-overclaim language detection) all close the boundary. The forward pointer to Stage A is correctly named but no Stage I content crosses it. Hardest check: §3 licensed-claim sentences in the worked examples (§5.1–§5.4) — none of them carry predictive-tier language. Pass.

### §3.12 commentary boundary

Strongly enforced. §1 "what Stage I does NOT do" list, §4.6 hard rule (§4.6 is NOT §3.12 commentary; operational distinction at verdict-vs-prior epistemic layer vs patient-facing-narrative layer), §7.7 anti-pattern (first-person narrative does not belong in §4.6 either), §9.6 refuse-to-lock gate check 5 all close the boundary. The §4.6 "third-person-or-recorded-prior voice" requirement is the right structural enforcement. Pass.

### §3.11 follow-up suggestions implementation

Strongly enforced. §4.8 implements both tracks (own-research + external-research) per the §3.11 binding. The external-research-N=1-scoping requirement is correctly named ("every external-research suggestion MUST explicitly name the N=1 limit that prevents us from answering the question ourselves") and the §9 unscoped-follow-up-fallacy is cited as the prohibition. The §9.6 refuse-to-lock gate check 3 enforces this at the skill level. The "distinct from open_inputs" cross-reference is the right separation (§4.8 = next claims; §4.9 = what is missing for this claim). Pass.

### L-ID citation discipline implementation

Strongly enforced. §4.5 implements the limitations doc r3 §5 binding ("Cite every limitation that touches the HA's primary signals or operationalisation. List by L-ID with one-sentence project-specific application") faithfully. The list-format is mandatory (§9.6 gate 1). NA-with-reason rows are required (the §4.5 hard rule "A citation that reads 'L3 (device generations) NA' without an explanation is forbidden; the NA call requires the same one-sentence project-specific reason as the apply call"). The L-ID mapping example for HA-C3 v2 aligns with the synthesis-structure map's `C-stress-fatigue-shape` row exactly (L1, L2, L3, L4, L6, L7 cited; L5 NA — matches map row column).

### Stage D upstream-gate discipline

Strongly enforced. The §2 inputs require the Stage D audit. The §6.2 conflict rules handle all four Stage D verdict-trust labels (TRUSTED proceeds; PROVISIONAL proceeds under explicit user-accept; REQUIRES-DESCRIPTIVE-WORK blocks; STRUCTURALLY-UNTESTABLE does-not-draft). The §9 agent-instruction outline encodes the refusal at §9.2 (gate) and §9.5 (produce-or-halt). The §4.9 refusal-to-proceed paths produce open_inputs entries per plan §3.5 hard rule. **One small fragmentation**: the four labels' routing is split across §2 (input description), §4.1 (header recording), §6.2 (conflict rule), §9.2 (gate behaviour). The same four labels appear in three places with slightly different framings — consistency check passes (no contradictions) but a future reader has to triangulate. Minor.

### Sibling naming consistency

The draft uses `analyses/interpretation/HA-XX.md` (flat, no per-HA subfolder; contrast to Stage D's per-HA folder). Verified against map r3 §2 (output path declaration) and §5 (conventions paragraph). Match. The justification for the difference from Stage D's per-HA folder convention is correctly named (Stage I has no plot output).

### Length and density

1399 lines is ~38% longer than guide #1's 1008. Per A4 above, the length is operationally necessary at the §-by-§ level — every section pulls weight. The redundancy that could be cut is the overlap between §4.3 (what the verdict licenses) per-verdict-label sub-rules and §5 (verdict-to-claim mapping rules); the same SUPPORTED / REJECTED / PARTIAL / INCONCLUSIVE rules appear in both sections with different framings. Compressing §4.3 to "see §5 for the per-label mapping rules" would save ~80 lines without losing content. Not blocking; a §11 step 8 dry-run on HA-C4 would surface whether the §4.3-§5 overlap is operationally useful redundancy or cuttable redundancy.

### What would block a Stage I dry-run on HA-C4

Concretely: if a Stage I drafter loaded this guide and tried to interpret HA-C4 v2 tomorrow, the operational gaps they would hit are:

1. **SUPPORTED-strong qualifier handling** (R2 above). HA-C4 v2's verdict is "REJECTED (triad sum = 0.0 / 3.0)" so this gap does not bind for HA-C4 v2 specifically; but HA-C4c v2 (hypothetical future re-run) or any future HA with a triad sum ≥ 3.0 would hit it.
2. **Agreement-direction smuggling** (R1 above). If the user's prior on HA-C4 v2 agrees with REJECTED ("yeah, I never thought the chain-T+1 daily-aggregate triad would discriminate at the corpus's effective n"), the §4.6 paragraph should explicitly note that agreement does not strengthen the §3 licensed claim.
3. **PROVISIONAL not-yet-accepted refusal path** (A3 above). If HA-C4 v2's Stage D audit lands as PROVISIONAL (e.g. A3 block-length sensitivity not fully closed on the Ch3 derivative), the §4.9 open_inputs path for "user has not yet accepted PROVISIONAL-carrying-forward" is not explicitly enumerated.

None of these three would block a Stage I drafter from producing a usable interpretation of HA-C4 v2 (which is REJECTED with TRUSTED audit, by all current evidence) — but all three should be closed before the §11 step 8 dry-run formalises the skill behaviour against the four ready HAs.

## 7. Required actions to absorb before LOCK

- **R1.** §4.6 add explicit "agreement does not strengthen the licensed claim" rule. The §3 licensed claim is what §4.3 says, regardless of whether §4.6 records prior-verdict agreement or divergence. One-sentence addition to the §4.6 hard rule block + §7.4 anti-pattern wording.

- **R2.** §5.5 add explicit rule for SUPPORTED-strong qualifier preservation (or collapse) in the §3 licensed-claim sentence. The "resolved-label family" mapping should specify whether triad-derived qualifiers (SUPPORTED-strong, k-of-N) carry forward verbatim or collapse to plain SUPPORTED with strength encoded in the effect-size magnitude. One-sentence addition to §5.5.

## 8. Recommended actions to absorb before LOCK (optional)

- **A1.** §5.3 HA-C3p worked example: add one-sentence pointer to result.md §6 4-cell matrix's inverted-U / concave reading, with the caveat that HA-C3p's own §6 marks it as caveat-class post-hoc not substantive (so Stage I cites it as descriptive context only, not as substantive interpretation).

- **A2.** §4.6 add one-sentence acknowledgment of the L4 meta-recursion (the LLM-assistant authors both the prior-elicitation seeds and the recording-of-prior). The §8.3 interview seed and the recording-verbatim discipline are the L4 mitigation reach; the §1.2 fresh-session reviewer reading the recorded prior is the structural protection. Aligns with limitations doc r3 L4's meta-recursion paragraph.

- **A3.** §4.9 add fourth refusal-to-proceed path: Stage D verdict-trust is PROVISIONAL and user has not yet accepted the PROVISIONAL-carrying-forward flag. The §9.2 gate already handles this case ("on user rejection, halt and produce only the §4.9 open_inputs entries inheriting from the audit's §5"); §4.9 should enumerate it symmetrically with the three existing paths.

- **A4.** §4.3 + §5 compression. The per-verdict-label sub-rules in §4.3 and the verdict-to-claim mapping rules in §5 overlap substantially. Recommend the §4.3-points-at-§5 form for the next revision pass (saves ~80 lines without losing content). Not blocking.

## 9. Confirmed-good

The following elements of the draft are sound and need no revision:

- §1 purpose framing + alternatives-considered paragraph + skill-precondition note.
- §2 seven-input list (the §6.2 spec's five + limitations doc + synthesis-structure map).
- §3 output spec + flat-no-per-HA-subfolder convention + sister-HA each-gets-its-own discipline + L-ID citation discipline at output level.
- §4.1 mechanical header (verdict verbatim, Stage D audit lock date, operationalisation summary, cluster row reference).
- §4.2 descriptive-paraphrase-no-claim-language rule + HA-C4 v2 worked example.
- §4.3 operationalisation-bound default rule + effect-size-direction rule + per-verdict-label sub-rules (modulo A4 compression).
- §4.4 four predictable overclaim shapes + HA-C4 v2 partial-positive worked example.
- §4.5 two sub-blocks (pre-reg + audit caveats vs L-ID citation block) + HA-C3 v2 worked example + hard rules (no empty §5b; NA-with-reason required).
- §4.6 three required content items + no-auto-resolution rule + §3.12-commentary boundary (modulo R1 agreement-direction smuggling fix).
- §4.7 closure-path statement (per-verdict-band guidance + NA framing for SUPPORTED/REJECTED).
- §4.8 own-research + external-research tracks + N=1-scoping discipline + four-HA worked examples + distinct-from-open_inputs cross-reference.
- §4.9 three refusal-to-proceed paths + skill-aggregation cross-reference (modulo A3 fourth path).
- §4.10 seven cross-reference destinations.
- §5.1–§5.4 per-label mapping rules + worked examples (modulo R2 SUPPORTED-strong handling + A1 HA-C3p inverted-U pointer).
- §5.5 triad-derived + k-of-N reduction rule (modulo R2).
- §6.1–§6.3 three conflict rules (verdict vs prior; verdict vs Stage D PROVISIONAL; verdict vs cluster expectation).
- §7.1–§7.9 nine anti-patterns including the four extensions beyond §6.2 spec.
- §8.1–§8.4 three required seeds + one optional verdict-trust confirmation seed.
- §9.1–§9.8 eight-phase agent-instruction outline including the §9.6 refuse-to-lock gate.
- §10 cross-references (all spot-checks pass).
- §11 lock log (per established convention).

The four ready HAs (HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo) are well-served by this guide: a Stage I drafter loading the guide tomorrow would have an operationally clear procedure for each, modulo the six recommended fixes above.

---

**Reviewer recommendation**: absorb R1 + R2 (one-revision-cycle fixes); A1–A4 are optional. After R1 + R2 absorption, the guide can LOCK without a second fresh-session review per the established Option-γ pattern matching plan / limitations / map / Stage D guide closures. The §11 step 6.3 (guide #3 `internal_synthesis.md`) drafting is unblocked by the LOCK.
