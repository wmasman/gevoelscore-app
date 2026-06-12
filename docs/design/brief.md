# Design brief — gevoelscore-app

> **What this is.** The aesthetic / tone / personality layer of the app.
>
> **What it is not.** Not the functional spec (that's [app_brief_gevoelscore.md](../app_brief_gevoelscore.md)). Not the v1 requirements (that's [REQUIREMENTS.md](../REQUIREMENTS.md)). Not the WCAG / brainfog floor or token mechanics (that's [frontend-conventions.md](../architecture/frontend-conventions.md)).
>
> Sits between them: above WCAG, below component code. Read it before designing any new screen, generating any new variant in superdesign, or writing any new Dutch microcopy.

---

## In one sentence

A quiet, considered, warmly-personal app that records without commenting — closer to a digital paper journal than a mood-tracker.

---

## Anchor reference

**Things 3.** Inherit the *feel*: warm off-white background, soft careful shadows, generous spacing, a single accent doing brand work, friendly without being cute, polished without being precious, quiet at rest and expressive only on the moment of action.

What we take from Things 3:
- Warm-whites foundation (off-white, never stark `#FFFFFF`)
- Soft, subtle elevation (depth via gentle shadow, not flat-design, not heavy)
- Single accent color carrying identity across the whole app
- Generous breathing room between elements
- Restrained chrome — UI gets out of the way of content

What we do **not** take from Things 3:
- Its blue. Gevoelscore is warm earth, not cool blue.
- Its check-circle metaphor. Gevoelscore is a score, not a todo.
- Its productivity-tool energy. Gevoelscore is a personal artifact, not a planning surface.

---

## Identity

### Palette

**Family: warm earth.** Terracotta / clay / ochre. Muted, not saturated — never neon, never primary-color-loud. The accent does emotional work: warmth, recovery, personal-not-clinical. Paired with warm-whites background and warm-dark text (not pure black).

| Token role | Direction (final hex via superdesign / Step-0 token layer) |
|---|---|
| Background base | Warm off-white (`bg-bg` token) |
| Surface elevated | A shade warmer/softer than base |
| Text primary | Warm dark, not `#000` |
| Text secondary | Warm gray, ~60% contrast |
| Accent | Terracotta / clay / ochre family — single brand color |
| Borders / dividers | Very subtle warm gray, low contrast |
| Empty-day marker | Soft orange dot (deliberately gentler than the accent — see "Allowed nuances") |

The accent is the *only* expressive color. No red for errors. No green for success. Errors and success states use **copy + position + subtle text-weight changes** rather than color signalling. ([Frontend conventions](../architecture/frontend-conventions.md) carries the 4.5:1 contrast contract.)

### Typography

**Humanist sans throughout.** Inter or IBM Plex Sans family — designed but neutral, very legible at ≥17px (the [brainfog body-text floor](../architecture/frontend-conventions.md#brainfog-extensions-above-wcag)). No serif body. No system font, because the warm-earth + Things-3 polish wants something with a touch more deliberateness than `-apple-system`.

Single typeface family, varied via weight + size only. Numerical scores rendered in the same family — no specialty numerical typography.

### Voice

**Reflective + quiet Dutch.** Sparse, observational, no exclamation marks, no second-person questions, past tense over imperative. The app records; it does not converse. Microcopy rules below.

---

## Spatial principle: thumb-first for input

> **Thumb-first voor invoer. Reading-surfaces mogen vrij.**
>
> The interface comes to the thumb, not the other way around.

**Applies to:** input surfaces — score popout, note popout, tags popout, edit-past-day popouts, settings forms. The user is holding the phone one-handed, often in bed, often on a 4-out-of-6 day. The interface arrives where the thumb already rests; the user does not navigate to the interface.

**Does NOT apply to:** reading surfaces — day overview, timeline, calendar, login. Those follow regular layout conventions; the eye scans, the thumb travels.

**Implications:**
- Input controls live in the bottom ~45-55% of the viewport (the thumb-natural zone).
- Progression through inputs (score → note → tags) morphs in place within one zone, not as discrete sheets opening and closing.
- Voice input (when added) lives in the same thumb zone as text, not a separate modal.
- Drag handles, close buttons, dates and labels at the top of an input sheet are for visual orientation only — never for taps the user must perform to progress.
- Past-day edit popouts inherit this layout, distinguished from today only by surface tint (cooler `surface-muted` background), not by added labels — see [Allowed nuances](#allowed-nuances).

**Source:** locked 2026-05-28 after exploring an alternative quick-entry UX. Captured in memory under [[design-principle-thumb-first-input]]. This is a **spatial** rule layered on top of the aesthetic rules in Identity; it does not replace them.

**Tension to watch:** the in-flight Step 4b score row (horizontal, upper-middle of the Today shell) is not thumb-first. That tension is deferred; if this principle stays, the score row's location will need to be revisited.

---

## Motion as communication

Motion is a communication channel, not decoration. Use it to mark meaningful moments — completion of input, change of state, arrival of new content, spatial acknowledgment ("your input is now here"). Do not use it for ambient ornament — idle glow, repeating pulses, loading shimmer, celebratory flourish.

**The test:** does this motion tell the user something they need to know? If yes, it can exist (within the 200ms cap for most transitions; one-shot completion acknowledgments may run slightly longer if they aid spatial parsing). If no, it's decoration and forbidden.

**Allowed examples** (each carries meaning):
- Panel slides up or down on summon and dismiss
- Today-card receives a one-shot tint-pulse on completion of a day's entry — spatial signal that your input now lives there
- Score number scale-pulses subtly on integer-cross during drag — visual replacement for the absent haptic tick
- Sheet content morphs between input steps (score → notitie → tags) as one continuous transformation, not three discrete open/close cycles

**Forbidden examples** (decoration without message):
- Loading skeleton shimmer
- Ambient glow on the streak number, the score, or any other passive element
- Confetti, sparkle, celebration flourishes
- Bounce, elastic, overshoot, or spring-with-rebound easing on any transition
- Repeating pulses on the same element (the one-shot acknowledgment above is the only kind allowed)

**Source:** locked 2026-05-28 in conversation about the end-of-flow moment. User's framing: *"we moeten met de gebruiker kunnen communiceren op verschillende manieren"* — communication channels matter, motion is one of them, as long as it carries intent.

This is a refinement of the original "no pulse" rule, which was too absolute. The principle (no decoration) holds; the specific prohibition needed nuance.

---

## Anchoring: self-referenced, never normative

When any surface shows a number in context — a trend, a result, a breakdown — the reference point is **the user's own history** (prior value, rolling baseline, usual range), never a healthy-population norm, an "average", or another person.

**Why.** A normative anchor invites a deficit read every time the score is shown; for someone whose ceiling is genuinely lowered it reframes honest reporting as failure, which can nudge under-reporting and quietly corrupt the data. A self-referenced anchor carries the same orienting information with no ranking and no incentive to under-report.

A bare number with no anchor is also wrong (illegible). The rule is *self-referenced* anchor, not *no* anchor. Allowed: `0,3 boven vorige maand. Binnen het gebruikelijke bereik.` Forbidden: `Lager dan een gezond persoon.`

Any clinical/normative comparison (to validate impairment to a doctor) lives only behind an explicit opt-in or on a clinician-facing export — never a default view.

**Source:** ratified 2026-06-04 from the Visible/Welltory UI/UX study ([../research/ui-ux-patterns-from-visible-welltory.md](../research/ui-ux-patterns-from-visible-welltory.md) §1.9), which observed Visible anchoring against a healthy person's score and judged that framing against this app's manifest.

---

## Component personality

| Element | Direction |
|---|---|
| Score buttons (1–10) | All neutral by default. Selected one fills with accent. The *number is the meaning* — no red→green gradient, no faces, no color-coded scale. Tap target ≥48×48 per brainfog rules. |
| Tag chips | Pill-shaped, very soft borders, generous internal padding. Tapped = filled with accent. Untapped = warm-gray outline. Frequently-used tags surface first (mechanic specified in [REQUIREMENTS.md](../REQUIREMENTS.md)). |
| Note input | Single open field, generous height, no decorative border, no character counter. Feels like writing in a margin. |
| Streak counter | Visible but quiet. May carry small visual elevation (slightly larger, accent color for the number) — explicitly *allowed* to be subtly proud, never loud. |
| Save confirmation | Brief text fade, ~150ms. "Bewaard." appears, fades. No checkmark animation, no pulse, no color flash. |
| Empty-day marker (calendar / recent-missed) | Soft orange dot. Gentler than the warm-earth accent (different hue, lower saturation), used *only* for the "you didn't log this day" cue. The only non-accent color in the system, and only for this purpose. |
| Past-day read-only view | Visually distinct from edit mode — softer background, no input borders. Edit toggle is a deliberate-feeling tap, matching the "edit is friction-on-purpose" decision in REQUIREMENTS. |
| Surfaces (sheets, modals) | Rounded, soft shadow, focus-trapped per [frontend-conventions](../architecture/frontend-conventions.md#focus-management). No slam-in animation. |

---

## Allowed nuances

These are *allowed* even within the restrained direction. Each was an explicit call, not an oversight.

- **Subtle streak elevation.** The streak number may be slightly larger and in the accent color. Not "47 dagen op rij! 🔥" — just "47 dagen" rendered with quiet pride.
- **Soft orange dot on empty calendar days.** Drives backfill behavior gently. Not red, not a warning icon, not "missing!" copy. Just presence-vs-absence rendered as a small dot.
- **Tutorials, tooltips, one-time setup wizards.** Allowed for genuinely instructional moments — 2FA pairing, first-time import. Must be dismissible, must not re-trigger, must not exist for features that don't need explanation.
- **End-of-day score reminder (opt-in via Settings).** Deferred to v2 per [REQUIREMENTS](../REQUIREMENTS.md#cardinal-principles) but the design intent is locked here. Canonical use case: the author writes a morning note without a score because the day's shape isn't clear yet; an evening reminder prompts them to add the score once the day has settled. Constraints any implementation must honor:
  - **Off by default.** Lives in Settings as a user toggle, not enabled at install.
  - **Silent.** No sound, no vibration, no banner-with-bell-icon. iOS-PWA "Notifications" only, with the user's OS-level sound/vibration settings respected (i.e. the app never requests sound).
  - **At most once per day.** A single reminder per missed-score day. Never re-sent within the same day. Never sent on days where a score is already logged.
  - **No streak-loss framing.** Copy is observational, not motivational. Allowed: `Vandaag nog geen score.` Forbidden: `Mis je streak niet!`, `Je hebt nog niets ingevuld vandaag!`, `Tijd om je dag te loggen`.
  - **Dismissible without entering the app.** Tapping the notification opens directly to today's entry; swiping it away is a valid action, not a "missed action".
  - **Configurable time** (default: evening, e.g. 21:00 local). User picks the hour in Settings.
  - **Never marketing, never engagement.** This is a *user-requested* prompt to complete a self-initiated workflow — not a tool to drive retention.

---

## Forbidden

| Anti-pattern | Why |
|---|---|
| **Gamification** — badges, achievements, level-ups, streak-loss-shaming, milestones with celebration | Genre-defining anti-pattern. The 1.363-day history was built without any of this; the app must not introduce reasons to log other than the user's own value. |
| **Emoji as score / mood language** (face emojis on the score row, mood-emoji headers, decorative emoji in chrome copy) | Incompatible with humanist-sans + restrained + reflective. Emoji in user-typed notes is the user's choice; emoji as UI element is forbidden. |
| **Coaching / encouraging copy from the app** ("Goed bezig!", "Mooie streak!", "Vergeet je dag niet!") | Patronizing on a bad day. The app does not perform emotional labor that wasn't asked for. |
| **Mascots, illustration characters, decorative artwork** | No friendly bird, no plant-that-grows-with-streak, no hand-drawn anything. The app's identity is type + color + space, not pictures. |
| **Celebration animations** | No confetti, no bouncing, no flashing. Pulses are forbidden as decoration; one-shot completion acknowledgments (e.g. today-card tint-pulse after the last tag is saved) are allowed — see [Motion as communication](#motion-as-communication). The 200ms cap from [frontend brainfog rules](../architecture/frontend-conventions.md#brainfog-extensions-above-wcag) still applies to most transitions. |
| **Color-coded score scale** (red→amber→green) | The score is a self-rating; color-coding feels like the app rendering judgment before the user has finished thinking. The accent fills the *selected* button only. |
| **Normative comparison by default** (score vs. healthy norm, "average", or other users) | Compares and judges the user against others — against the no-judgment manifest, and nudges under-reporting. Anchor to the user's own baseline/history; reserve normative framing for an opt-in or clinician export. See [Anchoring](#anchoring-self-referenced-never-normative). |
| **Unsolicited notifications** (default-on reminders, marketing/news, "we miss you" re-engagement) | Reminders are allowed *only* as an explicit user opt-in (see Allowed nuances). Anything that pushes without prior user consent — or that exists to drive engagement rather than serve the logging — is forbidden. |

---

## Dutch microcopy rules

Examples are non-exhaustive but anchor the tone. When in doubt, pick the option that sounds more like a paper journal labelling its sections and less like an app talking to its user.

### Do
- `Vandaag` (page title — noun, no question)
- `Bewaard.` (save confirmation — terminal period, past tense)
- `47 dagen` (streak — bare number, no exclamation)
- `Geen invoer.` (empty state — observational)
- `Verbinding verloren.` (error — observational, terminal period)
- `Bewerken` (action label — verb infinitive)
- `Exporteren` (action label — verb infinitive)

### Don't
- ~~`Hoe was vandaag?`~~ (second-person question)
- ~~`Opgeslagen!`~~ (exclamation)
- ~~`Top, opgeslagen 🎉`~~ (warm + emoji)
- ~~`47 dagen op rij!`~~ ("in a row" + exclamation = pride performance)
- ~~`Je hebt nog niets ingevuld vandaag`~~ (second-person, scolding)
- ~~`Oeps, er ging iets mis!`~~ (apologetic + exclamation)
- ~~`Mooie streak — ga zo door`~~ (coaching)
- ~~`Aan de slag!`~~ (cheerleading)

### General principles
- No exclamation marks anywhere in chrome copy.
- No second-person questions. (`Vandaag`, not `Hoe was je dag?`)
- Past tense over imperative for system states. (`Bewaard`, not `Opslaan` for confirmations; `Opslaan` is fine as a button label if needed, though v1 auto-saves so this should be rare.)
- Terminal periods on standalone strings (`Bewaard.`, `Geen invoer.`); they read as journal entries, not buttons.
- One word is almost always better than three. Brainfog floor.
- **No em-dash (`—`) in user-facing strings.** Prefer a comma (tightly related clauses), a period (split into two short sentences), or a colon (second clause explains the first). Example rewrites: `Niet opgeslagen — probeer nogmaals` → `Niet opgeslagen. Probeer nogmaals.` / `Eén tik per dag — geen oordeel, wel inzicht.` → `Eén tik per dag. Geen oordeel, wel inzicht.` / Email subject `Gevoelscore — interesse` → `Gevoelscore: interesse`. Standalone `—` as an empty-state glyph (e.g. `streak > 0 ? n : '—'`) is fine; the rule is about punctuation in sentences. This rule does NOT apply to source-code comments or this doc's prose.

All Dutch strings live in [`src/copy.ts`](../architecture/frontend-conventions.md#copy-discipline) per [frontend-conventions](../architecture/frontend-conventions.md). When the inline JSX literal would be `"Bewaard."`, it's `copy.daily.saved` — wired through the structured copy module.

---

## What this brief deliberately does NOT specify

- **Exact hex values** — direction only (warm-earth family, warm whites, warm dark text). Resolved in the [token layer in `globals.css`](../architecture/frontend-conventions.md#styling-utility-first-tailwind--design-tokens) and via superdesign's design-system pass.
- **Final typeface** — Inter vs IBM Plex Sans is an implementation detail. Both meet the humanist-sans direction and the ≥17px legibility floor.
- **Component layouts** — the score-row layout (1×10 vs 2×5 vs other) is flagged in [REQUIREMENTS](../REQUIREMENTS.md#v1-screens) as a feature-plan decision, not a brief-level one. Same for tag-chip grid, calendar layout, etc.
- **Dark mode** — deferred to v1.5+ per [frontend-conventions](../architecture/frontend-conventions.md#styling-utility-first-tailwind--design-tokens). The warm-earth + warm-whites direction must inform a dark-mode palette later; out of scope here.
- **Sub-component primitives** — no `<Button>` / `<Chip>` API; Tailwind utilities + `cn()` carry v1 per frontend conventions. Brief reasoning still applies whenever those primitives eventually get extracted.

---

## Using this brief

**With superdesign.** When invoking `/superdesign` for any screen variant, paste the "In one sentence", "Anchor reference", "Identity", and "Forbidden" sections into the prompt. They give the design agent enough to stay on-tone.

**In code review.** A diff that introduces a green checkmark, a streak badge, a `"!"` in a Dutch string, or a face-emoji-as-score should be rejected with a link to this file.

**In feature planning.** `/plan-feature` step files for new screens reference this brief in their "Acceptance Criteria" — specifically the relevant Forbidden rows and any Allowed-nuances that apply.

---

## Cross-references

- [REQUIREMENTS.md](../REQUIREMENTS.md) — cardinal principles + functional v1 spec.
- [app_brief_gevoelscore.md](../app_brief_gevoelscore.md) — original full brief with blocks 1–5, data model, v1.5/v2 roadmap.
- [architecture/frontend-conventions.md](../architecture/frontend-conventions.md) — WCAG 2.2 AA + brainfog extensions, design-token mechanics, copy module location.
- [features/daily-entry/README.md](../features/daily-entry/README.md) — the active feature where this brief gets its first test.
