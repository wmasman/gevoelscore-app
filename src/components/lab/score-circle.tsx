'use client';

// ScoreCircle — circular touch surface for picking a 1..10 score.
//
// Direct React port of docs/design/explorations/score-circle-prototype.html.
// The prototype's mechanic is what we validated on iPhone PWA; the React
// version preserves the same constants (20px per integer, 80ms pulse) so
// the feel carries over.
//
// Drag mechanic:
//   - pointerdown captures the pointer + saves the value+x at drag start
//   - pointermove computes deltaX, snaps to integer via Math.round(dx/20)
//     and updates the displayed value. No onCommit fires mid-drag.
//   - pointerup releases capture and fires onCommit with the snapped value.
//   - Each integer-crossing triggers an 80ms scale-pulse (visual replacement
//     for the absent haptic tick on iOS Safari).
//
// Keyboard: ArrowLeft/Right (and ArrowUp/Down aliases) +/- 1, Home = 1,
// End = 10. Each keypress is its own commit — the parent's debounce
// handles coalescing.
//
// `initialValue` is read once into local state on mount. If the parent
// remounts the component with a new initialValue the displayed value
// resets; if it just rerenders with a different prop, the displayed
// value stays put. This matches the prototype's "one source of truth
// for the drag value: the component itself" semantics.

import { useCallback, useEffect, useRef, useState } from 'react';
import { cn } from '@/lib/ui/cn';

const PIXELS_PER_INTEGER = 20;
const PULSE_MS = 80;
const MIN_VALUE = 1;
const MAX_VALUE = 10;

type Props = {
  initialValue?: number;
  onCommit: (value: number) => void;
  ariaLabel: string;
};

function clamp(n: number): number {
  return Math.max(MIN_VALUE, Math.min(MAX_VALUE, n));
}

export function ScoreCircle({ initialValue = 5, onCommit, ariaLabel }: Props) {
  const [value, setValue] = useState<number>(() => clamp(initialValue));
  const [pulsing, setPulsing] = useState(false);
  const circleRef = useRef<HTMLDivElement>(null);
  const dragRef = useRef<{ startValue: number; startX: number } | null>(null);
  const pulseTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const mountedRef = useRef(true);

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
      if (pulseTimerRef.current !== null) clearTimeout(pulseTimerRef.current);
    };
  }, []);

  const triggerPulse = useCallback((): void => {
    if (!mountedRef.current) return;
    setPulsing(true);
    if (pulseTimerRef.current !== null) clearTimeout(pulseTimerRef.current);
    pulseTimerRef.current = setTimeout(() => {
      if (!mountedRef.current) return;
      setPulsing(false);
    }, PULSE_MS);
  }, []);

  const applyValue = useCallback(
    (next: number): number => {
      const c = clamp(next);
      setValue((prev) => {
        if (prev !== c) triggerPulse();
        return c;
      });
      return c;
    },
    [triggerPulse],
  );

  function onPointerDown(e: React.PointerEvent<HTMLDivElement>): void {
    dragRef.current = { startValue: value, startX: e.clientX };
    circleRef.current?.setPointerCapture(e.pointerId);
    e.preventDefault();
  }
  function onPointerMove(e: React.PointerEvent<HTMLDivElement>): void {
    const drag = dragRef.current;
    if (!drag) return;
    const dx = e.clientX - drag.startX;
    applyValue(drag.startValue + Math.round(dx / PIXELS_PER_INTEGER));
  }
  function onPointerUp(e: React.PointerEvent<HTMLDivElement>): void {
    const drag = dragRef.current;
    if (!drag) return;
    dragRef.current = null;
    if (circleRef.current?.hasPointerCapture(e.pointerId)) {
      circleRef.current.releasePointerCapture(e.pointerId);
    }
    // Commit the value computed at the last move (or startValue if no move).
    const dx = e.clientX - drag.startX;
    const finalValue = clamp(drag.startValue + Math.round(dx / PIXELS_PER_INTEGER));
    onCommit(finalValue);
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLDivElement>): void {
    let next: number | null = null;
    switch (e.key) {
      case 'ArrowRight':
      case 'ArrowUp':
        next = value + 1;
        break;
      case 'ArrowLeft':
      case 'ArrowDown':
        next = value - 1;
        break;
      case 'Home':
        next = MIN_VALUE;
        break;
      case 'End':
        next = MAX_VALUE;
        break;
      default:
        return;
    }
    e.preventDefault();
    const committed = applyValue(next);
    onCommit(committed);
  }

  return (
    <div
      ref={circleRef}
      role="slider"
      aria-label={ariaLabel}
      aria-valuemin={MIN_VALUE}
      aria-valuemax={MAX_VALUE}
      aria-valuenow={value}
      tabIndex={0}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerCancel={onPointerUp}
      onKeyDown={onKeyDown}
      className={cn(
        'flex h-70 w-70 max-h-[80vw] max-w-[80vw] items-center justify-center',
        'rounded-full border border-border bg-surface',
        'shadow-[0_2px_6px_rgba(43,37,32,0.06)]',
        'cursor-grab touch-none select-none',
        'focus-visible:outline-2 focus-visible:outline-accent',
        'active:cursor-grabbing',
      )}
    >
      <span
        data-testid="score-number"
        data-pulsing={pulsing ? 'true' : 'false'}
        className={cn(
          'pointer-events-none text-[96px] font-semibold leading-none tabular-nums text-accent',
          'transition-transform duration-80 ease-out',
          pulsing && 'scale-105',
        )}
      >
        {value}
      </span>
    </div>
  );
}
