export type SubScoreValue = 1 | 2 | 3 | 4 | 5 | 6;

export type SubScoreError = 'wrong_type' | 'out_of_range' | 'not_integer';

export type ValidateSubScoreResult =
  | { ok: true; value: SubScoreValue }
  | { ok: false; error: SubScoreError };

export type SubScores = {
  cognitive: SubScoreValue | null;
  physical: SubScoreValue | null;
  mental: SubScoreValue | null;
};

export type SubScoresError =
  | 'wrong_type'
  | 'invalid_shape'
  | 'invalid_cognitive'
  | 'invalid_physical'
  | 'invalid_mental';

export type ValidateSubScoresResult =
  | { ok: true; value: SubScores | null }
  | { ok: false; error: SubScoresError };

export function validateSubScore(input: unknown): ValidateSubScoreResult {
  if (typeof input !== 'number' || Number.isNaN(input)) {
    return { ok: false, error: 'wrong_type' };
  }
  if (input < 1 || input > 6) {
    return { ok: false, error: 'out_of_range' };
  }
  if (!Number.isInteger(input)) {
    return { ok: false, error: 'not_integer' };
  }
  return { ok: true, value: input as SubScoreValue };
}

const SUB_SCORE_KEYS = ['cognitive', 'mental', 'physical'] as const;

export function validateSubScores(input: unknown): ValidateSubScoresResult {
  if (input === null) {
    return { ok: true, value: null };
  }
  if (typeof input !== 'object' || Array.isArray(input)) {
    return { ok: false, error: 'wrong_type' };
  }

  const obj = input as Record<string, unknown>;
  const keys = Object.keys(obj).sort();
  if (
    keys.length !== SUB_SCORE_KEYS.length ||
    !keys.every((k, i) => k === SUB_SCORE_KEYS[i])
  ) {
    return { ok: false, error: 'invalid_shape' };
  }

  const cognitive = validateFieldOrNull(obj.cognitive);
  if (!cognitive.ok) {
    return { ok: false, error: 'invalid_cognitive' };
  }
  const physical = validateFieldOrNull(obj.physical);
  if (!physical.ok) {
    return { ok: false, error: 'invalid_physical' };
  }
  const mental = validateFieldOrNull(obj.mental);
  if (!mental.ok) {
    return { ok: false, error: 'invalid_mental' };
  }

  return {
    ok: true,
    value: {
      cognitive: cognitive.value,
      physical: physical.value,
      mental: mental.value,
    },
  };
}

function validateFieldOrNull(
  input: unknown,
): { ok: true; value: SubScoreValue | null } | { ok: false } {
  if (input === null) {
    return { ok: true, value: null };
  }
  const result = validateSubScore(input);
  return result.ok ? result : { ok: false };
}
