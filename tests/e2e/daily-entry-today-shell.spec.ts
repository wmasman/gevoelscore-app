import { test, expect, type BrowserContext } from '@playwright/test';

// The today-shell layout itself is unit-tested in
// src/components/__tests__/today-shell.test.tsx. This e2e covers the auth
// boundary at the page level: with no session cookie the middleware
// redirects; with a placeholder cookie (no server-side session) the page
// renders the empty Today shell — strict validation happens at the API
// call surface when the wheel actually saves (Step 4).
//
// Matches the trade-off documented in
// docs/features/auth-hardening/step-1-bind-tfa-secret.md.

async function addPlaceholderSession(context: BrowserContext) {
  await context.addCookies([
    {
      name: 'gs_session',
      value: 'placeholder-session-id-no-server-entry',
      domain: 'localhost',
      path: '/',
      httpOnly: true,
      secure: false,
      sameSite: 'Strict',
    },
  ]);
}

test.describe('GET / — Today screen', () => {
  test('without any cookie, middleware redirects to /login', async ({ page }) => {
    await page.goto('/');
    await page.waitForURL(/\/login$/);
    expect(page.url()).toMatch(/\/login$/);
  });

  test('with a session cookie, renders the Today shell (entry null on placeholder)', async ({
    page,
    context,
  }) => {
    await addPlaceholderSession(context);
    await page.goto('/');
    // Date heading visible.
    await expect(
      page.getByRole('heading', {
        name: /^(maandag|dinsdag|woensdag|donderdag|vrijdag|zaterdag|zondag) /i,
        level: 1,
      }),
    ).toBeVisible();
    // Score wheel (listbox role) present with 10 options.
    const wheel = page.getByRole('listbox', { name: /score/i });
    await expect(wheel).toBeVisible();
    expect(await wheel.getByRole('option').count()).toBe(10);
  });
});
