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

import {
  createDirectus,
  createItem,
  createItems,
  deleteItems,
  readItems,
  rest,
  staticToken,
  updateItem,
} from '@directus/sdk';
import type { DayEntry } from '@/lib/domain/day-entry';

export type DayEntriesError =
  | 'network_error'
  | 'directus_error'
  | 'missing_score_for_create';
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
type DirectusJunctionRow = {
  id: string | number;
  day_entries_id: string;
  tags_id: string;
  source: string;
  confidence: number;
  confirmed_at: string;
};

type DirectusSchema = {
  day_entries: DirectusDayEntryRow[];
  day_entries_tags: DirectusJunctionRow[];
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

export type DayEntryPatch = {
  // Score is optional on update (NoteField + TagCategoryList save without
  // re-stating the score) but REQUIRED on create — see upsertDayEntry's
  // 'missing_score_for_create' branch. Route handlers should map that
  // error to 400 invalid_request.
  score?: DayEntry['score'];
  note?: string | null;
  tag_ids?: string[];
};

// Upsert a day_entry keyed by date. Three sub-operations:
//   1. Read existing row for the date (one query, expand tags so we can diff)
//   2. createItem OR updateItem on the day_entries collection
//   3. If patch.tag_ids supplied, sync the M2M junction (delete removed,
//      insert added) — preserves provenance columns for tags that don't
//      change. Patch omitting tag_ids leaves them untouched.
//   4. Re-read the canonical post-write shape so the caller has consistent
//      state including server-assigned updated_at.
//
// Reads twice (existing + final) because Directus PATCH/POST responses
// don't expand M2M relations by default. The cost is small (~10ms each on
// the internal Fly network) and the alternative (manual M2M expansion in
// the response wire-up) would duplicate the `tags.tags_id` expansion
// logic. Revisit if write latency becomes a UX concern.
export async function upsertDayEntry(
  accessToken: string,
  date: string,
  patch: DayEntryPatch,
): Promise<Result<DayEntry, DayEntriesError>> {
  try {
    const client = createClient(accessToken);

    // 1) Read existing row.
    type ExistingShape = { id: string; tags?: Array<{ tags_id: string }> | null };
    const existingRows = (await client.request(
      readItems('day_entries', {
        filter: { date: { _eq: date } },
        fields: ['id', 'tags.tags_id'],
        limit: 1,
      }),
    )) as ExistingShape[];

    let dayEntryId: string;
    let currentTagIds: string[];

    if (existingRows.length === 0) {
      // 2a) Create new row. Score is the only required column on
      // creation — without it the row is meaningless and the schema
      // rejects it. Note/tags can land on subsequent partial PUTs.
      if (patch.score === undefined) {
        return { ok: false, error: 'missing_score_for_create' };
      }
      const created = (await client.request(
        createItem('day_entries', { date, score: patch.score, note: patch.note ?? null }),
      )) as { id: string };
      dayEntryId = created.id;
      currentTagIds = [];
    } else {
      // 2b) Update existing row. Build the payload from whichever fields
      //     the patch actually carries — omit `score` if undefined,
      //     omit `note` if not in patch, etc. If the patch only touches
      //     M2M tags (handled at step 3) the update call is skipped
      //     entirely.
      dayEntryId = existingRows[0]!.id;
      currentTagIds = (existingRows[0]!.tags ?? []).map((t) => t.tags_id);
      const updatePayload: { score?: number; note?: string | null } = {};
      if (patch.score !== undefined) updatePayload.score = patch.score;
      if ('note' in patch) updatePayload.note = patch.note ?? null;
      if (Object.keys(updatePayload).length > 0) {
        await client.request(updateItem('day_entries', dayEntryId, updatePayload));
      }
    }

    // 3) M2M tag sync — only when patch.tag_ids supplied. Diff against
    // currentTagIds; delete removed junctions; insert new ones with
    // source='user' provenance.
    if (patch.tag_ids !== undefined) {
      const newTagIds = patch.tag_ids;
      const newSet = new Set(newTagIds);
      const currentSet = new Set(currentTagIds);
      const toAdd = newTagIds.filter((id) => !currentSet.has(id));
      const removed = currentTagIds.filter((id) => !newSet.has(id));

      if (removed.length > 0) {
        type JunctionLookup = { id: string | number; tags_id: string };
        const junctionRows = (await client.request(
          readItems('day_entries_tags', {
            // Filter operators on string fields are typed as `never` by the
            // SDK; cast to bypass. Runtime semantics are correct.
            filter: {
              _and: [
                { day_entries_id: { _eq: dayEntryId } },
                { tags_id: { _in: removed } },
              ],
            } as never,
            fields: ['id', 'tags_id'],
            limit: -1,
          }),
        )) as JunctionLookup[];
        const ids = junctionRows.map((r) => r.id);
        if (ids.length > 0) {
          await client.request(deleteItems('day_entries_tags', ids as never));
        }
      }

      if (toAdd.length > 0) {
        const nowIso = new Date().toISOString();
        await client.request(
          createItems(
            'day_entries_tags',
            toAdd.map((tagId) => ({
              day_entries_id: dayEntryId,
              tags_id: tagId,
              source: 'user',
              confidence: 1.0,
              confirmed_at: nowIso,
            })),
          ),
        );
      }
    }

    // 4) Re-read canonical post-write shape.
    const rows = (await client.request(
      readItems('day_entries', {
        filter: { date: { _eq: date } },
        fields: [...DAY_ENTRY_FIELDS],
        limit: 1,
      }),
    )) as DirectusDayEntryRow[];
    if (rows.length === 0) return { ok: false, error: 'directus_error' };
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
