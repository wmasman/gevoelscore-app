# App plan — pacing indicators + trajectory + events (active)

*Active product plan, merging `pem-pacing-indicators.md` (research-side
pacing indicators) and `2026-06-07-trajectory-and-events-app-plan.md`
(Families 1+2 app plan) into a single source of truth. State-of-the-
world: 2026-06-07 late-evening, after S02 + S02b + S02c + the
threshold-monotonicity v2 rescue round.*

*Both source documents are archived at
[_archive/](_archive/) and superseded by this one. Methodology framework
piece [2026-06-07-research-to-app-methodology.md](2026-06-07-research-to-app-methodology.md)
remains active.*

---

## 1. What this document is

A single product plan covering the surfaces the participant might see
in the app, anchored against the research's discipline (pre-registered
findings, audit-trailed verdicts, n=1 evidence, no-prescription rule).

**Audience.** Someone living with a chronic post-acute infection
syndrome (PAIS — Long COVID / ME/CFS / post-Lyme / post-EBV),
characterising their personal energy envelope and noticing events
that affect exertion or raise PEM risk. Also the participant in this
n=1 research project.

**Status.** Active product plan; not yet a feature spec. Phase 1 is
ready to move to `docs/features/` once participant decisions on the
open questions in §10 land. Later phases gated as described per
phase.

**Replaces:**
- `pem-pacing-indicators.md` (the research-side curated indicator
  catalogue) — archived at [_archive/pem-pacing-indicators.md](_archive/pem-pacing-indicators.md).
- `2026-06-07-trajectory-and-events-app-plan.md` (the Families 1+2
  app plan) — archived at [_archive/2026-06-07-trajectory-and-events-app-plan.md](_archive/2026-06-07-trajectory-and-events-app-plan.md).

---

## 2. Framing — PAIS, energy envelope, PEM

(Carried from the pacing-indicators piece. Sets the *why* behind any
surface in this plan.)

In PAIS conditions the patient often describes an *energy envelope*: a
range of exertion they can sustain without triggering Post-Exertional
Malaise (PEM). The envelope is small and unstable. Push above it once
(*shock*) or repeatedly (*push-crash*) and a crash follows, often
delayed by hours to days.

Two mechanistic threads recur in the literature:
- **Sympathetic over-activation** — autonomic dysregulation, with the
  sympathetic nervous system firing harder than it should during
  ordinary moments. Measurable as transient HR-derived stress spikes.
- **Parasympathetic recharge failure** — insufficient overnight
  recovery, often reported as "unrefreshing sleep". Measurable in
  principle as the overnight recharge of physiological reserves.

Two further patterns shape what an indicator should catch:
- **Shock-induced PEM** — a single acute event in an otherwise calm
  period can trigger a crash.
- **Push-crash** — sustained moderate elevation over 5-10 days erodes
  the envelope until a crash arrives.

A complete picture needs surfaces that respect both modes.

**Stabilisation framing, not recovery framing** (per project memory):
the participant is in active stabilisation, not "returning to a
healthy baseline." No pre-illness score reference exists. Cards must
frame the curve's best stretch as *lowest-burden period in the
tracked window*, never as *baseline* or *healthy*.

---

## 3. Design constraints (inherited, locked)

These are not invented for this plan; they are inherited project
rules every v1 surface must respect.

- **No em-dashes in UI copy.** Substitute comma, period, or colon.
- **Reflective Dutch tone** per the design brief. Restrained visual
  cues. Warm-earth palette. Humanist sans.
- **Things-3 anchor**: ambient, calm, doesn't demand attention.
  Cards present information; the user reads when they want.
- **Thumb-first for input surfaces** (today's log, score entry).
  Reading surfaces (trajectory, timeline, pacing-indicator cards)
  are free of that constraint.
- **Brainfog-friendly**: readable in seconds. No multi-paragraph
  walls.
- **WCAG 2.2 AA + Brainfog extensions.**
- **No prescription** ("rest more", "pace yourself", "today aim for
  ≤ 3 000 steps"). No causation claims.
- **"Stabilisation" not "recovery"** in copy.
- **No pre-illness anchor** — the curve's best stretch is "lowest-
  burden period in the tracked window," not "baseline" or "healthy."
- **Surfaces inform; they do not command or rank.** "vandaag was
  matig zwaar" reads as observation. "WAARSCHUWING: rust nemen"
  commands. Surfaces fall in the first category only.
- **Asymmetric error tolerance per family** (per
  [methodology piece](2026-06-07-research-to-app-methodology.md) §4):
  trajectory + events are low-stakes if framed honestly; biometric
  enrichment is medium-stakes; pre-emptive warnings are high-stakes
  and stay withheld.

---

## 4. The forbidden patterns (consolidated)

Convergent list from both source documents. These are surfaces that
would actively harm credibility or user experience; they are
*excluded* from the plan, not just *deferred*.

| Excluded surface | Why |
|---|---|
| Composite "crash risk %" / "PEM probability" number | No calibrated multi-day predictor exists. HA07d (the project's first overall-SUPPORTED test) yields a posterior of ~2.3% per fire against a ~1.7% base rate. Discrimination magnitudes ≠ predictive value. |
| Red/yellow/green traffic light implying certainty | Same problem in a different shape. Implies a decision the evidence cannot support. |
| Pre-emptive crash warning ("crash kan eraan komen") | Anxiety risk + habituation risk if false-alarms. Family 3b in the methodology piece — strong bias toward withhold. |
| Push notifications | Even well-meaning ones induce anxiety in PAIS patients and crowd the autonomic recovery these surfaces try to protect. Passive surfaces only. |
| Generic "recovery score" in Garmin / athletic-training framing | Recovery in athletic framing means muscular/cardiovascular adaptation; in PAIS framing it means autonomic recharge of an unstable envelope. Conflating them does damage. If a PAIS-specific recovery metric is built, it must be PEM-specific and clearly named. |
| Automated daily targets ("vandaag maximaal 3 000 stappen") | One step from a control-and-shame loop documented in the published literature on activity prescription in ME/CFS. Targets, if any, come from the patient. |
| Causal language ("because", "due to", "this caused") | No causal inference is supported by the current research. |
| Comparison to other users / populations | The project is n=1. No population claim is defensible. |
| Live biometric streaming | Out of scope for v1. |
| Badges, streaks, gamification | Things-3 style: app reflects the user's state, does not reward or punish. A "X days without a crash" streak makes the crash itself feel like a failure. |

These rules apply across all phases. Any new candidate card must be
checked against this list before scoping.

---

## 5. Phased plan

Phase numbering is the active version. Phase 1 is the v1 floor;
Phases 2-5 are progressive extensions; the Pending entry holds a
research-gated decision.

### Phase 1 — Score-only trajectory + events (the v1 floor)

**Goal**: a v1 surface the participant can live with. Two new
screens or screen-states, plus event markers on the existing
timeline.

#### 1.1 Trajectory card (single-axis, score-only)

A single card on a "trends" / "trajectory" screen, showing the 90-day
rolling score trajectory across the full tracked window. From
[S02](../garmin/hypotheses/S02-score-trajectory/notes.md).

- **Visual**: a single line (the 90-day rolling trimmed mean of
  `gevoelscore`), 1–6 y-axis, full tracked window x-axis.
- **Reference markers**: low-opacity vertical lines at LC diagnosis,
  tracking start, and (if the user wants) the analytical era
  boundary.
- **Crash + dip-cluster overlay**: three visual weight tiers per S02
  §3.7. Crash starts as filled triangles, cluster spans as shaded
  bands, singleton dips as low-opacity ticks.
- **Zoom strip**: last 6 months at finer resolution (per S02 §5.2),
  shown below or on-tap. The boundary-effect honesty the S02 spec
  calls for.
- **Status badge**: small text near the most recent anchor if a
  recent shift is detected.

**Copy examples** (Dutch, observational tone):
- Headline: "Je gevoel over tijd"
- Subtitle: "Hoe je dagen scoren, gemiddeld over 90 dagen"
- Recent change (if applicable): "De laatste maanden zijn iets
  zwaarder geweest dan in 2025."
- Caveat (always shown): "Dit is een terugblik. Geen voorspelling."

**What this card does NOT do:**
- Does not call any anchor "baseline" or "healthy."
- Does not predict the recent perturbation.
- Does not recommend any action.
- Does not claim causation for the arc shape.

#### 1.2 Event markers on the daily timeline

The existing daily-entry timeline gets two new marker types:

- **Crash episodes**: shaded bands or distinctive markers spanning
  the crash duration. Tappable.
- **Dips**: smaller, less prominent markers on single days.
  Tappable. Dip clusters render as wider spans.

Score-day markers are unchanged; the events are an overlay.

**Copy on marker tap:**
- Crash: "Crash van [start datum] tot [eind datum]. Klik voor
  details."
- Dip: "Een mindere dag. Klik voor context."
- Cluster: "Een ruwe periode van [N] dagen met meerdere mindere
  dagen."

#### 1.3 Per-crash detail view (score-only)

When the user taps a past crash from the timeline:

- **The crash itself**: score days, values, duration.
- **Recovery time**: how long until score returned to ≥ 4 for ≥ 2
  consecutive days. (Phase 1 uses a simple "first 2 consecutive ≥4
  days after the crash ended" rule. Replaceable with H05b's
  eventual definition once it lands.)
- **Comparison to typical**: descriptive only. "Most of your
  crashes have lasted 2–4 days; this one lasted [N]."
- **Notes from the day** (if logged): inline, if participant has
  opted in (see §9 open question about privacy).

**No biometric overlay in Phase 1.** Specificity checks haven't
landed. Adding biometric context now would either be undefensible
or risk anxiety. Phase 4 unlocks this conditionally.

**Copy examples:**
- Headline: "Crash van 27 maart tot 2 april"
- Recovery: "Je score was 4 dagen later weer rond je normale
  niveau."
- Comparison: "Korter dan veel van je eerdere crashes. Je gemiddelde
  van afgelopen jaar ligt rond 2 a 3 dagen."

#### Phase 1 gates

| Gate | Pass condition |
|---|---|
| G1 research bar | n/a — descriptive only |
| G2 specificity | n/a |
| G3 posterior | n/a |
| G4 family | Families 1 + 2 |
| G5 threshold | Low-stakes; cleared |
| G6 framing | Observational, reversible, anxiety-bounded — needs copy review |
| G7 anxiety/burden | Needs participant judgement |
| G8 calibration | Log how often the user taps each surface; iterate |
| G9 ship | Ready when G6 + G7 land |

#### Phase 1 deliverables

- A copy doc (Dutch) with every UI string written and reviewed.
- A simple wireframe of the trajectory card and timeline markers.
- A "what NOT to show" list embedded in the spec (forbidden
  patterns from §4).

---

### Phase 2 — Multi-axis trajectory + descriptive enrichment

**Goal**: deepen the trajectory story with the multi-axis evidence
the project has accumulated. Add a recovery-distribution descriptive
piece to the per-crash detail.

#### 2.1 Multi-axis stabilisation arc

Extends the Phase 1 trajectory card with optional additional
trajectories from [S01](../garmin/hypotheses/S01-stabilisation-trajectories/notes.md):

- Score trajectory (already shown in Phase 1).
- Average stress trajectory.
- Max stress-spike duration trajectory.
- Crash frequency per year.

Each as a small thumbnail or as toggleable overlays. Per S01 + S02,
a normalised "recovery direction" view ([S02 §5.2a](../garmin/hypotheses/S02-score-trajectory/notes.md))
makes lead/lag visually inspectable.

**Important framing constraint from S02b:** the trajectory-level
lead pattern (score peaks ~5 months before stress) was tested at
daily resolution in [S02b](../garmin/hypotheses/S02b-score-lead/notes.md)
and REFUTED. **The card must NOT be copy-written as "your score
predicts your biometrics."** Honest framing: "Hoe je gevoel, je
stress en je crash-frequentie samen bewegen over de jaren — alle
assen vertellen ongeveer hetzelfde verhaal, maar elk op zijn eigen
tempo."

**Copy examples:**
- "Alle assen vertellen ongeveer hetzelfde verhaal: minder
  intensiteit, meer rust."
- Recent perturbation (if applicable, framed via
  [S02c](../garmin/hypotheses/S02c-may2026-divergence/notes.md)
  recent-baseline reading): "De laatste maanden zien we een lichte
  stijging in je hartslag in rust. De andere assen bewegen
  vergelijkbaar met de afgelopen zes maanden."

#### 2.2 Recovery-distribution descriptive card

On the per-crash detail view, add a small descriptive card showing
the empirical distribution of past crash durations.

- Histogram or small distribution plot.
- "Most of your crashes have lasted 2-4 days. The longest was
  [N] in [year]."
- For the current crash, show where it falls in the distribution.

**This is NOT a recovery-time prediction.** It is a descriptive
characterisation of past crashes, presented for the user's own
reference. Family 4 (recovery indicators) is the predictive version
and waits for H05b.

#### 2.3 Yearly crash count

A simple bar or step display of crashes per year. From the
preflight [00-crash_v1-counts](../garmin/hypotheses/00-crash_v1-counts/counts.md).

- "2023: 9 crashes; 2024: 11; 2025: 2; 2026: 2 so far."
- Optionally dip count alongside: "Plus [N] mindere dagen per jaar."

#### Phase 2 gates

Same as Phase 1. Additional content increases copy-review surface at
G6 but doesn't change gate-pass logic.

---

### Phase 3 — Daily pacing indicators (NEW; from the pacing-indicators piece)

**Goal**: surface the Tier 1 indicators from the original
pacing-indicators document as daily-overview cards. These compose
into the "today's overview" reading surface, separate from the
trajectory + events reading surface.

The indicators below have direct research support from pre-registered
tests. They are passive, glanceable, retrospective, and explicitly
event- or fact-based (not predictive percentages).

#### 3.1 Daily exertion class (Tier 1, the anchor)

**What it is.** A five-level classification of today's overall
exertion: `none / light / moderate / heavy / very_heavy`. Computed
from a composite percentile rank over four axes (effective
intensity-minutes, total steps, daily-max HR, vigorous minutes),
each ranked within a 30-day rolling baseline of the *same* person.

**Research support.** The validate-era pre-registered test
([HA01b](../garmin/activity-labels/output/ha_results_4day.md)) showed
that the presence of a `heavy` or `very_heavy` day in the 4-day
window before a crash discriminates crash days from baseline days by
**+17.3 percentage points**. First SUPPORTED validate-era precursor
in the investigation. Sensitivity-tested ROBUST across 13 parameter
variations (Jaccard ≥ 0.7).

> **Caveat from Theme A** ([../garmin/activity-labels/output/ha_results_4day_lagged.md](../garmin/activity-labels/output/ha_results_4day_lagged.md)):
> on the A.1 lagged baseline, HA01b-recomputed dropped to +4.0 pp
> validate (refuted). The original +17.3 pp finding was substantially
> a rolling-baseline construction artifact. The descriptive exertion
> class still presents an honest fact-about-today — but the
> precursor framing was downgraded. App copy must NOT imply the
> exertion class is predictive of crashes; it is a descriptive
> read of today's exertion against the participant's recent baseline.

**App implementation.** Single-line reading card:

```
vandaag
[ . . . . . ] matig zwaar
```

Five dots, three filled. No number. No score. Compact enough for
the daily overview; sits next to the gevoelscore so the user sees
the *felt* score and the *measured* exertion class side by side.

For the timeline view: render the class as a small coloured bar
under each day, warm-earth palette graded from sand → terracotta.

#### 3.2 Daily stress-spike event marker (Tier 1)

**What it is.** A binary event marker: did today's single highest
minute of HR-derived stress exceed the personal H02b threshold?
Garmin's per-minute stress (0-100, computed from HRV) gives one value
per minute; this indicator triggers on the daily maximum exceeding
a learned personal threshold.

**Research support.** Multiple pre-registered SUPPORTED tests in
train-era (H02b at 3d, H02d bridge × 5d, HA06b nightly RHR z-score
4d, HA11 within-day U-dip z-score 4d, HA07c/d sleep-stress
primitives at 4d), one in validate-era (HA10 morning BB peak),
and **HA07d SUPPORTED in BOTH eras** under v2 rescue criteria.
Full era-shift framing in [synthesis.md](../garmin/hypotheses/synthesis.md).

**App implementation.** A small marker, only shown when the day's
max-stress exceeds the personal threshold. Event, not gauge:

```
vandaag was er een acute stresspiek
```

One sentence. Optional: a small icon on the timeline day-marker.
**Avoid any continuous "stress level" gauge** — the daily-max-spike
is binary in its information content.

Past-tense only. Phase 3 surfaces this on the daily overview the
same day; Phase 4 retrospective enrichment surfaces this in the
per-crash detail view for past crashes.

#### 3.3 Dip-cluster proximity (Tier 2, passive context)

**What it is.** A flag: are you currently inside a 7-day window
after a recent crash or dip cluster?

**Research support.** Descriptive only (crash_v2 cluster analysis).
We have not tested whether cluster-proximity predicts the next
crash — only observed that crashes and dips arrive in clusters more
often than in isolation. 45 of 79 dips chain into 15 clusters under
the 7-day proximity rule.

**App implementation.** A subtle background tint on the daily card
if today is within 7 days of a recent dip, with hover/expand text:

```
5 dagen na een dip
```

Easy to ignore when not relevant; visible when the user looks for
why a day feels harder.

#### Phase 3 gates

| Gate | Pass condition |
|---|---|
| G1 research bar | HA01b (descriptive read still robust per sensitivity test) + H02b retrospective (train, SUPPORTED) |
| G2 specificity | Not required for descriptive cards; required for any "predict-shaped" framing |
| G3 posterior | n/a — cards are descriptive, not predictive |
| G4 family | Pacing indicators (between Family 1 and Family 3a) |
| G5 threshold | Medium; framing discipline matters |
| G6 framing | Past-tense for stress-spike marker; present-tense observational for exertion class |
| G7 anxiety/burden | Needs participant judgement on whether the exertion-class card adds value or pressure |
| G8 calibration | Log surface tap-rates; iterate |
| G9 ship | Conditional on Phase 1 shipping cleanly first |

#### Phase 3 deliverables

- A copy doc (Dutch) with strings for each of 3.1, 3.2, 3.3.
- The Theme-A caveat baked into 3.1's framing review.
- Sensitivity-tested colour palette for the exertion-class dot
  visualisation.

---

### Phase 4 — Retrospective biometric enrichment of past crashes (conditional on v2 outcomes + specificity)

**Goal**: where the research now supports it, add retrospective
biometric context to past crashes. Carefully, with strict gates.

This phase was Phase 3 in the original
trajectory-and-events plan; renumbered Phase 4 to follow the daily
pacing indicators (Phase 3) which depend on neither v2 nor
specificity work.

**Conditional on:**
1. v2 threshold-sweep diagnostics complete on HA07d / HA10 / HA06b /
   HA11. **Status as of 2026-06-07**: v2 round HAS run; HA07d both
   eras RESCUE; HA10 validate RESCUE; HA11 train RESCUE; HA06b
   permanently CLOSED. So the v2 condition is now MET in part
   (HA07d + HA10 + HA11 carry forward; HA06b is permanently demoted
   from load-bearing status).
2. **Specificity checks** complete on whichever findings survive
   v2. *Status: pending.* This remains the binding gate.
3. Posterior-probability computation per family-3a evidence threshold
   from the [methodology piece](2026-06-07-research-to-app-methodology.md).

Without specificity checks + posterior numbers, **Phase 4 should
NOT ship** in v1. The v2 outcome alone is not sufficient.

#### 4.1 Train-era retrospective enrichment (conditional)

For crashes in the train era (pre-2024), if the H02b train-era
per-minute stress spike finding clears all gates:

- On per-crash detail: small descriptive note.

```
In de drie dagen voor deze crash was er een ongewone stresspiek
van [N] minuten op [dag]. Dat patroon hebben we vaker gezien voor
jouw crashes uit die periode.
```

**Strict framing rules:**
- Past-tense only.
- Cite the research provenance where appropriate ("Onderzoek wijst
  op een verband, maar dat is geen voorspelling.").
- Withhold for any crash where the specificity check showed the
  pattern was equally present in surrounding non-crash days.

#### 4.2 Validate-era retrospective enrichment (conditional on v2 RESCUE + specificity)

For crashes in the validate era (2024+), if HA07d v2 RESCUE +
specificity check both support:

- On per-crash detail: descriptive note about the autonomic-
  swing pattern.

```
In de nachten voor deze crash zagen we een patroon dat onderzoekers
beschrijven als een soort "freeze": het lichaam ziet er uitgerust
uit, maar het herstel valt anders uit dan verwacht.
```

- Cite Wiggers: "Dit type patroon is in onderzoek (Wiggers et al.)
  beschreven."

HA10 corroborates HA07d in validate-era and may also surface where
specificity supports.

If v2 RESCUE outcomes do not pair with specificity-check support,
**no validate-era enrichment in v1**. The validate-era retrospective
surface stays score-only.

#### 4.3 Cross-era awareness

Whichever crashes get biometric overlay should carry an explicit
era-context note:

```
Dit patroon was vooral zichtbaar in jouw eerdere crashes
(2022–2023). In jouw recentere crashes zien we andere patronen.
```

Per the project's locked era-shift framing.

#### Phase 4 gates (stricter)

| Gate | Pass condition |
|---|---|
| G1 research bar | v2 RESCUE for the relevant finding ✓ for HA07d, HA10, HA11; ✗ permanently for HA06b |
| G2 specificity | Specificity check completed; FPR < locked threshold. **Currently pending.** |
| G3 posterior | P(crash window \| pattern present) at era's base rate computed. **Currently pending.** |
| G4 family | Family 3a retrospective |
| G5 threshold | Family 3a evidence threshold from methodology piece |
| G6 framing | Past-tense, observational, era-specific, anxiety-bounded |
| G7 anxiety/burden | Participant judgement on whether they want this |
| G8 calibration | Log card-fire correctness over time |
| G9 ship | All previous gates pass |

---

### Phase 5 — Stabilisation milestones + reflection-tier indicators

**Goal**: surface specific factual milestones (descriptive only) and
provide deeper-tier indicators for reflection/review screens.

This phase is **not conditional on any pending research**; it can
ship alongside Phase 1 or 2.

#### 5.1 Milestone cards (retrospective, factual)

Small cards that appear on the trajectory screen when specific
data-driven milestones are passed:

- "Een jaar geleden was je gemiddelde [N]; nu is het [M]."
- "Je had [N] crashes in 2023, [M] in 2025."
- "Je langste crash duurde [N] dagen. Je laatste 5 crashes duurden
  gemiddeld [M]."
- "Het aandeel van slechte dagen (score 1-3) is gedaald van 20%
  naar 7% sinds je begon te loggen." (From S02 distribution
  finding.)
- "Score-6 dagen waren 2% van je weken; nu zijn ze 12%." (From
  S02 emergence-of-upper-mode finding.)
- (Conditional on S02 T4) "Je dagen worden gemengder. Je hebt nog
  steeds slechte dagen, maar minder vaak hele weken aan een stuk."

#### 5.2 The dip-cluster "rough patch" view

For the 15 identified dip clusters, a small descriptive view:

```
Tussen [start] en [eind] had je [N] mindere dagen verspreid over
[M] dagen. Een ruwe periode.
```

Optional: notes from those days inline (privacy-gated per §10).

#### 5.3 Effective exertion percentile rank (Tier 2, detail-view content)

The single-axis percentile rank of today's `effective_exertion_min`
within the personal 30-day baseline. Number from 0 to 100.

Surfaced as a *tooltip* or detail-view expansion on the exertion-
class card from 3.1: "vandaag: 78ste percentiel in jouw 30-daagse
venster voor effective intensity-minutes." Drill-in detail without
daily-overview clutter.

#### 5.4 Personal-baseline z-score (Tier 2, reflection-only)

Today's effective-exertion deviation from 30-day rolling baseline,
expressed as a z-score. NOT surfaced on the daily card; surfaced on
weekly/monthly review screens as a chart of 30 days of z-scores
with ±2 σ bands marked.

A reflection tool, not a daily-pacing one.

---

### Pending — 7-day push burden (descriptive shape, awaiting further research)

The original
[pem-pacing-indicators](_archive/pem-pacing-indicators.md) §3.2
proposed shipping a 7-day push-burden count as a descriptive card
("3 zware dagen, jouw mediaan is 1"). The original
[trajectory-and-events-app-plan](_archive/2026-06-07-trajectory-and-events-app-plan.md)
§4 excluded all push-pattern surfaces (Family 6) on the grounds that
any push-pattern card risks being read as a predictive warning
regardless of framing.

The disagreement is substantive. **This plan defers the decision
pending pre-registered research on the framing question.**

**Status**: PENDING — awaiting pre-registered participant evaluation.

**Open research question to pre-register before shipping:**

> Does a descriptive push-burden card, framed as a fact-with-context
> ("deze week: 3 zware dagen, jouw mediaan is 1") and explicitly
> labelled non-predictive, produce different user response than a
> predictive alert? Specifically: does it (a) accurately inform the
> participant about sustained-load patterns without inducing anxiety,
> (b) anchor the participant's pacing decisions in helpful ways, or
> (c) function as an implicit warning regardless of framing?

**Why this is research-gated:**
- The statistical case for push burden is asymmetric. The
  *predictive* test ([HA02 / HA02c](../garmin/activity-labels/output/ha_results_4day_lagged.md))
  was REFUTED on both rolling and lagged baselines. The
  *descriptive* sensitivity test (whether the raw count varies
  meaningfully with the participant's own median) was ROBUST.
- A's argument: a descriptive fact-card differs categorically from
  a predictive alert; the same number can be ethically shipped as
  the first but not the second.
- B's argument: PAIS patients reading any push-pattern surface may
  interpret it as a warning regardless of framing; framing
  discipline alone is insufficient guarantee.

Both arguments are defensible. The empirical question (does the
framing actually produce different participant behaviour?) is a
small participant-evaluation study, not a statistical test on the
biometric data. **Pre-register the protocol before shipping the
card; do not ship the card without the protocol's outcome.**

**Recommended study shape** (sketch, not locked):
- Show three variants of the card to the participant on different
  days (descriptive-fact / predictive-alert / no-card) and collect
  same-day score + tag data.
- Compare same-day score impact and self-report on anxiety / pacing
  decision quality.
- N is small (single participant), so this is a within-subject
  qualitative evaluation, not a power-calibrated trial.

**Until this lands**: do not ship a push-burden card in any form.
Push burden remains available as a research-side metric for
diagnostic work; it does not surface to the user.

---

## 6. Cross-cutting decisions for v1

### 6.1 Default opt-out for biometric enrichment

If Phase 4 ships, biometric overlay on per-crash detail defaults to
**off**. The user opts in once, with a short explanation:

> "Wil je dat we, waar mogelijk, naast jouw eigen score ook
> patronen uit je horloge laten zien bij oude crashes? Dat is
> beschrijvend, geen voorspelling."

If they opt in, the overlay appears for crashes where the gates
pass. They can opt out again at any time.

### 6.2 No badges, no streaks, no gamification

Things-3 style: the app reflects the user's state, doesn't reward
or punish. No "X day streak without a crash."

### 6.3 Honest empty states

Where the data doesn't yet support a surface, show honest empty
states, not placeholders:

- "We hebben nog niet genoeg data om jouw typische crash-duur te
  schatten. Komt later."
- "Jouw trajectory wordt zichtbaar zodra je 12 maanden hebt
  gelogd."
- "Voor crashes uit de afgelopen 2 jaar hebben we nog geen
  betrouwbaar patroon kunnen vaststellen. Dit blijft beschrijvend
  voor nu."

These are arguably the most important strings in the app. They
communicate the project's honesty discipline directly to the user.

### 6.4 Calibration logging from day one

Every card surface logs:
- When it appeared.
- Whether the user tapped it.
- Whether they dismissed it.
- (For event-based surfaces): whether the next 14 days showed any
  event that the surface implied.

Gate G8 from the methodology workflow. For the v1-vs-v1.5 iteration
loop, not for product analytics. A card that nobody taps after the
first month should probably be removed.

### 6.5 Era-aware surfacing

Any retrospective view that uses era-specific findings should let
the user see which era the surface is contextualising (visual or
textual: "Patroon voor crashes uit 2022–2023") so they understand
the surface is era-bounded, not universal.

### 6.6 Composition principles for the reading surfaces

The indicators across all phases compose into roughly three reading
surfaces:

| Surface | Purpose | Phases that feed it |
|---|---|---|
| Today's overview | Glance: where am I now | Phase 3 (exertion class, stress-spike marker, cluster proximity) |
| Trajectory / trends | Long-arc reflection | Phase 1 (single-axis), Phase 2 (multi-axis), Phase 5 (milestones) |
| Per-crash detail | Retrospective on a specific past event | Phase 1.3 (score-only), Phase 2.2 (recovery distribution), Phase 4 (biometric enrichment, conditional) |

The reading surfaces are *reading*, not input. They do not need to
obey the thumb-first input-zone rule (which governs score / note /
tag entry surfaces).

---

## 7. Suggested order of delivery

1. **Phase 1 first** (score-only trajectory + event markers +
   per-crash detail). Ships independently of any pending research.
2. **Phase 5 milestones** in parallel with or shortly after Phase 1.
   Same descriptive material; small additional cards.
3. **Phase 3 daily pacing indicators** when Phase 1 has bedded in
   and participant judgement on §10 open questions has landed.
   Daily exertion class is the priority indicator; stress-spike
   marker and dip-cluster proximity follow.
4. **Phase 2** when there's design capacity for the multi-axis
   trajectory view.
5. **Phase 4** when v2 + specificity checks complete (v2 is done;
   specificity pending). Conditional ship.
6. **Pending push-burden** ships only after its pre-registered
   participant-evaluation study returns a clear answer.

**Phase 1 + Phase 5 are the v1 floor.** Phase 3 is the high-value
extension once Phase 1 has bedded in. Phase 2 is the v1 stretch
goal. Phase 4 is the v1.5 candidate.

---

## 8. Honest caveats

- **n=1 evidence.** Every indicator and finding above was developed
  against a single participant's data. The *framework*
  (baseline-relative, multi-axis, percentile-rank, locked-bar
  pre-registration) should transfer; specific cutoffs almost
  certainly should not.
- **Era split is real but framed analytically.** The train/validate
  split is at 2023-12-31. It was revised mid-preflight from
  time-proportional to episode-balanced. Both halves clear 10
  episodes. The split is an analytical convenience, not a
  physiological boundary. The stabilisation trajectory is smooth,
  not a cliff (per S01 + S02).
- **No medical advice.** These surfaces are awareness signals; they
  do not replace clinical assessment, do not prescribe behaviour,
  and are not validated for clinical use.
- **Pending work.** Sleep-recharge / parasympathetic-recovery
  indicators (overnight Body Battery, per-minute HRV) are gated on
  H04b decoding. Until then, the parasympathetic side of the PAIS
  picture is not surfaced as a Tier 1 daily indicator.
- **Dataset window ends 2026-06-05.** Anyone re-running the
  analyses against a later window will find different cutoffs as
  the rolling baseline shifts.
- **S02b refuted the daily-resolution score-leads-Garmin pattern.**
  The trajectory-level lead is a real description of the rolling
  curves; the card must not present it as a daily-level predictive
  relationship.

---

## 9. What this plan deliberately does NOT include

(Already enumerated in §4 as the forbidden patterns, but
re-stated here as a checklist applied to the merged plan
specifically.)

| Excluded surface | Why |
|---|---|
| Pre-emptive crash warning ("crash kan eraan komen") | Family 3b — no finding meets posterior threshold. |
| Push-pattern alert (any form) | Pending the §5 Pending research question. Until that lands, no push-pattern card ships. |
| "You may crash soon" cards | Anxiety risk, no evidence base. |
| Causal language | No causal inference is supported. |
| Comparison to other users / populations | n=1; no population claim. |
| Numeric "recovery probability" / "crash risk %" | Would require a model the project does not have. |
| Live biometric streaming | Out of scope for v1. |
| Push notifications about any of the above | Anxiety risk + user-burden + opt-in complexity. |
| Badges, streaks, gamification | Things-3 anti-pattern. |
| Generic athletic-framed "recovery score" | Conflates PAIS recovery with athletic recovery; does damage. |

---

## 10. Open questions for the participant

Decisions only the participant can make. The methodology binds at G7
(anxiety/burden review) — surfaces only ship if the participant
wants them as designed.

1. **Naming**: "crashes" / "rough patches" / "moeilijke periodes" /
   participant's own term?
2. **Whether to surface the train/validate era split at all** in
   UI, or to handle it silently in the background.
3. **Whether the trajectory screen is a dedicated tab**, a section
   of an "insights" screen, or accessed from long-press on the
   timeline.
4. **Whether dip clusters should be surfaced as their own concept**
   ("ruwe periode") or only implicitly via the visual overlay.
5. **Whether the per-crash detail should auto-expand on the most
   recent crash** or always require an explicit tap.
6. **Whether notes from past crash days should be shown in the
   per-crash detail** or kept private (privacy risk: a clinician
   or family member glancing at the screen).
7. **Push-burden research question** (per §5 Pending): does the
   participant want to participate in the small framing-vs-no-card
   evaluation study?
8. **Phase 3 daily exertion class** (per §5.1): does the participant
   want a glanceable measure of today's exertion on the daily
   overview, or does that pressure rather than inform?

Questions 1-6 are inherited from the original Families 1+2 plan.
Questions 7-8 are new from the merge.

These shouldn't block Phase 1 design but should be answered before
the corresponding phase ships.

---

## 11. Bottom line

The research project has produced enough material to ship a
defensible, useful v1 right now, *without* the pre-emptive warning,
push-pattern alert, or recovery-probability surfaces the project
originally hoped for.

The v1 surfaces — score trajectory + events + descriptive
milestones (Phase 1 + 5) plus daily exertion class + stress-spike
marker + dip-cluster proximity (Phase 3) — are the ones the
participant will touch most often anyway.

The honest framing is: this is **not** a "crash predictor" app. It
is an app that helps the participant see their own data clearly, in
calm reflective Dutch, with respect for what the research can and
cannot say. That is a smaller product than the original ambition.
It is also the product the data actually supports.

The discipline that has run the research side is what carries into
the product side. Ship what you can defend. Withhold what you
can't. Calibrate as you go.

---

## 12. References and provenance

### Research findings underpinning each phase

- **Phase 1 trajectory + events**:
  [S02 score trajectory](../garmin/hypotheses/S02-score-trajectory/notes.md),
  [crash_v2 definition](../garmin/hypotheses/crash_v2-definition/definition.md),
  [00-crash_v1-counts preflight](../garmin/hypotheses/00-crash_v1-counts/counts.md).
- **Phase 1 trajectory framing constraints**:
  [S02b refuted daily-resolution lead](../garmin/hypotheses/S02b-score-lead/notes.md),
  [S02c characterised recent perturbation](../garmin/hypotheses/S02c-may2026-divergence/notes.md).
- **Phase 2 multi-axis**:
  [S01 Garmin pendulum](../garmin/hypotheses/S01-stabilisation-trajectories/notes.md),
  [K01 + K02 era shifts](../garmin/hypotheses/K01-crash-depth/result.md).
- **Phase 3 daily exertion class**:
  [HA01b 4-day window](../garmin/activity-labels/output/ha_results_4day.md),
  with Theme A caveat from
  [HA01b-recomputed lagged](../garmin/activity-labels/output/ha_results_4day_lagged.md).
- **Phase 3 stress-spike marker**:
  [H02b](../garmin/hypotheses/H02b-stress-spikes/result.md),
  [H02d](../garmin/hypotheses/H02d-stress-spikes-uncensored/result.md),
  [HA07d](../garmin/hypotheses/HA07d-sleep-stress-variability/hypothesis.md),
  [HA10](../garmin/hypotheses/HA10-bb-overnight-recharge/result.md),
  [HA11](../garmin/hypotheses/HA11-stress-udip/result.md),
  [HA06b](../garmin/hypotheses/HA06b-rhr-zscore/result.md).
- **Phase 4 retrospective biometric enrichment**:
  same as Phase 3 + the v2 threshold-monotonicity diagnostic round
  outcomes documented in [Wiggers progress map](../wiggers_progress_2026-06-07.md).
- **Phase 5 stabilisation milestones**:
  [S02 distribution findings](../garmin/hypotheses/S02-score-trajectory/notes.md),
  [00-crash_v1-counts](../garmin/hypotheses/00-crash_v1-counts/counts.md).

### Methodology + framework

- [research-to-app methodology piece](2026-06-07-research-to-app-methodology.md)
  — evidence framework, family asymmetries, posterior-probability
  bottleneck, gate definitions.
- [registry](../garmin/hypotheses/registry.md) — full registry of
  pre-registered hypotheses.
- [synthesis.md](../garmin/hypotheses/synthesis.md) — cross-batch
  synthesis, the latest entry covering S02/S02b/S02c integration.
- [STOCKTAKE.md](../STOCKTAKE.md) — running stocktake of what has
  been tested, supported, refuted, and queued.
- [Wiggers progress map](../wiggers_progress_2026-06-07.md) — map of
  Wiggers' testable hypotheses against project tests.

### Archived source documents

This plan merges and supersedes:
- [_archive/pem-pacing-indicators.md](_archive/pem-pacing-indicators.md)
  (research-side curated indicators).
- [_archive/2026-06-07-trajectory-and-events-app-plan.md](_archive/2026-06-07-trajectory-and-events-app-plan.md)
  (Families 1+2 app plan).

Both archived 2026-06-07. Content preserved verbatim for audit-trail
continuity.

---

*Active product plan as of 2026-06-07. Living document; updates
follow research outcomes. To be moved to `docs/features/` or
`docs/design/` if a feature owner picks up Phase 1 implementation.*
