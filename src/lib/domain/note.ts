export type NoteError = 'wrong_type';

export type NormalizeNoteResult =
  | { ok: true; value: string | null }
  | { ok: false; error: NoteError };

export function normalizeNote(input: unknown): NormalizeNoteResult {
  if (input === null) {
    return { ok: true, value: null };
  }
  if (typeof input !== 'string') {
    return { ok: false, error: 'wrong_type' };
  }
  const trimmed = input.trim();
  return { ok: true, value: trimmed.length === 0 ? null : trimmed };
}
