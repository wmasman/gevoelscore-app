# Review: Phase-axis collapsibility conventions methodology MD (phase_axis_collapsibility_conventions)

**Target**: [`docs/research/methodology/phase_axis_collapsibility_conventions.md`](../methodology/phase_axis_collapsibility_conventions.md) (r1 at commit `1282d9b`).
**Drafting handoff**: `C:/Users/Gebruiker/.claude/plans/session-phase-axis-collapsibility-conventions-md-draft-handoff-2026-06-22.md`
**User-locked decisions (PM 2026-06-22 via AskUserQuestion)**: (1) hypothesis-driven only collapse trigger; (2) new MD location (NOT v2 of `lc_recovery_phase_axis.md`); (3) Tier B channel-sensitivity binding rule for CONFIRMED-citalopram channels.
**Reviewer mode**: Claude (independent peer reviewer per [CONVENTIONS §1.2](../CONVENTIONS.md) + §2.2 + user-added plan-effectiveness dimension). *Fresh session — no exposure to the drafting context; doc-only knowledge.*
**Review date**: 2026-06-22.

---

## 1. What the MD proposes

The MD specifies a **3-tier collapsibility hierarchy + one hard boundary** for pooling phases within the [`lc_recovery_phase_axis.md`](../methodology/lc_recovery_phase_axis.md) 6-phase axis (phases 1, 2, 3, 4a, 4b, 5) when running HA pre-regs or descriptive analyses. **Tier A** pools sub-phases 4a + 4b into the original `pacing_pre_citalopram` (564 days) when the hypothesis is insensitive to within-phase-4 habit-formation variation OR per-sub-phase n is insufficient; **Tier B** pools phase 4 (or 4a + 4b separately) + phase 5 into a unified pacing+medication era, with a **binding channel-sensitivity rule** that CONFIRMED-citalopram channels (`stress_mean_sleep` / `all_day_stress_avg` / `bb_lowest` per [`citalopram_dose_response §5.6`](../methodology/citalopram_dose_response_stress_mean_sleep.md)) REQUIRE one of [`citalopram_phase_stratification §5.A/B/C`](../methodology/citalopram_phase_stratification.md) treatment patterns; **Tier C** pools phase 3 + 4 + 5 into the data-given Stratum 4 (project-canonical default for HA pre-regs not adopting within-LC sub-structure); and a **hard boundary** that NEVER pools across phase 1 ↔ phase 2 ↔ LC era (data-given strata per [`lc_era_temporal_segmentation §1`](../methodology/lc_era_temporal_segmentation.md); pooling would mix categorically distinct illness states). The **collapse trigger is hypothesis-driven only** per the user-locked PM 2026-06-22 decision — no data-driven empirical-invisibility back-door — which is the dual of the anti-data-driven-boundary-tuning discipline already locked in [`lc_era_temporal_segmentation §4`](../methodology/lc_era_temporal_segmentation.md) and [`citalopram_phase_stratification §3`](../methodology/citalopram_phase_stratification.md). The MD is downstream-consumer-only: it does NOT modify the axis spec, the citalopram stratification, the era segmentation, or the dose-response empirical anchor; reciprocal-cite paragraphs are queued for lock-time per §8 follow-ups. Adoption is opt-in for HA pre-regs (per `lc_era_temporal_segmentation §6`); descriptive analyses default to Tier C (for cross-stratum work) or no-collapse (for within-LC heterogeneity work). The MD anticipates a bout-level cascade interaction via [`bout_level_recovery_dynamics.md`](../methodology/bout_level_recovery_dynamics.md) (§6.4) and a long-memory interaction with [`recovery_arc/findings.md`](../analyses/descriptive/trajectory/recovery_arc/findings.md) via §5.4.

The MD's empirical claim is procedural: this is the convention vocabulary that HA pre-regs + descriptive analyses adopt when they pool phases. No causal claim, no SUPPORTED/REJECTED verdicts — only operational definitions + a binding §3.2 fire-condition rule.

---

## 2. What fired and why

### Layer 1 — Four-input bar (inherits from [CONVENTIONS §2.2](../CONVENTIONS.md))

**L1.1 Best-practices standards — pass.** §5.1 names three concrete bodies of standards each with the criterion it imposes: (i) WWC 2022 SCED + SCRIBE 2016 on hypothesis-driven phase-pooling discipline (operational-distinguishability + pre-registration + per-phase-n-reporting); (ii) the anti-data-driven-boundary-tuning principle from `lc_era_temporal_segmentation §4` + `citalopram_phase_stratification §3` re-cast as its **dual** (anti-data-driven-pooling) — this dual-framing is the load-bearing methodological move and it is named explicitly; (iii) Daza 2018 per-channel inheritance via the citalopram framework, not duplicated but named-by-place (Tier B). Each citation is tied to a criterion. The deferred-but-named candidates (Daza-family pooling follow-up, WWC SCED Appendix on phase-pooling) are appropriately scoped at §5.2.

**L1.2 Established literature — pass.** §5.2 cleanly downgrades to "deferred-but-named honestly" per the CONVENTIONS §2.2 deferred-honesty pattern, with concrete candidate fetch targets (Daza-family pooling-discipline follow-up; WWC 2022 SCED standards Appendix on phase-pooling). Inherited project-canonical anchors (SCRIBE / CENT / STROBE / Daza / WWC / Natesan via `CONVENTIONS §1.2`; the v3 dose-response confirmation via `citalopram_dose_response §5.6`) are properly cross-referenced without re-fetching. The framework reasoning does not depend on the deferred anchors.

**L1.3 Tradeoffs — pass with strong evidence.** §5.3 is an 8-row × 4-column structured table comparing (a) no conventions / (b) data-driven trigger / (d) always-stratify / (e) CHOSEN. The eight dimensions span risk-of-back-doors, compatibility with CONVENTIONS §4.2, compatibility with `lc_era_temporal_segmentation §4`, power preservation when sub-phase n is tight, channel-sensitivity preservation, hard-boundary preservation, cross-HA comparability, and cost to HA pre-reg authors. The tradeoff summary explicitly names the load-bearing choice ("hypothesis-driven trigger is the load-bearing choice; it ports the well-anchored anti-data-driven-boundary discipline... to the dual question of pooling"). Quality on par with the lc_recovery_phase_axis §5.3 table the prior audit cycle called "strongest in the methodology folder".

**L1.4 Research limitations + objectives — pass.** §5.4 enumerates four honest limits: (i) n=1 single-subject; HA-author honesty in classification is the enforcement; (ii) edge cases (e.g. mixed Tier B + Tier C on a CONFIRMED channel with pre-LC vs LC scope); (iii) sub-phase 4a's 56-day tight-n interaction with Tier A's n-adequacy condition; (iv) **long-memory inheritance via the citalopram dimension** with explicit reference to `recovery_arc/findings.md` factor-of-2 E[L]\* flag + block-aware bootstrap discipline in `lc_recovery_phase_axis §6.6`. Item (iv) is exactly the L4.1 fire the upstream `lc_recovery_phase_axis` audit (2026-06-19) flagged on its own §5.4 — the producer correctly absorbed that finding into the downstream MD's limitations row. Five objectives served are named explicitly. Clean.

### Layer 2 — Cross-axis consistency

**L2.1 Cross-axis position — pass.** §1.3's 3-layer axis table accurately describes the nesting: outer (data-given strata) → middle (recovery-phase axis, where this MD operates) → inner (citalopram dose-state, Tier B inheritance source). The framing is consistent with [`lc_recovery_phase_axis §1.3`](../methodology/lc_recovery_phase_axis.md) (which is the 3-layer source-of-truth) and with [`citalopram_phase_stratification §3 cross-axis position`](../methodology/citalopram_phase_stratification.md) (which calls its `unmedicated` phase the home of the recovery-phase sub-partition).

**L2.2 Tier B channel-sensitivity cites — pass.** §3.2 cites `citalopram_dose_response_stress_mean_sleep §5.6` for the 3 CONFIRMED-citalopram channels and names them explicitly (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`). The channel list matches the source MD §5.6.1 verdict matrix (CONFIRMED ×3 = those three). §3.2 cross-refs §5.A/B/C verbatim via `citalopram_phase_stratification` with sub-anchors `§5.A` / `§5.B` / `§5.C`. The "weak" `resting_hr` and "partial" `bb_overnight_gain` are correctly excluded from the binding-rule list.

**L2.3 Hard boundary inheritance — pass.** §3.4 hard boundary correctly inherits `lc_era_temporal_segmentation §1` data-given strata + dates (phase 1 2021-08-16 → 2022-03-20, phase 2 2022-03-21 → 2022-04-03, LC era from 2022-04-04). The "category error" framing (mixing healthy / acute-viral / chronic illness states; resulting pooled estimate uninterpretable as a coherent quantity) is sound and matches `lc_era_temporal_segmentation §1`'s "background, not a methodological choice" framing applied in its dual.

**L2.4 §6.x adoption pattern — pass with minor wording observation.** §6.1 HA opt-in pattern (declare tier + condition + §5.A/B/C choice for CONFIRMED channels) matches `lc_era_temporal_segmentation §6` opt-in discipline. §6.2 descriptive pattern (Tier C default for cross-stratum; no-collapse for within-LC heterogeneity) matches `lc_recovery_phase_axis §6.1-§6.3` descriptive adoption pattern. **Minor wording observation, not a fire**: §6.4 "the bout-level cascade... opts into the 6-phase recovery-phase axis via the bout-level MD's Approach A/B/C" is slightly imprecise. The bout-level MD's [§5.3 Approach A/B/C](../methodology/bout_level_recovery_dynamics.md) is about *per-bout dose-handling at cross-phase scope* (Approach A = bout-level dose-adjusted predictor; B = bout-level dose as covariate; C = stratify-by-citalopram-phase + meta-analyse), NOT about *opting into the recovery-phase axis itself*. The opting-in mechanism for bout-level HAs to the 6-phase axis is not actually named in the bout-level MD as "Approach A/B/C"; the §6.4 sentence conflates *cross-phase-scope handling at bout level* with *recovery-phase-axis opt-in*. r2 absorb opportunity: replace "via the bout-level MD's Approach A/B/C" with "via the bout-level MD's §5.3 cross-phase scope position" or similar; the inheritance still binds correctly via §6.4's three bullet points (declare-tier + CONFIRMED-channel-treatment + bout-level β source).

**L2.5 STOCKTAKE / lock-cascade anticipation — pass.** §8 follow-up #4 names the STOCKTAKE entry trigger at lock-commit per `STOCKTAKE §8` "New methodology MD locked"; §8 #5 names the `descriptive/README §5` index addition; §8 #1-#3 name the three reciprocal-cite paragraphs (`lc_recovery_phase_axis` + `lc_era_temporal_segmentation §1` + `citalopram_phase_stratification §5`). The lock-cascade pattern matches the `lc_recovery_phase_axis r2 lock` and `bout_level_recovery_dynamics r2 co-lock` precedents.

### Layer 3 — Operationalisation integrity

**L3.1 Tier A conditions — pass.** §3.1 lists three hypothesis-driven conditions (hypothesis-shape insensitivity; n-adequacy with sub-phase 4a's 56-day reference; structural insensitivity to pacing-habit timing) with explicit ANY-of-three semantics. Default is named: non-collapsed (4a + 4b as separate cells) is the default; Tier A collapse is the documented exception, with the HA pre-reg's `§3 Data sources` block carrying the condition + the resulting pooled unit name "phase 4 `pacing_pre_citalopram` (4a+4b pooled)". Cross-cite to `lc_recovery_phase_axis §3.4` parent + §3.4a / §3.4b sub-definitions is present.

**L3.2 Tier B channel-sensitivity rule — pass with strong evidence.** §3.2's channel-sensitivity rule is unambiguously framed as **BINDING** (capitalised), inside a blockquote, with the explicit "Pool-without-correction on these channels is a fire on this MD's discipline" — i.e. the fire-language is binding, not advisory. The audit-hook framing ("The audit hook is the same one already binding via `citalopram_phase_stratification §4` per-channel inheritance — Tier B does not add a new rule, it *names the place* where the rule applies") is honest about the inheritance source. The §3 Data sources block protocol carries through. Cross-cite to `citalopram_phase_stratification §3` + §5 + §6 + `citalopram_dose_response §5.6` is complete.

**L3.3 Tier C default — pass.** §3.3 explicitly states Tier C IS the project-canonical default in the strict sense ("every HA pre-reg that does not adopt within-LC sub-structure is operating at Tier C by default") and cites `lc_era_temporal_segmentation §1` Stratum 4 framing. The Tier C + Tier B interaction paragraph at end of §3.3 honestly carries the channel-sensitivity rule transitively (Tier C inclusive of Tier B's pool means CONFIRMED channels still require §5.A/B/C at Tier C — "the citalopram dose effect doesn't disappear when phase 3 is added to the pool"). This is the substantive operational lift.

**L3.4 Hard boundary — pass.** §3.4 unambiguously names the three never-pool boundaries (phase 1 ↔ 2 ↔ LC era), grounds the rationale in `lc_era_temporal_segmentation §1` data-given strata + the dual of `lc_era_temporal_segmentation §4` anti-data-driven discipline, and explicitly states "No conditions exist that justify this collapse." The category-error framing (healthy autonomic regulation vs acute-viral disruption vs chronic LC patterns; pooled estimate uninterpretable as coherent quantity) is sound. The phrasing "the boundaries are data-given (not a methodological choice); the same logic applies to the pooling-non-availability — it is not a discipline choice, it is a category-error preventive" is precise.

**L3.5 Worked examples — pass with bonus.** §3.5 (placed inside §3 rather than as a §2.5 sub-section per the handoff's section labelling — minor structural reorganization, defensible) contains six mixed-tier examples vs the handoff §2.5's five. The handoff's five all appear with their recommended pooling intact + tier mix labels; the sixth ("Does within-night autonomic recovery shape differ across LC era?") is added by the producer as a no-collapse-default illustration. The bonus example reinforces the "within-LC heterogeneity is the question → no collapse" framing for descriptive work. All six are illustrative-not-exhaustive per the framing paragraph. Cross-citations to `citalopram_phase_stratification §5.A` + §5.B inside example rows tie back to the binding-rule source.

**L3.6 HA pre-reg adoption pattern — pass.** §6.1 explicitly states HA pre-regs adopting the 6-phase axis MUST declare in `§3 Data sources`: (a) tier (Tier A / B / C / no-collapse / mixed); (b) hypothesis-driven condition (one of §3.1.1-3 for Tier A, §3.2.1-3 for Tier B, §3.3.1-3 for Tier C); (c) for Tier B on a CONFIRMED-citalopram channel, the §5.A/B/C treatment pattern + the `citalopram_phase_stratification §6` template reference. The protocol matches `lc_era_temporal_segmentation §6` opt-in template + `citalopram_phase_stratification §6` pre-reg template.

### Layer 4 — Project-specific audit hooks (inherits from [CONVENTIONS §3, §4](../CONVENTIONS.md))

**L4.1 CONVENTIONS §3.6 named-counts — pass with minor.** §2 hierarchy table reports the resulting unit's duration in days for each tier ("phase 4 `pacing_pre_citalopram` (564 days)"; "Stratum 4"; etc.) which carries the named-count for the *pooled cell* itself. §3 per-tier sections name component sub-phase n where Tier A is concerned (4a is 56 days; 4b is ~508 days). §6.5 explicitly states no row-level annotation is needed (tier choice is pre-reg / analysis-level). **Minor observation**: §6 does not name an explicit per-tier n-tracking expectation for downstream HA pre-regs adopting a tier (i.e. "the HA pre-reg's §3 Data sources block names the n at the chosen tier per CONVENTIONS §3.6"); the requirement is implicit via the HA pre-reg-author obligation that already exists, but a one-sentence cross-reference to CONVENTIONS §3.6 in §6.1 would close the audit hook explicitly. Magnitude minor; mechanical r2 absorb opportunity, not blocking.

**L4.2 CONVENTIONS §4.2 caveats-vs-apriori — pass with strong evidence.** The hypothesis-driven-only framing is kept clean throughout. §4(b) explicitly rejects the data-driven trigger with rationale ("Even an empirical-invisibility test is a hypothesis evaluation on the same data; reusing it to decide pooling-then-test creates a self-confirming pipeline"). §5.3 row "Compatibility with CONVENTIONS §4.2" marks (b) as VIOLATED and (e) as ALIGNED. §5.4 first bullet honestly names the enforcement limit ("hypothesis-driven discipline relies on the HA pre-reg author honestly classifying their hypothesis-channel pair"). No slippage into data-driven justification anywhere in the body. The §1.2 "NOT a data-driven decision tool" + §1.3 cross-axis framing + §3 per-tier conditions all bind structurally to hypothesis-driven-only — the framing is reinforced at six distinct surfaces.

**L4.3 CONVENTIONS §4.3 no-interpretive-marks — pass.** No SUPPORTED / REJECTED bars on the MD's own propositions; the only verdict-style language ("fire", "pool-without-correction = fire") is operational + binding-rule discipline, not a verdict on a hypothesis test. §4 alternatives table uses "rejected" / "proposed" / "CHOSEN" framing for the alternative comparison, which is the standard methodology-MD pattern (per `lc_recovery_phase_axis §4` + `bout_level_recovery_dynamics §4` precedents) and is not an interpretive mark on raw data. Clean against §4.3.

**L4.4 Long-memory implication — pass with strong evidence.** §5.4 fourth bullet explicitly names: long-memory inheritance via the citalopram dimension; the recovery_arc/findings.md factor-of-2 E[L]\* flag (6/7 cells; the audit-handoff specified 6/7); the project-default E[L]=7; the interaction with Tier C pool (full Stratum 4) bootstrap CIs; the cross-reference to `lc_recovery_phase_axis §6.6` block-aware bootstrap discipline. The single sentence "Pooling decisions interact with block-bootstrap E[L]\* choices: a Tier C pool on a CONFIRMED channel must run block-bootstrap with E[L]\* widened beyond the project default E[L]=7" carries the prescription forward without duplicating §6.6. This is the L4.1 fire from the upstream lc_recovery_phase_axis audit cycle absorbed as inherited limitation at the right place. Non-trivial pass.

### Plan-effectiveness dimension (per user request 2026-06-22)

#### PE.1 — Handoff-specified content coverage

Walk of handoff §3.1's 11 required sections (Authorship + Citation status + §1-§9):

| handoff §3.1 required section | r1 location | present / partial / missing |
|---|---|---|
| Authorship | r1 lines 7-13 | **present** (drafter + authorising user redacted + drafting-session context + status) |
| Citation status | r1 lines 17-33 | **present** (first-principles + inherited anchors named + deferred-but-named candidates listed) |
| §1 What this is / is not / cross-axis position | r1 §1.1, §1.2, §1.3 | **present** (the cross-axis position has its own §1.3 sub-section with 3-layer table) |
| §2 3-tier hierarchy + hard boundary (4 positions) | r1 §2 | **present** (all 4 positions in one 4-row table: Tier A / B / C / HARD BOUNDARY) |
| §3 Per-tier discipline + binding rules (4 sub-sections) | r1 §3.1-§3.4 + §3.5 examples | **present** (Tier A §3.1, Tier B §3.2 with binding channel-sensitivity rule, Tier C §3.3, hard boundary §3.4) |
| §4 Alternatives considered (a-e with (e) chosen) | r1 §4 | **present** (5 alternatives a-e exactly; (e) marked CHOSEN) |
| §5 Four-input reasoning (4 inputs) | r1 §5.1-§5.4 | **present** (all four inputs addressed; §5.3 trade-off table; §5.4 limitations + 5 objectives) |
| §6 Operational consequences (with sub-sections) | r1 §6.1-§6.6 | **present** (HA opt-in §6.1; descriptive §6.2; §5.A/B/C inheritance §6.3; bout-level cascade §6.4; per-day master column §6.5; `lc_era_temporal_segmentation §7` coverage §6.6) |
| §7 Status + lock-blocking gates (5 gates) | r1 §7.1 | **present** (5 lock-blocking gates enumerated; §7.2 hard discipline rules also present as historical record) |
| §8 Open follow-ups | r1 §8 (8 items) | **present** (3 reciprocal-cites + STOCKTAKE + descriptive/README index + HA-pre-reg template update + literature fetch + v2 amendment trigger) |
| §9 Cross-references | r1 §9 | **present** (all cross-ref MDs enumerated with section anchors) |

**PE.1 verdict**: **PASS-PE** — all 11 required sections covered; no missing-section fires. Coverage is faithful to the handoff §3.1 prescription with the structural variance noted in PE.4 (mixed examples placed in §3.5 instead of §2.5).

#### PE.2 — User-locked decisions honored

| user-locked decision (PM 2026-06-22) | r1 evidence | verdict |
|---|---|---|
| **Decision 1: hypothesis-driven only collapse trigger (no data-driven back-door)** | §1.1 "the trigger... is **hypothesis-driven only** (per PM 2026-06-22)"; §1.2 "NOT a data-driven decision tool"; §3.1.1-3 / §3.2.1-3 / §3.3.1-3 conditions are ALL hypothesis-structure-based (no in-data signal anywhere); §4(b) explicitly rejects data-driven trigger with rationale; §5.3 row "Compatibility with CONVENTIONS §4.2" marks data-driven as VIOLATED, chosen as ALIGNED; §5.4 first bullet honestly names HA-author enforcement; §2 default canonicals "the trigger for choosing a tier is hypothesis-driven only" | **PASS** — reinforced at six surfaces; no data-driven pathway anywhere in r1 |
| **Decision 2: new MD location (NOT v2 of lc_recovery_phase_axis.md)** | File exists at `docs/research/methodology/phase_axis_collapsibility_conventions.md` (the path itself is the proof); `lc_recovery_phase_axis.md` is unmodified (still at LOCKED r2 2026-06-19 `d47e0d3`); §1.2 explicitly states "NOT a re-derivation of the 6-phase axis" + "NOT a modification of cross-reference MDs"; §7.2 historical discipline rules preserve "Do NOT modify cross-reference MDs" | **PASS** — file location + cross-ref MDs unmodified |
| **Decision 3: Tier B channel-sensitivity binding rule for CONFIRMED-citalopram channels** | §3.2 channel-sensitivity rule is in BINDING CAPITALS inside a blockquote; the 3 channels named verbatim (`stress_mean_sleep` / `all_day_stress_avg` / `bb_lowest`); the §5.A/B/C requirement is unambiguous; "Pool-without-correction on these channels is a fire on this MD's discipline" — binding-language, not advisory; §2 hierarchy table cell "CONFIRMED-citalopram channels REQUIRE one of `citalopram_phase_stratification §5.A/B/C`" carries the rule to the hierarchy-summary surface; Tier C + Tier B interaction paragraph at end of §3.3 transitively extends the rule to Tier C | **PASS** — binding language + 3 channels named + fire-condition explicit + cross-tier transitivity preserved |

**PE.2 verdict**: **PASS-PE** — all 3 user-locked decisions honored at strong evidence. No decision-violation fire; the PE.2-blocking criterion (any FAIL → automatic REVISION RECOMMENDED) does NOT trigger.

#### PE.3 — Scope creep check

Walked the four scope-creep risk surfaces named in the handoff:

- **More than 4 tiers (A/B/C + hard)?** No. §2 table has exactly 4 rows (Tier A, Tier B, Tier C, HARD BOUNDARY). §3 has exactly 4 sub-sections (§3.1-§3.4). The mixed-examples table at §3.5 uses combinations of the 4 tiers (e.g. "Tier A + Tier B with §5.A correction"), not new tiers. Compliant.
- **Data-driven collapse pathways anywhere?** No. §3 conditions are all hypothesis-structure-based. §4(b) explicitly rejects data-driven trigger. §1.2 forbids it. Compliant.
- **Cross-reference MDs modified?** No. `git status` clean before r1 commit per the audit-handoff §5.1 + the producer's handoff §4 discipline. Reciprocal-cites are explicitly queued for lock-time at §8 follow-ups #1-#3. Compliant.
- **HA pre-reg content pre-authored?** No. §6.1 specifies the template HA pre-regs should follow (declare tier + condition + §5.A/B/C choice) but does not pre-author any specific HA pre-reg's tier choice. The §3.5 mixed-tier examples are illustrative hypothesis-shapes, not lock-bearing HA pre-reg drafts. Compliant.

**One in-intent scope-addition observation, not a fire**: §3.5 contains 6 mixed-tier examples vs the handoff §2.5's 5. The added example ("Does within-night autonomic recovery shape differ across LC era?") illustrates the no-collapse default for within-LC heterogeneity descriptive work. This is in-intent (the handoff explicitly framed §2.5 as "illustrative, not exhaustive"); the producer added a clarifying row that strengthens the descriptive-work pattern. Not creep.

**PE.3 verdict**: **PASS-PE** — no scope creep; one defensible in-intent addition.

#### PE.4 — Gap analysis

Walked things the handoff explicitly named that r1 might not have delivered:

- **§2 4-tier conditions wording fidelity**: handoff §2.1-2.4 specified each tier's conditions with "ANY of:" semantics. r1 §3.1-§3.4 carries the same "ANY of the three suffices" semantics + the conditions are paraphrased without losing the structural shape. The §3.1.1-3 / §3.2.1-3 / §3.3.1-3 condition triplets each map 1:1 to the handoff's three-bullet lists. **Not a gap.**
- **§2.5 mixed-tier examples**: handoff §2.5 had 5 examples; r1 §3.5 has 6 (one in-intent addition per PE.3). The handoff's 5 examples ALL appear in r1 §3.5 with their recommended pooling intact and tier-mix labels. **Not a gap.**
- **§3.1 prescribed structured sub-sections**: handoff §3.1 prescribed Authorship + Citation status + §1-§9. All present per PE.1. **Not a gap.**
- **Structural placement variance — minor mechanical**: the handoff §3.1 item 4 ("§2 The 3-tier hierarchy + hard boundary") implied the mixed examples might live in §2.5; r1 places them at §3.5 instead. The §2 in r1 is the *hierarchy table* (concise, 4-row); §3 is *per-tier discipline + binding rules* (with §3.5 as the examples sub-section). Structural reorganization is defensible (separates the "structural shape" surface from the "operational illustration" surface) and the content is preserved. **Not a gap** but worth flagging as a structural variance in case a future reader expects §2.5 examples per the handoff labelling.
- **Default canonicals (handoff §2.3 "Default canonical (per `lc_era_temporal_segmentation`): Stratum 4 IS the primary analytic surface; Tier C is the project-canonical default for most HA pre-regs")**: r1 §2 "Default canonicals" paragraph + §3.3 "Tier C is the **project-canonical default** in the strict sense" both deliver this. **Not a gap.**

**PE.4 verdict**: **PASS-PE** — no architectural omissions; one structural-placement minor observation noted but does not change content coverage or operational integrity.

#### Plan-effectiveness rollup verdict

**PASS-PE** across all four sub-dimensions. No decision-violation (PE.2 clean). No scope-creep (PE.3 clean). No gap-fire on content (PE.4 clean). All handoff §3.1 sections present (PE.1 clean). The minor structural-placement variance at §3.5 (vs handoff §2.5) is a defensible reorganization; the §6.4 wording on "bout-level MD's Approach A/B/C" is the L2.4 minor wording observation but does not fall in the PE dimension.

---

## 3. What does not fire (selective)

- **§5.3 trade-off table** is the strongest §5.3 in the methodology folder since the lc_recovery_phase_axis §5.3 (which the 2026-06-19 audit explicitly called out as "strongest in the methodology folder reviewed today"). 8 rows × 4 columns covering 8 dimensions of analytical risk + structural-preservation contrasts across 4 alternatives. The trade-off summary explicitly names the load-bearing choice. Non-trivial pass.

- **§4 alternatives table** names 5 alternatives (a-e) with one-sentence rationale each, (e) marked CHOSEN. The (b) data-driven trigger rejection cites the CONVENTIONS §4.2 + `lc_era_temporal_segmentation §4` discipline pair — internally coherent with the chosen-decision framing. The (c) per-channel collapsibility rules rejection honestly observes the over-specification cost. The (d) always-stratify rejection cites the tight-n (4a 56 days) interaction. Non-trivial completeness.

- **§3.4 hard boundary rationale** ("the boundaries are data-given (not a methodological choice); the same logic applies to the pooling-non-availability — it is not a discipline choice, it is a category-error preventive") cleanly inverts the `lc_era_temporal_segmentation §1` framing ("background, not a methodological choice") into its dual at the pooling layer. Internally coherent with the source-of-truth.

- **Tier C + Tier B interaction paragraph at end of §3.3** carries the channel-sensitivity rule transitively to Tier C ("the citalopram dose effect doesn't disappear when phase 3 is added to the pool. The Tier B channel-sensitivity rule binds at Tier C as well"). This is the substantive operational lift that prevents a Tier-C-pool-on-a-CONFIRMED-channel from being a back-door around the §3.2 binding rule. Non-trivial.

- **§5.4 long-memory bullet** absorbs the L4.1 fire from the upstream `lc_recovery_phase_axis` 2026-06-19 audit cycle. The producer correctly carried the recovery_arc/findings.md factor-of-2 E[L]\* flag + the block-aware bootstrap discipline forward as an inherited limitation. The cross-reference to `lc_recovery_phase_axis §6.6` (the block-aware bootstrap source-of-truth) avoids duplication.

- **§7.2 historical discipline rules** preserved cleanly. The five rules ("End at r1 + commit. Do NOT self-audit"; "Do NOT lock in this session"; "Do NOT modify cross-reference MDs"; "Do NOT pre-author what the audit should find"; "Do NOT relitigate user-confirmed decisions") match the handoff §4 hard rules and the `lc_recovery_phase_axis §7.2` historical-record pattern. The producer-mode-reviewer-mode session-context separation is preserved at the doc level, enabling this fresh-session audit to read cold.

- **§1.2 four "is not" bullets** are tight and prevent four common misreads: re-derivation of the axis; binding gate on every HA pre-reg; replacement for `citalopram_phase_stratification §5`; data-driven decision tool; modification of cross-reference MDs. The framing-discipline anchors are stated upfront.

- **Plan-effectiveness PE.2 evidence quality on Decision 1**: the hypothesis-driven-only commitment is reinforced at six distinct surfaces (§1.1, §1.2, §3.x conditions, §4(b) rejection, §5.3 table row, §5.4 first bullet). This is unusually disciplined; a producer-mode artefact reinforcing a user-locked commitment at six surfaces is the kind of evidence that resolves the PE.2 fresh-session-audit check unambiguously.

---

## 4. What would strengthen this MD

Concrete, named, ordered by leverage:

1. **§6.4 wording fix — "bout-level MD's Approach A/B/C" reframe** (closes L2.4 minor wording observation). Suggested wording: replace "via the bout-level MD's Approach A/B/C" with "via the bout-level MD's §5.3 cross-phase scope position" or "as documented in the bout-level MD's §5.3 (Approach A as headline + B + C as sensitivity arms for cross-phase scope handling)". The bout-level MD's Approach A/B/C are about per-bout dose-handling at cross-phase scope, NOT the recovery-phase-axis opt-in mechanism itself. The inheritance bullet structure (declare-tier + CONFIRMED-channel-treatment + bout-level β source) is correct; only the framing sentence needs the precision pass. Magnitude minor; mechanical r2 absorb.

2. **§6.1 add explicit CONVENTIONS §3.6 named-counts cross-reference** (closes L4.1 minor). Suggested wording: in the §6.1 third bullet add a sub-bullet: *"per [CONVENTIONS §3.6](../CONVENTIONS.md) named-counts discipline, the HA pre-reg's `§3 Data sources` block names the n at the chosen tier (e.g. 'Tier B pool n = 1295 days' for a 4+5 pool)."* — anchors the implicit author obligation to the convention surface. Magnitude minor.

3. **§3.5 placement note — add a §2.5 forward-pointer** (closes PE.4 structural-placement minor observation). The handoff implied §2.5 placement for the mixed examples; r1 placed them at §3.5 (defensible). A one-sentence forward-pointer in §2 ("Mixed-tier examples illustrating tier composition appear at §3.5") would resolve the reader-expectation mismatch without requiring re-placement. Magnitude minor; mechanical r2 absorb.

4. **§8 add one open follow-up for the §5.2 deferred-literature fetch result-back path** (low-leverage; queueing-discipline polish). When the §5.2 deferred-but-named candidates (Daza-family pooling-discipline follow-up; WWC SCED Appendix on phase-pooling) eventually land in `docs/research/literature/`, this MD's §5.2 row absorbs them via a §3.6 mechanical-compression r2 (per the methodology MD carve-out). §8 already names #7 "Literature fetch for the deferred-but-named §5.2 candidates" but does NOT name the absorb path; a one-sentence addition would close the loop ("on landing, r2 absorbs at §5.2 via `hypothesis_lock_process.md §3.6` mechanical compression"). Magnitude very minor; queueing-discipline only.

5. **§7.1 criterion 4 reciprocal-citation discipline polish** — the criterion is already named for lock-time but the polish opportunity is one-sentence per recipient MD: "reciprocal-cite paragraph in `[MD name] §[anchor]` adding [forward pointer text]". The handoff §8 covers the queueing; r1 §8 follow-ups #1-#3 sketch the per-recipient text intent. Magnitude very minor; lock-time discipline.

The four content-strengthening items above are all **mechanical r2 absorb** scope (per `hypothesis_lock_process.md §3.6` compression criteria for methodology MDs — pattern matches the `lc_recovery_phase_axis r2 lock` 2026-06-19 cycle which absorbed 5 L1-L4 fires mechanically). None require architectural revision; none change the 3-tier + hard-boundary structure; none relitigate any user-locked decision. Lock can proceed in a separate r2 drafter session after the mechanical absorb.

---

## 5. Verdict

**PASS-with-caveats** — the MD's 3-tier + hard-boundary architecture, hypothesis-driven-only discipline, Tier B binding channel-sensitivity rule, cross-axis inheritance from `citalopram_phase_stratification §5.A/B/C`, hard-boundary rationale (`lc_era_temporal_segmentation §1` dual), four-input bar coverage, and §5.4 long-memory inheritance absorb (carrying forward the L4.1 fire from the upstream `lc_recovery_phase_axis` 2026-06-19 audit) all read clean against both the content-audit (Layer 1-4) and plan-effectiveness (PE.1-4) dimensions; the highest-priority residual is the §6.4 minor wording observation (the "Approach A/B/C" framing on bout-level cascade inheritance is slightly imprecise per L2.4) plus three other mechanical r2 absorb opportunities at §6.1 (named-counts cross-ref), §3.5 (forward-pointer from §2), and §8 (deferred-literature absorb path); no blocking architectural fires; all three user-locked decisions are honored at strong evidence (PE.2 clean) with the hypothesis-driven-only commitment reinforced at six distinct surfaces; r2 absorb can proceed mechanically per `hypothesis_lock_process.md §3.6` compression criteria matching the `lc_recovery_phase_axis r2 lock` precedent.

---

## Methodology

This review walks the 4-layer content audit framework defined in this session's handoff
([`session-phase-axis-collapsibility-conventions-methodology-audit-handoff-2026-06-22.md`](file:///C:/Users/Gebruiker/.claude/plans/session-phase-axis-collapsibility-conventions-methodology-audit-handoff-2026-06-22.md)),
PLUS the plan-effectiveness audit dimension (PE.1-PE.4) added per user request 2026-06-22.

Standard layers adapted from [`reviews/README.md`](README.md) for the methodology-MD case
per [CONVENTIONS §2.2](../CONVENTIONS.md) four-input bar discipline.
Plan-effectiveness layer per [[feedback_pre_reg_writer_role]] adapted — verifies that
the producer agent's r1 output faithfully accomplished what the PM-level handoff +
user-locked decisions specified.

Project-specific audit hooks from [CONVENTIONS §3 + §4](../CONVENTIONS.md);
methodology-MD lock framework from
[`hypothesis_lock_process.md §1`](../methodology/hypothesis_lock_process.md)
(carve-out: methodology MDs are governed by CONVENTIONS §2.2 + §2.3, not the
HA lock process); r2 compression criteria from
[`hypothesis_lock_process.md §3.6`](../methodology/hypothesis_lock_process.md).
