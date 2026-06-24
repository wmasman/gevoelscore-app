# `resting_hr` -- operationalisation-support descriptive analysis

**Strand**: A (operationalisation support; template-driven; no operationalisation interview required per [`descriptive/README.md`](../../README.md) section 7b).

## Research question

Operationalisation-support descriptive characterisation of `resting_hr` on Stratum 4 + a LOAD-BEARING recovery-axis extension on the full corpus, answering Q3.6.a-i per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`; this channel listed as the HA06b-primary candidate with weak v3 dose-modulation). **2nd of the 5 Tier 2 channels** in the user-prioritised Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain `7d49ba4`; this Q3.6 closes Tier 2 2nd; next: Q3.7 exertion_class, Q3.8 push_burden_7d, Q3.9 gevoelscore).

Substantive status: **HA06b primary operand** (RHR z-score 4d bidirectional; LOCKED TRAIN SUPPORTED +18.9 pp / VALIDATE refuted +0.8 pp / OVERALL REFUTED per [`HA06b-rhr-zscore/result.md`](../../../analyses/hypotheses/HA06b-rhr-zscore/result.md); R14 single-pool **+6.7 pp [CI -18.7, +17.9] perm p=0.3368** NOT-SUPPORTED CONVERGE-ON-OVERALL `badd04a`). Also **H01 primary** (RHR drift absolute 7d-mean +3 bpm; LOCKED REFUTED both eras -1.2 / -9.5 pp; R14 single-pool **-3.1 pp [CI -9.4, +10.1] perm p=0.7820** NOT-SUPPORTED CONVERGE per [`H01-rhr-drift/result.md`](../../../analyses/hypotheses/H01-rhr-drift/result.md)) and **HA06 primary** (morning RHR delta absolute 4-5d bidirectional; LOCKED REFUTED both eras; SUPERSEDED by HA06b per [`HA06-morning-rhr-delta/result.md`](../../../analyses/hypotheses/HA06-morning-rhr-delta/result.md)). Channel IS in v3 multi-channel sweep scope per [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.6 (6-channel scope) and was classified as **REJECTED with weak/non-significant beta** (the 'weakly consistent' v3 row); citalopram-dose-modulation status is REJECTED at v3-locked verdict; Q3.6.d reports observed shifts descriptively per CONVENTIONS section 4.2 caveat-class framing and does NOT promote a v3 REJECTED -> CONFIRMED reclassification per handoff section 3 hard constraint.

## Method

- **Surface**: Stratum 4 primary (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05; n=1357 channel-valid days out of 1372 S4 days) **plus** LOAD-BEARING Q3.6.c extension on the full corpus to include pre_illness_healthy (2021-08-16 to 2022-03-20, ~217 day-level rows) + acute_infection (2022-03-21 to 2022-04-03, ~14 day-level rows) phases for the recovery_arc v2 cardiovascular-family acute-infection DIP reproduction per handoff section 2.4.
- **Primary phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with sister Strand-A analyses Q3.1 / Q3.2 / Q3.3 / Q3.4 / Q3.5.
- **Secondary phase axis (Q3.6.c extension)**: 6-phase LC recovery axis per [`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) (LOCKED `d47e0d3`) on the FULL CORPUS for the recovery_arc v2 acute-infection DIP descriptive reproduction.
- **Delegate**: Q3.6.a (distribution shape) **partial delegate** to [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) + **extend** with full skewness/kurtosis/heavy-tail-flag descriptors.
- **Cross-reference**: Q3.6.h (outliers + calibration-drift) cross-references [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) (UDS-passthrough family entries + chronotropic-incompetence substrate caveat per HA06 + H01 + HA06b result.md).
- **Computed directly from `per_day_master.csv`**: Q3.6.a (distribution shape), Q3.6.b (Politis-White E[L]\* on Stratum-4 pool; cross-reference recovery_arc v2 section 7b E[L]\*=22.7 reproduction), Q3.6.c (per-phase base rates citalopram axis + 6-phase recovery-axis extension on full corpus), Q3.6.d (phase-stratified medians + citalopram-axis shift + v3 REJECTED caveat-class framing per CONVENTIONS section 4.2 + handoff section 3 hard constraint), Q3.6.e (near-identity check |rho|>=0.92 on 15-channel panel), Q3.6.f (crash-vs-normal Cohen's d + Mann-Whitney U + stationary-bootstrap CI at E[L]=7 and data-driven E[L]\* + crash-drop sensitivity + LOAD-BEARING R14 single-pool descriptive cross-reference to HA06b + H01 rows), Q3.6.g (HA06b spike-form construct discussion + cross-channel pairwise correlations), Q3.6.i (covariate-sensitivity readiness for future HA pre-regs).
- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) (`compute_data_driven_block_length`, `stationary_bootstrap_ci`).
- **Load-bearing cross-references** per handoff section 2.4: recovery_arc v2 section 7b E[L]\*=22.7 reproduction in Q3.6.b; recovery_arc v2 cardiovascular-family acute-infection DIP (54 -> 52.5) reproduction in Q3.6.c; R14 HA06b + H01 single-pool results descriptively corroborated in Q3.6.f; v3 dose-response REJECTED weak-beta caveat-class framing in Q3.6.d. NO substantive HA verdict promotion per CONVENTIONS section 2.1; NO v3 REJECTED -> CONFIRMED reclassification per handoff section 3 hard constraint.
- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).

## Result

Headline (see [`findings.md`](findings.md) for the full answers Q3.6.a-i):

`resting_hr` on Stratum 4 is a **daily-aggregate cardiovascular channel** (median 56.00 bpm; MAD 2.00; skew +0.25; heavy_tail_flag=False). **Data-driven E[L]\*=7.0** -- Politis-White FALLBACK to default E[L]=7 (channel ACF too persistent at this Stratum-4 pool resolution; see findings.md Q3.6.b for the load-bearing methodological-divergence flag vs recovery_arc v2 reported 22.7 on the smaller 4a+4b sub-pool). **Phase-stratified medians** (citalopram axis, caveat-class per CONVENTIONS section 4.2 since v3 REJECTED with weak beta): unmedicated 56.00 -> consolidation 57.00 -> afbouw 61.00. Episode-level Cohen's d=-0.07 (bootstrap CI95 [-1.38, +0.94]) -- descriptively corroborates HA06b's locked TRAIN-only-SUPPORTED-now-OVERALL-REFUTED + R14 CONVERGE-ON-OVERALL + H01 both-eras-REFUTED + R14 CONVERGE signals at the coarse first-order-day-level read (HA06b's tested operand is the per-4-day MAX |z| of resting_hr; this Q3.6.f is the first-order day-level descriptive complement, NOT a re-anchoring of HA06b). **Q3.6.c LOAD-BEARING recovery-axis reproduction**: acute-infection DIP REPRODUCES recovery_arc v2 finding (observed -1.50 bpm vs reported -1.5 bpm). Near-identity check: **0** flagged pairs at the |rho|>=0.92 CONVENTIONS section 3.3 threshold.

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + `README.md` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup covering Q3.6.a-i + tables (programmatically emitted by run.py from summary.json per the Q3.2/Q3.3/Q3.4/Q3.5 architectural note about the Write-tool harness heuristic on the literal filename "findings")
- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- 6 PNGs: distribution, phase-stratified violins (citalopram), trajectory-with-phases, crash-vs-normal, ACF, 6-phase recovery-axis violins full corpus (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-05 corpus + 2026-06-24 analysis** (commit context: post-`7d49ba4` Q3.5 bb_overnight_gain LANDED; Phase 2 'finish the descriptive analysis' Tier 2 batch 2nd of 5 channels). Refresh when:

1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to spin up beyond the HA06b-locked operand.
2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 onward).
3. Politis-White E[L]\* shifts by another factor of 2 from current 7.0.
4. A v3-extension or revision run on resting_hr lands and updates the Q3.6.d citalopram-dose-modulation status (v3 currently LOCKED at REJECTED with weak beta).
5. recovery_arc v3 lands and updates the v2 cardiovascular-family per-phase reads (Q3.6.b + Q3.6.c reproductions).
6. HA06b threshold-monotonicity diagnostic or any HA06b-descendant test ships and triggers operationalisation-substrate consumption.

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`)
- **LOAD-BEARING trajectory analysis**: [`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/) (v2 LANDED `8feae6a`); resting_hr is the only channel where 4b-4a paired-bootstrap CI excludes 0 (+3.0 bpm CI [+2.0, +4.0], E[L]\*=22.7); cardiovascular-family acute-infection DIP (54 -> 52.5; parasympathetic dominance during viral infection); Q3.6.b reproduces E[L]\* + Q3.6.c reproduces DIP descriptively.
- **Q3.5 most-recent Tier 2 precedent**: [`descriptive/operationalisation_support/bb_overnight_gain/`](../bb_overnight_gain/) -- Tier 2 1st of 5; programmatic-emit pattern + load-bearing cross-reference template.
- **Q3.4 clean f-string precedent**: [`descriptive/operationalisation_support/stress_stdev_sleep/`](../stress_stdev_sleep/) -- Tier 1 final; full-coverage continuous-channel template.
- **Sister BB-floor inverse-coupling channel**: [`descriptive/operationalisation_support/bb_lowest/`](../bb_lowest/) -- Q3.3 reciprocal rho with resting_hr reported there (NOT near-identity).
- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) -- HA06b + H01 rows descriptively corroborated in Q3.6.d + Q3.6.f.
- **HA-* tests that this analysis anchors**:
  - **HA06b** (LOCKED TRAIN SUPPORTED only / OVERALL REFUTED; R14 single-pool NOT-SUPPORTED CONVERGE-ON-OVERALL); primary operand on this channel.
  - **H01** (LOCKED REFUTED both eras; R14 single-pool NOT-SUPPORTED CONVERGE); absolute spec on this channel.
  - **HA06** (LOCKED REFUTED both eras; SUPERSEDED by HA06b); absolute spec on this channel.
  - **HA-P6 v3** (LOCKED `a980b1c` 2026-06-17): resting_hr is in the 7-channel set + 4-of-7 distinguishable channels.
- **Definitional substrate**: [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) v3 section 5.6 (resting_hr in 6-channel scope; **REJECTED with weak/non-significant beta**; Q3.6.d caveat-class framing).
- **Other methodology MDs**: `lc_phase_descriptive.md`, `citalopram_phase_stratification.md`, `permutation_null_block_length.md`, `garmin_indicators_audit.md`, `lc_era_temporal_segmentation.md`, `lc_recovery_phase_axis.md` (6-phase axis for Q3.6.c extension), `_descriptive_stocktake_2026-06-23.md` (gap-list framing).
- **Existing complementary**: [`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) (Q3.6.e cross-reference; no near-identity in 9-anchor primitive set).
- **Upstream pipeline**: `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `pipeline/01_extract/garmin_uds_extras.py` (UDS-side passthrough for `restingHeartRate` field). `labels_crash_v2.csv` per locked `crash_v2-definition`.
