'use client';

// ScoreRow — horizontal scroll-snap picker of values 1..10. The cardinal-
// principle moment: one motion saves the day. Reshaped from the vertical
// scroll-snap wheel (Step 4) in Step 4b to match the locked design at
// docs/design/brief.md.
//
// Three interaction surfaces:
//   - touch / pointer scroll on the row (CSS scroll-snap-x mandatory)
//   - tap on a visible non-centred item to jump to it
//   - keyboard arrows (Left/Right primary, Up/Down kept as aliases for
//     muscle-memory + hardware-keyboard cases) + Home / End / PageUp /
//     PageDown / number keys 1-9 / 0=10
//
// Save semantics (preserved verbatim from Step 4):
//   - Idle (fresh day, no entry yet): centre at 5, no aria-selected
//   - First *deliberate* interaction → promotes to "set" and saves with
//     flush=true (immediate)
//   - Subsequent changes save via the hook's natural debounce (500ms)
//   - Re-selecting the already-saved value is a no-op
//   - The error revert effect still lives here; the hook itself is now
//     owned by <TodayShell> per Step 4b.4 (save + status passed in as
//     props, <SaveStatus /> renders in the page header).
//
// Tailwind v4 scroll-snap: this project's tailwind.config.* doesn't ship
// the snap utilities by default, so the row uses inline style for
// `scroll-snap-type` and each button uses inline style for
// `scroll-snap-align`. Centralising in CSS variables felt premature for
// two values.

import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { copy } from '@/copy';
import { useReportSaveStatus } from '@/components/save-status-context';
import { useDayEntryUpsert } from '@/hooks/use-day-entry-upsert';
import type { Score } from '@/lib/domain/score';

type Props = {
  date: string;
  initialScore: number | null;
  // Fires when the row transitions from idle → set (first deliberate save).
  // The composite uses this to enable the note + tag picker immediately,
  // sidestepping a server-component re-fetch.
  onFirstSet?: () => void;
};

const ROW_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] as const;
const DEFAULT_IDLE_SCORE = 5;
const MIN_SCORE = 1;
const MAX_SCORE = 10;
// Tap-target floor (brainfog extension above WCAG 2.2 AA). Used here for
// math on scroll positioning; the visual width matches.
const BUTTON_PX = 48;

export function ScoreRow({ date, initialScore, onFirstSet }: Props) {
  const [centred, setCentred] = useState<number>(initialScore ?? DEFAULT_IDLE_SCORE);
  const [phase, setPhase] = useState<'idle' | 'set'>(initialScore !== null ? 'set' : 'idle');
  const lastSavedRef = useRef<number | null>(initialScore);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const { save, status, lastError } = useDayEntryUpsert(date);

  // Broadcast our save status to the SaveStatusProvider so the page
  // header can render a single merged indicator. No-op outside a provider
  // (useReportSaveStatus tolerates the absent context for isolated tests).
  useReportSaveStatus('score', status, lastError);

  // Revert optimistic state when the hook reports an error.
  useEffect(() => {
    if (status === 'error' && lastSavedRef.current !== null) {
      setCentred(lastSavedRef.current);
    } else if (status === 'saved') {
      lastSavedRef.current = centred;
    }
  }, [status, centred]);

  // Pre-scroll so the initial centred value sits in the middle. Layout
  // effect so the user never sees the row at scrollLeft:0.
  useLayoutEffect(() => {
    const el = containerRef.current;
    if (el === null) return;
    const initialIndex = (initialScore ?? DEFAULT_IDLE_SCORE) - 1;
    const target = initialIndex * BUTTON_PX - el.clientWidth / 2 + BUTTON_PX / 2;
    el.scrollLeft = Math.max(0, target);
    // Intentional: initialScore only matters on mount.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function scrollIntoView(n: number): void {
    const el = containerRef.current;
    if (el === null) return;
    const idx = n - 1;
    const target = idx * BUTTON_PX - el.clientWidth / 2 + BUTTON_PX / 2;
    const prefersReducedMotion =
      typeof window !== 'undefined' &&
      typeof window.matchMedia === 'function' &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    el.scrollTo({
      left: Math.max(0, target),
      behavior: prefersReducedMotion ? 'auto' : 'smooth',
    });
  }

  function selectValue(n: number): void {
    const clamped = Math.max(MIN_SCORE, Math.min(MAX_SCORE, n));
    // No-op when target equals the already-saved value AND we're already
    // in set phase (fresh-day idle still saves the default 5 on first
    // interaction so the row actually gets created).
    if (phase === 'set' && clamped === lastSavedRef.current && clamped === centred) {
      return;
    }
    const wasIdle = phase === 'idle';
    setCentred(clamped);
    scrollIntoView(clamped);
    if (wasIdle) {
      setPhase('set');
      onFirstSet?.();
    }
    void save({ score: clamped as Score }, { flush: wasIdle });
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLDivElement>): void {
    switch (e.key) {
      // Primary axis — left/right matches the visual layout.
      case 'ArrowRight':
        e.preventDefault();
        selectValue(centred + 1);
        break;
      case 'ArrowLeft':
        e.preventDefault();
        selectValue(centred - 1);
        break;
      // Aliases — kept so Step 4's muscle memory and hardware-keyboard
      // cases still work. ArrowDown = forward (toward 10), ArrowUp = back.
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
        // Number keys 1..9 + 0 (=10) for quick keyboard entry.
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
    <div
      ref={containerRef}
      role="listbox"
      aria-label={copy.daily.score.label}
      data-phase={phase}
      data-default-score={String(DEFAULT_IDLE_SCORE)}
      tabIndex={0}
      onKeyDown={onKeyDown}
      style={{ scrollSnapType: 'x mandatory' }}
      className="flex h-20 flex-row items-center gap-0 overflow-x-auto overflow-y-hidden rounded-lg border border-border px-[calc(50%-24px)] focus-visible:outline-2 focus-visible:outline-accent"
    >
      {ROW_VALUES.map((n) => {
        const isCentred = n === centred;
        const isSelected = phase === 'set' && isCentred;
        // Items remain fully legible (WCAG 2.2 AA contrast against the
        // warm-earth tokens). The brief's "declining opacity" direction
        // is realised through font weight + ring on the centred item,
        // not via translucent off-centre numbers (see frontend-conventions
        // for the accessibility-vs-decoration precedence rule).
        return (
          <button
            key={n}
            type="button"
            role="option"
            aria-selected={isSelected ? true : undefined}
            data-score={n}
            data-centred={isCentred ? 'true' : undefined}
            onClick={() => selectValue(n)}
            style={{ scrollSnapAlign: 'center' }}
            className={
              isSelected
                ? 'flex h-12 w-12 shrink-0 items-center justify-center rounded-md text-2xl font-semibold text-fg ring-2 ring-accent'
                : isCentred
                  ? 'flex h-12 w-12 shrink-0 items-center justify-center text-2xl font-medium text-fg'
                  : 'flex h-12 w-12 shrink-0 items-center justify-center text-2xl text-fg-muted'
            }
          >
            {n}
          </button>
        );
      })}
    </div>
  );
}
