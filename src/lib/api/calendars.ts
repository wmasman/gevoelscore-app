// Server-side SDK wrapper for the calendar-binding feature (v1.6).
// Mirrors the shape of tags.ts / episodes.ts / day-entries.ts:
// stateless functions, fresh client per call, Result-shaped returns.
//
// Step-0 shipped the 4 row types + getCronMonitorJob.
// Step-1 Phase 1.C adds connection CRUD.
// Step-1 Phase 1.D will add event CRUD (read/create/update) +
//   series-exclusion read/insert/delete.
//
// See docs/features/calendar-binding/step-1-google-oauth-and-context.md
// AC1.30-AC1.43.

import {
  createDirectus,
  createItem,
  deleteItem,
  readItem,
  readItems,
  rest,
  staticToken,
  updateItem,
  updateItems,
} from '@directus/sdk';
import type { Result } from './result';

export type CalendarsError = 'network_error' | 'directus_error';

export type DirectusCalendarConnectionRow = {
  id: string;
  user_id: string;
  provider: 'google';
  provider_account_email: string;
  refresh_token_encrypted: string;
  scope: string;
  connected_at: string;
  last_synced_at: string | null;
  last_sync_error: string | null;
  status: 'active' | 'disconnected' | 'error';
  included_calendar_ids: string[];
};

export type DirectusCalendarEventRow = {
  id: string;
  connection_id: string;
  provider: 'google';
  provider_event_id: string;
  recurrence_id: string | null;
  start_at: string;
  end_at: string;
  all_day: boolean;
  title: string;
  location: string | null;
  attendees_count: number;
  declined: boolean;
  event_type: string | null;
  status: 'confirmed' | 'tentative' | 'cancelled';
  transparency: 'opaque' | 'transparent';
  organizer_is_self: boolean;
  ical_uid: string | null;
  html_link: string | null;
  linked_tag_id: string | null;
  linked_episode_id: string | null;
  included_as_context: boolean;
  user_decision: 'auto' | 'user_included' | 'user_excluded';
  created_at: string;
  updated_at: string;
};

export type DirectusCalendarSeriesExclusionRow = {
  id: string;
  connection_id: string;
  recurrence_id: string;
  excluded_at: string;
};

export type DirectusCronMonitorRow = {
  id: string;
  job_name: string;
  last_run_at: string | null;
  last_result: string | null;
  expected_interval_hours: number;
  is_active: boolean;
};

type DirectusSchema = {
  calendar_connections: DirectusCalendarConnectionRow[];
  calendar_events: DirectusCalendarEventRow[];
  calendar_series_exclusions: DirectusCalendarSeriesExclusionRow[];
  cron_monitor: DirectusCronMonitorRow[];
};

function directusUrl(): string {
  return (
    process.env.DIRECTUS_URL ??
    process.env.NEXT_PUBLIC_DIRECTUS_URL ??
    'http://localhost:8055'
  );
}

function isNetworkError(e: unknown): boolean {
  return e instanceof TypeError && /fetch/i.test(e.message);
}

function classifyError(e: unknown): CalendarsError {
  return isNetworkError(e) ? 'network_error' : 'directus_error';
}

function makeClient(accessToken: string) {
  return createDirectus<DirectusSchema>(directusUrl())
    .with(rest())
    .with(staticToken(accessToken));
}

// ─────────────────────────────────────────────────────────────────
// cron_monitor read
// ─────────────────────────────────────────────────────────────────

export async function getCronMonitorJob(
  accessToken: string,
  jobName: string,
): Promise<Result<DirectusCronMonitorRow | null, CalendarsError>> {
  try {
    const rows = (await makeClient(accessToken).request(
      readItems('cron_monitor', {
        filter: { job_name: { _eq: jobName } },
        limit: 1,
      } as never),
    )) as DirectusCronMonitorRow[];
    return { ok: true, value: rows[0] ?? null };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

// ─────────────────────────────────────────────────────────────────
// calendar_connections CRUD (Phase 1.C)
// ─────────────────────────────────────────────────────────────────

export type UpsertConnectionInput = {
  user_id: string;
  provider: 'google';
  provider_account_email: string;
  refresh_token_encrypted: string;
  scope: string;
  connected_at: string;
};

/**
 * Read a single connection by id. Returns null when not found.
 */
export async function readConnectionById(
  accessToken: string,
  id: string,
): Promise<
  Result<DirectusCalendarConnectionRow | null, CalendarsError>
> {
  try {
    const row = (await makeClient(accessToken).request(
      readItem('calendar_connections', id),
    )) as DirectusCalendarConnectionRow;
    return { ok: true, value: row };
  } catch (e) {
    const msg = String((e as { message?: string }).message ?? '');
    if (msg.includes('404') || msg.includes('FORBIDDEN')) {
      return { ok: true, value: null };
    }
    return { ok: false, error: classifyError(e) };
  }
}

/**
 * Read all active connections for a user. Used by the manual `Ververs nu`
 * sync route (session path) to iterate the session-user's connections.
 */
export async function readActiveConnectionsForUser(
  accessToken: string,
  userId: string,
): Promise<Result<DirectusCalendarConnectionRow[], CalendarsError>> {
  try {
    const rows = (await makeClient(accessToken).request(
      readItems('calendar_connections', {
        filter: {
          _and: [
            { user_id: { _eq: userId } },
            { status: { _eq: 'active' } },
          ],
        },
        limit: -1,
      } as never),
    )) as DirectusCalendarConnectionRow[];
    return { ok: true, value: rows };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

/**
 * Read all active connections across all users. Used by the daily cron
 * (bearer-gated sync route), which is system-scope, not user-scope.
 */
export async function readAllActiveConnections(
  accessToken: string,
): Promise<Result<DirectusCalendarConnectionRow[], CalendarsError>> {
  try {
    const rows = (await makeClient(accessToken).request(
      readItems('calendar_connections', {
        filter: { status: { _eq: 'active' } },
        limit: -1,
      } as never),
    )) as DirectusCalendarConnectionRow[];
    return { ok: true, value: rows };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

/**
 * Upsert a connection by (user_id, provider, provider_account_email).
 * INSERT if no row matches; UPDATE the existing row otherwise (refreshes
 * the encrypted refresh token + scope + connected_at + clears any prior
 * status='error'). Idempotent — re-running connect for the same account
 * does not create duplicates.
 */
export async function upsertConnection(
  accessToken: string,
  input: UpsertConnectionInput,
): Promise<Result<string, CalendarsError>> {
  try {
    const client = makeClient(accessToken);
    const existing = (await client.request(
      readItems('calendar_connections', {
        filter: {
          _and: [
            { user_id: { _eq: input.user_id } },
            { provider: { _eq: input.provider } },
            { provider_account_email: { _eq: input.provider_account_email } },
          ],
        },
        limit: 1,
      } as never),
    )) as DirectusCalendarConnectionRow[];

    if (existing.length > 0 && existing[0]) {
      await client.request(
        updateItem('calendar_connections', existing[0].id, {
          refresh_token_encrypted: input.refresh_token_encrypted,
          scope: input.scope,
          connected_at: input.connected_at,
          status: 'active',
          last_sync_error: null,
        }),
      );
      return { ok: true, value: existing[0].id };
    }

    const created = (await client.request(
      createItem('calendar_connections', {
        user_id: input.user_id,
        provider: input.provider,
        provider_account_email: input.provider_account_email,
        refresh_token_encrypted: input.refresh_token_encrypted,
        scope: input.scope,
        connected_at: input.connected_at,
        last_synced_at: null,
        last_sync_error: null,
        status: 'active',
        included_calendar_ids: [],
      }),
    )) as DirectusCalendarConnectionRow;
    return { ok: true, value: created.id };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

/**
 * PATCH a connection row. Used by:
 *   - choose-calendars POST to set included_calendar_ids
 *   - sync orchestrator to update last_synced_at + last_sync_error + status
 */
export async function patchConnection(
  accessToken: string,
  id: string,
  patch: Partial<DirectusCalendarConnectionRow>,
): Promise<Result<void, CalendarsError>> {
  try {
    await makeClient(accessToken).request(
      updateItem('calendar_connections', id, patch),
    );
    return { ok: true, value: undefined };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

/**
 * Delete a connection. FK CASCADE on the related events + series
 * exclusions removes them automatically. Used by disconnect.
 */
export async function deleteConnection(
  accessToken: string,
  id: string,
): Promise<Result<void, CalendarsError>> {
  try {
    await makeClient(accessToken).request(
      deleteItem('calendar_connections', id),
    );
    return { ok: true, value: undefined };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

// ─────────────────────────────────────────────────────────────────
// calendar_events CRUD (Phase 1.D)
// ─────────────────────────────────────────────────────────────────

/**
 * Read a single event by id. Returns null if not found.
 */
export async function readCalendarEventById(
  accessToken: string,
  id: string,
): Promise<Result<DirectusCalendarEventRow | null, CalendarsError>> {
  try {
    const row = (await makeClient(accessToken).request(
      readItem('calendar_events', id),
    )) as DirectusCalendarEventRow;
    return { ok: true, value: row };
  } catch (e) {
    const msg = String((e as { message?: string }).message ?? '');
    if (msg.includes('404') || msg.includes('FORBIDDEN')) {
      return { ok: true, value: null };
    }
    return { ok: false, error: classifyError(e) };
  }
}

/**
 * Read existing event rows for the given (connection_id, provider_event_id)
 * tuples. Used by the sync orchestrator to diff fetched events against
 * what's already stored.
 */
export async function readEventsByProviderIds(
  accessToken: string,
  connectionId: string,
  providerEventIds: string[],
): Promise<Result<DirectusCalendarEventRow[], CalendarsError>> {
  if (providerEventIds.length === 0) {
    return { ok: true, value: [] };
  }
  try {
    const rows = (await makeClient(accessToken).request(
      readItems('calendar_events', {
        filter: {
          _and: [
            { connection_id: { _eq: connectionId } },
            { provider_event_id: { _in: providerEventIds } },
          ],
        },
        limit: -1,
      } as never),
    )) as DirectusCalendarEventRow[];
    return { ok: true, value: rows };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

/**
 * Read all events sharing a recurrence_id within a connection. Used by
 * the include-series + sluit-uit-recurring routes to apply a bulk
 * status flip across an entire series.
 */
export async function readEventsByRecurrenceId(
  accessToken: string,
  connectionId: string,
  recurrenceId: string,
): Promise<Result<DirectusCalendarEventRow[], CalendarsError>> {
  try {
    const rows = (await makeClient(accessToken).request(
      readItems('calendar_events', {
        filter: {
          _and: [
            { connection_id: { _eq: connectionId } },
            { recurrence_id: { _eq: recurrenceId } },
          ],
        },
        limit: -1,
      } as never),
    )) as DirectusCalendarEventRow[];
    return { ok: true, value: rows };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

export async function createCalendarEvent(
  accessToken: string,
  row: Omit<DirectusCalendarEventRow, 'id' | 'created_at' | 'updated_at'>,
): Promise<Result<string, CalendarsError>> {
  try {
    const created = (await makeClient(accessToken).request(
      createItem('calendar_events', row),
    )) as DirectusCalendarEventRow;
    return { ok: true, value: created.id };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

export async function patchCalendarEvent(
  accessToken: string,
  id: string,
  patch: Partial<DirectusCalendarEventRow>,
): Promise<Result<void, CalendarsError>> {
  try {
    await makeClient(accessToken).request(
      updateItem('calendar_events', id, patch),
    );
    return { ok: true, value: undefined };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

/**
 * Patch multiple events with the same payload in a single SDK call.
 * Used by the recurring-event sluit-uit / include-series routes.
 */
export async function patchCalendarEventsBulk(
  accessToken: string,
  ids: string[],
  patch: Partial<DirectusCalendarEventRow>,
): Promise<Result<void, CalendarsError>> {
  if (ids.length === 0) {
    return { ok: true, value: undefined };
  }
  try {
    await makeClient(accessToken).request(
      updateItems('calendar_events', ids, patch),
    );
    return { ok: true, value: undefined };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

// ─────────────────────────────────────────────────────────────────
// calendar_series_exclusions CRUD (Phase 1.D)
// ─────────────────────────────────────────────────────────────────

/**
 * Read all series exclusions for a connection. Returns recurrence_ids
 * only (the orchestrator builds a Set from them).
 */
export async function readSeriesExclusionRecurrenceIds(
  accessToken: string,
  connectionId: string,
): Promise<Result<string[], CalendarsError>> {
  try {
    const rows = (await makeClient(accessToken).request(
      readItems('calendar_series_exclusions', {
        filter: { connection_id: { _eq: connectionId } },
        fields: ['recurrence_id'],
        limit: -1,
      } as never),
    )) as DirectusCalendarSeriesExclusionRow[];
    return { ok: true, value: rows.map((r) => r.recurrence_id) };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

/**
 * Insert a series exclusion. Idempotent on UNIQUE(connection_id,
 * recurrence_id) — a Directus duplicate-key error is treated as success.
 */
export async function insertSeriesExclusion(
  accessToken: string,
  connectionId: string,
  recurrenceId: string,
  excludedAt: string,
): Promise<Result<void, CalendarsError>> {
  try {
    await makeClient(accessToken).request(
      createItem('calendar_series_exclusions', {
        connection_id: connectionId,
        recurrence_id: recurrenceId,
        excluded_at: excludedAt,
      }),
    );
    return { ok: true, value: undefined };
  } catch (e) {
    // UNIQUE violation = already excluded = idempotent success
    const msg = String((e as { message?: string }).message ?? '');
    if (msg.includes('RECORD_NOT_UNIQUE') || msg.includes('duplicate') || msg.includes('UNIQUE')) {
      return { ok: true, value: undefined };
    }
    return { ok: false, error: classifyError(e) };
  }
}

/**
 * Delete a series exclusion (for the symmetric coarse re-include action).
 * Idempotent — already-absent is treated as success.
 */
export async function deleteSeriesExclusion(
  accessToken: string,
  connectionId: string,
  recurrenceId: string,
): Promise<Result<void, CalendarsError>> {
  try {
    const rows = (await makeClient(accessToken).request(
      readItems('calendar_series_exclusions', {
        filter: {
          _and: [
            { connection_id: { _eq: connectionId } },
            { recurrence_id: { _eq: recurrenceId } },
          ],
        },
        limit: 1,
      } as never),
    )) as DirectusCalendarSeriesExclusionRow[];
    const row = rows[0];
    if (!row) return { ok: true, value: undefined };
    await makeClient(accessToken).request(
      deleteItem('calendar_series_exclusions', row.id),
    );
    return { ok: true, value: undefined };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}
