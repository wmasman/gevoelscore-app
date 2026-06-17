# HA-C4b v3 dry-run report - sanity gates PASS

Drafted by `test.py --dry-run` per locked v3 hypothesis.md §10.4 protocol. v3 headline cell: unmedicated × train+validate POOLED × `S60_Mlow` × N_std=1.5 × primary 4d × one-sided elevated. v3 day-validity gates: gate 1 (HA11 valid ≥600) + gate 1b.i (≥900 in-range) + §4.2 exertion + §6. **v3 drops §4.3 1b.ii** (wake-window quartile-coverage) and **symmetrises the dry-run / full-run gate** so the n that passes here IS the n the full run evaluates.

## Eligible-crash-episodes per phase × era

| phase | train | validate | pooled |
|---|---:|---:|---:|
| unmedicated | 8 | 2 | 10 |
| buildup | 0 | 2 | 2 |
| consolidation | 0 | 5 | 5 |
| afbouw | 0 | 2 | 2 |

## Pooled-unmedicated n (v3 headline cell)

- Pre-§4.5: n = 10 (eligible-crash count after §4.2/§4.3/§6)
- Post-§4.5 baseline-availability: n_clean = 10 (v3 §10.2 gate: n ≥ 10 — PASS)

## v3 §7 raw per-phase median PRIMARY_COL (no §4.3 filter)

| phase | raw median | v3 §7 card | tol ±20% range | gate |
|---|---:|---:|---|---|
| unmedicated | 76.0 | 76.0 | [60.8, 91.2] | PASS |
| buildup | 36.0 | 35.0 | [28.0, 42.0] | PASS |
| consolidation | 38.0 | 38.0 | [30.4, 45.6] | PASS |
| afbouw | 63.0 | 63.0 | [50.4, 75.6] | PASS |

## Median lagged-baseline σ per phase (§4.3-eligible sample)

| phase | median σ | v3 §7 range (unmedicated [25, 55]) |
|---|---:|---|
| unmedicated | 33.4 | PASS |
| buildup | NA | (unmedicated only) |
| consolidation | 23.8 | (unmedicated only) |
| afbouw | 30.7 | (unmedicated only) |

## Next step (PASS branch)

Sanity gates passed; the full test runs immediately after the dry-run inside the same `python test.py` invocation, emitting `result.md` + `result-data.json`. **v3 §10.2 gate symmetry guarantees the n that passed here is the n the full run evaluates** (no further §4.3 exclusion between regimes).
