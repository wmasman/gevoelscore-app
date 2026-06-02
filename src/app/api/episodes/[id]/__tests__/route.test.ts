import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  updateEpisode: vi.fn(),
  getValidatedSession: vi.fn(),
  writeCheck: vi.fn(),
}));

vi.mock('@/lib/api/episodes', () => ({
  updateEpisode: mocks.updateEpisode,
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
    episodeWriteRateLimiter: {
      check: mocks.writeCheck,
      sweep: () => undefined,
    },
  };
});

import { PATCH } from '../route';

const validUuid = '01234567-89ab-cdef-0123-456789abcdef';

const happyEpisode = {
  id: validUuid,
  label: 'Coaching met Sarah',
  category: 'interventie' as const,
  start_date: '2026-04-01',
  end_date: null,
  description: null,
  calendar_binding: null,
  archived_at: null,
  created_at: '2026-04-01T08:00:00.000Z',
  updated_at: '2026-06-02T12:00:00.000Z',
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
  const request = new Request(`http://localhost:3000/api/episodes/${id}`, {
    method: 'PATCH',
    headers,
    body: typeof body === 'string' ? body : JSON.stringify(body),
  });
  return { request, context: { params: Promise.resolve({ id }) } };
}

beforeEach(() => {
  mocks.updateEpisode.mockReset();
  mocks.getValidatedSession.mockReset();
  mocks.writeCheck.mockReset();
  mocks.getValidatedSession.mockResolvedValue({
    accessToken: 'at-1',
    refreshToken: 'rt-1',
    expiresAt: Date.now() + 60_000,
  });
  mocks.writeCheck.mockReturnValue({ allowed: true });
});

describe('PATCH /api/episodes/[id]', () => {
  it('returns 200 with { episode } on valid partial body', async () => {
    mocks.updateEpisode.mockResolvedValue({ ok: true, value: happyEpisode });

    const { request, context } = makePatch(
      validUuid,
      { label: 'New label' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.episode.id).toBe(validUuid);
  });

  it('forwards the partial patch to the wrapper', async () => {
    mocks.updateEpisode.mockResolvedValue({ ok: true, value: happyEpisode });

    const { request, context } = makePatch(
      validUuid,
      { description: 'updated', archived_at: null },
      { cookie: 'gs_session=s-id' },
    );
    await PATCH(request, context);

    expect(mocks.updateEpisode).toHaveBeenCalledWith('at-1', validUuid, {
      description: 'updated',
      archived_at: null,
    });
  });

  it('archives the episode when body is { archived_at: ISO }', async () => {
    mocks.updateEpisode.mockResolvedValue({ ok: true, value: happyEpisode });

    const { request, context } = makePatch(
      validUuid,
      { archived_at: '2026-06-02T12:00:00.000Z' },
      { cookie: 'gs_session=s-id' },
    );
    await PATCH(request, context);

    expect(mocks.updateEpisode).toHaveBeenCalledWith('at-1', validUuid, {
      archived_at: '2026-06-02T12:00:00.000Z',
    });
  });

  it('un-archives when body is { archived_at: null }', async () => {
    mocks.updateEpisode.mockResolvedValue({ ok: true, value: happyEpisode });

    const { request, context } = makePatch(
      validUuid,
      { archived_at: null },
      { cookie: 'gs_session=s-id' },
    );
    await PATCH(request, context);

    expect(mocks.updateEpisode).toHaveBeenCalledWith('at-1', validUuid, {
      archived_at: null,
    });
  });

  // -------------------------------------------------------------------------
  // Unhappy paths
  // -------------------------------------------------------------------------

  it('returns 403 forbidden on cross-origin', async () => {
    const { request, context } = makePatch(
      validUuid,
      { label: 'x' },
      { cookie: 'gs_session=s-id', origin: 'https://evil.example.com' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(403);
    expect(mocks.updateEpisode).not.toHaveBeenCalled();
  });

  it('returns 429 when write rate-limit denies', async () => {
    mocks.writeCheck.mockReturnValue({ allowed: false, retryAfterMs: 1234 });

    const { request, context } = makePatch(
      validUuid,
      { label: 'x' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(429);
  });

  it('returns 401 when no session cookie', async () => {
    const { request, context } = makePatch(validUuid, { label: 'x' });
    const res = await PATCH(request, context);

    expect(res.status).toBe(401);
  });

  it('returns 401 when session resolves to null', async () => {
    mocks.getValidatedSession.mockResolvedValue(null);

    const { request, context } = makePatch(
      validUuid,
      { label: 'x' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(401);
  });

  it('returns 400 invalid_request when [id] is empty string', async () => {
    const { request, context } = makePatch(
      '',
      { label: 'x' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(400);
    expect(mocks.updateEpisode).not.toHaveBeenCalled();
  });

  it('returns 400 invalid_request when [id] is not UUID-shape ("not-a-uuid")', async () => {
    const { request, context } = makePatch(
      'not-a-uuid',
      { label: 'x' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(400);
    expect(mocks.updateEpisode).not.toHaveBeenCalled();
  });

  it('returns 400 invalid_request when [id] is a script-injection probe', async () => {
    // Defense-in-depth: malicious-looking values get rejected at the
    // boundary rather than being reflected into error paths or wasting
    // a Directus round-trip.
    const { request, context } = makePatch(
      'javascript:alert(1)',
      { label: 'x' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(400);
    expect(mocks.updateEpisode).not.toHaveBeenCalled();
  });

  it('returns 400 empty_patch on empty body', async () => {
    const { request, context } = makePatch(
      validUuid,
      {},
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(400);
    expect(await res.json()).toEqual({ error: 'empty_patch' });
    expect(mocks.updateEpisode).not.toHaveBeenCalled();
  });

  it('returns 400 malformed_body on non-JSON body', async () => {
    const { request, context } = makePatch(
      validUuid,
      'not-json-{',
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(400);
    expect(mocks.updateEpisode).not.toHaveBeenCalled();
  });

  it('returns 400 invalid_archived_at on garbage timestamp', async () => {
    mocks.updateEpisode.mockResolvedValue({
      ok: false,
      error: 'invalid_archived_at',
    });

    const { request, context } = makePatch(
      validUuid,
      { archived_at: 'not-a-timestamp' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(400);
    expect(await res.json()).toEqual({ error: 'invalid_archived_at' });
  });

  it('returns 400 invalid_label when wrapper rejects', async () => {
    mocks.updateEpisode.mockResolvedValue({ ok: false, error: 'invalid_label' });

    const { request, context } = makePatch(
      validUuid,
      { label: '   ' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(400);
    expect(await res.json()).toEqual({ error: 'invalid_label' });
  });

  it('returns 400 invalid_date_range when wrapper rejects', async () => {
    mocks.updateEpisode.mockResolvedValue({
      ok: false,
      error: 'invalid_date_range',
    });

    const { request, context } = makePatch(
      validUuid,
      { start_date: '2026-12-01' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(400);
  });

  it('returns 400 invalid_description when wrapper rejects (>10K)', async () => {
    mocks.updateEpisode.mockResolvedValue({
      ok: false,
      error: 'invalid_description',
    });

    const { request, context } = makePatch(
      validUuid,
      { description: 'a' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(400);
  });

  it('returns 404 not_found when wrapper returns not_found', async () => {
    mocks.updateEpisode.mockResolvedValue({ ok: false, error: 'not_found' });

    const { request, context } = makePatch(
      validUuid,
      { label: 'x' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(404);
    expect(await res.json()).toEqual({ error: 'not_found' });
  });

  it('returns 502 server_error on directus_error', async () => {
    mocks.updateEpisode.mockResolvedValue({
      ok: false,
      error: 'directus_error',
    });

    const { request, context } = makePatch(
      validUuid,
      { label: 'x' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(502);
  });

  it('returns 502 server_error on network_error', async () => {
    mocks.updateEpisode.mockResolvedValue({
      ok: false,
      error: 'network_error',
    });

    const { request, context } = makePatch(
      validUuid,
      { label: 'x' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    expect(res.status).toBe(502);
  });

  it('error responses do not echo the input body back', async () => {
    mocks.updateEpisode.mockResolvedValue({ ok: false, error: 'invalid_label' });

    const { request, context } = makePatch(
      validUuid,
      { label: '<script>alert(1)</script>' },
      { cookie: 'gs_session=s-id' },
    );
    const res = await PATCH(request, context);

    const body = await res.json();
    expect(body).toEqual({ error: 'invalid_label' });
    expect(JSON.stringify(body)).not.toContain('<script>');
  });
});
