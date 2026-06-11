# What one person's four-year Garmin record says back to Wiggers' smartwatch-pacing guide

*A response from one Long COVID dataset to the Wiggers handleiding.*

*Draft 2026-06-08.*

---

## Why this article exists

Laure Wiggers' *Watch Smart Pacing* handleiding is a generous document. It
is what one chronically-ill person learned about her own body by reading
a Garmin watch for years, distilled into observations she hopes are
useful to other patients. She is explicit that these are *lotgenoten*
observations, not medical claims, and that everyone has to learn what is
normal for themselves.

I sat with her guide for several weeks because I have something close to
what she has: a Garmin Forerunner 245 worn nearly continuously since 2021,
a one-tap "gevoelscore" (feeling-score) daily log started in
September 2022, and a Long COVID trajectory that has settled across the
last few years. I wanted to know what her observations look like in one
other person's data.

This article is the answer. It introduces the dataset, walks through
Wiggers' own six priority hypotheses one by one, and tries to be honest
about three different things at once: what the data confirms, what it
refuses to confirm, and what the data cannot say. I lead with one finding
that disciplines almost everything else: when I formally measured how
*independent* the different Garmin channels actually are, several of them
turned out to be the same signal seen twice.

There is a technical appendix at the end (Fisher's exact p-values, cross-
channel correlations, the full verdict ledger). The main body is meant to
be readable on its own.

---

## The dataset

| element | detail |
|---|---|
| participant | one person (me), Long COVID since 2022 |
| watch | Garmin Forerunner 245, worn nearly continuously since 2021-08-16 |
| feeling-score | one-tap gevoelscore 1–6 daily, started 2022-09-03 |
| analysis window | 2022-09-03 → 2026-06-05 (~1.370 days) |
| Garmin metrics used | resting HR, sleep stress (mean + variability), morning body-battery peak, per-minute stress samples, step + intensity-minute composites |
| crash labels (`crash_v1`) | gevoelscore ≤ 3 for ≥ 2 consecutive days, merged within 3 days. 29 episodes total |
| train / validate split | 2023-12-31 — pragmatic split that gives each era ~14–15 crashes for power |
| split rationale | the second half of 2023 was a turnaround point in the participant's stabilisation; not a "cliff," more like a pendulum settling |

A few honest framings up front, because Wiggers asks for them:

- **"Stabilisation," not "recovery."** Recovery implies returning to a
  prior state. What actually happened was a gradual settling: crash
  frequency dropped from roughly 10/year (2022–23) to roughly 2/year
  (2024–25), with a recent perturbation in May 2026.
- **`crash_v1` is one-dimensional.** A crash here is "feeling-score ≤ 3
  for 2+ days." That bucket mixes ME-style PEM, infection-driven low
  weeks, migraine clusters, and the occasional emotional rough patch.
  Several of Wiggers' hypotheses (H3 in particular) are *about*
  separating those mechanisms. I have not yet built a mechanism-aware
  label, so any claim about "the kind of crash this signal belongs to"
  is downstream.
- **Pre-registered tests, not exploratory mining.** Every hypothesis
  below was locked before its test ran: the metric, the threshold, the
  lead-up window, the direction, and a three-criterion bar (frequency
  + discrimination + magnitude). When something missed, I left it
  missed. The investigation has ~30 such pre-registered hypotheses
  closed so far.
- **A train/validate rule.** A finding only counts as load-bearing if it
  holds in both eras. A train-only or validate-only result is a
  *diagnostic* finding, not a load-bearing one. Wiggers' observations
  were made before her recovery shifted ground under her; mine had
  about the same problem, and the both-eras rule was the cheapest way
  to discipline it.

---

## The reading note that disciplines everything below

Before walking through Wiggers' six priority hypotheses, one finding I
only fully measured on 2026-06-08, and which changes how to read every
"channel converges" claim in the rest of the article:

**Several of my Garmin "channels" are not statistically independent.**
On a calendar-day level, across roughly 1.340 valid days:

- **Daily maximum stress-spike duration and a "bridged-spike" variant
  (H02b and H02d) are the same primitive** (Spearman ρ = +1.000;
  Pearson r = +1.000). They differ in window-length and validity
  rules, not in what the watch saw.
- **Morning body-battery peak and overnight sleep-stress mean
  (HA10 and HA07c) are essentially the same signal in opposite signs**
  (Spearman ρ = −0.922; Pearson r = −0.863). This is structural in
  Garmin's body-battery algorithm — BB goes down when stress goes up.
- **Sleep-stress mean and sleep-stress variability (HA07c and HA07d)
  are moderately collinear** (Spearman ρ = +0.501) — related but
  capturing distinct facets (level vs spread).
- Resting HR is moderately tied to both: HA06b ↔ HA07c = +0.377;
  HA06b ↔ HA10 = −0.393. Higher resting HR with poorer overnight
  recovery is one underlying pathway.

What this means for the article: where I had been informally writing
"three channels converge on the parasympathetic-swing pattern," the
honest reading is closer to **one autonomic-state signal seen through
several views, plus a partly-related variability channel**. The
*direction* of the finding is preserved; the *count of independent
corroborations* is not what the channel count suggested.

This is also the lens for the statistical results I quote. Of 11 primary
pre-registered verdicts, two clear conventional one-sided significance
(Fisher's exact, α = 0.05): **H02b train (p = 0.029)** and **H02d
train (p = 0.011)** — and those two are the same primitive. **None
clears a Bonferroni correction at the naive α = 0.05/11 ≈ 0.005.** Under
the more honest effective-N correction (~3–4 independent clusters,
α ≈ 0.0125), still only the within-day stress-spike cluster survives, and
only in the train era. The bar I pre-registered (≥ 60% recall, ≥ 15 pp
discrimination, median magnitude) is more permissive than conventional
α = 0.05. That was a deliberate choice for n-of-1 exploratory work,
but it costs the right to phrase findings as "significant."

With that on the table, the six Wiggers hypotheses one by one.

---

## H1 — do the wearable signals lead the felt crash?

This is Wiggers' single most product-decisive question. If the watch
warns me 24–48 hours before my own felt score drops, the watch earns
its place. If it doesn't, my one-tap score is already the better
instrument.

**What I tested.** Every pre-registered precursor test in this project
uses a 3- or 4- or 5-day *lead-up* window into a labelled crash day.
When several of those windows trigger more often before a crash than in
a matched non-crash baseline, that *implies* the wearable can lead the
felt event. Several do: train-era stress-spike (H02b train, +29.9 pp
discrimination over null), validate-era morning body-battery peak
(HA10 validate, +16.2 pp), sleep-stress variability (HA07d both eras,
+19.6 / +21.7 pp). So at the level of *windowed* discrimination, the
watch does carry information that the felt score hasn't yet expressed.

**What surprised me.** When I built the first *direct* daily-resolution
lag test (S02b) — taking the smoothed score series and the smoothed
average-stress series, asking whether one leads the other at any
specific lag — it **refused to confirm a daily-resolution lead at all**.
The peak lagged Spearman ρ (at +149 days, an artifact of trajectory
turnaround dates not matching) was +0.099; the same-day matched ρ was
−0.097; the difference was 0.002 against a 0.10 bar. Locked verdict:
refuted on criterion (c).

**Reading.** The discrimination on 3–5 day lead-up windows is real. The
implied lead-time is in the 3–5 day region. But the *daily*-resolution
cross-correlation does not pull a clean lead-vs-lag out of the smoothed
series, in either direction. The trajectory-level pattern that *looked*
like the score had a 5-month head-start on average stress (the S02
finding) did not survive the daily check (the S02b finding). That is a
methodology lesson I now carry: a rolling-curve turnaround date is not
the same kind of evidence as a daily lead/lag correlation.

**What this means for Wiggers' H1.** Partially confirmed and partially
not. The wearable does add information beyond same-day felt-score in
the 3–5 day window before a crash. It does not add a clean daily-
resolution lead that I can build a single-number "you will crash on
Friday" signal on. The one direction I haven't tested directly is the
canonical Wiggers direction — "the wearable leads the score" — at daily
resolution; the magnitude data suggests it would also be small but the
test remains on the queue.

---

## H2 — how many crashes are activity-invisible?

Wiggers' framing: if a sizable fraction of crashes happen without any
physical signal — no step elevation, no HR spike, just a mental or
emotional load that the wrist cannot see — then a wrist-only product
will always miss a category of events, and the calendar / journal
becomes a first-class input.

**What I tested.** Several activity-exertion pre-registrations
(HA01 / HA01b / HA01b-recomputed) using a composite of steps, intensity
minutes, max HR, and vigorous minutes all came back **refuted** as
crash precursors — meaning a generic "you did too much" composite did
not flag the bulk of validate-era crashes. That is consistent with
Wiggers' claim that many crashes are activity-invisible.

A per-axis decomposition (HA01b-per-axis-diagnostic, 2026-06-07) then
pulled the composite apart to see whether any individual exertion axis
was hiding inside it. **"Effective exertion"** — Garmin's intensity-
minutes plus recorded activity duration — was the only axis to clear
the both-eras gate (+21.3 pp train, +19.5 pp validate). A follow-up
pre-registration (HA01c) confirmed +21.3 / +19.5 pp at a locked rank
threshold of 0.75. Wiggers' own E3 hypothesis — that intensity-minutes
track exertion better than raw steps — landed.

**What surprised me.** Even with effective_exertion showing the
strongest single-axis discrimination, the *specificity* test failed.
On a base rate of ~1.7% crash-days, the channel fires in ~60% of any
matched 4-day window of non-crash days, yielding a posterior-per-fire
of ~2.2%. That is a real but tiny lift over base rate, and at a fire-
rate that would generate ~one alert every two days. As an "are you
overdoing it" diagnostic for a trained eye, it carries information. As
a card I could surface to a tired user, it would mostly cry wolf.

**Reading.** A fraction of crashes do leave an effective-exertion
signature. The fraction is large enough to discriminate crash from null
windows in both eras (positive evidence for Wiggers' E3, partial
evidence against a strong reading of H2). The fraction is *not* large
enough, and the per-fire posterior is *not* high enough, to build a
single-trigger "you did too much" alert. A formal per-crash count of
"physical signature present vs absent" — which is what Wiggers' H2
literally asks for — I have not yet done.

**What this means for Wiggers' H2.** Implicitly supported by the
HA01b composite refutation. Sharpened but unresolved by HA01c. Not yet
directly counted.

---

## H3 — do acute-illness crashes and PEM crashes have different signatures?

This is the one Wiggers product-decisive hypothesis I have not addressed
at all.

A crash by my current label (`crash_v1`) is a multi-day low-score
stretch. It does not distinguish a viral infection from a post-
exertional malaise from a migraine cluster from a depressive episode.
Each plausibly has a different Garmin signature — sustained RHR +
temperature for infection, HRV-led for PEM, autonomic-quiet for
migraine — and lumping them together dilutes any one of those
signatures to nothing.

I have notes language work in flight that may eventually let me split
crashes by mechanism (notes-keyword profiles already show that
late-era crashes contain more cognitive-load language and more severe-
symptom language than early-era crashes). That work is what unlocks H3
as a directly-testable hypothesis. Until it lands, H3 stays where
Wiggers parked it: a separation question that requires labels I do not
yet have.

**Reading.** Untested. Acknowledged as the largest mechanism-separation
move available, gated on notes-quality work.

---

## C3 / D1 / D2 — non-linearity of stress, body-battery level vs dynamics

Three of Wiggers' hypotheses sit close together: **C3** (the
stress→fatigue relationship is non-linear / convex — a 30→40 step on
the stress scale costs far more than it looks), **D1** (the absolute
body-battery level is a weak indicator of how the user feels), and
**D2** (body-battery *dynamics* — overnight gain, daytime slope —
predict the felt score better than the level).

**What I tested.**

- **C3.** Not directly. I added a same-day Spearman ρ between
  feeling-score and average daily stress as part of the score-
  trajectory work (S02 §3.8); it returned ρ = −0.056 [−0.164, +0.009],
  which is ambiguous and underpowered. That tests a *monotone*
  relationship, not curvature. The non-linearity question Wiggers
  raises remains untested.
- **D1.** Partially. The body-battery net delta (overnight gain minus
  daytime loss) was pre-registered as a crash precursor (H04). It came
  back refuted in both eras with one slight inversion. I have not
  directly correlated *level* against *felt score*.
- **D2.** This is where the most painful surprise of the project sits.
  I locked a per-minute body-battery overnight-recharge integral test
  (H03b) on 2026-06-07. When the test ran, it returned **INCONCLUSIVE
  across all 12 evaluation cells.** The reason: the Garmin Connect API
  only populates the per-3-minute `sleepBodyBattery` array from
  approximately 2024-06-03 onwards. Train era (14 crashes) has zero
  coverage; validate era (15 crashes) has six. The locked threshold of
  "≥ 10 clean crashes per era" binds, and the test cannot decide. The
  *coarse* version of the BB-overnight-recharge question (HA10, using
  the three daily anchor points HIGHEST / LOWEST / MOSTRECENT) does
  carry a validate-era SUPPORTED finding. The *sharpened* per-minute
  version, which is the one Wiggers' D2 actually asks for, will not
  run until I either back-fill the API or decode the relevant per-
  minute byte field (`unknown_233`) from the local FIT files.

**Reading.** C3 untested at the curvature level; D1 partly addressed
(net delta refuted, level-vs-felt not directly tested); D2 is the
project's most concretely *blocked* hypothesis — pre-registered, run,
and inconclusive on data availability rather than on biology. The
broader honest reading is: Garmin's *daily aggregate* body-battery and
stress numbers, the ones a user actually sees on the watch face, do
not on their own carry the predictive signal that the pacing literature
suggests they might. Whether the per-minute curves do is an open
question that depends on a decoding job I have not finished.

---

## B4 / H4 — parasympathetic swing as an inverted indicator

This is Wiggers' most counter-intuitive prediction: a *sudden HRV
increase* is not good news but a *negative* leading indicator, because
the body is overshooting into a parasympathetic state after
overexertion and a felt crash follows in 24–48 hours. The
"freeze" or "swing" pattern shows up in her own grafieken as a high
body-battery night that doesn't correspond to feeling refreshed.

I cannot test this on HRV directly — the Forerunner 245 does not record
HRV status. I used three Garmin signals that each carry part of the
autonomic-swing pattern as proxies:

- **HA06b**: resting HR z-score deviation from a 90-day baseline, with
  a directionality split.
- **HA10**: morning body-battery peak (HIGHEST anchor) z-score, again
  with direction.
- **HA07d**: overnight sleep-stress variability (standard deviation
  across the sleep window).

**What I found.** All three carry the swing direction in the validate
era: 75% of triggering validate crashes had a *lowered* RHR vs
baseline (the post-exertion drop), 69% had an *elevated* morning BB
peak (the false-energy reading), and the sleep-stress variability
moves consistent with the same picture. HA07d cleared both eras (+19.6
pp train, +21.7 pp validate); HA10 cleared validate (+16.2 pp); HA06b
cleared train (+18.9 pp).

In the qualitative sense, this is the project's most striking
agreement with Wiggers. The "great-looking numbers precede a crash"
pattern she names is empirically present in this participant's data,
on more than one operationalisation.

**Where I have to soften.** Two ways.

First, statistically: at conventional α = 0.05, HA07d validate p =
0.070, HA10 validate p = 0.148, HA06b train p = 0.136. None clears
α = 0.05 one-sided Fisher's exact at this sample size. None clears the
honest effective-N Bonferroni at α ≈ 0.0125.

Second, structurally — and this is where the 2026-06-08 reading note
comes back. HA10 and HA07c (sleep-stress mean, the closest thing the
data has to "HRV-derived overnight stress") are nearly the same signal
in opposite signs (ρ = −0.922). HA07d (the variability of the same
sleep-stress signal) is moderately correlated with HA07c (+0.501).
What I had been informally calling "three independent channels
converging on the parasympathetic-swing pattern" is closer to **one
autonomic-state signal viewed through several lenses, plus a partially-
tied variability channel.**

So I cannot claim three independent corroborations. I *can* claim:
the autonomic-state signal moves in the direction Wiggers predicted in
this participant's validate era; the variability channel moves the same
way; the resting-HR channel moves in the same direction in train; and
all of that is consistent with her qualitative description even if I
have to retract the "three channels" headline. The threshold-stability
diagnostic round (v2) preserved HA07d as load-bearing and HA10 as
corroborating, after permanently demoting HA06b on a separate, stricter
shape check.

**Reading.** Wiggers' counter-intuitive direction is empirically present
in this dataset. The strength of the corroboration is one channel and
a half, not three. The direction matters more than the count for a
patient-facing message ("your watch may show you a great-looking night
when you actually need to rest"); the count matters more for any
formal claim about generalisation.

---

## G3 — barometric pressure × headache

Wiggers' single cheapest external-data hypothesis: low or falling
barometric pressure associates with headache days and with worse
feeling-scores. She herself notes that on days below ~980 mbar she
becomes "a wet dishcloth" and that a free pressure feed could turn a
known patient pattern into a measurable one.

**What I tested.** Nothing. G3 is an external-data join I have not
written. Barometric pressure is available from the watch itself (the
FR245 has an altimeter / barometer) and from any number of free weather
data sources. The headache tag is the single most-cited symptom in the
notes-language analysis (~78% of crash-day notes mention `hoofdpijn`).
This is one of the highest-yield, lowest-cost remaining items in
Wiggers' register, and it is untouched.

**Reading.** Not addressed. Queued as a near-term priority on the basis
of how cheap it is to attempt and how strong Wiggers' qualitative
description of the effect is.

---

## What this exercise actually shows

A working summary across the six priority hypotheses, with the
disciplinary cost paid up front:

| Wiggers ID | what one person's data says back |
|---|---|
| **H1** | The wearable carries information in the 3–5 day window before a crash. It does *not* show a clean daily-resolution lead in either direction at the smoothed-curve level. |
| **H2** | A generic activity-exertion composite does not flag most validate-era crashes, consistent with Wiggers' "activity-invisible" claim. The intensity-minutes axis (her E3) does carry signal but at a fire-rate too high to ship as a single-trigger alert. |
| **H3** | Untested. Requires mechanism-aware crash labels I have not built. |
| **C3 / D1 / D2** | C3 (non-linearity) untested. D1 (BB level as weak indicator) partly addressed; H04 BB-net-delta refuted in both eras. D2 (BB dynamics) BLOCKED by a Garmin API cutover — the per-minute array is only available from June 2024 onwards. |
| **B4 / H4** | The parasympathetic-swing *direction* is empirically present in validate-era. The "three independent channels converge" framing was overstated; it is one autonomic-state signal viewed several ways plus a partially-related variability channel. No verdict clears α = 0.05 once collinearity is honoured. |
| **G3** | Untested. Highest-cheap-yield item still on the queue. |

What jumps out for me, sitting with this:

- **Wiggers' qualitative observations look like one person's empirical
  patterns more often than they look like noise.** The
  parasympathetic-swing direction, the intensity-minutes vs raw-steps
  asymmetry, the "absolute BB level is not the dial" intuition, the
  data-quality warning about device-baseline lag — all of those landed
  in this dataset more or less the way she described them.
- **But the project's *quantitative* headlines were softer than I had
  been writing.** A bar built around 60% recall and 15 percentage
  points of discrimination over null is more permissive than
  conventional one-sided α = 0.05 at n = 14–15. Most of my "SUPPORTED"
  verdicts have Fisher's exact p between 0.05 and 0.15 and 95% CIs
  that span 30–40 percentage points. With effective-N Bonferroni in
  the picture, only the within-day stress-spike train signal survives.
- **The Garmin data has a hard ceiling for one of Wiggers' most
  interesting questions.** D2 (BB dynamics over BB level) is exactly
  the kind of question the watch ought to be able to answer, and the
  manufacturer's API quietly does not. Without local FIT decoding,
  this person's pre-2024 body-battery dynamics are not recoverable for
  research at per-minute resolution.
- **The biggest single thing the watch cannot see in this dataset is
  the calendar.** When I sort late-era crashes by what the *notes* say
  about the day before, "had a hard conversation," "deadline at work,"
  "saw the GP," and similar cognitive/emotional loads show up more
  often than any Garmin biomarker. Wiggers makes the same point in
  her own discussion ("een intens moment in een rustige dag"), and
  the part of her guide that I keep coming back to is the one where
  she says the watch is a forensic companion more than a forecaster.
  That matches my own reading of the data.

If you are using a Garmin to pace, the practical readings I would carry
from Wiggers' register and from this dataset are:

- Track *deviation from your own rolling baseline*, never raw numbers,
  exactly as Wiggers says.
- Treat a *high* morning body-battery after a known overexertion as
  potential false energy, not a green light. The data agrees with her
  on this.
- Watch intensity-minutes (Garmin's "intensieve minuten") rather than
  raw steps as a personal-overexertion dial.
- Do not expect a single channel to lead a felt crash by 24–48 hours
  in a clean way. The lead-time is real but distributed, and your
  felt-score is part of the instrument cluster, not downstream of it.
- Pay attention to days where your notes mention severe symptoms,
  cognitive load, or family/relational strain — those carry signal
  the watch does not.

The project is open. Wiggers' register has roughly forty testable
items; I have addressed maybe half of them. The half I have addressed
includes the autonomic / parasympathetic-swing material in some depth.
The half I have not includes the sleep material almost entirely (sleep
duration, sleep score, bedtime variance, deep-sleep deviation), the
external-data material (pressure × headache), and several of the
methodology robustness checks Wiggers explicitly calls out (device-
warm-up periods, level shifts across sensor changes).

I owe Wiggers and her *lotgenoten* a follow-up that closes the
barometric-pressure × headache question (G3), the sleep-dimension
register (F1–F4), and the mechanism-aware crash labels (H3). Those are
the next three items on this thread.

---

## Acknowledgements

Laure Wiggers wrote the handleiding this article responds to, and she
wrote it generously — without it, I would not have had a register
this organised to test against. Her own framing ("dit is een handleiding
van lotgenoten voor lotgenoten") is the spirit I have tried to keep.

The analytic discipline (pre-registration, train/validate split,
three-criterion bar, the v2 threshold-monotonicity diagnostic, the
2026-06-08 effective-N audit) was built up across the project in
collaboration with a research-honest reviewer agent over many sessions.
Mistakes that survived to this article are mine.

---

## Appendix A — Verdict ledger at a glance

The eleven primary pre-registered verdicts that the 2026-06-08
Fisher's exact + 95% CI audit covers:

| anchor | era | recall (95% CI) | null fire (95% CI) | disc pp (95% CI) | Fisher p (one-sided) | clears α=0.05? |
|---|---|---|---|---|---:|:-:|
| H02b (max-spike, 3d) | train | 71.4% (45–88) | 41.5% (35–48) | +29.9 (+5 to +55) | 0.029 | ✓ |
| H02d (bridge-spike × 5d) | train | 92.3% (69–99) | 60.5% (54–67) | +31.8 (+16 to +47) | 0.011 | ✓ |
| HA06b (RHR z, 4d bidir) | train | 71.4% (45–88) | 52.5% (46–59) | +18.9 (−6 to +44) | 0.136 | — |
| HA07c (sleep-stress mean, 4d) | train | 69.2% (45–88) | 46.0% (39–53) | +23.2 (−2 to +48) | 0.058 | — |
| HA07d (sleep-stress σ, 4d bidir) | train | 84.6% (60–96) | 65.0% (58–71) | +19.6 (−0 to +40) | 0.093 | — |
| HA08c (sleep-stress slope, 4d) | train | 61.5% (39–84) | 38.5% (32–45) | +23.0 (−3 to +49) | 0.054 | — |
| HA11 (U-dip count, 4d) | train | 64.3% (39–84) | 41.5% (35–48) | +22.8 (−3 to +49) | 0.084 | — |
| HA07d (sleep-stress σ, 4d bidir) | validate | 86.7% (62–96) | 65.0% (58–71) | +21.7 (+3 to +40) | 0.070 | — |
| HA10 (morning BB peak, 4d bidir) | validate | 86.7% (62–96) | 70.5% (64–76) | +16.2 (−2 to +35) | 0.148 | — |
| HA01c (effective_exertion, τ=0.75) | train | 81.8% (52–95) | 60.5% (54–67) | +21.3 (−3 to +45) | 0.136 | — |
| HA01c (effective_exertion, τ=0.75) | validate | 80.0% (55–93) | 60.5% (54–67) | +19.5 (−2 to +41) | 0.109 | — |

Two clear α = 0.05 one-sided. Zero clear naive Bonferroni at α = 0.005.
Once H02b/H02d are folded as the same primitive, only one cluster
survives an honest effective-N correction at α ≈ 0.0125.

---

## Appendix B — Cross-channel Spearman ρ matrix

Across 1.340 shared valid days in the analysis window:

| | H02b | H02d | HA11 | HA06b | HA07c | HA07d | HA10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **H02b** (max-spike min) | **1.00** | +1.00 | +0.38 | −0.01 | −0.04 | +0.05 | +0.05 |
| **H02d** (bridge-spike min) | +1.00 | **1.00** | +0.38 | −0.01 | −0.04 | +0.05 | +0.05 |
| **HA11** (U-dip count) | +0.38 | +0.38 | **1.00** | +0.05 | +0.05 | +0.07 | −0.08 |
| **HA06b** (resting HR) | −0.01 | −0.01 | +0.05 | **1.00** | +0.38 | +0.07 | −0.39 |
| **HA07c** (sleep-stress mean) | −0.04 | −0.04 | +0.05 | +0.38 | **1.00** | +0.50 | **−0.92** |
| **HA07d** (sleep-stress σ) | +0.05 | +0.05 | +0.07 | +0.07 | +0.50 | **1.00** | −0.37 |
| **HA10** (morning BB peak) | +0.05 | +0.05 | −0.08 | −0.39 | **−0.92** | −0.37 | **1.00** |

Key collinearities in bold: H02b ≡ H02d (1.00), HA10 ≡ −HA07c (−0.92).
Moderate collinearity: HA07c ↔ HA07d (+0.50), HA06b ↔ HA10 (−0.39),
HA06b ↔ HA07c (+0.38), H02b ↔ HA11 (+0.38).

Effective independent channel count: **≈ 3–4 clusters**:

- **Cluster 1**: within-day stress (H02b/H02d + HA11)
- **Cluster 2**: autonomic state (HA07c + HA10 ± HA06b)
- **Cluster 3**: autonomic variability (HA07d, partially tied to
  Cluster 2 via HA07c at +0.50)

---

## Appendix C — Wiggers register coverage

| section | covered | partial | not addressed | blocked / inconclusive-by-data |
|---|---:|---:|---:|---:|
| A. Resting HR & night HR | 3 | 0 | 0 | 1 (A4 intraday) |
| B. HRV | 2 (B1/B2 via proxy) + 1 (B4) | 0 | 1 (B3) | 1 (B5 illness labels) |
| C. Stress | 1 (C1 via proxy) | 1 (C4) | 2 (C2, C3) | 0 |
| D. Body battery | 1 (D5) | 2 (D1, D4) | 1 (D3) | 1 (D2 INCONCLUSIVE-BY-DATA) |
| E. Steps / activity | 1 (E3) | 1 (E2) | 1 (E1) | 0 |
| F. Sleep | 0 | 0 | 4 | 0 |
| G. Other sensors | 0 | 0 | 3 (G1, G2, G3) | 1 (G4 deprioritised by source) |
| H. Mechanism & lead/lag | 1 (H4) | 2 (H1, H2, H5) | 1 (H3) | 0 |
| I. Methodology checks | 0 | 1 (I3) | 2 (I1, I2) | 0 |

Roughly half the register addressed, with the sleep section and the
external-data section the largest remaining gaps. Full per-hypothesis
status: [wiggers_progress_2026-06-08.md](wiggers_progress_2026-06-08.md).

---

*Article drafted 2026-06-08. Companion to
[wiggers_progress_2026-06-08.md](wiggers_progress_2026-06-08.md) and
to the underlying hypothesis ledger at
[garmin/hypotheses/](garmin/hypotheses/). All findings are n-of-1 and
the participant's own.*
