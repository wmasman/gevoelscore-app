import { describe, expect, it } from 'vitest';
import {
  MAX_EPISODE_LABEL_LENGTH,
  validateEpisodeLabel,
} from '../episode-label';

describe('episode-label', () => {
  describe('validateEpisodeLabel — accepts realistic labels', () => {
    it('accepts a 2-word label ("Coaching Sarah")', () => {
      const result = validateEpisodeLabel('Coaching Sarah');

      expect(result).toEqual({ ok: true, value: 'Coaching Sarah' });
    });

    it('accepts a 3-word label ("Coaching met Sarah") — no word-count constraint', () => {
      // Tag labels cap at 2 words; episodes don't. Natural 3-4 word
      // names ("Coaching met Sarah", "Vakantie Texel 2026") must pass.
      const result = validateEpisodeLabel('Coaching met Sarah');

      expect(result).toEqual({ ok: true, value: 'Coaching met Sarah' });
    });

    it('accepts a 4-word label ("Wekelijkse fysio bij Marieke")', () => {
      const result = validateEpisodeLabel('Wekelijkse fysio bij Marieke');

      expect(result).toEqual({
        ok: true,
        value: 'Wekelijkse fysio bij Marieke',
      });
    });
  });

  describe('validateEpisodeLabel — whitespace handling', () => {
    it('trims surrounding whitespace', () => {
      const result = validateEpisodeLabel('  Vakantie Texel  ');

      expect(result).toEqual({ ok: true, value: 'Vakantie Texel' });
    });

    it('collapses runs of internal whitespace to a single space', () => {
      // Mirror tag-label's dedup invariant: "hoofd  pijn" must compare
      // equal to "hoofd pijn" after normalisation.
      const result = validateEpisodeLabel('Coaching   met   Sarah');

      expect(result).toEqual({ ok: true, value: 'Coaching met Sarah' });
    });
  });

  describe('validateEpisodeLabel — length bound', () => {
    it('accepts a label at exactly MAX_EPISODE_LABEL_LENGTH', () => {
      const exact = 'a'.repeat(MAX_EPISODE_LABEL_LENGTH);

      const result = validateEpisodeLabel(exact);

      expect(result).toEqual({ ok: true, value: exact });
    });

    it('accepts a label that is exactly MAX after normalisation but longer with padding', () => {
      const inner = 'a'.repeat(MAX_EPISODE_LABEL_LENGTH);
      const padded = `   ${inner}   `;

      const result = validateEpisodeLabel(padded);

      expect(result).toEqual({ ok: true, value: inner });
    });

    it('rejects a label that is one over MAX with too_long', () => {
      const over = 'a'.repeat(MAX_EPISODE_LABEL_LENGTH + 1);

      const result = validateEpisodeLabel(over);

      expect(result).toEqual({ ok: false, error: 'too_long' });
    });
  });

  describe('validateEpisodeLabel — empty rejection', () => {
    it.each(['', ' ', '   ', '\n', '\t', '\n\t '])(
      'given %j (whitespace-only), then returns empty',
      (input) => {
        const result = validateEpisodeLabel(input);

        expect(result).toEqual({ ok: false, error: 'empty' });
      },
    );
  });

  describe('validateEpisodeLabel — wrong type rejection', () => {
    it.each([
      ['number', 42],
      ['null', null],
      ['undefined', undefined],
      ['object', { label: 'x' }],
      ['array', ['x']],
      ['boolean', true],
    ])(
      'given %s, then returns wrong_type',
      (_label, input) => {
        const result = validateEpisodeLabel(input);

        expect(result).toEqual({ ok: false, error: 'wrong_type' });
      },
    );
  });
});
