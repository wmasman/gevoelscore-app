> **ARCHIVED 2026-06-07 (same day as written).** This document has
> been **superseded by [app-plan.md](../app-plan.md)** (the merged
> active product plan combining this piece with the pacing-indicators
> piece). Content preserved verbatim below for audit-trail continuity.
> Do not edit; update the merged plan instead. The methodology piece
> referenced below remains active at its original path.

---

# App plan — trajectory + events (Families 1 + 2)

*Independent reviewer-agent piece, 2026-06-07. A concrete plan for
how the app could surface trajectory (Family 1) and events (Family 2)
based on the current research findings. Companion to
[the research-to-app methodology piece](../2026-06-07-research-to-app-methodology.md).
Status: draft for review. To be moved to `docs/features/` or
`docs/design/` if the project picks it up.*

---

## 1. Why these two families first

From the methodology piece: of the six indicator families, only Families 1
(trajectory) and 2 (event surfacing) clear all the gates for v1
shipping. Families 3a, 4, 5 need one round of additional research work
each. Families 3b and 6 should not ship in v1 at all.

The good news: Families 1 and 2 are the two families that touch the
participant *most often*. Every time the app is opened, the user can
see today's score and recent timeline. Every time they look back, they
can see the long arc. These are the two surfaces the participant lives
with — not the pre-emptive warning they (and we) wish we could ship.

The research material supporting these families is substantial and
already mostly in hand:

| Source | What it gives | Ready? |
|---|---|---|
| S01 stabilisation trajectories | 90-day rolling Garmin curves (stress, RHR, sleep eff, max-spike) | ✓ Done |
| S02 score trajectory | 90-day rolling score (mean, median, distribution) + zoom strip | Landing |
| K01 crash depth | Late crashes shallower (no 1's) | ✓ Done |
| K02 crash duration | Late crashes shorter; long-crash tail collapsed | ✓ Done |
| crash_v2 / dip clusters | 29 crashes + 79 dips + 15 clusters with overlay | ✓ Done |
| 00-crash_v1-counts | Yearly counts (10/year → 2/year) | ✓ Done |
| Notes language analyses | Distribution shifts in symptom severity, day topology, lead-up language | ✓ Done |

What is NOT yet in hand and would gate Phase 3 surfaces:

| Missing piece | What it gates |
|---|---|
| v2 threshold-sweep diagnostics on HA07d/HA10/HA06b/HA11 | Whether biometric enrichment can use validate-era findings |
| Specificity checks on the SUPPORTED autonomic-channel findings | Whether retrospective biometric overlays can ship at all |
| H05b sustained-recovery target | Recovery-indicator surfaces (Family 4, not part of this plan but adjacent) |
| Crash_v3 mechanism subtyping | Per-crash mechanism labels in the retrospective view |

---

## 2. Design constraints carried in from CLAUDE.md + memory

These are not invented for this plan; they're inherited project rules
the v1 surfaces must respect:

- **No em-dashes in UI copy.** Substitute comma, period, or colon.
- **Reflective Dutch tone** per the design brief. Restrained visual
  cues. Warm-earth palette, humanist sans.
- **Things-3 anchor**: ambient, calm, doesn't demand attention.
  Cards present information; the user reads when they want.
- **Thumb-first for input surfaces** (today's log, score entry).
  Reading surfaces (trajectory, timeline) are free of that
  constraint and can use the full viewport.
- **Brainfog-friendly**: readable in seconds. No multi-paragraph
  walls.
- **WCAG 2.2 AA + Brainfog extensions.**
- **No prescription** (no "rest more" / "pace yourself"). No
  causation claims.
- **"Stabilisation" not "recovery"** in copy.
- **No pre-illness anchor** — frame the curve's best stretch as
  "lowest-burden period in the tracked window," not as "baseline" or
  "healthy."
- **Asymmetric error tolerance per family** (from the methodology
  piece). For Family 1: low stakes if wrong, framing matters more
  than statistics. For Family 2: score-defined event has zero
  inference; biometric enrichment is decorative.

---

## 3. Phased plan

### Phase 1 — Minimum viable trajectory + events

**Goal**: a v1 surface the participant can actually live with. Two
new screens or screen-states, plus event markers on the existing
timeline.

**Surfaces:**

#### 1.1 Trajectory card (single-axis, score-only)

A single card on a "trends" or "trajectory" screen, showing the
participant's 90-day rolling score trajectory across the full
tracked window. From S02.

- **Visual**: a single line (the 90-day rolling trimmed mean of
  gevoelscore), 1–6 y-axis, full tracked window x-axis.
- **Reference markers**: small vertical lines at LC diagnosis,
  tracking start, and (if the user wants) the analytical era
  boundary. Quiet, low-opacity.
- **Crash + dip-cluster overlay**: small markers on the bottom
  margin (three visual weight tiers per S02 §3.7). Crash starts as
  filled triangles, cluster spans as shaded bands, singleton dips
  as low-opacity ticks.
- **Zoom strip**: last 6 months at finer resolution (per S02 §5.2
  zoom strip), shown below or on-tap. The boundary-effect honesty
  the S02 spec calls for.
- **Status badge**: small text near the most recent anchor
  indicating "recent change" if S02 detects it.

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

The existing daily-entry timeline (per the daily-entry feature
folder) gets two new marker types:

- **Crash episodes**: shaded bands or distinctive markers spanning
  the crash duration. Tappable to drill into the per-crash detail
  (1.3).
- **Dips**: smaller, less-prominent markers on single days.
  Tappable. Dip clusters render as a wider span.

Score-day markers are unchanged; the events are an overlay.

**Copy on marker tap:**
- Crash: "Crash van [start datum] tot [eind datum]. Klik voor
  details."
- Dip: "Een mindere dag. Klik voor context."
- Cluster: "Een ruwe periode van [N] dagen met meerdere mindere
  dagen."

#### 1.3 Per-crash detail view (score-only)

When the user taps a past crash from the timeline, they see:

- **The crash itself**: the score days, their values, the duration.
- **Recovery time**: how long until the score returned to ≥ 4 for
  ≥ 2 days. (Uses H05b's eventual definition once it lands; for
  v1 a simple "first 2 consecutive ≥4 days after the crash ended"
  works.)
- **Comparison to typical**: descriptive only. "Most of your crashes
  have lasted 2–4 days; this one lasted [N]."
- **Notes from the day** (if the user logged any): show inline.

**No biometric overlay in Phase 1.** Specificity checks haven't
landed and v2 diagnostics are pending. Adding biometric context now
would either be undefendable or risk anxiety induction. Phase 3
unlocks this conditionally.

**Copy examples:**
- Headline: "Crash van 27 maart tot 2 april"
- Recovery: "Je score was 4 dagen later weer rond je normale niveau."
- Comparison: "Korter dan veel van je eerdere crashes. Je gemiddelde
  van afgelopen jaar ligt rond 2 a 3 dagen."

**What this view does NOT do (yet):**
- No biometric overlay (Phase 3).
- No mechanism label (gated on crash_v3).
- No comparison to specific past crashes by name/date.

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
- A "what NOT to show" list embedded in the spec (explicit forbidden
  patterns).

---

### Phase 2 — Multi-axis trajectory + descriptive enrichment

**Goal**: deepen the trajectory story with the multi-axis evidence
the project has accumulated. Add a recovery-distribution descriptive
piece on per-crash detail.

**Surfaces:**

#### 2.1 Multi-axis stabilisation arc

Extends the Phase 1 trajectory card with optional additional
trajectories from S01:

- Score trajectory (already shown in Phase 1).
- Average stress trajectory.
- Max stress-spike duration trajectory.
- Crash frequency per year.

Each as a small thumbnail or as toggleable overlays. The user can
choose which axes to show. Per S01 + S02: a normalised "recovery
direction" view makes lead/lag visually inspectable.

**Copy examples:**
- "Hoe je gevoel, je stress en je crash-frequentie samen bewegen
  over de jaren."
- "Alle assen vertellen ongeveer hetzelfde verhaal: minder
  intensiteit, meer rust."
- Recent perturbation (if applicable): "De laatste maanden zien we
  een lichte stijging op een paar metingen. De moeite van het
  weten waard."

#### 2.2 Recovery-distribution descriptive card

On the per-crash detail view, add a small descriptive card showing
the empirical distribution of the user's crash durations.

- Histogram or small distribution plot of past crash spans.
- "Most of your crashes have lasted 2–4 days. The longest was
  [N] in [year]."
- For the current crash, show where it falls in the distribution.

**This is NOT a recovery-time prediction.** It's a descriptive
characterisation of past crashes, presented for the user's own
reference. Family 4 (recovery indicators) is the predictive version
and waits for H05b.

#### 2.3 Yearly crash count

A simple bar or step display of crashes per year. From
00-crash_v1-counts.

- "2023: 9 crashes; 2024: 11; 2025: 2; 2026: 2 so far."
- Optionally dip count alongside: "Plus [N] mindere dagen per jaar."

#### Phase 2 gates

Same gates as Phase 1. All descriptive; no inference. The
additional content increases the surface area for copy review at
G6 but doesn't change the gate-pass logic.

---

### Phase 3 — Biometric enrichment of events (conditional on v2)

**Goal**: where the research now supports it, add retrospective
biometric context to past crashes. Carefully, with strict gates.

This phase is **conditional** on:

1. v2 threshold-sweep diagnostics complete on HA07d, HA10, HA06b,
   HA11.
2. Specificity checks complete on whichever findings survive v2
   RESCUE.
3. Posterior-probability computation per family-3a evidence
   threshold from the methodology piece.

Without those, Phase 3 should NOT ship.

**Surfaces (conditional):**

#### 3.1 Train-era retrospective enrichment

For crashes in the train era (pre-2024), if the H02b train-era
per-minute stress spike finding clears all gates:

- On per-crash detail: small descriptive note. "In de drie dagen
  voor deze crash was er een ongewone stress-piek van [N] minuten
  op [dag]. Dat patroon hebben we vaker gezien voor jouw crashes
  uit die periode."

Strict framing rules:
- Past-tense only.
- Cite the research source where appropriate ("Onderzoek wijst op
  een verband, maar dat is geen voorspelling.").
- Withhold for any crash where the specificity check showed the
  pattern was equally present in surrounding non-crash days.

#### 3.2 Validate-era retrospective enrichment (conditional on v2 RESCUE)

For crashes in the validate era (2024+), if either HA07d or HA10
v2 RESCUES AND specificity check supports:

- On per-crash detail: descriptive note about the autonomic-
  swing pattern (paradoxical "great-looking night" finding).
- Cite Wiggers: "Dit type patroon, waarbij het lichaam er
  schijnbaar uitgerust uitziet maar toch crasht, is door onderzoek
  beschreven (Wiggers et al.)."

If v2 produces CLOSE on both: no validate-era enrichment in v1.
The validate-era retrospective surface stays score-only.

#### 3.3 Cross-era awareness

Whichever crashes get biometric overlay should have a small
contextual note explaining era-specificity:

- "Dit patroon was vooral zichtbaar in jouw eerdere crashes
  (2022–2023). In jouw recentere crashes zien we andere patronen."

#### Phase 3 gates (stricter)

| Gate | Pass condition |
|---|---|
| G1 research bar | v2 RESCUE for the relevant finding |
| G2 specificity | Specificity check completed; FPR < locked threshold |
| G3 posterior | P(event \| pattern present) at the relevant era's base rate computed |
| G4 family | Family 3a retrospective |
| G5 threshold | Family 3a evidence threshold from methodology piece |
| G6 framing | Past-tense, observational, era-specific, anxiety-bounded |
| G7 anxiety/burden | Participant judgement on whether they want this |
| G8 calibration | Log card-fire correctness over time |
| G9 ship | All previous gates pass |

---

### Phase 4 — Stabilisation milestones (descriptive only)

**Goal**: surface specific, factual milestones that emerge from the
data. Not predictive. Not anxiety-inducing.

This phase isn't conditional on any pending research; it can ship
alongside Phase 1 or Phase 2 if there's capacity.

**Surfaces:**

#### 4.1 Milestone cards (retrospective, factual)

Small cards that appear on the trajectory screen when specific
data-driven milestones are passed:

- "Een jaar geleden was je gemiddelde [N]; nu is het [M]."
- "Je had [N] crashes in 2023, [M] in 2025."
- "Je langste crash duurde [N] dagen. Je laatste 5 crashes duurden
  gemiddeld [M]."
- (If S02 detects sustained mean-median divergence per its T4
  trigger): "Je dagen worden gemengder. Je hebt nog steeds slechte
  dagen, maar minder vaak hele weken aan een stuk."

#### 4.2 The dip-cluster ("rough patch") view

For the 15 identified dip clusters, a small descriptive view:

- "Tussen [start] en [eind] had je [N] mindere dagen verspreid over
  [M] dagen. Een ruwe periode."
- Optional: notes from those days inline.

Avoid causal language. The cluster overlay is descriptive, not a
mechanism claim.

---

## 4. What this plan deliberately does NOT include

These are explicit choices, not omissions. Each one is gated.

| Excluded surface | Why |
|---|---|
| Pre-emptive crash warning | Family 3b — no finding meets the posterior threshold. Per methodology piece, do not ship in v1. |
| Push-pattern alert | Family 6 — the push channel has refuted in three operationalisations. Do not ship on lay-belief basis. |
| "You may crash soon" cards in any form | Anxiety risk, no evidence base. |
| Causal language ("because", "due to", "this caused") | No causal inference is supported by the current research. |
| Comparison to other users / populations | The project is n=1. No population claim is defensible. |
| Numeric "recovery probability" | Would require a model the project does not have. |
| Live biometric streaming | Out of scope for v1. |
| Push notifications about any of the above | Anxiety risk + user-burden + opt-in complexity. |

---

## 5. Cross-cutting decisions for v1

### 5.1 Default opt-out for biometric enrichment

If Phase 3 ships, biometric overlay on per-crash detail defaults to
**off**. The user opts in once, with a short explanation:

> "Wil je dat we, waar mogelijk, naast jouw eigen score ook
> patronen uit je horloge laten zien bij oude crashes? Dat is
> beschrijvend, geen voorspelling."

If they opt in, the overlay appears for crashes where the gates
pass. They can opt out again at any time.

### 5.2 No badges, no streaks, no gamification

Things-3 style: the app reflects the user's state, doesn't reward
or punish. No "X day streak without a crash" — that framing makes
the crash itself feel like a failure.

### 5.3 Honest empty states

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

### 5.4 Calibration logging from day one

Every card surface logs:
- When it appeared.
- Whether the user tapped it.
- Whether they dismissed it.
- (For event-based surfaces): whether the next 14 days showed any
  event that the surface implied.

This is gate G8 from the methodology workflow. Not for product
analytics in the dashboarding sense; for the v1-vs-v1.5 iteration
loop. A card that nobody taps after the first month should
probably be removed.

### 5.5 Era-aware surfacing

For any retrospective view that uses era-specific findings, the
user should always be able to see which era the surface is
contextualising. Visual or textual ("Patroon voor crashes uit
2022–2023") so the user understands the surface is era-bounded,
not universal.

---

## 6. Suggested order of delivery

1. **Phase 1 first** (trajectory card + event markers + per-crash
   detail). Minimum viable surface. Ships independently of any
   pending research.
2. **Phase 4 milestones** in parallel with or shortly after Phase 1.
   Same descriptive material; small additional cards.
3. **Phase 2** when S02 has landed and there's design capacity for
   the multi-axis view.
4. **Phase 3** when v2 diagnostics + specificity checks complete.
   This is the conditional phase; it may or may not ship in v1
   depending on outcomes.

Phase 1 + 4 are the v1 floor. Phase 2 is the v1 stretch goal.
Phase 3 is the v1.5 candidate.

---

## 7. Open questions for the participant

These are decisions only the participant can make. The methodology
binds at G7 (anxiety/burden review) — these surfaces only ship if
the participant wants them as designed.

1. **Naming**: "crashes" or another word ("rough patches",
   "moeilijke periodes", participant's own term)?
2. **Whether to surface the train/validate era split at all** in
   any UI, or to handle it silently in the background.
3. **Whether the trajectory screen is a dedicated tab, a section
   of an "insights" screen, or accessed from a long-press on the
   timeline**.
4. **Whether dip clusters should be surfaced as their own concept**
   ("ruwe periode") or only implicitly via the visual overlay.
5. **Whether the per-crash detail should auto-expand on the most
   recent crash** (so the user lands on it from a notification or
   deep link) or always require an explicit tap.
6. **Whether notes from past crash days should be shown in the
   per-crash detail** or kept private (privacy risk: a clinician
   or family member glancing at the screen).

These shouldn't block Phase 1 design but they should be answered
before Phase 1 ships.

---

## 8. Bottom line

The research project has produced enough material to ship a
defensible, useful v1 right now, *without* the pre-emptive warning
or push-pattern surfaces that the project originally hoped for. The
v1 surfaces — trajectory + events + descriptive milestones — are
the ones the participant will touch most often anyway.

The honest framing is: this is not a "crash predictor" app. It is
an app that helps the participant see their own data clearly, in
calm and reflective Dutch, with respect for what the research can
and cannot say. That is a smaller product than the original
ambition. It is also the product the data actually supports.

The discipline that has run the research side is what carries
into the product side. Ship what you can defend. Withhold what
you can't. Calibrate as you go.

---

*Draft for review by the participant. To be moved to `docs/features/`
or `docs/design/` once the Phase 1 scope is confirmed and a
implementation owner picks it up.*
