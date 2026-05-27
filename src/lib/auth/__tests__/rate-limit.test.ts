import { describe, expect, it } from 'vitest';
import { createRateLimiter } from '../rate-limit';

describe('rate-limit', () => {
  describe('createRateLimiter', () => {
    it('allows attempts up to the limit, then blocks the next one', () => {
      const now = 1_000_000;
      const limiter = createRateLimiter({
        limit: 5,
        windowMs: 5 * 60_000,
        now: () => now,
      });

      for (let i = 0; i < 5; i++) {
        const r = limiter.check('203.0.113.1');
        expect(r.allowed).toBe(true);
        if (r.allowed) {
          expect(r.remaining).toBe(4 - i);
        }
      }

      const blocked = limiter.check('203.0.113.1');
      expect(blocked.allowed).toBe(false);
      if (!blocked.allowed) {
        expect(blocked.retryAfterMs).toBeGreaterThan(0);
      }
    });

    it('resets the counter after the window expires', () => {
      let now = 1_000_000;
      const limiter = createRateLimiter({
        limit: 5,
        windowMs: 5 * 60_000,
        now: () => now,
      });

      for (let i = 0; i < 5; i++) limiter.check('1.2.3.4');
      expect(limiter.check('1.2.3.4').allowed).toBe(false);

      now += 5 * 60_000 + 1;
      const fresh = limiter.check('1.2.3.4');
      expect(fresh.allowed).toBe(true);
      if (fresh.allowed) {
        expect(fresh.remaining).toBe(4);
      }
    });

    it('isolates keys — one IP being blocked does not affect another', () => {
      const limiter = createRateLimiter({ limit: 5, windowMs: 60_000 });

      for (let i = 0; i < 5; i++) limiter.check('1.1.1.1');
      expect(limiter.check('1.1.1.1').allowed).toBe(false);
      expect(limiter.check('2.2.2.2').allowed).toBe(true);
    });

    it('isolates namespaces — login and totp counters do not share', () => {
      const loginLimiter = createRateLimiter({ limit: 5, windowMs: 60_000 });
      const totpLimiter = createRateLimiter({ limit: 5, windowMs: 60_000 });

      for (let i = 0; i < 5; i++) loginLimiter.check('9.9.9.9');
      expect(loginLimiter.check('9.9.9.9').allowed).toBe(false);
      expect(totpLimiter.check('9.9.9.9').allowed).toBe(true);
    });

    it('cleans up expired entries when sweep() is called', () => {
      let now = 1_000_000;
      const limiter = createRateLimiter({
        limit: 5,
        windowMs: 60_000,
        now: () => now,
      });

      limiter.check('1.1.1.1');
      limiter.check('2.2.2.2');
      expect(limiter.size()).toBe(2);

      now += 60_000 + 1;
      limiter.sweep();
      expect(limiter.size()).toBe(0);
    });

    it('reports retryAfterMs as the remaining window time, not the full window', () => {
      let now = 1_000_000;
      const limiter = createRateLimiter({
        limit: 5,
        windowMs: 60_000,
        now: () => now,
      });

      for (let i = 0; i < 5; i++) limiter.check('1.1.1.1');
      now += 20_000;
      const blocked = limiter.check('1.1.1.1');

      expect(blocked.allowed).toBe(false);
      if (!blocked.allowed) {
        expect(blocked.retryAfterMs).toBeGreaterThan(0);
        expect(blocked.retryAfterMs).toBeLessThanOrEqual(40_000);
      }
    });
  });
});
