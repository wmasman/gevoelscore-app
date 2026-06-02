'use client';

// Shared hook for every component that mutates an Episode (v1.5 Context
// tab → Periodes section). Encapsulates:
//   - explicit-save semantics: each create / update / archive call fires
//     immediately (no debounce). Periodes are config-style — multi-field
//     decisions — and the form has an explicit Bewaar button.
//   - AbortController: in-flight cancel when a new mutation supersedes.
//   - status / lastError state for components to read.
//   - router.refresh() on success: the single invalidation primitive,
//     matching useDayEntryUpsert.
//   - cleanup on unmount: pending requests aborted.
//
// API:
//   create(input)            → POST /api/episodes
//   update(id, patch)        → PATCH /api/episodes/[id]
//   archive(id)              → PATCH archived_at: now (wraps update)
//
// Each returns the updated Episode on success or null on error. The
// caller reads `status` + `lastError` to surface UI feedback. The
// existing SaveStatusContext + SaveAnnouncer infrastructure picks up
// the status (when wired by the component that uses this hook).

import { useCallback, useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import type { Episode } from '@/lib/domain/episode';

export type EpisodeUpsertStatus = 'idle' | 'saving' | 'saved' | 'error';

export type EpisodeCreateInput = {
  label: string;
  category: 'interventie' | 'levensgebeurtenis';
  start_date: string;
  end_date?: string | null;
  description?: string | null;
};

export type EpisodeUpdatePatch = {
  label?: string;
  category?: 'interventie' | 'levensgebeurtenis';
  start_date?: string;
  end_date?: string | null;
  description?: string | null;
  archived_at?: string | null;
};

export function useEpisodeUpsert() {
  const [status, setStatus] = useState<EpisodeUpsertStatus>('idle');
  const [lastError, setLastError] = useState<string | null>(null);
  const router = useRouter();

  const abortRef = useRef<AbortController | null>(null);
  const mountedRef = useRef(true);

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
      abortRef.current?.abort();
    };
  }, []);

  // Common path for both create and update. Issues the request, manages
  // status, calls router.refresh on success, returns the Episode or null.
  const fire = useCallback(
    async (
      url: string,
      method: 'POST' | 'PATCH',
      body: unknown,
    ): Promise<Episode | null> => {
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      setStatus('saving');
      setLastError(null);

      try {
        const res = await fetch(url, {
          method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
          signal: controller.signal,
        });
        if (!mountedRef.current) return null;
        if (!res.ok) {
          let errCode = `http_${res.status}`;
          try {
            const data = (await res.json()) as { error?: unknown };
            if (typeof data.error === 'string') errCode = data.error;
          } catch {
            // ignore body parse failures; keep the http_XXX code
          }
          if (!mountedRef.current) return null;
          setStatus('error');
          setLastError(errCode);
          return null;
        }
        // Success — parse the body for the returned episode.
        const data = (await res.json()) as { episode?: Episode };
        if (!mountedRef.current) return null;
        setStatus('saved');
        router.refresh();
        return data.episode ?? null;
      } catch (e) {
        if (!mountedRef.current) return null;
        if (e instanceof Error && e.name === 'AbortError') return null;
        setStatus('error');
        setLastError(e instanceof Error ? e.message : 'unknown');
        return null;
      }
    },
    [router],
  );

  const create = useCallback(
    (input: EpisodeCreateInput): Promise<Episode | null> => {
      return fire('/api/episodes', 'POST', input);
    },
    [fire],
  );

  const update = useCallback(
    (id: string, patch: EpisodeUpdatePatch): Promise<Episode | null> => {
      return fire(`/api/episodes/${id}`, 'PATCH', patch);
    },
    [fire],
  );

  const archive = useCallback(
    (id: string): Promise<Episode | null> => {
      // ISO timestamp built at click time. The wrapper's
      // ISO_UTC_TIMESTAMP_REGEX matches the toISOString output.
      return update(id, { archived_at: new Date().toISOString() });
    },
    [update],
  );

  return { create, update, archive, status, lastError };
}
