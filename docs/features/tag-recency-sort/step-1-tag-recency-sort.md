# Step 1: Tag recency sort within category

**Estimated time:** ~2 hours
**Test layers:** Vitest unit for the new comparator + recency-deriver in `src/lib/domain/tag-sort.ts`; Vitest component tests extending `tag-category-list.test.tsx` to assert sort order; no e2e change.
**Risk:** Low. Pure sort layered on top of the existing chip render. No data-model change. No API change. Falls back to alphabetical when recency data is absent.
**Prerequisite:** None. Builds on existing `readAllTags`, the `timelineEntries` prop already passed to TodayShell and TimelineView, and the QuickEntryFlow → TagCategoryList prop chain.

> Sort chips inside each expanded category by recency-then-frequency-then-alphabetical instead of pure-alphabetical. Recency signal is derived from the last-30-days `day_entries` already fetched in `page.tsx` — no new query, no schema change. Tags with no recency record fall back to frequency + alphabetical via the comparator. No new UI element; the cross-category "recent strip" alternative was rejected in the 2026-06-02 brainstorm.

---

## Acceptance criteria

- [ ] **AC1: In each expanded category, chips render in this order**:
  1. Tags with a recent-usage record, ordered by `last_used_at` DESC (most recent first).
  2. Within the same `last_used_at` date: `usage_count` DESC.
  3. Tags with no recent-usage record (last used >30 days ago or never): same fallback rules — `usage_count` DESC, then alphabetical ASC.
- [ ] **AC2: Category headers + their order are unchanged.** The 4 primary + Extra-opties + 4 extra categories still render in the same positions. Only chip order INSIDE each expanded category shifts.
- [ ] **AC3: Recency derived from the 30-day timeline window** (`timelineEntries` already on TodayShell / TimelineView via [page.tsx](../../../src/app/page.tsx)). For each tag-id, `last_used_at` = the most recent `day_entries.date` whose `tag_ids` array contains that id. Tags absent from any tag_ids array within the window get no recency entry → sink to the no-recency bucket.
- [ ] **AC4: Score-only path is unaffected.** No new computation runs when the user just taps a score and dismisses the popout without expanding a category. The sort is computed inside `byCategory` (which already only runs when the component renders chip rows), and `useMemo` keys on `[allTags, locallyAddedTags, recencyByTagId]` so the deps shift only when something genuinely changes.
- [ ] **AC5: No new UI affordance.** No "recent" badge on chips, no "voor jou" section, no separate strip. Just a reorder. Restrained per the design brief.
- [ ] **AC6: Newly created tags appear at the front of their category.** A tag just minted via inline-tag-creation has no `last_used_at` in the prop yet (the prop is server-derived; the router.refresh fires async). For the optimistic local-add path, treat the newly-added tag as "just used now" so it appears first. Simplest: prepend it visually to its category before re-sort kicks in. Acceptable since `setLocallyAddedTags` already segregates them.
- [ ] **AC7: Inline-tag-creation regression**: the existing `scrollIntoView + focus` behaviour for new chips still works. AC6 means the new chip is at position 1 of its category, so scroll-into-view brings the category top into view (which is where the chip lands).
- [ ] **AC8: Default-empty path**: when `recencyByTagId` is `{}` (e.g. in tests, fresh install, or when `timelineEntries` is empty), the existing alphabetical-within-category ordering holds. Existing tests keep passing.
- [ ] **AC9: Heatmap + line-chart unaffected.** Recency sort only touches the daily-flow chip picker. Tijdlijn rendering paths untouched.
- [ ] **AC10: Verify gate green.** `npm run verify` clean. No new lint disables.

---

## Technical constraints

- **No new dependency, no new API route, no schema change.** Recency derived in-app from data already fetched.
- **30-day recency horizon is the deliberate limit.** Tags used 31+ days ago are bucketed together as "no recent record" and tiebroken on usage_count + alphabetical. Wider window would require a separate fetch and is deferred to a future iteration.
- **Server→client serialisation**: `recencyByTagId` is a plain `Record<string, string>` (tag-id → ISO date string), JSON-safe across the page.tsx → TodayShell boundary. NOT a `Map` (not serialisable across server-component → client-component without conversion).
- **Computed once per render path**: TodayShell and TimelineView each compute recency via `useMemo` on `timelineEntries`. Two compute sites, identical helper — keep the cost trivial (30 entries × ~10 tag_ids = 300 ops).
- **Helper location**: `src/lib/domain/tag-sort.ts` (new) — testable in isolation, reusable by the future Settings tag-management UI.
- **The comparator and the deriver are pure functions** — no IO, no React, no side effects. Easy to unit-test exhaustively.

---

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | No | No new route. |
| New collection storing user data | GDPR Art 9 | No | No data. |
| New dependency | ADR | No | Pure derivation in existing modules. |
| New env var | A02 | No | — |
| Reduced motion / animation | WCAG 2.3.3 | No | No motion added; chips just render in a different order. |
| Aria labelling | WCAG 1.1.1 | No change | Chip aria-pressed semantics unchanged. The order shift is purely visual + reading-order for screen readers. |
| Forbidden UI patterns | brief.md | No | No new affordance; restraint principle upheld. |

---

## Plan

### 1.0 New helper module `src/lib/domain/tag-sort.ts`

Two pure functions + a constant for the comparator's recency horizon (kept as docs-clarifier, not a runtime cutoff since the deriver already only sees the window):

```ts
// src/lib/domain/tag-sort.ts
import type { DayEntry } from './day-entry';
import type { Tag } from './tag';

/**
 * Derive last-used-at per tag-id from a window of day_entries.
 *
 * Returns a record mapping tag-id to the most recent ISO date string
 * (YYYY-MM-DD) where that tag was attached. Tags not present in any
 * day_entry within the window get NO entry — callers should treat
 * absence as "no recent usage record" (lowest rank in the picker).
 *
 * Pure: same input → same output. Does not mutate inputs.
 */
export function computeRecencyByTagId(entries: DayEntry[]): Record<string, string> {
  const out: Record<string, string> = {};
  for (const e of entries) {
    for (const id of e.tag_ids) {
      const prev = out[id];
      if (prev === undefined || e.date > prev) {
        out[id] = e.date;
      }
    }
  }
  return out;
}

/**
 * Comparator for sorting tags within a single category in the daily
 * picker. Order: recent-first DESC by date, then usage_count DESC, then
 * alphabetical ASC by label.
 *
 * Tags with no entry in `recency` (i.e. not used in the last 30 days)
 * sink below ALL recent-usage tags, then sort among themselves by
 * usage_count + alphabetical.
 */
export function compareTagsForPicker(
  a: Tag,
  b: Tag,
  recency: Record<string, string>,
): number {
  const aLast = recency[a.id];
  const bLast = recency[b.id];
  // 1. Bucket: has-recency before no-recency.
  if (aLast !== undefined && bLast === undefined) return -1;
  if (aLast === undefined && bLast !== undefined) return 1;
  // 2. Within the same bucket: more-recent DESC.
  if (aLast !== undefined && bLast !== undefined && aLast !== bLast) {
    return aLast > bLast ? -1 : 1;
  }
  // 3. Tiebreaker: usage_count DESC.
  if (a.usage_count !== b.usage_count) return b.usage_count - a.usage_count;
  // 4. Final tiebreaker: alphabetical ASC, case-insensitive.
  return a.label.toLowerCase().localeCompare(b.label.toLowerCase());
}
```

### 1.1 Extend `TagCategoryList` to accept `recencyByTagId`

Add an optional prop, default `{}`. Apply the comparator in the `byCategory` memo:

```ts
type Props = {
  date: string;
  allTags: Tag[];
  initialTagIds: string[];
  disabled: boolean;
  recencyByTagId?: Record<string, string>;  // new, optional
};

export function TagCategoryList({ ..., recencyByTagId = {} }: Props) {
  // ... existing code ...
  const byCategory = useMemo(() => {
    const map = new Map<TagCategory, Tag[]>();
    for (const c of [...PRIMARY_CATEGORIES, ...EXTRA_CATEGORIES]) map.set(c, []);
    for (const t of effectiveTags) {
      if (t.archived_at !== null) continue;
      map.get(t.category)?.push(t);
    }
    // Sort each category in place using the picker comparator.
    for (const c of map.keys()) {
      map.get(c)!.sort((a, b) => compareTagsForPicker(a, b, recencyByTagId));
    }
    return map;
  }, [effectiveTags, recencyByTagId]);
  // ... rest unchanged ...
}
```

For AC6 (just-created tags first), the existing `locallyAddedTags` already segregates fresh tags. The merge order in `effectiveTags` puts `allTags` first, then `locallyAddedTags`. After my sort, both blocks reorder by recency. But a freshly-minted tag has no recency record — it'd sink. To fix: synthetically inject a "now" recency entry for newly-added tag-ids.

**Implementation choice**: when computing `recencyByTagId` for the picker, merge in any `locallyAddedTags` ids with `last_used_at = today`. Simplest place: a small `useMemo` inside TagCategoryList:

```ts
const effectiveRecency = useMemo(() => {
  if (locallyAddedTags.length === 0) return recencyByTagId;
  const merged = { ...recencyByTagId };
  for (const t of locallyAddedTags) merged[t.id] = date;  // synthetic "used today"
  return merged;
}, [recencyByTagId, locallyAddedTags, date]);
```

…and pass `effectiveRecency` into the comparator instead of the raw prop.

### 1.2 Thread `recencyByTagId` through `QuickEntryFlow`

QuickEntryFlow already takes `allTags: Tag[]`. Add an optional `recencyByTagId?: Record<string, string>` prop and pass it through to `<TagCategoryList recencyByTagId={...} />`. Default `{}`.

### 1.3 Derive + pass from `TodayShell` and `TimelineView`

In each component:
```ts
const recencyByTagId = useMemo(
  () => computeRecencyByTagId(timelineEntries),  // or `initialEntries` / `entries`
  [timelineEntries],
);
```
…and pass to every `<QuickEntryFlow recencyByTagId={recencyByTagId} ... />` instance. Both TodayShell and TimelineView render QuickEntryFlow; both need the prop wired.

For TimelineView specifically: derive from `entries` (the 30d or 90d window currently selected). When the user toggles to 90d, recency gains a 60-day window — slight behaviour change but acceptable for the past-day-edit flow.

### 1.4 No copy changes

No new strings in `src/copy.ts`.

---

## Test list (RED-first)

### Unit: `src/lib/domain/__tests__/tag-sort.test.ts` (new)

**For `computeRecencyByTagId`:**
- [ ] `returns an empty object for an empty entries array`
- [ ] `returns the date for a single entry with a single tag_id`
- [ ] `returns the LATEST date when a tag-id appears on multiple days`
- [ ] `returns nothing for tag-ids that never appear in the window`
- [ ] `handles entries with empty tag_ids arrays gracefully`
- [ ] `handles unordered entries — output independent of input order`

**For `compareTagsForPicker`:**
- [ ] `tag with recency sorts BEFORE tag without recency`
- [ ] `more-recent tag sorts BEFORE less-recent tag`
- [ ] `same recency date → higher usage_count sorts first`
- [ ] `same recency + same usage_count → alphabetical ASC, case-insensitive`
- [ ] `both no-recency → tiebreak on usage_count DESC, then alphabetical`
- [ ] `is a valid sort comparator (transitive, returns negative / zero / positive)`

### Component: extend `src/components/__tests__/tag-category-list.test.tsx`

- [ ] `when recencyByTagId is provided, chips inside a category render in recency-first order` — fixture: 3 tags in one category with different recency dates → assert DOM order is most-recent first.
- [ ] `default behaviour (no recencyByTagId prop) is alphabetical within category` — regression of existing tests, but assert explicitly.
- [ ] `newly created tag appears at the front of its category` — drives create flow with a mock fetch returning a new tag, asserts the new chip is the first chip in mentaal.
- [ ] `+ nieuw chip stays at the END of the category, regardless of recency sort`.

### Existing tests stay green

All existing TagCategoryList tests use no `recencyByTagId` prop → default `{}` → alphabetical fallback identical to old behaviour. No regressions expected.

---

## Done-when

- [ ] All listed tests written and RED first.
- [ ] Implementation lands; all tests GREEN.
- [ ] `npm run verify` clean.
- [ ] Manual on dev server:
  - Open Vandaag, expand a category that has both very-recent and never-used tags. Confirm the recent ones are at the front.
  - Toggle through 30d / 90d on the timeline — open the past-day edit popout, confirm recency sort applies to that popout's tag picker too.
  - Create a new tag via `+ nieuw` — confirm it appears at the FRONT of its category (not the end).
- [ ] Step + README ACs ticked.

---

## Out of scope

- Cross-category surfacing ("recent strip" above categories) — rejected in 2026-06-02 brainstorm.
- LLM-driven note → tag inference — v2.
- A "frequent / forgotten" inverse view — speculative.
- Materialising `last_used_at` as a stored column on the `tags` table — possible v1.6 optimisation if perf becomes an issue at scale.
- Surfacing recency across categories ("here are recent tags from mentaal AND fysiek mixed") — explicitly out of scope.
