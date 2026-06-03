import { describe, expect, it, vi } from 'vitest';
// @ts-expect-error — .mjs lib without type declarations is intentional.
import { findCheckViolations } from '../lib/audit-check-violations.mjs';

type Row = Record<string, unknown>;

function makeRequest(rowsByCollection: Record<string, Row[]>) {
  return vi.fn(async (endpoint: string) => {
    for (const [collection, rows] of Object.entries(rowsByCollection)) {
      if (endpoint.startsWith(`/items/${collection}?`) || endpoint === `/items/${collection}`) {
        return { data: rows };
      }
    }
    return { data: [] };
  });
}

describe('audit-check-violations', () => {
  it('given clean rows across all 5 collections, when audited, then every constraint reports count 0', async () => {
    const directusRequest = makeRequest({
      tags: [
        { id: 't-1', label: 'pacing', category: 'mentaal' },
        { id: 't-2', label: 'moe', category: 'fysiek' },
      ],
      episodes: [
        {
          id: 'e-1',
          label: 'coaching',
          category: 'interventie',
          start_date: '2026-05-01',
          end_date: '2026-05-15',
        },
        {
          id: 'e-2',
          label: 'vakantie',
          category: 'levensgebeurtenis',
          start_date: '2026-06-01',
          end_date: null,
        },
      ],
      day_entries: [
        { id: 'd-1', date: '2026-05-01', score: 5, sleep_hours: 7.5 },
        { id: 'd-2', date: '2026-05-02', score: 1, sleep_hours: null },
        { id: 'd-3', date: '2026-05-03', score: 10, sleep_hours: 24 },
      ],
      day_entries_tags: [
        { id: 'j-1', tags_id: 't-1', confidence: 1.0 },
        { id: 'j-2', tags_id: 't-2', confidence: null },
      ],
      project_entries_tags: [],
    });

    const result = await findCheckViolations(directusRequest);

    const byName: Record<string, number> = {};
    for (const r of result) byName[r.name] = r.count;
    expect(byName).toEqual({
      tags_category_check: 0,
      episodes_category_check: 0,
      day_entries_score_check: 0,
      day_entries_sleep_hours_check: 0,
      episodes_date_order_check: 0,
      day_entries_tags_confidence_check: 0,
      project_entries_tags_confidence_check: 0,
    });
  });

  it('given a tag with an off-enum category, when audited, then tags_category_check reports count 1 with the offending sample', async () => {
    const directusRequest = makeRequest({
      tags: [
        { id: 't-1', label: 'helder', category: 'mentaal' },
        { id: 't-bad', label: 'spuit-elf', category: 'NotARealCategory' },
      ],
    });

    const result = await findCheckViolations(directusRequest);
    const entry = result.find(
      (r: { name: string }) => r.name === 'tags_category_check',
    );

    expect(entry?.count).toBe(1);
    expect(entry?.samples).toEqual([
      expect.objectContaining({ id: 't-bad', category: 'NotARealCategory' }),
    ]);
  });

  it('given a day_entry with score 0 or 11, when audited, then day_entries_score_check reports both', async () => {
    const directusRequest = makeRequest({
      day_entries: [
        { id: 'd-1', date: '2026-05-01', score: 5 },
        { id: 'd-low', date: '2026-05-02', score: 0 },
        { id: 'd-high', date: '2026-05-03', score: 11 },
      ],
    });

    const result = await findCheckViolations(directusRequest);
    const entry = result.find(
      (r: { name: string }) => r.name === 'day_entries_score_check',
    );

    expect(entry?.count).toBe(2);
  });

  it('given a day_entry with sleep_hours -1 or 25 (but not null), when audited, then day_entries_sleep_hours_check reports both', async () => {
    const directusRequest = makeRequest({
      day_entries: [
        { id: 'd-1', date: '2026-05-01', score: 5, sleep_hours: 8 },
        { id: 'd-null', date: '2026-05-02', score: 5, sleep_hours: null },
        { id: 'd-neg', date: '2026-05-03', score: 5, sleep_hours: -1 },
        { id: 'd-too-much', date: '2026-05-04', score: 5, sleep_hours: 25 },
      ],
    });

    const result = await findCheckViolations(directusRequest);
    const entry = result.find(
      (r: { name: string }) => r.name === 'day_entries_sleep_hours_check',
    );

    expect(entry?.count).toBe(2);
  });

  it('given an episode whose end_date precedes start_date, when audited, then episodes_date_order_check reports it; null end_date is OK', async () => {
    const directusRequest = makeRequest({
      episodes: [
        {
          id: 'e-ok-open',
          label: 'lopend',
          category: 'levensgebeurtenis',
          start_date: '2026-06-01',
          end_date: null,
        },
        {
          id: 'e-ok-equal',
          label: 'eendaagse',
          category: 'interventie',
          start_date: '2026-06-01',
          end_date: '2026-06-01',
        },
        {
          id: 'e-bad',
          label: 'inverted',
          category: 'interventie',
          start_date: '2026-06-10',
          end_date: '2026-06-01',
        },
      ],
    });

    const result = await findCheckViolations(directusRequest);
    const entry = result.find(
      (r: { name: string }) => r.name === 'episodes_date_order_check',
    );

    expect(entry?.count).toBe(1);
    expect(entry?.samples[0]).toMatchObject({ id: 'e-bad' });
  });

  it('given junction rows with confidence outside [0,1], when audited, then BOTH junction tables surface independently', async () => {
    const directusRequest = makeRequest({
      day_entries_tags: [
        { id: 'j-1', tags_id: 't', confidence: 1.5 },
      ],
      project_entries_tags: [
        { id: 'pj-1', tags_id: 't', confidence: -0.1 },
      ],
    });

    const result = await findCheckViolations(directusRequest);
    const day = result.find(
      (r: { name: string }) => r.name === 'day_entries_tags_confidence_check',
    );
    const proj = result.find(
      (r: { name: string }) => r.name === 'project_entries_tags_confidence_check',
    );

    expect(day?.count).toBe(1);
    expect(proj?.count).toBe(1);
  });
});
