import { test, expect } from '@playwright/test';

test.describe('/login page', () => {
  test('email input is autofocused and has autocomplete=email', async ({ page }) => {
    await page.goto('/login');
    const email = page.getByLabel(/e-mail/i);
    await expect(email).toBeFocused();
    await expect(email).toHaveAttribute('autocomplete', 'email');
    await expect(email).toHaveAttribute('type', 'email');
  });

  test('password input has autocomplete=current-password', async ({ page }) => {
    await page.goto('/login');
    const pw = page.getByLabel(/wachtwoord/i);
    await expect(pw).toHaveAttribute('autocomplete', 'current-password');
    await expect(pw).toHaveAttribute('type', 'password');
  });

  test('successful login with {ok: true} navigates to /', async ({ page }) => {
    await page.route('**/api/auth/login', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        // Mirror the real route's Set-Cookie so middleware lets the / navigation through.
        // Real cookie includes Secure; tests run on HTTP so we drop it here.
        headers: {
          'set-cookie': 'gs_session=mock-session-id; Path=/; HttpOnly; SameSite=Strict; Max-Age=3600',
        },
        body: JSON.stringify({ ok: true }),
      }),
    );

    await page.goto('/login');
    await page.getByLabel(/e-mail/i).fill('user@example.com');
    await page.getByLabel(/wachtwoord/i).fill('correct-horse');
    await page.getByRole('button', { name: /aanmelden/i }).click();

    await page.waitForURL('http://localhost:3000/');
    expect(page.url()).toBe('http://localhost:3000/');
  });

  test('2FA-required response navigates to /login/verify', async ({ page }) => {
    await page.route('**/api/auth/login', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ requires_otp: true }),
      }),
    );

    await page.goto('/login');
    await page.getByLabel(/e-mail/i).fill('user@example.com');
    await page.getByLabel(/wachtwoord/i).fill('correct-horse');
    await page.getByRole('button', { name: /aanmelden/i }).click();

    await page.waitForURL(/\/login\/verify$/);
    expect(page.url()).toMatch(/\/login\/verify$/);
  });

  test('invalid credentials shows generic Dutch error', async ({ page }) => {
    await page.route('**/api/auth/login', (route) =>
      route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'invalid_credentials' }),
      }),
    );

    await page.goto('/login');
    await page.getByLabel(/e-mail/i).fill('user@example.com');
    await page.getByLabel(/wachtwoord/i).fill('wrong');
    await page.getByRole('button', { name: /aanmelden/i }).click();

    await expect(page.getByText(/onjuiste e-mail of wachtwoord/i)).toBeVisible();
  });

  test('Enter in the password field submits the form', async ({ page }) => {
    await page.route('**/api/auth/login', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        headers: {
          'set-cookie': 'gs_session=mock-session-id; Path=/; HttpOnly; SameSite=Strict; Max-Age=3600',
        },
        body: JSON.stringify({ ok: true }),
      }),
    );

    await page.goto('/login');
    await page.getByLabel(/e-mail/i).fill('user@example.com');
    await page.getByLabel(/wachtwoord/i).fill('correct-horse');
    await page.getByLabel(/wachtwoord/i).press('Enter');

    await page.waitForURL('http://localhost:3000/');
  });
});
