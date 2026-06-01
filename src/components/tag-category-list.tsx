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
//
// Inline tag creation (2026-06-01): each expanded category ends with a
// "+ nieuw" chip; tapping it reveals an inline input. Saving POSTs to
// /api/tags then chains into the existing day-entries PUT to attach the
// new tag-id. See docs/features/inline-tag-creation/.

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

type Composing = {
  category: TagCategory;
  label: string;
  status: 'idle' | 'pending' | 'error';
};

type CreateTagResponse = {
  outcome: 'created' | 'matched_active' | 'matched_reactivated';
  tag: Tag;
};

export function TagCategoryList({ date, allTags, initialTagIds, disabled }: Props) {
  const [selected, setSelected] = useState<Set<string>>(new Set(initialTagIds));
  const [expandedCats, setExpandedCats] = useState<Set<TagCategory>>(new Set());
  const [extraOpen, setExtraOpen] = useState<boolean>(false);
  const [composing, setComposing] = useState<Composing | null>(null);
  // Tags that were created or reactivated in this session. Merged with
  // allTags for rendering so the new chip appears immediately — before
  // the parent's router.refresh re-fetches the full list.
  const [locallyAddedTags, setLocallyAddedTags] = useState<Tag[]>([]);
  const lastSavedRef = useRef<Set<string>>(new Set(initialTagIds));
  const inputRef = useRef<HTMLInputElement | null>(null);
  const newChipRefs = useRef<Map<string, HTMLButtonElement>>(new Map());
  const focusAfterCreateId = useRef<string | null>(null);
  const { save, status, lastError } = useDayEntryUpsert(date);
  useReportSaveStatus('tags', status, lastError);

  const effectiveTags = useMemo<Tag[]>(() => {
    if (locallyAddedTags.length === 0) return allTags;
    const seen = new Set(allTags.map((t) => t.id));
    const merged = [...allTags];
    for (const t of locallyAddedTags) {
      if (!seen.has(t.id)) merged.push(t);
    }
    return merged;
  }, [allTags, locallyAddedTags]);

  const byCategory = useMemo(() => {
    const map = new Map<TagCategory, Tag[]>();
    for (const c of [...PRIMARY_CATEGORIES, ...EXTRA_CATEGORIES]) map.set(c, []);
    for (const t of effectiveTags) {
      if (t.archived_at !== null) continue;
      map.get(t.category)?.push(t);
    }
    return map;
  }, [effectiveTags]);

  const extraSelectedCount = useMemo(() => {
    let count = 0;
    for (const t of effectiveTags) {
      if (selected.has(t.id) && EXTRA_CATEGORIES.includes(t.category)) count++;
    }
    return count;
  }, [effectiveTags, selected]);

  useEffect(() => {
    if (status === 'error') {
      const lastSaved = lastSavedRef.current;
      const same =
        selected.size === lastSaved.size &&
        [...selected].every((id) => lastSaved.has(id));
      if (!same) setSelected(new Set(lastSaved));
    } else if (status === 'saved') {
      lastSavedRef.current = new Set(selected);
    }
  }, [status, selected]);

  // Focus the new chip after a successful create. The chip ref is set as
  // the new tag mounts; this effect runs after that mount and moves focus.
  useEffect(() => {
    const id = focusAfterCreateId.current;
    if (!id) return;
    const el = newChipRefs.current.get(id);
    if (el) {
      el.focus();
      focusAfterCreateId.current = null;
    }
  });

  // Focus the inline input when composing opens or re-opens.
  useEffect(() => {
    if (composing && composing.status !== 'pending') {
      inputRef.current?.focus();
    }
  }, [composing]);

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

  function openComposer(category: TagCategory): void {
    setComposing({ category, label: '', status: 'idle' });
  }

  function cancelComposer(): void {
    setComposing(null);
  }

  async function submitComposer(): Promise<void> {
    if (!composing) return;
    const trimmed = composing.label.trim().replace(/\s+/g, ' ');
    if (trimmed.length === 0) return; // no-op on whitespace-only
    const category = composing.category;
    setComposing({ category, label: trimmed, status: 'pending' });

    try {
      const res = await fetch('/api/tags', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ label: trimmed, category }),
      });
      if (!res.ok) {
        setComposing({ category, label: trimmed, status: 'error' });
        return;
      }
      const body = (await res.json()) as CreateTagResponse;
      if (body.outcome !== 'matched_active') {
        // Add to local tag list so the chip renders immediately.
        setLocallyAddedTags((prev) => {
          if (prev.some((t) => t.id === body.tag.id)) return prev;
          return [...prev, body.tag];
        });
      }
      // Select the (possibly-existing) tag and chain into the day-entry save.
      const nextSet = new Set(selected);
      nextSet.add(body.tag.id);
      setSelected(nextSet);
      focusAfterCreateId.current = body.tag.id;
      setComposing(null);
      void save({ tag_ids: Array.from(nextSet) }, { flush: true });
    } catch {
      setComposing({ category, label: trimmed, status: 'error' });
    }
  }

  function renderCategory(category: TagCategory) {
    const tags = byCategory.get(category) ?? [];
    const selectedCount = tags.filter((t) => selected.has(t.id)).length;
    const isExpanded = expandedCats.has(category);
    const isComposingHere = composing?.category === category;
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
          <div className="mt-1 flex flex-wrap items-center gap-2 px-1 py-2">
            {/* Composing input is rendered AT THE TOP of the chip area
                (before the chips) so it's always visible directly under
                the category header. Previous layout placed it at the
                bottom of the chip row, where on a long expanded category
                with the keyboard up it ended up below the visible area
                on iPhone. Top placement = always in view, no scroll
                required. The chips below remain interactive so the user
                can see what already exists and tap an existing chip if
                they realise their typed label is a duplicate. */}
            {isComposingHere && composing?.status === 'pending' && (
              <span
                data-pending="true"
                aria-disabled="true"
                className="basis-full inline-flex min-h-11 items-center rounded-full border border-border bg-bg px-4 py-2 text-sm text-fg opacity-60"
              >
                {composing.label}
              </span>
            )}
            {isComposingHere && composing?.status !== 'pending' ? (
              // basis-full takes its own row in the flex-wrap parent;
              // min-w-0 + flex-1 lets the input shrink to fit phone width
              // (without these the input forced horizontal overflow).
              <span className="flex w-full basis-full items-center gap-2">
                <input
                  ref={inputRef}
                  type="text"
                  aria-label={copy.daily.tags.newInputAriaLabel}
                  placeholder={copy.daily.tags.newInputPlaceholder}
                  value={composing.label}
                  onChange={(e) =>
                    setComposing((c) => (c ? { ...c, label: e.target.value, status: 'idle' } : null))
                  }
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      void submitComposer();
                    } else if (e.key === 'Escape') {
                      e.preventDefault();
                      cancelComposer();
                    }
                  }}
                  className="min-w-0 flex-1 min-h-11 rounded-full border border-accent bg-bg px-4 py-2 text-sm text-fg focus-visible:outline-2 focus-visible:outline-accent"
                />
                <button
                  type="button"
                  onMouseDown={(e) => {
                    // Defeat the blur-vs-click race: the input's blur would
                    // otherwise cancel composing before the click handler
                    // fires (m2 audit fix).
                    e.preventDefault();
                  }}
                  onClick={() => void submitComposer()}
                  className="inline-flex min-h-11 shrink-0 items-center rounded-full border border-accent bg-accent px-4 py-2 text-sm text-bg focus-visible:outline-2 focus-visible:outline-accent"
                >
                  {copy.daily.tags.addButton}
                </button>
              </span>
            ) : null}
            {tags.map((t) => {
              const isSelected = selected.has(t.id);
              return (
                <button
                  key={t.id}
                  type="button"
                  ref={(el) => {
                    if (el) newChipRefs.current.set(t.id, el);
                    else newChipRefs.current.delete(t.id);
                  }}
                  aria-pressed={isSelected}
                  onClick={() => toggleTag(t.id)}
                  disabled={disabled}
                  className={
                    isSelected
                      ? 'inline-flex min-h-11 items-center rounded-full border border-accent bg-accent px-4 py-2 text-sm text-bg disabled:opacity-60'
                      : 'inline-flex min-h-11 items-center rounded-full border border-border bg-bg px-4 py-2 text-sm text-fg disabled:opacity-60'
                  }
                >
                  {t.label}
                </button>
              );
            })}
            {!isComposingHere && (
              <button
                type="button"
                onClick={() => openComposer(category)}
                disabled={disabled}
                aria-label={`${copy.daily.tags.addAriaLabel} ${category}`}
                className="inline-flex min-h-11 items-center rounded-full border border-border border-dashed bg-bg px-4 py-2 text-sm text-fg-muted hover:text-fg disabled:opacity-60"
              >
                {copy.daily.tags.addChipLabel}
              </button>
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
        className="mt-1 inline-flex min-h-11 items-center gap-2 self-start rounded-md px-3 py-2 text-left text-sm text-fg-muted hover:text-fg focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
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
