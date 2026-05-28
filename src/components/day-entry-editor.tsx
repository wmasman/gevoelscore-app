'use client';

// DayEntryEditor — the composite that bundles row + note + tag picker as
// one vertical unit. The Today screen uses it with today's date; Step 6's
// timeline bottom sheet reuses the same component with the tapped date.
//
// Enable / disable rule (per AC: "no score set yet → note + tags inactive"):
//   - initialEntry === null → editable=false on first paint
//   - row's first save (idle → set transition) → editable=true via the
//     onFirstSet callback. Avoids the round-trip to refetch initialEntry.
//
// Each leaf component owns its own useDayEntryUpsert(date) (each has its
// own debounce timing) but broadcasts status to the surrounding
// <SaveStatusProvider> via useReportSaveStatus — a single header glyph
// shows the merged save state. Closed Step 4b's split-indicator UX per
// the 2026-05-28 audit's L2.

import { useState } from 'react';
import { NoteField } from '@/components/note-field';
import { ScoreRow } from '@/components/score-row';
import { TagCategoryList } from '@/components/tag-category-list';
import type { DayEntry } from '@/lib/domain/day-entry';
import type { Tag } from '@/lib/domain/tag';

type Props = {
  date: string;
  initialEntry: DayEntry | null;
  allTags: Tag[];
};

export function DayEntryEditor({ date, initialEntry, allTags }: Props) {
  const [editable, setEditable] = useState<boolean>(initialEntry !== null);

  return (
    <div className="flex flex-col gap-6">
      <ScoreRow
        date={date}
        initialScore={initialEntry?.score ?? null}
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
