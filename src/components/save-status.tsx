'use client';

import { copy } from '@/copy';
import type { SaveStatus as SaveStatusValue } from '@/hooks/use-day-entry-upsert';

// One source of truth for the saved/saving/error visual language.
//
// Variants (Step 4b):
//   - 'banner' (default, preserves Step 4 behaviour): renders the inline
//     actionable error message as a role="alert" div. Used inline by Step 5
//     components that own their save status.
//   - 'glyph': single-character status indicator. Used by <TodayShell>'s
//     header to show the wheel's save status at a glance. Saving = `…`,
//     saved = `✓`, error = `⚠` (U+26A0). Error glyph uses the tertiary
//     text color (`text-fg-subtle`) to stay quiet — the actionable retry
//     message lives in a separate banner.
//
// Idle state: renders nothing (avoids visual noise on first paint).

type Variant = 'banner' | 'glyph';

type Props = {
  status: SaveStatusValue;
  // Reserved for a future detailed error view; today the banner uses a
  // single generic Dutch string from copy.errors.notSaved.
  error?: string | null;
  variant?: Variant;
};

export function SaveStatus({ status, variant = 'banner' }: Props) {
  if (status === 'idle') return null;

  if (status === 'saving') {
    return (
      <span
        role="status"
        aria-live="polite"
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
        aria-live="polite"
        aria-label="Opgeslagen"
        className="text-sm text-fg-muted"
      >
        ✓
      </span>
    );
  }

  // error
  if (variant === 'glyph') {
    return (
      <span
        role="status"
        aria-live="polite"
        aria-label="Niet opgeslagen"
        className="text-sm text-fg-subtle"
      >
        ⚠
      </span>
    );
  }

  return (
    <div
      role="alert"
      className="rounded-md border border-border-strong bg-surface-muted px-3 py-2 text-sm"
    >
      {copy.errors.notSaved}
    </div>
  );
}
