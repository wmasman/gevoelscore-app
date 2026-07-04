# Methodology review — descriptive_precondition_audit.md (r1, 2026-06-24)

**Reviewer mode**: fresh-session peer review. Reviewer is independent of the drafting session. Fresh session — no exposure to the drafting context; doc-only knowledge.
**Target**: [`docs/research/methodology/descriptive_precondition_audit.md`](../methodology/descriptive_precondition_audit.md) (r1, 2026-06-24)
**Review date**: 2026-06-24
**Standards applied**: [CONVENTIONS](../CONVENTIONS.md) §1.2, §2.2, §3, §4; [plan](../methodology/_plan_results_analysis_layer.md) §6.1 spec; locked layer rules (plan §3.5, §3.7, §3.8, §3.9, §3.10, §3.12); [limitations doc](../methodology/research_line_limitations.md) r3; [synthesis map](../methodology/synthesis_structure_map.md) r3; [stocktake](../methodology/_descriptive_stocktake_2026-06-23.md).

## 1. Overall verdict

**REVISION RECOMMENDED.** The draft is structurally faithful to plan §6.1, implements all eight bullets in order, and adds five inventions that — with one substantive exception — are methodologically sound and operationally implementable. The §6.1 checklist faithfulness to the five cited methodology MDs is good (no misquotations found). The §5 checklist's operational tests track the cited MDs accurately, the §7 anti-patterns are distinct from upstream §9 plan anti-patterns, and the §9 phased agent-instruction outline is concrete enough that the §11 step 7 skill builder will know what to encode.

Three findings drive the REVISION RECOMMENDED verdict rather than ACCEPT. (a) The optional figures subfolder at §3 collides with the *de facto* existing convention `analyses/descriptive/*/plots/` (every existing descriptive analysis uses `plots/`, not `figures/`) — naming the audit subfolder differently from sibling descriptive analyses introduces avoidable inconsistency. (b) The §2 inputs paragraph mis-cites the limitations doc's §5 verbatim ("Cite L5 and L7 explicitly...") but then says the audit "does not cite L-IDs" — these two claims are in direct tension, and the draft does not resolve them. (c) The fourth verdict-trust label "STRUCTURALLY UNTESTABLE AS CURRENTLY SPECIFIED" is methodologically sound but its routing instructions create a small inconsistency: §4.4 says "exactly one of three labels," then §6.2 introduces the fourth, then §6.2 says "the audit terminates at §4 with no §4.5 open_inputs entry" — but §4.5 is required-per-spec for every audit and is also a §3.5 plan-level binding rule. None of the three blocks lock; all three are one-revision-cycle fixes.

## 2. Four-input bar findings (CONVENTIONS §2.2)

This MD is producer-mode infrastructure (per §3 of the target) rather than a methodology MD locking a substantive analytical choice; the four-input bar applies in lighter form. Two of the four inputs apply directly; two apply indirectly.

| Input | Status | Reasoning |
|---|---|---|
| 1. Best-practices standards | PASS | The audit shape (load-bearing-assumption enumeration, per-assumption status, gating verdict-trust call) is the standard "pre-publication checklist" pattern in observational-research methodology (STROBE §12-§13 limitations + missingness reporting; CENT item 21). The §7.3 post-hoc contamination check tracks the same discipline. |
| 2. Established literature | PARTIAL | No external citations in the body of the draft; this is acceptable because the binding sources are the five project-internal methodology MDs the §5 checklist cites + CONVENTIONS. The §10 cross-references do name the Daza / SCRIBE / CENT / STROBE PDFs but the body of the guide does not use them. Defensible for a project-internal procedure MD; a one-sentence locator in §1 saying "the guide's discipline traces to STROBE §13's missingness + §16's confounders reporting, and CENT item 21's N-of-1 limitations expectation" would tighten it. |
| 3. Tradeoff vision | PARTIAL | The draft does not explicitly enumerate alternatives considered (which is the typical signal of "tradeoff vision" in this folder's methodology MDs). It does, however, take a clear position on at least three judgment calls — verdict-trust is independent of verdict label (§6.4), L-ID citation lives at Stage I not Stage D (§5.5 + §10 cross-ref), commentary about audit lives in the audit not in Stage I (§7.4). An "alternatives considered" paragraph in §1 or §2 would tighten the four-input compliance; the silence-in-the-text on what was considered and rejected is the gap. |
| 4. Research limitations + objectives | PASS | The draft is built around the stocktake's actual gap distribution (4 ready, 24 NOT-BACKSTOPPED on shared-gap-1/2/3, 2 structurally untestable). The §5 checklist matches the eight-cell stocktake matrix. The §6.2 "data does not exist" pathway maps directly to the H03b precedent. Designed-for-this-corpus is unambiguous. |

Overall: 2 PASS, 2 PARTIAL. The PARTIALs are defensible for a producer-mode procedure MD, but flagging them as Recommended-action items below.

## 3. Faithfulness to §6.1 spec

§6.1 has eight required elements. Mapping:

| §6.1 element | Implementation | Faithfulness |
|---|---|---|
| Purpose | §1 (purpose + where it sits + what it does not do) | **Faithful with extension.** The extension is the "what Stage D does NOT do" paragraph (commentary / predictive measures / post-hoc caveats), which is helpful scope-clarification. Sound. |
| Inputs | §2 (six numbered inputs) | **Faithful with extension.** §6.1 names four inputs (hypothesis.md, result.md, methodology MDs, descriptive artefacts + test.py). §2 expands to six by separating hypothesis.md from result.md and by adding the stocktake as input #6. Both extensions are sound and stocktake-as-input is exactly the §6.3 precedent the draft also invents — these reinforce one another. |
| Output | §3 (path + folder convention + naming + optional figures subfolder + mode) | **Faithful with extension.** §6.1 specifies `analyses/descriptive/HA-XX/descriptive_audit.md` and the optional `figures/` subfolder verbatim from the spec. The four expansions (folder-naming convention, file-naming convention, mode) are sound. **One naming-collision concern with the existing `plots/` convention — see §6 below.** |
| Section outline | §4 (5 sections) | **Faithful.** §6.1 names 5 sections; §4 implements all 5 in the spec'd order. The "open_inputs block" is correctly numbered §4.5 mapping to §6.1's bullet 5. |
| Checklist | §5 (8 items A1-A8) | **Faithful with extension.** All 8 §6.1 checklist items are present in the same order. Each gets binding doc + operational test + worked examples ("BACKSTOPPED looks like" / "NOT BACKSTOPPED looks like" / "NOT APPLICABLE looks like") — this expansion is the right operationalisation of the spec sketch. §5.9 "optional HA-specific rows" is a clean extension. |
| Conflict rules | §6 (4 rules) | **Faithful with extension.** §6.1 names 2 conflict rules; §6 implements both (§6.1, §6.2) and adds two more (§6.3 audit-vs-stocktake; §6.4 verdict-trust-independent-of-verdict-label). Extensions evaluated under §4 below. |
| Anti-patterns | §7 (7 anti-patterns) | **Faithful with extension.** §6.1 names 3 anti-patterns; §7 implements all 3 (§7.1, §7.2, §7.3) and adds 4 more (§7.4-§7.7). Extensions evaluated under §4 below. |
| Interview-prompt seeds | §8 (3 required + 1 optional) | **Faithful with extension.** §6.1 names 3 seeds; §8 implements all 3 (§8.1, §8.2, §8.3) and adds §8.4 (optional verdict-trust confirmation seed). Extension sound and operationally cheap. |
| Agent-instruction outline | §9 (6 phases) | **Faithful with extension.** §6.1 names 4 bullets (Load / Extract / Walk / Produce / Refuse). §9 expands to 6 phases (Load / Extract / Interview / Produce / Refuse-gate / Acceptance+drift). The Acceptance+drift phase implements §3.7 + §3.8 rules absent from §6.1's outline; this is correct because those plan rules post-date §6.1's sketch. |

No §6.1 element is missing or substantively altered. Spec faithfulness is high.

## 4. The five inventions beyond §6.1

### Invention 1 — Fourth verdict-trust label "STRUCTURALLY UNTESTABLE AS CURRENTLY SPECIFIED" (§4.4 routing rule + §6.2 three-pathway expansion)

**Sound, with one operational inconsistency to fix.**

Methodologically sound. The plan §6.1 says "structurally untestable as currently specified" is routed back to pre-reg revision but does not name a label; the draft names one and threads it through §4.4 + §6.2 + §9.5. The three sub-pathways (pre-reg revision, retire, shelve-blocked-by-dependency) are well-grounded in the stocktake's §9 user decisions (H03b RETIRED, S02b SHELVED-BLOCKED-BY-S02, H05 RETIRED).

Operational inconsistency: §4.4 says "exactly one of three labels" — then immediately after, names the fourth as a "separate routing." This is read-friendly but structurally awkward. Cleanest revision: §4.4 should say "exactly one of FOUR labels" and list all four with their downstream consequences, OR keep three labels and explicitly route "structurally untestable" as a Stage-D-terminates-and-routes-elsewhere event without a verdict-trust label. The current draft mixes the two presentations.

Second concern: §6.2 says "the audit terminates at §4 with no §4.5 open_inputs entry." But §4.5 is plan §3.5-mandated for every audit (§3.5 hard rule: "every refusal-to-proceed in this layer is not to block work; it is to make the missing-input pathway productive"). A structurally-untestable HA is exactly the case where the missing input *is* "a revised pre-reg" or "an unblocking upstream artefact" — that should be an `open_inputs` entry routing to a pre-reg-revision producer-mode session, not absence-of-entry. The §3.5 hard rule does not exempt structurally-untestable cases.

### Invention 2 — §6.3 audit-disagrees-with-stocktake conflict rule

**Sound.** Useful and operationally implementable. The rule preserves the stocktake as a precedent but allows revision when a new descriptive artefact lands between stocktake (2026-06-23) and audit time. The "one-sentence diff against the stocktake" requirement is concrete and lightweight. No conflicts with upstream rules.

One small refinement: the rule says revisions appear in "§4 of the audit" but §4 is "Verdict-trust call." A diff against the stocktake's `B / N / /` assignment belongs in §3 (per-assumption status) where that assignment lives. Suggest: revise §6.3 to say "MUST appear in §3 of the audit (the per-assumption status section) with a one-sentence diff against the stocktake's matrix row."

### Invention 3 — §6.4 verdict-trust independent of verdict-label

**Sound and operationally important.** This invention catches the most common failure mode of an audit that mixes "trust the audit" with "trust the result" — a REJECTED verdict whose block-length is unbacked is still REJECTED but is not TRUSTED; a SUPPORTED whose block-length is unbacked is downgraded to PROVISIONAL. The draft's framing ("the audit does NOT preferentially trust REJECTED over SUPPORTED or vice versa; it audits assumptions, not conclusions") is exactly right and is the right defence against the §7.4 anti-pattern.

This invention is non-trivially different from anything §6.1 contemplates and is one of the strongest additions in the draft.

### Inventions 4 — Four added anti-patterns §7.4-§7.7

**Three sound, one cuttable.** Per-item:

- **§7.4 — Re-interpreting the verdict in the audit.** **Sound.** Distinct from §6.1's three. Distinct from upstream plan §9 anti-patterns (the "verdict-as-finding fallacy" is about *Stage I* skipping; this is about *Stage D* over-reaching into Stage I's territory). The right defence for §6.4's verdict-trust-independent-of-verdict-label rule.
- **§7.5 — Silent assumption-list editing.** **Sound.** Distinct from §6.1's three. Distinct from upstream plan §9. The "prose-vs-code drift surfacing" requirement maps cleanly to §9.2's "extract" phase and §8.1's first interview seed.
- **§7.6 — Marking TRUSTED to avoid blocking Stage I.** **Sound.** Distinct from §6.1's three. This anti-pattern is what §9.5's skill-level refuse-gate enforces; naming it as anti-pattern at the guide level + as refusal at the skill level is the right belt-and-suspenders discipline.
- **§7.7 — Citing the limitations doc instead of producing the backstop.** **Sound but mostly redundant with §7.1.** "L7 — survivorship per limitations doc" cited as A2 BACKSTOPPED is structurally identical to §7.1's "the test ran, therefore the assumptions held" — both are circular-citation patterns where a non-descriptive artefact is cited as descriptive backing. The §7.7 framing does add the specific L-ID-vs-descriptive distinction which is useful for clarity, but it could be a one-paragraph subnote under §7.1 rather than a full anti-pattern slot. Not load-bearing to keep separate; not load-bearing to merge. The draft can keep it as-is or merge.

### Invention 5 — Phased agent-instruction breakdown at §9

**Sound.** The six phases (Load / Extract / Interview / Produce / Refuse-gate / Acceptance+drift-trigger registration) are concrete enough that the §11 step 7 skill builder will know what to encode. The Acceptance+drift phase correctly implements both §3.7 (drift triggers) and §3.8 (user-acceptance-as-lock) which post-date §6.1's outline; the four-bullet §6.1 sketch would have been incomplete without it.

One operational gap: §9.1 names what the skill loads but does not name what it does if a candidate descriptive artefact under `analyses/descriptive/` matches a stocktake-precedent path but the path no longer exists (artefact moved or renamed). The skill should fail-safe to NOT BACKSTOPPED with an open_inputs entry naming "stocktake-cited artefact at [path] not found; verify path or re-run the artefact"; the draft does not say this.

## 5. Per-section findings

### §1 Purpose

Sound. The "where Stage D sits in the layer" diagram-paragraph and the "what Stage D does NOT do" framing are both helpful. The block-quote framing ("Before any interpretation is built on a verdict, prove the verdict's load-bearing assumptions held") echoes plan §6.1's opening exactly.

### §2 Inputs

Sound with one tension. The six numbered inputs are right. Input #3 names the five binding methodology MDs explicitly which is a good operationalisation of §6.1's "methodology MDs the hypothesis cites."

**Concern.** The closing paragraph reads: *"The audit MAY also use the layer-level `research_line_limitations.md` to inform which L-IDs Stage I will need to cite, but the audit itself does not cite L-IDs (per §5 of that MD: 'Cite L5 and L7 explicitly where the audit's checklist depends on them' — see §5.5 + §5.7 below for the structural points where L-IDs surface in the audit's own reasoning)."*

The limitations doc §5 table actually says: *"`descriptive_audit.md` | Cite L5 and L7 explicitly where the audit's checklist depends on them."* That is a citation **requirement** on the audit, not an opt-out. The draft's framing ("the audit itself does not cite L-IDs") contradicts what it quotes from the limitations doc on the same sentence. Either the limitations doc's §5 row was misread, or the audit guide is overruling it without saying so. **Required to resolve.**

The cleanest fix: align with the limitations doc — the audit DOES cite L5 in §5.5 v24 rows where v24 is present and L7 in §5.1 + §5.2 sample-size and missingness rows where they apply. The §10 cross-ref table already names this binding correctly; the §2 paragraph contradicts itself and the cross-ref.

### §3 Output

Sound on the artefact path + naming + mode. **Two concerns on figures.**

**Concern 1 (naming collision).** The draft specifies `analyses/descriptive/HA-XX/figures/` for the optional figures subfolder. Every existing descriptive analysis in the corpus uses `plots/` (verified at `analyses/descriptive/operationalisation_support/stress_mean_sleep/plots/`, `analyses/descriptive/trajectory/recovery_arc/plots/`). Introducing `figures/` for Stage D audits while siblings use `plots/` produces avoidable inconsistency in the same `analyses/descriptive/` tree. Recommend: rename to `plots/` to match existing convention, or explicitly note in §3 why `figures/` is the right name for audit-class supporting visuals while sibling descriptive runs use `plots/`. Either is defensible; silence on the choice is not.

**Concern 2 (provenance).** The §10 cross-ref table's literature anchors block (the four PDF paths) is well-anchored, but the draft does not say whether Stage D audits — which "MAY accumulate supporting plots" — are subject to the audit-before-push privacy gate (CONVENTIONS §2.3). Almost certainly yes (anything under `analyses/` is in scope), but worth a one-line confirmation under §3 or §11.

### §4 Section outline for the produced descriptive_audit.md

Sound. Five sub-sections, all faithful to §6.1. The "Hard rule on the BACKSTOPPED label" in §4.3 explicitly disqualifies citing the test's own result as backstop — this enforces §7.1 at the spec level, not just at the anti-pattern level. Good belt-and-suspenders.

**One concern on §4.4.** As named in §1 of this report, the "exactly one of three labels" framing is in tension with the §6.2 fourth label. Either §4.4 lists four labels with §6.2 explaining the fourth's routing, or the fourth label routes Stage D to terminate-and-route-elsewhere rather than carrying a label. Currently the draft does both, which produces operational ambiguity.

### §5 Load-bearing-assumption checklist

This is the strongest section of the draft. The eight items A1-A8 match §6.1 verbatim in order, each is bound to a specific methodology MD, and each carries a one-sentence operational test plus worked examples.

**Faithfulness to cited MDs:**

- **A1 sample size (§5.1)** — sound. The "INCONCLUSIVE-aware routing IS the backstop" framing correctly reads HA-C4 v2 §5.3 design.
- **A2 missingness (§5.2)** — sound. The three operational paths (pre-reg documents missingness handling; descriptive artefact has rate readout; gating mechanism is the missingness handler) cover the cases. The MD-binding cell honestly says "No single project-internal methodology MD covers missingness universally" — accurate.
- **A3 block-length (§5.3)** — faithful to [`permutation_null_block_length.md`](../methodology/permutation_null_block_length.md). The MD specifies stationary bootstrap E[L]=7 as project-wide default + data-driven E[L]\* confirmation + factor-of-2 deviation flag (verified at MD §"Decision"). The "BACKSTOPPED partial" framing for derivative channels (per-night delta, per-night σ, slope) is honest acknowledgment that ACF on the upstream channel may not characterise the derivative — this matches the stocktake §7's note on B partial usage. Operational test is accurate.
- **A4 era / Stratum-4 (§5.4)** — faithful to [`lc_era_temporal_segmentation.md`](../methodology/lc_era_temporal_segmentation.md). Stratum 4 as primary; M1/M2/M3 warrant per §6 of that MD; cross-phase pooling cites [`phase_axis_collapsibility_conventions.md`](../methodology/phase_axis_collapsibility_conventions.md). The historical 2023-12-31 split note for H/HA01-11 family correctly cross-references stocktake §3 Shared gap 2. Accurate.
- **A5 v24 (§5.5)** — faithful to [`symptom_mention_asymmetry.md`](../methodology/symptom_mention_asymmetry.md). Forbidden-use list (no prevalence claim, no absence-as-evidence), companion-flag gating (`has_note=True`, `intensity_source != ""`), caveat-class usage binding all correctly drawn from the MD's "right vs wrong use" worked examples. Accurate. Also includes the L5 surface paragraph which conflicts with §2 ("does not cite L-IDs") and must be reconciled.
- **A6 nightly attribution (§5.6)** — faithful to [`nightly_attribution.md`](../methodology/nightly_attribution.md). Wake-up-date convention; no date shifting at build script; per-HA `sleep_valid_flag` use the verifiable requirement. Accurate. The NOT APPLICABLE case (daytime-only) correctly matches the MD.
- **A7 effect-size (§5.7)** — sound. The binding is CONVENTIONS §2.1 + project-standing pre-reg discipline (which is real and binding even though it doesn't live in a single MD). The "result-data.json re-extraction" closure path is realistic.
- **A8 split-fate (§5.8)** — faithful to [`train_validate_split_fate.md`](../methodology/train_validate_split_fate.md). The 2026-06-13 lock date, single-pool primary, M3 sensitivity overlay, the historical-pre-reg cross-check queued exercise — all match the MD's §5 operational consequences. Accurate. The "narrows confidence, not blocks Stage I" framing for historical HAs correctly preserves stocktake §3 Shared gap 2's binding.

§5.9 Optional HA-specific rows is sound; explicit cross-references to `phase_axis_collapsibility_conventions.md`, `lc_recovery_phase_axis.md`, and `bout_level_recovery_dynamics.md` make the extension auditable.

### §6 Conflict rules

§6.1 + §6.2 are §6.1 spec items, implemented faithfully. §6.3 + §6.4 are inventions, evaluated under §4 of this report (sound).

**One small concern on §6.1 (descriptive-contradicts):** the second of three resolution paths is "New operationalisation pre-reg... the HA is superseded by a sister HA whose operationalisation respects the assumption (e.g. HA-C3 v1 → v2 absorbed a B4-absorber pre-commit)." HA-C3 v1 → v2 was an iteration on the SAME HA after a HALT, not the spawning of a sister HA. The cited example is misleading; HA-C3 v2 + HA-C3p (the personal-baseline sister) is the cleaner sister-HA example. Recommend swapping the example.

### §7 Anti-patterns

§7.1, §7.2, §7.3 are §6.1 spec, implemented faithfully (§7.3 in particular has the lock-date-discriminator language that operationalises "post-hoc and peeking" cleanly). §7.4-§7.7 are inventions, evaluated under §4 (three sound, one cuttable-or-mergeable).

### §8 Interview-prompt seeds

§8.1, §8.2, §8.3 are §6.1 spec, implemented faithfully. §8.4 is an extension (verdict-trust confirmation), evaluated under §4 (sound).

### §9 Agent-instruction outline

§9.1-§9.5 implement §6.1's four-bullet outline; §9.6 is the §3.7 + §3.8 extension, evaluated under §4 (sound).

**Operational gaps:**

- §9.1 does not specify what the skill does if a stocktake-cited descriptive artefact path no longer exists at load time (named under §4 above).
- §9.6 says "the skill registers two re-examination triggers at lock time — underlying HA's result.md re-runs, OR a cited methodology MD changes lock-version." This is correct per plan §3.7 table but the mechanism of how triggers are registered (a row in the audit's lock log? a separate trigger registry?) is undefined. Plan §3.7's cadence-check is meant to surface these but the registration mechanism is not yet built. **The limitations doc §8 "downstream-citation-count" tracking is currently manual per the explicit "until the skill lands, the table is maintained manually" note in that doc.** §9.6 here would inherit the same manual-pending-skill status; suggest naming this explicitly so the next agent does not expect an automated mechanism that does not exist.

### §10 Cross-references

Spot-checked links:

- `_plan_results_analysis_layer.md` § references (6.1, 3.5, 3.7, 3.8, 11) — all exist in the plan (verified).
- `_descriptive_stocktake_2026-06-23.md` § references (4, 3, 9) — all exist in the stocktake (verified).
- `synthesis_structure_map.md` — exists, r3 LOCKED 2026-06-24 (verified).
- `research_line_limitations.md` — exists, r3 LOCKED 2026-06-23 (verified).
- The five §5-anchor MDs — all exist (verified via Glob).
- `phase_axis_collapsibility_conventions.md`, `citalopram_phase_stratification.md`, `lc_recovery_phase_axis.md`, `bout_level_recovery_dynamics.md` — all exist (verified).
- `hypothesis_lock_process.md` — exists.
- Literature methodology PDFs — paths look correct relative to the methodology folder (`../literature/methodology/`).

The cross-reference layer is in good shape; no broken links found in the spot-check.

### §11 Lock log

Sound. Single entry recording the r1 draft + the next gate (user acceptance + fresh-session methodology-review). Matches the pattern used by `research_line_limitations.md` and `synthesis_structure_map.md`.

## 6. Cross-cutting concerns

### Stocktake matrix precedent framing

The draft frames the stocktake's per-HA matrix (30 HAs × 8 assumptions ≈ 240 cells, per stocktake §1) as the **precedent run** of the §5 checklist. This framing is accurate: the stocktake §2 column legend is identical to the §5 checklist labels (A1-A8 sample/missingness/block-length/era/v24/nightly/effect-size/split-fate). The §6.3 audit-disagrees-with-stocktake rule correctly positions the stocktake as a precedent that the audit may revise.

**One small caveat the draft does not flag.** Stocktake §7 explicitly says: *"This stocktake uses B partial liberally to keep the gap list focused on the structural gaps rather than enumerating every derivative."* So the stocktake's B-partial cells are not strict reads. The draft's §6.3 should note that strict-reading B-partial cells are a known case where audits may revise the stocktake's assignment — this is what the stocktake itself acknowledges. The draft alludes to it ("a stocktake-B row was generous on a derivative-specific point the strict reading would mark partial") but does not cite stocktake §7 explicitly. Minor.

### PROVISIONAL → Stage-I unblock consistency

The user-accepted policy is: PROVISIONAL unblocks Stage I under explicit user acceptance of the PROVISIONAL flag. The draft implements this consistently across:

- §4.4 ("Stage I MAY proceed under explicit user acceptance of the PROVISIONAL flag")
- §6 (§6.1 resolution path 3 "User accepts narrower claim... Stage I artefact carries the PROVISIONAL marker")
- §9.6 ("PROVISIONAL unblocks under explicit user acceptance of the flag")

This is consistently named. The "explicit user acceptance" gate is named identically in all three places. A future Stage I drafter reading the draft will see the same rule three times and route correctly.

**Minor refinement:** §4.4 says "the expected path is to close the descriptive gap first; PROVISIONAL is the fallback when the user accepts the inference under explicit narrower-claim discipline." The "narrower-claim discipline" phrasing could be tightened by cross-referencing plan §3.5's "always at most one tier narrower than the claim being blocked" rule. As written, "narrower-claim discipline" is hand-wavy; cross-referencing §3.5 makes it concrete.

### L-ID integration

The draft is internally inconsistent on L-ID citation as flagged in §5 above. Two readings of the limitations doc §5 row are possible:

(a) The audit MUST cite L5 + L7 in the rows where they apply (the limitations doc §5 row reads as a binding rule on Stage D).

(b) The audit MAY note where Stage I will need to cite L-IDs but does not cite them itself (the draft's §2 paragraph + §5.5 "L-ID surface" framing).

Reading (a) is what the limitations doc says verbatim ("Cite L5 and L7 explicitly..."). Reading (b) is the draft's §2 + §5.5 framing.

The draft must pick one and apply it consistently. Reading (a) is the cleaner default (the limitations doc is the binding rule; the audit guide either follows it or proposes an amendment to it). If the audit guide wants reading (b), it must be explicit that it overrules the limitations doc §5 row, which then triggers a sister-revision of the limitations doc.

### Length and density

863 lines for a procedure MD that implements an 8-element spec brief is on the long side but not disproportionate when measured against the project's other methodology MDs. Comparison points: `research_line_limitations.md` is 857 lines (which the draft is on par with), `lc_era_temporal_segmentation.md` is 155 lines (much smaller; it locks a single methodological choice), `symptom_mention_asymmetry.md` is 231 lines.

The draft is closer to the limitations doc model (a layer-level binding rule with downstream-binding-tables) than to the single-decision model. That is appropriate for the role.

**Cuttable redundancy spotted:**

- §5.5's "L-ID surface" paragraph + §10's L-ID notes restate the same binding twice; if reading (a) is adopted per concern above, one of them can be tightened.
- §7.7 may be merge-able into §7.1 (per §4 above) — saving ~10 lines.
- §3's "what Stage D does NOT do" content overlaps with §1's "what Stage D does NOT do" content. Pick one home.

Total ~50 lines of cuttable redundancy at most. Length is not a fire.

### Blocking a Stage D dry-run on HA-C4 or another ready HA

If a future drafter loaded this guide and tried to run a descriptive audit on HA-C4 v2 tomorrow (or HA-C3 v2 / HA-C3p / HA-C4c / HA11-bout-redo per the stocktake §4 list of ready HAs), they would hit:

1. **The L-ID-citation tension** — would the audit cite L5 + L7 in its rows, or not? The draft answers both ways. **Blocking until resolved.**
2. **The structurally-untestable open_inputs gap** — if Stage D ran on HA-C4 v2 and an assumption was found structurally untestable (it likely won't on HA-C4 v2, but per the §6.2 rule the case exists), would §4.5 be empty or populated? The draft says empty; plan §3.5 says populated. **Blocking until resolved.**
3. **The figures vs plots naming** — a drafter generating supporting plots for HA-C4 v2 would have to choose; the inconsistency with sibling descriptive analyses makes the choice friction-inducing. Not blocking but operationally ugly.
4. **The skill is not yet built** (§11 step 7) — the draft references `/research-interpret descriptive HA-XX` (§9 throughout) but the skill does not exist yet. The audit guide cannot be operationally tested without the skill; the four ready HAs are Stage D candidates *for the future skill build*, not for current dry-run. The draft acknowledges this implicitly but does not name it as a precondition. Worth a one-line note in §1 or §11 that the skill must land before any audit can be drafted.

None of (1)-(3) prevent the guide from locking; all four would surface during the first dry-run if not fixed first.

## 7. Required actions (must fix before lock)

1. **Resolve the L-ID citation tension between §2's "does not cite L-IDs" framing and the limitations doc §5 row's verbatim "Cite L5 and L7 explicitly" rule + the draft's own §5.5 L-ID-surface framing.** Either align with the limitations doc (audit cites L5 + L7 where the rows apply) or explicitly overrule it (and trigger a limitations doc sister-revision). The current self-contradiction is the most consequential fix.

2. **Resolve the §4.4 "exactly one of three labels" vs §6.2 "fourth label" inconsistency.** Either §4.4 lists four labels (and §6.2 explains the fourth's routing), or the fourth case is a terminate-and-route-elsewhere event with no audit label (and §6.2 says so explicitly without naming a fourth label).

3. **Resolve §6.2's "audit terminates with no §4.5 open_inputs entry" vs plan §3.5's hard rule that every refusal-to-proceed produces an open_inputs entry.** A structurally-untestable HA's missing-input *is* the revised pre-reg or unblocked dependency; that is an `open_inputs` candidate, not an absence.

4. **Resolve the `figures/` vs `plots/` naming collision with existing sibling descriptive analyses.** Recommend matching `plots/` to stay consistent with `analyses/descriptive/operationalisation_support/.../plots/` and `analyses/descriptive/trajectory/.../plots/`.

## 8. Recommended actions (should consider)

1. **Add an "alternatives considered" paragraph** at §1 or §2 to address CONVENTIONS §2.2 four-input bar item 3 (tradeoff vision). Even one paragraph naming what was considered and why this shape was chosen would tighten the four-input compliance.

2. **Move the §6.3 audit-disagrees-with-stocktake diff requirement from §4 to §3.** The diff is about the per-assumption status assignment (which lives in §3 of the audit) not the verdict-trust call (§4).

3. **Swap the §6.1 HA-C3 v1 → v2 example for HA-C3 v2 + HA-C3p.** v1 → v2 is an iteration on the same HA after a HALT; v2 + sister HA-C3p is the cleaner sister-HA example.

4. **Add a §9.1 fail-safe** for when a stocktake-cited descriptive artefact path no longer exists at load time. Default to NOT BACKSTOPPED with an open_inputs entry naming the missing path.

5. **Name the §9.6 drift-trigger registration as manual-pending-skill** (matching the limitations doc §8 "downstream-citation-count" pattern). The skill that automates this is built later in §11 step 7.

6. **Cross-reference plan §3.5's "always at most one tier narrower"** in the §4.4 PROVISIONAL "narrower-claim discipline" framing to make the discipline concrete.

7. **Note in §3 (or §11)** that Stage D audits accumulate under `analyses/` and are subject to the audit-before-push privacy gate per CONVENTIONS §2.3. Almost certainly inherited but worth one explicit line.

8. **Consider merging §7.7 into §7.1** as a sub-paragraph; the L-ID-vs-descriptive-backstop distinction is a subcase of the "non-descriptive cited as descriptive" pattern. Either keep or merge is defensible; merging saves ~10 lines.

9. **Cite stocktake §7 explicitly** in §6.3's "audit may revise the stocktake's B / N / / assignment" rule — the stocktake itself flags that its B-partial usage is liberal.

10. **Add a one-line precondition note** in §1 or §11 that the §11 step 7 skill must land before any audit can be drafted; the guide alone is necessary-but-not-sufficient.

## 9. What is fine as-is

- The §1 purpose framing + the block-quote opening + the "what Stage D does NOT do" scope clarification: all clear.
- The six §2 inputs, with stocktake-as-input added: sound and useful.
- The §3 artefact-naming convention (one folder per HA, exact registry ID, currently-locked-revision-only) is well-thought-through; the "no version suffix on filename" rule + "revision history in lock log" is the right pattern matching the limitations doc + map MDs.
- The §3 producer-mode + no-fresh-session-review framing for the audit artefact itself (it is an audit, not a verdict) is correct per plan §4 split table.
- The §4 five-section outline mapping faithfully to §6.1 bullets.
- The §4.3 "Hard rule on the BACKSTOPPED label" explicitly disqualifying "BACKSTOPPED by inspection of result.md" — strong belt-and-suspenders enforcement of §7.1.
- All eight §5 checklist items in their §6.1 order with binding doc + operational test + worked examples; the operational tests track the cited MDs accurately.
- §6.4 verdict-trust-independent-of-verdict-label invention — methodologically strong; one of the best additions.
- The §7.1-§7.3 anti-pattern implementations with §7.3's lock-date-discriminator language operationalising "post-hoc and peeking" cleanly.
- The §8.4 optional verdict-trust confirmation seed framed as confirmation-not-discovery seed (the §3 ticks mechanically determine the call).
- §9.2's prose-vs-code drift surfacing as a §8.1 interview seed feed (transparent rather than silent).
- §9.5's skill-level refuse-gate on TRUSTED when any row is NOT BACKSTOPPED — implementing §7.6 mechanically.
- The §10 cross-reference table coverage — comprehensive, well-anchored, no broken links in spot-check.
- The §11 lock log shape matching `research_line_limitations.md` and `synthesis_structure_map.md` conventions.
