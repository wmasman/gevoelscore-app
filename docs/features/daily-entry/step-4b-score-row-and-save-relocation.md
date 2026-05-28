# Step 4b: Score row redesign + save-status relocation

**Estimated time:** 1.5 hours
**Test layer:** Vitest component (jsdom) for the row state machine + Playwright e2e for horizontal-axis interaction against the dev server.
**Risk:** Medium. Touches the cardinal-principle screen post-ship. Most of Step 4's interaction model and save semantics are preserved; only the layout axis and the indicator position change. The horizontal thumb-reach on a phone held in bed is untested and is the single thing the phone-walkthrough must confirm.
**Prerequisite:** [Step 4](step-4-score-tap-ui.md) done. This step builds on Step 4's shipped state machine, hook, and component primitives — it does not redo them.

> Reshapes the cardinal screen to match the locked design at [docs/design/brief.md](../../design/brief.md). The score selector pivots from a vertical scroll-snap wheel to a horizontal scroll-snap row. The `<SaveStatus />` indicator relocates from inside the score component to the top-right of the page header. Component renamed `score-wheel` → `score-row` to match its new shape. Interaction model, save semantics (debounce / abort / no-op-on-same-value), keyboard handling, and accessibility are preserved — the change is intentionally surgical.

---

## Acceptance criteria

- [ ] AC1: `<ScoreRow>` renders 10 numbered buttons in a horizontal scroll-snap row inside a container that is ≤ the editor's max-width (~432px after page padding), ~80px tall, 8px corner radius, 1px border `var(--color-border)`. The container has `scroll-snap-type: x mandatory; overflow-x: auto; overflow-y: hidden`.
- [ ] AC2: Each button is 48×48 (brainfog tap target ≥ 48). Centred-in-`set` state: 2px ring in `var(--color-accent)` (Clay 500), 24px Inter weight 600, primary text color, no fill. Centred-in-`idle`: no ring, 24px Inter regular, `var(--color-fg-muted)`. Off-centre neighbours: 24px Inter regular, `var(--color-fg-muted)`, declining opacity with distance from centre (1.0 at ±0, ~0.6 at ±1, ~0.3 at ±2, 0 beyond — same opacity ramp as Step 4's vertical wheel, just on the horizontal axis).
- [ ] AC3: The Step 4 state machine (`idle` → `set` → `error`) is preserved verbatim. All save semantics from Step 4 ACs 2–4, 8, 9 still hold (first deliberate interaction promotes idle→set + fires immediate PUT; subsequent settled changes debounce-save 500ms; no-op when target equals last-saved; coalesce rapid changes).
- [ ] AC4: Keyboard mapping is rotated to match the new axis: `ArrowLeft` decrements (toward 1), `ArrowRight` increments (toward 10). `Home` = 1, `End` = 10, `PageUp` = -3, `PageDown` = +3, number keys `1`–`9` jump to that value, `0` jumps to 10. `ArrowUp` / `ArrowDown` are *also* accepted and map to decrement / increment respectively, so users with muscle memory from Step 4 still work (and so a phone with a hardware-keyboard case picks up either axis).
- [ ] AC5: `<SaveStatus />` is removed from inside `<ScoreRow>`'s render tree. `<TodayShell>` renders a new header row: a flex container with the H1 date on the left and `<SaveStatus />` on the right. The wheel/row no longer has the indicator in its own column.
- [ ] AC6: `<SaveStatus />` visual is **unchanged for `saving` (`…`) and `saved` (`✓`)** — same glyphs, same `aria-label`s ("Opslaan" / "Opgeslagen"), same `body-small` (15px) `var(--color-fg-muted)` text. **New for `error`**: renders the `⚠` glyph (U+26A0) in `var(--color-fg-subtle)` (#9C8F82, tertiary text color) with `aria-label="Niet opgeslagen"`. The existing inline error banner (`role="alert"`, `copy.errors.notSaved`) is preserved and continues to render below the score row in error state — the header glyph is an at-a-glance ambient indicator, not a replacement for the actionable banner.
- [ ] AC7: Reduced motion: `prefers-reduced-motion: reduce` disables smooth horizontal scrolling — keyboard-driven `scrollBy` calls use `behavior: 'auto'` instead of `'smooth'`. CSS scroll-snap itself respects the OS preference natively.
- [ ] AC8: All Step 4 e2e specs continue to pass after the rewrite. Specifically `tests/e2e/daily-entry-score-wheel.spec.ts` (renamed to `daily-entry-score-row.spec.ts`) — `getByRole('listbox', { name: /score/i })`, the `data-score` and `data-centred` attributes, and the `ArrowDown`/`ArrowUp` selectors all still work.
- [ ] AC9: New e2e: a horizontal-drag gesture (touch or mouse) on the row scrolls it; the new centred value triggers a save per AC3. Tapping a visible non-centred number jumps + saves.
- [ ] AC10: `<SaveStatus />` in the header is keyboard- and screen-reader-accessible: wrapped in `<span role="status" aria-live="polite">` (already there for `saving`/`saved`; preserved + extended to `error`).

---

## Technical constraints

- **No new dependency.** The horizontal row is the vertical wheel with the axis rotated: `flex-col` → `flex-row`, `h-56` → `h-20`, `overflow-y-auto` → `overflow-x-auto`, scroll-snap from `y mandatory` to `x mandatory`, IntersectionObserver `rootMargin` rotated.
- **File rename**: `src/components/score-wheel.tsx` → `src/components/score-row.tsx`. Test file `src/components/__tests__/score-wheel.test.tsx` → `src/components/__tests__/score-row.test.tsx`. Export `ScoreWheel` → `ScoreRow`. E2E spec `tests/e2e/daily-entry-score-wheel.spec.ts` → `tests/e2e/daily-entry-score-row.spec.ts`. Each rename also updates imports (only `src/components/today-shell.tsx` currently imports the component).
- **`<TodayShell>` header restructure** is small: wrap the existing `<h1>` plus a new `<SaveStatus />` slot in a `flex flex-row items-baseline justify-between` container. The `<SaveStatus />` instance has to receive `status` and `error` from somewhere — see "Plan / 4b.4" for the wiring choice.
- **IntersectionObserver rootMargin**: rotate from `'-44% 0px'` to `'0px -44%'` (vertical → horizontal); the `isIntersecting` item is still the current value.
- **LOC budget**: ~150 across renamed `score-row.tsx` + renamed test + ~20 lines of `today-shell.tsx` edits + ~10 lines of `save-status.tsx` for the new error glyph.

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | No | UI-only refactor |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | No new data fields |
| New dependency | ADR or step rationale | No | No new deps |
| `dangerouslySetInnerHTML` usage | A03 | No | — |
| New env var with a secret | A02, A05 | No | — |
| New telemetry / observability dep | Cardinal "no telemetry" | No | — |

## Plan

### 4b.0 Rename files and update imports

Mechanical first pass before any logic changes:
- `git mv src/components/score-wheel.tsx src/components/score-row.tsx`
- `git mv src/components/__tests__/score-wheel.test.tsx src/components/__tests__/score-row.test.tsx`
- `git mv tests/e2e/daily-entry-score-wheel.spec.ts tests/e2e/daily-entry-score-row.spec.ts`
- Inside each: `s/ScoreWheel/ScoreRow/g`, `s/score-wheel/score-row/g`, `s/wheel/row/g` where it refers to the component (NOT where it refers to mouse-wheel events).
- Update the single import in `src/components/today-shell.tsx`: `import { ScoreWheel } from '@/components/score-wheel'` → `import { ScoreRow } from '@/components/score-row'`. Also `<ScoreWheel … />` → `<ScoreRow … />`.

Run `npm run verify` here as a checkpoint — should be green with no behavior change.

### 4b.1 Pivot the layout axis

In `score-row.tsx`:
- Container `className`: `flex h-56 flex-col items-center justify-center overflow-hidden rounded-lg border border-border` → `flex h-20 flex-row items-center overflow-x-auto rounded-lg border border-border scroll-snap-x mandatory` (Tailwind classes for scroll-snap may need an inline style or arbitrary value depending on Tailwind v4 support — check `globals.css` for the snap utility or use `style={{ scrollSnapType: 'x mandatory' }}`).
- Each button's className keeps `h-12 w-12` (48×48) but the row container is now horizontal; existing flex-row + `items-center` arranges them in a line.
- Add `scroll-snap-align: center` to each button (Tailwind `snap-center` or inline style).
- Remove `overflow-hidden` from the container — it must be `overflow-x-auto` to allow scrolling.

### 4b.2 IntersectionObserver rotation

In `score-row.tsx`, wherever the IntersectionObserver is created:
- `rootMargin: '-44% 0px'` → `rootMargin: '0px -44%'` (top/bottom → left/right margins).
- `root` is still the container ref.
- The "which item is centred" calculation is identical — `entries.find(e => e.isIntersecting)?.target.dataset.score`.

### 4b.3 Keyboard handlers

In the existing `onKeyDown` switch:
- Add `ArrowLeft` and `ArrowRight` cases that mirror the current `ArrowDown` and `ArrowUp` cases respectively (left = decrement, right = increment).
- **Keep** `ArrowUp` / `ArrowDown` as aliases for backward compatibility with the test suite and for users with a hardware keyboard who instinctively use vertical arrows on a "score selector."
- `Home` / `End` / `PageUp` / `PageDown` / number keys: unchanged.

### 4b.4 Move `<SaveStatus />` from row into header

This needs the row's state to surface up so the header can render `<SaveStatus />` with the right props.

**Option A** (recommended): Hoist `useDayEntryUpsert(date)` up to `<TodayShell>`. Pass `save`, `status`, `lastError` down to `<ScoreRow>` as props. `<TodayShell>` renders `<SaveStatus status={status} error={lastError} />` in the header. Single source of truth for the hook; clean prop drilling of one level.

**Option B**: Keep `useDayEntryUpsert` inside `<ScoreRow>` and use a callback (`onStatusChange?: (s: SaveStatus) => void`) to surface the status to `<TodayShell>`. More indirection, less clean.

Go with **Option A**. The single-hook-per-screen pattern is the right one — Step 5's `<NoteField>` and `<TagCategoryList>` will *also* call `useDayEntryUpsert(date)`, but they each own their own input timing (NoteField has 1.5s typing-settle; TagCategoryList saves on every toggle). The hook is hook-local; the *status* is shared. So actually each component instantiates its own hook for its own debounce, but the hook itself can be enhanced (or a small `useUpsertStatus` wrapper added) to broadcast its status to a shared context. **Settle this in implementation** — for now Step 4b can hoist the wheel-specific hook only and Step 5 can revisit when wiring the additional components.

In `<TodayShell>`:
```tsx
const { save, status, lastError } = useDayEntryUpsert(date);
return (
  <main className="mx-auto flex min-h-screen max-w-[480px] flex-col gap-6 p-6">
    <header className="flex flex-row items-baseline justify-between gap-3">
      <h1 className="text-2xl font-semibold capitalize">{heading}</h1>
      <SaveStatus status={status} error={lastError} />
    </header>
    <ScoreRow date={date} initialScore={entry?.score ?? null} save={save} status={status} />
    {/* note section + tags section unchanged for this step — Step 5 wires them */}
  </main>
);
```

In `<ScoreRow>`: remove the `useDayEntryUpsert` call and the inner `<SaveStatus />` render; accept `save`, `status` as props instead. The status is still needed inside `<ScoreRow>` for the existing error-revert effect.

### 4b.5 Add `error` glyph to `<SaveStatus />`

In `src/components/save-status.tsx`, currently the `error` branch renders a `<div role="alert">` banner. Replace it with **two outputs** controlled by a render variant prop — OR keep the current behavior and let `<TodayShell>` render only the glyph version while a separate `<ErrorBanner />` renders the actionable banner below the row. **Decide in implementation** based on whether ergonomics favor a single component-with-variants or two purpose-built components.

Simplest path: add a `variant?: 'glyph' | 'banner'` prop to `<SaveStatus />`. `'glyph'` (new default in the header) renders a single character: `…` (saving) / `✓` (saved) / `⚠` (error), all in `body-small` + `var(--color-fg-muted)` except `⚠` which is in `var(--color-fg-subtle)`. `'banner'` (existing behavior, used inline by Step 5 components that want the actionable message) renders the existing banner UI.

`<TodayShell>` uses `<SaveStatus status={status} error={lastError} variant="glyph" />`. Step 5's NoteField and TagCategoryList (when they ship) decide their own variant — likely `'glyph'` for status-only feedback inline, and a single shared `<ErrorBanner>` mounted once in `<TodayShell>` for the actionable retry message.

### 4b.6 Update tests

`score-row.test.tsx` (renamed):
- Existing cases 1–10 mostly keep working after the rename. Adjust:
  - Case 6 ("Tap on visible non-centred value") — works the same; the visible non-centred value is now to the left/right, not above/below.
  - Case 7 ("ArrowUp key → centred increments toward 10 + save") — add a parallel case for `ArrowRight` doing the same. Keep `ArrowUp` test as the backward-compat check.
  - The "wheel container is 5 × 44px tall" assertion (if present) becomes "row container is 5 × 48px wide" or equivalent.

`today-shell.test.tsx`:
- New case: "Renders H1 date on the left and `<SaveStatus />` on the right within a flex header" — assert the DOM order and the `role="status"` element's presence.
- Existing cases: most keep working. The "renders ScoreWheel" assertion becomes "renders ScoreRow".

`save-status.test.tsx`:
- New cases:
  - `variant="glyph"` + `status="error"` → renders the `⚠` glyph with `aria-label="Niet opgeslagen"` and the tertiary-text-color class.
  - `variant="banner"` + `status="error"` → renders the existing banner (regression check).
- Existing 4 cases: rename or duplicate to test `variant="glyph"` as well.

`tests/e2e/daily-entry-score-row.spec.ts` (renamed):
- Existing 3 specs work after axis adjustment (`ArrowDown` → either `ArrowRight` or keep `ArrowDown` since AC4 keeps it as an alias).
- New spec: horizontal drag gesture on the row scrolls, save fires. Use Playwright's `mouse.down → mouse.move → mouse.up` for the drag; for touch, Playwright's `touchscreen` API.

### 4b.7 Verify

`npm run verify` — full Vitest + lint + typecheck green. Then `npx playwright test --project=chromium` for e2e.

## Test plan

### `src/components/__tests__/score-row.test.tsx` (renamed from score-wheel, ~11 cases — +1 for ArrowRight)

| # | Case |
|---|---|
| 1 | Fresh day: renders centred at `5` in `idle` state (no ring) |
| 2 | Existing entry: renders centred at saved score in `set` state (ring visible) |
| 3 | First interaction on `idle` row → fires PUT with current centred value + state becomes `set` |
| 4 | Settled scroll change after `set` → fires PUT with new value |
| 5 | Scrolling past a value back to the saved one → no PUT (AC4 from Step 4) |
| 6 | Tap on visible non-centred value → smooth scroll + save |
| 7a | `ArrowUp` key → centred increments toward 10 + save (backward compat) |
| 7b | `ArrowRight` key → centred increments toward 10 + save (primary axis) |
| 8 | 500 response → state reverts, error banner visible (via parent's `<SaveStatus variant="banner">`) |
| 9 | Rapid interactions (3 changes in 200ms) → debounce coalesces to 1 PUT |
| 10 | AbortError on superseded request → no UI revert, no error |

### `src/components/__tests__/save-status.test.tsx` (extended, +2 cases)

Existing 4 cases (one per status) — re-parameterize to run for `variant="glyph"` and `variant="banner"` where the behavior differs.

| # | New case |
|---|---|
| New A | `variant="glyph"` + `status="error"` → `⚠` rendered, `aria-label="Niet opgeslagen"`, color class for tertiary text |
| New B | `variant="banner"` + `status="error"` → existing banner UI (regression) |

### `src/components/__tests__/today-shell.test.tsx` (+1 case)

| # | Case |
|---|---|
| New | Header renders H1 date and `<SaveStatus role="status">` in a single flex row, H1 on the left, status on the right |

### `tests/e2e/daily-entry-score-row.spec.ts` (renamed, +1 case)

| # | Case |
|---|---|
| 1 | Fresh day: load `/`, row at `5` in idle (no ring); ArrowRight (or ArrowDown alias) to `6` → PUT lands; ring + saved-`✓` indicator appear in **header**, not below the row |
| 2 | Existing entry: load `/`, row at saved score; click a visible non-centred number → PUT lands |
| 3 | Offline (`context.setOffline(true)`) + interaction → error glyph `⚠` in header + error banner below row; row reverts |
| New | Horizontal drag gesture (mouse-down → move 96px right → mouse-up) on the row scrolls by 2 positions and saves the new value |

## Done criteria

- [ ] File rename committed cleanly (`git mv`, no orphan): `score-wheel.tsx` → `score-row.tsx`, test file, e2e spec. Single import in `today-shell.tsx` updated.
- [ ] Axis pivot complete: container is `flex-row h-20 overflow-x-auto`, scroll-snap on x, IntersectionObserver rootMargin rotated.
- [ ] Keyboard: `ArrowLeft`/`ArrowRight` primary, `ArrowUp`/`ArrowDown` aliases preserved.
- [ ] `useDayEntryUpsert(date)` hoisted to `<TodayShell>`; `save`/`status`/`lastError` props passed to `<ScoreRow>`; `<SaveStatus variant="glyph">` rendered in header.
- [ ] `<SaveStatus />` extended with `variant` prop; `⚠` glyph in tertiary color for error variant.
- [ ] Vitest count delta: +2 (1 today-shell header test, 2 save-status variant tests, 1 ArrowRight test, -2 from variants combining — net +2-ish). Final number: ~456.
- [ ] Playwright +1 (horizontal-drag spec). Existing 3 specs adapted, all still pass.
- [ ] `npm run verify` clean.
- [ ] **Phone walkthrough** (mandatory — this is the cardinal screen post-ship redesign):
  - One-handed thumb scroll left/right on the row, score-button reachable across the whole row width
  - Tap-to-jump on a visible number works at the edge of thumb reach
  - SaveStatus glyph in the header is visible while the user's thumb is on the row (no occlusion)
  - Error banner readable when network is throttled to offline
- [ ] **Brainfog walkthrough**: from open-app to score-saved on a 4-out-of-6 day, ≤ 10s. Compare to the vertical wheel's time-on-task — should be equal or faster.
- [ ] **A11y walkthrough**: VoiceOver / TalkBack reads the row in keyboard tab order; ArrowRight announces the next value; save-status changes announce via `aria-live="polite"`.

## Open questions to settle during implementation

- **Scroll-snap class availability in Tailwind v4.** If Tailwind v4 doesn't expose `snap-x` / `snap-center` as utilities by default, fall back to inline `style={{ scrollSnapType: 'x mandatory' }}` on the container and `style={{ scrollSnapAlign: 'center' }}` on each item. Document the choice in the file's top comment.
- **Initial-render scroll position.** On mount, the row needs to pre-scroll so the `initialScore ?? 5` is centred — same as the vertical wheel's `scrollTop` pre-set, but using `scrollLeft`. Calculate as `(initialIndex * itemWidth) - (containerWidth / 2) + (itemWidth / 2)`.
- **Touch-flick overshoot on iOS.** A hard horizontal flick scrolls past several values before snapping — same UX as the vertical wheel's vertical flick. Debounce in the hook ensures one save. No special handling.
- **Whether the alternative-axis arrow keys (`ArrowUp` / `ArrowDown`) should be removed in a future step** once muscle memory adjusts. Probably not — keeping them is harmless and helps anyone using a hardware-keyboard case. Re-evaluate in the post-merge audit.
