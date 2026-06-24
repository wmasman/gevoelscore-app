# `stress_stdev_sleep` -- operationalisation-support descriptive analysis

**Strand**: A (operationalisation support; template-driven; no operationalisation interview required per [`descriptive/README.md`](../../README.md) section 7b).

## Research question

Operationalisation-support descriptive characterisation of `stress_stdev_sleep` on Stratum 4, answering Q3.4.a-i per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`; this channel listed as the HA07d-primary-operand candidate). Phase 2 "finish the descriptive analysis" Tier 1 user-prioritised sequential batch; **FOURTH (FINAL) channel closing Tier 1** (R14 `single_pool_reanchor` first at `badd04a`; `all_day_stress_avg` second at `cf34ab1`; `bb_lowest` third at `40c351b`; this `stress_stdev_sleep` fourth). This channel is **HA07d's primary operand** -- HA07d is the **ONLY canonical both-eras-SUPPORTED test in the project** (train +19.6 pp / validate +21.7 pp / OVERALL SUPPORTED per [`HA07d-sleep-stress-variability/result.md`](../../../analyses/hypotheses/HA07d-sleep-stress-variability/result.md)) AND just R14-confirmed at single-pool +19.7 pp perm p (E[L]=7) = 0.0291 per [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) row HA07d -- the **only HA that retained SUPPORTED at single-pool** in the R14 cross-check (`badd04a`). Channel is **NOT in v3 multi-channel sweep scope** per [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.6 (covered 6 channels: stress_mean_sleep + all_day_stress_avg + bb_lowest + resting_hr + bb_overnight_gain + respiration_avg_sleep); **citalopram-dose-modulation status is OPEN** per CONVENTIONS section 4.2 caveat-class framing.

## Method

- **Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05; n=1339 channel-valid days out of 1372 S4 days).
- **Primary phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with sister Strand-A analyses Q3.1 / Q3.2 / Q3.3.
- **Delegate**: Q3.4.a (distribution shape) **partial delegate** to [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) + **extend** with full skewness/kurtosis/heavy-tail-flag descriptors (the delegate target was extended for continuous channels first and primarily documents `stress_mean_sleep`).
- **Cross-reference**: Q3.4.h (outliers + calibration-drift) cross-references [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) (sleep-stress-extraction family entries; no per-column row for stress_stdev_sleep specifically beyond the sister stress_mean_sleep shared lineage).
- **Computed directly from `per_day_master.csv`**: Q3.4.b (Politis-White E[L]\*), Q3.4.c (per-phase base rates), Q3.4.d (phase-stratified medians + citalopram-axis shift; **caveat-class per CONVENTIONS section 4.2** since channel NOT in v3 scope), Q3.4.e (near-identity check |rho|>=0.92 on 10-channel panel; **load-bearing substantive-independence check vs mean sibling `stress_mean_sleep` per handoff section 2.4**), Q3.4.f (crash-vs-normal Cohen's d + Mann-Whitney U + stationary-bootstrap CI at E[L]=7 and data-driven E[L]\* + crash-drop sensitivity per section 3.4 + crash-subset rho vs mean sibling supplementary), Q3.4.g (variability-primitive IS second-order spike-form discussion + cross-channel pairwise correlations), Q3.4.i (covariate-sensitivity readiness for future HA pre-regs).
- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) (`compute_data_driven_block_length`, `stationary_bootstrap_ci`).
- **Load-bearing cross-references** per handoff section 2.4: HA07d both-eras-SUPPORTED + R14 single-pool +19.7 pp p=0.0291 descriptively corroborated in Q3.4.f; sister-channel E[L]\* spread (12.6 / 21.1 / 29.25 / 29.8) cross-referenced in Q3.4.b; v3 dose-response open question framed caveat-class in Q3.4.d; near-identity vs mean sibling rigorously checked in Q3.4.e. NO substantive HA verdict promotion per CONVENTIONS section 2.1; NO CONFIRMED/REJECTED citalopram-modulation verdict pre-committed for Q3.4.d per CONVENTIONS section 4.2.
- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).

## Result

Headline (see [`findings.md`](findings.md) for the full answers Q3.4.a-i):

`stress_stdev_sleep` on Stratum 4 is a **per-night SECOND-ORDER variability channel** (skew=+1.87, excess kurtosis=+5.41, heavy_tail_flag=True). **Data-driven E[L]\*=7.0** -- vs sister Strand-A channels stress_mean_sleep 12.6 / stress_low_motion 21.1 / bb_lowest 29.25 / all_day_stress_avg 29.8. **Phase-stratified medians** (citalopram axis, caveat-class per CONVENTIONS section 4.2 since channel NOT in v3 scope): unmedicated 8.10 -> consolidation 6.63 -> afbouw 6.76. Episode-level Cohen's d=+0.48 (bootstrap CI95 [+0.315, +2.155]) -- descriptively corroborates HA07d's locked OVERALL-SUPPORTED + R14 single-pool +19.7 pp p=0.0291 signal at the coarse first-order-day-level read (HA07d's tested operand is the per-4-day MAX |z| of night-over-night delta; this Q3.4.f is the first-order day-level descriptive complement, NOT a re-anchoring of HA07d). Near-identity check vs mean sibling: see findings.md Q3.4.e for substantive-independence reading (HA07d both-eras-SUPPORTED + HA07c train-only-SUPPORTED divergence is descriptively consistent with rho<0.92 substantive independence).

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + `README.md` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup covering Q3.4.a-i + tables (programmatically emitted by run.py from summary.json per the Q3.2/Q3.3 architectural note about the Write-tool harness heuristic on the literal filename "findings")
- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- 5 PNGs: distribution, phase-stratified violins, trajectory-with-phases, crash-vs-normal, ACF (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-05 corpus + 2026-06-24 analysis** (commit context: post-`40c351b` Q3.3 bb_lowest LANDED; Phase 2 "finish the descriptive analysis" Tier 1 user-prioritised CONFIRMED-citalopram channel batch FINAL CHANNEL; R14 first at `badd04a`; Q3.2 second at `cf34ab1`; Q3.3 third at `40c351b`; **this Q3.4 fourth closes Tier 1**). Refresh when:

1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to spin up beyond the HA07d-locked operand.
2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 onward).
3. Politis-White E[L]\* shifts by another factor of 2 from current 7.0.
4. A v3-extension run on this channel lands and updates the Q3.4.d citalopram-modulation status from OPEN to CONFIRMED/REJECTED.
5. A `stress_stdev_sleep_lagged_lcera_z` materialisation lands in `per_day_master.csv` and updates the Q3.4.i covariate-4 needed-columns entry.
6. HA07d threshold-monotonicity diagnostic or any HA07d-descendant test ships and triggers operationalisation-substrate consumption.

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`)
- **First Strand A analysis** (template anchor + mean sibling): [`descriptive/operationalisation_support/stress_mean_sleep/`](../stress_mean_sleep/) -- mean sibling of same nightly stress series; closest precedent.
- **Q3.2 sibling**: [`descriptive/operationalisation_support/all_day_stress_avg/`](../all_day_stress_avg/) -- Phase-2 first precedent; programmatic-emit pattern.
- **Q3.3 most-recent precedent**: [`descriptive/operationalisation_support/bb_lowest/`](../bb_lowest/) -- inverse-direction CONFIRMED-citalopram sister; cross-channel E[L]\* spread comparison.
- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) -- HA07d row +19.7 pp p=0.0291 descriptively corroborated in Q3.4.f.
- **HA-* tests that this analysis anchors**:
  - **HA07d** (LOCKED OVERALL-SUPPORTED -- the ONLY canonical both-eras-SUPPORTED test in the project + R14 single-pool SUPPORTED); primary operand of HA07d.
  - HA07d threshold-monotonicity diagnostic (LOCKED; downstream of HA07d).
  - HA07c (LOCKED OVERALL-REFUTED; mean sibling channel); substantive-independence vs HA07d reflected in Q3.4.e.
  - HA08c (LOCKED OVERALL-REFUTED; slope-of-mean-sibling); inherits Q3.4.b autocorrelation context.
- **Definitional substrate**: [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.6 (v3 sweep scope -- this channel NOT in scope; Q3.4.d caveat-class framing).
- **Other methodology MDs**: `lc_phase_descriptive.md`, `citalopram_phase_stratification.md`, `permutation_null_block_length.md`, `garmin_indicators_audit.md`, `lc_era_temporal_segmentation.md`, `_descriptive_stocktake_2026-06-23.md` (gap-list framing).
- **Existing complementary**: [`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) (Q3.4.e cross-reference).
- **Upstream pipeline**: `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `processed/garmin/sleep_stress_nightly.csv` <- `garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`. `labels_crash_v2.csv` per locked `crash_v2-definition`.
