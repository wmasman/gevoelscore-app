// Validate an ISO YYYY-MM-DD pair where start is required and end is
// optional. When end is provided it must be >= start. No timezone
// assumptions — these are calendar dates, not timestamps.

const ISO_DATE_REGEX = /^\d{4}-\d{2}-\d{2}$/;

export type DateRangeError =
  | 'invalid_start_date'
  | 'invalid_end_date'
  | 'end_before_start';

export type ValidateDateRangeResult =
  | { ok: true; value: { start_date: string; end_date: string | null } }
  | { ok: false; error: DateRangeError };

export function validateDateRange(
  start: unknown,
  end: unknown,
): ValidateDateRangeResult {
  if (!isIsoDate(start)) {
    return { ok: false, error: 'invalid_start_date' };
  }
  if (end !== null) {
    if (!isIsoDate(end)) {
      return { ok: false, error: 'invalid_end_date' };
    }
    if (end < start) {
      return { ok: false, error: 'end_before_start' };
    }
  }
  return { ok: true, value: { start_date: start, end_date: end as string | null } };
}

function isIsoDate(input: unknown): input is string {
  if (typeof input !== 'string') return false;
  if (!ISO_DATE_REGEX.test(input)) return false;
  // Reject calendar-invalid dates like 2026-02-30 by round-tripping
  // through the Date parser: a date that doesn't exist will normalise
  // to a different YYYY-MM-DD on re-emit.
  const parsed = new Date(`${input}T00:00:00Z`);
  if (Number.isNaN(parsed.getTime())) return false;
  const reEmit = parsed.toISOString().slice(0, 10);
  return reEmit === input;
}
