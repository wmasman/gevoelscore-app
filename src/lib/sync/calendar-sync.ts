// Sync orchestrator: fetches events from a provider, applies smart-default
// rules, and upserts into Directus. Used by both the manual `Ververs nu`
// path (session-gated route) and the daily cron (bearer-gated route).
// Same code path, two triggers.
//
// All Directus + crypto dependencies are injected (DI). The route handler
// wires the real implementations; tests inject mocks. Keeps the orchestrator
// itself a pure async control-flow function.
//
// See docs/features/calendar-binding/step-1-google-oauth-and-context.md
// AC1.13-AC1.23.

import { computeDefaultIncluded } from '@/lib/domain/calendar-event';
import type {
  CalendarEvent,
  CalendarProvider,
} from '@/lib/integrations/calendar-provider';
import type {
  DirectusCalendarConnectionRow,
  DirectusCalendarEventRow,
} from '@/lib/api/calendars';

export const SYNC_WINDOW_BACK_DAYS = 7;
export const SYNC_WINDOW_FORWARD_DAYS = 30;
const MS_PER_DAY = 24 * 60 * 60 * 1000;

export type SyncResult = {
  connectionId: string;
  eventsPulled: number;
  eventsUpserted: number;
  eventsExcludedBySeries: number;
  errors: string[];
};

export type SyncDeps = {
  provider: CalendarProvider;
  decrypt: (encrypted: string) => string;
  readSeriesExclusions: (connectionId: string) => Promise<string[]>;
  readExistingEvents: (
    connectionId: string,
    providerEventIds: string[],
  ) => Promise<DirectusCalendarEventRow[]>;
  createEvent: (
    row: Omit<DirectusCalendarEventRow, 'id' | 'created_at' | 'updated_at'>,
  ) => Promise<void>;
  updateEvent: (
    id: string,
    patch: Partial<DirectusCalendarEventRow>,
  ) => Promise<void>;
  updateConnection: (
    id: string,
    patch: Partial<DirectusCalendarConnectionRow>,
  ) => Promise<void>;
};

// Maps a canonical CalendarEvent + the default-included decision into a
// Directus row shape (snake_case, ISO strings).
function mapToRow(
  event: CalendarEvent,
  connectionId: string,
  decision: { included: boolean; reason: string },
  userDecision: 'auto' | 'user_excluded',
): Omit<DirectusCalendarEventRow, 'id' | 'created_at' | 'updated_at'> {
  return {
    connection_id: connectionId,
    provider: 'google',
    provider_event_id: event.providerEventId,
    source_calendar_id: event.sourceCalendarId,
    recurrence_id: event.recurrenceId,
    start_at: event.startAt.toISOString(),
    end_at: event.endAt.toISOString(),
    all_day: event.allDay,
    title: event.title,
    location: event.location,
    attendees_count: event.attendeesCount,
    declined: event.declined,
    event_type: event.eventType,
    status: event.status,
    transparency: event.transparency,
    organizer_is_self: event.organizerIsSelf,
    ical_uid: event.iCalUid,
    html_link: event.htmlLink,
    linked_tag_id: null,
    linked_episode_id: null,
    included_as_context: decision.included,
    user_decision: userDecision,
  };
}

// Patch payload for an existing event. Excludes user_decision (preserved
// across syncs) + linked_tag_id / linked_episode_id (user-set, never
// rewritten by sync). source_calendar_id IS in the patch so back-fill
// runs of code that predates v1.6.1 fill in the field on existing rows.
function mapToPatch(
  event: CalendarEvent,
): Partial<DirectusCalendarEventRow> {
  return {
    source_calendar_id: event.sourceCalendarId,
    recurrence_id: event.recurrenceId,
    start_at: event.startAt.toISOString(),
    end_at: event.endAt.toISOString(),
    all_day: event.allDay,
    title: event.title,
    location: event.location,
    attendees_count: event.attendeesCount,
    declined: event.declined,
    event_type: event.eventType,
    status: event.status,
    transparency: event.transparency,
    organizer_is_self: event.organizerIsSelf,
    ical_uid: event.iCalUid,
    html_link: event.htmlLink,
  };
}

export type SyncWindow = {
  /** Override the default 7-back computation. Useful for historical backfill. */
  from?: Date;
  /** Override the default 30-forward computation. */
  to?: Date;
};

export async function syncConnection(
  connection: DirectusCalendarConnectionRow,
  deps: SyncDeps,
  now: Date,
  windowOverride?: SyncWindow,
): Promise<SyncResult> {
  const result: SyncResult = {
    connectionId: connection.id,
    eventsPulled: 0,
    eventsUpserted: 0,
    eventsExcludedBySeries: 0,
    errors: [],
  };

  // 1. Decrypt refresh token + refresh access token.
  let accessToken: string;
  try {
    const refreshToken = deps.decrypt(connection.refresh_token_encrypted);
    const refreshed = await deps.provider.refreshAccessToken(refreshToken);
    accessToken = refreshed.accessToken;
  } catch (e) {
    const code = e instanceof Error ? e.message : 'unknown_error';
    result.errors.push(code);
    await deps.updateConnection(connection.id, {
      status: 'error',
      last_sync_error: code,
    });
    return result;
  }

  // 2. Fetch events in the rolling window (or the override for backfill).
  const from =
    windowOverride?.from ??
    new Date(now.getTime() - SYNC_WINDOW_BACK_DAYS * MS_PER_DAY);
  const to =
    windowOverride?.to ??
    new Date(now.getTime() + SYNC_WINDOW_FORWARD_DAYS * MS_PER_DAY);

  let fetched: CalendarEvent[];
  try {
    fetched = await deps.provider.fetchEvents(
      accessToken,
      connection.included_calendar_ids,
      from,
      to,
    );
  } catch (e) {
    const code = e instanceof Error ? e.message : 'unknown_error';
    result.errors.push(code);
    await deps.updateConnection(connection.id, {
      status: 'error',
      last_sync_error: code,
    });
    return result;
  }
  result.eventsPulled = fetched.length;

  // 3. Load series exclusions + existing event rows.
  const seriesExclusionList = await deps.readSeriesExclusions(connection.id);
  const seriesExclusions = new Set(seriesExclusionList);
  const providerEventIds = fetched.map((e) => e.providerEventId);
  const existingRows = providerEventIds.length
    ? await deps.readExistingEvents(connection.id, providerEventIds)
    : [];
  const existingByProviderId = new Map(
    existingRows.map((r) => [r.provider_event_id, r]),
  );

  // 4. Upsert each event.
  for (const event of fetched) {
    const decision = computeDefaultIncluded(event, seriesExclusions);
    if (decision.reason === 'series_excluded') {
      result.eventsExcludedBySeries++;
    }

    const existing = existingByProviderId.get(event.providerEventId);
    try {
      if (existing) {
        await deps.updateEvent(existing.id, mapToPatch(event));
      } else {
        const userDecision: 'auto' | 'user_excluded' =
          decision.reason === 'series_excluded' ? 'user_excluded' : 'auto';
        await deps.createEvent(mapToRow(event, connection.id, decision, userDecision));
      }
      result.eventsUpserted++;
    } catch (e) {
      const code = e instanceof Error ? e.message : 'upsert_failed';
      result.errors.push(code);
    }
  }

  // 5. Mark connection success / partial-failure.
  if (result.errors.length === 0) {
    await deps.updateConnection(connection.id, {
      last_synced_at: now.toISOString(),
      last_sync_error: null,
      status: 'active',
    });
  } else {
    await deps.updateConnection(connection.id, {
      last_synced_at: now.toISOString(),
      last_sync_error: result.errors.join('; ').slice(0, 500),
      status: 'error',
    });
  }

  return result;
}
