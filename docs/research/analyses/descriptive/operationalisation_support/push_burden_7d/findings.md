# Findings -- `push_burden_7d` operationalisation-support descriptive (Q3.8.a-i)

**Channel**: `push_burden_7d_lagged` (HA02c primary operand; per-day count of push-days in trailing 7d window above the v3.2 lagged baseline; integer-valued bounded support [0, 6]; channel as it lives in master after audit MD 2026-06-11 item 2 dropped the v3.1 un-lagged variant). Column semantics: activity-labels family per [`activity-labels/definition.md`](../../../analyses/garmin_exploration/activity-labels/definition.md) + CONVENTIONS section 3.2 `[d-90, d-30]` lagged-baseline window.

**Substantive context**: HA02c is LOCKED at REJECTED both eras (train -18.7 pp / validate +0.7 pp) per [`REJECTED.md`](../../../REJECTED.md) HA02c row + [`activity-labels/output/ha_results_4day_lagged.md`](../../../analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md). HA02c was NOT in the R14 single-pool re-anchor stretch list per [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md); the closest single-pool diagnostic neighbour is the sister activity-axis HA01b-recomputed (R14 single-pool **+5.1 pp [CI -14.7, +13.3] perm p (E[L]=7) = 0.3689** NOT-SUPPORTED CONVERGE; `badd04a`). This Q3.8 is the Strand-A operationalisation-support backstop on the v3.2 lagged channel; the HA02c + HA01b-recomputed + R14 substantive verdicts are LOCKED and descriptively corroborated only.

**v3.1 -> v3.2 lagged-baseline correction context**: per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed + descriptive README section 3.4 explicit acknowledgment of 'push_burden's rolling-baseline contamination'. The v3.1 push_burden_7d used a 30-day trailing rolling baseline that included the candidate day (in sustained-push periods the baseline crept up with the pushes; the channel rebased into its own reference frame). v3.2 fixes this with a `[d-90, d-30]` window (the `_lagged` variant in master). The v3.1 un-lagged `push_burden_7d` was DROPPED from master per [`garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) audit 2026-06-11 item 2 (known rolling-baseline contamination). Per CONVENTIONS section 4.2 caveat-class framing: this Q3.8 reports the v3.2 channel descriptively; it does **NOT re-litigate the v3.1 -> v3.2 correction** (handoff section 3 hard constraint).

**CONVENTIONS section 3.2 / audit-MD contradiction** (surfaced per [[feedback_flag_contradictions]]): CONVENTIONS section 3.2 says v3.1 `push_burden_7d` 'stays in the master for backward compatibility with HA01b / HA02c'; audit MD 2026-06-11 item 2 explicitly removed it. The pipeline-side reality (column absent in master) binds this Q3.8; CONVENTIONS section 3.2 needs a stocktake refresh. NOT re-litigated here.

**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to 2026-06-05). n=1372 days with channel out of 1372 Stratum 4 days (0 NaN days).

**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`) -- HA-touched non-confirmed channel candidate list bullet `exertion_class + push_burden_7d (HA01b/HA01c primaries) -- partially covered by activity-labels/`. **4th of the 5 Tier 2 channels** in the user-prioritised Phase 2 sequential batch (Tier 1 closed `39d7693`; Tier 2 1st = Q3.5 bb_overnight_gain `7d49ba4`; Tier 2 2nd = Q3.6 resting_hr `5d28219`; Tier 2 3rd = Q3.7 exertion_class `9b03bed`; this Q3.8 closes Tier 2 4th; next: Q3.9 gevoelscore -- dispatched in parallel). Q3.8.a-i template applied per section 3.1 verbatim.

**Sources**: `per_day_master.csv` (Garmin v3.2 activity-axis composite) + `labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level per CONVENTIONS section 3.6).

**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). HA02c + HA01b-recomputed (LOCKED) + R14 HA01b-recomputed single-pool re-anchor (LOCKED `badd04a`) cross-references in this analysis are **descriptive corroboration only**; the substantive verdicts live in those result.md / REJECTED.md rows and are NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). No v3.1 -> v3.2 correction re-litigation per the handoff section 3 hard constraint. Statistical hygiene anchors: section 3.1 (personal baseline), section 3.2 (lagged-baseline discipline -- this channel IS the v3.2 fix), section 3.3 (column-duplication threshold |rho|>=0.92), section 3.4 (crash-drop sensitivity |delta|>0.10), section 3.5 (spike metrics -- this channel IS a count primitive on the activity axis), section 3.6 (named counts).

---

## Headline

`push_burden_7d_lagged` on Stratum 4 is an **integer-valued bounded-support [0, 6] right-skewed count primitive on the activity axis** (skew=+0.58, excess kurtosis=-0.33, heavy_tail_flag=False, p99/median = 5.00/2.00 = 2.50, fraction at 0 = 19.2%, fraction at >=4 = 14.1%). The **data-driven E[L]\*=7.0** (Politis-White; deviation ratio 0.00; factor-of-2 flag = False; cutoff lag M=None). Cross-channel context per handoff section 2.4: vs sister Strand-A channels stress_stdev_sleep 7.0 / bb_overnight_gain 6.5 / stress_mean_sleep 12.6 / stress_low_motion 21.1 / bb_lowest 29.25 / all_day_stress_avg 29.8 / resting_hr 7.0 (fallback) / exertion_class 7.0 (ordinal); push_burden_7d_lagged's E[L]\*=7.0 sits in the **autocorrelation-SPARSE-MEMORY** regime. **Phase-stratified medians** (citalopram axis): unmedicated 2.00 -> buildup 2.00 -> consolidation 2.00 -> afbouw 3.00 (consolidation-minus-unmedicated = +0.00). Day-resolved citalopram boundary step (2024-04-09 pre/post 30d) is **+0.70**. Crash-vs-normal: episode-level d=+0.13 (bootstrap CI95 [-0.36, +0.69]); day-level Mann-Whitney U z=-1.98 p=0.0473 P(crash>normal)=0.443 -- descriptively re-anchors HA02c's locked REFUTED-both-eras outcome (REJECTED.md HA02c row) at the first-order day-level read (HA02c's tested operand IS this Q3.8 channel at the spike-form Wiggers level). Near-identity check: **1 (expected: _lcera sibling; possibly exertion_class_lagged sibling)** at the |rho|>=0.92 CONVENTIONS section 3.3 threshold (the v3.2 _lcera sibling channel and possibly the exertion_class_lagged sister are the expected high-rho neighbours).

---

## Q3.8.a -- Distribution shape (Stratum 4)

`push_burden_7d_lagged` is an **integer-valued count primitive** with bounded support [0, 6] (per-day count of push-days in trailing 7d window above the v3.2 lagged baseline). For an integer-valued bounded-support channel the per-value frequency table is the load-bearing distribution descriptor; mean / median / MAD / quantiles apply identically to the continuous-template precedent (Q3.5 / Q3.6) but the heavy-tail flag interpretation is bounded by the support ceiling.

| stat | value | source |
|---|---:|---|
| n (Stratum 4) | 1372 | `per_day_master.csv` `push_burden_7d_lagged` non-NaN within S4 |
| mean | 1.832 | (single-pool S4) |
| median | 2.000 | |
| std (ddof=1) | 1.418 | |
| MAD (unscaled) | 1.000 | |
| MAD x 1.4826 (normal-equivalent SD) | 1.483 | for robust z-score scaling per section 3.1 |
| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | 0.0 / 0.0 / 0.0 / 1.0 / 2.0 / 3.0 / 4.0 / 4.0 / 5.0 | |
| skewness (Fisher-Pearson) | **+0.58** | right-skewed |
| excess kurtosis (Fisher) | **-0.33** | |
| heavy_tail_flag | **False** | skew>1 OR p99/median > 3.0 (bounded support [0, 6] caps the upper tail) |
| range | 0.0 to 6.0 | bounded by definition |
| fraction at 0 (no push in 7d) | **19.2%** | the no-push fraction |
| fraction at >=4 (sustained push week) | **14.1%** | the sustained-push fraction |

### Per-value frequency table

| value | n days | fraction |
|---:|---:|---:|
| 0 | 264 | 19.2% |
| 1 | 369 | 26.9% |
| 2 | 341 | 24.9% |
| 3 | 205 | 14.9% |
| 4 | 127 | 9.3% |
| 5 | 57 | 4.2% |
| 6 | 9 | 0.7% |

**push_burden_7d_lagged is a v3.2 lagged-baseline count primitive on the activity axis** (per-day count of push-days in trailing 7d window above the [d-90, d-30] lagged baseline). Distinct from the categorical sister Q3.7 exertion_class (5-level ordinal {none, light, moderate, heavy, very_heavy}) by aggregation: exertion_class is per-day classification; push_burden_7d_lagged is the within-7d count-of-push-above-baseline. The two channels share the activity-labels v3.2 family ancestry.

### Cross-channel comparison vs sister continuous Strand-A channels

| stat | push_burden_7d_lagged (this analysis) | resting_hr (Q3.6) | bb_overnight_gain (Q3.5) | stress_stdev_sleep (Q3.4) |
|---|---:|---:|---:|---:|
| n S4 | 1372 | 1357 | 593 | 1337 |
| mean | 1.83 | 56.68 | 16.65 | 7.18 |
| median | 2.00 | 56.00 | 16.00 | 6.00 |
| MAD (unscaled) | 1.00 | 2.00 | 4.00 | 2.00 |
| skewness | +0.58 | +0.25 | +0.97 | +1.71 |
| heavy_tail_flag | **False** | **False** | **False** | **True** |
| type | **integer count [0, 6]** | continuous bpm | continuous BB units | continuous stress units |

See [`plots/fig1_distribution_s4.png`](plots/fig1_distribution_s4.png).

---

## Q3.8.b -- Autocorrelation structure + E[L]\* + v3.1 -> v3.2 correction citation

The **data-driven block length is E[L]\*=7.0** (Politis-White 2004 with Patton-Politis-White 2009 correction per [`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) vs the project default E[L]=7 per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). The **factor-of-2 deviation flag = False** (deviation ratio = 0.00). Cutoff lag M=None.

| lag (days) | autocorrelation |
|---:|---:|
| 1 | +0.909 |
| 2 | +0.814 |
| 3 | +0.720 |
| 7 | +0.336 |
| 14 | +0.287 |

Politis-White 2-sigma significance threshold (n=1372): |rho| = 0.145.

### Cross-channel comparison (E[L]\* by Strand A analysis) -- handoff section 2.4 load-bearing

| analysis | channel | E[L]\* |
|---|---|---:|
| Q3.5 (bb_overnight_gain, truth window) | per-night SLEEPEND-SLEEPSTART | 6.5 |
| Q3.4 (stress_stdev_sleep) | per-night STDEV | 7.0 |
| Q3.6 (resting_hr) | daily UDS restingHeartRate | 7.0 (fallback) |
| Q3.7 (exertion_class ordinal) | 5-level activity class | 7.0 |
| Q3.1 (stress_mean_sleep) | sleep-window mean | 12.6 |
| Phase-1 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 |
| Q3.3 (bb_lowest) | daily NADIR | 29.25 |
| Q3.2 (all_day_stress_avg) | 24h-window mean | 29.8 |
| **this analysis (push_burden_7d_lagged)** | **integer count [0, 6] (within-7d burden)** | **7.0** |

### v3.1 -> v3.2 lagged-baseline correction (descriptive citation only)

Per CONVENTIONS section 3.2 + REJECTED.md HA01b-recomputed row + descriptive README section 3.4 explicit acknowledgment + garmin_indicators_audit.md audit 2026-06-11 item 2:

- **The v3.1 problem**: `push_burden_7d` used a 30-day TRAILING rolling baseline that included the candidate day; in sustained-push periods the baseline crept up with the pushes (the channel rebased into its own reference frame and stopped looking heavy). Descriptive README section 3.4 names this as 'push_burden's rolling-baseline contamination'.
- **The v3.2 fix**: switch to a `[d-90, d-30]` window (the `_lagged` variant in master; this Q3.8's channel). The lagged-baseline correction is the canonical project example of why baseline construction matters for sustained-push hypotheses.
- **The outcome for HA01b-recomputed**: train +5.8 / validate +4.0 pp -- the original v3.1 validate +17.3 pp 'first SUPPORTED' headline softened by -13.3 pp on v3.2 recomputation (REJECTED.md HA01b-recomputed row). The original headline was substantially a baseline-construction artefact.
- **The outcome for HA02c (this Q3.8's channel)**: train -18.7 / validate +0.7 pp -- the lagged-baseline correction improved measurement standing but did NOT resurrect push_burden as a predictor (REJECTED.md HA02c row).
- **The master-side reality**: the v3.1 un-lagged `push_burden_7d` was DROPPED from the master per garmin_indicators_audit.md audit 2026-06-11 item 2 ('known rolling-baseline contamination'). Only the v3.2 `_lagged` variant (this Q3.8's channel) and the `_lagged_lcera` variant are present.

Per handoff section 3 hard constraint: this Q3.8.b citation is **descriptive only**; the v3.1 -> v3.2 correction story is LOCKED at the CONVENTIONS section 3.2 + REJECTED.md + audit MD level and NOT re-litigated here. The autocorrelation reading is on the v3.2 channel.

See [`plots/fig5_acf.png`](plots/fig5_acf.png).

---

## Q3.8.c -- Base rates per citalopram phase (Stratum 4)

Phase axis per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3:

| phase | window | n | median | mean | MAD | p10 / p90 | frac=0 | frac>=4 |
|---|---|---:|---:|---:|---:|---|---:|---:|
| unmedicated | 2022-09-03 to 2024-04-08 | 584 | **2.00** | 1.85 | 1.00 | 0.00 / 4.00 | 20.0% | 16.1% |
| buildup | 2024-04-09 to 2024-06-19 | 72 | **2.00** | 2.01 | 1.00 | 1.00 / 3.00 | 4.2% | 9.7% |
| consolidation | 2024-06-20 to 2026-03-19 | 638 | **2.00** | 1.70 | 1.00 | 0.00 / 4.00 | 21.6% | 11.8% |
| afbouw | 2026-03-20 to 2026-06-05 | 78 | **3.00** | 2.60 | 1.00 | 1.00 / 4.00 | 7.7% | 21.8% |

The two **transition phases** (buildup n=72; afbouw n=78) have **n<79** each; the two **steady-state phases** (unmedicated n=584; consolidation n=638) are larger. Any HA test that wants per-phase verdicts on this channel faces a sample-size disadvantage in the transition phases (parity with sister channels Q3.1.c / Q3.2.c / Q3.3.c / Q3.4.c / Q3.5.c / Q3.6.c / Q3.7.c).

Named counts (CONVENTIONS section 3.6): the per-phase n's above are `push_burden_7d_lagged`-non-NaN day rows in `per_day_master.csv` within Stratum 4 date masks per `citalopram_phase_stratification.md section 3` boundary dates.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png).

---

## Q3.8.d -- Phase-stratified distribution + v3 scope status

**Per CONVENTIONS section 4.2 (caveats yes; a-priori claims no)**: push_burden_7d is NOT in the v3 multi-channel sweep scope per [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.6 (6-channel scope: stress_mean_sleep + all_day_stress_avg + bb_lowest + resting_hr + bb_overnight_gain + respiration_avg_sleep; activity-labels family is not in v3 scope). No v3 verdict exists to cite or re-promote on this channel. HA02c (the Wiggers test on this channel) is LOCKED REFUTED per REJECTED.md HA02c row. This Q3.8.d reports the observed median shifts descriptively.

Observed median shifts:

| comparison | delta median | within-phase MAD | within-MAD? |
|---|---:|---:|---|
| buildup minus unmedicated | **+0.00** | 1.00-1.00 | within 1 MAD |
| consolidation minus unmedicated | **+0.00** | 1.00-1.00 | within 1 MAD |
| consolidation minus buildup | **+0.00** | -- | -- |
| afbouw minus consolidation | **+1.00** | 1.00-1.00 | -- |
| afbouw minus unmedicated | **+1.00** | -- | -- |

### Descriptive reading (no verdict promotion)

The median moves from unmedicated (2.00) to consolidation (2.00) by **+0.00**. The day-resolved citalopram boundary step (30d pre/post 2024-04-09): **+0.70**. Per CONVENTIONS section 4.2: this is a Layer 1 descriptive observation; no a-priori claim is made about the shift's mechanism. push_burden_7d_lagged is the activity-axis count primitive -- the citalopram axis is not the natural confound axis for this channel (activity-labels family does NOT belong to the autonomic / cardiovascular v3 dose-response scope). Phase-stratified shifts on this activity-axis channel are reported for completeness; the substantive activity-axis story lives in the HA02c + HA01b-recomputed (LOCKED REFUTED) family.

### HA02c + HA01b-recomputed locked-verdict cross-reference (per handoff section 2.4 + R14 row)

Per handoff section 2.4 + REJECTED.md: HA02c (push burden on Theme A lagged baseline, REFUTED both eras train -18.7 / validate +0.7); HA01b-recomputed (v3.2 lagged composite at exertion_class_lagged in {{heavy, very_heavy}}, REFUTED both eras train +5.8 / validate +4.0; R14 single-pool +5.1 pp [CI -14.7, +13.3] perm p=0.3689 NOT-SUPPORTED CONVERGE per single_pool_reanchor/findings.md HA01b-recomputed row `badd04a`). HA02c itself was NOT in the R14 single-pool re-anchor stretch list (single_pool_reanchor/findings.md HA02c row absent); the HA01b-recomputed family R14 is the closest sister-channel single-pool re-anchor on the activity-axis. The per-phase median shifts observed in Q3.8.d's table above are at the count primitive's bounded support [0, 6]; this is the descriptive complement to HA02c's REJECTED-both-eras verdict.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) and [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d rolling median through phases).

---

## Q3.8.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)

Brief-mandated targets per handoff section 2.4: sister Q3.7 exertion_class via Spearman on ordinal-vs-numeric (load-bearing); activity-labels family v3.2 lagged siblings (the _lcera variant is the natural near-identity candidate); cross-family autonomic / cardiovascular companions.

| target channel | n | Pearson r | Spearman rho | near-identity flag? |
|---|---:|---:|---:|---|
| `exertion_class_lagged` (ordinal-encoded) | 1372 | +0.309 | +0.301 | no |
| `exertion_class_lagged_lcera` (ordinal-encoded) | 1372 | +0.309 | +0.301 | no |
| `eff_exertion_rank_lagged` | 1372 | +0.404 | +0.368 | no |
| `eff_exertion_rank_lagged_lcera` | 1372 | +0.404 | +0.368 | no |
| `exertion_rank_composite_lagged` | 1372 | +0.278 | +0.297 | no |
| `exertion_rank_composite_lagged_lcera` | 1372 | +0.278 | +0.297 | no |
| `push_burden_7d_lagged_lcera` | 1372 | +1.000 | +1.000 | **YES** |
| `exertion_class` (ordinal-encoded) | 1372 | +0.156 | +0.146 | no |
| `effective_exertion_min` | 1372 | +0.295 | +0.297 | no |
| `effective_exertion_slope_28d` | 1372 | +0.449 | +0.442 | no |
| `stress_mean_sleep` | 1339 | -0.005 | +0.038 | no |
| `all_day_stress_avg` | 1359 | +0.040 | +0.065 | no |
| `stress_low_motion_min_count_S60_Mlow` | 1365 | +0.029 | +0.060 | no |
| `stress_stdev_sleep` | 1339 | +0.042 | +0.050 | no |
| `resting_hr` | 1357 | +0.061 | +0.091 | no |
| `bb_overnight_gain` | 593 | +0.092 | +0.079 | no |
| `bb_lowest` | 1359 | -0.107 | -0.097 | no |
| `respiration_avg_sleep` | 1335 | -0.113 | -0.096 | no |

**1 near-identity pairs fire** at the |rho|>=0.92 CONVENTIONS section 3.3 threshold. The Q3.7 exertion_class sister (just LANDED `9b03bed`) reciprocally reports here the ordinal-encoded Spearman against this channel's numeric count form per handoff section 2.4 (load-bearing sibling activity-axis check). The expected near-identity pair is the `push_burden_7d_lagged_lcera` channel (same v3.2 lagged-baseline ancestry with the LC-era restriction layered on top); a high rho there is **expected by construction**, not a discovery. Any cross-family flags (stress / cardiovascular) would be material findings.

---

## Q3.8.f -- Crash-day vs normal-day (Stratum 4) + HA02c + HA01b-recomputed corroboration

Per CONVENTIONS section 3.6 named counts: 29 crash-episodes (crash_v2 episode-level via `labels_crash_v2.csv` unique `episode_id` starting with `crash-`); 103 crash-days (day-level, `label=='crash'`); 1269 non-crash days (the complement within Stratum 4 channel-valid days).

### Episode-level (primary unit per CONVENTIONS section 3.6)

| stat | value |
|---|---:|
| n crash-episodes | 29 |
| n normal-day base rate | 1269 |
| mean per-episode `push_burden_7d_lagged` | 2.025 |
| mean normal-day `push_burden_7d_lagged` | 1.848 |
| mean diff (episode minus normal-day) | **+0.177** |
| Cohen's d (episode-level vs normal-day pooled) | **+0.13** |
| Bootstrap 95% CI on mean diff | **[-0.358, +0.693]** (5000 iters, seed=20260624) |

**Episode-level Cohen's d=+0.13** on this channel. HA02c's substantive direction prior: sustained-push burden in trailing 7d window is hypothesised to elevate crash risk (the higher-burden-day -> higher-crash-rate direction). The Q3.8.f observation is a descriptive day-level complement to HA02c's Wiggers-test operand; HA02c's REJECTED verdict is LOCKED.

### Day-level (autocorrelation-inflated supplementary)

| stat | value |
|---|---:|
| n crash-days | 103 |
| n normal-days | 1269 |
| mean crash-day | 1.631 |
| mean normal-day | 1.848 |
| median crash-day | 1.00 |
| median normal-day | 2.00 |
| mean diff (point estimate) | **-0.217** |
| median diff | **-1.00** |
| Cohen's d | **-0.15** |
| Mann-Whitney U: z | **-1.98** |
| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **0.0473** |
| Mann-Whitney U: P(crash > normal) | **+0.443** |
| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (project default) | [-0.772, +0.439], width 1.211 |
| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (data-driven, Q3.8.b flag) | **[-0.772, +0.439]**, width 1.211 |

### LOAD-BEARING HA02c + HA01b-recomputed R14 single-pool descriptive cross-reference (per handoff section 2.4)

Per REJECTED.md HA02c row: **LOCKED REFUTED both eras** (train -18.7 pp / validate +0.7 pp). Push burden on Theme A lagged baseline; the lagged-baseline correction improved measurement standing but did NOT resurrect push_burden as a predictor. HA02c was NOT in the R14 single-pool re-anchor stretch list per [single_pool_reanchor/findings.md](../single_pool_reanchor/findings.md) (HA02c row absent); the closest single-pool diagnostic neighbour is the sister activity-axis HA01b-recomputed row: **+5.1 pp [CI -14.7, +13.3] perm p=0.3689 NOT-SUPPORTED CONVERGE (both NOT-SUPPORTED)** (`badd04a`). This Q3.8.f's first-order day-level Cohen's d=**+0.13** (episode-level) + Mann-Whitney U p=0.0473 (day-level) **descriptively corroborate** the locked HA02c REFUTED-both-eras outcome at the channel-distribution level. **The HA02c + HA01b-recomputed + R14 substantive verdicts are LOCKED**; this Q3.8.f observation is descriptive corroboration only, NOT a re-interpretation.

### Crash-drop sensitivity (CONVENTIONS section 3.4)

| frame | Spearman rho | n |
|---|---:|---:|
| full Stratum 4 | +0.070 | 1372 |
| crash-days dropped | +0.053 | 1269 |
| \|delta\| | **0.017** | -- |
| section 3.4 threshold (0.10) crossed? | **no** | -- |

See [`plots/fig4_crash_vs_normal.png`](plots/fig4_crash_vs_normal.png).

---

## Q3.8.g -- Spike-detecting primitive availability

`push_burden_7d_lagged` IS itself a count primitive (count of push-days in trailing 7d window above the v3.2 lagged baseline) -- the channel value at day d is the spike-form on the activity axis (the within-7d burden-spike construct). Per CONVENTIONS section 3.5 spike/peak/count metrics preference: **this channel IS the spike-form construct on the activity-axis**; HA02c's tested operand IS this channel at the per-day count resolution; HA01b-recomputed tested the sister exertion_class_lagged {heavy, very_heavy} classifier form at the same Wiggers level. Both HA02c and HA01b-recomputed are LOCKED REFUTED both eras on v3.2 lagged baseline.

Activity-axis primitives + companion siblings in master (for cross-channel pairwise comparison):

- `exertion_class` (n non-NaN = 1372)
- `exertion_class_lagged` (n non-NaN = 1372)
- `exertion_class_lagged_lcera` (n non-NaN = 1372)
- `eff_exertion_rank_lagged` (n non-NaN = 1372)
- `eff_exertion_rank_lagged_lcera` (n non-NaN = 1372)
- `exertion_rank_composite_lagged` (n non-NaN = 1372)
- `push_burden_7d_lagged_lcera` (n non-NaN = 1372)
- `effective_exertion_min` (n non-NaN = 1372)
- `effective_exertion_slope_28d` (n non-NaN = 1372)

### Pairwise correlations on Stratum 4

| partner channel | Pearson r | Spearman rho | n |
|---|---:|---:|---:|
| `exertion_class_lagged` | +0.309 | +0.301 | 1372 |
| `eff_exertion_rank_lagged` | +0.404 | +0.368 | 1372 |
| `push_burden_7d_lagged_lcera` | +1.000 | +1.000 | 1372 |
| `effective_exertion_slope_28d` | +0.449 | +0.442 | 1372 |

**Latent in FIT, not in master**:

- per-minute / per-second activity primitives (NOT in master; would require FIT-side extraction; activity-labels family is already a per-day aggregate by definition per activity-labels/definition.md)
- instantaneous exertion rate (NOT in master; HA-C4c uses exertion_class_lagged_lcera in {heavy, very_heavy} on T as a per-day heavy classifier instead)

Per CONVENTIONS section 3.5: spike/peak/count metrics preferred over daily means -- `push_burden_7d_lagged` IS the count primitive on the activity axis (count of push-days above lagged baseline in trailing 7d). Per CONVENTIONS section 3.2: prefer the v3.2 `_lagged` variant over the v3.1 rolling-baseline variant -- this Q3.8 channel IS the v3.2 fix. HA02c (REJECTED) tested this exact channel at the spike-form Wiggers level; HA01b-recomputed (REJECTED) tested the sister exertion_class_lagged {heavy, very_heavy} form; both REJECTED both eras.

---

## Q3.8.h -- Outlier detection + calibration-drift check + activity-labels partial-coverage

Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md):

- push_burden_7d_lagged is derived from the v3.2 lagged-baseline composite per activity-labels/definition.md + CONVENTIONS section 3.2 [d-90, d-30] window discipline; the master holds it as a daily integer count in [0, 6]
- The v3.1 un-lagged push_burden_7d was DROPPED from the master per garmin_indicators_audit.md audit 2026-06-11 item 2 (known rolling-baseline contamination per descriptive README section 3.4 + CONVENTIONS section 3.2 audit hook); this Q3.8 channel IS the v3.2 fix
- activity-labels partial-coverage precedent per garmin_exploration/activity-labels/ (existing primitive validation + visualisation); the per-day classification depends on Garmin's activity-labels family + steps + moderate-VPA per activity-labels/definition.md severity cutoffs (current state: cutoffs are NOT formally LOCKED; this Q3.8.h descriptively characterises the channel AS-IS under the current classifier definition)
- The integer-valued bounded support [0, 6] means MAD-z outlier semantics interpret 'extreme' as the upper-bound value 6 (a week with 6 push-days above lagged baseline) -- this is a legitimate high-burden week, NOT a sensor failure; the n_flagged count above reports the rule output, not a sensor-failure count
- Underlying sensor is Forerunner 245 Elevate V3 throughout the entire 2021-08-16 to present window -- no device change in the analytic window; the v3.2 lagged-baseline construction is the only intermediate transform between the raw activity primitives and this channel

### Outlier scan (MAD-based |z|>5 with count-primitive caveat)

**0 outlier-day flagged** out of 1372.

For an integer-valued bounded-support count primitive, MAD-z outlier semantics interpret 'extreme' as the upper-bound value (a week with 6 push-days above lagged baseline) -- this is a legitimate high-burden week, NOT a sensor failure; the n_flagged count above reports the rule output, not a sensor-failure count.

### Drift check -- rolling 90d median over Stratum 4

| snapshot date | rolling 90d median |
|---|---:|
| 2022-12-01 | 3.0 |
| 2023-06-01 | 1.0 |
| 2023-12-01 | 2.0 |
| 2024-06-01 | 1.5 |
| 2025-01-01 | 1.0 |
| 2025-12-01 | 0.0 |
| 2026-04-01 | 2.0 |

### Citalopram boundary step (2024-04-09)

Pre-30d mean = 1.30; post-30d mean = 2.00; **diff = +0.70**.

### Consolidation boundary step (2024-06-20)

Pre-30d mean = 2.33; post-30d mean = 1.63; **diff = -0.70**.

### Afbouw boundary step (2026-03-20)

Pre-30d mean = 2.77; post-30d mean = 2.83; **diff = +0.07**.

### Activity-labels partial-coverage reference (per handoff section 2.4)

Existing primitive validation + visualisation lives in [`garmin_exploration/activity-labels/`](../../../analyses/garmin_exploration/activity-labels/) (per programme spec section 3.4 'partially covered by activity-labels/'). The per-day classification depends on Garmin's activity-labels family + steps + moderate-VPA per the family's `definition.md` severity cutoffs (current state: cutoffs are NOT formally LOCKED). This Q3.8.h descriptively characterises the v3.2 lagged-baseline-corrected channel AS-IS under the current classifier definition; the family's locking state is unchanged by this Q3.8 (descriptive layer only).

See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).

---

## Q3.8.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel

Discipline anchor: [HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) (secondary-logistic-with-covariate pattern; beta disambiguation between primary-signal and candidate alternative readings). Names **four** candidate covariates a future HA on `push_burden_7d_lagged` (or a variant) as predictor should pre-spec. Note that HA02c (LOCKED REFUTED) already tested the primary operand at the Wiggers level; further HA pre-regs would explore different operand variants.

### 1. `exertion_class_lagged ordinal (sister activity-axis spike-form per Q3.7)`

Per Q3.7 sister analysis: exertion_class_lagged is the heavy/very_heavy classifier substrate used by HA-C4c (locked PARTIAL); push_burden_7d_lagged is the count-of-push-days-above-baseline in a 7d window form. The covariate disambiguates: beta_channel attenuates -> the push_burden signal is shared with the within-day heavy/very_heavy classification (the count-form captures the same activity-axis information as the categorical form); beta_channel survives -> the count-of-push-days-in-7d carries windowed-burden information distinct from per-day class.

*Source*: Q3.7 exertion_class sister analysis cross-pair table

*Observed correlation on S4*: Pearson r=+0.309 / Spearman rho=+0.301 (n=1372) (exertion_class_lagged ordinal-encoded per CATEGORY_ORDER).

### 2. `push_burden_7d_lagged_lcera (LC-era-restricted baseline variant)`

Per CONVENTIONS section 3.2: the _lcera variant restricts the [d-90, d-30] baseline to LC-era days only (>= 2022-04-04), so pre-LC and corona days don't dilute the reference. The covariate disambiguates: beta_channel attenuates -> the LC-era restriction doesn't add information; beta_channel survives -> the LC-era-specific baseline normalisation IS load-bearing. Default for PEM-pacing tests gated on lc_phase == 'lc' is the _lcera variant per CONVENTIONS section 3.2; any future HA on push_burden should pre-spec the _lcera variant as primary and the non-LC-restricted variant as secondary sensitivity arm.

*Source*: CONVENTIONS section 3.2 _lagged_lcera convention

*Observed correlation on S4*: Pearson r=+1.000 / Spearman rho=+1.000 (n=1372).

### 3. `effective_exertion_slope_28d (28d activity-axis trajectory)`

Per the v3.2 lagged-composite landing per garmin_indicators_audit.md section 195: 'Lagged ranks composite + push_burden + slope landed in the v3.2'. The slope captures the within-28d trajectory of effective exertion; combining with push_burden (within-7d count above baseline) disambiguates whether 'push burden' is the binding signal vs the underlying trajectory. beta_channel attenuates -> the 7d count is largely the trajectory leading into the index window; beta_channel survives -> the window-specific count carries new information vs the monthly trend.

*Source*: garmin_indicators_audit.md v3.2 lagged-composite landing note

*Observed correlation on S4*: Pearson r=+0.449 / Spearman rho=+0.442 (n=1372).

### 4. `resting_hr (cross-family cardiovascular response anchor)`

Per Q3.6 sister analysis: resting_hr is the cardiovascular-recovery anchor; push_burden_7d_lagged is the activity-axis burden count. The covariate disambiguates: beta_channel attenuates -> the push-burden signal is shared with the post-burden cardiovascular response (push days carry elevated RHR); beta_channel survives -> the activity-axis burden count carries independent information beyond the cardiovascular response signature.

*Source*: Q3.6 resting_hr sister analysis cross-pair table

*Observed correlation on S4*: Pearson r=+0.061 / Spearman rho=+0.091 (n=1357).

### Recommendation

Pre-spec all four covariates as secondary sensitivity arms. The exertion_class_lagged arm (covariate 1) is the sister activity-axis spike-form disambiguator -- since Q3.7 already characterised that channel, the covariate use here is diagnostic of within-vs-windowed activity-axis signal decomposition. The _lcera arm (covariate 2) is the baseline-window-choice diagnostic per CONVENTIONS section 3.2 convention. The slope arm (covariate 3) decomposes within-7d count vs 28d trajectory. The resting_hr arm (covariate 4) is the cross-family cardiovascular-response disambiguator.

---

## Cross-references

### HA-* tests that touch this channel (cite this analysis)

- **HA02c** (push burden in trailing 7d on Theme A v3.2 lagged baseline; LOCKED REFUTED both eras train -18.7 / validate +0.7 per REJECTED.md HA02c row; NOT in R14 single-pool re-anchor stretch list): primary operand IS this channel at the spike-form Wiggers level. **The descriptive substrate this analysis produces -- the Stratum-4 distribution (Q3.8.a) + autocorrelation E[L]\*=X (Q3.8.b) + per-phase reads (Q3.8.c, Q3.8.d) + first-order day-level crash-vs-normal (Q3.8.f) -- complements HA02c's tested operand with the raw-channel-distribution view.** The substantive HA02c verdict is LOCKED; this analysis's descriptive corroboration in Q3.8.f is NOT a re-interpretation.
- **HA01b-recomputed** (sister activity-axis Wiggers test; v3.2 lagged composite at exertion_class_lagged in {heavy, very_heavy}; LOCKED REFUTED both eras train +5.8 / validate +4.0 per REJECTED.md HA01b-recomputed row; R14 single-pool +5.1 pp [CI -14.7, +13.3] perm p=0.3689 NOT-SUPPORTED CONVERGE per single_pool_reanchor/findings.md HA01b-recomputed row `badd04a`): the closest single-pool diagnostic neighbour to HA02c on the activity-axis. Q3.8.f descriptively cites the R14 single-pool result as the closest sister-channel anchor.

### Methodology MDs cited

- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3 -- Q3.8.c phase axis; Q3.8.d phase-stratified treatment.
- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) -- E[L]=7 default + factor-of-2 deviation rule.
- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) -- Stratum 4 boundary definition.
- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) -- Q3.8.h cross-reference (audit 2026-06-11 item 2 push_burden_7d v3.1 drop + v3.2 lagged-composite landing).
- [`methodology/_descriptive_stocktake_2026-06-23.md`](../../../methodology/_descriptive_stocktake_2026-06-23.md) section 3 + section 5 -- gap-list framing.

### Existing artefacts referenced

- [`descriptive/operationalisation_support/exertion_class/findings.md`](../exertion_class/findings.md) -- sister Q3.7 activity-axis channel (just LANDED `9b03bed`); the ordinal-vs-numeric near-identity check in Q3.8.e re-uses Q3.7's CATEGORY_ORDER ordinal encoding.
- [`descriptive/operationalisation_support/resting_hr/findings.md`](../resting_hr/findings.md) -- Q3.6 sister continuous-channel precedent (Tier 2 2nd); clean programmatic-emit pattern.
- [`descriptive/operationalisation_support/bb_overnight_gain/findings.md`](../bb_overnight_gain/findings.md) -- Q3.5 sister continuous-channel precedent (Tier 2 1st).
- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) -- R14 HA01b-recomputed row (descriptively corroborated in Q3.8.f); HA02c row ABSENT per stretch-list scope.
- [`REJECTED.md`](../../../REJECTED.md) -- HA02c row + HA01b-recomputed row (v3.1 -> v3.2 correction).
- [`analyses/garmin_exploration/activity-labels/`](../../../analyses/garmin_exploration/activity-labels/) -- partial-coverage primitive validation + visualisation (per programme spec section 3.4 'partially covered by activity-labels/').

### Upstream pipeline

- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- activity-axis upstream classifier per `activity-labels/definition.md` severity cutoffs + v3.2 lagged-baseline construction per CONVENTIONS section 3.2 `[d-90, d-30]` window.
- `labels_crash_v2.csv` <- `garmin/hypotheses/crash_v2-definition/definition.md` (locked).

---

## Limitations

For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding constraints are:

1. **No HA verdict promotion**: HA02c + HA01b-recomputed + R14 HA01b-recomputed single-pool verdicts are LOCKED; this analysis's descriptive observations are NOT re-interpretations or re-promotions per CONVENTIONS section 4.2 + handoff section 3.
2. **No v3.1 -> v3.2 lagged-baseline correction re-litigation** per handoff section 3 hard constraint. The v3.2 correction story is LOCKED at the CONVENTIONS section 3.2 + REJECTED.md + audit MD level; Q3.8.b citation is descriptive only.
3. **HA02c was NOT in the R14 single-pool re-anchor stretch list** per single_pool_reanchor/findings.md (HA02c row absent); the descriptive cross-reference in Q3.8.f relies on the REJECTED.md HA02c locked verdict and the sister HA01b-recomputed R14 row.
4. **First-order day-level read distinct from HA02c's tested operand**: HA02c's spike-form construct (push burden in trailing 7d on lagged baseline) IS this Q3.8 channel at the count-primitive resolution; Q3.8.f's day-level Cohen's d is the descriptive-layer complement on episode-level + day-level reads.
5. **CONVENTIONS section 3.2 / audit-MD contradiction surfaced** (not re-litigated): CONVENTIONS section 3.2 says v3.1 push_burden_7d stays in master; the audit MD removed it. The pipeline-side reality binds; CONVENTIONS section 3.2 needs a stocktake refresh.
6. **activity-labels classifier definition cutoffs are NOT formally LOCKED** per activity-labels/definition.md (current state); Q3.8.h descriptively characterises the channel AS-IS under the current classifier definition.

---

*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` (gitignored per `docs/research/**/*.json`). To refresh: ``python run.py``.*
