# `detrended_correlation/` -- Q4.5.b (methodological sanity check)

**Strand**: B (multi-year trajectory; descriptive sanity check). First-time-in-any-artefact closure of the canonical Q4.5.b scope per [`analyses/descriptive/README.md`](../../README.md) section 4.5.b.

## Research question

For each pair where both channels show a multi-year trajectory, how much of the raw Spearman rho is within-window co-variation vs shared trajectory? Do the rho values from Q3.9.e + Q4.9 method (c) survive trajectory detrend per CONVENTIONS section 3.7? Per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) section 4.5.b (LOCKED 2026-06-18 r3, commit `ccbd12e`).

## Method (user-LOCKED operationalisation; do NOT iterate per Strand B section 7c discipline)

- **Surface**: Stratum 4 primary (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05; n=1372 day-level rows).
- **7 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr + gevoelscore (Q4.9 6-channel set + outcome). 21 unique pairs (7-choose-2).
- **3 detrend methods + sensitivity**: (1) linear OLS (CONVENTIONS section 3.7 default), (2) rolling-median 90d, (3) per-recovery-phase residual (subtract phase mean per row).
- **Both full-corpus + per-recovery-phase granularity** per user-locked choice 3: full-corpus tells you about multi-year arc cancellation; per-phase tells you about within-phase drift cancellation.
- **Spurious-correlation flag threshold = |delta rho| >= 0.1** per CONVENTIONS section 3.7 + HA precedent.
- **Shared utilities**: [`_utils/frame.py`](../../../_utils/frame.py) (loaders; Stratum 4 filter). NO new statistical machinery; uses numpy + pandas (Spearman rho vendored inline; no scipy dep).
- **No causal claims; no falsification bar; not a claim that raw rho was wrong** per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + section 3.7 + section 4.1 + section 4.2.

## Result

Headline (see [`findings.md`](findings.md) for full per-pair + per-method tables + cross-references):

**Spurious-flag count**: 6 of 21 pairs flagged SPURIOUS_TRAJECTORY_DRIVEN in >=1 detrend method; remaining 15 pairs survive all 3 detrend methods (WITHIN-WINDOW-REAL).

**Per-method spurious counts**: linear OLS = 5; rolling-median 90d = 2; per-recovery-phase = 2 (of 21 pairs each).

**Long-memory channels** (E[L]* >= 21d: all_day_stress_avg / bb_lowest / stress_low_motion_min_count_S60_Mlow) are more likely to carry trajectory-driven rho; **short-memory channels** (E[L]* <= 10d: stress_stdev_sleep / resting_hr) less so. Pair-group rates: 4 of 15 long-memory-touching pairs flagged SPURIOUS; 1 of 1 short-memory-only pairs.

**Layer 1 descriptive sanity-check only**. NO causal claims. NO HA verdict promotion. **NOT a claim that raw rho was wrong** (detrend is a sensitivity arm per CONVENTIONS section 3.7). HA07d + HA-C3 v2 + HA-C3p + HA-P6 v3 + recovery_arc v2 + crash_v2-definition LOCKED references are descriptive context only.

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- 8-stage analysis script; outputs `summary.json` + `findings.md` + `README.md` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup covering Stages 2-6 + per-phase granularity tables + methodology sensitivity report + cross-references + limitations (programmatically emitted by run.py)
- [`summary.json`](summary.json) -- machine-readable per-stage results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- 3 PNGs: rho matrix side-by-side, per-method spurious-flag count, sensitivity scatter (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-05 corpus + 2026-06-25 analysis**. Closes Q4.5.b (descriptive README sec 4.5.b r2 closure D3.4; previously had no home in any artefact). **Tier 3 Core 5 4th of 5 LANDED** (Q4.9 + Q4.6 + Q4.3 + this Q4.5.b; remaining Q4.4 cohort topology + Q4.2 intervention cross-channel).

Refresh when:
1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg using a pair from this 7-channel set as primary is about to spin up.
2. lc_recovery_phase_axis is amended (e.g. phase 6 post_afbouw added when corpus first acquires post-2026-06-05 data).
3. CONVENTIONS section 3.7 trajectory-detrend discipline is amended.

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`); section 4.5.b 'Detrended-companion correlation ''(spurious-correlation flag)' (r2 closure D3.4) -- this analysis closes it.
- **Q3.9.e Strand-A first-pass**: [`descriptive/operationalisation_support/gevoelscore/findings.md`](../../operationalisation_support/gevoelscore/findings.md) section 3.9.e -- linear-rank Spearman rho on the full Stratum-4 pool; REPRODUCED in this Q4.5.b Stage 2 as verification check.
- **Q4.9 method (c) rolling-Spearman precedent**: [`descriptive/trajectory/subjective_objective_coupling/findings.md`](../subjective_objective_coupling/findings.md) section 4 -- complementary view (rolling rho over time) vs Q4.5.b's full-pool-rho-on-detrended-residuals view.
- **Q4.3 era_boundaries**: [`descriptive/trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) -- rp5 citalopram-start strongest-boundary finding contextualises why per-recovery-phase detrend can preserve content that linear OLS cancels.
- **Q4.6 coverage_overview**: [`descriptive/trajectory/coverage_overview/findings.md`](../coverage_overview/findings.md) -- channel coverage; bb_lowest used in place of bb_overnight_gain for full Stratum-4 coverage.
- **HA07d both-eras-SUPPORTED**: [`analyses/hypotheses/HA07d-sleep-stress-variability/result.md`](../../../hypotheses/HA07d-sleep-stress-variability/result.md) (LOCKED) -- stress_stdev_sleep channel; short-memory makes the gevoelscore x stress_stdev_sleep pair the cleanest within-window-real test.
- **Methodology MDs**: [`CONVENTIONS section 3.7`](../../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) + [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) + [`permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) + [`lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md).
- **Upstream pipeline**: `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py`.

## Discipline guards (per CONVENTIONS)

- **section 2.1 descriptive-before-inference**: NO causal claims; NO falsification bar; NO HA verdict promotion. The LOCKED HA references (HA07d, HA-C3 v2, HA-C3p, HA-P6 v3, recovery_arc v2, crash_v2-definition) are descriptive context only; NONE are extended.
- **section 3.7 trajectory-detrend discipline**: |delta rho| >= 0.1 threshold inherits the HA precedent; detrend is a sensitivity arm, NOT a correction; **not a claim that raw rho was wrong**.
- **section 3.6 named counts**: every n in findings.md tables names scheme (Stratum 4 day-level rows) + unit (pair-wise non-NaN) + source (per_day_master.csv).
- **section 4.1 + section 4.2**: descriptive framing only; observations land as 'rho_raw = X, rho_detrended = Y, |delta| = Z, flag = SPURIOUS/WITHIN-WINDOW-REAL'; NO a-priori claims; NO mechanism interpretation.
- **section 4.5.b (descriptive README)**: this analysis closes the canonical Q4.5.b scope for the first time in any artefact per the LOCKED programme spec.
