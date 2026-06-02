'use client';

// TimelineView — Blok 2 of the daily flow. Renders:
//   - streak counter ("X dagen achter elkaar")
//   - 30/90-day toggle
//   - line chart of recent scores
//   - tap-any-day → opens the QuickEntryFlow popout for that date with
//     isPastDay=true (the popout is the single canonical edit surface
//     across the app post-Step-5)
//
// Data architecture:
//   - 30-day range is server-rendered in page.tsx and flows through as
//     `initialEntries`. The view READS THE PROP DIRECTLY for range=30 —
//     no useState shadow. Saves trigger router.refresh() inside
//     useDayEntryUpsert; the server component re-runs and a fresh
//     initialEntries arrives.
//   - 90-day range is client-fetched on first toggle into a local
//     cache (`range90Entries`). When a save fires while range=90 is
//     active we refetch the 90d window — router.refresh only
//     refreshes server data (the 30d window).

import { useCallback, useEffect, useMemo, useState } from 'react';
import { QuickEntryFlow } from '@/components/lab/quick-entry-flow';
import { ScoreChart } from '@/components/score-chart';
import { ScoreHeatmap } from '@/components/score-heatmap';
import { useMergedSaveStatus } from '@/components/save-status-context';
import { copy } from '@/copy';
import { currentStreak } from '@/lib/domain/streak';
import type { DayEntry } from '@/lib/domain/day-entry';
import type { Tag } from '@/lib/domain/tag';

type Range = 30 | 90;
type View = 'chart' | 'heatmap';

type Props = {
  today: string;
  initialEntries: DayEntry[];
  allTags: Tag[];
  /**
   * Tag-recency map derived from the 30-day timelineEntries window
   * by the parent (TodayShell). Forwarded into the past-day-edit
   * popout's QuickEntryFlow so the within-category sort applies in
   * BOTH today's flow and past-day editing. Optional with a {} default
   * to keep this component's existing tests + standalone use safe.
   */
  recencyByTagId?: Record<string, string>;
};

function shiftDate(date: string, days: number): string {
  const parsed = new Date(`${date}T12:00:00Z`);
  parsed.setUTCDate(parsed.getUTCDate() + days);
  const y = parsed.getUTCFullYear();
  const m = String(parsed.getUTCMonth() + 1).padStart(2, '0');
  const d = String(parsed.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export function TimelineView({
  today,
  initialEntries,
  allTags,
  recencyByTagId = {},
}: Props) {
  const [range, setRange] = useState<Range>(30);
  const [view, setView] = useState<View>('chart');
  // 30d entries come straight from the prop — no shadow. 90d is a
  // client-side lazy cache; null means "not fetched yet for this
  // session," in which case we fall back to the 30d prop so the chart
  // never renders empty mid-toggle.
  const [range90Entries, setRange90Entries] = useState<DayEntry[] | null>(null);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const merged = useMergedSaveStatus();

  const fromForRange = useMemo<Record<Range, string>>(
    () => ({
      30: shiftDate(today, -29),
      90: shiftDate(today, -89),
    }),
    [today],
  );

  const fetchRange90 = useCallback(async (): Promise<void> => {
    const from = fromForRange[90];
    try {
      const res = await fetch(
        `/api/day-entries?from=${from}&to=${today}`,
        { credentials: 'same-origin' },
      );
      if (!res.ok) return;
      const data = (await res.json()) as { entries?: DayEntry[] };
      if (Array.isArray(data.entries)) setRange90Entries(data.entries);
    } catch {
      // Network failure — leave whatever's there. The sheet's own save
      // flow surfaces errors; the timeline read is best-effort.
    }
  }, [fromForRange, today]);

  function onRangeChange(r: Range): void {
    if (r === range) return;
    setRange(r);
    // M-M4: auto-switch to Heatmap at 90 days. The line chart's per-
    // day stride at 90d (~3.8px on a 390px viewport) overlaps adjacent
    // hit-zones up to 6 days deep, making per-day drill-down
    // unreliable. The 44x44 heatmap cells are touch-correct at any
    // range. User can still flip back to Lijn manually.
    if (r === 90) setView('heatmap');
    if (r === 90 && range90Entries === null) void fetchRange90();
  }

  // When a save lands and the user is currently looking at the 90d
  // window, refresh the cache. The 30d window picks up automatically
  // via router.refresh (server re-runs, new initialEntries prop).
  useEffect(() => {
    if (merged.status === 'saved' && range === 90) {
      void fetchRange90();
    }
  }, [merged.status, range, fetchRange90]);

  const entries = range === 30 ? initialEntries : (range90Entries ?? initialEntries);
  const streak = currentStreak(entries, today);
  const selectedEntry =
    selectedDate === null
      ? null
      : (entries.find((e) => e.date === selectedDate) ?? null);

  return (
    <section
      aria-label={copy.timeline.title}
      className="flex flex-col gap-4"
    >
      {/* No visible h2 — the active "Tijdlijn" tab already names this
          section. Screen readers still get the section via aria-label. */}
      <header className="flex items-baseline justify-end gap-3">
        <div
          role="radiogroup"
          aria-label={copy.timeline.rangeAriaLabel}
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

      <div className="flex items-baseline justify-between gap-3">
        <p className="text-base text-fg-muted">
          {streak > 0 ? copy.timeline.streak(streak) : ''}
        </p>
        <div
          role="radiogroup"
          aria-label={copy.timeline.viewAriaLabel}
          className="flex items-center gap-1 text-sm"
        >
          <button
            type="button"
            role="radio"
            aria-checked={view === 'chart'}
            onClick={() => setView('chart')}
            className={
              view === 'chart'
                ? 'rounded-md bg-accent-soft px-3 py-1 font-medium text-fg ring-1 ring-accent'
                : 'rounded-md px-3 py-1 text-fg-muted hover:bg-surface-muted'
            }
          >
            {copy.timeline.viewChart}
          </button>
          <button
            type="button"
            role="radio"
            aria-checked={view === 'heatmap'}
            onClick={() => setView('heatmap')}
            className={
              view === 'heatmap'
                ? 'rounded-md bg-accent-soft px-3 py-1 font-medium text-fg ring-1 ring-accent'
                : 'rounded-md px-3 py-1 text-fg-muted hover:bg-surface-muted'
            }
          >
            {copy.timeline.viewHeatmap}
          </button>
        </div>
      </div>

      {view === 'chart' ? (
        <>
          <ScoreChart
            entries={entries}
            from={fromForRange[range]}
            to={today}
            onPointTap={(date) => setSelectedDate(date)}
          />
          <p className="text-xs text-fg-subtle">{copy.timeline.maSubtitle}</p>
        </>
      ) : (
        <ScoreHeatmap
          entries={entries}
          from={fromForRange[range]}
          to={today}
          onCellTap={(date) => setSelectedDate(date)}
        />
      )}

      <QuickEntryFlow
        date={selectedDate ?? today}
        initialEntry={selectedDate !== null ? selectedEntry : null}
        allTags={allTags}
        recencyByTagId={recencyByTagId}
        open={selectedDate !== null}
        startStep="score"
        isPastDay={selectedDate !== null && selectedDate !== today}
        onClose={() => setSelectedDate(null)}
        onComplete={() => setSelectedDate(null)}
      />
    </section>
  );
}
