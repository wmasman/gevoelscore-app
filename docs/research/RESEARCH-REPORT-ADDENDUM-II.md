# Wearable biometrics as predictors and characterisers of post-exertional malaise: an n-of-1 investigation in Long COVID stabilisation — Addendum II

*Addendum to the [2026-06-05 report](RESEARCH-REPORT.md) and the
[2026-06-06 Addendum I](RESEARCH-REPORT-ADDENDUM.md), covering work
completed 2026-06-07.*

This addendum extends the prior documents with five strands of work
completed within a single late session:

- **S02 — score-side trajectory characterisation** (§1). The first
  pre-registered analysis of the *outcome variable itself*, mirroring
  S01's methodology so the score's pendulum can be plotted on the
  same x-axis as the Garmin pendulum.
- **S02b — daily-resolution lagged correlation test** (§2). A locked
  confirmation test for S02's T1 trigger (score-leads-Garmin
  trajectory-level mismatch). REFUTED at the pre-registered bar.
- **S02c — May 2026 channel divergence descriptive characterisation**
  (§3). A locked re-framing of S02's T2 trigger against a recent
  180-day daily baseline, replacing S01's 5-year trajectory σ.
- **Cross-document propagation** (§4). Updates to S02 notes.md,
  Wiggers progress map, STOCKTAKE, synthesis, QUEUED-WORK so the
  per-piece findings are coherent across the project's dependent
  artefacts.
- **Product-plan consolidation** (§5). Merge of two prior product
  documents (pacing-indicators + trajectory-events plan) into a
  single active app-plan, resolving one substantive disagreement
  (push-burden card → pending further research) and reflecting the
  post-v2-rescue + post-S02 state of the world.

The findings reinforce the prior reports' conclusions on the central
question (no daily-aggregate predictor of validate-era crashes) while
adding two new methodology lessons (§7) that constrain how
trajectory-level findings should be read going forward.

---

## Abstract

Three pre-registered analyses targeting the score channel itself were
locked, executed, and documented within a single session on
2026-06-07. **S02** plotted the 90-day rolling trimmed mean +
untrimmed median + score-level distribution of the daily gevoelscore
across 184 anchors covering 2022-12-02 → 2026-06-05, identifying a
**clear distribution shift** (score≤3 share 20% → 7%; score=6 share
2% → 12%) that the trimmed mean smooths (4.35 → 4.72) because the
rebalancing happens inside the trim region. Two pre-registered S02b
triggers fired at the trajectory level: **T1** (score peaks 149 days
before avg-stress; troughs 100 days before max-spike duration) and
**T2** (May 2026 perturbation visible in 3 of 4 S01 metrics against
trajectory σ but invisible in both score views).

**S02b** tested whether the T1 lead/lag pattern survives at daily
resolution with proper autocorrelation correction. Primary Spearman
ρ at +149d lag = +0.099 [+0.035, +0.203] vs matched same-day ρ of
−0.097. Three of four pre-committed criteria failed; criterion (c)
"lag improves over same-day by ≥ 0.10" failed by 0.098. **REFUTED.**
The trajectory-level T1 finding does not survive at daily resolution
— a methodology lesson reframed as "rolling-curve turnaround-date
mismatches do not imply daily-resolution lead/lag signals." First
direct cross-correlation lag test for [Wiggers H1](wiggers_progress_2026-06-07.md);
empirically-observed score-leads direction refuted, Wiggers-direction
not directly tested.

**S02c** re-characterised the May 2026 perturbation against a 180-day
recent reference window. Only RHR shows an algorithmic onset
(2026-05-14) and even RHR (z_mean +0.82) is below the locked 1.0σ
"visibly worsening" bar. Stress, max-spike, sleep-efficiency, and
score are all "essentially unmoved" against the recent baseline.
Composite Garmin-worsen vs score gap = +0.324σ — directional but
small. **Methodology lesson:** two σ-frames (5-year trajectory σ vs
recent daily σ) produce categorically different perturbation
magnitudes; reports must be explicit about which frame they cite.

Combined reading across S02 + S02b + S02c: at the daily timescale,
score and Garmin channels live on largely-independent recent
baselines. Trajectory-level shapes co-vary in the broad sense but
daily dynamics are substantially independent. The "score channel
measures something different from Garmin at daily resolution"
reading from S02 §3.8 (all four channels' same-day ρ near zero)
is the through-line.

The merged product plan
([reviews/app-plan.md](reviews/app-plan.md)) replaces two prior
documents, defers the disputed push-burden card pending a
pre-registered participant-evaluation study, and incorporates the
post-v2-rescue + post-S02 state-of-the-world into Phase 3
(daily pacing indicators) and Phase 4 (retrospective biometric
enrichment, gated on specificity checks).

---

## 1. S02 — score-side trajectory (descriptive)

### 1.1. Motivation and pre-registration

[S01](garmin/hypotheses/S01-stabilisation-trajectories/notes.md)
characterised the stabilisation pendulum on four Garmin metrics
(RHR, avg stress, sleep efficiency, max stress-spike duration) as
90-day rolling trimmed means anchored every 7 days. S02 extends this
to the **outcome variable itself** — the daily gevoelscore — using
methodology identical to S01 so the score trajectory can be plotted
on the same x-axis as the Garmin pendulum.

Pre-registration at [S02 hypothesis.md](garmin/hypotheses/S02-score-trajectory/hypothesis.md),
written 2026-06-07 before `compute_trajectories.py` ran against any
data. Same-day revisions per peer-review feedback (also pre-data)
tightened §3.8 (added a same-day rank correlation), §5.2 (visual
tiers + zoom strip), §7 (algorithmic peak/trough rules), §8 (prior-
knowledge disclosure).

Three rolling statistics per anchor:
- **Trimmed mean** (10/10 trim) — mirrors S01.
- **Median** (untrimmed 50th percentile) — new for S02; preserves
  ordinality of the 1–6 discrete scale.
- **Score-level distribution** (proportion of in-window days at each
  score value 1–6) — six values per anchor summing to 1.0.

184 anchors cover 2022-12-02 → 2026-06-05 (the first anchor where the
90-day window contains a full 90 days of score data). All 184 anchors
returned valid statistics (no missing-data dropouts; score coverage
is 100%).

### 1.2. Distribution shift is the headline finding

The trimmed mean ranges from 3.83 (March 2024 dip) to 4.79 (November
2025) — a 0.96-point range. The most recent anchor (2026-06-05) is at
4.72, the highest value in the tracked window. The median is integer-
valued and **transitions from 4 → 5 around mid-2023 and stays at 5
for nearly the entire post-2023 window**, including through the
2024-2025 mean dip.

The level shift in the trimmed mean is real but small. The
**distributional shift is the more dramatic component**:

| score | early window (2022-12-16) | late window (2026-06-05) | change |
|---:|---:|---:|---:|
| 1 | 2.2% | 0.0% | −2.2 pp |
| 2 | 5.6% | 1.1% | −4.5 pp |
| 3 | 12.2% | 5.6% | −6.6 pp |
| 4 | 32.2% | 30.0% | −2.2 pp |
| 5 | 45.6% | 51.1% | +5.5 pp |
| 6 | 2.2% | 12.2% | **+10.0 pp** |

The worst tail (score 1–3 combined) drops from 20% to 7% (a 65%
relative reduction). The middle (score=4) is essentially stable. A
**new upper mode at score=6 emerges**, growing 6× from 2.2% to 12.2%
— now the third-most-common score value behind 5 and 4.

The trim mechanically chops the bottom and top 10% of days. On the
user's distribution this removes score=1 days from the low end and
score=6 days from the high end. The trimmed mean therefore *hides*
the emergence of the score=6 mode (those days are mostly being
trimmed out). The distribution panel surfaces what the mean smooths
over. **§3.5 trim-mechanics note locked in pre-registration**: 10/10
trim on a 1–6 discrete scale removes outlier *days* (not outlier
*values* as in a 0–100 stress scale); the trimmed mean is a
"robust-centre" statistic.

### 1.3. Locked questions answered

The S02 pre-registration locked five questions notes.md had to
answer, each with a specific anchor-date or distributional
observation:

1. **Does the score trajectory inflect at the same dates as the
   Garmin pendulum?** No. Score peak 2023-01-27 (vs avg-stress peak
   2023-06-25, Δ = 149 days; vs max-spike peak 2023-04-02, Δ = 65
   days). Score trough 2025-01-10 (vs avg-stress trough 2024-12-22,
   Δ = 19 days coincident; vs max-spike trough 2025-04-20, Δ = 100
   days). **Score leads Garmin pendulum at trajectory-level
   turnarounds** — fires the T1 trigger.
2. **Mean vs median divergence**. Bounded; max divergence anywhere
   0.611 points; never reaches the 1.0 sustained-divergence T4
   threshold. Mean is below median throughout most of the
   trajectory (sign of left-skewed in-window distribution: tail of
   score=3 days pulling mean below the score=5 mode).
3. **Distribution shift vs level shift**. Both — see §1.2 table. The
   distributional shift is more dramatic than the level shift.
4. **The May–June 2026 perturbation in score**. Score is at +0.40σ
   ABOVE trough in the recovery direction (improving, not perturbing)
   at the 90-day-window level. Zoom strip (last 6 months at daily
   resolution): 30d-mean today = 4.60 vs 30d-mean 90d earlier = 4.23
   = +0.37 in recovery direction. Both views agree: **score is
   improving while Garmin metrics show their recent uptick**. Fires
   the T2 trigger.
5. **No pre-illness anchor reminder**. The trajectory's "highest in
   tracked window" is the *least-burdened period in the tracked
   stretch*, not a "return to healthy."

### 1.4. §3.8 same-day rank correlation (primary statistical test)

Pre-registered Spearman ρ between daily score and daily avg stress
across 2022-09-03 → 2026-06-05 (n=1359 pairs after pairwise drop),
with **moving-block bootstrap CI at 90-day blocks × 10 000
iterations** to handle within-day autocorrelation. Three exploratory
secondaries on RHR, sleep efficiency, max-spike minutes.

| channel | role | ρ | 95% CI | n_eff blocks | verdict |
|---|---|---:|---|---:|---|
| avg stress | primary | **−0.0557** | [−0.164, +0.009] | 16 | ambiguous; underpowered |
| RHR | exploratory | +0.0203 | [−0.150, +0.081] | 16 | no detectable daily co-variation |
| sleep efficiency | exploratory | +0.0642 | [−0.002, +0.129] | 15 | no detectable daily co-variation |
| max-spike minutes | exploratory | +0.0425 | [−0.026, +0.093] | 16 | no detectable daily co-variation |

The primary ρ has the expected sign (better day ↔ less stress) but
the 95% CI spans 0 (upper edge at +0.009). Cannot exclude "no
relationship." All four channels are flat at daily resolution. The
trajectory-level (90-day rolling) curves visually share a pendulum
shape but **the underlying daily series do not co-vary at the day-
to-day timescale.**

This is the methodologically-correct way to surface "they look
similar at year scale but they're not measuring the same daily
phenomenon" — without the smoothing-induced correlation a naive test
on the rolling values would have manufactured.

### 1.5. Trigger panel (pre-registered surprise thresholds)

S02 §7.2 locked four trigger conditions, each with algorithmic
operationalisation in §7.1 (peak/trough search windows, "visible
perturbation" definition, lag-throughout pattern definition, sustained
divergence run rule).

| trigger | result | numbers |
|---|---|---|
| **T1** — inflection-date mismatch (≥ 91 days) | **FIRED** | score peak vs avg-stress peak Δ = **149 d**; score trough vs max-spike trough Δ = **100 d** |
| **T2** — May 2026 channel divergence | **FIRED** (forward) | S01 visible in 3/4 metrics; score not visible in 90d view OR zoom strip; score is +0.40σ ABOVE trough in recovery direction |
| **T3** — score lags Garmin throughout post-stabilisation | **not fired** | mean gap vs avg-stress = −0.07 (negative = score AHEAD of Garmin, opposite of Wiggers direction); vs max-spike = +0.02 (essentially zero); neither meets the 80%-of-anchors-at-≥0.20 bar |
| **T4** — sustained mean-median divergence (≥ 1.0 across ≥ 5 anchors) | **not fired** | max consecutive ≥ 1.0 run = 0; max divergence anywhere = 0.611 |

S02b queued conditional on T1 + T2 firing. Executed same-day; see §2
and §3.

### 1.6. Visual outputs

Three artefacts:
- [trajectories_score.csv](garmin/hypotheses/S02-score-trajectory/trajectories_score.csv)
  — anchor table.
- [score-trajectory-with-S01.png](garmin/hypotheses/S02-score-trajectory/score-trajectory-with-S01.png)
  — 3 main panels (S01 Garmin re-render, score mean+median, score
  distribution stacked area) + zoom strip (last 6 months at daily
  resolution, ±0.15 y-jitter for discrete-scale overlap, RNG seed
  locked at 42).
- [score-vs-garmin-normalised.png](garmin/hypotheses/S02-score-trajectory/score-vs-garmin-normalised.png)
  — 6 curves on shared 0–1 recovery-direction y-axis (each min-max
  normalised within own range, sign-flipped for worsen-direction
  metrics) for visual lead/lag inspection.

---

## 2. S02b — daily-resolution lagged correlation (locked test, REFUTED)

### 2.1. Pre-registration discipline — lag values not free-scanned

[S02b hypothesis.md](garmin/hypotheses/S02b-score-lead/hypothesis.md)
locks two lag values **derived from S02's algorithm, not free-scanned
from this dataset**:
- `lag_avg_stress_primary = +149 days` (score peak vs avg-stress
  peak).
- `lag_max_spike_secondary = +100 days` (score trough vs max-spike
  trough).

The pre-registration discipline is critical: S02b is a confirmation
test of a finding S02 produced, using independent inference machinery
(daily resolution + block bootstrap) but on the same underlying data.
The protection against motivated reasoning is the pre-committed bar
+ the refusal to free-scan additional lags. A free lag scan over
[−90, +90] days would be 180+ silent comparisons; locked discipline
elsewhere in the project (e.g. H02d's [D−4, D−1] from the activity-
labels lag-profile report) chooses lag windows from an independent
source before the test runs.

### 2.2. Locked SUPPORTED bar — four criteria

| Criterion | Requirement | Observed | Result |
|---|---|---|---|
| (a) magnitude | \|ρ_lag\| ≥ 0.20 | 0.099 | **FAIL** |
| (b) CI excludes 0 | yes | [+0.035, +0.203] | PASS |
| (c) lag improves over same-day | \|ρ_lag\| − \|ρ_same-day_matched\| ≥ 0.10 | +0.099 − +0.097 = +0.002 | **FAIL** |
| (d) expected sign | ρ_lag < 0 (score-leads-stress should produce high-score → low-stress later, expected negative for worsen-direction metric) | +0.099 | **FAIL** |

Three of four criteria FAIL. SUPPORTED requires all four. Verdict
**REFUTED on criterion (c)** — the lag does not improve over same-
day, by the largest margin of any criterion.

### 2.3. Sign-flipped near-equivalent ρ values

The headline finding:

- **Same-day ρ** on matched window: **−0.097** (n=1208)
- **Lagged ρ at +149d**: **+0.099** (n=1213)

Same magnitude, opposite sign. At day-to-day resolution, the score-vs-
stress relationship is small in either direction and sign-flips as
the lag shifts. **There is no daily-resolution version of "score
leads Garmin by ~5 months" in this user's data.**

Whatever produced S02's trajectory-level T1 finding of a 149-day
turnaround-date gap lives in the 90-day-smoothed signal, **not in the
day-by-day pairs**. The trajectory-level pattern is a smoothing-
window artifact of the participant's typical-day distribution
reshaping before the biometric baseline did, not a day-by-day
predictive relationship.

### 2.4. Secondary (max-spike +100d) null both ways

- ρ_lagged max-spike at +100d: **−0.025, 95% CI [−0.090, +0.033]**
- ρ_same-day matched: **+0.022**
- Delta: +0.003 (essentially zero)

Trough-side channel null in both lag conditions, both magnitudes <
0.03. The "100-day trough-side lead" finding from S02's T1 is also a
rolling-curve-only pattern.

### 2.5. Power and effective sample size

| condition | n_pairs | n_eff_blocks |
|---|---:|---:|
| avg_stress same-day | 1359 | 16 |
| avg_stress +149d | 1213 | 14 |
| max_spike same-day | 1364 | 16 |
| max_spike +100d | 1267 | 15 |

Loss of effective power from same-day → lagged is small (~1-2
blocks). The pre-registration's "INCONCLUSIVE" outcome anticipated
underpowering; the bar is decisively REFUTED on (c) instead. Power
was sufficient to reject.

### 2.6. Connection to Wiggers H1

S02b is the project's **first direct cross-correlation lag test** for
[Wiggers H1](wiggers_progress_2026-06-07.md) — "do wearable signals
lead the felt crash?". The Wiggers framing is **wearables lead score**.
S02 found the empirically-OPPOSITE direction (score leads wearables
in rolling-curve turnaround dates) and S02b tested that empirical
direction directly at daily resolution.

S02b refutes the score-leads-wearables direction at daily resolution.
This does NOT mean wearables-lead-score (the Wiggers direction) is
supported — S02b did not test that direction. Both directions remain
consistent with "no daily-resolution lead/lag signal in either
direction," which is what S02b's secondary result and the magnitude
of all four ρ values (none above |0.10|) suggests.

Wiggers progress map updated 2026-06-07 to reflect H1 status as
"PARTIAL → daily-resolution lead/lag REFUTED in the empirically-
observed direction (S02b); Wiggers-direction not directly tested."

### 2.7. Methodology lesson banked

> **Rolling-curve turnaround-date mismatches do NOT imply daily-
> resolution lead/lag signals.**

Future trajectory comparisons in this project (S03+ if any) should
cite this constraint before claiming daily-resolution implications
from a curve-level pattern.

---

## 3. S02c — May 2026 channel divergence (descriptive, two-σ-frame lesson)

### 3.1. Motivation

[S02 T2](#15-trigger-panel-pre-registered-surprise-thresholds) fired
because the May 2026 perturbation was visible in 3 of 4 S01 Garmin
metrics against S01's full 5-year trajectory σ. S02c re-characterises
the same perturbation period against a **180-day recent reference
window** (2025-09-08 → 2026-03-07) — the user's stabilised baseline
in the months immediately before the perturbation.

The two σ-frames ask categorically different questions:
- **S01-trajectory frame (S02 T2's reference)**: "is current state
  exceptional vs the whole tracked history?"
- **Recent-baseline frame (S02c's reference)**: "is current state
  exceptional vs the recent normal?"

The two answers can disagree because day-to-day variability is much
larger than 90-day-smoothed-anchor variability. (Empirically:
avg-stress S01-anchor σ = 2.51 across 238 anchor values; avg-stress
S02c-reference σ = 6.21 across 180 daily values — a factor of 2.5.)

### 3.2. Pre-registration locks methodology and reading rules

[S02c hypothesis.md](garmin/hypotheses/S02c-may2026-divergence/hypothesis.md)
locks:
- Reference window 2025-09-08 → 2026-03-07 (180 days).
- Perturbation window 2026-03-08 → 2026-06-05 (90 days, matching
  S01's rolling-window length so the "last anchor" of S01 represents
  exactly this period).
- Per-channel z-score against `μ_ref` / `σ_ref`.
- Algorithmic onset rule (§3.5): first day where `|z| ≥ 1.0` AND at
  least 7 of the next 14 days have `|z| ≥ 1.0` in the same direction.
- Reading rules (§3.7): `|z_mean_pert| ≥ 1.0` in worsening direction
  → "visibly worsening"; `|z| < 0.5` → "essentially unmoved";
  intermediate → "directional, not clearly visible."

### 3.3. Per-channel result

| channel | z_mean_pert | max\|z\|_pert | onset date | reading |
|---|---:|---:|---:|---|
| score | +0.07 | 3.40 (2026-05-12) | none | **essentially unmoved** |
| avg_stress | +0.24 | 3.32 (2026-05-02) | none | essentially unmoved |
| max_spike_minutes | +0.16 | 2.13 (2026-04-28) | none | essentially unmoved |
| RHR | **+0.82** | 1.68 (2026-05-26) | **2026-05-14** | directional toward worsening, not clearly visible |
| sleep_efficiency | −0.0006 | 3.92 (2026-04-21) | none | essentially unmoved |

**Only RHR shows an algorithmic onset** and even RHR (z_mean +0.82)
is below the 1.0σ "visibly worsening" bar. The other three Garmin
channels and the score are all "essentially unmoved" against the
recent baseline. The "perturbation visible in 3 of 4 metrics" framing
of S02 T2 does not hold at recent-baseline σ; only RHR carries any
directional signal at all.

### 3.4. Channel-pair correlations within the perturbation window

Only one pair co-varies above |r| = 0.5: **avg_stress × max_spike**
at r = +0.61 (n=83). Both are stress-derived measures from the same
physiological substrate, so this is unsurprising.

RHR is **independent of stress and max-spike within the window**:

| pair | r |
|---|---:|
| avg_stress × RHR | −0.01 |
| max_spike × RHR | −0.12 |
| RHR × sleep eff | −0.11 |

The RHR drift is solo. No coordinated multi-channel event onset.

Two cross-channel observations involving score are flagged but not
verdict-bearing per the spec's §3.6 "no CI at 1 effective block"
rule:
- score × avg_stress within window: r = +0.26 (positive — **opposite
  direction** to the full-corpus same-day finding from S02 §3.8 of
  ρ = −0.06). Consistent with a "productive activity → high
  sympathetic activation AND high subjective day-rating" pattern
  that the full corpus does not surface.
- score × max_spike within window: r = +0.20 (same direction as
  above, weaker).

Descriptive observations only; not pursued.

### 3.5. Headline divergence number

| measurement | value |
|---|---:|
| composite Garmin-worsen z (mean of stress / max-spike / RHR z-scores, mean across 83 perturbation days) | +0.41 |
| score z (mean across same 83 days) | +0.08 |
| **gap (composite − score)** | **+0.32σ** |
| max single-day gap | +3.07σ |

The composite gap is directional (Garmin trending toward worsening
while score essentially flat) but the magnitude is small at recent-
baseline σ. The 3.07σ max single-day extremum is informative but not
representative.

### 3.6. Substantive nuance of S02 T2's framing

S02 T2 "fired forward" against trajectory σ. S02c against recent
daily σ produces a much more modest reading. **Both are correct in
their own σ-frame; the reading just needs to be against the right
σ.** What S02c forecloses is the strongest reading of T2 — that the
Garmin perturbation is unambiguous and the score's stability is
striking. Against recent baseline, the Garmin perturbation is mostly
in one channel (RHR) at directional-but-not-clearly-visible
magnitude, and the score is essentially unmoved (not exceptionally
well, just normal-recent).

### 3.7. Methodology lesson banked

> **Two σ-frames produce categorically different perturbation
> magnitudes.** Trajectory σ (e.g. 90-day-rolling means across 5
> years) and recent daily σ (e.g. 180 raw daily values) are not
> interchangeable. Reports must be explicit about which frame they
> cite. Cards and STOCKTAKE claims that present a single perturbation
> reading should name the frame.

This applies retroactively to S02 T2's framing in stocktake-level
documents, which have been updated (§4).

### 3.8. Visual output

[divergence_plot.png](garmin/hypotheses/S02c-may2026-divergence/divergence_plot.png)
— two panels:
- **Panel A**: per-channel daily z-scores across both reference + per-
  turbation windows, vertical line at window boundary, onset markers
  (only RHR's at 2026-05-14).
- **Panel B**: composite Garmin-worsen z vs score z (positive z =
  improving direction for score), shaded gap, gap-mean text.

---

## 4. Cross-document propagation

The per-piece notes.md files for S02, S02b, S02c each explicitly
prescribed updates to dependent documents. All five updates landed
same-day; this section summarises what changed and why, for the
audit trail.

### 4.1. S02 notes.md — forward references added

Added at the top of S02's status statement and inside the §7.2
trigger-panel table:
- A forward-references block: "T1 was tested at daily resolution in
  S02b and REFUTED; T2 was characterised at daily resolution in S02c
  and the framing is substantively nuanced. Read T1 and T2 below in
  light of these follow-ups."
- Inline annotations in the T1 row ("FIRED at trajectory level;
  REFUTED at daily resolution by S02b") and T2 row ("FIRED at
  trajectory level; NUANCED at daily resolution by S02c").

Closes the "future readers might take T1/T2 as supported in
isolation" risk that the per-piece S02 notes.md left open before S02b
+ S02c executed.

### 4.2. Wiggers progress map — H1 row updated

[wiggers_progress_2026-06-07.md](wiggers_progress_2026-06-07.md):
- **H1 priority shortlist row**: status changed from "PARTIAL... S02b
  queued conditional on S02" to "PARTIAL → daily-resolution lead/lag
  REFUTED in the empirically-observed direction (S02b); Wiggers-
  direction not directly tested." Full criterion-by-criterion numbers
  embedded.
- **H1 section-by-section row**: full S02b context with the four
  criteria, the sign-flip finding, the methodology lesson.
- **"Recently queued items addressed" entry**: S02 now EXECUTED with
  both follow-ups, status updated.
- **Next-phase prioritisation** (§"Where this leaves the project"):
  the H1 lead/lag priority recast as "Wiggers-direction lag test"
  since the observed-direction is done.
- **C3 row**: now notes S02 §3.8 same-day correlation result;
  clarifies C3 (curvature) still untested.

### 4.3. STOCKTAKE.md — three locations updated

[STOCKTAKE.md](STOCKTAKE.md):
- **Card (a) stabilisation-arc entry**: extended with S02 distribution-
  shift anchors (score≤3 share 20% → 7%, score=6 share 2% → 12%,
  algorithmic peak/trough dates). Caveat block added: "trajectory-
  level score-leads-Garmin lead pattern can be cited but NOT as a
  predictive claim, per S02b refutation." S02c recent-baseline
  framing referenced for current-state framing.
- **Card-prototyping section** (Tier 1 supporting findings list):
  S02 added alongside S01 trajectories, K01/K02 era shifts,
  HA06b/HA10/HA11 era directionality reversal.
- **Card (a) closer paragraph**: 2026-06-07 update integrating all
  three pieces.

### 4.4. synthesis.md — new top-level section appended

[synthesis.md](garmin/hypotheses/synthesis.md): new "Update 2026-06-07
(later still ×2)" section integrates S02 + S02b + S02c under the
five-finding structure:

1. Score-side stabilisation is empirically anchored at the distribution
   level (S02 distribution shift gives Card (a) its score-side
   empirical anchor).
2. Score and Garmin channels measure substantially different state at
   the daily timescale (multiply confirmed by S02 §3.8 + S02b + S02c).
3. Rolling-curve turnaround-date mismatches do NOT automatically imply
   daily-resolution lead/lag signals (methodology lesson 1).
4. Two σ-frames produce categorically different perturbation magnitudes
   (methodology lesson 2).
5. The "score is at all-time high" framing from S02 needs nuancing —
   true at trajectory σ, "essentially unmoved" at recent-daily σ.

Plus Wiggers H1 connection, card-prototyping implications, and revised
"what's queued" list.

### 4.5. QUEUED-WORK.md C.5 — status update

[QUEUED-WORK.md C.5](QUEUED-WORK.md#c5-volatility--dip-frequency-progress-metric-descriptive)
volatility + dip-frequency entry now notes:
- S02 was executed and explicitly left volatility + dip-frequency as
  C.5's scope (S02 covers level + distribution; C.5 covers volatility
  + frequency).
- C.5 is downstream of S02 — can mirror S02's anchor grid for direct
  overlay.
- S02c's recent-baseline reading informs C.5's recent-period framing.

### 4.6. registry.md §4b — three new entries

S02, S02b, S02c each got their own one-line entry in §4b ("Closed
since 2026-06-05"), following the same shape as prior entries (one
line per piece with verdict + key numbers + cross-references).

---

## 5. Product-plan consolidation

### 5.1. Two source documents merged into one active plan

Two prior documents addressed the "research → app" question from
different angles:
- **`pem-pacing-indicators.md`** (research-side curated indicators
  catalog, anchored on Garmin metrics: daily exertion class, 7-day
  push burden, daily stress spike, effective exertion pctl rank,
  dip-cluster proximity, personal-baseline z-score).
- **`2026-06-07-trajectory-and-events-app-plan.md`** (Families 1+2
  app plan, anchored on score trajectory + crash/dip overlays).

These pieces were almost orthogonal in coverage but agreed strongly
on discipline (forbidden patterns, UI tone, n=1 caveats, retrospective
> pre-emptive framing). They also had one substantive disagreement:
the 7-day push burden card. The pacing-indicators piece argued for
shipping it as a *descriptive fact* ("3 zware dagen, jouw mediaan
is 1"); the trajectory-events piece argued for excluding *all*
push-pattern surfaces in v1 on the grounds that any push-pattern
card risks being read as a warning regardless of framing.

The merged active plan
([reviews/app-plan.md](reviews/app-plan.md)) replaces both, with the
two sources archived at [reviews/_archive/](reviews/_archive/) with
archive-notice headers preserving content verbatim.

### 5.2. Resolution of the push-burden disagreement: PENDING further research

The merged plan defers the push-burden card pending a pre-registered
participant-evaluation study. The open research question:

> Does a descriptive push-burden card, framed as a fact-with-context
> and explicitly labelled non-predictive, produce different user
> response than a predictive alert? Specifically: does it (a)
> accurately inform the participant about sustained-load patterns
> without inducing anxiety, (b) anchor pacing decisions usefully,
> or (c) function as an implicit warning regardless of framing?

Recommended (not locked) study shape: within-subject A/B/C comparison
of three card variants (descriptive-fact / predictive-alert / no-
card) with same-day score + tag data collection. Outcome decision
locked before the study ends. Until the study lands, no push-pattern
card ships.

### 5.3. Phased plan with v2 + S02 state-of-the-world reflected

Five active phases + the pending push-burden entry:

- **Phase 1** — Score-only trajectory + events (v1 floor). Built on
  S02 (trajectory card, zoom strip), crash_v2 labels (event markers
  on timeline), per-crash detail (score-only, no biometric overlay).
- **Phase 2** — Multi-axis trajectory + descriptive enrichment. S01
  Garmin trajectories alongside S02 score trajectory; recovery-time
  distribution descriptive card; yearly crash count. **S02b
  refutation explicit in copy constraint**: the trajectory-level
  score-leads-Garmin pattern must NOT be presented as "your score
  predicts your biometrics."
- **Phase 3** — Daily pacing indicators. Absorbs the pacing-indicators
  piece's Tier 1: daily exertion class (HA01b SUPPORTED with **Theme
  A caveat baked in** — copy must not imply predictive value), daily
  stress-spike event marker (H02b train-anchored, retrospective),
  dip-cluster proximity (passive context).
- **Phase 4** — Retrospective biometric enrichment (conditional).
  Was Phase 3 in the trajectory-events plan; renumbered Phase 4 to
  follow the daily pacing indicators. **v2 condition now MET in
  part**: HA07d + HA10 + HA11 v2 RESCUE (per Addendum I §5 +
  diagnostic outcomes); HA06b permanently CLOSED. **Specificity
  checks remain the binding gate.** Phase 4 does not ship without
  specificity + posterior numbers.
- **Phase 5** — Stabilisation milestones + reflection-tier indicators.
  Includes S02 distribution-shift milestones ("Het aandeel van
  slechte dagen is gedaald van 20% naar 7%"; "Score-6 dagen waren 2%
  van je weken; nu zijn ze 12%"). Tier 2 indicators (effective
  exertion pctl, baseline z-score) as detail-view content.

Suggested order of delivery: Phase 1 + Phase 5 (v1 floor) → Phase 3
(pacing indicators when Phase 1 has bedded in) → Phase 2 (multi-axis
stretch) → Phase 4 (conditional, post-specificity). Pending push-
burden ships only after its pre-registered study returns a clear
answer.

### 5.4. Documentation chain

Live references:
- [docs/roadmap.md](roadmap.md#L44) entry now points to the merged
  active plan.

Archived references preserved verbatim:
- [reviews/_archive/pem-pacing-indicators.md](reviews/_archive/pem-pacing-indicators.md)
  with archive-notice header.
- [reviews/_archive/2026-06-07-trajectory-and-events-app-plan.md](reviews/_archive/2026-06-07-trajectory-and-events-app-plan.md)
  with archive-notice header.

Historical research-doc references to "pem-pacing-indicators.md" (in
HA10 diagnostic.md, HA11 result.md, RESEARCH-REPORT-ADDENDUM.md §6,
QUEUED-WORK.md, etc.) left intact as audit-trail artefacts pointing
to the archive location.

---

## 6. Discussion — what this adds to the "kind of crash changed" framework

Addendum I §6 documented the "kind of crash changed" theory at **nine
directional findings on independent axes plus one cross-class
convergence finding** (the dip-tier convergence). Today's work adds
**two further descriptive axes** and **two methodology constraints**
on how the prior nine should be read.

### 6.1. Two new descriptive axes from S02

The score-side trajectory itself is a new characterisation surface
the prior nine-axis framework did not include:

**Axis 10 — score-distribution tail-collapse on the worst end.** The
score≤3 share dropped from 20% (early window) to 7% (late window) —
a 65% relative reduction. Pre-stabilisation: ~1 in 5 days was a
score≤3 day. Post-stabilisation: ~1 in 14. This is the score-side
counterpart to K01's nadir-shift finding (no score-1 days in late-
era crashes); S02 extends it to non-crash days at the distribution
level.

**Axis 11 — score-distribution upper-mode emergence.** The score=6
share grew from 2% to 12% — a 6× increase. Score=6 days were rare
events in the pre-stabilisation distribution; they are now the
third-most-common score value. The trimmed mean smooths this because
the trim chops the score=6 tail; the stacked-area distribution panel
surfaces it directly.

Both axes are visible in S02's distribution panel; both are stable
across the 184 anchors. Neither is captured by the prior nine
directional findings.

### 6.2. Two methodology constraints on the prior nine

The nine-axis framework in Addendum I §6 treats each axis as
"directional finding (early → late)." S02b and S02c together impose
a methodology constraint on how directional findings derived from
rolling curves should be cited:

**Constraint A** (from S02b): **Rolling-curve turnaround-date
mismatches do not imply daily-resolution lead/lag signals.** S02's T1
finding of 149-day score-vs-stress turnaround lag was clean at
trajectory level. S02b tested it at daily resolution and refuted it
on the locked bar (criterion c failed by 0.10). The trajectory-level
pattern is real as a description; the causal/predictive reading is
not supported. Any future trajectory-level lead/lag observation in
this project should carry a "but daily-resolution status unknown"
caveat unless a confirmation test like S02b has been run.

**Constraint B** (from S02c): **Two σ-frames produce categorically
different perturbation magnitudes.** S02 T2 "fired" against 5-year
trajectory σ for 3 of 4 Garmin metrics; S02c against recent 180-day
daily σ found only RHR carries directional signal. The two readings
are both correct in their own frame; reports must be explicit about
which frame they cite. Stocktake-level claims that present a single
perturbation reading should name the frame. Applies retroactively to
S01-trajectory-σ claims in Addendum I and prior — those claims stand
as trajectory-level observations but should be read alongside their
recent-baseline-frame counterparts where they exist.

### 6.3. The nine-axis framework, restated and constrained

Addendum I §6's framework table presented nine "directional findings
(early → late)" axes. After today's work, the framework reads:

**Trajectory-level descriptive axes (eleven):** the original nine
plus axis 10 (worst-tail collapse) and axis 11 (upper-mode emergence)
from S02. All eleven are trajectory-level descriptive findings about
the participant's recovery arc. None are inherently predictive.

**Daily-resolution status of axis-derived patterns:** mostly unknown.
S02b's refutation of the rolling-curve T1 lead is the first
systematic test. Other axes (e.g. axis 2 "stress precursor (spike
count): strong yes → weaker" from H02b) have implicit daily-
resolution status from their underlying test methodology, but no
direct cross-correlation lag analysis has been run on most axes.

**Implication for narrative use of the framework:** descriptive
trajectory-level claims are appropriate (e.g. "your worst-day share
has collapsed by 65%"). Causal or predictive claims derived from
trajectory shapes are not appropriate without a daily-resolution
confirmation test. The merged product plan (§5) carries this
constraint into copy discipline for Phase 2's multi-axis trajectory
card.

### 6.4. The May 2026 perturbation — coda

S02 T2 fired forward (Garmin perturbing, score not). S02c nuanced
the magnitude: at recent daily σ, only RHR shows directional drift
(z_mean +0.82, onset 2026-05-14), and even RHR is below the 1.0σ
"visibly worsening" bar. The other Garmin channels and the score are
essentially unmoved against the recent baseline.

This nuance reads two ways:
- **Sober reading**: the May 2026 "perturbation" is mostly an
  artifact of the trajectory being smoothed over a long window.
  Against recent baseline, only RHR is drifting, and only mildly.
- **Cautious reading**: a single channel quietly trending upward over
  22 days, against an otherwise stable recent baseline, is worth
  watching. If RHR continues to drift upward over the next month, the
  pattern becomes more interesting; if it plateaus or reverses, it
  was a transient state.

The current data does not resolve which reading is correct. The
descriptive characterisation is locked at S02c; any subsequent
re-evaluation needs new data (which will arrive naturally as the
participant continues to wear the watch).

---

## 7. Methodology notes new this addendum

Three methodology lessons banked from the S02 batch.

### 7.1. Pre-register algorithmic operationalisation of "surprise thresholds"

S02's initial pre-registration (pre-peer-review) had a T1 trigger
that said "score's turnaround date differs from S01's by ≥ 3 months."
The peer-review pass caught that "turnaround date" was not
algorithmically defined; two reviewers could legitimately pick
different dates from the same curve. Same-day revision (before any
data inspection) locked an algorithmic rule:

> **Peak anchor** = argmax of trajectory values within
> [2022-12-02, 2024-06-30] search window; argmin on tie pick earliest.
> **Trough anchor** = argmin within [2024-07-01, last_anchor − 90d]
> search window.

The search windows were chosen with knowledge of S01's published
turnaround timing (a deliberately wide search window of 18 / 22
months so the choice doesn't bias toward S01's exact dates; just
excludes the most recent quarter from competing as a peak/trough).

This lesson is **stronger than "pre-register the metric"**: it's
"pre-register the algorithmic computation of any threshold whose
'fire/no-fire' answer depends on which day or value is picked."
Future surprise-threshold pre-registrations should include
algorithmic rules + search windows + tie-break rules from the start.

### 7.2. Locked confirmation tests are the antidote to trajectory-level over-claiming

S02's T1 trigger fired at trajectory level. Before S02b ran, the
natural reading was "score leads Garmin pendulum at trajectory-level
turnarounds — possibly informative as a precursor signal." After
S02b ran (REFUTED at daily resolution), the reading shifted to
"trajectory-level pattern is real as a description; not informative
as a daily-resolution precursor."

The pre-registration discipline that made this work:
- S02's spec §7 named the triggers + their algorithmic rules.
- S02b's spec locked the pre-committed bar (four criteria) before
  data inspection.
- The lag values for S02b were derived from S02's algorithm, not
  free-scanned.
- S02b's expected sign (negative ρ for score-leads-stress) was pre-
  committed, so a sign-flip got recognised as criterion-(d) FAIL
  rather than as a curiosity to chase.

**Lesson**: when a trajectory-level finding emerges, the
confirmation-test pre-registration should be locked before celebrating
the finding. S02's same-day execution of S02b + S02c is the template:
trigger fires → pre-registration locked → confirmation test runs →
outcome reported faithfully against bar. Without S02b, the T1 finding
could have hardened into a "score leads biometrics" claim that
wouldn't survive scrutiny.

### 7.3. Cite the σ-frame on every perturbation claim

S02 T2 and S02c disagree on the May 2026 perturbation reading because
they use different σ-frames. **Neither is wrong; they're answering
different questions.** Future reports + cards + stocktake entries
that cite a "perturbation visible in N channels" should name the
σ-frame.

This is a small disciplinary lift. Two extra words per claim
("against trajectory σ" or "against recent daily σ") removes a real
source of inconsistency between documents. STOCKTAKE and the merged
app-plan both adopted this discipline in the cross-document
propagation pass.

---

## 8. Next steps

### 8.1. Updates to the original report's next steps (§7) and Addendum I's (§8)

The original report's five next-step directions and Addendum I's
update to them remain accurate; today's work doesn't supersede any
of them. Notes-quality work, H04b execution, dip subtyping,
cluster-based analyses, and the retrospective per-dip / rough-patch
card concepts are all still queued.

### 8.2. New strands queued

1. **S02b Wiggers-direction lag test.** S02b tested only the
   empirically-observed score-leads-Garmin direction. The Wiggers-
   canonical wearables-lead-score direction remains untested directly.
   Magnitude data from S02b suggests it would also be small at daily
   resolution; pre-registering and running would close the question.
2. **S03 — score-channel deeper characterisation?** Not yet scoped;
   possible next-batch S-piece. Open question: what does the score's
   variance / volatility look like over time? Partially overlaps with
   C.5 (queued).
3. **C.5 volatility + dip-frequency progress metric** (queued
   in [QUEUED-WORK.md C.5](QUEUED-WORK.md), now status-updated to
   reflect S02 as executed). Can mirror S02's anchor grid for direct
   overlay.
4. **Specificity checks on the v2-RESCUE findings** (HA07d, HA10,
   HA11) — these remain the binding gate on the merged app-plan's
   Phase 4 (retrospective biometric enrichment).
5. **Push-burden pre-registered participant-evaluation study**
   (Pending entry in the merged app-plan §5). Small within-subject
   evaluation of three card variants. Locked outcome decision before
   the study ends.

### 8.3. Methodology-honesty pattern banked

When a trajectory pattern is observed, locking a daily-resolution
confirmation test into the same pre-registration where possible is
the template. S02's locked S02b triggers + same-day execution
produced the strongest possible audit trail: the spec, the
confirmation test, the outcome, and the documentation propagation
all landed within hours of each other, each step's pre-registration
locked before the next step ran.

---

## 9. Acknowledgement of limitations

This addendum compounds the prior reports' n-of-1 limitation: one
participant's data, one Forerunner 245's firmware-versioned
algorithms, one 3.7-year window straddling a stabilisation
transition.

Specific to this addendum:

- **The S02 trajectory descriptions are summaries of one trajectory.**
  The framework (90-day rolling + trimmed mean + median + distribution)
  should transfer to other PAIS individuals; the specific anchor
  values and trigger outcomes almost certainly should not.
- **S02b's lag values (149d and 100d) are specific to this user's
  S02 turnaround dates.** A different user with a different
  stabilisation trajectory would have different lag values + a
  different S02b outcome.
- **S02c's recent-baseline reference window choice (180 days
  immediately pre-perturbation) is locked but not sensitivity-tested.**
  A longer reference would absorb older baseline; a shorter would
  lose statistical resolution. The 180-day choice is the locked
  compromise.
- **The product-plan consolidation reflects the current state of the
  art for this n-of-1 project.** The merged plan's phasing and copy
  examples are appropriate for this participant; transferability to
  other PAIS individuals would require redoing the framing-discipline
  pass for their specific evidence base.
- **The May 2026 perturbation reading is bounded by the data
  available.** RHR has been drifting upward for 22 days at the corpus
  edge. Whether this continues, plateaus, or reverses is unknowable
  from this data window. The descriptive characterisation will be
  refreshable as new data arrives; the locked reading at S02c is the
  state as of 2026-06-05.
- **No clinical use.** All findings here are awareness signals for
  this participant's pacing self-management. None replace clinical
  assessment, none are validated for clinical use, none prescribe
  behaviour.

---

*Addendum II locked 2026-06-07. Original report at
[RESEARCH-REPORT.md](RESEARCH-REPORT.md); Addendum I at
[RESEARCH-REPORT-ADDENDUM.md](RESEARCH-REPORT-ADDENDUM.md). Next-
phase work tracked in [docs/research/garmin/hypotheses/](garmin/hypotheses/),
[docs/research/QUEUED-WORK.md](QUEUED-WORK.md), and
[docs/research/reviews/app-plan.md](reviews/app-plan.md).*
