'use client';

import { copy } from '@/copy';
import type { DayEntry } from '@/lib/domain/day-entry';
import { formatDateDutch } from '@/lib/domain/date';
import { TAG_CATEGORIES } from '@/lib/domain/tag-category';

// Today screen shell — rendered by src/app/page.tsx as a client component
// after the server fetches today's entry. Step 2 keeps the wheel + category
// stack INERT: the wheel has no scroll handler, headers don't expand. Step
// 4 (ScoreWheel) and Step 5 (TagPicker) will replace these placeholders
// with their interactive equivalents.
//
// Layout: max-width 480px, vertically centred. Single column on phone.

type Props = {
  date: string;
  entry: DayEntry | null;
};

const WHEEL_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] as const;
const DEFAULT_IDLE_SCORE = 5;

export function TodayShell({ date, entry }: Props) {
  const heading = formatDateDutch(date);
  const centred = entry?.score ?? DEFAULT_IDLE_SCORE;
  const isSet = entry !== null;

  return (
    <main className="mx-auto flex min-h-screen max-w-[480px] flex-col gap-6 p-6">
      <h1 className="text-2xl font-semibold capitalize">{heading}</h1>

      <section className="flex flex-col gap-2">
        <div
          role="listbox"
          aria-label={copy.daily.score.label}
          data-default-score={String(DEFAULT_IDLE_SCORE)}
          data-phase={isSet ? 'set' : 'idle'}
          className="flex h-56 flex-col items-center justify-center overflow-hidden rounded-lg border border-[var(--color-border)]"
        >
          {WHEEL_VALUES.map((n) => {
            const selected = isSet && n === centred;
            return (
              <div
                key={n}
                role="option"
                aria-selected={selected ? true : undefined}
                data-score={n}
                data-centred={n === centred ? 'true' : undefined}
                className={
                  selected
                    ? 'flex h-12 w-12 items-center justify-center rounded-md text-2xl font-semibold ring-2 ring-[var(--color-accent)]'
                    : n === centred
                    ? 'flex h-12 w-12 items-center justify-center text-2xl text-[var(--color-fg-muted)]'
                    : 'flex h-12 w-12 items-center justify-center text-base text-[var(--color-fg-muted)] opacity-40'
                }
              >
                {n}
              </div>
            );
          })}
        </div>
      </section>

      <section aria-labelledby="note-heading" className="flex flex-col gap-2">
        <h2 id="note-heading" className="text-sm font-medium text-[var(--color-fg-muted)]">
          {copy.daily.note.label}
        </h2>
        <p className="text-[var(--color-fg-muted)] italic">
          {isSet ? copy.daily.note.placeholder : '—'}
        </p>
      </section>

      <section aria-labelledby="tags-heading" className="flex flex-col gap-2">
        <h2 id="tags-heading" className="text-sm font-medium text-[var(--color-fg-muted)]">
          {copy.daily.tags.label}
        </h2>
        <ul className="flex flex-col gap-1">
          {TAG_CATEGORIES.map((category) => (
            <li key={category}>
              <button
                type="button"
                aria-expanded={false}
                disabled
                className="flex w-full items-center justify-between rounded-md border border-[var(--color-border)] px-3 py-3 text-left text-base capitalize disabled:opacity-60"
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
