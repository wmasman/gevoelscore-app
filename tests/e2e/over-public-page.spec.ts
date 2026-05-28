import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

// /over is the public backer-recruitment page. Two things matter:
// 1. Anonymous visitors (no session cookie) must reach it without redirect.
// 2. The mailto CTA must carry the right address + subject + body so the
//    visitor's mail client opens with a usable draft.

test.describe('/over public landing page', () => {
  test('renders for anonymous visitors without redirect to /login', async ({
    page,
  }) => {
    const response = await page.goto('/over');
    expect(response?.status()).toBe(200);
    expect(page.url()).toMatch(/\/over$/);
    await expect(page.getByRole('heading', { level: 1, name: 'Gevoelscore' })).toBeVisible();
  });

  test('mailto link targets the right address with subject and body', async ({
    page,
  }) => {
    await page.goto('/over');
    const link = page.getByRole('link', {
      name: /Willem@brightpath-studio\.nl/i,
    });
    await expect(link).toBeVisible();
    const href = await link.getAttribute('href');
    expect(href).not.toBeNull();
    expect(href!).toMatch(/^mailto:Willem@brightpath-studio\.nl\?/);
    expect(href!).toContain('subject=');
    expect(href!).toContain('Gevoelscore');
    expect(href!).toContain('body=');
    expect(href!).toContain('core+backer');
  });

  test('renders the four cardinal principles and the four-trait profile', async ({
    page,
  }) => {
    await page.goto('/over');
    await expect(
      page.getByRole('heading', { level: 2, name: /principes/i }),
    ).toBeVisible();
    await expect(
      page.getByRole('heading', { level: 2, name: /20 mensen/i }),
    ).toBeVisible();
    await expect(
      page.getByRole('heading', { level: 2, name: /wat ik zoek/i }),
    ).toBeVisible();
    // 4 principle bullets + 4 profile bullets = 8 list items across the page.
    const items = page.getByRole('listitem');
    await expect(items).toHaveCount(8);
  });

  test('passes axe-core accessibility scan with no WCAG 2 AA violations', async ({
    page,
  }) => {
    await page.goto('/over');
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'])
      .analyze();
    expect(results.violations).toEqual([]);
  });
});
