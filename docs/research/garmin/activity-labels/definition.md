# Activity labels — pre-registration

**Locked 2026-06-06**, before any crash-labelled inspection of the
activity data. The feature definitions and extraction protocol are
locked at this revision. **Severity cutoffs are deferred** to
`spec/severity_spec.md` and will be locked after a blinded
distribution-only review (see §5). Any subsequent change to feature
definitions or step-spike rule creates an `activity-labels-v2`.

## 1. Purpose

The 2026-06-05 research report and 2026-06-06 addendum repeatedly
flagged exertion as a blind spot. Specifically:

1. **H02b specificity check** tagged 15 of 83 false-positive spike
   windows as `activity_induced` using a coarse rule (any recorded
   activity ≥ 30 min on the peak-spike day). A proper exertion
   feature layer is needed to disentangle exertion-driven spikes
   from autonomic-arousal spikes.
2. **The pacing literature** consistently identifies exertion as
   the most direct PEM trigger. Crashes, dips, and dip clusters
   should all be testable against an exertion precursor.
3. **HRV-derived signals are degraded around exertion** — stress
   samples drop out during activities, body battery calculation
   includes exercise compensation. Knowing when activity occurred
   contextualises the biometric stream.
4. **Step spikes** are a participant-flagged signal: sudden
   increases in step count likely represent unrecorded physical
   exertion (cleaning, gardening, social spikes) that lab-style
   activity tracking misses.

This module builds a **per-day exertion-load feature table**
spanning the full Garmin window (2021-06 → 2026-05) consumable by
downstream analyses: re-runs of H02b, crash/dip precursor tests,
dip-cluster context analysis, and future H04b body-battery work.

### 1.1 Framing — PEM-risk envelope, not athletic training

The fields we extract from Garmin are designed for athletic
training: aerobic training effect, anaerobic training effect, HR
zones, vO2max. **We are not measuring training. We are measuring
exertion load that may exceed a PEM-prone envelope.** The
distinction matters in several places:

- **The primary classification driver is passive intensity
  minutes from UDS**, NOT recorded-activity training-effect
  scores. Garmin's UDS files capture
  `vigorousIntensityMinutes` and `moderateIntensityMinutes` for
  every day passively — regardless of whether the participant
  tapped "start activity". For PEM the silent exertion (cleaning,
  gardening, walking around a social event) is as relevant as the
  deliberate exertion. A 40-minute high-HR house move that wasn't
  recorded as a workout is a PEM trigger; an athlete's tracking
  app would miss it entirely.
- **Severity cutoffs are calibrated to this person's envelope,
  not to athletic norms.** A "very heavy" day for a PEM patient
  is not the same as a "very heavy" training day for a runner.
  The cutoffs (§5) reflect what tends to be challenging for this
  participant — calibrated from the distribution of this person's
  data, blinded to crash labels.
- **Training-effect fields are kept as descriptors, not
  classifiers.** `aerobicTrainingEffect` and
  `anaerobicTrainingEffect` are recorded per activity and stored
  in `activities.csv`, but they do not drive the daily
  `exertion_class`. They may be informative for context
  ("this run had aerobic TE 3.2") but the envelope question is
  about total daily load, not training stress.
- **The eventual goal is a feature that helps people with PEM**,
  not a fitness tracker. Generalisation across PEM-prone users
  (future work) will use this same framing: passively-detected
  exertion minutes calibrated to individual envelopes.

This framing is locked in this revision. Any downstream test that
inadvertently re-introduces athletic-training framing (e.g. uses
aerobic TE as a primary classifier) is a flag.

## 2. Data sources

### 2.1 Recorded activities (rich per-activity)
- **File**: `DI_CONNECT/DI-Connect-Fitness/user@example.com_0_summarizedActivities.json`
- **N = 404** activities, 2021-08-16 → 2026-04-16
- **Type breakdown**: 268 walking, 86 running, 42 cycling, 5
  breathwork, 2 sailing_v2, 1 incident_detected.
- **Fields used per activity**:
  - `activityType`, `startTimeGmt` (millis), `duration` (ms)
  - HR: `avgHr`, `maxHr`, `minHr`,
    `hrTimeInZone_0` .. `hrTimeInZone_6` (ms)
  - Intensity: `moderateIntensityMinutes`,
    `vigorousIntensityMinutes`
  - Training effect: `aerobicTrainingEffect` (0–5),
    `anaerobicTrainingEffect` (0–5)
  - Stress impact: `startStress`, `endStress`, `differenceStress`,
    `avgStress`, `maxStress`
  - Distance: `distance` (m), `elevationGain`, `elevationLoss`
  - Calories: `calories` (active)
  - Self-report (where present, ~20% coverage):
    `workoutRpe`, `workoutFeel`

### 2.2 Passive daily summaries
- **Files**: `DI_CONNECT/DI-Connect-Aggregator/UDSFile_*.json`
  (18 files, ~100 days each, totaling 1,800+ days)
- **Range**: 2021-06-25 → 2026-05-30
- **Fields used per day**:
  - Identity: `calendarDate`
  - Steps: `totalSteps`, `dailyStepGoal`, `totalDistanceMeters`
  - Intensity (passively detected, always present):
    `moderateIntensityMinutes`, `vigorousIntensityMinutes`
  - Active time: `highlyActiveSeconds`, `activeSeconds`
  - Energy: `activeKilocalories`
  - HR: `restingHeartRate`

**Why both**: recorded activities give per-event detail (which
walk, what HR zones, how long). UDS daily summaries give the
**unified daily exertion total** — empirically (verified on 191
days with recorded vigorous activity)
`UDS vigorous_min ≥ Σ recorded vigorous_min` in 100% of cases,
with a mean overshoot of ~2.7 min. So the UDS channel is a
**superset** that includes every minute from a recorded workout
PLUS passively-detected vigorous moments outside recorded
activity. No double-counting — UDS is the single unified
exertion-load measure.

What's still useful from recorded activities:
- HR zones (time at HR zone 4+ for individual events)
- Distance and elevation
- `differenceStress` — Garmin's own measure of how much the
  activity shifted the participant's stress baseline
- Self-reported `workoutRpe` / `workoutFeel` (sparse but high-
  signal when present)
- Activity *type* (a 60-minute cycle is different from a
  60-minute sail, even at the same UDS vigorous-min)
- Long-duration low-HR activities (e.g. 5-hour sailing at low
  intensity) that UDS would record as 0 vigorous-min but are
  PEM-relevant load.

## 3. Feature definitions (locked)

### 3.1 Per-activity table — `activities.csv`

One row per activity. All fields above, plus computed:
- `start_date` (local date from `startTimeGmt`)
- `duration_min` = `duration` / 60000
- `time_in_zone_4plus_min` = sum of zones 4, 5, 6 / 60000
- `intensity_min_total` = `moderate` + `vigorous`

No filtering or transformation beyond these computed columns.
Sentinel handling: zero-duration breathwork sessions kept (they
are real sessions); `incident_detected` kept (it's a known data
point); we do not drop any record.

### 3.2 Per-day daily UDS table — `daily_uds.csv`

One row per calendar day in the UDS window
(2021-06-25 → 2026-05-30). Columns:
- `date`, `total_steps`, `daily_step_goal`,
  `total_distance_m`, `moderate_min`, `vigorous_min`,
  `highly_active_sec`, `active_sec`, `active_kcal`,
  `resting_hr`

If a date is present in multiple UDS files (boundary days), the
most recent file's record wins. Days missing from all UDS files
are emitted with empty columns (no imputation).

### 3.3 Merged per-day feature table — `activity_features_daily.csv`

One row per calendar day in `[2022-09-03, 2026-06-05]` (the
gevoelscore analysis window). Columns:

**Identity**:
- `date`, `gevoelscore` (joined from `day_entries.csv`)

**From recorded activities (zero if no activity that day)**:
- `n_activities`
- `activity_types` (comma-separated, alphabetised)
- `total_activity_min`
- `max_activity_min`
- `total_calories`
- `max_aerobicTE`, `max_anaerobicTE`
- `max_avgHr`, `max_maxHr`
- `total_time_zone4plus_sec`
- `max_differenceStress` (signed; positive = stress went down)
- `total_distance_km`
- `avg_workoutRpe`, `avg_workoutFeel` (mean of present values; empty if none)

**From UDS daily passive (always present if UDS covers the day)**:
- `total_steps`, `daily_step_goal`
- `vigorous_min_uds`, `moderate_min_uds`
- `highly_active_sec`, `active_sec`

**Derived**:
- `effective_exertion_min` = max(`total_activity_min`,
  `vigorous_min_uds` + 0.5 × `moderate_min_uds`). Single scalar
  combining recorded and passive views (the 0.5 weight on moderate
  is a fixed choice — moderate-intensity minutes count as half a
  vigorous minute when no recorded activity exists).

**Z-scores against 30-day trailing baseline** (all use robust
median + 1.4826 × MAD; days with < 20 valid prior days get empty
z-score):
- `step_z_30d`: z-score of `total_steps`.
- `effective_exertion_z_30d`: z-score of `effective_exertion_min`.
- `max_hr_z_30d`: z-score of `max_hr_uds`.
- `vigorous_min_z_30d`: z-score of `vigorous_min_uds`.

The z-score approach is PEM-pacing principled: every person has
their own baseline, and PEM is induced by deviation from that
baseline (a "shock") or sustained elevation (push-crash). Absolute
thresholds bake in athletic norms that don't generalise. Logged
in [feedback memory](../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_relative_not_absolute.md).

**Single-day shock indicators**:
- `step_spike` (boolean): `True` iff `step_z_30d ≥ 1.5` and
  `total_steps ≥ 4000` (absolute floor to suppress spurious
  spikes from very-low baseline). The 4000 floor is a noise gate,
  not a classification threshold.

**Push-burden indicators (sustained-elevation detection)**:
- `push_burden_7d`: rolling 7-day sum of `max(0,
  effective_exertion_z_30d)` over `[d−6, d]` (inclusive of day d).
  Captures cumulative push pressure — a single big day plus six
  rest days has the same `push_burden_7d` as seven moderate-push
  days, both signalling sustained envelope pressure.
- `above_baseline_streak`: count of consecutive prior days where
  `effective_exertion_z_30d ≥ 0`. Resets to 0 on the first
  below-baseline day. Captures "how many days have you been
  pushing".

The original 2026-06-06 draft included a derived
`activity_induced_spike_candidate` column using
`max_avgHr ≥ 130 AND total_activity_min ≥ 30`. Empirical
inspection showed the rule fires on **0 of 1,373** days in the
analysis window — the participant essentially stopped doing
high-HR recorded activity after the 2022-05 LC diagnosis (walking
median avg_hr ~98, max 129). The rule was inherited from
generic-athlete framing (§1.1's exact failure mode) and was
removed. Downstream tests that need an activity-induced filter
should combine `n_activities`, `total_activity_min`, and
`vigorous_min_uds` to define their own criteria scoped to the
PEM-envelope context.

**Exertion class** (added in step 04 after cutoffs locked):
- `exertion_class` ∈ {none, light, moderate, heavy, very_heavy}

### 3.4 Step-spike rule — LOCKED

- **z-score basis**: 30-day rolling, median + MAD (robust to
  outliers, e.g. one sick day with 200 steps doesn't crater the
  baseline).
- **Threshold**: z ≥ 1.5 (corresponds roughly to top ~7% of days
  vs participant's own recent baseline).
- **Absolute floor**: `total_steps ≥ 4000` (avoids "spike from
  near-zero baseline" artefacts on post-crash recovery days).
- **Boundary**: days with < 20 valid prior days excluded from
  `step_spike` (`None` value; empty in CSV). This affects the first
  ~30 days of the corpus only.

These rules are locked. Calibration of `exertion_class` cutoffs
proceeds separately (§5).

## 4. Calibration discipline

The severity cutoffs for `exertion_class` are NOT locked in this
spec. They are locked after a blinded distribution review:

1. **Step 1 — extract** features (scripts 01–03) and produce
   `activity_features_daily.csv`.
2. **Step 2 — review distributions** of each relevant feature
   (`vigorous_min`, `aerobicTE`, `effective_exertion_min`,
   `total_steps`, `step_z_30d`, time-in-zone-4-plus) across the
   ~1,373 days in the analysis window. Identify percentile
   breakpoints, natural clusters, sanity-check the maxima.
3. **Step 3 — propose cutoffs** for the five exertion classes
   based on distribution shape only. The proposal is recorded in
   `spec/severity_spec.md` along with the calibration evidence.
4. **Step 4 — lock cutoffs** in `spec/severity_spec.md` before
   any cross-tabulation with crash/dip/cluster labels.
5. **Step 5 — apply** cutoffs (script 04) to emit
   `exertion_class`. Visualise (script 05) on the crash_v2
   timeline.

The blinding is procedural: the distribution review and cutoff
proposal explicitly avoid loading `labels_crash_v2.csv` or any
gevoelscore-derived label. The downstream test step is then a
fair held-out evaluation.

## 5. Downstream tests (pre-registered separately, not in this
spec)

After exertion class is locked, the following hypotheses become
testable. Each will get its own pre-registration file:

- **HA01 — heavy/very-heavy exertion on day −1 predicts crash
  within 72 h**. Frequency, discrimination vs null, magnitude.
- **HA02 — step spike on day −1 to −3 predicts crash**. Sharper
  variant if HA01 is null because most exertion is "moderate".
- **HA03 — re-run H02b specificity check with
  `activity_induced_spike_candidate`** to properly attribute the
  15 H02b false positives originally tagged activity-induced.
- **HA04 — heavy exertion in week before dip clusters**. Tests
  whether rough patches are exertion-precipitated.
- **HA05 — exertion-stress interaction**: do exertion-induced
  spikes (HA03 candidates) precede crashes at the same rate as
  non-exertion-induced spikes?

These tests await the cutoffs lock.

## 6. Output artefacts

Consumable by downstream analyses:

- `output/daily_uds.csv` — 1,800+ days, raw UDS pulled to flat
  CSV (reusable for non-activity work; e.g. RHR re-checks).
- `output/activities.csv` — 404 activities, raw per-event detail.
- `output/activity_features_daily.csv` — the primary table.
  ~1,373 rows over the gevoelscore window.
- `output/distributions.html` — distribution diagnostics
  supporting the cutoff calibration.
- `output/timeline_with_activity.png` — crash_v2 timeline with
  exertion class overlay.
- `spec/severity_spec.md` — locked cutoffs + calibration evidence.

## 7. Caveats

- **Garmin's activity-detection algorithm is opaque and has
  evolved across firmware versions** (7.x → 10.4 on FR245).
  Vigorous-minutes detection sensitivity may have shifted across
  the 5-year window. Stabilisation-arc analyses should
  cross-reference with S01.
- **Self-reported fields cover only 20% of activities**. Their
  meaning is not standardised across the participant's logging
  practice. Use as sanity check, not primary classifier.
- **Step counts on full-rest days** (crash days) can be very low
  (< 500). The `step_z_30d` will be highly negative; we do not
  treat this as a signal per se — the absence of activity on a
  crash day is partly definitional and partly a recovery response.
- **`incident_detected` activity** type (1 record) is a fall-
  detection event, not exertion. Excluded from
  `total_activity_min` and intensity aggregates but kept in
  `activities.csv` for completeness.
- **Breathwork activities** have zero `movingDuration` and very
  low HR impact. Counted as activities (n_activities) but their
  duration is included in `total_activity_min`. May warrant
  exclusion downstream if breathwork is being used as a recovery
  intervention rather than an exertion event — flagged for review
  but not pre-resolved here.
- **`activity-labels` is locked at this revision**. Any change
  to feature definitions or step-spike rule (§3.4) creates
  `activity-labels-v2` and downstream analyses re-run from scratch.

---

*Pre-registration locked 2026-06-06. Next: scripts 01–03 run to
emit feature tables, then distribution review for cutoff
calibration.*
