// Server-side SDK wrapper for the tags collection. Mirrors the shape of
// day-entries.ts: stateless functions, fresh client per call, Result-shaped
// returns.
//
// Reads non-archived tags. The list is small (~83 seeded) and changes
// rarely; the server component fetches once per page render and threads
// them down through DayEntryEditor.

import { createDirectus, readItems, rest, staticToken } from '@directus/sdk';
import type { Tag } from '@/lib/domain/tag';

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
