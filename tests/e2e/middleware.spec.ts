import { test, expect } from '@playwright/test';

test.describe('middleware: protected-route gating (AC14)', () => {
  test('GET / without session cookie redirects to /login', async ({ page }) => {
    await page.goto('/');
    await page.waitForURL(/\/login$/);
    expect(page.url()).toMatch(/\/login$/);
  });

  test('GET / with gs_session cookie renders the page (no redirect)', async ({ page, context }) => {
    await context.addCookies([
      {
        name: 'gs_session',
        value: 'anything-middleware-only-checks-presence',
        domain: 'localhost',
        path: '/',
        httpOnly: true,
        secure: false,
        sameSite: 'Strict',
      },
    ]);

    await page.goto('/');
    expect(page.url()).toBe('http://localhost:3000/');
    // Step 2: home is now the Today screen; h1 reads the Dutch date.
    await expect(
      page.getByRole('heading', {
        name: /^(maandag|dinsdag|woensdag|donderdag|vrijdag|zaterdag|zondag) /i,
        level: 1,
      }),
    ).toBeVisible();
  });

  test('GET /login without cookie does NOT redirect (avoids loop)', async ({ page }) => {
    await page.goto('/login');
    expect(page.url()).toMatch(/\/login$/);
    await expect(page.getByLabel(/e-mail/i)).toBeVisible();
  });

  test('GET /api/health without cookie returns 200', async ({ request }) => {
    const res = await request.get('/api/health');
    expect(res.status()).toBe(200);
    expect(await res.json()).toEqual({ status: 'ok' });
  });

  test('POST /api/auth/login without cookie is reached by the route handler (not redirected by middleware)', async ({
    request,
  }) => {
    // Cross-origin Origin header → handler returns 403.
    // If middleware were intercepting, we'd get a 302 or HTML redirect instead.
    const res = await request.post('/api/auth/login', {
      data: { email: 'a@b.test', password: 'x' },
      headers: { origin: 'https://evil.example.com' },
    });
    expect([400, 401, 403]).toContain(res.status());
  });

  test('GET /api/probe without cookie returns 401 JSON (M2)', async ({ request }) => {
    // No /api/probe route exists; the middleware should return 401 JSON before
    // any route handler is invoked. The point: fetch clients hitting a future
    // /api/day-entries without a session get a parseable JSON 401 instead of
    // an HTML redirect.
    const res = await request.get('/api/probe', { maxRedirects: 0 });
    expect(res.status()).toBe(401);
    expect(res.headers()['content-type']).toMatch(/application\/json/);
    expect(await res.json()).toEqual({ error: 'unauthenticated' });
  });
});
