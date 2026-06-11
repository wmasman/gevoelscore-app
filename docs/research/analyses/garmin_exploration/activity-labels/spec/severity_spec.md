# Severity cutoffs — percentile-rank PEM-envelope classification

**Calibrated 2026-06-06 from the distribution of
`activity_features_daily.csv` (1,372 days), blinded to crash
labels.** Pending verification of class distribution before locking.

This is the **v3 of the severity spec.** History:
- v1 used absolute thresholds for 3 of 4 axes → rejected for failing
  the relative-not-absolute principle.
- v2 used z-scores (median + MAD) for all axes → broke on zero-heavy
  distributions: `effective_exertion_min` has median 0 across most
  windows, MAD collapses to 0, z explodes (max z = 127!).
- **v3 (this spec) uses percentile rank within trailing 30 days.**
  Robust to zero-heavy distributions, still entirely
  baseline-relative, intuitive (rank 0.85 = top 15% of recent days).

Both PEM mechanisms encoded:
- **Shock** via single-day `exertion_class` (axes A–D below). A
  shock day is one where today's value is in the upper tail of the
  participant's recent baseline on at least one axis.
- **Push-crash** via separate `push_burden_class` (§ Push burden).
  Captures sustained pushing over a 7-day window.

## Single-day shock — `exertion_class`

Composite of four percentile-rank axes against the participant's
own 30-day rolling baseline. Each axis classifies the day on a
5-level ordinal scale; the composite is the **max** of all axes.

The rank thresholds are universal across participants — they
encode "how far into the upper tail of recent days does today
sit?", which is the PEM-relevant question. The baseline itself
does the personalisation.

### Axes (same cutoffs for all four)
| class | range | meaning |
|---|---|---|
| none | rank < 0.5 | at or below median |
| light | 0.5 ≤ rank < 0.75 | above median, typical |
| moderate | 0.75 ≤ rank < 0.85 | top quartile |
| heavy | 0.85 ≤ rank < 0.95 | top 15% |
| very_heavy | rank ≥ 0.95 | top 5% (shock) |

- **Axis A — `effective_exertion_rank_30d`**: total HR-elevated
  minutes (passive UDS) plus recorded activity duration.
- **Axis B — `step_rank_30d`**: step burden vs personal baseline.
- **Axis C — `max_hr_rank_30d`**: daily peak-HR. Catches brief
  intense moments that don't accumulate into vigorous-min.
- **Axis D — `vigorous_min_rank_30d`**: sustained HR-elevation
  duration. Complement to axis C.

### Composite
`exertion_class = max(axis_A, axis_B, axis_C, axis_D)`

Ordering: none < light < moderate < heavy < very_heavy.

### Why four z-axes (vs collapsing to one)?
Each axis answers a different question about what shocked the
envelope today:
- A: "how much total elevated-load time vs your norm?"
- B: "how many more steps than your norm?"
- C: "did you peak above your normal HR peak?"
- D: "did HR stay elevated longer than your norm?"

These can disagree. A day with a single 5-min stairs-climb event
spikes axis C (max_hr_z) but not A/D (no accumulated time). A day
with 90 minutes of low-HR sailing spikes A (total exertion) but
not B/C/D (no steps, no HR peak). Multi-axis composite catches
both shapes; collapsing would mask one of them.

### Sanity floors
The step-spike rule retains its absolute floor (`total_steps ≥
4000`) to suppress spurious spikes when the baseline is very low
(e.g. coming off a crash week where median is 200 steps/day). This
is **not** a classification cutoff — it's a noise gate that
prevents tiny absolute moves from being read as huge z-scores.

For other axes, no floor: a z-score against MAD already handles
near-zero baselines (MAD = 0 → z is undefined and the field is left
empty, then defaults to `none` in classification).

## Push-crash — `push_burden_7d` (raw count, no class)

Sustained envelope pressure over a rolling 7-day window.
Independent from shock — these can move differently. A burst day
without sustained elevation is a shock (push_burden may stay low).
A two-week mild-push period without a single shock day is a
push-crash candidate (push_burden steadily rises).

### Primary metric — push_burden_7d
`push_burden_7d = count of days in [d-6, d] with
effective_exertion_rank_30d ≥ 0.75`

Integer 0-7. Counts how many days in the last week were at or
above the participant's 75th-percentile typical exertion. Captures
sustained pushing as the count of moderate+ days.

**Downstream tests use this raw count directly**, not a binned
class. See § Push burden class — deprecated.

### Secondary metric — above_baseline_streak
Count of consecutive prior days with `effective_exertion_rank_30d
> 0.5` (above-median). Resets to 0 on the first below-median day.
Surfaces patterns like "you've been above baseline for 9 straight
days." Used descriptively; not part of classification.

### Push burden class — deprecated 2026-06-06 (v3.1)

An earlier draft binned push_burden_7d into a 5-level
`push_burden_class` (none/light/moderate/heavy/very_heavy with
boundary at count = 5). The sensitivity test
([sensitivity_report.md](../output/sensitivity_report.md))
showed the **very_heavy** boundary was brittle:
- Varying push_window 7d → 14d shifted the count of very_heavy
  days from 25 to 369 (Jaccard 0.07).
- Varying push_threshold 0.75 → 0.85 shifted from 25 to 8 days
  (Jaccard 0.32).

The underlying push_burden_7d count itself is stable; the binning
introduced artificial sensitivity at the tight integer threshold.

**Resolution**: drop the class. Downstream tests use
push_burden_7d (0-7 integer) directly. The class column is still
emitted in the CSV for backward compatibility but should not be
used in isolation. Pre-registered downstream tests reference the
raw count.

## Baseline trajectories — descriptive layer

Separately captured (not part of classification):
- 30-day rolling median of `effective_exertion_min`,
  `total_steps`, `max_hr_uds`, `vigorous_min_uds` plotted over the
  full corpus.
- Surfaces envelope shifts: "your typical max HR drifted from 115
  in mid-2024 to 122 in early-2026" — the trend the z-score
  cancels out is itself meaningful for pacing.
- Cross-references with the S01 stabilisation-trajectory work.
- Output: `baseline_trajectories.png` from script 06.

## Actual joint distribution (v3 rank-based, after applying)

Per `04_classify_exertion.py` run 2026-06-06 on 1,372 days:

### exertion_class (single-day shock)

| class | count | % |
|---|---:|---:|
| none | 363 | 26.5% |
| light | 324 | 23.6% |
| moderate | 212 | 15.5% |
| heavy | 239 | 17.4% |
| very_heavy | 234 | 17.1% |

The 17.1% very_heavy is the union of "axis ≥ 0.95" across four
axes — each axis individually has ~7% above 0.95, and the union
expands as different axes capture different shock patterns. This
is expected by design (4-axis composite).

### push_burden_class (sustained pushing)

| class | count | % |
|---|---:|---:|
| none | 239 | 17.4% |
| light | 411 | 30.0% |
| moderate | 357 | 26.0% |
| heavy | 340 | 24.8% |
| very_heavy | 25 | 1.8% |

The 1.8% very_heavy push burden (25 days with 5+ push days in last
7) are the **push-crash candidate days** — testable against
subsequent crashes/dips.

### Shock vs burden are independent

A day can be high shock without high burden ("burst day with no
recent history") or high burden without a high-shock day ("steady
two-week push, no spike day"). Crash-precursor tests will compare
shock and burden separately.

## Caveats

- **Baseline definition matters.** 30-day window is a defensible
  choice — long enough to be stable, short enough to track envelope
  shifts. Other windows (14d, 60d, 90d) are reasonable; we lock 30d
  here to avoid post-hoc selection.
- **Boundary days** (first ~20 days of corpus) yield empty rank
  scores. These default to `none` on their axis. Affects ~20 days
  total.
- **Composite max() rule biases up.** Any one axis can escalate.
  This is the PEM-safe direction — better to over-flag than
  under-flag exertion — but downstream tests should report both
  composite distribution and per-axis distributions.
- **Push burden uses days at rank ≥ 0.75 only.** Days below
  median rank don't reduce burden (rest doesn't "pay back" prior
  push directly; the body integrates rest separately). May need
  revision if downstream analysis shows below-median days should
  count toward recovery / lower push burden.
- **Universal vs participant-specific thresholds.** The rank
  cutoffs (0.5/0.75/0.85/0.95) are universal across PEM patients
  — encoding "where in the upper tail of YOUR recent days does
  today sit?" This is the principled fix to the v1 absolute-
  threshold trap (athletic norms baked in). Cutoffs themselves
  are not calibrated to crash labels.

## Lock status

**LOCKED 2026-06-06** as v3.1 (percentile-rank +
push_burden_class deprecated). Verified by:
- Inspection of class distributions (this file)
- Driving-axis attribution (script 04 output)
- Visual review of `timeline_with_activity.png` and
  `baseline_trajectories.png`
- Sensitivity test (`sensitivity_report.md`):
  - `exertion_class` is ROBUST (heavy+very_heavy Jaccard
    ≥0.78 across all parameter variations)
  - `push_burden_7d` underlying ranking is ROBUST (Spearman
    rank correlation 0.957–0.985 across baseline windows)
  - `push_burden_class` very_heavy binning was SENSITIVE → class
    deprecated, raw count retained

Any subsequent change to axes, thresholds, push-burden rule, or
reintroduction of push_burden_class binning creates
`severity_spec_v4.md` and triggers re-run of all downstream
classifications + analyses.

## Lagged baseline + trend slope (v3.2 extension — 2026-06-06)

**This is an additive extension to v3.1, not a redefinition.** The
locked v3.1 columns (`effective_exertion_rank_30d`,
`exertion_class`, `push_burden_7d`, per-axis class columns)
remain unchanged; the v3.2 columns are appended alongside them.
The v3.1 Lock status above continues to hold for the original
columns. Downstream tests opt into the lagged columns explicitly.

### Motivation
Adopted in response to user's Part 1 critique on 2026-06-06:
the 30-day rolling rank in v3.1 absorbs sustained creeps into
its own reference frame, so `push_burden_7d`'s discriminative
power is least where the risk is highest — the slower and more
dangerous the push, the more completely the baseline absorbs it.
That is a monotonic bias in exactly the wrong direction.

The root cause is that two incompatible jobs were asked of one
construct:
- *Recent normal* (short-horizon, rolling) — what `exertion_class`
  needs, and is correct for.
- *Sustainable floor / envelope* (anchored to stable or recovered
  periods) — what `push_burden_7d` needs, and was borrowing the
  first.

Two complementary metrics fix this, each picked on theoretical
grounds for its own role (**not** a horse race between candidate
predictors — see § Why this is not p-hacking below).

### A.1 — Lagged baseline (`*_rank_lagged`)
For each of the four axes, percentile rank is recomputed against
days **[d-90, d-30]** — a 60-day window ending 30 days ago that
excludes the recent candidate region. Days with fewer than 40 of
60 prior values get empty rank.

New columns added by [scripts/11_compute_lagged_baseline.py](../scripts/11_compute_lagged_baseline.py):
- `effective_exertion_rank_lagged`
- `step_rank_lagged`
- `max_hr_rank_lagged`
- `vigorous_min_rank_lagged`
- `exertion_class_lagged` (composite max, same cutoffs as § Axes)
- `class_axis_*_lagged` (per-axis transparency, same cutoffs)
- `push_burden_7d_lagged` (count of last 7 days with
  `effective_exertion_rank_lagged ≥ 0.75`)

Push burden is the metric this fix is most aimed at: its job is
to measure "sustainable floor pressure," which requires anchoring
to periods *before* the recent push. A.1 gives it the right
reference frame.

### A.2 — Trend slope (`effective_exertion_slope_28d`)
OLS slope of log(1 + `effective_exertion_min`) regressed on day
index over the trailing 28 days (excluding today). Days with
fewer than 21 of 28 prior values get empty slope. Units:
log-units per day.

This is a **new metric** answering a different question than
push burden or exertion class:
- `push_burden_7d` asks "is your last week dense with heavy days?"
- `exertion_class` asks "where is today vs your recent norm?"
- `effective_exertion_slope_28d` asks "has your daily-load floor
  been creeping upward for weeks?"

Slope > +0.05 (≈5% daily growth, doubling in ~14 days) marks
sustained-creep-up candidates. Slope < -0.05 marks
sustained-decay-down candidates. Both extremes are descriptive
markers, not classification thresholds — downstream tests define
their own use.

### Audit trail and pre-commitments (per the D5 honesty discipline)
A.1 and A.2 were adopted on **2026-06-06** in response to the
user's Part 1 critique dated **before** any rerun result existed.
This ordering is the anchor against motivated rescue: A.1 was not
adopted because HA02 was refuted; it was adopted because the
baseline construction has an identified methodological bug.

**Pre-committed SUPPORTED bar for the bundled HA02c +
HA01b-recomputed re-test (run on A.1 lagged baseline):**
- Frequency ≥ 60% of crash episodes in the test window
- Discrimination ≥ +15 pp above the null base rate
- Same bar as original HA01 / H02b. No relaxation, no tightening.

If HA01b-recomputed falls below +15 pp discrimination on the
lagged baseline, the addendum's "first SUPPORTED validate-era
precursor" headline softens accordingly. Symmetric re-test
discipline: re-testing only the refutation while keeping the
win as-is would be selective rescue.

### Why this is not p-hacking
A.1 fixes `push_burden_7d`'s contamination bug — same metric,
different reference frame, principled fix. A.2 is a new metric
for a different physiological pattern (creeping floor), not a
competitor to A.1. A.3 (dual-EWMA architectural unification)
reserved as a later refactor option. Each picked on theoretical
grounds, not on which makes the downstream HA test strongest —
they are not horses in a race, they are tools for different
jobs.

### Caveats specific to v3.2
- **Boundary days widen.** v3.1 has ~20 boundary days at the
  start of the corpus where the 30-day rolling rank is empty.
  v3.2 boundary widens to ~90 days because the lagged window
  ends 30 days ago. Affects the first ~3 months of the corpus.
- **Slope on zero-heavy distributions is noisy.** When the
  trailing 28-day window is dominated by zeros, the OLS slope
  is near zero regardless of true trend. The `log1p` transform
  helps but does not eliminate this; treat near-zero slopes
  on low-activity stretches with caution.
- **A.1 inherits the lock window quirk.** Days 30-90 ago are
  themselves potentially contaminated by older creeps. The
  lagged trick is the best available dodge, not a clean
  solution — it gives timescale separation (durable shifts
  rebase over months; transient pushes do not enter the
  lagged window for ~3 weeks), but the fundamental measurement
  problem that "the patient's history is the only reference
  available, and that history overlaps with the very process
  being detected" remains.
