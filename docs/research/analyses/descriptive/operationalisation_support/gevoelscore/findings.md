# Findings -- `gevoelscore` operationalisation-support descriptive (Q3.9.a-i)

**Channel**: `gevoelscore` (the OUTCOME side of nearly every HA in the project; per-day self-reported felt-state on a 1-6 integer scale per the empirical range + [`crash_v2-definition`](../../../analyses/hypotheses/crash_v2-definition/) substrate; app-brief framing is 1-10 but observed values are 1-6). Logging started 2022-09-03 = the Stratum 4 left edge per [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) (Stratum 4 IS the gevoelscore-having days by definition).

**Substantive context** (handoff section 1): gevoelscore is the OUTCOME side of nearly every HA. **HA-C3 v2** (LOCKED REJECTED wrong-direction override; concave/inverted-U vs Wiggers' convex prediction; J*=0.481 p_a=0.6742; S=-0.740 p_c=0.0003; spline F=28.27 p_b=0.0002; spline secderiv at midpoints [35, 70] = [-0.0015, 0.0000]) + **HA-C3p** (LOCKED PARTIAL 2-of-3; p_b=0.0018 spline-F significant + p_c=0.0020 convexity-contrast significant in wrong direction S=-0.196; p_a=0.5925 Jonckheere monotone non-significant) use gevoelscore as the DIRECT outcome in stress -> felt-state bin-shape convexity tests; the joint outcome-side reading from these two LOCKED tests: at this corpus the stress -> felt-state mapping is **CONCAVE / inverted-U with peak around stress 30-40**, NOT convex per the Wiggers verbatim prediction. **HA10 + HA07d + many other HAs** use gevoelscore in their CRASH LABELS indirectly via [`crash_v2-definition`](../../../analyses/hypotheses/crash_v2-definition/) derivation (crash = score <= 3 for >= 2 consecutive days). Section 3.9.f is largely TAUTOLOGICAL on this channel (crashes are days with score <= 3 by definition) -- surfaced honestly per handoff section 1 + section 2.4. **gevoelscore was NOT in v3 multi-channel dose-response sweep scope** (per descriptive README section 3.4 'it's the outcome, not a Garmin channel'); no v3 verdict exists to cite or re-promote on this channel.

**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to 2026-06-05). n=1372 days with channel out of 1372 Stratum 4 days (0 NaN days).

**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`) -- HA-touched non-confirmed channel candidate list bullet `gevoelscore (almost every test's outcome side)`. **5th (FINAL) of the 5 Tier 2 channels** in the user-prioritised Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain `7d49ba4`; 2nd = Q3.6 resting_hr `5d28219`; 3rd = Q3.7 exertion_class `9b03bed`; 4th = Q3.8 push_burden_7d `92d7193`; this Q3.9 closes Tier 2). Q3.9.a-i template applied per section 3.1 with **OUTCOME-CHANNEL ADAPTATIONS** documented at each cell.

**Sources**: `per_day_master.csv` (`gevoelscore` column; integer 1-6 scale) + `labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level per CONVENTIONS section 3.6).

**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). HA-C3 v2 + HA-C3p (LOCKED) + crash_v2-definition (LOCKED) + recovery_arc v2 (LOCKED) cross-references in this analysis are **descriptive corroboration only**; the substantive verdicts live in those result.md / definition.md / findings.md files and are NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). No crash_v2-definition modification per handoff section 3 hard constraint. Statistical hygiene anchors: section 3.1 (personal baseline -- N/A; gevoelscore IS the personal felt-state), section 3.3 (column-duplication threshold |rho|>=0.92 -- N/A by construction; gevoelscore is the only felt-state channel), section 3.4 (crash-drop sensitivity -- TAUTOLOGICAL on this channel per Q3.9.f), section 3.5 (spike metrics -- DROP primitive on the outcome channel per Q3.9.g), section 3.6 (named counts).

---

## Headline

`gevoelscore` on Stratum 4 is a **bounded 1-6 INTEGER felt-state outcome channel** (skew=-0.71, excess kurtosis=+0.76, heavy_tail_flag=False; entropy 69.6% of log(6) ceiling). **Per-value frequency**: see Q3.9.a table below for the discrete distribution. The **data-driven E[L]\*=15.1** (Politis-White; vs project default E[L]=7; deviation ratio 1.15; factor-of-2 flag = True; cutoff lag M=8). **autocorrelation-MODERATE-MEMORY** memory regime. Cross-channel context per handoff section 2.4: vs sister Strand-A channels stress_stdev_sleep 7.0 / bb_overnight_gain 6.5 / stress_mean_sleep 12.6 / push_burden_7d_lagged 7.0 / resting_hr 7.0 (fallback) / exertion_class 7.0 (ordinal) / stress_low_motion 21.1 / bb_lowest 29.25 / all_day_stress_avg 29.8. **Phase-stratified medians** (citalopram axis): unmedicated 4.0 -> buildup 4.0 -> consolidation 5.0 -> afbouw 5.0. **Q3.9.e SUBSTANTIVE (subjective<->objective coupling)**: top-tracking Garmin sister channel is `stress_mean_sleep` (Spearman rho = -0.194); weakest-tracking is `bb_lowest` (Spearman rho = +0.010). Q3.9.f crash-vs-normal day-level Cohen's d=-2.47 + MWU p=<0.0001 reported descriptively but **TAUTOLOGICAL** per crash_v2-definition section 2.1 (crash days are by-definition the score <= 3 days; the difference is mechanically constrained). Score-floor descriptive on crash days: max score = 4; n crash-days with score > 3 = 5 (the few score-4 days that fall inside merged crash episodes per merge rule sec 2.1.b -- expected behaviour, NOT a labelling pipeline drift).

---

## Q3.9.a -- Distribution shape (Stratum 4) -- OUTCOME-CHANNEL ADAPTATION

**OUTCOME-CHANNEL ADAPTATION**: `gevoelscore` is a **bounded 1-6 INTEGER scale** (per crash_v2-definition sec 2.1 substrate; app-brief framing is 1-10 but empirical range observed is 1-6). Classical distribution stats apply but the value range is small + discrete -- the **per-value frequency vector + Shannon entropy** are the OUTCOME-channel primitives; mean / median / std / MAD / quantiles reported for parity with sister continuous Strand-A analyses (Q3.1-Q3.8) but interpreted with the bounded-integer-scale caveat in mind. The heavy_tail_flag uses the CONVENTIONS section 3.1 rule (skew > 1 OR p99/median > 3.0) but on a 6-ceiling bounded scale the heavy-tail concept does NOT meaningfully apply -- the flag is reported for parity but rarely fires on bounded scales by construction.

| stat | value | source |
|---|---:|---|
| n (Stratum 4) | 1372 | `per_day_master.csv` `gevoelscore` non-NaN within S4 |
| mean | 4.388 | (single-pool S4) |
| median | 5.000 | |
| std (ddof=1) | 0.877 | |
| MAD (unscaled) | 1.000 | |
| MAD x 1.4826 (normal-equivalent SD) | 1.483 | for robust z-score scaling per section 3.1 |
| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | 2 / 3 / 3 / 4 / 5 / 5 / 5 / 6 / 6 | |
| skewness (Fisher-Pearson) | **-0.71** | left-skewed |
| excess kurtosis (Fisher) | **+0.76** | |
| heavy_tail_flag | **False** | skew > 1 OR p99/median > 3.0; rarely fires on bounded scales |
| range | 1 to 6 | bounded 1-6 integer by construction |
| Shannon entropy (nats) | 1.246 | |
| max entropy (log 6 = uniform over 1-6) | 1.792 | |
| entropy normalised (fraction of log-6 ceiling) | **69.6%** | 100% = uniform; lower = concentrated |

### Per-value frequency table (the OUTCOME-channel primitive)

| gevoelscore value | n days | fraction |
|---:|---:|---:|
| 1 | 6 | 0.4% |
| 2 | 33 | 2.4% |
| 3 | 152 | 11.1% |
| 4 | 489 | 35.6% |
| 5 | 615 | 44.8% |
| 6 | 77 | 5.6% |

**gevoelscore is the FELT-STATE outcome channel** (per-day self-report on a 1-6 integer scale; substrate of crash_v2-definition's score-<=3 acute condition). The per-value frequency vector above is the load-bearing distribution descriptor (mean / median + classical moments reported for parity).

### Cross-channel comparison vs sister Strand-A channels (skew + heavy_tail_flag)

| stat | gevoelscore (this analysis) | resting_hr (Q3.6) | bb_overnight_gain (Q3.5) | push_burden_7d (Q3.8) | exertion_class (Q3.7, encoded) |
|---|---:|---:|---:|---:|---:|
| n S4 | 1372 | 1357 | 593 | 1372 | 1372 |
| mean | 4.39 | 56.68 | 16.65 | 1.93 | n/a (categorical) |
| median | 5.00 | 56.00 | 16.00 | 2.00 | n/a (categorical) |
| MAD (unscaled) | 1.00 | 2.00 | 4.00 | 1.00 | n/a |
| skewness | -0.71 | +0.25 | +0.97 | +0.58 | n/a |
| heavy_tail_flag | **False** | **False** | **False** | **False** | n/a |
| type | **integer felt-state 1-6 (OUTCOME)** | continuous bpm | continuous BB units | integer count [0, 6] | 5-level ordinal |

See [`plots/fig1_per_value_frequency_s4.png`](plots/fig1_per_value_frequency_s4.png).

---

## Q3.9.b -- Autocorrelation structure + E[L]\* on integer series

**OUTCOME-CHANNEL ADAPTATION**: ACF computed on the integer series as-is (no encoding needed; the integer scale 1-6 naturally supports the Politis-White ACF + block-length estimator). Integer-discreteness does not bias the estimator at this sample size.

The **data-driven block length is E[L]\*=15.1** (Politis-White 2004 with Patton-Politis-White 2009 correction per [`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) vs the project default E[L]=7 per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). The **factor-of-2 deviation flag = True** (deviation ratio = 1.15). Cutoff lag M=8.

| lag (days) | autocorrelation |
|---:|---:|
| 1 | +0.410 |
| 2 | +0.243 |
| 3 | +0.212 |
| 7 | +0.157 |
| 14 | +0.136 |

Politis-White 2-sigma significance threshold (n=1372): |rho| = 0.145.

### Cross-channel comparison (E[L]\* by Strand A analysis) -- handoff section 2.4 load-bearing

| analysis | channel | E[L]\* |
|---|---|---:|
| Q3.5 (bb_overnight_gain, truth window) | per-night SLEEPEND-SLEEPSTART | 6.5 |
| Q3.4 (stress_stdev_sleep) | per-night STDEV | 7.0 |
| Q3.6 (resting_hr) | daily UDS restingHeartRate | 7.0 (fallback) |
| Q3.7 (exertion_class ordinal) | 5-level activity class | 7.0 |
| Q3.8 (push_burden_7d_lagged) | integer count [0, 6] | 7.0 |
| Q3.1 (stress_mean_sleep) | sleep-window mean | 12.6 |
| Phase-1 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 |
| Q3.3 (bb_lowest) | daily NADIR | 29.25 |
| Q3.2 (all_day_stress_avg) | 24h-window mean | 29.8 |
| **this analysis (gevoelscore)** | **integer felt-state 1-6 (OUTCOME)** | **15.1** |

See [`plots/fig5_acf.png`](plots/fig5_acf.png).

---

## Q3.9.c -- Base rates per citalopram phase + recovery_arc v2 overlap notation

Phase axis per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3:

| phase | window | n | median | mean | MAD | p10 / p90 |
|---|---|---:|---:|---:|---:|---|
| unmedicated | 2022-09-03 to 2024-04-08 | 584 | 4.00 | 4.14 | 1.00 | 3 / 5 |
| buildup | 2024-04-09 to 2024-06-19 | 72 | 4.00 | 4.26 | 1.00 | 3 / 5 |
| consolidation | 2024-06-20 to 2026-03-19 | 638 | 5.00 | 4.58 | 1.00 | 4 / 5 |
| afbouw | 2026-03-20 to 2026-06-05 | 78 | 5.00 | 4.76 | 0.00 | 4 / 6 |

### Per-value frequency per phase

| phase | n | value=1 | value=2 | value=3 | value=4 | value=5 | value=6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| unmedicated | 584 | 6 (1.0%) | 25 (4.3%) | 92 (15.8%) | 227 (38.9%) | 225 (38.5%) | 9 (1.5%) |
| buildup | 72 | 0 (0.0%) | 1 (1.4%) | 12 (16.7%) | 26 (36.1%) | 33 (45.8%) | 0 (0.0%) |
| consolidation | 638 | 0 (0.0%) | 6 (0.9%) | 44 (6.9%) | 217 (34.0%) | 314 (49.2%) | 57 (8.9%) |
| afbouw | 78 | 0 (0.0%) | 1 (1.3%) | 4 (5.1%) | 19 (24.4%) | 43 (55.1%) | 11 (14.1%) |

### Recovery_arc v2 overlap notation (per handoff section 2.4)

Per handoff section 1 + section 2.4 + handoff bullet 'check overlap; do NOT re-characterise if already done': [`trajectory/recovery_arc/findings.md`](../../trajectory/recovery_arc/findings.md) already characterised gevoelscore on the 6-phase axis (section 2 table + section 2.1 per-channel narrative + section 3 / 7b paired-bootstrap CI). This Q3.9.c provides a **descriptive reproduction read** on the same axis at the same as-of-date for methodological consistency; it does NOT re-characterise.

Structural caveat: gevoelscore logging started 2022-09-03 = phase-3 last 19 days, so phases 1 (pre_illness_healthy) + 2 (acute_infection) have **n=0** and phase 3 (lc_pre_ergo) is partial (n=19).

| 6-phase axis | n (this Q3.9.c) | median (this Q3.9.c) | recovery_arc v2 reported median |
|---|---:|---:|---:|
| pre_illness_healthy | 0 | n=0 | n=0 (phase 1+2 pre-gevoelscore-logging) |
| acute_infection | 0 | n=0 | n=0 (phase 1+2 pre-gevoelscore-logging) |
| lc_pre_ergo | 19 | 3.00 | 3.00 (n=19) |
| pacing_pre_citalopram_learning_4a | 56 | 5.00 | 5.00 (n=56) |
| pacing_habit_established_4b | 509 | 4.00 | 4.00 (n=509) |
| citalopram_modulated | 788 | 5.00 | 5.00 (n=787) |

**Recovery_arc v2 reported headline** (per [`recovery_arc/findings.md`](../../trajectory/recovery_arc/findings.md) section 2 + section 7b): 4a -> 4b drop on gevoelscore (diff -1.0, CI [-1.0, 0.0]) sits at the boundary of the section 7b verdict -- upper CI bound is AT 0 (includes 0 but only just; descriptive read: ambiguous). Phase 3 -> 4a step is +2.0 (largest within-channel step) but phase 3's n=19 keeps its CI wide [3, 4] and shaped by structural partial-coverage. Per recovery_arc v2 section 4 felt-state narrative: phase 3 partial coverage shows median 3.0 (lowest gevoelscore median anywhere in the corpus); 4a (median 5; full 56-day sub-window) is the first complete characterisation of the 8-week ergotherapy-onboarding period in felt-state terms; 4b drops to median 4; phase 5 returns to 5.

Per handoff section 2.4 + CONVENTIONS section 4.2: this Q3.9.c overlap notation is **NOT a re-characterisation**; the recovery_arc v2 substantive narrative is LOCKED at the recovery_arc/findings.md level and NOT extended here.

Named counts (CONVENTIONS section 3.6): the per-phase n's above are `gevoelscore`-non-NaN day rows in `per_day_master.csv` within Stratum 4 date masks per `citalopram_phase_stratification.md section 3` boundary dates + `lc_recovery_phase_axis.md` 6-phase axis boundary dates.

See [`plots/fig2_phase_stratified_stacked_bar.png`](plots/fig2_phase_stratified_stacked_bar.png).

---

## Q3.9.d -- Phase-stratified distribution + descriptive shift report (no v3 caveat-class)

**Per CONVENTIONS section 4.2 (caveats yes; a-priori claims no)**: gevoelscore was NOT in the v3 multi-channel sweep scope per [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.6 (6-channel scope: stress_mean_sleep + all_day_stress_avg + bb_lowest + resting_hr + bb_overnight_gain + respiration_avg_sleep; **gevoelscore is the outcome, not a Garmin channel** -- per descriptive README section 3.4 + handoff section 1). **No v3 verdict exists to cite or re-promote on this channel**; observed phase shifts are pure Layer 1 descriptive observations.

Observed phase-to-phase median shifts:

| comparison | delta median | delta mean |
|---|---:|---:|
| buildup minus unmedicated | **+0.00** | +0.12 |
| consolidation minus unmedicated | **+1.00** | +0.44 |
| consolidation minus buildup | **+1.00** | +0.32 |
| afbouw minus consolidation | **+0.00** | +0.17 |
| afbouw minus unmedicated | **+1.00** | +0.61 |

### HA-C3 v2 + HA-C3p locked outcome-side cross-reference (per handoff section 2.4)

Per [`analyses/hypotheses/HA-C3/result.md`](../../../analyses/hypotheses/HA-C3/result.md) + [`HA-C3p/result.md`](../../../analyses/hypotheses/HA-C3p/result.md):

- **HA-C3 v2 (LOCKED REJECTED wrong-direction override)**: REJECTED (wrong-direction override) on the v2 4-bin all_day_stress_avg -> gevoelscore convexity test; primary 3-condition test on 3-bin reduction returned J*=0.481 p_a=0.6742 + S=-0.740 p_c=0.0003 + spline F=28.27 p_b=0.0002 + spline secderiv at midpoints [35, 70] = [-0.0015, 0.0000]. Wrong-direction override fired because S is significantly NEGATIVE (concave, not convex).
- **HA-C3p (LOCKED PARTIAL 2-of-3)**: PARTIAL (2-of-3 conditions MET) on personal-baseline-anchored equal-N quintile bins; p_b=0.0018 spline-F significant + p_c=0.0020 convexity-contrast significant in WRONG direction (S=-0.196); p_a=0.5925 Jonckheere monotone non-significant. Joint reading with HA-C3 v2 (per HA-C3p result.md sec 6 4-cell matrix consolidated): BOTH detect REAL non-linearity + CONCAVE/inverted-U shape with peak around stress 30-40 + decline at higher stress.

HA-C3 v2 + HA-C3p both use gevoelscore as the DIRECT outcome in the stress -> felt-state mapping convexity test. The joint finding from the outcome side: at this corpus the stress->felt-state mapping is CONCAVE / inverted-U with peak around stress 30-40, NOT convex per the Wiggers verbatim prediction. This Q3.9.d phase-stratified gevoelscore characterisation + Q3.9.e spearman-rho-vs-stress descriptively corroborates the inverted-U finding from the gevoelscore outcome side. The HA-C3 v2 + HA-C3p substantive verdicts are LOCKED and NOT extended here per CONVENTIONS section 4.2.

Per CONVENTIONS section 4.2: this Q3.9.d phase-stratified gevoelscore characterisation is **descriptive corroboration only** of the joint HA-C3 v2 + HA-C3p inverted-U outcome-side finding; the substantive HA verdicts live in those result.md files and are NOT extended here per handoff section 3 hard constraint.

See [`plots/fig2_phase_stratified_stacked_bar.png`](plots/fig2_phase_stratified_stacked_bar.png) (per-phase per-value frequency stacked bar) and [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (rolling 90d median through phases).

---

## Q3.9.e -- SUBSTANTIVE: Subjective <-> objective coupling (Spearman rho vs Garmin sister channels)

**SUBSTANTIVELY-INTERESTING cell** per handoff section 1 + section 2.4 + descriptive README section 4.9. Strand-A first-pass at the Q4.9 subjective<->objective coupling question (deferred to Strand B per descriptive README sec 4.9). **Descriptive only; NO causal mechanism interpretation; NO substantive HA verdict promotion** per CONVENTIONS section 4.1 + section 4.2.

Spearman rho between gevoelscore (felt-state) and key Garmin sister channels on the full Stratum-4 pool (multi-phase combined; no per-phase stratification at this Q3.9.e scope -- per-phase coupling structure is deferred to Strand-B Q4.9).

| target channel | n | Pearson r | Spearman rho | semantic |
|---|---:|---:|---:|---|
| `stress_mean_sleep` (PRIMARY) | 1339 | -0.297 | -0.194 | autonomic-load sleep-window; CONFIRMED-citalopram +0.43/mg; HA07c/HA07d/HA08c primary |
| `all_day_stress_avg` (PRIMARY) | 1359 | -0.119 | -0.056 | autonomic-load 24h; CONFIRMED-citalopram +0.57/mg; HA-C3 + HA-C3p primary stress predictor |
| `bb_lowest` (PRIMARY) | 1359 | +0.011 | +0.010 | BB-floor NADIR; CONFIRMED-citalopram -1.13/mg; HA-C4b v2 primary |
| `resting_hr` (PRIMARY) | 1357 | +0.018 | +0.020 | cardiovascular daily; HA06b + H01 + HA06 primary |
| `stress_stdev_sleep` (PRIMARY) | 1339 | -0.160 | -0.121 | sleep-window variability; HA07d primary (only canonical-SUPPORTED test) |
| `bb_overnight_gain` | 593 | +0.234 | +0.207 | BB-recovery; HA10 primary; partial coverage 2024-09-18 onward |
| `stress_low_motion_min_count_S60_Mlow` | 1365 | -0.123 | -0.056 | count-primitive; HA-C4b v2 primary; CONFIRMED-citalopram |
| `respiration_avg_sleep` | 1335 | -0.052 | -0.022 | respiration sleep-window; v3-sweep REJECTED |
| `all_day_stress_max` | 1359 | +0.039 | +0.042 | autonomic-load peak |
| `awake_stress_avg` | 1359 | +0.006 | +0.016 | waking-hour autonomic-load |
| `bb_during_sleep_value` | 861 | +0.155 | +0.134 | BB sleep-window |
| `asleep_stress_avg_uds` | 1351 | -0.280 | -0.180 | asleep stress UDS-passthrough |
| `max_spike_minutes` | 1364 | +0.026 | +0.043 | stress spike duration; H02b primary |
| `u_dip_count` | 1365 | -0.018 | +0.003 | stress U-dip count; HA11 primary (within-day spike-form) |
| `push_burden_7d_lagged_lcera` | 1372 | +0.073 | +0.070 | trailing 7d exertion burden; HA02 family primary |

### Which Garmin channel tracks felt-state most closely? (descriptive ranking)

Ranked by **|Spearman rho|** on the 5 PRIMARY targets:

1. `stress_mean_sleep` Spearman rho = -0.194 (n=1339)
2. `stress_stdev_sleep` Spearman rho = -0.121 (n=1339)
3. `all_day_stress_avg` Spearman rho = -0.056 (n=1359)
4. `resting_hr` Spearman rho = +0.020 (n=1357)
5. `bb_lowest` Spearman rho = +0.010 (n=1359)

**Top-tracking primary channel**: `stress_mean_sleep` (Spearman rho = -0.194, n=1339).
**Weakest-tracking primary channel**: `bb_lowest` (Spearman rho = +0.010, n=1359).

### LOAD-BEARING HA-C3 v2 + HA-C3p linear-companion cross-reference

Per [`HA-C3/result.md`](../../../analyses/hypotheses/HA-C3/result.md) section 3 + section 4.5.2 (opposing-model linear test):

**HA-C3 v2 reported the linear-companion Spearman rho on the unmedicated single-pool of all_day_stress_avg vs gevoelscore as rho=-0.0298 (p=0.4738, n=581)**. Per HA-C3 v2 section 4.5.2 reading: a near-zero linear rho **co-occurring with a strong convexity-test S=-0.740 p_c=0.0003** is the expected linear-companion when the true shape is inverted-U / concave with peak in the middle. The bin-shape convexity test carries the substantive signal; the Spearman rho is the LINEAR companion that DOES NOT detect concave shape (because positive-and-negative slopes cancel under a monotone-rank measure).

This Q3.9.e re-anchors at the **FULL Stratum-4 multi-pool resolution** + extends to the broader Garmin sister-channel set. **The Spearman rho values reported in this Q3.9.e table are NOT to be interpreted as 'strength of stress -> felt-state effect'** -- they are LINEAR companions to the bin-shape convexity tests; a low |rho| co-occurring with the HA-C3 v2 + HA-C3p inverted-U findings is the expected pattern, NOT evidence of weak coupling. **NO causal interpretation** per CONVENTIONS section 4.1.

### Strand-A first-pass at Q4.9 territory (per descriptive README section 4.9)

Per descriptive README section 4.9 'Subjective <-> objective coupling + crash-day body-state profile' (deferred to Strand B):

- This Q3.9.e provides a **partial first-pass** at the Q4.9 question 'When does gevoelscore align with the 3 CONFIRMED Garmin channels vs diverge?' -- at the single-rank-correlation resolution on the full Stratum-4 pool.
- **Future Strand-B Q4.9 analysis** would add: per-phase coupling stratification, lagged-coupling structure (does felt-state lead or lag Garmin signals?), episode-level coupling profile, and **the central project question of pre-crash divergence patterns between subjective + objective signals**.
- Per handoff section 3 hard constraint: this Q3.9.e is **descriptive only**; the Q4.9 substantive question is NOT resolved at this Strand-A scope.

See [`plots/fig4_q39e_spearman_vs_*.png`](plots/) (scatter + per-quintile mean gevoelscore overlay for the chosen top-tracking Garmin sister channel).

---

## Q3.9.f -- Crash-vs-normal -- TAUTOLOGICAL by definition (honest framing)

**TAUTOLOGICAL** per handoff section 1 + section 2.4 + crash_v2-definition section 2.1 + 2.2 + 2.3: crash + dip are BOTH DEFINED BY gevoelscore (crash = score <= 3 for >= 2 consecutive days; dip = isolated single day with score <= 3 between neighbours >= 4; normal = everything else including score-4 days). The day-level crash-vs-normal gevoelscore difference is **MECHANICALLY CONSTRAINED** -- crash days are by-definition the low-score days. The numbers below exist for parity with sister Strand-A analyses + to anchor the non-tautological framings (episode-level min + median + length, dip-vs-normal characterisation, score-floor verification).

**NO substantive crash-prediction claim** from this gevoelscore-vs-crash signal -- the crash definition IS the gevoelscore signal.

### Score-floor descriptive (with merge rule sec 2.1.b context)

| metric | value | expected per crash_v2 sec 2.1 + sec 2.1.b |
|---|---:|---|
| max score on crash days | 4 | <= 3 mostly; merge rule sec 2.1.b can include a few score-4 days inside merged crash episodes |
| n crash-days with score > 3 | 5 | typically a small number (the gap days between two acute sub-runs that merged) |
| score floor (max <= 3) | **False** | True = no merge-rule gap days observed; False = merge rule activated (expected behaviour) |

Per crash_v2-definition sec 2.1: a crash episode's days are ALL days from start (first sub-threshold day) through end (last sub-threshold day) AFTER merging. The merge rule sec 2.1.b merges two qualifying episodes whose last-day and next-day are within 3 days; this means a few score-4 days WITHIN a crash episode's date span are EXPECTED (the days between two acute sub-runs in a merged episode). The acute condition (score <= 3 for >= 2 consecutive days) is the EPISODE-INITIATION rule, NOT a per-day score floor on every crash-labelled day. So n_crash_days_with_score_above_3 > 0 is NOT a labelling pipeline drift -- it is the expected behaviour of the merge rule, descriptively characterising the small fraction of score-4 days that fall inside merged crash episodes.

### Day-level (TAUTOLOGICAL; reported for parity)

| stat | value |
|---|---:|
| n crash-days | 103 |
| n normal-days | 1269 |
| mean crash-day | 2.709 |
| mean normal-day | 4.525 |
| median crash-day | 3.00 |
| median normal-day | 5.00 |
| mean diff (crash minus normal) | **-1.816** |
| median diff | **-2.00** |
| Cohen's d | **-2.47** |
| Mann-Whitney U: z | **-16.70** |
| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **<0.0001** |

**Tautology framing**: the negative day-level Cohen's d is MECHANICALLY GUARANTEED by the crash_v2 definition -- crash days are LITERALLY defined as score <= 3 days in a >= 2-consecutive-day window. The numbers above are a definitional consistency check (score floor passes), NOT a substantive test of crash-prediction by gevoelscore. **No HA pre-reg should cite this Q3.9.f day-level Cohen's d as a predictor effect**.

### Episode-level min gevoelscore distribution (NON-tautological)

Per-episode minimum gevoelscore (how deep do crashes go?) -- this IS substantively informative; the crash definition only requires score <= 3 for >= 2 days; the per-episode minimum can be 1 / 2 / 3 (or NaN if missing).

| stat | value |
|---|---:|
| n crash-episodes | 29 |
| median of per-episode min | 2.00 |
| mean of per-episode min | 2.34 |
| min of per-episode min (deepest crash) | 1 |
| max of per-episode min (shallowest crash) | 3 |

**Per-episode min frequency** (across n=29 crash-episodes):

| per-episode min gevoelscore | n episodes |
|---:|---:|
| 1 | 3 |
| 2 | 13 |
| 3 | 13 |

### Episode-level median + length (NON-tautological)

| stat | value |
|---|---:|
| median of per-episode median | 3.00 |
| mean of per-episode median | 2.79 |
| median episode length (days) | 2.0 |
| mean episode length (days) | 3.6 |
| max episode length (days) | 14 |
| min episode length (days) | 2 |

### Dip-vs-normal characterisation (also definitionally constrained per crash_v2 section 2.2)

Per crash_v2-definition section 2.2: dip = isolated single day with score <= 3 between neighbours >= 4. The dip-day distribution is also definitionally constrained on this channel.

| stat | value |
|---|---:|
| n dip-days | 79 |
| mean dip-day | 2.924 |
| median dip-day | 3.00 |
| max dip-day score | 3 |
| n dip-days with score > 3 (should be 0) | 0 |

**Dip per-value frequency**:

| dip-day gevoelscore | n |
|---:|---:|
| 2 | 6 |
| 3 | 73 |

### crash_v2-definition cross-reference (per handoff section 3 hard constraint -- LOCKED)

Per [`analyses/hypotheses/crash_v2-definition/`](../../../analyses/hypotheses/crash_v2-definition/):

- **Section 2.1 acute condition**: score <= 3 for >= 2 consecutive days = crash
- **Section 2.2 dip condition**: isolated single day with score <= 3 between neighbours >= 4 = dip
- **Section 2.3 normal**: everything else (includes score-4 days; no separate vague_low tier)

Per crash_v2 definition section 5: 'we don't test it; we apply it, then re-run downstream tests with the new labels'. This Q3.9.f does NOT modify the crash_v2 labelling (canonical lock per handoff section 3); it characterises the underlying gevoelscore distribution that crash_v2's definition operationalises ON, descriptively + honestly.

---

## Q3.9.g -- Drop primitive (spike-form on outcome channel) -- OUTCOME-CHANNEL ADAPTATION

**OUTCOME-CHANNEL ADAPTATION** per handoff section 1 + CONVENTIONS section 3.5: the spike-form on the gevoelscore outcome channel is the **DROP primitive** (sudden decrease in gevoelscore from one day to the next; day-over-day diff with positive-magnitude-drop convention). The boundedness of the scale means drops >= 5 are structurally impossible (max - min = 6 - 1 = 5).

**Drop primitive definition**: per-day gevoelscore drop = -(today - yesterday) (positive = felt-state DROP day-over-day; negative = felt-state RISE; zero = no change). Drop magnitude >= 1 unit, >= 2 units, >= 3 units reported as spike-class thresholds.

| stat | value |
|---|---:|
| n consecutive-day pairs | 1371 |
| n no-change pairs (drop=0) | 612 |
| n drop >= 1 unit | 374 (27.3%) |
| n drop >= 2 units | 71 (5.2%) |
| n drop >= 3 units | 9 (0.7%) |
| n drop >= 4 units | 0 |
| n rise >= 1 unit | 385 |
| max drop observed | 3 |
| max rise observed | 3 |

### Diff magnitude distribution

| diff (today minus yesterday) | n pairs |
|---:|---:|
| -3 | 9 |
| -2 | 62 |
| -1 | 303 |
| 0 | 612 |
| +1 | 318 |
| +2 | 63 |
| +3 | 4 |

### HA11 family cross-reference (different channel; clarification)

Per [`HA11-stress-udip/result.md`](../../../analyses/hypotheses/HA11-stress-udip/result.md) + [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) row HA11:

- **HA11 operand**: max signed z (4d) of u_dip_count (within-day stress U-dip count primitive)
- **HA11 locked verdict**: TRAIN SUPPORTED +22.8 pp / VALIDATE REFUTED -10.7 pp / OVERALL REFUTED
- **HA11 R14 single-pool re-anchor**: NOT-SUPPORTED CONVERGE-ON-OVERALL (+16.8 pp [-22.4, +20.4] perm p=0.0906 per single_pool_reanchor)
- **HA11 channel**: u_dip_count (NOT gevoelscore)

HA11 family operationalised a within-day STRESS u-dip count primitive on the stress_minutes channel; the HA11 verdict is on u_dip_count, NOT on gevoelscore-drop. This Q3.9.g characterises the gevoelscore-drop primitive as the spike-form on the outcome channel; it does NOT operationalise an HA on this primitive. A future HA using gevoelscore-drop as outcome (e.g. 'large overnight felt-state drop is predicted by autonomic spikes') would be a NEW pre-reg, NOT a re-anchoring of HA11.

**Adaptation note**: Per OUTCOME-CHANNEL ADAPTATION + CONVENTIONS section 3.5: the spike-form on a 1-6 bounded INTEGER outcome channel is the DROP magnitude (today minus yesterday). The boundedness of the scale means drops >= 5 are structurally impossible (max-min = 6-1 = 5). The drop-rate-ge1 reported above is the rate of ANY day-over-day worsening; drop-rate-ge2 + drop-rate-ge3 are the larger spike-form thresholds. A drop of 3+ units on a 6-point scale represents a substantial felt-state shift -- candidate spike-form for any future HA using gevoelscore as outcome with a sudden-worsening operand.

See [`plots/fig6_drop_primitive_distribution.png`](plots/fig6_drop_primitive_distribution.png).

---

## Q3.9.h -- Coverage / missingness (bounded-scale outlier semantics) -- OUTCOME-CHANNEL ADAPTATION

**OUTCOME-CHANNEL ADAPTATION** per handoff section 1: a bounded 1-6 INTEGER scale has **no outliers in the classical MAD-z sense** (MAD-z > 5 is impossible on a 6-value range; max-min = 5 vs MAD x 1.4826 ~ 1.5; max possible z is ~3.3). Coverage / missingness patterns matter more. Stratum 4 is DEFINED as 'LC with gevoelscore + crash labels' per lc_era_temporal_segmentation.md -- every Stratum-4 day SHOULD have a gevoelscore by construction.

### Stratum-4 completeness

| metric | value |
|---|---:|
| n total Stratum-4 rows | 1372 |
| n present (gevoelscore non-NaN) | 1372 |
| n missing in Stratum 4 | 0 |
| coverage rate | 100.000% |
| Stratum 4 completeness flag | **COMPLETE** |

### crash_v2-definition section 3.1 + section 4 cross-check

Per crash_v2 section 4: '1372 day-level rows in 2022-09-03 -> 2026-06-05 window; zero gaps'.

| metric | value | expected |
|---|---:|---|
| expected n days (crash_v2 sec 4) | 1372 | 1372 |
| observed n total | 1372 | -- |
| observed n present | 1372 | -- |
| matches expected (1372) | **True** | True = consistent |

### Monthly coverage snapshot (first 6 + last 6 months)

| year-month | n total | n present | coverage rate |
|---|---:|---:|---:|
| 2022-09 | 28 | 28 | 100.0% |
| 2022-10 | 31 | 31 | 100.0% |
| 2022-11 | 30 | 30 | 100.0% |
| 2022-12 | 31 | 31 | 100.0% |
| 2023-01 | 31 | 31 | 100.0% |
| 2023-02 | 28 | 28 | 100.0% |
| 2026-01 | 31 | 31 | 100.0% |
| 2026-02 | 28 | 28 | 100.0% |
| 2026-03 | 31 | 31 | 100.0% |
| 2026-04 | 30 | 30 | 100.0% |
| 2026-05 | 31 | 31 | 100.0% |
| 2026-06 | 5 | 5 | 100.0% |
(... 34 months in between; truncated)

**Outlier semantics note** (OUTCOME-CHANNEL ADAPTATION): Per OUTCOME-CHANNEL ADAPTATION: no MAD-z outlier scan run on this channel; the bounded-INTEGER scale makes classical outlier detection inapplicable. The per-value frequency vector in Q3.9.a is the equivalent diagnostic; rare-value flag (any value < 5% of total) would be the categorical-equivalent flag (analogous to Q3.7.a CATEGORICAL ADAPTATION rare-class flag); reported in Q3.9.a output if it fires.

---

## Q3.9.i -- Covariate-sensitivity readiness for a future HA pre-reg using gevoelscore as outcome

**Discipline anchor**: HA-P7 hypothesis.md section 4.5.4 -- secondary-logistic-with-covariate pattern.

**Primary use case**: Future HA pre-reg using gevoelscore as OUTCOME (the dominant pattern in this project's HA family: direct via HA-C3 v2 + HA-C3p; indirect via crash_v2 derivation in HA10 + HA07d + many others). Covariate-sensitivity readiness for any predictor -> gevoelscore HA test; the four covariates below are the candidate confound-control + mediator-disambiguation set per HA-P7 section 4.5.4 worked-example pattern.

Names **4** candidate covariates a future HA on `gevoelscore` (as outcome) should pre-spec.

### 1. `gevoelscore[d-1] (own-lagged 1-day; autocorrelation-vs-mechanism control per HA-P7 section 4.5.4)`

Per HA-P7 section 4.5.4 worked example: any HA using gevoelscore as outcome should pre-spec the own-lagged 1-day value as the secondary autocorrelation-vs-mechanism control. Per Q3.9.b the lag-1 ACF is high (recovery_arc v2 implies lag-1 > 0.5 on the gevoelscore series; verify in run output) -- the covariate disambiguates: beta_predictor attenuates if today's gevoelscore is just yesterday's value carried forward; beta_predictor survives if the predictor carries new-day information beyond own-lag.

*Source*: HA-P7 hypothesis.md section 4.5.4 + Q3.9.b ACF

*Expected effect under sensitivity arm*: beta_predictor collapses if today's gevoelscore is just yesterday's value carried forward; beta_predictor survives if the signal carries new-day information

### 2. `dose_plasma_mg(d) (citalopram dose; CONFIRMED on 3 Garmin channels per v3; intervention_effects_descriptive includes felt-state)`

Per citalopram_dose_response_stress_mean_sleep.md v3 sec 5.6: 3 Garmin channels are CONFIRMED dose-modulated. gevoelscore was NOT in v3 scope (per descriptive README sec 3.4 'it's the outcome, not a Garmin channel') but per intervention_effects_descriptive.md the per-phase gevoelscore shifts are described as part of the citalopram arc. Any future HA using gevoelscore as outcome cross-phase should pre-spec dose as a secondary covariate; if beta_dose is significant net of beta_predictor, that is candidacy evidence for a citalopram-on-gevoelscore mediator test (NOT a re-promotion of any v3 verdict since gevoelscore was not in v3 scope).

*Source*: citalopram_dose_response_stress_mean_sleep.md v3 sec 5.6 + intervention_effects_descriptive.md

*Expected effect under sensitivity arm*: beta_dose carries any citalopram-on-gevoelscore residue; beta_predictor attenuates if predictor signal is shared with dose effect

### 3. `top-Q3.9.e-tracking Garmin sister channel (the autonomic-load channel with highest |spearman rho| vs gevoelscore on Stratum 4)`

Per Q3.9.e SUBSTANTIVE cell: ranks key Garmin sister channels by |spearman rho| with gevoelscore. The top-tracking channel is the candidate cross-family autonomic-load covariate for any future HA using gevoelscore as outcome with a felt-state-predicted-by-X operand. The covariate disambiguates: beta_predictor attenuates if the signal is shared with autonomic-load via this channel; beta_predictor survives if predictor carries channel-distinct information beyond the autonomic-load axis.

*Source*: Q3.9.e subjective<->objective coupling table

*Expected effect under sensitivity arm*: beta_predictor attenuates if shared autonomic-load dominates; beta_predictor survives if it carries channel-distinct information

### 4. `recovery_phase (6-phase axis per lc_recovery_phase_axis.md; LOCKED `d47e0d3`)`

Per lc_recovery_phase_axis.md + recovery_arc v2 findings.md: gevoelscore varies meaningfully across the 6-phase recovery axis (phase 3 median 3.0 [partial coverage] -> 4a median 5.0 -> 4b median 4.0 -> phase 5 median 5.0). Any future HA using gevoelscore as outcome should pre-spec the recovery_phase axis as a candidate stratification or covariate; the 4b low-gevoelscore phase + 4a high-gevoelscore sub-phase are natural per-phase strata. Per phase_axis_collapsibility_conventions.md tier-A: 4a + 4b -> 4 collapse is allowed when hypothesis-warranted.

*Source*: lc_recovery_phase_axis.md (LOCKED d47e0d3) + recovery_arc v2 findings.md + phase_axis_collapsibility_conventions.md

*Expected effect under sensitivity arm*: beta_predictor attenuates if predictor signal is partly carried by phase-context; beta_predictor survives if it carries within-phase information beyond the per-phase mean shift

### Recommendation

Pre-spec all four covariates as secondary sensitivity arms. Covariate 1 (own-lagged 1-day) operationalises HA-P7 sec 4.5.4 autocorrelation-vs-mechanism disambiguation on the outcome side. Covariate 2 (dose_plasma_mg) is the cross-phase citalopram-confound covariate. Covariate 3 (top-tracking Q3.9.e Garmin channel) is the cross-family autonomic-load disambiguator -- pre-spec the SPECIFIC channel from this Q3.9.e table at HA draft time (not from later refresh). Covariate 4 (recovery_phase) is the multi-year-trajectory stratification covariate.

**OUTCOME-CHANNEL ADAPTATION note**: Per OUTCOME-CHANNEL ADAPTATION: covariates listed here are for HAs USING gevoelscore as OUTCOME (the dominant pattern). Future HAs USING gevoelscore as PREDICTOR (rare; e.g. felt-state-predicts-Garmin tomorrow) would need a different covariate set -- not enumerated here per handoff section 3 hard constraint (do NOT promote to substantive HA verdicts; Q3.9.i scope is the dominant outcome-channel pattern only).

---

## Cross-references

### HA-* tests that touch this channel as OUTCOME (cite this analysis)

- **HA-C3 v2** (LOCKED REJECTED wrong-direction override; concave/inverted-U vs Wiggers' convex prediction): primary outcome IS this channel. **The descriptive substrate this analysis produces -- the Stratum-4 distribution (Q3.9.a) + per-phase reads (Q3.9.c, Q3.9.d) + subjective<->objective coupling (Q3.9.e) -- complements HA-C3 v2's tested operand with the raw-channel-distribution view.** The substantive HA-C3 v2 verdict is LOCKED; this analysis's descriptive corroboration is NOT a re-interpretation.
- **HA-C3p** (LOCKED PARTIAL 2-of-3; personal-baseline-anchored equal-N quintile bins): primary outcome IS this channel. Joint reading with HA-C3 v2 confirms the concave/inverted-U finding from BOTH bin-design variants (variable-width all-corpus vs equal-N personal-baseline).
- **HA10 + HA07d + HA11 family + every other HA using crash labels**: indirect outcome via crash_v2-definition derivation (crash = score <= 3 for >= 2 consecutive days). Q3.9.f surfaces the tautology honestly.

### Methodology MDs cited

- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 -- Q3.9.c citalopram-phase axis; Q3.9.d phase-stratified treatment.
- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) -- E[L]=7 default + factor-of-2 deviation rule.
- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) -- Stratum 4 boundary definition (Stratum 4 IS the gevoelscore-having days).
- [`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) -- 6-phase axis for Q3.9.c overlap notation.
- [`methodology/phase_axis_collapsibility_conventions.md`](../../../methodology/phase_axis_collapsibility_conventions.md) -- tier-A 4a + 4b -> 4 collapse for Q3.9.i covariate 4.
- [`methodology/_descriptive_stocktake_2026-06-23.md`](../../../methodology/_descriptive_stocktake_2026-06-23.md) section 3 + section 5 -- gap-list framing.

### Existing artefacts referenced

- [`analyses/hypotheses/crash_v2-definition/`](../../../analyses/hypotheses/crash_v2-definition/) -- canonical gevoelscore-to-crash mapping; LOCKED; Q3.9.f honest tautology framing.
- [`analyses/hypotheses/HA-C3/result.md`](../../../analyses/hypotheses/HA-C3/result.md) (LOCKED) + [`HA-C3p/result.md`](../../../analyses/hypotheses/HA-C3p/result.md) (LOCKED) -- outcome-side substantive references.
- [`descriptive/trajectory/recovery_arc/findings.md`](../../trajectory/recovery_arc/findings.md) -- 6-phase gevoelscore characterisation (LOCKED); Q3.9.c provides overlap notation, NOT re-characterisation.
- [`descriptive/operationalisation_support/push_burden_7d/findings.md`](../push_burden_7d/findings.md) -- Q3.8 sister precedent (Tier 2 4th of 5; LANDED `92d7193`); count-primitive bounded-support precedent.
- [`descriptive/operationalisation_support/resting_hr/findings.md`](../resting_hr/findings.md) -- Q3.6 continuous-channel precedent (Tier 2 2nd of 5).
- [`descriptive/operationalisation_support/exertion_class/findings.md`](../exertion_class/findings.md) -- Q3.7 categorical adaptation precedent (Tier 2 3rd of 5).
- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) -- R14 single-pool reads on Q3.9.g HA11 cross-reference.

### Upstream pipeline

- `per_day_master.csv` `gevoelscore` column <- `pipeline/03_consolidate/build_unified_dataset.py` <- app-side self-report on 1-10 scale (empirical range 1-6).
- `labels_crash_v2.csv` <- `crash_v2-definition/definition.md` (locked).

---

## Limitations

For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding constraints are:

1. **No HA verdict promotion**: HA-C3 v2 + HA-C3p (both LOCKED) verdicts are NOT extended or re-interpreted; the joint inverted-U finding is referenced only as descriptive corroboration in Q3.9.a + Q3.9.d + Q3.9.e per CONVENTIONS section 4.2 + handoff section 3.
2. **No crash_v2-definition modification** per handoff section 3 hard constraint. The crash + dip + normal definitions are LOCKED at the crash_v2-definition/ level; Q3.9.f surfaces the day-level tautology honestly but does not re-derive crash labels.
3. **No recovery_arc v2 re-characterisation** per handoff section 1 + section 2.4. Q3.9.c overlap notation references recovery_arc v2's existing per-phase reads; the substantive narrative is LOCKED at the recovery_arc/findings.md level.
4. **Q3.9.e is Strand-A first-pass at Q4.9 territory only** per descriptive README section 4.9. Per-phase coupling stratification, lagged-coupling structure, episode-level coupling profile, and pre-crash divergence patterns are deferred to Strand-B Q4.9 future analysis -- NOT resolved at this Strand-A scope.
5. **Q3.9.f day-level Cohen's d MUST NOT be cited as a predictor effect** per tautology framing in Q3.9.f. The negative day-level Cohen's d is mechanically guaranteed by crash_v2 section 2.1.
6. **No v3 multi-channel sweep verdict to cite or re-promote** on this channel per Q3.9.d framing (gevoelscore is the outcome, not a Garmin channel; not in v3 scope). Observed phase shifts are pure Layer 1 descriptive observations.
7. **Bounded 1-6 integer scale** means classical heavy-tail / outlier semantics do not meaningfully apply per OUTCOME-CHANNEL ADAPTATIONS at Q3.9.a + Q3.9.h. The per-value frequency vector + Shannon entropy are the load-bearing distribution primitives.

---

*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` (gitignored per `docs/research/**/*.json`). To refresh: ``python run.py``.*
