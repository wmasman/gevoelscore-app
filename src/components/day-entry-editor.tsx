'use client';

// DayEntryEditor — the composite that bundles row + note + tag picker as
// one vertical unit. The Today screen uses it with today's date; Step 6's
// timeline bottom sheet will reuse the same component with the tapped date.
//
// Enable / disable rule (per AC: "no score set yet → note + tags inactive"):
//   - initialEntry === null → editable=false on first paint
//   - row's first save (idle → set transition) → editable=true via the
//     onFirstSet callback. Avoids the round-trip to refetch initialEntry.
//
// Hook ownership: Step 4b hoisted the *score* hook up to <TodayShell> so
// the page header can render <SaveStatus />. NoteField and TagCategoryList
// keep their own per-component hook instances (each has its own debounce
// timing); a future unification step may merge them into a single hook +
// shared status context.

import { useState } from 'react';
import { NoteField } from '@/components/note-field';
import { ScoreRow } from '@/components/score-row';
import { TagCategoryList } from '@/components/tag-category-list';
import type { SaveStatus } from '@/hooks/use-day-entry-upsert';
import type { DayEntryPatch } from '@/lib/api/day-entries';
import type { DayEntry } from '@/lib/domain/day-entry';
import type { Tag } from '@/lib/domain/tag';

// Save signature mirrors useDayEntryUpsert.save — kept local to avoid a
// value-import of the hook in a server-safe re-export path.
type SaveFn = (
  patch: Partial<DayEntryPatch>,
  opts?: { flush?: boolean },
) => Promise<void>;

type Props = {
  date: string;
  initialEntry: DayEntry | null;
  allTags: Tag[];
  // Score-row hook lives at TodayShell; the editor just forwards it down.
  scoreSave: SaveFn;
  scoreStatus: SaveStatus;
};

export function DayEntryEditor({
  date,
  initialEntry,
  allTags,
  scoreSave,
  scoreStatus,
}: Props) {
  const [editable, setEditable] = useState<boolean>(initialEntry !== null);

  return (
    <div className="flex flex-col gap-6">
      <ScoreRow
        initialScore={initialEntry?.score ?? null}
        save={scoreSave}
        status={scoreStatus}
        onFirstSet={() => setEditable(true)}
      />
      <NoteField
        date={date}
        initialNote={initialEntry?.note ?? null}
        disabled={!editable}
      />
      <TagCategoryList
        date={date}
        allTags={allTags}
        initialTagIds={initialEntry?.tag_ids ?? []}
        disabled={!editable}
      />
    </div>
  );
}
