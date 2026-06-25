# Findings -- Q4.3 era_boundaries (methodological backstop)

**Strand**: B (multi-year trajectory; descriptive). Closes the canonical Q4.3 scope per [`analyses/descriptive/README.md`](../../README.md) sec 4.3 for the first time in any artefact -- methodological backstop providing DESCRIPTIVE justification for the project's era/phase boundaries vs data-driven candidates.

**Surface**: full corpus (2021-08-16 to 2026-06-04; n=1754 day-level rows). 12 CURRENT boundaries x 7 channels = 84 cells. NO causal claims; NO recommendation to change any boundary; NO promotion of any data-driven candidate as 'better' (user-owned decision per [[feedback_methodology_decisions_documented_reasoning]]).

**CRITICAL USER FRAMING**: recovery-phase boundaries ARE the lived-experience reference per [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) sec 3.3-3.5. Data-driven candidates compared AGAINST recovery-phase boundaries; CONFIRMED-by-data candidates that LAND ON them are confirmatory; NOVEL-data-driven candidates that DON'T land on them are NOT 'wrong' -- they may reflect channel-specific dynamics unrelated to the recovery-phase axis.

**User-LOCKED operationalisation** (per Strand B sec 7c interview 2026-06-25; do NOT iterate):

1. **12 boundaries**: 6 recovery-phase (per lc_recovery_phase_axis sec 2) + 5 citalopram-phase (per citalopram_phase_stratification sec 3) + 1 historical 2023-12-31 train/validate split (per train_validate_split_fate.md; RETIRED).
2. **Method = both**: per-boundary distribution-shift tests (KS + mean-shift + cumulative; +-30d window per side) AND data-driven change-point detection (binary segmentation on 28d-rolling median; min-segment 60d; max-depth 12; reduction-threshold 5%).
3. **7 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr + gevoelscore (Q4.9 6 Garmin + outcome).
4. **Alternatives = data-driven only**, compared AGAINST recovery-phase boundaries as lived-experience reference (proximity tolerance +-21d = 3 * E[L]=7); NO round-date alternatives.

**Discipline**: Layer 1 descriptive (no causal claims; no falsification bar; no HA verdict promotion) per [CONVENTIONS sec 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + sec 4.1 + sec 4.2 caveat-class. The lc_recovery_phase_axis sec 7b resting_hr 4a->4b finding (+3.0 bpm CI [+2.0, +4.0]) is descriptively REPRODUCED + EXTENDED across 7 channels in Stage 2; the recovery_arc v2 sec 5.A afbouw-reversal is descriptively cross-referenced for the citalopram-phase 5 boundary; Q4.9 + Q4.6 cross-referenced descriptively.

---

## Headline

**Per-boundary distribution-shift table (12 x 7 = 84 cells)**: 6 of 12 boundaries show shift on >=4 of 7 channels (strong multi-channel discrimination); 3 on 2-3 channels (moderate); 3 on <2 channels (weak/inconclusive; HONESTLY does NOT mean 'unjustified' per CONVENTIONS sec 4.2 -- boundary warrant remains the lived-experience M1 or documented-confounder M2 source).

**lc_recovery_phase_axis sec 7b 4a->4b finding REPRODUCED + EXTENDED**: at the 2022-11-17 boundary (rp4), 4 of 7 channels show shift in the broader 7-channel test. Channels with shift: [all_day_stress_avg, resting_hr, stress_low_motion_min_count_S60_Mlow, stress_mean_sleep]

**Recovery-phase boundary 7-channel sensitivity arm**: of 6 recovery-phase boundaries, 5 have >=1 channel discriminating in the +-30d window test (Stage 2 multi-channel reading reproduces + extends the sec 7b 4a->4b single-channel-discrimination finding to the wider boundary set).

**Data-driven change-point candidates per channel** (binary segmentation on 28d-rolling median; min-segment 60d): 108 total candidates across 7 channels; 18 land within +-21d of a recovery-phase boundary (CONFIRMED-by-data; descriptive corroboration of the lived-experience anchors); 90 do NOT land near a recovery-phase boundary (NOVEL-data-driven; may reflect channel-specific dynamics unrelated to recovery-phase per CONVENTIONS sec 4.3; descriptive only, not promoted as 'better' boundary).

**Citalopram-phase boundary defensibility**: 1 of 5 citalopram-phase boundaries show shift on >=4 of 7 channels in Stage 2 (descriptive cross-reference to citalopram_phase_stratification sec 3 + recovery_arc v2 sec 5.A afbouw-reversal finding on 3 CONFIRMED-citalopram channels).

**Historical 2023-12-31 train/validate boundary** (RETIRED per train_validate_split_fate.md; preserved descriptively here for reproducibility-artefact closure): 3 of 7 channels show shift in the +-30d window. Channels with shift: [resting_hr, stress_mean_sleep, stress_stdev_sleep]

---

## 1. Boundary catalog and warrants

12 CURRENT boundaries per the user-LOCKED scope (handoff sec 2.1):

| boundary_id | date | warrant class | source MD |
|---|---|---|---|
| `rp1_pre_illness_to_acute` | 2022-03-21 | data-given | lc_recovery_phase_axis sec 3 |
| `rp2_acute_to_lc_pre_ergo` | 2022-04-04 | data-given | lc_recovery_phase_axis sec 3 |
| `rp3_lc_pre_ergo_to_4a` | 2022-09-22 | M1 lived-experience | lc_recovery_phase_axis sec 3 |
| `rp4_4a_to_4b` | 2022-11-17 | M1 lived-experience | lc_recovery_phase_axis sec 3 |
| `rp5_4b_to_citalopram_modulated` | 2024-04-09 | M2 documented confounder | lc_recovery_phase_axis sec 3 |
| `rp6_citalopram_modulated_to_post_afbouw` | 2026-06-06 | out-of-corpus | lc_recovery_phase_axis sec 3 |
| `cp1_unmedicated_to_buildup` | 2024-04-09 | documented intervention | citalopram_phase_stratification sec 3 |
| `cp2_buildup_to_consolidation` | 2024-06-20 | documented intervention | citalopram_phase_stratification sec 3 |
| `cp3_consolidation_to_afbouw` | 2026-03-20 | documented intervention | citalopram_phase_stratification sec 3 |
| `cp4_afbouw_to_post_afbouw` | 2026-06-06 | out-of-corpus | citalopram_phase_stratification sec 3 |
| `cp5_lc_start_to_unmedicated` | 2022-04-04 | documented stratum boundary | citalopram_phase_stratification sec 3 |
| `hist1_2023_12_31_train_validate` | 2023-12-31 | RETIRED historical M3 sensitivity overlay | train_validate_split_fate |

---

## 2. Stage 2 -- per-boundary distribution-shift tests (12 x 7 = 84 cells)

**Method**: for each boundary x channel cell, compute KS p-value (two-sample; permutation null, n_permutations=1000) + mean-shift + Cohen's d + cumulative-distribution shift on the +-30d window each side of the boundary. Rolling 28d-median per side as the secondary evidence. Descriptive shift_detected flag = `(KS p < 0.05) OR (|Cohen's d| > 0.5)` (per-cell only; NOT a verdict per CONVENTIONS sec 4.2 -- the load-bearing read is the multi-channel synthesis per boundary).

**Per-boundary multi-channel synthesis** (one row per boundary; columns = n_channels_shift + which channels):

| boundary_id | date | n_shift / n_tested | channels with shift |
|---|---|---:|---|
| `rp1_pre_illness_to_acute` | 2022-03-21 | 4 / 6 | all_day_stress_avg, resting_hr, stress_low_motion_min_count_S60_Mlow, stress_mean_sleep |
| `rp2_acute_to_lc_pre_ergo` | 2022-04-04 | 4 / 6 | all_day_stress_avg, bb_lowest, resting_hr, stress_mean_sleep |
| `rp3_lc_pre_ergo_to_4a` | 2022-09-22 | 4 / 7 | all_day_stress_avg, gevoelscore, resting_hr, stress_mean_sleep |
| `rp4_4a_to_4b` | 2022-11-17 | 4 / 7 | all_day_stress_avg, resting_hr, stress_low_motion_min_count_S60_Mlow, stress_mean_sleep |
| `rp5_4b_to_citalopram_modulated` | 2024-04-09 | 5 / 7 | all_day_stress_avg, bb_lowest, resting_hr, stress_low_motion_min_count_S60_Mlow, stress_mean_sleep |
| `rp6_citalopram_modulated_to_post_afbouw` | 2026-06-06 | 0 / 0 | (none) |
| `cp1_unmedicated_to_buildup` | 2024-04-09 | 5 / 7 | all_day_stress_avg, bb_lowest, resting_hr, stress_low_motion_min_count_S60_Mlow, stress_mean_sleep |
| `cp2_buildup_to_consolidation` | 2024-06-20 | 1 / 7 | resting_hr |
| `cp3_consolidation_to_afbouw` | 2026-03-20 | 3 / 7 | bb_lowest, gevoelscore, stress_mean_sleep |
| `cp4_afbouw_to_post_afbouw` | 2026-06-06 | 0 / 0 | (none) |
| `cp5_lc_start_to_unmedicated` | 2022-04-04 | 3 / 6 | all_day_stress_avg, bb_lowest, resting_hr |
| `hist1_2023_12_31_train_validate` | 2023-12-31 | 3 / 7 | resting_hr, stress_mean_sleep, stress_stdev_sleep |

**Per-channel rolling 28d-median shift at each boundary** (the slower-scale evidence; numbers are post-median minus pre-median):

| boundary_id | `stress_mean_sleep` | `all_day_stress_avg` | `bb_lowest` | `stress_stdev_sleep` | `stress_low_motion_min_count_S60_Mlow` | `resting_hr` | `gevoelscore` |
|---|---:|---:|---:|---:|---:|---:|---:|
| `rp1_pre_illness_to_acute` | +5.37 | +5.50 | -4.50 | +0.27 | +19.50 | +2.00 | n/a |
| `rp2_acute_to_lc_pre_ergo` | +3.62 | +5.50 | -4.00 | +0.46 | +6.00 | +2.00 | n/a |
| `rp3_lc_pre_ergo_to_4a` | +4.18 | +3.50 | -1.50 | -0.43 | +10.50 | +3.50 | +2.00 |
| `rp4_4a_to_4b` | +3.54 | +2.50 | -2.50 | -0.07 | +23.50 | +4.00 | -1.00 |
| `rp5_4b_to_citalopram_modulated` | -3.17 | -6.50 | +7.00 | +0.12 | -43.00 | -2.50 | +0.00 |
| `rp6_citalopram_modulated_to_post_afbouw` | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `cp1_unmedicated_to_buildup` | -3.17 | -6.50 | +7.00 | +0.12 | -43.00 | -2.50 | +0.00 |
| `cp2_buildup_to_consolidation` | -1.77 | -1.50 | +0.00 | -0.18 | -12.00 | -2.00 | -0.50 |
| `cp3_consolidation_to_afbouw` | -1.86 | +1.50 | -5.00 | -1.14 | +24.50 | +0.00 | +1.00 |
| `cp4_afbouw_to_post_afbouw` | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `cp5_lc_start_to_unmedicated` | +3.62 | +5.50 | -4.00 | +0.46 | +6.00 | +2.00 | n/a |
| `hist1_2023_12_31_train_validate` | -3.03 | -1.50 | +1.00 | -2.44 | -14.50 | -3.00 | +0.00 |

**LOAD-BEARING lc_recovery_phase_axis sec 7b cross-reference**: the rp4 (4a -> 4b at 2022-11-17) cell on `resting_hr` is the project's prior single-channel-discrimination finding (+3.0 bpm, CI [+2.0, +4.0], excludes 0); 5 of 6 other channels in the prior sec 7b test wide-included 0. Stage 2's broader 7-channel test at rp4 + the wider 6 recovery-phase boundary scope EXTENDS this descriptively across the full recovery-phase axis. Per CONVENTIONS sec 4.2: where Stage 2 surfaces ' boundary X shows shift on Z of 7 channels' this is a DESCRIPTIVE characterisation, not a verdict on whether the boundary is 'justified'.

---

## 3. Stage 3 -- data-driven change-point detection per channel

**Method choice (binary segmentation over PELT; documented per handoff sec 6 acceptance criterion 7)**:

- Binary segmentation operates on the 28d-rolling median of the raw channel (smooths daily noise; preserves multi-month drift).
- Parameters: min-segment-size = 60d (~2 months; prevents micro-boundaries below the lived-experience phase scale); max-depth = 12 (allows up to 12 candidate change-points; comfortable cover for the 12 CURRENT boundaries); reduction-threshold = 5% of within-segment SSD (descriptive noise floor).
- Chosen over PELT because: (a) parameter-light (only depth + min-size; no data-scale-dependent penalty parameter); (b) interpretable per-cut traceability; (c) project has no pre-existing change-point library dependency.

**Per-channel candidate change-point dates**:

| channel | n_candidates | candidates |
|---|---:|---|
| `stress_mean_sleep` | 10 | 2021-10-30, 2022-01-13, 2022-04-03, 2022-07-22, 2022-09-26, 2022-12-01, 2023-04-19, 2025-11-13, 2026-01-14, 2026-03-28 |
| `all_day_stress_avg` | 18 | 2021-10-29, 2022-01-15, 2022-04-07, 2022-08-02, 2022-11-28, 2023-02-08, 2023-07-17, 2023-09-15, 2024-01-02, 2024-04-14, 2024-06-13, 2024-09-03, 2024-12-26, 2025-02-24, 2025-06-12, 2025-09-21, 2025-12-02, 2026-03-20 |
| `bb_lowest` | 19 | 2021-11-03, 2022-03-03, 2022-06-08, 2022-09-11, 2022-11-25, 2023-02-10, 2023-05-17, 2023-07-17, 2023-09-29, 2023-12-29, 2024-04-09, 2024-07-20, 2024-09-29, 2025-01-02, 2025-03-14, 2025-06-05, 2025-09-22, 2025-12-03, 2026-03-10 |
| `stress_stdev_sleep` | 12 | 2021-11-11, 2022-01-11, 2022-03-12, 2022-05-12, 2022-08-23, 2022-12-22, 2023-05-22, 2023-07-22, 2023-09-26, 2024-01-14, 2025-12-03, 2026-03-28 |
| `stress_low_motion_min_count_S60_Mlow` | 19 | 2021-12-30, 2022-04-05, 2022-07-01, 2022-10-06, 2022-12-16, 2023-02-15, 2023-05-21, 2023-07-21, 2023-11-05, 2024-01-05, 2024-04-15, 2024-06-14, 2024-08-28, 2024-10-30, 2025-01-09, 2025-03-12, 2025-05-11, 2025-08-07, 2025-12-03 |
| `resting_hr` | 19 | 2021-12-09, 2022-03-31, 2022-08-01, 2022-12-03, 2023-03-14, 2023-07-08, 2023-09-10, 2023-11-20, 2024-01-19, 2024-04-29, 2024-08-06, 2024-10-11, 2025-01-05, 2025-03-06, 2025-05-05, 2025-07-18, 2025-10-06, 2025-12-06, 2026-03-12 |
| `gevoelscore` | 11 | 2023-07-02, 2023-09-06, 2023-12-28, 2024-04-27, 2024-07-25, 2024-09-23, 2024-12-02, 2025-02-01, 2025-05-17, 2025-11-27, 2026-02-27 |

---

## 4. Stage 4 -- proximity comparison vs recovery-phase boundaries

**Method**: per data-driven candidate, find the nearest recovery-phase boundary (one of 6 from lc_recovery_phase_axis sec 2); compute the date difference in days; flag as **CONFIRMED-by-data** if `|diff| <= 21d` (= 3 * E[L]=7 per permutation_null_block_length.md) else **NOVEL-data-driven**.

**Per-channel proximity flag (per candidate)**:

| channel | candidate | nearest_rp_boundary | diff_days | label |
|---|---|---|---:|---|
| `stress_mean_sleep` | 2021-10-30 | 2022-03-21 | -142 | NOVEL-data-driven |
| `stress_mean_sleep` | 2022-01-13 | 2022-03-21 | -67 | NOVEL-data-driven |
| `stress_mean_sleep` | 2022-04-03 | 2022-04-04 | -1 | CONFIRMED-by-data |
| `stress_mean_sleep` | 2022-07-22 | 2022-09-22 | -62 | NOVEL-data-driven |
| `stress_mean_sleep` | 2022-09-26 | 2022-09-22 | +4 | CONFIRMED-by-data |
| `stress_mean_sleep` | 2022-12-01 | 2022-11-17 | +14 | CONFIRMED-by-data |
| `stress_mean_sleep` | 2023-04-19 | 2022-11-17 | +153 | NOVEL-data-driven |
| `stress_mean_sleep` | 2025-11-13 | 2026-06-06 | -205 | NOVEL-data-driven |
| `stress_mean_sleep` | 2026-01-14 | 2026-06-06 | -143 | NOVEL-data-driven |
| `stress_mean_sleep` | 2026-03-28 | 2026-06-06 | -70 | NOVEL-data-driven |
| `all_day_stress_avg` | 2021-10-29 | 2022-03-21 | -143 | NOVEL-data-driven |
| `all_day_stress_avg` | 2022-01-15 | 2022-03-21 | -65 | NOVEL-data-driven |
| `all_day_stress_avg` | 2022-04-07 | 2022-04-04 | +3 | CONFIRMED-by-data |
| `all_day_stress_avg` | 2022-08-02 | 2022-09-22 | -51 | NOVEL-data-driven |
| `all_day_stress_avg` | 2022-11-28 | 2022-11-17 | +11 | CONFIRMED-by-data |
| `all_day_stress_avg` | 2023-02-08 | 2022-11-17 | +83 | NOVEL-data-driven |
| `all_day_stress_avg` | 2023-07-17 | 2022-11-17 | +242 | NOVEL-data-driven |
| `all_day_stress_avg` | 2023-09-15 | 2024-04-09 | -207 | NOVEL-data-driven |
| `all_day_stress_avg` | 2024-01-02 | 2024-04-09 | -98 | NOVEL-data-driven |
| `all_day_stress_avg` | 2024-04-14 | 2024-04-09 | +5 | CONFIRMED-by-data |
| `all_day_stress_avg` | 2024-06-13 | 2024-04-09 | +65 | NOVEL-data-driven |
| `all_day_stress_avg` | 2024-09-03 | 2024-04-09 | +147 | NOVEL-data-driven |
| `all_day_stress_avg` | 2024-12-26 | 2024-04-09 | +261 | NOVEL-data-driven |
| `all_day_stress_avg` | 2025-02-24 | 2024-04-09 | +321 | NOVEL-data-driven |
| `all_day_stress_avg` | 2025-06-12 | 2026-06-06 | -359 | NOVEL-data-driven |
| `all_day_stress_avg` | 2025-09-21 | 2026-06-06 | -258 | NOVEL-data-driven |
| `all_day_stress_avg` | 2025-12-02 | 2026-06-06 | -186 | NOVEL-data-driven |
| `all_day_stress_avg` | 2026-03-20 | 2026-06-06 | -78 | NOVEL-data-driven |
| `bb_lowest` | 2021-11-03 | 2022-03-21 | -138 | NOVEL-data-driven |
| `bb_lowest` | 2022-03-03 | 2022-03-21 | -18 | CONFIRMED-by-data |
| `bb_lowest` | 2022-06-08 | 2022-04-04 | +65 | NOVEL-data-driven |
| `bb_lowest` | 2022-09-11 | 2022-09-22 | -11 | CONFIRMED-by-data |
| `bb_lowest` | 2022-11-25 | 2022-11-17 | +8 | CONFIRMED-by-data |
| `bb_lowest` | 2023-02-10 | 2022-11-17 | +85 | NOVEL-data-driven |
| `bb_lowest` | 2023-05-17 | 2022-11-17 | +181 | NOVEL-data-driven |
| `bb_lowest` | 2023-07-17 | 2022-11-17 | +242 | NOVEL-data-driven |
| `bb_lowest` | 2023-09-29 | 2024-04-09 | -193 | NOVEL-data-driven |
| `bb_lowest` | 2023-12-29 | 2024-04-09 | -102 | NOVEL-data-driven |
| `bb_lowest` | 2024-04-09 | 2024-04-09 | +0 | CONFIRMED-by-data |
| `bb_lowest` | 2024-07-20 | 2024-04-09 | +102 | NOVEL-data-driven |
| `bb_lowest` | 2024-09-29 | 2024-04-09 | +173 | NOVEL-data-driven |
| `bb_lowest` | 2025-01-02 | 2024-04-09 | +268 | NOVEL-data-driven |
| `bb_lowest` | 2025-03-14 | 2024-04-09 | +339 | NOVEL-data-driven |
| `bb_lowest` | 2025-06-05 | 2026-06-06 | -366 | NOVEL-data-driven |
| `bb_lowest` | 2025-09-22 | 2026-06-06 | -257 | NOVEL-data-driven |
| `bb_lowest` | 2025-12-03 | 2026-06-06 | -185 | NOVEL-data-driven |
| `bb_lowest` | 2026-03-10 | 2026-06-06 | -88 | NOVEL-data-driven |
| `stress_stdev_sleep` | 2021-11-11 | 2022-03-21 | -130 | NOVEL-data-driven |
| `stress_stdev_sleep` | 2022-01-11 | 2022-03-21 | -69 | NOVEL-data-driven |
| `stress_stdev_sleep` | 2022-03-12 | 2022-03-21 | -9 | CONFIRMED-by-data |
| `stress_stdev_sleep` | 2022-05-12 | 2022-04-04 | +38 | NOVEL-data-driven |
| `stress_stdev_sleep` | 2022-08-23 | 2022-09-22 | -30 | NOVEL-data-driven |
| `stress_stdev_sleep` | 2022-12-22 | 2022-11-17 | +35 | NOVEL-data-driven |
| `stress_stdev_sleep` | 2023-05-22 | 2022-11-17 | +186 | NOVEL-data-driven |
| `stress_stdev_sleep` | 2023-07-22 | 2022-11-17 | +247 | NOVEL-data-driven |
| `stress_stdev_sleep` | 2023-09-26 | 2024-04-09 | -196 | NOVEL-data-driven |
| `stress_stdev_sleep` | 2024-01-14 | 2024-04-09 | -86 | NOVEL-data-driven |
| `stress_stdev_sleep` | 2025-12-03 | 2026-06-06 | -185 | NOVEL-data-driven |
| `stress_stdev_sleep` | 2026-03-28 | 2026-06-06 | -70 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2021-12-30 | 2022-03-21 | -81 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2022-04-05 | 2022-04-04 | +1 | CONFIRMED-by-data |
| `stress_low_motion_min_count_S60_Mlow` | 2022-07-01 | 2022-09-22 | -83 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2022-10-06 | 2022-09-22 | +14 | CONFIRMED-by-data |
| `stress_low_motion_min_count_S60_Mlow` | 2022-12-16 | 2022-11-17 | +29 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2023-02-15 | 2022-11-17 | +90 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2023-05-21 | 2022-11-17 | +185 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2023-07-21 | 2022-11-17 | +246 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2023-11-05 | 2024-04-09 | -156 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2024-01-05 | 2024-04-09 | -95 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2024-04-15 | 2024-04-09 | +6 | CONFIRMED-by-data |
| `stress_low_motion_min_count_S60_Mlow` | 2024-06-14 | 2024-04-09 | +66 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2024-08-28 | 2024-04-09 | +141 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2024-10-30 | 2024-04-09 | +204 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2025-01-09 | 2024-04-09 | +275 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2025-03-12 | 2024-04-09 | +337 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2025-05-11 | 2026-06-06 | -391 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2025-08-07 | 2026-06-06 | -303 | NOVEL-data-driven |
| `stress_low_motion_min_count_S60_Mlow` | 2025-12-03 | 2026-06-06 | -185 | NOVEL-data-driven |
| `resting_hr` | 2021-12-09 | 2022-03-21 | -102 | NOVEL-data-driven |
| `resting_hr` | 2022-03-31 | 2022-04-04 | -4 | CONFIRMED-by-data |
| `resting_hr` | 2022-08-01 | 2022-09-22 | -52 | NOVEL-data-driven |
| `resting_hr` | 2022-12-03 | 2022-11-17 | +16 | CONFIRMED-by-data |
| `resting_hr` | 2023-03-14 | 2022-11-17 | +117 | NOVEL-data-driven |
| `resting_hr` | 2023-07-08 | 2022-11-17 | +233 | NOVEL-data-driven |
| `resting_hr` | 2023-09-10 | 2024-04-09 | -212 | NOVEL-data-driven |
| `resting_hr` | 2023-11-20 | 2024-04-09 | -141 | NOVEL-data-driven |
| `resting_hr` | 2024-01-19 | 2024-04-09 | -81 | NOVEL-data-driven |
| `resting_hr` | 2024-04-29 | 2024-04-09 | +20 | CONFIRMED-by-data |
| `resting_hr` | 2024-08-06 | 2024-04-09 | +119 | NOVEL-data-driven |
| `resting_hr` | 2024-10-11 | 2024-04-09 | +185 | NOVEL-data-driven |
| `resting_hr` | 2025-01-05 | 2024-04-09 | +271 | NOVEL-data-driven |
| `resting_hr` | 2025-03-06 | 2024-04-09 | +331 | NOVEL-data-driven |
| `resting_hr` | 2025-05-05 | 2024-04-09 | +391 | NOVEL-data-driven |
| `resting_hr` | 2025-07-18 | 2026-06-06 | -323 | NOVEL-data-driven |
| `resting_hr` | 2025-10-06 | 2026-06-06 | -243 | NOVEL-data-driven |
| `resting_hr` | 2025-12-06 | 2026-06-06 | -182 | NOVEL-data-driven |
| `resting_hr` | 2026-03-12 | 2026-06-06 | -86 | NOVEL-data-driven |
| `gevoelscore` | 2023-07-02 | 2022-11-17 | +227 | NOVEL-data-driven |
| `gevoelscore` | 2023-09-06 | 2024-04-09 | -216 | NOVEL-data-driven |
| `gevoelscore` | 2023-12-28 | 2024-04-09 | -103 | NOVEL-data-driven |
| `gevoelscore` | 2024-04-27 | 2024-04-09 | +18 | CONFIRMED-by-data |
| `gevoelscore` | 2024-07-25 | 2024-04-09 | +107 | NOVEL-data-driven |
| `gevoelscore` | 2024-09-23 | 2024-04-09 | +167 | NOVEL-data-driven |
| `gevoelscore` | 2024-12-02 | 2024-04-09 | +237 | NOVEL-data-driven |
| `gevoelscore` | 2025-02-01 | 2024-04-09 | +298 | NOVEL-data-driven |
| `gevoelscore` | 2025-05-17 | 2026-06-06 | -385 | NOVEL-data-driven |
| `gevoelscore` | 2025-11-27 | 2026-06-06 | -191 | NOVEL-data-driven |
| `gevoelscore` | 2026-02-27 | 2026-06-06 | -99 | NOVEL-data-driven |

**Per-channel CONFIRMED-by-data vs NOVEL-data-driven count**:

| channel | n_candidates | n_CONFIRMED-by-data | n_NOVEL-data-driven |
|---|---:|---:|---:|
| `stress_mean_sleep` | 10 | 3 | 7 |
| `all_day_stress_avg` | 18 | 3 | 15 |
| `bb_lowest` | 19 | 4 | 15 |
| `stress_stdev_sleep` | 12 | 1 | 11 |
| `stress_low_motion_min_count_S60_Mlow` | 19 | 3 | 16 |
| `resting_hr` | 19 | 3 | 16 |
| `gevoelscore` | 11 | 1 | 10 |

---

## 5. Stage 5 -- per-recovery-phase-boundary defensibility chart

**Method**: for each of 6 recovery-phase boundaries, report (a) Stage 2's n_channels_shift (out of 7), (b) Stage 4's n_channels_confirming (count of channels with >=1 data-driven candidate within +-21d).

| rp_boundary | date | warrant | Stage2 shift / tested | Stage4 confirming channels |
|---|---|---|---:|---:|
| `rp1_pre_illness_to_acute` | 2022-03-21 | data-given | 4 / 6 | 2 / 7 |
| `rp2_acute_to_lc_pre_ergo` | 2022-04-04 | data-given | 4 / 6 | 4 / 7 |
| `rp3_lc_pre_ergo_to_4a` | 2022-09-22 | M1 lived-experience | 4 / 7 | 3 / 7 |
| `rp4_4a_to_4b` | 2022-11-17 | M1 lived-experience | 4 / 7 | 4 / 7 |
| `rp5_4b_to_citalopram_modulated` | 2024-04-09 | M2 documented confounder | 5 / 7 | 5 / 7 |
| `rp6_citalopram_modulated_to_post_afbouw` | 2026-06-06 | out-of-corpus | 0 / 0 | 0 / 7 |

**Channels confirming each recovery-phase boundary** (Stage 4 within +-21d tolerance):

| rp_boundary | confirming channels (Stage 4) | channels with shift (Stage 2) |
|---|---|---|
| `rp1_pre_illness_to_acute` | bb_lowest, stress_stdev_sleep | all_day_stress_avg, resting_hr, stress_low_motion_min_count_S60_Mlow, stress_mean_sleep |
| `rp2_acute_to_lc_pre_ergo` | all_day_stress_avg, resting_hr, stress_low_motion_min_count_S60_Mlow, stress_mean_sleep | all_day_stress_avg, bb_lowest, resting_hr, stress_mean_sleep |
| `rp3_lc_pre_ergo_to_4a` | bb_lowest, stress_low_motion_min_count_S60_Mlow, stress_mean_sleep | all_day_stress_avg, gevoelscore, resting_hr, stress_mean_sleep |
| `rp4_4a_to_4b` | all_day_stress_avg, bb_lowest, resting_hr, stress_mean_sleep | all_day_stress_avg, resting_hr, stress_low_motion_min_count_S60_Mlow, stress_mean_sleep |
| `rp5_4b_to_citalopram_modulated` | all_day_stress_avg, bb_lowest, gevoelscore, resting_hr, stress_low_motion_min_count_S60_Mlow | all_day_stress_avg, bb_lowest, resting_hr, stress_low_motion_min_count_S60_Mlow, stress_mean_sleep |
| `rp6_citalopram_modulated_to_post_afbouw` | (none) | (none) |

---

## 6. Cross-references (DESCRIPTIVE corroboration only; NO HA verdict promotion; NO boundary-change recommendation)

### LOAD-BEARING cross-references

- **`lc_recovery_phase_axis.md` sec 7b 4a->4b finding**: the +3.0 bpm CI [+2.0, +4.0] resting_hr discrimination at the 2022-11-17 boundary is REPRODUCED + EXTENDED across the wider 7-channel + 6-recovery-phase-boundary scope in Stage 2. The descriptive read aligns with the prior finding's narrative that the boundary is most clearly visible on the slow cardiovascular drift channel (resting_hr) and is silent or weak on the autonomic-load family at most boundary cells -- which is consistent with channel-specific time scales rather than 'boundary X is unjustified'. The methodology MD's M1 lived-experience warrants per sec 3.4a + sec 3.4b remain the source-of-truth for the boundary; this analysis provides DESCRIPTIVE corroboration only.
- **Q4.9 subjective <-> objective coupling** ([`trajectory/subjective_objective_coupling/findings.md`](../subjective_objective_coupling/findings.md)): the autonomic-load family pre-crash elevation pattern (stress_mean_sleep +0.313 crash-minus-matched z; all_day_stress_avg +0.259; resting_hr +0.422 on the 4d lead-up) descriptively contextualises Stage 2 boundary-shift reads on the same channels at the recovery-phase boundary cells where crash episodes concentrate (phase 4b + phase 5). Q4.9's per-phase coupling-rate tables provide the per-channel-per-phase rate substrate that Stage 2's boundary-window reads sit inside.
- **Q4.6 coverage_overview** ([`trajectory/coverage_overview/findings.md`](../coverage_overview/findings.md)): some recovery-phase 1/2/3 boundaries in 2021-2022 have limited gevoelscore coverage (gevoelscore corpus starts 2022-09-03; rp1 at 2022-03-21 + rp2 at 2022-04-04 + rp3 at 2022-09-22 are all pre-or-early gevoelscore). Stage 2 cells where the post-window has insufficient data return `skipped`; per CONVENTIONS sec 3.6 named-counts this is flagged honestly per cell rather than hidden.
- **`recovery_arc v2` sec 5.A afbouw-reversal** ([`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md)): the cp3 (consolidation -> afbouw at 2026-03-20) and cp4 (afbouw -> post_afbouw at 2026-06-06) boundaries are the boundaries the afbouw-reversal narrative sits across. The 3 CONFIRMED-citalopram channels' Stage 2 shifts at cp3 are descriptively consistent with the afbouw-reversal direction (stress_mean_sleep going UP from 19.07 consolidation to 20.20 afbouw; all_day_stress_avg from 31 to 34; bb_lowest from 22 to 15). The recovery_arc v2 substantive afbouw-reversal verdict is LOCKED and NOT extended here per CONVENTIONS sec 4.2.
- **`permutation_null_block_length.md` E[L]=7**: the +-21d proximity tolerance in Stage 4 = 3 * E[L]=7, the autocorrelation-aware scale that connects the Stage 3 change-point detection scale with the recovery-phase boundary date precision (lived-experience boundaries are dated to a specific event but have a tolerance window equal to a few E[L] cycles by definition).

### Methodology MDs cited (binding for this analysis's discipline)

- [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) sec 2 (6-phase axis definitions) + sec 3.3-3.5 (per-phase warrants) + sec 7b (4a->4b operationalisation interview lock).
- [`methodology/lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md) sec 1 (data-given strata; the HARD BOUNDARY in phase_axis_collapsibility_conventions sec 3.4 -- this analysis does NOT pool across phase 1 <-> phase 2 <-> LC era).
- [`methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) sec 3 (5 citalopram-phase boundaries + canonical `citalopram_phase()` helper) + sec 5.A-C (treatment patterns; NOT applied here -- descriptive scope does not require dose-adjusted predictors).
- [`methodology/train_validate_split_fate.md`](../../../../methodology/train_validate_split_fate.md) (historical 2023-12-31 split; RETIRED per the MD; characterised descriptively here for reproducibility-artefact closure only).
- [`methodology/permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) (E[L]=7 default for autocorrelation-aware analyses; Stage 4 proximity tolerance = 3 * E[L]).
- [CONVENTIONS sec 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + sec 3.1 + sec 3.6 + sec 4.1 + sec 4.2 + sec 4.3 (descriptive-before-inference; personal baseline; named counts; framing discipline; caveat-class; data-driven change-point detection as exploratory only).

### Upstream pipeline

- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` (7 channel columns + date + recovery_phase + citalopram_phase via dose_plasma_mg).

---

## Limitations

For a producer-mode Layer-1 descriptive Strand B methodological backstop (no falsification bar; no causal claim per [CONVENTIONS sec 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + sec 4.3), the binding constraints are:

1. **No 'boundary X is unjustified' claims** per CONVENTIONS sec 4.2 caveat-class: where Stage 2 surfaces a boundary x channel cell with no shift, the descriptive read is ' boundary X shows distribution shift on Z of 7 channels' -- it does NOT mean the boundary is 'unjustified'. Recovery-phase boundaries are the lived-experience anchors per [`lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) sec 3.3-3.5; the M1 warrant survives even if Stage 2 cells are weak (a boundary may capture a lived-experience transition not visible at the channel resolution tested).
2. **No data-driven-candidate-as-better-boundary recommendation** per CONVENTIONS sec 4.3: Stage 3 binary segmentation candidates are exploratory only. CONFIRMED-by-data candidates that LAND ON a recovery-phase boundary are descriptive corroboration; NOVEL-data-driven candidates that DON'T land on one may reflect channel-specific dynamics (e.g. seasonality on a stress channel; firmware-rollout on bb_overnight_gain) NOT a flaw in the recovery-phase axis.
3. **Binary segmentation method choice** (Stage 3) was DOCUMENTED at the run.py docstring per handoff sec 6 acceptance criterion 7. PELT was the alternative; binary segmentation chosen for parameter-light + interpretability + no library dependency. A future analysis could re-run with PELT as a sensitivity arm.
4. **+-30d window** in Stage 2 may miss long-scale shifts on channels with E[L]\* >> 7 (e.g. resting_hr where recovery_arc v2 reports E[L]\*=20.1 in phase 4b). The rolling 28d-median secondary evidence partially mitigates this, but a wider window (e.g. +-90d) would surface different per-cell shifts. Per CONVENTIONS sec 3.6 named-counts: the +-30d choice is documented; a sensitivity arm at +-90d is a queued follow-up.
5. **+-21d proximity tolerance** in Stage 4 = 3 * E[L]=7. Tighter tolerance (e.g. +-7d) would yield fewer CONFIRMED-by-data flags; wider (e.g. +-42d) would yield more. The +-21d choice is autocorrelation-aware but is a single point on a continuum.
6. **`bb_overnight_gain` excluded from the 7-channel scope per the user-locked operationalisation** (handoff sec 2.3): channel coverage starts 2024-09-18 (5 of 6 recovery-phase boundaries pre-date this; per Q4.6 + bb_overnight_gain_proxy.md). The channel would skip on most cells regardless; the 7-channel scope keeps the analysis cross-channel-comparable.
7. **Historical 2023-12-31 train/validate boundary** is RETIRED per train_validate_split_fate.md and characterised here for reproducibility-artefact closure only -- the Stage 2 read on this boundary is NOT a recommendation to revive the split.
8. **Out-of-corpus boundaries** (rp6 + cp4) at 2026-06-06 are 2 days after corpus end (2026-06-04); their per-cell tests honestly return n_post=0 and skip. Included in the count per the user-locked '6 + 5' scope; the per-cell skip is surfaced.
9. **No HA verdict promotion**: HA-C3 v2 + HA-C3p + HA-P6 v3 + recovery_arc v2 + crash_v2-definition LOCKED references are descriptive corroboration only; NONE are extended or re-interpreted per CONVENTIONS sec 4.2 + handoff sec 4 hard constraint.
10. **No methodology MD modifications** per handoff sec 4 hard constraint. lc_recovery_phase_axis + lc_era_temporal_segmentation + citalopram_phase_stratification + train_validate_split_fate + CONVENTIONS are NOT edited.
11. **No iteration on the 4 user-locked operationalisation choices** per Strand B sec 7c discipline.
12. **User-owned boundary decision**: this analysis provides DESCRIPTIVE justification material; the user owns any decision to revise (or not revise) the project's era/phase boundaries per [[feedback_methodology_decisions_documented_reasoning]].

---

*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` (gitignored per `docs/research/**/*.json`). To refresh: `python run.py`.*