import { describe, expect, it } from 'vitest';
import { validateSubScore, validateSubScores } from '../sub-score';

describe('sub-score', () => {
  describe('validateSubScore — accepts integers 1–6', () => {
    it.each([1, 2, 3, 4, 5, 6] as const)(
      'given integer %i, when validated, then it returns { ok: true, value: %i }',
      (input) => {
        const result = validateSubScore(input);

        expect(result.ok).toBe(true);
        if (result.ok) {
          expect(result.value).toBe(input);
        }
      },
    );
  });

  describe('validateSubScore — rejects out-of-range', () => {
    it.each([7, 11, 100, Number.POSITIVE_INFINITY])(
      'given %s (above 6), when validated, then it returns out_of_range',
      (input) => {
        const result = validateSubScore(input);

        expect(result).toEqual({ ok: false, error: 'out_of_range' });
      },
    );

    it.each([0, -1, Number.NEGATIVE_INFINITY])(
      'given %s (below 1), when validated, then it returns out_of_range',
      (input) => {
        const result = validateSubScore(input);

        expect(result).toEqual({ ok: false, error: 'out_of_range' });
      },
    );
  });

  describe('validateSubScore — rejects non-integer', () => {
    it.each([1.5, 3.1, 5.999])(
      'given decimal %s, when validated, then it returns not_integer',
      (input) => {
        const result = validateSubScore(input);

        expect(result).toEqual({ ok: false, error: 'not_integer' });
      },
    );
  });

  describe('validateSubScore — rejects wrong type', () => {
    it.each([
      ['string', '3'],
      ['null', null],
      ['undefined', undefined],
      ['NaN', Number.NaN],
      ['object', {}],
      ['boolean', true],
    ])('given %s, when validated, then it returns wrong_type', (_label, input) => {
      const result = validateSubScore(input);

      expect(result).toEqual({ ok: false, error: 'wrong_type' });
    });
  });
});

describe('sub-scores', () => {
  describe('validateSubScores — accepts null and valid structs', () => {
    it('given null, when validated, then it is accepted as null', () => {
      const result = validateSubScores(null);

      expect(result).toEqual({ ok: true, value: null });
    });

    it('given { cognitive: 4, physical: null, mental: 5 }, when validated, then it is accepted', () => {
      const input = { cognitive: 4, physical: null, mental: 5 };

      const result = validateSubScores(input);

      expect(result).toEqual({
        ok: true,
        value: { cognitive: 4, physical: null, mental: 5 },
      });
    });

    it('given all three sub-scores populated with integers 1–6, when validated, then it is accepted', () => {
      const input = { cognitive: 6, physical: 1, mental: 3 };

      const result = validateSubScores(input);

      expect(result).toEqual({
        ok: true,
        value: { cognitive: 6, physical: 1, mental: 3 },
      });
    });

    it('given all three sub-scores null, when validated, then it is accepted', () => {
      const input = { cognitive: null, physical: null, mental: null };

      const result = validateSubScores(input);

      expect(result).toEqual({
        ok: true,
        value: { cognitive: null, physical: null, mental: null },
      });
    });
  });

  describe('validateSubScores — propagates per-field errors', () => {
    it('given cognitive: 7 (out of 1–6), when validated, then it returns invalid_cognitive', () => {
      const result = validateSubScores({ cognitive: 7, physical: null, mental: null });

      expect(result).toEqual({ ok: false, error: 'invalid_cognitive' });
    });

    it('given physical: 0, when validated, then it returns invalid_physical', () => {
      const result = validateSubScores({ cognitive: null, physical: 0, mental: null });

      expect(result).toEqual({ ok: false, error: 'invalid_physical' });
    });

    it('given mental: 4.5, when validated, then it returns invalid_mental', () => {
      const result = validateSubScores({ cognitive: null, physical: null, mental: 4.5 });

      expect(result).toEqual({ ok: false, error: 'invalid_mental' });
    });
  });

  describe('validateSubScores — rejects bad shape', () => {
    it('given missing key (no mental), when validated, then it returns invalid_shape', () => {
      const result = validateSubScores({ cognitive: 4, physical: 3 });

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });

    it('given extra key, when validated, then it returns invalid_shape', () => {
      const result = validateSubScores({
        cognitive: 4,
        physical: 3,
        mental: 5,
        unexpected: 1,
      });

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });

    it('given empty object, when validated, then it returns invalid_shape', () => {
      const result = validateSubScores({});

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });
  });

  describe('validateSubScores — rejects wrong type', () => {
    it.each([
      ['number', 5],
      ['string', '{}'],
      ['undefined', undefined],
      ['array', [4, 3, 5]],
      ['boolean', true],
    ])('given %s, when validated, then it returns wrong_type', (_label, input) => {
      const result = validateSubScores(input);

      expect(result).toEqual({ ok: false, error: 'wrong_type' });
    });
  });
});
