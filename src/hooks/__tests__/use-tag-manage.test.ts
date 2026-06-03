// @vitest-environment jsdom
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, renderHook, waitFor } from '@testing-library/react';

const routerMocks = vi.hoisted(() => ({
  refresh: vi.fn(),
  push: vi.fn(),
  replace: vi.fn(),
  back: vi.fn(),
  forward: vi.fn(),
  prefetch: vi.fn(),
}));
vi.mock('next/navigation', () => ({
  useRouter: () => routerMocks,
}));

import { useTagManage } from '../use-tag-manage';

function mockFetch(response: {
  status?: number;
  ok?: boolean;
  body?: unknown;
}) {
  const fn = vi.fn().mockResolvedValue({
    ok:
      response.ok ??
      (response.status !== undefined ? response.status < 400 : true),
    status: response.status ?? 200,
    json: async () => response.body ?? {},
  });
  vi.stubGlobal('fetch', fn);
  return fn;
}

const TAG_ID = '01234567-89ab-cdef-0123-456789abcdef';
const EPISODE_ID = '550e8400-e29b-41d4-a716-446655440000';

const HAPPY_TAG = {
  id: TAG_ID,
  label: 'pacing',
  category: 'mentaal' as const,
  project_id: null,
  parent_episode_id: null,
  usage_count: 3,
  archived_at: null,
  created_at: '2026-06-02T00:00:00.000Z',
};

describe('useTagManage', () => {
  beforeEach(() => {
    routerMocks.refresh.mockClear();
  });
  afterEach(() => {
    vi.unstubAllGlobals();
    cleanup();
  });

  describe('rename', () => {
    it('PATCHes /api/tags/[tagId] with { label } and calls router.refresh', async () => {
      const fetchMock = mockFetch({
        status: 200,
        body: { tag: { ...HAPPY_TAG, label: 'pacing-strategy' } },
      });
      const { result } = renderHook(() => useTagManage());

      await act(async () => {
        await result.current.rename(TAG_ID, 'pacing-strategy');
      });

      expect(fetchMock).toHaveBeenCalledTimes(1);
      const [url, init] = fetchMock.mock.calls[0]!;
      expect(url).toBe(`/api/tags/${TAG_ID}`);
      expect((init as RequestInit).method).toBe('PATCH');
      const body = JSON.parse((init as RequestInit).body as string);
      expect(body).toEqual({ label: 'pacing-strategy' });
      await waitFor(() => expect(routerMocks.refresh).toHaveBeenCalledTimes(1));
    });
  });

  describe('recategorize', () => {
    it('PATCHes with { category } and calls router.refresh', async () => {
      const fetchMock = mockFetch({
        status: 200,
        body: { tag: { ...HAPPY_TAG, category: 'fysiek' } },
      });
      const { result } = renderHook(() => useTagManage());

      await act(async () => {
        await result.current.recategorize(TAG_ID, 'fysiek');
      });

      const body = JSON.parse((fetchMock.mock.calls[0]![1] as RequestInit).body as string);
      expect(body).toEqual({ category: 'fysiek' });
      await waitFor(() => expect(routerMocks.refresh).toHaveBeenCalledTimes(1));
    });
  });

  describe('setArchived', () => {
    it('PATCHes with { archived_at: <ISO> } for archive', async () => {
      const iso = '2026-06-03T10:00:00.000Z';
      const fetchMock = mockFetch({
        status: 200,
        body: { tag: { ...HAPPY_TAG, archived_at: iso } },
      });
      const { result } = renderHook(() => useTagManage());

      await act(async () => {
        await result.current.setArchived(TAG_ID, iso);
      });

      const body = JSON.parse((fetchMock.mock.calls[0]![1] as RequestInit).body as string);
      expect(body).toEqual({ archived_at: iso });
    });

    it('PATCHes with { archived_at: null } for un-archive', async () => {
      const fetchMock = mockFetch({
        status: 200,
        body: { tag: HAPPY_TAG },
      });
      const { result } = renderHook(() => useTagManage());

      await act(async () => {
        await result.current.setArchived(TAG_ID, null);
      });

      const body = JSON.parse((fetchMock.mock.calls[0]![1] as RequestInit).body as string);
      expect(body).toEqual({ archived_at: null });
    });
  });

  describe('reparent', () => {
    it('PATCHes with { parent_episode_id }', async () => {
      const fetchMock = mockFetch({
        status: 200,
        body: { tag: { ...HAPPY_TAG, parent_episode_id: EPISODE_ID } },
      });
      const { result } = renderHook(() => useTagManage());

      await act(async () => {
        await result.current.reparent(TAG_ID, EPISODE_ID);
      });

      const body = JSON.parse((fetchMock.mock.calls[0]![1] as RequestInit).body as string);
      expect(body).toEqual({ parent_episode_id: EPISODE_ID });
    });
  });

  describe('hardDelete', () => {
    it('DELETEs /api/tags/[tagId] and triggers router.refresh on success', async () => {
      const fetchMock = mockFetch({
        status: 200,
        body: { deleted_id: TAG_ID },
      });
      const { result } = renderHook(() => useTagManage());

      let returned;
      await act(async () => {
        returned = await result.current.hardDelete(TAG_ID);
      });

      expect(fetchMock).toHaveBeenCalledTimes(1);
      const [url, init] = fetchMock.mock.calls[0]!;
      expect(url).toBe(`/api/tags/${TAG_ID}`);
      expect((init as RequestInit).method).toBe('DELETE');
      expect(returned).toEqual({ deleted_id: TAG_ID });
      await waitFor(() => expect(routerMocks.refresh).toHaveBeenCalledTimes(1));
    });

    it('returns null on 400 tag_in_use and does NOT call router.refresh', async () => {
      mockFetch({
        status: 400,
        body: { error: 'tag_in_use', usage_count: 5 },
      });
      const { result } = renderHook(() => useTagManage());

      let returned;
      await act(async () => {
        returned = await result.current.hardDelete(TAG_ID);
      });

      expect(returned).toBeNull();
      await waitFor(() => expect(result.current.status).toBe('error'));
      expect(result.current.lastError).toBe('tag_in_use');
      expect(routerMocks.refresh).not.toHaveBeenCalled();
    });
  });

  describe('save (multi-field diff)', () => {
    it('makes ONE PATCH with all three keys', async () => {
      const fetchMock = mockFetch({
        status: 200,
        body: {
          tag: {
            ...HAPPY_TAG,
            label: 'pacing',
            category: 'fysiek',
            parent_episode_id: EPISODE_ID,
          },
        },
      });
      const { result } = renderHook(() => useTagManage());

      await act(async () => {
        await result.current.save(TAG_ID, {
          label: 'pacing',
          category: 'fysiek',
          parent_episode_id: EPISODE_ID,
        });
      });

      expect(fetchMock).toHaveBeenCalledTimes(1);
      const body = JSON.parse((fetchMock.mock.calls[0]![1] as RequestInit).body as string);
      expect(body).toEqual({
        label: 'pacing',
        category: 'fysiek',
        parent_episode_id: EPISODE_ID,
      });
    });
  });

  describe('error surfacing', () => {
    it('per-field error code surfaces in lastError (M1 dividend)', async () => {
      mockFetch({ status: 400, body: { error: 'invalid_label' } });
      const { result } = renderHook(() => useTagManage());

      let returned;
      await act(async () => {
        returned = await result.current.rename(TAG_ID, '');
      });

      expect(returned).toBeNull();
      await waitFor(() => expect(result.current.status).toBe('error'));
      expect(result.current.lastError).toBe('invalid_label');
      expect(routerMocks.refresh).not.toHaveBeenCalled();
    });
  });

  describe('AbortController supersede semantics', () => {
    it('aborts the previous in-flight call when a new one supersedes it', async () => {
      // Same pattern as use-tag-link-upsert + use-episode-upsert.
      const responses = [
        { tag: { ...HAPPY_TAG, label: 'first' } },
        { tag: { ...HAPPY_TAG, label: 'second' } },
      ];
      let call = 0;
      const fetchMock = vi.fn().mockImplementation(async (_url, init) => {
        const signal = (init as RequestInit).signal;
        const body = responses[call];
        call += 1;
        return new Promise((resolve, reject) => {
          const timer = setTimeout(
            () => resolve({ ok: true, status: 200, json: async () => body }),
            10,
          );
          signal?.addEventListener('abort', () => {
            clearTimeout(timer);
            const err = new Error('aborted');
            err.name = 'AbortError';
            reject(err);
          });
        });
      });
      vi.stubGlobal('fetch', fetchMock);

      const { result } = renderHook(() => useTagManage());

      let firstReturn: unknown;
      let secondReturn: unknown;
      await act(async () => {
        const p1 = result.current.rename(TAG_ID, 'first');
        const p2 = result.current.rename(TAG_ID, 'second');
        [firstReturn, secondReturn] = await Promise.all([p1, p2]);
      });

      expect(firstReturn).toBeNull();
      expect((secondReturn as { label: string }).label).toBe('second');
    });
  });

  // -------------------------------------------------------------------------
  // merge — v1.5c. Tests 28-31 from
  // docs/features/tag-merge/step-1-tag-merge.md.
  // -------------------------------------------------------------------------

  describe('merge', () => {
    const SOURCE_ID = TAG_ID;
    const TARGET_ID = '11111111-2222-3333-4444-555555555555';
    const MERGE_PAYLOAD = {
      source_id: SOURCE_ID,
      target_id: TARGET_ID,
      affected_days: 4,
    };

    it('test 28: merge POSTs to /api/tags/[source]/merge with { target_tag_id: target }', async () => {
      const fetchMock = mockFetch({ body: MERGE_PAYLOAD });
      const { result } = renderHook(() => useTagManage());

      await act(async () => {
        await result.current.merge(SOURCE_ID, TARGET_ID);
      });

      expect(fetchMock).toHaveBeenCalledWith(
        `/api/tags/${SOURCE_ID}/merge`,
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ target_tag_id: TARGET_ID }),
        }),
      );
    });

    it('test 29: merge on 200 calls router.refresh and returns the { source_id, target_id, affected_days } payload', async () => {
      mockFetch({ body: MERGE_PAYLOAD });
      const { result } = renderHook(() => useTagManage());

      let returned;
      await act(async () => {
        returned = await result.current.merge(SOURCE_ID, TARGET_ID);
      });

      expect(returned).toEqual(MERGE_PAYLOAD);
      await waitFor(() =>
        expect(routerMocks.refresh).toHaveBeenCalledTimes(1),
      );
    });

    it('test 30: merge on 400 returns null, sets status=error, lastError=code, does NOT call router.refresh', async () => {
      mockFetch({ status: 400, body: { error: 'category_mismatch' } });
      const { result } = renderHook(() => useTagManage());

      let returned;
      await act(async () => {
        returned = await result.current.merge(SOURCE_ID, TARGET_ID);
      });

      expect(returned).toBeNull();
      await waitFor(() => expect(result.current.status).toBe('error'));
      expect(result.current.lastError).toBe('category_mismatch');
      expect(routerMocks.refresh).not.toHaveBeenCalled();
    });

    it('test 31: AbortController supersede — back-to-back merge calls cancel earlier ones', async () => {
      const responses = [
        { ...MERGE_PAYLOAD, affected_days: 1 },
        { ...MERGE_PAYLOAD, affected_days: 2 },
      ];
      let call = 0;
      const fetchMock = vi.fn().mockImplementation(async (_url, init) => {
        const signal = (init as RequestInit).signal;
        const body = responses[call];
        call += 1;
        return new Promise((resolve, reject) => {
          const timer = setTimeout(
            () => resolve({ ok: true, status: 200, json: async () => body }),
            10,
          );
          signal?.addEventListener('abort', () => {
            clearTimeout(timer);
            const err = new Error('aborted');
            err.name = 'AbortError';
            reject(err);
          });
        });
      });
      vi.stubGlobal('fetch', fetchMock);

      const { result } = renderHook(() => useTagManage());

      let firstReturn: unknown;
      let secondReturn: unknown;
      await act(async () => {
        const p1 = result.current.merge(SOURCE_ID, TARGET_ID);
        const p2 = result.current.merge(SOURCE_ID, TARGET_ID);
        [firstReturn, secondReturn] = await Promise.all([p1, p2]);
      });

      expect(firstReturn).toBeNull();
      expect((secondReturn as { affected_days: number }).affected_days).toBe(2);
    });
  });
});
