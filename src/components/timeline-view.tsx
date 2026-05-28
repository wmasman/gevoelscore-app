'use client';

// TimelineView — Blok 2 of the daily flow. Renders:
//   - streak counter ("X dagen achter elkaar")
//   - 30/90-day toggle
//   - line chart of recent scores
//   - tap-any-day → bottom sheet for that date (DayDetailSheet, which
//     reuses DayEntryEditor for the actual editing)
//
// Server component pre-fetches the 30-day window so first paint has data;
// 90-day window is lazy on first toggle. After any save in the sheet, the
// view re-fetches its current range (simplest correct behaviour — for v1's
// scale a 30/90-row read is cheap; replace with local patching if it ever
// matters).

import { useMemo, useState } from 'react';
import { DayDetailSheet } from '@/components/day-detail-sheet';
import { ScoreChart } from '@/components/score-chart';
import { copy } from '@/copy';
import { currentStreak } from '@/lib/domain/streak';
import type { DayEntry } from '@/lib/domain/day-entry';
import type { Tag } from '@/lib/domain/tag';

type Range = 30 | 90;

type Props = {
  today: string;
  initialEntries: DayEntry[];
  allTags: Tag[];
};

function shiftDate(date: string, days: number): string {
  const parsed = new Date(`${date}T12:00:00Z`);
  parsed.setUTCDate(parsed.getUTCDate() + days);
  const y = parsed.getUTCFullYear();
  const m = String(parsed.getUTCMonth() + 1).padStart(2, '0');
  const d = String(parsed.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export function TimelineView({ today, initialEntries, allTags }: Props) {
  const [range, setRange] = useState<Range>(30);
  const [entries, setEntries] = useState<DayEntry[]>(initialEntries);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);

  const fromForRange = useMemo<Record<Range, string>>(
    () => ({
      30: shiftDate(today, -29),
      90: shiftDate(today, -89),
    }),
    [today],
  );

  async function fetchRange(r: Range): Promise<void> {
    const from = fromForRange[r];
    try {
      const res = await fetch(
        `/api/day-entries?from=${from}&to=${today}`,
        { credentials: 'same-origin' },
      );
      if (!res.ok) return;
      const data = (await res.json()) as { entries?: DayEntry[] };
      if (Array.isArray(data.entries)) setEntries(data.entries);
    } catch {
      // Network failure — keep showing current entries. The sheet's own
      // save flow surfaces errors; the timeline read is best-effort.
    }
  }

  function onRangeChange(r: Range): void {
    if (r === range) return;
    setRange(r);
    void fetchRange(r);
  }

  function onSavedInSheet(): void {
    // Re-read the current range so the chart reflects the new value.
    void fetchRange(range);
  }

  const streak = currentStreak(entries, today);
  const selectedEntry =
    selectedDate === null
      ? null
      : (entries.find((e) => e.date === selectedDate) ?? null);

  return (
    <section
      aria-labelledby="timeline-heading"
      className="flex flex-col gap-4"
    >
      <header className="flex items-baseline justify-between gap-3">
        <h2 id="timeline-heading" className="text-2xl font-semibold">
          {copy.timeline.title}
        </h2>
        <div
          role="radiogroup"
          aria-label="Bereik"
          className="flex items-center gap-1 text-sm"
        >
          <button
            type="button"
            role="radio"
            aria-checked={range === 30}
            onClick={() => onRangeChange(30)}
            className={
              range === 30
                ? 'rounded-md bg-accent-soft px-3 py-1 font-medium text-fg ring-1 ring-accent'
                : 'rounded-md px-3 py-1 text-fg-muted hover:bg-surface-muted'
            }
          >
            {copy.timeline.range30}
          </button>
          <button
            type="button"
            role="radio"
            aria-checked={range === 90}
            onClick={() => onRangeChange(90)}
            className={
              range === 90
                ? 'rounded-md bg-accent-soft px-3 py-1 font-medium text-fg ring-1 ring-accent'
                : 'rounded-md px-3 py-1 text-fg-muted hover:bg-surface-muted'
            }
          >
            {copy.timeline.range90}
          </button>
        </div>
      </header>

      <p className="text-base text-fg-muted">
        {streak > 0 ? copy.timeline.streak(streak) : '—'}
      </p>

      <ScoreChart
        entries={entries}
        from={fromForRange[range]}
        to={today}
        onPointTap={(date) => setSelectedDate(date)}
      />

      {selectedDate !== null && (
        <DayDetailSheet
          date={selectedDate}
          entry={selectedEntry}
          allTags={allTags}
          onClose={() => setSelectedDate(null)}
          onSaved={onSavedInSheet}
        />
      )}
    </section>
  );
}
