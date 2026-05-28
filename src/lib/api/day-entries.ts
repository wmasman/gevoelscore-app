// Server-side SDK wrapper for the day_entries collection.
//
// Mirrors the shape of src/lib/auth/directus-auth.ts: stateless functions,
// fresh client per call, Result-shaped returns. Each function takes the
// access token explicitly (the route handler retrieves it via
// getValidatedSession).
//
// The wrapper flattens the Directus M2M response shape (nested `tags`
// objects with `tags_id` fields) into the domain `DayEntry.tag_ids` array,
// so callers see the domain type and never the Directus wire shape.

import { createDirectus, readItems, rest, staticToken } from '@directus/sdk';
import type { DayEntry } from '@/lib/domain/day-entry';

export type DayEntriesError = 'network_error' | 'directus_error';
export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

function directusUrl(): string {
  return (
    process.env.DIRECTUS_URL ??
    process.env.NEXT_PUBLIC_DIRECTUS_URL ??
    'http://localhost:8055'
  );
}

// Wire-shape schema for the SDK's generic type parameter. Tells `readItems`
// which collections exist and what they return. Drops the `as never` cast
// the audit flagged in src/lib/auth/directus-auth.ts — when more collections
// land, add them here.
type DirectusSchema = {
  day_entries: DirectusDayEntryRow[];
};

function createClient(accessToken: string) {
  return createDirectus<DirectusSchema>(directusUrl())
    .with(rest())
    .with(staticToken(accessToken));
}

function isNetworkError(e: unknown): boolean {
  return e instanceof TypeError && /fetch/i.test(e.message);
}

function mapError(e: unknown): DayEntriesError {
  if (isNetworkError(e)) return 'network_error';
  return 'directus_error';
}

// The Directus wire shape for a day_entries row, with `tags` expanded.
type DirectusDayEntryRow = {
  id: string;
  date: string;
  score: number;
  note: string | null;
  sub_scores: unknown;
  sleep_hours: number | null;
  special_event: string | null;
  garmin: unknown;
  health: unknown;
  weather: unknown;
  derived: unknown;
  created_at: string;
  updated_at: string;
  tags?: Array<{ tags_id: string }> | null;
};

// Fields requested from Directus. Includes `tags.tags_id` to surface the M2M
// tag IDs without dragging the full Tag object.
const DAY_ENTRY_FIELDS = ['*', 'tags.tags_id'] as const;

function flatten(row: DirectusDayEntryRow): DayEntry {
  return {
    date: row.date,
    score: row.score as DayEntry['score'],
    note: row.note,
    tag_ids: (row.tags ?? []).map((t) => t.tags_id),
    sub_scores: null,
    sleep_hours: row.sleep_hours,
    special_event: row.special_event,
    // M2M relations for projects + calendar are deferred until those features
    // ship; empty arrays satisfy the domain shape today.
    project_entry_ids: [],
    calendar_event_ids: [],
    garmin: null,
    health: null,
    weather: null,
    derived: null,
    created_at: row.created_at,
    updated_at: row.updated_at,
  };
}

export async function readDayEntryByDate(
  accessToken: string,
  date: string,
): Promise<Result<DayEntry | null, DayEntriesError>> {
  try {
    const client = createClient(accessToken);
    const rows = (await client.request(
      readItems('day_entries', {
        filter: { date: { _eq: date } },
        fields: [...DAY_ENTRY_FIELDS],
        limit: 1,
      }),
    )) as DirectusDayEntryRow[];
    if (rows.length === 0) return { ok: true, value: null };
    return { ok: true, value: flatten(rows[0]!) };
  } catch (e) {
    return { ok: false, error: mapError(e) };
  }
}

export async function readDayEntriesInRange(
  accessToken: string,
  from: string,
  to: string,
): Promise<Result<DayEntry[], DayEntriesError>> {
  try {
    const client = createClient(accessToken);
    const rows = (await client.request(
      readItems('day_entries', {
        // The SDK types `_gte`/`_lte`/`_between` as `never` for string-typed
        // fields (it assumes arbitrary strings, not ordered date strings).
        // The operators work at runtime; cast bypasses the over-narrow type.
        filter: {
          _and: [{ date: { _gte: from } }, { date: { _lte: to } }],
        } as never,
        fields: [...DAY_ENTRY_FIELDS],
        sort: ['date'],
        limit: -1,
      }),
    )) as DirectusDayEntryRow[];
    return { ok: true, value: rows.map(flatten) };
  } catch (e) {
    return { ok: false, error: mapError(e) };
  }
}
