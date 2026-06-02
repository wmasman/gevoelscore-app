'use client';

// TagPickerSheet — step-5 nested BottomSheet over the EpisodeFormSheet.
// Two paths into a linked tag:
//   1. Pick an existing tag: tap a row → onPickExisting(tagId). Tags
//      linked to a different episode show a "(bij: <label>)" suffix;
//      tapping them is the silent re-parent path.
//   2. Create a new tag with the parent pre-set: tap the CTA → mini-form
//      → onCreateNew({ label, category }). Parent goes on in the same
//      POST round-trip (the parent owns the hook).
//
// The picker is pure presentational. Network + router.refresh + sheet
// state all live in the parent (EpisodeFormSheet); the picker only emits
// intents and reflects { saving, lastError } back as UI feedback.

import { useEffect, useRef, useState } from 'react';
import { BottomSheet } from '@/components/lab/bottom-sheet';
import { copy } from '@/copy';
import type { Episode } from '@/lib/domain/episode';
import { MAX_TAG_LABEL_LENGTH } from '@/lib/domain/tag-label';
import type { Tag } from '@/lib/domain/tag';
import { TAG_CATEGORIES, type TagCategory } from '@/lib/domain/tag-category';

type Props = {
  episode: Episode;
  tags: Tag[];
  episodes: Episode[];
  open: boolean;
  onClose: () => void;
  onPickExisting: (tagId: string) => void;
  onCreateNew: (input: { label: string; category: TagCategory }) => void;
  saving: boolean;
  lastError: string | null;
};

// Display order — same as the canonical TAG_CATEGORIES, but Dutch
// title-case labels for the per-group h3.
const CATEGORY_LABEL: Record<TagCategory, string> = {
  mentaal: 'Mentaal',
  fysiek: 'Fysiek',
  overall: 'Overall',
  activiteit: 'Activiteit',
  gebeurtenis: 'Gebeurtenis',
  interventie: 'Interventie',
  project: 'Project',
  custom: 'Custom',
};

export function TagPickerSheet({
  episode,
  tags,
  episodes,
  open,
  onClose,
  onPickExisting,
  onCreateNew,
  saving,
  lastError,
}: Props) {
  const [creating, setCreating] = useState(false);
  const [newLabel, setNewLabel] = useState('');
  const [newCategory, setNewCategory] = useState<TagCategory | ''>('');
  const [showErrors, setShowErrors] = useState(false);

  // Reset mini-form state every time the picker re-opens. Same prevOpenRef
  // pattern as EpisodeFormSheet: start at false so the initial mount path
  // also triggers a clean state.
  const prevOpenRef = useRef<boolean>(false);
  useEffect(() => {
    if (open && !prevOpenRef.current) {
      setCreating(false);
      setNewLabel('');
      setNewCategory('');
      setShowErrors(false);
    }
    prevOpenRef.current = open;
  }, [open]);

  const eligible = tags.filter((t) => t.parent_episode_id !== episode.id);
  const grouped = TAG_CATEGORIES.map((cat) => ({
    category: cat,
    items: eligible.filter((t) => t.category === cat),
  })).filter((g) => g.items.length > 0);

  const episodeLabelById = new Map<string, string>();
  for (const e of episodes) {
    episodeLabelById.set(e.id, e.label);
  }

  const normalisedLabel = newLabel.trim().replace(/\s+/g, ' ');
  const labelError =
    normalisedLabel.length === 0
      ? 'labelEmpty'
      : normalisedLabel.length > MAX_TAG_LABEL_LENGTH
        ? 'labelTooLong'
        : null;
  const categoryError = newCategory === '' ? 'categoryMissing' : null;
  const canSubmit = !labelError && !categoryError;

  function handleSubmit(e: React.FormEvent): void {
    e.preventDefault();
    if (!canSubmit) {
      setShowErrors(true);
      return;
    }
    onCreateNew({ label: normalisedLabel, category: newCategory as TagCategory });
  }

  return (
    <BottomSheet
      open={open}
      onClose={onClose}
      ariaLabel={copy.context.tagPicker.sheetAriaLabel}
    >
      <div className="flex flex-col gap-4 overflow-y-auto px-6 pb-4">
        <header className="flex items-baseline justify-between pt-1">
          <h2 className="text-lg font-semibold text-fg">
            {copy.context.tagPicker.title}
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label={copy.context.tagPicker.close}
            className="inline-flex min-h-11 min-w-11 items-center justify-center rounded-md text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
          >
            ✕
          </button>
        </header>

        {lastError !== null && (
          <div
            role="alert"
            className="rounded-md border border-error bg-error-soft px-3 py-2 text-sm text-error"
          >
            {copy.context.tagPicker.error.serverError}
          </div>
        )}

        {/* Create CTA / inline mini-form */}
        {!creating ? (
          <div>
            <button
              type="button"
              onClick={() => setCreating(true)}
              disabled={saving}
              className="inline-flex min-h-11 items-center rounded-md border border-border bg-surface px-4 py-2 text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-60"
            >
              {copy.context.tagPicker.createButton}
            </button>
          </div>
        ) : (
          <form
            onSubmit={handleSubmit}
            noValidate
            className="flex flex-col gap-3 rounded-md border border-border bg-surface p-3"
          >
            <div className="flex flex-col gap-1">
              <label
                htmlFor="tag-picker-new-label"
                className="text-sm font-medium text-fg"
              >
                {copy.context.tagPicker.newTagLabelField}
              </label>
              <input
                id="tag-picker-new-label"
                type="text"
                value={newLabel}
                onChange={(e) => {
                  setNewLabel(e.target.value);
                  setShowErrors(true);
                }}
                // No maxLength attribute — the labelTooLong validator owns
                // the cap. Lets clipboard paste / IME input land in state
                // and surface the explicit Dutch error, rather than getting
                // silently truncated by the browser.
                placeholder={copy.context.tagPicker.newTagLabelPlaceholder}
                aria-required="true"
                aria-invalid={showErrors && labelError ? 'true' : 'false'}
                className="rounded-md border border-border bg-bg px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-accent"
              />
              {showErrors && labelError !== null && (
                <p role="alert" className="text-sm text-error">
                  {labelError === 'labelEmpty'
                    ? copy.context.tagPicker.error.labelEmpty
                    : copy.context.tagPicker.error.labelTooLong}
                </p>
              )}
            </div>
            <div className="flex flex-col gap-1">
              <label
                htmlFor="tag-picker-new-category"
                className="text-sm font-medium text-fg"
              >
                {copy.context.tagPicker.newTagCategoryField}
              </label>
              <select
                id="tag-picker-new-category"
                value={newCategory}
                onChange={(e) => {
                  setNewCategory(e.target.value as TagCategory | '');
                  setShowErrors(true);
                }}
                aria-required="true"
                aria-invalid={showErrors && categoryError ? 'true' : 'false'}
                className="rounded-md border border-border bg-bg px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-accent"
              >
                <option value="">
                  {copy.context.tagPicker.newTagCategoryPlaceholder}
                </option>
                {TAG_CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>
                    {CATEGORY_LABEL[cat]}
                  </option>
                ))}
              </select>
              {showErrors && categoryError !== null && (
                <p role="alert" className="text-sm text-error">
                  {copy.context.tagPicker.error.categoryMissing}
                </p>
              )}
            </div>
            <div className="flex items-center gap-3 pt-1">
              <button
                type="button"
                onClick={() => setCreating(false)}
                className="inline-flex min-h-11 items-center rounded-md px-3 py-2 text-sm text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
              >
                {copy.context.tagPicker.cancel}
              </button>
              <button
                type="submit"
                disabled={saving}
                aria-busy={saving ? 'true' : 'false'}
                className="inline-flex min-h-11 items-center rounded-md bg-accent-hover px-4 py-2 text-base font-medium text-bg focus-visible:outline-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-60"
              >
                {copy.context.tagPicker.newTagSubmit}
              </button>
            </div>
          </form>
        )}

        {/* Existing tags grouped by category */}
        {grouped.length === 0 ? (
          <p className="text-sm text-fg-muted">
            {copy.context.tagPicker.emptyCorpus}
          </p>
        ) : (
          <div className="flex flex-col gap-4">
            {grouped.map((g) => (
              <div key={g.category} className="flex flex-col gap-1">
                <h3 className="text-sm font-medium uppercase tracking-wider text-fg-muted">
                  {CATEGORY_LABEL[g.category]}
                </h3>
                <ul className="flex flex-col divide-y divide-border rounded-md border border-border bg-surface">
                  {g.items.map((t) => {
                    const otherLabel =
                      t.parent_episode_id !== null
                        ? episodeLabelById.get(t.parent_episode_id) ?? null
                        : null;
                    return (
                      <li key={t.id} className="flex">
                        <button
                          type="button"
                          onClick={() => onPickExisting(t.id)}
                          disabled={saving}
                          className="flex min-h-11 flex-1 items-center justify-between gap-3 p-4 text-left hover:bg-surface-muted focus-visible:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-60"
                        >
                          <span className="text-base text-fg">{t.label}</span>
                          {otherLabel !== null && (
                            <span className="text-sm text-fg-subtle">
                              {copy.context.tagPicker.bijSuffix(otherLabel)}
                            </span>
                          )}
                        </button>
                      </li>
                    );
                  })}
                </ul>
              </div>
            ))}
          </div>
        )}
      </div>
    </BottomSheet>
  );
}
