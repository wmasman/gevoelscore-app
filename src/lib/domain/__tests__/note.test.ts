import { describe, expect, it } from 'vitest';
import { MAX_NOTE_LENGTH, normalizeNote } from '../note';

describe('note', () => {
  describe('normalizeNote — accepts null', () => {
    it('given null, when normalized, then it returns { ok: true, value: null }', () => {
      const result = normalizeNote(null);

      expect(result).toEqual({ ok: true, value: null });
    });
  });

  describe('normalizeNote — whitespace-only normalizes to null', () => {
    it.each(['', '   ', '\n\t ', '\r\n', '   \n\n   '])(
      'given whitespace-only %j, when normalized, then it returns null',
      (input) => {
        const result = normalizeNote(input);

        expect(result).toEqual({ ok: true, value: null });
      },
    );
  });

  describe('normalizeNote — accepts non-empty string', () => {
    it('given a plain string, when normalized, then it is returned as-is', () => {
      const result = normalizeNote('hello');

      expect(result).toEqual({ ok: true, value: 'hello' });
    });

    it('given a string with surrounding whitespace, when normalized, then it is trimmed', () => {
      const result = normalizeNote('  hello  ');

      expect(result).toEqual({ ok: true, value: 'hello' });
    });

    it('given a multi-line note, when normalized, then internal whitespace is preserved', () => {
      const result = normalizeNote('  line one\nline two  ');

      expect(result).toEqual({ ok: true, value: 'line one\nline two' });
    });
  });

  describe('normalizeNote — rejects wrong type', () => {
    it.each([
      ['number', 42],
      ['undefined', undefined],
      ['object', { text: 'x' }],
      ['array', ['x']],
      ['boolean', true],
    ])('given %s, when normalized, then it returns wrong_type', (_label, input) => {
      const result = normalizeNote(input);

      expect(result).toEqual({ ok: false, error: 'wrong_type' });
    });
  });

  describe('normalizeNote — enforces max length', () => {
    it('accepts a note exactly at the cap', () => {
      const atCap = 'a'.repeat(MAX_NOTE_LENGTH);
      const result = normalizeNote(atCap);

      expect(result).toEqual({ ok: true, value: atCap });
    });

    it('rejects a note one character over the cap', () => {
      const overCap = 'a'.repeat(MAX_NOTE_LENGTH + 1);
      const result = normalizeNote(overCap);

      expect(result).toEqual({ ok: false, error: 'too_long' });
    });

    it('rejects far-oversized notes (1 MB)', () => {
      const huge = 'x'.repeat(1_000_000);
      const result = normalizeNote(huge);

      expect(result).toEqual({ ok: false, error: 'too_long' });
    });
  });
});
