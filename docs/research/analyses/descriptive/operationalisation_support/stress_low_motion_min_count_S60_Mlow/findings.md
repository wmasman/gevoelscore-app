# Findings -- stress_low_motion_min_count_S60_Mlow operationalisation-support descriptive (Q3.x.a-i)

**Channel**: `stress_low_motion_min_count_S60_Mlow` -- per-day integer count of minutes where Garmin `stress(t) >= 60` AND `intensity(t) <= 1` (low-motion class). Primary per [`methodology/stress_low_motion_primitive.md`](../../../methodology/stress_low_motion_primitive.md) section 4 (Session E lock 2026-06-15). Spike-counting primitive by construction per CONVENTIONS section 3.5; consumed by **HA-C4b v2 as primary** (and HA-C4 v2 as secondary before that test's REJECTION at `52bddb5` 2026-06-18).

**Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05). n=1365 days with channel out of 1372 Stratum 4 days (7 NaN days at the upstream extraction layer per `stress_low_motion_primitive.md` section 5 day-validity gate).

**Programme spec**: [`descriptive/README.md`](../../README.md) section 3.1 template (LOCKED 2026-06-18 r3, commit `ccbd12e`) generalised to this channel per section 6.3 (r2 closure D1.8 two-gaps-one-analysis: spike-detecting primitive coverage + HA-C4b v2 covariate-sensitivity readiness).

**Sources**: `per_day_master.csv` (Garmin daily aggregate; upstream extractor `pipeline/01_extract/stress_low_motion_extract.py` per `stress_low_motion_primitive.md` section 6) + `labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level -- per CONVENTIONS section 3.6).

**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar) per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). Statistical hygiene anchors: 3.1 (personal baseline), 3.3 (column-duplication threshold |rho|>=0.92), 3.4 (crash-drop sensitivity |delta|>0.10), 3.5 (spike metrics -- DIRECTLY APPLICABLE: this channel IS the spike primitive), 3.6 (named counts).

---

## Headline

`stress_low_motion_min_count_S60_Mlow` on Stratum 4 is a **right-skewed, autocorrelation-dense per-day count primitive** (skew=+1.40, excess kurtosis=+3.02; **data-driven E[L]\*=21.1 -- factor-of-3 above the project default E[L]=7 and ~1.7x above stress_mean_sleep's E[L]\*=12.6**, flag fires per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md)). Zero-inflation was anticipated in the handoff but **does not materialise** (zero-rate = 1.0%, n=14 zero-days out of 1365); the channel is a heavy-tailed positive count with median 55 min/day, not a zero-truncated rare-event channel. **The phase-stratified medians drop ~halve from unmedicated to consolidation** (med 77 to 38 min/day, delta=-39 min, ~-1.2 MAD on the consolidation MAD scale of 21 min/day) -- opposite to the direction a naive citalopram-raises-raw-stress-threshold reading would predict; the operationalisation-support implication is that the channel's per-phase interpretation is **non-monotonic in the upstream raw-stress threshold-shift**, requiring section 5.A/5.B treatment per the canonical framework. Crash-vs-normal separation is **smaller than `stress_mean_sleep`** at the episode level (d=+0.38 vs +0.91) but the rank-based Mann-Whitney U fires robustly (z=4.65 p<0.0001, P(crash>normal)=0.638). **Seven of eight sibling sensitivity-ladder columns flag as near-identity** (expected by construction per `stress_low_motion_primitive.md` section 4); the only out-of-flag sibling is `stress_low_motion_min_count_S75_Mstrict` (rho=+0.905, just below the 0.92 threshold). The continuous-form cousin `all_day_stress_avg` correlates at r=+0.85 / rho=+0.86 (NOT near-identity but very high -- the spike-form and daily-mean-form carry strongly overlapping signal on this corpus, more than the count-primitive design ladder suggests is independent).

---

## Q3.x.a -- Distribution shape (Stratum 4)

**Verdict on the section 3.1 delegate question**: **delegate is partial; extend in this analysis**. [`lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) was extended for continuous channels first and does not cover count primitives. The count-primitive-specific descriptors (zero-rate, dispersion ratio, monotonicity sanity) are surfaced here.

| stat | value | source |
|---|---:|---|
| n (Stratum 4) | 1365 | `per_day_master.csv` `stress_low_motion_min_count_S60_Mlow` non-NaN within S4 |
| unit | minutes/day (integer count) | `stress_low_motion_primitive.md` section 2 |
| mean | 66.8 | (single-pool S4) |
| median | 55.0 | |
| std (ddof=1) | 53.4 | |
| MAD (unscaled) | 29.0 | |
| MAD x 1.4826 (normal-equivalent SD) | 43.0 | for robust z-score scaling per section 3.1 |
| p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 | 0.6 / 9.0 / 15.0 / 29.0 / 55.0 / 94.0 / 131.0 / 160.0 / 228.1 | |
| skewness (Fisher-Pearson) | **+1.40** | right-skewed |
| excess kurtosis (Fisher) | **+3.02** | moderately heavy-tailed |
| heavy_tail_flag | **True** | skew>1 |
| range | 0 to 361 minutes/day | extreme tail values present |
| n_zero_days | **14** | per-day count = 0 |
| zero_rate | **1.0%** | NOT zero-inflated (handoff expectation refuted) |
| dispersion ratio (variance/mean) | 42.7 | over-dispersed relative to Poisson (would be ~1) |

### Count-primitive-specific notes

1. **Zero-inflation does NOT materialise on this primitive**. The handoff anticipated zero-inflation as the canonical count-primitive concern; the empirical zero-rate (1.0%) is in fact much smaller than would warrant a zero-inflated Poisson treatment. The channel is a heavy-tailed positive count with typical days carrying ~30-130 minutes of stress-at-rest. Read this as: *the primitive successfully measures a chronic-baseline construct, not a rare-event construct.*
2. **The dispersion ratio (variance/mean = 42.7) is far above Poisson** (expected 1) -- a Poisson regression would be badly under-dispersed. A negative-binomial or log-linear OLS framework is the natural model class for a future HA test using this channel as outcome; as predictor in a binary-outcome HA, the channel can enter on a transformed (log1p) scale to dampen the heavy tail.
3. **The robust-equivalent SD (MAD x 1.4826 = 43.0) is below the raw std=53.4** by ~20% -- the right tail is doing real work on the std, but less dramatically than on `stress_mean_sleep` (where the same ratio was ~30%). The MAD-based z-scoring (`_utils/frame.py::z_score_vs_rolling_baseline` default `robust=True`) is still preferred per CONVENTIONS section 3.1.

See [`plots/fig1_distribution_s4.png`](plots/fig1_distribution_s4.png).

---

## Q3.x.b -- Autocorrelation structure + E[L]*

The **data-driven block length is E[L]\*=21.1** (Politis-White 2004 with Patton-Politis-White 2009 correction per [`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) vs the project default E[L]=7 per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). The **factor-of-2 deviation flag fires** (deviation ratio = 2.0). Cutoff lag M=11.

| lag (days) | autocorrelation |
|---:|---:|
| 1 | +0.282 |
| 2 | +0.250 |
| 3 | +0.223 |
| 7 | +0.240 |
| 14 | +0.184 |

**Implication**: the channel is **more autocorrelated than `stress_mean_sleep`** (E[L]\*=21.1 here vs 12.6 for stress_mean_sleep on the same Stratum 4 surface). Two structural reasons are plausible:

1. **Long-memory weekly cycle**: ACF at lag 7 (+0.24) is *higher* than at lag 3 (+0.22), and the lag-14 ACF (+0.18) is still above the Politis-White 2-sigma threshold -- a weekly-rhythm residual on top of the slower trend that stress_mean_sleep doesn't carry. Plausibly reflecting weekly behavioural cadence (work-week vs weekend rest patterns) that the spike-during-rest construct catches but the daily-mean construct averages out.
2. **Slow trajectory**: the 90d rolling median (Q3.x.h) shows substantial multi-year movement (66 to 30 across the LC trajectory; ~halving), and the lag-1 ACF (+0.28) plus persistence past M=11 implies a slow trend that the channel rides for many weeks at a time.

Any HA pre-reg using `stress_low_motion_min_count_S60_Mlow` MUST (a) use the data-driven block length E[L]\*=21 as the primary bootstrap CI, OR (b) pre-spec a sensitivity arm at E[L]=21 alongside the default-E[L]=7 primary. The project default of 7 is **substantially too short** for this channel; the factor-of-3 deviation is larger than what triggered the stress_mean_sleep first analysis's E[L]=13 secondary CI.

See [`plots/fig5_acf.png`](plots/fig5_acf.png).

---

## Q3.x.c -- Base rates per citalopram phase (with zero-rate, count-primitive adaptation)

Phase axis per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 3:

| phase | window | n | median | mean | MAD | p25 / p75 / p90 | zero-rate |
|---|---|---:|---:|---:|---:|---|---:|
| unmedicated | 2022-09-03 to 2024-04-08 | 582 | **77.0** | 86.3 | 32.0 | 51 / 116 / 154 | 0.7% |
| buildup | 2024-04-09 to 2024-06-19 | 72 | **35.0** | 44.1 | 18.0 | 24 / 60 / 89 | 0.0% |
| consolidation | 2024-06-20 to 2026-03-19 | 634 | **38.0** | 51.1 | 21.0 | 24 / 64 / 105 | 1.6% |
| afbouw | 2026-03-20 to 2026-06-05 | 77 | **63.0** | 69.1 | 30.0 | 41 / 87 / 121 | 0.0% |

**The phase medians have a 2.2x range across phases** (77 unmedicated to 35 buildup), an order of magnitude larger than the corresponding `stress_mean_sleep` range (17.04 to 20.20 per the first analysis). The transition phases (buildup and afbouw) have **n<80 each** with narrower dispersion than the two **steady-state phases** (unmedicated and consolidation, n>580). Any HA test that wants per-phase verdicts under [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5.A on buildup or afbouw faces a ~8x n disadvantage vs the steady-state phases.

### Secondary cross-tab -- 6-phase recovery axis per [`lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) (LOCKED 2026-06-19 `d47e0d3`)

| recovery_phase | n | median | MAD | zero-rate |
|---|---:|---:|---:|---:|
| lc_pre_ergo | 19 | 55.0 | 30.0 | 0.0% |
| pacing_pre_citalopram_learning | 54 | 64.5 | 30.0 | 1.9% |
| pacing_habit_established | 509 | **79.0** | 32.0 | 0.6% |
| citalopram_modulated | 783 | **41.0** | 22.0 | 1.3% |

The 6-phase axis differentiates *within* the unmedicated portion of the citalopram axis (lc_pre_ergo / pacing_pre_citalopram_learning / pacing_habit_established are all `citalopram_phase == "unmedicated"`). The substantive pattern: within the unmedicated pacing era, the channel sits in the 55-79 median range; the citalopram era pulls the median down to 41. This is consistent with the citalopram-axis finding (Q3.x.d) but the recovery axis surfaces an additional fact: **within the pacing-habit-established sub-phase alone (n=509, the longest single bin), the median is 79 -- almost identical to the full unmedicated-axis median of 77.** The "phase shift" is concentrated at the citalopram boundary, not gradually accruing across the pacing learning sub-phases.

Named counts (CONVENTIONS section 3.6): the per-phase n's above are `stress_low_motion_min_count_S60_Mlow`-non-NaN day rows in `per_day_master.csv` within Stratum 4 date masks per each axis's source MD's boundary dates.

See [`plots/fig2_phase_stratified_citalopram.png`](plots/fig2_phase_stratified_citalopram.png) (citalopram axis violins) + [`plots/fig2b_phase_stratified_recovery_axis.png`](plots/fig2b_phase_stratified_recovery_axis.png) (6-phase recovery axis violins).

---

## Q3.x.d -- Phase-stratified distribution + count-primitive citalopram caveat

**This is the most operationally consequential finding for downstream HA pre-regs on this channel.**

Observed steady-state level shifts (median):

| comparison | delta median | within-phase MAD | within-MAD? |
|---|---:|---:|---|
| buildup minus unmedicated | **-42** min/day | 18-32 | ~-1.3 MAD on the buildup MAD; clearly outside MAD |
| consolidation minus unmedicated | **-39** min/day | 21-32 | ~-1.2 MAD on the consolidation MAD; clearly outside MAD |
| afbouw minus consolidation | **+25** min/day | 21-30 | ~+0.8 MAD on the consolidation MAD; close to MAD boundary |
| afbouw minus unmedicated | **-14** min/day | 30-32 | ~-0.4 MAD; within MAD |

### Reading the direction -- what the data shows + the operationalisation-support consequence

The medians **drop sharply at the citalopram boundary** (unmedicated to buildup: -42 min/day; about 55% reduction in median minutes-of-stress-at-rest per day). This is **opposite in direction to the naive prediction** that a citalopram-raised raw-stress baseline (+12-17 stress units at 30mg per the v3 dose-response MD section 5.6) would push more minutes above the S=60 threshold. Three readings are consistent with the descriptive observation; per CONVENTIONS section 2.1 + section 4.3 no single reading is asserted -- the descriptive substrate is the menu:

1. **Citalopram narrows the upper-tail of the raw stress distribution** (NOT just shifts its mean upward). A narrower distribution with elevated mean spends *less* time at extreme values like S>=60 even though the mean rises. This is consistent with a tranquillising-with-tone-lift effect: floor rises, ceiling drops, time-above-threshold falls. The dose-response MD's v3 finding measured the daily-mean shift (+12-17 raw stress points at 30mg), not the daily-tail-count shift, so the two findings are not incompatible.
2. **Genuine within-LC-trajectory recovery**: the citalopram phases (buildup to consolidation to afbouw) coincide with later-LC days. Pacing-practice strengthening + LC-recovery-arc partial improvement could be reducing genuine sympathetic-arousal-at-rest minutes over time, independent of the medication mechanism. The Q3.x.c recovery-axis breakdown (pacing_habit_established median 79; close to the unmedicated 77) argues against this reading at the pacing-era boundary specifically -- the within-unmedicated-era medians are flat -- but cannot rule out additional recovery happening across the citalopram boundary itself.
3. **The S=60 threshold is operating in a non-linear regime relative to the dose-modulation**. The primitive is dose-naive by design (per `stress_low_motion_primitive.md` section 1.2); consumer tests apply [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5.B dose-adjustment on the predictor side. The shape of the dose-modulation on the count is **non-linear by construction** (depends on the upstream raw-stress distribution's mass-above-threshold, not its mean) -- the per-mg slope on the raw stress channel does not translate to a per-mg slope on the count.

**Operational consequence for HA pre-regs on this channel**: a future HA on `stress_low_motion_min_count_S60_Mlow` cross-phase MUST adopt section 5.A per-phase stratification or section 5.B dose-adjustment. The cross-phase comparison is **not interpretable in raw form**. The section 5.B dose-adjustment as canonically formulated is for channels where the per-mg slope IS locked (e.g. +0.43/mg for stress_mean_sleep); for this count primitive the analogous dose-adjustment is a phase indicator or a phase-fixed-effects approach, NOT a per-mg numerical correction. This is a **structural difference from the stress_mean_sleep first analysis**: the operationalisation-support output here is "phase-fixed-effect treatment" not "dose-adjusted predictor".

**No per-mg slope is locked on this count primitive.** Per the handoff: unlike `stress_mean_sleep` (+0.43/mg p=0.001 buildup post-CPAP), the per-mg dose-response slope on this count is NOT a locked finding. The dose-modulation operates UPSTREAM on the raw stress channel; the count primitive is a non-linear function of that upstream distribution. A future analysis estimating a per-mg-on-count slope is a separable artefact (would need explicit motivation, e.g. a consumer HA test requesting it).

See [`plots/fig2_phase_stratified_citalopram.png`](plots/fig2_phase_stratified_citalopram.png) (violins) and [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d rolling median through phases).

---

## Q3.x.e -- Near-identity check (threshold |rho|>=0.92 per CONVENTIONS section 3.3)

Three sections per the handoff: 8 sibling sensitivity-ladder columns (highly correlated by construction); 2 respiration companions (orthogonal by design); 6 continuous cousins (the daily-mean stress / autonomic family).

### Section 1 -- sibling sensitivity-ladder columns

| sibling | n | Pearson r | Spearman rho | near-identity flag? |
|---|---:|---:|---:|---|
| `stress_low_motion_min_count_S50_Mstrict` | 1365 | +0.951 | +0.947 | YES |
| `stress_low_motion_min_count_S50_Mlow` | 1365 | +0.977 | +0.979 | YES |
| `stress_low_motion_min_count_S50_Mbelow_mod` | 1365 | +0.977 | +0.979 | YES |
| `stress_low_motion_min_count_S60_Mstrict` | 1365 | +0.977 | +0.971 | YES |
| `stress_low_motion_min_count_S60_Mbelow_mod` | 1365 | **+1.000** | **+1.000** | YES (identical) |
| `stress_low_motion_min_count_S75_Mstrict` | 1365 | +0.895 | +0.905 | no (just below) |
| `stress_low_motion_min_count_S75_Mlow` | 1365 | +0.916 | +0.920 | YES (Spearman = threshold) |
| `stress_low_motion_min_count_S75_Mbelow_mod` | 1365 | +0.916 | +0.920 | YES (Spearman = threshold) |

**Seven of eight siblings flag near-identity**. This is **expected by construction** per `stress_low_motion_primitive.md` sections 3.2 + 4: the three motion classes `Mlow` and `Mbelow_mod` are operationally identical in the v1 primitive (section 3.2 notes the collapse), and the S=50 / S=60 / S=75 thresholds operate on the same upstream per-minute stress trace.

Two findings beyond construction:

1. **`stress_low_motion_min_count_S60_Mbelow_mod` is exactly identical to the primary** (rho=+1.000, r=+1.000). This **confirms the section 3.2 design note** that `M=low_or_below` and `M=any_below_moderate` collapse to the same column in v1 -- the two columns are the same data. The 9-column sensitivity ladder is effectively a **6-column ladder** at v1 (3 stress thresholds x 2 distinct motion classes); the `_Mbelow_mod` columns are placeholders for future-refinement intensity-class investigation per `stress_low_motion_primitive.md` section 3.2.
2. **The only sibling NOT flagging is `S75_Mstrict`** (Pearson +0.895, Spearman +0.905) -- the most conservative threshold + strictest motion filter combination. This is the column that picks up only the rarest events (median 10 min/day vs the primary's 55). The independent-signal portion of this sibling is the *rare high-stress at strict-sedentary minutes* -- the construct's high-confidence subset. A consumer test wanting a stricter version of the primary should use this column, not just raise the threshold of the primary alone.

### Section 2 -- respiration companions (orthogonal by design per section 4b)

| companion | n | Pearson r | Spearman rho | near-identity flag? |
|---|---:|---:|---:|---|
| `n_minutes_resp_above_18` | 1365 | +0.200 | +0.093 | no |
| `n_minutes_resp_in_rest_band_10_18` | 1365 | +0.149 | +0.102 | no |

Both companions are **far from near-identity** -- they carry independent signal as the section 4b design intends. The slightly-positive Pearson r=+0.20 with `n_minutes_resp_above_18` is consistent with section 3.3b's "either hidden motion or sympathetic arousal" reading: a fraction of stress-at-rest minutes do co-occur with elevated respiration. The two columns can enter a future HA as separate covariates without redundancy.

### Section 3 -- continuous cousins

| cousin | n | Pearson r | Spearman rho | near-identity flag? |
|---|---:|---:|---:|---|
| `stress_mean_sleep` | 1339 | +0.294 | +0.167 | no |
| `stress_stdev_sleep` | 1339 | +0.204 | +0.194 | no |
| `all_day_stress_avg` | 1358 | **+0.847** | **+0.860** | no (close) |
| `all_day_stress_max` | 1358 | +0.376 | +0.479 | no |
| `awake_stress_avg` | 1358 | **+0.821** | **+0.863** | no (close) |
| `asleep_stress_avg_uds` | 1363 | +0.300 | +0.186 | no |

**No near-identity flag fires on continuous cousins**, but **`all_day_stress_avg` (r=+0.85 / rho=+0.86) and `awake_stress_avg` (r=+0.82 / rho=+0.86) are very high** -- close enough that they should be treated with care by any consumer HA. Both are 24h-window daily-mean stress metrics; the strong correlation reflects that on a typical day, when the 24h stress mean rises, more minutes cross the S=60 threshold *and* most of those threshold crossings happen during awake (not asleep) windows. The cross-channel-correlation card's existing 7-channel panel does not include either of these pairs vs `stress_low_motion_min_count_S60_Mlow`; **propose adding them at the next refresh of `analyses/garmin_exploration/cards/cross-channel-correlation.md`** (flag-only -- no edits to the card as part of this analysis per handoff section 6 + section 5.5 discipline).

**`stress_mean_sleep` is essentially independent** of this channel (r=+0.29 / rho=+0.17), confirming the first-analysis Q3.1.e finding -- sleep-window mean stress and 24h-window stress-at-rest spike-counts are different constructs.

See [`plots/fig6_sibling_ladder_corr.png`](plots/fig6_sibling_ladder_corr.png) (sibling sensitivity-ladder Spearman heatmap).

---

## Q3.x.f -- Crash-day vs normal-day (refresh into operationalisation-support; count-primitive Mann-Whitney U robustness check)

Per CONVENTIONS section 3.6 named counts: 29 crash-episodes (crash_v2 episode-level via `labels_crash_v2.csv` unique `episode_id` starting with `crash-`); 103 crash-days (day-level, `label=='crash'`); 1262 non-crash days (the complement within Stratum 4 channel-valid days).

### Episode-level (primary unit per CONVENTIONS section 3.6)

| stat | value |
|---|---:|
| n crash-episodes | 29 |
| n normal-day base rate | 1262 |
| mean per-episode count | 73.0 |
| mean normal-day count | 55.4 |
| median normal-day count | 47.0 |
| mean diff (episode minus normal-day) | **+17.6** min/day |
| median diff (episode minus normal-day) | **+22.0** min/day |
| Cohen's d (episode-level vs normal-day pooled) | **+0.38** |
| Bootstrap 95% CI on mean diff | **[+0.94, +34.88]** (5000 iters, seed=20260622) |

**Cohen's d=+0.38 is smaller than `stress_mean_sleep`'s +0.91** at the episode level (per the first analysis Q3.1.f). The bootstrap 95% CI on mean diff just barely excludes zero (+0.94 lower bound); the signal is real but **substantially less pronounced** than the daily-mean stress channel. The median diff (+22) is consistent with a real but moderate effect; the count primitive picks up a positive crash-day shift, but the construct is less tightly coupled to crashes than sleep-window mean stress.

### Day-level (autocorrelation-inflated supplementary)

| stat | value |
|---|---:|
| n crash-days | 103 |
| n normal-days | 1262 |
| mean crash-day | 88.8 |
| mean normal-day | 55.5 |
| median crash-day | 79.0 |
| median normal-day | 53.0 |
| mean diff (point estimate) | **+33.3** min/day |
| median diff | **+26.0** min/day |
| Cohen's d | **+0.68** |
| Mann-Whitney U: z | **+4.65** |
| Mann-Whitney U: p (two-sided, normal approx with tie correction) | **<0.0001** |
| Mann-Whitney U: P(crash > normal) | **+0.638** |
| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (project default) | [+12.12, +54.15], width 42.02 |
| Stationary bootstrap 95% CI on mean diff, **E[L]=21** (data-driven, Q3.x.b flag fired) | **[+9.73, +56.13]**, width 46.41 |

### Mann-Whitney U robustness -- the count-primitive's primary read

The Mann-Whitney U is the rank-based equivalent (no parametric assumption on Cohen's d's pooled-SD logic, which can mislead on heavy-tailed count data). **The signal is unambiguously present**: z=+4.65, p<0.0001, P(crash > normal) = 63.8% (i.e. a randomly-picked crash day has a higher count than a randomly-picked normal day 64% of the time, vs 50% under the null). The median diff (+26 min/day) is similar magnitude to the IQR-half-width (32 = 94 - 62 for the full population), comparable to ~1 within-population MAD.

**Read together with Cohen's d**: the count primitive carries a moderate positive shift on crash days that survives the rank-based robustness check. The smaller-than-stress_mean_sleep Cohen's d at episode level (+0.38 vs +0.91) reflects the wider within-population dispersion of the count primitive, not absence of signal.

### Block-length sensitivity (Q3.x.b cross-check)

Per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md), when the data-driven E[L]* deviates from the project default by more than a factor of 2, the analysis must report the CI at the data-driven value alongside the default. Q3.x.b fired that flag (E[L]*=21, deviation ratio 2.0). The E[L]=21 CI ([+9.73, +56.13]) is +10.5% wider than the E[L]=7 CI ([+12.12, +54.15]) and slightly shifted -- both exclude zero, and the substantive read is unchanged. **Both block-length choices fire the day-level signal**; the day-level Cohen's d and Mann-Whitney U findings are robust to the autocorrelation block-length choice.

### Crash-drop sensitivity (CONVENTIONS section 3.4)

For a descriptive-layer sanity check we report `Spearman(stress_low_motion_min_count_S60_Mlow, gevoelscore)` with `is_crash` rows dropped:

| frame | Spearman rho | n |
|---|---:|---:|
| full Stratum 4 | -0.056 | 1365 |
| crash-days dropped | +0.001 | 1262 |
| \|delta\| | **0.057** | -- |
| section 3.4 threshold (0.10) crossed? | **no** | -- |

The crash days **are doing some correlation work** in the channel-vs-gevoelscore pair (full rho=-0.06 reverses to ~0 when crashes drop), but the magnitude is below the section 3.4 threshold. No flag fires. The same-day channel-vs-gevoelscore correlation is essentially zero in the normal-day population -- gevoelscore and stress-at-rest minute counts are **decoupled on normal days** at the daily resolution. This is consistent with the project's broader same-day-coupling observations (gevoelscore is more sensitive to context than to a single autonomic-channel value).

See [`plots/fig4_crash_vs_normal.png`](plots/fig4_crash_vs_normal.png).

---

## Q3.x.g -- Spike-detecting primitive availability -- **the channel IS the spike primitive by construction**

Per CONVENTIONS section 3.5 + `stress_low_motion_primitive.md` section 7.4 audit hook on section 3.5: this channel is per-minute threshold-crossing (`stress(t) >= 60` AND `intensity(t) <= 1`) aggregated to a per-day count. It IS the spike primitive -- not a continuous daily-mean dilution-vulnerable to acute load.

### Sensitivity-ladder coverage in master (9 columns + 2 respiration companions)

| column | n | median (S4) | p90 | is primary? |
|---|---:|---:|---:|---|
| `stress_low_motion_min_count_S50_Mstrict` | 1365 | 64.0 | 147 | no |
| `stress_low_motion_min_count_S50_Mlow` | 1365 | 90.0 | 183 | no |
| `stress_low_motion_min_count_S50_Mbelow_mod` | 1365 | 90.0 | 183 | no |
| `stress_low_motion_min_count_S60_Mstrict` | 1365 | 38.0 | 104 | no |
| **`stress_low_motion_min_count_S60_Mlow`** | **1365** | **55.0** | **131** | **PRIMARY** |
| `stress_low_motion_min_count_S60_Mbelow_mod` | 1365 | 55.0 | 131 | no |
| `stress_low_motion_min_count_S75_Mstrict` | 1365 | 10.0 | 46 | no |
| `stress_low_motion_min_count_S75_Mlow` | 1365 | 18.0 | 60 | no |
| `stress_low_motion_min_count_S75_Mbelow_mod` | 1365 | 18.0 | 60 | no |
| `n_minutes_resp_above_18` | 1365 | (resp companion) | | resp companion |
| `n_minutes_resp_in_rest_band_10_18` | 1365 | (resp companion) | | resp companion |

### Sensitivity-ladder findings beyond the primary

1. **Monotonicity holds across the entire S4 surface** (no day-level violations): at every motion class, count(S=50) >= count(S=60) >= count(S=75), n=1365 days. This is the section 8.3 validation check from `stress_low_motion_primitive.md` returning all-OK on the live data. The primitive extractor is functioning correctly.
2. **The Mlow == Mbelow_mod collapse is total** at v1: every (S, Mbelow_mod) column is *exactly identical* to the corresponding (S, Mlow) column on this corpus (Q3.x.e rho=+1.000). This **confirms the section 3.2 design note** that `M=low_or_below` and `M=any_below_moderate` are operationally the same column in v1 (placeholder for future refinement). The effective ladder is 6 columns (3 stress thresholds x 2 distinct motion classes), not 9. Future v2 of the primitive may differentiate `Mbelow_mod`; until then, sensitivity-ladder consumer tests should report 6 distinct columns per section 4 sensitivity discipline, not 9 (the 9-column language in section 4 should be read as "9 column names, 6 distinct primitives at v1").
3. **The S75 columns carry independent-from-primary signal** more visibly than the S50 columns (S75_Mstrict rho=+0.905 vs primary; S75_Mlow rho=+0.920 vs primary). For a consumer test wanting a *stricter* spike-primitive, the S75 family is informative -- not just a re-thresholding of the primary.

### Continuous-form cousin: `all_day_stress_avg`

Per CONVENTIONS section 3.5, the daily-mean dilution-vulnerable form of this construct is `all_day_stress_avg` (CONFIRMED-citalopram +0.57/mg per dose-response MD v3 section 5.6). The Pearson r=+0.847 / Spearman rho=+0.860 between primary count and `all_day_stress_avg` (n=1358) is high but **not** near-identity (Q3.x.e). The interpretation per construction: when the day's 24h-window mean stress rises, more minutes cross the S=60 threshold; the count primitive carries that information PLUS the threshold-specific timing/density information the daily mean averages out. A future HA whose mechanism is *acute spike at rest* should use the count primitive; a future HA whose mechanism is *general autonomic load throughout the day* should use the continuous cousin. The two channels are not interchangeable but they share substantial signal on this corpus.

**Operational consequence**: this primitive answers the spike-vs-mean question per section 3.5 in a binding way for any consumer HA in the autonomic-load family. The "continuous-form cousin" + "spike-form primitive" pair is the framework's recommended pattern; this primitive is the spike-form on this corpus and `all_day_stress_avg` is its continuous cousin.

### Respiration companions

Per `stress_low_motion_primitive.md` section 4b, the two respiration companions (`n_minutes_resp_above_18`, `n_minutes_resp_in_rest_band_10_18`) carry orthogonal signal (Q3.x.e r=+0.20 and r=+0.15 respectively). They enable downstream tests to disambiguate the hidden-motion vs sympathetic-arousal readings of the primary count per section 3.3b's honest reading rules. A consumer HA wanting the **high-confidence-stress-at-genuine-rest** subset can intersect primary count with `n_minutes_resp_in_rest_band_10_18`; a consumer wanting the **stress-with-breathing-change** subset can intersect with `n_minutes_resp_above_18`. Both intersections live in the consumer test (not in this primitive's extraction or this descriptive analysis).

---

## Q3.x.h -- Outlier detection + calibration-drift check + audit-doc gap

Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md):
- Day-validity gate >=600 in-range stress samples per `stress_low_motion_primitive.md` section 5; days below gate get count=0 + valid_flag=0 (not NaN -- the day was tracked but coverage was insufficient).
- Days with no monitoring_b FIT file at all: all 9 columns NaN + valid_flag NaN (device-off days).
- Underlying sensor is Forerunner 245 Elevate V3 throughout 2021-08-16 to present -- **no device change**.

### **Audit-doc gap (PROPOSE-ONLY)**

[`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) **does NOT yet have a row for this primitive family** (`stress_low_motion_min_count_S<S>_M<M>` + the 2 respiration companions). It is a Wave-4-era custom extraction added after the audit's last revision. **Proposed row content** (do NOT apply as part of this analysis per handoff section 6 + section 5.5 discipline):

> Channel family: `stress_low_motion_min_count_S<S>_M<M>` (9 columns per `stress_low_motion_primitive.md` section 4 + 2 respiration companions per section 4b). Upstream extractor: `pipeline/01_extract/stress_low_motion_extract.py`. Source FIT: monitoring_b classified files per HA11 precedent. Day-validity gate: >=600 in-range stress samples (values in [1,100]) per `stress_low_motion_primitive.md` section 5; days below gate get count=0 + valid_flag=0. Sentinel handling: too_active + off_wrist values outside [1,100] not counted; both contribute to day's in-range sample count being below the 600 gate if numerous. Calibration: no documented drift events for this primitive (added 2026-06-22 per descriptive `stress_low_motion_min_count_S60_Mlow/findings.md` Q3.x.h). Device: Forerunner 245 Elevate V3 throughout 2021-08-16 to present (no device change).

Surface to user for authorisation in a separate session per the discipline.

### Outlier scan (MAD-based |z|>5; threshold per CONVENTIONS section 3.1 robust-baseline default)

**6 outlier-days flagged** out of 1365:

| date | value (min/day) | MAD-z | likely category |
|---|---:|---:|---|
| 2023-04-01 | 311 | +5.95 | early-LC April-2023 pair (same dates flagged in stress_mean_sleep Q3.1.h) |
| 2023-04-02 | 318 | +6.12 | (pair) |
| 2023-07-07 | 307 | +5.86 | mid-2023 isolated |
| 2023-11-28 | 285 | +5.35 | Nov-2023 prodrome (named exemplar day per `stress_low_motion_viz/family_a_daily.py`) |
| 2023-11-29 | **361** | **+7.12** | global max (this is the channel's max; same date is also the global max for stress_mean_sleep per Q3.1.h "peak crash" exemplar) |
| 2025-01-17 | 297 | +5.63 | early-consolidation isolated |

The outliers are **not artefacts**: they cluster around named high-stress-at-rest events (2023-04 pair, 2023-11 prodrome+peak per the lived-experience-anchored exemplars in `garmin_exploration/stress_low_motion_viz/family_a_daily.py`). The 2023-11-29 global max is the *same day* as the global-max outlier on `stress_mean_sleep` (per Q3.1.h of the first analysis) -- cross-channel consistency of the peak-crash event signature. Downstream HA tests should NOT trim these -- they are real stress-at-rest events, not sensor failures.

### Drift check -- rolling 90d median over Stratum 4

| snapshot date | rolling 90d median (min/day) |
|---|---:|
| 2022-12-01 | 66.0 |
| 2023-06-01 | 86.5 |
| 2023-12-01 | 75.5 |
| 2024-06-01 | 44.0 |
| 2025-01-01 | 30.0 |
| 2025-12-01 | 35.0 |

**The rolling 90d median exhibits a clear multi-year downward trajectory** (66 to 86.5 mid-2023 peak to 30 early-2025 trough to 35 late-2025; ~2x swing top to bottom). This is **not** a calibration-drift signature -- the change tracks the citalopram boundary (2024-04-09, sharp drop from ~75 to ~44 in mid-2024) and the broader LC-recovery trajectory. The **consolidation-boundary step at 2024-06-20** shows trailing-30d mean = 58.8, leading-30d mean = 61.0 -- a **+2.2 min/day step**, well within MAD; the channel does NOT register a sharp step at the consolidation boundary specifically (the citalopram-modulation effect is spread across buildup + early consolidation, not crystallised on 2024-06-20). The full citalopram-axis shift surfaces in the longer 90d window (44 by 2024-06-01).

See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).

---

## Q3.x.i -- Covariate-sensitivity readiness for a future HA pre-reg on this channel

Discipline anchor: [HA-P7 hypothesis.md section 4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) (secondary-logistic-with-covariate pattern; beta disambiguation between primary-signal and a candidate alternative reading). Names **four** candidate covariates a future HA on `stress_low_motion_min_count_S60_Mlow` as predictor should pre-spec:

### 1. `all_day_stress_avg` -- continuous-form cousin; "general stress level" control

Observed Q3.x.e Pearson r=+0.847 / Spearman rho=+0.860 (n=1358) -- strong shared signal. The covariate disambiguates the spike-during-rest count from the general-daily-stress-level reading: **beta_channel attenuates -- the primary signal was just "today was a higher-stress day overall"**; **beta_channel survives -- the spike-during-rest count carries information beyond mean stress**. This is the **obligatory spike-vs-mean disambiguator per CONVENTIONS section 3.5** for any consumer HA on this channel. The dose-modulation confound is **shared** between predictor and this covariate (both are downstream of the same upstream raw stress channel modulated by citalopram), so this arm primarily disambiguates the temporal-density/timing signal from the global-level signal, not the citalopram confound.

### 2. `n_minutes_resp_above_18` -- respiration companion; hidden-motion vs sympathetic-arousal

Observed Q3.x.e Pearson r=+0.20 / Spearman rho=+0.09 (n=1365) -- far from redundant; carries genuine independent signal. Per `stress_low_motion_primitive.md` section 3.3b's honest reading rules: a high-stress-low-motion minute that is ALSO in this respiration-elevated bucket is either hidden motion the intensity proxy missed OR genuine sympathetic arousal with breathing change. The covariate disambiguates: **beta_channel attenuates -- respiration was doing the predictive work (the signal is generic sympathetic arousal, the motion-filter wasn't the discriminator)**; **beta_channel survives -- the stress-at-rest construct's intensity-filtered specificity is doing real work**. This is the **obligatory hidden-motion disambiguator** for any consumer HA on this channel.

### 3. `resting_hr` -- alternative autonomic-tone anchor

Observed Pearson r=+0.13 / Spearman rho=+0.10 (n=1356) -- modest correlation. The covariate disambiguates: **beta_channel attenuates -- the signal is shared autonomic-tone (chronic sympathetic-dominance)**; **beta_channel survives -- the acute-spike-at-rest construct is distinct from chronic autonomic-tone**. The weaker correlation than stress_mean_sleep showed with resting_hr (+0.34 / +0.38 per first analysis Q3.1.i) is informative: the spike-count primitive is more autocorrelation-orthogonal to resting HR than the daily-sleep-stress mean is. Useful diagnostic covariate.

### 4. `stress_low_motion_min_count_S60_Mlow_lagged_mean_14d(d) = mean(channel[d-14:d-1])` -- autocorrelation-vs-mechanism

Per HA-P7 section 4.5.4 worked example (lagged outcome covariate). Per Q3.x.b the cutoff lag M=11 and E[L]*=21; **the channel's autocorrelation horizon is longer than for stress_mean_sleep**, so a 14d lagged trailing mean is *just past* the autocorrelation horizon for this primitive (vs comfortably-past for stress_mean_sleep). A consumer HA might prefer a 21d or 28d window for this covariate on this channel specifically -- the descriptive substrate says the autocorrelation is longer here, the consumer-test pre-reg has the discretion to set the window past the M=11 cutoff with margin.

### Recommendation for any HA pre-reg on this channel

Pre-spec all four covariates as **secondary sensitivity arms**. Concordance across the four secondaries = high confidence in the primary; divergence = the disambiguation is doing real work. Per the **count-primitive nature** of this channel, consumer tests should also consider:

- **Modelling-class choice**: the dispersion ratio (variance/mean = 42.7 per Q3.x.a) is far above Poisson; negative-binomial or log-linear OLS (with log1p transform) are the natural model classes; Poisson regression is wrong by construction here.
- **Cardinality-matching for the covariate set**: the all_day_stress_avg + resting_hr arms are continuous; the respiration companion is a count (matches predictor cardinality); the 14d-lagged arm inherits the predictor's count cardinality. A negative-binomial outcome with a mix of count and continuous covariates is the standard form.
- **Phase treatment per section 5.A is the natural canonical** (per Q3.x.d); section 5.B dose-adjustment as canonically formulated requires a per-mg slope which is not locked on this count primitive -- phase-fixed-effects is the safer default.

---

## Cross-references

### HA-* tests that touch this channel (cite this analysis)

- **HA-C4b v2** (primary user of this channel as predictor): the test that locked the channel name itself. v3 NOT-SUPPORTED at v3-result; the descriptive substrate this analysis produces is upstream of HA-C4b vNext reframing. Specifically: Q3.x.d's per-phase findings argue for section 5.A phase-stratification over section 5.B numerical dose-adjustment; Q3.x.f's moderate-but-real episode-level signal (d=+0.38) constrains the section 7 anchor strategy; Q3.x.b's E[L]*=21 expands the block-length policy to a longer window than HA-C4b v2 used.
- **HA-C4 v2** (REJECTED at `52bddb5` 2026-06-18): the multi-channel Wiggers-C4 triad including this primitive among the secondaries. The descriptive substrate this analysis produces is relevant for the post-rejection re-interpretation conversation: did the rejection stem from (a) channel-level non-signal, (b) operationalisation-mismatch, or (c) genuine Wiggers-C4 falsification on this corpus? **Q3.x.f shows the channel HAS a moderate crash-vs-normal signal at episode level (d=+0.38, Mann-Whitney p<0.0001)** -- so reading (a) "channel-level non-signal" is hard to sustain on this primitive specifically. The triad sum 0.0 at HA-C4 v2 likely reflects either operationalisation-mismatch or genuine falsification on the triad's specific construct definition, not absence of signal on this individual channel.
- **HA-C4b vNext / HA-C4c** (likely future consumers per `bout_level_recovery_dynamics.md` `c57ff3f`): the bout-level reframing surface that will eventually consume this primitive at sub-day resolution. The descriptive characterisation here at per-day resolution is upstream of any bout-level reframing; the count primitive aggregates *over the bouts within each day* (per `stress_low_motion_primitive.md` section 2), so the bout-level analysis is a refinement, not a replacement.
- **HA11** (`HA11-stress-udip/extract_udip_counts.py`): shares the FIT-source and the 600-sample day-validity gate; Q3.x.h's known-issues summary cross-references HA11's gate.

### Methodology MDs cited

- [`methodology/stress_low_motion_primitive.md`](../../../methodology/stress_low_motion_primitive.md) -- definitional substrate (Session E lock 2026-06-15); cited across all Q3.x.a-i.
- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) sections 3-6 -- Q3.x.c phase axis, Q3.x.d phase-stratified, Q3.x.i covariate framework.
- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) v3 section 5.6 -- conceptual link in Q3.x.d (raw-stress dose-modulation propagating to count via threshold-shift).
- [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) -- Q3.x.a delegate target (extended here for count primitive; the MD does not cover count channels in detail).
- [`methodology/lc_recovery_phase_axis.md`](../../../methodology/lc_recovery_phase_axis.md) (LOCKED 2026-06-19 `d47e0d3`) -- Q3.x.c secondary axis cross-tabulation.
- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) -- E[L]=7 default + factor-of-2 deviation rule; Q3.x.b fires the flag (factor-of-3 deviation).
- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) -- Q3.x.h cross-reference; **MISSING ROW for this primitive flagged** (PROPOSE-ONLY).
- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) -- Stratum 4 boundary definition.
- [`methodology/bout_level_recovery_dynamics.md`](../../../methodology/bout_level_recovery_dynamics.md) (LOCKED 2026-06-21 `c57ff3f`) -- future bout-level reframing surface.

### Existing artefacts referenced

- [`garmin_exploration/stress_low_motion_viz/`](../../../analyses/garmin_exploration/stress_low_motion_viz/) -- existing primitive visualisation work. Specifically:
  - `per_phase_descriptive.py` -- emits a per-phase descriptive card on the RAW column (no HA-C4b section 4.3 eligibility restriction); this analysis refreshes the substantive findings in operationalisation-support framing.
  - `family_a_daily.py` -- within-day per-minute plots for 3 exemplar days: 2023-11-28 prodrome, 2023-11-29 peak crash (also this analysis's Q3.x.h global outlier max), 2024-11-26 rest exemplar. Cited as complementary visualisation.
  - `family_b_timeseries.py`, `family_c_event.py`, `family_d_diagnostic.py` -- additional visualisation families; cited as existing coverage.
- [`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) -- Q3.x.e cross-reference. This analysis surfaces **two new near-misses worth indexing** at next refresh: `all_day_stress_avg` (r=+0.85) and `awake_stress_avg` (r=+0.82) vs the primary count.
- [`descriptive/operationalisation_support/stress_mean_sleep/`](../stress_mean_sleep/) -- first Strand A analysis; this analysis mirrors its Q-template structure with count-primitive adaptations and provides explicit cross-channel comparison anchors (E[L]* 21 here vs 12.6 there; Cohen's d episode-level +0.38 here vs +0.91 there).

### Upstream pipeline

- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` <- `processed/garmin/stress_low_motion_minutes.csv` <- `pipeline/01_extract/stress_low_motion_extract.py` per `stress_low_motion_primitive.md` section 6.
- `labels_crash_v2.csv` <- `garmin/hypotheses/crash_v2-definition/definition.md` (locked).

---

## Limitations

For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding limitations a downstream HA pre-reg author should carry forward are:

1. **Q3.x.c-d are on raw channel values, not dose-adjusted or phase-fixed-effects-adjusted.** Per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) section 5, any HA using this channel cross-phase must adopt section 5.A / 5.B / 5.C treatment; section 5.A (per-phase stratification) is the safer default for THIS count primitive because the per-mg slope on the count is not locked (unlike stress_mean_sleep). The opposite-direction phase-shift (medication-LOWERS counts) is a structural property of the threshold-based count, not a contradiction of the dose-response MD's daily-mean finding.
2. **The channel IS the spike primitive per CONVENTIONS section 3.5**, NOT a daily-mean dilution-vulnerable channel (Q3.x.g). A future HA whose mechanism is *general autonomic load* should use the continuous cousin `all_day_stress_avg`, not this channel as primary; a future HA whose mechanism is *acute spike-during-rest* should use this channel. The two are different constructs even though they correlate at r=+0.85 on this corpus.
3. **The day-level Cohen's d=+0.68 is autocorrelation-inflated** (Q3.x.f). The episode-level d=+0.38 is the headline (substantially smaller than `stress_mean_sleep`'s +0.91 episode-level); consecutive within-episode days are not independent observations. The Mann-Whitney U at day level (z=+4.65 p<0.0001) provides a robust crash-vs-normal signal but the rank-based test still treats consecutive days as independent; the episode-level Cohen's d + bootstrap CI is the unit-of-analysis-clean read.
4. **The outlier-rule MAD-z|>5 is a descriptive-stage screen** (Q3.x.h) -- downstream HA tests must NOT trim these days; they are real stress-at-rest events (the 2023-11-29 peak crash + the 2023-04-01/02 pair are named exemplars per `stress_low_motion_viz/family_a_daily.py`). Per CONVENTIONS the heavy-tail is part of the channel's natural shape.
5. **The 9-column sensitivity ladder is effectively a 6-column ladder at v1** (Q3.x.e + Q3.x.g): `Mbelow_mod` == `Mlow` for every stress threshold. Consumer tests applying the section 4 sensitivity discipline should report 6 distinct primitives, not 9. The 9-column language in `stress_low_motion_primitive.md` section 4 is correct as forward-compatible naming for a future v2 refinement; on the live v1 data the ladder is 3 stress thresholds x 2 distinct motion classes.
6. **The autocorrelation horizon is longer than for `stress_mean_sleep`** (Q3.x.b E[L]*=21 vs 12.6). Consumer tests using this channel with autocorrelation-controlled methods (block bootstrap, OLS-with-Newey-West, etc.) must use a longer block-length than the project default. The factor-of-3 deviation is the largest yet observed in the Strand A analyses landed so far.
7. **The `garmin_indicators_audit.md` row for this primitive family is missing** (Q3.x.h). Proposed row content surfaced; do NOT apply without user authorisation per handoff discipline section 6.

---

## Status

**Current as of 2026-06-22** (commit context: post-`ccbd12e` descriptive programme lock; Phase 1 third analysis; landed alongside the bout-level methodology lock cascade `c57ff3f`). Refresh when:

1. Stratum 4 right edge advances by >=30 days AND any HA pre-reg on this channel is about to spin up (per CONVENTIONS section 3.1 personal-baseline freshness).
2. A new citalopram-phase boundary lands (e.g. post-afbouw enters analytic scope as of 2026-06-06 onward).
3. The Politis-White E[L]* shifts by another factor of 2 from current 21.1 (current factor-of-3-vs-default flag fired; further drift changes downstream HA block-length policy).
4. The `all_day_stress_avg` and `awake_stress_avg` near-miss pairs (Q3.x.e r=+0.85 / r=+0.82) get propagated into the cross-channel-correlation card's 7-channel panel (would update Q3.x.e cross-reference).
5. HA-C4 v2 bout-level reframing (per `bout_level_recovery_dynamics.md` `c57ff3f` future consumers) spins up and surfaces sub-day operationalisation findings that would change the per-day descriptive substrate.
6. The `garmin_indicators_audit.md` row gets added with the proposed content (Q3.x.h flag); this analysis's Q3.x.h cross-reference would then be a direct citation rather than a flag.
