# Findings -- `bb_lowest` operationalisation-support descriptive (Q3.3.a-k)

**Channel**: `bb_lowest` (CONFIRMED-citalopram, -1.134/mg p=0.000 buildup post-CPAP per [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) v3 section 5.6.1 -- the **largest absolute beta** among the 3 CONFIRMED channels in INVERSE direction; citalopram RAISES bb_lowest, i.e. better overnight floor under medication). Column semantics: [DATA_DICTIONARY.md Body Battery section](../../../DATA_DICTIONARY.md) -- daily NADIR of Garmin Body Battery UDS-pre-aggregated stat (lowest BB value observed across the 24h window), JSON-passthrough from `daily_uds.csv` per [`garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) Wave-3 propagation 2026-06-12 (no FIT parsing).

**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to 2026-06-05). n=1359 days with channel out of 1372 Stratum 4 days (13 NaN days from UDS-side coverage gaps).

**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.3 (LOCKED 2026-06-18 r3, commit `ccbd12e`) -- this analysis is the **third (final) of the 3 CONFIRMED-citalopram channels in the Tier 1 user-prioritised Phase 2 sequential batch** (R14 `single_pool_reanchor` first at `badd04a`; `all_day_stress_avg` second at `cf34ab1`; this bb_lowest third; `stress_stdev_sleep` closes Tier 1 next). Q3.3.a-i template applied per section 3.1 verbatim + Q3.3.j + Q3.3.k channel-specific extensions per section 3.3.

**Sources**: `per_day_master.csv` (Garmin daily aggregate) + `labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level per CONVENTIONS section 3.6).

**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). HA10 (BB overnight recharge; LOCKED OVERALL-REFUTED with R14 single-pool re-anchor CONVERGE-ON-OVERALL) + HA-P6 v3 (LOCKED; bb_lowest is one of 4/7 distinguishable channels) + HA-C4b (BB-floor candidate; DEFERRED per STOCKTAKE section 6) cross-references in this analysis are **descriptive corroboration only**; the substantive verdicts live in those result.md files and are NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). Statistical hygiene anchors: section 3.1 (personal baseline), section 3.3 (column-duplication threshold |rho|>=0.92), section 3.4 (crash-drop sensitivity |delta|>0.10), section 3.5 (spike metrics -- bb_lowest IS the spike-form NADIR primitive on the BB-floor construct; not a 24h mean), section 3.6 (named counts).

---

## Headline

`bb_lowest` on Stratum 4 is a **mildly right-skewed, autocorrelation-DENSE daily-NADIR channel** (skew=+0.42, excess kurtosis=+0.45, heavy_tail_flag=False, p99/median = 43/20 = 2.17). The **data-driven E[L]\*=29.2** (Politis-White; deviation ratio 3.18; factor-of-2 flag = True; cutoff lag M=18). Cross-channel context: vs sister CONFIRMED-citalopram channels `stress_mean_sleep` E[L]\*=12.6 + `all_day_stress_avg` E[L]\*=29.8 + spike-companion `stress_low_motion_min_count_S60_Mlow` E[L]\*=21.1 -- this channel sits at longer autocorrelation. The **phase-stratified medians track the recovery_arc v2 section 5.A trajectory faithfully**: unmedicated median 18.0 -> buildup 26.0 -> consolidation 22.0 -> **afbouw 15.0** (citalopram lifts the floor through buildup + consolidation, then the afbouw phase GOES LOWER than even unmedicated baseline -- the load-bearing reversal finding per [recovery_arc v2 findings.md section 5.A](../../trajectory/recovery_arc/findings.md) + [STOCKTAKE section 6 line 187](../../../STOCKTAKE.md)). Day-resolved citalopram boundary step (2024-04-09 pre/post 30d) is **+8.17 BB units**; afbouw boundary step (2026-03-20 pre/post 30d) is **-5.77 BB units** -- the latter shows the empirical afbouw drop in day-resolved form. Crash-vs-normal: episode-level d=-0.30 (bootstrap CI95 [-5.45, +0.36]); day-level Mann-Whitney U z=-4.05 p=<0.0001 P(crash>normal)=0.380. Near-identity check: zero near-identity pairs at the |rho|>=0.92 CONVENTIONS section 3.3 threshold. Q3.3.j: bb_lowest has full corpus coverage from 2021-08-17 onward (98.7% of corpus rows) -- contrast with bb_overnight_gain (2024-09-18 onset; 33.8% of corpus). Q3.3.k: bb_overnight_gain pairing rho values reported in section Q3.3.k below.

---

## Q3.3.a -- Distribution shape (Stratum 4)

**Verdict on the section 3.1 delegate question**: **delegate is partial; extend in this analysis**. [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) was extended for continuous channels first and primarily documents `stress_mean_sleep`; coverage on `bb_lowest` is incidental. The full distribution descriptors (skewness/kurtosis/heavy-tail flag/p99-vs-median ratio) are surfaced here for the first time on this channel.

| stat | value | source |
|---|---:|---|
| n (Stratum 4) | 1359 | `per_day_master.csv` `bb_lowest` non-NaN within S4 |
| mean | 20.61 | (single-pool S4) |
| median | 20.00 | |
| std (ddof=1) | 8.80 | |
| MAD (unscaled) | 6.00 | |
| MAD x 1.4826 (normal-equivalent SD) | 8.90 | for robust z-score scaling per section 3.1 |
| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | 5.0 / 6.0 / 9.0 / 15.0 / 20.0 / 26.0 / 32.0 / 35.1 / 43.4 | |
| skewness (Fisher-Pearson) | **+0.42** | mildly right-skewed (NADIR channel; lower-bounded near 5) |
| excess kurtosis (Fisher) | **+0.45** | |
| heavy_tail_flag | **False** | skew>1 OR p99/median > 3.0 |
| range | 5.0 to 69.0 | BB values bounded 0-100 (Garmin scale); the channel sits in the lower half of that range |

### Cross-channel comparison vs sister CONFIRMED-citalopram channels

| stat | bb_lowest (this analysis) | all_day_stress_avg (Q3.2) | stress_mean_sleep (Q3.1) |
|---|---:|---:|---:|
| n S4 | 1359 | 1359 | 1339 |
| mean | 20.61 | 32.72 | 19.97 |
| median | 20.00 | 32.00 | 19.21 |
| MAD (unscaled) | 6.00 | 4.00 | 2.87 |
| skewness | +0.42 | +0.87 | +2.72 |
| heavy_tail_flag | **False** | **False** | **True** |

**bb_lowest is a daily NADIR (already an extreme-of-day extremum) operationally distinct from the 24h-mean stress channels.** Per CONVENTIONS section 3.5 the NADIR IS the spike-form on the BB-floor construct; it is not dilution-vulnerable in the same way as the sister stress channels' 24h-window means. The complementary BB extremum is bb_highest (peak); the recharge arc (bb_overnight_gain = SLEEPEND - SLEEPSTART) is a separate compound primitive (Q3.3.k).

See [`plots/fig1_distribution_s4.png`](plots/fig1_distribution_s4.png).

---

## Q3.3.b -- Autocorrelation structure + E[L]\*

The **data-driven block length is E[L]\*=29.2** (Politis-White 2004 with Patton-Politis-White 2009 correction per [`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) vs the project default E[L]=7 per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). The **factor-of-2 deviation flag = True** (deviation ratio = 3.18). Cutoff lag M=18.

| lag (days) | autocorrelation |
|---:|---:|
| 1 | +0.484 |
| 2 | +0.256 |
| 3 | +0.210 |
| 7 | +0.234 |
| 14 | +0.168 |

Politis-White 2-sigma significance threshold (n=1359): |rho| = 0.146.

### Cross-channel comparison (E[L]\* by Strand A analysis)

| analysis | channel | E[L]\* | M | factor-of-2 flag |
|---|---|---:|---:|---|
| Phase-1 #1 (stress_mean_sleep) | sleep-window mean | 12.6 | 6 | YES (factor-of-2) |
| Phase-1 #3 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 | 11 | YES (factor-of-3) |
| Phase-2 #2 (all_day_stress_avg) | 24h-window mean | 29.8 | 18 | YES (factor-of-4) |
| **this analysis (bb_lowest)** | **daily NADIR** | **29.2** | **18** | **YES** |

**Implication**: any HA pre-reg using `bb_lowest` should pre-spec a sensitivity arm at E[L]\*=29 alongside the default-E[L]=7 primary. Per Q3.3.b's data-driven estimate the channel's serial dependence sits at the autocorrelation horizon reported in the cross-channel table above. The mechanistic interpretation: bb_lowest inherits long-range trend structure from the multi-year recovery arc (lift 12 -> 22 across phases per recovery_arc v2 section 2) + the citalopram trajectory (section 5.A within-phase-5 sub-cells); the autocorrelation reflects both day-to-day serial dependence and the slow trajectory absorption.

See [`plots/fig5_acf.png`](plots/fig5_acf.png).

---

## Q3.3.c -- Base rates per citalopram phase

Phase axis per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3:

| phase | window | n | median | mean | MAD | p10 / p90 |
|---|---|---:|---:|---:|---:|---|
| unmedicated | 2022-09-03 to 2024-04-08 | 581 | **18.00** | 18.46 | 5.00 | 8.0 / 28.0 |
| buildup | 2024-04-09 to 2024-06-19 | 72 | **26.00** | 26.07 | 5.00 | 17.1 / 36.0 |
| consolidation | 2024-06-20 to 2026-03-19 | 635 | **22.00** | 22.40 | 6.00 | 10.0 / 34.0 |
| afbouw | 2026-03-20 to 2026-06-05 | 71 | **15.00** | 16.73 | 5.00 | 6.0 / 25.0 |

The two **transition phases** (buildup n=72; afbouw n=71) have **n<75 each**; the two **steady-state phases** (unmedicated n=581; consolidation n=635) are an order of magnitude larger. Any HA test that wants per-phase verdicts under [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5.A on buildup or afbouw faces a ~10x n disadvantage vs the steady-state phases (same as sister channels Q3.1.c / Q3.2.c).

Named counts (CONVENTIONS section 3.6): the per-phase n's above are `bb_lowest`-non-NaN day rows in `per_day_master.csv` within Stratum 4 date masks per `citalopram_phase_stratification.md section 3` boundary dates.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (citalopram-phase violins).

---

## Q3.3.d -- Phase-stratified distribution + citalopram step magnitude vs natural variation

**This is the most operationally consequential finding for downstream HA pre-regs on this channel, AND the location of the load-bearing recovery_arc v2 afbouw-reversal cross-reference.**

The locked dose-response anchor (v3 section 5.6.1): **buildup post-CPAP beta = -1.134/mg p=0.000** (the **LARGEST ABSOLUTE beta** among the 3 CONFIRMED-citalopram channels in INVERSE direction: `stress_mean_sleep` +0.43/mg, `all_day_stress_avg` +0.57/mg, this channel -1.13/mg). The sign convention: citalopram **raises** bb_lowest (better overnight floor under medication). Naive extrapolation: at 30mg steady-state (consolidation), the implied citalopram-attributable lift is -(-1.134) x 30 = **+34.02 BB units** -- larger than the channel's full interquartile range (p75 - p25 = 11) **TRIPLED**, and ~5+ standard deviations on the consolidation-phase MAD.

Observed steady-state level shifts (median):

| comparison | delta median | within-phase MAD | within-MAD? |
|---|---:|---:|---|
| buildup minus unmedicated | **+8.0** | 5.0-5.0 | citalopram lift visible at buildup |
| consolidation minus unmedicated | **+4.0** | 6.0 | citalopram lift sustained at steady-state |
| consolidation minus buildup | **-4.0** | 6.0 | the v2 recovery_arc 26 -> 22 trajectory within phase 5 |
| afbouw minus consolidation | **-7.0** | 6.0-5.0 | the afbouw collapse |
| afbouw minus unmedicated | **-3.0** | 5.0-5.0 | the load-bearing reversal cell |

### Reading the direction -- what the data shows + the load-bearing recovery_arc v2 reversal

The median **lifts substantially during citalopram phases** (unmedicated 18.0 -> buildup 26.0 -> consolidation 22.0; consistent with the citalopram-raises-bb_lowest direction). The day-resolved citalopram boundary step (30d pre vs post the 2024-04-09 boundary): **+8.17 BB units** -- the empirical day-resolved citalopram-onset effect on the channel.

**The afbouw cell (median 15.0) is the load-bearing finding.** Per [recovery_arc v2 findings.md section 5.A](../../trajectory/recovery_arc/findings.md) the within-phase-5 citalopram-axis sub-cells were reported as **buildup 26 -> consolidation 22 -> afbouw 15** -- afbouw COLLAPSES BELOW the pacing-4b baseline of 18 (the established post-pacing-habit BB-floor level). This analysis's afbouw-minus-consolidation diff (-7.0) + afbouw-minus-unmedicated diff (-3.0) REPRODUCE the v2 recovery_arc afbouw-LOWER-than-baseline pattern at the citalopram-axis-only stratification. The day-resolved afbouw boundary step (30d pre/post 2026-03-20): **-5.77 BB units** -- the empirical day-resolved afbouw-onset effect.

### OPPOSITE-direction contrast with sister `all_day_stress_avg` afbouw-fully-recovers

Per handoff section 2.4 + section 5.A of recovery_arc v2: bb_lowest's afbouw pattern is **OPPOSITE-direction from sister `all_day_stress_avg`'s afbouw-fully-recovers finding**:

| channel | unmed median | buildup median | consolidation median | afbouw median | afbouw vs unmed | reversal pattern |
|---|---:|---:|---:|---:|---:|---|
| `stress_mean_sleep` (Q3.1) | 17.04 | -- | 19.07 | 20.20 | +3.16 | afbouw HIGHER than unmed (citalopram benefit reverses) |
| `all_day_stress_avg` (Q3.2) | 34.0 | 28.5 | 31.0 | 34.0 | 0.0 | afbouw FULLY RECOVERS to unmed baseline |
| **`bb_lowest` (this analysis)** | **18.0** | **26.0** | **22.0** | **15.0** | **-3.0** | afbouw GOES LOWER THAN unmed baseline -- INVERTS |

**This is the substantive cross-channel observation per handoff section 2.4 + STOCKTAKE section 6 line 187**: on the 3 CONFIRMED-citalopram channels at this corpus snapshot, the afbouw pattern is **channel-specific** -- some channels recover toward unmed baseline (all_day_stress_avg), some go HIGHER (stress_mean_sleep, consistent with the +β prior), and bb_lowest INVERTS to BELOW unmed baseline (NOT just the inverse of stress channels' afbouw-rises; it goes LOWER than the unmedicated floor). Three readings, none asserted as substantive truth per CONVENTIONS section 2.1 + section 4.3:

1. **The beta is a within-buildup-window dose-trend, not a between-phase steady-state level shift.** The v3 dose-response MD's beta is the slope of `bb_lowest` against `dose_plasma_mg(d)` *within* the buildup-window (2024-04-09 to 2024-06-19); it measures how the channel changes as dose rises from 0 to 30mg over ~70 days. Across phases, the LC-trajectory's broader recovery arc PLUS the citalopram step PLUS pacing-practice strengthening all overlap; the between-phase level shift can move opposite to the within-window beta if the broader trajectory dominates. The recovery_arc v2 analysis ([`descriptive/trajectory/recovery_arc/`](../../trajectory/recovery_arc/)) documents this trajectory at multi-channel detail.

2. **The dose-adjusted-predictor pattern under [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5.B is the framework-prescribed cross-phase treatment**: predictor = `bb_lowest - (-1.134)*dose = bb_lowest + 1.134*dose`. Any HA-C4b BB-floor pre-reg considering this channel cross-phase MUST adopt one of section 5.A / 5.B / 5.C per the inheritance table in `citalopram_phase_stratification.md section 4` (this channel is load-bearing CONFIRMED).

3. **The afbouw reversal IS the multi-year-trajectory signature**: per recovery_arc v2 section 5.A this channel is the standout where citalopram benefit doesn't just disappear during dose reduction, it inverts. The afbouw median 15.0 sits BELOW even the unmedicated baseline 18.0 -- a graded buildup -> consolidation -> afbouw downward arc that continues past the unmedicated baseline. Note: this is a Layer 1 observation; the recovery_arc analysis is the load-bearing artefact for substantive readings.

### HA10 single-pool re-anchor descriptive cross-reference (load-bearing per handoff section 2.4)

HA10 (BB overnight recharge proxy, primary channel `bb_highest`) is LOCKED at TRAIN REFUTED (-20.5 pp) / VALIDATE SUPPORTED (+16.2 pp) / OVERALL REFUTED with era-directionality reversal. R14 single_pool_reanchor (LANDED `badd04a`) showed this directionality reversal **flattens cleanly under single-pool re-anchor to +4.1 pp [CI -16.5, +16.8], perm p=0.4328, NOT-SUPPORTED CONVERGE-ON-OVERALL**. The descriptive substrate this analysis produces -- the per-phase signal in Q3.3.c + the citalopram-axis trajectory in Q3.3.d (unmed 18.0 -> buildup 26.0 -> consolidation 22.0 -> afbouw 15.0) -- **descriptively corroborates** the R14 reading that the era-directionality reversal is consistent with a per-phase (per-citalopram-state) effect rather than a true per-era effect, because the LC era contains the unmedicated-to-citalopram-buildup boundary that the train-vs-validate split happens to straddle. The substantive HA10 verdict + the R14 single-pool verdict are LOCKED; this Q3.3.d descriptive observation is NOT a re-interpretation of either.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) and [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d rolling median through phases).

---

## Q3.3.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)

Brief-mandated three channels (sister stress_mean_sleep + all_day_stress_avg + bb_overnight_gain) plus extended biologically-plausible neighbours (BB family + stress family + cardiovascular). The bb_overnight_gain pair appears here AND in Q3.3.k channel-specific extension for parity.

| target channel | n | Pearson r | Spearman rho | near-identity flag? |
|---|---:|---:|---:|---|
| `stress_mean_sleep` | 1339 | -0.425 | -0.423 | no |
| `all_day_stress_avg` | 1359 | -0.727 | -0.749 | no |
| `bb_overnight_gain` | 593 | +0.197 | +0.214 | no |
| `bb_highest` | 1359 | +0.508 | +0.487 | no |
| `bb_sleep_start_value` | 667 | +0.483 | +0.508 | no |
| `bb_sleep_end_value` | 593 | +0.560 | +0.525 | no |
| `bb_during_sleep_value` | 861 | +0.199 | +0.206 | no |
| `bb_overnight_gain_proxy` | 667 | +0.174 | +0.179 | no |
| `bb_overnight_gain_best` | 667 | +0.183 | +0.190 | no |
| `stress_low_motion_min_count_S60_Mlow` | 1358 | -0.597 | -0.620 | no |
| `stress_stdev_sleep` | 1339 | -0.409 | -0.381 | no |
| `awake_stress_avg` | 1359 | -0.689 | -0.689 | no |
| `resting_hr` | 1357 | -0.194 | -0.171 | no |

**Zero near-identity pairs fire** at the |rho|>=0.92 CONVENTIONS section 3.3 threshold. The closest pairs and their substantive context live in Q3.3.k below for the bb_overnight_gain family; sister all_day_stress_avg rho-with-this-channel reciprocally confirms the rho=-0.749 inverse-direction signal reported in all_day_stress_avg Q3.2.e.

---

## Q3.3.f -- Crash-day vs normal-day (Stratum 4 refresh in operationalisation-support framing)

Per CONVENTIONS section 3.6 named counts: 29 crash-episodes (crash_v2 episode-level via `labels_crash_v2.csv` unique `episode_id` starting with `crash-`); 103 crash-days (day-level, `label=='crash'`); 1256 non-crash days (the complement within Stratum 4 channel-valid days).

### Episode-level (primary unit per CONVENTIONS section 3.6)

| stat | value |
|---|---:|
| n crash-episodes | 29 |
| n normal-day base rate | 1256 |
| mean per-episode `bb_lowest` | 18.26 |
| mean normal-day `bb_lowest` | 20.88 |
| mean diff (episode minus normal-day) | **-2.62** |
| Cohen's d (episode-level vs normal-day pooled) | **-0.30** |
| Bootstrap 95% CI on mean diff | **[-5.45, +0.36]** (5000 iters, seed=20260624) |

**Episode-level Cohen's d=-0.30** on this channel. Substantive direction prior: bb_lowest LOWER on crash days = depleted overnight floor (the Wiggers-aligned direction). Compare cross-channel: `stress_mean_sleep` episode d=+0.91 (sister +direction); `all_day_stress_avg` episode d=+0.37 with CI brushing zero; `stress_low_motion_min_count_S60_Mlow` episode d=+0.38.

### Day-level (autocorrelation-inflated supplementary)

| stat | value |
|---|---:|
| n crash-days | 103 |
| n normal-days | 1256 |
| mean crash-day | 17.31 |
| mean normal-day | 20.88 |
| median crash-day | 17.0 |
| median normal-day | 20.0 |
| mean diff (point estimate) | **-3.57** |
| median diff | **-3.0** |
| Cohen's d | **-0.41** |
| Mann-Whitney U: z | **-4.05** |
| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **<0.0001** |
| Mann-Whitney U: P(crash > normal) | **+0.380** |
| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (project default) | [-6.75, -0.24], width 6.51 |
| Stationary bootstrap 95% CI on mean diff, **E[L]=29** (data-driven, Q3.3.b flag) | **[-7.21, -0.01]**, width 7.20 |

### HA10 single-pool re-anchor cross-reference (load-bearing per handoff section 2.4)

Per the R14 single_pool_reanchor result on HA10 (BB-recharge channel, NOT bb_lowest directly): the era-directionality reversal flattens to +4.1 pp CONVERGE-ON-OVERALL. **This analysis's crash-vs-normal read on bb_lowest is the floor-side companion to HA10's peak-side test.** The episode-level signal observed here (d=-0.30 on the floor) provides cross-construct context for any HA-C4b BB-floor pre-reg that wants to use bb_lowest as primary; that pre-reg should adopt section 5.A / 5.B / 5.C per the citalopram-phase inheritance rule (Q3.3.i covariate-readiness arm 1) AND should pre-spec the long-autocorrelation E[L]\*=29 block-length sensitivity per Q3.3.b.

### Block-length sensitivity (Q3.3.b cross-check)

Per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md), when the data-driven E[L]\* deviates from the project default by more than a factor of 2, the analysis must report the CI at the data-driven value alongside the default. E[L]=29 CI ([-7.21, -0.01]) vs E[L]=7 CI ([-6.75, -0.24]) -- 10.5% wider at the data-driven block length.

### Crash-drop sensitivity (CONVENTIONS section 3.4)

| frame | Spearman rho | n |
|---|---:|---:|
| full Stratum 4 | +0.010 | 1359 |
| crash-days dropped | -0.048 | 1256 |
| \|delta\| | **0.058** | -- |
| section 3.4 threshold (0.10) crossed? | **no** | -- |

See [`plots/fig4_crash_vs_normal.png`](plots/fig4_crash_vs_normal.png).

---

## Q3.3.g -- Spike-detecting primitive availability

`bb_lowest` is **structurally the daily NADIR** (UDS-pre-aggregated; JSON-passthrough from `daily_uds.csv`; no FIT parsing per `garmin_indicators_audit.md` Wave-3 propagation 2026-06-12). Per CONVENTIONS section 3.5 it IS the spike-form primitive on the BB-floor construct (the depleted-state extremum of the day); it is NOT a dilution-vulnerable continuous-mean form like the sister stress channels' 24h-window means. Sub-daily BB resolution is **not in `per_day_master.csv`** and NOT in the GDPR dump per [bb_overnight_gain_proxy.md section 6 caveat 5](../../../methodology/bb_overnight_gain_proxy.md).

BB-related primitives in the master:

| column | n_non_nan (S4) | type | relation to `bb_lowest` |
|---|---:|---|---|
| `bb_highest` | 1359 | daily peak (24h max) | Pearson r=**+0.51** / rho=+0.49; complementary BB extremum |
| `bb_sleep_start_value` | -- | anchor: BB at sleep start | Pearson r=**+0.48** / rho=+0.51; the recharge-arc starting point |
| `bb_sleep_end_value` | -- | anchor: BB at sleep end | Pearson r=**+0.56** / rho=+0.52; the recharge-arc ending point |
| `bb_during_sleep_value` | -- | sleep-window-averaged BB | Pearson r=**+0.20** / rho=+0.21 |
| `bb_overnight_gain` | -- | SLEEPEND - SLEEPSTART (recharge arc) | Pearson r=**+0.20** / rho=+0.21; HA10 primary (Q3.3.k) |
| `bb_overnight_gain_best` | -- | best (truth + proxy) recharge | Pearson r=**+0.18** / rho=+0.19; coverage-extended HA10 |

### CONVENTIONS section 3.5 framing -- the NADIR IS the spike-form on the BB-floor construct

Unlike the sister stress channels where the continuous-form (24h mean) and spike-form (low-motion-count, max-spike-minutes) live in separate columns, **bb_lowest is a single extremum-form column**: the depleted-state floor reached at any point in the 24h window. A consumer test whose mechanism is *acute BB-floor depletion* should use bb_lowest as primary -- it IS the extremum operand. A consumer test whose mechanism is *overnight recharge magnitude* should use bb_overnight_gain (Q3.3.k) as primary. A consumer test whose mechanism is *daily peak* should use bb_highest (HA10 primary).

**Latent in FIT, not in master**: per-minute body-battery samples are absent from the GDPR dump entirely per [bb_overnight_gain_proxy.md section 6 caveat 5](../../../methodology/bb_overnight_gain_proxy.md) ("No per-minute BB anywhere in the dump"). Within-day BB-spike-density at finer-than-daily resolution is structurally unavailable; this is not a project-side extraction gap but a Garmin-side data-export gap. This analysis does NOT action it.

---

## Q3.3.h -- Outlier detection + calibration-drift check

Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) + load-bearing [`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md):

- This channel is a **UDS-side passthrough** from `daily_uds.csv`; no FIT parsing needed; part of the Body Battery family extracted via Wave-3 JSON-side propagation 2026-06-12.
- **No specific calibration-drift events catalogued for `bb_lowest`** in `garmin_indicators_audit.md`; the audit's per-column provenance map covers BB channels collectively under the UDS-passthrough rows rather than per-column for the daily-aggregate floor.
- Underlying sensor is **Forerunner 245 Elevate V3 throughout the entire 2021-08-16 to present window** -- no device change in the analytic window. Per bb_overnight_gain_proxy.md section 6 caveat 1 the single-watch / single-firmware-family discipline extends to all BB columns.
- **Coverage-bridge framing applied (load-bearing per handoff section 2.4)**: bb_overnight_gain_proxy.md establishes r=0.989 vs truth post-2024-09-18 + sensitivity-only for the 2024-07-08 -> 2024-09-17 bridge window. bb_lowest itself has NO equivalent rollout gap (Q3.3.j confirms full corpus coverage from 2021); the coverage-bridge discipline applies to bb_overnight_gain pairing (Q3.3.k), not to bb_lowest directly.

### Outlier scan (MAD-based |z|>5; threshold per CONVENTIONS section 3.1 robust-baseline default)

**1 outlier-day flagged** out of 1359:

| date | value | MAD-z |
|---|---:|---:|
| 2024-11-22 | 69.0 | **+5.51** |

### Drift check -- rolling 90d median over Stratum 4

| snapshot date | rolling 90d median |
|---|---:|
| 2022-12-01 | 19.0 |
| 2023-06-01 | 16.0 |
| 2023-12-01 | 18.0 |
| 2024-06-01 | 25.0 |
| 2025-01-01 | 26.0 |
| 2025-12-01 | 23.5 |
| 2026-04-01 | 17.0 |

The rolling 90d median shows the multi-year lift documented in recovery_arc v2 (12 healthy -> 22 phase 5 maximum), and the day-resolved citalopram boundary step (2024-04-09) shows trailing-30d mean = 22.60 vs leading-30d mean = 30.77 -- a **+8.17 step**, ~1.4 channel-MADs. The consolidation-boundary step at 2024-06-20 shows 22.27 -> 20.20 = **-2.07**. The **afbouw boundary step at 2026-03-20 shows 20.23 -> 14.47 = -5.77** -- the day-resolved afbouw drop in the same window where recovery_arc v2 section 5.A surfaces the load-bearing reversal.

**This is NOT a calibration-drift signature** -- the shifts are precisely time-located at documented intervention boundaries (citalopram dose ramp + afbouw onset), and the multi-year lift aligns with the documented LC recovery arc. A calibration-drift signature would be a gradual monotonic creep unrelated to documented events; this channel shows the opposite -- structured shifts at known boundaries.

See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).

---

## Q3.3.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel

Discipline anchor: [HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) (secondary-logistic-with-covariate pattern; beta disambiguation between primary-signal and a candidate alternative reading). Names **four** candidate covariates a future HA on `bb_lowest` as predictor should pre-spec:

### 1. `dose_plasma_mg(d)` -- obligatory under [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5.B

The channel is CONFIRMED dose-modulated at -1.134/mg p=0.000 (the LARGEST ABSOLUTE beta among the 3 CONFIRMED channels in INVERSE direction). A future HA MUST either section 5.A per-phase stratify or section 5.B dose-adjust. The section 5.B operationalisation on this channel: `bb_lowest_adj(d) = bb_lowest(d) - (-1.134) * dose_plasma_mg(d) = bb_lowest(d) + 1.134 * dose_plasma_mg(d)`. At 30mg steady-state the adjustment subtracts ~+34 BB units from bb_lowest, which is larger than the channel's full IQR -- a structural sanity flag for the section 5.B treatment on this specific channel: the dose-adjusted predictor sits in a very different numerical range than the raw channel; the rolling baseline operates on the corrected signal.

### 2. `bb_overnight_gain` (HA10 primary; or bb_overnight_gain_best with coverage extension)

On Stratum 4 observed (this analysis Q3.3.k): Pearson r=+0.197 / Spearman rho=+0.214 (n=593). HA10's primary BB-recharge channel.

The covariate disambiguates: is the bb_lowest signal driven by the depleted-state floor (beta_channel survives -- bb_lowest carries information beyond the recharge magnitude) or by the recharge magnitude itself (beta_channel attenuates -- bb_overnight_gain was doing the work). NOTE: coverage discipline per bb_overnight_gain_proxy.md applies if pre-2024-09-18 days enter the analysis.

### 3. `all_day_stress_avg` -- sister CONFIRMED-citalopram channel (strongest inverse neighbour)

On Stratum 4 observed (this analysis Q3.3.e): Pearson r=-0.727 / Spearman rho=-0.749 (n=1359). Sister CONFIRMED-citalopram channel; INVERSE-direction neighbour.

Both channels are CONFIRMED dose-modulated in opposite directions. The covariate disambiguates: BB-floor mechanism vs autonomic-state shared variance.

### 4. `bb_lowest_lagged_lcera_z` -- already-materialised lagged-baseline covariate

Per Q3.3.b the cutoff lag M=18 and E[L]\*=29.2. The `bb_lowest_lagged_lcera_z` column is ALREADY materialised in `per_day_master.csv` per CONVENTIONS section 3.2 _lagged_lcera convention (LC-era-only [d-90, d-30] trailing baseline). A consumer HA can use it directly OR compute a shorter-window covariate at N=29d or N=28d for the autocorrelation-vs-mechanism disambiguation.

### Recommendation for any HA pre-reg on this channel

Pre-spec all four covariates as **secondary sensitivity arms**. Concordance across the four secondaries = high confidence in the primary; divergence = the disambiguation is doing real work. The section 5.B citalopram-dose adjustment is **obligatory** per the framework AND per this channel being the LARGEST-absolute-beta CONFIRMED member; the BB-pair (covariate 2) is the BB-construct disambiguator; the cross-channel (covariate 3) is the BB-floor-vs-autonomic-state disambiguator; the autocorrelation-vs-mechanism arm (covariate 4) operationalises HA-P7 section 4.5.4 on this specific channel. HA-C4b BB-floor pre-reg (deferred per STOCKTAKE section 6) is the natural consumer.

---

## Q3.3.j (channel-specific) -- BB-source coverage

**`bb_lowest` has full corpus coverage from 2021-08-17 onward** (1732 / 1755 = 98.69% of corpus rows). Last non-nan: 2026-05-29.

### Per-phase coverage on Stratum 4

| phase | n days in window | n with channel | coverage % |
|---|---:|---:|---:|
| unmedicated | 584 | 581 | 99.49% |
| buildup | 72 | 72 | 100.00% |
| consolidation | 638 | 635 | 99.53% |
| afbouw | 78 | 71 | 91.03% |

### Contrast with bb_overnight_gain (HA10 primary; load-bearing coverage-bridge per handoff section 2.4)

bb_overnight_gain: first non-nan 2024-09-18; 593 / 1755 = 33.79% of corpus rows.

Per [bb_overnight_gain_proxy.md section 1 + section 5.4](../../../methodology/bb_overnight_gain_proxy.md): bb_overnight_gain is **structurally absent for ~64% of LC corpus pre-2024-09-18** because Garmin's UDS export rolled the underlying stats out in two stages on this user's FR245 -- SLEEPSTART first emitted 2024-07-08; SLEEPEND first emitted 2024-09-18. This is a Garmin-side schema rollout, NOT a project-side pipeline gap. The `bb_overnight_gain_best` fused channel rescues 74 days of pre-2024-09-18 coverage via the bb_overnight_gain_proxy = HIGHEST - SLEEPSTART (validated at r=0.989 vs truth post-2024-09-18; section 4 discipline rules govern consumer use).

### Verdict (operational consequence)

bb_lowest has full corpus coverage from 2021-08-16 onward (no Garmin schema rollout gap); contrast with bb_overnight_gain which is structurally absent for ~64% of LC corpus pre-2024-09-18 (SLEEPSTART rollout 2024-07-08; SLEEPEND rollout 2024-09-18) per bb_overnight_gain_proxy.md section 1. Any HA test on bb_lowest can use the full Stratum 4 window without coverage-bridge sensitivity; any HA on bb_overnight_gain MUST use bb_overnight_gain_best with proxy-share disclosure per bb_overnight_gain_proxy.md section 4 discipline rule 1 OR restrict to post-2024-09-18.

---

## Q3.3.k (channel-specific) -- Relationship to bb_overnight_gain (HA10 primary)

**Discipline anchor**: bb_overnight_gain_proxy.md (r=0.989 vs truth post-2024-09-18; sensitivity-only for 2024-07-08 -> 2024-09-17 bridge).

Pair statistics on Stratum 4:

| target channel | n | Pearson r | Spearman rho | near-identity flag? | window |
|---|---:|---:|---:|---|---|
| `bb_overnight_gain` | 593 | +0.197 | +0.214 | no | 2024-09-18 -> 2026-05-29 |
| `bb_overnight_gain_best` | 667 | +0.183 | +0.190 | no | 2024-07-08 -> 2026-05-29 |
| `bb_overnight_gain_proxy` | 667 | +0.174 | +0.179 | no | 2024-07-08 -> 2026-05-29 |

### Source-conditioned check for bb_overnight_gain_best (per bb_overnight_gain_proxy.md discipline rule 1)

On the 667 bb_lowest <-> bb_overnight_gain_best pair days: **593 truth-source days** (post-2024-09-18 SLEEPEND-emitted nights) + **74 proxy-source days** (the 2024-07-08 -> 2024-09-17 bridge + 3 post-rollout SLEEPEND-failure nights per bb_overnight_gain_proxy.md section 5.4).

Truth-only subset: Pearson r=+0.197 / Spearman rho=+0.214.
Proxy-only subset: Pearson r=+0.177 / Spearman rho=+0.155.

### Substantive gap description

bb_lowest measures the daily NADIR (lowest BB observed across the 24h window). bb_overnight_gain measures the RECHARGE ARC during sleep (SLEEPEND - SLEEPSTART). These are operationally distinct constructs even on a perfect-coverage day: the floor depth and the recharge magnitude can move independently (a deep-floor night with strong recharge vs a shallow-floor night with weak recharge). The empirically-observed correlation magnitude reported above characterises the shared variance on the overlap window; the near-identity flag at |rho|>=0.92 governs whether the pair counts as column-duplication per CONVENTIONS section 3.3.

### Operational consequence

HA10 primary uses BB peak (bb_highest) as the morning-recovery marker; bb_lowest is the complementary depleted-state marker. A future HA-C4b BB-floor pre-reg (deferred per STOCKTAKE section 6) would use bb_lowest as primary; HA10 + HA-C4b together would cover both ends of the BB construct. bb_overnight_gain is the arc between them and the third leg of the BB-recovery construct triangle.

---

## Cross-references

### HA-* tests that touch this channel (cite this analysis)

- **HA10** (BB overnight recharge, LOCKED `analyses/hypotheses/HA10-bb-overnight-recharge/result.md`): primary channel is `bb_highest` (not bb_lowest); bb_lowest is the complementary floor primitive. R14 single_pool_reanchor (`badd04a`) flattened the era-directionality reversal -20.5 / +16.2 to +4.1 pp CONVERGE-ON-OVERALL on the recharge channel. **The descriptive substrate this analysis produces -- per-phase trajectory (Q3.3.c, Q3.3.d) + crash-vs-normal (Q3.3.f) on the floor channel -- complements HA10's peak-channel result with floor-side context.** The substantive HA10 verdict + the R14 single-pool verdict are LOCKED; this analysis's descriptive corroboration is NOT a re-interpretation.
- **HA-P6 v3** (descriptive Layer 1; LOCKED `a980b1c` 2026-06-17): bb_lowest is one of the 4/7 distinguishable channels in the matched-control framework. The descriptive substrate this analysis produces (E[L]\*=29.2, autocorrelation context; episode-level d=-0.30; per-phase trajectory; afbouw reversal) provides context for the HA-P6 result reading on this specific channel.
- **HA-C4b** (BB-floor candidate; DEFERRED per STOCKTAKE section 6): the natural consumer of this descriptive analysis. The deferred status awaits per-minute primitive availability, which Q3.3.g + bb_overnight_gain_proxy.md section 6 caveat 5 confirm is **not in the GDPR dump** -- any HA-C4b pre-reg using bb_lowest as primary at daily resolution would inherit this analysis's operationalisation substrate (Q3.3.i covariate-readiness arm; Q3.3.d phase-stratified anchor; Q3.3.f crash-vs-normal floor).

### Methodology MDs cited

- [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) -- Q3.3.a delegate target (partial; extended for the full skewness/kurtosis/heavy-tail-flag set on this channel).
- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) sections 3-6 -- Q3.3.c phase axis, Q3.3.d phase-stratified treatment, Q3.3.i covariate framework.
- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) v3 section 5.6.1 -- locked -1.134/mg dose-response slope (largest absolute beta among 3 CONFIRMED channels; INVERSE direction).
- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) -- E[L]=7 default + factor-of-2 deviation rule; Q3.3.b reports E[L]\*=29.2 (factor-of-2 flag fires).
- [`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md) -- load-bearing coverage-bridge MD for Q3.3.h + Q3.3.j + Q3.3.k (r=0.989 vs truth post-2024-09-18; sensitivity-only for 2024-07-08 -> 2024-09-17 bridge).
- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) -- Q3.3.h cross-reference; BB-family per-column rows absorbed into UDS-passthrough collective rows.
- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) -- Stratum 4 boundary definition.

### Existing artefacts referenced

- [`descriptive/operationalisation_support/stress_mean_sleep/findings.md`](../stress_mean_sleep/findings.md) -- sister CONFIRMED-citalopram channel; first Phase-1 Strand A analysis; cross-channel comparison anchors throughout (E[L]\* 29.2 here vs 12.6 there).
- [`descriptive/operationalisation_support/all_day_stress_avg/findings.md`](../all_day_stress_avg/findings.md) -- sister CONFIRMED-citalopram channel; Phase-2 Q3.2 precedent; OPPOSITE-direction afbouw contrast surfaced in Q3.3.d.
- [`descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/findings.md`](../stress_low_motion_min_count_S60_Mlow/findings.md) -- spike-form companion for the stress family; third Phase-1 Strand A analysis; cross-pair r=+0.85 / rho=+0.86 with sister all_day_stress_avg.
- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) -- R14 cross-check (LANDED `badd04a`); the HA10 row descriptively corroborated in Q3.3.d.
- [`descriptive/trajectory/recovery_arc/findings.md`](../../trajectory/recovery_arc/findings.md) -- v2 LANDED 2026-06-22 (`8feae6a`); section 5.A afbouw-reversal finding load-bearing in Q3.3.d.
- [`analyses/hypotheses/HA10-bb-overnight-recharge/result.md`](../../hypotheses/HA10-bb-overnight-recharge/result.md) -- LOCKED OVERALL-REFUTED with era-directionality reversal; bb_lowest is the floor-side companion to HA10's peak-side primary.
- [`analyses/hypotheses/HA-P6/result.md`](../../hypotheses/HA-P6/result.md) -- v3 LOCKED `a980b1c` 2026-06-17; bb_lowest is one of 4/7 distinguishable channels.
- [`analyses/garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) -- Q3.3.e cross-reference for the 7-channel panel; this analysis surfaces the bb_lowest <-> all_day_stress_avg rho=-0.749 reciprocal pair already documented from the stress-side at Q3.2.e.

### Upstream pipeline

- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `daily_uds.csv` (Wave-3 JSON-side passthrough 2026-06-12 per `garmin_indicators_audit.md`). NO custom FIT extraction for this channel.
- `labels_crash_v2.csv` <- `garmin/hypotheses/crash_v2-definition/definition.md` (locked).

---

## Limitations

For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding limitations a downstream HA pre-reg author should carry forward are:

1. **Q3.3.c-d are on raw channel values, not dose-adjusted.** Per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5, any HA using `bb_lowest` cross-phase MUST adopt section 5.A / 5.B / 5.C treatment. Q3.3.d explains the citalopram-axis dynamics descriptively; a section 5.B dose-adjusted phase comparison is the natural follow-up but lives in the HA pre-reg, not here.
2. **The channel IS the daily NADIR (a spike-form extremum) per CONVENTIONS section 3.5** (Q3.3.g); the discipline distinction is reversed from the stress channels' continuous-form/spike-form pairing. A future HA whose mechanism is *overnight recharge magnitude* should use bb_overnight_gain (HA10's primary; coverage-discipline per bb_overnight_gain_proxy.md), NOT bb_lowest. A future HA whose mechanism is *peak BB during the day* should use bb_highest.
3. **The episode-level Cohen's d=-0.30 CI is [-5.45, +0.36]** (Q3.3.f). The episode-level is the unit-of-analysis-clean read per CONVENTIONS section 3.6; consumer HAs using this channel as a crash-discriminator should NOT rely on the day-level (autocorrelation-inflated) as the primary read.
4. **Block-length sensitivity matters** (Q3.3.b E[L]\*=29.2 vs default 7). Consumer tests using this channel with autocorrelation-controlled methods should pre-spec the E[L]\*~29 sensitivity arm alongside the default-E[L]=7 primary.
5. **The afbouw-reversal finding is descriptively striking but Layer-1 only**: per Q3.3.d the afbouw median 15.0 sits BELOW the unmedicated baseline 18.0; cross-referenced load-bearing in [recovery_arc v2 section 5.A](../../trajectory/recovery_arc/findings.md) + [STOCKTAKE section 6 line 187](../../../STOCKTAKE.md). The substantive afbouw-reversal interpretation lives in recovery_arc v2; this analysis's Q3.3.d corroborates it descriptively but does NOT extend or promote the substantive reading.
6. **Q3.3.j confirms full corpus coverage for bb_lowest itself** (no Garmin schema rollout gap), but Q3.3.k applies the bb_overnight_gain_proxy.md coverage-bridge discipline to the bb_overnight_gain pairing; any consumer HA combining bb_lowest with bb_overnight_gain must report proxy-share per bb_overnight_gain_proxy.md section 4 discipline rule 1.
7. **Per-minute BB primitive is NOT in the GDPR dump** per bb_overnight_gain_proxy.md section 6 caveat 5 (Q3.3.g + Q3.3.g latent-in-FIT note). Within-day BB-floor density at finer-than-daily resolution is structurally unavailable; HA-C4b BB-floor at daily resolution is the maximum resolution achievable on this corpus.
8. **HA10 + HA-P6 v3 verdicts are LOCKED with R14 single-pool re-anchor descriptively corroborating.** This analysis's Q3.3.c + Q3.3.d + Q3.3.f cross-references are descriptive corroboration only; the locked verdicts are NOT extended by this analysis per CONVENTIONS section 4.2 (caveats yes; a-priori claims no).

---

## Status

**Current as of 2026-06-24** (commit context: post-`cf34ab1` Q3.2 all_day_stress_avg LANDED; Phase 2 "finish the descriptive analysis" Tier 1 user-prioritised CONFIRMED-citalopram channel #3 of 3; R14 `single_pool_reanchor` first at `badd04a`; `all_day_stress_avg` second at `cf34ab1`; this `bb_lowest` third; `stress_stdev_sleep` closes Tier 1 next). Refresh when:

1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to spin up (per CONVENTIONS section 3.1 personal-baseline freshness).
2. A new citalopram-phase boundary lands (e.g. post-afbouw enters analytic scope as of 2026-06-06 onward).
3. The Politis-White E[L]\* shifts by another factor of 2 from current 29.2.
4. HA-C4b BB-floor pre-reg unblocks (per STOCKTAKE section 6 deferred status) and triggers operationalisation-substrate consumption from this analysis.
5. Per-minute BB primitive becomes available (currently not in GDPR dump; would re-open Q3.3.g sub-daily spike-density question).
6. recovery_arc v3 refresh ships and updates the section 5.A afbouw-reversal characterisation; this analysis's Q3.3.d would refresh in lockstep.
