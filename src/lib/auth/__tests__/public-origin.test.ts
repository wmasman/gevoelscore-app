// Tests for the OAuth public-origin resolver. Covers the four
// resolution paths from public-origin.ts.

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { getPublicOrigin } from '../public-origin';

function makeRequest(opts: {
  url?: string;
  host?: string;
  forwardedHost?: string;
  forwardedProto?: string;
} = {}): Request {
  const headers: Record<string, string> = {};
  if (opts.host) headers.host = opts.host;
  if (opts.forwardedHost) headers['x-forwarded-host'] = opts.forwardedHost;
  if (opts.forwardedProto) headers['x-forwarded-proto'] = opts.forwardedProto;
  return new Request(opts.url ?? 'http://0.0.0.0:3000/api/test', { headers });
}

beforeEach(() => {
  vi.unstubAllEnvs();
});

afterEach(() => {
  vi.unstubAllEnvs();
});

describe('getPublicOrigin', () => {
  describe('APP_BASE_URL precedence', () => {
    it('given APP_BASE_URL set, when called, then returns it verbatim regardless of headers', () => {
      vi.stubEnv('APP_BASE_URL', 'https://gevoelscore-frontend.fly.dev');

      const origin = getPublicOrigin(
        makeRequest({
          url: 'http://0.0.0.0:3000/x',
          host: '0.0.0.0:3000',
        }),
      );

      expect(origin).toBe('https://gevoelscore-frontend.fly.dev');
    });

    it('strips trailing slashes from APP_BASE_URL', () => {
      vi.stubEnv('APP_BASE_URL', 'https://gevoelscore-frontend.fly.dev/');

      const origin = getPublicOrigin(makeRequest());

      expect(origin).toBe('https://gevoelscore-frontend.fly.dev');
    });
  });

  describe('Fly production scenario (the bug we are fixing)', () => {
    it('given Node sees 0.0.0.0 internally but Fly forwards the public host, when called, then returns the public origin from headers', () => {
      // This is the scenario the user hit: request.url is internal,
      // host header is the public Fly domain.
      const origin = getPublicOrigin(
        makeRequest({
          url: 'https://0.0.0.0:3000/api/calendars/google/connect',
          host: 'gevoelscore-frontend.fly.dev',
          forwardedProto: 'https',
        }),
      );

      expect(origin).toBe('https://gevoelscore-frontend.fly.dev');
    });

    it('prefers x-forwarded-host over host header when both are set', () => {
      const origin = getPublicOrigin(
        makeRequest({
          host: 'gevoelscore-frontend.fly.dev',
          forwardedHost: 'app.example.com',
          forwardedProto: 'https',
        }),
      );

      expect(origin).toBe('https://app.example.com');
    });

    it('defaults to https when x-forwarded-proto is absent but host is public', () => {
      const origin = getPublicOrigin(
        makeRequest({
          host: 'gevoelscore-frontend.fly.dev',
        }),
      );

      expect(origin).toBe('https://gevoelscore-frontend.fly.dev');
    });
  });

  describe('local dev fallback', () => {
    it('given host=localhost:3000, when called, then falls back to request.url origin', () => {
      const origin = getPublicOrigin(
        makeRequest({
          url: 'http://localhost:3000/api/x',
          host: 'localhost:3000',
        }),
      );

      expect(origin).toBe('http://localhost:3000');
    });

    it('given host=0.0.0.0:3000 (Node internal), when called, then falls back to request.url origin', () => {
      const origin = getPublicOrigin(
        makeRequest({
          url: 'http://0.0.0.0:3000/api/x',
          host: '0.0.0.0:3000',
        }),
      );

      expect(origin).toBe('http://0.0.0.0:3000');
    });

    it('given no host header at all, when called, then uses request.url origin', () => {
      const origin = getPublicOrigin(makeRequest({ url: 'http://localhost:3000/api/x' }));

      expect(origin).toBe('http://localhost:3000');
    });
  });
});
