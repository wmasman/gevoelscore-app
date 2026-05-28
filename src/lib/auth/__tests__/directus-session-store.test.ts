// Unit tests for the Directus-backed SessionStore. The SDK is mocked so we
// can assert behaviour deterministically — the goal is to pin down the
// contract that survives the in-memory ↔ Directus swap, not to test the
// Directus server itself. Integration against a real Directus instance
// lives in tests/e2e/session-persistence.spec.ts.

import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => {
  type Row = {
    id: string;
    access_token: string;
    refresh_token: string;
    expires_at: string;
  };
  const rows = new Map<string, Row>();
  let throwOnNext: { error?: unknown } | null = null;

  function makeNotFoundError() {
    return {
      errors: [{ extensions: { code: 'RECORD_NOT_FOUND' } }],
    };
  }
  function makeForbiddenError() {
    return {
      errors: [{ extensions: { code: 'FORBIDDEN' } }],
    };
  }
  function makeNetworkError() {
    return new TypeError('fetch failed: ECONNREFUSED');
  }

  return {
    rows,
    throwOnNext,
    setThrow(err: unknown) {
      throwOnNext = { error: err };
    },
    makeNotFoundError,
    makeForbiddenError,
    makeNetworkError,
    pollThrow() {
      const t = throwOnNext;
      throwOnNext = null;
      return t;
    },
  };
});

vi.mock('@directus/sdk', () => {
  // Each helper just packages the action into an opaque object — the fake
  // client below interprets these to mutate `mocks.rows`.
  return {
    createDirectus: () => ({
      with: () => ({
        with: () => ({
          async request(action: { kind: string; args?: unknown }) {
            const t = mocks.pollThrow();
            if (t) throw t.error;
            switch (action.kind) {
              case 'createItem': {
                const a = action.args as {
                  collection: string;
                  data: { id: string; access_token: string; refresh_token: string; expires_at: string };
                };
                mocks.rows.set(a.data.id, { ...a.data });
                return { ...a.data };
              }
              case 'readItem': {
                const a = action.args as { collection: string; id: string };
                const row = mocks.rows.get(a.id);
                if (!row) throw mocks.makeNotFoundError();
                return row;
              }
              case 'updateItem': {
                const a = action.args as {
                  collection: string;
                  id: string;
                  data: { access_token: string; refresh_token: string; expires_at: string };
                };
                const row = mocks.rows.get(a.id);
                if (!row) throw mocks.makeNotFoundError();
                mocks.rows.set(a.id, { ...row, ...a.data });
                return { ...row, ...a.data };
              }
              case 'deleteItem': {
                const a = action.args as { collection: string; id: string };
                if (!mocks.rows.has(a.id)) throw mocks.makeNotFoundError();
                mocks.rows.delete(a.id);
                return null;
              }
              case 'readItems': {
                const a = action.args as { collection: string; query?: { filter?: { expires_at?: { _lte?: string } } } };
                const cutoff = a.query?.filter?.expires_at?._lte;
                const all = Array.from(mocks.rows.values());
                if (cutoff) {
                  return all.filter((r) => r.expires_at <= cutoff).map((r) => ({ id: r.id }));
                }
                return all.map((r) => ({ id: r.id }));
              }
              default:
                throw new Error('unhandled action kind: ' + action.kind);
            }
          },
        }),
      }),
    }),
    rest: () => ({}),
    staticToken: () => ({}),
    createItem: (collection: string, data: unknown) => ({
      kind: 'createItem',
      args: { collection, data },
    }),
    readItem: (collection: string, id: string) => ({
      kind: 'readItem',
      args: { collection, id },
    }),
    updateItem: (collection: string, id: string, data: unknown) => ({
      kind: 'updateItem',
      args: { collection, id, data },
    }),
    deleteItem: (collection: string, id: string) => ({
      kind: 'deleteItem',
      args: { collection, id },
    }),
    readItems: (collection: string, query: unknown) => ({
      kind: 'readItems',
      args: { collection, query },
    }),
  };
});

import { createDirectusSessionStore } from '../directus-session-store';

function build() {
  let counter = 0;
  return createDirectusSessionStore({
    directusUrl: 'https://example.directus.test',
    adminToken: 'admin-token',
    idGenerator: () => `id-${++counter}`,
    now: () => 1_000_000,
  });
}

describe('createDirectusSessionStore', () => {
  beforeEach(() => {
    mocks.rows.clear();
  });

  it('create + peek round-trip preserves the session payload', async () => {
    const store = build();
    const id = await store.create({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: 1_900_000,
    });
    expect(id).toBe('id-1');

    const peeked = await store.peek(id);
    expect(peeked).toEqual({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: 1_900_000,
    });
  });

  it('peek returns undefined for an unknown id (RECORD_NOT_FOUND)', async () => {
    const store = build();
    expect(await store.peek('does-not-exist')).toBeUndefined();
  });

  it('peek returns undefined when Directus answers FORBIDDEN (policy hides row existence)', async () => {
    const store = build();
    mocks.setThrow(mocks.makeForbiddenError());
    expect(await store.peek('hidden-id')).toBeUndefined();
  });

  it('get evicts an expired session and returns undefined', async () => {
    const store = build(); // now=1_000_000
    const id = await store.create({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: 500_000, // already expired vs now=1_000_000
    });

    const got = await store.get(id);
    expect(got).toBeUndefined();
    expect(await store.peek(id)).toBeUndefined(); // confirms eviction
  });

  it('update succeeds for a known id, returns true, mutates the row', async () => {
    const store = build();
    const id = await store.create({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: 1_900_000,
    });

    const ok = await store.update(id, {
      accessToken: 'at-2',
      refreshToken: 'rt-2',
      expiresAt: 2_000_000,
    });
    expect(ok).toBe(true);
    expect((await store.peek(id))?.accessToken).toBe('at-2');
  });

  it('update returns false for an unknown id (RECORD_NOT_FOUND)', async () => {
    const store = build();
    const ok = await store.update('unknown', {
      accessToken: 'x',
      refreshToken: 'y',
      expiresAt: 1_900_000,
    });
    expect(ok).toBe(false);
  });

  it('delete swallows RECORD_NOT_FOUND (logout is idempotent)', async () => {
    const store = build();
    await expect(store.delete('never-existed')).resolves.toBeUndefined();
  });

  it('delete propagates non-not-found errors (e.g. network failure)', async () => {
    const store = build();
    mocks.setThrow(mocks.makeNetworkError());
    await expect(store.delete('any-id')).rejects.toThrowError(/fetch/i);
  });

  it('cleanupExpired removes rows whose expires_at is at or before now', async () => {
    const store = build(); // now=1_000_000
    const live = await store.create({
      accessToken: 'live',
      refreshToken: 'rt-live',
      expiresAt: 1_900_000,
    });
    const expired = await store.create({
      accessToken: 'expired',
      refreshToken: 'rt-expired',
      expiresAt: 500_000,
    });
    expect(await store.size()).toBe(2);

    await store.cleanupExpired();

    expect(await store.size()).toBe(1);
    expect(await store.peek(live)).toBeDefined();
    expect(await store.peek(expired)).toBeUndefined();
  });

  it('the same row read by two stores backed by the same Directus is consistent (the Fly-restart invariant)', async () => {
    // The whole point of this store: a brand-new instance (simulating a
    // restarted process) sees sessions created by an earlier instance.
    const a = build();
    const id = await a.create({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: 1_900_000,
    });

    // Build a SECOND store — fresh memory state, same backing rows map
    // (Directus is the source of truth in real life).
    const b = build();
    const peeked = await b.peek(id);
    expect(peeked).toEqual({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: 1_900_000,
    });
  });
});
