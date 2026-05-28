import type { DayEntry } from './day-entry';

// movingAverage — trailing N-day average for each calendar day in [from, to].
//
// Semantics:
//   - "Trailing": the window for day D is [D - windowDays + 1, D], inclusive.
//   - Missing days are skipped, not interpolated. The denominator is the
//     count of *present* days in the window (honest data — same principle
//     as ScoreChart's gap rendering).
//   - If fewer than MIN_WINDOW_PRESENT days are present in the window, the
//     average is reported as null. Two reasons:
//       (a) one or two samples is not a meaningful smoothing — a single
//           score-3 day would yank the "average" line to 3, defeating the
//           point of the moving average.
//       (b) the start of a fresh user's data should not have a synthetic
//           "average" line that's just the first datapoint repeated.
//
// Date arithmetic uses UTC noon to dodge DST boundaries — same convention
// as streak.ts and score-chart.tsx.

export const MIN_WINDOW_PRESENT = 3;

export type MovingAveragePoint = {
  date: string;
  average: number | null;
};

export function movingAverage(
  entries: DayEntry[],
  windowDays: number,
  from: string,
  to: string,
): MovingAveragePoint[] {
  const byDate = new Map<string, number>();
  for (const e of entries) byDate.set(e.date, e.score);

  const total = daysBetween(from, to) + 1;
  const out: MovingAveragePoint[] = [];

  for (let i = 0; i < total; i += 1) {
    const day = shiftDate(from, i);
    let sum = 0;
    let count = 0;
    for (let k = 0; k < windowDays; k += 1) {
      const probe = shiftDate(day, -k);
      const v = byDate.get(probe);
      if (v !== undefined) {
        sum += v;
        count += 1;
      }
    }
    out.push({
      date: day,
      average: count >= MIN_WINDOW_PRESENT ? sum / count : null,
    });
  }
  return out;
}

function daysBetween(from: string, to: string): number {
  const a = new Date(`${from}T12:00:00Z`).getTime();
  const b = new Date(`${to}T12:00:00Z`).getTime();
  return Math.round((b - a) / (24 * 60 * 60 * 1000));
}

function shiftDate(date: string, days: number): string {
  const parsed = new Date(`${date}T12:00:00Z`);
  parsed.setUTCDate(parsed.getUTCDate() + days);
  const y = parsed.getUTCFullYear();
  const m = String(parsed.getUTCMonth() + 1).padStart(2, '0');
  const d = String(parsed.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}
