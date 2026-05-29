// One-off verification script. Drives Playwright against the live prod
// site, captures screenshots + console errors for each page, and reports
// what we can observe without 2FA.
//
// Run: node c:/tmp/verify-prod.mjs
import { chromium } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

const BASE = 'https://gevoelscore-frontend.fly.dev';
const OUT_DIR = 'c:/tmp/verify-shots';
fs.mkdirSync(OUT_DIR, { recursive: true });

const findings = [];

async function visit(browser, label, urlPath, { viewport = { width: 390, height: 844 } } = {}) {
  const context = await browser.newContext({
    viewport,
    deviceScaleFactor: 2,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  });
  const page = await context.newPage();
  const consoleErrors = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  const pageErrors = [];
  page.on('pageerror', (err) => {
    pageErrors.push(err.message);
  });

  const response = await page.goto(`${BASE}${urlPath}`, {
    waitUntil: 'domcontentloaded',
    timeout: 15000,
  });

  const finalUrl = page.url();
  const status = response?.status();

  // For redirect inspection, do a separate fetch w/o following.
  const noFollowRes = await page.context().request.get(`${BASE}${urlPath}`, { maxRedirects: 0 }).catch((e) => ({ _err: e.message }));
  const noFollowStatus = noFollowRes._err ? 'fetch-err' : noFollowRes.status();
  const noFollowLocation = noFollowRes._err ? null : noFollowRes.headers()['location'];

  // Settle visually.
  await page.waitForTimeout(800);

  const shotPath = path.join(OUT_DIR, `${label}.png`);
  await page.screenshot({ path: shotPath, fullPage: true });

  // Inspect computed styles for warm-earth tokens.
  const tokens = await page.evaluate(() => {
    const root = document.documentElement;
    const style = getComputedStyle(root);
    return {
      bg: style.getPropertyValue('--color-bg').trim(),
      surface: style.getPropertyValue('--color-surface').trim(),
      accent: style.getPropertyValue('--color-accent').trim(),
      fg: style.getPropertyValue('--color-fg').trim(),
    };
  });

  // Grab some structural facts.
  const facts = await page.evaluate(() => ({
    title: document.title,
    h1Text: document.querySelector('h1')?.textContent?.trim() ?? null,
    forms: document.querySelectorAll('form').length,
    emailInput: !!document.querySelector('input[type="email"]'),
    passwordInput: !!document.querySelector('input[type="password"]'),
    submitButtonText: document.querySelector('button[type="submit"]')?.textContent?.trim() ?? null,
    bodyBg: getComputedStyle(document.body).backgroundColor,
    headingCount: document.querySelectorAll('h1, h2, h3').length,
  }));

  console.log(`\n=== ${label}: ${urlPath} ===`);
  console.log('  follow:           ', status, '→', finalUrl);
  console.log('  no-follow:        ', noFollowStatus, '→', noFollowLocation ?? '(no Location)');
  console.log('  title:            ', facts.title);
  console.log('  h1:               ', facts.h1Text);
  console.log('  forms:            ', facts.forms, '| email:', facts.emailInput, '| pw:', facts.passwordInput, '| submitBtn:', JSON.stringify(facts.submitButtonText));
  console.log('  headings (h1+h2+h3):', facts.headingCount);
  console.log('  body bg:          ', facts.bodyBg);
  console.log('  tokens:           ', JSON.stringify(tokens));
  console.log('  console errors:   ', consoleErrors.length === 0 ? 'none' : consoleErrors.length);
  if (consoleErrors.length > 0) for (const e of consoleErrors) console.log('    -', e);
  console.log('  pageerror:        ', pageErrors.length === 0 ? 'none' : pageErrors.length);
  if (pageErrors.length > 0) for (const e of pageErrors) console.log('    -', e);
  console.log('  screenshot:       ', shotPath);

  findings.push({
    label,
    path: urlPath,
    statusFollow: status,
    finalUrl,
    statusNoFollow: noFollowStatus,
    location: noFollowLocation,
    title: facts.title,
    h1: facts.h1Text,
    forms: facts.forms,
    emailInput: facts.emailInput,
    passwordInput: facts.passwordInput,
    submitButton: facts.submitButtonText,
    bodyBg: facts.bodyBg,
    tokens,
    consoleErrors,
    pageErrors,
    shotPath,
  });

  await context.close();
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    await visit(browser, '01-root-unauth',  '/');
    await visit(browser, '02-login',        '/login');
    await visit(browser, '03-over',         '/over');
    await visit(browser, '04-settings-unauth', '/settings');
    await visit(browser, '05-nonexistent',  '/does-not-exist');
  } finally {
    await browser.close();
  }
  fs.writeFileSync(path.join(OUT_DIR, 'findings.json'), JSON.stringify(findings, null, 2));
  console.log('\nfindings.json:', path.join(OUT_DIR, 'findings.json'));
})();
