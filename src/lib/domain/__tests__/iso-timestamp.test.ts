import { describe, expect, it } from 'vitest';
import {
  isIsoUtcTimestamp,
  validateIsoUtcTimestamp,
} from '../iso-timestamp';

describe('iso-timestamp', () => {
  describe('validateIsoUtcTimestamp — accepts valid ISO UTC', () => {
    it('returns ok for full-precision millisecond timestamp', () => {
      const result = validateIsoUtcTimestamp('2026-06-03T10:00:00.000Z');

      expect(result).toEqual({ ok: true, value: '2026-06-03T10:00:00.000Z' });
    });

    it('returns ok for second-precision (no milliseconds)', () => {
      const result = validateIsoUtcTimestamp('2026-06-03T10:00:00Z');

      expect(result).toEqual({ ok: true, value: '2026-06-03T10:00:00Z' });
    });
  });

  describe('validateIsoUtcTimestamp — rejects invalid input', () => {
    it.each([
      ['empty string', ''],
      ['date-only (no time)', '2026-06-03'],
      ['non-UTC offset', '2026-06-03T10:00:00+02:00'],
      ['no timezone marker', '2026-06-03T10:00:00'],
      ['word date', 'yesterday'],
      ['too many ms digits (4)', '2026-06-03T10:00:00.0000Z'],
    ])('returns invalid_iso_timestamp for %s', (_label, input) => {
      const result = validateIsoUtcTimestamp(input);

      expect(result).toEqual({ ok: false, error: 'invalid_iso_timestamp' });
    });

    it.each([
      ['null', null],
      ['undefined', undefined],
      ['number', 1717410000000],
      ['object', { date: '2026-06-03T10:00:00Z' }],
      ['boolean', true],
    ])('returns invalid_iso_timestamp for non-string %s', (_label, input) => {
      const result = validateIsoUtcTimestamp(input);

      expect(result).toEqual({ ok: false, error: 'invalid_iso_timestamp' });
    });

    it('returns invalid_iso_timestamp for syntactically-valid but impossible date', () => {
      // Regex passes but Date parsing rejects month 13 — the new Date()
      // round-trip is the guard.
      const result = validateIsoUtcTimestamp('2026-13-99T00:00:00Z');

      expect(result).toEqual({ ok: false, error: 'invalid_iso_timestamp' });
    });
  });

  describe('isIsoUtcTimestamp — type-guard convenience export', () => {
    it('returns true for valid ISO UTC', () => {
      expect(isIsoUtcTimestamp('2026-06-03T10:00:00.000Z')).toBe(true);
    });

    it('returns false for invalid input', () => {
      expect(isIsoUtcTimestamp('')).toBe(false);
      expect(isIsoUtcTimestamp(null)).toBe(false);
      expect(isIsoUtcTimestamp('2026-06-03')).toBe(false);
    });
  });
});
