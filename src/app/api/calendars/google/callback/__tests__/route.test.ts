// Step-1 Phase 1.C — GET /api/calendars/google/callback tests.

import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  getValidatedSession: vi.fn(),
  upsertConnection: vi.fn(),
  encrypt: vi.fn(),
  getGoogleProvider: vi.fn(),
}));

vi.mock('@/lib/auth/get-validated-session', () => ({
  getValidatedSession: mocks.getValidatedSession,
}));

vi.mock('@/lib/api/calendars', () => ({
  upsertConnection: mocks.upsertConnection,
}));

vi.mock('@/lib/auth/envelope-encryption', () => ({
  encrypt: mocks.encrypt,
}));

vi.mock('@/lib/integrations/google/get-provider', () => ({
  getGoogleProvider: mocks.getGoogleProvider,
}));

import { GET } from '../route';

function makeGet(opts: {
  state?: string;
  code?: string;
  cookies?: string;
}): Request {
  const params = new URLSearchParams();
  if (opts.state) params.set('state', opts.state);
  if (opts.code) params.set('code', opts.code);
  const url = `http://localhost:3000/api/calendars/google/callback?${params.toString()}`;
  const headers: Record<string, string> = {};
  if (opts.cookies !== undefined) headers.cookie = opts.cookies;
  return new Request(url, { method: 'GET', headers });
}

beforeEach(() => {
  vi.unstubAllEnvs();
  vi.stubEnv('WILLEM_USER_ID', '16f6f68b-e683-4dc9-8afc-e80695c4259d');
  vi.stubEnv('CALENDAR_KEK', 'test-kek-32-bytes-base64-pad-here==');
  vi.stubEnv('DIRECTUS_TOKEN', 'at');

  mocks.getValidatedSession.mockReset();
  mocks.upsertConnection.mockReset();
  mocks.encrypt.mockReset();
  mocks.getGoogleProvider.mockReset();

  mocks.getValidatedSession.mockResolvedValue({
    accessToken: 'at',
    refreshToken: 'rt',
    expiresAt: Date.now() + 60_000,
  });
  mocks.encrypt.mockReturnValue('v1.iv.ct.tag');
  mocks.upsertConnection.mockResolvedValue({ ok: true, value: 'conn-1' });
  mocks.getGoogleProvider.mockReturnValue({
    id: 'google',
    exchangeCode: async () => ({
      refreshToken: 'fake-refresh',
      accessToken: 'fake-access',
      expiresAt: new Date(Date.now() + 3600_000),
      accountEmail: 'user@example.com',
    }),
  });
});

describe('GET /api/calendars/google/callback', () => {
  it('test 44: state_mismatch (query state != cookie state) → 400', async () => {
    const request = makeGet({
      state: 'bad-state',
      code: 'auth-code',
      cookies: 'cal_oauth_state=good-state; gs_session=s-1',
    });

    const res = await GET(request);

    expect(res.status).toBe(400);
    expect((await res.json()).error).toBe('state_mismatch');
  });

  it('test 45: state_missing (no cal_oauth_state cookie) → 400', async () => {
    const request = makeGet({
      state: 'some-state',
      code: 'auth-code',
      cookies: 'gs_session=s-1',
    });

    const res = await GET(request);

    expect(res.status).toBe(400);
    expect((await res.json()).error).toBe('state_missing');
  });

  it('test 46: no session cookie → 401 unauthenticated', async () => {
    const request = makeGet({
      state: 'good-state',
      code: 'auth-code',
      cookies: 'cal_oauth_state=good-state',
    });

    const res = await GET(request);

    expect(res.status).toBe(401);
  });

  it('test 47: happy path → 302 redirect to /settings/kalenders/choose?connection_id=...', async () => {
    const request = makeGet({
      state: 'good-state',
      code: 'auth-code',
      cookies: 'cal_oauth_state=good-state; gs_session=s-1',
    });

    const res = await GET(request);

    expect(res.status).toBe(302);
    expect(res.headers.get('Location')).toContain(
      '/settings/kalenders/choose?connection_id=conn-1',
    );
    // Clear state cookie set
    const setCookie = res.headers.get('Set-Cookie');
    expect(setCookie).toContain('cal_oauth_state=');
    expect(setCookie).toContain('Max-Age=0');
  });

  it('test 48: upsertConnection is called with the encrypted refresh token + account email', async () => {
    const request = makeGet({
      state: 'good-state',
      code: 'auth-code',
      cookies: 'cal_oauth_state=good-state; gs_session=s-1',
    });

    await GET(request);

    expect(mocks.encrypt).toHaveBeenCalledWith(
      'fake-refresh',
      'test-kek-32-bytes-base64-pad-here==',
    );
    expect(mocks.upsertConnection).toHaveBeenCalledWith(
      'at',
      expect.objectContaining({
        user_id: '16f6f68b-e683-4dc9-8afc-e80695c4259d',
        provider: 'google',
        provider_account_email: 'user@example.com',
        refresh_token_encrypted: 'v1.iv.ct.tag',
      }),
    );
  });

  it('test 49: exchangeCode failure → 502 oauth_exchange_failed', async () => {
    mocks.getGoogleProvider.mockReturnValue({
      id: 'google',
      exchangeCode: async () => {
        throw new Error('google_api_invalid_response');
      },
    });

    const request = makeGet({
      state: 'good-state',
      code: 'auth-code',
      cookies: 'cal_oauth_state=good-state; gs_session=s-1',
    });

    const res = await GET(request);

    expect(res.status).toBe(502);
    expect((await res.json()).error).toBe('oauth_exchange_failed');
  });

  it('test 50: upsertConnection error → 502 directus_error', async () => {
    mocks.upsertConnection.mockResolvedValue({
      ok: false,
      error: 'directus_error',
    });

    const request = makeGet({
      state: 'good-state',
      code: 'auth-code',
      cookies: 'cal_oauth_state=good-state; gs_session=s-1',
    });

    const res = await GET(request);

    expect(res.status).toBe(502);
    expect((await res.json()).error).toBe('directus_error');
  });
});
