# Step 1: Tag-beheer in Settings (single step)

**Estimated time:** ~6 hours. Multi-component but tightly scoped — one new Settings section, one new BottomSheet component (`TagFormSheet`), one new API route (DELETE `/api/tags/[id]`), and extending PATCH `/api/tags/[id]` to accept three more keys.
**Test layers:** Vitest unit tests for the validators + the SDK wrapper extensions (`updateTag` patch surface, new `deleteTag`). Vitest route tests for PATCH (extended keys + the new fields) and DELETE (usage_count gate + standard auth stack). Vitest component tests for `TagFormSheet` + the new `TagManagementSection` in `SettingsView`. Existing tests stay green.
**Risk:** Low-medium. The hard-delete path is the only genuinely-new wire-level destructive operation in the app to date; needs careful auth + usage_count gating. The other operations reuse the patterns step-5 already established. UI surface is contained to Settings — no risk of regressing the daily flow.
**Prerequisite:** v1.5 anchor + timeline overlay + today-card region all shipped (commits up to `460bfe2`). No schema work needed.

> Step-1 ships the v1.5b administrative cleanup surface. Five actions on existing tags (rename · recategorize · archive · un-archive · re-parent) plus a sixth, gated action (hard-delete when usage_count === 0). All driven by a new `TagFormSheet` BottomSheet that opens on tap-into-row inside the new Settings → Tag-beheer section. Merge + bulk-select + search are explicitly out of scope, queued for v1.5c.

---

## Resolved decisions (2026-06-03)

All locked before drafting:

- **List shape**: **A — label + category only** in the list. Drill-down for everything else. Linked tags show a small right-aligned `→ <episode label>` suffix on the row as the only extra signal.
- **Per-row tap behaviour**: **whole row taps to open the BottomSheet** (same pattern as Context tab list items + Tijdlijn band-taps + today-card ongoing rows). No inline edit affordances.
- **Hard-delete UX**: **behind a confirm dialog** inside the BottomSheet. Focus lands on `Annuleer` on appear (matches `settings-view.tsx` logout-confirm).
- **Merge**: **deferred to v1.5c**. Atomic-transaction-across-day_entries scope is too large for this step.
- **Bulk select-mode**: **deferred**. Per-item is verbose but predictable; bulk earns its keep only after real usage proves the friction.
- **Search / filter**: **deferred**. Grouped + recency-sorted list is scannable at the current ~100-tag corpus.

---

## Acceptance criteria

### Domain layer — prerequisite extraction (M3 audit fix)

- [x] **AC0: Extract the ISO UTC timestamp validator to a shared helper** at `src/lib/domain/iso-timestamp.ts`. The regex `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$` plus a `new Date(value)` round-trip check currently lives inlined in [`tag.ts:50`](../../../src/lib/domain/tag.ts#L50) and [`day-entry.ts`](../../../src/lib/domain/day-entry.ts); `updateEpisode` does the same check inlined too. Export `validateIsoUtcTimestamp(input: unknown): Result<string, 'invalid_iso_timestamp'>`. **Refactor-while-green**: replace the two existing inline copies in `tag.ts` + `day-entry.ts` with the helper; verify gate stays green via existing tests in those domains. Episode-side and the new `updateTag` then both reuse it.

### API library

- [x] **AC1: `updateTag`'s `UpdateTagPatch` shape expands** from the single `parent_episode_id` key to also accept `label?: string`, `category?: TagCategory`, `archived_at?: string | null`. All keys optional; empty patch returns `'invalid_patch'` (existing rule preserved).
- [x] **AC2: `updateTag` validates each key it sees with PER-FIELD error variants** (M1 audit fix — mirrors the `updateEpisode` pattern). `UpdateTagError` becomes `'invalid_patch' | 'invalid_label' | 'invalid_category' | 'invalid_archived_at' | 'invalid_parent_episode_id' | 'network_error' | 'directus_error'`. `label` runs through `validateTagLabel` → maps `'invalid_tag_label'` to `'invalid_label'`. `category` runs through `validateTagCategory` → maps to `'invalid_category'`. `archived_at` accepts `null` directly, otherwise runs through `validateIsoUtcTimestamp` (from AC0) → maps to `'invalid_archived_at'`. The `'invalid_patch'` variant is reserved for shape-level violations (empty patch, unknown key, non-object body). Each variant maps to a 400 with the same error code in the route, so the form + future API consumers can tell the user which field failed.
- [x] **AC3: A new `deleteTag(accessToken, id): Promise<Result<{ deleted_id: string }, ...>>`** lives in [`src/lib/api/tags.ts`](../../../src/lib/api/tags.ts). It does NOT itself check usage_count — that gate lives in the route handler (read-then-delete with a transaction-style guard). On success, returns `{ deleted_id: id }`. On Directus failure (network / server), the existing `network_error` / `directus_error` variants apply.

### Route handlers

- [x] **AC4: PATCH `/api/tags/[id]` accepts the four allowed keys** + maps per-field errors. Allowed keys: `parent_episode_id`, `label`, `category`, `archived_at`. Any other key in the body → 400 `invalid_patch` (existing gate). Per-field validation failures from `updateTag` (`'invalid_label'` / `'invalid_category'` / `'invalid_archived_at'` / `'invalid_parent_episode_id'`) each map to 400 with the same error code in the response body — UI can show the user which field is wrong.
- [x] **AC5: A new DELETE `/api/tags/[id]` route** lives at [`src/app/api/tags/[id]/route.ts`](../../../src/app/api/tags/[id]/route.ts). Standard auth stack (origin → session → rate-limit (`tagWriteRateLimiter`, budget raised in AC5b) → UUID-format gate on `id`). On success returns 200 `{ deleted_id: id }`. Body is empty (no payload needed for DELETE). **404 behaviour** (M5 audit fix): a well-formed UUID that doesn't match any tag in Directus surfaces as `directus_error` from the lib and maps to 502 `{ error: 'server_error' }` in the route — consistent with the PATCH non-existent-UUID path (test 32 of step-5). No 404 variant; the picker shouldn't surface non-existent ids in normal flow.
- [x] **AC5b: Raise `tagWriteRateLimiter` budget from 60 → 200 writes per 5 minutes** (M4 audit fix). The original 60/5min was sized for daily-flow inline-create + occasional re-link, not for a bulk cleanup session that might edit 30-60 tags in 3 minutes. 200/5min stays anti-abuse-shaped (a real human can't legitimately exceed this on a mobile keyboard) while comfortably absorbing a real cleanup pass. Single value, applies to POST + PATCH + DELETE — keeps the budget unified.
- [x] **AC6: DELETE is gated by usage_count === 0**. The route reads the tag first (via a targeted Directus fetch); if `usage_count > 0` returns 400 `{ error: 'tag_in_use', usage_count }`. Only when usage_count is 0 does the Directus DELETE fire. TOCTOU note: same single-user app assumption as step-5's TOCTOU note — functionally impossible for a logged tag to become "in use" between the read and the delete.

### Hook + state

- [x] **AC7: A new `useTagManage()` hook** lives at [`src/hooks/use-tag-manage.ts`](../../../src/hooks/use-tag-manage.ts), mirroring the shape of `useTagLinkUpsert`. Four methods, all return `Promise<Tag | null>` (or `null` for delete) and trigger `router.refresh()` on success:
  - `rename(tagId, label)` → PATCH with `{ label }`.
  - `recategorize(tagId, category)` → PATCH with `{ category }`.
  - `setArchived(tagId, archived_at)` → PATCH with `{ archived_at }` (null to un-archive, ISO timestamp to archive).
  - `reparent(tagId, parent_episode_id)` → PATCH with `{ parent_episode_id }`. (Reuses the same route as `useTagLinkUpsert.link` / `.unlink`.)
  - `hardDelete(tagId)` → DELETE /api/tags/[id]. Returns `null` on success (no tag to return; row gone).
  - The hook also exports a combined `save(tagId, patch)` that runs ONE PATCH with all changed fields in a single round-trip — used by `TagFormSheet`'s Bewaar button.

### Components

- [x] **AC8: A new `TagFormSheet` component** at [`src/components/tag-form-sheet.tsx`](../../../src/components/tag-form-sheet.tsx). Mirrors `EpisodeFormSheet` shape:
  - Props: `{ tag: Tag | null, episodes: Episode[], open: boolean, onClose, onSaved, onDeleted }`.
  - Internal state: form fields seeded from `tag` on the closed→open edge (same `prevOpenRef` pattern as `EpisodeFormSheet`).
  - Fields: Naam (text), Categorie (radio / select of 8 categories), Behoort bij (select: `Geen` + non-archived episodes), Status (read-only `n keer gebruikt, laatst {dutchDate}`).
  - Action row: `Bewaar` (primary), `Archiveer` OR `Activeer opnieuw` (state-dependent), `Verwijder` (only enabled when `tag.usage_count === 0`).
  - Server-error banner at the top (reused from existing components).
- [x] **AC9: `Verwijder` opens an inline confirm alertdialog INSIDE the TagFormSheet** (not a nested BottomSheet — saves a layer). Prompt: `Tag "{label}" definitief verwijderen? Deze actie kan niet ongedaan gemaakt worden.` Buttons: `Annuleer` (default focus) + `Ja, verwijder`. Annuleer returns to the form; Ja, verwijder fires `hardDelete` and closes the sheet on success.
- [x] **AC10: TagFormSheet validates client-side BEFORE submit**: label runs through `validateTagLabel`, category gate is trivial (always one of the 8), parent_episode_id is a valid UUID or null (validateParentEpisodeId). On invalid, surface the same `role="alert"` per-field error pattern as `EpisodeFormSheet`. Submit is disabled while saving.

### Settings view extension

- [x] **AC11: A new `TagManagementSection` component** renders inside `SettingsView` between the Account section and the Data section. Header `<h2>{copy.settings.tagManagementHeading}</h2>`.
- [x] **AC12: The section renders the tag list grouped by category**, in the canonical `TAG_CATEGORIES` order. Within each category, tags are sorted by **last-used desc** (using the same `computeRecencyByTagId` helper that powers the daily picker, derived from the most recent 90 days of `day_entries`). Tags with no recency record sink to the bottom of their group.
- [x] **AC13: A `Toon gearchiveerd` checkbox** above the list toggles archived-tag visibility. Default OFF (archived tags hidden). When ON, archived tags render with reduced opacity + a small `(gearchiveerd)` suffix in their category group.
- [x] **AC14: Each row is a button** that opens TagFormSheet with that tag. aria-label format: `{label}, {category-dutch}, tik om te bewerken` (with the dutch category label — same one used in `TagPickerSheet`'s `CATEGORY_LABEL` map).
- [x] **AC15: Linked-tag rows show a right-aligned `→ {episode label}` suffix**. Compact, single-line; if the episode label is long it truncates at ~20 chars with `…` ellipsis. The full label is in the aria-label so screen readers get it.
- [x] **AC16: Empty corpus state**: if there are no non-archived tags, render `Geen tags. Tags maak je in het Vandaag-scherm.` as a muted paragraph. (Brainfog-friendly: tells the user where the action is.)

### Settings page data

- [x] **AC17: `src/app/settings/page.tsx` extends its existing server function to fetch the data the new section needs** (M2 audit fix). The page-level server component already runs the two-tier auth gate; extend it to also `Promise.all` three reads (`readAllTags`, `readAllEpisodes`, `readDayEntriesInRange` over the last 90 days for recency derivation). Pass the three arrays as props to the existing `SettingsView`, which stays a **client component** (its existing `useState` + `useRouter` for logout is unchanged). No `SettingsViewClient` rename, no server-component shim — same pattern as `page.tsx → TodayShell`.
- [x] **AC18: All three reads happen in parallel** via `Promise.all` in `settings/page.tsx`. Read failures fall back to empty arrays (the section degrades to the empty-corpus state). The existing auth gate runs BEFORE the parallel reads (no point fetching for an unauthenticated request).

### Cross-feature integrity

- [x] **AC19: Daily flow stays UNCHANGED**. `TagCategoryList` + `QuickEntryFlow` tests stay green. Recency sort still applies. Inline-create still posts via POST `/api/tags`.
- [x] **AC20: Episode-side `TagPickerSheet` stays UNCHANGED**. Its create-with-parent + silent-re-parent paths are unaffected; the tag-side re-parent in Settings is an additional path, not a replacement.
- [x] **AC21: Renaming a tag propagates everywhere via id-reference**. Verified: no `day_entries.tag_ids[]` rewrite needed (references are by id). The next render of the daily picker, the today-card linked-tag chips, and the timeline linked-tag dots all pick up the new label.

---

## Technical constraints

- **No schema changes.** All fields exist. The DELETE route is the only new wire endpoint.
- **No Zod.** Domain validators continue to own per-field validation (`validateTagLabel`, `validateTagCategory`, `validateParentEpisodeId`, the new shared `validateIsoUtcTimestamp` from AC0). Per-field error variants surface to the UI (M1 fix).
- **`router.refresh()` is the only invalidation primitive.** Same pattern as every other mutation in the app.
- **Single-PATCH for the Bewaar button.** When the user changes label + category + parent in one form session, the form computes the diff against `initialTag` and sends ONE PATCH with the changed keys. Avoids three round-trips for a single user action.
- **Hard-delete confirm focus management.** The confirm `alertdialog` traps focus on the `Annuleer` button on appear; Escape returns to the form (matches `settings-view.tsx` logout-confirm rules).
- **Rate-limit unified at 200 writes / 5min** (M4 fix). `tagWriteRateLimiter` covers POST + PATCH + DELETE; the raised budget absorbs a real cleanup pass without rate-limiting a legitimate user.
- **DELETE method needs origin check.** `validateOrigin` already covers PATCH; the same call applies to DELETE.
- **TOCTOU on hard-delete.** Read usage_count → check === 0 → DELETE. Single-user single-device app makes the race functionally impossible (same posture as step-5's documentation). The DB-level fix (a transaction with row lock) is tracked as a "if we ever go multi-user" item.
- **Recency derivation in SettingsView.** Reuses `computeRecencyByTagId` from [`src/lib/domain/tag-sort.ts`](../../../src/lib/domain/tag-sort.ts). 90-day window matches what `TimelineView` already fetches at the 90d range.
- **Linked-episode label lookup in the row**. Index `episodes` by id once, look up O(1) per row. Same pattern as `TagPickerSheet`'s `episodeLabelById` map.
- **Archived-tag rendering**. `archived_at !== null` → opacity 60% + `(gearchiveerd)` suffix. Don't hide the row — the toggle gates visibility.

---

## Test plan

### Domain helper — AC0 prerequisite (`src/lib/domain/__tests__/iso-timestamp.test.ts` — NEW)

A. `validateIsoUtcTimestamp` returns ok for `'2026-06-03T10:00:00.000Z'`.
B. Returns ok for `'2026-06-03T10:00:00Z'` (no milliseconds, still ISO UTC).
C. Returns `'invalid_iso_timestamp'` for empty string.
D. Returns `'invalid_iso_timestamp'` for non-string input (null, number, object).
E. Returns `'invalid_iso_timestamp'` for malformed string (`'yesterday'`, `'2026-06-03'`, `'2026-06-03T10:00:00+02:00'`).
F. Returns `'invalid_iso_timestamp'` for syntactically-valid-but-impossible date (`'2026-13-99T00:00:00Z'`).
G. Regression: existing `tag.ts` validateTag tests stay green after the inline regex is replaced by the helper.
H. Regression: existing `day-entry.ts` validateDayEntry tests stay green after the same replacement.

### API library (`src/lib/api/__tests__/tags.test.ts` — EXTEND)

1. `updateTag` with valid `{ label: 'pacing-strategy' }` → 200 with updated tag, PATCH wire body contains only `label`.
2. `updateTag` with valid `{ category: 'fysiek' }` → 200 with updated tag.
3. `updateTag` with valid `{ archived_at: '2026-06-03T10:00:00.000Z' }` → 200 with archived tag.
4. `updateTag` with valid `{ archived_at: null }` → 200 with un-archived tag.
5. `updateTag` combining label + category + parent in one patch → 200 with all three applied; one wire call.
6. `updateTag` with empty label string → `'invalid_label'` BEFORE wire (M1: per-field variant).
7. `updateTag` with too-long label (>40 chars) → `'invalid_label'` BEFORE wire.
8. `updateTag` with too-many-words label → `'invalid_label'` BEFORE wire.
9. `updateTag` with non-enum category → `'invalid_category'` BEFORE wire (M1).
10. `updateTag` with malformed archived_at (not ISO) → `'invalid_archived_at'` BEFORE wire (M1).
11. `updateTag` with malformed parent_episode_id (non-UUID) → `'invalid_parent_episode_id'` BEFORE wire (M1).
12. `updateTag` with unknown key → `'invalid_patch'` BEFORE wire (shape-level — variant preserved).
13. `updateTag` with empty patch → `'invalid_patch'` BEFORE wire (shape-level).
14. `updateTag` regression: existing `parent_episode_id`-only patches still work.
15. `deleteTag` happy path → 200 with `{ deleted_id: id }`.
16. `deleteTag` network failure → `network_error`.
17. `deleteTag` directus error → `directus_error`.

### Route handler — extended PATCH (`src/app/api/tags/[id]/__tests__/route.test.ts` — EXTEND)

18. PATCH with `{ label: 'pacing' }` → 200 with updated tag.
19. PATCH with `{ category: 'fysiek' }` → 200.
20. PATCH with `{ archived_at: '2026-06-03T...Z' }` → 200.
21. PATCH with `{ archived_at: null }` → 200.
22. PATCH with `{ label, category, parent_episode_id }` in one body → 200.
23. PATCH with unknown key `{ foo: 'bar' }` → 400 `{ error: 'invalid_patch' }` (regression).
24. PATCH with malformed label → 400 `{ error: 'invalid_label' }` (M1: per-field response).
25. PATCH with non-enum category → 400 `{ error: 'invalid_category' }` (M1).
26. PATCH with malformed archived_at → 400 `{ error: 'invalid_archived_at' }` (M1).

### Route handler — new DELETE (`src/app/api/tags/[id]/__tests__/route.test.ts` — EXTEND)

27. DELETE happy path (usage_count === 0) → 200 with `{ deleted_id }`.
28. DELETE with usage_count > 0 → 400 `{ error: 'tag_in_use', usage_count: N }`. Directus DELETE is NOT called.
29. DELETE with non-UUID id → 400 `invalid_id`.
30. DELETE without session cookie → 401.
31. DELETE from disallowed origin → 403.
32. DELETE rate-limited at the new 200/5min budget → 429 (verify the higher cap works).
33. DELETE with non-existent tag id (UUID format ok but no row in Directus) → 502 `{ error: 'server_error' }` (M5: matches PATCH non-existent-UUID behaviour).

### Hook (`src/hooks/__tests__/use-tag-manage.test.ts` — NEW)

34. `rename` PATCHes with `{ label }` and calls router.refresh.
35. `recategorize` PATCHes with `{ category }` and calls router.refresh.
36. `setArchived` with ISO timestamp PATCHes archive_at.
37. `setArchived` with null PATCHes archived_at=null (un-archive).
38. `reparent` PATCHes parent_episode_id.
39. `hardDelete` calls DELETE /api/tags/[id] and triggers router.refresh on success.
40. `save({ label, category, parent_episode_id })` makes ONE PATCH with all three keys (not three).
41. Failed mutation surfaces `lastError` with the per-field error code (M1) and does NOT call router.refresh.
42. AbortController supersede semantics (rapid back-to-back calls).

### TagFormSheet (`src/components/__tests__/tag-form-sheet.test.tsx` — NEW)

43. Renders title `Tag bewerken` + Naam + Categorie + Behoort bij + Status block.
44. Seeds form fields from `tag` prop on open.
45. Save button is disabled when no field differs from `initialTag`.
46. Save calls `hook.save` with ONLY the diff.
47. Archive button toggles between `Archiveer` and `Activeer opnieuw` based on `tag.archived_at`.
48. Hard-delete button is DISABLED when `usage_count > 0`.
49. Hard-delete button is ENABLED when `usage_count === 0`.
50. Tapping enabled Verwijder opens the inline confirm alertdialog.
51. Confirm's default focus is on `Annuleer`.
52. Tapping `Annuleer` returns to the form (alertdialog gone, form intact).
53. Tapping `Ja, verwijder` calls `hook.hardDelete` and fires `onDeleted` on success.
54. Server-side per-field error (e.g. `invalid_label`) surfaces in the top-of-sheet banner with field-specific copy (M1 fix's UX dividend).
55. Behoort bij dropdown lists `Geen` + every non-archived episode label.
56. Selecting `Geen` from a previously-linked tag clears `parent_episode_id` on save.
57. Status block renders `n keer gebruikt, laatst {dutchDate}` for a usage_count > 0 tag.
58. Status block renders `Nog niet gebruikt` for a usage_count === 0 tag.

### TagManagementSection (`src/components/__tests__/tag-management-section.test.tsx` — NEW)

59. Renders `<h2>` with the configured Tag-beheer copy.
60. Groups tags by category in the canonical order.
61. Within a category, tags are sorted by last-used desc.
62. A tag never used sinks to the bottom of its category.
63. The `Toon gearchiveerd` checkbox defaults to unchecked.
64. With the toggle OFF, archived tags are NOT rendered.
65. With the toggle ON, archived tags render with the `(gearchiveerd)` suffix.
66. Each row is a button with the documented aria-label.
67. Tapping a row opens TagFormSheet for that tag.
68. Linked-tag rows show the `→ {episodeLabel}` suffix.
69. Long episode-label truncation: a 30-char episode label renders truncated; aria-label has full text.
70. Empty corpus → `Geen tags. Tags maak je in het Vandaag-scherm.` muted line; no list rendered.

### SettingsView wiring (`src/components/__tests__/settings-view.test.tsx` — EXTEND)

71. Renders the new TagManagementSection between Account and Data.
72. Existing logout + binnenkort tests stay green.

### Regression suite

73. Daily-flow `TagCategoryList` tests stay green (AC19).
74. Episode-side `TagPickerSheet` tests stay green (AC20).
75. Existing PATCH `parent_episode_id` smoke (in `episodes-smoke.mjs` 8a-8d) stays green even at the new 200/5min rate limit.

### Smoke (`scripts/tag-management-smoke.mjs` — NEW + run-tag-management-smoke.ps1 wrapper)

76. Login → create test tag → PATCH rename → confirm via Directus read.
77. PATCH recategorize → confirm via Directus.
78. PATCH archive → confirm row archived_at set.
79. PATCH un-archive → confirm cleared.
80. PATCH reparent → confirm parent set.
81. DELETE on usage_count === 0 tag → confirm row gone.
82. DELETE on usage_count > 0 tag (use a tag that's actually attached to a day_entry) → 400 `tag_in_use`; row still present.
83. DELETE on a non-existent UUID → 502 `server_error` (M5 boundary verification on the live wire).

---

## Build order (TDD shape — RED → GREEN → REFACTOR per phase)

Six phases (was five — added the AC0 prerequisite extraction). Verify gate green at each phase boundary.

1. **Domain helper extraction (AC0)**: write `iso-timestamp.ts` + tests A–F. RED, implement, GREEN. Then **refactor while green** — replace the inline regex in `tag.ts` + `day-entry.ts`; verify tests G + H stay green. Single small commit.
2. **API library**: extend `updateTag` patch surface with per-field error variants (tests 1–14); add `deleteTag` (tests 15–17). RED, implement, GREEN. Also raise `tagWriteRateLimiter` budget from 60 → 200 in `src/lib/auth/stores.ts` (AC5b — tested at the route layer in Phase 2).
3. **Route handlers**: extend PATCH allowed keys + per-field error mapping (tests 18–26); add DELETE (tests 27–33). RED, implement, GREEN.
4. **Hook**: `useTagManage` (tests 34–42). RED, implement, GREEN.
5. **Components**: `TagFormSheet` (tests 43–58) + `TagManagementSection` (tests 59–70). RED, implement, GREEN. Copy additions land here.
6. **`settings/page.tsx` data fetch + regression + smoke** (tests 71–83). Verify gate green; commit + push + deploy; production smoke.

Commit at each phase boundary.

---

## Out of scope (v1.5b — see also README §Out of scope)

- **Merge tags** (combine two tags into one with day_entries rewrite). v1.5c.
- **Bulk select-mode**. v1.5c if real cleanup-pass usage warrants.
- **Search / filter by substring**. Add if real usage shows the list grows past ~200 OR scanning friction is reported.
- **Per-tag usage chart / heatmap** (visualising when a tag was used over time). v2 — adjacent to the tag-intelligence vision.
- **Tag-creation from this surface**. Tag-creation stays in the daily flow (inline `+ nieuw` chip) and the episode-side `TagPickerSheet` (create-with-parent). Settings is for *existing* tags only.
- **Audit log / undo for tag changes**. The data layer preserves history via id-reference (rename propagates, archive is reversible), but a per-tag activity timeline is v2.

---

## Notes for the next feature

What v1.5c / next features need to remember:

- The `TagFormSheet` is reusable. If v1.5c adds "merge", the merge UX likely starts inside this sheet (`Samenvoegen met…` button) — pre-builds the affordance home.
- The DELETE route's usage_count gate is the only logical-FK enforcement against `day_entries.tag_ids[]` in the app. If/when merge ships, the same gate concept applies in reverse (must rewrite all references before/while deleting the source).
- `TagManagementSection` is a section, not a page. If the corpus genuinely grows past where a single-screen list is comfortable, a dedicated `/settings/tags` route can wrap the same section component without rewriting the surface.
