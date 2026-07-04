# Methodology review — internal_synthesis.md (r1, 2026-06-24)

**Reviewer mode**: fresh-session peer review. Reviewer is independent of the drafting session. Fresh session — no exposure to the drafting context; doc-only knowledge.
**Target**: [`docs/research/methodology/internal_synthesis.md`](../methodology/internal_synthesis.md) (r1, 2026-06-24)
**Review date**: 2026-06-24
**Standards applied**: [CONVENTIONS](../CONVENTIONS.md) §1, §2.1, §2.2, §3 (esp. §3.4), §4; [plan](../methodology/_plan_results_analysis_layer.md) r5 §6.3 spec + §3.5 + §3.6 + §3.7 + §3.8 + §3.9 + §3.10 + §3.11 + §3.12 + §9; [limitations doc](../methodology/research_line_limitations.md) r3; [synthesis map](../methodology/synthesis_structure_map.md) r3; [Stage D guide](../methodology/descriptive_precondition_audit.md) r2 LOCKED; [Stage I guide](../methodology/verdict_to_inference.md) r2 LOCKED; [seed notes](../methodology/_synthesis_seed_notes_2026-06-23.md); [stocktake](../methodology/_descriptive_stocktake_2026-06-23.md); four ready HA result.md files (HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo); Daza 2018 / CENT 2015 / SCRIBE 2016 / Natesan 2023.

---

## 1. Overall verdict

**REVISION RECOMMENDED.** The draft is structurally faithful to plan §6.3, implements all 9 declared sections plus the §3.5-mandated `open_inputs` block, and the seven inventions beyond the spec are — with two substantive exceptions — methodologically sound and operationally implementable. The §6.1 four halt-criteria for the §3.6 conflict-resolution rule are concrete and well-grounded; the §5.5 cascade-arrow handling rule correctly routes the C-bout-framework verdict into C-bout-substance as caveat-class precondition (matching the map r3 §3 row's binding language); the §6.3 PROVISIONAL non-compounding rule prevents the perverse incentive it names; the §7 anti-pattern list (11 items) is distinct from upstream plan §9, guide #1, and guide #2 anti-patterns. The §9 phased agent-instruction outline is concrete enough that the §11 step 7 skill build will know what to encode. The §4.5 L-ID citation discipline correctly translates limitations doc r3 §5 row for `cluster-*.md` into binding form — minus one factual concern noted below.

Four findings drive the REVISION RECOMMENDED verdict rather than ACCEPT. Two are required (R1, R2); two are recommended (A1, A2). None blocks future map-revision work or the §11 step 7 skill build; all four are one-revision-cycle fixes. Plus a noted-but-not-blocking length concern (A3) and a sibling-naming check (A4).

- **R1.** §5.2's "Possible PARTIALLY CONCORDANT reading" worked example for C-stress-fatigue-shape mischaracterises HA-C3 v2's verdict as "monotone-inverse" and frames the HA-C3 v2 vs HA-C3p disagreement as "monotone-inverse vs inverted-U." Per HA-C3 v2 r2 result.md §3 (S = m₃ − 2·m₂ + m₁ = −0.740, p = 0.0002, sign-flip into significantly concave) + HA-C3p result.md §6 4-cell consolidation matrix (the cell that fires reads "BOTH detect CONCAVE not CONVEX shape" and both detect inverted-U / threshold pattern peaking at stress 30-40), the two HAs **agree** on the inverse-non-monotone (concave, peaked) shape — they do not disagree on it. A Stage S₁ drafter loading this guide and reading the §5.2 worked example would land on PARTIALLY CONCORDANT or even CONFLICT when the actual evidence points closer to CONCORDANT-on-the-non-Wiggers-direction. The §5.2 worked example needs rewriting to reflect the actual result.md substance; the §5.3 alternative CONFLICT reading should also be rewritten or removed.

- **R2.** §3 L-ID worked example for `cluster-bout-substance.md` says cross-phase pooling within HA-C4c itself triggers the L2-era-strata-mismatch citation "at the cluster level even though there is only one constituent HA." The limitations doc r3 §5 row for `cluster-*.md` reads: "Cite every limitation that touches any cluster member; **also cite L2 if cluster members are from different era strata.**" The "if cluster members are from different era strata" clause refers to **cluster members** (plural HAs), not within-member sub-strata. HA-C4c carries its cross-phase pooling caveat at the per-HA Stage I level (via L2 in its own §4.5); the cluster-level L2-era-strata-mismatch citation is intended for the case where, e.g., one cluster member runs unmedicated-only and another runs medicated-only. The draft's extension of the rule to within-member sub-strata is a plausible interpretation but goes beyond the binding's literal wording. The §3 worked example should either (a) re-derive the C-bout-substance L-ID set without invoking the L2 cluster-level addition, or (b) flag this as an extension of the limitations doc binding and route the extension back to limitations doc §5 for an explicit lock-version bump. The same concern applies to §4.5 5b's "L2-era-strata-mismatch cluster-level binding where it triggers" language and §9.6 gate 2.

Recommended:

- **A1.** §5.6 trivial-ORTHOGONAL handling for single-member clusters. The draft uses ORTHOGONAL as the default label for single-member clusters, with the rationale at §5.4 that ORTHOGONAL is "for HAs that share a construct but address distinct facets." Strictly read, a single-member cluster does not have HAs that address distinct facets — it has one HA that is the cluster. Adopting trivial-ORTHOGONAL is a reasonable workaround (it avoids inventing a fifth label per §7.10, and the label's semantics of "no cross-HA inference" do hold for the single-member case), but the §5.6 explanation should explicitly acknowledge the semantic stretch and justify why this is preferable to a fifth label like NA-SINGLE-MEMBER or COLLAPSES-TO-MEMBER-CLAIM. As written, §5.4 forbids using ORTHOGONAL for "HAs that address different constructs entirely" and the single-member trivial case sits adjacent to that forbidden zone — a one-paragraph clarification would close the boundary. This is structurally important because two of the three currently-active clusters (C-bout-framework, C-bout-substance) are single-member; the trivial-ORTHOGONAL framing will be heavily used early in the rollout.

- **A2.** §5.6 + §3 thin-S₁ vs skipped-with-stub choice for single-member clusters. The draft says the choice between thin-S₁ and skip-with-stub "is the user's at the moment the cluster becomes eligible — both options are valid." But §5.6 also says "The thin-S₁ option is preferred when the cluster carries cascade-arrow language (because the cascade-precondition handling needs an artefact to live in)" — which for C-bout-substance makes thin-S₁ effectively forced (since it is the only cascade-downstream cluster currently). The draft does not enumerate which of the three active clusters falls in which path:
  - C-stress-fatigue-shape (2 members) → standard S₁ (not single-member).
  - C-bout-framework (single member, no cascade-arrow upstream) → user choice (thin-S₁ or skip-with-stub).
  - C-bout-substance (single member, cascade-arrow downstream from C-bout-framework) → thin-S₁ effectively forced.

  This per-cluster determination would help a Stage S₁ drafter know what they are looking at for each of the three active clusters before they start.

## 2. Four-input bar findings (CONVENTIONS §2.2)

This MD is producer-mode infrastructure (per §3 of the target, per plan §4 row "Guide MDs (6×)") rather than a methodology MD locking a substantive analytical choice; the four-input bar applies in lighter form. Two of the four inputs apply directly; two apply indirectly.

| Input | Status | Reasoning |
|---|---|---|
| 1. Best-practices standards | PASS | The cluster-coherence-call mapping shape (four exhaustive labels; default-to-CONFLICT-on-ambiguity; no auto-resolution discipline; effect-size-magnitude consistency check at CONCORDANT) traces to N-of-1 multi-test synthesis standards (Daza 2018 multi-test combination at the within-subject level; CENT items 21+22; Natesan 2023 defensible cluster-level coherence bar; SCRIBE participant-as-researcher transparency). The §2 input list cites all four with one-sentence operational role; Daza is correctly named primary for Stage S₁'s multi-test discipline. |
| 2. Established literature | PASS | The §1 "alternatives considered" paragraph cites two rejected paths (addendum-as-synthesis; Stage S₂ only with no S₁) with the project-internal precedent (guides #1 and #2 used the same rejection reasoning for their respective upstream stages). The §2 input list, §4.5 5b worked examples, and §4.8 external-research-N=1-scoping references draw on the four literature methodology anchors. This is stronger than guide #1's r1 framing (which absorbed the alternatives paragraph at r2) and matches guide #2's r1 strength. |
| 3. Tradeoff vision | PASS | The "alternatives considered" paragraph satisfies CONVENTIONS §2.2 item 3 explicitly. Specific judgment-call calls visible in the body: (a) ORTHOGONAL-as-trivial-default for single-member clusters per §5.6 (vs introducing a fifth label per §7.10 — sound tradeoff per A1 caveat above); (b) default-to-CONFLICT on PARTIALLY-CONCORDANT-vs-CONFLICT ambiguity per §4.4 hard rule (vs default-to-PARTIALLY-CONCORDANT — the preserve-the-conflict default is correctly chosen); (c) cascade-arrow as caveat-class precondition rather than co-equal verdict per §5.5 (the map's r1 → r2 rationale is cited correctly). |
| 4. Research limitations + objectives | PASS | The §5 worked examples draw from the three active clusters in the map's r3 (C-stress-fatigue-shape, C-bout-framework, C-bout-substance); the §6.1 four halt-criteria + §6.3 PROVISIONAL inheritance handle the corpus's known difficulties (Stratum 4 unmedicated × train default scope; cross-phase pooling on HA-C4c; cascade-arrow on C-bout-substance); the §4.5 L-ID citation discipline matches the synthesis-structure map's §3 per-cluster L-IDs columns (modulo R2). |

Overall: 4 PASS. The four-input compliance is strong — the trajectory of guide #1 r1 (2 PASS, 2 PARTIAL on alternatives + literature) → guide #2 r1 (4 PASS) → guide #3 r1 (4 PASS) shows the discipline propagating session-to-session. The drafter's self-report of having read guide #1 and guide #2 reviews before drafting is borne out.

## 3. Faithfulness to §6.3 spec

§6.3 has nine listed elements (purpose, inputs, output, 10-section outline, cluster pre-declaration rule, checklist sketch, conflict rules, anti-patterns, interview seeds, agent-instruction outline). Mapping:

| §6.3 element | Implementation | Faithfulness |
|---|---|---|
| Purpose | §1 (purpose + where it sits + what it does not do) | **Faithful with extension.** The extension is the "What Stage S₁ does NOT do" six-bullet list (re-test verdicts / predictive claims / commentary / new caveats / re-route HAs / multi-cluster-per-session). All six are operationally important boundary statements. Sound. The "Alternatives considered" paragraph satisfies CONVENTIONS §2.2 item 3 explicitly. |
| Inputs | §2 (eight numbered inputs) | **Faithful with extension.** §6.3 names three inputs (constituent HA interpretations; methodology MDs; addendum entries). §2 expands to eight: adds the synthesis-structure map's §3 row (binding for cluster constellation per §6.1); cascade-arrow upstream cluster's `cluster-*.md` (binding precondition for cascade-downstream clusters); seed notes (advisory only — correctly framed); Stage D audit verdict-trust call chain (via member interpretation §1 headers); CONVENTIONS sections (esp. §3.4 crash-drop sensitivity, anchoring §5.7 invention); literature methodology anchors (four PDFs). The addition of the synthesis-structure map as binding input is the right operationalisation of the §3.6 layer rule. The exclusion of the addendum entries from the input list — the §6.3 spec named them as input — is a substantive omission; the draft's §1 alternatives-considered paragraph implies the addendum chain is a competing approach rejected in favour of cluster-bounded synthesis, but the spec named the addendum entries as *inputs* not as alternatives. The omission is consistent with the producer/reviewer mode discipline (the addendum is a producer-mode artefact; the cluster synthesis is reviewer-mode-with-authorization) but should be acknowledged explicitly. **Minor.** |
| Output | §3 (path + naming + flat-no-subfolder + mode + L-ID citation discipline) | **Faithful with extension.** §6.3 specifies `analyses/synthesis/cluster-XXX.md` (by-cluster, flat naming per plan §5). §3 specifies the flat-no-per-cluster-subfolder convention explicitly and justifies the difference from Stage D's per-HA folder. The thin-S₁ vs skipped-with-stub choice for single-member clusters is added explicitly (per A2). The §3 L-ID citation discipline closing block is the right place to bind limitations doc r3 §5 row into the output spec (modulo R2 concern). |
| Section outline | §4 (10 sub-sections, §4.1–§4.10) | **Faithful.** §6.3 names 10 sections; §4 implements all 10 with the §4.5 sub-blocks (5a caveats / 5b L-ID citation / 5c cascade-precondition) and §4.7 sub-blocks (7a what licenses / 7b what does NOT license). The §4.9 `open_inputs` block was named as item 8 in the §6.3 spec; the draft's §4.9 routes it to position 9, with §4.8 follow-up suggestions at position 8 — the swap is correct per plan §3.5 (open_inputs first-class) + §3.11 (follow-up section), and the relative positions match guide #2's §4.8 / §4.9 swap. |
| Cluster pre-declaration rule | §4.2 + §6.1 + §8.1 + §9.4 | **Faithful with extension.** §6.3 says "a cluster must be pre-declared by constituent HAs before any HA's `interpretation.md` is read for synthesis." The draft routes this via §4.2 (the cite-the-map-row paragraph with date + lock-version), §6.1 (halt-and-route if in-stage work reveals re-clustering need), §8.1 (interview seed surfacing map-vs-stage misalignment), and §9.4 (skill walks §8.1 first). The four-touchpoint enforcement is operationally robust. The §4.2 hard rule "does NOT re-derive the constellation" is the right discipline. |
| Checklist | Folded into §4 sub-sections + §9.6 refuse-to-lock gate | **Faithful.** The §6.3 checklist's five bullets are implemented across the §4 sub-sections + §9.6 — all-HAs-have-interpretation (§9.2 gate + refusal-path-1), cluster-pre-declared-and-signed-off (§4.2 + §6.1 + §8.1), coherence-call-supported-by-per-HA-rows (§4.3 row format + §4.4 rationale-from-rows), CONFLICT-preserved-not-resolved (§4.6 + §7.2 + §7.11), joint-claim-no-wider-than-narrowest-member (§4.7a width discipline). This is the right place to fold them; a separate §-checklist section would be redundant. |
| Conflict rules | §6 (4 rules) | **Faithful with extension.** §6.3 names 2 conflict rules (HAs disagree → CONFLICT; one HA effect-size dominant → does not dominate). §6 implements both (§6.2 cascade-upstream-unlocked = refusal; §6.3 PROVISIONAL inheritance covers the dominance question implicitly via the no-silent-degradation rule) and adds two more (§6.1 map-change-needed = the §3.6 layer-rule operationalisation; §6.4 cluster vs lived-experience prior reconciliation extending guide #2 §4.6 to the cluster level). Both additions sound — see §4 below. |
| Anti-patterns | §7 (11 anti-patterns) | **Faithful with extension.** §6.3 names 3 anti-patterns (cherry-picking which HAs count; "3 of 5 HAs agree therefore established"; splitting the difference). §7 implements all 3 (§7.2 = splitting CONFLICT; §7.4-§7.5 + §6.1 cover cherry-picking; §6.3 spec's "3 of 5 HAs agree" routes through the §1 width-discipline and the §4.7a "no wider than narrowest" rule with the same-signal-multi-take vs independent-operationalisations distinction from the map row). The 8 additions are all distinct and sound — see §4 below. |
| Interview seeds | §8 (3 required + 1 optional) | **Faithful with extension.** §6.3 names 3 seeds (which HAs belong + shared construct; operationalisation overlap independence; divergence informativeness). §8 implements all 3 (§8.1 = first; §8.2 = third combined with second; §8.3 = joint-claim narrowing as additional seed driving §4.7a/b; §8.4 optional cluster-trust confirmation). The optional fourth parallels guide #1's §8.4 and guide #2's §8.4 confirmation-seed pattern. Sound. |
| Agent-instruction outline | §9 (8 phases) | **Faithful with extension.** §6.3 names 5 bullets (Load / Refuse / Walk / Produce / Recommend). §9 expands to 8 phases (Load / Gate / Extract / Interview / Produce / Refuse-to-lock-gate / Review-handoff / Acceptance + drift-trigger registration). The Acceptance + drift-trigger phase implements §3.7 + §3.8 (drift triggers, user-acceptance-as-lock); the Refuse-to-lock gate enumerates seven structural checks. Both extensions correct because the relevant plan rules post-date §6.3's sketch. The cascade-arrow-aware fifth drift trigger for cascade-downstream clusters is a sound and necessary extension. |

No §6.3 element is missing or substantively altered. Spec faithfulness is high. The §6.3 spec ambiguities the agent's self-report flags (operationalisation-overlap-note source; open-conflicts-preserved operationalisation) are resolved cleanly: the overlap-note is read verbatim from the map's §3 row cell; the open-conflicts-preserved discipline is operationalised through §4.6 paragraph-per-conflict + §4.4 default-to-CONFLICT + §7.2 anti-pattern as a three-part structural defence. Both resolutions sound.

## 4. The seven inventions beyond §6.3

### Invention 1 — §5.5 cascade-arrow handling rule

**Sound.** The C-bout-framework → C-bout-substance cascade is the canonical cascade in the map r3, and §5.5 routes it correctly. The map r3 §3 row for C-bout-substance reads: "S₁ on this cluster MUST consume the C-bout-framework verdict as caveat-class precondition (per cascade arrow above) before reading the C-bout-substance verdict on its own merits." §5.5 implements this exactly: the upstream cluster's coherence call enters §4.5 (caveats) and the §5.5 cascade-handling rule as precondition that bounds the downstream's substantive claim, **NOT** §4.4 (coherence call) as a third "vote." The four-band routing (CONCORDANT / PARTIALLY CONCORDANT / CONFLICT / ORTHOGONAL upstream → respective downstream narrowing) is operationally complete. The worked example for C-bout-substance reading C-bout-framework's trivial-ORTHOGONAL is concrete and accurate against HA11-bout-redo result.md (+20.26 pp, bars 1+2 PASS, bar 3 FAIL at p=0.2609).

The §7.3 anti-pattern ("Treating cascade-arrow caveat-class precondition as co-equal verdict") is the right defence and correctly cites the map r1 → r2 split rationale (the conflation of framework-validity with substantive verdicts the map split was designed to prevent).

### Invention 2 — §5.6 trivial-ORTHOGONAL for single-member clusters

**Sound with one operational concern (A1 above).** This is a structural workaround for the map's single-member cluster shape and is methodologically the cleaner choice between (a) inventing a fifth label (forbidden by §7.10), (b) skipping S₁ via `stage_skipped.md` stub (permitted but loses the cluster-level L-ID block and cascade-precondition surface), or (c) declaring the single-member case label-undefined (creates a hole in §4.4). The trivial-ORTHOGONAL approach uses the existing four-label set, preserves the cluster-level artefact for L-ID and cascade-precondition handling, and the "joint claim collapses to single member's licensed claim" rule is operationally trivial.

The semantic stretch (per A1) is that §5.4 defines ORTHOGONAL as "HAs that share a construct but address distinct facets" — a single-member cluster does not have HAs (plural). A one-paragraph clarification in §5.6 acknowledging the stretch and naming why trivial-ORTHOGONAL is preferable to the alternatives would close the boundary cleanly.

The §3 thin-S₁-vs-skipped-with-stub choice for single-member clusters (per A2) is the right framing but should enumerate which of the three active clusters falls in which path to be operationally complete.

### Invention 3 — §5.7 cluster-level crash-drop sensitivity discipline

**Sound.** The cluster-level operationalisation of CONVENTIONS §3.4 (crash-drop sensitivity row on every Layer 4+ correlation) is the correct extension. The rule cites the |Δ| > 0.10 threshold from CONVENTIONS §3.4 verbatim and routes the cluster-level surfacing via §4.5 5a (caveats) + §4.6 (open conflicts where the cluster-coherence-direction changes). The "NOT averaged away" framing matches CONVENTIONS §3.4's "the contrast itself is informative" rule. The closing sentence ("This rule operationalises CONVENTIONS §3.4 at the cluster level; it does NOT introduce a new crash-drop discipline beyond what the convention already binds") is the right framing — the discipline is inherited, not invented.

The worked example for C-bout-substance is hypothetical (it does not claim HA-C4c's result.md actually reports |Δ| > 0.10), which is the right way to demonstrate the rule without overclaiming what the data shows.

### Invention 4 — §6.1 four halt-criteria for the §3.6 conflict-resolution rule

**Sound.** The plan §3.6 conflict-resolution rule names the discipline ("when per-cluster S₁ work reveals that the §3.6 layer-wide map needs to change, Stage S₁ halts and routes to a separate producer-mode map-revision session"). The four concrete halt-criteria (member HA's interpretation places HA on different construct; cluster's coherence call requires evidence from non-cluster HA; operationalisation-overlap-note cell inadequate; cascade-arrow language wrong) are operationally implementable. The route-out instructions (stop drafting mid-session, produce only §4.9 open_inputs entry, hand off, resume only after separate map-revision session) match plan §3.6's "halt-and-route" discipline verbatim.

The four halt-criteria are exhaustive for the cases the §3.6 rule was designed for: (1) and (2) cover the HA-belongs-in-different-cluster + new-cluster-should-exist cases the spec names; (3) is the operationalisation-overlap-note cell's correctness (which is what makes the cluster's evidence-strength rationale binding); (4) is the cascade-arrow language's correctness (which is what makes the cascade-downstream coherence call sound). The "topic boundary wrong" case the §3.6 spec names is not in the four halt-criteria — it would be a Stage S₂ halt rather than Stage S₁, which is consistent with the draft's §1 cluster-bounded-scope discipline. Sound omission.

### Invention 5 — §6.3 cluster-trust PROVISIONAL inheritance + multi-PROVISIONAL non-compounding

**Sound.** The inheritance rule (PROVISIONAL member narrows cluster's joint claim by at most one tier per plan §3.5) is the right cross-reference — it parallels guide #2 §6.2's PROVISIONAL-narrowing rule exactly. The non-compounding rule is well-motivated: capping multi-PROVISIONAL narrowing at one tier prevents the perverse incentive to push a member's audit to REQUIRES-DESCRIPTIVE-WORK rather than PROVISIONAL to avoid the multi-PROVISIONAL inflation. The "narrowing discipline is structural (PROVISIONAL presence → one-tier narrower joint claim), not compounding" framing is operationally clear.

No new gaps created: a downstream Stage S₂ reading a cluster with multi-PROVISIONAL members still sees the one-tier narrowing, which is sufficient signal that the cluster's substantive claim is bounded. The §11 lock log + the §4.4 rationale paragraph both record the PROVISIONAL chain explicitly, so the inheritance trace is auditable.

### Invention 6 — §6.4 cluster vs lived-experience prior reconciliation

**Sound.** Per the §6.3 spec, lived-experience prior reconciliation lives at the per-HA Stage I level (guide #2 §4.6). The cluster-level extension is the case where a cluster-level tension surfaces that is not inheritable from any individual member's Stage I §4.6 — e.g., the cluster's coherence call surfaces a structural prior tension that no individual member's §4.6 carries. The draft routes this through §4.6 (open conflicts) + §4.8 (own-research follow-up), explicitly distinguishing it from §3.12 subject-narrative commentary (which is forbidden at Stage S₁ per §1 + §7.8). The structured prior-vs-verdict reconciliation discipline carries through from guide #2; the cluster-level version is methodologically consistent.

The draft also inherits guide #2 §4.6's "agreement does not strengthen the licensed claim" rule implicitly through the §4.7a width discipline ("joint claim is no wider than the narrowest member's licensed claim allows, unless cross-operationalisation replication explicitly warrants the broader claim") — though this is not made explicit. The implicit inheritance is acceptable; making it explicit in §6.4 would tighten the discipline.

### Invention 7 — §9.6 phased refuse-to-lock gate

**Sound.** The seven structural checks (L-ID block missing entries the map row lists; L2-era-strata-mismatch citation missing when triggered; cascade-precondition sub-paragraph missing on cascade-downstream cluster; §4.4 carries invented label; §4.6 reads CONFLICT/PARTIALLY CONCORDANT without preservation discipline; §4.7b missing one of four predictable overclaim shapes; §4.8 external-research suggestion without N=1-scoping; §4.7a joint claim width exceeds discipline; §4.3-§4.7 anti-pattern violations) are the right structural gates. Each maps to a §4 sub-section requirement, so the gate is implementable as a skill-level check rather than as judgment.

The last check ("§4.3 / §4.4 / §4.5 / §4.6 / §4.7 contain anti-pattern violations per §7") is text-pattern detection and harder to enforce at the skill level than the first seven; the same concern guide #2's review flagged for the §9.6 check 5 applies here. Not blocking; a §9.6-level refinement could specify pattern-detection heuristics (presence of "predicts", "forecasts", "X means Y", first-person narrative, "splitting the difference" wording in §4.4-§4.7 triggers the gate).

## 5. Per-section findings

### §1 Purpose

Sound. The block-quote framing ("A cluster of related HA verdicts is not a chorus. Stage S₁ produces a single coherence call, drawn from a fixed label set, that says how the cluster's per-HA interpretations sit against each other at the construct level — preserving conflicts where they exist, refusing to average them into a 'middle' reading") matches plan §6.3's opening framing. The six-bullet "What Stage S₁ does NOT do" is helpful scope-clarification — particularly the §3.10 / §3.12 boundaries and the no-re-routing rule which §6.1 + §7.1 enforce structurally. The "Alternatives considered" paragraph satisfies CONVENTIONS §2.2 item 3 explicitly. The skill-precondition note matches guide #1 + guide #2 framing and is operationally important.

### §2 Inputs

Sound (modulo the addendum-omission noted in §3 above). The eight numbered inputs cover the §6.3 spec's three plus the layer-level binding additions (synthesis-structure map; cascade-arrow upstream cluster's `cluster-*.md` where applicable; seed notes as advisory only; Stage D verdict-trust call chain; CONVENTIONS; literature methodology anchors). The closing "what the interpretation does NOT load" paragraph is the right negative-space discipline. The §2 input #4 framing of cascade-arrow upstream cluster's `cluster-*.md` as binding precondition is operationally correct (matches §6.2 refusal-path-3 + §9.2 gate behaviour).

The §2 input #5 framing of seed notes as "advisory only" is correctly aligned with the seed-notes file's own status header AND the map r3 §3 note's relocation rationale. §7.6 anti-pattern enforces the rule that the sketches are not constraints on the coherence call. Pass.

### §3 Output

Sound on the artefact path + flat naming convention + mode + L-ID citation discipline (modulo R2 above on the L2-era-strata-mismatch worked example for C-bout-substance).

The justification for the flat naming convention ("one file per cluster at the top level of `analyses/synthesis/` — no per-cluster subfolder") matches the map r3 §2 declared output path and the locked plan §5 output-structure tree. The thin-S₁ vs skipped-with-stub choice for single-member clusters is named explicitly (per A2 above), with the choice routed to user decision at §11 lock-log time. The cluster-name-from-the-map-row-exact-ID rule is operationally clear — but note that the map r3's cluster IDs include the `C-` prefix (`C-stress-fatigue-shape`, `C-bout-framework`, `C-bout-substance`), while the draft's §3 examples drop the prefix (`cluster-stress-fatigue-shape.md` etc.). The draft follows the plan §5 output tree convention (which also drops the prefix), not the map r3 ID convention. This is consistent with the plan but inconsistent with the map; flagging as A4 below.

The "L-ID citation discipline at the output level" closing block correctly routes the limitations doc r3 §5 row binding into the output spec, with the binding rule "every limitation that touches any cluster member" + "also cite L2 if cluster members are from different era strata." But the §3 worked example for C-bout-substance interprets "different era strata" as within-member sub-strata (per R2) — needs revision.

The hard rules at §3 are correctly framed (no empty §4.5 L-ID block; no NA citation without one-sentence project-specific reason) and are enforced at §9.6 gates 1-2.

### §4 Section outline for the produced cluster-XXX.md

Sound. The ten sub-sections cover §6.3's ten-section outline with the §4.5 sub-blocks and §4.7 sub-blocks structurally clear.

**§4.1 (cluster name + constituent HAs)**: sound; the verbatim-copy rule (cluster ID, member HA list, verdicts with qualifiers per guide #2 §5.5, Stage D verdict-trust calls, shared construct, operationalisation-overlap-note, cascade-arrow language) is the right header discipline.

**§4.2 (pre-declared constellation)**: sound; the template paragraph correctly cites the map row's declared-date and lock-version verbatim, the hard rule that it "does NOT re-derive the constellation" prevents in-stage re-clustering, and the cascade-arrow sub-paragraph extension for cascade-downstream clusters is correctly framed.

**§4.3 (per-HA verdict + interpretation row)**: sound; the row format is operationally clear and the worked example for C-stress-fatigue-shape (2-member cluster) correctly enumerates the seven row fields. The "for clusters with cascade-arrow language, §4.3 contains ONLY the downstream cluster's members — the upstream verdict propagates via §4.5 + §5.5, NOT as a co-equal row" rule is the right boundary enforcement (matches §7.3 anti-pattern).

**§4.4 (coherence call)**: sound on the four-label exhaustiveness rule and the default-to-CONFLICT-on-ambiguity hard rule. §5 mapping rules are the operational guidance.

**§4.5 (cluster-level caveats narrowing the joint claim, with L-ID citation block)**: sound on the three sub-block structure (5a caveats from member interpretations; 5b L-ID citation block; 5c cascade-precondition sub-paragraph where applicable). The "Stage S₁ may synthesise caveats but does NOT add caveats the member interpretations did not carry" rule is the right discipline. The "If Stage S₁ identifies a cluster-level caveat that no member interpretation carried, §7.4 anti-pattern routing applies" is the right routing back to upstream Stage I gap. The §4.5 5b L-ID citation block is the layer's commensurability guarantee at the cluster level; the operationalisation is correct minus R2's concern on the L2-era-strata-mismatch worked example.

The §4.5 5c cascade-precondition sub-paragraph template is operationally clear and the C-bout-substance worked example correctly reads the C-bout-framework upstream as caveat-class precondition.

**§4.6 (open conflicts preserved with both readings)**: sound on the no-auto-resolution rule and the paragraph-per-HA-conflict structure. The resolution paths (tie-breaker HA; descriptive deep-dive; Stage S₂ external-literature positioning as forward pointer) are correctly framed as "NOT executed at Stage S₁." The CONFLICT-as-default-coherence-direction wording for the cluster's joint claim is the right preservation discipline.

The CONCORDANT and ORTHOGONAL trivial fillings ("No open conflicts at the cluster level" / "Cluster members address different aspects") are operationally complete.

**§4.7 (what the cluster jointly licenses + does NOT license)**: sound on the two sub-block structure and the width-discipline rule. The independent-operationalisation-vs-same-signal-multi-take distinction (the map's §3 operationalisation-overlap-note feeding the §4.7a width discipline) is operationally correct. The §4.7b four predictable overclaim refusals (mechanism / group-level / predictive / averaging-the-conflict) cover the §6.3 spec's three-bullet "what the cluster does NOT license" list with one extension (the fourth — averaging-the-conflict — is the cluster-level analogue of guide #2's §4.4 PARTIAL-is-not-weak-SUPPORTED refusal applied to multi-HA reading). Sound.

**§4.8 (follow-up suggestions, own + external)**: sound on the two-track structure and the §3.11 external-research-N=1-scoping discipline. The three worked examples (C-stress-fatigue-shape third sister-HA on rolling-window OR median-split binning; C-bout-framework framework-validity HA on extended-window reference pool; C-bout-substance unmedicated-only sister-HA) are concrete pre-reg shapes rather than vague directions. The "distinct from open_inputs" cross-reference is the right separation (§4.8 = next claims; §4.9 = what is missing for this claim).

**§4.9 (open_inputs block)**: sound on the three refusal-to-proceed paths (member HA `interpretation.md` missing; cluster not in map; cascade-arrow upstream cluster's `cluster-*.md` not yet locked). The "open inputs do not block completion" framing per plan §3.8 is correctly inherited. The four-field shape (what is missing / what it blocks / cheapest acquisition path / fallback claim) matches plan §3.5 binding.

**§4.10 (cross-references)**: sound; the eleven destinations (member HA interpretations; map's §3 / §4 / §5 rows; cascade upstream `cluster-*.md`; limitations cross-refs; seed notes; literature methodology anchors; CONVENTIONS §3.4; locked plan §3.5-§3.12 + §4 + §6.3) are the right scope.

### §5 The coherence-call mapping rules

Sound on structure (per-label rules + worked examples + cascade-handling + trivial-ORTHOGONAL + crash-drop sensitivity). **R1 above**: the §5.2 PARTIALLY CONCORDANT worked example for C-stress-fatigue-shape mischaracterises HA-C3 v2's verdict as "monotone-inverse" — per HA-C3 v2 r2 result.md §3 + HA-C3p result.md §6 consolidation matrix, both HAs detect CONCAVE / inverted-U / threshold pattern peaking at stress 30-40, agreeing on the shape direction. The §5.2 + §5.3 alternative CONFLICT reading needs rewriting.

The §5.5 cascade-handling rule and worked example are accurate (per Invention 1 above; HA11-bout-redo +20.26 pp bars 1+2 PASS / bar 3 FAIL p=0.2609 matches result.md §3 exactly). The §5.6 trivial-ORTHOGONAL framing is sound with the A1 caveat above. The §5.7 cluster-level crash-drop sensitivity is sound per Invention 3 above.

### §6 Conflict rules

Sound. §6.1 (map-change-needed = the §3.6 layer-rule operationalisation) is the most important rule of the section and is concrete enough for a Stage S₁ drafter to apply it (per Invention 4 above). §6.2 (cascade-upstream-not-locked refusal) is structurally correct. §6.3 (PROVISIONAL inheritance + non-compounding) is sound (per Invention 5 above). §6.4 (cluster vs lived-experience prior) extends guide #2 §4.6 to the cluster level by analogy and is sound (per Invention 6 above).

### §7 Anti-patterns

Sound. The 11 anti-patterns + the §6.3 spec's 3 are correctly mapped (§7.2 = splitting CONFLICT; §7.4-§7.5 + §6.1 cover cherry-picking; §6.3 spec's "3 of 5 HAs agree" routes through §1 + §4.7a). The 8 additions (§7.1 in-stage re-routing; §7.3 cascade-as-co-equal; §7.4 cross-cluster smuggling; §7.5 sister-cluster evidence promotion; §7.6 seed-notes-as-constraints; §7.7 post-hoc caveats; §7.8 §3.12 commentary; §7.9 predictive-quality measures; §7.10 invented labels; §7.11 auto-resolving on re-examination) are the right boundary-enforcement anti-patterns for the layer-cross-cutting rules §3.10 + §3.12 + §3.6 + §3.7.

Distinct from upstream: §7.6 (seed-notes-as-constraints) is unique to Stage S₁ (no analogue in guide #1 or guide #2 because the seed notes file is Stage-S₁-specific). §7.3 (cascade-as-co-equal) is unique to Stage S₁ (cascade-arrow language only operates at cluster level). §7.4 + §7.5 (cross-cluster smuggling + sister-cluster evidence promotion) are unique to the cluster-bounded scope. §7.11 (auto-resolving on re-examination) is unique to the §3.7 drift policy at the cluster level. The remaining anti-patterns (§7.7 post-hoc caveats; §7.8 §3.12 commentary; §7.9 predictive measures; §7.10 invented labels) are the cluster-level analogues of guide #1 / guide #2 anti-patterns and are correctly framed as such.

### §8 Interview-prompt seeds

Sound. The 3 required seeds (cluster pre-declaration check; coherence-call interview; joint-claim narrowing) match §6.3 spec verbatim. The §8.4 optional fourth (cluster-trust upstream confirmation) parallels guide #1 §8.4 and guide #2 §8.4. The §8.1 confirmation-seed framing (cluster constellation should mechanically match the map's §3 row by the time the skill reaches §8.1; the seed exists to surface map-vs-stage misalignment, not to re-decide the constellation) is the right discipline and matches the §4.2 hard rule.

### §9 Agent-instruction outline

Sound (per Invention 7 above). The eight phases (Load / Gate / Extract / Interview / Produce / Refuse-to-lock-gate / Review-handoff / Acceptance + drift-trigger registration) are concrete and operationally implementable. The §9.6 refuse-to-lock gate's seven structural checks are the right protection layer (with the noted text-pattern detection concern for the eighth/last check). The §9.8 fifth drift-trigger registration for cascade-downstream clusters is a sound and necessary extension.

### §10 Cross-references

Spot-checked links (per request 15):

- `_plan_results_analysis_layer.md` § references (6.3, 3, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 4, 9) — all exist in the plan (verified).
- `descriptive_precondition_audit.md` (guide #1 LOCKED r2 2026-06-24) — referenced for verdict-trust chain; verified to exist.
- `verdict_to_inference.md` (guide #2 LOCKED r2 2026-06-24) — referenced for §3 output convention, §4 outline, §4.6 lived-experience reconciliation, §5.5 verbatim-qualifier rule, §6.2 PROVISIONAL handling, §7 anti-patterns; all sections verified to exist in guide #2 r1 (the locked r2 referenced is post-R1/R2 absorption per the guide #2 review).
- `research_line_limitations.md` (LOCKED r3) § references (5, 8) — all exist in the locked doc r3 (verified). The §5 row for `cluster-*.md` is correctly cited verbatim.
- `synthesis_structure_map.md` (LOCKED r3) § references (2, 3, 4, 5, 7) — all exist in the locked map r3 (verified; r3's cluster-table cells match the §3 worked examples for C-stress-fatigue-shape, C-bout-framework, C-bout-substance modulo R2 concern).
- `_synthesis_seed_notes_2026-06-23.md` — verified to exist; the advisory-only framing in §2 input #5 matches the seed-notes file's own status header.
- `_descriptive_stocktake_2026-06-23.md` § references (4, 9) — verified to exist.
- `bout_level_recovery_dynamics.md` + `citalopram_phase_stratification.md` — referenced for cluster-specific methodology MDs; verified to exist.
- Four literature methodology PDFs (Daza 2018, Shamseer / CENT 2015, Tate / SCRIBE 2016, Natesan 2023) — verified at named paths.
- CONVENTIONS § references (1, 1.2, 2.1, 3.4, 4.1, 4.2, 4.3) — all exist; the §3.4 crash-drop sensitivity reference correctly anchors §5.7.
- Four HA result.md references (HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo) — all exist; verdict + effect-size citations verified per R1 caveat above.

The cross-reference layer is in good shape; no broken links found in the spot-check.

### §11 Lock log

Sound. Single entry recording the r1 draft, six explicit named inventions (the seventh — §6.4 — is named in the body but worded slightly differently in the lock log entry), and the two §6.3 spec ambiguities resolved by interpretation. Matches the lock-log convention established by guide #1 r2, guide #2 r1, and map r3. The narrative explanation of what each invention does and what it extends is helpful for a future reviewer.

## 6. Cross-cutting concerns

### §3.6 conflict-resolution rule operationalisation (§6.1 of the draft)

Strongly enforced. The §6.1 four halt-criteria are concrete and operationally implementable (per Invention 4 above). The route-out instructions are concrete (stop drafting mid-session; produce only §4.9 open_inputs entry; hand off; resume only after separate map-revision session). The "Why this rule" paragraph correctly anchors the discipline to the layer-wide map's pre-registration discipline. The four halt-criteria cover the in-stage discovery cases the §3.6 rule was designed for — modulo the "topic boundary wrong" case which would be a Stage S₂ halt rather than Stage S₁ (consistent with the cluster-bounded-scope discipline). §7.1 anti-pattern enforces the rule against in-session map editing. The §8.1 interview seed surfaces map-vs-stage misalignment at the right point in the flow. The §9.2 gate operates correctly on the cluster-not-in-map path.

### §3.12 commentary boundary

Strongly enforced. §1 "what Stage S₁ does NOT do" list (third bullet), §6.4 (cluster-vs-prior is NOT §3.12 commentary), §7.8 anti-pattern (first-person narrative does not belong in §4.4-§4.7), §9.6 refuse-to-lock gate check on anti-pattern violations all close the boundary. The §6.4 distinction between cluster-level lived-experience prior reconciliation (structured, agree-or-diverge, no-auto-resolution) and §3.12 commentary (patient-facing subject-narrative, attached-to-formal-claim, language-bounded) is operationally correct and matches guide #2 §4.6's framing.

### §3.10 hard predictive gate boundary

Strongly enforced. §1 "what Stage S₁ does NOT do" list (second bullet), §4.7b third overclaim refusal, §5 mapping rules (no predictive language in any joint-claim sentence), §7.9 anti-pattern (no PPV, base rate, sensitivity, specificity, false-alarm rate, lead time, reliability), §9.6 refuse-to-lock gate check 8 (anti-pattern violations including predictive-language detection) all close the boundary. The forward pointer to Stage A via the synthesis-structure map's §5 K-construct row is correctly named but no Stage S₁ content crosses it.

### §3.11 follow-up suggestions implementation

Strongly enforced. §4.8 implements both tracks (own-research + external-research) per the §3.11 binding. The external-research-N=1-scoping requirement is correctly named ("every external-research suggestion MUST explicitly name the N=1 limit that prevents us from answering the question ourselves") and the §9 unscoped-follow-up-fallacy is cited as the prohibition. The §9.6 refuse-to-lock gate check 7 enforces this at the skill level. The "distinct from open_inputs" cross-reference (per §4.8 closing block) is the right separation.

The three worked examples (C-stress-fatigue-shape third sister-HA on rolling-window OR median-split binning; C-bout-framework framework-validity HA on extended-window reference pool; C-bout-substance unmedicated-only sister-HA on `bout_n_did_not_return_day`) are concrete pre-reg shapes. The C-bout-substance unmedicated-only sister-HA proposal is particularly well-motivated — HA-C4c's own unmedicated-only sensitivity arm landed REJECTED (δ=+0.059, p=0.1145) per result.md §4 row 1, which is exactly the cross-phase pooling confound the seed notes §3 caveat list flagged. Sound.

### L-ID citation discipline at cluster level

Mostly enforced (modulo R2 on the L2-era-strata-mismatch worked example for C-bout-substance). §4.5 implements the limitations doc r3 §5 binding ("Cite every limitation that touches any cluster member; also cite L2 if cluster members are from different era strata") faithfully on the "every L-ID that touches any cluster member" half. The list-format is mandatory (§9.6 gate 1). NA-with-reason rows are required (per §3 hard rule). The L-ID mapping examples for `cluster-stress-fatigue-shape.md` (L1, L2, L3, L4, L6, L7; L5 NA) and `cluster-bout-framework.md` (L1, L2, L3, L4, L6, L7; L5 NA) align with the synthesis-structure map's per-cluster L-IDs columns exactly.

The `cluster-bout-substance.md` L-ID mapping (L1, L2, L3, L4, L7; L5 NA, L6 NA) matches the map row's column. But the additional triggering of the L2-era-strata-mismatch citation "at the cluster level even though there is only one constituent HA" is a stretch beyond the limitations doc's literal "if cluster members are from different era strata" wording (per R2 above). The fix is one of: (a) drop the L2-era-strata-mismatch triggering from the C-bout-substance worked example and let HA-C4c's per-HA L2 citation carry the cross-phase pooling caveat; (b) route the within-member-sub-strata extension of L2 back to limitations doc §5 for an explicit lock-version bump (which would propagate to a guide #3 revision).

### Pre-declared constellation discipline (§4.2 of the draft)

Strongly enforced. The §4.2 paragraph cites the map row's declared-date and lock-version verbatim. The hard rule "It does NOT re-derive the constellation, does NOT add or remove constituents, and does NOT propose a re-clustering" is the right structural enforcement. The §6.1 halt-and-route rule covers the case where in-stage work reveals a re-clustering need. §8.1 interview seed surfaces map-vs-stage misalignment at the right point in the flow. §9.4 routes §8.1 first in the skill's interview phases.

The §4.2 question "what happens if a member HA's interpretation reveals it doesn't fit the cluster as defined?" is answered by §6.1 halt-criterion 1 ("A cluster member's interpretation makes a substantive licensed claim that places the HA on a different construct than the map's §3 row's 'shared construct' cell declares") + the route-out instructions. The Stage S₁ session does not silently treat the HA as if it were in a different cluster (§7.1 anti-pattern); it halts and routes to map-revision session.

### Stage I upstream-gate discipline

Strongly enforced. The §2 inputs require each cluster member's `interpretation.md`. The §6.2 cascade-upstream refusal handles the cascade-downstream case. The §9 agent-instruction outline encodes the refusal at §9.2 (gate) and §9.5 (produce-or-halt). The §4.9 refusal-to-proceed paths produce open_inputs entries per plan §3.5 hard rule. The four-routing-pathways (all members locked + cluster in map + cascade-upstream locked → proceed; any member's interpretation missing → halt; cluster not in map → halt; cascade-upstream `cluster-*.md` missing → halt) at §9.2 are operationally complete.

The Stage D verdict-trust call inheritance via the member interpretation §1 header (§2 input #6) is the right routing — Stage S₁ does not re-read the audit's per-assumption rows. The §6.3 PROVISIONAL inheritance rule covers the multi-PROVISIONAL case correctly.

### Sibling naming consistency

The draft uses `analyses/synthesis/cluster-XXX.md` (flat, no per-cluster subfolder). Verified against map r3 §2 (output path declaration in lock log entries) and plan §5 (output-structure tree). Match on the flat structure.

**A4 concern**: the map r3's cluster IDs include the `C-` prefix (`C-stress-fatigue-shape`, `C-bout-framework`, `C-bout-substance`) while the draft's §3 examples (and the plan §5 output tree) drop the prefix (`cluster-stress-fatigue-shape.md` etc.). The draft is consistent with the plan §5 tree, not with the map r3 ID convention. This is a minor naming inconsistency — a Stage S₁ drafter loading the guide and the map both at once would have to translate the cluster ID from `C-stress-fatigue-shape` (map row) to `cluster-stress-fatigue-shape.md` (output filename). One sentence in §3 acknowledging the prefix-drop convention ("the cluster's exact ID from the map's §3 row, with the `C-` prefix replaced by `cluster-` to match the plan §5 output tree convention") would close the loop.

### Length and density

1939 lines is ~30% longer than guide #2 (1493 lines) and ~92% longer than guide #1 (1008 lines). The trajectory (1008 → 1493 → 1939) is concerning if it extrapolates: guides #4-6 would land at ~2500-3000+ lines each, taking the methodology corpus past 15,000 lines.

Per the agent's self-report, §5 cascade walkthroughs are the compression candidate. Reviewer assessment: §5.1-§5.7 covers seven cases (the four label-mapping rules + cascade-handling + trivial-ORTHOGONAL + crash-drop sensitivity) and is the section most operationally useful at cluster level — every drafter will need it. The §5.5 cascade worked example for C-bout-substance reading C-bout-framework is dense but explains the most novel discipline rule in the layer; the C-stress-fatigue-shape worked examples at §5.2-§5.3 carry both readings (PARTIALLY CONCORDANT and CONFLICT alternative) which is operationally useful for showing the default-to-CONFLICT discipline in action.

Realistic compression opportunities (in priority order):

- **§4.5 5b worked examples (~30 lines)**: the three worked examples (cluster-stress-fatigue-shape; cluster-bout-framework; cluster-bout-substance) each enumerate L-IDs that touch the cluster and the L2-era-strata-mismatch addition. The triplet repeats structure; could compress to a single template + per-cluster L-ID list table.
- **Hard rule boxes throughout (~50 lines)**: several "Hard rule" blocks repeat themselves (e.g. §3 + §4.5 both carry hard rules on L-ID block completeness; §4.4 + §5 + §7.10 all enforce the four-label exhaustiveness). Cross-referencing rather than repeating would save ~50 lines.
- **§5 mapping rules + §4.4 surface (~50 lines)**: §4.4's coherence-call definitions and §5's per-label mapping rules overlap. The §4.4-points-at-§5 form (analogous to guide #2's §4.3 + §5 overlap A4 recommendation) would save ~50 lines without losing content.

Realistic total compression: ~130-200 lines (7-10%). Not blocking; A3 below recommends the compression for a future revision pass but does not require it.

The growth trajectory is operationally explainable: guide #1 covered single-HA audit (the simplest case); guide #2 covered single-HA interpretation with verdict-to-claim mapping (more complex but still per-HA); guide #3 covers multi-HA cluster synthesis with cascade-arrow handling, PROVISIONAL inheritance, four-label mapping, lived-experience-prior at cluster level (genuinely more complex). The +30% from guide #2 is not surprising. But the trajectory should be monitored at guides #4-6 — if guide #4 (Stage S₂ external contextualisation) lands at 2500+ lines, the methodology corpus risks becoming non-readable as a whole and per-stage compression becomes priority.

### What would block a Stage S₁ dry-run on C-stress-fatigue-shape at §11 step 8

Concretely: if a Stage S₁ drafter loaded this guide and tried to synthesise the C-stress-fatigue-shape cluster tomorrow, the operational gaps they would hit are:

1. **The §5.2 worked example points them in the wrong direction (R1 above).** The "monotone-inverse vs inverted-U" framing for HA-C3 v2 vs HA-C3p does not match the result.md substance. A drafter who relied on §5.2 would mis-label the cluster. The §5.3 alternative CONFLICT reading would also lead to a mis-label. **This is the most operationally important fix.**
2. **The §3 L-ID worked example for C-bout-substance (R2 above) creates ambiguity about whether the cross-phase-pooling within HA-C4c triggers a cluster-level L2 citation.** A C-bout-substance drafter would either (a) follow the worked example and cite L2 at the cluster level (which goes beyond the limitations doc's literal binding), or (b) ignore the worked example and cite only the L-IDs the map row lists (which under-cites per the draft's intended discipline). The ambiguity needs resolution before C-bout-substance is drafted.
3. **The trivial-ORTHOGONAL semantic stretch (A1 above) for single-member clusters.** A C-bout-framework drafter would need to read §5.4 + §5.6 carefully to understand why ORTHOGONAL applies to a single-member cluster despite §5.4's definition requiring multiple HAs. A one-paragraph clarification in §5.6 would close it.
4. **The thin-S₁ vs skipped-with-stub choice (A2 above) for the three active clusters.** A drafter starting on C-bout-framework or C-bout-substance would need to ask the user which path to take; the guide should enumerate which clusters fall in which path.

R1 + R2 are operationally most important; A1 + A2 are clarity refinements. None blocks the §11 step 7 skill build (which can encode the refuse-to-lock gates without the worked-example corrections), but R1 + R2 should be closed before the §11 step 8 dry-run.

## 7. Required actions to absorb before LOCK

- **R1.** §5.2 PARTIALLY CONCORDANT worked example + §5.3 CONFLICT alternative worked example for C-stress-fatigue-shape: rewrite to reflect actual HA-C3 v2 + HA-C3p result.md substance. Per HA-C3 v2 r2 result.md §3 (S = −0.740 p = 0.0002 sign-flip into significantly concave → wrong-direction override) + HA-C3p result.md §6 4-cell consolidation matrix (both HAs detect CONCAVE/inverted-U/threshold pattern peaking at stress 30-40, agreeing on inverse-non-monotone direction), the actual cluster reading lands closer to CONCORDANT-on-non-Wiggers-direction than PARTIALLY CONCORDANT or CONFLICT. The §5.2 + §5.3 worked examples should be rewritten to either (a) recharacterise both HAs as agreeing on inverted-U/concave shape and show the cluster reading as CONCORDANT-with-narrowed-Wiggers-rejection, OR (b) leave the C-stress-fatigue-shape worked example as a TBD (with a note that the actual cluster reading is for Stage S₁ to determine) and use a hypothetical cluster for the worked example. The current "monotone-inverse vs inverted-U" framing is factually incorrect and would mis-route a Stage S₁ drafter.

- **R2.** §3 L-ID worked example for `cluster-bout-substance.md` + §4.5 5b L2-era-strata-mismatch cluster-level binding + §9.6 gate 2: resolve the within-member-sub-strata vs across-member-strata interpretation of the limitations doc r3 §5 "if cluster members are from different era strata" clause. Either (a) drop the L2-era-strata-mismatch triggering from the C-bout-substance worked example and let HA-C4c's per-HA L2 citation in its own §4.5 carry the cross-phase pooling caveat (the cluster-level L2 citation is then NA, with one-sentence reason — i.e. "cluster has only one member; L2 cluster-level addition does not trigger; per-HA L2 carries the cross-phase pooling caveat"); OR (b) route the extension back to limitations doc §5 for an explicit lock-version bump (limitations doc r3 → r4 absorbing the within-member-sub-strata extension), which would then propagate downstream to a guide #3 revision.

## 8. Recommended actions to absorb before LOCK (optional)

- **A1.** §5.6 trivial-ORTHOGONAL for single-member clusters: add one-paragraph clarification acknowledging the semantic stretch (ORTHOGONAL per §5.4 defines "HAs that share a construct but address distinct facets" — strictly read, a single-member cluster has one HA not plural) and justifying why trivial-ORTHOGONAL is preferable to the alternatives (inventing a fifth label per §7.10; skipping S₁ via stage_skipped.md stub which loses the cluster-level L-ID block + cascade-precondition surface; leaving §4.4 undefined). This is operationally important because two of the three currently-active clusters are single-member.

- **A2.** §3 + §5.6: enumerate which of the three active clusters falls in which thin-S₁-vs-skipped-with-stub path:
  - C-stress-fatigue-shape (2 members) → standard S₁ (not single-member).
  - C-bout-framework (single member, no cascade-arrow upstream) → user choice (thin-S₁ or skip-with-stub).
  - C-bout-substance (single member, cascade-arrow downstream from C-bout-framework) → thin-S₁ effectively forced (cascade-precondition needs an artefact to live in).

  This per-cluster determination would help a Stage S₁ drafter know what they are looking at for each of the three active clusters before they start.

- **A3.** Length compression for a future revision pass (not blocking). Three candidates in priority order: §4.5 5b worked examples could compress to template + per-cluster L-ID list table (~30 lines); Hard rule boxes throughout could cross-reference rather than repeat (~50 lines); §4.4 surface + §5 mapping rules could use the §4.4-points-at-§5 form (per the guide #2 A4 recommendation; ~50 lines). Realistic total: ~130-200 lines (7-10%) without losing operational content. The §5 cascade walkthroughs the agent's self-report flagged as the compression candidate are reviewer-assessed as the section most operationally useful at cluster level — they should NOT be compressed.

- **A4.** §3 sibling-naming convention: add one sentence acknowledging the prefix-drop from map's `C-` cluster ID convention to plan §5's `cluster-` output tree convention ("the cluster's exact ID from the map's §3 row, with the `C-` prefix replaced by `cluster-` to match the plan §5 output tree convention"). Minor but closes the naming-translation loop for a drafter loading both the guide and the map.

## 9. Confirmed-good

The following elements of the draft are sound and need no revision:

- §1 purpose framing + alternatives-considered paragraph + skill-precondition note + six-bullet "What Stage S₁ does NOT do" list.
- §2 eight-input list (the §6.3 spec's three + the synthesis-structure map binding + cascade-upstream `cluster-*.md` + seed notes advisory + Stage D verdict-trust chain + CONVENTIONS + literature anchors).
- §3 output spec + flat-no-per-cluster-subfolder convention + thin-S₁ vs skip-with-stub framing + L-ID citation discipline at output level (modulo R2 on the L2 cluster-level extension).
- §4.1 mechanical header (cluster ID + member HA list + verdicts with qualifiers per guide #2 §5.5 + Stage D verdict-trust calls + shared construct + operationalisation-overlap-note + cascade-arrow language).
- §4.2 pre-declared constellation template + hard rule against re-derivation + cascade-arrow sub-paragraph extension.
- §4.3 per-HA row format + worked example for C-stress-fatigue-shape (the row format itself; R1 caveat applies to the §5.2 reading of those rows).
- §4.4 four-label exhaustiveness + default-to-CONFLICT-on-ambiguity hard rule.
- §4.5 three sub-block structure (5a caveats / 5b L-ID citation / 5c cascade-precondition) + "no new caveats at Stage S₁" discipline + the cascade-precondition sub-paragraph template (modulo R2 on 5b).
- §4.6 no-auto-resolution rule + paragraph-per-conflict structure + resolution-paths-not-executed-at-Stage-S₁ framing + trivial fillings for CONCORDANT and ORTHOGONAL.
- §4.7a width discipline (no wider than narrowest member's claim unless cross-operationalisation replication warrants it; independent vs same-signal-multi-take distinction) + §4.7b four predictable overclaim refusals.
- §4.8 two-track structure + N=1-scoping discipline + three concrete pre-reg-shape worked examples + distinct-from-open_inputs cross-reference.
- §4.9 three refusal-to-proceed paths + four-field shape + open-inputs-do-not-block-completion framing.
- §4.10 eleven cross-reference destinations.
- §5.1 + §5.3 + §5.4 + §5.5 cascade-handling + §5.6 trivial-ORTHOGONAL (modulo A1 clarification) + §5.7 crash-drop sensitivity (the mapping rules themselves; R1 caveat applies to §5.2 only).
- §6.1 four halt-criteria + route-out instructions + "why this rule" paragraph.
- §6.2 cascade-upstream-not-locked refusal.
- §6.3 PROVISIONAL inheritance + non-compounding rule + perverse-incentive-prevention reasoning.
- §6.4 cluster-vs-lived-experience-prior reconciliation extending guide #2 §4.6.
- §7.1-§7.11 eleven anti-patterns including the eight extensions beyond §6.3 spec.
- §8.1-§8.4 three required seeds + one optional cluster-trust-confirmation seed.
- §9.1-§9.8 eight-phase agent-instruction outline including the §9.6 refuse-to-lock gate (seven structural checks).
- §10 cross-references (all spot-checks pass).
- §11 lock log (per established convention).

The three active clusters in the map r3 (C-stress-fatigue-shape, C-bout-framework, C-bout-substance) are mostly well-served by this guide: a Stage S₁ drafter loading the guide tomorrow would have an operationally clear procedure for each, modulo the four findings above (R1 + R2 + A1 + A2).

---

**Reviewer recommendation**: absorb R1 + R2 (one-revision-cycle fixes); A1 + A2 are recommended for clarity; A3 + A4 are optional refinements. After R1 + R2 absorption, the guide can LOCK without a second fresh-session review per the established Option-γ pattern matching plan / limitations / map / Stage D guide / Stage I guide closures. The §11 step 6.4 (guide #4 `external_contextualisation.md`) drafting is unblocked by the LOCK on guide #3.
