# `subjective_objective_coupling/` -- Q4.9 (THE CENTRAL PROJECT QUESTION)

**Strand**: B (multi-year trajectory; descriptive). First-time-in-any-artefact closure of the canonical Q4.9 scope per [`analyses/descriptive/README.md`](../../README.md) section 4.9.

## Research question

When does `gevoelscore` align with the 6 CONFIRMED + non-CONFIRMED Garmin channels vs diverge? On a crash day, what does the body-state profile combining gevoelscore + cross-channel Garmin patterns look like? Are there pre-crash divergence patterns where Garmin signals one thing and gevoelscore another? Per the locked descriptive programme spec at [`docs/research/analyses/descriptive/README.md`](../../README.md) section 4.9 (LOCKED 2026-06-18 r3, commit `ccbd12e`).

## Method (user-LOCKED operationalisation; do NOT iterate per Strand B section 7c discipline)

- **Surface**: Stratum 4 primary (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05; n=1372 day-level rows; n=29 crash episodes per crash_v2-definition).
- **6 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr (3 CONFIRMED-citalopram + 3 not).
- **3 coupling methods**: (a) z-sign agreement on 28d-lagged baseline + (b) quintile-bin agreement + (c) rolling 28d Spearman rho + low-rho epoch flag.
- **Pre-crash matched control** per HA-P6 v3 Arm-A REUSE: 29 crash episodes paired with non-crash matched controls (tolerance ladder [+-1.0, +-1.5, +-2.0]; phase-match; 4d pre-crash lead-up window).
- **Pooled primary + per-citalopram-phase sensitivity arm** per [`phase_axis_collapsibility_conventions §6`](../../../../methodology/phase_axis_collapsibility_conventions.md) binding on 3 CONFIRMED-citalopram channels.
- **Shared utilities**: [`_utils/frame.py`](../../../_utils/frame.py) (loaders; Stratum 4 filter); per-channel z-score with 28d-lagged trailing window + robust median + MAD x 1.4826 per CONVENTIONS section 3.1.
- **No causal claims; no falsification bar** per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + section 4.1 + section 4.2.

## Result

Headline (see [`findings.md`](findings.md) for full per-channel + per-phase tables + per-crash episode roster + cross-references):

**Method (a) z-sign agreement** rates range 32% to 41% across 6 channels (pooled Stratum 4).
**Method (b) quintile-bin coupling** (bin diff <=1) rates range 57% to 63% across 6 channels.
**Method (c) rolling 28d Spearman**: low-rho epoch rates (|rho|<0.1) range 25% to 37% across 6 channels; per-phase distribution in findings.md section 4.
**Episode-level matched pre-crash body-state profile**: 28/29 crash episodes paired with HA-P6 v3 Arm-A matched controls; 4d pre-crash lead-up 6-channel z-score profile in findings.md section 5 + heatmap plots.
**Phase sensitivity arm**: per-citalopram-phase reads of all 3 methods in findings.md section 6; recovery_arc v2 section 5.A afbouw-reversal direction REPRODUCED descriptively at the per-channel coupling-rate resolution.

**Layer 1 descriptive only**. NO causal claims. NO HA verdict promotion. HA-C3 v2 + HA-C3p inverted-U + HA-P6 v3 Arm-A + crash_v2-definition + recovery_arc v2 LOCKED references are descriptive corroboration only.

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- 8-stage analysis script; outputs `summary.json` + `findings.md` + `README.md` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup covering methods (a) + (b) + (c) + pre-crash matched-control profile + phase sensitivity arm + cross-references + limitations (programmatically emitted by run.py per the Q3.5-Q3.9 Strand-A architectural note about the Write-tool harness heuristic on the literal filename 'findings')
- [`summary.json`](summary.json) -- machine-readable per-stage results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- 3 PNGs: cross-method coupling rates, per-crash body-state profile heatmap, pre-crash divergence heatmap (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-05 corpus + 2026-06-25 analysis**. Closes Q4.9 (THE central project question; previously had no home in any artefact per descriptive README section 4.9). **Tier 3 Strand B 1st of 8 LANDED** (Q4.2 + Q4.3 + Q4.4 + Q4.5.b + Q4.6 + Q4.7 + Q4.8 deferred per the Phase 2 batch sequencing; each requires user operationalisation interview per Strand B section 7c).

Refresh when:
1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg using gevoelscore + a Garmin channel pair is about to spin up beyond the HA-C3 v2 / HA-P6 v3 LOCKED operands.
2. A new crash episode lands (currently n=29; next refresh trigger N_crashes >= 30).
3. crash_v2-definition is revised (current state: LOCKED; revision would warrant a Q4.9 refresh).
4. HA-P6 v3 Arm-A matched-control machinery is amended (current state: LOCKED at HA-P6 v3 hypothesis.md).
5. recovery_arc v2 afbouw-reversal narrative is updated (current state: LOCKED at recovery_arc v2 findings.md).

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`); section 4.9 'Subjective <-> objective coupling + crash-day body-state profile' -- THE central project question; this analysis closes it.
- **Strand-A first-pass at Q4.9**: [`descriptive/operationalisation_support/gevoelscore/findings.md`](../../operationalisation_support/gevoelscore/findings.md) section 3.9.e -- linear-rank Spearman rho on the full Stratum-4 pool; REPRODUCED + EXTENDED in this Q4.9 method (c).
- **HA-C3 v2 (LOCKED REJECTED) + HA-C3p (LOCKED PARTIAL 2-of-3)**: [`HA-C3/result.md`](../../../hypotheses/HA-C3/result.md) + [`HA-C3p/result.md`](../../../hypotheses/HA-C3p/result.md) -- joint inverted-U finding (stress -> felt-state concave with peak around stress 30-40) descriptively CONTEXTUALISES method (a)'s divergence-at-extremes vs divergence-at-middle split.
- **HA-P6 v3 hypothesis.md section 4.4** (Arm-A matched-control machinery; LOCKED): [`HA-P6/hypothesis.md`](../../../hypotheses/HA-P6/hypothesis.md) -- REUSED descriptively in section 5 pre-crash body-state profile.
- **crash_v2-definition** (LOCKED): [`crash_v2-definition/definition.md`](../../../hypotheses/crash_v2-definition/definition.md) -- canonical 29 crash episodes.
- **recovery_arc v2 section 5.A** (LOCKED): [`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) -- afbouw-reversal on 3 CONFIRMED-citalopram channels REPRODUCED descriptively at per-channel coupling-rate resolution in section 6 phase sensitivity arm.
- **R14 single-pool re-anchor**: [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../../operationalisation_support/single_pool_reanchor/findings.md) -- HA verdicts on these channels (HA10, HA-C3, HA-C4b, HA07d, HA11) for cross-context.
- **Methodology MDs**: [`citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) + [`phase_axis_collapsibility_conventions.md`](../../../../methodology/phase_axis_collapsibility_conventions.md) + [`permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) + [`lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md).
- **Upstream pipeline**: `per_day_master.csv` (6 channel columns + gevoelscore + dose_plasma_mg + recovery_phase) <- `pipeline/03_consolidate/build_unified_dataset.py`; `labels_crash_v2.csv` <- `crash_v2-definition/definition.md`.

## Discipline guards (per CONVENTIONS)

- **section 2.1 descriptive-before-inference**: NO causal claims; NO falsification bar; NO HA verdict promotion. The LOCKED HA references (HA-C3 v2, HA-C3p, HA-P6 v3, recovery_arc v2, crash_v2-definition, R14 single_pool_reanchor) are descriptive corroboration only; NONE are extended.
- **section 3.1 personal baseline**: 28d-lagged trailing window with robust median + MAD x 1.4826 for per-channel z-scores.
- **section 3.4 crash-drop sensitivity**: dispatched by construction in section 5 (matched controls ARE non-crash episodes; the sensitivity hook does not apply at the episode-centred level).
- **section 3.6 named counts**: every n in findings.md tables names scheme + unit + source.
- **section 4.1 + section 4.2**: descriptive framing only; observations reported as 'rate X%, divergence concentrates Z way, profile shows W pattern'; NO a-priori claims; NO mechanism interpretation.
- **section 4.9 (descriptive README)**: this analysis closes the canonical Q4.9 scope for the first time in any artefact per the LOCKED programme spec.
