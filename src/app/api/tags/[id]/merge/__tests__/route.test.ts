import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  mergeTag: vi.fn(),
  getValidatedSession: vi.fn(),
  writeCheck: vi.fn(),
}));

vi.mock('@/lib/api/tags', () => ({
  mergeTag: mocks.mergeTag,
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
      check: mocks.writeCheck,
      sweep: () => undefined,
    },
  };
});

import { POST } from '../route';

const sourceId = '01234567-89ab-cdef-0123-456789abcdef';
const targetId = '550e8400-e29b-41d4-a716-446655440000';

function makePost(
  id: string,
  body: unknown,
  opts: { cookie?: string; origin?: string; rawBody?: string } = {},
): {
  request: Request;
  context: { params: Promise<{ id: string }> };
} {
  const headers: Record<string, string> = {
    origin: opts.origin ?? 'http://localhost:3000',
    'content-type': 'application/json',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  const bodyText =
    opts.rawBody !== undefined ? opts.rawBody : JSON.stringify(body);
  const request = new Request(`http://localhost:3000/api/tags/${id}/merge`, {
    method: 'POST',
    headers,
    body: bodyText,
  });
  return { request, context: { params: Promise.resolve({ id }) } };
}

beforeEach(() => {
  mocks.mergeTag.mockReset();
  mocks.getValidatedSession.mockReset();
  mocks.writeCheck.mockReset();
  mocks.getValidatedSession.mockResolvedValue({
    accessToken: 'at-1',
    refreshToken: 'rt-1',
    expiresAt: Date.now() + 60_000,
  });
  mocks.writeCheck.mockReturnValue({ allowed: true });
});

describe('POST /api/tags/[id]/merge', () => {
  it('test 15: happy path → 200 with { source_id, target_id, affected_days }', async () => {
    mocks.mergeTag.mockResolvedValue({
      ok: true,
      value: { source_id: sourceId, target_id: targetId, affected_days: 4 },
    });

    const { request, context } = makePost(
      sourceId,
      { target_tag_id: targetId },
      { cookie: 'gs_session=s-id' },
    );
    const res = await POST(request, context);

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body).toEqual({
      source_id: sourceId,
      target_id: targetId,
      affected_days: 4,
    });
    expect(mocks.mergeTag).toHaveBeenCalledWith('at-1', sourceId, targetId);
  });

  it('test 16: non-UUID source id in URL → 400 invalid_id', async () => {
    const { request, context } = makePost(
      'not-a-uuid',
      { target_tag_id: targetId },
      { cookie: 'gs_session=s-id' },
    );
    const res = await POST(request, context);

    expect(res.status).toBe(400);
    expect((await res.json()).error).toBe('invalid_id');
    expect(mocks.mergeTag).not.toHaveBeenCalled();
  });

  it('test 17: missing target_tag_id in body → 400 malformed_body', async () => {
    const { request, context } = makePost(
      sourceId,
      {},
      { cookie: 'gs_session=s-id' },
    );
    const res = await POST(request, context);

    expect(res.status).toBe(400);
    expect((await res.json()).error).toBe('malformed_body');
    expect(mocks.mergeTag).not.toHaveBeenCalled();
  });

  it('test 17b: unparseable body → 400 malformed_body', async () => {
    const { request, context } = makePost(sourceId, null, {
      cookie: 'gs_session=s-id',
      rawBody: 'not json',
    });
    const res = await POST(request, context);

    expect(res.status).toBe(400);
    expect((await res.json()).error).toBe('malformed_body');
  });

  it('test 18: non-UUID target_tag_id → 400 invalid_target', async () => {
    const { request, context } = makePost(
      sourceId,
      { target_tag_id: 'not-a-uuid' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await POST(request, context);

    expect(res.status).toBe(400);
    expect((await res.json()).error).toBe('invalid_target');
    expect(mocks.mergeTag).not.toHaveBeenCalled();
  });

  it('test 19: no session cookie → 401', async () => {
    const { request, context } = makePost(sourceId, {
      target_tag_id: targetId,
    });
    const res = await POST(request, context);

    expect(res.status).toBe(401);
    expect((await res.json()).error).toBe('unauthenticated');
    expect(mocks.mergeTag).not.toHaveBeenCalled();
  });

  it('test 20: disallowed origin → 403', async () => {
    const { request, context } = makePost(
      sourceId,
      { target_tag_id: targetId },
      { cookie: 'gs_session=s-id', origin: 'http://evil.example.com' },
    );
    const res = await POST(request, context);

    expect(res.status).toBe(403);
    expect((await res.json()).error).toBe('forbidden');
    expect(mocks.mergeTag).not.toHaveBeenCalled();
  });

  it('test 21: rate-limited → 429', async () => {
    mocks.writeCheck.mockReturnValue({ allowed: false, retryAfterMs: 30_000 });

    const { request, context } = makePost(
      sourceId,
      { target_tag_id: targetId },
      { cookie: 'gs_session=s-id' },
    );
    const res = await POST(request, context);

    expect(res.status).toBe(429);
    const body = await res.json();
    expect(body.error).toBe('rate_limited');
    expect(body.retry_after_ms).toBe(30_000);
    expect(mocks.mergeTag).not.toHaveBeenCalled();
  });

  it.each([
    ['same_tag'],
    ['source_not_found'],
    ['target_not_found'],
    ['source_archived'],
    ['target_archived'],
    ['category_mismatch'],
  ])(
    'tests 22-26: lib reports %s → 400 with that code',
    async (errCode) => {
      mocks.mergeTag.mockResolvedValue({ ok: false, error: errCode });

      const { request, context } = makePost(
        sourceId,
        { target_tag_id: targetId },
        { cookie: 'gs_session=s-id' },
      );
      const res = await POST(request, context);

      expect(res.status).toBe(400);
      expect((await res.json()).error).toBe(errCode);
    },
  );

  it('test 27a: lib reports directus_error → 502 server_error', async () => {
    mocks.mergeTag.mockResolvedValue({ ok: false, error: 'directus_error' });

    const { request, context } = makePost(
      sourceId,
      { target_tag_id: targetId },
      { cookie: 'gs_session=s-id' },
    );
    const res = await POST(request, context);

    expect(res.status).toBe(502);
    expect((await res.json()).error).toBe('server_error');
  });

  it('test 27b: lib reports network_error → 502 server_error', async () => {
    mocks.mergeTag.mockResolvedValue({ ok: false, error: 'network_error' });

    const { request, context } = makePost(
      sourceId,
      { target_tag_id: targetId },
      { cookie: 'gs_session=s-id' },
    );
    const res = await POST(request, context);

    expect(res.status).toBe(502);
    expect((await res.json()).error).toBe('server_error');
  });
});
