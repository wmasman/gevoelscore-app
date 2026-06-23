# HA-C3 r2 dry-run report - SANITY GATE FAILURE (HALT)

Emitted by `test.py --dry-run` per locked r2 hypothesis.md §10.4. Headline cell: unmedicated × 5-bin × `gevoelscore` × 3-condition gated outcome × block-permutation null at E[L]=7. Day-validity per §4.3 (LC era + unmedicated + not April-2024 cluster + not first 21 device-baseline days + non-NaN both columns).

- Pool n = 581
- Stress median = 34.00
- Gevoelscore median = 4.00

## Per-bin sample sizes (`all_day_stress_avg`)

| bin | label | n | mean gevoelscore | median gevoelscore |
|---|---|---:|---:|---:|
| B1 | B1[0,20) | 0 | NA | NA |
| B2 | B2[20,30) | 95 | 3.958 | 4.00 |
| B3 | B3[30,40) | 385 | 4.265 | 4.00 |
| B4 | B4[40,60) | 100 | 3.860 | 4.00 |
| B5 | B5[60,100] | 1 | 1.000 | 1.00 |

## Gate results

| gate | description | result |
|---|---|---|
| 1 | per-bin n >= 30 (×5 bins) | FAIL |
| 2 | stress median in [20.0, 60.0] | PASS |
| 3 | gevoelscore median in [3.0, 6.0] | PASS |
| 4 | >= 3 bins n>=30 AND total n>=100 | PASS |

## HALT-eligible failures

- **Gate 1** (per-bin n >= 30): bins below threshold: [('B1', 0), ('B5', 1)]; spec 7.3 halt-option-A pre-committed only for sole-B5 failure; other failures require v2 spec redraft.

Per locked r2 §10.4 step 1 + `hypothesis_lock_process.md` §3.9: the full test is **HALTed** if the failure is not absorbed by the pre-committed §7.3 halt-option-A. Failures other than sole-B5 underpower require a v2 spec redraft.

