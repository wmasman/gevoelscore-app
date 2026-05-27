export type TagIdsError = 'wrong_type' | 'non_string_element' | 'duplicates';

export type ValidateTagIdsResult =
  | { ok: true; value: string[] }
  | { ok: false; error: TagIdsError };

export function validateTagIds(input: unknown): ValidateTagIdsResult {
  if (!Array.isArray(input)) {
    return { ok: false, error: 'wrong_type' };
  }
  for (const item of input) {
    if (typeof item !== 'string') {
      return { ok: false, error: 'non_string_element' };
    }
  }
  if (new Set(input).size !== input.length) {
    return { ok: false, error: 'duplicates' };
  }
  return { ok: true, value: input };
}
