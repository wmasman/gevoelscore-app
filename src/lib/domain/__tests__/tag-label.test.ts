import { describe, expect, it } from 'vitest';
import {
  MAX_TAG_LABEL_LENGTH,
  MAX_TAG_LABEL_WORDS,
  validateTagLabel,
} from '../tag-label';

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

  describe('validateTagLabel — length bound', () => {
    it('accepts labels at exactly MAX_TAG_LABEL_LENGTH', () => {
      const exact = 'a'.repeat(MAX_TAG_LABEL_LENGTH);

      const result = validateTagLabel(exact);

      expect(result).toEqual({ ok: true, value: exact });
    });

    it('rejects labels exceeding MAX_TAG_LABEL_LENGTH with too_long', () => {
      const over = 'a'.repeat(MAX_TAG_LABEL_LENGTH + 1);

      const result = validateTagLabel(over);

      expect(result).toEqual({ ok: false, error: 'too_long' });
    });

    it('trims before applying the length check', () => {
      // Padding is stripped before measuring, so a 44-char string that
      // trims to MAX-2 chars is accepted.
      const inner = 'a'.repeat(MAX_TAG_LABEL_LENGTH - 2);
      const padded = `   ${inner}   `;

      const result = validateTagLabel(padded);

      expect(result).toEqual({ ok: true, value: inner });
    });
  });

  describe('validateTagLabel — word-count bound', () => {
    it('accepts a single-word label', () => {
      const result = validateTagLabel('hoofdpijn');

      expect(result).toEqual({ ok: true, value: 'hoofdpijn' });
    });

    it('accepts a two-word label', () => {
      const result = validateTagLabel('minder slapen');

      expect(result).toEqual({ ok: true, value: 'minder slapen' });
    });

    it(`rejects a label with more than ${MAX_TAG_LABEL_WORDS} words with too_many_words`, () => {
      const result = validateTagLabel('naar de fysio');

      expect(result).toEqual({ ok: false, error: 'too_many_words' });
    });

    it('normalises runs of internal whitespace to a single space', () => {
      // Required for dedup: `"hoofd  pijn"` and `"hoofd pijn"` must match.
      // After normalisation both become `"hoofd pijn"`.
      const result = validateTagLabel('minder    slapen');

      expect(result).toEqual({ ok: true, value: 'minder slapen' });
    });

    it('treats a hyphenated token as one word', () => {
      const result = validateTagLabel('post-COVID');

      expect(result).toEqual({ ok: true, value: 'post-COVID' });
    });

    it('counts a hyphenated phrase + extra token as two words', () => {
      const result = validateTagLabel('post-COVID herstel');

      expect(result).toEqual({ ok: true, value: 'post-COVID herstel' });
    });

    it('rejects a phrase that becomes three words when split on whitespace', () => {
      const result = validateTagLabel('post COVID symptomen');

      expect(result).toEqual({ ok: false, error: 'too_many_words' });
    });
  });

  describe('validateTagLabel — error precedence', () => {
    it('reports too_long before too_many_words when both would fail', () => {
      // 60 single-word characters: exceeds length but is only one word.
      // Length is the harder bound so its error takes precedence.
      const longSingleWord = 'a'.repeat(60);

      const result = validateTagLabel(longSingleWord);

      expect(result).toEqual({ ok: false, error: 'too_long' });
    });
  });
});
