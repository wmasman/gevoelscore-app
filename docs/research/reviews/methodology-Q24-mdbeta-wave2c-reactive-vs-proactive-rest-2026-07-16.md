# Methodology review: Q24 MD-beta Wave 2C descriptive audit -- reactive vs proactive rest

**Target artefact**: [`analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md) DRAFT r0 2026-07-16 (producer-mode Stage -1 descriptive audit per [CONVENTIONS section 1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs)).

**Review type**: Producer-mode methodology-adjacent review; 4-layer checklist walk per [`reviews/README.md`](README.md) plus Wave 2C-specific structural checks. Sister to [`methodology-Q24-mdbeta-precursor-rest-streak-2026-07-16.md`](methodology-Q24-mdbeta-precursor-rest-streak-2026-07-16.md) (Wave 2B) and [`methodology-Q24-mdalpha-precursor-phase-intensity-2026-07-16.md`](methodology-Q24-mdalpha-precursor-phase-intensity-2026-07-16.md).

**Reviewer**: fresh-session Claude (Opus 4.7) under user delegation. Cold context. Read target + companion `scripts/audit.py` + all 7 output CSVs + MD-beta LOCKED r1 + grandparent Q24 MD LOCKED r1 + Wave 2B sister audit + CONVENTIONS + memory `project_rest_day_operand_semantics` from disk.

**Discipline**: reviewer-mode per [CONVENTIONS section 1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations). NO edits to target audit, MD-beta, CONVENTIONS, or memory. Verdict for producer-mode artefact per this doc's section 5.

---

## 1. What the data shows

Empirical claims made by the target audit, plain restate (interpretive framing separated in section 2). All numbers cross-verified against `output/*.csv` byte-for-byte.

1. **Rest-day composition shifts monotonically across LC-era (audit section 3)**. On the 341-episode-adjacent rest-day pool, the proactive-strategic fraction (crash-before = False AND gevoelscore >= 5) rises 26.7% (2023) -> 25.3% (2024) -> 53.2% (2025) -> 56.2% (2026 partial). Crisis-reactive fraction (crash-before True AND gevoelscore <= 3) collapses 15.1% -> 9.5% -> 1.3% -> 0.0%. 2022 is data-availability-degraded (40.8% gs-nan).

2. **Mean gevoelscore on rest-day step-jumps at 2024 -> 2025 boundary (audit section 4)**. Heavy-adjacent pool: 3.99 -> 4.54; all-corpus rest-days pool: 4.03 -> 4.57. Median steps from 4 to 5 at the same transition. Two-pool agreement supports representativeness of heavy-adjacent subset.

3. **Whole-corpus mean gevoelscore also step-jumps at 2024 -> 2025 (audit section 4.4)**. LC-era all-non-NaN days: 4.10 (2023) -> 4.79 (2025), a +0.69 step; rest-day shift is +0.55 heavy-adj / +0.54 all-corpus. The rest-day shift is NOT larger than the whole-year shift; the felt-state improvement is not composition-specific.

4. **§5 LOAD-BEARING sign-flip (audit section 5)**. Pooled proactive-strategic-rest-after -> crash-in-5d RR = **0.354** (5/80 = 6.25% [Wilson 2.7, 13.8] vs complement 41/232 = 17.67% [13.3, 23.1]). Wave 2B pooled RR was 1.54 on the un-conditioned K=3 rest-after primary arm. Per-year: 2023 RR = 0.22 (clean flip); 2024 RR = **0.93** (does not flip, PS-True arm n=15 with 3 crashes); 2025 RR = 0.00 (0/23 vs 2/43); 2026 RR = 0.00 (0/15 vs 4/21).

5. **§6 endogeneity-isolation companion (audit section 6)**. Pooled crisis-reactive-rest RR = **4.29** (23/59 = 38.98% [27.6, 51.7] vs complement 23/253 = 9.09% [6.1, 13.3]). 2023: RR = **6.70** (9/14 = 64.29%). Per-year crisis-reactive arm goes viable_n_min5 = False in 2025 (n=4) and 2026 (n=4).

6. **Interpretation D VH-shrinkage sub-claim FALSIFIED (audit section 7)**. VH / activity-days: 14.2% (2023) -> 16.4% (2024) -> 16.2% (2025) -> 21.2% (2026 partial). Absolute VH counts flat 52 / 60 / 59 / 33 (partial). Directionally UP not DOWN.

7. **Step-envelope partial (audit section 8)**. Mean total_steps monotone down (6006 -> 4528, -25% over 4 years); p75 monotone down (7572 -> 5854); p25 roughly flat (~3200-3800 across all years). CV non-monotone (0.43 / 0.47 / **0.36** / 0.40 / 0.42), with 2024 tightest.

8. **Tactical-response AMBIGUOUS (audit section 9)**. Median heavy-to-next-rest gap 2 / 2 / 2 / 3 / 1 across 2022-2026, non-monotone. Mean gap noisy.

9. **10 reviewer concerns pre-surfaced by the audit itself (audit section 11)** -- gs threshold construct-validity, whole-corpus felt-state comparator handling, 2024 residual tension, day-level VH proxy, CV metric choice, rolling-p25 moves-with-envelope artefact, Interpretation B alternatives, physical-rest-only disclosure prominence, two-session peer-review discipline, and r2 revision-surface scope.

---

## 2. What fired and why

Layer-grouped fires with quote citations, magnitude, and absorb-vs-escalate signal.

### Layer 1 -- Universal reporting (SCRIBE 2016; STROBE 2007)

**L1.1 Operationalisation traceability -- PASSES with high confidence.** Audit sections 2.1 + 5.0 name operand + gevoelscore-bucket definitions with source-file cross-refs and inline citation of memory `project_rest_day_operand_semantics`. Every rate + RR carries scheme + unit + source CSV filename in-text per [CONVENTIONS section 3.6](../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file). Row-total checks at audit section 5.1 (312 = 314 - 2 NaN, crash counts summing 46) explicitly verify against parent Wave 2B section 7. Companion `scripts/audit.py` idempotently emits all 7 CSVs; every audit table matches the CSV byte-for-byte on spot check.

**L1.2 Framing not-overclaiming -- PASSES with high confidence.** The load-bearing §5 pooled RR = 0.354 is framed as "CONSISTENT-WITH Interpretation A" (section 5.3), not as a verdict or as "supports Interpretation A". Section 5.3 second paragraph explicitly qualifies: "proactive-strategic subset RR = 0.35 pooled is not a Stage-D verdict on Interpretation A; it is a descriptive-with-CI sign-flip on the pooled arm. Per CONVENTIONS section 2.1 the reading discipline is descriptive, not inferential." Section 2.4 pre-declares CONSISTENT-WITH / AMBIGUOUS-FOR / FALSIFYING as the only reading modes. The pattern is followed rigorously; no drift into causal or verdict language.

**L1.3 Deviation-from-parent-audit documentation -- PASSES.** NaN-drop discipline inherited from parent Wave 2B (audit section 5.1 tail: "2 NaN rest-after episodes dropped per parent Wave 2B NaN-drop discipline"); 312 vs 314 episode-count discrepancy is explicit. Corpus counts pointer-only to parent Stage -1 audit at section 1 rather than re-emitted, per [CONVENTIONS section 1.1](../CONVENTIONS.md) pointer-not-duplicate discipline.

**L1.4 Confounding-by-indication anchor citation -- PASSES.** Salas 2001 + Kyriacou & Lewis 2016 *JAMA* cited at audit sections 2.1 and 6.3 for the endogeneity mechanism, inheriting from MD-beta section 3.9 confound 1 without re-derivation.

### Layer 2 -- Observational n=1 (Daza 2018)

**L2.1 Counterfactual framing -- PASSES.** Audit section 2.4 pre-commits both Interpretation A and Interpretation D as partial-testable at n=1 with CONSISTENT-WITH / AMBIGUOUS-FOR / FALSIFYING as the only-permitted verdict labels. Section 5.3 explicitly names two alternative readings for the 2024 exception (small-n artefact vs partial mitigation only) rather than picking one silently. Section 4.2 confound-to-flag paragraph explicitly names the two alternative attributions of the mean-gs rise (composition shift vs whole-corpus felt-state improvement) and defers to section 4.4 comparator.

**L2.2 Stationarity assumption -- SUBSTANTIVE PASS (correctly-framed).** The whole Wave 2C is an investigation of whether the parent Wave 2B era-stratified sign-inversion reflects a stationarity break rather than a stable physiological signal. The audit's own conclusion at section 6.4 ("The pooled rest-adj arm rate (16.8%) is an arithmetic average of these sub-populations; the sign of the pooled RR depends on the mixture weights of strategic vs crisis rest-days, which per section 3 shift over the LC-era corpus") is the right frame. Combined with the Wave 2B review's already-recommended MD-beta r2 Path A (era + intensity to primary stratifier), the stationarity concern is architecturally-owned and does not need re-escalating from this audit.

**L2.3 Data provenance traceability -- PASSES.** All 7 CSV outputs named + written to `output/`; script path cited; `RANDOM_SEED = 20260716` declared even though not exercised at Stage -1 (correct discipline). Idempotent-re-run attestation at section 12 lock log.

**L2.4 Held-out-structure per `project_garmin_research_bias_boundary` -- PASSES.** The audit reads across 2022-2026 including the 2026 pre-dump extraction window; gevoelscore-conditioning uses gevoelscore-on-rest-day, which is the user's own subjective log rather than a Garmin-derived signal, so the analytical-bias boundary does not fire. `total_steps` and `exertion_class_lagged_lcera` are Garmin-derived but were tactical inputs pre-dump, not analytical -- consistent with memory `project_garmin_research_bias_boundary`. No fire.

### Layer 3 -- Time-series specific (Natesan Batley 2023; WWC 2022; CENT 2015)

**L3.1 Autocorrelation implications -- N/A at Stage -1 (correct scope).** Stage -1 descriptive; no bootstrap or permutation null exercised. The audit does not overreach into Stage D inference machinery. Not a fire.

**L3.2 Rolling-baseline moves-with-envelope artefact -- SUBSTANTIVE FIRE (correctly-surfaced, absorb).** Section 9.3 tail explicitly names the concern: "if the whole step-envelope shifts down (§8), the p25 threshold moves down too, potentially DELAYING the classification of a low-step day as a rest-day in years with lower overall step counts. This is an operand-artefact concern per MD-beta section 3.1 rolling-threshold discussion; not resolved at Stage -1." Section 11 concern 6 re-surfaces this as a reviewer-concern with a proposed remediation (absolute-step-threshold rest-day operand at total_steps < 3000). This is exactly the right level of surfacing: the artefact is named, its plausibility is grounded in section 8's mean-step-down finding, and the resolution is scoped as a Stage D companion rather than blocking r1 lock. Reviewer concurrence: no r1 blocking action needed; recommend Stage D companion (see section 4.4 below).

### Layer 4 -- Project-specific audit hooks (CONVENTIONS sections 3-4)

**L4.1 Personal-baseline discipline per CONVENTIONS section 3.1 -- PASSES.** Rest-day operand is `rest_day_p25` = personal 30d rolling p25 (inherited verbatim from MD-beta section 3.1). Gevoelscore threshold (>= 5 strategic, <= 3 crisis) is a construct-validity judgement on a subjective 1-6 scale where the participant's own idiographic anchoring is what the threshold reads against. The 4/5 split is defensible on face value for a personal-baseline read (gs 5 = "feels okay"; gs 4 = "middling"; gs 3 = "not okay"). See L4.2 for the construct-validity sensitivity discussion.

**L4.2 Definitional-pair discipline per CONVENTIONS section 3.3 -- SUBSTANTIVE FIRE (escalate for MD-beta author; absorb-eligible if r2 codifies).** §5 (proactive-strategic RR = 0.35) and §6 (crisis-reactive RR = 4.29) are two definitions on the same 314-episode + 341-rest-day pool. They are architecturally a definitional pair: strategic and crisis are complementary buckets on the same rest-day gevoelscore axis. The audit section 6.4 (Convergent evidence from §5 + §6) correctly frames the two as complementary sub-populations of the un-conditioned rest-arm, and the discussion at section 6.4 second paragraph ("The pooled rest-adj arm rate (16.8%) is an arithmetic average of these sub-populations") correctly treats them as an axis-decomposition rather than as independent tests. This is the right framing. What the audit does NOT do explicitly is name §5 + §6 as a definitional pair per CONVENTIONS section 3.3 and cite that discipline. This is a mechanical clarification (absorb-tier) at the audit level. The escalation to MD-beta author: the audit's implicit definitional pair (`rest_day_p25_strategic` + `rest_day_p25_crisis`) is exactly the "Definitional-pair extension candidate" flagged in memory `project_rest_day_operand_semantics` bullet 4; the empirical Wave 2C evidence justifies codifying this at MD-beta r2 section 3.1. See section 4.1 below for the load-bearing recommendation.

**L4.3 Construct-validity of the >= 5 vs <= 3 threshold -- SUBSTANTIVE FIRE (absorb with sensitivity companion at Stage D).** Section 5.4 correctly names the concern: "the gevoelscore = 4/5 boundary is a construct-validity judgement. Alternative thresholds (>= 4, borderline-inclusive; >= 6, strict-strategic-only) were not tested in this Wave 2C audit; a Stage D companion would need to run threshold sensitivity per MD-beta section 3.10 definitional-pair discipline. The pooled RR = 0.35 finding is contingent on the >= 5 threshold; the direction of the sign-flip is robust as long as rest-days with gevoelscore >= 5 are less crash-associated than rest-days with gevoelscore <= 4." This is textbook caveat-class framing per [CONVENTIONS section 4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no); the constraint on the robustness argument ("robust as long as gs >= 5 rest-days are less crash-associated than gs <= 4 rest-days") is honest about the operational claim scope. Reviewer concurrence: this is correctly-surfaced. Add-on recommendation: at Stage D, run at least the >= 4 vs <= 3 companion (borderline-inclusive strategic) and the >= 5 vs <= 4 companion (borderline-inclusive crisis) as sensitivity CSVs; see section 4.3 below.

**L4.4 Caveat-class vs a-priori framing per CONVENTIONS section 4.2 -- PASSES.** Every finding in sections 3-9 uses CONSISTENT-WITH / AMBIGUOUS-FOR / FALSIFYING framing. No a-priori language leaks in. The 2024 per-year exception (§5.3) is surfaced honestly with two candidate readings rather than absorbed into a "trend is clear except for one year" narrative. The §7 VH-fraction rise is framed as falsifying only the VH-shrinkage sub-claim of Interpretation D, not the whole interpretation (section 7.3 second paragraph explicitly: "If Interpretation D is to survive, it must survive on the tactical-response sub-claim (§9) or the step-envelope sub-claim (§8), not the very-heavy-frequency sub-claim"). Section 10.2 restates this discipline at findings-summary level. Discipline is followed rigorously.

**L4.5 Named-count discipline per CONVENTIONS section 3.6 -- PASSES.** Every count carries scheme + unit + source (e.g. "Crash days | 103 (crash_v2, day-level, `labels_crash_v2.csv`)" at section 1). Cell-count row-total checks are explicit at section 5.1 tail and section 6.1 tail.

**L4.6 Zero-vs-NaN discipline -- PASSES.** Section 12 lock log third bullet: "`is_crash.fillna(False).astype(bool)` only; gevoelscore NaN preserved as its own bucket (`gs_bucket == 'nan'`, 20 heavy-adjacent rest-days in 2022 pre-tracker onset); rest_day_p25 NaN preserved via parent Wave 2B `_rest_indicator` logic (2 rest-after NaN episodes dropped from §5 + §6 2x2s)." Consistent with the parent Wave 2B discipline; the 2022 40.8% gs-nan rate is transparently attributed to pre-tracker-onset at sections 1 + 3.2. No collapse of NaN into a boolean state.

**L4.7 Physical-rest-only operand disclosure per memory `project_rest_day_operand_semantics` -- PASSES.** Section 2.1 header carries the disclosure prominently; section 12 lock log seventh bullet re-attests it. Section 11 concern 8 self-surfaces the question of whether the disclosure is prominent enough in §5 and §6 headers where the load-bearing tests run. Reviewer note: the disclosure IS prominent at section 2.1 and cross-referenced at section 2.4; the load-bearing tests at §5 and §6 use the gevoelscore-bucket variables and would benefit from a one-sentence in-header reminder, but this is a copy-edit tier concern and does not block r1 lock. Absorb-tier if the audit revises to r1.

**L4.8 Sample-size discipline for §5 sub-cell analyses per parent §7.10 -- PASSES with minor comment.** Wilson CIs are reported on every rate at sections 5 + 6; the 2024 PS-True arm's n=15 / 3 crashes case is called out at section 5.2 as "under-powered" with the Wilson CI [7.0, 45.2] cited. The 2025 + 2026 crisis-reactive cells are correctly flagged `viable_n_min5 = False` in the CSV (n=4 crisis-reactive arm) and correspondingly not over-read in the narrative. Minor comment: audit section 5.2 could have been more explicit that the 2024 PS-True Wilson CI [7.0, 45.2] entirely contains RR = 1.0 relative to the complement rate 21.5% [13.3, 33.0], so the "sign-flip absent" reading is genuinely not distinguishable from either RR = 1 or RR = 0.5 at n=15. This is a mechanical clarification-tier concern; the audit's narrative treatment at section 5.3 second bullet ("Wide Wilson CI on the PS arm ... means this cell is under-powered") is adequate.

**L4.9 Interpretation A vs alternative-mechanism completeness -- MINOR FIRE (absorb, discretionary).** The audit tests Interpretation A + Interpretation D. Section 11 concern 7 correctly self-surfaces that Interpretation B alternatives (medication effect on subjective gevoelscore, seasonal effect, correlated symptom-report habit change, participant physiology genuinely changed) are not tested. This is honest surfacing of scope. Not a fire that blocks r1 lock. However, for completeness the audit could name a specific concrete example -- e.g. **the citalopram anchor from memory `feedback_stress_is_garmin_measure`** ("stress = Garmin HRV-derived score; frame all site copy + interpretation that way (load-bearing for the citalopram mechanism + stress -> felt curve)"). If citalopram was initiated near the 2024 -> 2025 boundary (which the memory strongly implies), that would be a specific alternative mechanism for the mean-gs step-jump at section 4 that would compete directly with the composition-shift reading. Recommend the audit surface this specific alternative in section 11 concern 7 at r1 revision (absorb-tier).

**L4.10 Whole-corpus felt-state comparator (§4.4) -- PASSES.** Section 4.4 correctly reports the whole-year mean gs rise (4.10 -> 4.79, +0.69) alongside the rest-day mean gs rise (+0.55 heavy-adj / +0.54 all-corpus) and concludes at section 4.4 fourth paragraph: "Reading: §4 alone does NOT distinguish 'rest-day composition shifted specifically' from 'everything felt better in 2025'. §3 and §5 are the composition-specific tests; §4 confirms the shift exists, does not attribute it to composition specifically." Consistency assessment at section 4.4 tail correctly reads AMBIGUOUS-FOR at the composition-specificity resolution. This is textbook decomposition discipline; the audit avoids the tempting overreach of using §4 as composition-specific evidence when §4.4 shows it is not. Section 11 concern 2 self-surfaces that the comparator is reported as inline paragraph rather than a separate CSV; a proper LC-era-per-year mean-gs CSV would be a strengthening addition (see section 4.5 below), but the current inline treatment is adequate for r1 lock.

**L4.11 2024 residual tension framing (§5) -- SUBSTANTIVE PASS (correctly-surfaced, absorb-eligible).** The 2024 per-year proactive-strategic RR = 0.93 is the biggest tension with the Interpretation A monotone-recovery story. Section 5.3 surfaces two candidate readings (a) small-n artefact vs (b) partial mitigation only, without picking one silently. Section 10.1 second-to-last paragraph restates the tension explicitly ("BUT: the 2024 per-year proactive-strategic RR = 0.93 does not neatly resolve") and pre-commits it to caveat-class-per-CONVENTIONS-section-4.2 handling for any MD-beta r2 revision. Section 11 concern 3 self-surfaces whether the DECLINED-NARRATIVE-ONLY marking per memory `feedback_narrative_only_events` would be more appropriate than DEFERRED. Reviewer call: the 2024 case does have a candidate exit condition (larger n in 2027-2028 if Wave 2C were re-run with fresh data) and is not purely narrative-only, so DEFERRED with caveat-class flag is appropriate; DECLINED-NARRATIVE-ONLY would be over-strong. But the tension is architecturally significant enough that it warrants a formal sub-arc investigation before Stage H commits to any Interpretation-A-anchored pre-reg (see section 4.2 below).

**L4.12 §7 Interpretation-D-partial-falsification framing -- PASSES.** Section 7.3 first paragraph: "Interpretation D's load-envelope shrinkage sub-claim -- 'fewer very-heavy days in 2025-2026' -- is FALSIFIED at the descriptive resolution of this audit." Second paragraph correctly scopes the falsification: "If Interpretation D is to survive, it must survive on the tactical-response sub-claim (§9) or the step-envelope sub-claim (§8), not the very-heavy-frequency sub-claim." Section 10.2 restates this at findings-summary level. Third paragraph at section 7.3 correctly names the day-level-VH-classification limitation as a caveat on the falsification (sub-day intensity structure not captured by day-level operand). This is textbook multi-sub-claim discipline; the audit does not overreach the falsification to the whole Interpretation D. The self-surfaced concern at section 11 concern 4 (whether day-level VH proxy is adequate for the VH-frequency question or whether sub-day bout-level intensity should be a follow-up Wave 2D probe) is a reasonable Stage D companion but not a blocker for r1 lock.

---

## 3. What does not fire (selective)

Non-trivial passes worth stating positively:

- **§5 load-bearing framing discipline**. The pooled RR = 0.354 finding is the strongest descriptive evidence Wave 2C produces and the audit resists all four common overreach patterns: (a) does NOT frame as "supports Interpretation A"; (b) does NOT hide the 2024 non-flip in a "trend is clear except for one year" narrative; (c) does NOT ignore the construct-validity contingency of the >= 5 threshold; (d) does NOT recast the pooled sign-flip as a Stage-D-ready verdict. Section 5.3 last two paragraphs explicitly enforce all four disciplines.

- **§7 partial-falsification restraint**. The temptation to read "VH-fraction rose from 14.2% to 21.2%" as falsifying Interpretation D wholesale is real; the audit correctly restricts the falsification to the sub-claim and preserves the other two sub-claims (envelope + tactical-response) as testable. This is exactly the sub-claim-decomposition discipline that keeps a multi-clause hypothesis empirically-testable rather than a strawman.

- **§4.4 composition-specificity comparator discipline**. The temptation to declare "mean gs on rest-days rose therefore rest-day composition shifted" is strong; the audit correctly checks the whole-corpus mean-gs comparator, finds the rest-day shift is not larger than the whole-corpus shift, and downgrades §4 to CONSISTENT-WITH-at-felt-state-resolution-only + AMBIGUOUS-FOR-at-composition-specificity-resolution. This is the exact form of comparator-check that Daza 2018 counterfactual framing demands for observational n=1 work; it protects against confusing a marginal shift for a compositional shift.

- **§6 endogeneity-isolation framing**. The temptation to read the RR = 4.29 crisis-reactive finding as "evidence AGAINST rest preventing crashes" is real and would be structurally wrong: the crisis-reactive arm is downstream of the crash trajectory, not upstream. Section 6.3 gets this exactly right: "the 'rest' is downstream of the crash risk that materialises in the +5d window; the rest-day is a symptom of the imminent crash trajectory, not a cause of it." The audit correctly frames this as descriptive-CONSISTENT-WITH the confounding-by-indication mechanism (Salas 2001; Kyriacou & Lewis 2016) rather than as evidence against the rest-prevents-crashes reading.

- **Pre-surfaced reviewer concerns at section 11**. Ten reviewer-concerns pre-surfaced by the audit itself, each cited to the section that generated it and mapped to either a Stage D companion or a MD-beta r2 revision-surface question. This is the model of producer-mode auditor self-surveillance; the reviewer's job is mostly to concur or push back at the margins rather than to name new concerns.

- **Producer-mode-revision-surface discipline (section 10.4)**. The revision-surface note is scoped as producer-mode; explicitly does not draft the r2 revision; correctly points at either a rest-day-composition-stratified sensitivity arm or an acknowledgement of rest-day composition as a first-class uncorrected confounder. Section 10.4 last paragraph is exactly the right scope: "This is producer-mode note only; the MD-beta r2 revision itself is a downstream methodology-editing session, not this Wave 2C audit's scope." Concern 10 at section 11 self-surfaces the same question.

---

## 4. What would strengthen this finding

Concrete + named. Each recommendation states expected effect.

### 4.1 (LOAD-BEARING) MD-beta r2 codification of gevoelscore-conditioned definitional pair

**Recommendation**: MD-beta r2 section 3.1 SHOULD codify the gevoelscore-conditioned rest-day operand as a definitional-pair extension per CONVENTIONS section 3.3, adding `rest_day_p25_strategic` (= `rest_day_p25` AND `gevoelscore >= 5`) and `rest_day_p25_crisis` (= `rest_day_p25` AND `gevoelscore <= 3`) alongside the primary + sensitivity operands already locked at r1.

**Rationale**:

- The empirical Wave 2C evidence (pooled RR = 0.354 vs RR = 4.29 across the strategic-crisis split, factor-of-12 divergence) is exactly the kind of composition-driven axis-decomposition that CONVENTIONS section 3.3 definitional-pair discipline exists to codify. The un-conditioned `rest_day_p25` operand is an arithmetic average of two sub-populations with drastically different crash-in-5d risk profiles; running crash-prediction on the un-conditioned operand at Stage D would mix two structurally distinct signals into a single RR that inherits the mixture-weight artefact identified at audit section 6.4.
- Memory `project_rest_day_operand_semantics` bullet 4 already names this as a "Definitional-pair extension candidate ... Decision deferred to descriptive-audit findings on the reactive-vs-proactive-rest quadrant table (Wave 2C)." Wave 2C IS that descriptive-audit finding. The deferral condition is now satisfied.
- Codifying the definitional pair at MD-beta r2 removes the tension flagged at L4.2: §5 + §6 are structurally a definitional pair on the same 341-rest-day pool, and treating them as such rather than as independent tests is the correct discipline per CONVENTIONS section 3.3. Without codification, downstream Stage H pre-regs may inherit the un-conditioned operand and re-import the mixture-weight artefact.
- This is architecturally larger than the Wave 2B review's r2 Path A (which upgraded era + intensity from sensitivity to primary stratifier). Adding a new definitional-pair extension is a structural change to the operand family, closer in magnitude to Path B in the Wave 2B review terminology. If MD-beta r2 combines the Wave 2B Path A upgrade with the Wave 2C definitional-pair extension, that is a **substantial r2** that per MD-beta section 7 compression discipline may require fresh-session re-review before r2 lock.

**Call**: **YES, codify the definitional-pair extension at MD-beta r2**. The Wave 2C evidence justifies the codification and the memory's deferral condition is met. Defer to a later r3 only if the user prefers to keep the Wave 2B Path A upgrade as a minimum-magnitude r2 patch and split the definitional-pair extension into r3; this is a valid staging choice but would leave the gevoelscore-conditioning as an ad-hoc operand-extension for any downstream Wave 2D or Stage D consumer rather than a first-class MD-locked operand.

**Expected effect**: unblocks Stage D with a definitional-pair-clean operand family that separates strategic-vs-crisis rest at the operand level rather than at the Stage-D-analysis level. Prevents downstream synthesis or Stage H pre-reg from re-importing the un-conditioned operand mixture-weight artefact.

### 4.2 (LOAD-BEARING) 2024 residual tension formal sub-arc investigation

**Recommendation**: BEFORE Stage H commits to any Interpretation-A-anchored pre-registration, a **formal sub-arc investigation of the 2024 per-year proactive-strategic RR = 0.93 tension** SHOULD be scoped and run.

**Rationale**:

- The 2024 exception is not a small-n mystery on a well-fitting pattern; it is a genuine tension with the Interpretation-A monotone-recovery story. 2023 flips cleanly (RR = 0.22), 2025 flips cleanly (RR = 0.00), 2026 flips cleanly (RR = 0.00), but 2024 does NOT flip (RR = 0.93). This is not a smooth transition curve; it is a sign-flip PAUSE.
- The audit's two candidate readings (a) small-n artefact vs (b) partial mitigation only are structurally different and would motivate different Stage H frames. Under (a) the pooled RR = 0.354 is straightforwardly consistent with Interpretation A once we accept the 2024 cell as under-powered noise; under (b) the pooled RR = 0.354 is a mixture that ROUNDs to consistent-with-Interpretation-A but has a specific 2024 sub-population where the mechanism does not operate, which invites a Stage-H-shaped question about what changed structurally in 2024 (or what did not change).
- A sub-arc investigation could take multiple concrete shapes: (i) a threshold-sensitivity 2x2 grid on the 2024 sub-arm at gs >= 4, >= 5, >= 6 thresholds to check whether the flip appears at a different threshold; (ii) a within-2024 timeline of proactive-strategic vs crisis-reactive rest-day density to check for sub-year structure (e.g. was the first half of 2024 crisis-dominant and the second half strategic-dominant?); (iii) a rest-before-versus-rest-after decomposition on 2024 to check if the tension is direction-specific; (iv) an intensity-stratified read on 2024 (heavy vs very_heavy end_class) to check if the tension is intensity-carrier-specific.
- Without this investigation the Stage H pre-reg would inherit an unresolved specific counterexample to Interpretation A that a sceptical reviewer will foreground. The Wave 2C audit correctly surfaces it as caveat-class per CONVENTIONS section 4.2 (section 10.1) but that is the descriptive-Stage-1 disposition; a Stage H pre-reg committing to an Interpretation-A-anchored direction pre-commit needs a defensible answer to "why does 2024 not fit?"

**Call**: **YES, scope a 2024 sub-arc investigation before Stage H**. A Wave 2D or Wave 2E audit covering the 2024 tension with the four investigative shapes above (or a defensible subset) is the right scope; running Stage H without it would leave Interpretation A architecturally exposed on a specific empirical counterexample.

**Expected effect**: either resolves the 2024 tension into a defensible sub-hypothesis (e.g. "2024 was a transitional year where the participant was learning to distinguish strategic from crisis rest and the gs >= 5 threshold was not yet calibrated") or surfaces it as a hard limitation of Interpretation A that the Stage H pre-reg must accept up front rather than absorb silently.

### 4.3 (Absorb) Gevoelscore threshold sensitivity companion at Stage D

**Recommendation**: at Stage D, run a threshold-sensitivity companion computing §5 pooled RR at three additional thresholds: (a) strategic = gs >= 4 (borderline-inclusive strategic); (b) strategic = gs >= 5 AND crisis = gs <= 4 (borderline-inclusive crisis); (c) strategic = gs >= 6 (strict-strategic-only). Report as `proactive_strategic_rest_crash_2x2_threshold_sensitivity.csv`.

**Rationale**: audit section 5.4 correctly names the concern but does not run the companion. The Wave 2C audit's discipline scope is Stage -1 descriptive (section 1), so a threshold-sensitivity companion is out of scope for r1 lock but is exactly the natural Stage D extension per MD-beta section 3.10 definitional-pair discipline.

**Expected effect**: establishes the robustness envelope of the §5 pooled sign-flip. If RR remains below 1.0 across all three sensitivity thresholds, the >= 5 threshold is a defensible primary; if RR crosses 1.0 at >= 4 or >= 6, the threshold contingency is a first-class caveat that any downstream Stage H must inherit.

### 4.4 (Absorb) Absolute-step-threshold rest-day operand companion

**Recommendation**: at Stage D, run a companion §5 + §6 analysis with an absolute-step-threshold rest-day operand (e.g. `total_steps < 3000` or another concrete threshold pre-committed at MD-beta r2) alongside the current rolling-p25 operand. Report as `proactive_strategic_rest_crash_2x2_absolute_threshold.csv`.

**Rationale**: audit section 9.3 second-to-last paragraph correctly names the moves-with-envelope artefact. The rolling p25 threshold shifts with the mean-step trend, so "rest-day" in 2025-26 is a different absolute-step level than in 2023-24. If the §5 pooled sign-flip and §7 falsification survive on the absolute-step operand as well as the rolling-p25 operand, that meaningfully strengthens the composition-shift story; if they do not survive, the artefact is load-bearing on the audit's headline findings.

**Expected effect**: separates the operand-invariant composition-shift finding from any moves-with-envelope artefact. Discretionary; not blocking for r1 lock.

### 4.5 (Absorb, discretionary) Section 4.4 LC-era-per-year mean-gs CSV

**Recommendation**: emit `lc_era_mean_gevoelscore_per_year.csv` for the whole-corpus felt-state comparator currently reported as inline paragraph at section 4.4. Include n_days_valid, mean, median, and per-year Wilson-CI-analogue (bootstrap 95% CI on the mean, per parent MD-beta section 3.6 machinery).

**Rationale**: audit section 11 concern 2 self-surfaces the question. The inline paragraph is adequate for r1 lock but a proper CSV would let downstream consumers audit the +0.69 whole-year shift vs the +0.55 rest-day shift claim directly. Also enables comparison against the corpus-baseline crash rate per year, which is a natural cross-check for the crash-rate collapse pattern that Interpretation D is trying to explain.

**Expected effect**: gives downstream synthesis a proper anchor for the composition-specificity question rather than requiring re-computation from the source per_day_master.csv.

### 4.6 (Absorb, discretionary) Section 11 concern 7 -- name the specific citalopram alternative

**Recommendation**: at r1 revision, add to section 11 concern 7 a specific named alternative mechanism -- **the citalopram / SSRI initiation timeline per memory `feedback_stress_is_garmin_measure`**. If citalopram was initiated near the 2024 -> 2025 transition, that would be a specific mechanism-level alternative for the mean-gs step-jump at section 4 that competes directly with the composition-shift reading and that any downstream Interpretation-B section would need to address.

**Rationale**: audit section 11 concern 7 is abstractly correct but names the "Interpretation B" alternative in generic terms only. A specific concrete named alternative (with a specific timeline that the user's memory anchors) is much stronger and gives the Stage H reviewer a specific alternative to test rather than a general "medication effect" placeholder.

**Expected effect**: sharpens the alternative-mechanism completeness check from a generic placeholder into a specific empirically-testable competing hypothesis.

---

## 5. Verdict

**DEFENSIBLE with revision.**

The Wave 2C audit is a high-quality Stage -1 descriptive audit that correctly operationalises Interpretation A + Interpretation D as partial-testable at n=1, produces the load-bearing §5 pooled sign-flip finding (RR = 0.354) with rigorously honest framing that avoids all four common overreach patterns, correctly frames §6 endogeneity-isolation (RR = 4.29) as descriptive-CONSISTENT-WITH the confounding-by-indication mechanism (Salas 2001) rather than as evidence against rest-prevents-crashes, correctly restricts §7 VH-fraction falsification to the sub-claim rather than to Interpretation D wholesale, and applies §4.4 composition-specificity comparator discipline that correctly downgrades §4 from composition-specific evidence to felt-state-improved evidence. The 2024 per-year proactive-strategic RR = 0.93 residual tension is surfaced honestly with two candidate readings rather than absorbed into a monotone-recovery narrative. Zero-vs-NaN + physical-rest-only + named-count + caveat-class disciplines are all followed. Two load-bearing recommendations for MD-beta r2 (definitional-pair codification per section 4.1; 2024 sub-arc investigation per section 4.2) are architecturally significant and warrant fresh-session re-review before r2 lock if combined with the Wave 2B Path A upgrade. No BLOCKING issue found; the audit is safe to lock at r1 with the mechanical clarifications from section 4.3-4.6 as absorb-tier and the r2 revision-surface owned architecturally rather than by this audit.

---

## Methodology footer

This review walks the 4-layer checklist defined in [`reviews/README.md`](README.md), which inherits from:

- **Layer 1**: SCRIBE 2016 items 3-5, 14, 18, 22-24 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/)); STROBE 2007 items 6, 12, 13 ([literature/methodology/vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf)).
- **Layer 2**: Daza 2018 self-tracked n-of-1 counterfactual ([literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)); Personal Science norms; project memory `project_garmin_research_bias_boundary` for held-out-structure framing.
- **Layer 3**: Natesan Batley et al. 2023 systematic review ([literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf)); WWC 2022 SCED handbook v5.0; CENT 2015 (Shamseer et al.). L3 is largely N/A at Stage -1 descriptive scope; the rolling-baseline moves-with-envelope artefact is the one time-series-specific concern that fires.
- **Layer 4**: [CONVENTIONS.md](../CONVENTIONS.md) sections 3.1 (personal baseline), 3.3 (definitional pair), 3.6 (named counts), 4.2 (caveat-class vs a-priori); memory `project_rest_day_operand_semantics` for the physical-rest-only semantic constraint and definitional-pair-extension deferral condition; memory `feedback_stress_is_garmin_measure` for the specific citalopram alternative mechanism named at section 4.6; memory `feedback_narrative_only_events` for the DECLINED-NARRATIVE-ONLY vs DEFERRED disposition on the 2024 tension.

Confounding-by-indication epidemiological anchor: Salas M et al. 2001; Kyriacou DN & Lewis RJ 2016 *JAMA* (both cited by MD-beta section 3.9 confound 1, re-cited by parent Wave 2B audit sections 7.2 + 9.3, and re-cited by target Wave 2C audit sections 2.1 + 6.3).

**Reviewer discipline**: fresh-session; cold context; read target audit + companion `scripts/audit.py` + all 7 output CSVs (spot-checked `proactive_strategic_rest_crash_2x2.csv`, `crisis_reactive_rest_crash_2x2.csv`, `rest_day_gevoelscore_quadrants_per_year.csv`, `very_heavy_frequency_per_year.csv`, `rest_day_mean_gevoelscore_per_year.csv`, `step_envelope_variance_per_year.csv`, `heavy_gap_to_next_rest_per_year.csv` -- all reproduce the audit's cited numbers byte-for-byte) + MD-beta LOCKED r1 + Wave 2B sister audit + Wave 2B review report + CONVENTIONS + memory `project_rest_day_operand_semantics` + `reviews/README.md` from disk. NO edits to target audit, MD-beta, CONVENTIONS, or memory.
