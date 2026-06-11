# HA07c — Night-over-night sleep stress mean delta (z-score) as crash precursor

**Pre-registration written 2026-06-07, before any sleep-stress
backfill data has been inspected.** Locked. Any subsequent change
creates an HA07c2.

HA07c is the **substitute test for HA07** after HA07 was
[blocked-pending-hardware](../HA07-hrv-day-over-day/hypothesis.md)
(Forerunner 245 does not record nightly HRV; this is a hardware
limitation, not an API issue). HA07c tests the same physiological
question — autonomic state shift before crashes — through a
defensible HRV proxy: **mean Garmin stress during the sleep
window**.

## The proxy argument

Garmin's `stress` is computed as `f(HRV, HR, activity)`. During
sleep, activity ≈ 0, so `sleep_stress ≈ f(HRV, HR)`. Higher mean
sleep stress corresponds to lower HRV (sympathetic dominance) and
vice versa. The relationship is non-linear and bounded [1, 100],
but it is the algorithm's *interpretation* of HRV during the
period we care about. **Workwell and Wiggers reference Garmin's
stress signal in their pacing recommendations as an HRV-class
indicator** — practitioners in the field treat it as a proxy.

HA07c's verdict must be interpreted as a verdict on **the
proxy's discriminative value**, not on HRV directly. See §8 for
the explicit caveats `result.md` must carry.

## 1. Claim

In the **4 days** before a `crash_v1` episode (primary) and the
**5 days** before a `crash_v1` episode (secondary), at least one
night-over-night delta of mean sleep stress deviates from its
lagged personal baseline by **(stress_mean[d] − stress_mean[d-1]
− μ_delta) / σ_delta ≥ N_std** (one-sided **elevated** = stress
rises night-over-night, the autonomic-deviation direction the HRV
hypothesis predicted as `HRV drops`). The crash-episode frequency
of this deviation is discriminative against randomly-sampled
non-crash windows in **both train and validate windows
independently**.

**Primary direction: one-sided elevated** (sleep stress rises = HRV
proxy drops = canonical Wiggers / Workwell autonomic-deviation
direction). One-sided lowered + bidirectional reported as
sensitivity arms — per HA06b + HA10 era reversal pattern, validate
may show the opposite direction.

## 2. Why we think this

- **Direct substitute for HA07's HRV-drop hypothesis** via a
  defensible proxy.
- **Four train-era SUPPORTED autonomic precursors on four channels**
  (H02b stress spike, H02d bridge × 5d, HA06b RHR, HA11 U-dip).
  If HA07c train SUPPORTED, the **fifth** train-era channel
  confirms — this would be the strongest test of cross-channel
  multi-method convergence.
- **HA10 validate-era SUPPORTED at +16.2 pp on the paradoxical
  swing direction** (elevated BB peak). If HA07c validate also
  shows the paradoxical direction (lowered sleep stress mean), the
  validate-era parasympathetic-swing signature becomes
  **three-channel-confirmed** (HA06b RHR low + HA10 BB high + HA07c
  sleep stress low).
- **Sleep window is when autonomic state is least confounded by
  activity**. The H02 (daily-avg stress) refutation was partly
  because activity masked the autonomic signal during waking
  hours. Restricting to the sleep window removes that confound.

## 3. Data sources

- **Crash labels**: `crash_v1` from
  [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv).
- **Per-night sleep stress array**: Garmin Connect REST API
  endpoint `get_sleep_data(date)` → `sleepStress` field. Backfilled
  via [api_path_c/backfill_sleep.py](../../scripts/api_path_c/backfill_sleep.py)
  for the analysis window. Cached locally at
  `C:\Users\Gebruiker\Documents\gevoelscore-data\garmin
  data\api_pull\sleep\YYYY-MM\YYYY-MM-DD.json`.
- **Sleep window timestamps**: from `dailySleepDTO` in the same
  response (`sleepStartTimestampGMT`, `sleepEndTimestampGMT`).
- **Analysis window + train/validate split**: same as HA06b / HA10
  / HA11.

## 4. Measurement protocol

### 4.1 Per-night mean sleep stress

For each calendar day `d`:
1. Load the cached sleep response.
2. Identify the sleep window
   `[sleepStartTimestampGMT, sleepEndTimestampGMT]`.
3. Filter `sleepStress` array entries to those with
   `startGMT` in the sleep window AND `value` in [1, 100].
4. **Validity**: at least **120 valid entries** within the sleep
   window (covers ~6 hours at per-3-min cadence; matches HA10
   morning-peak validity floor).
5. `stress_mean[d]` = arithmetic mean of valid in-window values.

Days with no cache file, empty cache file, or insufficient samples
are flagged *insufficient-coverage* and skipped. Report fraction.

### 4.2 Night-over-night delta

For each pair of consecutive valid days `(d-1, d)`:
- `delta_dod(d) = stress_mean(d) − stress_mean(d-1)` (signed)
- If either is invalid, no delta is computed.

### 4.3 Lagged personal baseline of deltas (per Theme A)

For each day `d` with a defined delta_dod(d):
- Baseline window: deltas computed on days in `[d-90, d-30]`.
- Trimmed mean (10/90 cut) `μ_delta`; stdev `σ_delta`.
- Computed only when ≥ 40 valid delta pairs are available.
- If `σ_delta` ≤ 2.0 stress points, flag as low-variability and
  skip. Report fraction.

### 4.4 Per-day z-scored delta

For each valid day `d`:
- `z_delta(d) = (delta_dod(d) − μ_delta(d)) / σ_delta(d)` (signed)
- `|z_delta(d)|` (unsigned)

### 4.5 Per-episode lead-up profile

Same structure as HA10 / HA11:
- 4-day primary lead-up: [C-4, C-3, C-2, C-1].
- 5-day secondary lead-up: [C-5, C-4, C-3, C-2, C-1].
- Min valid days: 3 of 4 for primary; 4 of 5 for secondary.
- **Primary trigger flag (one-sided elevated)**:
  `max z_delta ≥ N_std`.
- Sensitivity arms: bidirectional `max |z_delta| ≥ N_std`;
  one-sided lowered `min z_delta ≤ −N_std`.
- Record directionality split.

### 4.6 Threshold N_std

| Tier | N_std |
|---|---:|
| Primary | **1.5** |
| Secondary | **2.0** |
| Sensitivity check | **2.5** |

### 4.7 Null sample

200 random non-overlapping reference dates, seed `20260605`.

## 5. Pre-registered falsification criterion

Identical to HA06b / HA10 / HA11:

**(a) Frequency**: ≥ **60%** of crash episodes trigger.
**(b) Discrimination**: ≥ **+15 pp** above null.
**(c) Magnitude**: median trigger magnitude ≥ **N_std / 2**.

Any one of (a), (b), (c) failing in either train or validate of
the primary tier (N_std = 1.5, one-sided elevated) → **refuted**
under the primary direction. Sensitivity arms reported alongside.

If fewer than 10 clean crash episodes per window → **inconclusive**.

## 6. Pre-committed verdict mapping per era directionality

Per HA06b + HA10 expectations:

| era / direction | predicted from prior tests | locked criterion |
|---|---|---|
| train one-sided elevated | SUPPORTED (canonical, stress rises = HRV drops before crash) | strict bar |
| train bidirectional | SUPPORTED (subsumes elevated) | strict bar |
| train one-sided lowered | refuted expected | sensitivity arm only |
| validate one-sided elevated | refuted expected (per HA06b/HA10 reversal) | sensitivity arm only |
| validate bidirectional | SUPPORTED expected if paradoxical-lowered holds | strict bar |
| validate one-sided lowered | SUPPORTED expected (parasympathetic swing → HRV rises → sleep stress drops) | sensitivity arm; report explicitly |

A pattern where validate one-sided lowered SUPPORTS (matching the
HA10 paradoxical-elevated-BB / HA06b paradoxical-lowered-RHR direction
mapped through HRV-proxy inversion) is consistent with the project's
era directionality reversal theory. Such a finding does NOT promote
to overall SUPPORTED under the locked rule (which requires the
primary direction to support in both eras) but is reported as
**era-asymmetric SUPPORTED** with explicit directionality
explanation.

## 7. Expected effect size if hypothesis is true

- Train one-sided elevated 4d primary: 60-80% trigger rate at +15-25
  pp disc (matching HA06b / HA11 train magnitudes).
- Validate primary direction refuted; validate one-sided lowered
  SUPPORTED at +15-30 pp if the parasympathetic-swing-mirrors
  hold.
- Median |z_delta|: 1.5-2.5.
- Null sample base rate: 6-15%.

## 8. Caveats `result.md` must explicitly acknowledge

- **Sleep stress is a proxy for HRV, not HRV itself**. The
  relationship is non-linear and bounded [1, 100]. Effect sizes
  are NOT comparable to HRV-literature values.
- **A REFUTED HA07c result does NOT refute the HRV hypothesis.**
  It refutes the proxy. The HRV hypothesis remains untested for
  this dataset.
- **A SUPPORTED HA07c result does NOT confirm the HRV hypothesis
  directly**. It supports the proxy's discriminative value, which
  is its own finding worth banking.
- **Cross-channel coherence with HA06b RHR / HA10 BB / HA11 U-dip
  is the strongest validation** the proxy can provide. If sleep
  stress shows era directionality reversal mirroring those
  channels, the proxy is doing its job.
- **Sleep window definition depends on Garmin's algorithm**. The
  `sleepStartTimestampGMT` is an algorithm output, not a
  ground-truth measurement. ±10-15 min uncertainty.
- **Garmin API ToS-grey**. The endpoint is undocumented for personal
  use; data could become inaccessible if Garmin changes the API.
- **`crash_v1` mixes mechanisms**. Same caveat as all prior tests.
- **Multi-comparison**. HA07c is the 17th pre-registered hypothesis
  (replacing HA07 in the count). Held-out validation discipline
  applies.

## 9. What we do with each outcome

- **Supported in both windows AND directions matching the era
  reversal pattern** → fifth train-era and third validate-era
  channel-confirmed via HRV-proxy. Strongest cross-channel
  convergence in the project. Card (b) train + (b2) validate
  retrospectives both gain anchors. HRV hypothesis remains
  unproven but proxy is fully validated.
- **Train supported, validate refuted** → fifth train-era channel
  confirms; HRV proxy adds train-era robustness. Validate
  unchanged (HA10 only).
- **Train refuted, validate supported lowered** → validate-era
  swing pattern becomes three-channel confirmed (HA06b + HA10 +
  HA07c proxy); train HRV-proxy channel is null. Surprising; the
  three SUPPORTED stress-spike-related train tests (H02b, H02d,
  HA11) make this unlikely.
- **Both refuted** → HRV proxy is not a precursor channel for
  this participant. Joins H03b as the only path-C tests; if H03b
  also doesn't sharpen, the path C investment has limited yield.

---

*Pre-registration locked 2026-06-07 before any sleep-stress data
inspection. Same test-script pattern as HA10 / HA11 with sleep
stress mean delta loading. Same `--dry-run` mode; same null seed
(`20260605`); same lagged baseline machinery.*
