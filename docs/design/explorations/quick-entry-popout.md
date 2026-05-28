# Quick-entry popout — design exploration

> **Status: design exploration, not on the v1 roadmap.** Captured during a focused design conversation on 2026-05-28. Build decision deferred until the exploration is judged ready (or rejected) against the in-flight Step 4b score-row direction. This document is the single source of truth for the exploration; the principles it invokes live in the [design brief](../brief.md).

---

## Why this exists

The v1 daily-entry feature (Steps 0–6 in [`docs/features/daily-entry/`](../../features/daily-entry/)) currently builds a today-shell with a horizontal score row at the top, a note field below, and tag-category buttons below that. The page scrolls. The user enters data by tapping a score, scrolling to the note, tapping again, scrolling to tags, tapping again.

That design solves the cardinal-principle requirements correctly. It is also **form-shaped** — controls distributed across a scrollable page, the user's thumb travels across the screen, grip shifts to reach the next field.

This exploration takes a different shape: a **single persistent thumb-zone panel** where score, note, and tags morph in place. The user's thumb stays put; the interface arrives where it already is.

The motivating user phrase: *"ideally, it is just a series of taps while you hold your phone in your hand. Every time, the new input is perfectly located at tapping height for your thumb."*

---

## Principles invoked

Both of these are general design principles for the whole app, now applied concretely to this surface.

- **[Spatial principle: thumb-first for input](../brief.md#spatial-principle-thumb-first-for-input)** — input surfaces live in the bottom ~45–55% of the viewport; the interface comes to the thumb. (Scoped to input surfaces; reading surfaces are free.)
- **[Motion as communication](../brief.md#motion-as-communication)** — motion exists to mark meaningful moments, never as decoration. The test: does this motion tell the user something they need to know?
- **[Reflective + quiet Dutch tone](../brief.md#voice)** — no exclamation marks, no second-person questions, terminal periods, no em-dash in user-facing strings.
- **Past-day distinction via surface tint, not via labels** — see Allowed nuances in brief.

---

## Anchor references (chosen 2026-05-28)

The brief's original Things-3 anchor remains in force for the rest of the app (palette, shadow weight, typography polish). For this specific input-surface exploration, three additional anchors were chosen:

| Anchor | What it imports |
|---|---|
| **Claude mobile / WhatsApp input bar** | Persistent input zone with co-located inputs. The composer never moves; content scrolls above it. *(Voice + text co-location is parked to v2 — see Voice section below.)* |
| **iPod scroll-wheel** | Tactile in-place gesture where the thumb learns the geography over time. No need to look. |
| **iOS Reachability gesture** | Interface descends to the thumb; the user does not reach up. The whole pattern of "interface comes to you" is Apple's own acknowledgement that thumb-zone matters. |

**Explicitly NOT chosen:** Snapchat shutter (too "instant capture" energy — we want a sustained ritual, not a snap-and-go).

---

## The panel

| Property | Value |
|---|---|
| Position | Bottom of viewport, slides up from below |
| Height | ~45–55% of viewport (fixed throughout the flow — content morphs inside, panel does not resize) |
| Width | Full viewport width, with horizontal padding via the project's standard `--gap` tokens |
| Background — today | `--color-surface` (#FFFCF8) — warm, slightly elevated |
| Background — past day | `--color-surface-muted` (#F2EDE5) — cooler, flatter, reads as "behind glass" |
| Top corners | 28px rounded (matches the design-system sheet token) |
| Shadow | `--shadow-lg` (single-direction soft drop) |
| Backdrop | The today-overview above is visible but dimmed (~40% warm-dark wash) |

**Inside the panel — three regions:**

```
┌────────────────────────────────────┐
│  drag-handle    date    ✕          │  ← top: orientation only, no
│                                    │     primary-action taps required
├────────────────────────────────────┤
│                                    │
│        (middle region —            │  ← morphs between steps
│         the input control          │     (score / note / tags)
│         that morphs)               │     fixed height: ≥ thumb reach
│                                    │
├────────────────────────────────────┤
│        ← back     forward →        │  ← bottom: action zone, in thumb
│                                    │     reach; symmetrical pair
└────────────────────────────────────┘
```

The **top region** is purely orientation — drag-handle for the close gesture, date for context, optional X to dismiss. None of these are required for forward progression through the flow. They exist so the user can see *where they are* without needing to act on them.

The **middle region** is where the actual work happens. This is the only part that morphs between steps.

The **bottom region** carries the explicit progression controls — forward button on every step, back button from step 2 onwards. Both live in the thumb zone, symmetrical pair.

---

## Five trigger moments

| # | Moment | Behaviour |
|---|---|---|
| 1 | App opens; today has no entry yet | Panel auto-appears on **score mode**. No tap to summon. The interface is already at the thumb when the user opens the app, on the day's most-likely action. |
| 2 | App opens; today already has an entry | **No panel.** Day-overview only. Avoids pop-up-in-your-face on a return visit when nothing needs doing. |
| 3 | Tap on a region of the today-card (score / note / tags) | Panel slides up, opens at **that specific mode**. Spatial coherence: the place you tapped is where the panel "comes from". |
| 4 | Tap on a previous-day card | Same as #3, but the panel uses `--color-surface-muted` (cooler tint) to signal "this is not today". No text label — tint is the entire signal. |
| 5 | Within-panel progression | **Hybrid** (see Progression section below). |

---

## Score-circle mechanic

| Property | Value |
|---|---|
| Visual | Large decorative circle in the centre of the middle region. The circle carries visual rest and brand identity — it is **not** the gesture surface in the iPod-rotational sense. |
| Current score | Rendered very large in the circle's centre. Display size (28px+), Inter weight 600, `--color-accent` (Clay 500). |
| Gesture | Horizontal drag inside the circle. Left = lower value, right = higher value. Like a horizontal mouse-scroll-wheel, not a rotational dial. |
| Drag-zone | The circle itself, not the whole panel. Prevents accidental activation from incidental touches elsewhere. |
| Sensitivity | ~20px of horizontal movement = one integer step. 200px total spans the full 1–10 range — comfortable within a 375px viewport, reachable without grip-change. |
| Live feedback during drag | The number in the centre updates per integer crossed (5 → 6 → 7), no decimals shown. Each integer-cross triggers a subtle scale-pulse on the number (1.0 → 1.05 → 1.0 in ~80ms) — the visual substitute for the haptic tick we'd otherwise have. |
| Commit | On release: snap to nearest integer = score commit → auto-advance to note. |
| Haptic | **Not in v1.** Web Vibration API is unsupported on iOS Safari (the author's primary device). Deferred to v2 once a native shim exists. The scale-pulse carries the rhythm without haptic. |
| Tick marks on rim | None. The centre number is the only readout. Clean visual; the user learns the gesture's range by feel. |

**Why this is "B with decorative circle" rather than pure iPod rotation:** rotation requires learning where 1 vs 10 sits around the rim. Horizontal drag is more discoverable from day one. The circle stays as a visual anchor (brand identity, sense of rest) but the gesture is linear.

---

## Note input

- Standard `<textarea>` in the middle region, surface-muted background, generous height
- Placeholder uses `copy.daily.note.placeholder` (currently "Schrijf hier je notitie…")
- No character counter, no required-field affordance, no length cap
- **Voice input is parked to v2** — no mic icon, no mode toggle in v1. The Claude-mobile anchor's voice-and-text-co-located dimension applies once voice is built; the persistent-thumb-zone dimension applies now.
- Auto-save debounces 1.5s after typing pauses (matches the existing Step 5 plan for NoteField)
- Forward button works on an empty note — typing is optional, not required to progress

---

## Tag input

Reuses the existing [Step 5 plan](../../features/daily-entry/step-5-note-and-tags-ui.md) for `TagCategoryList`:
- 4 primary category headers visible (mentaal / fysiek / overall / activiteit)
- "Extra opties (Interventie, Project, etc) ⌄" expands to reveal the remaining 4
- Each category header expands to show its chips inline; multiple may be expanded simultaneously
- Chip taps auto-save immediately (no explicit confirmation per tag)
- Forward button progresses to "Klaar" regardless of whether any tag is selected

The visual presentation lives inside the panel's middle region rather than as a stacked section on the page.

---

## Progression within the panel (moment 5)

**Hybrid progression** — different inputs have different completion semantics:

| Step | Progression rule |
|---|---|
| Score | **Auto-advance** ~500ms after the value commits (release → snap → pause → morph to note). No explicit forward button on this step — the gesture itself is the progression. |
| Note | **Explicit forward button** in the bottom region. User decides when they're done typing. Works on empty input (skips). |
| Tags | **Explicit forward button** in the bottom region. User decides when they're done selecting. Works with zero tags selected (skips). |
| Any step ≥ note | **Back button** also in the bottom region, symmetrically paired with forward. Returns to the previous step without losing input. |

Forward and back live in the **thumb zone** — both in the bottom region of the panel, never reaching to the top.

---

## End-of-flow

User taps "Klaar" after the final tag. Sequence:

1. Panel slides down (~250ms ease-out) — exits via the bottom edge of the viewport
2. As the panel reaches the bottom edge, **the today-card in the overview receives a one-shot tint-pulse**:
   - Background: `--color-surface` → `--color-surface` with a `--color-accent-soft` wash → back to `--color-surface`
   - Duration: ~400ms total
   - No scale, no glow, no checkmark, no text
3. Eye naturally follows: panel-downward motion → card-pulse — *spatial signal that the input now lives in that card*

This is a deliberate exception to the brief's original "no pulses" rule. See [Motion as communication](../brief.md#motion-as-communication) — the test passes: the pulse tells the user something they need to know ("your input is now there"), it's one-shot rather than ambient, and it lives on the destination not on the source.

---

## Morph between steps

Only the **middle region** of the panel morphs. The top region (drag-handle / date / X) and the bottom region (forward / back buttons) stay put as orientation anchors.

| Property | Value |
|---|---|
| Mechanism | Crossfade in-place |
| Outgoing | Opacity 1 → 0 over ~150ms, ease-in |
| Incoming | Opacity 0 → 1 over ~150ms, ease-out |
| Overlap | ~50ms — the panel is never visually "empty" |
| Spatial movement | None — no sliding, no resizing, no translation |
| Panel height | **Fixed throughout** — content variations get more or less whitespace, never resize the panel |
| Reduced motion | `prefers-reduced-motion: reduce` flattens all durations to 0.01ms (global default in `globals.css`) |

**Why crossfade rather than slide:** sliding implies "moving forward through screens", which is the form-shaped pattern this whole exploration is rejecting. Crossfade says "same place, different task" — reinforces the persistent-zone principle.

---

## Closing

Three ways the panel closes:

1. **Drag-down on the panel itself** — standard iOS sheet gesture, requires no explanation
2. **Tap the X in the top-right** — for keyboard / non-touch users; visual orientation, not the primary close path
3. **Natural completion** — after the last tag, "Klaar" tap → end-of-flow sequence

All three:
- Return the user to the day-overview (`/`)
- Auto-save preserves whatever has been entered up to that point
- Reopening (via tap on the relevant card-region) returns the user to the input with the entered state restored

---

## Past-day vs today distinction

| Surface | Today | Past day |
|---|---|---|
| Panel background | `--color-surface` (#FFFCF8) — warmer, lighter | `--color-surface-muted` (#F2EDE5) — cooler, flatter |
| Backdrop | Standard ~40% warm-dark wash | Same |
| Text labels | None — only the date in the top region | None — only the date in the top region |
| Affordances | Identical to today | Identical to today |

The tint is the **entire** distinguishing signal. No "Bewerken eerdere dag" subtitle, no warning colour, no icon. The user's eye registers the tint shift in well under 500ms without conscious effort — faster than reading any label, and it requires no cognitive parsing on a brainfog day.

The data-integrity concern (user typing into the wrong day by accident) is satisfied because (a) the tint reads instantly, and (b) the date in the top region always shows which day is being edited.

---

## Tension with current code

[Step 4b](../../features/daily-entry/step-4b-score-row-and-save-relocation.md) is currently in flight. It builds a horizontal score row at the top of `TodayShell`, with `SaveStatus` relocated to the page header.

If this exploration matures into a build decision:

- **The horizontal score row layout becomes incompatible** with the persistent-panel pattern. The score-row lives in the upper-middle of the screen, not in the thumb zone.
- **The hoisted `useDayEntryUpsert` and `SaveStatus variant` work in 4b is still reusable** — the hook and the status component are framework-level, not layout-specific.
- **The `TagCategoryList` from Step 5** is also reusable — same 4+4 split mechanic, just rendered inside the panel rather than as a stacked page section.

Resolution is deferred. This document captures the alternative direction so it can be evaluated against the current direction before a build commitment is made.

---

## Validation log

Real-device milestones for this exploration, oldest first.

- **2026-05-28 — Score-circle gesture validated on iPhone PWA.** Throwaway prototype at [`score-circle-prototype.html`](score-circle-prototype.html) tested in iOS Safari standalone mode. Confirmed: smooth horizontal drag, snap-to-integer, 80ms scale-pulse per integer crossed, gesture isolation between circle and sheet (handle-only dismiss works), no scroll conflicts, `touch-action: none` + `setPointerCapture()` behave correctly. Native pointer events were sufficient — `@use-gesture/react` is now an ergonomic choice for the production build, not a feasibility one. The validated defaults (280px circle, 20px per integer, 80ms pulse) stand.
- **2026-05-28 — Expanded flow prototype tested on desktop.** Throwaway prototype at [`quick-entry-flow-prototype.html`](quick-entry-flow-prototype.html) covers the full flow: auto-appear on empty today, score → note → tags morph, back/forward in thumb zone, end-of-flow tint-pulse on the today-card, past-day editing with surface-muted tint, today-card region-tap to reopen at a specific step. Desktop pass confirmed:
  - ✓ Crossfade morph between steps feels natural (not jarring)
  - ✓ Today-card tint-pulse on completion registers as spatial confirmation
  - ⏳ iOS keyboard handling during the note step (via `visualViewport` API) — deferred to post-deploy
  - ⏳ Morph quality and pulse quality on actual touch device — deferred to post-deploy

  **Mobile validation deferred to post-build/deploy.** Testing locally on the iPhone requires friction (separate static server on the LAN) that doesn't pay off vs deploying the real feature and validating there.

## What still needs work before any build

These are real open items for any future implementation:

- **Animation library** — Framer Motion vs View Transitions API vs vanilla CSS. For the panel morph, the end-of-flow card pulse, and the panel slide. Bundle-size and maintenance trade-offs.
- **Sheet primitive** — Vaul vs Headless UI vs custom. The handle-only dismiss pattern is validated and Vaul supports it out of the box; the question is whether its other opinions match ours.
- **Layer 3 (moment of use)** — where / when / in what body-state the user opens this. Likely surfaces additional constraints (e.g. does the panel height need to adjust when the iOS keyboard is open for the note step?).
- **Voice input v2 design** — a separate exploration once v1 lands.
- **Keyboard handling for the note step** — does the iOS keyboard push the panel up? Cover the back/forward buttons? Needs prototyping on a real device.
- **First-time user discoverability** — the panel auto-appears on a fresh day, but the user needs to understand "drag horizontally on the circle". Is a one-time hint label needed? Probably yes, fading after first successful use.

---

## Source

This document captures a focused design conversation on **2026-05-28**. The conversational thread moved through five layers (feel → references → moment-of-use partially → motions → technical pending). Two general design principles were extracted and added to the project brief in the same session:

- [Spatial principle: thumb-first for input](../brief.md#spatial-principle-thumb-first-for-input) (memory: [design_principle_thumb_first_input.md](../../../../../../../.claude/projects/C--Users-Gebruiker-Documents-gevoelscore-app/memory/design_principle_thumb_first_input.md))
- [Motion as communication](../brief.md#motion-as-communication)

The specific UX spec for this surface lives here.
