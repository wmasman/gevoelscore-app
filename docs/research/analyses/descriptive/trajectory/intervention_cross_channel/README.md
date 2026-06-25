# `trajectory/intervention_cross_channel/` -- README

**Strand B (multi-year trajectory) descriptive analysis** -- integrated cross-channel timing + transition picture of the citalopram effect across 6 channels. Closes Q4.2 per [`descriptive/README.md`](../../README.md) sec 4.2 + closes the user-prioritised 'finish the descriptive analysis' Phase 2 batch (Tier 3 Core 5 = Q4.9 + Q4.6 + Q4.3 + Q4.5.b + Q4.4 + Q4.2).

## Research question

Per descriptive README sec 4.2: 'What's the integrated picture of the citalopram effect across all 6 candidate channels? Where does the SSRI signal land first (stress vs BB vs RHR vs respiration)? Is there a timing relationship?'

**Honest framing per handoff sec 3.4 + CONVENTIONS sec 4.2 caveat-class**: cross-channel timing ladder is DESCRIPTIVE observation ('channel X has earlier onset under Method (a) than channel Y'); NOT causal ('SSRI hits channel X first'). Non-CONFIRMED channels (stress_stdev_sleep + stress_low_motion + resting_hr) are NOT promoted to CONFIRMED-citalopram candidacy -- v3-extension territory is OUT-OF-SCOPE here.

## User-LOCKED operationalisation (per Strand B sec 7c interview 2026-06-25; do NOT iterate)

1. **6 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest (CONFIRMED-citalopram v3) + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr (non-CONFIRMED; descriptive only).
2. **ALL 3 timing-onset methods + sensitivity**: threshold-cross + PELT/binseg first-CP + time-to-half-effect.
3. **Buildup-transition + afbouw-reversal** (2024-04-09 + 2026-03-20).
4. **ALL 3 visualisations**: per-channel timeline + heatmap + cross-channel timing ladder (+ method-sensitivity comparison).

## Method (8-stage architecture per handoff sec 3.2)

- **Stage 1 (data prep)**: load per_day_master; restrict to 6 channels + gevoelscore + recovery_phase + dose_plasma_mg + derived citalopram_phase. Compute (i) `_z_pre` z-score vs pre-citalopram pool's robust median + MAD; (ii) `_z_28d` 28d-trailing-window robust z (lag=1; CONVENTIONS sec 3.1).
- **Stage 2 (Method (a) threshold-cross)**: per channel, find first day post-2024-04-09 where |z_pre| >= 1.0 sustained >= 7 consecutive day-rows; CONFIRMED channels require run-direction match the v3 prior.
- **Stage 3 (Method (b) PELT/binseg first-CP)**: per channel, binary segmentation on 14d-rolling median of post-2024-04-09 z_pre series; min-segment 14d; max-depth 8; reduction-threshold 5%; first change-point date reported.
- **Stage 4 (Method (c) time-to-half-effect)**: per channel, exponential decay z(t) = z_inf * (1 - exp(-t/tau)) fit on 180d post-window; half-effect-days = tau * ln(2); descriptive SSRI-kinetics PROXY only.
- **Stage 5 (per-phase transition analysis)**: buildup-transition Delta z_pre (+-30d windows) + afbouw-reversal phase-pool medians + Pattern 2 direction labels per STOCKTAKE sec 6.
- **Stage 6 (cross-channel timing ladder)**: per-method ranking + method-sensitivity (channels stable vs disagreeing across all 3 methods) + consensus ordering.
- **Stage 7 (4 visualisations)**: per-channel timeline aligned at t0 + heatmap (channel x time x z) + cross-channel timing ladder + method-sensitivity rank scatter.
- **Stage 8 (programmatic emit)**: findings.md + README.md.

## Headline (descriptive only; NO causal claims; NO HA verdict promotion; NO mechanism interpretation; NO promotion of non-CONFIRMED channels)

**Cross-channel timing ladder (consensus across 3 methods)**:

- 1. `all_day_stress_avg` (mean rank 1.67)
- 2. `bb_lowest` (mean rank 2.33)
- 3. `resting_hr` (mean rank 3.67)
- 4. `stress_mean_sleep` (mean rank 4.33)
- 5. `stress_low_motion_min_count_S60_Mlow` (mean rank 5.33)
- 6. `stress_stdev_sleep` (mean rank 5.67)

**Method-sensitivity**: 1 of 6 channels are STABLE across all 3 methods; 5 DISAGREE on at least one method-pair.

**Afbouw-reversal Pattern 2 reproduction**:

- `stress_mean_sleep`: reversal-below (afbouw crosses baseline in opposite direction)
- `all_day_stress_avg`: full-recovery (afbouw returns to unmedicated baseline)
- `bb_lowest`: reversal-below (afbouw crosses baseline in opposite direction)
- `stress_stdev_sleep`: shift-below-baseline
- `stress_low_motion_min_count_S60_Mlow`: shift-below-baseline
- `resting_hr`: rise-above-baseline (afbouw shift exceeds unmedicated)

Full per-method onset tables + per-channel buildup + afbouw Delta-z tables in [`findings.md`](findings.md); machine-readable data in `summary.json` (gitignored).

## Files

- [`README.md`](README.md) -- this file
- [`run.py`](run.py) -- 8-stage analysis script; emits `summary.json` + `findings.md` + `README.md` + `plots/*.png`
- [`findings.md`](findings.md) -- writeup of all 8 stages with cross-references + limitations (programmatic emit per the Write-tool harness heuristic on the literal filename 'findings')
- [`summary.json`](summary.json) -- machine-readable per-stage results (gitignored per `docs/research/**/*.json`)
- [`plots/`](plots/) -- 4 PNGs: per-channel timeline + heatmap + timing ladder + method-sensitivity (gitignored per `docs/research/**/*.png`)

## Status

**Current as of 2026-06-04 corpus + 2026-06-25 analysis**. Closes Q4.2 (integrated cross-channel picture; previously deferred per descriptive README sec 4.2). **CLOSES TIER 3 CORE 5** (Q4.9 + Q4.6 + Q4.3 + Q4.5.b + Q4.4 + Q4.2 = 6 Strand B trajectory analyses). **CLOSES Phase 2 user-prioritised 'finish the descriptive analysis' batch** (16 analyses total since 2026-06-18 programme bootstrap). Foundation for research-interpret skill pivot at user's call.

Refresh when:
1. A new boundary lands (e.g. post_afbouw boundary 2026-06-06 becomes in-corpus).
2. A new methodology MD revises the citalopram-phase boundary dates.
3. The v3 sweep is extended (CONFIRMED/REJECTED set changes); the 6-channel scope may need refresh.
4. The Pattern 2 direction-label classification rule is revised per future cross-channel descriptive work.

## Cross-references

- **Programme spec** (parent): [`descriptive/README.md`](../../README.md) (LOCKED r3 2026-06-18, commit `ccbd12e`); sec 4.2 'Intervention cross-channel view (the citalopram integrated picture)' -- this analysis closes it.
- **`citalopram_dose_response_stress_mean_sleep.md` sec 5.6** (LOAD-BEARING; v3 sweep): [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) -- CONFIRMED 3 / REJECTED 1; NOT extended.
- **`recovery_arc v2` sec 5.A afbouw-reversal**: [`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) -- per-phase CONFIRMED-citalopram trajectory + afbouw-reversal LOCKED verdict; descriptively reproduced + extended in Stage 5.
- **STOCKTAKE sec 6 Pattern 2**: [`STOCKTAKE.md`](../../../../STOCKTAKE.md) -- 6-channel afbouw direction split; closed with timing in Stage 5.
- **Q4.3 era_boundaries rp5**: [`trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) -- 2024-04-09 strongest distribution-shift boundary; cross-referenced.
- **Q4.4 cohort_topology rp5/cp3 event-rate decoupling**: [`trajectory/cohort_topology/findings.md`](../cohort_topology/findings.md) -- honest framing that Q4.2 is on channel distributions NOT event rates.
- **Q4.5.b detrended_correlation resting_hr trajectory-driven**: [`trajectory/detrended_correlation/findings.md`](../detrended_correlation/findings.md) -- resting_hr caveat (timing-onset may partly reflect multi-year arc artefact).
- **Methodology MDs**: [`citalopram_dose_response_stress_mean_sleep.md`](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) + [`intervention_effects_descriptive.md`](../../../../methodology/intervention_effects_descriptive.md) + [`citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) + [`permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) + [`CONVENTIONS.md`](../../../../CONVENTIONS.md).
- **Upstream pipeline**: `per_day_master.csv` (6 channel columns + date + recovery_phase + dose_plasma_mg + derived citalopram_phase) <- `pipeline/03_consolidate/build_unified_dataset.py`.

## Discipline guards (per CONVENTIONS)

- **sec 2.1 descriptive-before-inference**: NO causal claims; NO falsification bar; NO HA verdict promotion. All LOCKED HA + descriptive references are corroborative only.
- **sec 3.1 personal baseline**: 28d-trailing robust z (lag=1) on the rolling layer; pre-citalopram-pool robust median + MAD on the global-baseline layer.
- **sec 3.6 named counts**: every n in findings.md tables names scheme + unit.
- **sec 3.7 trajectory-detrend sensitivity**: resting_hr Q4.5.b caveat surfaced honestly.
- **sec 4.1 + sec 4.2 caveat-class**: descriptive framing only; 'channel X has earlier onset than Y under Method (a)' (NOT 'SSRI hits X first').
- **sec 4.3**: Method (b) data-driven change-point detection is exploratory; surfaced descriptively, cross-checked against Methods (a) + (c).
- **handoff sec 4 hard constraints**: NO HA artefact modifications; NO methodology MD modifications; NO per_day_master.csv modifications; NO iteration on the 4 user-locked operationalisation choices; NO promotion of non-CONFIRMED channels; NO mechanism interpretation of SSRI kinetics.
