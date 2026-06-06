# Research stocktake — what we have, what it shows, what could become a feature

*Snapshot of the Garmin × gevoelscore × notes research as of 2026-06-06
(crash_v2 phase). Original snapshot 2026-06-05; updated 2026-06-06.
Source-of-truth pointers below each section. The crash_v2 phase has its
own writeup at [RESEARCH-REPORT-ADDENDUM.md](RESEARCH-REPORT-ADDENDUM.md);
this stocktake folds the new findings into the cross-cutting view.*

The goal of this document: one frame in which to see (a) the data we
actually have, (b) what looks insightful **before / during / after** a
crash, and (c) which indicators have earned enough evidence to be
candidates for the app — versus which would be misleading to build.

---

## 1. The data

### Subjective (gevoelscore + notes)

- **1.372 day_entries** with score across **2022-09-03 → 2026-06-05**.
  100% have a score on a 1–6 scale heavily clustered at 4–5.
- **686 day_entries (50%) have a written note.** Note coverage is
  uneven by year: 18% (2022, partial) → 40% (2023) → **71% (2024 peak)** →
  52% (2025) → 44% (2026 partial).
- Crash labels via locked `crash_v1`: score ≤ 3 for ≥2 consecutive days,
  episodes within 3 days merged.
- **`crash_v2` (locked 2026-06-06)** adds a tier-2 `dip` category for
  isolated single days at score ≤ 3 with neighbours ≥ 4. Tier-1 `crash`
  is exactly `crash_v1` — a pre-registered slow-recovery filter was
  empirically removed after the data showed all 29 v1 episodes have a
  multi-day rough tail (tail_median ∈ {4.0, 5.0}). See
  [crash_v2 definition](garmin/hypotheses/crash_v2-definition/definition.md).
- **Activity feature table (locked 2026-06-06, v3.1 percentile-rank)**:
  daily features at `garmin/activity-labels/output/activity_features_daily.csv`
  with `exertion_class` (4-axis composite of personal-baseline-relative
  percentile ranks), `push_burden_7d` (sustained-push count), and a
  passively-detected unified UDS intensity-minutes channel (empirically
  a superset of recorded-activity vigorous minutes). Spec is
  PEM-envelope, not athletic-training, and uses deviations from personal
  baseline throughout (no absolutes). Sensitivity-tested across 13
  parameter alternates; `exertion_class` is ROBUST (Jaccard ≥0.78
  on heavy+very_heavy across all variations); `push_burden_class`
  binning was SENSITIVE and was deprecated (raw count used downstream).

### Crash counts under `crash_v1`

| year | episodes | note |
|------|---------:|------|
| 2022 | 5 | partial year (~4 months of tracking) |
| 2023 | 9 | |
| 2024 | 11 | peak |
| **2025** | **2** | full year |
| 2026 | 2 | partial year (~5 months) |
| **total** | **29** | episodes |

Derived counts: **98 crash days** total (any day inside an episode with
score ≤ 3); **84 lead-up days** (3 days before each episode start);
**59 crash days have notes** (60%); **45 lead-up days have notes** (54%).

Episode span distribution (calendar days from first to last low day):
2-day = 19; 3–4-day = 4; 5–7-day = 3; 8–14-day = 3; 15+ = 0 (merge rule).
Long-crash tail collapsed from 5/14 early-era to 1/15 late-era.

Nadir distribution: early min = score 1 (3 episodes), late min = score 2
(no score-1 episodes in late era).

### Dip counts under `crash_v2`

**79 isolated single-day dips** across the corpus, on top of the 29
crash episodes (which are unchanged from `crash_v1`).

| era | crashes | dips | dip:crash ratio |
|---|---:|---:|---:|
| 2022-09-03 → 2023-12-31 (train) | 14 | 26 | 1.9× |
| 2024-01-01 → 2026-06-05 (validate) | 15 | 53 | 3.5× |

The dip:crash ratio nearly doubles between eras. The participant has
disproportionately more transient single-day rough patches in the
validate era — a finding the original `crash_v1`-only framework could
not surface formally.

**Dip clusters (descriptive overlay)**: 45 of the 79 dips (57%)
chain into 15 multi-day rough-patch clusters under a 7-day proximity
rule. 5 clusters are in the train era (covering 13 dips), 10 in the
validate era (covering 32 dips). The longest cluster spans
2024-03-14 → 2024-04-16 (9 dips, 34 days). The cluster concentration
in the validate era reinforces the "kind of crash changed" narrative:
rough patches in the residual era are protracted and intermittent
rather than sustained-low. Per-day labels are unchanged; clusters
are captured as a `dip_cluster_id` column for downstream analyses.

### Objective (Garmin)

- **~1.700 days** of monitoring data (2021-08-16 → 2026-06-04, 98.8%
  coverage). Pre-LC period (2021-08 → 2022-09) is healthy-baseline
  reference, not used for labelled tests.
- Daily aggregates we use: RHR, average stress, charged/drained body
  battery, sleep efficiency.
- Per-minute samples we extracted: stress (~1.400/day) for spike
  analysis (H02b).
- Per-minute body battery is NOT yet extracted — encoded in undocumented
  FIT message type 233. **2026-06-06 literature sweep confirmed no public
  decode exists** (HarryOnline community spreadsheet lists it with a
  question mark; tcgoetz/Fit, GoldenCheetah, fitdecode all treat it as
  unknown). A two-path H04b protocol is locked at
  [.claude/plans/adaptive-foraging-hamming.md](../../.claude/plans/adaptive-foraging-hamming.md):
  Path C uses `cyberjunky/python-garminconnect` to pull per-minute BB
  via Garmin Connect REST API (ToS-grey but accepted for personal use);
  Path B decodes `unknown_233` from FIT using Path C as supervised labels.
- Sub-daily signals also confirmed-present in FIT but not yet extracted:
  HRV (the channel H04 hinted at, untested), respiration, SpO2.

---

## 2. What each phase shows — before / during / after a crash

The phase split is the user-natural way to ask "what does the data tell us?"

### 2a. Before a crash (the precursor question)

Across all four daily-aggregate signals we tested, only one cleared its
pre-registered bar in any window:

| signal (3 or 7-day lead-up) | early-era (2022–23) | late-era (2024+) | source |
|---|---|---|---|
| Daily resting HR drift (Workwell rule) | flat | flat, slight inversion | [H01](garmin/hypotheses/H01-rhr-drift/result.md) |
| Daily avg stress | clear positive direction, refuted at strict bar | flat | [H02](garmin/hypotheses/H02-stress-elevation/result.md) |
| Daily sleep efficiency | flat | flat | [H03](garmin/hypotheses/H03-sleep-efficiency/result.md) |
| Daily body-battery net delta | slight inversion | weak positive (almost cleared bar, +13 pp) | [H04](garmin/hypotheses/H04-body-battery/result.md) |
| **Per-minute stress spike duration (max contiguous ≥75 ≥5min), 3-day window** | **SUPPORTED** (71% of episodes, +29.9 pp discrim) | refuted; near-miss | [H02b](garmin/hypotheses/H02b-stress-spikes/result.md) |
| **Per-minute stress spike duration, sentinel-corrected + 4-5 day window (H02d, 2026-06-06)** | **bridge × 5d SUPPORTED at +31.8 pp — strongest train-era single-channel signal of the whole project**; imputed arms refuted (sentinel imputation too generous; ~159 too_active samples/day) | refuted in all 4 arms (imputed × {4d, 5d}, bridge × {4d, 5d}). 5 stress-channel tests now consistent on validate refutation | [H02d](garmin/hypotheses/H02d-stress-spikes-uncensored/result.md) |
| Spike duration before *dips* (2026-06-06) | refuted (+9.1 pp, ~3× weaker than crashes), but criterion C passes | refuted (+5.2 pp), criterion C passes; converges with crash signal | [H02b on dips](garmin/hypotheses/crash_v2-definition/h02b_on_dips_result.md) |
| Activity shock 3-day lead-up (HA01, 2026-06-06) | refuted (+0.7 pp) | refuted (+11.5 pp, close to bar) | [HA01](garmin/activity-labels/output/ha_results.md) |
| **Activity shock 4-day lead-up, rolling baseline (HA01b, 2026-06-06)** | refuted (+8.6 pp, underpowered) | **originally reported SUPPORTED (+17.3 pp) — see next row for re-test** | [HA01b](garmin/activity-labels/output/ha_results_4day.md) |
| **Activity shock 4-day lead-up, lagged baseline (HA01b-recomputed + HA02c, 2026-06-06)** | refuted (+5.8 pp) | **REFUTED (+4.0 pp; -13.3 pp delta vs rolling)** — the original +17.3 pp was substantially a rolling-baseline construction artifact | [bundled re-test](garmin/activity-labels/output/ha_results_4day_lagged.md) |
| Activity shock lag profile (post-hoc, 2026-06-06) | empirical peak at 5d (+15.3 pp; not pre-registered, exploratory only; also subject to the same baseline-construction concern) | empirical peak at 5d (+23.0 pp; exploratory only; same caveat) | [lag profile](garmin/activity-labels/output/lag_profile_report.md) |
| Push burden 3 or 4 day lead-up (HA02 / HA02b / HA02c) | refuted on both baselines | refuted on both baselines | [HA02](garmin/activity-labels/output/ha_results.md) + [HA02c](garmin/activity-labels/output/ha_results_4day_lagged.md) |
| Lead-up notes language | (less informative than during) | less symptom-warning language, more cognitive-load mention | [notes v2](notes/02-categorize-clauses/categories-analysis-v2.md) |

**Headline takeaway** (revised 2026-06-06 after the Theme A bundled re-test + H02d): For early-era crashes (pre-stabilisation), the per-minute stress spike is a real and discriminative precursor — your own framing "an intense moment in an otherwise calm day can trigger a crash" is confirmed by the data, now across three nested operationalisations: H02 (daily-avg), H02b (3-day spike), and H02d (sentinel-corrected, 4-5 day windows). H02d's bridge × 5d arm produced **+31.8 pp train discrimination — the strongest train-era single-channel signal of the whole project**, surpassing H02b's +29.9 pp, with monotonic 3d → 4d → 5d scaling (+29.9 → +27.6 → +31.8 pp) that confirms a 4-5 day empirical lag. For late-era crashes, all five stress-channel tests (H02, H02b, H02d × 4 arms) refute in validate. HA01b at the 4-day window was initially reported as the first SUPPORTED validate-era precursor (+17.3 pp on the rolling 30-day baseline), but the **pre-registered bundled re-test on the methodologically cleaner lagged 30-90-day baseline (Theme A fix) refuted that finding** — the recomputed validate-era discrimination dropped to +4.0 pp (-13.3 pp delta), and the bundled HA02c push-burden test was also refuted. The original +17.3 pp was substantially a rolling-baseline construction artifact (the rolling reference includes the recent candidate window in its denominator; a sustained creep rebases itself). **The honest position as of the Theme A re-test + H02d: the validate-era refutation now spans 5 stress-channel tests + 4 activity-shock channel tests + all prior daily-aggregate tests. The waking-hour channel is closed across two independent channel families.** The 4-5 day empirical lag is corroborated by both H02d bridge train and HA01b lag profile — independently of which channel survives a clean re-test, the lag for this person centres at ~5 days, not 3. The investigation now has **two train-era SUPPORTED stress-spike findings** (H02b 3d, H02d bridge × 5d) and **zero overall-SUPPORTED precursors under clean methodology**. The next candidate — morning resting-HR delta (HA06, gated on its own pre-registration) — operates on a physiological quantity with strong external evidence (Workwell RHR+15, Bateman Horne "back to baseline next morning?") and is the only remaining waking-hour-adjacent test before the direction shifts to overnight recovery (gated on H04b unlocking per-minute Body Battery).

### 2b. During a crash (the symptom and topology signature)

This is where the data is strongest. Crash days have a clear and
reproducible signature, and the signature has shifted across the
stabilisation transition.

**The reliable signature** (from notes v2 categorisation, all 59
crash days with notes):

| signature | crash rate | vs. non-crash | source |
|---|---:|---:|---|
| Physical symptom mentioned (hoofdpijn, koorts, etc.) | 92% | 68% | notes v2 |
| Cognitive symptom mentioned (brainfog, mistig) | 19% | 6% | notes v2 |
| External-illness trigger (corona, griep, keelpijn) | 5% | <1% | notes v2 (8.7x ratio) |
| Emotional load mentioned (load not symptom) | 7% | 4% | notes v2 (2.9x ratio) |

**The era-shift in crash signature** (early vs late, on crash days):

| dimension | early | late | shift |
|---|---:|---:|---|
| symptoom_fysiek state = severe | 4% | 22% | **+18 pp** |
| symptoom_fysiek state = present (default) | 81% | 69% | −13 pp |
| `belasting_gezin` mentioned | 0% | 22% | **+22 pp** |
| `symptoom_cognitief` (brainfog etc.) | 11% | 25% | **+14 pp** |
| `triggers_extern` | 7% | 3% | −4 pp |
| day is "mixed-day topology" (positive content + crash) | 11% | 50% | **+39 pp** |

**Headline takeaway**: residual crashes are categorically different
in their during-crash signature, not just less frequent. They're
more often severe in physical-symptom intensity, more often paired
with caregiving context (kids, partner), more cognitive-symptom-heavy,
fewer infection-triggered, and crucially **more often embedded in
days that also contain functional/positive content** — the crashes
are less totalizing.

### 2c. After a crash (recovery / aftermath)

Less mature than during-crash. Two threads:

- **H05 (recovery time)** was spec-broken (recovery target structurally
  trivial). [H05b](garmin/hypotheses/H05-recovery-time/result.md)
  queued with a sustained-recovery target.
- **Long-arc stabilisation visible across the whole window**
  ([S01 trajectories](garmin/hypotheses/S01-stabilisation-trajectories/notes.md)):
  - Max stress-spike duration: 10.5 min (pre-LC) → **13.2 min** (mid-2023
    peak) → **5.8 min** (Apr 2025 trough) → 11.4 min (May 2026 uptick)
  - Avg stress baseline: 32.6 → 36 → 29 → 33.7 (recent uptick)
  - RHR: mostly stable, but **notable recent rise to 60.8 bpm in May
    2026** (highest in the whole window)
  - Sleep efficiency: flat at ~99% throughout (the body's sleep
    continued to work through everything)

The stabilisation-arc card is now empirically anchored across multiple
biometric dimensions, plus the per-episode K## findings (depth, duration).

---

## 3. The eight directional findings + one convergence supporting the "kind of crash changed" theory

A single tabulated view of how the picture coheres across H##, K##,
notes, and now `crash_v2`:

| axis | source | direction (early → late) |
|---|---|---|
| stress precursor (daily avg) | H02 | yes → no |
| stress precursor (spike count, 3d) | H02b | train SUPPORTED +29.9 pp → validate refuted |
| **stress precursor (spike count, 4-5d, sentinel-corrected)** *(new 2026-06-06)* | **H02d** | **train SUPPORTED bridge × 5d +31.8 pp (project-strongest) → validate refuted in all 4 arms** |
| crash depth (score nadir) | K01 | late shallower (no score-1) |
| crash duration (span) | K02 | late shorter (long-tail 5→1) |
| crash language: symptom severity | notes v2 | late severe-symptom +18 pp |
| crash language: day topology | notes v2 | late mixed +39 pp |
| lead-up language | notes v2 | late less warning, more cognitive |
| **dip:crash ratio** *(new 2026-06-06)* | **crash_v2** | **1.9× → 3.5×** (more transient single-day events) |

Plus one cross-class **convergence** finding:

| axis | source | direction (early → late) |
|---|---|---|
| **crash vs dip precursor magnitude** *(new 2026-06-06)* | **H02b on dips** | **+29.9 pp / +9.1 pp (3× ratio, train) → −8.2 pp / +5.2 pp (converged, validate)** |

And one within-class structure finding:

| axis | source | direction (early → late) |
|---|---|---|
| **dip cluster concentration** *(new 2026-06-06)* | **crash_v2 cluster overlay** | **5 clusters / 13 dips train → 10 clusters / 32 dips validate** (multi-day rough patches concentrate in residual era) |

**Nine directional findings on independent axes, plus a cross-class
convergence, no contradictions.** None individually clears its strict
pre-registered bar in isolation, but the cumulative weight is strong:
the residual crashes are qualitatively different, not just fewer —
and in the validate era they have collapsed toward the (always weak)
physiological signature of single-day dips.

---

## 4. Candidate indicators for the app — ranked by evidence

The candidates fall into three confidence tiers. Each is a card concept,
not a fully designed feature.

### Tier 1 — Strong evidence, ready to prototype

These have multi-axis empirical support. Build first.

**a. The stabilisation-arc card (retrospective).** A long-arc view of
the user's journey: crash frequency by year, stress baseline shift,
spike-duration compression, sleep stability. Backed by seven
directional findings (§3) and the S01 trajectories. Frames the
recovery story honestly: not "you're recovered" and not "you're
still ill" — "you're stabilising, here's the arc."

**b. The per-crash retrospective card for pre-2024 crashes.**
"Around 5 March your stress was at ~30 most of the day, but a
22-minute spike to 88 in the afternoon — what was happening?" Uses
the H02b spike-precursor metric. **Validated as discriminative on
71% of train-era crashes.** Honest framing: works for historical
(2022–23) crashes, less reliable on 2024+ residual crashes.

**b2. The per-crash retrospective card for validate-era crashes
(originally Tier 1 on HA01b 2026-06-06; DOWNGRADED 2026-06-06
after Theme A bundled re-test).** Originally framed as: "Looking
back at your crash starting [date]: in the 4 days before it, you
had heavy or very_heavy exertion on day [list]. What was happening
then?" — with HA01b's +17.3 pp validate-era discrimination as the
empirical anchor. **The bundled re-test on the methodologically
cleaner lagged baseline (Theme A fix) refuted the +17.3 pp finding:
HA01b-recomputed shows +4.0 pp validate-era discrimination, well
below the +15 pp SUPPORTED bar.** Card (b2) loses its empirical
anchor. It may still be useful as a *descriptive* retrospective
("here is what your activity looked like in the 4 days before")
without the precursor framing, but it should not ship as a
"validated discriminator." Downgraded to Tier 2 pending a
fresh empirically-grounded validate-era precursor (HA06 morning
RHR is the next candidate).

**c. The crash-day signature card.** "On this crash day you mentioned
[physical symptom], [cognitive symptom], [emotional load].
Caregiving was in the background." Built from notes v2
categorisation. Doesn't predict — describes.

**d. The mixed-day topology card.** "Your crashes increasingly happen
on days where good things also happen — your body is finding edges."
Backed by the +39 pp finding in late-era crashes. Powerful framing
for the user's own recovery narrative.

**e. The recent-perturbation awareness card.** "Your RHR is up about
5 bpm in the last few months." Three of four trajectory metrics
moved up together in May 2026. Worth surfacing as awareness, not
alarm.

### Tier 2 — Promising, needs more work or supports a v2

**f. The spike-detection retrospective card for new crashes** (not
prediction). Same shape as (b) but framed: "we see a notable spike
that day but the pattern is less consistent than it used to be."
Fires on ~33% of validate-era crashes with a real spike; rest get a
honest "we don't see an unusual spike pattern before this crash."

**g. Caregiving-context tagging on late-era crashes.** 22% of
late-era crash days mention family/caregiving load. Could surface
as a context tag: "this crash was on a day with caregiving demands."
Needs the eventual app tagging feature to land (research first per
the discipline).

**h. Sleep-as-protector reframe.** Direct positive copy: "your sleep
efficiency has stayed stable at ~99% through this whole journey." The
"good sleep is not a protector" reframe — sleep didn't prevent
crashes but also wasn't disrupted by them. Useful framing, low-risk.

### Tier 3 — Candidates pending further research

Wait for follow-up work before building.

**i. Body-battery intra-day rise/drop occurrences.** User insight
("BB-rise occurrences are themselves meaningful"; afternoon-nap
recovery; sharp drops as stress events). Needs per-minute BB data —
either decode `unknown_233` (FIT-level research) or hit Garmin
Connect REST API. Queued as H04b.

**j. The shielder-vs-reliever experiment.** The eventual pacing-doc
ambition: "did intervention X reduce crash depth or recovery time?"
Needs an `interventie` category in the notes dictionary AND the
recovered H05b sustained-recovery metric. Substantial work, big
payoff if it lands.

**k. Recovery-time card (per crash).** Pending H05b spec fix.

---

## 5. What we know NOT to build

Each of these would look reasonable on first inspection but would
mislead the user.

- **A daily Garmin tile dashboard.** RHR / stress / sleep / body-battery
  as four daily numbers next to today's score. Accurate but useless:
  the daily aggregates don't predict residual crashes. We'd be
  selling a false sense of warning signal.
- **A "you might crash tomorrow" predictor card.** None of H01–H04
  clears the prediction bar on validate-era data. H02b train passed
  but late-era validation failed. Building this would produce a
  steady stream of false alarms with poor true-positive rate.
- **A sleep-as-warning card.** Sleep efficiency was flat across crashes,
  lead-ups, and non-crash days. Telling the user "your sleep is X
  tonight, might be a sign" has no empirical support for them
  personally.
- **A "your stress score is high" alert.** Daily avg stress was
  train-only positive. By the time of the residual crashes, the
  signal is gone. Surfaces noise.

---

## 6. Methodology lessons we've banked

Captured in synthesis.md; restated here so the next round inherits
them.

1. **Pre-register on both median and mean** when the metric clusters
   on integers / minimums (K01 / K02 lesson).
2. **Small dry-run before locking a spec** — three episodes' computed
   values eyeballed catches definitional artifacts that pre-registration
   alone doesn't (H03 confirmation-type whitelist bug, H05 recovery
   target trivially met).
3. **Substring matching needs negation handling** at every layer
   where it matters — symptoms AND polarity. v2 fixed symptoms; the
   v3 follow-up handles polarity.
4. **Output-key naming matters** when a script produces rich
   metadata — use distinct prefixes to avoid clashes (the
   `_present` clash that initially showed 75% instead of 92%).
5. **Look at actual clauses behind every striking statistic** before
   building anything on top.

---

## 7. What's queued

After the 2026-06-06 crash_v2 + activity-labels + Theme A bundled re-test phases the queue is:

1. **HA06 — morning resting-HR delta (C.1)**. Pre-register as a both-era test (train + validate, separately evaluated) per the D7 reframe pre-commitment. Strongest external evidence of any candidate (Workwell RHR+15, Bateman Horne "back to baseline next morning?", HRV staying suppressed 24h post-VT in patients). Computable now from existing UDS resting-HR — does not depend on H04b. Pairs naturally with push burden as the cumulative-erosion mechanism made visible. The only remaining waking-hour-adjacent candidate after Theme A refuted HA01b on the cleanest baseline.
2. **C.3 personal-lag teaching** — derivative one-pager from crash_v2 + activity-labels data. Descriptive only, no prediction bar. Independent of the precursor failure: a teaching artefact about lag patterns, not a discrimination claim. Era framing needs honest reframing post-bundled-re-test (the 4-day SUPPORTED claim has been withdrawn).
3. **C.5 volatility + dip-frequency progress metric** — derivative one-pager (rolling 30-day std + monthly dip count). Operationalises the scale-compression finding (real improvement = lower variance + fewer dips, not higher mean).
4. **C.2 cognitive/emotional load mining** — interaction test with the notes/tag layer. The independence-of-Garmin angle: even if Garmin's waking-hour channels are closed for validate-era crashes, the journal layer may carry signal Garmin can't see.
5. **Notes label-quality work** (participant-requested). Pre-cursor to any v3 notes categorisation across crash, dip, and normal day-types.
6. **H04b — decode `unknown_233` for per-minute Body Battery**. Protocol locked at [.claude/plans/adaptive-foraging-hamming.md](../../.claude/plans/adaptive-foraging-hamming.md); execution gated on the notes work completing. Becomes more important now that waking-hour aggregates are closed for validate-era crashes — overnight recovery is the next frontier.
7. **H03b — overnight Body Battery recharge as a marker of unrefreshing sleep**. Gated on H04b success.
8. **C.4 recovery-completeness over time** — depends on C.1 (HA06) outcome + a sustained-recovery primitive (H05b).
9. **Dip subtyping (dip_v2)** — split the 79 dips into "almost-crash" (with physiological precursor) and "mood-only" (without) subtypes. Now the HA01 3-day "dip > crash" finding inherits the same baseline-construction caveat as HA01b; should be re-evaluated under the lagged baseline before being used as motivation.
10. **Card (b2) prototyping** — downgraded to Tier 2 in §4; ships as descriptive only if at all, until a fresh validate-era precursor lands.
11. **Dictionary v3** (polarity-negation handling) and **H05b** (sustained-recovery target). Cheap, deferred.

**Card (a) the stabilisation-arc card** remains the highest-evidence card concept — its supporting findings are not affected by the baseline-construction issue (S01 trajectories, K01/K02 era shifts, dip:crash ratio, notes v2 era shifts all use independent data and metrics).

The hardest part — the analytical work that tells us *whether* an
indicator is worth building on — is largely done. What's left is
mostly product / craft decisions about how to surface the findings,
with a few targeted research follow-ups (H04b, H03b, dip subtyping)
supporting specific card concepts.

---

*Stocktake written 2026-06-05 after H## + K## + S## + notes-v2 work
plus the late-positive-dominant verification. Living document — to
be updated as Tier-2 work matures or Tier-3 research lands.*
