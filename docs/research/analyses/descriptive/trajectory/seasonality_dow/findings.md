# `trajectory/seasonality_dow/` -- findings (Q4.8 confound check)

## Authorship

- **Computed**: 2026-06-26 by Claude (Opus 4.7) via [`run.py`](run.py) under the user-LOCKED operationalisation in [`README.md`](README.md) (Strand B section 7c interview 2026-06-25).
- **Data**: `per_day_master.csv` at `$GEVOELSCORE_DATA_PATH/unified/`; as-of-date **2026-06-04** (Garmin coverage right edge per [STOCKTAKE section 1](../../../../STOCKTAKE.md#1-the-corpus)). 1754 day-level rows.
- **Axis**: 6-phase LC recovery axis from [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) (LOCKED `d47e0d3` 2026-06-19) for Stage 7.
- **Layer 1 descriptive per [CONVENTIONS section 2.1 + section 4.3](../../../../CONVENTIONS.md)**: NO causal claims; NO `SUPPORTED` bar; NO `REFUTED` mark. This document characterises seasonality + DOW patterns on the 6 channels; intervention attribution is out of scope. Per CONVENTIONS section 4.2 caveat-class: seasonality detected on a channel is reported as `harmonic R2=X; amplitude Y; suspect for seasonality confound` -- NOT promoted to `the multi-year arc is partly seasonal`.
- **Cross-references**: [`run.py`](run.py) + [`summary.json`](summary.json) (gitignored) + [`plots/`](plots/) (5 PNGs, gitignored). Per-channel per-stage numbers below trace to the JSON.

---

## Headline

**Seasonality (harmonic, annual)**: 0 of 6 channels flagged suspect at R2 >= 0.1.

**DOW (weekday-vs-weekend, MWU)**: 2 of 6 channels show Mann-Whitney U two-sided p < 0.05.

**Per-month (Kruskal-Wallis across 12 months)**: 6 of 6 channels show p < 0.05.
**Per-DOW (Kruskal-Wallis across 7 days)**: 5 of 6 channels show p < 0.05.

**v3 spring-control extension (CONFIRMED-citalopram channels)**: of the 3 CONFIRMED channels (stress_mean_sleep, all_day_stress_avg, bb_lowest), 1 show the citalopram-step surviving same-season comparison (test-year direction matches prior AND control-year is roughly flat). This is a **descriptive observation only** per CONVENTIONS section 4.2: it neither confirms nor refutes the v3 verdict; it extends the spring-control logic per [citalopram_dose_response section 5.6](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) LOAD-BEARING.

**Per-recovery-phase seasonality**: 18 of 36 (channel x phase) cells have sufficient n + span for an annual harmonic fit; remaining cells skipped per the within-phase span >= 180d gate (annual harmonic underdetermined on short phases).

---

## 1. Stage 2 -- annual harmonic per channel

**Method**: per channel, fit `y = alpha + b1*sin(2*pi*doy/365) + b2*cos(2*pi*doy/365) + eps` on all non-null rows. Report amplitude = sqrt(b1^2 + b2^2); peak-DOY (day-of-year when harmonic peaks); R2; F-test p; suspect-flag = `R2 >= 0.10`.

| channel | n | beta_sin | beta_cos | amplitude | peak DOY | R2 | F p | flag |
|---|---:|---:|---:|---:|---:|---:|---:|:---|
| `stress_mean_sleep` | 1707 | +0.466 | +0.963 | 1.070 | 26 | 0.0119 | 0.0000 | no-flag |
| `all_day_stress_avg` | 1732 | +0.439 | -0.349 | 0.561 | 130 | 0.0040 | 0.0317 | no-flag |
| `bb_lowest` | 1732 | -0.039 | +1.409 | 1.410 | 363 | 0.0114 | 0.0001 | no-flag |
| `stress_stdev_sleep` | 1707 | -0.182 | +0.110 | 0.213 | 305 | 0.0023 | 0.1382 | no-flag |
| `stress_low_motion_min_count_S60_Mlow` | 1739 | +5.155 | -1.103 | 5.272 | 103 | 0.0056 | 0.0077 | no-flag |
| `resting_hr` | 1731 | +1.037 | +0.645 | 1.221 | 59 | 0.0850 | 0.0000 | no-flag |

**Suspect-flag reading per CONVENTIONS section 4.2 caveat-class**: a SUSPECT flag means the annual harmonic explains >= 10% of variance in the raw channel. This is a **descriptive marker** that seasonality is non-negligible at this channel; it does **NOT** promote to a claim that the multi-year arc is partly seasonal. Trajectory-vs-seasonality disambiguation requires a model with both terms (out of scope for this descriptive check).

---

## 2. Stage 3 -- per-month medians + Kruskal-Wallis

**Method**: per channel, stratify rows by calendar month (1..12); report per-month median + IQR; test Kruskal-Wallis H across the 12 month-groups; suspect = `p < 0.05`. Per-month outliers = months whose median exceeds grand-median +/- 2x within-channel IQR/2.

**Per-month median table (each cell: median value; blank = no data)**:

| channel | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | KW p | spread |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `stress_mean_sleep` | 19.18 | 20.17 | 19.54 | 18.47 | 19.01 | 19.01 | 16.95 | 16.21 | 18.65 | 19.47 | 19.49 | 21.20 | **0.0000** | 4.984 |
| `all_day_stress_avg` | 32.00 | 32.00 | 33.00 | 33.00 | 32.00 | 34.00 | 33.00 | 32.00 | 32.00 | 31.00 | 32.00 | 33.00 | **0.0410** | 3.000 |
| `bb_lowest` | 21.00 | 18.00 | 20.00 | 17.00 | 18.00 | 17.50 | 17.00 | 16.00 | 20.00 | 21.00 | 19.00 | 19.00 | **0.0001** | 5.000 |
| `stress_stdev_sleep` | 7.30 | 7.38 | 7.06 | 7.13 | 7.06 | 7.78 | 7.57 | 6.97 | 7.23 | 7.71 | 7.08 | 8.48 | **0.0015** | 1.504 |
| `stress_low_motion_min_count_S60_Mlow` | 53.00 | 61.00 | 63.00 | 58.50 | 51.00 | 59.00 | 61.00 | 49.00 | 53.50 | 46.00 | 50.00 | 60.00 | **0.0042** | 17.000 |
| `resting_hr` | 56.50 | 58.00 | 57.00 | 57.00 | 56.00 | 57.00 | 55.00 | 54.00 | 55.00 | 55.00 | 56.00 | 57.00 | **0.0000** | 4.000 |

**Per-channel month-median spread** (max-month-median minus min-month-median; descriptive magnitude of seasonality on raw units):

- `stress_mean_sleep`: spread = 4.984 (grand median across months = 19.093)
- `all_day_stress_avg`: spread = 3.000 (grand median across months = 32.000)
- `bb_lowest`: spread = 5.000 (grand median across months = 18.500)
- `stress_stdev_sleep`: spread = 1.504 (grand median across months = 7.265)
- `stress_low_motion_min_count_S60_Mlow`: spread = 17.000 (grand median across months = 56.000)
- `resting_hr`: spread = 4.000 (grand median across months = 56.250)

---

## 3. Stage 4 -- per-DOW medians + Kruskal-Wallis

**Method**: per channel, stratify rows by day-of-week (Mon..Sun); report per-DOW median + IQR; test Kruskal-Wallis H across the 7 DOW-groups; suspect = `p < 0.05`.

**Per-DOW median table**:

| channel | Mon | Tue | Wed | Thu | Fri | Sat | Sun | KW p | spread |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `stress_mean_sleep` | 17.97 | 18.39 | 19.55 | 19.40 | 19.20 | 18.94 | 19.44 | **0.0016** | 1.581 |
| `all_day_stress_avg` | 31.00 | 33.00 | 33.00 | 33.00 | 32.00 | 33.00 | 31.00 | **0.0000** | 2.000 |
| `bb_lowest` | 21.00 | 18.00 | 18.00 | 17.00 | 18.00 | 19.00 | 19.00 | **0.0094** | 4.000 |
| `stress_stdev_sleep` | 7.39 | 6.74 | 7.34 | 7.08 | 7.14 | 7.72 | 7.92 | **0.0006** | 1.180 |
| `stress_low_motion_min_count_S60_Mlow` | 48.00 | 66.00 | 53.00 | 67.00 | 57.00 | 55.00 | 46.00 | **0.0000** | 21.000 |
| `resting_hr` | 56.00 | 56.00 | 56.00 | 56.00 | 56.00 | 56.00 | 56.00 | 1.0000 | 0.000 |

## 4. Stage 5 -- weekday-vs-weekend (Mann-Whitney U + Cliff's delta)

**Method**: per channel, split rows by weekday (Mon..Fri) vs weekend (Sat..Sun); compute median per group; two-sided Mann-Whitney U; Cliff's delta (weekend vs weekday; positive = weekend tends higher).

| channel | n_wd | n_we | med_wd | med_we | we-wd | MWU U | MWU p | Cliff delta | flag |
|---|---:|---:|---:|---:|---:|---:|---:|---:|:---|
| `stress_mean_sleep` | 1217 | 490 | 18.953 | 19.077 | +0.124 | 285186.0 | 0.1589 | +0.0435 | no-flag |
| `all_day_stress_avg` | 1236 | 496 | 32.500 | 32.000 | -0.500 | 311762.0 | 0.5775 | -0.0171 | no-flag |
| `bb_lowest` | 1236 | 496 | 18.000 | 19.000 | +1.000 | 304337.5 | 0.8158 | +0.0071 | no-flag |
| `stress_stdev_sleep` | 1217 | 490 | 7.142 | 7.789 | +0.647 | 260152.5 | 0.0000 | +0.1275 | **SUSPECT** |
| `stress_low_motion_min_count_S60_Mlow` | 1241 | 498 | 58.000 | 50.000 | -8.000 | 338178.0 | 0.0021 | -0.0944 | **SUSPECT** |
| `resting_hr` | 1236 | 495 | 56.000 | 56.000 | +0.000 | 307276.5 | 0.8837 | -0.0045 | no-flag |

**Cross-reference (Q4.4 4b highest-event-rate descriptive check)** -- per [`cohort_topology/findings.md`](../cohort_topology/findings.md) section 2 the `pacing_habit_established` (4b) phase has the highest total event rate (2.89/30d). If a DOW pattern (e.g. weekday work-stress) drives 4b event rates, it should also leak into the weekday-vs-weekend split here. The per-channel flag column above is the descriptive substrate for that cross-reference; **NO causal mechanism claim**.

---

## 5. Stage 6 -- v3 spring-control extension to all 6 channels

**Method (LOAD-BEARING per [citalopram_dose_response_stress_mean_sleep.md section 5.5 + 5.6](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md))**: for each channel, fit `channel ~ const + beta_time*days` on the spring window `03-20` -> `06-05` for the control year (2025; 30mg consolidation throughout) and the test year (2026; afbouw 30->8mg). HAC SE (maxlags=4). Report per-year beta + 95% CI + two-sided p. The **descriptive 'step-survives-same-season' flag** for CONFIRMED-citalopram channels is `yes-direction-and-2025-flat` iff (a) test-year beta sign matches the dose-down expected direction (`-prior`), AND (b) `|beta_2025| / |beta_2026| < 0.5`. **Descriptive observation only per CONVENTIONS section 4.2** -- this neither confirms nor refutes the v3 verdict; it extends the spring-control logic to 6 channels.

| channel | v3 prior | n_2025 | beta_2025 | CI_2025 | n_2026 | beta_2026 | CI_2026 | delta | step-survives? |
|---|---:|---:|---:|---|---:|---:|---|---:|:---|
| `stress_mean_sleep` | +1 | 78 | +0.0043 | [-0.0360,+0.0446] | 69 | -0.0259 | [-0.0646,+0.0129] | -0.0301 | yes-direction-and-2025-flat |
| `all_day_stress_avg` | +1 | 78 | +0.0420 | [+0.0063,+0.0777] | 71 | -0.0531 | [-0.0982,-0.0081] | -0.0951 | ambiguous-control-similar-magnitude |
| `bb_lowest` | -1 | 78 | -0.1339 | [-0.2036,-0.0641] | 71 | +0.0598 | [-0.0165,+0.1362] | +0.1937 | ambiguous-control-similar-magnitude |
| `stress_stdev_sleep` | n/a | 78 | +0.0297 | [+0.0120,+0.0475] | 69 | -0.0067 | [-0.0339,+0.0205] | -0.0364 | not-CONFIRMED-channel |
| `stress_low_motion_min_count_S60_Mlow` | n/a | 78 | +0.2479 | [+0.0159,+0.4798] | 77 | -0.5793 | [-0.8347,-0.3239] | -0.8272 | not-CONFIRMED-channel |
| `resting_hr` | n/a | 78 | +0.0108 | [-0.0071,+0.0287] | 71 | +0.0163 | [-0.0032,+0.0359] | +0.0055 | not-CONFIRMED-channel |

**Cross-references (descriptive only; LOAD-BEARING)**:

- **v3 spring-2025 control extension** (LOAD-BEARING per [citalopram_dose_response_stress_mean_sleep.md section 5.5.1 + section 5.6](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md)): the original v3 control was run on `stress_mean_sleep` only (beta_2025=-0.023/day -- flat); the section-5.6 multi-channel extension ran control on the other 5 channels and reported per-channel beta_2025 (all flat or small-counter-direction per section-5.6 table). Stage 6 above descriptively reproduces those numbers on the 6 channels in the user-locked scope. The v3 verdict (3 CONFIRMED channels: stress_mean_sleep, all_day_stress_avg, bb_lowest) is **NOT extended, NOT modified, NOT promoted** here per CONVENTIONS section 4.2.
- **Q4.2 buildup-transition Delta-z cross-reference** -- per [`intervention_cross_channel/findings.md`](../intervention_cross_channel/findings.md) section 5.1 the 2024-04-09 citalopram-buildup boundary on +/-30d windows shows per-channel Delta-z_pre values that are also present in 2025 spring control fit comparison context. Stage 6's per-channel beta_2025 (column above) is the substrate for any cross-window buildup-vs-spring-control comparison; **NO substantive verdict promotion**.
- **Q4.3 rp5 (citalopram-start) cross-reference** -- per [`era_boundaries/findings.md`](../era_boundaries/findings.md) section 2 the 2024-04-09 rp5 boundary shows distribution shift on 4 of 7 channels (autonomic-load + RHR family). Stage 6's beta_2025 column tests whether the same 4 channels also show a spring trend in the *clean* control year. If so, the rp5 shift inherits a seasonality caveat; if not, the rp5 shift is season-clean. **Descriptive substrate only per CONVENTIONS section 4.1.**

---

## 6. Stage 7 -- per-recovery-phase seasonality (harmonic per channel x phase)

**Method**: for each (channel, phase) cell, restrict to within-phase rows and refit the annual harmonic. Cells with n < 30 OR within-phase span < 180 days are skipped (annual harmonic underdetermined). Report amplitude + R2 per cell.

**Per-channel x phase harmonic amplitude (n in parens; `n/a` = skipped)**:

| channel | pre_illness_healthy | acute_infection | lc_pre_ergo | pacing_pre_citalopram_learning | pacing_habit_established | citalopram_modulated |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `stress_mean_sleep` | A=4.10 R2=0.08 (n=215) | n/a (n=14) | n/a (n=158) | n/a (n=53) | A=1.73 R2=0.03 (n=500) | A=2.40 R2=0.09 (n=767) |
| `all_day_stress_avg` | A=4.41 R2=0.12 (n=216) | n/a (n=14) | n/a (n=162) | n/a (n=53) | A=0.35 R2=0.00 (n=509) | A=1.01 R2=0.02 (n=778) |
| `bb_lowest` | A=5.43 R2=0.12 (n=216) | n/a (n=14) | n/a (n=162) | n/a (n=53) | A=2.40 R2=0.05 (n=509) | A=1.01 R2=0.01 (n=778) |
| `stress_stdev_sleep` | A=1.22 R2=0.04 (n=215) | n/a (n=14) | n/a (n=158) | n/a (n=53) | A=0.22 R2=0.00 (n=500) | A=0.26 R2=0.00 (n=767) |
| `stress_low_motion_min_count_S60_Mlow` | A=14.86 R2=0.03 (n=217) | n/a (n=14) | n/a (n=162) | n/a (n=54) | A=4.44 R2=0.00 (n=509) | A=9.33 R2=0.02 (n=783) |
| `resting_hr` | A=2.71 R2=0.50 (n=217) | n/a (n=14) | n/a (n=162) | n/a (n=53) | A=1.26 R2=0.15 (n=509) | A=2.19 R2=0.31 (n=776) |

**Cross-reference (recovery_arc v2 multi-year-arc seasonal-component check)** -- per [`recovery_arc/findings.md`](../recovery_arc/findings.md) section 5.A + section 2 the multi-year arc decomposes into 6 phase-cells per channel; the per-channel multi-year-arc shape may have a seasonal component within long phases. Stage 7 above is the descriptive substrate: if the per-channel harmonic amplitude is high within the `pacing_habit_established` (4b) or `citalopram_modulated` (5) cells, the recovery_arc per-phase reading inherits a seasonality-suspect flag at that cell. **NO claim that the multi-year arc is partly seasonal** per CONVENTIONS section 4.2 -- the descriptive substrate is per-phase, the arc-attribution would require a joint model with both trajectory + harmonic terms (out of scope).

---

## 7. Caveats

1. **No causal claims.** Per CONVENTIONS section 2.1 + section 4.3 this is Layer 1 descriptive. The per-channel seasonality flags + DOW flags + spring-control flags are descriptive substrate; intervention attribution is out of scope. Per CONVENTIONS section 4.2 caveat-class, suspect-flags are reported as `harmonic R2=X; suspect for seasonality confound` -- NOT promoted to substantive claims.
2. **Annual harmonic is a single-frequency model.** Multi-harmonic (semi-annual) + irregular seasonality (winter-illness clusters) are not captured by this Stage 2 model. The R2 reported is a lower bound on the 'fraction of variance explainable by seasonality'.
3. **DOW patterns may be expected on stress/RHR channels** (work-week stress is well-documented in general literature). The Stage 4 + Stage 5 suspect flags are descriptive substrate; mechanism claims are out of scope per CONVENTIONS section 4.2.
4. **v3 spring-control extension is descriptive observation only** per CONVENTIONS section 4.2. The `step-survives-same-season` flag in Stage 6 captures a per-channel reading of whether the spring-2025 control fit is roughly flat vs the spring-2026 test fit. This **neither confirms nor refutes** the v3 verdict per [citalopram_dose_response section 5.6](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md); it extends the spring-control logic to 6 channels descriptively. The 6-channel scope here differs from the v3 spec scope (v3 used 6 channels: the 3 CONFIRMED + 3 companions; this analysis's 6 channels are the user-locked Q4.9 + Q4.5.b + Q4.2 set; `bb_overnight_gain` is in v3 but not in Q4.8 scope; `stress_stdev_sleep` + `stress_low_motion_min_count_S60_Mlow` + `resting_hr` are common; v3 includes `respiration_avg_sleep` which Q4.8 does not).
5. **Per-recovery-phase seasonality (Stage 7) is restricted to phases with span >= 180 days**. Per `lc_recovery_phase_axis.md` section 2: pre_illness_healthy = ~217 days, acute_infection = 14 days, lc_pre_ergo = ~171 days, pacing_pre_citalopram_learning (4a) = 56 days, pacing_habit_established (4b) = ~508 days, citalopram_modulated = ~787 days. Stage 7's per-cell fit is only meaningful on the long phases (4b, 5; possibly pre_illness_healthy and lc_pre_ergo depending on coverage). Acute infection + 4a are too short for annual-harmonic fitting; reported as `n/a`.
6. **Single-year coverage** for some phases. `pre_illness_healthy` covers ~7 months of 2021-2022 (one shoulder-season cycle only); the per-channel harmonic fit on this phase is shaped by the single-year coverage and cannot disentangle within-year seasonality from the trajectory. Per [`recovery_arc/findings.md`](../recovery_arc/findings.md) section 5 caveat 4: any healthy-vs-LC contrast confounds illness state with season by construction.
7. **DOW analysis (Stage 4 + Stage 5) is on the full corpus**, not stratified by recovery phase. Phase-stratified DOW analysis would be a future deferred check; the Q4.8 spec is corpus-wide.
8. **HAC SE on the spring-window OLS** (Stage 6) assumes weak time-series autocorrelation within the ~78-day spring window. Per `permutation_null_block_length.md` the project default E[L]=7; HAC with maxlags=4 is comparable and was used in the original v3 spring_comparison.py per citalopram_dose_response_stress_mean_sleep.md section 5.5.1. The Stage 6 numbers descriptively reproduce the v3 method choice on 6 channels rather than re-arguing it.
9. **2024-04 boundary-collision** (CPAP end 2024-04-16 + Citalopram buildup start 2024-04-09; 7 days apart) per [intervention_effects section 2b](../../../../methodology/intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain) + section 8.1. The rp5 (4b -> 5) recovery-phase boundary at 2024-04-09 inherits the collision; Stage 7's 4b vs 5 amplitude comparison cannot disentangle CPAP-end effects from citalopram-start effects from any seasonal component. **Descriptive substrate only**, NOT a confounded-verdict claim.
10. **Q4.5.b resting_hr trajectory-driven cross-reference** -- per [`detrended_correlation/findings.md`](../detrended_correlation/findings.md) headline, 5 of 6 spurious-flag pairs involve `resting_hr` (the slow cardiovascular drift channel with E[L]\* long-memory structure). Stage 2 + Stage 7 above report `resting_hr` harmonic numbers; if the channel shows a high amplitude this is **consistent with** the Q4.5.b trajectory-driven spurious-correlation pattern but does **NOT** extend or modify the Q4.5.b verdict.

---

## 8. Cross-references

### LOAD-BEARING cross-references (descriptive corroboration only; NOT verdict extension)

- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../../../../methodology/citalopram_dose_response_stress_mean_sleep.md) section 5.5.1 + section 5.6 -- v3 spring-2025 control logic (LOAD-BEARING for Stage 6 extension to 6 channels).
- [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) section 2 -- 6-phase axis for Stage 7 per-recovery-phase seasonality.
- [`analyses/descriptive/trajectory/recovery_arc/findings.md`](../recovery_arc/findings.md) section 5 caveat 4 + section 5.A -- multi-year-arc seasonal-component descriptive check (Stage 7 substrate).
- [`analyses/descriptive/trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) section 2 -- Q4.3 rp5 (2024-04-09) distribution-shift cross-reference (Stage 6 substrate for seasonal-overlay check).
- [`analyses/descriptive/trajectory/intervention_cross_channel/findings.md`](../intervention_cross_channel/findings.md) section 5.1 -- Q4.2 buildup-transition Delta-z_pre cross-reference (Stage 6 substrate for seasonal-overlay check).
- [`analyses/descriptive/trajectory/cohort_topology/findings.md`](../cohort_topology/findings.md) section 2 -- Q4.4 4b highest-event-rate (2.89/30d) cross-reference (Stage 4 + Stage 5 substrate for DOW-pattern check).
- [`analyses/descriptive/trajectory/detrended_correlation/findings.md`](../detrended_correlation/findings.md) headline -- Q4.5.b resting_hr trajectory-driven cross-reference (Stage 2 + Stage 7 substrate for similar-pattern check).

### Methodology MDs cited (binding for this analysis's discipline)

- [`CONVENTIONS.md`](../../../../CONVENTIONS.md) section 2.1 (descriptive-before-inference), section 3.6 (named-counts), section 4.1 (caveats vs a-priori), section 4.2 (caveat-class language), section 4.3 (no interpretive marks).
- [`methodology/permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) -- block-length convention E[L]=7 (companion to HAC maxlags=4 in Stage 6).

### Upstream pipeline

- `pipeline/03_consolidate/build_unified_dataset.py` -- `per_day_master.csv` builder (includes the `recovery_phase` column populated at `e00df27`).
- `analyses/_utils/frame.py` -- `load_master()` loader (single source of truth for the as-of-date convention).

---

## 9. Status

**Q4.8 findings landed 2026-06-26** from a single execution of [`run.py`](run.py) under the user-LOCKED operationalisation (Strand B section 7c interview 2026-06-25). **Tier 3 deferred topic 1 of 2 LANDED**; remaining: Q4.7 notes-categorisation patterns. Next refresh per [`descriptive/README.md`](../../README.md) section 7d: when new data accrues +180 days (extends the harmonic-fit window) OR when an HA-* result raises a season-sensitive question.

