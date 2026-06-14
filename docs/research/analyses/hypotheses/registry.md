# Hypothesis registry — Garmin × gevoelscore insight cards

The index of every insight-card hypothesis we are systematically testing
before any feature work begins. Each hypothesis is **pre-registered**
(statement + measurement + falsification criterion locked before the data
is examined for that test), runs against a **single fixed `crash_v1`
definition** so verdicts are comparable, and uses a **held-out window**
where applicable so we don't fool ourselves.

**Nothing in this registry has been tested yet.** Status = `pending`
across the board.

**Locked 2026-06-05**:
- `crash_v1` = Option B-tightened (§2): run of ≥2 consecutive days with
  **score ≤ 3** on the 1–6 gevoelscore scale, episodes within 3 days
  merged. (Revised same day from the original "personal bottom 15%"
  rule after [00-crash_v1-counts](00-crash_v1-counts/counts.md) showed
  the percentile rule was broken by ties at score=4, catching ~50% of
  days instead of ~15%. The absolute threshold is a closer realisation
  of the original intent.)
- First batch H01–H05 (§3) is locked. H01 starts next.
- Train/validate split (§1, revised after preflight): train 2022-09-03 →
  2023-12-31 (14 episodes); validate 2024-01-01 → 2026-06-05 (15
  episodes). Roughly 50/50 by count; required revision after the
  preflight surfaced a recovery cliff between 2024 and 2025. Hypotheses
  are "supported" only if the pre-registered criterion holds on *both*
  halves.

---

## 1. Scope and ground rules

**Analysis window.** 2022-09-03 → today (2026-06-05). The post-gevoelscore
overlap with Garmin coverage. ~3.7 years, ~1.370 day-entries, ~1.370
matched monitoring_b files. See [project_timeline_anchors](../../../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/project_timeline_anchors.md) for why these dates.

**Pre-LC Garmin (2021-08-16 → 2022-09-02)** is *not* part of any
label-based test. It may be referenced for baseline-calibration cards
("how far has the system moved") in a later batch, but never as a source
of crash labels.

**Train/validate split.** Default for any predictive hypothesis:
- Train: 2022-09-03 → 2023-12-31 (~16 months, 14 crash_v1 episodes)
- Validate: 2024-01-01 → 2026-06-05 (~29 months, 15 crash_v1 episodes)

Revised 2026-06-05 after the preflight ([00-crash_v1-counts](00-crash_v1-counts/counts.md))
revealed a recovery cliff: crash episodes drop from ~10/year in 2023–24
to ~2/year in 2025–26, which the user confirms is real PEM-frequency
recovery and not score-interpretation drift. A simple time-proportional
70/30 split would have left the validate window with only 3 episodes;
the revised split is roughly 50/50 by episode count.

The cliff *inside* the validate window is itself the harder test: if a
Garmin precursor pattern is genuinely PEM-related, it should still
appear in the residual 2025+ episodes even though the underlying state
has shifted. If the pattern was an artifact of overall worse-state
physiology, it will fail validation.

A hypothesis is "supported" only if the pattern holds on *both* halves.
Hypotheses that are descriptive (e.g. characterising recovery time, not
predicting a future event) don't need a held-out split — note that
per-hypothesis.

**Pre-registration discipline.** Each hypothesis gets its own folder
`hypotheses/H##-<name>/` containing:

- `hypothesis.md` — statement, why, measurement window, falsification
  criterion, expected effect size if positive. Written *before* `test.py`
  runs against real data.
- `test.py` — pulls gevoelscore + Garmin (+ later calendar) per the
  measurement spec, computes the test, emits a chart and summary numbers.
- `result.md` — honest verdict, the chart, caveats, what to do next.
- `card.md` — **only if result.md is "supported"**. 2–3 candidate
  card-text variants for the insight card this hypothesis would enable,
  using real numbers from the analysis and (where notes are present)
  real quoted phrases from the user's `day_entries.note`. Must respect
  the design brief tone (reflective Dutch, restrained, no em-dashes
  per [feedback_no_emdash_in_ui]), the pacing-doc principle that we
  present conclusions and not prescriptions, and the brainfog rule that
  the card is readable in seconds. Cards are not designed in advance;
  they are written from the data the test produces.

The `card.md` step is deliberately separated from `result.md`: the
research determines whether a card *should* exist; the craft step
determines what it *says*. Composing cards across multiple supported
hypotheses (e.g. "RHR was +5 *and* stress was sustained" when H01 + H02
both fire on the same episode) is a later step.

**Honest verdict categories.** Every result uses the same labels:
- **Supported** — pattern present in train *and* validate, effect size at
  or above the pre-registered threshold.
- **Refuted** — pattern absent or below threshold in at least one of
  train / validate.
- **Inconclusive** — too few crash episodes to power the test, or signal
  noisy enough that we can't tell.
- **Partial / needs reshape** — interesting in one direction but the
  pre-registered measurement was wrong; document and decide whether to
  re-pre-register a v2.

**Multiple-comparisons honesty.** Testing 5–6 candidate signals against
the same crash list means some will look positive by chance. The
held-out validation is the main defence; we additionally note in each
result the number of comparisons made and the rough probability of a
spurious positive under the null.

---

## 2. `crash_v1` — operational definition of a crash

**Locked 2026-06-05: Option B (score-percentile, run-based).**

Rationale: the `[fysiek] pem` tag is recent and was not in use for most of
the 1.370-day history, so a tag-based definition would only catch crashes
from the recent window — Garmin × gevoelscore validation needs the full
overlap. The historical crash signal lives instead in the free-text
notes (e.g. "hoofdpijn"), which is a richer source than tags but needs
NLP to mine — deferred to `crash_v2` (see §4).

Every hypothesis test answers the question "what happens around a
crash". For the verdicts to be comparable across hypotheses, "a crash"
needs one fixed definition.

### Option A — Tag-based *(not selected for crash_v1)*
> A crash day = any `day_entries.date` where the day_entries record is
> tagged with `[fysiek] pem`.

- **Pros**: Ground truth from the user's own in-the-moment judgment.
  No threshold to pick.
- **Cons**: Tag discipline likely evolved over the 3.7 years — early
  entries may be under-tagged. May miss crashes the user didn't tag.
  Unknown how many days carry this tag (need to count before locking).
- **Risk**: If only ~20 PEM-tagged days exist, every test will be
  underpowered.

### Option B — Score-based, run-based *(LOCKED as crash_v1, threshold revised to absolute)*

**Final locked rule**: a crash episode = a run of ≥2 consecutive
`day_entries.date` rows with **score ≤ 3** (out of 1–6), with episodes
within 3 days of each other merged into one (dated to the first day of
the first run).
> *(Original definition before preflight)*: a crash episode = a run of
> ≥2 consecutive `day_entries.date` where the score is in the user's
> all-time personal bottom 15%, with the episode dated to the first day
> of the run.

- **Pros**: Objective, scale-agnostic, captures the multi-day nature of
  PEM (a single bad day may not be a crash).
- **Cons**: Threshold chosen ahead of test; doesn't use the PEM tag the
  user is already creating. A score of 2 next to a 5 still doesn't fire.
- **Risk**: Excludes acute single-day crashes that recovered next-day.
- **Preflight finding**: percentile-based threshold fails on tied
  scores. The 1–6 scale has 35.6% of days at score=4, so "personal
  bottom 15%" lands at "score ≤ 4" and covers ~50% of days. Replaced
  with an absolute threshold (see locked rule above).

### Option C — Combined *(not selected for crash_v1)*
> A crash episode = either:
>   - any day tagged with `[fysiek] pem`, OR
>   - a run of ≥2 consecutive days in the user's personal bottom 15%
>     of scores.
> Episodes within 3 days of each other are merged into one episode dated
> to its first day.

- **Pros**: Catches both labeled and unlabeled crashes. The merge rule
  prevents one drawn-out crash from being counted as several.
- **Cons**: Definition has two components; possible to have a tagged day
  that scores high, which would be surprising — log these as edge cases.
- **Risk**: Conflates two phenomena that may have different precursors.
  Mitigation: in each result, also break down by source ("of N crashes,
  M were tag-only, P were score-only, Q were both").

**Locked**: Option B.

The first action of every test will be to print the total count of
`crash_v1` episodes (and the underlying score distribution we derived
the bottom-15% threshold from), so we know whether each test is even
powered.

### `crash_v2` — extended classification (locked 2026-06-06)

`crash_v2` is a two-tier classification that retains `crash_v1` as
tier-1 unchanged and adds a tier-2 `dip` category for sub-threshold
events the v1 framework missed. Pre-registration, application
script, label CSV, and a descriptive dip-cluster overlay live at
[crash_v2-definition/](crash_v2-definition/).

Key points:
- **Tier 1 `crash`** = exactly `crash_v1`. A pre-registered
  slow-recovery filter was empirically removed (zero demotions on
  first run — every v1 episode has tail_median ≤ 5, a positive
  validation of the acute condition).
- **Tier 2 `dip`** = single isolated bad day (score ≤ 3, neighbours
  ≥ 4, excluding crash recovery shadow). 79 dips identified.
- **Dip cluster overlay** = transitive chains of ≥ 2 dips within
  7 days of each other. 15 clusters covering 45 of 79 dips.
  Descriptive only — per-day labels unchanged.
- **Hypotheses default to v1 labels** for backward compatibility;
  v2 labels are available via [labels_crash_v2.csv](crash_v2-definition/labels_crash_v2.csv)
  for re-runs that explicitly opt in (so far: H02b-on-dips,
  specificity-retag).

---

## 3. First batch of candidate insight-card hypotheses

Five candidates: four precursor-shaped (do biometric signals lead the
gevoelscore?) and one aftermath-shaped (what does recovery look like?).
A second batch will follow once we know which of these have spine.

Each entry below is a stub. Once locked, each gets its own
`hypothesis.md` with full pre-registration.

### H01 — Resting heart rate elevation before crashes
- **Claim**: In the 7 days before a `crash_v1` episode, the user's
  per-day RHR (from `UDSFile_*.json`) is consistently above their
  rolling-90-day baseline.
- **Why**: The Workwell foundation "RHR + 15" rule is the most
  established pacing indicator in ME/CFS / Long COVID. If true for this
  user, RHR drift becomes the simplest possible early-warning signal.
- **Pre-registered falsification**: At least 60% of crash episodes must
  show a mean lead-up RHR ≥3 bpm above baseline. Effect must hold in
  both train and validate windows.
- **Card it would enable**: an RHR-elevation precursor card. Exact copy
  drafted in `card.md` only after `result.md` is "supported", using real
  numbers from this user's data and a real quoted note where applicable.
- **Status**: **refuted** (see [H01-rhr-drift/result.md](H01-rhr-drift/result.md))
  — train and validate both fail all three criteria. Notably, validate
  window shows RHR *lower* in lead-up than baseline, not higher. Most
  plausible interpretations: (a) the user is well-paced enough that
  residual crashes aren't physical-exertion-triggered, (b) chronotropic
  incompetence blunting the signal, (c) `crash_v1` mixes mechanisms.
  Increases priority of H02 (stress, catches non-physical sympathetic
  load).

### H02 — Sustained stress elevation before crashes
- **Claim**: In the 3 days before a `crash_v1` episode, the daily count
  of stress samples (from monitoring_b `stress_level`) above 60 is
  consistently higher than the user's per-day median.
- **Why**: Sympathetic-overload precursor is in the pacing literature
  and we already know stress samples are present at ~1.400/day
  resolution.
- **Pre-registered falsification**: Crash-lead-up windows show at least
  20% more minutes-above-stress-60 than randomly-sampled matched
  3-day windows. Holds train + validate.
- **Card it would enable**: a sustained-stress precursor card. Drafted
  in `card.md` only after support.
- **Status**: **refuted** overall, **with a meaningful train-supported
  pattern** (see [H02-stress-elevation/result.md](H02-stress-elevation/result.md))
  — train: 79% of episodes had positive direction, median +2.7 stress
  points, discrimination +25.9 pp above null, passes crit b and c but
  fails crit a; validate: ~null with slight inversion. The train/validate
  asymmetry matches the recovery-cliff hypothesis precisely:
  pre-recovery crashes had a stress precursor; residual 2024+ crashes
  do not. Strengthens the case for "the kind of crash changed" and
  raises priority of H03 (sleep) as next test.

### H03 — Sleep efficiency / fragmentation before crashes
- **Claim**: In the 3–7 days before a `crash_v1` episode, mean nightly
  sleep efficiency (deep + light + REM seconds / total in-bed seconds,
  from `*_sleepData.json`) drops at least 5 percentage points below
  the user's 90-day baseline.
- **Why**: Sleep dysregulation is a recognised PEM precursor and the
  sleepData JSON has it daily across the full window.
- **Pre-registered falsification**: Less than 50% of crash episodes
  show the ≥5pp drop in lead-up nights. Holds train + validate.
- **Card it would enable**: a sleep-fragmentation precursor card.
  Drafted in `card.md` only after support.
- **Status**: **refuted** in both windows, decisively (see
  [H03-sleep-efficiency/result.md](H03-sleep-efficiency/result.md)). 0%
  of episodes and 0% of null windows crossed the −5 pp efficiency
  threshold; medians ~0. Sleep efficiency for this user is flat as a
  board. Does not rule out other sleep metrics (deep-fraction, REM
  fraction, total sleep time, fragmentation) — flagged as H03b for the
  second batch. The cross-hypothesis pattern now reads: pre-recovery
  crashes had a sympathetic-arousal precursor (H02 train) but no
  RHR or sleep-efficiency precursor — supporting the interpretation
  that the crashes were sympathetic-load precipitated, not sleep-debt
  precipitated.

### H04 — Body-battery net-drain elevated before crashes
- **Claim**: In the 3 days before a `crash_v1` episode, daily
  `bodyBattery.drainedValue − chargedValue` is consistently more
  negative than the user's 90-day median net delta.
- **Why**: Body Battery already fuses HR + HRV + stress in Garmin's own
  algorithm. If net drain leads crashes, this is a single-number proxy
  the user already understands.
- **Pre-registered falsification**: At least 60% of crash episodes show
  net-drain in the lead-up window worse than the bottom 25th percentile
  of all 3-day windows. Holds train + validate.
- **Card it would enable**: a body-battery-imbalance precursor card.
  Drafted in `card.md` only after support.
- **Status**: **refuted** in both windows (see
  [H04-body-battery/result.md](H04-body-battery/result.md)) but with
  the only positive-direction validate signal of any H01-H04
  (discrimination +13.3 pp, just below the +15 pp criterion; median
  −3.0, at the criterion). Train slightly inverted. Body battery's
  composite does not inherit H02 train's stress signal — the energy-
  envelope framing maps onto stress for this user, not onto the
  composite. The marginal validate hint may point at HRV (the one
  component we didn't test directly).

### H05 — Recovery-time pattern after crashes (aftermath, descriptive)
- **Claim** (descriptive, not predictive): After a `crash_v1` episode,
  the gevoelscore returns to within 1 point of the user's 30-day
  rolling median in a measurable, characterisable distribution
  (median, IQR, range).
- **Why**: This is the foundation card for the shielder-vs-reliever
  experiment the pacing-doc points to. We need to *first* know what
  recovery looks like before we can ask "did intervention X shorten it".
- **Pre-registered falsification**: Not applicable (descriptive).
  Success = a clean distribution with enough episodes (N ≥ 20) to
  characterise. Failure = too few crash episodes under `crash_v1`
  to map recovery at all.
- **No train/validate split**: descriptive characterisation, not
  prediction.
- **Card it would enable**: a recovery-comparison card for each crash
  episode. Drafted in `card.md` once the recovery distribution has been
  characterised. Uniquely, this card *only works* once enough episodes
  have accumulated to compare against.
- **Status**: **spec-induced trivial** (see
  [H05-recovery-time/result.md](H05-recovery-time/result.md)). The
  recovery target as pre-registered (`baseline − 1`) is met
  definitionally on the day after episode-end because of how `crash_v1`
  episodes are constructed. All 25 measured episodes recover in "0
  days." This is a finding about the spec, not about recovery — the
  data and crash_v1 detection are unaffected. **H05b** with a
  sustained-recovery target is queued (see §4 deferred).

---

### K01 — Crash depth shifted across eras *(see kind-of-crash-investigation.md)*
- **Status**: **suggestive_underpowered** (see
  [K01-crash-depth/result.md](K01-crash-depth/result.md)) —
  delta_median = +1.0 on 1-6 scale, mean +0.67; **0 of 15 late-era
  crashes reached score 1 vs 3 of 14 early-era**; permutation p =
  0.28 (fails ≤ 0.10 bar because the integer nadir scale makes the
  median brittle on small samples). Direction is unambiguous.

### K02 — Crash duration shifted across eras *(see kind-of-crash-investigation.md)*
- **Status**: **refuted by bar but with categorical tail-collapse
  finding** (see [K02-crash-duration/result.md](K02-crash-duration/result.md))
  — delta_median = −0.5 days (fails the −1 day bar); but mean dropped
  from 4.64 → 2.53 days (−2.11), and the **long-crash tail (≥5 days)
  shrank from 36% to 7% of episodes**. Permutation p = 0.095 (just
  clears 0.10 bar). Same median-brittleness lesson as K01.

## 4. Deferred to later batches

These are likely valuable but defer until the first batch has either
spine or doesn't:

- **Activity-load 24–72h before crashes** — boom-bust pattern. Partly
  overlaps with H02 (stress) and H04 (body battery); test after we know
  whether the simpler signals work.
- **Calendar-context corroboration** — once calendar binding lands and
  we have event-type tags. Card: "Three social events in the three
  days before this crash."
- **Pre-LC baseline calibration card** — "Your healthy-baseline RHR
  was 48; current baseline is 58; the gap is how far the system has
  moved." Uses the pre-2022-09 Garmin data we're otherwise excluding.
- **H02c — H02b sensitivity to spike-definition choices** — the locked
  H02b protocol used one operationalisation: contiguous run ≥ 5 minutes
  of samples ≥ 75. Other defensible shapes: ≥3 min, ≥10 min; threshold
  ≥60 vs ≥75 vs ≥85; aggregation as max-spike-per-day vs
  sum-of-spike-minutes vs count-of-distinct-spikes. **Goal of H02c**:
  run the H02b test across a grid of these choices and map the
  signal-to-noise boundary — find the spike severity × endurance
  combinations where conclusions still hold vs. where signal degrades
  into noise. Tells us how robust the H02b finding is and where the
  natural physiological "size" of a precursor-relevant spike lies for
  this user. Defer to a later batch.
- **H02d — sentinel handling and lead-up window for stress spikes**
  *(CLOSED 2026-06-06, refuted overall but with informative split:
  bridge × 5d train +31.8 pp, strongest train-window single-channel
  signal of the project; validate refuted across all 4 arm × window
  combinations.
  Result at [H02d-stress-spikes-uncensored/result.md](H02d-stress-spikes-uncensored/result.md);
  pre-registration at [H02d-stress-spikes-uncensored/hypothesis.md](H02d-stress-spikes-uncensored/hypothesis.md))*
  — two operationalisation gaps surfaced in H02b, both biased *against*
  the signal H02b targets:
  1. **Sentinel collapse.** H02b drops all stress values outside
     [1, 100] ([extract_daily_max_spike.py:116](H02b-stress-spikes/extract_daily_max_spike.py#L116)),
     conflating off-wrist (real missing data) with "too active"
     (Garmin refusing to compute when arousal exceeds the HRV-stress
     algorithm's reliability envelope). "Too active" is censored
     extreme arousal, not noise — discarding it can split a long
     spike (sentinel block ≤ 3 min stays inside the gap rule but
     breaks the `≥ 75` chain; > 3 min terminates the spike).
  2. **Lead-up window.** H02b uses `[D−3, D−1]` for cross-hypothesis
     comparability with H02. The lag profile measured *after* H02b
     was locked ([../activity-labels/output/lag_profile_report.md](../activity-labels/output/lag_profile_report.md))
     shows this user's empirical lag peaks at 5 days (+23.0 pp
     validate discrimination for HA01 at 5d vs +11.5 pp at 3d). H02b
     sits on the rising edge of the lag distribution and likely
     misses spikes at D−4 / D−5.

  **Locked H02d shape**: same metric family as H02b, but (a) classify
  each sentinel by HR-sample presence within ±60s (locked from an
  8-file stratified calibration — 100% sentinel coverage at 60s, 92.7%
  at 30s) and treat "too active" sentinels as ≥75 by imputation
  (primary); a bridge-only sensitivity arm runs alongside; (b) lead-up
  `[D−4, D−1]` primary (matching HA01b's locked window) and
  `[D−5, D−1]` secondary (matching the empirical lag peak). H02b stays
  as-locked; H02d is a new pre-registration on the same data, not a
  re-cut. Falsification bar identical to H02b's (60% / +15 pp /
  +5 min). If H02b refutes but H02d supports → the spike framing is
  correct; censoring and window were the bug.

  **Findings 2026-06-06**: imputation made the metric undiscriminating
  (null ≈ 85% at +10 min — flat-imputing all too_active as ≥75 is too
  generous; ~159 too_active samples/day average). Window extension
  worked exactly as the lag profile predicted: bridge train
  discrimination smoothly increased 3d→4d→5d (+29.9 → +27.6 → +31.8 pp).
  Validate refuted across all 4 arms — five tests now consistent that
  residual 2025+ crashes are *not* sympathetic-spike-precipitated.
- **Autonomic-channel sibling hypotheses HA06-HA12** *(family, queued 2026-06-06)*
  — pre-registration TODOs in [QUEUED-WORK.md "Autonomic-channel sibling
  hypotheses (HA06 family)"](../../QUEUED-WORK.md). Family of six
  hypotheses testing the overnight-recovery / autonomic-regulation
  mechanism through complementary channels, queued from Laure
  Wiggers' *Smartwatch Pacing* pdf (2025-07; cites Workwell +
  Bateman Horne + Ruijgt/Wüst 2025).
  - **HA06** *(CLOSED 2026-06-07, REFUTED both eras)* — bidirectional
    `|RHR − baseline| ≥ N` against the lagged baseline, 4-day primary
    + 5-day secondary lead-up window; sensitivity arm reports
    one-sided result and directionality split. Train freq=21.4%,
    disc=+13.9 pp (close to bar but fails crit a); **validate
    freq=0.0%** (0 of 15 crashes trigger — decisive refutation).
    N=10 and N=15 sensitivity checks vacuous (median max-|delta|
    sits at 1.6-3.5 bpm; pre-registered thresholds calibrated to
    Wiggers' / Workwell's RHR-variability range that exceeds this
    participant's actual range). Parasympathetic-swing
    contribution real but small (+7.1 pp train excess of
    bidirectional over one-sided). Result at
    [HA06-morning-rhr-delta/result.md](HA06-morning-rhr-delta/result.md).
  - **HA06b** *(CLOSED 2026-06-07, train SUPPORTED / validate
    REFUTED, overall REFUTED)* — same as HA06 but with relative
    threshold `|RHR − μ| / σ ≥ N_std` (N_std = 1.5 / 2.0 / 2.5)
    instead of absolute bpm. Pre-registered as a Theme-A-style
    methodological re-test after HA06's absolute thresholds were
    revealed mis-calibrated to this participant's RHR variability.
    Train **SUPPORTED at N_std=1.5 (71.4% freq, +18.9 pp disc,
    median |z|=2.31)** and at N_std=2.0 (+21.3 pp); validate
    refuted (53.3% freq, +0.8 pp disc — non-discriminative not
    inverse). Striking directionality split: train 70% elevated /
    30% lowered; **validate 25% elevated / 75% lowered** (Wiggers'
    parasympathetic-swing pattern empirically present in validate
    crashes at 75% but does not discriminate from null windows
    where the same pattern appears at similar rate). Sensitivity
    arm: validate one-sided elevated-only shows −16.2 pp disc —
    classical Workwell direction is anti-predictive in validate.
    Third train-era SUPPORTED autonomic-deviation precursor (after
    H02b, H02d) on a third channel. Result at
    [HA06b-rhr-zscore/result.md](HA06b-rhr-zscore/result.md).
  - **HA07** *(BLOCKED-PENDING-HARDWARE 2026-06-07)* — original
    day-over-day HRV drop hypothesis. After H04b path C
    authorisation, discovered the Forerunner 245 does NOT record
    HRV (HRV Status feature requires newer hardware introduced in
    Forerunner 255/265/955/965 / Fenix 7 generation). The
    `/hrv-service/hrv/{date}` endpoint returns an empty dict for
    every date sampled (2022-2026). Cannot run on this dataset.
    Substitute: **HA07c (sleep stress mean delta as HRV proxy)**.
  - **HA08** *(BLOCKED-PENDING-HARDWARE 2026-06-07)* — same
    blocker as HA07. Substitute: **HA08c (sleep stress slope as
    HRV-proxy creep)**.
  - **HA07c** *(CLOSED 2026-06-07, train SUPPORTED / validate
    refuted)* — substitute test for HA07 using sleep stress
    (HRV-derived during sleep) as proxy. Per-night mean sleep
    stress night-over-night delta, z-scored against lagged
    baseline. Sleep windows from local sleepData.json; per-minute
    stress from FIT files (no API dependency). 4d N_std=1.5
    one-sided elevated primary. **Train SUPPORTED at 69.2% freq +
    +23.2 pp disc + median signed z 1.677**. Validate refuted
    (40.0% / −6.0 pp). Multiple supporting arms (5d secondary
    elevated +18.4 pp, 4d N_std=2.0 lowered +26.0 pp, bidirectional
    +19.7 pp) confirm train signal robustness. **5th train-era
    SUPPORTED autonomic-channel precursor on the 5th channel**
    (after H02b, H02d, HA06b, HA11). The HRV-proxy validation:
    sleep stress as HRV proxy successfully discriminates train
    crashes. The HRV hypothesis itself remains untested
    (permanently, on this dataset). Result at
    [HA07c-sleep-stress-mean-delta/result.md](HA07c-sleep-stress-mean-delta/result.md).
  - **HA08c** *(CLOSED 2026-06-07, train SUPPORTED / validate
    refuted)* — substitute test for HA08. Trailing-5-day OLS
    slope of mean sleep stress, z-scored. Same data as HA07c.
    Primary 4d N_std=1.5 one-sided elevated: **TRAIN SUPPORTED at
    61.5% freq + +23.0 pp + median 2.116**. Validate refuted
    (40.0% / +1.5 pp). Notable validate ANTI-PREDICTIVE pattern
    at higher thresholds (N_std=2.0 bidirectional validate
    −36.2 pp, one-sided lowered −27.3 pp) — validate-era crashes
    are LESS likely than null windows to show large slope
    deviations. Validate crashes arrive against UNUSUALLY-FLAT
    baseline, not accumulating trend. **6th train-era SUPPORTED
    finding under clean methodology**; both acute (HA07c delta)
    and sustained (HA08c slope) modes confirmed in train. Result
    at [HA08c-sleep-stress-slope/result.md](HA08c-sleep-stress-slope/result.md).
  - **HA07d** *(CLOSED 2026-06-07, BOTH ERAS SUPPORTED at primary
    bidirectional → OVERALL SUPPORTED per the locked rule — FIRST
    PROJECT-LEVEL OVERALL-SUPPORTED TEST)* — substitute test
    measuring **night-over-night delta of in-sleep-window stress
    STDEV** (second-order primitive — HRV-of-HRV-proxy / autonomic
    variability). 4d N_std=1.5 bidirectional primary: **train
    SUPPORTED 84.6% freq, +19.6 pp; validate SUPPORTED 86.7% freq,
    +21.7 pp**. The bidirectional primary was crucial — one-sided
    arms reveal train SUPPORTS BOTH directions (elevated +27.4,
    lowered +16.5) while validate SUPPORTS ONLY the LOWERED
    direction (+21.7 pp at N_std=1.5, **+28.5 pp at N_std=2.0**).
    Validate-era discrimination peaks ABOVE HA10's previous best
    (+27.5 pp). The validate-era pattern is **autonomic stillness
    / freeze**: sleep stress variability DROPS in the days before
    validate-era crashes — the autonomic state becomes unusually
    stable, "looks like" great recovery, but symptoms continue.
    Combined with HA10 (elevated BB peak), validate-era crashes now
    have **two converging empirical anchors** both consistent with
    Wiggers' "freeze" / parasympathetic-swing pattern. **The
    project's first overall-SUPPORTED test under the canonical bar
    after 19 pre-registered hypotheses.** Card (b2) validate-era
    retrospective is now Tier 1 with two channel anchors. Result
    at [HA07d-sleep-stress-variability/result.md](HA07d-sleep-stress-variability/result.md).
  - **HA10** *(CLOSED 2026-06-07, train REFUTED / validate
    SUPPORTED, overall REFUTED — but VALIDATE-ERA SUPPORTED is a
    project first)* — morning BB peak z-score against lagged
    baseline (HIGHEST anchor, 03:00-10:00 timestamp window),
    4d primary + 5d secondary, bidirectional + one-sided arms.
    Train 50.0% freq + **−20.5 pp disc** (refuted; null rate 70.5%
    is high enough that train crashes trigger LESS than null);
    **validate 86.7% freq + +16.2 pp disc + median |z| 2.121 —
    SUPPORTED** (clears all three criteria; **first validate-era
    SUPPORTED test in the entire investigation**). Striking
    directionality reversal: train 0% elevated / 100% lowered
    (Wiggers' canonical direction); validate 69% elevated / 31%
    lowered (**paradoxical "swing" direction**). 5-day secondary
    each-era one-sided: **train SUPPORTED at +18.3 pp lowered;
    validate SUPPORTED at +27.5 pp elevated** — opposite-direction
    SUPPORTED in both eras at the 5d window. Cross-channel
    coherence with HA06b is striking: BB ∝ vagal tone (inverse to
    RHR) so the opposite-direction-per-era pattern is internally
    consistent — train sympathetic overarousal (high RHR ↔ low BB);
    validate parasympathetic swing (low RHR ↔ high BB). The
    **Wiggers "freeze" pattern is now empirically population-level
    visible** in two independent biometric channels for this
    participant. Pre-committed soft outcome: **HA10 SUPPORTED in
    validate → H04b strongly prioritised**. Card (b2) regains an
    empirical anchor. Result at
    [HA10-bb-overnight-recharge/result.md](HA10-bb-overnight-recharge/result.md).
  - **HA11** *(CLOSED 2026-06-07, train SUPPORTED / validate
    REFUTED, overall REFUTED)* — within-day U-dip event count
    z-scored against lagged baseline. Per-minute stress samples
    re-parsed from monitoring_b FIT files; U-dip event = sharp
    drop (≥ 25 points) from elevated baseline (S_pre ≥ 40)
    followed by plateau ≥ 5 points HIGHER than pre-dip baseline,
    refractory 60 min between events. Train **SUPPORTED at 4d
    N_std=1.5 one-sided elevated** (64.3% freq, +22.8 pp disc,
    median signed z = 2.168); also SUPPORTED at 4d bidirectional
    (+16.8 pp). Validate **refuted inverse-direction** (30.8% freq,
    −10.7 pp disc at 4d elevated, scaling to −24.1 pp at 5d
    N_std=2.0). Directionality split among triggering events:
    train 9/9 elevated (100%); validate 4/4 elevated (100%) — when
    they trigger they're uniformly elevated direction, but
    validate's trigger rate is below null. Wiggers' U-dip
    (orthostatic / electrolyte) pattern is empirically population-
    level present in pre-cliff era; absent / inverse in validate
    era. Fourth train-era SUPPORTED autonomic-channel precursor
    on the fourth channel (after H02b stress spike, H02d bridge ×
    5d sentinel-corrected, HA06b RHR z-score). Pre-cliff era's
    sympathetic-overarousal / orthostatic-instability precursor
    signature is now four-channel confirmed. Result at
    [HA11-stress-udip/result.md](HA11-stress-udip/result.md).
  - **HA09** *(work-on-later)* — parasympathetic-swing detection;
    multi-stage definition harder to pre-register cleanly;
    downstream of HA06's bidirectional reporting.
  - **HA12** *(work-on-later)* — pre-infection HRV rise; descriptive
    only; gated on notes-quality work for cleaner infection labels.
- **H02e — HR-modulated sentinel imputation** *(candidate, no spec yet)*
  — H02d's flat imputation of too_active as ≥75 over-counted ~159
  daily samples that are likely brisk walks, light exertion, or
  restlessness, not panic-grade arousal. Candidate H02e: only impute
  too_active as ≥75 when nearby HR exceeds a threshold (~100 bpm),
  filtering out the moderate-effort sentinels. Same window (4d/5d) and
  bar as H02d. Defer until the value vs. an HR-aware variant of HA01b
  is clear — both tests want HR magnitude information at the same
  sentinel minutes, and a unified extract step would serve both.

- **H02b — per-minute FIT stress samples (peak-spike count)** —
  **CLOSED 2026-06-05 (train-supported, validate near-miss).** H02 used Garmin's daily aggregate
  (averageStressLevel + highDuration). The original stub language was
  about "stress samples above 60" — a spike-count metric, not an
  average. The user has independently confirmed (2026-06-05) the
  experiential pattern: *an intense moment during an otherwise calm
  day can trigger a crash.* A daily average dilutes a 5-minute spike
  by 1.435 other minutes. The spike-count metric is built precisely
  for what the user describes. Re-run on the raw monitoring_b stress
  samples (~1.400/day) — proposed candidate metrics:
  count of stress samples ≥75 per day, peak stress sample per day,
  count of distinct ≥10-minute "intense windows" per day. To be tested
  after H04 finishes; ahead of H03b.
- **H04b — body battery intra-day dynamics** —
  **PROTOCOL LOCKED 2026-06-06**, execution pending notes-quality
  work. Full plan at
  [.claude/plans/adaptive-foraging-hamming.md](../../../../.claude/plans/adaptive-foraging-hamming.md).
  Folder scaffolded at [H04b-decode-unknown-233/](H04b-decode-unknown-233/)
  (empty, awaiting execution).

  User insight (2026-06-05): within-day body battery has two signal
  shapes worth testing — *rises* (catching active recovery, e.g.
  middagslaap) and *sharp drops* (catching discrete stress/exertion
  events through a different channel than pure stress samples). The
  *occurrence count* of BB-rise events is itself meaningful — not
  just totals or averages.

  This requirement (counting distinct intra-day events) **rules out
  the cheap option of using the 3 UDS timestamped points**
  (HIGHEST/LOWEST/MOSTRECENT can describe at most one transition).
  Per-minute BB is required.

  **2026-06-06 literature sweep confirmed no public decode of
  `unknown_233` exists** (HarryOnline community sheet lists it with
  a question mark; tcgoetz/Fit, GoldenCheetah, fitdecode, ANT forum,
  Garmin FIT-SDK forum — all treat it as unknown). A successful
  decode would be a small public contribution.

  Two parallel paths locked in the plan:
  - **(C) Garmin Connect REST API** via
    [`cyberjunky/python-garminconnect`](https://github.com/cyberjunky/python-garminconnect)
    — calls the internal endpoint
    `/wellness-service/wellness/bodyBattery/events/{date}` to pull
    per-minute BB. ToS-grey (general Terms of Use prohibit automated
    scraping; internal endpoints not covered by personal-use API
    agreement); accepted by participant for own-data analysis.
    Provides supervised labels.
  - **(B) Decode `unknown_233`** in monitoring_b FIT files using
    Path C labels as ground truth. ~12 candidate byte encodings to
    test (b3 direct, b2:b3 int16 scaled, byte-delta, off-wrist flag
    in b1, etc.) against a pre-registered 180-day holdout. Three
    fallback strategies specified if no direct encoding works
    (joint-channel regression, state-buffer reframing, raw-stream
    feature mining).

  Execution gated on the participant-requested notes label-quality
  work completing. Unblocks H03b (overnight BB recharge) and
  potential dip subtyping (dip_v2).
- **Dictionary v3 for notes — polarity-marker negation** — the v2
  three-layer model handles negation around symptom phrases but not
  around polarity markers. "het is echt **niet fijn**" fires
  `polarity_positive` because "fijn" matches. Fix: apply the same
  3-word negation window to polarity markers. Caught during
  late-positive-dominant verification 2026-06-05; small but real.

- **H03b — sharper sleep metrics** — H03 (efficiency) was refuted
  decisively. But efficiency averages over many sleep
  pathophysiologies. Candidate metrics for H03b: deep-sleep fraction,
  REM fraction, total sleep time, fragmentation count. Deferred to
  second batch unless H05 surfaces a sleep-recovery angle.
- **H05b — recovery time with sustained target** — H05 as
  pre-registered produced trivial 0-day recoveries because the
  recovery target (`baseline − 1`) was definitionally met by the day
  after episode-end. H05b candidate spec: recovery = first day of a
  ≥2-consecutive-day sustained run with `score ≥ pre-episode baseline
  rounded down`. Same data, same crash_v1 detection. Methodology
  lesson logged: small dry-runs catch spec artifacts that
  pre-registration alone does not.
- **Subtle-signal mining** — if every H01–H04 comes back refuted, dig
  into HRV proxies, respiration variance, SpO2 nocturnal dips,
  `unknown_233` decoding, etc.
- **Recovery-trajectory card (descriptive, long-arc)** — characterise
  the crash-frequency cliff itself: "your crash frequency dropped from
  ~10/year in 2023–24 to ~2/year in 2025–26." Foundation finding from
  the preflight (see [00-crash_v1-counts](00-crash_v1-counts/counts.md)).
  This is a different card shape from H01–H04 (precursor) or H05
  (per-episode recovery time) — it's the multi-year recovery arc, and
  would sit at the top of a retrospective view. Pair with calibration
  cards using the pre-LC Garmin data ("how far has the system moved")
  once both are settled.
- **`crash_v2` from notes (NLP-derived labels)** — *superseded
  2026-06-06*. The current `crash_v2` is a score-based two-tier
  extension (crash + dip) locked at
  [crash_v2-definition/](crash_v2-definition/), not the NLP-based
  refinement originally envisioned. The NLP angle now lives as
  the eventual notes-label-quality work + Goal B tagging-suggestion
  engine, both of which inform notes-derived labels but no longer
  carry the `crash_v2` name.
- **Dip subtyping (dip_v2)** — split the 79 v2 dips into
  "almost-crash" subtype (strong physiological precursor) vs
  "mood-only" subtype (no precursor). Initial evidence: H02b-on-dips
  showed a heterogeneous dip tier — top dips by spike delta are
  clear almost-crashes (e.g. 2024-03-30 with +77.6 min lead-up
  spike) while others have flat baselines. Defer until per-minute
  BB from H04b adds a second corroborating channel.
- **Shielder-vs-reliever intervention comparison** — needs H05 + an
  intervention-tag taxonomy. The eventual payload of this whole
  exercise.

---

## 4a. Synthesis

After all five hypotheses closed, a cross-batch synthesis was written
at [_archive/synthesis.md](_archive/synthesis.md) (archived 2026-06-13). It reads each refuted hypothesis
productively (what the data does and does not say), lists
caveats applying across the batch, and prioritises follow-ups. Living
document, last updated 2026-06-06 with the crash_v2 phase.

## 4b. Closed since 2026-06-05 (post-synthesis-v1)

- **H02b-trajectory (archived 2026-06-13)** ([_archive/H02b-trajectory-sub-files/trajectory-notes.md](_archive/H02b-trajectory-sub-files/trajectory-notes.md))
  — rolling 12-month discrimination curve replacing the binary
  H02b verdict; smooth ~12-month decay from +31.8 pp peak
  (mid-2023) to near zero by mid-2024.
- **S01 (archived 2026-06-13)** ([_archive/S01-stabilisation-trajectories/notes.md](_archive/S01-stabilisation-trajectories/notes.md))
  — 90-day rolling means of 4 metrics across the full Garmin
  window. Archived because the trajectory framing was qualitative,
  not a validated analytical era.
- **S02 score trajectory (archived 2026-06-13)** ([_archive/S02-score-trajectory/notes.md](_archive/S02-score-trajectory/notes.md),
  run 2026-06-07) — 90d rolling trimmed mean + median + score-level
  distribution of daily gevoelscore + pre-registered same-day rank
  correlation (§3.8) + four pre-registered S02b triggers (§7.2).
  Two triggers fired: **T1 inflection-date mismatch** (score peaks
  149 d before avg-stress, troughs 100 d before max-spike — score
  LEADS Garmin pendulum, opposite of the Wiggers patient-narrative
  direction T3 was set up for) and **T2 May 2026 channel divergence
  forward** (perturbation visible in 3/4 Garmin metrics but
  invisible in both the score 90d view and the zoom strip — score
  currently at its all-time-high in the tracked window). §3.8
  primary ρ (score × avg stress) = −0.0557 [−0.164, +0.009],
  ambiguous-underpowered at 16 effective blocks; all secondaries
  null. Distribution shows a clear tail-collapse on the worst end
  (score≤3 share 20% → 7%) AND a new upper mode (score=6 share
  2% → 12%); the central tendency moves modestly (trimmed mean
  4.35 → 4.72) because the rebalancing happens inside the trim
  region. S02b (T1-lag) and S02c (T2-divergence) executed same
  day — see following two entries.
- **S02b score-lead lagged correlation** ([S02b-score-lead/notes.md](S02b-score-lead/notes.md),
  run 2026-06-07) — daily-resolution Spearman ρ for score(t) ×
  avg-stress(t+149d) [primary] and score(t) × max-spike(t+100d)
  [secondary], lags pre-committed from S02's algorithm, NOT
  free-scanned. **REFUTED** on criterion (c) "lag improves over
  same-day": primary ρ_lag = +0.099 [+0.035, +0.203] vs matched
  same-day ρ = −0.097, |delta| = +0.002 (bar 0.10). Also fails (a)
  magnitude < 0.20 and (d) wrong sign (expected negative). Same-day
  and lagged ρ values are sign-flipped but nearly identical in
  magnitude (~0.10) — no daily-resolution lead/lag signal in
  either direction. Secondary at +100d also null
  (ρ = −0.025 [−0.090, +0.033]). **The rolling-curve T1 finding
  does NOT survive at daily resolution.** First direct
  cross-correlation lag test for [Wiggers H1](../../wiggers_progress_2026-06-07.md);
  empirically-observed score-leads direction refuted. Methodology
  lesson banked: rolling-curve turnaround-date mismatches can occur
  without daily-resolution lead/lag signals.
- **S02c May 2026 channel divergence (archived 2026-06-13)** ([_archive/S02c-may2026-divergence/notes.md](_archive/S02c-may2026-divergence/notes.md),
  run 2026-06-07) — daily-resolution z-score characterisation of
  the perturbation period (2026-03-08 → 2026-06-05, n=90) against
  a 180-day pre-perturbation reference window (2025-09-08 →
  2026-03-07). Descriptive only; no support/refute verdict.
  **The S02 T2 framing is substantively nuanced**: against the
  recent daily σ (not S01's 5-year trajectory σ), only RHR has any
  algorithmic onset (2026-05-14) and even RHR is below the
  "visibly worsening" 1.0σ bar (z_mean_pert = +0.82, reading
  "directional toward worsening, not clearly visible"). Other
  Garmin channels: avg_stress +0.24σ, max_spike +0.16σ, sleep eff
  +0.00σ — all "essentially unmoved." Score +0.07σ, also
  "essentially unmoved." Composite Garmin-worsen vs score gap =
  **+0.324σ** (small). Only one co-varying channel pair within
  window: avg_stress × max_spike (r = +0.61). Reading: at
  daily-resolution against recent baseline, the May 2026
  perturbation is modest and concentrated in RHR; the "score
  diverging from Garmin" framing is small in σ-units. Combined
  with S02b: at the daily timescale, score and Garmin live on
  largely-independent recent baselines.
- **K01 + K02** ([K01-crash-depth/result.md](K01-crash-depth/result.md),
  [K02-crash-duration/result.md](K02-crash-duration/result.md))
  — depth shallower, duration shorter; both refuted on bar but
  with categorical findings.
- **H02b specificity check** ([H02b-stress-spikes/specificity-check.md](H02b-stress-spikes/specificity-check.md))
  — characterised the 83 false-positive spike windows; 32 were
  `near_miss` (had a score-3 day crash_v1 missed).
- **Notes v1 + v2** ([notes/01-language-around-crashes/notes-summary.md](../../notes/01-language-around-crashes/notes-summary.md),
  [notes/02-categorize-clauses/categories-analysis-v2.md](../../notes/02-categorize-clauses/categories-analysis-v2.md))
  — clause-level language analysis with 3-layer dictionary
  (categories + modifiers + polarity). Surfaced symptom severity
  shift (+18 pp), mixed-day topology (+39 pp), lead-up language
  changes.
- **`crash_v2`** ([crash_v2-definition/](crash_v2-definition/),
  locked 2026-06-06) — two-tier (crash = v1 + dip), recovery filter
  empirically removed, 79 isolated dips identified, 15 dip clusters
  as descriptive overlay.
- **H02b on dips** ([crash_v2-definition/h02b_on_dips_result.md](crash_v2-definition/h02b_on_dips_result.md))
  — re-run of H02b's metric against the 79 dips. Refuted by strict
  bar (+9.1 train, +5.2 validate); ~3× weaker than crashes in train;
  validate-era convergence with crash signal.
- **Specificity re-tag** ([crash_v2-definition/specificity_retag.md](crash_v2-definition/specificity_retag.md))
  — 39% of original false positives now explained by crash_v2
  (24% v2 dips + 14% crash-adjacent).
- **`unknown_233` literature sweep + H04b plan** (2026-06-06) —
  no public decode exists; two-path protocol locked at
  [.claude/plans/adaptive-foraging-hamming.md](../../../../.claude/plans/adaptive-foraging-hamming.md).
- **Activity-labels v3.1** ([../activity-labels/](../activity-labels/),
  locked 2026-06-06) — per-day exertion-feature layer using
  personal-baseline-relative percentile-rank metrics (PEM-envelope
  framing). Iterated v1 (absolute thresholds, rejected) → v2
  (z-scores, broke on zero-heavy) → v3 (percentile rank) → v3.1
  (deprecate brittle push_burden_class binning per sensitivity
  test). Outputs `exertion_class` + `push_burden_7d` per day.
- **HA01 + HA02 + HA05** ([../activity-labels/output/ha_results.md](../activity-labels/output/ha_results.md))
  — 3-day lead-up window. All REFUTED. Surprisingly, dips show
  more activity-shock signal than crashes at 3-day (+9.3 vs +0.7 pp
  train).
- **HA01b + HA02b + HA05b** ([../activity-labels/output/ha_results_4day.md](../activity-labels/output/ha_results_4day.md))
  — 4-day lead-up window, pre-registered after participant's
  experiential PEM lag framing. **HA01b validate SUPPORTED at +17.3 pp**
  (93% of validate-era crashes have heavy/very_heavy exertion in
  the 4-day lead-up). **First SUPPORTED validate-era precursor of
  the whole investigation.** HA02b push burden still refuted at
  4-day. Implication: the "kind of crash changed" theory gains
  a "longer trigger lag" dimension — train-era 3-day H02b
  precursor, validate-era 4-day HA01b precursor.
- **Theme A baseline-contamination fix + bundled re-test
  pre-registration** ([../activity-labels/spec/severity_spec.md](../activity-labels/spec/severity_spec.md) §Lagged baseline,
  locked 2026-06-06) — adopted **A.1** (lagged baseline: rank
  against days [d-90, d-30], excluding the recent candidate
  window) and **A.2** (trend slope: OLS slope of
  log(1+`effective_exertion_min`) over the trailing 28 days) in
  response to user's Part 1 critique 2026-06-06. The 30-day
  rolling rank used in v3.1 absorbs sustained creeps into its
  own reference frame, so `push_burden_7d`'s discriminative
  power is least where risk is highest. A.1 fixes
  `push_burden_7d` (same metric, different reference frame);
  A.2 is a new metric for the creeping-floor pattern. Picked
  on theoretical grounds, not on outcome — A.3 (dual-EWMA)
  reserved as later refactor option.

  **Pre-registered BEFORE any rerun runs** (audit-trail anchor
  against motivated rescue):
  - **HA02c** — `push_burden_7d_lagged` → crash, train + validate
  - **HA01b-recomputed** — `exertion_class_lagged ∈ {heavy,
    very_heavy}` in 4-day lead-up → crash, train + validate

  **Bundled** (both run on the same A.1 reference, evaluated
  together) to maintain symmetric re-test discipline. Re-testing
  only the refutation (HA02) while keeping the win (HA01b) as-is
  would be selective rescue, which is p-hacking by another name.

  **Pre-committed SUPPORTED bar** for both: same as original
  (frequency ≥ 60%, discrimination ≥ +15 pp). If HA01b-recomputed
  falls below +15 pp on the lagged baseline, the addendum's
  "first SUPPORTED validate-era precursor" headline softens
  accordingly — honest accountancy.

  Implementation: [../activity-labels/scripts/11_compute_lagged_baseline.py](../activity-labels/scripts/11_compute_lagged_baseline.py).
  Outputs lagged ranks + slope columns extending
  `activity_features_daily.csv`. Bundled re-test scripts pending
  next on queue.
- **HA06 morning resting-HR delta (bidirectional, lagged baseline)**
  ([HA06-morning-rhr-delta/result.md](HA06-morning-rhr-delta/result.md),
  run 2026-06-07) — pre-registered as the autonomic-channel sibling
  test after Theme A refuted HA01b and H02d closed the stress channel
  for validate-era. Revised after Wiggers pdf input (2025-07) to be
  bidirectional, use the nightly lowest stable HR field, 4d primary +
  5d secondary, lagged baseline per Theme A. **REFUTED both eras**:
  train 21.4% freq + +13.9 pp disc (close but fails crit a);
  validate **0/15 crashes trigger** at the 5 bpm threshold —
  decisive refutation. Methodologically motivated re-test as HA06b
  with z-score thresholds followed in the same session.
- **HA06b RHR delta with relative thresholds (z-score)**
  ([HA06b-rhr-zscore/result.md](HA06b-rhr-zscore/result.md), run
  2026-06-07) — Theme-A-style methodological re-test of HA06 with
  participant-variability-normalised thresholds (`|RHR − μ| / σ
  ≥ N_std`; N_std = 1.5 / 2.0 / 2.5) instead of absolute bpm.
  Motivated by the locked `relative_not_absolute` feedback principle
  and HA06's revealed mis-calibration (median max-|delta| 1.6-3.5 bpm
  vs Wiggers/Workwell-calibrated 5 bpm primary floor). **Train
  SUPPORTED at N_std=1.5** (71.4% freq, +18.9 pp disc, median |z|
  2.31) **and at N_std=2.0** (+21.3 pp); validate refuted (53.3%
  freq, +0.8 pp disc — non-discriminative, not inverse).
  Directionality split striking: **train 70% elevated / 30% lowered;
  validate 25% elevated / 75% lowered** — Wiggers' parasympathetic-
  swing pattern empirically present in validate at 75% but does not
  discriminate from null. Sensitivity arm (one-sided elevated only)
  shows validate **−16.2 pp** (classical Workwell direction
  anti-predictive in validate). **Third train-era SUPPORTED
  autonomic-deviation precursor under clean methodology** (after
  H02b 3d spike-count, H02d bridge × 5d spike). Twelve pre-registered
  tests now consistent on validate-era precursor-invisibility under
  the canonical bar. **Methodology lesson banked**: pre-register
  relative thresholds (z-score or percentile rank) as the default
  for autonomic-channel tests; absolute thresholds drawn from
  external populations need re-calibration to participant
  variability *before* the test. Applies to HA07 (HRV channel) and
  HA10 (BB recharge) which should pre-register on relative
  thresholds from the start.
- **v2 threshold-sweep diagnostic round** (atomic, 2026-06-07,
  per user-locked Option C tightened) — four locked v2 diagnostic
  files run against locked v2 criteria
  ([methodology/threshold-sweep-rescue-criteria-v2.md](../methodology/threshold-sweep-rescue-criteria-v2.md))
  with the five-category shape rule (canonical decline /
  stable plateau / rising-late-peak / bumpy with sign changes /
  loose-tail noise) on the meaningful range [1.0, 3.0]:
  - **HA10 v2** ([HA10-threshold-monotonicity-diagnostic-v2/result.md](HA10-threshold-monotonicity-diagnostic-v2/result.md))
    — validate bidirectional **RESCUE** via Cat 3 (rising/late-peak).
    Restored as corroborating secondary anchor for validate-era.
  - **HA07d v2** ([HA07d-threshold-monotonicity-diagnostic-v2/result.md](HA07d-threshold-monotonicity-diagnostic-v2/result.md))
    — both eras **RESCUE**: train via Cat 3 (rising/late-peak),
    validate via Cat 2 (stable plateau) + Cat 3. Overall-SUPPORTED
    status restored. Sole primary anchor for validate-era; one of
    multiple load-bearing anchors for train-era.
  - **HA06b v2** ([HA06b-threshold-monotonicity-diagnostic-v2/result.md](HA06b-threshold-monotonicity-diagnostic-v2/result.md))
    — train bidirectional **CLOSE** via Cat 4 (2 sign-changes
    in [1.0, 3.0]: curve crosses zero at N_std=1.0 with disc
    −4.1, then at N_std=3.0 with disc −2.1; Spearman rho near
    zero +0.005; positive_across_rise fails because disc at
    N_std=1.0 is negative). **Permanently demoted to non-load-
    bearing.** Locked +18.9 pp SUPPORTED verdict stays on record.
    One of four anchors removed from the pre-cliff load-bearing
    list.
  - **HA11 v2** ([HA11-threshold-monotonicity-diagnostic-v2/result.md](HA11-threshold-monotonicity-diagnostic-v2/result.md))
    — train one-sided elevated **RESCUE** via Cat 1 (canonical
    decline; textbook robust shape; peak at N_std=1.25 with
    +45.4 pp; Spearman −0.683; sign-changes 0). Restored to
    load-bearing.

  **Restoration map**: HA10, HA07d (both eras), HA11 restored.
  HA06b train permanently demoted. The discipline binds in both
  directions per user-locked Option C — three RESCUES via
  principled v2 shape categories, one CLOSE via genuine shape
  fragility. The reviewer's symmetric-application critique was
  vindicated.

  **Methodology lesson banked**: v2 criteria become the project's
  locked methodology for any future threshold-sweep diagnostic.
  v3 escape hatch is strictly bounded (three required conditions:
  external authority, pre-locked inadequacy statement, symmetric
  re-application).

- **HA07d threshold-monotonicity diagnostic v1**
  ([HA07d-threshold-monotonicity-diagnostic/result.md](HA07d-threshold-monotonicity-diagnostic/result.md),
  run 2026-06-07 as positive-control follow-up to the HA10
  diagnostic) — fine N_std grid [0.5 → 4.0, 13 tiers] applied to
  HA07d's bidirectional primary in BOTH eras. **Verdict per
  locked rescue/close/ambiguous criteria v1: CLOSE BOTH ERAS.**
  Train: peak at N_std=1.75; Spearman rho +0.005; 4 sign changes
  (bumpy curve consistent with train autonomic-volatility
  hypothesis but failing the v1 monotonicity test). Validate:
  peak at N_std=1.75; Spearman rho +0.170 (positive — rising-
  with-threshold shape); 0 sign changes; **discrimination
  sustained +19 to +31 pp across N_std=1.0 through 4.0**
  (maximally robust signal that v1 criteria penalise because
  they only capture canonical-decline robustness). HA07d's
  locked SUPPORTED verdicts stay on record per audit-trail
  discipline; synthesis-level framing demotes HA07d to
  non-load-bearing per the locked v1 CLOSE clause.

  **Diagnostic-v1 criteria methodological defect acknowledged**:
  the v1 criteria only capture one robust shape (canonical
  decline) and penalise stable-plateau and rising-with-threshold
  shapes that are equally robust. **v2 criteria pre-registered**
  as a methodology document at
  [../methodology/threshold-sweep-rescue-criteria-v2.md](../methodology/threshold-sweep-rescue-criteria-v2.md)
  with a five-category shape rule. **v2 diagnostics pre-
  registered as separate locked diagnostic.md files for HA10,
  HA07d, HA06b, HA11** — symmetric application across the test
  family per user-locked Option C.

  Effect of v1 CLOSE both eras:
  - Card (b2) validate-era retrospective loses its sole anchor
    on top of having lost HA10. NO LOAD-BEARING ANCHOR in v1
    framework. Cannot ship anchored.
  - Project effectively has NO load-bearing overall-SUPPORTED
    test under v1 diagnostic criteria.
  - Era-as-moderator narrative weakens to "supported by
    physiological consistency across multiple non-load-bearing
    findings."
  - v2 outcomes will decide whether load-bearing status is
    restored or demotion is permanent.

- **HA10 threshold-monotonicity diagnostic v1**
  ([HA10-threshold-monotonicity-diagnostic/result.md](HA10-threshold-monotonicity-diagnostic/result.md),
  run 2026-06-07 in response to the [independent peer review §3](../review/2026-06-07-variable-architecture-review.md)
  fragility critique) — fine N_std grid [0.5 → 4.0, 13 tiers]
  applied to HA10's validate-era 4d bidirectional primary.
  **Verdict per locked rescue/close/ambiguous criteria v1: CLOSE.**
  Peak at N_std=1.75 (+19.5 pp), one σ-tier past the rescue window
  [1.0, 1.5]. Other shape criteria PASS (disc +14.0 at N_std=2.0,
  +11.0 at 2.5; Spearman rho −0.456; one sign change). Per locked
  rule any close criterion triggers CLOSE; peak-location failure
  is the only close trigger. **HA10's locked SUPPORTED verdict
  stays on record** (pre-registration discipline). But synthesis-
  level framing demotes HA10 to non-load-bearing per the locked
  CLOSE clause. Important nuance: HA10's one-sided ELEVATED arm
  (the paradoxical-swing direction Wiggers documents) shows robust
  threshold-monotonicity (+23 pp plateau N_std=1.5 → 2.5); the
  DIRECTION is supported, only HA10's specific bidirectional-
  primary choice failed the diagnostic. **Action**: card (b2)
  drops HA10 anchor; HA07d becomes the sole load-bearing
  validate-era anchor. Methodology lessons banked: threshold-
  monotonicity diagnostic added to project methodology playbook
  for any test with primary SUPPORTED at loosest tier only;
  directional pre-registration may need to match the physiological
  hypothesis more tightly than bidirectional-default does.

- **HA07d sleep stress variability delta (z-score, BIDIRECTIONAL)**
  ([HA07d-sleep-stress-variability/result.md](HA07d-sleep-stress-variability/result.md),
  run 2026-06-07) — substitute test for the blocked HA07; second-
  order primitive (HRV-of-HRV-proxy = autonomic flexibility shift).
  Per-night stdev of in-sleep-window stress samples, night-over-
  night delta, z-scored against lagged baseline. Bidirectional
  primary (physiological direction a priori ambiguous). **PRIMARY
  4d N_std=1.5: train SUPPORTED (84.6% freq, +19.6 pp); validate
  SUPPORTED (86.7% freq, +21.7 pp) → OVERALL SUPPORTED per the
  locked both-eras rule.** First overall-SUPPORTED test in the
  19-hypothesis H##/HA## series. Validate-era discrimination
  reaches **+28.5 pp at N_std=2.0 one-sided lowered** (variability
  collapse) — exceeds HA10's previous validate best (+27.5 pp).
  Train SUPPORTS BOTH directions at N_std=1.5; validate SUPPORTS
  ONLY lowered direction. The validate-era pattern is **autonomic
  stillness/freeze**: sleep stress variability vanishes before
  validate-era crashes — autonomic state becomes unusually stable
  while symptoms continue. Combined with HA10 (elevated morning BB),
  validate-era now has two converging empirical anchors both
  consistent with Wiggers' "freeze" / parasympathetic-swing
  pattern. **Major project shift**: the era directionality
  reversal is now a single-channel both-eras-SUPPORTED finding (not
  cross-channel inference). Card (b2) validate-era retrospective
  promoted to Tier 1 with two anchors.

- **HA08c sleep stress mean slope (z-score, one-sided elevated)**
  ([HA08c-sleep-stress-slope/result.md](HA08c-sleep-stress-slope/result.md),
  run 2026-06-07) — substitute test for the blocked HA08.
  Trailing-5-day OLS slope of nightly mean sleep stress. **Train
  SUPPORTED at 4d N_std=1.5 (+23.0 pp, 61.5% freq, median 2.116);
  validate refuted (40.0% / +1.5 pp).** 5d secondary one-sided
  elevated train also SUPPORTED (+23.2 pp, 69.2%). Strong validate
  ANTI-PREDICTIVE pattern at higher thresholds — validate-era
  crashes arrive against unusually-flat baseline (sleep stress
  variability collapse hinted at HA07d's later finding). **Sixth
  train-era SUPPORTED finding** under clean methodology; both
  acute (HA07c delta) and sustained (HA08c slope) modes
  SUPPORTED in train on the same channel.

- **HA07c sleep stress mean delta (z-score, one-sided elevated)**
  ([HA07c-sleep-stress-mean-delta/result.md](HA07c-sleep-stress-mean-delta/result.md),
  run 2026-06-07) — substitute test for the blocked HA07 using
  sleep stress (Garmin's HRV-derived stress, isolated to the sleep
  window when activity ≈ 0) as HRV proxy. Stage 1 extraction
  re-parsed monitoring_b FIT files (1707 valid nights with ≥120
  per-3-min samples within local-sleepData.json sleep windows).
  Night-over-night delta of mean sleep stress, z-scored.
  **Primary 4d N_std=1.5 one-sided elevated: TRAIN SUPPORTED
  (+23.2 pp, 69.2% freq, median 1.677); validate refuted
  (-6.0 pp).** Multi-arm robustness: 4d N_std=2.0 bidirectional
  +19.7 pp SUPPORTED, 4d N_std=2.0 lowered +26.0 pp SUPPORTED, 5d
  arms also SUPPORTED. Train signal is robust to direction +
  threshold + window choice. Directionality split among triggers:
  train 33% elevated / 67% lowered-at-max-|z| — train-era crashes
  preceded by HIGH AUTONOMIC VOLATILITY (large shifts in both
  directions, downward direction at higher thresholds is the
  strongest discriminator). **5th train-era SUPPORTED autonomic-
  channel precursor on the 5th channel.** The HRV-proxy is
  validated for train; the HRV hypothesis itself remains
  permanently untestable on this dataset.

- **API path C smoke test + sleep backfill** (2026-06-07) —
  garminconnect library authenticated successfully; cached token
  at `~/.garminconnect_tokens/`. Smoke test on 2026-05-15
  confirmed Body Battery, Sleep, and per-minute stress endpoints
  respond cleanly. **HRV endpoint returns empty for all dates**
  (the FR245 hardware does not record HRV; HRV Status feature
  requires newer Forerunner 255/265/955/965 / Fenix 7 hardware).
  Per-minute sleep stress arrays from the API are populated only
  for recent dates (2026+) — older dates return empty arrays even
  though FIT files capture per-minute stress. Decision: pivot
  HA07c/HA08c/HA07d to use LOCAL FIT data + LOCAL sleep window
  timestamps (works for full corpus); H03b stays on API backfill
  (running in background; recent dates populated for validate-era
  BB sharpening). Original HA07 / HA08 hypothesis.md files marked
  BLOCKED-PENDING-HARDWARE for audit trail. Substitute pre-
  registrations (HA07c / HA08c / HA07d) locked **before** any
  data was inspected — pre-registration discipline preserved.

- **HA11 within-day stress U-dip event count (z-score, one-sided
  elevated primary)** ([HA11-stress-udip/result.md](HA11-stress-udip/result.md),
  run 2026-06-07) — pre-registered after HA10 as the second
  user-confirmed pivot test (HA10 → HA11). Re-parsed all 7888
  monitoring_b FIT files in Stage 1 (~6-7 min, 1739 days, 1722
  valid ≥600 samples, 1469 total U-dip events) to produce per-day
  u_dip_count primitive; U-dip event = sharp drop ≥ 25 stress
  points from a S_pre ≥ 40 baseline followed by a plateau ≥ 5
  points higher than baseline, refractory 60 min. Distribution:
  47% of valid days have 0 events, 31% have 1, 14% have 2, 7% have
  3+. **Train SUPPORTED at 4d primary N_std=1.5 one-sided elevated
  (64.3% freq, +22.8 pp disc, median signed z = 2.168)**; also
  SUPPORTED at 4d bidirectional (+16.8 pp). **Validate refuted
  inverse-direction** (30.8% freq at 4d elevated, −10.7 pp disc;
  scales to −24.1 pp at 5d N_std=2.0). Validate-era crashes have
  *fewer* U-dip events than typical 4-5d windows — the inverse-
  direction signal is itself a *characteristic* signature of the
  parasympathetic-swing era. Directionality split among triggering
  events: train 9/9 elevated (100%), validate 4/4 elevated (100%) —
  triggering is direction-pure (lowered direction is structurally
  rare because U-dip count is bounded below by 0). Same-day
  Spearman ρ between u_dip_count and gevoelscore is essentially
  zero (train +0.075, validate +0.012) — U-dip is a 4-day-lead
  precursor in train, not a same-day symptom correlate.

  **Implications:**
  - **Fourth train-era SUPPORTED autonomic-channel precursor on
    the fourth channel** (after H02b stress spike count, H02d
    bridge × 5d sentinel-corrected, HA06b RHR z-score). The pre-
    cliff era's sympathetic-overarousal precursor signature is
    now four-channel-confirmed across distinct measurement
    modalities (per-minute stress trajectory, per-night autonomic
    state, per-day within-day pattern). Strongest multi-channel
    convergence in the project.
  - **Wiggers' U-dip pattern is empirically population-level real
    for pre-cliff era, absent / inverse for post-cliff era**. Her
    qualitative description fits the train era's autonomic state;
    validate-era crashes' parasympathetic-dominance state does
    not produce U-dip events.
  - **Card (b) train-era retrospective per-crash card now has
    FOUR converging empirical anchors** (H02b + H02d + HA06b +
    HA11). Strongest anchoring for any card concept in the project.
  - **HA10 remains the only validate-era SUPPORTED test**; HA11
    does not contribute to validate-era anchoring.
  - HA09 (parasympathetic-swing detection) reframing reinforced
    again — validate-era crashes characterised by absence of
    sympathetic-arousal patterns (NOT presence of swing patterns
    discriminating from null per HA06b finding).
  - H04b path C authorisation priority unchanged from HA10's
    SUPPORTED-validate finding (still strongly prioritised).

  Doc updates pending for next bundle.

- **HA10 BB overnight recharge coarse proxy (z-score, bidirectional)**
  ([HA10-bb-overnight-recharge/result.md](HA10-bb-overnight-recharge/result.md),
  run 2026-06-07) — pre-registered after HA07 was blocked on data
  availability (HRV not in any local source); pivoted to HA10 as the
  next operationalisable autonomic-channel test from the 3 daily
  UDS BB anchors. Morning BB peak = HIGHEST anchor's statsValue
  filtered to 03:00-10:00 local timestamp; z-scored against lagged
  baseline [d-90, d-30]; thresholds N_std = 1.5 / 2.0 / 2.5
  consistent with HA06b. Primary 4d bidirectional N_std=1.5:
  **train REFUTED (50.0% freq, −20.5 pp disc); validate SUPPORTED
  (86.7% freq, +16.2 pp disc, median |z|=2.121)** — overall REFUTED
  per the locked both-eras rule, but the **validate-era SUPPORTED
  is the project's first validate-era SUPPORTED test under clean
  pre-registration**. Striking directionality reversal: **train 0%
  elevated / 100% lowered** (Wiggers' canonical "didn't recharge"
  direction); **validate 69% elevated / 31% lowered** (paradoxical
  "looked like a great night but" direction). 5-day secondary:
  **train SUPPORTED at +18.3 pp one-sided lowered AND validate
  SUPPORTED at +27.5 pp one-sided elevated** — both eras SUPPORTED
  in opposite directions, the cleanest era-directionality reversal
  in the project. Cross-channel coherence with HA06b is striking:
  BB ∝ vagal tone (inverse to RHR), so opposite-direction-per-era
  pattern is internally consistent — train sympathetic overarousal
  (high RHR ↔ low BB); validate parasympathetic swing (low RHR ↔
  high BB). The Wiggers "freeze" pattern is now empirically
  population-level visible in two independent channels.
  Pre-committed soft outcome held: **HA10 SUPPORTED in validate →
  H04b strongly prioritised**.

  **Implications:**
  - First validate-era SUPPORTED precursor in the project under
    canonical bar (13 prior pre-registered tests refuted in
    validate; HA10 4d primary bidirectional validate passes all
    three criteria).
  - D7 single-mechanism-two-regimes reframe gains its first
    empirical validate-era anchor.
  - Card (b2) validate-era retrospective regains an empirical
    anchor — promote back from Tier 2 to Tier 1 candidate pending
    H04b per-minute trajectory enrichment.
  - H04b path C authorisation priority increases sharply.
  - HA11 still next on queue per user pivot order.

  Doc updates pending for next bundle (after HA11).

- **Theme A bundled re-test RESULT** ([../activity-labels/output/ha_results_4day_lagged.md](../activity-labels/output/ha_results_4day_lagged.md),
  run 2026-06-06) — pre-registered HA02c + HA01b-recomputed bundle on
  the A.1 lagged baseline. **Both tests REFUTED** at the pre-committed
  bar. HA01b-recomputed: train +5.8 pp (refuted), validate **+4.0 pp**
  (refuted) — vs the original rolling-baseline result of train +8.6 pp,
  validate +17.3 pp. The **-13.3 pp delta on the validate side** means
  the original "first SUPPORTED validate-era precursor" headline was
  substantially a rolling-baseline construction artifact. HA02c:
  train -18.7 pp, validate +0.7 pp (refuted both windows; push burden
  is genuinely not a precursor for this person on either reference
  frame; Theme A improves measurement-theoretic standing but does not
  resurrect it as a predictor). Sample caveat: 3 of 14 train crashes
  fell inside the 90-day lagged-rank boundary and were dropped from
  the train-side test; validate side has all 15 crashes clean and is
  decisively refuted independent of the dropped train crashes.

  **Implications:** the "kind of crash changed" theory's "longer
  trigger lag" extension (train-era H02b 3-day stress-spike paired
  with validate-era HA01b 4-day activity-shock) does not hold up on
  a clean baseline; the validate-era counterpart vanishes. The D7
  one-mechanism-two-regimes reframe becomes harder to support;
  HA06 (morning resting-HR delta) becomes the next pre-registered
  candidate to provide an empirical stake. Card (b2) loses its
  Tier-1 empirical anchor — downgraded to Tier 2 in
  [STOCKTAKE §4](../../STOCKTAKE.md). The pre-committed honesty
  discipline (re-test bundled, bar held at original level, audit
  trail dated before reruns ran) functioned as designed — the
  artifact was surfaced before it hardened into a long-lived headline.

  Doc updates landed in the same session:
  [RESEARCH-REPORT-ADDENDUM.md §5.9](../../RESEARCH-REPORT-ADDENDUM.md),
  [STOCKTAKE.md §2a + §4 + §7](../../STOCKTAKE.md),
  [_archive/synthesis.md](_archive/synthesis.md) "Update 2026-06-06 (later still)".

- **HA01b per-axis decomposition diagnostic** ([HA01b-per-axis-diagnostic/result.md](HA01b-per-axis-diagnostic/result.md),
  run 2026-06-07) — pre-registered under the user-locked Option A
  testing playbook ([../methodology/testing-playbook.md](../methodology/testing-playbook.md)),
  the **first diagnostic locked under the consolidated playbook §9
  compliance bar**. Decomposed HA01b's `exertion_class_lagged`
  composite into its 4 input axes (effective_exertion, step_burden,
  max_hr_peak, vigorous_min) and asked: would any single axis, if
  pre-registered as primary, have produced a SUPPORTED verdict?

  **Finding**: **effective_exertion SUPPORTED both eras** at the
  locked 3-criterion bar (train +21.3 pp, validate +19.5 pp, freq
  80-82%, median rank on triggering 0.88-0.91). step_burden SUPPORTED
  validate-only (train misses crit-c by 0.008); vigorous_min
  SUPPORTED validate-only (train misses crit-b at +10.7 pp);
  max_hr_peak REFUTED both eras (validate inverted at -7.7 pp,
  consistent with chronotropic incompetence). Composite control
  reproduces HA01b REFUTED both eras (+3.4 / +1.5 pp) — confirms the
  diagnostic is honestly extracting signal the composite obscured.

  **Why composite REFUTES while per-axis SUPPORTS**: the composite
  `MAX(rank) ≥ 0.75` fires in ~78% of null windows; spread vs crashes
  (~80%) is tiny. Per-axis trigger drops null rate to ~60%, lifting
  discrimination to ~+20 pp. This is a generalisable lesson about
  MAX-rank composites diluting per-axis signal in the null
  distribution (queued for playbook §3 addendum).

  **Verdict framing**: the locked HA01b composite REFUTED verdict
  STAYS on record. Per playbook §5.2, this diagnostic produces a
  **diagnostic finding**, NOT a re-test verdict. The both-eras
  rule (playbook §4.4) reduces load-bearing axes to 1
  (effective_exertion). step_burden and vigorous_min validate-only
  findings are noted but NOT promoted.

  **Specificity reality check (per playbook §6.2)**: even at +19.5 pp
  validate, posterior-per-fire is ~2.2% vs 1.7% base rate (60% of
  any 4-day window in the analysis range triggers). NOT shippable as
  a card without further refinement.

  **Cross-axis correlation matrix**: Spearman 0.31-0.69 across the 4
  axes; effective_exertion is the "central" axis (mean ρ ≈ 0.58).
  Effective N of comparisons ≈ 2.5 (not 4) — multi-comparison concern
  bounded but real.

  **Pre-committed follow-ups** (locked under HA01b per-axis
  diagnostic §6 BEFORE the run): HA01c (effective_exertion as
  primary, same threshold) + HA01c v2 threshold-monotonicity
  diagnostic. Both locked 2026-06-07.

- **HA01c effective-exertion shock (per-axis re-formulation)**
  ([HA01c-effective-exertion-shock/result.md](HA01c-effective-exertion-shock/result.md),
  run 2026-06-07; **SUPPORTED both eras at locked threshold**) —
  pre-committed follow-up triggered by HA01b per-axis diagnostic's
  both-eras SUPPORTED finding on effective_exertion. Primary:
  `effective_exertion_rank_lagged ≥ 0.75` in 4-day lead-up. Same
  3-criterion bar as HA01b composite; both-eras rule applies.

  **Locked verdict**: SUPPORTED both eras at the locked 0.75
  threshold. Train: 81.8% freq, +21.3 pp disc, median rank 0.883
  (n_clean=11; 3 train crashes dropped to lagged-baseline warmup).
  Validate: 80.0% freq, +19.5 pp disc, median rank 0.909
  (n_clean=15, all crashes retained). Numbers identical to per-axis
  diagnostic (same data, seed, threshold; disciplinary re-run, not
  informational). HA01b composite REFUTED stays on record per
  playbook §2.2 (HA01c is a separate hypothesis with a different
  primary, not a re-test).

  **Load-bearing status**: gated on v2 RESCUE per HA01c
  hypothesis.md §5 co-lock. See HA01c v2 entry below.

- **HA01c v2 threshold-monotonicity diagnostic**
  ([HA01c-threshold-monotonicity-diagnostic-v2/result.md](HA01c-threshold-monotonicity-diagnostic-v2/result.md),
  run 2026-06-07; **MIXED v2 verdict**) — 5th v2 diagnostic in the
  v2 round (after HA10, HA07d, HA06b, HA11). Tested 8 rank
  thresholds {0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95} per
  rank-adapted locked five-category shape rule (Cat 1 peak in
  [0.50, 0.70]; Cat 3 peak ≥ 0.80; sign-changes in [0.60, 0.90]).

  **Train v2: AMBIGUOUS** (first AMBIGUOUS in the v2 series). Shape
  is bumpy-but-never-negative: 15.4 → 6.4 → 16.2 → 21.3 → 10.3 →
  7.9 → 2.0 → 7.3. Peak at τ=0.75 (+21.3 pp). Fails Cat 1 (peak
  not in [0.50, 0.70]), Cat 2 (range too wide), Cat 3 (the
  0.50→0.60 drop breaks monotone rise to peak), Cat 4 (0
  sign-changes — never crosses zero), Cat 5 (peak too high).
  Genuine edge case the locked rule doesn't categorize.

  **Validate v2: RESCUE via Cat 1**. Textbook canonical decline:
  15.4 → 24.6 → 21.0 → 19.5 → 13.3 → 13.3 → 12.3 → 6.7. Peak at
  τ=0.60 (+24.6 pp), monotone decline beyond, Spearman ρ = -0.850.
  Cleanest Cat 1 shape in the v2 round.

  **Mixed verdict per playbook §4.4 both-eras rule**: HA01c stays
  **SUPPORTED-with-stability-mixed** — honest at τ=0.75 but
  **NOT load-bearing**. effective_exertion's train-arm
  threshold-stability is undecided under the locked v2 framework.

  **Discipline binds**: this is the first AMBIGUOUS verdict in the
  v2 series. The locked criteria correctly surface the edge case
  rather than forcing a fit. The user pre-committed to the
  framework; the framework returned mixed; load-bearing status is
  withheld per pre-commitment.

  **No HA01c card.md drafted**: per playbook §2.7 card-craft rule
  (only if result.md is SUPPORTED + specificity tables pass) AND
  §6.2 (2.2% posterior per fire vs 1.7% base rate already blocked
  card draft regardless of v2 outcome). Card direction: NOT shipped
  without further refinement (tighter threshold + additional
  conditions or temporal aggregation).

- **H03b per-minute BB overnight recharge**
  ([H03b-bb-overnight-recharge-permin/result.md](H03b-bb-overnight-recharge-permin/result.md),
  run 2026-06-07; **INCONCLUSIVE × 12 by data availability**) —
  pre-registered as the sharpening test of HA10 (per-minute
  trajectory vs HA10's 3-anchor proxy). Data-availability
  investigation 2026-06-07 surfaced TWO Garmin API cutover dates:
  (1) `bodyBatteryChange` daily scalar populated from ~2023-12-31;
  (2) `sleepBodyBattery` per-3-min array populated from ~2024-06-03.
  H03b needs the per-3-min array; only 6 of 15 validate crashes
  have both data AND a usable lagged baseline (the baseline window
  [d-90, d-30] needs ≥40 valid days, which only stabilises ~Sept
  2024). Train (14 crashes) has zero coverage.

  **Locked n_clean ≥ 10 threshold from hypothesis.md §5 binds**:
  all 12 evaluation cells (3 N_std × 2 windows × 2 eras) return
  INCONCLUSIVE. User pre-committed (2026-06-07) to running H03b
  as-locked and accepting the verdict rather than lowering the
  threshold mid-run (which would be a spec change requiring an
  H03c per playbook §2.2).

  **Endpoint clarification audit trail (per playbook §2.5)**:
  hypothesis.md §3 specified the
  `/wellness-service/wellness/bodyBattery/events/{date}` endpoint;
  this actually returns event records (sleep/activities/naps), not
  per-minute samples. The per-3-min BB during sleep window IS
  available via `get_sleep_data().sleepBodyBattery`, which already
  came along with the path C sleep backfill — no separate BB
  backfill needed. This is an implementation-source clarification,
  not a spec change.

  **HA10 stays canonical for BB overnight recharge channel**:
  HA10 already SUPPORTED validate at +16.2 pp (coarse 3-anchor
  proxy on full corpus) + v2 RESCUE Cat 3. The sharpening test
  cannot be performed on the API data alone; H03b is re-runnable
  only after path B (FIT decode of `unknown_233`) unlocks
  per-minute BB for the old corpus.

  **No card.md drafted** (INCONCLUSIVE cannot lead to card per
  playbook §2.7).

  **Methodology lesson banked**: when a pre-registered hypothesis
  depends on a third-party API endpoint, verify data availability
  across the analysis window BEFORE locking the inconclusive
  threshold. Queued for playbook §3 addendum consideration.

- **Tier 2 specificity tables for load-bearing anchors**
  ([../cards/card-b-train-specificity.md](../cards/card-b-train-specificity.md)
  + [../cards/card-b2-validate-specificity.md](../cards/card-b2-validate-specificity.md),
  computed 2026-06-07; **all 9 anchors land in Tier C**) — Tier 2
  peer-review action item completed. Locked spec at
  [../methodology/specificity-tables-spec.md](../methodology/specificity-tables-spec.md);
  derivative Bayes computation over locked result-data.json files
  (no new hypothesis tests, no new null draws).

  **Locked era day counts + base rates**: train 14/485 = 2.89%;
  validate 15/887 = 1.69%.

  **Results summary**: best train anchor is H02b 3d at **4.87%
  precision, 1.69× lift**; best validate anchor is HA07d 4d at
  **2.24% precision, 1.33× lift**. Zero anchors reach Tier B
  (precision ≥ 5% AND lift ≥ 2×) or Tier A (≥30% + ≥5×).

  **Structural insight**: lift ≈ recall/null_fire is independent
  of base rate; no anchor's recall/null_fire ratio exceeds 2×, so
  the 2× lift threshold cannot be cleared at any base rate. The
  hypothesis-test 3-criterion bar confirms discrimination between
  crash and null windows but does NOT confirm forward-predictive
  viability.

  **Card framing implications**: Card (b) train-era and Card (b2)
  validate-era both restricted to **retrospective-annotation-only
  surfaces** per playbook §6.6 no-go list. The acceptable surface
  is timeline annotation during after-the-fact review, paired with
  the gevoelscore record. Applies to HA07d (project's only
  overall-SUPPORTED + v2-validated finding) as well.

  **Methodology lesson**: a hypothesis-test bar clearance and a
  card-shippable precision are different gates. Future card
  pre-registrations should include specificity-table thresholds in
  the hypothesis.md, not deferred to a downstream check.

- **Tier 2 statistical audits — Fisher's exact + cross-channel
  correlation** ([../cards/primary-verdict-statistics.md](../cards/primary-verdict-statistics.md)
  + [../cards/cross-channel-correlation.md](../cards/cross-channel-correlation.md),
  computed 2026-06-08) — two cheap derivative computations over
  locked result-data.json files and per-day primitive CSVs. No new
  hypothesis tests, no new null draws.

  **Fisher's exact + 95% CIs on 11 primary verdicts**: only **H02b
  train (p=0.029) and H02d bridge × 5d train (p=0.011)** reach
  α=0.05 one-sided. Zero reach Bonferroni α=0.005. HA07d train
  +19.6 pp → p=0.0934; HA07d validate +21.7 pp → p=0.0703; HA10
  validate +16.2 pp → p=0.1475; HA01c train/validate → p=0.136/0.109
  — all fail α=0.05. The project's 60%/+15pp/magnitude bar is
  more permissive than conventional α=0.05 statistical
  significance with n=14-15 crashes. This is a conscious choice
  for n-of-1 exploratory work, now documented with numbers.

  **Cross-channel correlation matrix (Spearman ρ + Pearson r)**:
  paradigm-shifting findings:
  - **H02b ≡ H02d at per-day primitive level (ρ = +1.000)** —
    identical values across all 1737 shared valid days. The
    discrimination difference (+29.9 vs +31.8 pp) is from
    window/validity differences, NOT from a distinct underlying
    signal. **H02d must drop as a separate channel.**
  - **HA10 ≡ −HA07c (ρ = −0.922)** — morning BB peak and sleep
    stress mean are nearly the same signal in opposite signs
    (structural in Garmin's BB algorithm). **NOT independent
    channels.**
  - HA06b ↔ HA07c = +0.377; HA06b ↔ HA10 = −0.393 (vagal-tone
    pathway).
  - HA07c ↔ HA07d = +0.501 (level and variability of the same
    sleep-stress signal).
  - H02b ↔ HA11 = +0.377 (within-day stress patterns share
    variance).

  **Effective N of independent signal clusters: 3-4 (not 7)**:
  Cluster 1 within-day stress (H02b/H02d + HA11); Cluster 2
  autonomic state (HA07c + HA10 ± HA06b); Cluster 3 autonomic
  variability (HA07d, partially tied to Cluster 2).

  **Honest effective-N Bonferroni** (α = 0.05/4 ≈ 0.0125): only
  H02d (p=0.011) clears it. With H02b/H02d collinearity counted as
  one, **only ONE distinct primitive survives honest effective-N
  statistical-significance correction**.

  **Synthesis implications**: the discrimination findings are real;
  the "many converging channels" framing was overstated. The
  load-bearing list tightens: H02b (with H02d folded in) remains
  the cleanest train signal; HA07d remains the only project-level
  overall-SUPPORTED + v2-validated finding but its statistical
  power is below conventional thresholds. The "seven SUPPORTED on
  six channels" headline must soften to "three-to-four
  effectively-independent signal clusters, of which one (within-day
  stress spike) clears α=0.05 in train". This is the most
  significant project-shape revision since the Theme A bundled
  re-test.

  Doc updates landed same session: STOCKTAKE §2a + headline,
  RESEARCH-REPORT-ADDENDUM §5.26, QUEUED-WORK.

## 5. Status legend

- **pending** — pre-registered, not yet tested.
- **running** — `test.py` written, results not yet written up.
- **supported** — pattern confirmed in train + validate per criterion.
- **refuted** — pattern absent or below criterion.
- **inconclusive** — underpowered or noise-dominated.
- **partial** — interesting in a different shape than pre-registered;
  needs reshape and re-pre-registration as a new hypothesis.

---

*Created 2026-06-05. Lock the `crash_v1` choice and the first-batch
list before any `H##/test.py` runs.*
