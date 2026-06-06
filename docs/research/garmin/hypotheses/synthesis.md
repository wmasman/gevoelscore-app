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


