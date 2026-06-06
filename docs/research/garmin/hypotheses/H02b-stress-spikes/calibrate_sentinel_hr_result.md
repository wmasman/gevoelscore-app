# H02d sentinel-vs-HR calibration

Stratified sample of 8 monitoring_b files across the analysis window.

## Files sampled

| date | stress samples | HR samples | sentinel count |
|---|---:|---:|---:|
| 2021-08-16 | 0 | 0 | 0 |
| 2021-11-17 | 5 | 4 | 5 |
| 2022-04-04 | 285 | 190 | 9 |
| 2022-11-02 | 477 | 411 | 76 |
| 2023-06-07 | 762 | 523 | 26 |
| 2024-01-23 | 333 | 216 | 11 |
| 2024-08-10 | 238 | 208 | 43 |
| 2025-04-18 | 238 | 206 | 50 |

Totals: 2338 stress samples, 2118 valid (1-100), 220 sentinel, 1758 unique HR timestamps.

## Sentinel value distribution

| value | count |
|---:|---:|
| -2 | 187 |
| -1 | 33 |

## HR sample cadence (seconds between consecutive HR samples)

- median: 60s
- p90: 120s
- p99: 300s
- max: 21700680s

## Gap from each sentinel-stress sample to nearest HR sample

- N sentinel samples: 220
- N with no HR in this file: 0
- median gap (finite): 0s
- p90 gap (finite): 0s

## Fraction of sentinels with HR within tolerance window

| tolerance (s) | sentinels covered | % of sentinels | valid-stress covered | % of valid |
|---:|---:|---:|---:|---:|
| 30 | 204 | 92.7% | 1547 | 73.0% |
| 60 | 220 | 100.0% | 2038 | 96.2% |
| 90 | 220 | 100.0% | 2038 | 96.2% |
| 180 | 220 | 100.0% | 2117 | 100.0% |
| 300 | 220 | 100.0% | 2118 | 100.0% |

## Reading

If sentinel-coverage % at small tolerances (30-90s) is high, the 'HR-present means too_active' rule is clean. If coverage drops sharply between sentinels and valid samples, the sentinels are systematically clustered in HR-gaps (off-wrist).