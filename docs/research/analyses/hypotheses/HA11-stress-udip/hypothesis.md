# HA11 — Within-day stress U-dip events as crash precursor (orthostatic / electrolyte signature)

**Pre-registration written 2026-06-07, before any per-minute U-dip
data was inspected for this test.** Locked. Any subsequent change
creates an HA11b.

HA11 tests Wiggers' lived-experience within-day pattern: per-minute
stress drops sharply (the "U") and then plateaus at a
**higher-than-pre-dip** baseline. Wiggers reports resolving this
pattern with ORS / electrolytes; the physiological hypothesis is
orthostatic / low-blood-volume dysregulation — when blood volume is
inadequate, momentary postural changes trigger a brief vagal-tone
moment (low stress reading on Garmin's HRV-derived scale) followed
by sympathetic compensation that holds blood pressure but reads as
*higher* sustained stress.

HA11 is the **first within-day pattern test in the project** (all
prior precursor tests have used day-level metrics). The data
primitive is per-minute stress samples already validated by H02b /
H02d.

## 1. Claim

In the **4 days** before a `crash_v1` episode (primary) and the
**5 days** before a `crash_v1` episode (secondary), at least one
day's count of within-day U-dip events deviates from its lagged
personal baseline by **(u_dip_count − μ) / σ ≥ N_std** (N_std
locked below; one-sided ELEVATED direction). The crash-episode
frequency of this deviation is discriminative against
randomly-sampled non-crash windows in **both train and validate
windows independently**.

A bidirectional sensitivity arm reports the |z| ≥ N_std result.
The primary direction is one-sided elevated (more U-dips = more
orthostatic events = pre-crash precursor) per Wiggers' framing.

Secondary descriptive outcome: same-day correlation between U-dip
events and gevoelscore. Report as descriptive only; no SUPPORTED
bar.

## 2. Why we think this

- **Wiggers documents the U-dip pattern qualitatively in detail**
  in *Smartwatch Pacing* (2025-07). She reports resolving it with
  ORS / electrolytes, suggesting the mechanism is
  orthostatic / blood-volume-related rather than purely autonomic.
- **Three train-era SUPPORTED autonomic-deviation precursors on
  three channels** (H02b stress spike count, H02d sentinel-corrected
  spike, HA06b RHR z-score) and **HA10 validate-era SUPPORTED on
  morning BB peak** all indicate the participant's crashes have
  population-level physiological precursor signatures. A within-day
  pattern is the obvious complementary axis to test, and HA11's
  mechanism (orthostatic) is independent of the autonomic-deviation
  patterns already characterised.
- **HA10's validate-era SUPPORTED finding** is the project's first
  validate-era precursor; HA11 tests a different mechanism (postural
  / orthostatic) that may also be a validate-era precursor and may
  even be a *partial physiological explanation* for HA10's pattern
  (orthostatic events → sympathetic compensation → night's BB peak
  shifts higher).
- **The participant has soak-tested ORS in the past** (see
  `project_recovery_trajectory` memory). If U-dip events are
  detected, cross-referencing with notes for ORS / electrolyte
  mentions could provide first-person corroboration.
- **The per-minute stress data is already validated** by H02b and
  H02d. The U-dip detection is a new within-day pattern recognition
  task on the same input data, no new extraction is needed beyond
  re-parsing the monitoring_b FIT files to keep per-minute samples
  (vs H02b's daily-max-spike summary).

## 3. Data sources

- **Crash labels**: `crash_v1` from
  [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv).
- **Per-minute stress**: extracted from `monitoring_b` FIT files in
  the GDPR dump's `DI-Connect-Uploaded-Files/UploadedFiles_*.zip`
  archives. Sample cadence ~60 seconds. Filter: drop values outside
  [1, 100] (sentinels) per H02b's locked convention.
- **Analysis window + train/validate split**: same as HA06b / HA10
  (train 2022-09-03 → 2023-12-31, 14 episodes; validate 2024-01-01
  → 2026-06-05, 15 episodes).

## 4. Measurement protocol

### 4.1 Per-minute stress samples

Same as H02b's extraction:
- Parse monitoring_b FIT files for `stress_level` records.
- Drop values outside [1, 100].
- Aggregate by date (Garmin's calendar-day boundary).

### 4.2 U-dip event definition (locked)

A U-dip event at timestamp `t` requires three valid windows:

| window | duration | offset from t | content |
|---|---:|---|---|
| `pre_dip` | 30 min | [t − 35, t − 5] | the baseline period before the dip |
| `dip` | 15 min | [t − 7, t + 7] | the sharp drop period |
| `post_dip` | 30 min | [t + 8, t + 38] | the plateau period after the dip |

Validity per window: at least **70%** of expected samples (21 of 30
for pre/post, 11 of 15 for dip) must be present and inside [1, 100].

Per-window aggregates:
- `S_pre` = mean(pre_dip valid samples)
- `S_floor` = minimum(dip valid samples)
- `S_post` = mean(post_dip valid samples)

A U-dip event triggers when all three conditions hold:
- **(1) Meaningful pre-dip baseline**: `S_pre ≥ 40` (moderate stress
  baseline; not just a flat-low resting period).
- **(2) Sharp drop**: `S_floor ≤ S_pre − 25` (≥ 25-point drop from
  baseline to floor).
- **(3) Higher plateau**: `S_post ≥ S_pre + 5` (post-dip plateau is
  ≥ 5 points higher than pre-dip baseline).

### 4.3 U-dip count per day

To avoid double-counting one slow trajectory, a sliding-window
detection rule:

- Scan each timestamp `t` in the day's per-minute sample sequence
  (at minute resolution).
- When a U-dip event triggers, record `t` and **skip the next 60
  minutes** before evaluating the next candidate. This ensures
  consecutive U-dips are at least 60 minutes apart.

`u_dip_count[d]` = count of distinct U-dip events on calendar day d.

### 4.4 Day validity

A day is **valid for HA11** if it has at least **600 valid
per-minute stress samples** (i.e. ≥ 10 hours of coverage). Days
with fewer samples are flagged *insufficient-coverage* and skipped
in the test. Report fraction of such days.

### 4.5 Lagged personal baseline (per Theme A)

For each valid day `d`:

- Baseline window: days in `[d-90, d-30]` (60-day window).
- **Baseline mean (μ)**: trimmed mean (10/90 cut) of `u_dip_count`
  values across the prior days that are themselves valid.
- **Baseline std (σ)**: stdev of the same trimmed values.
- Computed only when ≥ 40 of 60 prior days are valid.
- If σ ≤ 0.5 events — i.e. the baseline is essentially flat (most
  days have the same count, typically 0) — flag the day as
  *low-variability* and skip it in the test. Report fraction.

### 4.6 Per-day z-scored U-dip count

For each valid day `d` with both `u_dip_count` and a defined
(μ, σ) pair:

- `delta(d) = u_dip_count(d) − μ(d)`
- `z(d) = delta(d) / σ(d)`
- `|z(d)| = abs(z(d))`

### 4.7 Per-episode lead-up profile

Same structure as HA06b / HA10:
- 4-day primary lead-up: [C-4, C-3, C-2, C-1]
- 5-day secondary lead-up: [C-5, C-4, C-3, C-2, C-1]
- Min valid days: 3 of 4 for primary; 4 of 5 for secondary
- Episode trigger flag (one-sided elevated, primary):
  `max_signed_z ≥ N_std`
- Bidirectional sensitivity arm: `max |z| ≥ N_std`
- Record direction of max-|z| day and all signed z values.

### 4.8 Threshold N_std

Three pre-registered thresholds, consistent with HA06b / HA10:

| Tier | N_std | Anchor |
|---|---:|---|
| Primary | **1.5** | mild-to-moderate deviation |
| Secondary | **2.0** | classical outlier threshold |
| Sensitivity check | **2.5** | strict |

The **primary tier (N_std = 1.5) determines the headline verdict**;
secondary and sensitivity check are reported alongside.

### 4.9 Null sample

200 random non-overlapping reference dates, same construction +
seed (`20260605`) as HA06b / HA10. Per-window null trigger flag
computed exactly as in §4.7. Only days satisfying §4.4 validity are
eligible as reference dates.

### 4.10 Secondary descriptive outcome — same-day correlation

For each calendar day d with both `u_dip_count[d]` and
`gevoelscore[d]` defined, report:
- Median `u_dip_count` by gevoelscore value.
- Spearman correlation `u_dip_count` vs `gevoelscore`.
- Report split by era (train vs validate).

This is descriptive only. No SUPPORTED bar; no
verdict-determining role.

## 5. Pre-registered falsification criterion

Identical three-criterion bar shape to H02b / HA01b / HA06b / H02d
/ HA10:

**(a) Frequency**: at least **60%** of crash episodes have
`max signed_z ≥ N_std` (one-sided primary) in their lead-up window.

**(b) Discrimination**: the crash-episode frequency from (a) is at
least **15 percentage points higher** than the null-sample
frequency.

**(c) Magnitude**: the median `max signed_z` across crash episodes
is at least **N_std / 2** (0.75 / 1.0 / 1.25 for N_std = 1.5 / 2.0
/ 2.5 respectively).

Any one of (a), (b), (c) failing in either train or validate of
the primary tier (N_std = 1.5) → **refuted**.

If we have fewer than 10 clean crash episodes per window after
exclusions → **inconclusive**.

## 6. Exclusion rules

- Days with fewer than 600 valid per-minute stress samples are
  excluded (insufficient coverage).
- Days where the U-dip baseline σ ≤ 0.5 events are flagged
  *low-variability* and excluded.
- Days where fewer than 40 of 60 prior valid days are available
  are excluded (insufficient baseline).

## 7. Expected effect size if hypothesis is true

- 60-80% of crash episodes have `max signed_z ≥ 1.5` in the 4-day
  lead-up.
- Null sample rate: 7-20% (one-sided Gaussian tail expectation
  ~6.7% per day; max over 4 days inflates this).
- Median `max signed_z`: 1.5-2.5.
- **Sanity check on baseline U-dip rate**: if U-dip events fire on
  ≥ 50% of days (i.e. the spec is too loose) or on < 5% of days
  (i.e. too strict for σ to be meaningful), flag for design review.
  Pre-committed acceptable range: U-dip event rate per valid day
  should fall in [0.1, 5.0] events/day across the corpus.
- **Sanity check on σ**: if median baseline σ is < 0.5 events
  → spec is too strict (low-variability flag will catch most days).
  If median σ is > 3.0 events → spec is too loose (one-day
  fluctuation drowns the signal).

If either sanity check fails on the dry-run, the spec needs review
BEFORE running the full test. The dry-run is the gate.

## 8. Caveats `result.md` must explicitly acknowledge

- **U-dip detection is novel** for this project. Even with locked
  pre-registration, the absolute event rate is sensitive to the
  thresholds (S_pre ≥ 40, drop ≥ 25, plateau ≥ +5). A different
  choice could produce a different U-dip count. The pre-registered
  thresholds are physiologically motivated (S_pre 40 = moderate
  baseline; drop 25 = clearly visible on Garmin's 0-100 scale;
  plateau +5 = a meaningful step above baseline) but not validated
  against ground truth (e.g. orthostatic challenge tests).
- **No first-person corroboration baseline**. Wiggers documents
  her own U-dips with notes ("ORS hielp"), but this participant's
  notes have not been mined for orthostatic / electrolyte mentions.
  The secondary descriptive outcome's gevoelscore correlation is
  the best within-this-project corroboration available.
- **Watch-off coverage**: the day validity rule (≥ 600 samples)
  excludes ~10-15% of days based on H02b's coverage.
- **Garmin's stress algorithm uses HRV as input**; the stress
  signal is HRV-derived. U-dip events therefore are
  fundamentally HRV-shape events, not pure orthostatic signals.
  Garmin does NOT compute orthostatic-specific patterns. The U-dip
  pattern is a proxy that *correlates with* Wiggers' description,
  not a direct orthostatic measurement.
- **`crash_v1` mixes mechanisms**. Same caveat as all prior tests.
- **Multi-comparison**. HA11 is the 15th pre-registered hypothesis
  in the H##/HA## series. The held-out validate window is the
  primary defence.
- **Era considerations**: the participant's stress baseline shifted
  between eras (S01 trajectories: average stress dropped from ~35
  pre-cliff to ~29 mid-2025 then rose to ~33.7 in May 2026). A
  fixed `S_pre ≥ 40` threshold may produce fewer events in the
  low-baseline middle period and more events in 2022-23 / May 2026.
  The lagged baseline partially compensates by z-scoring relative
  to the same period.

## 9. What we do with each outcome

- **Supported in both windows** (primary 4d, both train + validate)
  → **second project-level SUPPORTED-in-both finding** (HA10
  validate stands alone; no test has SUPPORTED both eras yet under
  clean methodology). Confirms a within-day orthostatic precursor
  is a real predictor on top of the autonomic-deviation patterns.
  Then `card.md`: a U-dip-event-aware retrospective card concept.
- **Train supported, validate refuted** → fourth train-era
  SUPPORTED finding on a different channel (within-day vs across-
  day). The pre-cliff multi-channel autonomic + orthostatic
  signature gets stronger. Validate-era still has only HA10's BB
  signal.
- **Train refuted, validate supported** → second validate-era
  SUPPORTED finding (after HA10). The orthostatic mechanism may be
  more characteristic of the residual era than the pre-cliff era,
  consistent with stabilisation reducing sympathetic-overarousal
  patterns but not addressing underlying orthostatic / blood-volume
  issues. **Notable because it would imply the validate-era crashes
  have TWO independent precursor channels (BB recharge + U-dip
  count) where the train era only has one (BB recharge in the
  Wiggers direction at 5d).**
- **Refuted in both windows** → within-day U-dip count does NOT
  carry crash-precursor signal at the population level for this
  participant. Wiggers' qualitative pattern may still be
  experientially real, but does not show up as an aggregable
  precursor signature. ORS / electrolyte intervention's relevance
  becomes a per-event question (HA11b on dip-cluster days,
  perhaps), not a daily-pattern question.
- **Primary refutes but bidirectional sensitivity arm differs**
  → report honestly; do not redefine the headline verdict on the
  sensitivity arm's result. Document for HA11b consideration on
  truly new data.
- **Spec sanity-check fails on dry-run** (U-dip rate outside
  [0.1, 5.0] events/day, or median σ outside [0.5, 3.0]) → DO NOT
  run the full test. Document the failure in the dry-run report
  and revise the spec (creating HA11-revised with audit trail).

## 10. Detection script architecture

The extraction is computationally heavier than HA06b / HA10
(per-minute samples for ~1700 days). Two-stage design to minimise
re-work:

1. **Stage 1** (`extract_udip_counts.py`): parse all monitoring_b
   FIT files, build per-minute stress sequences per date, detect
   U-dip events per the locked §4.2 definition, emit
   `udip_counts.csv` with schema
   `date, sample_count, u_dip_count, valid` (valid = 1 if
   sample_count ≥ 600).
2. **Stage 2** (`test.py`): load udip_counts.csv, compute lagged
   baselines, run the precursor test per the same null-seed +
   windowing machinery as HA06 / HA06b / HA10.

The Stage 1 extraction is cached on first run; Stage 2 re-runs in
seconds.

`--dry-run` mode in test.py prints first-3-episodes per era to
confirm the spec is producing sane values before the full
evaluation runs.

---

*Pre-registration locked 2026-06-07. Same test-script pattern as
HA10 with U-dip-count loading replacing morning-peak loading. Same
`--dry-run` mode; same null seed (`20260605`); same lagged baseline
machinery.*
