import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { allowedOrigins } from '../allowed-origins';

describe('allowedOrigins', () => {
  beforeEach(() => {
    vi.unstubAllEnvs();
  });

  afterEach(() => {
    vi.unstubAllEnvs();
  });

  it('returns only the NEXT_PUBLIC_APP_URL origin in production', () => {
    vi.stubEnv('NEXT_PUBLIC_APP_URL', 'https://app.example.com');
    vi.stubEnv('NODE_ENV', 'production');
    expect(allowedOrigins()).toEqual(['https://app.example.com']);
  });

  it('adds localhost:3000-3003 alongside NEXT_PUBLIC_APP_URL in development', () => {
    vi.stubEnv('NEXT_PUBLIC_APP_URL', 'https://app.example.com');
    vi.stubEnv('NODE_ENV', 'development');
    expect(allowedOrigins()).toEqual([
      'https://app.example.com',
      'http://localhost:3000',
      'http://localhost:3001',
      'http://localhost:3002',
      'http://localhost:3003',
    ]);
  });

  it('returns localhost:3000-3003 when NEXT_PUBLIC_APP_URL is unset in dev', () => {
    vi.stubEnv('NEXT_PUBLIC_APP_URL', '');
    vi.stubEnv('NODE_ENV', 'development');
    expect(allowedOrigins()).toEqual([
      'http://localhost:3000',
      'http://localhost:3001',
      'http://localhost:3002',
      'http://localhost:3003',
    ]);
  });

  it('throws in production when NEXT_PUBLIC_APP_URL is unset (M3 fix)', () => {
    vi.stubEnv('NEXT_PUBLIC_APP_URL', '');
    vi.stubEnv('NODE_ENV', 'production');
    expect(() => allowedOrigins()).toThrow(/NEXT_PUBLIC_APP_URL/);
  });
});
