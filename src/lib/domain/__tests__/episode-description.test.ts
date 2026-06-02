import { describe, expect, it } from 'vitest';
import {
  MAX_EPISODE_DESCRIPTION_LENGTH,
  validateEpisodeDescription,
} from '../episode-description';

describe('episode-description', () => {
  describe('validateEpisodeDescription — accepts null + undefined', () => {
    it('given null, then returns ok with value null', () => {
      const result = validateEpisodeDescription(null);

      expect(result).toEqual({ ok: true, value: null });
    });

    it('given undefined, then returns ok with value null (coerced)', () => {
      // Undefined is treated as "not set" which is semantically null.
      // The wrapper passes patch.description as-is — when the caller omits
      // the key entirely, JS reads it as undefined, and we want that to
      // mean "no description" rather than "wrong type".
      const result = validateEpisodeDescription(undefined);

      expect(result).toEqual({ ok: true, value: null });
    });
  });

  describe('validateEpisodeDescription — accepts strings', () => {
    it('given an empty string, then returns ok with value "" (distinct from null)', () => {
      // Empty string IS a valid description value. The caller can use
      // "" to clear a description without going through null.
      const result = validateEpisodeDescription('');

      expect(result).toEqual({ ok: true, value: '' });
    });

    it('given a normal single-line description, then returns ok with the same value', () => {
      const result = validateEpisodeDescription('Wekelijks, 6 sessies.');

      expect(result).toEqual({ ok: true, value: 'Wekelijks, 6 sessies.' });
    });

    it('given a multi-line description, then preserves newlines and does NOT trim', () => {
      // Description is multi-line free-text. Whitespace at line edges is
      // intentional (paragraph spacing, indentation). Unlike label, we
      // do NOT normalise.
      const input = '  Citalopram afbouw\n  - week 1: 20mg dagelijks\n  - week 2: 15mg dagelijks\n';

      const result = validateEpisodeDescription(input);

      expect(result).toEqual({ ok: true, value: input });
    });
  });

  describe('validateEpisodeDescription — length bound', () => {
    it('given a description at exactly MAX chars, then returns ok with the same value', () => {
      const exact = 'a'.repeat(MAX_EPISODE_DESCRIPTION_LENGTH);

      const result = validateEpisodeDescription(exact);

      expect(result).toEqual({ ok: true, value: exact });
    });

    it('given a description one over MAX, then returns too_long', () => {
      const over = 'a'.repeat(MAX_EPISODE_DESCRIPTION_LENGTH + 1);

      const result = validateEpisodeDescription(over);

      expect(result).toEqual({ ok: false, error: 'too_long' });
    });
  });

  describe('validateEpisodeDescription — wrong type rejection', () => {
    it.each([
      ['number', 42],
      ['object', { description: 'x' }],
      ['array', ['x']],
      ['boolean', true],
    ])(
      'given %s (non-string non-null non-undefined), then returns wrong_type',
      (_label, input) => {
        const result = validateEpisodeDescription(input);

        expect(result).toEqual({ ok: false, error: 'wrong_type' });
      },
    );
  });
});
