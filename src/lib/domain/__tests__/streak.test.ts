import { describe, expect, it } from 'vitest';
import type { DayEntry } from '../day-entry';
import { currentStreak } from '../streak';

// The streak counts consecutive logged days walking back from "today" (or
// yesterday if today is missing). Stops at the first gap. Used by the
// timeline view's streak counter.

function entry(date: string): DayEntry {
  return {
    date,
    score: 5 as DayEntry['score'],
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

describe('currentStreak', () => {
  it('returns 0 when the entry list is empty', () => {
    expect(currentStreak([], '2026-05-28')).toBe(0);
  });

  it('today logged + yesterday logged + day before → 3', () => {
    const entries = [
      entry('2026-05-26'),
      entry('2026-05-27'),
      entry('2026-05-28'),
    ];
    expect(currentStreak(entries, '2026-05-28')).toBe(3);
  });

  it('today missing + yesterday logged + day before → 2 (walks back from yesterday)', () => {
    const entries = [
      entry('2026-05-26'),
      entry('2026-05-27'),
    ];
    expect(currentStreak(entries, '2026-05-28')).toBe(2);
  });

  it('today logged + yesterday missing → 1 (today only)', () => {
    const entries = [
      entry('2026-05-26'),
      entry('2026-05-28'),
    ];
    expect(currentStreak(entries, '2026-05-28')).toBe(1);
  });

  it('entries with gaps further back do not extend the streak', () => {
    const entries = [
      entry('2026-05-20'),
      entry('2026-05-21'),
      // gap at 2026-05-22
      entry('2026-05-23'),
      entry('2026-05-24'),
      entry('2026-05-25'),
      entry('2026-05-26'),
      entry('2026-05-27'),
      entry('2026-05-28'),
    ];
    // Walks back from 2026-05-28 → 23 (6 days), stops at the 2026-05-22 gap.
    expect(currentStreak(entries, '2026-05-28')).toBe(6);
  });

  it('handles year boundary (Dec 31 → Jan 1) correctly', () => {
    const entries = [
      entry('2025-12-30'),
      entry('2025-12-31'),
      entry('2026-01-01'),
      entry('2026-01-02'),
    ];
    expect(currentStreak(entries, '2026-01-02')).toBe(4);
  });

  it('today AND yesterday missing → 0', () => {
    const entries = [
      entry('2026-05-25'),
      entry('2026-05-26'),
    ];
    // Today is 2026-05-28; yesterday 2026-05-27 also missing.
    expect(currentStreak(entries, '2026-05-28')).toBe(0);
  });
});
