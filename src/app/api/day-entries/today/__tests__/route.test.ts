import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  readDayEntryByDate: vi.fn(),
  getValidatedSession: vi.fn(),
  todayInAmsterdam: vi.fn(),
}));

vi.mock('@/lib/api/day-entries', () => ({
  readDayEntryByDate: mocks.readDayEntryByDate,
}));

vi.mock('@/lib/auth/get-validated-session', () => ({
  getValidatedSession: mocks.getValidatedSession,
}));

vi.mock('@/lib/domain/date', async () => {
  const actual = await vi.importActual<typeof import('@/lib/domain/date')>('@/lib/domain/date');
  return { ...actual, todayInAmsterdam: mocks.todayInAmsterdam };
});

import { GET } from '../route';

function makeRequest(opts: { cookie?: string; origin?: string } = {}) {
  const headers: Record<string, string> = {
    origin: opts.origin ?? 'http://localhost:3000',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  return new Request('http://localhost:3000/api/day-entries/today', {
    method: 'GET',
    headers,
  });
}

const sampleEntry = {
  date: '2026-05-28',
  score: 7 as const,
  note: null,
  tag_ids: ['tag-1'],
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

describe('GET /api/day-entries/today', () => {
  beforeEach(() => {
    mocks.readDayEntryByDate.mockReset();
    mocks.getValidatedSession.mockReset();
    mocks.todayInAmsterdam.mockReset();
    mocks.todayInAmsterdam.mockReturnValue('2026-05-28');
    mocks.getValidatedSession.mockResolvedValue({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: Date.now() + 60_000,
    });
  });

  it('returns 200 with { entry: null } when no row exists for today', async () => {
    mocks.readDayEntryByDate.mockResolvedValue({ ok: true, value: null });

    const res = await GET(makeRequest({ cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ entry: null });
    expect(mocks.readDayEntryByDate).toHaveBeenCalledWith('at-1', '2026-05-28');
  });

  it("returns 200 with { entry: DayEntry } when today's row exists", async () => {
    mocks.readDayEntryByDate.mockResolvedValue({ ok: true, value: sampleEntry });

    const res = await GET(makeRequest({ cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ entry: sampleEntry });
  });

  it('returns 401 without a session cookie', async () => {
    const res = await GET(makeRequest());

    expect(res.status).toBe(401);
    expect(mocks.readDayEntryByDate).not.toHaveBeenCalled();
  });

  it('returns 401 when the session cookie does not resolve to a valid session', async () => {
    mocks.getValidatedSession.mockResolvedValue(null);

    const res = await GET(makeRequest({ cookie: 'gs_session=stale' }));

    expect(res.status).toBe(401);
    expect(mocks.readDayEntryByDate).not.toHaveBeenCalled();
  });

  it('returns 502 when the SDK wrapper returns a directus_error', async () => {
    mocks.readDayEntryByDate.mockResolvedValue({ ok: false, error: 'directus_error' });

    const res = await GET(makeRequest({ cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(502);
    expect(await res.json()).toEqual({ error: 'server_error' });
  });
});
