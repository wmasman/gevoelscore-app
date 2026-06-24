# `all_day_stress_avg` -- operationalisation-support descriptive analysis

**Strand**: A (operationalisation support; template-driven; no operationalisation interview required per [`descriptive/README.md`](../../README.md) section 7b).

## Research question

Operationalisation-support descriptive characterisation of `all_day_stress_avg` on Stratum 4, answering Q3.2.a-i per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.2 (LOCKED 2026-06-18 r3, commit `ccbd12e`). Phase 2 "finish the descriptive analysis" Tier 1 user-prioritised sequential batch; **second of the 3 CONFIRMED-citalopram channels** (R14 `single_pool_reanchor` landed first at `badd04a`; `bb_lowest` next). This channel is the **CONFIRMED-citalopram channel with the largest beta** (+0.565/mg p=0.000 buildup post-CPAP per [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.6.1; sister stress_mean_sleep +0.43/mg; bb_lowest -1.13/mg inverse direction); **primary predictor in the HA-C3 v2 REJECTED + HA-C3p PARTIAL cluster** (2026-06-23) which jointly detected an inverted-U / concave non-linearity on this channel; also present in HA-P6 v3's 7-channel distinguishable-channel set.

## Method

- **Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05; n=1359 channel-valid days out of 1372 S4 days).
- **Primary phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with the stress_mean_sleep first analysis.
- **Delegate**: Q3.2.a (distribution shape) **partial delegate** to [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) + **extend** with full skewness/kurtosis/heavy-tail-flag descriptors (the delegate target was extended for continuous channels first and primarily documents `stress_mean_sleep`).
- **Cross-reference**: Q3.2.h (outliers + calibration-drift) cross-references [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md); **the audit MD does NOT yet have a per-column row for the all-day stress family** (proposed row content surfaced in findings.md Q3.2.h; PROPOSE-ONLY per handoff section 3).
- **Computed directly from `per_day_master.csv`**: Q3.2.b (Politis-White E[L]\*), Q3.2.c (per-phase base rates + HA-C3p quintile-bin reproduction), Q3.2.d (phase-stratified medians + citalopram step magnitude vs +0.565/mg recalibration anchor), Q3.2.e (near-identity check |rho|>=0.92), Q3.2.f (crash-vs-normal Cohen's d + Mann-Whitney U + stationary-bootstrap CI at E[L]=7 and E[L]\*~30 + crash-drop sensitivity per section 3.4), Q3.2.g (spike-primitive availability + continuous-vs-spike pair with `stress_low_motion_min_count_S60_Mlow`), Q3.2.i (covariate-sensitivity readiness for future HA pre-regs).
- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) (`compute_data_driven_block_length`, `stationary_bootstrap_ci`).
- **HA-C3 cluster cross-references** (load-bearing per handoff section 2.4): findings.md descriptively reproduces HA-C3p's right-shift unmedicated bin observation (Q3.2.c); descriptively corroborates the HA-C3 cluster's inverted-U finding via predictor-side mass-distribution observation (Q3.2.d); anchors phase-stratified discussion on the locked +0.565/mg recalibration anchor (Q3.2.d); contextualises this channel's E[L]\* against sister Phase-1 channels (Q3.2.b). NO substantive HA verdict promotion per CONVENTIONS section 2.1.
- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).

## Result

Headline (see [`findings.md`](findings.md) for the full answers Q3.2.a-i):

`all_day_stress_avg` on Stratum 4 is a **mildly right-skewed, autocorrelation-DENSE 24h-window daily-mean channel** (skew=+0.87, excess kurtosis=+1.99; **NOT heavy-tail-flag-triggering** unlike sister `stress_mean_sleep`). **Data-driven E[L]\*=29.8** -- factor-of-4 above project default; **the LONGEST E[L]\* yet observed in Strand A** (vs `stress_mean_sleep` 12.6 / `stress_low_motion_min_count_S60_Mlow` 21.1). **Phase-stratified medians shift sharply at the citalopram boundary** (34.0 unmedicated to 28.5 buildup; ~-5.5 median; ~-1.8 buildup-MAD) and **recover fully during afbouw** (34.0 afbouw = 34.0 unmedicated). Day-resolved citalopram-boundary step (2024-04-09 pre/post 30d) is -7.2 stress units. Crash-vs-normal: episode-level d=+0.37 with bootstrap CI **brushing zero** [-0.40, +4.71] -- WEAK episode-level signal; day-level Mann-Whitney U fires robustly (z=+4.30, p<0.0001). **Zero near-identity pairs** at |rho|>=0.92; closest is `awake_stress_avg` rho=+0.887 (just below). **The HA-C3p right-shift unmedicated bin observation is REPRODUCED EXACTLY** at the locked quintile boundaries (unmed counts [45, 80, 129, 138, 189] n=581); the unmedicated stratum carries 1.45x the full-pool share of Q5 mass (3.5x the full-pool share of Q1 mass) -- an extension of the HA-C3p descriptive observation to a share-ratio quantification. The `garmin_indicators_audit.md` per-column row for the all-day stress family is **missing** -- proposed row content surfaced in findings.md Q3.2.h for separate user authorisation.

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `findings.md` + `README.md` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup covering Q3.2.a-i + tables (programmatically emitted by run.py from summary.json)
- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- 5 PNGs: distribution, phase-stratified violins (citalopram axis), trajectory-with-phases, crash-vs-normal, ACF (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-24** (commit context: post-`ccbd12e` descriptive programme lock; Phase 2 "finish the descriptive analysis" Tier 1 user-prioritised CONFIRMED-citalopram channel #2; R14 `single_pool_reanchor` landed first at `badd04a`; `bb_lowest` next). Refresh when:

1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to spin up.
2. A new citalopram-phase boundary lands (e.g. post-afbouw enters analytic scope as of 2026-06-06 onward).
3. The Politis-White E[L]\* shifts by another factor of 2 from current 29.8 (factor-of-4-vs-default flag already fired).
4. The `all_day_stress_avg <-> bb_lowest` near-miss pair (Q3.2.e rho=-0.75) gets propagated into the cross-channel-correlation card's 7-channel panel.
5. The `garmin_indicators_audit.md` per-column row for the all-day stress family gets added with the proposed content (Q3.2.h flag).
6. An HA-C3 v3 / HA-C3p v2 alternative-shape pre-reg spins up and surfaces new operationalisation choices on this channel that would change the per-channel descriptive substrate.

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`)
- **First Strand A analysis** (template anchor): [`descriptive/operationalisation_support/stress_mean_sleep/`](../stress_mean_sleep/) -- this analysis adapts the same Q-template to a 24h-window mean continuous channel; cross-analysis comparison anchors throughout findings.md.
- **Third Strand A analysis** (count-primitive spike companion): [`descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/`](../stress_low_motion_min_count_S60_Mlow/) -- reciprocally named spike-form companion per CONVENTIONS section 3.5; cross-pair r=+0.85 / rho=+0.86.
- **Recovery arc** (Strand B): [`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/) v2 LANDED 2026-06-22 (`8feae6a`); the afbouw-reversal finding cross-references this analysis's Q3.2.c + Q3.2.d afbouw-recovery observation.
- **HA-* tests that this analysis anchors**:
  - HA-C3 v2 (primary user; REJECTED at `a2b18ba` 2026-06-23, wrong-direction override);   descriptive substrate upstream of any HA-C3 v3 redraft.
  - HA-C3p (sister; PARTIAL at `e5a63fe` 2026-06-23); right-shift section 2 observation   reproduced + extended in Q3.2.c.
  - HA-P6 v3 (descriptive Layer 1); includes this channel in 7-channel distinguishable set.
  - HA-C4 v2 (REJECTED at `52bddb5` 2026-06-18); this channel was Ch1 of the daily-aggregate   triad; the weak episode-level signal observation here constrains the post-rejection re-  interpretation.
- **Definitional substrate**: [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.6.1 (locked +0.565/mg dose-response).
- **Other methodology MDs**: `lc_phase_descriptive.md`, `citalopram_phase_stratification.md`, `permutation_null_block_length.md`, `garmin_indicators_audit.md`, `lc_era_temporal_segmentation.md`.
- **Existing complementary**: [`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) (Q3.2.e cross-reference; one new near-miss pair `all_day_stress_avg <-> bb_lowest` rho=-0.75 surfaced for next refresh).
- **Upstream pipeline**: `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `daily_uds.csv` (Wave-3 JSON-side passthrough 2026-06-12 per `garmin_indicators_audit.md`). NO custom FIT extraction. `labels_crash_v2.csv` per locked `crash_v2-definition`.
