'use client';

// DayDetailSheet — bottom sheet that opens from the timeline when a user
// taps a day on the chart. Wraps <DayEntryEditor /> with sheet chrome:
// overlay, dialog role + aria-modal, focus trap, close button, ESC to
// close, and focus restoration to the trigger element.
//
// The sheet has its own <SaveStatusProvider> instance (scoped to the
// tapped date) so its merged status is independent of the page-level
// Today provider. The single status glyph lives in the sheet's own
// header; the actionable error banner renders below the editor on
// `status === 'error'`.

import { useEffect, useRef } from 'react';
import { DayEntryEditor } from '@/components/day-entry-editor';
import { SaveStatus } from '@/components/save-status';
import {
  SaveStatusProvider,
  useMergedSaveStatus,
} from '@/components/save-status-context';
import { copy } from '@/copy';
import type { DayEntry } from '@/lib/domain/day-entry';
import { formatDateDutch } from '@/lib/domain/date';
import type { Tag } from '@/lib/domain/tag';

type Props = {
  date: string;
  entry: DayEntry | null;
  allTags: Tag[];
  onClose: () => void;
  onSaved?: () => void;
};

// "Meaningfully later" threshold for the bewerkt marker. created_at and
// updated_at differ by a few ms on a fresh write — we only want to surface
// the marker on actual subsequent edits. 5 seconds is a generous floor.
const EDITED_THRESHOLD_MS = 5_000;

function wasEdited(entry: DayEntry | null): boolean {
  if (entry === null) return false;
  const created = Date.parse(entry.created_at);
  const updated = Date.parse(entry.updated_at);
  return updated - created > EDITED_THRESHOLD_MS;
}

export function DayDetailSheet(props: Props) {
  return (
    <SaveStatusProvider>
      <SheetInner {...props} />
    </SaveStatusProvider>
  );
}

function SheetInner({ date, entry, allTags, onClose, onSaved }: Props) {
  const sheetRef = useRef<HTMLDivElement | null>(null);
  const closeBtnRef = useRef<HTMLButtonElement | null>(null);
  const previouslyFocusedRef = useRef<Element | null>(null);
  const merged = useMergedSaveStatus();

  // Fire onSaved exactly once per successful save so the timeline can
  // re-fetch the visible range.
  const prevStatus = useRef(merged.status);
  useEffect(() => {
    if (prevStatus.current !== 'saved' && merged.status === 'saved' && onSaved) {
      onSaved();
    }
    prevStatus.current = merged.status;
  }, [merged.status, onSaved]);

  // Open behaviour: remember whoever was focused, move focus into the
  // sheet (close button), and restore on unmount. ESC + focus-trap is
  // wired at the document level so the dialog div can stay a passive
  // ARIA wrapper (jsx-a11y forbids onKeyDown on role="dialog").
  useEffect(() => {
    previouslyFocusedRef.current = document.activeElement;
    closeBtnRef.current?.focus();

    function handle(e: KeyboardEvent): void {
      if (e.key === 'Escape') {
        e.preventDefault();
        onClose();
        return;
      }
      if (e.key !== 'Tab') return;
      const root = sheetRef.current;
      if (root === null) return;
      const focusables = root.querySelectorAll<HTMLElement>(
        'button, [href], input, textarea, select, [tabindex]:not([tabindex="-1"])',
      );
      if (focusables.length === 0) return;
      const first = focusables[0]!;
      const last = focusables[focusables.length - 1]!;
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }

    document.addEventListener('keydown', handle);
    return () => {
      document.removeEventListener('keydown', handle);
      const prev = previouslyFocusedRef.current;
      if (prev instanceof HTMLElement) prev.focus();
    };
  }, [onClose]);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={`Entry voor ${formatDateDutch(date)}`}
      ref={sheetRef}
      className="fixed inset-0 z-50 flex items-end justify-center bg-fg/40 sm:items-center"
    >
      {/* Backdrop click closes. The button is invisible but focusable so
          screen-reader users can also dismiss. */}
      <button
        type="button"
        aria-label={copy.timeline.close}
        onClick={onClose}
        className="absolute inset-0 -z-10 cursor-default"
      />
      <div className="flex max-h-[90vh] w-full max-w-120 flex-col gap-4 overflow-y-auto rounded-t-xl bg-surface p-6 shadow-lg sm:rounded-xl">
        <header className="flex items-baseline justify-between gap-3">
          <h2 className="text-xl font-semibold capitalize">{formatDateDutch(date)}</h2>
          <div className="flex items-center gap-2">
            {wasEdited(entry) && (
              <span className="text-sm text-fg-muted">{copy.timeline.edited}</span>
            )}
            <SaveStatus status={merged.status} error={merged.error} variant="glyph" />
            <button
              ref={closeBtnRef}
              type="button"
              onClick={onClose}
              aria-label={copy.timeline.close}
              className="flex h-9 w-9 items-center justify-center rounded-md text-2xl text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
            >
              ×
            </button>
          </div>
        </header>
        <DayEntryEditor date={date} initialEntry={entry} allTags={allTags} />
        {merged.status === 'error' && (
          <SaveStatus status="error" error={merged.error} variant="banner" />
        )}
      </div>
    </div>
  );
}
