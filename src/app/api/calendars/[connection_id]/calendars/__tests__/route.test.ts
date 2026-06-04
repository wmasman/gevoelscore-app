// Step-1 Phase 1.C — GET + POST /api/calendars/[connection_id]/calendars tests.

import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  getValidatedSession: vi.fn(),
  writeCheck: vi.fn(),
  readConnectionById: vi.fn(),
  patchConnection: vi.fn(),
  decrypt: vi.fn(),
  getGoogleProvider: vi.fn(),
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
  readConnectionById: mocks.readConnectionById,
  patchConnection: mocks.patchConnection,
}));

vi.mock('@/lib/auth/envelope-encryption', () => ({
  decrypt: mocks.decrypt,
}));

vi.mock('@/lib/integrations/google/get-provider', () => ({
  getGoogleProvider: mocks.getGoogleProvider,
}));

import { GET, POST } from '../route';

const USER_ID = '16f6f68b-e683-4dc9-8afc-e80695c4259d';
const OTHER_USER_ID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';
const CONN_ID = '550e8400-e29b-41d4-a716-446655440000';

function makeGetReq(opts: { cookie?: string } = {}): {
  request: Request;
  context: { params: Promise<{ connection_id: string }> };
} {
  const headers: Record<string, string> = {
    origin: 'http://localhost:3000',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  return {
    request: new Request(
      `http://localhost:3000/api/calendars/${CONN_ID}/calendars`,
      { method: 'GET', headers },
    ),
    context: { params: Promise.resolve({ connection_id: CONN_ID }) },
  };
}

function makePostReq(
  body: unknown,
  opts: { cookie?: string } = {},
): {
  request: Request;
  context: { params: Promise<{ connection_id: string }> };
} {
  const headers: Record<string, string> = {
    origin: 'http://localhost:3000',
    'content-type': 'application/json',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  return {
    request: new Request(
      `http://localhost:3000/api/calendars/${CONN_ID}/calendars`,
      {
        method: 'POST',
        headers,
        body: JSON.stringify(body),
      },
    ),
    context: { params: Promise.resolve({ connection_id: CONN_ID }) },
  };
}

beforeEach(() => {
  vi.unstubAllEnvs();
  vi.stubEnv('WILLEM_USER_ID', USER_ID);
  vi.stubEnv('CALENDAR_KEK', 'test-kek-32-bytes-base64-pad-here==');
  vi.stubEnv('DIRECTUS_TOKEN', 'at');

  mocks.getValidatedSession.mockReset();
  mocks.writeCheck.mockReset();
  mocks.readConnectionById.mockReset();
  mocks.patchConnection.mockReset();
  mocks.decrypt.mockReset();
  mocks.getGoogleProvider.mockReset();

  mocks.getValidatedSession.mockResolvedValue({
    accessToken: 'at',
    refreshToken: 'rt',
    expiresAt: Date.now() + 60_000,
  });
  mocks.writeCheck.mockReturnValue({ allowed: true });
  mocks.readConnectionById.mockResolvedValue({
    ok: true,
    value: {
      id: CONN_ID,
      user_id: USER_ID,
      provider: 'google',
      provider_account_email: 'wmasman@gmail.com',
      refresh_token_encrypted: 'v1.iv.ct.tag',
      scope: 'calendar.readonly',
      connected_at: '2026-06-04T12:00:00Z',
      last_synced_at: null,
      last_sync_error: null,
      status: 'active',
      included_calendar_ids: [],
    },
  });
  mocks.patchConnection.mockResolvedValue({ ok: true, value: undefined });
  mocks.decrypt.mockReturnValue('plain-refresh-token');
  mocks.getGoogleProvider.mockReturnValue({
    id: 'google',
    refreshAccessToken: async () => ({
      accessToken: 'fresh-access',
      expiresAt: new Date(Date.now() + 3600_000),
    }),
    listCalendars: async () => [
      { id: 'wmasman@gmail.com', displayName: 'wmasman@gmail.com', isPrimary: true },
      { id: 'work-cal', displayName: 'Work', isPrimary: false },
    ],
  });
});

describe('GET /api/calendars/[connection_id]/calendars', () => {
  it('test 51: ownership mismatch (user_id differs) → 403', async () => {
    mocks.readConnectionById.mockResolvedValue({
      ok: true,
      value: {
        id: CONN_ID,
        user_id: OTHER_USER_ID,
        provider: 'google',
        provider_account_email: 'other@x.com',
        refresh_token_encrypted: 'v1.x.x.x',
        scope: 's',
        connected_at: '2026-06-04T12:00:00Z',
        last_synced_at: null,
        last_sync_error: null,
        status: 'active',
        included_calendar_ids: [],
      },
    });

    const { request, context } = makeGetReq({ cookie: 'gs_session=s-1' });
    const res = await GET(request, context);

    expect(res.status).toBe(403);
  });

  it('test 52: happy path → 200 with calendars list mapped from Google', async () => {
    const { request, context } = makeGetReq({ cookie: 'gs_session=s-1' });

    const res = await GET(request, context);

    expect(res.status).toBe(200);
    const body = (await res.json()) as {
      calendars: Array<{ id: string; displayName: string; isPrimary: boolean }>;
    };
    expect(body.calendars).toHaveLength(2);
    expect(body.calendars[0]!.isPrimary).toBe(true);
  });
});

describe('POST /api/calendars/[connection_id]/calendars', () => {
  it('test 53: non-array body → 400 malformed_body', async () => {
    const { request, context } = makePostReq(
      { included_calendar_ids: 'not-an-array' },
      { cookie: 'gs_session=s-1' },
    );

    const res = await POST(request, context);

    expect(res.status).toBe(400);
    expect((await res.json()).error).toBe('malformed_body');
  });

  it('test 54: non-string element → 400 malformed_body', async () => {
    const { request, context } = makePostReq(
      { included_calendar_ids: ['ok', 42, 'ok2'] },
      { cookie: 'gs_session=s-1' },
    );

    const res = await POST(request, context);

    expect(res.status).toBe(400);
    expect((await res.json()).error).toBe('malformed_body');
  });

  it('test 55: happy path → 200 + patchConnection called with the array', async () => {
    const { request, context } = makePostReq(
      { included_calendar_ids: ['cal-a', 'cal-b'] },
      { cookie: 'gs_session=s-1' },
    );

    const res = await POST(request, context);

    expect(res.status).toBe(200);
    expect(mocks.patchConnection).toHaveBeenCalledWith('at', CONN_ID, {
      included_calendar_ids: ['cal-a', 'cal-b'],
    });
  });

  it('test 56: phase-1.D defer note — POST does NOT trigger an immediate sync in Phase 1.C', async () => {
    // The orchestrator will be wired here in Phase 1.D. For now we just
    // assert no extra mocks needed.
    const { request, context } = makePostReq(
      { included_calendar_ids: ['cal-a'] },
      { cookie: 'gs_session=s-1' },
    );

    const res = await POST(request, context);

    expect(res.status).toBe(200);
    // patchConnection is the ONLY mock that should be called for writes.
    expect(mocks.patchConnection).toHaveBeenCalledTimes(1);
  });
});
