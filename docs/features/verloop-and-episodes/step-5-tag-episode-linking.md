# Step 5: Tag-to-episode linking from episode detail

**Estimated time:** ~6 hours (substantial API extension + new picker UI surface + integration with existing EpisodeFormSheet).
**Test layers:** Vitest domain test for `validateParentEpisodeId`. Vitest unit tests for `createOrUpsertTag` (extended) and the new `updateTag`. Vitest route tests for the extended `POST /api/tags` and the new `PATCH /api/tags/[id]`. Vitest hook test for `useTagLinkUpsert`. Vitest component tests for the new `LinkedTagsSection`, `TagPickerSheet`, and the EpisodeFormSheet integration. Regression: existing QuickEntryFlow / TagCategoryList tests stay green (AC-F8). Smoke: extend `tags-smoke.mjs` (or `episodes-smoke.mjs`) to cover the linking + unlinking round-trip.
**Risk:** Medium. The API extension touches an existing wire contract (POST /api/tags) — care needed to keep the daily-flow inline-tag-creation path unchanged. New PATCH route is greenfield. Nested BottomSheet over BottomSheet is a new pattern in this app — needs verification on iOS PWA (focus trap, scroll lock, drag-down behaviour through two layers).
**Prerequisite:** Step-4 GREEN + deployed. EpisodeFormSheet ships create + edit + archive. Episodes are persisted with a stable id, which is what we'll be writing into `tags.parent_episode_id`.

> Step-5 closes the feature loop. From inside an existing episode's edit form, the user can attach existing tags or create a new tag with the parent pre-set in one round-trip. The daily-flow tag picker in `QuickEntryFlow` does NOT change — linking lives entirely in the Context tab's episode edit surface.

---

## Resolved decisions (2026-06-02)

All four open design questions were settled before drafting:

- **Picker UI shape**: **Nested BottomSheet over the EpisodeFormSheet**. Same primitive as the form itself; consistent thumb-first feel; long lists scroll inside the sheet. Verified-via-test that drag-down on the picker returns to the form, not to the page.
- **Picker contents**: **All non-archived tags, grouped by the 8-category enum**. Tags already linked to a DIFFERENT episode show a `(bij: <label>)` badge so the user knows what they'd move; tags linked to THIS episode are hidden (they're already in the LinkedTagsSection above). Search/filter deferred — corpus is ~83 today, list with sticky category headers is scannable.
- **Conflict rule when a tag is already linked elsewhere**: **Silent re-parent**. Tapping the tag PATCHes its `parent_episode_id` to the current episode. Mirrors the README's "renaming an episode propagates globally" stance — references are by id, the link is metadata. Undo = pick the tag back from the original episode's picker. No confirm dialog (the app has none).
- **Inline create-with-parent**: **One round-trip**. The picker's `+ Maak een nieuwe tag aan` CTA opens an inline mini-form (label + category select). Submit POSTs to `/api/tags` with `{ label, category, parent_episode_id }` in a single request — `createOrUpsertTag` is extended to accept the optional field.

---

## Open decisions to confirm before build

None. All four design calls above are settled.

---

## Acceptance criteria

### Domain layer

- [ ] **AC1: `validateParentEpisodeId(value: unknown): Result<string | null, 'invalid_parent_episode_id'>`** lives at `src/lib/domain/parent-episode-id.ts`.
  - `null` → ok with `null`.
  - String matching the UUID regex (same regex as `src/app/api/episodes/[id]/route.ts`) → ok with the value.
  - Anything else (empty string, malformed UUID, number, object) → err `'invalid_parent_episode_id'`.

### API library

- [ ] **AC2: `CreateOrUpsertTagInput` is extended** with `parent_episode_id?: string | null` (optional). Backwards-compatible — omitting it preserves the current "create unlinked" behaviour. When present:
  - `null` → tag is created (or upserted) with `parent_episode_id: null`.
  - UUID string → tag is created with `parent_episode_id: <UUID>`. If the upsert hits the `matched_active` branch AND the existing tag's parent differs, the function PATCHes the parent before returning (returns `matched_active` with the updated row). If `matched_reactivated`, the parent is set as part of the single reactivation PATCH (not a second round-trip).
- [ ] **AC3: `createOrUpsertTag` validates `parent_episode_id` via `validateParentEpisodeId`** before any wire call. Returns err `'invalid_parent_episode_id'` on a malformed UUID. Reuses `CreateOrUpsertTagError` union (extended).
- [ ] **AC4: `updateTag(accessToken, id, patch): Result<Tag, TagsError | 'invalid_patch'>`** lives in `src/lib/api/tags.ts`. Today's `patch` shape is `{ parent_episode_id: string | null }`; the function validates the field through `validateParentEpisodeId` and rejects unknown keys. Returns the updated tag (mapped through `rowToTag`). No fetch-then-validate dance (PATCH a single scalar — TOCTOU is not a real risk here, mirroring the day-entries `score` PATCH pattern).

### Route handlers

- [ ] **AC5: `POST /api/tags` accepts `parent_episode_id` in the body** (optional). When present, it's threaded through to `createOrUpsertTag` after the existing label + category validation. Malformed UUID returns `400 { error: 'invalid_parent_episode_id' }`. Existing 200 / 400 / 401 / 403 / 429 / 502 paths unchanged. The rate limiter (`tagWriteRateLimiter`) is unchanged — this is still a tag write.
- [ ] **AC6: A new `PATCH /api/tags/[id]/route.ts`** mirrors the structure of `PATCH /api/episodes/[id]/route.ts`:
  - Origin check (403), session check (401), rate-limit check via `tagWriteRateLimiter` (429), UUID format gate on `id` (400 `invalid_id`), body parsing (400 `malformed_body`).
  - Body must be `{ parent_episode_id: string | null }`. Any other key returns 400 `invalid_patch`.
  - Calls `updateTag` → 200 with the updated tag, or 502 on `directus_error` / `network_error`.

### Hook + state

- [ ] **AC7: A new `useTagLinkUpsert()` hook** lives at `src/hooks/use-tag-link-upsert.ts`. Three methods, all return `Promise<Tag | null>` and trigger `router.refresh()` on success:
  - `createWithParent({ label, category, parent_episode_id })` → POST /api/tags.
  - `link(tagId, episodeId)` → PATCH /api/tags/[id] with `{ parent_episode_id: episodeId }`.
  - `unlink(tagId)` → PATCH /api/tags/[id] with `{ parent_episode_id: null }`.
  - Same status machine as `useEpisodeUpsert`: `idle | saving | saved | error`, `lastError` string, AbortController + mountedRef cleanup. Single in-flight call only (subsequent calls while `saving` are dropped — mirrors `useEpisodeUpsert`).

### LinkedTagsSection

- [ ] **AC8: A new `LinkedTagsSection` component** lives at `src/components/linked-tags-section.tsx`. Pure presentational; receives `{ episode: Episode, tags: Tag[], onOpenPicker: () => void }` props. Renders:
  - h3 heading `Tags die hierbij horen` (uppercase + tracking-wider, same style as the Periodes sub-group headings).
  - Chip list for tags where `tag.parent_episode_id === episode.id`. Each chip shows the label and has a small `✕` button (min 44×44 effective tap target via padding) that calls the unlink hook method.
  - When no tags are linked, a muted line: `Nog geen gekoppelde tags.` (no extra prose — brainfog rule).
  - A `+ Tag` button (44×44 min, same style as the Periodes launchers) that calls `onOpenPicker`.
- [ ] **AC9: LinkedTagsSection only renders in EpisodeFormSheet's edit mode.** In create mode there is no episode id to link against, so the section is omitted entirely. (Tested explicitly — see Test plan.)

### TagPickerSheet

- [ ] **AC10: A new `TagPickerSheet` component** lives at `src/components/tag-picker-sheet.tsx`. Receives `{ episode: Episode, tags: Tag[], open: boolean, onClose: () => void, onPicked: () => void }`. Renders a BottomSheet (nested over EpisodeFormSheet) containing:
  - Title: `Kies of maak een tag`.
  - At the top: `+ Maak een nieuwe tag aan` button. Tapping it expands an inline mini-form (label `<input>` + category `<select>` from the 8-category enum) and a `Bewaar` button. Submit → `createWithParent` → close picker on success.
  - Below the create CTA: tags grouped by category (sticky h3 per category). For each tag, a row showing the label; rows for tags linked to a DIFFERENT episode also show a small muted suffix `(bij: <ander episode label>)`. Tags linked to THIS episode are filtered out (already in the LinkedTagsSection above).
  - Tap a row → `link(tag.id, episode.id)` (silent re-parent if needed) → close picker via `onPicked`.
  - Server error → top-of-sheet banner reusing the existing error pattern from EpisodeFormSheet.
- [ ] **AC11: Picker handles the empty-corpus state**: if there are no eligible tags (e.g. all tags are already linked to this episode OR the corpus is empty), only the `+ Maak een nieuwe tag aan` CTA is shown with the muted line `Nog geen andere tags. Maak er een aan.`

### EpisodeFormSheet integration

- [ ] **AC12: EpisodeFormSheet accepts a new `tags: Tag[]` prop.** It renders `LinkedTagsSection` between the description field and the action row, only when `mode === 'edit' && initialEpisode !== null`. Picker `open` state lives inside EpisodeFormSheet (the form OWNS the picker since the picker is conceptually a sub-action of the form).
- [ ] **AC13: ContextView threads tags through.** ContextView accepts a new `tags: Tag[]` prop and passes it to EpisodeFormSheet. TodayShell threads its existing `tags` prop to ContextView. `page.tsx` already calls `readAllTags` — no new server call.

### Cross-feature integrity

- [ ] **AC14: The daily-flow tag picker (`TagCategoryList` in QuickEntryFlow) is UNCHANGED.** No regression: existing component tests stay green, no new affordance is added to the daily flow. (Verifies AC-F8 in the README.)
- [ ] **AC15: `parent_episode_id` is preserved across tag reactivation.** When `createOrUpsertTag` hits the `matched_reactivated` branch (the row was archived) and `parent_episode_id` is set in the input, the reactivation PATCH sets it in the same call — no two-step. (The existing `RESET_ON_REACTIVATE` columns — `archived_at: null, project_id: null, usage_count: 0` — are preserved; the parent is merged in for this code path.)
- [ ] **AC16: AC-F7 in README ticked.** "From an episode detail, the user can attach an existing tag or create a new tag with the parent set."

---

## Technical constraints

- **The UUID regex** is the same one already used in `src/app/api/episodes/[id]/route.ts`: `/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i`. Extract to `src/lib/domain/uuid.ts` if it's now used in 3+ places; otherwise inline it in `parent-episode-id.ts` (one occurrence is fine, two is a pattern, three demands extraction — checked at build time).
- **Domain validator placement**: `validateParentEpisodeId` lives in `src/lib/domain/parent-episode-id.ts` to mirror `episode-category.ts`, `episode-label.ts`, etc. No new sub-folder.
- **No Zod**, per `.claude/conventions.md`. Validation stays as the strict-shape domain validators returning `Result<T, E>`.
- **No client cache**: same `router.refresh()` invalidation primitive across all three mutations (createWithParent / link / unlink). The server re-runs, the fresh tags prop arrives, the section + picker re-derive.
- **No optimistic updates**. Single-user single-device app; the network round-trip to Fly + Directus is fast enough that the saving state is acceptable.
- **Nested BottomSheet semantics**: the picker is mounted INSIDE EpisodeFormSheet's React tree but is a sibling DOM portal at the document root (via the BottomSheet primitive's existing portal). Focus trap: when picker opens, focus moves to the picker; when picker closes, focus returns to the `+ Tag` button. Verified-via-test for keyboard nav.
- **Scroll lock through two layers**: BottomSheet's existing scroll-lock hook handles the body. When picker opens on top of the form, the form's interior scroll is unaffected by the picker's open state — the lock is body-level, not form-level. Verified manually on iOS PWA.
- **Picker rate-limiting**: `tagWriteRateLimiter` is shared across POST /api/tags AND PATCH /api/tags/[id]. 60 writes / 5 min is high enough for a real user (a flurry of linking activity on episode creation is ~10 calls); the limit is anti-abuse, not anti-user.
- **Idempotency of re-parent**: PATCH /api/tags/[id] with `{ parent_episode_id: X }` is naturally idempotent — same call twice → same final state. No `If-Match` header needed for v1.5.
- **No PATCH /api/tags/[id] returns 404**: missing tag id surfaces as a Directus error (`directus_error` → 502) rather than a 404. Acceptable for v1.5 — single-user app, the picker only shows ids it just read.

---

## Test plan

### Domain (`src/lib/domain/__tests__/parent-episode-id.test.ts`)

1. `null` returns ok with `null`.
2. Valid UUID v4 returns ok with the value.
3. Empty string returns err `'invalid_parent_episode_id'`.
4. Non-UUID string returns err `'invalid_parent_episode_id'`.
5. Malformed UUID (wrong segment lengths) returns err `'invalid_parent_episode_id'`.
6. Number returns err `'invalid_parent_episode_id'`.
7. Object returns err `'invalid_parent_episode_id'`.

### API library (`src/lib/api/__tests__/tags.test.ts` — extend existing)

8. `createOrUpsertTag` with no `parent_episode_id` in input → tag created with `parent_episode_id: null` (regression — existing daily-flow path).
9. `createOrUpsertTag` with `parent_episode_id: <UUID>` in input → tag created with parent set (single POST to Directus).
10. `createOrUpsertTag` hits matched_active AND input `parent_episode_id` differs from existing → returns `matched_active` with the PATCHED parent (verifies the in-branch PATCH).
11. `createOrUpsertTag` hits matched_active AND input `parent_episode_id` matches existing → returns `matched_active` with no PATCH (idempotent — verifies no wasted wire call).
12. `createOrUpsertTag` hits matched_reactivated AND input `parent_episode_id` is set → reactivation PATCH includes `parent_episode_id` in the same body alongside `RESET_ON_REACTIVATE` (single round-trip).
13. `createOrUpsertTag` with malformed `parent_episode_id` → returns err `'invalid_parent_episode_id'` BEFORE any wire call.
14. `updateTag` happy path → returns ok with the updated tag mapped through `rowToTag`.
15. `updateTag` with `parent_episode_id: null` → returns ok with the tag (unlinked).
16. `updateTag` with malformed UUID in patch → returns err `'invalid_patch'`.
17. `updateTag` with extra unknown key in patch → returns err `'invalid_patch'`.
18. `updateTag` on network failure → returns err `'network_error'`.
19. `updateTag` on Directus error → returns err `'directus_error'`.

### Route handler `POST /api/tags` (`src/app/api/tags/__tests__/route.test.ts` — extend existing)

20. POST with no `parent_episode_id` in body → 200, tag created unlinked (regression).
21. POST with `parent_episode_id: <UUID>` in body → 200, tag returned with parent set.
22. POST with `parent_episode_id: null` in body → 200, tag returned unlinked (explicit null).
23. POST with malformed `parent_episode_id` → 400 `{ error: 'invalid_parent_episode_id' }`.

### Route handler `PATCH /api/tags/[id]` (`src/app/api/tags/[id]/__tests__/route.test.ts` — NEW)

24. PATCH with valid id + `{ parent_episode_id: <UUID> }` → 200 with updated tag.
25. PATCH with valid id + `{ parent_episode_id: null }` → 200 with updated tag (unlinked).
26. PATCH with non-UUID id in path → 400 `{ error: 'invalid_id' }`.
27. PATCH with empty body → 400 `{ error: 'malformed_body' }`.
28. PATCH with unknown key in body → 400 `{ error: 'invalid_patch' }`.
29. PATCH without session cookie → 401.
30. PATCH from disallowed origin → 403.
31. PATCH rate-limited (61st write in 5 min) → 429 with `retry_after_ms`.
32. PATCH with a UUID that doesn't exist in Directus → 502 (mirrors PATCH /api/episodes/[id]).

### Hook (`src/hooks/__tests__/use-tag-link-upsert.test.ts` — NEW)

33. `createWithParent` POSTs to /api/tags with `{ label, category, parent_episode_id }` and calls `router.refresh()` on success.
34. `link(tagId, episodeId)` PATCHes /api/tags/[tagId] with `{ parent_episode_id: episodeId }` and calls `router.refresh()`.
35. `unlink(tagId)` PATCHes /api/tags/[tagId] with `{ parent_episode_id: null }` and calls `router.refresh()`.
36. Failed mutation surfaces `lastError` and does NOT call `router.refresh()`.
37. `status` flips `idle → saving → saved` on success and `idle → saving → error` on failure.
38. Second call while `saving` is in flight is dropped (returns null without making a request).
39. Component unmount during in-flight call aborts via AbortController (no setState after unmount warning).

### LinkedTagsSection (`src/components/__tests__/linked-tags-section.test.tsx` — NEW)

40. Renders a chip for each tag where `tag.parent_episode_id === episode.id`.
41. Tags with a different parent_episode_id are NOT rendered.
42. Tags with `parent_episode_id: null` are NOT rendered.
43. Empty-state line `Nog geen gekoppelde tags.` renders when no tags are linked.
44. The `+ Tag` button calls `onOpenPicker` on tap.
45. Each chip has an `✕` unlink affordance with `aria-label` describing the action.
46. Tapping the `✕` calls the hook's `unlink(tag.id)` method.
47. Disabled state during `saving`: `+ Tag` button + all `✕` chips are disabled to prevent double-click bursts.

### TagPickerSheet (`src/components/__tests__/tag-picker-sheet.test.tsx` — NEW)

48. Renders a BottomSheet with title `Kies of maak een tag`.
49. Renders `+ Maak een nieuwe tag aan` CTA at top.
50. Renders all non-archived tags grouped by category, sticky h3 per category.
51. Tags already linked to THIS episode are NOT shown in the picker list.
52. Tags linked to a DIFFERENT episode are shown WITH a `(bij: <label>)` suffix.
53. Tap a tag row → calls `link(tag.id, episode.id)` and closes via `onPicked`.
54. Tap a tag already linked elsewhere → silent re-parent (link is called with the same args; no confirm dialog renders).
55. Tap `+ Maak een nieuwe tag aan` → inline mini-form (label input + category select) becomes visible.
56. Submit mini-form with valid label + category → calls `createWithParent({ label, category, parent_episode_id: episode.id })` and closes via `onPicked`.
57. Mini-form validation: empty label shows inline error and does NOT call the API.
58. Mini-form validation: label > 40 chars shows the too-long error.
59. Mini-form validation: category not selected → error (the select defaults to a placeholder requiring an explicit choice).
60. Server error surfaces in the top-of-sheet error banner.
61. Empty-corpus state (no eligible tags) → only the `+ Maak nieuwe tag aan` CTA + muted line `Nog geen andere tags. Maak er een aan.`.
62. Drag-down / Escape / close button each call `onClose` (BottomSheet primitive contract — light-touch verification).

### EpisodeFormSheet integration (`src/components/__tests__/episode-form-sheet.test.tsx` — extend)

63. In create mode, `LinkedTagsSection` does NOT render.
64. In edit mode, `LinkedTagsSection` renders BETWEEN the description field and the action row.
65. Tapping `+ Tag` inside LinkedTagsSection opens the nested TagPickerSheet.
66. Closing the picker (via `onClose` or `onPicked`) returns focus to the `+ Tag` button.
67. The picker is closed when the EpisodeFormSheet itself is closed (no orphan sheet).

### Cross-feature regression

68. ContextView test: passes `tags` prop through to EpisodeFormSheet.
69. TodayShell test: threads `tags` prop into ContextView.
70. QuickEntryFlow / TagCategoryList component tests stay green (AC-F8 — no daily-flow regression).
71. Copy snapshot lock (`src/__tests__/copy.test.ts`): updated assertion array for the new `tagLinking` + `tagPicker` keys.

### Smoke (`scripts/tags-smoke.mjs` — extend or new)

72. POST /api/tags with `parent_episode_id` set → tag has parent in DB.
73. PATCH /api/tags/[id] with `parent_episode_id` set → tag re-parented in DB.
74. PATCH /api/tags/[id] with `parent_episode_id: null` → tag unlinked in DB.
75. Cleanup: hard-delete the test tag + test episode via DIRECTUS_TOKEN.

---

## Build order (TDD shape — RED → GREEN → REFACTOR per phase)

Six phases. Each phase is its own RED-first cycle.

1. **Domain**: `validateParentEpisodeId`. Tests 1–7 RED, then implementation, then GREEN.
2. **API library**: extend `createOrUpsertTag` (tests 8–13), add `updateTag` (tests 14–19). RED, implement, GREEN.
3. **Route handlers**: extend POST /api/tags (tests 20–23), add PATCH /api/tags/[id] (tests 24–32). RED, implement, GREEN. Run the verify gate.
4. **Hook**: `useTagLinkUpsert` (tests 33–39). RED, implement, GREEN.
5. **Components**: LinkedTagsSection (tests 40–47), TagPickerSheet (tests 48–62). RED, implement, GREEN. Copy additions land here.
6. **Integration + regression + smoke**: EpisodeFormSheet integration (tests 63–67), regression checks (tests 68–71), smoke extension (tests 72–75). Verify gate, deploy, manual iOS PWA sanity (drag-down through two sheets, focus return).

Commit at each phase boundary. The verify gate (`npm run verify`) must be green before moving to the next phase.

---

## Out of scope (step-5)

- **Bulk linking** ("link the last 5 days' tags to this episode"). v1.5b.
- **Tag detail / Settings → Tag-beheer** path for setting parent_episode_id from the tag side. v1.5b.
- **Hard delete of linked tags**. Soft delete only, same as episodes.
- **Cascading on episode archive**. Tags retain `parent_episode_id` even when the episode is archived — README's resolved decision.
- **Optimistic UI**. Saving state surfaces in the picker; no shadow state.
- **Server-side validation of the parent_episode_id existing in the `episodes` table**. Directus FK constraint handles referential integrity; client surfaces the resulting Directus error as `directus_error` → 502 if a stale id is somehow sent.
- **Linking from the timeline-episode-overlay surface** (v1.5 sibling feature) — that's a v1.5b consideration.

---

## Notes carried back to README

After AC-F7 ticks: README's AC-F7 line gets `(Step-5, <commit>)`. The "Tag-to-episode linking" subsection of the UI shape section ("Linking happens in two places") stays accurate — path 1 (from episode detail) ships in step-5; path 2 (from the tag's detail in Settings → Tag-beheer) stays as the v1.5b note.
