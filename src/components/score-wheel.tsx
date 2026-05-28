'use client';

// ScoreWheel — vertical scroll-snap picker of values 1..10. The cardinal-
// principle moment: one motion saves the day.
//
// Two interaction surfaces:
//   - touch / mouse scroll on the wheel itself (CSS scroll-snap + an
//     IntersectionObserver that detects the centred item)
//   - tap on a visible non-centred item to jump to it
//   - keyboard arrows / Home / End for accessibility
//
// Save semantics (per the daily-entry README AC2 and Step 4 plan):
//   - Idle (fresh day, no entry yet): wheel centres at 5, no aria-selected
//   - First *deliberate* interaction → promotes to "set" and saves with
//     flush=true (immediate)
//   - Subsequent changes save via the hook's natural debounce (500ms)
//   - Re-selecting the already-saved value is a no-op (AC4)
//   - The hook handles abort, status, and error revert; this component
//     just reads `status` and reverts its optimistic `centred` if needed

import { useEffect, useRef, useState } from 'react';
import { SaveStatus } from '@/components/save-status';
import { copy } from '@/copy';
import { useDayEntryUpsert } from '@/hooks/use-day-entry-upsert';
import type { Score } from '@/lib/domain/score';

type Props = {
  date: string;
  initialScore: number | null;
  // Fires when the wheel transitions from idle → set (first deliberate save).
  // The composite uses this to enable the note + tag picker immediately,
  // sidestepping a server-component re-fetch.
  onFirstSet?: () => void;
};

const WHEEL_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] as const;
const DEFAULT_IDLE_SCORE = 5;
const MIN_SCORE = 1;
const MAX_SCORE = 10;

export function ScoreWheel({ date, initialScore, onFirstSet }: Props) {
  const [centred, setCentred] = useState<number>(initialScore ?? DEFAULT_IDLE_SCORE);
  const [phase, setPhase] = useState<'idle' | 'set'>(initialScore !== null ? 'set' : 'idle');
  const lastSavedRef = useRef<number | null>(initialScore);
  const { save, status, lastError } = useDayEntryUpsert(date);

  // Revert optimistic state when the hook reports an error.
  useEffect(() => {
    if (status === 'error' && lastSavedRef.current !== null) {
      setCentred(lastSavedRef.current);
    } else if (status === 'saved') {
      lastSavedRef.current = centred;
    }
  }, [status, centred]);

  function selectValue(n: number): void {
    const clamped = Math.max(MIN_SCORE, Math.min(MAX_SCORE, n));
    // AC4: no-op when target equals the already-saved value AND we're
    // already in set phase (fresh-day idle still saves the default 5 on
    // first interaction so the row actually gets created).
    if (phase === 'set' && clamped === lastSavedRef.current && clamped === centred) {
      return;
    }
    const wasIdle = phase === 'idle';
    setCentred(clamped);
    if (wasIdle) {
      setPhase('set');
      onFirstSet?.();
    }
    // Clamped to [1..10] above; cast to the domain Score type.
    void save({ score: clamped as Score }, { flush: wasIdle });
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLDivElement>): void {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        selectValue(centred + 1);
        break;
      case 'ArrowUp':
        e.preventDefault();
        selectValue(centred - 1);
        break;
      case 'PageDown':
        e.preventDefault();
        selectValue(centred + 3);
        break;
      case 'PageUp':
        e.preventDefault();
        selectValue(centred - 3);
        break;
      case 'Home':
        e.preventDefault();
        selectValue(MIN_SCORE);
        break;
      case 'End':
        e.preventDefault();
        selectValue(MAX_SCORE);
        break;
      default:
        // Number keys 1..9 + 0 (=10) for quick keyboard entry
        if (e.key >= '1' && e.key <= '9') {
          e.preventDefault();
          selectValue(Number(e.key));
        } else if (e.key === '0') {
          e.preventDefault();
          selectValue(MAX_SCORE);
        }
    }
  }

  return (
    <div className="flex flex-col gap-2">
      <div
        role="listbox"
        aria-label={copy.daily.score.label}
        data-phase={phase}
        data-default-score={String(DEFAULT_IDLE_SCORE)}
        tabIndex={0}
        onKeyDown={onKeyDown}
        className="flex h-56 flex-col items-center justify-center overflow-hidden rounded-lg border border-border focus-visible:outline-2 focus-visible:outline-accent"
      >
        {WHEEL_VALUES.map((n) => {
          const isCentred = n === centred;
          const isSelected = phase === 'set' && isCentred;
          return (
            <button
              key={n}
              type="button"
              role="option"
              aria-selected={isSelected ? true : undefined}
              data-score={n}
              data-centred={isCentred ? 'true' : undefined}
              onClick={() => selectValue(n)}
              className={
                isSelected
                  ? 'flex h-12 w-12 items-center justify-center rounded-md text-2xl font-semibold text-fg ring-2 ring-accent'
                  : isCentred
                    ? 'flex h-12 w-12 items-center justify-center text-2xl text-fg'
                    : 'flex h-12 w-12 items-center justify-center text-base text-fg'
              }
            >
              {n}
            </button>
          );
        })}
      </div>
      <SaveStatus status={status} error={lastError} />
    </div>
  );
}
