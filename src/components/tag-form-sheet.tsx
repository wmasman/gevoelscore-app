'use client';

// TagFormSheet — v1.5b tag-management edit surface.
//
// Mirrors EpisodeFormSheet shape: BottomSheet hosting a form with
// closed→open edge-sync via prevOpenRef. Rename + recategorize +
// re-parent commit in ONE PATCH (the form computes a diff against
// initialTag). Archive / Un-archive is a single-key PATCH. Hard-delete
// (only enabled when usage_count === 0) is gated by an inline confirm
// alertdialog where focus lands on Annuleer (M5: brainfog protection).
//
// Validation: client-side via the same validators the API library uses
// (validateTagLabel, validateTagCategory). Per-field server errors
// surface in the top-of-sheet banner with field-specific copy (M1 fix
// dividend — the user sees "Naam is ongeldig" not "invalid_patch").

import { useEffect, useRef, useState } from 'react';
import { BottomSheet } from '@/components/lab/bottom-sheet';
import { copy } from '@/copy';
import { useTagManage, type TagManagePatch } from '@/hooks/use-tag-manage';
import type { Episode } from '@/lib/domain/episode';
import { formatDateDutch } from '@/lib/domain/date';
import { MAX_TAG_LABEL_LENGTH, MAX_TAG_LABEL_WORDS } from '@/lib/domain/tag-label';
import type { Tag } from '@/lib/domain/tag';
import { TAG_CATEGORIES, type TagCategory } from '@/lib/domain/tag-category';
import { cn } from '@/lib/ui/cn';

type Props = {
  tag: Tag;
  episodes: Episode[];
  open: boolean;
  onClose: () => void;
  onSaved: (tag: Tag) => void;
  onDeleted: (deletedId: string) => void;
};

// Map server-side per-field error codes to Dutch copy.
function serverErrorCopy(code: string | null): string | null {
  if (code === null) return null;
  const e = copy.settings.tagManagement.form.error;
  switch (code) {
    case 'invalid_label':
      return e.invalidLabel;
    case 'invalid_category':
      return e.invalidCategory;
    case 'invalid_archived_at':
      return e.invalidArchivedAt;
    case 'invalid_parent_episode_id':
      return e.invalidParent;
    case 'tag_in_use':
      return e.tagInUse;
    default:
      return e.serverError;
  }
}

export function TagFormSheet({
  tag,
  episodes,
  open,
  onClose,
  onSaved,
  onDeleted,
}: Props) {
  const t = copy.settings.tagManagement;

  const [label, setLabel] = useState<string>(tag.label);
  const [category, setCategory] = useState<TagCategory>(tag.category);
  const [parent, setParent] = useState<string | null>(tag.parent_episode_id);
  const [showLabelError, setShowLabelError] = useState<boolean>(false);
  const [confirming, setConfirming] = useState<boolean>(false);
  const cancelButtonRef = useRef<HTMLButtonElement>(null);

  const { save, setArchived, hardDelete, status, lastError } = useTagManage();

  // Closed → open edge: re-sync state from props. Same pattern as
  // EpisodeFormSheet — prevOpenRef starts at false so a component that
  // mounts with open=true ALSO triggers the initial sync.
  const prevOpenRef = useRef<boolean>(false);
  useEffect(() => {
    if (open && !prevOpenRef.current) {
      setLabel(tag.label);
      setCategory(tag.category);
      setParent(tag.parent_episode_id);
      setShowLabelError(false);
      setConfirming(false);
    }
    prevOpenRef.current = open;
  }, [open, tag]);

  // Focus management for the confirm alertdialog (M5 + matches the
  // settings-view.tsx logout-confirm pattern).
  useEffect(() => {
    if (confirming) {
      cancelButtonRef.current?.focus();
    }
  }, [confirming]);

  // Derived: label validation. Replicates validateTagLabel rules.
  const trimmedLabel = label.trim().replace(/\s+/g, ' ');
  const labelError: 'empty' | 'tooLong' | 'tooManyWords' | null =
    trimmedLabel.length === 0
      ? 'empty'
      : trimmedLabel.length > MAX_TAG_LABEL_LENGTH
        ? 'tooLong'
        : trimmedLabel.split(' ').length > MAX_TAG_LABEL_WORDS
          ? 'tooManyWords'
          : null;

  // Diff against initialTag — Save only fires the changed keys.
  const diff: TagManagePatch = {};
  if (trimmedLabel !== tag.label) diff.label = trimmedLabel;
  if (category !== tag.category) diff.category = category;
  if (parent !== tag.parent_episode_id) diff.parent_episode_id = parent;
  const hasChanges = Object.keys(diff).length > 0;

  const canSubmit = hasChanges && labelError === null;

  async function handleSave(e: React.FormEvent): Promise<void> {
    e.preventDefault();
    if (!canSubmit) {
      setShowLabelError(true);
      return;
    }
    const updated = await save(tag.id, diff);
    if (updated) onSaved(updated);
  }

  async function handleArchiveToggle(): Promise<void> {
    const next = tag.archived_at === null ? new Date().toISOString() : null;
    const updated = await setArchived(tag.id, next);
    if (updated) onSaved(updated);
  }

  async function handleConfirmDelete(): Promise<void> {
    const result = await hardDelete(tag.id);
    if (result) {
      setConfirming(false);
      onDeleted(result.deleted_id);
    }
  }

  const archived = tag.archived_at !== null;
  const canHardDelete = tag.usage_count === 0;
  const serverBanner = serverErrorCopy(lastError);

  return (
    <BottomSheet
      open={open}
      onClose={onClose}
      ariaLabel={t.form.sheetAriaLabel}
    >
      <form
        onSubmit={handleSave}
        noValidate
        className="flex flex-col gap-4 overflow-y-auto px-6 pb-4"
      >
        <header className="flex items-baseline justify-between pt-1">
          <h2 className="text-lg font-semibold text-fg">{t.form.title}</h2>
          <button
            type="button"
            onClick={onClose}
            aria-label={t.form.close}
            className="inline-flex min-h-11 min-w-11 items-center justify-center rounded-md text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
          >
            ✕
          </button>
        </header>

        {serverBanner !== null && (
          <div
            role="alert"
            className="rounded-md border border-error bg-error-soft px-3 py-2 text-sm text-error"
          >
            {serverBanner}
          </div>
        )}

        {/* Naam */}
        <div className="flex flex-col gap-1">
          <label
            htmlFor="tag-form-label"
            className="text-sm font-medium text-fg"
          >
            {t.form.labelField}
          </label>
          <input
            id="tag-form-label"
            type="text"
            value={label}
            onChange={(e) => {
              setLabel(e.target.value);
              setShowLabelError(true);
            }}
            aria-required="true"
            aria-invalid={showLabelError && labelError ? 'true' : 'false'}
            className="rounded-md border border-border bg-bg px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-accent"
          />
          {showLabelError && labelError !== null && (
            <p role="alert" className="text-sm text-error">
              {labelError === 'empty'
                ? t.form.error.labelEmpty
                : labelError === 'tooLong'
                  ? t.form.error.labelTooLong
                  : t.form.error.labelTooManyWords}
            </p>
          )}
        </div>

        {/* Categorie */}
        <div className="flex flex-col gap-1">
          <label
            htmlFor="tag-form-category"
            className="text-sm font-medium text-fg"
          >
            {t.form.categoryField}
          </label>
          <select
            id="tag-form-category"
            value={category}
            onChange={(e) => setCategory(e.target.value as TagCategory)}
            className="rounded-md border border-border bg-bg px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-accent"
          >
            {TAG_CATEGORIES.map((c) => (
              <option key={c} value={c}>
                {t.categoryLabel[c]}
              </option>
            ))}
          </select>
        </div>

        {/* Behoort bij */}
        <div className="flex flex-col gap-1">
          <label
            htmlFor="tag-form-parent"
            className="text-sm font-medium text-fg"
          >
            {t.form.parentField}
          </label>
          <select
            id="tag-form-parent"
            value={parent ?? ''}
            onChange={(e) =>
              setParent(e.target.value === '' ? null : e.target.value)
            }
            className="rounded-md border border-border bg-bg px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-accent"
          >
            <option value="">{t.form.parentNone}</option>
            {episodes
              .filter((ep) => ep.archived_at === null)
              .map((ep) => (
                <option key={ep.id} value={ep.id}>
                  {ep.label}
                </option>
              ))}
          </select>
        </div>

        {/* Status block — read-only grounding before destructive actions */}
        <p className="text-sm text-fg-muted">
          {tag.usage_count === 0
            ? t.statusNeverUsed
            : t.statusUsed(
                tag.usage_count,
                formatDateDutch(tag.created_at.slice(0, 10)),
              )}
        </p>

        {/* Action row */}
        <div className="flex flex-col gap-3 pt-2">
          <button
            type="submit"
            disabled={!canSubmit || status === 'saving'}
            aria-busy={status === 'saving' ? 'true' : 'false'}
            className={cn(
              'inline-flex min-h-11 items-center justify-center rounded-md px-4 py-2 text-base font-medium focus-visible:outline-2 focus-visible:outline-accent',
              !canSubmit || status === 'saving'
                ? 'cursor-not-allowed bg-surface-muted text-fg-muted'
                : 'bg-accent-hover text-bg',
            )}
          >
            {status === 'saving' ? t.form.saving : t.form.save}
          </button>

          <button
            type="button"
            onClick={() => void handleArchiveToggle()}
            disabled={status === 'saving'}
            className="inline-flex min-h-11 items-center justify-center rounded-md border border-border px-4 py-2 text-base text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
          >
            {archived ? t.form.unarchive : t.form.archive}
          </button>

          <button
            type="button"
            onClick={() => setConfirming(true)}
            disabled={!canHardDelete || status === 'saving'}
            className="inline-flex min-h-11 items-center justify-center rounded-md px-4 py-2 text-base text-error hover:bg-error-soft focus-visible:outline-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-50"
          >
            {t.form.delete}
          </button>
          {!canHardDelete && (
            <p className="text-xs text-fg-subtle">{t.form.deleteHint}</p>
          )}
        </div>

        {/* Inline confirm alertdialog — appears INSIDE the form */}
        {confirming && (
          <div
            role="alertdialog"
            aria-labelledby="tag-delete-prompt"
            className="flex flex-col gap-3 rounded-md border border-error bg-error-soft p-4"
          >
            <p id="tag-delete-prompt" className="text-base text-fg">
              {t.form.confirm.prompt(tag.label)}
            </p>
            <div className="flex gap-3">
              <button
                ref={cancelButtonRef}
                type="button"
                onClick={() => setConfirming(false)}
                disabled={status === 'saving'}
                className="inline-flex min-h-11 items-center rounded-md border border-border bg-bg px-4 py-2 text-base text-fg focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
              >
                {t.form.confirm.cancel}
              </button>
              <button
                type="button"
                onClick={() => void handleConfirmDelete()}
                disabled={status === 'saving'}
                className="inline-flex min-h-11 items-center rounded-md bg-accent-hover px-4 py-2 text-base font-medium text-bg focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
              >
                {t.form.confirm.confirm}
              </button>
            </div>
          </div>
        )}
      </form>
    </BottomSheet>
  );
}
