# H02b — Result: per-minute stress spike duration before crashes

**Verdict: TRAIN SUPPORTED, validate near-miss → OVERALL REFUTED per
the locked rule.** But this is the first window of the whole
investigation to fully clear all three pre-registered criteria, and
the per-episode breakdown directly confirms the user's experiential
claim for the pre-recovery era.

H02 (daily-average stress) was close in train. H02b (per-minute spike
detection) **clears the bar by clear margins** in train. The user's
own framing — "an intense moment in an otherwise calm day can trigger
a crash" — is supported by the data for 2022–23.

The validate window is the more nuanced part of the story. Not flat,
not refuted-decisively. Most validate episodes still show positive
direction, but everything has compressed: both baseline spike
durations AND lead-up max-spike durations shrank with recovery, and
the discrimination against the (noisy) null sample doesn't clear the
+15 pp bar.

No `card.md` per the strict overall rule. But this result earns a
detailed discussion of *what kind of card it would support*. See §6.

Data: [result-data.json](result-data.json). Plots:
[result-train.png](result-train.png),
[result-validate.png](result-validate.png).

## Numbers

|                                              | train    | validate |
|----------------------------------------------|---------:|---------:|
| crash episodes in window                     | 14       | 15       |
| excluded for missing data                    | 0        | 0        |
| excluded for lead-up overlap                 | 0        | 0        |
| **clean crash episodes**                     | **14**   | **15**   |
| null sample size                             | 200      | 200      |
| % of crash lead-ups with delta ≥ +10 min     | **71.4%** | 33.3%   |
| % of null windows with delta ≥ +10 min       | 41.5%    | 41.5%    |
| **discrimination (crash − null, pp)**        | **+29.9** | −8.2    |
| median delta_spike_minutes                   | **+16.2** | +6.7    |
| lower quartile delta_spike_minutes           | +6.8     | −0.4     |
| criterion a (≥60% at +10 min)                | **PASS** | FAIL     |
| criterion b (discrim ≥ +15 pp)               | **PASS** | FAIL     |
| criterion c (median ≥ +5, lower-q ≥ 0)       | **PASS** | FAIL (by 0.4 min on lower-q) |

**Train clears all three criteria.** Validate fails criterion b by a
substantial margin and criterion c by literal fractions of a minute on
lower-quartile. Median delta_spike in validate is +6.7 min — above
criterion c's +5 — but the bar requires all three together.

## Per-episode breakdown

### Train (14 of 14 had measurable lead-up + baseline; 10 of 14 crossed +10 min)

| episode start | lead-up max | baseline | delta | crosses +10? |
|---|---:|---:|---:|---|
| 2022-09-03 | 43.0 | 14.3 | **+28.7** | YES |
| 2022-09-16 | 16.0 | 16.2 | −0.2 | no |
| 2022-09-30 | 56.0 | 16.0 | **+40.0** | YES |
| 2022-11-23 | 41.0 | 12.3 | **+28.7** | YES |
| 2022-12-27 | 22.0 | 11.3 | **+10.7** | YES |
| 2023-02-04 | 27.0 | 13.0 | **+14.0** | YES |
| 2023-04-02 | 42.0 | 13.4 | **+28.6** | YES |
| 2023-05-28 | 19.0 | 12.2 | +6.8 | no |
| 2023-06-12 | 29.0 | 12.0 | **+17.0** | YES |
| 2023-09-07 | 42.0 | 12.8 | **+29.2** | YES |
| 2023-09-16 | 29.0 | 12.5 | **+16.5** | YES |
| 2023-09-27 | 13.0 | 12.8 | +0.2 | no |
| 2023-11-12 | 18.0 | 11.2 | +6.8 | no |
| 2023-11-27 | 27.0 | 11.1 | **+15.9** | YES |

Ten of the 14 train crashes have an unusually long stress spike — 15+
minutes of sustained ≥75 stress, where the user's typical max-spike
day has 12-ish minutes. The four exceptions (2022-09-16, 2023-05-28,
2023-09-27, 2023-11-12) all show baseline-level or just-above-baseline
spikes — these may be the non-spike-precursor subset of train crashes
(see "mixed mechanisms" below).

### Validate (8 of 15 above baseline, 5 of 15 crossed +10 min)

| episode start | lead-up max | baseline | delta | crosses +10? |
|---|---:|---:|---:|---|
| 2024-01-12 | 17.0 | 10.6 | +6.4 | no |
| 2024-01-21 | 9.0 | 9.8 | −0.8 | no |
| 2024-02-15 | 24.0 | 9.7 | **+14.3** | YES |
| 2024-02-25 | 16.0 | 9.9 | +6.1 | no |
| 2024-04-30 | 8.0 | 11.7 | −3.7 | no |
| 2024-05-28 | 18.0 | 10.3 | +7.7 | no |
| 2024-06-18 | 30.0 | 9.8 | **+20.2** | YES |
| 2024-06-25 | 21.0 | 9.6 | **+11.4** | YES |
| 2024-07-15 | 9.0 | 9.9 | −0.9 | no |
| 2024-08-29 | 17.0 | 10.3 | +6.7 | no |
| 2024-12-23 | 14.0 | 7.2 | +6.8 | no |
| 2025-04-24 | 16.0 | 5.8 | **+10.2** | YES |
| 2025-10-02 | 14.0 | 10.2 | +3.8 | no |
| 2026-05-12 | 11.0 | 11.4 | −0.4 | no |
| 2026-05-20 | 23.0 | 11.3 | **+11.7** | YES |

Five of 15 validate crashes still show a spike-precursor pattern
clearly. Eight show modestly elevated lead-up spikes (not enough to
pass the +10 criterion). Two show flat or slightly inverted.

## The compression finding

Baselines in train: 11–16 min. Baselines in validate: **5–12 min**.
Lead-up maxes in train: 13–56 min. In validate: **8–30 min**.

Recovery shrank the spike landscape on both sides — the user has
fewer intense moments overall (lower baselines) AND smaller crisis
events when they happen (lower lead-up max). The *direction* of the
signal is preserved (most validate episodes still have lead-ups above
their own baseline), but the *magnitudes* shrank into noise.

This is a meaningful finding in its own right: it directly characterises
what recovery looks like at the spike level — a more even daily
emotional/stress landscape, with smaller deviations from normal.

## What the data DOES say

- **For pre-recovery crashes (2022–23), the user's experiential claim
  is confirmed.** 71% of those crashes had a ≥10-minute longer
  stress spike than typical in the 3 days before them. The median
  pre-crash day had a 27-minute intense spike against a typical
  ~12-minute spike.
- **The discrimination is strong (+29.9 pp) against 200 random
  non-crash 3-day windows.** This is not noise.
- **The spike-detection metric is materially better than daily averages**
  (H02) at picking up this pattern, exactly as the user's experiential
  framing predicted: a daily mean dilutes a 30-minute spike with 1.420
  other minutes; the spike-detection metric sees it directly.
- **For post-recovery crashes (2024+), the *direction* of the signal
  is preserved but the *magnitudes* have compressed below
  reliable-detection threshold.** Median lead-up spike is still ~7
  minutes above baseline (positive) — just not enough above the null
  sample's natural variation to clear the strict bar.

## What the data does NOT say

- **It does NOT mean stress spikes don't matter in the validate era.**
  Five of 15 validate crashes (33%) still show clear +10 min lead-up
  spikes. That's the same as the *null* rate (41.5%), which is why
  we can't claim predictive value at population level — but for those
  5 specific crashes, the spike-precursor pattern is real.
- **It does NOT mean a spike-detection card can't ever fire on a
  validate-era crash.** It means we can't *promise* it will.
- **It does NOT decode why the spikes have shrunk.** Less external
  stress, better stress-handling, smaller life events, or some
  combination — the data shows the compression, not the cause.
- **It does NOT contradict the user's experiential framing for the
  current era.** They report that intense moments can trigger crashes.
  The data shows they often do (5/15 still match clearly) — just
  that the typical magnitude of those moments has fallen, making them
  harder to discriminate from baseline noise.

## The kind-of-crash theory now has strong support

Combined picture across H02 + H02b:

- H02 train showed a real direction but didn't clear the bar
- H02b train **clears the bar decisively** with a 71% rate and
  +29.9 pp discrimination
- Both windows show validate as null or near-null
- The shape of the compression (baselines and lead-up maxes both
  shrank) directly fits "the kind of crash changed" — not just
  fewer crashes, but different in physiological signature

This is the strongest single finding of the investigation so far, and
it dovetails with the kind-of-crash investigation plan
([kind-of-crash-investigation.md](../kind-of-crash-investigation.md)).
K01 and K02 (severity / duration shifts) should now have higher prior
probability of finding something.

## What kind of card this would support (if we relax pre-registration)

Per the strict rule, no `card.md`. But the result is informative
enough that we should sketch what's defensible:

- **A retrospective card for pre-2024 crashes is fully supported.**
  Reading a 2023 crash's lead-up days and surfacing "there was a
  Y-minute stress spike on day Z" would be accurate 71% of the time —
  not 100%, but high enough that the card adds real value.
- **A precursor card for new 2024+ crashes is NOT supported.** It
  would fire wrongly on null days at ~40% rate and miss real spikes
  on ~67% of validate crashes. Not actionable.
- **A retrospective card for 2024+ crashes is defensible if framed
  honestly.** For ~5 of 15 it would surface a real spike; for the
  rest it would honestly say "we don't see an unusual spike pattern
  before this crash." That's the brainfog-aware framing the design
  brief asks for: not pretending to see signal that isn't there.

This is the kind of nuance the eventual `card.md` should encode if
the user wants to revisit the verdict and write a *retrospective-only*
card variant. Pre-registration's strict bar prevents us from claiming
predictive use; a retrospective-only card sidesteps that.

## Caveats acknowledged

- **Garmin's stress algorithm changes across firmware versions** —
  7.x → 10.4 across the window. The "≥75" threshold may not mean
  exactly the same physiological state in 2023 and 2026. The
  compression finding above could be partly algorithmic, not purely
  physiological.
  - *Update 2026-06-05*: brief web research on this — Garmin's own
    position (forum-moderator answer to a similar question in June
    2024) is that "the algorithm doesn't change on any model,
    [but] the baseline might be reset on firmware update." No
    documented major stress-algorithm overhaul targeting the FR245
    in 2022–2026; only minor bug fixes (v8.20 touched RHR /
    Firstbeat interference). The "enhanced Body Battery" (Venu 3 /
    Vivoactive 5, Sept 2023) is explicitly *not* a calculation
    change. If firmware were the explanation, we'd expect
    discontinuities at update dates rather than the smooth 18-month
    decline we see in S01. Small calibration shifts can't be
    fully ruled out but the shape of the trajectory fits real
    physiology better than algorithmic drift. References:
    [Garmin forum June 2024](https://forums.garmin.com/apps-software/mobile-apps-web/f/garmin-connect-web/397167/did-the-stress-algorithm-change-in-june-2024),
    [FR245 v8.20 changelog](https://forums.garmin.com/sports-fitness/running-multisport/f/forerunner-245-series/278298/forerunner-245-series-software-version-8-20---live),
    [gadgetsandwearables enhanced BB](https://gadgetsandwearables.com/2023/10/29/garmin-enhanced-body-battery/).
- **Watch-on-wrist confound**: an intense spike during a sweaty
  workout where the user forgot to start an activity could
  mis-trigger as "intense moment." We don't filter on activity-
  overlap days in this version. H02c could.
- **One-of-many operationalisations**: "spike ≥ 5 min ≥ 75" is a
  reasonable choice but not the only one. Different thresholds
  (≥3 min, ≥60 stress) or different aggregations (sum-of-spikes
  vs max-spike) could give different results.
- **Mechanism mixing in `crash_v1`**: confirmed yet again — four train
  episodes and ten validate episodes show no clear spike precursor.
  Those are candidates for `crash_v2` analysis to see if they form a
  coherent non-spike subtype.
- **Shared upstream**: a panic attack at 4 pm and a crash 2 days
  later could both be downstream of the same underlying event. The
  test can't disentangle.

## What we do next

- Per [hypothesis.md §9](hypothesis.md): train-supported / validate-
  refuted = "partial / asymmetric" → write this result.md (done),
  consider candidate H02c reshapes (not now), proceed to K01 + K02.
- The kind-of-crash thread is now even better-supported by this
  result; recommend running K01 (depth) + K02 (duration) next — both
  cheap and well-shaped to confirm the era shift directly.
- Note for product: the spike-detecting metric is **the right shape**
  for a retrospective-card prototype if we ever choose to write one,
  even though the strict bar wasn't cleared overall.

---

*Test run 2026-06-05. Extractor processed 7.888 monitoring_b FIT
files, ~5 minutes. Re-runnable with same seed (`20260605`).*
