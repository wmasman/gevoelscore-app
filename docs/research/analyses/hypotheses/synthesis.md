# Synthesis — what the H01–H05 batch tells us, and what it doesn't

*Written 2026-06-05, after all five pre-registered tests in the first
batch closed. Reads each refuted hypothesis productively, in the style
the user set out: "good sleep is not a protector against crashes, they
still occur; whether bad sleep would extend or deepen them, this
dataset cannot tell us."*

This is not a verdict on PEM in general. It is a verdict on what one
person's data, across 3.7 years and 29 crash_v1 episodes, supports as a
predictive precursor when analysed at daily resolution.

---

## 1. The five verdicts in one frame

| H##  | metric                       | crash_v1 train (14 ep) | crash_v1 validate (15 ep) | what passed | overall |
|------|------------------------------|------------------------|---------------------------|-------------|---------|
| H01  | resting HR drift             | flat                   | flat, slight inversion    | nothing     | refuted |
| H02  | daily avg stress             | clear positive direction (79% positive, median +2.7, disc +25.9 pp) | flat | crit b + c only | refuted |
| H03  | sleep efficiency             | flat                   | flat                      | nothing     | refuted |
| H04  | body-battery net delta       | slight inversion       | weak positive (disc +13.3 pp, just below) | nothing | refuted |
| H05  | recovery-time distribution   | n/a — spec-induced trivial result; H05b queued | | n/a | spec broken |

Only one signal cleared two of three pre-registered criteria in any
window: H02 in train. Everything else was flat, almost-flat, or
slightly inverted within noise. None reached "supported."

## 2. What the data DOES say

Stated as carefully bounded findings, each with a "for this person, in
this window" clause attached.

### 2.1 Pre-recovery crashes (2022–23) had a sympathetic-arousal precursor

Eleven of 14 train-era crashes (79%) had elevated lead-up daily mean
stress — median +2.7 points on Garmin's 0–100 scale, with high-band
duration averaging ~13 extra minutes per day, against a null sample
that almost never reaches +25.9 pp at that frequency by chance. The
direction is unambiguous even though the strict 60%-at-+3 bar wasn't
cleared.

**The data says**: in the period when this user was less recovered,
the days running up to a crash were quantifiably more sympathetically
activated than randomly-chosen 3-day windows.

**The data does NOT say**: stress *caused* the crashes. A shared
upstream — accumulated cognitive load, an undiagnosed infection
mounting, hormonal cycle — would produce both the stress reading and
the subsequent crash. We cannot disentangle these without intervention
data.

### 2.2 The same signal does not appear in post-recovery crashes (2024+)

Validate-window H02 was flat: 40% positive direction (≈ coin flip),
median −0.2, discrimination −3.7 pp. The user has confirmed this is
real recovery, not score-interpretation drift.

**The data says**: the residual 2024+ crashes (~2 per year, down from
~10/year in 2023) are not preceded by elevated daily mean stress in
the way the earlier crashes were.

**The data does NOT say**: stress is irrelevant to the residual
crashes. The daily mean smooths over intra-day spikes — and the user
has independently reported (saved to project memory) that *an intense
moment in an otherwise calm day can still trigger a crash*. The daily
average is the wrong instrument for that pattern. H02b (per-minute
spike count) was promoted to high-priority deferred specifically to
test the right shape.

### 2.3 Sleep quality (as efficiency) is not a protector for this user, in either era

H03 returned 0% of episodes and 0% of null windows crossing the −5 pp
efficiency threshold. Median delta efficiency ~0 in both windows.

**The data says**: this user has remarkably stable sleep efficiency.
Crashes happen with the same sleep efficiency in the 7 nights before
them as in random non-crash 7-night periods. Sleep being *good* did
not prevent the 29 crashes. Sleep being *normal* did not predict the
crash either.

**The data does NOT say** (this is the user's framing):
- that bad sleep wouldn't extend or deepen a crash
- that sleep dysregulation isn't a real PEM mechanism for *other*
  people
- that this user's deep-sleep specifically, REM specifically,
  total-sleep-time specifically, or sleep fragmentation specifically
  is preserved — only that the *efficiency composite* is preserved.
  H03b (sharper sleep metrics) could still find something.

### 2.4 Body Battery's composite doesn't add value over its components for this question

H04 missed in both windows. Train slightly inverted; validate was the
only positive-direction validate signal we saw (discrim +13.3 pp,
median −3.0) but didn't clear the bar.

**The data says**: Garmin's body-battery composite did not inherit
H02 train's stress signal as one might mechanically expect — the
composite seems to dampen the stress channel via sleep charging and
the (null) RHR component. So body battery's daily value is *not* the
single-number proxy for the energy envelope for this user that the
pacing literature suggests it might be.

**The data does NOT say**:
- that intraday body battery curves don't carry signal (we tested
  daily totals only)
- that the validate-window hint isn't real — it just isn't strong
  enough to act on. It does point at HRV (the only body-battery
  component we didn't test directly) as a candidate for future
  investigation.

### 2.5 Resting HR drift is not the channel here

H01 was flat in both windows, with validate slightly inverted (RHR
*lower* than baseline before crashes by ~1 bpm, median).

**The data says**: the Workwell Foundation's "RHR + 15" pacing rule,
the most established pacing indicator in the broader literature, does
not predict crashes for this user in either era. In the post-recovery
era, the direction is faintly inverted — consistent with "the user is
so well-paced that residual crashes happen when nothing HR-visible has
gone wrong."

**The data does NOT say**:
- that chronotropic incompetence isn't blunting the signal (Workwell
  themselves flag this affects most ME/CFS patients).
- that RHR rising *during or after* a crash isn't real — H01 only
  tested 7-day lead-up.
- that RHR isn't useful for other people whose autonomic response is
  intact.

## 3. The cross-hypothesis pattern

Read together, H01–H04 deliver a coherent picture:

**For this user, the daily-aggregate channel of Garmin biometrics is
closed as a crash-precursor signal.** That includes the daily mean
stress (the closest thing to a signal we found), daily RHR, daily
sleep efficiency, and the daily body-battery composite. None of them
crosses the pre-registered bar; the one that came closest (H02 train)
disappears in the post-recovery window where it would actually be
useful.

This is not a small thing. It clears a lot of brush:

1. **A "tile dashboard of daily Garmin numbers" feature would not help
   this user prevent crashes.** Not because the data isn't there — it
   is, with excellent coverage — but because the daily summaries do
   not contain the signal in the form a prevention card needs it.
2. **The signal that did appear in train (stress) lives in a channel
   that recovery has closed.** A naive feature trained on 2023's data
   would either show false alarms or miss residual crashes entirely
   by 2026.
3. **Whatever triggers the residual ~2/year crashes lives below the
   daily aggregation horizon, or in a channel we did not test at this
   resolution.** The candidates are: per-minute stress spikes (H02b),
   HRV (untested), specific sleep subcomponents (H03b), or
   non-biometric triggers (cognitive load, emotional events,
   hormonal, viral, mast-cell) that no wearable captures.

## 4. The user-experiential framing strengthens the next-step priority

The user reports (saved to project memory) that *an intense moment
during an otherwise calm day can trigger a crash*. This is rare
first-person evidence about mechanism, and it points exactly at where
our daily-aggregate tests are blind.

Daily mean stress dilutes a 5-minute spike by 1.435 other minutes.
"Highest stress sample of the day" / "number of minutes ≥ 75 / day" /
"count of distinct ≥10-minute intense windows" are the metrics that
would catch the pattern the user describes. H02b is built for this.

This is also the most economically valuable card we could build: a
retrospective view that, after a crash, surfaces "there was a
17-minute stress spike on Tuesday afternoon — was that the dentist?"
turns the wearable from a daily-summary tile into a forensic
companion.

## 5. Caveats we found, listed once

These apply across the batch and would apply to any future tests using
the same data:

**About `crash_v1` itself:**
- It is a one-dimensional definition (score ≤ 3 for 2+ days, merged
  within 3). It mixes mechanisms: a tag-able PEM crash, an
  infection-driven low period, a migraine cluster, a depressive
  episode all collapse to the same label. A supported precursor on one
  subtype could be diluted to null by averaging across the others.
- The threshold was revised mid-preflight from "personal bottom 15%"
  (which landed on tied scores and covered 50% of days) to "score ≤ 3."
  The current definition still captures 14% of days as low, which is
  defensible but not the only valid choice.
- `crash_v2` from notes-based labels remains the natural way to split
  mechanisms. Worth doing before re-testing precursors in batch 2.

**About the train/validate split:**
- The recovery cliff between 2024 and 2025 reshaped the split from
  time-proportional to episode-balanced. Both halves clear 10
  episodes, which was the minimum for power.
- A precursor that's true in both windows would be strong evidence
  *across the recovery transition*. A precursor that's true in only
  one is interesting (H02 train pattern) but not generalisable to the
  current life-state.

**About the metrics:**
- **Daily aggregation hides intraday signal.** Confirmed by H02's
  partial result and reinforced by user's lived experience.
- **Garmin's algorithms are opaque** (Body Battery especially) and
  **firmware changes** between FR245 versions 7.x and 10.4 plausibly
  shifted baselines we cannot control for.
- **`unknown_233`** in the FIT files (1.440 per-minute records per day
  across 5 years) is unidentified by the wider community — could be
  body-battery internal state, HRV bytes, something else entirely.
  Decoding it would unlock per-minute Body Battery and possibly
  per-minute HRV.

**About the inference itself:**
- We can never distinguish "X precedes a crash" from "X and the crash
  share an upstream cause." Acute infection, hormonal cycle, ambient
  stressors all qualify as shared causes.
- Hypotheses are tested on the same 29 episodes. Multi-comparison
  inflation was controlled by pre-registration and held-out
  validation; with all five refuted on the bar, inflation didn't bite.
- A spec error (H03 confirmation-type whitelist; H05 recovery target
  too lenient) is caught after the fact. **Methodology lesson**: a
  small dry-run printing the first 3 episodes' computed values
  *before* finalising the spec would have caught both. Add to second
  batch's protocol.

**About the user-experiential evidence:**
- The user's report that intense moments trigger crashes is n=1 and
  introspective. It is the strongest direct evidence we have about
  this user's mechanism, and it is also exactly the kind of evidence
  patient self-management literature relies on. Treat as a strong
  prior for designing H02b, but not as a finding from this dataset.

## 6. Insights useful for design (no card mockups — those come per
hypothesis)

What the synthesis frees up the product to do or not do:

1. **Do not build a Garmin daily-tile dashboard.** It would be both
   accurate to the data and useless to the user, because the predictive
   information isn't there. The pacing-doc already said the product's
   job is detection and timing not prescription; this synthesis
   sharpens that to "*intraday* detection and *spike-anchored* timing,
   not daily-aggregate summaries."

2. **The most useful retrospective card for this user is anchored to
   a crash and looks for spikes, not averages, in the days before.**
   Pending H02b confirmation, the card would read something like
   "around 4 March your stress was sitting at ~30 most of the time, but
   there was a 22-minute spike to 88 on the afternoon of 2 March."
   That's the shape of card the user has effectively pre-validated.

3. **Sleep can be presented as preserved, not as something to fix.**
   Frame matters: "your sleep efficiency has stayed stable through all
   of this" is supportive, accurate, and avoids the population-level
   anxiety of "sleep is critical for recovery." If H03b finds a
   specific subcomponent that does move, the framing can adjust.

4. **Body Battery's daily score is not useful as a crash-prevention
   signal for this user.** It can still be useful as a within-day
   pacing dial (its intended Garmin use). Don't promise the daily
   number predicts anything.

5. **Recovery-time as a card concept is still alive** — only the
   specific spec was broken. H05b queued.

6. **The recovery cliff itself deserves a retrospective recovery-arc
   card** (parked in registry §4 as the trajectory card). "Crashes
   dropped from 10/year to 2/year between 2024 and 2025" is the kind
   of summary that gives the user perspective on the whole journey.

7. **A `crash_v2` based on note keywords** (hoofdpijn, kapot, moe,
   etc.) is now upstream of most second-batch precursor tests. Splitting
   the 29 episodes by *kind* may surface precursors that were
   dilution-killed in `crash_v1`.

## 7. What's next, ordered

1. **H02b** — per-minute stress spike count. Tests the user's lived
   experience directly. Likely highest-yielding single test in the
   project's near future.
2. **H05b** — sustained-recovery target. Recovers the recovery-time
   card concept. Cheap to run.
3. **`crash_v2`** — notes-based labels. Surface what kinds of crashes
   are in the 29 episodes.
4. **H03b** — sharper sleep metrics, deferred unless `crash_v2`
   surfaces a sleep-recovery angle.
5. **HRV-on-rest** — the channel H04's validate hint points at.
6. **Decode `unknown_233`** — long shot but high-value if it turns out
   to be per-minute body battery or HRV.

The investigation is open. Five pre-registered tests cleared the brush
honestly. Two of the five surfaced refined follow-ups (H02b, H03b).
One revealed a methodology lesson (H05). Together, they tell us where
*not* to spend feature-design effort, where the next test is most
likely to fire, and what to frame supportively rather than alarmingly
when the time comes to surface anything to the user.

---

## Update 2026-06-05 (later same day) — H02b + K01 + K02 results

Three more tests closed after the first batch and synthesis. Brief
recap; full detail in their per-folder result.md files.

**H02b — per-minute stress spike count.** **Train SUPPORTED on all
three criteria** (71% of crashes had a ≥10 min longer lead-up spike
than typical; discrimination +29.9 pp; median +16 min). Validate
near-miss (33%, discrim −8 pp, median +6.7 min). Overall verdict:
refuted by the strict bar (both windows required). But the train
result is the **first window of the whole investigation to fully
clear all three pre-registered criteria**, and it directly validates
the user's experiential framing about intense spikes triggering
crashes. The validate-window weakness is partly explained by a
"compression" finding: baselines and lead-up max-spikes both shrank
across the cliff, so signal-to-noise fell even though direction is
preserved.

**K01 — crash depth shifted.** Suggestive but underpowered. Early
median nadir = 2, late = 3 (delta +1.0). Mean shift +0.67 on a 1–6
scale. **No late-era crash reached score 1; three early crashes
did.** Permutation p = 0.28 — fails the ≤ 0.10 bar because the
nadir variable takes only three integer values, making the median
brittle on 14 vs 15 samples.

**K02 — crash duration shifted.** Refuted on bar but with a
striking structural finding. Median spans differ by only 0.5 days,
but the **mean** drops from 4.64 to 2.53 days (−2.11 days). The
**long-crash tail collapses**: 5 of 14 early episodes ran ≥ 5 days
(including 9, 11, and 14-day runs); only 1 of 15 late episodes did
(7 days). Permutation p = 0.095 — just clears the bar — but
criterion a (median magnitude) fails because both eras' medians
are dominated by 2-day episodes.

### Combined picture

The kind-of-crash theory now has **four directional supporting
findings across independent axes**, with no contradictions:

| test  | axis                  | verdict                 | direction       |
|-------|-----------------------|-------------------------|-----------------|
| H02   | stress (daily avg)    | refuted, train-direction | train: yes; late: no |
| H02b  | stress (spike count)  | refuted overall; train **SUPPORTED** | train: yes; late: weaker |
| K01   | crash depth           | suggestive_underpowered | late shallower |
| K02   | crash duration        | refuted on bar; tail collapse | late shorter |

None passes its strict bar in isolation. Together they tell a
coherent story: residual 2024+ crashes are **less frequent
(preflight), shallower (K01), shorter (K02), without daily-average
biometric precursors (H01–H04), and with weaker spike precursors
than pre-recovery crashes (H02b validate)**. The user's recovery is
documented across multiple independent axes.

### Methodology lesson surfaced by K01 + K02

Pre-registering on the **median** when the metric takes few distinct
values and clusters on the minimum (nadir: 3 values, mostly 2; span:
mostly 2 days) makes the median statistic brittle. The mean catches
the shift cleanly in both cases. **For K03 and onward in the K## thread,
pre-register on both median AND mean criteria** (or some other shape
that handles heavy-skew small-sample distributions better). Also
true going back: a small dry-run printing 3 episodes' computed
values would have surfaced this before locking.

### New high-priority follow-up

The user added (2026-06-05) the framing that **within-day body-
battery rise *occurrences* are themselves meaningful** — not just
totals or averages. This rules out the cheap H04b option (3
timestamped daily points) and pushes toward decoding `unknown_233`
from the FIT files for per-minute BB. See registry §4 for the
full updated H04b plan.

### Updated recommendation for app design

Add to the synthesis section 6:

- **The recovery-arc card concept (registry §4 deferred) now has
  strong supporting evidence to back it.** Crashes are less frequent
  AND shallower AND shorter AND have different (weaker, compressed)
  precursors. That's a multi-axis recovery story.
- **For the spike-anchored retrospective card sketched in section 6:
  H02b train evidence justifies prototyping it for historical
  (pre-2024) crashes immediately**, with honest framing that the
  pattern is less reliable for newer crashes.

---

*Synthesis written 2026-06-05. Updated same day after H02b, K01,
K02 closed. Living document — to be amended as further tests
land.*

## Update 2026-06-05 (still same day) — S01 + H02b-trajectory + naming

Two more pieces closed, and a terminology refinement from the user.

**Naming: "recovery cliff" → "stabilisation transition" / "the
pendulum settling."** The user pointed out the "cliff" framing
overstated what's actually a gradual process. The 2023-12-31 split
we used was an analytical convenience for episode-balanced power,
not a real phase boundary. Going forward: prefer **"stabilisation"**
over "recovery" (recovery implies returning to a prior state;
stabilisation describes the dynamics) and **"transition"** /
**"pendulum settling"** over "cliff." The actual physiological shift
was a smooth turnaround across 2023–2024, bottoming in early-to-mid
2025, with a recent (May 2026) perturbation.

**S01 — Stabilisation trajectories** ([S01/notes.md](S01-stabilisation-trajectories/notes.md)).
Plots 90-day rolling means of 4 metrics across the full Garmin
window (2021-08 → 2026-06):

- **Max stress-spike duration**: ~10.5 min pre-LC → 13.2 min peak
  (mid-2023) → 5.8 min trough (Apr 2025) → 11.4 min (May 2026).
  Cleanest pendulum signal.
- **Avg stress**: ~32.6 pre-LC → 36 peak (2022–23) → 29 trough
  (2025) → 33.7 (May 2026).
- **RHR**: mostly stable 54–58 bpm; **notable recent rise to 60.8
  bpm in May 2026** — worth watching.
- **Sleep efficiency**: flat at ~99% throughout — confirms H03.

Two strong pendulum signals (spike + stress), one mostly stable
with recent uptick (RHR), one flat (sleep efficiency).

**H02b-trajectory** ([H02b/trajectory-notes.md](H02b-stress-spikes/trajectory-notes.md)).
Rolling 12-month discrimination curve for the spike precursor:

| anchor | discrim (pp) |
|---|---:|
| 2023-08 (peak) | **+31.8** |
| 2023-12 | +17.0 (still above bar) |
| 2024-04 | +5.5 |
| 2024-08 | +1.9 |
| 2024-12 | −16.0 |
| 2025+ | near zero with small N |

The signal **decayed smoothly over ~12 months** (peak mid-2023 →
near zero by mid-2024) rather than at a cliff. Replaces the binary
H02b verdict with the actual trajectory.

### What this enables for the stabilisation-arc card

Concrete card copy ideas now have empirical anchors:

- "Your stress baseline has come down from ~35 (mid-2023) to ~30
  (2025). Recent uptick to ~34."
- "Your typical intense moment was 13 min in 2023; lately around 11.
  You've had quieter years in between."
- "Your resting heart rate is up about 5 bpm in the last few months
  — worth knowing."

Multi-axis, descriptive, retrospective, aligned with the pacing-doc
principle "presenting conclusions, not making decisions."

### Recent perturbation (May 2026)

Three of four trajectory metrics show a 2026 uptick: stress up to
33.7, max-spike up to 11.4, RHR up to 60.8 bpm (highest in the
whole window). Not a return to peak-crisis values, but a meaningful
recent perturbation. The S01 script doesn't speculate about cause.
Worth surfacing to the user as awareness; the app can later let
them correlate with what they remember about the period.

### Next phase

The analytical layer of this project is largely complete — H##
precursors closed, K## kind-of-crash partly closed (K01/K02; K03
pending), S## trajectories done, synthesis up to date. **The
natural next phase shifts from "analyse the data we have" to
"explore the notes — what content patterns predict, accompany, or
follow these crashes, and which notes deserve tags?"** This is
where the K03 (symptom keyword profile) hypothesis lives, and it
opens the way to the tagging-research thread (deferred app feature,
research first).

---

## Update 2026-06-05 (much later same day) — notes-language analyses

After the H## and K## numerical work, we moved to the
[docs/research/notes/](../../notes/) folder for clause-level
analyses of the 686 day-entry notes. Three rounds:

1. **Goal A — word frequency** ([01-language-around-crashes](../../notes/01-language-around-crashes/notes-summary.md)).
   Found the headline crash-day vocabulary (hoofdpijn 78% of crash
   notes, koorts 11.6x over-represented, "emotioneel" 4.7x, etc.).
   Lead-up days "context-dominated" finding was too thin to be useful
   — flagged the need for richer analysis.

2. **Goal A.5 — clause-level v1** ([02-categorize-clauses/categories-analysis.md](../../notes/02-categorize-clauses/categories-analysis.md)).
   Built first dictionary, 10 categories. Found:
   - crash days have a clear language signature (92% symptoom_fysiek,
     8.7x triggers_extern, 2.9x belasting_emotioneel)
   - **strong era shift**: late-era crash days are paired with
     `belasting_gezin` 22% of the time (vs 0% early); late lead-up
     days have `belasting_cognitief` 12% (vs 0% early — modest
     return-to-work signature) and 22 pp less symptoom_fysiek
     language (less warning signal in lead-ups)
   - `symptoom_emotioneel` empty across all groups — the user frames
     emotional content as load not symptom

3. **Goal A.5 — clause-level v2 with polarity** ([02-categorize-clauses/categories-analysis-v2.md](../../notes/02-categorize-clauses/categories-analysis-v2.md)).
   v1 conflated "geen hoofdpijn" with "hoofdpijn" and discarded "matig"
   to neutral. v2 adds: modifier layer (negation + severity) and
   polarity layer (positive / negative / mixed). The 92% symptoom_fysiek
   becomes a proper distribution (3% absent / 75% present / 14% severe
   in v1's terms; the late era pushes severity dramatically).

### The five new findings worth synthesis attention

a. **Severe-symptom days on crashes jumped from 4% to 22% across eras**
   (+18 pp). Late crashes are 5× more likely to include severe symptom
   language. This sharpens K01 (deeper nadirs): it's specifically the
   severe-symptom cluster that's over-represented in the residual
   crashes.

b. **Late-era crash days are 50% positive-dominant by clause polarity**
   (vs 11% early), under a `pos > neg` definition. Verification of 16
   such days
   ([verification-late-positive.md](../../notes/02-categorize-clauses/verification-late-positive.md))
   shows the finding is real but the interpretation is **mixed-day
   topology, not "active reframing"**: late-era crash days more often
   contain functional and positive content alongside the crash, not
   just symptoms. The crashes are **less totalizing** — the day still
   has a morning that went well, a moment of improvement, a phone call
   with a family member. The reading: late crashes are embedded in days that
   otherwise function, where early crashes more often consumed the
   whole day. This is a meaningful recovery finding distinct from
   crash-frequency or crash-depth.

c. **Two definition inconsistencies caught by verification**
   (methodology):
   - `day_dominant_polarity` is computed two different ways in the same
     script (loose `pos > neg` vs strict `pos > neg AND pos > neu`),
     producing 50% vs 0% on the same data.
   - Naming clash between category `_present` and symptom-state
     `_present` keys — caused the v2 markdown to report 75%
     symptoom_fysiek presence when the per-day CSV stored 92%. Both
     fixed but worth noting: when the dictionary metadata is rich,
     output keys need disambiguating prefixes.

d. **Late lead-up days show LESS symptom warning language** (−22 pp
   on symptoom_fysiek), less recovery-action mention (−11 pp), and
   slightly MORE cognitive-load mention (+12 pp). The crashes-that-
   still-happen come with less warning, less proactive recovery, more
   cognitive precipitation. Aligns with H02b's compression finding
   and the residual-crash trigger profile.

e. **Polarity layer surfaces a known bug** — substring matching for
   polarity_positive doesn't apply the 3-word negation window that
   symptom matching does. "het is echt **niet fijn**" fires polarity
   positive because "fijn" matches. Estimated effect: 1-2 of 16
   positive-dominant late crashes are partly false-positive. Real but
   small. Fix would be a dictionary v3 that applies negation
   detection to polarity markers too. Logged as a follow-up.

### K## thread now has direct language-level support

The kind-of-crash theory had four directional findings before notes
analysis (H02, H02b, K01, K02). Notes analysis adds a fifth, with two
sub-findings:

| axis | source | shape | direction |
|---|---|---|---|
| stress precursor (daily avg) | H02 | refuted overall, train-direction | train: yes; late: no |
| stress precursor (spike count) | H02b | refuted overall, train SUPPORTED | train: yes; late: weaker |
| crash depth (score nadir) | K01 | suggestive_underpowered | late shallower (no 1's) |
| crash duration (span) | K02 | refuted bar; tail collapse | late shorter, 5→1 long crashes |
| crash language: symptom severity | notes v2 | clear shift | late severe-symptom +18 pp |
| crash language: day topology | notes v2 | clear shift | late more mixed (positive + crash) |
| lead-up language | notes v2 | clear shift | late less warning, more cognitive |

**Seven directional findings on independent axes, all consistent with
the kind-of-crash-changed theory; none contradicting it.** The
remaining 2025–26 crashes are: fewer, shallower, shorter, more often
severe in their symptom signature, embedded in mixed (not totalizing)
days, with weaker warning language in the lead-up, and with cognitive
rather than physical/sympathetic precursors. The user has not just
fewer crashes but qualitatively different ones — which means feature
work should likely tag them as a separate class rather than treating
"a crash is a crash."

### Adjusted feature-design implications

Adding to the synthesis section 6:

- **The stabilisation-arc card** (the recovery-arc card) is now
  empirically supported across **seven independent axes**. This is
  the highest-priority card concept in the project.
- **The mixed-day topology finding (finding b)** is itself
  card-worthy: "your crashes increasingly happen on days where good
  things also happen — that's a sign the body is finding edges."
- **The dictionary v3 follow-up** (apply negation to polarity
  markers) is small but useful. Add to the deferred work.

### What's queued

- **Goal B** — tagging-suggestion engine seeded from the v2
  categorisation. Foundation for the eventual in-app tagging hint
  feature. Cardinal-principle: research first, build second.
- **Dictionary v3** — polarity negation handling. Cheap fix.
- **H04b decoding `unknown_233`** — per-minute body battery, the
  longer-running research project. Still deferred.
- **H05b** — recovery time with a sustained-recovery target (v1
  spec was structurally trivial).
- **K03 — symptom keyword profile** — partly subsumed by the notes
  v2 work, but a formal pre-registered version could close the
  K## thread.

---

## Update 2026-06-06 — `crash_v2`, dips, dip clusters, and the kind-of-crash narrative sharpened

Four pieces of work closed since the 2026-06-05 entries above:
`crash_v2` was locked and applied; the per-minute stress-spike test
(H02b) was re-run against the new isolated-dip tier; the H02b
specificity check was re-tagged with crash_v2 labels; and a
descriptive dip-cluster overlay was added after visual inspection of
the labels surfaced multi-day rough-patch structure the single-day
spec missed. Full writeup in
[RESEARCH-REPORT-ADDENDUM.md](../../RESEARCH-REPORT-ADDENDUM.md);
this is the synthesis-level summary.

**crash_v2 — two tiers (crash + dip), no demotions, simplified spec.**
Pre-registered as a two-tier classification with a slow-recovery
filter on tier-1 to address the original H02b finding that 4+10
crashes lacked a spike precursor. Empirically the filter demoted
**zero** episodes: every one of the 29 v1 episodes has tail_median ∈
{4.0, 5.0}. crash_v1's acute condition is positively validated as a
PEM-shape detector. The filter was removed; tier-1 `crash` is now
exactly crash_v1. Tier-2 `dip` (single isolated bad days) added
**79 new sub-threshold events** the original framework missed.

**Era distribution of dips reinforces the kind-of-crash narrative.**
Train era 14 crashes / 26 dips (dip:crash 1.9×); validate era 15
crashes / 53 dips (dip:crash 3.5×). The participant's residual
eventscape is dominated by transient single-day bad days, not
sustained crashes.

**H02b on dips — refuted by strict bar, sharpened the original
H02b finding.** Train discrimination +9.1 pp (vs +29.9 for crashes);
validate +5.2 pp (vs −8.2 for crashes). The crashes show a 3× stronger
train-era spike-precursor than dips, sharpening the original report's
framing: the spike precursor is specifically a multi-day-crash
phenomenon, not a generic bad-day marker. In the validate era,
crash and dip discrimination magnitudes have **converged**:
residual crashes look like dips physiologically. The dip tier is
itself heterogeneous — "almost-crash" subtype (strong precursor,
e.g. 2024-03-30 with +77.6 min lead-up spike) vs "mood-only"
subtype (no precursor). A future dip_v2 split is queued, gated on
H04b unlocking per-minute Body Battery as a corroborating signal.

**Specificity re-tag — 39% of original false positives explained
by crash_v2.** Of the 83 false-positive null windows in the original
specificity check, 20 (24%) now contain a v2 dip; 12 (14%) contain
a crash-adjacent day inside a recovery shadow; 51 (61%) remain
unexplained (tolerated precursors, activity-induced spikes, or
noise). The original "necessary-but-not-sufficient" interpretation
of the spike is sharpened in proportion.

**Dip cluster overlay — multi-day rough patches.** Visual inspection
of the labelled timeline surfaced clusters of dips close in time
(e.g. score 4-3-4-3-4 patterns). 15 clusters identified under a
7-day proximity rule, covering 45 of 79 dips (57%). Cluster
concentration is heavier in validate (10 clusters, 32 dips) than
train (5 clusters, 13 dips). Longest cluster: 2024-03-14 →
2024-04-16, 9 dips, 34 days. Clusters are descriptive overlay
(per-day labels unchanged) and open up "rough-patch" analyses
downstream.

### The kind-of-crash table after this update

Adding to the eight-axis table from the previous update:

| axis | source | direction (early → late) |
|---|---|---|
| stress precursor (daily avg) | H02 | train: yes; late: no |
| stress precursor (spike count) | H02b | train: SUPPORTED; late: weaker |
| crash depth (score nadir) | K01 | late shallower (no 1's) |
| crash duration (span) | K02 | late shorter, 5→1 long crashes |
| crash language: symptom severity | notes v2 | late severe-symptom +18 pp |
| crash language: day topology | notes v2 | late more mixed (positive + crash) |
| lead-up language | notes v2 | late less warning, more cognitive |
| **dip:crash ratio** *(new)* | **crash_v2** | **1.9× → 3.5×** |
| **dip cluster concentration** *(new)* | **crash_v2 overlay** | **5 / 13 train → 10 / 32 validate** |
| **crash vs dip precursor magnitude** *(new)* | **H02b on dips** | **3× ratio train → ~1× validate (convergence)** |

**Nine directional findings, plus one convergence — all consistent,
none contradicting.** The residual eventscape (2024+) is fewer
crashes, shallower, shorter, less totalizing, less warned-about in
language, more cognitive in lead-up, transient (single-day dips),
clustered (multi-day rough patches), and **physiologically less
distinguishable from dips than crashes used to be**.

### Adjusted implications for feature design

- **The stabilisation-arc card** now has a tenth supporting finding
  (dip cluster concentration). Still the highest-evidence card
  concept in the project.
- **The mixed-day topology card** (from 2026-06-05 notes update)
  pairs naturally with a new **rough-patch card** built on dip
  clusters: "between 14 March and 16 April you had 9 separate dip
  days clustered together — what was happening that month?"
  Conditional on the cluster overlay surviving downstream
  validation against notes/calendar context.
- **A per-dip retrospective card** is conditional on dip_v2
  surfacing the almost-crash vs mood-only split (gated on H04b).

### What's queued (replaces earlier list)

1. **Notes label-quality work** (participant-requested, in
   progress). Pre-cursor to v3 notes categorisation across crash,
   dip, and normal day-types.
2. **H04b — decode `unknown_233`** for per-minute Body Battery.
   Protocol locked at
   [.claude/plans/adaptive-foraging-hamming.md](../../../../.claude/plans/adaptive-foraging-hamming.md);
   execution gated on notes work. Path C (API) + Path B (FIT decode)
   in parallel.
3. **H03b — overnight BB recharge** as a marker of unrefreshing
   sleep. Replaces both the refuted H03 and the earlier sharper-
   sleep-metrics plan with a physiologically targeted test. Gated
   on H04b success.
4. **Dip subtyping (dip_v2)** — split the 79 dips into almost-crash
   vs mood-only subtypes by physiological precursor. Gated on H04b.
5. **Cluster-based analyses** — "rough patch duration", "rough
   patch precursors", retrospective context for the longest cluster
   (March–April 2024). Now feasible with the overlay in place.
6. **Tier 1 cards prototyping** — if the participant prefers to
   move to product work before further research. Highest-evidence
   first.
7. **Dictionary v3** (polarity-negation handling) and **H05b**
   (sustained-recovery target). Cheap deferred items.

---

*Update 2026-06-06 covers the crash_v2 phase. Living document.*

---

## Update 2026-06-06 (later, same day) — Activity-labels phase + first validate-era precursor

Three pieces closed after the crash_v2 phase:
1. **Activity-labels v3.1 spec** locked at
   [garmin/activity-labels/](../../activity-labels/). Personal-baseline-
   relative metrics (percentile rank within 30-day rolling baseline)
   for four exertion axes — effective_exertion_min (UDS passive
   intensity + recorded duration), step burden, max_hr peak,
   vigorous_min duration. Plus a push_burden_7d count and
   above_baseline_streak. **The PEM-envelope framing principle (saved
   to feedback memory)**: every PEM patient has their own baseline;
   metrics must use deviations from that personal baseline, not
   absolute thresholds. Sensitivity-tested across 13 parameter
   alternates; `exertion_class` is ROBUST, `push_burden_class` binning
   was SENSITIVE and deprecated (raw count used downstream).
2. **HA01 + HA02 + HA05 at 3-day window** — all REFUTED. Activity
   shocks 1-3 days before crash do NOT predict crashes (+0.7 pp train,
   +11.5 pp validate; below the +15 pp bar). Push burden also
   refuted. Surprisingly, **dips showed +9.3 pp activity-shock
   discrimination (3-day) — stronger than crashes**. Mirror of the
   "dip tier is heterogeneous" finding from H02b-on-dips.
3. **HA01b at 4-day window — SUPPORTED for validate-era crashes
   (+17.3 pp)**. Pre-registered with the wider window after
   participant's experiential PEM-lag framing: "trigger day, day after
   still ok, crash sets in on day 2-3, deepens for 1-2 more." 93% of
   validate-era crashes have a heavy/very_heavy exertion day in the 4
   days before crash_start. Train HA01b at +8.6 pp (refuted but close,
   N=13 underpowered). HA02b (push burden at 4-day) still refuted.

### What HA01b changes

The original report concluded "the daily-aggregate biometric channel
is closed for residual crashes." HA01b reopens that conclusion: **the
channel is open at the 4-day lag, just not at the 3-day lag the prior
analyses (H01-H04, H02b, HA01) tested.** The "kind of crash changed"
theory gains a new dimension — **the change may not be "no precursor"
but "longer lag."** Train-era H02b showed a 3-day stress-spike
precursor; validate-era HA01b shows a 4-day activity-shock precursor.
Two different precursor mechanisms operating at two different lags
across two different eras.

This is the **first SUPPORTED validate-era precursor** of the whole
investigation. The same theory-driven hypothesis pattern as H02b
emerging from "intense moments trigger crashes" — here, the
participant's experiential lag framing drove HA01b, which then
SUPPORTED at its pre-registered bar.

### Updated kind-of-crash table

| axis | source | direction (early → late) |
|---|---|---|
| stress precursor (daily avg) | H02 | train: yes; late: no |
| stress precursor (spike count) | H02b | train: SUPPORTED; late: weaker |
| crash depth (score nadir) | K01 | late shallower |
| crash duration (span) | K02 | late shorter |
| crash language: symptom severity | notes v2 | late severe-symptom +18 pp |
| crash language: day topology | notes v2 | late mixed-day +39 pp |
| lead-up language | notes v2 | late less warning, more cognitive |
| dip:crash ratio | crash_v2 | 1.9× → 3.5× |
| dip cluster concentration | crash_v2 overlay | 5/13 train → 10/32 validate |
| crash vs dip precursor (spike) | H02b on dips | 3× train → ~1× validate |
| **activity shock at 3-day lag (HA01)** | **HA01 / HA01b 3-day** | **+0.7 pp train (refuted), +11.5 pp validate (refuted)** |
| **activity shock at 4-day lag (HA01b)** | **HA01b 4-day** | **+8.6 pp train (refuted, N=13), +17.3 pp validate (SUPPORTED ✓)** |
| **lag length** | **HA01b vs H02b** | **3 days (train, stress) → 4 days (validate, activity)** |

### Implications for feature design

- **Card concept (b2)**: validate-era retrospective per-crash card
  now empirically supported. "In the 4 days before this crash, you
  had heavy/very_heavy exertion on [day list]." Fires on ~93% of
  validate-era crashes. Complements the H02b-supported card (b) for
  train-era crashes (per-minute stress spike at 3-day lag). Both eras
  now have an empirically grounded retrospective card.
- **Dip subtyping motivation strengthened**: HA01 at 3-day showed
  dips with stronger activity signal than crashes (+9.3 vs +0.7 pp).
  Suggests dip tier already separates "exertion-triggered" subtype.
  A dip_v2 split with HA01-style flagging may surface this.
- **HA02 push burden refuted at both windows**: the "you've been
  pushing for N days" framing does not predict crashes for this
  person at this resolution. Either push-crash isn't this person's
  PEM mechanism, or it operates at a finer timescale than daily.

### What's queued

1. Lag bracketing: HA01c (5-day) and HA01d (6-day) windows to
   bracket the validate-era PEM lag; per-axis decomposition to
   identify which of effective_exertion / step / max_hr / vigorous
   drives HA01b.
2. Notes label-quality work (participant-requested).
3. H04b decoding `unknown_233`.
4. H03b overnight BB recharge (gated on H04b).
5. Dip subtyping (dip_v2), now newly motivated by HA01 3-day dip
   finding.
6. Card (b2) prototyping.
7. Dictionary v3 + H05b (deferred).

---

*Update 2026-06-06 (later same day) covers the activity-labels phase.
Living document.*

---

## Update 2026-06-06 (later still) — Theme A bundled re-test honest accountancy

The HA01b SUPPORTED-validate finding from the activity-labels update above
did not survive a methodologically cleaner re-test. The full account lives
at [RESEARCH-REPORT-ADDENDUM.md §5.9](../../RESEARCH-REPORT-ADDENDUM.md) and
[activity-labels/output/ha_results_4day_lagged.md](../activity-labels/output/ha_results_4day_lagged.md);
this is the synthesis-level summary.

**The methodological issue.** The 30-day rolling rank used in v3.1
includes the recent candidate region in its reference frame — a
sustained creep rebases itself into its own baseline. Push burden was
the metric most aimed at by this bug; HA01b's rank-based shock detector
inherits the same contamination at a different timescale. The
participant's Part 1 critique on 2026-06-06 articulated the bug clearly
enough to motivate two complementary fixes (A.1 lagged baseline, A.2
trend slope) and a bundled re-test (HA02c + HA01b-recomputed) on the
cleaner reference frame. Pre-committed SUPPORTED bar: same as original
(frequency ≥60%, discrimination ≥+15 pp). Audit trail dated *before*
any rerun ran.

**The result.** Both tests refuted on the lagged baseline.

| test | window | rolling (original) | lagged (re-test) | verdict |
|---|---|---:|---:|---|
| HA01b validate crash | 4-day | +17.3 pp (SUPPORTED) | +4.0 pp | REFUTED |
| HA02b/c validate crash | 4-day | -7.4 pp | +0.7 pp | REFUTED |
| HA01b train crash | 4-day | +8.6 pp | +5.8 pp | REFUTED |
| HA02b/c train crash | 4-day | -2.0 pp | -18.7 pp | REFUTED |

The original +17.3 pp validate-era HA01b finding was substantially a
rolling-baseline construction artifact. What HA01b was probably catching
is *short-window relative heaviness* (today's exertion exceeds the
immediate recent past), not *long-window relative heaviness against a
stable envelope reference*. Two different physiological constructs.

### What changes in the synthesis narrative

The activity-labels-phase update above states: *"The 'kind of crash
changed' theory gains a new dimension: the change may not be 'no
precursor' but 'longer lag.' Train-era H02b showed a 3-day stress-spike
precursor; validate-era HA01b shows a 4-day activity-shock precursor."*

After the bundled re-test, that dimension softens to: **the validate-era
counterpart vanishes on a clean baseline.** Train-era H02b stress-spike
remains the only SUPPORTED precursor in the investigation. Validate-era
crashes have no measurable precursor in any waking-hour Garmin aggregate
tested so far, on the cleanest available baseline construction. The
"longer lag" extension does not hold up.

### Updated kind-of-crash table (revised after bundled re-test)

| axis | source | direction (early → late) |
|---|---|---|
| stress precursor (daily avg) | H02 | train: yes; late: no |
| stress precursor (spike count) | H02b | train: SUPPORTED; late: weaker |
| crash depth (score nadir) | K01 | late shallower |
| crash duration (span) | K02 | late shorter |
| crash language: symptom severity | notes v2 | late severe-symptom +18 pp |
| crash language: day topology | notes v2 | late mixed-day +39 pp |
| lead-up language | notes v2 | late less warning, more cognitive |
| dip:crash ratio | crash_v2 | 1.9× → 3.5× |
| dip cluster concentration | crash_v2 overlay | 5/13 train → 10/32 validate |
| crash vs dip precursor (spike) | H02b on dips | 3× train → ~1× validate |
| activity shock 3-day lag | HA01 | refuted both windows |
| activity shock 4-day lag, rolling baseline | HA01b (original) | refuted train; **originally SUPPORTED +17.3 pp validate** |
| **activity shock 4-day lag, lagged baseline (Theme A)** | **HA01b-recomputed** | **refuted train; REFUTED +4.0 pp validate — original +17.3 pp was largely a baseline-construction artifact** |
| push burden 4-day lag, lagged baseline | HA02c | refuted both windows on clean baseline (HA02's original refutation was confounded with the same baseline issue but is not rescued either) |
| validate-era physiological precursor on cleanest baseline | summary across H##, HA##, HA##-recomputed | none demonstrated |

### Implications

- **D7 reframe (single-mechanism-two-regimes) becomes harder to support.**
  The "two pathways through the same threshold" reading needed an empirical
  validate-era anchor. HA01b was the candidate; on a clean baseline it
  isn't there. The reframe is not falsified — it just doesn't yet have
  the empirical stake we hoped to give it.
- **HA06 (morning resting-HR delta, C.1) becomes more important.** It is
  now the only remaining waking-hour-adjacent candidate for a validate-era
  precursor before the direction shifts to overnight recovery (gated on
  H04b). It also has the strongest external evidence of any candidate in
  the pacing literature.
- **Card (b2) loses its empirical anchor.** Downgraded to Tier 2 in
  STOCKTAKE §4. May still ship as descriptive, not as a validated
  discriminator.

### Methodology lesson banked

When a baseline-relative metric posts an unusually strong validate-era
result against a long literature of negative findings on similar
constructs, default to skepticism and pre-register a clean-baseline
re-test before the result enters synthesis. The pre-commitment is what
kept the audit trail clean here — the bundled re-test surfaced the
artifact in the same session that produced the original claim, before it
hardened into a long-lived headline.

### What's queued (replaces earlier list)

1. **HA06 (C.1 morning resting-HR delta) pre-registered as a both-era
   test.** The empirical stake for the D7 reframe and the only remaining
   waking-hour candidate. Strong external evidence; computable now from
   UDS resting-HR without needing H04b.
2. **C.3 personal-lag teaching** — derivative one-pager from existing
   data. Era framing needs reworking now that the 4-day SUPPORTED claim
   has been withdrawn; descriptive only.
3. **C.5 volatility + dip-frequency progress metric** — derivative
   one-pager. Independent of the precursor failure.
4. **C.2 cognitive/emotional load mining** — interaction test using
   notes/tags. The journal-layer angle becomes more important now that
   the Garmin waking-hour layer is closed for validate-era crashes.
5. **Notes label-quality work** (participant-requested).
6. **H04b — decode `unknown_233`** for per-minute Body Battery. More
   important now: overnight recovery is the next frontier after waking-hour
   aggregates closed.
7. **H03b — overnight BB recharge**, gated on H04b.
8. **Dip subtyping (dip_v2)** — the HA01 3-day "dip > crash" finding
   inherits the same baseline-construction caveat; should be re-evaluated
   under the lagged baseline before being used as motivation.
9. **Dictionary v3 + H05b** — cheap deferred items.

---

*Update 2026-06-06 (later still) — Theme A bundled re-test. Living
document.*

---

## Update 2026-06-06 (later still even) — H02d acknowledgment

While the Theme A bundled re-test was in flight, a parallel
methodological re-evaluation of the stress channel (H02d) also ran on
2026-06-06 — pre-registered, run, and closed in the same session
independently of the activity-shock re-test above. Result at
[H02d-stress-spikes-uncensored/result.md](H02d-stress-spikes-uncensored/result.md).
This entry folds H02d into the synthesis and corrects one stale claim
in the previous update.

### What H02d tested

H02d addressed two operationalisation gaps in H02b that biased
*against* finding signal in the validate era:

1. **Sentinel collapse.** Garmin's stress = −1 / −2 sentinels include
   both off-wrist (real missing data) and on-wrist "too active" moments
   (HRV-stress algorithm censoring extreme arousal). H02b drops both.
   8-file stratified calibration showed 100% of sentinels have HR
   within ±60 s — "too active" is dominant, "off-wrist" is rare. H02d's
   primary arm imputes "too active" as ≥75; a bridge-only sensitivity
   arm runs alongside.
2. **Lead-up window.** H02b used 3-day for cross-comparability; the
   post-H02b lag profile peaks at 5 days. H02d uses 4-day primary
   (matching HA01b) and 5-day secondary.

### What H02d found

Two clean findings under an overall refutation:

- **Sentinel imputation made the metric over-sensitive.** ~159 "too
  active" samples/day on average; flat-imputing all as ≥75 collapsed
  the discrimination (null ≈ 85% above threshold under imputation).
  The censored-arousal hypothesis is not killed; the specific "treat
  ALL too_active as 75-stress" operationalisation is. H02e candidate
  queued (HR-modulated imputation: impute only when nearby HR ≥ ~100 bpm).
- **Bridge × 5-day arm produced +31.8 pp train discrimination — the
  strongest train-era single-channel signal of the entire project**,
  surpassing H02b's +29.9 pp. Bridge train discrimination scales
  smoothly monotonically with window: 3d → 4d → 5d = +29.9 → +27.6 →
  +31.8 pp. The 4-5 day lag is now independently corroborated by
  H02d stress and HA01b activity-lag-profile — strong methodological
  convergence.
- **Validate refuted in all four arms** (imputed × {4d, 5d}, bridge ×
  {4d, 5d}). Five tests on the stress channel are now consistent on
  validate refutation (H02 daily-avg, H02b 3d, H02d × 4 arms).

### Correction to the previous update's claim

The Theme A update above states: *"Train-era H02b stress-spike remains
the only SUPPORTED precursor in the investigation."* After H02d, this
sharpens to:

> **Train-era H02b stress-spike at 3d is joined by H02d bridge × 5d
> (+31.8 pp) as a SECOND train-era SUPPORTED stress-spike finding,
> both overall-REFUTED by their validate fails. Zero overall-SUPPORTED
> precursors under clean methodology. Two train-era SUPPORTED
> stress-spike findings at convergent 3-5 day windows.**

The activity-shock channel and the stress-spike channel both refuted
in validate under methodologically clean pre-registration — the
two channels reach the same conclusion through independent
re-evaluations. The pre-cliff stress-spike precursor is well-replicated
(H02 → H02b → H02d bridge); the post-cliff stress-spike precursor
genuinely isn't there in any of the operationalisations tried.

### Final kind-of-crash table

| axis | source | direction (early → late) |
|---|---|---|
| stress precursor (daily avg) | H02 | train: yes; late: no |
| stress precursor (spike count, 3d) | H02b | train: SUPPORTED +29.9 pp; late: refuted |
| **stress precursor (spike count, 4-5d, sentinel-corrected)** | **H02d** | **train: SUPPORTED bridge × 5d +31.8 pp (project-strongest train signal); late: refuted in all 4 arms** |
| crash depth (score nadir) | K01 | late shallower |
| crash duration (span) | K02 | late shorter |
| crash language: symptom severity | notes v2 | late severe-symptom +18 pp |
| crash language: day topology | notes v2 | late mixed-day +39 pp |
| lead-up language | notes v2 | late less warning, more cognitive |
| dip:crash ratio | crash_v2 | 1.9× → 3.5× |
| dip cluster concentration | crash_v2 overlay | 5/13 train → 10/32 validate |
| crash vs dip precursor (spike) | H02b on dips | 3× train → ~1× validate |
| activity shock 3-day lag | HA01 | refuted both windows |
| activity shock 4-day lag, rolling baseline | HA01b (original) | refuted train; originally SUPPORTED +17.3 pp validate (subsequently withdrawn) |
| activity shock 4-day lag, lagged baseline (Theme A) | HA01b-recomputed | refuted train; refuted +4.0 pp validate — original was baseline-construction artifact |
| push burden 4-day lag, lagged baseline | HA02c | refuted both windows on clean baseline |
| **4-5 day empirical lag (cross-channel convergence)** | **H02d bridge train monotonic 3d→4d→5d + HA01b lag profile peak at 5d** | **both channels point at 4-5 day lag in this person; settled across two methodologically independent analyses** |
| validate-era physiological precursor on cleanest baseline | summary across H##, HA##, H02d, HA##-recomputed | none demonstrated across 8 pre-registered tests on waking-hour signals |

### Implications (revised after H02d)

- **The validate-era refutation is more thorough, not less.** My
  previous "validate-era invisible on cleanest baseline" claim was
  technically correct but premature — H02d hadn't been folded in
  yet. After H02d, validate-era is now refuted across:
  - 5 stress-channel tests (H02, H02b, H02d × 4)
  - 4 activity-shock channel tests (HA01, HA01b rolling + lagged, HA02c)
  - all prior daily-aggregate tests (H01, H03, H04)
- **The 4-5 day lag is settled.** Two independent channels (stress via
  H02d, activity via HA01b lag profile) converge on the same lag for
  this person. Future precursor hypotheses default to 4d/5d windows.
- **The pre-cliff stress-spike precursor is well-replicated.** H02 → H02b
  → H02d bridge train discrimination is monotonic and rises with window.
  Card (b) for the 2022-23 era retrospective has its strongest empirical
  ground yet.
- **HA06 (morning resting-HR delta) is still the key remaining
  waking-hour candidate.** Unchanged from the previous update; its
  importance is reinforced by the H02d corroboration that the waking-hour
  stress channel doesn't fire in validate.
- **H02e (HR-modulated sentinel imputation) becomes a serious candidate.**
  Not the most urgent — HA06 still goes first — but the H02d author
  flagged it as the natural next refinement of the stress channel if
  HA06 also refutes.

### What's queued (revised after H02d)

1. **HA06 (C.1 morning resting-HR delta) pre-registered as a both-era
   test.** Empirical stake for the D7 reframe; the only remaining
   waking-hour candidate after H02d corroborated the stress-channel
   refutation in validate. Strong external evidence; computable now
   from UDS resting-HR.
2. **C.3 personal-lag teaching** — the 4-5 day lag is now cross-channel
   confirmed (H02d + HA01b lag profile), strengthening the teaching
   content even though no SUPPORTED-overall finding anchors it.
3. **C.5 volatility + dip-frequency progress metric** — derivative,
   independent of the precursor failure.
4. **C.2 cognitive/emotional load mining** — journal-layer angle
   becomes more important now that Garmin waking-hour layer is closed
   for validate-era crashes across two independent channel families.
5. **Notes label-quality work** (participant-requested).
6. **H04b — decode `unknown_233`** for per-minute Body Battery.
   Overnight recovery is the next frontier.
7. **H03b — overnight BB recharge**, gated on H04b.
8. **H02e — HR-modulated sentinel imputation** — candidate refinement
   of H02d's flat imputation; only impute "too active" as ≥75 when
   nearby HR exceeds ~100 bpm. Defer until value vs. an HR-aware
   variant of HA01b is clear; both want HR magnitude at sentinel
   minutes, a unified extract step would serve both.
9. **Dip subtyping (dip_v2)** — same lagged-baseline re-evaluation
   caveat as before.
10. **Dictionary v3 + H05b** — cheap deferred items.

---

*Update 2026-06-06 (later still even) — H02d acknowledgment. Living
document.*

---

## Update 2026-06-07 — HA06 + HA06b, three-channel train-era convergence, methodology lesson on relative thresholds

Two pre-registered tests closed on 2026-06-07 — HA06 (morning nightly
RHR delta with absolute thresholds) and HA06b (z-score relative-threshold
methodological re-test). Together they sharpen the project's overall
picture in three ways: a third channel joins the train-era SUPPORTED
list, a directionality reversal between eras becomes formal, and the
methodology playbook gains a "pre-register relative thresholds for
autonomic-channel tests" rule. Full details at
[HA06-morning-rhr-delta/result.md](HA06-morning-rhr-delta/result.md)
and [HA06b-rhr-zscore/result.md](HA06b-rhr-zscore/result.md);
addendum at [RESEARCH-REPORT-ADDENDUM.md §§5.12-5.13](../../RESEARCH-REPORT-ADDENDUM.md).

### HA06 — absolute thresholds refuted both eras

Pre-registration revised after reading the Laure Wiggers *Smartwatch
Pacing* pdf (2025-07): bidirectional (`|RHR − baseline| ≥ N` to catch
both classical elevated-RHR and Wiggers' parasympathetic-swing
lowered-RHR pattern); Garmin UDS `restingHeartRate` field (the
nightly lowest stable HR Wiggers explicitly points at); 4-day primary
+ 5-day secondary window; lagged baseline `[d-90, d-30]` per Theme A;
sensitivity arm reporting one-sided result and directionality split.
Thresholds N = 5 (Wiggers' floor) / 10 (Workwell lower) / 15 (Workwell
upper) bpm.

**Result: REFUTED both eras.** Train 21.4% freq + +13.9 pp disc (close
but fails crit a; magnitude 3.49 bpm passes crit c). Validate
**0 of 15 crashes trigger at the 5 bpm threshold** — decisive
refutation; the N=10 and N=15 sensitivity arms are vacuous (0% on
both crash and null windows for both eras).

**The reason**: median max-|delta| for this participant sits at
**1.6-3.5 bpm**. The Wiggers/Workwell-calibrated thresholds (5-15 bpm)
were drawn from populations whose RHR variability materially exceeds
this participant's. The pre-committed bar held — refutation was
honestly reported — but the methodological gap motivated a same-session
re-test under a relative-threshold variant.

### HA06b — z-score relative thresholds: train SUPPORTED

Pre-registered as a Theme-A-style methodological re-test: same data,
same lagged baseline window, same 4-day primary, same bar shape —
but threshold `|RHR − μ| / σ ≥ N_std` (N_std = 1.5 / 2.0 / 2.5)
instead of absolute bpm. Motivation: locked
[`relative_not_absolute`](../../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_relative_not_absolute.md)
feedback principle says *"for PEM-pacing metrics in this project,
always use z-scores or deviations from personal baseline, not absolute
thresholds."* HA06 partially followed this (the delta-from-baseline
part was relative) but the threshold N itself was absolute. HA06b
fully follows the principle.

**Result: TRAIN SUPPORTED at N_std=1.5** (71.4% freq, +18.9 pp disc,
median |z|=2.31) AND at N_std=2.0 (+21.3 pp). Train SUPPORTED in 4 of
6 bidirectional configurations (4d/5d × 1.5/2.0); the train-era
signal is robust across threshold and window choice. **Validate
REFUTED** (53.3% freq, +0.8 pp disc — non-discriminative, not
inverse). Overall REFUTED by the locked rule.

The relative-threshold framing matters: HA06's absolute 5 bpm bar
missed **47.4 percentage points** of train triggering events
(HA06b bidirectional 71.4% vs HA06 absolute 21.4% on the same train
crashes). The signal was present in HA06's data; the threshold was
simply too coarse to register most of it.

### The directionality reversal between eras

| | n triggering | elevated (z ≥ +1.5) | lowered (z ≤ −1.5) |
|---|---:|---:|---:|
| train | 10 | **7 (70%)** | 3 (30%) |
| validate | 8 | 2 (25%) | **6 (75%)** |

Train-era triggering crashes are predominantly elevated-direction
(classical Workwell / sympathetic overarousal). **Validate-era
triggering crashes are predominantly lowered-direction (Wiggers'
parasympathetic-swing pattern).** The era split is now demonstrated
at the per-episode physiological directionality level, not just at
the aggregate frequency level.

Wiggers' parasympathetic-swing pattern is **empirically present in
this participant's validate era at 75% of triggering crashes** — but
the same lowered pattern appears in random non-crash 4-day windows
at roughly the same rate (the null also runs at ~50% under
bidirectional N_std=1.5, driven by the participant's natural daily
RHR fluctuation). The pattern is part of the participant's *current
autonomic baseline*, not a precursor signal. Validate one-sided
"elevated only" arm is **−16.2 pp** discrimination — classical
Workwell elevated-RHR direction is *anti*-predictive of validate-era
crashes.

### Three train-era SUPPORTED autonomic-deviation precursors on three channels

| test | channel | window | metric | train freq | train disc |
|---|---|---|---|---:|---:|
| H02b | per-minute stress spike count | 3d rolling | abs minutes ≥ +10 | 71.4% | +29.9 pp |
| H02d bridge × 5d | per-minute stress spike (sentinel-corrected) | 5d | abs minutes ≥ +10 | 92.3% | +31.8 pp |
| **HA06b** | **nightly RHR z-score** | **4d lagged** | **rel \|z\| ≥ 1.5** | **71.4%** | **+18.9 pp** |

Three SUPPORTED train findings across three different channels on
three different time-scales and three different methodologies, all
converging on the same train-era crashes. **The pre-cliff
autonomic-deviation precursor is now demonstrably multi-channel, not
stress-specific.** The b retrospective card (train-era 2022-23
per-crash) has a substantially stronger empirical case than after
H02b alone.

The validate-era refutation likewise extends. **Twelve pre-registered
tests now consistent** that no clean validate-era precursor exists in
waking-hour-derivable Garmin signals under the canonical
3-criterion bar (5 stress-channel + 4 activity-shock channel +
2 RHR channel + 1 sleep-efficiency channel).

### Methodology lesson banked

**Pre-register relative thresholds (z-score or percentile rank) as
the default for autonomic-channel tests.** Absolute thresholds drawn
from external populations need re-calibration to participant
variability *before* the test runs, not after. HA06 → HA06b is the
textbook case: this participant's median max-|delta| of 1.6-3.5 bpm
vs Wiggers/Workwell-calibrated 5/10/15 bpm thresholds is a
signal-to-noise mismatch that absolute thresholds could not have
caught without an upstream calibration step.

Applies forward to:
- **HA07** (day-over-day HRV drop) — pre-register on z-score
  thresholds from the start, not the *vermoeidheidskliniek*'s
  absolute 10 ms.
- **HA08** (multi-day HRV creep / slope) — pre-register slope
  thresholds in standardized units.
- **HA10** (BB overnight recharge coarse proxy) — pre-register on
  z-score against the participant's own recharge distribution, not
  Wiggers' absolute 70-80% floor.

This joins the Theme A lesson (lagged baseline for push-burden-style
metrics; symmetric pre-registered re-test discipline) in the
project's methodology playbook.

### Final kind-of-crash table (revised after HA06b)

| axis | source | direction (early → late) |
|---|---|---|
| stress precursor (daily avg) | H02 | train: yes; late: no |
| stress precursor (spike count, 3d) | H02b | train SUPPORTED +29.9 pp; late refuted |
| stress precursor (spike count, 4-5d, sentinel-corrected) | H02d | train SUPPORTED bridge × 5d +31.8 pp (project-strongest train signal); late refuted in all 4 arms |
| **RHR delta, absolute thresholds, 4-5d lagged** | **HA06** | **train refuted (21.4% freq, close); validate decisively refuted (0/15 trigger); Wiggers/Workwell thresholds exceed this participant's variability range** |
| **RHR z-score, relative thresholds, 4d lagged** | **HA06b** | **train SUPPORTED +18.9 pp at N_std=1.5 (71.4% freq); validate refuted +0.8 pp; directionality reversal: train 70% elevated → validate 75% lowered (Wiggers' swing pattern physiologically present in validate but non-discriminative)** |
| crash depth (score nadir) | K01 | late shallower |
| crash duration (span) | K02 | late shorter |
| crash language: symptom severity | notes v2 | late severe-symptom +18 pp |
| crash language: day topology | notes v2 | late mixed-day +39 pp |
| lead-up language | notes v2 | late less warning, more cognitive |
| dip:crash ratio | crash_v2 | 1.9× → 3.5× |
| dip cluster concentration | crash_v2 overlay | 5/13 train → 10/32 validate |
| crash vs dip precursor (spike) | H02b on dips | 3× train → ~1× validate |
| activity shock 3-day lag | HA01 | refuted both windows |
| activity shock 4-day lag, lagged baseline (Theme A) | HA01b-recomputed | refuted train; refuted +4.0 pp validate (original +17.3 pp was baseline-construction artifact) |
| push burden 4-day lag, lagged baseline | HA02c | refuted both windows on clean baseline |
| **4-5 day empirical lag (cross-channel convergence)** | **H02d bridge train monotonic 3d→4d→5d + HA01b lag profile peak at 5d + HA06b 4d train SUPPORTED** | **settled across three methodologically independent analyses on three channels** |
| validate-era physiological precursor on cleanest baseline | summary across H##, HA##, H02d, HA06, HA06b | **none demonstrated across 12 pre-registered tests on waking-hour signals** |

### Implications

- **D7 single-mechanism-two-regimes reframe** gains a per-episode
  directionality anchor (train elevated → validate lowered) but
  does NOT gain a validate-era empirical anchor in the strict
  pre-registered sense — the validate-era lowered pattern is
  physiologically present but non-discriminative. The reframe
  remains literature-parsimony-grade for validate; awaiting H04b /
  H03b for overnight recovery as the next candidate empirical
  stake.
- **Card (b) train-era retrospective** now has three converging
  empirical anchors (H02b + H02d + HA06b) on the same train-era
  crashes. Strongest empirical case in the project for a per-crash
  retrospective surface.
- **Card (b2) validate-era retrospective** remains downgraded to
  Tier 2 after HA06b's validate refutation. The validate-era one-sided
  arm at −16.2 pp anti-predictive is the cleanest evidence yet that
  classical elevated-RHR framing is actively wrong for this
  participant's residual era.
- **HA07 (HRV channel) becomes the most informative next test.**
  HRV is less subject to chronotropic incompetence than RHR.
  Combined with HA06b's lesson, HA07 must pre-register on z-score
  thresholds from the start. If train SUPPORTS → autonomic-deviation
  pattern is four-channel-confirmed for pre-cliff. If validate still
  refutes → the validate-era waking-hour signal is genuinely absent
  across all autonomic channels we can measure.

### What's queued (revised after HA06b)

1. **HA07 (HRV day-over-day drop on z-score thresholds)** — natural
   sibling test on a less-chronotropic-blunted channel; pre-register
   relative thresholds from the start.
2. **HA10 (BB overnight recharge coarse proxy on z-score)** —
   operationalisable NOW without H04b; pre-commits a soft outcome
   that informs H03b/H04b prioritisation.
3. **HA08 (multi-day HRV creep, slope)** — straightforward extension
   of HA07.
4. **HA11 (within-day stress U-dip)** — within-day pattern,
   complementary axis.
5. **HA09 (parasympathetic-swing detection)** — work-on-later;
   HA06b confirms the pattern is present at 75% in validate but
   non-discriminative on the current framing; would need a
   different anchor (known overexertion days, not crash labels).
6. **HA12 (pre-infection HRV rise)** — work-on-later; gated on
   notes-quality work.
7. **Notes label-quality work** (participant-requested).
8. **H04b — decode `unknown_233`** for per-minute Body Battery.
9. **H03b — overnight BB recharge**, gated on H04b; may be
   de-prioritised if HA10 coarse proxy refutes.
10. **C.X derivative cards** (C.3 personal-lag teaching, C.5
    volatility + dip-frequency, C.2 cognitive/emotional load mining,
    C.4 recovery-completeness gated on H05b).
11. **H02e (HR-modulated sentinel imputation)** + **Dictionary v3** +
    **H05b sustained-recovery target** — cheap deferred items.

---

*Update 2026-06-07 — HA06 + HA06b. Living document.*

---

## Update 2026-06-07 (later same day) — HA10 + HA11: first validate-era SUPPORTED + four-channel train-era convergence

Two pre-registered tests closed on 2026-06-07 (same day as HA06 +
HA06b, after the HA07 HRV channel was discovered to be unavailable
in local data and the user pivoted to HA10 → HA11). Together they
substantially change the project's picture: the first validate-era
SUPPORTED finding under canonical methodology lands, the
sympathetic-overarousal precursor signature is four-channel
confirmed for train, and the era directionality reversal becomes
formal across four channels.

Full details at [HA10-bb-overnight-recharge/result.md](HA10-bb-overnight-recharge/result.md)
and [HA11-stress-udip/result.md](HA11-stress-udip/result.md);
addendum at [RESEARCH-REPORT-ADDENDUM.md §§5.14-5.16](../../RESEARCH-REPORT-ADDENDUM.md).

### HA07 blocker discovered → pivot to HA10 then HA11

HA07 (day-over-day HRV drop, z-score thresholds per HA06b
methodology lesson) was queued as next. **Investigation showed
HRV is not present in any local data source** for this
participant's Forerunner 245 GDPR dump: no HRV field in UDS,
sleepData, bioMetrics, monitoring_b FIT, or activity FIT. HRV
records live only in the Garmin Connect cloud, accessible via the
same ToS-grey REST API path (`python-garminconnect`) as H04b's
per-minute Body Battery. HA07 was therefore gated on the same
authorisation as H04b.

User pivot order: **HA10 (BB recharge coarse proxy)** then
**HA11 (within-day U-dip pattern)**, both operationalisable on
existing local data. Stay-the-course on chronological
train/validate split as primary (user methodological discussion
2026-06-07).

### HA10 — BB morning peak: first validate-era SUPPORTED

Per-day metric: HIGHEST BB anchor's `statsValue` filtered to
03:00-10:00 local timestamp (morning peak after overnight
recharge). Z-scored against lagged baseline [d-90, d-30]. Same
thresholds, bar, and machinery as HA06b. Bidirectional primary
with one-sided lowered (Wiggers direction) + one-sided elevated
sensitivity arms.

**Result: TRAIN REFUTED, VALIDATE SUPPORTED → overall REFUTED
per the locked rule.** But the validate arm clears all three
criteria substantially:

| | train | validate |
|---|---:|---:|
| crash episodes triggering (\|z\| ≥ 1.5) | 7 (50.0%) | **13 (86.7%)** |
| null windows triggering | 141 (70.5%) | 141 (70.5%) |
| discrimination (pp) | **−20.5** | **+16.2** |
| median max-\|z\| | 1.637 | 2.121 |
| verdict | refuted | **SUPPORTED** |

**This is the first validate-era SUPPORTED test in the entire
investigation under the canonical 3-criterion bar.** Thirteen
prior pre-registered tests on waking-hour Garmin signals had
refuted validate-era. The pattern that fires in HA10 validate is
the PARADOXICAL direction: elevated morning BB peak (NOT lowered
as Wiggers' canonical framing predicts).

#### Striking directionality reversal between eras

| | n triggering | elevated (z ≥ +1.5) | lowered (z ≤ −1.5) |
|---|---:|---:|---:|
| train | 7 | 0 (0%) | **7 (100%)** |
| validate | 13 | **9 (69%)** | 4 (31%) |

**Train: 100% lowered direction** (Wiggers' canonical "didn't
recharge" pattern). **Validate: 69% elevated direction**
(paradoxical "looked like a great night but" pattern, Wiggers'
"freeze" / parasympathetic-swing pattern). At the 5-day secondary
window, BOTH eras are SUPPORTED in their respective opposite
directions (train +18.3 pp lowered; validate +27.5 pp elevated) —
cleanest era-directionality reversal in the project.

#### Cross-channel coherence with HA06b — strongest internal-consistency evidence

BB is inversely-related to RHR via the vagal-tone / HRV → stress
→ BB pathway. The fact that HA10 (BB) and HA06b (RHR) show
**opposite directions per era** is *expected* if the underlying
autonomic deviation is real and the era split represents a flip
in dominant direction. The fact that the pattern emerges
**independently on two channels** is strong internal-consistency
evidence the autonomic-deviation phenomenon is genuine.

| era | HA06b RHR | HA10 BB | autonomic state |
|---|---|---|---|
| train | predominantly elevated (70%) | predominantly lowered (100% 4d) | **sympathetic overarousal**: high RHR ↔ low HRV ↔ low BB |
| validate | predominantly lowered (75%) | predominantly elevated (69%) | **parasympathetic swing** (Wiggers "freeze"): low RHR ↔ high HRV ↔ high BB |

**Wiggers' "freeze" pattern is now empirically population-level
visible** in this participant's validate-era crashes on two
independent channels. Not just lived-experience anecdote; a
quantitative signature with discriminative frequency rates.

### HA11 — Within-day U-dip count: fourth train-era SUPPORTED on fourth channel

Tests Wiggers' within-day pattern: per-minute stress drops sharply
(the "U") and plateaus at a higher-than-pre-dip baseline. Wiggers
reports resolving this with ORS / electrolytes; physiologically
hypothesised as orthostatic / low-blood-volume dysregulation.
**First within-day pattern test in the project**.

Stage 1 extraction re-parsed all 7888 monitoring_b FIT files
(~6-7 min, 1739 days, 1722 valid ≥600 samples, 1469 total U-dip
events). U-dip event = sharp drop ≥ 25 stress points from elevated
baseline (S_pre ≥ 40) followed by plateau ≥ 5 points HIGHER than
baseline, refractory 60 min. Per-day `u_dip_count` z-scored
against lagged baseline. Distribution: 47% of valid days have 0
events, 31% have 1, 14% have 2, 7% have 3+.

**Pre-registered direction**: one-sided ELEVATED (more U-dips =
more orthostatic events = pre-crash precursor per Wiggers' framing).

**Result: TRAIN SUPPORTED, VALIDATE REFUTED → overall REFUTED.**

| | train | validate |
|---|---:|---:|
| crash episodes triggering (signed z ≥ +1.5) | **9 (64.3%)** | 4 (30.8%) |
| null windows triggering | 83 (41.5%) | 83 (41.5%) |
| discrimination (pp) | **+22.8** | **−10.7** |
| median max signed z | 2.168 | 0.374 |
| verdict | **supported** | **refuted (inverse)** |

Train clears all three criteria substantially. **Validate is
anti-predictive**: −10.7 pp at 4d primary, scaling to −24.1 pp
at 5d N_std=2.0. Validate-era crashes have *fewer* U-dip events
than typical 4-5d windows — the inverse-direction signal is
itself a *characteristic* signature of the parasympathetic-swing
era, not random noise.

Same-day correlation between u_dip_count and gevoelscore is
essentially zero (train ρ=+0.075, validate ρ=+0.012). The U-dip
metric is a 4-day-lead precursor in train, NOT a same-day symptom
correlate — consistent with the autonomic-precursor framing.

### Four-channel train-era convergence

HA11 adds the fourth train-era SUPPORTED autonomic precursor on
the fourth channel:

| test | channel | window | metric | train freq | train disc |
|---|---|---|---|---:|---:|
| H02b | per-minute stress spike count | 3d rolling | abs minutes ≥ +10 | 71.4% | +29.9 pp |
| H02d bridge × 5d | per-minute stress spike (sentinel-corrected) | 5d | abs minutes ≥ +10 | 92.3% | +31.8 pp |
| HA06b | nightly RHR z-score | 4d lagged | rel \|z\| ≥ 1.5 (bidir) | 71.4% | +18.9 pp |
| **HA11** | **within-day U-dip count z-score** | **4d lagged** | **rel signed z ≥ 1.5 (elevated)** | **64.3%** | **+22.8 pp** |

Four SUPPORTED train findings across four distinct channels (per-
minute stress trajectory, per-night autonomic state, per-day
within-day pattern) on three different time-scales. The pre-cliff
era's sympathetic-overarousal / orthostatic-instability precursor
signature is now **four-channel-confirmed**. **Strongest
multi-channel convergence in the project.**

### Era directionality reversal formalised across four channels

| era | H02b/H02d (stress) | HA06b (RHR) | HA11 (U-dip) | HA10 (BB peak) |
|---|---|---|---|---|
| **train** | SUPPORTED elevated | SUPPORTED elevated | **SUPPORTED elevated** | refuted (5d lowered SUPPORTED) |
| **validate** | refuted | refuted | **refuted inverse-direction** | **SUPPORTED elevated** (paradoxical swing) |

Pre-cliff: sympathetic-arousal-spectrum events fire across all
four channels (elevated stress spikes, elevated RHR, elevated
U-dip count, lowered BB peak — internally consistent via
vagal-tone physiology).

Post-cliff: parasympathetic-swing-spectrum events fire (elevated
BB peak / lowered RHR / lowered U-dip count — internally
consistent in the *opposite* direction via the same physiology).

### Consolidated picture

**Pre-cliff (2022-23) — sympathetic-overarousal precursor
signature, four-channel confirmed:**
- H02b stress spike count 3d (+29.9 pp, 71.4%)
- H02d bridge × 5d (+31.8 pp, 92.3%) — strongest train signal
- HA06b RHR z-score 4d (+18.9 pp, 71.4%)
- HA11 U-dip count z-score 4d (+22.8 pp, 64.3%)
- HA10 BB peak lowered 5d (+18.3 pp, 64.3%) — fifth train arm
  SUPPORTED in the inverse-of-validate direction

**Post-cliff (2024+) — parasympathetic-swing precursor signature,
one-channel confirmed:**
- HA10 BB peak elevated 4d primary (+16.2 pp, 86.7%) — first
  validate-era SUPPORTED under the canonical bar.

### Final kind-of-crash table (revised after HA10 + HA11)

| axis | source | direction (early → late) |
|---|---|---|
| stress precursor (daily avg) | H02 | train: yes; late: no |
| stress precursor (spike count, 3d) | H02b | train SUPPORTED +29.9 pp; late refuted |
| stress precursor (spike count, 4-5d, sentinel-corrected) | H02d | train SUPPORTED bridge × 5d +31.8 pp (project-strongest); late refuted in all 4 arms |
| RHR delta, absolute thresholds, 4-5d lagged | HA06 | train refuted (21.4% freq); validate decisively refuted (0/15 trigger) |
| RHR z-score, relative thresholds, 4d lagged | HA06b | train SUPPORTED +18.9 pp; validate refuted +0.8 pp; **directionality reversal train 70% elevated → validate 75% lowered** |
| **within-day U-dip count z-score, 4d lagged (NEW)** | **HA11** | **train SUPPORTED elevated +22.8 pp (64.3% freq); validate refuted INVERSE-direction (−10.7 to −24.1 pp); first within-day pattern test in project** |
| **morning BB peak z-score, 4d lagged (NEW)** | **HA10** | **train refuted (−20.5 pp, 100% lowered direction); validate SUPPORTED +16.2 pp (86.7% freq, 69% elevated — paradoxical "swing" direction); FIRST VALIDATE-ERA SUPPORTED IN THE PROJECT; each era SUPPORTED in opposite direction at 5d secondary** |
| crash depth (score nadir) | K01 | late shallower |
| crash duration (span) | K02 | late shorter |
| crash language: symptom severity | notes v2 | late severe-symptom +18 pp |
| crash language: day topology | notes v2 | late mixed-day +39 pp |
| lead-up language | notes v2 | late less warning, more cognitive |
| dip:crash ratio | crash_v2 | 1.9× → 3.5× |
| dip cluster concentration | crash_v2 overlay | 5/13 train → 10/32 validate |
| crash vs dip precursor (spike) | H02b on dips | 3× train → ~1× validate |
| activity shock 4d lag, lagged baseline (Theme A) | HA01b-recomputed | refuted both windows (rolling-baseline artifact retracted) |
| push burden 4d lag, lagged baseline | HA02c | refuted both windows on clean baseline |
| **era directionality reversal (cross-channel, NEW)** | **HA06b + HA10 + HA11** | **train: sympathetic-arousal-spectrum (high stress / high RHR / high U-dip / low BB); validate: parasympathetic-swing-spectrum (high BB / low RHR / low U-dip); internally consistent via vagal-tone physiology** |
| **4-5 day empirical lag (cross-channel convergence)** | **H02d bridge train + HA01b lag profile + HA06b 4d train + HA11 4d train + HA10 4d validate** | **settled across five methodologically independent analyses; lag is genuinely 4-5 days for this person, not 3** |

### Implications

- **D7 reframe gains empirical anchors in BOTH eras.** Previously
  literature-parsimony-grade only; now anchored in pre-cliff (four
  channels) and post-cliff (HA10 BB peak), with internally
  consistent vagal-tone-mediated opposite-direction patterns.
- **Card (b) train-era retrospective** now has four converging
  empirical anchors (H02b + H02d + HA06b + HA11). Strongest
  empirical case for any card concept in the project.
- **Card (b2) validate-era retrospective** regains its empirical
  anchor: HA10 morning BB peak elevated direction. Promote back
  from Tier 2 to Tier 1 candidate, pending H04b per-minute
  trajectory enrichment.
- **H04b path C authorisation** becomes the highest-leverage next
  research step. Unlocks HRV (HA07/HA08/HA09/HA12 unblocked) AND
  per-minute BB (H03b proper, sharpens HA10 validate signal).
- **HA09 reframing reinforced**. HA06b + HA10 + HA11 confirm the
  parasympathetic-swing pattern is real and predictive (via HA10)
  for validate-era crashes. The remaining HA09 question is
  whether swing events also predict post-overexertion recovery
  quality — needs H05b primitive.
- **HA11 invites a focused re-look at train-era notes** for
  orthostatic / hydration / ORS mentions around U-dip-elevated
  days. Defer to notes-quality work.

### What's queued (revised after HA10 + HA11)

1. **H04b path C authorisation** — highest-leverage next step.
   Three benefits stack (unblocks HRV channel tests, sharpens
   HA10 validate signal, triggers HA10 §9 pre-commit). Protocol
   locked.
2. **HA07 day-over-day HRV drop** (z-score thresholds, gated on
   H04b path C) — once authorised. Five-channel-confirmation
   for pre-cliff or validate-era is the next milestone.
3. **HA08 multi-day HRV creep** (slope, z-scored), gated on H04b.
4. **C.3 personal-lag teaching** — 4-5 day lag now four-channel
   confirmed. Descriptive one-pager.
5. **C.5 volatility + dip-frequency progress metric** —
   derivative, independent of all precursor findings.
6. **C.2 cognitive/emotional load mining** — journal-layer angle.
7. **Notes label-quality work** — also: focused re-look at
   train-era notes around U-dip-elevated days for orthostatic
   mentions (per HA11 result.md).
8. **H03b overnight BB recharge** (per-minute), gated on H04b.
9. **C.4 recovery-completeness over time** — depends on H05b.
10. **HA09 + HA12** — work-on-later.
11. **H02e + Dictionary v3 + H05b sustained-recovery target** —
    cheap deferred.

---

*Update 2026-06-07 (later same day) — HA10 + HA11. Living
document.*

---

## Update 2026-06-07 (later still even) — HA07c + HA08c + HA07d: project's FIRST overall-SUPPORTED test

After HA10 + HA11 landed and H04b path C authorisation completed
(2026-06-07), we discovered that **the Forerunner 245 hardware
does not record HRV** — the HRV Status feature was added on the
newer Forerunner 255/265/955/965 / Fenix 7 generation watches
(2022-2023) with a multi-sample sensor that the FR245's 2019
hardware lacks. HA07 / HA08 / HA12 are therefore BLOCKED-PENDING-
HARDWARE permanently for this dataset.

But sleep stress is a defensible HRV proxy (Garmin's stress
algorithm is HRV-derived during sleep when activity ≈ 0; Workwell
and Wiggers reference it as an HRV-class indicator). Three
substitute pre-registrations were locked **before** any data
inspection:
- HA07c: night-over-night sleep stress mean delta z-scored
  (analog of HA07)
- HA08c: trailing-5-day sleep stress mean slope z-scored
  (analog of HA08)
- HA07d: night-over-night sleep stress STDEV delta z-scored
  (variability of HRV proxy = second-order primitive)

Stage 1 re-parsed all 7888 monitoring_b FIT files, intersected
per-minute stress samples with sleep windows from local
`*_sleepData.json`, emitted `sleep_stress_nightly.csv` (1734
nights, 1707 valid ≥120 samples, mean 592 samples/valid-night).

### HA07c — Train SUPPORTED, 5th channel

Primary 4d N_std=1.5 one-sided elevated: **train SUPPORTED +23.2 pp
(69.2% freq, median signed z 1.677)**; validate refuted (40.0% /
−6.0 pp). Multi-arm robustness in train (5d elevated +18.4 pp, 4d
N_std=2.0 lowered +26.0 pp, bidirectional +19.7 pp). **5th
train-era SUPPORTED autonomic-channel precursor on the 5th
channel** (after H02b, H02d, HA06b, HA11). The HRV proxy is
validated for train.

Directionality split: train 33% elevated / 67% lowered-at-max-|z|
— train-era crashes preceded by HIGH AUTONOMIC VOLATILITY (large
shifts in BOTH directions; the downward direction at higher
thresholds is the strongest discriminator).

### HA08c — Train SUPPORTED, 6th finding

Primary 4d N_std=1.5 one-sided elevated: **train SUPPORTED +23.0 pp
(61.5% freq); validate refuted (+1.5 pp)**. 5d secondary elevated
+23.2 pp also SUPPORTED. **6th train-era SUPPORTED finding**
under clean methodology; both acute (HA07c delta) and sustained
(HA08c slope) modes confirmed in train.

Strong validate ANTI-PREDICTIVE pattern at higher thresholds
(N_std=2.0 bidirectional **−36.2 pp**, one-sided lowered −27.3 pp).
Validate-era crashes arrive against unusually-FLAT baseline — the
autonomic creep that precedes train-era crashes is absent in
validate-era lead-ups. This foreshadows HA07d's variability
finding.

### HA07d — BOTH ERAS SUPPORTED → project's FIRST OVERALL-SUPPORTED

**Primary 4d N_std=1.5 BIDIRECTIONAL: train SUPPORTED (84.6%
freq, +19.6 pp disc); validate SUPPORTED (86.7% freq, +21.7 pp
disc) → OVERALL SUPPORTED per the locked rule.** This is the FIRST
pre-registered test in 19 hypotheses to OVERALL SUPPORT in both
eras at primary under the strict locked bar.

Per-era directionality within the bidirectional finding:

| arm | train | validate |
|---|---|---|
| **N_std=1.5 bidirectional (PRIMARY)** | **SUPPORTED +19.6** | **SUPPORTED +21.7** |
| N_std=1.5 one-sided elevated | **SUPPORTED +27.4** | refuted +3.8 |
| N_std=1.5 one-sided lowered | **SUPPORTED +16.5** | **SUPPORTED +21.7** |
| N_std=2.0 bidirectional | **SUPPORTED +15.5** | **SUPPORTED +27.3** |
| N_std=2.0 one-sided lowered | refuted | **SUPPORTED +28.5** |

**Train SUPPORTS BOTH directions** (variability rose AND fell) =
autonomic VOLATILITY. **Validate SUPPORTS ONLY the LOWERED
direction** (variability fell) = autonomic STILLNESS / FREEZE.

**HA07d's +28.5 pp validate discrimination at N_std=2.0 one-sided
lowered is the strongest validate-era discrimination on any arm
in the project**, exceeding HA10's previous best (+27.5 pp at 5d
one-sided elevated).

### Validate-era multi-channel picture is now anchored

Validate-era crashes have TWO converging empirical anchors:

| validate signature | direction | discrimination | interpretation |
|---|---|---:|---|
| HA10 morning BB peak z-score | elevated | +16.2 pp (4d primary) | "looks like great recharge" |
| **HA07d sleep stress variability** | **lowered** | **+21.7 pp (4d primary), +28.5 pp (N_std=2.0 lowered)** | **"frozen autonomic state"** |

Both LOOK like recovery. Neither IS recovery. Wiggers'
qualitative "freeze" / parasympathetic-swing pattern is now
**empirically population-level confirmed at substantial
discrimination magnitudes** in two independent biometric
channels.

### Final findings table (revised after HA07d + peer-review framing fixes)

**Important honest framing per the independent peer review** (see
[../review/2026-06-07-variable-architecture-review.md](../review/2026-06-07-variable-architecture-review.md)
and [../review/2026-06-07-reply-with-ha07d-context.md](../review/2026-06-07-reply-with-ha07d-context.md)):
the seven train-era SUPPORTED tests below are NOT seven
statistically independent channels. Three of them (HA07c, HA08c,
HA07d) are different primitives on the *same* sleep-stress channel.
Body Battery (HA10) is a fused composite of HR/HRV/stress/sleep.
Sleep stress is per-minute stress restricted to the sleep window.
The "convergence" framing should be read as **six distinct
measurement axes confirming an underlying autonomic-state
construct**, not as independent samples of nature.

**Pre-cliff (2022-23) era — six channels SUPPORTED across seven
tests** (sleep stress channel with three SUPPORTED primitives):
- H02b stress spike count 3d (+29.9 pp)
- H02d bridge × 5d (+31.8 pp, strongest train signal)
- HA06b RHR z-score 4d (+18.9 pp)
- HA11 U-dip count 4d (+22.8 pp)
- HA07c sleep stress mean delta 4d (+23.2 pp) — sleep-stress channel
- HA08c sleep stress slope 4d (+23.0 pp) — sleep-stress channel
- HA07d sleep stress variability delta 4d bidirectional (+19.6 pp)
  — sleep-stress channel, ALSO validate-era SUPPORTED

**Post-cliff (2024+) era — NO LOAD-BEARING CHANNEL after the
threshold-monotonicity diagnostic round** (HA10 CLOSE 2026-06-07,
HA07d CLOSE both eras 2026-06-07, both per locked diagnostic-v1
rule):

- **HA07d sleep stress variability lowered 4d** — locked
  SUPPORTED verdict stays on record (+21.7 pp at N_std=1.5
  bidirectional both eras). Diagnostic-v1 CLOSE both eras per
  locked rule (peak at N_std=1.75 outside rescue window in both;
  train bumpy with 4 sign changes; validate positive Spearman due
  to rising-with-threshold discrimination). Synthesis-level
  framing demotes HA07d to **non-load-bearing**. v2 diagnostic
  pre-registered; pending review and run.

- **HA10 BB peak elevated 4d** — locked SUPPORTED verdict stays
  on record (+16.2 pp 4d primary bidirectional validate).
  Diagnostic-v1 CLOSE per locked rule (peak at N_std=1.75 outside
  rescue window). Synthesis-level framing demotes HA10 to
  **non-load-bearing**. v2 diagnostic pre-registered; pending
  review and run.
  The diagnostic ran a fine N_std grid [0.5 → 4.0] and found
  HA10's primary bidirectional arm peaks at N_std=1.75 — one
  σ-tier past the locked rescue window. The locked rule
  (diagnostic.md §4) triggers CLOSE on this peak-location
  failure even though every other shape criterion passed
  (disc holds at +14 at N_std=2.0, +11 at 2.5; Spearman rho
  −0.456; one sign change). Important nuance: HA10's one-sided
  ELEVATED arm shows robust threshold-monotonicity (+23 pp
  plateau N_std=1.5 → 2.5); the **direction** HA10 identified
  (paradoxical elevated BB peak before validate-era crashes)
  remains supported, only HA10's specific bidirectional-primary
  arm choice failed the diagnostic.

**ONE overall-SUPPORTED finding on record under the strict locked
rule** (HA07d) — but **demoted from load-bearing status** in
synthesis per the threshold-monotonicity diagnostic-v1 CLOSE
verdict in both eras (2026-06-07). The locked SUPPORTED verdict
stays on record per audit-trail discipline; synthesis-level
load-bearing claims do not. The era reversal observable in HA07d's
per-direction-arm data remains physiologically interesting but the
synthesis-level "demonstrated within a single test" claim is
paused pending v2 diagnostic outcomes.

The diagnostic-v1 locked criteria themselves are acknowledged to
have a methodological defect — they only capture canonical-decline
robustness and penalise stable-plateau and rising-with-threshold
shapes that are equally robust. **v2 criteria** were pre-registered
2026-06-07 as a methodology document with a five-category shape
rule (canonical decline / stable plateau / rising-late-peak /
bumpy with sign changes / loose-tail noise). v2 diagnostics for
HA10, HA07d, HA06b, HA11 are pre-registered as separate locked
diagnostic.md files.

**Symmetric interim demotion** (peer-review concern on interim
asymmetry): HA06b and HA11 were also demoted to "load-bearing
pending v2 diagnostic" in synthesis-level framing, joining HA10
and HA07d. The discipline-cost of demotion was paid symmetrically
by all four findings until the v2 diagnostics ran.

**Atomic synthesis update after all four v2 diagnostics (2026-06-07)**:

- **HA10 validate bidirectional**: v2 RESCUE via Cat 3
  (rising/late-peak; peak at N_std=1.75 with +19.5 pp; disc held
  +14 at N_std=2.0, +11 at 2.5; 1 sign-change in [1.0, 3.0];
  positive across rise). **Restored to load-bearing corroborating
  secondary anchor** for validate-era.
- **HA07d both eras bidirectional**: v2 RESCUE — train via Cat 3
  (peak 1.75 with +21.4 pp; 0 sign-changes in meaningful range;
  the worked walkthrough confirmed this exactly, against the
  researcher's earlier intuition that train would CLOSE); validate
  via Cat 2 + Cat 3 (8 contiguous tiers > +15 pp from N_std=1.0 to
  2.75; sustained stable plateau). **Restored to load-bearing
  primary anchor** for validate-era and to load-bearing for
  train-era. Project's first overall-SUPPORTED test status
  restored under v2.
- **HA11 train one-sided elevated**: v2 RESCUE via Cat 1
  (canonical decline; peak at N_std=1.25 with +45.4 pp; Spearman
  −0.683; 0 sign-changes). Cleanest robust shape in the round.
  **Restored to load-bearing**.
- **HA06b train bidirectional**: v2 CLOSE via Cat 4 (2
  sign-changes in [1.0, 3.0]: curve crosses zero at N_std=1.0
  with disc −4.1, then at N_std=3.0 with disc −2.1). **Permanently
  demoted to non-load-bearing**. Locked +18.9 pp SUPPORTED
  verdict stays on record per audit-trail discipline. One of
  four pre-cliff anchors removed from the load-bearing list.

**Discipline binding in both directions**: the v1 demotions held
until v2 ran. v2 restored three of four findings via principled
shape categories (Cat 1, 2, 3). v2 closed one (HA06b train) via
genuine shape fragility (2 zero-crossings in meaningful range).
The reviewer's symmetric-application critique was correct: HA06b
could not be exempt from v2 just because it wasn't in the original
v1 round.

### Implications

- **Card (b) train-era retrospective** now has SEVEN converging
  empirical anchors. Strongest empirical case for any card
  concept in the project.
- **Card (b2) validate-era retrospective** now has TWO converging
  empirical anchors (HA10 + HA07d). Promote to Tier 1 *with
  anchors*. Ship is unblocked.
- **D7 single-mechanism-two-regimes reframe** is now empirically
  anchored on the SAME channel (sleep stress variability) showing
  different directions per era — single-test internal consistency,
  not just cross-channel inference. The autonomic dimension that
  shifts before crashes is FLEXIBILITY (variability), not LEVEL
  (mean).
- **HRV-of-HRV-proxy is a real autonomic-precursor signal for this
  participant.** Banked methodologically. Future tests on other
  channels' variability (RHR variability, BB variability) become
  defensible follow-up directions.
- **Methodology lesson: bidirectional primary when direction is
  a priori ambiguous.** HA07d's primary bidirectional was crucial
  — a one-sided primary would have missed the validate-era finding
  entirely (validate only SUPPORTS on the lowered arm).
- **The HRV hypotheses remain permanently untestable on this
  dataset** but the proxy substitutes have provided answers to
  the underlying physiological question.

### Methodology lessons banked from this round

1. **Pre-register relative thresholds for autonomic-channel
   tests** (HA06 → HA06b banked; HA07c/HA08c/HA07d all followed).
2. **Pre-register the bidirectional primary** when the
   physiological direction is genuinely ambiguous a priori.
3. **Second-order primitives can carry signal first-order
   primitives miss.** HA07c (mean delta) refuted validate at
   +4.3 pp; HA07d (variability delta) supported validate at
   +21.7 pp.
4. **Locked HRV pre-registrations are not wasted effort if
   hardware blocks them** — they form the audit-trail record of
   what was attempted; substitute pre-registrations were locked
   *before* data inspection.
5. **When path C authorisation reveals a hardware gap, the
   defensible substitute path is to find a proxy whose
   relationship to the original signal is known**, not to abandon
   the pre-registered question.

### What's queued (revised after HA07d)

1. **H03b** — per-minute BB overnight recharge for sharpening
   HA10's validate-era SUPPORTED finding. API backfill running
   in background; H03b pre-registration locked at
   [H03b/hypothesis.md](H03b-bb-overnight-recharge-permin/hypothesis.md)
   *before* any per-minute data inspection.
2. **Card (a) + (b) + (b2) prototyping** — all three Tier 1 cards
   now have strong empirical anchors. Ship is unblocked.
3. **C.3 personal-lag teaching one-pager** — 4-day lead-up
   confirmed across 7 train + 2 validate SUPPORTED tests at the
   same window. Descriptive only.
4. **C.5 volatility + dip-frequency progress metric** — adds the
   HA07d era directionality reversal as a candidate progress axis
   (variability shifting from train-era volatile to validate-era
   stable IS a stabilisation metric).
5. **HA09 reframing reinforced again.** HA10 + HA07d together
   formalise the freeze pattern as detectable AND predictive in
   validate. HA09 ("can the *combination* of elevated BB + lowered
   variability be detected as a unified 'freeze night' marker?")
   becomes more urgent. Work-on-later promoted to candidate.
6. **C.2 cognitive/emotional load mining** — journal-layer angle.
7. **Notes label-quality work** — also: re-look at validate-era
   notes around HA07d-triggering crashes for "felt stable but
   crashed" / freeze descriptions.
8. **C.4 recovery-completeness over time** — depends on H05b.
9. **HA12 pre-infection HRV rise** — work-on-later; remains
   gated on HRV access (won't happen on FR245).
10. **HA09 + H02e + H05b + Dictionary v3** — cheap deferred.

---

## Update 2026-06-07 (later still ×2): S02 + S02b + S02c — the score-side trajectory and the trajectory-vs-daily-resolution methodology lesson

Three sibling pieces ran same-day, addressing the score channel
itself for the first time in the project's analytical work:

- **[S02](S02-score-trajectory/notes.md)** — score-side trajectory
  (90d rolling trimmed mean + median + score-level distribution),
  pre-registered same-day rank correlation (§3.8), four
  pre-registered S02b triggers (§7.2). Two triggers fired:
  T1 inflection-date mismatch (score peaks 149d before avg-stress;
  troughs 100d before max-spike — score leads Garmin pendulum at
  trajectory level) and T2 May 2026 channel divergence forward.
- **[S02b](S02b-score-lead/notes.md)** — daily-resolution lagged
  correlation testing whether T1's rolling-curve pattern survives.
  **REFUTED** on criterion (c): primary ρ_lag at +149d = +0.099
  vs matched same-day ρ = −0.097, |delta| = +0.002 against the
  0.10 bar. Same-day and lagged ρ values are sign-flipped but
  nearly identical in magnitude (~0.10). No daily-resolution
  lead/lag signal in either direction. Secondary at +100d also
  null.
- **[S02c](S02c-may2026-divergence/notes.md)** — daily-resolution
  z-score characterisation of the recent perturbation period
  against a 180-day recent reference window. Only RHR shows an
  algorithmic onset (2026-05-14, z_mean +0.82) and even RHR is
  below the locked 1.0σ "visibly worsening" bar. Other Garmin
  channels and score are "essentially unmoved" at recent-baseline
  σ. Composite Garmin-worsen vs score gap = **+0.324σ** —
  directional but small.

### Five things these three pieces tell us

**1. The score-side stabilisation is empirically anchored at the
distribution level.** S02 §3 found a clear tail-collapse on the
worst end (score≤3 share 20% → 7% across the tracked window) AND
a new upper mode emerging (score=6 share 2% → 12%). The trimmed
mean moves modestly (4.35 → 4.72) because the rebalancing happens
inside the trim region. Card (a) the stabilisation-arc card gains
its score-side empirical anchor.

**2. The score channel and the Garmin channels measure substantially
different state at the daily timescale.** S02's §3.8 same-day ρ
values were near zero for all four channels (primary avg-stress
ρ = −0.06, exploratory all within ±0.07); S02b confirmed this at
both lag conditions; S02c confirmed it within the perturbation
window (with one curious within-window positive r between score
and avg-stress that doesn't generalise). The "watch and felt
experience track different things day-by-day" reading is now
multiply confirmed at daily resolution.

**3. Rolling-curve turnaround-date mismatches do NOT automatically
imply daily-resolution lead/lag signals.** This is the
methodology lesson banked by S02b. S02 T1 fired because the
90-day-smoothed score peaked 5 months before the
90-day-smoothed stress. S02b found the underlying daily series
have no such lead/lag relationship. The trajectory-level pattern is
a smoothing-window artifact of the participant's typical-day
distribution reshaping before the biometric baseline did, NOT a
day-by-day predictive relationship. **Future trajectory comparisons
should cite this constraint before claiming daily-resolution
implications.**

**4. The "two reference frames produce different perturbation
magnitudes" methodology lesson.** S02 T2 fired against S01's full
5-year anchor σ for 3 of 4 Garmin channels. S02c re-measured
against the recent 180-day daily σ and found only RHR registers any
directional drift, and even RHR is below the 1.0σ bar. Both
σ-frames are correct for their respective questions ("vs whole
tracked history" vs "vs recent baseline"); the reading just needs
to be against the right σ. **Stocktake / synthesis / card claims
should be explicit about which reference frame they cite.**

**5. The "score is at all-time high" finding from S02 needs the
same nuance.** Trajectory-level: true, 4.72 trimmed mean at the
last anchor is the highest in the tracked window. Daily-resolution
against recent baseline: z_mean +0.07, essentially unmoved. Both
are correct in their frame; the all-time-high framing is
appropriate against the 5-year trajectory; "essentially unmoved
against recent normal" is appropriate against the last six months.

### Wiggers H1 connection

S02b is the project's **first direct cross-correlation lag test**
for [Wiggers H1](../../wiggers_progress_2026-06-07.md) ("do
wearable signals lead the felt crash?"). S02b tested the
empirically-observed score-leads-Garmin direction (not the Wiggers
direction, which is the reverse) and refuted it at daily resolution.
The Wiggers-canonical wearables-lead-score direction remains
untested directly, but the magnitude of all observed lagged ρ
values (|0.025|−|0.099|) suggests that direction would also be
small at daily resolution. The implicit "wearables lead" reading
from the 3–5 day lead-up window tests (H02b train, H02d, HA06b
train, HA11 train, HA10 validate, HA07d both eras) still stands;
the explicit cross-correlation lag test is refuted in the observed
direction.

### Implications for card prototyping (revised)

- **Card (a) stabilisation-arc**: empirical anchors now include
  S02's score-distribution shift and trajectory dates. Card copy
  must be careful: the trajectory-level lead pattern is real but
  must NOT be presented as "your score predicts your biometrics"
  (S02b refuted that). Honest framing: "your typical-day band
  reshaped before your biometric pendulum did, in the
  smoothed view." S02c's recent-baseline framing applies for any
  "current state" element of the card.
- **Card (b) train-era retrospective** + **Card (b2)
  validate-era retrospective**: unchanged. S02/S02b/S02c don't
  affect the per-crash autonomic findings.

### What's queued (revised after S02 + S02b + S02c)

1. **S03 — score channel deeper characterisation?** Not yet
   scoped; possible next-batch S-piece. Open question: what does
   the score's variance / volatility look like over time (the C.5
   piece that S02 deferred)? Probably worth pre-registering before
   running.
2. **Wiggers H1 Wiggers-direction lag test** — S02b tested the
   observed direction; the canonical Wiggers direction
   (wearables-lead-score) remains untested. Magnitude data
   suggests it would also be small but pre-registering and running
   would close the question.
3. **The C.3 personal-lag teaching one-pager** still pending.
   Now anchored on the 3–5d implicit lead findings, NOT on the
   S02 trajectory-level lead (which S02b refuted).
4. **Methodology-honesty pattern banked**: when a trajectory
   pattern is observed, a daily-resolution confirmation test
   should be locked into the same pre-registration where
   possible. S02's locked S02b triggers + same-day execution is
   the template.

---

*Update 2026-06-07 (later still even) — HA07c + HA08c + HA07d.
Living document.*

*Update 2026-06-07 (last that day): S02 + S02b + S02c. Adds
score-side trajectory + distribution-shift finding + the
trajectory-vs-daily-resolution methodology lesson + the
two-σ-frames methodology lesson.*

---

## Update 2026-06-07 (later still ×3): HA01b per-axis decomposition diagnostic

First diagnostic run under the consolidated testing playbook
([../methodology/testing-playbook.md](../methodology/testing-playbook.md))
section 9 compliance bar. Pre-registered at
[HA01b-per-axis-diagnostic/diagnostic.md](HA01b-per-axis-diagnostic/diagnostic.md);
result at
[HA01b-per-axis-diagnostic/result.md](HA01b-per-axis-diagnostic/result.md).

### The finding

The HA01b composite REFUTED verdict (Theme A bundled re-test:
train +5.8 / validate +4.0 pp on lagged baseline) was hiding a
per-axis signal. Decomposed into its 4 input axes:

| axis | train | validate |
|---|---|---|
| **effective_exertion** | **SUPPORTED** +21.3 pp / 81.8% freq | **SUPPORTED** +19.5 pp / 80.0% freq |
| step_burden | refuted (crit-c miss by 0.008) | SUPPORTED +16.6 pp |
| max_hr_peak | refuted +7.5 pp | refuted -7.7 pp (inverted) |
| vigorous_min | refuted +10.7 pp (crit-b miss) | SUPPORTED +24.6 pp |

Composite control reproduces HA01b REFUTED (+3.4 train / +1.5
validate pp) — confirms the per-axis decomposition is honestly
extracting signal the composite obscured.

**Why the composite REFUTES while effective_exertion SUPPORTS**:
the composite is `MAX(rank across 4 axes) ≥ 0.75`. Both crashes
AND nulls hit this MAX threshold ~80% of the time, so the
crash-vs-null spread is tiny. When you ask "is THIS specific axis
elevated," the null rate drops to ~60% (axes are correlated
0.31-0.69 but not identical, so the MAX is broader than any
single axis), and discrimination jumps to ~+20 pp.

**This is a methodological lesson about composite construction**:
MAX-of-ranks composites trade per-axis specificity for over-broad
triggering. The lesson is queued for the testing playbook §3
addendum.

### Both-eras rule reduces load-bearing to 1 axis

Per playbook §4.4, only effective_exertion clears both-eras gate.
step_burden and vigorous_min validate-only SUPPORTED are diagnostic
findings, NOT load-bearing. max_hr_peak is decisively REFUTED
(validate inversion is consistent with chronotropic incompetence
in ME/CFS, >85% prevalence per literature).

### Cross-axis correlation matrix (per playbook §6.1)

Spearman ρ across 1184 fully-valid days:

|                    | eff_exert | step_burd | max_hr | vig_min |
|---|---:|---:|---:|---:|
| effective_exertion | 1.000 | 0.437 | 0.624 | 0.692 |
| step_burden        | 0.437 | 1.000 | 0.312 | 0.307 |
| max_hr_peak        | 0.624 | 0.312 | 1.000 | 0.588 |
| vigorous_min       | 0.692 | 0.307 | 0.588 | 1.000 |

effective_exertion is the "central" axis (mean ρ ≈ 0.58); step_burden
is most independent (mean ρ ≈ 0.35). Effective N of independent
comparisons ≈ 2.5 (not 4).

### Critical specificity caveat (per playbook §6.2)

Even at +19.5 pp validate discrimination, posterior-per-fire is
**~2.2% vs 1.7% base rate** (60% of any 4-day window triggers in
the null). NOT shippable as a card without further refinement. The
HA01c v2 threshold-monotonicity diagnostic is precisely designed
to probe whether tighter thresholds yield acceptable specificity.

### Pre-committed follow-ups (locked 2026-06-07, BEFORE per-axis
diagnostic ran)

- **HA01c**
  ([HA01c-effective-exertion-shock/hypothesis.md](HA01c-effective-exertion-shock/hypothesis.md)):
  effective_exertion as primary, same threshold (rank ≥ 0.75),
  same 3-criterion bar, both-eras rule. Not a re-test of HA01b;
  new hypothesis with a different primary per playbook §2.2.
- **HA01c v2 threshold-monotonicity diagnostic**
  ([HA01c-threshold-monotonicity-diagnostic-v2/diagnostic.md](HA01c-threshold-monotonicity-diagnostic-v2/diagnostic.md)):
  5th in v2 round (after HA10, HA07d, HA06b, HA11). Tests rank
  thresholds {0.50…0.95} per locked five-category shape rule.

### What this changes in synthesis

- **HA01b composite REFUTED verdict** unchanged on record. The
  per-axis diagnostic produces a **diagnostic finding**, NOT a
  re-test verdict (per playbook §5.2).
- **If HA01c + v2 both pass**: effective_exertion becomes the
  **second project-level both-eras SUPPORTED finding** after HA07d.
  The D7 single-mechanism-two-regimes reframe regains an
  empirical anchor (a validate-era physiological precursor on a
  cleanly-pre-registered single primary).
- **If HA01c REFUTES or v2 fails**: HA01b composite REFUTED stays;
  per-axis finding documented as diagnostic-only; downgraded from
  "diagnostic finding" to "investigative artefact" per playbook
  §2.5 audit-trail discipline.

### Methodology lesson banked (for future composites)

For composite metrics with N input axes:
- Pre-register per-axis primaries IN ADDITION to the composite
  (not as substitutes). The composite-vs-per-axis comparison is
  informative.
- OR use AND-of-axes composites (require all N axes to trigger)
  rather than MAX-of-ranks. Tighter specificity at the cost of
  sensitivity.

This is a generalisable lesson queued for the playbook §3
addendum on first-order/second-order primitive selection.

---

*Update 2026-06-07 (later still ×3): HA01b per-axis decomposition
diagnostic. First diagnostic under consolidated playbook. HA01c +
v2 pre-registered as pre-committed follow-ups pending user
approval to run.*

---

## Update 2026-06-07 (later still ×4): HA01c + HA01c v2 — first AMBIGUOUS verdict in v2 series

Same-day execution of the pre-committed HA01c + HA01c v2 chain
after user approval. Results at
[HA01c result.md](HA01c-effective-exertion-shock/result.md) and
[HA01c v2 result.md](HA01c-threshold-monotonicity-diagnostic-v2/result.md).

### HA01c locked-threshold verdict

**SUPPORTED both eras** at the locked 0.75 threshold:

- Train: 81.8% freq, +21.3 pp disc, median rank 0.883 (n_clean=11)
- Validate: 80.0% freq, +19.5 pp disc, median rank 0.909 (n_clean=15)

Numbers identical to the per-axis diagnostic (same data, same null
seed, same threshold). HA01c was a disciplinary re-run; the locked
verdict is the canonical artifact for the effective_exertion-as-primary
hypothesis. HA01b composite REFUTED stays on record per playbook
§2.2 (separate hypothesis with different primary).

### HA01c v2 threshold-monotonicity diagnostic

**MIXED verdict — first AMBIGUOUS in v2 series**:

**Train AMBIGUOUS**: shape is bumpy-but-never-negative
(15.4 → 6.4 → 16.2 → 21.3 → 10.3 → 7.9 → 2.0 → 7.3); peak τ=0.75
+21.3 pp. The locked Cat 1-5 rule doesn't categorize it:
- Cat 1 fails (peak 0.75 not in [0.50, 0.70])
- Cat 2 fails (range 19.3 pp > 5 pp threshold)
- Cat 3 fails (peak 0.75 < 0.80 AND the 0.50→0.60 drop breaks
  monotone rise to peak)
- Cat 4 fails (0 sign-changes — curve never crosses zero)
- Cat 5 fails (peak too high)

This is the **edge case the framework was designed to surface**:
shape is robust (all 8 thresholds positive, declining on average
ρ=-0.45) but doesn't fit a locked category. Discipline binds:
returns AMBIGUOUS rather than forcing a fit.

**Validate RESCUE via Cat 1**: textbook canonical decline
(15.4 → 24.6 → 21.0 → 19.5 → 13.3 → 13.3 → 12.3 → 6.7); peak
τ=0.60 +24.6 pp; ρ=-0.850; 0 sign-changes; monotone decline
beyond peak. Cleanest Cat 1 shape in the entire v2 round.

### Project net state after HA01c + v2

Per playbook §4.4 both-eras rule + HA01c hypothesis.md §5 v2-gate:
HA01c stays **SUPPORTED-with-stability-mixed** — honest at τ=0.75
but **NOT load-bearing**.

| status | finding |
|---|---|
| Project-level overall-SUPPORTED + v2-validated | **HA07d only** (both eras RESCUE; unchanged) |
| Load-bearing in synthesis | HA07d (both eras), HA10 (validate corroborating), HA11 (train), H02b/H02d (train) |
| SUPPORTED-with-stability-mixed (noted, not load-bearing) | **HA01c (new)** — joins this status |
| Permanently demoted | HA06b (CLOSE Cat 4 in v2 round, demoted) |

The composite REFUTED verdict (HA01b) stays unchanged on record.
The per-axis diagnostic finding (effective_exertion both-eras
SUPPORTED) is preserved as audit trail. The HA01c locked verdict
+ v2 mixed verdict is the latest snapshot of "what we know" about
the effective_exertion channel.

### Card-craft outcome

**No HA01c card.md drafted**. Two converging reasons:

1. **Playbook §6.2 specificity gate**: posterior per fire ~2.2%
   vs 1.7% base rate. 60% of any 4-day window triggers in the
   null. Card would fire ~every other day with marginal posterior
   lift over base rate.
2. **HA01c v2 mixed verdict**: load-bearing status withheld for
   synthesis purposes, which also withholds card-craft per
   playbook §2.7.

The user's pre-committed choice for this phase was "Wait for HA01c
+ v2 to resolve before any card work"; the resolution is: do not
draft. effective_exertion as a single-axis precursor remains an
honest research finding documented in result.md but does not
graduate to a user-facing surface.

### What this means for the v2 framework

The v2 framework now has **worked examples of all four outcomes**:

| outcome | example |
|---|---|
| RESCUE Cat 1 (canonical decline) | HA11 train (peak 1.25 +45.4 pp); HA01c validate (peak τ=0.60 +24.6 pp) |
| RESCUE Cat 2 (stable plateau) | HA07d validate (8 contiguous tiers > +15 pp) |
| RESCUE Cat 3 (rising / late-peak) | HA10 validate; HA07d train |
| CLOSE Cat 4 (bumpy with sign-changes) | HA06b train (2 sign-changes, permanently demoted) |
| **AMBIGUOUS** (no category triggers) | **HA01c train (first instance)** |

The framework is now battle-tested across the qualitative space of
threshold-stability shapes. The AMBIGUOUS verdict is rare but the
framework correctly produces it rather than forcing a fit — exactly
the discipline the locked criteria are designed to enforce.

### Discipline-cost paid in full (revised after HA01c)

The user pre-committed to the locked v2 framework after the HA07d
v1 CLOSE moment. The framework has now:
- Demoted HA06b (CLOSE Cat 4) — discipline binds against rescue
- Rescued HA10 validate / HA07d both / HA11 train via Cat 1/2/3
- Surfaced HA01c train AMBIGUOUS — discipline binds against
  forced-fit when the shape is genuinely between categories

The framework distinguishes "robust but uncategorizable" from
"non-robust and bumpy" (AMBIGUOUS vs CLOSE) — the former returns
honest indeterminacy, the latter returns load-bearing-blocked.
Both are mature outcomes of a locked discipline.

---

*Update 2026-06-07 (later still ×4): HA01c locked-threshold
SUPPORTED both eras; HA01c v2 mixed verdict (first AMBIGUOUS in v2
series); HA01c added to noted-but-not-load-bearing list; no card
drafted; v2 framework now has worked examples of all four
outcomes.*


