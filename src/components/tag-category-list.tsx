'use client';

// TagCategoryList — vertical stack of 4 primary category headers
// (mentaal, fysiek, overall, activiteit) followed by an "Extra opties"
// expand toggle that reveals the 4 secondary categories (gebeurtenis,
// interventie, project, custom) inline. Brainfog rule: ≤5 primary actions
// visible at once.
//
// Each individual category header is independently expand/collapse-able to
// reveal its chips. Multiple categories may be expanded simultaneously —
// exploration is not punished. The Extra-opties toggle and each header's
// chip-display state are independent.

import { useEffect, useMemo, useRef, useState } from 'react';
import { useReportSaveStatus } from '@/components/save-status-context';
import { copy } from '@/copy';
import { useDayEntryUpsert } from '@/hooks/use-day-entry-upsert';
import type { Tag } from '@/lib/domain/tag';
import type { TagCategory } from '@/lib/domain/tag-category';

const PRIMARY_CATEGORIES: readonly TagCategory[] = [
  'mentaal',
  'fysiek',
  'overall',
  'activiteit',
];
const EXTRA_CATEGORIES: readonly TagCategory[] = [
  'gebeurtenis',
  'interventie',
  'project',
  'custom',
];

type Props = {
  date: string;
  allTags: Tag[];
  initialTagIds: string[];
  disabled: boolean;
};

export function TagCategoryList({ date, allTags, initialTagIds, disabled }: Props) {
  const [selected, setSelected] = useState<Set<string>>(new Set(initialTagIds));
  const [expandedCats, setExpandedCats] = useState<Set<TagCategory>>(new Set());
  const [extraOpen, setExtraOpen] = useState<boolean>(false);
  const lastSavedRef = useRef<Set<string>>(new Set(initialTagIds));
  const { save, status, lastError } = useDayEntryUpsert(date);
  useReportSaveStatus('tags', status, lastError);

  const byCategory = useMemo(() => {
    const map = new Map<TagCategory, Tag[]>();
    for (const c of [...PRIMARY_CATEGORIES, ...EXTRA_CATEGORIES]) map.set(c, []);
    for (const t of allTags) {
      if (t.archived_at !== null) continue;
      map.get(t.category)?.push(t);
    }
    return map;
  }, [allTags]);

  const extraSelectedCount = useMemo(() => {
    let count = 0;
    for (const t of allTags) {
      if (selected.has(t.id) && EXTRA_CATEGORIES.includes(t.category)) count++;
    }
    return count;
  }, [allTags, selected]);

  useEffect(() => {
    if (status === 'error') {
      // Restore from snapshot only if current optimistic state differs —
      // unconditional setSelected(new Set(...)) would create a fresh ref
      // every render and loop.
      const lastSaved = lastSavedRef.current;
      const same =
        selected.size === lastSaved.size &&
        [...selected].every((id) => lastSaved.has(id));
      if (!same) setSelected(new Set(lastSaved));
    } else if (status === 'saved') {
      lastSavedRef.current = new Set(selected);
    }
  }, [status, selected]);

  function toggleCategory(category: TagCategory): void {
    setExpandedCats((prev) => {
      const next = new Set(prev);
      if (next.has(category)) next.delete(category);
      else next.add(category);
      return next;
    });
  }

  function toggleTag(tagId: string): void {
    const nextSet = new Set(selected);
    if (nextSet.has(tagId)) nextSet.delete(tagId);
    else nextSet.add(tagId);
    setSelected(nextSet);
    void save({ tag_ids: Array.from(nextSet) }, { flush: true });
  }

  function renderCategory(category: TagCategory) {
    const tags = byCategory.get(category) ?? [];
    const selectedCount = tags.filter((t) => selected.has(t.id)).length;
    const isExpanded = expandedCats.has(category);
    return (
      <li key={category}>
        <button
          type="button"
          aria-expanded={isExpanded}
          onClick={() => toggleCategory(category)}
          disabled={disabled}
          className="flex w-full min-h-12 items-center justify-between rounded-md border border-border px-3 py-3 text-left text-base capitalize disabled:opacity-60"
        >
          <span>
            <span>{category}</span>
            {selectedCount > 0 && (
              <span className="ml-2 text-sm text-fg-muted">· {selectedCount}</span>
            )}
          </span>
          <span aria-hidden="true">{isExpanded ? '−' : '+'}</span>
        </button>
        {isExpanded && (
          <div className="mt-1 flex flex-wrap gap-2 px-1 py-2">
            {tags.length === 0 ? (
              <span className="text-sm italic text-fg-muted">{copy.daily.tags.empty}</span>
            ) : (
              tags.map((t) => {
                const isSelected = selected.has(t.id);
                return (
                  <button
                    key={t.id}
                    type="button"
                    aria-pressed={isSelected}
                    onClick={() => toggleTag(t.id)}
                    disabled={disabled}
                    className={
                      isSelected
                        ? 'min-h-9 rounded-full border border-accent bg-accent px-3 py-1 text-sm text-bg disabled:opacity-60'
                        : 'min-h-9 rounded-full border border-border bg-bg px-3 py-1 text-sm text-fg disabled:opacity-60'
                    }
                  >
                    {t.label}
                  </button>
                );
              })
            )}
          </div>
        )}
      </li>
    );
  }

  return (
    <section aria-labelledby="tags-heading" className="flex flex-col gap-2">
      <h2 id="tags-heading" className="text-sm font-medium text-fg-muted">
        {copy.daily.tags.label}
      </h2>
      <ul className="flex flex-col gap-1">
        {PRIMARY_CATEGORIES.map(renderCategory)}
      </ul>

      <button
        type="button"
        aria-expanded={extraOpen}
        onClick={() => setExtraOpen((prev) => !prev)}
        disabled={disabled}
        className="mt-1 inline-flex items-center gap-2 self-start rounded-md px-2 py-1 text-left text-sm text-fg-muted hover:text-fg focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
      >
        <span>
          {copy.daily.tags.extraToggle}
          {extraSelectedCount > 0 ? ` (${extraSelectedCount})` : ''}
        </span>
        <span aria-hidden="true">{extraOpen ? '⌃' : '⌄'}</span>
      </button>

      {extraOpen && (
        <ul className="flex flex-col gap-1">
          {EXTRA_CATEGORIES.map(renderCategory)}
        </ul>
      )}
    </section>
  );
}
