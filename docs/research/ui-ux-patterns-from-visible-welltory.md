# UI/UX pattern study — Visible & Welltory

*A developer-facing teardown of two existing energy-limiting-illness trackers, extracting the interaction patterns worth borrowing for the gevoelsscore app, with the design rationale for each. Source material: 13 screenshots from **Visible** (FUNCAP27 onboarding, daily check-ins, functional-capacity result, trackers, reminders, health-report) and 1 from **Welltory** ("What's going on?" check-in).*

> **Status: reference, not spec.** This describes patterns observed in shipping products and judges them against our own design principles (one-tap daily input; the data is the user's; present conclusions, don't decide; all exertion counts; surface the *delayed* cost). It is meant to be argued with and to give a developer concrete, buildable detail. It does not commit us to copying any screen.

---

## 0. The two products at a glance

**Visible** is purpose-built for ME/CFS and Long COVID. It is the closest existing product to this project's intent: a daily symptom/crash check-in, a monthly *functional capacity* questionnaire (FUNCAP27), trackers the user can shape, scheduled reminders, and a clinician-ready PDF export. Its visual language is calm, dark-navy, low-stimulation, one-question-per-screen.

**Welltory** is a general HRV/wellness app, not illness-specific. Only its "What's going on?" logging screen is relevant here: it shows a faster, denser, tag-first way to capture context and mood in a single screen. Useful as a *contrast* — it trades calm for speed.

The throughline of what we like: **both minimise the cost of a single entry**, but Visible does it by slowing down and isolating each decision, while Welltory does it by collapsing everything onto one dense screen. Our app has to pick deliberately between those two postures for different moments (daily vs. monthly).

---

## 1. Pattern catalogue

Each pattern below lists: **what it is**, **why we like it**, and **build notes** concrete enough to implement.

### 1.1 One-question-per-screen daily input (Visible)

**What it is.** The daily flow asks one thing at a time on its own full screen: "How was your sleep?" with four large tiles (1 Awful / 2 Bad / 3 Fair / 4 Good) and nothing else competing for attention. A progress indicator (segmented dashes near the top) shows how many steps remain. Each screen has a single primary action (`Save`) pinned to the bottom.

**Why we like it.** This is the lowest-cognitive-load way to ask a question, which matters enormously for a population with brain fog and limited cognitive budget — *cognitive load is itself part of the energy envelope we're trying to respect*. One decision per screen means no scanning, no scrolling-to-find, no accidental mis-tap on an adjacent field. It directly serves our cardinal principle of frictionless daily input.

**Build notes.**
- Tappable targets are large (≈ quarter-screen-width tiles), thumb-reachable, with the numeric value as the primary glyph and the word label underneath. Number + word together serves both fast repeat-users and first-timers.
- Each step is independently savable; progress persists (see 1.7). Treat the flow as a resumable sequence of atomic answers, not one big form that must be completed in a session.
- Bottom-pinned single CTA. Never put two competing primary buttons on a daily screen.
- Keep the date visible but unobtrusive (top-right, e.g. "Wed, 3 Jun") so a user back-filling yesterday always knows which day they're scoring.

### 1.2 Severity grid with numeric + verbal anchors and colour (Visible)

**What it is.** "How were your symptoms today, at their worst?" presents a matrix: symptom rows (Fatigue, Headache, Memory issues, Brain Fog, Anxiety, Muscle aches…) × four columns labelled **None / Mild / Moderate / Severe**, mapped to **0 / 1 / 2 / 3**. The selected cell fills with a traffic-light colour — green at 0, yellow at 2, orange at 3 — so a filled row reads at a glance.

**Why we like it.** It captures multi-symptom severity in a single compact, scannable gesture. The double labelling (word *and* number) keeps it intuitive for newcomers while producing clean ordinal data for analysis. Colour gives instant visual feedback that an answer registered, and lets the user sanity-check the whole grid before saving. The framing "**at their worst**" is a deliberate, defensible measurement choice — it picks a consistent reference point rather than the fuzzier "on average."

**Build notes.**
- Fixed 4-point ordinal scale (0–3) per symptom. Store the integer, render the word + colour.
- Colour ramp tied to value, not to symptom: 0 = green, 1 = neutral/unfilled, 2 = amber, 3 = orange/red. Unselected cells stay low-contrast navy so the selected one pops.
- The symptom *rows* are user-configured (see 1.4) — the grid is generated from the user's active symptom set, not hard-coded.
- "At their worst" is the prompt wording; keep the measurement reference explicit and constant, because changing it later breaks longitudinal comparability.
- Note the parallel binary question above the grid — "Were you in a crash today? No / Yes" — captured as a first-class boolean event, not buried as a symptom. Crash is the outcome variable that matters most; it deserves its own control.

### 1.3 "Use previous answers" carry-forward toggle (Visible)

**What it is.** A toggle at the top of the symptom screen labelled **"Use previous answers"** pre-fills today's grid with yesterday's responses, so an unchanged day is a one-tap confirm instead of a full re-entry.

**Why we like it.** For a chronic condition many days are similar; re-entering identical data is friction that drives drop-off. Carrying forward and letting the user *adjust the deltas* respects their time and dramatically lowers the daily cost — again the cardinal goal. It also subtly improves data quality: people are more likely to log every day if a typical day is nearly free.

**Build notes.**
- Toggle pre-populates from the most recent completed entry. User edits only what changed.
- **Data-integrity caveat (important for us):** record whether a value was *carried-forward-unconfirmed* vs. *actively set*, at least internally. Our own findings doc warns against treating carried/missing data as if it were freshly asserted. A silent copy that looks identical to a real answer can distort later trend analysis. Store provenance even if you never show it.
- **Gentle anti-drift nudge.** If the user carries forward unchanged for several days running (e.g. ≥ 3–4 in a row), surface a soft, non-blocking prompt — *"This is the 4th day with the same answers. Has anything shifted, even a little?"* — easy to dismiss with a single tap. The goal is to catch autopilot logging that flattens real variation, not to scold. Keep it rare and quiet (a one-line banner, not a modal), and never block saving. This improves the data *at the source*, which is better than only flagging it after the fact.
- Default the toggle to *off* on first use; let the user opt into it.

### 1.4 User-shaped trackers, grouped, with "Add my own" (Visible)

**What it is.** A `Trackers` area with three tabs — **Symptoms**, **Exertion**, **Other factors**. Within Symptoms, items are grouped (General: Fatigue, Fever, Allergies, Tremors; Brain: Headache…) and each is a toggle pill the user switches on/off. A dashed **"+ Add my own"** card under a **Custom** header lets users define their own. A subtle **"Learn more about symptom tracking"** link sits at the top.

**Why we like it.** It lets the user shape what they track without overwhelming a newcomer — sensible defaults, grouped for scanability, fully customisable. This is a direct expression of *the data is the user's*: they decide what's worth measuring about their own body. The grouping (General / Brain / …) keeps a long list navigable.

**Build notes.**
- Three categories of trackable thing, each independently togglable: **symptoms**, **exertion types**, **other factors** (experiences/medication/lifestyle).
- Ship curated defaults grouped by system; allow custom entries with a name (and a type/scale). Custom items must flow into the same daily grid as built-ins.
- The active tracker set is the schema for the daily check-in — turning a tracker on adds a row to the relevant daily screen. Design the data model so the daily entry references tracker IDs, not a fixed column list.

### 1.5 Exertion as a first-class, multi-dimensional tracker (Visible)

**What it is.** The **Exertion** tab tracks four distinct kinds: **Cognitive, Emotional, Physical, Social**. Each is an independently togglable tracker.

**Why we like it — and why it matters more for us than for them.** This is the single most under-appreciated truth in pacing and it's the one a step-counter misses entirely: *all exertion draws on the same energy budget*. Cognitive and emotional load can crash someone as hard as a walk. Visible modelling exertion as four separate axes (not just "activity") is exactly right and aligns with our pacing research. We should match or exceed this.

**Build notes.**
- Model exertion as ≥4 independent dimensions (cognitive, emotional, physical, social), each scored on its own ordinal scale per day — not collapsed into a single "activity" number.
- These become the candidate *leading indicators* the gevoelsscore (the outcome) can be correlated against, including with a delay. Make sure each exertion entry is timestamped/dated so a 48–72h lag analysis is possible downstream.

### 1.6 "Other factors": experiences, medication, lifestyle as taggable events (Visible / Welltory)

**What it is.** Visible's **Other factors** tab separates **Experience** (Infection, Period — booleans), **Medication** ("+ Add item"), and **Lifestyle** ("+ Add item"). Welltory's "What's going on?" does the fast version: a wrap of coloured tag chips (sleep, workout, lying down, water, **crash**, work, insomnia, meal, **More…**) tapped on/off in one gesture.

**Why we like it.** Confounders and interventions are what turn a diary into an *experiment*. Letting users log infection, period, medication, and lifestyle events means later analysis can ask "was this crash an exertion-flare or an external infection?" and can probe the shielder-vs-reliever medication question for that individual. Welltory's chip cloud shows how to make this near-frictionless when speed matters.

**Build notes.**
- Support both shapes: Visible's structured/grouped list (good for a deliberate setup screen) and Welltory's one-tap chip cloud (good for the daily moment). The chip cloud is the better daily UX; the grouped list is the better configuration UX.
- "Infection" and "Period" as date-stamped boolean episodes; medication and lifestyle as user-defined items that can be toggled per day with optional timing.
- This is the substrate for the n-of-1 intervention log our pacing research flags as the highest-value Tier-3 feature. Build the event model now even if the analysis comes later: every factor needs an id, a date, and (ideally) a time-of-day.

### 1.7 Resumable progress with explicit reassurance (Visible)

**What it is.** The "Before we begin" screen sets expectations plainly: **"This should take 5–10 minutes," "If you need a break, your progress will be saved so you can return anytime,"** and a social nudge — "complete this together with someone who sees you in everyday life" — plus a clear medical disclaimer. Progress dashes appear throughout the flow.

**Why we like it.** Telling a low-energy user up front how long something takes and that they can stop without losing work removes a real barrier to starting. It's honest and respectful of limited capacity. The disclaimer up front is the right place for it.

**Build notes.**
- State expected duration and persistence *before* a multi-step flow begins.
- Autosave every atomic answer; allow resume at the exact step. Show progress (segmented dashes) so remaining effort is legible.
- Keep the medical disclaimer present but out of the way ("not designed for diagnosis/treatment… check with a health provider"). We need the equivalent given our manifest's stance.

### 1.8 The monthly questionnaire framing screen (Visible / FUNCAP27)

**What it is.** Before the monthly questionnaire, Visible explains *what it is and how to answer it*. "What's involved?" introduces FUNCAP27 as "a validated, patient-informed questionnaire that evaluates your functional capacity across 27 unique activities," and states the core question: *"What are the consequences for you if you perform this activity? To what extent does this affect how much else you can do?"* A separate **"When answering, keep in mind"** screen gives three answering rules: **(1)** base it on an *average* day in the last month, not the worst or best; **(2)** if you haven't done an activity, score how you think it *would* affect you; **(3)** include all necessary steps (e.g. "going to the shop" includes getting dressed and travelling).

**Why we like it.** It anchors the measurement so answers are comparable month-to-month and between people — the framing rules are doing real psychometric work. Leaning on a *validated* instrument (FUNCAP27) gives the score external credibility a home-made scale lacks. And the "consequences for you / how much else you can do" framing measures the *trade-off cost* of activity, which is exactly the energy-envelope concept at the heart of pacing.

**Build notes.**
- For any periodic standardized assessment, precede it with (a) a one-screen "what this is" and (b) a one-screen "how to answer" with explicit reference-window rules. These rules are not fluff — they are what make the longitudinal series valid.
- If we adopt FUNCAP27 (or similar), respect its scoring exactly; don't silently rescale (our findings doc's warning against naive rescaling applies). Keep the instrument's native scale and document any mapping.
- Monthly cadence is deliberately distinct from the daily flow — different posture, more time budgeted, more explanation. Don't reuse the one-tap daily ergonomics here.

### 1.9 Functional-capacity result: gauge + comparison + subscale breakdown (Visible)

**What it is.** The result screen shows a semicircular **gauge reading 4.1 on a 0.0–6.0 scale**, dated. Below: *"Your functional capacity score is lower than a healthy person's score of 6.0,"* a "Learn more about FUNCAP27" link, and a **Breakdown** card: a plain-language summary ("your ability to carry out day-to-day activities is impacted, particularly in *Activities in home*") followed by horizontal sub-scores per domain (Personal hygiene/basic functions, Walking/moving around, Being upright, Activities in home), each a track with a coloured marker showing where the user falls.

**Why we like the structure — with one deliberate change.** One headline number for orientation, an interpretable anchor so the number *means* something, and a breakdown that localises *where* the impairment is — all without telling the user what to do about it. This is precisely our principle of **present the conclusion, let the person decide**: it surfaces a pattern ("particularly Activities in home") and stops there.

**Where we diverge: drop the healthy-person comparison as the default.** Visible anchors the score against a healthy population — *"lower than a healthy person's score of 6.0."* We don't want that as the default framing. It goes against the manifest's stance on not comparing, pushing, or judging people: a normative anchor invites a deficit read every time the score is shown, and for someone whose ceiling is genuinely lowered it reframes honest reporting as failure — which can perversely nudge users to under-report to feel better, quietly corrupting the data we depend on.

The fix is **not to remove the anchor** (a bare number is illegible) but to swap a *normative* anchor for a *self-referenced* one: compare the user to **their own baseline / last month / their usual range**, not to a healthy norm. "Up 0.3 from last month, within your usual range" carries the same orienting information with none of the ranking, and has no incentive to under-report.

Some users do still want the clinical/normative comparison — to validate to themselves or a doctor that the impairment is real. So: **self-referenced framing is the default**; any healthy-population comparison lives only on the clinician-facing PDF export or behind an explicit opt-in, never the default result view.

**Build notes.**
- Headline gauge with a fixed, labelled range and the raw value large and central.
- Anchor the score to the **user's own history** by default (prior value, rolling baseline, personal range) — *not* a healthy-population reference. A bare number isn't legible; a number against the user's own baseline is, without judging them against anyone.
- Reserve normative/healthy comparison for the clinician PDF or an explicit opt-in setting; keep it off the default daily/monthly result.
- Subscale breakdown as horizontal position-markers per domain — fast to scan, no chart-reading skill required. Anchor these to the user's own prior too, not a population norm.
- Plain-language summary that *describes* ("impacted, particularly in X" / "lower than your usual") and never *prescribes* or *ranks against others*. No "you should rest more," no "below average." This is a hard line for us.
- Colour-code the markers consistently with the rest of the app's severity ramp so the visual language is one system, not per-screen.

### 1.10 Scheduled reminders, dual cadence, user-set times (Visible)

**What it is.** A `Reminders` screen with two independently togglable reminders: **Morning check-in** ("Measure your body's ability to take on the day. It's best to do this in bed as soon as you wake up," default 07:30) and **Evening check-in** ("Log how your day has been… before bedtime," default 20:00). Each has an editable "Remind me at" time.

**Why we like it.** Two cadences map to two genuinely different measurements: morning = baseline capacity (best taken before the day loads the body), evening = the day's actual cost. The reminder copy *teaches the method* ("do this in bed as soon as you wake up") in the act of nudging. Editable times respect that everyone's day is different.

**Build notes.**
- Two distinct daily entry types (morning baseline, evening outcome), each with its own reminder, default time, and editable schedule, each independently on/off.
- Reminder copy should encode the *correct method*, not just "time to log."
- (Implementation: local notifications; in our environment, recurring reminders/briefings could also be backed by a scheduled task.)

### 1.11 Clinician-ready PDF export, gated on data sufficiency (Visible)

**What it is.** A **Health Report PDF** feature that previews a polished clinical summary (symptom heatmaps, overall symptom-burden curve, treatments timeline) but is **gated**: "Complete 30 days of tracking to create your health report — we need 30 days of morning check-in data to generate a health report." A separate plain **Data export** lives alongside it.

**Why we like it.** A shareable, clinician-legible artifact makes the user's invisible illness *legible to a doctor* — high real-world value. Gating on 30 days is honest about when the output becomes meaningful rather than generating noise from three data points. And offering a raw **Data export** beside the formatted PDF is a clean expression of *the data is the user's* — they can take it and leave.

**Build notes.**
- Two export paths: a **formatted clinical PDF** (curated, narrative + visuals, for sharing) and a **raw data export** (CSV/JSON, for ownership/portability). Ship both.
- Gate the *formatted* report on a stated minimum data window; show the requirement and current progress, not a dead button.
- Raw export should never be gated — the user's data is theirs from day one.

### 1.12 Calm, low-stimulation visual system (Visible) vs. fast dense system (Welltory)

**What it is.** Visible is uniformly dark navy, high-contrast white type, generous spacing, one accent colour for selection (mint/teal toggles), traffic-light only for severity. Large type, lots of breathing room. Welltory is near-black, *denser*: multicoloured chips, a 5-face mood row, a 5-heart feeling row, blood-pressure/weight shortcuts, and a comment field with voice input — everything on one screen.

**Why we like it (and the trade-off).** Visible's restraint is the right default for a photophobic, fatigued, brain-fogged user: low light output, minimal simultaneous decisions, nothing flashy. Welltory's density is the right *exception* for a power-user moment where capturing many things fast beats calm. We like Visible's calm as the house style and Welltory's chip-cloud as the model for the one specific moment (daily context tagging) where speed wins.

**Build notes.**
- House style: dark, low-luminance background; high-contrast type; one selection accent; severity-only colour ramp. Respect reduced-motion and large-text accessibility settings; avoid bright flashes and busy animation.
- Reserve density (Welltory-style chip clouds, multi-control single screens) for explicitly opt-in fast-entry moments, never for the default guided flow.
- Voice-to-text for free notes (Welltory's mic) is a genuine accessibility win for users for whom typing is costly — worth adopting.

### 1.13 Mood and "feeling" as separate lightweight scales (Welltory)

**What it is.** Welltory captures **Mood** (5 face icons, sad→happy) and **Feeling** (5 hearts, filled left-to-right) as two distinct quick scales, plus optional structured vitals (blood pressure, weight) and a free comment.

**Why we like it.** Separating "mood" (emotional state) from "feeling" (a general somatic wellness sense) acknowledges they're different signals. Both are single-tap. It's a reminder that our core *gevoelsscore* can stay this light — a single fast subjective rating — while still leaving room for optional structured add-ons (vitals) for those who want them.

**Build notes.**
- The cardinal daily score should be one fast tap on a short ordinal scale (this is our gevoelsscore).
- Optional, clearly-secondary structured fields (vitals, weight, free note) can hang off the same screen for users who want them, without ever blocking the one-tap path.

---

## 2. Cross-cutting patterns we want to carry over

1. **Atomic, resumable, autosaved entries.** Every answer saves on its own; the flow can be abandoned and resumed. (1.1, 1.7)
2. **Word + number + colour triple-coding** on every ordinal control, so it's legible to newcomers and produces clean data. (1.2, 1.9)
3. **The active tracker set *is* the daily schema.** Daily screens are generated from the user's configured trackers, not hard-coded. (1.4, 1.5, 1.6)
4. **Exertion modelled as multiple independent axes**, never one "activity" number. (1.5)
5. **Two cadences:** fast daily (one-tap, carry-forward) + deliberate periodic (validated, well-framed). Different ergonomics for each. (1.1, 1.8, 1.10)
6. **Score → anchor → breakdown → stop.** Show the number against a reference, localise it, describe it in plain language, and never prescribe an action. (1.9)
7. **The data is the user's:** raw export ungated from day one; formatted clinical PDF gated on sufficiency. (1.11)
8. **Provenance under the hood:** carried-forward and missing values are flagged internally so later analysis doesn't mistake them for fresh assertions. (1.3)

---

## 3. What to avoid / adapt rather than copy

- **Don't naively rescale** any validated instrument into our internal scale. Keep the native scale; document mappings. (Our findings doc's tails-carry-the-story warning.)
- **Don't let carry-forward silently fabricate a time series.** Visible's "Use previous answers" is great UX but must be paired with (a) internal provenance flags and (b) a gentle anti-drift nudge after several unchanged days running ("are you sure nothing changed?") — or it pollutes trends. (1.3)
- **Don't over-densify the daily flow.** Welltory's one-screen approach is the exception, not the rule — the default population can't afford the cognitive load most days.
- **Don't cross the prescription line.** Visible describes ("particularly Activities in home") and stops. Any temptation to add "so you should…" violates our manifest.
- **Don't anchor the score against a healthy norm by default.** Visible's "lower than a healthy person's 6.0" compares and judges the user against others — against our manifest, and it can nudge under-reporting. Anchor to the user's own baseline/history instead; keep normative comparison to the clinician PDF or an opt-in. (See 1.9.)
- **Mind the privacy boundary** for the clinical PDF/export: this is health data; favour local processing and state the security stance explicitly (per our SECURITY posture).

---

## 4. Quick reference — pattern → our principle

| Pattern (source) | Serves which gevoelsscore principle |
|---|---|
| One-question-per-screen (1.1) | Frictionless one-tap daily input |
| Severity grid, triple-coded (1.2) | Low cognitive load + clean ordinal data |
| Carry-forward toggle (1.3) | Minimise daily cost (with provenance caveat) |
| User-shaped, grouped trackers (1.4) | The data is the user's |
| Exertion as 4 axes (1.5) | All exertion counts; leading indicators |
| Other-factors event log (1.6) | Diary → n-of-1 experiment platform |
| Resumable + expectation-setting (1.7) | Respect limited capacity |
| Questionnaire framing rules (1.8) | Comparable, valid longitudinal measurement |
| Gauge + breakdown, self-referenced anchor (1.9) | Present conclusions, don't decide; don't compare/judge against others |
| Dual-cadence reminders (1.10) | Method taught in the nudge; morning≠evening |
| Gated PDF + ungated raw export (1.11) | The data is the user's |
| Calm house style / fast exception (1.12) | Low-stimulation by default |
| Mood vs feeling, single-tap (1.13) | The core score stays light |

---

*Prepared June 2026 for the gevoelsscore project. Observations are from product screenshots; judgments are against our own manifest and research notes (`pacing-and-crash-mitigation.md`, `pais-pem-literature-review.md`, the dashboard findings, and the v1 brief). Patterns to adopt are flagged with build notes; the carry-forward provenance and no-rescale cautions are the two most important not-to-break constraints.*
