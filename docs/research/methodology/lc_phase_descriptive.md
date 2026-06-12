# lc_phase descriptive summary

*Per-phase distribution of key signals on per_day_master.csv. Generated 2026-06-12*
*from `c:/tmp/lc_phase_descriptive.py`. Pure-observation per the*
*no-interpretive-marks rule: describes distributions within each phase, does not*
*compare across phases or impute causal meaning. Re-run when the master changes.*

Phases (see DATA_DICTIONARY.md sec0 `lc_phase`):

- `pre_corona` (date < 2022-03-21) - healthy / training-period window
- `corona_infection` (2022-03-21 -> 2022-04-03) - corona-ziek-week through Fietsweekend Ardennen
- `lc` (date >= 2022-04-04) - LC-symptom-onset and onwards

**Read-out caveats** (pure observation; downstream interpretation TBD):

- `gevoelscore` only exists in the `lc` phase; the gevoelscore corpus starts 2022-09-03.
- v3.2 `_lagged_lcera` columns are 0% populated in `pre_corona` and `corona_infection` by design (baseline excludes those days).
- v3.2 `_lagged` all-era columns are populated in all three phases (after the 90-day warmup, effective start ~2021-11-14).
- Distributions are NOT corrected for seasonality, day-of-week, or umbrella event labels.

---

## Phase overview

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n_days | 217 | 14 | 1524 |
| date range | 2021-08-16 -> 2022-03-20 | 2022-03-21 -> 2022-04-03 | 2022-04-04 -> 2026-06-05 |
| has_garmin_uds | 217 (100.0%) | 14 (100.0%) | 1503 (98.6%) |
| has_garmin_sleep | 215 (99.1%) | 14 (100.0%) | 1478 (97.0%) |
| has_score | 0 (0.0%) | 0 (0.0%) | 1372 (90.0%) |
| has_note | 0 (0.0%) | 0 (0.0%) | 686 (45.0%) |
| has_intensity_triage | 79 (36.4%) | 13 (92.9%) | 1465 (96.1%) |

---

## Garmin daily activity (gated on has_garmin_uds=True)

### total_steps

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1501 |
| mean | 10317 | 5736 | 5113 |
| std | 6267 | 2968 | 2202 |
| min | 1073 | 1005 | 17 |
| p10 | 3802 | 2261 | 2602 |
| p25 | 5747 | 3892 | 3566 |
| p50 | 8326 | 5220 | 4799 |
| p75 | 13700 | 8032 | 6404 |
| p90 | 19572 | 9722 | 8081 |
| max | 36258 | 11249 | 16932 |

### moderate_min

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1503 |
| mean | 6.7 | 3.6 | 10.7 |
| std | 16.6 | 9.7 | 18.9 |
| min | 0 | 0 | 0 |
| p10 | 0 | 0 | 0 |
| p25 | 0 | 0 | 0 |
| p50 | 1 | 0 | 0 |
| p75 | 7 | 0 | 14 |
| p90 | 13 | 9.8 | 36 |
| max | 126 | 36 | 150 |

### vigorous_min

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1503 |
| mean | 31.9 | 10.7 | 1.2 |
| std | 50.5 | 34.3 | 3.2 |
| min | 0 | 0 | 0 |
| p10 | 0 | 0 | 0 |
| p25 | 0 | 0 | 0 |
| p50 | 3 | 0 | 0 |
| p75 | 52 | 1.8 | 1 |
| p90 | 90 | 7.6 | 4 |
| max | 446 | 134 | 50 |

### total_calories

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1503 |
| mean | 720 | 406 | 354 |
| std | 677 | 489 | 207 |
| min | 44 | 35 | 0 |
| p10 | 161 | 113 | 142 |
| p25 | 265 | 158 | 206 |
| p50 | 508 | 250 | 311 |
| p75 | 992 | 405 | 450 |
| p90 | 1457 | 585 | 628 |
| max | 6175 | 2078 | 1382 |

### daily_step_goal

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1503 |
| mean | 9886 | 6509 | 5134 |
| std | 1486 | 1149 | 1168 |
| min | 6170 | 4900 | 2340 |
| p10 | 7822 | 5168 | 3740 |
| p25 | 8880 | 5245 | 4260 |
| p50 | 10000 | 6715 | 5040 |
| p75 | 11060 | 7390 | 5830 |
| p90 | 11698 | 7879 | 6648 |
| max | 13040 | 8240 | 9890 |

---

## Garmin heart rate (gated on has_garmin_uds=True)

### resting_hr

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1500 |
| mean | 53.4 | 53.4 | 56.5 |
| std | 2.9 | 2.4 | 2.8 |
| min | 47 | 51 | 49 |
| p10 | 49 | 51 | 53 |
| p25 | 52 | 51 | 55 |
| p50 | 54 | 52.5 | 56 |
| p75 | 55 | 55 | 58 |
| p90 | 57 | 56.7 | 60.1 |
| max | 61 | 58 | 65 |

### min_hr

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1502 |
| mean | 49.3 | 50.8 | 54.1 |
| std | 3.7 | 3.8 | 3.7 |
| min | 39 | 46 | 31 |
| p10 | 45 | 46 | 50 |
| p25 | 47 | 47 | 52 |
| p50 | 49 | 52 | 54 |
| p75 | 51 | 53.8 | 56 |
| p90 | 53 | 54.7 | 59 |
| max | 63 | 58 | 72 |

### max_hr

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1502 |
| mean | 137.4 | 115.5 | 119.4 |
| std | 30.0 | 19.8 | 11.0 |
| min | 93 | 99 | 67 |
| p10 | 104 | 102.9 | 108 |
| p25 | 110 | 106 | 112 |
| p50 | 122 | 108.5 | 118 |
| p75 | 170 | 114 | 125 |
| p90 | 177 | 133.8 | 133 |
| max | 183 | 178 | 184 |

### max_avg_hr_uds

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1502 |
| mean | 135.4 | 113.4 | 116.9 |
| std | 30.7 | 19.6 | 10.7 |
| min | 91 | 98 | 67 |
| p10 | 101.6 | 101.3 | 105 |
| p25 | 108 | 103 | 110 |
| p50 | 120 | 107 | 116 |
| p75 | 169 | 112 | 122 |
| p90 | 176 | 129.8 | 131 |
| max | 182 | 176 | 181 |

---

## Garmin engineered exertion (gated on has_garmin_uds=True)

### effective_exertion_min (raw)

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1503 |
| mean | 37.0 | 13.2 | 10.8 |
| std | 62.4 | 41.5 | 21.4 |
| min | 0 | 0 | 0 |
| p10 | 0 | 0 | 0 |
| p25 | 0 | 0 | 0 |
| p50 | 4.5 | 0 | 1 |
| p75 | 58.5 | 1.8 | 12 |
| p90 | 99.9 | 12.5 | 35.3 |
| max | 629.5 | 162.2 | 325.5 |

### step_z_30d (v3.1 LEGACY)

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 197 | 14 | 1501 |
| mean | 0.36 | -0.17 | 0.14 |
| std | 1.23 | 0.66 | 1.20 |
| min | -1.85 | -1.21 | -4.08 |
| p10 | -0.95 | -0.95 | -1.19 |
| p25 | -0.57 | -0.60 | -0.68 |
| p50 | -0.01 | -0.23 | -0.01 |
| p75 | 1.08 | 0.42 | 0.84 |
| p90 | 2.03 | 0.71 | 1.72 |
| max | 5.63 | 0.94 | 5.55 |

### exertion_rank_composite_lagged (v3.2 all-era)

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 147 | 14 | 1503 |
| mean | 0.602 | 0.433 | 0.696 |
| std | 0.307 | 0.202 | 0.231 |
| min | 0.108 | 0.208 | 0.208 |
| p10 | 0.169 | 0.233 | 0.342 |
| p25 | 0.325 | 0.256 | 0.500 |
| p50 | 0.583 | 0.408 | 0.733 |
| p75 | 0.917 | 0.542 | 0.908 |
| p90 | 0.967 | 0.573 | 0.983 |
| max | 1 | 1 | 1 |

### exertion_rank_composite_lagged_lcera (v3.2 LC-era-only)

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | -- | -- | 1433 |
| mean | -- | -- | 0.703 |
| std | -- | -- | 0.232 |
| min | -- | -- | 0.196 |
| p10 | -- | -- | 0.342 |
| p25 | -- | -- | 0.500 |
| p50 | -- | -- | 0.758 |
| p75 | -- | -- | 0.917 |
| p90 | -- | -- | 0.983 |
| max | -- | -- | 1 |

### push_burden_7d_lagged

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1503 |
| mean | 1.41 | 0.14 | 1.81 |
| std | 1.18 | 0.35 | 1.43 |
| min | 0 | 0 | 0 |
| p10 | 0 | 0 | 0 |
| p25 | 0 | 0 | 1 |
| p50 | 2 | 0 | 2 |
| p75 | 2 | 0 | 3 |
| p90 | 3 | 0.70 | 4 |
| max | 4 | 1 | 6 |

### push_burden_7d_lagged_lcera

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1503 |
| mean | 0 | 0 | 1.78 |
| std | 0 | 0 | 1.44 |
| min | 0 | 0 | 0 |
| p10 | 0 | 0 | 0 |
| p25 | 0 | 0 | 1 |
| p50 | 0 | 0 | 2 |
| p75 | 0 | 0 | 3 |
| p90 | 0 | 0 | 4 |
| max | 0 | 0 | 6 |

### effective_exertion_slope_28d

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 196 | 14 | 1503 |
| mean | -0.0044 | -0.0884 | 0.0009 |
| std | 0.0279 | 0.0155 | 0.0364 |
| min | -0.0836 | -0.1167 | -0.1103 |
| p10 | -0.0375 | -0.1095 | -0.0458 |
| p25 | -0.0233 | -0.0979 | -0.0208 |
| p50 | -0.0061 | -0.0896 | 0.0024 |
| p75 | 0.0166 | -0.0746 | 0.0251 |
| p90 | 0.0347 | -0.0728 | 0.0433 |
| max | 0.0642 | -0.0621 | 0.1255 |

### above_baseline_streak

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1503 |
| mean | 0.52 | 0.29 | 0.86 |
| std | 0.71 | 0.59 | 1.30 |
| min | 0 | 0 | 0 |
| p10 | 0 | 0 | 0 |
| p25 | 0 | 0 | 0 |
| p50 | 0 | 0 | 0 |
| p75 | 1 | 0 | 1 |
| p90 | 1 | 1 | 3 |
| max | 4 | 2 | 9 |

### exertion_class (v3.1)

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| value | pre_corona | corona_infection | lc |
|---|---|---|---|
| (denom) | 217 | 14 | 1503 |
| none | 96 (44.2%) | 6 (42.9%) | 370 (24.6%) |
| very_light | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| light | 39 (18.0%) | 6 (42.9%) | 367 (24.4%) |
| moderate | 17 (7.8%) | 1 (7.1%) | 237 (15.8%) |
| heavy | 35 (16.1%) | 0 (0.0%) | 265 (17.6%) |
| very_heavy | 30 (13.8%) | 1 (7.1%) | 264 (17.6%) |
| (empty/NaN) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

### exertion_class_lagged (v3.2 all-era)

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| value | pre_corona | corona_infection | lc |
|---|---|---|---|
| (denom) | 217 | 14 | 1503 |
| none | 59 (27.2%) | 9 (64.3%) | 375 (25.0%) |
| very_light | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| light | 23 (10.6%) | 4 (28.6%) | 394 (26.2%) |
| moderate | 13 (6.0%) | 0 (0.0%) | 199 (13.2%) |
| heavy | 26 (12.0%) | 0 (0.0%) | 278 (18.5%) |
| very_heavy | 26 (12.0%) | 1 (7.1%) | 257 (17.1%) |
| (empty/NaN) | 70 (32.3%) | 0 (0.0%) | 0 (0.0%) |

### exertion_class_lagged_lcera (v3.2 LC-era-only)

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| value | pre_corona | corona_infection | lc |
|---|---|---|---|
| (denom) | 217 | 14 | 1503 |
| none | 0 (0.0%) | 0 (0.0%) | 351 (23.4%) |
| very_light | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| light | 0 (0.0%) | 0 (0.0%) | 352 (23.4%) |
| moderate | 0 (0.0%) | 0 (0.0%) | 198 (13.2%) |
| heavy | 0 (0.0%) | 0 (0.0%) | 276 (18.4%) |
| very_heavy | 0 (0.0%) | 0 (0.0%) | 256 (17.0%) |
| (empty/NaN) | 217 (100.0%) | 14 (100.0%) | 70 (4.7%) |

---

## Garmin stress spikes + sleep (gated on respective flags)

### max_spike_minutes

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 216 | 14 | 1507 |
| mean | 12.3 | 17 | 12.3 |
| std | 14.7 | 19.3 | 12.9 |
| min | 0 | 0 | 0 |
| p10 | 0 | 1.5 | 0 |
| p25 | 5 | 5.2 | 5 |
| p50 | 8.5 | 11 | 9 |
| p75 | 15 | 21.5 | 16 |
| p90 | 31 | 31.4 | 28 |
| max | 116 | 77 | 119 |

### stress_mean_sleep

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 215 | 14 | 1478 |
| mean | 17.38 | 24.70 | 20.05 |
| std | 8.51 | 14.63 | 6.32 |
| min | 4.58 | 11.25 | 7.87 |
| p10 | 7.98 | 11.60 | 13.83 |
| p25 | 11.31 | 14.58 | 16.39 |
| p50 | 15.95 | 20.31 | 19.27 |
| p75 | 21.93 | 27.35 | 22.46 |
| p90 | 27.12 | 43.20 | 26.51 |
| max | 55.05 | 63.55 | 73.00 |

### stress_stdev_sleep

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 215 | 14 | 1478 |
| mean | 9.99 | 11.41 | 8.01 |
| std | 4.64 | 5.18 | 2.75 |
| min | 3.49 | 5.93 | 4.33 |
| p10 | 5.37 | 6.77 | 5.47 |
| p25 | 6.51 | 7.51 | 6.13 |
| p50 | 8.77 | 9.18 | 7.19 |
| p75 | 12.38 | 14.77 | 9.17 |
| p90 | 16.30 | 19.95 | 11.65 |
| max | 30.22 | 21.65 | 24.78 |

### sleep_duration_min

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 215 | 14 | 1478 |
| mean | 520.4 | 547.6 | 613.9 |
| std | 64.2 | 71.3 | 85.6 |
| min | 359 | 387 | 247 |
| p10 | 442 | 446.8 | 497 |
| p25 | 476 | 529.5 | 564 |
| p50 | 514 | 557 | 622 |
| p75 | 558 | 585.5 | 670 |
| p90 | 596.6 | 622.1 | 713 |
| max | 722 | 661 | 951 |

### bedtime_hour_local

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 215 | 14 | 1478 |
| mean | 18.19 | 16.09 | 20.39 |
| std | 9.19 | 9.47 | 5.16 |
| min | 0 | 0.32 | 0 |
| p10 | 0.32 | 0.70 | 20.20 |
| p25 | 21.85 | 7.05 | 20.78 |
| p50 | 22.77 | 21.51 | 21.52 |
| p75 | 23.35 | 22.38 | 22.35 |
| p90 | 23.69 | 23.01 | 23.12 |
| max | 23.97 | 23.33 | 23.98 |

### bedtime_std_7d

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 214 | 14 | 1478 |
| mean | 0.62 | 0.94 | 0.90 |
| std | 0.22 | 0.12 | 0.26 |
| min | 0.28 | 0.67 | 0.13 |
| p10 | 0.42 | 0.79 | 0.55 |
| p25 | 0.46 | 0.85 | 0.73 |
| p50 | 0.57 | 0.97 | 0.91 |
| p75 | 0.73 | 1.01 | 1.07 |
| p90 | 0.85 | 1.06 | 1.22 |
| max | 1.32 | 1.09 | 1.79 |

---

## Wiggers enrichments - all-day stress (gated on has_garmin_uds=True)

### all_day_stress_avg

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 216 | 14 | 1502 |
| mean | 30.69 | 36.14 | 33.09 |
| std | 6.94 | 6.82 | 6.17 |
| min | 15 | 24 | 16 |
| p10 | 22 | 30.60 | 26 |
| p25 | 26 | 32 | 29 |
| p50 | 30 | 33 | 33 |
| p75 | 35 | 41.50 | 36 |
| p90 | 38.50 | 46.50 | 41 |
| max | 54 | 48 | 69 |

### all_day_stress_max

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1502 |
| mean | 95.6 | 95.6 | 96.2 |
| std | 7.5 | 3.2 | 4.3 |
| min | 0 | 90 | 27 |
| p10 | 90 | 91.3 | 92 |
| p25 | 94 | 93 | 95 |
| p50 | 97 | 96 | 97 |
| p75 | 99 | 99 | 99 |
| p90 | 99 | 99 | 99 |
| max | 100 | 99 | 100 |

### awake_stress_avg

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 216 | 14 | 1502 |
| mean | 41.44 | 44.64 | 42.97 |
| std | 10.66 | 8.91 | 8.77 |
| min | 19 | 31 | 21 |
| p10 | 29 | 32.90 | 32 |
| p25 | 33 | 37.25 | 37 |
| p50 | 41 | 43.50 | 43 |
| p75 | 48 | 51.75 | 48 |
| p90 | 55.50 | 57.20 | 54 |
| max | 73 | 59 | 73 |

### awake_stress_max

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1502 |
| mean | 95.5 | 95.6 | 96.2 |
| std | 7.6 | 3.2 | 4.3 |
| min | 0 | 90 | 27 |
| p10 | 90 | 91.3 | 92 |
| p25 | 94 | 93 | 95 |
| p50 | 97 | 96 | 97 |
| p75 | 99 | 99 | 99 |
| p90 | 99 | 99 | 99 |
| max | 100 | 99 | 100 |

### asleep_stress_avg_uds

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 216 | 14 | 1492 |
| mean | 16.93 | 23.36 | 18.72 |
| std | 8.01 | 12.84 | 6.22 |
| min | 4 | 9 | 6 |
| p10 | 8 | 11 | 13 |
| p25 | 12 | 13.25 | 15 |
| p50 | 15 | 20 | 18 |
| p75 | 21 | 26.50 | 21 |
| p90 | 26.50 | 42.20 | 24 |
| max | 54 | 53 | 74 |

---

## Wiggers enrichments - Body Battery (gated on has_garmin_uds=True for 24h cols, sleep-window subset for sleep cols)

### bb_highest

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 216 | 14 | 1502 |
| mean | 80.2 | 70 | 76.2 |
| std | 19.3 | 24.7 | 16.4 |
| min | 14 | 23 | 12 |
| p10 | 49 | 35.2 | 53.1 |
| p25 | 70.8 | 55.8 | 67 |
| p50 | 85 | 67.5 | 79 |
| p75 | 97.2 | 93.8 | 88 |
| p90 | 100 | 99.1 | 96 |
| max | 100 | 100 | 100 |

### bb_lowest

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 216 | 14 | 1502 |
| mean | 13.5 | 14.8 | 19.8 |
| std | 8.3 | 9.4 | 9.0 |
| min | 5 | 5 | 5 |
| p10 | 5 | 5 | 8 |
| p25 | 6 | 5 | 14 |
| p50 | 12 | 14.5 | 19 |
| p75 | 18 | 20 | 26 |
| p90 | 24 | 25.4 | 32 |
| max | 49 | 36 | 69 |

### bb_charged_24h

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 216 | 14 | 1502 |
| mean | 68.0 | 53.1 | 55.2 |
| std | 17.5 | 17.4 | 15.5 |
| min | 7 | 18 | 0 |
| p10 | 46.5 | 29.6 | 36 |
| p25 | 58 | 44.5 | 46 |
| p50 | 68.5 | 56.5 | 57 |
| p75 | 80 | 61.8 | 65 |
| p90 | 87 | 74.9 | 74 |
| max | 130 | 81 | 97 |

### bb_drained_24h

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 216 | 14 | 1502 |
| mean | 67.7 | 55.9 | 55.7 |
| std | 19.8 | 19.6 | 15.4 |
| min | 15 | 14 | 0 |
| p10 | 41 | 33.3 | 36 |
| p25 | 54.8 | 47.2 | 46 |
| p50 | 70.5 | 53.5 | 57 |
| p75 | 82 | 69.5 | 66 |
| p90 | 92 | 79.4 | 74.9 |
| max | 107 | 86 | 93 |

### bb_during_sleep_value

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | -- | -- | 861 |
| mean | -- | -- | 50.4 |
| std | -- | -- | 12.9 |
| min | -- | -- | 3 |
| p10 | -- | -- | 33 |
| p25 | -- | -- | 43 |
| p50 | -- | -- | 51 |
| p75 | -- | -- | 60 |
| p90 | -- | -- | 66 |
| max | -- | -- | 82 |

### bb_sleep_start_value

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | -- | -- | 667 |
| mean | -- | -- | 27.9 |
| std | -- | -- | 12.3 |
| min | -- | -- | 5 |
| p10 | -- | -- | 14 |
| p25 | -- | -- | 19 |
| p50 | -- | -- | 26 |
| p75 | -- | -- | 35 |
| p90 | -- | -- | 44 |
| max | -- | -- | 87 |

### bb_sleep_end_value

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | -- | -- | 593 |
| mean | -- | -- | 76.2 |
| std | -- | -- | 15.3 |
| min | -- | -- | 26 |
| p10 | -- | -- | 55.2 |
| p25 | -- | -- | 69 |
| p50 | -- | -- | 78 |
| p75 | -- | -- | 87 |
| p90 | -- | -- | 94 |
| max | -- | -- | 100 |

### bb_overnight_gain

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | -- | -- | 593 |
| mean | -- | -- | 48.1 |
| std | -- | -- | 13.1 |
| min | -- | -- | 3 |
| p10 | -- | -- | 31 |
| p25 | -- | -- | 41 |
| p50 | -- | -- | 49 |
| p75 | -- | -- | 57 |
| p90 | -- | -- | 64 |
| max | -- | -- | 82 |

---

## Wiggers enrichments - respiration (rpm; 24h gated on has_garmin_uds, sleep on sleep_valid_flag)

### respiration_avg_waking

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 216 | 14 | 1502 |
| mean | 13.19 | 13.36 | 13.81 |
| std | 0.40 | 0.48 | 0.42 |
| min | 12 | 13 | 13 |
| p10 | 13 | 13 | 13 |
| p25 | 13 | 13 | 14 |
| p50 | 13 | 13 | 14 |
| p75 | 13 | 14 | 14 |
| p90 | 14 | 14 | 14 |
| max | 14 | 14 | 16 |

### respiration_min_24h

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 216 | 14 | 1502 |
| mean | 9.06 | 8.86 | 10.06 |
| std | 0.79 | 0.64 | 1.04 |
| min | 6 | 8 | 3 |
| p10 | 8 | 8 | 9 |
| p25 | 9 | 8.25 | 9 |
| p50 | 9 | 9 | 10 |
| p75 | 9 | 9 | 11 |
| p90 | 10 | 9.70 | 11 |
| max | 12 | 10 | 13 |

### respiration_max_24h

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 216 | 14 | 1502 |
| mean | 18.45 | 18.79 | 18.94 |
| std | 1.93 | 1.66 | 2.19 |
| min | 15 | 17 | 14 |
| p10 | 16 | 17 | 17 |
| p25 | 17 | 17.25 | 17 |
| p50 | 18 | 18 | 18 |
| p75 | 20 | 20 | 20 |
| p90 | 21 | 21 | 22 |
| max | 25 | 22 | 27 |

### respiration_avg_sleep

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 215 | 14 | 1474 |
| mean | 13.31 | 13.57 | 13.75 |
| std | 0.58 | 0.62 | 0.57 |
| min | 12 | 13 | 12 |
| p10 | 13 | 13 | 13 |
| p25 | 13 | 13 | 13 |
| p50 | 13 | 13.50 | 14 |
| p75 | 14 | 14 | 14 |
| p90 | 14 | 14 | 14.10 |
| max | 15 | 15 | 17 |

### respiration_min_sleep

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 215 | 14 | 1474 |
| mean | 9.39 | 9 | 10.54 |
| std | 1.08 | 1 | 1.10 |
| min | 7 | 8 | 6 |
| p10 | 8 | 8 | 9 |
| p25 | 9 | 8.25 | 10 |
| p50 | 9 | 9 | 11 |
| p75 | 10 | 9 | 11 |
| p90 | 11 | 9.70 | 12 |
| max | 12 | 12 | 13 |

### respiration_max_sleep

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 215 | 14 | 1474 |
| mean | 17.25 | 17.93 | 17.87 |
| std | 1.80 | 1.53 | 2.38 |
| min | 15 | 16 | 14 |
| p10 | 16 | 16 | 16 |
| p25 | 16 | 17 | 16 |
| p50 | 17 | 18 | 17 |
| p75 | 18 | 18.75 | 18 |
| p90 | 20 | 20 | 21 |
| max | 25 | 21 | 27 |

---

## Wiggers enrichments - sleep stages (gated on sleep_valid_flag=True; minutes)

### sleep_deep_min

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 215 | 14 | 1474 |
| mean | 29.5 | 41.5 | 61.2 |
| std | 22.9 | 24.1 | 41.7 |
| min | 0 | 0 | 0 |
| p10 | 0 | 10.1 | 15 |
| p25 | 9.5 | 23.8 | 33 |
| p50 | 28 | 42.5 | 58 |
| p75 | 46.5 | 62 | 82 |
| p90 | 63 | 70 | 108 |
| max | 92 | 77 | 442 |

### sleep_light_min

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 215 | 14 | 1474 |
| mean | 319.1 | 360.7 | 439.7 |
| std | 56.5 | 72.8 | 83.2 |
| min | 172 | 188 | 0 |
| p10 | 252 | 269.9 | 335 |
| p25 | 284.5 | 321.5 | 394 |
| p50 | 318 | 385.5 | 448 |
| p75 | 352.5 | 407.8 | 493.8 |
| p90 | 387 | 440.4 | 537 |
| max | 483 | 456 | 713 |

### sleep_awake_min

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 215 | 14 | 1474 |
| mean | 6.5 | 5.5 | 5.5 |
| std | 7.1 | 4.5 | 7.6 |
| min | 0 | 0 | 0 |
| p10 | 0 | 0.3 | 0 |
| p25 | 2 | 2.2 | 1 |
| p50 | 4 | 4 | 3 |
| p75 | 9 | 8.5 | 7 |
| p90 | 15 | 12.4 | 13 |c:\tmp\lc_phase_descriptive.py:127: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  vals = sub[col].fillna("").astype(str)

| max | 44 | 14 | 126 |

### sleep_unmeasurable_min

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 215 | 14 | 1474 |
| mean | 0.3 | 0.8 | 0.8 |
| std | 2.5 | 2.8 | 5.7 |
| min | 0 | 0 | 0 |
| p10 | 0 | 0 | 0 |
| p25 | 0 | 0 | 0 |
| p50 | 0 | 0 | 0 |
| p75 | 0 | 0 | 0 |
| p90 | 0 | 0 | 0 |
| max | 21 | 11 | 82 |

---

## Wiggers enrichments - SpO2 (percent; 24h gated on has_garmin_uds, sleep on sleep_valid_flag)

### spo2_avg_24h

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1457 |
| mean | 95.28 | 95.14 | 93.60 |
| std | 1.06 | 0.52 | 1.24 |
| min | 92 | 94 | 88 |
| p10 | 94 | 95 | 92 |
| p25 | 95 | 95 | 93 |
| p50 | 95 | 95 | 94 |
| p75 | 96 | 95 | 94 |
| p90 | 97 | 96 | 95 |
| max | 98 | 96 | 98 |

### spo2_min_24h

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1457 |
| mean | 86.07 | 86.50 | 84.76 |
| std | 2.53 | 1.92 | 3.25 |
| min | 76 | 84 | 72 |
| p10 | 83 | 84 | 81 |
| p25 | 85 | 85 | 83 |
| p50 | 86 | 86 | 85 |
| p75 | 88 | 88 | 87 |
| p90 | 89 | 88.70 | 88 |
| max | 93 | 90 | 97 |

### spo2_avg_sleep

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 212 | 14 | 1292 |
| mean | 95.25 | 95 | 93.56 |
| std | 1.06 | 0.65 | 1.17 |
| min | 92 | 94 | 88.94 |
| p10 | 94 | 94 | 92 |
| p25 | 95 | 95 | 93 |
| p50 | 95 | 95 | 94 |
| p75 | 96 | 95 | 94 |
| p90 | 97 | 96 | 95 |
| max | 98 | 96 | 98 |

### spo2_min_sleep

*Gated on `sleep_valid_flag=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 212 | 14 | 1292 |
| mean | 86.08 | 86.43 | 84.27 |
| std | 2.60 | 1.88 | 2.78 |
| min | 76 | 84 | 72 |
| p10 | 83 | 84 | 81 |
| p25 | 85 | 85 | 83 |
| p50 | 86 | 86 | 84 |
| p75 | 88 | 88 | 86 |
| p90 | 89 | 88.70 | 87 |
| max | 94 | 90 | 93 |

---

## Wiggers enrichments - intraday HR features (FIT-derived, waking-period; gated on has_garmin_uds=True)

*The threshold-based columns (`*_above_daytime_baseline_*`) use the user's own*
*rolling daytime HR baseline (`hr_daytime_baseline_lagged`) + 20 bpm. See*
*DATA_DICTIONARY.md sec 5 + methodology/garmin_indicators_audit.md for the rationale*
*(replaces the prior sleep-RHR-based threshold which was too permissive for Wiggers A4).*

### hr_median_waking (today's median waking HR; no threshold)

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 217 | 14 | 1493 |
| mean | 72.3 | 72.2 | 77.2 |
| std | 8.2 | 6.4 | 5.4 |
| min | 57 | 63.5 | 60 |
| p10 | 64.6 | 67 | 71 |
| p25 | 67 | 67 | 73 |
| p50 | 71 | 71 | 77 |
| p75 | 75 | 77 | 80 |
| p90 | 81.4 | 79.7 | 84 |
| max | 133 | 87 | 100 |

### hr_daytime_baseline_lagged (rolling [d-90, d-30] baseline)

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 173 | 14 | 1501 |
| mean | 72.3 | 68.8 | 76.3 |
| std | 1.2 | 0.6 | 2.5 |
| min | 69 | 68 | 67.5 |
| p10 | 70.5 | 68 | 73 |
| p25 | 72 | 68.1 | 74 |
| p50 | 72 | 69 | 77 |
| p75 | 73 | 69 | 78 |
| p90 | 74 | 69.5 | 79 |
| max | 74 | 69.5 | 82 |

### hr_min_above_daytime_baseline_plus_20_waking

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 173 | 14 | 1501 |
| mean | 85.8 | 94.8 | 74.0 |
| std | 74.2 | 74.6 | 57.8 |
| min | 0 | 10 | 0 |
| p10 | 13.2 | 30.7 | 16 |
| p25 | 26 | 51.8 | 33 |
| p50 | 69 | 65 | 60 |
| p75 | 119 | 122.5 | 99 |
| p90 | 178.2 | 176.8 | 148 |
| max | 435 | 304 | 421 |

### hr_longest_elevated_run_min_waking

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 173 | 14 | 1501 |
| mean | 13.8 | 12.9 | 11.8 |
| std | 9.5 | 8.8 | 7.8 |
| min | 0 | 4 | 0 |
| p10 | 3 | 6 | 4 |
| p25 | 6 | 7.5 | 6 |
| p50 | 12 | 10.5 | 10 |
| p75 | 19 | 15 | 16 |
| p90 | 28 | 18.1 | 22 |
| max | 44 | 41 | 57 |

### hr_area_above_daytime_baseline_waking

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 173 | 14 | 1501 |
| mean | 3758.0 | 3319.9 | 2148.0 |
| std | 3633.8 | 4275.2 | 1869.5 |
| min | 0 | 260 | 0 |
| p10 | 330.2 | 764.8 | 414 |
| p25 | 695 | 1326 | 842 |
| p50 | 2460 | 1784.8 | 1644 |
| p75 | 5849 | 3223 | 2842 |
| p90 | 8484.8 | 5496.5 | 4480 |
| max | 19924 | 17808 | 14565.5 |

### hr_sustained_elevated_flag (categorical, all-era)

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| value | pre_corona | corona_infection | lc |
|---|---|---|---|
| (denom) | 217 | 14 | 1503 |
| False | 160 (73.7%) | 13 (92.9%) | 1454 (96.7%) |
| True | 13 (6.0%) | 1 (7.1%) | 47 (3.1%) |
| (empty/NaN) | 44 (20.3%) | 0 (0.0%) | 2 (0.1%) |

---

## Wiggers enrichments - intraday HR A4 (LC-era-only baseline; use for PEM-pacing analyses)

*The `_lcera` variants restrict the rolling baseline to dates >= LC_ERA_START (2022-04-04).*
*Pre-LC days are NaN by design. Effective fill from 2022-07-03 onwards (after 90-day warmup).*

### hr_daytime_baseline_lagged_lcera

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | -- | -- | 1457 |
| mean | -- | -- | 76.6 |
| std | -- | -- | 2.2 |
| min | -- | -- | 73 |
| p10 | -- | -- | 74 |
| p25 | -- | -- | 74.5 |
| p50 | -- | -- | 77 |
| p75 | -- | -- | 78 |
| p90 | -- | -- | 79 |
| max | -- | -- | 82 |

### hr_min_above_daytime_baseline_plus_20_waking_lcera

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | -- | -- | 1457 |
| mean | -- | -- | 72.6 |
| std | -- | -- | 57.4 |
| min | -- | -- | 0 |
| p10 | -- | -- | 16 |
| p25 | -- | -- | 32 |
| p50 | -- | -- | 59 |
| p75 | -- | -- | 97 |
| p90 | -- | -- | 146.4 |
| max | -- | -- | 421 |

### hr_longest_elevated_run_min_waking_lcera

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | -- | -- | 1457 |
| mean | -- | -- | 11.6 |
| std | -- | -- | 7.8 |
| min | -- | -- | 0 |
| p10 | -- | -- | 4 |
| p25 | -- | -- | 6 |
| p50 | -- | -- | 10 |
| p75 | -- | -- | 15 |
| p90 | -- | -- | 22 |
| max | -- | -- | 57 |

### hr_area_above_daytime_baseline_waking_lcera

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | -- | -- | 1457 |
| mean | -- | -- | 2106.5 |
| std | -- | -- | 1862.2 |
| min | -- | -- | 0 |
| p10 | -- | -- | 410.5 |
| p25 | -- | -- | 815 |
| p50 | -- | -- | 1613 |
| p75 | -- | -- | 2741 |
| p90 | -- | -- | 4387.2 |
| max | -- | -- | 14565.5 |

### hr_sustained_elevated_flag_lcera (categorical, LC-era-only)

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| value | pre_corona | corona_infection | lc |
|---|---|---|---|
| (denom) | 217 | 14 | 1503 |
| False | 0 (0.0%) | 0 (0.0%) | 1411 (93.9%) |c:\tmp\lc_phase_descriptive.py:348: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  n_true = int(slp["sleep_start_afternoon_flag"].fillna(False).astype(bool).sum())
c:\tmp\lc_phase_descriptive.py:348: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  n_true = int(slp["sleep_start_afternoon_flag"].fillna(False).astype(bool).sum())
c:\tmp\lc_phase_descriptive.py:348: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  n_true = int(slp["sleep_start_afternoon_flag"].fillna(False).astype(bool).sum())

| True | 0 (0.0%) | 0 (0.0%) | 46 (3.1%) |
| (empty/NaN) | 217 (100.0%) | 14 (100.0%) | 46 (3.1%) |

---

## Wiggers enrichments - intraday stress recovery (FIT-derived; gated on has_garmin_uds=True)

### stress_high_duration_min

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 216 | 14 | 1501 |
| mean | 58.5 | 70.4 | 73.1 |
| std | 50.3 | 48.3 | 57.2 |
| min | 1 | 2 | 0 |
| p10 | 11 | 22 | 16 |
| p25 | 22.8 | 26.2 | 30 |
| p50 | 45 | 75 | 58 |
| p75 | 78.2 | 98 | 100 |
| p90 | 124 | 103.9 | 151 |
| max | 269 | 192 | 373 |

### stress_post_peak_drop_avg

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 212 | 13 | 1490 |
| mean | 56.02 | 58.72 | 58.43 |
| std | 19.50 | 15.57 | 17.52 |
| min | 20.90 | 29.80 | 17.50 |
| p10 | 31.31 | 36.58 | 35.90 |
| p25 | 41.65 | 49.80 | 45.42 |
| p50 | 55.55 | 61.10 | 57.20 |
| p75 | 69.22 | 69 | 70.50 |
| p90 | 84.86 | 77.68 | 82.92 |
| max | 100 | 82.50 | 100 |

### stress_post_peak_time_to_rest_min

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 193 | 13 | 1310 |
| mean | 66.7 | 97.5 | 101.7 |
| std | 76.8 | 82.5 | 108.5 |
| min | 1 | 6 | 1 |
| p10 | 5 | 17.4 | 10 |
| p25 | 17 | 40 | 28 |
| p50 | 42 | 72 | 69.5 |
| p75 | 89 | 168 | 137 |
| p90 | 153.6 | 234.0 | 228.1 |
| max | 558 | 254 | 842 |

### stress_recovery_pct_within_2h

*Gated on `has_garmin_uds=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | 170 | 13 | 1337 |
| mean | 52.92 | 47.92 | 50.22 |
| std | 22.37 | 16.55 | 22.92 |
| min | 0 | 23.20 | 0 |
| p10 | 20.56 | 26.14 | 15.20 |
| p25 | 35.88 | 37.60 | 32.30 |
| p50 | 57.90 | 51.10 | 55.60 |
| p75 | 72.20 | 58.10 | 69.40 |
| p90 | 77.39 | 64.36 | 76.30 |
| max | 87.10 | 81.80 | 96 |

### sleep_start_afternoon_flag (True count, base rate within sleep_valid_flag=True)

| phase | sleep_valid_n | flag_True_n | base_rate |
|---|---|---|---|
| pre_corona | 215 | 46 | 21.40% |
| corona_infection | 14 | 4 | 28.57% |
| lc | 1478 | 94 | 6.36% |

---

## Subjective state (lc phase only)

*`gevoelscore` and notes only exist from 2022-09-03 onwards (corpus start).*
*pre_corona and corona_infection phases have no subjective data by design.*

### gevoelscore

*Gated on `has_score=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | -- | -- | 1372 |
| mean | -- | -- | 4.39 |
| std | -- | -- | 0.88 |
| min | -- | -- | 1 |
| p10 | -- | -- | 3 |
| p25 | -- | -- | 4 |
| p50 | -- | -- | 5 |
| p75 | -- | -- | 5 |
| p90 | -- | -- | 5 |
| max | -- | -- | 6 |

### Crash / dip flags (True count, base rate within phase)

| flag | pre_corona | corona_infection | lc |
|---|---|---|---|
| is_crash | 0 (0.00%) | 0 (0.00%) | 103 (6.76%) |
| is_dip | 0 (0.00%) | 0 (0.00%) | 79 (5.18%) |
| is_sub_threshold_dip | 0 (0.00%) | 0 (0.00%) | 35 (2.30%) |

---

## Note-categorisation (gated on has_note=True; lc phase only by construction)

### n_clauses

*Gated on `has_note=True`. Denominator within each phase = phase days where the gate is True.*

| stat | pre_corona | corona_infection | lc |
|---|---|---|---|
| n | -- | -- | 686 |
| mean | -- | -- | 3.51 |
| std | -- | -- | 2.80 |
| min | -- | -- | 1 |
| p10 | -- | -- | 1 |
| p25 | -- | -- | 2 |
| p50 | -- | -- | 3 |
| p75 | -- | -- | 5 |
| p90 | -- | -- | 7 |
| max | -- | -- | 22 |

### Positive-evidence density per category (among has_note=True days)

| category | pre_corona | corona_infection | lc |
|---|---|---|---|
| cat_symptoom_fysiek | -- (no note-days) | -- (no note-days) | 477 (69.5%) |
| cat_context_neutraal | -- (no note-days) | -- (no note-days) | 481 (70.1%) |
| cat_sub_systemisch_vermoeid | -- (no note-days) | -- (no note-days) | 343 (50.0%) |
| cat_sub_hoofdpijn | -- (no note-days) | -- (no note-days) | 236 (34.4%) |
| cat_belasting_gezin | -- (no note-days) | -- (no note-days) | 136 (19.8%) |
| cat_recovery_actie | -- (no note-days) | -- (no note-days) | 133 (19.4%) |
| cat_belasting_fysiek | -- (no note-days) | -- (no note-days) | 80 (11.7%) |
| cat_symptoom_cognitief | -- (no note-days) | -- (no note-days) | 45 (6.6%) |

---

*End of per-phase descriptive summary. Next: regenerate this doc when the master changes (column additions, era boundary updates).*
