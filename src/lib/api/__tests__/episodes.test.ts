import { beforeEach, describe, expect, it, vi } from 'vitest';

// Mock the Directus SDK — same hoisted-shared-mock pattern as tags.test.ts.
// Each SDK function returns a tagged object so tests can assert on which
// call was issued AND with what arguments. The `request` mock is shared
// state across all tests and reset in beforeEach.
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

import { createEpisode, readAllEpisodes, updateEpisode } from '../episodes';

type MockCmd = {
  __cmd: 'readItems' | 'createItem' | 'updateItem';
  collection?: string;
  query?: { filter?: unknown; sort?: unknown; limit?: number };
  item?: Record<string, unknown>;
  id?: string;
  patch?: Record<string, unknown>;
};

/** Factory for a complete Directus episode row, snake_case. */
function dbEpisode(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    id: 'ep_01HQ5XYZ',
    label: 'Coaching met Sarah',
    category: 'interventie',
    start_date: '2026-04-01',
    end_date: null,
    description: null,
    calendar_binding: null,
    archived_at: null,
    created_at: '2026-04-01T08:00:00.000Z',
    updated_at: '2026-04-01T08:00:00.000Z',
    ...overrides,
  };
}

describe('episodes SDK wrapper', () => {
  beforeEach(() => {
    mocks.request.mockReset();
  });

  // ===========================================================================
  // readAllEpisodes
  // ===========================================================================

  describe('readAllEpisodes', () => {
    it('returns an empty list when Directus returns no rows', async () => {
      mocks.request.mockResolvedValue([]);

      const result = await readAllEpisodes('access-token');

      expect(result).toEqual({ ok: true, value: [] });
    });

    it('returns episodes mapped through rowToEpisode (calendar_binding forced to null)', async () => {
      // A DB row with a stray non-null calendar_binding must be normalised
      // to null by the wrapper before reaching the domain layer.
      mocks.request.mockResolvedValue([
        dbEpisode({ calendar_binding: { stray: 'data' } }),
      ]);

      const result = await readAllEpisodes('access-token');

      expect(result.ok).toBe(true);
      if (!result.ok) return;
      expect(result.value).toHaveLength(1);
      expect(result.value[0]!.calendar_binding).toBeNull();
      expect(result.value[0]!.label).toBe('Coaching met Sarah');
    });

    it('default call passes archived_at: { _null: true } filter', async () => {
      mocks.request.mockResolvedValue([]);

      await readAllEpisodes('access-token');

      const cmd = mocks.request.mock.calls[0]![0] as MockCmd;
      expect(cmd.__cmd).toBe('readItems');
      expect(cmd.collection).toBe('episodes');
      expect(cmd.query?.filter).toEqual({ archived_at: { _null: true } });
    });

    it('with includeArchived: true does NOT pass the archived_at filter', async () => {
      mocks.request.mockResolvedValue([]);

      await readAllEpisodes('access-token', { includeArchived: true });

      const cmd = mocks.request.mock.calls[0]![0] as MockCmd;
      expect(cmd.query?.filter).toBeUndefined();
    });

    it('sort is start_date DESC', async () => {
      mocks.request.mockResolvedValue([]);

      await readAllEpisodes('access-token');

      const cmd = mocks.request.mock.calls[0]![0] as MockCmd;
      expect(cmd.query?.sort).toEqual(['-start_date']);
    });

    it('limit is -1 (unbounded)', async () => {
      mocks.request.mockResolvedValue([]);

      await readAllEpisodes('access-token');

      const cmd = mocks.request.mock.calls[0]![0] as MockCmd;
      expect(cmd.query?.limit).toBe(-1);
    });

    it('maps a fetch TypeError to network_error', async () => {
      mocks.request.mockRejectedValue(new TypeError('fetch failed'));

      const result = await readAllEpisodes('access-token');

      expect(result).toEqual({ ok: false, error: 'network_error' });
    });

    it('maps a non-network SDK error to directus_error', async () => {
      mocks.request.mockRejectedValue(new Error('HTTP 500 boom'));

      const result = await readAllEpisodes('access-token');

      expect(result).toEqual({ ok: false, error: 'directus_error' });
    });
  });

  // ===========================================================================
  // createEpisode
  // ===========================================================================

  describe('createEpisode', () => {
    it('given valid minimal input, POSTs label/category/start_date and nulls for the optional fields', async () => {
      mocks.request.mockResolvedValue(dbEpisode());

      await createEpisode('access-token', {
        label: 'Coaching met Sarah',
        category: 'interventie',
        start_date: '2026-04-01',
      });

      const cmd = mocks.request.mock.calls[0]![0] as MockCmd;
      expect(cmd.__cmd).toBe('createItem');
      expect(cmd.collection).toBe('episodes');
      expect(cmd.item).toEqual({
        label: 'Coaching met Sarah',
        category: 'interventie',
        start_date: '2026-04-01',
        end_date: null,
        description: null,
      });
    });

    it('given input with all optional fields set, POSTs them all', async () => {
      mocks.request.mockResolvedValue(
        dbEpisode({ end_date: '2026-06-01', description: 'wekelijks' }),
      );

      await createEpisode('access-token', {
        label: 'Ergotherapie',
        category: 'interventie',
        start_date: '2026-04-01',
        end_date: '2026-06-01',
        description: 'wekelijks',
      });

      const cmd = mocks.request.mock.calls[0]![0] as MockCmd;
      expect(cmd.item).toEqual({
        label: 'Ergotherapie',
        category: 'interventie',
        start_date: '2026-04-01',
        end_date: '2026-06-01',
        description: 'wekelijks',
      });
    });

    it('returns the row mapped through rowToEpisode', async () => {
      mocks.request.mockResolvedValue(dbEpisode());

      const result = await createEpisode('access-token', {
        label: 'Coaching met Sarah',
        category: 'interventie',
        start_date: '2026-04-01',
      });

      expect(result.ok).toBe(true);
      if (!result.ok) return;
      expect(result.value.id).toBe('ep_01HQ5XYZ');
      expect(result.value.label).toBe('Coaching met Sarah');
      expect(result.value.calendar_binding).toBeNull();
    });

    it('rejects invalid label without calling the SDK', async () => {
      const result = await createEpisode('access-token', {
        label: '   ',
        category: 'interventie',
        start_date: '2026-04-01',
      });

      expect(result).toEqual({ ok: false, error: 'invalid_label' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('rejects invalid category without calling the SDK', async () => {
      const result = await createEpisode('access-token', {
        label: 'Coaching met Sarah',
        category: 'project' as never,
        start_date: '2026-04-01',
      });

      expect(result).toEqual({ ok: false, error: 'invalid_category' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('rejects invalid date range (end < start) without calling the SDK', async () => {
      const result = await createEpisode('access-token', {
        label: 'Coaching met Sarah',
        category: 'interventie',
        start_date: '2026-04-01',
        end_date: '2026-03-15',
      });

      expect(result).toEqual({ ok: false, error: 'invalid_date_range' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('rejects non-string description without calling the SDK', async () => {
      const result = await createEpisode('access-token', {
        label: 'Coaching met Sarah',
        category: 'interventie',
        start_date: '2026-04-01',
        description: 42 as never,
      });

      expect(result).toEqual({ ok: false, error: 'invalid_description' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('rejects description > 10,000 chars without calling the SDK', async () => {
      const result = await createEpisode('access-token', {
        label: 'Coaching met Sarah',
        category: 'interventie',
        start_date: '2026-04-01',
        description: 'a'.repeat(10_001),
      });

      expect(result).toEqual({ ok: false, error: 'invalid_description' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('maps a fetch TypeError to network_error', async () => {
      mocks.request.mockRejectedValue(new TypeError('fetch failed'));

      const result = await createEpisode('access-token', {
        label: 'Coaching met Sarah',
        category: 'interventie',
        start_date: '2026-04-01',
      });

      expect(result).toEqual({ ok: false, error: 'network_error' });
    });

    it('maps a non-network SDK error to directus_error', async () => {
      mocks.request.mockRejectedValue(new Error('HTTP 500 boom'));

      const result = await createEpisode('access-token', {
        label: 'Coaching met Sarah',
        category: 'interventie',
        start_date: '2026-04-01',
      });

      expect(result).toEqual({ ok: false, error: 'directus_error' });
    });
  });

  // ===========================================================================
  // updateEpisode
  // ===========================================================================

  describe('updateEpisode', () => {
    it('rejects empty patch with empty_patch (no SDK call)', async () => {
      const result = await updateEpisode('access-token', 'ep_01HQ5XYZ', {});

      expect(result).toEqual({ ok: false, error: 'empty_patch' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('partial { description } PATCHes only description (no read of current row)', async () => {
      mocks.request.mockResolvedValue(dbEpisode({ description: 'updated' }));

      await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        description: 'updated',
      });

      // Exactly one SDK call: the updateItem PATCH. No prior readItems.
      expect(mocks.request).toHaveBeenCalledTimes(1);
      const cmd = mocks.request.mock.calls[0]![0] as MockCmd;
      expect(cmd.__cmd).toBe('updateItem');
      expect(cmd.id).toBe('ep_01HQ5XYZ');
      expect(cmd.patch).toEqual({ description: 'updated' });
    });

    it('partial { label } PATCHes only label (no read of current row)', async () => {
      mocks.request.mockResolvedValue(dbEpisode({ label: 'Nieuwe naam' }));

      await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        label: 'Nieuwe naam',
      });

      expect(mocks.request).toHaveBeenCalledTimes(1);
      const cmd = mocks.request.mock.calls[0]![0] as MockCmd;
      expect(cmd.__cmd).toBe('updateItem');
      expect(cmd.patch).toEqual({ label: 'Nieuwe naam' });
    });

    it('partial { archived_at: ISO } archives the episode', async () => {
      mocks.request.mockResolvedValue(
        dbEpisode({ archived_at: '2026-06-02T12:00:00.000Z' }),
      );

      await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        archived_at: '2026-06-02T12:00:00.000Z',
      });

      expect(mocks.request).toHaveBeenCalledTimes(1);
      const cmd = mocks.request.mock.calls[0]![0] as MockCmd;
      expect(cmd.patch).toEqual({ archived_at: '2026-06-02T12:00:00.000Z' });
    });

    it('partial { archived_at: null } un-archives the episode', async () => {
      mocks.request.mockResolvedValue(dbEpisode({ archived_at: null }));

      await updateEpisode('access-token', 'ep_01HQ5XYZ', { archived_at: null });

      expect(mocks.request).toHaveBeenCalledTimes(1);
      const cmd = mocks.request.mock.calls[0]![0] as MockCmd;
      expect(cmd.patch).toEqual({ archived_at: null });
    });

    it('partial { start_date, end_date } pair reads current row, validates, PATCHes BOTH', async () => {
      // First request: readItems for the merge validation.
      // Second request: updateItem with both date keys.
      mocks.request
        .mockResolvedValueOnce([dbEpisode()])
        .mockResolvedValueOnce(dbEpisode({ start_date: '2026-03-15', end_date: '2026-06-15' }));

      await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        start_date: '2026-03-15',
        end_date: '2026-06-15',
      });

      expect(mocks.request).toHaveBeenCalledTimes(2);
      const readCmd = mocks.request.mock.calls[0]![0] as MockCmd;
      const writeCmd = mocks.request.mock.calls[1]![0] as MockCmd;
      expect(readCmd.__cmd).toBe('readItems');
      expect(writeCmd.__cmd).toBe('updateItem');
      expect(writeCmd.patch).toEqual({
        start_date: '2026-03-15',
        end_date: '2026-06-15',
      });
    });

    it('partial { start_date } alone reads current row, validates against DB end_date, PATCHes only start_date', async () => {
      // DB row has end_date 2026-06-01. New start_date 2026-03-15 is before
      // that, so merge is valid. The PATCH carries ONLY start_date — the
      // existing end_date is not echoed back.
      mocks.request
        .mockResolvedValueOnce([dbEpisode({ end_date: '2026-06-01' })])
        .mockResolvedValueOnce(dbEpisode({ start_date: '2026-03-15', end_date: '2026-06-01' }));

      await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        start_date: '2026-03-15',
      });

      expect(mocks.request).toHaveBeenCalledTimes(2);
      const writeCmd = mocks.request.mock.calls[1]![0] as MockCmd;
      expect(writeCmd.patch).toEqual({ start_date: '2026-03-15' });
    });

    it('partial { end_date: ISO } alone fills in start_date from DB, validates, PATCHes only end_date', async () => {
      mocks.request
        .mockResolvedValueOnce([dbEpisode({ start_date: '2026-04-01', end_date: null })])
        .mockResolvedValueOnce(dbEpisode({ end_date: '2026-08-15' }));

      await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        end_date: '2026-08-15',
      });

      expect(mocks.request).toHaveBeenCalledTimes(2);
      const writeCmd = mocks.request.mock.calls[1]![0] as MockCmd;
      expect(writeCmd.patch).toEqual({ end_date: '2026-08-15' });
    });

    it('partial { end_date: null } alone un-completes the episode (PATCHes only end_date)', async () => {
      // DB row has a closed range. The caller un-completes by setting
      // end_date back to null. start_date stays as-is in the DB; the
      // merge validation uses (DB start, null) which is valid.
      mocks.request
        .mockResolvedValueOnce([
          dbEpisode({ start_date: '2026-04-01', end_date: '2026-06-01' }),
        ])
        .mockResolvedValueOnce(dbEpisode({ end_date: null }));

      await updateEpisode('access-token', 'ep_01HQ5XYZ', { end_date: null });

      expect(mocks.request).toHaveBeenCalledTimes(2);
      const writeCmd = mocks.request.mock.calls[1]![0] as MockCmd;
      expect(writeCmd.patch).toEqual({ end_date: null });
    });

    it('partial { start_date } whose merged pair fails ordering returns invalid_date_range (no write attempted)', async () => {
      // DB row: start=2026-04-01, end=2026-05-01. Caller wants
      // start=2026-06-01 — that would put start after end. Merge fails;
      // no write should fire.
      mocks.request.mockResolvedValueOnce([
        dbEpisode({ start_date: '2026-04-01', end_date: '2026-05-01' }),
      ]);

      const result = await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        start_date: '2026-06-01',
      });

      expect(result).toEqual({ ok: false, error: 'invalid_date_range' });
      // Only the read happened; the write was never attempted.
      expect(mocks.request).toHaveBeenCalledTimes(1);
      expect((mocks.request.mock.calls[0]![0] as MockCmd).__cmd).toBe('readItems');
    });

    it('partial { start_date } when the row does not exist (read returns []) maps to not_found', async () => {
      mocks.request.mockResolvedValueOnce([]);

      const result = await updateEpisode('access-token', 'ep_missing', {
        start_date: '2026-03-15',
      });

      expect(result).toEqual({ ok: false, error: 'not_found' });
      expect(mocks.request).toHaveBeenCalledTimes(1);
    });

    it('partial { start_date } when the read fails with network maps to network_error (no write)', async () => {
      mocks.request.mockRejectedValueOnce(new TypeError('fetch failed'));

      const result = await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        start_date: '2026-03-15',
      });

      expect(result).toEqual({ ok: false, error: 'network_error' });
      expect(mocks.request).toHaveBeenCalledTimes(1);
    });

    it('rejects { label: "" } with invalid_label (no read, no SDK write)', async () => {
      const result = await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        label: '   ',
      });

      expect(result).toEqual({ ok: false, error: 'invalid_label' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('rejects archived_at as a non-ISO string with invalid_archived_at', async () => {
      const result = await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        archived_at: 'not-a-timestamp' as never,
      });

      expect(result).toEqual({ ok: false, error: 'invalid_archived_at' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('rejects archived_at as undefined (vs missing key) with invalid_archived_at', async () => {
      // Setting `archived_at: undefined` in the patch IS sending the key
      // (`'archived_at' in patch` is true) with a wrong-type value. Must
      // surface as invalid_archived_at, not be silently coerced.
      const result = await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        archived_at: undefined as never,
      });

      expect(result).toEqual({ ok: false, error: 'invalid_archived_at' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('description > 10,000 chars rejected with invalid_description (no SDK call)', async () => {
      const result = await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        description: 'a'.repeat(10_001),
      });

      expect(result).toEqual({ ok: false, error: 'invalid_description' });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('SDK 404 on write maps to not_found', async () => {
      // No date in patch → no pre-read → write happens directly. Write
      // fails with a 404-shaped error message.
      mocks.request.mockRejectedValue(new Error('HTTP 404 not found'));

      const result = await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        label: 'new label',
      });

      expect(result).toEqual({ ok: false, error: 'not_found' });
    });

    it('network error on write maps to network_error', async () => {
      mocks.request.mockRejectedValue(new TypeError('fetch failed'));

      const result = await updateEpisode('access-token', 'ep_01HQ5XYZ', {
        label: 'new label',
      });

      expect(result).toEqual({ ok: false, error: 'network_error' });
    });
  });
});
