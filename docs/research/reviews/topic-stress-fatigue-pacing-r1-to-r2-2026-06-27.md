# Artefact review — topic-stress-fatigue-pacing.md r1 → r2 diff (2026-06-27)

**Reviewer mode**: fresh-session peer review. Reviewer is independent of the r1→r2 drafting session. Doc-only knowledge of the correction.
**Target**: [`docs/research/analyses/contextualisation/topic-stress-fatigue-pacing.md`](../analyses/contextualisation/topic-stress-fatigue-pacing.md) r2 DRAFT (status header + NEW §4.3.5 + §4.4 Subclaim 1 + §4.4 Subclaim 2 Measurement + §4.6 caveat 2 + §4.7 L3 + §4.8(b) + §4.8 Comparability bound + §4.8 Resolution paths + §4.9 OI#4 row + §4.9 own-research item + §4.9 external-research item + §11 lock-log three new rows).
**Scope**: r1 → r2 diff only. The r1 LOCKED baseline was user-accepted 2026-06-25 in Phase A.7 (Option-γ); re-reviewing unchanged r1 sections (§4.1, §4.2, §4.3, §4.5, §4.7 L1/L2/L4/L6/L7/L5, §4.8 (a)/(c)/(d)/(e), §4.10) is out of scope.
**Review date**: 2026-06-27 (Stage S₂ artefact in Phase A re-open).
**Standards applied**: [CONVENTIONS](../CONVENTIONS.md) §1.2 (reviewer-mode), §2.1 (descriptive-before-inference + no-interpretive-marks), §2.2 (four-input bar — adapted to reviewer-mode-with-authorization at S₂); [external_contextualisation.md](../methodology/external_contextualisation.md) r3 LOCKED 2026-06-26 (the binding methodology, especially §4.3.5 + §4.4 lead-in + §5.3 DIVERGES mapping + §7.13 anti-pattern); [wiggers_testable_hypotheses.md](../wiggers_testable_hypotheses.md) §C C3 verbatim (USER-VERIFIED-VIA-REGISTER-ANCHOR-VERIFICATION-2026-06-12, the source claim); [Daza 2018] N-of-1 inference reach; [CENT 2015] items 21+22; [SCRIBE 2016] transparency; [Natesan 2023] N-of-1 defensibility bar.

---

## 1. Overall verdict

**ACCEPT.** The r1→r2 diff correctly absorbs guide #4 r3's §4.3.5 binding into the topic artefact's Subclaim-1 chain. The new §4.3.5 section follows the guide's procedure faithfully; the CONSTRUCT-IDENTICAL verdict for Wiggers's "stress score" × project's `all_day_stress_avg` is warranted by the §C C3 verbatim (Garmin Connect UI references "annual stress overview" + "stress score line" + "your own stress scores" all anchor to the Firstbeat-derived UI metric). The 12 downstream reframings are internally consistent: §4.4 Subclaim 1 Measurement now correctly cites §4.3.5; the Sub-1 Overall call correctly drops measurement from the fault-line list; §4.4 Sub-2 Measurement holds independently on the broader-PEM-literature substrate-mismatch (which §4.3.5 rule 1 correctly does NOT fire on, since no source-side named metric is cross-cited); §4.6 caveat 2's dual-scope (within-vendor for Sub-1 + cross-substrate for Sub-2) cleanly distinguishes the two subclaims' comparability bounds; §4.7 L3, §4.8(b), §4.8 Comparability bound, §4.8 Resolution paths, and §4.9 entries all chain correctly. The §4.5 positioning (DIVERGES + EXTENDS + CANNOT-SAY) is correctly preserved — under the §5.3 mapping the COMPARABLE-on-construct + PARTIALLY-COMPARABLE-on-era reading at Sub-1 still routes to DIVERGES (era is non-load-bearing for the direction-of-curvature question; the divergence on direction does not weaken when the comparability bound narrows). No leftover misframings outside the intentional historical references. The §11 lock-log rows preserve r1 provenance correctly and signal r2's DRAFT-PENDING-FRESH-REVIEW state. No required findings; no recommended findings rise to the level of revision-blocking. The artefact can lock r2 as-is after the user accepts this review.

The transferability picture is the main thing for the drafter to attend to next: of the three inheriting artefacts, two carry r1-shaped misframings and need the same pattern of correction (research-audience topic translation §5.4 + §5.5 + §5.9; patient-audience topic translation §5.4 + §5.9). The actionability construct does not carry the misframing in any user-visible form (it consumes the topic's positioning calls + tier aspiration, not the comparability internals). See §11 below.

## 2. Summary of findings

| ID | Type | Section | Severity | One-line |
|---|---|---|---|---|
| — | — | — | — | No required or recommended findings on the r1→r2 diff itself. |
| T1 | TRANSFERABILITY | translation/research-audience §5.4 + §5.5 + §5.9 | Mild (downstream) | The research-audience translation inherits r1 misframings ("Garmin-vs-subjective-stress instrumentation fault-line"; "Wiggers' qualitative subjective-stress framing without named instrument"; "Cross-instrumentation comparability study"); same correction pattern applies — flag for the drafter when extending the correction. |
| T2 | TRANSFERABILITY | translation/patient-audience §5.4 (line 51) + §5.4 (line 61(b)) + audit notitie | Mild (downstream) | The patient-audience translation carries the same r1 misframing in Dutch ("objectieve Garmin-stresswaarde ... versus subjectieve stress-inschattingen ... zonder een specifiek meet-instrument te noemen"; line 61(b) "misschien meet Garmin-stress iets anders dan wat Wiggers met 'stress' bedoelt"); needs the same correction adapted to patient-audience plain-language registry. This is the artefact whose hedge wording originally surfaced the miss. |
| T3 | TRANSFERABILITY | actionability/construct-stress-fatigue-monitoring.md | None | The construct doesn't surface comparability internals; it consumes positioning verdicts + tier aspiration. No correction needed there. |

## 3. Required findings

**None.** The r1→r2 diff is methodologically sound, internally consistent, and faithful to the binding methodology guide. The artefact is acceptance-ready on the diff alone.

## 4. Recommended findings

**None at the revision-blocking level.** Minor observations that did NOT rise to revision-recommended:

- §4.3.5 origin-note paragraph (lines 70 of the artefact) cleanly documents the r1 miss with Daza N=1 + SCRIBE transparency. The level of detail is appropriate for a permanent provenance trail; not overlong. No fix needed.
- §4.3.5 Subclaim 1's L3-stretch language ("These three sub-issues sit under L3 literally per its 'underlying algorithm updates' + 'calibration drift' framing but stretch L3 past its hardware-upgrade-triggered project-specific manifestation; whether to expand L3 or add an L8 is flagged to the [`research_line_limitations.md`](../../methodology/research_line_limitations.md) maintainer as a separate decision") is the same A2 recommendation from guide #4 r3 review propagated correctly to this artefact. Good.
- §4.7 L3 entry (line 160) and §4.3.5 Subclaim 1 both flag the L3-expansion-vs-new-L8 question; the redundant flagging is appropriate at S₂ (both sections legitimately surface the same open decision in different contexts) and not duplicative noise.

## 5. §4.3.5 faithfulness to guide #4 r3 (per-procedure-step assessment)

**Procedure step 1 (identify named metrics; skip non-overlapping)**: The new §4.3.5 correctly identifies Wiggers's "stress score" as the source's named metric for Subclaim 1; correctly identifies that Subclaim 2 has no source-side named metric to check (broader PEM-pacing literature does NOT cross-cite a Garmin metric); correctly inherits Subclaim 3's LITERATURE-GAP status from §4.3. Pass.

**Procedure step 2 (read source's operational definition)**: The §4.3.5 Subclaim 1 block names three textual anchors from the §C C3 verbatim ("annual stress overview" + "stress score line" + "your own stress scores") all pointing at the Garmin Connect UI feature; cites the source's section title ("Annual Stress Scores" section, lines 1357-1368). This is direct anchoring to the source's operational definition. Pass.

**Procedure step 3 (cite project's operational definition)**: The §4.3.5 Subclaim 1 block cites `all_day_stress_avg` = daily mean of Garmin Firstbeat per-minute stress score (0-100 scale), with `wiggers_testable_hypotheses.md` §C cell map as the project-side anchor. Pass.

**Procedure step 4 (compare → 3-label set verdict)**: CONSTRUCT-IDENTICAL is correctly derived. Same instrument family (Garmin Firstbeat), same UI metric (Annual Stress Scores), same scale (0-100). Pass.

**Procedure step 5 (record per-subclaim-per-metric block; §4.4 inherits + cites)**: §4.3.5 records the verdict + two one-sentence descriptions; §4.4 Subclaim 1 Measurement cites the §4.3.5 verdict ("COMPARABLE on construct + instrument family per §4.3.5 CONSTRUCT-IDENTICAL verdict"); §4.7 L3 entry cites the same verdict ("Garmin FR245-derived `all_day_stress_avg` and Wiggers's 'stress score' both observe the same Firstbeat HRV-derived stress score UI metric per §4.3.5 CONSTRUCT-IDENTICAL verdict"); §4.8 Comparability bound cites the same verdict. Wiring discipline is followed throughout. Pass.

**Hard rule 1 (§4.3.5 fires only on CONSENSUS-EXISTS / COMPETING-POSITIONS subclaims, not LITERATURE-GAP / CONSENSUS-DOES-NOT-EXIST)**: §4.3.5 Subclaim 3 correctly does NOT fire because §4.3 records LITERATURE-GAP; the §6.5 routing applies upstream of §4.3.5. Pass.

**Hard rule 1 applied to Subclaim 2**: The §4.3.5 Subclaim 2 block correctly does NOT fire — §4.3 records COMPETING-POSITIONS but the position-holders (energy-envelope, push-crash, Appelman 2024) do NOT cross-cite a Garmin metric with the project. The genuine substrate-mismatch is captured directly at §4.4 Subclaim 2 Measurement on its own grounds (subjective fatigue inventories, muscle biopsy markers, crash-report instruments vs project Garmin-stress). Pass — this is the subtle case where the hard rule allows substrate-mismatch at §4.4 because there's no source-side named-metric to compare; §4.3.5 not firing does NOT mean §4.4 Measurement defaults to COMPARABLE on construct.

**Hard rule 3 (substrate-mismatch is NOT a default; CONSTRUCT-IDENTICAL unless source's text establishes otherwise)**: The §4.3.5 Subclaim 1 reasoning correctly anchors to the source's UI references, not to "the wording sounds qualitative" inference. Pass — this is precisely the §7.13 anti-pattern the section was designed to close.

**Hard rule 4 (§4.4 Measurement MUST cite §4.3.5 verdict per subclaim per metric)**: §4.4 Subclaim 1 Measurement cites §4.3.5 verbatim; §4.4 Subclaim 2 Measurement cites the §4.3.5 not-firing rationale. Pass.

**Origin-note transparency assessment**: The origin-note (line 70) is appropriately Daza N=1 + SCRIBE transparency-grade — it documents the r1 miss with provenance (patient-audience hedge wording, root cause: guide #4 r2 had no construct-identity step), names the methodology fix (guide #4 r3 §4.3.5), and explicitly identifies r2's role as absorbing the correction. The level of detail is appropriate for a permanent provenance trail without becoming load-bearing on the substantive S₂ output.

**Mapping to §4.4 Measurement constraint**: §4.3.5 Subclaim 1's CONSTRUCT-IDENTICAL verdict correctly maps to "substrate-mismatch is forbidden as a fault-line; remaining fault-lines are calibration-level" at §4.4. The three remaining calibration-level caveats (device-generation L3, Firstbeat algorithm-version drift, population-Firstbeat-calibration) are correctly enumerated and consistent with the guide's worked-example anchor. Pass.

## 6. Internal consistency of the 12 reframings (per-edit assessment)

**(1) NEW §4.3.5 section**: Pass (see §5 above).

**(2) §4.4 Subclaim 1 Measurement**: Correctly reframed to COMPARABLE on construct + instrument family per §4.3.5; remaining fault-lines enumerated as within-vendor calibration (device-gen L3 + algo-version drift + population-Firstbeat-calibration); Daza 2018 reach citation preserved with appropriate scoping ("convergence-or-divergence-data-point reach for the direction-level question" + "the within-vendor calibration caveats place the absolute-value comparison at hypothesis-generating reach only" — this is the correct two-tier reach assertion).

**(3) §4.4 Subclaim 1 Overall**: Correctly reframed from PARTIALLY COMPARABLE on measurement + era → PARTIALLY COMPARABLE on era only. The era fault-line (medication-phase comparability) is correctly identified as non-load-bearing for the direction-of-curvature question. Pass.

**(4) §4.4 Subclaim 2 Measurement**: Correctly decoupled from "same as Subclaim 1" reference (which the LOCKED-r1 had inherited as a shortcut, but in r2 with Subclaim 1 reframed to COMPARABLE the shortcut would propagate the wrong answer). The Sub-2 substrate-mismatch is now restated on its own grounds (broader PEM-pacing literature uses subjective fatigue inventories, muscle biopsy markers, crash-report instruments vs project Garmin-stress). The "fault-line is load-bearing only for absolute-magnitude claims across substrates; for the direction-of-shape question it is not load-bearing" reach scoping is preserved correctly. Pass.

**(5) §4.6 caveat 2**: Correctly reframed to dual-scope wording: "(i) within-vendor calibration (device-generation + Firstbeat algorithm-version + population-Firstbeat-calibration) for the Wiggers comparison on its shared Garmin substrate, and (ii) cross-substrate bridging for the broader-PEM-pacing-literature comparison." The two-scope split cleanly distinguishes Sub-1's comparability bound from Sub-2's; the explicit closing sentence ("not the cross-substrate one the LOCKED-r1 misframing implied") is appropriate self-correction transparency. Pass.

**(6) §4.7 L3 citation entry**: Correctly reframed from cross-instrumentation to within-vendor (FR245 vs Wiggers's source-data device pool; Firstbeat algorithm-version drift) + population-Firstbeat-calibration. The §4.3.5 verdict citation is included. The L3-expansion-vs-L8-addition flag is preserved. Pass.

**(7) §4.8(b) candidate explanation**: Correctly reframed from "Garmin captures different construct than Wiggers' subjective rating" → "Measurement instrument calibration" (device-gen + algo-version + population-calibration delta). The candidate retains its function as a non-null explanation for the divergence (the same nominal stress score could represent different underlying autonomic-load levels across cohorts), now correctly attributed to within-vendor calibration rather than to construct-validity. The "Replaces the LOCKED-r1 'different construct' candidate per §4.3.5 verdict" replaces-note is appropriate transparency. Pass.

**(8) §4.8 Comparability bound**: Correctly reframed to "PARTIALLY COMPARABLE on era only" with measurement-COMPARABLE-on-construct citation. The remaining within-vendor calibration caveats are correctly scoped as bounding absolute-magnitude reach but not direction-of-shape reach. Pass.

**(9) §4.8 Resolution paths**: The "Within-vendor Firstbeat-calibration cross-walk" entry correctly replaces the LOCKED-r1 "Garmin-vs-subjective-stress-rating descriptive run" entry. The clarification "not required for the direction-of-shape question per the §4.3.5 CONSTRUCT-IDENTICAL verdict" is correct (the cross-walk would resolve the §4.8(b) calibration-delta candidate, not the direction-divergence). Pass.

**(10) §4.9 OI#4 table row**: Correctly reframed to "Within-vendor Firstbeat-calibration cross-walk between FR245 readings and other Firstbeat-derived datasets ... for the absolute-magnitude question." The "Replaces the LOCKED-r1 'Garmin-vs-subjective-stress-rating' framing per §4.3.5 verdict" replaces-note is preserved. Acquisition-path realism ("Requires Wiggers's source-data Garmin-stress distribution (not publicly known) OR cross-device Garmin-stress comparison studies from broader Firstbeat-validation literature; M-L effort, partially external-research-dependent") is honest. Pass.

**(11) §4.9 own-research track**: The own-research entry for "Within-vendor Firstbeat-calibration cross-walk" is correctly reframed. The explicit replaces-note ("The LOCKED-r1 'Garmin-vs-subjective-stress-rating descriptive run' entry was removed at r2 per the construct-validity-of-named-metric correction (Wiggers and the project both measure the same Firstbeat-derived UI metric per §4.3.5; the within-subject substrate-mismatch the r1 entry assumed does not exist).") is correct provenance discipline. Pass.

**(12) §4.9 external-research track**: Correctly reframed to "Cross-cohort Garmin-stress calibration validation study in a comparable LC / PAIS population using the same Firstbeat algorithm family." The L3 + population-Firstbeat-calibration scoping is preserved. The replaces-note for the LOCKED-r1 cross-instrumentation framing is preserved. The clarification "A calibration validation study would clarify whether the Wiggers-observed monotone-convex shape and the project-observed concave / inverted-U shape arise from a calibration delta on the same instrument family vs from genuine subject-level biological variation" is the correct framing of what the external study would actually answer. Pass.

## 7. Worked-example verification (independent confirmation)

I independently read `wiggers_testable_hypotheses.md` §C C3 (lines 485-497). The verbatim quote at line 490 contains exactly: "Your annual stress overview includes a stress score line. If you've paid attention to your own stress scores, you might know that a day with a score of 40 is much more tiring than a day with a score of 30. Such a step appears very small on the graph, but it isn't. This graph shows a kind of stair step. This person has overexerted themselves and their health is deteriorating as a result." This sourcing is dated 2026-06-12 batch 2 with "VERBATIM MATCH" finding. The textual anchors "annual stress overview" + "stress score line" + "your own stress scores" all point unambiguously at the Garmin Connect Annual Stress Scores dashboard UI feature — Wiggers's "stress score" is the Garmin Firstbeat-derived UI metric, not a subjective rating. The §C section heading in the corresponding cell map is "Stress score (Garmin daytime/night, HRV-derived)" — explicit Garmin-Firstbeat attribution.

The §4.3.5 Subclaim 1 reading is warranted. The artefact's claim that Wiggers's "stress score" = Garmin Connect UI metric = same Firstbeat-derived UI metric the project's `all_day_stress_avg` aggregates is correct on the source evidence. (Note: the methodology-review on guide #4 r3 already verified this; this is an independent confirmation that the artefact's r2 verdict re-derives the same conclusion from the same primary evidence.)

## 8. Positioning preservation assessment (does DIVERGES still hold?)

The §4.5 positioning calls (Sub-1 DIVERGES; Sub-2 EXTENDS; Sub-3 CANNOT-SAY) are unchanged in r2. The question: under the corrected §4.4 Sub-1 (COMPARABLE on construct + PARTIALLY COMPARABLE on era only), does DIVERGES still hold per guide #4 r3 §5.3 mapping?

**Guide #4 r3 §5.3 mapping**: "DIVERGES applies when: §4.3 is CONSENSUS-EXISTS ...; §4.4 is COMPARABLE (or PARTIALLY COMPARABLE with unmatched dimensions not load-bearing for the divergence — if load-bearing, positioning routes to CANNOT-SAY instead); the subject's reading contradicts external consensus on direction."

The artefact's Sub-1 satisfies all three conditions under the corrected reading:
1. §4.3 Sub-1 = CONSENSUS-EXISTS (unchanged). Pass.
2. §4.4 Sub-1 = PARTIALLY COMPARABLE on era only (measurement is COMPARABLE per §4.3.5). The unmatched era dimension (medication-phase comparability) is correctly identified as non-load-bearing for the direction-of-curvature question (per CENT 2015 item 22 generalisability framing — medication-phase variation affects absolute-magnitude calibration of the dose-response, not its directional shape). Pass.
3. The subject's reading (concave / inverted-U with peak at mid-stress, decline at upper stress) contradicts the Wiggers convex-cost direction. Pass.

DIVERGES remains the correct call.

**Counter-consideration**: would AGREES (the strongest positioning) become applicable under the corrected COMPARABLE-on-construct reading? No — AGREES requires the subject's reading to align with external consensus on direction. The cluster's joint claim is inverse-direction curvature (concave / inverted-U vs Wiggers's monotone-convex), so AGREES is structurally not available regardless of comparability bound. The corrected comparability bound narrows the scope of the divergence (now correctly attributed to within-vendor-calibration / population-calibration / direction reach rather than to cross-substrate substrate-mismatch), but does not change the direction-of-shape divergence itself.

**Counter-consideration**: would the corrected comparability route Sub-1 to CANNOT-SAY (per §5.3 "if load-bearing, positioning routes to CANNOT-SAY instead")? No — the era dimension is correctly identified as non-load-bearing for direction-of-curvature; the within-vendor calibration caveats bound absolute-magnitude reach but not direction-of-shape reach (this is the explicit two-tier reach split at §4.4 Sub-1). Routing to CANNOT-SAY would be the wrong call.

The intended-outcome assertion in the review brief ("The construct-validity correction narrowed the comparability-bound scope but didn't change the direction-of-shape verdict") is correct. DIVERGES is the right call; it should stay.

## 9. Leftover-misframings sweep

I searched the r2 artefact for surviving traces of the r1 misframing. Findings:

**Intentional historical references (appropriate; do NOT flag)**:
- Status header (line 3): "an invented substrate-mismatch on a 'Wiggers uses subjective stress rating without naming a specific instrument' framing" — appropriately framed as the r1 miss being absorbed.
- §4.3.5 origin note (line 70): "an invented 'Wiggers uses subjective stress rating without naming a specific instrument' framing — a CONSTRUCT-RELATED-by-presumption misframing that propagated through §4.4, §4.6 caveat 2, §4.8(b), and §4.9" — appropriate provenance documentation.
- §4.4 Sub-1 Overall (line 90): "the LOCKED-r1 PARTIALLY-COMPARABLE-on-measurement attribution was the construct-validity-of-named-metric miss corrected at r2" — appropriate self-correction transparency.
- §4.6 caveat 2 closing (line 146): "not the cross-substrate one the LOCKED-r1 misframing implied" — appropriate.
- §4.8(b) closing (line 183): "Replaces the LOCKED-r1 'different construct' candidate per §4.3.5 verdict." — appropriate.
- §4.8 Resolution paths (line 190): "replaces the LOCKED-r1 'Garmin-vs-subjective-stress-rating' framing" — appropriate.
- §4.9 own-research closing (line 205): "The LOCKED-r1 'Garmin-vs-subjective-stress-rating descriptive run' entry was removed at r2 per the construct-validity-of-named-metric correction" — appropriate.
- §4.9 external-research closing (line 211): "The LOCKED-r1 framing of this entry as a 'cross-instrumentation Garmin-vs-subjective' study has been corrected per the §4.3.5 verdict" — appropriate.
- §4.9 OI#4 closing (line 220): "Replaces the LOCKED-r1 'Garmin-vs-subjective-stress-rating' framing per §4.3.5 verdict." — appropriate.
- §11 lock-log row 2026-06-26 (line 254) + row 2026-06-27 (line 255): describes the drift trigger + correction; appropriate provenance.

**Un-corrected leftovers**: **None found.** All occurrences of "subjective" / "substrate-mismatch" / "cross-instrumentation" / "different construct" / "Garmin signal vs Wiggers" in r2 are either (a) explicit historical replaces-notes / origin-notes / self-correction transparency, or (b) correctly-applied substrate-mismatch language for Sub-2's broader-PEM-pacing comparison (which is the genuine substrate-mismatch the §4.3.5 hard rule 1 does NOT touch). Pass.

## 10. Lock-log + status-header convention check

**§11 new rows format match**: The three new rows (2026-06-25 LOCKED r1 / 2026-06-26 Drift trigger fired / 2026-06-27 Drafted r1 → r2) follow the artefact's existing `| Date | Event | Note |` row format. Date format consistent. Event labels consistent with prior rows. Note fields include the load-bearing provenance pieces: user-acceptance + cite-provenance for the LOCKED r1 row; drift-trigger-number + the guide #4 r2→r3 lock-version + the methodology-doc miss provenance for the drift-trigger row; the six substantive changes enumerated for the Drafted r1→r2 row with explicit STATUS: NOT LOCKED — awaiting fresh-session `/research-review` (no Option-γ per 2026-06-26 process-discipline change) closing. Pass.

**Status header r1-history preservation**: The status header explicitly names "**DRAFT r2 PENDING FRESH-SESSION `/research-review` 2026-06-27**. r1 LOCKED 2026-06-25 by user acceptance per §11 step 10 Phase A.7 (Option-γ)." This correctly preserves r1's locked status as historical record while signalling r2's not-yet-locked state. The r1→r2 absorption is named with the specific construct-validity miss and the specific propagation chain. The closing sentence "Remaining sections (§4.1, §4.2, §4.3, §4.5, §4.7, §4.8 (a)(c)(d)(e), §4.10) carry through from r1 unchanged" correctly bounds the diff scope for the fresh-session reviewer. The "no Option-γ per 2026-06-26 process discipline change" call-out is appropriate process-trail transparency. Pass.

## 11. Transferability assessment for the inheriting artefacts

I scanned the three inheriting artefacts identified in the review brief. Findings:

**(T1) [`docs/research/analyses/translation/research-audience/topic-stress-fatigue-pacing.md`](../analyses/translation/research-audience/topic-stress-fatigue-pacing.md)** — **carries the r1 misframing; same correction pattern applies.**
- **§5.2 (line 23)** lists as a "likely first-read question": *"What is the substrate-mismatch impact on the DIVERGES call — does the Garmin-vs-subjective-stress instrumentation fault-line undercut the divergence?"* — this is the audience-anticipated framing of the very misframing that the r2 absorbs. The corrected reading is that there is no Garmin-vs-subjective-stress instrumentation fault-line; the §5.2 anticipated-question text should be reframed (the corrected first-read question is closer to "does the within-vendor Firstbeat-calibration delta undercut the divergence?").
- **§5.4 (line 41)** carries: *"PARTIALLY COMPARABLE on measurement (Garmin `all_day_stress_avg` 24-hour HRV-derived sympathetic-arousal index vs Wiggers' qualitative subjective-stress framing without named instrument) + era ..."* — direct propagation of the r1 misframing. Needs reframing to PARTIALLY COMPARABLE on era only + within-vendor-calibration scoping per the source r2 §4.4 Sub-1 + §4.6 caveat 2 dual-scope.
- **§5.5 (line 59)** L3 entry: *"Garmin FR245-derived `all_day_stress_avg` operationalises stress vs Wiggers' subjective-stress framing in the handleiding (no specific instrument named in the source)"* — direct propagation. Needs reframing per source r2 §4.7 L3 entry (within-vendor + population-Firstbeat-calibration).
- **§5.9 own-research (line 103)**: *"Garmin-`all_day_stress_avg` vs subjective-stress-rating comparability descriptive run"* — needs reframing per source r2 §4.9 own-research (within-vendor Firstbeat-calibration cross-walk).
- **§5.9 external-research (line 109)**: *"Cross-instrumentation comparability study Garmin `all_day_stress_avg` vs subjective-stress-rating"* — needs reframing per source r2 §4.9 external-research (cross-cohort Garmin-stress calibration validation study).
- **Watch-for**: this artefact is itself LOCKED r1 by user acceptance 2026-06-25 (Phase A.7), so the correction extends as r1→r2 of *this* translation artefact too, with its own lock-log + status-header preservation discipline. The research-audience track preserves methodology vocabulary verbatim per guide #6 §4.1, so the reframings can use the same terminology as the source's r2.

**(T2) [`docs/research/analyses/translation/patient-audience/topic-stress-fatigue-pacing.md`](../analyses/translation/patient-audience/topic-stress-fatigue-pacing.md)** — **carries the r1 misframing in plain Dutch; same correction pattern applies; this is the artefact whose hedge originally surfaced the miss.**
- **§5.4 (line 51)**: *"Ik vergelijk mijn **objectieve Garmin-stresswaarde** (een 24-uurs gemiddelde dat het horloge berekent uit hartritme-data) met de Wiggers-handleiding die over **subjectieve stress-inschattingen** spreekt (zonder een specifiek meet-instrument te noemen). Dat zijn twee verschillende substraten ..."* — the patient-audience plain-Dutch propagation of the r1 misframing. The corrected reading needs: Wiggers and the participant both measure the same Garmin Firstbeat-derived stress score; remaining caveats are within-vendor calibration (apparaat-generatie + algoritme-versie + populatie-kalibratie van het Firstbeat-algoritme dat oorspronkelijk op atleten/gezonde populaties gevalideerd is).
- **§5.4 line 61(b)**: *"misschien meet Garmin-stress iets anders dan wat Wiggers met 'stress' bedoelt"* — the user-spot-checked hedge that surfaced the miss. The corrected (b) candidate at source r2 §4.8(b) is "measurement instrument calibration" (device-gen + algo-version + population-Firstbeat-calibration delta). The plain-Dutch reframing would be along the lines of: "misschien meet de Garmin-stresswaarde op mijn FR245 hetzelfde Firstbeat-getal als waar Wiggers naar verwijst, maar betekent datzelfde getal voor LC-patiënten iets anders qua onderliggende autonome belasting dan voor de gezonde populatie waarop het algoritme oorspronkelijk gekalibreerd is."
- **§5.9-equivalent / open-inputs**: the patient-audience translation also needs the OI#4 + own-research + external-research entries reframed per source r2.
- **Watch-for**: this artefact is also LOCKED r1 (with layperson-test-pending accepted as production-state per locked-plan §10.7); the correction extends as r1→r2 of this translation, with its own status-header + lock-log preservation. The plain-Dutch register is more demanding to reframe than the research-audience English-vocabulary register; care needed not to invent new methodology-vocabulary translations on the fly. The "binnen-vendor Firstbeat-kalibratie cross-walk" / "populatie-Firstbeat-kalibratie" plain-Dutch translations probably want to go through the [`plain_language_dictionary.md`](../methodology/plain_language_dictionary.md) skill responsibility #7 first.

**(T3) [`docs/research/analyses/actionability/construct-stress-fatigue-monitoring.md`](../analyses/actionability/construct-stress-fatigue-monitoring.md)** — **does NOT carry the r1 misframing in any user-visible form; no correction needed.**
- This Stage A construct consumes the topic's per-subclaim positioning verdicts (DIVERGES + EXTENDS + CANNOT-SAY) and the tier aspiration (tier-1 monitoring); it does NOT surface the §4.4 comparability internals, §4.6 caveats, §4.7 L-ID details, or §4.9 follow-up tracks in any form that propagates the r1 misframing. References to "Wiggers consensus" / "Wiggers convex-cost claim" / "direction-anomaly with Wiggers' canonical claim" are positioning-call-level (DIVERGES is preserved) and L1-citation-level (which doesn't engage with the comparability misframing).
- The map's tier-2 aspiration block (line 33 "Informative-pattern (tier-2) blocked by single-cluster evidence + direction-anomaly with Wiggers' canonical claim") references the direction-anomaly, not the comparability-misframing. Pass.
- §5.4 NOT-DO #6 (line 90) Direction-vs-Wiggers overclaim ("DIVERGES adds a within-subject divergence data point, not a refutation") is unchanged-correct under r2. Pass.
- **Watch-for**: when the topic's r2 lands LOCKED, the construct artefact's "Source artefact" cite + source-artefact-lock-version reference should be updated to LOCKED r2 from LOCKED r1 (mechanical version-pointer update, not a substantive correction).

**Cross-cutting transferability watch-for**: the [`docs/research/analyses/translation/research-audience/construct-stress-fatigue-monitoring.md`](../analyses/translation/research-audience/construct-stress-fatigue-monitoring.md) and [`docs/research/analyses/translation/patient-audience/construct-stress-fatigue-monitoring.md`](../analyses/translation/patient-audience/construct-stress-fatigue-monitoring.md) (the sister Stage T translations of the construct, referenced in T2's text) likely need the same kind of mechanical version-pointer updates rather than substantive reframings — they consume the construct, which consumes positioning-level outputs from the topic, which are unchanged. Confirm by reading those two files when the topic's r2 LOCKs.

## 12. Final recommendation

**Lock r2 as-is** after user acceptance of this review.

The diff is methodologically sound (faithful to guide #4 r3 §4.3.5 procedure + hard rules + worked-example anchor); internally consistent (the 12 reframings chain correctly through §4.3.5 → §4.4 → §4.6 → §4.7 → §4.8 → §4.9); the worked-example verdict (CONSTRUCT-IDENTICAL for Wiggers's "stress score" × project's `all_day_stress_avg`) is warranted by the §C C3 verbatim; the §4.5 positioning preservation (DIVERGES + EXTENDS + CANNOT-SAY) is correct under the §5.3 mapping with the corrected comparability bound; no leftover misframings outside intentional historical references; the §11 lock-log + status-header conventions are followed. No required findings; no recommended findings rise to the level of revision-blocking.

The transferability findings (T1 + T2) are **downstream** — they bind the drafter's next moves on the two translation artefacts, not the r2 lock decision for this artefact. T3 (the actionability construct) requires only a mechanical version-pointer update when the topic r2 LOCKs.

**Suggested next-step sequence**:
1. User accepts this review → lock topic r2 in §11.
2. Drafter extends the same correction pattern to research-audience translation (r1→r2) + patient-audience translation (r1→r2) under §3.7 drift triggers, with their own fresh-session reviews.
3. Mechanical version-pointer update on actionability construct + the two construct translations when the topic r2 LOCKs.
4. The within-vendor Firstbeat-calibration cross-walk own-research entry (§4.9) is now correctly framed; remains an open follow-up for absolute-magnitude work and is appropriately scoped as "not blocking for the direction-of-divergence finding."
