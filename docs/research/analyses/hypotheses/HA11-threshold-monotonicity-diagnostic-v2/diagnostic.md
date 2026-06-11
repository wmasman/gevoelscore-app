# HA11 threshold-monotonicity diagnostic v2

**Pre-registration locked 2026-06-07** per the user-locked Option C
tightened. HA11 had **no v1 diagnostic**; v2 is the first
threshold-monotonicity diagnostic applied to HA11. Locked
symmetrically with HA10, HA07d, HA06b v2 diagnostics.

**Criteria source**: [v2 methodology document](../../methodology/threshold-sweep-rescue-criteria-v2.md).

## 1. What this diagnostic evaluates

**Test under diagnostic**: HA11 (within-day U-dip event count
z-score; locked train SUPPORTED at primary 4d **one-sided
elevated** N_std=1.5 +22.8 pp; validate refuted inverse-direction).

**Important note**: HA11's locked primary direction is one-sided
elevated, NOT bidirectional. The v2 methodology was written for
bidirectional primaries. For HA11, the v2 diagnostic is applied
to **HA11's actual locked primary direction (one-sided elevated)**,
not artificially imposed as bidirectional.

This is a pre-committed accommodation to the v2 criteria, not an
escape hatch: HA11's primary was always one-sided elevated, so
v2 evaluates the same arm that v1 would have. The five-category
shape rule applies identically to one-sided arms as to
bidirectional arms.

## 2. Data sources and machinery

Same as HA11 test: per-day U-dip counts from
[udip_counts.csv](HA11-stress-udip/udip_counts.csv) (1722 valid
days); lagged baseline [d-90, d-30]; 4d primary; null sample seed
`20260605`.

Fine N_std grid: [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5,
2.75, 3.0, 3.5, 4.0].

Requires running HA11's test machinery on the fine grid.

## 3. v2 verdict logic

Apply [v2 methodology §3](../../methodology/threshold-sweep-rescue-criteria-v2.md#3-the-five-category-shape-rule)
to HA11's TRAIN ONE-SIDED ELEVATED primary curve.

Validate one-sided elevated curve also computed; validate v1
verdict was REFUTED (inverse direction, −10.7 pp); v2 cannot
RESCUE a refuted test for SUPPORTED status, only confirm/deny
the shape robustness of the refutation. The "inverse-direction"
finding in validate is itself a signature pattern; v2 informs
whether it's threshold-robust.

## 4. Test-specific notes

- HA11's one-sided elevated direction is **physiologically
  motivated by Wiggers' specific orthostatic pattern prediction**;
  the locked one-sided primary is the right direction for the
  hypothesis.
- HA11's U-dip detector has **parameter degrees of freedom**
  (S_pre ≥ 40, drop ≥ 25, plateau ≥ +5, refractory 60 min) that
  the peer-review §3 flagged as "not externally anchored." The v2
  diagnostic does NOT address this concern — parameter sensitivity
  is a separate diagnostic (queued Tier 2). The v2 diagnostic only
  addresses threshold robustness given the locked U-dip parameters.

## 5. Pre-registered restoration / demotion actions

### If train RESCUE under v2

- HA11 train confirms as load-bearing finding for the pre-cliff
  autonomic-deviation precursor signature on a within-day pattern
  channel.
- Six-channel train convergence narrative stays with HA11 intact.
- Card (b) train-era retrospective keeps HA11 as one of its
  anchors.

### If train CLOSE under v2

- HA11 train SUPPORTED verdict stays on record but synthesis-level
  framing demotes to non-load-bearing.
- Within-day U-dip channel removed from load-bearing list.
- Worth noting in result.md: HA11's one-sided primary may exhibit
  a different shape pattern than bidirectional tests; the v2
  five-category rule still applies but may flag a category-3
  (rising-late-peak) pattern as RESCUE on a one-sided arm that
  is genuinely robust.

### If validate one-sided elevated v1 was inverse → v2 shape

- Reported descriptively. The inverse-direction signature itself
  is a finding; v2 doesn't change that finding's status.

## 6. Outputs

- `result-data.json` — fine-grid discrimination table per era +
  direction; shape category match; train v2 verdict on one-sided
  elevated primary.
- `result.md` — verdict statement, synthesis-framing
  implications.

Result.md produced after ALL FOUR v2 diagnostics run.

---

*Locked 2026-06-07. First v2 diagnostic on HA11. Symmetric
application with HA10 / HA07d / HA06b v2 diagnostics enforced.
v2 evaluation on HA11's actual locked primary direction
(one-sided elevated) — not artificially bidirectional.*
