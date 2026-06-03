# Step 1: Tag merge (single step)

**Estimated time:** ~5 hours. Smaller surface than v1.5b: one new API library function, one new route, one new picker component, one new button + handler on the existing `TagFormSheet`. No schema change, no new external dependencies.
**Test layers:** Vitest unit tests for the new `mergeTag` SDK function (junction-rewrite logic, dedup, error variants). Vitest route tests for `POST /api/tags/[id]/merge` (standard auth stack + per-error mapping + 200 with affected_days). Vitest component tests for the new `TagMergeTargetPickerSheet` and the `TagFormSheet` integration (button visibility + tap-to-merge flow). Smoke script for the end-to-end production round-trip with a seeded duplicate.
**Risk:** Medium. The junction-rewrite operation is the only genuinely-new destructive cross-collection operation in the app to date (DELETE was atomic, this is read-then-rewrite-then-delete). Failure modes are recoverable per the README's transaction-safety table but each step needs explicit test coverage.
**Prerequisite:** Tag-management-settings shipped (commit `b58433f` + hotfixes `070b64c` / `b233c2d`). `TagFormSheet` exists and is extensible.

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
- [ ] **AC3: Validation order**: same-tag check (source === target) → source read → target read → archived check → category match. Earliest-cheap-fastest-first. Each failure returns BEFORE any wire write.
- [ ] **AC4: Junction read**: queries `day_entries_tags` for rows where `tags_id = source_id`, returning `day_entries_id` + junction `id`. Then queries `day_entries_tags` for rows where `tags_id = target_id AND day_entries_id IN <sourceDays>`, returning the set of "days already containing target". Two reads, both bounded by source's effective count.
- [ ] **AC5: Rewrite per junction**: if the day is in the "already-has-target" set → DELETE the source junction (avoid duplicate); else → PATCH the junction's `tags_id` from source to target. Operations are issued individually (not bulk) — Directus M2M junction tables don't support array PATCH the way day_entries does.
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

- [ ] **AC13: A new `TagMergeTargetPickerSheet` component** at `src/components/tag-merge-target-picker-sheet.tsx`. Props: `{ source: Tag, tags: Tag[], open: boolean, onClose, onTarget: (target: Tag) => void, saving: boolean, lastError: string | null }`. Renders a nested BottomSheet with title "Samenvoegen met...", lists non-archived tags in `source.category` excluding `source.id`, sorted alphabetically (no recency map needed — corpus stays small within a category). Tap a row → calls `onTarget(target)`. Server error banner reused.
- [ ] **AC14: Picker empty state**: if there are no eligible same-category targets, only a muted line `Geen andere tags in deze categorie om mee samen te voegen.`
- [ ] **AC15: `TagFormSheet` gets a "Samenvoegen met..." button** in the action row, BELOW the Verwijder button. Disabled when:
  - `useTagManage.status === 'saving'`, OR
  - `tag.archived_at !== null` (can't merge from an archive), OR
  - No same-category non-archived tags exist apart from `tag` itself.
- [ ] **AC16: Tapping "Samenvoegen met..." opens the picker** (nested inside `TagFormSheet`; sheet-over-sheet pattern matches the episode-side `TagPickerSheet` from step-5). Picker state is local to `TagFormSheet`.
- [ ] **AC17: Tapping a target row in the picker opens a confirm alertdialog** inside the picker (not nested again — confirm renders inline within the picker, sharing the picker's focus trap). Prompt copy uses `source.usage_count` for the day count. Focus lands on `Annuleer` on appear.
- [ ] **AC18: Tapping "Ja, samenvoegen"** calls `useTagManage.merge(source.id, target.id)`. On success: close picker + close `TagFormSheet` (the source is gone — the form has nothing to show). `onMerged?: (affected_days: number)` callback fires for the parent to surface the count if it wants.
- [ ] **AC19: Tapping "Annuleer"** dismisses the confirm; picker stays open so the user can pick a different target.

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
- **Per-junction operation, not bulk.** Each junction row is either updated or deleted individually. With typical source usage_count ≤ 50 and the Directus SDK's keep-alive connections, this is fast enough. If a future merge hits hundreds, a bulk endpoint is the optimization (out of scope).
- **TOCTOU** between read and rewrite is the documented limitation (same posture as step-5 + step-1 of tag-management-settings).
- **Picker sort: alphabetical, not recency.** Within one category at ~10-20 tags, the corpus is small; alphabetical is more predictable than recency for finding a specific target.
- **Source archived check**: a merge FROM an archived source is blocked (returns `'source_archived'`). Rationale: if a tag is archived, the user shouldn't be incidentally rewriting history from a state they thought was retired. Recovery: un-archive first, then merge.
- **Target archived check**: same blocked. Don't bring an archive back to life via merge.

---

## Test plan

### API library (`src/lib/api/__tests__/tags.test.ts` — EXTEND)

1. `mergeTag` with `source === target` → `'same_tag'` BEFORE any wire call.
2. `mergeTag` where source tag doesn't exist → `'source_not_found'`.
3. `mergeTag` where target tag doesn't exist → `'target_not_found'`.
4. `mergeTag` where source is archived → `'source_archived'`.
5. `mergeTag` where target is archived → `'target_archived'`.
6. `mergeTag` where categories differ → `'category_mismatch'`.
7. `mergeTag` happy path with no overlap (source has 3 junctions, target has 0 on those days) → all 3 junctions PATCHed to target; source deleted; target.usage_count = 3; affected_days = 3.
8. `mergeTag` happy path with full overlap (source has 3 junctions, target has 3 on the SAME days) → all 3 source junctions DELETED (dedup); source deleted; target.usage_count unchanged at 3; affected_days = 3.
9. `mergeTag` happy path with partial overlap (source has 3 junctions; target on 1 of those days already) → 2 PATCHed, 1 DELETED; source deleted; target.usage_count = 3; affected_days = 3.
10. `mergeTag` recomputes target.usage_count from the actual junction-row count (catches drift).
11. `mergeTag` surfaces network errors as `'network_error'`.
12. `mergeTag` surfaces other Directus failures as `'directus_error'`.

### Route handler (`src/app/api/tags/[id]/merge/__tests__/route.test.ts` — NEW)

13. POST happy path → 200 with `{ source_id, target_id, affected_days }`.
14. POST with non-UUID source id in URL → 400 `invalid_id`.
15. POST with missing `target_tag_id` in body → 400 `malformed_body`.
16. POST with non-UUID `target_tag_id` → 400 `invalid_target`.
17. POST without session cookie → 401.
18. POST from disallowed origin → 403.
19. POST rate-limited → 429.
20. POST when lib reports `same_tag` → 400 `same_tag`.
21. POST when lib reports `source_archived` → 400 `source_archived`.
22. POST when lib reports `target_archived` → 400 `target_archived`.
23. POST when lib reports `category_mismatch` → 400 `category_mismatch`.
24. POST when lib reports `source_not_found` or `target_not_found` → 400 with that code.
25. POST when lib reports `directus_error` → 502 `server_error`.

### Hook (`src/hooks/__tests__/use-tag-manage.test.ts` — EXTEND)

26. `merge(source, target)` POSTs to `/api/tags/[source]/merge` with `{ target_tag_id: target }`.
27. `merge` on 200 calls `router.refresh()` and returns the `{ source_id, target_id, affected_days }` payload.
28. `merge` on 400 returns null, sets `status='error'`, `lastError` = the error code, does NOT call `router.refresh()`.
29. `merge` AbortController supersede semantics — back-to-back calls cancel earlier ones.

### `TagMergeTargetPickerSheet` (`src/components/__tests__/tag-merge-target-picker-sheet.test.tsx` — NEW)

30. Renders a BottomSheet with title "Samenvoegen met...".
31. Lists ONLY non-archived tags in the source's category, sorted alphabetically.
32. Excludes the source from the list (no self-merge offered).
33. Tap a row calls `onTarget(target)` with that target tag.
34. Server error banner renders when `lastError` is set.
35. Empty-state line renders when no eligible targets exist.
36. Close button + drag-down call `onClose`.

### `TagFormSheet` integration (`src/components/__tests__/tag-form-sheet.test.tsx` — EXTEND)

37. "Samenvoegen met..." button is rendered in the action row.
38. Button is DISABLED when `tag.archived_at !== null`.
39. Button is DISABLED when there are no same-category non-archived alternatives.
40. Button is ENABLED when there's at least one same-category non-archived other tag.
41. Tapping the button opens the picker.
42. Tapping a target row in the picker → confirm alertdialog renders with the source.usage_count in the prompt.
43. Confirm dialog focus lands on `Annuleer`.
44. Tapping `Annuleer` dismisses the confirm; picker stays open.
45. Tapping `Ja, samenvoegen` calls `hook.merge(source.id, target.id)`.
46. On merge success, both the picker AND the `TagFormSheet` close (source no longer exists).

### Cross-feature regression

47. `TagCategoryList` tests stay green (AC21).
48. Episode-side `TagPickerSheet` tests stay green (AC22).
49. Tag-management-settings tests stay green (AC23).

### Smoke (`scripts/tag-merge-smoke.mjs` — NEW + run-tag-merge-smoke.ps1 wrapper)

50. Login → create source tag `_merge src` + target tag `_merge tgt` in the same category.
51. Seed: create a day_entry (via a POST to /api/day-entries/today or via direct Directus) with BOTH tags attached.
52. Call merge → 200 with `affected_days === 1`.
53. Directus read-back: source tag is gone (404 on direct read).
54. Directus read-back: target tag's `usage_count` reflects the merge.
55. Directus read-back: no junction rows reference the source.
56. Negative: merge same → same → 400 `same_tag`.
57. Negative: merge across categories → 400 `category_mismatch`.
58. Cleanup: hard-delete the seeded day_entry + target tag via admin.

---

## Build order (TDD shape — RED → GREEN → REFACTOR per phase)

Five phases. Verify gate green at each phase boundary.

1. **API library** — `mergeTag` (tests 1–12). RED, implement, GREEN. Refactor while green: extract `readJunctionRows(...)` helper if the lib function is hard to read.
2. **Route handler** — `POST /api/tags/[id]/merge` (tests 13–25). RED, implement, GREEN.
3. **Hook** — extend `useTagManage` with `merge` (tests 26–29). RED, implement, GREEN.
4. **Components** — `TagMergeTargetPickerSheet` (tests 30–36) + `TagFormSheet` integration (tests 37–46). RED, implement, GREEN. Copy additions land here.
5. **Regression + smoke** — tests 47–49 stay green; smoke script ships (tests 50–58). Verify gate green; commit + push + deploy; production smoke.

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
- The per-junction rewrite pattern (read → diff → patch-or-delete) is a template for any future operation that consolidates references. The dedup case is the subtle bit; copy it.
- The "hard-delete that bypasses the gated route" pattern is generalisable: any cross-collection cleanup that ends in a tag/episode/etc deletion can take this approach. Document the gate-bypass explicitly in the calling function's comment.
