# HA-C4b dry-run report (sanity-gate failure)

Drafted by `test.py --dry-run` per locked hypothesis.md §10.4 protocol. Sanity gates failed; full test NOT run; result.md NOT emitted.

Quartile cache used: no (1b.i only — 1b.ii deferred)

## Sanity failures (§7)

- consolidation train n=0 < 10 (§7 / §5.3)
- consolidation validate n=5 < 10 (§7 / §5.3)
- unmedicated median primary = 78.0 outside [15, 60] (§7)

## Eligible-crash-episodes per phase x era

| phase | train | validate |
|---|---:|---:|
| unmedicated | 8 | 2 |
| buildup | 0 | 2 |
| consolidation | 0 | 5 |
| afbouw | 0 | 2 |

## Median primary predictor + median baseline sigma per phase

| phase | median predictor | median baseline sigma |
|---|---:|---:|
| unmedicated | 78.0 | 33.4 |
| buildup | 36.0 | NA |
| consolidation | 39.0 | 23.8 |
| afbouw | 64.0 | 30.7 |

## Next step

Per the locked-pre-reg discipline (hypothesis.md §10.4 + §9), the spec must be revised before any further test run; the revision creates HA-C4b-v2 with the v1 archived. The next session opens a v2-draft pre-reg session under [CONVENTIONS §1.2 reviewer-mode-with-authorization].
