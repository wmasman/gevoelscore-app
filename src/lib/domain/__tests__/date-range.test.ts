import { describe, expect, it } from 'vitest';
import { validateDateRange } from '../date-range';

describe('date-range', () => {
  describe('validateDateRange — accepts valid ranges', () => {
    it('given a valid start_date and null end_date, then returns ok (ongoing episode)', () => {
      const result = validateDateRange('2026-06-02', null);

      expect(result).toEqual({
        ok: true,
        value: { start_date: '2026-06-02', end_date: null },
      });
    });

    it('given a valid start_date and a later end_date, then returns ok (closed range)', () => {
      const result = validateDateRange('2026-04-01', '2026-05-15');

      expect(result).toEqual({
        ok: true,
        value: { start_date: '2026-04-01', end_date: '2026-05-15' },
      });
    });

    it('given start_date == end_date, then returns ok (single-day episode is OK)', () => {
      const result = validateDateRange('2026-06-02', '2026-06-02');

      expect(result).toEqual({
        ok: true,
        value: { start_date: '2026-06-02', end_date: '2026-06-02' },
      });
    });

    it('given a future start_date, then returns ok (no upper bound on start_date)', () => {
      const result = validateDateRange('2099-12-31', null);

      expect(result).toEqual({
        ok: true,
        value: { start_date: '2099-12-31', end_date: null },
      });
    });
  });

  describe('validateDateRange — rejects ordering violations', () => {
    it('given end_date strictly before start_date, then returns end_before_start', () => {
      const result = validateDateRange('2026-06-02', '2026-06-01');

      expect(result).toEqual({ ok: false, error: 'end_before_start' });
    });
  });

  describe('validateDateRange — rejects malformed start_date', () => {
    it.each([
      ['out-of-range month', '2026-13-01'],
      ['slash separator', '2026/06/01'],
      ['empty string', ''],
      ['short year', '26-06-01'],
      ['extra suffix', '2026-06-01T00:00:00Z'],
      ['invalid calendar date', '2026-02-30'],
    ])(
      'given start_date %s (%j), then returns invalid_start_date',
      (_label, input) => {
        const result = validateDateRange(input, null);

        expect(result).toEqual({ ok: false, error: 'invalid_start_date' });
      },
    );
  });

  describe('validateDateRange — rejects malformed end_date when non-null', () => {
    it.each([
      ['out-of-range month', '2026-13-01'],
      ['slash separator', '2026/06/01'],
      ['empty string', ''],
      ['invalid calendar date', '2026-02-30'],
    ])(
      'given valid start and malformed end %s (%j), then returns invalid_end_date',
      (_label, input) => {
        const result = validateDateRange('2026-06-02', input);

        expect(result).toEqual({ ok: false, error: 'invalid_end_date' });
      },
    );
  });

  describe('validateDateRange — rejects non-string inputs', () => {
    it.each([
      ['number', 20260602],
      ['null', null],
      ['undefined', undefined],
      ['object', { date: '2026-06-02' }],
      ['boolean', true],
    ])(
      'given start_date as %s, then returns invalid_start_date',
      (_label, input) => {
        const result = validateDateRange(input, null);

        expect(result).toEqual({ ok: false, error: 'invalid_start_date' });
      },
    );

    it.each([
      ['number', 20260602],
      ['object', { date: '2026-06-02' }],
      ['boolean', true],
    ])(
      'given valid start and end_date as %s, then returns invalid_end_date',
      (_label, input) => {
        const result = validateDateRange('2026-06-02', input);

        expect(result).toEqual({ ok: false, error: 'invalid_end_date' });
      },
    );
  });

  describe('validateDateRange — undefined end_date is not the same as null', () => {
    it('given end_date undefined (not null), then returns invalid_end_date (ongoing must be expressed as null)', () => {
      // Only `null` means "ongoing". `undefined` is a programmer error — most
      // likely a missing field — and must surface as a validation failure
      // rather than be silently coerced to null.
      const result = validateDateRange('2026-06-02', undefined);

      expect(result).toEqual({ ok: false, error: 'invalid_end_date' });
    });
  });
});
