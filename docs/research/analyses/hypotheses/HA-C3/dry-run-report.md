# HA-C3 v2 r2 dry-run report - section 7.3 halt-option-A triggered (PRE-COMMITTED absorb; proceeding)

Emitted by `test.py --dry-run` per locked v2 r2 hypothesis.md section 10.4. Headline cell: unmedicated x 4-bin x `gevoelscore` x 3-condition gated outcome x block-permutation null at E[L]=7. Day-validity per section 4.3 (LC era + unmedicated + not April-2024 cluster + not first 21 device-baseline days + non-NaN both columns).

- Pool n = 581
- Stress median = 34.00
- Gevoelscore median = 4.00

## Per-bin sample sizes (`all_day_stress_avg`, v2 4-bin scheme)

| bin | label | n | mean gevoelscore | median gevoelscore |
|---|---|---:|---:|---:|
| B1 | B1[0,30) | 95 | 3.958 | 4.00 |
| B2 | B2[30,40) | 385 | 4.265 | 4.00 |
| B3 | B3[40,60) | 100 | 3.860 | 4.00 |
| B4 | B4[60,100] | 1 | 1.000 | 1.00 |

## Gate results

| gate | description | result |
|---|---|---|
| 1 | per-bin n >= 30 (4 bins) | FAIL |
| 2 | stress median in [20.0, 60.0] | PASS |
| 3 | gevoelscore median in [3.0, 6.0] | PASS |
| 4 | >= 2 bins n>=30 AND total n>=100 | PASS |

## section 7.3 halt-option-A APPLIED (PRE-COMMITTED absorb)

Per v2 r2 LOCKED spec section 7.3 + section 4.1: B4 [60,100] underpower (n < 30) triggers automatic absorption into B3 [40,60), producing the 3-bin reduction `{B1 [0,30), B2 [30,40), B3' [40,100]}`. The test runs on the 3-bin reduction with the contrast reduced to a single second-difference `S = m_3 - 2*m_2 + m_1` and the spline reduced to 2 internal knots at (30, 40); visual-gating count reduces to >= 1 of 2 segment midpoints from {35, 70}. This is NOT a halt; the LOCKED spec PRE-COMMITS to this absorption as the default for B4 underpower.

**3-bin reduction descriptives (post-absorption)**:

| bin | label | n | mean gevoelscore | median gevoelscore |
|---|---|---:|---:|---:|
| B1 | B1[0,30) | 95 | 3.958 | 4.00 |
| B2 | B2[30,40) | 385 | 4.265 | 4.00 |
| B3 | B3'[40,100] | 101 | 3.832 | 4.00 |

**Dry-run verdict: PASS (after section 7.3 absorption)** -- proceeding with full run on the 3-bin reduction.

