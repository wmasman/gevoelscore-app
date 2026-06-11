# HA08c — Multi-day sleep stress mean slope (z-score) as crash precursor

**Pre-registration written 2026-06-07, before any sleep-stress
backfill data has been inspected.** Locked. Any subsequent change
creates an HA08c2.

HA08c is the **substitute test for HA08** after HA08 was
[blocked-pending-hardware](../HA08-hrv-multiday-slope/hypothesis.md)
(same hardware blocker as HA07 — FR245 does not record HRV).

HA08c tests the multi-day creep mode (Wiggers' *"HRV daalt over
meerdere dagen na overbelasten"*) through the sleep-stress HRV
proxy. Where HA07c catches single-night shifts, HA08c catches
sustained multi-day trends. This matches the A.2 trend-slope
concept from Theme A applied to the sleep-stress signal.

The same proxy caveats from HA07c apply (§8 below). HA08c's
verdict is a verdict on the proxy, not HRV directly.

## 1. Claim

In the **4 days** before a `crash_v1` episode (primary) and the
**5 days** before a `crash_v1` episode (secondary), at least one
day's trailing-5-day mean-sleep-stress slope deviates from its
lagged personal baseline by **(slope_5d − μ_slope) / σ_slope
≥ +N_std** (one-sided **elevated** = sustained upward sleep-stress
trend = sustained downward HRV proxy = Wiggers' "creep" direction).
The crash-episode frequency of this deviation is discriminative
against randomly-sampled non-crash windows in **both train and
validate windows independently**.

**Primary direction: one-sided elevated** (sleep stress rising over
days = HRV proxy declining over days = Wiggers' canonical direction
for the slow erosion mode).

## 2. Why we think this

- Direct substitute for HA08's HRV-creep hypothesis.
- Wiggers' multi-day pattern is well-documented:
  *"HRV daalt over meerdere dagen na overbelasten"*.
- The Theme A trend-slope concept (A.2) was deliberately designed
  for sustained creeps; this is its cleanest physiological
  application on the sleep-stress proxy.
- Complements HA07c (acute single-night shift). Acute and chronic
  modes can both be real or one can dominate.
- **Validate era directionality reversal expectation**: per HA10 +
  HA06b, validate one-sided elevated may refute and validate
  one-sided lowered (sustained sleep-stress decline = sustained HRV
  proxy rise = parasympathetic-dominance creep) may SUPPORT —
  another test of whether the swing pattern is sustained.

## 3. Data sources

Same as HA07c (cached sleep responses at
`...api_pull\sleep\YYYY-MM\YYYY-MM-DD.json`).

## 4. Measurement protocol

### 4.1 Per-night mean sleep stress

Same as [HA07c §4.1](../HA07c-sleep-stress-mean-delta/hypothesis.md#41-per-night-mean-sleep-stress).

### 4.2 Trailing-5-day stress slope

For each day `d` with valid prior data:
- Collect `stress_mean` values from days `[d-4, d-3, d-2, d-1, d]`.
- Require ≥ 4 of 5 days to have valid `stress_mean`.
- Compute OLS slope of stress_mean vs day-index. Units:
  stress points per day.
- Positive slope = sleep stress rising over the window.

`slope_5d[d]` = OLS slope over the trailing 5-day window
including d.

### 4.3 Lagged personal baseline of slopes

For each valid day `d` with a defined `slope_5d`:
- Baseline window: slopes computed on days in `[d-90, d-30]`.
- Trimmed mean (10/90 cut) `μ_slope`; stdev `σ_slope`.
- Computed only when ≥ 40 valid slope values are available in the
  baseline.
- If `σ_slope` ≤ 0.5 stress-points/day, flag as low-variability
  and skip. Report fraction.

### 4.4 Per-day z-scored slope

For each valid day `d`:
- `z_slope(d) = (slope_5d(d) − μ_slope(d)) / σ_slope(d)` (signed)
- `|z_slope(d)|` (unsigned)

### 4.5 Per-episode lead-up profile

Same structure as HA07c:
- 4-day primary lead-up: [C-4, C-3, C-2, C-1].
- 5-day secondary lead-up: [C-5, C-4, C-3, C-2, C-1].
- Min valid days: 3 of 4 for primary; 4 of 5 for secondary.
- **Primary trigger flag (one-sided elevated)**:
  `max z_slope ≥ +N_std`.
- Sensitivity arms: bidirectional `max |z_slope| ≥ N_std`;
  one-sided lowered `min z_slope ≤ −N_std`.

### 4.6 Threshold N_std

Same as HA07c: 1.5 / 2.0 / 2.5.

### 4.7 Null sample

Same as HA07c: 200 random non-overlapping references, seed
`20260605`.

## 5. Pre-registered falsification criterion

Identical to HA07c (60% / +15 pp / median ≥ N_std/2).

## 6. Pre-committed verdict mapping per era directionality

Same shape as HA07c §6, applied to slope direction.

## 7. Expected effect size if hypothesis is true

- Train one-sided elevated 4d primary: 60-80% trigger rate at
  +15-25 pp disc.
- Validate primary direction refuted; validate one-sided lowered
  may SUPPORT if the parasympathetic-creep pattern manifests.
- Median |z_slope|: 1.5-2.5.

## 8. Caveats `result.md` must explicitly acknowledge

All HA07c §8 caveats apply (proxy nature, sleep window
uncertainty, ToS-grey API, crash_v1 mixes mechanisms,
multi-comparison). Additional:

- **OLS slope sensitive to single outliers**. A single anomalous
  night can swing the slope of a 5-day window. Robust regression
  (Theil-Sen) is a defensible alternative but is NOT pre-registered
  as primary; OLS is locked.
- **5-day slope window**. Other window lengths (7d, 10d) are
  defensible; 5d locked for consistency with the 4-5d empirical
  PEM lag confirmed across four channels.

## 9. What we do with each outcome

- **HA07c + HA08c both SUPPORTED** → acute + sustained autonomic
  patterns both present; HRV-proxy channel is real on multiple
  time-scales. Strongest possible substitute test result.
- **HA07c supported, HA08c refuted** → acute single-night shift
  dominates; sustained creep not a separate signal.
- **HA07c refuted, HA08c supported** → slow creep dominates;
  single-night shocks too noisy on the proxy.
- **Both refuted** → HRV-proxy channel null. Direction shifts to
  H03b (BB sharpening) as the only remaining path C value.

---

*Pre-registration locked 2026-06-07 before any sleep-stress data
inspection. Same test-script pattern as HA10 / HA11 with slope
loading. Same `--dry-run` mode; same null seed (`20260605`); same
lagged baseline machinery.*
