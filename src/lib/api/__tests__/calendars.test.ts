// Step-0 AC0.16: getCronMonitorJob — minimal smoke method against the
// Directus SDK. Established in step-0 so step-2 health endpoint has a
// foundation to read from.

import { describe, expect, it, vi, beforeEach } from 'vitest';

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
  deleteItem: (collection: string, id: string) => ({
    kind: 'deleteItem',
    collection,
    id,
  }),
}));

import {
  getCronMonitorJob,
  readConnectionById,
  upsertConnection,
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
});
