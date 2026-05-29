// Drives the deployed app as a real signed-in user (the no-2FA verify
// bot). Captures screenshots of the authenticated surfaces — TodayShell
// with the auto-appearing popout, the Tijdlijn tab, the Settings page.
//
// CRITICAL: This script never drags the score circle. The ScoreCircle's
// onCommit triggers a save and day_entries is keyed only by date (no
// owner column), so a save by the verify-bot would clobber whichever
// row is currently there. The popout is opened, photographed, and
// closed via the X button without committing.
//
// Run:
//   $env:TEST_EMAIL = "..."; $env:TEST_PASSWORD = "..."
//   node scripts/verify-prod-authed.mjs

import { chromium } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

const BASE = 'https://gevoelscore-frontend.fly.dev';
const EMAIL = process.env.TEST_EMAIL;
const PASSWORD = process.env.TEST_PASSWORD;
if (!EMAIL || !PASSWORD) {
  console.error('TEST_EMAIL + TEST_PASSWORD required');
  process.exit(1);
}

const OUT = 'c:/tmp/verify-shots';
fs.mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 2,
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
});
const page = await context.newPage();
const consoleErrors = [];
const pageErrors = [];
page.on('console', (m) => { if (m.type() === 'error') consoleErrors.push(m.text()); });
page.on('pageerror', (e) => { pageErrors.push(e.message); });

async function shot(name, opts = {}) {
  await page.waitForTimeout(opts.settle ?? 600);
  const p = path.join(OUT, `${name}.png`);
  await page.screenshot({ path: p, fullPage: opts.fullPage ?? false });
  console.log(`  ${name}.png`);
  return p;
}

console.log('=== Login flow ===');
await page.goto(`${BASE}/login`, { waitUntil: 'domcontentloaded' });
await page.fill('input[type="email"]', EMAIL);
await page.fill('input[type="password"]', PASSWORD);

const loginResp = page.waitForResponse((r) => r.url().includes('/api/auth/login') && r.request().method() === 'POST', { timeout: 15000 });
await page.click('button[type="submit"]');
const r1 = await loginResp;
console.log('  POST /api/auth/login →', r1.status());
const body = await r1.text();
console.log('  body:', body);

// Verify-bot has no 2FA → should land directly on /. If it tried to
// redirect to /login/verify, that means 2FA is on (shouldn't be).
await page.waitForURL((u) => !u.toString().includes('/login'), { timeout: 10000 });
console.log('  landed at:', page.url());

console.log('\n=== Today tab (auto-appear popout) ===');
// The auto-appear sheet should be open (verify-bot has no entry for today).
await shot('a01-today-autoappear');

// Inspect the popout DOM.
const sheet = await page.evaluate(() => {
  const dialog = document.querySelector('[role="dialog"]');
  if (!dialog) return null;
  const slider = dialog.querySelector('[role="slider"]');
  return {
    ariaLabel: dialog.getAttribute('aria-label'),
    bgClass: Array.from(dialog.classList).find((c) => c.startsWith('bg-')) ?? null,
    sliderAriaNow: slider?.getAttribute('aria-valuenow') ?? null,
    sliderAriaMin: slider?.getAttribute('aria-valuemin') ?? null,
    sliderAriaMax: slider?.getAttribute('aria-valuemax') ?? null,
    handleClasses: dialog.querySelector('[data-testid="bottom-sheet-handle"]')?.className ?? null,
  };
});
console.log('  popout shape:', JSON.stringify(sheet, null, 2));

// Close the popout via the X button so the today-card-with-empty-state
// is visible. NO score drag — we don't want to commit anything.
const closeBtn = page.getByRole('button', { name: 'Sluiten' });
if (await closeBtn.isVisible().catch(() => false)) {
  await closeBtn.click();
  console.log('  popout dismissed via X');
} else {
  // Fallback: Escape key.
  await page.keyboard.press('Escape');
  console.log('  popout dismissed via Escape');
}
await page.waitForTimeout(400);
await shot('a02-today-card-empty');

console.log('\n=== Settings ===');
// The cog icon links to /settings.
const cog = page.getByRole('link', { name: /instellingen openen/i });
if (await cog.isVisible().catch(() => false)) {
  await cog.click();
  await page.waitForURL((u) => u.toString().includes('/settings'));
  await shot('a03-settings');
} else {
  console.log('  cog not found; navigating directly');
  await page.goto(`${BASE}/settings`, { waitUntil: 'domcontentloaded' });
  await shot('a03-settings');
}

// Tap "Uitloggen" to see the confirm step.
const logoutBtn = page.getByRole('button', { name: /^uitloggen$/i });
await logoutBtn.click();
await page.waitForTimeout(300);
await shot('a04-settings-logout-confirm');

// Cancel — we don't want to log out yet, more tabs to visit.
const cancelBtn = page.getByRole('button', { name: /annuleer/i });
await cancelBtn.click();
await page.waitForTimeout(200);

// Back to home via the "Terug" link.
const back = page.getByRole('link', { name: /^terug$/i });
await back.click();
await page.waitForURL((u) => u.toString().endsWith('/'));
await page.waitForTimeout(400);

// The popout will auto-open again because verify-bot still has no today
// entry. Close it.
const reopenedSheet = page.getByRole('dialog');
if (await reopenedSheet.isVisible().catch(() => false)) {
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
}

console.log('\n=== Timeline tab ===');
await page.getByRole('tab', { name: /tijdlijn/i }).click();
await shot('a05-timeline-chart');

// Toggle to Heatmap view.
const heatmapBtn = page.getByRole('radio', { name: /heatmap/i });
if (await heatmapBtn.isVisible().catch(() => false)) {
  await heatmapBtn.click();
  await page.waitForTimeout(400);
  await shot('a06-timeline-heatmap');
}

// Toggle back to chart + try 90 days.
await page.getByRole('radio', { name: /^lijn$/i }).click();
await page.getByRole('radio', { name: /90 dagen/i }).click();
await page.waitForTimeout(1000);
await shot('a07-timeline-90d');

console.log('\n=== Logout (real) ===');
await page.goto(`${BASE}/settings`, { waitUntil: 'domcontentloaded' });
await page.getByRole('button', { name: /^uitloggen$/i }).click();
await page.waitForTimeout(200);
const yes = page.getByRole('button', { name: /ja, uitloggen/i });
await yes.click();
await page.waitForURL((u) => u.toString().includes('/login'), { timeout: 10000 });
console.log('  after logout:', page.url());
await shot('a08-after-logout', { settle: 600 });

console.log('\nconsole errors during run:', consoleErrors.length);
for (const e of consoleErrors) console.log('  -', e);
console.log('pageerrors:', pageErrors.length);
for (const e of pageErrors) console.log('  -', e);

await browser.close();
