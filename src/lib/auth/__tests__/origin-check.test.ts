import { describe, expect, it } from 'vitest';
import { validateOrigin } from '../origin-check';

describe('origin-check', () => {
  const allowed = ['https://gevoelscore-frontend.fly.dev'];

  describe('validateOrigin', () => {
    it('accepts a request whose Origin matches an allowed origin', () => {
      expect(validateOrigin('https://gevoelscore-frontend.fly.dev', null, allowed)).toBe(true);
    });

    it('accepts a same-origin request with no Origin and no Referer (Safari behaviour)', () => {
      expect(validateOrigin(null, null, allowed)).toBe(true);
    });

    it('falls back to Referer when Origin is missing', () => {
      expect(validateOrigin(null, 'https://gevoelscore-frontend.fly.dev/login', allowed)).toBe(true);
    });

    it('rejects a request from a non-allowed Origin', () => {
      expect(validateOrigin('https://evil.example.com', null, allowed)).toBe(false);
    });

    it('rejects a request whose Referer points at a non-allowed origin', () => {
      expect(validateOrigin(null, 'https://evil.example.com/x', allowed)).toBe(false);
    });

    it('rejects an Origin header that does not parse as a URL', () => {
      expect(validateOrigin('not-a-url', null, allowed)).toBe(false);
    });

    it('rejects a malformed Referer (does not fall through to no-header path)', () => {
      expect(validateOrigin(null, 'not-a-url', allowed)).toBe(false);
    });

    it('handles localhost dev origins when configured', () => {
      const dev = ['http://localhost:3000'];
      expect(validateOrigin('http://localhost:3000', null, dev)).toBe(true);
      expect(validateOrigin('http://localhost:3001', null, dev)).toBe(false);
    });

    it('does NOT do wildcard or subdomain matching — strict equality only', () => {
      expect(validateOrigin('https://attacker.gevoelscore-frontend.fly.dev', null, allowed)).toBe(false);
      expect(validateOrigin('https://gevoelscore-frontend.fly.dev.evil.com', null, allowed)).toBe(false);
    });
  });
});
