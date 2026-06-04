import { describe, expect, it } from 'vitest';
import { relativeDutchTime } from '../relative-dutch-time';

const NOW = new Date('2026-06-04T12:00:00Z');

describe('relativeDutchTime', () => {
  it('returns "zojuist" for less than a minute ago', () => {
    expect(relativeDutchTime(new Date('2026-06-04T11:59:30Z'), NOW)).toBe('zojuist');
  });

  it('returns "X min geleden" for minutes', () => {
    expect(relativeDutchTime(new Date('2026-06-04T11:55:00Z'), NOW)).toBe('5 min geleden');
  });

  it('returns "1 uur geleden" for exactly one hour', () => {
    expect(relativeDutchTime(new Date('2026-06-04T11:00:00Z'), NOW)).toBe('1 uur geleden');
  });

  it('returns "X uur geleden" for multi-hour', () => {
    expect(relativeDutchTime(new Date('2026-06-04T07:00:00Z'), NOW)).toBe('5 uur geleden');
  });

  it('returns "gisteren" for ~24h ago', () => {
    expect(relativeDutchTime(new Date('2026-06-03T12:00:00Z'), NOW)).toBe('gisteren');
  });

  it('returns "X dagen geleden" for several days', () => {
    expect(relativeDutchTime(new Date('2026-06-01T12:00:00Z'), NOW)).toBe('3 dagen geleden');
  });

  it('returns "1 week geleden" for ~7 days', () => {
    expect(relativeDutchTime(new Date('2026-05-28T12:00:00Z'), NOW)).toBe('1 week geleden');
  });

  it('returns "X weken geleden" for multi-week', () => {
    expect(relativeDutchTime(new Date('2026-05-14T12:00:00Z'), NOW)).toBe('3 weken geleden');
  });

  it('returns "1 maand geleden" for ~30 days', () => {
    expect(relativeDutchTime(new Date('2026-05-04T12:00:00Z'), NOW)).toBe('1 maand geleden');
  });

  it('returns "X jaar geleden" for years', () => {
    expect(relativeDutchTime(new Date('2024-06-04T12:00:00Z'), NOW)).toBe('2 jaar geleden');
  });

  it('returns "zojuist" for future timestamps (defensive)', () => {
    expect(relativeDutchTime(new Date('2026-06-04T13:00:00Z'), NOW)).toBe('zojuist');
  });
});
