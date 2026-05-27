export type Score = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
export type ScoreError = 'out_of_range' | 'not_integer' | 'wrong_type';
export type ValidateScoreResult =
  | { ok: true; value: Score }
  | { ok: false; error: ScoreError };

export function validateScore(input: unknown): ValidateScoreResult {
  if (typeof input !== 'number' || Number.isNaN(input)) {
    return { ok: false, error: 'wrong_type' };
  }
  // Range check runs before the integer check so Infinity / -Infinity fall into
  // out_of_range (they pass > 10 / < 1 but aren't integers). For inputs like
  // -0.5, out_of_range is also the more user-meaningful error.
  if (input < 1 || input > 10) {
    return { ok: false, error: 'out_of_range' };
  }
  if (!Number.isInteger(input)) {
    return { ok: false, error: 'not_integer' };
  }
  return { ok: true, value: input as Score };
}
