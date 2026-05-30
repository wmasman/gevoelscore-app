'use client';

// QuickEntryFlow — the composite that orchestrates ScoreCircle, NoteField,
// and TagCategoryList inside a BottomSheet. The user navigates score →
// note → tags; the parent (TodayShell, in Step 4) decides when to open
// and listens for `onComplete`.
//
// Design decisions documented at the top so this file stays readable
// without paging back to the step plan:
//
// 1. All three step components stay mounted for the lifetime of the
//    sheet. Step changes are crossfaded via opacity, not unmount/mount.
//    Rationale: NoteField holds typed-but-not-yet-saved text in local
//    state until its 1.5s settle timer fires. Unmounting on step change
//    would lose that text. Tag selection has the same shape.
//
// 2. Score save is hoisted to this component (ScoreCircle is presentational
//    per Step 2). NoteField and TagCategoryList retain their own
//    `useDayEntryUpsert` calls — they were designed that way for the
//    daily-entry feature and we reuse them as-is.
//
// 3. No auto-advance. The score step shows a "Volgende: notitie"
//    forward button that becomes enabled after the first commit (i.e.
//    after `editable` flips). The previous 500 ms auto-advance broke
//    WCAG 2.2 SC 2.2.1 (Timing Adjustable) and contradicted the
//    brief's "no time pressure" rule — a brainfog user reading "7"
//    out loud saw the surface morph under them. Explicit advance only.
//
// 4. Editable gate: NoteField + TagCategoryList are disabled until the
//    first score save has been initiated. After commit they become
//    editable optimistically — if the save fails the user can re-attempt
//    via the standard save-status path.
//
// 5. End-of-flow signalling: "Klaar" on the tags step fires `onComplete()`.
//    The parent decides what happens (close the sheet, pulse the today
//    card). Drag-down dismiss and Escape close the sheet via the BottomSheet
//    primitive but do NOT count as completion — only "Klaar" does.

import { useEffect, useRef, useState } from 'react';
import { BottomSheet } from '@/components/lab/bottom-sheet';
import { ScoreCircle } from '@/components/lab/score-circle';
import { NoteField } from '@/components/note-field';
import { TagCategoryList } from '@/components/tag-category-list';
import { useDayEntryUpsert } from '@/hooks/use-day-entry-upsert';
import { cn } from '@/lib/ui/cn';
import { formatDateDutch } from '@/lib/domain/date';
import type { DayEntry } from '@/lib/domain/day-entry';
import type { Tag } from '@/lib/domain/tag';
import { copy } from '@/copy';

export type Step = 'score' | 'note' | 'tags';

type Props = {
  date: string;
  initialEntry: DayEntry | null;
  allTags: Tag[];
  open: boolean;
  startStep?: Step;
  isPastDay?: boolean;
  onClose: () => void;
  onComplete: () => void;
};

export function QuickEntryFlow({
  date,
  initialEntry,
  allTags,
  open,
  startStep = 'score',
  isPastDay = false,
  onClose,
  onComplete,
}: Props) {
  const [step, setStep] = useState<Step>(startStep);
  const [editable, setEditable] = useState<boolean>(initialEntry !== null);
  const { save: saveScore } = useDayEntryUpsert(date);

  // Sync internal step + editable to the latest props on the
  // closed→open edge. useState(startStep) only reads the prop on
  // first mount, so without this the same QuickEntryFlow instance
  // (which lives in the tree for the page's lifetime) would keep
  // showing whichever step it was last on — making every edit pencil
  // open the popout at the wrong step.
  const prevOpenRef = useRef(open);
  useEffect(() => {
    if (open && !prevOpenRef.current) {
      setStep(startStep);
      setEditable(initialEntry !== null);
    }
    prevOpenRef.current = open;
  }, [open, startStep, initialEntry]);

  function handleScoreCommit(value: number): void {
    // M-M3: no flush. The hook's 500 ms debounce coalesces a keyboard
    // arrow-burst (one PUT per arrow keystroke previously) into a
    // single PUT + router.refresh. Touch drag is already one pointer-
    // up event so debounce doesn't delay it meaningfully.
    void saveScore({ score: value as DayEntry['score'] });
    if (!editable) setEditable(true);
  }

  function goBack(): void {
    setStep((s) => (s === 'tags' ? 'note' : s === 'note' ? 'score' : s));
  }
  function goForward(): void {
    if (step === 'score') setStep('note');
    else if (step === 'note') setStep('tags');
    else if (step === 'tags') onComplete();
  }

  const tint = isPastDay ? 'past' : 'today';
  const backLabel =
    step === 'note'
      ? `← ${copy.daily.score.label}`
      : step === 'tags'
        ? `← ${copy.daily.note.label}`
        : null;
  const forwardLabel =
    step === 'score'
      ? 'Volgende: notitie'
      : step === 'note'
        ? 'Volgende: tags'
        : step === 'tags'
          ? 'Klaar'
          : null;
  // On the score step the forward button stays disabled until the
  // user has committed a value (editable flips at first commit) so
  // the default-shown 5 can't be advanced past without an explicit
  // user choice — matches the brief's anti-anchoring stance.
  const forwardDisabled = step === 'score' && !editable;

  const layerBase =
    'absolute inset-0 flex flex-col px-6 transition-opacity duration-150 ease-out';
  function layerClass(active: boolean): string {
    return cn(layerBase, active ? 'opacity-100' : 'pointer-events-none opacity-0');
  }

  return (
    <BottomSheet
      open={open}
      onClose={onClose}
      tint={tint}
      ariaLabel={copy.app.title}
    >
      <div className="flex items-baseline justify-between px-6 pb-1 pt-1">
        <span className="text-xs font-medium uppercase tracking-wider text-fg-muted">
          {formatDateDutch(date)}
        </span>
        <button
          type="button"
          onClick={onClose}
          aria-label="Sluiten"
          className="inline-flex min-h-11 min-w-11 items-center justify-center rounded-md text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
        >
          ✕
        </button>
      </div>

      {/* Content area: flex-1 so it claims available height inside the
          sheet's flex column, min-h-0 so it can shrink when the visual
          viewport is constrained (iPhone with keyboard up). Replaces
          the prior fixed h-95 (380px), which on iPhone PWA pushed the
          sheet past the visible viewport once the soft keyboard rose.

          data-autofocus on the layer matching `step` tells useFocusTrap
          to focus the first focusable inside that wrapper rather than
          the close ✕ button — see use-focus-trap.ts. */}
      <div className="relative min-h-0 flex-1">
        <div
          className={layerClass(step === 'score')}
          data-autofocus={step === 'score' ? 'true' : undefined}
        >
          <div className="flex h-full items-center justify-center">
            <ScoreCircle
              initialValue={initialEntry?.score ?? 5}
              onCommit={handleScoreCommit}
              ariaLabel={copy.daily.score.label}
            />
          </div>
        </div>
        <div
          className={layerClass(step === 'note')}
          data-autofocus={step === 'note' ? 'true' : undefined}
        >
          <div className="flex h-full flex-col pt-4">
            <NoteField
              date={date}
              initialNote={initialEntry?.note ?? null}
              disabled={!editable}
            />
          </div>
        </div>
        <div
          className={cn(layerClass(step === 'tags'), 'overflow-y-auto')}
          data-autofocus={step === 'tags' ? 'true' : undefined}
        >
          <TagCategoryList
            date={date}
            allTags={allTags}
            initialTagIds={initialEntry?.tag_ids ?? []}
            disabled={!editable}
          />
        </div>
      </div>

      <div className="flex items-center justify-between gap-3 px-6 pb-4 pt-2">
        {backLabel !== null ? (
          <button
            type="button"
            onClick={goBack}
            className="inline-flex min-h-11 items-center rounded-md px-4 py-2 text-base text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
          >
            {backLabel}
          </button>
        ) : (
          <span />
        )}
        {forwardLabel !== null ? (
          <button
            type="button"
            onClick={goForward}
            disabled={forwardDisabled}
            className="inline-flex min-h-11 items-center rounded-md bg-accent-hover px-4 py-2 text-base font-medium text-bg focus-visible:outline-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-50"
          >
            {forwardLabel}
          </button>
        ) : null}
      </div>
    </BottomSheet>
  );
}
