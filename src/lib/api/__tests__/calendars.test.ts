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
  readItems: (collection: string, opts: unknown) => ({
    kind: 'readItems',
    collection,
    opts,
  }),
}));

import { getCronMonitorJob } from '../calendars';

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
});
