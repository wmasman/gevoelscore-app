import { test, expect } from '@playwright/test';

test.describe('POST /api/auth/logout', () => {
  test('returns 200 with no session cookie (idempotent)', async ({ request }) => {
    const res = await request.post('/api/auth/logout');
    expect(res.status()).toBe(200);
    expect(await res.json()).toEqual({ ok: true });
  });

  test('returns 200 with a stale session cookie (idempotent)', async ({ request }) => {
    const res = await request.post('/api/auth/logout', {
      headers: { cookie: 'gs_session=stale-uuid' },
    });
    expect(res.status()).toBe(200);
  });

  test('clears the session cookie via Max-Age=0', async ({ request }) => {
    const res = await request.post('/api/auth/logout', {
      headers: { cookie: 'gs_session=anything' },
    });
    const setCookie = res.headers()['set-cookie'] ?? '';
    expect(setCookie).toContain('gs_session=');
    expect(setCookie).toContain('Max-Age=0');
    expect(setCookie).toContain('HttpOnly');
  });

  test('returns 403 on cross-origin Origin header', async ({ request }) => {
    const res = await request.post('/api/auth/logout', {
      headers: { origin: 'https://evil.example.com' },
    });
    expect(res.status()).toBe(403);
  });
});
