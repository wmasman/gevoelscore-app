import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  updateTag: vi.fn(),
  deleteTag: vi.fn(),
  readTagById: vi.fn(),
  getValidatedSession: vi.fn(),
  writeCheck: vi.fn(),
}));

vi.mock('@/lib/api/tags', () => ({
  updateTag: mocks.updateTag,
  deleteTag: mocks.deleteTag,
  readTagById: mocks.readTagById,
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

import { DELETE, PATCH } from '../route';

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
  mocks.deleteTag.mockReset();
  mocks.readTagById.mockReset();
  mocks.getValidatedSession.mockReset();
  mocks.writeCheck.mockReset();
  mocks.getValidatedSession.mockResolvedValue({
    accessToken: 'at-1',
    refreshToken: 'rt-1',
    expiresAt: Date.now() + 60_000,
  });
  mocks.writeCheck.mockReturnValue({ allowed: true });
});

function makeDelete(
  id: string,
  opts: { cookie?: string; origin?: string } = {},
): {
  request: Request;
  context: { params: Promise<{ id: string }> };
} {
  const headers: Record<string, string> = {
    origin: opts.origin ?? 'http://localhost:3000',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  const request = new Request(`http://localhost:3000/api/tags/${id}`, {
    method: 'DELETE',
    headers,
  });
  return { request, context: { params: Promise.resolve({ id }) } };
}

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

  // ---------------------------------------------------------------------
  // Step v1.5b: extended PATCH surface (label / category / archived_at)
  // with per-field error variants (M1 audit fix).
  // ---------------------------------------------------------------------

  describe('extended patch surface', () => {
    it('returns 200 with updated tag for { label } patch', async () => {
      mocks.updateTag.mockResolvedValue({
        ok: true,
        value: { ...happyTag, label: 'pacing-strategy' },
      });

      const { request, context } = makePatch(
        validTagId,
        { label: 'pacing-strategy' },
        { cookie: 'gs_session=s-id' },
      );
      const res = await PATCH(request, context);

      expect(res.status).toBe(200);
      const body = await res.json();
      expect(body.tag.label).toBe('pacing-strategy');
    });

    it('returns 200 with updated tag for { category } patch', async () => {
      mocks.updateTag.mockResolvedValue({
        ok: true,
        value: { ...happyTag, category: 'fysiek' },
      });

      const { request, context } = makePatch(
        validTagId,
        { category: 'fysiek' },
        { cookie: 'gs_session=s-id' },
      );
      const res = await PATCH(request, context);

      expect(res.status).toBe(200);
    });

    it('returns 200 with updated tag for { archived_at: <ISO> } patch', async () => {
      const iso = '2026-06-03T10:00:00.000Z';
      mocks.updateTag.mockResolvedValue({
        ok: true,
        value: { ...happyTag, archived_at: iso },
      });

      const { request, context } = makePatch(
        validTagId,
        { archived_at: iso },
        { cookie: 'gs_session=s-id' },
      );
      const res = await PATCH(request, context);

      expect(res.status).toBe(200);
    });

    it('returns 200 with updated tag for { archived_at: null } patch (un-archive)', async () => {
      mocks.updateTag.mockResolvedValue({
        ok: true,
        value: { ...happyTag, archived_at: null },
      });

      const { request, context } = makePatch(
        validTagId,
        { archived_at: null },
        { cookie: 'gs_session=s-id' },
      );
      const res = await PATCH(request, context);

      expect(res.status).toBe(200);
    });

    it('returns 200 for a multi-field patch combining label + category + parent_episode_id', async () => {
      mocks.updateTag.mockResolvedValue({ ok: true, value: happyTag });

      const { request, context } = makePatch(
        validTagId,
        {
          label: 'pacing',
          category: 'mentaal',
          parent_episode_id: validEpisodeId,
        },
        { cookie: 'gs_session=s-id' },
      );
      const res = await PATCH(request, context);

      expect(res.status).toBe(200);
      const args = mocks.updateTag.mock.calls[0]?.[2];
      expect(args).toEqual({
        label: 'pacing',
        category: 'mentaal',
        parent_episode_id: validEpisodeId,
      });
    });

    it('returns 400 invalid_label when the lib reports invalid_label (M1)', async () => {
      mocks.updateTag.mockResolvedValue({ ok: false, error: 'invalid_label' });

      const { request, context } = makePatch(
        validTagId,
        { label: '' },
        { cookie: 'gs_session=s-id' },
      );
      const res = await PATCH(request, context);

      expect(res.status).toBe(400);
      const body = await res.json();
      expect(body.error).toBe('invalid_label');
    });

    it('returns 400 invalid_category when the lib reports invalid_category (M1)', async () => {
      mocks.updateTag.mockResolvedValue({
        ok: false,
        error: 'invalid_category',
      });

      const { request, context } = makePatch(
        validTagId,
        { category: 'made-up' },
        { cookie: 'gs_session=s-id' },
      );
      const res = await PATCH(request, context);

      expect(res.status).toBe(400);
      const body = await res.json();
      expect(body.error).toBe('invalid_category');
    });

    it('returns 400 invalid_archived_at when the lib reports invalid_archived_at (M1)', async () => {
      mocks.updateTag.mockResolvedValue({
        ok: false,
        error: 'invalid_archived_at',
      });

      const { request, context } = makePatch(
        validTagId,
        { archived_at: 'yesterday' },
        { cookie: 'gs_session=s-id' },
      );
      const res = await PATCH(request, context);

      expect(res.status).toBe(400);
      const body = await res.json();
      expect(body.error).toBe('invalid_archived_at');
    });
  });
});

// =========================================================================
// DELETE /api/tags/[id] — step v1.5b hard-delete with usage_count gate
// =========================================================================

describe('DELETE /api/tags/[id]', () => {
  const tagAt = (overrides: Partial<typeof happyTag> = {}) => ({
    ...happyTag,
    ...overrides,
  });

  it('returns 200 with deleted_id when usage_count === 0', async () => {
    mocks.readTagById.mockResolvedValue({
      ok: true,
      value: tagAt({ usage_count: 0 }),
    });
    mocks.deleteTag.mockResolvedValue({
      ok: true,
      value: { deleted_id: validTagId },
    });

    const { request, context } = makeDelete(validTagId, {
      cookie: 'gs_session=s-id',
    });
    const res = await DELETE(request, context);

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.deleted_id).toBe(validTagId);
    expect(mocks.deleteTag).toHaveBeenCalledWith('at-1', validTagId);
  });

  it('returns 400 tag_in_use when usage_count > 0 — Directus DELETE NOT called', async () => {
    mocks.readTagById.mockResolvedValue({
      ok: true,
      value: tagAt({ usage_count: 5 }),
    });

    const { request, context } = makeDelete(validTagId, {
      cookie: 'gs_session=s-id',
    });
    const res = await DELETE(request, context);

    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.error).toBe('tag_in_use');
    expect(body.usage_count).toBe(5);
    expect(mocks.deleteTag).not.toHaveBeenCalled();
  });

  it('returns 400 invalid_id for a non-UUID path param', async () => {
    const { request, context } = makeDelete('not-a-uuid', {
      cookie: 'gs_session=s-id',
    });
    const res = await DELETE(request, context);

    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.error).toBe('invalid_id');
    expect(mocks.deleteTag).not.toHaveBeenCalled();
  });

  it('returns 401 when the session cookie is missing', async () => {
    const { request, context } = makeDelete(validTagId);
    const res = await DELETE(request, context);

    expect(res.status).toBe(401);
    expect(mocks.deleteTag).not.toHaveBeenCalled();
  });

  it('returns 403 when the origin is not allowlisted', async () => {
    const { request, context } = makeDelete(validTagId, {
      cookie: 'gs_session=s-id',
      origin: 'https://evil.example.com',
    });
    const res = await DELETE(request, context);

    expect(res.status).toBe(403);
    expect(mocks.deleteTag).not.toHaveBeenCalled();
  });

  it('returns 429 when the rate limiter blocks the request', async () => {
    mocks.writeCheck.mockReturnValue({ allowed: false, retryAfterMs: 12345 });

    const { request, context } = makeDelete(validTagId, {
      cookie: 'gs_session=s-id',
    });
    const res = await DELETE(request, context);

    expect(res.status).toBe(429);
    const body = await res.json();
    expect(body.error).toBe('rate_limited');
    expect(body.retry_after_ms).toBe(12345);
    expect(mocks.deleteTag).not.toHaveBeenCalled();
  });

  it('returns 502 server_error for a non-existent UUID (M5: matches PATCH 502 path)', async () => {
    // The usage_count read fails because Directus has no row for the id.
    mocks.readTagById.mockResolvedValue({
      ok: false,
      error: 'directus_error',
    });

    const { request, context } = makeDelete(validTagId, {
      cookie: 'gs_session=s-id',
    });
    const res = await DELETE(request, context);

    expect(res.status).toBe(502);
    const body = await res.json();
    expect(body.error).toBe('server_error');
    expect(mocks.deleteTag).not.toHaveBeenCalled();
  });
});
