# HA10 — Body Battery overnight recharge as crash precursor (coarse 3-anchor proxy, z-score relative thresholds)

**Pre-registration written 2026-06-07, before any BB-recharge data
was inspected for this test.** Locked. Any subsequent change creates
an HA10b.

HA10 tests the overnight-recovery / autonomic-recharge mechanism
through the Garmin Body Battery channel, using the 3 daily UDS
anchor points (HIGHEST / LOWEST / MOSTRECENT / ENDOFDAY) **without
needing per-minute BB decoding**. Per Wiggers' lived-experience
framing: chronic-illness Body Battery rarely reaches 100% even with
adequate sleep; she calls 70-80% her practical "stay above" floor
for stability. A morning peak that falls short of personal-typical
should precede crashes if the overnight-recharge mechanism is a
precursor channel for this participant.

**This is the coarse proxy.** The per-minute version (H03b) is
gated on H04b decoding `unknown_233` or authorising the Garmin
Connect REST API path. HA10 is operationalisable NOW with existing
UDS data and **pre-commits a soft outcome that informs whether
H04b's per-minute version is worth the decoding effort**:

- If HA10 SUPPORTS in either era → per-minute version is worth
  H04b's effort.
- If HA10 REFUTES both eras → the overnight-recharge channel
  likely has no precursor signal at coarse resolution. H03b's
  priority drops materially.

## Why is HA10 next instead of HA07?

HA07 was originally next on queue (HRV channel; less blunted by
chronotropic incompetence than RHR). But **HRV data is not
available in the GDPR export**: no HRV field exists in UDS,
sleepData, bioMetrics, monitoring_b FIT files, or activity FIT
files for this participant's Forerunner 245 dump. The HRV records
live only in the Garmin Connect cloud, accessible via the same
ToS-grey REST API path as H04b's per-minute BB (`python-garminconnect`
endpoint `/wellness-service/wellness/dailyHrv/{date}`). HA07 is
therefore gated on the same authorisation as H04b.

HA10 is the next-best autonomic-channel test that runs on existing
data, and **also serves H04b prioritisation** through its
pre-committed soft outcome.

## 1. Claim

In the **4 days** before a `crash_v1` episode (primary) and the
**5 days** before a `crash_v1` episode (secondary), at least one
day's morning Body Battery peak deviates from its lagged personal
baseline by **|morning_peak − baseline_μ| / baseline_σ ≥ N_std**
(N_std locked below). The crash-episode frequency of this deviation
is discriminative against randomly-sampled non-crash windows in
**both train and validate windows independently**.

The bidirectional formulation (consistent with HA06b's design)
catches both "low morning peak" (the Wiggers / Workwell expected
direction) and "high morning peak" (less expected but symmetric)
patterns. A sensitivity arm reports the one-sided lowered-only
result so we can see whether the bidirectional framing is doing the
work.

## 2. Why we think this

- **Wiggers explicitly anchors on the morning BB peak**: chronic-
  illness BB rarely reaches 100% even with adequate sleep; she
  flags below 70-80% as her practical floor. The morning HIGHEST
  anchor in Garmin UDS is the natural readout for this.
- **Bateman Horne Center's "back to baseline next morning?"**
  heuristic is the strongest external evidence in the pacing
  literature for overnight-recovery as a precursor channel.
- **The H04 daily-BB-net-delta test showed a positive-direction
  validate-era hint** (+13.3 pp discrimination, just below the
  +15 pp bar). That signal lives in a related but different
  construct (daily net charge vs morning peak). HA10 tests the
  more physiologically targeted version of the same channel.
- **The locked
  [`relative_not_absolute`](../../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_relative_not_absolute.md)
  feedback principle** says explicitly: *"For PEM-pacing metrics in
  this project, always use z-scores or deviations from personal
  baseline, not absolute thresholds."* Per the HA06b methodology
  lesson, we pre-register on z-score thresholds from the start, NOT
  Wiggers' absolute 70-80% floor — since that floor is calibrated
  to lotgenoten populations whose BB-recharge variability may not
  match this participant's.
- **Three train-era SUPPORTED autonomic-deviation precursors on
  three channels** (H02b stress spike 3d, H02d bridge × 5d stress
  spike, HA06b RHR z-score 4d) — if HA10 also SUPPORTS in train,
  the pre-cliff autonomic-deviation pattern is four-channel-confirmed.
  If validate SUPPORTS (which it has not on any prior channel), the
  D7 reframe gains its first empirical validate-era anchor.

## 3. Data sources

- **Crash labels**: `crash_v1` from
  [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv).
- **Body Battery anchors**: Garmin UDS `bodyBattery.bodyBatteryStatList`,
  filtered to records where `bodyBatteryStatType == "HIGHEST"`. Same
  path and dedup logic as H04. Each day's HIGHEST anchor has a
  `statsValue` (BB level, 0-100) and a `statTimestamp`.
- **Analysis window + train/validate split**: same as HA06b
  (train 2022-09-03 → 2023-12-31, 14 episodes; validate
  2024-01-01 → 2026-06-05, 15 episodes).

## 4. Measurement protocol

### 4.1 Per-day morning BB peak

For each calendar day `d`:

- Take the HIGHEST anchor's `statsValue` from the UDS record for
  date `d`.
- **Time-window filter**: only include if the HIGHEST timestamp
  falls between **03:00 and 10:00 local time** on day `d`. This
  ensures it represents the overnight rebound rather than a
  daytime peak (e.g. post-nap). Daytime-peak days are flagged and
  excluded from the analysis with their count reported separately.
- Validity range: `morning_peak` ∈ [0, 100]. Values outside are
  dropped (none expected, but defensive).
- If no HIGHEST anchor exists for day `d`, the day is skipped.

This yields `morning_peak[d]` per valid day.

### 4.2 Lagged personal baseline (per Theme A)

For each day `d`:

- Baseline window: days in `[d-90, d-30]` (60-day window, ending
  30 days before `d`). Identical to HA06 / HA06b.
- **Baseline mean (μ)**: trimmed mean with 10/90 cut.
- **Baseline std (σ)**: standard deviation of the same trimmed
  prior-value list used for the mean.
- Computed only when ≥ 40 of 60 prior days have a valid
  `morning_peak`. If σ ≤ 2.0 BB points — i.e. the baseline is
  essentially flat — flag the day as *low-variability* and skip
  it in the test (avoids division by near-zero noise; report
  fraction of such days). (The 2.0 BB-point floor is intentionally
  higher than HA06b's 0.5 bpm floor because BB is a 0-100 scale
  with much wider day-to-day swings; a flat baseline is genuinely
  unusual.)

### 4.3 Per-day z-scored delta

For each day `d` with both `morning_peak` and a defined (μ, σ)
pair:

- `delta(d) = morning_peak(d) − μ(d)` (signed; BB points)
- `z(d) = delta(d) / σ(d)` (signed; std-units)
- `|z(d)| = abs(z(d))` (unsigned; primary metric for bidirectional)
- Sign label: `elevated` if z ≥ N_std, `lowered` if z ≤ −N_std,
  `neutral` otherwise.

### 4.4 Per-episode lead-up profile

For each crash episode with start date `C`:

- 4-day primary lead-up: days [C-4, C-3, C-2, C-1].
- 5-day secondary lead-up: days [C-5, C-4, C-3, C-2, C-1].
- For each lead-up day, compute `z(d)` if valid.
- Episode requires ≥ 3 of 4 valid days for primary,
  ≥ 4 of 5 for secondary (same as HA06b).
- **Episode trigger flag (bidirectional, primary)**:
  `max |z| ≥ N_std` across valid lead-up days.
- Record signed direction of the max-|z| day (elevated / lowered).
- Record all signed z values across the lead-up for downstream
  analysis.

### 4.5 Threshold N_std

Three pre-registered thresholds, consistent with HA06b / HA07's
planned thresholds:

| Tier | N_std | Two-tail fraction (Gaussian) | Anchor |
|---|---:|---:|---|
| Primary | **1.5** | ~13.4% | mild-to-moderate deviation |
| Secondary | **2.0** | ~4.6% | classical "outlier" threshold |
| Sensitivity check | **2.5** | ~1.2% | strict; only catches extreme deviations |

The **primary tier (N_std = 1.5) determines the headline verdict**;
secondary and sensitivity check are reported alongside.

### 4.6 Null sample

200 random non-overlapping reference dates, same construction +
seed (`20260605`) as HA06 / HA06b. Per-window null trigger flag
computed exactly as in §4.4.

### 4.7 Sensitivity arm — one-sided "lowered only" (Wiggers direction)

Same lead-up windows as §4.4 but using signed z ≤ −N_std (not |z|).
This is the directional version Wiggers' framing predicts: morning
peak is LOWER than personal baseline → BB did not recharge as well
as usual → precursor. If primary supports but one-sided lowered
arm refutes, elevated-direction events are doing the work — flag
and report.

### 4.8 Directionality split

Of the SUPPORTED crash windows under the bidirectional primary,
report what fraction of triggering events are `elevated`
(z ≥ +N_std) vs `lowered` (z ≤ −N_std). HA06b documented a striking
era reversal (train 70% elevated → validate 75% lowered); HA10
should report whether the same pattern appears on the BB channel.

### 4.9 Sensitivity arm — overnight delta metric (optional)

As a secondary metric arm, also compute:
`overnight_delta[d] = morning_peak[d] − evening_low_preceding[d]`

where `evening_low_preceding[d]` is the LOWEST anchor with timestamp
preceding `morning_peak[d]`'s timestamp within 24 hours. Z-score
against its own lagged baseline distribution. Reported as a
sensitivity arm only — the primary metric remains `morning_peak`
(Wiggers-anchored). This sensitivity arm tells us whether the test
is more sensitive to "the level reached" or "the amount recharged."

## 5. Pre-registered falsification criterion

Identical three-criterion bar shape to H02b / HA01b / HA06b / H02d:

**(a) Frequency**: at least **60%** of crash episodes have
`max |z| ≥ N_std` in their lead-up window.

**(b) Discrimination**: the crash-episode frequency from (a) is at
least **15 percentage points higher** than the null-sample
frequency.

**(c) Magnitude**: the median `max |z|` across crash episodes is at
least **N_std / 2** (0.75 / 1.0 / 1.25 for N_std = 1.5 / 2.0 / 2.5
respectively).

Any one of (a), (b), (c) failing in either train or validate of the
primary tier (N_std = 1.5) → **refuted**.

If we have fewer than 10 clean crash episodes per window after
exclusions → **inconclusive**.

## 6. Exclusion rules

- Days where the HIGHEST anchor timestamp is outside 03:00-10:00
  local (daytime peak, likely post-nap or watch-off-overnight) are
  excluded from the analysis. Report the count of such exclusions.
- Days where baseline σ ≤ 2.0 BB points are flagged *low-variability*
  and excluded.
- Days where fewer than 40 of 60 prior days have a valid
  `morning_peak` are excluded (insufficient baseline).
- Train/validate split: same boundary as all prior tests.

## 7. Expected effect size if hypothesis is true

- 60-80% of crash episodes have `max |z| ≥ 1.5` in the 4-day lead-up.
- Null sample rate: 13-30% (Gaussian-tail expectation under no
  signal is ~13.4% per day; max over 4 days inflates this).
- Median `max |z|`: 1.5-2.5.
- Directionality split prediction: train-era likely skewed toward
  `lowered` (Wiggers' canonical direction); validate-era unclear
  given HA06b's reversal pattern on RHR — possible the BB channel
  inherits the same reversal, possible it doesn't.
- If crash rate ≥ 95% and null rate ≥ 85% → metric is over-inflated;
  flag and consider whether N_std = 1.5 is too loose.

## 8. Caveats `result.md` must explicitly acknowledge

- **3-anchor coarse proxy**. The HIGHEST anchor captures the peak
  but not the recharge trajectory (how steep, when it occurred
  relative to wake). The per-minute version (H03b via H04b) would
  capture trajectory; HA10 cannot. If HA10 REFUTES, the trajectory
  version may still SUPPORT.
- **Garmin's BB algorithm is opaque**. Firmware changes between FR245
  versions 7.x and 10.4 plausibly shifted the BB algorithm's
  internal calibration. The lagged baseline partially compensates
  for slow drift but a sudden algorithm change would distort.
- **Watch-off nights don't contribute**. Verify the night-coverage
  rate matches HA06's 99.4% train / 98.6% validate before running.
- **Daytime-peak days excluded**. Days where the HIGHEST timestamp
  falls outside 03:00-10:00 are excluded as "not a morning peak."
  This may exclude legitimate "slept late and got up at 11" days.
  The count of exclusions should be reported; if exclusions exceed
  ~10% of crash episodes' lead-up days, flag for design review.
- **`crash_v1` mixes mechanisms**. Same caveat as all prior tests.
- **Multi-comparison**. HA10 is the 14th pre-registered hypothesis
  in the H##/HA## series. The held-out validate window is the
  primary defence.
- **Chronotropic-incompetence-adjacent**: BB is derived in part
  from stress/HRV signals which are HR-dependent. If chronotropic
  incompetence blunts HR-derived signals (Workwell's caveat for
  HA06), BB may inherit some of that blunting. The morning-peak
  level itself is more about cumulative overnight HRV recovery
  than acute HR response, so the blunting concern is weaker here
  than for HA06.
- **The "soft outcome for H04b" pre-commitment**: explicitly state
  in the result.md whether HA10's verdict moves H04b's priority
  up or down per §9 below.

## 9. What we do with each outcome

- **Supported in both windows** (primary 4d, both train + validate)
  → **first overall-SUPPORTED precursor of the project under clean
  methodology**. Provides the empirical stake for the D7 single-
  mechanism-two-regimes reframe. H04b per-minute decode is **strongly
  prioritised** — the coarse signal is already there; the per-minute
  trajectory will be sharper. Then `card.md`: a BB-recharge-aware
  card concept for both eras.
- **Train supported, validate refuted** → adds a fourth train-era
  SUPPORTED autonomic-deviation precursor to the project (after H02b,
  H02d, HA06b). The pre-cliff multi-channel pattern strengthens.
  H04b remains **moderately prioritised** for train-era retrospective
  surfacing; validate-era still has no measurable precursor.
- **Train refuted, validate supported** → unusual; would be the first
  validate-era precursor in the project, and on a channel where
  train should arguably show more signal. Investigate carefully.
  H04b **highly prioritised** to confirm with per-minute version.
- **Refuted in both windows** → BB overnight-recharge channel
  shows no signal at coarse resolution. **H04b's priority drops
  materially**: per-minute BB decoding may not unlock a precursor
  signal worth the effort. Focus shifts to (i) HA11 within-day
  stress U-dip pattern, (ii) HA07 + HA08 if API path C is
  eventually authorised.
- **Primary refutes but sensitivity arm differs** → report honestly;
  do not redefine the headline verdict on the sensitivity arm's
  result. Document for HA10b consideration if API access is later
  obtained.

---

*Pre-registration locked 2026-06-07. Same test-script pattern as
HA06b with morning-peak loading replacing RHR loading; same
`--dry-run` mode; same null seed (`20260605`); same lagged baseline
machinery.*
