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
    await expect(page.getByRole('heading', { name: 'Gevoelscore', level: 1 })).toBeVisible();
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
});
