# Methodology review — actionability_translation.md (r1, 2026-06-24)

**Reviewer mode**: fresh-session peer review. Reviewer is independent of the drafting session. Fresh session — no exposure to the drafting context; doc-only knowledge.
**Target**: [`docs/research/methodology/actionability_translation.md`](../methodology/actionability_translation.md) (r1, 2026-06-24)
**Review date**: 2026-06-24
**Standards applied**: [CONVENTIONS](../CONVENTIONS.md) §1, §1.2, §2.1, §2.2, §3, §4; [plan](../methodology/_plan_results_analysis_layer.md) r5 §6.5 spec + §3.5 + §3.6 + §3.7 + §3.8 + §3.9 + §3.10 (hard predictive gate — binding) + §3.11 + §3.12 (commentary layer — binding) + §9; [limitations doc](../methodology/research_line_limitations.md) r3 §3 + §5 (most rigorous L-ID discipline of any artefact type); [synthesis-structure map](../methodology/synthesis_structure_map.md) r3 §5 K-rows; [Stage S₂ guide](../methodology/external_contextualisation.md) r2 LOCKED (immediate upstream gate); [Stage S₁ guide](../methodology/internal_synthesis.md) r2 LOCKED; [Stage I guide](../methodology/verdict_to_inference.md) r2 LOCKED; [Stage D guide](../methodology/descriptive_precondition_audit.md) r2 LOCKED; [RESEARCH-REPORT](../RESEARCH-REPORT.md) §5.2 PPV-with-base-rate precedent; [hypothesis_lock_process.md](../methodology/hypothesis_lock_process.md); [personal_hypotheses.md](../personal_hypotheses.md) line 32; Daza 2018 / Shamseer-CENT 2015 / Tate-SCRIBE 2016 / Natesan 2023 / WWC 2022 SCED.

---

## 1. Overall verdict

**REVISION RECOMMENDED (mild).** The draft is structurally faithful to plan §6.5, implements all ten declared content sections plus two additional sections (§5.11 all-seven L-ID block, §5.12 cross-references) consistent with the limitations-doc §5 binding and the §5.12 chain-traceability discipline guides #1-#4 established. **Most importantly, the hard predictive gate from §3.10 is preserved without weakening anywhere in §4-§9.** The §3.12 commentary discipline is implemented faithfully with all four hard separations carried into §5.9 + §6.4 + §7.7 + §7.8 + §7.9 + §7.14. The eight inventions beyond §6.5 are — with two operational concerns and one cross-reference miss — methodologically sound and operationally implementable. The §6.5 four halt-criteria for the §3.6 conflict-resolution rule are concrete at the construct level (parallel to guide #3 §6.1 at the cluster level + guide #4 §6.1 at the topic level); the §5.6 five refusal-to-proceed paths cleanly operationalise the §3.5 missing-inputs binding without creating a backdoor to the §3.10 gate; the §7 fourteen-anti-pattern list is distinct from upstream plan §9, guides #1/#2/#3/#4 anti-patterns; the §9 phased agent-instruction outline is concrete enough that the §11 step 7 skill build will know what to encode. The §5.11 L-ID citation discipline correctly translates limitations doc r3 §5 row for `construct-*.md` into binding form (all seven cited with applies-or-NA; NA-with-reason mandatory). All cited methodology files exist at the named paths.

Five findings drive the REVISION RECOMMENDED verdict rather than ACCEPT. Two are required (R1, R2); three are recommended (A1–A3). None blocks the §11 step 7 skill build or the §11 step 8 dry-run on either K-stress-fatigue-monitoring (tier-1) or K-bout-recovery-signal (tier-2); all five are one-revision-cycle fixes.

- **R1.** §5.5 six-element forward-validation HA shape is operationally sound and maps cleanly onto `hypothesis_lock_process.md` §3.2.4's 10-section pre-reg template (element 1 → §1+§3+§4; element 2 → §4+§6; element 3 → §4+§5; element 4 → §4; element 5 → §5+§9; element 6 → Authorship lock-date), but **element 5 "verdict criteria" leaves the PPV-floor pre-registration choice operationally undefined**. The shape says "SUPPORTED if PPV ≥ pre-registered floor AND lead-time matches pre-registration AND reliability bound computable" without specifying how the floor is anchored (uniform null base rate? base rate per RESEARCH-REPORT §5.2? cluster-level S₁ effect-size confidence interval?). The §5.5 K-stress-fatigue-monitoring worked example invokes "PPV ≥ pre-registered floor at the uniform-three-bin null base rate (~0.33)" but the K-bout-recovery-signal worked example only says "PPV ≥ pre-registered floor at the ~2/year residual-crash base rate" without specifying the anchoring discipline. A one-sentence operational guidance on how the floor is chosen (anchored against the null base rate vs anchored against tier-2 cross-op evidence ceiling) is needed; without it, a future forward-validation HA pre-reg drafter could choose a floor that's trivially passable, which would weaken §3.10 at the §11-step-7-skill-build level. Specifically: the §5.5 shape spec should add a seventh consideration ("PPV floor anchoring discipline") that names which of those two anchors applies in which case (suggested: floor anchored at the null base rate by default; floor anchored at the tier-2 cross-op evidence point estimate when the cross-op replication produced a point estimate; in both cases, the floor cannot be set at or below the null base rate without justifying-the-tier-3-question-itself). See §4 below for the detailed framing.

- **R2.** **§5.10 cross-reference miss.** §5.10 ("Open downgrades from review") names the timing interpretation (filled-at-review-time, not at-drafting-time) and the locked-plan §4 row for actionability-tier-claim artefacts, but **does not cross-reference §6.1 (Tier requirements unmet → tier downgrades) or §6.2 (Forward-validation HA REJECTED → predictive claim removed) for the downgrade-mechanics**. A drafter reading §5.10 alone would not know that the actual downgrade rules live at §6.1 + §6.2 + §6.4. The fix is one-sentence cross-reference: "Per §6 conflict rules: §6.1 governs tier-condition-unmet downgrades (typically tier-2 → tier-1); §6.2 governs forward-validation-HA-REJECTED downgrades (tier-3 → tier-2 with §5.5 forward-validation HA shape addendum); §6.4 governs commentary-vs-evidence conflicts (no tier change, commentary revised)." Without this, the §5.10 review-time fill operates without the rule book it depends on.

Recommended:

- **A1.** Length discipline. 1759 lines lands 3.5% over the upper bound (1700 target). The agent's self-report names eight inventions as the density drivers; the reviewer assesses §5.4 (NOT-DO refusals, mandatory minimum with per-tier additions + two construct-specific worked examples) and §5.11 (worked examples for both active constructs) as the most compressible surfaces. The §5.4 worked example for K-stress-fatigue-monitoring tier-1 is concrete and operationally clear but ~25 lines could fold into the mandatory-minimum framework rather than a separate worked block. The §5.11 worked examples for both constructs run ~90 lines combined; one full paragraph per L-ID per construct doubles the surface unnecessarily — a single full worked example for K-stress-fatigue-monitoring + a compact diff-from-K-stress-fatigue-monitoring for K-bout-recovery-signal (citing only the differences: L2 cross-phase pooling; L6 NA; L7 cross-phase coverage) would save ~30-40 lines without losing operational content. Realistic total: ~50-80 lines (~3-4%) without losing operational content. Not blocking.

- **A2.** §5.7 plain-language combined frame at tier-2 mandatory minimum. The §5.7 spec correctly names PPV + base rate + plain-language combined frame as the three required at tier-2+; the K-bout-recovery-signal worked example correctly implements the plain-language frame ("When the bout-recovery signal fires, a crash day followed within the window N out of M times in past data; crash days occur about 2 per year residual..."). But the §5.7 spec frames the "plain-language combined frame" as item 3 of a numbered list with the per-measure paragraph style; an explicit cross-reference to **§7.4 anti-pattern (bare-percentage actionability) as the enforcement mechanism for the combined-frame requirement** would tighten the §5.7 → §7.4 binding. Currently §7.4 references §5.3 + §5.7 for "carry the frame consistently"; the reverse pointer (§5.7 → §7.4) is the natural completion of the binding loop. One-sentence addition.

- **A3.** §11 lock log entry is dense but at ~50+ lines of unbroken prose it is harder to scan than the per-revision diffs in the upstream guides — same A4 concern guide #4 r1 review flagged. Two-or-three short paragraphs (one for inventions; one for §6.5 ambiguity interpretations; one for the §11 step 7 skill dependency note + the §3 + §5.11 worked-example anchor) would scan better without losing content.

## 2. Four-input bar findings (CONVENTIONS §2.2)

This MD is producer-mode infrastructure (per §3 of the target, per plan §4 row "Guide MDs (6×)") rather than a methodology MD locking a substantive analytical choice; the four-input bar applies in lighter form. Two of the four inputs apply directly; two apply indirectly.

| Input | Status | Reasoning |
|---|---|---|
| 1. Best-practices standards | PASS | The three-tier set (monitoring / informative-pattern / predictive-use) traces to the hard predictive gate's literature anchor (Daza 2018 N-of-1-to-group reach for tier-1/tier-2 monitoring/association vs forward-validated predictive forecasting; CENT 2015 item 22 generalisability for the §5.4 group-level overclaim refusal; SCRIBE 2016 for L4 transparency at the construct level; Natesan 2023 as defensibility bar; WWC 2022 SCED inherited via S₂'s §4.4 evidence-quality framing). The RESEARCH-REPORT §5.2 PPV-with-base-rate precedent is correctly invoked as the project-internal anchor for §5.7 quality measures and §7.4 anti-pattern. The §2 input list cites all six with one-sentence operational role. |
| 2. Established literature | PASS | The §1 "alternatives considered" paragraph cites two rejected paths (folding actionability into Stage T; skipping Stage A) with explicit project-internal precedent and rejection reasoning. The §2 input list, §5.11 worked examples, and §5.12 cross-references draw on the established literature anchors. The RESEARCH-REPORT §5.2 precedent is correctly named as load-bearing for §5.7 + §7.4 in three places (§1, §2 input #8, §5.7). Consistent with guides #2-#4 r1 strength. |
| 3. Tradeoff vision | PASS | The "alternatives considered" paragraph satisfies CONVENTIONS §2.2 item 3 explicitly. Specific judgment-calls visible in the body: (a) three-tier set at §4 as exhaustive (vs continuous tier or two-tier or four-tier — sound; §7.12 forbids invented intermediate labels); (b) §3.10 hard gate at tier-3 (vs hedged-wording tier-3 — sound; the gate is what saves the patient from unearned forecast claims); (c) §3.12 commentary as bounded patient-facing nuance space (vs no-commentary-allowed OR unbounded narrative — sound; the hard separations in §5.9 + §6.4 + §7.7 + §7.8 + §7.9 + §7.14 prevent commentary from backdooring the gate); (d) §5.6 five refusal-to-proceed paths producing `open_inputs` entries rather than silent claim-weakening (sound; matches §3.5 hard rule verbatim). The §5.5 forward-validation HA shape (R1 above) is the one tradeoff axis where operational definition needs tightening. |
| 4. Research limitations + objectives | PASS | The §5.11 worked examples draw from the two active constructs in the map's r3 (K-stress-fatigue-monitoring tier-1, K-bout-recovery-signal tier-2); §5.11 implements the limitations doc r3 §5 row for `construct-*.md` faithfully (all seven cited with applies-or-NA per limitation; NA-with-reason mandatory per the §3 hard rule). The §5.11 L-ID applicability for both constructs matches the map r3 §5 L-ID notes column exactly (K-stress-fatigue-monitoring: L1/L2/L3/L4 apply, L5 NA, L6/L7 apply; K-bout-recovery-signal: L1/L2/L3/L4 apply, L5 NA, L6 NA, L7 applies). The §6.5 four halt-criteria handle the corpus's known map-revision-trigger cases at the construct level; the §5.6 refusal-path-3 (tier-3 wanted but forward-validation HA missing) is the construct-level operationalisation of the §3.10 gate that the corpus's two active constructs sit inside. |

Overall: 4 PASS. The four-input compliance is strong. The trajectory of guide #1 r1 (2 PASS, 2 PARTIAL) → guide #2 r1 (4 PASS) → guide #3 r1 (4 PASS) → guide #4 r1 (4 PASS) → guide #5 r1 (4 PASS) shows the drafting-discipline propagation has fully landed across the layer's five drafted guides.

## 3. Faithfulness to §6.5 spec

§6.5 has nine listed elements (purpose, inputs, output, three tiers, ten-section outline, checklist sketch, conflict rules, anti-patterns, interview seeds, agent-instruction outline). Mapping:

| §6.5 element | Implementation | Faithfulness |
|---|---|---|
| Purpose | §1 (purpose + alternatives + skill-precondition + what Stage A does NOT do) | **Faithful with extension.** The "What Stage A does NOT do" seven-bullet list (re-test verdict / predict without forward-validation / invent caveats / frame as advice / use §3.12 to escape §3.10 / re-decide map / multi-construct-per-session) is operationally important boundary statement. The §3.12 boundary at the seventh bullet is the new-since-§6.5-spec discipline added at plan r5 §3.12. The "alternatives considered" paragraph satisfies CONVENTIONS §2.2 item 3 explicitly. |
| Inputs | §2 (twelve numbered inputs) | **Faithful with extension.** §6.5 names three inputs (Stage S₂ topic; lived-experience priors; hard predictive gate). §2 expands to twelve: adds the synthesis-structure map's §5 construct row (binding for tier-aspiration ceiling + §3.12 commentary-eligibility); the limitations doc (binding for all-seven L-ID citation); forward-validation HAs in the registry (operationalisation of §3.10); RESEARCH-REPORT §5.2 (precedent for §5.7); CONVENTIONS sections. All additions sound and binding. The §3.10 hard predictive gate is correctly named in input #9 as "the **load-bearing constraint of the entire stage**" — the framing matches plan §3.10's "non-negotiable at the layer level" wording verbatim. |
| Output | §3 (path + flat naming + mode + L-ID discipline + worked-example anchors + hard rules) | **Faithful with extension.** §6.5 specifies `analyses/actionability/construct-XXX.md`. §3 specifies flat-no-per-construct-subfolder convention; correctly distinguishes from Stage D's per-HA folder + matches the flat naming guide #4 §3 established for topic-level artefacts. The L-ID citation discipline at the output level correctly translates limitations doc r3 §5 row for `construct-*.md` ("MUST cite all seven, with explicit applicability-or-NA per limitation") into binding form. The two hard rules at §3 (no missing L1-L7; no bare "Lx NA" without project-specific reason) are correctly framed and enforced at §9.6. The worked-example anchors at §3 correctly forecast the §5.11 worked examples for both active constructs. |
| Three tiers | §4 (3 sub-sections + §4.4 summary table) | **Faithful with extension.** §6.5 names the three tiers in a single table with claim shape + required evidence. §4 expands to one sub-section per tier with claim shape, required evidence, §3.10 PPV status, permitted wording, forbidden wording, §3.12 commentary eligibility, worked example. The §4.4 summary table is a structural extension that the §6.5 spec did not name but is operationally helpful for downstream Stage T reader-traceability. The §3.10 status sub-bullets carry the hard-gate-binding correctly: PPV-exempt at tier-1; required at tier-2; required + lead-time + reliability at tier-3. |
| Section outline | §5 (twelve sub-sections, §5.1–§5.12) | **Faithful with extension.** §6.5 names ten sections; §5 implements all ten plus §5.11 (all-seven L-ID block) and §5.12 (cross-references). The §5.11 extension is the limitations-doc §5 binding made-binding at construct level — not in the §6.5 spec but mandated by the limitations doc r3 §5 row for `construct-*.md`. The §5.12 extension matches guides #1-#4 §5/§4 chain-traceability discipline. The §5.6 "specific to the §6.5 spec brief" framing of the `open_inputs` block correctly carries the four-field shape per §3.5 + §6.5 explicit "fallback tier the artefact has therefore been capped at" requirement. |
| Checklist sketch | Folded into §5 sub-sections + §9.6 refuse-to-lock gate | **Faithful.** The §6.5 checklist's five bullets (tier no higher than evidence; wording does not drift to advice; predictive claim names HA; easy overclaims refused; v1.5+ connection framed as request) are implemented across §5 + §9.6: tier ceiling (§5.2 + §9.6 item 1-3 + §6.1); advice prohibition (§5.4 + §7.2 + §9.6 item 5); HA name (§5.5 + §9.6 item 7); overclaims refused (§5.4 + §9.6 item 6); v1.5+ — implicit at §5.8 follow-up. The fifth checklist item (v1.5+ connection) is the only one that does not land explicitly in §5 or §9.6 — see §5 finding below for whether this is a gap or correctly subsumed. |
| Conflict rules | §6 (5 rules) | **Faithful with extension.** §6.5 names 3 conflict rules (tier requirements unmet; forward-validation HA REJECTED; lived-experience prior without forward-validation HA). §6 implements all 3 (§6.1, §6.2, §6.3) and adds §6.4 (commentary-vs-forward-validation conflict — the §3.12 hard-separation "cannot promote tier" at the per-construct level) and §6.5 (map-change-needed = the §3.6 layer-rule operationalisation, parallel to guide #3 §6.1 + guide #4 §6.1). Both additions sound and necessary; §6.4 is the load-bearing addition for the §3.12 commentary discipline. |
| Anti-patterns | §7 (14 anti-patterns) | **Faithful with extension.** §6.5 names 5 anti-patterns (promoting retrospective fit; framing as advice; collapsing presence-conditioned; single HA = monitoring tier; backdoor predictive via wording). §7 implements all 5 (§7.1, §7.2, §7.3 + §7.11, §7.5) and adds 9 more (§7.4 bare-percentage; §7.6 inventing new caveats; §7.7 bare-narrative-as-actionability; §7.8 commentary-promotion fallacy; §7.9 downstream-citation-of-commentary; §7.10 PPV at HA-test level; §7.12 inventing new tier labels; §7.13 re-routing topics in-stage; §7.14 producing commentary at tier-3). All nine additions distinct and sound — §7.7-§7.9 + §7.14 operationalise the §3.12 hard separations at anti-pattern level; §7.4 + §7.10 operationalise the §3.10 binding at anti-pattern level. |
| Interview seeds | §8 (3 required + 1 optional) | **Faithful with extension.** §6.5 names 3 seeds (tier reach; forward-validation; harm scenario). §8 implements all 3 (§8.1, §8.2, §8.3) and adds §8.4 (commentary-shape interview, for §5.9). Optional fourth parallels guides #1-#4 §8.4 confirmation-seed pattern but carries §3.12-specific discipline (eligibility check; permitted-wording-only; hard-separations reminder). Sound and necessary for the §3.12 layer. |
| Agent-instruction outline | §9 (8 phases) | **Faithful with extension.** §6.5 names 4 bullets (Load / Refuse / Walk / Produce). §9 expands to 8 phases (Load / Gate / Extract / Interview / Produce / Refuse-to-lock-gate / Review-handoff / Acceptance + drift-trigger registration). The Refuse-to-lock gate enumerates 15 structural checks (agent self-reports fifteen; literal count confirms 15). Extension correct because the relevant plan rules (§3.7 drift; §3.8 completion; §3.10 + §3.12 bindings; §4 producer/reviewer-split row; §11 step 7 skill dependency) post-date §6.5's sketch. |

No §6.5 element is missing or substantively altered. Spec faithfulness is high — matches guide #2 r1 / guide #3 r1 / guide #4 r1 strength on the §6.5 spec discipline. The two §6.5 spec ambiguities the agent's self-report flags (constructed-claim base-rate framing fail routing; §5.10 timing) are resolved cleanly: the base-rate-framing-fail routing is operationalised at §5.6 refusal-path-5 (tier-1 fallback with re-cast monitoring wording) consistent with §3.10's "skill never lets an uncalibrated quasi-predictive claim pass with hedged wording" binding; the §5.10 fill-at-review-time interpretation is the only one consistent with the plan §4 row's "tier downgrades on review concerns" framing (drafting-time downgrades would already be reflected in §5.2/§5.3 via §6.1 conflict rule, leaving §5.10 with no drafting-time content).

## 4. The eight inventions beyond §6.5

### Invention 1 — §4.4 tier mapping summary table

**Sound.** The §6.5 spec carries the three tiers in a single table with claim shape + required evidence; §4.4's summary table extends to six columns (tier / claim shape / evidence floor / §3.10 PPV / forward-validation HA / §3.12 commentary). The added §3.12 commentary column reflects the plan r5 §3.12 addition that post-dates the §6.5 spec; the added §3.10 PPV column makes the binding visible at the tier-mapping surface (currently buried in the per-tier sub-sections). The "discipline cascade" closing paragraph (monitoring = descriptive; informative-pattern = historical-association; predictive-use = forecast; tier promotion requires higher evidence floor, not stronger wording) is the right closing framing.

The table is operationally implementable and matches the §4.1-§4.3 per-tier sub-sections faithfully.

### Invention 2 — §5.2 three-paragraph evidence-layer structure

**Sound.** The §6.5 spec names "Evidence layer (which tiers' requirements are met / unmet)" as section 2 of the outline without specifying the internal structure. §5.2's three-paragraph structure (one per tier, with met/unmet check + which condition fails + §5.6 routing) is the right reduction. The closing line "tier earned at this Stage A time" is the binding output the §5.3 claim depends on; making this explicit at the close of §5.2 is operationally helpful. The "earned tier vs map aspiration as ceiling" framing carried throughout §2 input #5, §5.1, §5.2 is the right distinction (the §3.10 gate operates on earned tier, not aspiration).

The §5.2 tier-3 evidence-check paragraph carries the §3.10 hard predictive gate framing correctly: "the §3.10 hard predictive gate: if any of the forward-validation HA conditions fail, tier-3 is structurally unreachable and the construct caps at tier-2."

### Invention 3 — §5.5 six-element forward-validation HA shape

**Sound with one operational gap (R1 above).** The six elements (target+signal; prediction window; prediction rule; outcome operationalisation; verdict criteria; pre-registration lock date) cover the operationally distinct pre-reg fields a forward-validation HA needs. The mapping onto `hypothesis_lock_process.md` §3.2.4's 10-section pre-reg template is clean: element 1 → §1 Claim + §3 Data sources + §4 Measurement protocol; element 2 → §4 + §6 Exclusion rules; element 3 → §4 + §5 Pre-registered falsification criterion; element 4 → §4; element 5 → §5 + §9 What we do with each outcome; element 6 → Authorship block lock-date. A future forward-validation HA pre-reg drafter could write each element into its pre-reg section straightforwardly.

The §5.5 worked-example sketches for both active constructs (K-stress-fatigue-monitoring: ~90-day Stratum 4 window, inverted-U-peak-bin predicts D+1 gevoelscore range; K-bout-recovery-signal: ~180-day cross-phase pooled window, heavy-T threshold predicts crash-day D+L) are concrete and operationally implementable — the operationalisations name actual columns + actual cells + actual base rates.

**R1 above** is on element 5 (verdict criteria) operational definition: the shape leaves "pre-registered PPV floor" without anchoring discipline. The K-stress-fatigue-monitoring example correctly anchors at the uniform-three-bin null base rate (~0.33); the K-bout-recovery-signal example references the ~2/year residual-crash base rate without specifying whether the floor is anchored at that base rate or above the tier-2 cross-op evidence point estimate (HA-C4c Cliff's δ = +0.120; +20.26 pp discrimination per map §5). Without anchoring discipline, a future drafter could choose a floor at the null base rate plus a trivial margin and "pass" tier-3 forward-validation without the predictive evidence the §3.10 gate intends. The shape needs a seventh "PPV floor anchoring discipline" consideration to close this. See §7 below for the proposed addition.

### Invention 4 — §5.6 five refusal-to-proceed paths

**Sound (with R2 cross-reference observation).** The five refusal paths (topic missing → halt; construct not in map → halt; tier-3 forward-validation HA missing → proceed at tier-2 fallback; tier-2 PPV uncomputable → proceed at tier-1 fallback; constructed-claim base-rate framing fail → proceed at tier-1 with re-cast monitoring frame) cover the operationally distinct refusal cases at the construct level. The four-field entry shape (what is missing; what is blocked; cheapest acquisition path; fallback tier) matches §3.5 binding verbatim plus the §6.5 spec's "fallback tier the artefact has therefore been capped at" requirement.

The crucial distinction the §5.6 spec carries: refusal-paths 1 and 2 produce only `open_inputs` entries (the construct artefact is not drafted); refusal-paths 3, 4, 5 produce a fallback-tier draft + `open_inputs` entry. This is the right operational distinction — refusal-paths 1 and 2 are upstream-chain gaps that block the artefact entirely; refusal-paths 3, 4, 5 are within-stage tier-promotion gaps where the lower-tier claim is still earned.

**Critical for R1's "does §5.6 create a backdoor to the §3.10 gate?"** check: No. Refusal-path 3 explicitly falls back to tier-2 (or tier-1 if tier-2 fails); refusal-path 4 falls back to tier-1; refusal-path 5 falls back to tier-1 with re-cast wording. None of the refusal paths permit a tier-3 claim without the forward-validation HA. The §5.6 routing preserves the §3.10 gate at the operational level. **Sound.**

### Invention 5 — §5.7 per-measure block structure (3 required at tier-2+ + 6 optional)

**Sound (with A2 binding-loop observation).** The three required measures at tier-2+ (PPV; base rate; plain-language combined frame) implement the §3.10 binding faithfully. The six optional measures (NPV; sensitivity; specificity; false-alarm rate; lead time; reliability) with lead-time + reliability **required at tier-3** correctly implement the §3.10 tier-3 discipline ("A predictive claim that does not specify 'a day in advance' vs 'an hour in advance' is operationally meaningless; one that does not check whether the signal is stable across similar days has no defence against random-walk artefacts").

The per-measure paragraph format (one paragraph per measure with plain-language frame) is operationally clear. The §5.7 K-bout-recovery-signal worked example correctly implements the plain-language combined frame ("When the bout-recovery signal fires, a crash day followed within the window N out of M times in past data; crash days occur about 2 per year residual...").

The §5.7 conflict-rule paragraph correctly carries §3.10's "tier downgrades to tier-1 (monitoring) per §3.10 conflict rule" routing for PPV-uncomputable cases.

**A2 above** is on the §5.7 → §7.4 binding-loop completion. Currently §7.4 references §5.3 + §5.7 ("§5.3 + §5.7 carry the frame consistently"); the reverse pointer from §5.7 to §7.4 (citing §7.4 as the enforcement mechanism for the combined-frame requirement) would tighten the binding.

### Invention 6 — §6.4 commentary-vs-forward-validation conflict rule

**Sound — this is the load-bearing operationalisation of the §3.12 commentary discipline.** The §3.12 layer-binding says "commentary cannot promote tier; only forward-validation HA per §3.10 unlocks tier-3"; §6.4 operationalises this at the per-construct conflict-rule level. The rule handles the specific case where §5.9 commentary content would, if read as analytical input, suggest a higher tier than §5.2 earned: commentary stays at language-bounded form; tier stays at §5.2 level; the two epistemic categories do not arithmetic-combine.

The second paragraph of §6.4 handles **the precursor case** correctly (the case my review concern 3 specifically asked about): "If commentary surfaces a candidate own-research HA the §5.8 track missed, the candidate is added to §5.8 (routing through `hypothesis_lock_process.md`); commentary does not double as own-research entry." This is the right routing — commentary that emerges as a precursor to a forward-validation HA pre-reg gets logged at §5.8 follow-up track, not at §5.9 itself; the commentary section stays bounded to its own discipline. **Sound.**

### Invention 7 — §6.5 four halt-criteria for map-change-needed

**Sound.** The plan §3.6 conflict-resolution rule names the discipline at the layer level; the four concrete halt-criteria (feeding topic lands on different construct; construct's tier evidence requires evidence from non-map topic; map's tier aspiration incompatible with §5.2 evidence layer; §3.12 commentary-eligibility status wrong) are operationally implementable and parallel guide #3 §6.1's four halt-criteria at the cluster level + guide #4 §6.1's four halt-criteria at the topic level.

The route-out instructions (stop drafting mid-session; do NOT save a partial artefact; do NOT edit the map in-session; produce only the §5.6 `open_inputs` entry; hand off to user with halt-criterion + proposed change; resume only after separate producer-mode session updates the map) match plan §3.6's "halt-and-route" discipline verbatim.

The four halt-criteria are exhaustive for the cases the §3.6 rule was designed for at the construct level. Criterion 4 (the §3.12 commentary-eligibility status case) is the new-since-§6.5-spec discipline added at plan r5 §3.12 propagated through map r3; correctly added at this guide.

### Invention 8 — §9.6 fifteen-item refuse-to-lock gate

**Sound (modulo R2's §5.10 cross-reference observation).** The 15 checks (L1-L7 missing; L-ID NA without justification; tier-2+ missing §3.10 PPV-with-base-rate; tier-claim forbidden wording; advice-form wording; missing NOT-DO refusal categories; §5.5 missing for tier-3; lock-date violates §3.10; bare-percentage without base-rate; commentary at tier-3; commentary forbidden wording; commentary suggests tier promotion; commentary floats unattached; external-research N=1-scoping; any §5 section contains §7 violations) are the right structural gates. Each maps to a §5 sub-section requirement or to a §3.10/§3.12 binding, so the gate is implementable as a skill-level check rather than as judgment.

Spot-checking three items for distinctness and implementability:
- **Item 8 (lock-date violates §3.10)**: implementable as date-comparison between the §5.5 forward-validation HA's `## Authorship` block lock-date and the prediction-window start; this is the most rigorous of all the items (the single item that operationalises the §3.10 "locked before the prediction window begins" binding). Distinct from item 7 (which is presence-check, not date-check). **Sound and load-bearing.**
- **Item 11 (commentary forbidden wording)**: implementable as text-pattern detection on §5.9 against the §3.12 forbidden-wording list ("predicts", "forecasts", "will happen", "tomorrow", "X means Y", "this signals that..."); distinct from item 12 (commentary suggests tier promotion — semantic check, not lexical). **Sound and implementable.**
- **Item 12 (commentary suggests tier promotion)**: harder to implement at the skill level than items 11 (lexical) or 13 (unattached check). The skill needs to compare §5.9 commentary content against the §5.2 earned tier; if commentary content reads as evidence for a higher tier, refuse. This is essentially the §6.4 conflict rule enforced at lock time. Implementable as user-prompt at refuse-to-lock time ("Does §5.9 commentary read as evidence for a higher tier than §5.2 earned?") rather than as autonomous skill check; the §8.4 commentary-shape interview's "skill refuses to lock if commentary suggests tier promotion" framing already anticipates this. **Sound but harder to fully automate.**

Collectively the 15 items are complete enough to enforce the hard predictive gate: items 3, 7, 8, 9 enforce the §3.10 binding (tier-2+ PPV-with-base-rate; tier-3 §5.5 presence; lock-date discipline; bare-percentage prohibition); items 10, 11, 12, 13 enforce the §3.12 binding (commentary at tier-3 prohibition; forbidden wording; tier-promotion prohibition; unattached prohibition); items 1, 2, 5, 6 enforce the L-ID + advice + NOT-DO baseline; items 4, 14, 15 enforce the wording/scoping/anti-pattern baseline.

R2 above is a cross-reference completeness observation, not a §9.6 gate gap.

## 5. Per-section findings

### §1 Purpose

Sound. The block-quote framing ("A construct's topic-level positioning is a within-subject finding placed against external literature. Stage A produces — or refuses to produce — a daily-life-signal claim at one of three tiers...") matches plan §6.5's opening framing. The seven-bullet "What Stage A does NOT do" list correctly carries the §3.10 binding (second bullet), §3.12 boundary (fifth bullet), §3.6 map-change-needed routing (sixth bullet). The opening paragraph's "Stage A is the **highest-risk surface in the layer**" framing matches plan §6.5's "the highest-risk surface in the layer; the hard predictive gate is intentionally severe" framing verbatim. The "Alternatives considered" paragraph satisfies CONVENTIONS §2.2 item 3 explicitly. The skill-precondition note matches guides #1-#4 framing.

### §2 Inputs

Sound. The twelve numbered inputs cover §6.5's three plus the layer-level binding additions. Input #9 ("the hard predictive gate from §3.10") correctly names the gate as "the **load-bearing constraint of the entire stage**" — the framing is faithful to the plan §3.10 "non-negotiable at the layer level; guide drafts may not weaken it" binding. Input #10 (§3.12 commentary-eligibility status from map's r3 §5 row) and input #11 (lived-experience priors with the explicit "cannot promote the tier without forward-validation HA" framing) correctly carry the §3.12 + §6.3 conflict-rule discipline. Input #8 (RESEARCH-REPORT §5.2 PPV-with-base-rate precedent) is correctly cited with the verbatim quote from the source.

The closing "what the translation does NOT load" paragraph is the right negative-space discipline (rejects: raw descriptive runs; member HAs' `test.py`; other constructs' `construct-*.md` files).

### §3 Output

Sound. The flat-no-per-construct-subfolder convention matches the locked plan §5 output tree. The L-ID citation discipline at the output level correctly translates limitations doc r3 §5 row for `construct-*.md` ("MUST cite all seven, with explicit applicability-or-NA per limitation") into binding form. The two hard rules at §3 (no missing L1-L7; no bare "Lx NA" without project-specific reason) are correctly framed and enforced at §9.6 gates 1-2.

The §3 worked-example anchors align with the synthesis-structure map r3 §5 construct row L-IDs columns exactly:
- K-stress-fatigue-monitoring: L1/L2/L3/L4/L6/L7 apply + L5 NA → matches map r3 §5 row verbatim (L1 applies, L2 applies (unmed only), L3 applies (Garmin signal), L4 applies (Wiggers prior), L5 NA (no v24 primary), L6 applies (gevoelscore), L7 applies (gating dropouts)).
- K-bout-recovery-signal: L1/L2/L3/L4/L7 apply + L5 NA + L6 NA → matches map r3 §5 row verbatim (L1 applies, L2 applies (cross-phase pooled per HA-C4c), L3 applies (bout-derived Garmin), L4 applies (Wiggers prior), L5 NA (no v24), L6 NA (gevoelscore not in primary cell), L7 applies (gating + cross-phase coverage)).

Both anchors carry the tier aspiration verbatim from the map (K-stress-fatigue-monitoring tier-1 PPV-exempt; K-bout-recovery-signal tier-2 PPV-required) and the §3.12 commentary-eligibility verbatim (both eligible per map r3 §5 row).

### §4 The three tiers

Sound. §4.1 (tier-1 monitoring) + §4.2 (tier-2 informative pattern) + §4.3 (tier-3 predictive use) carry the §3.10 PPV status binding faithfully at each tier. The forbidden-wording lists per tier correctly enforce the §3.10 gate at the wording level (per §7.5 anti-pattern). The §3.12 commentary-eligibility note per tier is correct (tier-1 + tier-2 eligible; tier-3 NOT eligible per §3.12 hard separation 4).

The §4.1 worked example for K-stress-fatigue-monitoring correctly reads tier-1 only — "Daily `all_day_stress_avg` tracks daily `gevoelscore` descriptively across the Stratum 4 unmedicated window. The two signals move together with an inverted-U shape peaking around mid-stress" — correctly omits forecast frame ("tomorrow's gevoelscore"); correctly avoids the inverted-U vs Wiggers-monotone-convex DIVERGES content (that lives at S₂ topic level, not Stage A). The worked example's "tier-1 wording deliberately omits 'tomorrow's gevoelscore'..." closing line is the right §3.10-gate-aware framing.

The §4.2 worked example for K-bout-recovery-signal correctly carries the tier-2 "associated with under conditions" framing with explicit cross-phase pooled cell + ~2/year residual base rate reference + RESEARCH-REPORT §5.2 precedent citation. The "if §5.7 PPV-with-base-rate computes" conditional framing correctly preserves the §3.10 conflict rule routing.

The §4.3 worked example "none active in the map's r3" framing correctly handles the upstream state — neither active construct reaches tier-3.

§4.4 summary table (Invention 1) is sound; see §4 Inventions above.

### §5 Section outline

Sound (modulo R2 cross-reference, R1 operational definition, A1 length, A2 binding loop).

**§5.1 (target construct + originating topic)**: sound; mechanical header copy from map row + each feeding topic's §4.1 header; correctly carries the tier aspiration + §3.12 commentary-eligibility status from map verbatim.

**§5.2 (evidence layer)**: sound (per Invention 2). The three-paragraph structure with "tier earned at this Stage A time" closing line is the right operational shape. The tier-3 evidence-check paragraph correctly carries the §3.10 hard predictive gate framing ("if any of the forward-validation HA conditions fail, tier-3 is structurally unreachable").

**§5.3 (tier claim + permitted wording)**: sound; the one-paragraph-per-claim structure with explicit signal name + construct name + era/cohort/condition scope is the right operational shape. The "permitted-wording list for the subject at the claim's tier" framing correctly forecasts Stage T's translation source.

**§5.4 (NOT-DO refusals)**: sound; the mandatory minimum at tier-1 (4 categories) + additions at tier-2 (2 more) + additions at tier-3 (2 more) cover the easy overclaims per tier. The K-stress-fatigue-monitoring worked example is concrete and operationally clear. **A1 above** is on the worked-example length (~25 lines compressible into the mandatory-minimum framework).

**§5.5 (forward-validation pathway)**: sound (modulo R1 above). The mandatory-when conditions (tier-3 wanted but not earned; tier-3 earned with HA citation) + the not-aspired record-with-rationale framing handle the three operational cases cleanly. The six-element shape (Invention 3) is operationally implementable but needs the PPV-floor anchoring discipline addition per R1.

**§5.6 (`open_inputs` block)**: sound (per Invention 4). The five refusal-to-proceed paths cover the construct-level refusal cases without backdoor risk. The four-field entry shape matches §3.5 binding verbatim + §6.5 spec's "fallback tier" requirement.

**§5.7 (quality measures)**: sound (per Invention 5, modulo A2). The three required at tier-2+ (PPV; base rate; plain-language combined frame) + six optional with tier-3-required-lead-time-+-reliability correctly implement §3.10. The §3.10 conflict-rule routing at the close of §5.7 ("the skill never lets an uncalibrated quasi-predictive claim pass with hedged wording") correctly carries the load-bearing §3.10 binding at the §5.7 level.

The §5.7 closing paragraph ("Forbidden at the HA-test level... required at the actionability layer") correctly carries the §3.10 + `personal_hypotheses.md` line 32 two-direction discipline (HA-test = reality of relationship; Stage A = usability of relationship in life) and is enforced at §7.10 anti-pattern.

**§5.8 (follow-up suggestions)**: sound; the own + external two-track structure matches §3.11 binding. The own-research track correctly cross-references §5.5 forward-validation HA shape; the external-research track correctly requires N=1 limit scoping per §3.11 binding (the §5.8 reasoning paragraph cites L1 / L3 / L4 per study type). The two worked-example sketches (K-stress-fatigue-monitoring: PEM-pacing cohort + intervention; K-bout-recovery-signal: CPET-based bout-recovery + intervention RCT) are concrete pre-reg shapes rather than vague directions.

**§5.9 (commentary)**: sound — this is the load-bearing §3.12 operationalisation at the construct artefact level. The four required disciplines when filled (cite attached claim; subject-attribution every sentence; permitted language; forbidden language) match §3.12 binding verbatim. The five hard separations (cannot promote tier; cannot be cited downstream; cannot float unattached; forbidden in research-audience translation track; layperson-test propagation per §6.6) correctly carry §3.12 + §6.6 binding. The two worked examples for K-stress-fatigue-monitoring tier-1 + K-bout-recovery-signal tier-2 are concrete and operationally clear; both correctly carry subject-attribution every sentence + permitted-wording-only.

**Critical for review concern 7 (tier-3 boundary check)**: §5.9 correctly carries "NOT eligible per §3.12 hard separations" at the tier-3 boundary in two places — the §4.3 tier-3 sub-section's §3.12 status bullet AND the §5.9 opening paragraph ("It does NOT attach to tier-3 (tier-3 carries forward-validation HA evidence; §7.14 anti-pattern enforces)"). The §7.14 anti-pattern is the third enforcement layer. **Tier-3 boundary correctly closed.**

**§5.10 (open downgrades from review)**: sound (modulo R2 cross-reference miss). The fill-at-review-time framing correctly handles the timing ambiguity from §6.5 spec. R2 above is on the cross-reference to §6.1 + §6.2 + §6.4 for the downgrade-mechanics — without this, the §5.10 review-time fill operates without the rule book it depends on.

**§5.11 (L-ID block)**: sound — this is the most rigorous L-ID discipline in the layer (all seven cited with applies-or-NA per limitation; NA-with-reason mandatory). The worked-example sketches for both active constructs are concrete and align with the limitations doc r3 §5 row + map r3 §5 L-ID notes column exactly.

**Spot-checking the K-stress-fatigue-monitoring §5.11 worked example against limitations doc r3 §3**:
- L1 (single-subject reach): correctly invokes Daza 2018; correctly cites §5.8 group-level study cross-reference.
- L2 (era confounds): correctly bounded to Stratum 4 unmedicated per feeding topic positioning.
- L3 (device generations): correctly cites FR245 Elevate V3 `all_day_stress_avg` + §3.7 drift trigger on device upgrade.
- L4 (analyst-is-subject): correctly cites Wiggers convex-cost prior + fresh-session `/research-review` + §5.10 review-time tier-downgrade gate; correctly notes "advice forms forbidden per §5.4 + §7.2 because L4 prevents the intervention-study design advice would require."
- L5 NA: correctly cites "feeding cluster C-stress-fatigue-shape has no v24 primary signals per map §3" — matches map r3 §3 row verbatim.
- L6 (self-reporting): correctly cites gevoelscore + "tier-1 claim respects the subjective-reporting noise floor — works at bin-level range, not per-point."
- L7 (survivorship): correctly cites gating on `all_day_stress_avg` non-NaN and `gevoelscore` non-NaN within Stratum 4 unmedicated.

All seven cited; all citations operationally specific and project-grounded. Sound.

**Spot-checking the K-bout-recovery-signal §5.11 worked example against limitations doc r3 §3**:
- L1: correctly invokes Daza 2018 with the "tier-2 informative-pattern claim (if PPV computes per §5.7) is within-subject association across cross-phase pooled cell" framing.
- L2: correctly cites HA-C4c's cross-phase pooling + warrant + per-phase reporting + `citalopram_phase_stratification.md` §5 correction discipline.
- L3: correctly cites FR245-derived bout signal.
- L4: correctly cites HA-C4c Wiggers within-day-recovery prior + L4-aware methodology choice rationale.
- L5 NA: correctly cites "C-bout-substance has no v24 primary signals per map §3" — matches map r3 §3 row.
- L6 NA: correctly cites "gevoelscore not in C-bout-substance's primary cell per map §5" — matches map r3 §5 row verbatim (the L6 NA reason "gevoelscore not in primary cell").
- L7: correctly cites HA-C4c gating on cross-phase pooled cell + heavy-T classifier coverage + §5.8 unmedicated-only sister-HA follow-up.

All seven cited; all citations operationally specific. Sound.

**§5.12 (cross-references)**: sound; the destinations cover the full forward + upstream chain. Spot-checked references:
- `_plan_results_analysis_layer.md` §3.5/§3.6/§3.7/§3.8/§3.9/§3.10/§3.11/§3.12/§4/§6.5 — all exist (verified).
- `synthesis_structure_map.md` §2/§3/§4/§5 — all exist (verified; the §5 K-rows for the two active constructs match the §3 + §5.11 worked examples).
- `research_line_limitations.md` §3/§5/§8 — all exist (verified; the §5 row for `construct-*.md` "MUST cite all seven with applies-or-NA" is correctly cited verbatim).
- `external_contextualisation.md` (guide #4 LOCKED r2) — referenced for immediate upstream gate; verified to exist.
- `internal_synthesis.md` / `verdict_to_inference.md` / `descriptive_precondition_audit.md` (guides #3/#2/#1 LOCKED r2) — all verified to exist.
- `RESEARCH-REPORT.md` §5.2 — verified to exist; line 320 contains the PPV-with-base-rate precedent quote ("The positive predictive value of any such alert, even computing optimistically from H02b's train-window evidence, is ~4% at the residual-crash base rate of ~2 per year. A predictive alert card would be wrong 24 times out of 25.") verbatim against the §5.7 quote.
- `personal_hypotheses.md` "§32" — verified; line 32 contains "Descriptive characterisation, not classifier discrimination — no AUCs, no logistic regression, no joint-model verdicts. Means, CIs, effect sizes only." The "§32" citation style matches the plan §3.10's citation style (both reference line 32, not a section 32 that doesn't exist) — consistent with the project pattern.
- `hypothesis_lock_process.md` — verified to exist; §5.5 + §5.8 own-research routing references are correctly anchored.
- `bout_level_recovery_dynamics.md` / `citalopram_phase_stratification.md` / `symptom_mention_asymmetry.md` — all verified to exist.

The cross-reference layer is in good shape; no broken links found in the spot-check. R2 above is on the §5.10 → §6.1/§6.2/§6.4 missing cross-reference, not on the §5.12 chain.

### §6 Conflict rules

Sound. §6.1 (tier requirements unmet → tier downgrades), §6.2 (forward-validation HA REJECTED → predictive claim removed), §6.3 (lived-experience prior without forward-validation HA → recorded but does not promote tier) are direct cite-and-implement of the §6.5 spec's three conflict rules. §6.4 (commentary-vs-forward-validation conflict — Invention 6) is the load-bearing addition for §3.12 discipline; §6.5 (map-change-needed = §3.6 layer-rule operationalisation — Invention 7) is the construct-level analogue of guide #3 §6.1 + guide #4 §6.1.

§6.2 correctly carries the "tier-3 inertia" prohibition ("Per §3.10: the gate is non-negotiable for promotion AND for maintenance — tier-3 evidence must remain SUPPORTED at every drift re-examination; no tier-3 inertia"). This is the §3.10 binding at the maintenance level, not just the promotion level. Sound and operationally important.

### §7 Anti-patterns

Sound. The 14 anti-patterns + the §6.5 spec's 5 are correctly mapped. The 9 additions (§7.4 bare-percentage; §7.6 inventing new caveats; §7.7 bare-narrative-as-actionability; §7.8 commentary-promotion fallacy; §7.9 downstream-citation-of-commentary; §7.10 PPV at HA-test level; §7.12 inventing new tier labels; §7.13 re-routing topics in-stage; §7.14 producing commentary at tier-3) are distinct and sound.

**Reviewer concern 11 check (three new layer-level anti-patterns from plan §9 at Stage A)**:
- Bare-percentage actionability → §7.4. Correctly cites RESEARCH-REPORT §5.2 + §5.3 + §5.7. Sound.
- Backdoor predictive via wording → §7.5. Correctly cites §3.10 + §3.12 + §4 permitted-wording lists per tier. Sound.
- Collapsing presence-conditioned to prevalence → §7.3. Correctly cites L5 + §5.11 binding. Sound.

All three layer-level anti-patterns from plan §9 are operationalised at Stage A. Per reviewer concern 11.

The §7.7-§7.9 + §7.14 cluster of commentary anti-patterns correctly operationalise the §3.12 hard separations at the anti-pattern level (forbidden-floating; commentary-cannot-promote; commentary-cannot-be-cited; commentary-cannot-attach-to-tier-3). Each correctly cross-references the §3.12 binding + the §5.9 + §6.4 conflict-rule implementation.

### §8 Interview-prompt seeds

Sound. The 3 required seeds (tier reach; forward-validation; harm scenario) match §6.5 spec verbatim. The §8.4 optional fourth (commentary-shape interview) parallels guides #1-#4 §8.4 confirmation-seed pattern but carries §3.12-specific discipline. The §8.4 closing paragraph ("§5.9 commentary is drafted in advance of the Stage T patient-audience layperson test... Downstream test failure on commentary wording propagates back to Stage A's §5.9 per §3.7 drift") correctly carries the §3.12 + §6.6 layperson-test-propagation binding.

The §8.2 (forward-validation interview) "Skill MUST NOT autonomously fill any element (pre-reg is the user's discipline gate)" framing correctly carries the §3.10 binding at the interview level.

### §9 Agent-instruction outline

Sound (per Invention 8). The eight phases are concrete. The §9.6 refuse-to-lock gate's 15 structural checks are the right protection layer. The §9.7 review handoff correctly routes to `/research-review` (matches plan §4 row for actionability-tier-claim artefacts: "Skill-driven, with **hard gate** / Fresh-session `/research-review`; tier downgrades on review concerns"). The §9.8 acceptance + drift-trigger registration enumerates 4 re-examination triggers (per §3.7 + commentary-carrying constructs add a fifth trigger: Stage T patient-audience layperson test fails on commentary wording).

The §9.4 closing paragraph ("Skill MUST NOT autonomously fill §5.2 tier earned, §5.5 forward-validation shape, or §5.9 commentary") correctly carries the discipline that judgment-call fields require user articulation, not skill autofill.

### §10 Cross-references

Comprehensive. Spot-checked links pass (per §5.12 spot-check above).

### §11 Lock log

Per A3 above: ~50+ lines of unbroken prose. Content is correct (eight named inventions; two §6.5 ambiguity interpretations; named-invention-beyond-spec flag on §6.5 base-rate-framing-fail routing as the strongest invention for reviewer attention). The narrative explanation of what each invention does is helpful for a future reviewer, but the scannability is lower than the per-revision-diff format used in upstream guides' lock logs.

## 6. Cross-cutting concerns

### §3.10 hard predictive gate preservation (the load-bearing review check)

**Strongly enforced; no backdoors found.** Verified at five enforcement layers:

1. **Layer-binding statement**: §1 + §2 input #9 correctly name §3.10 as "non-negotiable" / "load-bearing constraint of the entire stage" — faithful to plan §3.10 binding.
2. **Tier mapping (§4)**: §4.3 tier-3 sub-section requires both pre-registered forward-validation HA AND SUPPORTED verdict ("A pre-registered forward-validation HA... must be named in the registry, locked before the prediction window begins, predict on unseen days, and produce a SUPPORTED verdict on its `result.md`. Retrospective-only fit does NOT qualify"). The "SUPPORTED" verdict requirement (not just "registered") is correctly carried — see reviewer concern 2(a) check below.
3. **Evidence-layer check (§5.2)**: tier-3 evidence-check paragraph carries "the §3.10 hard predictive gate: if any of the forward-validation HA conditions fail, tier-3 is structurally unreachable and the construct caps at tier-2."
4. **Refusal-paths (§5.6)**: refusal-path-3 (tier-3 wanted but forward-validation HA missing) correctly falls back to tier-2 (or tier-1 if tier-2 also fails) — no tier-3 backdoor created.
5. **Refuse-to-lock gate (§9.6)**: items 3 + 7 + 8 + 9 enforce the §3.10 binding at lock time (tier-2+ PPV-with-base-rate required; §5.5 mandatory for tier-3; lock-date precedes window-start; bare-percentage prohibited).

**Reviewer concern 2(a) check (tier-3 unlock requires SUPPORTED, not just registered)**: §4.3 says "produce a SUPPORTED verdict on its `result.md`"; §5.2 says "with a SUPPORTED verdict on its `result.md`"; §5.5 element 5 says "SUPPORTED if PPV ≥ pre-registered floor AND lead-time matches pre-registration AND reliability bound computable"; §5.5 says "the registry HA that earned it" (earned = SUPPORTED verdict). **Faithful at all four touchpoints.**

**Reviewer concern 2(b) check (§5.6 refusal paths don't create backdoor)**: see Invention 4 above — none of the five refusal paths permit a tier-3 claim without the forward-validation HA. **Faithful.**

**Reviewer concern 2(c) check (§9.6 enforces hard rule)**: items 3 + 7 + 8 + 9 enforce the §3.10 binding at lock time (per §9.6 spot-check above). **Faithful.**

### §3.12 commentary discipline implementation (the second load-bearing review check)

**Strongly enforced.** All four hard separations from §3.12 are operationalised at §5.9:

1. **Cannot promote tier**: §5.9 hard-separations #1 carries "Cannot promote tier"; §6.4 commentary-vs-forward-validation conflict rule operationalises; §7.8 anti-pattern (commentary-promotion fallacy) enforces; §9.6 gate 12 refuses to lock if commentary suggests tier promotion. Four-layer enforcement.
2. **Cannot be cited downstream**: §5.9 hard-separations #2 carries "Cannot be cited as evidence"; §7.9 anti-pattern (downstream-citation-of-commentary fallacy) enforces; Stage A's `construct-*.md` is correctly named as "the **one place commentary lives in research artefacts**, and even there it is attached-and-bounded per §3.12." Two-layer enforcement.
3. **Cannot float unattached**: §5.9 hard-separations #3 carries "Cannot float unattached"; §5.9 required-discipline #1 requires "attached to: K-XXX tier-N claim per §5.3" opening line; §7.7 anti-pattern (bare-narrative-as-actionability) enforces; §9.6 gate 13 refuses to lock if commentary floats unattached. Four-layer enforcement.
4. **Cannot appear in research-audience translation track**: §5.9 hard-separations #4 carries "Forbidden in research-audience translation track per locked decision"; the §5.9 paragraph closes with "Guide #6 (Stage T) routes commentary to patient-audience track only" — correctly forecasts Stage T's discipline. Single-layer at Stage A (the second enforcement lives at Stage T, not Stage A).

The language discipline (subject-attribution required + permitted vs forbidden wording) is carried at §5.9 required-discipline #2-#4 with the §3.12 permitted-wording list verbatim ("I notice", "in my experience", "in retrospect", "I sometimes", "the pattern hints at / suggests-not-confirms / reads as", "worth attention", "I lean toward") and forbidden-wording list verbatim ("predicts", "forecasts", "will happen", "tomorrow", "X means Y", "this signals that...", any causal-claim or forecast-claim wording).

Per reviewer concern 4: all four hard separations + language discipline + patient-audience-only restriction faithfully implemented.

### L-ID citation discipline at construct level (§3 + §5.11 + §9.6 gates 1-2)

Strongly enforced (no issues found). §5.11 implements the limitations doc r3 §5 binding for `construct-*.md` faithfully ("MUST cite all seven L-IDs with explicit applicability-or-NA per limitation"). The §9.6 refuse-to-lock gate 1 enforces the all-seven rule; gate 2 enforces the NA-with-reason rule. The §3 hard rule ("Stage A MUST NOT cite an L-ID without a project-specific application or NA reason") is correctly framed. Per the spot-check in §5 findings above: both worked examples (K-stress-fatigue-monitoring + K-bout-recovery-signal) match limitations doc r3 §3 + map r3 §5 L-ID notes column exactly.

### PPV-with-base-rate in RESEARCH-REPORT §5.2 frame (§5.7 enforcement)

Strongly enforced. The frame "right N out of M when it fires" / "wrong M-N out of M when it fires" is required at §5.7 items 1-3 (PPV; base rate; plain-language combined frame). The K-bout-recovery-signal worked example correctly implements the frame with the ~2/year residual base rate citation. The §7.4 anti-pattern (bare-percentage actionability) enforces the frame at the anti-pattern level. **A2 above** is on the reverse cross-reference (§5.7 → §7.4) for binding-loop completion, not on the substantive enforcement.

Per reviewer concern 5: §5.7 implements the RESEARCH-REPORT §5.2 frame faithfully.

### §3.5 hard rule on missing inputs (§5.6 five refusal-to-proceed paths)

Strongly enforced. The five refusal paths each produce an `open_inputs` entry per §3.5 binding (per Invention 4 above). The four-field entry shape (what is missing; what is blocked; cheapest acquisition path; fallback tier) matches §3.5 binding verbatim plus the §6.5 spec's "fallback tier the artefact has therefore been capped at" requirement. The "open inputs do not block completion" framing per §3.8 is correctly carried at the §5.6 close ("Open inputs do not block completion per locked-plan §3.8. Exception: the five refusal-to-proceed paths above produce only the `open_inputs` entry; the construct artefact itself is not drafted when refusal-paths 1 or 2 fire, and is drafted at the fallback tier when refusal-paths 3 / 4 / 5 fire").

Per reviewer concern 8: each refusal path produces an `open_inputs` entry per §3.5.

### §3.11 follow-up suggestions N=1 scoping (§5.8)

Strongly enforced. §5.8 implements both tracks per §3.11 binding. The own-research track at Stage A is correctly the forward-validation HA shape per §5.5 (per §3.11 binding "Stage A row: own = forward-validation HA shape for tier promotion"). The external-research track correctly requires N=1 limit scoping per §3.11 binding; per-suggestion L-ID-citing (L1 / L3 / L4 per study type) is operationally implementable. The two worked-example sketches (K-stress-fatigue-monitoring + K-bout-recovery-signal) are concrete pre-reg shapes rather than vague directions.

Per reviewer concern 9: §5.8 carries the Stage A-specific shape per §3.11.

### §3.6 map conflict-resolution (§6.5 four halt-criteria)

Strongly enforced (per Invention 7 above). The four halt-criteria at the construct level match the guide #3 §6.1 + guide #4 §6.1 four-criteria pattern. The route-out instructions are concrete (stop drafting; do NOT edit map; produce only §5.6 entry; hand off; resume only after separate map-revision session). §7.13 anti-pattern (re-routing topics in-stage) enforces the rule against in-session map editing. The §8 interview seeds correctly surface map-vs-stage misalignment at the right interview-points.

Per reviewer concern 10: the four halt-criteria match guides #3 + #4 patterns.

### Worked examples — upstream-state accuracy check (reviewer concern 12)

Both worked examples handle the actual upstream state correctly:

**K-stress-fatigue-monitoring tier-1 cap check**: §4.1 worked example, §5.1 originating-topic-reference, §5.3 tier-1 claim, §5.4 NOT-DO refusals (mandatory minimum + construct-specific), §5.9 commentary, §5.11 L-ID block all correctly land at tier-1 only. The §5.2 evidence-layer paragraph correctly identifies tier-2 as blocked: "informative-pattern (tier-2) blocked by single-cluster evidence + direction-anomaly with Wiggers' canonical claim" (per map r3 §5 K-stress-fatigue-monitoring predictive-feasibility cell — HA-C3 v2 REJECTED + HA-C3p PARTIAL together cap at descriptive monitoring per map r3). **Faithful.**

**K-bout-recovery-signal tier-2 aspiration check**: §4.2 worked example, §5.1 originating-topic-reference, §5.3 tier-2 claim (conditional on §5.7 PPV computation), §5.4 NOT-DO refusals (tier-1+2), §5.5 forward-validation HA sketch (for tier-3 aspiration), §5.7 quality measures with PPV-with-base-rate against ~2/year residual crash base rate per RESEARCH-REPORT §5.2, §5.9 commentary, §5.11 L-ID block all correctly land at tier-2 aspiration with §3.10 PPV requirement. The §5.2 evidence-layer paragraph correctly identifies tier-3 as blocked by the §3.10 hard predictive gate. **Faithful.**

Both worked examples carry the upstream cluster-and-topic state accurately.

### Length and density

1759 lines is 3.5% over the upper bound (1700 target). The trajectory across the five guides (1008 → 1493 → 1939 → 1551 → 1759) shows the discipline-signal landed differentially: guide #3 (1939) was the longest; guides #4 (1551) and #5 (1759) sit in a comparable 1500-1800 range. The 59-line overrun in guide #5 vs the upper bound is operationally explainable as the §3.12 commentary discipline implementation (§5.9 + §6.4 + §7.7-§7.9 + §7.14 + §8.4 + §9.6 commentary-related gates) plus the §5.11 all-seven L-ID worked examples for both active constructs.

Realistic compression opportunities (in priority order):

- **§5.4 worked-example + mandatory-minimum overlap (~25 lines)**: the K-stress-fatigue-monitoring tier-1 §5.4 worked example carries the mandatory-minimum categories verbatim with K-stress-fatigue-monitoring-specific wording — could fold into the framework as an inline example rather than a separate worked block.
- **§5.11 worked-example length (~30-40 lines)**: the K-bout-recovery-signal §5.11 worked example doubles the surface of the K-stress-fatigue-monitoring worked example; a compact diff-from-K-stress-fatigue-monitoring (citing only L2 cross-phase pooling, L6 NA gevoelscore-not-in-primary-cell, L7 cross-phase coverage differences) would save ~30-40 lines.

Realistic total: ~50-80 lines (~3-4%) without losing operational content. Not blocking; A1 above recommends the compression for a future revision pass but does not require it.

### What would block a Stage A dry-run on K-stress-fatigue-monitoring at §11 step 8

Concretely: if a Stage A drafter loaded this guide and tried to translate the K-stress-fatigue-monitoring construct tomorrow at the §11 step 8 dry-run, the operational gaps they would hit are:

1. **§5.5 PPV-floor anchoring discipline (R1 above) is under-defined.** The drafter walking the §8.2 forward-validation interview for tier-3 aspiration (even if tier-3 aspiration is currently capped at tier-1 for K-stress-fatigue-monitoring per map r3, the drafter would still draft the §5.5 forward-validation pathway sketch per §5.5 mandatory-when condition "Tier-3 was wanted but not earned") would face element 5 (verdict criteria) and not know how to anchor the PPV floor. The §5.5 K-stress-fatigue-monitoring worked example happens to anchor at the uniform-three-bin null base rate (~0.33), which is operationally correct for this construct — but the discipline is implicit, not explicit. A drafter on a different construct would need the discipline made explicit. The fix is one-revision-cycle operational definition.
2. **§5.10 cross-reference to downgrade-mechanics (R2 above) is missing.** Less load-bearing at drafting time (§5.10 is fill-at-review-time), but the drafter would hit this at review absorption time (when the reviewer surfaces a tier downgrade and the drafter needs to know which conflict rule governs the downgrade-mechanics). The fix is one-revision-cycle cross-reference addition.

For K-stress-fatigue-monitoring specifically, both gaps are absorbable inline at the dry-run; for the general layer-wide skill, both should close before §11 step 7 skill build to encode the discipline at the skill level.

## 7. Required actions to absorb before LOCK

- **R1.** §5.5 PPV-floor anchoring discipline: add a seventh consideration to the six-element forward-validation HA shape ("PPV floor anchoring discipline"). Suggested wording: "**PPV floor anchoring discipline**. The pre-registered PPV floor is anchored at the relevant base rate by default (the null base rate that the prediction rule must exceed to demonstrate predictive value over chance); when the cross-op replication produced a tier-2 point estimate, the floor may instead anchor at or above the tier-2 point estimate (the prediction rule must demonstrate predictive value on unseen days that meets or exceeds the in-sample tier-2 evidence). In both cases, the floor cannot be set at or below the null base rate without justifying-the-tier-3-question-itself (the §3.10 gate would be backdoored by a trivially-passable floor). The K-stress-fatigue-monitoring worked example below anchors at the uniform-three-bin null base rate (~0.33); the K-bout-recovery-signal worked example anchors above the cross-op evidence point estimate (Cliff's δ = +0.120; +20.26 pp discrimination per map §5 + HA-C4c)." Update both worked-example sketches to make the anchoring explicit.

- **R2.** §5.10 cross-reference to downgrade-mechanics: add one-sentence cross-reference to §6.1 + §6.2 + §6.4. Suggested wording at §5.10: "Per §6 conflict rules: §6.1 governs tier-condition-unmet downgrades (typically tier-2 → tier-1 when cross-op evidence or PPV-with-base-rate fails); §6.2 governs forward-validation-HA-REJECTED downgrades (tier-3 → tier-2 with §5.5 forward-validation HA shape addendum); §6.4 governs commentary-vs-evidence conflicts (no tier change; commentary revised per §3.12 binding). The §5.10 review-time fill records the per-concern downgrade with the §6 conflict-rule reference." This closes the §5.10 review-time-fill operational loop.

## 8. Recommended actions to absorb before LOCK (optional)

- **A1.** Length compression for a future revision pass (not blocking). Two candidates in priority order: §5.4 worked-example could fold into the framework (~25 lines); §5.11 K-bout-recovery-signal worked example could compact to diff-from-K-stress-fatigue-monitoring (~30-40 lines). Realistic total: ~50-80 lines (~3-4%) without losing operational content.

- **A2.** §5.7 → §7.4 binding-loop completion: add one-sentence reverse cross-reference from §5.7 to §7.4. Suggested wording: "**§7.4 anti-pattern enforces.** Bare-percentage actionability without the combined plain-language frame is forbidden per §7.4; §5.7 items 1-3 are the construct-level operationalisation of the §7.4 prohibition." Close the binding loop at the §5.7 level.

- **A3.** §11 lock log: split the ~50+ line single paragraph into two-or-three short paragraphs (one for inventions; one for §6.5 ambiguity interpretations; one for the §11 step 7 skill dependency note + the §3 + §5.11 worked-example anchor). Same shape as A4 in guide #4 r1 review.

## 9. Confirmed-good

The following elements of the draft are sound and need no revision:

- §1 purpose framing + alternatives-considered paragraph + skill-precondition note + seven-bullet "What Stage A does NOT do" list (including the §3.12 boundary at bullet 5).
- §2 twelve-input list (the §6.5 spec's three + the synthesis-structure map + limitations doc + forward-validation HAs + RESEARCH-REPORT §5.2 + §3.10 hard predictive gate as input #9 + §3.12 commentary-eligibility + lived-experience priors + CONVENTIONS).
- §3 output spec + flat-no-per-construct-subfolder convention + L-ID citation discipline at output level + two hard rules + worked-example anchors for both active constructs.
- §4.1 tier-1 monitoring sub-section + claim shape + required evidence + §3.10 PPV-exempt status + permitted wording + forbidden wording + §3.12 commentary eligibility + K-stress-fatigue-monitoring worked example.
- §4.2 tier-2 informative-pattern sub-section + claim shape + required evidence (including cross-op replication discipline) + §3.10 PPV required + permitted wording + forbidden wording + §3.12 commentary eligibility + K-bout-recovery-signal worked example.
- §4.3 tier-3 predictive-use sub-section + claim shape + required evidence (forward-validation HA + lead time + reliability) + §3.10 status + permitted wording + forbidden wording + §3.12 NOT eligible + "none active in map r3" framing.
- §4.4 tier mapping summary table + "discipline cascade" closing paragraph.
- §5.1 mechanical header (construct ID + name + topics feeding + per-topic positioning + tier aspiration + §3.12 commentary-eligibility + declared-date + lock-version).
- §5.2 three-paragraph evidence-layer structure + "tier earned at this Stage A time" closing line.
- §5.3 tier claim + permitted-wording-for-subject list.
- §5.4 NOT-DO refusals with mandatory-minimum-per-tier + construct-specific additions + K-stress-fatigue-monitoring worked example (modulo A1 length).
- §5.5 six-element forward-validation HA shape + mandatory-when conditions + not-aspired record-with-rationale framing + K-stress-fatigue-monitoring + K-bout-recovery-signal worked-example sketches (modulo R1 PPV-floor anchoring discipline).
- §5.6 four-field entry shape + five refusal-to-proceed paths + open-inputs-do-not-block-completion framing + refusal-path-1/2 vs refusal-path-3/4/5 distinction.
- §5.7 three required measures at tier-2+ (PPV; base rate; plain-language combined frame) + six optional measures with tier-3-required lead-time-+-reliability + §3.10 conflict rule + HA-test-level vs actionability-layer two-direction discipline + K-bout-recovery-signal worked example (modulo A2 binding-loop completion).
- §5.8 own + external two-track structure + N=1 scoping discipline + L-ID-citing per study type + two worked-example sketches for both active constructs.
- §5.9 commentary section with four required disciplines + five hard separations + K-stress-fatigue-monitoring + K-bout-recovery-signal worked examples + tier-3 boundary correctly closed.
- §5.10 fill-at-review-time interpretation (modulo R2 cross-reference miss).
- §5.11 all-seven L-ID block with applies-or-NA + K-stress-fatigue-monitoring + K-bout-recovery-signal worked examples (both spot-checked against limitations doc r3 §3 + map r3 §5 L-ID notes column).
- §5.12 cross-references (all spot-checks pass).
- §6.1 + §6.2 + §6.3 cite-and-implement of §6.5 spec conflict rules.
- §6.2 "tier-3 inertia prohibition" at maintenance level (per §3.10 binding at maintenance, not just promotion).
- §6.4 commentary-vs-forward-validation conflict rule + precursor-routing-to-§5.8 (per Invention 6 + reviewer concern 3 check).
- §6.5 four halt-criteria + route-out instructions (parallel guide #3 §6.1 + guide #4 §6.1).
- §7.1-§7.14 fourteen anti-patterns including the nine extensions beyond §6.5 spec (including the §7.7-§7.9 + §7.14 commentary anti-pattern cluster).
- §8.1-§8.4 three required seeds + one optional commentary-shape interview seed.
- §9.1-§9.8 eight-phase agent-instruction outline including the §9.6 fifteen-item refuse-to-lock gate.
- §10 cross-references (all spot-checks pass; all referenced methodology files verified at named paths).
- §11 lock log (per A3 on scannability).

The two active constructs in the map r3 (K-stress-fatigue-monitoring tier-1; K-bout-recovery-signal tier-2) are mostly well-served by this guide: a Stage A drafter loading the guide tomorrow would have an operationally clear procedure for each, modulo the two findings above (R1 + R2 + A1-A3).

---

**Reviewer recommendation**: absorb R1 + R2 (one-revision-cycle fixes); A1-A3 are recommended for clarity/density. After R1 + R2 absorption, the guide can LOCK without a second fresh-session review per the established Option-γ pattern matching plan / limitations / map / Stage D guide / Stage I guide / Stage S₁ guide / Stage S₂ guide closures. The §11 step 6.6 (guide #6 `translation_to_audience.md`) drafting is unblocked by the LOCK on guide #5; the §11 step 7 skill build is unblocked once all six guides LOCK; the §11 step 8 dry-run on K-stress-fatigue-monitoring or K-bout-recovery-signal is unblocked once the skill build lands. The hard predictive gate from §3.10 was preserved without weakening; the §3.12 commentary discipline was implemented faithfully with all four hard separations carried at multiple enforcement layers.
