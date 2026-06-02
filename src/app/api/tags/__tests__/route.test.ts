import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  createOrUpsertTag: vi.fn(),
  getValidatedSession: vi.fn(),
  rateLimiterCheck: vi.fn(),
}));

vi.mock('@/lib/api/tags', () => ({
  createOrUpsertTag: mocks.createOrUpsertTag,
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
    tagWriteRateLimiter: {
      check: mocks.rateLimiterCheck,
      sweep: () => undefined,
    },
  };
});

import { POST } from '../route';

function makeRequest(
  body: unknown,
  opts: { cookie?: string; origin?: string; clientIp?: string } = {},
) {
  const headers: Record<string, string> = {
    origin: opts.origin ?? 'http://localhost:3000',
    'content-type': 'application/json',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  if (opts.clientIp !== undefined) headers['fly-client-ip'] = opts.clientIp;
  return new Request('http://localhost:3000/api/tags', {
    method: 'POST',
    headers,
    body: typeof body === 'string' ? body : JSON.stringify(body),
  });
}

describe('POST /api/tags', () => {
  beforeEach(() => {
    mocks.createOrUpsertTag.mockReset();
    mocks.getValidatedSession.mockReset();
    mocks.rateLimiterCheck.mockReset();
    mocks.getValidatedSession.mockResolvedValue({
      accessToken: 'at-1',
      refreshToken: 'rt-1',
      expiresAt: Date.now() + 60_000,
    });
    mocks.rateLimiterCheck.mockReturnValue({ allowed: true });
  });

  it('returns 200 with outcome=created on happy path', async () => {
    mocks.createOrUpsertTag.mockResolvedValue({
      ok: true,
      value: {
        kind: 'created',
        tag: {
          id: 'tag-new',
          label: 'pacing',
          category: 'mentaal',
          project_id: null,
          usage_count: 0,
          archived_at: null,
          created_at: '2026-06-01T00:00:00.000Z',
        },
      },
    });

    const res = await POST(
      makeRequest(
        { label: 'pacing', category: 'mentaal' },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.outcome).toBe('created');
    expect(body.tag.id).toBe('tag-new');
  });

  it('returns 200 with outcome=matched_active for an existing-tag dedup', async () => {
    mocks.createOrUpsertTag.mockResolvedValue({
      ok: true,
      value: {
        kind: 'matched_active',
        tag: {
          id: 'tag-existing',
          label: 'pacing',
          category: 'mentaal',
          project_id: null,
          usage_count: 5,
          archived_at: null,
          created_at: '2026-01-01T00:00:00.000Z',
        },
      },
    });

    const res = await POST(
      makeRequest(
        { label: 'PACING', category: 'mentaal' },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.outcome).toBe('matched_active');
  });

  it('returns 200 with outcome=matched_reactivated when an archived tag is reactivated', async () => {
    mocks.createOrUpsertTag.mockResolvedValue({
      ok: true,
      value: {
        kind: 'matched_reactivated',
        tag: {
          id: 'tag-archived',
          label: 'coaching',
          category: 'interventie',
          project_id: null,
          usage_count: 0,
          archived_at: null,
          created_at: '2026-04-01T00:00:00.000Z',
        },
      },
    });

    const res = await POST(
      makeRequest(
        { label: 'coaching', category: 'interventie' },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.outcome).toBe('matched_reactivated');
  });

  it('returns 403 when origin is not allowlisted', async () => {
    const res = await POST(
      makeRequest(
        { label: 'pacing', category: 'mentaal' },
        { cookie: 'gs_session=s-id', origin: 'https://evil.example.com' },
      ),
    );

    expect(res.status).toBe(403);
    expect(mocks.createOrUpsertTag).not.toHaveBeenCalled();
  });

  it('returns 401 when the session cookie is missing', async () => {
    const res = await POST(makeRequest({ label: 'pacing', category: 'mentaal' }));

    expect(res.status).toBe(401);
    expect(mocks.createOrUpsertTag).not.toHaveBeenCalled();
  });

  it('returns 401 when getValidatedSession returns null', async () => {
    mocks.getValidatedSession.mockResolvedValueOnce(null);

    const res = await POST(
      makeRequest(
        { label: 'pacing', category: 'mentaal' },
        { cookie: 'gs_session=stale' },
      ),
    );

    expect(res.status).toBe(401);
    expect(mocks.createOrUpsertTag).not.toHaveBeenCalled();
  });

  it('returns 429 when the rate limiter blocks the request', async () => {
    mocks.rateLimiterCheck.mockReturnValue({
      allowed: false,
      retryAfterMs: 12345,
    });

    const res = await POST(
      makeRequest(
        { label: 'pacing', category: 'mentaal' },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(res.status).toBe(429);
    const body = await res.json();
    expect(body.error).toBe('rate_limited');
    expect(body.retry_after_ms).toBe(12345);
    expect(mocks.createOrUpsertTag).not.toHaveBeenCalled();
  });

  it('returns 400 on malformed body (not JSON)', async () => {
    const res = await POST(
      makeRequest('not json at all', { cookie: 'gs_session=s-id' }),
    );

    expect(res.status).toBe(400);
  });

  it('returns 400 when label is missing', async () => {
    const res = await POST(
      makeRequest({ category: 'mentaal' }, { cookie: 'gs_session=s-id' }),
    );

    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.error).toBe('malformed_body');
  });

  it('returns 400 invalid_label when the lib reports invalid_label', async () => {
    mocks.createOrUpsertTag.mockResolvedValue({
      ok: false,
      error: 'invalid_label',
    });

    const res = await POST(
      makeRequest(
        { label: 'naar de fysio', category: 'interventie' },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.error).toBe('invalid_label');
  });

  it('returns 400 invalid_category when the lib reports invalid_category', async () => {
    mocks.createOrUpsertTag.mockResolvedValue({
      ok: false,
      error: 'invalid_category',
    });

    const res = await POST(
      makeRequest(
        { label: 'pacing', category: 'made-up' },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.error).toBe('invalid_category');
  });

  it('returns 502 when the lib surfaces a directus_error', async () => {
    mocks.createOrUpsertTag.mockResolvedValue({
      ok: false,
      error: 'directus_error',
    });

    const res = await POST(
      makeRequest(
        { label: 'pacing', category: 'mentaal' },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(res.status).toBe(502);
  });

  // -------------------------------------------------------------------------
  // Step-5 extension: parent_episode_id in POST body
  // -------------------------------------------------------------------------

  it('regression: POST without parent_episode_id passes input through unchanged', async () => {
    mocks.createOrUpsertTag.mockResolvedValue({
      ok: true,
      value: {
        kind: 'created',
        tag: {
          id: 'tag-new',
          label: 'pacing',
          category: 'mentaal',
          project_id: null,
          parent_episode_id: null,
          usage_count: 0,
          archived_at: null,
          created_at: '2026-06-01T00:00:00.000Z',
        },
      },
    });

    const res = await POST(
      makeRequest(
        { label: 'pacing', category: 'mentaal' },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(res.status).toBe(200);
    // The route must NOT inject parent_episode_id when the caller omits it.
    const args = mocks.createOrUpsertTag.mock.calls[0]?.[1] as Record<
      string,
      unknown
    >;
    expect(args).not.toHaveProperty('parent_episode_id');
  });

  it('POST with parent_episode_id: <UUID> threads value to createOrUpsertTag', async () => {
    const VALID_EPISODE_ID = '550e8400-e29b-41d4-a716-446655440000';
    mocks.createOrUpsertTag.mockResolvedValue({
      ok: true,
      value: {
        kind: 'created',
        tag: {
          id: 'tag-new',
          label: 'coaching sessie',
          category: 'interventie',
          project_id: null,
          parent_episode_id: VALID_EPISODE_ID,
          usage_count: 0,
          archived_at: null,
          created_at: '2026-06-02T00:00:00.000Z',
        },
      },
    });

    const res = await POST(
      makeRequest(
        {
          label: 'coaching sessie',
          category: 'interventie',
          parent_episode_id: VALID_EPISODE_ID,
        },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.tag.parent_episode_id).toBe(VALID_EPISODE_ID);
    const args = mocks.createOrUpsertTag.mock.calls[0]?.[1] as Record<
      string,
      unknown
    >;
    expect(args.parent_episode_id).toBe(VALID_EPISODE_ID);
  });

  it('POST with parent_episode_id: null threads explicit null through', async () => {
    mocks.createOrUpsertTag.mockResolvedValue({
      ok: true,
      value: {
        kind: 'created',
        tag: {
          id: 'tag-new',
          label: 'standalone',
          category: 'mentaal',
          project_id: null,
          parent_episode_id: null,
          usage_count: 0,
          archived_at: null,
          created_at: '2026-06-02T00:00:00.000Z',
        },
      },
    });

    const res = await POST(
      makeRequest(
        { label: 'standalone', category: 'mentaal', parent_episode_id: null },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(res.status).toBe(200);
    const args = mocks.createOrUpsertTag.mock.calls[0]?.[1] as Record<
      string,
      unknown
    >;
    expect(args).toHaveProperty('parent_episode_id', null);
  });

  it('returns 400 invalid_parent_episode_id when the lib rejects a malformed UUID', async () => {
    mocks.createOrUpsertTag.mockResolvedValue({
      ok: false,
      error: 'invalid_parent_episode_id',
    });

    const res = await POST(
      makeRequest(
        {
          label: 'pacing',
          category: 'mentaal',
          parent_episode_id: 'not-a-uuid',
        },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.error).toBe('invalid_parent_episode_id');
  });

  it('does NOT attempt to attach to a day_entry — the route is single-purpose', async () => {
    mocks.createOrUpsertTag.mockResolvedValue({
      ok: true,
      value: {
        kind: 'created',
        tag: {
          id: 'tag-new',
          label: 'pacing',
          category: 'mentaal',
          project_id: null,
          usage_count: 0,
          archived_at: null,
          created_at: '2026-06-01T00:00:00.000Z',
        },
      },
    });

    const res = await POST(
      makeRequest(
        // Even if a client tries to pass attach_to_date, the route ignores it.
        { label: 'pacing', category: 'mentaal', attach_to_date: '2026-06-01' },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body).not.toHaveProperty('attach_error');
    expect(body).not.toHaveProperty('attached');
  });
});
