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
  /**
   * The provider-side calendar this event came from. v1.6.1 addition;
   * NULL for events imported by code that predates v1.6.1 (the initial
   * smoke + first historical backfill). Future syncs populate it on
   * every upsert (mapToPatch + mapToRow both include it). Used by the
   * choose-calendars POST to delete events of a calendar the user
   * just removed from the include list.
   */
  source_calendar_id: string | null;
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
  // Logs the underlying Directus SDK error (code + first line of
  // message) before classifying. The SDK throws structured objects of
  // shape { errors: [{ message, extensions: { code, ... } }] } rather
  // than Error instances, so we extract the known fields here.
  //
  // Worth keeping in prod: the verbose form survived the step-1 debug
  // arc (surfaced FORBIDDEN, RECORD_NOT_UNIQUE during the historical
  // backfill). No PII: SDK error messages contain endpoint paths +
  // status codes + collection names, not user data. If it ever
  // becomes noisy, gate behind `process.env.NODE_ENV !== 'production'`.
  try {
    const obj = e as Record<string, unknown> | null | undefined;
    const errors = obj?.errors as
      | Array<{ message?: string; extensions?: { code?: string } }>
      | undefined;
    if (Array.isArray(errors) && errors.length > 0) {
      const first = errors[0];
      console.error(
        `[calendars] directus_error: ${first?.extensions?.code ?? 'unknown'}: ${(first?.message ?? 'no message').slice(0, 300)}`,
      );
    } else if (e instanceof Error) {
      console.error(
        `[calendars] directus_error: ${e.constructor.name}: ${e.message.slice(0, 300)}`,
      );
    } else {
      // Fallback: dump the keys we know are safe.
      const safe = {
        status: obj?.status,
        statusText: obj?.statusText,
        message: typeof obj?.message === 'string' ? obj.message.slice(0, 300) : undefined,
        name: typeof obj?.name === 'string' ? obj.name : undefined,
      };
      console.error(`[calendars] directus_error: ${JSON.stringify(safe)}`);
    }
  } catch {
    // never throw from a logger
    console.error('[calendars] directus_error: (failed to serialize)');
  }
  return isNetworkError(e) ? 'network_error' : 'directus_error';
}

function makeClient(accessToken: string) {
  return createDirectus<DirectusSchema>(directusUrl())
    .with(rest())
    .with(staticToken(accessToken));
}

// ─────────────────────────────────────────────────────────────────
// cron_monitor read + write
// ─────────────────────────────────────────────────────────────────

export type CronRunResult =
  | { ok: true; details: object }
  | { ok: false; error: string };

/**
 * PATCH the cron_monitor row matching `jobName` with `last_run_at = now`
 * and `last_result = JSON.stringify(result).slice(0, 1000)`. Defensive
 * by design (AC2.5): never throws. A failure to write the monitor row
 * must not break the sync route's own 200 response — the monitor is a
 * staleness signal, not a critical-path write.
 *
 * The 1000-char cap (AC2.1) prevents accidental log-equivalent
 * disclosure if a future error message ever leaks into what should be
 * a code-only field. Caller is responsible for supplying counts-only
 * success details (AC2.2) and short error codes (AC2.3) — this
 * function does not enforce shape beyond the type signature.
 *
 * step-2 Phase 2.A.
 */
export async function recordCronRun(
  adminToken: string,
  jobName: string,
  result: CronRunResult,
): Promise<void> {
  try {
    const client = makeClient(adminToken);
    const rows = (await client.request(
      readItems('cron_monitor', {
        filter: { job_name: { _eq: jobName } },
        limit: 1,
      } as never),
    )) as DirectusCronMonitorRow[];
    const row = rows[0];
    if (!row) {
      console.error(
        `[calendars] recordCronRun: no cron_monitor row for ${jobName}`,
      );
      return;
    }
    await client.request(
      updateItem('cron_monitor', row.id, {
        last_run_at: new Date().toISOString(),
        last_result: JSON.stringify(result).slice(0, 1000),
      }),
    );
  } catch (e) {
    const msg =
      e instanceof Error ? e.message.slice(0, 200) : 'unknown';
    console.error(`[calendars] recordCronRun failed: ${msg}`);
  }
}

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

/**
 * Read events overlapping a date range. Used by the Context tab to
 * render the per-day Activiteiten list, and by the Today card.
 * Filters to events where start_at < toIso AND end_at > fromIso
 * (standard overlap check). Caller passes ISO strings — typically the
 * start-of-day and end-of-day for the selected date.
 */
export async function readCalendarEventsInRange(
  accessToken: string,
  fromIso: string,
  toIso: string,
): Promise<Result<DirectusCalendarEventRow[], CalendarsError>> {
  try {
    const rows = (await makeClient(accessToken).request(
      readItems('calendar_events', {
        filter: {
          _and: [
            { start_at: { _lt: toIso } },
            { end_at: { _gt: fromIso } },
          ],
        },
        limit: -1,
        sort: ['start_at'],
      } as never),
    )) as DirectusCalendarEventRow[];
    return { ok: true, value: rows };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

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

/**
 * Delete every event whose source_calendar_id is in `sourceCalendarIds`
 * for the given connection. Used by the choose-calendars POST when the
 * user removes calendars from the include list AND confirms they want
 * the existing events of those calendars removed. NULL source_calendar_id
 * (pre-v1.6.1 events) is NOT matched here; those are handled by a one-off
 * cleanup script, not by everyday exclude actions.
 *
 * Returns the count of rows deleted. Two-step (read ids, then deleteItems
 * one at a time) because the Directus SDK doesn't expose a filtered bulk
 * delete; the SDK's deleteItems takes an explicit id list.
 */
export async function deleteEventsBySourceCalendarIds(
  accessToken: string,
  connectionId: string,
  sourceCalendarIds: string[],
): Promise<Result<number, CalendarsError>> {
  if (sourceCalendarIds.length === 0) {
    return { ok: true, value: 0 };
  }
  try {
    const client = makeClient(accessToken);
    const rows = (await client.request(
      readItems('calendar_events', {
        filter: {
          _and: [
            { connection_id: { _eq: connectionId } },
            { source_calendar_id: { _in: sourceCalendarIds } },
          ],
        },
        fields: ['id'],
        limit: -1,
      } as never),
    )) as Array<{ id: string }>;
    if (rows.length === 0) {
      return { ok: true, value: 0 };
    }
    for (const r of rows) {
      await client.request(deleteItem('calendar_events', r.id));
    }
    return { ok: true, value: rows.length };
  } catch (e) {
    return { ok: false, error: classifyError(e) };
  }
}

/**
 * Count events per source_calendar_id for a connection. Used by the
 * choose-calendars GET so the form can show the user how many events
 * would be removed if they exclude a given calendar. NULL
 * source_calendar_id is folded into a single "(unknown)" bucket so the
 * total still matches the calendar_events row count.
 */
export async function countEventsBySourceCalendar(
  accessToken: string,
  connectionId: string,
): Promise<Result<Record<string, number>, CalendarsError>> {
  try {
    const rows = (await makeClient(accessToken).request(
      readItems('calendar_events', {
        filter: { connection_id: { _eq: connectionId } },
        fields: ['source_calendar_id'],
        limit: -1,
      } as never),
    )) as Array<{ source_calendar_id: string | null }>;
    const counts: Record<string, number> = {};
    for (const r of rows) {
      const key = r.source_calendar_id ?? '(unknown)';
      counts[key] = (counts[key] ?? 0) + 1;
    }
    return { ok: true, value: counts };
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
