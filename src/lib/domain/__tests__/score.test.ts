import { describe, expect, it } from 'vitest';
import { validateScore } from '../score';

describe('score', () => {
  describe('validateScore — accepts valid scores', () => {
    it.each([1, 2, 3, 4, 5, 6, 7, 8, 9, 10] as const)(
      'given integer %i, when validated, then it returns { ok: true, value: %i }',
      (input) => {
        const result = validateScore(input);

        expect(result.ok).toBe(true);
        if (result.ok) {
          expect(result.value).toBe(input);
        }
      },
    );
  });

  describe('validateScore — rejects out-of-range', () => {
    it.each([11, 100, Number.POSITIVE_INFINITY])(
      'given %s (above 10), when validated, then it returns out_of_range',
      (input) => {
        const result = validateScore(input);

        expect(result).toEqual({ ok: false, error: 'out_of_range' });
      },
    );

    it.each([0, -1, Number.NEGATIVE_INFINITY])(
      'given %s (below 1), when validated, then it returns out_of_range',
      (input) => {
        const result = validateScore(input);

        expect(result).toEqual({ ok: false, error: 'out_of_range' });
      },
    );
  });

  describe('validateScore — rejects non-integer', () => {
    it('given 4.5 (half-value), when validated, then it returns not_integer', () => {
      const result = validateScore(4.5);

      expect(result).toEqual({ ok: false, error: 'not_integer' });
    });

    it.each([3.1, 5.999])(
      'given decimal %s, when validated, then it returns not_integer',
      (input) => {
        const result = validateScore(input);

        expect(result).toEqual({ ok: false, error: 'not_integer' });
      },
    );
  });

  describe('validateScore — rejects wrong type', () => {
    it.each([
      ['string', '3'],
      ['null', null],
      ['undefined', undefined],
      ['NaN', Number.NaN],
      ['object', {}],
      ['array', [3]],
      ['boolean', true],
    ])(
      'given %s, when validated, then it returns wrong_type',
      (_label, input) => {
        const result = validateScore(input);

        expect(result).toEqual({ ok: false, error: 'wrong_type' });
      },
    );
  });
});
