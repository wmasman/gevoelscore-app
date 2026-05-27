import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  directusEnableTfa: vi.fn(),
  getValidatedSession: vi.fn(),
}));

vi.mock('@/lib/auth/directus-auth', () => ({
  directusEnableTfa: mocks.directusEnableTfa,
}));

vi.mock('@/lib/auth/get-validated-session', () => ({
  getValidatedSession: mocks.getValidatedSession,
}));

vi.mock('@/lib/auth/stores', () => ({
  loginRateLimiter: { check: vi.fn(), sweep: vi.fn(), size: vi.fn() },
  verifyRateLimiter: { check: vi.fn(), sweep: vi.fn(), size: vi.fn() },
  sessionStore: {
    create: vi.fn(),
    get: vi.fn(),
    peek: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
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

function makeRequest(body: unknown, opts: { cookie?: string; origin?: string } = {}) {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    origin: opts.origin ?? 'http://localhost:3000',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  return new Request('http://localhost:3000/api/auth/2fa/enable', {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });
}

describe('POST /api/auth/2fa/enable', () => {
  beforeEach(() => {
    mocks.directusEnableTfa.mockReset();
    mocks.getValidatedSession.mockReset();
    mocks.getValidatedSession.mockResolvedValue({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: Date.now() + 60_000,
    });
  });

  it('200 on valid session + secret + otp', async () => {
    mocks.directusEnableTfa.mockResolvedValue({ ok: true, value: undefined });

    const res = await POST(
      makeRequest({ secret: 'JBSWY', otp: '123456' }, { cookie: 'gs_session=s-id' }),
    );
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ ok: true });
    expect(mocks.directusEnableTfa).toHaveBeenCalledWith('at-1', 'JBSWY', '123456');
  });

  it('401 when no session cookie', async () => {
    const res = await POST(makeRequest({ secret: 'JBSWY', otp: '123456' }));
    expect(res.status).toBe(401);
    expect(mocks.directusEnableTfa).not.toHaveBeenCalled();
  });

  it('401 when Directus rejects the OTP', async () => {
    mocks.directusEnableTfa.mockResolvedValue({ ok: false, error: 'invalid_otp' });
    const res = await POST(
      makeRequest({ secret: 'JBSWY', otp: '000000' }, { cookie: 'gs_session=s-id' }),
    );
    expect(res.status).toBe(401);
    expect(await res.json()).toEqual({ error: 'invalid_otp' });
  });

  it('403 on cross-origin', async () => {
    const res = await POST(
      makeRequest({ secret: 'JBSWY', otp: '123456' }, {
        cookie: 'gs_session=s-id',
        origin: 'https://evil.example.com',
      }),
    );
    expect(res.status).toBe(403);
  });

  it('400 on missing secret', async () => {
    const res = await POST(makeRequest({ otp: '123456' }, { cookie: 'gs_session=s-id' }));
    expect(res.status).toBe(400);
  });

  it('400 on missing otp', async () => {
    const res = await POST(makeRequest({ secret: 'JBSWY' }, { cookie: 'gs_session=s-id' }));
    expect(res.status).toBe(400);
  });
});
