# Step 4: TodayShell integration + past-day editing

**Estimated time:** 2.5 hours
**Test layer:** Vitest component tests for the today-card region taps, the auto-appear behaviour, and the past-day card tap. Playwright e2e for the full integrated screen with real Directus data.
**Risk:** Medium-High. This is the step where the new direction meets the existing app. Touches `src/app/page.tsx` and `src/components/today-shell.tsx`. The reconciliation decision with `daily-entry/` Step 4b lives here.
**Prerequisite:** [Steps 0, 1, 2, 3](README.md#steps) shipped. The `<NoteField>` and `<TagCategoryList>` from `daily-entry/` Step 5 must also be available.

> **Status: outline.** Full step detail will be filled in as we approach `/build-step` — particularly the reconciliation decision below, which needs to be made (or explicitly deferred) before this step lands.

---

## Scope summary

Wire `<QuickEntryFlow>` into the actual app. Specifically:

1. **Restructure `TodayShell`** so the today-card has three tappable regions (score / note / tags). Each region tap opens `<QuickEntryFlow>` at the matching step.
2. **Auto-appear** the sheet on initial render when today has no entry (`entry === null`).
3. **Render past-day cards** in a `Vorige dagen` section beneath the today-card. Each past-day card tap opens `<QuickEntryFlow>` with `isPastDay=true`.
4. **End-of-flow pulse** on the target card when `onComplete()` fires from QuickEntryFlow.

---

## Acceptance criteria

Inherited from feature README AC7–AC10 and AC26–AC28:

- [ ] AC1 (== README AC7): App opens, today empty → sheet auto-appears on score step
- [ ] AC2 (== README AC8): App opens, today filled → no sheet, overview only
- [ ] AC3 (== README AC9): Tap score region of today-card → sheet opens at score step. Tap note region → note step. Tap tags region → tags step.
- [ ] AC4 (== README AC10): Tap past-day card → sheet opens with surface-muted tint, score step
- [ ] AC5 (== README AC26): Klaar → sheet slides down. As it reaches bottom, the target card (today or past) receives a one-shot tint-pulse: `surface → surface with accent-soft wash → surface`, ~400ms total
- [ ] AC6 (== README AC27): No text confirmation, no checkmark, no green
- [ ] AC7 (== README AC28): Target card immediately shows the committed values

Additional:

- [ ] AC8: Past-day cards in "Vorige dagen" — **3 most-recent days visible by default**, with a `Toon meer` text-button below that reveals an additional 7 days inline (10 total). Each card shows date / score / note-preview (truncated to ~50 chars). The 3-default keeps the overview brainfog-friendly; the expand is one tap when needed.
- [ ] AC9: Past-day data fetched server-side (matches existing `daily-entry/` Step 1 read API pattern). Page is a server component; the QuickEntryFlow client wrapper receives initial state via props. Fetch the most recent 10 entries; the `Toon meer` toggle is purely client-state, no second fetch.
- [ ] AC10: Pulse animation respects `prefers-reduced-motion` (already global default in `globals.css`)

---

## Reconciliation decision with `daily-entry/` Step 4b

This is the step where we decide:

**Option A — QuickEntryFlow replaces the in-flow Step 4b score row entirely.**
- Remove `<ScoreRow>` from `<TodayShell>`
- Remove `<SaveStatus>` from the page header (no longer needed — end-of-flow pulse is the signal)
- Existing tests for the horizontal score row become invalid; they get removed or rewritten
- `daily-entry/` README's "Steps" section gets updated to note that Step 4b is superseded by `quick-entry-popout/` Step 4

**Option B — Coexist behind a preference toggle.**
- Both implementations live in the codebase
- A user preference (Settings) toggles between "Classic" (Step 4b) and "Popout" (this feature)
- More code to maintain; more tests to keep green; more user-facing complexity
- Probably only worth it if real-device testing on the popout reveals issues we can't fix in v1

**Option C — Defer the decision.**
- Land this step as `/lab/quick-entry-popout` only — does not touch `src/app/page.tsx`
- The popout lives at a separate route accessible only by direct URL
- User tests it on the deployed app via that route; if it wins, a follow-up step replaces the home flow
- Most conservative; defers the breaking change

**Decision is required before this step starts.** Suggested default: **Option C** for the initial build (least disruption to existing tests and the other programmer's in-flight work), with a follow-up Step 5 that promotes to home if validation passes.

---

## Test plan (stub)

### `src/components/__tests__/today-shell.test.tsx` (updates)

Adds cases:
- Today-card score region click → opens QuickEntryFlow at `startStep='score'`
- Today-card note region click → opens at `startStep='note'`
- Today-card tags region click → opens at `startStep='tags'`
- Past-day card click → opens with `isPastDay=true`
- Auto-appear on `entry === null`

### `tests/e2e/quick-entry-popout-integrated.spec.ts` (new)

- Full session: log in → today empty → sheet auto-appears → complete flow → today-card pulses → tap past day → edit → close
- axe-core scan on the integrated page

---

## Done criteria

- [ ] `<TodayShell>` updated to host the today-card-with-regions and past-day list (per the chosen reconciliation option)
- [ ] `<QuickEntryFlow>` integrated; opens on auto-appear + region taps + past-day taps
- [ ] End-of-flow pulse implemented (CSS class toggled via state, ~400ms duration)
- [ ] Vitest count delta: +5–8 (depending on reconciliation option)
- [ ] Playwright count delta: +2
- [ ] `npm run verify` clean
- [ ] **Reconciliation decision documented in the step's Done section** — which option was chosen and why

---

## Open questions to settle during implementation

- **Reconciliation option:** see above. Decide before starting.
- **Region-tap affordances on the today-card:** the prototype showed an Edit pencil icon on each region. Spec brief forbids decorative icons in chrome; but a small functional edit icon is arguably non-decorative since it communicates "this region is editable". Decision: include it, small (16px), `fg-subtle` color, only visible on hover/focus.
- **Empty-state in today-card before any entry:** how does the today-card look when nothing has been entered yet? The auto-appear sheet covers most of the screen — but the card behind it still needs an empty state. Match the placeholder pattern from the existing `today-shell.tsx` ("nog niet ingevuld" etc.).
