# `bb_overnight_gain` -- operationalisation-support descriptive analysis

**Strand**: A (operationalisation support; template-driven; no operationalisation interview required per [`descriptive/README.md`](../../README.md) section 7b).

## Research question

Operationalisation-support descriptive characterisation of `bb_overnight_gain` (HA10 primary Wiggers D2 operand in primitive form; SLEEPEND - SLEEPSTART overnight recharge arc) on the truth-available analytic window, answering Q3.5.a-i + Q3.5.j (channel-specific coverage extension) per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`). **First of the 5 Tier 2 channels** in the user-prioritised Phase 2 batch (Tier 1 closed `39d7693`; Tier 2 sequential: this bb_overnight_gain first, then `resting_hr`, `exertion_class`, `push_burden_7d`, `gevoelscore`).

Substantive status: **HA10 primary operand surrogate** (HA10 itself tested bb_highest as the morning BB peak proxy via UDS; bb_overnight_gain is the sleep-recharge-arc Wiggers D2 channel in primitive form). HA10 LOCKED OVERALL-REFUTED with era-directionality reversal (train -20.5 / validate +16.2 pp); just R14-confirmed CONVERGE-ON-OVERALL at single-pool **+4.1 pp [-16.5, +16.8] perm p=0.4328** (`badd04a`).

## Method

- **LOAD-BEARING coverage anchor**: [`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md) (truth coverage starts 2024-09-18 per Garmin's UDS `SLEEPEND` rollout on this FR245; proxy r=0.989 bridge 2024-07-08 to 2024-09-17). **Truth-only window 2024-09-18 -> 2026-06-05 adopted as primary** for Q3.5.a-i. The default Stratum 4 2022-09-03+ window does NOT have full coverage; Q3.5.j explicitly justifies the window choice.
- **Surface**: truth-available window (2024-09-18 to 2026-06-05); n=593 channel-valid days. Unmedicated + buildup citalopram phases structurally absent on truth; consolidation + afbouw are the only fully-coverable per-phase cells.
- **Primary phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 (unmedicated / buildup / consolidation / afbouw) -- coverage-restricted per Q3.5.j.
- **Computed directly from `per_day_master.csv`**: Q3.5.a (distribution shape on signed compound-difference channel), Q3.5.b (Politis-White E[L]\* on truth window), Q3.5.c (per-phase base rates, coverage-restricted), Q3.5.d (consolidation -> afbouw delta + HA10 R14 single-pool descriptive cross-reference + v3 'partial' caveat-class framing), Q3.5.e (near-identity check |rho|>=0.92 + multi-resolution bb_lowest sister-channel reproduction per handoff section 2.4), Q3.5.f (crash-vs-normal Cohen's d + Mann-Whitney U + stationary-bootstrap CI at E[L]=7 + data-driven E[L]\* + crash-drop sensitivity), Q3.5.g (compound-difference-form discussion + BB-family pairwise correlations), Q3.5.h (outliers + calibration-drift; coverage-restricted boundary-step reads), Q3.5.i (covariate-sensitivity readiness for future HA pre-regs).
- **Channel-specific Q3.5.j extension** per handoff section 2.4: LOAD-BEARING coverage analysis (truth/proxy/best 3-way + per-phase coverage + analytic-window-choice justification + blocked-per-phase reads explicit).
- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) (`compute_data_driven_block_length`, `stationary_bootstrap_ci`).
- **Load-bearing cross-references** per handoff section 2.4: bb_overnight_gain_proxy.md coverage framing applied in Q3.5.j; HA10 R14 single-pool re-anchor (badd04a) descriptively corroborated in Q3.5.d; Q3.3 bb_lowest sister-channel rho reproduced + extended in Q3.5.e; sister-channel E[L]\* spread context in Q3.5.b. NO substantive HA verdict promotion per CONVENTIONS section 2.1.
- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).

## Result

Headline (see [`findings.md`](findings.md) for the full answers Q3.5.a-j):

`bb_overnight_gain` on truth-only window is a **signed compound-difference channel** (skew=-0.52, excess kurtosis=+0.41, heavy_tail_flag=False; share negative = 0.0%). **Data-driven E[L]\*=6.5** -- vs sister Strand-A channels stress_stdev_sleep 7.0 / stress_mean_sleep 12.6 / stress_low_motion 21.1 / bb_lowest 29.25 / all_day_stress_avg 29.8. **Per-phase trajectory on truth-coverage-restricted window**: consolidation median 49.00 -> afbouw 49.00 (the only fully-bracketed per-phase shift; unmedicated + buildup blocked by coverage per Q3.5.j load-bearing analysis). Episode-level Cohen's d=-0.80; bootstrap CI95 [-17.31, -3.64]. **Q3.5.j load-bearing**: truth coverage starts 2024-09-18; proxy r=0.989 bridge 2024-07-08 to 2024-09-17 available as sensitivity but not adopted for primary per bb_overnight_gain_proxy.md discipline rule 2; truth-only window adopted for Q3.5.a-i headlines.

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + `README.md` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup covering Q3.5.a-j + tables (programmatically emitted by run.py from summary.json per the Q3.2/Q3.3/Q3.4 architectural note about the Write-tool harness heuristic on the literal filename "findings")
- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- 5 PNGs: distribution, phase-stratified violins, trajectory-with-phases, crash-vs-normal, ACF (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-24** (commit context: post-`39d7693` Tier 1 closed; Tier 2 first of 5 = this bb_overnight_gain; next: resting_hr, exertion_class, push_burden_7d, gevoelscore).

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`)
- **LOAD-BEARING methodology MD**: [`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md) (coverage framing).
- **Sister BB-channel analysis**: [`descriptive/operationalisation_support/bb_lowest/`](../bb_lowest/) -- Q3.3.k reciprocal bb_overnight_gain pair (rho ~+0.19 NOT near-identity); this Q3.5 reproduces from the gain side + extends to multi-resolution.
- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) -- HA10 row descriptively corroborated in Q3.5.d.
- **Most-recent Strand-A precedent**: [`descriptive/operationalisation_support/stress_stdev_sleep/`](../stress_stdev_sleep/) -- Q3.4 (programmatic-emit pattern + clean f-string discipline).
- **HA-* tests that this analysis anchors**:
  - HA10 (LOCKED OVERALL-REFUTED; R14 single-pool NOT-SUPPORTED CONVERGE-ON-OVERALL); HA10 primary is bb_highest -- bb_overnight_gain is the sleep-recharge-arc primitive in Wiggers D2 form.
- **Definitional substrate**: [`pipeline/01_extract/garmin_uds_extras.py`](../../../../pipeline/01_extract/garmin_uds_extras.py) (derivation: SLEEPEND - SLEEPSTART from UDS bodyBatteryStatList).
- **Other methodology MDs**: `citalopram_phase_stratification.md`, `citalopram_dose_response_stress_mean_sleep.md` (v3 section 5.6 'partial' status), `permutation_null_block_length.md`, `garmin_indicators_audit.md`, `lc_era_temporal_segmentation.md`.
- **Upstream pipeline**: `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `pipeline/01_extract/garmin_uds_extras.py`. `labels_crash_v2.csv` per locked `crash_v2-definition`.
