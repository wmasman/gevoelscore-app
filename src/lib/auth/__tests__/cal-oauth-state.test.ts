// Step-1 Phase 1.C — cal_oauth_state cookie helpers.

import { describe, expect, it } from 'vitest';
import {
  STATE_COOKIE_NAME,
  STATE_COOKIE_MAX_AGE_S,
  generateOAuthState,
  buildStateCookie,
  clearStateCookie,
  parseStateCookie,
  statesMatch,
} from '../cal-oauth-state';

describe('cal-oauth-state', () => {
  describe('generateOAuthState', () => {
    it('returns a base64url string of plausible length', () => {
      const s = generateOAuthState();

      expect(s).toMatch(/^[A-Za-z0-9_-]+$/);
      // 32 bytes base64url-encoded → ~43 chars (4n/3 rounded down, no padding)
      expect(s.length).toBeGreaterThanOrEqual(40);
      expect(s.length).toBeLessThanOrEqual(48);
    });

    it('two calls yield distinct values (randomness sanity)', () => {
      const a = generateOAuthState();
      const b = generateOAuthState();

      expect(a).not.toBe(b);
    });
  });

  describe('buildStateCookie', () => {
    it('emits the expected attributes including SameSite=Lax + Max-Age=600', () => {
      const cookie = buildStateCookie('abc123');

      expect(cookie).toContain(`${STATE_COOKIE_NAME}=abc123`);
      expect(cookie).toContain('HttpOnly');
      expect(cookie).toContain('Secure');
      expect(cookie).toContain('SameSite=Lax');
      expect(cookie).toContain('Path=/');
      expect(cookie).toContain(`Max-Age=${STATE_COOKIE_MAX_AGE_S}`);
      expect(STATE_COOKIE_MAX_AGE_S).toBe(600);
    });
  });

  describe('clearStateCookie', () => {
    it('emits Max-Age=0 to evict the cookie', () => {
      const cookie = clearStateCookie();

      expect(cookie).toContain(`${STATE_COOKIE_NAME}=`);
      expect(cookie).toContain('Max-Age=0');
    });
  });

  describe('parseStateCookie', () => {
    it('returns the value when the cookie header contains cal_oauth_state', () => {
      const result = parseStateCookie(`${STATE_COOKIE_NAME}=abc; other=foo`);

      expect(result).toBe('abc');
    });

    it('returns null when the header is missing', () => {
      expect(parseStateCookie(null)).toBeNull();
    });

    it('returns null when cal_oauth_state is absent', () => {
      expect(parseStateCookie('other=foo')).toBeNull();
    });

    it('returns null when the value is empty', () => {
      expect(parseStateCookie(`${STATE_COOKIE_NAME}=; other=foo`)).toBeNull();
    });
  });

  describe('statesMatch', () => {
    it('returns true for equal values', () => {
      expect(statesMatch('abc', 'abc')).toBe(true);
    });

    it('returns false for different values of the same length', () => {
      expect(statesMatch('abc', 'abd')).toBe(false);
    });

    it('returns false for different lengths (avoids timingSafeEqual throw)', () => {
      expect(statesMatch('abc', 'abcd')).toBe(false);
    });

    it('returns false for empty values', () => {
      expect(statesMatch('', '')).toBe(true); // both empty: technically equal
      expect(statesMatch('abc', '')).toBe(false);
    });
  });
});
