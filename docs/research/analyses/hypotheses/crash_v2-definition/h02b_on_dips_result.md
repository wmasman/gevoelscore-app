# H02b on dips — spike-precursor test against crash_v2 tier-2

Re-run of H02b's metric (lead-up max stress spike vs 90-day trimmed baseline) using **single-day isolated dips** instead of multi-day crash episodes as reference events. Same null sample seed, same criteria, same windows.

## Question

Do isolated single-day dips show the same +10-minute spike-precursor pattern as crashes? If yes, the spike precursor is a generic 'bad day' marker. If no, it is specifically a multi-day-crash phenomenon.

## Reference for comparison (from H02b/result.md)

| | train (14 crashes) | validate (15 crashes) |
|---|---:|---:|
| % crash lead-ups with delta >= +10 min | 71.4% | 33.3% |
| discrimination vs null (pp) | +29.9 | -8.2 |
| median delta_spike_minutes | +16.2 | +6.7 |
| verdict | SUPPORTED | refuted |

## Dip results

| | train | validate |
|---|---:|---:|
| dips in window | 27 | 52 |
| clean dips (valid lead-up + baseline) | 27 | 52 |
| null sample size | 200 | 200 |
| % dip lead-ups with delta >= +10 min | 48.1% | 44.2% |
| % null windows with delta >= +10 min | 39.0% | 39.0% |
| **discrimination (dip - null, pp)** | +9.1 pp | +5.2 pp |
| median delta_spike_minutes | +9.3 | +7.8 |
| lower-quartile delta_spike_minutes | +4.7 | +2.6 |
| criterion a (>=60% at +10 min) | fail | fail |
| criterion b (discrim >= +15 pp) | fail | fail |
| criterion c (median >= +5, lower-q >= 0) | **PASS** | **PASS** |
| **verdict** | **REFUTED** | **REFUTED** |

## How to read this

**Both supported -> ** spike precursor predicts both crashes and dips. It's a generic 'bad day' marker, not crash-specific.

**Both refuted -> ** dips have a different physiological signature than crashes. They may be mood-only events with no autonomic precursor.

**Train supported, validate refuted -> ** same trajectory pattern as crashes themselves: signal was real in 2022-23, faded with stabilisation. Supports the 'kind of bad day changed' broader story.

**Train refuted, validate supported -> ** unlikely; flag for investigation.

## Per-dip deltas — train window

(top 20 by |delta|)

| date | leadup_max | baseline_tm | delta |
|---|---:|---:|---:|
| 2023-02-01 | 63.0 | 12.8 | +50.2 |
| 2023-08-23 | 51.0 | 13.2 | +37.8 |
| 2023-03-29 | 50.0 | 13.1 | +36.9 |
| 2023-07-08 | 48.0 | 12.2 | +35.8 |
| 2023-10-07 | 44.0 | 12.3 | +31.7 |
| 2023-11-10 | 40.0 | 11.2 | +28.8 |
| 2023-10-17 | 37.0 | 12.0 | +25.0 |
| 2023-02-22 | 30.0 | 13.2 | +16.8 |
| 2023-05-12 | 28.0 | 11.9 | +16.1 |
| 2023-10-28 | 26.0 | 11.7 | +14.3 |
| 2023-07-15 | 25.0 | 12.7 | +12.3 |
| 2022-10-21 | 27.0 | 14.8 | +12.2 |
| 2022-09-14 | 27.0 | 15.8 | +11.2 |
| 2022-12-09 | 20.0 | 10.7 | +9.3 |
| 2022-11-01 | 21.0 | 13.3 | +7.7 |
| 2023-11-03 | 19.0 | 11.5 | +7.5 |
| 2023-12-20 | 18.0 | 11.1 | +6.9 |
| 2023-08-07 | 20.0 | 13.2 | +6.8 |
| 2023-06-23 | 18.0 | 12.3 | +5.7 |
| 2023-05-22 | 17.0 | 12.0 | +5.0 |

## Per-dip deltas — validate window

(top 20 by |delta|)

| date | leadup_max | baseline_tm | delta |
|---|---:|---:|---:|
| 2024-03-30 | 88.0 | 10.4 | +77.6 |
| 2024-07-11 | 69.0 | 9.5 | +59.5 |
| 2026-02-11 | 66.0 | 9.3 | +56.7 |
| 2024-10-24 | 53.0 | 7.8 | +45.2 |
| 2024-03-14 | 48.0 | 9.6 | +38.4 |
| 2025-01-20 | 40.0 | 6.8 | +33.2 |
| 2026-02-15 | 41.0 | 9.3 | +31.7 |
| 2026-04-30 | 42.0 | 11.3 | +30.7 |
| 2025-02-09 | 37.0 | 6.5 | +30.5 |
| 2024-11-07 | 33.0 | 7.4 | +25.6 |
| 2024-02-08 | 34.0 | 9.8 | +24.2 |
| 2025-11-28 | 30.0 | 6.5 | +23.5 |
| 2024-11-22 | 31.0 | 7.6 | +23.4 |
| 2025-06-12 | 29.0 | 7.1 | +21.9 |
| 2024-01-09 | 28.0 | 10.5 | +17.5 |
| 2024-08-12 | 25.0 | 9.9 | +15.1 |
| 2024-03-19 | 24.0 | 10.0 | +14.0 |
| 2026-02-27 | 24.0 | 10.1 | +13.9 |
| 2024-03-24 | 23.0 | 10.2 | +12.8 |
| 2025-12-17 | 19.0 | 6.9 | +12.1 |

---

*Run 2026-06-06. Seed `20260605` matches H02b's null sample.*