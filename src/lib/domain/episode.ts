import { validateDateRange } from './date-range';
import { validateEpisodeCategory, type EpisodeCategory } from './episode-category';
import { validateEpisodeLabel } from './episode-label';

export type Episode = {
  id: string;
  label: string;
  category: EpisodeCategory;
  start_date: string;
  end_date: string | null;
  description: string | null;
  // v1.5: always null. The column exists for v1.6 calendar binding;
  // typed `unknown | null` for now and locked to null in the validator.
  calendar_binding: unknown | null;
  archived_at: string | null;
  created_at: string;
  updated_at: string;
};

export type EpisodeError =
  | 'invalid_shape'
  | 'invalid_id'
  | 'invalid_label'
  | 'invalid_category'
  | 'invalid_date_range'
  | 'invalid_description'
  | 'invalid_calendar_binding'
  | 'invalid_archived_at'
  | 'invalid_created_at'
  | 'invalid_updated_at';

export type ValidateEpisodeResult =
  | { ok: true; value: Episode }
  | { ok: false; error: EpisodeError };

const REQUIRED_KEYS = [
  'archived_at',
  'calendar_binding',
  'category',
  'created_at',
  'description',
  'end_date',
  'id',
  'label',
  'start_date',
  'updated_at',
] as const;

// Inline copy of day-entry/tag.ts's regex. Extract to a shared module
// when a fourth caller appears (3+ rule). Until then, local.
const ISO_UTC_TIMESTAMP_REGEX =
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;

export function validateEpisode(input: unknown): ValidateEpisodeResult {
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

  const labelResult = validateEpisodeLabel(obj.label);
  if (!labelResult.ok) return { ok: false, error: 'invalid_label' };

  const categoryResult = validateEpisodeCategory(obj.category);
  if (!categoryResult.ok) return { ok: false, error: 'invalid_category' };

  const rangeResult = validateDateRange(obj.start_date, obj.end_date);
  if (!rangeResult.ok) return { ok: false, error: 'invalid_date_range' };

  if (obj.description !== null && typeof obj.description !== 'string') {
    return { ok: false, error: 'invalid_description' };
  }

  // v1.5 gate: calendar_binding must be null. The column exists for
  // v1.6 but accepting any non-null shape now would lock us in before
  // that design lands.
  if (obj.calendar_binding !== null) {
    return { ok: false, error: 'invalid_calendar_binding' };
  }

  if (obj.archived_at !== null && !isIsoUtcTimestamp(obj.archived_at)) {
    return { ok: false, error: 'invalid_archived_at' };
  }
  if (!isIsoUtcTimestamp(obj.created_at)) {
    return { ok: false, error: 'invalid_created_at' };
  }
  if (!isIsoUtcTimestamp(obj.updated_at)) {
    return { ok: false, error: 'invalid_updated_at' };
  }

  return {
    ok: true,
    value: {
      id: obj.id,
      label: labelResult.value,
      category: categoryResult.value,
      start_date: rangeResult.value.start_date,
      end_date: rangeResult.value.end_date,
      description: obj.description as string | null,
      calendar_binding: null,
      archived_at: obj.archived_at as string | null,
      created_at: obj.created_at,
      updated_at: obj.updated_at,
    },
  };
}

function isIsoUtcTimestamp(input: unknown): input is string {
  if (typeof input !== 'string') return false;
  if (!ISO_UTC_TIMESTAMP_REGEX.test(input)) return false;
  const parsed = new Date(input);
  return !Number.isNaN(parsed.getTime());
}
