// @vitest-environment jsdom
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, renderHook, waitFor } from '@testing-library/react';

// Mocked next/navigation router. We want to assert that successful saves
// invalidate server-rendered data via router.refresh() — the single
// invalidation primitive for the app per the data architecture pass.
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

import { useDayEntryUpsert } from '../use-day-entry-upsert';

function mockFetch(response: { status?: number; ok?: boolean; body?: unknown }) {
  const fn = vi.fn().mockResolvedValue({
    ok: response.ok ?? (response.status !== undefined ? response.status < 400 : true),
    status: response.status ?? 200,
    json: async () => response.body ?? {},
  });
  vi.stubGlobal('fetch', fn);
  return fn;
}

describe('useDayEntryUpsert', () => {
  beforeEach(() => {
    routerMocks.refresh.mockClear();
  });
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
    cleanup();
  });

  it('on successful save, calls router.refresh() so server-fetched props re-flow without a manual GET', async () => {
    mockFetch({ status: 200 });
    const { result } = renderHook(() => useDayEntryUpsert('2026-05-28'));

    await act(async () => {
      await result.current.save({ score: 7 }, { flush: true });
    });
    await waitFor(() => expect(result.current.status).toBe('saved'));

    expect(routerMocks.refresh).toHaveBeenCalledTimes(1);
  });

  it('on error response, does NOT call router.refresh() — only successful writes invalidate', async () => {
    mockFetch({ status: 502, body: { error: 'server_error' } });
    const { result } = renderHook(() => useDayEntryUpsert('2026-05-28'));

    await act(async () => {
      await result.current.save({ score: 7 }, { flush: true });
    });
    await waitFor(() => expect(result.current.status).toBe('error'));

    expect(routerMocks.refresh).not.toHaveBeenCalled();
  });

  it('save with patch (debounced) fires PUT to /api/day-entries/[date] with the patch body', async () => {
    vi.useFakeTimers();
    const fetchMock = mockFetch({ status: 200, body: { entry: { score: 7 } } });
    const { result } = renderHook(() => useDayEntryUpsert('2026-05-28'));

    await act(async () => {
      await result.current.save({ score: 7 });
    });
    // Hook debounces 500ms before firing.
    await act(async () => {
      await vi.advanceTimersByTimeAsync(500);
    });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [url, init] = fetchMock.mock.calls[0]!;
    expect(url).toBe('/api/day-entries/2026-05-28');
    expect((init as RequestInit).method).toBe('PUT');
    expect(JSON.parse((init as RequestInit).body as string)).toEqual({ score: 7 });
  });

  it('flush=true fires immediately, bypassing the settle debounce', async () => {
    const fetchMock = mockFetch({ status: 200 });
    const { result } = renderHook(() => useDayEntryUpsert('2026-05-28'));

    await act(async () => {
      await result.current.save({ score: 3 }, { flush: true });
    });

    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('rapid save calls (3 within 200ms) coalesce to one PUT with merged final patch', async () => {
    vi.useFakeTimers();
    const fetchMock = mockFetch({ status: 200 });
    const { result } = renderHook(() => useDayEntryUpsert('2026-05-28'));

    await act(async () => {
      await result.current.save({ score: 4 });
      await vi.advanceTimersByTimeAsync(100);
      await result.current.save({ score: 5 });
      await vi.advanceTimersByTimeAsync(100);
      await result.current.save({ score: 6 });
    });
    await act(async () => {
      await vi.advanceTimersByTimeAsync(500);
    });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [, init] = fetchMock.mock.calls[0]!;
    expect(JSON.parse((init as RequestInit).body as string)).toEqual({ score: 6 });
  });

  it('200 response → status saved; lastError null', async () => {
    mockFetch({ status: 200 });
    const { result } = renderHook(() => useDayEntryUpsert('2026-05-28'));

    await act(async () => {
      await result.current.save({ score: 7 }, { flush: true });
    });
    await waitFor(() => expect(result.current.status).toBe('saved'));
    expect(result.current.lastError).toBeNull();
  });

  it('500 response → status error; lastError populated', async () => {
    mockFetch({ status: 502, body: { error: 'server_error' } });
    const { result } = renderHook(() => useDayEntryUpsert('2026-05-28'));

    await act(async () => {
      await result.current.save({ score: 7 }, { flush: true });
    });
    await waitFor(() => expect(result.current.status).toBe('error'));
    expect(result.current.lastError).toBe('server_error');
  });

  it('network failure (fetch reject) → status error', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('fetch failed')));
    const { result } = renderHook(() => useDayEntryUpsert('2026-05-28'));

    await act(async () => {
      await result.current.save({ score: 7 }, { flush: true });
    });
    await waitFor(() => expect(result.current.status).toBe('error'));
    expect(result.current.lastError).not.toBeNull();
  });

  it('after error, next save call clears the error and tries again', async () => {
    let firstCall = true;
    const fetchMock = vi.fn().mockImplementation(() => {
      if (firstCall) {
        firstCall = false;
        return Promise.resolve({ ok: false, status: 502, json: async () => ({ error: 'server_error' }) });
      }
      return Promise.resolve({ ok: true, status: 200, json: async () => ({ entry: {} }) });
    });
    vi.stubGlobal('fetch', fetchMock);

    const { result } = renderHook(() => useDayEntryUpsert('2026-05-28'));

    await act(async () => {
      await result.current.save({ score: 7 }, { flush: true });
    });
    await waitFor(() => expect(result.current.status).toBe('error'));

    await act(async () => {
      await result.current.save({ score: 7 }, { flush: true });
    });
    await waitFor(() => expect(result.current.status).toBe('saved'));
    expect(result.current.lastError).toBeNull();
  });

  it('rapid flush=true calls abort the previous in-flight request', async () => {
    let aborts = 0;
    let resolveCount = 0;
    const fetchMock = vi.fn().mockImplementation((_url: string, init: RequestInit) => {
      return new Promise((resolve, reject) => {
        (init.signal as AbortSignal).addEventListener('abort', () => {
          aborts += 1;
          reject(new DOMException('aborted', 'AbortError'));
        });
        // Resolve after a microtask so the abort path can fire first.
        Promise.resolve().then(() => {
          if (!(init.signal as AbortSignal).aborted) {
            resolveCount += 1;
            resolve({ ok: true, status: 200, json: async () => ({}) });
          }
        });
      });
    });
    vi.stubGlobal('fetch', fetchMock);

    const { result } = renderHook(() => useDayEntryUpsert('2026-05-28'));

    // Don't await — first save() never resolves (mock pends until next save aborts it).
    let p1: Promise<void>;
    let p2: Promise<void>;
    await act(async () => {
      p1 = result.current.save({ score: 4 }, { flush: true });
      p2 = result.current.save({ score: 7 }, { flush: true });
      await Promise.allSettled([p1!, p2!]);
    });

    expect(aborts).toBeGreaterThanOrEqual(1);
    expect(resolveCount).toBeGreaterThanOrEqual(1);
    await waitFor(() => expect(result.current.status).toBe('saved'));
  });

  it('component unmount aborts pending request', async () => {
    let aborted = false;
    const fetchMock = vi.fn().mockImplementation((_url: string, init: RequestInit) => {
      return new Promise((_resolve, reject) => {
        (init.signal as AbortSignal).addEventListener('abort', () => {
          aborted = true;
          reject(new DOMException('aborted', 'AbortError'));
        });
      });
    });
    vi.stubGlobal('fetch', fetchMock);

    const { result, unmount } = renderHook(() => useDayEntryUpsert('2026-05-28'));

    // Kick off the save WITHOUT awaiting — the fetch never resolves until
    // unmount aborts it. Awaiting would hang the test.
    await act(async () => {
      void result.current.save({ score: 7 }, { flush: true });
      // Yield once so fetch() is called.
      await Promise.resolve();
    });
    unmount();
    // Yield again so the abort listener fires.
    await new Promise((r) => setTimeout(r, 0));
    expect(aborted).toBe(true);
  });
});
