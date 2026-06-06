# H04 — Body battery net-drain elevated before crashes

**Pre-registration written 2026-06-05, before any data was inspected
for this test.** Locked. Any subsequent change creates an H04b.

## 1. Claim

In the 3 days before a `crash_v1` episode (per [registry §2](../registry.md)),
this user's daily **net body-battery delta**
(`chargedValue − drainedValue` from the UDS daily aggregates) is
consistently more negative than their own rolling 90-day baseline. The
elevation is *discriminative* — appears more often before crash
episodes than in randomly-sampled non-crash 3-day windows.

A negative `net_delta` means the day drained more battery than it
charged. The hypothesis is that crashes are preceded by 3 days of
sustained net drain — the body burning through its budget faster than
it can recover.

## 2. Why we think this

- Body Battery is Garmin's own composite of HR + HRV + stress + sleep.
  It is the **single number** the user already sees in Garmin Connect
  and the closest off-the-shelf proxy to the pacing literature's
  "energy envelope" concept.
- H01 (RHR) was null. H02 (avg stress) was train-supported but
  validate-refuted. H03 (sleep efficiency) was null in both windows.
  H04 effectively tests **the composite** of these signals. If the
  composite picks up something the individual signals don't, the
  algorithm's weighting may be useful. If H04 inherits the H02 train-
  only pattern, that's expected (stress carrying the signal through the
  composite). If H04 is null in both windows, we've confirmed that no
  daily-aggregate composite catches the residual crash precursor.
- H04 is the **last clean test of the daily-aggregate hypothesis**.
  After H04, the remaining unexplored angles are sub-daily (per-minute
  spikes — H02b), specific sleep subcomponents (H03b), or descriptive
  aftermath analysis (H05).

## 3. Data sources

- **Crash labels**: identical to H01/H02/H03 — `crash_v1` per registry §2.
- **Body battery**: `DI_CONNECT/DI-Connect-Aggregator/UDSFile_*.json`,
  fields `bodyBattery.chargedValue` and `bodyBattery.drainedValue` per
  day. `net_delta = chargedValue - drainedValue` (negative = net drain).
- **Analysis window**: 2022-09-03 → 2026-06-05.
- **Train / validate split**: train 2022-09-03 → 2023-12-31 (14
  episodes); validate 2024-01-01 → 2026-06-05 (15 episodes).

## 4. Measurement protocol

For each crash episode dated `D`:

1. **Lead-up window** = `[D − 3, D − 1]` (3 days, same as H02 — body
   battery is reactive on a similar timescale to stress).
2. **Baseline window** = `[D − 93, D − 4]` (90 days ending 3 days before
   the episode).
3. **Baseline net_delta** = trimmed mean (drop top + bottom 10%) of
   daily `net_delta` within the baseline window.
4. **Lead-up net_delta** = simple mean of daily `net_delta` within the
   lead-up window.
5. **`delta_bb_net` for this episode** = lead-up minus baseline (units:
   body-battery points; negative means lead-up was more drained than
   baseline).

For discrimination:

6. **Null sample** = 200 randomly-selected 3-day windows from the same
   analysis window, disjoint from any crash episode's lead-up. Seed
   `20260605`.

## 5. Pre-registered falsification criterion

The hypothesis is **supported** if and only if **all three** hold in
**both** train and validate windows independently:

a. **Frequency**: at least **60%** of crash episodes have
   `delta_bb_net ≤ −5` body-battery points.

b. **Discrimination**: the crash-episode frequency from (a) is at
   least **15 percentage points higher** than the null-sample frequency
   of windows with `delta_bb_net ≤ −5`.

c. **Magnitude**: the median `delta_bb_net` across crash episodes is at
   most **−3** points, and the upper quartile is at most **0** points
   (most lead-ups drained more than baseline).

Any one of (a), (b), (c) failing in either window → **refuted**.

If we have fewer than 10 clean crash episodes per window after
exclusions → **inconclusive**.

The −5 / −3 thresholds reflect that body-battery typical daily ranges
are roughly ±30; a 5-point shift in the lead-up mean is a meaningful
~15% relative shift but not extreme.

## 6. Exclusion rules

- **Episode requires all 3 valid body-battery days in lead-up** (3 of
  3, matching H02's tighter requirement for the small window).
- **Episode requires ≥ 30 valid days out of 90** in baseline.
- **Days where chargedValue and drainedValue are both 0** are excluded
  as off-wrist or sync-failure days, not real zero-delta days.
- **Episodes whose lead-up overlaps another crash episode's days** are
  excluded from primary analysis, reported separately.
- Baseline may use pre-2022-09 UDS data.

## 7. Expected effect size if the hypothesis is true

Rough sanity checks for result.md:

- 70–80% of crash episodes show `delta_bb_net ≤ −5`
- Null sample rate: 20–35% (random 3-day windows have natural
  variance, and battery deltas are noisier than stress averages)
- Median `delta_bb_net` across crashes: roughly −5 to −15 points
- If we see crash rate 95% and null rate 90%, the baseline is broken.

## 8. Caveats `result.md` must explicitly acknowledge

- **Body Battery is opaque**. Garmin doesn't publish the algorithm.
  We're testing whether a closed-source composite predicts crashes,
  not the underlying mechanisms.
- **Algorithm version drift**: FR245 firmware 7.x → 10.4 across the
  window. Body Battery weighting plausibly changed.
- **chargedValue includes sleep charging**, which is large compared to
  daytime drain. If sleep is preserved (per H03), days with normal
  sleep + a tough day might still come out roughly balanced, masking
  daytime drain.
- **The composite includes stress** (H02 train-positive). H04 may
  inherit the H02 train-only pattern by construction. If so, H04 isn't
  adding new info — it's confirming that stress is the dominant
  daily-aggregate signal channel.
- **Shared cause**, **mechanism mixing in `crash_v1`**, and
  **multi-comparison** caveats from H01–H03 apply identically.

## 9. What we do with each outcome

- **Supported in both windows** → write `card.md`. The card would say
  something like "your body battery drained more than it charged for
  three days running before this." (Real copy in `card.md`, not here.)
- **Train-only supported (matches H02 pattern)** → write `result.md`
  noting this is mechanically expected if stress drives the composite.
  H04 in that case adds no new info beyond H02.
- **Refuted in both** → confirms the daily-aggregate channel is closed
  for the residual crashes. The synthesis after H05 should treat this
  as the definitive close of "daily averages as precursor."
- **Inconclusive** → unlikely given UDS coverage; if it happens flag
  the data issue.

---

*Pre-registration locked 2026-06-05. Next: `test.py`.*
