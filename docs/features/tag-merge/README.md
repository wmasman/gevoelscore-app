# Tag merge

**Feature:** Combine two same-category tags into one. Inside `TagFormSheet`, a new "Samenvoegen met…" button opens a nested picker of other tags in the same category. Pick the target → confirm with affected-day count → server rewrites every `day_entries_tags` junction row that pointed at the source to point at the target (de-duplicating where the target was already on the same day) → hard-deletes the source. The result: a single canonical tag, with every day that ever had the source now having the target instead.
**Version:** v1.5c (deferred from v1.5b's `tag-management-settings` to ship after that surface had real soak signal).
**Status:** **Shipped 2026-06-03** (commits `36737f5..103ace6`). Deployed to prod; smoke 11/11 green; soak in progress on iPhone PWA.
**Steps (all shipped):**
- **[Step 0 — Junction + label integrity hardening](./step-0-junction-integrity.md)** (DB prerequisite, commits `36737f5..2228f63`). 4 UNIQUE indexes — composites on the two junction tables + partial case-insensitive `(LOWER(label), category) WHERE archived_at IS NULL` on `tags` + `episodes`. Introduced the `pg`-backed `runSqlFile` / `queryPg` helpers and the FK + UNIQUE assertions in `verify-schema.mjs`.
- **[Step 0b — Tier 3 CHECK constraints](./step-0b-check-constraints.md)** (defense-in-depth, commit `063b609`). 7 CHECK constraints: category enums on `tags` + `episodes`, score 1-10, sleep_hours 0-24, episode date order, confidence 0-1 on both junctions.
- **[Step 1 — Tag merge](./step-1-tag-merge.md)** (the feature itself, commits `8efb03b..35b9421`). `mergeTag` SDK + `POST /api/tags/[id]/merge` route + `useTagManage.merge` + `TagMergeTargetPickerSheet` + `TagFormSheet` integration.
**Parent docs:** [features/tag-management-settings/](../tag-management-settings/) (parent v1.5b that deferred this) · [features/inline-tag-creation/](../inline-tag-creation/) (creates the duplicate-tag pressure this resolves) · [features/tag-recency-sort/](../tag-recency-sort/) (the picker that benefits from a cleaner corpus)

---

## When does the user merge?

After tag-management-settings shipped, the user has rename / recategorize / archive / hard-delete. None of those handle the most common cleanup case: **"hoofdpijn" + "hoofdpijn licht" + "lichte hoofdpijn" should all be one tag**. Rename consolidates the label going forward but doesn't fix the historical data — the day_entries still have the old tag-ids attached. Hard-delete can't run because the duplicate has usage_count > 0.

Merge is the operation that closes the gap: it rewrites the historical references AND removes the duplicate in one transaction. After merge:
- Every `day_entry` that had `source` now has `target` instead (deduped if `target` was already there).
- `source` is gone (hard-deleted).
- `target`'s stored `usage_count` reflects the union.

## Resolved decisions (2026-06-03)

All three open design questions settled:

- **Cross-category targets**: **same-category only, hard block**. The picker lists ONLY tags in the source's category. Cross-category cleanup requires recategorizing first, which is a deliberate two-step rather than a one-tap footgun. Simpler rule, simpler tests.
- **Source fate after merge**: **hard-delete**. After the junction rewrite, the source has zero references; an archived ghost in the corpus would defeat the cleanup intent. Reversible only via export+restore, but that's true of every hard-delete in the app.
- **Confirmation flow**: **2-step** (pick → confirm-with-count). Tap target in the picker → confirm dialog with the affected-day count drawn from the source's `usage_count`. Single confirm dialog. The merge response carries the exact post-rewrite count for the success state.

## UI shape

### `TagFormSheet` — new "Samenvoegen met…" button

Appended to the action row in the existing `TagFormSheet`:

```
[ Bewaar ]
[ Archiveer / Activeer opnieuw ]
[ Verwijder ]                          (disabled when usage_count > 0)
[ Samenvoegen met… ]                   (disabled when no other same-cat tags)
```

The button is disabled when:
- No other non-archived tags share the source's category (no possible targets).
- A save / archive / delete is in flight.

### Nested picker — `TagMergeTargetPickerSheet`

Mirrors the `TagPickerSheet` pattern from step-5 of verloop-and-episodes (nested BottomSheet over the parent sheet). Renders a flat list (no category groups — every row shares the same category) of non-archived tags in the source's category, excluding self, sorted by recency desc (same `computeRecencyByTagId` used elsewhere).

Each row: label only. Tap → opens the confirm dialog.

### Confirm dialog (inline `role="alertdialog"`)

Inside the picker (one layer up from "inside the parent form" — closer to the user's action). Focus on `Annuleer`.

```
Tag "<source.label>" samenvoegen met "<target.label>"?

<source.usage_count> dagen waarop "<source.label>" voorkomt krijgen
"<target.label>". Daarna wordt "<source.label>" definitief verwijderd.

  [ Annuleer ]   [ Ja, samenvoegen ]
```

`Ja, samenvoegen` button uses `bg-accent-hover text-bg` (matching the logout-confirm + delete-confirm patterns — the destructive-action treatment).

## Data flow

```
POST /api/tags/[source_id]/merge
Body:   { target_tag_id: string }
200:    { source_id, target_id, affected_days }
400:    'invalid_id' | 'malformed_body' | 'invalid_target' | 'same_tag' | 'category_mismatch' | 'source_archived'
401/403/429:  standard auth stack
502:    'server_error' (source / target not found, or rewrite failed mid-way)
```

The route handles the whole transaction internally:

1. **Validate** via a **single combined read**: `readItems('tags', { filter: { id: { _in: [sourceId, targetId] } } })` returns both rows (or fewer, surfacing source_not_found / target_not_found). Both must be non-archived. source.id ≠ target.id and source.category === target.category.
2. **Read** all `day_entries_tags` rows where `tags_id = source`. Capture distinct `day_entries_id`s (sourceDays).
3. **Read** `day_entries_tags` rows where `tags_id = target AND day_entries_id IN <sourceDays>`. Build the set of "days that already have target" (overlapDays). Junction reads stay split because the target read is filtered by source days — combining would pull target's full junction set even when target ≫ source.
4. **Partition** source junction IDs by `day_entries_id ∈ overlapDays` → `overlapJunctionIds` + `nonOverlapJunctionIds`.
5. **Rewrite in two bulk ID-array operations, ordered**:
   - **Bulk DELETE** `overlapJunctionIds` from `day_entries_tags` (removes would-be duplicates).
   - **Bulk PATCH** `nonOverlapJunctionIds` setting `{ tags_id: target_id }`. The order matters: bulk PATCH first would collide on UNIQUE(`day_entries_id`, `tags_id`) for every overlap day and fail the whole batch.
6. **Recompute** target's `usage_count` from the actual post-rewrite junction count and PATCH the target tag row.
7. **Hard-delete** the source tag row (bypasses the usage_count gate — at this point source has zero references).
8. **Return** `{ source_id, target_id, affected_days: <count of distinct days touched> }`.

**Round-trip count per merge: 5** — one combined tag read + two junction reads + two bulk junction writes counts as 5 Directus round-trips, plus 1 PATCH (target.usage_count) + 1 DELETE (source). The count is constant w.r.t. source size up to ~hundreds of junctions; very large sources would need pagination on step 2.

The hard-delete in step 7 is direct via the Directus SDK (`deleteTag` from `tags.ts`) — not via the gated DELETE route — because the route's `usage_count > 0 → 400` gate would otherwise reject the call if the stored `usage_count` is stale.

## Transaction safety

Directus doesn't expose cross-collection ACID. Single-user single-device app means concurrent writes are functionally impossible. Order of operations is chosen so that any partial failure leaves a recoverable state:

| Step | Failure mode | Recovery |
|---|---|---|
| 1 (combined source/target tag read) | Network — no writes done | Retry safely. |
| 2 (read source junctions) | Network — no writes done | Retry safely. |
| 3 (read target junctions) | Network — no writes done | Retry safely. |
| 5a (bulk DELETE overlap junctions) | Bulk atomic; either all overlap junctions removed or none. If failed → source still has all junctions (incl. overlap); rerun merge. | Retry. The bulk DELETE is idempotent w.r.t. retry — second pass recomputes overlap from current state. |
| 5b (bulk PATCH non-overlap to target) | Bulk atomic; either all non-overlap moved or none. If failed AFTER 5a → overlap junctions gone, non-overlap still point at source; rerun merge. | Retry. Second pass: source junction count = original non-overlap; overlap set is empty (target already has those days); the patch moves remainder cleanly. |
| 6 (recount target.usage_count) | Failed after rewrite | `usage_count` drifts; cosmetic only. The `recountTagUsage` helper (see step-1 §Notes) is the future fix; a scheduled recount script could call it for any drifty tag (out of scope). |
| 7 (hard-delete source) | Failed after rewrite | Source has 0 references but still exists. Manual delete via Directus admin, OR the user retries merge (step 2 finds 0 junctions, route returns success with affected_days=0). |

TOCTOU note: same posture as step-5 of verloop-and-episodes + step v1.5b's hard-delete. Functionally impossible on a single-user single-device app.

## Out of scope (v1.5c — defer to later)

- **Cross-category merge**. Recategorize first.
- **Bulk merge** (select N source tags → merge into one target). v2.
- **3+ tag chain** in one operation. Run merge twice.
- **Undo / merge history**. The operation is irreversible; the design relies on the confirm dialog + the 2-step flow to prevent accidents.
- **Preview screen showing exact affected dates**. The count from `source.usage_count` is enough; if the stored value has drifted, the merge response surfaces the actual count post-facto.
- **Merging linked tags** with `parent_episode_id` set: works the same as unlinked; target wins (keeps its own `parent_episode_id`, source's is discarded). No special case needed.
- **Restoring usage_count drift** if step 6 fails partially: a scheduled recount script is the right fix; not blocking this feature.

## Cross-feature integrity

- **Daily flow UNCHANGED**. `TagCategoryList` + `QuickEntryFlow` see the merged target; the source is gone. No regression in the picker / today-card / timeline.
- **Episode-side linking UNCHANGED**. The `TagPickerSheet` in `EpisodeFormSheet` (step-5 of verloop-and-episodes) keeps working — it never references source ids that no longer exist.
- **Tag-management UNCHANGED**. Rename / recategorize / archive / hard-delete in `TagFormSheet` keep working on the surviving target.
- **`usage_count` consistency**: step 6 recomputes target's usage_count from the actual junction count. The pre-existing question of whether `usage_count` is accurate in steady-state (it's a stored column, not derived) is unchanged by this feature — the merge brings it back into alignment for the target.

## References

- [features/tag-management-settings/](../tag-management-settings/) — parent feature; this fills its v1.5c deferred slot.
- [features/inline-tag-creation/](../inline-tag-creation/) — the source of duplicate-tag pressure.
- [features/tag-recency-sort/](../tag-recency-sort/) — the picker that benefits from a cleaner corpus.
- [roadmap.md](../../roadmap.md) — v1.5c slot.

## History

- 2026-06-03: feature folder created; 3 design decisions resolved (same-category only hard block; hard-delete source; 2-step confirm). Step file follows.
