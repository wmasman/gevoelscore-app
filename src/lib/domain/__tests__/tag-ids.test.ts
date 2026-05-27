import { describe, expect, it } from 'vitest';
import { validateTagIds } from '../tag-ids';

describe('tag-ids', () => {
  describe('validateTagIds — accepts valid arrays', () => {
    it('given an empty array, when validated, then it is accepted', () => {
      const result = validateTagIds([]);

      expect(result).toEqual({ ok: true, value: [] });
    });

    it('given a unique array of strings, when validated, then it is accepted', () => {
      const result = validateTagIds(['fysiek-hoofdpijn', 'mentaal-stress', 'activiteit-rust']);

      expect(result).toEqual({
        ok: true,
        value: ['fysiek-hoofdpijn', 'mentaal-stress', 'activiteit-rust'],
      });
    });

    it('given a single-element array, when validated, then it is accepted', () => {
      const result = validateTagIds(['only-one']);

      expect(result).toEqual({ ok: true, value: ['only-one'] });
    });
  });

  describe('validateTagIds — rejects duplicates', () => {
    it('given an array with duplicates, when validated, then it returns duplicates', () => {
      const result = validateTagIds(['a', 'a']);

      expect(result).toEqual({ ok: false, error: 'duplicates' });
    });

    it('given an array with later-position duplicates, when validated, then it returns duplicates', () => {
      const result = validateTagIds(['a', 'b', 'c', 'a']);

      expect(result).toEqual({ ok: false, error: 'duplicates' });
    });
  });

  describe('validateTagIds — rejects non-array', () => {
    it.each([
      ['string', 'fysiek-hoofdpijn'],
      ['number', 42],
      ['null', null],
      ['undefined', undefined],
      ['object', { tags: ['a'] }],
      ['boolean', true],
    ])('given %s, when validated, then it returns wrong_type', (_label, input) => {
      const result = validateTagIds(input);

      expect(result).toEqual({ ok: false, error: 'wrong_type' });
    });
  });

  describe('validateTagIds — rejects non-string elements', () => {
    it.each([
      ['number element', ['a', 42, 'c']],
      ['null element', ['a', null, 'c']],
      ['undefined element', ['a', undefined, 'c']],
      ['object element', ['a', { id: 'x' }, 'c']],
      ['boolean element', ['a', true, 'c']],
    ])('given array with %s, when validated, then it returns non_string_element', (_label, input) => {
      const result = validateTagIds(input);

      expect(result).toEqual({ ok: false, error: 'non_string_element' });
    });
  });
});
