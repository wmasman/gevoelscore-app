# S02 — Score trajectory: notes

**Status: descriptive trajectory analysis (no support/refute verdict),
plus one pre-registered statistical test (§3.8) and four pre-registered
S02b triggers (§7.2). Spec at [hypothesis.md](hypothesis.md).
Executed 2026-06-07.**

> **Forward cross-references (added 2026-06-07 after S02b + S02c
> executed same day).** T1's rolling-curve lead/lag pattern was tested
> at daily resolution in [S02b](../S02b-score-lead/notes.md) and
> **REFUTED**: the score-leads-Garmin pattern is a smoothing-induced
> trajectory-level phenomenon, NOT a daily-resolution signal.
> T2's May 2026 channel divergence was characterised at daily
> resolution in [S02c](../S02c-may2026-divergence/notes.md): against
> the recent 180-day baseline (not S01's 5-year σ), only RHR shows
> a weak directional drift; the other three Garmin channels are
> "essentially unmoved" and the composite divergence vs score is just
> +0.32σ. **Read T1 and T2 below in light of these follow-ups; the
> trajectory-level descriptions remain accurate but the
> causal/predictive readings are constrained by S02b's refutation and
> S02c's nuance.**

Plot: [score-trajectory-with-S01.png](score-trajectory-with-S01.png).
Normalised companion: [score-vs-garmin-normalised.png](score-vs-garmin-normalised.png).
Data: [trajectories_score.csv](trajectories_score.csv) (rolling
summaries), [correlation_results.csv](correlation_results.csv)
(§3.8 ρ + CI). Execution log: [execution-log.txt](execution-log.txt).

The score-side pendulum, plotted on the same x-axis as S01's
four-metric Garmin pendulum. 184 anchors across 2022-12-02 → 2026-06-05,
90-day window, 7-day cadence, methodology identical to S01.

**Two pre-registered triggers fired** (T1 inflection-date mismatch +
T2 May 2026 channel-divergence). S02b is therefore on the queue — but
the SHAPE of what fired matters: not the patient-narrative
"subjective recovery lags biometric" pattern T3 was set up for, but
the **opposite** direction. The score is *ahead* of the Garmin
pendulum at both turnaround points, and the May 2026 Garmin
perturbation does not appear in the score channel at all.

## Selected anchor-date table

Anchors aligned as closely as possible to S01's published anchor
dates so the two trajectories can be read side-by-side at a glance.
Score columns blank pre-tracking. The last anchor's `mean` (4.72)
is **the highest value in the entire window**.

| anchor (S02) | anchor (S01) | n | mean (10/10 trim) | median | p1 | p2 | p3 | p4 | p5 | p6 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| — | 2021-11-14 *(pre-LC)* | — | — | — | — | — | — | — | — | — |
| — | 2022-06-12 *(post-dx, pre-track)* | — | — | — | — | — | — | — | — | — |
| 2022-12-16 | 2023-01-08 | 90 | 4.347 | 4.0 | 0.022 | 0.056 | 0.122 | 0.322 | 0.456 | 0.022 |
| 2023-01-27 *(SCORE PEAK)* | — | 90 | **4.611** | 5.0 | 0.000 | 0.011 | 0.122 | 0.211 | 0.611 | 0.044 |
| 2023-08-04 | 2023-08-06 | 90 | 4.361 | 4.0 | 0.000 | 0.022 | 0.178 | 0.311 | 0.444 | 0.044 |
| 2024-03-01 | 2024-03-03 | 90 | **3.833** ← within-window dip | 4.0 | 0.000 | 0.044 | 0.256 | 0.533 | 0.156 | 0.011 |
| 2024-09-27 | 2024-09-29 | 90 | 4.569 | 5.0 | 0.000 | 0.011 | 0.089 | 0.344 | 0.533 | 0.022 |
| 2025-01-10 *(SCORE TROUGH)* | — | 90 | **4.319** | 5.0 | 0.000 | 0.022 | 0.122 | 0.456 | 0.378 | 0.022 |
| 2025-04-25 | 2025-04-27 | 90 | 4.556 | 5.0 | 0.000 | 0.000 | 0.056 | 0.400 | 0.522 | 0.022 |
| 2025-11-21 | 2025-11-23 | 90 | 4.792 | 5.0 | 0.000 | 0.000 | 0.044 | 0.267 | 0.544 | 0.144 |
| 2026-05-29 | 2026-05-31 | 90 | 4.681 | 5.0 | 0.000 | 0.011 | 0.056 | 0.311 | 0.500 | 0.122 |
| **2026-06-05** *(LAST)* | — | 90 | **4.722** ← all-time high | 5.0 | 0.000 | 0.011 | 0.056 | 0.300 | 0.511 | 0.122 |

## Per-statistic reading

**Trimmed mean** (1–6 scale, 10/10 trim — "centre of the typical-day
band"). Three-phase trajectory: rise to **4.61 peak in late Jan 2023**,
fall through 2024 to **4.32 trough in Jan 2025**, then rise again to
**4.72 at the corpus edge — highest value in the whole window**.
Range across the trajectory: 0.46 points (3.83 to 4.79). The mid-period
3.83 anchor (March 2024) is the only sub-4.0 reading and corresponds
to a real distributional shift (see below), not noise.

**Median** (untrimmed, ordinal-respecting). On a 1–6 discrete scale
the median is integer-valued and the step plot makes this visible.
The median **transitions from 4 → 5 around mid-2023 and stays at 5
for nearly the entire post-2023 window**, including throughout the
2024-2025 mean dip. Mean-median divergence ranges from 0 to 0.61 —
**never reaches 1.0**; T4 not fired. The divergence between mean=4.32
(below 4.5) and median=5.0 at the 2025-01-10 trough is the most
striking visual mean-median gap; reads as "the typical-day band sat
below the median because a meaningful tail of score=3-4 days pulled
the mean down even though more than half the in-window days were
score=5."

**Score-level distribution** (stacked area).
- **Score=1 days are essentially absent throughout** — never above
  2.2% of any window (the 2022-12-16 anchor). Most anchors are 0%.
- **Score=2 days are rare** — peak at 5.6% in the early window,
  effectively 0% from mid-2023 onwards.
- **Score=3 declines steadily**: 12% → 4-5% by late 2025.
- **Score=4 is volatile**: 32% → peak 53% in March 2024 (the dip
  period) → 31% at last anchor. The March 2024 spike in score=4 share
  IS the mean dip.
- **Score=5 rises overall**: 46% → 50-54% by late 2025.
- **Score=6 days emerge late**: 2% throughout the early window,
  then 12-14% from late 2025 onwards. **This is a new mode** —
  before 2025 these were rare; in the last year they're the
  third-most-common score after 5 and 4.

**Both level shift AND distribution shift are happening** (answers §4
question 3 — see below). The level shift (mean from 4.35 → 4.72) is
real but small. The distributional shift is more dramatic: the
*shape* of the typical 90-day window has changed from
[2% / 6% / 12% / 32% / 46% / 2%] in late 2022 to
[0% / 1% / 6% / 30% / 51% / 12%] in mid-2026 — score=2 and score=3
shares roughly halved or quartered, score=6 share grew 6×.

## §3.8 same-day rank correlation result

Primary test (Spearman ρ between daily score and daily avg stress,
2022-09-03 → 2026-06-05, block-bootstrap CI with 90-day blocks ×
10 000 iter, n=1359 pairs, ~16 effective blocks):

| channel | role | ρ | 95% CI | n_eff blocks | verdict |
|---|---|---:|---|---:|---|
| **avg stress** | **primary** | **−0.0557** | **[−0.1637, +0.0090]** | 16 | **ambiguous; underpowered at this resolution** |
| RHR | exploratory | +0.0203 | [−0.1498, +0.0810] | 16 | no detectable daily co-variation |
| sleep efficiency | exploratory | +0.0642 | [−0.0015, +0.1291] | 15 | no detectable daily co-variation |
| max-spike minutes | exploratory | +0.0425 | [−0.0256, +0.0931] | 16 | no detectable daily co-variation |

**Reading.** All four channels are flat at daily resolution. The
primary ρ = −0.0557 has the expected sign (better day ↔ less stress)
but the 95% CI spans 0 (slightly: upper edge at +0.009), so we cannot
exclude "no relationship." All three secondaries are in the
"|ρ| < 0.10 with CI inside ±0.15" verdict — no detectable
co-variation. The sleep-efficiency CI has its upper edge at +0.129
(very close to the +0.15 boundary), so among the secondaries it has
the most suggestive direction (slightly positive: better day ↔
higher sleep efficiency), but still inside the locked "no detectable"
band.

**Sign-check on the primary**: ρ < 0 is the expected direction; no
reframe candidate triggered. The exploratory channels do not have
pre-committed expected signs and carry no verdict; their positive
signs (especially max-spike at +0.04) would be counter-intuitive if
they were large, but at this magnitude they are within sampling noise.

**What this tells us combined with the trigger results below**:
the score and Garmin channels track largely DIFFERENT state at the
day-to-day timescale. The trajectory-level (90-day rolling) curves
visually share a pendulum shape but the underlying daily series
don't co-vary in any of the four channels measured. This is the
methodologically-correct way to surface "they look similar at year
scale but they're not measuring the same daily phenomenon" — without
the smoothing-induced correlation that a naive test on the rolling
curves would have manufactured.

## §7.2 trigger panel

| trigger | result | numbers |
|---|---|---|
| **T1** — inflection-date mismatch (≥ 91 days) | **FIRED at trajectory level; REFUTED at daily resolution by [S02b](../S02b-score-lead/notes.md)** | score peak 2023-01-27 vs avg-stress peak 2023-06-25 (Δ = **149 d**); score trough 2025-01-10 vs max-spike trough 2025-04-20 (Δ = **100 d**). S02b primary ρ_lag at +149d = +0.099 (CI [+0.035, +0.203]) vs matched same-day ρ = −0.097; |delta| = +0.002 (criterion-c bar 0.10). The trajectory-level mismatch is real but does NOT reflect a daily-resolution lead/lag signal. |
| **T2** — May 2026 channel divergence | **FIRED at trajectory level; NUANCED at daily resolution by [S02c](../S02c-may2026-divergence/notes.md)** | At S02 trajectory σ: visible in 3/4 S01 metrics; not visible in either score view. At S02c's recent 180-day daily σ: only RHR shows directional drift (z_mean +0.82, onset 2026-05-14); other Garmin channels all "essentially unmoved" (avg_stress +0.24, max_spike +0.16, sleep eff +0.00σ); score +0.07σ; composite gap vs score = +0.32σ. The "channels diverging" framing holds directionally but is small in σ-units against the recent baseline. |
| **T3** — score lags Garmin throughout post-stabilisation | **not fired** | vs avg stress: gap ≥ 0.20 in 21.3% of 61 anchors, mean gap = **−0.067**; vs max-spike: gap ≥ 0.20 in 34.4%, mean gap = +0.019 |
| **T4** — sustained mean-median divergence (≥ 1.0, ≥ 5 anchors) | **not fired** | max consecutive ≥ 1.0 run = 0 anchors; max divergence anywhere = 0.611 |

**T3 conservative-bar reading** (per §7.2 spec rule). The strict bar
does not fire, but the diagnostic numbers tell the opposite story
from what T3 was constructed to detect. Mean gap against avg-stress
is **negative** (−0.067), meaning on average across the 61 lag-window
anchors the SCORE is at a slightly higher recovery percentile than
avg-stress is — score-ahead-of-Garmin, not Garmin-ahead-of-score.
Mean gap against max-spike is essentially zero (+0.019). Neither
direction holds at the ≥ 0.20 / ≥ 80% bar, but the normalised-scale
figure ([score-vs-garmin-normalised.png](score-vs-garmin-normalised.png))
does show the **score curves running at higher recovery-pctl than
the Garmin curves** through the bulk of 2024-2025 — consistent
with T1's "score peaks/troughs first" finding and inconsistent with
the Wiggers/patient-narrative direction. We are explicitly NOT
treating this as "T3 fired" because it didn't meet the locked bar
and the diagnostic mean gap doesn't fire any S02b trigger on its
own. But it is **the direction of the persistent visual gap** and
notes.md is the place to log that, per the §7.2 conservative-bar rule.

**S02b is therefore triggered (T1 + T2 fired).** S02b's shape should
address the score-leads-Garmin direction (T1) and the May 2026
absence (T2), not the patient-narrative direction.

## Answers to the five §4 questions

### Q1 — Does the score trajectory inflect at the same date(s) as the Garmin pendulum?

**No** — the score's algorithmically picked turnaround dates are
**earlier than S01's on the peak axis** and **earlier than max-spike's
on the trough axis**, both at meaningful (≥ 91-day) deltas.

- Score peak: **2023-01-27** (mean = 4.611, the system's "best
  stretch" by central tendency). This is *before* the LC stabilisation
  peak in any of the four Garmin metrics:
  - avg stress peak: 2023-06-25 (Δ = 149 d, **T1 FIRES**)
  - max-spike peak: 2023-04-02 (Δ = 65 d, below T1 bar but
    same-direction lead)
  - RHR peak: 2024-02-11 (more than a year later)
  - sleep efficiency peak: 2024-05-05 (more than a year later)
- Score trough: **2025-01-10** (mean = 4.319). Close to avg-stress's
  trough (2024-12-22, Δ = 19 d — coincident) but earlier than
  max-spike's:
  - max-spike trough: 2025-04-20 (Δ = 100 d, **T1 FIRES**)
  - RHR trough: 2024-07-21 (sym slightly different shape — RHR's
    minimum is in mid-2024, well before either score or stress)
  - sleep efficiency trough: 2024-09-15 (different shape)

**Reading**: at both turnaround points, the score channel is moving
before the Garmin sympathetic-arousal channels follow. The pattern
is most distinct against avg-stress (149-day peak-lead) and
max-spike (100-day trough-lead). RHR and sleep efficiency have
turnaround dates that aren't naturally comparable here — RHR's
extremum is in mid-2024 (a different kind of curve), and sleep
efficiency is nearly flat (σ = 0.0018 — the smallest σ of any
channel by two orders of magnitude).

### Q2 — Mean vs median divergence

**Bounded, never sustained at ≥ 1.0** (T4 does not fire). Maximum
divergence anywhere = 0.611. The pattern: **median is at 5
throughout nearly the entire post-2023 window**, while the trimmed
mean wanders between 3.83 and 4.79. The divergence is **largest
during the 2024-2025 dip period**: at the 2025-01-10 trough,
mean = 4.32 and median = 5 (Δ = 0.68). The divergence is in the
direction of **mean below median** at most anchors — signalling a
left-skewed in-window distribution: a tail of score=3 and score=4
days pulling the average below the central 5-mode.

This is itself a finding: across most of the trajectory the
**modal day is a score=5 day**, but the meaningful presence of
score=3 days and the volatility of score=4 days drags the trimmed
mean down to 4-4.5.

### Q3 — Distribution shift vs level shift

**Both, with the distribution shift being the more dramatic
component.** Comparing the first and last full-window anchors:

| score | early (2022-12-16) | late (2026-06-05) | change |
|---:|---:|---:|---:|
| 1 | 2.2% | 0.0% | −2.2 pp |
| 2 | 5.6% | 1.1% | −4.5 pp |
| 3 | 12.2% | 5.6% | −6.6 pp |
| 4 | 32.2% | 30.0% | −2.2 pp |
| 5 | 45.6% | 51.1% | +5.5 pp |
| 6 | 2.2% | 12.2% | **+10.0 pp** |

- **Tail-collapse on the worst end is real**: score≤3 share drops
  from 20% → 7% (a 65% relative reduction).
- **score=4 share is roughly stable** (32% → 30%) — the distribution
  isn't a clean "shift by one notch right" pattern.
- **score=6 share grows 6×** (2.2% → 12.2%) — this is the most
  dramatic single change in the entire distribution. score=6 days
  were rare events early on; they are now the third-most-common
  score behind 5 and 4.

**Shape interpretation**: the worst tail (score 1-3) is being
*eroded*, the middle (score=4) is *stable*, and a new upper mode at
score=6 is *growing*. The level statistics (mean) move modestly
because the distribution is rebalancing inside the trim region —
score=3 days converting to score=5/6 days. The stacked-area panel
of [the main PNG](score-trajectory-with-S01.png) shows this
visually: the dark-bottom layers thin and a light-top layer
emerges in 2025-2026.

### Q4 — The May–June 2026 perturbation

**Visible in 3/4 Garmin metrics (S01); NOT visible in either score
view.** Both views agree on the score side, which is itself useful
(it means the absence in the 90d view isn't a boundary-blur
artefact — the zoom strip also shows score going UP, not down).

S01 perturbation (each metric, last anchor vs trough + 1 σ):
- avg stress: +4.92 above trough (σ = 2.51) → **visible**
- max-spike minutes: +5.73 above trough (σ = 2.31) → **visible**
- RHR: +7.14 above trough (σ = 2.20) → **visible**
- sleep efficiency: −0.0022 below trough (σ = 0.0018) → not visible

Score (last anchor vs trough − 1 σ in worsening direction):
- 90d view: trough = 4.319, σ = 0.280, last = 4.722. The last
  anchor is **+0.403 ABOVE trough** (recovery direction) — the score
  is at its all-time high, not perturbing. **Not visible.**
- Zoom strip (last ~6 months): 30d-mean today = 4.60;
  30d-mean 90 days earlier = 4.23. **Δ = +0.37 in recovery
  direction**. Score has been *improving* across the period the
  Garmin metrics have been perturbing.

**This is T2 firing in the "forward" direction** — Garmin sees
something the score does not. Three independent Garmin channels are
elevated against their own variability; both score views (the
smoothed 90d and the high-resolution zoom) show the score *moving
the other way*. The score is currently the most positive it has been
in the entire window.

What this could mean (descriptive, NOT mechanistic):
- The Garmin perturbation may reflect a recent stressor the
  participant's subjective state has metabolised positively (e.g.
  excitement, anticipation, productive activity);
- Or it reflects a physiological signal whose subjective component
  is delayed beyond the 30-day zoom window;
- Or the score's "good stretch" framing has expanded — a score=5 in
  June 2026 may carry different meaning than a score=5 in early 2023.
- Or measurement drift on either channel.

S02 does not resolve these. **S02b T2-shape would address this
directly with raw daily data, no smoothing.**

### Q5 — The "no pre-illness anchor" caveat

The score's "best stretch" (4.79 in late 2025) and the score's
"highest single anchor" (4.72 last week) are the highest values in
the tracked window. They are **NOT a "return to healthy."** No
pre-illness score baseline exists; the tracked window begins
2022-09-03, 4 months after the LC diagnosis (2022-05-06). The
"highest value in the tracked window" is "least-burdened period
inside the post-diagnosis tracked stretch" — possibly substantially
below a hypothetical pre-illness baseline that we have no data on.

This is an asymmetry compared with S01: the Garmin pendulum has a
pre-LC RHR baseline of 55.1 (similar to the recent ~57-58 readings),
suggesting the body's *resting* state has not moved much from a
healthy reference. The score has no such reference and cannot make
that comparison. Stabilisation framing reframes this honestly but
does not remove the asymmetry.

## The recent uptick — both views

**90-day view**: the score trimmed mean rose from a Jan 2025 trough
of 4.32 to 4.79 by Nov 2025 and 4.72 at the corpus edge. This is a
**0.40-point sustained rise over 16 months**, well above the
methodology's "noise" threshold of 0.2 (§6 caveats). The lower-end
tail (score=3) shrank from 12% to 6%; the upper-end tail (score=6)
grew from 2% to 12%.

**Zoom strip** (last 6 months at daily resolution): the 30d rolling
mean was 4.23 in early March 2026 and is 4.60 in early June 2026 —
a **0.37-point rise in 90 days**, consistent direction with the 90d
view. The daily scatter shows score=5 and score=4 dominate the
recent window; very few score=3 days; multiple score=6 days
clustered in late April through May.

**Boundary-effect note**: the last 90-day window (March–June 2026)
is the period where Garmin shows its perturbation. The score's
positive trajectory through this exact period is *not* a boundary
artefact — both the 90d view and the zoom strip agree on the
direction (improvement) and magnitude (~0.4 point). The
boundary-effect caveat (§6) is real but does not apply here because
both views resolve the same dynamics.

## Methodology notes

- **Anchor-grid offset between S01 and S02**: S01's anchors started
  2021-11-14 (90 days after Garmin start); S02's started 2022-12-02
  (90 days after score start). The grids are both 7-day cadenced but
  offset by 5 days mod 7 — they never coincide. T3 evaluation
  therefore linear-interpolates S01's trajectory onto S02's anchor
  grid (max interpolation distance: 3 days; small versus the 90-day
  smoothing window). Documented in
  [compute_trajectories.py](compute_trajectories.py)
  `interpolate_at()` docstring.
- **Trim mechanics caveat (§3.5)**: on a discrete 1–6 scale, 10/10
  trim removes outlier *days* (the bottom and top ~9 score values),
  not outlier *values* as in a 0–100 stress scale. The trim
  consistently chops the worst score=1/2 days and the best score=6
  days from the window's average. Across the trajectory this is
  doing roughly the right thing for "centre of the typical-day
  band" but it does mean the upward growth of score=6 days
  (2.2% → 12.2%) is partly invisible in the trimmed mean — those
  days are mostly being trimmed out. The distribution panel
  surfaces what the mean smooths over.
- **Singleton dips**: 34 isolated dips are rendered as low-opacity
  ticks on the bottom margin of panel 3 (alpha 0.20, per spec
  §3.7). At the chosen alpha they don't obscure the cluster
  signal; not falling back to omission.
- **§3.8 effective-blocks caveat**: with 90-day blocks across ~1.360
  pairs, ~15-16 effective independent blocks. CIs are
  correspondingly wide. The "ambiguous; underpowered" verdict on
  the primary is exactly what the spec's effective-blocks caveat
  predicted.

## Caveats

- **Ordinal not interval.** Trimmed mean treats the 1-6 scale as
  approximately interval; median preserves ordinality. Reported
  together; the divergence between them is the answer to Q2.
- **Self-report under brainfog.** A 0.2-point shift on the 1-6
  scale over 90 days is within day-to-day noise. The 0.4-point shift
  documented above is above that threshold.
- **No pre-illness anchor.** The "highest in window" reading is
  framed as least-burdened period in tracked window, NOT healthy
  reference. See Q5.
- **Boundary effect at last anchor.** The 90d view absorbs
  April-June 2026 into one smoothed value. Zoom strip exists as the
  methodological-honesty response (§5.2 spec). Both agree here.
- **Trim mechanics differ from S01's** (§3.5 + above) — relevant for
  reading the trimmed mean's small magnitude of change against the
  larger distributional change.
- **§3.8 underpowered.** 15-16 effective blocks limits ρ-detection.
  The "ambiguous; underpowered" verdict on the primary should not
  be read as "the channels co-vary" — only as "we cannot exclude
  small co-variation at this sample size." The point estimate is
  small (−0.06) and the lower edge of the CI is at −0.16, so the
  evidence is consistent with anything from negligible-negative
  to no-relationship. A future S02b daily-resolution test with
  more iterations or a different block length would not change
  this fundamental power limit.

## What this enables

This is the empirical foundation for the **score-side panel of the
stabilisation-arc card** referenced in
[QUEUED-WORK.md §C.5](../../QUEUED-WORK.md). Concrete card-shape
findings now backed by data:

- "Your *worst stretches* are getting rarer — score=3 days dropped
  from 12% to 6% across the tracked window; score=2 days from 6% to
  1%; score=1 days have effectively disappeared."
- "Your *best stretches* are emerging — score=6 days were 2% of
  your in-window days early on; they're now 12%."
- "Your typical day's central-tendency moves slowly (a 0.4-point
  rise over 16 months), but the *shape* of your typical week has
  changed substantially."

These card-shape sentences are descriptive, retrospective, and
respect the participant's lived experience. Not predictive. They
also frame the change as "shape of the typical week" rather than
"trajectory of recovery," in keeping with the
[recovery_trajectory project memory](../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/project_recovery_trajectory.md)
note that the user prefers stabilisation framing.

## What this does NOT do

- Does not predict whether the recent rise will continue.
- Does not predict whether the May 2026 Garmin perturbation will
  eventually reach the score channel.
- Does not test correlation between the score-trajectory shape and
  the Garmin-trajectory shape statistically (the daily-resolution
  §3.8 test was null; a trajectory-level test would be
  smoothing-inflated and is correctly deferred — see hypothesis.md
  §3.8 reasoning).
- Does not establish causation for any observed pattern.
- Does not generalise to other users.
- Does not reframe crash_v1 or crash_v2 — the locked train/validate
  split remains analytical, even though the score's algorithmically
  picked peak (Jan 2023) and trough (Jan 2025) make the
  "score-side stabilisation arc" visible.
- Does not declare a new era boundary even though the algorithmic
  turnaround dates surface them clearly.

## S02b + S02c — both executed same day (2026-06-07)

T1 and T2 both fired at trajectory level. Two sibling follow-ups
were pre-registered, executed, and documented same-day:

- **[S02b score-lead lagged correlation](../S02b-score-lead/notes.md)** —
  daily-resolution Spearman ρ at the pre-committed lag values (+149d
  for avg stress, +100d for max-spike); pre-committed bar (mag ≥ 0.20,
  CI excludes 0, lag improves over same-day by ≥ 0.10, expected sign
  negative). **REFUTED** on criterion (c): primary lagged ρ = +0.099
  vs matched same-day ρ = −0.097, |delta| = +0.002. The trajectory-
  level T1 pattern does NOT survive at daily resolution. First direct
  cross-correlation lag test for Wiggers H1.
- **[S02c May 2026 channel divergence](../S02c-may2026-divergence/notes.md)** —
  daily-resolution z-score characterisation against a 180-day recent
  reference window. Only RHR has an algorithmic onset (2026-05-14)
  and even RHR is below the locked 1.0σ "visibly worsening" bar.
  Other Garmin channels and score are "essentially unmoved" against
  recent baseline. Composite Garmin-worsen vs score gap = **+0.324σ**
  (directional but small).

**Combined reading**: at daily resolution, score and Garmin channels
live on largely-independent recent baselines. T1 and T2 are
trajectory-level findings about how the 90-day-rolling curves behave;
neither extends to a daily-resolution signal. Methodology lesson
banked: rolling-curve turnaround-date mismatches and σ-vs-trough
perturbation flags do NOT automatically imply daily-resolution
patterns. Future trajectory comparisons should cite this constraint
before claiming daily-resolution implications.

---

*S02 executed 2026-06-07. Spec at [hypothesis.md](hypothesis.md);
revision dated same-day pre-data per peer-review feedback. CSVs and
PNGs in this folder are re-runnable; trajectory lengthens naturally
as score data is added.*
