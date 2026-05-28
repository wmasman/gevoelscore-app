'use client';

// Today + Tijdlijn — two sibling views inside one screen. Step 6 added the
// timeline; the two views live in a horizontal scroll-snap container so
// the user swipes between them on phone. Tab buttons sit above the
// snap-container for explicit navigation (also serves as a focus target
// for keyboard users — swipe-only navigation isn't keyboard-reachable).
//
// State that crosses the two views:
//   - The wheel hook owned here (per Step 4b) feeds the page-header
//     SaveStatus. The timeline's bottom sheet uses its own hook instance
//     for the tapped date — independent transport, independent status.
//   - "active" tab is local state; URL routing intentionally omitted to
//     keep this an SPA-feeling single screen.

import { useState } from 'react';
import { DayEntryEditor } from '@/components/day-entry-editor';
import { SaveStatus } from '@/components/save-status';
import { TimelineView } from '@/components/timeline-view';
import { copy } from '@/copy';
import { useDayEntryUpsert } from '@/hooks/use-day-entry-upsert';
import type { DayEntry } from '@/lib/domain/day-entry';
import { formatDateDutch } from '@/lib/domain/date';
import type { Tag } from '@/lib/domain/tag';

type Props = {
  date: string;
  entry: DayEntry | null;
  allTags: Tag[];
  timelineEntries: DayEntry[];
};

type Tab = 'today' | 'timeline';

export function TodayShell({ date, entry, allTags, timelineEntries }: Props) {
  const heading = formatDateDutch(date);
  const [tab, setTab] = useState<Tab>('today');
  const { save, status, lastError } = useDayEntryUpsert(date);

  return (
    <main className="mx-auto flex min-h-screen max-w-120 flex-col gap-6 p-6">
      <header className="flex flex-row items-baseline justify-between gap-3">
        <h1 className="text-2xl font-semibold capitalize">{heading}</h1>
        <SaveStatus status={status} error={lastError} variant="glyph" />
      </header>

      <div
        role="tablist"
        aria-label="Schermen"
        className="flex w-full items-center gap-2 border-b border-border"
      >
        <button
          type="button"
          role="tab"
          aria-selected={tab === 'today'}
          onClick={() => setTab('today')}
          className={
            tab === 'today'
              ? '-mb-px border-b-2 border-accent px-3 py-2 text-base font-medium text-fg'
              : '-mb-px border-b-2 border-transparent px-3 py-2 text-base text-fg-muted hover:text-fg'
          }
        >
          {copy.timeline.todayTab}
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={tab === 'timeline'}
          onClick={() => setTab('timeline')}
          className={
            tab === 'timeline'
              ? '-mb-px border-b-2 border-accent px-3 py-2 text-base font-medium text-fg'
              : '-mb-px border-b-2 border-transparent px-3 py-2 text-base text-fg-muted hover:text-fg'
          }
        >
          {copy.timeline.title}
        </button>
      </div>

      {tab === 'today' ? (
        <DayEntryEditor
          date={date}
          initialEntry={entry}
          allTags={allTags}
          scoreSave={save}
          scoreStatus={status}
        />
      ) : (
        <TimelineView today={date} initialEntries={timelineEntries} allTags={allTags} />
      )}

      {status === 'error' && tab === 'today' && (
        <SaveStatus status={status} error={lastError} variant="banner" />
      )}
    </main>
  );
}
