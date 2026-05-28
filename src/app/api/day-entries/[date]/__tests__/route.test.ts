import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  upsertDayEntry: vi.fn(),
  getValidatedSession: vi.fn(),
  dayEntryWriteRateLimiterCheck: vi.fn(),
}));

vi.mock('@/lib/api/day-entries', () => ({
  upsertDayEntry: mocks.upsertDayEntry,
}));

vi.mock('@/lib/auth/get-validated-session', () => ({
  getValidatedSession: mocks.getValidatedSession,
}));

vi.mock('@/lib/auth/stores', () => ({
  dayEntryWriteRateLimiter: {
    check: mocks.dayEntryWriteRateLimiterCheck,
    sweep: vi.fn(),
    size: vi.fn(),
  },
  getClientIp: () => '1.2.3.4',
}));

import { PUT } from '../route';

function makeRequest(
  date: string,
  body: unknown,
  opts: { cookie?: string; origin?: string } = {},
) {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    origin: opts.origin ?? 'http://localhost:3000',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  return new Request(`http://localhost:3000/api/day-entries/${date}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(body),
  });
}

const ctx = (date: string) => ({ params: Promise.resolve({ date }) });

const sampleEntry = {
  date: '2026-05-28',
  score: 7 as const,
  note: null,
  tag_ids: [],
  sub_scores: null,
  sleep_hours: null,
  special_event: null,
  project_entry_ids: [],
  calendar_event_ids: [],
  garmin: null,
  health: null,
  weather: null,
  derived: null,
  created_at: '2026-05-28T08:00:00.000Z',
  updated_at: '2026-05-28T08:00:00.000Z',
};

describe('PUT /api/day-entries/[date]', () => {
  beforeEach(() => {
    mocks.upsertDayEntry.mockReset();
    mocks.getValidatedSession.mockReset();
    mocks.dayEntryWriteRateLimiterCheck.mockReset();
    mocks.dayEntryWriteRateLimiterCheck.mockReturnValue({ allowed: true });
    mocks.getValidatedSession.mockResolvedValue({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: Date.now() + 60_000,
    });
    mocks.upsertDayEntry.mockResolvedValue({ ok: true, value: sampleEntry });
  });

  it('200 with entry on valid score-only PUT', async () => {
    const res = await PUT(
      makeRequest('2026-05-28', { score: 7 }, { cookie: 'gs_session=s-id' }),
      ctx('2026-05-28'),
    );
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ entry: sampleEntry });
    expect(mocks.upsertDayEntry).toHaveBeenCalledWith('at-1', '2026-05-28', { score: 7 });
  });

  it('200 with full patch (score + note + tag_ids)', async () => {
    await PUT(
      makeRequest(
        '2026-05-28',
        { score: 6, note: 'good day', tag_ids: ['t-1', 't-2'] },
        { cookie: 'gs_session=s-id' },
      ),
      ctx('2026-05-28'),
    );
    expect(mocks.upsertDayEntry).toHaveBeenCalledWith('at-1', '2026-05-28', {
      score: 6,
      note: 'good day',
      tag_ids: ['t-1', 't-2'],
    });
  });

  it('400 on missing score', async () => {
    const res = await PUT(
      makeRequest('2026-05-28', { note: 'no score' }, { cookie: 'gs_session=s-id' }),
      ctx('2026-05-28'),
    );
    expect(res.status).toBe(400);
    expect(mocks.upsertDayEntry).not.toHaveBeenCalled();
  });

  it('400 on out-of-range score', async () => {
    const res = await PUT(
      makeRequest('2026-05-28', { score: 11 }, { cookie: 'gs_session=s-id' }),
      ctx('2026-05-28'),
    );
    expect(res.status).toBe(400);
    expect(mocks.upsertDayEntry).not.toHaveBeenCalled();
  });

  it('400 on malformed date in path', async () => {
    const res = await PUT(
      makeRequest('not-a-date', { score: 7 }, { cookie: 'gs_session=s-id' }),
      ctx('not-a-date'),
    );
    expect(res.status).toBe(400);
  });

  it('400 on future date in path', async () => {
    const res = await PUT(
      makeRequest('2099-12-31', { score: 7 }, { cookie: 'gs_session=s-id' }),
      ctx('2099-12-31'),
    );
    expect(res.status).toBe(400);
  });

  it('401 without a session cookie', async () => {
    const res = await PUT(
      makeRequest('2026-05-28', { score: 7 }),
      ctx('2026-05-28'),
    );
    expect(res.status).toBe(401);
    expect(mocks.upsertDayEntry).not.toHaveBeenCalled();
  });

  it('403 on cross-origin', async () => {
    const res = await PUT(
      makeRequest(
        '2026-05-28',
        { score: 7 },
        { cookie: 'gs_session=s-id', origin: 'https://evil.example.com' },
      ),
      ctx('2026-05-28'),
    );
    expect(res.status).toBe(403);
  });

  it('429 when rate limit exceeded', async () => {
    mocks.dayEntryWriteRateLimiterCheck.mockReturnValue({
      allowed: false,
      retryAfterMs: 1234,
    });
    const res = await PUT(
      makeRequest('2026-05-28', { score: 7 }, { cookie: 'gs_session=s-id' }),
      ctx('2026-05-28'),
    );
    expect(res.status).toBe(429);
    expect(await res.json()).toEqual({ error: 'rate_limited', retry_after_ms: 1234 });
    expect(mocks.upsertDayEntry).not.toHaveBeenCalled();
  });

  it('502 when SDK wrapper returns directus_error', async () => {
    mocks.upsertDayEntry.mockResolvedValue({ ok: false, error: 'directus_error' });
    const res = await PUT(
      makeRequest('2026-05-28', { score: 7 }, { cookie: 'gs_session=s-id' }),
      ctx('2026-05-28'),
    );
    expect(res.status).toBe(502);
  });
});
