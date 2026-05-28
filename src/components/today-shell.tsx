import { DayEntryEditor } from '@/components/day-entry-editor';
import type { DayEntry } from '@/lib/domain/day-entry';
import { formatDateDutch } from '@/lib/domain/date';
import type { Tag } from '@/lib/domain/tag';

// Today screen — auth-gated server component (src/app/page.tsx) passes
// today's entry + allTags down. DayEntryEditor composes wheel + note + tag
// picker into a single vertical unit; same composite is reused by Step 6's
// timeline bottom sheet.
//
// Layout: max-width 480px, vertically centred. Single column on phone.

type Props = {
  date: string;
  entry: DayEntry | null;
  allTags: Tag[];
};

export function TodayShell({ date, entry, allTags }: Props) {
  const heading = formatDateDutch(date);

  return (
    <main className="mx-auto flex min-h-screen max-w-120 flex-col gap-6 p-6">
      <h1 className="text-2xl font-semibold capitalize">{heading}</h1>
      <DayEntryEditor date={date} initialEntry={entry} allTags={allTags} />
    </main>
  );
}
