import { describe, expect, it } from 'vitest';
import { validateTag } from '../tag';

/** Factory for a minimal valid non-project Tag. */
function validTag(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    id: 'tag_01HQ5XYZ',
    label: 'hoofdpijn',
    category: 'fysiek',
    project_id: null,
    usage_count: 0,
    archived_at: null,
    created_at: '2026-05-26T08:00:00.000Z',
    ...overrides,
  };
}

describe('tag', () => {
  describe('validateTag — happy path', () => {
    it('accepts a minimal valid non-project Tag', () => {
      const result = validateTag(validTag());

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.label).toBe('hoofdpijn');
        expect(result.value.category).toBe('fysiek');
        expect(result.value.project_id).toBeNull();
      }
    });

    it('accepts a project Tag with project_id', () => {
      const result = validateTag(
        validTag({ category: 'project', project_id: 'proj_01HQ5ABC' }),
      );

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.category).toBe('project');
        expect(result.value.project_id).toBe('proj_01HQ5ABC');
      }
    });

    it('accepts an archived Tag with archived_at timestamp', () => {
      const result = validateTag(
        validTag({ archived_at: '2026-04-01T12:00:00.000Z' }),
      );

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.archived_at).toBe('2026-04-01T12:00:00.000Z');
      }
    });

    it('trims label whitespace before storing', () => {
      const result = validateTag(validTag({ label: '  goede dag  ' }));

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.label).toBe('goede dag');
      }
    });

    it('accepts non-zero usage_count', () => {
      const result = validateTag(validTag({ usage_count: 42 }));

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.usage_count).toBe(42);
      }
    });
  });

  describe('validateTag — propagates per-field errors', () => {
    it('rejects invalid label (empty)', () => {
      const result = validateTag(validTag({ label: '   ' }));

      expect(result).toEqual({ ok: false, error: 'invalid_label' });
    });

    it('rejects invalid category (retired positief)', () => {
      const result = validateTag(validTag({ category: 'positief' }));

      expect(result).toEqual({ ok: false, error: 'invalid_category' });
    });

    it("rejects category 'project' when project_id is null", () => {
      const result = validateTag(validTag({ category: 'project', project_id: null }));

      expect(result).toEqual({ ok: false, error: 'missing_project_id' });
    });

    it("rejects non-project category when project_id is provided", () => {
      const result = validateTag(
        validTag({ category: 'fysiek', project_id: 'proj_01HQ5ABC' }),
      );

      expect(result).toEqual({ ok: false, error: 'unexpected_project_id' });
    });

    it("rejects project category with empty-string project_id", () => {
      const result = validateTag(validTag({ category: 'project', project_id: '' }));

      expect(result).toEqual({ ok: false, error: 'invalid_project_id' });
    });

    it("rejects project category with non-string project_id", () => {
      const result = validateTag(validTag({ category: 'project', project_id: 42 }));

      expect(result).toEqual({ ok: false, error: 'invalid_project_id' });
    });
  });

  describe('validateTag — usage_count', () => {
    it('rejects negative usage_count', () => {
      const result = validateTag(validTag({ usage_count: -1 }));

      expect(result).toEqual({ ok: false, error: 'invalid_usage_count' });
    });

    it('rejects non-integer usage_count', () => {
      const result = validateTag(validTag({ usage_count: 3.5 }));

      expect(result).toEqual({ ok: false, error: 'invalid_usage_count' });
    });

    it('rejects non-number usage_count', () => {
      const result = validateTag(validTag({ usage_count: '5' }));

      expect(result).toEqual({ ok: false, error: 'invalid_usage_count' });
    });

    it('rejects NaN usage_count', () => {
      const result = validateTag(validTag({ usage_count: Number.NaN }));

      expect(result).toEqual({ ok: false, error: 'invalid_usage_count' });
    });
  });

  describe('validateTag — id', () => {
    it('rejects empty-string id', () => {
      const result = validateTag(validTag({ id: '' }));

      expect(result).toEqual({ ok: false, error: 'invalid_id' });
    });

    it('rejects non-string id', () => {
      const result = validateTag(validTag({ id: 42 }));

      expect(result).toEqual({ ok: false, error: 'invalid_id' });
    });

    it('rejects null id', () => {
      const result = validateTag(validTag({ id: null }));

      expect(result).toEqual({ ok: false, error: 'invalid_id' });
    });
  });

  describe('validateTag — timestamps', () => {
    it('rejects malformed created_at', () => {
      const result = validateTag(validTag({ created_at: 'yesterday' }));

      expect(result).toEqual({ ok: false, error: 'invalid_created_at' });
    });

    it('rejects null created_at (required)', () => {
      const result = validateTag(validTag({ created_at: null }));

      expect(result).toEqual({ ok: false, error: 'invalid_created_at' });
    });

    it('rejects malformed archived_at', () => {
      const result = validateTag(validTag({ archived_at: '2026-04-01' }));

      expect(result).toEqual({ ok: false, error: 'invalid_archived_at' });
    });

    it('accepts null archived_at (active tag)', () => {
      const result = validateTag(validTag({ archived_at: null }));

      expect(result.ok).toBe(true);
    });
  });

  describe('validateTag — shape', () => {
    it.each([
      ['null', null],
      ['array', []],
      ['number', 42],
      ['string', '{}'],
    ])('rejects non-object %s → invalid_shape', (_label, input) => {
      const result = validateTag(input);

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });

    it('rejects entry with a missing key', () => {
      const incomplete = validTag();
      delete (incomplete as Record<string, unknown>).usage_count;

      const result = validateTag(incomplete);

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });

    it('rejects entry with an extra key', () => {
      const result = validateTag(validTag({ unexpected: 'x' }));

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });
  });
});
