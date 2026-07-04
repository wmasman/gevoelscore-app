# Methodology review — external_contextualisation.md (r1, 2026-06-24)

**Reviewer mode**: fresh-session peer review. Reviewer is independent of the drafting session. Fresh session — no exposure to the drafting context; doc-only knowledge.
**Target**: [`docs/research/methodology/external_contextualisation.md`](../methodology/external_contextualisation.md) (r1, 2026-06-24)
**Review date**: 2026-06-24
**Standards applied**: [CONVENTIONS](../CONVENTIONS.md) §1, §2.1, §2.2, §3, §4; [plan](../methodology/_plan_results_analysis_layer.md) r5 §6.4 spec + §3.5 + §3.6 + §3.9 + §3.10 + §3.11 + §3.12 + §9; [limitations doc](../methodology/research_line_limitations.md) r3 §3 + §5; [synthesis-structure map](../methodology/synthesis_structure_map.md) r3 §3 + §4 + §5; [Stage S₁ guide](../methodology/internal_synthesis.md) r2 LOCKED; [Stage I guide](../methodology/verdict_to_inference.md) r2 LOCKED; [Stage D guide](../methodology/descriptive_precondition_audit.md) r2 LOCKED; [literature-gap log](../methodology/_pending_literature_fetch.md); Daza 2018 / Shamseer-CENT 2015 / Tate-SCRIBE 2016 / Natesan 2023 / WWC 2022 SCED; the four T-within-day-recovery primary anchors (Marques 2023, Mooren 2023, Ryabkova 2024, van Campen 2022); the Wiggers pacing handbook.

---

## 1. Overall verdict

**REVISION RECOMMENDED (mild).** The draft is structurally faithful to plan §6.4, implements all ten declared content sections plus the §3.5-mandated `open_inputs` sub-block at §4.9, and the five named inventions beyond the spec are — with two operational concerns — methodologically sound and operationally implementable. The §6.1 four halt-criteria for the §3.6 conflict-resolution rule are concrete and well-grounded at the topic level (parallel to guide #3 §6.1 at the cluster level); the §6.5 two-paths-after-logging structure correctly operationalises the §6.4 spec's "defer OR proceed under CANNOT-SAY" alternation; the §7 twelve-anti-pattern list is distinct from upstream plan §9, guides #1/#2/#3 anti-patterns; the §9 phased agent-instruction outline is concrete enough that the §11 step 7 skill build will know what to encode. The §4.7 L-ID citation discipline correctly translates limitations doc r3 §5 row for `topic-*.md` into binding form (L1+L2+L4 unconditionally; L3/L5/L6/L7 as apply; NA-with-reason mandatory). All cited literature files exist at the named paths.

Six findings drive the REVISION RECOMMENDED verdict rather than ACCEPT. Two are required (R1, R2); four are recommended (A1–A4). None blocks the §11 step 7 skill build or the §11 step 8 dry-run on T-stress-fatigue-pacing; all six are one-revision-cycle fixes.

- **R1.** §6.5's "load-bearing-vs-non-load-bearing" criterion for choosing between the two literature-gap paths is the strongest invention but is operationally under-defined. The criterion is named without a single sentence of operational guidance on how a Stage S₂ drafter (or the user at the §8 interview) decides whether a given uncited subclaim is "load-bearing" for the topic's positioning. The §6.4 PARTIALLY COMPARABLE → CANNOT-SAY rule already uses "load-bearing" in a different sense (load-bearing **fault-line dimension** for comparability), and the absence of an explicit cross-reference creates ambiguity between the two uses. A one-paragraph operational definition (e.g. "load-bearing = the topic's positioning would substantively differ between AGREES and CANNOT-SAY at the topic-summary level if this subclaim's consensus map closed") and an explicit disambiguation from the §4.4-sense load-bearing would close the loop. (See §4 below.)
- **R2.** §5.5 multi-subclaim aggregation rule for the topic-level summary paragraph is sound on the four enumerated cases (all-AGREES; AGREES+EXTENDS; any-DIVERGES; all/majority-CANNOT-SAY) but does NOT cover the operationally common **mixed-CANNOT-SAY-with-other-labels** case (e.g. one subclaim AGREES, one subclaim CANNOT-SAY due to literature-gap). The aggregation rule should explicitly say whether the topic-level summary names the CANNOT-SAY alongside the AGREES (preserving the gap as visible to downstream Stage A) or whether the CANNOT-SAY washes out into a topic-level call dominated by the AGREES subclaim. Given the §6.4 spec's "CANNOT-SAY is a valid and preferred outcome" framing, the preserve-the-gap reading is the right one — but the §5.5 list does not say so explicitly. A fifth bullet for the mixed-CANNOT-SAY-with-other-labels case is needed.

Recommended:

- **A1.** Density discipline. 1551 lines lands 3.4% over the upper bound (1500 target). The agent's self-report names the §6.5 two-paths and the §4.3 four-label consensus-existence status as the inventions that added length; the reviewer assesses the §4.5 + §5 overlap as the more compressible surface (per A4 in the guide #3 review, recommendation that did not land — see §6 below for ~50–80 line cutbacks).
- **A2.** §4.4 comparability call's three-label set draws explicitly on Daza 2018 / CENT 2015 / Natesan 2023 / WWC 2022 SCED inference-reach bounds, which is correctly framed. But the **operational mapping from each label to which paper's specific framing** is not consistent — Daza's "hypothesis-generating prior" framing is invoked at PARTIALLY COMPARABLE, but CENT item 22 (generalisability) is named only at §4.6 caveat 1, not at §4.4 directly. A one-sentence clarification in §4.4 of which standard each label cites (COMPARABLE → Daza convergence-data-point; PARTIALLY → Daza hypothesis-generating-only OR CENT 22 generalisability; NOT COMPARABLE → Daza no-bridge OR WWC does-not-meet-standards) would tighten the inference-reach correspondence.
- **A3.** §4.7 worked example for T-within-day-recovery is concrete and operationally clear, but a parallel worked example for T-stress-fatigue-pacing's L-ID block (the topic the §11 step 8 dry-run is most likely to target) does not appear in §4.7 itself — it only appears as a bullet sketch in §3 alongside the within-day-recovery sketch. A second §4.7 worked example for T-stress-fatigue-pacing (with the L3 Garmin-stress-vs-Wiggers-subjective-stress fault-line; L6 gevoelscore; L7 gating dropouts; L5 NA) would help the §11 step 8 drafter as much as the within-day example helps.
- **A4.** §11 lock log entry is dense but at 28+ lines of unbroken prose it is harder to scan than the per-revision diffs in the upstream guides. Two-or-three short paragraphs (one for inventions, one for §6.4 ambiguity interpretations, one for the §11 step 7 dependency note) would scan better without losing content.

## 2. Four-input bar findings (CONVENTIONS §2.2)

This MD is producer-mode infrastructure (per §3 of the target, per plan §4 row "Guide MDs (6×)") rather than a methodology MD locking a substantive analytical choice; the four-input bar applies in lighter form. Two of the four inputs apply directly; two apply indirectly.

| Input | Status | Reasoning |
|---|---|---|
| 1. Best-practices standards | PASS | The positioning-call mapping shape (four exhaustive labels at §4.5; three exhaustive comparability labels at §4.4; default-to-preserve discipline on ambiguity; no auto-resolution on DIVERGES; CANNOT-SAY as valid-and-preferred outcome) traces to N-of-1-to-group inference standards (Daza 2018 as primary anchor for the comparability-and-positioning question; CENT 2015 items 21+22 for limitations + generalisability binding §4.6 + §4.7; SCRIBE 2016 for L4 transparency at the topic level; Natesan 2023 as defensibility bar; WWC 2022 SCED for the evidence-quality framing §4.4 adapts). The §2 input list cites all five with one-sentence operational role; Daza is correctly named the primary anchor for the comparability-check question. |
| 2. Established literature | PASS | The §1 "alternatives considered" paragraph cites two rejected paths (addendum-embedded contextualisation; skip-S₂-go-direct-to-A) with explicit project-internal precedent (guides #1, #2, #3 used the same rejection reasoning for their respective upstream stages). The §2 input list, §4.7 worked example, and §4.8 + §4.9 cross-references draw on the five literature methodology anchors. This is consistent with guides #2 r1 and #3 r1 strength. |
| 3. Tradeoff vision | PASS | The "alternatives considered" paragraph satisfies CONVENTIONS §2.2 item 3 explicitly. Specific judgment-calls visible in the body: (a) four-label positioning set at §4.5 (vs free-form positioning prose — sound tradeoff per the §4.5 hard rule); (b) three-label comparability set at §4.4 (vs continuous comparability score — sound; the discrete-label discipline keeps positioning calls commensurate across topics); (c) CANNOT-SAY as preferred outcome over forced positioning per §4.5 + §5.4 (vs forcing AGREES/DIVERGES on weak evidence — sound; matches §6.4 spec verbatim); (d) two-paths-after-logging at §6.5 with load-bearing-vs-non-load-bearing as choice criterion (sound shape but operationally under-defined per R1). |
| 4. Research limitations + objectives | PASS | The §5 worked examples draw from the two active topics in the map's r3 (T-stress-fatigue-pacing, T-within-day-recovery); the §4.7 L-ID block correctly implements the limitations doc r3 §5 row for `topic-*.md` (L1+L2+L4 unconditional; L3/L5/L6/L7 as apply; NA-with-reason mandatory per the §3 hard rule); the §6.1 four halt-criteria handle the corpus's known map-revision-trigger cases at the topic level; the §6.5 literature-gap routing matches the `_pending_literature_fetch.md` "Candidate paper list" pattern verbatim. |

Overall: 4 PASS. The four-input compliance is strong. The trajectory of guide #1 r1 (2 PASS, 2 PARTIAL) → guide #2 r1 (4 PASS) → guide #3 r1 (4 PASS) → guide #4 r1 (4 PASS) shows the drafting-discipline propagation has fully landed.

## 3. Faithfulness to §6.4 spec

§6.4 has nine listed elements (purpose, inputs, output, 10-section outline, checklist, conflict rules, anti-patterns, interview seeds, agent-instruction outline). Mapping:

| §6.4 element | Implementation | Faithfulness |
|---|---|---|
| Purpose | §1 (purpose + where it sits + what it does not do + alternatives) | **Faithful with extension.** The "What Stage S₂ does NOT do" seven-bullet list (re-test cluster coherence / predictive claims / §3.12 commentary / refute consensus on N=1 / invent caveats / re-decide map / multi-topic-per-session) is operationally important boundary statement. The "alternatives considered" paragraph satisfies CONVENTIONS §2.2 item 3 explicitly. |
| Inputs | §2 (seven numbered inputs) | **Faithful with extension.** §6.4 names four inputs (cluster MD; literature/ contents; N-of-1 methodology; literature-gap log). §2 expands to seven: adds the synthesis-structure map's §4 topic row (binding for topic constellation per §6.1); the limitations doc (binding for L-ID citation per §4.7); CONVENTIONS sections (esp. §4.1-§4.3). All three additions sound and binding. |
| Output | §3 (path + flat naming + mode + L-ID discipline + worked-example anchors + hard rules) | **Faithful with extension.** §6.4 specifies `analyses/contextualisation/topic-XXX.md`. §3 specifies flat-no-per-topic-subfolder convention; correctly distinguishes from Stage D's per-HA folder. The "no thin-topic-skip" rule (every topic with locked constituents gets its own artefact; no analogue to guide #3 §5.6's single-member skip) is sound — the topic-vs-cluster epistemic distinction makes the skip unwarranted at this stage. The hard rule on NA-with-reason mandatory matches the limitations doc §5 binding. |
| Section outline | §4 (10 sub-sections, §4.1–§4.10) | **Faithful.** §6.4 names 10 sections; §4 implements all 10 with §4.5 carrying the topic-level positioning summary, §4.7 carrying the L-ID block, §4.9 carrying the four refusal-to-proceed paths + the `open_inputs` sub-block. The §6.4 spec's section 5 "Citations" was folded into §4.3-§4.5 (every external claim cites at the relevant section); the §6.4 spec's section 8 "open_inputs" was hoisted into §4.9 alongside follow-up suggestions. Both fold-ins correct per the §3.5 + §3.11 layer bindings. |
| Checklist | Folded into §4 sub-sections + §9.6 refuse-to-lock gate | **Faithful.** The §6.4 checklist's six bullets are implemented across §4 + §9.6: every-external-claim-cited (§4.3 + §9.6 gate 3); literature-gap-log routing (§6.5 + §9.6); comparability-explicit-CANNOT-SAY-preferred (§4.4 + §4.5 + §5.4 + §9.6 gate 5); N-of-1-to-group inference reach (§4.4 + §4.6 + §9.6 gate 7); DIVERGES-does-not-auto-claim (§4.5 + §4.8 + §7.2 + §9.6 gate 6). This is the right place to fold them. |
| Conflict rules | §6 (5 rules) | **Faithful with extension.** §6.4 names 3 conflict rules (we diverge; consensus does not exist; comparability fails). §6 implements all 3 (§6.2, §6.3, §6.4) and adds §6.1 (map-change-needed = the §3.6 layer-rule operationalisation, parallel to guide #3 §6.1) and §6.5 (literature-gap routing with the two-paths-after-logging structure). Both additions sound and necessary. |
| Anti-patterns | §7 (12 anti-patterns) | **Faithful with extension.** §6.4 names 4 anti-patterns (title-only alignment; N=1-as-refutation; cherry-picking; citing-paper-for-unmade-claim). §7 implements all 4 (§7.1, §7.2, §7.3, §7.4) and adds 8 more (§7.5 cross-topic smuggling; §7.6 post-hoc caveats; §7.7 §3.12 commentary at S₂; §7.8 predictive-quality measures; §7.9 invented labels; §7.10 uncited claims floating; §7.11 in-stage re-routing; §7.12 averaging-the-divergence). All eight additions distinct and sound — see §4 below. |
| Interview seeds | §8 (3 required + 1 optional) | **Faithful with extension.** §6.4 names 3 seeds (consensus existence; comparability; charitable-explanations for divergence). §8 implements all 3 (§8.1, §8.2, §8.3) and adds §8.4 (topic-trust upstream confirmation). Optional fourth parallels guide #1 §8.4, guide #2 §8.4, guide #3 §8.4 confirmation-seed pattern. Sound. |
| Agent-instruction outline | §9 (8 phases) | **Faithful with extension.** §6.4 names 4 bullets (Load / Walk / Produce / Refuse). §9 expands to 8 phases (Load / Gate / Extract / Interview / Produce / Refuse-to-lock-gate / Review-handoff / Acceptance + drift-trigger registration). The Refuse-to-lock gate enumerates ten structural checks (the agent self-reports eleven; the actual count is ten — the "any §4 section contains anti-pattern violations" is the catch-all tenth item). Extension correct because the relevant plan rules post-date §6.4's sketch. |

No §6.4 element is missing or substantively altered. Spec faithfulness is high — matches guide #2 r1 / guide #3 r1 strength on the §6.4 spec discipline. The two §6.4 spec ambiguities the agent's self-report flags (comparability-fails → CANNOT-SAY routing; literature-gap two-paths-after-logging) are resolved cleanly: the comparability auto-route is operationalised at §4.4 + §5.4 + §6.4 as a three-touchpoint structural rule; the two-paths-after-logging is operationalised at §6.5 with the load-bearing-vs-non-load-bearing choice criterion (sound shape; R1 above is on operational definition only).

## 4. The five inventions beyond §6.4

### Invention 1 — §4.3 four-label consensus-existence status

**Sound.** The §6.4 spec asks "does external consensus exist? What is it? If competing positions exist, what are they?" but does not define the label set. The draft's four-label set (CONSENSUS-EXISTS / COMPETING-POSITIONS / CONSENSUS-DOES-NOT-EXIST / LITERATURE-GAP) covers the operationally distinct cases the §6.4 spec implicitly distinguishes:

- CONSENSUS-EXISTS = a single consensus statement with primary citation.
- COMPETING-POSITIONS = multiple positions named with position-holders.
- CONSENSUS-DOES-NOT-EXIST = surveyed scope shows literature has spoken but no consensus formed.
- LITERATURE-GAP = relevant section unread OR paper not in `literature/`.

The fourth label (LITERATURE-GAP) is the critical operationalisation — it distinguishes "we surveyed the literature and found no consensus" (CONSENSUS-DOES-NOT-EXIST, which routes to §6.3 conflict rule) from "we have not surveyed yet" (LITERATURE-GAP, which routes to §6.5 literature-gap log). Without this distinction, the §6.5 routing would collapse into §6.3 and the literature-gap log would not get the entries it needs. Sound and necessary.

The §4.3 per-subclaim block structure (subclaim → status → position-holders) is operationally implementable.

### Invention 2 — §4.4 three-label comparability check with Daza inference-reach citation per call

**Sound (modulo A2 above).** The three-label set (COMPARABLE / PARTIALLY COMPARABLE / NOT COMPARABLE) is the right reduction of the §6.4 spec's "is the external population / measurement / era close enough" question. The default-to-NOT-COMPARABLE-on-ambiguity rule (parallel to guide #3 §4.4 default-to-CONFLICT-on-ambiguity) is the conservative discipline that prevents drift toward forcing positioning calls. The per-dimension matching requirement (population / measurement / era) keeps the call auditable.

The "Each comparability call MUST cite the N-of-1-to-group reach bound it leans on" rule is the right discipline — Daza 2018 is the primary anchor for the comparability question, and naming the reach-bound per call prevents the comparability label from becoming a hollow categorical. The mapping of COMPARABLE → convergence-or-divergence-data-point reach; PARTIALLY COMPARABLE → hypothesis-generating-only for unmatched dimensions; NOT COMPARABLE → no-inference-bridge is the right Daza-anchored reduction.

The A2 concern above is on operational clarity (which paper's framing each label cites), not on substance.

### Invention 3 — §5.5 multi-subclaim aggregation rule for topic-level summary paragraph

**Sound with one operational gap (R2 above).** The §6.4 spec addresses per-subclaim positioning but does not specify the topic-level summary aggregation. §5.5's four enumerated cases (all-AGREES; AGREES+EXTENDS; any-DIVERGES; all/majority-CANNOT-SAY) cover the most common aggregation patterns. The "any DIVERGES is carried forward as primary substantive finding; not averaged with AGREES into mostly-agrees" rule prevents the §7.12 anti-pattern at the summary level — the right discipline.

The R2 concern is the mixed-CANNOT-SAY-with-other-labels case (one AGREES + one CANNOT-SAY, or one EXTENDS + one CANNOT-SAY due to literature-gap). The aggregation rule does not say whether the topic-level summary names the CANNOT-SAY alongside the other labels (preserving the gap for downstream Stage A) or whether the CANNOT-SAY washes out. Given the §6.4 spec's "CANNOT-SAY is valid and preferred" framing, the preserve-the-gap reading is the right one — but the §5.5 list does not say so explicitly. A fifth bullet for the mixed-CANNOT-SAY-with-other-labels case ("the topic-level summary names the CANNOT-SAY explicitly alongside the other labels; the literature-gap remains visible to downstream Stage A") closes the gap.

### Invention 4 — §6.1 four halt-criteria for the map-change-needed conflict-resolution rule

**Sound.** The plan §3.6 conflict-resolution rule names the discipline at the layer level; the four concrete halt-criteria (constituent cluster's coherence call on different construct; topic positioning requires evidence from non-cluster member; external-literature scope cell inadequate; topic-vs-cluster boundary wrong) are operationally implementable and parallel guide #3 §6.1's four halt-criteria at the cluster level. The route-out instructions (stop drafting mid-session; produce only §4.9 `open_inputs` entry; hand off; resume only after separate map-revision session) match plan §3.6's "halt-and-route" discipline verbatim.

The four halt-criteria are exhaustive for the cases the §3.6 rule was designed for at the topic level: (1) covers the constituent-cluster-on-different-construct case; (2) covers the topic-membership-needs-revision case; (3) covers the literature-scope-cell-needs-revision case; (4) covers the topic-boundary-needs-revision case. The cluster-level "HA-belongs-in-different-cluster" case the §3.6 spec also names is correctly absent from the topic-level halt-criteria (it would be a Stage S₁ halt rather than Stage S₂, consistent with the topic-bounded-scope discipline). Sound omission.

### Invention 5 — §9.6 phased refuse-to-lock gate with ten structural checks

**Sound.** The agent self-reports eleven items but the actual count in §9.6 is ten (per a literal count of bullets in the section). The ten checks (L1/L2/L4 missing from §4.7; L3/L5/L6/L7 silently omitted; §4.3 uncited external claim; §4.4 invented label; §4.5 invented label; §4.8 DIVERGES without both-readings preservation; §4.6 missing three N-of-1 caveats; §4.9 external-research lacks N=1 scoping; §4.5 averaging-DIVERGES into AGREES; any §4 anti-pattern violation) are the right structural gates. Each maps to a §4 sub-section requirement, so the gate is implementable as a skill-level check rather than as judgment.

The last check ("any §4 section contains anti-pattern violations per §7") is text-pattern detection and harder to enforce at the skill level than the first nine; the same concern guide #2 r1 review and guide #3 r1 review flagged for their respective §9.6 catch-all items applies here. Not blocking; a §9.6-level refinement could specify pattern-detection heuristics (presence of "predicts", "forecasts", "X means Y", first-person narrative in §4.3-§4.7 triggers the gate).

### Inventions beyond the five named — the §6.5 load-bearing-vs-non-load-bearing criterion

**The agent's self-report flags this as the strongest invention** beyond §6.4. Per R1 above: the criterion is the right axis of discrimination but is operationally under-defined. The §6.4 spec offers the two options (defer until acquired OR proceed under CANNOT-SAY) without specifying which path applies when; the draft's load-bearing-vs-non-load-bearing choice criterion is the right discrimination axis (a topic with a load-bearing subclaim under literature-gap would lock with a CANNOT-SAY that substantively misrepresents the positioning surface; a non-load-bearing subclaim under literature-gap can lock with CANNOT-SAY without misrepresentation). But the criterion needs operational definition (per R1).

The disambiguation from the §4.4-sense load-bearing (load-bearing **fault-line dimension** for comparability) is also needed — the term "load-bearing" appears in both §4.4 (PARTIALLY COMPARABLE with load-bearing fault-line → CANNOT-SAY) and §6.5 (load-bearing subclaim → defer-until-acquired path), and the two uses are different. The draft does not flag the disambiguation explicitly.

The axis itself is methodologically correct; the operational definition + disambiguation is what needs the one-revision-cycle fix.

## 5. Per-section findings

### §1 Purpose

Sound. The block-quote framing ("A cluster's coherence call is a within-subject reading. Stage S₂ places that reading against external published literature for the topic's construct — producing a positioning call drawn from a fixed label set after an honest comparability check. CANNOT-SAY is a valid and often preferred outcome") matches plan §6.4's opening framing. The seven-bullet "What Stage S₂ does NOT do" is helpful scope-clarification — particularly the §3.10 + §3.12 boundaries and the no-re-decide-map rule which §6.1 + §7.11 enforce structurally. The "Alternatives considered" paragraph satisfies CONVENTIONS §2.2 item 3 explicitly. The skill-precondition note matches guides #1-#3 framing and is operationally important.

### §2 Inputs

Sound. The seven numbered inputs cover the §6.4 spec's four plus the layer-level binding additions (synthesis-structure map; limitations doc; CONVENTIONS). The closing "what the contextualisation does NOT load" paragraph is the right negative-space discipline. The §2 input #3 framing of the external-literature PDFs as primary-anchor-with-relevant-section-read is operationally correct (matches §7.1 anti-pattern + §9.6 gate 3).

The §2 input #4 framing of the N-of-1 methodology anchors with Daza as primary for Stage S₂ is correct (Daza's N-of-1-to-group inference-reach framing is the closest match for the comparability-and-positioning question). The roles of CENT (items 21+22 for §4.6 + §4.7), SCRIBE (L4 for §4.7), Natesan (defensibility bar), and WWC SCED (evidence-quality framing §4.4 adapts) are each named in one sentence with the operational role. Pass.

### §3 Output

Sound. The flat-no-per-topic-subfolder convention matches the locked plan §5 output tree. The "no thin-topic-skip" rule is the right discipline at this stage. The L-ID citation discipline at the output level correctly translates limitations doc r3 §5 row for `topic-*.md` into binding form (L1+L2+L4 unconditional; L3/L5/L6/L7 as apply; NA-with-reason mandatory). The two hard rules at §3 (no missing L1/L2/L4; no NA without one-sentence reason) are correctly framed and enforced at §9.6 gates 1-2.

The §3 worked-example anchors (T-stress-fatigue-pacing L-ID sketch; T-within-day-recovery L-ID sketch) align with the synthesis-structure map r3 §4 topic row L-IDs columns exactly. The T-stress-fatigue-pacing sketch cites L1+L2+L4 unconditional + L3 (Garmin), L6 (gevoelscore), L7 (gating dropouts), with L5 NA (no v24); matches map r3 row. The T-within-day-recovery sketch cites L1+L2+L4 unconditional + L3 (bout-derived Garmin), L7 (gating + cross-phase coverage), with L5 NA + L6 NA (gevoelscore not in primary cell); matches map r3 row. Both sketches concrete and accurate. **A3 above**: the full-paragraph worked example at §4.7 covers only T-within-day-recovery; a parallel T-stress-fatigue-pacing worked example would help the §11 step 8 drafter.

### §4 Section outline for the produced topic-XXX.md

Sound. The ten sub-sections cover §6.4's ten-section outline. Per-section notes:

**§4.1 (topic name + constituent clusters)**: sound; mechanical header copy from map row + each constituent's `cluster-*.md` §4.1; the qualifier-preservation rule for cluster coherence calls (e.g. "trivial-ORTHOGONAL", "PARTIALLY CONCORDANT (spec-mechanism disagreement, shape agreement)") inherits from guide #3 §5.5 verbatim-qualifier rule.

**§4.2 (pre-declared topic membership)**: sound; the template paragraph correctly cites the map row's declared-date and lock-version verbatim; the hard rule that it "does NOT re-derive membership" prevents in-stage re-mapping. Parallel to guide #3 §4.2 at the topic level.

**§4.3 (consensus map)**: sound (per Invention 1 above). The per-subclaim block structure (subclaim → status → position-holders) is operationally implementable. The hard rule on every-external-claim-cites-OR-logs-gap is enforced at §9.6 gate 3. The worked-example anchor for T-within-day-recovery is concrete.

**§4.4 (comparability check)**: sound (per Invention 2 above; modulo A2). The three-label set is the right exhaustive reduction. The per-call N-of-1-to-group reach citation discipline is the right operationalisation of the Daza/CENT/Natesan/WWC anchor block.

**§4.5 (positioning)**: sound; the four-label set is correctly framed; the CANNOT-SAY-as-preferred discipline is enforced (per §6.4 spec). The topic-level positioning summary paragraph at the close of §4.5 is the right aggregation surface — but R2 above on the mixed-CANNOT-SAY case.

**§4.6 (caveats specific to N-of-1 → group comparison)**: sound; the three structural caveats (one-data-point-not-settlement; comparability-bound-is-reach-bound; external-consensus-not-external-truth) cover the §6.4 spec's "N-of-1 inference reach" + "DIVERGES does not auto-claim 'truth'" bindings cleanly. The "MUST appear in every §4.6 section, even when positioning is AGREES" rule is the right structural enforcement (AGREES does not erase the N=1 reach bound).

The §4.6 separation from §4.7 (structural N-of-1-to-group caveats vs L-ID citation block) is operationally clear and matches the limitations doc §5 binding for `topic-*.md`.

**§4.7 (per-topic limitations — L-ID citation block)**: sound; the binding L1+L2+L4 unconditional + L3/L5/L6/L7 as-apply rule correctly implements limitations doc r3 §5 row. The "one paragraph per L-ID" format is operationally clear. The NA-with-one-sentence-reason rule is enforced at §9.6 gate 2.

The T-within-day-recovery worked example is concrete and accurate against the limitations doc r3 §3 + the map r3 §4 row. **Daza/CENT/SCRIBE citations spot-checked**: L1 citation correctly invokes Daza 2018's "convergence as one data point, not settlement" framing (Daza's N-of-1-to-group reach binding); L4 mitigation reach correctly cites the fresh-session `/research-review` + the limitations-doc r3 §3 L4 meta-recursion caveat; L2 cross-phase-pooling caveat correctly cites HA-C4c's primary-cell pooling against the four anchor populations' likely single-medication-phase cohorts. **A3 above**: a parallel T-stress-fatigue-pacing worked example would help.

**§4.8 (open conflicts preserved with both readings)**: sound; the no-auto-resolution rule and the paragraph-per-DIVERGES-subclaim structure are correctly framed. The resolution paths (literature-gap fill; sister-HA moving comparability; group-level external-research) are correctly framed as "NOT executed at Stage S₂." The all-AGREES + mixed-AGREES-with-EXTENDS trivial fillings are operationally complete.

**§4.9 (follow-up suggestions + open_inputs)**: sound; the two-track structure (own-research + external-research) matches the §3.11 binding. The external-research-N=1-scoping discipline is correctly framed. The four refusal-to-proceed paths (cluster missing/unlocked; topic not in map; literature-gap on load-bearing subclaim; comparability cannot be assessed without missing literature) are operationally complete. The "distinct from open_inputs" cross-reference matches the §3.5 vs §3.11 separation.

**§4.10 (cross-references)**: sound; the destinations cover the full forward + upstream chain.

### §5 Positioning-call mapping rules

Sound on structure (per-label rules + worked examples + multi-subclaim aggregation). One worked example per mapping rule, drawn from the two active topics, matches the §6.4 spec's worked-example anchor discipline.

- §5.1 AGREES worked example for T-within-day-recovery: the **N=1 reach caveat per §6 caveat 1** is correctly carried; the PARTIALLY COMPARABLE-on-measurement-and-era handling is operationally clear (Daza's "PARTIALLY COMPARABLE still allows AGREES on direction" framing is the right reach-bound).
- §5.2 EXTENDS worked example for T-within-day-recovery (bout-resolution finding): the "consensus measures at daily/cohort-average resolution; subject's pattern measures at within-day bout resolution" framing is operationally clear; the hypothesis-generating-only routing per Daza 2018 is correct.
- §5.3 DIVERGES worked example for T-stress-fatigue-pacing (inverted-U vs Wiggers monotone-convex): **accurate against the upstream cluster reading**. Per the locked guide #3 r2 §5.2 (which the r1 review corrected from "monotone-inverse" to "inverted-U/concave agreement across both HAs"), C-stress-fatigue-shape's joint reading is concave/inverted-U peaking around stress 30-40, NOT Wiggers-monotone-convex. The §5.3 worked example correctly carries this as DIVERGES against the Wiggers handbook (lines 1357-1368 convex-cost claim) with the PARTIALLY COMPARABLE-on-measurement-not-load-bearing-for-direction routing landing DIVERGES rather than CANNOT-SAY. The five-dimension candidate-explanation enumeration (population/measurement/era/individual variation/methodological difference) is operationally complete.
- §5.4 CANNOT-SAY worked example for T-stress-fatigue-pacing (peak-location subclaim under literature-gap): accurate; the §6.5 literature-gap routing is correctly invoked.
- §5.5 multi-subclaim aggregation: per R2 above, the mixed-CANNOT-SAY case is missing.

### §6 Conflict rules

Sound. §6.1 (map-change-needed = the §3.6 layer-rule operationalisation at the topic level) is the most important rule of the section and is concrete enough for a Stage S₂ drafter to apply it (per Invention 4 above). §6.2-§6.4 are direct cite-and-implement of the §6.4 spec's three conflict rules. §6.5 (literature-gap routing with the two-paths-after-logging) is the most novel rule and is operationally underdefined per R1 above.

### §7 Anti-patterns

Sound. The 12 anti-patterns + the §6.4 spec's 4 are correctly mapped. The 8 additions (§7.5 cross-topic smuggling; §7.6 post-hoc caveats; §7.7 §3.12 commentary; §7.8 predictive-quality measures; §7.9 invented labels; §7.10 uncited claims; §7.11 in-stage re-routing; §7.12 averaging-the-divergence) are distinct and sound. Several are the topic-level analogues of cluster-level anti-patterns (§7.5 from guide #3 §7.4; §7.6 from guide #3 §7.7; §7.7 from guide #3 §7.8; §7.11 from guide #3 §7.1; §7.12 from guide #3 §7.2) — the parallel discipline is correctly carried up to the topic level.

The §7.2 "treating N=1 as refutation" anti-pattern correctly invokes the symmetric L1 + Daza 2018 binding (N=1 cannot confirm AND cannot refute group-level consensus on its own).

### §8 Interview-prompt seeds

Sound. The 3 required seeds (consensus existence; comparability; charitable-explanations for DIVERGES) match §6.4 spec verbatim. The §8.4 optional fourth (topic-trust upstream confirmation) parallels guides #1-#3 §8.4 confirmation-seed pattern.

### §9 Agent-instruction outline

Sound (per Invention 5 above). The eight phases are concrete. The §9.6 refuse-to-lock gate's ten structural checks (agent self-reports eleven; literal count is ten) are the right protection layer. The §9.7 review handoff correctly routes to `/research-review` (not `/research-methodology-review` — `topic-*.md` is reviewer-mode-with-authorization per plan §4, not a binding methodology MD). The §9.8 acceptance + drift-trigger registration enumerates four re-examination triggers; the cluster-revision-driven trigger is the most operationally common and is correctly named first.

### §10 Cross-references

Spot-checked links (per request 10):

- `_plan_results_analysis_layer.md` § references (6.4, 3, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 4) — all exist in the plan (verified).
- `internal_synthesis.md` (guide #3 LOCKED r2 2026-06-24) — referenced for upstream cluster coherence-call chain; verified to exist.
- `verdict_to_inference.md` (guide #2 LOCKED r2 2026-06-24) — referenced for upstream licensed-claim chain; verified to exist.
- `descriptive_precondition_audit.md` (guide #1 LOCKED r2 2026-06-24) — referenced for upstream verdict-trust chain; verified to exist.
- `research_line_limitations.md` (LOCKED r3) § references (3, 5, 8) — all exist (verified). The §5 row for `topic-*.md` (L1+L2+L4 unconditional; L3/L5/L6/L7 as apply) is correctly cited verbatim.
- `synthesis_structure_map.md` (LOCKED r3) § references (2, 3, 4, 5, 7) — all exist (verified; the §4 topic row L-IDs columns for T-stress-fatigue-pacing and T-within-day-recovery match the §3 worked examples).
- `_pending_literature_fetch.md` — verified to exist; the "Candidate paper list" pattern §6.5 invokes for literature-gap log entries matches the file's structure.
- `_descriptive_stocktake_2026-06-23.md` § references (4, 9) — verified to exist.
- CONVENTIONS § references (1, 1.2, 2.1, 4.1, 4.2, 4.3) — all exist.
- **Literature files verified at named paths**:
  - `literature/wiggers_pacing_handleiding.pdf` — exists.
  - `literature/marques_2023_lc_cardiovascular_autonomic_dysfunction.pdf` — exists.
  - `literature/mooren_2023_postcovid_hrv_autonomic_dysregulation.pdf` — exists.
  - `literature/ryabkova_2024_mecfs_lc_dysautonomia_patterns.pdf` — exists.
  - `literature/vancampen_2022_mecfs_rhr_elevated.pdf` — exists.
  - `literature/appelman_2024_muscle_pem_long_covid.pdf` — exists.
  - `literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf` — exists.
  - `literature/methodology/shamseer_2015_cent_consort_nof1.pdf` — exists.
  - `literature/methodology/tate_2016_scribe_single_case_reporting.pdf` — exists.
  - `literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf` — exists.
  - `literature/methodology/wwc_2022_standards_handbook_v5_0.pdf` — exists.

The cross-reference layer is in good shape; no broken links found in the spot-check.

### §11 Lock log

Per A4 above: 28+ lines of unbroken prose. Content is correct (six named inventions; two §6.4 ambiguity interpretations; named-invention-beyond-spec flag on §6.5). The narrative explanation of what each invention does is helpful for a future reviewer, but the scannability is lower than the per-revision-diff format used in upstream guides' lock logs. Recommend breaking into two-or-three short paragraphs for the next revision. **Minor count discrepancy**: the agent reports §9.6 as having "ten-item refuse-to-lock gate" in one place and "eleven structural checks" in another. The literal count in the §9.6 section is ten (the eleventh item the agent perhaps counted is "Any §4 section contains anti-pattern violations per §7", which is structurally the catch-all; whether to count it as a structural check or as a separate text-pattern check is a definitional call). Not blocking but worth tightening.

## 6. Cross-cutting concerns

### §3.6 conflict-resolution rule operationalisation (§6.1 of the draft)

Strongly enforced. The §6.1 four halt-criteria are concrete and operationally implementable (per Invention 4 above). The route-out instructions are concrete (stop drafting mid-session; produce only §4.9 `open_inputs` entry; hand off; resume only after separate map-revision session). The "why this rule" rationale is the cite-by-reference to guide #3 §6.1's rationale, which is the right way to avoid duplication. §7.11 anti-pattern enforces the rule against in-session map editing. The §8.4 optional confirmation seed surfaces map-vs-stage misalignment at the right point.

### §3.10 hard predictive gate boundary

Strongly enforced. §1 "what Stage S₂ does NOT do" list (second bullet), §4.5 (positioning is direction not diagnostic-quality measures), §4.6 caveat 1 (positioning is one data point not settlement), §7.8 anti-pattern (no PPV, base rate, sensitivity, specificity, false-alarm rate, lead time, reliability), §9.6 refuse-to-lock gate (anti-pattern violations check) all close the boundary. The forward pointer to Stage A via the synthesis-structure map's §5 K-construct row is correctly named but no Stage S₂ content crosses it.

### §3.11 follow-up suggestions implementation

Strongly enforced. §4.9 implements both tracks per the §3.11 binding. The external-research-N=1-scoping requirement is correctly named ("every external-research suggestion MUST explicitly name the N=1 limit"); the §9 layer-level unscoped-follow-up fallacy is cited as the prohibition. The §9.6 refuse-to-lock gate check 8 enforces this at the skill level.

The two worked-example sketches (T-stress-fatigue-pacing third sister-HA on rolling-window-baseline binning; T-within-day-recovery unmedicated-only sister-HA on `bout_n_did_not_return_day`) are concrete pre-reg shapes rather than vague directions. The "reading Wiggers' convex-cost derivation in full" follow-up for T-stress-fatigue-pacing is the right literature-gap-fill suggestion.

### §3.12 commentary boundary

Strongly enforced. §1 "what Stage S₂ does NOT do" list (third bullet), §7.7 anti-pattern (subject-narrative-at-Stage-S₂ forbidden), §9.6 refuse-to-lock gate (anti-pattern violations check) all close the boundary. The distinction from §4.6 N-of-1-to-group caveats is operationally clear (caveats are structural reach-bounds; commentary is subject-narrative).

### §3.11 N=1 scoping for external-research suggestions

Strongly enforced. The §4.9 "every external-research suggestion MUST explicitly name the N=1 limit" rule is the right discipline; the per-suggestion L-ID-citing requirement (typically L1 for group-level confirmation studies; L4 for blinding-required designs; L3 for cross-instrumentation work) is operationally implementable.

### L-ID citation discipline at topic level (§4.7 + §9.6 gate 1-2)

Strongly enforced (no issues found). §4.7 implements the limitations doc r3 §5 binding for `topic-*.md` faithfully ("MUST cite L1, L2, L4 unconditionally; cite L3, L5, L6, L7 as they apply"). The §9.6 refuse-to-lock gate 1 enforces the L1+L2+L4 unconditional rule; gate 2 enforces the NA-with-reason rule for applicable L3/L5/L6/L7. The unconditional-vs-as-apply distinction matches the limitations doc r3 §5 table row verbatim. The L-ID mapping examples for T-stress-fatigue-pacing (L1+L2+L4 unconditional + L3 Garmin, L6 gevoelscore, L7 gating; L5 NA) and T-within-day-recovery (L1+L2+L4 unconditional + L3 bout-derived Garmin, L7 gating + cross-phase coverage; L5 NA, L6 NA) align with the map r3 §4 row L-IDs columns exactly. The worked example at §4.7 (T-within-day-recovery only) is operationally clear; **A3 above** recommends a parallel T-stress-fatigue-pacing worked example.

### CANNOT-SAY as preferred outcome over forced positioning (§4.5 + §5.4 + §6.4)

Strongly enforced. §4.5 explicitly carries "CANNOT-SAY is a valid and often preferred outcome over forced positioning per the locked-plan §6.4 spec." §5.4 carries the four CANNOT-SAY routing conditions (literature-gap; NOT COMPARABLE auto-route; PARTIALLY COMPARABLE with load-bearing fault-line; no clean mapping among competing positions). §6.4 cite-and-implements the §6.4 spec's "comparability fails → CANNOT-SAY; do not force" rule. The §4.5 hard rule "defaults to CANNOT-SAY" on label ambiguity matches the default-to-preserve discipline of guide #3 §4.4 (default-to-CONFLICT-on-ambiguity). The discipline is operationally complete.

### Literature-gap-log routing (§6.5 + `_pending_literature_fetch.md`)

Mostly enforced. §6.5 correctly invokes the `_pending_literature_fetch.md` "Candidate paper list" pattern (citation, candidate-claim, where to look, MD section using it) verbatim. The two-paths-after-logging structure (defer vs proceed under CANNOT-SAY) operationalises the §6.4 spec's alternation; **R1 above** is on the load-bearing-vs-non-load-bearing operational definition only. The §4.9 refusal-to-proceed path 3 ("Literature gap blocks positioning on a load-bearing subclaim") and path 4 ("Comparability cannot be assessed without missing literature") are operationally complete.

### Length and density

1551 lines is 3.4% over the upper bound (1500 target). The trajectory across the four guides (1008 → 1493 → 1939 → 1551) shows the discipline-signal landed (the agent compressed by ~20% from guide #3, despite guide #4 covering arguably more complex content: external-literature contextualisation has more discipline surfaces than internal synthesis). The 50-line overrun is operationally explainable as the §6.5 two-paths-after-logging structure (which guide #3 did not have to operationalise) plus the §5 four-mapping-rule worked examples (one per label) plus the §4.4 three-label set with per-label Daza/CENT/Natesan/WWC reach-bound citation.

Realistic compression opportunities (in priority order):

- **§4.5 + §5 overlap (~50 lines)**: §4.5 carries the four positioning labels with one-paragraph definitions; §5.1-§5.4 carries the same four labels with mapping-rule paragraphs. The same pattern guide #2 r1 review and guide #3 r1 review flagged (A4 in both). The §4.5-points-at-§5 form (analogous to guide #2 r1 A4 recommendation that did not land in guide #2 r2) would save ~50 lines without losing content.
- **§3 worked-example sketches + §4.7 worked example overlap (~20-30 lines)**: §3 carries L-ID sketches for both T-stress-fatigue-pacing and T-within-day-recovery; §4.7 carries the full T-within-day-recovery worked example. Either the §3 sketches could compress to a single sentence pointing forward to §4.7 (with the T-stress-fatigue-pacing sketch hoisted into §4.7 per A3), or the §4.7 worked example could compress into one block per topic. Either path saves ~20-30 lines.
- **Hard rule boxes (~30 lines)**: several "Hard rule" blocks repeat (e.g. §3 + §4.5 + §7.9 all enforce the four-label exhaustiveness for positioning; §3 + §4.7 both carry the L1+L2+L4 unconditional rule). Cross-referencing rather than repeating would save ~30 lines.

Realistic total compression: ~100-110 lines (~7%). Not blocking; A1 above recommends the compression for a future revision pass but does not require it.

### What would block a Stage S₂ dry-run on T-stress-fatigue-pacing at §11 step 8

Concretely: if a Stage S₂ drafter loaded this guide and tried to contextualise the T-stress-fatigue-pacing topic tomorrow, the operational gaps they would hit are:

1. **The §6.5 load-bearing-vs-non-load-bearing criterion (R1 above) is under-defined.** The drafter walking the §8.1 consensus-existence interview seed for the inverted-U-peak-location subclaim would encounter the LITERATURE-GAP status (Wiggers does not address peak-location of non-monotone alternatives; broader PEM-pacing literature not yet read for explicit peak-location claims). At §6.5 they would face the two-paths choice and not know how to apply the load-bearing-vs-non-load-bearing criterion to this specific subclaim. A drafter would either guess or ask the user. The fix is one-revision-cycle operational definition.
2. **The §5.5 mixed-CANNOT-SAY-with-other-labels case (R2 above) is missing.** If the drafter lands AGREES on the broader Wiggers-direction-divergence subclaim and CANNOT-SAY on the peak-location subclaim, they would need the §5.5 aggregation rule to know whether the topic-level summary names both or whether the CANNOT-SAY washes out. The §5.5 list does not cover this case explicitly. The fix is one-revision-cycle addition.
3. **§4.7 worked example covers T-within-day-recovery only (A3 above).** The T-stress-fatigue-pacing L-ID block has the §3 sketch but no full paragraph worked example. The drafter would have to translate the sketch into the full §4.7 paragraph format on their own. Not blocking but adds friction.

R1 + R2 are operationally most important; A1-A4 are clarity/density refinements. None blocks the §11 step 7 skill build (the skill can encode the refuse-to-lock gates without the R1 operational definition), but R1 + R2 should be closed before the §11 step 8 dry-run.

## 7. Required actions to absorb before LOCK

- **R1.** §6.5 two-paths-after-logging criterion: add one paragraph of operational guidance for the load-bearing-vs-non-load-bearing criterion. Specifically: (a) one-sentence operational definition of "load-bearing" at the §6.5 level (e.g. "load-bearing = the topic's positioning at the topic-summary level would substantively differ between AGREES/EXTENDS/DIVERGES and CANNOT-SAY if this subclaim's consensus map closed"); (b) one-sentence disambiguation from the §4.4-sense load-bearing (load-bearing **fault-line dimension** for comparability vs load-bearing **subclaim** for topic-positioning); (c) one worked example from the two active topics naming how each decision would land (e.g. T-stress-fatigue-pacing peak-location subclaim → non-load-bearing → proceed under CANNOT-SAY; a hypothetical Wiggers-direction-divergence subclaim with no consensus citation yet → load-bearing → defer-until-acquired).

- **R2.** §5.5 multi-subclaim aggregation rule: add a fifth bullet for the mixed-CANNOT-SAY-with-other-labels case. Suggested wording: "**Mixed CANNOT-SAY with other labels**: the summary names the CANNOT-SAY explicitly alongside the other labels (AGREES, EXTENDS, DIVERGES); the literature-gap or comparability gap that drove the CANNOT-SAY is recorded as visible to downstream Stage A; CANNOT-SAY does NOT wash out into the topic-level call dominated by AGREES/EXTENDS/DIVERGES subclaims." This preserves the §6.4 spec's "CANNOT-SAY is valid and preferred" framing at the aggregation level.

## 8. Recommended actions to absorb before LOCK (optional)

- **A1.** Length compression for a future revision pass (not blocking). Three candidates in priority order: §4.5 + §5 overlap could compress to §4.5-points-at-§5 form (per guide #2 r1 A4 recommendation; ~50 lines); §3 worked-example sketches + §4.7 worked example overlap could compress by either pointing-forward or hoisting the T-stress-fatigue-pacing sketch into §4.7 (~20-30 lines); Hard rule boxes could cross-reference rather than repeat (~30 lines). Realistic total: ~100-110 lines (~7%) without losing operational content.

- **A2.** §4.4 comparability call operational mapping to inference-reach standards: add one sentence per label clarifying which standard's specific framing each label cites. Suggested mapping: COMPARABLE → Daza 2018 convergence-or-divergence-data-point reach; PARTIALLY COMPARABLE → Daza 2018 hypothesis-generating-only-for-unmatched-dimensions reach (alternative: CENT 2015 item 22 generalisability for the unmatched-dimensions caveat); NOT COMPARABLE → Daza 2018 no-inference-bridge reach (alternative: WWC 2022 SCED does-not-meet-standards framing for the cross-population comparison).

- **A3.** §4.7 worked example: add a parallel T-stress-fatigue-pacing L-ID worked example to the existing T-within-day-recovery worked example. The §3 sketch can be hoisted into the §4.7 full-paragraph format. Specifically: L1 paragraph on the Wiggers convex-cost-vs-inverted-U single-subject reading; L2 paragraph on the Stratum 4 unmedicated scope; L4 paragraph on the Wiggers-prior-anchor structure (HA-C3 v2 + HA-C3p both pre-registered with the Wiggers prior); L3 paragraph on the Garmin-stress-vs-Wiggers-subjective-stress instrumentation mismatch; L6 paragraph on the gevoelscore outcome; L7 paragraph on the gating dropouts in the unmedicated cell; L5 NA reason (no v24 primary signals per the map r3 §3 row for C-stress-fatigue-shape).

- **A4.** §11 lock log: split the 28+ line single paragraph into two-or-three short paragraphs (one for inventions; one for §6.4 ambiguity interpretations; one for the §11 step 7 skill dependency note). Also tighten the §9.6 count discrepancy (the agent reports ten-item gate in one place and eleven structural checks in another; the literal count is ten — the "any §4 anti-pattern violation" is the catch-all tenth).

## 9. Confirmed-good

The following elements of the draft are sound and need no revision:

- §1 purpose framing + alternatives-considered paragraph + skill-precondition note + seven-bullet "What Stage S₂ does NOT do" list.
- §2 seven-input list (the §6.4 spec's four + the synthesis-structure map binding + the limitations doc + CONVENTIONS).
- §3 output spec + flat-no-per-topic-subfolder convention + no-thin-topic-skip rule + L-ID citation discipline at output level + hard rules + worked-example anchors.
- §4.1 mechanical header (topic ID + name + constituent cluster list with coherence calls + qualifiers per guide #3 §5.5 + shared construct + external-literature scope).
- §4.2 pre-declared topic membership template + hard rule against re-derivation.
- §4.3 four-label consensus-existence status + per-subclaim block structure + hard rule on cited-OR-logged + worked-example anchor.
- §4.4 three-label comparability check + per-call N-of-1-to-group reach citation discipline + default-to-NOT-COMPARABLE-on-ambiguity hard rule (modulo A2 operational mapping).
- §4.5 four-label positioning + CANNOT-SAY-as-preferred discipline + topic-level positioning summary paragraph (modulo R2 on mixed-CANNOT-SAY).
- §4.6 three structural N-of-1-to-group caveats + "must appear even when AGREES" rule + separation from §4.7.
- §4.7 L-ID citation block + L1+L2+L4 unconditional + L3/L5/L6/L7 as-apply + NA-with-reason rule + T-within-day-recovery worked example (A3 above on the parallel T-stress-fatigue-pacing worked example).
- §4.8 no-auto-resolution rule + paragraph-per-DIVERGES + resolution-paths-not-executed-at-S₂ framing + trivial fillings for all-AGREES and AGREES+EXTENDS.
- §4.9 four refusal-to-proceed paths + four-field shape + open-inputs-do-not-block-completion framing + distinct-from-follow-up-suggestions cross-reference.
- §4.10 cross-references (all spot-checks pass; full forward + upstream chain).
- §5.1-§5.4 four mapping rules with one worked example each (drawn from the two active topics).
- §5.3 DIVERGES worked example for T-stress-fatigue-pacing: accurate against the upstream cluster reading per guide #3 r2 §5.2 corrected framing (concave/inverted-U agreement, NOT monotone-inverse).
- §6.1 four halt-criteria + route-out instructions + cite-by-reference to guide #3 §6.1 rationale.
- §6.2-§6.4 cite-and-implement of the §6.4 spec's three conflict rules.
- §6.5 literature-gap routing with the two-paths-after-logging structure (modulo R1 operational definition).
- §7.1-§7.12 twelve anti-patterns including the eight extensions beyond §6.4 spec.
- §8.1-§8.4 three required seeds + one optional topic-trust-confirmation seed.
- §9.1-§9.8 eight-phase agent-instruction outline including the §9.6 refuse-to-lock gate.
- §10 cross-references (all spot-checks pass; all literature files verified at named paths).
- §11 lock log (per A4 on scannability + count discrepancy).

The two active topics in the map r3 (T-stress-fatigue-pacing, T-within-day-recovery) are mostly well-served by this guide: a Stage S₂ drafter loading the guide tomorrow would have an operationally clear procedure for each, modulo the four findings above (R1 + R2 + A1-A4).

---

**Reviewer recommendation**: absorb R1 + R2 (one-revision-cycle fixes); A1-A4 are recommended for clarity/density. After R1 + R2 absorption, the guide can LOCK without a second fresh-session review per the established Option-γ pattern matching plan / limitations / map / Stage D guide / Stage I guide / Stage S₁ guide closures. The §11 step 6.5 (guide #5 `actionability_translation.md`) drafting is unblocked by the LOCK on guide #4.
