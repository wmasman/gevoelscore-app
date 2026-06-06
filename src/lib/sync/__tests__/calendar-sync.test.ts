// Step-1 Phase 1.B — sync orchestrator tests.
// All dependencies are injected; the orchestrator itself is pure async
// flow control. Tests assert: window math, refresh-token error path,
// upsert logic, user_decision preservation, series-exclusion default,
// last_synced_at update, per-connection error containment.

import { describe, expect, it, vi, type MockedFunction } from 'vitest';
import {
  syncConnection,
  SYNC_WINDOW_BACK_DAYS,
  SYNC_WINDOW_FORWARD_DAYS,
  type SyncDeps,
} from '../calendar-sync';
import type { CalendarEvent, CalendarProvider } from '@/lib/integrations/calendar-provider';
import type {
  DirectusCalendarConnectionRow,
  DirectusCalendarEventRow,
} from '@/lib/api/calendars';

function makeConnection(
  overrides: Partial<DirectusCalendarConnectionRow> = {},
): DirectusCalendarConnectionRow {
  return {
    id: 'conn-1',
    user_id: 'user-1',
    provider: 'google',
    provider_account_email: 'user@example.com',
    refresh_token_encrypted: 'v1.iv.ct.tag',
    scope: 'https://www.googleapis.com/auth/calendar.readonly',
    connected_at: '2026-06-01T00:00:00Z',
    last_synced_at: null,
    last_sync_error: null,
    status: 'active',
    included_calendar_ids: ['user@example.com', 'work-cal'],
    ...overrides,
  };
}

function makeProviderEvent(overrides: Partial<CalendarEvent> = {}): CalendarEvent {
  return {
    providerEventId: 'evt-1',
    sourceCalendarId: 'cal-primary@gmail.com',
    recurrenceId: null,
    startAt: new Date('2026-06-04T10:00:00Z'),
    endAt: new Date('2026-06-04T11:00:00Z'),
    allDay: false,
    title: 'Event title',
    location: null,
    attendeesCount: 0,
    declined: false,
    eventType: 'default',
    status: 'confirmed',
    transparency: 'opaque',
    organizerIsSelf: false,
    iCalUid: 'i@google.com',
    htmlLink: 'https://calendar.google.com/x',
    ...overrides,
  };
}

function makeProvider(
  overrides: Partial<CalendarProvider> = {},
): CalendarProvider {
  return {
    id: 'google',
    buildAuthUrl: vi.fn(() => 'https://example.test'),
    exchangeCode: vi.fn(),
    refreshAccessToken: vi.fn().mockResolvedValue({
      accessToken: 'fresh-access-token',
      expiresAt: new Date(Date.now() + 3600 * 1000),
    }),
    listCalendars: vi.fn().mockResolvedValue([]),
    fetchEvents: vi.fn().mockResolvedValue([]),
    revoke: vi.fn(),
    ...overrides,
  } as CalendarProvider;
}

function makeDeps(overrides: Partial<SyncDeps> = {}): SyncDeps {
  return {
    provider: makeProvider(),
    decrypt: vi.fn((enc: string) => `decrypted(${enc})`),
    readSeriesExclusions: vi.fn().mockResolvedValue([]),
    readExistingEvents: vi.fn().mockResolvedValue([]),
    createEvent: vi.fn().mockResolvedValue(undefined),
    updateEvent: vi.fn().mockResolvedValue(undefined),
    updateConnection: vi.fn().mockResolvedValue(undefined),
    ...overrides,
  };
}

const NOW = new Date('2026-06-04T12:00:00Z');

describe('calendar-sync', () => {
  // ─────────────────────────────────────────────────────────────────
  // AC1.14 — window constants
  // ─────────────────────────────────────────────────────────────────

  describe('sync window constants (AC1.14)', () => {
    it('SYNC_WINDOW_BACK_DAYS is 7', () => {
      expect(SYNC_WINDOW_BACK_DAYS).toBe(7);
    });

    it('SYNC_WINDOW_FORWARD_DAYS is 30', () => {
      expect(SYNC_WINDOW_FORWARD_DAYS).toBe(30);
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // AC1.15 — refresh token flow + error
  // ─────────────────────────────────────────────────────────────────

  describe('refreshAccessToken flow (AC1.15)', () => {
    it('given a connection, when synced, then refreshAccessToken is called with the decrypted refresh token', async () => {
      const decrypt = vi.fn((enc: string) => `plain-${enc}`);
      const provider = makeProvider();
      const deps = makeDeps({ provider, decrypt });

      await syncConnection(makeConnection(), deps, NOW);

      expect(decrypt).toHaveBeenCalledWith('v1.iv.ct.tag');
      expect(provider.refreshAccessToken).toHaveBeenCalledWith('plain-v1.iv.ct.tag');
    });

    it('given refreshAccessToken throws refresh_token_invalid, when synced, then connection status set to error and last_sync_error captured', async () => {
      const provider = makeProvider({
        refreshAccessToken: vi
          .fn()
          .mockRejectedValue(new Error('refresh_token_invalid')),
      });
      const updateConnection = vi.fn().mockResolvedValue(undefined);
      const deps = makeDeps({ provider, updateConnection });

      const result = await syncConnection(makeConnection(), deps, NOW);

      expect(result.errors).toContain('refresh_token_invalid');
      expect(updateConnection).toHaveBeenCalledWith(
        'conn-1',
        expect.objectContaining({
          status: 'error',
          last_sync_error: 'refresh_token_invalid',
        }),
      );
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // AC1.16 — fetchEvents called with included_calendar_ids + window
  // ─────────────────────────────────────────────────────────────────

  describe('fetchEvents invocation (AC1.16)', () => {
    it('given a connection with included_calendar_ids, when synced, then provider.fetchEvents is called with those ids + 7-back/30-forward window', async () => {
      const provider = makeProvider();
      const deps = makeDeps({ provider });
      const conn = makeConnection({
        included_calendar_ids: ['cal-a', 'cal-b'],
      });

      await syncConnection(conn, deps, NOW);

      expect(provider.fetchEvents).toHaveBeenCalledTimes(1);
      const [accessToken, calIds, from, to] = (provider.fetchEvents as MockedFunction<
        CalendarProvider['fetchEvents']
      >).mock.calls[0]!;
      expect(accessToken).toBe('fresh-access-token');
      expect(calIds).toEqual(['cal-a', 'cal-b']);
      expect(from.getTime()).toBe(NOW.getTime() - 7 * 24 * 60 * 60 * 1000);
      expect(to.getTime()).toBe(NOW.getTime() + 30 * 24 * 60 * 60 * 1000);
    });

    it('given a windowOverride, when synced, then provider.fetchEvents uses the overridden from/to (for historical backfill)', async () => {
      const provider = makeProvider();
      const deps = makeDeps({ provider });
      const conn = makeConnection({
        included_calendar_ids: ['cal-a'],
      });
      const customFrom = new Date('2022-09-01T00:00:00Z');
      const customTo = new Date('2022-09-30T00:00:00Z');

      await syncConnection(conn, deps, NOW, { from: customFrom, to: customTo });

      const [, , from, to] = (provider.fetchEvents as MockedFunction<
        CalendarProvider['fetchEvents']
      >).mock.calls[0]!;
      expect(from.getTime()).toBe(customFrom.getTime());
      expect(to.getTime()).toBe(customTo.getTime());
    });

    it('given a partial windowOverride (only `from`), when synced, then `to` falls back to the default forward window', async () => {
      const provider = makeProvider();
      const deps = makeDeps({ provider });
      const conn = makeConnection({ included_calendar_ids: ['cal-a'] });
      const customFrom = new Date('2022-09-01T00:00:00Z');

      await syncConnection(conn, deps, NOW, { from: customFrom });

      const [, , from, to] = (provider.fetchEvents as MockedFunction<
        CalendarProvider['fetchEvents']
      >).mock.calls[0]!;
      expect(from.getTime()).toBe(customFrom.getTime());
      expect(to.getTime()).toBe(NOW.getTime() + 30 * 24 * 60 * 60 * 1000);
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // AC1.17 — reads series exclusions
  // ─────────────────────────────────────────────────────────────────

  describe('series exclusions read (AC1.17)', () => {
    it('given a connection, when synced, then readSeriesExclusions is called with the connection id', async () => {
      const readSeriesExclusions = vi.fn().mockResolvedValue(['rec-yoga']);
      const deps = makeDeps({ readSeriesExclusions });

      await syncConnection(makeConnection(), deps, NOW);

      expect(readSeriesExclusions).toHaveBeenCalledWith('conn-1');
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // AC1.18, AC1.19, AC1.20 — upsert + smart-default rules + user_decision
  // ─────────────────────────────────────────────────────────────────

  describe('upsert logic (AC1.18, AC1.19, AC1.20)', () => {
    it('given new events from the provider, when synced, then createEvent is called for each with user_decision=auto', async () => {
      const provider = makeProvider({
        fetchEvents: vi.fn().mockResolvedValue([
          makeProviderEvent({ providerEventId: 'evt-1' }),
          makeProviderEvent({ providerEventId: 'evt-2' }),
        ]),
      });
      const createEvent = vi.fn().mockResolvedValue(undefined);
      const deps = makeDeps({ provider, createEvent });

      const result = await syncConnection(makeConnection(), deps, NOW);

      expect(createEvent).toHaveBeenCalledTimes(2);
      expect(createEvent).toHaveBeenCalledWith(
        expect.objectContaining({
          provider_event_id: 'evt-1',
          user_decision: 'auto',
          included_as_context: true, // default rule for one-off non-declined
        }),
      );
      expect(result.eventsUpserted).toBe(2);
    });

    it('given an existing event row, when synced, then updateEvent is called and preserves the existing user_decision', async () => {
      const provider = makeProvider({
        fetchEvents: vi.fn().mockResolvedValue([
          makeProviderEvent({ providerEventId: 'evt-1', title: 'Updated title' }),
        ]),
      });
      const existing: DirectusCalendarEventRow = {
        id: 'row-1',
        connection_id: 'conn-1',
        provider: 'google',
        provider_event_id: 'evt-1',
        source_calendar_id: 'cal-primary@gmail.com',
        recurrence_id: null,
        start_at: '2026-06-04T10:00:00Z',
        end_at: '2026-06-04T11:00:00Z',
        all_day: false,
        title: 'Old title',
        location: null,
        attendees_count: 0,
        declined: false,
        event_type: 'default',
        status: 'confirmed',
        transparency: 'opaque',
        organizer_is_self: false,
        ical_uid: 'i@google.com',
        html_link: 'https://calendar.google.com/x',
        linked_tag_id: null,
        linked_episode_id: null,
        included_as_context: false,
        user_decision: 'user_excluded', // user manually excluded earlier
        created_at: '2026-06-03T00:00:00Z',
        updated_at: '2026-06-03T00:00:00Z',
      };
      const readExistingEvents = vi.fn().mockResolvedValue([existing]);
      const updateEvent = vi.fn().mockResolvedValue(undefined);
      const createEvent = vi.fn().mockResolvedValue(undefined);
      const deps = makeDeps({
        provider,
        readExistingEvents,
        updateEvent,
        createEvent,
      });

      await syncConnection(makeConnection(), deps, NOW);

      expect(createEvent).not.toHaveBeenCalled();
      expect(updateEvent).toHaveBeenCalledWith(
        'row-1',
        expect.objectContaining({
          title: 'Updated title',
          // user_decision NOT in the patch (or explicitly preserved)
        }),
      );
      const patch = (updateEvent as MockedFunction<SyncDeps['updateEvent']>).mock
        .calls[0]![1];
      // user_decision must not be flipped back to 'auto'
      expect(patch.user_decision).toBeUndefined();
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // AC1.21 — events under existing series exclusion
  // ─────────────────────────────────────────────────────────────────

  describe('series exclusion on insert (AC1.21)', () => {
    it('given a new event whose recurrence is in calendar_series_exclusions, when synced, then included_as_context=false + user_decision=user_excluded', async () => {
      const provider = makeProvider({
        fetchEvents: vi.fn().mockResolvedValue([
          makeProviderEvent({
            providerEventId: 'evt-yoga-1',
            recurrenceId: 'rec-yoga',
          }),
        ]),
      });
      const readSeriesExclusions = vi.fn().mockResolvedValue(['rec-yoga']);
      const createEvent = vi.fn().mockResolvedValue(undefined);
      const deps = makeDeps({ provider, readSeriesExclusions, createEvent });

      const result = await syncConnection(makeConnection(), deps, NOW);

      expect(createEvent).toHaveBeenCalledWith(
        expect.objectContaining({
          included_as_context: false,
          user_decision: 'user_excluded',
        }),
      );
      expect(result.eventsExcludedBySeries).toBe(1);
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // AC1.22 — connection update on success
  // ─────────────────────────────────────────────────────────────────

  describe('connection update on success (AC1.22)', () => {
    it('given a successful sync, when complete, then updateConnection sets last_synced_at=now, last_sync_error=null, status=active', async () => {
      const updateConnection = vi.fn().mockResolvedValue(undefined);
      const deps = makeDeps({ updateConnection });

      await syncConnection(makeConnection(), deps, NOW);

      expect(updateConnection).toHaveBeenCalledWith(
        'conn-1',
        expect.objectContaining({
          last_synced_at: NOW.toISOString(),
          last_sync_error: null,
          status: 'active',
        }),
      );
    });
  });

  // ─────────────────────────────────────────────────────────────────
  // AC1.23 — per-connection error containment
  // ─────────────────────────────────────────────────────────────────

  describe('error containment (AC1.23)', () => {
    it('given fetchEvents throws a generic error, when synced, then the error is captured in result.errors but the function resolves (does not throw)', async () => {
      const provider = makeProvider({
        fetchEvents: vi.fn().mockRejectedValue(new Error('network failed')),
      });
      const deps = makeDeps({ provider });

      const result = await syncConnection(makeConnection(), deps, NOW);

      expect(result.errors.length).toBeGreaterThan(0);
      // and the connection is marked as error
      expect(
        (deps.updateConnection as MockedFunction<SyncDeps['updateConnection']>)
          .mock.calls[0]![1].status,
      ).toBe('error');
    });
  });
});
