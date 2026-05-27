import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  directusLogout: vi.fn(),
  sessionGet: vi.fn(),
  sessionDelete: vi.fn(),
}));

vi.mock('@/lib/auth/directus-auth', () => ({
  directusLogout: mocks.directusLogout,
}));

vi.mock('@/lib/auth/stores', () => ({
  loginRateLimiter: { check: vi.fn(), sweep: vi.fn(), size: vi.fn() },
  verifyRateLimiter: { check: vi.fn(), sweep: vi.fn(), size: vi.fn() },
  sessionStore: {
    create: vi.fn(),
    get: mocks.sessionGet,
    delete: mocks.sessionDelete,
    cleanupExpired: vi.fn(),
    size: vi.fn(),
  },
  pendingOtpStore: {
    create: vi.fn(),
    get: vi.fn(),
    delete: vi.fn(),
    cleanupExpired: vi.fn(),
    size: vi.fn(),
  },
  getClientIp: () => '1.2.3.4',
}));

import { POST } from '../route';

function makeRequest(opts: { cookie?: string; origin?: string } = {}) {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    origin: opts.origin ?? 'http://localhost:3000',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  return new Request('http://localhost:3000/api/auth/logout', { method: 'POST', headers });
}

describe('POST /api/auth/logout', () => {
  beforeEach(() => {
    mocks.directusLogout.mockReset();
    mocks.sessionGet.mockReset();
    mocks.sessionDelete.mockReset();
    mocks.directusLogout.mockResolvedValue({ ok: true, value: undefined });
  });

  it('AC13: with valid session cookie → calls Directus logout + clears session + 200', async () => {
    mocks.sessionGet.mockReturnValue({
      accessToken: 'at',
      refreshToken: 'rt',
      expiresAt: Date.now() + 60_000,
    });

    const res = await POST(makeRequest({ cookie: 'gs_session=s-id' }));
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ ok: true });
    expect(mocks.directusLogout).toHaveBeenCalledWith('rt');
    expect(mocks.sessionDelete).toHaveBeenCalledWith('s-id');

    const setCookie = res.headers.get('set-cookie') ?? '';
    expect(setCookie).toContain('gs_session=');
    expect(setCookie).toContain('Max-Age=0');
    expect(setCookie).toContain('HttpOnly');
  });

  it('idempotent: no session cookie → 200, no Directus call', async () => {
    const res = await POST(makeRequest());
    expect(res.status).toBe(200);
    expect(mocks.directusLogout).not.toHaveBeenCalled();
    expect(mocks.sessionDelete).not.toHaveBeenCalled();
  });

  it('idempotent: stale session cookie (no matching server state) → 200, no Directus call', async () => {
    mocks.sessionGet.mockReturnValue(undefined);
    const res = await POST(makeRequest({ cookie: 'gs_session=stale' }));
    expect(res.status).toBe(200);
    expect(mocks.directusLogout).not.toHaveBeenCalled();
  });

  it('A08: cross-origin → 403', async () => {
    const res = await POST(makeRequest({ origin: 'https://evil.example.com' }));
    expect(res.status).toBe(403);
  });
});
