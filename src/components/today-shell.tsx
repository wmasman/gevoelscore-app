'use client';

import { DayEntryEditor } from '@/components/day-entry-editor';
import { SaveStatus } from '@/components/save-status';
import { useDayEntryUpsert } from '@/hooks/use-day-entry-upsert';
import type { DayEntry } from '@/lib/domain/day-entry';
import { formatDateDutch } from '@/lib/domain/date';
import type { Tag } from '@/lib/domain/tag';

// Today screen — auth-gated server component (src/app/page.tsx) passes
// today's entry + allTags down. DayEntryEditor composes row + note + tag
// picker into a single vertical unit; same composite is reused by Step 6's
// timeline bottom sheet.
//
// Step 4b moved the *score* hook from inside <ScoreRow> up to here, so the
// page header can render <SaveStatus variant="glyph" /> alongside the H1
// date. NoteField + TagCategoryList still own their own hook instances
// (each has its own debounce timing); a future unification step may merge
// them.
//
// Layout: max-width 480px, vertically centred. Single column on phone.

type Props = {
  date: string;
  entry: DayEntry | null;
  allTags: Tag[];
};

export function TodayShell({ date, entry, allTags }: Props) {
  const heading = formatDateDutch(date);
  const { save, status, lastError } = useDayEntryUpsert(date);

  return (
    <main className="mx-auto flex min-h-screen max-w-120 flex-col gap-6 p-6">
      <header className="flex flex-row items-baseline justify-between gap-3">
        <h1 className="text-2xl font-semibold capitalize">{heading}</h1>
        <SaveStatus status={status} error={lastError} variant="glyph" />
      </header>
      <DayEntryEditor
        date={date}
        initialEntry={entry}
        allTags={allTags}
        scoreSave={save}
        scoreStatus={status}
      />
      {status === 'error' && (
        <SaveStatus status={status} error={lastError} variant="banner" />
      )}
    </main>
  );
}
