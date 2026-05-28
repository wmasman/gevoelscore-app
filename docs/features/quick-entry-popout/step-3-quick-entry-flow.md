# Step 3: QuickEntryFlow composite

**Estimated time:** 3 hours
**Test layer:** Vitest component tests for step orchestration, back/forward, auto-advance timing, end-of-flow trigger. Playwright e2e for the full flow against a live local Directus.
**Risk:** Medium. This is the orchestrator — it composes ScoreCircle, NoteField, TagCategoryList inside BottomSheet, manages the step state, runs the morph, threads `useDayEntryUpsert` saves through each child, and triggers the end-of-flow tint-pulse on the target card.
**Prerequisite:** [Step 0](step-0-shared-primitives.md), [Step 1](step-1-bottom-sheet.md), [Step 2](step-2-score-circle.md) shipped.

**Hard external prerequisite: `daily-entry/` Step 5 must be shipped before this step can start.** Step 3 imports `<NoteField>` and `<TagCategoryList>` from that step. Steps 0–2 of this feature can run in parallel with the other programmer's Step 5 work; Step 3 cannot start until Step 5 lands. If Step 5's component APIs differ from what this plan assumes (e.g. different prop names, slightly different state-management shape), expect a small adapter layer or a focused refactor at the start of this step.

> **Status: outline.** Full step detail will be filled in as we approach `/build-step`.

---

## Scope summary

The composite component that everything else hangs off. Lives at `src/components/lab/quick-entry-flow.tsx`.

```tsx
type Props = {
  date: string;                          // YYYY-MM-DD
  initialEntry: DayEntry | null;
  open: boolean;
  startStep?: 'score' | 'note' | 'tags'; // default: 'score'
  isPastDay?: boolean;                   // affects tint
  onClose: () => void;
  onComplete: () => void;                // fires when the user taps "Klaar"
};
```

The component:
1. Renders `<BottomSheet>` with the right tint
2. Uses `useStepMorph` to crossfade between score → note → tags
3. Mounts `<ScoreCircle>`, `<NoteField>`, `<TagCategoryList>` inside the morphing middle region
4. Renders the fixed footer with back + forward buttons (in the thumb zone)
5. Calls `useDayEntryUpsert(date)` once at this level; child components emit save patches up via callbacks
6. After tags step, "Klaar" tap → `onComplete()` (parent triggers the today-card pulse)
7. Auto-advances score → note after the score commits, with a ~500ms pause

---

## Acceptance criteria

Inherited from feature README AC17–AC25 and AC29–AC30. Replicated:

- [ ] AC1 (== README AC17): Steps morph via crossfade in place — 150ms out, 150ms in, 50ms overlap, fixed panel height
- [ ] AC2 (== README AC18): Only middle region morphs; header (date, X) and footer (back / forward) stay put
- [ ] AC3 (== README AC19): `prefers-reduced-motion: reduce` flattens to 0.01ms
- [ ] AC4 (== README AC20): Note step renders `<NoteField>` with surface-muted background, soft border, brainfog-floor sizing
- [ ] AC5 (== README AC21): Forward text: `Volgende: tags` (note step) / `Klaar ✓` (tags step). Back text: `← Score` (note) / `← Notitie` (tags). Both in thumb zone.
- [ ] AC6 (== README AC22): Forward button works on empty note (skips). Back returns with the saved value.
- [ ] AC7 (== README AC23): Tags step renders `<TagCategoryList>` with 4 primary + `Extra opties` toggle
- [ ] AC8 (== README AC24): Categories expand inline; multiple at once allowed; selection counts on headers
- [ ] AC9 (== README AC25): Forward on tags step = `Klaar ✓`; triggers `onComplete()`
- [ ] AC10 (== README AC29): Auto-save via `useDayEntryUpsert` — score on commit, note on 1.5s debounce, tags on every toggle
- [ ] AC11 (== README AC30): Mid-flow dismiss (drag-down, backdrop click, Escape) does not lose data; reopening returns saved state

Additional:

- [ ] AC12: Auto-advance from score to note step after `onCommit` fires. Delay defined as a named constant `AUTO_ADVANCE_SCORE_TO_NOTE_MS = 500` at the top of `quick-entry-flow.tsx` (tuneable based on real-device feedback; the constant pattern makes it cheap to revise without hunting through the file). If the user opens the sheet at the score step but the day already has a saved score, **no auto-advance** — they came to review, not to commit again.
- [ ] AC13: If `startStep === 'note'` or `startStep === 'tags'` (i.e. the user tapped the matching region of the today-card), the sheet opens directly at that step. Score step is not auto-shown.
- [ ] AC14: Back button is hidden on the score step, visible from note onwards.

---

## Component composition reference

```
<BottomSheet open={open} onClose={onClose} tint={isPastDay ? 'past' : 'today'}>
  <Header>
    <Date>{formatDateDutch(date)}</Date>
    <CloseButton onClick={onClose} />
  </Header>
  <MiddleRegion>
    {/* useStepMorph manages which step is rendered */}
    {renderedStep === 'score' && <ScoreStep ... />}
    {renderedStep === 'note' && <NoteStep ... />}
    {renderedStep === 'tags' && <TagsStep ... />}
  </MiddleRegion>
  <Footer>
    {currentStep !== 'score' && <BackButton ... />}
    {currentStep !== 'score' && <ForwardButton ... />}
  </Footer>
</BottomSheet>
```

The middle region has fixed height (~380px) so morphs don't reflow. Each step is absolute-positioned inside it.

---

## Test plan (stub)

### `src/components/lab/__tests__/quick-entry-flow.test.tsx` (~8 cases)

1. Initial render at `startStep='score'`: ScoreCircle visible, NoteField absent (or display:none), tags absent. Back button hidden.
2. `<ScoreCircle>` `onCommit` fires: parent calls `save({ score })`, after 500ms morph to note step. Back button appears.
3. `startStep='note'` for an existing entry: opens directly at note step, no auto-advance
4. Note step + forward button: morph to tags step
5. Tags step + Klaar: fires `onComplete()`; sheet stays open (parent decides to close + pulse)
6. Back button on tags: morph to note step. Selection state preserved.
7. Drag-down dismiss mid-flow: `onClose` fires; saved state preserved (mock useDayEntryUpsert)
8. `isPastDay=true`: BottomSheet receives `tint='past'`

### `tests/e2e/quick-entry-popout-flow.spec.ts` (~3 cases)

1. Full flow on empty day: open → score drag → note type → tags select → Klaar → sheet closes
2. Re-open at note: tap note region → opens at note step with saved note visible
3. axe-core scan at each step

---

## Done criteria

- [ ] `QuickEntryFlow` shipped, 8 unit tests green, 3 e2e tests green
- [ ] Vitest count delta: +8
- [ ] Playwright count delta: +3
- [ ] `npm run verify` clean

---

## Open questions to settle during implementation

- **Auto-advance vs review distinction:** the rule is "auto-advance only when the user actively committed a NEW value, not when they're just looking". Implementation: track whether the score change came from a user gesture vs prop-driven initial state. Probably a `userInitiatedRef.current` boolean.
- **NoteField focus on step entry:** when morphing into the note step, should the textarea auto-focus (triggering the iOS keyboard immediately)? Spec says yes — the user is on this step because they want to type. Add a short delay (~200ms) so the morph completes before the keyboard rises.
- **Tag selection that auto-completes the entry:** does selecting all desired tags + closing the sheet without tapping "Klaar" count as completion? It already saves (per AC10), but the end-of-flow card pulse only fires on `onComplete()`. Decision: drag-down dismiss does NOT pulse; only "Klaar" does. The pulse is the explicit ritual of "I am done with this day".
- **Composite reuse for timeline-bottom-sheet (daily-entry Step 6):** the existing `daily-entry/` Step 5 plans a `<DayEntryEditor>` composite that Step 6's timeline view reuses. Once this Step 3 lands, the QuickEntryFlow composite could play the same role — the timeline taps a past day → `<QuickEntryFlow>` opens with `isPastDay=true`. Defer this decision to Step 5 of this feature.
