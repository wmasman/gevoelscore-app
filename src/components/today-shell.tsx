'use client';

import { copy } from '@/copy';
import { ScoreWheel } from '@/components/score-wheel';
import type { DayEntry } from '@/lib/domain/day-entry';
import { formatDateDutch } from '@/lib/domain/date';
import { TAG_CATEGORIES } from '@/lib/domain/tag-category';

// Today screen — auth-gated server component (src/app/page.tsx) passes
// today's entry down. Step 4 wires the score wheel; Step 5 will replace
// the inert collapsed category headers with the real tag picker.
//
// Layout: max-width 480px, vertically centred. Single column on phone.

type Props = {
  date: string;
  entry: DayEntry | null;
};

export function TodayShell({ date, entry }: Props) {
  const heading = formatDateDutch(date);
  const noteSet = entry !== null;

  return (
    <main className="mx-auto flex min-h-screen max-w-[480px] flex-col gap-6 p-6">
      <h1 className="text-2xl font-semibold capitalize">{heading}</h1>

      <ScoreWheel date={date} initialScore={entry?.score ?? null} />

      <section aria-labelledby="note-heading" className="flex flex-col gap-2">
        <h2 id="note-heading" className="text-sm font-medium text-fg-muted">
          {copy.daily.note.label}
        </h2>
        <p className="text-fg-muted italic">
          {noteSet ? copy.daily.note.placeholder : '—'}
        </p>
      </section>

      <section aria-labelledby="tags-heading" className="flex flex-col gap-2">
        <h2 id="tags-heading" className="text-sm font-medium text-fg-muted">
          {copy.daily.tags.label}
        </h2>
        <ul className="flex flex-col gap-1">
          {TAG_CATEGORIES.map((category) => (
            <li key={category}>
              <button
                type="button"
                aria-expanded={false}
                disabled
                className="flex w-full items-center justify-between rounded-md border border-border px-3 py-3 text-left text-base capitalize disabled:opacity-60"
              >
                <span>{category}</span>
                <span aria-hidden="true">+</span>
              </button>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
