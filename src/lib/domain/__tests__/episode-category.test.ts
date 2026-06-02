import { describe, expect, it } from 'vitest';
import {
  EPISODE_CATEGORIES,
  validateEpisodeCategory,
} from '../episode-category';

describe('episode-category', () => {
  describe('EPISODE_CATEGORIES — locked set', () => {
    it('contains exactly interventie and levensgebeurtenis (in that order)', () => {
      // Order is part of the contract — consumers iterating the const will
      // see interventie first. If categories are added or reordered (v2),
      // update this assertion deliberately.
      expect(EPISODE_CATEGORIES).toEqual(['interventie', 'levensgebeurtenis']);
    });
  });

  describe('validateEpisodeCategory — accepts the v1.5 categories', () => {
    it('given "interventie", then returns ok', () => {
      const result = validateEpisodeCategory('interventie');

      expect(result).toEqual({ ok: true, value: 'interventie' });
    });

    it('given "levensgebeurtenis", then returns ok', () => {
      const result = validateEpisodeCategory('levensgebeurtenis');

      expect(result).toEqual({ ok: true, value: 'levensgebeurtenis' });
    });
  });

  describe('validateEpisodeCategory — rejects v2-reserved categories', () => {
    it.each([
      ['project', 'project'],
      ['patroon', 'patroon'],
    ])(
      'given %s (v2-reserved), then returns invalid_episode_category',
      (_label, input) => {
        // The schema column is wide enough to hold these (string), but the
        // domain layer gates them out so a v2 value can't sneak in via
        // direct DB write.
        const result = validateEpisodeCategory(input);

        expect(result).toEqual({ ok: false, error: 'invalid_episode_category' });
      },
    );
  });

  describe('validateEpisodeCategory — rejects tag-category leak', () => {
    it.each([
      ['mentaal'],
      ['fysiek'],
      ['overall'],
      ['activiteit'],
      ['gebeurtenis'],
      ['custom'],
    ])('given tag-category %s, then returns invalid_episode_category', (input) => {
      const result = validateEpisodeCategory(input);

      expect(result).toEqual({ ok: false, error: 'invalid_episode_category' });
    });
  });

  describe('validateEpisodeCategory — rejects wrong type', () => {
    it.each([
      ['empty string', ''],
      ['null', null],
      ['undefined', undefined],
      ['number', 1],
      ['object', { category: 'interventie' }],
      ['array', ['interventie']],
      ['boolean', true],
    ])(
      'given %s, then returns invalid_episode_category',
      (_label, input) => {
        const result = validateEpisodeCategory(input);

        expect(result).toEqual({ ok: false, error: 'invalid_episode_category' });
      },
    );
  });
});
