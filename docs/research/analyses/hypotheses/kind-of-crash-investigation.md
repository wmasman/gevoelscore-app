# Investigation plan — testing the "kind of crash changed" theory

*Companion to [synthesis.md](synthesis.md). Plan-only document — no
tests have been pre-registered yet under this thread. The H## numbering
is reserved for first-batch precursor hypotheses; this thread uses
**K## (kind)** for hypotheses about how crashes themselves differ
across eras.*

## 1. Why this thread is worth its own plan

The first batch (H01–H05 + synthesis) produced one finding that is
genuinely structural rather than just "test result":

> Pre-recovery crashes had a sympathetic-arousal precursor (H02 train
> showed clear direction). Post-recovery crashes don't show that
> precursor — or any of the daily-aggregate precursors we tested.

The simplest explanation that fits the data is: **the kind of crash
the user experiences in 2025–26 is qualitatively different from what
they experienced in 2022–23.** Not just less frequent (which we know:
~10/year → ~2/year), but different in *mechanism*.

This theory is currently *indirectly inferred*. It would be useful to
test it directly, because:

- **Feature consequences are large.** A spike-detecting H02b-style
  card and a sleep-fragmentation H03b-style card serve different
  populations of crashes. If pre-recovery and post-recovery crashes
  cluster into distinct types, we should tag insight cards with
  "applies to crashes of type X" rather than treating all crashes the
  same.
- **It tells the user something about their journey.** "The crashes
  that still happen are a different kind from the ones that used to
  happen" is itself a powerful retrospective card. Without this
  investigation it's a hypothesis; with it, it's a finding.
- **It reframes the residual crashes**. Rather than "you still get
  crashes — here's how to predict them," it becomes "you've moved
  through one mechanism; this residual mechanism is the next thing
  to learn." Very different emotional weight.

## 2. What "kind of crash changed" could specifically mean

Before designing tests, surface the candidate mechanisms by which
crashes could differ. The five plausible axes:

1. **Severity / depth.** Maybe 2024+ crashes score higher (less deep)
   on the gevoelscore scale even though they're still ≤ 3.
2. **Duration.** Maybe 2024+ crashes resolve faster (or slower) than
   2022–23 ones.
3. **Symptom profile.** Maybe the dominant symptoms reported in notes
   shifted — e.g. headache-dominant → fatigue-dominant, physical → 
   cognitive, etc.
4. **Antecedent type.** Maybe 2022–23 crashes were preceded more
   often by physical-load events; 2024+ crashes preceded more often
   by emotional / cognitive / illness events.
5. **In-crash physiological signature.** Maybe during a 2022–23 crash
   HR / stress / sleep look different from during a 2024+ crash.

Each axis has different evidence sources and different test shapes.

## 3. Pre-registered hypotheses queue

Six candidate K-hypotheses, in roughly the order they should be tested.
None has been pre-registered yet; each will get its own
`K##-<name>/hypothesis.md` before any test runs.

### K01 — Crash depth shifted across eras (severity axis)

**Claim**: The minimum score within each crash_v1 episode (the
"crash nadir") is on average **higher** in 2024+ than in 2022–23.

**Measurement**: For each episode, the minimum score during the
episode is the nadir. Compare distributions of nadirs in train vs
validate.

**Falsification**: median nadir in validate is *not* at least 0.3
points higher than median nadir in train (this user's scale is 1–6;
0.3 is meaningful but not overclaiming).

**Why first**: cheapest possible test, no new data needed.

**Data**: gevoelscore only.

### K02 — Crash duration shifted across eras (duration axis)

**Claim**: The total span (calendar days from first low day to last
low day in the merged episode) is on average **shorter** in 2024+
than in 2022–23.

**Measurement**: Compare span distributions.

**Falsification**: median span in validate is not at least 1 day
shorter than median span in train.

**Why next**: also cheap; complements K01.

**Caveats**: H05's spec-broken finding does not affect K02 because
this metric is about episode span, not recovery time.

### K03 — Symptom profile shifted across eras (symptom axis)

**Claim**: Notes on crash days mention different keyword clusters in
2024+ vs 2022–23. Specifically, the relative frequency of physical
symptoms (hoofdpijn, moe, kapot, misselijk, slap) vs cognitive
symptoms (concentratie, brainfog, mistig, traag) vs emotional
descriptors (huil, somber, paniek) differs by era.

**Measurement**: Build a keyword dictionary (Dutch). For each crash
day, score the notes for each cluster. Build per-episode vectors
(physical / cognitive / emotional weights). Test era × cluster
distribution with a simple frequency comparison.

**Falsification**: relative cluster weights are not meaningfully
different across eras (defined by some pre-registered effect-size
threshold).

**Why important**: this directly tests the mechanism-shift theory at
the level of subjective experience. If the user's *language* about
crashes shifted, that's strong evidence the underlying experience
shifted.

**Caveats**: notes-use discipline may have evolved; need to verify
the per-day word count is comparable across eras before drawing
conclusions about cluster mix.

**Cost**: requires a curated Dutch symptom-keyword dictionary. The
user can collaborate on this — it's exactly the kind of "your
language about this" knowledge only they have.

### K04 — Antecedent type shifted across eras (trigger axis)

**Claim**: 2022–23 crashes were preceded more often by quantifiable
physical-load events (long activities, high active-minutes), 2024+
crashes are preceded more by neutral physical lead-ups.

**Measurement**: For each crash, compute the 3-day pre-episode
total active-minutes (highly active + active seconds from UDS) and
the count of recorded workouts. Compare distributions across eras.

**Falsification**: pre-crash active-minutes are not meaningfully
different across eras.

**Why important**: directly tests "boom-bust precipitates 2022–23
crashes, residual crashes are non-physical-load triggered."

**Data**: gevoelscore + UDS daily aggregates + summarizedActivities.

### K05 — In-crash physiological signature shifted (in-crash axis)

**Claim**: During the crash itself (not before), the 2022–23 crashes
show different stress / RHR / sleep patterns from the 2024+ crashes.

**Measurement**: For each crash, average the Garmin metrics across
the episode's days. Compare across eras.

**Falsification**: in-crash metric distributions don't meaningfully
differ across eras.

**Why later**: more confounded by the same physiological-shift the
user has undergone independent of crash mechanism. A "more stressed
during crashes" finding in train vs validate could just mean "user
was more stressed overall in 2022–23." Need to control by comparing
in-crash to matched non-crash baselines.

**Refinement needed**: K05 may want to use *change from baseline
during the crash* rather than absolute values, to control for the
general physiological shift.

### K06 — Calendar-context profile shifted (context axis, deferred)

**Claim**: Crashes in 2024+ are more often preceded by specific
calendar-event categories (e.g. social events, travel, family
demands) than 2022–23 ones.

**Status**: **deferred** until calendar coverage backfills further
or until we accept that calendar only covers 2022-06 onward.

## 4. Sequencing and interlock with the H## thread

```
H02b (now)                  K01, K02 (cheapest)
   │                              │
   ▼                              ▼
 H02b result                 K01, K02 results
   │                              │
   ├──→ if supported: feeds K03   ├──→ inform K03 design
   │    (which crashes had        │
   │     the spike precursor?)    │
   ▼                              ▼
 H05b (sustained recovery)   K03 (symptom profile)
                                  │
                                  ▼
                             K04 (antecedent type)
                                  │
                                  ▼
                             K05 (in-crash signature)
                                  │
                                  ▼
                             K06 (calendar context, when coverage allows)
```

Run order proposed:

1. Finish H02b. Its result either confirms or refutes the
   "spike-anchored precursor" thread.
2. K01 + K02 in parallel (both very cheap). These give the first
   direct evidence on the era-shift theory.
3. K03 — collaborate with the user on a Dutch symptom-keyword
   dictionary first. Then test.
4. H05b — clean spec, restore the recovery-time card concept.
5. K04 — antecedent type, requires combining gevoelscore + Garmin
   activity counts.
6. K05 — in-crash physiological signature, more confounded so
   later.
7. K06 — calendar context, when data permits.

## 5. What this would deliver if supported

If K01–K05 confirm the era shift in multiple ways, the synthesis
gains a clear positive finding:

> The crashes the user experiences in 2024+ are quantifiably
> different from the crashes they experienced in 2022–23 — in depth
> (K01), duration (K02), reported symptom profile (K03), antecedent
> type (K04), and in-crash signature (K05). This is the strongest
> evidence we can get from this dataset that the user is not just
> experiencing fewer crashes of the same kind, but moving through a
> mechanism.

That conclusion would directly support:

- A **recovery-arc card** as a foundational retrospective view
  ("you've moved through one kind of crash mechanism")
- **Subtype-tagged insight cards** ("this looks like a 2024+-pattern
  crash, here's what we know about those")
- **Forward-looking framing** that respects where the user actually
  is on their journey rather than re-litigating the past

If K01–K05 do *not* confirm — if the crashes are basically the same
just less frequent — that's also useful information. It would push us
back toward the H## thread (spike-anchored precursors, sleep
subcomponents, HRV) and away from era-specific framing.

## 6. What this plan does NOT cover

- **Why** the user is recovering (the intervention question). This is
  the shielder-vs-reliever territory the pacing-doc points at, and it
  requires intervention tags we haven't yet structured.
- **Whether** the recovery will continue. The dataset can describe
  the trajectory; it cannot predict whether it will plateau, accelerate,
  or reverse.
- **Generalisability** to other PEM patients. The whole project is
  n-of-1.

## 7. Methodology lessons to carry into this thread

From the H## batch:

1. **Dry-run a small sample before locking a spec.** H03's
   confirmation-type whitelist and H05's recovery target both passed
   pre-registration review but produced uninformative results when
   met by reality. A "compute the metric for 3 episodes, eyeball it,
   then lock" checkpoint would have caught both.
2. **Use absolute thresholds when distributions cluster on integers.**
   The crash_v1 preflight revealed ties at score=4 broke percentile
   rules. Same caution applies to anything K## might compute over
   the 1–6 score scale.
3. **Pre-register the falsification criterion that *would* have made
   you change your mind.** "What number would have refuted me" forces
   honest design.
4. **Note what the data does not say**, alongside what it does.
   The user's "good sleep is not a protector" framing is the model.
5. **Save n=1 experiential evidence as project memory** when the user
   reports it. The "intense moment in calm day" memory was the
   strongest single piece of mechanism evidence the project has,
   and it shaped H02b's design.

## 8. When this plan gets re-opened for review

After H02b closes. The result will sharpen the priorities here —
specifically, if H02b is supported, K## investigation can focus on
"which crashes the spike-precursor card applies to" as a subgroup
analysis rather than re-testing precursors. If H02b is refuted,
K## investigation becomes the only remaining structured path forward
in this dataset.

---

*Plan written 2026-06-05 while H02b's FIT-parse stage runs in
background. Pre-registrations follow the same `hypothesis.md → test.py
→ result.md → card.md` flow as the H## batch.*
