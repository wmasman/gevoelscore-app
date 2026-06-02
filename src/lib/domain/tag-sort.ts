// Sort helpers for the daily tag picker. The picker orders chips inside
// each expanded category by recency-then-frequency-then-alphabetical so
// the chip a user reaches for most is the first chip they see. No new
// UI affordance — just a reorder.
//
// See features/tag-recency-sort/ for the design + the rejected
// alternative (cross-category "recent strip" was too prominent for a
// brainfog-sensitive surface).

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
 * picker. Order:
 *
 *   1. Tags with recency sort BEFORE tags without recency.
 *   2. Within the recency bucket: more-recent (DESC by ISO date).
 *   3. Same recency (or both no-recency): higher usage_count first.
 *   4. Final tiebreaker: alphabetical ASC, case-insensitive.
 *
 * Pure. Stable when used with Array.prototype.sort.
 */
export function compareTagsForPicker(
  a: Tag,
  b: Tag,
  recency: Record<string, string>,
): number {
  const aLast = recency[a.id];
  const bLast = recency[b.id];
  if (aLast !== undefined && bLast === undefined) return -1;
  if (aLast === undefined && bLast !== undefined) return 1;
  if (aLast !== undefined && bLast !== undefined && aLast !== bLast) {
    return aLast > bLast ? -1 : 1;
  }
  if (a.usage_count !== b.usage_count) return b.usage_count - a.usage_count;
  return a.label.toLowerCase().localeCompare(b.label.toLowerCase());
}
