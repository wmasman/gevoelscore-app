import { test, expect } from '@playwright/test';

// Unique IP per test so rate-limit buckets don't collide across parallel runs.
function fakeIp(): string {
  return `10.${rand()}.${rand()}.${rand()}`;
}
function rand(): number {
  return Math.floor(Math.random() * 254) + 1;
}

test.describe('POST /api/auth/login', () => {
  test('returns 400 on missing body fields', async ({ request }) => {
    const res = await request.post('/api/auth/login', {
      data: {},
      headers: { 'x-forwarded-for': fakeIp() },
    });
    expect(res.status()).toBe(400);
  });

  test('returns 400 on missing password', async ({ request }) => {
    const res = await request.post('/api/auth/login', {
      data: { email: 'a@b.com' },
      headers: { 'x-forwarded-for': fakeIp() },
    });
    expect(res.status()).toBe(400);
  });

  test('returns 400 on email without @', async ({ request }) => {
    const res = await request.post('/api/auth/login', {
      data: { email: 'notanemail', password: 'whatever' },
      headers: { 'x-forwarded-for': fakeIp() },
    });
    expect(res.status()).toBe(400);
  });

  test('returns 403 on cross-origin Origin header', async ({ request }) => {
    const res = await request.post('/api/auth/login', {
      data: { email: 'a@b.com', password: 'pw' },
      headers: { 'x-forwarded-for': fakeIp(), origin: 'https://evil.example.com' },
    });
    expect(res.status()).toBe(403);
  });

  test('returns 401 on credentials Directus rejects (or unreachable in test)', async ({ request }) => {
    // Without a real Directus user this hits invalid_credentials or directus_error,
    // both of which the route maps to a generic 401. Happy-path 200 lives in Step 7.
    const res = await request.post('/api/auth/login', {
      data: { email: 'notarealuser@example.test', password: 'definitely-wrong' },
      headers: { 'x-forwarded-for': fakeIp() },
    });
    expect(res.status()).toBe(401);
    const body = await res.json();
    expect(body).toEqual({ error: 'invalid_credentials' });
  });

  // Rate-limit enforcement is covered by:
  //   1. src/lib/auth/__tests__/rate-limit.test.ts (the limiter itself, 6 cases)
  //   2. src/app/api/auth/login/__tests__/route.test.ts (the route returns 429
  //      when the limiter says blocked — mocked)
  // The wiring of the two in a real Next.js process is NOT testable against
  // `next dev` because dev mode re-evaluates server modules between requests,
  // resetting in-memory state. Step 7 (Playwright against `next start` / live
  // Fly stack) will add the integration test.
  test.skip('rate-limits at 5 attempts per 5 minutes per IP (Step 7)', async () => {});
});
