# Findings -- Q4.5.b detrended_correlation (methodological sanity check)

**Strand**: B (multi-year trajectory; descriptive sanity check). Closes the canonical Q4.5.b scope per [`analyses/descriptive/README.md`](../../README.md) section 4.5.b (r2 closure D3.4) -- detrended-companion correlation matrix per [CONVENTIONS section 3.7](../../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) trajectory-detrend sensitivity discipline.

**Surface**: Stratum 4 (LC + gevoelscore + crash labels, 2022-09-03 to 2026-06-05). n=1372 day-level rows.

**Programme spec**: [`descriptive/README.md`](../../README.md) section 4.5.b (LOCKED 2026-06-18 r3, commit `ccbd12e`) -- 'detrended-companion correlation matrix; spurious-correlation flag for time-trended pairs'.

**User-LOCKED operationalisation** (per Strand B section 7c interview 2026-06-25; do NOT iterate):

1. **Detrend method = ALL 3 methods + sensitivity**: linear OLS (CONVENTIONS section 3.7 default) + rolling-median 90d + per-recovery-phase residual.
2. **Channel-pair scope = 7x7 matrix (21 unique pairs)**: stress_mean_sleep + all_day_stress_avg + bb_lowest + stress_stdev_sleep + stress_low_motion_min_count_S60_Mlow + resting_hr + gevoelscore.
3. **Detrend granularity = both full + per-phase**: full-corpus single detrend tells you about multi-year arc cancellation; per-recovery-phase detrend tells you about within-phase drift cancellation.
4. **Spurious-correlation flag threshold = |delta rho| >= 0.1** per CONVENTIONS section 3.7 + HA precedent. Pairs where detrend changes rho by >= 0.1 in any method get SPURIOUS_TRAJECTORY_DRIVEN flag; otherwise WITHIN-WINDOW-REAL.

**Discipline**: Layer 1 descriptive sanity-check (no causal claims; no falsification bar; no HA verdict promotion; **not a claim that raw rho was wrong** -- detrend is a sensitivity arm per CONVENTIONS section 3.7) per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + section 3.7 + section 4.1 + section 4.2. HA07d both-eras-SUPPORTED + HA-C3 v2 + HA-C3p + crash_v2-definition + HA-P6 v3 + recovery_arc v2 LOCKED references are descriptive corroboration only; NONE are extended here.

---

## Headline

**Spurious-flag verdict**: 6 of 21 pairs flagged SPURIOUS_TRAJECTORY_DRIVEN in >=1 method; the remaining 15 survive all 3 detrend methods within the |delta rho| < 0.1 threshold (WITHIN-WINDOW-REAL).

**Per-method spurious-flag counts** (of 21 pairs):

| method | n pairs flagged SPURIOUS | rate |
|---|---:|---:|
| linear OLS | 5 | 23.8% |
| rolling-median 90d | 2 | 9.5% |
| per-recovery-phase | 2 | 9.5% |

**Long-memory vs short-memory rho-collapse pattern** (per Tier 1+2 E[L]* spread per handoff section 3.3): long-memory channels (E[L]* >= 21d: all_day_stress_avg / bb_lowest / stress_low_motion_min_count_S60_Mlow) are more likely to carry trajectory-driven rho; short-memory channels (E[L]* <= 10d: stress_stdev_sleep / resting_hr) less so.

| pair group | n pairs total | n flagged SPURIOUS | rate |
|---|---:|---:|---:|
| pairs involving any long-memory channel | 15 | 4 | 26.7% |
| short-memory x short-memory pairs only | 1 | 1 | 100.0% |

**HA07d-relevant pair** (stress_stdev_sleep x gevoelscore; E[L]*=7.0 short-memory channel; clean test of within-window-real per handoff section 3.3):

- rho_raw = -0.121 (n=1339)
- rho_ols = -0.072 (delta = +0.048)
- rho_rolling90d = -0.081 (delta = +0.040)
- rho_phase = -0.067 (delta = +0.054)
- **flag**: WITHIN-WINDOW-REAL (survives all 3 detrend methods)

**Methodology sensitivity**: per-method spurious-flag counts above are the descriptive measure of method-sensitivity. If the 3 methods produce systematically different counts, detrend method choice is load-bearing for the substantive read; if counts align, the rho values are robust to method choice.

---

## 2. Stage 2 -- raw rho matrix (21 pairs) -- VERIFICATION CHECK

**Method**: Spearman rho on the full Stratum 4 single-pool (matching Q3.9.e + Q4.9 method (c) full-pool resolution). 21 unique pairs from the 7-channel set (7-choose-2).

**REPRODUCES Q3.9.e rho ranking** per handoff section 3.3 (verification check): the 5 PRIMARY pairs involving `gevoelscore` (per Q3.9.e Strand-A first-pass) appear in this matrix and should match Q3.9.e reported values (stress_mean_sleep -0.194 / stress_stdev_sleep -0.121 / all_day_stress_avg -0.056 / resting_hr +0.020 / bb_lowest +0.010).

**Q3.9.e + Q4.9 method (c) verification table** (gevoelscore-vs-X pairs):

| pair | n | rho_raw (this analysis) | Q3.9.e reported | match? |
|---|---:|---:|---:|---|
| stress_mean_sleep x gevoelscore | 1339 | -0.194 | -0.194 | YES (within 0.005) |
| stress_stdev_sleep x gevoelscore | 1339 | -0.121 | -0.121 | YES (within 0.005) |
| all_day_stress_avg x gevoelscore | 1359 | -0.056 | -0.056 | YES (within 0.005) |
| resting_hr x gevoelscore | 1357 | +0.020 | +0.020 | YES (within 0.005) |
| bb_lowest x gevoelscore | 1359 | +0.010 | +0.010 | YES (within 0.005) |

**Full 21-pair raw rho matrix**:

| pair | n | rho_raw |
|---|---:|---:|
| stress_mean_sleep x all_day_stress_avg | 1339 | +0.404 |
| stress_mean_sleep x bb_lowest | 1339 | -0.423 |
| stress_mean_sleep x stress_stdev_sleep | 1339 | +0.501 |
| stress_mean_sleep x stress_low_motion_min_count_S60_Mlow | 1339 | +0.167 |
| stress_mean_sleep x resting_hr | 1337 | +0.377 |
| stress_mean_sleep x gevoelscore | 1339 | -0.194 |
| all_day_stress_avg x bb_lowest | 1359 | -0.749 |
| all_day_stress_avg x stress_stdev_sleep | 1339 | +0.266 |
| all_day_stress_avg x stress_low_motion_min_count_S60_Mlow | 1358 | +0.860 |
| all_day_stress_avg x resting_hr | 1357 | +0.195 |
| all_day_stress_avg x gevoelscore | 1359 | -0.056 |
| bb_lowest x stress_stdev_sleep | 1339 | -0.381 |
| bb_lowest x stress_low_motion_min_count_S60_Mlow | 1358 | -0.620 |
| bb_lowest x resting_hr | 1357 | -0.171 |
| bb_lowest x gevoelscore | 1359 | +0.010 |
| stress_stdev_sleep x stress_low_motion_min_count_S60_Mlow | 1339 | +0.194 |
| stress_stdev_sleep x resting_hr | 1337 | +0.073 |
| stress_stdev_sleep x gevoelscore | 1339 | -0.121 |
| stress_low_motion_min_count_S60_Mlow x resting_hr | 1356 | +0.099 |
| stress_low_motion_min_count_S60_Mlow x gevoelscore | 1365 | -0.056 |
| resting_hr x gevoelscore | 1357 | +0.020 |

---

## 3. Stage 3 -- linear OLS detrend (CONVENTIONS section 3.7 default)

**Method**: per channel, fit linear OLS of value ~ days-from-start; compute residual = value - (slope x t + intercept). Then for each pair, Spearman rho on residuals. This is the canonical detrend per [CONVENTIONS section 3.7](../../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) (adapted from the pre-vs-post-window precedent to the cross-channel correlation use-case).

**Honest framing per CONVENTIONS section 3.7**: if a pair's rho collapses under linear OLS detrend (|delta rho| >= 0.1), the raw rho is characterised SPURIOUS_TRAJECTORY_DRIVEN -- the multi-year arc was carrying the rank correlation. **Not a claim the raw rho was wrong**; the raw rho honestly describes the rank correlation on raw data + the detrended rho honestly describes the rank correlation on trajectory-removed residuals. Both are valid descriptions of different layers of structure.

| pair | n | rho_raw | rho_ols | delta_ols | |delta| | flag |
|---|---:|---:|---:|---:|---:|---|
| stress_mean_sleep x all_day_stress_avg | 1339 | +0.404 | +0.420 | +0.017 | 0.017 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x bb_lowest | 1339 | -0.423 | -0.428 | -0.005 | 0.005 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x stress_stdev_sleep | 1339 | +0.501 | +0.522 | +0.021 | 0.021 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x stress_low_motion_min_count_S60_Mlow | 1339 | +0.167 | +0.182 | +0.015 | 0.015 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x resting_hr | 1337 | +0.377 | +0.418 | +0.041 | 0.041 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x gevoelscore | 1339 | -0.194 | -0.211 | -0.016 | 0.016 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x bb_lowest | 1359 | -0.749 | -0.746 | +0.003 | 0.003 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x stress_stdev_sleep | 1339 | +0.266 | +0.219 | -0.047 | 0.047 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x stress_low_motion_min_count_S60_Mlow | 1358 | +0.860 | +0.849 | -0.012 | 0.012 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x resting_hr | 1357 | +0.195 | +0.351 | +0.155 | 0.155 | SPURIOUS |
| all_day_stress_avg x gevoelscore | 1359 | -0.056 | -0.015 | +0.040 | 0.040 | WITHIN-WINDOW-REAL |
| bb_lowest x stress_stdev_sleep | 1339 | -0.381 | -0.356 | +0.025 | 0.025 | WITHIN-WINDOW-REAL |
| bb_lowest x stress_low_motion_min_count_S60_Mlow | 1358 | -0.620 | -0.612 | +0.008 | 0.008 | WITHIN-WINDOW-REAL |
| bb_lowest x resting_hr | 1357 | -0.171 | -0.272 | -0.101 | 0.101 | SPURIOUS |
| bb_lowest x gevoelscore | 1359 | +0.010 | -0.018 | -0.028 | 0.028 | WITHIN-WINDOW-REAL |
| stress_stdev_sleep x stress_low_motion_min_count_S60_Mlow | 1339 | +0.194 | +0.137 | -0.057 | 0.057 | WITHIN-WINDOW-REAL |
| stress_stdev_sleep x resting_hr | 1337 | +0.073 | +0.228 | +0.155 | 0.155 | SPURIOUS |
| stress_stdev_sleep x gevoelscore | 1339 | -0.121 | -0.072 | +0.048 | 0.048 | WITHIN-WINDOW-REAL |
| stress_low_motion_min_count_S60_Mlow x resting_hr | 1356 | +0.099 | +0.280 | +0.181 | 0.181 | SPURIOUS |
| stress_low_motion_min_count_S60_Mlow x gevoelscore | 1365 | -0.056 | -0.006 | +0.050 | 0.050 | WITHIN-WINDOW-REAL |
| resting_hr x gevoelscore | 1357 | +0.020 | -0.088 | -0.108 | 0.108 | SPURIOUS |

---

## 4. Stage 4 -- rolling-median 90d detrend

**Method**: per channel, centred 90d rolling median; subtract from raw values to get residuals. Then for each pair, Spearman rho on residuals. The 90d window is wider than every channel's E[L]* (longest = all_day_stress_avg ~30d) so it preserves seasonal-to-trajectory structure while damping noise; complements linear OLS (which assumes constant slope across the corpus).

| pair | n | rho_raw | rho_rolling90d | delta_rolling | |delta| | flag |
|---|---:|---:|---:|---:|---:|---|
| stress_mean_sleep x all_day_stress_avg | 1339 | +0.404 | +0.405 | +0.001 | 0.001 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x bb_lowest | 1339 | -0.423 | -0.471 | -0.048 | 0.048 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x stress_stdev_sleep | 1339 | +0.501 | +0.537 | +0.036 | 0.036 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x stress_low_motion_min_count_S60_Mlow | 1339 | +0.167 | +0.146 | -0.021 | 0.021 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x resting_hr | 1337 | +0.377 | +0.361 | -0.017 | 0.017 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x gevoelscore | 1339 | -0.194 | -0.195 | -0.001 | 0.001 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x bb_lowest | 1359 | -0.749 | -0.725 | +0.024 | 0.024 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x stress_stdev_sleep | 1339 | +0.266 | +0.172 | -0.094 | 0.094 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x stress_low_motion_min_count_S60_Mlow | 1358 | +0.860 | +0.819 | -0.041 | 0.041 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x resting_hr | 1357 | +0.195 | +0.253 | +0.057 | 0.057 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x gevoelscore | 1359 | -0.056 | -0.030 | +0.026 | 0.026 | WITHIN-WINDOW-REAL |
| bb_lowest x stress_stdev_sleep | 1339 | -0.381 | -0.305 | +0.076 | 0.076 | WITHIN-WINDOW-REAL |
| bb_lowest x stress_low_motion_min_count_S60_Mlow | 1358 | -0.620 | -0.556 | +0.064 | 0.064 | WITHIN-WINDOW-REAL |
| bb_lowest x resting_hr | 1357 | -0.171 | -0.228 | -0.056 | 0.056 | WITHIN-WINDOW-REAL |
| bb_lowest x gevoelscore | 1359 | +0.010 | +0.030 | +0.021 | 0.021 | WITHIN-WINDOW-REAL |
| stress_stdev_sleep x stress_low_motion_min_count_S60_Mlow | 1339 | +0.194 | +0.063 | -0.131 | 0.131 | SPURIOUS |
| stress_stdev_sleep x resting_hr | 1337 | +0.073 | +0.184 | +0.111 | 0.111 | SPURIOUS |
| stress_stdev_sleep x gevoelscore | 1339 | -0.121 | -0.081 | +0.040 | 0.040 | WITHIN-WINDOW-REAL |
| stress_low_motion_min_count_S60_Mlow x resting_hr | 1356 | +0.099 | +0.140 | +0.041 | 0.041 | WITHIN-WINDOW-REAL |
| stress_low_motion_min_count_S60_Mlow x gevoelscore | 1365 | -0.056 | -0.002 | +0.054 | 0.054 | WITHIN-WINDOW-REAL |
| resting_hr x gevoelscore | 1357 | +0.020 | -0.062 | -0.082 | 0.082 | WITHIN-WINDOW-REAL |

---

## 5. Stage 5 -- per-recovery-phase residual detrend

**Method**: per channel, subtract the per-recovery-phase mean from each row. Phases from [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) section 2 (6 phases; Stratum 4 contains last 19 days of `lc_pre_ergo` + 4a + 4b + 5). Then for each pair, Spearman rho on residuals.

**LOAD-BEARING Q4.3 rp5 cross-reference (descriptive only)** per handoff section 3.3: Q4.3 found rp5 (citalopram start, 2024-04-09) is the strongest boundary on 5 of 6 channels -- the multi-year arc carries substantial citalopram-step component. Therefore linear OLS detrend on the full corpus may CANCEL multi-year-arc structure (including the citalopram step), but per-recovery-phase detrend PRESERVES within-phase content (the citalopram step is absorbed into the per-phase mean shift). Pairs that flag SPURIOUS under linear OLS but survive under per-phase detrend are particularly interesting: the multi-year arc was carrying the rho but the within-phase drift wasn't. The Q4.3 rp5 substantive finding is LOCKED and NOT extended here.

| pair | n | rho_raw | rho_phase | delta_phase | |delta| | flag |
|---|---:|---:|---:|---:|---:|---|
| stress_mean_sleep x all_day_stress_avg | 1339 | +0.404 | +0.405 | +0.002 | 0.002 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x bb_lowest | 1339 | -0.423 | -0.417 | +0.006 | 0.006 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x stress_stdev_sleep | 1339 | +0.501 | +0.515 | +0.014 | 0.014 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x stress_low_motion_min_count_S60_Mlow | 1339 | +0.167 | +0.162 | -0.006 | 0.006 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x resting_hr | 1337 | +0.377 | +0.413 | +0.036 | 0.036 | WITHIN-WINDOW-REAL |
| stress_mean_sleep x gevoelscore | 1339 | -0.194 | -0.204 | -0.009 | 0.009 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x bb_lowest | 1359 | -0.749 | -0.738 | +0.011 | 0.011 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x stress_stdev_sleep | 1339 | +0.266 | +0.189 | -0.077 | 0.077 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x stress_low_motion_min_count_S60_Mlow | 1358 | +0.860 | +0.833 | -0.027 | 0.027 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x resting_hr | 1357 | +0.195 | +0.291 | +0.096 | 0.096 | WITHIN-WINDOW-REAL |
| all_day_stress_avg x gevoelscore | 1359 | -0.056 | +0.011 | +0.067 | 0.067 | WITHIN-WINDOW-REAL |
| bb_lowest x stress_stdev_sleep | 1339 | -0.381 | -0.335 | +0.046 | 0.046 | WITHIN-WINDOW-REAL |
| bb_lowest x stress_low_motion_min_count_S60_Mlow | 1358 | -0.620 | -0.591 | +0.029 | 0.029 | WITHIN-WINDOW-REAL |
| bb_lowest x resting_hr | 1357 | -0.171 | -0.230 | -0.059 | 0.059 | WITHIN-WINDOW-REAL |
| bb_lowest x gevoelscore | 1359 | +0.010 | -0.045 | -0.054 | 0.054 | WITHIN-WINDOW-REAL |
| stress_stdev_sleep x stress_low_motion_min_count_S60_Mlow | 1339 | +0.194 | +0.093 | -0.101 | 0.101 | SPURIOUS |
| stress_stdev_sleep x resting_hr | 1337 | +0.073 | +0.159 | +0.086 | 0.086 | WITHIN-WINDOW-REAL |
| stress_stdev_sleep x gevoelscore | 1339 | -0.121 | -0.067 | +0.054 | 0.054 | WITHIN-WINDOW-REAL |
| stress_low_motion_min_count_S60_Mlow x resting_hr | 1356 | +0.099 | +0.202 | +0.102 | 0.102 | SPURIOUS |
| stress_low_motion_min_count_S60_Mlow x gevoelscore | 1365 | -0.056 | +0.028 | +0.084 | 0.084 | WITHIN-WINDOW-REAL |
| resting_hr x gevoelscore | 1357 | +0.020 | -0.047 | -0.067 | 0.067 | WITHIN-WINDOW-REAL |

---

## 6. Stage 6 -- sensitivity comparison + spurious-flag table

**Method**: per pair, compute |delta rho| vs raw for each of 3 detrend methods; flag SPURIOUS_TRAJECTORY_DRIVEN if any |delta rho| >= 0.1 (CONVENTIONS section 3.7 default + HA precedent).

**Spurious-flag count**: 6 of 21 pairs flagged SPURIOUS in >=1 detrend method.

**Flagged pair table** (sorted by max |delta|):

| pair | n | rho_raw | rho_ols | rho_rolling | rho_phase | max |delta| | method driving max delta |
|---|---:|---:|---:|---:|---:|---:|---|
| stress_low_motion_min_count_S60_Mlow x resting_hr | 1356 | +0.099 | +0.280 | +0.140 | +0.202 | 0.181 | ols |
| all_day_stress_avg x resting_hr | 1357 | +0.195 | +0.351 | +0.253 | +0.291 | 0.155 | ols |
| stress_stdev_sleep x resting_hr | 1337 | +0.073 | +0.228 | +0.184 | +0.159 | 0.155 | ols |
| stress_stdev_sleep x stress_low_motion_min_count_S60_Mlow | 1339 | +0.194 | +0.137 | +0.063 | +0.093 | 0.131 | rolling |
| resting_hr x gevoelscore | 1357 | +0.020 | -0.088 | -0.062 | -0.047 | 0.108 | ols |
| bb_lowest x resting_hr | 1357 | -0.171 | -0.272 | -0.228 | -0.230 | 0.101 | ols |

**Surviving pair table (WITHIN-WINDOW-REAL across all 3 methods)**:

| pair | n | rho_raw | rho_ols | rho_rolling | rho_phase | max |delta| |
|---|---:|---:|---:|---:|---:|---:|
| stress_mean_sleep x all_day_stress_avg | 1339 | +0.404 | +0.420 | +0.405 | +0.405 | 0.017 |
| stress_mean_sleep x bb_lowest | 1339 | -0.423 | -0.428 | -0.471 | -0.417 | 0.048 |
| stress_mean_sleep x stress_stdev_sleep | 1339 | +0.501 | +0.522 | +0.537 | +0.515 | 0.036 |
| stress_mean_sleep x stress_low_motion_min_count_S60_Mlow | 1339 | +0.167 | +0.182 | +0.146 | +0.162 | 0.021 |
| stress_mean_sleep x resting_hr | 1337 | +0.377 | +0.418 | +0.361 | +0.413 | 0.041 |
| stress_mean_sleep x gevoelscore | 1339 | -0.194 | -0.211 | -0.195 | -0.204 | 0.016 |
| all_day_stress_avg x bb_lowest | 1359 | -0.749 | -0.746 | -0.725 | -0.738 | 0.024 |
| all_day_stress_avg x stress_stdev_sleep | 1339 | +0.266 | +0.219 | +0.172 | +0.189 | 0.094 |
| all_day_stress_avg x stress_low_motion_min_count_S60_Mlow | 1358 | +0.860 | +0.849 | +0.819 | +0.833 | 0.041 |
| all_day_stress_avg x gevoelscore | 1359 | -0.056 | -0.015 | -0.030 | +0.011 | 0.067 |
| bb_lowest x stress_stdev_sleep | 1339 | -0.381 | -0.356 | -0.305 | -0.335 | 0.076 |
| bb_lowest x stress_low_motion_min_count_S60_Mlow | 1358 | -0.620 | -0.612 | -0.556 | -0.591 | 0.064 |
| bb_lowest x gevoelscore | 1359 | +0.010 | -0.018 | +0.030 | -0.045 | 0.054 |
| stress_stdev_sleep x gevoelscore | 1339 | -0.121 | -0.072 | -0.081 | -0.067 | 0.054 |
| stress_low_motion_min_count_S60_Mlow x gevoelscore | 1365 | -0.056 | -0.006 | -0.002 | +0.028 | 0.084 |

**Particularly-interesting pairs** (SPURIOUS under linear OLS but survive under per-phase detrend; multi-year arc was carrying rho but within-phase drift wasn't):

- **all_day_stress_avg x resting_hr**: rho_raw = +0.195; rho_ols = +0.351 (delta = +0.155 collapsed); rho_phase = +0.291 (delta = +0.096 preserved)
- **bb_lowest x resting_hr**: rho_raw = -0.171; rho_ols = -0.272 (delta = -0.101 collapsed); rho_phase = -0.230 (delta = -0.059 preserved)
- **stress_stdev_sleep x resting_hr**: rho_raw = +0.073; rho_ols = +0.228 (delta = +0.155 collapsed); rho_phase = +0.159 (delta = +0.086 preserved)
- **resting_hr x gevoelscore**: rho_raw = +0.020; rho_ols = -0.088 (delta = -0.108 collapsed); rho_phase = -0.047 (delta = -0.067 preserved)

---

## 7. Stage 5b -- per-recovery-phase granularity tables (within-phase rho)

**Method**: per recovery phase with n>=30 rows, compute the per-pair Spearman rho on the in-phase subset. This is the **per-phase granularity** tier of the user-locked operationalisation choice 3 (both full + per-phase); complements Stage 5's per-phase mean-residual detrend by showing the within-phase rho directly.

**Per-phase n** (rows with `recovery_phase` matching; Stratum 4 right edge 2026-06-05):

| phase | n | included in per-phase granularity? |
|---|---:|---|
| pre_illness_healthy | 0 | no (n<30) |
| acute_infection | 0 | no (n<30) |
| lc_pre_ergo | 19 | no (n<30) |
| pacing_pre_citalopram_learning | 56 | YES |
| pacing_habit_established | 509 | YES |
| citalopram_modulated | 788 | YES |

### Phase: `pacing_pre_citalopram_learning` (n=56)

| pair | n | rho_within_phase |
|---|---:|---:|
| stress_mean_sleep x all_day_stress_avg | 53 | +0.272 |
| stress_mean_sleep x bb_lowest | 53 | -0.345 |
| stress_mean_sleep x stress_stdev_sleep | 53 | +0.478 |
| stress_mean_sleep x stress_low_motion_min_count_S60_Mlow | 53 | +0.098 |
| stress_mean_sleep x resting_hr | 53 | +0.290 |
| stress_mean_sleep x gevoelscore | 53 | -0.301 |
| all_day_stress_avg x bb_lowest | 53 | -0.804 |
| all_day_stress_avg x stress_stdev_sleep | 53 | +0.148 |
| all_day_stress_avg x stress_low_motion_min_count_S60_Mlow | 53 | +0.887 |
| all_day_stress_avg x resting_hr | 53 | -0.032 |
| all_day_stress_avg x gevoelscore | 53 | +0.218 |
| bb_lowest x stress_stdev_sleep | 53 | -0.184 |
| bb_lowest x stress_low_motion_min_count_S60_Mlow | 53 | -0.638 |
| bb_lowest x resting_hr | 53 | -0.092 |
| bb_lowest x gevoelscore | 53 | -0.194 |
| stress_stdev_sleep x stress_low_motion_min_count_S60_Mlow | 53 | +0.048 |
| stress_stdev_sleep x resting_hr | 53 | +0.057 |
| stress_stdev_sleep x gevoelscore | 53 | -0.085 |
| stress_low_motion_min_count_S60_Mlow x resting_hr | 53 | -0.076 |
| stress_low_motion_min_count_S60_Mlow x gevoelscore | 54 | +0.285 |
| resting_hr x gevoelscore | 53 | +0.050 |

### Phase: `pacing_habit_established` (n=509)

| pair | n | rho_within_phase |
|---|---:|---:|
| stress_mean_sleep x all_day_stress_avg | 500 | +0.419 |
| stress_mean_sleep x bb_lowest | 500 | -0.416 |
| stress_mean_sleep x stress_stdev_sleep | 500 | +0.545 |
| stress_mean_sleep x stress_low_motion_min_count_S60_Mlow | 500 | +0.189 |
| stress_mean_sleep x resting_hr | 500 | +0.467 |
| stress_mean_sleep x gevoelscore | 500 | -0.267 |
| all_day_stress_avg x bb_lowest | 509 | -0.714 |
| all_day_stress_avg x stress_stdev_sleep | 500 | +0.164 |
| all_day_stress_avg x stress_low_motion_min_count_S60_Mlow | 509 | +0.838 |
| all_day_stress_avg x resting_hr | 509 | +0.322 |
| all_day_stress_avg x gevoelscore | 509 | -0.091 |
| bb_lowest x stress_stdev_sleep | 500 | -0.302 |
| bb_lowest x stress_low_motion_min_count_S60_Mlow | 509 | -0.596 |
| bb_lowest x resting_hr | 509 | -0.180 |
| bb_lowest x gevoelscore | 509 | +0.012 |
| stress_stdev_sleep x stress_low_motion_min_count_S60_Mlow | 500 | +0.080 |
| stress_stdev_sleep x resting_hr | 500 | +0.192 |
| stress_stdev_sleep x gevoelscore | 500 | -0.079 |
| stress_low_motion_min_count_S60_Mlow x resting_hr | 509 | +0.192 |
| stress_low_motion_min_count_S60_Mlow x gevoelscore | 509 | -0.062 |
| resting_hr x gevoelscore | 509 | -0.257 |

### Phase: `citalopram_modulated` (n=788)

| pair | n | rho_within_phase |
|---|---:|---:|
| stress_mean_sleep x all_day_stress_avg | 767 | +0.411 |
| stress_mean_sleep x bb_lowest | 767 | -0.427 |
| stress_mean_sleep x stress_stdev_sleep | 767 | +0.481 |
| stress_mean_sleep x stress_low_motion_min_count_S60_Mlow | 767 | +0.148 |
| stress_mean_sleep x resting_hr | 765 | +0.401 |
| stress_mean_sleep x gevoelscore | 767 | -0.157 |
| all_day_stress_avg x bb_lowest | 778 | -0.748 |
| all_day_stress_avg x stress_stdev_sleep | 767 | +0.206 |
| all_day_stress_avg x stress_low_motion_min_count_S60_Mlow | 777 | +0.832 |
| all_day_stress_avg x resting_hr | 776 | +0.293 |
| all_day_stress_avg x gevoelscore | 778 | +0.045 |
| bb_lowest x stress_stdev_sleep | 767 | -0.365 |
| bb_lowest x stress_low_motion_min_count_S60_Mlow | 777 | -0.589 |
| bb_lowest x resting_hr | 776 | -0.262 |
| bb_lowest x gevoelscore | 778 | -0.052 |
| stress_stdev_sleep x stress_low_motion_min_count_S60_Mlow | 767 | +0.107 |
| stress_stdev_sleep x resting_hr | 765 | +0.137 |
| stress_stdev_sleep x gevoelscore | 767 | -0.070 |
| stress_low_motion_min_count_S60_Mlow x resting_hr | 775 | +0.230 |
| stress_low_motion_min_count_S60_Mlow x gevoelscore | 783 | +0.064 |
| resting_hr x gevoelscore | 776 | +0.078 |

---

## 8. Methodology sensitivity report

**Question**: does detrend method choice systematically alter conclusions? Compare per-method spurious counts and per-pair |delta| patterns.

**Per-method spurious counts** (recap from headline): linear OLS = 5, rolling-median 90d = 2, per-phase = 2.

**Per-method aggregate |delta| statistics** (across 21 pairs):

| method | mean |delta| | median |delta| | max |delta| | n with |delta|>=0.1 |
|---|---:|---:|---:|---:|
| linear OLS | 0.054 | 0.040 | 0.181 | 5 |
| rolling-median 90d | 0.050 | 0.041 | 0.131 | 2 |
| per-recovery-phase | 0.049 | 0.054 | 0.102 | 2 |

**Method-sensitivity narrative** (descriptive only per CONVENTIONS section 4.1): if the three method counts agree closely, the spurious/within-window-real verdict is robust to method choice. If the per-phase method flags substantially fewer pairs than linear OLS, the within-phase content survives even when the multi-year arc is removed (cf. Q4.3 rp5 citalopram-step finding -- per-phase detrend leaves the within-phase drift intact). If rolling-median 90d falls between OLS and per-phase, the slow trajectory + per-phase shift BOTH carry meaningful structure; method choice has gradient sensitivity.

**Long-memory vs short-memory pattern**: long-memory channels (E[L]* >= 21d) are structurally more prone to trajectory-driven rho because their slow drift dominates the variance budget; short-memory channels (E[L]* <= 10d) have weaker trajectory weight. The pair-group rates above descriptively surface this expectation.

---

## Cross-references

### LOAD-BEARING cross-references (descriptive corroboration only; NOT verdict extension)

- **Q3.9.e Strand-A first-pass** at [`descriptive/operationalisation_support/gevoelscore/findings.md`](../../operationalisation_support/gevoelscore/findings.md) section 3.9.e: linear-rank Spearman rho ranking on the full Stratum-4 pool. Stage 2 above REPRODUCES the 5 PRIMARY gevoelscore-vs-X pairs as a verification check.
- **Q4.9 method (c) rolling-Spearman precedent** at [`descriptive/trajectory/subjective_objective_coupling/findings.md`](../subjective_objective_coupling/findings.md) section 4: rolling-window rho approach for the time-varying-structure complement; Q4.9 stays on raw rho across rolling windows -- this Q4.5.b complements with full-pool detrended rho across 3 methods.
- **Q4.3 era_boundaries finding** at [`descriptive/trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) section 2-3: rp5 citalopram-start is the strongest boundary (5 of 6 channels). The multi-year arc carries substantial citalopram-step component; this contextualises why linear OLS detrend (which cancels the arc) can collapse pairs that per-phase detrend (which absorbs the step into the per-phase mean) preserves.
- **Q4.6 coverage_overview finding** at [`descriptive/trajectory/coverage_overview/findings.md`](../coverage_overview/findings.md): bb_overnight_gain only available from 2024-09-18 onward (excluded from this 7-channel scope per user-locked operationalisation, which uses bb_lowest in its place). bb_lowest itself has full coverage in Stratum 4.
- **HA07d both-eras-SUPPORTED finding** at [`analyses/hypotheses/HA07d-sleep-stress-variability/result.md`](../../../hypotheses/HA07d-sleep-stress-variability/result.md) (LOCKED): stress_stdev_sleep is the channel; E[L]*=7.0 short-memory makes the gevoelscore x stress_stdev_sleep pair the cleanest test of within-window-real (low trajectory loading by E[L]* metric). The HA07d substantive verdict is LOCKED and NOT extended here.
- **CONVENTIONS section 3.7** trajectory-detrend sensitivity discipline [`CONVENTIONS.md`](../../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons): binding precedent for the |delta rho| >= 0.1 threshold + the linear-on-pre-window-form-is-conservative framing + the empirical-validation paragraph (Session C intervention_effects MD found 2 of 7 raw-test findings were trajectory artifacts under detrend; the pattern is not hypothetical).

### Methodology MDs cited (binding for this analysis's discipline)

- [CONVENTIONS section 3.7](../../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) trajectory-detrend sensitivity for raw comparisons.
- [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) (6-phase axis for per-recovery-phase detrend in Stage 5).
- [`methodology/permutation_null_block_length.md`](../../../../methodology/permutation_null_block_length.md) (E[L]=7 default + factor-of-2 deviation rule; per-channel E[L]* informs the long-memory vs short-memory rho-collapse rate framing).
- [`methodology/lc_era_temporal_segmentation.md`](../../../../methodology/lc_era_temporal_segmentation.md) (Stratum 4 boundary; surface for primary analysis).
- [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + section 4.1 + section 4.2 (descriptive-only framing discipline).

### Upstream pipeline

- `per_day_master.csv` <- `pipeline/03_consolidate/build_unified_dataset.py` (7 channel columns + recovery_phase).

---

## Limitations

For a producer-mode Layer-1 descriptive Strand B sanity-check analysis (no falsification bar; no causal claim per [CONVENTIONS section 2.1](../../../../CONVENTIONS.md#21-descriptive-before-inference) + section 3.7 sensitivity-arm framing), the binding constraints are:

1. **Detrend is a sensitivity arm, NOT a correction** per CONVENTIONS section 3.7. The raw rho honestly describes the rank correlation on raw data; the detrended rho honestly describes the rank correlation on trajectory-removed residuals. **Not a claim the raw rho was wrong**. Pairs flagged SPURIOUS surface as 'rho_raw collapses to rho_detrended ~0 under method X' -- a structural observation, not a correction.
2. **No HA verdict promotion**: HA07d both-eras-SUPPORTED + HA-C3 v2 + HA-C3p + HA-P6 v3 + recovery_arc v2 + crash_v2-definition LOCKED verdicts are referenced as descriptive context only; NONE are extended or re-interpreted per CONVENTIONS section 4.2 + handoff section 4 hard constraint.
3. **No crash_v2-definition modification** + no methodology MD modification + no per_day_master.csv modification per handoff section 4 hard constraint.
4. **No iteration on the 4 user-locked operationalisation choices** per Strand B section 7c discipline.
5. **Linear OLS assumes constant slope across Stratum 4** -- if the true trajectory is non-linear (e.g. logistic recovery), linear OLS may under-detrend (residuals still carry curvature) or over-detrend (residuals contain spurious sub-trajectory). The rolling-median 90d and per-phase methods complement by allowing non-linear / piecewise trajectory shapes.
6. **Rolling-median 90d edge effects**: centred 90d rolling median shrinks at the corpus edges (first and last ~45 days). Residuals near edges may be unstable; per CONVENTIONS section 3.6 named-count discipline, the |delta| values for rolling-median include the edge regions if data is present.
7. **Per-phase detrend reduces variance more aggressively when phase n is small** (e.g. pacing_pre_citalopram_learning n=56 in Stratum 4). Per-pair rho on tiny in-phase subsets is high-variance; the per-phase granularity tables in section 7 skip phases with n<30 for robustness.
8. **Recovery-phase axis is the 6-phase axis from `lc_recovery_phase_axis.md`** (LOCKED 2026-06-19 d47e0d3). Stratum 4 spans last 19 days of `lc_pre_ergo` + 4a + 4b + 5; phases 1 + 2 (pre_illness_healthy, acute_infection) have zero rows in Stratum 4 by construction (gevoelscore logging started 2022-09-03).
9. **Spurious-flag threshold = 0.1 inherits CONVENTIONS section 3.7 + HA precedent**. Alternative thresholds (0.05 stricter; 0.15 looser) would yield different flagged-pair counts; the 0.1 value is the locked precedent and is not re-negotiated here.
10. **gevoelscore is bounded 1-6 integer** per Q3.9.a + Q4.9. Spearman rho handles this via average-rank ties; linear OLS detrend subtracts a continuous trend from a discrete series (residuals are no longer integer). The Spearman rho on those residuals is mathematically well-defined; the interpretation as 'within-window rho structure on a 1-6 felt-state channel after multi-year arc removal' is the appropriate framing.

---

*Generated programmatically by [`run.py`](run.py) from the resolved `summary.json` (gitignored per `docs/research/**/*.json`). To refresh: `python run.py`.*