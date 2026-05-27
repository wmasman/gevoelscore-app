# Step 5: Note + tag chips UI

**Estimated time:** 2 hours
**Test layer:** Vitest component tests (jsdom) for the note debounce + tag toggle + Playwright e2e against the dev server.
**Risk:** Medium. The note field's "save on pause" debounce is easy to get subtly wrong (saves too often or skips the final keystroke). Tag picker UX has 83 chips to lay out without overwhelming the brainfog user.
**Prerequisite:** Steps 1–4 done.

> Adds the optional context fields to the daily tap flow. Note saves on blur or after 1.5s of typing-pause. Tag chips are grouped by category, tap toggles inclusion, each toggle is an immediate PUT. AC5–AC7 from the feature README.

---

## Acceptance criteria

- [ ] AC1: Note `<textarea>` appears below the score row. Placeholder: "Notitie (optioneel)". Disabled when no score is set yet (per feature AC7).
- [ ] AC2: Typing in the note debounces saves at 1.5s. The save fires PUT `/api/day-entries/[date]` with `{ note: <value> }`. Other fields are preserved server-side via Step 3's upsert.
- [ ] AC3: Blur-on-note (Tab away, click outside) flushes the debounce — saves immediately if there's a pending change. Avoids the "I closed the tab and lost the note" trap.
- [ ] AC4: Empty/whitespace note → saved as `null` (matches domain `normalizeNote`). Reflects in the UI as the placeholder reappearing.
- [ ] AC5: Below the note, 8 collapsible category headers in a vertical stack: mentaal, fysiek, overall, activiteit, gebeurtenis, interventie, project, custom. Headers are in Dutch. The category list is the locked enum from [`src/lib/domain/tag-category.ts`](../../../src/lib/domain/tag-category.ts).
- [ ] AC6: Each header is a button. Tap → the category expands inline below the header, showing all chips in that category. Tap again → collapses. **Multiple categories can be expanded simultaneously** — exploration is not punished.
- [ ] AC7: A category header shows a small count badge if any chips in that category are currently selected (e.g. "fysiek · 2"). Lets the user see selection state without expanding every category.
- [ ] AC8: Tap a chip → toggles its inclusion in `tag_ids` and immediately PUTs the full new array. Optimistic update + revert-on-error matching the wheel's pattern from Step 4.
- [ ] AC9: Chips within an expanded category wrap horizontally; touch target ≥ 36px. A short empty-state "(geen tags in deze categorie)" appears if the category is empty (shouldn't happen with the 83 seeded but defensive against future archived states).
- [ ] AC10: Tags list is sourced from the server component at page-load (passed as a prop) — same approach as `entry` in Step 2. No new `/api/tags` endpoint in this step; if the timeline view (Step 6) needs the list too, the server component just passes it down the tree.

## Technical constraints

- Note debounce uses a plain `useEffect` + `setTimeout` + cleanup. No new dep (no `lodash.debounce`, no `use-debounce`).
- Tag chip toggle pipes through the same `/api/day-entries/[date]` PUT endpoint as Step 4 — the route already handles `tag_ids` upsert (Step 3 AC4 + AC7).
- Race condition: a score tap during a pending note save must not lose the note. Per Step 3's upsert, partial body is OK (omitted fields preserved). Test: tap score, immediately type a note, blur within 100ms — both must land.
- Layout: chips wrap; category sections collapse on phone if all 83 fit awkwardly. **Trade-off to settle in the step**: do we ship the full 83 visible by default, or hidden-by-default per category with expand-on-tap? Brainfog principle says "fewer things visible" but the daily-entry flow says "tap = done, no extra navigation". **Default plan**: all 83 visible, category headers, no expand/collapse. Revisit if usability testing shows it's too noisy.

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | Maybe | Only if AC9 chooses the endpoint route over the server-component prop |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | Notes are PII — log discipline already covered by Step 3 |
| New dependency | ADR or step rationale | No | No new deps |
| `dangerouslySetInnerHTML` usage | A03 | No | — |
| New env var with a secret | A02, A05 | No | — |
| New telemetry / observability dep | Cardinal "no telemetry" | No | — |

## Plan

> **Reuse strategy.** Both new components call the `useDayEntryUpsert(date)` hook + render `<SaveStatus />`, both introduced in Step 4. This step also lands the **`<DayEntryEditor />` composite** — wheel + note + tag picker as a single vertical unit — which Step 6's timeline bottom sheet will reuse.

### 5.1 New components

- `src/components/note-field.tsx` — textarea. Calls `useDayEntryUpsert(date).save({ note })` on debounced typing + on blur. Uses `<SaveStatus />` for its indicator. Pure UI; no transport logic — all that lives in the hook.
- `src/components/tag-picker.tsx` — 8 category-header buttons in a vertical stack; each header has expanded/collapsed state. Tapping a chip calls `useDayEntryUpsert(date).save({ tag_ids: newArray })`. The component owns the expand/collapse UI state (per-category boolean Map) and the optimistic selection state; the hook owns the save.

### 5.2 New composite: `src/components/day-entry-editor.tsx`

```tsx
type Props = {
  date: string;
  initialEntry: DayEntry | null;
  allTags: Tag[];
};

export function DayEntryEditor({ date, initialEntry, allTags }: Props) {
  return (
    <div>
      <ScoreWheel date={date} initialScore={initialEntry?.score ?? null} />
      <NoteField date={date} initialNote={initialEntry?.note ?? null} disabled={!initialEntry} />
      <TagPicker
        date={date}
        allTags={allTags}
        initialTagIds={initialEntry?.tag_ids ?? []}
        disabled={!initialEntry}
      />
    </div>
  );
}
```

Today screen uses it via `<DayEntryEditor date={today} initialEntry={entry} allTags={allTags} />`. Timeline's bottom sheet (Step 6) uses the same component with a different date.

`disabled={!initialEntry}` propagates the "no score set yet → note/tags inactive" rule. Once the wheel saves (promotes the day from no-entry to has-entry), the parent server component re-fetches and `initialEntry` becomes non-null on next render — **but** that requires a server-component re-fetch. To avoid a full page round-trip, the wheel's first save also bubbles an `onFirstSave?: (entry: DayEntry) => void` event up; the editor catches it and updates its internal mirror of `initialEntry` so the note + tags can be edited immediately.

### 5.3 Wire from server component

`src/app/page.tsx` server component additionally fetches `allTags` (via new SDK wrapper). Passes to `<DayEntryEditor />` which threads to its children.

### 5.4 New SDK wrapper

`src/lib/api/tags.ts` — `readAllTags(accessToken): Result<Tag[]>`. Mirrors `day-entries.ts` shape. Cache via `unstable_cache` with a 1-hour TTL — tag list changes rarely.

### 5.5 What the hook handles vs what each child handles

| Concern | Owner |
|---|---|
| HTTP transport, abort, status, error | `useDayEntryUpsert` |
| Debounce (500ms generic + 1.5s note-typing) | The component owning the input — calls `save()` when it's time. The hook's own settle-debounce coalesces if the component calls in bursts. |
| Optimistic local state | The component (wheel's `centred`, note's `value`, tag picker's `selectedTagIds`) |
| Revert on error | The component reads `status === 'error'` and restores from its last-saved snapshot |
| Save-indicator visual | `<SaveStatus />` (children embed it; one source of truth) |

## Test plan

### `src/components/__tests__/note-field.test.tsx` (new, ~5 cases)

| # | Case |
|---|---|
| 1 | Typing calls `hook.save({note})` after 1.5s of pause |
| 2 | Continued typing within 1.5s does not call save |
| 3 | Blur flushes the pending debounce |
| 4 | Empty/whitespace value calls save with `{note: null}` |
| 5 | Disabled when `disabled` prop is true |

### `src/components/__tests__/tag-picker.test.tsx` (new, ~7 cases)

| # | Case |
|---|---|
| 1 | Renders 8 category headers, all collapsed by default |
| 2 | Tapping a header expands its chips inline; ARIA `aria-expanded` flips |
| 3 | Multiple headers can be expanded simultaneously (test sequential taps) |
| 4 | Tapping an unselected chip in an expanded category calls save with the new `tag_ids` array |
| 5 | Tapping a selected chip toggles it off (save called with reduced array) |
| 6 | Selection count badge appears on header when ≥1 chip in that category is selected |
| 7 | Server error reverts the toggle + `<SaveStatus>` shows error |

### `src/components/__tests__/day-entry-editor.test.tsx` (new, ~3 cases)

| # | Case |
|---|---|
| 1 | Renders wheel + note + tag picker in order |
| 2 | When `initialEntry === null`, note + tags are disabled |
| 3 | Wheel's first-save callback flips internal `disabled` state so note + tags become editable without server re-fetch |

### `tests/e2e/daily-entry-note-and-tags.spec.ts` (new, ~4 cases)

| # | Case |
|---|---|
| 1 | Type a note + tab away → request lands |
| 2 | Expand a category, tap a chip → request lands; tap another category header → first stays open, second expands |
| 3 | Race: scroll wheel, immediately type note, immediately tap chip → all three land within 2s; final state is consistent |
| 4 | axe-core scan on the today screen post-render: no WCAG 2.2 AA violations |

## Done criteria

- [ ] `NoteField` + `TagPicker` shipped, 12 unit tests green
- [ ] `DayEntryEditor` composite shipped, 3 unit tests green
- [ ] `readAllTags` SDK wrapper shipped (+ ~2 wrapper tests)
- [ ] Server component fetches + passes tags down through `DayEntryEditor`
- [ ] Playwright e2e +4 green (including the axe-core scan)
- [ ] Vitest count delta: +17 (5 NoteField + 7 TagPicker + 3 Editor + 2 SDK wrapper)
- [ ] `npm run verify` clean
- [ ] **A11y walkthrough**: keyboard-only — tab through wheel → note → category headers → expanded chips → arrows expand/collapse; VoiceOver announces collapsed-state, count badges, and chip toggles correctly
- [ ] **Brainfog walkthrough**: tag picker stays usable when 3 categories are expanded at once; no visual overload
- [ ] Phone walkthrough: 3-tag good-day entry in ≤ 30s including pause-to-think time
