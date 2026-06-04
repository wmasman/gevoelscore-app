// Console-cleanliness smoke. Loads each unauthenticated route and
// asserts the browser console produces NO errors and NO uncaught
// page exceptions during first paint + post-hydration settle.
//
// Catches the class of bugs `npm run verify` cannot see because they
// only fire in a real SSR-then-hydrate browser:
//   - React hydration mismatches (#418) — server paint ≠ client paint
//   - Static-asset misroutings — manifest.webmanifest behind auth,
//     etc. (browser parses HTML as JSON and screams)
//   - Future CSP violations from new third-party scripts
//   - Bundled-code runtime exceptions (TDZ, undefined access) that
//     unit tests with mocks happen to miss
//
// Public surfaces only (no session cookie attached). Auth-gated screens
// (/, /settings, /timeline) need a logged-in fixture, which lives in a
// follow-up under tests/e2e/authed-* (deferred until we have a stable
// test-user seeding flow).
//
// Real bugs this would have caught had it existed earlier:
//   - 2026-06-04: 215× React #418 on /settings from
//     CalendarsSection's `now ?? new Date()` (commit 0cdb30b).
//   - 2026-06-04: 10× "Manifest: Line 1, column 1, Syntax error"
//     because middleware 307-redirected /manifest.webmanifest to
//     /login (commit 1a36a20).

import { test, expect, type ConsoleMessage } from '@playwright/test';

// Paths the matcher does NOT protect — load anonymously without redirect.
const PUBLIC_PATHS = ['/login', '/over'];

// Asset that the middleware MUST let through (PWA manifest). Loading the
// browser to /login already triggers a fetch of this, but we hit it
// directly to assert it parses as JSON.
const PUBLIC_ASSETS = ['/manifest.webmanifest'];

// Console messages outside our control. Keep this list TIGHT — every
// entry is a future bug that won't surface here. Empty by default.
const ALLOWED_CONSOLE_PATTERNS: RegExp[] = [
  // (none)
];

function isAllowed(msg: ConsoleMessage): boolean {
  const text = msg.text();
  return ALLOWED_CONSOLE_PATTERNS.some((p) => p.test(text));
}

test.describe('console cleanliness on public surfaces', () => {
  for (const path of PUBLIC_PATHS) {
    test(`${path} produces no console errors or page exceptions`, async ({ page }) => {
      const errors: string[] = [];

      page.on('pageerror', (e) => {
        errors.push(`pageerror: ${e.message}`);
      });
      page.on('console', (msg) => {
        if (msg.type() !== 'error') return;
        if (isAllowed(msg)) return;
        errors.push(`console.error: ${msg.text()}`);
      });

      const response = await page.goto(path, { waitUntil: 'networkidle' });
      expect(response, `no response for ${path}`).not.toBeNull();
      expect(response!.status(), `bad status for ${path}`).toBeLessThan(400);

      // Give React a tick to finish any post-mount work that might
      // log async errors (hydration warnings can be deferred).
      await page.waitForTimeout(500);

      expect(
        errors,
        `\nConsole errors on ${path}:\n  ${errors.join('\n  ')}\n`,
      ).toEqual([]);
    });
  }

  for (const path of PUBLIC_ASSETS) {
    test(`${path} is reachable and parses as the expected content-type`, async ({ request }) => {
      const res = await request.get(path);
      expect(res.status(), `${path} status`).toBe(200);
      const ct = res.headers()['content-type'] ?? '';
      // The manifest must serve as application/manifest+json or
      // application/json; both are valid. An HTML response means
      // middleware swallowed it (the 2026-06-04 bug).
      expect(
        ct,
        `${path} returned wrong content-type "${ct}" — middleware likely intercepted (saw bug 2026-06-04)`,
      ).toMatch(/(application\/(manifest\+)?json|application\/octet-stream)/);
      // Parse — fails if the body is HTML masquerading as something else.
      const body = await res.text();
      expect(
        () => JSON.parse(body),
        `${path} body did not parse as JSON`,
      ).not.toThrow();
    });
  }
});
