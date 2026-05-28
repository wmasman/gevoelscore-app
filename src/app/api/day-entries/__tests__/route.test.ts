import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  readDayEntriesInRange: vi.fn(),
  getValidatedSession: vi.fn(),
}));

vi.mock('@/lib/api/day-entries', () => ({
  readDayEntriesInRange: mocks.readDayEntriesInRange,
}));

vi.mock('@/lib/auth/get-validated-session', () => ({
  getValidatedSession: mocks.getValidatedSession,
}));

import { GET } from '../route';

function makeRequest(
  query: { from?: string; to?: string },
  opts: { cookie?: string; origin?: string } = {},
) {
  const url = new URL('http://localhost:3000/api/day-entries');
  if (query.from !== undefined) url.searchParams.set('from', query.from);
  if (query.to !== undefined) url.searchParams.set('to', query.to);
  const headers: Record<string, string> = {
    origin: opts.origin ?? 'http://localhost:3000',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  return new Request(url, { method: 'GET', headers });
}

describe('GET /api/day-entries', () => {
  beforeEach(() => {
    mocks.readDayEntriesInRange.mockReset();
    mocks.getValidatedSession.mockReset();
    mocks.getValidatedSession.mockResolvedValue({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: Date.now() + 60_000,
    });
  });

  it('returns 200 with entries when from/to are valid', async () => {
    mocks.readDayEntriesInRange.mockResolvedValue({ ok: true, value: [] });

    const res = await GET(
      makeRequest({ from: '2026-05-01', to: '2026-05-28' }, { cookie: 'gs_session=s-id' }),
    );

    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ entries: [] });
    expect(mocks.readDayEntriesInRange).toHaveBeenCalledWith('at-1', '2026-05-01', '2026-05-28');
  });

  it('returns 400 on missing from', async () => {
    const res = await GET(makeRequest({ to: '2026-05-28' }, { cookie: 'gs_session=s-id' }));
    expect(res.status).toBe(400);
  });

  it('returns 400 on malformed from', async () => {
    const res = await GET(
      makeRequest({ from: 'not-a-date', to: '2026-05-28' }, { cookie: 'gs_session=s-id' }),
    );
    expect(res.status).toBe(400);
  });

  it('returns 400 when to < from', async () => {
    const res = await GET(
      makeRequest({ from: '2026-05-28', to: '2026-05-01' }, { cookie: 'gs_session=s-id' }),
    );
    expect(res.status).toBe(400);
    expect(mocks.readDayEntriesInRange).not.toHaveBeenCalled();
  });

  it('returns 400 when range exceeds 90 days', async () => {
    const res = await GET(
      makeRequest({ from: '2026-01-01', to: '2026-05-01' }, { cookie: 'gs_session=s-id' }),
    );
    expect(res.status).toBe(400);
    expect(mocks.readDayEntriesInRange).not.toHaveBeenCalled();
  });

  it('returns 401 without a session cookie', async () => {
    const res = await GET(makeRequest({ from: '2026-05-01', to: '2026-05-28' }));
    expect(res.status).toBe(401);
  });

  it('returns 403 on cross-origin', async () => {
    const res = await GET(
      makeRequest(
        { from: '2026-05-01', to: '2026-05-28' },
        { cookie: 'gs_session=s-id', origin: 'https://evil.example.com' },
      ),
    );
    expect(res.status).toBe(403);
  });

  it('returns 502 when SDK wrapper returns directus_error', async () => {
    mocks.readDayEntriesInRange.mockResolvedValue({ ok: false, error: 'directus_error' });

    const res = await GET(
      makeRequest({ from: '2026-05-01', to: '2026-05-28' }, { cookie: 'gs_session=s-id' }),
    );

    expect(res.status).toBe(502);
  });
});
