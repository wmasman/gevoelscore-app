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

import { readDayEntriesInRange, readDayEntryByDate } from '../day-entries';

const directusRowAt = (date: string, score: number, tagIds: string[] = []) => ({
  id: `row-${date}`,
  date,
  score,
  note: null,
  sub_scores: null,
  sleep_hours: null,
  special_event: null,
  garmin: null,
  health: null,
  weather: null,
  derived: null,
  created_at: '2026-05-28T08:00:00.000Z',
  updated_at: '2026-05-28T08:00:00.000Z',
  tags: tagIds.map((id) => ({ tags_id: id })),
});

describe('day-entries SDK wrapper', () => {
  beforeEach(() => {
    mocks.request.mockReset();
  });

  describe('readDayEntryByDate', () => {
    it('returns null when no row exists for the date', async () => {
      mocks.request.mockResolvedValue([]);

      const result = await readDayEntryByDate('access-token', '2026-05-28');

      expect(result).toEqual({ ok: true, value: null });
    });

    it('flattens the Directus M2M tags shape to tag_ids on the DayEntry', async () => {
      mocks.request.mockResolvedValue([
        directusRowAt('2026-05-28', 7, ['tag-uuid-1', 'tag-uuid-2']),
      ]);

      const result = await readDayEntryByDate('access-token', '2026-05-28');

      expect(result.ok).toBe(true);
      if (!result.ok) return;
      expect(result.value).not.toBeNull();
      expect(result.value!.date).toBe('2026-05-28');
      expect(result.value!.score).toBe(7);
      expect(result.value!.tag_ids).toEqual(['tag-uuid-1', 'tag-uuid-2']);
      expect(result.value!.project_entry_ids).toEqual([]);
      expect(result.value!.calendar_event_ids).toEqual([]);
    });

    it('maps a fetch TypeError to network_error', async () => {
      mocks.request.mockRejectedValue(new TypeError('fetch failed'));

      const result = await readDayEntryByDate('access-token', '2026-05-28');

      expect(result).toEqual({ ok: false, error: 'network_error' });
    });

    it('maps an unknown Directus error to directus_error', async () => {
      mocks.request.mockRejectedValue({ errors: [{ extensions: { code: 'INTERNAL' } }] });

      const result = await readDayEntryByDate('access-token', '2026-05-28');

      expect(result).toEqual({ ok: false, error: 'directus_error' });
    });
  });

  describe('readDayEntriesInRange', () => {
    it('returns rows sorted by date ascending', async () => {
      mocks.request.mockResolvedValue([
        directusRowAt('2026-05-26', 4),
        directusRowAt('2026-05-27', 5),
        directusRowAt('2026-05-28', 7, ['tag-uuid-1']),
      ]);

      const result = await readDayEntriesInRange('access-token', '2026-05-26', '2026-05-28');

      expect(result.ok).toBe(true);
      if (!result.ok) return;
      expect(result.value.map((e) => e.date)).toEqual([
        '2026-05-26',
        '2026-05-27',
        '2026-05-28',
      ]);
      expect(result.value[2]!.tag_ids).toEqual(['tag-uuid-1']);
    });

    it('returns an empty array when no rows exist in the range', async () => {
      mocks.request.mockResolvedValue([]);

      const result = await readDayEntriesInRange('access-token', '2099-01-01', '2099-01-10');

      expect(result).toEqual({ ok: true, value: [] });
    });
  });
});
