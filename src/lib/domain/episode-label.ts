// Same character ceiling as MAX_TAG_LABEL_LENGTH (40), but episodes
// have NO word-count limit (tags cap at 2 words; episodes naturally
// run 3-4 words: "Coaching met Sarah", "Wekelijkse fysio bij Marieke").
// Narrative content goes in `description`, not the label.

export const MAX_EPISODE_LABEL_LENGTH = 40;

export type EpisodeLabelError = 'wrong_type' | 'empty' | 'too_long';

export type ValidateEpisodeLabelResult =
  | { ok: true; value: string }
  | { ok: false; error: EpisodeLabelError };

export function validateEpisodeLabel(input: unknown): ValidateEpisodeLabelResult {
  if (typeof input !== 'string') {
    return { ok: false, error: 'wrong_type' };
  }
  // Trim surrounding + collapse runs of internal whitespace to a single
  // space. Required so "coaching  sarah" and "coaching sarah" compare
  // equal on dedup — mirrors validateTagLabel.
  const normalised = input.trim().replace(/\s+/g, ' ');
  if (normalised.length === 0) {
    return { ok: false, error: 'empty' };
  }
  if (normalised.length > MAX_EPISODE_LABEL_LENGTH) {
    return { ok: false, error: 'too_long' };
  }
  return { ok: true, value: normalised };
}
