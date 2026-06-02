import { validateTagCategory, type TagCategory } from './tag-category';
import { validateTagLabel } from './tag-label';

export type Tag = {
  id: string;
  label: string;
  category: TagCategory;
  project_id: string | null;
  // v1.5: optional FK to episodes.id. When set, this tag is an
  // "occurrence" of that episode on the day it appears in a day_entry.
  // ON DELETE SET NULL at the DB level — if the episode is hard-deleted
  // (Directus admin only), referencing tags revert to standalone.
  parent_episode_id: string | null;
  usage_count: number;
  archived_at: string | null;
  created_at: string;
};

export type TagError =
  | 'invalid_shape'
  | 'invalid_id'
  | 'invalid_label'
  | 'invalid_category'
  | 'missing_project_id'
  | 'unexpected_project_id'
  | 'invalid_project_id'
  | 'invalid_parent_episode_id'
  | 'invalid_usage_count'
  | 'invalid_archived_at'
  | 'invalid_created_at';

export type ValidateTagResult =
  | { ok: true; value: Tag }
  | { ok: false; error: TagError };

const REQUIRED_KEYS = [
  'archived_at',
  'category',
  'created_at',
  'id',
  'label',
  'parent_episode_id',
  'project_id',
  'usage_count',
] as const;

// Inline copy of day-entry.ts's regex. When a third caller needs this, extract
// to src/lib/domain/iso-timestamp.ts; until then per the 3+ rule keep it local.
const ISO_UTC_TIMESTAMP_REGEX =
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;

export function validateTag(input: unknown): ValidateTagResult {
  if (input === null || typeof input !== 'object' || Array.isArray(input)) {
    return { ok: false, error: 'invalid_shape' };
  }
  const obj = input as Record<string, unknown>;
  const actualKeys = Object.keys(obj).sort();
  if (
    actualKeys.length !== REQUIRED_KEYS.length ||
    !actualKeys.every((k, i) => k === REQUIRED_KEYS[i])
  ) {
    return { ok: false, error: 'invalid_shape' };
  }

  if (typeof obj.id !== 'string' || obj.id.length === 0) {
    return { ok: false, error: 'invalid_id' };
  }

  const labelResult = validateTagLabel(obj.label);
  if (!labelResult.ok) return { ok: false, error: 'invalid_label' };

  const categoryResult = validateTagCategory(obj.category);
  if (!categoryResult.ok) return { ok: false, error: 'invalid_category' };
  const category = categoryResult.value;

  if (category === 'project') {
    if (obj.project_id === null) {
      return { ok: false, error: 'missing_project_id' };
    }
    if (typeof obj.project_id !== 'string' || obj.project_id.length === 0) {
      return { ok: false, error: 'invalid_project_id' };
    }
  } else if (obj.project_id !== null) {
    return { ok: false, error: 'unexpected_project_id' };
  }

  if (obj.parent_episode_id !== null) {
    if (
      typeof obj.parent_episode_id !== 'string' ||
      obj.parent_episode_id.length === 0
    ) {
      return { ok: false, error: 'invalid_parent_episode_id' };
    }
  }

  if (
    typeof obj.usage_count !== 'number' ||
    Number.isNaN(obj.usage_count) ||
    !Number.isInteger(obj.usage_count) ||
    obj.usage_count < 0
  ) {
    return { ok: false, error: 'invalid_usage_count' };
  }

  if (obj.archived_at !== null && !isIsoUtcTimestamp(obj.archived_at)) {
    return { ok: false, error: 'invalid_archived_at' };
  }

  if (!isIsoUtcTimestamp(obj.created_at)) {
    return { ok: false, error: 'invalid_created_at' };
  }

  return {
    ok: true,
    value: {
      id: obj.id,
      label: labelResult.value,
      category,
      project_id: obj.project_id as string | null,
      parent_episode_id: obj.parent_episode_id as string | null,
      usage_count: obj.usage_count,
      archived_at: obj.archived_at as string | null,
      created_at: obj.created_at,
    },
  };
}

function isIsoUtcTimestamp(input: unknown): input is string {
  if (typeof input !== 'string') return false;
  if (!ISO_UTC_TIMESTAMP_REGEX.test(input)) return false;
  const parsed = new Date(input);
  return !Number.isNaN(parsed.getTime());
}
