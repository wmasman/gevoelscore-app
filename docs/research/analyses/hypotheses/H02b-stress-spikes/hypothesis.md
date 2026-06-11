# H02b — Per-minute stress spike duration before crashes

**Pre-registration written 2026-06-05, before any data was inspected
for this test.** Locked. Any subsequent change creates an H02c.

## 1. Claim

In the 3 days before a `crash_v1` episode (per [registry §2](../registry.md)),
at least one day contained a **longer-than-baseline sustained intense
stress spike**, measured at per-minute resolution from the raw
monitoring_b FIT samples. The lead-up's max-spike-duration is
*discriminative* against randomly-sampled non-crash 3-day windows.

A "spike" here is a contiguous run of stress samples ≥ 75 lasting
≥ 5 minutes. We score each day by its longest such spike; we score
each 3-day lead-up by the **maximum** of those daily values; we
compare each crash's lead-up to that user's own baseline of typical
daily max-spike-duration.

## 2. Why we think this

- **H02 (daily mean stress) found a train-window positive direction
  but no validate signal.** The daily average dilutes a 20-minute
  intense spike with 1.420 calmer minutes.
- The user has **independently reported** (saved as
  [project memory](../../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/project_crash_triggers_user_experience.md)):
  > "An intense episode during a day, even when the rest of the day
  > is kept calm, can still trigger crashes."
  This is the most direct first-person evidence we have about *this*
  user's crash mechanism, and it points exactly at the metric daily
  aggregates miss.
- Per-minute stress samples are present at ~1.400/day across the
  full 1.733-day monitoring_b coverage. The data is there; we just
  haven't summarised it at this resolution before.
- This is the highest-probability single test in the project's near
  future for finding a precursor that survives the recovery cliff.

## 3. Data sources

- **Crash labels**: `crash_v1` per registry §2 (identical to H01–H05).
- **Per-minute stress**: `stress_level` messages from each
  `monitoring_b` FIT file, decoded with `fitdecode`. Fields:
  `timestamp`, `stress_level_value` (0–100). Multiple files per day
  are merged (a day's stress timeline = union of timestamps across
  files for that calendarDate, deduped).
- **Daily reference baseline (sleep / activity)**: not used — H02b is
  pure stress-spike timing.
- **Analysis window**: 2022-09-03 → 2026-06-05.
- **Train / validate split**: train 2022-09-03 → 2023-12-31 (14
  episodes); validate 2024-01-01 → 2026-06-05 (15 episodes). Same as
  H01–H04.

## 4. Measurement protocol

### 4.1 Daily max-spike-duration

For each calendar date with monitoring_b data:

1. Collect all `stress_level` samples for that date, sorted by
   timestamp, deduped on timestamp.
2. Drop any sentinel/invalid values: stress values outside [1, 100]
   are excluded (Garmin uses 0 / negatives to mean "off-wrist" /
   "too active" — we don't want those treated as low stress).
3. Walk the timeline. Define a "spike" as a run of consecutive
   samples where:
   - all values are ≥ 75, AND
   - gaps between consecutive timestamps are ≤ 3 minutes (allows for
     occasional missed samples), AND
   - the total duration (last timestamp − first timestamp) is ≥ 5
     minutes.
4. Day's `max_spike_minutes` = duration in minutes of the longest
   qualifying spike on that day, or 0 if none.
5. Days with fewer than 60 stress samples are flagged as
   "low-coverage" and excluded from baseline computation (these are
   off-wrist / partial-wear days that would bias the baseline
   downward).

### 4.2 Per-episode profile

For each crash episode dated `D`:

1. **Lead-up window** = `[D − 3, D − 1]` (3 days, same as H02).
2. **Baseline window** = `[D − 93, D − 4]` (90 days ending 3 days
   before the episode).
3. **Lead-up max-spike** = max of `max_spike_minutes` across the 3
   lead-up days.
4. **Baseline mean max-spike** = trimmed mean (10/90) of
   `max_spike_minutes` across valid days in the baseline window.
5. **`delta_spike` for this episode** = lead-up max-spike − baseline
   mean max-spike (units: minutes).

### 4.3 Null sample

200 randomly-selected 3-day windows from the analysis window, each
disjoint from any crash episode's lead-up. Same logic as H02; same
seed `20260605`.

## 5. Pre-registered falsification criterion

The hypothesis is **supported** if and only if **all three** hold in
**both** the train window and the validate window independently:

a. **Frequency**: at least **60%** of crash episodes have
   `delta_spike ≥ 10 minutes` (lead-up had at least one spike 10 minutes
   longer than typical for this user).

b. **Discrimination**: the crash-episode frequency from (a) is at
   least **15 percentage points higher** than the null-sample
   frequency of windows with `delta_spike ≥ 10 minutes`.

c. **Magnitude**: the median `delta_spike` across crash episodes is at
   least **+5 minutes**, and the lower quartile is at least **0
   minutes** (most lead-ups have at least equal-to-baseline spike
   duration, not just a few outliers).

Any one of (a), (b), (c) failing in either window → **refuted**.

If we have fewer than 10 clean crash episodes per window after
exclusions → **inconclusive**.

The +10 / +5 thresholds are deliberately modest: a 10-minute longer
intense spike than typical, sustained for at least 5 minutes — that's
roughly a single dentist visit, a sustained argument, a panic moment.
Below this, the signal is in noise; above, the user's experiential
claim says it can trigger a crash.

## 6. Exclusion rules

- **Episode requires ≥ 2 valid stress days out of 3** in lead-up
  (slightly less strict than H02 because a single off-wrist day in a
  3-day window is more likely with raw FIT data than with daily
  aggregates).
- **Episode requires ≥ 30 valid days out of 90** in baseline.
- **Days with fewer than 60 stress samples total** are excluded from
  both baseline and lead-up (this is the "low-coverage" definition
  in §4.1).
- **Episodes whose lead-up overlaps another crash episode's days**
  excluded from primary, reported separately.

## 7. Expected effect size if hypothesis is true

Rough sanity-checks for `result.md`:

- 70–80% of crash episodes have `delta_spike ≥ 10 min`
- Null sample rate: 25–40% (random 3-day windows naturally include
  some genuinely stressful day)
- Median `delta_spike`: 10–25 minutes
- If we see crash rate of 100% and null rate of 95%, the metric is
  too sensitive (everyone has a stressful spike sometimes) — flag.

## 8. Caveats `result.md` must explicitly acknowledge

- **Garmin's stress algorithm is opaque** and changes between
  firmware versions (FR245 7.x → 10.4 across the window). A 75 in
  2023 may not mean exactly the same physiological state as a 75 in
  2026.
- **"Spike ≥ 5 minutes ≥ 75" is one of many ways to operationalise
  the user's experiential claim.** "Highest sample of the day,"
  "count of samples ≥75 / day," "longest spike with threshold 60 vs
  75," and several other shapes are all defensible. This test picks
  one and pre-commits.
- **Watch-on-wrist confound**: an intense spike during a 20-minute
  emotional event matters; an intense spike that's actually a sweaty
  workout where the user remembered to start an activity does not.
  We do not currently filter out activity-overlap days. Future H02c
  could.
- **Shared upstream**: a 30-minute panic attack the day before a
  crash could be (a) the trigger, or (b) the early subjective
  signal of the same process that's about to produce the crash. The
  test cannot distinguish these.
- **`crash_v1` mixes mechanisms**: this test may catch the
  intense-moment-triggered subset cleanly while being null on others.
  If the verdict is "partial" in a per-episode-breakdown way (some
  episodes show big deltas, others zero), that's interesting and
  goes into result.md.
- **Multi-comparison**: H02b is the 6th hypothesis tested. Given
  five refuted on the bar, inflation isn't acute, but it would
  matter if H02b also lands borderline.

## 9. What we do with each outcome

- **Supported in both windows** → first supported hypothesis of the
  whole project. Write `card.md` with 2–3 candidate card-text
  variants using real numbers from this user's data and real quoted
  notes from the supported crash days. The card here is the
  forensic-companion card the synthesis pointed at: "around X date
  there was a Y-minute stress spike on day Z — what was happening?"
  Strong consideration for being the first card prototyped in the
  app.
- **Refuted in both** → the user's experiential claim is *not*
  captured by this particular operationalisation. Doesn't mean the
  underlying claim is wrong — only that "longest contiguous ≥75
  spike, lead-up max" isn't the right shape. Candidate H02c
  reshapes (different threshold, different aggregation) listed in
  registry.
- **Partial / asymmetric** (train-yes / validate-no, or vice versa)
  → particularly interesting given the recovery cliff. Validate-only
  positive would be a major finding: the residual crashes *do* have
  a precursor, it just lives below the daily-aggregate horizon.
- **Inconclusive** → unlikely given coverage, but if FIT-parse
  issues bring usable episodes below 10/window, debug and re-run.

---

*Pre-registration locked 2026-06-05. Next: `test.py` parses ~8.000
monitoring_b FIT files (takes a few minutes), then evaluates per
above protocol.*
