import { test, expect } from '@playwright/test';

function fakeIp(): string {
  return `10.${rand()}.${rand()}.${rand()}`;
}
function rand(): number {
  return Math.floor(Math.random() * 254) + 1;
}

test.describe('POST /api/auth/login/verify', () => {
  test('returns 401 when no pending-OTP cookie is present', async ({ request }) => {
    const res = await request.post('/api/auth/login/verify', {
      data: { otp: '123456' },
      headers: { 'x-forwarded-for': fakeIp() },
    });
    expect(res.status()).toBe(401);
    expect(await res.json()).toEqual({ error: 'invalid_otp' });
  });

  test('returns 401 with a stale pending-OTP cookie (no server-side state)', async ({ request }) => {
    const res = await request.post('/api/auth/login/verify', {
      data: { otp: '123456' },
      headers: {
        'x-forwarded-for': fakeIp(),
        cookie: 'gs_pending_otp=stale-uuid-that-doesnt-exist',
      },
    });
    expect(res.status()).toBe(401);
  });

  test('returns 403 on cross-origin Origin header', async ({ request }) => {
    const res = await request.post('/api/auth/login/verify', {
      data: { otp: '123456' },
      headers: { 'x-forwarded-for': fakeIp(), origin: 'https://evil.example.com' },
    });
    expect(res.status()).toBe(403);
  });

  // Rate-limit bucket isolation between /api/auth/login and /api/auth/login/verify
  // is tested in two places:
  //   1. src/lib/auth/__tests__/rate-limit.test.ts ("isolates namespaces")
  //   2. The two route unit tests use distinct mock limiter instances.
  // End-to-end against a real Next.js process belongs to Step 7 (next start).
  test.skip('separate rate-limit bucket from /api/auth/login (Step 7)', async () => {});
});
