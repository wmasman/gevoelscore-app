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
at [synthesis.md](synthesis.md). It reads each refuted hypothesis
productively (what the data does and does not say), lists
caveats applying across the batch, and prioritises follow-ups. Living
document, last updated 2026-06-06 with the crash_v2 phase.

## 4b. Closed since 2026-06-05 (post-synthesis-v1)

- **H02b-trajectory** ([H02b-stress-spikes/trajectory-notes.md](H02b-stress-spikes/trajectory-notes.md))
  — rolling 12-month discrimination curve replacing the binary
  H02b verdict; smooth ~12-month decay from +31.8 pp peak
  (mid-2023) to near zero by mid-2024.
- **S01 stabilisation trajectories** ([S01-stabilisation-trajectories/notes.md](S01-stabilisation-trajectories/notes.md))
  — 90-day rolling means of 4 metrics across the full Garmin
  window; cleanest pendulum signal in max stress-spike duration.
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
  [synthesis.md](synthesis.md) "Update 2026-06-06 (later still)".

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
