import { describe, expect, it } from 'vitest';
import { validateParentEpisodeId } from '../parent-episode-id';

describe('parent-episode-id', () => {
  describe('validateParentEpisodeId — null path', () => {
    it('given null, then returns ok with null', () => {
      // null is the canonical "unlinked" sentinel — a tag with no parent
      // episode. The validator must accept it (not coerce it, not reject
      // it) so callers can use the same validator for both link and unlink.
      const result = validateParentEpisodeId(null);

      expect(result).toEqual({ ok: true, value: null });
    });
  });

  describe('validateParentEpisodeId — accepts UUID-shape strings', () => {
    it.each([
      ['lowercase v4', '550e8400-e29b-41d4-a716-446655440000'],
      ['uppercase', '550E8400-E29B-41D4-A716-446655440000'],
      ['mixed case', '550e8400-E29B-41d4-A716-446655440000'],
    ])('given %s, then returns ok with the value', (_label, input) => {
      const result = validateParentEpisodeId(input);

      expect(result).toEqual({ ok: true, value: input });
    });
  });

  describe('validateParentEpisodeId — rejects non-UUID strings', () => {
    it.each([
      ['empty string', ''],
      ['too short', '550e8400'],
      ['missing dashes', '550e8400e29b41d4a716446655440000'],
      ['wrong segment lengths', '550e840-e29b-41d4-a716-446655440000'],
      ['extra segments', '550e8400-e29b-41d4-a716-446655440000-extra'],
      ['non-hex characters', '550e8400-e29b-41d4-a716-44665544zzzz'],
      ['whitespace around uuid', ' 550e8400-e29b-41d4-a716-446655440000 '],
    ])('given %s, then returns invalid_parent_episode_id', (_label, input) => {
      const result = validateParentEpisodeId(input);

      expect(result).toEqual({
        ok: false,
        error: 'invalid_parent_episode_id',
      });
    });
  });

  describe('validateParentEpisodeId — rejects wrong types', () => {
    it.each([
      ['undefined', undefined],
      ['number', 1],
      ['object', { id: '550e8400-e29b-41d4-a716-446655440000' }],
      ['array', ['550e8400-e29b-41d4-a716-446655440000']],
      ['boolean true', true],
      ['boolean false', false],
    ])('given %s, then returns invalid_parent_episode_id', (_label, input) => {
      const result = validateParentEpisodeId(input);

      expect(result).toEqual({
        ok: false,
        error: 'invalid_parent_episode_id',
      });
    });
  });
});
