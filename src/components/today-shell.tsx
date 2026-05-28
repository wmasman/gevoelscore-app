'use client';

// Today + Tijdlijn — two sibling views inside one screen. Step 6 added the
// timeline; the two views live behind a tablist. Saves from any of the
// three child components (score row, note field, tag category list)
// broadcast their status into <SaveStatusProvider>; the page header
// renders one merged glyph (no per-child indicators — see L2 of the
// 2026-05-28 audit).

import { useState } from 'react';
import { DayEntryEditor } from '@/components/day-entry-editor';
import { SaveStatus } from '@/components/save-status';
import {
  SaveStatusProvider,
  useMergedSaveStatus,
} from '@/components/save-status-context';
import { TimelineView } from '@/components/timeline-view';
import { copy } from '@/copy';
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
  return (
    <SaveStatusProvider>
      <TodayShellInner
        date={date}
        entry={entry}
        allTags={allTags}
        timelineEntries={timelineEntries}
      />
    </SaveStatusProvider>
  );
}

function TodayShellInner({ date, entry, allTags, timelineEntries }: Props) {
  const heading = formatDateDutch(date);
  const [tab, setTab] = useState<Tab>('today');
  const merged = useMergedSaveStatus();

  return (
    <main className="mx-auto flex min-h-screen max-w-120 flex-col gap-6 p-6">
      <header className="flex flex-row items-baseline justify-between gap-3">
        <h1 className="text-2xl font-semibold capitalize">{heading}</h1>
        <SaveStatus status={merged.status} error={merged.error} variant="glyph" />
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
        <DayEntryEditor date={date} initialEntry={entry} allTags={allTags} />
      ) : (
        <TimelineView today={date} initialEntries={timelineEntries} allTags={allTags} />
      )}

      {merged.status === 'error' && tab === 'today' && (
        <SaveStatus status="error" error={merged.error} variant="banner" />
      )}
    </main>
  );
}
