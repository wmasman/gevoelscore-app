import { beforeEach, describe, expect, it, vi } from 'vitest';
import { getValidatedSession } from '../get-validated-session';
import type { SessionData } from '../session';

describe('getValidatedSession', () => {
  // Build a fresh in-test fake store for each case.
  function makeStore(initial: Record<string, SessionData> = {}) {
    const entries = new Map<string, SessionData>(Object.entries(initial));
    return {
      peek: vi.fn(async (id: string) => entries.get(id)),
      update: vi.fn(async (id: string, data: SessionData) => {
        if (!entries.has(id)) return false;
        entries.set(id, data);
        return true;
      }),
      delete: vi.fn(async (id: string) => {
        entries.delete(id);
      }),
      _entries: entries,
    };
  }

  const aliveSession: SessionData = {
    accessToken: 'at-old',
    refreshToken: 'rt-old',
    expiresAt: 2_000_000,
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('returns the session unchanged when the access token is still alive', async () => {
    const store = makeStore({ 's-1': aliveSession });
    const refresh = vi.fn();

    const result = await getValidatedSession('s-1', {
      store,
      refresh,
      now: () => 1_500_000, // before expiresAt
    });

    expect(result).toEqual(aliveSession);
    expect(refresh).not.toHaveBeenCalled();
    expect(store.update).not.toHaveBeenCalled();
    expect(store.delete).not.toHaveBeenCalled();
  });

  it('refreshes when expired + refresh succeeds; updates the store; returns new tokens', async () => {
    const expired: SessionData = {
      accessToken: 'at-old',
      refreshToken: 'rt-old',
      expiresAt: 1_000_000,
    };
    const store = makeStore({ 's-1': expired });
    const refresh = vi.fn().mockResolvedValue({
      ok: true,
      value: { accessToken: 'at-new', refreshToken: 'rt-new', expiresInMs: 900_000 },
    });

    const result = await getValidatedSession('s-1', {
      store,
      refresh,
      now: () => 2_000_000, // past expiresAt
    });

    expect(refresh).toHaveBeenCalledWith('rt-old');
    expect(result).toEqual({
      accessToken: 'at-new',
      refreshToken: 'rt-new',
      expiresAt: 2_000_000 + 900_000,
    });
    expect(store.update).toHaveBeenCalledWith('s-1', result);
    expect(store.delete).not.toHaveBeenCalled();
  });

  it('returns null and evicts the session when refresh fails', async () => {
    const expired: SessionData = {
      accessToken: 'at-old',
      refreshToken: 'rt-revoked',
      expiresAt: 1_000_000,
    };
    const store = makeStore({ 's-1': expired });
    const refresh = vi.fn().mockResolvedValue({ ok: false, error: 'invalid_refresh_token' });

    const result = await getValidatedSession('s-1', {
      store,
      refresh,
      now: () => 2_000_000,
    });

    expect(result).toBeNull();
    expect(store.delete).toHaveBeenCalledWith('s-1');
    expect(store.update).not.toHaveBeenCalled();
  });

  it('returns null for an unknown session id WITHOUT attempting refresh', async () => {
    const store = makeStore();
    const refresh = vi.fn();

    const result = await getValidatedSession('does-not-exist', { store, refresh });

    expect(result).toBeNull();
    expect(refresh).not.toHaveBeenCalled();
    expect(store.delete).not.toHaveBeenCalled();
  });

  it('on network_error during refresh, returns null but PRESERVES the session — next request retries', async () => {
    // Why: a transient Directus blip (deploy, brief outage) used to
    // permanently destroy the session. The user got logged out for
    // a 50ms hiccup. Network errors are explicitly transient — the
    // refresh token may still be valid. Don't evict.
    const expired: SessionData = {
      accessToken: 'at-old',
      refreshToken: 'rt-still-valid',
      expiresAt: 1_000_000,
    };
    const store = makeStore({ 's-net': expired });
    const refresh = vi.fn().mockResolvedValue({ ok: false, error: 'network_error' });

    const result = await getValidatedSession('s-net', {
      store,
      refresh,
      now: () => 2_000_000,
    });

    expect(result).toBeNull();
    expect(store.delete).not.toHaveBeenCalled();
    // Session row is still there with the original tokens.
    expect(store._entries.get('s-net')).toEqual(expired);
  });

  it('on directus_error during refresh, returns null but PRESERVES the session — also transient', async () => {
    const expired: SessionData = {
      accessToken: 'at-old',
      refreshToken: 'rt-still-valid',
      expiresAt: 1_000_000,
    };
    const store = makeStore({ 's-glitch': expired });
    const refresh = vi.fn().mockResolvedValue({ ok: false, error: 'directus_error' });

    const result = await getValidatedSession('s-glitch', {
      store,
      refresh,
      now: () => 2_000_000,
    });

    expect(result).toBeNull();
    expect(store.delete).not.toHaveBeenCalled();
    expect(store._entries.get('s-glitch')).toEqual(expired);
  });

  it('coalesces parallel refreshes for the same session — refresh fires ONCE, both callers receive the new tokens', async () => {
    // Why: two requests hitting an expired access token at the same
    // moment used to BOTH call refresh with the same refresh token.
    // Directus consumes refresh tokens on use, so the second call
    // got invalid_refresh_token and the session was deleted out from
    // under both users. The per-session refresh lock collapses the
    // burst into one Directus call.
    const expired: SessionData = {
      accessToken: 'at-old',
      refreshToken: 'rt-old',
      expiresAt: 1_000_000,
    };
    const store = makeStore({ 's-race': expired });

    let resolveRefresh: (v: unknown) => void = () => {};
    const refresh = vi.fn().mockReturnValue(
      new Promise((resolve) => {
        resolveRefresh = resolve;
      }),
    );

    const p1 = getValidatedSession('s-race', {
      store,
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      refresh: refresh as any,
      now: () => 2_000_000,
    });
    const p2 = getValidatedSession('s-race', {
      store,
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      refresh: refresh as any,
      now: () => 2_000_000,
    });

    // Microtask yield so both calls have hit the lock check.
    await Promise.resolve();
    await Promise.resolve();
    expect(refresh).toHaveBeenCalledTimes(1);

    resolveRefresh({
      ok: true,
      value: { accessToken: 'at-new', refreshToken: 'rt-new', expiresInMs: 900_000 },
    });

    const [r1, r2] = await Promise.all([p1, p2]);
    const expected = {
      accessToken: 'at-new',
      refreshToken: 'rt-new',
      expiresAt: 2_000_000 + 900_000,
    };
    expect(r1).toEqual(expected);
    expect(r2).toEqual(expected);
    // store.update should also only fire once across both callers.
    expect(store.update).toHaveBeenCalledTimes(1);
  });
});
