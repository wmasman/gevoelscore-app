'use client';

import { copy } from '@/copy';
import type { SaveStatus as SaveStatusValue } from '@/hooks/use-day-entry-upsert';

// One source of truth for the saved/saving/error visual language. Every
// component that calls useDayEntryUpsert embeds <SaveStatus /> next to its
// own optimistic UI; the hook's status state drives the display.
//
// Idle state: renders nothing (avoids visual noise on first paint).

type Props = {
  status: SaveStatusValue;
  // Reserved for a future detailed error view; today the banner uses a
  // single generic Dutch string from copy.errors.notSaved.
  error?: string | null;
};

export function SaveStatus({ status }: Props) {
  if (status === 'idle') return null;

  if (status === 'saving') {
    return (
      <span
        role="status"
        aria-label="Opslaan"
        className="text-sm text-fg-muted"
      >
        …
      </span>
    );
  }

  if (status === 'saved') {
    return (
      <span
        role="status"
        aria-label="Opgeslagen"
        className="text-sm text-fg-muted"
      >
        ✓
      </span>
    );
  }

  // error
  return (
    <div
      role="alert"
      className="rounded-md border border-border-strong bg-surface-muted px-3 py-2 text-sm"
    >
      {copy.errors.notSaved}
    </div>
  );
}
