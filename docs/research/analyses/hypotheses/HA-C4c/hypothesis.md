# HA-C4c — Substantive Wiggers C4 retest at bout-level resolution ("stress fails to drop during rest periods after overexertion — stuck sympathetic")

## Authorship

**Drafted 2026-06-23** by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem.

**Drafting trigger**: the bout-level cascade is unblocked-with-calibration-caveat per [HA11-bout-redo result](../HA11-bout-redo/result.md) PARTIAL verdict 2026-06-23 (commit `6e06d12`; Bars 1+2 PASS at +20.26pp / median signed z 2.410; Bar 3 FAIL at p=0.2609 — a power-shortfall at n_calm=70/n_crash=11 stratum, NOT a signal failure). The cascade-resuming substantive Wiggers C4 retest at bout resolution is now drafted per [HA11-bout-redo §9.2](../HA11-bout-redo/hypothesis.md#92-partial-exactly-2-of-3-5-bars-met--framework-validity-gate-partial): *"HA-C4c drafting UNBLOCKS with explicit calibration caveat naming bar 3 (block-perm p<0.05 at n_calm=70/n_crash=11 stratum) as the failing bar"*. The parent methodology MD ([`bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md), LOCKED `c57ff3f` 2026-06-21) §1.3 names HA-C4c as the enabled-at-lock substantive Wiggers C4 retest at bout resolution.

**Verification log** (anchors the draft on the current state of the cascade):

- Read parent MD `bout_level_recovery_dynamics.md` at worktree commit `d39aa55`. §1.3 enabled-at-lock register row confirmed; §3 bout-detection rule LOCKED verbatim; §4 per-bout feature set LOCKED verbatim (the per-day aggregation `bout_n_did_not_return_day` is one of six per-day aggregations); §5.3 Approach A definition + §5.5 framework-validity restriction to unmedicated confirmed.
- Read sub-MD `bout_level_dose_response_calibration.md` at worktree commit `d39aa55`. §6 inheritance table populated; **0/7 features CONFIRMED at this corpus's bout-level n** → Approach A is NOT load-bearing for any downstream HA pre-reg at this corpus's bout-level n; primary outcome MUST be dose-naive per the §6 architectural-implications paragraph.
- Read [HA11-bout-redo result](../HA11-bout-redo/result.md) at commit `6e06d12`. PARTIAL verdict on bars 1+2 PASS / bar 3 FAIL at the n_calm=70/n_crash=11 stratum; transient-excluded sensitivity arm degrades discrimination to +11.69pp; **motion-clean-only arm degenerate** because 4285/4317 bouts (99.3%) carry `motion_confound_flag=True` — a corpus-property finding that the entire HA-C4c operand inherits.
- Read [HA-C4 v2 hypothesis.md + result.md](../HA-C4/) — daily-aggregate REJECTED 2026-06-18 (triad sum 0.0/3.0; commit `52bddb5`), but Channel 1's `stress_post_peak_drop_avg` SUPPORTED on BOTH eras + Channel 1 + Channel 2 primary SUPPORTED on validate. The signal IS detectable at finer resolution; bout-level operationalisation is the pivot per HA-C4 v2 §9 REJECTED branch.
- Read [STOCKTAKE §6 architectural-implications paragraph](../../../STOCKTAKE.md#6-cross-section-synthesis) for the cross-phase pooling permission at this corpus's bout-level n + the dose-naive primary framing.

**Locked decisions at draft time** (the 7 operationalisation pre-commits surfaced from the handoff; each defended below + cross-referenced to the §4 measurement protocol subsection where it applies):

1. **Operand: `bout_n_did_not_return_day` per-day count** (parent MD §4 aggregation). Defined as the per-day count of detected bouts with `did_not_return_flag == True` (per parent MD §3.2: bouts whose stress did not return to within +5 of `pre_bout_baseline` for ≥10 consecutive minutes within 180 minutes after peak). **Single-operand framing** (NOT 3-channel triad). Rationale: most direct match for Wiggers C4 verbatim language *"stress doesn't decrease for a long time"* + *"stuck sympathetic"* (PDF lines 1140-1141, 1223-1231 per the register entry); each within-day bout with `did_not_return_flag=True` IS by construction a "stress failed to drop within the rest window" event. Single-operand cleaner than HA-C4 v2's 3-channel triad (which contributed to v1's INCONCLUSIVE-handling overhead at lock + the v2 REJECTED reading at daily aggregate). Alternatives considered + rejected as primary: (a) `bout_recovery_half_life_median_day` (per-day median of per-bout recovery half-lives) — sensitive to the bulk-distribution shape, BUT the Wiggers C4 claim is about the *failure* tail (stress that doesn't drop AT ALL), which is exactly what `did_not_return_flag` isolates; the median collapses the tail into the bulk. (b) 3-channel triad mirroring HA-C4 v2 (`bout_n_did_not_return_day` + `bout_recovery_half_life_median_day` + cross-checks) — adds verdict-shape complexity for diminishing returns when the substantive Wiggers C4 claim is well-captured by a single operand at this resolution; the HA-C4 v2 lesson is that the 3-channel triad added INCONCLUSIVE-handling overhead without buying clearer interpretability. See §4.1.

2. **Stratum: cross-phase pooled on the `citalopram_phase` axis (`citalopram_phase(d) ∈ {unmedicated, buildup, consolidation, afbouw, post_afbouw}`) as primary**, restricted on the `recovery_phase` axis to sub-phase 4b (`pacing_habit_established`) + phase 5 (`citalopram_modulated`) per the §4.2 left-edge cross-axis layering; **unmedicated-only (`citalopram_phase == unmedicated`) as a primary sensitivity arm** for cross-test consistency with HA11-bout-redo's reference frame. Rationale: per recalibration §6 inheritance table + STOCKTAKE §6 architectural-implications paragraph (with the 2026-06-23 naming-discipline note at commit `4b53ea1` clarifying that the boundary at issue is `unmedicated → buildup` on the `citalopram_phase` axis = `sub-phase 4b → phase 5` on the `recovery_phase` axis), cross-phase pooling across the `unmedicated → buildup` (= 4b → 5) boundary is permissible at this corpus's bout-level n without §5.A/B/C inheritance violation — 0/7 features CONFIRMED → Approach A is NOT load-bearing → no inheritance binding at the per-bout layer. Pooling gains ~70 day-clusters of n (per STOCKTAKE §6) which is exactly the dimension HA11-bout-redo's bar 3 failed on (n_calm=70/n_crash=11). Unmedicated-only sensitivity arm preserves cross-test comparability with HA11-bout-redo (same stratum). Alternatives considered + rejected as primary: (a) unmedicated-only — preserves cross-test reference frame BUT inherits the same n_crash~11 power constraint that broke HA11-bout-redo's bar 3 in the calibration; HA-C4c would face the same power problem. (b) per-citalopram-phase stratified (separate verdicts in unmedicated + buildup + consolidation + afbouw) — n-per-phase too thin for bout-level work at this corpus; meta-combine introduces multiplicity. See §4.2.

3. **Verdict shape: single-operand SUPPORTED / PARTIAL / REJECTED with explicit INCONCLUSIVE handling** (n-shortfall routing per §4.7 walk-forward gate). Inherits the INCONCLUSIVE-aware pattern from [HA-C4 v2 §5.3](../HA-C4/hypothesis.md#53-triad-verdict-rule-v2-rewritten-with-explicit-inconclusive-handling) — a single-operand collapse of HA-C4 v2's per-channel CONFIRMED/CONFIRMED-PARTIAL/REFUTED ladder. SUPPORTED requires both discrimination + effect-size bars met in the predicted direction; PARTIAL is the descriptive band for direction-correct-but-effect-or-significance-fails; REJECTED is direction-wrong or both bars fail; INCONCLUSIVE is n-shortfall. See §5.

4. **Block-permutation E[L] = 7 days** inherited from [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) per parent MD §5.1 inheritance + the project canonical default. Data-driven E[L]\* companion reported with factor-of-2 flag per CONVENTIONS §3.6. See §4.6.

5. **Crash-drop sensitivity required** per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-row-for-any-same-day-correlation); surface |Δ effect-size| > 5pp (mirrors HA11-bout-redo's 5pp threshold; absolute pp on the heavy-T-vs-non-heavy-T discrimination is the comparable operand) as a §3.4 finding ("the heavy-T signal is crash-driven, not robust across the broader heavy-T pool"). Verdict per §5 is unchanged; crash-drop is informative-for-interpretation. See §4.10.

6. **Holm step-down across sensitivity arms**: primary + 3 sensitivity arms = 4 cells in the Holm family (unmedicated-only sensitivity + motion-clean-only sensitivity + transient-excluded sensitivity). The Approach A dose-adjusted sensitivity arm (§4.9) is reported alongside but NOT in the Holm family because it is a different inferential machinery (dose-adjusted predictor rather than a sub-set restriction). Apply Holm at α=0.05 across the primary + 3 sub-set sensitivity arms; report alongside the uncorrected primary per [HA-C4 v2 §5.5](../HA-C4/hypothesis.md#55-holm-step-down-across-channels-locked-within-test-multiplicity-correction-verbatim-from-v1) pattern (Holm is a fragility-flag secondary, not verdict-driving). See §4.6 + §5.

7. **Approach A sensitivity-arm form**: per recalibration §6 inheritance — since `bout_n_did_not_return_day` was NOT in the recalibration's 7-feature scope (it was implemented downstream of the recalibration's scope; the closest analogues are `bout_n_per_day` NULL + `bout_n_fast_recovery_day` weakly_consistent), the Approach A inheritance applies **via the closest-analogue feature with a sensitivity inheritance**: use `bout_n_fast_recovery_day`'s buildup-post-CPAP β = −0.056/mg [95% CI −0.145, +0.034] as the inheritance template (sign-concordant prior, weakly_consistent verdict; per sub-MD §6 the inheritance default for sensitivity-arm purposes). The Approach A sensitivity arm computes `bout_n_did_not_return_day_adj(d) = bout_n_did_not_return_day(d) − β_inherited × dose_plasma_mg(d)` and re-runs the primary procedure with this dose-adjusted operand. Report alongside the primary; explicitly named as inheritance-by-analogue (NOT inheritance-by-recalibration on the operand itself), with a §8 caveat naming this as a pre-spec sensitivity rather than a load-bearing dose-correction. See §4.9.

**Mandatory dispatches at lock-blocking gate level** (per [`hypothesis_lock_process.md` §3.2 step 4 + §3.8 gates](../../../methodology/hypothesis_lock_process.md)):

- **Power-calc dispatch**: power calc inapplicable per [Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) within-subject design. The block-permutation null at E[L]=7 (per §4.6) is the within-subject inferential machinery; the §5 verdict bars determine the substantive verdict rather than asymptotic-power thresholds; INCONCLUSIVE cells are sample-size shortfalls per §4.7 walk-forward gate.
- **Single-cell headline lock**: the headline is the single triple {bout-level test on `bout_n_did_not_return_day` × cross-phase-pooled on `citalopram_phase` axis (= sub-phase 4b + phase 5 on `recovery_phase` axis per §4.2) × heavy-T-vs-non-heavy-T} evaluated against the §5 SUPPORTED/PARTIAL/REJECTED bars; sensitivity arms (unmedicated-only, motion-clean-only, transient-excluded, baseline-invalid-excluded, crash-drop, Approach A dose-adjusted) are diagnostic only and cannot promote to SUPPORTED independently per the single-cell headline-lock discipline.

**§3.8 lock-blocking gate-verification template** (per [`hypothesis_lock_process.md` §3.8](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc); the lock-commit message will confirm each — currently UNFILLED at draft):

| gate | requirement | status at draft | confirmation at lock |
|---|---|---|---|
| **Gate 1** — Power-calc dispatch | §8 carries either explicit calc or the one-line Daza 2018 within-subject dispatch | Daza 2018 dispatch present in §8 caveat 1 + Authorship "Mandatory dispatches" | [to confirm at lock] |
| **Gate 2** — Multi-comparison discipline | Single-cell headline lock OR explicit Bonferroni-style correction | Single-cell headline lock per Authorship "Mandatory dispatches"; Holm step-down across sensitivity arms is secondary fragility-flag report only | [to confirm at lock] |
| **Gate 3** — Register-row pointer | Wiggers C4 register row updated at lock OR explicit non-supersession confirmation | HA-C4c is a substantive Wiggers C4 retest at bout-level resolution; the C4 register row already forward-points at parent MD `bout_level_recovery_dynamics.md` as available infrastructure (per parent MD §7.1); HA-C4c lock-commit will ADD a forward-pointer to HA-C4c's hypothesis.md as the lock-stage substantive retest at bout-level (HA-C4 v2 daily-aggregate REJECTED verdict pointer stays; pointers coexist) | [to confirm at lock + register update] |
| **Gate 4** — Re-audit clean OR §3.6 compression | r2 re-audit cleanly closed OR compression decision documented in lock-commit message per §3.6 acceptability criteria | **MET** — fresh-session re-audit `docs/research/reviews/HA-C4c-2026-06-23-v2-reaudit.md` returned PASS-with-caveats with NO Layer fires (L1-L4 all clean across 5+3 verified surfaces; r2 absorb closed all 3 r1 fires cleanly + §4.9 reordering structurally enhanced in audit-endorsed direction); 2 optional precision items at §4 explicitly NOT gating per re-audit Section 4; LOCK via §3.6 compression criteria satisfied. | confirmed at lock |

**Revision log**:

| rev | date | notes |
|---|---|---|
| r1 | 2026-06-23 | Initial drafting (`d59352c`) per cascade-resuming substantive Wiggers C4 retest at bout resolution; unblocked by HA11-bout-redo PARTIAL framework-validity verdict (`6e06d12`) + β-recalibration r4 0/7 CONFIRMED LOCKED (`fb97d1c`). Drafted 7 operationalisation pre-commits per the cascade-context discipline; 4 cascade-context caveats baked in load-bearingly at §8. |
| r2 | 2026-06-23 | Substantive absorb of fresh-session audit fires (REVISION RECOMMENDED; report [`reviews/HA-C4c-2026-06-23.md`](../../../reviews/HA-C4c-2026-06-23.md) commit `5f79bd1`): (1) L1.2 BLOCKING column-confusion fix at 5 surfaces (§1 + §4.2 + §6 + §10.2 + §3.8 gate table's supporting Authorship "Locked decisions" item 2 + "Mandatory dispatches" single-cell headline lock); the labels `pacing_habit_established` + `citalopram_modulated` are `recovery_phase` values (NOT `citalopram_phase` values), corresponding to sub-phase 4b + phase 5 (NOT 5 + 6); primary stratum re-stated as cross-phase pooled on `citalopram_phase` axis (`{unmedicated, buildup, consolidation, afbouw, post_afbouw}`) with explicit sub-phase 4b + phase 5 cross-reference to `recovery_phase` axis where relevant per `lc_recovery_phase_axis §1.3` layering; upstream STOCKTAKE §6 fix already in main at commit `4b53ea1` (naming-discipline note inline); §6 phase-numbering also corrected to canonical 1/2/3/4a/4b/5 per `lc_recovery_phase_axis §2`. (2) L4.7 substantive §4.9 framing slip — reordered to lead with the underpowered-NULL framing (5-surface precedent from [`reviews/bout_level_dose_response_calibration-r3-2026-06-22.md` §3](../../../reviews/bout_level_dose_response_calibration-r3-2026-06-22.md)) before the sign-flip mechanics; the inheritance-by-analogue is now explicitly framed as a **descriptive companion** using the analogue β as a coefficient-of-convenience, NOT a CONFIRMED dose-correction; the CI-bracket sub-arm is named as inheritance-fragility, NOT a substantive precision check. (3) L3.3 minor Holm shrunk-family disclosure sentence added at §5.3 per [HA-C4 v2 §5.5 r2 fewer-comparisons absorb](../HA-C4/hypothesis.md) precedent. **r2 status: drafted, NOT locked** per user-selected Option γ — fresh-session re-audit follows before LOCK to safety-check the 5-surface propagation. No changes to §5 falsification bars, §9 branching pre-spec, or methodology MDs. |

**Status**: **r2 LOCKED 2026-06-23 by user acceptance + fresh-session re-audit clean** (Option γ closure). Re-audit at [`reviews/HA-C4c-2026-06-23-v2-reaudit.md`](../../../reviews/HA-C4c-2026-06-23-v2-reaudit.md) returned PASS-with-caveats with NO Layer fires; all 3 r1 fires (L1.2 BLOCKING 5-surface column-confusion, L4.7 §4.9 framing slip, L3.3 Holm shrunk-family disclosure) closed cleanly per the r2 substantive absorb at `310e145`; 2 optional precision items at §4 explicitly NOT gating. Cascade gate now closes per §6 of `bout_level_recovery_dynamics.md`: HA-C4c is the substantive Wiggers C4 bout-level retest; test execution is the next post-lock session.

---

## 1. Claim

**The substantive Wiggers C4 retest at bout resolution**: on heavy-exertion days (T-conditioning per HA-C4 v2 §4.1: `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T) within the **cross-phase-pooled stratum on the `citalopram_phase` axis** (`citalopram_phase(d) ∈ {unmedicated, buildup, consolidation, afbouw, post_afbouw}`; equivalently `recovery_phase(d) ∈ {sub-phase 4b (pacing_habit_established), phase 5 (citalopram_modulated)}` per the cross-axis layering per [`lc_recovery_phase_axis.md §1.3`](../../../methodology/lc_recovery_phase_axis.md#13-relationship-to-existing-axes--three-layers); LC era 2022-04-04 → present, excluding April 2024 cluster per §6), the per-day operand `bout_n_did_not_return_day` is **systematically higher** on heavy-T days than on non-heavy-T days. The directional prediction is one-sided elevated: heavy-T days produce more bouts whose stress fails to return to baseline within the 180-minute post-peak window — Wiggers' verbatim *"stress doesn't decrease for a long time"* (PDF lines 1140-1141) read as a per-day count of within-day "stuck stress" events.

**Headline cell**: cross-phase-pooled-on-`citalopram_phase`-axis stratum × `bout_n_did_not_return_day` × heavy-T-vs-non-heavy-T × Mann-Whitney U + Cliff's delta + block-permutation null at E[L]=7 × verdict bands per §5.

**Verdict rule** (single-operand SUPPORTED/PARTIAL/REJECTED with explicit INCONCLUSIVE handling; per §5):

- **SUPPORTED**: (a) block-permutation p < 0.05 (one-sided elevated direction) AND (b) Cliff's delta ≥ +0.20 in the predicted positive direction.
- **PARTIAL**: direction-correct AND (one of (a) or (b) clears, the other does not) AND (a) survives the calibration discount per §8 caveat 2 (i.e. is interpreted with the HA11-bout-redo calibration discount visible).
- **REJECTED**: direction wrong-sign OR both (a) and (b) fail OR effect collapses under §4.10 crash-drop sensitivity (|Δ Cliff's delta| > 0.20 in the direction-flipping sense, indicating the entire heavy-T signal is crash-driven).
- **INCONCLUSIVE**: either arm has fewer than 30 days post-eligibility per §4.7 walk-forward gate, OR the dry-run §10.4 sanity gates fail.

## 2. Why we think this

Three priors anchor the substantive prediction at bout resolution:

1. **Wiggers source-verified verbatim** (per the [C4 register entry](../../../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic) batch 2 2026-06-12, PDF lines 1112-1119, 1140-1143, 1223-1231, 1306-1314). Five passages directly support the within-day "failure to recover" framing the bout-level `did_not_return_flag` operand isolates:

   - *"Going so far beyond your limits that your resting heart rate remains elevated and your stress level doesn't decrease for a long time & PEM"* (PDF lines 1140-1141, Walls of Stress) — direct support for per-bout failure-to-return semantics; `did_not_return_flag=True` is the per-bout instance of *"stress level doesn't decrease for a long time"*.
   - *"Stuck in Stress. When you've done something and then lie down, you want to see blue again. Sometimes, usually when your nervous system is a bit unstable due to, for example, PEM or low blood volume, your stress remains high"* (PDF lines 1223-1231) — explicit reference to the within-day stress-recovery failure pattern; bouts that exceed the 180-minute return-window cap are the per-event instantiation.
   - *"Complete walls of orange ... sustained high state"* (PDF lines 1112-1119) — the descriptive companion at within-day resolution; each `did_not_return` bout is a 180-minute-plus segment of "sustained high state".
   - *"It would be great if living a calmer life, pacing yourself better, and doing more relaxing things would instantly give you days full of blue. Unfortunately, that's not how it works. Usually, you have to take it easy for a while before your body finds its peace again"* (PDF lines 1306-1314) — recovery-takes-time framing; the per-day count `bout_n_did_not_return_day` quantifies how often within-day recovery fails.
   - Adrenaline-lingers mechanism *"Our theory is that the body produces too much adrenaline when overdoing things. Especially if you overdo it every day. It lingers for a long time"* (PDF lines 1316-1324) — Wiggers' explanatory mechanism; not a separate hypothesis but the conceptual frame the operand operationalises.

2. **HA-C4 v2 daily-aggregate REJECTED + Ch1 alternative `stress_post_peak_drop_avg` SUPPORTED on BOTH eras** (commit `52bddb5` 2026-06-18). The triad sum was 0.0/3.0 at daily-aggregate level — REJECTED — but the per-cell pattern is informative: Channel 1's `stress_post_peak_drop_avg` companion (per HA-C4 v2 §4.11) SUPPORTED on both eras at +0.210 / +0.364 Cliff's deltas, AND Channel 1 + Channel 2 primary SUPPORTED on validate. The within-day signal IS detectable at finer resolution; the daily-aggregate operationalisation collapses the within-day decay shape into a scalar by construction. Per HA-C4 v2 §9 REJECTED branch: *"C4 mechanism would need different operationalisation (e.g. bout-level recovery curves)"* — that operationalisation is now this pre-reg's primary operand.

3. **HA11-bout-redo PARTIAL framework-validity** (commit `6e06d12` 2026-06-23): the bout-level operand reproduces HA11 v1's discrimination magnitude cleanly (+20.26 vs +22.8 pp; median signed z 2.410 vs 2.168 — both within 12% of the HA11 v1 reference) — Bars 1 (directional sign) + 2 (effect-size comparability) PASS. The framework-validity gate confirms the per-bout extraction at the methodology level: the operand can re-detect a signal we have independent evidence for. Bar 3 (block-permutation p) FAILED at p=0.2609, but this is a **power constraint at n_calm=70/n_crash=11**, not a signal failure — the calibration caveat baked into §8 makes this propagation explicit.

**Sister-test context** establishes additional priors:

- **HA-C4b v3 NOT-SUPPORTED** on the motion-filter crash-precursor framing — a per-episode crash-precursor test on the stress-with-low-motion COUNT primitive. HA-C4c tests a different question on a different metric: not "does the pattern predict crashes" but "does the per-day count of within-day failure-to-return bouts differ between heavy-T and non-heavy-T days at all". A SUPPORTED-at-HA-C4c-and-NOT-SUPPORTED-at-HA-C4b shape is consistent with the *protective-rather-than-predictive* alternative reading from HA-C4b v3 §9 (the pattern exists but isn't a per-episode crash precursor because the participant uses Garmin as a live pacing signal).
- **HA11 v1 SUPPORTED-on-train** (within-day stress U-dip count, +22.8 pp discrimination, median signed z = 2.168) — the *inverse* of "stuck stress" (sharp recovery rather than failure to recover). The U-dip is what the participant looks like on calm days; `bout_n_did_not_return_day` is what the participant looks like on heavy days (predicted). The two operands triangulate the same Wiggers C4 claim from opposite sides at bout resolution.
- **Four SUPPORTED autonomic-deviation precursors on train** (H02b stress spike count, H02d sentinel-corrected spike, HA06b RHR z-score, HA11 U-dip count) all fired in the unmedicated phase. The autonomic-dysregulation prior is substantial at daily-aggregate resolution; HA-C4c is the bout-level operationalisation of the same underlying autonomic-state question.

## 3. Data sources

- **Primary operand** `bout_n_did_not_return_day` — per-day count of bouts with `did_not_return_flag == True` per parent MD §3.2 + §4. Joined into `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` from `per_bout_master.csv` via the bout-extraction pipeline ([`pipeline/02_features/extract_stress_bouts.py`](../../../pipeline/02_features/extract_stress_bouts.py), LOCKED `d5b394c` 2026-06-22). Emits `0` on valid days with no `did_not_return` bouts; emits blank (NaN) on §3.4-invalid days per the pipeline README.
- **Per-bout source data** `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.csv` (4,317 bouts across 1,479 valid days per the LANDED 2026-06-22 pipeline run; bout-level flag fields used for §4.10 sensitivity arm re-aggregation: `motion_confound_flag`, `transient_flag`, `baseline_invalid_flag`, `did_not_return_flag`).
- **Heavy-T classification** `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T per [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) + v3.2 lagged-baseline conventions (verbatim inheritance from HA-C4 v2 §4.1). Coverage ~83% within LC era.
- **Citalopram phase / dose** — `citalopram_phase(d)` ∈ {unmedicated, buildup, consolidation, afbouw, post_afbouw} + `dose_plasma_mg(d)` (PK-smoothed plasma exposure) per [`citalopram_phase_stratification.md §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification). Used for §4.2 stratum definition + §4.9 Approach A sensitivity arm.
- **`crash_v1` crash labels** — used by the §4.10 crash-drop sensitivity arm per CONVENTIONS §3.4. Source: [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv).
- **β-recalibration inheritance** — [`bout_level_dose_response_calibration.md §6`](../../../methodology/bout_level_dose_response_calibration.md) populated r3/r4 inheritance table 2026-06-22 (commit `d9c6fa4`) + 2026-06-23 r4 reconciliation (commit `fb97d1c`). Source CSV: `$GEVOELSCORE_DATA_PATH/unified/bout_level_dose_response_calibration_results.csv`. The `bout_n_fast_recovery_day` buildup-post-CPAP β coefficient is the inheritance template for the §4.9 Approach A sensitivity arm (since `bout_n_did_not_return_day` itself was not in the recalibration's 7-feature scope — see Authorship "Locked decisions" item 7 + §8 caveat for the inheritance-by-analogue framing).

**No new FIT-level extraction required.** All inputs are in `per_day_master.csv` + `per_bout_master.csv` post-pipeline-run `d5b394c`, plus `labels_crash_v2.csv` for the §4.10 sensitivity arm.

## 4. Measurement protocol

### 4.1 Operand definition (locked pre-commit per Authorship "Locked decisions" item 1)

**Primary operand**: `bout_n_did_not_return_day` — per-day count of bouts with `did_not_return_flag == True` per parent MD §3.2.

The per-bout `did_not_return_flag` fires when the 180-minute forward cap from `t_peak` is reached without the stress trace returning to within +5 of `pre_bout_baseline` for ≥10 consecutive minutes. Per parent MD §3.2 this IS the Wiggers-C4-positive per-event case ("this bout's recovery exceeded the observation window"). The per-day count `bout_n_did_not_return_day` aggregates these per-bout positives over the day, producing an integer (0 if no `did_not_return` bouts on the day; NaN on §3.4-invalid days per the pipeline README).

**Transient handling**: per parent MD §3.1 r2 absorb, **transient bouts are INCLUDED in the primary operand** without down-weighting (the parent MD's pre-committed default; structural determinism). HA11-bout-redo's transient-fragility finding (discrimination drops from +20.26 pp to +11.69 pp under transient exclusion) is acknowledged at §8 caveat 5; HA-C4c reports the transient-excluded sensitivity arm at §4.10 as a parallel.

**Direction-of-effect under SUPPORTED**: `bout_n_did_not_return_day` is HIGHER on heavy-T days than on non-heavy-T days (one-sided elevated per §1).

### 4.2 Stratum (locked pre-commit per Authorship "Locked decisions" item 2)

**Primary stratum**: cross-phase pooled on the [`citalopram_phase` axis](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification) — `citalopram_phase(d) ∈ {unmedicated, buildup, consolidation, afbouw, post_afbouw}` per `citalopram_phase_stratification §3`. The 2024-04-09 `unmedicated → buildup` boundary on this axis (equivalently `sub-phase 4b (pacing_habit_established) → phase 5 (citalopram_modulated)` on the [`recovery_phase` axis](../../../methodology/lc_recovery_phase_axis.md) per `lc_recovery_phase_axis §3.4b + §3.5`; the two axes layer per `lc_recovery_phase_axis §1.3`) is **not load-bearing for bout-level analyses at this corpus's bout-level n** per the recalibration's 0/7 CONFIRMED finding ([sub-MD §6 architectural-implications paragraph](../../../methodology/bout_level_dose_response_calibration.md) + [STOCKTAKE §6 architectural-implications paragraph](../../../STOCKTAKE.md#6-cross-section-synthesis) + 2026-06-23 naming-discipline note at STOCKTAKE §6 commit `4b53ea1`). Pooling across the `unmedicated → buildup` boundary (equivalently the 4b → 5 boundary on the recovery axis) gains ~70 day-clusters of n; permissible without §5.A/B/C inheritance violation per recalibration §6 (0/7 features CONFIRMED → Approach A NOT load-bearing → no per-channel inheritance binding for bout-level operands at this n).

**Stratum exclusions**:

- Phase 1 (`pre_illness_healthy`), phase 2 (`acute_infection`), phase 3 (`lc_pre_ergo`), sub-phase 4a (`pacing_pre_citalopram_learning`; the LC pacing-learning sub-phase BEFORE the 8-week-post-ergotherapie boundary, per `lc_recovery_phase_axis §3.4a`) on the recovery axis — pre-LC-era or pre-pacing-stable; out of scope per parent MD §3.4 device-baseline-lag rule + the bout-extraction pipeline's day-validity gate. (Per [`lc_recovery_phase_axis §2`](../../../methodology/lc_recovery_phase_axis.md) the canonical recovery-axis numbering is 1/2/3/4a/4b/5 with no phase 6; sub-phase 4a covers 2022-09-22 → 2022-11-17, the immediate pre-stratum window before HA-C4c's 2022-11-17 left edge.)
- Phase 4a/4b sub-boundary at 2022-11-17 (the 8-week-post-ergotherapie M1 lived-experience boundary per [`lc_recovery_phase_axis.md §3.4b`](../../../methodology/lc_recovery_phase_axis.md)) demarcates the left edge of HA-C4c's primary stratum: only sub-phase 4b (`pacing_habit_established`) + phase 5 (`citalopram_modulated`) enter on the recovery axis. On the `citalopram_phase` axis this is equivalent to: the entire `citalopram_phase ∈ {unmedicated, buildup, consolidation, afbouw, post_afbouw}` enum is in scope, restricted to days `>= 2022-11-17` (recovery_phase `>= pacing_habit_established`) per the §6 exclusion rules.

**Primary sensitivity arm — unmedicated-only stratum**: `citalopram_phase(d) == unmedicated` only (equivalently the `recovery_phase(d) == pacing_habit_established` slice restricted to days before the 2024-04-09 citalopram start; LC era 2022-04-04 → 2024-04-08, further restricted to days `>= 2022-11-17` per the §6 sub-phase 4b left-edge; excluding April 2024 cluster per §6). Mirrors HA11-bout-redo's reference frame for cross-test consistency; reported per §4.10.

### 4.3 Heavy-T eligibility (verbatim from HA-C4 v2 §4.1)

A day `T` is a **heavy-T candidate** if `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T. A day is a **non-heavy-T candidate** if `exertion_class_lagged_lcera ∈ {none, light, moderate}` on T. Days with missing exertion classification are excluded from the comparison.

**Note vs HA-C4b**: HA-C4b conditioned on `heavy/very_heavy` on T OR T-1 (union, capturing crashes triggered by exertion on either day). HA-C4c conditions on T only (per HA-C4 v2 §4.1 pattern), more conservative; the chain-T+1 question (HA-C4 v2 Channel 3) does not arise for a same-day per-day operand like `bout_n_did_not_return_day`.

### 4.4 Day-validity gate (verbatim from parent MD §3.4 + HA-C4 v2 §4.3)

A day `T` enters the comparison if all of:

1. `T` is in the LC era (`>= 2022-04-04`) AND in the primary stratum per §4.2.
2. `T` is NOT in the April 2024 cluster (`2024-04-09 → 2024-04-16`) — structurally unanalysable per [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md).
3. `T` is NOT in the first 21 days of `has_garmin_uds=True` coverage (device-baseline-lag per parent MD §3.4).
4. `T` has computable `bout_n_did_not_return_day` (i.e. non-NaN per the pipeline §3.4 day-validity gate: ≥ 600 valid per-minute stress samples on `T`).
5. `T` has computable `exertion_class_lagged_lcera` (i.e. heavy-T classification is non-NaN).

### 4.5 Chain-T+1 exclusion (NOT APPLICABLE for HA-C4c)

The chain-T+1 exclusion in HA-C4 v2 §4.7 applies to Channel 3's `awake_stress_avg[T+1]` cross-day operand. HA-C4c's primary operand `bout_n_did_not_return_day` is a **same-day per-day count on T only**; no T+1 cross-day reference is involved. Chain-T+1 exclusion is informational only — included here for HA-C4 v2 cross-reference completeness, but does NOT restrict the HA-C4c primary cell.

### 4.6 Statistical machinery (locked pre-commits)

For the primary cell + each sensitivity arm:

1. **Mann-Whitney U statistic** on `bout_n_did_not_return_day` values: heavy-T arm vs non-heavy-T arm. One-sided (heavy-T > non-heavy-T per §1 directional prediction).
2. **Cliff's delta** as the non-parametric effect size: `delta = (n_heavy>non − n_heavy<non) / (n_heavy × n_non)`. Range [-1, +1]; positive = heavy-T > non-heavy-T.
3. **Block-permutation null at E[L]=7 days**: per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) + parent MD §5.1 inheritance. Permute the binary `is_heavy_T[d]` label sequence in geometric-distributed blocks (mean E[L]=7 days) while keeping the per-day `bout_n_did_not_return_day` values in their original temporal positions. Empirical one-sided p-value = `(1 + #{U_null >= U_observed}) / (B + 1)` with B = 10,000 null draws.
4. **Cell SUPPORTED** if: empirical p < 0.05 AND Cliff's delta ≥ +0.20 in the predicted positive direction (per §5 verdict rule).

**Seed**: `RANDOM_SEED = 20260623` (HA-C4c distinct seed; distinct from HA-C4 v2's `20260618` + HA11-bout-redo's `20260622` + HA-C4 v1's `20260617` + HA-C4b v3's `20260615`, to keep HA-C4c's null distribution independently reproducible from sister tests' archived nulls).

**E[L]\* data-driven companion** + **factor-of-2 flag** per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) + CONVENTIONS §3.6: compute the data-driven `E[L]*` on `bout_n_did_not_return_day[d]` over the primary stratum; flag if `|E[L]* − 7| / 7 > 0.5`. The flag is descriptive context only (does NOT modify the §5 verdict); per the empirical anchor in parent MD §5.1 r2 absorb (6/7 Stratum-4 cells fire the factor-of-2 flag on HA-P6 channels), the flag is expected to fire and is not a halt trigger.

**Holm step-down across sensitivity arms** (per Authorship "Locked decisions" item 6): the Holm family is {primary, unmedicated-only sensitivity, motion-clean-only sensitivity, transient-excluded sensitivity} = 4 cells. Holm cutoffs at α=0.05: α/4, α/3, α/2, α/1. The dose-adjusted Approach A sensitivity arm (§4.9) is NOT in the Holm family (different inferential machinery); baseline-invalid-excluded + crash-drop are NOT in the Holm family (descriptive variants per CONVENTIONS §3.3 column-duplication discipline + §3.4 audit-hook scope). The Holm result is REPORTED alongside the uncorrected primary verdict; if the primary survives Holm correction, that's stronger; if it doesn't, that's a multiplicity-fragility flag. Holm cannot be computed on a cell that is INCONCLUSIVE; that cell is omitted from the Holm step-down ordering.

### 4.7 Walk-forward gate (n ≥ 30 per arm)

Each cell (primary + each sensitivity arm) must have ≥ 30 heavy-T days AND ≥ 30 non-heavy-T days satisfying §4.4 day-validity. Below 30 on either arm, the cell is **INCONCLUSIVE** per §5 verdict rule (does NOT halt the test; routes to INCONCLUSIVE per the [HA-C4 v2 §5.4 + §5.3](../HA-C4/hypothesis.md#54-inconclusive-bar-locked-verbatim-from-v1-v2-53-absorbs-the-formerly-halt-triggering-condition) INCONCLUSIVE-aware pattern, single-operand collapsed).

**Expected n per arm** (anchored on HA-C4 v2 §7.3 unmedicated counts + STOCKTAKE §6 cross-phase gain estimate): primary cross-phase-pooled stratum heavy-T n ≈ unmedicated 247 + medicated ~70 = ~317; non-heavy-T n ≈ unmedicated 419 + medicated ~150 = ~569. Sensitivity-arm n is the unmedicated-only subset: 247 heavy-T / 419 non-heavy-T per HA-C4 v2 §7.1. All cells comfortably clear the ≥30 bar at the primary cross-phase-pooled stratum; the unmedicated-only sensitivity arm clears as well. The motion-clean-only sensitivity arm may be degenerate (per HA11-bout-redo's 99.3% motion-confound finding at the bout level); if so, that arm routes to INCONCLUSIVE per §4.10.

### 4.8 Verdict bands (locked pre-commits per §5)

Inherits from [HA-C4 v2 §5.3 INCONCLUSIVE-aware pattern](../HA-C4/hypothesis.md#53-triad-verdict-rule-v2-rewritten-with-explicit-inconclusive-handling), collapsed to single-operand:

| outcome | condition |
|---|---|
| **SUPPORTED** | both bars met (block-perm p<0.05 + Cliff's delta ≥ +0.20) in predicted positive direction |
| **PARTIAL** | direction-correct AND exactly one bar clears, AND the failure is read against the §8 calibration discount |
| **REJECTED** | direction wrong-sign OR both bars fail OR §4.10 crash-drop sensitivity surfaces direction-flipping |
| **INCONCLUSIVE** | walk-forward gate (§4.7) not met OR §10.4 sanity gates fail |

See §5 for the full bar-by-bar definitions and verdict rule precedence.

### 4.9 Approach A inheritance — by-analogue descriptive companion with underpowered-NULL discipline (per Authorship "Locked decisions" item 7)

**Underpowered-NULL framing leads.** Per [`bout_level_dose_response_calibration.md §6` (r4 LOCKED `fb97d1c`)](../../../methodology/bout_level_dose_response_calibration.md) + [STOCKTAKE §6 architectural-implications paragraph](../../../STOCKTAKE.md#6-cross-section-synthesis), the bout-level β recalibration produced **0/7 CONFIRMED at the discriminative bar** at this corpus's bout-level n (~49 day-clusters/window in buildup-post-CPAP; ~75-78 in afbouw) — Approach A is **NOT load-bearing for any downstream HA pre-reg at this corpus's bout-level n**. The framing discipline preserved at five surfaces in the recalibration audit ([`reviews/bout_level_dose_response_calibration-r3-2026-06-22.md` §3](../../../reviews/bout_level_dose_response_calibration-r3-2026-06-22.md)) is the **underpowered-NULL framing**: at this corpus's per-window n, β coefficients cannot cross the sub-MD §3.4 four-condition discriminative bar; this is the honest claim *"we cannot demonstrate per-bout dose-modulation at this n"*, NOT a definitive claim about citalopram's bout-level pharmacology or about dose-naivety. **HA-C4c primary outcome is dose-naive within that framing.** Approach A is RELEGATED to sensitivity arm per the recalibration §6 architectural-implications paragraph; the section that follows derives a **descriptive companion** (NOT a load-bearing dose-correction) using the closest-analogue β as a coefficient-of-convenience.

**Inheritance-by-analogue as descriptive companion** (since `bout_n_did_not_return_day` was NOT in the recalibration's 7-feature scope, no per-feature β is available for this operand; the construction below is descriptive and inherits the underpowered-NULL framing):

- Closest-analogue feature with a sensitivity inheritance: `bout_n_fast_recovery_day` (also a per-day bout-count operand; verdict **weakly_consistent** per sub-MD §6; buildup-post-CPAP β = **−0.056/mg [95% CI −0.145, +0.034] p=0.223**). The CI **crosses zero**; the p-value is well above 0.05; sign-concordance with the −1 prior is the only reason the verdict is not NULL. Per the underpowered-NULL framing the recalibration audit preserved at five surfaces, this β is **NOT a CONFIRMED dose-modulation** for `bout_n_fast_recovery_day`; using it as an inheritance template for a different feature inherits BOTH the source β's CI uncertainty AND the analogue-substitution uncertainty.
- Within that frame, to compute the descriptive companion: use the analogue β as a coefficient-of-convenience, sign-flipped to match HA-C4c's +1 prior direction on `bout_n_did_not_return_day` (more failures-to-return under elevated sympathetic tone) versus `bout_n_fast_recovery_day`'s −1 prior direction in the recalibration. The fiat sign-flip imports a +1 directional prior on `bout_n_did_not_return_day` that the recalibration **never tested for this feature** (the feature was downstream of the recalibration's scope). This sign-flip is honest only as a descriptive-companion device; it is NOT a CONFIRMED-direction claim. **Approach A inheritance-by-analogue β for `bout_n_did_not_return_day`**: +0.056/mg (sign-flipped from `bout_n_fast_recovery_day`'s template; same magnitude).
- Approach A sensitivity arm (descriptive companion): `bout_n_did_not_return_day_adj(d) = bout_n_did_not_return_day(d) − β_template × dose_plasma_mg(d) = bout_n_did_not_return_day(d) − 0.056 × dose_plasma_mg(d)`.
- Re-run the §4.6 primary procedure on the dose-adjusted operand; report alongside the primary as a **SENSITIVITY-ARM-ONLY** inheritance, NOT a primary-arm bias-correction. Explicitly marked as **inheritance-by-analogue (descriptive companion under the underpowered-NULL frame, NOT inheritance-by-recalibration on the operand itself)** in the result.md per the [§8 caveat 3 framing](#8-caveats-resultmd-must-explicitly-acknowledge).

**Why this is a descriptive companion, not a load-bearing dose-correction** (anchors the framing inline; §8 caveat 3 restates this load-bearingly):

1. The source β is itself NULL/weakly-consistent per the recalibration's underpowered-NULL framing — no CONFIRMED dose-modulation exists for the analogue feature at this corpus's per-window n, let alone for `bout_n_did_not_return_day`.
2. The analogue substitution adds further uncertainty beyond the source β's CI: `bout_n_fast_recovery_day`'s per-day distribution shape, its dose-modulation mechanism (if any), and the +1 → −1 prior-direction asymmetry are all unmeasured for the inheritance step.
3. The underpowered-NULL framing at the recalibration cascades to HA-C4c: any apparent dose-adjustment on `bout_n_did_not_return_day` carries the recalibration's binding-constraint-is-n caveat, not a citalopram-pharmacology-on-this-operand claim.
4. Using a CI-crosses-zero β as a load-bearing dose-correction would inject the recalibration's noise into the primary verdict; keeping Approach A as a sensitivity arm honours the recalibration's NULL/weakly-consistent reading.

**Sensitivity-of-verdict-to-CI-bounds sub-arm** (per parent MD §8 caveat 3 + sub-MD §7 caveat 5 + [§8 caveat 3 below](#8-caveats-resultmd-must-explicitly-acknowledge)): the Approach A sensitivity arm is re-run at the analogue β's CI lower bound (β = −0.145/mg → +0.145/mg template after sign-flip; CI lower of `bout_n_fast_recovery_day`) AND the CI upper bound (β = +0.034/mg → −0.034/mg template after sign-flip; CI upper) to **characterise the inheritance fragility**. Per the underpowered-NULL frame, the analogue β's CI crosses zero, so this CI bracket is structurally a NULL-bracket: re-running primary on a NULL-bracket template is a descriptive companion to illustrate inheritance fragility, NOT a substantive precision check on a CONFIRMED β. If the verdict on the Approach A sensitivity arm flips across the CI range, surface as a **β-precision-fragility finding** with the explicit framing that the fragility is **a property of the inheritance-by-analogue construction**, NOT a substantive finding about dose-modulation on `bout_n_did_not_return_day` (which the recalibration does not warrant a claim about at this corpus's per-window n).

### 4.10 Sensitivity arms (descriptive; cannot promote to SUPPORTED)

Per parent MD §3.4 + parent MD §3.1.1 + CONVENTIONS §3.4 + Authorship "Locked decisions" item 5:

- **Unmedicated-only stratum** (per §4.2 secondary): re-run the §4.6 primary procedure restricted to `citalopram_phase == unmedicated` only (equivalently the `recovery_phase == pacing_habit_established` slice restricted to days before 2024-04-09; LC era 2022-04-04 → 2024-04-08, further restricted to days `>= 2022-11-17` per the §6 sub-phase 4b left-edge; excluding April 2024 cluster). Mirrors HA11-bout-redo's reference frame for cross-test consistency. Reported; cannot promote to SUPPORTED. If verdict differs from primary, surface as **stratum-fragility finding**.
- **Motion-clean-only arm** (per parent MD §3.4 + HA11-bout-redo §4.10): re-aggregate `bout_n_did_not_return_day` from `per_bout_master.csv` restricted to bouts with `motion_confound_flag == False`. **Anticipated degeneracy per HA11-bout-redo result §4**: 4285/4317 bouts (99.3%) carry `motion_confound_flag=True` on this corpus; the motion-clean-only re-aggregation may produce a per-day count series with near-zero variance that collapses below the §4.7 walk-forward gate → arm routes to INCONCLUSIVE. If so, the cell is reported as **motion-fragility flagged INCONCLUSIVE** per HA11-bout-redo §9.5 pattern; the framework-validity reading is that the bouts-as-currently-extracted ARE motion-tagged events and any "rest-stress" semantic claim is necessarily across the motion-tagged pool (per §8 caveat 4).
- **Transient-excluded arm** (per parent MD §3.1 r2 absorb; primary INCLUDES transients): restrict the count to bouts with `transient_flag == False`. **Anticipated fragility per HA11-bout-redo result §4**: HA11-bout-redo's transient-excluded discrimination dropped from +20.26pp to +11.69pp; HA-C4c is likely to see analogous attenuation on `bout_n_did_not_return_day` (transient bouts contribute to the per-day count). Report; if verdict swings under transient exclusion, surface as **transient-fragility finding** per §8 caveat 5.
- **Baseline-invalid-excluded arm** (per parent MD §4 NaN semantics): restrict to bouts where `baseline_invalid_flag == False`. Per HA11-bout-redo result, only 44/4317 bouts (1.0%) carry `baseline_invalid_flag=True`; expected to be a low-impact descriptive companion. If verdict changes, flag as baseline-validity fragility.
- **Crash-drop sensitivity arm** (CONVENTIONS §3.4 + Authorship "Locked decisions" item 5): re-run the §4.6 primary procedure with `is_crash == True` rows dropped from BOTH the heavy-T arm AND the non-heavy-T arm (paralleling HA-C4 v2 §4.11.1). Compare crash-dropped Cliff's delta vs primary Cliff's delta. If `|Δ Cliff's delta| > 0.10` (HA-C4 v2 pattern) OR `|Δ pp on discrimination| > 5` (HA11-bout-redo pattern, where applicable), flag as a §3.4 finding (*"the heavy-T signal is crash-driven, not robust across the broader heavy-T pool"*). The primary verdict per §5 is unchanged; crash-drop is informative-for-interpretation per CONVENTIONS §3.4 pattern. If `|Δ Cliff's delta| > 0.20` AND the direction flips, route the primary verdict to REJECTED per §5 (the entire heavy-T signal is crash-driven and not a generalisable Wiggers-C4-positive pattern).

**Sister-test cross-reference companion** (no statistical machinery, just descriptive table): report HA-C4 v2 daily-aggregate verdict (REJECTED triad sum 0/3; Channel 1 drop_avg SUPPORTED both eras) + HA-C4b v3 verdict (NOT-SUPPORTED on motion-filter crash-precursor) + HA11 v1 verdict (SUPPORTED-on-train U-dip count) + HA11-bout-redo verdict (PARTIAL framework-validity reproduction at bout level) alongside the HA-C4c primary verdict in the result.md sister-test-table. Per CONVENTIONS §4.4 reviewer-mode discipline: HA-C4c does NOT claim a cross-test pass conclusion at result-emission time; cross-test interpretation is a separate post-lock synthesis session.

### 4.11 Per-bout-n reporting discipline (locked per parent MD §6.3 + CONVENTIONS §3.6)

Per parent MD §6.3 r2 absorb (inherited downstream from HA11-bout-redo §4.11), HA-C4c's result.md MUST report:

- **Per-arm `n_bouts`**: total bouts in the heavy-T-day pool; total bouts in the non-heavy-T-day pool (cross-phase-pooled stratum); same for the unmedicated-only sensitivity arm.
- **Per-cell `n_did_not_return_bouts × n_days × n_did_not_return_bouts_per_day`**: per-arm decomposition of the per-day count.
- **Named-counts triplet per CONVENTIONS §3.6**: every count phrasing names scheme + unit + source-file (e.g. *"X did-not-return bouts per `bout_n_did_not_return_day` count over Y heavy-T days from `per_day_master.csv` cross-phase-pooled stratum"*).

Per-bout n is a derived quantity (depends on per-minute stress trace coverage + bout-extraction rule + the §3.2 return-window rule); under-reporting would obscure the effective power of HA-C4c's verdict.

## 5. Pre-registered falsification criterion

### 5.0 Multi-comparison discipline — single-cell headline lock (per Authorship "Mandatory dispatches" + §3.8 gate 2)

HA-C4c is a **single-cell headline lock**: the headline verdict is the SUPPORTED/PARTIAL/REJECTED/INCONCLUSIVE outcome on the single triple {cross-phase-pooled stratum × `bout_n_did_not_return_day` × heavy-T-vs-non-heavy-T} per §4.6. All sensitivity arms (unmedicated-only stratum, motion-clean-only, transient-excluded, baseline-invalid-excluded, crash-drop, Approach A dose-adjusted) are diagnostic / sensitivity ONLY. They are reported in result.md but **none can promote to SUPPORTED on their own**.

### 5.1 Per-cell confirmation bar (applied to the primary cell + each sensitivity arm)

For each cell that meets the §4.7 walk-forward gate (≥ 30 per arm):

**(a) Discrimination**: empirical one-sided p < 0.05 from the block-permutation null at E[L]=7 (per §4.6).

**(b) Effect size**: Cliff's delta ≥ +0.20 in the predicted direction (heavy-T > non-heavy-T).

**Cell SUPPORTED** if BOTH (a) and (b) hold in the predicted positive direction.

### 5.2 Verdict rule (single-operand SUPPORTED/PARTIAL/REJECTED with INCONCLUSIVE handling)

The headline verdict is computed on the primary cell only per the §5.0 single-cell headline lock. Verdict bands:

| outcome | condition (primary cell) |
|---|---|
| **SUPPORTED** | both (a) discrimination + (b) effect-size bars met in the predicted positive direction per §5.1 |
| **PARTIAL** | direction-correct AND exactly one of (a) or (b) clears, AND the failed bar is interpreted against the HA11-bout-redo calibration discount per §8 caveat 2 |
| **REJECTED** | direction wrong-sign OR both (a) and (b) fail OR §4.10 crash-drop sensitivity surfaces `|Δ Cliff's delta| > 0.20` AND a sign-flip |
| **INCONCLUSIVE** | §4.7 walk-forward gate not met OR §10.4 dry-run sanity gates fail |

**Verdict rule precedence**: INCONCLUSIVE checked first (a degenerate n-shortfall cell cannot have a meaningful (a) or (b) read; routes to INCONCLUSIVE without evaluating bars). Then REJECTED (direction-wrong OR crash-drop sign-flip — the failure-mode reads). Then SUPPORTED. Then PARTIAL (fallback for direction-correct-but-partial cells).

**Honest framing per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)**: this verdict rule was added in this draft as a single-operand collapse of HA-C4 v2's INCONCLUSIVE-aware triad pattern. The PARTIAL band is the explicit handling for cells where the discrimination magnitude reproduces the predicted direction but the block-permutation p-value cannot clear 0.05 at the analysis-pool size — the same failure-mode shape HA11-bout-redo's PARTIAL verdict surfaced at the framework-validity level. HA-C4c is structurally vulnerable to the same failure-mode at substantive level if its n is similar to HA11-bout-redo's (it isn't — cross-phase-pooled n is materially larger — but the §8 caveat 2 calibration discount makes the cross-test risk visible). The verdict rule is structural; applies regardless of which way the (a) / (b) bars actually fall on this corpus.

### 5.3 Holm step-down across sensitivity arms (multiplicity correction; secondary fragility-flag report)

Per Authorship "Locked decisions" item 6 + §4.6: Holm step-down across the {primary, unmedicated-only sensitivity, motion-clean-only sensitivity, transient-excluded sensitivity} family at α=0.05 (4 comparisons). The Holm result is REPORTED alongside the uncorrected primary; if the primary survives Holm correction, that's stronger; if it doesn't, that's a multiplicity-fragility flag. The §5.2 hard rule binds the primary verdict from the uncorrected (a)/(b) bars; Holm is secondary report.

**Holm fewer-comparisons disclosure**: if motion-clean-only sensitivity arm returns INCONCLUSIVE (anticipated per §8 caveat 4 due to the 99.3% motion-confound corpus-property finding), the Holm step-down family across `{primary, sens A (block bootstrap), sens E (crash-drop)}` collapses from 4 cells to 3 (cutoffs α/3, α/2, α/1 instead of α/4, α/3, α/2, α/1) — the result.md Holm column MUST be annotated explicitly when this occurs (form: *"Holm (3-of-4 sens arms; motion-clean INCONCLUSIVE)"*). Reporting-discipline only; the §5 hard verdict criteria still bind Holm as secondary report. Inherits the disclosure pattern from [HA-C4 v2 §5.5 r2 fewer-comparisons absorb](../HA-C4/hypothesis.md#55-holm-step-down-across-channels-locked-within-test-multiplicity-correction-verbatim-from-v1).

### 5.4 INCONCLUSIVE bar (per §4.7)

A cell is **INCONCLUSIVE** if either the heavy-T arm OR the non-heavy-T arm has < 30 days satisfying §4.4 day-validity. INCONCLUSIVE cells DO NOT REFUTE; they yield no (a)/(b) read and are reported as such. If the primary cell is INCONCLUSIVE, the headline verdict is INCONCLUSIVE per §5.2 — HA-C4c-v2 may be drafted with a different stratum (e.g. per-phase stratified or a different cross-phase pooling) per §9.

## 6. Exclusion rules (locked)

- **LC era only**: days before `2022-04-04` excluded.
- **Primary stratum**: cross-phase pooled on the `citalopram_phase` axis (`citalopram_phase(d) ∈ {unmedicated, buildup, consolidation, afbouw, post_afbouw}` per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification)), restricted on the `recovery_phase` axis to sub-phase 4b (`pacing_habit_established`; 2022-11-17 → 2024-04-08) UNION phase 5 (`citalopram_modulated`; 2024-04-09 onward, excluding April 2024 cluster) per [`lc_recovery_phase_axis §3.4b + §3.5`](../../../methodology/lc_recovery_phase_axis.md). Days in earlier recovery phases (phase 1 `pre_illness_healthy` / phase 2 `acute_infection` / phase 3 `lc_pre_ergo` / sub-phase 4a `pacing_pre_citalopram_learning`) excluded per the canonical 1/2/3/4a/4b/5 numbering in `lc_recovery_phase_axis §2`. The phase 4a/4b sub-boundary at 2022-11-17 is the left edge of HA-C4c's primary stratum (the 8-week-post-ergotherapie M1 lived-experience boundary per `lc_recovery_phase_axis §3.4b`).
- **April 2024 cluster (2024-04-09 → 2024-04-16)**: structurally unanalysable per [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md); excluded from all arms.
- **21-day device-baseline-lag**: days in the first 21 days of `has_garmin_uds=True` coverage excluded per parent MD §3.4.
- **Missing exertion classification**: days with `exertion_class_lagged_lcera` NaN excluded.
- **Day-validity NaN on `bout_n_did_not_return_day`**: days failing the pipeline §3.4 day-validity gate (≥ 600 valid per-minute stress samples; not in first 21 device-baseline days; not in April 2024 cluster) excluded. The pipeline emits `0` on valid days with no `did_not_return` bouts (NOT NaN); `0` is a valid value entering the count.
- **Unmedicated-stratum restriction NOT REQUIRED for HA-C4c primary** per parent MD §6 — that restriction is the framework-validity gate's scope (HA11-bout-redo), not the substantive Wiggers C4 retest scope. HA-C4c's primary uses the cross-phase-pooled stratum per §4.2; the unmedicated-only restriction is the primary sensitivity arm per §4.10.

## 7. Expected effect size if true

**Anchored on**: (i) HA-C4 v2 §7.1 unmedicated descriptives (the daily-aggregate analogue; informs the range of within-day "stuck stress" prevalence on this corpus); (ii) the per-bout `did_not_return_flag` rate from the LANDED pipeline run 2026-06-22 (22.8% did_not_return per [STOCKTAKE §6 bout-level pipeline paragraph](../../../STOCKTAKE.md#6-cross-section-synthesis)); (iii) the HA-C4 v2 §7.2 heavy-T vs non-heavy-T descriptive deltas pattern (heavy-T median higher on all C4-related channels at the daily-aggregate level).

**Pre-committed sanity-check ranges**:

- **Per-day `bout_n_did_not_return_day` mean across the primary cross-phase-pooled stratum**: expected in **[0.3, 1.5]** events/day. Anchor: 22.8% did_not_return rate × ~3-5 bouts/day average (per parent MD §5 cross-bout sparsity estimate) ≈ 0.68-1.14 events/day. If the actual mean is outside [0.3, 1.5] (a factor-of-2 deviation), HALT the test per §10.4 sanity-check rule.

- **Per-day `bout_n_did_not_return_day` median**: expected in **[0, 2]** events. If the actual median exceeds 4, HALT (the operand is firing too often to be Wiggers-C4-positive-meaningful; suggests the 180-min return-window cap is too tight on this corpus or the +5 baseline tolerance is too strict — operand-calibration concern).

- **Heavy-T arm mean — non-heavy-T arm mean** (descriptive directional anchor): expected **> 0** under SUPPORTED. Anchor against HA-C4 v2 §7.2 Channel 1 NaN-fraction-tied pattern at daily aggregate (heavy-T NaN 18.6% vs non-heavy-T NaN 18.1% — *essentially tied*) which informed HA-C4 v2's eventual REJECTED daily-aggregate verdict. The bout-level operand may show a different magnitude pattern (the within-day decomposition surfaces "stuck stress" events that the daily-aggregate NaN-fraction read missed); the descriptive direction is the dry-run sanity check.

- **Cliff's delta under SUPPORTED**: expected in **[+0.20, +0.40]**. Anchor: HA11-bout-redo's framework-validity Cliff's delta was +0.306 [paired-bootstrap 95% CI −0.021, +0.626]; HA-C4c's substantive shift should be of comparable order at bout-level resolution. **At-risk for the +0.20 bar** if the daily-aggregate NaN-fraction-tied pattern from HA-C4 v2 §7.2 propagates to bout level (it shouldn't — that's the whole point of the bout-level pivot per HA-C4 v2 §9 REJECTED branch — but the §7.2 descriptive baseline is the conservative anchor).

- **Block-permutation p-value under SUPPORTED**: expected **< 0.05** at cross-phase-pooled stratum (n ~ 317 heavy-T / 569 non-heavy-T; much larger than HA11-bout-redo's n_crash=11). The HA11-bout-redo PARTIAL outcome at bar 3 was a power-shortfall artefact at n_crash=11; cross-phase-pooled HA-C4c primary should have ample power for bar 3 if the effect size is in the expected range. Per §8 caveat 2 calibration discount, this expectation is interpretively important: the HA-C4c verdict is the substantive read of whether the operand's signal clears the bar at a larger n than HA11-bout-redo's framework-validity cell could provide.

- **Per-day baseline σ on `bout_n_did_not_return_day`** (cross-phase-pooled stratum): expected in **[0.5, 2.0]** per HA11-bout-redo §4.6 r2 anchor pattern (median σ on `bout_n_fast_recovery_day` was 0.739). If median baseline σ is < 0.5, low-variability flag may fire on most days; if > 2.0, one-day fluctuation drowns the signal.

If any sanity-check fails on the dry-run, HALT and revise the spec per §10.4 (creating HA-C4c-v2). The dry-run is the gate per [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock).

## 8. Caveats `result.md` must explicitly acknowledge

**LOAD-BEARING per the cascade context** — these caveats propagate from the four cascade-context findings the drafter is responsible for surfacing per the handoff §1:

1. **Power-calc dispatch**: power calc inapplicable per [Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) within-subject design. The block-permutation null at E[L]=7 (§4.6) is the within-subject inferential machinery; the §5 verdict bars determine the substantive verdict rather than asymptotic-power thresholds. INCONCLUSIVE cells per §4.7 walk-forward gate are the operational definition of "underpowered for this cell". (Per [`hypothesis_lock_process.md` §3.2 step 4 + §3.8 gate 1](../../../methodology/hypothesis_lock_process.md) mandatory dispatch.)

2. **Framework-validity calibration caveat from HA11-bout-redo PARTIAL** (per [HA11-bout-redo §9.2](../HA11-bout-redo/hypothesis.md#92-partial-exactly-2-of-3-5-bars-met--framework-validity-gate-partial) + [HA11-bout-redo result.md §6 cascade implication](../HA11-bout-redo/result.md#6-verdict-and-cascade-implication)): HA11-bout-redo's framework-validity gate cleared bars 1+2 (directional sign + effect-size comparability) at +20.26 pp / median signed z 2.410 — magnitude-validates the operand — but **bar 3 (block-permutation p < 0.05) FAILED at p=0.2609** at the n_calm=70/n_crash=11 stratum. The propagation to HA-C4c: the bout-level operand is *partially fit for purpose*; HA-C4c verdict-magnitudes are interpreted with a calibration discount. **Specifically**: if HA-C4c primary clears bars (a) discrimination + (b) effect-size at the cross-phase-pooled stratum (which has materially larger n than the framework-validity cell), the SUPPORTED verdict is interpretively stronger than the same magnitudes at HA11-bout-redo's framework-validity cell would have been. If HA-C4c primary falls into PARTIAL with bar (a) failing (i.e. magnitude correct but block-perm p ≥ 0.05), the failure-mode shape REPLICATES HA11-bout-redo's PARTIAL pattern — and the substantive Wiggers C4 question becomes power-bound at this corpus's bout-level n across BOTH the framework-validity gate AND the substantive gate, suggesting the n-per-arm dimension is the binding constraint on bout-level inference for THIS class of within-day-recovery question. **The HA-C4c verdict must be read with this calibration context visible**; the result.md MUST report the HA11-bout-redo framework-validity gate's per-bar status alongside the HA-C4c per-bar status.

3. **β-recalibration dose-naive primary framing** (per [sub-MD §6 architectural-implications paragraph](../../../methodology/bout_level_dose_response_calibration.md) + [STOCKTAKE §6](../../../STOCKTAKE.md#6-cross-section-synthesis)): **0/7 features CONFIRMED at this corpus's bout-level n**; Approach A is NOT load-bearing → HA-C4c primary is dose-naive (cross-phase pooling permitted without §5.A/B/C inheritance violation per parent MD §5.3 + the recalibration §6 architectural-implications paragraph). The Approach A sensitivity arm (§4.9) uses **inheritance-by-analogue** from `bout_n_fast_recovery_day`'s buildup-post-CPAP β (weakly_consistent verdict; CI crosses zero) — this is a pre-spec sensitivity rather than a load-bearing dose-correction. If the Approach A sensitivity arm produces a materially different verdict than primary, the divergence is informative about per-bout dose-modulation precision on `bout_n_did_not_return_day` (not a fragility of the primary). The result.md MUST name the Approach A inheritance as inheritance-by-analogue explicitly.

4. **99.3% motion-confound corpus property** (per [HA11-bout-redo result §4 motion-clean-only arm degeneracy](../HA11-bout-redo/result.md#4-sensitivity-arms-descriptive-cannot-promote-to-passed-per-single-cell-headline-lock)): **4285/4317 bouts (99.3%) carry `motion_confound_flag=True`** on this corpus + extraction threshold. This is a corpus-property finding, NOT a sub-arm issue — the entire HA-C4c operand inherits this; the substantive Wiggers verbatim *"during rest periods"* language is operationalised against the motion-tagged bout pool. Wiggers' "stress doesn't decrease despite resting" framing has been tested at the motion-filter operationalisation (HA-C4b v3 NOT-SUPPORTED) and at the bout-level operand here (HA-C4c primary keeps motion-confounded bouts per parent MD §3.4 default + HA11-bout-redo framework-validity reference-frame consistency). The HA-C4c primary verdict is interpreted as *"on this participant's per-minute stress trace, where bouts are overwhelmingly motion-coincident events, does the within-day failure-to-return pattern differ between heavy-T and non-heavy-T days?"*. The motion-clean-only sensitivity arm at §4.10 is anticipated to be INCONCLUSIVE per the 99.3% finding; if so, this is reported as a corpus-property reaffirmation, NOT a verdict-modifying flag. The result.md MUST name the 99.3% finding as a corpus-property caveat that the entire operand inherits.

5. **Transient-fragility** (per [HA11-bout-redo result §4 transient-excluded arm](../HA11-bout-redo/result.md#4-sensitivity-arms-descriptive-cannot-promote-to-passed-per-single-cell-headline-lock)): HA11-bout-redo's transient-excluded discrimination dropped from +20.26 pp to +11.69 pp; a non-trivial fraction of the bout-level signal lives in transient bouts. HA-C4c primary INCLUDES transients per parent MD §3.1 r2 absorb; transient-excluded variant is the §4.10 sensitivity arm. If the HA-C4c primary verdict swings under transient exclusion (e.g. SUPPORTED → PARTIAL or PARTIAL → REJECTED), surface as a transient-fragility finding in the result.md per CONVENTIONS §3.3 column-duplication discipline (the two cells read together as one diagnostic, not as independent verdicts).

6. **n=1 single-subject + observational + multi-source** per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) + [`wiggers_test_design_on_chained_regime.md` Cross-cutting statistical hygiene §1-§4](../../../methodology/wiggers_test_design_on_chained_regime.md#cross-cutting-statistical-hygiene). Personal-baseline thresholds (the §4.4 day-validity gate inherits HA11 v1's 600-sample-per-day rule; operand calibrated to the participant's distribution; cross-subject generalisation out of scope).

7. **Operational vs mechanistic per [CONVENTIONS §4.1](../../../CONVENTIONS.md#41-no-interpretive-marks-on-raw-or-descriptive-layers)**: per-bout features are operational descriptions of the per-minute Garmin stress trace, NOT mechanistic measurements of autonomic state. A SUPPORTED verdict on HA-C4c is a statement about per-minute-trace-operand patterns on heavy-T vs non-heavy-T days, NOT about autonomic-recovery physiology directly. Per parent MD §2.4 + §8 caveat 5 + sub-MD §7 caveat 4, the upstream Firstbeat algorithm is opaque (closed-source); per-bout features at minute resolution SURFACE algorithmic artefacts that daily-aggregate hid. The HA-C4c verdict inherits this caveat.

**Additional substantive caveats**:

8. **Cross-phase pooling permissibility is conditional on the recalibration's 0/7 CONFIRMED reading** (per recalibration §6 architectural-implications). If a future expanded corpus or revised bout-detection rule materially changes the per-window n and produces CONFIRMED features in the recalibration, the cross-phase pooling permission may need to be revisited; HA-C4c would then need a v2 with per-phase stratification OR Approach A as primary. The current draft pre-commits cross-phase pooling at the current recalibration state; if the recalibration re-runs and the inheritance table changes, the pre-reg becomes out-of-spec per [`hypothesis_lock_process.md` §3.7](../../../methodology/hypothesis_lock_process.md) (post-lock changes create v2).

9. **HA-C4 v2 daily-aggregate REJECTED is the prior state of evidence** at coarser resolution; HA-C4c does NOT supersede HA-C4 v2's verdict at daily-aggregate level — that REJECTED verdict stands as the historical record for daily-aggregate operationalisation. HA-C4c at bout resolution is an additional verdict on a finer-resolution operand; the two verdicts coexist per parent MD §1.3 (the C4 register row will carry pointers to BOTH at HA-C4c lock; HA-C4c does NOT remove the HA-C4 v2 pointer).

10. **Pacing-behaviour confounder** (inherited from HA-C4 v2 §8 + parent MD §2.4 r2 absorb): if the within-day stress pattern this participant generates is mediated by active pacing behaviour (the participant uses Garmin stress as a live pacing signal per [`garmin_pacing_practice.md`](../../../methodology/garmin_pacing_practice.md)), bout-level analysis may not "fix" the daily-aggregate flatness — it may reveal that the pacing behaviour shapes per-bout features too. The cross-phase-pooled stratum partially insulates against this (sub-phase 4b `pacing_habit_established` UNION phase 5 `citalopram_modulated` on the `recovery_phase` axis span the post-2022-11-17 pacing-stable LC era; pre-pacing-stable era days are excluded per §6 stratum). The HA-C4c verdict cannot fully eliminate this risk; a SUPPORTED-here-NOT-SUPPORTED-at-HA-C4b shape is consistent with the protective-rather-than-predictive alternative reading from HA-C4b v3 §9.

## 9. What we do with each outcome

### 9.1 SUPPORTED — strong evidence for Wiggers C4 at bout resolution

The bout-level operand `bout_n_did_not_return_day` shows systematically higher counts on heavy-T days than on non-heavy-T days at the cross-phase-pooled stratum, with both (a) discrimination + (b) effect-size bars clearing in the predicted direction. The Wiggers C4 claim *"stress doesn't decrease for a long time after overexertion"* is empirically reproduced at within-day-event resolution; the HA-C4 v2 REJECTED-at-daily-aggregate verdict is contextualised as a resolution-mismatch finding (the within-day signal IS detectable at bout level even though it collapsed at daily aggregate).

**Downstream actions on SUPPORTED**:

- The C4 register row at [`wiggers_testable_hypotheses.md`](../../../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic) updates at HA-C4c lock to add the substantive-at-bout-level SUPPORTED pointer (HA-C4 v2 REJECTED-at-daily-aggregate pointer stays; pointers coexist per §8 caveat 9).
- **Cross-test pass relevance**: HA-C4c SUPPORTED + HA-C4b v3 NOT-SUPPORTED + HA11 SUPPORTED-on-train + HA11-bout-redo PARTIAL = the within-day-recovery-shape autonomic story is multi-channel-confirmed at bout resolution (the U-dip at HA11 + the failure-to-return at HA-C4c are inverse-direction confirmations of the same per-bout recovery-dynamics construct); HA-C4b's NOT-SUPPORTED reads as the protective-rather-than-predictive alternative per HA-C4b v3 §9. The cross-test interpretation is a separate post-lock synthesis session per CONVENTIONS §4.4.
- The methodology MD parent + sub-MD + bout-extraction pipeline all remain LOCKED.
- The Approach A sensitivity arm result informs whether dose-aware reading is needed for downstream sister tests; if Approach A diverges materially from primary, the recalibration may be queued for a re-run with refined spec per recalibration §8.

### 9.2 PARTIAL — narrower claim about which conditions hold

The HA-C4c primary verdict is direction-correct AND exactly one of (a) discrimination or (b) effect-size clears, with the failure interpreted against the §8 caveat 2 calibration discount.

**Two PARTIAL configurations + their interpretation**:

- **Direction-correct + (b) Cliff's delta ≥ +0.20 + (a) block-perm p ≥ 0.05**: the substantive magnitude reproduces the predicted shape but the block-permutation null cannot statistically distinguish it. The failure-mode REPLICATES HA11-bout-redo's bar-3 PARTIAL pattern — and at HA-C4c's larger cross-phase-pooled n. Reading: the bout-level operand's signal exists in the predicted direction with a non-trivial effect size, BUT the n-per-arm at the cross-phase-pooled stratum + the block-permutation null at E[L]=7 cannot statistically clear 0.05. This is a power-bound substantive finding — the operand is fit-for-purpose at the magnitude/direction level but not statistically distinguishable from the null at this corpus's bout-level n. The Wiggers C4 claim at bout resolution is *"the pattern exists in the predicted direction at this corpus, with a Cliff's delta in [+0.20, +0.40] range, but cannot be statistically distinguished from the block-permutation null at the present analysis-pool size"*.

- **Direction-correct + (a) block-perm p < 0.05 + (b) Cliff's delta < +0.20**: the discriminative signal is statistically distinguishable from the null BUT the effect size is below the "small-to-medium" threshold. Reading: the signal exists and is statistically real but is small in magnitude — the substantive Wiggers C4 reading is a weak-effect-but-real positive pattern. The fragility flag is whether the small-effect signal survives the §4.10 sensitivity arms (transient-excluded in particular is anticipated to attenuate further; if PARTIAL primary plus FAILED transient-excluded, the small effect lives in transient bouts).

**Downstream actions on PARTIAL**:

- The C4 register row updates at HA-C4c lock to add a PARTIAL pointer with the configuration explicitly named.
- The cross-test pass folds in the PARTIAL configuration: PARTIAL-with-(a)-failing is interpretively distinct from PARTIAL-with-(b)-failing.
- **Optionally**: a HA-C4c-v2 may be drafted with a refined operand (e.g. `bout_recovery_half_life_median_day` as primary; OR a 3-channel triad incorporating `bout_n_did_not_return_day` + `bout_recovery_half_life_median_day` + a third channel) — NOT required; PARTIAL does not halt the cascade.
- The parent MD + sub-MD + pipeline all remain LOCKED.

### 9.3 REJECTED — Wiggers C4 framework not detectable on this corpus even at bout resolution

The HA-C4c primary verdict is direction-wrong OR both bars fail OR the §4.10 crash-drop sensitivity arm surfaces a direction-flip indicating the entire heavy-T signal is crash-driven. The substantive Wiggers C4 claim does NOT operationalise cleanly on this corpus at either daily aggregate (HA-C4 v2 REJECTED) OR bout level (HA-C4c REJECTED).

**Downstream actions on REJECTED**:

- The C4 register row updates at HA-C4c lock to add the REJECTED-at-bout-level pointer (alongside the HA-C4 v2 REJECTED-at-daily-aggregate pointer); the C4 lineage closes on the substantive question at this corpus's resolution.
- **Cross-test pass relevance**: REJECTED + HA-C4b v3 NOT-SUPPORTED + HA11 SUPPORTED-on-train + HA11-bout-redo PARTIAL = the Wiggers C4 framework doesn't operationalise cleanly on this corpus at either the precursor (HA-C4b) or the descriptive (HA-C4 v2 + HA-C4c) level; the within-day U-dip (HA11) sister channel does survive though. The C4 framework may need a fundamentally different operationalisation (e.g. HR-channel bout-level analysis per parent MD §1.4 A4 enabled-on-request candidate) — out of scope for HA-C4c.
- Parent MD + sub-MD + pipeline remain LOCKED (the REJECTED verdict is a substantive finding about the per-day operand, not a methodology failure — the framework-validity gate cleared bars 1+2 at HA11-bout-redo).
- The pacing-behaviour confounder per §8 caveat 10 is the most likely structural explanation: if the participant's active pacing behaviour systematically prevents within-day "stuck stress" events even on heavy-T days, the operand will flatten across heavy-T-vs-non-heavy-T contrast on this corpus.

### 9.4 INCONCLUSIVE — n shortfall or sanity-gate failure

Either the §4.7 walk-forward gate (≥ 30 per arm) is not met on the primary cell OR the §10.4 dry-run sanity gates (per §7 expected-range checks) fail.

**Downstream actions on INCONCLUSIVE**:

- HA-C4c-v2 reframe with different stratum or different operand candidate. Options: (a) per-recovery-phase stratified verdict (separate verdicts in sub-phase 4b `pacing_habit_established` + phase 5 `citalopram_modulated`; meta-combine) OR per-citalopram-phase stratified verdict (separate verdicts in unmedicated + buildup + consolidation + afbouw; meta-combine); (b) `bout_recovery_half_life_median_day` as primary operand instead; (c) restrict the heavy-T classification to `very_heavy` only (more conservative; smaller n); (d) extend the stratum to include sub-phase 4a `pacing_pre_citalopram_learning` + phase 3 `lc_pre_ergo` on the recovery axis (full pre-pacing-stable LC era).
- HA-C4c v1 is archived per [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock); HA-C4c-v2 drafting in a fresh session.
- The cross-test pass does NOT fold in an INCONCLUSIVE verdict beyond the methodological-failure-mode reading (the operand or stratum or analytical machinery cannot clear the dry-run sanity gates at this corpus's bout-level n).

### 9.5 Sensitivity-arm divergence (per §4.10)

- **Unmedicated-only sensitivity arm verdict differs from primary**: surface as **stratum-fragility finding**. The primary cross-phase-pooled verdict is the headline; the unmedicated-only sensitivity reads against HA11-bout-redo's reference frame. If the verdicts agree, the cross-phase pooling permission per recalibration §6 is empirically reaffirmed at the HA-C4c level; if they disagree, the pooling-vs-stratification choice is doing analytical work and the result.md must report the divergence.
- **Motion-clean-only arm verdict differs from primary (or is INCONCLUSIVE per the 99.3% finding)**: surface as **motion-fragility finding** OR a motion-clean-INCONCLUSIVE corpus-property reaffirmation per §8 caveat 4. The primary verdict per §5 is unchanged.
- **Transient-excluded arm verdict differs from primary**: surface as **transient-fragility finding** per §8 caveat 5. The primary verdict per §5 is unchanged.
- **Baseline-invalid-excluded arm verdict differs from primary**: surface as baseline-validity fragility (anticipated low-impact per HA11-bout-redo's 1% baseline-invalid bout count).
- **Crash-drop sensitivity surfaces `|Δ Cliff's delta| > 0.10` OR `|Δ pp on discrimination| > 5`**: surface as a CONVENTIONS §3.4 finding (*"the heavy-T signal is crash-driven, not robust across the broader heavy-T pool"*). The primary verdict per §5 is unchanged UNLESS `|Δ Cliff's delta| > 0.20` AND the direction flips, in which case the primary verdict routes to REJECTED per §5.
- **Approach A dose-adjusted sensitivity arm verdict differs from primary**: surface as a β-precision-fragility finding; the result.md MUST name the divergence as informative about per-bout dose-modulation precision on `bout_n_did_not_return_day` (per §8 caveat 3 inheritance-by-analogue framing). The primary verdict per §5 is unchanged.

### 9.6 Spec sanity-check fails on dry-run (per §7 + §10.4)

If the per-day `bout_n_did_not_return_day` mean is outside [0.3, 1.5] OR median outside [0, 4] OR baseline σ outside [0.5, 2.0], DO NOT run the full test. Document in dry-run report; revise the spec creating HA-C4c-v2 with this pre-reg archived as v1. The walk-forward gate (§4.7) failure routes to INCONCLUSIVE per §9.4 (not a halt; the cell is reported as INCONCLUSIVE).

## 10. Detection script architecture

### 10.1 Stage 1 — data (already done)

All inputs are in place post-pipeline-run `d5b394c`:

- `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` carries `bout_n_did_not_return_day` joined from `per_bout_aggregations_daily.csv` per the bout-extraction pipeline README.
- `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.csv` carries the per-bout dataset (4,317 bouts) for §4.10 sensitivity arm re-aggregation.
- `crash_v2-definition/labels_crash_v2.csv` carries `crash_v1` crash labels per HA11 v1 §3 (used by §4.10 crash-drop sensitivity arm).
- `dose_plasma_mg(d)` + `citalopram_phase(d)` derivable from date per [`citalopram_phase_stratification.md §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification).
- `exertion_class_lagged_lcera` already in `per_day_master.csv` per [DATA_DICTIONARY.md](../../../DATA_DICTIONARY.md).

**Pre-flight pipeline-trust check**: re-confirm `extract_stress_bouts.py --smoke-tests` PASS at commit `d5b394c` before running the test.

### 10.2 Stage 2 — test (`HA-C4c/test.py`, written post-lock in a separate session)

**Two-stage design**:

**Stage 2a (data preparation)**:
- Load `per_day_master.csv`; filter to primary stratum (cross-phase pooled on `citalopram_phase` axis = `citalopram_phase(d) ∈ {unmedicated, buildup, consolidation, afbouw, post_afbouw}`; equivalently sub-phase 4b + phase 5 on `recovery_phase` axis per §4.2) × §4.4 day-validity × §4.3 heavy-T classification non-NaN.
- Identify heavy-T arm (heavy + very_heavy) and non-heavy-T arm (none + light + moderate); compute n per arm.
- Compute per-day `bout_n_did_not_return_day` values; verify non-NaN per §4.4 gate.

**Stage 2b (primary test)**:
- Mann-Whitney U + Cliff's delta + block-permutation p at E[L]=7, B=10,000 draws, seed `20260623` per §4.6.
- Compute data-driven E[L]\* on `bout_n_did_not_return_day[d]` over primary stratum; flag factor-of-2 per CONVENTIONS §3.6.
- Evaluate §5 verdict rule: SUPPORTED / PARTIAL / REJECTED / INCONCLUSIVE.

**Stage 2c (sensitivity arms per §4.10)**: re-run Stage 2b on:
- Unmedicated-only stratum (`citalopram_phase == unmedicated`; equivalently `recovery_phase == pacing_habit_established` slice restricted to days before 2024-04-09).
- Motion-clean-only arm (re-aggregate from `per_bout_master.csv` restricted to `motion_confound_flag == False`).
- Transient-excluded arm (re-aggregate from `per_bout_master.csv` restricted to `transient_flag == False`).
- Baseline-invalid-excluded arm (re-aggregate restricted to `baseline_invalid_flag == False`).
- Crash-drop arm (drop `is_crash == True` rows from both arms; re-run primary).
- Approach A dose-adjusted arm (compute `bout_n_did_not_return_day_adj` per §4.9; re-run primary; also at CI lower/upper bounds per §4.9 sensitivity-of-verdict-to-CI-bounds).

**Stage 2d (Holm step-down)**: compute Holm step-down across the {primary, unmedicated-only sensitivity, motion-clean-only sensitivity, transient-excluded sensitivity} family at α=0.05 per §4.6 + §5.3; report alongside the uncorrected primary verdict.

**Companion descriptives**:
- Per-arm `n_bouts` + per-cell `n_did_not_return_bouts × n_days × n_did_not_return_bouts_per_day` per §4.11.
- Per-day `bout_n_did_not_return_day` distribution summary (mean, median, IQR, full range) per §7 sanity-check.
- Per-arm `did_not_return_flag` fraction at the bout level (not just per-day count).
- Per-arm bout-count distribution (mean per-day, max per-day, count of zero-`did_not_return` days).
- HA11-bout-redo framework-validity cross-reference: report HA11-bout-redo's primary cell verdict (PARTIAL with bars 1+2 PASS / bar 3 FAIL) alongside HA-C4c's primary verdict; allow the reader to triangulate the calibration discount per §8 caveat 2.

**Dry-run mode** (`--dry-run`): prints sample sizes per arm; per-day `bout_n_did_not_return_day` mean + median + IQR per §7; first-3-heavy-T-days summary for sanity-check. **HALT** on §7 sanity-check failure OR §4.7 walk-forward gate failure on primary cell per §10.4.

### 10.3 Stage 3 — `result.md` template

Reports in order:

1. **Headline verdict block** at top: HA-C4c verdict (SUPPORTED / PARTIAL / REJECTED / INCONCLUSIVE) + §5 (a) discrimination + (b) effect-size bar-by-bar breakdown + cross-test cascade implication (with explicit cross-reference to HA11-bout-redo PARTIAL framework-validity calibration discount per §8 caveat 2).
2. **Per-bar table**: each bar's observed value + threshold + pass/fail.
3. **Per-arm summary table**: heavy-T arm + non-heavy-T arm + Mann-Whitney U + Cliff's delta + Cliff's delta 95% CI + block-permutation p + n_days per arm + n_bouts per arm per §4.11 + n_did_not_return_bouts per arm per §4.11.
4. **Companion descriptives**: per-day distribution, sanity-check pass/fail, E[L]\* companion + factor-of-2 flag, per-arm `did_not_return_flag` fraction.
5. **Sensitivity arms section** per §4.10: unmedicated-only verdict, motion-clean-only verdict (anticipated INCONCLUSIVE per 99.3% finding), transient-excluded verdict, baseline-invalid-excluded verdict, crash-drop verdict + |Δ Cliff's delta|, Approach A dose-adjusted verdict + sensitivity-of-verdict-to-CI-bounds.
6. **Holm step-down**: family of 4 cells per §5.3; corrected p-values + per-cell pass/fail; multiplicity-fragility flag if primary doesn't survive Holm.
7. **Sister-test cross-reference table** per §4.10 last bullet: HA-C4 v2 daily-aggregate verdict + HA-C4b v3 verdict + HA11 v1 verdict + HA11-bout-redo verdict alongside HA-C4c primary verdict (descriptive only; no cross-test pass conclusion per CONVENTIONS §4.4).
8. **Pipeline-trust block**: re-confirm `extract_stress_bouts.py` commit + smoke-test PASS at run-time.
9. **Verification log**: parent MD commit at test-time + sub-MD commit at test-time + HA11-bout-redo result.md commit at test-time + HA-C4 v2 result.md commit at test-time + pipeline commit at test-time.
10. **Caveats per §8** (all 10 prominently surfaced; the calibration-discount caveat at top alongside the headline verdict per the cascade-context discipline).
11. **Downstream actions per §9** (SUPPORTED / PARTIAL / REJECTED / INCONCLUSIVE branch as actually fired).

### 10.4 Run protocol

1. **Dry-run** (`python test.py --dry-run`): prints sample sizes, per-day distribution summary, first-3-heavy-T-days summary. **HALT triggers**:
   - **§4.7 walk-forward gate**: n_heavy < 30 OR n_non_heavy < 30 on primary cell → INCONCLUSIVE; document + return without full-run (route to §9.4 reframe).
   - **§7 sanity-check gates** (any of):
     - mean `bout_n_did_not_return_day` outside [0.3, 1.5]
     - median outside [0, 4]
     - baseline σ outside [0.5, 2.0]
     → HALT + revise spec creating HA-C4c-v2.
2. **Full run** (`python test.py`): emits `result.md` + `result-data.json` directly into this folder.
3. **No iteration on the spec after dry-run passes.** Post-dry-run revisions create v2 with v1 archived per the project's locked-pre-reg discipline per [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock).

### 10.5 Reproducibility

- **Environment variable**: `GEVOELSCORE_DATA_PATH` (default `C:\Users\Gebruiker\Documents\gevoelscore-data` per HA-C4 / HA-C4b / HA11-bout-redo precedent).
- **Seeds**: HA-C4c block-permutation null seed `20260623` (distinct from sister tests). Cliff's delta 95% CI paired-bootstrap: same seed.
- **Statistical machinery**: stationary bootstrap (Politis-Romano 1994), geometric block length E[L]=7, B=10,000 draws; data-driven E[L]\* per Politis-White 2004 + Patton-Politis-White 2009; Mann-Whitney U via vendored mid-rank implementation per HA11-bout-redo precedent.
- **Regenerate command**:
  ```
  cd docs/research/analyses/hypotheses/HA-C4c
  python test.py --dry-run   # §10.4 sanity gates only
  python test.py             # full run; emits result.md + result-data.json
  ```
- **Output files**: `result.md` (committed) + `result-data.json` (machine-readable companion; gitignored per `docs/research/**/*.json` rule).

---

*Pre-registration drafted 2026-06-23 by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Drafting trigger: cascade-resuming after HA11-bout-redo PARTIAL framework-validity verdict 2026-06-23 (`6e06d12`) + β-recalibration r4 0/7 CONFIRMED LOCKED 2026-06-23 (`fb97d1c`). Status: **drafted, not locked**. Audit + lock are separate fresh sessions per [`hypothesis_lock_process.md` §3.4 + §3.5 + §3.8](../../../methodology/hypothesis_lock_process.md). Next stage: fresh-session audit via `/research-review docs/research/analyses/hypotheses/HA-C4c/hypothesis.md`.*
