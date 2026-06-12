# Step 4: `<ExertionSection>` UI + copy + e2e

**Estimated time:** 2.5–3.5 hours
**Test layer:** Component + e2e + manual walkthrough
**Risk:** High (UX) — this is the only step that touches the daily surface. The one-tap path and the ≤10s budget are the things most at risk; the visual-language rules (no colour scale) are a hard line.
**Prerequisite:** Step 3 (exertion persists end-to-end).

---

## Acceptance criteria (this step)

- [ ] AC11: A collapsed **"Inspanning"** row renders below the tag section in the daily popout, on **today and on a past-day edit** (both use `QuickEntryFlow`). Collapsed by default. The score path above it is unaffected.
- [ ] AC12: Expanding reveals three axes — **cognitief, fysiek, emotioneel** — each a row of four options labelled **geen / een beetje / behoorlijk / veel**. Rendered as word + position only; **no traffic-light / red-green colour**. Only the selected option carries the accent (matching the score-row rule).
- [ ] AC13: Tapping an option saves immediately through `useDayEntryUpsert(date)` (optimistic; revert on error via the existing error state). Re-tapping the selected value is a no-op (no wasted PUT). Axes are independent; an untouched axis persists as `null`.
- [ ] AC14: Score-only entry still completes in one tap and never requires touching exertion. A timed good-day flow that **skips** exertion stays **≤ 10s** (stopwatch).
- [ ] AC15: Touch targets ≥ 48×48; option + axis labels ≥ 17px; every option keyboard-operable with a visible `:focus-visible` ring; the expand control announces expanded/collapsed state (`aria-expanded`); `prefers-reduced-motion` flattens the expand animation; axe scan clean.

## Technical constraints

- **Mount point**: add `<ExertionSection date={date} initialExertion={entry?.exertion ?? null} />` into [`src/components/lab/quick-entry-flow.tsx`](../../../src/components/lab/quick-entry-flow.tsx), below the tag step. Follow how `NoteField` / `TagCategoryList` are composed and how they call `useDayEntryUpsert` — do not invent a new save mechanism.
- **Visual language** ([design/brief.md](../../design/brief.md)): neutral options, single accent on selection, soft pill/row shapes, no colour ramp, no emoji, ≤200ms motion. The collapsed row is one element (stays within the max-5-primary-actions density rule).
- **Thumb-first**: the section lives in the bottom input zone of the popout, like note + tags.
- **Copy** lives in `src/copy.ts` (no inline JSX literals): a section label, three axis labels, four anchor labels. Reflective Dutch, no em-dash, no exclamation, no second-person question. Suggested:
  - `copy.exertion.label` = `Inspanning`
  - axes: `Cognitief`, `Fysiek`, `Emotioneel`
  - anchors (1–4): `Geen`, `Een beetje`, `Behoorlijk`, `Veel`
- **No carry-forward / provenance** — out of scope by design.

### Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01,A03,A08 | No | client component; saves via existing route (Step 3) |
| New collection storing user data | GDPR Art 9 | No | — |
| New dependency | ADR/rationale | No | Tailwind + existing hook |
| `dangerouslySetInnerHTML` | A03 | No | worded labels are static copy, not user input |
| New env var with secret | A02,A05 | No | — |
| New telemetry dep | Cardinal no-telemetry | No | — |

## Test plan

| File | Cases (one per `it`) |
|------|----------------------|
| `src/components/__tests__/exertion-section.test.tsx` | collapsed by default (axes not in DOM / hidden); activating the row expands it (`aria-expanded` flips); renders 3 axes × 4 worded options; selected option has the accent class, others neutral; tapping an option calls `save` with `{ exertion: { cognitive: 3, physical: null, emotional: null } }`; re-tapping the selected value does not call `save`; initialExertion pre-selects the right options; keyboard activation works |
| `tests/e2e/exertion.spec.ts` | open popout → set score only → close, stopwatch ≤10s with exertion never touched; expand → set fysiek=veel → reload → still veel; axe scan on the expanded popout clean |

> Component test mocks `useDayEntryUpsert` and asserts the patch shape — mirror the existing `note-field` / `tag-category-list` component tests.

## Done criteria

- [ ] All ACs GREEN; RED then GREEN captured.
- [ ] Full suite + typecheck + lint clean.
- [ ] **Walkthrough done** (daily screen touched): one-handed, low light, arm's length; skip-exertion flow ≤10s; expand + three taps feels effortless; offline → optimistic value reverts with the existing error state.
- [ ] axe e2e clean; VoiceOver announces the expand control + option selection.
- [ ] `npm run predeploy` green before any deploy.
- [ ] No HIGH gate findings.

---

## Execution order

### 4.1 Baseline
Screenshot the current popout (today + past-day) for visual-regression comparison. Stopwatch the current score-only flow to record the pre-change ≤10s baseline.

### 4.2 Tests (RED)
Write `exertion-section.test.tsx` + the e2e spec. Run:
```
npm test -- exertion-section
```
Must FAIL (component does not exist).

### 4.3 Implement (GREEN)
- Add copy keys to `src/copy.ts`.
- Create `src/components/exertion-section.tsx`: a `'use client'` component owning only the expand/collapse state; renders the collapsed "Inspanning" row and, when open, three `AxisPicker` rows (four worded options each). On option tap, call `save({ exertion: { ...current, [axis]: value } })` via `useDayEntryUpsert(date)`; guard the re-tap no-op.
- Mount it in `quick-entry-flow.tsx` below tags, passing `date` + `initialExertion`, for both today and `isPastDay` paths.
Run again — PASS.

### 4.4 Regression
```
npm test
```
All green; existing popout (note/tags/score) behaviour unchanged.

### 4.5 Refactor
Keep `AxisPicker` private to the file unless a second surface needs it. No premature primitive.

### 4.6 Walkthrough
Per Done criteria: ≤10s skip path, offline revert, keyboard + VoiceOver, reduced-motion. Compare against the 4.1 baseline screenshots — the collapsed surface should look essentially unchanged.

### 4.7 Checkpoint
Commit: `feat(exertion/step-4): collapsed Inspanning section with three worded axis pickers`.

---

## What this step does NOT do
No analysis / correlation view (deferred delayed-cost feature). No 4th `social` axis. No carry-forward. Does not alter the score row, note field, or tag stack. Does not add a Settings toggle (availability is "always present, collapsed" by decision).
