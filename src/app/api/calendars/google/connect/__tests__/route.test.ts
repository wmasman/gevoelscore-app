// Step-1 Phase 1.C — POST /api/calendars/google/connect tests.

import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  getValidatedSession: vi.fn(),
  writeCheck: vi.fn(),
  getGoogleProvider: vi.fn(),
}));

vi.mock('@/lib/auth/get-validated-session', () => ({
  getValidatedSession: mocks.getValidatedSession,
}));

vi.mock('@/lib/auth/stores', async () => {
  const actual = await vi.importActual<typeof import('@/lib/auth/stores')>(
    '@/lib/auth/stores',
  );
  return {
    ...actual,
    calendarWriteRateLimiter: {
      check: mocks.writeCheck,
      sweep: () => undefined,
    },
  };
});

vi.mock('@/lib/integrations/google/get-provider', () => ({
  getGoogleProvider: mocks.getGoogleProvider,
}));

import { POST } from '../route';

function makePost(opts: { cookie?: string; origin?: string } = {}): Request {
  const headers: Record<string, string> = {
    origin: opts.origin ?? 'http://localhost:3000',
    'content-type': 'application/json',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  return new Request('http://localhost:3000/api/calendars/google/connect', {
    method: 'POST',
    headers,
  });
}

beforeEach(() => {
  mocks.getValidatedSession.mockReset();
  mocks.writeCheck.mockReset();
  mocks.getGoogleProvider.mockReset();
  mocks.getValidatedSession.mockResolvedValue({
    accessToken: 'at',
    refreshToken: 'rt',
    expiresAt: Date.now() + 60_000,
  });
  mocks.writeCheck.mockReturnValue({ allowed: true });
  mocks.getGoogleProvider.mockReturnValue({
    id: 'google',
    buildAuthUrl: (state: string, redirectUri: string) =>
      `https://accounts.google.com/o/oauth2/v2/auth?state=${state}&redirect_uri=${encodeURIComponent(redirectUri)}`,
  });
});

describe('POST /api/calendars/google/connect', () => {
  it('test 38: bad origin → 403 forbidden', async () => {
    const request = makePost({ origin: 'https://evil.example' });

    const res = await POST(request);

    expect(res.status).toBe(403);
    expect((await res.json()).error).toBe('forbidden');
  });

  it('test 39: no session cookie → 401 unauthenticated', async () => {
    const request = makePost();

    const res = await POST(request);

    expect(res.status).toBe(401);
  });

  it('test 40: rate-limited → 429', async () => {
    mocks.writeCheck.mockReturnValue({ allowed: false, retryAfterMs: 30000 });

    const request = makePost({ cookie: 'gs_session=s-1' });
    const res = await POST(request);

    expect(res.status).toBe(429);
  });

  it('test 41: happy path → 200 with redirect_url and cal_oauth_state cookie set', async () => {
    const request = makePost({ cookie: 'gs_session=s-1' });

    const res = await POST(request);

    expect(res.status).toBe(200);
    const body = (await res.json()) as { redirect_url: string };
    expect(body.redirect_url).toContain('accounts.google.com');
    const setCookie = res.headers.get('Set-Cookie');
    expect(setCookie).toContain('cal_oauth_state=');
    expect(setCookie).toContain('HttpOnly');
    expect(setCookie).toContain('Secure');
    expect(setCookie).toContain('SameSite=Lax');
    expect(setCookie).toContain('Max-Age=600');
  });

  it('test 42: redirect_url contains the same state as the cookie', async () => {
    const request = makePost({ cookie: 'gs_session=s-1' });

    const res = await POST(request);

    const body = (await res.json()) as { redirect_url: string };
    const urlState = new URL(body.redirect_url).searchParams.get('state');
    const setCookie = res.headers.get('Set-Cookie') ?? '';
    const cookieMatch = /cal_oauth_state=([^;]+)/.exec(setCookie);
    const cookieState = cookieMatch?.[1];

    expect(urlState).toBeTruthy();
    expect(urlState).toBe(cookieState);
  });

  it('test 43: missing GOOGLE_CLIENT_ID/SECRET → 500 server_error (provider factory throws)', async () => {
    mocks.getGoogleProvider.mockImplementation(() => {
      throw new Error('GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set');
    });

    const request = makePost({ cookie: 'gs_session=s-1' });
    const res = await POST(request);

    expect(res.status).toBe(500);
    expect((await res.json()).error).toBe('server_error');
  });
});
