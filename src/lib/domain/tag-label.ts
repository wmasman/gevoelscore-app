export type TagLabelError = 'wrong_type' | 'empty';

export type ValidateTagLabelResult =
  | { ok: true; value: string }
  | { ok: false; error: TagLabelError };

export function validateTagLabel(input: unknown): ValidateTagLabelResult {
  if (typeof input !== 'string') {
    return { ok: false, error: 'wrong_type' };
  }
  const trimmed = input.trim();
  if (trimmed.length === 0) {
    return { ok: false, error: 'empty' };
  }
  return { ok: true, value: trimmed };
}
