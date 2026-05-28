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
  };
});

import { readAllTags } from '../tags';

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
