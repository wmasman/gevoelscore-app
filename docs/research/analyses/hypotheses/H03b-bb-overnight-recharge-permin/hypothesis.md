# H03b — Overnight Body Battery recharge (per-minute, z-score) as crash precursor

**Pre-registration written 2026-06-07, before any per-minute BB
data has been pulled.** Locked. Any subsequent change creates an
H03c.

H03b replaces the original H03 (sleep efficiency, refuted
decisively) and supersedes the planned "sharper sleep metrics"
follow-up. It tests a physiologically targeted version of
"unrefreshing sleep": the actual amount of Body Battery recovered
overnight, computed from per-minute samples.

H03b is also the **sharpening test for HA10's validate-era SUPPORTED
finding**. HA10 found that elevated morning BB peak z-score
(paradoxical "swing" direction) is a validate-era precursor at
+16.2 pp discrimination / 86.7% frequency at 4d primary
bidirectional. H03b tests whether the per-minute *trajectory* (the
*integral* of overnight recharge, not just the peak value) carries
even sharper signal than HA10's coarse 3-anchor proxy.

**Computability gate: H04b path C authorisation must complete first**
(unlocks the Garmin Connect REST API endpoint
`/wellness-service/wellness/bodyBattery/events/{date}`).

## 1. Claim

In the **4 days** before a `crash_v1` episode (primary) and the
**5 days** before a `crash_v1` episode (secondary), at least one
night's overnight BB recharge deviates from its lagged personal
baseline by **|overnight_recharge − μ| / σ ≥ N_std** (N_std locked
below). The crash-episode frequency of this deviation is
discriminative against randomly-sampled non-crash windows in **both
train and validate windows independently**.

**Bidirectional primary** (matching HA10's locked design after
HA10's directionality reversal between eras was discovered): the
Wiggers / Bateman Horne canonical direction is lowered overnight
recharge (= incomplete recovery), but HA10 documented validate-era
crashes show the *paradoxical elevated* direction (= "looked like
a great recovery but"). Bidirectional captures both. One-sided
lowered + one-sided elevated reported as sensitivity arms.

## 2. Why we think this

- **HA10 validate-era SUPPORTED at coarse resolution.** Morning BB
  peak z-score at 4d primary bidirectional supports validate at
  +16.2 pp (86.7% freq, 69% elevated-direction triggering). The
  per-minute version SHOULD sharpen this signal — the trajectory
  carries information the peak alone does not. If H03b validate
  supports at higher discrimination than HA10's +16.2 pp, the
  per-minute version is the right operationalisation. If it
  doesn't, HA10's peak-only metric was already sufficient.
- **Bateman Horne Center's "back to baseline next morning?"**
  heuristic is the strongest external evidence for overnight
  recovery as a precursor channel. The integral of recharge (peak
  − sleep-onset) is the most direct operationalisation of "back
  to baseline."
- **Workwell's framework**: overnight recharge depression is one of
  the two primary mechanisms in their pacing model (the other is
  sympathetic overarousal, which we've tested via H02b / H02d /
  HA06b / HA11 in train).
- **Four train-era SUPPORTED autonomic precursors on four channels
  exist** (H02b, H02d, HA06b, HA11); HA10's 5d secondary one-sided
  lowered SUPPORTED at +18.3 pp adds a fifth train-arm finding.
  H03b train should SUPPORT in the canonical lowered direction at
  some window if the pattern is real.
- **HA10's directionality reversal between eras** (train 100%
  lowered → validate 69% elevated) should reproduce on the
  per-minute version. Bidirectional primary respects this; the
  one-sided arms test the direction-specific hypotheses.

## 3. Data sources

- **Crash labels**: `crash_v1` from
  [`crash_v2-definition/labels_crash_v2.csv`](../crash_v2-definition/labels_crash_v2.csv).
- **Per-minute Body Battery**: Garmin Connect REST API endpoint
  `/wellness-service/wellness/bodyBattery/events/{date}` via
  `cyberjunky/python-garminconnect`. Authorisation: H04b path C
  (ToS-grey, user-accepted for personal-use, own-data analysis).
  Stored at `C:\Users\Gebruiker\Documents\gevoelscore-data\garmin
  data\api_pull\bb_per_minute\` as CSV-per-month.
- **Sleep window** (to identify "sleep onset" and "morning wake"):
  from existing `*_sleepData.json` files
  (`sleepStartTimestampGMT` and `sleepEndTimestampGMT`).
- **Analysis window + train/validate split**: same as HA06b / HA10 /
  HA11.

## 4. Measurement protocol

### 4.1 Per-night overnight recharge

For each calendar day `d`:

1. **Identify the sleep window**: from sleepData for date d, take
   `sleepStartTimestampGMT` (sleep onset) and `sleepEndTimestampGMT`
   (wake). If sleep data is missing for d, the night is skipped.
2. **Identify the BB sleep-onset value**: per-minute BB value at
   the timestamp closest to sleep_onset (within ±10 min). If no
   sample within window, skipped.
3. **Identify the BB peak during sleep**: max per-minute BB value
   in the interval [sleep_onset − 30 min, sleep_end + 30 min]. The
   30-min padding catches the actual peak which may occur slightly
   after wake. If no samples in interval, skipped.
4. **Compute**: `overnight_recharge[d] = peak_during_sleep − sleep_onset_value`.
   Range: typically [0, 100]; negative values flagged as
   pathological (peak before sleep_onset → sample alignment bug
   or pre-bedtime nap; excluded with count reported).

### 4.2 Validity rules

A night is **valid for H03b** if:
- Sleep window is identified (from sleepData) AND
- ≥ 30 valid per-minute BB samples in the sleep window AND
- `overnight_recharge[d]` is in [0, 100].

Days with fewer samples are flagged *insufficient-coverage* and
skipped. Report fraction.

### 4.3 Lagged personal baseline (per Theme A)

For each valid day `d`:
- Baseline window: days in `[d-90, d-30]` (60-day window).
- Trimmed mean (10/90 cut) μ; stdev σ over the same trimmed values.
- Computed only when ≥ 40 of 60 prior days are valid.
- If σ ≤ 3.0 BB points (baseline is essentially flat), flag the
  day as *low-variability* and skip. Report fraction.

### 4.4 Per-day z-scored recharge

For each valid day `d` with both `overnight_recharge[d]` and a
defined (μ, σ) pair:
- `delta(d) = overnight_recharge(d) − μ(d)` (signed)
- `z(d) = delta(d) / σ(d)` (signed)
- `|z(d)| = abs(z(d))` (unsigned)

### 4.5 Per-episode lead-up profile

Same as HA10:
- 4-day primary lead-up: [C-4, C-3, C-2, C-1].
- 5-day secondary lead-up: [C-5, C-4, C-3, C-2, C-1].
- Min valid days: 3 of 4 for primary; 4 of 5 for secondary.
- Episode trigger flag (bidirectional, primary): `max |z| ≥ N_std`.
- Sensitivity arms: one-sided lowered, one-sided elevated.
- Record directionality split.

### 4.6 Threshold N_std

Three pre-registered thresholds, consistent with HA06b / HA10 /
HA11:

| Tier | N_std | Anchor |
|---|---:|---|
| Primary | **1.5** | mild-to-moderate deviation |
| Secondary | **2.0** | classical outlier threshold |
| Sensitivity check | **2.5** | strict |

### 4.7 Null sample

200 random non-overlapping reference dates, same construction +
seed (`20260605`) as HA10 / HA11. Only valid days eligible.

## 5. Pre-registered falsification criterion

Identical three-criterion bar shape to HA10:

**(a) Frequency**: at least **60%** of crash episodes have
`max |z| ≥ N_std` in their lead-up window.

**(b) Discrimination**: the crash-episode frequency from (a) is at
least **15 percentage points higher** than the null-sample
frequency.

**(c) Magnitude**: the median `max |z|` across crash episodes is at
least **N_std / 2** (0.75 / 1.0 / 1.25 for N_std = 1.5 / 2.0 / 2.5).

Any one of (a), (b), (c) failing in either train or validate of
the primary tier (N_std = 1.5) → **refuted**.

Per-era SUPPORTED status is also reported under the strict bar; an
HA10-style era-specific result is valid (e.g. validate SUPPORTED
but train refuted is interpretable, not a project failure).

If fewer than 10 clean crash episodes per window → **inconclusive**.

## 6. Comparison to HA10 — pre-committed verdict mapping

H03b is explicitly a *sharpening test* of HA10. Pre-commit on the
verdict-mapping:

| H03b result | HA10 comparison | interpretation |
|---|---|---|
| Validate SUPPORTED at ≥ HA10's +16.2 pp | Per-minute sharpens HA10 | H03b becomes the validate-era anchor; card (b2) gets H03b-based framing instead of HA10 |
| Validate SUPPORTED at < HA10's +16.2 pp | Per-minute doesn't help | HA10 stays the validate-era anchor; H03b adds incremental coverage |
| Validate REFUTED | Per-minute LOSES HA10's signal | Investigate why; possible the peak-only metric was capturing something the integral doesn't |
| Train SUPPORTED at lowered (canonical direction) | Adds train-era anchor where HA10 train was refuted at 4d | Train-era retrospective card gains a fifth converging anchor |
| Train SUPPORTED at elevated | Unexpected reversal vs HA10 train | Investigate; possible per-minute reveals a pattern peak-only missed |
| Train REFUTED both directions | HA10 5d lowered SUPPORTED stands as the train BB-channel finding | H03b adds no train-era contribution |

## 7. Expected effect size if hypothesis is true

- Validate-era 4d primary bidirectional: 70-90% trigger rate
  (matching or exceeding HA10's 86.7%).
- Validate-era discrimination ≥ HA10's +16.2 pp.
- Validate-era directionality: predominantly elevated (matching
  HA10's 69% elevated).
- Train-era 5d one-sided lowered: 60-80% trigger rate at +15-25 pp
  disc (matching or exceeding HA10's 5d lowered +18.3 pp / 64.3%).
- Median |z| ≥ 2.0 across crash episodes.

## 8. Caveats `result.md` must explicitly acknowledge

- **Garmin API ToS-grey**. The endpoint is undocumented for personal
  use; data could become inaccessible if Garmin changes the API. The
  cached CSV survives if access is later revoked.
- **Garmin's BB algorithm is opaque**. Firmware changes may have
  shifted internal calibration during the analysis window. The
  lagged baseline partially compensates.
- **HRV is one of BB's inputs** (alongside HR and stress). H03b
  inherits some chronotropic-incompetence sensitivity from HR; less
  so than HA06.
- **Sleep-onset timing approximation**. Garmin's sleepStartTimestamp
  is itself an algorithm output, not a ground-truth measurement of
  when the participant fell asleep. ±10-15 min uncertainty is
  expected.
- **Per-minute samples may have gaps**. Watch-off-overnight produces
  uniform skips. Report sample density per night.
- **Multi-comparison**. H03b is the 16th pre-registered hypothesis
  in the H##/HA## series. Held-out validation discipline applies.

## 9. What we do with each outcome

Per §6 verdict-mapping. Additional global rules:

- **Both eras SUPPORTED in bidirectional with opposite-direction
  patterns** → H03b becomes the strongest single test in the project.
  Replaces or supplements HA10 as the per-channel anchor.
- **Both eras REFUTED** → BB channel is doubly refuted at coarse
  AND sharp resolution; per-minute didn't help. Card (b2) loses
  its HA10 anchor too. Direction shifts further toward HRV
  (HA07/HA08) and the four-channel train cluster for retrospective
  use.

---

*Pre-registration locked 2026-06-07 before any per-minute BB pull.
Same test-script pattern as HA10 with overnight-integral loading
replacing morning-peak loading. Same `--dry-run` mode; same null
seed (`20260605`); same lagged baseline machinery.*
