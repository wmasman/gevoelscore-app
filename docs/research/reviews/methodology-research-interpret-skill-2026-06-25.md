# Methodology review — research-interpret skill (r1, 2026-06-25)

**Reviewer mode**: fresh-session peer review. Reviewer is independent of the drafting session. Fresh session — no exposure to the drafting context; doc-only knowledge.
**Target**: [`.claude/skills/research-interpret/SKILL.md`](../../../.claude/skills/research-interpret/SKILL.md) (DRAFT r1, 2026-06-25, 566 lines).
**Review date**: 2026-06-25
**Standards applied**: [CONVENTIONS](../CONVENTIONS.md) §1, §1.2 (role split + reviewer-mode-with-authorization + fresh-session-review), §2.1, §2.3; [plan](../methodology/_plan_results_analysis_layer.md) r5 LOCKED §3 (stage-map), §3.5 (missing-inputs first-class), §3.6 (map conflict-resolution), §3.7 (drift), §3.8 (stopping/completion), §3.9 (limitations binding), §3.10 (hard predictive gate), §3.11 (follow-up tracks), §3.12 (commentary boundary), §4 (producer/reviewer split — guides + map + limitations + this skill = methodology MDs; per-HA / cluster / topic / construct / translation outputs = reviewer-mode-with-authorization), §5 (output-structure tree), §7 (the binding spec for this skill), §9 (layer anti-patterns), §11 step 7; six LOCKED methodology guides r2 (descriptive_precondition_audit / verdict_to_inference / internal_synthesis / external_contextualisation / actionability_translation / translation_to_audience); [limitations doc](../methodology/research_line_limitations.md) r3 §3 + §5 + §8; [synthesis-structure map](../methodology/synthesis_structure_map.md) r3; sibling skill `.claude/skills/superdesign/SKILL.md` (frontmatter anchor). Prior reviews methodology-{descriptive,verdict,synthesis,context,actionability,translation}-2026-06-{24,25}.md as shape template.

---

## 1. Overall verdict

**REVISION RECOMMENDED (mild).** The skill is a faithful operationalisation of locked-plan §7. All seven §7 responsibilities + the three "what the skill must NOT do" prohibitions land at the prose level; the six-stage routing table mechanically maps each `<stage>` arg to the correct guide MD + the correct output-path + the correct refusal precondition; the §3.12 commentary discipline + the §3.10 hard predictive gate propagate without backdoor; the L-ID citation discipline table tracks the limitations doc r3 §5 row-for-row; the producer/reviewer-split handoff at responsibility #8 correctly routes interpretation/synthesis/contextualisation/actionability/translation outputs to `/research-review` (not `/research-methodology-review`). The seven inventions beyond §7 are each either a faithful consolidation of per-guide §9 outlines (routing table, interview-engine loop, L-ID table, downstream-citation-count) OR a per-guide-traced operational addendum (§3.12 cross-cutting section consolidating Stage A §5.9 + Stage T §5.11; bootstrap responsibilities for `_open_inputs.md` + `plain_language_dictionary.md`; expanded anti-pattern list). None invents new policy; each is traceable to a §7 sub-bullet or a per-guide §9 paragraph.

**The skill-doesn't-weaken-guide check passes.** Spot-checking every routing-table refusal precondition against the corresponding guide's §9.1-§9.2 found no weakening; the §3.12 commentary boundary is preserved at three locations (routing table Stage T row, the cross-cutting §3.12 section, the skill-specific anti-patterns); the Stage A hard predictive gate is preserved in three locations (routing table Stage A row, skill-specific anti-pattern #2, §3.12 cross-cutting section's commentary-cannot-promote-tier paragraph); the L-ID table matches limitations doc r3 §5 row-by-row with the correct "MUST cite unconditionally" / "all seven applies-or-NA" / "as they apply" distinctions. **Frontmatter discoverability is confirmed** — the system-reminder lists the skill in the available-skills surface with the description rendering coherently; the frontmatter shape (`name + description + metadata{author,version}`) matches the sibling `superdesign/SKILL.md` convention verbatim.

Five findings drive the REVISION RECOMMENDED verdict rather than ACCEPT. Two are required (R1, R2); three are recommended (A1–A3). **None blocks §11 step 8 dry-run** if R1 is absorbed first; all five are one-revision-cycle fixes that can be absorbed before the dry-run on HA-C4 begins.

- **R1.** **Cluster-row "L2-if-strata-mismatch" trigger and topic-row "L1+L2+L4 unconditional" assertion both correct, but the L-ID table's S₁ row says "also cites L2 if cluster members are from different era strata" — the wording is faithful to limitations doc r3 §5 verbatim ("also cite L2 if cluster members are from different era strata"). However, the limitations doc §5 binding is **on top of** the union of L-IDs touching members; the skill table reads "Cites every limitation that touches any cluster member; also cites L2 if cluster members are from different era strata." That is exactly the limitations doc wording — no weakening. The concern is downstream: the routing table's Stage S₁ refusal preconditions cite "cascade-arrow upstream `cluster-*.md` (where the map's §3 row declares a cascade precondition, e.g. C-bout-framework → C-bout-substance) must exist and be LOCKED." Verified against the map's §3 row for C-bout-substance: the cascade-arrow language is "this cluster's verdict propagates as a caveat-class precondition to C-bout-substance (downstream)." The skill correctly extracts this as a refusal precondition. **No fix needed on the L-ID table itself; this finding upgrades to OBSERVATION-ONLY.** Promoting R1 to be the bootstrap-race concern instead: see new R1 immediately below.

- **R1 (revised).** **Bootstrap race-condition between `_open_inputs.md` and `plain_language_dictionary.md` is not resolved.** Responsibility #6 scaffolds `_open_inputs.md` on first ever invocation if missing (any stage); responsibility #7 scaffolds `plain_language_dictionary.md` on first Stage T invocation if missing. These are independent code paths but they both run on first invocation under common conditions. The race condition: if the user's first ever invocation is `/research-interpret translate <source-path>`, both scaffolds need to fire. The skill describes each in isolation but does not specify the order. The minimum fix: one sentence in responsibility #7 stating "If `_open_inputs.md` is also missing (i.e., this is the first ever invocation of any stage), responsibility #6's scaffold runs FIRST so the dictionary's bootstrap can itself append an `open_inputs` entry if the bootstrap encounters a partial-scaffold state." A stronger fix would name both bootstraps in §"Skill responsibilities" #6 and explicitly order them. This matters operationally for the §11 step 9 translation dry-run, not for the §11 step 8 HA-C4 dry-run (Stages D → A only touch responsibility #6's scaffold). **Not blocking for step 8** but blocks step 9.

- **R2.** **The skill's routing table Stage T row reads "research-audience track may be skipped only via explicit skip-research-internal record at source" — this is the right discipline, but the location of the skip-record is under-specified.** Per guide #6 §3 ("Skip-research-internal option"): "the source artefact's cross-references record 'Stage T translation skipped — research-internal only; rationale: <one sentence>'." The skill should explicitly name that the skip lives at the **source artefact's** §-cross-references (Stage I §4.10 / Stage S₁ §4.10 / Stage S₂ §4.10 — these section numbers exist verbatim in the locked guides), not at a separate file. As written the skill prose ("explicit skip-research-internal record at source") is technically correct but leaves the skill checking-the-wrong-location ambiguity at execution time. One-sentence fix in the routing table's Stage T row OR in responsibility #2: "The skip-record lives at the source artefact's §10 / §4.10 cross-references section (per guide #6 §3); the skill reads it from there before refusing on missing patient-audience-only output." Closes the routing ambiguity.

Recommended:

- **A1.** The `--drift-check` helper specification (responsibility #9) names six concrete trigger-check mechanisms (`git log` on cited `result.md`; lock-log version walk; map §3 cluster-member additions; ≥6-month cadence; `_pending_literature_fetch.md` check; "etc."). The "etc." is the under-specification. Per guides #2/#3/#4/#5/#6 §9.8, the registered trigger sets are stage-specific (4 triggers for I; 4-or-5 for S₁ where cascade-downstream adds the fifth; 4 for S₂; 4-or-5 for A where commentary-carrying constructs add the fifth layperson-test-fail trigger; 4-or-5 for T where commentary-carrying translations add the fifth layperson-test-re-test trigger). A drift-check helper that does not enumerate every trigger type will silently miss the commentary-carrying-extras at A and T, which are the ones most likely to fire in the project's near-term roadmap (the four ready HAs will produce two commentary-eligible constructs). Recommended fix: expand the §9 helper-implementation list to ~9-10 concrete trigger types instead of 6-with-"etc." Not blocking for step 8.

- **A2.** The Skill responsibilities #11 (limitations-doc downstream-citation-count maintenance) names the five citation-block locations to increment ("Stage I §4.5; Stage S₁ §4.5; Stage S₂ §4.7; Stage A §5.11; Stage T §5.5"). Spot-checking against the guides:
  - Guide #2 (Stage I): citation block lives at §4.5 5b — the skill says "§4.5" without the 5b sub-marker. Acceptable shorthand but the increment-execution will need to find the L-ID list inside §4.5 (not at the §4.5 header), so the skill needs to know to scan into 5b. One sentence "(specifically the 5b L-ID sub-block where applicable)" would tighten.
  - Guide #3 (Stage S₁): citation block lives at §4.5 (with sub-blocks 5b L-ID, 5c cascade-precondition). Same shorthand-ambiguity concern. Same one-sentence fix.
  - Guide #4 (Stage S₂): citation block lives at §4.7 verbatim. Match. **No fix.**
  - Guide #5 (Stage A): citation block lives at §5.11 verbatim. Match. **No fix.**
  - Guide #6 (Stage T): citation block lives at §5.5 verbatim. Match. **No fix.**

  Net: a one-sentence parenthetical for Stage I + Stage S₁ would tighten the increment-target. Not blocking.

- **A3.** The skill's lock-log entry is a single 1,300-character paragraph (the longest in the layer's lock-log corpus by ~3×). Same A4-class observation flagged in guides #4, #5, #6 r1 reviews. Two-or-three short paragraphs (one for the seven inventions; one for the §7-faithfulness traceability; one for the discovery about superdesign/SKILL.md frontmatter convention) would scan better. Not blocking.

## 2. Four-input bar findings (CONVENTIONS §2.2)

This skill MD is **producer-mode infrastructure** per plan §4 row "/research-interpret skill | Producer | Claude builds | Skill-test session: dry-run on one HA per guide". The four-input bar applies in the lighter form used for guide #6's review (planning-MD-style assessment, not analytical-claim-style).

| Input | Status | Reasoning |
|---|---|---|
| 1. Best-practices standards | PASS | The frontmatter shape (`name + description + metadata{author,version}`) matches the existing project skill convention exactly (verified against `.claude/skills/superdesign/SKILL.md`). The interview-engine loop pattern (Load → Gate → Extract → Interview → Produce → Refuse-to-lock → Acceptance + handoff) is a faithful consolidation of the six guides' §9 phase structure (each guide has §9.1-§9.8; the skill's seven phases collapse §9.7 + §9.8 into a single Phase 7). The skill matches Claude Code's general skill-loading discipline (skill loads guide MD as data; never inlines guide content). |
| 2. Established literature | PASS | The cross-references section names the right anchor MDs as binding (locked plan §7 as the binding spec; six guides as binding rule-MDs; limitations doc + map as cross-cutting supporting MDs; CONVENTIONS §1.2 + §2.3 as the project's role-split + audit-before-push). The "Adjacent skills" sub-section correctly distinguishes `/research-review` (for reviewer-mode-with-authorization outputs) from `/research-methodology-review` (for producer-mode methodology MDs including this skill itself); spot-checked against locked plan §4 + §11 intro and matches. |
| 3. Tradeoff vision | PARTIAL | The skill does NOT carry an "Alternatives considered" paragraph (cf. each guide r2's §1 closing paragraph satisfying CONVENTIONS §2.2 item 3 explicitly). The lock-log mentions tradeoffs implicitly ("operational details invented beyond plan §7 (each is a faithful realisation of the §7 brief plus the per-guide §9 outlines, NOT new policy)") but no explicit alternatives-considered section. The natural alternatives — multiple per-stage skills (vs single skill loading guide as data per plan §2 locked decision); separating `--drift-check` into its own skill; per-stage interview-engines instead of a guide-uniform six-phase loop — are not explicitly evaluated. Not load-bearing for a producer-mode infrastructure MD whose spec is fully pinned by plan §7, but inconsistent with the per-guide pattern. Recommended at A4 below (not promoted from recommended to required because the plan §7 spec is unambiguous on the single-skill / guide-as-data shape; the alternatives are foreclosed by the plan). |
| 4. Research limitations + objectives | PASS | The skill correctly cites the four ready HAs (HA-C3 v2, HA-C3p, HA-C4c, HA11-bout-redo) implicitly via the routing-table examples (`HA-C4c`, `C-bout-substance`, `topic-hrv-in-lc`, `construct-overnight-recovery`). The §3.12 commentary discipline section correctly grounds in K-stress-fatigue-monitoring + K-bout-recovery-signal (the two commentary-eligible constructs in map r3 §5). The lock log notes the producer-mode-infrastructure status correctly. |

Overall: 3 PASS + 1 PARTIAL. The four-input compliance is good. Adding A4 below (explicit alternatives-considered paragraph) would lift the PARTIAL to PASS.

## 3. Faithfulness to plan r5 §7 spec

Plan §7 specifies eight elements for the skill: invocation shape; seven skill responsibilities; the skill-instruction-MD contents (header / routing-table / per-stage preconditions / interview-engine pattern / anti-patterns block / drift-check helper / fresh-session-review pointer); three "What the skill must NOT do" prohibitions; the §3.6 map-conflict-resolution routing inherited from upstream guides.

| §7 element | Implementation | Faithfulness |
|---|---|---|
| Invocation shape | §"Invocation" section + the `--drift-check` helper sub-section | **Faithful.** The `<stage> <target>` shape is correct; the six `<stage>` arg values map to the locked plan's six stages; the `<target>` semantics per stage match guide-#1's HA-XX folder convention, guide-#3's cluster-XXX naming, guide-#4's topic-XXX naming, guide-#5's construct-XXX naming, and guide-#6's source-path resolution (the source-path variant is the right resolution of the plan's "source-stage artefact path" language). The `--drift-check` helper is named per plan §7 and operationalised in responsibility #9. |
| Skill responsibility #1 (Stage-routing) | Skill responsibilities section #1 + the routing table | **Faithful.** The skill loads the right guide MD per `<stage>` arg; the "Never duplicate guide content; cite it" framing matches the plan §7 "skill is the engine; the guides remain the source of truth." |
| Skill responsibility #2 (Dependency check) | Skill responsibilities section #2 + the routing table's Refusal-preconditions column | **Faithful.** Refuse on upstream missing/wrong-state; produce only the relevant `open_inputs` entries on refusal; never silently soft-fail. Matches §7 verbatim. R2 above is the one ambiguity (Stage T skip-record location). |
| Skill responsibility #3 (Interview execution) | Skill responsibilities section #3 + the §"Interview-engine pattern" Phase 4 | **Faithful.** Walk §8 seeds verbatim; for §9.4 "skill MUST NOT autonomously fill" judgment-call fields, present the seed and record the user's articulation; never silently pick. Matches §7 + per-guide §9.4 verbatim. |
| Skill responsibility #4 (Artefact production) | Skill responsibilities section #4 + Phase 5 Produce | **Faithful.** Output at routing-table-named path; follow guide's §4/§5 outline; DRAFT r1 + mode flag in status header; `## Authorship` block per CONVENTIONS §1.2 for reviewer-mode-with-authorization artefacts (Stages I/S₁/S₂/A/T); producer-mode for Stage D. The producer/reviewer split is correctly mapped. |
| Skill responsibility #5 (Refusal discipline) | Skill responsibilities section #5 + Phase 6 Refuse-to-lock gate | **Faithful with extension.** Walk each guide's §9.6 fire-list item-by-item; refuse to mark ready-for-lock if any check fires; user may not force-of-argument override; remedy is fix the gap OR log to open_inputs and accept lower-tier/PROVISIONAL. Matches §7 + per-guide §9.6 verbatim. Extension: the explicit "user-accepts-as-ready-for-completion time" framing operationalises the §3.8 stopping criterion at lock-decision time. |
| Skill responsibility #6 (Missing-inputs queue maintenance) | Skill responsibilities section #6 | **Faithful.** Read existing queue + scaffold on first invocation; surface current queue length; on lock-event append entries deduplicated by (missing-input × blocked-target) key; four-field shape per plan §3.5. The scaffold-on-first-invocation responsibility correctly traces to plan §3.5 (which names the queue path) + the absence of `_open_inputs.md` from disk today (verified via grep — does not exist). |
| Skill responsibility #7 (Bootstrap plain_language_dictionary.md) | Skill responsibilities section #7 | **Faithful.** The bootstrap pattern matches guide #6 §9.1 verbatim (the alternative-bootstrap-pathway at step 7 sibling task is the guide's own alternative; the §9.1 first-invocation-scaffold is the fallback). One-time skill responsibility; subsequent Stage T invocations load-and-append. R1 above is on the race-condition with responsibility #6. |
| Skill responsibility #8 (Review handoff) | Skill responsibilities section #8 + Phase 7 acceptance | **Faithful and correctly routed.** Stage D: no fresh-session review (producer-mode audit). Stages I / S₁ / S₂ / A / T: fresh-session `/research-review` (NOT `/research-methodology-review`). Stage T patient-audience: additional layperson-test gate per guide #6 §9.7 + locked-plan §4. The routing is exactly per plan §4 producer/reviewer-split table + §11 intro discipline-gate routing. **Critical correctness check passes:** the skill correctly identifies that the producer/reviewer split routes per-HA / cluster / topic / construct / translation outputs to `/research-review`, NOT to `/research-methodology-review` (the latter is reserved for guides + supporting MDs + this skill itself). |
| Skill responsibility #9 (--drift-check helper) | Skill responsibilities section #9 | **Faithful.** Walk all locked artefacts; read each lock log's "Drift triggers registered" line; check whether triggers have fired; surface triggered artefacts sorted by downstream-blast-radius; user decides which to re-examine; skill does NOT auto-re-examine; re-examination produces CONFIRMED-NO-CHANGE or REVISED. Matches plan §3.7 + §7 helper-spec verbatim. A1 above is on the under-enumerated trigger-type list. |
| Skill responsibility #10 (drift-trigger registration manual-pending-skill) | Skill responsibilities section #10 | **Faithful.** Until the skill is in use, the lock-log "Drift triggers registered" line is maintained by hand; once in use, the skill walks the lines. The carry-forward pattern correctly bootstraps the skill onto pre-existing locked artefacts (the four ready HAs + the limitations doc + the map + the six guides). |
| Skill responsibility #11 (Limitations-doc downstream-citation-count maintenance) | Skill responsibilities section #11 | **Faithful.** Cited from the limitations doc §8 worked-example pattern (verified at limitations doc r3 §8 "Tracking-mechanism status (current limitation): The intended mechanism is the `/research-interpret` skill's `--drift-check` helper... That skill does not yet exist — it is built in plan §11 step 7... Until the skill lands, the table is maintained manually..."). A2 above is on the §4.5 5b shorthand. |
| What the skill must NOT do (3 prohibitions) | Skill-specific anti-patterns 1-3 | **Faithful.** All three prohibitions land verbatim — (1) Pick an interpretation when the guide names it a judgment call; (2) Promote a tier in Stage A by force of argument; (3) Edit the guide MDs in-session. Each prohibition cites its source (per-guide §9.4 for #1; plan §3.10 + guide #5 §9.6 for #2; plan §6 conflict-rule pattern for #3). |
| §3.6 map-conflict-resolution | §"§3.6 map-conflict-resolution handling" cross-cutting section | **Faithful.** Halt-and-route discipline; do NOT edit map in-session; record proposed map change in `_open_inputs.md`; resume only after separate producer-mode session updates the map and runs its own `/research-methodology-review` pass. Matches plan §3.6 verbatim and parallels the halt-and-route in guide #3 §6.1, guide #4 §6.1, guide #5 §6.5, guide #6 §6.6. |

No §7 element is missing or substantively altered. Spec faithfulness is high.

## 4. The seven inventions beyond §7

### Invention 1 — Six-stage routing table

**Sound.** §7 says "A stage-routing table mapping `<stage>` arg → guide MD path → output folder (six rows, one per stage)." The skill's routing table extends to four columns (`<stage>` / Guide MD / Output path / Refusal preconditions). Spot-checking each row against the corresponding guide's §3 (output path) + §9.1-§9.2 (refusal preconditions):

- **Stage D**: Output `docs/research/analyses/descriptive/HA-XX/descriptive_audit.md (+ plots/ subfolder)` — matches guide #1 §3 verbatim. Refusal: "hypothesis.md, result.md, test.py must all exist for the HA" — matches guide #1 §9.1 verbatim ("The skill MUST refuse to proceed if any of `hypothesis.md`, `result.md`, or `test.py` is missing").
- **Stage I**: Output `docs/research/analyses/interpretation/HA-XX.md` — matches guide #2 §3 verbatim (flat naming, no per-HA subfolder). Refusal: audit-trust four-state routing — matches guide #2 §9.2 verbatim (TRUSTED proceeds; DOWNGRADED-INCONCLUSIVE-PROVISIONAL proceeds under explicit user acceptance; REQUIRES-DESCRIPTIVE-WORK halts; STRUCTURALLY-UNTESTABLE-AS-CURRENTLY-SPECIFIED halts and routes to pre-reg revision).
- **Stage S₁**: Output `docs/research/analyses/synthesis/cluster-XXX.md` — matches guide #3 §3 verbatim. Refusal: every cluster-member HA's interpretation locked + cluster in map + cascade-arrow upstream locked where applicable — matches guide #3 §9.2 verbatim (four-state gate). The cascade example "C-bout-framework → C-bout-substance" is correct against map r3 §3.
- **Stage S₂**: Output `docs/research/analyses/contextualisation/topic-XXX.md` — matches guide #4 §3 verbatim. Refusal: every constituent cluster-*.md LOCKED + topic in map + limitations doc must exist — matches guide #4 §9.2 verbatim.
- **Stage A**: Output `docs/research/analyses/actionability/construct-XXX.md` — matches guide #5 §3 verbatim. Refusal: every feeding topic LOCKED + construct in map + tier aspiration permits claimed tier + for tier-3 a pre-registered forward-validation HA with lock-date before window-start — matches guide #5 §9.2 + §5.5 verbatim. **Hard predictive gate preserved as load-bearing refusal precondition.**
- **Stage T**: Output both `docs/research/analyses/translation/research-audience/<source-name>.md` AND `patient-audience/<source-name>.md` — matches guide #6 §3 verbatim against locked plan §5 binding tree. Commentary "patient-audience track only" parenthetical correctly carries the §3.12 hard separation. Refusal: source locked + limitations doc exists + dictionary exists or scaffolded under responsibility #7 — matches guide #6 §9.2 verbatim. R2 above is on the skip-research-internal record location.

**The transitive-chain enforcement paragraph below the table** ("for every stage the skill ALSO refuses if the upstream-stage dependency chain has any unlocked artefact — the chain is transitive [Stage T on a Stage A source requires the Stage S₂ → Stage S₁ → Stage I → Stage D upstream chain locked for the relevant HAs]") correctly extends plan §3 dependency rules to the skill's enforcement surface. Sound.

### Invention 2 — Seven-phase interview-engine loop

**Sound.** The loop collapses each guide's eight §9 sub-sections into seven phases (Load / Gate / Extract / Interview / Produce / Refuse-to-lock gate / Acceptance + handoff). The compression is structural: §9.1 → Phase 1; §9.2 → Phase 2; §9.3 → Phase 3; §9.4 → Phase 4; §9.5 → Phase 5; §9.6 → Phase 6; §9.7 + §9.8 → Phase 7 (review handoff merged with acceptance + drift-trigger registration, which is the right grouping because the handoff fires on user acceptance per §3.8 stopping criterion).

Spot-checking each phase against the corresponding §9 section across all six guides confirms guide-uniformity holds (each phase's content is consistent across all six guides; only the loaded data + the interview seeds + the gate items differ). The "Phase 1 Load" fail-safe to "NOT BACKSTOPPED + `open_inputs` entry rather than silent soft-fail" correctly inherits guide #1 §9.1's fail-safe pattern as the canonical example (verified against guide #1 §9.1 verbatim).

### Invention 3 — Cross-cutting §3.12 commentary discipline section

**Sound — this is the load-bearing §3.12-at-skill-level operationalisation.** The section consolidates three propagation points (Stage A §5.9 → Stage T patient §5.11 → Stage T research-audience FORBIDDEN) into one place. Verification against the upstream sources:

- Guide #5 §5.9 (the Stage A optional commentary section) — matches the skill's Stage A §5.9 paragraph: tier-1 OR tier-2 attached only (not tier-3); subject-attribution every sentence; permitted-vs-forbidden wording per guide #5 §5.9; cannot promote tier; cannot float unattached; skipped-with-rationale is a valid completion state. **Verified.**
- Guide #6 §5.11 (the Stage T patient-audience-track-ONLY commentary translation) — matches the skill's Stage T patient §5.11 paragraph: layperson-test gate as binding test; revision before lock if layperson reads commentary as soft prediction or advice. **Verified.**
- Plan §3.12 hard separation (research-audience FORBIDDEN) — matches the skill's Stage T research-audience paragraph: §5.11 commentary FORBIDDEN; skill refuses to lock research-audience track with §5.11 section present (guide #6 §9.6 item #12). **Verified.**

The closing paragraph carries the load-bearing hard-separations as cross-cutting reminders: commentary never cited downstream; commentary cannot promote tier (cites guide #5 §6.4 + §7.8 + plan §9 commentary-promotion fallacy); tier promotion requires forward-validation per §3.10 full stop. **All three §3.12 hard separations preserved at the skill-engine level.**

### Invention 4 — L-ID citation discipline table

**Sound.** The table consolidates the limitations doc r3 §5 binding per stage. Spot-checking each row against the limitations doc §5 verbatim:

- **D `descriptive_audit.md`** — "Cites L5 + L7 where the checklist depends on them (the §6.1 v24-presence-conditioning item → L5; the §6.1 missingness item → L7)" — matches limitations doc §5 row verbatim (with the corrected §6.1 → §5.5/§5.2 sub-routing per guide #1 r2 §5 actual section numbers; the skill's reference to "§6.1" is the limitations doc's reference to the **plan's §6.1 brief**, not guide #1's actual §5 — slightly confusing but not wrong since the limitations doc itself references "§6.1" of the plan-brief).
- **I `interpretation.md`** — "Cites every limitation that touches the HA's primary signals or operationalisation; one-sentence project-specific application per L-ID" — matches limitations doc §5 verbatim.
- **S₁ `cluster-*.md`** — "Cites every limitation that touches any cluster member; also cites L2 if cluster members are from different era strata" — matches limitations doc §5 verbatim.
- **S₂ `topic-*.md`** — "**MUST cite L1, L2, L4 unconditionally**; cite L3, L5, L6, L7 as they apply" — matches limitations doc §5 verbatim, with the unconditional emphasis preserved.
- **A `construct-*.md`** — "**MUST cite all seven L1-L7 with explicit applicability-or-NA per limitation** — most rigorous L-ID discipline in the layer" — matches limitations doc §5 verbatim ("MUST cite all seven, with explicit applicability-or-NA per limitation (actionability is the downstream-most claim and inherits all systemic context)").
- **T translation artefacts** — "Patient-audience track translates applicable limitations into plain-language honest-uncertainty wording; research-audience track keeps the L-IDs as cross-references" — matches limitations doc §5 verbatim.

The closing paragraph correctly enforces "A citation is not a copy-paste; it is a one-line acknowledgment with the L-ID and one sentence on how the limitation applies to this artefact's specific claim" (matches limitations doc §5 verbatim) + the skill-level refuse-to-lock check on missing L-IDs + on Stage T source-citation-fidelity. **No paraphrase weakening; the table is a faithful citation-discipline reference.**

### Invention 5 — Responsibility #11 downstream-citation-count maintenance

**Sound.** Per the brief's self-report, this is "lifted from the limitations doc's §8 worked-example into an explicit skill responsibility for completeness." Verification against limitations doc r3 §8 confirms the manual-pending-skill discipline is named verbatim there ("Until the skill lands, the table is maintained manually by the drafter of each downstream artefact... The §11 step 7 skill landing will replace this manual discipline with the automated `--drift-check` mechanism"). Lifting it to an explicit skill responsibility is the right framing because the skill is the binding implementation event the limitations doc named; without the responsibility-list entry the increment-on-lock behaviour would be implicit-only. A2 above is on the §4.5 / §5.11 / §5.5 shorthand.

### Invention 6 — Bootstrap responsibilities for both `_open_inputs.md` AND `plain_language_dictionary.md`

**Sound but the race-condition is unresolved.** Per the brief's self-report, "responsibility #6 + #7 explicit bootstrap for both `_open_inputs.md` AND `plain_language_dictionary.md`." Both files are confirmed absent from disk (verified via grep on `docs/research/methodology/`). The bootstrap-on-first-invocation pattern is operationally implementable for each in isolation:

- Responsibility #6 (`_open_inputs.md`): "Read the existing... queue (scaffold it on first ever invocation if missing — minimal header + empty table)." Implementable as Read-or-Write idempotent at start of every invocation.
- Responsibility #7 (`plain_language_dictionary.md`): "first Stage T invocation when not present... The skill writes a minimal header (status: live artefact, producer-mode, maintained by `/research-interpret translate` invocations) and an empty body table (one row per term: Dutch + English + source-scope note + date). Subsequent Stage T invocations load-and-append." Implementable as Read-or-Write idempotent at start of every Stage T invocation.

R1 above is on the race-condition between the two on first-ever-invocation-being-Stage-T.

The bootstrap pattern matches the limitations doc §8 worked-example pattern (the §8 table is manual-pending-skill; once the skill lands it walks the table; the same discipline applies here — once these files exist they live as producer-mode infrastructure per plan §4).

### Invention 7 — Skill-specific anti-patterns expanded 3 → 6

**Sound but worth fact-checking each addendum.** The three operational addenda beyond plan §7's named three:

- **Addendum #4 — Backdoor a §3.12 commentary into a higher tier or research-audience track.** Traceable to plan §3.12 hard separations (commentary cannot promote actionability tier; commentary cannot be cited downstream as analytical evidence; commentary cannot float unattached; FORBIDDEN in research-audience track). The skill's anti-pattern paragraph cites Stage A §5.9 + Stage T §5.11 as the only legal commentary venues + Stage T commentary as patient-audience track ONLY. **All four hard separations preserved.** Not new policy; consolidates plan §3.12 + guide #5 §6.4 + §7.7 + §7.8 + §7.9 + §7.14 + guide #6 §7.3 + §7.4 into a single anti-pattern reminder.

- **Addendum #5 — Skip the missing-inputs `open_inputs` entry when narrowing a claim (silent-narrowing fallacy per locked-plan §9).** Traceable to plan §9 "silent-narrowing fallacy" verbatim ("degrading a claim's wording to fit available inputs without producing an `open_inputs` entry that names what is missing and what claim it is blocking"). The skill's anti-pattern paragraph correctly carries the plan §9 framing — "Hedged wording without an accompanying `open_inputs` entry is forbidden." Not new policy.

- **Addendum #6 — Cross the producer / reviewer split.** Traceable to CONVENTIONS §1.2 verbatim ("After lock, the `/research-review` (or equivalent peer review) must run in a different session"). The skill's anti-pattern paragraph correctly carries the CONVENTIONS §1.2 framing — "Stage I / S₁ / S₂ / A / T artefacts are reviewer-mode-with-authorization; their fresh-session review must run in a different conversation." Not new policy; reframes CONVENTIONS §1.2 at the skill-execution layer.

**All three addenda trace back to existing rules.** No new policy invented; each addendum consolidates a rule that previously lived in plan §9 / plan §3.12 / CONVENTIONS §1.2 into the skill's anti-pattern enforcement surface. The 3 → 6 expansion is operationally appropriate because the original three were "what the skill must NOT do at the engine level" while the three new are "what the skill must NOT enable the user to do via interview cooperation" — a different enforcement layer.

## 5. Per-section findings

### §"Status + intro paragraphs" (lines 11-37)

Sound. The DRAFT r1 + producer-mode + NOT LOCKED status correctly carries the producer-mode-infrastructure framing per plan §4. The "awaiting (a) user acceptance, (b) skill-test dry-run per locked-plan §11 step 8, and (c) fresh-session `/research-methodology-review`" routing correctly identifies all three gates before lock (the user-acceptance + dry-run is required by plan §11 steps 8-9; the fresh-session methodology-review is required by plan §4 row "/research-interpret skill | Skill-test session: dry-run on one HA per guide" + the implicit CONVENTIONS §1.2 fresh-session discipline applied to methodology MDs).

The "skill is an engine, not a re-statement" framing + "If a discrepancy ever appears between this skill and a guide, the guide wins" is the right load-bearing discipline for the engine-vs-data separation. **Critical correctness check passes**: the skill cannot become the source of truth even by user-acceptance + drift; the guides are always primary.

### §"Invocation" (lines 39-94)

Sound. The `<stage> <target>` shape + the six `<stage>` arg values + the per-stage `<target>` semantics are all correctly mapped. The six examples cover all six stages. The `--drift-check` helper invocation is correctly factored out from the stage-invocation shape.

The Stage T `translate <source-path>` semantics ("the source's stage is inferred from the path") is the right operational shape but worth noting: the skill will need to recognise the path patterns `analyses/interpretation/`, `analyses/synthesis/`, `analyses/contextualisation/`, `analyses/actionability/` to infer stage. This is implementable as a simple path-prefix check, but the skill prose does not say so explicitly. Minor observation, not a fix.

### §"Six-stage routing table" (lines 96-110)

Sound per Invention 1 above. R2 above is on the Stage T row's skip-record location ambiguity.

### §"Skill responsibilities" (lines 112-237)

Sound per Faithfulness §3 above. R1 above is on responsibility #7's bootstrap-race; A2 above is on responsibility #11's §4.5 / §5.11 / §5.5 shorthand.

### §"Anti-patterns the skill must refuse" (lines 239-330)

Sound per Invention 7 above. The three categories (per-guide anti-patterns; layer-level anti-patterns; skill-specific anti-patterns) is the right three-tier enforcement structure. Each per-guide anti-pattern bullet cites the guide's §7 verbatim and links to it; spot-checking Stage A's bullet covers all the §7 items I sampled (§7.1 retrospective-as-predictive; §7.2 advice-form; §7.3 presence-conditioned-as-prevalence; §7.4 bare-percentage; §7.5 backdoor-predictive-wording; §7.6 inventing-new-caveats; §7.7 commentary-floats-unattached; §7.8 commentary-promotes-tier; §7.14 tier-3-commentary). The "the rest of §7" framing is slightly loose but operationally tolerable since each guide's full §7 is the authoritative source.

### §"Interview-engine pattern" (lines 332-417)

Sound per Invention 2 above. The seven phases are well-scoped. Phase 1 Load's fail-safe correctly inherits guide #1 §9.1's pattern. Phase 4 Interview's "Never silently fill a §9.4 'skill MUST NOT autonomously fill' field" correctly carries the §7 + per-guide §9.4 discipline. Phase 6 Refuse-to-lock gate's "names the unmet check with the guide-§-number, the specific section / wording / citation that fired it, and the remedy" is the right operational shape for the user-feedback surface.

### §"§3.6 map-conflict-resolution handling" (lines 419-439)

Sound per Faithfulness §3 above. The halt-and-route discipline is parallel to guide #3 §6.1 + guide #4 §6.1 + guide #5 §6.5 + guide #6 §6.6.

### §"§3.12 commentary discipline (cross-cutting)" (lines 441-471)

Sound per Invention 3 above. The §3.12 hard separation is preserved at three locations (Stage A §5.9 paragraph; Stage T patient §5.11 paragraph; Stage T research-audience FORBIDDEN paragraph). The closing paragraph correctly carries the load-bearing hard-separations as cross-cutting reminders.

### §"L-ID citation discipline" (lines 473-494)

Sound per Invention 4 above. All six rows match the limitations doc §5 verbatim.

### §"Cross-references" (lines 496-560)

Comprehensive. All cited paths verified:
- `_plan_results_analysis_layer.md` — exists at correct path, LOCKED r5 2026-06-24 ✓
- Six guides — all six verified to exist at correct paths, all LOCKED r2 2026-06-24 ✓
- `research_line_limitations.md` — exists, LOCKED r3 2026-06-23 ✓
- `synthesis_structure_map.md` — exists, LOCKED r3 2026-06-24 ✓
- `_open_inputs.md` — does NOT exist (per R1 above) ✓ (correctly listed under "Live artefacts the skill maintains" — i.e., to-be-scaffolded)
- `plain_language_dictionary.md` — does NOT exist (per R1 above) ✓ (same)
- `CONVENTIONS.md` — exists, sections §1 / §1.2 / §2.1 / §2.3 / §3 / §4.1-§4.3 correctly cited
- Adjacent skills: `.claude/commands/research-review.md` + `.claude/commands/research-methodology-review.md` + `.claude/commands/fetch-paper.md` — the path convention `.claude/commands/` is the right convention for slash-command skills per project structure (verified against `.claude/skills/superdesign/SKILL.md` which uses `.claude/skills/<name>/SKILL.md` — different pattern; commands are at `.claude/commands/`). **Verified consistent.**

### §"Lock log" (lines 562-566)

Per A3 above: 1,300-character paragraph. Content is correct (five named inventions; project-convention discoveries about superdesign/SKILL.md frontmatter). The discovery framing ("Project-convention discoveries: existing skill at `.claude/skills/superdesign/SKILL.md` uses YAML frontmatter (`name + description + metadata`) and follows the `.claude/skills/<name>/SKILL.md` path; `.claude/commands/<name>.md` uses simpler `description`-only frontmatter — this skill matches the SKILL.md shape per locked-plan §7's explicit path mandate") is the right precedent-citation pattern.

## 6. Cross-cutting concerns

### §3.12 patient-audience-ONLY commentary boundary (load-bearing review check)

**Strongly enforced; verified at three skill-engine touchpoints.** The boundary is operationalised at:

1. **Routing table Stage T row**: "commentary section per §3.12 is **patient-audience track only**" — preserves the hard separation at the routing-table surface.
2. **Cross-cutting §3.12 section**: explicitly enumerates the three propagation points (Stage A §5.9 attached-only; Stage T patient §5.11 rendered; Stage T research-audience FORBIDDEN), with the closing paragraph carrying the four hard separations (cannot promote tier; cannot be cited downstream; cannot float unattached; FORBIDDEN in research-audience track).
3. **Skill-specific anti-pattern #4**: explicitly forbids backdooring §3.12 commentary into higher tier or research-audience track, citing plan §3.12 hard separations verbatim.

No skill section permits commentary in research-audience track. The Stage T routing-table refusal-precondition does not mention commentary, but the §3.12 cross-cutting section + the anti-pattern #4 close the gap at the engine-execution layer. **The §3.12 patient-audience-ONLY hard separation holds at every touchpoint. Verified.**

### §3.10 hard predictive gate propagation (second load-bearing review check)

**Strongly enforced; no backdoors found.** The gate is preserved at three skill-engine touchpoints:

1. **Routing table Stage A row**: "**for tier-3 (predictive) reach**, a pre-registered forward-validation HA must exist in the registry with lock-date **before** the prediction-window start (locked-plan §3.10 hard predictive gate)" — preserves the gate at the routing-table surface as a refusal precondition.
2. **Skill-specific anti-pattern #2**: "Promote a tier in Stage A by force of argument. The hard predictive gate (locked-plan §3.10) is structural, not rhetorical. Tier-3 requires a registered forward-validation HA whose lock-date precedes the prediction-window start, full stop. No amount of user assertion (or guide-author intuition) unlocks it." — preserves the gate at the anti-pattern surface as a force-of-argument-block.
3. **Cross-cutting §3.12 section closing paragraph**: "Tier promotion requires forward-validation per §3.10, full stop." — preserves the gate at the commentary-cannot-be-the-backdoor surface.

**Verified.** The §3.10 hard predictive gate propagates without backdoor; the skill structurally refuses tier-3 without forward-validation HA at routing-table precondition time, and the skill cannot be talked into bypassing it via force-of-argument per anti-pattern #2, and the §3.12 commentary cannot be the backdoor per anti-pattern #4 + cross-cutting §3.12 closing.

### Refusal precondition implementability

Each stage's refusal precondition is checkable by file/state inspection:

- **Stage D**: existence-check on hypothesis.md + result.md + test.py — implementable as path-exists checks.
- **Stage I**: read audit's §4.4 verdict-trust call from the audit MD's header section — implementable as Read + simple text extraction (the audit's §4.4 has a fixed four-state label set).
- **Stage S₁**: existence-and-LOCKED check on every cluster-member interpretation + map §3 row presence + cascade-arrow upstream LOCKED — implementable as Read of map + per-HA interpretation file headers.
- **Stage S₂**: existence-and-LOCKED check on every constituent cluster + map §4 row presence + limitations doc existence — implementable as Read + status-line check.
- **Stage A**: existence-and-LOCKED check on every feeding topic + map §5 row presence + tier-aspiration check + for tier-3 a forward-validation HA registry check with lock-date < window-start — the last condition (lock-date comparison) requires the skill to read the HA pre-reg's lock-log + the forward-validation HA's prediction-window start date and compare timestamps. **Implementable but more complex than the other refusal preconditions; worth flagging.** A future skill-build session might want to factor this into a helper function.
- **Stage T**: existence-and-LOCKED check on source + limitations doc existence + dictionary existence-or-scaffolded under responsibility #7 — implementable. R2 above is on the skip-record location.

All refusal preconditions are operationally implementable. The Stage A tier-3 lock-date comparison is the most complex but is the load-bearing hard-predictive-gate enforcement; implementability is preserved.

### --drift-check helper specification

Implementable per A1 above's observations. The six concrete trigger-check mechanisms are operationally implementable as listed; the "etc." should be expanded to ~9-10 explicit trigger types (cascade-upstream re-examination for Stage S₁ cascade-downstream; layperson-test-fail for Stage A commentary-carrying + Stage T commentary-carrying; forward-validation HA new-verdict for Stage A; new-literature-of-moderate-or-higher-relevance for Stage S₂; methodology-MD-lock-version-bump for all stages).

### Bootstrap responsibilities — operationality check

Both bootstraps are operationally specified per Invention 6 above. The bootstrap patterns match guide #6 §9.1 (dictionary scaffold) + the limitations doc §8 worked-example pattern (manual-pending-skill discipline). R1 above is on the race-condition.

### Skill-as-engine vs guide-as-data separation

**No paraphrasing weakening found.** Spot-checking five §-numbered cross-references:

- Routing table Stage D row's "Per guide #1 §9.1 — `hypothesis.md`, `result.md`, `test.py` must all exist for the HA" — guide #1 §9.1 says verbatim "The skill MUST refuse to proceed if any of `hypothesis.md`, `result.md`, or `test.py` is missing." **No paraphrasing weakening.**
- Routing table Stage A row's "**for tier-3 (predictive) reach**, a pre-registered forward-validation HA must exist in the registry with lock-date **before** the prediction-window start (locked-plan §3.10 hard predictive gate)" — guide #5 §5.5 element 6 says verbatim "Pre-registration lock date — before the prediction window begins. The lock date is the anti-cherry-pick discipline at the tier-3 evidence floor." **No paraphrasing weakening.**
- Skill-specific anti-pattern #4's "§3.12 hard separations: commentary cannot promote actionability tier, cannot be cited downstream as analytical evidence, cannot float unattached, and is FORBIDDEN in research-audience track" — plan §3.12 says verbatim "Commentary cannot promote actionability tier... Commentary cannot be cited as evidence in HAs, interpretations, syntheses, contextualisations, or research-audience translations... Commentary cannot float unattached... Commentary is forbidden in research-audience translation track per the locked decision." **No paraphrasing weakening.**
- L-ID table topic row's "**MUST cite L1, L2, L4 unconditionally**; cite L3, L5, L6, L7 as they apply" — limitations doc r3 §5 says verbatim "**MUST cite L1, L2, L4 unconditionally** (every topic-level positioning sits inside the single-subject + era-stratified + analyst-is-subject envelope). Cite L3, L5, L6, L7 as they apply." **No paraphrasing weakening.**
- Phase 7 Acceptance + handoff's "On user explicit acceptance: Status header transitions DRAFT → LOCKED with a lock-log entry" — plan §3.8 says verbatim "'User explicitly accepts' is the binding event for completion. The skill marks an artefact as 'ready for completion review' when its checklist is fully ticked or fully open-inputs-logged, but it never auto-completes. The user's acceptance is the lock event." **No paraphrasing weakening.**

**No section duplicates guide content; every cross-reference is a faithful pointer.** The 566-line skill vs ~9,300 lines of guide corpus ratio is operationally appropriate.

### Frontmatter discoverability

**Confirmed via system-reminder evidence.** The system reminder's available-skills list includes "research-interpret: Interview-engine skill operationalising the six LOCKED methodology guides (descriptive_precondition_audit, verdict_to_inference, internal_synthesis, external_contextualisation, actionability_translation, translation_to_audience) across stages D / I / S1 / S2 / A / T. Loads the relevant guide MD as data and walks the user through that stage's procedure. Use when drafting any results-analysis-layer artefact under `docs/research/analyses/{descriptive,interpretation,synthesis,contextualisation,actionability,translation}/`. Refuses on dependency-gate failures; never edits guide MDs in-session." This matches the SKILL.md frontmatter `description` field verbatim. The frontmatter shape (`name + description + metadata{author,version}`) matches the sibling `superdesign/SKILL.md` convention verbatim. **Discoverability confirmed.**

### Producer/reviewer-split routing in responsibility #8

**Correctly routed.** Responsibility #8 distinguishes:
- Stage D (`descriptive_audit.md`): producer-mode; no fresh-session review; user explicit acceptance = lock event.
- Stages I / S₁ / S₂ / A / T (reviewer-mode-with-authorization artefacts): fresh-session `/research-review` required (NOT `/research-methodology-review`).
- Stage T patient-audience track: additional layperson-test gate.

Cross-referenced against locked plan §4 producer/reviewer-split table + §11 intro discipline-gate routing:
- Guide MDs (6×) → `/research-methodology-review` ✓ (the skill itself, when it goes for review, falls into this category — correctly reflected in §"Adjacent skills")
- `synthesis_structure_map.md` → `/research-methodology-review` ✓
- `research_line_limitations.md` → `/research-methodology-review` ✓
- `descriptive_audit.md` (per HA) → no fresh-session review ✓
- `interpretation.md` (per HA) → `/research-review` ✓
- `cluster-*.md` synthesis → `/research-review` ✓
- `topic-*.md` contextualisation → `/research-review` ✓
- Actionability tier claims → `/research-review` (with tier-downgrades-on-review-concerns) ✓
- Translation artefacts → `/research-review` plus layperson-test where patient-audience track exists ✓

**All seven routing rows correctly mapped. Verified.**

### Step-8 dry-run readiness on HA-C4

Concretely: if a user invokes `/research-interpret descriptive HA-C4` tomorrow, what would they hit that the skill doesn't answer?

Spot-walking the seven phases on HA-C4 (assuming HA-C4 has `hypothesis.md`, `result.md`, `test.py` at `docs/research/analyses/hypotheses/HA-C4/`):

- **Phase 1 Load**: skill loads HA-C4's hypothesis + result + test.py + cited methodology MDs + stocktake's HA-C4 row (if present) + candidate descriptive artefacts. The "HA-C4" naming is ambiguous against the registry — there is "HA-C4" the parent HA + "HA-C4 v1" + "HA-C4 v2" + "HA-C4c" + "HA-C4b" + variants. The skill prose says the `<target>` is "the HA ID (e.g. `HA-C4c`)" but does not specify what happens if the user passes the parent ID (`HA-C4`) when only the v2 + v1 + v2c variants exist. **Minor gap but operationally tolerable** because the skill can interview the user about which revision is the target.
- **Phase 2 Gate**: HA-C4 has hypothesis.md + result.md + test.py — Gate passes. The skill does not refuse on file existence.
- **Phase 3 Extract**: skill extracts assumption list from test.py + pre-reg + methodology cites. Stocktake's HA-C4 row precedent provides starting point.
- **Phase 4 Interview**: skill walks guide #1 §8 seeds — §8.1 (assumption identification), §8.2 (per-assumption coverage check), §8.3 (post-hoc contamination check), §8.4 (verdict-trust audit confirmation).
- **Phase 5 Produce**: skill drafts `analyses/descriptive/HA-C4/descriptive_audit.md` (or `HA-C4 v2` or `HA-C4c` depending on revision target).
- **Phase 6 Refuse-to-lock gate**: skill walks guide #1 §9.6 fire-list — but guide #1 §9.5 lists the "Refuse-to-mark-TRUSTED gate" only; there is no §9.6 in guide #1 (guide #1's §9 has §9.1 through §9.6 — verified the §9.6 in guide #1 is "Acceptance + drift-trigger registration", not the refuse-to-lock gate). **The skill prose Phase 6 says "walks the guide's §9.6 fire-list item-by-item" but for guide #1 the equivalent is §9.5 Refuse-to-mark-TRUSTED gate.** Minor §-number ambiguity (Phase 6 is correct conceptually but the §9.6 cite is wrong for guide #1 specifically; for guides #2-#6 the §9.6 IS the Refuse-to-lock gate). Worth a one-sentence parenthetical "(§9.5 for guide #1's Refuse-to-mark-TRUSTED gate; §9.6 for guides #2-#6's Refuse-to-lock gate)".
- **Phase 7 Acceptance + handoff**: user acceptance triggers DRAFT → LOCKED + `_open_inputs.md` propagation + drift-trigger registration. For Stage D specifically, no fresh-session `/research-review` per responsibility #8.

**Most likely step-8 dry-run friction:** (a) the HA-C4 vs HA-C4 v2 vs HA-C4c naming ambiguity at `<target>` parsing time; (b) the bootstrap-on-first-invocation of `_open_inputs.md` (responsibility #6 — should fire on Phase 7 lock-event); (c) the §9.5-vs-§9.6 numbering for guide #1 at Phase 6.

None of these block the dry-run; all are recoverable in-session by user interview or skill clarification. R1 above is the only operational blocker, and it does not fire for Stage D (only Stage T touches `plain_language_dictionary.md`).

## 7. Required actions for revision

1. **R1: Resolve bootstrap race-condition between responsibility #6 and responsibility #7.** Add one sentence to responsibility #7: "If `_open_inputs.md` is also missing (i.e., this is the first ever invocation of any stage), responsibility #6's `_open_inputs.md` scaffold runs FIRST, so the dictionary's bootstrap can itself append an `open_inputs` entry if the bootstrap encounters a partial-scaffold state." Optionally also note in responsibility #6 that "the scaffold runs before any other phase, including before responsibility #7's dictionary scaffold." Closes the race condition for first-Stage-T-as-first-invocation. **Not blocking for step 8 (only Stage T touches the dictionary); blocks step 9.**

2. **R2: Tighten the Stage T routing table row + responsibility #2 on the skip-research-internal record location.** One-sentence fix in the Stage T row: "The skip-record lives at the source artefact's §10 / §4.10 cross-references section (per guide #6 §3); the skill reads it from there before refusing on missing patient-audience-only output." Closes the routing ambiguity. **Not blocking for step 8.**

## 8. Recommended actions

1. **A1: Expand `--drift-check` helper trigger-type enumeration.** The "etc." at the end of the six trigger-type list should expand to ~9-10 explicit trigger types (cascade-upstream re-examination for Stage S₁ cascade-downstream; layperson-test-fail for Stage A commentary-carrying + Stage T commentary-carrying; forward-validation HA new-verdict for Stage A; new-literature-of-moderate-or-higher-relevance for Stage S₂; methodology-MD-lock-version-bump for all stages). Not blocking.

2. **A2: Tighten responsibility #11's citation-block location shorthand.** Add parentheticals "(specifically the 5b L-ID sub-block where applicable)" for Stage I §4.5 + Stage S₁ §4.5 increment targets. Not blocking.

3. **A3: §11 lock log scannability.** Split the single 1,300-character paragraph into two-or-three short paragraphs (one for the seven inventions; one for the §7-faithfulness traceability; one for the discovery about superdesign/SKILL.md frontmatter convention). Same A4-class observation flagged in guides #4, #5, #6 r1 reviews; remains optional refinement.

4. **A4 (optional, lifts PARTIAL → PASS on input #3):** Add an "Alternatives considered" paragraph at the §"Status + intro paragraphs" section closing, naming the foreclosed alternatives (multiple per-stage skills; separate `--drift-check` skill; per-stage interview-engines) and citing the plan §2 locked decisions that foreclose them. Optional refinement; the four-input bar PARTIAL is operationally tolerable for a producer-mode infrastructure MD whose spec is fully pinned by plan §7.

## 9. Summary verdict

**REVISION RECOMMENDED (mild).** Two required fixes (R1: bootstrap race-condition; R2: Stage T skip-record location); three (or four with optional A4) recommended refinements. None blocks §11 step 8 dry-run on HA-C4 (R1 fires only for Stage T which is step 9; R2 is for Stage T routing). The skill is structurally faithful to plan §7 across all eight §7 elements + the three "what the skill must NOT do" prohibitions. The seven inventions beyond §7 are each faithfully traceable to per-guide §9 outlines or to plan §3.12 / §9 / CONVENTIONS §1.2; none invents new policy. The §3.12 patient-audience-ONLY commentary boundary holds at three skill-engine touchpoints; the §3.10 hard predictive gate propagates without backdoor at three skill-engine touchpoints; the L-ID citation discipline table matches the limitations doc r3 §5 row-by-row with no paraphrasing weakening; the producer/reviewer-split routing in responsibility #8 correctly maps all seven artefact types to the right review skill. The frontmatter discoverability is confirmed via system-reminder evidence — the skill's description renders coherently in the available-skills surface. **The skill-doesn't-weaken-guide check passes**: spot-checking five §-numbered cross-references found no paraphrasing weakening; the engine-vs-data separation is operationally maintained. The skill is ready for §11 step 8 dry-run on HA-C4 after R1 (optional for step 8) + R2 (optional for step 8) absorption; the §11 step 9 translation dry-run requires R1 absorption to avoid first-Stage-T-as-first-invocation bootstrap race.

---

*Review report drafted by Claude under fresh-session-reviewer discipline per CONVENTIONS §1.2. Target was read in full; no edits made to target per reviewer-mode rule.*
