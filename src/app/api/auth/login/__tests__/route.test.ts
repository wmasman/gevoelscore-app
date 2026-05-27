import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  directusLogin: vi.fn(),
  loginRateCheck: vi.fn(),
  sessionCreate: vi.fn(),
  pendingOtpCreate: vi.fn(),
}));

vi.mock('@/lib/auth/directus-auth', () => ({
  directusLogin: mocks.directusLogin,
}));

vi.mock('@/lib/auth/stores', () => ({
  loginRateLimiter: { check: mocks.loginRateCheck, sweep: vi.fn(), size: vi.fn() },
  verifyRateLimiter: { check: vi.fn(), sweep: vi.fn(), size: vi.fn() },
  sessionStore: {
    create: mocks.sessionCreate,
    get: vi.fn(),
    delete: vi.fn(),
    cleanupExpired: vi.fn(),
    size: vi.fn(),
  },
  pendingOtpStore: {
    create: mocks.pendingOtpCreate,
    get: vi.fn(),
    delete: vi.fn(),
    cleanupExpired: vi.fn(),
    size: vi.fn(),
  },
  getClientIp: () => '1.2.3.4',
}));

import { POST } from '../route';

function makeRequest(body: unknown, headers: Record<string, string> = {}) {
  return new Request('http://localhost:3000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', origin: 'http://localhost:3000', ...headers },
    body: JSON.stringify(body),
  });
}

describe('POST /api/auth/login', () => {
  beforeEach(() => {
    mocks.directusLogin.mockReset();
    mocks.loginRateCheck.mockReset();
    mocks.sessionCreate.mockReset();
    mocks.pendingOtpCreate.mockReset();
    // Defaults: rate-limit allows, session/pending create return fixed ids
    mocks.loginRateCheck.mockReturnValue({ allowed: true, remaining: 4 });
    mocks.sessionCreate.mockReturnValue('session-id-1');
    mocks.pendingOtpCreate.mockReturnValue('pending-id-1');
  });

  it('AC1: valid creds without 2FA → 200, session cookie set', async () => {
    mocks.directusLogin.mockResolvedValue({
      ok: true,
      value: { accessToken: 'at', refreshToken: 'rt', expiresInMs: 3600_000 },
    });

    const res = await POST(makeRequest({ email: 'a@b.com', password: 'pw' }));
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body).toEqual({ ok: true });

    const setCookie = res.headers.get('set-cookie') ?? '';
    expect(setCookie).toContain('gs_session=session-id-1');
    expect(setCookie).toContain('HttpOnly');
    expect(setCookie).toContain('Secure');
    expect(setCookie).toContain('SameSite=Strict');
    expect(setCookie).toContain('Path=/');
    expect(mocks.sessionCreate).toHaveBeenCalledWith(
      expect.objectContaining({ accessToken: 'at', refreshToken: 'rt' }),
    );
  });

  it('AC2: 2FA-required account → 200 with requires_otp=true, pending cookie set', async () => {
    mocks.directusLogin.mockResolvedValue({ ok: false, error: 'otp_required' });

    const res = await POST(makeRequest({ email: 'a@b.com', password: 'pw' }));
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ requires_otp: true });

    const setCookie = res.headers.get('set-cookie') ?? '';
    expect(setCookie).toContain('gs_pending_otp=pending-id-1');
    expect(setCookie).toContain('HttpOnly');
    expect(setCookie).toContain('SameSite=Strict');
    expect(setCookie).toContain('Max-Age=300');
    expect(mocks.pendingOtpCreate).toHaveBeenCalledWith(
      expect.objectContaining({ email: 'a@b.com', password: 'pw' }),
    );
  });

  it('AC3: invalid credentials → 401 with generic error', async () => {
    mocks.directusLogin.mockResolvedValue({ ok: false, error: 'invalid_credentials' });

    const res = await POST(makeRequest({ email: 'a@b.com', password: 'wrong' }));
    expect(res.status).toBe(401);
    expect(await res.json()).toEqual({ error: 'invalid_credentials' });
    expect(res.headers.get('set-cookie')).toBeNull();
  });

  it('AC3 (extended): network error → 401 with same generic error (no info leak)', async () => {
    mocks.directusLogin.mockResolvedValue({ ok: false, error: 'network_error' });

    const res = await POST(makeRequest({ email: 'a@b.com', password: 'pw' }));
    expect(res.status).toBe(401);
    expect(await res.json()).toEqual({ error: 'invalid_credentials' });
  });

  it('AC5: rate-limited → 429', async () => {
    mocks.loginRateCheck.mockReturnValue({ allowed: false, retryAfterMs: 30_000 });

    const res = await POST(makeRequest({ email: 'a@b.com', password: 'pw' }));
    expect(res.status).toBe(429);
    expect(mocks.directusLogin).not.toHaveBeenCalled();
  });

  it('A08: cross-origin request → 403', async () => {
    const res = await POST(makeRequest({ email: 'a@b.com', password: 'pw' }, { origin: 'https://evil.example.com' }));
    expect(res.status).toBe(403);
    expect(mocks.directusLogin).not.toHaveBeenCalled();
  });

  it('400 on missing email', async () => {
    const res = await POST(makeRequest({ password: 'pw' }));
    expect(res.status).toBe(400);
    expect(mocks.directusLogin).not.toHaveBeenCalled();
  });

  it('400 on missing password', async () => {
    const res = await POST(makeRequest({ email: 'a@b.com' }));
    expect(res.status).toBe(400);
  });

  it('400 on email without @', async () => {
    const res = await POST(makeRequest({ email: 'notanemail', password: 'pw' }));
    expect(res.status).toBe(400);
  });

  it('400 on malformed JSON', async () => {
    const req = new Request('http://localhost:3000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', origin: 'http://localhost:3000' },
      body: 'not json',
    });
    const res = await POST(req);
    expect(res.status).toBe(400);
  });
});
