import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  directusLoginWithOtp: vi.fn(),
  verifyRateCheck: vi.fn(),
  sessionCreate: vi.fn(),
  pendingOtpGet: vi.fn(),
  pendingOtpDelete: vi.fn(),
  pendingOtpIncrementAttempts: vi.fn(),
}));

vi.mock('@/lib/auth/directus-auth', () => ({
  directusLoginWithOtp: mocks.directusLoginWithOtp,
}));

vi.mock('@/lib/auth/stores', () => ({
  loginRateLimiter: { check: vi.fn(), sweep: vi.fn(), size: vi.fn() },
  verifyRateLimiter: { check: mocks.verifyRateCheck, sweep: vi.fn(), size: vi.fn() },
  sessionStore: {
    create: mocks.sessionCreate,
    get: vi.fn(),
    delete: vi.fn(),
    cleanupExpired: vi.fn(),
    size: vi.fn(),
  },
  pendingOtpStore: {
    create: vi.fn(),
    get: mocks.pendingOtpGet,
    delete: mocks.pendingOtpDelete,
    incrementAttempts: mocks.pendingOtpIncrementAttempts,
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
  return new Request('http://localhost:3000/api/auth/login/verify', {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });
}

describe('POST /api/auth/login/verify', () => {
  beforeEach(() => {
    mocks.directusLoginWithOtp.mockReset();
    mocks.verifyRateCheck.mockReset();
    mocks.sessionCreate.mockReset();
    mocks.pendingOtpGet.mockReset();
    mocks.pendingOtpDelete.mockReset();
    mocks.pendingOtpIncrementAttempts.mockReset();
    mocks.verifyRateCheck.mockReturnValue({ allowed: true, remaining: 4 });
    mocks.sessionCreate.mockReturnValue('session-id-1');
    mocks.pendingOtpGet.mockReturnValue({
      email: 'a@b.com',
      password: 'pw',
      expiresAt: Date.now() + 60_000,
      attempts: 0,
    });
    mocks.pendingOtpIncrementAttempts.mockReturnValue(1);
  });

  it('AC6: valid OTP + valid pending → 200 + session cookie + cleared pending cookie', async () => {
    mocks.directusLoginWithOtp.mockResolvedValue({
      ok: true,
      value: { accessToken: 'at', refreshToken: 'rt', expiresInMs: 3600_000 },
    });

    const res = await POST(makeRequest({ otp: '123456' }, { cookie: 'gs_pending_otp=p-id' }));
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ ok: true });

    const setCookies = res.headers.getSetCookie();
    expect(setCookies.some((c) => c.includes('gs_session=session-id-1'))).toBe(true);
    expect(setCookies.some((c) => c.includes('gs_pending_otp=') && c.includes('Max-Age=0'))).toBe(true);
    expect(mocks.pendingOtpDelete).toHaveBeenCalledWith('p-id');
  });

  it('AC7: invalid OTP → 401, keeps pending state intact', async () => {
    mocks.directusLoginWithOtp.mockResolvedValue({ ok: false, error: 'invalid_otp' });

    const res = await POST(makeRequest({ otp: '000000' }, { cookie: 'gs_pending_otp=p-id' }));
    expect(res.status).toBe(401);
    expect(await res.json()).toEqual({ error: 'invalid_otp' });
    expect(mocks.pendingOtpDelete).not.toHaveBeenCalled();
  });

  it('AC10: no pending cookie → 401 (same generic error as wrong code)', async () => {
    const res = await POST(makeRequest({ otp: '123456' }));
    expect(res.status).toBe(401);
    expect(await res.json()).toEqual({ error: 'invalid_otp' });
    expect(mocks.directusLoginWithOtp).not.toHaveBeenCalled();
  });

  it('AC10: pending cookie but no matching state → 401', async () => {
    mocks.pendingOtpGet.mockReturnValue(undefined);
    const res = await POST(makeRequest({ otp: '123456' }, { cookie: 'gs_pending_otp=stale-id' }));
    expect(res.status).toBe(401);
    expect(mocks.directusLoginWithOtp).not.toHaveBeenCalled();
  });

  it('AC8: rate-limited → 429, no Directus call', async () => {
    mocks.verifyRateCheck.mockReturnValue({ allowed: false, retryAfterMs: 30_000 });
    const res = await POST(makeRequest({ otp: '123456' }, { cookie: 'gs_pending_otp=p-id' }));
    expect(res.status).toBe(429);
    expect(mocks.directusLoginWithOtp).not.toHaveBeenCalled();
  });

  it('A08: cross-origin → 403', async () => {
    const res = await POST(
      makeRequest({ otp: '123456' }, { cookie: 'gs_pending_otp=p-id', origin: 'https://evil.example.com' }),
    );
    expect(res.status).toBe(403);
  });

  it('400 on missing otp', async () => {
    const res = await POST(makeRequest({}, { cookie: 'gs_pending_otp=p-id' }));
    expect(res.status).toBe(400);
  });

  it('M5: 1st and 2nd wrong OTP keep the pending cookie alive', async () => {
    mocks.directusLoginWithOtp.mockResolvedValue({ ok: false, error: 'invalid_otp' });
    mocks.pendingOtpIncrementAttempts.mockReturnValueOnce(1);
    const res1 = await POST(makeRequest({ otp: '000000' }, { cookie: 'gs_pending_otp=p-id' }));
    expect(res1.status).toBe(401);
    expect(res1.headers.getSetCookie().some((c) => c.includes('gs_pending_otp=') && c.includes('Max-Age=0'))).toBe(false);
    expect(mocks.pendingOtpDelete).not.toHaveBeenCalled();

    mocks.pendingOtpIncrementAttempts.mockReturnValueOnce(2);
    const res2 = await POST(makeRequest({ otp: '000000' }, { cookie: 'gs_pending_otp=p-id' }));
    expect(res2.status).toBe(401);
    expect(res2.headers.getSetCookie().some((c) => c.includes('gs_pending_otp=') && c.includes('Max-Age=0'))).toBe(false);
    expect(mocks.pendingOtpDelete).not.toHaveBeenCalled();
  });

  it('M5: 3rd wrong OTP clears pending state + cookie (still generic error)', async () => {
    mocks.directusLoginWithOtp.mockResolvedValue({ ok: false, error: 'invalid_otp' });
    mocks.pendingOtpIncrementAttempts.mockReturnValue(3);
    const res = await POST(makeRequest({ otp: '000000' }, { cookie: 'gs_pending_otp=p-id' }));
    expect(res.status).toBe(401);
    expect(await res.json()).toEqual({ error: 'invalid_otp' });
    expect(res.headers.getSetCookie().some((c) => c.includes('gs_pending_otp=') && c.includes('Max-Age=0'))).toBe(true);
    expect(mocks.pendingOtpDelete).toHaveBeenCalledWith('p-id');
  });
});
