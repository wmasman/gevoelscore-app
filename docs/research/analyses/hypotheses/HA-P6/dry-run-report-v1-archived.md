# HA-P6 -- dry-run report

*Generated 2026-06-17 by `script.py --dry-run` per spec Sec 10.4 step 1.*

## Episode counts

- Pooled LC-era crash_v2 episodes: **29**
- Per-phase episode counts (after Sec 6 buildup CPAP buffer):
  - pooled: 29
  - unmedicated: 18
  - buildup: 3
  - consolidation: 6
  - afbouw: 2
  - post_afbouw: 0
- bb_overnight_gain post-2024-09-18 episodes: **5**
- Arm A matches (within +/- 2.0 tolerance ladder): **27 / 29**
- Arm A tolerance ladder used: +/-1.0: 15, +/-2.0: 12

## E[L]* per channel (pooled LC baseline pool)

| channel | E[L]* (days) | flag (Sec 7 [3.5, 10.5]) | note |
|---|---:|---|---|
| stress_mean_sleep | 6.50 | ok |  |
| all_day_stress_avg | 22.21 | FLAG |  |
| bb_lowest | 7.00 | ok | No clear ACF cutoff (all lags within max_lag are significant); returning default |
| bb_overnight_gain | 7.00 | ok | Closed-form formula degenerate; returning default |
| resting_hr | 7.00 | ok | No clear ACF cutoff (all lags within max_lag are significant); returning default |
| gevoelscore | 7.00 | ok | Closed-form formula degenerate; returning default |
| stress_low_motion_min_count_S60_Mlow | 30.72 | FLAG |  |

## Sanity-check verdict

**HALT** -- one or more sanity checks fired:
- channel all_day_stress_avg E[L]*=22.21 outside [3.5, 10.5] (Sec 7)
- channel stress_low_motion_min_count_S60_Mlow E[L]*=30.72 outside [3.5, 10.5] (Sec 7)

Per spec Sec 10.4 step 1 + Sec 7, the spec requires revision before the full characterisation can run. **No spec edits in this session per Sec 3.9 step 4** of the lock-process MD; the implied next step is to draft HA-P6-v2 in a separate session.

## Episode roster

| # | start | end | duration (d) | phase | t0 (episode-end) | t0 (last-below-threshold) |
|---:|---|---|---:|---|---|---|
| 1 | 2022-09-03 | 2022-09-04 | 2 | unmedicated | 2022-09-04 | 2022-09-03 |
| 2 | 2022-09-16 | 2022-09-24 | 9 | unmedicated | 2022-09-24 | 2022-09-23 |
| 3 | 2022-09-30 | 2022-10-01 | 2 | unmedicated | 2022-10-01 | 2022-09-30 |
| 4 | 2022-11-23 | 2022-11-25 | 3 | unmedicated | 2022-11-25 | 2022-11-24 |
| 5 | 2022-12-27 | 2022-12-30 | 4 | unmedicated | 2022-12-30 | 2022-12-27 |
| 6 | 2023-02-04 | 2023-02-08 | 5 | unmedicated | 2023-02-08 | 2023-02-05 |
| 7 | 2023-04-02 | 2023-04-03 | 2 | unmedicated | 2023-04-03 | 2023-04-02 |
| 8 | 2023-05-28 | 2023-06-07 | 11 | unmedicated | 2023-06-07 | 2023-06-04 |
| 9 | 2023-06-12 | 2023-06-13 | 2 | unmedicated | 2023-06-13 | 2023-06-13 |
| 10 | 2023-09-07 | 2023-09-08 | 2 | unmedicated | 2023-09-08 | 2023-09-08 |
| 11 | 2023-09-16 | 2023-09-17 | 2 | unmedicated | 2023-09-17 | 2023-09-17 |
| 12 | 2023-09-27 | 2023-09-28 | 2 | unmedicated | 2023-09-28 | 2023-09-27 |
| 13 | 2023-11-12 | 2023-11-16 | 5 | unmedicated | 2023-11-16 | 2023-11-15 |
| 14 | 2023-11-27 | 2023-12-10 | 14 | unmedicated | 2023-12-10 | 2023-12-01 |
| 15 | 2024-01-12 | 2024-01-13 | 2 | unmedicated | 2024-01-13 | 2024-01-13 |
| 16 | 2024-01-21 | 2024-01-22 | 2 | unmedicated | 2024-01-22 | 2024-01-22 |
| 17 | 2024-02-15 | 2024-02-16 | 2 | unmedicated | 2024-02-16 | 2024-02-16 |
| 18 | 2024-02-25 | 2024-03-02 | 7 | unmedicated | 2024-03-02 | 2024-03-02 |
| 19 | 2024-04-30 | 2024-05-01 | 2 | buildup | 2024-05-01 | 2024-05-01 |
| 20 | 2024-05-28 | 2024-05-29 | 2 | buildup | 2024-05-29 | 2024-05-28 |
| 21 | 2024-06-18 | 2024-06-19 | 2 | buildup | 2024-06-19 | 2024-06-19 |
| 22 | 2024-06-25 | 2024-06-26 | 2 | consolidation | 2024-06-26 | 2024-06-25 |
| 23 | 2024-07-15 | 2024-07-17 | 3 | consolidation | 2024-07-17 | 2024-07-16 |
| 24 | 2024-08-29 | 2024-08-30 | 2 | consolidation | 2024-08-30 | 2024-08-30 |
| 25 | 2024-12-23 | 2024-12-26 | 4 | consolidation | 2024-12-26 | 2024-12-25 |
| 26 | 2025-04-24 | 2025-04-25 | 2 | consolidation | 2025-04-25 | 2025-04-25 |
| 27 | 2025-10-02 | 2025-10-03 | 2 | consolidation | 2025-10-03 | 2025-10-03 |
| 28 | 2026-05-12 | 2026-05-13 | 2 | afbouw | 2026-05-13 | 2026-05-12 |
| 29 | 2026-05-20 | 2026-05-21 | 2 | afbouw | 2026-05-21 | 2026-05-21 |

