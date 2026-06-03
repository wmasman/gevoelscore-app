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
  deleteItem,
  readItem,
  readItems,
  rest,
  staticToken,
  updateItem,
} from '@directus/sdk';
import { isIsoUtcTimestamp } from '@/lib/domain/iso-timestamp';
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
  opts: { includeArchived?: boolean } = {},
): Promise<Result<Tag[], TagsError>> {
  try {
    const client = createDirectus<DirectusSchema>(directusUrl())
      .with(rest())
      .with(staticToken(accessToken));

    // includeArchived defaults to false to preserve the existing daily-
    // flow contract (the picker / today-card / timeline never see
    // archived tags). The Settings → Tag-beheer surface opts in so the
    // "Toon gearchiveerd" toggle actually has something to surface.
    const query: { filter?: unknown; sort: string[]; limit: number } = {
      sort: ['category', 'label'],
      limit: -1,
    };
    if (!opts.includeArchived) {
      query.filter = { archived_at: { _null: true } };
    }
    const rows = (await client.request(
      readItems('tags', query as never),
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
// updateTag — PATCH wrapper.
//
// Step-5 (2026-06-02): single key, parent_episode_id, for the picker's
// re-link / unlink paths.
//
// Step v1.5b (2026-06-03): extended to also accept label, category,
// archived_at — for the Settings → Tag-beheer surface (rename /
// recategorize / archive / un-archive). Per-field validation surfaces
// distinct error variants (invalid_label / invalid_category /
// invalid_archived_at / invalid_parent_episode_id) so the UI can show
// the user which field is wrong. The invalid_patch variant is reserved
// for shape-level violations (empty body, unknown key, non-object).
// ---------------------------------------------------------------------------

export type UpdateTagPatch = {
  label?: string;
  category?: TagCategory;
  archived_at?: string | null;
  parent_episode_id?: string | null;
};

export type UpdateTagError =
  | TagsError
  | 'invalid_patch'
  | 'invalid_label'
  | 'invalid_category'
  | 'invalid_archived_at'
  | 'invalid_parent_episode_id';

const ALLOWED_PATCH_KEYS = new Set([
  'label',
  'category',
  'archived_at',
  'parent_episode_id',
]);

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

  // Per-field validation. Each runs only if the key is present in the
  // patch (the form sends only changed keys, so an absent key means "no
  // change"). The output is the wire-body — we re-build it field by
  // field rather than spreading the input directly so the validated /
  // normalised values land in Directus.
  const wireBody: Record<string, unknown> = {};

  if ('label' in patch) {
    const labelResult = validateTagLabel(patch.label);
    if (!labelResult.ok) return { ok: false, error: 'invalid_label' };
    wireBody.label = labelResult.value;
  }
  if ('category' in patch) {
    const categoryResult = validateTagCategory(patch.category);
    if (!categoryResult.ok) return { ok: false, error: 'invalid_category' };
    wireBody.category = categoryResult.value;
  }
  if ('archived_at' in patch) {
    if (patch.archived_at === null) {
      wireBody.archived_at = null;
    } else if (isIsoUtcTimestamp(patch.archived_at)) {
      wireBody.archived_at = patch.archived_at;
    } else {
      return { ok: false, error: 'invalid_archived_at' };
    }
  }
  if ('parent_episode_id' in patch) {
    const parentResult = validateParentEpisodeId(patch.parent_episode_id);
    if (!parentResult.ok) {
      return { ok: false, error: 'invalid_parent_episode_id' };
    }
    wireBody.parent_episode_id = parentResult.value;
  }

  try {
    const client = createDirectus<DirectusSchema>(directusUrl())
      .with(rest())
      .with(staticToken(accessToken));

    const updated = (await client.request(
      updateItem('tags', id, wireBody as never),
    )) as DirectusTagRow;
    return { ok: true, value: rowToTag(updated) };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    return { ok: false, error: 'directus_error' };
  }
}

// ---------------------------------------------------------------------------
// deleteTag — step v1.5b hard-delete wrapper.
//
// Does NOT itself gate by usage_count — the route handler enforces that
// rule (read-then-delete with a logical-FK guard against
// day_entries.tag_ids[]). The lib stays single-purpose: it forwards the
// DELETE to Directus and maps the Result variant.
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// readTagById — step v1.5b targeted single-row read.
//
// Used by the DELETE /api/tags/[id] route to gate hard-delete by
// usage_count === 0 BEFORE issuing the Directus delete. Returns the
// full Tag (not just usage_count) so the route can include the count
// in the 400 tag_in_use response.
// ---------------------------------------------------------------------------

export async function readTagById(
  accessToken: string,
  id: string,
): Promise<Result<Tag, TagsError>> {
  try {
    const client = createDirectus<DirectusSchema>(directusUrl())
      .with(rest())
      .with(staticToken(accessToken));

    const row = (await client.request(readItem('tags', id))) as DirectusTagRow;
    return { ok: true, value: rowToTag(row) };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    return { ok: false, error: 'directus_error' };
  }
}

export async function deleteTag(
  accessToken: string,
  id: string,
): Promise<Result<{ deleted_id: string }, TagsError>> {
  try {
    const client = createDirectus<DirectusSchema>(directusUrl())
      .with(rest())
      .with(staticToken(accessToken));

    await client.request(deleteItem('tags', id));
    return { ok: true, value: { deleted_id: id } };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    return { ok: false, error: 'directus_error' };
  }
}
