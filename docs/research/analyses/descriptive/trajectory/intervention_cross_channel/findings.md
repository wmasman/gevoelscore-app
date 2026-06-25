# Findings -- Q4.2 intervention_cross_channel (integrated citalopram picture)

**Strand**: B (multi-year trajectory; descriptive). Closes the canonical Q4.2 scope per [`analyses/descriptive/README.md`](../../README.md) sec 4.2 for the first time in any artefact -- integrated cross-channel timing + transition picture of the citalopram effect.

**Surface**: full corpus (2021-08-16 to 2026-06-04; n=1754 day-level rows). 6 channels x 3 timing-onset methods + 2 transitions analysed. NO causal claims; NO promotion of non-CONFIRMED channels to CONFIRMED-citalopram candidacy; NO mechanism interpretation of SSRI kinetics.

**User-LOCKED operationalisation** (per Strand B sec 7c interview 2026-06-25; do NOT iterate):

1. **6 channels**: stress_mean_sleep + all_day_stress_avg + bb_lowest (CONFIRMED-citalopram v3) + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr (non-CONFIRMED; descriptive only).
2. **ALL 3 timing-onset methods + sensitivity**: (a) threshold-cross (|z| >= 1.0 sustained >= 7d post-2024-04-09); (b) PELT/binseg change-point on post-citalopram z-trajectory; (c) time-to-half-effect via exponential decay fit (SSRI-kinetics proxy).
3. **Buildup-transition (2024-04-09) + afbouw-reversal (2026-03-20)**: per-channel Delta-z across each transition; Stage 5 reproduces Pattern 2 6-channel afbouw direction split from STOCKTAKE sec 6.
4. **ALL 3 visualisations**: per-channel timeline aligned at t0=2024-04-09 + heatmap (channel x time x z) + cross-channel timing ladder per 3 methods (+ method-sensitivity comparison plot).

**Discipline**: Layer 1 descriptive (no causal claims; no falsification bar; no HA verdict promotion) per [CONVENTIONS sec 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + sec 4.1 + sec 4.2 caveat-class. Honest framing per handoff sec 3.4: 'channel X has earlier onset than channel Y under Method (a)' is descriptive observation; NOT 'the SSRI hits channel X first'.

---

## Headline

**Cross-channel timing ladder (consensus order across 3 methods; descriptive)**: all_day_stress_avg (mean rank 1.67), bb_lowest (mean rank 2.33), resting_hr (mean rank 3.67), stress_mean_sleep (mean rank 4.33), stress_low_motion_min_count_S60_Mlow (mean rank 5.33), stress_stdev_sleep (mean rank 5.67)

**Method-sensitivity**: 1 of 6 channels are STABLE across all 3 methods (rank diff <=1 on every method-pair); 5 channels DISAGREE on at least one method-pair (rank diff >1).

**Buildup-transition Delta-z per channel at 2024-04-09** (z_pre median in +-30d post vs pre window; CONFIRMED tag from v3 sweep):

| channel | v3 tag | pre +-30d z_pre median | post +-30d z_pre median | Delta z_pre |
|---|---|---:|---:|---:|
| `stress_mean_sleep` | CONFIRMED-citalopram | -0.077 | -0.715 | -0.639 |
| `all_day_stress_avg` | CONFIRMED-citalopram | -0.169 | -1.349 | -1.180 |
| `bb_lowest` | CONFIRMED-citalopram | +0.787 | +1.574 | +0.787 |
| `stress_stdev_sleep` | non-CONFIRMED | -0.769 | -0.686 | +0.083 |
| `stress_low_motion_min_count_S60_Mlow` | non-CONFIRMED | +0.010 | -0.848 | -0.858 |
| `resting_hr` | non-CONFIRMED | +0.674 | -0.337 | -1.012 |

**Afbouw-reversal Delta-z per channel at 2026-03-20** (raw-medians on unmedicated + consolidation + afbouw pools; reproduces Pattern 2 6-channel direction split per STOCKTAKE sec 6):

| channel | v3 tag | unmed pool med | consolidation pool med | afbouw pool med | Pattern 2 label |
|---|---|---:|---:|---:|---|
| `stress_mean_sleep` | CONFIRMED-citalopram | 19.09 | 19.07 | 20.20 | reversal-below (afbouw crosses baseline in opposite direction) |
| `all_day_stress_avg` | CONFIRMED-citalopram | 34.00 | 31.00 | 34.00 | full-recovery (afbouw returns to unmedicated baseline) |
| `bb_lowest` | CONFIRMED-citalopram | 16.00 | 22.00 | 15.00 | reversal-below (afbouw crosses baseline in opposite direction) |
| `stress_stdev_sleep` | non-CONFIRMED | 8.21 | 6.63 | 6.76 | shift-below-baseline |
| `stress_low_motion_min_count_S60_Mlow` | non-CONFIRMED | 71.00 | 38.00 | 63.00 | shift-below-baseline |
| `resting_hr` | non-CONFIRMED | 55.00 | 57.00 | 61.00 | rise-above-baseline (afbouw shift exceeds unmedicated) |

**resting_hr caveat per Q4.5.b** ([`detrended_correlation/findings.md`](../detrended_correlation/findings.md)): resting_hr drives 5 of 6 trajectory-driven spurious-flagged pairs under linear-OLS detrend (long-memory channel carrying multi-year arc). Per CONVENTIONS sec 3.7: the resting_hr timing-onset detected at this stage may **partly reflect a multi-year arc artefact** rather than a citalopram-specific timing read. Flagged honestly per handoff sec 3.4; the resting_hr ladder rank should be read in light of this caveat. resting_hr is also NOT in the v3 sweep CONFIRMED set; it is included here per the locked 6-channel scope for cross-channel breadth, NOT as a citalopram-candidate channel.

---

## 1. Data prep + z-trajectory substrate

**Corpus**: 6 channels + gevoelscore context + recovery_phase + dose_plasma_mg + derived citalopram_phase. Pre-citalopram pool n=967 day-level rows (date < 2024-04-09); post-citalopram pool n=787.

**Two z-substrates derived**:

- `<channel>_z_pre`: z-score against the pre-citalopram (unmedicated) pool's robust median + MAD scaling. Used for Methods (a) + (c) + the per-channel timeline + heatmap. Centred at the unmedicated baseline so post-citalopram drift is directly visible.
- `<channel>_z_28d`: 28d-trailing-window robust z-score (lag=1 excludes current point; CONVENTIONS sec 3.1 personal-baseline default). Used for the afbouw +-30d window Delta-z read in Stage 5.

Per-channel non-NaN counts in the full corpus:

| channel | n_non_nan |
|---|---:|
| `stress_mean_sleep` | 1707 |
| `all_day_stress_avg` | 1732 |
| `bb_lowest` | 1732 |
| `stress_stdev_sleep` | 1707 |
| `stress_low_motion_min_count_S60_Mlow` | 1739 |
| `resting_hr` | 1731 |

---

## 2. Method (a) threshold-cross results

**Definition**: first day post-2024-04-09 where |z_pre| >= 1.0 sustained for >= 7 consecutive day-rows. **Direction-agnostic**: |z| threshold accepts either sign; the sign of the onset run is reported for transparency + flagged for whether it matches the v3 within-citalopram-traject prior. Direction-agnostic because z_pre is referenced to the unmedicated pool which spans the LC recovery arc (phase 3 + 4a + 4b); the LC recovery trajectory continues across the boundary so the citalopram_modulated phase z_pre direction can be either sign relative to the unmed pool independently of the within-citalopram dose-response direction. A direction filter tied to the v3 prior would misattribute LC-recovery direction to the citalopram boundary. Threshold + sustained-days + direction-agnostic choices documented at the run.py Stage 2 docstring; alternative thresholds (e.g. 0.5 + 14d; 1.5 + 5d) would yield different onsets and are out of scope per the locked operationalisation.

| channel | v3 tag | onset found | onset date | days post t0 | onset sign | matches v3 prior? |
|---|---|:---:|---|---:|---:|:---:|
| `stress_mean_sleep` | CONFIRMED | no | n/a | n/a | n/a | n/a |
| `all_day_stress_avg` | CONFIRMED | yes | 2024-04-27 | 18 | - | no |
| `bb_lowest` | CONFIRMED | yes | 2024-04-24 | 15 | + | no |
| `stress_stdev_sleep` | non-CONFIRMED | no | n/a | n/a | n/a | n/a |
| `stress_low_motion_min_count_S60_Mlow` | non-CONFIRMED | no | n/a | n/a | n/a | n/a |
| `resting_hr` | non-CONFIRMED | yes | 2024-12-24 | 259 | + | yes |

---

## 3. Method (b) PELT/binseg change-point results

**Definition**: per channel, binary segmentation on the 14d-rolling median of the post-2024-04-09 z_pre series; min-segment-size 14d; max-depth 8; reduction-threshold 5%. First change-point date reported (the earliest detected inflection).

| channel | v3 tag | n_smoothed | n_candidates | first change-point | days post t0 |
|---|---|---:|---:|---|---:|
| `stress_mean_sleep` | CONFIRMED | 761 | 37 | 2024-05-11 | 32 |
| `all_day_stress_avg` | CONFIRMED | 772 | 32 | 2024-04-29 | 20 |
| `bb_lowest` | CONFIRMED | 772 | 40 | 2024-05-01 | 22 |
| `stress_stdev_sleep` | non-CONFIRMED | 761 | 8 | 2025-11-22 | 592 |
| `stress_low_motion_min_count_S60_Mlow` | non-CONFIRMED | 777 | 30 | 2024-05-01 | 22 |
| `resting_hr` | non-CONFIRMED | 770 | 38 | 2024-04-29 | 20 |

---

## 4. Method (c) time-to-half-effect (decay fit) results

**Definition**: exponential decay z(t) = z_inf * (1 - exp(-t/tau)) fit on the **28d-rolling median of z_pre** over the post-2024-04-09 180d window. half_effect_days = tau * ln(2). Descriptive SSRI-kinetics PROXY per handoff sec 2 user-locked choice 2c; no CI per CONVENTIONS sec 4.2 + handoff hard constraint -- NOT a substantive mechanism claim about SSRI receptor kinetics.

**Smoothing rationale**: raw daily z_pre is dominated by day-to-day noise at this corpus's autocorrelation horizons (E[L] = 7-30 across the 6 channels per Tier 1+2 spread); a decay fit on raw daily data collapses to tau approximately 1d (an immediate-step interpretation) when asked to explain noisy daily data with a single z_inf + tau pair. Smoothing to 28d-rolling median leaves the slow-scale signal the decay model is designed to capture. tau lower bound = E[L]=7 (project default autocorrelation horizon); sub-E[L] tau would be modelling sub-autocorrelation noise as signal.

**Fit-quality flag**: 'good' = |z_inf| >= 0.1 AND RMSE <= 1.0 AND tau > 7.5d. 'step-like (tau at lower edge; effective step at E[L])' = the smoothed series is best explained by an effective step at the project's autocorrelation horizon; the SSRI-kinetics-proxy interpretation breaks down because the fit is identifying a step, not a graded decay. 'poor (effectively flat z_inf)' = the decay model didn't capture a meaningful pattern. 'poor (high RMSE)' = the model fits the smoothed series with greater than 1 SD residual error.

| channel | v3 tag | n_fit | tau (days) | z_inf | half-effect (days) | RMSE | fit quality |
|---|---|---:|---:|---:|---:|---:|---|
| `stress_mean_sleep` | CONFIRMED | 170 | 7.0 | -0.400 | 4.9 | 0.208 | step-like (tau at lower edge; effective step at E[L]) |
| `all_day_stress_avg` | CONFIRMED | 171 | 7.0 | -0.750 | 4.9 | 0.307 | step-like (tau at lower edge; effective step at E[L]) |
| `bb_lowest` | CONFIRMED | 171 | 7.0 | +0.775 | 4.9 | 0.419 | step-like (tau at lower edge; effective step at E[L]) |
| `stress_stdev_sleep` | non-CONFIRMED | 170 | 7.0 | -0.600 | 4.9 | 0.090 | step-like (tau at lower edge; effective step at E[L]) |
| `stress_low_motion_min_count_S60_Mlow` | non-CONFIRMED | 171 | 7.0 | -0.650 | 4.9 | 0.181 | step-like (tau at lower edge; effective step at E[L]) |
| `resting_hr` | non-CONFIRMED | 171 | 23.4 | -0.400 | 16.2 | 0.260 | good |

---

## 5. Stage 5 per-phase transition analysis -- buildup + afbouw

### 5.1 Buildup-transition at 2024-04-09 (per-channel Delta-z_pre on +-30d windows)

| channel | v3 tag | pre +-30d n | post +-30d n | pre z_pre median | post z_pre median | Delta z_pre |
|---|---|---:|---:|---:|---:|---:|
| `stress_mean_sleep` | CONFIRMED | 29 | 29 | -0.077 | -0.715 | -0.639 |
| `all_day_stress_avg` | CONFIRMED | 30 | 30 | -0.169 | -1.349 | -1.180 |
| `bb_lowest` | CONFIRMED | 30 | 30 | +0.787 | +1.574 | +0.787 |
| `stress_stdev_sleep` | non-CONFIRMED | 29 | 29 | -0.769 | -0.686 | +0.083 |
| `stress_low_motion_min_count_S60_Mlow` | non-CONFIRMED | 30 | 30 | +0.010 | -0.848 | -0.858 |
| `resting_hr` | non-CONFIRMED | 30 | 30 | +0.674 | -0.337 | -1.012 |

### 5.2 Afbouw-reversal at 2026-03-20 (per-channel raw-median on phase pools + +-30d z_28d Delta)

**Reproduces Pattern 2 6-channel afbouw direction split from STOCKTAKE sec 6** + extends with timing per handoff sec 3.3 load-bearing.

| channel | v3 tag | unmed n | unmed med | cons n | cons med | afb n | afb med | Pattern 2 label | +-30d Delta z_28d |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| `stress_mean_sleep` | CONFIRMED | 940 | 19.09 | 627 | 19.07 | 69 | 20.20 | reversal-below (afbouw crosses baseline in opposite direction) | -0.731 |
| `all_day_stress_avg` | CONFIRMED | 954 | 34.00 | 635 | 31.00 | 71 | 34.00 | full-recovery (afbouw returns to unmedicated baseline) | -0.042 |
| `bb_lowest` | CONFIRMED | 954 | 16.00 | 635 | 22.00 | 71 | 15.00 | reversal-below (afbouw crosses baseline in opposite direction) | -0.453 |
| `stress_stdev_sleep` | non-CONFIRMED | 940 | 8.21 | 627 | 6.63 | 69 | 6.76 | shift-below-baseline | -0.914 |
| `stress_low_motion_min_count_S60_Mlow` | non-CONFIRMED | 956 | 71.00 | 634 | 38.00 | 77 | 63.00 | shift-below-baseline | +0.006 |
| `resting_hr` | non-CONFIRMED | 955 | 55.00 | 633 | 57.00 | 71 | 61.00 | rise-above-baseline (afbouw shift exceeds unmedicated) | -2.023 |

**Pattern 2 cross-reference**: STOCKTAKE sec 6 Pattern 2 reports six distinct afbouw patterns on the 2026-03-20 boundary: `all_day_stress_avg` FULLY RECOVERS to unmed baseline; `bb_lowest` REVERSES below unmed baseline; `bb_overnight_gain` NO shift; `stress_stdev_sleep` no reversal; `resting_hr` RISES +4 above baseline; `push_burden_7d_lagged` RISES +1 above baseline; `gevoelscore` NO reversal. Q4.2's Stage 5 reproduces these direction-labels on the 6 channels in this analysis's scope (push_burden_7d_lagged + bb_overnight_gain + gevoelscore are NOT in scope per the user-locked 6-channel choice). The recovery_arc v2 sec 5.A afbouw-reversal LOCKED verdict on the 3 CONFIRMED-citalopram channels (stress_mean_sleep buildup 17.04 -> consolidation 19.07 -> afbouw 20.20; all_day_stress_avg buildup 28.5 -> consolidation 31 -> afbouw 34; bb_lowest buildup 26 -> consolidation 22 -> afbouw 15) is descriptively reproduced + cross-referenced; NOT re-anchored or extended per CONVENTIONS sec 4.2.

---

## 6. Stage 6 cross-channel timing ladder + method-sensitivity

### 6.1 Per-channel onset across 3 methods (raw days post t0; lower = earlier)

| channel | v3 tag | Method (a) onset | Method (b) first CP | Method (c) half-effect | n_disagreement_pairs |
|---|---|---:|---:|---:|---:|
| `stress_mean_sleep` | CONFIRMED | n/a | 32 | 4.9 | 3 |
| `all_day_stress_avg` | CONFIRMED | 18 | 20 | 4.9 | 0 |
| `bb_lowest` | CONFIRMED | 15 | 22 | 4.9 | 2 |
| `stress_stdev_sleep` | non-CONFIRMED | n/a | 592 | 4.9 | 2 |
| `stress_low_motion_min_count_S60_Mlow` | non-CONFIRMED | n/a | 22 | 4.9 | 2 |
| `resting_hr` | non-CONFIRMED | 259 | 20 | 16.2 | 2 |

### 6.2 Per-method ladder rank (1 = earliest; N+1 = no onset)

| channel | v3 tag | rank (a) | rank (b) | rank (c) | stable across methods |
|---|---|---:|---:|---:|:---:|
| `stress_mean_sleep` | CONFIRMED | 7 | 5 | 1 | no |
| `all_day_stress_avg` | CONFIRMED | 2 | 1 | 2 | yes |
| `bb_lowest` | CONFIRMED | 1 | 3 | 3 | no |
| `stress_stdev_sleep` | non-CONFIRMED | 7 | 6 | 4 | no |
| `stress_low_motion_min_count_S60_Mlow` | non-CONFIRMED | 7 | 4 | 5 | no |
| `resting_hr` | non-CONFIRMED | 3 | 2 | 6 | no |

### 6.3 Consensus ranking (mean rank across 3 methods; alphabetical tie-break)

| consensus order | channel | mean rank |
|---:|---|---:|
| 1 | `all_day_stress_avg` | 1.67 |
| 2 | `bb_lowest` | 2.33 |
| 3 | `resting_hr` | 3.67 |
| 4 | `stress_mean_sleep` | 4.33 |
| 5 | `stress_low_motion_min_count_S60_Mlow` | 5.33 |
| 6 | `stress_stdev_sleep` | 5.67 |

**Method-sensitivity headline**: 1 of 6 channels show STABLE rank across all 3 methods (rank diff <=1 on every method-pair); 5 channels DISAGREE on at least one method-pair. Channels where methods agree carry stronger descriptive weight; channels where methods disagree should be read with method-sensitivity in mind. The disagreement reflects channel-specific time-series structure (e.g. long-memory channels can lag Method (a) sustained-threshold-crossing relative to Method (b)'s smoothed inflection-detection; the half-effect fit (c) is sensitive to the post-window length choice).

---

## 7. Cross-references (DESCRIPTIVE corroboration only; NO HA verdict promotion; NO mechanism interpretation; NO promotion of non-CONFIRMED channels to CONFIRMED-citalopram candidacy)

### LOAD-BEARING cross-references

- **`citalopram_dose_response_stress_mean_sleep.md` sec 5.6** (v3 sweep CONFIRMED 3 / REJECTED 1): CONFIRMED channels stress_mean_sleep (+0.43/mg p=0.001) + all_day_stress_avg (+0.57/mg p=0.000) + bb_lowest (-1.13/mg p=0.000). REJECTED channel respiration_avg_sleep (-0.011 p=0.86). Q4.2 extends the v3 picture with a TIMING layer + adds 3 non-CONFIRMED channels (stress_stdev_sleep + stress_low_motion + resting_hr) descriptively. The non-CONFIRMED channels are **NOT promoted to CONFIRMED-citalopram candidacy** per handoff sec 3.4 + sec 4 hard constraint -- that's v3-extension territory and NOT Q4.2 scope.
- **`recovery_arc v2` sec 5.A afbouw-reversal** ([`trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md)): the LOCKED sub-stratification on phase-5 CONFIRMED-citalopram channels surfaces the buildup -> consolidation -> afbouw movement (stress_mean_sleep 17.04 -> 19.07 -> 20.20; all_day_stress_avg 28.5 -> 31 -> 34; bb_lowest 26 -> 22 -> 15). Q4.2's Stage 5 afbouw-reversal table descriptively REPRODUCES + EXTENDS this with timing onset windows around the 2026-03-20 transition + Pattern 2 direction labels. The recovery_arc v2 substantive verdict is NOT re-anchored.
- **STOCKTAKE sec 6 Pattern 2** (6-channel afbouw direction split): full-recovery / reversal-below / no-shift / rise-above / shift-below classifications on the 2026-03-20 boundary. Q4.2's Stage 5 afbouw-reversal table reproduces the direction labels on the 6 channels in this analysis's scope; closes the Pattern 2 cross-channel observation with timing (afbouw +-30d z_28d Delta + first-CP timing per method (b) where post-2026-03-20 CPs fall).
- **Q4.3 `era_boundaries` rp5 strongest-boundary** ([`trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) sec 2): the 2024-04-09 boundary (rp5 / cp1) shows distribution shift on 5 of 7 channels in Q4.3's +-30d window test -- the project's strongest distribution-shift boundary. Q4.2's Stage 5 buildup-transition reproduces this descriptively (per-channel Delta z_pre) on the 6 channels in this analysis's scope. Q4.3's wider-7-channel boundary scan is the methodological backstop; Q4.2 here extends with timing onset.
- **Q4.4 `cohort_topology` rp5/cp3 event-rate decoupling** ([`trajectory/cohort_topology/findings.md`](../cohort_topology/findings.md) sec 2): event rate barely shifts at rp5 (Delta -0.04/30d) even though channel distributions shift substantially; event rate drops at cp3 (Delta -0.85/30d). **HONEST FRAMING for Q4.2**: Q4.2's timing-ladder analysis is on **channel distributions** (the z-trajectory of each channel post-citalopram-start), NOT on crash/dip event rates. The Q4.4 decoupling means Q4.2's per-channel onset findings DO NOT translate into 'the SSRI prevented crashes by N days' or similar event-rate-based claims. Channel-distribution timing and event-rate timing are distinct surfaces; Q4.2 reports on the former.
- **Q4.5.b `detrended_correlation` resting_hr trajectory-driven** ([`trajectory/detrended_correlation/findings.md`](../detrended_correlation/findings.md) sec 6): resting_hr drives 5 of 6 trajectory-driven spurious-flagged pairs under linear-OLS detrend (long-memory channel carrying multi-year arc). **HONEST FRAMING for Q4.2**: the resting_hr timing-onset detected in Q4.2 may **partly reflect a multi-year arc artefact** rather than a citalopram-specific timing read per CONVENTIONS sec 3.7. The resting_hr timing-ladder rank should be read in light of this caveat; flagged in the Limitations section. resting_hr is ALSO not in the v3 CONFIRMED set; it is included here per the locked 6-channel scope for cross-channel breadth, NOT as a citalopram-candidate channel.

### Methodology MDs cited (binding for this analysis's discipline)

- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) sec 5.6 (v3 sweep + CONFIRMED 3 / REJECTED 1 verdict; NOT extended).
- [`methodology/intervention_effects_descriptive.md`](../../../../methodology/intervention_effects_descriptive.md) (canonical citalopram-arc narrative; NOT extended).
- [`methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) sec 3 (5 citalopram-phase definitions + canonical `citalopram_phase()` helper) + sec 4 (CONFIRMED-channel sec 5.A/B/C inheritance; NOT applied here -- descriptive scope does not require dose-adjusted predictors).
- [`methodology/permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) (E[L]=7 default; Method (a) sustained-day threshold = E[L] in alignment with project autocorrelation horizon).
- [`analyses/_utils/frame.py`](../../../_utils/frame.py) (`z_score_vs_rolling_baseline` reference; inline `_rolling_z` matches its semantics with explicit window=28 + lag=1 + robust=True).
- [CONVENTIONS sec 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + sec 3.1 + sec 3.6 + sec 3.7 + sec 4.1 + sec 4.2 + sec 4.3 (descriptive-before-inference; personal baseline; named counts; trajectory-detrend sensitivity; framing discipline; caveat-class; data-driven change-point detection as exploratory only).

### Upstream pipeline

- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` (6 channel columns + date + recovery_phase + dose_plasma_mg + derived citalopram_phase via citalopram_phase_stratification sec 3 helper).

---

## Limitations

For a producer-mode Layer-1 descriptive Strand B integrated-cross-channel analysis (no falsification bar; no causal claim per [CONVENTIONS sec 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + sec 4.1 + sec 4.2 + handoff sec 4 hard constraints), the binding constraints are:

1. **No causal mechanism interpretation of SSRI kinetics** per CONVENTIONS sec 4.1 + sec 4.2 + handoff sec 4 hard constraint. Method (c)'s exponential decay tau + half-effect-days are descriptive SSRI-kinetics PROXY values; they are NOT claims about citalopram receptor up/down-regulation, plasma-PK, or pharmacological half-life. The fit is descriptive; no CI; no model-comparison; no inference.
2. **No 'SSRI hits channel X first' framing** per CONVENTIONS sec 4.2 caveat-class + handoff sec 3.4. Cross-channel timing ladder is descriptive observation ('channel X has earlier onset under Method (a) than channel Y'); NOT causal ordering of where the SSRI acts first.
3. **No promotion of non-CONFIRMED channels to CONFIRMED-citalopram candidacy** per handoff sec 4 hard constraint. stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr were NOT in the v3 sweep CONFIRMED set; they are included here for cross-channel breadth and remain DESCRIPTIVE ONLY. v3-extension to a 6-channel CONFIRMED sweep is OUT-OF-SCOPE here.
4. **resting_hr trajectory-driven caveat per Q4.5.b**: resting_hr drives 5 of 6 trajectory-driven spurious-flagged pairs (per `detrended_correlation/findings.md` sec 6). The resting_hr timing-onset detected here may partly reflect multi-year arc structure rather than a citalopram-specific timing read. Flagged honestly per CONVENTIONS sec 3.7; the resting_hr ladder rank carries this caveat.
5. **Method (a) threshold choice** (|z| >= 1.0 + sustained 7d) is the project-default pairing (1-SD-equivalent against the unmedicated-pool MAD scale + E[L]=7 autocorrelation horizon). Alternative thresholds (0.5 + 14d; 1.5 + 5d) would yield different onsets; sensitivity to this choice is out of scope per the locked operationalisation.
6. **Method (b) PELT/binseg method choice** (binary segmentation over Killick-2012 PELT) was DOCUMENTED at the Stage 3 docstring; same reasons as Q4.3 era_boundaries (parameter-light + interpretable + no library dependency). A future analysis could re-run with PELT proper as a sensitivity arm.
7. **Method (c) decay-fit window length** = 180 days. Shorter windows (e.g. 90d) emphasise early dynamics; longer (e.g. 360d) capture late-asymptote drift. The 180d choice is descriptive-default; not sensitivity-tested here.
8. **Pattern 2 reproduction is on 6 channels, not 7**: STOCKTAKE sec 6 Pattern 2 spans 6 channels + push_burden_7d_lagged + gevoelscore (the latter two NOT in Q4.2's user-locked 6-channel scope). The Pattern 2 direction-labels reported in Stage 5.2 are descriptively consistent with STOCKTAKE for the channels in scope; the absent push_burden_7d_lagged + gevoelscore reads are not recomputed here.
9. **Buildup-transition Delta-z uses z_pre** (vs pre-citalopram pool); **Afbouw-reversal uses raw-medians on phase pools + z_28d on +-30d window**. The two transition reads use DIFFERENT z-substrates because they ask different descriptive questions (the buildup-transition Delta measures the drift from the unmedicated baseline; the afbouw-reversal compares phase pools per Pattern 2 + uses a 28d-rolling z for the local-baseline-relative shift at the boundary). Documented here for transparency.
10. **No HA verdict promotion**: recovery_arc v2 + Q4.3 + Q4.4 + Q4.5.b + citalopram_dose_response v3 LOCKED references are descriptive corroboration only; NONE are extended or re-interpreted per CONVENTIONS sec 4.2 + handoff sec 4 hard constraint.
11. **No methodology MD modifications** + no HA artefact modifications + no per_day_master.csv modifications + no other Strand-A/B analysis modifications per handoff sec 4 hard constraints.
12. **No iteration on the 4 user-locked operationalisation choices** per Strand B sec 7c discipline.

---

*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` (gitignored per `docs/research/**/*.json`). To refresh: `python run.py`.*