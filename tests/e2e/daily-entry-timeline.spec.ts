import AxeBuilder from '@axe-core/playwright';
import { test, expect, type BrowserContext } from '@playwright/test';

// Timeline (Blok 2) — Tab to "Tijdlijn" view, see the chart + streak,
// tap a point to open the editable bottom sheet, range toggle re-fetches.
//
// The PUT and range GETs are intercepted via page.route so we don't need
// real Directus state. The range GET returns a small fixture so the chart
// has tappable points.

async function addPlaceholderSession(context: BrowserContext) {
  await context.addCookies([
    {
      name: 'gs_session',
      value: 'placeholder-session-id',
      domain: 'localhost',
      path: '/',
      httpOnly: true,
      secure: false,
      sameSite: 'Strict',
    },
  ]);
}

test.describe('Timeline view — Blok 2', () => {
  test('switching to the Tijdlijn tab reveals the chart + streak counter', async ({ page, context }) => {
    await addPlaceholderSession(context);
    await page.goto('/');

    await page.getByRole('tab', { name: /tijdlijn/i }).click();

    // Empty data → "—" placeholder; chart present.
    await expect(page.getByRole('img', { name: /score-tijdlijn/i })).toBeVisible();
  });

  test('range toggle 30 → 90 fires a fetch', async ({ page, context }) => {
    await addPlaceholderSession(context);

    const requests: string[] = [];
    await page.route('**/api/day-entries?**', (route) => {
      requests.push(route.request().url());
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ entries: [] }),
      });
    });

    await page.goto('/');
    await page.getByRole('tab', { name: /tijdlijn/i }).click();
    await page.getByRole('radio', { name: /90 dagen/i }).click();

    await expect.poll(() => requests.length).toBeGreaterThanOrEqual(1);
    expect(requests[0]).toMatch(/\/api\/day-entries\?from=\d{4}-\d{2}-\d{2}&to=\d{4}-\d{2}-\d{2}/);
  });

  test('Escape closes the bottom sheet when opened from a chart point', async ({ page, context }) => {
    await addPlaceholderSession(context);

    // Range GET returns one fixture point we can tap.
    await page.route('**/api/day-entries?**', (route) => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          entries: [
            {
              date: '2026-05-26',
              score: 6,
              note: null,
              tag_ids: [],
              sub_scores: null,
              sleep_hours: null,
              special_event: null,
              project_entry_ids: [],
              calendar_event_ids: [],
              garmin: null,
              health: null,
              weather: null,
              derived: null,
              created_at: '2026-05-26T08:00:00.000Z',
              updated_at: '2026-05-26T08:00:00.000Z',
            },
          ],
        }),
      });
    });

    await page.goto('/');
    await page.getByRole('tab', { name: /tijdlijn/i }).click();
    // Toggle to 90 to trigger the fetch (30 is the default range, so
    // clicking it is a no-op).
    await page.getByRole('radio', { name: /90 dagen/i }).click();

    // Wait for the point to be in the chart, then tap.
    const point = page.getByRole('button', { name: /2026-05-26/ });
    await expect(point).toBeVisible();
    await point.click();

    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeVisible();

    await page.keyboard.press('Escape');
    await expect(dialog).not.toBeVisible();
  });

  test('axe-core scan on the timeline tab passes WCAG 2.2 AA', async ({ page, context }) => {
    await addPlaceholderSession(context);
    await page.route('**/api/day-entries?**', (route) => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ entries: [] }),
      });
    });

    await page.goto('/');
    await page.getByRole('tab', { name: /tijdlijn/i }).click();
    await expect(page.getByRole('img', { name: /score-tijdlijn/i })).toBeVisible();

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    expect(results.violations).toEqual([]);
  });
});
