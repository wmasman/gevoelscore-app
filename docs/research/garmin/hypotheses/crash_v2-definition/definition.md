# crash_v2 — two-tier crash / dip classification

**Pre-registration written 2026-06-06, before any data was inspected
under this definition.** Locked. Any subsequent change creates a `crash_v3`.

## 1. Purpose

`crash_v1` (registry §2) labels a "crash" as `score ≤ 3 for ≥ 2
consecutive days, merged within 3 days`. That definition has
served H01–H05 + K01/K02 + H02b. It has two known weaknesses,
both surfaced by the H02b specificity check:

1. **Mixed mechanisms inside `crash_v1`.** Of 14 train + 15 validate
   crash_v1 episodes, 4 + 10 respectively show no biometric spike
   precursor. Some "crashes" may be 2-day functional dips that don't
   share the PEM signature with the others.
2. **Sub-threshold "dips" outside `crash_v1`.** The specificity check
   tagged 32 of 83 false-positive spike windows as `near_miss` — at
   least one day in window had score = 3 but the 2-day rule wasn't
   met. The watch saw something. The score-3 day was a real bad day.
   `crash_v1` discards these as noise.

`crash_v2` introduces a **two-tier** classification — `crash` and
`dip` — so that re-runs of K01, K02, H02b, and notes-categorisation
can test whether **real PEM crashes** (tier 1) and **acute bad days**
(tier 2) behave differently in the biometric and language signal.

A separate `vague_low` tier was considered (score-4-day clusters)
and **explicitly rejected** as overcomplication — the strong
signals live in score-≤3 territory; score-4 days go into `normal`.

## 2. Definitions

### 2.1 Tier 1 — `crash` (strict PEM)

A `crash` episode is a run of days satisfying **both**:

a. **Acute condition** — `score ≤ 3` for `≥ 2 consecutive days`.
   (Identical to `crash_v1`.)

b. **Merge** — two qualifying episodes whose last-day and next-day
   are within `3 days` of each other merge into one. (Identical
   merge rule to `crash_v1`.)

A `crash` episode's **days are all days from `start` (first
sub-threshold day) through `end` (last sub-threshold day)**, after
merging.

**Note: tier-1 `crash` is exactly `crash_v1`.** A slow-recovery
tail filter (`median(score)` over days `[end+1, end+7]` ≤ 5) was
included in the original 2026-06-06 draft of this spec, with the
hypothesis that 4–10 short v1 episodes would demote to dip on
fast bounce-back. The data showed **all 29 v1 episodes have
tail_median ∈ {4.0, 5.0}**, so the filter demoted zero episodes
and was removed for simplicity. The empirical finding "all v1
crashes have a slow-recovery tail" is now a positive validation
of crash_v1's acute condition: it already only catches PEM-shape
events. The recovery-tail median is still **computed and stored
in the labels CSV** for descriptive analysis even though it
plays no classification role.

### 2.2 Tier 2 — `dip` (acute bad day, isolated)

A `dip` is:

**Isolated bad day** — a single day with `score ≤ 3` whose
neighbours both have `score ≥ 4`. Days outside the corpus
boundary are treated as `≥ 4` for this rule, so day 1 and day N
can qualify.

Two consecutive bad days never form a dip — they're either a
crash (tier 1) or, if isolated by a missing-score gap on one or
both sides, they're still considered a dip-pair (treated as two
separate dips). In practice this edge case has not been
observed given the user's complete-coverage logging.

`dip`s do not merge — each qualifying single day is its own dip.

### 2.3 `normal`

Every day not classified as `crash` or `dip` is `normal`. This
includes score-4 days regardless of context (no separate
`vague_low` tier).

### 2.3a Dip clusters (descriptive overlay, not a tier)

A **dip cluster** is a transitive chain of two or more isolated dips
where each consecutive pair is within 7 days of each other. Clusters
capture "rough patches" — periods where the participant has multiple
single bad days separated by partial recovery, e.g. a 4-3-4-3-4
pattern, that the per-day classification splits into separate dip
events but that visually and experientially read as one extended
event.

Clusters are **descriptive overlay only** — they do not change the
per-day labels (each constituent day remains `dip`). They are
captured as a `dip_cluster_id` column in `labels_crash_v2.csv` so
downstream analyses can choose to:
- treat each dip as an independent event (existing behaviour), or
- collapse clusters into single multi-day events (e.g. for "rough
  patch" duration analysis).

Singleton dips (not in any cluster of size ≥ 2) have an empty
`dip_cluster_id`. The cluster rule was added 2026-06-06 after the
visualisation of the dip layer surfaced a real "multi-day rough
patch" phenomenon the single-day spec could not represent. Initial
run produced 15 clusters covering 45 of 79 dips (57%), with the
longest cluster spanning 2024-03-14 → 2024-04-16 (9 dips, 34 days).

### 2.4 Precedence

When a day could fit multiple tiers:

1. If it's part of a `crash` episode (tier 1) → tier 1.
2. Otherwise, if it meets `dip` criteria (tier 2) → tier 2.
3. Otherwise → `normal`.

**Crash shadow**: a day inside the 7-day window after a crash
ends (days `end+1` through `end+7`) is **not** classified as a
separate dip even if its score is ≤ 3 and its neighbours qualify.
It is labelled `normal` with an `in_crash_tail=True` flag in the
labels CSV. This prevents the recovery-period score-3 days from
being double-counted as new events.

## 3. Edge cases

### 3.1 Missing-score days
Days where the user did not log a `gevoelscore` are treated as
**run-breakers** — a gap of any size breaks a consecutive-day run,
matching the existing `crash_v1` detection logic in
`H02b-stress-spikes/test.py`. Missing days also do not contribute
to the recovery-tail median (their slot is skipped). In the current
corpus (2022-09-03 → 2026-06-05) the user has logged every single
day (1,372 scored days, 0 gaps), so this rule has no effect in
practice; it is fixed now so future re-runs over expanded windows
behave predictably.

### 3.2 Episode at corpus boundary
A potential `crash` episode whose recovery window `[end+1, end+7]`
extends past the corpus end (`2026-06-05` at lock time): use the
median over the available days for descriptive logging only. With
the slow-recovery filter removed (§2.1) this no longer affects
classification — every v1-shape episode becomes a tier-1 crash
regardless of how truncated its tail is.

### 3.3 Very-low days (score = 1 or 2)
No special treatment. They count toward sub-threshold runs and
recovery medians identically to score-3 days.

### 3.4 Multi-mode users (re-recovery + re-crash)
After a `crash` episode ends, the next qualifying episode is its
own episode regardless of subsequent score trajectory. Stabilisation
across years (per S01) is captured by re-running classification
per-era, not by varying the definition.

## 4. Counts (as run 2026-06-06)

The original pre-registration predicted **crash 18–25, dip 50–120**.
First run produced **crash 29, dip 79**. The crash count was outside
the predicted range because the prediction assumed the slow-recovery
filter would demote 4–10 v1 episodes; the data showed 0 demotions
(every v1 episode has tail_median ∈ {4.0, 5.0}, none ≥ 6). The
filter was therefore removed (§2.1) and the actual ranges below
replace the predictions:

| label | count, 2022-09-03 → 2026-06-05 |
|---|---:|
| `crash` episodes | 29 (= `crash_v1`; positively validated — every v1 episode has slow-recovery tail) |
| `dip` events | 79 (within the original 50–120 range, no adjustment needed) |
| `normal` days | majority (~91% of 1,372 days) |

The original review flags (re-stated for future re-runs):
- **<10 crash episodes** in any future re-run → flag for review.
- **>40 crash episodes** in any future re-run → flag for review.
- **>500 dip events** → dip definition catching noise; flag.

Era split (informative, not in sanity-check):

| era | crash episodes | isolated dips | dip:crash ratio |
|---|---:|---:|---:|
| 2022-09 → 2023-12 (train) | 14 | 26 | 1.9× |
| 2024-01 → 2026-06 (validate) | 15 | 53 | 3.5× |

The dip:crash ratio nearly doubles between eras — visually consistent
with the stabilisation-pendulum narrative (fewer sustained crashes,
more transient bad days).

## 5. Validation plan

`crash_v2` is a definition, not a hypothesis. We don't "test" it; we
**apply it, then re-run downstream tests with the new labels**.

### 5.1 Apply
- `scripts/apply_crash_v2.py` — takes day_entries.csv (gevoelscore
  per day), emits `labels_crash_v2.csv` with columns
  `date, score, label, episode_id, episode_start, episode_end,
  episode_length_days, tail_median, tail_n_days, verdict,
  in_crash_tail`.
- `scripts/visualize_timeline.py` — emits `timeline_v1_v2.png` for
  visual sanity-check of label placement.
- `comparison_to_v1.md` — auto-generated report showing
  per-episode crash_v1 → crash_v2 mapping (with the slow-recovery
  filter removed, mapping is 1:1) and the new isolated-dip list.

### 5.2 Re-run downstream (in this order)
1. **K01 (depth)** — does the median per-episode min score differ
   between crash_v2-tier-1 and tier-2? If yes → tiers capture
   something real.
2. **K02 (duration)** — does episode length differ?
3. **H02b (spike precursor)** — re-run the discrimination test
   with crash_v2 tier-1 labels only. Prediction: discrimination
   should *strengthen* because we've removed the mixed-mechanism
   subset.
4. **specificity check** — re-run with the new tier-1 labels.
   Prediction: `near_miss` proportion drops because most former
   near-misses are now properly labelled as `dip`.
5. **notes categorisation** — re-run with three groups (`crash`,
   `dip`, `normal`) instead of two. Does the language signature
   differ between crash and dip? This is the **key question** for
   whether the tier distinction is biologically real or just a
   re-labelling exercise.

### 5.3 Acceptance: when can we say crash_v2 is the right cut?
**Either** of these is sufficient:
- **H02b spike-discrimination strengthens** (crash − null ≥ +35 pp on
  train) when restricted to tier-1 crashes, vs +29.9 pp under
  crash_v1.
- **Language signature differs between tier-1 crash and tier-2 dip**
  with effect size ≥ +20 percentage-point difference in
  `negative-dominant` polarity rate.

If **neither** strengthens, crash_v2 is a re-labelling without
predictive value. Document that honestly and consider whether to
revert to crash_v1 for downstream work.

## 6. Caveats

- **The 7-day recovery window is retained for descriptive logging
  only.** The slow-recovery filter is removed (§2.1), so the
  window doesn't affect classification — but the median is still
  captured per-episode in the labels CSV. Future analyses may
  use it as a per-episode covariate (e.g. "deeper crashes have
  lower tail medians").
- **`dip` events are not merged.** A user with three consecutive
  isolated bad days separated by good days will get three dips. This
  may be wrong for some product framings (e.g. "you had a rough
  patch"). For statistical analysis it's the right cut — each
  qualifying event is independent for testing purposes.
- **The score-only definition deliberately excludes biometric
  corroboration** from the tier definition itself. This avoids
  circularity when we then test whether biometric signals predict
  crash_v2 tiers. The trade-off: a "crash" defined purely on
  self-score may sometimes be a 2-day mood-low without HRV
  signature, or vice versa. We accept this.
- **Crash and v1 are identical in this corpus.** The empirical
  finding (§4) that every v1 episode has tail_median ≤ 5
  validates crash_v1's acute condition. But it's also possible
  future expanded data (additional users, extended window) would
  surface fast-bounce 2-day lows that the recovery filter would
  catch. If that happens, the filter should be re-introduced as
  a `crash_v3` — not a silent revision of v2.
- **`crash_v2` is locked at this revision.** Any change to thresholds
  or rules from this point forward becomes `crash_v3` — and we re-run
  all downstream from scratch.

## 7. What we do with each outcome

After §5 re-runs:

- **K01/K02 separation + H02b strengthening + notes signature** —
  crash_v2 is the new standard. Update registry.md §2 to point to
  this definition. Future hypotheses default to tier-1 labels.
- **K01/K02 separation only** — crash_v2 partially validated.
  Document the partial result; keep both definitions live; prefer
  v2 for biometric, v1 for backward-compat.
- **No separation** — crash_v2 was a re-labelling exercise. Document
  and revert to crash_v1 as the standard. Save the script and the
  reasoning so a future researcher doesn't repeat the exercise.

---

*Pre-registration locked 2026-06-06. Next: `apply_crash_v2.py`
runs against day_entries.csv (~1.733 days), emits labels.csv +
comparison.md.*
