'use client';

// useTagManage — v1.5b tag-management Settings hook.
//
// Six methods, all return a Promise resolving to the resulting Tag (or
// `null` for hardDelete and on error). Each triggers router.refresh()
// on success so the server-rendered tag list updates without a client
// cache shadow. AbortController supersede semantics mirror the other
// upsert hooks — rapid back-to-back calls cancel earlier in-flight
// requests rather than racing.
//
//   rename(tagId, label)               → PATCH { label }
//   recategorize(tagId, category)      → PATCH { category }
//   setArchived(tagId, archived_at)    → PATCH { archived_at }   (null = un-archive)
//   reparent(tagId, parent_episode_id) → PATCH { parent_episode_id }
//   hardDelete(tagId)                  → DELETE /api/tags/[tagId]
//   save(tagId, patch)                 → ONE PATCH with all changed keys

import { useCallback, useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import type { Tag } from '@/lib/domain/tag';
import type { TagCategory } from '@/lib/domain/tag-category';

export type TagManageStatus = 'idle' | 'saving' | 'saved' | 'error';

export type TagManagePatch = {
  label?: string;
  category?: TagCategory;
  archived_at?: string | null;
  parent_episode_id?: string | null;
};

export function useTagManage() {
  const [status, setStatus] = useState<TagManageStatus>('idle');
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

  // fire — common path for PATCH and DELETE. Returns parsed body on
  // success, null on error or abort. PATCH returns the updated tag;
  // DELETE returns { deleted_id }. Either way the hook publishes the
  // status + lastError.
  const fire = useCallback(
    async <T,>(
      url: string,
      method: 'PATCH' | 'DELETE' | 'POST',
      body: unknown | null,
    ): Promise<T | null> => {
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      setStatus('saving');
      setLastError(null);

      try {
        const init: RequestInit = {
          method,
          headers:
            body !== null ? { 'Content-Type': 'application/json' } : {},
          signal: controller.signal,
        };
        if (body !== null) init.body = JSON.stringify(body);
        const res = await fetch(url, init);
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
        const data = (await res.json()) as T;
        if (!mountedRef.current) return null;
        setStatus('saved');
        router.refresh();
        return data;
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

  const patch = useCallback(
    async (tagId: string, body: TagManagePatch): Promise<Tag | null> => {
      const data = await fire<{ tag?: Tag }>(`/api/tags/${tagId}`, 'PATCH', body);
      return data?.tag ?? null;
    },
    [fire],
  );

  const rename = useCallback(
    (tagId: string, label: string): Promise<Tag | null> =>
      patch(tagId, { label }),
    [patch],
  );

  const recategorize = useCallback(
    (tagId: string, category: TagCategory): Promise<Tag | null> =>
      patch(tagId, { category }),
    [patch],
  );

  const setArchived = useCallback(
    (tagId: string, archived_at: string | null): Promise<Tag | null> =>
      patch(tagId, { archived_at }),
    [patch],
  );

  const reparent = useCallback(
    (tagId: string, parent_episode_id: string | null): Promise<Tag | null> =>
      patch(tagId, { parent_episode_id }),
    [patch],
  );

  const save = useCallback(
    (tagId: string, body: TagManagePatch): Promise<Tag | null> =>
      patch(tagId, body),
    [patch],
  );

  const hardDelete = useCallback(
    async (tagId: string): Promise<{ deleted_id: string } | null> => {
      const data = await fire<{ deleted_id?: string }>(
        `/api/tags/${tagId}`,
        'DELETE',
        null,
      );
      return data?.deleted_id ? { deleted_id: data.deleted_id } : null;
    },
    [fire],
  );

  const merge = useCallback(
    async (
      sourceId: string,
      targetId: string,
    ): Promise<MergeOutcome | null> => {
      const data = await fire<MergeOutcome>(
        `/api/tags/${sourceId}/merge`,
        'POST',
        { target_tag_id: targetId },
      );
      return data ?? null;
    },
    [fire],
  );

  return {
    rename,
    recategorize,
    setArchived,
    reparent,
    save,
    hardDelete,
    merge,
    status,
    lastError,
  };
}

export type MergeOutcome = {
  source_id: string;
  target_id: string;
  affected_days: number;
};
