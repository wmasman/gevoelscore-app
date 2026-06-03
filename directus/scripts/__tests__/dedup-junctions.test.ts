import { describe, expect, it, vi } from 'vitest';
// @ts-expect-error — .mjs lib without type declarations is intentional.
import { dedupJunctions } from '../lib/audit-junctions.mjs';

type JunctionRow = {
  id: string;
  day_entries_id: string;
  tags_id: string;
};

function makeRequest(initialRows: JunctionRow[]) {
  const deletedIds: string[] = [];
  const request = vi.fn(async (endpoint: string, method = 'GET', body?: unknown) => {
    if (method === 'GET' && endpoint.startsWith('/items/day_entries_tags')) {
      return { data: initialRows };
    }
    if (method === 'DELETE' && endpoint.startsWith('/items/day_entries_tags')) {
      // Directus bulk delete: DELETE /items/<col> with body = [ids]
      const ids = Array.isArray(body) ? (body as string[]) : [];
      deletedIds.push(...ids);
      return { success: true };
    }
    return { data: [] };
  });
  return { request, deletedIds };
}

describe('dedup-junctions', () => {
  it('given no duplicates, when run, then no SDK delete calls are made and recomputeTagUsage is not called', async () => {
    const { request, deletedIds } = makeRequest([
      { id: 'j-1', day_entries_id: 'd-1', tags_id: 't-a' },
      { id: 'j-2', day_entries_id: 'd-2', tags_id: 't-a' },
    ]);
    const recomputeTagUsage = vi.fn(async () => {});

    const result = await dedupJunctions({
      directusRequest: request,
      recomputeTagUsage,
      collection: 'day_entries_tags',
      commit: true,
    });

    expect(deletedIds).toEqual([]);
    expect(recomputeTagUsage).not.toHaveBeenCalled();
    expect(result.deleted).toEqual([]);
    expect(result.affectedTagIds).toEqual([]);
  });

  it('given one duplicate group of 3 rows on the same (day, tag), when committed, then deletes the two non-lowest-id rows and keeps the lowest', async () => {
    const { request, deletedIds } = makeRequest([
      { id: 'j-uuid-c', day_entries_id: 'd-1', tags_id: 't-a' },
      { id: 'j-uuid-a', day_entries_id: 'd-1', tags_id: 't-a' }, // lex-lowest → keeper
      { id: 'j-uuid-b', day_entries_id: 'd-1', tags_id: 't-a' },
    ]);
    const recomputeTagUsage = vi.fn(async () => {});

    const result = await dedupJunctions({
      directusRequest: request,
      recomputeTagUsage,
      collection: 'day_entries_tags',
      commit: true,
    });

    expect(result.kept).toEqual(['j-uuid-a']);
    expect(result.deleted.sort()).toEqual(['j-uuid-b', 'j-uuid-c']);
    expect(deletedIds.sort()).toEqual(['j-uuid-b', 'j-uuid-c']);
  });

  it('given duplicates and commit: false, when run, then NO delete calls are issued and the result still reports the plan', async () => {
    const { request, deletedIds } = makeRequest([
      { id: 'j-uuid-b', day_entries_id: 'd-1', tags_id: 't-a' },
      { id: 'j-uuid-a', day_entries_id: 'd-1', tags_id: 't-a' },
    ]);
    const recomputeTagUsage = vi.fn(async () => {});

    const result = await dedupJunctions({
      directusRequest: request,
      recomputeTagUsage,
      collection: 'day_entries_tags',
      commit: false,
    });

    expect(deletedIds).toEqual([]);
    expect(recomputeTagUsage).not.toHaveBeenCalled();
    expect(result.kept).toEqual(['j-uuid-a']);
    expect(result.deleted).toEqual(['j-uuid-b']);
  });

  it('given duplicates and commit: true, when run, then recomputeTagUsage is called with the affected tag ids after deletions complete', async () => {
    const { request } = makeRequest([
      { id: 'j-uuid-c', day_entries_id: 'd-1', tags_id: 't-a' },
      { id: 'j-uuid-a', day_entries_id: 'd-1', tags_id: 't-a' },
      { id: 'j-uuid-d', day_entries_id: 'd-2', tags_id: 't-b' },
      { id: 'j-uuid-b', day_entries_id: 'd-2', tags_id: 't-b' },
    ]);
    const recomputeTagUsage = vi.fn(async () => {});

    await dedupJunctions({
      directusRequest: request,
      recomputeTagUsage,
      collection: 'day_entries_tags',
      commit: true,
    });

    expect(recomputeTagUsage).toHaveBeenCalledTimes(1);
    const calledWith = recomputeTagUsage.mock.calls[0]![0];
    expect((calledWith as string[]).sort()).toEqual(['t-a', 't-b']);
  });
});
