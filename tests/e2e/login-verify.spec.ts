import { test, expect } from '@playwright/test';

test.describe('/login/verify page', () => {
  test('without gs_pending_otp cookie redirects to /login (AC10)', async ({ page }) => {
    await page.goto('/login/verify');
    await page.waitForURL(/\/login$/);
    expect(page.url()).toMatch(/\/login$/);
  });

  test('with pending cookie renders the OTP form with numeric inputmode', async ({ page, context }) => {
    await context.addCookies([
      {
        name: 'gs_pending_otp',
        value: 'fake-pending-id',
        domain: 'localhost',
        path: '/',
        httpOnly: true,
        secure: false,
        sameSite: 'Strict',
      },
    ]);

    await page.goto('/login/verify');
    const otp = page.getByLabel(/code/i);
    await expect(otp).toBeVisible();
    await expect(otp).toHaveAttribute('inputmode', 'numeric');
    await expect(otp).toHaveAttribute('maxlength', '6');
  });

  test('typing 6 digits auto-submits and navigates to / on {ok: true}', async ({ page, context }) => {
    await context.addCookies([
      {
        name: 'gs_pending_otp',
        value: 'fake-pending-id',
        domain: 'localhost',
        path: '/',
        httpOnly: true,
        secure: false,
        sameSite: 'Strict',
      },
    ]);

    await page.route('**/api/auth/login/verify', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        // Mirror the real route's Set-Cookie so middleware lets the / navigation through.
        headers: {
          'set-cookie': 'gs_session=mock-session-id; Path=/; HttpOnly; SameSite=Strict; Max-Age=3600',
        },
        body: JSON.stringify({ ok: true }),
      }),
    );

    await page.goto('/login/verify');
    // Auto-submit: typing 6 chars should fire the POST without an explicit submit button click
    await page.getByLabel(/code/i).fill('123456');
    await page.waitForURL('http://localhost:3000/');
  });

  test('non-digit characters are filtered out', async ({ page, context }) => {
    await context.addCookies([
      {
        name: 'gs_pending_otp',
        value: 'fake-pending-id',
        domain: 'localhost',
        path: '/',
        httpOnly: true,
        secure: false,
        sameSite: 'Strict',
      },
    ]);

    await page.goto('/login/verify');
    const otp = page.getByLabel(/code/i);
    await otp.fill('12a34b');
    await expect(otp).toHaveValue('1234');
  });

  test('invalid OTP shows generic error and clears the input', async ({ page, context }) => {
    await context.addCookies([
      {
        name: 'gs_pending_otp',
        value: 'fake-pending-id',
        domain: 'localhost',
        path: '/',
        httpOnly: true,
        secure: false,
        sameSite: 'Strict',
      },
    ]);

    await page.route('**/api/auth/login/verify', (route) =>
      route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'invalid_otp' }),
      }),
    );

    await page.goto('/login/verify');
    await page.getByLabel(/code/i).fill('000000');

    await expect(page.getByText(/code ongeldig/i)).toBeVisible();
    await expect(page.getByLabel(/code/i)).toHaveValue('');
  });
});
