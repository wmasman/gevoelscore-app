import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  directusGenerateTfaSecret: vi.fn(),
  getValidatedSession: vi.fn(),
  pendingTfaCreate: vi.fn(),
  tfaGenerateRateLimiterCheck: vi.fn(),
}));

vi.mock('@/lib/auth/directus-auth', () => ({
  directusGenerateTfaSecret: mocks.directusGenerateTfaSecret,
}));

vi.mock('@/lib/auth/get-validated-session', () => ({
  getValidatedSession: mocks.getValidatedSession,
}));

vi.mock('@/lib/auth/stores', () => ({
  loginRateLimiter: { check: vi.fn(), sweep: vi.fn(), size: vi.fn() },
  verifyRateLimiter: { check: vi.fn(), sweep: vi.fn(), size: vi.fn() },
  tfaGenerateRateLimiter: {
    check: mocks.tfaGenerateRateLimiterCheck,
    sweep: vi.fn(),
    size: vi.fn(),
  },
  tfaEnableRateLimiter: { check: vi.fn(), sweep: vi.fn(), size: vi.fn() },
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
    create: mocks.pendingTfaCreate,
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
  return new Request('http://localhost:3000/api/auth/2fa/generate', {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });
}

describe('POST /api/auth/2fa/generate', () => {
  beforeEach(() => {
    mocks.directusGenerateTfaSecret.mockReset();
    mocks.getValidatedSession.mockReset();
    mocks.pendingTfaCreate.mockReset();
    mocks.tfaGenerateRateLimiterCheck.mockReset();
    mocks.tfaGenerateRateLimiterCheck.mockReturnValue({ allowed: true });
    mocks.getValidatedSession.mockResolvedValue({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: Date.now() + 60_000,
    });
  });

  it('200 with valid session + correct password → returns secret + otpauth_url', async () => {
    mocks.directusGenerateTfaSecret.mockResolvedValue({
      ok: true,
      value: { secret: 'JBSWY3DPEHPK3PXP', otpauthUrl: 'otpauth://totp/Directus:a@b.com?secret=JBSWY3DPEHPK3PXP' },
    });

    const res = await POST(makeRequest({ password: 'mypassword' }, { cookie: 'gs_session=s-id' }));
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({
      secret: 'JBSWY3DPEHPK3PXP',
      otpauth_url: 'otpauth://totp/Directus:a@b.com?secret=JBSWY3DPEHPK3PXP',
    });
    expect(mocks.directusGenerateTfaSecret).toHaveBeenCalledWith('at-1', 'mypassword');
  });

  it('stashes the generated secret in pendingTfaStore keyed by session id', async () => {
    mocks.directusGenerateTfaSecret.mockResolvedValue({
      ok: true,
      value: { secret: 'JBSWY3DPEHPK3PXP', otpauthUrl: 'otpauth://x' },
    });
    await POST(makeRequest({ password: 'mypassword' }, { cookie: 'gs_session=s-id' }));
    expect(mocks.pendingTfaCreate).toHaveBeenCalledOnce();
    const [sessionId, data] = mocks.pendingTfaCreate.mock.calls[0]!;
    expect(sessionId).toBe('s-id');
    expect(data.secret).toBe('JBSWY3DPEHPK3PXP');
    expect(typeof data.expiresAt).toBe('number');
    expect(data.expiresAt).toBeGreaterThan(Date.now());
  });

  it('does not stash on Directus failure', async () => {
    mocks.directusGenerateTfaSecret.mockResolvedValue({ ok: false, error: 'invalid_password' });
    await POST(makeRequest({ password: 'wrong' }, { cookie: 'gs_session=s-id' }));
    expect(mocks.pendingTfaCreate).not.toHaveBeenCalled();
  });

  it('401 when no session cookie', async () => {
    const res = await POST(makeRequest({ password: 'pw' }));
    expect(res.status).toBe(401);
    expect(mocks.directusGenerateTfaSecret).not.toHaveBeenCalled();
  });

  it('401 when session cookie present but no server state', async () => {
    mocks.getValidatedSession.mockResolvedValue(null);
    const res = await POST(makeRequest({ password: 'pw' }, { cookie: 'gs_session=stale' }));
    expect(res.status).toBe(401);
  });

  it('401 when Directus rejects the password', async () => {
    mocks.directusGenerateTfaSecret.mockResolvedValue({ ok: false, error: 'invalid_password' });
    const res = await POST(makeRequest({ password: 'wrong' }, { cookie: 'gs_session=s-id' }));
    expect(res.status).toBe(401);
    expect(await res.json()).toEqual({ error: 'invalid_password' });
  });

  it('403 on cross-origin', async () => {
    const res = await POST(makeRequest({ password: 'pw' }, { cookie: 'gs_session=s-id', origin: 'https://evil.example.com' }));
    expect(res.status).toBe(403);
  });

  it('400 on missing password', async () => {
    const res = await POST(makeRequest({}, { cookie: 'gs_session=s-id' }));
    expect(res.status).toBe(400);
  });

  it('429 when tfaGenerateRateLimiter rejects (H1)', async () => {
    mocks.tfaGenerateRateLimiterCheck.mockReturnValue({ allowed: false, retryAfterMs: 1234 });
    const res = await POST(makeRequest({ password: 'pw' }, { cookie: 'gs_session=s-id' }));
    expect(res.status).toBe(429);
    expect(await res.json()).toEqual({ error: 'rate_limited', retry_after_ms: 1234 });
    expect(mocks.directusGenerateTfaSecret).not.toHaveBeenCalled();
  });
});
