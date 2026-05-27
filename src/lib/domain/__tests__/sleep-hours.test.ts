import { describe, expect, it } from 'vitest';
import { validateSleepHours } from '../sleep-hours';

describe('sleep-hours', () => {
  describe('validateSleepHours — accepts null and valid numbers', () => {
    it('given null, when validated, then it is accepted', () => {
      const result = validateSleepHours(null);

      expect(result).toEqual({ ok: true, value: null });
    });

    it('given 0 (lower bound), when validated, then it is accepted', () => {
      const result = validateSleepHours(0);

      expect(result).toEqual({ ok: true, value: 0 });
    });

    it('given 24 (upper bound), when validated, then it is accepted', () => {
      const result = validateSleepHours(24);

      expect(result).toEqual({ ok: true, value: 24 });
    });

    it.each([1, 6, 7.5, 8.25, 12, 23.99])(
      'given valid decimal/integer %s, when validated, then it is accepted',
      (input) => {
        const result = validateSleepHours(input);

        expect(result).toEqual({ ok: true, value: input });
      },
    );
  });

  describe('validateSleepHours — rejects out-of-range', () => {
    it.each([-1, -0.01, Number.NEGATIVE_INFINITY])(
      'given %s (below 0), when validated, then it returns out_of_range',
      (input) => {
        const result = validateSleepHours(input);

        expect(result).toEqual({ ok: false, error: 'out_of_range' });
      },
    );

    it.each([25, 24.01, 100, Number.POSITIVE_INFINITY])(
      'given %s (above 24), when validated, then it returns out_of_range',
      (input) => {
        const result = validateSleepHours(input);

        expect(result).toEqual({ ok: false, error: 'out_of_range' });
      },
    );
  });

  describe('validateSleepHours — rejects wrong type', () => {
    it.each([
      ['string', '8'],
      ['undefined', undefined],
      ['NaN', Number.NaN],
      ['object', {}],
      ['array', [8]],
      ['boolean', true],
    ])('given %s, when validated, then it returns wrong_type', (_label, input) => {
      const result = validateSleepHours(input);

      expect(result).toEqual({ ok: false, error: 'wrong_type' });
    });
  });
});
