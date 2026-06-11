# H05 — Recovery-time characterisation after crashes

**Pre-registration written 2026-06-05, before any data was inspected
for this test.** Locked.

**This hypothesis is descriptive, not predictive.** No train/validate
split is applied. The goal is to characterise what recovery from a
`crash_v1` episode actually looks like for this user, so that future
cards comparing a current crash's recovery to past patterns have a
reference distribution. The pacing-doc explicitly anchors the
shielder-vs-reliever experiment on this kind of foundation card.

## 1. Claim (descriptive)

After a `crash_v1` episode ends (last day with score ≤ 3 in the
merged episode), there exists a characterisable distribution of
**recovery time** — defined as the number of days until the gevoelscore
returns to within 1 point of the user's 30-day rolling median score.

We expect:
- A measurable median recovery time
- An IQR that can be used to express "shorter than usual" or "longer
  than usual"
- Possibly a difference in distribution between pre-recovery (2022–23)
  and post-recovery (2024–26) episodes — but the pre-registered
  primary deliverable is the overall distribution; the pre/post
  comparison is secondary.

## 2. Why this test

- Card-enabling. "Recovery from this crash took 5 days; your typical
  recovery from crashes this deep is 4–7 days." That sentence requires
  knowing the distribution.
- Mechanism-shift detection. If H01–H04 collectively show "the kind of
  crash changed between 2023–24 and 2025–26", recovery-time
  distribution is one place that change might also appear. A change
  in recovery distribution would corroborate the mechanism-shift
  story; no change would slightly weaken it (the residual crashes,
  though less frequent, would still have similar dynamics).
- It's also the foundation for the shielder-vs-reliever
  experiment ([pacing-and-crash-mitigation §5](../../../pacing-and-crash-mitigation.md)).
  Recovery-time distribution is the variable that intervention timing
  would later be tested against.

## 3. Data sources

- **Crash labels**: `crash_v1` per registry §2.
- **Daily scores**: `day_entries.date` + `day_entries.score`.
- No Garmin data is required for this test.
- **Analysis window**: 2022-09-03 → 2026-06-05.

## 4. Measurement protocol

For each `crash_v1` episode:

1. **Episode end day** = the last day in the merged episode where
   `score ≤ LOW_THRESHOLD` (score ≤ 3).
2. **Reference baseline** = the trimmed mean (10/90) of the user's
   score in the 30 days **before** the episode start day (so it
   reflects pre-episode normalcy, not post-recovery overshoot).
3. **Recovery target** = `reference_baseline − 1`. We say the user has
   recovered when their score has come back to within 1 point of
   pre-episode normal.
4. **Recovery time** = number of calendar days from the day **after**
   episode end until the **first** day where `score ≥ recovery_target`.
   Counts the recovery-walk days.
5. If the score never reaches the recovery target before the next
   crash episode begins → recovery is "censored by next episode".
   Report the count of censored episodes separately.
6. If the recovery target is met on the day immediately after episode
   end → recovery time = 0 days.

## 5. Deliverables (no pass/fail criterion — descriptive)

A single distribution summarising recovery time across episodes, with:

- N total episodes
- N episodes with completed recovery
- N episodes censored by next crash
- N episodes with data gap preventing measurement
- For completed-recovery episodes: median, IQR (25th–75th percentile),
  range, histogram
- Per-episode breakdown showing: episode start, end, episode duration,
  pre-episode baseline, recovery target, recovery time (or censored
  flag).

**Secondary breakdown** by era (pre-2024 train-era / 2024+
validate-era) — descriptive only, not a hypothesis test. The
mechanism-shift theory predicts recovery distributions may differ; we
report if they do but don't pre-register a threshold for "different".

## 6. Exclusion rules

- **Episodes whose episode-end is within 31 days of the end of the
  analysis window** (2026-06-05) are excluded — they may have
  insufficient post-episode data to characterise recovery.
- **Episodes where the 30-day pre-episode baseline window has fewer
  than 20 valid scores** are excluded — too little context to
  determine "normal".

## 7. Expected shape if everything works

Rough sanity checks for `result.md`:

- Median recovery time: 2–7 days (matching the typical PEM literature)
- IQR roughly 1–10 days
- A small tail of long-recovery episodes (10+ days) corresponding to
  the deeper / longer crashes
- 0 days is possible (the day after episode end already meets target)

If we see median 0 days for everything, the recovery target is set
too low. If we see "all episodes censored", the recovery target is too
high. Both should be flagged in result.md as data quality issues.

## 8. Caveats `result.md` must explicitly acknowledge

- **Recovery time as defined is a statistical artifact**, not a
  clinical recovery metric. "Score returns to baseline" doesn't mean
  the user feels back to themselves — it just means the gevoelscore
  has stopped marking them as below pre-episode normal. Subjective
  full recovery may take much longer.
- **The 30-day pre-episode baseline can be shifted by ongoing
  recovery trajectory** — early-window baselines are lower (worse
  health era) than late-window baselines. This is intentional (we
  want recovery relative to *that time's* normal) but it means
  recovery times across eras are comparing different reference
  points.
- **Censoring by next crash** is most common in dense crash years
  (2023–24). Don't read "more long recoveries in 2023–24" as a
  finding without first checking how many were censored.
- **The pre/post-2024 secondary comparison is heavily confounded** by
  the very recovery trajectory we're studying. Crashes in 2025–26
  are by definition the residual ones the user pulls through despite
  being in a better state. Drawing causal conclusions from any
  pre/post difference here is unwarranted; the descriptive shape is
  what we can stand on.
- **Score interpretation drift is ruled out** for our purposes since
  the user has confirmed real recovery (per
  [project_recovery_trajectory](../../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/project_recovery_trajectory.md)).

## 9. What we do with the result

- **Clean distribution emerges** → write `card.md` with 2–3 candidate
  recovery-comparison card variants. The card is uniquely
  *retrospective* — it can only fire on a crash that has already
  resolved (or one we're watching mid-recovery), comparing to the
  distribution this hypothesis produces.
- **Distribution is too sparse / mostly censored** → write `result.md`
  flagging the data limitation. May need to relax the recovery target
  (e.g. within 1.5 points instead of 1) but that would be H05b, not
  re-running H05.

---

*Pre-registration locked 2026-06-05. Next: `test.py`.*
