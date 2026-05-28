export type NoteError = 'wrong_type' | 'too_long';

export type NormalizeNoteResult =
  | { ok: true; value: string | null }
  | { ok: false; error: NoteError };

// Defense-in-depth cap on the free-text note. Directus stores `text`
// (unbounded) but the app has no use case for multi-megabyte journal
// entries; capping at 10_000 characters covers ~1500 Dutch words —
// generous for honest use, narrow enough that a stuck-key paste or a
// malicious script PUT gets rejected at the boundary. Matches the
// 2026-05-28 audit's note-input defense-in-depth recommendation.
//
// If a real entry ever needs more, raise the cap; the API + schema
// happily accept it. The cap is policy, not a structural limit.
export const MAX_NOTE_LENGTH = 10_000;

export function normalizeNote(input: unknown): NormalizeNoteResult {
  if (input === null) {
    return { ok: true, value: null };
  }
  if (typeof input !== 'string') {
    return { ok: false, error: 'wrong_type' };
  }
  if (input.length > MAX_NOTE_LENGTH) {
    return { ok: false, error: 'too_long' };
  }
  const trimmed = input.trim();
  return { ok: true, value: trimmed.length === 0 ? null : trimmed };
}
