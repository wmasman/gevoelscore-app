'use client';

// TagManagementSection — v1.5b Settings → Tag-beheer surface.
//
// List shape A (per the audit decision): label + category only in the
// list row, with an optional `→ {episodeLabel}` suffix for linked tags.
// Drill-down for everything else via TagFormSheet on tap.
//
// Sort: groups by canonical TAG_CATEGORIES order; within each category,
// rows sort by last-used desc (using computeRecencyByTagId from the
// shipped tag-sort helper). Tags never used sink to the bottom of their
// group.
//
// Archived tags hidden by default behind a "Toon gearchiveerd" toggle.
// When ON, archived rows show with reduced opacity + a "(gearchiveerd)"
// suffix.

import { useMemo, useState } from 'react';
import { TagFormSheet } from '@/components/tag-form-sheet';
import { copy } from '@/copy';
import type { DayEntry } from '@/lib/domain/day-entry';
import type { Episode } from '@/lib/domain/episode';
import type { Tag } from '@/lib/domain/tag';
import { computeRecencyByTagId } from '@/lib/domain/tag-sort';
import { TAG_CATEGORIES, type TagCategory } from '@/lib/domain/tag-category';
import { cn } from '@/lib/ui/cn';

type Props = {
  tags: Tag[];
  episodes: Episode[];
  timelineEntries: DayEntry[];
};

const NEVER_USED_SENTINEL = '0000-00-00';

export function TagManagementSection({
  tags,
  episodes,
  timelineEntries,
}: Props) {
  const t = copy.settings.tagManagement;

  const [showArchived, setShowArchived] = useState<boolean>(false);
  const [editTarget, setEditTarget] = useState<Tag | null>(null);

  const recencyByTagId = useMemo(
    () => computeRecencyByTagId(timelineEntries),
    [timelineEntries],
  );

  const episodeLabelById = useMemo(() => {
    const m = new Map<string, string>();
    for (const ep of episodes) m.set(ep.id, ep.label);
    return m;
  }, [episodes]);

  // Filter: archived gated by toggle. Then group by category in the
  // canonical order, sort within by last-used desc.
  const visibleTags = useMemo(
    () => tags.filter((tag) => showArchived || tag.archived_at === null),
    [tags, showArchived],
  );

  const grouped = useMemo(() => {
    const byCategory = new Map<TagCategory, Tag[]>();
    for (const cat of TAG_CATEGORIES) byCategory.set(cat, []);
    for (const tag of visibleTags) byCategory.get(tag.category)?.push(tag);
    for (const cat of TAG_CATEGORIES) {
      const arr = byCategory.get(cat)!;
      arr.sort((a, b) => {
        const ra = recencyByTagId[a.id] ?? NEVER_USED_SENTINEL;
        const rb = recencyByTagId[b.id] ?? NEVER_USED_SENTINEL;
        // Desc — later date first.
        if (rb !== ra) return rb < ra ? -1 : 1;
        // Tie-break: alphabetical for stability.
        return a.label < b.label ? -1 : a.label > b.label ? 1 : 0;
      });
    }
    return byCategory;
  }, [visibleTags, recencyByTagId]);

  const isEmpty = visibleTags.length === 0;

  return (
    <section className="flex flex-col gap-3">
      <h2 className="text-lg font-medium text-fg">{t.heading}</h2>

      <label className="inline-flex items-center gap-2 text-sm text-fg-muted">
        <input
          type="checkbox"
          checked={showArchived}
          onChange={(e) => setShowArchived(e.target.checked)}
          className="h-4 w-4"
        />
        <span>{t.showArchivedToggle}</span>
      </label>

      {isEmpty ? (
        <p className="text-base text-fg-muted">{t.emptyCorpus}</p>
      ) : (
        <div className="flex flex-col gap-4">
          {TAG_CATEGORIES.map((cat) => {
            const items = grouped.get(cat) ?? [];
            if (items.length === 0) return null;
            return (
              <div key={cat} className="flex flex-col gap-1">
                <h3 className="text-sm font-medium uppercase tracking-wider text-fg-muted">
                  {t.categoryLabel[cat]}
                </h3>
                <ul className="flex flex-col divide-y divide-border rounded-md border border-border bg-surface">
                  {items.map((tag) => {
                    const archived = tag.archived_at !== null;
                    const parentLabel =
                      tag.parent_episode_id !== null
                        ? episodeLabelById.get(tag.parent_episode_id) ?? null
                        : null;
                    return (
                      <li key={tag.id} className="flex">
                        <button
                          type="button"
                          onClick={() => setEditTarget(tag)}
                          aria-label={t.rowAriaLabel(
                            tag.label,
                            t.categoryLabel[cat],
                          )}
                          className={cn(
                            'flex min-h-11 flex-1 items-center justify-between gap-3 p-3 text-left text-base',
                            'hover:bg-surface-muted focus-visible:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent',
                            archived && 'opacity-60',
                          )}
                        >
                          <span className="flex items-center gap-2">
                            <span className="text-fg">{tag.label}</span>
                            {archived && (
                              <span className="text-xs text-fg-subtle">
                                {t.archivedSuffix}
                              </span>
                            )}
                          </span>
                          {parentLabel !== null && (
                            <span className="truncate text-sm text-fg-subtle">
                              → {parentLabel}
                            </span>
                          )}
                        </button>
                      </li>
                    );
                  })}
                </ul>
              </div>
            );
          })}
        </div>
      )}

      {editTarget !== null && (
        <TagFormSheet
          tag={editTarget}
          episodes={episodes}
          // v1.5c: forward the full non-archived corpus so the merge
          // button + nested picker can compute eligible same-category
          // alternatives.
          tags={tags}
          open={true}
          onClose={() => setEditTarget(null)}
          onSaved={() => setEditTarget(null)}
          onDeleted={() => setEditTarget(null)}
        />
      )}
    </section>
  );
}
