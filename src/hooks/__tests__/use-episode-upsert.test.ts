// @vitest-environment jsdom
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, renderHook, waitFor } from '@testing-library/react';

// Mock next/navigation so we can assert router.refresh() fires on
// successful mutations. The single invalidation primitive — same
// pattern as useDayEntryUpsert.
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

import { useEpisodeUpsert } from '../use-episode-upsert';

function mockFetch(response: {
  status?: number;
  ok?: boolean;
  body?: unknown;
}) {
  const fn = vi.fn().mockResolvedValue({
    ok: response.ok ?? (response.status !== undefined ? response.status < 400 : true),
    status: response.status ?? 200,
    json: async () => response.body ?? {},
  });
  vi.stubGlobal('fetch', fn);
  return fn;
}

const HAPPY_EPISODE = {
  id: 'ep-01HQ',
  label: 'Coaching met Sarah',
  category: 'interventie' as const,
  start_date: '2026-04-01',
  end_date: null,
  description: null,
  calendar_binding: null,
  archived_at: null,
  created_at: '2026-04-01T08:00:00.000Z',
  updated_at: '2026-04-01T08:00:00.000Z',
};

describe('useEpisodeUpsert', () => {
  beforeEach(() => {
    routerMocks.refresh.mockClear();
  });
  afterEach(() => {
    vi.unstubAllGlobals();
    cleanup();
  });

  // -------------------------------------------------------------------------
  // create
  // -------------------------------------------------------------------------

  describe('create', () => {
    it('POSTs to /api/episodes with the input body and Content-Type application/json', async () => {
      const fetchMock = mockFetch({ status: 200, body: { episode: HAPPY_EPISODE } });
      const { result } = renderHook(() => useEpisodeUpsert());

      await act(async () => {
        await result.current.create({
          label: 'Coaching met Sarah',
          category: 'interventie',
          start_date: '2026-04-01',
        });
      });

      expect(fetchMock).toHaveBeenCalledTimes(1);
      const [url, init] = fetchMock.mock.calls[0]!;
      expect(url).toBe('/api/episodes');
      expect((init as RequestInit).method).toBe('POST');
      const headers = (init as RequestInit).headers as Record<string, string>;
      expect(headers['Content-Type']).toBe('application/json');
      const body = JSON.parse((init as RequestInit).body as string);
      expect(body).toEqual({
        label: 'Coaching met Sarah',
        category: 'interventie',
        start_date: '2026-04-01',
      });
    });

    it('on 200 returns the episode and calls router.refresh()', async () => {
      mockFetch({ status: 200, body: { episode: HAPPY_EPISODE } });
      const { result } = renderHook(() => useEpisodeUpsert());

      let returned;
      await act(async () => {
        returned = await result.current.create({
          label: 'Coaching met Sarah',
          category: 'interventie',
          start_date: '2026-04-01',
        });
      });

      expect(returned).toEqual(HAPPY_EPISODE);
      await waitFor(() => expect(result.current.status).toBe('saved'));
      expect(routerMocks.refresh).toHaveBeenCalledTimes(1);
    });

    it('on 400 invalid_label returns null, sets status=error with the error variant, and does NOT call router.refresh()', async () => {
      mockFetch({ status: 400, body: { error: 'invalid_label' } });
      const { result } = renderHook(() => useEpisodeUpsert());

      let returned;
      await act(async () => {
        returned = await result.current.create({
          label: '',
          category: 'interventie',
          start_date: '2026-04-01',
        });
      });

      expect(returned).toBeNull();
      await waitFor(() => expect(result.current.status).toBe('error'));
      expect(result.current.lastError).toBe('invalid_label');
      expect(routerMocks.refresh).not.toHaveBeenCalled();
    });

    it('on 502 server_error returns null and surfaces the error variant', async () => {
      mockFetch({ status: 502, body: { error: 'server_error' } });
      const { result } = renderHook(() => useEpisodeUpsert());

      let returned;
      await act(async () => {
        returned = await result.current.create({
          label: 'x',
          category: 'interventie',
          start_date: '2026-04-01',
        });
      });

      expect(returned).toBeNull();
      expect(result.current.lastError).toBe('server_error');
    });
  });

  // -------------------------------------------------------------------------
  // update
  // -------------------------------------------------------------------------

  describe('update', () => {
    it('PATCHes to /api/episodes/[id] with the patch body', async () => {
      const fetchMock = mockFetch({ status: 200, body: { episode: HAPPY_EPISODE } });
      const { result } = renderHook(() => useEpisodeUpsert());

      await act(async () => {
        await result.current.update('ep-01HQ', { description: 'updated' });
      });

      expect(fetchMock).toHaveBeenCalledTimes(1);
      const [url, init] = fetchMock.mock.calls[0]!;
      expect(url).toBe('/api/episodes/ep-01HQ');
      expect((init as RequestInit).method).toBe('PATCH');
      const body = JSON.parse((init as RequestInit).body as string);
      expect(body).toEqual({ description: 'updated' });
    });

    it('on 200 returns the updated episode and calls router.refresh()', async () => {
      const updated = { ...HAPPY_EPISODE, description: 'updated' };
      mockFetch({ status: 200, body: { episode: updated } });
      const { result } = renderHook(() => useEpisodeUpsert());

      let returned;
      await act(async () => {
        returned = await result.current.update('ep-01HQ', { description: 'updated' });
      });

      expect(returned).toEqual(updated);
      expect(routerMocks.refresh).toHaveBeenCalledTimes(1);
    });

    it('on 404 not_found returns null with lastError=not_found', async () => {
      mockFetch({ status: 404, body: { error: 'not_found' } });
      const { result } = renderHook(() => useEpisodeUpsert());

      let returned;
      await act(async () => {
        returned = await result.current.update('ep-missing', { label: 'x' });
      });

      expect(returned).toBeNull();
      await waitFor(() => expect(result.current.status).toBe('error'));
      expect(result.current.lastError).toBe('not_found');
      expect(routerMocks.refresh).not.toHaveBeenCalled();
    });
  });

  // -------------------------------------------------------------------------
  // archive
  // -------------------------------------------------------------------------

  describe('archive', () => {
    it('PATCHes archived_at with an ISO timestamp', async () => {
      const archived = { ...HAPPY_EPISODE, archived_at: '2026-06-02T12:00:00.000Z' };
      const fetchMock = mockFetch({ status: 200, body: { episode: archived } });
      const { result } = renderHook(() => useEpisodeUpsert());

      await act(async () => {
        await result.current.archive('ep-01HQ');
      });

      expect(fetchMock).toHaveBeenCalledTimes(1);
      const [url, init] = fetchMock.mock.calls[0]!;
      expect(url).toBe('/api/episodes/ep-01HQ');
      expect((init as RequestInit).method).toBe('PATCH');
      const body = JSON.parse((init as RequestInit).body as string) as { archived_at?: string };
      // archived_at is an ISO UTC timestamp string.
      expect(typeof body.archived_at).toBe('string');
      expect(body.archived_at).toMatch(
        /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/,
      );
    });

    it('on 200 returns the archived episode and calls router.refresh()', async () => {
      const archived = { ...HAPPY_EPISODE, archived_at: '2026-06-02T12:00:00.000Z' };
      mockFetch({ status: 200, body: { episode: archived } });
      const { result } = renderHook(() => useEpisodeUpsert());

      let returned;
      await act(async () => {
        returned = await result.current.archive('ep-01HQ');
      });

      expect(returned).toEqual(archived);
      expect(routerMocks.refresh).toHaveBeenCalledTimes(1);
    });
  });

  // -------------------------------------------------------------------------
  // status machine
  // -------------------------------------------------------------------------

  describe('status', () => {
    it('starts at idle before the first mutation', () => {
      mockFetch({ status: 200, body: { episode: HAPPY_EPISODE } });
      const { result } = renderHook(() => useEpisodeUpsert());

      expect(result.current.status).toBe('idle');
      expect(result.current.lastError).toBeNull();
    });

    it('transitions to "saving" while a create is in flight, then "saved" on success', async () => {
      mockFetch({ status: 200, body: { episode: HAPPY_EPISODE } });
      const { result } = renderHook(() => useEpisodeUpsert());

      let createPromise: Promise<unknown> | undefined;
      act(() => {
        createPromise = result.current.create({
          label: 'x',
          category: 'interventie',
          start_date: '2026-04-01',
        });
      });
      // Mid-flight: status should be 'saving'. The mocked fetch resolves
      // asynchronously, so React state updates a microtask later.
      await waitFor(() => expect(result.current.status).toBe('saving'));
      await act(async () => {
        await createPromise;
      });
      await waitFor(() => expect(result.current.status).toBe('saved'));
    });

    it('lastError is cleared on a subsequent successful save', async () => {
      // First call errors.
      mockFetch({ status: 400, body: { error: 'invalid_label' } });
      const { result } = renderHook(() => useEpisodeUpsert());
      await act(async () => {
        await result.current.create({
          label: '',
          category: 'interventie',
          start_date: '2026-04-01',
        });
      });
      expect(result.current.lastError).toBe('invalid_label');

      // Second call succeeds.
      mockFetch({ status: 200, body: { episode: HAPPY_EPISODE } });
      await act(async () => {
        await result.current.create({
          label: 'fine',
          category: 'interventie',
          start_date: '2026-04-01',
        });
      });

      expect(result.current.status).toBe('saved');
      expect(result.current.lastError).toBeNull();
    });
  });
});
