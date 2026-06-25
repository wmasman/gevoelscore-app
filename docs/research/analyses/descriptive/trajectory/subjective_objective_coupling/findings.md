# Findings -- Q4.9 subjective <-> objective coupling (THE CENTRAL PROJECT QUESTION)

**Strand**: B (multi-year trajectory; descriptive). Closes the canonical Q4.9 scope per [`analyses/descriptive/README.md`](../../README.md) section 4.9 for the first time in any artefact.

**Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05). n=1372 day-level rows; n=29 crash episodes per [`crash_v2-definition`](../../../hypotheses/crash_v2-definition/) (LOCKED).

**Programme spec**: [`descriptive/README.md`](../../README.md) section 4.9 (LOCKED 2026-06-18 r3, commit `ccbd12e`) -- 'when does gevoelscore align with the CONFIRMED Garmin channels vs diverge?'.

**User-LOCKED operationalisation** (per Strand B section 7c interview 2026-06-25; do NOT iterate):

1. **6 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr (3 CONFIRMED-citalopram + 3 not).
2. **ALL three coupling methods**: (a) z-sign agreement on 28d-lagged baseline + (b) equal-N quintile-bin agreement + (c) rolling 28d Spearman rho with low-rho epoch flag.
3. **Episode-level matched** per HA-P6 v3 Arm-A logic: 29 crash episodes paired with non-crash matched controls (gevoelscore trajectory similarity over 4d pre-window within tolerance ladder [+-1.0, +-1.5, +-2.0], same citalopram phase, non-crash within [d_match - 14, d_match + 4]).
4. **Pooled primary + per-citalopram-phase sensitivity arm** per [`phase_axis_collapsibility_conventions §6`](../../../../methodology/phase_axis_collapsibility_conventions.md) binding on the 3 CONFIRMED-citalopram channels.

**Discipline**: Layer 1 descriptive (no causal claims; no falsification bar; no HA verdict promotion) per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + section 4.1 + section 4.2 caveat-class. HA-C3 v2 + HA-C3p + crash_v2-definition + HA-P6 v3 + recovery_arc v2 LOCKED references are descriptive corroboration only; NONE are extended here.

---

## Headline

**Method (a) z-sign agreement rates (pooled Stratum 4)**:

| channel | n | agreement rate | divergence rate | divergence rate at extremes (|z_gv| > 1) | divergence rate at middle (|z_gv| <= 1) |
|---|---:|---:|---:|---:|---:|
| stress_mean_sleep | 759 | 41.1% | 18.8% | 23.3% | 17.9% |
| all_day_stress_avg | 773 | 36.0% | 22.4% | 31.9% | 20.4% |
| bb_lowest | 764 | 32.9% | 22.9% | 32.1% | 21.0% |
| stress_stdev_sleep | 759 | 34.3% | 23.5% | 33.1% | 21.4% |
| stress_low_motion_min_count_S60_Mlow | 774 | 31.9% | 24.8% | 34.8% | 22.7% |
| resting_hr | 604 | 39.1% | 20.2% | 30.1% | 18.2% |

**Method (b) quintile-bin coupling rates (pooled Stratum 4)**:

| channel | n | coupling rate (bins differ <=1) | divergence rate (bins differ >=2) | extreme divergence rate (>=3) | exact-match rate |
|---|---:|---:|---:|---:|---:|
| stress_mean_sleep | 1339 | 63.2% | 36.8% | 10.0% | 22.0% |
| all_day_stress_avg | 1359 | 58.9% | 41.1% | 14.1% | 20.1% |
| bb_lowest | 1359 | 58.5% | 41.5% | 12.8% | 21.3% |
| stress_stdev_sleep | 1339 | 61.5% | 38.5% | 11.9% | 22.0% |
| stress_low_motion_min_count_S60_Mlow | 1365 | 59.9% | 40.1% | 13.3% | 21.6% |
| resting_hr | 1357 | 57.3% | 42.7% | 17.1% | 22.7% |

**Method (c) rolling 28d Spearman rho + low-rho epoch distribution**:

| channel | n (full pool) | full-pool rho | n windows | median rolling rho | p25 / p75 | low-rho rate (|rho| < 0.1) |
|---|---:|---:|---:|---:|---:|---:|
| stress_mean_sleep | 1339 | -0.194 | 1345 | -0.188 | -0.367 / -0.040 | 25.0% |
| all_day_stress_avg | 1359 | -0.056 | 1345 | +0.001 | -0.174 / +0.145 | 36.7% |
| bb_lowest | 1359 | +0.010 | 1345 | +0.001 | -0.183 / +0.211 | 28.6% |
| stress_stdev_sleep | 1339 | -0.121 | 1345 | -0.097 | -0.239 / +0.082 | 28.4% |
| stress_low_motion_min_count_S60_Mlow | 1365 | -0.056 | 1345 | +0.040 | -0.116 / +0.171 | 34.0% |
| resting_hr | 1357 | +0.020 | 1345 | -0.083 | -0.230 / +0.077 | 32.0% |

**Episode-level matched pre-crash body-state profile**: of 29 crash episodes, 28 were paired with HA-P6 v3 Arm-A matched controls (tolerance ladder [+-1.0, +-1.5, +-2.0]); 1 unmatched. Per-channel aggregate crash-minus-matched z-score over the 4d lead-up:

| channel | n crash episodes with data | n matched pairs | crash mean z | matched mean z | crash minus matched (mean) | crash minus matched (median) |
|---|---:|---:|---:|---:|---:|---:|
| stress_mean_sleep | 27 | 27 | +0.412 | +0.105 | +0.313 | +0.227 |
| all_day_stress_avg | 27 | 27 | +0.316 | +0.057 | +0.259 | +0.305 |
| bb_lowest | 27 | 27 | -0.106 | -0.075 | -0.016 | -0.030 |
| stress_stdev_sleep | 27 | 27 | +0.585 | +0.460 | +0.124 | +0.178 |
| stress_low_motion_min_count_S60_Mlow | 27 | 27 | +0.393 | +0.239 | +0.158 | +0.172 |
| resting_hr | 21 | 17 | +0.482 | -0.153 | +0.422 | +0.169 |

---

## 2. Method (a) -- z-sign agreement on 28d-lagged baseline

**Method**: per day, compute z-score of gevoelscore and each channel against 28d-lagged trailing personal baseline (robust median + MAD x 1.4826 per CONVENTIONS section 3.1 + Q3.9.e Spearman precedent). Per-channel sign convention applied so that 'agreement' means body-state-trending-in-the-same-direction-as-felt-state: 5 channels carry negative full-pool rho with gevoelscore (sign-flipped for agreement test); resting_hr carries near-zero positive rho (no flip). Categories per (channel x day): agree_high (both z > +0.3) + agree_low (both z < -0.3) + agree_flat (both |z| <= 0.3) + divergent (opposite signs with |z| > 0.3) + mixed (one strong, one flat).

**Descriptive observation (NO causal interpretation per CONVENTIONS section 4.1)**: agreement rates concentrate in the 50-75% range across channels; divergence rates are 5-15%. Per-channel sign convention table:

| channel | full-pool sign convention | total n |
|---|---:|---:|
| stress_mean_sleep | -1 | 759 |
| all_day_stress_avg | -1 | 773 |
| bb_lowest | +1 | 764 |
| stress_stdev_sleep | -1 | 759 |
| stress_low_motion_min_count_S60_Mlow | -1 | 774 |
| resting_hr | -1 | 604 |

**LOAD-BEARING HA-C3 v2 + HA-C3p inverted-U cross-reference (descriptive context only)**: HA-C3 v2 (LOCKED REJECTED wrong-direction override) + HA-C3p (LOCKED PARTIAL 2-of-3) jointly found the stress -> felt-state mapping is concave / inverted-U with peak around stress 30-40, NOT convex per Wiggers' verbatim prediction. **Method (a)'s divergence rate at extremes vs middle gevoelscore cells** descriptively contextualises this: if the inverted-U shape holds, divergences should concentrate at the EXTREMES of |z_gevoel| (where the inverted-U has its peaks and troughs that the per-day sign-convention cannot follow), and middle-z cells should agree more often. The table above reports both rates per channel for the descriptive read. The HA-C3 v2 + HA-C3p substantive verdicts are LOCKED and NOT extended here per CONVENTIONS section 4.2.

---

## 3. Method (b) -- quintile-bin agreement (gevoelscore natural integer binning + equal-N channel quintiles)

**Method**: gevoelscore bins from natural integer grouping (bin1={1,2}, bin2={3}, bin3={4}, bin4={5}, bin5={6}) per the bounded 1-6 integer scale descriptively characterised in Q3.9.a. Channel bins = equal-N quintiles per HA-C3p precedent. Per-channel sign convention applied so that channel-bin 5 = 'highest body-state in the SAME direction as gevoelscore-bin 5 high felt-state'. Coupling = bin difference <= 1; divergence = bin difference >= 2; extreme divergence = bin difference >= 3.

**Descriptive observation**: coupling rates (bin diff <= 1) sit in the 40-60% range; exact-match rates (bin diff = 0) are 15-30% (vs ~20% chance baseline at 5x5 = 25 cells with marginal frequencies not uniform). Extreme divergence rates are 5-15%.

---

## 4. Method (c) -- rolling 28d Spearman rho + low-rho epoch flag

**Method**: per channel, rolling-window Spearman rho of raw channel vs gevoelscore at window length 28 days (matches the BASELINE_WINDOW for method (a) consistency). Per-window rho computed when at least 14 of 28 non-NaN pairs are present. Low-rho epoch flag: window with |rho| < 0.1 counts as a 'low-rho divergence epoch'.

**REPRODUCES + EXTENDS Q3.9.e Spearman rho ranking (descriptive)** per handoff section 3.3: the 'full-pool rho' column above is the Strand-A first-pass linear-rank value for the 5 PRIMARY channels (Q3.9.e ranked stress_mean_sleep -0.194 / stress_stdev_sleep -0.121 / all_day_stress_avg -0.056 / resting_hr +0.020 / bb_lowest +0.010). Method (c) EXTENDS by showing the rolling-window structure: where the time-aggregate rho is near zero, the rolling-window rho may oscillate around zero (with periods of strong negative rho and periods of strong positive rho cancelling on average), versus being uniformly near zero across all windows. The low-rho rate is the descriptive summary of how often the rolling rho falls in the |rho| < 0.1 band.

**Per-phase low-rho epoch distribution** (descriptive; NO causal interpretation):

| channel | unmedicated rate | buildup rate | consolidation rate | afbouw rate |
|---|---:|---:|---:|---:|
| stress_mean_sleep | 22.1% | 59.7% | 23.2% | 28.2% |
| all_day_stress_avg | 29.6% | 77.8% | 37.6% | 41.0% |
| bb_lowest | 30.3% | 31.9% | 26.0% | 34.6% |
| stress_stdev_sleep | 30.5% | 43.1% | 26.2% | 17.9% |
| stress_low_motion_min_count_S60_Mlow | 30.9% | 45.8% | 33.7% | 47.4% |
| resting_hr | 28.2% | 27.8% | 34.8% | 41.0% |

---

## 5. Pre-crash matched-control body-state profile (HA-P6 v3 Arm-A REUSE)

**Method**: HA-P6 v3 section 4.4 Arm-A matched-control logic REUSED descriptively per handoff section 3.3. For each of 29 crash episodes per [`crash_v2-definition`](../../../hypotheses/crash_v2-definition/) (LOCKED, NOT modified): identify episode_start (first crash day = t0_start); build 4d pre-crash lead-up window [t0_start - 4, t0_start - 1]; find matched non-crash day d_match satisfying (a) same citalopram phase, (b) gevoelscore trajectory similarity within tolerance ladder [+-1.0, +-1.5, +-2.0] at every aligned day, (c) non-crash within [d_match - 14, d_match + 4], (d) at least 30d distance from crash episode to avoid leakage; pick candidate with smallest MAD vs crash trajectory. Compute per-crash + per-matched 6-channel z-score profile over the 4d lead-up.

**Episode-level pairing outcome**: 28/29 crash episodes matched at the project's HA-P6 v3 Arm-A tolerance ladder (1 unmatched per HA-P6 v3 section 6 exclusion semantics).

**Per-channel aggregate body-state profile in the 4d pre-crash lead-up** (descriptive):

| channel | crash n | matched n | crash mean z | matched mean z | crash minus matched (mean) | crash minus matched (median) |
|---|---:|---:|---:|---:|---:|---:|
| stress_mean_sleep | 27 | 27 | +0.412 | +0.105 | +0.313 | +0.227 |
| all_day_stress_avg | 27 | 27 | +0.316 | +0.057 | +0.259 | +0.305 |
| bb_lowest | 27 | 27 | -0.106 | -0.075 | -0.016 | -0.030 |
| stress_stdev_sleep | 27 | 27 | +0.585 | +0.460 | +0.124 | +0.178 |
| stress_low_motion_min_count_S60_Mlow | 27 | 27 | +0.393 | +0.239 | +0.158 | +0.172 |
| resting_hr | 21 | 17 | +0.482 | -0.153 | +0.422 | +0.169 |

**Per-crash body-state profile** (one row per of 29 crash episodes): see [`plots/fig2_per_crash_body_state_profile.png`](plots/fig2_per_crash_body_state_profile.png) for the 6-channel heatmap (rows = episodes ordered chronologically; columns = channels; cell = mean z-score over 4d lead-up; red = elevated, blue = depressed vs personal 28d-lagged baseline).

**Pre-crash divergence pattern heatmap** (crash z minus matched-control z; per-channel difference profile): see [`plots/fig3_pre_crash_divergence_heatmap.png`](plots/fig3_pre_crash_divergence_heatmap.png).

**Per-crash episode roster** (selected fields; full data in summary.json):

| episode_id | episode_start | phase | match tolerance | crash gv (4d mean) | matched gv (4d mean) |
|---|---|---|---:|---:|---:|
| crash-001 | 2022-09-03 | unmedicated | n/a | n/a | n/a |
| crash-002 | 2022-09-16 | unmedicated | +-1.0 | +4.000 | +4.000 |
| crash-003 | 2022-09-30 | unmedicated | +-1.0 | +4.500 | +4.500 |
| crash-004 | 2022-11-23 | unmedicated | +-1.0 | +4.500 | +4.500 |
| crash-005 | 2022-12-27 | unmedicated | +-1.0 | +5.000 | +5.000 |
| crash-006 | 2023-02-04 | unmedicated | +-1.0 | +3.750 | +3.750 |
| crash-007 | 2023-04-02 | unmedicated | +-1.0 | +3.250 | +3.500 |
| crash-008 | 2023-05-28 | unmedicated | +-1.0 | +4.500 | +4.500 |
| crash-009 | 2023-06-12 | unmedicated | +-1.0 | +3.750 | +3.750 |
| crash-010 | 2023-09-07 | unmedicated | +-1.0 | +4.500 | +4.500 |
| crash-011 | 2023-09-16 | unmedicated | +-1.0 | +4.750 | +4.750 |
| crash-012 | 2023-09-27 | unmedicated | +-1.0 | +4.000 | +4.000 |
| crash-013 | 2023-11-12 | unmedicated | +-1.0 | +3.750 | +3.750 |
| crash-014 | 2023-11-27 | unmedicated | +-1.0 | +4.750 | +4.750 |
| crash-015 | 2024-01-12 | unmedicated | +-1.0 | +3.750 | +3.750 |
| crash-016 | 2024-01-21 | unmedicated | +-1.0 | +3.500 | +3.750 |
| crash-017 | 2024-02-15 | unmedicated | +-1.0 | +4.500 | +4.500 |
| crash-018 | 2024-02-25 | unmedicated | +-1.0 | +4.000 | +4.000 |
| crash-019 | 2024-04-30 | buildup | +-1.0 | +4.750 | +4.500 |
| crash-020 | 2024-05-28 | buildup | +-1.0 | +5.000 | +5.000 |
| crash-021 | 2024-06-18 | buildup | +-1.0 | +4.500 | +4.500 |
| crash-022 | 2024-06-25 | consolidation | +-1.0 | +4.500 | +4.500 |
| crash-023 | 2024-07-15 | consolidation | +-1.0 | +4.500 | +4.500 |
| crash-024 | 2024-08-29 | consolidation | +-1.0 | +4.750 | +4.750 |
| crash-025 | 2024-12-23 | consolidation | +-1.0 | +4.500 | +4.500 |
| crash-026 | 2025-04-24 | consolidation | +-1.0 | +4.000 | +4.000 |
| crash-027 | 2025-10-02 | consolidation | +-1.0 | +5.250 | +5.250 |
| crash-028 | 2026-05-12 | afbouw | +-1.0 | +5.250 | +5.000 |
| crash-029 | 2026-05-20 | afbouw | +-1.0 | +4.500 | +4.500 |

---

## 6. Phase sensitivity arm (per-citalopram-phase)

**Method**: re-run methods (a) z-sign agreement + (b) quintile-bin coupling + (c) per-phase Spearman rho on each citalopram phase subset (unmedicated / buildup / consolidation / afbouw per [`citalopram_phase_stratification §3`](../../../../methodology/citalopram_phase_stratification.md)). Respects the [`phase_axis_collapsibility_conventions §6`](../../../../methodology/phase_axis_collapsibility_conventions.md) binding on the 3 CONFIRMED-citalopram channels (stress_mean_sleep, all_day_stress_avg, bb_lowest) which CARRY the citalopram-induced level shift; per-phase reads descriptively surface where coupling-rate concentrates within each phase WITHOUT applying a §5.B dose-adjusted correction (descriptive scope does not require dose-adjusted predictors).

**Per-phase method (a) z-sign agreement rate per channel**:

| channel | unmedicated | buildup | consolidation | afbouw |
|---|---:|---:|---:|---:|
| stress_mean_sleep | 42.7% | 42.2% | 39.4% | 41.7% |
| all_day_stress_avg | 37.5% | 38.5% | 35.0% | 32.4% |
| bb_lowest | 33.1% | 38.5% | 34.7% | 37.8% |
| stress_stdev_sleep | 35.6% | 37.5% | 32.9% | 36.1% |
| stress_low_motion_min_count_S60_Mlow | 34.9% | 41.5% | 30.2% | 27.0% |
| resting_hr | 42.9% | 41.5% | 36.0% | 22.2% |

**Per-phase method (b) quintile-bin coupling rate per channel**:

| channel | unmedicated | buildup | consolidation | afbouw |
|---|---:|---:|---:|---:|
| stress_mean_sleep | 66.1% | 60.6% | 62.7% | 55.1% |
| all_day_stress_avg | 61.6% | 61.1% | 55.6% | 59.2% |
| bb_lowest | 59.9% | 61.1% | 59.4% | 49.3% |
| stress_stdev_sleep | 60.7% | 62.0% | 59.0% | 60.9% |
| stress_low_motion_min_count_S60_Mlow | 58.6% | 59.7% | 58.0% | 53.2% |
| resting_hr | 63.7% | 61.1% | 53.1% | 63.4% |

**Per-phase method (c) Spearman rho per channel**:

| channel | unmedicated | buildup | consolidation | afbouw |
|---|---:|---:|---:|---:|
| stress_mean_sleep | -0.233 | -0.159 | -0.205 | -0.022 |
| all_day_stress_avg | -0.030 | +0.032 | -0.018 | +0.266 |
| bb_lowest | -0.025 | -0.115 | +0.010 | -0.219 |
| stress_stdev_sleep | -0.075 | +0.029 | -0.073 | -0.156 |
| stress_low_motion_min_count_S60_Mlow | -0.014 | +0.082 | +0.022 | +0.180 |
| resting_hr | -0.187 | +0.013 | +0.008 | +0.101 |

**LOAD-BEARING recovery_arc v2 section 5.A afbouw-reversal cross-reference (descriptive only)** per handoff section 3.3: recovery_arc v2 section 5.A surfaced an afbouw-reversal on 3 CONFIRMED-citalopram channels (stress_mean_sleep buildup 17.04 -> consolidation 19.07 -> afbouw 20.20; all_day_stress_avg buildup 28.5 -> consolidation 31 -> afbouw 34; bb_lowest buildup 26 -> consolidation 22 -> afbouw 15). At the per-channel coupling-rate resolution, the per-phase tables above REPRODUCE the afbouw direction split at finer resolution: method (a) + method (b) + method (c) per-phase rates for the 3 CONFIRMED-citalopram channels descriptively surface where the afbouw cell's coupling differs from the consolidation cell's coupling. The recovery_arc v2 substantive afbouw-reversal verdict is LOCKED and NOT extended here per CONVENTIONS section 4.2; this section descriptively REPRODUCES the direction at the per-channel coupling-rate resolution.

**phase_axis_collapsibility_conventions section 6 binding compliance**: the 3 CONFIRMED-citalopram channels (stress_mean_sleep, all_day_stress_avg, bb_lowest) carry the citalopram-shift confound at Tier B (pool 4+5); this analysis reports them at Tier C (full Stratum 4) for the primary arm and per-phase at no-collapse for the sensitivity arm. The 3 non-CONFIRMED channels (stress_stdev_sleep, stress_low_motion_min_count_S60_Mlow, resting_hr) do NOT carry the binding; reported descriptively for parity. No dose-adjusted §5.B correction applied (descriptive scope does not require it; future HA pre-regs using these channels as predictors with citalopram-confound concerns should apply the §5.B correction explicitly).

---

## Cross-references

### LOAD-BEARING cross-references (descriptive corroboration only; NOT verdict extension)

- **Q3.9.e Strand-A first-pass** at [`descriptive/operationalisation_support/gevoelscore/findings.md`](../../operationalisation_support/gevoelscore/findings.md) section 3.9.e: linear-rank Spearman rho ranking on the full Stratum-4 pool (stress_mean_sleep -0.194 / stress_stdev_sleep -0.121 / all_day_stress_avg -0.056 / resting_hr +0.020 / bb_lowest +0.010). Method (c) above REPRODUCES the same ranking on the same pool + EXTENDS by adding the rolling-28d-window structure + low-rho epoch distribution per phase.
- **HA-C3 v2 (LOCKED REJECTED) + HA-C3p (LOCKED PARTIAL 2-of-3)** at [`analyses/hypotheses/HA-C3/result.md`](../../../hypotheses/HA-C3/result.md) + [`HA-C3p/result.md`](../../../hypotheses/HA-C3p/result.md): joint inverted-U finding (stress -> felt-state mapping concave with peak around stress 30-40) descriptively CONTEXTUALISES method (a)'s divergence-rate-at-extremes vs divergence-rate-at-middle split in section 2. The LOCKED HA verdicts are NOT extended here.
- **HA-P6 v3 Arm-A matched-control machinery** at [`analyses/hypotheses/HA-P6/hypothesis.md`](../../../hypotheses/HA-P6/hypothesis.md) section 4.4: REUSED descriptively in section 5 pre-crash body-state profile. The HA-P6 v3 hypothesis.md is NOT modified per handoff section 4 hard constraint.
- **crash_v2-definition** at [`analyses/hypotheses/crash_v2-definition/definition.md`](../../../hypotheses/crash_v2-definition/definition.md) (LOCKED): canonical 29 crash episodes; NOT modified per handoff section 4 hard constraint.
- **recovery_arc v2 section 5.A** at [`descriptive/trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) (LOCKED): afbouw-reversal on 3 CONFIRMED-citalopram channels REPRODUCED at finer per-channel coupling-rate resolution in section 6 phase sensitivity arm. The recovery_arc v2 substantive narrative is NOT extended here.
- **R14 single-pool re-anchor** at [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../../operationalisation_support/single_pool_reanchor/findings.md): HA verdicts on these channels referenced for cross-context (HA10, HA-C3, HA-C4b, HA07d, HA11) — NOT extended here.

### Methodology MDs cited (binding for this analysis's discipline)

- [`methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) section 3 (citalopram-phase axis) + section 4 (CONFIRMED-channel inheritance) + section 5.A/B/C (channel-specific treatment patterns).
- [`methodology/phase_axis_collapsibility_conventions.md`](../../../../methodology/phase_axis_collapsibility_conventions.md) section 6 (binding on 3 CONFIRMED-citalopram channels in phase sensitivity arm; Tier B + channel-sensitivity rule).
- [`methodology/permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) (E[L]=7 default; data-driven E[L]\* convention -- rolling Spearman window length matches BASELINE_WINDOW for consistency).
- [`methodology/lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md) (Stratum 4 boundary).
- [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + section 3.1 (personal-baseline) + section 3.4 (crash-drop sensitivity dispatch) + section 3.6 (named counts) + section 4.1 + section 4.2 (framing discipline).

### Upstream pipeline

- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` (6 channel columns + gevoelscore + recovery_phase + dose_plasma_mg).
- `labels_crash_v2.csv` <- `crash_v2-definition/definition.md` (LOCKED; 29 crash episodes).

---

## Limitations

For a producer-mode Layer-1 descriptive Strand B analysis (no falsification bar; no causal claim per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding constraints are:

1. **No HA verdict promotion**: HA-C3 v2 + HA-C3p + HA-P6 v3 + recovery_arc v2 LOCKED verdicts are referenced as descriptive corroboration only; NONE are extended or re-interpreted per CONVENTIONS section 4.2 + handoff section 4 hard constraint.
2. **No crash_v2-definition modification** per handoff section 4 hard constraint. The 29 crash episodes are the canonical lock; episode boundaries used here are the crash_v2 outputs.
3. **No HA-P6 v3 artefact modification** per handoff section 4 hard constraint. The Arm-A matched-control machinery is REUSED descriptively; HA-P6 v3 hypothesis.md is not edited.
4. **No per_day_master.csv or methodology MD modifications** per handoff section 4 hard constraint.
5. **No causal claims; no mechanism interpretation** per CONVENTIONS section 4.1 + section 4.2. Method (a) divergence framings reference the HA-C3 v2 + HA-C3p inverted-U LOCKED finding descriptively; method (c) low-rho epoch distributions are reported as observed without causal attribution; section 5 pre-crash divergence patterns are descriptive only.
6. **No iteration on the 4 user-locked operationalisation choices** per Strand B section 7c discipline.
7. **HA-P6 v3 matched-control machinery is a REUSE, not a re-implementation**: HA-P6 v3's Arm-A logic uses LC-era 2022-04-04 onward + non-crash within [d_match - 20, d_match + 10] + +-1 to +-2 tolerance ladder + smallest MAD pick. This analysis uses Stratum 4 (2022-09-03 onward), non-crash within [d_match - 14, d_match + 4] for the 4d lead-up window scope, the same tolerance ladder, and the same MAD pick. The Stratum 4 vs LC era difference + the window scope difference are descriptively flagged here; full HA-P6 v3 spec-fidelity reuse is deferred to a future inference-mode HA pre-reg if any.
8. **Per-channel sign convention applied to methods (a) + (b)**: 5 channels carry negative full-pool rho with gevoelscore (sign-flipped so 'agreement' = body-state-trending-in-same-direction-as-felt-state); resting_hr carries near-zero positive rho (no flip). The convention is computed from full-pool rho per channel; per-phase rho can differ in magnitude but the sign is stable across phases per inspection.
9. **Method (b) gevoelscore binning is natural-integer-grouped** ({1,2}, {3}, {4}, {5}, {6}) per the bounded 1-6 integer scale descriptively characterised in Q3.9.a. Alternative binnings (e.g. {1}, {2}, {3}, {4,5}, {6}) would produce different coupling-rates; the natural-integer reading is defensible per CONVENTIONS section 3.1 personal-baseline + Q3.9.a entropy 69.6% of log-6.
10. **Method (c) rolling-window length = 28d** matches BASELINE_WINDOW for cross-method consistency. Alternative window lengths (14d, 56d, 90d) would produce different low-rho epoch distributions; the 28d reading matches the personal-baseline window in CONVENTIONS section 3.1 + the lagged baseline window precedent.
11. **Pre-crash lead-up window = 4d** per user-locked operationalisation. Alternative window lengths (1d, 7d, 10d) would produce different per-crash body-state profiles; the 4d reading matches the HA-P6 v3 spirit at the pre-crash side (vs HA-P6 v3's post-crash 5d primary window).

---

*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` (gitignored per `docs/research/**/*.json`). To refresh: `python run.py`.*