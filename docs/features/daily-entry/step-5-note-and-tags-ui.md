# Step 5: Note + tag chips UI

**Estimated time:** 2 hours
**Test layer:** Vitest component tests (jsdom) for the note debounce + tag toggle + Playwright e2e against the dev server.
**Risk:** Medium. The note field's "save on pause" debounce is easy to get subtly wrong (saves too often or skips the final keystroke). Tag picker UX has 83 chips to lay out without overwhelming the brainfog user.
**Prerequisite:** Steps 1–4 done. **Also assumes [Step 4b](step-4b-score-row-and-save-relocation.md) has landed** — Step 4b hoists `useDayEntryUpsert(date)` to `<TodayShell>` and introduces `<SaveStatus variant="glyph" | "banner">`. This step's components reuse both.

> Adds the optional context fields to the daily tap flow. Note saves on blur or after 1.5s of typing-pause. Tag chips are grouped by category, tap toggles inclusion, each toggle is an immediate PUT. AC5–AC7 from the feature README.

---

## Acceptance criteria

- [ ] AC1: Note `<textarea>` appears below the score row. Placeholder: "Schrijf hier je notitie…" (matches the locked design at [docs/design/brief.md](../../design/brief.md); copy lives in `src/copy.ts` as `copy.daily.note.placeholder`). Disabled when no score is set yet (per feature AC7).
- [ ] AC2: Typing in the note debounces saves at 1.5s. The save fires PUT `/api/day-entries/[date]` with `{ note: <value> }`. Other fields are preserved server-side via Step 3's upsert.
- [ ] AC3: Blur-on-note (Tab away, click outside) flushes the debounce — saves immediately if there's a pending change. Avoids the "I closed the tab and lost the note" trap.
- [ ] AC4: Empty/whitespace note → saved as `null` (matches domain `normalizeNote`). Reflects in the UI as the placeholder reappearing.
- [ ] AC5: Below the note, **4 primary category headers** are visible in a vertical stack: `mentaal`, `fysiek`, `overall`, `activiteit`. Below them, a single text-button **"Extra opties (Interventie, Project, etc) ⌄"** in `var(--color-fg-muted)` text. Tapping it reveals the remaining 4 categories inline (`gebeurtenis`, `interventie`, `project`, `custom`). Tap again → collapses back to the 4-primary view. This split respects the brainfog rule (≤5 primary actions visible at once) while keeping all 8 categories reachable. The locked enum is at [`src/lib/domain/tag-category.ts`](../../../src/lib/domain/tag-category.ts); the split is purely a presentation grouping (the 4 primary are the highest-frequency in the author's historical data).
- [ ] AC6: Each category header is a button. Tap → the category expands inline below the header, showing all chips in that category. Tap again → collapses. **Multiple categories can be expanded simultaneously** — exploration is not punished. This rule applies to both the 4-primary categories and to the 4-extra categories once revealed.
- [ ] AC7: A category header shows a small count badge if any chips in that category are currently selected (e.g. "fysiek · 2"). Lets the user see selection state without expanding every category. The "Extra opties" button also shows a count of selected chips in the hidden categories (e.g. "Extra opties (3) ⌄") so a user with a chip selected in `interventie` knows it's there even before expanding.
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
- `src/components/tag-category-list.tsx` — 4 primary category-header buttons + 1 "Extra opties" expand-button that reveals the 4 remaining categories inline. Each individual category header has its own expanded/collapsed chip-display state (independent of the primary/extra split). Tapping a chip calls `useDayEntryUpsert(date).save({ tag_ids: newArray })`. The component owns three pieces of UI state: the primary/extra split toggle, the per-category chip-display expansion (Map), and the optimistic selection state; the hook owns the save. (Renamed from the originally planned `tag-picker.tsx` — "category list" describes the shape more accurately than "picker" once the 4+4 grouping is the dominant structure.)

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
      <TagCategoryList
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

### `src/components/__tests__/tag-category-list.test.tsx` (new, ~9 cases — +2 over the original tag-picker plan to cover the 4+4 split)

| # | Case |
|---|---|
| 1 | Renders 4 primary category headers (mentaal, fysiek, overall, activiteit) + an "Extra opties" toggle. The 4 extra categories (gebeurtenis, interventie, project, custom) are NOT in the DOM by default. |
| 2 | Tapping "Extra opties" reveals the 4 extra categories inline; tapping again collapses them back to invisible. ARIA `aria-expanded` flips on the toggle. |
| 3 | Tapping a (primary or revealed-extra) category header expands its chips inline; ARIA `aria-expanded` flips on the header. |
| 4 | Multiple category headers can be expanded simultaneously (test sequential taps; works across the primary/extra boundary). |
| 5 | Tapping an unselected chip in an expanded category calls save with the new `tag_ids` array. |
| 6 | Tapping a selected chip toggles it off (save called with reduced array). |
| 7 | Selection count badge appears on a category header when ≥1 chip in that category is selected. |
| 8 | The "Extra opties" toggle shows a count of selected chips in the hidden categories (e.g. selecting a chip in `interventie`, then collapsing extras → the toggle reads "Extra opties (1) ⌄"). |
| 9 | Server error reverts the toggle + `<SaveStatus>` shows error. |

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

- [ ] `NoteField` + `TagCategoryList` shipped, 14 unit tests green (5 NoteField + 9 TagCategoryList)
- [ ] `DayEntryEditor` composite shipped, 3 unit tests green
- [ ] `readAllTags` SDK wrapper shipped (+ ~2 wrapper tests)
- [ ] Server component fetches + passes tags down through `DayEntryEditor`
- [ ] `copy.daily.note.placeholder` updated to "Schrijf hier je notitie…"
- [ ] Playwright e2e +4 green (including the axe-core scan)
- [ ] Vitest count delta: +19 (5 NoteField + 9 TagCategoryList + 3 Editor + 2 SDK wrapper)
- [ ] `npm run verify` clean
- [ ] **A11y walkthrough**: keyboard-only — tab through row → note → category headers → "Extra opties" toggle → revealed extra categories → expanded chips; VoiceOver announces collapsed-state, the "Extra opties (n)" count, count badges per category, and chip toggles correctly
- [ ] **Brainfog walkthrough**: page stays scannable with extras collapsed; tag picker stays usable when 3 categories are expanded at once across the primary/extra boundary; no visual overload
- [ ] Phone walkthrough: 3-tag good-day entry in ≤ 30s including pause-to-think time
