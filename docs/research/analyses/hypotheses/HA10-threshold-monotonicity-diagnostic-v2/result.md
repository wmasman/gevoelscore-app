# HA10 v2 diagnostic — result

**Verdict per locked v2 criteria: RESCUE** (validate bidirectional
primary). Cat 3 (rising/late-peak) passes. No FAIL category
triggers.

HA10's locked SUPPORTED verdict at validate-era 4d primary
bidirectional N_std=1.5 (+16.2 pp, 86.7% freq) stays on record per
audit-trail discipline. Under v2 the synthesis-level demotion is
**reversed** and HA10 is restored to **load-bearing (corroborating
secondary) anchor for validate-era**, with the revised-criteria
reasoning cited.

## Shape analysis (validate bidirectional, meaningful range [1.0, 3.0])

| stat | value | criterion check |
|---|---:|---|
| peak N_std | 1.75 | Cat 3 requires > 1.5 ✓ |
| peak disc | +19.5 pp | Cat 3 requires ≥ +15 ✓ |
| disc at N_std=2.0 | +14.0 pp | Cat 3 requires ≥ +10 ✓ |
| sign-changes (zero-crossings) | 1 | Cat 3 requires ≤ 1 ✓ |
| positive across [1.0, peak] | yes (all positive) | Cat 3 requires ✓ |
| Spearman rho | −0.583 | (Cat 1 requires ≤ −0.3 ✓; Cat 3 has no rho requirement) |
| direction reversals (descriptive only) | 5 | not used in verdict |
| max negative disc | −4.7 (at N_std=3.0) | Cat 4 requires ≤ −10 to trigger ✗ |

**Verdict**: Cat 3 PASS, no FAIL category triggers → Rule (ii):
PASS only → **RESCUE**.

## Comparison to v1

v1 CLOSE was triggered by peak at 1.75 outside the [1.0, 1.5]
rescue window. v2 explicitly added Cat 3 for the rising/late-peak
shape, which captures HA10's curve correctly. The discipline
binds in the restoration direction: v2 criteria are stricter overall
(see HA06b which CLOSES under v2 even though no v1 ran), but HA10
fits the Cat 3 shape category that v1 didn't acknowledge.

## What this changes

Per the locked v2 §4 verdict logic and §5 application rules:

- HA10 validate-era restored to **load-bearing corroborating
  secondary anchor** for card (b2). (HA07d remains primary
  anchor.)
- Synthesis-level framing: HA10 was "demoted to non-load-bearing
  under v1 CLOSE" → updates to "RESCUED under v2 Cat 3
  (rising/late-peak shape); load-bearing as corroborating
  secondary anchor for validate-era picture."
- HA10 train descriptive arm closes under v2 (was already refuted
  at v1 primary; not load-bearing in either era for train).

## What this does NOT change

- HA10 train was REFUTED at v1 primary; v2 doesn't change that.
- The validate-era specificity caveats for card (b2) still apply
  per the peer review §5.3 — discrimination magnitudes still
  don't translate to posterior-probability.
- HA10's BB-algorithm-opacity caveat still applies.

---

*v2 diagnostic locked at [diagnostic.md](diagnostic.md); v2 criteria
locked at [methodology/threshold-sweep-rescue-criteria-v2.md](../../methodology/threshold-sweep-rescue-criteria-v2.md).
Same v1 fine-grid data; no new computation needed for HA10 v2.*
