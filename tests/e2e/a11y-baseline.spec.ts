// Accessibility baseline — axe-core scans against the auth pages (the only
// pages live in production today). WCAG 2.2 AA is the project floor; see
// docs/architecture/frontend-conventions.md.
//
// Each new UI step adds its own axe scan; this file stays as the
// authentication-surface guard.

import AxeBuilder from '@axe-core/playwright';
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

test.describe('a11y baseline (WCAG 2.2 AA)', () => {
  test('/login passes axe scan at WCAG 2.2 AA', async ({ page }) => {
    await page.goto('/login');
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    expect(results.violations).toEqual([]);
  });

  test('/login/2fa-setup passes axe scan at WCAG 2.2 AA (with session cookie)', async ({
    page,
    context,
  }) => {
    await addSessionCookie(context);
    await page.goto('/login/2fa-setup');
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    expect(results.violations).toEqual([]);
  });
});
