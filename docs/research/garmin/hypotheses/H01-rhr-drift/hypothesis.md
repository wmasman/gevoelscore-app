# H01 — Resting heart rate drift before crashes

**Pre-registration written 2026-06-05, before any data was inspected
for this test.** Locked. Any subsequent change creates an H01b, not an
edit to this file. The point of pre-registration is that we cannot
adjust the criterion after seeing the result.

## 1. Claim

In the 7 days before a `crash_v1` episode (per [registry §2](../registry.md)),
this user's daily resting heart rate is consistently elevated above their
own rolling 90-day baseline. The elevation pattern is *discriminative* —
meaning it appears more often before crash episodes than in
randomly-sampled non-crash 7-day windows from the same period.

## 2. Why we think this

- The Workwell Foundation's "resting HR + 15 bpm" rule for ME/CFS and
  Long COVID pacing is the most established lay-friendly indicator; it
  rests on the observation that the autonomic nervous system runs hot
  for days before and during PEM episodes.
- The 2025 wearable HRV study cited in
  [pais-pem-literature-review](../../../pais-pem-literature-review.md)
  found HRV depression lasting ~24h after crossing VT1; RHR is the
  cheap-and-public twin signal.
- This user's monitoring_b coverage is 98.8% across the analysis
  window (see [README](../../README.md)), so missing-data attrition
  should be manageable.

## 3. Data sources

- **Crash labels**: `day_entries.date` + `day_entries.score` from the
  project Directus instance. Crash episodes derived per `crash_v1` in
  [registry §2](../registry.md).
- **RHR per day**: field `restingHeartRate` from
  `DI_CONNECT/DI-Connect-Aggregator/UDSFile_*.json`. (Garmin's published
  daily value, typically derived from the lowest sustained 30-minute HR
  window. We deliberately do *not* use `currentDayRestingHeartRate`,
  which is the same day's snapshot rather than the smoothed value the
  pacing literature references.)
- **Analysis window**: 2022-09-03 → 2026-06-05 (post-gevoelscore
  overlap, per [project_timeline_anchors](../../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/project_timeline_anchors.md)).
- **Train / validate split**: train 2022-09-03 → 2023-12-31 (14 crash_v1
  episodes); validate 2024-01-01 → 2026-06-05 (15 episodes). Revised
  2026-06-05 after preflight surfaced a recovery cliff — see
  [registry §1](../registry.md) for rationale.

## 4. Measurement protocol

For each crash episode dated `D` (first day of the episode):

1. **Lead-up window** = `[D − 7, D − 1]` (7 days, exclusive of D itself).
2. **Baseline window** = `[D − 97, D − 8]` (90 days ending 7 days before
   the episode, so the baseline is not contaminated by the lead-up).
3. **Baseline RHR** = trimmed mean (drop top and bottom 10%) of the
   `restingHeartRate` values within the baseline window.
4. **Lead-up RHR** = simple mean of the `restingHeartRate` values within
   the lead-up window.
5. **`delta_rhr` for this episode** = lead-up RHR − baseline RHR (bpm).

For the discriminative comparison, also compute the same `delta_rhr` for
a matched **null sample**:

6. **Null sample** = 200 randomly-selected 7-day windows from the same
   analysis window, each with the same baseline-window construction,
   each disjoint from any crash episode's lead-up window. Random seed
   fixed (`20260605`) so the sample is reproducible.

## 5. Pre-registered falsification criterion

The hypothesis is **supported** if and only if **all three** hold in
**both** the train window and the validate window independently:

a. **Frequency**: at least **60%** of crash episodes have
   `delta_rhr ≥ 3 bpm`.

b. **Discrimination**: the crash-episode frequency from (a) is at least
   **15 percentage points higher** than the null-sample frequency of
   windows with `delta_rhr ≥ 3 bpm`. (Without this, we'd just be
   measuring that RHR fluctuates by 3 bpm sometimes.)

c. **Magnitude**: the median `delta_rhr` across crash episodes is at
   least **+2 bpm**, and the lower quartile is at least **0 bpm** (i.e.
   most lead-ups show some elevation, not just a few extreme ones).

Any one of (a), (b), (c) failing in either window → **refuted**.

If we have fewer than 10 crash episodes per train/validate window after
exclusions (§6), the result is **inconclusive**, not refuted.

## 6. Exclusion rules

- **Episode requires ≥ 6 valid RHR days out of 7** in the lead-up
  window. Otherwise the episode is excluded and reported as "excluded
  for missing data" in the result.
- **Episode requires ≥ 30 valid RHR days out of 90** in the baseline
  window. Same handling.
- **Episodes whose 7-day lead-up overlaps another crash episode's days**
  are excluded from the primary analysis (contaminated lead-up). These
  are reported separately as "back-to-back episodes" in the result and
  may be analysed in a follow-up.
- **First episodes near the analysis-window start** (where the
  90-day baseline window extends before 2022-09-03 Garmin coverage start)
  use whatever baseline days are available, subject to the ≥30 valid
  days rule. Note: Garmin coverage actually starts 2021-08, so the
  baseline is not constrained by Garmin gaps — it's only constrained by
  the gevoelscore window start of 2022-09-03 in the sense that we
  cannot have crash labels earlier. Baseline RHR may use pre-2022-09
  RHR data; this is harmless because the baseline is a physiological
  reference, not a labelled comparison.

## 7. Expected effect size if the hypothesis is true

Rough, for sanity-checking the result:

- 70–80% of crash episodes show `delta_rhr ≥ 3 bpm`
- Null-sample rate: 30–40% (RHR fluctuates naturally; some random
  windows will exceed the threshold)
- Median `delta_rhr` across crashes: roughly +4 to +6 bpm
- If we see crash rate of 95% and null rate of 90%, something is wrong
  (probably a baseline bug) and result.md should flag it before
  declaring support.

## 8. Caveats `result.md` must explicitly acknowledge

Whether the result is supported, refuted, or inconclusive:

- **Chronotropic incompetence** affects most ME/CFS patients — HR
  responses may be blunted. If RHR doesn't lead, the absence may reflect
  *this person's* physiology rather than disproving the broader theory.
- **Seasonality**: RHR varies with ambient temperature, training load,
  and acute illness. None of these is controlled for.
- **Score scale drift**: if the user's interpretation of the score
  changed over 3.7 years, the "personal bottom 15%" definition may
  capture different physiological states in 2022 vs 2026. This is a
  known limitation of `crash_v1` itself, not specific to H01.
- **Multiple-comparisons**: H01 is one of five hypotheses tested. With
  pre-registered criteria and held-out validation, the protection is
  decent but not perfect.
- **Reverse causation is unlikely here** (a crash on day D cannot
  retrocausally elevate RHR on day D−5), but a *shared cause*
  (e.g. a developing infection) elevates both RHR and crash risk and
  would look identical. The analysis cannot distinguish "RHR predicts
  crash" from "early infection produces both" — `result.md` must say so.

## 9. What we do with each outcome

- **Supported in both windows** → write `card.md` with 2–3 candidate
  card-text variants using real numbers from this user's data and (where
  present) real quoted phrases from the user's notes on those crash
  days. Proceed to H02.
- **Refuted** → write `result.md` documenting *exactly why* it failed
  (which of a/b/c, in which window, by how much). Do not re-run with
  tweaked criteria — that would defeat pre-registration. If the failure
  shape suggests a different hypothesis worth testing (e.g. RHR rises
  on the day-of, not in lead-up), that becomes H01b with its own
  hypothesis.md. Proceed to H02 unchanged.
- **Inconclusive (too few episodes)** → write `result.md` with the
  episode count and reason. This is real information: it tells us
  `crash_v1` is underpowered, and may push us to develop `crash_v2`
  (notes-based labels) earlier than planned.

---

*Pre-registration locked 2026-06-05. Next: write `test.py`.*
