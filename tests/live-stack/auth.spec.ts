import { test, expect } from '@playwright/test';

const EMAIL = process.env.PLAYWRIGHT_TEST_EMAIL;
const PASSWORD = process.env.PLAYWRIGHT_TEST_PASSWORD;

const hasCreds = typeof EMAIL === 'string' && typeof PASSWORD === 'string';

test.describe('Real Directus auth', () => {
  test.skip(!hasCreds, 'PLAYWRIGHT_TEST_EMAIL / PASSWORD not set in .env.local — see step-8 docs');

  test('AC3: invalid credentials return 401 invalid_credentials (real Directus envelope)', async ({
    request,
  }) => {
    const res = await request.post('/api/auth/login', {
      data: { email: EMAIL, password: 'definitely-not-the-real-password-' + Date.now() },
    });

    expect(res.status()).toBe(401);
    expect(await res.json()).toEqual({ error: 'invalid_credentials' });
    expect(res.headers()['set-cookie']).toBeFalsy();
  });

  test('AC1 or AC2: valid credentials yield either {ok:true} + session cookie OR {requires_otp:true} + pending cookie', async ({
    request,
  }) => {
    const res = await request.post('/api/auth/login', {
      data: { email: EMAIL, password: PASSWORD },
    });

    expect(res.status()).toBe(200);
    const body = (await res.json()) as { ok?: true; requires_otp?: true };

    if (body.requires_otp) {
      // 2FA-enabled account path (AC2). Pending cookie set.
      const setCookie = res.headers()['set-cookie'] ?? '';
      expect(setCookie).toContain('gs_pending_otp=');
      expect(setCookie).toContain('HttpOnly');
      expect(setCookie).toContain('SameSite=Strict');
      expect(setCookie).toContain('Max-Age=300');
    } else if (body.ok) {
      // No-2FA path (AC1). Session cookie set. Verify attrs, then log out
      // immediately so we don't accumulate refresh tokens in Directus.
      const setCookie = res.headers()['set-cookie'] ?? '';
      expect(setCookie).toContain('gs_session=');
      expect(setCookie).toContain('HttpOnly');
      expect(setCookie).toContain('SameSite=Strict');
      expect(setCookie).toContain('Path=/');

      // AC13: logout invalidates the refresh token on the Directus side.
      // Extract cookie value and forward it on logout.
      const sessionMatch = setCookie.match(/gs_session=([^;]+)/);
      expect(sessionMatch).not.toBeNull();
      const sessionValue = sessionMatch![1];

      const logoutRes = await request.post('/api/auth/logout', {
        headers: { cookie: `gs_session=${sessionValue}` },
      });
      expect(logoutRes.status()).toBe(200);
    } else {
      throw new Error('Unexpected response body shape: ' + JSON.stringify(body));
    }
  });
});
