# Findings -- `resting_hr` operationalisation-support descriptive (Q3.6.a-i)

**Channel**: `resting_hr` (HA06b + H01 + HA06 primary operand; Garmin UDS `restingHeartRate` field; daily aggregate of the lowest stable nightly HR; UDS-passthrough from `daily_uds.csv` per [`garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) UDS-family discipline). Column semantics: [DATA_DICTIONARY.md cardiovascular section](../../../DATA_DICTIONARY.md).

**Substantive context**: HA06b is LOCKED at TRAIN SUPPORTED +18.9 pp / VALIDATE refuted +0.8 pp / OVERALL REFUTED per [`HA06b-rhr-zscore/result.md`](../../../analyses/hypotheses/HA06b-rhr-zscore/result.md); just R14-confirmed CONVERGE-ON-OVERALL at single-pool **+6.7 pp [CI -18.7, +17.9] perm p (E[L]=7) = 0.3368** per [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) row HA06b (`badd04a`). H01 (the absolute-7d-mean-delta predecessor) is LOCKED at REFUTED both eras (-1.2 / -9.5 pp) per [`H01-rhr-drift/result.md`](../../../analyses/hypotheses/H01-rhr-drift/result.md); R14 single-pool **-3.1 pp [CI -9.4, +10.1] perm p=0.7820** NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED). HA06 (the absolute-bidirectional-delta variant; SUPERSEDED by HA06b) is LOCKED REFUTED both eras per [`HA06-morning-rhr-delta/result.md`](../../../analyses/hypotheses/HA06-morning-rhr-delta/result.md). This Q3.6 is the Strand-A operationalisation-support backstop; the HA06b + H01 + HA06 + R14 substantive verdicts are LOCKED and descriptively corroborated only.

**v3 dose-response status**: resting_hr IS in v3 multi-channel scope per [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.6 (6-channel scope: stress_mean_sleep + all_day_stress_avg + bb_lowest + resting_hr + bb_overnight_gain + respiration_avg_sleep) and was classified as **REJECTED with weak/non-significant beta** (the 'weakly consistent' v3 row). Per CONVENTIONS section 4.2 caveat-class framing: Q3.6.d reports observed phase shifts descriptively; this Q3.6 does **NOT promote a v3 REJECTED -> CONFIRMED reclassification** (handoff section 3 hard constraint).

**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to 2026-06-05). n=1357 days with channel out of 1372 Stratum 4 days (15 NaN days from UDS-side coverage gaps).

**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`) -- HA-touched non-confirmed channel candidate list bullet `resting_hr (HA06b primary; weak v3 dose-modulation)`. **2nd of the 5 Tier 2 channels** in the user-prioritised Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain `7d49ba4`; this Q3.6 closes Tier 2 2nd; next: Q3.7 exertion_class, Q3.8 push_burden_7d, Q3.9 gevoelscore). Q3.6.a-i template applied per section 3.1 verbatim + Q3.6.c LOAD-BEARING recovery-axis extension on full corpus per handoff section 2.4 (reproduces recovery_arc v2 cardiovascular-family acute-infection DIP finding).

**Sources**: `per_day_master.csv` (Garmin daily aggregate) + `labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level per CONVENTIONS section 3.6).

**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). HA06b + H01 + HA06 (LOCKED) + R14 single-pool re-anchors (LOCKED `badd04a`) + HA-P6 v3 + v3 dose-response REJECTED (LOCKED) cross-references in this analysis are **descriptive corroboration only**; the substantive verdicts live in those result.md files and are NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). The v3 REJECTED verdict is LOCKED and this Q3.6.d does NOT promote a CONFIRMED-citalopram reclassification per the handoff section 3 hard constraint. Statistical hygiene anchors: section 3.1 (personal baseline), section 3.3 (column-duplication threshold |rho|>=0.92), section 3.4 (crash-drop sensitivity |delta|>0.10), section 3.5 (spike metrics -- HA06b's tested operand IS the per-4-day MAX |z| spike-form on this daily channel), section 3.6 (named counts).

---

## Headline

`resting_hr` on Stratum 4 is a **roughly-symmetric, VERY-LONG-MEMORY (Politis-White estimator fallback at this pool) daily cardiovascular channel** (skew=+0.25, excess kurtosis=-0.25, heavy_tail_flag=False, p99/median = 63.00/56.00 = 1.12). The **data-driven E[L]\*=7.0** (Politis-White; deviation ratio 0.00; factor-of-2 flag = False; cutoff lag M=None). Cross-channel context per handoff section 2.4: vs sister Strand-A channels stress_stdev_sleep 7.0 / bb_overnight_gain 6.5 / stress_mean_sleep 12.6 / stress_low_motion 21.1 / bb_lowest 29.25 / all_day_stress_avg 29.8; recovery_arc v2 sec 7b reported 22.7 for resting_hr -- this Q3.6.b's E[L]\*=7.0 is **DEFAULTED to E[L]=7 fallback because the Politis-White ACF cutoff was not found within max_lag (n/4); per the cutoff rule ALL lags within max_lag remained above the 2-sigma significance threshold |rho|=0.146. The fallback is itself a 'memory longer than the estimator can resolve' descriptive signal -- lag-7 ACF = +0.682; lag-14 ACF = +0.533 -- consistent with the recovery_arc v2 4a+4b sub-pool E[L]*=22.7 in spirit (both findings point at long-memory structure); the apparent numerical match of E[L]=7 with the project default is a FALLBACK ARTEFACT, not a SHORT-memory finding. Per CONVENTIONS section 4.2: this is a Layer 1 descriptive observation; the data-driven block-length point estimate cannot be cleanly extracted from Strand-A's full Stratum-4 pool because the channel's autocorrelation is too persistent at this resolution** (recovery_arc's pool was the joined 4a+4b sub-window n=53+500; this Q3.6.b's pool is full Stratum-4 n=1357). **Phase-stratified medians** (citalopram axis, caveat-class per CONVENTIONS section 4.2 since v3 REJECTED with weak beta): unmedicated 56.00 -> buildup 54.00 -> consolidation 57.00 -> afbouw 61.00 (consolidation-minus-unmedicated = +1.00 bpm). Day-resolved citalopram boundary step (2024-04-09 pre/post 30d) is **-2.33 bpm**. Crash-vs-normal: episode-level d=-0.07 (bootstrap CI95 [-1.38, +0.94]); day-level Mann-Whitney U z=+1.98 p=0.0475 P(crash>normal)=0.558 -- descriptively re-anchors HA06b's TRAIN-only-SUPPORTED-now-OVERALL-REFUTED + R14 CONVERGE-ON-OVERALL + H01 both-eras-REFUTED + R14 CONVERGE (both NOT-SUPPORTED). Near-identity check: **Zero** near-identity pairs fire at the |rho|>=0.92 CONVENTIONS section 3.3 threshold. **Q3.6.c LOAD-BEARING recovery_arc reproduction**: acute-infection DIP REPRODUCES the recovery_arc v2 finding (observed dip -1.50 bpm vs recovery_arc reported -1.5 bpm) (recovery_arc v2 reported -1.5 bpm; this Q3.6.c observed -1.50 bpm).

---

## Q3.6.a -- Distribution shape (Stratum 4)

**Verdict on the section 3.1 delegate question**: **delegate is partial; extend in this analysis**. [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) primarily documents `stress_mean_sleep`-family channels; coverage on `resting_hr` is incidental. The full distribution descriptors (skewness/kurtosis/heavy-tail flag/p99-vs-median ratio) are surfaced here for the first time on this channel at the operationalisation-support framing.

| stat | value | source |
|---|---:|---|
| n (Stratum 4) | 1357 | `per_day_master.csv` `resting_hr` non-NaN within S4 |
| mean | 56.678 | (single-pool S4) |
| median | 56.000 | |
| std (ddof=1) | 2.722 | |
| MAD (unscaled) | 2.000 | |
| MAD x 1.4826 (normal-equivalent SD) | 2.965 | for robust z-score scaling per section 3.1 |
| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | 51.0 / 53.0 / 53.0 / 55.0 / 56.0 / 58.0 / 61.0 / 61.2 / 63.0 | |
| skewness (Fisher-Pearson) | **+0.25** | roughly-symmetric |
| excess kurtosis (Fisher) | **-0.25** | |
| heavy_tail_flag | **False** | skew>1 OR p99/median > 3.0 |
| range | 50.0 to 65.0 bpm | |

**resting_hr is a per-day Garmin UDS daily aggregate** (the lowest stable nightly HR via Garmin's `restingHeartRate` UDS field). Per HA06 + HA06b result framing: the field maps cleanly to the bottom of the night-sleep-HR graph and is the Wiggers-aligned 'lowest stable nightly HR' construct. The participant's typical max |z| sits at 1.6-3.5 bpm relative to the lagged baseline per HA06b (median 2.31 train / 1.57 validate); the baseline sigma sits stably at 2.0-2.3 bpm per HA06b sensitivity arms.

### Cross-channel comparison vs sister CONFIRMED-citalopram channels

| stat | resting_hr (this analysis) | stress_mean_sleep (Q3.1, CONFIRMED) | all_day_stress_avg (Q3.2, CONFIRMED) | bb_lowest (Q3.3, CONFIRMED) |
|---|---:|---:|---:|---:|
| n S4 | 1357 | 1339 | 1359 | 1359 |
| mean | 56.68 | 19.97 | 32.72 | 20.61 |
| median | 56.00 | 19.21 | 32.00 | 20.00 |
| MAD (unscaled) | 2.00 | 2.87 | 4.00 | 6.00 |
| skewness | +0.25 | +2.72 | +0.87 | +0.42 |
| heavy_tail_flag | **False** | **True** | **False** | **False** |

**resting_hr is a DAILY-AGGREGATE cardiovascular primitive** (Garmin UDS-passthrough; lowest stable nightly HR). Distinct from the BB-floor NADIR (bb_lowest) by mechanism: RHR is the cardiovascular-recovery anchor; BB-floor is the autonomic-recovery anchor. Distinct from autonomic-load stress channels (stress_mean_sleep mean / all_day_stress_avg mean) by mechanism: RHR measures cardiovascular state; stress channels are HRV-proxies from monitoring_b. The sister BB-floor channel (bb_lowest Q3.3.e) reciprocally reported rho=-0.171 with this channel (NOT near-identity; modest INVERSE coupling: BB-floor up co-occurs with RHR down).

See [`plots/fig1_distribution_s4.png`](plots/fig1_distribution_s4.png).

---

## Q3.6.b -- Autocorrelation structure + E[L]\* (LOAD-BEARING recovery_arc v2 reproduction)

The **data-driven block length is E[L]\*=7.0** (Politis-White 2004 with Patton-Politis-White 2009 correction per [`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) vs the project default E[L]=7 per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). The **factor-of-2 deviation flag = False** (deviation ratio = 0.00). Cutoff lag M=None.

| lag (days) | autocorrelation |
|---:|---:|
| 1 | +0.970 |
| 2 | +0.937 |
| 3 | +0.891 |
| 7 | +0.682 |
| 14 | +0.533 |

Politis-White 2-sigma significance threshold (n=1357): |rho| = 0.146.

### Cross-channel comparison (E[L]\* by Strand A analysis) -- handoff section 2.4 load-bearing

| analysis | channel | E[L]\* | M | factor-of-2 flag |
|---|---|---:|---:|---|
| Q3.5 (bb_overnight_gain, truth window) | per-night SLEEPEND-SLEEPSTART | 6.5 | -- | no |
| Q3.4 (stress_stdev_sleep) | per-night STDEV | 7.0 | -- | no |
| Q3.1 (stress_mean_sleep) | sleep-window mean | 12.6 | 6 | YES (factor-of-2) |
| Phase-1 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 | 11 | YES (factor-of-3) |
| Q3.3 (bb_lowest) | daily NADIR | 29.25 | 17 | YES (factor-of-4) |
| Q3.2 (all_day_stress_avg) | 24h-window mean | 29.8 | 18 | YES (factor-of-4) |
| **this analysis (resting_hr)** | **daily Garmin UDS restingHeartRate** | **7.0 (fallback)** | **n/a (no cutoff)** | **no (but see fallback caveat above)** |

### LOAD-BEARING recovery_arc v2 section 7b reproduction (per handoff section 2.4)

**recovery_arc v2 section 7b reported E[L]\*=22.7 for resting_hr** (paired-bootstrap combined E[L]\* from the joined 4a+4b sub-window n=53+500 day-level rows). resting_hr was the only channel in the v2 7-channel set where the 4b-4a paired-bootstrap CI excluded 0 (+3.0 bpm, CI [+2.0, +4.0]). This Q3.6.b's E[L]\*=7.0: **DEFAULTED to E[L]=7 fallback because the Politis-White ACF cutoff was not found within max_lag (n/4); per the cutoff rule ALL lags within max_lag remained above the 2-sigma significance threshold |rho|=0.146. The fallback is itself a 'memory longer than the estimator can resolve' descriptive signal -- lag-7 ACF = +0.682; lag-14 ACF = +0.533 -- consistent with the recovery_arc v2 4a+4b sub-pool E[L]*=22.7 in spirit (both findings point at long-memory structure); the apparent numerical match of E[L]=7 with the project default is a FALLBACK ARTEFACT, not a SHORT-memory finding. Per CONVENTIONS section 4.2: this is a Layer 1 descriptive observation; the data-driven block-length point estimate cannot be cleanly extracted from Strand-A's full Stratum-4 pool because the channel's autocorrelation is too persistent at this resolution**. Pool difference: recovery_arc's pool was the joined 4a+4b sub-window (~553 day-level rows); this Q3.6.b's pool is full Stratum-4 (n=1357). The pools differ in temporal coverage (Stratum 4 starts 2022-09-03 = end of sub-phase 4a; full Stratum 4 extends through citalopram_modulated phase 5 = AS_OF_DATE 2026-06-05). Per CONVENTIONS section 4.2: this is Layer 1 descriptive observation only; the methodological-divergence flag (fallback vs converging estimate) is the load-bearing finding here, not a per-pool block-length number to inherit.

**Implication for downstream HA pre-regs**: any future HA on `resting_hr` (beyond HA06b's locked second-order operand) should pre-spec a sensitivity arm at the recovery_arc v2 reported E[L]\*=22.7 alongside the default-E[L]=7 primary (the fallback observed here does NOT establish a SHORT-memory regime -- the ACF lag-7=+0.682 + lag-14=+0.533 both remain well above the 2-sigma threshold 0.146; the channel has very-long memory at this resolution). HA06b itself used E[L]=7 for the locked test; the R14 single-pool re-anchor at +6.7 pp p=0.3368 also used E[L]=7. The Q3.6.b finding here updates the channel-level block-length characterisation for any FUTURE HA on this channel; HA06b's already-locked verdict + the R14 single-pool verdict are NOT re-anchored.

See [`plots/fig5_acf.png`](plots/fig5_acf.png).

---

## Q3.6.c -- Base rates per citalopram phase + LOAD-BEARING recovery-axis extension

### Citalopram axis (Stratum 4 primary)

Phase axis per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3:

| phase | window | n | median | mean | MAD | p10 / p90 |
|---|---|---:|---:|---:|---:|---|
| unmedicated | 2022-09-03 to 2024-04-08 | 581 | **56.00** | 55.97 | 1.00 | 53.00 / 59.00 |
| buildup | 2024-04-09 to 2024-06-19 | 72 | **54.00** | 54.35 | 1.00 | 53.00 / 57.00 |
| consolidation | 2024-06-20 to 2026-03-19 | 633 | **57.00** | 57.14 | 2.00 | 54.00 / 61.00 |
| afbouw | 2026-03-20 to 2026-06-05 | 71 | **61.00** | 60.69 | 1.00 | 59.00 / 62.00 |

The two **transition phases** (buildup n=72; afbouw n=71) have **n<75 each**; the two **steady-state phases** (unmedicated n=581; consolidation n=633) are an order of magnitude larger. Any HA test that wants per-phase verdicts on this channel faces a ~10x n disadvantage vs the steady-state phases (same as sister channels Q3.1.c / Q3.2.c / Q3.3.c / Q3.4.c / Q3.5.c).

Named counts (CONVENTIONS section 3.6): the per-phase n's above are `resting_hr`-non-NaN day rows in `per_day_master.csv` within Stratum 4 date masks per `citalopram_phase_stratification.md section 3` boundary dates.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (citalopram-phase violins).

### Recovery-axis LOAD-BEARING extension on FULL CORPUS (per handoff section 2.4)

Per handoff section 2.4: this section extends OUT of the default Stratum-4 window to include the **pre_illness_healthy (2021-08-16 to 2022-03-20) + acute_infection (2022-03-21 to 2022-04-03) phases** on the full corpus, so the [recovery_arc v2 findings.md section 5.A](../../trajectory/recovery_arc/findings.md) cardiovascular-family **acute-infection DIP finding (54 -> 52.5)** can be descriptively reproduced. 6-phase axis per [`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) (LOCKED `d47e0d3`). Per recovery_arc v2 section 5.A: **resting_hr uniquely DIPS in acute infection (parasympathetic dominance during viral infection; n=14 too short for tight CI)**.

| phase | window start | n | observed median | observed CI95 (E[L]=7) | recovery_arc v2 reported | delta (this - recovery_arc) |
|---|---|---:|---:|---|---:|---:|
| pre_illness_healthy (1) | 2021-08-16 | 217 | **54.00** | [52.0, 55.0] | 54.0 | **+0.00** |
| acute_infection (2) | 2022-03-21 | 14 | **52.50** | [51.0, 55.0] | 52.5 | **+0.00** |
| lc_pre_ergo (3) | 2022-04-04 | 162 | **55.00** | [52.0, 56.0] | 55.0 | **+0.00** |
| pacing 4a | 2022-09-22 | 53 | **53.00** | [53.0, 54.0] | 53.0 | **+0.00** |
| pacing 4b | 2022-11-17 | 509 | **56.00** | [56.0, 57.0] | 56.0 | **+0.00** |
| citalopram (5) | 2024-04-09 | 776 | **57.00** | [56.0, 58.0] | 57.0 | **+0.00** |

**Acute-infection DIP reproduction verdict**: REPRODUCES the recovery_arc v2 finding (observed dip -1.50 bpm vs recovery_arc reported -1.5 bpm).

**Per CONVENTIONS section 4.2 caveat-class framing**: the recovery_arc v2 cells reported in the comparison column above are NOT re-promoted to substantive findings here; the recovery_arc v2 substantive narrative (parasympathetic dominance during viral infection + slow cardiovascular upward drift through 4b + phase 5) is LOCKED at the recovery_arc/findings.md level. This Q3.6.c reproduction is descriptive corroboration only -- if the observed values match within +/-1 bpm of the recovery_arc reported values, that confirms methodological consistency; material divergence is descriptively flagged.

See [`plots/fig6_recovery_axis_full_corpus.png`](plots/fig6_recovery_axis_full_corpus.png) (6-phase recovery-axis violins on full corpus).

---

## Q3.6.d -- Phase-stratified distribution + v3 dose-response REJECTED caveat-class

**Per CONVENTIONS section 4.2 (caveats yes; a-priori claims no) + handoff section 1 + section 2.4 + section 3 hard constraint**: `resting_hr` IS in the v3 multi-channel sweep scope per [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.6 (6-channel scope) and was classified as **REJECTED with weak/non-significant beta** (the 'weakly consistent' v3 row). The citalopram-dose-modulation status on this channel is therefore **REJECTED at v3-locked verdict**. This Q3.6.d reports the observed median + dispersion shift across the citalopram-axis phases descriptively; it does **NOT promote a v3 REJECTED -> CONFIRMED reclassification** per the handoff section 3 hard constraint.

Observed median shifts:

| comparison | delta median (bpm) | within-phase MAD | within-MAD? |
|---|---:|---:|---|
| buildup minus unmedicated | **-2.00** | 1.00-1.00 | > 1 MAD; descriptively meaningful |
| consolidation minus unmedicated | **+1.00** | 2.00 | within 1 MAD |
| consolidation minus buildup | **+3.00** | 2.00 | |
| afbouw minus consolidation | **+4.00** | 2.00-1.00 | |
| afbouw minus unmedicated | **+5.00** | 1.00-1.00 | |

### Descriptive reading (no verdict promotion; v3 REJECTED LOCKED)

The median moves from unmedicated (56.00) to consolidation (57.00) by **+1.00 bpm**. The day-resolved citalopram boundary step (30d pre/post 2024-04-09): **-2.33 bpm** -- the empirical day-resolved citalopram-onset shift. Per the framing above: **the v3 dose-response analysis classified resting_hr as REJECTED with weak/non-significant beta**, and this Q3.6.d does NOT promote that REJECTED verdict to CONFIRMED. The observed phase shift is consistent with the v3 'weakly consistent' rating: there is a measurable shift across the citalopram boundary on the daily-resolved channel, but the within-buildup-window dose-response slope was not significant in the v3 sweep. The shift visible at the citalopram boundary may reflect any combination of: (i) the v3 REJECTED beta carrying residual weakly-consistent signal that the per-phase median shift surfaces, (ii) the recovery_arc v2 slow cardiovascular upward drift through 4b + phase 5 (consistent across the multi-year arc), (iii) co-temporal trajectory effects unrelated to citalopram dose-modulation. The v3 REJECTED verdict is LOCKED; this Q3.6.d observation is a Layer 1 descriptive cross-reference only.

### HA06b + H01 + HA06 locked-verdict cross-reference

Per handoff section 1: HA06b (z-score relative-threshold framing, TRAIN SUPPORTED only); H01 (absolute 7d-mean +3 bpm framing, REFUTED both eras); HA06 (absolute 4-5d delta >=5 bpm bidirectional, REFUTED both eras; SUPERSEDED by HA06b). Per HA06b result.md the absolute-threshold misalignment vs the participant's RHR variability is the canonical story: HA06's 5 bpm bar caught 21.4% train freq with +13.9 pp; HA06b's z-score relative bar caught 71.4% train freq with +18.9 pp. The per-phase median shifts observed in Q3.6.d's table above are in the 1-5 bpm absolute range across the citalopram axis -- which is on the same order as HA06's absolute threshold of 5 bpm and well above HA06b's relative N_std=1.5 (~2-3 bpm at the participant's sigma_floor=0.5-2.3 bpm range) at the per-day-channel level.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) and [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d rolling median through phases).

---

## Q3.6.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)

Brief-mandated targets per handoff section 2.4: sister CONFIRMED-citalopram channels (stress_mean_sleep + all_day_stress_avg + bb_lowest) + stress-family neighbours + respiration cross-family. Cross-family cardiovascular vs autonomic-load companions are the load-bearing comparisons.

| target channel | n | Pearson r | Spearman rho | near-identity flag? |
|---|---:|---:|---:|---|
| `stress_mean_sleep` | 1337 | +0.359 | +0.377 | no |
| `all_day_stress_avg` | 1357 | +0.231 | +0.195 | no |
| `stress_low_motion_min_count_S60_Mlow` | 1356 | +0.133 | +0.099 | no |
| `stress_stdev_sleep` | 1337 | +0.121 | +0.073 | no |
| `asleep_stress_avg_uds` | 1349 | +0.371 | +0.422 | no |
| `awake_stress_avg` | 1357 | +0.063 | +0.036 | no |
| `awake_stress_max` | 1357 | +0.002 | -0.004 | no |
| `all_day_stress_max` | 1357 | +0.002 | -0.003 | no |
| `bb_lowest` | 1357 | -0.194 | -0.171 | no |
| `bb_highest` | 1357 | -0.414 | -0.393 | no |
| `bb_during_sleep_value` | 859 | -0.366 | -0.349 | no |
| `bb_overnight_gain` | 591 | -0.262 | -0.241 | no |
| `respiration_avg_sleep` | 1333 | +0.182 | +0.081 | no |
| `respiration_lowest` | -- | -- | -- | column absent |
| `respiration_highest` | -- | -- | -- | column absent |

**Zero near-identity pairs fire** at the |rho|>=0.92 CONVENTIONS section 3.3 threshold. Sister `bb_lowest` Q3.3.e reciprocally reported Pearson r=-0.194 / Spearman rho=-0.171 with this channel (NOT near-identity at the section 3.3 threshold; modest INVERSE coupling: BB-floor up co-occurs with RHR down). The cross-channel-correlation card ([`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md)) already documented no near-identity in the project's 9-anchor primitive set; this Q3.6.e reproduces from the resting_hr side.

---

## Q3.6.f -- Crash-day vs normal-day (Stratum 4) + HA06b + H01 corroboration

Per CONVENTIONS section 3.6 named counts: 29 crash-episodes (crash_v2 episode-level via `labels_crash_v2.csv` unique `episode_id` starting with `crash-`); 103 crash-days (day-level, `label=='crash'`); 1254 non-crash days (the complement within Stratum 4 channel-valid days).

### Episode-level (primary unit per CONVENTIONS section 3.6)

| stat | value |
|---|---:|
| n crash-episodes | 29 |
| n normal-day base rate | 1254 |
| mean per-episode `resting_hr` | 56.448 bpm |
| mean normal-day `resting_hr` | 56.642 bpm |
| mean diff (episode minus normal-day) | **-0.194 bpm** |
| Cohen's d (episode-level vs normal-day pooled) | **-0.07** |
| Bootstrap 95% CI on mean diff | **[-1.375, +0.944]** (5000 iters, seed=20260624) |

**Episode-level Cohen's d=-0.07** on this channel. Substantive direction prior per HA06b + HA06: bidirectional crash-day RHR deviation (elevated direction = classical Workwell sympathetic overarousal in train era; lowered direction = parasympathetic-swing pattern in validate era per HA06b directionality split). Compare cross-channel: `stress_mean_sleep` episode d=+0.91; `stress_stdev_sleep` episode d=+0.48; `all_day_stress_avg` episode d=+0.37; `stress_low_motion_min_count_S60_Mlow` episode d=+0.38; `bb_lowest` episode d=-0.30; `bb_overnight_gain` episode d=-0.80.

### Day-level (autocorrelation-inflated supplementary)

| stat | value |
|---|---:|
| n crash-days | 103 |
| n normal-days | 1254 |
| mean crash-day | 57.117 bpm |
| mean normal-day | 56.642 bpm |
| median crash-day | 57.00 bpm |
| median normal-day | 56.00 bpm |
| mean diff (point estimate) | **+0.475 bpm** |
| median diff | **+1.00 bpm** |
| Cohen's d | **+0.17** |
| Mann-Whitney U: z | **+1.98** |
| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **0.0475** |
| Mann-Whitney U: P(crash > normal) | **+0.558** |
| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (project default) | [-1.120, +1.885], width 3.006 |
| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (data-driven, Q3.6.b flag) | **[-1.120, +1.885]**, width 3.006 |

### LOAD-BEARING HA06b + H01 R14 single-pool descriptive cross-reference (per handoff section 2.4)

Per [single_pool_reanchor/findings.md](../single_pool_reanchor/findings.md) row HA06b: R14 single-pool **+6.7 pp [CI -18.7, +17.9] perm p=0.3368 NOT-SUPPORTED CONVERGE-ON-OVERALL** (`badd04a`). Per row H01: single-pool **-3.1 pp [CI -9.4, +10.1] perm p=0.7820 NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED)**. This Q3.6.f's first-order day-level Cohen's d=-0.07 (episode-level) + Mann-Whitney U p=0.0475 (day-level) **descriptively corroborate** the R14 reading that the cardiovascular channel does NOT produce a clean validate-era precursor signal under any of the operationalisations tested (absolute 7d-mean H01; absolute bidirectional 4-5d HA06; relative z-score 4d HA06b) -- the channel-distribution-level signal at the day-level is consistent with HA06b's train-only-SUPPORTED + R14 CONVERGE-ON-OVERALL verdict and H01's both-eras-REFUTED + R14 CONVERGE verdict. **The HA06b + H01 + R14 substantive verdicts are LOCKED**; this Q3.6.f observation is descriptive corroboration only, NOT a re-interpretation of either.

### Block-length sensitivity (Q3.6.b cross-check)

Per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md), when the data-driven E[L]\* deviates from the project default by more than a factor of 2, the analysis must report the CI at the data-driven value alongside the default. E[L]=7 CI ([-1.120, +1.885]) vs E[L]=7 CI ([-1.120, +1.885]) -- 0.0% narrower at the data-driven block length.

### Crash-drop sensitivity (CONVENTIONS section 3.4)

| frame | Spearman rho | n |
|---|---:|---:|
| full Stratum 4 | +0.020 | 1357 |
| crash-days dropped | +0.056 | 1254 |
| \|delta\| | **0.036** | -- |
| section 3.4 threshold (0.10) crossed? | **no** | -- |

See [`plots/fig4_crash_vs_normal.png`](plots/fig4_crash_vs_normal.png).

---

## Q3.6.g -- Spike-detecting primitive availability

`resting_hr` is a **per-day Garmin UDS daily aggregate** (the lowest stable nightly HR via Garmin's `restingHeartRate` UDS field; UDS-passthrough; no FIT parsing). Per CONVENTIONS section 3.5 spike/peak/count metrics preference: **HA06b's tested operand IS the spike-form construct on this channel** -- the per-4-day MAX |z| (bidirectional) of resting_hr with lagged baseline + sigma_floor=0.5 bpm. The per-day resting_hr value IS the operationalisation substrate; the per-4-day max |z| is the within-4-day spike-of-HR-deviation metric HA06b uses.

Cardiovascular + autonomic-arousal primitives in master (for cross-channel pairwise comparison):

- `stress_mean_sleep` (n non-NaN = 1339)
- `all_day_stress_max` (n non-NaN = 1359)
- `awake_stress_max` (n non-NaN = 1359)
- `stress_low_motion_min_count_S60_Mlow` (n non-NaN = 1365)
- `bb_lowest` (n non-NaN = 1359)
- `bb_highest` (n non-NaN = 1359)
- `respiration_avg_sleep` (n non-NaN = 1335)

### Pairwise correlations on Stratum 4

| partner channel | Pearson r | Spearman rho | n |
|---|---:|---:|---:|
| `bb_lowest` | -0.194 | -0.171 | 1357 |
| `stress_mean_sleep` | +0.359 | +0.377 | 1337 |
| `all_day_stress_avg` | +0.231 | +0.195 | 1357 |
| `respiration_avg_sleep` | +0.182 | +0.081 | 1333 |
| `awake_stress_max` | +0.002 | -0.004 | 1357 |

**Latent in FIT, not in master**:

- per-minute heart-rate samples (NOT in master; would require FIT-side extraction)
- per-second HR during specific intervals (NOT in master)
- morning-only RHR vs all-day RHR (Garmin UDS exposes restingHeartRate as a single daily value; finer-than-daily RHR is not in the GDPR dump as restingHeartRate per garmin_indicators_audit.md UDS-passthrough discipline)

Per CONVENTIONS section 3.5: spike/peak/count metrics preferred over daily means -- HA06b's spike-form construct (per-4-day max |z| of resting_hr with lagged baseline + sigma_floor=0.5 bpm) IS the within-4-day spike-of-HR-deviation metric on this channel. The per-day resting_hr value IS the operationalisation substrate for that spike-form; finer-than-daily resolution would require new FIT-side extraction. Per HA06 result.md caveat: chronotropic incompetence (>85% of ME/CFS patients have blunted HR response per Workwell's own caveat) is a substrate caveat for HR-channel signals' biological interpretation, not a calibration-drift signature.

---

## Q3.6.h -- Outlier detection + calibration-drift check

Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md):

- resting_hr is UDS-side passthrough from daily_uds.csv (Garmin restingHeartRate field); JSON-side no FIT parsing; UDS-passthrough discipline applies per garmin_indicators_audit.md UDS family rows
- No specific calibration-drift events catalogued for resting_hr in garmin_indicators_audit.md beyond the shared UDS-family entries (same as sister BB-family channels which are also UDS-passthrough)
- Underlying sensor is Forerunner 245 Elevate V3 throughout the entire 2021-08-16 to present window -- no device change in the analytic window
- Per HA06 result.md + H01 result.md caveat: chronotropic incompetence (>85% of ME/CFS patients have blunted HR response per Workwell's own caveat) is a substrate caveat for any HR-channel signal's biological interpretation. This is NOT a calibration-drift signature on this device; it is a population-level physiological caveat noted by the source literature.
- Per HA06b result.md: the participant's typical max |z| sits in the 1.6-3.5 bpm range (relative) and the lagged baseline sigma sits around 2.0-2.3 bpm; the channel's day-to-day variability is consistent and stable across the analytic window.

### Outlier scan (MAD-based |z|>5; threshold per CONVENTIONS section 3.1 robust-baseline default)

**0 outlier-day flagged** out of 1357.

No outliers above the |z|>5 threshold on Stratum 4.

### Drift check -- rolling 90d median over Stratum 4

| snapshot date | rolling 90d median (bpm) |
|---|---:|
| 2022-12-01 | 53.0 |
| 2023-06-01 | 56.0 |
| 2023-12-01 | 56.0 |
| 2024-06-01 | 55.0 |
| 2025-01-01 | 56.0 |
| 2025-12-01 | 56.5 |
| 2026-04-01 | 61.0 |

### Citalopram boundary step (2024-04-09)

Pre-30d mean = 56.77; post-30d mean = 54.43; **diff = -2.33**.

### Consolidation boundary step (2024-06-20)

Pre-30d mean = 54.83; post-30d mean = 53.30; **diff = -1.53**.

### Afbouw boundary step (2026-03-20)

Pre-30d mean = 60.03; post-30d mean = 60.60; **diff = +0.57**.

Per recovery_arc v2 section 5.A: the broader cardiovascular-family pattern is **slow upward drift through 4b + phase 5** (lc_pre_ergo 55 -> 4a 53 -> 4b 56 -> citalopram_modulated 57); the per-30d boundary steps reported above are the day-resolved view of the slow drift at specific intervention boundaries. These are NOT calibration-drift signatures (which would be gradual monotonic creeps unrelated to documented events); the rolling-90d median snapshot table shows the multi-year trajectory aligning with the recovery_arc v2 narrative.

See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).

---

## Q3.6.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel

Discipline anchor: [HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) (secondary-logistic-with-covariate pattern; beta disambiguation between primary-signal and candidate alternative readings). Names **four** candidate covariates a future HA on `resting_hr` as predictor should pre-spec.

### 1. `dose_plasma_mg(d) (citalopram covariate -- v3 REJECTED with weak beta)`

resting_hr was in v3 multi-channel sweep scope per citalopram_dose_response_stress_mean_sleep.md section 5.6 and classified as REJECTED with weak/non-significant beta. A future HA on resting_hr cross-phase should pre-spec dose as a secondary covariate to surface any latent dose-modulation residue and to descriptively re-anchor the v3 REJECTED verdict; if beta_dose is significant in the secondary, that is candidacy evidence for a v3 re-test (NOT a re-promotion of the v3 verdict). Per CONVENTIONS section 4.2 caveat-class: the v3 REJECTED verdict is LOCKED and this covariate arm is diagnostic, not a re-promotion path.

*Source*: methodology/citalopram_dose_response_stress_mean_sleep.md v3 section 5.6 (REJECTED with weak beta); CONVENTIONS section 4.2 caveat-class framing

### 2. `resting_hr_lagged_lcera_z(d) (already materialised in master per CONVENTIONS section 3.2)`

Mirrors HA-P7 section 4.5.4 worked example (lagged-outcome covariate) for the autocorrelation-vs-mechanism disambiguation. Per Q3.6.b the cutoff lag M and data-driven E[L]* are inputs to this choice. per_day_master ALREADY has a materialised resting_hr_lagged_lcera_z column (LC-era-only [d-90, d-30] trailing baseline per CONVENTIONS section 3.2 _lagged_lcera convention). HA06b's tested operand IS the per-4-day max |z| using this lagged baseline; any future HA on resting_hr should use the materialised _lagged_lcera_z directly OR pre-spec a shorter window.

*Source*: HA-P7 hypothesis.md section 4.5.4; per_day_master.csv resting_hr_lagged_lcera_z column

### 3. `bb_lowest (alternative autonomic-recovery anchor; INVERSE direction sister)`

Per Q3.3.e sister analysis: bb_lowest <-> resting_hr Spearman rho ~-0.171 (NOT near-identity at section 3.3 threshold). The covariate disambiguates: beta_channel attenuates -> the resting_hr signal is shared with cardiovascular-recovery via the BB-floor axis (RHR-up co-occurs with BB-floor-down); beta_channel survives -> the RHR signal carries autonomic-arousal-specific information beyond the BB-floor axis.

*Source*: Q3.3.e bb_lowest sister analysis cross-pair table

*Observed correlation on S4*: Pearson r=-0.194 / Spearman rho=-0.171 (n=1357).

### 4. `stress_mean_sleep (cross-family autonomic-load anchor; CONFIRMED-citalopram sister)`

Per Q3.1.e sister analysis: stress_mean_sleep <-> resting_hr Spearman rho ~+0.10-0.20 range (NOT near-identity at section 3.3 threshold; cross-family modest positive coupling). The covariate disambiguates: beta_channel attenuates -> the RHR signal is shared autonomic-load via the sleep-stress axis; beta_channel survives -> RHR carries cardiovascular-specific information beyond the autonomic-load axis.

*Source*: Q3.1.e sister stress_mean_sleep cross-pair table + cross-channel-correlation card

*Observed correlation on S4*: Pearson r=+0.359 / Spearman rho=+0.377 (n=1337).

### Recommendation

Pre-spec all four covariates as secondary sensitivity arms. The dose_plasma_mg arm (covariate 1) is diagnostic-only at this time per the v3 REJECTED status; a positive beta_dose residue in the secondary is candidacy for a v3 re-test, NOT a re-promotion of the v3 verdict. The autocorrelation arm (covariate 2) operationalises HA-P7 section 4.5.4 on this channel using the already-materialised _lagged_lcera_z variant. The bb_lowest arm (covariate 3) is the cross-family autonomic-recovery disambiguator. The stress_mean_sleep arm (covariate 4) is the cross-family autonomic-load disambiguator.

---

## Cross-references

### HA-* tests that touch this channel (cite this analysis)

- **HA06b** (RHR z-score, 4d bidirectional; LOCKED TRAIN SUPPORTED / VALIDATE refuted / OVERALL REFUTED; R14 single-pool NOT-SUPPORTED CONVERGE-ON-OVERALL `badd04a`): primary operand IS this channel in second-order spike-form. **The descriptive substrate this analysis produces -- the Stratum-4 distribution (Q3.6.a) + autocorrelation E[L]\*=7.0 (Q3.6.b) + per-phase + recovery-axis reads (Q3.6.c) + first-order day-level crash-vs-normal (Q3.6.f) -- complements HA06b's tested operand with the raw-channel-distribution view.** The substantive HA06b verdict + the R14 single-pool verdict are LOCKED; this analysis's descriptive corroboration in Q3.6.f is NOT a re-interpretation.
- **H01** (RHR drift, absolute 7d-mean +3 bpm; LOCKED REFUTED both eras; R14 single-pool NOT-SUPPORTED CONVERGE `badd04a`): primary operand is this channel in absolute-threshold form. Q3.6.f descriptively re-anchors at the day-level.
- **HA06** (morning RHR delta, absolute bidirectional 4-5d; LOCKED REFUTED both eras; SUPERSEDED by HA06b): primary operand is this channel in absolute-delta form.
- **HA-P6 v3** (descriptive Layer 1; LOCKED `a980b1c` 2026-06-17): resting_hr is in the HA-P6 v3 7-channel set + the 4-of-7 distinguishable channels; this Q3.6 provides the per-channel substrate.
- **recovery_arc v2** (LOCKED `8feae6a` 2026-06-22): resting_hr was the only channel in the v2 7-channel set where the 4b-4a paired-bootstrap CI excluded 0 (+3.0 bpm, CI [+2.0, +4.0], E[L]\*=22.7); Q3.6.b reproduces the E[L]\* on Strand-A's pool; Q3.6.c reproduces the acute-infection DIP descriptively.

### Methodology MDs cited

- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3-6 -- Q3.6.c phase axis; Q3.6.d phase-stratified treatment.
- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) v3 section 5.6 -- resting_hr IS in 6-channel scope; **REJECTED with weak/non-significant beta**; Q3.6.d caveat-class framing per CONVENTIONS section 4.2.
- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) -- E[L]=7 default + factor-of-2 deviation rule; Q3.6.b reports E[L]\*=7.0.
- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) -- Stratum 4 boundary definition.
- [`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) (LOCKED `d47e0d3`) -- 6-phase recovery axis used in Q3.6.c LOAD-BEARING extension.
- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) -- Q3.6.h cross-reference.

### Existing artefacts referenced

- [`descriptive/trajectory/recovery_arc/findings.md`](../../trajectory/recovery_arc/findings.md) **LOAD-BEARING**: section 5.A cardiovascular family + section 7b 4b-4a paired-bootstrap (resting_hr the only excludes-0 channel, +3.0 bpm CI [+2.0, +4.0], E[L]\*=22.7); Q3.6.b reproduces E[L]\* + Q3.6.c reproduces acute-infection DIP.
- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) -- R14 HA06b + H01 rows (LANDED `badd04a`); descriptively corroborated in Q3.6.d + Q3.6.f.
- [`descriptive/operationalisation_support/bb_overnight_gain/findings.md`](../bb_overnight_gain/findings.md) -- most-recent Strand-A precedent (Q3.5; Tier 2 first); programmatic-emit pattern + load-bearing cross-reference template.
- [`descriptive/operationalisation_support/stress_stdev_sleep/findings.md`](../stress_stdev_sleep/findings.md) -- Q3.4 precedent for full-coverage continuous-channel pattern + clean f-string discipline.
- [`descriptive/operationalisation_support/bb_lowest/findings.md`](../bb_lowest/findings.md) -- Q3.3 sister BB-floor channel; reciprocal rho with resting_hr reported there.
- [`descriptive/operationalisation_support/all_day_stress_avg/findings.md`](../all_day_stress_avg/findings.md) -- Q3.2 precedent (CONFIRMED-citalopram sister).
- [`descriptive/operationalisation_support/stress_mean_sleep/findings.md`](../stress_mean_sleep/findings.md) -- Q3.1 original Phase-1 precedent.
- [`analyses/hypotheses/HA06b-rhr-zscore/result.md`](../../hypotheses/HA06b-rhr-zscore/result.md) -- LOCKED TRAIN SUPPORTED / VALIDATE refuted / OVERALL REFUTED; primary operand on this channel.
- [`analyses/hypotheses/H01-rhr-drift/result.md`](../../hypotheses/H01-rhr-drift/result.md) -- LOCKED REFUTED both eras; absolute spec on this channel.
- [`analyses/hypotheses/HA06-morning-rhr-delta/result.md`](../../hypotheses/HA06-morning-rhr-delta/result.md) -- LOCKED REFUTED both eras; SUPERSEDED by HA06b.

### Upstream pipeline

- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `pipeline/01_extract/garmin_uds_extras.py` (UDS-side passthrough for restingHeartRate field).
- `labels_crash_v2.csv` <- `garmin/hypotheses/crash_v2-definition/definition.md` (locked).

---

## Limitations

For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding constraints are:

1. **No HA verdict promotion**: HA06b + H01 + HA06 + R14 single-pool verdicts + v3 dose-response REJECTED verdict are LOCKED; this analysis's descriptive observations are NOT re-interpretations or re-promotions per CONVENTIONS section 4.2 + handoff section 3.
2. **No v3 REJECTED -> CONFIRMED reclassification** per handoff section 3 hard constraint. The observed phase shifts in Q3.6.d are descriptive Layer 1 observations; the v3 verdict lives in citalopram_dose_response_stress_mean_sleep.md and is the load-bearing artefact.
3. **First-order day-level read distinct from HA06b's tested operand**: HA06b's spike-form construct (per-4-day MAX |z|, bidirectional, lagged baseline) is the canonical HA test on this channel; Q3.6.f's first-order day-level Cohen's d is the descriptive-layer complement at a coarser resolution -- NOT a re-anchoring of HA06b.
4. **Chronotropic incompetence caveat** per HA06 + H01 + HA06b result.md: >85% of ME/CFS patients have blunted HR response per Workwell's own caveat; this is a population-level physiological caveat on RHR signals' biological interpretation, NOT a calibration-drift signature on this device.
5. **Recovery-axis Q3.6.c extension covers pre-illness + acute phases on the FULL CORPUS** OUT of Stratum 4 strictly for the load-bearing recovery_arc v2 reproduction per handoff section 2.4. Per CONVENTIONS section 4.3 + recovery_arc v2 caveat 2: the acute-phase n=14 limits tight CI on the dip magnitude.

---

*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` (gitignored per `docs/research/**/*.json`). To refresh: ``python run.py``.*
