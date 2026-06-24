# Findings -- `stress_stdev_sleep` operationalisation-support descriptive (Q3.4.a-i)

**Channel**: `stress_stdev_sleep` (HA07d primary operand; per-night STDEV of sleep-window monitoring_b stress samples, custom FIT extraction per [`garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`](../../../../garmin/scripts/sleep_stress_extract/extract_sleep_stress.py); MIN_SAMPLES_PER_NIGHT=120 gate; same nightly sample set as sister `stress_mean_sleep`). Column semantics: [DATA_DICTIONARY.md sleep-stress section](../../../DATA_DICTIONARY.md).

**Substantive context**: HA07d is the **only canonical both-eras-SUPPORTED test in the project** (train +19.6 pp / validate +21.7 pp / OVERALL SUPPORTED per [`HA07d-sleep-stress-variability/result.md`](../../../analyses/hypotheses/HA07d-sleep-stress-variability/result.md)) AND just R14-confirmed at single-pool +19.7 pp [CI -18.1, +17.0] perm p (E[L]=7) = 0.0291 per [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) row HA07d -- the **only HA that retained SUPPORTED at single-pool** in the R14 cross-check (`badd04a`). This Q3.4 is the Strand-A backstop on the channel; the HA07d substantive verdicts are LOCKED and descriptively corroborated only.

**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 to 2026-06-05). n=1339 days with channel out of 1372 Stratum 4 days (33 NaN nights from MIN_SAMPLES_PER_NIGHT=120 gate; sleep_valid_flag=False).

**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`) -- HA-touched non-confirmed channel candidate list; specifically the section 3.4 bullet "`stress_stdev_sleep` (HA07d primary, the only canonical-SUPPORTED test) -- needs a Strand A analysis for the variability story". This analysis is the **FINAL Tier 1 channel** in the user-prioritised Phase 2 sequential batch (R14 `single_pool_reanchor` first at `badd04a`; Q3.2 `all_day_stress_avg` second at `cf34ab1`; Q3.3 `bb_lowest` third at `40c351b`; this Q3.4 closes Tier 1). Q3.4.a-i template applied per section 3.1 verbatim (substituted channel name + adapted section 3.4.d to NOT-in-v3-scope caveat-class framing).

**Sources**: `per_day_master.csv` (Garmin daily aggregate) + `labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level per CONVENTIONS section 3.6).

**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). HA07d (LOCKED OVERALL-SUPPORTED + R14 single-pool SUPPORTED) + HA07c (LOCKED OVERALL-REFUTED with train-only-SUPPORTED) + HA08c (LOCKED OVERALL-REFUTED with train-only-SUPPORTED) cross-references in this analysis are **descriptive corroboration only**; the substantive verdicts live in those result.md files and are NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). Statistical hygiene anchors: section 3.1 (personal baseline), section 3.3 (column-duplication threshold |rho|>=0.92), section 3.4 (crash-drop sensitivity |delta|>0.10), section 3.5 (spike metrics -- stress_stdev_sleep IS the second-order within-night variability primitive; HA07d's tested operand is the per-4-day spike-form construct on this channel), section 3.6 (named counts).

---

## Headline

`stress_stdev_sleep` on Stratum 4 is a **right-skewed, autocorrelation-SPARSE per-night dispersion channel** (skew=+1.87, excess kurtosis=+5.41, heavy_tail_flag=True, p99/median = 17.00/7.09 = 2.40). The **data-driven E[L]\*=7.0** (Politis-White; deviation ratio 0.00; factor-of-2 flag = False; cutoff lag M=1). Cross-channel context per handoff section 2.4: vs sister Strand-A channels `stress_mean_sleep` E[L]\*=12.6 + `stress_low_motion_min_count_S60_Mlow` 21.1 + `bb_lowest` 29.25 + `all_day_stress_avg` 29.8 -- this channel sits near mean-sibling stress_mean_sleep (12.6). **Phase-stratified medians** (citalopram axis, caveat-class observation per CONVENTIONS section 4.2 since channel NOT in v3 scope): unmedicated 8.10 -> buildup 6.49 -> consolidation 6.63 -> afbouw 6.76 (consolidation-minus-unmedicated = -1.47; descriptively suggests candidacy for a future v3 extension -- NO CONFIRMED/REJECTED verdict pre-committed). Day-resolved citalopram boundary step (2024-04-09 pre/post 30d) is **+0.23 units**. Crash-vs-normal: episode-level d=+0.48 (bootstrap CI95 [+0.31, +2.15]); day-level Mann-Whitney U z=+4.69 p=<0.0001 P(crash>normal)=0.640 -- the channel-distribution corroborates the HA07d locked OVERALL-SUPPORTED signal at the coarse first-order-day-level read (HA07d's tested operand is the 4d max |z| of night-over-night delta; this Q3.4.f is the first-order day-level descriptive complement). Near-identity check vs mean sibling: zero near-identity pairs at the |rho|>=0.92 CONVENTIONS section 3.3 threshold -- the rho-with-`stress_mean_sleep` value reported in section Q3.4.e is the substantive-independence check; HA07d both-eras-SUPPORTED + HA07c train-only-SUPPORTED divergence is descriptively consistent with the observed rho.

---

## Q3.4.a -- Distribution shape (Stratum 4)

**Verdict on the section 3.1 delegate question**: **delegate is partial; extend in this analysis**. [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) primarily documents `stress_mean_sleep`; coverage on `stress_stdev_sleep` is incidental at best. The full distribution descriptors (skewness/kurtosis/heavy-tail flag/p99-vs-median ratio) are surfaced here for the first time on this channel.

| stat | value | source |
|---|---:|---|
| n (Stratum 4) | 1339 | `per_day_master.csv` `stress_stdev_sleep` non-NaN within S4 |
| mean | 7.884 | (single-pool S4) |
| median | 7.087 | |
| std (ddof=1) | 2.667 | |
| MAD (unscaled) | 1.296 | |
| MAD x 1.4826 (normal-equivalent SD) | 1.921 | for robust z-score scaling per section 3.1 |
| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | 4.62 / 5.07 / 5.43 / 6.05 / 7.09 / 9.04 / 11.45 / 13.10 / 17.00 | |
| skewness (Fisher-Pearson) | **+1.87** | right-skewed (non-negative dispersion measure; lower-bounded at 0) |
| excess kurtosis (Fisher) | **+5.41** | |
| heavy_tail_flag | **True** | skew>1 OR p99/median > 3.0 |
| range | 4.33 to 24.78 | |

### Cross-channel comparison vs sister CONFIRMED-citalopram channels + mean sibling

| stat | stress_stdev_sleep (this analysis) | stress_mean_sleep (Q3.1, mean sibling) | all_day_stress_avg (Q3.2) | bb_lowest (Q3.3) |
|---|---:|---:|---:|---:|
| n S4 | 1339 | 1339 | 1359 | (Q3.3 value) |
| mean | 7.884 | 19.97 | 32.72 | (Q3.3 value) |
| median | 7.087 | 19.21 | 32.00 | (Q3.3 value) |
| MAD (unscaled) | 1.296 | 2.87 | 4.00 | (Q3.3 value) |
| skewness | +1.87 | +2.72 | +0.87 | (Q3.3 value) |
| heavy_tail_flag | **True** | **True** | **False** | (Q3.3 value) |

**stress_stdev_sleep is a per-night SECOND-ORDER summary** (within-night STDEV of the nightly stress samples) operationally distinct from the per-night MEAN (sister `stress_mean_sleep`) even though both summarise the same monitoring_b sample set. Per HA07d result.md framing: the channel is the 'HRV-of-HRV-proxy' construct -- a second-order autonomic-flexibility signal. Distribution shape comparison with sister mean: substantially smaller absolute scale (median 7.09 stress-units of dispersion vs mean sibling median 19.21 stress-units of level), distinct skewness profile (per construction: dispersion measures are right-skewed by zero-floor regardless of the underlying signal's skew).

See [`plots/fig1_distribution_s4.png`](plots/fig1_distribution_s4.png).

---

## Q3.4.b -- Autocorrelation structure + E[L]\*

The **data-driven block length is E[L]\*=7.0** (Politis-White 2004 with Patton-Politis-White 2009 correction per [`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) vs the project default E[L]=7 per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). The **factor-of-2 deviation flag = False** (deviation ratio = 0.00). Cutoff lag M=1.

| lag (days) | autocorrelation |
|---:|---:|
| 1 | +0.200 |
| 2 | +0.117 |
| 3 | +0.116 |
| 7 | +0.081 |
| 14 | +0.095 |

Politis-White 2-sigma significance threshold (n=1339): |rho| = 0.147.

### Cross-channel comparison (E[L]\* by Strand A analysis) -- handoff section 2.4 load-bearing

| analysis | channel | E[L]\* | M | factor-of-2 flag |
|---|---|---:|---:|---|
| Phase-1 #1 (stress_mean_sleep) | sleep-window mean (mean sibling) | 12.6 | 6 | YES (factor-of-2) |
| Phase-1 #3 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 | 11 | YES (factor-of-3) |
| Phase-2 #2 (all_day_stress_avg) | 24h-window mean | 29.8 | 18 | YES (factor-of-4) |
| Phase-2 #3 (bb_lowest) | daily NADIR | 29.25 | 17 | YES (factor-of-4) |
| **this analysis (stress_stdev_sleep)** | **per-night STDEV (variability primitive)** | **7.0** | **1** | **no** |

**Implication per handoff section 2.4**: stress_stdev_sleep's E[L]\*=7.0 sits near mean-sibling stress_mean_sleep (12.6). The variability primitive sits closer to its mean sibling than to the long-memory cluster. Any HA pre-reg using `stress_stdev_sleep` (beyond HA07d's locked second-order operand) should pre-spec a sensitivity arm at E[L]\*=7 alongside the default-E[L]=7 primary. NOTE: HA07d itself used E[L]=7 for the locked test; the R14 single-pool re-anchor at +19.7 pp p=0.0291 was at E[L]=7. The Q3.4.b finding here updates the channel-level block-length characterisation for any FUTURE HA on this channel; HA07d's already-locked verdict is NOT re-anchored.

See [`plots/fig5_acf.png`](plots/fig5_acf.png).

---

## Q3.4.c -- Base rates per citalopram phase

Phase axis per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3:

| phase | window | n | median | mean | MAD | p10 / p90 |
|---|---|---:|---:|---:|---:|---|
| unmedicated | 2022-09-03 to 2024-04-08 | 572 | **8.10** | 8.50 | 1.59 | 5.75 / 12.00 |
| buildup | 2024-04-09 to 2024-06-19 | 71 | **6.49** | 6.99 | 0.68 | 5.54 / 8.53 |
| consolidation | 2024-06-20 to 2026-03-19 | 627 | **6.63** | 7.48 | 1.07 | 5.22 / 10.73 |
| afbouw | 2026-03-20 to 2026-06-05 | 69 | **6.76** | 7.38 | 1.03 | 5.32 / 9.64 |

The two **transition phases** (buildup n=71; afbouw n=69) have **n<75 each**; the two **steady-state phases** (unmedicated n=572; consolidation n=627) are an order of magnitude larger. Any HA test that wants per-phase verdicts on this channel faces a ~10x n disadvantage vs the steady-state phases (same as sister channels Q3.1.c / Q3.2.c / Q3.3.c).

Named counts (CONVENTIONS section 3.6): the per-phase n's above are `stress_stdev_sleep`-non-NaN day rows in `per_day_master.csv` within Stratum 4 date masks per `citalopram_phase_stratification.md section 3` boundary dates.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (citalopram-phase violins).

---

## Q3.4.d -- Phase-stratified distribution + v3 dose-modulation OPEN question (caveat-class)

**Per CONVENTIONS section 4.2 (caveats yes; a-priori claims no) + handoff section 1 + section 2.4**: `stress_stdev_sleep` is **NOT in v3 multi-channel sweep scope** per [`citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.6 (the v3 sweep covered 6 baseline channels: `stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`, `resting_hr`, `bb_overnight_gain`, `respiration_avg_sleep`). The citalopram-dose-modulation status on `stress_stdev_sleep` is therefore **OPEN**. This Q3.4.d reports the observed median + dispersion shift across the citalopram-axis phases descriptively; it does **NOT pre-commit a CONFIRMED/REJECTED verdict** on dose-modulation candidacy -- that decision belongs in a future v3 extension that explicitly tests this channel.

Observed median shifts:

| comparison | delta median | within-phase MAD | within-MAD? |
|---|---:|---:|---|
| buildup minus unmedicated | **-1.61** | 0.68-1.59 | >1 MAD; descriptively meaningful |
| consolidation minus unmedicated | **-1.47** | 1.07 | >1 MAD; descriptively meaningful |
| consolidation minus buildup | **+0.13** | 1.07 | |
| afbouw minus consolidation | **+0.13** | 1.07-1.03 | |
| afbouw minus unmedicated | **-1.34** | 1.59-1.03 | |

### Descriptive reading (no verdict promotion)

The median descends from unmedicated (8.10) to consolidation (6.63) by **-1.47** units (0.92 unmedicated-MADs). The day-resolved citalopram boundary step (30d pre/post 2024-04-09): **+0.23 units** -- the empirical day-resolved citalopram-onset shift. Per the framing above: **the observed shift descriptively suggests candidacy for a future v3 extension to add stress_stdev_sleep as a 7th candidate channel**, but no verdict is pre-committed here. A future v3 extension run on this channel would (i) apply the three-pronged test pattern (buildup post-CPAP beta + afbouw beta + spring 2025 control) per `citalopram_dose_response_stress_mean_sleep.md` section 5.6.1; (ii) decide CONFIRMED/REJECTED per the four discipline rules in section 5.6.1; (iii) update the framework MD's per-channel inheritance table at section 4 of `citalopram_phase_stratification.md`.

### Substantive contrast with sister mean's flat-phase-medians pattern

Per [sister `stress_mean_sleep` Q3.1.d](../stress_mean_sleep/findings.md): the mean sibling shows **nearly flat phase medians** (range 17.04 -> 20.20 across the four phases; consolidation-minus-unmedicated = -0.44, within MAD), with the citalopram dose-response effect being a within-buildup-window slope NOT a between-phase level shift. **stress_stdev_sleep shows a substantively larger between-phase shift (consolidation-minus-unmedicated = -1.47)**. The observation is reported descriptively; the substantive interpretation (does this reflect citalopram dose-modulation? Trajectory drift? Sleep-architecture confound per HA07d caveat section 8?) belongs to a future v3 extension.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) and [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d rolling median through phases).

---

## Q3.4.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)

**Per handoff section 2.4**: this Q3.4.e rigorously checks near-identity vs `stress_mean_sleep` (the obvious candidate -- both summarise the same nightly monitoring_b stress sample set; sigma and mean of the same series MAY be near-identical via heteroskedasticity OR may be substantively independent). The **HA07d both-eras-SUPPORTED + HA07c train-only-SUPPORTED divergence** at the test level suggests substantive independence; the descriptive rho at day-level confirms or refutes.

| target channel | n | Pearson r | Spearman rho | near-identity flag? |
|---|---:|---:|---:|---|
| `stress_mean_sleep` | 1339 | +0.602 | +0.501 | no |
| `all_day_stress_avg` | 1339 | +0.309 | +0.266 | no |
| `stress_low_motion_min_count_S60_Mlow` | 1339 | +0.204 | +0.194 | no |
| `asleep_stress_avg_uds` | 1337 | +0.387 | +0.246 | no |
| `awake_stress_avg` | 1339 | +0.186 | +0.208 | no |
| `awake_stress_max` | 1339 | +0.042 | +0.064 | no |
| `all_day_stress_max` | 1339 | +0.046 | +0.066 | no |
| `resting_hr` | 1337 | +0.121 | +0.073 | no |
| `bb_lowest` | 1339 | -0.409 | -0.381 | no |
| `bb_overnight_gain` | 593 | -0.305 | -0.216 | no |

**Zero near-identity pairs fire** at the |rho|>=0.92 CONVENTIONS section 3.3 threshold.

### Substantive-independence reading vs mean sibling (load-bearing per handoff section 2.4)

`stress_stdev_sleep` vs `stress_mean_sleep`: Pearson r=+0.602 / Spearman rho=+0.501 (n=1339). **Reciprocal check confirms sister stress_mean_sleep Q3.1.e's reported rho** (Q3.1.e reported Pearson r=+0.602 / Spearman rho=+0.501 with this channel). The pair is **substantively independent** at the section 3.3 threshold (max(|r|, |rho|) = 0.602 < 0.92). The HA07d both-eras-SUPPORTED + HA07c train-only-SUPPORTED divergence at the test level is descriptively consistent with this substantive-independence reading: variability and mean of the same nightly stress series carry **distinct day-level information**, and the test-level divergence reflects substantive independence of the second-order construct from the first-order mean.

### Crash-subset rho check vs mean sibling (supplementary per handoff section 2.4)

On the crash-day subset (n=101) vs the normal-day subset (n=1238):

| subset | Pearson r vs `stress_mean_sleep` | Spearman rho vs `stress_mean_sleep` |
|---|---:|---:|
| crash days only | +0.639 | +0.740 |
| normal days only | +0.600 | +0.468 |

If `|rho_crash| << |rho_normal|`, the variability primitive carries crash-distinct information that the mean does not. Observed: crash-subset rho=+0.740, normal-subset rho=+0.468 -- the descriptive pattern is NOT showing strong crash-subset divergence. Layer 1 observation; substantive interpretation belongs in a downstream HA pre-reg.

---

## Q3.4.f -- Crash-day vs normal-day (Stratum 4) + HA07d corroboration

Per CONVENTIONS section 3.6 named counts: 29 crash-episodes (crash_v2 episode-level via `labels_crash_v2.csv` unique `episode_id` starting with `crash-`); 101 crash-days (day-level, `label=='crash'`); 1238 non-crash days (the complement within Stratum 4 channel-valid days).

### Episode-level (primary unit per CONVENTIONS section 3.6)

| stat | value |
|---|---:|
| n crash-episodes | 29 |
| n normal-day base rate | 1238 |
| mean per-episode `stress_stdev_sleep` | 9.002 |
| mean normal-day `stress_stdev_sleep` | 7.768 |
| mean diff (episode minus normal-day) | **+1.234** |
| Cohen's d (episode-level vs normal-day pooled) | **+0.48** |
| Bootstrap 95% CI on mean diff | **[+0.315, +2.155]** (5000 iters, seed=20260624) |

**Episode-level Cohen's d=+0.48** on this channel. Compare cross-channel: `stress_mean_sleep` episode d=+0.91 (sister mean); `all_day_stress_avg` episode d=+0.37 with CI brushing zero; `stress_low_motion_min_count_S60_Mlow` episode d=+0.38.

### Day-level (autocorrelation-inflated supplementary)

| stat | value |
|---|---:|
| n crash-days | 101 |
| n normal-days | 1238 |
| mean crash-day | 9.305 |
| mean normal-day | 7.768 |
| median crash-day | 8.64 |
| median normal-day | 7.04 |
| mean diff (point estimate) | **+1.537** |
| median diff | **+1.61** |
| Cohen's d | **+0.58** |
| Mann-Whitney U: z | **+4.69** |
| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **<0.0001** |
| Mann-Whitney U: P(crash > normal) | **+0.640** |
| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (project default) | [+0.583, +2.438], width 1.855 |
| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (data-driven, Q3.4.b flag) | **[+0.583, +2.438]**, width 1.855 |

### HA07d both-eras-SUPPORTED + R14 single-pool SUPPORTED cross-reference (load-bearing per handoff section 2.4)

HA07d is the **only canonical both-eras-SUPPORTED test in the project** (train +19.6 pp / validate +21.7 pp / OVERALL SUPPORTED per [HA07d-sleep-stress-variability/result.md](../../../analyses/hypotheses/HA07d-sleep-stress-variability/result.md)). R14 single_pool_reanchor confirmed at single-pool **+19.7 pp** [CI95 [-18.1, 17.0]] **perm p (E[L]=7) = 0.0291** -- the **only HA that retained SUPPORTED at single-pool** in the R14 cross-check (per [single_pool_reanchor/findings.md](../single_pool_reanchor/findings.md) row HA07d).

**This analysis's first-order day-level Q3.4.f read** (episode-level d=+0.48; CI [+0.315, +2.155]) **descriptively corroborates the HA07d second-order signal at the coarse channel-distribution level**. NOTE: HA07d's tested operand is the per-4-day MAX |z| of NIGHT-OVER-NIGHT DELTA of `stress_stdev_sleep` (a within-4-day spike-form construct on the channel); this Q3.4.f is on the raw daily channel value (first-order, day-level), which is a coarser descriptive complement rather than a re-anchoring of the HA07d operand. HA07d's tested operand discriminates crash-precursor windows at +19.6/+21.7/+19.7 pp; the first-order day-level d here is the descriptive substrate that the HA07d-level signal is built on. The HA07d locked verdicts + the R14 single-pool verdict are LOCKED; this Q3.4.f descriptive observation is NOT a re-interpretation of either.

### Block-length sensitivity (Q3.4.b cross-check)

Per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md), when the data-driven E[L]\* deviates from the project default by more than a factor of 2, the analysis must report the CI at the data-driven value alongside the default. E[L]=7 CI ([+0.583, +2.438]) vs E[L]=7 CI ([+0.583, +2.438]) -- 0.0% narrower at the data-driven block length.

### Crash-drop sensitivity (CONVENTIONS section 3.4)

| frame | Spearman rho | n |
|---|---:|---:|
| full Stratum 4 | -0.121 | 1339 |
| crash-days dropped | -0.072 | 1238 |
| \|delta\| | **0.049** | -- |
| section 3.4 threshold (0.10) crossed? | **no** | -- |

See [`plots/fig4_crash_vs_normal.png`](plots/fig4_crash_vs_normal.png).

---

## Q3.4.g -- Spike-detecting primitive availability

`stress_stdev_sleep` is **structurally a per-night SECOND-ORDER summary**: per-night STDEV of the monitoring_b stress samples within the sleep window per [`garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`](../../../../garmin/scripts/sleep_stress_extract/extract_sleep_stress.py); MIN_SAMPLES_PER_NIGHT=120 gate (~6h at 3-min cadence). Sub-night resolution is NOT in `per_day_master.csv`. Per CONVENTIONS section 3.5 + HA07d result.md framing: this channel IS the second-order autonomic-flexibility primitive on the nightly stress series (the 'HRV-of-HRV-proxy' construct). HA07d's tested operand is the per-4-day MAX |z| of night-over-night delta -- that IS the spike-form construct on this channel at the 4-day-window resolution.

Related stress primitives in the master:

| column | type | relation to `stress_stdev_sleep` |
|---|---|---|
| `stress_mean_sleep` | per-night MEAN of same nightly sample set (mean sibling) | Pearson r=**+0.60** / rho=+0.50; substantive-independence pair per Q3.4.e |
| `all_day_stress_max` | 24h MAX (extremum form, all-day) | Pearson r=**+0.05** / rho=+0.07 |
| `awake_stress_max` | 24h MAX during awake window | Pearson r=**+0.04** / rho=+0.06 |
| `stress_low_motion_min_count_S60_Mlow` | per-minute count of low-motion-high-stress minutes (24h) | Pearson r=**+0.20** / rho=+0.19; spike-form companion in 24h-window |
| `asleep_stress_avg_uds` | UDS-side asleep stress average | Pearson r=**+0.39** / rho=+0.25 |

### CONVENTIONS section 3.5 framing -- the variability primitive IS the second-order spike-form

Unlike the sister mean channel `stress_mean_sleep` which is dilution-vulnerable per CONVENTIONS section 3.5 (24h-mean form prefers spike companions for acute-load mechanisms), **`stress_stdev_sleep` is itself a within-night dispersion primitive**: a single value per sleep-night that measures within-night sample variability. A consumer test whose mechanism is *acute within-night autonomic instability* should use stress_stdev_sleep as primary -- it IS the extremum-form summary on the within-night variability construct. HA07d uses the per-4-day MAX |z| of night-over-night delta to extract a multi-day spike-form construct from this first-order variability metric.

**Latent in FIT, not in master**: per-minute monitoring_b stress samples (the source of this channel) are not exposed in master; finer-than-night resolution (sub-hour stdev) could be computed but is not currently extracted; sleep-stage-stratified stdev (REM vs deep vs disturbed) would require sleep-stage alignment per HA07d caveat section 8 sleep-architecture confound. This analysis does NOT action any of these.

---

## Q3.4.h -- Outlier detection + calibration-drift check

Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md):

- `stress_stdev_sleep` is **custom-extracted from monitoring_b FIT files** per `garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`; MIN_SAMPLES_PER_NIGHT=120 gate (~6h at 3-min cadence). Nights below the gate drop to NaN (`sleep_valid_flag=False`); 33 such nights in Stratum 4.
- **No specific calibration-drift events catalogued for `stress_stdev_sleep`** in `garmin_indicators_audit.md` beyond the shared sleep-stress-extraction family entries (same as sister stress_mean_sleep Q3.1.h).
- Underlying sensor is **Forerunner 245 Elevate V3 throughout the entire 2021-08-16 to present window** -- no device change.
- Per HA07d hypothesis.md section 8 caveat: **sleep architecture confound** -- higher sleep stress variability can reflect more sleep-stage transitions (REM vs deep cycles), not autonomic dysregulation directly. This is a substrate caveat for the channel's biological interpretation, not a calibration-drift signature.

### Outlier scan (MAD-based |z|>5; threshold per CONVENTIONS section 3.1 robust-baseline default)

**14 outlier-day flagged** out of 1339:

| date | value | MAD-z |
|---|---:|---:|
| 2022-12-24 | 19.84 | **+6.64** |
| 2023-02-04 | 24.21 | **+8.91** |
| 2023-07-08 | 18.34 | **+5.86** |
| 2023-08-19 | 23.11 | **+8.34** |
| 2023-09-11 | 20.90 | **+7.19** |
| 2024-07-17 | 19.92 | **+6.68** |
| 2024-08-20 | 24.78 | **+9.21** |
| 2024-12-27 | 20.34 | **+6.90** |
| 2025-01-01 | 17.70 | **+5.53** |
| 2025-01-18 | 22.05 | **+7.79** |
| 2025-02-08 | 18.58 | **+5.98** |
| 2025-07-13 | 18.57 | **+5.98** |
| 2025-09-29 | 19.70 | **+6.57** |
| 2026-03-29 | 17.23 | **+5.28** |

### Drift check -- rolling 90d median over Stratum 4

| snapshot date | rolling 90d median |
|---|---:|
| 2022-12-01 | 7.817 |
| 2023-06-01 | 8.678 |
| 2023-12-01 | 7.952 |
| 2024-06-01 | 6.385 |
| 2025-01-01 | 6.504 |
| 2025-12-01 | 6.632 |
| 2026-04-01 | 7.079 |

Day-resolved boundary steps (30d pre vs post): citalopram 2024-04-09 = **+0.23**, consolidation 2024-06-20 = **+0.75**, afbouw 2026-03-20 = **-0.57**. The rolling 90d median trajectory + boundary steps are descriptively reported; the citalopram-modulation interpretation (Q3.4.d) remains caveat-class per CONVENTIONS section 4.2.

See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).

---

## Q3.4.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel

Discipline anchor: [HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) (secondary-logistic-with-covariate pattern; beta disambiguation between primary-signal and a candidate alternative reading). Names **four** candidate covariates a future HA on `stress_stdev_sleep` as predictor should pre-spec.

### 1. `stress_mean_sleep` -- mean sibling of same nightly stress series (substantive-independence covariate)

On Stratum 4 observed (this analysis Q3.4.e): Pearson r=+0.602 / Spearman rho=+0.501 (n=1339).

Variability and mean of the same nightly stress series may share heteroskedasticity-driven covariance. The covariate disambiguates: beta_channel survives -> the stress_stdev_sleep signal carries variability-primitive-specific information beyond shared nightly stress level; beta_channel attenuates -> shared autonomic-load via heteroskedasticity. **Load-bearing for any future HA on this channel**: the HA07d both-eras-SUPPORTED + HA07c train-only-SUPPORTED test-level divergence is descriptively consistent with this independence reading, but a per-HA secondary check is the canonical disambiguation.

### 2. `dose_plasma_mg(d)` -- citalopram covariate (status OPEN; diagnostic-only)

Channel is **NOT in v3 multi-channel sweep scope** per `citalopram_dose_response_stress_mean_sleep.md` section 5.6. Citalopram-dose-modulation status is OPEN per Q3.4.d caveat-class framing. A future HA cross-phase should pre-spec dose as a secondary covariate to surface any latent dose-modulation; if beta_dose is significant in the secondary, that is evidence for a future v3 extension to add this channel as a 7th candidate. Until v3 covers this channel, neither `citalopram_phase_stratification.md` section 5.A nor section 5.B treatment is OBLIGATORY (unlike the 3 CONFIRMED channels) -- the dose covariate is a diagnostic, not a framework requirement.

### 3. `resting_hr` -- alternative autonomic-load anchor

On Stratum 4 observed (this analysis): Pearson r=+0.121 / Spearman rho=+0.073 (n=1337).

Per HA07d result.md the channel is framed as 'HRV-of-HRV-proxy' (second-order autonomic-flexibility signal). The covariate disambiguates: beta_channel attenuates -> shared autonomic-arousal carried by resting HR; beta_channel survives -> HRV-proxy-variability-specific beyond the resting-HR axis.

### 4. Own-lagged trailing mean -- autocorrelation-vs-mechanism (HA-P7 section 4.5.4)

Per Q3.4.b the cutoff lag M=1 and E[L]\*=7.0. A consumer HA can compute `stress_stdev_sleep_lagged_mean_Nd(d)` at N tuned to E[L]\*=7 with margin. NOTE: this channel does **NOT** have a materialised `_lagged_lcera_z` variant in `per_day_master` (sister channels stress_mean_sleep + all_day_stress_avg + resting_hr + bb_lowest + bb_overnight_gain do, per CONVENTIONS section 3.2). HA author must compute the covariate at runtime.

### Recommendation for any future HA pre-reg on this channel

Pre-spec all four covariates as **secondary sensitivity arms**. Concordance across the four secondaries = high confidence in the primary; divergence = the disambiguation is doing real work. Covariate 1 (mean sibling) is the **load-bearing substantive-independence check**; covariate 2 (dose) is **diagnostic-only** at this time per the channel's NOT-in-v3-scope status; covariate 3 (resting_hr) is the cross-channel autonomic-state disambiguator; covariate 4 (autocorrelation) operationalises HA-P7 section 4.5.4 on this specific channel.

---

## Cross-references

### HA-* tests that touch this channel (cite this analysis)

- **HA07d** (sleep-stress variability delta as crash precursor; LOCKED OVERALL-SUPPORTED -- the ONLY canonical both-eras-SUPPORTED test in the project per [`analyses/hypotheses/HA07d-sleep-stress-variability/result.md`](../../../analyses/hypotheses/HA07d-sleep-stress-variability/result.md); R14 single-pool SUPPORTED at +19.7 pp p=0.0291). This Q3.4 is the Strand-A backstop on the primary operand. The descriptive substrate (E[L]\*=7.0 + phase-stratified trajectory + episode-level d=+0.48) **descriptively corroborates** the locked HA07d signal at the channel-distribution level. The substantive HA07d verdict + R14 single-pool verdict are LOCKED; this analysis's descriptive observations are NOT a re-interpretation or extension.
- **HA07d threshold-monotonicity diagnostic** (LOCKED; downstream of HA07d): inherits the channel; this Q3.4 provides the descriptive substrate that the diagnostic test consumes.
- **HA07c** (sleep-stress MEAN delta; LOCKED TRAIN SUPPORTED / VALIDATE REFUTED / OVERALL REFUTED; channel `stress_mean_sleep`): mean sibling of this channel. The HA07d both-eras-SUPPORTED + HA07c train-only-SUPPORTED divergence is **substantively reflected in the Q3.4.e rho=<sister> reading** (NOT near-identity -- variability and mean carry distinct day-level information).
- **HA08c** (sleep-stress SLOPE; LOCKED TRAIN SUPPORTED / VALIDATE REFUTED / OVERALL REFUTED; channel `stress_mean_sleep`): slope-of-mean sibling. Inherits Q3.4.b autocorrelation finding via the mean sibling's E[L]\*=12.6; the channel-difference autocorrelation is reported here.

### Methodology MDs cited

- [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) -- Q3.4.a delegate target (partial; extended for full skewness/kurtosis/heavy-tail-flag set on this channel).
- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) sections 3-6 -- Q3.4.c phase axis; Q3.4.d phase-stratified is caveat-class per CONVENTIONS section 4.2 since channel NOT in v3 scope.
- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) v3 section 5.6 -- v3 multi-channel sweep scope (6 channels; this channel NOT in scope; Q3.4.d framing).
- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) -- E[L]=7 default + factor-of-2 deviation rule; Q3.4.b reports E[L]\*=7.0 (flag does not fire).
- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) -- Q3.4.h cross-reference; sleep-stress family entries.
- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) -- Stratum 4 boundary definition.
- [`methodology/_descriptive_stocktake_2026-06-23.md`](../../../methodology/_descriptive_stocktake_2026-06-23.md) section 3 + section 5 -- gap-list framing (HA07d Shared gap 1 A3 block-length + A2 missingness + A1 per-cell n now BACKSTOPPED by this analysis).

### Existing artefacts referenced

- [`descriptive/operationalisation_support/stress_mean_sleep/findings.md`](../stress_mean_sleep/findings.md) -- mean sibling of same nightly stress series; closest sister precedent; Q3.1.e reciprocal rho check cross-referenced in Q3.4.e.
- [`descriptive/operationalisation_support/all_day_stress_avg/findings.md`](../all_day_stress_avg/findings.md) -- Q3.2 precedent (CONFIRMED-citalopram channel; programmatic-emit pattern).
- [`descriptive/operationalisation_support/bb_lowest/findings.md`](../bb_lowest/findings.md) -- Q3.3 most-recent Strand-A precedent; cross-channel E[L]\* spread comparison in Q3.4.b.
- [`descriptive/operationalisation_support/stress_low_motion_min_count_S60_Mlow/findings.md`](../stress_low_motion_min_count_S60_Mlow/findings.md) -- spike-form companion (24h-window); E[L]\*=21.1 cross-reference in Q3.4.b.
- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) -- R14 cross-check (LANDED `badd04a`); the HA07d row (+19.7 pp p=0.0291) descriptively corroborated in Q3.4.f.
- [`analyses/hypotheses/HA07d-sleep-stress-variability/result.md`](../../../analyses/hypotheses/HA07d-sleep-stress-variability/result.md) -- LOCKED OVERALL-SUPPORTED; the project's only canonical both-eras-SUPPORTED test.
- [`analyses/hypotheses/HA07c-sleep-stress-mean-delta/result.md`](../../../analyses/hypotheses/HA07c-sleep-stress-mean-delta/result.md) -- LOCKED TRAIN SUPPORTED / VALIDATE REFUTED / OVERALL REFUTED; substantive-independence vs HA07d cross-referenced in Q3.4.e.
- [`analyses/garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) -- Q3.4.e cross-reference; this analysis reciprocally confirms the rho with sister stress_mean_sleep + characterises the new variability-primitive entry into the cluster map.

### Upstream pipeline

- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `processed/garmin/sleep_stress_nightly.csv` <- `garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`.
- `labels_crash_v2.csv` <- `garmin/hypotheses/crash_v2-definition/definition.md` (locked).

---

## Limitations

For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding limitations a downstream HA pre-reg author should carry forward are:

1. **Q3.4.d is caveat-class per CONVENTIONS section 4.2.** The channel is NOT in v3 multi-channel sweep scope; citalopram-dose-modulation status is OPEN; no CONFIRMED/REJECTED verdict is pre-committed here. A future v3 extension that adds this channel must apply the three-pronged test pattern (buildup post-CPAP beta + afbouw beta + spring 2025 control) per `citalopram_dose_response_stress_mean_sleep.md` section 5.6.1.
2. **The channel IS the second-order variability primitive per CONVENTIONS section 3.5** (Q3.4.g). HA07d's tested operand is the per-4-day MAX |z| of night-over-night delta (the second-order spike-form construct on this first-order variability metric). A consumer test whose mechanism is *acute within-night autonomic instability* should use stress_stdev_sleep directly; mechanisms operating at multi-day or weekly resolution should consider whether the HA07d-style second-order construct or a different per-4-day primitive is more apt.
3. **The episode-level Cohen's d=+0.48 CI is [+0.315, +2.155]** (Q3.4.f). The episode-level is the unit-of-analysis-clean read per CONVENTIONS section 3.6; consumer HAs using this channel as a crash-discriminator should NOT rely on the day-level (autocorrelation-inflated) as the primary read.
4. **Block-length sensitivity matters** (Q3.4.b E[L]\*=7.0 vs default 7). Future HAs (beyond HA07d's locked operand which used E[L]=7) should pre-spec the E[L]\*~7 sensitivity arm alongside the default-E[L]=7 primary. HA07d's already-locked verdict is NOT re-anchored.
5. **Mean sibling near-identity Q3.4.e is descriptive only.** Substantive-independence reading vs `stress_mean_sleep` is consistent with the HA07d/HA07c test-level divergence, but a per-HA secondary-with-mean-as-covariate is the canonical disambiguation; this analysis does NOT pre-commit it.
6. **No `_lagged_lcera_z` variant in master.** Per CONVENTIONS section 3.2 the lagged-baseline infrastructure exists for sister channels (stress_mean_sleep + all_day_stress_avg + resting_hr + bb_lowest + bb_overnight_gain) but NOT for stress_stdev_sleep. A consumer HA using lagged-baseline z-scoring must compute the covariate at runtime (per Q3.4.i covariate 4). Materialising the column is a queued infrastructure task; this analysis does NOT action it.
7. **HA07d's sleep-architecture confound (HA07d hypothesis.md section 8) is inherited.** Higher sleep stress variability can reflect more sleep-stage transitions (REM vs deep cycles), not autonomic dysregulation directly; this is a substrate caveat for the channel's biological interpretation that propagates to any descendant test.
8. **HA07d substantive verdict + R14 single-pool verdict are LOCKED with this analysis descriptively corroborating.** This Q3.4 is the Strand-A backstop on the channel; NO substantive HA verdict promotion per CONVENTIONS section 4.2.

---

## Status

**Current as of 2026-06-05 corpus + 2026-06-24 analysis** (commit context: post-`40c351b` Q3.3 bb_lowest LANDED; Phase 2 "finish the descriptive analysis" Tier 1 user-prioritised batch FINAL CHANNEL of 4; R14 `single_pool_reanchor` first at `badd04a`; `all_day_stress_avg` second at `cf34ab1`; `bb_lowest` third at `40c351b`; **this `stress_stdev_sleep` FOURTH closes Tier 1**). Refresh when:

1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to spin up beyond the HA07d-locked operand.
2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 onward).
3. The Politis-White E[L]\* shifts by another factor of 2 from current 7.0.
4. A v3-extension run on this channel lands and updates the Q3.4.d citalopram-modulation status from OPEN to CONFIRMED/REJECTED.
5. A `stress_stdev_sleep_lagged_lcera_z` materialisation lands in `per_day_master.csv` and updates the Q3.4.i covariate-4 needed-columns entry from RUNTIME to MATERIALISED.
6. HA07d threshold-monotonicity diagnostic v3 or any HA07d-descendant test ships and triggers operationalisation-substrate consumption from this analysis.
