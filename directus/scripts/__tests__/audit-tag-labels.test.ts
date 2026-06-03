import { describe, expect, it, vi } from 'vitest';
// @ts-expect-error — .mjs lib without type declarations is intentional.
import { findDuplicateTagLabels } from '../lib/audit-tag-labels.mjs';

type TagRow = {
  id: string;
  label: string;
  category: string;
  archived_at: string | null;
};

function makeRequest(rowsByCollection: Record<string, TagRow[]>) {
  return vi.fn(async (endpoint: string) => {
    for (const [collection, rows] of Object.entries(rowsByCollection)) {
      if (endpoint.startsWith(`/items/${collection}`)) {
        return { data: rows };
      }
    }
    return { data: [] };
  });
}

describe('audit-tag-labels', () => {
  describe('findDuplicateTagLabels', () => {
    it('given tags with no label duplicates, when audited, then returns dupGroups: 0', async () => {
      const directusRequest = makeRequest({
        tags: [
          { id: 't-1', label: 'hoofdpijn', category: 'fysiek', archived_at: null },
          { id: 't-2', label: 'moe',       category: 'fysiek', archived_at: null },
          { id: 't-3', label: 'hoofdpijn', category: 'mentaal', archived_at: null },
          // same label in DIFFERENT category — NOT a duplicate
        ],
      });

      const result = await findDuplicateTagLabels(directusRequest, 'tags');

      expect(result).toEqual({
        collection: 'tags',
        dupGroups: 0,
        extraRows: 0,
        samples: [],
      });
    });

    it('given two tags with case-different labels in the same category, when audited, then returns one dup group (case-insensitive grouping)', async () => {
      const directusRequest = makeRequest({
        tags: [
          { id: 't-1', label: 'Hoofdpijn', category: 'fysiek', archived_at: null },
          { id: 't-2', label: 'hoofdpijn', category: 'fysiek', archived_at: null },
        ],
      });

      const result = await findDuplicateTagLabels(directusRequest, 'tags');

      expect(result.dupGroups).toBe(1);
      expect(result.extraRows).toBe(1);
      expect(result.samples).toEqual([
        { label: 'hoofdpijn', category: 'fysiek', count: 2 },
      ]);
    });

    it('given an archived tag with the same lowered-label as a live tag, when audited, then the pair is NOT counted as a duplicate', async () => {
      const directusRequest = makeRequest({
        tags: [
          { id: 't-1', label: 'hoofdpijn', category: 'fysiek', archived_at: null },
          { id: 't-2', label: 'hoofdpijn', category: 'fysiek', archived_at: '2026-05-01T00:00:00Z' },
        ],
      });

      const result = await findDuplicateTagLabels(directusRequest, 'tags');

      expect(result.dupGroups).toBe(0);
    });
  });
});
