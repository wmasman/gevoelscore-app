# HA-C4b v2 dry-run report — sanity gates PASS

Drafted by `test.py --dry-run` per locked v2 hypothesis.md §10.4 protocol. v2 headline cell: unmedicated × train+validate POOLED × `S60_Mlow` × N_std=1.5 × primary 4d × one-sided elevated.

Quartile cache (§4.3 1b.ii): deferred (1b.i only — full run will build cache + reapply)

## Eligible-crash-episodes per phase × era

| phase | train | validate | pooled |
|---|---:|---:|---:|
| unmedicated | 8 | 2 | 10 |
| buildup | 0 | 2 | 2 |
| consolidation | 0 | 5 | 5 |
| afbouw | 0 | 2 | 2 |

## Pooled-unmedicated n (v2 headline cell)

- Pre-§4.5: n = 10 (eligible-crash count after §4.2/§4.3/§6)
- Post-§4.5 baseline-availability: n_clean = 10 (v2 §10.2 gate: n ≥ 10 — PASS)

## v2 §7 raw per-phase median PRIMARY_COL (no §4.3 filter)

| phase | raw median | v2 §7 card | tol ±20% range | gate |
|---|---:|---:|---|---|
| unmedicated | 76.0 | 76.0 | [60.8, 91.2] | PASS |
| buildup | 36.0 | 35.0 | [28.0, 42.0] | PASS |
| consolidation | 38.0 | 38.0 | [30.4, 45.6] | PASS |
| afbouw | 63.0 | 63.0 | [50.4, 75.6] | PASS |

## Median lagged-baseline σ per phase (§4.3-eligible sample)

| phase | median σ | v2 §7 range (unmedicated [25, 55]) |
|---|---:|---|
| unmedicated | 33.4 | PASS |
| buildup | NA | (unmedicated only) |
| consolidation | 23.8 | (unmedicated only) |
| afbouw | 30.7 | (unmedicated only) |

## Next step (PASS branch)

Sanity gates passed; the full test runs immediately after the dry-run inside the same `python test.py` invocation, emitting `result.md` + `result-data.json`.

## Post-full-run observation (added after the full run landed) — §10.2 gate / §4.3 1b.ii asymmetry

The §10.2 spec-sanity-gate at dry-run was evaluated with §4.3 1b.i only (the dry-run defaults to skipping 1b.ii because the quartile-coverage cache takes 5-15 min to build from FIT files). Under 1b.i only, pooled-unmedicated n = 10 (8 train + 2 validate) — PASS at the §5.3 bar.

The full run then built the quartile-coverage cache and applied §4.3 1b.ii. **Under 1b.ii, the pooled-unmedicated cell drops to n = 9 (7 train + 2 validate)** — below the §5.3 bar. The dropped train episode is `2023-02-04`, whose 4-day lead-up included a `max_signed_z = +3.73` peak (the unmedicated train arm's highest signal episode by the dry-run printout).

The headline verdict at the full run is therefore INCONCLUSIVE per v2 §5.3. See [`result.md`](result.md) for the descriptive-companion report; no SUPPORTED claim is made.

**Spec-design observation for the v2 → v3 audit trail**: the §10.2 dry-run sanity gate and the full-run gate are asymmetric (1b.i-only vs full §4.3). A spec-design revision (v3 candidate) would either symmetrise the dry-run gate (apply 1b.ii at dry-run; slow but accurate) or reconsider whether 1b.ii is required for the LC-era unmedicated headline. **No retroactive v3 is auto-triggered.** Documented here for the user's review.
