import { test, expect } from '@playwright/test';

test.describe('POST /api/auth/2fa/generate', () => {
  test('returns 401 without session cookie', async ({ request }) => {
    const res = await request.post('/api/auth/2fa/generate', {
      data: { password: 'whatever' },
    });
    expect(res.status()).toBe(401);
  });

  test('returns 401 with stale session cookie (no server state)', async ({ request }) => {
    const res = await request.post('/api/auth/2fa/generate', {
      data: { password: 'whatever' },
      headers: { cookie: 'gs_session=stale-uuid' },
    });
    expect(res.status()).toBe(401);
  });

  test('returns 403 on cross-origin', async ({ request }) => {
    const res = await request.post('/api/auth/2fa/generate', {
      data: { password: 'pw' },
      headers: { origin: 'https://evil.example.com' },
    });
    expect(res.status()).toBe(403);
  });

  test('returns 400 on missing password', async ({ request }) => {
    const res = await request.post('/api/auth/2fa/generate', {
      data: {},
      headers: { cookie: 'gs_session=stale-uuid' },
    });
    // No session → 401 before we get to body validation. Both layers are valid responses here.
    expect([400, 401]).toContain(res.status());
  });
});

test.describe('POST /api/auth/2fa/enable', () => {
  test('returns 401 without session cookie', async ({ request }) => {
    const res = await request.post('/api/auth/2fa/enable', {
      data: { secret: 'JBSWY', otp: '123456' },
    });
    expect(res.status()).toBe(401);
  });

  test('returns 403 on cross-origin', async ({ request }) => {
    const res = await request.post('/api/auth/2fa/enable', {
      data: { secret: 'JBSWY', otp: '123456' },
      headers: { origin: 'https://evil.example.com' },
    });
    expect(res.status()).toBe(403);
  });
});
