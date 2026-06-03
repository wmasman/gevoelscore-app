import { validateDate } from './date';
import { isIsoUtcTimestamp } from './iso-timestamp';
import { normalizeNote } from './note';
import { validateScore, type Score } from './score';
import { validateSleepHours } from './sleep-hours';
import { validateSubScores, type SubScores } from './sub-score';
import { validateTagIds } from './tag-ids';

export type DayEntry = {
  date: string;
  score: Score;
  note: string | null;
  tag_ids: string[];
  sub_scores: SubScores | null;
  sleep_hours: number | null;
  special_event: string | null;
  project_entry_ids: string[];
  calendar_event_ids: string[];
  // v2 fields — present in the type but constrained to null in v1.
  // When v2 lands these widen to their populated shapes.
  garmin: null;
  health: null;
  weather: null;
  derived: null;
  created_at: string;
  updated_at: string;
};

export type DayEntryError =
  | 'invalid_shape'
  | 'invalid_date'
  | 'invalid_score'
  | 'invalid_note'
  | 'invalid_tag_ids'
  | 'invalid_sub_scores'
  | 'invalid_sleep_hours'
  | 'invalid_special_event'
  | 'invalid_project_entry_ids'
  | 'invalid_calendar_event_ids'
  | 'invalid_v2_field'
  | 'invalid_created_at'
  | 'invalid_updated_at'
  | 'invalid_timestamp_order';

export type ValidateDayEntryResult =
  | { ok: true; value: DayEntry }
  | { ok: false; error: DayEntryError };

const REQUIRED_KEYS = [
  'calendar_event_ids',
  'created_at',
  'date',
  'derived',
  'garmin',
  'health',
  'note',
  'project_entry_ids',
  'score',
  'sleep_hours',
  'special_event',
  'sub_scores',
  'tag_ids',
  'updated_at',
  'weather',
] as const;

export function validateDayEntry(input: unknown): ValidateDayEntryResult {
  // Shape: must be a plain object with exactly the required keys.
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

  const dateResult = validateDate(obj.date);
  if (!dateResult.ok) return { ok: false, error: 'invalid_date' };

  const scoreResult = validateScore(obj.score);
  if (!scoreResult.ok) return { ok: false, error: 'invalid_score' };

  const noteResult = normalizeNote(obj.note);
  if (!noteResult.ok) return { ok: false, error: 'invalid_note' };

  const tagIdsResult = validateTagIds(obj.tag_ids);
  if (!tagIdsResult.ok) return { ok: false, error: 'invalid_tag_ids' };

  const subScoresResult = validateSubScores(obj.sub_scores);
  if (!subScoresResult.ok) return { ok: false, error: 'invalid_sub_scores' };

  const sleepHoursResult = validateSleepHours(obj.sleep_hours);
  if (!sleepHoursResult.ok) return { ok: false, error: 'invalid_sleep_hours' };

  if (obj.special_event !== null && typeof obj.special_event !== 'string') {
    return { ok: false, error: 'invalid_special_event' };
  }

  // project_entry_ids and calendar_event_ids have the same shape as tag_ids:
  // array of unique strings. Reusing the validator keeps the rules in one place.
  const projectIdsResult = validateTagIds(obj.project_entry_ids);
  if (!projectIdsResult.ok) {
    return { ok: false, error: 'invalid_project_entry_ids' };
  }

  const calendarIdsResult = validateTagIds(obj.calendar_event_ids);
  if (!calendarIdsResult.ok) {
    return { ok: false, error: 'invalid_calendar_event_ids' };
  }

  // v2 fields must be null in v1. When v2 lands, replace with deep validators.
  if (
    obj.garmin !== null ||
    obj.health !== null ||
    obj.weather !== null ||
    obj.derived !== null
  ) {
    return { ok: false, error: 'invalid_v2_field' };
  }

  if (!isIsoUtcTimestamp(obj.created_at)) {
    return { ok: false, error: 'invalid_created_at' };
  }
  if (!isIsoUtcTimestamp(obj.updated_at)) {
    return { ok: false, error: 'invalid_updated_at' };
  }
  // Lexicographic string comparison is calendar-correct for ISO 8601 UTC.
  if (obj.created_at > obj.updated_at) {
    return { ok: false, error: 'invalid_timestamp_order' };
  }

  return {
    ok: true,
    value: {
      date: dateResult.value,
      score: scoreResult.value,
      note: noteResult.value,
      tag_ids: tagIdsResult.value,
      sub_scores: subScoresResult.value,
      sleep_hours: sleepHoursResult.value,
      special_event: obj.special_event,
      project_entry_ids: projectIdsResult.value,
      calendar_event_ids: calendarIdsResult.value,
      garmin: null,
      health: null,
      weather: null,
      derived: null,
      created_at: obj.created_at,
      updated_at: obj.updated_at,
    },
  };
}

