'use client';

// Shared hook for every component that mutates a day_entry. Encapsulates:
//   - debounce-coalesce: rapid saves within 500ms merge into one PUT
//   - flush option: bypass debounce when the caller wants immediate save
//   - AbortController: in-flight cancel when a new save supersedes
//   - status / lastError state for components to revert / display
//   - cleanup on unmount: pending requests aborted
//
// Per the daily-entry README architecture section, every component that
// mutates a day_entry calls this — wheel (Step 4), note + tags (Step 5),
// timeline bottom sheet (Step 6). One source of truth for save semantics.

import { useCallback, useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import type { DayEntryPatch } from '@/lib/api/day-entries';

export type SaveStatus = 'idle' | 'saving' | 'saved' | 'error';

const SETTLE_MS = 500;

type SaveOptions = { flush?: boolean };

export function useDayEntryUpsert(date: string) {
  const [status, setStatus] = useState<SaveStatus>('idle');
  const [lastError, setLastError] = useState<string | null>(null);
  const router = useRouter();

  const abortRef = useRef<AbortController | null>(null);
  const settleTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pendingPatchRef = useRef<Partial<DayEntryPatch>>({});
  const mountedRef = useRef(true);

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
      abortRef.current?.abort();
      if (settleTimerRef.current !== null) clearTimeout(settleTimerRef.current);
    };
  }, []);

  const fire = useCallback(async (): Promise<void> => {
    const patch = pendingPatchRef.current;
    pendingPatchRef.current = {};

    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setStatus('saving');
    setLastError(null);

    try {
      const res = await fetch(`/api/day-entries/${date}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(patch),
        signal: controller.signal,
      });
      if (!mountedRef.current) return;
      if (!res.ok) {
        let errCode = `http_${res.status}`;
        try {
          const data = (await res.json()) as { error?: unknown };
          if (typeof data.error === 'string') errCode = data.error;
        } catch {
          // ignore body parse failures; keep the http_XXX code
        }
        if (!mountedRef.current) return;
        setStatus('error');
        setLastError(errCode);
        return;
      }
      setStatus('saved');
      // Invalidate the current route's server-rendered data. The single
      // source-of-truth pattern: every mutation triggers a server re-run;
      // components read from props and never shadow with useState.
      router.refresh();
    } catch (e) {
      if (!mountedRef.current) return;
      if (e instanceof Error && e.name === 'AbortError') return;
      setStatus('error');
      setLastError(e instanceof Error ? e.message : 'unknown');
    }
  }, [date, router]);

  const save = useCallback(
    async (patch: Partial<DayEntryPatch>, opts: SaveOptions = {}): Promise<void> => {
      pendingPatchRef.current = { ...pendingPatchRef.current, ...patch };

      if (settleTimerRef.current !== null) {
        clearTimeout(settleTimerRef.current);
        settleTimerRef.current = null;
      }

      if (opts.flush) {
        await fire();
        return;
      }

      settleTimerRef.current = setTimeout(() => {
        settleTimerRef.current = null;
        void fire();
      }, SETTLE_MS);
    },
    [fire],
  );

  return { save, status, lastError };
}
