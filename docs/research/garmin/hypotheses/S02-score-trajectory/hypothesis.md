# S02 — Score trajectory: pre-registered spec

**Pre-registration written 2026-06-07, before `compute_trajectories.py`
runs against any data. Revised same day per peer-review feedback,
still before any data inspection (revisions tighten §3.8, §5.2, §7,
§8 — see git history). Locked. Any further change AFTER data
inspection creates `S02-revised/` as a new folder; this spec is not
edited in place beyond the same-day pre-data revisions just landed.**

**Status**: pending. Descriptive trajectory analysis, no support/refute
verdict. Companion piece to S01
([S01-stabilisation-trajectories](../S01-stabilisation-trajectories/notes.md)).

---

## 1. Purpose

S01 plotted the pendulum on four Garmin metrics (RHR, avg stress, sleep
efficiency, max stress-spike duration). S02 plots the same pendulum
shape on the **outcome variable itself** — daily gevoelscore — using
methodology identical to S01 so the two trajectories can be read
directly against each other on a shared x-axis.

This is descriptive characterisation. The piece answers five locked
questions (§4) about what the score trajectory looks like across the
tracked window. It does not test crash precursors, predict the
May 2026 perturbation, or carry support/refute language. Surprise
thresholds for triggering an S02b lead/lag follow-up are pre-committed
in §7 to prevent motivated reasoning post-hoc.

## 2. Scope

In scope:
- Daily gevoelscore (1–6 ordinal) across 2022-09-03 → corpus end
  (currently 2026-06-05).
- Three rolling summaries per anchor: trimmed mean, median, score-level
  distribution.
- Visual overlay with S01's four trajectories on a shared x-axis,
  plus a companion **normalised-scale figure** (§5.2a) that puts
  all six curves on a 0–1 recovery-direction y-axis for visual
  lead/lag inspection.
- Crash-start markers, dip-cluster shaded bands, and **singleton-dip
  low-opacity ticks** on the time axis (three visual weight tiers,
  sourced from
  [crash_v2-definition/labels_crash_v2.csv](../crash_v2-definition/labels_crash_v2.csv)).
- A small companion "zoom strip" of the last ~6 months at daily
  resolution to address the 90d window's boundary blur.
- **One pre-registered same-day rank correlation** (Spearman ρ) between
  daily score and daily avg stress with block-bootstrap CI, plus three
  exploratory rank correlations against S01's other channels (§3.8).
  Added 2026-06-07 after participant request to attach a defensible
  number to the "do these channels co-vary" question; pre-committed
  interpretation rules locked in §3.8 before any data inspection.

Out of scope (locked):
- No notes, tags, or calendar data. Score only by design.
- **No tests of lead/lag, shape similarity at multi-year arc scale, or
  channel-divergence on the May 2026 perturbation.** Lead/lag and
  channel-divergence are deferred to S02b conditional on §7
  surprise-trigger firing; multi-year shape similarity is answered by
  the visual overlay, not by a statistic. The one same-day rank
  correlation in §3.8 is the only statistical test in S02.
- No prediction or forecasting of the May 2026 perturbation.
- No reframing of crash_v1 / crash_v2.
- No retroactive rewriting of the train/validate split, even if an
  inflection date is visually obvious. The 2023-12-31 cut remains
  analytical-not-physiological per registry §1.
- **No volatility (rolling 30d std) or dip-frequency metric.** These
  are queued separately as
  [C.5](../../../QUEUED-WORK.md#c5--volatility--dip-frequency-progress-metric-descriptive)
  and are a *progress* framing of the pendulum; S02 is the
  *level/distribution* framing. notes.md will cross-reference C.5 so
  neither piece silently forgets the other.

## 3. Methodology — locked

### 3.1 Data source

`day_entries.csv` (copied per-hypothesis-folder per project
convention). Columns used: `date`, `score`. Preflight
([00-crash_v1-counts](../00-crash_v1-counts/counts.md)) confirmed 100%
coverage across the analysis window; ~1.372 rows expected.

### 3.2 Rolling-window parameters (identical to S01)

- Window: **90 days**.
- Anchor cadence: **every 7 days**.
- First anchor: **2022-12-02** (90 days after gevoelscore tracking
  start, so the first window is full).
- Last anchor: most recent date in `day_entries.csv`.

### 3.3 Three rolling statistics per anchor

- **Trimmed mean** — drop top/bottom 10% of the 90 in-window scores,
  take the mean of the remainder. Matches S01.
- **Median** — untrimmed 50th percentile of the 90 in-window scores.
  New for S02; preserves the ordinality of the 1–6 scale.
- **Score-level distribution** — for each score value v ∈ {1, 2, 3, 4,
  5, 6}, the proportion `p_v` of in-window days at exactly that score.
  Six proportions per anchor; sum to 1.0.

### 3.4 Why both trimmed mean AND median

- The score is ordinal, not interval. The trimmed mean treats it as
  approximately interval (defensible but not theoretically clean).
- The median respects ordinality but on a discrete 1–6 scale is
  integer or half-integer valued — visually a step function, not a
  smooth curve. That visual mismatch is *honoured* by the rendering
  choice in §5.2, not papered over.
- A divergence between mean and median is itself a finding (signals
  skew that one statistic smooths over). Both are reported. Neither
  is privileged.

### 3.5 Trim mechanics on a discrete 1–6 scale (methodology note)

A 10/10 trim chops the top/bottom 10% of in-window days. On the user's
distribution (~35.6% of days at score=4 per preflight), this trim
removes score=1 days from the low end and score=6 days from the high
end — a "robust-centre" statistic. Mechanically different from S01's
10/10 trim on the 0–100 stress scale, where 10/10 removes outlier
*values*; on the 1–6 score scale it removes outlier *days*. Both are
defensible; the difference is flagged in notes.md as a methodology
note, not a problem.

### 3.6 Reference vertical lines (on all panels)

- 2022-05-06 — LC diagnosis. Annotated, pre-tracking.
- 2022-09-03 — gevoelscore tracking start (score data begins).
- 2023-12-31 — analytical train/validate split. Labelled in the
  legend explicitly as **analytical, not physiological**.

The pre-LC interval (2021-08-16 → 2022-09-02 — Garmin data present,
score data absent) is annotated on the score panels with a "no score
data" band rather than left as an unexplained gap.

### 3.7 Event overlay (bottom panel only)

Source: [crash_v2-definition/labels_crash_v2.csv](../crash_v2-definition/labels_crash_v2.csv).

**Three visual weight tiers** so the reader sees clusters first but
the singleton density isn't invisible (revised from original
"singletons not marked" per peer review 2026-06-07, still pre-data):

- **Crash starts** (tier-1 crash episodes = crash_v1; first-day-of-
  episode rows only) — filled triangle markers (▲) at the bottom
  margin of the distribution panel, alpha=1.0. Highest visual
  weight.
- **Dip clusters** (`dip_cluster_id` non-null rows, collapsed to
  cluster start → cluster end) — shaded rectangular bands across
  the cluster date range, alpha=0.40. Medium visual weight.
- **Singleton dips** (isolated dips with `dip_cluster_id` null) —
  short vertical tick marks at the bottom margin, alpha=0.20.
  Lowest visual weight; reader scanning for cluster signal won't
  fixate on them, but a clustering of ticks near a perturbation
  phase will register. If post-data this clutters the plot enough
  that the cluster signal is obscured, the choice falls back to
  omission and the swap is logged in notes.md as a finding
  (per §8 audit-trail rule).

### 3.8 Same-day rank correlation with S01's Garmin channels (primary statistical test)

Added 2026-06-07 after participant request. The visual overlay alone
attaches no number to the question "do score and physiology co-vary
day-to-day?". This section locks one defensible number — and explains
why this specific shape, not the obvious alternatives.

**Why this test and not the others I rejected in the prior turn:**

- **Spearman ρ, not Pearson r.** The score is ordinal (1–6); Pearson
  assumes interval scaling. Spearman tests monotonic association
  without that assumption and survives the ordinal-not-interval
  caveat in §6.
- **Raw daily values, not rolling means.** The 90-day rolling mean
  shares ~87 of 90 days with its neighbour, so any naive test on the
  rolling values is inflated by shared smoothing — two independent
  random walks smoothed the same way will correlate above 0.7
  routinely. The honest place to compute the correlation is the
  underlying daily series.
- **Same-day, no lag scan.** A free lag scan over [−90, +90] days is
  180+ silent comparisons. Locked discipline elsewhere in the project
  (H02d's [D−4, D−1] from
  [activity-labels/output/lag_profile_report.md](../../activity-labels/output/lag_profile_report.md),
  HA10's window) chooses lag windows from an independent source
  before the test runs. No such source exists yet for
  score-vs-Garmin, so same-day is what can be done honestly. Lag is
  deferred to S02b per §7.
- **One primary channel + three exploratory secondaries, not four
  parallel tests.** Avg stress is the only S01 channel where
  [H02](../H02-stress-elevation/result.md) found train-era
  discrimination above null. It is the channel most likely to track
  score if anything does, and pre-committing to it as primary avoids
  cherry-picking after seeing all four numbers. RHR, sleep
  efficiency, and max-spike-minutes are reported as exploratory
  secondaries in the same table; their CIs are not verdict-bearing.
- **Block bootstrap CI, not naive sample CI.** Both series have
  strong temporal autocorrelation (multi-day crash episodes,
  multi-week stress runs). A naive CI under independence would be
  wildly too narrow. Block bootstrap with 90-day blocks resamples
  whole "rounds" of state, preserving within-block autocorrelation.
  90 days matches the project's rolling-window choice elsewhere
  (§3.2, S01).

**Test specification — locked:**

- **Series 1**: daily gevoelscore, 1–6 integer, from `day_entries.csv`.
- **Series 2 (primary)**: daily avg stress, UDS
  `allDayStress.aggregatorList[type=TOTAL].averageStressLevel`,
  loaded from the same UDS source S01 uses
  ([S01/compute_trajectories.py:53-77](../S01-stabilisation-trajectories/compute_trajectories.py#L53-L77)),
  **raw daily values, NOT the rolling mean**.
- **Window**: 2022-09-03 → corpus end. Days where either series is
  missing are dropped pairwise; report N excluded.
- **Statistic**: Spearman ρ.
- **Confidence interval**: 95%, **moving-block bootstrap, 90-day
  blocks, 10 000 iterations** (overlapping blocks sampled with
  replacement; for each iteration, sample ⌈N/90⌉ blocks, concatenate,
  truncate to N, recompute ρ).
- **Secondaries**: same construction, on UDS `restingHeartRate`,
  sleep efficiency (per
  [S01/compute_trajectories.py:80-107](../S01-stabilisation-trajectories/compute_trajectories.py#L80-L107)),
  and `max_spike_minutes` (from
  [H02b/daily_max_spike.csv](../H02b-stress-spikes/daily_max_spike.csv)).
  Reported alongside the primary; verdict applies only to the
  primary. **Holm-Bonferroni** correction is NOT applied because the
  secondaries are explicitly labelled exploratory and carry no
  verdict — the primary is the only test that "counts."

**Pre-committed interpretation rules** — locked before data; written
in advance so the number in notes.md is read against rules I committed
to *before* seeing it:

| ρ_primary | 95% CI | Locked reading in notes.md |
|---|---|---|
| ≥ 0.30 | excludes 0 | "score and avg stress co-vary detectably at daily resolution; both channels measure overlapping state" |
| ≥ 0.30 | spans 0 | "point estimate suggestive but underpowered at the effective sample size; cannot conclude" |
| 0.10 to 0.30 | any | "ambiguous; descriptive piece does not resolve the question at this resolution" |
| < 0.10 | contained within [−0.15, +0.15] | "score and avg stress do not detectably co-vary at daily resolution; the two channels track different state at the day-to-day timescale even where their 90d trajectories appear similar" |
| < 0 sign | excludes 0 | "score and avg stress are inversely related at daily resolution — surprising; flag for S02b reframe" |

Sign convention: higher score = better day; higher avg stress = more
sympathetic activation. Expected sign of the correlation if both
channels track sympathetic-arousal state is **negative** (better day
↔ less stress). The first row's "co-vary detectably" is therefore
about |ρ|, not sign — note the actual sign explicitly in notes.md.

Thresholds 0.30 / 0.10 are Cohen-style "moderate / negligible"
cutoffs adapted for rank correlation. Chosen before data inspection.
Do not drift.

**Effective sample size caveat — locked into notes.md:** with 90-day
blocks across ~1.370 valid pairs, the effective sample size for
inference is roughly ⌈1.370 / 90⌉ ≈ 15 independent blocks. Statistical
power for ρ detection is correspondingly limited; CIs will be wider
than the naive √N intuition suggests. The "underpowered" interpretation
row exists for exactly this reason. State the effective-blocks figure
explicitly in notes.md alongside the ρ and CI.

**What this test does NOT do, even if it fires:**
- Does not establish causation. Shared upstream confounders (cognitive
  load, infection, hormonal cycle) remain unaddressed.
- Does not address lead/lag (deferred to S02b per §7).
- Does not address multi-year arc shape similarity (the visual
  overlay answers that; this is the cross-sectional daily-resolution
  answer).
- Does not address whether the May 2026 perturbation is shared
  (deferred to S02b channel-divergence per §7).
- Does not generalise to other users.

## 4. Locked questions notes.md must answer

Pre-committed before any data inspection. Each gets a paragraph in
notes.md with a specific anchor-date or distributional observation, not
a hand-wave.

1. **Does the score trajectory inflect at the same date(s) as the
   Garmin pendulum?** Compare against S01's documented turnarounds
   (mid-2023 stress + spike peak; early-2025 trough). Report
   directionally; no statistical test.
2. **Mean vs median divergence.** Where do they diverge, by how much,
   and in which direction? Divergence signals distributional skew that
   either statistic alone smooths over.
3. **Distribution shift vs level shift.** Is the share of score=5 days
   rising at the expense of score=3 days? Or is the entire
   distribution shifting up by one notch? These are different
   stabilisation shapes and the stacked-area panel must distinguish
   them.
4. **The May–June 2026 perturbation.** Does it show in the 90-day
   mean/median (main panel)? Does it show in the zoom strip (last 6
   months at daily resolution)? **Different answers from the two views
   are themselves a finding** — and notes.md must acknowledge the
   boundary-effect limit on the 90d view's resolution near the corpus
   edge.
5. **No pre-illness anchor.** Unlike S01, the score has no healthy
   baseline. The "best" stretch of the curve is the participant's
   *lowest-symptom-burden window in the tracked period*, **not a
   healthy reference**. notes.md must state this clearly so the
   trajectory is not misread as "returned to healthy."

## 5. Outputs

### 5.1 `trajectories_score.csv`

Columns:
- `anchor_date`
- `n_in_window` (count of valid score days in the 90-day pre-anchor
  window; expected = 90 given 100% coverage, but report what the data
  shows)
- `score_trimmed_mean` (10/10 trim)
- `score_median` (untrimmed)
- `p1`, `p2`, `p3`, `p4`, `p5`, `p6` (proportions; sum = 1.0)

### 5.1a `correlation_results.csv`

One row per S01 channel tested in §3.8. Columns:
- `channel` (`avg_stress` | `rhr` | `sleep_efficiency` | `max_spike_minutes`)
- `role` (`primary` | `exploratory`)
- `n_pairs` (after pairwise drop of missing days)
- `n_excluded` (days dropped from each series)
- `n_effective_blocks` (⌈n_pairs / 90⌉ — the autocorrelation-corrected
  power figure)
- `spearman_rho`
- `ci95_lo`, `ci95_hi` (moving-block bootstrap, 90-day blocks, 10 000
  iter)
- `verdict_row` (the row label from §3.8's interpretation table; only
  the primary's verdict counts)

### 5.2 `score-trajectory-with-S01.png`

Three main panels + one zoom strip, sharing the x-axis.

- **Panel 1 (top)** — S01's four trajectories, re-rendered identically.
  Included for direct visual overlay; not re-computed (loaded from
  S01's `trajectories.csv`).
- **Panel 2 (middle)** — score trimmed mean rendered as a smooth solid
  line + score median rendered as a step plot
  (`drawstyle='steps-post'`) on a shared y-axis 1–6. The step
  rendering visually honours the fact that the median over 90 integer
  scores is intrinsically integer/half-integer valued while the
  trimmed mean is interpolated. Divergence between the two lines is
  the question #2 finding.
- **Panel 3 (bottom)** — stacked area of the six score-level
  proportions. Colour-graded score=1 (darkest) to score=6 (lightest)
  so "darkest = worst-day share." Crash-start markers + dip-cluster
  shaded spans on the bottom margin per §3.7.
- **Zoom strip (below panel 3, ~1/3 the height of a main panel)** —
  most recent ~6 months only (2025-12-01 → corpus end). Daily raw
  score as small scatter dots, rendered with **±0.15 random uniform
  jitter on the y-axis** to resolve overlap on the discrete 1–6
  scale (otherwise ~180 dots stack on 6 horizontal lines and visually
  lie about density). **RNG seed locked at 42** for reproducibility.
  30-day rolling mean rendered as a line **without jitter**. Strip
  uses visibly different styling (smaller, lighter background tint)
  so no reader mistakes it for the canonical curve. Caveated
  explicitly in notes.md as "preliminary; finer-resolution view of
  recent dynamics the 90d curve cannot yet resolve."

All four share the x-axis and the §3.6 reference vertical lines.

### 5.2a `score-vs-garmin-normalised.png` — companion lead/lag figure

Added 2026-06-07 same day per peer review. Different-scale curves
(score 1–6 vs RHR ~55–60 bpm vs avg stress ~30 vs efficiency ~0.99 vs
spike ~6–13 min) are unreadable for visual lead/lag inspection on
absolute axes — the eye cannot register that a 0.3-score-point shift
"matches" a 4-bpm RHR shift. The main PNG's panel 1 + panel 2 carry
absolute reading for honest level interpretation; this companion
figure carries normalised reading for lead/lag inspection.

**Construction:**
- Six curves on one panel, shared x-axis:
  - score trimmed mean
  - score median
  - avg stress
  - max-spike minutes
  - RHR
  - sleep efficiency
- Each curve **min-max normalised within its own full trajectory**
  so all curves sit on a **0–1 y-axis** (0 = own trajectory's
  minimum anchor value; 1 = own trajectory's maximum anchor value).
- **Sign-flipped to "recovery-direction"** for worsen-direction
  metrics so all six curves rise = improvement: score curves stay
  as-is (higher score = better); avg stress, max-spike, RHR are
  rendered as `(1 − normalised)`; sleep efficiency stays as-is. The
  y-axis label is **"recovery direction (higher = better, each
  channel normalised to own range)"**. Locked in the legend so
  there's no ambiguity in notes.md when reading lead/lag direction.
- Same colours as panel 1 (Garmin) + panel 2 (score) for cross-figure
  legibility.
- Same reference vertical lines as the main PNG (§3.6).

This figure is referenced from §4 question 1 ("does the score
trajectory inflect at the same date as the Garmin pendulum?") —
the answer to that question is read from this figure, not from the
absolute-axis main panel.

### 5.3 `notes.md`

Same shape as S01's notes.md. Sections:
- Status statement at top.
- Selected anchor-date table using **the same dates S01 used** so the
  trajectories can be compared side-by-side at a glance. Pre-tracking
  rows (e.g. 2021-11-14) show "—" in the score columns; the table
  itself becomes a record of the "no pre-LC anchor" caveat.
- Per-statistic reading (mean, median, distribution shifts).
- Answers to the five questions in §4. Question 1 (inflection-date
  alignment) is read against the **§5.2a normalised-scale figure**,
  not against the absolute-axis main panel, and reports the
  algorithmically picked peak/trough anchors per §7.1.
- **§3.8 correlation result** — the primary ρ + CI + effective-block
  count + verdict-row label from the locked interpretation table.
  Exploratory secondaries reported in a small table beneath, marked
  exploratory and not verdict-bearing. Explicit note on the sign of
  the primary (expected negative; flag any positive sign as
  surprising and queue an S02b reframe candidate).
- **§7.2 trigger panel** — one line per trigger T1/T2/T3/T4 saying
  "fired / not fired" with the specific numbers against the
  thresholds. Reported even when all four are null-trigger so the
  audit trail is explicit: no silent "I checked and nothing fired."
- The recent uptick — both 90d view and zoom-strip view.
- Methodology notes (including the §3.5 trim caveat and the §3.8
  effective-blocks caveat).
- Caveats (§6).
- "What this enables" + "What this does NOT do" closer matching S01.

## 6. Caveats locked into notes.md

- **Ordinal not interval.** Mean treats as approximately interval;
  median preserves ordinality. Reported together.
- **Self-report under brainfog.** A 0.2-point shift on the 1–6 scale
  is within day-to-day noise. A 0.5+ point shift sustained over 90
  days is probably meaningful. Do not over-interpret small wobbles.
- **No pre-illness anchor.** Frame the curve's high points as
  "lowest-burden period in the tracked window," never as "baseline."
- **Boundary effect at the last anchor.** The last 90-day window
  absorbs April–June 2026 into a single smoothed value. The zoom
  strip is the methodological-honesty response; both views are
  reported and may disagree.
- **Trim mechanics differ from S01's** — see §3.5.

## 7. Surprise thresholds for triggering S02b

S02 itself carries no support/refute verdict. But it embeds implicit
comparisons with S01. Pre-commit what would surprise, **with
algorithmic rules** where "surprise" relies on a visual judgement
two reviewers could legitimately disagree on. Locked before data
inspection so a post-hoc "this is interesting enough" can't drift
these.

Revised 2026-06-07 same day per peer review: original spec had two
triggers anchored to "the turnaround date" with no operational rule
for identifying it. Revised to (a) lock algorithmic definitions in
§7.1 and (b) add two more pre-committed triggers (T3
lag-throughout, T4 sustained mean-median divergence) so plausible
findings are pre-registered rather than surfaced post-hoc.

### 7.1 Algorithmic definitions used by §7.2 triggers

**Peak anchor of a trajectory** = the anchor with the maximum value
within the search window **[2022-12-02, 2024-06-30]** (~18 months,
spanning the early-stabilisation peak documented in
[S01](../S01-stabilisation-trajectories/notes.md) as "mid-2023" for
stress and max-spike). If multiple anchors tie at the maximum, pick
the earliest. The locked window excludes the May 2026 perturbation
from being selectable as "the peak."

**Trough anchor of a trajectory** = the anchor with the minimum
value within the search window **[2024-07-01, last_anchor − 90 days]**
(~22 months). The "−90 days" guard excludes the most recent quarter
from being selectable; otherwise boundary-effect blur near the
corpus edge could compete with a real trough. If multiple anchors
tie, pick the earliest.

For worsen-direction metrics (avg stress, max-spike, RHR), peak =
worst state, trough = best state. For improve-direction metrics
(sleep efficiency, score), peak = best state, trough = worst state.
The algorithmic rule operates on raw-value extrema; reading-direction
is recorded in the trigger wording below.

**Visible perturbation in an anchored trajectory** = the last
anchor's value is **≥ 1.0 σ** away from the trough anchor's value
in the worsening direction, where σ = standard deviation of all
anchor values in the trajectory across the full window.

**Visible perturbation in the zoom strip** = the 30-day rolling mean
at the most recent day differs from the 30-day rolling mean as of
90 days earlier by **≥ 0.5 score points** in the worsening direction
(score going down).

**Recovery-direction percentile rank** = each anchor's value
normalised to a 0–1 percentile within its own full trajectory, then
**sign-flipped for worsen-direction metrics** so higher pctl = more
recovered across all channels. Identical construction to §5.2a's
normalised figure; reused here so the §7.3 visual matches the
algorithmic test.

**Sustained mean-median divergence** = `|score_trimmed_mean −
score_median| ≥ 1.0` across **≥ 5 consecutive anchors** (consecutive,
not 5-of-10).

**Lag-throughout window** = anchors in `[trough_anchor_of_score,
last_anchor − 90 days]`. The trough_anchor used here is the
SCORE's trough, not S01's (so the window measures "from when the
score bottomed out onwards"). The −90 days guard matches the
trough-search guard for consistency.

### 7.2 Triggers — S02b fires if any one holds

Each trigger gets a short paragraph in notes.md saying "fired / not
fired" with the specific number against the threshold.

**T1 — Inflection-date mismatch.** Score trimmed-mean's peak anchor
OR trough anchor (per §7.1) differs from EITHER avg-stress's OR
max-spike's corresponding peak/trough anchor by **≥ 13 anchor steps
(≈ 91 days, "≥ 3 months")**. Below 13 steps is anchor-cadence noise.

**T2 — Channel-divergence on May 2026 perturbation.** Visible
perturbation (per §7.1) in **≥ 2 of S01's four metrics**, but
invisible in **both** the score 90d view AND the zoom strip. Or the
reverse: visible in score AND zoom strip, but invisible in **≥ 3 of
S01's four metrics**. (Asymmetry: Garmin is a four-channel array so
"absent in Garmin" needs more channels to be convincing than "absent
in score" which is a single channel.)

**T3 — Score lags Garmin pendulum throughout post-stabilisation.**
Across the §7.1 lag-throughout window, against the comparison metric
M ∈ {avg stress, max-spike}: `(recovery_pctl_M − recovery_pctl_score)
≥ 0.20` in **≥ 80% of anchors** in the window. Reads as "Garmin says
≥ 20 percentile points more recovered than score does, sustained
across the entire post-stabilisation stretch." Trigger fires if true
against either metric. This is the Wiggers / patient-narrative
pattern (subjective recovery trailing biometric recovery); locked
here so a positive finding is pre-registered rather than surfaced
as post-hoc surprise. Pre-committed direction: only **Garmin-ahead-
of-score** counts; the reverse (score-ahead-of-Garmin throughout)
would be doubly surprising and is captured at the edge by T1 + T2.

**T3 conservative-bar reading rule** (added 2026-06-07 same-day per
peer review, before execution). The 80%-of-anchors-at-≥0.20-pctl bar
is a high-specificity threshold. A more diffuse lag pattern (e.g.
≥ 20 pctl gap on 60% of anchors, or ≥ 10 pctl gap on 90% of anchors)
would not fire T3 but might still be visible in the §5.2a
normalised-scale figure. **If T3 does NOT fire but the §5.2a figure
shows a persistent visual gap between the score curves and the
comparison metrics across the lag window**, notes.md must report
this as a "T3 did not fire under strict bar; visual inspection
shows [X]" paragraph — not as a silent null. Two intermediate
diagnostic numbers are computed and reported alongside the strict
T3 outcome (defined here so they are pre-committed numbers, not
post-hoc summaries):
- **Share-at-0.20**: the actual % of lag-window anchors where the
  ≥0.20 pctl gap holds (the strict T3 threshold is 80%).
- **Mean gap**: the mean `(recovery_pctl_M − recovery_pctl_score)`
  across all lag-window anchors (positive = Garmin-ahead-of-score).

Both are reported even when T3 is null. A mean gap of, say, +0.15
with share-at-0.20 of 55% is a "diffuse lag" pattern that does not
fire T3 but is still a finding. Whether it warrants an S02b is a
notes.md judgement call, not an automatic trigger.

**T4 — Sustained mean-median divergence.** Sustained divergence per
§7.1 (|mean − median| ≥ 1.0 across ≥ 5 consecutive anchors). Signals
a strong distributional skew the level statistics smooth over; the
stacked-area panel must visually corroborate (a high-density tail
on one end of the distribution at those anchors).

**Otherwise**: S02 stands as descriptive characterisation; no
follow-up triggered.

### 7.3 What S02b would look like if a trigger fires

S02b is a separate pre-registration in a new folder
(`S02b-<descriptor>/`) addressing the specific trigger that fired.
The S02b shape depends on which trigger(s) fire and is designed
after S02's notes.md is committed — not pre-designed here.

Sketch shapes (NOT locked; the actual pre-registration for S02b
gets written in the relevant follow-up session):
- **T1 fires** → lag analysis with a lag window locked from S01's
  documented turnaround dates and the score's algorithmically picked
  turnaround date; daily-resolution cross-correlation with
  block-bootstrap CI per §3.8's autocorrelation discipline.
- **T2 fires** → per-day channel comparison across April–June 2026
  with raw daily data; no smoothing.
- **T3 fires** → percentile-rank-gap analysis across the full
  post-stabilisation window with block-bootstrap CI on the mean gap.
- **T4 fires** → distributional decomposition across the divergence
  anchors; identify the score values driving the skew.

These thresholds embed a prior ("score and Garmin should move
together — or if they diverge, plausibly in the patient-narrative
Garmin-ahead direction"). Pre-committing them is part of the
discipline; if any fire, it's a finding worth a separate piece.

## 8. Audit-trail discipline

- This spec is committed BEFORE `compute_trajectories.py` runs against
  any data. The same-day 2026-06-07 peer-review revisions to §3.8,
  §5.2, §7, §8 are also pre-data; they tighten the spec rather than
  rescue a result. Git history is the audit anchor for which version
  of §7 (in particular) the eventual notes.md was read against.
- If a methodology issue surfaces during execution (e.g. the trim
  mechanics produce an unreadable curve, or the median is constant at
  4 for the entire window and the panel-2 finding is null), the issue
  is **logged in notes.md as a finding**, not silently fixed.
- Any methodology change AFTER data inspection creates
  `S02-revised/` as a new folder with a new pre-registration; this
  one is left intact for the audit trail.

### 8.1 Prior-knowledge disclosure (added 2026-06-07 same-day per peer review)

What the spec author knew before locking §7's algorithmic windows
and §3.8's primary-channel choice (avg stress):

- **From S01's published notes**
  ([S01/notes.md](../S01-stabilisation-trajectories/notes.md)):
  avg stress + max-spike peak in mid-2023; trough in early-to-mid
  2025; recent May 2026 uptick on RHR (60.8), stress (33.7), spike
  (11.4).
- **From session-level project context (pre-data)**:
  user-described pendulum settling across 2023→2025 with the recent
  May 2026 perturbation already characterised as biometric. (Memory
  item: stabilisation trajectory.)
- **From H02's published result**
  ([H02/result.md](../H02-stress-elevation/result.md)): avg stress
  was the only S01 channel with train-era discrimination above null
  — basis for §3.8's primary-channel choice.

What was NOT inspected before locking this spec:
- Any score-trajectory anchor value (mean, median, distribution
  proportions). No version of `compute_trajectories.py` has been
  written; no preview plot of the score curve exists.
- `day_entries.csv` beyond its structural fact (date, score columns;
  ~1.372 rows per the
  [00-crash_v1-counts preflight](../00-crash_v1-counts/counts.md)).
- Any per-anchor or per-day cross-correlation between score and
  Garmin.

The §7.1 peak/trough search windows ([2022-12-02, 2024-06-30] and
[2024-07-01, last_anchor − 90 days]) were chosen with knowledge of
S01's published turnaround timing. They are deliberately wide
(~18 / ~22 months) so they don't pre-commit the score's chosen
extrema toward S01's; they only exclude the recent May 2026
perturbation from competing as a peak/trough. If post-data the
score's natural peak or trough falls **outside** either window, the
algorithm picks the boundary anchor and the §7.2 trigger is logged
in notes.md as "score's extremum is at the window boundary; T1 is
inconclusive against this metric, treat as null-trigger."

## 9. Registry update — locked

Once `notes.md` is committed, add one line to
[registry.md §4b "Closed since 2026-06-05"](../registry.md):

> - **S02 score trajectory**
>   ([S02-score-trajectory/notes.md](S02-score-trajectory/notes.md))
>   — 90-day rolling trimmed mean + median + score-level distribution
>   of daily gevoelscore, plotted alongside S01's four-metric Garmin
>   pendulum. [One-line headline summarising the actual finding.]

The synthesis.md update is a **separate decision** taken once the
result is in hand, not bundled with the §4b line.

## 10. Explicitly NOT done (the closer)

- Does not predict the May 2026 perturbation.
- Does not test lead/lag or channel-divergence statistically —
  deferred to S02b conditional on §7.
- Does not test multi-year arc shape similarity statistically — the
  visual overlay is the answer to that question.
- The one statistical test that IS done (§3.8 same-day rank
  correlation) does not establish causation, does not generalise
  to other users, and is bounded by an effective sample size of
  ~15 independent 90-day blocks.
- Does not reframe crash_v1 or crash_v2.
- Does not assign causation to any observed inflection.
- Does not declare a new era boundary even if one is visually
  obvious.
- Does not include volatility (rolling 30d std) or dip frequency —
  these are C.5's scope.

---

*Spec written 2026-06-07. Execution pending. Trajectory will lengthen
naturally as new score data is added; re-runnable without spec
revision.*
