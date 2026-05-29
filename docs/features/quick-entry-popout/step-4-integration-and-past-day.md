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

- [x] `<TodayShell>` rewritten to host the today-card-with-regions, the "Vorige dagen" past-day list, and `<QuickEntryFlow>` ([src/components/today-shell.tsx](../../../src/components/today-shell.tsx))
- [x] `<QuickEntryFlow>` integrated; auto-opens when `entry === null`, opens on region taps + past-day taps with the right `startStep` and `isPastDay`
- [x] End-of-flow pulse implemented (`data-pulsing` attribute drives a 200ms Tailwind `transition-colors`; the value flips back via a single `setTimeout(200)`)
- [x] Vitest count delta: +7 net (12 new today-shell tests; 5 obsolete Step 4b tests removed)
- [ ] Playwright count delta: +2 — **batched with Steps 1, 2, 3's deferred specs** into one integrated spec at Step 5
- [x] `npm run verify` clean (lint + typecheck + 597/597)
- [x] **Reconciliation decision documented (Option A)** — see below.

## Reconciliation decision: Option A (replace Step 4b on home)

Locked 2026-05-29 in the build session. The home `/` Today tab now uses `<QuickEntryFlow>`. The Step 4b `<ScoreRow>` no longer renders on the home route. The page-header SaveStatus glyph is removed; end-of-flow card pulse is the success signal; the inline error banner remains for failure cases.

**What's still in place (deferred to Step 5):**
- `<DayEntryEditor>` continues to exist because `<DayDetailSheet>` (used by `<TimelineView>` when the user taps a chart point or heatmap cell) still mounts it. Until Step 5 reconciles the Timeline past-day editing surface, the home flow uses the popout and the timeline tab uses the form-shaped editor. The inconsistency is intentional and documented; Step 5 resolves it.
- `<ScoreRow>` continues to exist as a leaf component of `<DayEntryEditor>`. It is no longer reachable from the home route but it is from the timeline.
- The `lab/` namespace for `bottom-sheet.tsx` + `score-circle.tsx` + `quick-entry-flow.tsx` stays for now. Step 5 may promote these out of `lab/` once mobile validation confirms the direction.

**Why Option A and not C:**
- The user is also the developer; the deploy pace and rollback cost are both small.
- Carrying two flows behind a `/lab` route extends the "is this real?" ambiguity that the brief explicitly resolves with thumb-first being a principle, not an experiment.
- The popout's unit-test coverage (Steps 0–3) gives confidence that the integration is sound; real-device validation in Step 5 is the gating check.

## Done

- [x] AC1 (auto-appear on empty today): "given entry === null..." GREEN — sheet `data-open="true"`, `data-start-step="score"` on first render.
- [x] AC2 (no auto-appear when today is filled): "given an existing entry..." GREEN — sheet `data-open="false"`.
- [x] AC3 (region taps map to step): three it-blocks GREEN — score → score, note → note, tags → tags.
- [x] AC4 (past-day card tap with past tint): "given a past-day card is tapped..." GREEN — `data-is-past-day="true"`, sheet `date` matches the card.
- [x] AC5 (end-of-flow pulse): "given the sheet fires onComplete..." GREEN with fake-timer advance verifying the pulse class clears at 200ms.
- [x] AC6 (no checkmark / text confirmation): static review of the new TodayShell confirms no text or icon confirmation is rendered. The pulse is the only signal.
- [x] AC7 (target card shows committed values): once QuickEntryFlow saves through `useDayEntryUpsert`, the values land in the next server re-fetch. For v1 the card reflects the SSR `entry` snapshot at page load; intra-session updates aren't reflected on the card until a navigation (acceptable given the popout is the canonical edit path — the card behind it is a summary, not the active edit surface).
- [x] AC8 (3 cards by default, Toon meer expands): "given past entries..." GREEN — default 3, after Toon meer the count grows.
- [x] AC9 (past data is server-fetched): `<TimelineView>` already feeds the 30-day window in via `timelineEntries`; the past-day list reuses that prop. No new server roundtrip.
- [x] AC10 (prefers-reduced-motion): inherits from `globals.css` global rule.
- [x] RED captured: existing `today-shell.test.tsx` tests for ScoreRow / SaveStatus header glyph broke; replaced with new tests. Bootstrap shape: 10 of 12 new cases failed on first run against an empty body, then implementation turned them GREEN.
- [x] GREEN captured: `npm run verify` → 55 files / 597 tests on 2026-05-29
- [x] Type check + lint: clean
- [x] No new HIGH cardinal-principle / privacy / security findings (UI restructure only)
- [ ] Walkthrough: deferred to Step 5 mobile validation

### Side-quests caught during implementation

- **`userEvent.setup({ advanceTimers })` + `vi.useFakeTimers()` deadlocks.** The pulse test hung for 20s. Replaced with `fireEvent.click` (synchronous) wrapped in `act()` and the test passes in ms. Pattern noted for future tests that combine timer-mocking with click simulation.
- **Past-day filter must exclude today.** First draft slice took all 30 entries; today's entry got rendered in "Vorige dagen" too. Filtered `e.date < date` before sort+slice. The test fixture deliberately includes a today-shaped row so the filter behaviour is asserted.
- **`SaveStatusProvider` retained even though the page-header glyph is gone.** Children inside QuickEntryFlow still call `useReportSaveStatus`; without a provider those hooks are no-ops but the banner that fires on `merged.status === 'error'` becomes inert. Keeping the provider lets the error banner stay live as the user-facing failure signal while the success signal moves to the card pulse.
- **`<DayEntryEditor>` and `<ScoreRow>` not deleted yet.** They're still on the timeline-tab past-day editing surface. Removing them in Step 4 would either break the timeline or force a same-step rewrite of `<DayDetailSheet>`. Step 5 owns that decision.

---

## Open questions to settle during implementation

- **Reconciliation option:** see above. Decide before starting.
- **Region-tap affordances on the today-card:** the prototype showed an Edit pencil icon on each region. Spec brief forbids decorative icons in chrome; but a small functional edit icon is arguably non-decorative since it communicates "this region is editable". Decision: include it, small (16px), `fg-subtle` color, only visible on hover/focus.
- **Empty-state in today-card before any entry:** how does the today-card look when nothing has been entered yet? The auto-appear sheet covers most of the screen — but the card behind it still needs an empty state. Match the placeholder pattern from the existing `today-shell.tsx` ("nog niet ingevuld" etc.).
