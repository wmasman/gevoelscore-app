import { validateDateRange } from './date-range';
import { validateEpisodeCategory, type EpisodeCategory } from './episode-category';
import { validateEpisodeLabel } from './episode-label';
import { isIsoUtcTimestamp } from './iso-timestamp';

export type Episode = {
  id: string;
  label: string;
  category: EpisodeCategory;
  start_date: string;
  end_date: string | null;
  description: string | null;
  // v1.6 ships calendar binding via the event-side `calendar_events.linked_episode_id`
  // (Shape A in docs/features/calendar-binding/). This column is reserved for
  // v1.6.1 calendar-bound episodes (Shape B — promoting a recurring series to
  // an episode that auto-tracks it). Typed `unknown | null` for now and locked
  // to null in the validator until that feature ships.
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

  // v1.6 gate: calendar_binding must be null. The column is reserved for
  // v1.6.1 (Shape B calendar-bound episodes). v1.6 ships only Shape A
  // (event-side `calendar_events.linked_episode_id`); accepting a non-null
  // calendar_binding now would lock us in before v1.6.1 design lands.
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

