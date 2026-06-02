// Server-side SDK wrapper for the tags collection. Mirrors the shape of
// day-entries.ts: stateless functions, fresh client per call, Result-shaped
// returns.
//
// Reads non-archived tags. The list is small (~83 seeded) and changes
// rarely; the server component fetches once per page render and threads
// them down through DayEntryEditor.

import {
  createDirectus,
  createItem,
  readItems,
  rest,
  staticToken,
  updateItem,
} from '@directus/sdk';
import type { Tag } from '@/lib/domain/tag';
import { validateTagCategory, type TagCategory } from '@/lib/domain/tag-category';
import { validateTagLabel } from '@/lib/domain/tag-label';

export type TagsError = 'network_error' | 'directus_error';
export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

function directusUrl(): string {
  return (
    process.env.DIRECTUS_URL ??
    process.env.NEXT_PUBLIC_DIRECTUS_URL ??
    'http://localhost:8055'
  );
}

type DirectusTagRow = {
  id: string;
  label: string;
  category: Tag['category'];
  project_id: string | null;
  parent_episode_id: string | null;
  usage_count: number;
  archived_at: string | null;
  created_at: string;
};

type DirectusSchema = {
  tags: DirectusTagRow[];
};

function isNetworkError(e: unknown): boolean {
  return e instanceof TypeError && /fetch/i.test(e.message);
}

export async function readAllTags(
  accessToken: string,
): Promise<Result<Tag[], TagsError>> {
  try {
    const client = createDirectus<DirectusSchema>(directusUrl())
      .with(rest())
      .with(staticToken(accessToken));

    const rows = (await client.request(
      readItems('tags', {
        filter: { archived_at: { _null: true } } as never,
        sort: ['category', 'label'],
        limit: -1,
      }),
    )) as DirectusTagRow[];

    return {
      ok: true,
      value: rows.map((r) => ({
        id: r.id,
        label: r.label,
        category: r.category,
        project_id: r.project_id,
        parent_episode_id: r.parent_episode_id,
        usage_count: r.usage_count,
        archived_at: r.archived_at,
        created_at: r.created_at,
      })),
    };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    return { ok: false, error: 'directus_error' };
  }
}

// -----------------------------------------------------------------------------
// createOrUpsertTag — inline tag creation feature (2026-06-01).
//
// One logical operation: "ensure a tag with this (label, category) exists and
// is active". Branches:
//   - exact case-insensitive match (within the category) on the trimmed label
//     and the row is active → return matched_active with the existing tag.
//   - same match but the row is archived → PATCH archived_at:null AND reset
//     project_id:null + usage_count:0 (B2 audit fix — stale columns from a
//     previous lifetime must not survive reactivation silently). Return
//     matched_reactivated.
//   - no match → POST a new tag with usage_count=0 and return created.
//
// Dedup query: Directus has no _iequals operator. The query uses
// _icontains (case-insensitive substring) as a coarse case-insensitive
// filter, then JS post-filters for exact equality on the lowercased
// trimmed label to reject substring false positives. Confirmed against
// the Directus filter-rules docs + the programmeerprobeer reference
// project (2026-06-01 hotfix; the earlier _iequals attempt returned
// HTTP 400 from Directus).
//
// TOCTOU note: this read-then-write pattern leaves a race window when two
// simultaneous calls with the same (category, label) arrive. For today's
// single-user app the race is functionally impossible. The DB-level fix
// is a unique index on (category, lower(trim(label))) — tracked in
// docs/audits/OPEN.md (see M1 from the 2026-06-01 step-1 audit).
// -----------------------------------------------------------------------------

const RESET_ON_REACTIVATE = {
  archived_at: null,
  project_id: null,
  usage_count: 0,
} as const;

export type CreateOrUpsertTagInput = {
  label: string;
  category: TagCategory;
};

export type CreateOrUpsertTagOutcome =
  | { kind: 'created'; tag: Tag }
  | { kind: 'matched_active'; tag: Tag }
  | { kind: 'matched_reactivated'; tag: Tag };

export type CreateOrUpsertTagError =
  | 'invalid_label'
  | 'invalid_category'
  | 'network_error'
  | 'directus_error';

function rowToTag(r: DirectusTagRow): Tag {
  return {
    id: r.id,
    label: r.label,
    category: r.category,
    project_id: r.project_id,
    parent_episode_id: r.parent_episode_id,
    usage_count: r.usage_count,
    archived_at: r.archived_at,
    created_at: r.created_at,
  };
}

export async function createOrUpsertTag(
  accessToken: string,
  input: CreateOrUpsertTagInput,
): Promise<Result<CreateOrUpsertTagOutcome, CreateOrUpsertTagError>> {
  const labelResult = validateTagLabel(input.label);
  if (!labelResult.ok) return { ok: false, error: 'invalid_label' };
  const categoryResult = validateTagCategory(input.category);
  if (!categoryResult.ok) return { ok: false, error: 'invalid_category' };

  const label = labelResult.value;
  const category = categoryResult.value;

  try {
    const client = createDirectus<DirectusSchema>(directusUrl())
      .with(rest())
      .with(staticToken(accessToken));

    // Directus has no _iequals operator (verified 2026-06-01: filtering by
    // _iequals returns HTTP 400). Use _icontains (case-insensitive substring)
    // as a coarse filter, then post-filter in JS for exact case-insensitive
    // equality on the trimmed label. The substring filter may surface false
    // positives (e.g. "pacing" matches "rapid-pacing"); the JS pass rejects
    // those. Limit is generous (50) so the exact match isn't paged off the
    // result by false positives — the tags collection is small (~83 rows).
    const lowerLabel = label.toLowerCase();
    const candidates = (await client.request(
      readItems('tags', {
        filter: {
          category: { _eq: category },
          label: { _icontains: label },
        } as never,
        limit: 50,
      }),
    )) as DirectusTagRow[];

    const match = candidates.find((r) => r.label.toLowerCase() === lowerLabel);
    if (match) {
      if (match.archived_at !== null) {
        const updated = (await client.request(
          updateItem('tags', match.id, RESET_ON_REACTIVATE),
        )) as DirectusTagRow;
        return { ok: true, value: { kind: 'matched_reactivated', tag: rowToTag(updated) } };
      }
      return { ok: true, value: { kind: 'matched_active', tag: rowToTag(match) } };
    }

    const created = (await client.request(
      createItem('tags', {
        label,
        category,
        project_id: null,
        usage_count: 0,
      } as never),
    )) as DirectusTagRow;
    return { ok: true, value: { kind: 'created', tag: rowToTag(created) } };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    return { ok: false, error: 'directus_error' };
  }
}
