# Findings -- `all_day_stress_avg` operationalisation-support descriptive (Q3.2.a-i)

**Channel**: `all_day_stress_avg` (CONFIRMED-citalopram, +0.565/mg p=0.000 buildup post-CPAP per [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) v3 section 5.6.1 -- the **largest beta** among the 3 CONFIRMED channels). Column semantics: [DATA_DICTIONARY.md section 7B All-day stress](../../../DATA_DICTIONARY.md) -- 24h-window mean of UDS pre-aggregated stress samples, JSON-passthrough from `daily_uds.csv` per [`garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) Wave-3 propagation 2026-06-12 (no FIT parsing).

**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to 2026-06-05). n=1359 days with channel out of 1372 Stratum 4 days (13 NaN days from UDS-side coverage gaps).

**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.2 (LOCKED 2026-06-18 r3, commit `ccbd12e`) -- this analysis is the **second of the 3 CONFIRMED-citalopram channels in the Tier 1 user-prioritised Phase 2 sequential batch** (R14 `single_pool_reanchor` landed first at `badd04a`; `bb_lowest` next). Q3.2.a-i template applied per section 3.1 verbatim.

**Sources**: `per_day_master.csv` (Garmin daily aggregate) + `labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level per CONVENTIONS section 3.6).

**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). HA-C3 cluster (HA-C3 v2 REJECTED `a2b18ba` + HA-C3p PARTIAL `e5a63fe`, both 2026-06-23) cross-references in this analysis are **descriptive corroboration only**; the inverted-U / concave non-linearity finding lives in those result.md files and is NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). Statistical hygiene anchors: section 3.1 (personal baseline), section 3.3 (column-duplication threshold |rho|>=0.92), section 3.4 (crash-drop sensitivity |delta|>0.10), section 3.5 (spike metrics -- this channel is a 24h-window MEAN; the spike-form companion lives in `stress_low_motion_min_count_S60_Mlow`), section 3.6 (named counts).

---

## Headline

`all_day_stress_avg` on Stratum 4 is a **mildly right-skewed, autocorrelation-DENSE 24h-window daily-mean channel** (skew=+0.87, excess kurtosis=+1.99 -- **NOT heavy-tail-flag-triggering**, p99/median = 51.4/32.0 = 1.61; this channel is materially less heavy-tailed than its sister `stress_mean_sleep` skew=+2.72). The **data-driven E[L]\*=29.8** (factor-of-4 above project default; **the LONGEST yet observed in Strand A**, longer than `stress_low_motion_min_count_S60_Mlow` E[L]\*=21.1 and `stress_mean_sleep` E[L]\*=12.6). The **phase-stratified medians shift DRAMATICALLY at the citalopram boundary** (unmedicated median 34.0 to buildup median 28.5 to consolidation 31.0 to afbouw 34.0; ~-5.5 median shift at the buildup boundary, ~-1.8 within-buildup-phase MAD); the citalopram 30d-mean step (2024-04-09 pre/post) is **-7.2 stress units** -- empirically larger than the recalibration's slope-extrapolation predicts at the day-resolution of the boundary. The **afbouw phase recovers fully to the unmedicated median** (median 34.0 = unmedicated 34.0), suggesting a within-citalopram-traject reversibility readable from this descriptive layer (consistent with the `recovery_arc v2` afbouw-reversal finding cross-referenced in `descriptive/README.md` section 5). Crash-vs-normal at episode level is **weak** (d=+0.37; bootstrap CI95 [-0.40, +4.71] **brushes zero**); day-level Mann-Whitney U fires robustly (z=+4.30, p<0.0001, P(crash>normal)=0.627). **Zero near-identity pairs** at the |rho|>=0.92 threshold; closest is `awake_stress_avg` at rho=+0.887 (just below). The **HA-C3p right-shift unmedicated bin observation is REPRODUCED EXACTLY** at the quintile boundaries (unmed counts [45, 80, 129, 138, 189], n=581; full pool [251, 256, 296, 251, 305], n=1359 -- HA-C3p's full pool was n=1351 because that pre-reg additionally gevoelscore-filtered); the unmedicated stratum carries **1.45x the full-pool share of Q5 mass and 0.42x the full-pool share of Q1 mass**, an extension of the HA-C3p descriptive observation to a share-ratio quantification.

---

## Q3.2.a -- Distribution shape (Stratum 4)

**Verdict on the section 3.1 delegate question**: **delegate is partial; extend in this analysis**. [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) was extended for continuous channels first and primarily documents `stress_mean_sleep`; coverage on `all_day_stress_avg` is incidental. The full distribution descriptors (skewness/kurtosis/heavy-tail flag/p99-vs-median ratio) are surfaced here for the first time on this channel.

| stat | value | source |
|---|---:|---|
| n (Stratum 4) | 1359 | `per_day_master.csv` `all_day_stress_avg` non-NaN within S4 |
| mean | 32.72 | (single-pool S4) |
| median | 32.00 | |
| std (ddof=1) | 6.03 | |
| MAD (unscaled) | 4.00 | |
| MAD x 1.4826 (normal-equivalent SD) | 5.93 | for robust z-score scaling per section 3.1 |
| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | 21.6 / 24.0 / 25.0 / 28.5 / 32.0 / 36.0 / 40.0 / 43.0 / 51.4 | |
| skewness (Fisher-Pearson) | **+0.87** | mildly right-skewed; **does NOT trigger skew>1 heavy-tail rule** |
| excess kurtosis (Fisher) | **+1.99** | mildly heavy-tailed (sister stress_mean_sleep was +15.5) |
| heavy_tail_flag | **False** | skew<=1 AND p99/median = 1.61 < 3.0 (both heavy-tail conditions fail) |
| range | 19.0 to 69.0 | tail extends to ~2.2x median (sister stress_mean_sleep reached ~4.2x) |

### Cross-channel comparison vs sister `stress_mean_sleep` (first analysis Q3.1.a)

| stat | all_day_stress_avg (this analysis) | stress_mean_sleep (first analysis) |
|---|---:|---:|
| n S4 | 1359 | 1339 |
| mean | 32.72 | 19.97 |
| median | 32.00 | 19.21 |
| MAD (unscaled) | 4.00 | 2.87 |
| skewness | +0.87 | +2.72 |
| excess kurtosis | +1.99 | +15.45 |
| heavy_tail_flag | **False** | **True** |
| p99 / median ratio | 1.61 | 2.27 |

**The 24h-window mean is materially less heavy-tailed than the sleep-window mean.** Mechanistic reading: the 24h-window aggregates over many minutes (~480 stress samples at 3-min cadence), so extreme-night events get diluted; the sleep-window mean (~120 samples per night) is more susceptible to a single bad night driving the day's stat. The implication for HA-pre-regs: the robust-vs-non-robust z-scoring choice matters less for this channel than for the sister (raw std is 6.03 vs robust-equiv 5.93, only a 1.6% difference; sister's was 30%). The MAD-based robust z-scoring per CONVENTIONS section 3.1 is **still preferred** -- the heavy-tail-flag failing does not promote to "use mean+std" -- but the cost of getting it wrong is smaller here.

See [`plots/fig1_distribution_s4.png`](plots/fig1_distribution_s4.png).

---

## Q3.2.b -- Autocorrelation structure + E[L]\*

The **data-driven block length is E[L]\*=29.8** (Politis-White 2004 with Patton-Politis-White 2009 correction per [`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) vs the project default E[L]=7 per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). The **factor-of-2 deviation flag fires** (deviation ratio = 3.26 = factor-of-4+ deviation). Cutoff lag M=18. **This is the LONGEST autocorrelation horizon yet observed in the Strand A landed analyses.**

| lag (days) | autocorrelation |
|---:|---:|
| 1 | +0.349 |
| 2 | +0.290 |
| 3 | +0.256 |
| 7 | +0.222 |
| 14 | +0.189 |

Politis-White 2-sigma significance threshold (n=1359): |rho| = 0.146. The lag-14 ACF (+0.189) is **still above the significance threshold**, and the lag-7 ACF (+0.222) is comfortably above -- consistent with the M=18 cutoff lag (significance persists out to lag ~14-18). Compare to `stress_mean_sleep` (M=6) and `stress_low_motion_min_count_S60_Mlow` (M=11): this channel's serial dependence persists FURTHER than either sister.

### Cross-channel comparison (E[L]\* by analysis)

| analysis | channel | E[L]\* | M | factor-of-2 flag |
|---|---|---:|---:|---|
| Phase-1 #1 (stress_mean_sleep) | sleep-window mean | 12.6 | 6 | YES (factor-of-2) |
| Phase-1 #3 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 | 11 | YES (factor-of-3) |
| **this analysis (all_day_stress_avg)** | **24h-window mean** | **29.8** | **18** | **YES (factor-of-4)** |

**Implication**: any HA pre-reg using `all_day_stress_avg` MUST (a) use the data-driven block length E[L]\*~30 as the primary bootstrap CI, OR (b) pre-spec a sensitivity arm at E[L]=30 alongside the default-E[L]=7 primary. The project default of 7 is **dramatically too short** for this channel; the factor-of-4 deviation is the largest yet observed in Strand A. The mechanistic interpretation: the 24h-window mean smooths over many minutes per day AND inherits long-range trend structure from the citalopram trajectory + LC-recovery arc, both of which the data-driven estimator picks up on top of the day-to-day serial dependence.

**HA-C3 cluster note**: HA-C3 v2 and HA-C3p both reported their data-driven E[L]\* in result.md section 7 from a different derivation (linear-residual on the continuous predictor = 5.35; bin-label sequence = 7.0; "No flags"). The HAs' bin-label-sequence derivation gives a shorter E[L]\* because binning collapses the within-bin trend variance the raw channel carries; the HAs' E[L]\*=7 reading is consistent with **the bin-label sequence's own autocorrelation**, NOT the underlying raw `all_day_stress_avg` channel's autocorrelation. This descriptive analysis's E[L]\*=29.8 on the raw channel is a **DIFFERENT derivation from the HAs'**; both are correct in their respective frames. A consumer test that operates on the raw channel directly (not binned) should follow this analysis's E[L]\*~30; a consumer test that operates on a binned/categorical derivative of the channel can follow the HAs' shorter E[L]\* derivation.

See [`plots/fig5_acf.png`](plots/fig5_acf.png).

---

## Q3.2.c -- Base rates per citalopram phase + quintile bin distribution

Phase axis per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3:

| phase | window | n | median | mean | MAD | p10 / p90 |
|---|---|---:|---:|---:|---:|---|
| unmedicated | 2022-09-03 to 2024-04-08 | 581 | **34.00** | 34.78 | 3.00 | 28.0 / 42.0 |
| buildup | 2024-04-09 to 2024-06-19 | 72 | **28.50** | 28.92 | 2.50 | 24.0 / 34.0 |
| consolidation | 2024-06-20 to 2026-03-19 | 635 | **31.00** | 31.15 | 3.00 | 25.0 / 38.0 |
| afbouw | 2026-03-20 to 2026-06-05 | 71 | **34.00** | 33.76 | 3.00 | 25.0 / 40.0 |

**The phase medians shift sharply at the citalopram boundary.** Compare to sister `stress_mean_sleep` (first analysis Q3.1.c) where the phase medians were nearly flat (17.04 to 20.20 across all four phases). On THIS channel:

- unmedicated to buildup: **-5.5 median units** (~-1.8 buildup-MAD; clearly outside MAD)
- unmedicated to consolidation: **-3.0 median units** (~-1.0 consolidation-MAD)
- consolidation to afbouw: **+3.0 median units** (recovery toward unmedicated baseline)
- afbouw vs unmedicated: **+0.0 median units** (full recovery to unmedicated baseline)

The two **transition phases** (buildup n=72; afbouw n=71) have **n<75 each** with **narrower OR similar dispersion** (MAD~2.5-3.0) than the two **steady-state phases** (unmedicated n=581; consolidation n=635, MAD~3.0). Any HA test that wants per-phase verdicts under [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5.A on buildup or afbouw faces a ~8x n disadvantage vs the steady-state phases.

Named counts (CONVENTIONS section 3.6): the per-phase n's above are `all_day_stress_avg`-non-NaN day rows in `per_day_master.csv` within Stratum 4 date masks per `citalopram_phase_stratification.md section 3` boundary dates.

### Q3.2.c extension -- HA-C3p right-shift unmedicated bin observation REPRODUCED at finer quantile resolution

Per handoff section 2.4: this section descriptively reproduces / extends the [HA-C3p result.md section 2 right-shift observation](../../hypotheses/HA-C3p/result.md). HA-C3p's locked quintile boundaries are pre-committed to `per_day_master.csv` SHA-256 `d0ff9253` and tested on the as-of-date 2026-06-05 corpus.

Quintile boundaries: {Q1[0,28), Q2[28,31), Q3[31,34), Q4[34,37), Q5[37,100]} (locked per HA-C3p hypothesis.md section 4.1).

| bin | unmed n | unmed share % | full S4 n | full S4 share % | share ratio (unmed/full) |
|---|---:|---:|---:|---:|---:|
| Q1[0,28) | **45** | 7.75% | 251 | 18.47% | **0.42** |
| Q2[28,31) | **80** | 13.77% | 256 | 18.84% | **0.73** |
| Q3[31,34) | **129** | 22.2% | 296 | 21.78% | **1.02** |
| Q4[34,37) | **138** | 23.75% | 251 | 18.47% | **1.29** |
| Q5[37,100] | **189** | 32.53% | 305 | 22.44% | **1.45** |
| total | 581 | 100% | 1359 | 100% | -- |

**The HA-C3p right-shift unmedicated bin counts [45, 80, 129, 138, 189] (n=581) reproduce EXACTLY at this analysis's draft-time snapshot.** The full-pool counts differ slightly (this analysis [251, 256, 296, 251, 305] n=1359 vs HA-C3p [248, 253, 294, 251, 305] n=1351); the 8-day difference reflects this analysis's no-gevoelscore-filter approach (descriptive layer) vs HA-C3p's gevoelscore-required filter (test layer). The substantive right-shift pattern is identical.

**Share-ratio quantification** (this analysis's extension of the HA-C3p observation): the unmedicated stratum carries **1.45x the full-pool share of Q5 mass (~3.5x the full-pool share of Q1 mass)** -- a graded right-shift across all five quintiles, monotonic from Q1 (under-represented at 0.42) through Q3 (essentially at-par at 1.02) to Q5 (over-represented at 1.45). The unmedicated decile p10/p90 of [28, 42] vs full-pool [25, 40] also shows the right-shift (both quantiles ~+2-3 stress units higher in the unmedicated pool).

Per handoff section 2.4: this is a **cross-test validation of the recalibration +0.565/mg beta finding at a different operationalisation** (bin distribution rather than mean beta). The HA-C3p result.md section 2 framed this consistency descriptively; this analysis reproduces it at the snapshot level. The HA-C3p substantive verdict is NOT extended or promoted here per the handoff's NO-HA-verdict-promotion discipline.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (citalopram-phase violins).

---

## Q3.2.d -- Phase-stratified distribution + citalopram step magnitude vs natural variation

**This is the most operationally consequential finding for downstream HA pre-regs on this channel.**

The locked dose-response anchor (v3 section 5.6.1): **buildup post-CPAP beta = +0.565/mg p=0.000** (the **LARGEST beta** among the 3 CONFIRMED-citalopram channels: `stress_mean_sleep` +0.43/mg, `bb_lowest` -1.13/mg inverse direction). Naive extrapolation: at 30mg steady-state (consolidation), the implied citalopram-attributable lift is +0.565 x 30 = **+16.95 stress units** -- larger than the channel's full interquartile range (p75 - p25 = 7.5) **DOUBLED**, and ~3 standard deviations on the consolidation-phase MAD.

Observed steady-state level shifts (median):

| comparison | delta median | within-phase MAD | within-MAD? |
|---|---:|---:|---|
| buildup minus unmedicated | **-5.5** | 2.5-3.0 | ~-1.8 buildup-MAD; clearly OUTSIDE MAD |
| consolidation minus unmedicated | **-3.0** | 3.0 | ~-1.0 consolidation-MAD; AT the MAD boundary |
| afbouw minus consolidation | **+3.0** | 3.0 | ~+1.0 consolidation-MAD; AT the MAD boundary |
| afbouw minus unmedicated | **+0.0** | 3.0 | full recovery to unmedicated baseline |

### Reading the direction -- what the data shows + the operationalisation-support consequence

The median **drops sharply at the citalopram boundary** (unmedicated to buildup: -5.5 stress units in median, ~16% reduction) and **recovers fully during afbouw** (afbouw median 34.0 = unmedicated median 34.0). The day-resolved citalopram boundary step (30d pre vs post the 2024-04-09 boundary): **-7.2 stress units** -- larger than the phase-median shift because the buildup phase's first 30 days are still dose-ramping at sub-steady-state levels.

This pattern is **opposite in direction to the dose-response beta** (+0.565/mg should push the channel UP with rising dose, not DOWN). Three readings, none asserted as the substantive truth per CONVENTIONS section 2.1 + section 4.3:

1. **The beta is a within-buildup-window dose-trend, not a between-phase steady-state level shift.** The v3 dose-response MD's beta is the slope of `all_day_stress_avg` against `dose_plasma_mg(d)` *within* the buildup-window (2024-04-09 to 2024-06-19); it measures how the channel changes as dose rises from 0 to 30mg over ~70 days. Across phases, the LC-trajectory's broader recovery arc PLUS the citalopram step PLUS pacing-practice strengthening all overlap; the between-phase level shift can move opposite to the within-window beta if the broader trajectory dominates. The recovery_arc v2 analysis ([`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/)) documents this trajectory at multi-channel detail.

2. **The dose-adjusted-predictor pattern under [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5.B remains correct for within-phase work**; the cross-phase level shift in raw form is NOT what the section 5.B framework promises to recover. The HA-C3 v2 and HA-C3p section 5.B sensitivity arms (cross-phase pool with predictor = raw - 0.565/mg x dose) BOTH returned REJECTED (0-of-3 conditions MET); the section 5.B numerical adjustment does not recover the unmedicated-pool inverted-U shape that the section 5.A unmedicated headline carries.

3. **The afbouw recovery is descriptively striking**: afbouw median 34.0 = unmedicated median 34.0 EXACTLY. This is consistent with the `recovery_arc v2` analysis's afbouw-reversal finding (referenced in `descriptive/README.md` section 5 [`row 14`](../../README.md): "section 5.A sub-stratification on phase-5 CONFIRMED-citalopram channels surfaces **afbouw reversal** (citalopram benefit reversible during dose reduction)"). The afbouw recovery on `all_day_stress_avg` corroborates that finding descriptively. Note: this is a Layer 1 observation; the recovery_arc analysis is the load-bearing artefact for substantive readings.

### HA-C3 cluster descriptive cross-reference (load-bearing per handoff section 2.4)

The HA-C3 cluster (v2 REJECTED + HA-C3p PARTIAL, both 2026-06-23) detected an **inverted-U / concave non-linearity** in the stress to gevoelscore mapping on the **unmedicated section 5.A headline pool** (n=581 here): HA-C3 v2 found bin-means B1[0,30)=3.958, B2[30,40)=4.265, B3'[40,100]=3.832 (peak at B2); HA-C3p found Q1=3.822, Q2=4.138, Q3=4.271, Q4=4.290, Q5=4.016 (peak at Q3-Q4). The descriptive bin-mean trajectory at this analysis's Q3.2.c quintile boundaries (showing the **predictor-side distribution** rather than the outcome-side trajectory) is consistent with the inverted-U structural reading: the unmedicated stratum's mass concentrates in the Q3-Q5 region where the HA-C3 cluster found the gevoelscore peak. The Q3.2.d phase-median shifts (unmed 34.0 to buildup 28.5) move the channel mass **toward the lower end of the HA-C3 cluster's inverted-U** -- the citalopram boundary pushes typical days into Q1-Q2 (HA-C3p Q1[0,28) median predictor; the day-typical value drops from ~34 in unmedicated to ~28 in buildup).

**Important honesty constraint (handoff section 3 + CONVENTIONS section 4.2)**: this descriptive observation does NOT extend the HA-C3 cluster's inverted-U substantive claim or promote any direction-of-causality reading on the citalopram boundary. The HA-C3 cluster verdicts are LOCKED at REJECTED + PARTIAL (and their joint cross-test reading of "Wiggers' numbers wrong-for-this-participant but the underlying SHAPE IS REAL in the INVERSE direction" is the consolidated 4-cell-matrix reading in HA-C3p result.md section 6, NOT a substantive HA-C3 v3 / HA-C3p v2 alternative claim). This Q3.2.d's descriptive corroboration is a **substrate that an HA-pre-reg author can cite when drafting a non-linearity-on-this-channel HA**, not an additive interpretation layer.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) and [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d rolling median through phases).

---

## Q3.2.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)

Brief-mandated three channels plus five biologically-plausible neighbours.

| target channel | n | Pearson r | Spearman rho | near-identity flag? |
|---|---:|---:|---:|---|
| `stress_stdev_sleep` | 1339 | +0.309 | +0.266 | no |
| `stress_mean_sleep` | 1339 | +0.522 | +0.404 | no |
| `stress_low_motion_min_count_S60_Mlow` | 1358 | +0.847 | +0.860 | no |
| `awake_stress_avg` | 1359 | +0.865 | +0.887 | no |
| `asleep_stress_avg_uds` | 1351 | +0.542 | +0.440 | no |
| `bb_lowest` | 1359 | -0.727 | -0.749 | no |
| `all_day_stress_max` | 1359 | +0.391 | +0.493 | no |
| `resting_hr` | 1357 | +0.231 | +0.195 | no |

**Zero near-identity pairs fire** at the |rho|>=0.92 CONVENTIONS section 3.3 threshold. The closest pair is `awake_stress_avg` at Spearman rho=+0.887 (Pearson r=+0.865), well below the threshold but high enough to warrant care: `awake_stress_avg` is the 24h-window mean restricted to the awake portion of the day, while this channel includes asleep + awake; the two are heavily overlapping by construction.

Three substantive observations beyond the threshold check:

1. **The spike-form companion `stress_low_motion_min_count_S60_Mlow` is r=+0.85 / rho=+0.86 with this channel** (reciprocally confirmed: per stress_low_motion findings.md Q3.x.e the same pair was r=+0.85 / rho=+0.86, n=1358). The continuous-form daily mean and the spike-counting primitive carry strongly overlapping signal on this corpus but are NOT near-identity. A consumer HA whose mechanism is *acute spike at rest* should use the count primitive; a consumer HA whose mechanism is *general autonomic load throughout the day* should use this channel. The two channels are different constructs operationally even though they covary strongly.

2. **The sister `stress_mean_sleep` is r=+0.52 / rho=+0.40 with this channel**. Same direction (both are CONFIRMED-citalopram autonomic-load channels) but **only ~20-30% of the variance is shared**. This is consistent with the stress_mean_sleep first analysis Q3.1.e finding (same pair, reciprocally r=+0.52 / rho=+0.40 from the sleep-window side). The sleep-window-mean and 24h-window-mean stress are operationally distinct constructs even though biologically connected; they are NOT redundant in an HA covariate model.

3. **`bb_lowest` is rho=-0.75** -- strong negative correlation, the strongest inverse-direction partner. Both are CONFIRMED-citalopram channels with opposite-direction priors (stress UP with dose; BB DOWN with dose). The rho=-0.75 magnitude reflects the shared autonomic-state structure (high stress days have low BB nadirs) and the shared citalopram-trajectory absorption; both effects superimpose. NOT near-identity but the closest inverse-direction neighbour.

The cross-channel-correlation card's existing 7-channel panel ([`cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md)) does NOT include this channel as a primary; the surfaced pair `all_day_stress_avg <-> bb_lowest` at rho=-0.75 is a candidate for inclusion at the next refresh (flag-only -- no card edits as part of this analysis per discipline).

---

## Q3.2.f -- Crash-day vs normal-day (Stratum 4 refresh in operationalisation-support framing)

Per CONVENTIONS section 3.6 named counts: 29 crash-episodes (crash_v2 episode-level via `labels_crash_v2.csv` unique `episode_id` starting with `crash-`); 103 crash-days (day-level, `label=='crash'`); 1256 non-crash days (the complement within Stratum 4 channel-valid days).

### Episode-level (primary unit per CONVENTIONS section 3.6)

| stat | value |
|---|---:|
| n crash-episodes | 29 |
| n normal-day base rate | 1256 |
| mean per-episode `all_day_stress_avg` | 34.50 |
| mean normal-day `all_day_stress_avg` | 32.41 |
| mean diff (episode minus normal-day) | **+2.09** |
| Cohen's d (episode-level vs normal-day pooled) | **+0.37** |
| Bootstrap 95% CI on mean diff | **[-0.40, +4.71]** (5000 iters, seed=20260624) |

**The episode-level signal is WEAK on this channel.** Cohen's d=+0.37 is **similar magnitude to `stress_low_motion_min_count_S60_Mlow` episode-level d=+0.38** (the count primitive's third-analysis Q3.x.f finding) but **substantially smaller than `stress_mean_sleep` d=+0.91** (the first-analysis Q3.1.f). The bootstrap 95% CI **brushes zero** (-0.40, +4.71); the episode-level signal does not robustly exclude zero on this channel at the as-of-date 2026-06-05 snapshot. Compare to `stress_mean_sleep` (CI [+1.58, +8.40], robust) and `stress_low_motion_min_count_S60_Mlow` (CI [+0.94, +34.88], just barely excluding zero).

### Day-level (autocorrelation-inflated supplementary)

| stat | value |
|---|---:|
| n crash-days | 103 |
| n normal-days | 1256 |
| mean crash-day | 36.46 |
| mean normal-day | 32.41 |
| median crash-day | 35.0 |
| median normal-day | 32.0 |
| mean diff (point estimate) | **+4.04** |
| median diff | **+3.0** |
| Cohen's d | **+0.68** |
| Mann-Whitney U: z | **+4.30** |
| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **<0.0001** |
| Mann-Whitney U: P(crash > normal) | **+0.627** |
| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (project default) | [+1.20, +6.65], width 5.46 |
| Stationary bootstrap 95% CI on mean diff, **E[L]=30** (data-driven, Q3.2.b flag fired) | **[+0.59, +7.10]**, width 6.52 |

### Mann-Whitney U as the heavy-tail-robust read

Although this channel is NOT heavy-tail-flag-triggering (Q3.2.a), the Mann-Whitney U is reported for parity with the count-primitive third analysis (and as a rank-based robustness check on the Cohen's d). **The day-level signal is unambiguously present**: z=+4.30, p<0.0001, P(crash > normal) = 62.7% (vs 50% null). The median diff (+3.0) is equal to the within-population MAD on the channel (4.0) -- a moderate effect at the day level that survives the rank-based robustness check.

**Read together with Cohen's d**: the channel carries a moderate positive shift on crash days at the day level (d=+0.68) that becomes weak at the episode level (d=+0.37). This is the **expected within-episode-autocorrelation inflation** -- consecutive within-episode days are not independent observations; the day-level d=+0.68 is the inflated read and the episode-level d=+0.37 is the unit-of-analysis-clean read. **The unit-of-analysis-clean read does NOT robustly exclude zero** at the as-of-date snapshot; the episode-level CI brushes zero (-0.40, +4.71). Consumer HAs using this channel as a crash-discriminator should report the episode-level (not the day-level) as the unit-of-analysis-clean read.

### Block-length sensitivity (Q3.2.b cross-check)

Per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md), when the data-driven E[L]\* deviates from the project default by more than a factor of 2, the analysis must report the CI at the data-driven value alongside the default. Q3.2.b fired that flag (E[L]\*=29.8, deviation ratio 3.26 = factor-of-4). The E[L]=30 CI ([+0.59, +7.10]) is **+19.4% wider** than the E[L]=7 CI ([+1.20, +6.65]) -- the largest CI-width change across the three Strand A landed analyses' block-length sensitivity arms (sister stress_mean_sleep was +5%; count primitive was +10.5%). **Both block-length choices still exclude zero** on the day level, but the wider data-driven CI's lower bound (+0.59) is much closer to zero than the project default's (+1.20). At the episode level (which carries the unit-of-analysis-clean read), the CI brushes zero regardless of block-length choice.

### Crash-drop sensitivity (CONVENTIONS section 3.4)

| frame | Spearman rho | n |
|---|---:|---:|
| full Stratum 4 | -0.056 | 1359 |
| crash-days dropped | -0.004 | 1256 |
| \|delta\| | **0.051** | -- |
| section 3.4 threshold (0.10) crossed? | **no** | -- |

The crash days **are doing some correlation work** in the channel-vs-gevoelscore pair (full rho=-0.056 moves to ~0 when crashes drop), but the magnitude is below the section 3.4 threshold. **No flag fires.** Same pattern as the count-primitive third analysis (full rho=-0.056 -> dropped +0.001 |delta|=0.057). The same-day channel-vs-gevoelscore correlation is essentially **zero on normal days** -- gevoelscore and 24h-mean-stress are **decoupled on normal days** at the daily resolution. This is consistent with the project's broader same-day-coupling observations across the three CONFIRMED-citalopram autonomic-load channels.

See [`plots/fig4_crash_vs_normal.png`](plots/fig4_crash_vs_normal.png).

---

## Q3.2.g -- Spike-detecting primitive availability

`all_day_stress_avg` is **structurally a 24h-window daily mean** (UDS-pre-aggregated; JSON-passthrough from `daily_uds.csv`; no FIT parsing per `garmin_indicators_audit.md` Wave-3 propagation 2026-06-12). Per CONVENTIONS section 3.5 it is the **dilution-vulnerable continuous form** of the autonomic-load construct; the spike-form companion `stress_low_motion_min_count_S60_Mlow` (Phase-1 third analysis) carries spike-during-rest information beyond this daily mean. Sub-daily resolution is **not in `per_day_master.csv`** for this channel's exact form; latent in monitoring_b FIT files.

Spike-related primitives in the master (24h-window):

| column | DATA_DICTIONARY | n_non_nan (S4) | type | relation to `all_day_stress_avg` |
|---|---|---:|---|---|
| `all_day_stress_max` | [section 7B](../../../DATA_DICTIONARY.md) | 1359 | daily peak stress value (24h) | Pearson r=**+0.39** / rho=+0.49; partial overlap (peak vs mean) |
| `max_spike_minutes` | [section 8](../../../DATA_DICTIONARY.md) | 1364 | longest contiguous run of stress>=75 lasting >=5min in 24h | Pearson r=**+0.54** / rho=+0.58; moderate overlap (peak-duration vs mean) |
| `stress_high_duration_min` | [section 8B C4](../../../DATA_DICTIONARY.md) | 1364 | total 24h minutes at high-stress threshold per FIT extraction | (not paired here, but logically related to spike-form) |
| `stress_low_motion_min_count_S60_Mlow` | [section 8C](../../../DATA_DICTIONARY.md) | 1365 | minute-level count of low-motion-high-stress windows (24h) | Pearson r=**+0.85** / rho=+0.86 -- the spike-form companion per CONVENTIONS section 3.5 |

### CONVENTIONS section 3.5 framing -- the continuous-vs-spike pair on this channel

The third Phase-1 Strand-A analysis ([`stress_low_motion_min_count_S60_Mlow`](../stress_low_motion_min_count_S60_Mlow/findings.md) Q3.x.g) explicitly named THIS channel as its **continuous-form cousin** per CONVENTIONS section 3.5; this analysis reciprocally names `stress_low_motion_min_count_S60_Mlow` as the **spike-form companion**. The cross-pair correlation r=+0.85 / rho=+0.86 (reciprocally confirmed on both sides) characterises the "general autonomic load throughout the day" vs "acute spike at rest" construct pair:

- A future HA whose mechanism is **acute spike-at-rest** should use `stress_low_motion_min_count_S60_Mlow` as primary, NOT this channel as primary -- this channel dilutes the within-day spike density across all 480+ samples.
- A future HA whose mechanism is **general autonomic load throughout the day** should use this channel as primary, NOT the count primitive -- the count primitive's threshold-counting collapses level information into binary above/below decisions.
- Both channels enter a future HA as separate constructs (their r=+0.85 IS NOT near-identity at the section 3.3 threshold); the spike-vs-mean disambiguation belongs in the HA's covariate-sensitivity arm (per Q3.2.i below).

`all_day_stress_max` is the in-master 24h-peak; `max_spike_minutes` is the in-master longest-spike-duration. Both are weakly-to-moderately related to this channel (r=+0.39 and r=+0.54 respectively) -- they carry independent peak-and-duration information that this channel's 24h mean averages out. A consumer test wanting the "high water mark" of the day should use `all_day_stress_max`; a test wanting the "longest contiguous spike" should use `max_spike_minutes`.

**Latent in FIT, not in master**: per-minute monitoring_b stress samples (raw ~3-min cadence; the source of all UDS aggregates). Building a customised within-day stress-density primitive at finer-than-daily resolution is a queued extraction task; this analysis does NOT action it.

---

## Q3.2.h -- Outlier detection + calibration-drift check

Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md):

- This channel is a **Wave-3 JSON-side passthrough** (2026-06-12) from `daily_uds.csv`; no FIT parsing needed. One of 5 all-day stress columns extracted in the Wave-3 batch (also: `all_day_stress_max`, `awake_stress_avg`, `asleep_stress_avg_uds`, and one count companion).
- **No specific calibration-drift events catalogued for `all_day_stress_avg`** in `garmin_indicators_audit.md`; the audit's per-column provenance map covers it under the Wave-3 passthrough bullet rather than as its own row.
- Underlying sensor is **Forerunner 245 Elevate V3 throughout the entire 2021-08-16 to present window** -- no device change in the analytic window.

### Outlier scan (MAD-based |z|>5; threshold per CONVENTIONS section 3.1 robust-baseline default)

**1 outlier-day flagged** out of 1359:

| date | value | MAD-z | likely category |
|---|---:|---:|---|
| 2023-11-29 | 69.0 | **+6.24** | global max; same date is the global max for `stress_mean_sleep` (Q3.1.h) AND for `stress_low_motion_min_count_S60_Mlow` (Q3.x.h global max at 361 min/day); the **named peak-crash exemplar day** per [`garmin_exploration/stress_low_motion_viz/family_a_daily.py`](../../../analyses/garmin_exploration/stress_low_motion_viz/family_a_daily.py) |

**The single outlier is NOT an artefact**: 2023-11-29 is the same date that fires as the global max on `stress_mean_sleep` (value 72.99, MAD-z +12.64) and on `stress_low_motion_min_count_S60_Mlow` (value 361 min/day, MAD-z +7.12). Three independent autonomic channels all spike together on this date -- a clear **cross-channel-consistent real stress event**, not a sensor failure. The day is also a named exemplar in the stress_low_motion within-day visualisation work. Downstream HA tests should NOT trim this date; it is part of the channel's natural shape.

The fact that THIS channel flags ONLY 1 outlier at the |z|>5 threshold (vs 16 on `stress_mean_sleep` and 6 on `stress_low_motion_min_count_S60_Mlow`) is consistent with Q3.2.a's heavy-tail-flag = FALSE finding: the 24h-window mean dilutes spike-day signals more than the other two channels, so the upper tail is more compressed and the |z|>5 outlier rule fires less often. The single firing day is the most extreme cross-channel-consistent event; lesser stress-spike days on the other two channels are absorbed into this channel's body distribution.

### Drift check -- rolling 90d median over Stratum 4

| snapshot date | rolling 90d median |
|---|---:|
| 2022-12-01 | 34.0 |
| 2023-06-01 | 34.5 |
| 2023-12-01 | 34.0 |
| 2024-06-01 | 30.0 |
| 2025-01-01 | 29.0 |
| 2025-12-01 | 29.5 |

The rolling 90d median exhibits a **clear multi-year shift** at the citalopram boundary: ~34.0-34.5 throughout the unmedicated era (2022-12 through 2023-12); ~29-30 throughout the consolidation era (2024-06 onward). The ~5-unit shift (~1.25 channel-MADs) over a ~6-month window centred on the 2024-04-09 citalopram boundary is the largest single-event step in the channel's history per this analysis. The **consolidation-boundary step at 2024-06-20** (entry into 30mg steady-state) shows trailing-30d mean = 31.27, leading-30d mean = 31.60 -- a **+0.33 step**, well within MAD; the consolidation boundary specifically does NOT register a sharp step (the shift had already happened by the citalopram-axis boundary 2024-04-09). The **citalopram-axis boundary 2024-04-09 step** shows trailing-30d mean = 33.53, leading-30d mean = 26.33 -- a **-7.20 step**, ~1.8 channel-MADs -- THIS is the empirical day-resolved shift driving the longer 90d-window pattern.

**This is NOT a calibration-drift signature** -- the shift is precisely time-located at a documented intervention boundary (citalopram dose ramp begins 2024-04-09), and the channel recovers fully during afbouw (per Q3.2.c). A calibration-drift signature would be a gradual monotonic creep unrelated to documented events; this is the opposite -- a sharp drop at the boundary with full recovery at the reverse boundary.

### `garmin_indicators_audit.md` row proposal (PROPOSE-ONLY)

[`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) does NOT yet have a per-column row for the all-day stress family (5 columns: `all_day_stress_avg`, `all_day_stress_max`, `awake_stress_avg`, `asleep_stress_avg_uds`, and the in-master count companion); only the Wave-3 passthrough bullet aggregates them. **Proposed row content** (do NOT apply as part of this analysis per handoff section 3 / discipline):

> Channel family: `all_day_stress_avg`, `all_day_stress_max`, `awake_stress_avg`, `asleep_stress_avg_uds` (4 columns from `daily_uds.csv` Wave-3 passthrough 2026-06-12). Upstream extractor: JSON-side propagation in `pipeline/03_consolidate/build_unified_dataset.py`. Source: `daily_uds.csv` from Garmin's UDS pre-aggregated stress fields. Day-validity gate: NaN when UDS missing the field on the day (~1% of S4 days). Sentinel handling: UDS-side cleaning happens upstream of this channel's appearance in the master. Calibration: no documented drift events; sharp -7.2 step at 2024-04-09 citalopram boundary, +5 step recovery at 2026-03-20 afbouw boundary -- both are documented intervention effects, NOT drift (added 2026-06-24 per descriptive `all_day_stress_avg/findings.md` Q3.2.h). Device: Forerunner 245 Elevate V3 throughout 2021-08-16 to present (no device change).

Surface to user for authorisation in a separate session per the discipline.

See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).

---

## Q3.2.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel

Discipline anchor: [HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) (secondary-logistic-with-covariate pattern; beta disambiguation between primary-signal and a candidate alternative reading). Names **four** candidate covariates a future HA on `all_day_stress_avg` as predictor should pre-spec:

### 1. `dose_plasma_mg(d)` -- obligatory under [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5.B

The channel is CONFIRMED dose-modulated at +0.565/mg p=0.000 (the LARGEST beta among the 3 CONFIRMED channels). A future HA MUST either section 5.A per-phase stratify or section 5.B dose-adjust. **HA-C3 v2 and HA-C3p both used the dual treatment** (section 5.A unmedicated headline as primary + section 5.B dose-adjusted cross-phase as sensitivity arm); both pre-regs' section 5.B sensitivity arms returned REJECTED at 0-of-3 conditions MET, while the section 5.A unmedicated headline carried the substantive verdicts (HA-C3 v2 REJECTED via wrong-direction override; HA-C3p PARTIAL). The operational consequence: **the section 5.A unmedicated headline is the load-bearing operationalisation choice** for HAs probing non-linearity or shape on this channel; the section 5.B numerical adjustment does NOT recover the unmedicated-pool inverted-U pattern. The covariate version (secondary logistic adding `dose_plasma_mg(d)` to a primary-channel logistic) is the framework-prescribed disambiguator for HAs that pool cross-phase.

Needed columns: `lc_phase` is in the master; `dose_plasma_mg(d)` is computed runtime per [`citalopram_dose_response/dose_response.py`](../../../analyses/garmin_exploration/intervention_effects/dose_response.py).

### 2. `stress_mean_sleep` -- sister CONFIRMED-citalopram channel (autonomic-load shared)

On Stratum 4 observed (this analysis Q3.2.e, n=1339): Pearson r=+0.522, Spearman rho=+0.404 between `all_day_stress_avg` and `stress_mean_sleep`. Sister CONFIRMED-citalopram channel (+0.43/mg beta on sleep-window stress mean vs +0.57/mg on this channel's 24h mean). Both load on the same autonomic-load family per dose-response v3 section 5.6.2 (autonomic-load axis: 24h mean + sleep-window mean both confirmed). The covariate disambiguates: is the all-day signal specifically driven by the **awake portion of the day** (beta_channel survives when sleep-mean enters) or by **shared autonomic tone** (beta_channel attenuates). The sleep-window vs 24h-window split IS the operational disambiguation.

### 3. `stress_low_motion_min_count_S60_Mlow` -- spike-form companion per CONVENTIONS section 3.5

On Stratum 4 observed (this analysis Q3.2.e, n=1358): Pearson r=+0.847, Spearman rho=+0.860 -- high but NOT near-identity. The covariate disambiguates: is the all-day stress signal driven by the **temporal density of above-threshold minutes** (beta_channel attenuates -- spike-count was doing the work) or by the **average level** (beta_channel survives -- the daily mean carries information beyond threshold-crossing count). This is the **spike-vs-mean disambiguator per CONVENTIONS section 3.5**.

### 4. `all_day_stress_avg_lagged_mean_14d(d) = mean(channel[d-14:d-1])` -- autocorrelation-vs-mechanism

Mirrors HA-P7 section 4.5.4 worked example. Per Q3.2.b the cutoff lag M=18 and E[L]\*=29.8; **the channel's autocorrelation horizon is LONGER than both sister channels' (12.6 sleep-mean; 21.1 count primitive)**, so a 14d lagged trailing mean is **NOT past the autocorrelation horizon** for this primitive. A consumer HA should prefer a **30d or 28d window** for this covariate on this channel specifically -- the descriptive substrate says the autocorrelation extends to ~M=18 cutoff, so the consumer-test pre-reg has discretion to set the window past the M cutoff with margin (~28-30d is the natural choice).

Reconciliation with CONVENTIONS section 3.2 `_lagged_lcera` family: `all_day_stress_avg` is **not** currently in the section 3.2 audit-hook list and has no `_lagged_lcera` materialised variant in `per_day_master.csv` as of 2026-06-24. The lagged-mean-14d covariate is a same-day-HA diagnostic built just past Q3.2.b's M cutoff; it does NOT substitute for section 3.2's longer trailing baseline window, which belongs in the HA's own z-scoring or covariate-adjustment layer.

### Recommendation for any HA pre-reg on this channel

Pre-spec all four covariates as **secondary sensitivity arms**. Concordance across the four secondaries = high confidence in the primary; divergence = the disambiguation is doing real work. The section 5.B citalopram-dose adjustment is **obligatory** per the framework AND per the HA-C3 cluster's load-bearing precedent (both HA-C3 v2 + HA-C3p locked dual section 5.A + section 5.B treatment); the other three are diagnostic. Per the **HA-C3 cluster's joint inverted-U finding**: HAs probing non-linearity on this channel should follow the HA-C3p result.md section 4 sensitivity-table template (section 5.A unmedicated headline + section 5.B dose-adjusted + z-score sensitivity + crash-drop + train/validate descriptive overlay + t+1 lagged variant).

---

## Cross-references

### HA-* tests that touch this channel (cite this analysis)

- **HA-C3 v2** (REJECTED at `a2b18ba` 2026-06-23, wrong-direction override): primary user of this channel as predictor (Wiggers-verbatim 30->40 anchor bin scheme). The descriptive substrate this analysis produces is the **load-bearing substrate for the HA's section 5.A unmedicated headline operationalisation choice** (per Q3.2.c quintile-bin distribution reproducing HA-C3p's right-shift observation + Q3.2.d phase-stratified medians documenting the citalopram-axis dynamics + Q3.2.b E[L]\*=29.8 contextualising the HA's bin-label-sequence E[L]\* derivation). The HA's REJECTED verdict via wrong-direction override is NOT extended or promoted by this analysis per CONVENTIONS section 2.1.
- **HA-C3p** (PARTIAL at `e5a63fe` 2026-06-23): sister pre-reg testing the underlying convex-shape claim on personal-baseline-anchored quintile bins. The descriptive substrate this analysis produces **reproduces HA-C3p's section 2 right-shift unmedicated bin observation EXACTLY** (Q3.2.c quintile counts [45, 80, 129, 138, 189]) and extends it with share-ratio quantification (Q5 unmed/full = 1.45). The HA-C3p PARTIAL verdict + 4-cell-matrix consolidated reading ("Wiggers' numbers wrong-for-this-participant but the underlying SHAPE IS REAL in the INVERSE direction") is NOT extended or promoted by this analysis.
- **HA-P6 v3** (descriptive Layer 1): includes this channel in its 7-channel set as the distinguishable channel from Arm-A matched control. The descriptive substrate this analysis produces (E[L]\*=29.8 longer than any sister; episode-level crash signal CI brushing zero; sharp citalopram-boundary step + full afbouw recovery) provides context for the HA-P6 result reading on this specific channel.
- **HA-C4 v2** (REJECTED at `52bddb5` 2026-06-18): primary daily-aggregate triad on the 3 CONFIRMED-citalopram autonomic channels (including this one as Ch1). The descriptive substrate this analysis produces (episode-level d=+0.37 with CI brushing zero) constrains the post-rejection re-interpretation: did this channel specifically lack signal at the episode level on the v2-locked operationalisation? **This analysis confirms YES** -- the channel does NOT carry a robust episode-level signal at as-of-date 2026-06-05 with E[L]=7 OR E[L]=30; the day-level signal exists but autocorrelation-inflated.

### Methodology MDs cited

- [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) -- Q3.2.a delegate target (partial; extended for the full skewness/kurtosis/heavy-tail-flag set on this channel).
- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) sections 3-6 -- Q3.2.c phase axis, Q3.2.d phase-stratified treatment, Q3.2.i covariate framework.
- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) v3 section 5.6.1 -- locked +0.565/mg dose-response slope (largest beta among 3 CONFIRMED channels); section 5.6.2 autonomic-load family.
- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) -- E[L]=7 default + factor-of-2 deviation rule; Q3.2.b fires factor-of-4 (the largest deviation in Strand A).
- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) -- Q3.2.h cross-reference; **per-column row for all-day stress family is missing** (PROPOSE-ONLY).
- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) -- Stratum 4 boundary definition.

### Existing artefacts referenced

- [`descriptive/operationalisation_support/stress_mean_sleep/findings.md`](../stress_mean_sleep/findings.md) -- sister CONFIRMED-citalopram channel; first Phase-1 Strand A analysis; cross-channel comparison anchors throughout (E[L]\* 29.8 here vs 12.6 there; episode-level d +0.37 here vs +0.91 there; heavy-tail-flag False here vs True there).
- [`descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/findings.md`](../stress_low_motion_min_count_S60_Mlow/findings.md) -- spike-form companion per CONVENTIONS section 3.5; third Phase-1 Strand A analysis; cross-pair r=+0.85 / rho=+0.86 reciprocally confirmed; the continuous-vs-spike pair on this channel.
- [`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/) -- v2 LANDED 2026-06-22 (`8feae6a`); the afbouw-reversal finding per section 5.A sub-stratification cross-references the Q3.2.c + Q3.2.d afbouw-median recovery observation on this channel.
- [`analyses/hypotheses/HA-C3/result.md`](../../hypotheses/HA-C3/result.md) -- HA-C3 v2 REJECTED 2026-06-23; primary user of this channel.
- [`analyses/hypotheses/HA-C3p/result.md`](../../hypotheses/HA-C3p/result.md) -- HA-C3p PARTIAL 2026-06-23; right-shift section 2 observation reproduced + extended in Q3.2.c.
- [`analyses/garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) -- Q3.2.e cross-reference; new near-miss pair `all_day_stress_avg <-> bb_lowest` rho=-0.75 surfaced for next refresh (flag-only).
- [`analyses/garmin_exploration/stress_low_motion_viz/family_a_daily.py`](../../../analyses/garmin_exploration/stress_low_motion_viz/family_a_daily.py) -- the 2023-11-29 named-exemplar peak-crash day that fires as this channel's sole MAD-z>5 outlier (Q3.2.h).

### Upstream pipeline

- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `daily_uds.csv` (Wave-3 JSON-side passthrough 2026-06-12 per `garmin_indicators_audit.md`). NO custom FIT extraction for this channel.
- `labels_crash_v2.csv` <- `garmin/hypotheses/crash_v2-definition/definition.md` (locked).

---

## Limitations

For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding limitations a downstream HA pre-reg author should carry forward are:

1. **Q3.2.c-d are on raw channel values, not dose-adjusted.** Per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5, any HA using `all_day_stress_avg` cross-phase MUST adopt section 5.A / 5.B / 5.C treatment. The HA-C3 cluster's load-bearing precedent (both v2 + HA-C3p) is dual section 5.A unmedicated headline + section 5.B dose-adjusted sensitivity. Q3.2.d explains the citalopram-axis dynamics descriptively; a section 5.B dose-adjusted phase comparison is the natural follow-up but lives in the HA pre-reg, not here.
2. **The channel IS a 24h-window daily mean** (Q3.2.g) per CONVENTIONS section 3.5 -- dilution-vulnerable for acute-load mechanisms. A future HA whose mechanism is *acute spike-during-rest* should use `stress_low_motion_min_count_S60_Mlow` (the spike-form companion at r=+0.85 / rho=+0.86) as primary; this channel is the continuous-form cousin.
3. **The episode-level Cohen's d=+0.37 has bootstrap CI brushing zero** (Q3.2.f). The episode-level is the unit-of-analysis-clean read per CONVENTIONS section 3.6; consumer HAs using this channel as a crash-discriminator should NOT rely on the day-level d=+0.68 (autocorrelation-inflated) as the primary read. The signal exists but is weak at the episode level on this corpus at as-of-date 2026-06-05.
4. **The autocorrelation horizon is the LONGEST in Strand A** (Q3.2.b E[L]\*=29.8 vs 12.6 sleep-mean / 21.1 count primitive). Consumer tests using this channel with auto-correlation-controlled methods MUST use a longer block-length than the project default; the factor-of-4 deviation is the largest yet observed. The HA-C3 cluster's bin-label-sequence E[L]\* derivation (=7.0, "no flags") is a different frame; both are correct in their respective frames (raw channel vs binned derivative).
5. **The outlier-rule MAD-z|>5 is a descriptive-stage screen** (Q3.2.h) -- the single firing day (2023-11-29) is the cross-channel-consistent peak-crash exemplar; downstream HA tests must NOT trim it.
6. **The afbouw-recovery finding is descriptively striking but Layer-1 only**: afbouw median 34.0 = unmedicated median 34.0 exactly. The substantive afbouw-reversal interpretation lives in `recovery_arc v2` analysis ([`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/) section 5.A); this analysis's Q3.2.d corroborates it descriptively but does NOT extend or promote the substantive reading.
7. **The `garmin_indicators_audit.md` per-column row for the all-day stress family is missing** (Q3.2.h). Proposed row content surfaced; do NOT apply without user authorisation per handoff discipline section 3.
8. **The HA-C3 cluster verdicts are LOCKED at REJECTED + PARTIAL with consolidated joint reading.** This analysis's Q3.2.c quintile-bin reproduction + Q3.2.d phase-stratified observation are **descriptive corroboration only**; the HA-C3 cluster's inverted-U finding is NOT extended by this analysis per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). Future HA-C3 v3 / HA-C3p v2 alternative-shape pre-regs would be a separate authorship session per `hypothesis_lock_process.md` section 3.2 redraft discipline.

---

## Status

**Current as of 2026-06-24** (commit context: post-`ccbd12e` descriptive programme lock; Phase 2 "finish the descriptive analysis" Tier 1 user-prioritised CONFIRMED-citalopram channel #2; R14 `single_pool_reanchor` landed first at `badd04a`; `bb_lowest` next). Refresh when:

1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to spin up (per CONVENTIONS section 3.1 personal-baseline freshness).
2. A new citalopram-phase boundary lands (e.g. post-afbouw enters analytic scope as of 2026-06-06 onward).
3. The Politis-White E[L]\* shifts by another factor of 2 from current 29.8 (factor-of-4-vs-default flag already fired).
4. The `all_day_stress_avg <-> bb_lowest` near-miss pair (Q3.2.e rho=-0.75) gets propagated into the cross-channel-correlation card's 7-channel panel.
5. The `garmin_indicators_audit.md` per-column row for the all-day stress family gets added with the proposed content (Q3.2.h flag).
6. An HA-C3 v3 / HA-C3p v2 alternative-shape pre-reg spins up and surfaces new operationalisation choices on this channel that would change the per-channel descriptive substrate.
