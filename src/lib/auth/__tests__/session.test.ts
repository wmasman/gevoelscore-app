import { describe, expect, it } from 'vitest';
import {
  createSessionStore,
  buildSessionCookie,
  parseSessionCookie,
  SESSION_COOKIE_NAME,
} from '../session';

describe('session', () => {
  describe('createSessionStore', () => {
    it('creates a session and returns an opaque session id', () => {
      const store = createSessionStore();

      const id = store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      expect(typeof id).toBe('string');
      expect(id.length).toBeGreaterThan(20);
    });

    it('returns the session by id', () => {
      const store = createSessionStore();
      const id = store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      const session = store.get(id);
      expect(session?.accessToken).toBe('at-1');
      expect(session?.refreshToken).toBe('rt-1');
    });

    it('returns undefined for an unknown id', () => {
      const store = createSessionStore();
      expect(store.get('does-not-exist')).toBeUndefined();
    });

    it('returns undefined for an expired session and removes it', () => {
      let now = 1_000_000;
      const store = createSessionStore({ now: () => now });
      const id = store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: now + 1_000,
      });

      now += 2_000;
      expect(store.get(id)).toBeUndefined();
      expect(store.size()).toBe(0);
    });

    it('delete removes the session', () => {
      const store = createSessionStore();
      const id = store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      store.delete(id);
      expect(store.get(id)).toBeUndefined();
    });

    it('cleanupExpired removes only expired sessions', () => {
      const now = 1_000_000;
      const store = createSessionStore({ now: () => now });

      const liveId = store.create({
        accessToken: 'live',
        refreshToken: 'rt-live',
        expiresAt: now + 60_000,
      });
      store.create({
        accessToken: 'expired',
        refreshToken: 'rt-expired',
        expiresAt: now - 1,
      });

      store.cleanupExpired();
      expect(store.size()).toBe(1);
      expect(store.get(liveId)).toBeDefined();
    });

    it('uses an injected idGenerator when provided (deterministic tests)', () => {
      let counter = 0;
      const store = createSessionStore({
        idGenerator: () => `id-${++counter}`,
      });

      const id = store.create({
        accessToken: 'at',
        refreshToken: 'rt',
        expiresAt: Date.now() + 60_000,
      });
      expect(id).toBe('id-1');
    });
  });

  describe('peek (no eviction)', () => {
    it('returns the entry as-is for a live session', () => {
      const store = createSessionStore();
      const id = store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      expect(store.peek(id)?.accessToken).toBe('at-1');
    });

    it('returns the entry even when the access token is expired (does NOT evict)', () => {
      let clock = 1_000_000;
      const store = createSessionStore({ now: () => clock });
      const id = store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: clock + 1_000,
      });

      clock += 2_000;
      const peeked = store.peek(id);
      expect(peeked?.accessToken).toBe('at-1');
      expect(store.size()).toBe(1);
    });

    it('returns undefined for an unknown id', () => {
      const store = createSessionStore();
      expect(store.peek('nope')).toBeUndefined();
    });
  });

  describe('update (replace in place)', () => {
    it('replaces the entry data for a known id and returns true', () => {
      const store = createSessionStore();
      const id = store.create({
        accessToken: 'at-1',
        refreshToken: 'rt-1',
        expiresAt: Date.now() + 60_000,
      });

      const result = store.update(id, {
        accessToken: 'at-2',
        refreshToken: 'rt-2',
        expiresAt: Date.now() + 120_000,
      });

      expect(result).toBe(true);
      expect(store.peek(id)?.accessToken).toBe('at-2');
      expect(store.peek(id)?.refreshToken).toBe('rt-2');
    });

    it('returns false for an unknown id and does NOT create a new entry', () => {
      const store = createSessionStore();
      const result = store.update('unknown', {
        accessToken: 'at',
        refreshToken: 'rt',
        expiresAt: Date.now() + 60_000,
      });

      expect(result).toBe(false);
      expect(store.size()).toBe(0);
    });
  });

  describe('buildSessionCookie', () => {
    it('produces a httpOnly Secure SameSite=Strict cookie with Max-Age', () => {
      const cookie = buildSessionCookie('abc-123', 3600);

      expect(cookie).toContain(`${SESSION_COOKIE_NAME}=abc-123`);
      expect(cookie).toContain('HttpOnly');
      expect(cookie).toContain('Secure');
      expect(cookie).toContain('SameSite=Strict');
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
