'use client';

// BottomSheet — presentational shell for the quick-entry-popout flow.
//
// Knows nothing about score / note / tags. Provides:
//   - slide-up/down transitions (CSS transform, no animation library)
//   - backdrop with click-to-close
//   - handle-only drag-to-dismiss (gesture isolation: dismiss-gesture lives
//     on the handle bar, score-drag-gesture lives on its own element later)
//   - focus trap (useFocusTrap) so keyboard users can't escape the modal
//   - body scroll lock (useBodyScrollLock) so the page behind doesn't move
//   - iOS keyboard anchor (useVisualViewport) so the sheet floats above
//     the soft keyboard during the note step
//   - surface-tint variant (today vs past)
//
// Renders into a portal at document.body to avoid z-index battles with
// any future stacking context inside the app shell.
//
// Inline styles are restricted to values driven by imperative state —
// drag offset during a pointer-down sequence, and the keyboard-aware
// bottom positioning. All other styling lives in Tailwind utility
// classes composed via cn().

import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { useBodyScrollLock } from '@/hooks/use-body-scroll-lock';
import { useFocusTrap } from '@/hooks/use-focus-trap';
import { useVisualViewport } from '@/hooks/use-visual-viewport';
import { cn } from '@/lib/ui/cn';

type Props = {
  open: boolean;
  onClose: () => void;
  tint?: 'today' | 'past';
  children: React.ReactNode;
  ariaLabel: string;
};

const DISMISS_THRESHOLD_PX = 100;
// 200 ms aligns with the brief's motion cap (docs/design/brief.md:91)
// and the brainfog-friendly "≤ 200ms" rule. The sheet's slide-up/down
// is one of the few transitions in the app — extra polish from running
// longer doesn't beat the discipline of one cap everywhere.
const TRANSITION_MS = 200;

export function BottomSheet({
  open,
  onClose,
  tint = 'today',
  children,
  ariaLabel,
}: Props) {
  const sheetRef = useRef<HTMLDivElement>(null);
  const handleRef = useRef<HTMLDivElement>(null);
  const [shouldRender, setShouldRender] = useState(open);
  const [dragOffset, setDragOffset] = useState(0);
  const [dragging, setDragging] = useState(false);
  const dragStartY = useRef(0);
  const viewport = useVisualViewport();

  useFocusTrap(sheetRef, open);
  useBodyScrollLock(open);

  // Mount/unmount lifecycle synced with the close transition so the
  // sheet animates out before disappearing from the DOM.
  useEffect(() => {
    if (open) {
      setShouldRender(true);
      return;
    }
    const t = setTimeout(() => setShouldRender(false), TRANSITION_MS);
    return () => clearTimeout(t);
  }, [open]);

  useEffect(() => {
    if (!open) return;
    function onKey(e: KeyboardEvent): void {
      if (e.key === 'Escape') onClose();
    }
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  function onHandlePointerDown(e: React.PointerEvent<HTMLDivElement>): void {
    setDragging(true);
    dragStartY.current = e.clientY;
    setDragOffset(0);
    handleRef.current?.setPointerCapture(e.pointerId);
  }
  function onHandlePointerMove(e: React.PointerEvent<HTMLDivElement>): void {
    if (!dragging) return;
    const dy = Math.max(0, e.clientY - dragStartY.current);
    setDragOffset(dy);
  }
  function onHandlePointerUp(e: React.PointerEvent<HTMLDivElement>): void {
    if (!dragging) return;
    handleRef.current?.releasePointerCapture(e.pointerId);
    const offset = dragOffset;
    setDragging(false);
    setDragOffset(0);
    if (offset > DISMISS_THRESHOLD_PX) onClose();
  }

  if (!shouldRender) return null;

  const keyboardOffset =
    typeof window !== 'undefined'
      ? Math.max(0, window.innerHeight - viewport.height)
      : 0;

  // Only imperative values live here — everything stylistic is Tailwind.
  // maxHeight caps the sheet at the visible viewport (above keyboard +
  // below status bar) so its top can't push off-screen when the soft
  // keyboard is up — the prior bug where the textarea floated above
  // the status bar on iPhone PWA. calc() leaves space for the iOS
  // Dynamic Island / notch.
  const sheetStyle: React.CSSProperties = {
    bottom: `${keyboardOffset}px`,
  };
  if (viewport.height > 0) {
    sheetStyle.maxHeight = `calc(${viewport.height}px - env(safe-area-inset-top, 0px))`;
  }
  if (dragging) {
    sheetStyle.transform = `translateY(${dragOffset}px)`;
    sheetStyle.transition = 'none';
  }

  return createPortal(
    <>
      <div
        className={cn(
          'fixed inset-0 z-40 bg-[rgba(43,37,32,0.4)]',
          'transition-opacity duration-200 ease-out',
          !open && 'pointer-events-none opacity-0',
        )}
        onClick={onClose}
        aria-hidden="true"
      />
      <div
        ref={sheetRef}
        role="dialog"
        aria-modal="true"
        aria-label={ariaLabel}
        // Programmatically focusable as the useFocusTrap fallback when
        // children render no focusable elements (Open Q4 from step-1).
        tabIndex={-1}
        className={cn(
          'fixed left-0 right-0 z-50 mx-auto flex max-w-120 flex-col',
          'rounded-t-[28px] shadow-[0_-8px_24px_rgba(43,37,32,0.08)]',
          'pb-[env(safe-area-inset-bottom,0)]',
          'transition-[transform,background-color,bottom] duration-200 ease-out',
          // overflow-x: hidden at the sheet itself, NOT just on body —
          // position:fixed children aren't clipped by html/body
          // overflow rules, so any inner element forcing horizontal
          // expansion (e.g. a flex row that doesn't shrink enough on a
          // narrow iPhone viewport) bleeds past the sheet box into the
          // viewport's right edge. Clipping here is the only correct
          // place. 2026-06-01 inline-tag-creation hotfix.
          'overflow-x-hidden',
          tint === 'past' ? 'bg-surface-muted' : 'bg-surface',
          !open && 'translate-y-full',
        )}
        style={sheetStyle}
      >
        <div
          ref={handleRef}
          data-testid="bottom-sheet-handle"
          aria-hidden="true"
          className={cn(
            'flex w-full cursor-grab touch-pan-y select-none justify-center pb-2 pt-3',
            'active:cursor-grabbing',
          )}
          onPointerDown={onHandlePointerDown}
          onPointerMove={onHandlePointerMove}
          onPointerUp={onHandlePointerUp}
          onPointerCancel={onHandlePointerUp}
        >
          <div className="pointer-events-none h-1 w-9 rounded-sm bg-fg-subtle" />
        </div>
        {children}
      </div>
    </>,
    document.body,
  );
}
