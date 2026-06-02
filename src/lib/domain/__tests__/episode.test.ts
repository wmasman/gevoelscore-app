import { describe, expect, it } from 'vitest';
import { validateEpisode } from '../episode';

/** Factory for a minimal valid ongoing Episode (snake_case, Directus shape). */
function validEpisode(
  overrides: Record<string, unknown> = {},
): Record<string, unknown> {
  return {
    id: 'ep_01HQ5XYZ',
    label: 'Coaching met Sarah',
    category: 'interventie',
    start_date: '2026-04-01',
    end_date: null,
    description: null,
    calendar_binding: null,
    archived_at: null,
    created_at: '2026-04-01T08:00:00.000Z',
    updated_at: '2026-04-01T08:00:00.000Z',
    ...overrides,
  };
}

describe('episode', () => {
  describe('validateEpisode — happy path', () => {
    it('accepts a minimal valid ongoing Episode', () => {
      const result = validateEpisode(validEpisode());

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.label).toBe('Coaching met Sarah');
        expect(result.value.category).toBe('interventie');
        expect(result.value.end_date).toBeNull();
      }
    });

    it('accepts a closed-range Episode (end_date set)', () => {
      const result = validateEpisode(
        validEpisode({ end_date: '2026-06-01' }),
      );

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.end_date).toBe('2026-06-01');
      }
    });

    it('accepts a levensgebeurtenis Episode', () => {
      const result = validateEpisode(
        validEpisode({
          label: 'Vakantie Texel',
          category: 'levensgebeurtenis',
          start_date: '2026-07-15',
          end_date: '2026-07-22',
        }),
      );

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.category).toBe('levensgebeurtenis');
      }
    });

    it('accepts an archived Episode (archived_at set)', () => {
      const result = validateEpisode(
        validEpisode({ archived_at: '2026-05-01T10:00:00.000Z' }),
      );

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.archived_at).toBe('2026-05-01T10:00:00.000Z');
      }
    });

    it('accepts a description string', () => {
      const result = validateEpisode(
        validEpisode({
          description: '20mg → 10mg afbouw over 6 weken, dagelijks',
        }),
      );

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.description).toBe(
          '20mg → 10mg afbouw over 6 weken, dagelijks',
        );
      }
    });

    it('round-trips: validator output matches input snake_case keys and values', () => {
      const input = validEpisode({
        label: 'Ergotherapie',
        category: 'interventie',
        start_date: '2026-05-15',
        end_date: '2026-08-15',
        description: 'wekelijks',
        archived_at: null,
      });

      const result = validateEpisode(input);

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value).toEqual({
          id: 'ep_01HQ5XYZ',
          label: 'Ergotherapie',
          category: 'interventie',
          start_date: '2026-05-15',
          end_date: '2026-08-15',
          description: 'wekelijks',
          calendar_binding: null,
          archived_at: null,
          created_at: '2026-04-01T08:00:00.000Z',
          updated_at: '2026-04-01T08:00:00.000Z',
        });
      }
    });
  });

  describe('validateEpisode — shape rejection', () => {
    it('rejects null', () => {
      const result = validateEpisode(null);

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });

    it('rejects an array', () => {
      const result = validateEpisode([]);

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });

    it('rejects a non-object (string)', () => {
      const result = validateEpisode('not an object');

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });

    it('rejects an object missing a required key', () => {
      const partial = validEpisode();
      delete (partial as Record<string, unknown>).updated_at;

      const result = validateEpisode(partial);

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });

    it('rejects an object with an extra unexpected key', () => {
      // Strict shape — extra keys signal drift. Catching this here avoids
      // silently accepting a renamed field from a future Directus migration.
      const result = validateEpisode(validEpisode({ extra_field: 'whoops' }));

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });
  });

  describe('validateEpisode — per-field rejection', () => {
    it('rejects empty id with invalid_id', () => {
      const result = validateEpisode(validEpisode({ id: '' }));

      expect(result).toEqual({ ok: false, error: 'invalid_id' });
    });

    it('rejects non-string id with invalid_id', () => {
      const result = validateEpisode(validEpisode({ id: 42 }));

      expect(result).toEqual({ ok: false, error: 'invalid_id' });
    });

    it('rejects bad label with invalid_label', () => {
      const result = validateEpisode(validEpisode({ label: '   ' }));

      expect(result).toEqual({ ok: false, error: 'invalid_label' });
    });

    it('rejects category "project" (v2-reserved) with invalid_category', () => {
      // Schema column is wide enough to hold "project" (string), so the
      // domain validator MUST refuse it — that's the v2-gate.
      const result = validateEpisode(validEpisode({ category: 'project' }));

      expect(result).toEqual({ ok: false, error: 'invalid_category' });
    });

    it('rejects category "patroon" (v2-reserved) with invalid_category', () => {
      const result = validateEpisode(validEpisode({ category: 'patroon' }));

      expect(result).toEqual({ ok: false, error: 'invalid_category' });
    });

    it('rejects category "mentaal" (tag-category leak) with invalid_category', () => {
      const result = validateEpisode(validEpisode({ category: 'mentaal' }));

      expect(result).toEqual({ ok: false, error: 'invalid_category' });
    });

    it('rejects end_date < start_date with invalid_date_range', () => {
      const result = validateEpisode(
        validEpisode({ start_date: '2026-05-15', end_date: '2026-04-01' }),
      );

      expect(result).toEqual({ ok: false, error: 'invalid_date_range' });
    });

    it('rejects malformed start_date with invalid_date_range', () => {
      const result = validateEpisode(validEpisode({ start_date: '2026/04/01' }));

      expect(result).toEqual({ ok: false, error: 'invalid_date_range' });
    });

    it('rejects non-string description (when not null) with invalid_description', () => {
      const result = validateEpisode(validEpisode({ description: 42 }));

      expect(result).toEqual({ ok: false, error: 'invalid_description' });
    });

    it('rejects non-null calendar_binding with invalid_calendar_binding (v1.5 gate)', () => {
      // Column exists in schema for v1.6 but v1.5 must lock it to null.
      const result = validateEpisode(
        validEpisode({ calendar_binding: { google: 'series_xyz' } }),
      );

      expect(result).toEqual({ ok: false, error: 'invalid_calendar_binding' });
    });

    it('rejects bad archived_at format with invalid_archived_at', () => {
      const result = validateEpisode(
        validEpisode({ archived_at: '2026-05-01' }),
      );

      expect(result).toEqual({ ok: false, error: 'invalid_archived_at' });
    });

    it('rejects bad created_at with invalid_created_at', () => {
      const result = validateEpisode(
        validEpisode({ created_at: 'not-a-timestamp' }),
      );

      expect(result).toEqual({ ok: false, error: 'invalid_created_at' });
    });

    it('rejects bad updated_at with invalid_updated_at', () => {
      const result = validateEpisode(
        validEpisode({ updated_at: 'not-a-timestamp' }),
      );

      expect(result).toEqual({ ok: false, error: 'invalid_updated_at' });
    });
  });
});
