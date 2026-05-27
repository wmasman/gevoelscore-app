import { describe, expect, it } from 'vitest';
import { validateTagCategory } from '../tag-category';

describe('tag-category', () => {
  describe('validateTagCategory — accepts the 8 locked v1 categories', () => {
    it.each([
      'mentaal',
      'fysiek',
      'overall',
      'activiteit',
      'gebeurtenis',
      'interventie',
      'project',
      'custom',
    ] as const)(
      'accepts %s as a valid category',
      (input) => {
        const result = validateTagCategory(input);

        expect(result).toEqual({ ok: true, value: input });
      },
    );
  });

  describe('validateTagCategory — rejects unknown categories', () => {
    it("rejects 'positief' (retired from the brief's original 4-cluster proposal)", () => {
      const result = validateTagCategory('positief');

      expect(result).toEqual({ ok: false, error: 'unknown_category' });
    });

    it.each(['unknown', 'PROJECT', 'fysieke', '', 'interventies'])(
      'rejects %j as unknown_category',
      (input) => {
        const result = validateTagCategory(input);

        expect(result).toEqual({ ok: false, error: 'unknown_category' });
      },
    );
  });

  describe('validateTagCategory — rejects wrong type', () => {
    it.each([
      ['number', 1],
      ['null', null],
      ['undefined', undefined],
      ['object', { category: 'mentaal' }],
      ['array', ['mentaal']],
      ['boolean', true],
    ])('given %s, when validated, then it returns wrong_type', (_label, input) => {
      const result = validateTagCategory(input);

      expect(result).toEqual({ ok: false, error: 'wrong_type' });
    });
  });
});
