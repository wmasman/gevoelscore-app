import { test, expect, type BrowserContext } from '@playwright/test';

// Row-tap → PUT round-trip. With a placeholder session cookie, the home
// page renders the shell in idle state (getValidatedSession returns null,
// page.tsx falls through with entry=null) — perfect for testing the
// "fresh day first interaction" path.
//
// The PUT /api/day-entries/[date] route is intercepted via page.route so
// we don't need real Directus state — we're testing the row's wiring,
// not the upsert itself (covered by unit + live-stack specs).

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

test.describe('Score row — fresh-day interaction', () => {
  test('tap a value: fires PUT and the row flips to set state', async ({ page, context }) => {
    await addPlaceholderSession(context);

    const requests: { url: string; body: string | null }[] = [];
    await page.route('**/api/day-entries/**', (route) => {
      const req = route.request();
      requests.push({ url: req.url(), body: req.postData() });
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          entry: {
            date: '2026-05-28',
            score: 7,
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
            created_at: '2026-05-28T08:00:00.000Z',
            updated_at: '2026-05-28T08:00:00.000Z',
          },
        }),
      });
    });

    await page.goto('/');
    const row = page.getByRole('listbox', { name: /score/i });
    await expect(row).toHaveAttribute('data-phase', 'idle');

    await row.getByRole('option', { name: '7' }).click();

    // PUT fired with score:7
    await expect.poll(() => requests.length).toBeGreaterThanOrEqual(1);
    expect(requests[0]!.url).toMatch(/\/api\/day-entries\/\d{4}-\d{2}-\d{2}$/);
    expect(JSON.parse(requests[0]!.body!)).toEqual({ score: 7 });

    // Row is now in set phase, value 7 selected
    await expect(row).toHaveAttribute('data-phase', 'set');
    await expect(row.getByRole('option', { selected: true })).toHaveText('7');
  });

  test('keyboard ArrowRight changes centred value and triggers PUT', async ({ page, context }) => {
    await addPlaceholderSession(context);

    const requests: { body: string | null }[] = [];
    await page.route('**/api/day-entries/**', (route) => {
      requests.push({ body: route.request().postData() });
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ entry: {} }) });
    });

    await page.goto('/');
    const row = page.getByRole('listbox', { name: /score/i });
    await row.focus();
    // ArrowRight moves towards higher values (5 → 6 → 7)
    await page.keyboard.press('ArrowRight');

    await expect.poll(() => requests.length).toBeGreaterThanOrEqual(1);
    expect(JSON.parse(requests[0]!.body!)).toEqual({ score: 6 });
    await expect(row).toHaveAttribute('data-phase', 'set');
  });

  test('ArrowDown alias is preserved (Step 4 muscle memory)', async ({ page, context }) => {
    await addPlaceholderSession(context);

    const requests: { body: string | null }[] = [];
    await page.route('**/api/day-entries/**', (route) => {
      requests.push({ body: route.request().postData() });
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ entry: {} }) });
    });

    await page.goto('/');
    const row = page.getByRole('listbox', { name: /score/i });
    await row.focus();
    await page.keyboard.press('ArrowDown');

    await expect.poll(() => requests.length).toBeGreaterThanOrEqual(1);
    expect(JSON.parse(requests[0]!.body!)).toEqual({ score: 6 });
  });

  test('failed PUT shows error banner in the page footer + warn glyph in the header', async ({ page, context }) => {
    await addPlaceholderSession(context);

    await page.route('**/api/day-entries/**', (route) => {
      route.fulfill({
        status: 502,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'server_error' }),
      });
    });

    await page.goto('/');
    const row = page.getByRole('listbox', { name: /score/i });
    await row.getByRole('option', { name: '8' }).click();

    // The banner (under the row) carries the actionable Dutch message.
    await expect(page.getByText(/niet opgeslagen/i)).toBeVisible();
    // The header glyph carries the ambient indicator. role="status" with
    // aria-label "Niet opgeslagen". Multiple role=status may be present
    // (Next's hidden announcer); we identify ours by accessible name.
    const glyph = page.getByRole('status', { name: /niet opgeslagen/i });
    await expect(glyph).toBeVisible();
  });
});
