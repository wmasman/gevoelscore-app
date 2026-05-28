import AxeBuilder from '@axe-core/playwright';
import { test, expect, type BrowserContext } from '@playwright/test';

// Note + tags interaction round-trip. With a placeholder session the home
// page renders the shell in idle state — first wheel tap promotes the
// composite to editable, then the note + tags can be exercised. The PUT
// route is intercepted via page.route so we don't need real Directus state.
//
// Test 4 runs axe-core for WCAG 2.2 AA conformance on the post-render
// today screen (per Step 5 AC4 of the e2e plan).

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

test.describe('Note + tag picker — interaction round-trip', () => {
  test('first wheel tap enables note + tags; typing note + tab away fires PUT', async ({
    page,
    context,
  }) => {
    await addPlaceholderSession(context);

    const requests: { body: string | null }[] = [];
    await page.route('**/api/day-entries/**', (route) => {
      requests.push({ body: route.request().postData() });
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ entry: {} }),
      });
    });

    await page.goto('/');

    // Initially disabled.
    const textarea = page.getByRole('textbox', { name: /notitie/i });
    await expect(textarea).toBeDisabled();

    // Promote to editable.
    await page.getByRole('listbox', { name: /score/i }).getByRole('option', { name: '6' }).click();
    await expect(textarea).not.toBeDisabled();

    // Type + blur → PUT lands.
    await textarea.fill('rustige avond');
    await textarea.blur();

    await expect.poll(() => requests.length).toBeGreaterThanOrEqual(2);
    const noteReq = requests.find((r) => r.body !== null && JSON.parse(r.body).note !== undefined);
    expect(noteReq).toBeDefined();
    expect(JSON.parse(noteReq!.body!).note).toBe('rustige avond');
  });

  test('multiple categories can be expanded at once', async ({ page, context }) => {
    await addPlaceholderSession(context);
    await page.route('**/api/day-entries/**', (route) => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ entry: {} }),
      });
    });

    await page.goto('/');
    await page.getByRole('listbox', { name: /score/i }).getByRole('option', { name: '7' }).click();

    const mentaal = page.getByRole('button', { name: /mentaal/i });
    const fysiek = page.getByRole('button', { name: /fysiek/i });

    await mentaal.click();
    await expect(mentaal).toHaveAttribute('aria-expanded', 'true');

    await fysiek.click();
    await expect(fysiek).toHaveAttribute('aria-expanded', 'true');
    // Mentaal still open.
    await expect(mentaal).toHaveAttribute('aria-expanded', 'true');
  });

  test('axe-core scan: today screen passes WCAG 2.2 AA', async ({ page, context }) => {
    await addPlaceholderSession(context);
    await page.route('**/api/day-entries/**', (route) => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ entry: {} }),
      });
    });

    await page.goto('/');
    // Wait for the wheel listbox to confirm hydration.
    await expect(page.getByRole('listbox', { name: /score/i })).toBeVisible();

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    expect(results.violations).toEqual([]);
  });
});
