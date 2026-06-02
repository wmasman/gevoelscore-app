'use client';

// Mutation hook for tag-to-episode linking (step-5). Three explicit-save
// methods, each fires immediately and returns the resulting Tag (or null):
//   createWithParent(input)       → POST /api/tags (inline create + link in
//                                   one round-trip)
//   link(tagId, episodeId)        → PATCH /api/tags/[tagId] with parent set
//   unlink(tagId)                 → PATCH /api/tags/[tagId] with null parent
//
// router.refresh() on success — single invalidation primitive, mirroring
// useEpisodeUpsert + useDayEntryUpsert. AbortController supersedes previous
// in-flight calls (rapid tapping in the picker is graceful, not racy).

import { useCallback, useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import type { TagCategory } from '@/lib/domain/tag-category';
import type { Tag } from '@/lib/domain/tag';

export type TagLinkUpsertStatus = 'idle' | 'saving' | 'saved' | 'error';

export type CreateWithParentInput = {
  label: string;
  category: TagCategory;
  parent_episode_id: string;
};

export function useTagLinkUpsert() {
  const [status, setStatus] = useState<TagLinkUpsertStatus>('idle');
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

  const fire = useCallback(
    async (
      url: string,
      method: 'POST' | 'PATCH',
      body: unknown,
    ): Promise<Tag | null> => {
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
            // body parse failed — keep the http_XXX code
          }
          if (!mountedRef.current) return null;
          setStatus('error');
          setLastError(errCode);
          return null;
        }
        const data = (await res.json()) as { tag?: Tag };
        if (!mountedRef.current) return null;
        setStatus('saved');
        router.refresh();
        return data.tag ?? null;
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

  const createWithParent = useCallback(
    (input: CreateWithParentInput): Promise<Tag | null> => {
      return fire('/api/tags', 'POST', input);
    },
    [fire],
  );

  const link = useCallback(
    (tagId: string, episodeId: string): Promise<Tag | null> => {
      return fire(`/api/tags/${tagId}`, 'PATCH', {
        parent_episode_id: episodeId,
      });
    },
    [fire],
  );

  const unlink = useCallback(
    (tagId: string): Promise<Tag | null> => {
      return fire(`/api/tags/${tagId}`, 'PATCH', { parent_episode_id: null });
    },
    [fire],
  );

  return { createWithParent, link, unlink, status, lastError };
}
