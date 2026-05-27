export type SleepHoursError = 'wrong_type' | 'out_of_range';

export type ValidateSleepHoursResult =
  | { ok: true; value: number | null }
  | { ok: false; error: SleepHoursError };

export function validateSleepHours(input: unknown): ValidateSleepHoursResult {
  if (input === null) {
    return { ok: true, value: null };
  }
  if (typeof input !== 'number' || Number.isNaN(input)) {
    return { ok: false, error: 'wrong_type' };
  }
  // Decimals are allowed for sleep hours (unlike scores), so no integer check.
  // Infinity / -Infinity are caught here because they're numerically out of [0, 24].
  if (input < 0 || input > 24) {
    return { ok: false, error: 'out_of_range' };
  }
  return { ok: true, value: input };
}
