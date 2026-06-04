// Step-0 AC0.16: getCronMonitorJob — minimal smoke method against the
// Directus SDK. Established in step-0 so step-2 health endpoint has a
// foundation to read from.

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  request: vi.fn(),
}));

vi.mock('@directus/sdk', () => ({
  createDirectus: () => ({
    with: () => ({
      with: () => ({ request: mocks.request }),
    }),
  }),
  rest: () => () => null,
  staticToken: () => () => null,
  readItem: (collection: string, id: string) => ({
    kind: 'readItem',
    collection,
    id,
  }),
  readItems: (collection: string, opts: unknown) => ({
    kind: 'readItems',
    collection,
    opts,
  }),
  createItem: (collection: string, row: unknown) => ({
    kind: 'createItem',
    collection,
    row,
  }),
  updateItem: (collection: string, id: string, patch: unknown) => ({
    kind: 'updateItem',
    collection,
    id,
    patch,
  }),
  updateItems: (collection: string, ids: string[], patch: unknown) => ({
    kind: 'updateItems',
    collection,
    ids,
    patch,
  }),
  deleteItem: (collection: string, id: string) => ({
    kind: 'deleteItem',
    collection,
    id,
  }),
}));

import {
  getCronMonitorJob,
  readConnectionById,
  recordCronRun,
  upsertConnection,
  readEventsByProviderIds,
  readEventsByRecurrenceId,
  patchCalendarEventsBulk,
  readSeriesExclusionRecurrenceIds,
  insertSeriesExclusion,
  deleteSeriesExclusion,
} from '../calendars';

describe('calendars (Directus wrapper)', () => {
  beforeEach(() => {
    mocks.request.mockReset();
  });

  describe('getCronMonitorJob (AC0.16)', () => {
    it('given a job_name match, when called, then returns the row with shape DirectusCronMonitorRow', async () => {
      mocks.request.mockResolvedValue([
        {
          id: 'cm-1',
          job_name: 'daily_calendar_sync',
          last_run_at: '2026-06-03T03:00:00Z',
          last_result: '{"connections":1}',
          expected_interval_hours: 26,
          is_active: true,
        },
      ]);

      const result = await getCronMonitorJob('fake-token', 'daily_calendar_sync');

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value?.job_name).toBe('daily_calendar_sync');
        expect(result.value?.expected_interval_hours).toBe(26);
        expect(result.value?.is_active).toBe(true);
      }
    });

    it('given no matching row, when called, then returns null on the success branch', async () => {
      mocks.request.mockResolvedValue([]);

      const result = await getCronMonitorJob('fake-token', 'unknown_job');

      expect(result).toEqual({ ok: true, value: null });
    });

    it('given a network failure (TypeError: fetch failed), when called, then returns network_error', async () => {
      mocks.request.mockRejectedValue(
        new TypeError('fetch failed: ECONNREFUSED'),
      );

      const result = await getCronMonitorJob('fake-token', 'daily_calendar_sync');

      expect(result).toEqual({ ok: false, error: 'network_error' });
    });

    it('given a Directus error (anything non-TypeError), when called, then returns directus_error', async () => {
      mocks.request.mockRejectedValue(new Error('HTTP 500'));

      const result = await getCronMonitorJob('fake-token', 'daily_calendar_sync');

      expect(result).toEqual({ ok: false, error: 'directus_error' });
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // cron_monitor write (step-2 Phase 2.A)
  // ─────────────────────────────────────────────────────────────────

  describe('recordCronRun (AC2.1-2.5)', () => {
    beforeEach(() => {
      vi.useFakeTimers();
      vi.setSystemTime(new Date('2026-06-04T12:34:56.000Z'));
    });
    afterEach(() => {
      vi.useRealTimers();
    });

    it('given a success result, when called, then reads the row by job_name then PATCHes it by id (AC2.1)', async () => {
      mocks.request.mockResolvedValueOnce([
        { id: 'cm-1', job_name: 'daily_calendar_sync' },
      ]);
      mocks.request.mockResolvedValueOnce({});

      await recordCronRun('admin-token', 'daily_calendar_sync', {
        ok: true,
        details: {
          connections: 1,
          events_pulled: 0,
          events_upserted: 0,
          events_excluded_by_series: 0,
        },
      });

      expect(mocks.request).toHaveBeenCalledTimes(2);
      const readCall = mocks.request.mock.calls[0]![0] as {
        kind: string;
        collection: string;
        opts: { filter: unknown };
      };
      expect(readCall.kind).toBe('readItems');
      expect(readCall.collection).toBe('cron_monitor');
      expect(readCall.opts.filter).toEqual({
        job_name: { _eq: 'daily_calendar_sync' },
      });
      const patchCall = mocks.request.mock.calls[1]![0] as {
        kind: string;
        collection: string;
        id: string;
      };
      expect(patchCall.kind).toBe('updateItem');
      expect(patchCall.collection).toBe('cron_monitor');
      expect(patchCall.id).toBe('cm-1');
    });

    it('sets last_run_at to now in the PATCH (AC2.1)', async () => {
      mocks.request.mockResolvedValueOnce([{ id: 'cm-1' }]);
      mocks.request.mockResolvedValueOnce({});

      await recordCronRun('admin-token', 'daily_calendar_sync', {
        ok: true,
        details: { connections: 1 },
      });

      const patchCall = mocks.request.mock.calls[1]![0] as {
        patch: { last_run_at: string };
      };
      expect(patchCall.patch.last_run_at).toBe('2026-06-04T12:34:56.000Z');
    });

    it('sets last_result to JSON-encoded success body, counts only (AC2.1, AC2.2)', async () => {
      mocks.request.mockResolvedValueOnce([{ id: 'cm-1' }]);
      mocks.request.mockResolvedValueOnce({});

      const details = {
        connections: 1,
        events_pulled: 42,
        events_upserted: 40,
        events_excluded_by_series: 2,
      };
      await recordCronRun('admin-token', 'daily_calendar_sync', {
        ok: true,
        details,
      });

      const patchCall = mocks.request.mock.calls[1]![0] as {
        patch: { last_result: string };
      };
      expect(JSON.parse(patchCall.patch.last_result)).toEqual({
        ok: true,
        details,
      });
    });

    it('truncates last_result to 1000 chars hard cap (AC2.1)', async () => {
      mocks.request.mockResolvedValueOnce([{ id: 'cm-1' }]);
      mocks.request.mockResolvedValueOnce({});

      // Force the JSON body well over 1000 chars so the cap activates
      // regardless of small wording shifts in the wrapper.
      const huge: Record<string, number> = {};
      for (let i = 0; i < 200; i++) huge[`metric_${i}`] = i;

      await recordCronRun('admin-token', 'daily_calendar_sync', {
        ok: true,
        details: huge,
      });

      const patchCall = mocks.request.mock.calls[1]![0] as {
        patch: { last_result: string };
      };
      expect(patchCall.patch.last_result).toHaveLength(1000);
    });

    it('given a failure result, when called, then stores { ok: false, error: code } only (AC2.3)', async () => {
      mocks.request.mockResolvedValueOnce([{ id: 'cm-1' }]);
      mocks.request.mockResolvedValueOnce({});

      await recordCronRun('admin-token', 'daily_calendar_sync', {
        ok: false,
        error: 'refresh_token_invalid',
      });

      const patchCall = mocks.request.mock.calls[1]![0] as {
        patch: { last_result: string };
      };
      expect(JSON.parse(patchCall.patch.last_result)).toEqual({
        ok: false,
        error: 'refresh_token_invalid',
      });
    });

    it('when the read or PATCH throws (Directus unreachable), then does NOT propagate, logs, and resolves (AC2.5)', async () => {
      mocks.request.mockRejectedValue(
        new TypeError('fetch failed: ECONNREFUSED'),
      );
      const errSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      await expect(
        recordCronRun('admin-token', 'daily_calendar_sync', {
          ok: true,
          details: { connections: 0 },
        }),
      ).resolves.toBeUndefined();

      expect(errSpy).toHaveBeenCalled();
      errSpy.mockRestore();
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // calendar_connections CRUD (Phase 1.C)
  // ─────────────────────────────────────────────────────────────────

  describe('readConnectionById', () => {
    it('given a found id, when called, then returns the row', async () => {
      mocks.request.mockResolvedValue({
        id: 'conn-1',
        user_id: 'user-1',
        provider: 'google',
      });

      const result = await readConnectionById('at', 'conn-1');

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value?.id).toBe('conn-1');
      }
    });

    it('given a 404, when called, then returns null on the success branch', async () => {
      mocks.request.mockRejectedValue(new Error('HTTP 404'));

      const result = await readConnectionById('at', 'missing');

      expect(result).toEqual({ ok: true, value: null });
    });

    it('given a network error, when called, then returns network_error', async () => {
      mocks.request.mockRejectedValue(new TypeError('fetch failed'));

      const result = await readConnectionById('at', 'conn-1');

      expect(result).toEqual({ ok: false, error: 'network_error' });
    });
  });

  describe('upsertConnection', () => {
    it('given no existing row, when upserted, then INSERTs and returns the new id', async () => {
      // readItems (existing check) → empty
      mocks.request.mockResolvedValueOnce([]);
      // createItem → row
      mocks.request.mockResolvedValueOnce({ id: 'new-conn-id' });

      const result = await upsertConnection('at', {
        user_id: 'user-1',
        provider: 'google',
        provider_account_email: 'a@x.com',
        refresh_token_encrypted: 'v1.aaa.bbb.ccc',
        scope: 'https://www.googleapis.com/auth/calendar.readonly',
        connected_at: '2026-06-04T12:00:00Z',
      });

      expect(result).toEqual({ ok: true, value: 'new-conn-id' });
      // 2 calls: readItems (existing check) + createItem (insert)
      expect(mocks.request).toHaveBeenCalledTimes(2);
    });

    it('given an existing row by (user, provider, email), when upserted, then UPDATEs and returns existing id', async () => {
      mocks.request.mockResolvedValueOnce([
        { id: 'existing-conn-id', user_id: 'user-1' },
      ]);
      mocks.request.mockResolvedValueOnce({}); // updateItem ack

      const result = await upsertConnection('at', {
        user_id: 'user-1',
        provider: 'google',
        provider_account_email: 'a@x.com',
        refresh_token_encrypted: 'v1.new.encrypted.token',
        scope: 'https://www.googleapis.com/auth/calendar.readonly',
        connected_at: '2026-06-04T12:00:00Z',
      });

      expect(result).toEqual({ ok: true, value: 'existing-conn-id' });
      expect(mocks.request).toHaveBeenCalledTimes(2);
      // Second call should be updateItem with the refresh token + status=active
      const secondCall = mocks.request.mock.calls[1]![0] as {
        kind: string;
        patch: Record<string, unknown>;
      };
      expect(secondCall.kind).toBe('updateItem');
      expect(secondCall.patch.refresh_token_encrypted).toBe(
        'v1.new.encrypted.token',
      );
      expect(secondCall.patch.status).toBe('active');
      expect(secondCall.patch.last_sync_error).toBeNull();
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // calendar_events + calendar_series_exclusions CRUD (Phase 1.D)
  // ─────────────────────────────────────────────────────────────────

  describe('readEventsByProviderIds', () => {
    it('given an empty providerEventIds array, when called, then returns empty array without a wire call', async () => {
      const result = await readEventsByProviderIds('at', 'conn-1', []);

      expect(result).toEqual({ ok: true, value: [] });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('given a non-empty array, when called, then queries with the _in filter', async () => {
      mocks.request.mockResolvedValue([{ id: 'evt-row-1', provider_event_id: 'evt-1' }]);

      const result = await readEventsByProviderIds('at', 'conn-1', ['evt-1', 'evt-2']);

      expect(result.ok).toBe(true);
      const call = mocks.request.mock.calls[0]![0] as { opts: { filter: unknown } };
      expect(call.opts.filter).toMatchObject({
        _and: expect.any(Array),
      });
    });
  });

  describe('readEventsByRecurrenceId', () => {
    it('given a recurrence_id, when called, then queries with both connection_id and recurrence_id filters', async () => {
      mocks.request.mockResolvedValue([
        { id: 'evt-1', recurrence_id: 'rec-yoga' },
        { id: 'evt-2', recurrence_id: 'rec-yoga' },
      ]);

      const result = await readEventsByRecurrenceId('at', 'conn-1', 'rec-yoga');

      expect(result.ok).toBe(true);
      if (result.ok) expect(result.value).toHaveLength(2);
    });
  });

  describe('patchCalendarEventsBulk', () => {
    it('given an empty ids array, when called, then no wire call is made', async () => {
      const result = await patchCalendarEventsBulk('at', [], { included_as_context: false });

      expect(result).toEqual({ ok: true, value: undefined });
      expect(mocks.request).not.toHaveBeenCalled();
    });

    it('given a non-empty ids array, when called, then one updateItems call with the patch', async () => {
      mocks.request.mockResolvedValue([{}]);

      const result = await patchCalendarEventsBulk('at', ['evt-1', 'evt-2'], {
        included_as_context: false,
        user_decision: 'user_excluded',
      });

      expect(result.ok).toBe(true);
      const call = mocks.request.mock.calls[0]![0] as { kind: string; ids: string[] };
      expect(call.kind).toBe('updateItems');
      expect(call.ids).toEqual(['evt-1', 'evt-2']);
    });
  });

  describe('readSeriesExclusionRecurrenceIds', () => {
    it('given a connection_id, when called, then returns the recurrence_id strings only', async () => {
      mocks.request.mockResolvedValue([
        { recurrence_id: 'rec-yoga' },
        { recurrence_id: 'rec-standup' },
      ]);

      const result = await readSeriesExclusionRecurrenceIds('at', 'conn-1');

      expect(result).toEqual({
        ok: true,
        value: ['rec-yoga', 'rec-standup'],
      });
    });
  });

  describe('insertSeriesExclusion', () => {
    it('given a fresh recurrence_id, when inserted, then createItem is called and returns ok', async () => {
      mocks.request.mockResolvedValue({ id: 'new-exclusion' });

      const result = await insertSeriesExclusion(
        'at',
        'conn-1',
        'rec-yoga',
        '2026-06-04T12:00:00Z',
      );

      expect(result).toEqual({ ok: true, value: undefined });
    });

    it('given a UNIQUE violation (already excluded), when inserted, then treats as idempotent success', async () => {
      mocks.request.mockRejectedValue(new Error('RECORD_NOT_UNIQUE'));

      const result = await insertSeriesExclusion(
        'at',
        'conn-1',
        'rec-yoga',
        '2026-06-04T12:00:00Z',
      );

      expect(result).toEqual({ ok: true, value: undefined });
    });
  });

  describe('deleteSeriesExclusion', () => {
    it('given an existing exclusion, when deleted, then 2 calls (readItems lookup + deleteItem)', async () => {
      mocks.request.mockResolvedValueOnce([{ id: 'excl-1' }]);
      mocks.request.mockResolvedValueOnce({});

      const result = await deleteSeriesExclusion('at', 'conn-1', 'rec-yoga');

      expect(result).toEqual({ ok: true, value: undefined });
      expect(mocks.request).toHaveBeenCalledTimes(2);
    });

    it('given no matching row, when deleted, then no-op success (1 read call, no delete)', async () => {
      mocks.request.mockResolvedValueOnce([]);

      const result = await deleteSeriesExclusion('at', 'conn-1', 'rec-yoga');

      expect(result).toEqual({ ok: true, value: undefined });
      expect(mocks.request).toHaveBeenCalledTimes(1);
    });
  });
});
