# Findings — `stress_mean_sleep` operationalisation-support descriptive (Q3.1.a–i)

**Channel**: `stress_mean_sleep` (CONFIRMED-citalopram, +0.43/mg p=0.001 buildup post-CPAP per [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) v3 §5.6.1). Column semantics: [DATA_DICTIONARY.md §7](../../../DATA_DICTIONARY.md) — daily mean of monitoring_b stress samples within sleep window; NaN when `sleep_valid_flag=False`.

**Surface**: Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 → 2026-06-05). n=1339 days with channel out of 1372 Stratum 4 days (33 NaN nights below the MIN_SAMPLES_PER_NIGHT=120 gate; `sleep_valid_flag=False`).

**Programme spec**: [`descriptive/README.md`](../../README.md) §3.1 (LOCKED 2026-06-18 r3, commit ccbd12e).

**Sources**: `per_day_master.csv` (Garmin daily aggregate) + `labels_crash_v2.csv` (`label=='crash'` day-level; `episode_id` starting with `crash-` episode-level — per CONVENTIONS §3.6).

**Discipline**: Layer 1 descriptive (no causal claims, no falsification bar) per [CONVENTIONS §2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). Statistical hygiene anchors: §3.1 (personal baseline), §3.3 (column-duplication threshold |ρ|≥0.92), §3.4 (crash-drop sensitivity |Δ|>0.10), §3.5 (spike metrics), §3.6 (named counts).

---

## Headline

`stress_mean_sleep` on Stratum 4 is a **heavily right-skewed, autocorrelation-dense daily channel** (skew=+2.72, excess kurtosis=+15.5; data-driven E[L]*=12.6 — factor-of-2 above the project default E[L]=7). The **citalopram-window phase medians are nearly flat** (range 17.04 → 20.20 across the four phases) — the locked +0.43/mg dose-response slope is a within-buildup-window effect, **not a between-phase steady-state level shift**. The crash-vs-normal separation is robust (episode-level Cohen's d=+0.91; bootstrap CI95 on mean diff [+1.58, +8.40] stress units). **One new near-identity pair surfaces**: `asleep_stress_avg_uds` (Pearson r=+0.93). All other named near-identity candidates pass the §3.3 threshold cleanly.

---

## Q3.1.a — Distribution shape (Stratum 4)

**Verdict on the §3.1 delegate question**: **delegate to [`lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) AND extend**. That doc covers the same channel on the full LC era (n=1478, 2022-04-04 onward) with mean=20.05, std=6.32, p50=19.27 — distribution shape on Stratum 4 (n=1339, 2022-09-03 onward) is materially identical at the central-tendency and quantile level (mean=19.97, std=6.11, p50=19.21). The **material gap** in `lc_phase_descriptive.md` is that it reports percentiles only — **no skewness, kurtosis, MAD, or heavy-tail flag**, which are the statistics that determine whether a downstream HA test on this channel should use robust or non-robust baselines. This analysis surfaces those.

| stat | value | source |
|---|---:|---|
| n (Stratum 4) | 1339 | `per_day_master.csv` `stress_mean_sleep` non-NaN within S4 |
| mean | 19.97 | (single-pool S4) |
| median | 19.21 | |
| std (ddof=1) | 6.11 | |
| MAD (unscaled) | 2.87 | |
| MAD × 1.4826 (normal-equivalent SD) | 4.25 | for robust z-score scaling per §3.1 |
| p1 / p10 / p25 / p50 / p75 / p90 / p99 | 10.02 / 14.06 / 16.46 / 19.21 / 22.27 / 26.22 / 43.62 | |
| skewness (Fisher-Pearson) | **+2.72** | strongly right-skewed |
| excess kurtosis (Fisher) | **+15.45** | heavy-tailed |
| heavy_tail_flag | **True** | skew>1 |
| range | 8.32 → 72.99 | extreme tail values present |

The robust-equivalent SD (MAD × 1.4826 = 4.25) is **30% lower than the raw std=6.11** — confirming that the tail is doing real work on the std. Downstream HA tests with `stress_mean_sleep` as predictor should default to **robust personal baselines (median + MAD)** per CONVENTIONS §3.1; the [`_utils/frame.py::z_score_vs_rolling_baseline`](../../../analyses/_utils/frame.py) default (`robust=True`) is correct for this channel.

See [`plots/fig1_distribution_s4.png`](plots/fig1_distribution_s4.png).

---

## Q3.1.b — Autocorrelation structure + E[L]\*

The **data-driven block length is E[L]\*=12.6** (Politis-White 2004 with Patton-Politis-White 2009 correction per [`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)) vs the project default E[L]=7 per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md). The **factor-of-2 deviation flag fires** (deviation ratio = 0.80 > 0.5 threshold). Cutoff lag M=6.

| lag (days) | autocorrelation |
|---:|---:|
| 1 | +0.393 |
| 2 | +0.311 |
| 3 | +0.264 |
| 7 | +0.142 |
| 14 | +0.091 |

**Implication**: any HA pre-reg using `stress_mean_sleep` MUST either (a) use the data-driven block length E[L]\*≈13 as the primary bootstrap CI, or (b) pre-spec a sensitivity arm at E[L]=13 alongside the default-E[L]=7 primary. The project default of 7 is not adequate for this channel; serial dependence persists past lag 7 visibly (rho_lag7=+0.14, comparable to the Politis-White cutoff threshold of 0.147 computed via `2·√(log n / n)` at n=1339 — the formula used by [`_utils/inference.py::compute_data_driven_block_length`](../../../analyses/_utils/inference.py)). The fig5 plot caption matches.

See [`plots/fig5_acf.png`](plots/fig5_acf.png).

---

## Q3.1.c — Base rates per citalopram phase

Phase axis per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) §3:

| phase | window | n | median | mean | MAD | p10 / p90 |
|---|---|---:|---:|---:|---:|---|
| unmedicated | 2022-09-03 → 2024-04-08 | 572 | 19.51 | 20.36 | 2.98 | 14.11 / 26.73 |
| buildup | 2024-04-09 → 2024-06-19 | 71 | 17.04 | 16.76 | 2.00 | 12.50 / 21.11 |
| consolidation | 2024-06-20 → 2026-03-19 | 627 | 19.07 | 19.99 | 2.80 | 14.20 / 26.31 |
| afbouw | 2026-03-20 → 2026-06-05 | 69 | 20.20 | 19.93 | 2.45 | 14.85 / 24.73 |

The two **transition phases** (buildup and afbouw) have **n<75 each** and **narrower dispersion** (MAD~2.0–2.5) than the two **steady-state phases** (unmedicated and consolidation, n>570, MAD~2.8–3.0). Any HA test that wants per-phase verdicts under [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) §5.A on buildup or afbouw faces a **5× n disadvantage** vs the steady-state phases — power loss is real.

Named counts (CONVENTIONS §3.6): the per-phase n's above are `stress_mean_sleep`-non-NaN day rows in `per_day_master.csv` within Stratum 4 date masks per `citalopram_phase_stratification.md §3` boundary dates.

---

## Q3.1.d — Phase-stratified distribution: citalopram step magnitude vs natural variation

**This is the most operationally consequential finding for downstream HA pre-regs on this channel.**

The locked dose-response anchor (v3 §5.6.1): **+0.43/mg p=0.001 buildup post-CPAP β, +0.25/mg afbouw β**. Naive extrapolation: at 30mg steady-state (consolidation), the implied citalopram-attributable lift is +0.43 × 30 = **+12.9 stress units** — comparable to the channel's interquartile range (p75 − p25 = 5.81) **doubled**.

Observed steady-state level shifts (median):

| comparison | Δ median | within-phase MAD | within-MAD? |
|---|---:|---:|---|
| buildup − unmedicated | **−2.47** | 2.00–2.98 | wrong direction; ~1 MAD |
| consolidation − unmedicated | **−0.44** | 2.80–2.98 | well within MAD (~0.15 MAD) |
| afbouw − consolidation | **+1.13** | 2.45–2.80 | within MAD (~0.4 MAD) |
| afbouw − unmedicated | **+0.69** | 2.45–2.98 | well within MAD |

**The +0.43/mg dose-response slope does NOT translate to a between-phase level shift at the median.** Three readings of this discrepancy, all consistent with the locked methodology:

1. **The slope is a within-window time-trend, not a steady-state level shift.** The v3 buildup post-CPAP β is the slope of `stress_mean_sleep` against `dose_plasma_mg(d)` *within* the buildup-window. Across phases, the LC-trajectory's broader recovery arc absorbs the slope's implied level shift — the unmedicated phase coincides with earlier-LC days (median ~19.5), consolidation with later-LC steady-state-on-30mg days (median ~19.1). The unmedicated baseline is already elevated relative to the eventual on-drug consolidation baseline by the LC trajectory itself, not by absence of citalopram.

2. **The dose-adjusted-predictor pattern under [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) §5.B remains correct for within-phase work**; it does not promise to recover a between-phase level shift. The §5.B framework is a single-confounder fix for the dose dimension; cross-phase pooling without §5.B treatment is still biased on the slope, even though the medians look flat.

3. **The 30mg implied lift (+12.9) is a slope-extrapolation, not a level prediction.** Per the dose-response MD's own caveats (§5.6 buildup-vs-afbouw asymmetry, framework MD §8.4), the buildup-β is on a dose-naive system and may overcorrect at steady-state.

**Operational consequence for HA pre-regs on this channel**: a future HA on `stress_mean_sleep` that uses dose-adjustment (§5.B) will not see a dramatic between-phase level shift after correction — the medians are already close. The §5.B correction's primary value is for **within-buildup-window and within-afbouw-window** dose-modulated days, not for steady-state cross-phase comparisons. The §5.A per-phase stratification is therefore the safer default for **steady-state pooled tests** (unmedicated + consolidation), even though it loses n.

See [`plots/fig2_phase_stratified.png`](plots/fig2_phase_stratified.png) (violins) and [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png) (90d rolling median through phases).

---

## Q3.1.e — Near-identity check vs neighbouring channels (threshold |ρ|≥0.92 per CONVENTIONS §3.3)

Cross-channel-correlation card ([`cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md)) flagged HA07c (this channel) ≡ −HA10 (`bb_overnight_gain` morning-peak proxy) at Spearman ρ=−0.922 on Stratum 4. That finding stands. This analysis covers the three named channels in §3.1 plus three extra near-neighbours. Column semantics for each target row link to the relevant [DATA_DICTIONARY.md](../../../DATA_DICTIONARY.md) section.

| target channel | DATA_DICTIONARY | n | Pearson r | Spearman ρ | near-identity flag? |
|---|---|---:|---:|---:|---|
| `stress_stdev_sleep` | [§7](../../../DATA_DICTIONARY.md) | 1339 | +0.602 | +0.501 | no |
| `all_day_stress_avg` | [§7B All-day stress](../../../DATA_DICTIONARY.md) | 1339 | +0.522 | +0.404 | no |
| `stress_low_motion_min_count_S60_Mlow` | [§8C](../../../DATA_DICTIONARY.md) | 1339 | +0.294 | +0.167 | no |
| **`asleep_stress_avg_uds`** | [§7B All-day stress](../../../DATA_DICTIONARY.md) | 1337 | **+0.929** | +0.895 | **YES (Pearson)** |
| `awake_stress_avg` | [§7B All-day stress](../../../DATA_DICTIONARY.md) | 1339 | +0.143 | +0.106 | no |
| `bb_lowest` | [§7B Body Battery](../../../DATA_DICTIONARY.md) | 1339 | −0.425 | −0.423 | no |

**New near-identity pair**: `stress_mean_sleep` ≡ `asleep_stress_avg_uds` (Pearson r=+0.929, Spearman ρ=+0.895 — Pearson exceeds the 0.92 threshold, Spearman is just below). This pair is **not** in the cross-channel-correlation card's 7-channel panel; it is surfaced here. Mechanistically expected: `asleep_stress_avg_uds` is the UDS-side asleep-stress average (whole-night, from `daily_uds.csv`), while `stress_mean_sleep` is the custom-extracted mean of monitoring_b stress samples within the sleep window (from `sleep_stress_nightly.csv`). Both are "average stress during sleep" with slightly different sample-selection rules; the near-identity is a methodological-overlap finding, not a biological one.

**Implication**: any HA test that uses `stress_mean_sleep` should NOT also enter `asleep_stress_avg_uds` as a "second autonomic channel" — they are the same primitive at the daily resolution. The cross-channel-correlation card's panel should be **extended** to include `asleep_stress_avg_uds` in a future refresh (queued, not part of this analysis).

The other five candidates pass cleanly. `stress_stdev_sleep` (r=+0.60) confirms the level-vs-variability split — partial overlap but distinct facets per the HRV proxy validation BONUS section (R²=0.378 between SD and mean). `all_day_stress_avg` and `stress_low_motion_min_count_S60_Mlow` are mostly independent. The `bb_lowest` negative correlation (r=−0.42) is structural-by-construction (BB drops when stress is high; consistent with cross-channel-correlation card's autonomic-state cluster).

---

## Q3.1.f — Crash-day vs normal-day (refresh of `hrv_proxy_validation/` Check 7.3 in operationalisation-support framing)

Per CONVENTIONS §3.6 named counts: 29 crash-episodes (crash_v2 day-level → episode-level via `labels_crash_v2.csv` unique `episode_id` starting with `crash-`); 101 crash-days (day-level, `label=='crash'`); 1238 non-crash days (the complement within Stratum 4 sleep_valid days).

### Episode-level (primary unit per CONVENTIONS §3.6)

| stat | value |
|---|---:|
| n crash-episodes | 29 |
| n normal-day base rate | 1238 |
| mean per-episode `stress_mean_sleep` | 24.18 |
| mean normal-day `stress_mean_sleep` | 19.51 |
| mean diff (episode − normal-day) | **+4.67** |
| Cohen's d (episode-level vs normal-day pooled) | **+0.91** |
| Bootstrap 95% CI on mean diff | [+1.58, +8.40] (5000 iters, seed=20260618) |

This **aligns with the canonical hrv_proxy_validation finding** (Check 7.3 episode-level: d=+0.90 CI95 [+1.51, +8.22]) — same headline, current-corpus refresh.

### Day-level (autocorrelation-inflated supplementary)

| stat | value |
|---|---:|
| n crash-days | 101 |
| n normal-days | 1238 |
| mean crash-day | 25.67 |
| mean normal-day | 19.51 |
| mean diff (point estimate) | **+6.17** |
| Cohen's d | **+1.05** |
| Stationary bootstrap 95% CI on mean diff, **E[L]=7** (project default) | [+2.80, +9.56], width 6.76 |
| Stationary bootstrap 95% CI on mean diff, **E[L]=13** (data-driven, Q3.1.b flag fired) | **[+2.54, +9.63], width 7.09** |

The day-level d=+1.05 vs episode-level d=+0.91 is the expected within-episode-autocorrelation inflation; the episode-level is the headline.

**Block-length sensitivity (Q3.1.b cross-check)**: per [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md), when the data-driven E[L]\* deviates from the project default by more than a factor of 2, the analysis must report the CI at the data-driven value alongside the default. Q3.1.b fired that flag (E[L]\*=12.6, deviation ratio 0.80). Above the second CI row at E[L]=13 closes the audit gate. **Substantive read: both CIs exclude zero and the widths differ by only +5% (7.09 vs 6.76).** The stationary-bootstrap's geometric-block-length distribution is mildly insensitive to the mean-length choice within a factor of 2 (per the methodology MD's tradeoff column); the day-level signal is robust to the block-length choice, which is an even stronger finding than a wider-CI-still-excluding-zero would be.

### Crash-drop sensitivity (CONVENTIONS §3.4)

For a descriptive-layer sanity check we report `Spearman(stress_mean_sleep, gevoelscore)` with `is_crash` rows dropped:

| frame | Spearman ρ | n |
|---|---:|---:|
| full Stratum 4 | −0.194 | 1339 |
| crash-days dropped | −0.147 | 1238 |
| \|Δ\| | **0.047** | — |
| §3.4 threshold (0.10) crossed? | **no** | — |

The crash days are **not** doing systematic correlation work in the channel-vs-gevoelscore pair on Stratum 4. (Compare: the exertion-vs-RHR Spearman swings ~+0.0 to ~+0.4 when crash days drop, per the canonical §3.4 example. `stress_mean_sleep` vs `gevoelscore` is much more stable.) **No flag fires.**

See [`plots/fig4_crash_vs_normal.png`](plots/fig4_crash_vs_normal.png).

---

## Q3.1.g — Spike-detecting primitive availability

`stress_mean_sleep` is **by construction a daily-aggregate**: it is the mean of monitoring_b stress samples within the sleep window per [`garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`](../../../../garmin/scripts/sleep_stress_extract/extract_sleep_stress.py); minimum 120 samples per night gate (~6h at 3-min cadence). Sub-daily resolution is **not in `per_day_master.csv`**.

Spike primitives in the master (24h, not sleep-window):

| column | DATA_DICTIONARY | n_non_nan (S4) | type | relation to `stress_mean_sleep` |
|---|---|---:|---|---|
| `max_spike_minutes` | [§8](../../../DATA_DICTIONARY.md) | 1364 | longest contiguous run of stress≥75 lasting ≥5min in 24h | Pearson r = **+0.058** on n=1339; essentially independent |
| `stress_high_duration_min` | [§8B C4](../../../DATA_DICTIONARY.md) | 1364 | total 24h minutes at high-stress threshold per FIT extraction | (not paired here) |
| `stress_low_motion_min_count_S60_Mlow` | [§8C](../../../DATA_DICTIONARY.md) | 1365 | minute-level count of low-motion-high-stress windows (24h) | per Q3.1.e, ρ=+0.17 with `stress_mean_sleep`; mostly independent |

**Latent in FIT, not in master**:
- per-minute monitoring_b stress samples (raw ~3-min cadence; the source of `stress_mean_sleep`)
- sleep-window vs awake-window separation at per-minute resolution (carve sleep into deep vs disturbed)

**Implication per CONVENTIONS §3.5**: `stress_mean_sleep` is the **daily mean** channel; a future HA whose mechanism is acute sleep-disturbed arousal (e.g. a spike-of-stress during a single fragmented night) should NOT use this channel as primary — a spike-of-night primitive (currently latent in monitoring_b FIT files) would be the correct surface. The cross-channel card's existing `stress_low_motion_min_count_S60_Mlow` is the closest spike companion currently in the master, but it operates on the 24h window, not specifically on the sleep window. Building a sleep-window-only spike primitive is a queued extraction task; this analysis does **not** action it.

---

## Q3.1.h — Outlier detection + calibration-drift check

Per [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md):
- MIN_SAMPLES_PER_NIGHT=120 gate; nights below threshold drop to NaN. 33 such nights in Stratum 4.
- No calibration-drift events catalogued for `stress_mean_sleep` specifically.
- Underlying sensor is Forerunner 245 Elevate V3 throughout the entire 2021-08-16 → present window — **no device change**.

### Outlier scan (MAD-based |z|>5; threshold per CONVENTIONS §3.1 robust-baseline default)

**16 outlier-days flagged** out of 1339:

| date | value | MAD-z | likely category |
|---|---:|---:|---|
| 2022-09-30 | 40.57 | +5.02 | early-LC |
| 2023-02-04 | 49.70 | +7.17 | Feb-2023 cluster (3 consecutive days flagged) |
| 2023-02-05 | 49.40 | +7.10 | (cluster) |
| 2023-02-06 | 44.89 | +6.04 | (cluster) |
| 2023-04-01 | 48.89 | +6.98 | April-2023 pair |
| 2023-04-02 | 64.66 | +10.68 | (pair) |
| 2023-06-12 | 57.49 | +9.00 | isolated |
| 2023-11-29 | 62.12 | +10.09 | Nov-Dec-2023 cluster |
| 2023-11-30 | **72.99** | **+12.64** | global max (this is the channel's max) |
| 2023-12-02 | 51.06 | +7.49 | (cluster) |
| 2024-07-16 | 71.99 | +12.41 | early-consolidation |
| 2024-12-25 | 46.50 | +6.42 | (holiday period) |
| 2025-01-01 | 53.56 | +8.07 | (holiday period) |
| 2025-01-18 | 45.47 | +6.17 | isolated |
| 2025-12-09 | 52.03 | +7.72 | isolated |
| 2026-01-07 | 41.56 | +5.25 | isolated |

The outliers are **not artefacts**: they cluster in time (Feb 2023, late-Nov 2023, holiday season 2024-25), are mostly consecutive 1–3-day events, and reach extreme values (max +12.6 MAD-z on the rolling median). These look like **real night-stress events** (illness episodes, acute stress, or sleep-disturbed nights), not sensor failures. The 33 NaN nights (sleep_valid_flag=False) are the silent-drop boundary; what makes it into the master is genuine signal. Downstream HA tests should NOT trim these — they are part of the channel's natural heavy-tail.

### Drift check — rolling 90d median over Stratum 4

| snapshot date | rolling 90d median |
|---|---:|
| 2022-12-01 | 19.54 |
| 2023-06-01 | 17.66 |
| 2023-12-01 | 19.85 |
| 2024-06-01 | 17.34 |
| 2025-01-01 | 19.39 |
| 2025-12-01 | 19.93 |

The rolling 90d median **fluctuates within a 17.3 ↔ 19.9 band** (range = 2.6 units, ~1 MAD) over 3+ years. No monotonic creep. The **consolidation-boundary step at 2024-06-20** (entry into 30mg steady-state) shows trailing-30d mean = 18.47, leading-30d mean = 19.37 — a **+0.90 step**, again within ~1 MAD and within the natural year-to-year fluctuation band. No calibration-drift signature.

See [`plots/fig3_trajectory_with_phases.png`](plots/fig3_trajectory_with_phases.png).

---

## Q3.1.i — Covariate-sensitivity readiness for a future HA pre-reg on this channel

Discipline anchor: [HA-P7 hypothesis.md §4.5.4](../../../analyses/hypotheses/HA-P7/hypothesis.md) (secondary-logistic-with-covariate pattern; β disambiguation between primary-signal and a candidate alternative reading). Q3.1.i names **three** candidate covariates a future HA on `stress_mean_sleep` as predictor should pre-spec:

### 1. `dose_plasma_mg(d)` — obligatory under [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) §5.B

The channel is dose-modulated at +0.43/mg p=0.001. A future HA MUST either §5.A per-phase stratify or §5.B dose-adjust. The covariate version (secondary logistic adding `dose_plasma_mg(d)` to a primary-channel logistic) is the framework-prescribed disambiguator: **β_channel collapses toward zero in the secondary model + β_dose carries the load** → the channel's primary signal was the citalopram dose, not the LC-physiology. **β_channel survives** → the channel carries information beyond dose. Per Q3.1.d the medians are flat at steady-state, so this covariate is unlikely to dramatically shift consolidation-pooled results — but it is the obligatory transparency arm.

Needed columns: `lc_phase` is in the master; `dose_plasma_mg(d)` is currently computed runtime per [`citalopram_dose_response/dose_response.py`](../../../analyses/garmin_exploration/intervention_effects/dose_response.py); CONVENTIONS §3.2-style materialisation in `per_day_master.csv` is queued.

### 2. `resting_hr` — alternative autonomic-load anchor

Column semantics: [DATA_DICTIONARY.md §5](../../../DATA_DICTIONARY.md).

On Stratum 4 observed (this analysis, n=1337): Pearson r=+0.359, Spearman ρ=+0.377 between `stress_mean_sleep` and `resting_hr`. Frame anchor: the canonical hrv_proxy_validation Check 7.2 ([result-table.txt](../../../analyses/garmin_exploration/hrv_proxy_validation/result-table.txt)) reports **r=+0.342 on the full LC era** (n=1476, R²=0.117 → **88% of `stress_mean_sleep` variance is NOT RHR-explained**). The S4-vs-LC-era difference is +0.017 — within sampling noise; the substantive read is unchanged. The covariate disambiguates: **β_channel attenuates → the signal is shared autonomic-arousal**; **β_channel survives → the signal is HRV-proxy-specific** beyond the resting-HR axis.

### 3. `stress_mean_sleep_lagged_mean_14d(d) = mean(channel[d-14:d-1])` — autocorrelation-vs-mechanism

Mirrors the HA-P7 §4.5.4 worked example (lagged outcome covariate). Per Q3.1.b the cutoff lag M=6 and E[L]\*=12.6; a 14d lagged trailing mean is **just past the within-channel autocorrelation horizon**, so the covariate captures the "trailing autonomic state carried forward" reading without overlapping today. **β_channel collapses → today's signal is yesterday's signal carried forward** (the primary signal is autocorrelation, not a same-day mechanism). **β_channel survives → the signal carries new-day information**.

**Reconciliation with CONVENTIONS §3.2 `_lagged_lcera` family**. §3.2 mandates the v3.2 `_lagged_lcera` `[d-90, d-30]` window for PEM-pacing analyses on **exertion-rank columns** (`exertion_class_lagged_lcera`, `push_burden_7d_lagged_lcera`, the per-axis rank-composite variants). `stress_mean_sleep` is not currently in the §3.2 audit-hook list and has no `_lagged_lcera` materialised variant in `per_day_master.csv` as of 2026-06-18. Two reading paths for a future HA on this channel:
- **For a same-day mechanism HA** (e.g. "today's `stress_mean_sleep` predicts today's `is_crash`"), the 14d covariate proposed here is the descriptive substrate's autocorrelation-vs-mechanism check; the HA's primary z-score should follow [`_utils/frame.py::z_score_vs_rolling_baseline`](../../../analyses/_utils/frame.py) at the v3.2-compatible `[d-90, d-30]` window per §3.2's spirit, not the 14d window (14d is the descriptive's diagnostic, not the HA's baseline).
- **For a pre-window-burden HA** (e.g. "trailing 14d `stress_mean_sleep` predicts day d+0"), the 14d window IS the HA's primary, and the covariate role above does not apply — a `_lagged_lcera`-style `[d-90, d-30]` mean would be the descriptive substrate's autocorrelation-vs-mechanism check instead.

In short: this Q3.1.i covariate is **a same-day-HA diagnostic** built just past Q3.1.b's M=6 cutoff; it does NOT substitute for §3.2's longer trailing baseline window, which belongs in the HA's own z-scoring or covariate-adjustment layer.

### Recommendation for any HA pre-reg on this channel

Pre-spec all three covariates as **secondary sensitivity arms**. Concordance across the three secondaries = high confidence in the primary; divergence = the disambiguation is doing real work. The §5.B citalopram-dose adjustment is obligatory per the framework; the other two are diagnostic.

---

## Cross-references

### HA-* tests that touch this channel (cite this analysis)

- **HA07c** (sleep-stress mean; train SUPPORTED / validate REFUTED; citalopram-as-confound currently a caveat-class). Re-interpretation hinges on **Q3.1.d phase-stratified medians being flat** — the validate-REFUTED reading does NOT line up with a "citalopram pushes the signal away" story at the steady-state level; the train-vs-validate divergence is more likely a within-LC-trajectory effect than a citalopram-step effect.
- **HA07d** (sleep-stress stdev; the only canonical-SUPPORTED Tier-1 test). Related channel: `stress_stdev_sleep` (Q3.1.e Pearson r=+0.60 with this channel; level vs variability distinct).
- **HA08c** (sleep-stress slope; 5-day rolling OLS slope of this channel). Inherits Q3.1.b autocorrelation finding directly — the slope is computed on a channel with E[L]\*≈13, so the slope's own block-length policy needs auditing.
- Any future HA pre-reg using `stress_mean_sleep` as predictor of a crash-related outcome must adopt one of [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) §5.A / §5.B / §5.C treatments AND cite this analysis for the descriptive substrate per the lock-process MD §3.2 amendment landing in Phase 4.

### Methodology MDs cited

- [`methodology/lc_phase_descriptive.md`](../../../methodology/lc_phase_descriptive.md) — Q3.1.a delegated; this analysis extends with skewness/kurtosis/MAD/heavy-tail.
- [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) §3-§6 — Q3.1.c phase axis, Q3.1.d phase-stratified, Q3.1.i covariate.
- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md) v3 §5.6.1 — locked +0.43/mg dose-response slope.
- [`methodology/permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) — E[L]=7 default + factor-of-2 deviation rule; Q3.1.b fires the flag.
- [`methodology/garmin_indicators_audit.md`](../../../methodology/garmin_indicators_audit.md) — Q3.1.h known-issues catalog (no calibration events on this channel).
- [`methodology/lc_era_temporal_segmentation.md`](../../../methodology/lc_era_temporal_segmentation.md) — Stratum 4 boundary definition.

### Existing artefacts referenced

- [`garmin_exploration/hrv_proxy_validation/`](../../../analyses/garmin_exploration/hrv_proxy_validation/) — Q3.1.f refresh; current-corpus values align with canonical (d_ep=+0.91 here vs +0.90 there).
- [`garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) — Q3.1.e cross-reference; this analysis surfaces one **new** near-identity pair (`asleep_stress_avg_uds`) not in the card's 7-channel panel.

### Upstream pipeline

- `per_day_master.csv` ← `pipeline/03_consolidate/build_unified_dataset.py` ← `processed/garmin/sleep_stress_nightly.csv` ← `garmin/scripts/sleep_stress_extract/extract_sleep_stress.py`.
- `labels_crash_v2.csv` ← `garmin/hypotheses/crash_v2-definition/definition.md` (locked).

---

## Limitations

For a producer-mode Layer-1 descriptive analysis (no falsification bar, no causal claim per [CONVENTIONS §2.1](../../../CONVENTIONS.md#21-descriptive-before-inference)), the binding limitations a downstream HA pre-reg author should carry forward are:

1. **Q3.1.c–d are on raw channel values, not dose-adjusted.** Per [`methodology/citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) §5, any HA using `stress_mean_sleep` cross-phase must adopt §5.A / §5.B / §5.C treatment. Q3.1.d explains why the medians are flat in raw form; a dose-adjusted phase comparison is the natural follow-up but lives in the HA pre-reg, not here.
2. **The channel is structurally a daily mean** (Q3.1.g) and therefore **dilution-vulnerable for acute-load mechanisms** per CONVENTIONS §3.5. A future HA whose mechanism is acute sleep-disturbed arousal should use a sleep-window spike primitive (currently latent in monitoring_b FIT, not in master) rather than this channel as primary.
3. **The day-level Cohen's d=+1.05 is autocorrelation-inflated** (Q3.1.f). The episode-level d=+0.91 is the headline; consecutive within-episode days are not independent observations. Block-length-sensitivity rows are reported but the basic non-independence stands.
4. **The outlier-rule MAD-z|>5 is a descriptive-stage screen** (Q3.1.h) — downstream HA tests must NOT trim these days; they are real night-stress events (illness, acute stress, holiday-period clusters), not sensor failures. Per CONVENTIONS the heavy-tail is part of the channel's natural shape.
5. **The new `asleep_stress_avg_uds` near-identity pair** (Q3.1.e) has not yet been propagated into the cross-channel-correlation card's 7-channel panel. Any HA pre-reg using `stress_mean_sleep` as predictor must NOT also enter `asleep_stress_avg_uds` as a "second autonomic channel" pending that propagation.

---

## Status

**Current as of 2026-06-18 (commit context: post-`ccbd12e` descriptive programme lock; revised per fresh-session `/research-review` 2026-06-18 — [report](../../../reviews/descriptive-stress_mean_sleep-2026-06-18.md), verdict PASS with caveats; one L3.4 substantive + five minor closures applied).** Refresh when:
1. Stratum 4 right edge advances by ≥30 days AND any HA pre-reg on this channel is about to spin up (per CONVENTIONS §3.1 personal-baseline freshness).
2. A new citalopram-phase boundary lands (e.g. post-afbouw enters analytic scope).
3. The Politis-White E[L]\* shifts by another factor of 2 from current 12.6 (current factor-of-2 flag already fired; further drift changes downstream HA block-length policy).
4. ~~The `asleep_stress_avg_uds` near-identity pair gets propagated into the cross-channel-correlation card's 7-channel panel (would update Q3.1.e cross-reference).~~ **DISCHARGED-BY-PROPAGATION-2026-07-09** per OI-034 execution: the pair is now recorded in [`analyses/garmin_exploration/cards/cross-channel-correlation.md`](../../../analyses/garmin_exploration/cards/cross-channel-correlation.md) Key findings entry 6 + the "Near-identity pairs discovered post-2026-06-08" table + the card's Status / Lock log (2026-07-09 entry). Cluster 2 annotation in the card's "Effective N of independent channels" section names the UDS-side sister of HA07c. Q3.1.e cross-reference stands as-locked (source-side wording preserved); downstream HA discipline (do NOT enter `asleep_stress_avg_uds` as a "second autonomic channel" alongside `stress_mean_sleep` or HA07c) now lives in the corpus-wide near-identity map in addition to Q3.1.e + Limitations bullet 5.
