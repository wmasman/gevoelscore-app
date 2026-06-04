import { describe, expect, it } from 'vitest';
import {
  createSessionStore,
  buildSessionCookie,
  parseSessionCookie,
  SESSION_COOKIE_NAME,
} from '../session';

describe('session', () => {
  describe('createSessionStore', () => {
    it('creates a session and returns an opaque session id', async () => {
      const store = createSessionStore();

      const id = await store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      expect(typeof id).toBe('string');
      expect(id.length).toBeGreaterThan(20);
    });

    it('returns the session by id', async () => {
      const store = createSessionStore();
      const id = await store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      const session = await store.get(id);
      expect(session?.accessToken).toBe('at-1');
      expect(session?.refreshToken).toBe('rt-1');
    });

    it('returns undefined for an unknown id', async () => {
      const store = createSessionStore();
      expect(await store.get('does-not-exist')).toBeUndefined();
    });

    it('returns undefined for an expired session and removes it', async () => {
      let now = 1_000_000;
      const store = createSessionStore({ now: () => now });
      const id = await store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: now + 1_000,
      });

      now += 2_000;
      expect(await store.get(id)).toBeUndefined();
      expect(await store.size()).toBe(0);
    });

    it('delete removes the session', async () => {
      const store = createSessionStore();
      const id = await store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      await store.delete(id);
      expect(await store.get(id)).toBeUndefined();
    });

    it('cleanupExpired removes only expired sessions', async () => {
      const now = 1_000_000;
      const store = createSessionStore({ now: () => now });

      const liveId = await store.create({
        accessToken: 'live',
        refreshToken: 'rt-live',
        expiresAt: now + 60_000,
      });
      await store.create({
        accessToken: 'expired',
        refreshToken: 'rt-expired',
        expiresAt: now - 1,
      });

      await store.cleanupExpired();
      expect(await store.size()).toBe(1);
      expect(await store.get(liveId)).toBeDefined();
    });

    it('uses an injected idGenerator when provided (deterministic tests)', async () => {
      let counter = 0;
      const store = createSessionStore({
        idGenerator: () => `id-${++counter}`,
      });

      const id = await store.create({
        accessToken: 'at',
        refreshToken: 'rt',
        expiresAt: Date.now() + 60_000,
      });
      expect(id).toBe('id-1');
    });
  });

  describe('peek (no eviction)', () => {
    it('returns the entry as-is for a live session', async () => {
      const store = createSessionStore();
      const id = await store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      expect((await store.peek(id))?.accessToken).toBe('at-1');
    });

    it('returns the entry even when the access token is expired (does NOT evict)', async () => {
      let clock = 1_000_000;
      const store = createSessionStore({ now: () => clock });
      const id = await store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: clock + 1_000,
      });

      clock += 2_000;
      const peeked = await store.peek(id);
      expect(peeked?.accessToken).toBe('at-1');
      expect(await store.size()).toBe(1);
    });

    it('returns undefined for an unknown id', async () => {
      const store = createSessionStore();
      expect(await store.peek('nope')).toBeUndefined();
    });
  });

  describe('update (replace in place)', () => {
    it('replaces the entry data for a known id and returns true', async () => {
      const store = createSessionStore();
      const id = await store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      const result = await store.update(id, {
        accessToken: 'at-2',
        refreshToken: 'rt-2',
        expiresAt: Date.now() + 120_000,
      });

      expect(result).toBe(true);
      expect((await store.peek(id))?.accessToken).toBe('at-2');
      expect((await store.peek(id))?.refreshToken).toBe('rt-2');
    });

    it('returns false for an unknown id and does NOT create a new entry', async () => {
      const store = createSessionStore();
      const result = await store.update('unknown', {
        accessToken: 'at',
        refreshToken: 'rt',
        expiresAt: Date.now() + 60_000,
      });

      expect(result).toBe(false);
      expect(await store.size()).toBe(0);
    });
  });

  describe('buildSessionCookie', () => {
    it('produces a httpOnly Secure SameSite=Lax cookie with Max-Age', () => {
      // SameSite=Lax (not Strict) so the cookie flows on top-level cross-site
      // GET navigation, which OAuth callbacks need (e.g. Google -> our
      // /api/calendars/google/callback redirect). CSRF on mutations is
      // covered by the validateOrigin check, not by SameSite.
      const cookie = buildSessionCookie('abc-123', 3600);

      expect(cookie).toContain(`${SESSION_COOKIE_NAME}=abc-123`);
      expect(cookie).toContain('HttpOnly');
      expect(cookie).toContain('Secure');
      expect(cookie).toContain('SameSite=Lax');
      expect(cookie).toContain('Path=/');
      expect(cookie).toContain('Max-Age=3600');
    });

    it('produces a cookie deletion string when sessionId is null', () => {
      const cookie = buildSessionCookie(null, 0);

      expect(cookie).toContain(`${SESSION_COOKIE_NAME}=`);
      expect(cookie).toContain('Max-Age=0');
      expect(cookie).toContain('HttpOnly');
      expect(cookie).toContain('Secure');
    });
  });

  describe('parseSessionCookie', () => {
    it('extracts the session id from a Cookie header', () => {
      const header = `${SESSION_COOKIE_NAME}=abc-123; other=foo`;
      expect(parseSessionCookie(header)).toBe('abc-123');
    });

    it('returns null when the cookie is absent', () => {
      expect(parseSessionCookie('other=foo; another=bar')).toBeNull();
    });

    it('returns null for an empty or null header', () => {
      expect(parseSessionCookie('')).toBeNull();
      expect(parseSessionCookie(null)).toBeNull();
    });
  });
});
