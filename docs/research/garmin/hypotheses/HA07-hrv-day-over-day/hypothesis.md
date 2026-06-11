# HA07 — Day-over-day HRV drop (z-score) as crash precursor

**STATUS: BLOCKED-PENDING-HARDWARE (2026-06-07, later same day).**
The Forerunner 245 hardware does **not** record nightly HRV — HRV
Status was added to Garmin's newer Forerunner 255/265/955/965 and
Fenix 7 generation watches via a newer multi-sample optical HR
sensor that the FR245's 2019 hardware lacks. Garmin Connect's
`/hrv-service/hrv/{date}` endpoint returns an empty dict for every
date in this dataset (verified 2026-06-07 across 6 sample dates
spanning 2022-2026). The endpoint exists, the user is authenticated,
but no HRV records were ever captured by the watch.

**This hypothesis remains as audit-trail record. It cannot be run
on this dataset.** A future watch upgrade plus 3+ years of
post-upgrade data would be needed to unblock.

**Substitute test pre-registered**: **HA07c (sleep stress mean
delta as HRV proxy)** at [../HA07c-sleep-stress-mean-delta/hypothesis.md](../HA07c-sleep-stress-mean-delta/hypothesis.md).
Garmin's stress signal is HRV-derived during sleep when activity ≈ 0
and is used by Workwell / Wiggers as an HRV proxy in pacing
recommendations. The result.md of HA07c must explicitly acknowledge
the proxy relationship.

---

**Original pre-registration written 2026-06-07, before any HRV data
had been pulled.** Locked. Any subsequent change creates an HA07b.

HA07 tests Wiggers' attribution to *de vermoeidheidskliniek* —
a drop of ≥ 10 HRV points night-over-night may indicate PEM is
coming. Per the HA06b methodology lesson banked 2026-06-07, we
pre-register on **z-score thresholds**, not the absolute 10 ms,
since 10 ms is calibrated to lotgenoten / fatigue-clinic
populations whose HRV variability may not match this participant's.

**Computability gate: H04b path C authorisation must complete first**
(unlocks the Garmin Connect REST API endpoint
`/wellness-service/wellness/dailyHrv/{date}`). HRV is not present in
any local data source for this participant's Forerunner 245 GDPR
dump (verified 2026-06-07 across UDS, sleepData, bioMetrics,
monitoring_b FIT, activity FIT).

HA07 is the **first HRV-channel test** in the project. HRV is less
subject to chronotropic incompetence than HR (Workwell's caveat
for HA06) — if HA07 train SUPPORTS, the pre-cliff
sympathetic-overarousal precursor signature becomes
**five-channel-confirmed**. If validate SUPPORTS in any direction,
the validate-era picture becomes multi-channel anchored.

## 1. Claim

In the **4 days** before a `crash_v1` episode (primary) and the
**5 days** before a `crash_v1` episode (secondary), at least one
night-over-night HRV delta deviates from its lagged personal
baseline by **(HRV[d] − HRV[d-1] − μ_delta) / σ_delta ≥ N_std**
(one-sided lowered = drop, per Wiggers' canonical direction) or
**|...| ≥ N_std** (bidirectional sensitivity arm; per HA06b lesson
that validate-era pattern may be opposite). The crash-episode
frequency of this deviation is discriminative against
randomly-sampled non-crash windows in **both train and validate
windows independently**.

**Primary direction: one-sided lowered** (Wiggers' framing). Per
HA10's directionality reversal between eras, the bidirectional and
one-sided elevated arms are reported as sensitivity arms — if
validate inverts to the elevated direction (consistent with HA06b
+ HA10 pattern), the elevated arm catches it.

## 2. Why we think this

- **Wiggers / vermoeidheidskliniek explicit prediction**:
  night-over-night HRV drop ≥ 10 ms signals PEM coming. Pre-cliff
  era with active sympathetic overarousal should produce this
  pattern in lead-up windows.
- **HRV is the cleanest physiological channel for autonomic state**.
  Less HR-dependent than RHR (HA06b's "chronotropic incompetence"
  caveat applies less); Garmin's stress algorithm uses HRV as
  primary input but HRV-direct should be sharper still.
- **Four train-era SUPPORTED autonomic precursors on four channels**
  (H02b stress spike, H02d bridge × 5d, HA06b RHR z-score, HA11
  U-dip count z-score). HA07 train SUPPORTED would make five.
- **HA06b documented era directionality reversal** (train elevated
  RHR → validate lowered RHR). HRV is inversely-related to RHR
  via vagal tone, so the predicted directionality:
  - Train: HRV *drops* before crashes (canonical Wiggers direction)
  - Validate: HRV *rises* before crashes (paradoxical swing
    direction, matching HA10 elevated BB peak)
  Bidirectional sensitivity arm catches both.
- **HA10's validate-era SUPPORTED at +16.2 pp** in the paradoxical
  direction provides the strongest prior that HRV validate may
  show the same paradoxical elevated direction. If yes, HA07
  validate SUPPORTED in the elevated direction would add a
  **third channel to the validate-era parasympathetic-swing
  signature** (after HA06b lowered RHR + HA10 elevated BB).

## 3. Data sources

- **Crash labels**: `crash_v1` from
  [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv).
- **Nightly HRV**: Garmin Connect REST API endpoint
  `/wellness-service/wellness/dailyHrv/{date}` via
  `cyberjunky/python-garminconnect`. Field name + unit verified on
  smoke-test batch before locking spec. Expected: RMSSD-derived in
  ms.
- **Analysis window + train/validate split**: same as HA06b / HA10
  / HA11.

## 4. Measurement protocol

### 4.1 Per-night HRV value

For each calendar day `d`:
- Pull the API response for date d.
- Extract the nightly HRV value (field name TBD on smoke test;
  documented in result.md).
- Validity range: typically RMSSD is in [10, 200] ms. Drop values
  outside as bad data.
- If the night has no HRV (watch off, firmware < 7.30, or API
  null), the night is skipped.

### 4.2 Day-over-day delta

For each pair of consecutive valid days `(d-1, d)`:
- `delta_dod(d) = HRV(d) − HRV(d-1)` (signed; ms).
- If either `d-1` or `d` is invalid, no delta is computed for d.

### 4.3 Lagged personal baseline of deltas (per Theme A)

For each day `d` with a defined delta_dod(d):
- Baseline window: deltas computed on days in `[d-90, d-30]`.
- Trimmed mean (10/90 cut) `μ_delta`; stdev `σ_delta`.
- Computed only when ≥ 40 valid delta pairs are available in the
  baseline window.
- If `σ_delta` ≤ 1.0 ms, flag as low-variability and skip. Report
  fraction.

**Variant fallback**: if delta-baseline approach has variance
pathology (e.g. wide tails dominated by single outliers), fall
back to baselining `HRV[d]` against the HRV-value distribution
(not the delta distribution). This decision must be made on the
dry-run, not on the test result. Documented in the result.md.

### 4.4 Per-day z-scored delta

For each day `d` with both `delta_dod` and a defined (μ_delta,
σ_delta) pair:
- `z_delta(d) = (delta_dod(d) − μ_delta(d)) / σ_delta(d)` (signed)
- `|z_delta(d)|` (unsigned)

### 4.5 Per-episode lead-up profile

Same structure as HA10 / HA11:
- 4-day primary lead-up: [C-4, C-3, C-2, C-1].
- 5-day secondary lead-up: [C-5, C-4, C-3, C-2, C-1].
- Min valid days: 3 of 4 for primary; 4 of 5 for secondary.
- **Primary trigger flag (one-sided lowered)**: `min z_delta ≤ −N_std`
  in lead-up (the most negative delta-z in the window).
- Sensitivity arms: bidirectional `max |z_delta| ≥ N_std`;
  one-sided elevated `max z_delta ≥ +N_std`.
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

Identical three-criterion bar shape to HA06b / HA10 / HA11:

**(a) Frequency**: at least **60%** of crash episodes trigger.

**(b) Discrimination**: ≥ **+15 pp** above null.

**(c) Magnitude**: median trigger magnitude ≥ **N_std / 2**.

Any one of (a), (b), (c) failing in either train or validate of
the primary tier (N_std = 1.5, one-sided lowered) → **refuted**
under the primary direction. Sensitivity arms reported alongside.

If fewer than 10 clean crash episodes per window → **inconclusive**.

## 6. Pre-committed verdict mapping per era directionality

Per HA06b + HA10 expectations:

| era / direction | predicted from prior tests | locked criterion |
|---|---|---|
| train one-sided lowered | SUPPORTED (canonical, HRV drop precedes crash) | strict bar |
| train bidirectional | SUPPORTED (subsumes lowered) | strict bar |
| train one-sided elevated | refuted expected | sensitivity arm only |
| validate one-sided lowered | refuted expected (per HA06b/HA10 reversal) | sensitivity arm only |
| validate bidirectional | SUPPORTED expected if paradoxical-elevated holds | strict bar |
| validate one-sided elevated | SUPPORTED expected (parasympathetic swing) | sensitivity arm; report explicitly |

A pattern where validate one-sided elevated SUPPORTS (matching the
HA10 paradoxical direction) is consistent with the project's era
directionality reversal theory. Such a finding does NOT promote
to overall SUPPORTED under the locked rule (which requires the
*primary* direction to support in both eras) but is reported as
**era-asymmetric SUPPORTED** with explicit directionality
explanation.

## 7. Expected effect size if hypothesis is true

- Train one-sided lowered 4d primary: 60-80% trigger rate at +15-25
  pp disc (matching the magnitudes of HA06b, HA11 train).
- Validate primary direction refuted; validate one-sided elevated
  SUPPORTED at +15-30 pp (matching HA10's validate elevated arm
  +29.0 pp).
- Median |z_delta|: 1.5-2.5.
- Null sample base rate: 6-15% (one-sided Gaussian tail
  expectation under no signal is ~6.7% per day; max over 4 days
  inflates this).

## 8. Caveats `result.md` must explicitly acknowledge

- **Garmin API ToS-grey**. The endpoint is undocumented for personal
  use; data could become inaccessible if Garmin changes the API.
- **Firmware 7.30 cutoff**. FR245's HRV Status feature was added in
  August 2022. Pre-firmware-7.30 dates will return null HRV.
  Report coverage rate by month; if pre-7.30 dates dominate any
  era, flag for design review.
- **HRV is itself the input to Garmin's stress algorithm**. HA07's
  signal may overlap with H02b's stress-spike signal at the
  per-minute level. Note explicitly; treat as related but distinct
  observations (HA07 is per-night aggregate; H02b is per-minute
  spike).
- **Watch-off coverage**: nights without watch contribute no delta
  pair. Verify coverage matches HA06's 99.4% train / 98.6%
  validate before running; if substantially worse, flag.
- **Day-over-day variance can be high**. The 3-episode dry-run
  print MUST surface if the natural day-over-day HRV variability
  already produces |z_delta| ≥ 1.5 on ~50% of any random window
  (as RHR did under HA06b). If so, the test is structurally
  non-discriminative; flag and consider HA07b with a different
  metric primitive (e.g. HRV value directly z-scored, NOT
  delta-of-delta).
- **`crash_v1` mixes mechanisms**. Same caveat as all prior tests.
- **Multi-comparison**. HA07 is the 17th pre-registered hypothesis
  in the H##/HA## series. Held-out validation discipline applies.

## 9. What we do with each outcome

- **Supported in both windows AND directions matching the era
  directionality reversal** → five-channel confirmation for
  pre-cliff + three-channel confirmation for validate-era.
  Strongest single test result in the project. Card (b) train
  + (b2) validate retrospectives both gain anchors.
- **Train supported primary, validate refuted bidirectional**
  → adds to four-channel train cluster; validate stays at one-
  channel (HA10).
- **Train refuted, validate supported elevated** → validate-era
  swing pattern becomes two-channel confirmed (HA10 + HA07);
  train HRV channel is null for this participant.
- **Both refuted** → HRV is not a precursor channel for this
  participant. The four-channel train pattern stands; the
  one-channel validate pattern stands. Direction shifts to H03b
  (BB per-minute) as the next sharpening test for HA10.

---

*Pre-registration locked 2026-06-07 before any HRV pull. Same
test-script pattern as HA10 with HRV delta loading replacing
morning-peak loading. Same `--dry-run` mode; same null seed
(`20260605`); same lagged baseline machinery.*
