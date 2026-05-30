'use client';

// NoteField — optional free-text note attached to the day's entry. Save
// semantics differ from the wheel:
//   - typing settles for 1.5s before firing PUT (user is still composing)
//   - blur flushes any pending change immediately ("I closed the tab and lost
//     the note" is the trap we're avoiding)
//   - empty / whitespace input normalises to null at the wire boundary
//     (matches domain normalizeNote)
//
// The hook's own 500ms generic debounce coalesces calls; we layer the
// note-specific 1.5s on top because typing-speed is a different time scale
// than tap-bursts on the wheel.

import { useEffect, useRef, useState } from 'react';
import { useReportSaveStatus } from '@/components/save-status-context';
import { copy } from '@/copy';
import { useDayEntryUpsert } from '@/hooks/use-day-entry-upsert';
import { MAX_NOTE_LENGTH } from '@/lib/domain/note';

const TYPING_SETTLE_MS = 1500;

type Props = {
  date: string;
  initialNote: string | null;
  disabled: boolean;
};

export function NoteField({ date, initialNote, disabled }: Props) {
  const [value, setValue] = useState<string>(initialNote ?? '');
  const lastSavedRef = useRef<string | null>(initialNote);
  const settleTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const { save, status, lastError } = useDayEntryUpsert(date);
  useReportSaveStatus('note', status, lastError);

  useEffect(() => {
    return () => {
      if (settleTimerRef.current !== null) clearTimeout(settleTimerRef.current);
    };
  }, []);

  function normalize(input: string): string | null {
    const trimmed = input.trim();
    return trimmed.length === 0 ? null : trimmed;
  }

  function flush(): void {
    if (settleTimerRef.current !== null) {
      clearTimeout(settleTimerRef.current);
      settleTimerRef.current = null;
    }
    const next = normalize(value);
    if (next === lastSavedRef.current) return;
    lastSavedRef.current = next;
    void save({ note: next }, { flush: true });
  }

  function onChange(e: React.ChangeEvent<HTMLTextAreaElement>): void {
    setValue(e.target.value);
    if (settleTimerRef.current !== null) {
      clearTimeout(settleTimerRef.current);
    }
    settleTimerRef.current = setTimeout(() => {
      settleTimerRef.current = null;
      const next = normalize(e.target.value);
      if (next === lastSavedRef.current) return;
      lastSavedRef.current = next;
      void save({ note: next }, { flush: true });
    }, TYPING_SETTLE_MS);
  }

  return (
    // h-full so the label fills its parent layer; the textarea then
    // grows to fill the remaining space below the label. Replaces the
    // prior layout where rows={3} + no flex caused the textarea to
    // float at the top of the layer with a large empty area below.
    <label className="flex h-full flex-col gap-1 text-sm font-medium text-fg-muted">
      {copy.daily.note.label}
      <textarea
        value={value}
        onChange={onChange}
        onBlur={flush}
        disabled={disabled}
        placeholder={copy.daily.note.placeholder}
        rows={3}
        // Soft client-side cap mirroring the server-side normalizeNote
        // boundary. Browsers refuse paste/type past this; the route
        // handler still rejects an oversized note as a defense-in-depth
        // backstop if the client is bypassed.
        maxLength={MAX_NOTE_LENGTH}
        className="min-h-24 flex-1 rounded-md border border-border bg-bg p-3 text-base text-fg placeholder:text-fg-muted focus-visible:outline-2 focus-visible:outline-accent disabled:opacity-60"
      />
    </label>
  );
}
