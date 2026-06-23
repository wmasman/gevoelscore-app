# HA-C3p r2 dry-run report - sanity gates PASS

Emitted by `test.py --dry-run` per LOCKED r2 hypothesis.md section 10.4. **Headline cell**: unmedicated x 5-quintile-bin x `gevoelscore` x 3-condition gated outcome x block-permutation null at E[L]=7. Day-validity per section 4.3 (LC era + unmedicated + not April-2024 cluster + not first 21 device-baseline days + non-NaN both columns).

- Unmedicated pool n = 581
- Stress median = 34.00
- Gevoelscore median = 4.00

## Per-bin sample sizes (unmedicated, `all_day_stress_avg` quintile bins)

| bin | label | n | mean gevoelscore | median gevoelscore |
|---|---|---:|---:|---:|
| Q1 | Q1[0,28) | 45 | 3.822 | 4.00 |
| Q2 | Q2[28,31) | 80 | 4.138 | 4.00 |
| Q3 | Q3[31,34) | 129 | 4.271 | 4.00 |
| Q4 | Q4[34,37) | 138 | 4.290 | 4.00 |
| Q5 | Q5[37,100] | 189 | 4.016 | 4.00 |

## Gate results

| gate | description | result |
|---|---|---|
| 1 | per-bin n >= 30 (x5 bins) | PASS |
| 2 | stress median in [20.0, 60.0] | PASS |
| 3 | gevoelscore median in [3.0, 6.0] | PASS |
| 4 | all 5 bins n>=30 AND total n>=100 | PASS |
| 5 (SHA) | snapshot SHA-256 matches `d0ff9253` | PASS |
| 5 (boundaries) | quintile boundary shift <= 1 stress-unit | PASS |

**Gate 5 recomputed boundaries** (q=0.2,0.4,0.6,0.8 on the full Stratum 4 pool): [28.0, 31.0, 34.0, 37.0]; locked = [28.0, 31.0, 34.0, 37.0].

**DRY-RUN VERDICT: PASS** - proceed with full run.

