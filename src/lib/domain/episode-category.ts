export const EPISODE_CATEGORIES = ['interventie', 'levensgebeurtenis'] as const;
export type EpisodeCategory = (typeof EPISODE_CATEGORIES)[number];

export type EpisodeCategoryError = 'invalid_episode_category';

export type ValidateEpisodeCategoryResult =
  | { ok: true; value: EpisodeCategory }
  | { ok: false; error: EpisodeCategoryError };

export function validateEpisodeCategory(
  input: unknown,
): ValidateEpisodeCategoryResult {
  if (
    typeof input === 'string' &&
    (EPISODE_CATEGORIES as readonly string[]).includes(input)
  ) {
    return { ok: true, value: input as EpisodeCategory };
  }
  return { ok: false, error: 'invalid_episode_category' };
}
