# HA-C4c - RESULT: PARTIAL

Emitted by `test.py` per LOCKED r2 hypothesis.md section 10.3. **Headline cell**: cross-phase-pooled stratum on the `citalopram_phase` axis (equivalently `recovery_phase` in {`pacing_habit_established`, `citalopram_modulated`}) x `bout_n_did_not_return` x heavy-T-vs-non-heavy-T x Mann-Whitney U + Cliff's delta + block-permutation null at E[L]=7. **Seed**: `RANDOM_SEED = 20260623`; **B** = 10000. **Operand direction**: heavy-T > non-heavy-T (one-sided elevated).

## Authorship

- **Drafting date**: 2026-06-23 (this result.md emitted in the post-lock test-execution session).
- **Agent**: Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS section 1.1](../../../CONVENTIONS.md). Authorising user: Willem.
- **Pre-reg commit**: r2 LOCKED 2026-06-23 at [`hypothesis.md`](hypothesis.md) commit `4e666a2` (substantive absorb `310e145`). Worktree HEAD at run: `a59997a`.
- **Test commit**: this session's `test.py` commit (set by dispatcher after cherry-pick).
- **Pipeline commit**: bout-extraction pipeline LOCKED at `d5b394c` (2026-06-22). Smoke tests re-confirmed PASS at run-time per section 8.
- **Status**: LANDED. Test executed end-to-end; dry-run section 10.4 gates passed; primary headline emitted; sensitivity arms reported; cascade implication recorded in section 6.

## Section 1 - Headline verdict + cascade-context calibration discount

**Verdict: PARTIAL** -- direction=+, (a) p<0.05=PASS (p=0.0001), (b) delta>=+0.20=FAIL (delta=+0.120).

**HA11-bout-redo PARTIAL framework-validity calibration discount (load-bearing per pre-reg section 8 caveat 2; cascade-context discipline)**: HA11-bout-redo's framework-validity gate cleared bars 1+2 (directional sign + effect-size comparability) at +20.26 pp / median signed z 2.410 - magnitude-validates the operand - but **bar 3 (block-permutation p<0.05) FAILED at p=0.2609** at the n_calm=70/n_crash=11 stratum. The propagation to HA-C4c: the bout-level operand is *partially fit for purpose*; HA-C4c verdict-magnitudes are interpreted with a calibration discount. The HA-C4c verdict MUST be read with this calibration context visible.

**Cross-test cascade implication (section 9.2 PARTIAL branch; bar (b)-failing configuration)**: direction-correct AND (a) block-perm p < 0.05 (here p=0.0001, well below threshold) AND (b) Cliff's delta < +0.20 (here delta=+0.120, comfortably in [+0.10, +0.15] band). The discriminative signal is **statistically distinguishable from the null at very high confidence** but the effect size is below the small-to-medium +0.20 threshold the pre-reg pre-committed. Reading per pre-reg section 9.2: the signal exists and is statistically real but small in magnitude - a **weak-effect-but-real positive pattern**.

**Important distinction vs HA11-bout-redo's bar-3 PARTIAL pattern**: HA-C4c's bar-(b) failure-mode is the *opposite* failure-mode shape from HA11-bout-redo. HA11-bout-redo had directional + effect-size comparability PASS (bars 1+2 at +20.26 pp) with **block-perm p FAIL** (bar 3 at p=0.2609) - i.e., magnitude reproduces the signal but the small n_calm=70/n_crash=11 stratum cannot statistically distinguish it. HA-C4c at the cross-phase-pooled stratum (n_heavy=465, n_non_heavy=809) has the *inverse* shape: **block-perm p PASS at p=0.0001** but **effect size BELOW the +0.20 small-to-medium threshold**. The materially-larger n removed HA11-bout-redo's power-shortfall constraint (per pre-reg section 8 caveat 2 expectation); the substantive finding is that the heavy-T vs non-heavy-T contrast on this corpus's `bout_n_did_not_return` operand is real but smaller in magnitude than the +0.20 threshold the pre-reg pre-committed.

## Section 2 - Per-bar table

| bar | target | observed | result |
|---|---|---:|:---:|
| direction | heavy-T > non-heavy-T (Cliff's delta > 0) | delta = +0.120 | PASS |
| **Bar (a) - discrimination** | block-perm p < 0.05 | p = 0.0001 | PASS |
| **Bar (b) - effect size** | Cliff's delta >= +0.2 | delta = +0.120 | FAIL |

## Section 3 - Per-arm summary table (primary cell)

| metric | heavy-T arm | non-heavy-T arm |
|---|---:|---:|
| n_days | 465 | 809 |
| mean `bout_n_did_not_return` | 0.742 | 0.588 |
| median `bout_n_did_not_return` | 1.00 | 1.00 |
| Mann-Whitney U (heavy first) | 210614 | -- |
| Mann-Whitney p (one-sided normal approx, descriptive) | 0.0002 | -- |
| Cliff's delta (heavy vs non-heavy) | +0.120 | -- |
| Cliff's delta 95% CI (paired-bootstrap B=2000) | [+0.064, +0.178] | -- |
| block-permutation p (E[L]=7, B=10000, seed `20260623`) | 0.0001 | -- |
| block-perm null delta median | -0.000 | -- |
| block-perm null delta 95% CI | [-0.061, +0.060] | -- |
| n_did_not_return bouts in pool (sum across days) | 821 | -- |

## Section 4 - Companion descriptives (per-day distribution + section 7 sanity)

| metric | observed | section 7 expected | sanity status |
|---|---:|---|:---:|
| per-day mean | 0.6444 | [0.3, 1.5] | PASS |
| per-day median | 1.00 | <= 4.0 | PASS |
| per-day sigma | 0.6703 | [0.5, 2.0] | PASS |
| per-day p25-p75 | [0.00, 1.00] | -- | -- |
| per-day range | [0.00, 3.00] | -- | -- |

**E[L]\* data-driven companion** (CONVENTIONS section 3.6 + parent MD section 5.1): E[L]\* = 7.00 days (cutoff_lag=1); factor-of-2 deviation flag: NOT FLAGGED. Per pre-reg section 4.6 + CONVENTIONS section 3.6: factor-of-2 flag is descriptive context only; does NOT modify the section 5 verdict.

## Section 5 - Sensitivity arms (per section 4.10; descriptive, cannot promote to SUPPORTED)

| arm | n_heavy | n_non_heavy | heavy mean | non-heavy mean | Cliff's delta | block-perm p | (a) | (b) | verdict | fragility vs primary |
|---|---:|---:|---:|---:|---:|---:|:---:|:---:|:---:|---|
| **primary** (cross-phase-pooled) | 465 | 809 | 0.742 | 0.588 | +0.120 | 0.0001 | PASS | FAIL | **PARTIAL** | -- |
| unmedicated-only stratum | 183 | 323 | 0.776 | 0.690 | +0.059 | 0.1145 | FAIL | FAIL | REJECTED | flagged |
| motion-clean-only (motion_confound_flag=False) | 465 | 809 | 0.002 | 0.000 | +0.002 | 0.1841 | FAIL | FAIL | REJECTED | flagged |
| transient-excluded (transient_flag=False) | 465 | 809 | 0.703 | 0.557 | +0.116 | 0.0001 | PASS | FAIL | PARTIAL | consistent |
| baseline-invalid-excluded (baseline_invalid_flag=False) | 465 | 809 | 0.716 | 0.560 | +0.123 | 0.0001 | PASS | FAIL | PARTIAL | consistent |

**Motion-clean-only arm corpus-property reaffirmation (per pre-reg section 8 caveat 4)**: 4285 of 4317 bouts (99.3%) carry `motion_confound_flag=True` on this corpus + extraction threshold; only 32 motion-clean bouts exist. Re-aggregating `bout_n_did_not_return` over the motion-clean subset produces near-zero per-day counts on essentially all days (heavy mean 0.002, non-heavy mean 0.000). The walk-forward gate clears (n_heavy=465, n_non_heavy=809; both arms still have valid days) so the arm doesn't route to INCONCLUSIVE as pre-reg section 8 caveat 4 anticipated; instead the discriminative signal collapses to near-zero (delta=+0.002, p=0.1841). The verdict resolves to REJECTED via the section 5.2 "both bars fail" path. **Reading**: this is the **corpus-property reaffirmation** the pre-reg anticipated, manifesting as a near-zero-signal arm rather than a degenerate-n arm. The framework-validity reading is unchanged from HA11-bout-redo's section 4 framing: the bouts-as-currently-extracted ARE motion-tagged events; any "rest-stress" semantic claim is necessarily across the motion-tagged pool. The result.md does NOT promote this to a fragility-of-primary finding (the primary's PARTIAL verdict is at the cross-phase-pooled stratum that includes motion-tagged bouts per parent MD section 3.4 default); it documents the corpus property as a substantive context.

**Unmedicated-only stratum REJECTED divergence (stratum-fragility finding per pre-reg section 9.5)**: the unmedicated-only sensitivity arm fails both bars (delta=+0.059 < +0.20; p=0.1145 >= 0.05) at the smaller n_heavy=183/n_non_heavy=323 stratum. Direction-correct (delta=+0.059 positive) but with too small an effect AND insufficient block-perm signal to clear (a). Reading: the primary cross-phase-pooled stratum's PARTIAL verdict is **stratum-pooling-dependent** - the cross-phase pooling (gaining ~282 heavy + ~486 non-heavy days from the medicated phases) is doing analytical work. The unmedicated-only effect size is materially smaller (+0.059 vs +0.120 at primary). Per pre-reg section 9.5 + section 8 caveat 8: the cross-phase pooling permission is conditional on the recalibration's 0/7 CONFIRMED reading; this divergence is the descriptive signature of that pooling being load-bearing for the substantive signal. Per pre-reg section 8 caveat 10 (pacing-behaviour confounder): the unmedicated stratum is the more pacing-pure-vs-medicated subset; the smaller effect size there is consistent with the medicated phases contributing more to the headline contrast (perhaps via dose-shaped baseline shifts the operand picks up). This is a **stratum-fragility finding** to surface to downstream readers; the primary verdict is unchanged (single-cell headline lock per pre-reg section 5.0).

### Crash-drop sensitivity (CONVENTIONS section 3.4 + pre-reg section 4.10)

| metric | primary | crash-dropped | delta |
|---|---:|---:|---:|
| n_heavy | 465 | 441 | -24 |
| n_non_heavy | 809 | 745 | -64 |
| Cliff's delta | +0.120 | +0.135 | +0.015 |
| block-perm p | 0.0001 | 0.0001 | 0.0000 |
| verdict | PARTIAL | PARTIAL | unchanged |

**|Delta Cliff's delta| = 0.015** (threshold 0.1 per CONVENTIONS section 3.4 + HA-C4 v2 pattern): NOT FIRED (clean). **|Delta Cliff's delta * 100| = 1.51 pp** (threshold 5.0 pp per HA11-bout-redo analogue): NOT FIRED. **Route to REJECTED** (|delta delta| > 0.2 AND sign-flip): NO.

### Approach A dose-adjusted sensitivity arm (section 4.9 inheritance-by-analogue; descriptive companion only)

Per pre-reg section 4.9 r2 underpowered-NULL framing + section 8 caveat 3: the Approach A inheritance is **inheritance-by-analogue** from `bout_n_fast_recovery_day` buildup-post-CPAP beta = -0.056/mg [CI -0.145, +0.034] (sign-flipped to +0.056/mg for HA-C4c's +1 prior direction). The source beta is NULL/weakly-consistent (CI crosses zero; p=0.223 in the source recalibration). This is a **descriptive companion** under the underpowered-NULL frame; NOT a load-bearing dose-correction. The CI-bracket sub-arm characterises **inheritance fragility**, NOT a substantive precision check.

| sub-arm | beta/mg | Cliff's delta | block-perm p | (a) | (b) | verdict | divergence from primary |
|---|---:|---:|---:|:---:|:---:|:---:|---|
| Approach A primary template | +0.056 | +0.098 | 0.0075 | PASS | FAIL | PARTIAL | consistent |
| CI lower bracket (NULL) | +0.145 | +0.076 | 0.0352 | PASS | FAIL | PARTIAL | consistent |
| CI upper bracket (NULL) | -0.034 | +0.077 | 0.0259 | PASS | FAIL | PARTIAL | consistent |

## Section 6 - Holm step-down (section 5.3; secondary fragility-flag report)

**Holm (4-of-4 sens arms; all valid)** at alpha=0.05.

| cell | rank | raw p | threshold | adjusted p | Holm-rejected |
|---|---:|---:|---:|---:|:---:|
| primary | 1 | 0.0001 | 0.01250 | 0.0004 | YES |
| transient_excluded | 2 | 0.0001 | 0.01667 | 0.0004 | YES |
| unmedicated_only | 3 | 0.1145 | 0.02500 | 0.2290 | NO |
| motion_clean | 4 | 0.1841 | 0.05000 | 0.2290 | NO |

Per pre-reg section 5.3: Holm is a secondary fragility-flag report. The primary verdict per section 5.2 is the uncorrected primary cell; Holm cannot override.

## Section 7 - Sister-test cross-reference table

Per pre-reg section 4.10 + CONVENTIONS section 4.4: descriptive only; NO cross-test pass conclusion at result-emission time. Cross-test interpretation is a separate post-lock synthesis session.

| hypothesis | verdict | one-line note |
|---|---|---|
| HA-C4 v2 | REJECTED | daily-aggregate triad sum 0.0/3.0; Ch1 drop_avg SUPPORTED both eras |
| HA-C4b v3 | NOT-SUPPORTED | motion-filter crash-precursor; per-episode operationalisation |
| HA11 v1 | SUPPORTED-on-train | U-dip count +22.8 pp; calm-day sister channel |
| HA11-bout-redo | PARTIAL | framework-validity 2-of-3 bars met; bar 3 p=0.2609 at n_calm=70/n_crash=11 |
| **HA-C4c (this test)** | **PARTIAL** | cross-phase-pooled bout-level; delta=+0.120, p=0.0001, n_heavy=465, n_non_heavy=809 |

## Section 8 - Pipeline-trust block

Bout-extraction pipeline LOCKED at commit `d5b394c` (2026-06-22, [`extract_stress_bouts.py`](../../../pipeline/02_features/extract_stress_bouts.py)). The pipeline's 9 inline smoke tests provide audit coverage. **Smoke tests re-confirmed PASS at run-time** per pre-reg section 10.1 (run-step pre-flight check; verified by the dispatcher prior to test.py invocation).

- Test 1: canonical bout detected, peak=80, returns -- PASS
- Test 2: did_not_return fires; tail_length capped at 180 -- PASS
- Test 3 + 3b: cross-midnight peak attribution -- PASS
- Test 4: NaN gaps in pre-window correctly fail hysteresis -- PASS
- Test 5: transient bout flagged -- PASS
- Test 6a/6b/6c: motion_confound flag logic -- PASS

## Section 9 - Verification log

Anchors the test on the cascade state at run-time:

- Pre-reg `hypothesis.md` LOCKED 2026-06-23 r2 commit `4e666a2` (substantive absorb `310e145`).
- Worktree HEAD at test-time: `a59997a`.
- Pipeline (`extract_stress_bouts.py`) commit: `d5b394c` (LOCKED 2026-06-22).
- Parent MD (`bout_level_recovery_dynamics.md`) LOCKED at `c57ff3f` (2026-06-21).
- Sub-MD (`bout_level_dose_response_calibration.md`) r4 LOCKED at `fb97d1c` (2026-06-23); inheritance table populated to 0/7 CONFIRMED.
- HA11-bout-redo result PARTIAL at commit `6e06d12` (2026-06-23); used for the cascade-context calibration discount per pre-reg section 8 caveat 2.
- HA-C4 v2 result REJECTED at commit `52bddb5` (2026-06-18); used for the daily-aggregate reference per pre-reg section 1 + section 9.3.
- Re-audit (`reviews/HA-C4c-2026-06-23-v2-reaudit.md`) PASS-with-caveats; NO L1-L4 fires; two optional precision items at section 4 explicitly NOT gating.
- Dry-run gates per section 10.4 + section 7: all 4 PASS at run-time (walk-forward n_heavy=465, n_non_heavy=809; per-day mean=0.6444; median=1.00; sigma=0.6703).
- Per-day master CSV: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` (column `bout_n_did_not_return`); primary stratum non-NaN days: 1274.
- Per-bout master CSV: `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.csv` (4317 bouts; used for section 4.10 sensitivity-arm re-aggregation).

## Section 10 - Caveats (per pre-reg section 8; all 10 prominently surfaced)

1. **Power-calc dispatch (LOCKED verbatim from pre-reg)**: power calc inapplicable per [Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) within-subject design. The block-permutation null at E[L]=7 is the within-subject inferential machinery; the section 5 verdict bars determine substantive verdict rather than asymptotic-power thresholds. INCONCLUSIVE cells per section 4.7 walk-forward gate are the operational definition of 'underpowered for this cell'.

2. **Framework-validity calibration caveat from HA11-bout-redo PARTIAL** (load-bearing per cascade-context discipline): HA11-bout-redo's framework-validity gate cleared bars 1+2 (+20.26 pp / median signed z 2.410) but **bar 3 FAILED at p=0.2609 at n_calm=70/n_crash=11**. The HA-C4c verdict MUST be read with this calibration context visible. Per the cascade-resuming session's framing discipline, the HA-C4c result.md propagates this caveat at the top alongside the headline verdict (see section 1).

3. **beta-recalibration dose-naive primary framing**: 0/7 features CONFIRMED at this corpus's bout-level n in the recalibration; Approach A is NOT load-bearing -> HA-C4c primary is dose-naive. Cross-phase pooling permitted without section 5.A/B/C inheritance violation. The Approach A sensitivity arm uses inheritance-by-analogue (descriptive companion under the underpowered-NULL frame); divergence from primary is informative about per-bout dose-modulation precision on `bout_n_did_not_return`, NOT a fragility of the primary verdict.

4. **99.3% motion-confound corpus property**: 4285/4317 bouts (99.3%) carry `motion_confound_flag=True` on this corpus + extraction threshold. The entire HA-C4c operand inherits this corpus-property finding; Wiggers' 'during rest periods' language is operationalised against the motion-tagged bout pool. The motion-clean-only sensitivity arm was anticipated to be INCONCLUSIVE per this finding; observed REJECTED with near-zero discriminative signal (delta=+0.002, p=0.1841) - a slightly different manifestation of the same corpus property (the n stays valid because zero-count days are still valid; the discriminative signal collapses to noise). See section 5 motion-clean reaffirmation paragraph.

5. **Transient-fragility**: HA11-bout-redo's transient-excluded discrimination dropped from +20.26pp to +11.69pp; a non-trivial fraction of the bout-level signal lives in transient bouts. HA-C4c primary INCLUDES transients per parent MD section 3.1 r2 absorb; transient-excluded variant is the section 4.10 sensitivity arm. Fragility flag fires if verdict swings under transient exclusion.

6. **n=1 single-subject + observational + multi-source**: per CONVENTIONS section 3.1 + the chained-regime methodology MD. Personal-baseline thresholds; cross-subject generalisation out of scope.

7. **Operational vs mechanistic**: per-bout features are operational descriptions of the per-minute Garmin stress trace, NOT mechanistic measurements of autonomic state. A SUPPORTED verdict is a statement about per-minute-trace-operand patterns on heavy-T vs non-heavy-T days, NOT about autonomic-recovery physiology directly. The upstream Firstbeat algorithm is opaque (closed-source); per-bout features surface algorithmic artefacts that daily-aggregate hid.

8. **Cross-phase pooling permissibility is conditional on the recalibration's 0/7 CONFIRMED reading**: if a future expanded corpus or revised bout-detection rule materially changes the per-window n and produces CONFIRMED features in the recalibration, the cross-phase pooling permission may need to be revisited; HA-C4c would then need a v2 with per-phase stratification OR Approach A as primary. **Observed manifestation**: the unmedicated-only sensitivity arm REJECTED verdict (delta=+0.059, p=0.1145 at n_heavy=183/n_non_heavy=323) diverges from the primary cross-phase-pooled PARTIAL verdict (delta=+0.120, p=0.0001). Per pre-reg section 9.5 stratum-fragility, this is a substantive descriptive finding about how the cross-phase pooling shapes the headline contrast; the primary verdict per pre-reg section 5.0 single-cell headline lock is unchanged but the divergence is informative for downstream sister-test framing.

9. **HA-C4 v2 daily-aggregate REJECTED is the prior state of evidence at coarser resolution**: HA-C4c does NOT supersede HA-C4 v2's verdict at daily-aggregate level - that REJECTED verdict stands as the historical record for daily-aggregate operationalisation. The two verdicts coexist; the C4 register row will carry pointers to BOTH at HA-C4c lock.

10. **Pacing-behaviour confounder** (inherited from HA-C4 v2 section 8 + parent MD section 2.4): if the within-day stress pattern this participant generates is mediated by active pacing behaviour (participant uses Garmin stress as a live pacing signal), bout-level analysis may not 'fix' the daily-aggregate flatness - it may reveal that the pacing behaviour shapes per-bout features too. The cross-phase-pooled stratum partially insulates against this (sub-phase 4b + phase 5 span the post-2022-11-17 pacing-stable LC era; pre-pacing-stable era days are excluded). A SUPPORTED-here-NOT-SUPPORTED-at-HA-C4b shape is consistent with the protective-rather-than-predictive alternative reading from HA-C4b v3 section 9.

## Section 11 - Downstream actions (per pre-reg section 9 branch that actually fired)

Per pre-reg section 9.2 PARTIAL branch:

- The C4 register row updates at HA-C4c lock to add a PARTIAL pointer with the configuration explicitly named.
- Cross-test pass folds in the PARTIAL configuration: PARTIAL-with-(a)-failing is interpretively distinct from PARTIAL-with-(b)-failing.
- Optionally: HA-C4c-v2 may be drafted with a refined operand (e.g. `bout_recovery_half_life_median_day` as primary; OR a 3-channel triad). NOT required; PARTIAL does not halt the cascade.
- Parent MD + sub-MD + pipeline all remain LOCKED.

---

*Test run 2026-06-23 by Claude (Opus 4.7) in producer-mode under user authorisation per [CONVENTIONS section 1.1](../../../CONVENTIONS.md). Pre-registration LOCKED 2026-06-23 r2 at [`hypothesis.md`](hypothesis.md) commit `4e666a2` (substantive absorb `310e145`). Worktree HEAD at run: `a59997a`. Pipeline commit: `d5b394c`. `result-data.json` is the machine-readable companion (gitignored per `docs/research/**/*.json` rule).*
