import { test, expect } from '@playwright/test';

// Home is auth-gated by middleware (step 6 of login). Every test sets a
// placeholder session cookie before navigation — middleware only checks
// cookie presence, the page itself doesn't validate the value yet.
test.describe('Home page (authenticated)', () => {
  test.beforeEach(async ({ context }) => {
    await context.addCookies([
      {
        name: 'gs_session',
        value: 'test-fixture-session-id',
        domain: 'localhost',
        path: '/',
        httpOnly: true,
        secure: false,
        sameSite: 'Strict',
      },
    ]);
  });

  test('renders the app name', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Gevoelscore', level: 1 })).toBeVisible();
  });

  test('sets the Dutch language attribute', async ({ page }) => {
    await page.goto('/');
    const lang = await page.locator('html').getAttribute('lang');
    expect(lang).toBe('nl');
  });

  test('has the correct document title', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Gevoelscore/);
  });
});
