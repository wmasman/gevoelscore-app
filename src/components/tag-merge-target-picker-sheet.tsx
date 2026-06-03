'use client';

// TagMergeTargetPickerSheet — v1.5c nested BottomSheet over TagFormSheet.
//
// Pure presentational: lists same-category non-archived alternatives,
// holds the pending-target in local state, owns the inline confirm
// alertdialog (focus on Annuleer for brainfog protection), and emits
// `onMergeConfirmed(target)` ONLY when the user taps "Ja, samenvoegen".
// Tap on a row enters confirm-mode; Annuleer returns to list-mode.
//
// Sorting: alphabetical (no recency map needed — corpus is small within
// one category). Same-category-only is a hard rule of v1.5c.

import { useEffect, useRef, useState } from 'react';
import { BottomSheet } from '@/components/lab/bottom-sheet';
import { copy } from '@/copy';
import type { Tag } from '@/lib/domain/tag';

type Props = {
  source: Tag;
  tags: Tag[];
  open: boolean;
  onClose: () => void;
  onMergeConfirmed: (target: Tag) => void;
  saving: boolean;
  lastError: string | null;
};

function serverErrorCopy(code: string | null): string | null {
  if (code === null) return null;
  const e = copy.settings.tagManagement.merge.error;
  switch (code) {
    case 'same_tag':
      return e.sameTag;
    case 'source_not_found':
      return e.sourceNotFound;
    case 'target_not_found':
      return e.targetNotFound;
    case 'source_archived':
      return e.sourceArchived;
    case 'target_archived':
      return e.targetArchived;
    case 'category_mismatch':
      return e.categoryMismatch;
    default:
      return e.serverError;
  }
}

export function TagMergeTargetPickerSheet({
  source,
  tags,
  open,
  onClose,
  onMergeConfirmed,
  saving,
  lastError,
}: Props) {
  const m = copy.settings.tagManagement.merge;

  const [pendingTarget, setPendingTarget] = useState<Tag | null>(null);
  const cancelButtonRef = useRef<HTMLButtonElement>(null);

  // Closed → open edge: reset confirm-mode each re-open.
  const prevOpenRef = useRef<boolean>(false);
  useEffect(() => {
    if (open && !prevOpenRef.current) {
      setPendingTarget(null);
    }
    prevOpenRef.current = open;
  }, [open]);

  // Focus on Annuleer when confirm-mode engages (brainfog protection).
  useEffect(() => {
    if (pendingTarget !== null) {
      cancelButtonRef.current?.focus();
    }
  }, [pendingTarget]);

  const eligible = tags
    .filter(
      (t) =>
        t.category === source.category &&
        t.archived_at === null &&
        t.id !== source.id,
    )
    .sort((a, b) =>
      a.label.localeCompare(b.label, 'nl', { sensitivity: 'base' }),
    );

  const serverBanner = serverErrorCopy(lastError);

  return (
    <BottomSheet open={open} onClose={onClose} ariaLabel={m.sheetAriaLabel}>
      <div className="flex flex-col gap-4 overflow-y-auto px-6 pb-4">
        <header className="flex items-baseline justify-between pt-1">
          <h2 className="text-lg font-semibold text-fg">{m.sheetTitle}</h2>
          <button
            type="button"
            onClick={onClose}
            aria-label={m.close}
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

        {pendingTarget === null ? (
          eligible.length === 0 ? (
            <p className="text-sm text-fg-muted">{m.emptyState}</p>
          ) : (
            <ul className="flex flex-col gap-1">
              {eligible.map((t) => (
                <li key={t.id}>
                  <button
                    type="button"
                    onClick={() => setPendingTarget(t)}
                    disabled={saving}
                    className="inline-flex w-full min-h-11 items-center rounded-md px-3 py-2 text-left text-base text-fg hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {t.label}
                  </button>
                </li>
              ))}
            </ul>
          )
        ) : (
          <div
            role="alertdialog"
            aria-labelledby="tag-merge-confirm-prompt"
            className="flex flex-col gap-3 rounded-md border border-accent bg-surface-muted p-4"
          >
            <p id="tag-merge-confirm-prompt" className="text-base text-fg">
              {m.confirm.prompt(source.label, source.usage_count, pendingTarget.label)}
            </p>
            <div className="flex gap-3">
              <button
                ref={cancelButtonRef}
                type="button"
                onClick={() => setPendingTarget(null)}
                disabled={saving}
                className="inline-flex min-h-11 items-center rounded-md border border-border bg-bg px-4 py-2 text-base text-fg focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
              >
                {m.confirm.cancel}
              </button>
              <button
                type="button"
                onClick={() => onMergeConfirmed(pendingTarget)}
                disabled={saving}
                className="inline-flex min-h-11 items-center rounded-md bg-accent-hover px-4 py-2 text-base font-medium text-bg focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
              >
                {m.confirm.confirm}
              </button>
            </div>
          </div>
        )}
      </div>
    </BottomSheet>
  );
}
