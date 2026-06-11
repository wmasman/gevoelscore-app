# HA07d — Night-over-night sleep stress variability delta (z-score) as crash precursor

**Pre-registration written 2026-06-07, before any sleep-stress
backfill data has been inspected.** Locked. Any subsequent change
creates an HA07d2.

HA07d is a **complementary primitive** to HA07c — same proxy
chain (sleep stress as HRV proxy) but measuring **variability**
rather than mean. Where HA07c asks "does the per-night autonomic
state mean shift before crashes?", HA07d asks "does the per-night
autonomic state become more or less oscillatory before crashes?"

The proxy caveats from HA07c apply equally (§8). HA07d's primitive
is the **per-night standard deviation** of in-sleep-window stress
values. A higher stdev means the autonomic state was more
oscillatory during sleep (alternating between vagal and sympathetic
moments); a lower stdev means more stable autonomic regulation.

## The HRV-of-HRV question

Classical HRV is itself a measure of beat-to-beat variability.
HA07d is therefore "variability of (HRV-proxy)" — a second-order
measure. This is **physiologically motivated**:
- High sympathetic tone + low vagal tone → flat low HRV → flat
  HIGH sleep stress → LOW variability
- Healthy autonomic flexibility → oscillating HRV through sleep
  stages → oscillating sleep stress → HIGHER variability
- Autonomic dysregulation often shows up as MIXED moments —
  vagal recovery interrupted by sympathetic spikes → ELEVATED
  variability

The expected direction is **ambiguous a priori**, which is why
HA07d is bidirectional primary (NOT one-sided like HA07c). Either
direction shift could be precursor-relevant.

## 1. Claim

In the **4 days** before a `crash_v1` episode (primary) and the
**5 days** before a `crash_v1` episode (secondary), at least one
night-over-night delta of in-sleep-window stress stdev deviates
from its lagged personal baseline by **|stress_stdev[d] −
stress_stdev[d-1] − μ_delta| / σ_delta ≥ N_std** (bidirectional).
The crash-episode frequency of this deviation is discriminative
against randomly-sampled non-crash windows in **both train and
validate windows independently**.

**Primary direction: bidirectional** (the physiological direction
is ambiguous; either an unusually oscillatory or unusually flat
night may precede crashes). One-sided arms reported as
sensitivity.

## 2. Why we think this

- Tests the **HRV-of-HRV** dimension that HA07c (mean) does not
  catch. A night where mean sleep stress is normal but variability
  has shifted is a legitimate autonomic anomaly worth detecting.
- Complementary primitive to HA07c — costs ~zero extra given the
  HA07c extraction is in place.
- **Autonomic dysregulation often manifests as variability shifts
  before mean shifts** (this is the basis for HRV analysis in
  general).
- Mean and stdev are independent in principle; a finding on stdev
  not paralleled in mean is interpretable as "the autonomic state's
  *flexibility* shifted before the crash, not its baseline level."

## 3. Data sources

Same as HA07c (cached sleep responses).

## 4. Measurement protocol

### 4.1 Per-night sleep stress stdev

For each calendar day `d`:
1. Same loading + sleep window filter as
   [HA07c §4.1](../HA07c-sleep-stress-mean-delta/hypothesis.md#41-per-night-mean-sleep-stress).
2. Require ≥ 120 valid entries (same threshold as HA07c).
3. `stress_stdev[d]` = sample standard deviation of valid
   in-window stress values.

### 4.2 Night-over-night delta

For each pair `(d-1, d)` where both stdevs are defined:
- `delta_dod(d) = stress_stdev(d) − stress_stdev(d-1)` (signed)

### 4.3 Lagged personal baseline of deltas

Same construction as HA07c §4.3, with `σ_delta` low-variability
floor at **0.5 stress-points** (lower than HA07c's 2.0 floor
because the stdev's own variability is structurally smaller).

### 4.4 Per-day z-scored delta

For each valid day `d`:
- `z_delta(d) = (delta_dod(d) − μ_delta(d)) / σ_delta(d)` (signed)
- `|z_delta(d)|` (unsigned)

### 4.5 Per-episode lead-up profile

Same structure as HA07c with **primary trigger flag
(bidirectional)**:
- `max |z_delta| ≥ N_std`.
- Sensitivity arms: one-sided elevated (variability rose) and
  one-sided lowered (variability fell).
- Record directionality split.

### 4.6 Threshold N_std

Same as HA07c / HA08c: 1.5 / 2.0 / 2.5.

### 4.7 Null sample

Same as HA07c.

## 5. Pre-registered falsification criterion

Identical to HA07c / HA08c (60% / +15 pp / median ≥ N_std/2).

## 6. Pre-committed verdict mapping

| era / direction | predicted from prior tests | locked criterion |
|---|---|---|
| train bidirectional | no strong prior; consider SUPPORTED if either tail catches signal | strict bar |
| train one-sided elevated | speculative; report only | sensitivity arm |
| train one-sided lowered | speculative; report only | sensitivity arm |
| validate bidirectional | no strong prior | strict bar |
| validate one-sided elevated | speculative; report only | sensitivity arm |
| validate one-sided lowered | speculative; report only | sensitivity arm |

HA07d is the **most exploratory** of the three substitute tests.
The bidirectional primary respects the a priori uncertainty about
which direction the dysregulation manifests in.

## 7. Expected effect size if hypothesis is true

- Train OR validate bidirectional 4d primary: 60-80% trigger rate
  at +15-25 pp disc.
- Median |z_delta|: 1.5-2.5.
- Honest expectation: **modest signal at best**; the second-order
  primitive (stdev-of-derived-metric) is less direct than the
  first-order (mean) primitive HA07c tests.

## 8. Caveats `result.md` must explicitly acknowledge

All HA07c §8 caveats apply (proxy nature, sleep window
uncertainty, ToS-grey API, crash_v1 mixes mechanisms,
multi-comparison). Additional:

- **HA07d is a second-order primitive**. Variability of an already-
  derived metric (stress, itself derived from HRV+HR) is two steps
  removed from raw autonomic state. Effect sizes are correspondingly
  attenuated.
- **Sleep architecture confound**. Stress fluctuates with sleep
  stages (REM vs deep vs light). Higher sleep stress variability
  may reflect more sleep-stage transitions, not autonomic
  dysregulation. The lagged baseline z-score partially controls
  for this (transition rates are personal-stable).
- **Refutation is the expected outcome** if the channel doesn't
  carry signal at this second-order resolution. A REFUTED HA07d
  alongside SUPPORTED HA07c would say "the autonomic state shifts
  in mean before crashes, but not in variability." This is itself
  interpretable.
- **Multi-comparison**. HA07d is the 19th pre-registered hypothesis
  in the H##/HA## series.

## 9. What we do with each outcome

- **Supported in both windows** → HRV-of-HRV pattern is a third
  layer of the autonomic-deviation precursor signature. Novel
  finding worth banking; would invite follow-up tests on other
  channels' variability (RHR variability, BB variability).
- **One era SUPPORTED, other refuted** → era-specific variability
  pattern. Interpretable in the era-reversal framework.
- **Both refuted** → the variability dimension is not
  precursor-discriminative for this participant. The mean (HA07c)
  remains the relevant primitive.
- **Spec sanity-check fails on dry-run** (median σ_delta outside
  reasonable range, or stress_stdev distribution pathological)
  → flag explicitly. Pre-registration discipline holds.

---

*Pre-registration locked 2026-06-07 before any sleep-stress data
inspection. Same test-script pattern as HA07c with stdev loading
replacing mean loading. Same `--dry-run` mode; same null seed
(`20260605`); same lagged baseline machinery.*
