# Quick-entry popout

**Feature:** A persistent thumb-zone bottom-sheet for daily input. Replaces the form-shaped Today shell (score row + note + tag accordion stacked on a scrollable page) with a single sheet that lives in the thumb zone and morphs between score → note → tags steps. The interface comes to the thumb, not the other way around.
**Version:** v1 (alternative implementation path)
**Status:** Plan landed 2026-05-28 after a focused design exploration. Spec at [`docs/design/explorations/quick-entry-popout.md`](../../design/explorations/quick-entry-popout.md). Two throwaway HTML prototypes validated the gesture (iPhone PWA) and the full flow visual structure (desktop). Build decision: pending — depends on whether this supersedes the in-flight Step 4b horizontal score row in `daily-entry/`, or coexists.
**Parent docs:** [REQUIREMENTS.md](../../REQUIREMENTS.md) · [design/brief.md](../../design/brief.md) · [design/explorations/quick-entry-popout.md](../../design/explorations/quick-entry-popout.md) · [daily-entry/README.md](../daily-entry/README.md)

---

## Why this feature exists

The `daily-entry/` feature solves the cardinal-principle requirements correctly. It is also **form-shaped**: controls are distributed across a scrollable page, the user's thumb travels across the screen, and grip shifts as you move from score to note to tags. That's the conventional pattern. It works.

This feature explores an alternative shape: a single persistent **bottom-sheet at thumb height** where score, note, and tags morph in place. The user's hand stays put; the interface arrives where it already is.

Two design principles drive the difference:

1. **Spatial principle: thumb-first for input** (see [brief](../../design/brief.md#spatial-principle-thumb-first-for-input)). Input surfaces live in the bottom of the viewport. The interface comes to the thumb.
2. **Motion as communication** (see [brief](../../design/brief.md#motion-as-communication)). Motion exists to mark meaningful moments — completion, state change, spatial arrival — never as decoration.

The motivating user phrase: *"ideally, it is just a series of taps while you hold your phone in your hand. Every time, the new input is perfectly located at tapping height for your thumb."*

## Position relative to soak-test mode

The project memory entry `Soak-test mode` notes: *"daily-entry deployed 2026-05-28, user installed as iOS PWA; wait for friction signal before proposing new screens."*

This feature proceeds despite that memory, deliberately:

- The exploration was **user-initiated** during a design conversation, not proposed unsolicited
- This is an **alternative implementation** of the existing daily-entry surface, not a *new* screen — the memory's intent is to avoid feature-creep, not to freeze the existing surface against design improvements
- Two principles emerged from the exploration ([thumb-first for input](../../design/brief.md#spatial-principle-thumb-first-for-input) and [motion as communication](../../design/brief.md#motion-as-communication)) that improve the project regardless of which UI direction ultimately wins
- The build is structured so it does not displace `daily-entry/` Step 4b work until an explicit decision in this feature's Step 4

If post-deploy soak-test of `daily-entry/` reveals that the current direction works well enough that this feature isn't needed, Steps 0–3 still yield reusable primitives (hooks, bottom-sheet, score-circle) and Step 4 can defer indefinitely.

---

## Relationship to existing daily-entry work

This feature was conceived **after** `daily-entry/` Steps 0–4 had shipped and Step 4b (horizontal score row + save-status relocation) was in flight. The two directions are not currently compatible:

| Daily-entry direction | Quick-entry-popout direction |
|---|---|
| Today-shell as scrollable page with stacked score / note / tags sections | Single bottom-sheet that morphs between score / note / tags steps in place |
| Horizontal score row at the top of the Today shell (Step 4b) | Score circle inside the sheet, in the thumb zone |
| `<SaveStatus>` relocated to the page header (Step 4b) | `<SaveStatus>` not needed in the sheet header — completion is communicated by the today-card tint-pulse at end of flow |
| Tags as 4-primary + Extra-opties stacked headers on the page (Step 5) | Same 4+4 grouping, rendered inside the sheet's tags step |

**Reusable across both directions:**
- `useDayEntryUpsert(date)` hook (Step 4)
- `<SaveStatus>` component variants (Step 4b)
- `<TagCategoryList>` component (Step 5) — same UI, different container
- Domain layer (validators, types) — entirely unchanged
- `/api/day-entries/[date]` PUT route (Step 3) — entirely unchanged

**A decision point exists at the end of this feature's Step 4**: does the quick-entry-popout supersede Step 4b's score row, or do both coexist (e.g. popout as a toggleable preference)? Resolution deferred to that step's plan.

---

## What this feature ships

Five steps, mostly UI work. Backend APIs are already shipped via `daily-entry/` Steps 1–3.

1. **Shared primitives** — focus trap, body scroll lock, visual-viewport hook (iOS keyboard), step-morph hook. Reusable across the rest of the app.
2. **BottomSheet primitive** — sheet shell with handle-only drag-to-dismiss, backdrop, slide transitions, surface-tint variants. Pure presentational.
3. **ScoreCircle component** — circular touch surface with horizontal-drag gesture, snap-to-integer, scale-pulse per integer cross. Native pointer events, no library dep.
4. **QuickEntryFlow composite** — orchestrates ScoreCircle + NoteField + TagCategoryList inside BottomSheet, with the step morph, back/forward buttons in the thumb zone, and end-of-flow tint-pulse on the target card.
5. **TodayShell integration + past-day editing** — today-card with three tappable regions, auto-appear on empty today, past-day cards in "Vorige dagen", surface-muted tint when editing past. Reconciliation decision with Step 4b.

**What this feature does NOT ship:**
- Voice input (parked to v2 per the spec)
- Haptic feedback on integer-cross (Web Vibration API unsupported on iOS Safari; parked to v2 once a native shim exists)
- Tag picker for the v1.5 "Extra opties" categories beyond the 4 primary (those expand inline but full management lives in v1.5 Settings)
- End-of-day reminder (already v2 per REQUIREMENTS)

---

## Acceptance criteria

Numbered to match the spec section they implement. Each step's own AC list expands on these.

### The sheet itself

- [ ] AC1: The sheet appears as a bottom-positioned panel with rounded top corners (28px) and a soft single-direction shadow. Width clamps to 480px and centres on larger screens. Middle region (the morphing content area) has a **fixed height of 380px** to accommodate the 280px score circle plus padding. Total sheet height (handle + header + middle + footer + safe-area) lands around 55–65% of viewport on typical phones; specific px values per phone are an implementation detail, but the fixed-middle-region rule is the contract.
- [ ] AC2: Sheet height is **fixed** throughout the flow. Content variations get more or less whitespace; the panel never resizes between steps.
- [ ] AC3: Sheet uses `--color-surface` (#FFFCF8) when editing today's entry, `--color-surface-muted` (#F2EDE5) when editing a past day. No text label distinguishes the two — tint is the entire signal.
- [ ] AC4: A 36×4px handle bar at the top of the sheet is the **only** affordance that initiates drag-to-dismiss. The body of the sheet does not accept dismiss gestures. This isolates the score-circle's horizontal drag from the sheet's vertical dismiss.
- [ ] AC5: Backdrop click closes the sheet. Escape key closes the sheet. Both restore focus to the element that opened the sheet.
- [ ] AC6: When the iOS keyboard rises (during the note step), the sheet anchors to the visible viewport bottom via the `visualViewport` API so the panel and its buttons stay above the keyboard.

### Trigger moments

- [ ] AC7: App opens, today has no entry → sheet **auto-appears** on score step. No tap to summon.
- [ ] AC8: App opens, today is already filled → no sheet. Day-overview only.
- [ ] AC9: Tap on a region of the today-card (score / note / tags) → sheet opens at **that specific mode**. Spatial: the tapped region is where the panel comes from.
- [ ] AC10: Tap on a past-day card → sheet opens at score mode with `--color-surface-muted` tint.

### Score step

- [ ] AC11: A decorative circle (~280px diameter, max 80vw, capped to viewport) sits in the centre of the sheet's middle region. The current score is rendered very large in the centre of the circle (display-size, weight 600, `--color-accent`).
- [ ] AC12: Horizontal drag inside the circle changes the value: left = lower, right = higher. ~20px per integer step (200px total spans 1–10). The circle is the touch surface; the rest of the sheet body is not.
- [ ] AC13: The number in the centre updates per integer crossed during drag (5 → 6 → 7, no decimals shown). Each integer-cross triggers an 80ms scale-pulse (1.0 → 1.05 → 1.0) on the number.
- [ ] AC14: On pointer release, value snaps to the nearest integer = commit. The committed value persists in component state. Auto-advance to the note step after ~500ms.
- [ ] AC15: Keyboard accessibility: `ArrowLeft`/`ArrowRight` (and `ArrowDown`/`ArrowUp` as aliases) increment / decrement; `Home` = 1, `End` = 10. The circle has `role="slider"` with `aria-valuemin/max/now`.
- [ ] AC16: No tick marks visible on the circle's rim. No labels at "1" or "10". The centre number is the only readout.

### Step morph

- [ ] AC17: Steps morph via **crossfade in place**. Outgoing step fades to opacity 0 in ~150ms (ease-in); incoming fades to opacity 1 in ~150ms (ease-out). 50ms overlap so the middle region is never empty.
- [ ] AC18: Only the **middle region** of the sheet morphs. The header (date, X close) and the footer (back / forward buttons) stay put as orientation anchors.
- [ ] AC19: `prefers-reduced-motion: reduce` flattens all durations to 0.01ms.

### Note step

- [ ] AC20: A textarea fills the middle region with `--color-surface-muted` background, soft border, generous height. Placeholder `copy.daily.note.placeholder`.
- [ ] AC21: Forward button text: `Volgende: tags`. Back button text: `← Score`. Both in the thumb zone (sheet footer).
- [ ] AC22: Forward button works on an empty note (skips). Back button returns to score step with the saved value visible in the circle.

### Tags step

- [ ] AC23: The 4 primary category headers (mentaal / fysiek / overall / activiteit) are visible. Below them, an `Extra opties (Interventie, Project, etc) ⌄` toggle expands the remaining 4 in place.
- [ ] AC24: Each category header expands to show chips inline. Multiple categories may be expanded at once. Selection count badge appears on a header when ≥1 chip in it is selected.
- [ ] AC25: Forward button text on this step: `Klaar ✓`. Tapping it commits any remaining state and triggers the end-of-flow sequence.

### End of flow

- [ ] AC26: Sheet slides down (~250ms ease-out). As the sheet reaches the bottom edge of the viewport, the target card (today-card or the relevant past-day card) receives a one-shot tint-pulse: `surface → surface with accent-soft wash → surface`, ~400ms total.
- [ ] AC27: No text confirmation, no checkmark icon flash, no green success colour. The tint-pulse is the entire signal.
- [ ] AC28: The today-card immediately shows the committed values (score, note, tags) — auto-save has already persisted them during the flow.

### Auto-save semantics

- [ ] AC29: Every field change auto-saves (per existing `useDayEntryUpsert` contract from `daily-entry/` Step 4). Score auto-saves on commit. Note debounces 1.5s after typing pause. Tag toggles save immediately.
- [ ] AC30: Drag-down dismiss or backdrop close mid-flow does **not** lose data. Whatever was entered is auto-saved; reopening at the matching region returns the saved state.

### Accessibility

- [ ] AC31: Sheet meets WCAG 2.2 AA. Focus moves into the sheet on open, traps within it, returns to the trigger element on close. Score circle is keyboard-operable per AC15. All interactive elements have visible focus rings (`:focus-visible`).
- [ ] AC32: `axe-core` Playwright scan on the sheet at each step (score / note / tags) returns zero AA violations.

---

## Standards-enforcement

| Concern | Applies? | Note |
|---|---|---|
| New route handler | No | Reuses `/api/day-entries/[date]` from `daily-entry/` Step 3 |
| New collection / schema | No | Reuses `day_entries` and `tags` |
| New dependency | **No** | Native pointer events, vanilla CSS transitions, custom sheet — see [technical-decisions](#technical-decisions). Zero new deps in `package.json`. |
| `dangerouslySetInnerHTML` | No | — |
| New env var with secret | No | — |
| New telemetry / observability dep | No | Cardinal "no unsolicited notifications / analytics / tracking" preserved |
| OAuth / browser permissions | No | No new permissions; visualViewport API is implicit |

---

## Technical decisions

Resolved during the design exploration on 2026-05-28. See the conversation history captured in [the spec doc](../../design/explorations/quick-entry-popout.md) for the reasoning.

| Concern | Decision | Bundle impact |
|---|---|---|
| Gesture handling | Native Pointer Events (no library) | 0 KB |
| Animation library | Vanilla CSS transitions + React state (no library) | 0 KB |
| Sheet primitive | Custom `<BottomSheet>` component (~200 lines including hooks) | 0 KB |
| Focus / a11y plumbing | Custom hooks (`useFocusTrap`, `useBodyScrollLock`, `useVisualViewport`) | 0 KB |
| **Total new deps** | **None** | **0 KB** |

Reasoning:
- The motion inventory (opacity, transform, background-colour transitions) is entirely GPU-accelerated CSS primitives. No spring physics needed (brief forbids celebratory motion).
- The score-circle gesture was validated on iPhone PWA with native pointer events — no library required.
- The handle-only drag-to-dismiss pattern was validated in the HTML prototype.
- Bundle weight matters for a brainfog-friendly PWA; zero deps = fastest first paint.

---

## Component architecture

```
QuickEntryFlow                            (orchestrator; lives in TodayShell)
 ├─ BottomSheet                           (presentational shell — primitive)
 │   ├─ <handle>                          (the only drag-dismiss zone)
 │   ├─ <header>                          (date, close X — orientation only)
 │   ├─ <middle>                          (fixed-height, morphing region)
 │   │   ├─ ScoreStep
 │   │   │   └─ ScoreCircle               (horizontal drag, snap, pulse)
 │   │   ├─ NoteStep
 │   │   │   └─ NoteField                 (reused from daily-entry/Step 5)
 │   │   └─ TagsStep
 │   │       └─ TagCategoryList           (reused from daily-entry/Step 5)
 │   └─ <footer>                          (back + forward buttons, thumb zone)
 │
 ├─ useStepMorph                          (manages active vs rendered step)
 ├─ useFocusTrap                          (a11y; captures focus on open)
 ├─ useBodyScrollLock                     (prevents background scroll)
 └─ useVisualViewport                     (iOS keyboard anchor)
```

Shared with `daily-entry/` Step 4:
- `useDayEntryUpsert(date)` — same save semantics across both directions
- `<SaveStatus>` — used inline for in-flow indication if a save fails (banner variant); the glyph variant is not needed inside the sheet since end-of-flow has the card-pulse signal

---

## Steps

0. **[Step 0 — Shared primitives foundation](step-0-shared-primitives.md)** — `useFocusTrap`, `useBodyScrollLock`, `useVisualViewport`, `useStepMorph`. Pure hooks with Vitest unit tests. Prerequisite for every UI step. Reusable across the rest of the app (settings dialogs, future bottom-sheets).
1. **[Step 1 — BottomSheet primitive](step-1-bottom-sheet.md)** — `<BottomSheet>` component with handle-only drag-to-dismiss, slide transitions, backdrop, surface-tint variants. Pure presentational. Reused by every input flow.
2. **[Step 2 — ScoreCircle component](step-2-score-circle.md)** — Circular touch surface with horizontal-drag gesture, snap-to-integer, scale-pulse. Native pointer events. Does not know about save semantics.
3. **[Step 3 — QuickEntryFlow composite](step-3-quick-entry-flow.md)** — Orchestrates ScoreCircle + NoteField + TagCategoryList inside BottomSheet, with step morph, back/forward, end-of-flow tint-pulse. **Hard prerequisite: `daily-entry/` Step 5 must ship first** (provides `<NoteField>` and `<TagCategoryList>`). Steps 0, 1, 2 of this feature can run in parallel with the other programmer's Step 5 work; Step 3 waits.
4. **[Step 4 — TodayShell integration + past-day editing](step-4-integration-and-past-day.md)** — Today-card with tappable regions, auto-appear on empty today, past-day cards, surface-muted tint. Reconciliation decision with Step 4b.
5. **[Step 5 — Reconciliation and cleanup](step-5-reconciliation.md)** — Resolve the Step 4b tension, remove superseded code (if applicable), update `daily-entry/` README cross-refs, post-deploy mobile validation.

Steps 0 and 1 are **fully detailed and ready for `/build-step`**. Steps 2–5 are outlined; full detail will be filled in as we approach each one (or on demand).

Each step follows the strict RED → GREEN → REFACTOR loop via `/build-step`.

---

## Verification

- **Automated**: Vitest grows by ~25 tests across the five steps (4 hooks + sheet + circle + flow composite).
- **Playwright**: new spec `tests/e2e/quick-entry-popout.spec.ts` covers auto-appear, full flow, past-day tint, axe-core a11y scan.
- **Manual walkthrough** (cardinal-principle gate): one-handed, arm's length, low light, on the phone. Stopwatch the tap-to-score flow at ≤ 5s on a good-day simulation. Brainfog simulation (delay between intention and motor action — read but don't act for 2s — verify the flow doesn't time out / require re-tapping). Network-throttled connection to verify auto-save isn't blocking.
- **Real-device validation log**: per the spec doc's "Validation log" section. Three confirmed pre-build (gesture, morph, pulse on desktop); the rest depend on post-deploy mobile testing.

---

## Cardinal-principle impact

| Principle | Impact | How we stay inside |
|---|---|---|
| One-tap entry | This *is* the principle — score tap saves the day | Auto-appear on empty today, drag-and-release on circle = one continuous gesture |
| Sub-10-second flow | The thing that gets measured | Stopwatch at end of step 4's walkthrough |
| Brainfog-friendly | Daily reality | Thumb-first principle is brainfog accommodation made literal |
| No unsolicited notifications / ads / analytics | Enforced | Zero new deps; ESLint rule from `daily-entry/` still blocks Sentry/PostHog/Vercel Analytics |
| User-owned data | Directus on Fly + Neon | No new endpoints, no new storage |
| Export / delete still works | Unblocked | Schema unchanged; reuses existing data paths |

---

## Alternatives considered

### Decision: Quick-entry popout vs `daily-entry/` Step 4b horizontal score row

- **Chose:** explore the popout direction in parallel with the in-flight Step 4b work. Build-or-not decision deferred to Step 4 of this feature plan.
- **Considered and rejected as the only path:** committing fully to Step 4b's direction would have foreclosed the thumb-first exploration. The exploration produced two new general principles for the brief (thumb-first input, motion as communication) that improve the project regardless of which UI direction wins.
- **When to revisit:** at the end of Step 4 of this feature plan, with both implementations testable on the deployed app.

### Decision: native pointer events vs `@use-gesture/react`

- **Chose:** native Pointer Events.
- **Reasoning:** the HTML prototype proved the gesture works at ~50 lines of vanilla JS. Adding `@use-gesture/react` (~9 KB) would be ergonomic-only, not feasibility.
- **When to revisit:** if v1.5 introduces more complex gesture compositions (e.g. multi-touch on the timeline), reconsider as part of that work.

### Decision: vanilla CSS vs Framer Motion

- **Chose:** vanilla CSS transitions + React state.
- **Reasoning:** the motion inventory is all opacity / transform / background — native CSS primitives, GPU-accelerated. Framer Motion's value-add (spring physics) is forbidden by the brief.
- **When to revisit:** v1.5 timeline chart animations may benefit; reconsider then.

### Decision: custom sheet vs Vaul

- **Chose:** custom `<BottomSheet>`.
- **Reasoning:** Vaul drags Framer Motion in as a peer dep (~31 KB net). With the vanilla CSS decision above, Vaul's bundle math no longer favours it. The prototype validated the handle-only drag pattern in ~30 lines.
- **When to revisit:** if multiple bottom-sheets ever need to overlay each other, Vaul's stacking management becomes worth the dep.

---

## Privacy & permissions

- No new OAuth scopes
- No new browser permissions (visualViewport API is implicit)
- No new third-party endpoints
- No new data collected — reuses the existing `DayEntry` schema entirely
- Export and full-delete paths unchanged (covered by `daily-entry/`)
