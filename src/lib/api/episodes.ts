// Server-side SDK wrapper for the episodes collection (v1.5
// verloop-and-episodes feature, user-facing tab: Periodes).
//
// Mirrors the shape of tags.ts and day-entries.ts: stateless functions,
// fresh client per call, Result-shaped returns. Each function takes the
// access token explicitly (the route handler retrieves it via
// getValidatedSession).
//
// Validation is done at this boundary by the pure domain validators
// (validateEpisodeLabel, validateEpisodeCategory, validateDateRange,
// validateEpisodeDescription). The route handler does a coarse shape
// check (typeof body.label === 'string'); this wrapper is the strict
// gate.
//
// PATCH semantics: true partial-PATCH. If either start_date OR
// end_date is in the patch, the wrapper reads the current row, fills
// in the absent half, validates the merged pair, and PATCHes ONLY
// the keys the caller provided. Trade-off + TOCTOU window documented
// in docs/features/verloop-and-episodes/step-2-episodes-api.md.

import {
  createDirectus,
  readItems,
  createItem,
  updateItem,
  rest,
  staticToken,
} from '@directus/sdk';
import { validateDateRange } from '@/lib/domain/date-range';
import { validateEpisodeCategory, type EpisodeCategory } from '@/lib/domain/episode-category';
import { validateEpisodeDescription } from '@/lib/domain/episode-description';
import { validateEpisodeLabel } from '@/lib/domain/episode-label';
import type { Episode } from '@/lib/domain/episode';
import type { Result } from './result';

export type EpisodesError = 'network_error' | 'directus_error';

export type CreateEpisodeError =
  | 'invalid_label'
  | 'invalid_category'
  | 'invalid_date_range'
  | 'invalid_description'
  | 'network_error'
  | 'directus_error';

export type UpdateEpisodeError =
  | CreateEpisodeError
  | 'invalid_archived_at'
  | 'not_found'
  | 'empty_patch';

export type CreateEpisodeInput = {
  label: string;
  category: EpisodeCategory;
  start_date: string;
  end_date?: string | null;
  description?: string | null;
};

export type UpdateEpisodePatch = {
  label?: string;
  category?: EpisodeCategory;
  start_date?: string;
  end_date?: string | null;
  description?: string | null;
  archived_at?: string | null;
};

type DirectusEpisodeRow = {
  id: string;
  label: string;
  category: EpisodeCategory;
  start_date: string;
  end_date: string | null;
  description: string | null;
  calendar_binding: unknown | null;
  archived_at: string | null;
  created_at: string;
  updated_at: string;
};

type DirectusSchema = { episodes: DirectusEpisodeRow[] };

const ISO_UTC_TIMESTAMP_REGEX =
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;

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

function isNotFoundError(e: unknown): boolean {
  const msg = String((e as { message?: string }).message ?? '');
  return msg.includes('404') || msg.includes('FORBIDDEN');
}

function rowToEpisode(r: DirectusEpisodeRow): Episode {
  // Force calendar_binding to null per the v1.5 gate. The schema column
  // is reserved for v1.6 calendar binding; until then any non-null value
  // is forbidden. We normalise here so the domain layer never sees a
  // non-null calendar_binding from a stray Directus admin write.
  return {
    id: r.id,
    label: r.label,
    category: r.category,
    start_date: r.start_date,
    end_date: r.end_date,
    description: r.description,
    calendar_binding: null,
    archived_at: r.archived_at,
    created_at: r.created_at,
    updated_at: r.updated_at,
  };
}

function makeClient(accessToken: string) {
  return createDirectus<DirectusSchema>(directusUrl())
    .with(rest())
    .with(staticToken(accessToken));
}

// ---------------------------------------------------------------------------
// readAllEpisodes — list with optional includeArchived filter
// ---------------------------------------------------------------------------

export async function readAllEpisodes(
  accessToken: string,
  opts: { includeArchived?: boolean } = {},
): Promise<Result<Episode[], EpisodesError>> {
  try {
    const client = makeClient(accessToken);

    const query: { filter?: unknown; sort: string[]; limit: number } = {
      sort: ['-start_date'],
      limit: -1,
    };
    if (!opts.includeArchived) {
      query.filter = { archived_at: { _null: true } };
    }

    const rows = (await client.request(
      readItems('episodes', query as never),
    )) as DirectusEpisodeRow[];

    return { ok: true, value: rows.map(rowToEpisode) };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    return { ok: false, error: 'directus_error' };
  }
}

// ---------------------------------------------------------------------------
// createEpisode — validates then POSTs
// ---------------------------------------------------------------------------

export async function createEpisode(
  accessToken: string,
  input: CreateEpisodeInput,
): Promise<Result<Episode, CreateEpisodeError>> {
  const labelResult = validateEpisodeLabel(input.label);
  if (!labelResult.ok) return { ok: false, error: 'invalid_label' };

  const categoryResult = validateEpisodeCategory(input.category);
  if (!categoryResult.ok) return { ok: false, error: 'invalid_category' };

  const rangeResult = validateDateRange(input.start_date, input.end_date ?? null);
  if (!rangeResult.ok) return { ok: false, error: 'invalid_date_range' };

  const descResult = validateEpisodeDescription(input.description ?? null);
  if (!descResult.ok) return { ok: false, error: 'invalid_description' };

  try {
    const client = makeClient(accessToken);
    const row = (await client.request(
      createItem('episodes', {
        label: labelResult.value,
        category: categoryResult.value,
        start_date: rangeResult.value.start_date,
        end_date: rangeResult.value.end_date,
        description: descResult.value,
      } as never),
    )) as DirectusEpisodeRow;

    return { ok: true, value: rowToEpisode(row) };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    return { ok: false, error: 'directus_error' };
  }
}

// ---------------------------------------------------------------------------
// updateEpisode — partial PATCH with fetch-then-validate for date ranges
// ---------------------------------------------------------------------------

export async function updateEpisode(
  accessToken: string,
  id: string,
  patch: UpdateEpisodePatch,
): Promise<Result<Episode, UpdateEpisodeError>> {
  // Empty patch is a no-op and gets rejected at the boundary so the
  // write path can assume there's something to write.
  const patchKeys = Object.keys(patch);
  if (patchKeys.length === 0) return { ok: false, error: 'empty_patch' };

  const cleaned: Record<string, unknown> = {};

  if ('label' in patch) {
    const r = validateEpisodeLabel(patch.label);
    if (!r.ok) return { ok: false, error: 'invalid_label' };
    cleaned.label = r.value;
  }

  if ('category' in patch) {
    const r = validateEpisodeCategory(patch.category);
    if (!r.ok) return { ok: false, error: 'invalid_category' };
    cleaned.category = r.value;
  }

  if ('description' in patch) {
    const r = validateEpisodeDescription(patch.description);
    if (!r.ok) return { ok: false, error: 'invalid_description' };
    cleaned.description = r.value;
  }

  if ('archived_at' in patch) {
    // archived_at: null = un-archive. ISO timestamp = archive. Anything
    // else (including the explicit `undefined`) is wrong-type.
    if (patch.archived_at !== null) {
      if (
        typeof patch.archived_at !== 'string' ||
        !ISO_UTC_TIMESTAMP_REGEX.test(patch.archived_at)
      ) {
        return { ok: false, error: 'invalid_archived_at' };
      }
    }
    cleaned.archived_at = patch.archived_at;
  }

  // Date-range branch: if either start_date or end_date is in the patch,
  // we MUST validate against the merged candidate (caller value + DB
  // value for the absent half). True PATCH semantics. The read is purely
  // for validation; the PATCH itself only carries the caller-supplied
  // keys. See step-2 plan §Technical constraints for the TOCTOU caveat.
  if ('start_date' in patch || 'end_date' in patch) {
    let currentRow: DirectusEpisodeRow | undefined;
    try {
      const readClient = makeClient(accessToken);
      const rows = (await readClient.request(
        readItems('episodes', {
          filter: { id: { _eq: id } } as never,
          limit: 1,
        }),
      )) as DirectusEpisodeRow[];
      currentRow = rows[0];
    } catch (e) {
      if (isNetworkError(e)) return { ok: false, error: 'network_error' };
      if (isNotFoundError(e)) return { ok: false, error: 'not_found' };
      return { ok: false, error: 'directus_error' };
    }
    if (!currentRow) return { ok: false, error: 'not_found' };

    const candidateStart =
      'start_date' in patch ? patch.start_date : currentRow.start_date;
    const candidateEnd =
      'end_date' in patch ? (patch.end_date ?? null) : currentRow.end_date;

    const r = validateDateRange(candidateStart, candidateEnd);
    if (!r.ok) return { ok: false, error: 'invalid_date_range' };

    // Only echo back the keys the CALLER sent — don't overwrite the
    // absent half with the value we read.
    if ('start_date' in patch) cleaned.start_date = r.value.start_date;
    if ('end_date' in patch) cleaned.end_date = r.value.end_date;
  }

  // Write phase.
  try {
    const client = makeClient(accessToken);
    const row = (await client.request(
      updateItem('episodes', id, cleaned as never),
    )) as DirectusEpisodeRow;

    return { ok: true, value: rowToEpisode(row) };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    if (isNotFoundError(e)) return { ok: false, error: 'not_found' };
    return { ok: false, error: 'directus_error' };
  }
}
