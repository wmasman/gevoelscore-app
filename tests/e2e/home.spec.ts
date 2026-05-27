import { test, expect } from '@playwright/test';

test.describe('Home page', () => {
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
