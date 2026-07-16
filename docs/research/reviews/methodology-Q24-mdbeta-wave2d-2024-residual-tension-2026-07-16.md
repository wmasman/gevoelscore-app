# Methodology review: Q24 MD-beta Wave 2D descriptive audit -- 2024 residual tension investigation

**Target artefact**: [`analyses/descriptive/Q24-mdbeta-wave2d-2024-residual-tension/audit.md`](../analyses/descriptive/Q24-mdbeta-wave2d-2024-residual-tension/audit.md) DRAFT r0 2026-07-16 (producer-mode Stage -1 descriptive audit per [CONVENTIONS section 1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs)).

**Review type**: Producer-mode methodology-adjacent review; 4-layer checklist walk per [`reviews/README.md`](README.md) plus Wave 2D-specific structural checks. Sister to [`methodology-Q24-mdbeta-wave2c-reactive-vs-proactive-rest-2026-07-16.md`](methodology-Q24-mdbeta-wave2c-reactive-vs-proactive-rest-2026-07-16.md) (Wave 2C parent), [`methodology-Q24-mdbeta-precursor-rest-streak-2026-07-16.md`](methodology-Q24-mdbeta-precursor-rest-streak-2026-07-16.md) (Wave 2B), and [`methodology-Q24-mdalpha-precursor-phase-intensity-2026-07-16.md`](methodology-Q24-mdalpha-precursor-phase-intensity-2026-07-16.md) (MD-alpha Wave 2A).

**Reviewer**: fresh-session Claude (Opus 4.7) under user delegation. Cold context. Read target audit.md + companion `scripts/audit.py` (801 lines) + all 9 output CSVs + parent Wave 2C audit LOCKED r1 + parent Wave 2B audit LOCKED r1 + MD-beta LOCKED r1 + MD-alpha §3.1 + MD-alpha Wave 2A audit §8 + CONVENTIONS §§1-5 + `reviews/README.md` 4-layer spec from disk. No exposure to drafting session context; doc-only knowledge.

**Discipline**: reviewer-mode per [CONVENTIONS section 1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations). NO edits to target audit, MD-beta, MD-alpha, CONVENTIONS, memory, or sister audits. Verdict for producer-mode artefact per this doc's section 5.

---

## 1. What the data shows

Empirical claims made by the target audit, plain restate (interpretive framing separated in section 2). All numbers cross-verified against `output/*.csv` byte-for-byte.

1. **2024 tension recap (audit section 1)**. The tension inherited from Wave 2C section 5.1: pooled proactive-strategic (PS) RR = 0.354; 2023 RR = 0.223; 2024 RR = 0.929 (3/15 vs 14/65 on the K=3 rest-after primary + gs >= 5 + no-crash-in-3d-lookback subset); 2025 RR = 0.000; 2026 partial RR = 0.000. 2024 is the outlier year among four in which the pre-committed sign-flip does not appear.

2. **§3 per-quarter within-2024 partial signal**. 2024 PS crashes concentrate in Q2 (1/3, narrative-only) and Q3 (2/5 = 40%, viable_n_min5 borderline, Wilson [11.8, 76.9]). Q1 (0/1) and Q4 (0/6) carry zero PS-True crashes; Q4 aligns with the 2025 zero pattern.

3. **§4 by-intensity within-2024 LOAD-BEARING signal**. All 3 of the 2024 PS-True crashes are on `end_class = very_heavy` (RR = 3.500 on n=6 with Wilson [18.8, 81.2]); zero PS-True crashes on `end_class = heavy` (n=9, RR = 0.000). Directionally strong stratification; wide CI on the RR estimate.

4. **§5 per-episode diagnostic on n=3 crash events + n=12 non-crash baseline (narrative-only)**. All 3 crash cases: very_heavy end_class, gs=5 exactly on rest-day, short streak (1-2d), first-crash 3-4 days after episode-end, elevated pre-window 30d effective_exertion_min (mean 214.7 min), low subsequent-7d exertion (2-10 min). Non-crash baseline (n=12): gs=5 exactly is universal too (not distinguishing); 7/12 heavy vs 5/12 very_heavy end_class; pre-window 30d mean 114.8 min.

5. **§6 threshold sensitivity within 2024**. strict_gs_ge_6: **0 PS-True episodes in 2024** (no rest-day in the K=3 window carried gs >= 6). primary_gs_ge_5: RR = 0.929. loose_gs_ge_4: RR = 0.536 (n=35 PS-True, adds 20 gs=4 rest-days + 2 crashes). Direction moves toward pre-committed under loose threshold.

6. **§7 absolute-step operand narrows but does not resolve the 2024 tension**. Under `total_steps < 3000` rebuild: pooled RR shifts 0.354 -> 0.111; 2024 RR shifts 0.929 -> 0.652 (n=7 PS-True with 1 crash); 2023 RR shifts 0.223 -> 0.000 (clean flip preserved). 2024 tension narrows ~30% under abs operand, still non-zero.

7. **§9 pre-window cumulative-load 2x separation within 2024 PS-True**. 30d pre-window effective_exertion_min sum: crash mean 214.7 vs non-crash mean 114.8 (ratio 1.87x, median 206 vs 108 = 1.91x). vigorous_min 30d sum: crash 44.0 vs non-crash 27.2 (1.62x mean, 2.24x median). total_steps 30d sum: 167k vs 155k (1.08x, weak).

8. **§10 neighbouring-year composition anomaly on 2023 pre-window activity**. Per-year PS-arm mean pre-window effective_exertion_min per day: **2023 = 26.28**; 2024 = 4.49; 2025 = 5.15. Mean gs-on-rest-day flat across years (5.05 / 5.00 / 5.22). Mean streak length: 2023 = 1.40 / 2024 = 1.27 / 2025 = 2.09.

9. **§11 joint (b) + (e) reading**. The audit concludes the evidence is most consistent with a joint mechanism of (b) partial-mitigation via pre-window cumulative load + (e) intensity-interaction residual, while acknowledging both are strong-consistent + sample sizes do not distinguish.

10. **§12 three-path r2 codification surface**. Path R2A (minimal, caveat-only), R2B (joint end_class stratifier + pre-window covariate deferred), R2C (joint end_class stratifier + pre-window covariate both codified). Audit surfaces the three; refuses to pick.

11. **§13 reviewer-concerns pre-surfaced (n=12)**. Includes the 2023 pre-window activity anomaly at item 8, flagged as unexplained.

---

## 2. What fired and why

Layer-grouped fires with citation, magnitude, and absorb-vs-escalate signal per fire.

### Layer 1 -- Universal reporting (SCRIBE 2016; STROBE 2007)

**L1.1 Operationalisation traceability -- PASSES with high confidence.** Audit §1, §2, §3, §4, §6, §7, §9 each state operand + threshold + source-CSV filename in the same paragraph. `scripts/audit.py` is idempotent, well-commented (54-line docstring), and RANDOM_SEED declared per MD-beta §3.6 even though not exercised. Every audit table verifies byte-for-byte against the emitted CSV (spot-checked §4 by-intensity, §9 pre-window load, §10 neighbouring context). Row-total checks are explicit at §3.1 (Q1+Q2+Q3+Q4 = 80 = 2024 ALL) and §4.1 (heavy + very_heavy = 39+41 = 80). **Absorb**: none needed.

**L1.2 Framing not-overclaiming -- PASSES with high confidence.** All findings are labelled CONSISTENT-WITH / AMBIGUOUS-FOR / FALSIFYING per the §2 pre-declared framing. Load-bearing §4 finding (RR = 3.50 on 2024 very_heavy PS-True) is framed as CONSISTENT-WITH candidate (e) not as verdict; §4.4 explicitly caveats "n = 6 ... Wilson [18.8, 81.2] very wide". Load-bearing §9 finding (2x pre-window separation) is framed as CONSISTENT-WITH candidate (b) with the narrative-only + n=3 caveat repeated in §5.5 + §9.2 + §9.3. §11.2 joint reading is qualified as "sample sizes do not distinguish them cleanly". No drift into causal or verdict language. **Absorb**: none needed.

**L1.3 Deviation-from-parent-audit documentation -- PASSES.** §2 recaps the five candidate readings verbatim from parent Wave 2C §5.3 + reviewer L10.5 extension. Inheritance-only claims (corpus counts, heavy-day definition, rest-day operand) are pointer-only to parent Wave 2B / parent Q24 MD, not re-emitted. §7.3 explicitly references the Wave 2C §5.5 moving-target artefact concern that motivated the abs-step companion. **Absorb**: none needed.

**L1.4 Named counts per [CONVENTIONS §3.6](../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file) -- PASSES with a small tightening opportunity.** All cell counts carry scheme (K=3 rest-after primary, PS subset) + unit (episode / rest-day / event) + source-CSV filename. Only borderline: §9's per-episode aggregate statistics use the phrase "3 events on 3 episodes on 3 rest-days on 3 dates" (§5.5) which is exemplary; §10.1's "n_PS_ep" column label matches the neighbouring_context CSV column. **Absorb**: none required; §5.5 is a positive precedent.

### Layer 2 -- Observational n=1 (Daza 2018; Personal Science norms)

**L2.1 Counterfactual framing partial-testable at n=1 -- PASSES.** §2 explicitly declares the five candidate readings as partial-testable at n=1 and pre-commits CONSISTENT-WITH / AMBIGUOUS-FOR / FALSIFYING as the only reading modes. §11.1 walks each candidate and applies the framing consistently. This is exactly the reading discipline Daza 2018 §3 requires when a randomised counterfactual is unavailable. **Absorb**: none needed.

**L2.2 Stationarity acknowledgment -- SUBSTANTIVE FIRE (absorb-tier, load-bearing patch recommended).** §10.3 flags the 2023 pre-window activity anomaly (mean 26.28 vs 4.49 in 2024 and 5.15 in 2025) and labels it "flagged as reviewer concern for fresh-session walk" with two candidate readings: (i) real behaviour change or (ii) data-artefact. **BOTH proposed readings are incomplete.** The MD-alpha methodology MD §3.1 documents the four LC recovery phases with `citalopram_modulated` starting exactly 2024-04-09 -- a 100% temporal confound with the calendar-year axis used in §10.1. The MD-alpha Wave 2A audit §8 pre-window mean-level table reports per-phase `effective_exertion_min` pre-window means of 9.50 (`lc_pre_ergo`) -> 27.78 (`pacing_pre_citalopram_learning`) -> **19.39** (`pacing_habit_established`) -> **5.17** (`citalopram_modulated`). The 2023 PS-arm mean of 26.28 is within the mean-median band of the pre-citalopram phases (which cover most of 2023 up to 2024-04-08); the 2024 mean of 4.49 and 2025 mean of 5.15 sit inside the `citalopram_modulated` phase (2024-04-09 -> 2026-06-05). The "anomaly" is the KNOWN citalopram-onset step, not an unexplained artefact. **Magnitude**: high; the framing gap propagates into §12.3 (pre-window covariate recommendation would be applied on absolute values across the phase boundary, giving a systematic bias). **Absorb**: patch §10.3 to name the citalopram phase-boundary anchor and cite MD-alpha §3.1 + MD-alpha Wave 2A audit §8. Patch §12.3 to require phase-standardisation or phase-stratification for any pre-window covariate at MD-beta r2. Wave 2D §9 within-2024 finding is UNAFFECTED (within-year comparison stays inside `citalopram_modulated`); the anchor patch is a framing correction not a numerical revision.

**L2.3 Calendar-time vs subject-time separation -- PASSES.** Per-quarter analysis (§3, §8) uses D_end's calendar quarter, consistent across years. Pre-window 30d is anchored on D_start_idx (script `_pre_window_load_metrics` at line 392). No subject-time drift risk in the operand construction. **Absorb**: none needed.

**L2.4 Data provenance traceability -- PASSES.** Every table cites its source CSV filename in the §-header paragraph. `INPUT = DATA_PATH / "unified" / "per_day_master.csv"` at script line 70 anchors the whole pipeline. **Absorb**: none needed.

### Layer 3 -- Time-series-specific (Natesan 2023; WWC 2022; CENT 2015)

**L3.1 Autocorrelation reporting -- N/A for Stage -1 descriptive.** Wave 2D reports per-cell 2x2s + Wilson CIs on rates, no permutation nulls or lag-carryover models. The episode unit (gap=0 heavy runs) inherently collapses adjacent-day dependency at the day resolution; per-quarter and per-year strata further reduce within-stratum lag structure. No autocorrelation escalation warranted at Stage -1. **Absorb**: none needed.

**L3.2 Rolling-baseline moves-with-envelope caveat -- PASSES via §7 companion.** §7 executes the Wave 2C §5.5 L3.2-absorbed abs-step companion test. §7.3 correctly frames the finding: pooled sign-flip strengthens under abs (RR 0.354 -> 0.111); 2024 residual narrows ~30% (0.93 -> 0.65) but survives; 2023 clean flip preserved. §7.4 correctly concludes the rolling-baseline artefact is NOT the dominant driver of the 2024 tension. **Absorb**: none needed.

### Layer 4 -- Project-specific audit hooks (CONVENTIONS §3)

**L4.1 Personal baseline + zero-vs-NaN -- PASSES.** `is_crash.fillna(False).astype(bool)` at script line 102 per §3.10 discipline. Gevoelscore NaN preserved via `_bucket_from_gs` returning `"nan"` bucket (script line 249). `rest_day_p25` NaN preserved via `np.where(... isna, np.nan, ...)` (script line 117-121). Attestation in §14 explicitly asserts zero-vs-NaN discipline inherited from parent. Spot-check: script `_pre_window_load_metrics` uses `.fillna(0).sum()` for aggregation (line 409-411), which is a **legitimate zero-treatment for sum aggregation** (Garmin missingness on activity minutes typically encodes zero-activity days, not un-instrumented days on LC-era corpus with full coverage). This does not violate §3.10 given the coverage attestation in MD-alpha Wave 2A audit §7.3 (100% coverage on `effective_exertion_min` across all four phases). **Absorb**: none needed; a footnote at §9 explicitly naming the fillna(0) convention as sum-aggregation-safe would tighten the trail but is not required.

**L4.2 Caveat-class vs a-priori-class per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) -- PASSES.** §12.4 explicitly qualifies "Wave 2D does NOT recommend abandoning the gevoelscore-conditioning primary operand" -- flags the 2024 residual as caveat-class not falsification. §11.1's per-candidate summary uses CONSISTENT-WITH / AMBIGUOUS-FOR labels throughout, never elevates a candidate to verdict. §11.3 uses SUPPORTS / FALSIFIES / LEAVES AMBIGUOUS at the r2-codification-decision level, not at the mechanism-verdict level. **Absorb**: none needed.

**L4.3 Definitional-pair discipline per [CONVENTIONS §3.3](../CONVENTIONS.md#33-one-column-per-definitional-pair) -- SUBSTANTIVE FIRE (absorb-tier, framing clarification recommended).** Wave 2D tests four different characterisations of the 2024 residual: §5 per-episode features, §6 threshold sensitivity, §7 absolute-step operand, §9 pre-window load. §3 (per-quarter) and §4 (by-intensity) add two more stratifications. These are **not one definitional pair each**; they are complementary characterisations that partially overlap in the constructs they measure. The §11.1 per-candidate summary treats each characterisation as evidence for a candidate reading, which is the right frame -- but the audit does not explicitly name that §6 (threshold sensitivity) and §9 (pre-window cumulative load) are testing DIFFERENT constructs (both relate to candidate (b) partial-mitigation but through different channels: gs-boundary construct-validity vs pre-window load channel). Reader could conflate them as independently-evidencing the same thing. **Magnitude**: low-medium; the §11.2 "joint (b) + (e)" reading is at risk of overfitting two separate mechanism-hypotheses to n=3 crash events. **Absorb**: patch §11.2 or §12.5 to explicitly acknowledge that §6 and §9 test different channels of candidate (b), and that the "joint (b) + (e)" reading treats §4 + §9 as the two primary CONSISTENT-WITH signals with §6 as a corroborating direction-check. This is a framing tightening, not a numerical revision.

**L4.4 Narrative-only for n=3 per memory `feedback_narrative_only_events` -- PASSES.** §5 explicitly discloses "n = 3 is narrative-only per parent Stage -1 audit threshold. The per-episode diagnostic is reported as a descriptive table + narrative observations; NO inferential statistic is computed on the 3-vs-12 comparison" (§5 preamble). §9.3 repeats the caveat: "Wilson-style CIs are not applicable to means (this is a per-episode-level aggregate)". §11.1 (a) explicitly flags §3 Q3 (2/5) as "sample sizes drop below n_min5 in Q1 and Q2 ... Q3 has Wilson [11.8, 76.9]; overlaps RR = 1 heavily". **Absorb**: none needed.

**L4.5 Prior-driven vs post-hoc per [CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-post-hoc-testing-is-exploratory) -- PASSES with note.** Wave 2D is explicitly **exploratory** (§1 discipline-scope): "The five candidate readings of the 2024 exception are treated as partial-testable at n=1: findings can be described as CONSISTENT-WITH, AMBIGUOUS-FOR, or FALSIFYING for each candidate reading, but no test in this audit constitutes a verdict on any of them." The five candidates come from the parent Wave 2C §5.3 pre-committed candidate frame, not from post-hoc data-mining -- so the reading is confirmatory-consistent-with even though the audit does not carry verdict weight. The §12.2 + §12.3 recommendations for MD-beta r2 codification are labelled as recommendations from a descriptive audit into a downstream methodology decision, not as themselves verdicted. **Absorb**: none needed.

---

## 3. What does not fire (selective)

Layer items that explicitly pass with non-trivial evidence. Skips trivially-passing items.

- **L1.2 not-overclaiming** passes despite two load-bearing findings (RR = 3.50 on §4; 2x pre-window separation on §9) that could tempt overclaiming. The audit's discipline in stopping at CONSISTENT-WITH labels is a positive signal; the §12.4 explicit "does NOT recommend abandoning the gevoelscore-conditioning primary operand" is exactly the caveat-class disposition [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) requires.
- **L2.1 partial-testable-at-n=1** passes with the §2 pre-declaration of reading modes + §11.1 per-candidate walk. The audit's explicit refusal to force a single-winner reading in §2 ("The audit does not force a single-winner reading") is the correct application of Daza 2018 §3 counterfactual discipline.
- **L4.2 caveat-class** passes with the §12.4 "does NOT recommend" list -- exactly the disposition [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) contrasts with a-priori claims.
- **L4.4 narrative-only** passes with n=3 discipline stated in §5 preamble + §9.3 CI-not-applicable caveat + §11.1 (a) Wilson-CI overlap note.
- **Reproducibility** (script byte-identity + idempotency + declared seed) passes cleanly, matching the precedent set by parent Wave 2C audit that reached LOCKED r1 on the same criteria.

---

## 4. What would strengthen this finding

Constructive close. Concrete, named, pointing at existing methodology MDs or audit-script paths where possible.

### 4.1 [LOAD-BEARING (a)] Citalopram phase-boundary reading for §10.3 anomaly

**Recommendation**: patch §10.3 to name the citalopram-onset step (2024-04-09) as the mechanistic explanation for the 2023 vs 2024/2025 pre-window activity gap. Anchor the patch at [MD-alpha methodology MD §3.1](../methodology/post_heavy_day_pacing_learning.md) recovery_phase table (phases + boundary dates) and [MD-alpha Wave 2A audit §8](../analyses/descriptive/Q24-mdalpha-precursor-phase-intensity/audit.md#8-per-phase-pre-window-mean-level-table-md-alpha-35-level-vs-change-discipline) pre-window `effective_exertion_min` table.

The relevant numbers side-by-side:

| Phase (MD-alpha §3.1) | Date range | Wave 2A §8 pre-window mean `effective_exertion_min` (min/day) |
|---|---|---:|
| `pacing_habit_established` | 2022-11-17 -> 2024-04-08 | **19.39** |
| `citalopram_modulated` | 2024-04-09 -> 2026-06-05 | **5.17** |

Wave 2D §10.1 reports per-year PS-arm mean pre-window `effective_exertion_min` per day of 26.28 (2023) / 4.49 (2024) / 5.15 (2025). 2023 sits inside `pacing_habit_established`; 2024's mean of 4.49 is a mixture of `pacing_habit_established` (~Q1 + early Q2) and `citalopram_modulated` (from 2024-04-09 onward, dominating the year); 2025's mean of 5.15 sits fully inside `citalopram_modulated`. The 2023 PS-arm mean of 26.28 is elevated above the phase mean of 19.39 because Wave 2D operates on a **subset** (PS-True arm only, n=20 for 2023) rather than the full episode pool (n=125 in `pacing_habit_established`); the subset selection is expected to further elevate the pre-window load on the PS arm (PS = no crash in prior 3d AND gs >= 5, which conditions on episodes that were followed by a "capable" rest-day, plausibly correlated with sustained higher pre-window intensity).

**Reading**: the 2023 anomaly is the KNOWN citalopram baseline shift, not an unexplained data artefact. Reading (i) in §10.3 ("real behaviour change") is closer to correct than reading (ii) ("data-artefact"), but neither is complete without the phase-boundary anchor.

**Downstream implication for §12.3 codification** (also load-bearing; feeds §4.2 below): the pre-window covariate recommendation must be phase-standardised or phase-stratified at MD-beta r2, NOT applied on absolute-value cut-points across the citalopram boundary. The descriptive separation Wave 2D reports at ~200 min (crash) vs ~115 min (non-crash) on the 30d effective_exertion sum is **within `citalopram_modulated`** (all 3 crash cases are 2024-04-26, 2024-07-11, 2024-08-24 per §5.1 -- all post-citalopram-onset). This within-phase comparison is defensible; but a Stage H pre-registration that applies the ~150-180 min cut-point suggested by §9.4 across 2023 episodes would systematically misclassify 2023 as "high load" almost universally, because pre-citalopram phases sit at absolute levels 4-6x higher.

**Wave 2D §9 within-2024 finding is UNAFFECTED**: it is a within-year (and thus within-phase, since all 3 crashes are post-2024-04-09) comparison. The patch is a framing correction not a numerical revision, and applies only to §10.3 + §12.3 wording.

### 4.2 [LOAD-BEARING (b)] Codification path recommendation: R2B (joint-stratifier extension)

**Recommendation**: MD-beta r2 should adopt **Path R2B (joint end_class stratifier; pre-window covariate deferred to Stage H)** rather than R2A (minimal) or R2C (full extension). Reasoning below.

**Why not R2A (minimal, caveat-only)**: R2A leaves the §4 finding (RR = 3.50 on 2024 very_heavy PS-True, 3/3 crashes on very_heavy end_class) as a caveat-line in a footnote. This is defensible on [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) grounds if the §4 signal were only directional; but the signal has an internal replication (§5.2 "all 3 events are very_heavy end_class" as a per-episode feature) and inherits from parent Wave 2B §10 whole-corpus intensity stratification (heavy RR = 2.07 vs very_heavy RR = 0.96). This is not a lone n=6 fragile finding; it is a converging descriptive pattern across two audits.

**Why not R2C (full extension, joint-stratifier + pre-window covariate codified)**: the pre-window covariate is load-bearing per §5 + §9 but faces the citalopram phase-boundary concern raised in §4.1 above. Codifying it at MD-beta r2 requires either (i) phase-standardisation (which the audit does not compute) or (ii) phase-stratification (which multiplies the definitional-pair count and stresses [CONVENTIONS §3.3](../CONVENTIONS.md#33-one-column-per-definitional-pair) discipline). Neither is worked-through at Wave 2D resolution. R2C also risks overfitting two mechanism-hypotheses (b) + (e) to n=3 crash events; the joint reading is the audit's own §11.2 preferred interpretation but §11.2 itself qualifies "sample sizes do not distinguish them cleanly".

**Why R2B**: the joint end_class stratifier (heavy vs very_heavy) is (i) already partially codified via parent Wave 2B §13.10 Path A upgrade to end_class + era as primary stratifiers at MD-beta r2; (ii) supported by two audits (Wave 2B + Wave 2D) reading the same pattern from different angles; (iii) NOT sensitive to the phase-boundary confound at §4.1 (end_class stratification operates within-episode, not across the citalopram boundary). The pre-window covariate can be deferred to a Stage H pre-registration on its own definitional-pair with an explicit phase-standardisation decision at that point, informed by the §4.1 patch reading.

**Concrete r2 codification suggestion for the MD-beta r2 author**:

- Add `rest_adjacency_2x2_by_endclass` as a joint primary reporting cut per Wave 2D §12.2 (stratify simultaneously by rest-day gevoelscore bucket AND end_class).
- Cite Wave 2D §4 + Wave 2B §10 as the two converging descriptive anchors.
- Add a note that pre-window cumulative-load is a candidate covariate for Stage H, deferred pending phase-standardisation decision, with the citalopram-phase anchor named per §4.1 above.
- Keep the §12.4 discipline: do NOT abandon gevoelscore-conditioning as primary operand; the 2024 residual is a caveat-class refinement not a falsification.

Precedent for this shape: Wave 2C §10.5 reviewer L10.5 extension made a specific YES on codifying `rest_day_p25_strategic` + `rest_day_p25_crisis` as a definitional pair; the Wave 2D r2-path decision is the natural next step of that precedent.

### 4.3 Framing tightening (non-blocking)

Two smaller items that would tighten the trail without changing numerics:

- **§9 fillna(0) footnote**: name the sum-aggregation-safe convention (with a pointer to MD-alpha Wave 2A audit §7.3's 100% coverage attestation on `effective_exertion_min`) so a fresh reader does not confuse `fillna(0).sum()` at script line 409-411 with a violation of [CONVENTIONS §3.10 zero-vs-NaN](../CONVENTIONS.md#310-operationalisation-faithful-to-the-data-not-just-to-the-description).
- **§11.2 joint-reading clarification**: patch to explicitly acknowledge that §6 threshold sensitivity and §9 pre-window load test DIFFERENT channels of candidate (b) partial-mitigation (gs-boundary construct-validity vs pre-window load channel), and that the "joint (b) + (e)" reading treats §4 + §9 as the two primary CONSISTENT-WITH signals with §6 as a corroborating direction-check. Not a numerical revision; a framing precision that prevents readers from conflating §6 and §9 as independently-evidencing the same construct.

### 4.4 §13 reviewer-concern dispositions

Walking §13 item-by-item with reviewer-disposition:

- **Item 1 (§3 per-quarter Q3 concentration)**: adequately caveated. §3.3 explicitly qualifies "sample sizes are tiny (Q4 n = 6 on PS-True arm), Wilson CIs overlap heavily". §11.1 (c) explicitly reads Q3 as "descriptively consistent but not distinguishable from a Q3-outlier reading at n = 5 PS-True episodes". No further tightening required.
- **Item 2 (§4 RR = 3.50 with wide CI)**: CONSISTENT-WITH framing is correct. Do not upgrade to a firmer framing at Wave 2D descriptive resolution; the wide CI is exactly what the framing acknowledges.
- **Item 3 (§5 narrative-only n=3)**: adequately caveated per L4.4 above.
- **Item 4 (§5 rest-day date privacy)**: dates are already in the source corpus + prior audits emit them; aligned with prior convention.
- **Item 5 (§6 strict_gs_ge_6 zero-observation)**: adequately handled. §6.4 correctly concludes strict-only is sample-limited and cannot be a primary Stage H operand. Whether to check 2023 / 2025 / 2026 strict-threshold availability as a companion is a nice-to-have for Wave 2D r1 lock but not blocking (the 2024 zero-observation is itself sufficient to disqualify strict as primary).
- **Item 6 (§7 abs-step narrows only modestly)**: "modest not dominant" framing is correct. A ~30% reduction (0.93 -> 0.65) is meaningful but leaves the residual non-zero + still carries a crash-event, so the moving-target artefact is correctly not attributed as the dominant driver.
- **Item 7 (§9 2x separation at n=3 vs n=12)**: descriptively load-bearing enough to justify §12.3 pre-window covariate as a candidate for Stage H (not for MD-beta r2 codification without the phase-standardisation patch per §4.1 above). The reviewer's escalation is to R2B not R2C per §4.2 above.
- **Item 8 (§10.3 2023 anomaly)**: **NOT sufficient as a "flagged as reviewer concern" caveat**; the citalopram phase-boundary reading per §4.1 above is load-bearing and should be named in §10.3 + §12.3 as a patch.
- **Item 9 (§11.2 joint (b) + (e) reading)**: appropriate multi-candidate framing per §2 discipline; §4.3 above proposes a small tightening.
- **Item 10 (§12 recommendations)**: appropriately narrow. §12.1-§12.4 point at codification decisions rather than draft the codification; §12.5 explicitly defers the R2A/R2B/R2C choice to the r2 author. §4.2 above proposes R2B as the r2-path but this is the reviewer's recommendation, not a Wave 2D verdict.
- **Item 11 (descriptive-only discipline)**: honoured across all sections; no verdicts, no p-values, Wilson CIs on all rates.
- **Item 12 (narrative-only for n=3)**: applied consistently in §5 + §9 + §11.

---

## 5. Verdict

**DEFENSIBLE with revision.**

Wave 2D is a methodologically rigorous descriptive audit that resolves the 2024 residual tension from Wave 2C to a level sufficient for MD-beta r2 codification, subject to two load-bearing framing patches (§10.3 citalopram phase-boundary anchor + §12.3 phase-standardisation requirement for the pre-window covariate) and one r2-path recommendation (Path R2B: joint end_class stratifier now, pre-window covariate deferred to Stage H). The highest-priority fire is L2.2 stationarity acknowledgment: the §10.3 "2023 pre-window activity anomaly" is the well-documented citalopram-onset step at 2024-04-09, not an unexplained artefact, and the framing gap propagates into §12.3's r2 codification recommendation. No numerical revisions required; framing patches only. Fresh-session reviewer walk of Wave 2D r1 (post-absorption) is unnecessary if the two patches land cleanly + §11.2 tightening per §4.3 is applied; the r0 -> r1 lock precedent from Wave 2C absorption confirms this shape of methodology-review absorption is standard.

**Highest-priority fires per layer**:

- Layer 1: none (all L1 items pass).
- Layer 2: L2.2 stationarity (§10.3 citalopram phase-boundary reading).
- Layer 3: none (L3.1 N/A; L3.2 passes via §7 companion).
- Layer 4: L4.3 definitional-pair discipline (§11.2 joint-reading channel-clarity tightening).

---

## Methodology

Fresh-session Claude (Opus 4.7) walked the 4-layer checklist from [`reviews/README.md`](README.md) against the target audit's DRAFT r0. Read from disk: target audit.md (571 lines), `scripts/audit.py` (801 lines), 9 output CSVs (spot-checked §4 by-intensity, §9 pre-window load, §10 neighbouring context byte-for-byte against tables), parent Wave 2C audit LOCKED r1 (§5.1, §5.3, §5.5, §10.5 for reading-precedent), parent Wave 2B audit LOCKED r1 (§10 for intensity-stratification precedent), MD-beta LOCKED r1 (§3.1, §3.6, §3.7 for operand + primary-direction lock), MD-alpha §3.1 (recovery_phase axis + boundary dates for L2.2 fire), MD-alpha Wave 2A audit §8 (per-phase pre-window `effective_exertion_min` table for L2.2 fire), CONVENTIONS §§1-5 for role-split + audit-hook citations. No exposure to drafting-session context; doc-only knowledge per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations) fresh-session reviewer discipline. Report structure follows [`reviews/README.md`](README.md) 5-section template. NO edits to target audit, MD-beta, MD-alpha, sister audits, CONVENTIONS, or memory. Verdict tier applied per producer-mode methodology-adjacent review convention (DEFENSIBLE / DEFENSIBLE with revision / REVISION RECOMMENDED / BLOCKING) rather than the reviewer-mode PASS / PASS with caveats / REVISION RECOMMENDED spec, matching precedent set by sister Wave 2A, 2B, and 2C reviews on the same date.
