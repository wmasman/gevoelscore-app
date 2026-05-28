export type DateError =
  | 'wrong_type'
  | 'invalid_format'
  | 'invalid_calendar_date'
  | 'future_date';

export type ValidateDateResult =
  | { ok: true; value: string }
  | { ok: false; error: DateError };

const ISO_DATE_REGEX = /^\d{4}-\d{2}-\d{2}$/;

export function validateDate(input: unknown): ValidateDateResult {
  if (typeof input !== 'string') {
    return { ok: false, error: 'wrong_type' };
  }
  if (!ISO_DATE_REGEX.test(input)) {
    return { ok: false, error: 'invalid_format' };
  }
  // Parse the segments. Regex guarantees fixed positions so substring is safe
  // (and avoids the `noUncheckedIndexedAccess` friction of array destructuring).
  const year = Number(input.substring(0, 4));
  const month = Number(input.substring(5, 7));
  const day = Number(input.substring(8, 10));
  // Real-calendar check via round-trip: JS Date silently rolls 2026-02-30 → 2026-03-02,
  // so we reconstruct and confirm the parts survive intact.
  const reconstructed = new Date(year, month - 1, day);
  if (
    reconstructed.getFullYear() !== year ||
    reconstructed.getMonth() !== month - 1 ||
    reconstructed.getDate() !== day
  ) {
    return { ok: false, error: 'invalid_calendar_date' };
  }
  // Future-date check: compare against today's local-date string.
  // String comparison works for `YYYY-MM-DD` because lexicographic order matches calendar order.
  if (input > todayLocalString()) {
    return { ok: false, error: 'future_date' };
  }
  return { ok: true, value: input };
}

function todayLocalString(): string {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

// Returns the current YYYY-MM-DD in Europe/Amsterdam. The user is in
// Amsterdam — codifying the timezone here means server clock changes (Fly
// is UTC) don't shift what "today" means. Used by the /api/day-entries/today
// route handler and the daily-entry UI.
//
// 'sv-SE' locale produces YYYY-MM-DD natively, avoiding manual zero-padding.
export function todayInAmsterdam(): string {
  return new Intl.DateTimeFormat('sv-SE', {
    timeZone: 'Europe/Amsterdam',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date());
}
