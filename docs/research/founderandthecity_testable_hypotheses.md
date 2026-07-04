# Founder & the City (Welltory 700k-days) — testable hypotheses and cross-source comparison

Sibling to [wiggers_testable_hypotheses.md](wiggers_testable_hypotheses.md). Where that
document mines a patient-authored pacing *guide*, this one mines a completed empirical
*analysis* of a large wearable cohort, and asks the same two questions: what did the author
claim, and what can our N=1 corpus say back.

## Why this document exists

We want to ground our research in the research of others, and build on what others have
already done, so that we get further as a community rather than each starting from zero.
We started with the Wiggers pacing guide (a prescriptive, patient-craft source). This
Founder & the City piece — a population-scale wearable analysis of the same illness — was
the next thing we tried to replicate and use as inspiration. We take it seriously as prior
work and as a source of testable ideas, while keeping in full view the caveats and
limitations of an N=1 design: what a 2,000-to-45,000-person between-groups study finds and
what one person's within-subject time series can say are different inferential objects, and
neither can settle the other. This document is the honest bridge between the two.

## When to start

FC-H# testing is the **next-wave anchor**, not current-wave work. Three
gates must clear before FC dispatches open:

1. **Wiggers Tier 1 substantive close** — the C-cluster is closed as
   of 2026-06-23 (HA-C3 v2 REJECTED, HA-C3p PARTIAL, HA-C4c PARTIAL);
   remaining Wiggers work (P-cluster + K-cluster + cross-test
   interpretation pass) proceeds first.
2. **Website-team research-requests wound down** — the 18 open + 4
   in-progress R# requests (per `research-requests.md`) must reach a
   steady state; R14 + R15 (single-pool primary + driver ledger)
   are the load-bearing site-facing reframe and must land before FC.
3. **Operationalisation confidence** — pre-registrations for FC-H#
   tests need the operationalisation vocabulary already stabilised.
   The `/research-interpret` skill's D → I → S₁ → S₂ → A → T cascade
   through Phases A/B/C is what stabilises it; until Phase C
   (C-bout-substance / HA-C4c) closes, operationalisation is still
   in flight.

Until all three gates clear, FC-H# entries in this document are
**reserved-slot pre-regs**, not active dispatches. Cross-references
from Wiggers HAs to FC# claims are allowed and encouraged (they help
frame Wiggers findings against the between-groups population picture);
active FC-H# testing is not.

## Source

- **Title**: "I Analyzed 700,000 Days of Wearable Data to Find a Symptom No Test Can See"
- **Publication / author**: *Founder And The City* (Substack), published **2026-06-05**.
- **URL**: https://founderandthecity.com/p/i-analyzed-700000-days-of-wearable
- **Archive** (line-verified 2026-07-04):
  [literature/founderandthecity_2026_welltory_700k_pem.html](literature/founderandthecity_2026_welltory_700k_pem.html)
  (byte-faithful) + [.txt](literature/founderandthecity_2026_welltory_700k_pem.txt)
  (clean text for line-citation).
- **Dataset**: ~700,000 wearable user-days from **2,000+ users**; retrospective validation
  on **45,000+ users**; cohort split by **self-reported PEM** vs non-PEM.
- **Conflict of interest (load-bearing, flag on every citation)**: the author is the
  **CEO and founder of Welltory**, the platform whose data and product are analyzed, and
  discloses *"a direct commercial interest."* This is a Visible/Aitken-grade COI. It does
  not invalidate the work, but the surviving-feature story is told by the party that
  benefits from it, on its own data, with self-reported labels.
- **Genre difference from Wiggers**: Wiggers is prescriptive craft (claims to *act on*);
  this is a descriptive analysis (results to *compare against*).

## How to read this

- **FC# ids** index the author's claims (FC1…FC7 + a validation block), mirroring the
  Wiggers `A1…I3` register.
- **`FC-H#` ids** index the *within-person tests* those claims suggest for our corpus.
- **"His object / our object / same-thing?"** is the central comparison move: two sources
  can use the same word (*recovery*, *autonomic*, *variability*) for operationally different
  things. We say so explicitly rather than assume identity.
- **Status codes** on our tests: **CONFIRM** (we effectively already have it), **EXTEND**
  (we have a related piece, need to reshape), **NEW** (genuine gap), **PARTIAL** (started /
  queued), and where noted **ADVANCES-PAST** (a test finer than his metric could run).
- **The load-bearing difference**, applied throughout: his inferential object is a
  *difference between people* (between-groups, cross-sectional, self-reported labels,
  N up to 45k); ours is a *deviation within one person* (within-subject, hard crash
  definition `crash = run of >=2 consecutive days score <=3`, longitudinal, N=1, objective
  Garmin channels). A between-person effect can be a who-has-PEM confound — he demonstrated
  exactly this (FC2). A within-person effect cannot be, but cannot generalize. Complementary,
  not the same.

---

## A. The claims register — verbatim, operationalization, outcome

Quotes below are short verbatim fragments confirmed against the archive on 2026-07-04.

### FC1 — The boom-bust cycle does not appear
- **Claim (verbatim)**: *"The boom-bust cycle that the literature describes? Doesn't exist
  in the data."*
- **Operationalized as**: a detector using *"activity autocorrelation, crash probability
  modeling"* over 700,000 user-days; PEM vs non-PEM.
- **Outcome**: activity-autocorrelation difference **Cohen's d = 0.004**; crash probability
  after a high-activity day **15.8% (PEM) vs 16.9% (non-PEM)** — indistinguishable, if
  anything higher in non-PEM.
- **His reinterpretation**: boom-bust is *"a description of early-stage illness"*; adapted
  patients *"live on a carefully managed plateau"*; therefore *"you are not measuring the
  disease. You are measuring the result of someone coping with it."*

### FC2 — Recovery is paradoxically *better* in PEM (a confound, not a finding)
- **Claim (verbatim)**: *"The PEM group recovered better than non-PEM users. …
  In the wrong direction."*
- **Operationalized as**: matched pairs on age, sex, **step count**; recovery = *"how
  quickly and completely heart rate returned to baseline after exertion"* (acute,
  post-bout).
- **Outcome**: **Cohen's d = −0.12, p = 0.001**, PEM "better."
- **His diagnosis (verbatim)**: *"Matching on step count controls for how much someone walks,
  but it doesn't control for how they walk."* Same steps, different cardiac load →
  less to recover from. He warns this activity-intensity confound is likely
  *"under-addressed in much of the published wearable-PEM literature."*

### FC3 — Self-report and physiology barely agree
- **Operationalized as**: 47 users, 3 months of crash-severity / symptom surveys; **ICC**
  (intraclass correlation) against physiology, six features.
- **Outcome (verbatim)**: *"ICC … ranged from 0.019 to 0.356 across six features"*
  (below 0.4 = poor, below 0.2 = noise); best feature barely clears noise.
- **His framing**: *"The bill arrives 24 to 72 hours after the spending. Self-assessment
  captures the arrival of the bill, not the expense."* Lesson: *"self-report is a
  complement, not ground truth."*

### FC4 — The pivot: not how much, but how *predictably* (variability, not average)
- **Claim (verbatim)**: *"the consistency was the difference."*
- **Operationalized as**: **coefficient of variation (CV)** of recovery quality across days,
  in place of averages.
- **Outcome (verbatim)**: *"Non-PEM … steady, CV = 7%. Self-reported PEM … oscillating
  wildly, CV = 22%."* Effect sizes jumped to **Cohen's d > 0.7** after *"months of
  d = ±0.1"*.
- **His own framing of the primitive**: *"HRV itself is a variability metric — but applying
  it to multi-day recovery patterns was the move that unlocked this project."*

### FC5 / FC6 / FC7 — The three surviving features
- **FC5 Recovery consistency**: *"A body in the self-reported PEM group shows roughly twice
  the day-to-day spread. Same average, substantially different predictability."*
- **FC6 Autonomic switching speed**: *"how quickly the nervous system shifts gears after
  effort … (Cole et al., 1999); in the self-reported PEM group, the switch is slower … it
  held across every activity quartile."* (Cole 1999 = acute post-exercise heart-rate
  recovery — a minutes-scale measure.)
- **FC7 Cardiac cost of movement**: *"For the same walk, a person in the self-reported PEM
  group's heart works roughly 50% harder than an activity-matched non-PEM user."*

### FC-V — Validation (45,000+ users)
- **Model**: *"over twenty features … three-feature model slightly outperformed … AUC ≈ 0.77
  — meaningful for research signal-detection, but well short of … clinical use."*
- **Dose-response**: *"monotonic increase across crash severity (p < 0.001)."*
- **Cascade**: *"A bad recovery night predicts another bad night at more than double the
  baseline risk."*
- **Community cohort**: *"more than double the expected rate of elevated-risk scores."*

### FC-lim — Stated limitations (verbatim)
*"misses more than half of self-reported PEM cases. We chose specificity over sensitivity"*;
*"Menstrual cycle effects are almost certainly a first-class variable I'm not yet
incorporating. The sensitivity ceiling bothers me. The self-reported ground truth means
these are observational patterns, not validated diagnostics — replicating in clinically
confirmed cohorts is the essential next step."*

---

## B. Line-verification log (2026-07-04)

Every figure below was found in the archived source with the surrounding framing intact.

| Item | Verified value / phrase | In archive |
|---|---|---|
| Corpus | 700,000 days / "over two thousand people"; validation "more than 45,000" | ✓ |
| FC1 | d = 0.004; 15.8% vs 16.9% | ✓ |
| FC2 | d = −0.12; p = 0.001; "recovered better" | ✓ |
| FC3 | 47 users; ICC 0.019–0.356; six features | ✓ |
| FC4 | CV 7% vs 22%; d > 0.7 | ✓ |
| FC5–7 | "twice the day-to-day spread"; "Cole et al., 1999 … switch is slower … every activity quartile"; "50% harder" | ✓ |
| FC-V | AUC ≈ 0.77; monotonic p < 0.001; "more than double" (cascade + community) | ✓ |
| FC-lim | "misses more than half"; "menstrual … first-class variable"; "sensitivity ceiling bothers me"; "not validated diagnostics"; "clinically confirmed cohorts" | ✓ |

**Framing facts the verification surfaced**: (1) the author is Welltory's CEO (COI, above);
(2) his "recovery" is *acute* post-bout HR-return, not multi-day settle; (3) his metric
self-framing ("HRV is a variability metric applied to multi-day recovery") is our
`stress_stdev_sleep` "HRV-of-HRV-proxy" construct, reached independently.

---

## C. Are we talking about the same thing?

Short answer: on the two headline ideas, yes; on the specific metrics, mostly no — **same
principle, different primitive and different timescale.**

| Construct | His object | Our object | Same thing? |
|---|---|---|---|
| **"Recovery"** | acute HR-return-to-baseline after a bout (minutes) | felt-state + overnight-stress settle over days around a crash ([peri-event-recovery-export.md](analyses/garmin_exploration/cards/peri-event-recovery-export.md)) | Different timescale; related idea, not the same signal |
| **Variability > average** | between-day **CV** of a recovery scalar | within-night **stdev** of overnight stress + its night-to-night delta (HA07d) ([stress_stdev_sleep](analyses/descriptive/operationalisation_support/stress_stdev_sleep/findings.md)) | Same principle, different primitive — the strongest convergence |
| **Autonomic switching speed** | acute post-exercise parasympathetic reactivation (Cole 1999 HRR) | multi-day post-crash overnight-stress settle slope | Same word, different physiology/timescale |
| **Cardiac cost of movement** | HR work per unit walking (~50% harder) | none — our activity spec even parks "chronotropic incompetence" as do-not-build | We have not measured it (gap) |
| **Self-report vs physiology** | cross-person **ICC** (survey vs physiology), 47 users | within-person coupling over time (z-sign 32–41%, rolling ρ ≈ 0) ([subjective_objective_coupling](analyses/descriptive/trajectory/subjective_objective_coupling/findings.md)) | Same conclusion (weak, lagged), different unit |
| **Boom-bust** | population daily-activity autocorrelation → null | within-person antecedents; crashes carry *lower* avg activity ([exertion_class](analyses/descriptive/operationalisation_support/exertion_class/findings.md)); spike-in-calm-day hypothesis | Same null at daily aggregate; we can test finer than his metric can |

**Two framing convergences worth naming**, both independent of the metrics:
1. His *"carefully managed plateau … measuring the result of someone coping"* is our
   **"lived ceiling"** — felt-state realised only 1–6 on a 1–10 scale (R13,
   [felt_state_timeline](analyses/descriptive/felt_state_timeline/findings.md)).
2. His boom-bust null matches our finding that crashes carry *lower* average activity — but
   his own caveat ("measuring coping, not the disease") is exactly the door our
   **spike-in-a-calm-day** hypothesis walks through, and his daily-autocorrelation metric
   structurally cannot see it (memory: crash-triggers). This is where we can advance past him.

---

## D. Wiggers crosswalk

Where the two external sources meet (Wiggers register in
[wiggers_testable_hypotheses.md](wiggers_testable_hypotheses.md); contextualisation in
[analyses/contextualisation/topic-stress-fatigue-pacing.md](analyses/contextualisation/topic-stress-fatigue-pacing.md)):

| Construct | Wiggers | Founder & the City | Relationship |
|---|---|---|---|
| **Boom-bust** | central premise; pacing exists to prevent it | FC1: "doesn't exist in the data" (with the coping-plateau caveat) | **Tension** — same construct, opposite headline; both partly rescued by "spikes, not daily totals" |
| **Autonomic over-activation / slow settle** | C4/C4b "stuck sympathetic", slow stress decay | FC6 "the switch is slower" | **Agree** — same construct from prescriptive vs empirical sides |
| **Stress → fatigue shape** | C3: convex/non-linear (30→40 costs more) | no direct analog; nearest is FC7 + monotonic dose-response | **Different axis** — felt cost (Wiggers) vs cardiac cost (FATC); our HA-C3 found inverted-U, not convex |
| **Self-report as ground truth** | implicitly trusts the felt/stress coupling | FC3: felt ≈ noise vs physiology; "a complement, not ground truth" | **FATC qualifies Wiggers** — warns the felt signal is lagged and weak |

The sharpest cross-source story: **Wiggers and Founder & the City disagree about boom-bust,
and our data sits between them** — the kind of preserved conflict the contextualisation layer
is built to hold (both readings kept, comparability bound stated).

---

## E. What our N=1 research already tested

| Topic | Status | Where | Core finding |
|---|---|---|---|
| Recovery consistency / variability | Strong | [stress_stdev_sleep](analyses/descriptive/operationalisation_support/stress_stdev_sleep/findings.md), [HA07d result](analyses/hypotheses/HA07d-sleep-stress-variability/result.md) | Within-night stress variability is the **only** canonical both-eras-SUPPORTED discriminant (+19.6pp train / +21.7pp validate) |
| Autonomic recovery speed | Corroborated (shape) | [peri-event-recovery-export.md](analyses/garmin_exploration/cards/peri-event-recovery-export.md) | Felt-state rebounds in ~2–3 d (sharp V); overnight stress settles slowly over ~2 weeks |
| Cardiac cost of movement | **Gap** | none | No HR-per-activity metric anywhere |
| Self-report vs physiology | Corroborated (weak) | [subjective_objective_coupling](analyses/descriptive/trajectory/subjective_objective_coupling/findings.md) | z-sign agreement 32–41%; "the watch sees the crash, not the dip" |
| Boom-bust / activity→crash | Partial | [kind-of-crash-investigation.md](analyses/hypotheses/kind-of-crash-investigation.md) (K04 queued), [exertion_class](analyses/descriptive/operationalisation_support/exertion_class/findings.md) | Crashes carry *lower* avg activity (heavy+ 25.2% vs 35.8%); spike-timing hypothesised, not yet formally tested |
| Crash definition | Firm | [crash_v2-definition/definition.md](analyses/hypotheses/crash_v2-definition/definition.md) | crash = >=2 days score <=3 (n=29); dip = isolated bad day (n=79); distinct autonomic signatures |

Note: our crash label is objective and hard (>=2 days <=3), where his is self-reported
crash frequency — our ground truth is firmer, his cohort is vastly larger.

---

## F. Testable hypotheses and preparation

Prior-driven / confirmatory (source = Founder & the City, per CONVENTIONS §4.3), each an N=1
adaptation of a between-groups claim into a within-person crash-vs-baseline contrast. The
last column is the cross-hypothesis hook — which of *our* findings each lets us discuss
together.

| ID | FATC claim → our within-person test | Predicted direction | Status | Ties together |
|---|---|---|---|---|
| **FC-H1** | Recovery **CV** discriminates → rolling within-person CV of a recovery primitive (overnight-stress settle, RHR-return), crash-adjacent vs stable | higher CV near crashes | **CONFIRM + normalise** (we have stdev; CV is its normalised twin) | HA07d ⇄ his headline; makes "variability is the signal" externally comparable |
| **FC-H2** | Autonomic **switching speed** slower → fit a slope/rate scalar on overnight-stress settle (and, if extractable, an acute post-effort HR-recovery rate) per crash | slower settle at/after crash | **EXTEND** (we have curves, not a per-event slope) | peri-event R9 ⇄ Cole-1999 framing |
| **FC-H3** | **Cardiac cost of movement** → HR-per-step (or HR-per-active-minute) in matched activity bins, crash-era vs stable-era | higher HR-per-step near crashes | **NEW — clean gap** | fills the empty cell; stress-tests our step-based exertion_class |
| **FC-H4** | Self-report ↔ physiology weak & lagged → ICC/lag analog between gevoelscore-severity and a physiology composite | low ICC; best agreement at +1–3 d lag | **CONFIRM** | subjective_objective_coupling ⇄ his ICC; "watch sees crash not dip" ⇄ "bill vs expense" |
| **FC-H5** | Boom-bust absent at daily aggregate but **spikes** may trigger → daily-autocorrelation null test **and** a spike-in-calm-day → crash-at-+1–3d test | daily: null; spike: positive | **PARTIAL → ADVANCES-PAST** | exertion_class + K04 + crash-triggers; where our metric beats his |
| **FC-H6** | **Cascade** (bad night → 2× next night) → within-person night-to-night persistence of the bad-recovery state around crashes | elevated next-night risk near crashes | **NEW-ish** | connects peri-event settle to crash chaining (62% of crashes chain within 14 d) |

**Preparation (unlocks several at once):**

- **P1 — an intensity / cardiac-demand proxy (highest leverage).** His recovery-paradox
  lesson is *"step count controls how much someone walks, not how they walk."* Our
  `exertion_class` is step/activity-based, so it likely carries the **same confound he
  warns about**. An HR-relative-to-activity proxy (HR-per-step / active-HR) is the
  prerequisite for FC-H3 **and** retroactively hardens `exertion_class`, `HA-C4c`, and the
  boom-bust reading — one artefact improving three places.
- **P2 — a CV primitive beside our stdev primitive.** Normalise `stress_stdev_sleep` by its
  mean to get a true CV, so FC-H1 is *exactly* his metric and HA07d becomes an
  apples-to-apples external comparison rather than an analogy.

**Suggested starting point**: P1 + FC-H3 together — the one genuine gap, small and
self-contained, doubling as a confound-audit of our existing activity metrics.

---

## G. Caveats (N-of-1 discipline)

Carried per CONVENTIONS §4.6 and the contextualisation N-of-1 rules:

1. **A positioning call is one data point, not a settlement.** His population finding cannot
   settle our within-person question, and ours cannot settle his; an "agreement" is one
   aligned point across incommensurable units.
2. **The comparability bound is the reach bound.** Between-groups (his) vs within-subject
   (ours), self-reported PEM label (his) vs hard crash definition (ours), unspecified device
   pool (his) vs Garmin FR-class + `stress_mean_sleep` proxy (ours). These bounds cap every
   claim of "same" or "different" above.
3. **External consensus is not external truth**, and here the "consensus" is a single COI-laden
   source on its own data with self-reported labels. Treat FC1–FC-V as prior-driven hypotheses
   to test, not results to inherit.

_Authored 2026-07-04 as a producer-mode source register + first-pass comparison. Positioning
verdicts here are provisional and route to the reviewer-mode pipeline (per-test pre-regs +
`/research-review`) before any lock._
