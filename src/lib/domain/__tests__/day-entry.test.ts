import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { validateDayEntry } from '../day-entry';

/** Factory for a minimal valid v1 DayEntry input (raw `unknown` shape that the composer should accept). */
function validEntry(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    date: '2026-05-26',
    score: 4,
    note: null,
    tag_ids: [],
    sub_scores: null,
    sleep_hours: null,
    special_event: null,
    project_entry_ids: [],
    calendar_event_ids: [],
    garmin: null,
    health: null,
    weather: null,
    derived: null,
    created_at: '2026-05-26T08:00:00.000Z',
    updated_at: '2026-05-26T08:00:00.000Z',
    ...overrides,
  };
}

describe('day-entry', () => {
  // Pin "today" so date validation is deterministic across all tests in this file.
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date(2026, 4, 26, 12, 0, 0));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  describe('validateDayEntry — happy path', () => {
    it('accepts a minimal valid v1 entry (all v1.5/v2 fields null/empty)', () => {
      const result = validateDayEntry(validEntry());

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.date).toBe('2026-05-26');
        expect(result.value.score).toBe(4);
        expect(result.value.note).toBeNull();
        expect(result.value.tag_ids).toEqual([]);
        expect(result.value.sub_scores).toBeNull();
        expect(result.value.sleep_hours).toBeNull();
      }
    });

    it('accepts an entry with sub_scores populated (v2 forward-compat)', () => {
      const result = validateDayEntry(
        validEntry({ sub_scores: { cognitive: 4, physical: null, mental: 5 } }),
      );

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.sub_scores).toEqual({
          cognitive: 4,
          physical: null,
          mental: 5,
        });
      }
    });

    it('normalizes whitespace-only note to null', () => {
      const result = validateDayEntry(validEntry({ note: '   \n\t  ' }));

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.note).toBeNull();
      }
    });

    it('trims whitespace from a note', () => {
      const result = validateDayEntry(validEntry({ note: '  hoofdpijn vandaag  ' }));

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.note).toBe('hoofdpijn vandaag');
      }
    });

    it('accepts an entry with sleep_hours populated', () => {
      const result = validateDayEntry(validEntry({ sleep_hours: 7.5 }));

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.sleep_hours).toBe(7.5);
      }
    });
  });

  describe('validateDayEntry — propagates per-field errors', () => {
    it('propagates date errors → invalid_date', () => {
      const result = validateDayEntry(validEntry({ date: '2026-02-30' }));

      expect(result).toEqual({ ok: false, error: 'invalid_date' });
    });

    it('propagates score errors → invalid_score', () => {
      const result = validateDayEntry(validEntry({ score: 11 }));

      expect(result).toEqual({ ok: false, error: 'invalid_score' });
    });

    it('propagates note type errors → invalid_note', () => {
      const result = validateDayEntry(validEntry({ note: 42 }));

      expect(result).toEqual({ ok: false, error: 'invalid_note' });
    });

    it('propagates tag_ids duplicate errors → invalid_tag_ids', () => {
      const result = validateDayEntry(validEntry({ tag_ids: ['a', 'a'] }));

      expect(result).toEqual({ ok: false, error: 'invalid_tag_ids' });
    });

    it('propagates sub_scores errors → invalid_sub_scores', () => {
      const result = validateDayEntry(
        validEntry({ sub_scores: { cognitive: 7, physical: null, mental: null } }),
      );

      expect(result).toEqual({ ok: false, error: 'invalid_sub_scores' });
    });

    it('propagates sleep_hours errors → invalid_sleep_hours', () => {
      const result = validateDayEntry(validEntry({ sleep_hours: 25 }));

      expect(result).toEqual({ ok: false, error: 'invalid_sleep_hours' });
    });

    it('propagates project_entry_ids errors → invalid_project_entry_ids', () => {
      const result = validateDayEntry(validEntry({ project_entry_ids: ['a', 'a'] }));

      expect(result).toEqual({ ok: false, error: 'invalid_project_entry_ids' });
    });

    it('propagates calendar_event_ids errors → invalid_calendar_event_ids', () => {
      const result = validateDayEntry(validEntry({ calendar_event_ids: ['a', 'a'] }));

      expect(result).toEqual({ ok: false, error: 'invalid_calendar_event_ids' });
    });
  });

  describe('validateDayEntry — special_event', () => {
    it('accepts null special_event', () => {
      const result = validateDayEntry(validEntry({ special_event: null }));

      expect(result.ok).toBe(true);
    });

    it('accepts a string special_event (v1.5 forward-compat)', () => {
      const result = validateDayEntry(validEntry({ special_event: 'verjaardag' }));

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.special_event).toBe('verjaardag');
      }
    });

    it('rejects a non-string non-null special_event', () => {
      const result = validateDayEntry(validEntry({ special_event: 42 }));

      expect(result).toEqual({ ok: false, error: 'invalid_special_event' });
    });
  });

  describe('validateDayEntry — v2 fields enforced null in v1', () => {
    it.each([
      ['garmin', { garmin: { rhr: 60 } }],
      ['health', { health: { steps: 8000 } }],
      ['weather', { weather: { temp_avg: 18 } }],
      ['derived', { derived: { activity_load: 'matig' } }],
    ])('rejects non-null %s as invalid_v2_field', (_field, override) => {
      const result = validateDayEntry(validEntry(override));

      expect(result).toEqual({ ok: false, error: 'invalid_v2_field' });
    });
  });

  describe('validateDayEntry — timestamps', () => {
    it('rejects malformed created_at → invalid_created_at', () => {
      const result = validateDayEntry(validEntry({ created_at: 'yesterday' }));

      expect(result).toEqual({ ok: false, error: 'invalid_created_at' });
    });

    it('rejects malformed updated_at → invalid_updated_at', () => {
      const result = validateDayEntry(validEntry({ updated_at: '2026-05-26 08:00' }));

      expect(result).toEqual({ ok: false, error: 'invalid_updated_at' });
    });

    it('rejects created_at > updated_at → invalid_timestamp_order', () => {
      const result = validateDayEntry(
        validEntry({
          created_at: '2026-05-26T10:00:00.000Z',
          updated_at: '2026-05-26T08:00:00.000Z',
        }),
      );

      expect(result).toEqual({ ok: false, error: 'invalid_timestamp_order' });
    });

    it('accepts created_at === updated_at (entry written and not yet edited)', () => {
      const result = validateDayEntry(
        validEntry({
          created_at: '2026-05-26T08:00:00.000Z',
          updated_at: '2026-05-26T08:00:00.000Z',
        }),
      );

      expect(result.ok).toBe(true);
    });
  });

  describe('validateDayEntry — shape', () => {
    it.each([
      ['null', null],
      ['array', [4]],
      ['number', 4],
      ['string', '{}'],
    ])('rejects non-object input %s → invalid_shape', (_label, input) => {
      const result = validateDayEntry(input);

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });

    it('rejects an entry with a missing key', () => {
      const incomplete = validEntry();
      delete (incomplete as Record<string, unknown>).score;

      const result = validateDayEntry(incomplete);

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });

    it('rejects an entry with an extra key', () => {
      const result = validateDayEntry(validEntry({ unexpected: 'x' }));

      expect(result).toEqual({ ok: false, error: 'invalid_shape' });
    });
  });
});
