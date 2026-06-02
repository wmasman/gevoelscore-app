import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  updateTag: vi.fn(),
  getValidatedSession: vi.fn(),
  writeCheck: vi.fn(),
}));

vi.mock('@/lib/api/tags', () => ({
  updateTag: mocks.updateTag,
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

import { PATCH } from '../route';

const validTagId = '01234567-89ab-cdef-0123-456789abcdef';
const validEpisodeId = '550e8400-e29b-41d4-a716-446655440000';

const happyTag = {
  id: validTagId,
  label: 'coaching sessie',
  category: 'interventie' as const,
  project_id: null,
  parent_episode_id: validEpisodeId,
  usage_count: 0,
  archived_at: null,
  created_at: '2026-06-02T00:00:00.000Z',
};

function makePatch(
  id: string,
  body: unknown,
  opts: { cookie?: string; origin?: string } = {},
): {
  request: Request;
  context: { params: Promise<{ id: string }> };
} {
  const headers: Record<string, string> = {
    origin: opts.origin ?? 'http://localhost:3000',
    'content-type': 'application/json',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  const request = new Request(`http://localhost:3000/api/tags/${id}`, {
    method: 'PATCH',
    headers,
    body: typeof body === 'string' ? body : JSON.stringify(body),
  });
  return { request, context: { params: Promise.resolve({ id }) } };
}

beforeEach(() => {
  mocks.updateTag.mockReset();
  mocks.getValidatedSession.mockReset();
  mocks.writeCheck.mockReset();
  mocks.getValidatedSession.mockResolvedValue({
    accessToken: 'at-1',
    refreshToken: 'rt-1',
    expiresAt: Date.now() + 60_000,
  });
  mocks.writeCheck.mockReturnValue({ allowed: true });
});

describe('PATCH /api/tags/[id]', () => {
  it('returns 200 with the updated tag when parent_episode_id is set', async () => {
    mocks.updateTag.mockResolvedValue({ ok: true, value: happyTag });

    const { request, context } = makePatch(
      validTagId,
      { parent_episode_id: validEpisodeId },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.tag.id).toBe(validTagId);
    expect(body.tag.parent_episode_id).toBe(validEpisodeId);
    expect(mocks.updateTag).toHaveBeenCalledWith('at-1', validTagId, {
      parent_episode_id: validEpisodeId,
    });
  });

  it('returns 200 with the updated tag when parent_episode_id is null', async () => {
    mocks.updateTag.mockResolvedValue({
      ok: true,
      value: { ...happyTag, parent_episode_id: null },
    });

    const { request, context } = makePatch(
      validTagId,
      { parent_episode_id: null },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.tag.parent_episode_id).toBeNull();
  });

  it('returns 400 invalid_id when the path id is not UUID-shape', async () => {
    const { request, context } = makePatch(
      'not-a-uuid',
      { parent_episode_id: null },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.error).toBe('invalid_id');
    expect(mocks.updateTag).not.toHaveBeenCalled();
  });

  it('returns 400 malformed_body when the request body is not JSON', async () => {
    const { request, context } = makePatch(validTagId, 'not json', {
      cookie: 'gs_session=s-id',
    });
    const res = await PATCH(request, context);

    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.error).toBe('malformed_body');
  });

  it('returns 400 invalid_patch when the body contains an unknown key', async () => {
    mocks.updateTag.mockResolvedValue({ ok: false, error: 'invalid_patch' });

    const { request, context } = makePatch(
      validTagId,
      { label: 'sneaky', parent_episode_id: validEpisodeId },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.error).toBe('invalid_patch');
  });

  it('returns 401 when the session cookie is missing', async () => {
    const { request, context } = makePatch(validTagId, {
      parent_episode_id: null,
    });
    const res = await PATCH(request, context);

    expect(res.status).toBe(401);
    expect(mocks.updateTag).not.toHaveBeenCalled();
  });

  it('returns 401 when getValidatedSession returns null (stale session)', async () => {
    mocks.getValidatedSession.mockResolvedValueOnce(null);

    const { request, context } = makePatch(
      validTagId,
      { parent_episode_id: null },
      { cookie: 'gs_session=stale' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(401);
    expect(mocks.updateTag).not.toHaveBeenCalled();
  });

  it('returns 403 when the origin is not allowlisted', async () => {
    const { request, context } = makePatch(
      validTagId,
      { parent_episode_id: null },
      { cookie: 'gs_session=s-id', origin: 'https://evil.example.com' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(403);
    expect(mocks.updateTag).not.toHaveBeenCalled();
  });

  it('returns 429 when the rate limiter blocks the request', async () => {
    mocks.writeCheck.mockReturnValue({ allowed: false, retryAfterMs: 12345 });

    const { request, context } = makePatch(
      validTagId,
      { parent_episode_id: null },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(429);
    const body = await res.json();
    expect(body.error).toBe('rate_limited');
    expect(body.retry_after_ms).toBe(12345);
    expect(mocks.updateTag).not.toHaveBeenCalled();
  });

  it('returns 502 when the lib surfaces a directus_error (missing tag id)', async () => {
    mocks.updateTag.mockResolvedValue({ ok: false, error: 'directus_error' });

    const { request, context } = makePatch(
      validTagId,
      { parent_episode_id: validEpisodeId },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(502);
    const body = await res.json();
    expect(body.error).toBe('server_error');
  });
});
