import { describe, expect, it, vi } from 'vitest';
// @ts-expect-error — .mjs lib without type declarations is intentional;
// the audit lib is a pure-JS helper and tests assert its runtime shape.
import { findDuplicateJunctions } from '../lib/audit-junctions.mjs';

type JunctionRow = {
  id: string;
  day_entries_id?: string;
  project_entries_id?: string;
  tags_id: string;
};

function makeRequest(rowsByCollection: Record<string, JunctionRow[]>) {
  return vi.fn(async (endpoint: string) => {
    for (const [collection, rows] of Object.entries(rowsByCollection)) {
      if (endpoint.startsWith(`/items/${collection}`)) {
        return { data: rows };
      }
    }
    return { data: [] };
  });
}

describe('audit-junctions', () => {
  describe('findDuplicateJunctions', () => {
    it('given a junction with no duplicates, when audited, then returns dupGroups: 0 and extraRows: 0', async () => {
      const directusRequest = makeRequest({
        day_entries_tags: [
          { id: 'j-1', day_entries_id: 'd-1', tags_id: 't-a' },
          { id: 'j-2', day_entries_id: 'd-1', tags_id: 't-b' },
          { id: 'j-3', day_entries_id: 'd-2', tags_id: 't-a' },
        ],
      });

      const result = await findDuplicateJunctions(
        directusRequest,
        'day_entries_tags',
      );

      expect(result).toEqual({
        collection: 'day_entries_tags',
        dupGroups: 0,
        extraRows: 0,
        samples: [],
      });
    });

    it('given a junction with one duplicate group of 3 rows on the same pair, when audited, then returns dupGroups: 1, extraRows: 2, and a sample with count 3', async () => {
      const directusRequest = makeRequest({
        day_entries_tags: [
          { id: 'j-1', day_entries_id: 'd-1', tags_id: 't-a' },
          { id: 'j-2', day_entries_id: 'd-1', tags_id: 't-a' }, // dup
          { id: 'j-3', day_entries_id: 'd-1', tags_id: 't-a' }, // dup
          { id: 'j-4', day_entries_id: 'd-2', tags_id: 't-b' },
        ],
      });

      const result = await findDuplicateJunctions(
        directusRequest,
        'day_entries_tags',
      );

      expect(result.dupGroups).toBe(1);
      expect(result.extraRows).toBe(2);
      expect(result.samples).toEqual([
        { day_entries_id: 'd-1', tags_id: 't-a', count: 3 },
      ]);
    });

    it('given the project_entries_tags collection, when audited, then uses project_entries_id as the first FK and returns the same shape', async () => {
      const directusRequest = makeRequest({
        project_entries_tags: [
          { id: 'pj-1', project_entries_id: 'p-1', tags_id: 't-a' },
          { id: 'pj-2', project_entries_id: 'p-1', tags_id: 't-a' }, // dup
        ],
      });

      const result = await findDuplicateJunctions(
        directusRequest,
        'project_entries_tags',
      );

      expect(result.collection).toBe('project_entries_tags');
      expect(result.dupGroups).toBe(1);
      expect(result.extraRows).toBe(1);
      expect(result.samples).toEqual([
        { project_entries_id: 'p-1', tags_id: 't-a', count: 2 },
      ]);
    });
  });
});
