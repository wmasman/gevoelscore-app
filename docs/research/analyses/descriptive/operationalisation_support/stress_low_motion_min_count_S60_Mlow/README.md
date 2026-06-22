# `stress_low_motion_min_count_S60_Mlow` -- operationalisation-support descriptive analysis

**Strand**: A (operationalisation support; template-driven; no operationalisation interview required per [`descriptive/README.md`](../../README.md) section 7b).

## Research question

Operationalisation-support descriptive characterisation of `stress_low_motion_min_count_S60_Mlow` on Stratum 4, answering Q3.x.a-i per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) section 3.1 template (LOCKED 2026-06-18 r3, commit `ccbd12e`) generalised to this channel per section 6.3 (r2 closure D1.8 two-gaps-one-analysis). Phase 1 third analysis under the locked programme; the channel is the **primary spike-counting primitive** for HA-C4b v2 (consumer of the "elevated stress while at rest" construct per [`methodology/stress_low_motion_primitive.md`](../../../methodology/stress_low_motion_primitive.md) Session E lock 2026-06-15) AND simultaneously covers the audit-surfaced D1.8 spike-primitive-coverage gap (per CONVENTIONS section 3.5) and D5.3 HA-pre-reg covariate-sensitivity-readiness gap in one analysis.

## Method

- **Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05; n=1365 channel-valid days out of 1372 S4 days).
- **Primary phase axis**: four-phase citalopram traject per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 (unmedicated / buildup / consolidation / afbouw) -- parity with the stress_mean_sleep first analysis.
- **Secondary phase axis**: 6-phase recovery axis per [`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) (LOCKED 2026-06-19 `d47e0d3`) -- cross-tabulated for additional context per the r3 default-for-descriptive-work guidance.
- **Delegate**: Q3.x.a (distribution shape) **partial delegate** to [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) + **extend** with count-primitive-specific descriptors (zero-rate, dispersion ratio, monotonicity sanity) -- the delegate target was extended for continuous channels first and does not cover count primitives.
- **Cross-reference**: Q3.x.h (outliers + calibration-drift) cross-references [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md); **the audit MD does NOT yet have a row for this primitive family** (proposed row content surfaced in findings.md; PROPOSE-ONLY per handoff section 6).
- **Computed directly from `per_day_master.csv`**: Q3.x.b (Politis-White E[L]\*), Q3.x.c (per-phase base rates + zero-rate), Q3.x.d (phase-stratified medians + count-primitive citalopram caveat), Q3.x.e (near-identity check |rho|>=0.92 across 8 sibling sensitivity-ladder columns + 2 respiration companions + 6 continuous cousins), Q3.x.f (crash-vs-normal Cohen's d + median diff + Mann-Whitney U robustness + stationary-bootstrap CI at E[L]=7 and E[L]=21 + crash-drop sensitivity per section 3.4), Q3.x.g (spike-primitive availability -- this channel IS the spike primitive per CONVENTIONS section 3.5 + monotonicity validation), Q3.x.i (covariate-sensitivity readiness for future HA pre-regs).
- **Shared utilities**: [`_utils/frame.py`](../../../analyses/_utils/frame.py) (loaders, Stratum 4 filter, crash-drop sensitivity) + [`_utils/inference.py`](../../../analyses/_utils/inference.py) (`compute_data_driven_block_length`, `stationary_bootstrap_ci`).
- **Count-primitive adaptations** vs continuous-channel first analysis (stress_mean_sleep): zero-rate per phase in Q3.x.c; Mann-Whitney U + median diff alongside Cohen's d in Q3.x.f; sibling-sensitivity-ladder peers in Q3.x.e (highly correlated by construction; the diagnostic is whether the primary carries information beyond a neighbour); "the channel IS the spike primitive" framing in Q3.x.g; modelling-class guidance for negative-binomial / log-linear OLS over Poisson in Q3.x.a + Q3.x.i.
- **No causal claims, no falsification bar** per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference).

## Result

Headline (see [`findings.md`](findings.md) for the full answers Q3.x.a-i):

`stress_low_motion_min_count_S60_Mlow` on Stratum 4 is a **right-skewed, autocorrelation-dense per-day count primitive** (skew=+1.40, excess kurtosis=+3.02; **data-driven E[L]\*=21.1 -- factor-of-3 above project default E[L]=7 and ~1.7x above stress_mean_sleep's E[L]\*=12.6**, flag fires per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md)). **Zero-inflation does NOT materialise** (zero-rate = 1.0%, n=14/1365); the channel is a heavy-tailed positive count with median 55 min/day. **The phase-stratified medians drop sharply at the citalopram boundary** (unmedicated 77 to buildup 35 min/day; delta=-42, ~-1.3 MAD) -- opposite-direction to a naive raw-stress-threshold-shift reading; the operationalisation-support implication is that any HA cross-phase MUST adopt section 5.A phase-stratification (section 5.B numerical dose-adjustment doesn't apply because no per-mg slope is locked on the count primitive). Crash-vs-normal: episode-level Cohen's d=+0.38 (smaller than stress_mean_sleep's +0.91) BUT day-level Mann-Whitney U fires robustly (z=+4.65, p<0.0001, P(crash>normal)=0.638). **Seven of eight sibling sensitivity-ladder columns flag as near-identity** (expected by construction); the `Mbelow_mod` == `Mlow` collapse is total (rho=+1.000) -- the effective ladder is 6 distinct primitives at v1, not 9. The continuous-form cousin `all_day_stress_avg` correlates at r=+0.85 (NOT near-identity but high enough to require care in any consumer HA). The `garmin_indicators_audit.md` row for this primitive family is **missing** -- proposed row content surfaced in findings.md Q3.x.h for separate user authorisation.

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- descriptive computation; outputs `summary.json` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup covering Q3.x.a-i + figures/tables
- [`summary.json`](summary.json) -- machine-readable per-question results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- 7 PNGs: distribution, phase-stratified violins (citalopram + 6-phase recovery), trajectory-with-phases, crash-vs-normal, ACF, sibling-ladder correlation heatmap (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-22** (commit context: post-`ccbd12e` descriptive programme lock; Phase 1 third analysis; landed alongside the bout-level methodology lock cascade `c57ff3f`). Refresh when:

1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to spin up.
2. A new citalopram-phase boundary lands (e.g. post-afbouw enters analytic scope as of 2026-06-06 onward).
3. The Politis-White E[L]\* shifts by another factor of 2 from current 21.1 (factor-of-3-vs-default flag already fired).
4. The `all_day_stress_avg` and `awake_stress_avg` near-miss pairs (Q3.x.e r=+0.85 / r=+0.82) get propagated into the cross-channel-correlation card's 7-channel panel.
5. The HA-C4 v2 bout-level reframing (per `bout_level_recovery_dynamics.md` `c57ff3f` future consumers) spins up and surfaces sub-day operationalisation findings.
6. The `garmin_indicators_audit.md` row gets added with the proposed content (Q3.x.h flag).

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`)
- **First Strand A analysis** (template anchor): [`descriptive/operationalisation_support/stress_mean_sleep/`](../stress_mean_sleep/) -- this analysis adapts the same Q-template to a count primitive; cross-analysis comparison anchors throughout findings.md.
- **Second Strand B analysis** (recovery_arc): [`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/) -- the cross-test pairing that includes this primitive in the 7-channel HA-P6 set; the recovery_arc found this channel survives 90d detrend on the LC trajectory.
- **HA-* tests that this analysis anchors**:
  - HA-C4b v2 (primary user); v3 NOT-SUPPORTED at v3-result; descriptive substrate upstream of vNext reframing.
  - HA-C4 v2 (REJECTED at `52bddb5` 2026-06-18); secondary user before rejection; descriptive substrate supports the post-rejection re-interpretation conversation.
  - HA-C4b vNext / HA-C4c (likely future consumers per `bout_level_recovery_dynamics.md` `c57ff3f`).
  - HA11 (shares FIT-source + 600-sample day-validity gate).
- **Definitional substrate**: [`methodology/stress_low_motion_primitive.md`](../../../methodology/stress_low_motion_primitive.md) (Session E lock 2026-06-15).
- **Other methodology MDs**: `lc_phase_descriptive.md`, `citalopram_phase_stratification.md`, `citalopram_dose_response_stress_mean_sleep.md`, `permutation_null_block_length.md`, `garmin_indicators_audit.md`, `lc_era_temporal_segmentation.md`, `lc_recovery_phase_axis.md`, `bout_level_recovery_dynamics.md`.
- **Existing complementary**: [`garmin_exploration/stress_low_motion_viz/`](../../../analyses/garmin_exploration/stress_low_motion_viz/) (per_phase_descriptive.py + Family A/B/C/D within-day exemplar plots) + [`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) (Q3.x.e cross-reference; two new near-miss pairs surfaced for next refresh).
- **Upstream pipeline**: `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `processed/garmin/stress_low_motion_minutes.csv` <- `pipeline/01_extract/stress_low_motion_extract.py` per `stress_low_motion_primitive.md` section 6. `labels_crash_v2.csv` per locked `crash_v2-definition`.
