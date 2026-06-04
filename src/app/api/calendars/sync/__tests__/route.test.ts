// Step-1 Phase 1.D — POST /api/calendars/sync tests.

import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  getValidatedSession: vi.fn(),
  writeCheck: vi.fn(),
  readActiveConnectionsForUser: vi.fn(),
  readAllActiveConnections: vi.fn(),
  recordCronRun: vi.fn(),
  syncConnection: vi.fn(),
  getGoogleProvider: vi.fn(),
  decrypt: vi.fn(),
  readSeriesExclusionRecurrenceIds: vi.fn(),
  readEventsByProviderIds: vi.fn(),
  createCalendarEvent: vi.fn(),
  patchCalendarEvent: vi.fn(),
  patchConnection: vi.fn(),
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
  readActiveConnectionsForUser: mocks.readActiveConnectionsForUser,
  readAllActiveConnections: mocks.readAllActiveConnections,
  readSeriesExclusionRecurrenceIds: mocks.readSeriesExclusionRecurrenceIds,
  readEventsByProviderIds: mocks.readEventsByProviderIds,
  createCalendarEvent: mocks.createCalendarEvent,
  patchCalendarEvent: mocks.patchCalendarEvent,
  patchConnection: mocks.patchConnection,
  recordCronRun: mocks.recordCronRun,
}));

vi.mock('@/lib/sync/calendar-sync', () => ({
  syncConnection: mocks.syncConnection,
}));

vi.mock('@/lib/integrations/google/get-provider', () => ({
  getGoogleProvider: mocks.getGoogleProvider,
}));

vi.mock('@/lib/auth/envelope-encryption', () => ({
  decrypt: mocks.decrypt,
}));

import { POST } from '../route';

const USER_ID = '16f6f68b-e683-4dc9-8afc-e80695c4259d';

function makePost(opts: {
  cookie?: string;
  origin?: string;
  authHeader?: string;
} = {}): Request {
  const headers: Record<string, string> = {
    origin: opts.origin ?? 'http://localhost:3000',
    'content-type': 'application/json',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  if (opts.authHeader !== undefined) headers.authorization = opts.authHeader;
  return new Request('http://localhost:3000/api/calendars/sync', {
    method: 'POST',
    headers,
  });
}

beforeEach(() => {
  vi.unstubAllEnvs();
  vi.stubEnv('WILLEM_USER_ID', USER_ID);
  vi.stubEnv('CALENDAR_KEK', 'test-kek');
  // Step-1 used DIRECTUS_TOKEN for the bearer path; step-2 swaps to
  // CALENDAR_CRON_DIRECTUS_TOKEN (scoped to the frontend-api policy)
  // because DIRECTUS_TOKEN on Fly is the sessions-only scoped token
  // and would FORBIDDEN on calendar_connections.
  vi.stubEnv('CALENDAR_CRON_DIRECTUS_TOKEN', 'cron-token');
  vi.stubEnv('CALENDAR_SYNC_SECRET', 'bearer-secret-32-bytes-base64-here==');

  mocks.getValidatedSession.mockReset();
  mocks.writeCheck.mockReset();
  mocks.readActiveConnectionsForUser.mockReset();
  mocks.readAllActiveConnections.mockReset();
  mocks.recordCronRun.mockReset();
  mocks.recordCronRun.mockResolvedValue(undefined);
  mocks.syncConnection.mockReset();
  mocks.getGoogleProvider.mockReset();

  mocks.getValidatedSession.mockResolvedValue({
    accessToken: 'at',
    refreshToken: 'rt',
    expiresAt: Date.now() + 60_000,
  });
  mocks.writeCheck.mockReturnValue({ allowed: true });
  mocks.readActiveConnectionsForUser.mockResolvedValue({
    ok: true,
    value: [
      {
        id: 'conn-1',
        user_id: USER_ID,
        provider: 'google',
        refresh_token_encrypted: 'enc',
        included_calendar_ids: ['cal-a'],
        status: 'active',
      },
    ],
  });
  mocks.readAllActiveConnections.mockResolvedValue({
    ok: true,
    value: [
      { id: 'conn-1', user_id: USER_ID, provider: 'google', status: 'active' },
    ],
  });
  mocks.syncConnection.mockResolvedValue({
    connectionId: 'conn-1',
    eventsPulled: 5,
    eventsUpserted: 5,
    eventsExcludedBySeries: 0,
    errors: [],
  });
  mocks.getGoogleProvider.mockReturnValue({});
});

describe('POST /api/calendars/sync', () => {
  it('test 57: bad origin (no bearer) → 403 forbidden', async () => {
    const res = await POST(makePost({ origin: 'https://evil.example' }));

    expect(res.status).toBe(403);
  });

  it('test 58: no session and no bearer → 401', async () => {
    const res = await POST(makePost());

    expect(res.status).toBe(401);
  });

  it('test 59: invalid bearer (wrong secret) → falls through to session gate → 401', async () => {
    const res = await POST(makePost({ authHeader: 'Bearer wrong-secret' }));

    expect(res.status).toBe(401);
  });

  it('test 60: session path → 200 + aggregate result; readActiveConnectionsForUser called', async () => {
    const res = await POST(makePost({ cookie: 'gs_session=s-1' }));

    expect(res.status).toBe(200);
    const body = (await res.json()) as {
      ok: boolean;
      scope: string;
      connections: number;
      events_pulled: number;
    };
    expect(body.ok).toBe(true);
    expect(body.scope).toBe('session');
    expect(body.connections).toBe(1);
    expect(body.events_pulled).toBe(5);
    expect(mocks.readActiveConnectionsForUser).toHaveBeenCalled();
    expect(mocks.readAllActiveConnections).not.toHaveBeenCalled();
  });

  it('test 61: bearer path → 200 + readAllActiveConnections called (system scope)', async () => {
    const res = await POST(
      makePost({
        authHeader: 'Bearer bearer-secret-32-bytes-base64-here==',
      }),
    );

    expect(res.status).toBe(200);
    const body = (await res.json()) as { scope: string };
    expect(body.scope).toBe('bearer');
    expect(mocks.readAllActiveConnections).toHaveBeenCalled();
    expect(mocks.readActiveConnectionsForUser).not.toHaveBeenCalled();
  });

  it('test 61b (step-2): bearer path uses CALENDAR_CRON_DIRECTUS_TOKEN as the Directus accessToken (not session.accessToken)', async () => {
    await POST(
      makePost({
        authHeader: 'Bearer bearer-secret-32-bytes-base64-here==',
      }),
    );

    // The wrapper-call here is the loadActiveConnections path; it must
    // be invoked with the cron token, not anything user-scoped.
    expect(mocks.readAllActiveConnections).toHaveBeenCalledWith('cron-token');
  });

  it('test 61c (step-2): bearer path with valid auth but CALENDAR_CRON_DIRECTUS_TOKEN unset → 500 server_error', async () => {
    vi.stubEnv('CALENDAR_CRON_DIRECTUS_TOKEN', '');
    const res = await POST(
      makePost({
        authHeader: 'Bearer bearer-secret-32-bytes-base64-here==',
      }),
    );

    expect(res.status).toBe(500);
    expect((await res.json()).error).toBe('server_error');
    // Must NOT reach the Directus layer when the env var is missing.
    expect(mocks.readAllActiveConnections).not.toHaveBeenCalled();
  });

  it('test 62: per-connection error is captured in result.errors but route still returns 200', async () => {
    mocks.syncConnection.mockResolvedValue({
      connectionId: 'conn-1',
      eventsPulled: 0,
      eventsUpserted: 0,
      eventsExcludedBySeries: 0,
      errors: ['refresh_token_invalid'],
    });

    const res = await POST(makePost({ cookie: 'gs_session=s-1' }));

    expect(res.status).toBe(200);
    const body = (await res.json()) as { errors: string[] };
    expect(body.errors).toContain('refresh_token_invalid');
  });

  it('test 63: bearer-gate uses constant-time comparison (matching length wrong content → falls through to session)', async () => {
    // Same length as the valid secret, but content differs.
    const samelen = 'X'.repeat('bearer-secret-32-bytes-base64-here=='.length);
    const res = await POST(makePost({ authHeader: `Bearer ${samelen}` }));

    expect(res.status).toBe(401); // falls through, no session → 401
  });

  // ────────────────────────────────────────────────────────────
  // step-2 Phase 2.B — recordCronRun integration (AC2.3-2.5)
  // ────────────────────────────────────────────────────────────

  it('test 64 (step-2): session path → recordCronRun called with success counts (AC2.4)', async () => {
    await POST(makePost({ cookie: 'gs_session=s-1' }));

    expect(mocks.recordCronRun).toHaveBeenCalledTimes(1);
    expect(mocks.recordCronRun).toHaveBeenCalledWith(
      'at',
      'daily_calendar_sync',
      {
        ok: true,
        details: {
          connections: 1,
          events_pulled: 5,
          events_upserted: 5,
          events_excluded_by_series: 0,
        },
      },
    );
  });

  it('test 65 (step-2): bearer path → recordCronRun called with the cron token + success counts (AC2.4)', async () => {
    await POST(
      makePost({
        authHeader: 'Bearer bearer-secret-32-bytes-base64-here==',
      }),
    );

    expect(mocks.recordCronRun).toHaveBeenCalledTimes(1);
    expect(mocks.recordCronRun).toHaveBeenCalledWith(
      'cron-token',
      'daily_calendar_sync',
      {
        ok: true,
        details: {
          connections: 1,
          events_pulled: 5,
          events_upserted: 5,
          events_excluded_by_series: 0,
        },
      },
    );
  });

  it('test 66 (step-2): if recordCronRun rejects, the sync route still returns 200 with aggregate results (AC2.5)', async () => {
    // Defense in depth — the wrapper itself is no-throw, but the route
    // must also swallow any breach of that contract so a future bug
    // in recordCronRun can never break the user's Ververs nu response
    // or the cron's HTTP signal.
    mocks.recordCronRun.mockRejectedValueOnce(
      new Error('cron_monitor unreachable'),
    );

    const res = await POST(makePost({ cookie: 'gs_session=s-1' }));

    expect(res.status).toBe(200);
    const body = (await res.json()) as { ok: boolean; events_pulled: number };
    expect(body.ok).toBe(true);
    expect(body.events_pulled).toBe(5);
    // The route MUST attempt the monitor write. Without this check the
    // test passes vacuously when recordCronRun isn't wired at all.
    expect(mocks.recordCronRun).toHaveBeenCalledTimes(1);
  });

  it('test 67 (step-2): per-connection error → recordCronRun called with { ok: false, error: code } (AC2.3)', async () => {
    mocks.syncConnection.mockResolvedValue({
      connectionId: 'conn-1',
      eventsPulled: 0,
      eventsUpserted: 0,
      eventsExcludedBySeries: 0,
      errors: ['refresh_token_invalid'],
    });

    await POST(makePost({ cookie: 'gs_session=s-1' }));

    expect(mocks.recordCronRun).toHaveBeenCalledTimes(1);
    expect(mocks.recordCronRun).toHaveBeenCalledWith(
      'at',
      'daily_calendar_sync',
      { ok: false, error: 'refresh_token_invalid' },
    );
  });
});
