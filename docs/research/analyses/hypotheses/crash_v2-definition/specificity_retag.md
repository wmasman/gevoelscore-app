# Specificity re-tag — H02b false positives under crash_v2

Reproduces H02b's specificity-check null sample (seed `20260605`) and re-tags each false-positive window (delta >= +10 min) with crash_v2 labels.

**Key question:** the original specificity check tagged 32/83 false positives as `near_miss` (any score-3 day in window). With crash_v2, those score-3 days should now be labelled `dip`. Does the mapping hold?

## Counts

- Null sample size: **200**

- False positives (delta >= +10): **83** (42%)


### Cross-tab: `near_miss` (orig) vs `v2_dip_in_window` (new)

| | v2_dip=True | v2_dip=False | total |
|---|---:|---:|---:|
| **near_miss=True**  | 20 | 12 | 32 |
| **near_miss=False** | 0 | 51 | 51 |
| **total** | 20 | 63 | 83 |

**How to read:** the (True, True) cell counts windows where the old `near_miss` tag is now confirmed by a v2 dip label. (True, False) = old `near_miss` but no v2 dip — these are score-3 days that are part of a crash episode (tier-1) or in a crash recovery shadow. (False, True) = NEW dips that weren't near_miss (likely v2 dip with score 1 or 2, which the old NEAR_MISS_SCORE=3 rule missed).


## Per-window detail (sorted by delta, descending)

| ref | delta | scores [d-3,d-2,d-1,ref] | near_miss (orig) | v2_dip_in_window | v2_dip_days | days_to_crash | tags |
|---|---:|---|---|---|---|---:|---|
| 2026-01-24 | +96.9 | 5,6,5,6 | — | — | — | +108 | unexplained |
| 2023-11-18 | +78.6 | 4,3,2,5 | YES | — | — | -6 | near_miss, close_to_crash |
| 2024-03-30 | +77.6 | 4,4,4,3 | YES | YES | 2024-03-30 | +31 | near_miss, v2_dip |
| 2025-10-29 | +71.4 | 5,5,5,5 | — | — | — | -27 | unexplained |
| 2026-01-09 | +61.0 | 5,4,5,5 | — | — | — | -99 | unexplained |
| 2024-07-12 | +59.5 | 3,5,4,5 | YES | YES | 2024-07-11 | +3 | near_miss, v2_dip, close_to_crash |
| 2026-02-11 | +56.7 | 5,5,4,3 | YES | YES | 2026-02-11 | +90 | near_miss, v2_dip |
| 2023-05-15 | +54.9 | 5,5,3,5 | YES | YES | 2023-05-12 | +13 | near_miss, v2_dip, close_to_crash |
| 2023-05-16 | +54.8 | 5,5,5,4 | — | — | — | +12 | close_to_crash |
| 2023-05-17 | +54.7 | 4,5,5,5 | — | — | — | +11 | close_to_crash |
| 2025-07-08 | +51.1 | 5,4,5,5 | — | — | — | -75 | unexplained |
| 2024-10-24 | +45.2 | 4,4,4,3 | YES | YES | 2024-10-24 | -56 | near_miss, v2_dip |
| 2024-10-24 | +45.2 | 4,4,4,3 | YES | YES | 2024-10-24 | -56 | near_miss, v2_dip |
| 2023-12-01 | +44.0 | 1,1,3,1 | YES | — | — | -4 | near_miss, close_to_crash |
| 2023-12-01 | +44.0 | 1,1,3,1 | YES | — | — | -4 | near_miss, close_to_crash |
| 2023-03-02 | +41.6 | 5,5,5,5 | — | — | — | -26 | unexplained |
| 2023-03-03 | +41.4 | 5,5,5,6 | — | — | — | -27 | unexplained |
| 2026-01-16 | +39.5 | 6,5,5,5 | — | — | — | -106 | unexplained |
| 2024-03-13 | +38.3 | 5,4,5,5 | — | — | — | -17 | unexplained |
| 2026-02-19 | +37.5 | 4,4,5,4 | — | — | — | +82 | unexplained |
| 2025-03-30 | +37.2 | 5,5,4,4 | — | — | — | +25 | unexplained |
| 2023-07-08 | +35.8 | 5,5,5,3 | YES | YES | 2023-07-08 | -26 | near_miss, v2_dip |
| 2025-01-19 | +33.2 | 4,4,5,4 | — | — | — | -27 | unexplained |
| 2025-01-21 | +32.9 | 3,4,4,5 | YES | YES | 2025-01-20 | -29 | near_miss, v2_dip |
| 2024-11-01 | +31.9 | 5,4,4,5 | — | — | — | +52 | unexplained |
| 2023-10-06 | +31.8 | 4,4,3,4 | YES | — | — | -9 | near_miss, close_to_crash |
| 2026-02-15 | +31.7 | 4,4,5,3 | YES | YES | 2026-02-15 | +86 | near_miss, v2_dip |
| 2023-10-07 | +31.7 | 4,4,4,3 | YES | YES | 2023-10-07 | -10 | near_miss, v2_dip, close_to_crash |
| 2025-06-07 | +31.6 | 6,6,4,6 | — | — | — | -44 | unexplained |
| 2025-08-09 | +31.4 | 4,5,5,4 | — | — | — | +54 | unexplained |
| 2025-08-10 | +31.1 | 4,4,5,5 | — | — | — | +53 | unexplained |
| 2026-05-01 | +30.8 | 3,4,5,5 | YES | YES | 2026-04-30 | +11 | near_miss, v2_dip, close_to_crash |
| 2025-04-04 | +30.2 | 4,5,5,4 | — | — | — | +20 | unexplained |
| 2026-04-12 | +29.3 | 5,4,5,5 | — | — | — | +30 | unexplained |
| 2023-11-09 | +28.6 | 4,4,4,4 | — | — | — | +3 | close_to_crash |
| 2024-12-06 | +28.0 | 5,5,5,5 | — | — | — | +17 | unexplained |
| 2023-07-14 | +27.8 | 5,5,5,5 | — | — | — | -32 | unexplained |
| 2023-07-13 | +27.7 | 5,5,5,5 | — | — | — | -31 | unexplained |
| 2022-12-23 | +27.2 | 5,4,4,5 | — | — | — | +4 | close_to_crash |
| 2023-05-25 | +26.1 | 4,4,3,5 | YES | YES | 2023-05-22 | +3 | near_miss, v2_dip, close_to_crash |
| 2025-07-26 | +25.9 | 4,6,5,6 | — | — | — | +68 | unexplained |
| 2023-04-20 | +25.4 | 4,5,5,5 | — | — | — | -18 | unexplained |
| 2024-02-22 | +24.7 | 4,5,3,4 | YES | — | — | +3 | near_miss, close_to_crash |
| 2026-01-14 | +24.5 | 5,5,4,5 | — | — | — | -104 | unexplained |
| 2026-04-10 | +23.4 | 5,4,5,4 | — | — | — | +32 | unexplained |
| 2024-10-17 | +23.0 | 4,4,5,4 | — | — | — | -49 | unexplained |
| 2023-08-03 | +22.8 | 5,4,4,5 | — | — | — | +35 | unexplained |
| 2023-08-05 | +22.7 | 5,5,5,5 | — | — | — | +33 | unexplained |
| 2023-08-05 | +22.7 | 5,5,5,5 | — | — | — | +33 | unexplained |
| 2026-02-02 | +22.6 | 5,5,6,5 | — | — | — | +99 | unexplained |
| 2023-06-03 | +22.6 | 2,3,4,3 | YES | — | — | -6 | near_miss, close_to_crash |
| 2025-06-10 | +22.0 | 4,5,6,5 | — | — | — | -47 | unexplained |
| 2022-12-30 | +21.6 | 3,3,2,3 | YES | — | — | -3 | near_miss |
| 2024-10-26 | +18.2 | 4,3,4,5 | YES | YES | 2024-10-24 | -58 | near_miss, v2_dip |
| 2024-10-26 | +18.2 | 4,3,4,5 | YES | YES | 2024-10-24 | -58 | near_miss, v2_dip |
| 2023-03-20 | +17.9 | 4,3,4,5 | YES | YES | 2023-03-18 | +13 | near_miss, v2_dip, close_to_crash |
| 2025-11-19 | +17.8 | 6,5,5,4 | — | — | — | -48 | unexplained |
| 2024-12-07 | +17.8 | 5,5,5,4 | — | — | — | +16 | unexplained |
| 2023-06-15 | +16.4 | 4,3,3,5 | YES | — | — | -3 | near_miss |
| 2022-11-15 | +16.4 | 5,5,5,5 | — | — | — | +8 | close_to_crash |
| 2024-04-18 | +16.3 | 5,3,5,5 | YES | YES | 2024-04-16 | +12 | near_miss, v2_dip, close_to_crash |
| 2023-05-10 | +16.3 | 5,4,4,5 | — | — | — | +18 | unexplained |
| 2022-09-08 | +15.9 | 4,4,4,3 | YES | — | — | -5 | near_miss, close_to_crash |
| 2024-03-20 | +14.1 | 3,5,4,5 | YES | YES | 2024-03-19 | -24 | near_miss, v2_dip |
| 2026-02-27 | +13.9 | 4,4,5,3 | YES | YES | 2026-02-27 | +74 | near_miss, v2_dip |
| 2023-01-15 | +13.9 | 4,5,5,5 | — | — | — | -19 | unexplained |
| 2025-05-15 | +13.5 | 4,6,5,5 | — | — | — | -21 | unexplained |
| 2022-09-11 | +13.5 | 2,4,3,5 | YES | — | — | +5 | near_miss, close_to_crash |
| 2024-12-01 | +13.0 | 5,5,3,5 | YES | YES | 2024-11-28 | +22 | near_miss, v2_dip |
| 2024-12-02 | +13.0 | 5,5,5,4 | — | — | — | +21 | unexplained |
| 2023-08-29 | +12.7 | 4,4,4,5 | — | — | — | +9 | close_to_crash |
| 2023-08-27 | +12.6 | 4,5,4,4 | — | — | — | +11 | close_to_crash |
| 2023-01-31 | +12.4 | 5,3,4,4 | YES | YES | 2023-01-29 | +4 | near_miss, v2_dip, close_to_crash |
| 2023-07-28 | +12.4 | 5,5,4,5 | — | — | — | +41 | unexplained |
| 2024-03-09 | +12.3 | 3,4,4,4 | YES | — | — | -13 | near_miss, close_to_crash |
| 2023-02-16 | +12.3 | 4,5,5,5 | — | — | — | -12 | close_to_crash |
| 2023-01-06 | +12.0 | 5,5,5,5 | — | — | — | -10 | close_to_crash |
| 2023-01-07 | +11.9 | 5,5,5,5 | — | — | — | -11 | close_to_crash |
| 2024-08-08 | +11.1 | 5,5,5,5 | — | — | — | +21 | unexplained |
| 2025-09-05 | +11.0 | 5,4,6,5 | — | — | — | +27 | unexplained |
| 2024-08-07 | +10.9 | 5,5,4,5 | — | — | — | +22 | unexplained |
| 2025-03-24 | +10.9 | 4,4,5,5 | — | — | — | +31 | unexplained |
| 2023-06-07 | +10.0 | 3,3,2,3 | YES | — | — | +5 | near_miss, close_to_crash |

---

*Generated 2026-06-06. Same null sample as H02b/specificity-check.md.*