import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  readAllEpisodes: vi.fn(),
  createEpisode: vi.fn(),
  getValidatedSession: vi.fn(),
  readCheck: vi.fn(),
  writeCheck: vi.fn(),
}));

vi.mock('@/lib/api/episodes', () => ({
  readAllEpisodes: mocks.readAllEpisodes,
  createEpisode: mocks.createEpisode,
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
    episodeReadRateLimiter: {
      check: mocks.readCheck,
      sweep: () => undefined,
    },
    episodeWriteRateLimiter: {
      check: mocks.writeCheck,
      sweep: () => undefined,
    },
  };
});

import { GET, POST } from '../route';

const happyEpisode = {
  id: 'ep_01HQ5XYZ',
  label: 'Coaching met Sarah',
  category: 'interventie' as const,
  start_date: '2026-04-01',
  end_date: null,
  description: null,
  calendar_binding: null,
  archived_at: null,
  created_at: '2026-04-01T08:00:00.000Z',
  updated_at: '2026-04-01T08:00:00.000Z',
};

function makeGet(
  query: { archived?: string } = {},
  opts: { cookie?: string; origin?: string } = {},
): Request {
  const url = new URL('http://localhost:3000/api/episodes');
  if (query.archived !== undefined) url.searchParams.set('archived', query.archived);
  const headers: Record<string, string> = {
    origin: opts.origin ?? 'http://localhost:3000',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  return new Request(url, { method: 'GET', headers });
}

function makePost(
  body: unknown,
  opts: { cookie?: string; origin?: string } = {},
): Request {
  const headers: Record<string, string> = {
    origin: opts.origin ?? 'http://localhost:3000',
    'content-type': 'application/json',
  };
  if (opts.cookie !== undefined) headers.cookie = opts.cookie;
  return new Request('http://localhost:3000/api/episodes', {
    method: 'POST',
    headers,
    body: typeof body === 'string' ? body : JSON.stringify(body),
  });
}

beforeEach(() => {
  mocks.readAllEpisodes.mockReset();
  mocks.createEpisode.mockReset();
  mocks.getValidatedSession.mockReset();
  mocks.readCheck.mockReset();
  mocks.writeCheck.mockReset();
  mocks.getValidatedSession.mockResolvedValue({
    accessToken: 'at-1',
    refreshToken: 'rt-1',
    expiresAt: Date.now() + 60_000,
  });
  mocks.readCheck.mockReturnValue({ allowed: true });
  mocks.writeCheck.mockReturnValue({ allowed: true });
});

// ===========================================================================
// GET /api/episodes
// ===========================================================================

describe('GET /api/episodes', () => {
  it('returns 200 with empty list when wrapper returns []', async () => {
    mocks.readAllEpisodes.mockResolvedValue({ ok: true, value: [] });

    const res = await GET(makeGet({}, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ episodes: [] });
  });

  it('returns 200 with the episodes when wrapper returns rows', async () => {
    mocks.readAllEpisodes.mockResolvedValue({ ok: true, value: [happyEpisode] });

    const res = await GET(makeGet({}, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.episodes).toHaveLength(1);
    expect(body.episodes[0].id).toBe('ep_01HQ5XYZ');
  });

  it('default call passes includeArchived: false to the wrapper', async () => {
    mocks.readAllEpisodes.mockResolvedValue({ ok: true, value: [] });

    await GET(makeGet({}, { cookie: 'gs_session=s-id' }));

    expect(mocks.readAllEpisodes).toHaveBeenCalledWith('at-1', { includeArchived: false });
  });

  it('?archived=all passes includeArchived: true to the wrapper', async () => {
    mocks.readAllEpisodes.mockResolvedValue({ ok: true, value: [] });

    await GET(makeGet({ archived: 'all' }, { cookie: 'gs_session=s-id' }));

    expect(mocks.readAllEpisodes).toHaveBeenCalledWith('at-1', { includeArchived: true });
  });

  it('returns 400 invalid_request when ?archived has any other value', async () => {
    const res = await GET(
      makeGet({ archived: 'true' }, { cookie: 'gs_session=s-id' }),
    );

    expect(res.status).toBe(400);
    expect(mocks.readAllEpisodes).not.toHaveBeenCalled();
  });

  it('returns 403 forbidden on cross-origin', async () => {
    const res = await GET(
      makeGet({}, { cookie: 'gs_session=s-id', origin: 'https://evil.example.com' }),
    );

    expect(res.status).toBe(403);
    expect(mocks.readAllEpisodes).not.toHaveBeenCalled();
  });

  it('returns 429 when read rate-limit denies', async () => {
    mocks.readCheck.mockReturnValue({ allowed: false, retryAfterMs: 12_345 });

    const res = await GET(makeGet({}, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(429);
    const body = await res.json();
    expect(body.error).toBe('rate_limited');
    expect(body.retry_after_ms).toBe(12_345);
  });

  it('returns 401 when no session cookie', async () => {
    const res = await GET(makeGet());

    expect(res.status).toBe(401);
    expect(mocks.readAllEpisodes).not.toHaveBeenCalled();
  });

  it('returns 401 when session resolves to null', async () => {
    mocks.getValidatedSession.mockResolvedValue(null);

    const res = await GET(makeGet({}, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(401);
    expect(mocks.readAllEpisodes).not.toHaveBeenCalled();
  });

  it('returns 502 server_error when wrapper returns directus_error', async () => {
    mocks.readAllEpisodes.mockResolvedValue({ ok: false, error: 'directus_error' });

    const res = await GET(makeGet({}, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(502);
  });

  it('returns 502 server_error when wrapper returns network_error', async () => {
    mocks.readAllEpisodes.mockResolvedValue({ ok: false, error: 'network_error' });

    const res = await GET(makeGet({}, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(502);
  });
});

// ===========================================================================
// POST /api/episodes
// ===========================================================================

describe('POST /api/episodes', () => {
  const validBody = {
    label: 'Coaching met Sarah',
    category: 'interventie',
    start_date: '2026-04-01',
  };

  it('returns 200 with { episode } on valid body', async () => {
    mocks.createEpisode.mockResolvedValue({ ok: true, value: happyEpisode });

    const res = await POST(makePost(validBody, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.episode.id).toBe('ep_01HQ5XYZ');
  });

  it('forwards label/category/start_date/end_date/description to the wrapper', async () => {
    mocks.createEpisode.mockResolvedValue({ ok: true, value: happyEpisode });

    await POST(
      makePost(
        {
          label: 'Citalopram afbouw',
          category: 'interventie',
          start_date: '2026-04-01',
          end_date: '2026-06-01',
          description: 'wekelijks',
        },
        { cookie: 'gs_session=s-id' },
      ),
    );

    expect(mocks.createEpisode).toHaveBeenCalledWith('at-1', {
      label: 'Citalopram afbouw',
      category: 'interventie',
      start_date: '2026-04-01',
      end_date: '2026-06-01',
      description: 'wekelijks',
    });
  });

  it('returns 403 forbidden on cross-origin', async () => {
    const res = await POST(
      makePost(validBody, {
        cookie: 'gs_session=s-id',
        origin: 'https://evil.example.com',
      }),
    );

    expect(res.status).toBe(403);
    expect(mocks.createEpisode).not.toHaveBeenCalled();
  });

  it('returns 429 when write rate-limit denies', async () => {
    mocks.writeCheck.mockReturnValue({ allowed: false, retryAfterMs: 99 });

    const res = await POST(makePost(validBody, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(429);
  });

  it('returns 401 when no session cookie', async () => {
    const res = await POST(makePost(validBody));

    expect(res.status).toBe(401);
  });

  it('returns 400 malformed_body on non-JSON body', async () => {
    const res = await POST(makePost('not-json-{', { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(400);
    expect(mocks.createEpisode).not.toHaveBeenCalled();
  });

  it('returns 400 malformed_body when label is missing', async () => {
    const res = await POST(
      makePost({ category: 'interventie', start_date: '2026-04-01' }, { cookie: 'gs_session=s-id' }),
    );

    expect(res.status).toBe(400);
    expect(mocks.createEpisode).not.toHaveBeenCalled();
  });

  it('returns 400 malformed_body when category is missing', async () => {
    const res = await POST(
      makePost({ label: 'x', start_date: '2026-04-01' }, { cookie: 'gs_session=s-id' }),
    );

    expect(res.status).toBe(400);
  });

  it('returns 400 malformed_body when start_date is missing', async () => {
    const res = await POST(
      makePost({ label: 'x', category: 'interventie' }, { cookie: 'gs_session=s-id' }),
    );

    expect(res.status).toBe(400);
  });

  it('returns 400 invalid_label when wrapper rejects label', async () => {
    mocks.createEpisode.mockResolvedValue({ ok: false, error: 'invalid_label' });

    const res = await POST(makePost(validBody, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(400);
    expect(await res.json()).toEqual({ error: 'invalid_label' });
  });

  it('returns 400 invalid_category when wrapper rejects category', async () => {
    mocks.createEpisode.mockResolvedValue({ ok: false, error: 'invalid_category' });

    const res = await POST(makePost(validBody, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(400);
    expect(await res.json()).toEqual({ error: 'invalid_category' });
  });

  it('returns 400 invalid_date_range when wrapper rejects range', async () => {
    mocks.createEpisode.mockResolvedValue({ ok: false, error: 'invalid_date_range' });

    const res = await POST(makePost(validBody, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(400);
    expect(await res.json()).toEqual({ error: 'invalid_date_range' });
  });

  it('returns 400 invalid_description when wrapper rejects description (>10K)', async () => {
    mocks.createEpisode.mockResolvedValue({ ok: false, error: 'invalid_description' });

    const res = await POST(makePost(validBody, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(400);
    expect(await res.json()).toEqual({ error: 'invalid_description' });
  });

  it('returns 502 server_error on directus_error', async () => {
    mocks.createEpisode.mockResolvedValue({ ok: false, error: 'directus_error' });

    const res = await POST(makePost(validBody, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(502);
  });

  it('returns 502 server_error on network_error', async () => {
    mocks.createEpisode.mockResolvedValue({ ok: false, error: 'network_error' });

    const res = await POST(makePost(validBody, { cookie: 'gs_session=s-id' }));

    expect(res.status).toBe(502);
  });

  it('error responses do not echo the input body back', async () => {
    // Defense-in-depth per .claude/security-checklist.md A04.
    mocks.createEpisode.mockResolvedValue({ ok: false, error: 'invalid_label' });

    const res = await POST(
      makePost(
        { label: '<script>alert(1)</script>', category: 'interventie', start_date: '2026-04-01' },
        { cookie: 'gs_session=s-id' },
      ),
    );

    const body = await res.json();
    expect(body).toEqual({ error: 'invalid_label' });
    // The error response carries ONLY the error variant — nothing reflects
    // the input back.
    expect(JSON.stringify(body)).not.toContain('<script>');
    expect(JSON.stringify(body)).not.toContain('alert');
  });
});
