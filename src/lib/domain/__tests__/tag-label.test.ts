import { describe, expect, it } from 'vitest';
import { validateTagLabel } from '../tag-label';

describe('tag-label', () => {
  describe('validateTagLabel — accepts non-empty trimmed strings', () => {
    it('accepts a plain non-empty string', () => {
      const result = validateTagLabel('hoofdpijn');

      expect(result).toEqual({ ok: true, value: 'hoofdpijn' });
    });

    it('trims surrounding whitespace', () => {
      const result = validateTagLabel('  hoofdpijn  ');

      expect(result).toEqual({ ok: true, value: 'hoofdpijn' });
    });

    it('preserves internal whitespace', () => {
      const result = validateTagLabel('goede dag');

      expect(result).toEqual({ ok: true, value: 'goede dag' });
    });
  });

  describe('validateTagLabel — rejects empty after trim', () => {
    it.each(['', ' ', '   ', '\n', '\t', '\n\t '])(
      'given %j, when validated, then it returns empty',
      (input) => {
        const result = validateTagLabel(input);

        expect(result).toEqual({ ok: false, error: 'empty' });
      },
    );
  });

  describe('validateTagLabel — rejects wrong type', () => {
    it.each([
      ['number', 42],
      ['null', null],
      ['undefined', undefined],
      ['object', { label: 'x' }],
      ['array', ['x']],
      ['boolean', true],
    ])('given %s, when validated, then it returns wrong_type', (_label, input) => {
      const result = validateTagLabel(input);

      expect(result).toEqual({ ok: false, error: 'wrong_type' });
    });
  });
});
