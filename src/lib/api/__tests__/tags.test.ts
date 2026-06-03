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
    deleteItem: (collection: string, id: string) => ({
      __cmd: 'deleteItem',
      collection,
      id,
    }),
  };
});

import { createOrUpsertTag, deleteTag, readAllTags, updateTag } from '../tags';

const VALID_EPISODE_ID = '550e8400-e29b-41d4-a716-446655440000';
const OTHER_EPISODE_ID = '6ba7b810-9dad-11d1-80b4-00c04fd430c8';

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
  __cmd: 'readItems' | 'createItem' | 'updateItem' | 'deleteItem';
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
  deleteItem?: (cmd: MockCmd) => unknown;
}) {
  mocks.request.mockImplementation(async (cmd: MockCmd) => {
    if (cmd.__cmd === 'readItems' && handlers.readItems) return handlers.readItems(cmd);
    if (cmd.__cmd === 'createItem' && handlers.createItem) return handlers.createItem(cmd);
    if (cmd.__cmd === 'updateItem' && handlers.updateItem) return handlers.updateItem(cmd);
    if (cmd.__cmd === 'deleteItem' && handlers.deleteItem) return handlers.deleteItem(cmd);
    throw new Error(`Unhandled mock command: ${cmd.__cmd}`);
  });
}

function existingTag(overrides: Partial<Record<string, unknown>> = {}) {
  return {
    id: 'tag-existing',
    label: 'pacing',
    category: 'mentaal',
    project_id: null,
    parent_episode_id: null,
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

// ---------------------------------------------------------------------------
// createOrUpsertTag — parent_episode_id extension (step-5, 2026-06-02)
//
// The input may optionally carry parent_episode_id. Behaviour:
//   - omitted/undefined  → existing semantics (regression-safe)
//   - null               → tag is created or upserted with parent_episode_id null
//   - UUID string        → tag is created with parent set, OR (matched_active)
//                          PATCHed to the new parent if it currently differs,
//                          OR (matched_reactivated) folded into the single
//                          reactivation PATCH alongside RESET_ON_REACTIVATE.
//   - malformed string   → returns err 'invalid_parent_episode_id' BEFORE wire.
// ---------------------------------------------------------------------------

describe('createOrUpsertTag — parent_episode_id extension', () => {
  beforeEach(() => {
    mocks.request.mockReset();
  });

  it('regression: no parent_episode_id in input → tag created with parent null', async () => {
    let capturedItem: Record<string, unknown> | undefined;
    setupMockHandlers({
      readItems: () => [],
      createItem: (cmd) => {
        capturedItem = cmd.item as Record<string, unknown>;
        return {
          id: 'tag-new',
          label: 'hoofdpijn',
          category: 'fysiek',
          project_id: null,
          parent_episode_id: null,
          usage_count: 0,
          archived_at: null,
          created_at: '2026-06-01T00:00:00.000Z',
        };
      },
    });

    const result = await createOrUpsertTag('access-token', {
      label: 'hoofdpijn',
      category: 'fysiek',
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.kind).toBe('created');
    expect(result.value.tag.parent_episode_id).toBeNull();
    // The wire body must NOT include parent_episode_id when input omits it —
    // we want to preserve the existing daily-flow contract exactly.
    expect(capturedItem).toBeDefined();
    expect(capturedItem).not.toHaveProperty('parent_episode_id');
  });

  it('creates tag with parent_episode_id set in the same POST', async () => {
    let capturedItem: Record<string, unknown> | undefined;
    setupMockHandlers({
      readItems: () => [],
      createItem: (cmd) => {
        capturedItem = cmd.item as Record<string, unknown>;
        return {
          id: 'tag-new',
          label: 'coaching sessie',
          category: 'interventie',
          project_id: null,
          parent_episode_id: VALID_EPISODE_ID,
          usage_count: 0,
          archived_at: null,
          created_at: '2026-06-02T00:00:00.000Z',
        };
      },
    });

    const result = await createOrUpsertTag('access-token', {
      label: 'coaching sessie',
      category: 'interventie',
      parent_episode_id: VALID_EPISODE_ID,
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.kind).toBe('created');
    expect(result.value.tag.parent_episode_id).toBe(VALID_EPISODE_ID);
    expect(capturedItem).toMatchObject({ parent_episode_id: VALID_EPISODE_ID });
  });

  it('matched_active + parent_episode_id differs → PATCHes parent in same branch', async () => {
    const tag = existingTag({
      label: 'pacing',
      category: 'mentaal',
      parent_episode_id: OTHER_EPISODE_ID,
    });
    let capturedPatch: Record<string, unknown> | undefined;
    setupMockHandlers({
      readItems: () => [tag],
      updateItem: (cmd) => {
        capturedPatch = cmd.patch as Record<string, unknown>;
        return { ...tag, parent_episode_id: VALID_EPISODE_ID };
      },
    });

    const result = await createOrUpsertTag('access-token', {
      label: 'pacing',
      category: 'mentaal',
      parent_episode_id: VALID_EPISODE_ID,
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.kind).toBe('matched_active');
    expect(result.value.tag.parent_episode_id).toBe(VALID_EPISODE_ID);
    expect(capturedPatch).toEqual({ parent_episode_id: VALID_EPISODE_ID });
  });

  it('matched_active + parent_episode_id already equal → no PATCH (idempotent)', async () => {
    const tag = existingTag({
      label: 'pacing',
      category: 'mentaal',
      parent_episode_id: VALID_EPISODE_ID,
    });
    const updateSpy = vi.fn();
    setupMockHandlers({
      readItems: () => [tag],
      updateItem: (cmd) => {
        updateSpy(cmd);
        return tag;
      },
    });

    const result = await createOrUpsertTag('access-token', {
      label: 'pacing',
      category: 'mentaal',
      parent_episode_id: VALID_EPISODE_ID,
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.kind).toBe('matched_active');
    expect(result.value.tag.parent_episode_id).toBe(VALID_EPISODE_ID);
    expect(updateSpy).not.toHaveBeenCalled();
  });

  it('matched_reactivated + parent_episode_id set → reactivation PATCH includes parent', async () => {
    const archived = existingTag({
      id: 'tag-archived',
      label: 'coaching',
      category: 'interventie',
      project_id: 'project-old',
      usage_count: 17,
      archived_at: '2026-04-01T00:00:00.000Z',
      parent_episode_id: null,
    });
    let capturedPatch: Record<string, unknown> | undefined;
    setupMockHandlers({
      readItems: () => [archived],
      updateItem: (cmd) => {
        capturedPatch = cmd.patch as Record<string, unknown>;
        return {
          ...archived,
          archived_at: null,
          project_id: null,
          usage_count: 0,
          parent_episode_id: VALID_EPISODE_ID,
        };
      },
    });

    const result = await createOrUpsertTag('access-token', {
      label: 'coaching',
      category: 'interventie',
      parent_episode_id: VALID_EPISODE_ID,
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.kind).toBe('matched_reactivated');
    expect(result.value.tag.parent_episode_id).toBe(VALID_EPISODE_ID);
    // Single PATCH — RESET_ON_REACTIVATE + parent_episode_id in one body.
    expect(capturedPatch).toEqual({
      archived_at: null,
      project_id: null,
      usage_count: 0,
      parent_episode_id: VALID_EPISODE_ID,
    });
  });

  it('rejects malformed parent_episode_id BEFORE any wire call', async () => {
    const result = await createOrUpsertTag('access-token', {
      label: 'pacing',
      category: 'mentaal',
      parent_episode_id: 'not-a-uuid',
    });

    expect(result).toEqual({
      ok: false,
      error: 'invalid_parent_episode_id',
    });
    expect(mocks.request).not.toHaveBeenCalled();
  });
});

// ---------------------------------------------------------------------------
// updateTag — step-5 PATCH wrapper. Handles the re-link / unlink path
// from the picker. Today's only allowed patch key is parent_episode_id;
// the wrapper rejects unknown keys defensively.
// ---------------------------------------------------------------------------

describe('updateTag', () => {
  beforeEach(() => {
    mocks.request.mockReset();
  });

  it('PATCH with parent_episode_id set returns the updated tag', async () => {
    let capturedId: string | undefined;
    let capturedPatch: Record<string, unknown> | undefined;
    setupMockHandlers({
      updateItem: (cmd) => {
        capturedId = cmd.id;
        capturedPatch = cmd.patch as Record<string, unknown>;
        return existingTag({
          id: 'tag-1',
          parent_episode_id: VALID_EPISODE_ID,
        });
      },
    });

    const result = await updateTag('access-token', 'tag-1', {
      parent_episode_id: VALID_EPISODE_ID,
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.parent_episode_id).toBe(VALID_EPISODE_ID);
    expect(capturedId).toBe('tag-1');
    expect(capturedPatch).toEqual({ parent_episode_id: VALID_EPISODE_ID });
  });

  it('PATCH with parent_episode_id: null unlinks the tag', async () => {
    setupMockHandlers({
      updateItem: () =>
        existingTag({ id: 'tag-1', parent_episode_id: null }),
    });

    const result = await updateTag('access-token', 'tag-1', {
      parent_episode_id: null,
    });

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.parent_episode_id).toBeNull();
  });

  it('rejects malformed UUID with invalid_parent_episode_id BEFORE wire (M1: per-field variant)', async () => {
    const result = await updateTag('access-token', 'tag-1', {
      parent_episode_id: 'not-a-uuid' as never,
    });

    expect(result).toEqual({ ok: false, error: 'invalid_parent_episode_id' });
    expect(mocks.request).not.toHaveBeenCalled();
  });

  it('rejects unknown patch keys with invalid_patch BEFORE wire', async () => {
    const result = await updateTag(
      'access-token',
      'tag-1',
      // @ts-expect-error — testing runtime guard against forbidden keys
      { foo: 'bar', parent_episode_id: VALID_EPISODE_ID },
    );

    expect(result).toEqual({ ok: false, error: 'invalid_patch' });
    expect(mocks.request).not.toHaveBeenCalled();
  });

  it('surfaces network errors as network_error', async () => {
    mocks.request.mockRejectedValue(new TypeError('fetch failed'));

    const result = await updateTag('access-token', 'tag-1', {
      parent_episode_id: VALID_EPISODE_ID,
    });

    expect(result).toEqual({ ok: false, error: 'network_error' });
  });

  it('surfaces other request errors as directus_error', async () => {
    mocks.request.mockRejectedValue(new Error('500 internal'));

    const result = await updateTag('access-token', 'tag-1', {
      parent_episode_id: VALID_EPISODE_ID,
    });

    expect(result).toEqual({ ok: false, error: 'directus_error' });
  });

  // -------------------------------------------------------------------------
  // Step v1.5b: extended patch surface (label + category + archived_at)
  // with per-field error variants (M1 audit fix).
  // -------------------------------------------------------------------------

  describe('extended patch surface — label / category / archived_at', () => {
    const ISO = '2026-06-03T10:00:00.000Z';

    it('PATCH with label → 200 with updated tag; wire body contains only label', async () => {
      let capturedPatch: Record<string, unknown> | undefined;
      setupMockHandlers({
        updateItem: (cmd) => {
          capturedPatch = cmd.patch as Record<string, unknown>;
          return existingTag({ id: 'tag-1', label: 'pacing-strategy' });
        },
      });

      const result = await updateTag('access-token', 'tag-1', {
        label: 'pacing-strategy',
      });

      expect(result.ok).toBe(true);
      if (!result.ok) return;
      expect(result.value.label).toBe('pacing-strategy');
      expect(capturedPatch).toEqual({ label: 'pacing-strategy' });
    });

    it('PATCH with category → 200 with updated tag', async () => {
      setupMockHandlers({
        updateItem: () => existingTag({ id: 'tag-1', category: 'fysiek' }),
      });

      const result = await updateTag('access-token', 'tag-1', {
        category: 'fysiek',
      });

      expect(result.ok).toBe(true);
      if (!result.ok) return;
      expect(result.value.category).toBe('fysiek');
    });

    it('PATCH with archived_at (ISO timestamp) → 200 with archived tag', async () => {
      setupMockHandlers({
        updateItem: () => existingTag({ id: 'tag-1', archived_at: ISO }),
      });

      const result = await updateTag('access-token', 'tag-1', {
        archived_at: ISO,
      });

      expect(result.ok).toBe(true);
      if (!result.ok) return;
      expect(result.value.archived_at).toBe(ISO);
    });

    it('PATCH with archived_at: null → 200 with un-archived tag', async () => {
      setupMockHandlers({
        updateItem: () => existingTag({ id: 'tag-1', archived_at: null }),
      });

      const result = await updateTag('access-token', 'tag-1', {
        archived_at: null,
      });

      expect(result.ok).toBe(true);
      if (!result.ok) return;
      expect(result.value.archived_at).toBeNull();
    });

    it('PATCH combining label + category + parent_episode_id → ONE wire call with all three', async () => {
      let capturedPatch: Record<string, unknown> | undefined;
      let wireCalls = 0;
      setupMockHandlers({
        updateItem: (cmd) => {
          wireCalls += 1;
          capturedPatch = cmd.patch as Record<string, unknown>;
          return existingTag({
            id: 'tag-1',
            label: 'new-label',
            category: 'fysiek',
            parent_episode_id: VALID_EPISODE_ID,
          });
        },
      });

      const result = await updateTag('access-token', 'tag-1', {
        label: 'new-label',
        category: 'fysiek',
        parent_episode_id: VALID_EPISODE_ID,
      });

      expect(result.ok).toBe(true);
      expect(wireCalls).toBe(1);
      expect(capturedPatch).toEqual({
        label: 'new-label',
        category: 'fysiek',
        parent_episode_id: VALID_EPISODE_ID,
      });
    });

    it('rejects empty label string with invalid_label BEFORE wire', async () => {
      const result = await updateTag('access-token', 'tag-1', { label: '' });

      expect(result).toEqual({ ok: false, error: 'invalid_label' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('rejects too-long label with invalid_label BEFORE wire', async () => {
      const result = await updateTag('access-token', 'tag-1', {
        label: 'a'.repeat(50),
      });

      expect(result).toEqual({ ok: false, error: 'invalid_label' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('rejects too-many-words label with invalid_label BEFORE wire', async () => {
      const result = await updateTag('access-token', 'tag-1', {
        label: 'naar de fysio',
      });

      expect(result).toEqual({ ok: false, error: 'invalid_label' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('rejects non-enum category with invalid_category BEFORE wire', async () => {
      const result = await updateTag('access-token', 'tag-1', {
        category: 'made-up' as never,
      });

      expect(result).toEqual({ ok: false, error: 'invalid_category' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('rejects malformed archived_at with invalid_archived_at BEFORE wire', async () => {
      const result = await updateTag('access-token', 'tag-1', {
        archived_at: 'yesterday' as never,
      });

      expect(result).toEqual({ ok: false, error: 'invalid_archived_at' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('rejects empty patch with invalid_patch (shape-level)', async () => {
      const result = await updateTag('access-token', 'tag-1', {});

      expect(result).toEqual({ ok: false, error: 'invalid_patch' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('regression: existing parent_episode_id-only patches still work', async () => {
      setupMockHandlers({
        updateItem: () =>
          existingTag({ id: 'tag-1', parent_episode_id: VALID_EPISODE_ID }),
      });

      const result = await updateTag('access-token', 'tag-1', {
        parent_episode_id: VALID_EPISODE_ID,
      });

      expect(result.ok).toBe(true);
    });
  });
});

// ---------------------------------------------------------------------------
// deleteTag — step v1.5b hard-delete wrapper. Does NOT itself check
// usage_count — that gate lives in the route handler (read-then-delete).
// ---------------------------------------------------------------------------

describe('deleteTag', () => {
  beforeEach(() => {
    mocks.request.mockReset();
  });

  it('happy path → returns ok with deleted_id', async () => {
    setupMockHandlers({
      deleteItem: () => undefined,
    });

    const result = await deleteTag('access-token', 'tag-1');

    expect(result).toEqual({ ok: true, value: { deleted_id: 'tag-1' } });
  });

  it('surfaces network errors as network_error', async () => {
    mocks.request.mockRejectedValue(new TypeError('fetch failed'));

    const result = await deleteTag('access-token', 'tag-1');

    expect(result).toEqual({ ok: false, error: 'network_error' });
  });

  it('surfaces other request errors as directus_error', async () => {
    mocks.request.mockRejectedValue(new Error('404 not found'));

    const result = await deleteTag('access-token', 'tag-1');

    expect(result).toEqual({ ok: false, error: 'directus_error' });
  });
});
