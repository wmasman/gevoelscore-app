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

| stat | pre_corona | corona_infection | lc |c:\tmp\lc_phase_descriptive.py:234: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  n_true = int(slp["sleep_start_afternoon_flag"].fillna(False).astype(bool).sum())
c:\tmp\lc_phase_descriptive.py:234: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  n_true = int(slp["sleep_start_afternoon_flag"].fillna(False).astype(bool).sum())
c:\tmp\lc_phase_descriptive.py:234: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  n_true = int(slp["sleep_start_afternoon_flag"].fillna(False).astype(bool).sum())

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
