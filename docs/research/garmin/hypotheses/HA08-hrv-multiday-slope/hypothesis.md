# HA08 — Multi-day HRV creep / slope (z-score) as crash precursor

**STATUS: BLOCKED-PENDING-HARDWARE (2026-06-07, later same day).**
Same blocker as [HA07](../HA07-hrv-day-over-day/hypothesis.md) —
the Forerunner 245 hardware does not record nightly HRV.

**This hypothesis remains as audit-trail record. It cannot be run
on this dataset.**

**Substitute test pre-registered**: **HA08c (multi-day sleep
stress mean slope as HRV-proxy creep)** at
[../HA08c-sleep-stress-slope/hypothesis.md](../HA08c-sleep-stress-slope/hypothesis.md).

---

**Original pre-registration written 2026-06-07, before any HRV data
had been pulled.** Locked. Any subsequent change creates an HA08b.

HA08 tests Wiggers' attribution: *"HRV daalt over meerdere dagen na
overbelasten"* — the slow-erosion mode, complementary to HA07's
single-night-shock mode. Where HA07 catches day-over-day drops,
HA08 catches sustained multi-day trends.

This matches the A.2 trend-slope concept from Theme A (locked
2026-06-06) but applied to the HRV signal instead of activity-load.

**Computability gate: H04b path C authorisation must complete first**
(unlocks the Garmin Connect REST API endpoint
`/wellness-service/wellness/dailyHrv/{date}`). Same gate as HA07.

## 1. Claim

In the **4 days** before a `crash_v1` episode (primary) and the
**5 days** before a `crash_v1` episode (secondary), at least one
day's trailing-5-day HRV slope deviates from its lagged personal
baseline by **(slope_5d − μ_slope) / σ_slope ≤ −N_std** (one-sided
lowered = sustained downward HRV trend, per Wiggers' "creep"
direction). The crash-episode frequency of this deviation is
discriminative against randomly-sampled non-crash windows in
**both train and validate windows independently**.

**Primary direction: one-sided lowered** (Wiggers' framing).
Bidirectional + one-sided elevated as sensitivity arms per the
HA10 era-directionality-reversal pattern.

## 2. Why we think this

- **Wiggers' "HRV daalt over meerdere dagen na overbelasten"** is
  the explicit slow-erosion mode pattern. Single-night drops
  (HA07) catch acute shock; multi-day slopes catch sustained push.
- **The Theme A trend-slope concept (A.2) was deliberately
  designed for this pattern** — sustained creeps that rebase into
  their own rolling baseline. HA08 is the cleanest physiological
  channel to test A.2's slope-as-first-class-metric approach.
- **Pre-cliff era's sympathetic-overarousal pattern** is now
  four-channel-confirmed (H02b, H02d, HA06b, HA11). A sustained
  HRV decline over days would be its smoothed multi-day signature.
- **Wiggers' framing fits both eras differently**: pre-cliff era's
  "overbelasten" produces sustained HRV decline (canonical); post-
  cliff era's stabilisation should produce different multi-day
  patterns. If validate one-sided lowered REFUTES while validate
  one-sided elevated (sustained HRV climb) SUPPORTS, the
  parasympathetic-swing pattern (HA06b lowered RHR + HA10 elevated
  BB) gains a third channel signature.
- **Complements HA07**: HA07 catches single-night events; HA08
  catches gradual creeps. They should be partially overlapping
  but not redundant. A pattern where one supports and the other
  refutes is interpretable (acute vs sustained mechanism).

## 3. Data sources

- **Crash labels**: `crash_v1` from
  [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv).
- **Nightly HRV**: same as HA07 (Garmin Connect REST API
  `/wellness-service/wellness/dailyHrv/{date}`).
- **Analysis window + train/validate split**: same as HA07.

## 4. Measurement protocol

### 4.1 Trailing-5-day HRV slope

For each calendar day `d` with sufficient prior HRV data:
- Collect HRV values from days `[d-4, d-3, d-2, d-1, d]` (5
  consecutive days including d).
- Require ≥ 4 of 5 days to have valid HRV.
- Compute OLS slope of HRV value vs day-index over the available
  points. Units: ms/day.
- Negative slope = HRV declining over the window.

`slope_5d[d]` = OLS slope of HRV over the trailing 5-day window
including d.

### 4.2 Lagged personal baseline of slopes (per Theme A)

For each valid day `d` with a defined `slope_5d`:
- Baseline window: slopes computed on days in `[d-90, d-30]`.
- Trimmed mean (10/90 cut) `μ_slope`; stdev `σ_slope`.
- Computed only when ≥ 40 valid slope values are available in the
  baseline window.
- If `σ_slope` ≤ 0.2 ms/day, flag as low-variability and skip.
  Report fraction.

### 4.3 Per-day z-scored slope

For each valid day `d`:
- `delta_slope(d) = slope_5d(d) − μ_slope(d)` (signed; ms/day)
- `z_slope(d) = delta_slope(d) / σ_slope(d)` (signed)
- `|z_slope(d)|` (unsigned)

### 4.4 Per-episode lead-up profile

Same structure as HA07:
- 4-day primary lead-up: [C-4, C-3, C-2, C-1].
- 5-day secondary lead-up: [C-5, C-4, C-3, C-2, C-1].
- Min valid days: 3 of 4 for primary; 4 of 5 for secondary.
- **Primary trigger flag (one-sided lowered)**: `min z_slope ≤ −N_std`
  in lead-up.
- Sensitivity arms: bidirectional `max |z_slope| ≥ N_std`;
  one-sided elevated `max z_slope ≥ +N_std`.

### 4.5 Threshold N_std

| Tier | N_std |
|---|---:|
| Primary | **1.5** |
| Secondary | **2.0** |
| Sensitivity check | **2.5** |

### 4.6 Null sample

200 random non-overlapping reference dates, seed `20260605`.

## 5. Pre-registered falsification criterion

Identical to HA07: 60% / +15 pp / median ≥ N_std/2 in BOTH eras
under primary one-sided lowered direction.

## 6. Comparison to HA07

HA07 and HA08 test the same channel (HRV) at different timescales:

- **HA07** = single-night shock (delta from previous night).
- **HA08** = multi-day creep (slope over 5 days).

Pre-commit on the interpretation:

| HA07 | HA08 | reading |
|---|---|---|
| SUPPORTED | SUPPORTED | both shock + creep are real; HRV is the dominant precursor channel |
| SUPPORTED | refuted | acute shock dominates; sustained creep is not a separate signal |
| refuted | SUPPORTED | slow creep dominates; single-night shocks too noisy |
| refuted | refuted | HRV channel is null; direction shifts to BB (H03b) or back to stress / RHR / U-dip aggregates |

## 7. Expected effect size if hypothesis is true

- Train one-sided lowered 4d primary: 60-80% trigger rate at +15-25
  pp disc.
- Validate primary direction refuted; validate one-sided elevated
  may SUPPORT if parasympathetic-swing pattern manifests as
  *sustained* HRV climb (HA10's BB-peak elevated pattern's slow
  cousin).
- Median |z_slope|: 1.5-2.5.
- Null sample base rate: 6-15%.

## 8. Caveats `result.md` must explicitly acknowledge

- All HA07 caveats apply (ToS-grey API, firmware 7.30 cutoff,
  HRV-feeds-stress confound, watch-off coverage).
- **Slope can be sensitive to single outliers**. The OLS slope of
  5 points can swing dramatically if one day has an extreme HRV
  value. Robust regression (e.g. Theil-Sen) is a viable alternative
  but is NOT pre-registered as primary; OLS is locked.
- **5-day window choice**. Wiggers describes "multiple days" without
  pinning a number. 5 days is the choice locked here, matching the
  empirical 4-5 day PEM lag confirmed across four channels. A 7-day
  window is also defensible and is reported as a secondary
  sensitivity arm.
- **Multi-comparison**. HA08 is the 18th pre-registered hypothesis.

## 9. What we do with each outcome

- **Supported in both windows AND directions matching HA06b/HA10/HA07
  reversal pattern** → A.2 slope-as-first-class-metric concept is
  validated on a clean physiological channel. Sets up replication
  for HRV-slope (B-channel) and BB-recharge-slope (overnight) as
  alternative metric shapes.
- **Train supported, validate refuted** → adds to train-era cluster.
- **Train refuted, validate supported** → unusual; investigate.
- **Both refuted** → multi-day HRV creep not detectable for this
  participant at the slope/z-score operationalisation; consider
  alternative metric shapes for the future (HA08b on EWMA-based
  trend extraction, or HA08c with longer 10-14 day windows).

---

*Pre-registration locked 2026-06-07 before any HRV pull. Same
test-script pattern as HA10 with slope loading replacing
morning-peak loading. Same `--dry-run` mode; same null seed
(`20260605`); same lagged baseline machinery.*
