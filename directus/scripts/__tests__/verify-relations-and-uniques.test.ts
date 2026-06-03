import { describe, expect, it, vi } from 'vitest';
// @ts-expect-error — .mjs lib without type declarations is intentional.
import {
  verifyCheckConstraints,
  verifyRelations,
  verifyUniqueIndexes,
} from '../lib/verify-relations-and-uniques.mjs';

type RelationDoc = {
  data: {
    collection: string;
    field: string;
    related_collection: string;
    schema: { on_delete: string; on_update?: string } | null;
  };
};

function makeRelationsRequest(
  relations: Record<string, RelationDoc['data']>,
) {
  return vi.fn(async (endpoint: string) => {
    const m = endpoint.match(/^\/relations\/([^/]+)\/([^/]+)$/);
    if (!m) throw new Error(`unexpected endpoint: ${endpoint}`);
    const key = `${m[1]}.${m[2]}`;
    const relation = relations[key];
    if (!relation) {
      throw new Error(`HTTP 404 on GET ${endpoint}\nrelation not found`);
    }
    return { data: relation };
  });
}

describe('verify-relations-and-uniques', () => {
  describe('verifyRelations', () => {
    it('given a relation whose actual on_delete matches the expected value, when verified, then records a pass and no failures', async () => {
      const directusRequest = makeRelationsRequest({
        'day_entries_tags.day_entries_id': {
          collection: 'day_entries_tags',
          field: 'day_entries_id',
          related_collection: 'day_entries',
          schema: { on_delete: 'CASCADE' },
        },
      });

      const result = await verifyRelations(directusRequest, [
        {
          collection: 'day_entries_tags',
          field: 'day_entries_id',
          related_collection: 'day_entries',
          on_delete: 'CASCADE',
        },
      ]);

      expect(result.passes).toEqual(['day_entries_tags.day_entries_id']);
      expect(result.failures).toEqual([]);
    });

    it('given a relation whose on_delete is wrong, when verified, then records a failure with the expected vs actual diff', async () => {
      const directusRequest = makeRelationsRequest({
        'tags.parent_id': {
          collection: 'tags',
          field: 'parent_id',
          related_collection: 'tags',
          schema: { on_delete: 'CASCADE' }, // expected SET NULL
        },
      });

      const result = await verifyRelations(directusRequest, [
        {
          collection: 'tags',
          field: 'parent_id',
          related_collection: 'tags',
          on_delete: 'SET NULL',
        },
      ]);

      expect(result.passes).toEqual([]);
      expect(result.failures).toHaveLength(1);
      expect(result.failures[0].name).toBe('tags.parent_id');
      expect(result.failures[0].issues.join(' ')).toMatch(/on_delete.*SET NULL.*CASCADE/);
    });

    it('given a relation whose related_collection is wrong, when verified, then records a failure', async () => {
      const directusRequest = makeRelationsRequest({
        'tags.parent_episode_id': {
          collection: 'tags',
          field: 'parent_episode_id',
          related_collection: 'tags', // expected 'episodes'
          schema: { on_delete: 'SET NULL' },
        },
      });

      const result = await verifyRelations(directusRequest, [
        {
          collection: 'tags',
          field: 'parent_episode_id',
          related_collection: 'episodes',
          on_delete: 'SET NULL',
        },
      ]);

      expect(result.failures).toHaveLength(1);
      expect(result.failures[0].issues.join(' ')).toMatch(/related_collection.*episodes.*tags/);
    });
  });

  describe('verifyUniqueIndexes', () => {
    const PG_INDEXES_SQL_PATTERN = /pg_indexes/i;

    it('given an index that exists with the expected definition, when verified, then records a pass', async () => {
      const queryPg = vi.fn(async (sql: string) => {
        expect(sql).toMatch(PG_INDEXES_SQL_PATTERN);
        return [
          {
            indexname: 'day_entries_tags_unique_pair',
            indexdef:
              'CREATE UNIQUE INDEX day_entries_tags_unique_pair ON public.day_entries_tags USING btree (day_entries_id, tags_id)',
          },
        ];
      });

      const result = await verifyUniqueIndexes(queryPg, [
        {
          indexname: 'day_entries_tags_unique_pair',
          definitionMustMatch: /UNIQUE INDEX day_entries_tags_unique_pair.*day_entries_tags.*\(day_entries_id, tags_id\)/,
        },
      ]);

      expect(result.passes).toEqual(['day_entries_tags_unique_pair']);
      expect(result.failures).toEqual([]);
    });

    it('given an index that is missing entirely, when verified, then records a failure naming the index', async () => {
      const queryPg = vi.fn(async () => []);

      const result = await verifyUniqueIndexes(queryPg, [
        {
          indexname: 'tags_label_category_active_unique',
          definitionMustMatch: /UNIQUE INDEX/,
        },
      ]);

      expect(result.passes).toEqual([]);
      expect(result.failures).toHaveLength(1);
      expect(result.failures[0].name).toBe('tags_label_category_active_unique');
      expect(result.failures[0].issues.join(' ')).toMatch(/not found/i);
    });

    it('given an index whose definition does not match (e.g. missing WHERE clause), when verified, then records a failure', async () => {
      const queryPg = vi.fn(async () => [
        {
          indexname: 'tags_label_category_active_unique',
          indexdef:
            'CREATE UNIQUE INDEX tags_label_category_active_unique ON public.tags USING btree (lower(label::text), category)',
          // Missing the WHERE archived_at IS NULL clause
        },
      ]);

      const result = await verifyUniqueIndexes(queryPg, [
        {
          indexname: 'tags_label_category_active_unique',
          definitionMustMatch: /WHERE \(?archived_at IS NULL\)?/,
        },
      ]);

      expect(result.failures).toHaveLength(1);
      expect(result.failures[0].issues.join(' ')).toMatch(/definitionMustMatch/);
    });
  });

  describe('verifyCheckConstraints', () => {
    it('given a CHECK constraint that matches the expected def, when verified, then records a pass', async () => {
      const queryPg = vi.fn(async () => [
        {
          conname: 'day_entries_score_check',
          tablename: 'day_entries',
          def: 'CHECK ((score >= 1 AND score <= 10))',
        },
      ]);

      const result = await verifyCheckConstraints(queryPg, [
        {
          conname: 'day_entries_score_check',
          table: 'day_entries',
          definitionMustMatch: /score.*1.*10/i,
        },
      ]);

      expect(result.passes).toEqual(['day_entries_score_check']);
      expect(result.failures).toEqual([]);
    });

    it('given a missing CHECK constraint, when verified, then records a failure', async () => {
      const queryPg = vi.fn(async () => []);

      const result = await verifyCheckConstraints(queryPg, [
        {
          conname: 'tags_category_check',
          table: 'tags',
          definitionMustMatch: /category/i,
        },
      ]);

      expect(result.failures).toHaveLength(1);
      expect(result.failures[0].issues.join(' ')).toMatch(/not found/i);
    });

    it('given a CHECK constraint on the wrong table, when verified, then records a failure', async () => {
      const queryPg = vi.fn(async () => [
        {
          conname: 'tags_category_check',
          tablename: 'episodes',
          def: 'CHECK (category IN (...))',
        },
      ]);

      const result = await verifyCheckConstraints(queryPg, [
        {
          conname: 'tags_category_check',
          table: 'tags',
          definitionMustMatch: /category/i,
        },
      ]);

      expect(result.failures).toHaveLength(1);
      expect(result.failures[0].issues.join(' ')).toMatch(/table: expected tags/);
    });
  });
});
