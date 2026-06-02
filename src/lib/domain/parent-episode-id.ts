import { isUuidShape } from './uuid';

export type ParentEpisodeIdError = 'invalid_parent_episode_id';

export type ValidateParentEpisodeIdResult =
  | { ok: true; value: string | null }
  | { ok: false; error: ParentEpisodeIdError };

export function validateParentEpisodeId(
  input: unknown,
): ValidateParentEpisodeIdResult {
  if (input === null) {
    return { ok: true, value: null };
  }
  if (isUuidShape(input)) {
    return { ok: true, value: input };
  }
  return { ok: false, error: 'invalid_parent_episode_id' };
}
