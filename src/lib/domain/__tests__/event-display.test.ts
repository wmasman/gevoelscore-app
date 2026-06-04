import { describe, expect, it } from 'vitest';
import {
  formatDutchDate,
  formatDutchTime,
  formatEventDateTime,
} from '../event-display';

describe('event-display', () => {
  describe('formatDutchDate', () => {
    it('formats a midweek date in Dutch', () => {
      // 2026-06-04 is a Thursday
      const d = new Date(2026, 5, 4); // local-time constructor
      expect(formatDutchDate(d)).toBe('donderdag 4 juni 2026');
    });

    it('handles year + month boundaries', () => {
      const d = new Date(2026, 0, 1); // 1 jan 2026 (Thursday)
      expect(formatDutchDate(d)).toBe('donderdag 1 januari 2026');
    });
  });

  describe('formatDutchTime', () => {
    it('formats HH:mm with zero padding', () => {
      const d = new Date(2026, 5, 4, 9, 5);
      expect(formatDutchTime(d)).toBe('09:05');
    });

    it('formats midnight as 00:00', () => {
      const d = new Date(2026, 5, 4, 0, 0);
      expect(formatDutchTime(d)).toBe('00:00');
    });
  });

  describe('formatEventDateTime', () => {
    it('all-day events render date only', () => {
      const start = new Date(2026, 5, 4, 0, 0);
      const end = new Date(2026, 5, 5, 0, 0);
      expect(formatEventDateTime(start, end, true)).toBe('donderdag 4 juni 2026');
    });

    it('same-day timed events render date + time range with en-dash', () => {
      const start = new Date(2026, 5, 4, 10, 0);
      const end = new Date(2026, 5, 4, 11, 0);
      expect(formatEventDateTime(start, end, false)).toBe(
        'donderdag 4 juni 2026, 10:00 – 11:00',
      );
    });

    it('multi-day timed events render both date+time blocks', () => {
      const start = new Date(2026, 5, 4, 14, 0);
      const end = new Date(2026, 5, 5, 11, 0);
      expect(formatEventDateTime(start, end, false)).toBe(
        'donderdag 4 juni 2026, 14:00 – vrijdag 5 juni 2026, 11:00',
      );
    });
  });
});
