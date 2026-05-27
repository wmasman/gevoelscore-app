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
- [ ] AC5: Tag chips appear below the note, grouped by category (mentaal, fysiek, overall, activiteit, gebeurtenis, interventie, project, custom). Section headers in Dutch. The category list is read from the locked enum in [`src/lib/domain/tag-category.ts`](../../../src/lib/domain/tag-category.ts).
- [ ] AC6: Tap a chip → it toggles its inclusion in `tag_ids` and immediately PUTs the full new array. Optimistic update + revert-on-error like the score row (AC2–AC4 of Step 4).
- [ ] AC7: Tag chips are reachable on mobile without horizontal scroll — flex-wrap. Touch target ≥ 36px (chips are smaller than score buttons; tradeoff: 83 chips need to fit).
- [ ] AC8: An empty tag list shows a single grey "Geen tags" line; toggling any chip removes that placeholder.
- [ ] AC9: Tags list is sourced from a new `GET /api/tags` endpoint (server-side cached, since the tag set rarely changes). Or: passed from the server component at page-load. **Choose during the step**: server-component prop is simpler if the page is dynamic; an endpoint is needed if tags are lazy-loaded. Default to server-component prop.

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

### 5.1 New components

- `src/components/note-field.tsx` — textarea + debounce + blur-flush. Same optimistic-update + revert pattern as `ScoreRow`.
- `src/components/tag-picker.tsx` — chips grouped by category. Same PUT pattern. Takes `allTags: Tag[]` + `selectedTagIds: string[]` as props.

### 5.2 Wire from server component

`src/app/page.tsx` server component additionally fetches `allTags` (via new SDK wrapper or existing). Passes to `TodayShell` which threads to `TagPicker`. Cache via `unstable_cache` with a 1-hour TTL — tag list changes rarely.

### 5.3 New SDK wrapper

`src/lib/api/tags.ts` — `readAllTags(accessToken): Result<Tag[]>`. Mirrors `day-entries.ts` shape.

### 5.4 Decision pending: endpoint vs. prop for tags

Default plan: pass `allTags` from server component to client. If the timeline view in Step 6 wants the tag list too, we promote to a `/api/tags` endpoint (still cached). Documented as a decision point per AC9.

## Test plan

### `src/components/__tests__/note-field.test.tsx` (new, ~5 cases)

| # | Case |
|---|---|
| 1 | Typing fires a save after 1.5s of pause |
| 2 | Continued typing within 1.5s does not fire |
| 3 | Blur flushes the pending debounce |
| 4 | Empty/whitespace value is saved as null |
| 5 | Disabled when `entry === null` (no score yet) |

### `src/components/__tests__/tag-picker.test.tsx` (new, ~5 cases)

| # | Case |
|---|---|
| 1 | Renders all 8 category headers and the chips under each |
| 2 | Tapping an unselected chip toggles it to selected + fires PUT with updated `tag_ids` |
| 3 | Tapping a selected chip toggles it off |
| 4 | Empty `selectedTagIds` shows "Geen tags" placeholder |
| 5 | Server error reverts the toggle + shows the error banner |

### `tests/e2e/daily-entry-note-and-tags.spec.ts` (new, ~3 cases)

| # | Case |
|---|---|
| 1 | Type a note + tab away → request lands |
| 2 | Toggle a chip → request lands; toggle again → second request lands |
| 3 | Race: tap score, immediately type note, immediately tap chip → all three land within 2s; final state is consistent |

## Done criteria

- [ ] `NoteField` + `TagPicker` shipped, 10 unit tests green
- [ ] `readAllTags` SDK wrapper shipped (+ wrapper tests if it warrants them)
- [ ] Server component fetches + passes tags
- [ ] Playwright e2e +3 green
- [ ] Vitest count delta: +12 (5 NoteField + 5 TagPicker + 2 SDK wrapper)
- [ ] `npm run verify` clean
- [ ] Manual: walkthrough on phone — note + tags entry flow ≤ 30s for a "good day" 3-tag entry (still well under the brainfog tolerance ceiling)
