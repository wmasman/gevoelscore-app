import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  directusEnableTfa: vi.fn(),
  getValidatedSession: vi.fn(),
  pendingTfaGet: vi.fn(),
  pendingTfaDelete: vi.fn(),
  tfaEnableRateLimiterCheck: vi.fn(),
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
  tfaGenerateRateLimiter: { check: vi.fn(), sweep: vi.fn(), size: vi.fn() },
  tfaEnableRateLimiter: {
    check: mocks.tfaEnableRateLimiterCheck,
    sweep: vi.fn(),
    size: vi.fn(),
  },
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
  pendingTfaStore: {
    create: vi.fn(),
    get: mocks.pendingTfaGet,
    delete: mocks.pendingTfaDelete,
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
    mocks.pendingTfaGet.mockReset();
    mocks.pendingTfaDelete.mockReset();
    mocks.tfaEnableRateLimiterCheck.mockReset();
    mocks.tfaEnableRateLimiterCheck.mockReturnValue({ allowed: true });
    mocks.getValidatedSession.mockResolvedValue({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: Date.now() + 60_000,
    });
    mocks.pendingTfaGet.mockReturnValue({ secret: 'LEGIT', expiresAt: Date.now() + 60_000 });
  });

  it('200 on valid session + pending entry + otp', async () => {
    mocks.directusEnableTfa.mockResolvedValue({ ok: true, value: undefined });

    const res = await POST(
      makeRequest({ otp: '123456' }, { cookie: 'gs_session=s-id' }),
    );
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ ok: true });
    expect(mocks.directusEnableTfa).toHaveBeenCalledWith('at-1', 'LEGIT', '123456');
  });

  it('uses the stored secret and ignores body.secret (H2 fix)', async () => {
    mocks.directusEnableTfa.mockResolvedValue({ ok: true, value: undefined });
    await POST(
      makeRequest(
        { secret: 'ATTACKER', otp: '123456' },
        { cookie: 'gs_session=s-id' },
      ),
    );
    expect(mocks.directusEnableTfa).toHaveBeenCalledWith('at-1', 'LEGIT', '123456');
  });

  it('deletes the pending entry on successful enable', async () => {
    mocks.directusEnableTfa.mockResolvedValue({ ok: true, value: undefined });
    await POST(makeRequest({ otp: '123456' }, { cookie: 'gs_session=s-id' }));
    expect(mocks.pendingTfaDelete).toHaveBeenCalledWith('s-id');
  });

  it('400 when no pending TFA entry exists for the session', async () => {
    mocks.pendingTfaGet.mockReturnValue(undefined);
    const res = await POST(makeRequest({ otp: '123456' }, { cookie: 'gs_session=s-id' }));
    expect(res.status).toBe(400);
    expect(mocks.directusEnableTfa).not.toHaveBeenCalled();
  });

  it('401 when no session cookie', async () => {
    const res = await POST(makeRequest({ otp: '123456' }));
    expect(res.status).toBe(401);
    expect(mocks.directusEnableTfa).not.toHaveBeenCalled();
  });

  it('401 when Directus rejects the OTP', async () => {
    mocks.directusEnableTfa.mockResolvedValue({ ok: false, error: 'invalid_otp' });
    const res = await POST(
      makeRequest({ otp: '000000' }, { cookie: 'gs_session=s-id' }),
    );
    expect(res.status).toBe(401);
    expect(await res.json()).toEqual({ error: 'invalid_otp' });
  });

  it('does not delete pending entry on Directus failure (user can retry)', async () => {
    mocks.directusEnableTfa.mockResolvedValue({ ok: false, error: 'invalid_otp' });
    await POST(makeRequest({ otp: '000000' }, { cookie: 'gs_session=s-id' }));
    expect(mocks.pendingTfaDelete).not.toHaveBeenCalled();
  });

  it('403 on cross-origin', async () => {
    const res = await POST(
      makeRequest({ otp: '123456' }, {
        cookie: 'gs_session=s-id',
        origin: 'https://evil.example.com',
      }),
    );
    expect(res.status).toBe(403);
  });

  it('400 on missing otp', async () => {
    const res = await POST(makeRequest({}, { cookie: 'gs_session=s-id' }));
    expect(res.status).toBe(400);
  });

  it('429 when tfaEnableRateLimiter rejects (H1)', async () => {
    mocks.tfaEnableRateLimiterCheck.mockReturnValue({ allowed: false, retryAfterMs: 2345 });
    const res = await POST(makeRequest({ otp: '123456' }, { cookie: 'gs_session=s-id' }));
    expect(res.status).toBe(429);
    expect(await res.json()).toEqual({ error: 'rate_limited', retry_after_ms: 2345 });
    expect(mocks.directusEnableTfa).not.toHaveBeenCalled();
  });
});
