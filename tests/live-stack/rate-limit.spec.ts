import { test, expect } from '@playwright/test';

// These two specs were skipped in tests/api/auth/{login,login-verify}.spec.ts
// because `next dev` re-evaluates server modules between requests. Here we run
// against `next start` (production) where module state persists.

function fakeIp(): string {
  return `10.${rand()}.${rand()}.${rand()}`;
}
function rand(): number {
  return Math.floor(Math.random() * 254) + 1;
}

test.describe('AC5: /api/auth/login rate-limit', () => {
  test('6th attempt within 5 minutes from same IP returns 429', async ({ request }) => {
    const ip = fakeIp();
    for (let i = 0; i < 5; i++) {
      const res = await request.post('/api/auth/login', {
        data: { email: 'rl@example.test', password: 'definitely-wrong' },
        headers: { 'x-forwarded-for': ip },
      });
      // Each rejected with invalid_credentials (real Directus says so) — not 429 yet.
      expect([400, 401]).toContain(res.status());
    }

    const blocked = await request.post('/api/auth/login', {
      data: { email: 'rl@example.test', password: 'definitely-wrong' },
      headers: { 'x-forwarded-for': ip },
    });
    expect(blocked.status()).toBe(429);
  });
});

test.describe('AC8: /api/auth/login/verify rate-limit is a separate bucket', () => {
  test('exhausting /login does not exhaust /login/verify (different IPs)', async ({ request }) => {
    // Use distinct IP from the test above so we start from zero on both buckets.
    const ip = fakeIp();

    // Burn the login bucket
    for (let i = 0; i < 6; i++) {
      await request.post('/api/auth/login', {
        data: { email: 'iso@example.test', password: 'wrong' },
        headers: { 'x-forwarded-for': ip },
      });
    }

    // Verify bucket should still be fresh — request returns 401 (no pending state),
    // NOT 429. This proves the namespaces are isolated.
    const verifyRes = await request.post('/api/auth/login/verify', {
      data: { otp: '123456' },
      headers: { 'x-forwarded-for': ip },
    });
    expect(verifyRes.status()).not.toBe(429);
    expect(verifyRes.status()).toBe(401);
  });
});
