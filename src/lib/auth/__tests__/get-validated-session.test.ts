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
});
