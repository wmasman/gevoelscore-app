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
import { validateParentEpisodeId } from '@/lib/domain/parent-episode-id';
import { validateTagCategory, type TagCategory } from '@/lib/domain/tag-category';
import { validateTagLabel } from '@/lib/domain/tag-label';
import type { Result } from './result';

export type TagsError = 'network_error' | 'directus_error';

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
  // Step-5: optional. When omitted → existing daily-flow semantics
  // (tag created unlinked). When provided → validated through
  // validateParentEpisodeId; null = unlinked, UUID = linked. In the
  // matched_active branch the value is also enforced via an extra PATCH
  // if it differs; in matched_reactivated it's folded into the single
  // reactivation PATCH body.
  parent_episode_id?: string | null;
};

export type CreateOrUpsertTagOutcome =
  | { kind: 'created'; tag: Tag }
  | { kind: 'matched_active'; tag: Tag }
  | { kind: 'matched_reactivated'; tag: Tag };

export type CreateOrUpsertTagError =
  | 'invalid_label'
  | 'invalid_category'
  | 'invalid_parent_episode_id'
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

  // Parent is opt-in. Only validate when the caller explicitly passed it
  // (including null, which means "set to null"). `undefined` means "leave
  // alone" — the existing daily-flow contract.
  const hasParentInput = Object.prototype.hasOwnProperty.call(
    input,
    'parent_episode_id',
  );
  let parentEpisodeId: string | null | undefined = undefined;
  if (hasParentInput) {
    const parentResult = validateParentEpisodeId(input.parent_episode_id);
    if (!parentResult.ok) {
      return { ok: false, error: 'invalid_parent_episode_id' };
    }
    parentEpisodeId = parentResult.value;
  }

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
        // Reactivation: fold parent_episode_id into the single PATCH body
        // if the caller provided it, so we don't double-round-trip. When
        // omitted, parent_episode_id is preserved as-is from the archived row.
        const reactivatePatch =
          parentEpisodeId !== undefined
            ? { ...RESET_ON_REACTIVATE, parent_episode_id: parentEpisodeId }
            : RESET_ON_REACTIVATE;
        const updated = (await client.request(
          updateItem('tags', match.id, reactivatePatch),
        )) as DirectusTagRow;
        return {
          ok: true,
          value: { kind: 'matched_reactivated', tag: rowToTag(updated) },
        };
      }
      // matched_active: if caller supplied parent_episode_id and it differs,
      // PATCH the parent into place. Idempotent — equal values skip the wire.
      if (
        parentEpisodeId !== undefined &&
        parentEpisodeId !== match.parent_episode_id
      ) {
        const updated = (await client.request(
          updateItem('tags', match.id, {
            parent_episode_id: parentEpisodeId,
          }),
        )) as DirectusTagRow;
        return {
          ok: true,
          value: { kind: 'matched_active', tag: rowToTag(updated) },
        };
      }
      return { ok: true, value: { kind: 'matched_active', tag: rowToTag(match) } };
    }

    // Create branch — include parent_episode_id in the POST body only when
    // explicitly provided. Omission preserves the existing daily-flow wire
    // contract (no behavioural change to the inline-tag-creation path).
    const createBody: Record<string, unknown> = {
      label,
      category,
      project_id: null,
      usage_count: 0,
    };
    if (parentEpisodeId !== undefined) {
      createBody.parent_episode_id = parentEpisodeId;
    }
    const created = (await client.request(
      createItem('tags', createBody as never),
    )) as DirectusTagRow;
    return { ok: true, value: { kind: 'created', tag: rowToTag(created) } };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    return { ok: false, error: 'directus_error' };
  }
}

// ---------------------------------------------------------------------------
// updateTag — step-5 PATCH wrapper. Handles the picker's re-link and unlink
// paths. v1.5 patch surface is intentionally tight: only parent_episode_id.
// Any unknown key returns 'invalid_patch' before any wire call so a future
// regression that adds a stray field can't silently leak to Directus.
// ---------------------------------------------------------------------------

export type UpdateTagPatch = {
  parent_episode_id: string | null;
};

export type UpdateTagError = TagsError | 'invalid_patch';

const ALLOWED_PATCH_KEYS = new Set(['parent_episode_id']);

export async function updateTag(
  accessToken: string,
  id: string,
  patch: UpdateTagPatch,
): Promise<Result<Tag, UpdateTagError>> {
  if (typeof patch !== 'object' || patch === null || Array.isArray(patch)) {
    return { ok: false, error: 'invalid_patch' };
  }
  const keys = Object.keys(patch);
  if (keys.length === 0) {
    return { ok: false, error: 'invalid_patch' };
  }
  for (const key of keys) {
    if (!ALLOWED_PATCH_KEYS.has(key)) {
      return { ok: false, error: 'invalid_patch' };
    }
  }
  const parentResult = validateParentEpisodeId(patch.parent_episode_id);
  if (!parentResult.ok) {
    return { ok: false, error: 'invalid_patch' };
  }

  try {
    const client = createDirectus<DirectusSchema>(directusUrl())
      .with(rest())
      .with(staticToken(accessToken));

    const updated = (await client.request(
      updateItem('tags', id, { parent_episode_id: parentResult.value }),
    )) as DirectusTagRow;
    return { ok: true, value: rowToTag(updated) };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    return { ok: false, error: 'directus_error' };
  }
}
