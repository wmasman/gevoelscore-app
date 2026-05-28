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
    createItem: (collection: string, data: unknown) => ({
      __cmd: 'createItem',
      collection,
      data,
    }),
    updateItem: (collection: string, id: string, data: unknown) => ({
      __cmd: 'updateItem',
      collection,
      id,
      data,
    }),
    createItems: (collection: string, data: unknown) => ({
      __cmd: 'createItems',
      collection,
      data,
    }),
    deleteItems: (collection: string, ids: unknown) => ({
      __cmd: 'deleteItems',
      collection,
      ids,
    }),
  };
});

import { readDayEntriesInRange, readDayEntryByDate, upsertDayEntry } from '../day-entries';

const directusRowAt = (date: string, score: number, tagIds: string[] = []) => ({
  id: `row-${date}`,
  date,
  score,
  note: null as string | null,
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

  describe('upsertDayEntry', () => {
    // Each upsert path is: read existing -> create OR update -> sync tags ->
    // re-read with full shape. We mock `request` per call sequentially.

    function setupCreate(rowAfter: ReturnType<typeof directusRowAt>) {
      // 1) read existing → empty
      mocks.request.mockResolvedValueOnce([]);
      // 2) createItem → returns the new id
      mocks.request.mockResolvedValueOnce({ id: rowAfter.id });
      // 3) re-read by date → returns the canonical post-write row
      mocks.request.mockResolvedValueOnce([rowAfter]);
    }

    function setupUpdate(
      existing: { id: string; tag_ids: string[] },
      rowAfter: ReturnType<typeof directusRowAt>,
    ) {
      // 1) read existing → one row
      mocks.request.mockResolvedValueOnce([
        { id: existing.id, tags: existing.tag_ids.map((t) => ({ tags_id: t })) },
      ]);
      // 2) updateItem → returns the existing id (Directus does)
      mocks.request.mockResolvedValueOnce({ id: existing.id });
      // 3) re-read → returns the canonical post-write row
      mocks.request.mockResolvedValueOnce([rowAfter]);
    }

    it('creates a new row when none exists for the date', async () => {
      const after = directusRowAt('2026-05-28', 7);
      setupCreate(after);

      const result = await upsertDayEntry('access-token', '2026-05-28', { score: 7 });

      expect(result.ok).toBe(true);
      if (!result.ok) return;
      expect(result.value.date).toBe('2026-05-28');
      expect(result.value.score).toBe(7);

      // First call: read existing by date.
      const firstCall = mocks.request.mock.calls[0]![0] as { __cmd: string };
      expect(firstCall.__cmd).toBe('readItems');
      // Second call: createItem in day_entries.
      const secondCall = mocks.request.mock.calls[1]![0] as {
        __cmd: string;
        collection: string;
        data: { date: string; score: number };
      };
      expect(secondCall.__cmd).toBe('createItem');
      expect(secondCall.collection).toBe('day_entries');
      expect(secondCall.data).toMatchObject({ date: '2026-05-28', score: 7 });
    });

    it('updates an existing row in place when one exists for the date', async () => {
      const after = directusRowAt('2026-05-28', 8);
      setupUpdate({ id: 'row-2026-05-28', tag_ids: [] }, after);

      const result = await upsertDayEntry('access-token', '2026-05-28', { score: 8 });

      expect(result.ok).toBe(true);
      if (!result.ok) return;
      expect(result.value.score).toBe(8);

      const secondCall = mocks.request.mock.calls[1]![0] as { __cmd: string; collection: string };
      expect(secondCall.__cmd).toBe('updateItem');
      expect(secondCall.collection).toBe('day_entries');
    });

    it('syncs M2M tags: removes ones not in patch, adds new ones', async () => {
      // Existing day_entry has tags [A, B]. Patch sends [B, C].
      // Net: delete A, add C, keep B (no-op on B).
      const after = directusRowAt('2026-05-28', 5, ['tag-B', 'tag-C']);
      // 1) Read existing returns day_entry with tags [A, B].
      mocks.request.mockResolvedValueOnce([
        {
          id: 'row-x',
          tags: [
            { tags_id: 'tag-A' },
            { tags_id: 'tag-B' },
          ],
        },
      ]);
      // 2) updateItem on the day_entry score.
      mocks.request.mockResolvedValueOnce({ id: 'row-x' });
      // 3) Read junction rows (to get junction ids for deletion).
      mocks.request.mockResolvedValueOnce([
        { id: 'jct-A', tags_id: 'tag-A' },
      ]);
      // 4) deleteItems for [jct-A].
      mocks.request.mockResolvedValueOnce(null);
      // 5) createItems for new junction row(s) — tag-C.
      mocks.request.mockResolvedValueOnce([{ id: 'jct-C-new' }]);
      // 6) re-read returns canonical post-write row.
      mocks.request.mockResolvedValueOnce([after]);

      const result = await upsertDayEntry('access-token', '2026-05-28', {
        score: 5,
        tag_ids: ['tag-B', 'tag-C'],
      });

      expect(result.ok).toBe(true);
      if (!result.ok) return;
      expect(result.value.tag_ids).toEqual(['tag-B', 'tag-C']);

      // Check the delete + create ops were issued correctly.
      const calls = mocks.request.mock.calls.map(
        (c) => c[0] as { __cmd: string; collection?: string; ids?: unknown; data?: unknown },
      );
      const deleteCall = calls.find((c) => c.__cmd === 'deleteItems');
      expect(deleteCall).toBeDefined();
      expect(deleteCall!.collection).toBe('day_entries_tags');
      expect(deleteCall!.ids).toEqual(['jct-A']);

      const createCall = calls.find((c) => c.__cmd === 'createItems');
      expect(createCall).toBeDefined();
      expect(createCall!.collection).toBe('day_entries_tags');
      const created = createCall!.data as Array<{ day_entries_id: string; tags_id: string; source: string }>;
      expect(created).toHaveLength(1);
      expect(created[0]).toMatchObject({
        day_entries_id: 'row-x',
        tags_id: 'tag-C',
        source: 'user',
      });
    });

    it('preserves note when patch omits it', async () => {
      const after = { ...directusRowAt('2026-05-28', 5), note: 'existing note' };
      setupUpdate({ id: 'row-x', tag_ids: [] }, after);

      const result = await upsertDayEntry('access-token', '2026-05-28', { score: 5 });

      expect(result.ok).toBe(true);
      const updateCall = mocks.request.mock.calls[1]![0] as { data: Record<string, unknown> };
      // No `note` key in the update payload — Directus preserves the existing value.
      expect('note' in updateCall.data).toBe(false);
    });

    it('clears note when patch sets note: null', async () => {
      const after = directusRowAt('2026-05-28', 5);
      after.note = null;
      setupUpdate({ id: 'row-x', tag_ids: [] }, after);

      const result = await upsertDayEntry('access-token', '2026-05-28', {
        score: 5,
        note: null,
      });

      expect(result.ok).toBe(true);
      const updateCall = mocks.request.mock.calls[1]![0] as { data: Record<string, unknown> };
      expect(updateCall.data.note).toBeNull();
    });

    it('maps a fetch TypeError to network_error', async () => {
      mocks.request.mockRejectedValue(new TypeError('fetch failed'));

      const result = await upsertDayEntry('access-token', '2026-05-28', { score: 7 });

      expect(result).toEqual({ ok: false, error: 'network_error' });
    });
  });
});
