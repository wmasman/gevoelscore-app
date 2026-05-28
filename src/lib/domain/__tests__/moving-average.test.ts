import { describe, expect, it } from 'vitest';
import type { DayEntry } from '../day-entry';
import { movingAverage, MIN_WINDOW_PRESENT } from '../moving-average';

function entry(date: string, score: number): DayEntry {
  return {
    date,
    score: score as DayEntry['score'],
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
    created_at: `${date}T08:00:00.000Z`,
    updated_at: `${date}T08:00:00.000Z`,
  };
}

describe('movingAverage', () => {
  it('returns one row per day in [from, to] inclusive', () => {
    const result = movingAverage([], 7, '2026-05-20', '2026-05-22');
    expect(result.map((r) => r.date)).toEqual([
      '2026-05-20',
      '2026-05-21',
      '2026-05-22',
    ]);
  });

  it('returns average: null for every day when no entries logged', () => {
    const result = movingAverage([], 7, '2026-05-20', '2026-05-22');
    expect(result.every((r) => r.average === null)).toBe(true);
  });

  it('emits null until window has MIN_WINDOW_PRESENT logged days', () => {
    // 7-day trailing window, MIN_WINDOW_PRESENT=3.
    // Only 2 of the 7 trailing days logged → average still null on day 2.
    // On day 3, the 3rd entry tips into "≥3 present", so average emits.
    const entries = [
      entry('2026-05-20', 5),
      entry('2026-05-21', 7),
      entry('2026-05-22', 6),
    ];
    const result = movingAverage(entries, 7, '2026-05-20', '2026-05-22');
    expect(result[0]!.average).toBe(null); // window has 1 present
    expect(result[1]!.average).toBe(null); // window has 2 present
    // window has 3 present, average of [5,7,6] = 6
    expect(result[2]!.average).toBe(6);
  });

  it('computes average over present days only (skips missing)', () => {
    // 7-day trailing window ending 2026-05-26.
    // Present days in window: 20, 22, 24, 25, 26 (5 of 7) → avg of [5,7,4,8,6]
    const entries = [
      entry('2026-05-20', 5),
      // gap 21
      entry('2026-05-22', 7),
      // gap 23
      entry('2026-05-24', 4),
      entry('2026-05-25', 8),
      entry('2026-05-26', 6),
    ];
    const result = movingAverage(entries, 7, '2026-05-26', '2026-05-26');
    // (5 + 7 + 4 + 8 + 6) / 5 = 6
    expect(result[0]!.average).toBe(6);
  });

  it('window strictly trails: a day outside [date-windowDays+1, date] is excluded', () => {
    const entries = [
      entry('2026-05-19', 1), // 8 days before 26, OUT of 7-day window
      entry('2026-05-20', 5),
      entry('2026-05-21', 5),
      entry('2026-05-22', 5),
      entry('2026-05-23', 5),
      entry('2026-05-24', 5),
      entry('2026-05-25', 5),
      entry('2026-05-26', 5),
    ];
    // Window for 2026-05-26 is [2026-05-20 .. 2026-05-26] (7 days inclusive)
    // The score=1 on May 19 must NOT pull the average down.
    const result = movingAverage(entries, 7, '2026-05-26', '2026-05-26');
    expect(result[0]!.average).toBe(5);
  });

  it('average reacts to the trailing window as it advances', () => {
    // Constant 5 from May 20-26, then 10 on May 27 + 28.
    // On May 27: window = [21..27], values = [5,5,5,5,5,5,10] = 45/7 ≈ 6.43
    // On May 28: window = [22..28], values = [5,5,5,5,5,10,10] = 45/7 ≈ 6.43... wait
    // = (5*5 + 10*2)/7 = 45/7 ≈ 6.43. Same? Let me redo.
    // 22..28: 22=5, 23=5, 24=5, 25=5, 26=5, 27=10, 28=10 → (5*5+10*2)/7 = (25+20)/7 = 45/7
    // 21..27: 21=5, 22=5, 23=5, 24=5, 25=5, 26=5, 27=10 → (5*6+10)/7 = 40/7
    const entries = [
      entry('2026-05-20', 5),
      entry('2026-05-21', 5),
      entry('2026-05-22', 5),
      entry('2026-05-23', 5),
      entry('2026-05-24', 5),
      entry('2026-05-25', 5),
      entry('2026-05-26', 5),
      entry('2026-05-27', 10),
      entry('2026-05-28', 10),
    ];
    const result = movingAverage(entries, 7, '2026-05-27', '2026-05-28');
    expect(result[0]!.average).toBeCloseTo(40 / 7, 5);
    expect(result[1]!.average).toBeCloseTo(45 / 7, 5);
  });

  it('handles year boundary correctly (date arithmetic via UTC noon)', () => {
    const entries = [
      entry('2025-12-29', 4),
      entry('2025-12-30', 5),
      entry('2025-12-31', 6),
      entry('2026-01-01', 7),
      entry('2026-01-02', 8),
    ];
    // On 2026-01-02, 7-day window = [2025-12-27 .. 2026-01-02]
    // Present: 29,30,31,01,02 = [4,5,6,7,8] → avg 6
    const result = movingAverage(entries, 7, '2026-01-02', '2026-01-02');
    expect(result[0]!.average).toBe(6);
  });

  it('exposes MIN_WINDOW_PRESENT >= 2 (smoothing requires more than one sample)', () => {
    expect(MIN_WINDOW_PRESENT).toBeGreaterThanOrEqual(2);
  });
});
