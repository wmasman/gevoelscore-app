import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { validateDate } from '../date';

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
});
