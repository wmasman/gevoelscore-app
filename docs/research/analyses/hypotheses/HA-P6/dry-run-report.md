# HA-P6 v3 -- dry-run report

*Generated 2026-06-17 by `script.py --dry-run` per spec Sec 10.4 step 1 of the v3 LOCKED pre-registration.*

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

## v3 §4.8.1 four-verdict E[L]* policy (Series A + Series B)

| channel | verdict (A) | E[L]\* (A pooled-LC) | verdict (B) | E[L]\* (B unmed) | E[L] used | binds | cap | note (A) |
|---|---|---:|---|---:|---:|:---:|:---:|---|
| stress_mean_sleep | FAIL | 19.65 | PASS-real | 4.83 | 5 | B | no | -- |
| all_day_stress_avg | FAIL | 26.60 | PASS-fallback-degenerate | 7.00 | 21 | A | yes | -- |
| bb_lowest | PASS-fallback-no-cutoff | 7.00 | FAIL | 18.40 | 14 | A | no | No clear ACF cutoff (all lags within max_lag are significant... |
| bb_overnight_gain | PASS-real | 6.54 | PASS-fallback-degenerate | 7.00 | 7 | A | no | -- |
| resting_hr | PASS-fallback-no-cutoff | 7.00 | PASS-fallback-no-cutoff | 7.00 | 14 | A | no | No clear ACF cutoff (all lags within max_lag are significant... |
| gevoelscore | PASS-fallback-degenerate | 7.00 | PASS-fallback-degenerate | 7.00 | 7 | A | no | Closed-form formula degenerate; returning default |
| stress_low_motion_min_count_S60_Mlow | PASS-real | 5.99 | PASS-fallback-degenerate | 7.00 | 7 | A | no | -- |

Series A n (pooled-LC daily non-crash days): 1377; Series B n (unmedicated stratum daily non-crash days): 635.

## v3 sanity-check verdict

**PASS** -- all v3 Sec 7 sanity checks satisfied. Proceeding to full run per Sec 10.4 step 2.

v3 dispositions (proceed-ready, no halt):
- stress_mean_sleep: FAIL (Series A E[L]*=19.65 → E[L]_used=5, binds Series B)
- all_day_stress_avg: FAIL (Series A E[L]*=26.60 → E[L]_used=21, binds Series A; CAP-BINDING)
- bb_lowest: PASS-fallback-no-cutoff (Series A E[L]*=7.00 → E[L]_used=14, binds Series A)
- resting_hr: PASS-fallback-no-cutoff (Series A E[L]*=7.00 → E[L]_used=14, binds Series A)
- gevoelscore: PASS-fallback-degenerate (Series A E[L]*=7.00 → E[L]_used=7, binds Series A)

## Episode roster

| # | start | end | duration (d) | phase | t0 (episode-end) | t0 (last-below) |
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

