// Step-1 Phase 1.D — POST /api/calendars/events/[id]/include-series tests.

import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  getValidatedSession: vi.fn(),
  writeCheck: vi.fn(),
  readCalendarEventById: vi.fn(),
  readConnectionById: vi.fn(),
  readEventsByRecurrenceId: vi.fn(),
  deleteSeriesExclusion: vi.fn(),
  patchCalendarEventsBulk: vi.fn(),
}));

vi.mock('@/lib/auth/get-validated-session', () => ({
  getValidatedSession: mocks.getValidatedSession,
}));

vi.mock('@/lib/auth/stores', async () => {
  const actual = await vi.importActual<typeof import('@/lib/auth/stores')>(
    '@/lib/auth/stores',
  );
  return {
    ...actual,
    calendarWriteRateLimiter: {
      check: mocks.writeCheck,
      sweep: () => undefined,
    },
  };
});

vi.mock('@/lib/api/calendars', () => ({
  readCalendarEventById: mocks.readCalendarEventById,
  readConnectionById: mocks.readConnectionById,
  readEventsByRecurrenceId: mocks.readEventsByRecurrenceId,
  deleteSeriesExclusion: mocks.deleteSeriesExclusion,
  patchCalendarEventsBulk: mocks.patchCalendarEventsBulk,
}));

import { POST } from '../route';

const USER_ID = '16f6f68b-e683-4dc9-8afc-e80695c4259d';
const EVENT_ID = '550e8400-e29b-41d4-a716-446655440000';
const CONN_ID = '660e8400-e29b-41d4-a716-446655440001';

function makePost(opts: { cookie?: string } = {}): {
  request: Request;
  context: { params: Promise<{ id: string }> };
} {
  const headers: Record<string, string> = {
    origin: 'http://localhost:3000',
    'content-type': 'application/json',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  return {
    request: new Request(
      `http://localhost:3000/api/calendars/events/${EVENT_ID}/include-series`,
      { method: 'POST', headers },
    ),
    context: { params: Promise.resolve({ id: EVENT_ID }) },
  };
}

beforeEach(() => {
  vi.unstubAllEnvs();
  vi.stubEnv('WILLEM_USER_ID', USER_ID);
  vi.stubEnv('DIRECTUS_TOKEN', 'at');

  mocks.getValidatedSession.mockReset();
  mocks.writeCheck.mockReset();
  mocks.readCalendarEventById.mockReset();
  mocks.readConnectionById.mockReset();
  mocks.readEventsByRecurrenceId.mockReset();
  mocks.deleteSeriesExclusion.mockReset();
  mocks.patchCalendarEventsBulk.mockReset();

  mocks.getValidatedSession.mockResolvedValue({
    accessToken: 'at',
    refreshToken: 'rt',
    expiresAt: Date.now() + 60_000,
  });
  mocks.writeCheck.mockReturnValue({ allowed: true });
  mocks.readConnectionById.mockResolvedValue({
    ok: true,
    value: { id: CONN_ID, user_id: USER_ID },
  });
  mocks.readEventsByRecurrenceId.mockResolvedValue({
    ok: true,
    value: [{ id: 'sib-1' }, { id: 'sib-2' }],
  });
  mocks.deleteSeriesExclusion.mockResolvedValue({ ok: true, value: undefined });
  mocks.patchCalendarEventsBulk.mockResolvedValue({ ok: true, value: undefined });
});

describe('POST /api/calendars/events/[id]/include-series', () => {
  it('test 81: non-recurring event → 400 event_not_recurring', async () => {
    mocks.readCalendarEventById.mockResolvedValue({
      ok: true,
      value: { id: EVENT_ID, connection_id: CONN_ID, recurrence_id: null },
    });

    const { request, context } = makePost({ cookie: 'gs_session=s-1' });
    const res = await POST(request, context);

    expect(res.status).toBe(400);
    expect((await res.json()).error).toBe('event_not_recurring');
  });

  it('test 82: happy path → DELETE series_exclusion + bulk PATCH siblings to included + user_included', async () => {
    mocks.readCalendarEventById.mockResolvedValue({
      ok: true,
      value: {
        id: EVENT_ID,
        connection_id: CONN_ID,
        recurrence_id: 'rec-yoga',
      },
    });

    const { request, context } = makePost({ cookie: 'gs_session=s-1' });
    const res = await POST(request, context);

    expect(res.status).toBe(200);
    expect(mocks.deleteSeriesExclusion).toHaveBeenCalledWith(
      'at',
      CONN_ID,
      'rec-yoga',
    );
    expect(mocks.patchCalendarEventsBulk).toHaveBeenCalledWith(
      'at',
      ['sib-1', 'sib-2'],
      { included_as_context: true, user_decision: 'user_included' },
    );
  });

  it('test 83: response includes recurrence_id + events_updated count', async () => {
    mocks.readCalendarEventById.mockResolvedValue({
      ok: true,
      value: {
        id: EVENT_ID,
        connection_id: CONN_ID,
        recurrence_id: 'rec-yoga',
      },
    });

    const { request, context } = makePost({ cookie: 'gs_session=s-1' });
    const res = await POST(request, context);

    const body = (await res.json()) as {
      recurrence_id: string;
      events_updated: number;
    };
    expect(body.recurrence_id).toBe('rec-yoga');
    expect(body.events_updated).toBe(2);
  });

  it('test 84: order — DELETE exclusion BEFORE bulk PATCH', async () => {
    mocks.readCalendarEventById.mockResolvedValue({
      ok: true,
      value: {
        id: EVENT_ID,
        connection_id: CONN_ID,
        recurrence_id: 'rec-yoga',
      },
    });
    const callOrder: string[] = [];
    mocks.deleteSeriesExclusion.mockImplementation(async () => {
      callOrder.push('delete');
      return { ok: true, value: undefined };
    });
    mocks.patchCalendarEventsBulk.mockImplementation(async () => {
      callOrder.push('bulk');
      return { ok: true, value: undefined };
    });

    const { request, context } = makePost({ cookie: 'gs_session=s-1' });
    await POST(request, context);

    expect(callOrder).toEqual(['delete', 'bulk']);
  });
});
