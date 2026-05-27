import { describe, expect, it } from 'vitest';
import {
  createPendingOtpStore,
  buildPendingOtpCookie,
  parsePendingOtpCookie,
  PENDING_OTP_COOKIE_NAME,
} from '../pending-otp';

describe('pending-otp', () => {
  describe('createPendingOtpStore', () => {
    it('stashes credentials and returns an opaque id', () => {
      const store = createPendingOtpStore();
      const id = store.create({
        email: 'a@b.com',
        password: 'pw',
        expiresAt: Date.now() + 60_000,
      });
      expect(typeof id).toBe('string');
      expect(id.length).toBeGreaterThan(20);
    });

    it('returns the stashed credentials by id', () => {
      const store = createPendingOtpStore();
      const id = store.create({
        email: 'a@b.com',
        password: 'pw',
        expiresAt: Date.now() + 60_000,
      });
      const got = store.get(id);
      expect(got?.email).toBe('a@b.com');
      expect(got?.password).toBe('pw');
    });

    it('returns undefined for an unknown id', () => {
      const store = createPendingOtpStore();
      expect(store.get('nope')).toBeUndefined();
    });

    it('expires entries past expiresAt and removes them on read', () => {
      const now = 1_000_000;
      let clock = now;
      const store = createPendingOtpStore({ now: () => clock });
      const id = store.create({ email: 'a@b.com', password: 'pw', expiresAt: now + 1_000 });
      clock = now + 2_000;
      expect(store.get(id)).toBeUndefined();
      expect(store.size()).toBe(0);
    });

    it('delete removes the entry', () => {
      const store = createPendingOtpStore();
      const id = store.create({ email: 'a@b.com', password: 'pw', expiresAt: Date.now() + 60_000 });
      store.delete(id);
      expect(store.get(id)).toBeUndefined();
    });
  });

  describe('buildPendingOtpCookie', () => {
    it('produces httpOnly Secure SameSite=Strict cookie with short Max-Age', () => {
      const cookie = buildPendingOtpCookie('p-123', 300);
      expect(cookie).toContain(`${PENDING_OTP_COOKIE_NAME}=p-123`);
      expect(cookie).toContain('HttpOnly');
      expect(cookie).toContain('Secure');
      expect(cookie).toContain('SameSite=Strict');
      expect(cookie).toContain('Path=/');
      expect(cookie).toContain('Max-Age=300');
    });

    it('builds a deletion cookie when id is null', () => {
      const cookie = buildPendingOtpCookie(null, 0);
      expect(cookie).toContain(`${PENDING_OTP_COOKIE_NAME}=`);
      expect(cookie).toContain('Max-Age=0');
    });
  });

  describe('parsePendingOtpCookie', () => {
    it('extracts the id from a Cookie header', () => {
      const header = `gs_session=other; ${PENDING_OTP_COOKIE_NAME}=p-abc; x=y`;
      expect(parsePendingOtpCookie(header)).toBe('p-abc');
    });

    it('returns null when cookie absent or empty', () => {
      expect(parsePendingOtpCookie('other=v')).toBeNull();
      expect(parsePendingOtpCookie('')).toBeNull();
      expect(parsePendingOtpCookie(null)).toBeNull();
    });
  });
});
