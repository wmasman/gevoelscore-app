import { test, expect } from '@playwright/test';

test.describe('GET /api/health', () => {
  test('returns 200 with { status: "ok" }', async ({ request }) => {
    const res = await request.get('/api/health');

    expect(res.status()).toBe(200);
    expect(res.headers()['content-type']).toContain('application/json');

    const body = await res.json();
    expect(body).toEqual({ status: 'ok' });
  });

  test('does not require auth', async ({ request }) => {
    // No cookies, no auth header — should still respond.
    const res = await request.get('/api/health', {
      headers: { cookie: '' },
    });
    expect(res.status()).toBe(200);
  });
});
