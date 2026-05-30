'use client';

// SaveAnnouncer — single page-level live region for screen-reader users.
//
// Audit A-H4: the prior SaveStatus rendered three small inline
// indicators each with `role="status"` and a per-state `aria-label`
// that toggled on every cycle, which NVDA/JAWS can announce repeatedly
// during a typing burst. Plus there was no audible confirmation of a
// save landing — only the visual pulse.
//
// This component fixes both by:
//   - Mounting once at the page root, not next to each save source.
//   - Announcing only on the saving → saved | error transition (no
//     "Opslaan" chatter during in-progress saves).
//   - Throttling repeat announcements to one per
//     ANNOUNCE_THROTTLE_MS so a flurry of tag toggles doesn't
//     stutter through several "Opgeslagen" reads.
//   - Clearing the live-region text after CLEAR_MS so a subsequent
//     identical transition re-announces (live regions ignore
//     unchanged text).
//
// Date.now is used for throttling — vi.setSystemTime is the way to
// simulate it in tests; fake timers alone do not affect Date.now.

import { useEffect, useRef, useState } from 'react';
import { useMergedSaveStatus } from '@/components/save-status-context';
import { copy } from '@/copy';

const ANNOUNCE_THROTTLE_MS = 5_000;
const CLEAR_MS = 3_000;

export function SaveAnnouncer() {
  const merged = useMergedSaveStatus();
  const [text, setText] = useState<string>('');
  const prevStatus = useRef<typeof merged.status>('idle');
  const lastAnnouncedAt = useRef<number>(0);
  const clearTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (clearTimer.current !== null) clearTimeout(clearTimer.current);
    };
  }, []);

  useEffect(() => {
    const wasSaving = prevStatus.current === 'saving';
    prevStatus.current = merged.status;
    if (!wasSaving) return;

    const now = Date.now();
    if (now - lastAnnouncedAt.current < ANNOUNCE_THROTTLE_MS) return;

    const message =
      merged.status === 'saved'
        ? copy.announce.saved
        : merged.status === 'error'
          ? copy.announce.notSaved
          : null;
    if (message === null) return;

    lastAnnouncedAt.current = now;
    setText(message);
    if (clearTimer.current !== null) clearTimeout(clearTimer.current);
    clearTimer.current = setTimeout(() => setText(''), CLEAR_MS);
  }, [merged.status]);

  return (
    <div role="status" aria-live="polite" aria-atomic="true" className="sr-only">
      {text}
    </div>
  );
}
