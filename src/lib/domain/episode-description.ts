// Server-side cap on episode description text. The schema column is
// `text` (effectively unlimited); the cap is defense-in-depth against
// accidental "paste a whole PDF" or malicious payloads. Matches the
// note-length soft cap from .claude/security-checklist.md.
//
// Unlike validateEpisodeLabel, we do NOT trim or normalise whitespace —
// description is multi-line free-text and surrounding whitespace can
// be intentional (paragraph spacing, indentation in a list).

export const MAX_EPISODE_DESCRIPTION_LENGTH = 10_000;

export type EpisodeDescriptionError = 'wrong_type' | 'too_long';

export type ValidateEpisodeDescriptionResult =
  | { ok: true; value: string | null }
  | { ok: false; error: EpisodeDescriptionError };

export function validateEpisodeDescription(
  input: unknown,
): ValidateEpisodeDescriptionResult {
  if (input === null || input === undefined) {
    return { ok: true, value: null };
  }
  if (typeof input !== 'string') {
    return { ok: false, error: 'wrong_type' };
  }
  if (input.length > MAX_EPISODE_DESCRIPTION_LENGTH) {
    return { ok: false, error: 'too_long' };
  }
  return { ok: true, value: input };
}
