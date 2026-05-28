# Step 1: BottomSheet primitive

**Estimated time:** 3 hours
**Test layer:** Vitest component tests (jsdom) for the sheet's open/close states, drag-to-dismiss thresholds, focus management, and tint variants. Playwright e2e for the gesture-isolation behaviour and iOS-keyboard interaction (the latter validated post-deploy per the spec).
**Risk:** Medium. The handle-only-drag-to-dismiss pattern is validated in the HTML prototype but needs translation into a React component without losing the precision. The iOS-keyboard handling depends on the `useVisualViewport` hook from Step 0; verified-in-prod after deploy.
**Prerequisite:** [Step 0](step-0-shared-primitives.md) shipped (uses all four hooks).

> A presentational bottom-sheet shell. Knows nothing about score / note / tags. Provides: slide-up/down transitions, backdrop with click-to-close, handle-only drag-to-dismiss, focus trap, body scroll lock, iOS keyboard anchoring, and surface-tint variants. Reusable for any future input-surface modal.

---

## Acceptance criteria

- [ ] AC1: Component signature:
  ```ts
  type Props = {
    open: boolean;
    onClose: () => void;
    tint?: 'today' | 'past';                  // default: 'today'
    children: React.ReactNode;
    ariaLabel: string;                        // for the dialog role
  };
  ```
  Single import: `import { BottomSheet } from '@/components/lab/bottom-sheet'`.
- [ ] AC2: When `open` is true:
  - Sheet slides up from below (~250ms ease-out)
  - Backdrop fades in (~200ms ease-out) at 40% warm-dark wash (`rgba(43, 37, 32, 0.4)`)
  - Focus moves into the sheet via `useFocusTrap`
  - Body scroll is locked via `useBodyScrollLock`
- [ ] AC3: When `open` is false:
  - Sheet slides down (~250ms ease-out)
  - Backdrop fades out
  - Focus returns to the element that triggered the open
  - Body scroll restores
- [ ] AC4: Drag-handle (36×4px bar at top of sheet) is the **only** element that initiates drag-to-dismiss. The sheet body does not accept dismiss gestures. Drag the handle down > 100px = `onClose()` fires. Drag down < 100px = snap-back.
- [ ] AC5: Backdrop click fires `onClose()`. Escape key (when sheet is open) fires `onClose()`.
- [ ] AC6: `tint="today"` renders sheet with `--color-surface` background; `tint="past"` renders with `--color-surface-muted`. Transition between tints is ~200ms when the prop changes.
- [ ] AC7: Sheet has `role="dialog"`, `aria-modal="true"`, `aria-label={ariaLabel}`. Renders inside a Portal to `document.body` to avoid z-index battles.
- [ ] AC8: When the iOS keyboard rises (visualViewport height shrinks), the sheet anchors to the visible viewport bottom via `useVisualViewport` — `style.bottom = window.innerHeight - visualViewport.height`. Updates smoothly.
- [ ] AC9: Maximum width 480px, centred on larger screens. Top corners rounded 28px. Shadow: `0 -8px 24px rgba(43, 37, 32, 0.08)`.
- [ ] AC10: Respects `prefers-reduced-motion: reduce` — transitions flatten to 0.01ms (already global default in `globals.css`).
- [ ] AC11: Renders nothing in DOM when `open === false` after the close transition completes (clean unmount via the same render-after-transition pattern `useStepMorph` uses). Avoids invisible-but-mounted overhead.

---

## Technical constraints

- **No new dependency.** All four hooks from Step 0 + native pointer events + CSS transitions.
- **All files quarantined under `src/components/lab/`** to mark this as exploration code, not production. The other programmer can see at a glance this is the new direction.
- **Styling via Tailwind utility classes**, per [`frontend-conventions.md`](../../architecture/frontend-conventions.md#styling-utility-first-tailwind--design-tokens). No CSS modules, no styled-components. Dynamic class composition via `cn()` from [`src/lib/ui/cn.ts`](../../../src/lib/ui/cn.ts). Tokens already exposed in `globals.css` (`bg-surface`, `bg-surface-muted`, `bg-fg-subtle`, etc.).
- **No new keyframes required.** Slide animation is `transform: translate-y-full ↔ translate-y-0` with a Tailwind `transition-transform` utility. Backdrop fade is `opacity-0 ↔ opacity-100` with `transition-opacity`. Both are GPU-accelerated.
- **Portal target:** `document.body`. Server-render safe (Portal renders nothing during SSR; client takes over).
- **Z-index:** sheet at `z-50`, backdrop at `z-40`. Sits above all `daily-entry/` content but below any future global toast layer.
- **Pointer events not touch events.** Matches the validated prototype. Avoids the per-platform touch-event quirks.
- **LOC budget:** ~150 lines of TypeScript. No separate stylesheet.

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | No | UI primitive |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | No data |
| New dependency | ADR or step rationale | No | Hand-rolled |
| `dangerouslySetInnerHTML` usage | A03 | No | — |
| New env var with a secret | A02, A05 | No | — |
| New telemetry / observability dep | Cardinal "no telemetry" | No | — |

## Plan

### 1.1 `src/components/lab/bottom-sheet.tsx`

Skeleton (Tailwind utility classes via `cn()`; no separate stylesheet):

```tsx
'use client';
import { createPortal } from 'react-dom';
import { useEffect, useRef, useState } from 'react';
import { useFocusTrap } from '@/hooks/use-focus-trap';
import { useBodyScrollLock } from '@/hooks/use-body-scroll-lock';
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
const TRANSITION_MS = 250;

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
  const dragStartY = useRef(0);
  const dragging = useRef(false);
  const viewport = useVisualViewport();

  useFocusTrap(sheetRef, open);
  useBodyScrollLock(open);

  // Mount/unmount lifecycle synced with the close transition
  useEffect(() => {
    if (open) setShouldRender(true);
    else {
      const t = setTimeout(() => setShouldRender(false), TRANSITION_MS);
      return () => clearTimeout(t);
    }
  }, [open]);

  // Escape key
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  // Handle drag-to-dismiss
  function onHandlePointerDown(e: React.PointerEvent) {
    dragging.current = true;
    dragStartY.current = e.clientY;
    setDragOffset(0);
    handleRef.current?.setPointerCapture(e.pointerId);
  }
  function onHandlePointerMove(e: React.PointerEvent) {
    if (!dragging.current) return;
    const dy = Math.max(0, e.clientY - dragStartY.current);
    setDragOffset(dy);
  }
  function onHandlePointerUp(e: React.PointerEvent) {
    if (!dragging.current) return;
    dragging.current = false;
    handleRef.current?.releasePointerCapture(e.pointerId);
    if (dragOffset > DISMISS_THRESHOLD_PX) onClose();
    setDragOffset(0);
  }

  if (!shouldRender) return null;

  const keyboardOffset =
    typeof window !== 'undefined'
      ? Math.max(0, window.innerHeight - viewport.height)
      : 0;

  // Inline style is only used for values the browser must drive imperatively
  // (drag offset, keyboard-aware bottom). Everything else is Tailwind.
  const sheetStyle: React.CSSProperties = {
    transform: dragging.current ? `translateY(${dragOffset}px)` : undefined,
    transition: dragging.current ? 'none' : undefined,
    bottom: `${keyboardOffset}px`,
  };

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
        className={cn(
          'fixed bottom-0 left-0 right-0 z-50 mx-auto max-w-[480px]',
          'rounded-t-[28px] shadow-[0_-8px_24px_rgba(43,37,32,0.08)]',
          'pb-[env(safe-area-inset-bottom,0)]',
          'transition-[transform,background-color,bottom] duration-[250ms] ease-out',
          tint === 'past' ? 'bg-surface-muted' : 'bg-surface',
          !open && 'translate-y-full',
        )}
        style={sheetStyle}
        role="dialog"
        aria-modal="true"
        aria-label={ariaLabel}
      >
        <div
          ref={handleRef}
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
```

### 1.2 No separate stylesheet

All styling is Tailwind utility classes (composed via `cn()` where conditional). The two inline-style values (`transform` during drag, `bottom` for keyboard-aware positioning) are necessary because they're driven by imperative state — not stylistic choices. They are tracked carefully because [`frontend-conventions.md`](../../architecture/frontend-conventions.md#styling-utility-first-tailwind--design-tokens) discourages inline style; the rationale is documented in the component's top comment.

The `bg-surface`, `bg-surface-muted`, and `bg-fg-subtle` utilities resolve to the tokens already exposed via `@theme` in [`src/app/globals.css`](../../../src/app/globals.css). No additions to `globals.css` needed.

### 1.3 Public API

Single named export: `BottomSheet`. No barrel — direct import.

### 1.4 Usage example (for documentation only — not shipped this step)

```tsx
const [open, setOpen] = useState(false);
<BottomSheet open={open} onClose={() => setOpen(false)} ariaLabel="Invoer">
  <div className="px-6 pb-8">
    {/* score / note / tags content arrives in Step 3 */}
  </div>
</BottomSheet>
```

## Test plan

### `src/components/lab/__tests__/bottom-sheet.test.tsx` (~10 cases)

| # | Case |
|---|---|
| 1 | `open={false}` initially: renders nothing (after the close-transition delay) |
| 2 | `open={true}`: renders backdrop + sheet, sheet has `role="dialog"` + `aria-modal="true"` |
| 3 | Backdrop click: calls `onClose` |
| 4 | Escape key while open: calls `onClose` |
| 5 | Handle drag > 100px down: calls `onClose`; handle drag < 100px: no `onClose`, transform resets |
| 6 | Sheet body click (NOT handle): does NOT call `onClose` — gesture isolation preserved |
| 7 | `tint="past"`: sheet renders with `surface-muted` background class |
| 8 | Open → close: focus returns to the previously-focused element (via useFocusTrap) |
| 9 | Open → close: body scroll restores (via useBodyScrollLock) |
| 10 | Visual viewport resize (mocked): sheet `bottom` style updates to compensate |

### `tests/e2e/quick-entry-popout-sheet.spec.ts` (~3 cases)

Focused on the gesture isolation that unit tests can't simulate properly.

| # | Case |
|---|---|
| 1 | Open the sheet via a trigger button. Touch-drag horizontally inside the sheet body (not on the handle). The sheet does NOT dismiss. |
| 2 | Touch-drag the handle bar down past 100px. The sheet dismisses. |
| 3 | axe-core scan on the open sheet: zero WCAG 2.2 AA violations. |

## Done criteria

- [ ] `BottomSheet` component shipped at `src/components/lab/bottom-sheet.tsx` (single file, no separate stylesheet — Tailwind utilities via `cn()`)
- [ ] 10 unit tests green
- [ ] 3 e2e tests green
- [ ] Vitest count delta: +10
- [ ] Playwright count delta: +3
- [ ] `npm run verify` clean
- [ ] **Mobile validation deferred to post-deploy** per the spec doc's strategy. Specifically: that the visualViewport keyboard offset works in iOS PWA standalone mode and that pointer-capture on the handle persists when the user's finger crosses outside the handle during a fast drag.

## Open questions to settle during implementation

- **Where exactly to lock `body` overflow on iOS:** the `useBodyScrollLock` hook from Step 0 handles this, but if iOS Safari in PWA mode shows rubber-band behaviour at the top of the document during the sheet's lifetime, we may need to additionally set `overscroll-behavior: none` on `html`. Test on real device.
- **Portal target on initial render:** `document.body` is the target; SSR-safe because `createPortal` is only called after `shouldRender` becomes true (which happens in a client effect). Verify no hydration warnings in Next.js dev console.
- **Sheet width at edge cases:** on viewports between 480px and 540px wide, the centred 480px sheet leaves narrow side margins. Acceptable per the design system's 560px max content container, but worth confirming visually on real devices.
- **`useFocusTrap` and the sheet's children:** if the children render no focusable elements (e.g. a sheet with only display content), focus should fall on the handle (which is keyboard-focusable via `tabindex="0"` — currently not set in the skeleton above; add). Note in implementation.
