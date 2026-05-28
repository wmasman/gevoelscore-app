import type { DayEntry } from './day-entry';

// currentStreak — counts the number of consecutive logged days walking
// back from `today` (inclusive). If `today` itself is unlogged, the walk
// starts from yesterday — the cardinal principle is "logged today is a
// great day", but a missing today shouldn't reset a long streak before
// the user has even finished the day.
//
// Stops at the first gap. Returns 0 if both today and yesterday are
// unlogged (no streak to claim — same rule as the existing Google Sheet
// the user has been keeping for 1,363 days).
//
// Date arithmetic uses UTC noon to dodge DST transitions: any date string
// at noon UTC parses to a stable wall-clock day in Europe/Amsterdam, and
// subtracting 24h always lands on the previous calendar day.

export function currentStreak(entries: DayEntry[], today: string): number {
  if (entries.length === 0) return 0;

  const logged = new Set(entries.map((e) => e.date));

  // Determine the starting point: today if logged, else yesterday if
  // logged, else 0.
  let cursor: string;
  if (logged.has(today)) {
    cursor = today;
  } else {
    const yesterday = shiftDate(today, -1);
    if (!logged.has(yesterday)) return 0;
    cursor = yesterday;
  }

  let count = 0;
  while (logged.has(cursor)) {
    count += 1;
    cursor = shiftDate(cursor, -1);
  }
  return count;
}

function shiftDate(date: string, days: number): string {
  // Anchor on UTC noon so DST shifts can't push us across day boundaries.
  const parsed = new Date(`${date}T12:00:00Z`);
  parsed.setUTCDate(parsed.getUTCDate() + days);
  const y = parsed.getUTCFullYear();
  const m = String(parsed.getUTCMonth() + 1).padStart(2, '0');
  const d = String(parsed.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}
