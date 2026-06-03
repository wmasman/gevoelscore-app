# Step 1: Tag merge (single step)

**Estimated time:** ~5 hours. Smaller surface than v1.5b: one new API library function, one new route, one new picker component, one new button + handler on the existing `TagFormSheet`. No schema change, no new external dependencies.
**Test layers:** Vitest unit tests for the new `mergeTag` SDK function (junction-rewrite logic, dedup, error variants). Vitest route tests for `POST /api/tags/[id]/merge` (standard auth stack + per-error mapping + 200 with affected_days). Vitest component tests for the new `TagMergeTargetPickerSheet` and the `TagFormSheet` integration (button visibility + tap-to-merge flow). Smoke script for the end-to-end production round-trip with a seeded duplicate.
**Risk:** Medium. The junction-rewrite operation is the only genuinely-new destructive cross-collection operation in the app to date (DELETE was atomic, this is read-then-rewrite-then-delete). Failure modes are recoverable per the README's transaction-safety table but each step needs explicit test coverage.
**Prerequisite:** (1) Tag-management-settings shipped (commit `b58433f` + hotfixes `070b64c` / `b233c2d`); `TagFormSheet` exists and is extensible. (2) **[Step 0 — Junction + label integrity hardening](./step-0-junction-integrity.md) applied to production**: `UNIQUE(day_entries_id, tags_id)` on `day_entries_tags` + the 3 sibling constraints are live, and `verify-schema.mjs` passes. AC5's bulk-delete-then-bulk-patch ordering relies on the junction UNIQUE being DB-enforced; running step 1 without step 0 means a refactor that flipped the order would silently create duplicate junctions instead of failing loudly.

> Step-1 ships the v1.5c merge surface in one focused step. The 3 design decisions (same-category only, hard-delete source, 2-step confirm) are locked in the README. No new schema, no new auth surface.

---

## Resolved decisions (from README)

- **Cross-category**: hard block. Picker filters by source.category.
- **Source fate**: hard-delete. Direct call (bypasses the DELETE route's `usage_count > 0` gate, since stale `usage_count` would otherwise block).
- **Confirm flow**: 2-step. Pick target → confirm-with-count from `source.usage_count`. Merge response carries the actual count.

---

## Acceptance criteria

### API library — `mergeTag` (new function in `src/lib/api/tags.ts`)

- [ ] **AC1: A new `mergeTag(accessToken, sourceId, targetId)`** returns `Result<{ source_id, target_id, affected_days }, MergeTagError>`. The function performs the whole transaction internally (read junction rows → rewrite → recount target → hard-delete source).
- [ ] **AC2: `MergeTagError` variants**: `'same_tag'` (source === target) · `'source_not_found'` · `'target_not_found'` · `'source_archived'` · `'target_archived'` · `'category_mismatch'` · `'network_error'` · `'directus_error'`. Each guards a distinct failure mode and maps 1:1 to a 400 in the route (except the last two → 502).
- [ ] **AC3: Validation order**: same-tag check (source === target) → **combined** source+target tag read via single `readItems('tags', { filter: { id: { _in: [sourceId, targetId] } } })` → existence check (both rows present in result) → archived check → category match. Earliest-cheap-fastest-first. Each failure returns BEFORE any wire write. The combined read collapses what would be two round-trips into one; missing-row is detected by inspecting result length + ids.
- [ ] **AC4: Junction read** (two reads, NOT combined — see Technical Constraints for why): first `readItems('day_entries_tags', { filter: { tags_id: { _eq: source_id } }, fields: ['id', 'day_entries_id'] })`. Then `readItems('day_entries_tags', { filter: { _and: [{ tags_id: { _eq: target_id } }, { day_entries_id: { _in: <sourceDays> } }] }, fields: ['day_entries_id'] })`. Both bounded by source's effective count (target read is filtered to source days, so target's total size doesn't matter).
- [ ] **AC5: Rewrite via two bulk ID-array operations**, ordered. Partition source junction IDs by whether their `day_entries_id` is in the "already-has-target" set:
  - **Bulk DELETE overlap source junctions** by ID: `deleteItems('day_entries_tags', overlapJunctionIds)` (same SDK pattern as `day-entries.ts:236`). Removes the would-be duplicates.
  - **Bulk PATCH remaining source junctions** to point at target: `updateItems('day_entries_tags', nonOverlapJunctionIds, { tags_id: target_id })`. After the delete, the UNIQUE(`day_entries_id`, `tags_id`) constraint cannot fire — these junctions land on days where target has no row yet.
  Order is load-bearing: bulk PATCH first would collide on the UNIQUE constraint for every overlap day and the batch would fail. ID-array bulk ops (not filter-based) match the established pattern in `day-entries.ts`.
- [ ] **AC6: Target usage_count recount**: after the rewrite, count distinct `day_entries_id`s in `day_entries_tags` where `tags_id = target_id`. PATCH target tag's `usage_count` to that number. Brings the stored column back into truth.
- [ ] **AC7: Source hard-delete**: direct `deleteItem('tags', sourceId)` call (no route, no gate). At this point source has 0 junction references; the delete is safe.
- [ ] **AC8: affected_days = distinct count of `day_entries_id` from the source's junction set**. Returned in the success payload.

### Route handler — `POST /api/tags/[id]/merge` (new sub-route)

- [ ] **AC9: A new `src/app/api/tags/[id]/merge/route.ts`** exports `POST`. Standard auth stack: origin → session → rate-limit (`tagWriteRateLimiter`) → UUID-format gate on the path id → JSON body parse (must contain `target_tag_id` as a UUID-shape string).
- [ ] **AC10: Per-error mapping** from `mergeTag`'s `MergeTagError`:
  - `'invalid_target'` (body validation, route-level) → 400
  - `'same_tag'` → 400
  - `'source_not_found'` / `'target_not_found'` → 400 (defensive — the picker shouldn't surface invalid ids in normal flow)
  - `'source_archived'` / `'target_archived'` → 400
  - `'category_mismatch'` → 400
  - `'network_error'` / `'directus_error'` → 502 `server_error`
- [ ] **AC11: 200 response**: `{ source_id, target_id, affected_days }`. JSON content type, no extra wrapping.

### Hook — extend `useTagManage` (no new hook needed)

- [ ] **AC12: A new `merge(sourceId, targetId)` method** added to `useTagManage`. POSTs to `/api/tags/[sourceId]/merge` with `{ target_tag_id: targetId }`. Returns `Promise<{ source_id, target_id, affected_days } | null>`. Calls `router.refresh()` on success. Per-error code surfaces in `lastError` (no `router.refresh` on failure). AbortController supersedes prior in-flight calls — same pattern as the other methods on the hook.

### Components — picker + form integration

- [ ] **AC13: A new `TagMergeTargetPickerSheet` component** at `src/components/tag-merge-target-picker-sheet.tsx`. Props: `{ source: Tag, tags: Tag[], open: boolean, onClose, onMergeConfirmed: (target: Tag) => void, saving: boolean, lastError: string | null }`. Renders a nested BottomSheet with title "Samenvoegen met...", lists non-archived tags in `source.category` excluding `source.id`, sorted alphabetically (no recency map needed — corpus stays small within a category). Tap a row → picker switches to internal confirm-mode (pending target held in local state). Tap "Ja, samenvoegen" → `onMergeConfirmed(target)`. Tap "Annuleer" → back to list. Picker owns the confirm UI; parent only sees the confirmed callback.
- [ ] **AC14: Picker empty state**: if there are no eligible same-category targets, only a muted line `Geen andere tags in deze categorie om mee samen te voegen.` Defensive — AC15's disabled-button check prevents opening the picker in this state under normal flow, but the empty list renders correctly if `tags` changes between button-tap and picker-mount.
- [ ] **AC15: `TagFormSheet` gets a "Samenvoegen met..." button** in the action row, BELOW the Verwijder button. To compute "no same-category non-archived alternatives", `TagFormSheet` gains a new prop `tags: Tag[]` (full non-archived corpus, forwarded from `TagManagementSection` which already holds it for sort/grouping). Disabled when:
  - `useTagManage.status === 'saving'`, OR
  - `tag.archived_at !== null` (can't merge from an archive), OR
  - `tags.filter(t => t.category === tag.category && t.archived_at === null && t.id !== tag.id).length === 0`.
- [ ] **AC16: Tapping "Samenvoegen met..." opens the picker** (nested inside `TagFormSheet`; sheet-over-sheet pattern matches the episode-side `TagPickerSheet` from step-5). Picker open-state is local to `TagFormSheet`.
- [ ] **AC17: Tapping a target row in the picker switches it to internal confirm-mode**. The confirm `role="alertdialog"` renders inline within the picker (sharing the picker's focus trap, NOT a new sheet). Prompt copy uses `source.usage_count` for the day count. Focus lands on `Annuleer` on appear. Picker holds the pending target in local state until Ja / Annuleer resolves it.
- [ ] **AC18: Tapping "Ja, samenvoegen"** fires `onMergeConfirmed(target)` from the picker. `TagFormSheet` wires this callback to `useTagManage.merge(source.id, target.id)`. On success: picker closes + `TagFormSheet` closes (source no longer exists — the form has nothing to show). `onMerged?: (affected_days: number)` callback on `TagFormSheet` fires upward so `TagManagementSection` can surface the count if it wants.
- [ ] **AC19: Tapping "Annuleer"** dismisses the confirm; picker stays on the list so the user can pick a different target. `onMergeConfirmed` is NOT called.

### Rate-limit

- [ ] **AC20: Merge counts against `tagWriteRateLimiter`** (200/5min budget set in v1.5b). One merge = one write from the limiter's perspective regardless of how many junction rewrites happen internally — anti-abuse is at the user-action level.

### Cross-feature integrity

- [ ] **AC21: Daily flow UNCHANGED**. `TagCategoryList` + `QuickEntryFlow` continue working; after a merge, the source tag is gone from the picker, the target's recency score reflects the union.
- [ ] **AC22: Episode-side `TagPickerSheet` UNCHANGED**. Linked-tag picker on episode edit doesn't gain a merge affordance.
- [ ] **AC23: Tag-management list re-renders correctly** after merge via `router.refresh()`. Source row is gone; target row's `usage_count` reflects the recount.

---

## Technical constraints

- **No schema changes.** All operations on existing collections (`tags`, `day_entries_tags`).
- **Single-purpose merge route.** Does NOT also accept rename/recategorize/etc. — those go through the existing PATCH route.
- **Direct hard-delete (bypassing the gated DELETE route).** The `mergeTag` lib function calls `deleteItem('tags', sourceId)` directly via the Directus SDK after the rewrite. The DELETE route's `usage_count > 0 → 400 tag_in_use` gate would block merge if usage_count had drifted; the merge is the authority on whether it's safe to delete the source.
- **Recount target's usage_count post-rewrite.** Even if the stored value was accurate before merge, it WILL drift unless we recount — the merge moves N junctions into target, and the dedup case (where target was already on a day) means net new count is `target_pre + source_new_only`, not `target_pre + source_total`.
- **Bulk ID-array operations, ordered.** The rewrite is two bulk SDK calls (`deleteItems` then `updateItems` on `day_entries_tags`), NOT N per-row writes. Order is load-bearing AND DB-enforced (step 0 added `UNIQUE(day_entries_id, tags_id)` on the junction; reversed order would hit the constraint on every overlap day and fail the entire batch with PG error 23505, so the bug surfaces immediately if a refactor flips the order). The combined source/target tag read in AC3 + the two junction reads in AC4 + two bulk writes + target.usage_count PATCH + source DELETE = **5 Directus round-trips per merge**, regardless of source size (assuming source.usage_count ≤ ~hundreds; very large sources would need pagination on the AC4 reads but that's a v2 concern).
- **One user-action = one rate-limit token = ≤5 internal Directus round-trips.** `tagWriteRateLimiter` (200/5min) counts the route hit, not the internal SDK calls. Anti-abuse is at the user-action level; internal-RTT count is bounded by AC5's design regardless of source size. Worth knowing if a future drift-recount script runs many merges in succession — would chew the limiter at user-action cadence, not RTT cadence.
- **Unsaved field edits in `TagFormSheet` are silently discarded** if the user taps merge mid-edit. The source no longer exists post-merge so any unsaved label / category / parent change is moot. The button does NOT prompt "wijzigingen niet bewaard" (consistent with hard-delete from v1.5b which also silently discards).
- **`AbortController.merge` cancels the client request only.** Server-side bulk writes are atomic per-step but the full 4-step sequence (junction-delete, junction-patch, target-recount, source-delete) is NOT transactional. Mid-merge abort + UI close = user must `router.refresh()` (or reopen the form) to see actual state. In practice: single tap → single confirm → no realistic abort path; documented for completeness so the next maintainer doesn't assume rollback semantics that aren't there.
- **TOCTOU** between read and rewrite is the documented limitation (same posture as step-5 + step-1 of tag-management-settings).
- **Picker sort: alphabetical, not recency.** Within one category at ~10-20 tags, the corpus is small; alphabetical is more predictable than recency for finding a specific target.
- **Source archived check**: a merge FROM an archived source is blocked (returns `'source_archived'`). Rationale: if a tag is archived, the user shouldn't be incidentally rewriting history from a state they thought was retired. Recovery: un-archive first, then merge.
- **Target archived check**: same blocked. Don't bring an archive back to life via merge.

---

## Test plan

### API library (`src/lib/api/__tests__/tags.test.ts` — EXTEND)

1. `mergeTag` with `source === target` → `'same_tag'` BEFORE any wire call.
2. `mergeTag` source/target tag read is **one combined `readItems('tags', { filter: { id: { _in: [source, target] } } })` call**, NOT two separate reads (AC3).
3. `mergeTag` where source tag missing from the combined-read result → `'source_not_found'`.
4. `mergeTag` where target tag missing from the combined-read result → `'target_not_found'`.
5. `mergeTag` where source is archived → `'source_archived'`.
6. `mergeTag` where target is archived → `'target_archived'`.
7. `mergeTag` where categories differ → `'category_mismatch'`.
8. `mergeTag` happy path with no overlap (source has 3 junctions, target has 0 on those days) → bulk DELETE called with empty ID array (no-op or skipped); bulk PATCH called with all 3 source-junction IDs and `{ tags_id: target }`; source deleted; target.usage_count = 3; affected_days = 3.
9. `mergeTag` happy path with full overlap (source has 3 junctions, target has 3 on the SAME days) → bulk DELETE called with all 3 source-junction IDs; bulk PATCH called with empty ID array (no-op or skipped); source deleted; target.usage_count unchanged at 3; affected_days = 3.
10. `mergeTag` happy path with partial overlap (source has 3 junctions; target on 1 of those days already) → bulk DELETE called with the 1 overlap ID; bulk PATCH called with the 2 non-overlap IDs; source deleted; target.usage_count = 3; affected_days = 3.
11. `mergeTag` always issues the bulk DELETE BEFORE the bulk PATCH (call order is load-bearing for the UNIQUE constraint).
12. `mergeTag` recomputes target.usage_count from the actual junction-row count post-rewrite (catches drift; not derived from `source.usage_count + delta` math).
13. `mergeTag` surfaces network errors as `'network_error'`.
14. `mergeTag` surfaces other Directus failures as `'directus_error'`.

### Route handler (`src/app/api/tags/[id]/merge/__tests__/route.test.ts` — NEW)

15. POST happy path → 200 with `{ source_id, target_id, affected_days }`.
16. POST with non-UUID source id in URL → 400 `invalid_id`.
17. POST with missing `target_tag_id` in body → 400 `malformed_body`.
18. POST with non-UUID `target_tag_id` → 400 `invalid_target`.
19. POST without session cookie → 401.
20. POST from disallowed origin → 403.
21. POST rate-limited → 429.
22. POST when lib reports `same_tag` → 400 `same_tag`.
23. POST when lib reports `source_archived` → 400 `source_archived`.
24. POST when lib reports `target_archived` → 400 `target_archived`.
25. POST when lib reports `category_mismatch` → 400 `category_mismatch`.
26. POST when lib reports `source_not_found` or `target_not_found` → 400 with that code.
27. POST when lib reports `directus_error` → 502 `server_error`.

### Hook (`src/hooks/__tests__/use-tag-manage.test.ts` — EXTEND)

28. `merge(source, target)` POSTs to `/api/tags/[source]/merge` with `{ target_tag_id: target }`.
29. `merge` on 200 calls `router.refresh()` and returns the `{ source_id, target_id, affected_days }` payload.
30. `merge` on 400 returns null, sets `status='error'`, `lastError` = the error code, does NOT call `router.refresh()`.
31. `merge` AbortController supersede semantics — back-to-back calls cancel earlier ones (with the explicit caveat that abort does NOT roll back server-side work; see Technical Constraints).

### `TagMergeTargetPickerSheet` (`src/components/__tests__/tag-merge-target-picker-sheet.test.tsx` — NEW)

32. Renders a BottomSheet with title "Samenvoegen met...".
33. Lists ONLY non-archived tags in the source's category, sorted alphabetically.
34. Excludes the source from the list (no self-merge offered).
35. Tap a row switches the picker into confirm-mode (confirm alertdialog renders); does NOT call `onMergeConfirmed` yet (pending target held in local state).
36. Tap `Ja, samenvoegen` in confirm calls `onMergeConfirmed(target)` with the pending target.
37. Tap `Annuleer` in confirm returns to list mode; does NOT call `onMergeConfirmed`.
38. Server error banner renders when `lastError` is set.
39. Empty-state line renders when no eligible targets exist.
40. Close button + drag-down call `onClose`.

### `TagFormSheet` integration (`src/components/__tests__/tag-form-sheet.test.tsx` — EXTEND)

41. `TagFormSheet` accepts a new `tags: Tag[]` prop (defaults to `[]` for back-compat with existing call sites; the new merge button is the only consumer).
42. "Samenvoegen met..." button is rendered in the action row.
43. Button is DISABLED when `tag.archived_at !== null`.
44. Button is DISABLED when `tags` contains no same-category non-archived alternatives (filtered as in AC15).
45. Button is ENABLED when `tags` contains at least one same-category non-archived other tag.
46. Tapping the button opens the picker.
47. Tapping a target row in the picker → confirm alertdialog renders with `source.usage_count` in the prompt.
48. Confirm dialog focus lands on `Annuleer`.
49. Tapping `Annuleer` dismisses the confirm; picker stays open.
50. Tapping `Ja, samenvoegen` calls `hook.merge(source.id, target.id)`.
51. On merge success, both the picker AND the `TagFormSheet` close (source no longer exists).

### Cross-feature regression

52. `TagCategoryList` tests stay green (AC21).
53. Episode-side `TagPickerSheet` tests stay green (AC22).
54. Tag-management-settings tests stay green (AC23) — note `TagManagementSection` must forward its existing `allTags` corpus to `TagFormSheet` via the new `tags` prop.

### Smoke (`scripts/tag-merge-smoke.mjs` — NEW + run-tag-merge-smoke.ps1 wrapper)

55. Login → create source tag `_merge src` + target tag `_merge tgt` in the same category.
56. Seed: create a day_entry (via a POST to /api/day-entries/today or via direct Directus) with BOTH tags attached.
57. Call merge → 200 with `affected_days === 1`.
58. Directus read-back: source tag is gone (404 on direct read).
59. Directus read-back: target tag's `usage_count` reflects the merge.
60. Directus read-back: no junction rows reference the source.
61. Negative: merge same → same → 400 `same_tag`.
62. Negative: merge across categories → 400 `category_mismatch`.
63. Cleanup: hard-delete the seeded day_entry + target tag via admin.

---

## Build order (TDD shape — RED → GREEN → REFACTOR per phase)

Five phases. Verify gate green at each phase boundary.

1. **API library** — `mergeTag` (tests 1–14). RED, implement, GREEN. Refactor while green: extract `readJunctionRows(...)` helper if the lib function is hard to read; consider extracting `recountTagUsage(token, tagId)` for AC6 reuse (see Notes for the next feature).
2. **Route handler** — `POST /api/tags/[id]/merge` (tests 15–27). RED, implement, GREEN.
3. **Hook** — extend `useTagManage` with `merge` (tests 28–31). RED, implement, GREEN.
4. **Components** — `TagMergeTargetPickerSheet` (tests 32–40) + `TagFormSheet` integration (tests 41–51). RED, implement, GREEN. Copy additions land here. Includes wiring `tags` corpus from `TagManagementSection` → `TagFormSheet` → `TagMergeTargetPickerSheet`.
5. **Regression + smoke** — tests 52–54 stay green; smoke script ships (tests 55–63). Verify gate green; commit + push + deploy; production smoke.

Commit at each phase boundary.

---

## Out of scope (v1.5c — see also README §Out of scope)

- **Cross-category merge with category-change confirm**.
- **Bulk merge** (select N sources → one target). v2.
- **3-tag chain merge in one operation**. Run twice.
- **Undo / merge history**. The operation is irreversible by design.
- **Pre-flight preview screen with exact dates**. `source.usage_count` is the v1.5c approximation; the merge response carries the actual count.
- **Scheduled usage_count drift recount script**. The merge brings target back in line; the broader stored-count-drift problem is a separate cleanup.

---

## Notes for the next feature

What v1.5d / future features might want to remember:

- The `mergeTag` SDK function is reusable: a future "bulk merge" UI can call it N times serially. The route is single-source-single-target by design; bulk merge gets its own route if and when shipped.
- The bulk-delete-then-bulk-patch rewrite pattern (with the UNIQUE-constraint-aware ordering) is a template for any future operation that consolidates references in a junction table. The dedup-by-overlap-day is the subtle bit; copy it.
- The "hard-delete that bypasses the gated route" pattern is generalisable: any cross-collection cleanup that ends in a tag/episode/etc deletion can take this approach. Document the gate-bypass explicitly in the calling function's comment.
- **`recountTagUsage` extraction (architectural).** AC6's logic (count junction rows where `tags_id = X`, PATCH the tag's `usage_count` to that count) is the first place in the app that brings a stored aggregate column back into truth from junction-table reality. Future v1.6+ ops that touch junction tables outside of `QuickEntry` (a future scheduled drift-recount script, bulk-merge UI, direct day-entry tag-add via the API) should extract `recountTagUsage(token, tagId): Promise<Result<number, ...>>` from `mergeTag` and reuse it. Keep it side-effect-free except for the single PATCH — easy to test, easy to compose. If the recount opportunity grows beyond one call site during this build, do the extraction in Phase 1's REFACTOR slot; otherwise leave it as a comment-only "extract me" marker.
- **`usage_count` as a stored column is the underlying drift hazard.** The merge is the second consumer (after v1.5b's delete-with-gate) to depend on this column being accurate. If a third consumer appears in v1.6+, evaluate moving `usage_count` to a Directus computed field / view-backed aggregate. Otherwise the manual maintenance cost grows superlinearly with consumers.
