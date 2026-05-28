import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { formatDateDutch, todayInAmsterdam, validateDate } from '../date';

describe('date', () => {
  describe('validateDate — with today pinned to 2026-05-26', () => {
    beforeEach(() => {
      vi.useFakeTimers();
      // 2026-05-26 local time (month is 0-indexed in JS Date constructor).
      vi.setSystemTime(new Date(2026, 4, 26, 12, 0, 0));
    });

    afterEach(() => {
      vi.useRealTimers();
    });

    it('given today (2026-05-26), when validated, then it is accepted', () => {
      const result = validateDate('2026-05-26');

      expect(result).toEqual({ ok: true, value: '2026-05-26' });
    });

    it('given yesterday (2026-05-25), when validated, then it is accepted', () => {
      const result = validateDate('2026-05-25');

      expect(result).toEqual({ ok: true, value: '2026-05-25' });
    });

    it("given the user's first logging day (2022-09-03), when validated, then it is accepted", () => {
      const result = validateDate('2022-09-03');

      expect(result).toEqual({ ok: true, value: '2022-09-03' });
    });

    it('given tomorrow (2026-05-27), when validated, then it returns future_date', () => {
      const result = validateDate('2026-05-27');

      expect(result).toEqual({ ok: false, error: 'future_date' });
    });

    it('given a far-future date (2030-01-01), when validated, then it returns future_date', () => {
      const result = validateDate('2030-01-01');

      expect(result).toEqual({ ok: false, error: 'future_date' });
    });
  });

  describe('validateDate — rejects bad format', () => {
    it.each([
      '2026/05/26',
      'May 26',
      '2026-5-26',
      '20260526',
      '',
      '2026-05-26T00:00:00Z',
      '2026-05-26 ',
    ])('given format %j, when validated, then it returns invalid_format', (input) => {
      const result = validateDate(input);

      expect(result).toEqual({ ok: false, error: 'invalid_format' });
    });
  });

  describe('validateDate — rejects calendar-impossible dates', () => {
    it.each([
      '2026-02-30',
      '2026-13-01',
      '2026-00-15',
      '2026-04-31',
      '2025-02-29',
    ])('given %s, when validated, then it returns invalid_calendar_date', (input) => {
      const result = validateDate(input);

      expect(result).toEqual({ ok: false, error: 'invalid_calendar_date' });
    });

    it('given 2024-02-29 (real leap-year date), when validated (with today pinned), then it is accepted', () => {
      vi.useFakeTimers();
      vi.setSystemTime(new Date(2026, 4, 26));

      const result = validateDate('2024-02-29');

      expect(result).toEqual({ ok: true, value: '2024-02-29' });

      vi.useRealTimers();
    });
  });

  describe('validateDate — rejects non-string', () => {
    it.each([
      ['number', 20260526],
      ['null', null],
      ['undefined', undefined],
      ['object', {}],
      ['array', ['2026-05-26']],
      ['Date instance', new Date('2026-05-26')],
      ['boolean', true],
    ])('given %s, when validated, then it returns wrong_type', (_label, input) => {
      const result = validateDate(input);

      expect(result).toEqual({ ok: false, error: 'wrong_type' });
    });
  });

  describe('todayInAmsterdam', () => {
    afterEach(() => {
      vi.useRealTimers();
    });

    it('returns a YYYY-MM-DD shaped string', () => {
      const result = todayInAmsterdam();
      expect(result).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    });

    it('returns the Amsterdam-local date at 2026-05-28 09:00 UTC', () => {
      vi.useFakeTimers();
      vi.setSystemTime(new Date('2026-05-28T09:00:00Z'));
      // Amsterdam is CEST (UTC+2) in May → same calendar day.
      expect(todayInAmsterdam()).toBe('2026-05-28');
    });

    it('returns the NEXT Amsterdam-local date when UTC is still on the previous day', () => {
      vi.useFakeTimers();
      // 2026-05-27 23:30 UTC = 2026-05-28 01:30 CEST.
      vi.setSystemTime(new Date('2026-05-27T23:30:00Z'));
      expect(todayInAmsterdam()).toBe('2026-05-28');
    });

    it('returns the PREVIOUS Amsterdam-local date when UTC has rolled to the next day but Amsterdam has not (winter, no DST)', () => {
      vi.useFakeTimers();
      // 2026-01-01 00:30 UTC = 2026-01-01 01:30 CET → same calendar day.
      // Edge case: at exactly the moment Amsterdam ticks to a new day before UTC.
      // 2026-01-01 00:30 CET = 2025-12-31 23:30 UTC → so Amsterdam date precedes UTC by a day at the end.
      vi.setSystemTime(new Date('2025-12-31T23:30:00Z'));
      expect(todayInAmsterdam()).toBe('2026-01-01');
    });
  });

  describe('formatDateDutch', () => {
    it('formats a midweek day', () => {
      expect(formatDateDutch('2026-05-27')).toBe('woensdag 27 mei 2026');
    });

    it('formats a weekend day', () => {
      expect(formatDateDutch('2026-05-30')).toBe('zaterdag 30 mei 2026');
    });

    it('formats a January day', () => {
      expect(formatDateDutch('2026-01-15')).toBe('donderdag 15 januari 2026');
    });
  });
});
