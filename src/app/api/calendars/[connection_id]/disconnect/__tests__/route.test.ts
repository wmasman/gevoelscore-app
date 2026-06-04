// Step-1 Phase 1.C — POST /api/calendars/[connection_id]/disconnect tests.

import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  getValidatedSession: vi.fn(),
  writeCheck: vi.fn(),
  readConnectionById: vi.fn(),
  deleteConnection: vi.fn(),
  decrypt: vi.fn(),
  getGoogleProvider: vi.fn(),
  revoke: vi.fn(),
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
  deleteConnection: mocks.deleteConnection,
}));

vi.mock('@/lib/auth/envelope-encryption', () => ({
  decrypt: mocks.decrypt,
}));

vi.mock('@/lib/integrations/google/get-provider', () => ({
  getGoogleProvider: mocks.getGoogleProvider,
}));

import { POST } from '../route';

const USER_ID = '16f6f68b-e683-4dc9-8afc-e80695c4259d';
const OTHER_USER_ID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';
const CONN_ID = '550e8400-e29b-41d4-a716-446655440000';

function makePost(opts: { cookie?: string } = {}): {
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
      `http://localhost:3000/api/calendars/${CONN_ID}/disconnect`,
      { method: 'POST', headers },
    ),
    context: { params: Promise.resolve({ connection_id: CONN_ID }) },
  };
}

beforeEach(() => {
  vi.unstubAllEnvs();
  vi.stubEnv('WILLEM_USER_ID', USER_ID);
  vi.stubEnv('CALENDAR_KEK', 'test-kek-32-bytes-base64-pad-here==');
  vi.stubEnv('DIRECTUS_TOKEN', 'admin-token');

  mocks.getValidatedSession.mockReset();
  mocks.writeCheck.mockReset();
  mocks.readConnectionById.mockReset();
  mocks.deleteConnection.mockReset();
  mocks.decrypt.mockReset();
  mocks.getGoogleProvider.mockReset();
  mocks.revoke.mockReset();

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
  mocks.deleteConnection.mockResolvedValue({ ok: true, value: undefined });
  mocks.decrypt.mockReturnValue('plain-refresh');
  mocks.revoke.mockResolvedValue(undefined);
  mocks.getGoogleProvider.mockReturnValue({
    id: 'google',
    revoke: mocks.revoke,
  });
});

describe('POST /api/calendars/[connection_id]/disconnect', () => {
  it('test 64: ownership mismatch → 403', async () => {
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

    const { request, context } = makePost({ cookie: 'gs_session=s-1' });
    const res = await POST(request, context);

    expect(res.status).toBe(403);
  });

  it('test 65: happy path → 200, revoke called, cascade triggered via deleteConnection', async () => {
    const { request, context } = makePost({ cookie: 'gs_session=s-1' });

    const res = await POST(request, context);

    expect(res.status).toBe(200);
    expect(mocks.revoke).toHaveBeenCalledWith('plain-refresh');
    expect(mocks.deleteConnection).toHaveBeenCalledWith('admin-token', CONN_ID);
    const body = (await res.json()) as { ok: boolean; revoke_ok: boolean };
    expect(body.ok).toBe(true);
    expect(body.revoke_ok).toBe(true);
  });

  it('test 67: revoke failure (Google 500) → local cascade still runs; response includes revoke_ok=false', async () => {
    mocks.revoke.mockRejectedValue(new Error('revoke HTTP 500'));

    const { request, context } = makePost({ cookie: 'gs_session=s-1' });
    const res = await POST(request, context);

    expect(res.status).toBe(200);
    expect(mocks.deleteConnection).toHaveBeenCalled();
    const body = (await res.json()) as { ok: boolean; revoke_ok: boolean };
    expect(body.revoke_ok).toBe(false);
  });

  it('test 68: revoke "already revoked" (provider treats 400 as success) → revoke_ok=true', async () => {
    // The provider's revoke() function swallows 400 invalid_token and
    // resolves, so the route sees a successful revoke.
    mocks.revoke.mockResolvedValue(undefined);

    const { request, context } = makePost({ cookie: 'gs_session=s-1' });
    const res = await POST(request, context);

    const body = (await res.json()) as { revoke_ok: boolean };
    expect(body.revoke_ok).toBe(true);
  });

  it('extra: not_found → 404 (connection_id resolved to nothing)', async () => {
    mocks.readConnectionById.mockResolvedValue({ ok: true, value: null });

    const { request, context } = makePost({ cookie: 'gs_session=s-1' });
    const res = await POST(request, context);

    expect(res.status).toBe(404);
  });
});
