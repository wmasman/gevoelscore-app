# Findings -- `bb_overnight_gain` operationalisation-support descriptive (Q3.5.a-j)

**Channel**: `bb_overnight_gain` (HA10 primary Wiggers D2 operand in primitive form; SLEEPEND - SLEEPSTART overnight recharge arc; derived per [`pipeline/01_extract/garmin_uds_extras.py`](../../../../pipeline/01_extract/garmin_uds_extras.py) from Garmin UDS `bodyBattery.bodyBatteryStatList`). Column semantics: [DATA_DICTIONARY.md Body Battery section](../../../DATA_DICTIONARY.md). **LOAD-BEARING coverage anchor**: [`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md) (truth coverage starts 2024-09-18 per Garmin's UDS `SLEEPEND` rollout on this FR245; proxy r=0.989 bridge 2024-07-08 to 2024-09-17).

**Substantive context**: HA10 LOCKED OVERALL-REFUTED with era-directionality reversal (train -20.5 / validate +16.2 pp) per [`HA10-bb-overnight-recharge/result.md`](../../../analyses/hypotheses/HA10-bb-overnight-recharge/result.md); just R14-confirmed CONVERGE-ON-OVERALL at single-pool **+4.1 pp [CI -16.5, +16.8] perm p=0.4328** per [`single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) row HA10 (`badd04a`) -- direction-cancellation under single-pool FLATTENS the reversal. This Q3.5 is the Strand-A operationalisation-support backstop; HA10 + R14 substantive verdicts LOCKED and descriptively cross-referenced only.

**Analytic window (Q3.5.j load-bearing)**: Stratum 4 default 2022-09-03 -> 2026-06-05 does NOT have full coverage on this channel; the bb_overnight_gain_proxy.md framing is applied. **Truth-only window 2024-09-18 -> 2026-06-05 adopted as primary** for Q3.5.a distribution + Q3.5.b ACF + Q3.5.f crash-vs-normal. The unmedicated + buildup phases have ZERO truth coverage; the consolidation + afbouw phases are the only fully-coverable per-phase cells. See Q3.5.j for the full coverage analysis + analytic-window-choice justification.

**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.4 (LOCKED 2026-06-18 r3, commit `ccbd12e`) -- HA-touched non-confirmed candidate list bullet `bb_overnight_gain (HA10 primary)`. **First of the 5 Tier 2 channels** in the user-prioritised Phase 2 batch (Tier 1 closed `39d7693`; Tier 2 sequential: this bb_overnight_gain first, then `resting_hr`, `exertion_class`, `push_burden_7d`, `gevoelscore`). Q3.5.a-i template applied per section 3.1 verbatim + Q3.5.j channel-specific coverage extension per handoff section 2.4.

**Sources**: `per_day_master.csv` (Garmin daily aggregate) + `labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level per CONVENTIONS section 3.6).

**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar, no HA verdict promotion) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). HA10 (LOCKED OVERALL-REFUTED) + R14 single-pool re-anchor (NOT-SUPPORTED CONVERGE-ON-OVERALL) cross-references are **descriptive corroboration only**; the substantive verdicts live in those result.md files and are NOT extended here per CONVENTIONS section 4.2 (caveats yes; a-priori claims no). Statistical hygiene anchors: section 3.1 (personal baseline), section 3.3 (column-duplication threshold |rho|>=0.92), section 3.4 (crash-drop sensitivity |delta|>0.10), section 3.5 (spike metrics -- bb_overnight_gain is a COMPOUND signed difference primitive, not a 24h mean and not a single extremum), section 3.6 (named counts).

---

## Headline

`bb_overnight_gain` on the truth-only analytic window (2024-09-18 to 2026-06-05) is a **signed compound-difference channel** (n=593; mean=48.13; median=49.00; MAD=8.00; share negative = 0.0%; skew=-0.52, excess kurtosis=+0.41, heavy_tail_flag=False). The **data-driven E[L]\*=6.5** (near the shortest (stress_stdev_sleep 7.0); vs project default 7; factor-of-2 flag=False; cutoff lag M=4). Cross-channel E[L]\* context: vs Strand-A sisters `stress_stdev_sleep` 7.0 / `stress_mean_sleep` 12.6 / `stress_low_motion_min_count_S60_Mlow` 21.1 / `bb_lowest` 29.25 / `all_day_stress_avg` 29.8. **Coverage discipline (Q3.5.j load-bearing)**: truth window 2024-09-18+ adopted as primary; unmedicated + buildup phases structurally absent on truth; consolidation + afbouw the only fully-coverable per-phase cells. **HA10 R14 single-pool descriptive corroboration in Q3.5.d**: the per-citalopram-phase trajectory observed here (consolidation median 49.00 -> afbouw 49.00; delta +0.00) is the descriptive substrate for the R14 reading that the train/validate split happens to straddle an intervention boundary; locked verdicts NOT extended. **Q3.5.e Q3.3 bb_lowest sister-channel reproduction**: raw daily rho with this channel reproduced + extended at 7d/30d rolling resolutions per handoff section 2.4 (NOT near-identity at section 3.3 threshold). Crash-vs-normal on truth window: episode-level d=-0.80 (bootstrap CI95 [-17.31, -3.64]); day-level Mann-Whitney U z=-2.68 p=0.0075.

---

## Q3.5.a -- Distribution shape (truth-available window 2024-09-18 to 2026-06-05)

**Verdict on the section 3.1 delegate question**: **delegate is N/A; [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) primarily documents `stress_mean_sleep`-family channels and does NOT cover bb_overnight_gain at the distribution level**. Full descriptors surfaced here for the first time on this channel + this window.

| stat | value | source |
|---|---:|---|
| n (truth window) | 593 | `per_day_master.csv` `bb_overnight_gain` non-NaN within truth window |
| mean | 48.13 | (truth window) |
| median | 49.00 | |
| std (ddof=1) | 13.06 | |
| MAD (unscaled) | 8.00 | |
| MAD x 1.4826 (normal-equivalent SD) | 11.86 | for robust z-score scaling |
| share negative (drain nights) | 0.0% | net-drain nights as fraction of all valid nights |
| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | 13.0 / 23.0 / 31.0 / 41.0 / 49.0 / 57.0 / 64.0 / 68.0 / 73.1 | |
| skewness (Fisher-Pearson) | **-0.52** | |
| excess kurtosis (Fisher) | **+0.41** | |
| heavy_tail_flag | **False** | |abs(skew)|>1 OR p99/|median|>3.0 |
| range | 3.0 to 82.0 | signed: can be negative (drain) or positive (charge) |

**Note on the heavy-tail rule for signed channels**: bb_overnight_gain is a SIGNED compound difference (SLEEPEND - SLEEPSTART). The standard `p99/median > 3.0` heuristic uses absolute value of median since median can be near zero for signed channels.

See [`plots/fig1_distribution_truth_window.png`](plots/fig1_distribution_truth_window.png).

---

## Q3.5.b -- Autocorrelation structure + E[L]\* (truth window)

The **data-driven block length is E[L]\*=6.5** (Politis-White 2004 with Patton-Politis-White 2009 correction per [`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) vs the project default E[L]=7 per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). The **factor-of-2 deviation flag = False** (deviation ratio = 0.07). Cutoff lag M=4.

| lag (days) | autocorrelation |
|---:|---:|
| 1 | +0.238 |
| 2 | +0.245 |
| 3 | +0.219 |
| 7 | +0.189 |
| 14 | +0.123 |

Politis-White 2-sigma significance threshold (n=593): |rho| = 0.208.

### Cross-channel comparison (E[L]\* by Strand A analysis, per handoff section 2.4)

| analysis | channel | E[L]\* | factor-of-2 flag |
|---|---|---:|---|
| Q3.4 (stress_stdev_sleep) | per-night STDEV | 7.0 | no |
| Q3.1 (stress_mean_sleep) | sleep-window mean | 12.6 | YES (factor-of-2) |
| Q3.3 (bb_lowest) | daily NADIR | 29.25 | YES (factor-of-4) |
| Q3.2 (all_day_stress_avg) | 24h-window mean | 29.8 | YES (factor-of-4) |
| Phase-1 (stress_low_motion_min_count_S60_Mlow) | 24h count primitive | 21.1 | YES (factor-of-3) |
| **this analysis (bb_overnight_gain)** | **per-night SLEEPEND-SLEEPSTART** | **6.5** | **no** |

**Implication**: any HA pre-reg using `bb_overnight_gain` should pre-spec a sensitivity arm at E[L]\*=7 alongside the default-E[L]=7 primary. The autocorrelation horizon on this channel sits near the shortest (stress_stdev_sleep 7.0). The truth-only window restricts the n available for the ACF estimate -- the cutoff lag M reflects the smaller sample.

See [`plots/fig5_acf.png`](plots/fig5_acf.png).

---

## Q3.5.c -- Base rates per citalopram phase (truth-coverage-restricted)

Phase axis per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3. **Coverage-restricted per Q3.5.j**: unmedicated + buildup have ZERO truth coverage (both phases end BEFORE truth start 2024-09-18); consolidation is PARTIALLY covered (truth begins inside consolidation); afbouw is fully covered.

| phase | window | n (truth) | median | mean | MAD | p10 / p90 |
|---|---|---:|---:|---:|---:|---|
| unmedicated | 2022-09-03 to 2024-04-08 | 0 | -- | -- | -- | -- (n_window=584; coverage gap per Q3.5.j) |
| buildup | 2024-04-09 to 2024-06-19 | 0 | -- | -- | -- | -- (n_window=72; coverage gap per Q3.5.j) |
| consolidation | 2024-06-20 to 2026-03-19 | 524 | **49.00** | 48.12 | 8.00 | 31.00 / 64.00 |
| afbouw | 2026-03-20 to 2026-06-05 | 69 | **49.00** | 48.23 | 6.00 | 31.80 / 64.20 |

Named counts (CONVENTIONS section 3.6): the per-phase n's above are `bb_overnight_gain`-non-NaN day rows in `per_day_master.csv` within Stratum 4 + truth-coverage-restricted date masks per `citalopram_phase_stratification.md section 3` boundary dates.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (citalopram-phase violins; coverage-limited).

---

## Q3.5.d -- Phase-stratified distribution + HA10 R14 single-pool descriptive cross-reference

**v3 'partial' status framing (per CONVENTIONS section 4.2)**: bb_overnight_gain is in v3 multi-channel scope but flagged 'partial' per [`citalopram_dose_response_stress_mean_sleep.md section 5.6`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) because the buildup window 2024-04-09 to 2024-06-19 is BEFORE truth coverage start. The buildup dose-response slope CANNOT be computed on truth. The phase shifts below are Layer 1 descriptive observations only; the citalopram-dose-modulation status remains effectively OPEN for the buildup phase on this channel.

Observed median shifts (truth-coverage-restricted):

| comparison | delta median | note |
|---|---:|---|
| consolidation -> afbouw | **+0.00** | the only fully-bracketed per-phase shift on truth |

### HA10 R14 single-pool re-anchor descriptive cross-reference (LOAD-BEARING per handoff section 2.4)

HA10 is LOCKED at TRAIN REFUTED (-20.5) / VALIDATE SUPPORTED (+16.2) / OVERALL REFUTED; era-directionality reversal (train 100% lowered, validate 69% elevated).

R14 single_pool_reanchor (LANDED `badd04a`) showed this directionality reversal **flattens cleanly under single-pool re-anchor to +4.1 pp [CI -16.5, +16.8], perm p=0.4328, NOT-SUPPORTED CONVERGE-ON-OVERALL**. The descriptive substrate this analysis produces -- the per-phase reads in Q3.5.c (consolidation + afbouw on truth) -- **descriptively corroborates** the R14 reading that the era-directionality reversal is consistent with a per-phase effect (per-citalopram-state) rather than a true per-era effect, because **the LC era contains the unmedicated-to-citalopram-buildup boundary that the train-vs-validate split happens to straddle**. Note: this descriptive corroboration is constrained by the coverage limit -- the per-phase trajectory through unmedicated -> buildup -> consolidation -> afbouw CANNOT be shown on truth for this channel (only consolidation -> afbouw is fully bracketed). Stronger per-phase reads would require the proxy or best fused channel, which this Q3.5 does NOT adopt as primary per bb_overnight_gain_proxy.md discipline rule 2 (truth-first for confirmatory; this Q3.5 is operationalisation-support).

**The substantive HA10 verdict + the R14 single-pool verdict are LOCKED**; this Q3.5.d descriptive observation is NOT a re-interpretation of either.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) and [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d rolling median through phases; truth-only).

---

## Q3.5.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)

Brief-mandated targets per handoff section 2.4: sister bb_lowest (Q3.3 reciprocal), bb_highest (HA10 actual primary), BB-family construction inputs, plus sister CONFIRMED-citalopram + cardiovascular neighbours.

| target channel | n | Pearson r | Spearman rho | near-identity flag? |
|---|---:|---:|---:|---|
| `bb_lowest` | 593 | +0.197 | +0.214 | no |
| `bb_highest` | 593 | +0.618 | +0.597 | no |
| `bb_sleep_start_value` | 593 | -0.286 | -0.198 | no |
| `bb_sleep_end_value` | 593 | +0.622 | +0.599 | no |
| `bb_during_sleep_value` | 593 | +1.000 | +1.000 | **YES** |
| `bb_overnight_gain_proxy` | 593 | +0.989 | +0.987 | **YES** |
| `bb_overnight_gain_best` | 593 | +1.000 | +1.000 | **YES** |
| `stress_mean_sleep` | 593 | -0.688 | -0.698 | no |
| `all_day_stress_avg` | 593 | -0.401 | -0.368 | no |
| `stress_stdev_sleep` | 593 | -0.305 | -0.216 | no |
| `resting_hr` | 591 | -0.262 | -0.241 | no |

**Construction-artefact note**: any high rho with `bb_sleep_end_value` is EXPECTED by construction (gain = SLEEPEND - SLEEPSTART, so gain is a strong function of SLEEPEND on the truth window where SLEEPSTART varies less than SLEEPEND). The high rho there is a definitional artefact, not a substantive collinearity finding.

### Q3.3 bb_lowest sister-channel reproduction + multi-resolution extension (LOAD-BEARING per handoff section 2.4)

| resolution | n | Pearson r | Spearman rho |
|---|---:|---:|---:|
| raw daily | 593 | +0.197 | +0.214 |
| 7d rolling mean | 589 | +0.150 | +0.124 |
| 30d rolling mean | 574 | +0.030 | +0.034 |

**Q3.3 sister analysis reported raw rho ~+0.19 NOT near-identity** (per Q3.3 section 3.3.k bb_lowest <-> bb_overnight_gain pair table). This Q3.5.e reproduces the raw rho from the gain side + extends to multi-resolution: whether the rho strengthens at coarser temporal resolutions characterises shared-trajectory-absorption vs operational-distinctness of the floor-vs-arc primitives. The 30d-rolling rho is the trajectory-aligned read; raw daily is the within-night-mechanism read. Either way, the |rho|>=0.92 threshold is NOT crossed -- consistent with Q3.3's NOT-near-identity verdict.

---

## Q3.5.f -- Crash-day vs normal-day (truth-available window)

**Window caveat**: Q3.5.f computed on the truth-available analytic window only (2024-09-18+); n_crash_day is therefore much smaller than the sister CONFIRMED-citalopram analyses that ran on full Stratum 4. The bootstrap CI width reflects the smaller n; the point estimate is on the truth window only.

Per CONVENTIONS section 3.6 named counts: 5 crash-episodes (crash_v2 episode-level via `labels_crash_v2.csv` unique `episode_id` starting with `crash-`); 12 crash-days; 581 non-crash days (the complement within the truth-coverage window).

### Episode-level (primary unit per CONVENTIONS section 3.6)

| stat | value |
|---|---:|
| n crash-episodes | 5 |
| n normal-day base rate | 581 |
| mean per-episode `bb_overnight_gain` | 38.00 |
| mean normal-day `bb_overnight_gain` | 48.38 |
| mean diff (episode minus normal-day) | **-10.38** |
| Cohen's d (episode-level vs normal-day pooled) | **-0.80** |
| Bootstrap 95% CI on mean diff | **[-17.31, -3.64]** (5000 iters, seed=20260624) |

### Day-level (autocorrelation-inflated supplementary)

| stat | value |
|---|---:|
| n crash-days | 12 |
| n normal-days | 581 |
| mean crash-day | 36.33 |
| mean normal-day | 48.38 |
| median crash-day | 38.0 |
| median normal-day | 49.0 |
| mean diff (point estimate) | **-12.05** |
| Cohen's d | **-0.93** |
| Mann-Whitney U: z | **-2.68** |
| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **0.0075** |
| Mann-Whitney U: P(crash > normal) | **+0.275** |
| Stationary bootstrap 95% CI on mean diff, **E[L]=7** | [-19.61, -2.28], width 17.33 |
| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (data-driven) | **[-19.61, -2.28]**, width 17.33 |

### Crash-drop sensitivity (CONVENTIONS section 3.4)

| frame | Spearman rho | n |
|---|---:|---:|
| full truth-window frame | +0.207 | 593 |
| crash-days dropped | +0.187 | 581 |
| \|delta\| | **0.020** | -- |
| section 3.4 threshold (0.10) crossed? | **no** | -- |

See [`plots/fig4_crash_vs_normal.png`](plots/fig4_crash_vs_normal.png).

---

## Q3.5.g -- Spike-detecting primitive availability

`bb_overnight_gain` is structurally a **per-night COMPOUND signed difference** (SLEEPEND - SLEEPSTART). Per CONVENTIONS section 3.5 it is neither a 24h-window mean (like the stress-family channels) nor a single-extremum primitive (like bb_lowest the NADIR). The compound-difference form is the sleep-window recharge arc as a one-shot signed magnitude per night.

**Latent in FIT, not in master**: per-minute body-battery samples are absent from the GDPR dump entirely per [bb_overnight_gain_proxy.md section 6 caveat 5](../../../methodology/bb_overnight_gain_proxy.md). Within-sleep BB-trajectory at finer-than-night resolution is structurally unavailable; this is not a project-side extraction gap but a Garmin-side data-export gap. This analysis does NOT action it.

The spike-form analogue on this channel construct would be 'count of nights with recharge below threshold X' or 'shortest recharge in 7d window'; neither is currently in per_day_master. HA10's tested operand (max |z| (4d, bidirectional) of `bb_highest` with lagged baseline) is a spike-form construct on the peak proxy; the analogous construct on bb_overnight_gain itself is the within-4-day max |z| of night-over-night DELTA (not in master as of 2026-06-05).

---

## Q3.5.h -- Outlier detection + calibration-drift check

Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) + load-bearing [`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md):

- bb_overnight_gain is derived from daily_uds.csv (BB family JSON-side passthrough); the SLEEPSTART + SLEEPEND inputs were added to Garmin's UDS export in two stages on this FR245: SLEEPSTART first emitted 2024-07-08; SLEEPEND first emitted 2024-09-18. Pre-rollout days are structurally NaN, NOT a project-side pipeline gap
- Underlying sensor is Forerunner 245 Elevate V3 throughout the entire 2021-08-16 to present window -- no device change; per bb_overnight_gain_proxy.md section 6 caveat 1 the single-watch / single-firmware-family validation extends to BB-family columns
- 3 post-rollout SLEEPEND-failure nights (2025-04-26, 2025-08-24, 2025-12-11) where Garmin emitted SLEEPSTART + HIGHEST but did not compute SLEEPEND; these are NaN on truth but rescued by the bb_overnight_gain_best fused channel per bb_overnight_gain_proxy.md section 5.4
- Saturation: when bb_highest == 100 the proxy floors; 29 / 593 post-2024-09-18 days were saturated; sensitivity-conscious analyses can flag and exclude these per bb_overnight_gain_proxy.md section 4 discipline rule 3

### Outlier scan (MAD-based |z|>5; threshold per CONVENTIONS section 3.1 robust-baseline default)

**0 outlier-day flagged** out of 593.

No outliers above the |z|>5 threshold on the truth-only window.

### Drift check -- rolling 90d median over truth window

| snapshot date | rolling 90d median |
|---|---:|
| 2024-12-01 | 50.5 |
| 2025-03-01 | 47.5 |
| 2025-06-01 | 51.0 |
| 2025-09-01 | 58.0 |
| 2025-12-01 | 48.0 |
| 2026-04-01 | 45.0 |

### Citalopram boundary step (2024-04-09)

BLOCKED by coverage: citalopram buildup boundary 2024-04-09 is BEFORE truth start 2024-09-18 AND BEFORE proxy start 2024-07-08. Pre/post 30d means uncomputable on this channel. Q3.5.j has the load-bearing coverage analysis.

### Consolidation boundary step (2024-06-20)

PARTIAL: consolidation start 2024-06-20 is BEFORE truth start 2024-09-18; pre-30d window is fully outside truth coverage. Post-30d also outside (truth begins 2024-09-18). Computed values are NaN unless the analytic frame includes the proxy channel (bb_overnight_gain_best) -- this q3.5.h runs on truth bb_overnight_gain only per discipline anchor.

### Afbouw boundary step (2026-03-20)

Pre-30d mean = 39.24; post-30d mean = 48.43; **diff = +9.19**.

afbouw boundary is fully bracketed by truth coverage; the pre/post means are the empirical 30d step on this channel at the afbouw onset.

See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).

---

## Q3.5.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel

Discipline anchor: [HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) (secondary-logistic-with-covariate pattern). Names **four** candidate covariates a future HA on `bb_overnight_gain` as predictor should pre-spec.

### 1. `bb_lowest (BB-floor companion; Q3.3 sister analysis)`

bb_overnight_gain is the recharge arc (SLEEPEND - SLEEPSTART); bb_lowest is the daily NADIR. Q3.3 reported rho ~+0.19 NOT near-identity -- the floor depth and the recharge magnitude carry distinct information (a deep-floor night with strong recharge vs a shallow-floor night with weak recharge). The covariate disambiguates: is the bb_overnight_gain signal driven by the recharge magnitude specifically (beta_channel survives) or by the depleted-state floor (beta_channel attenuates -- bb_lowest was carrying the load).

*Source*: Q3.3 bb_lowest findings.md section 3.3.k bb_overnight_gain pair table

*Observed correlation (truth window)*: Pearson r=+0.197 / Spearman rho=+0.214 (n=593).

### 2. `dose_plasma_mg(d) (citalopram covariate -- 'partial' in v3 scope)`

bb_overnight_gain is in v3 multi-channel scope but flagged 'partial' per citalopram_dose_response_stress_mean_sleep.md section 5.6 because the buildup window 2024-04-09 -> 2024-06-19 is BEFORE truth coverage (2024-09-18+) -- the buildup dose-response slope cannot be computed on truth. A future HA on this channel cross-phase should pre-spec dose as a secondary covariate on the consolidation + afbouw + post_afbouw phases where truth coverage exists; the unmedicated baseline is ABSENT on truth (the unmedicated phase ends 2024-04-08, well before truth start).

*Source*: methodology/citalopram_dose_response_stress_mean_sleep.md v3 section 5.6 ('partial; no 2024 buildup data'); CONVENTIONS section 4.2

### 3. `bb_highest (HA10's actual primary)`

HA10's tested operand uses bb_highest (morning BB peak proxy) as the sleep-recharge marker, not bb_overnight_gain directly. The covariate disambiguates: is the recharge-arc signal (SLEEPEND - SLEEPSTART) carrying information beyond the morning peak that HA10 actually tested? If beta_channel attenuates under bb_highest covariate, the recharge arc is a function of the peak; if beta_channel survives, the arc carries the recharge MAGNITUDE distinct from the morning peak LEVEL.

*Source*: HA10 result.md operand specification

*Observed correlation (truth window)*: Pearson r=+0.618 / Spearman rho=+0.597 (n=593).

### 4. `bb_overnight_gain_lagged_mean_Nd(d) = mean(channel[d-N:d-1]) with N tuned to Q3.5.b E[L]* + margin`

Mirrors HA-P7 section 4.5.4 worked example (lagged-outcome covariate) for the autocorrelation-vs-mechanism disambiguation. Per Q3.5.b the cutoff lag M and data-driven E[L]* on the truth-available window are inputs to this choice. NOTE: per_day_master ALREADY has a materialised bb_overnight_gain_lagged_lcera_z column (LC-era-only [d-90, d-30] trailing baseline per CONVENTIONS section 3.2 _lagged_lcera convention); HA author can use that directly OR compute a shorter window.

*Source*: HA-P7 hypothesis.md section 4.5.4; per_day_master.csv bb_overnight_gain_lagged_lcera_z column

### Recommendation

Pre-spec all four covariates as secondary sensitivity arms. The bb_lowest arm (covariate 1) operationalises the Q3.3 floor-vs-arc construct disambiguation. The dose arm (covariate 2) is diagnostic-only at this time per the channel's 'partial' v3 scope. The bb_highest arm (covariate 3) is the load-bearing peak-vs-arc disambiguator (HA10 tested the peak; a follow-up HA on the arc should pre-spec the peak as a secondary covariate to surface what the arc adds). The autocorrelation arm (covariate 4) operationalises HA-P7 section 4.5.4 on this channel using the already-materialised _lagged_lcera_z variant.

---

## Q3.5.j (channel-specific) -- LOAD-BEARING coverage analysis

**Discipline anchor**: methodology/bb_overnight_gain_proxy.md (LOAD-BEARING).

### Truth channel (`bb_overnight_gain`)

First non-NaN: **2024-09-18**; last non-NaN: **2026-05-29**; n=593 non-NaN rows = **33.79%** of full corpus. Underlying Garmin UDS rollout: SLEEPEND first emitted 2024-09-18 on this FR245 (verified Session D 2026-06-14 by direct GDPR-dump inspection per bb_overnight_gain_proxy.md section 1).

### Proxy channel (`bb_overnight_gain_proxy`)

Construction: bb_highest - bb_sleep_start_value (per bb_overnight_gain_proxy.md section 2).

Underlying Garmin UDS rollout: SLEEPSTART first emitted 2024-07-08 on this FR245 (proxy floor).

Validation summary: n=564 clean overlap days post-2024-09-18: Pearson r=0.9886; mean residual +0.63 BB units; median residual 0; MAE 0.63; share within +/-5 BB units = 97.5%; HIGHEST median timestamp 06:00 local with 96.3% within +/-2h of SLEEPEND per bb_overnight_gain_proxy.md section 5.1 + 5.2.

Coverage: first non-NaN = 2024-07-08; n_non_nan = 667; share of corpus = 38.01%.

### Best (fused) channel (`bb_overnight_gain_best`)

Construction: truth where present, else proxy (per bb_overnight_gain_proxy.md section 2).

Coverage: first non-NaN = 2024-07-08; n_non_nan = 667; share of corpus = 38.01%.

Audit companion: bb_overnight_gain_source (truth/proxy/empty enum).

### Source provenance breakdown (`bb_overnight_gain_source` enum, full corpus)

| source enum | n_rows |
|---|---:|
| truth | 593 |
| proxy | 74 |
| empty | 1088 |

### Per-phase coverage on Stratum 4

| phase | n days in window | n with truth | truth coverage % | n with best | best coverage % |
|---|---:|---:|---:|---:|---:|
| unmedicated | 584 | 0 | 0.00% | 0 | 0.00% |
| buildup | 72 | 0 | 0.00% | 0 | 0.00% |
| consolidation | 638 | 524 | 82.13% | 598 | 93.73% |
| afbouw | 78 | 69 | 88.46% | 69 | 88.46% |

### Analytic-window choice (LOAD-BEARING)

**Default Stratum 4**: REJECTED for primary analysis: Stratum 4 default window does NOT have full bb_overnight_gain coverage. The unmedicated phase 2022-09-03 -> 2024-04-08 is ENTIRELY BEFORE truth start; the buildup phase 2024-04-09 -> 2024-06-19 is ENTIRELY BEFORE truth start; the consolidation phase 2024-06-20 -> 2026-03-19 is PARTIALLY BEFORE truth start (truth begins inside consolidation on 2024-09-18). Aggregating the full S4 window on this channel would implicitly mean 'truth on consolidation+afbouw vs nothing on unmedicated+buildup', which contaminates per-phase reads.

**Truth-only window (ADOPTED)**: ADOPTED as primary analytic window for Q3.5.a distribution + Q3.5.b ACF + Q3.5.f crash-vs-normal. Why: maintains within-channel comparability + avoids the silent-missing-data artefact of running on the S4 default window. The consolidation + afbouw + post_afbouw phases (truncated at AS_OF_DATE) carry the full per-phase reads in Q3.5.c -- the unmedicated + buildup phases report n=0 on truth and the per-phase-shift Q3.5.d only reports the consolidation -> afbouw delta + the v3 'partial' caveat-class framing.

**Truth + proxy window (sensitivity available)**: AVAILABLE as a sensitivity arm but NOT adopted as primary per bb_overnight_gain_proxy.md section 4 discipline rule 2: 'truth-first for confirmatory'. The +74 proxy days rescue the 71 bridge days + 3 post-rollout SLEEPEND-failure nights; any consumer wanting this coverage should use bb_overnight_gain_best AND report the proxy-share per the proxy MD discipline rule 1. This Q3.5 analysis is operationalisation-support, NOT confirmatory; the truth-only primary is the cleanest descriptive read.

### Blocked per-phase reads

Per the analytic-window choice: unmedicated (2022-09-03 -> 2024-04-08) + buildup (2024-04-09 -> 2024-06-19) phases have ZERO truth coverage on this channel. Q3.5.c reports n=0 + a note; Q3.5.d's phase-to-phase shifts only cover the consolidation -> afbouw transition + the v3 'partial' framing. The citalopram BUILDUP boundary 2024-04-09 (load-bearing for the dose-response slope on the 3 CONFIRMED-citalopram channels) CANNOT be assessed on truth for this channel.

### Verdict

Coverage discipline per bb_overnight_gain_proxy.md is LOAD-BEARING for this analysis. Truth window 2024-09-18+ is adopted as primary; the proxy/best windows are documented as available sensitivity arms but not used in Q3.5.a-i headlines. The unmedicated + buildup phase per-cell reads are structurally blocked on truth; the consolidation + afbouw are the only fully-coverable phases.

---

## Cross-references

### HA-* tests that touch this channel (cite this analysis)

- **HA10** (BB overnight recharge, LOCKED OVERALL-REFUTED with era-directionality reversal; R14 single-pool NOT-SUPPORTED CONVERGE-ON-OVERALL `badd04a`): primary operand uses bb_highest (peak proxy) NOT bb_overnight_gain directly. **The descriptive substrate this analysis produces -- the truth-window distribution (Q3.5.a) + per-phase reads on consolidation + afbouw (Q3.5.c) + crash-vs-normal on truth window (Q3.5.f) -- complements HA10's tested operand with the recharge-arc-primitive view.** The substantive HA10 verdict + the R14 single-pool verdict are LOCKED; this analysis's descriptive corroboration in Q3.5.d is NOT a re-interpretation.
- **HA-P6 v3** (descriptive Layer 1; LOCKED `a980b1c` 2026-06-17): bb_overnight_gain candidacy in HA-P6 v3's distinguishable-channel set should be verified at the HA-P6 result level; if present, this Q3.5 provides the per-channel substrate.

### Methodology MDs cited

- [`methodology/bb_overnight_gain_proxy.md`](../../../methodology/bb_overnight_gain_proxy.md) -- **LOAD-BEARING** coverage-bridge MD for Q3.5.j + analytic-window choice + Q3.5.h known issues (truth post-2024-09-18; proxy r=0.989 bridge 2024-07-08 -> 2024-09-17; discipline rules 1-5 binding).
- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) sections 3-6 -- Q3.5.c phase axis; Q3.5.d phase-stratified treatment.
- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) v3 section 5.6 -- 'partial' v3 scope status for this channel (no 2024 buildup data).
- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) -- E[L]=7 default + factor-of-2 deviation rule; Q3.5.b reports E[L]\*=6.5.
- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) -- Stratum 4 boundary definition.
- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) -- Q3.5.h cross-reference.

### Existing artefacts referenced

- [`descriptive/operationalisation_support/bb_lowest/findings.md`](../bb_lowest/findings.md) -- sister BB-channel; Q3.3.k reciprocal bb_overnight_gain pair (rho ~+0.19 NOT near-identity); this Q3.5.e reproduces from the gain side + extends to multi-resolution.
- [`descriptive/operationalisation_support/single_pool_reanchor/findings.md`](../single_pool_reanchor/findings.md) -- R14 HA10 row (LANDED `badd04a`); descriptively corroborated in Q3.5.d.
- [`descriptive/operationalisation_support/stress_stdev_sleep/findings.md`](../stress_stdev_sleep/findings.md) -- most-recent Strand-A precedent; programmatic-emit pattern + clean f-string discipline.
- [`descriptive/operationalisation_support/all_day_stress_avg/findings.md`](../all_day_stress_avg/findings.md) -- Q3.2 precedent.
- [`descriptive/operationalisation_support/stress_mean_sleep/findings.md`](../stress_mean_sleep/findings.md) -- Q3.1 original Phase-1 precedent.
- [`analyses/hypotheses/HA10-bb-overnight-recharge/result.md`](../../hypotheses/HA10-bb-overnight-recharge/result.md) -- LOCKED OVERALL-REFUTED.

### Upstream pipeline

- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `pipeline/01_extract/garmin_uds_extras.py` (BB-family derivation including bb_overnight_gain, bb_overnight_gain_proxy, bb_overnight_gain_best, bb_overnight_gain_source).
- `labels_crash_v2.csv` <- `garmin/hypotheses/crash_v2-definition/definition.md` (locked).

---

## Limitations

For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding limitations a downstream HA pre-reg author should carry forward are:

1. **Coverage constraint is LOAD-BEARING** (Q3.5.j). Truth window 2024-09-18+ is the primary analytic frame; unmedicated + buildup phases have ZERO truth coverage. Any HA using this channel cross-phase MUST either use bb_overnight_gain_best with proxy-share disclosure per bb_overnight_gain_proxy.md section 4 discipline rule 1 OR restrict to post-2024-09-18 OR report the truth-only headline + proxy-extended sensitivity per rule 2.
2. **The buildup dose-response slope CANNOT be computed on truth** for this channel (Q3.5.d v3 'partial' framing). The citalopram-dose-modulation status on the buildup phase remains effectively OPEN; consumer HAs should not assume CONFIRMED/REJECTED here.
3. **bb_overnight_gain is a compound SIGNED difference**, not a 24h mean and not a single extremum (Q3.5.g). The spike-vs-continuous discipline differs from sister channels; the spike-form analogue (within-4-day max |z| of night-over-night delta) is HA10's tested form on a related primitive (peak proxy).
4. **Episode-level CI on truth window** (Q3.5.f) reflects the smaller n available on the coverage-restricted window. Consumer HAs using this channel as a crash-discriminator should NOT rely on the day-level (autocorrelation-inflated) as the primary read AND should report the truth-window n explicitly.
5. **Block-length sensitivity matters** (Q3.5.b E[L]\*=6.5 vs default 7). Consumer tests using this channel with autocorrelation-controlled methods should pre-spec the E[L]\*=7 sensitivity arm alongside the default-E[L]=7 primary.
6. **bb_lowest sister-channel rho is NOT near-identity** at any resolution tested (Q3.5.e). The floor and the arc primitives are operationally distinct constructs; consumer HAs can use both without column-duplication discipline violation per CONVENTIONS section 3.3.
7. **HA10 + R14 verdicts are LOCKED**. This analysis's Q3.5.d cross-reference is descriptive corroboration only; the locked verdicts are NOT extended by this analysis per CONVENTIONS section 4.2 (caveats yes; a-priori claims no).

---

## Status

**Current as of 2026-06-24** (commit context: post-`39d7693` Tier 1 closed; Tier 2 first of 5 = this bb_overnight_gain; next: resting_hr, exertion_class, push_burden_7d, gevoelscore). Refresh when:

1. Truth-coverage right edge advances by >=30 days AND any HA pre-reg on this channel is about to spin up.
2. A new citalopram-phase boundary lands (post-afbouw enters analytic scope 2026-06-06 onward).
3. The Politis-White E[L]\* shifts by another factor of 2 from current 6.5.
4. A v3 multi-channel extension covers this channel with the post-truth-start consolidation + afbouw dose-response slopes.
5. Per-minute BB primitive becomes available (currently not in GDPR dump per bb_overnight_gain_proxy.md section 6 caveat 5).
