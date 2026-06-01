export const MAX_TAG_LABEL_LENGTH = 40;
export const MAX_TAG_LABEL_WORDS = 2;

export type TagLabelError = 'wrong_type' | 'empty' | 'too_long' | 'too_many_words';

export type ValidateTagLabelResult =
  | { ok: true; value: string }
  | { ok: false; error: TagLabelError };

export function validateTagLabel(input: unknown): ValidateTagLabelResult {
  if (typeof input !== 'string') {
    return { ok: false, error: 'wrong_type' };
  }
  // Trim + normalise runs of internal whitespace to a single space.
  // The normalisation is required for dedup: `"hoofd  pijn"` and
  // `"hoofd pijn"` must compare equal after this step.
  const normalised = input.trim().replace(/\s+/g, ' ');
  if (normalised.length === 0) {
    return { ok: false, error: 'empty' };
  }
  // Length is the harder bound and reports first when both would fail.
  if (normalised.length > MAX_TAG_LABEL_LENGTH) {
    return { ok: false, error: 'too_long' };
  }
  const wordCount = normalised.split(' ').length;
  if (wordCount > MAX_TAG_LABEL_WORDS) {
    return { ok: false, error: 'too_many_words' };
  }
  return { ok: true, value: normalised };
}
