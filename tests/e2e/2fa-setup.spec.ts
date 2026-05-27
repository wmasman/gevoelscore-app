import { test, expect, type BrowserContext } from '@playwright/test';

async function addSessionCookie(context: BrowserContext) {
  await context.addCookies([
    {
      name: 'gs_session',
      value: 'mock-session-id',
      domain: 'localhost',
      path: '/',
      httpOnly: true,
      secure: false,
      sameSite: 'Strict',
    },
  ]);
}

test.describe('/login/2fa-setup page', () => {
  test('without gs_session cookie redirects to /login (AC15)', async ({ page }) => {
    await page.goto('/login/2fa-setup');
    await page.waitForURL(/\/login$/);
    expect(page.url()).toMatch(/\/login$/);
  });

  test('shows password input on initial load when authenticated', async ({ page, context }) => {
    await addSessionCookie(context);
    await page.goto('/login/2fa-setup');

    const pw = page.getByLabel(/wachtwoord/i);
    await expect(pw).toBeVisible();
    await expect(pw).toBeFocused();
    await expect(pw).toHaveAttribute('autocomplete', 'current-password');
  });

  test('valid password reveals secret + otpauth URL + OTP input (AC16)', async ({
    page,
    context,
  }) => {
    await addSessionCookie(context);

    await page.route('**/api/auth/2fa/generate', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          secret: 'JBSWY3DPEHPK3PXP',
          otpauth_url: 'otpauth://totp/Directus:a@b.com?secret=JBSWY3DPEHPK3PXP',
        }),
      }),
    );

    await page.goto('/login/2fa-setup');
    await page.getByLabel(/wachtwoord/i).fill('mypassword');
    await page.getByRole('button', { name: /genereer/i }).click();

    await expect(page.getByTestId('tfa-secret')).toContainText('JBSWY3DPEHPK3PXP');
    await expect(page.getByTestId('tfa-otpauth-url')).toContainText('otpauth://totp/');
    const otp = page.getByLabel(/code/i);
    await expect(otp).toBeVisible();
    await expect(otp).toHaveAttribute('inputmode', 'numeric');
    await expect(otp).toHaveAttribute('maxlength', '6');
  });

  test('wrong password shows generic error', async ({ page, context }) => {
    await addSessionCookie(context);

    await page.route('**/api/auth/2fa/generate', (route) =>
      route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'invalid_password' }),
      }),
    );

    await page.goto('/login/2fa-setup');
    await page.getByLabel(/wachtwoord/i).fill('wrong');
    await page.getByRole('button', { name: /genereer/i }).click();

    await expect(page.getByText(/wachtwoord onjuist/i)).toBeVisible();
  });

  test('valid OTP activates 2FA and navigates to / (AC17)', async ({ page, context }) => {
    await addSessionCookie(context);

    await page.route('**/api/auth/2fa/generate', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          secret: 'JBSWY3DPEHPK3PXP',
          otpauth_url: 'otpauth://totp/Directus:a@b.com?secret=JBSWY3DPEHPK3PXP',
        }),
      }),
    );
    await page.route('**/api/auth/2fa/enable', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ ok: true }),
      }),
    );

    await page.goto('/login/2fa-setup');
    await page.getByLabel(/wachtwoord/i).fill('mypassword');
    await page.getByRole('button', { name: /genereer/i }).click();
    await page.getByLabel(/code/i).fill('123456');

    await expect(page.getByText(/2fa actief/i)).toBeVisible();
    await page.waitForURL('http://localhost:3000/');
  });

  test('invalid OTP shows generic error and clears the input', async ({ page, context }) => {
    await addSessionCookie(context);

    await page.route('**/api/auth/2fa/generate', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          secret: 'JBSWY3DPEHPK3PXP',
          otpauth_url: 'otpauth://totp/Directus:a@b.com?secret=JBSWY3DPEHPK3PXP',
        }),
      }),
    );
    await page.route('**/api/auth/2fa/enable', (route) =>
      route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'invalid_otp' }),
      }),
    );

    await page.goto('/login/2fa-setup');
    await page.getByLabel(/wachtwoord/i).fill('mypassword');
    await page.getByRole('button', { name: /genereer/i }).click();
    await page.getByLabel(/code/i).fill('000000');

    await expect(page.getByText(/code ongeldig/i)).toBeVisible();
    await expect(page.getByLabel(/code/i)).toHaveValue('');
  });
});
