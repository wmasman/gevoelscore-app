# `bb_lowest` -- operationalisation-support descriptive analysis

**Strand**: A (operationalisation support; template-driven; no operationalisation interview required per [`descriptive/README.md`](../../README.md) section 7b).

## Research question

Operationalisation-support descriptive characterisation of `bb_lowest` on Stratum 4, answering Q3.3.a-k per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.3 (LOCKED 2026-06-18 r3, commit `ccbd12e`). Phase 2 "finish the descriptive analysis" Tier 1 user-prioritised sequential batch; **third (final) of the 3 CONFIRMED-citalopram channels** (R14 `single_pool_reanchor` first at `badd04a`; `all_day_stress_avg` second at `cf34ab1`; this `bb_lowest` third; `stress_stdev_sleep` closes Tier 1 next). This channel is the **CONFIRMED-citalopram channel with the largest absolute beta** (-1.134/mg p=0.000 buildup post-CPAP per [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.6.1; sister stress_mean_sleep +0.43/mg; sister all_day_stress_avg +0.57/mg; this channel -1.13/mg INVERSE direction; citalopram **raises** bb_lowest). **HA10 floor-side companion (HA10 primary is bb_highest)**; **HA-P6 v3 distinguishable channel** (4/7 in matched-control framework); **HA-C4b BB-floor candidate channel** (DEFERRED per STOCKTAKE section 6). **recovery_arc v2 standout** -- the channel where afbouw GOES LOWER than even unmedicated baseline (load-bearing finding per recovery_arc v2 section 5.A + STOCKTAKE section 6 line 187).

## Method

- **Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05; n=1359 channel-valid days out of 1372 S4 days).
- **Primary phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with sister CONFIRMED-citalopram analyses.
- **Delegate**: Q3.3.a (distribution shape) **partial delegate** to [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) + **extend** with full skewness/kurtosis/heavy-tail-flag descriptors (the delegate target was extended for continuous channels first and primarily documents `stress_mean_sleep`).
- **Cross-reference**: Q3.3.h (outliers + calibration-drift) cross-references [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) (no per-column row for bb_lowest specifically; absorbed into UDS-passthrough collective rows) AND [`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md) as the load-bearing BB-family coverage-discipline MD.
- **Computed directly from `per_day_master.csv`**: Q3.3.b (Politis-White E[L]\*), Q3.3.c (per-phase base rates), Q3.3.d (phase-stratified medians + citalopram step + load-bearing afbouw-reversal cross-reference), Q3.3.e (near-identity check |rho|>=0.92 on 13-channel panel), Q3.3.f (crash-vs-normal Cohen's d + Mann-Whitney U + stationary-bootstrap CI at E[L]=7 and data-driven E[L]\* + crash-drop sensitivity per section 3.4), Q3.3.g (NADIR-is-spike-form discussion + BB-family pairwise correlations), Q3.3.i (covariate-sensitivity readiness for future HA pre-regs).
- **Channel-specific Q3.3.j + Q3.3.k extensions** per descriptive README section 3.3: Q3.3.j BB-source coverage (bb_lowest has full corpus coverage from 2021-08-16 -- 100% Stratum 4 minus UDS-side NaN gaps -- contrast with bb_overnight_gain ~37% of corpus); Q3.3.k relationship to bb_overnight_gain (HA10 primary; source-conditioned reads for bb_overnight_gain_best per bb_overnight_gain_proxy.md discipline rule 1).
- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) (`compute_data_driven_block_length`, `stationary_bootstrap_ci`).
- **Load-bearing cross-references** per handoff section 2.4: HA10 single-pool R14 re-anchor (badd04a) descriptively corroborated in Q3.3.d + Q3.3.f; recovery_arc v2 section 5.A afbouw-reversal reproduced + OPPOSITE-direction contrast with sister all_day_stress_avg afbouw-fully-recovers in Q3.3.d; recalibration -1.13/mg beta anchored in Q3.3.d; bb_overnight_gain_proxy.md coverage-bridge framing applied in Q3.3.h + Q3.3.j + Q3.3.k. NO substantive HA verdict promotion per CONVENTIONS section 2.1.
- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).

## Result

Headline (see [`findings.md`](findings.md) for the full answers Q3.3.a-k):

`bb_lowest` on Stratum 4 is a **daily-NADIR channel** (skew=+0.42, excess kurtosis=+0.45, heavy_tail_flag=False). **Data-driven E[L]\*=29.2** -- vs sister Strand-A channels stress_mean_sleep 12.6 / stress_low_motion 21.1 / all_day_stress_avg 29.8. **Phase-stratified medians track the recovery_arc v2 section 5.A trajectory faithfully**: unmedicated 18.0 -> buildup 26.0 -> consolidation 22.0 -> **afbouw 15.0** -- afbouw GOES LOWER than unmedicated baseline (the load-bearing recovery_arc v2 section 5.A reversal); **OPPOSITE-direction from sister all_day_stress_avg afbouw-fully-recovers (per Q3.2.d 34.0 = 34.0 unmed)**. Episode-level Cohen's d=-0.30; bootstrap CI95 [-5.45, +0.36]. Q3.3.j: bb_lowest full corpus coverage from 2021-08-17 onward (98.7% of corpus), contrast with bb_overnight_gain (33.8% of corpus). Q3.3.k: bb_lowest <-> bb_overnight_gain pair statistics in findings.md (source-conditioned per bb_overnight_gain_proxy.md discipline rule 1).

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + `README.md` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup covering Q3.3.a-k + tables (programmatically emitted by run.py from summary.json per the Q3.2 architectural note about the Write-tool harness heuristic on the literal filename "findings")
- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- 5 PNGs: distribution, phase-stratified violins, trajectory-with-phases, crash-vs-normal, ACF (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-24** (commit context: post-`cf34ab1` Q3.2 all_day_stress_avg LANDED; Phase 2 "finish the descriptive analysis" Tier 1 user-prioritised CONFIRMED-citalopram channel #3 of 3; R14 first at `badd04a`; Q3.2 second at `cf34ab1`; this Q3.3 third; `stress_stdev_sleep` closes Tier 1 next). Refresh when:

1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to spin up.
2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 onward).
3. Politis-White E[L]\* shifts by another factor of 2 from current 29.2.
4. HA-C4b BB-floor pre-reg unblocks per STOCKTAKE section 6 and triggers operationalisation-substrate consumption.
5. Per-minute BB primitive becomes available (currently not in GDPR dump per bb_overnight_gain_proxy.md section 6 caveat 5).
6. recovery_arc v3 refresh ships and updates the section 5.A afbouw-reversal characterisation.

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`)
- **First Strand A analysis** (template anchor): [`descriptive/operationalisation_support/stress_mean_sleep/`](../stress_mean_sleep/) -- sister CONFIRMED-citalopram channel; first Phase-1 Strand A analysis.
- **Second Strand A analysis** (Q3.2 most recent precedent): [`descriptive/operationalisation_support/all_day_stress_avg/`](../all_day_stress_avg/) -- sister CONFIRMED-citalopram channel; OPPOSITE-direction afbouw contrast surfaced in Q3.3.d.
- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/`](../single_pool_reanchor/) -- the HA10 row descriptively corroborated in Q3.3.d + Q3.3.f.
- **Recovery arc** (Strand B): [`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/) v2 LANDED 2026-06-22 (`8feae6a`); section 5.A afbouw-reversal load-bearing in Q3.3.d.
- **HA-* tests that this analysis anchors**:
  - HA10 (LOCKED OVERALL-REFUTED with R14 single-pool CONVERGE-ON-OVERALL); primary is bb_highest -- bb_lowest is the complementary floor primitive.
  - HA-P6 v3 (LOCKED `a980b1c` 2026-06-17); bb_lowest is 1 of 4/7 distinguishable channels.
  - HA-C4b (DEFERRED per STOCKTAKE section 6); natural consumer for HA-C4b BB-floor pre-reg.
- **Definitional substrate**: [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.6.1 (locked -1.134/mg dose-response; INVERSE direction).
- **Other methodology MDs**: `lc_phase_descriptive.md`, `citalopram_phase_stratification.md`, `permutation_null_block_length.md`, `bb_overnight_gain_proxy.md` (load-bearing), `garmin_indicators_audit.md`, `lc_era_temporal_segmentation.md`.
- **Existing complementary**: [`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) (Q3.3.e cross-reference; reciprocally confirms the rho=-0.749 bb_lowest <-> all_day_stress_avg pair from the all_day_stress_avg Q3.2.e side).
- **Upstream pipeline**: `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `daily_uds.csv` (Wave-3 JSON-side passthrough 2026-06-12 per `garmin_indicators_audit.md`). NO custom FIT extraction. `labels_crash_v2.csv` per locked `crash_v2-definition`.
