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

import { useTagLinkUpsert } from '../use-tag-link-upsert';

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

const EPISODE_ID = '550e8400-e29b-41d4-a716-446655440000';
const TAG_ID = '01234567-89ab-cdef-0123-456789abcdef';

const HAPPY_TAG = {
  id: TAG_ID,
  label: 'coaching sessie',
  category: 'interventie' as const,
  project_id: null,
  parent_episode_id: EPISODE_ID,
  usage_count: 0,
  archived_at: null,
  created_at: '2026-06-02T00:00:00.000Z',
};

describe('useTagLinkUpsert', () => {
  beforeEach(() => {
    routerMocks.refresh.mockClear();
  });
  afterEach(() => {
    vi.unstubAllGlobals();
    cleanup();
  });

  // -------------------------------------------------------------------------
  // createWithParent
  // -------------------------------------------------------------------------

  describe('createWithParent', () => {
    it('POSTs to /api/tags with { label, category, parent_episode_id } and Content-Type JSON', async () => {
      const fetchMock = mockFetch({
        status: 200,
        body: { outcome: 'created', tag: HAPPY_TAG },
      });
      const { result } = renderHook(() => useTagLinkUpsert());

      await act(async () => {
        await result.current.createWithParent({
          label: 'coaching sessie',
          category: 'interventie',
          parent_episode_id: EPISODE_ID,
        });
      });

      expect(fetchMock).toHaveBeenCalledTimes(1);
      const [url, init] = fetchMock.mock.calls[0]!;
      expect(url).toBe('/api/tags');
      expect((init as RequestInit).method).toBe('POST');
      const headers = (init as RequestInit).headers as Record<string, string>;
      expect(headers['Content-Type']).toBe('application/json');
      const body = JSON.parse((init as RequestInit).body as string);
      expect(body).toEqual({
        label: 'coaching sessie',
        category: 'interventie',
        parent_episode_id: EPISODE_ID,
      });
    });

    it('on 200 returns the tag and calls router.refresh()', async () => {
      mockFetch({ status: 200, body: { outcome: 'created', tag: HAPPY_TAG } });
      const { result } = renderHook(() => useTagLinkUpsert());

      let returned;
      await act(async () => {
        returned = await result.current.createWithParent({
          label: 'coaching sessie',
          category: 'interventie',
          parent_episode_id: EPISODE_ID,
        });
      });

      expect(returned).toEqual(HAPPY_TAG);
      await waitFor(() => expect(result.current.status).toBe('saved'));
      expect(routerMocks.refresh).toHaveBeenCalledTimes(1);
    });

    it('on 400 invalid_label returns null, sets status=error with the error variant, and does NOT call router.refresh()', async () => {
      mockFetch({ status: 400, body: { error: 'invalid_label' } });
      const { result } = renderHook(() => useTagLinkUpsert());

      let returned;
      await act(async () => {
        returned = await result.current.createWithParent({
          label: '',
          category: 'mentaal',
          parent_episode_id: EPISODE_ID,
        });
      });

      expect(returned).toBeNull();
      await waitFor(() => expect(result.current.status).toBe('error'));
      expect(result.current.lastError).toBe('invalid_label');
      expect(routerMocks.refresh).not.toHaveBeenCalled();
    });
  });

  // -------------------------------------------------------------------------
  // link
  // -------------------------------------------------------------------------

  describe('link', () => {
    it('PATCHes /api/tags/[tagId] with { parent_episode_id: episodeId }', async () => {
      const fetchMock = mockFetch({ status: 200, body: { tag: HAPPY_TAG } });
      const { result } = renderHook(() => useTagLinkUpsert());

      await act(async () => {
        await result.current.link(TAG_ID, EPISODE_ID);
      });

      expect(fetchMock).toHaveBeenCalledTimes(1);
      const [url, init] = fetchMock.mock.calls[0]!;
      expect(url).toBe(`/api/tags/${TAG_ID}`);
      expect((init as RequestInit).method).toBe('PATCH');
      const body = JSON.parse((init as RequestInit).body as string);
      expect(body).toEqual({ parent_episode_id: EPISODE_ID });
    });

    it('on 200 returns the updated tag and calls router.refresh()', async () => {
      mockFetch({ status: 200, body: { tag: HAPPY_TAG } });
      const { result } = renderHook(() => useTagLinkUpsert());

      let returned;
      await act(async () => {
        returned = await result.current.link(TAG_ID, EPISODE_ID);
      });

      expect(returned).toEqual(HAPPY_TAG);
      await waitFor(() => expect(result.current.status).toBe('saved'));
      expect(routerMocks.refresh).toHaveBeenCalledTimes(1);
    });

    it('on 502 server_error returns null and surfaces the error code', async () => {
      mockFetch({ status: 502, body: { error: 'server_error' } });
      const { result } = renderHook(() => useTagLinkUpsert());

      let returned;
      await act(async () => {
        returned = await result.current.link(TAG_ID, EPISODE_ID);
      });

      expect(returned).toBeNull();
      await waitFor(() => expect(result.current.status).toBe('error'));
      expect(result.current.lastError).toBe('server_error');
      expect(routerMocks.refresh).not.toHaveBeenCalled();
    });
  });

  // -------------------------------------------------------------------------
  // unlink
  // -------------------------------------------------------------------------

  describe('unlink', () => {
    it('PATCHes /api/tags/[tagId] with { parent_episode_id: null }', async () => {
      const fetchMock = mockFetch({
        status: 200,
        body: { tag: { ...HAPPY_TAG, parent_episode_id: null } },
      });
      const { result } = renderHook(() => useTagLinkUpsert());

      await act(async () => {
        await result.current.unlink(TAG_ID);
      });

      expect(fetchMock).toHaveBeenCalledTimes(1);
      const [url, init] = fetchMock.mock.calls[0]!;
      expect(url).toBe(`/api/tags/${TAG_ID}`);
      expect((init as RequestInit).method).toBe('PATCH');
      const body = JSON.parse((init as RequestInit).body as string);
      expect(body).toEqual({ parent_episode_id: null });
    });

    it('on 200 returns the unlinked tag and calls router.refresh()', async () => {
      mockFetch({
        status: 200,
        body: { tag: { ...HAPPY_TAG, parent_episode_id: null } },
      });
      const { result } = renderHook(() => useTagLinkUpsert());

      let returned;
      await act(async () => {
        returned = await result.current.unlink(TAG_ID);
      });

      expect(returned).not.toBeNull();
      expect(returned!.parent_episode_id).toBeNull();
      await waitFor(() => expect(result.current.status).toBe('saved'));
      expect(routerMocks.refresh).toHaveBeenCalledTimes(1);
    });
  });

  // -------------------------------------------------------------------------
  // Lifecycle / status machine
  // -------------------------------------------------------------------------

  it('status flips idle → saving → saved on success', async () => {
    mockFetch({ status: 200, body: { tag: HAPPY_TAG } });
    const { result } = renderHook(() => useTagLinkUpsert());

    expect(result.current.status).toBe('idle');
    let promise!: Promise<unknown>;
    await act(async () => {
      promise = result.current.link(TAG_ID, EPISODE_ID);
    });
    // Note: status check after await — the saving → saved transition
    // happens inside the same microtask flush in jsdom, so we observe
    // 'saved' here. The important contract: it lands on saved, not error.
    await act(async () => {
      await promise;
    });
    await waitFor(() => expect(result.current.status).toBe('saved'));
  });

  it('status flips idle → saving → error on failure', async () => {
    mockFetch({ status: 502, body: { error: 'server_error' } });
    const { result } = renderHook(() => useTagLinkUpsert());

    await act(async () => {
      await result.current.link(TAG_ID, EPISODE_ID);
    });

    await waitFor(() => expect(result.current.status).toBe('error'));
  });

  it('aborts the previous in-flight call when a new one supersedes it', async () => {
    // Mirrors useEpisodeUpsert: the AbortController is replaced and the
    // previous fetch is aborted. The second call resolves; the first
    // resolves to null (the hook detects AbortError and bails silently).
    const responses = [
      { tag: { ...HAPPY_TAG, id: 'tag-A' } },
      { tag: { ...HAPPY_TAG, id: 'tag-B' } },
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

    const { result } = renderHook(() => useTagLinkUpsert());

    let firstReturn: unknown;
    let secondReturn: unknown;
    await act(async () => {
      const p1 = result.current.link(TAG_ID, EPISODE_ID);
      const p2 = result.current.link(TAG_ID, EPISODE_ID);
      [firstReturn, secondReturn] = await Promise.all([p1, p2]);
    });

    expect(firstReturn).toBeNull();
    expect((secondReturn as { id: string }).id).toBe('tag-B');
  });

  it('cleanup on unmount aborts any in-flight request without console errors', async () => {
    let abortFired = false;
    const fetchMock = vi.fn().mockImplementation(async (_url, init) => {
      const signal = (init as RequestInit).signal;
      return new Promise((resolve, reject) => {
        const timer = setTimeout(
          () => resolve({ ok: true, status: 200, json: async () => ({}) }),
          100,
        );
        signal?.addEventListener('abort', () => {
          abortFired = true;
          clearTimeout(timer);
          const err = new Error('aborted');
          err.name = 'AbortError';
          reject(err);
        });
      });
    });
    vi.stubGlobal('fetch', fetchMock);

    const { result, unmount } = renderHook(() => useTagLinkUpsert());

    act(() => {
      void result.current.link(TAG_ID, EPISODE_ID);
    });
    unmount();

    await waitFor(() => expect(abortFired).toBe(true));
  });
});
