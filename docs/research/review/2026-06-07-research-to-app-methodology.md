# From research findings to app surfaces — a methodology

*Independent reviewer-agent piece, 2026-06-07. Proposes a framework
for translating Garmin × crash research findings into the six indicator
families the participant wants in the app. Written as discussion input;
not a research-folder artefact. Status: draft for review.*

---

## 1. The translation problem

Research findings and app surfaces operate in different evidence
spaces. A research test asks:

> Does the metric discriminate crash-windows from non-crash windows
> above chance, with sensitivity/discrimination beyond a pre-registered
> threshold?

An app surface asks:

> Given what we now know, should we tell the user this — and if so,
> with what wording, with what confidence, and with what risk of
> producing a worse outcome by telling them?

The first is about signal detection. The second is about communication
under uncertainty with a real human consequence. Most of the project's
findings would pass the first test and fail the second under a careful
read. The translation has to be deliberate.

The core mismatch is **posterior probability**. The HA07d validate
finding (86.7% sensitivity, 65% null rate, base rate ~1.7% per
crash-window) yields:

> P(crash within 4 days | card fires) ≈ (0.867 × 0.017) / (0.867 × 0.017 + 0.65 × 0.983) ≈ **2.3%**

The card would fire on roughly 65% of days and be right about a crash
2 times in 100. That is not a useful pre-emptive warning. It might be
a useful retrospective explanation; it might be a useful descriptive
pattern. **The same statistic supports very different surfaces.**

This methodology starts from the principle that **the indicator type
constrains the evidence threshold, not the other way round**.

---

## 2. The six indicator families and their evidence asymmetries

The participant outlined six aims. They are not equivalent in their
evidence demands; one of the methodology's main jobs is to make those
asymmetries explicit.

| # | Family | Stakes if wrong | Bias preferred |
|---|---|---|---|
| 1 | Trajectory / stabilisation | Low — descriptive | Showing weak findings is OK if framed honestly |
| 2 | Event surfacing (crashes, dips) | Low for the score-defined event; medium for biometric corroboration | Score is ground truth; biometric overlay is decorative |
| 3a | Retrospective early warning ("this is what led up to it") | Low-to-medium | Surface readily if biometric pattern is plausible; framing must be observational |
| 3b | Pre-emptive early warning ("this may be coming") | **HIGH** | Strong bias toward **withhold** — false positives create anxiety, false alarms create habituation, both worsen behaviour |
| 4 | Recovery / return-to-pacing | Medium | **Bias to "still in crash territory"** — conservatism avoids premature reactivation |
| 5 | Personal lag calibration | Medium | Bias toward withhold-if-uncertain; only surface with CI |
| 6 | Push-pattern alert | High | Strong bias toward withhold unless evidence is robust + framing is observational |

The asymmetries matter because **the evidence threshold for each
family is a design choice, not a research output**. Two findings with
identical research statistics can warrant different surfacing
decisions depending on which family the card belongs to.

---

## 3. A general evidence framework

Six quantities should accompany every candidate card before any
"should we ship this" conversation. Most are already computed in some
form by the research apparatus; some are not.

| # | Quantity | Already produced? | What it answers |
|---|---|---|---|
| 1 | Discrimination (crash-rate − null-rate) | Yes, in every result.md | "Does it move at all?" |
| 2 | Sensitivity (P(card fires \| crash)) | Implicitly | "Of crashes, how many would the card catch?" |
| 3 | Specificity (1 − P(card fires \| no crash)) | Implicitly | "Of non-crashes, how often is the user left alone?" |
| 4 | Positive predictive value / posterior (P(crash \| card fires)) | **No** | "When the card fires, how often is it right?" |
| 5 | Confidence interval on the posterior | **No** | "How sure are we about the answer to #4?" |
| 6 | Era applicability (train / validate / both) | Yes | "Is this expected to work for *this* participant *now*?" |

Items 4 and 5 are the bottleneck. Without them, no surfacing decision
can be defensible. The HA07d Bayes example above shows why — a +20 pp
discrimination can produce a 2% posterior at low base rates.

### 3.1 The withhold-by-default rule

A finding becomes a card *only* if it crosses an explicit threshold on
the posterior, not just on discrimination. The threshold is family-
specific (see §4).

A finding that does not cross the threshold can still be:
- mentioned in onboarding / education ("research suggests …"),
- used inside the app's analytical layer to inform other features
  (e.g. retrospective explanations even if not pre-emptive warnings),
- preserved as future-research material.

It simply cannot become a card the user sees in their normal flow.

### 3.2 The framing-discipline rule

Even when a finding crosses the evidence threshold, the *wording*
matters. Cards should follow three principles:

- **Observational, not predictive.** "Your morning Body Battery has
  been unusual" reads as an observation. "Your morning Body Battery
  suggests a crash may be coming" reads as a prediction the data
  cannot support.
- **Reversible, not anchoring.** Users should be able to read the card,
  notice it, and continue their day. Cards should not produce a
  recommendation that, if wrong, causes the user to behave worse than
  they would have without the card.
- **Past-tense friendly.** Retrospective cards are nearly always safer
  to ship than pre-emptive ones. "Looking back at the days before
  your crash on Tuesday" carries no anxiety load; "you may be heading
  into a crash" does. Where possible, prefer retrospective framing
  even when the underlying signal could support pre-emptive framing.

---

## 4. Per-family methodology

### Family 1 — Trajectory / stabilisation indicators

**What it is.** Long-arc descriptive read on whether the participant
is becoming more stable over time. Stress baseline coming down,
max-spike duration shortening, crash frequency dropping, mean
gevoelscore trending up. Built on S01 (Garmin trajectories) +
proposed S02 (score trajectory) + K01/K02 (crash depth + duration)
+ the dip-cluster overlay.

**Evidence threshold.** Low. This is descriptive characterisation of
the participant's own history, not a prediction. The risk of being
wrong is small — at worst, the user reads "your stress baseline has
come down" and finds the framing slightly off. No false alarm, no
behavioural consequence.

**Required statistics.**
- At least 18 months of data (so the rolling window can produce a
  meaningful arc).
- A normalised or annotated y-axis so the user understands the
  comparison ("compared to your peak in 2023, your typical stress is
  now 4 points lower").
- A "no pre-illness anchor" caveat baked into the framing.

**Framing discipline.**
- Reflective Dutch, retrospective tense.
- Multi-axis. "Your crash frequency has dropped from ~10/year to ~2/year;
  your typical stress is down 4 points; your sleep efficiency is stable."
  Single-metric cards over-fit to noise; multi-axis cards triangulate.
- No causal claim about *why* the trajectory changed.
- Explicit handling of the May 2026 perturbation: "Recent uptick worth
  knowing about" rather than "trend reversing."

**Withhold rule.** If the user has < 12 months of data, withhold the
trajectory card entirely. Show "trajectory will appear once you have
12 months of data" instead.

**Current research status.** S01 done; S02 queued. K01 + K02 done.
Sufficient material exists to prototype trajectory cards now.

### Family 2 — Event surfacing (crashes, dips)

**What it is.** Mark crashes and dips on the timeline as the user
sees their daily log. Optionally enrich with biometric context
("there was unusual stress that week").

**Evidence threshold.** Zero for the score-defined event itself; the
gevoelscore IS the ground truth for crashes (`crash_v1` / `crash_v2`).
A score-≤3-for-2-days sequence is, by definition, a crash. There is
no inferential gap.

For biometric enrichment, the threshold is moderate. The enrichment
should be marked as such ("there was an unusual stress pattern on
Tuesday — the watch noticed it") and the user should understand it as
supporting context, not as the crash itself.

**Required statistics.**
- The crash/dip classifier (locked in `crash_v2-definition`).
- For biometric enrichment: a per-event biometric summary using the
  SUPPORTED-channel findings as flagging criteria.

**Framing discipline.**
- The event itself is named ("crash" / "dip" / "rough patch" — using
  the participant's own preferred terminology).
- Biometric enrichment is optional and observational.
- Do NOT use biometric data to relabel the event. If the user
  logged score 3 for 2 days, it's a crash regardless of what the
  watch saw.

**Withhold rule.** Biometric enrichment is withheld for any individual
event where the enrichment statistic falls in an ambiguous range
(e.g. discrimination at threshold). The event is still marked; just
without enrichment text.

**Current research status.** Crash_v1, crash_v2, dips, dip clusters
all defined. The HA07d + HA10 findings provide candidate biometric
enrichment signals for validate-era crashes. The H02b + H02d findings
provide enrichment for train-era crashes. Sufficient material exists
to prototype.

### Family 3a — Retrospective early-warning ("this is what led up to it")

**What it is.** When the user reviews a past crash, show what the
biometric signals looked like in the days leading up. Examples: "in
the 3 days before this crash you had a 17-minute stress spike on
Tuesday afternoon" or "your morning Body Battery was unusually high
in the 4 days before this crash — sometimes a sign of paradoxical
recovery."

**Evidence threshold.** Medium. The retrospective framing carries
much lower anxiety risk than pre-emptive, so the bar can be lower
than 3b. But the framing must remain observational and avoid causal
language.

**Required statistics.**
- Discrimination + sensitivity above pre-registered bars (already
  achieved by HA07d, HA10, H02b, H02d, HA06b, HA11).
- Specificity good enough that the pattern isn't "this happened in
  most non-crash periods too." This is the missing piece for
  several findings — HA10's 70% null rate means the same pattern is
  present in most non-crash days too, which weakens the "this is what
  led up to it" claim.
- Era applicability: the finding must hold in the era the user is
  currently in. Train-era findings should be retrospective-only for
  pre-2024 crashes; validate-era findings retrospective-only for
  post-2024 crashes.

**Framing discipline.**
- Past-tense, descriptive. "In the 4 days before this crash, your
  morning Body Battery sat unusually high. The body sometimes shows
  this pattern when overnight recovery looks better than it actually
  was."
- Cite the research source: "Wiggers and others have described this
  pattern as the 'parasympathetic swing.'" Adds legitimacy and
  defuses "the watch is judging me" framing.
- NEVER imply the user could have prevented the crash by responding
  to a signal that was only visible in hindsight.

**Withhold rule.** Withhold for any crash where the specificity check
shows the pattern was equally present in surrounding non-crash days.

**Current research status.** Multiple SUPPORTED findings available.
The specificity checks have been done for H02b train-era; missing for
HA07d / HA10 / HA06b / HA11. **Highest-priority methodological gap.**

### Family 3b — Pre-emptive early-warning ("this may be coming")

**What it is.** A live signal that fires before a crash to alert the
user. Examples: "your last 3 nights' stress variability has collapsed
— this pattern has preceded crashes" or "watch out — you may be
heading into a rough patch."

**Evidence threshold.** **HIGH and currently unmet by any project
finding.** Pre-emptive cards have the highest stakes:

- False positives induce anxiety, reactive behaviour, false alarm
  fatigue (user stops trusting the app).
- False negatives create a "the app said I was fine" anchor that may
  prevent the user from self-pacing when they otherwise would.
- Either failure mode worsens outcomes relative to no card at all.

The evidence bar must be set at the posterior probability level, not
the discrimination level. **A reasonable rule of thumb: P(crash within
N days | card fires) ≥ 50%** (i.e. the card is right more than half
the time it fires). At base rates of 1–2% per day, this requires
extremely high specificity — typically > 99%. None of the current
findings come close.

**Required statistics.**
- All six items from §3.
- Per-fire confidence interval on the posterior.
- Era applicability bounded to the current era.
- A long enough validation history that the pre-emptive prediction
  has been "wrong about no crash" enough times to characterise the
  false-positive rate empirically.

**Framing discipline.**
- If a pre-emptive card ever ships, it should be framed in the
  *gentlest possible* observational language: "Your body has been
  doing something it has sometimes done before a rough patch. Worth
  knowing." Not "you may crash." Not "warning."
- Should be dismissible without the user feeling judged.
- Should NEVER recommend a specific behavioural change ("rest more")
  — that crosses into clinical prescription and is outside scope.
- Frequency-capped. Should fire no more than once per real crash
  window, not daily.

**Withhold rule.** The current project state has **no finding that
meets the bar for pre-emptive surfacing**. The right product
decision is to ship the app *without* this family entirely, marking
it as future-research-dependent.

If the bar is ever met (e.g. through HA07d sharpened by H04b per-
minute decode, or through a cross-channel composite that achieves
> 99% specificity), surfacing should be opt-in only and gated behind
explicit user enrollment with a description of expected accuracy.

**Current research status.** Insufficient. Strong reading: do not ship
pre-emptive cards in v1.

### Family 4 — Recovery / return-to-pacing indicators

**What it is.** After a crash, signal when it appears safe to resume
normal pacing — or, conversely, signal that the participant is still
in crash territory and should keep their guard up.

**Evidence threshold.** Medium-high, with **asymmetric error
preference**. False positive ("safe to resume") when actually still
crashing → reactivation, possible deeper crash. False negative
("still in crash") when actually recovered → unnecessary caution but
no physiological harm. **Bias strongly toward false negative** (i.e.
prefer to keep the user in "still in crash" framing longer than
strictly necessary).

**Required statistics.**
- Empirical recovery-time distribution from the participant's own
  crashes. K02 partly characterises this; H05 was spec-broken and
  H05b is queued.
- Per-crash biometric "return to baseline" check on the SUPPORTED
  channels.
- Confidence interval on the recovery estimate.

**Framing discipline.**
- Conservative-direction framing: "your last few crashes have
  averaged 2.5 days; you're on day 4 — likely past the worst, though
  not always" rather than "you've recovered."
- Multi-source: combine score-trajectory + biometric-return + average
  duration. No single source should drive the call.
- Always end with a "you know your body best" defer-to-user note.

**Withhold rule.** If the participant's recovery distribution shows
high variance (e.g. some 2-day crashes, some 14-day), the precise
estimate becomes unreliable. In that case, show the *distribution*
("between 2 and 14 days; usually 3–4") rather than a point estimate.

**Current research status.** Recovery-time data is implicitly in the
crash-episode list but not formally characterised as a distribution.
H05b is queued. **Worth elevating** — recovery framing has lower
anxiety risk than pre-emptive warning and is conceptually well-defined.

### Family 5 — Personal lag calibration

**What it is.** Personal estimate of the typical delay between an
exertion / trigger event and the resulting crash, with an uncertainty
interval. "After a high-exertion day, your crashes typically follow
3–5 days later" or, when the data doesn't support it, nothing.

**Evidence threshold.** Medium, with **withhold-on-uncertainty** as
first-class outcome.

**Required statistics.**
- An empirical lag distribution from the participant's own crashes.
  The lag profile work (HA01b, H02d 3d/4d/5d sweep) gives the start
  of this for activity-shock and stress-spike channels.
- Per-channel lag estimate (the lag for stress-spike → crash may
  differ from activity-shock → crash).
- 95% CI on the lag estimate.
- Minimum episode count: probably 10+ events with a clear preceding
  trigger to support a lag estimate.

**Framing discipline.**
- Probabilistic. "Your crashes have typically followed exertion days
  by 3–5 days, give or take." Never a point estimate without a
  range.
- Trigger-specific where the data supports it. "For high-stress
  days the gap has been ~3 days; for high-physical-exertion days,
  closer to 4–5."
- Always defer to the user's experience: "this is an empirical
  pattern; your body may differ on any given day."

**Withhold rule.** If the 95% CI on the lag spans more than 3 days
(e.g. CI = 2 to 7 days), withhold. The card is no longer informative.
Replace with "your lag pattern is still being learned."

**Current research status.** The lag-profile evidence exists in
fragments (H02d, HA01b lag-profile report) but has not been
consolidated into a per-participant lag estimate with CI. **Modest
research effort to formalise; high product leverage.**

### Family 6 — Push-pattern alert

**What it is.** Detection of sustained-overexertion-without-recovery
patterns ("the push pattern"). If the participant is on a 5-day
above-baseline activity stretch without a recovery day, surface that.

**Evidence threshold.** **HIGH** — same family as 3b for the
pre-emptive case. The "push theory" is plausible but the project's
direct test of it (HA02 / HA02b / HA02c push burden) refuted in both
eras on a clean baseline. **There is currently no empirical evidence
that the push pattern precedes crashes in this participant.**

This is a crucial finding. The push pattern is one of the most
strongly held lay beliefs about PEM, and it is empirically absent
from this participant's pre-crash data on three operationalisations.
Surfacing a "you're pushing" alert based on lay belief rather than
on the participant's own data would violate the project's evidence
discipline.

**Required statistics.**
- A SUPPORTED finding on the push channel for the participant's
  current era.
- Specificity high enough that the alert doesn't fire on most weeks
  the participant is fine.
- Per-fire posterior probability ≥ 50%.

**Framing discipline.**
- If ever shipped: descriptive, not prescriptive. "You've had 5
  above-baseline days in a row without a recovery day. The body
  sometimes responds to this with a rough patch."
- Never recommend a specific intervention.
- Frequency-capped per real-pattern instance.

**Withhold rule.** Until a push-channel finding SUPPORTS for the
participant's current era, withhold entirely. Do not ship the push
alert on lay-belief basis.

**Current research status.** The push channel has refuted in three
operationalisations (HA02 / HA02b / HA02c). The right v1 decision is
to **not ship this family**. Future research (e.g. activity-load on a
finer time-scale, or coupled to the stress / BB channels) may unlock
it.

---

## 5. Cross-cutting principles

### 5.1 Asymmetric error tolerance is family-dependent

For trajectory (Family 1) and event-surfacing (Family 2), the cost of
being wrong is small. Push the cards out, frame them honestly.

For retrospective warning (Family 3a) and recovery (Family 4),
moderate caution. Specificity matters; framing carries most of the
safety burden.

For pre-emptive warning (Family 3b) and push-pattern alert (Family 6),
high caution. Most current research findings do not clear the bar.
Default decision is "do not ship."

For personal lag (Family 5), withhold-on-uncertainty is first-class.
Showing "we don't yet know your lag" is preferable to showing a
misleading point estimate.

### 5.2 Anxiety is a first-class output of any surfacing decision

The project's research has been disciplined about statistical
properties of its findings. The surfacing layer must be equally
disciplined about anxiety properties. A finding that increases the
user's anxiety without improving their outcomes is a net negative
even if it is "statistically real."

Concrete rule: any card that fires more than once a week, OR that
uses warning-like language ("watch out," "may be," "could lead to"),
should be evaluated against the question "would I want to receive
this card on a normal Tuesday?"

### 5.3 Era moderation needs surfacing-level handling

Findings that hold only in one era should be either:

- restricted to retrospective surfacing for that era (e.g. H02b train
  retrospective for pre-2024 crashes only), or
- restricted to the era the participant is currently in (e.g. HA07d
  validate for current pre-emptive consideration).

A SUPPORTED finding from the wrong era should not be surfaced.

### 5.4 Calibration over time

Every card that fires should be loggable as fired-correctly or
fired-incorrectly (e.g. by the next 4 days' actual experience). The
app should record this and update its own estimates of the card's
posterior probability over time. A card that fires correctly < X% of
the time over a sustained window should auto-suppress.

This is the longest-term commitment but the one that turns the app
from a "research findings frozen in time" tool into a "this participant's
data refines the findings as it accumulates" tool.

### 5.5 User control

Every card family should be opt-out at the user level. Family 3b
(pre-emptive warning) should be opt-in even if it ever ships. Family
4 (recovery) should default to conservative framing; user can opt
into faster framing if they want.

---

## 6. The "from finding to card" workflow

A proposed pipeline for any future finding entering the app:

| Gate | Question | Owner |
|---|---|---|
| **G1 — Research bar passed** | Discrimination + sensitivity above pre-registered floor, in the era of interest | Research agent |
| **G2 — Specificity check** | False positive rate characterised on the participant's actual non-crash days | Research agent |
| **G3 — Posterior probability computed** | P(event \| card fires) at the base rate of the relevant era | Research agent + reviewer |
| **G4 — Family assignment** | Which of the six families does this card belong to? | Reviewer + product |
| **G5 — Threshold check** | Does the posterior meet the family-specific threshold from §4? | Reviewer + product |
| **G6 — Framing draft** | Is the wording observational, reversible, anxiety-bounded? | Product + reviewer |
| **G7 — Anxiety/burden review** | Would the user want this card on a normal Tuesday? | Product + participant |
| **G8 — Calibration plan** | How will the card's correctness be measured over time? | Product |
| **G9 — Ship** | All previous gates pass; surface as opt-out card | Product |

G1–G3 are research-side and partly mechanical. G4–G9 are product /
design / participant decisions and need the participant's own
judgement as the binding input.

The most useful immediate output of this methodology is **a list of
which current findings can pass which gates**.

---

## 7. Current findings against the gate framework

| Finding | G1 (research bar) | G2 (specificity) | G3 (posterior) | Recommended family |
|---|---|---|---|---|
| H02b train per-minute stress spike | ✓ SUPPORTED | ✓ checked (specificity-check.md) | ? not formally computed | Family 3a retrospective, pre-2024 crashes only |
| H02d bridge × 5d train stress spike | ✓ SUPPORTED | partly | ? | Family 3a retrospective, pre-2024 crashes only |
| HA06b train RHR z-score | ✓ SUPPORTED | ✗ not checked | ✗ | Family 3a retrospective, pre-2024 crashes; pending specificity |
| HA10 validate morning BB peak | ✓ SUPPORTED (fragile) | ✗ not checked (70% null rate → low) | likely low (Bayes ~2%) | Family 1 / 3a observational only; not pre-emptive |
| HA11 train within-day stress U-dip | ✓ SUPPORTED | ✗ not checked | ✗ | Family 3a retrospective, pre-2024 crashes; pending specificity |
| HA07d both eras sleep stress variability | ✓ SUPPORTED both | ✗ not checked | likely low at current rates | Family 3a both eras + Family 1 trajectory anchor; not pre-emptive |
| Stabilisation trajectory (S01 + K01 + K02) | n/a — descriptive | n/a | n/a | Family 1 — ready to prototype |
| Crash + dip event labels | n/a — definitional | n/a | n/a | Family 2 — ready to prototype |
| Push burden (HA02 family) | ✗ REFUTED | n/a | n/a | Withhold entirely |

**Cards ready to prototype now:**
- Family 1 trajectory cards (S01 + S02 + K01 + K02 + dip clusters).
- Family 2 event-surfacing (crash/dip markers; biometric enrichment
  on the train-era retrospective channel where specificity is known).

**Cards needing one more research step before prototyping:**
- Family 3a retrospective cards on validate-era findings (HA07d,
  HA10). Need specificity checks first.
- Family 4 recovery cards. Need H05b (sustained recovery target) + a
  per-channel return-to-baseline check.
- Family 5 personal-lag card. Needs a per-participant lag estimate
  with CI on the SUPPORTED channels.

**Cards that should NOT be shipped in v1:**
- Family 3b pre-emptive warning — no finding meets the posterior bar.
- Family 6 push-pattern alert — channel has refuted in three
  operationalisations.

---

## 8. The bottom line

The project's research has produced enough material to support
Families 1 and 2 immediately, Families 3a / 4 / 5 with one round of
methodology work each, and Families 3b / 6 not at all without further
research that may or may not deliver.

This is not a small product. Trajectory + event surfacing + retro-
spective warning + recovery + personal-lag is a complete, honest,
defensible v1. It would be a useful tool. It would not contain the
predictions the user might expect from a "watch tells me when I'm
about to crash" framing — but that framing is not supported by the
data, and shipping it anyway would harm rather than help the
participant.

The methodological discipline the project has shown on the research
side should carry over to the product side. The discipline says:
**ship what you can defend; withhold what you can't; calibrate as
you go.**

---

*Draft for review. Save to `docs/research/review/` or move to a
product-facing location (`docs/design/` or a new `docs/product/`
folder) depending on where the v1 conversations are happening.*
