// Security response headers — closes audit M1.
//
// These run against `npm run build && npm run start` (the production server)
// because dev-mode Next strips/relaxes some headers, which would make the
// assertions inaccurate.

import { test, expect } from '@playwright/test';

const REQUIRED_HEADERS = [
  'content-security-policy',
  'strict-transport-security',
  'x-content-type-options',
  'referrer-policy',
  'permissions-policy',
];

test('all five security headers present on /login', async ({ request }) => {
  const res = await request.get('/login');
  for (const h of REQUIRED_HEADERS) {
    expect(res.headers()[h], `missing header: ${h}`).toBeDefined();
  }
  expect(res.headers()['x-powered-by']).toBeUndefined();
});

test('all five security headers present on /api/health', async ({ request }) => {
  const res = await request.get('/api/health');
  for (const h of REQUIRED_HEADERS) {
    expect(res.headers()[h], `missing header: ${h}`).toBeDefined();
  }
});

test('CSP locks default-src to self and denies framing', async ({ request }) => {
  const res = await request.get('/login');
  const csp = res.headers()['content-security-policy'] ?? '';
  expect(csp).toContain("default-src 'self'");
  expect(csp).toContain("frame-ancestors 'none'");
});

test('HSTS asserts a long max-age and includeSubDomains', async ({ request }) => {
  const res = await request.get('/login');
  const hsts = res.headers()['strict-transport-security'] ?? '';
  expect(hsts).toMatch(/max-age=\d{7,}/);
  expect(hsts).toContain('includeSubDomains');
});

test('X-Content-Type-Options is nosniff', async ({ request }) => {
  const res = await request.get('/login');
  expect(res.headers()['x-content-type-options']).toBe('nosniff');
});
