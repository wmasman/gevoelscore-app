// Reproduces two suspected bugs in the quick-entry-popout feature:
//
//   Bug 1: edit pencils on the today-card always open the popout on the
//          SCORE step, regardless of which region was tapped (note / tags).
//   Bug 2: dismissing the popout in edit mode (existing entry) does not
//          play the today-card pulse — the user gets no confirmation that
//          the edit landed.
//
// Strategy:
//   1. Login as verify-bot (no 2FA).
//   2. Use ArrowUp to commit a score in the auto-popout, then dismiss.
//   3. Reload — now an entry exists for today. Today-card renders.
//      QuickEntryFlow re-mounts with its internal `step` state set to
//      'score' (because useState(startStep) only reads the prop once,
//      and at first render sheet.startStep === 'score').
//   4. Tap each pencil (note → tags → score). Inspect which layer is
//      visible in the popout. If bug 1 holds, all three open with the
//      score layer visible.
//   5. On close-via-X from the note edit, observe data-pulsing on the
//      today-card. If bug 2 holds, it stays 'false'.
//
// Run:
//   $env:TEST_EMAIL = "..."; $env:TEST_PASSWORD = "..."
//   node scripts/repro-edit-step-bug.mjs

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

const OUT = 'c:/tmp/verify-shots/edit-bug';
fs.mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 2,
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
});
const page = await context.newPage();
const consoleErrors = [];
page.on('console', (m) => { if (m.type() === 'error') consoleErrors.push(m.text()); });
page.on('pageerror', (e) => { consoleErrors.push(`pageerror: ${e.message}`); });

async function shot(name, opts = {}) {
  await page.waitForTimeout(opts.settle ?? 400);
  const p = path.join(OUT, `${name}.png`);
  await page.screenshot({ path: p, fullPage: opts.fullPage ?? false });
  console.log(`  ${name}.png`);
  return p;
}

// Returns which layer is opacity:1 inside the popout, plus what the
// score / note / tags step elements look like. Also returns the
// today-card data-pulsing attribute (set during the 200ms pulse window).
async function probe() {
  return await page.evaluate(() => {
    const dialog = document.querySelector('[role="dialog"]');
    const card = document.querySelector('[data-testid="today-card"]');
    let activeLayer = null;
    let layerOpacities = null;
    if (dialog) {
      const layers = Array.from(dialog.querySelectorAll('.absolute.inset-0'));
      layerOpacities = layers.map((el, i) => {
        const o = getComputedStyle(el).opacity;
        return { i, opacity: o, sample: el.textContent?.trim().slice(0, 40) ?? '' };
      });
      const fully = layerOpacities.find((x) => x.opacity === '1');
      activeLayer = fully ? fully.i : null;
    }
    return {
      dialogOpen: !!dialog,
      activeLayer,
      layerOpacities,
      cardPulsing: card?.getAttribute('data-pulsing') ?? null,
    };
  });
}

console.log('=== Login + setup: create today\'s entry ===');
await page.goto(`${BASE}/login`, { waitUntil: 'domcontentloaded' });
await page.fill('input[type="email"]', EMAIL);
await page.fill('input[type="password"]', PASSWORD);
const loginResp = page.waitForResponse((r) => r.url().includes('/api/auth/login') && r.request().method() === 'POST', { timeout: 15000 });
await page.click('button[type="submit"]');
const r = await loginResp;
console.log('  POST /api/auth/login →', r.status());
await page.waitForURL((u) => !u.toString().includes('/login'), { timeout: 10000 });
console.log('  landed at:', page.url());

await page.waitForTimeout(1200);
// day_entries is shared across users (no owner column) so the bot may
// already see today's row from Willem's earlier save. If the sheet
// auto-opened, dismiss it. Either way, today-card should be visible
// because an entry exists.
const dialogPresent = await page.locator('[role="dialog"]').count();
console.log('  dialog present on landing?', dialogPresent > 0);
if (dialogPresent > 0) {
  const cls = page.getByRole('button', { name: 'Sluiten' });
  if (await cls.isVisible().catch(() => false)) {
    await cls.click();
    console.log('  dismissed auto-popout via X');
  } else {
    await page.keyboard.press('Escape');
    console.log('  dismissed auto-popout via Escape');
  }
  await page.waitForTimeout(400);
}

// Hard-reload so QuickEntryFlow re-mounts with a fresh `step = 'score'`
// init — matching the exact state the user lands in.
console.log('\n=== Reload — fresh mount, sheet closed (entry exists) ===');
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1200);
await shot('01-today-card-with-entry', { fullPage: true });

const cardBefore = await page.evaluate(() => {
  const card = document.querySelector('[data-testid="today-card"]');
  return {
    pulsing: card?.getAttribute('data-pulsing') ?? null,
    text: card?.textContent?.trim() ?? null,
  };
});
console.log('  today-card before tap:', cardBefore);

console.log('\n=== TAP: note pencil ===');
// The note region is the second tappable region under the today-card.
// Its aria-label starts with "Notitie: ".
const noteRegion = page.getByRole('button', { name: /^notitie:/i });
await noteRegion.click();
await page.waitForTimeout(500);
await shot('02-tapped-note-pencil');
const noteProbe = await probe();
console.log('  probe after note-tap:', JSON.stringify(noteProbe, null, 2));

// Close via X. Then measure pulse within the 200ms window.
const xBtn = page.getByRole('button', { name: 'Sluiten' });
await xBtn.click();
// Capture data-pulsing immediately and then at 50/150/300ms.
const samples = [];
for (const t of [10, 50, 100, 150, 300, 500]) {
  await page.waitForTimeout(t === 10 ? 10 : t - samples.length * 0);
  const p = await page.evaluate(() => {
    const card = document.querySelector('[data-testid="today-card"]');
    return card?.getAttribute('data-pulsing') ?? null;
  });
  samples.push({ at_ms_marker: t, pulsing: p });
}
console.log('  post-close pulse samples:', JSON.stringify(samples));
await shot('03-after-close-from-note');

console.log('\n=== TAP: tags pencil ===');
const tagsRegion = page.getByRole('button', { name: /^tags:/i });
await tagsRegion.click();
await page.waitForTimeout(500);
await shot('04-tapped-tags-pencil');
const tagsProbe = await probe();
console.log('  probe after tags-tap:', JSON.stringify(tagsProbe, null, 2));

await xBtn.click();
await page.waitForTimeout(400);

console.log('\n=== TAP: score pencil (control) ===');
const scoreRegion = page.getByRole('button', { name: /^gevoelscore:/i });
await scoreRegion.click();
await page.waitForTimeout(500);
await shot('05-tapped-score-pencil');
const scoreProbe = await probe();
console.log('  probe after score-tap:', JSON.stringify(scoreProbe, null, 2));

await xBtn.click();
await page.waitForTimeout(400);

console.log('\n=== Logout ===');
await page.goto(`${BASE}/settings`, { waitUntil: 'domcontentloaded' });
await page.getByRole('button', { name: /^uitloggen$/i }).click();
await page.waitForTimeout(200);
await page.getByRole('button', { name: /ja, uitloggen/i }).click();
await page.waitForURL((u) => u.toString().includes('/login'), { timeout: 10000 });

console.log('\nconsole errors during run:', consoleErrors.length);
for (const e of consoleErrors) console.log('  -', e);

await browser.close();
console.log('\nDone. Screenshots in:', OUT);
