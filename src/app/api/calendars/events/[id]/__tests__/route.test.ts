// Step-1 Phase 1.D — PATCH /api/calendars/events/[id] tests.

import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  getValidatedSession: vi.fn(),
  writeCheck: vi.fn(),
  readCalendarEventById: vi.fn(),
  readConnectionById: vi.fn(),
  readEventsByRecurrenceId: vi.fn(),
  patchCalendarEvent: vi.fn(),
  patchCalendarEventsBulk: vi.fn(),
  insertSeriesExclusion: vi.fn(),
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
  patchCalendarEvent: mocks.patchCalendarEvent,
  patchCalendarEventsBulk: mocks.patchCalendarEventsBulk,
  insertSeriesExclusion: mocks.insertSeriesExclusion,
}));

import { PATCH } from '../route';

const USER_ID = '16f6f68b-e683-4dc9-8afc-e80695c4259d';
const OTHER_USER_ID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';
const EVENT_ID = '550e8400-e29b-41d4-a716-446655440000';
const CONN_ID = '660e8400-e29b-41d4-a716-446655440001';
const TAG_ID = '770e8400-e29b-41d4-a716-446655440002';
const EPISODE_ID = '880e8400-e29b-41d4-a716-446655440003';

function makePatch(
  body: unknown,
  opts: { cookie?: string } = {},
): {
  request: Request;
  context: { params: Promise<{ id: string }> };
} {
  const headers: Record<string, string> = {
    origin: 'http://localhost:3000',
    'content-type': 'application/json',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  return {
    request: new Request(`http://localhost:3000/api/calendars/events/${EVENT_ID}`, {
      method: 'PATCH',
      headers,
      body: JSON.stringify(body),
    }),
    context: { params: Promise.resolve({ id: EVENT_ID }) },
  };
}

function nonRecurringEvent() {
  return {
    id: EVENT_ID,
    connection_id: CONN_ID,
    recurrence_id: null,
    linked_tag_id: null,
    linked_episode_id: null,
    included_as_context: true,
    user_decision: 'auto',
  };
}

function recurringEvent() {
  return {
    ...nonRecurringEvent(),
    recurrence_id: 'rec-yoga',
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
  mocks.patchCalendarEvent.mockReset();
  mocks.patchCalendarEventsBulk.mockReset();
  mocks.insertSeriesExclusion.mockReset();

  mocks.getValidatedSession.mockResolvedValue({
    accessToken: 'at',
    refreshToken: 'rt',
    expiresAt: Date.now() + 60_000,
  });
  mocks.writeCheck.mockReturnValue({ allowed: true });
  mocks.readConnectionById.mockResolvedValue({
    ok: true,
    value: { id: CONN_ID, user_id: USER_ID, provider: 'google' },
  });
  mocks.patchCalendarEvent.mockResolvedValue({ ok: true, value: undefined });
  mocks.patchCalendarEventsBulk.mockResolvedValue({ ok: true, value: undefined });
  mocks.insertSeriesExclusion.mockResolvedValue({ ok: true, value: undefined });
  mocks.readEventsByRecurrenceId.mockResolvedValue({
    ok: true,
    value: [
      { id: 'sib-1' },
      { id: 'sib-2' },
      { id: 'sib-3' },
    ],
  });
});

describe('PATCH /api/calendars/events/[id]', () => {
  it('test 69: ownership mismatch (event.connection.user_id != session user) → 403', async () => {
    mocks.readCalendarEventById.mockResolvedValue({
      ok: true,
      value: nonRecurringEvent(),
    });
    mocks.readConnectionById.mockResolvedValue({
      ok: true,
      value: { id: CONN_ID, user_id: OTHER_USER_ID },
    });

    const { request, context } = makePatch(
      { linked_tag_id: TAG_ID },
      { cookie: 'gs_session=s-1' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(403);
  });

  it('test 70: PATCH linked_tag_id → patchCalendarEvent called with that id', async () => {
    mocks.readCalendarEventById.mockResolvedValue({
      ok: true,
      value: nonRecurringEvent(),
    });

    const { request, context } = makePatch(
      { linked_tag_id: TAG_ID },
      { cookie: 'gs_session=s-1' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(200);
    expect(mocks.patchCalendarEvent).toHaveBeenCalledWith(
      'at',
      EVENT_ID,
      expect.objectContaining({ linked_tag_id: TAG_ID }),
    );
  });

  it('test 71: PATCH linked_episode_id → patchCalendarEvent called with that id', async () => {
    mocks.readCalendarEventById.mockResolvedValue({
      ok: true,
      value: nonRecurringEvent(),
    });

    const { request, context } = makePatch(
      { linked_episode_id: EPISODE_ID },
      { cookie: 'gs_session=s-1' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(200);
    expect(mocks.patchCalendarEvent).toHaveBeenCalledWith(
      'at',
      EVENT_ID,
      expect.objectContaining({ linked_episode_id: EPISODE_ID }),
    );
  });

  it('test 72: included=false on non-recurring → per-row PATCH with user_excluded', async () => {
    mocks.readCalendarEventById.mockResolvedValue({
      ok: true,
      value: nonRecurringEvent(),
    });

    const { request, context } = makePatch(
      { included_as_context: false },
      { cookie: 'gs_session=s-1' },
    );
    await PATCH(request, context);

    expect(mocks.insertSeriesExclusion).not.toHaveBeenCalled();
    expect(mocks.patchCalendarEventsBulk).not.toHaveBeenCalled();
    expect(mocks.patchCalendarEvent).toHaveBeenCalledWith(
      'at',
      EVENT_ID,
      expect.objectContaining({
        included_as_context: false,
        user_decision: 'user_excluded',
      }),
    );
  });

  it('test 73: included=false on recurring → series exclusion INSERTed + siblings bulk-PATCHed', async () => {
    mocks.readCalendarEventById.mockResolvedValue({
      ok: true,
      value: recurringEvent(),
    });

    const { request, context } = makePatch(
      { included_as_context: false },
      { cookie: 'gs_session=s-1' },
    );
    await PATCH(request, context);

    expect(mocks.insertSeriesExclusion).toHaveBeenCalledWith(
      'at',
      CONN_ID,
      'rec-yoga',
      expect.any(String),
    );
    expect(mocks.patchCalendarEventsBulk).toHaveBeenCalledWith(
      'at',
      ['sib-1', 'sib-2', 'sib-3'],
      {
        included_as_context: false,
        user_decision: 'user_excluded',
      },
    );
  });

  it('test 75: included=true on recurring → does NOT delete series_exclusion (asymmetric re-include)', async () => {
    mocks.readCalendarEventById.mockResolvedValue({
      ok: true,
      value: { ...recurringEvent(), included_as_context: false, user_decision: 'user_excluded' },
    });

    const { request, context } = makePatch(
      { included_as_context: true },
      { cookie: 'gs_session=s-1' },
    );
    await PATCH(request, context);

    expect(mocks.insertSeriesExclusion).not.toHaveBeenCalled();
    expect(mocks.patchCalendarEventsBulk).not.toHaveBeenCalled();
    expect(mocks.patchCalendarEvent).toHaveBeenCalledWith(
      'at',
      EVENT_ID,
      expect.objectContaining({
        included_as_context: true,
        user_decision: 'user_included',
      }),
    );
  });

  it('test 78: order — INSERT exclusion BEFORE bulk PATCH siblings', async () => {
    mocks.readCalendarEventById.mockResolvedValue({
      ok: true,
      value: recurringEvent(),
    });
    const callOrder: string[] = [];
    mocks.insertSeriesExclusion.mockImplementation(async () => {
      callOrder.push('insert');
      return { ok: true, value: undefined };
    });
    mocks.patchCalendarEventsBulk.mockImplementation(async () => {
      callOrder.push('bulk');
      return { ok: true, value: undefined };
    });

    const { request, context } = makePatch(
      { included_as_context: false },
      { cookie: 'gs_session=s-1' },
    );
    await PATCH(request, context);

    expect(callOrder).toEqual(['insert', 'bulk']);
  });
});
