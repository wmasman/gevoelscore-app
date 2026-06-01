import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  request: vi.fn(),
}));

vi.mock('@directus/sdk', () => {
  const client = {
    with: () => client,
    request: mocks.request,
  };
  return {
    createDirectus: () => client,
    rest: () => null,
    staticToken: () => null,
    readItems: (collection: string, query: unknown) => ({
      __cmd: 'readItems',
      collection,
      query,
    }),
    createItem: (collection: string, item: unknown) => ({
      __cmd: 'createItem',
      collection,
      item,
    }),
    updateItem: (collection: string, id: string, patch: unknown) => ({
      __cmd: 'updateItem',
      collection,
      id,
      patch,
    }),
  };
});

import { createOrUpsertTag, readAllTags } from '../tags';

describe('tags SDK wrapper', () => {
  beforeEach(() => {
    mocks.request.mockReset();
  });

  it('returns active tags from the tags collection', async () => {
    mocks.request.mockResolvedValue([
      {
        id: 'tag-1',
        label: 'helder',
        category: 'mentaal',
        project_id: null,
        usage_count: 3,
        archived_at: null,
        created_at: '2026-01-01T00:00:00.000Z',
      },
      {
        id: 'tag-2',
        label: 'moe',
        category: 'fysiek',
        project_id: null,
        usage_count: 1,
        archived_at: null,
        created_at: '2026-01-02T00:00:00.000Z',
      },
    ]);

    const result = await readAllTags('access-token');

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value).toHaveLength(2);
    expect(result.value[0]!.id).toBe('tag-1');
    expect(result.value[0]!.label).toBe('helder');
    expect(result.value[1]!.category).toBe('fysiek');
  });

  it('maps a fetch TypeError to network_error', async () => {
    mocks.request.mockRejectedValue(new TypeError('fetch failed'));

    const result = await readAllTags('access-token');

    expect(result).toEqual({ ok: false, error: 'network_error' });
  });
});

// ---------------------------------------------------------------------------
// createOrUpsertTag — added 2026-06-01 for inline tag creation feature
// (see docs/features/inline-tag-creation/step-1-inline-tag-creation.md)
// ---------------------------------------------------------------------------

type MockCmd = {
  __cmd: 'readItems' | 'createItem' | 'updateItem';
  collection?: string;
  query?: unknown;
  item?: unknown;
  id?: string;
  patch?: unknown;
};

function setupMockHandlers(handlers: {
  readItems?: (cmd: MockCmd) => unknown;
  createItem?: (cmd: MockCmd) => unknown;
  updateItem?: (cmd: MockCmd) => unknown;
}) {
  mocks.request.mockImplementation(async (cmd: MockCmd) => {
    if (cmd.__cmd === 'readItems' && handlers.readItems) return handlers.readItems(cmd);
    if (cmd.__cmd === 'createItem' && handlers.createItem) return handlers.createItem(cmd);
    if (cmd.__cmd === 'updateItem' && handlers.updateItem) return handlers.updateItem(cmd);
    throw new Error(`Unhandled mock command: ${cmd.__cmd}`);
  });
}

function existingTag(overrides: Partial<Record<string, unknown>> = {}) {
  return {
    id: 'tag-existing',
    label: 'pacing',
    category: 'mentaal',
    project_id: null,
    usage_count: 5,
    archived_at: null,
    created_at: '2026-01-01T00:00:00.000Z',
    ...overrides,
  };
}

describe('createOrUpsertTag', () => {
  beforeEach(() => {
    mocks.request.mockReset();
  });

  it('creates a new tag when no match exists', async () => {
    setupMockHandlers({
      readItems: () => [],
      createItem: (cmd) => ({
        id: 'tag-new',
        label: (cmd.item as { label: string }).label,
        category: (cmd.item as { category: string }).category,
        project_id: null,
        usage_count: 0,
        archived_at: null,
        created_at: '2026-06-01T00:00:00.000Z',
      }),
    });

    const result = await createOrUpsertTag('access-token', {
      label: 'hoofdpijn',
      category: 'fysiek',
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.kind).toBe('created');
    expect(result.value.tag.label).toBe('hoofdpijn');
    expect(result.value.tag.category).toBe('fysiek');
  });

  it('trims whitespace before dedup comparison', async () => {
    const tag = existingTag({ label: 'pacing', category: 'mentaal' });
    setupMockHandlers({ readItems: () => [tag] });

    const result = await createOrUpsertTag('access-token', {
      label: '  pacing  ',
      category: 'mentaal',
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.kind).toBe('matched_active');
    expect(result.value.tag.id).toBe('tag-existing');
  });

  it('matches case-insensitively within category via _icontains + JS exact-match post-filter', async () => {
    // Directus has no _iequals operator (confirmed against official docs +
    // programmeerprobeer reference 2026-06-01). The query uses _icontains
    // as a coarse case-insensitive filter; the lib then post-filters in JS
    // for exact equality on the lowercased trimmed label.
    const tag = existingTag({ label: 'pacing', category: 'mentaal' });
    let capturedQuery: unknown;
    setupMockHandlers({
      readItems: (cmd) => {
        capturedQuery = cmd.query;
        return [tag];
      },
    });

    const result = await createOrUpsertTag('access-token', {
      label: 'PACING',
      category: 'mentaal',
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.kind).toBe('matched_active');
    const filter = (capturedQuery as { filter?: { label?: Record<string, unknown> } })
      .filter?.label;
    expect(filter).toEqual({ _icontains: 'PACING' });
  });

  it('post-filters _icontains false positives (substring matches that are not exact)', async () => {
    // _icontains matches substrings, so a query for "pacing" can return
    // rows like "rapid-pacing". The JS post-filter must reject these.
    const falsePositive = existingTag({
      id: 'tag-pacing-strategy',
      label: 'pacing-strategy',
      category: 'mentaal',
    });
    setupMockHandlers({
      readItems: () => [falsePositive],
      createItem: () => ({
        id: 'tag-new',
        label: 'pacing',
        category: 'mentaal',
        project_id: null,
        usage_count: 0,
        archived_at: null,
        created_at: '2026-06-01T00:00:00.000Z',
      }),
    });

    const result = await createOrUpsertTag('access-token', {
      label: 'pacing',
      category: 'mentaal',
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    // No exact match -> a fresh tag is created, not the substring match.
    expect(result.value.kind).toBe('created');
    expect(result.value.tag.id).toBe('tag-new');
  });

  it('does NOT match across categories', async () => {
    // No row found when filtering category=custom (the existing 'pacing' is mentaal).
    setupMockHandlers({
      readItems: () => [],
      createItem: () => ({
        id: 'tag-new',
        label: 'pacing',
        category: 'custom',
        project_id: null,
        usage_count: 0,
        archived_at: null,
        created_at: '2026-06-01T00:00:00.000Z',
      }),
    });

    const result = await createOrUpsertTag('access-token', {
      label: 'pacing',
      category: 'custom',
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.kind).toBe('created');
    expect(result.value.tag.category).toBe('custom');
  });

  it('reactivates an archived tag and clears stale project_id + usage_count', async () => {
    const archived = existingTag({
      id: 'tag-archived',
      label: 'coaching',
      category: 'interventie',
      project_id: 'project-old',
      usage_count: 17,
      archived_at: '2026-04-01T00:00:00.000Z',
    });
    let capturedPatch: unknown;
    setupMockHandlers({
      readItems: () => [archived],
      updateItem: (cmd) => {
        capturedPatch = cmd.patch;
        return {
          ...archived,
          archived_at: null,
          project_id: null,
          usage_count: 0,
        };
      },
    });

    const result = await createOrUpsertTag('access-token', {
      label: 'coaching',
      category: 'interventie',
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.kind).toBe('matched_reactivated');
    expect(result.value.tag.id).toBe('tag-archived');
    expect(result.value.tag.archived_at).toBeNull();
    expect(result.value.tag.project_id).toBeNull();
    expect(result.value.tag.usage_count).toBe(0);
    expect(capturedPatch).toEqual({
      archived_at: null,
      project_id: null,
      usage_count: 0,
    });
  });

  it('rejects empty / whitespace-only label with invalid_label', async () => {
    const result = await createOrUpsertTag('access-token', {
      label: '   ',
      category: 'mentaal',
    });

    expect(result).toEqual({ ok: false, error: 'invalid_label' });
    expect(mocks.request).not.toHaveBeenCalled();
  });

  it('rejects too-long label with invalid_label', async () => {
    const result = await createOrUpsertTag('access-token', {
      label: 'a'.repeat(50),
      category: 'mentaal',
    });

    expect(result).toEqual({ ok: false, error: 'invalid_label' });
    expect(mocks.request).not.toHaveBeenCalled();
  });

  it('rejects too-many-words label with invalid_label', async () => {
    const result = await createOrUpsertTag('access-token', {
      label: 'naar de fysio',
      category: 'interventie',
    });

    expect(result).toEqual({ ok: false, error: 'invalid_label' });
    expect(mocks.request).not.toHaveBeenCalled();
  });

  it('rejects invalid category with invalid_category', async () => {
    const result = await createOrUpsertTag('access-token', {
      label: 'pacing',
      // @ts-expect-error — testing runtime guard against non-enum value
      category: 'not-a-real-category',
    });

    expect(result).toEqual({ ok: false, error: 'invalid_category' });
    expect(mocks.request).not.toHaveBeenCalled();
  });

  it('surfaces network errors as network_error', async () => {
    mocks.request.mockRejectedValue(new TypeError('fetch failed'));

    const result = await createOrUpsertTag('access-token', {
      label: 'pacing',
      category: 'mentaal',
    });

    expect(result).toEqual({ ok: false, error: 'network_error' });
  });

  it('surfaces other request errors as directus_error', async () => {
    mocks.request.mockRejectedValue(new Error('500 internal'));

    const result = await createOrUpsertTag('access-token', {
      label: 'pacing',
      category: 'mentaal',
    });

    expect(result).toEqual({ ok: false, error: 'directus_error' });
  });

  // TOCTOU race: two simultaneous calls with the same (category, label) and
  // no existing row may both find empty and both POST -> two rows. This
  // documents the known limit (see M1 in step-1 audit + audits/OPEN.md
  // follow-up for the DB-level unique index that closes the window).
  it('does not crash on concurrent calls (TOCTOU known limit, see audits/OPEN.md)', async () => {
    let createCount = 0;
    setupMockHandlers({
      readItems: () => [],
      createItem: () => {
        createCount += 1;
        return {
          id: `tag-${createCount}`,
          label: 'pacing',
          category: 'mentaal',
          project_id: null,
          usage_count: 0,
          archived_at: null,
          created_at: '2026-06-01T00:00:00.000Z',
        };
      },
    });

    const [a, b] = await Promise.all([
      createOrUpsertTag('t', { label: 'pacing', category: 'mentaal' }),
      createOrUpsertTag('t', { label: 'pacing', category: 'mentaal' }),
    ]);

    expect(a.ok).toBe(true);
    expect(b.ok).toBe(true);
    // Both calls succeed; this is the documented race. The fix is a DB-
    // level unique index (tracked in audits/OPEN.md).
    expect(createCount).toBeLessThanOrEqual(2);
  });
});
