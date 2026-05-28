# Step 0: Shared primitives foundation

**Estimated time:** 2.5 hours
**Test layer:** Vitest unit tests (jsdom) — pure hooks, no UI integration in this step.
**Risk:** Low. Each hook is a well-trodden pattern with a small surface. The `useVisualViewport` hook has one platform-specific concern (iOS PWA behaviour) flagged below.
**Prerequisite:** None for this step — it's the new foundation. Sits alongside the existing `useDayEntryUpsert` and `useDayEntryRead` hooks under `src/hooks/`.

> Lands four hooks that the rest of this feature builds on. They are intentionally small, framework-agnostic, and reusable across the app (settings modals, future bottom-sheets, anywhere we open a focus-trapped surface).

---

## Acceptance criteria

### `useFocusTrap`

- [ ] AC1: Hook signature `useFocusTrap(containerRef: RefObject<HTMLElement>, active: boolean): void`. When `active` flips to `true`, focus moves to the first focusable element inside `containerRef`. When `active` flips to `false`, focus returns to the element that had focus when `active` became `true`.
- [ ] AC2: While `active === true`, Tab and Shift+Tab cycle focus only within the container. Focus cannot escape via keyboard.
- [ ] AC3: If the container has no focusable elements when `active` becomes `true`, focus moves to the container itself (which must be programmatically focusable via `tabindex="-1"` on the consumer side).
- [ ] AC4: Hook handles unmount cleanly — if the consumer unmounts while `active === true`, the previously-focused element is restored.
- [ ] AC5: No external dependency — the hook is implemented in pure DOM + React.

### `useBodyScrollLock`

- [ ] AC6: Hook signature `useBodyScrollLock(active: boolean): void`. When `active === true`, `document.body` becomes scroll-locked (no scrolling of background content). When `active === false`, body scroll is restored.
- [ ] AC7: Multiple components can call this hook concurrently. The lock is reference-counted: scroll is restored only when the last active caller deactivates.
- [ ] AC8: iOS-specific concern: setting `overflow: hidden` on body alone does not prevent iOS Safari from scrolling. The hook applies the `position: fixed; top: -<scrollY>px` pattern to prevent the page from jumping when unlocked.
- [ ] AC9: Cleanup on unmount restores scroll position correctly.

### `useVisualViewport`

- [ ] AC10: Hook signature `useVisualViewport(): { offsetTop: number; offsetLeft: number; width: number; height: number }`. Returns the current `window.visualViewport` dimensions; updates on `resize` and `scroll` events.
- [ ] AC11: When the iOS soft keyboard appears, `visualViewport.height` shrinks; consumers can compute the keyboard height as `window.innerHeight - visualViewport.height`.
- [ ] AC12: Hook handles browsers without `visualViewport` API by falling back to `window.innerWidth/Height` and returning `offsetTop: 0`. No errors thrown.
- [ ] AC13: Listener cleanup on unmount — no memory leaks.

### `useStepMorph`

- [ ] AC14: Hook signature `useStepMorph<S extends string>(activeStep: S, durationMs?: number): { renderedStep: S; phase: 'in' | 'out' }`. Default duration: 150ms.
- [ ] AC15: When `activeStep` changes, `phase` becomes `'out'` immediately; after `durationMs` elapses, `renderedStep` updates to the new `activeStep` and `phase` becomes `'in'`.
- [ ] AC16: If `activeStep` changes again before the timer fires, the timer resets — the most recent step wins. No intermediate flickers.
- [ ] AC17: Timer cleanup on unmount — no setState on unmounted components.

---

## Technical constraints

- **No new dependency.** All four hooks are implementable in ~150 lines of TypeScript total. No `focus-trap-react`, no `body-scroll-lock`, no `react-resize-detector`.
- **All hooks live in `src/hooks/`** alongside the existing `useDayEntryUpsert` and `useDayEntryRead`. Naming matches the prevailing `use-*.ts` convention.
- **Tests live in `src/hooks/__tests__/use-*.test.ts`** mirroring the existing test layout.
- **Each hook handles SSR** — checks `typeof window !== 'undefined'` before touching browser APIs. Next.js server components or static generation that imports these must not crash.
- **Each hook respects `prefers-reduced-motion`** where motion-related (currently only `useStepMorph` flattens its duration to 0.01ms; documented inline).

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | No | Pure hooks |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | No data persisted |
| New dependency | ADR or step rationale | **No** | All hooks hand-rolled; bundle impact zero |
| `dangerouslySetInnerHTML` usage | A03 | No | — |
| New env var with a secret | A02, A05 | No | — |
| New telemetry / observability dep | Cardinal "no telemetry" | No | — |

## Plan

### 0.1 `src/hooks/use-focus-trap.ts`

```ts
import { useEffect } from 'react';

const FOCUSABLE_SELECTOR =
  'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

export function useFocusTrap(
  containerRef: React.RefObject<HTMLElement | null>,
  active: boolean,
): void {
  useEffect(() => {
    if (!active || !containerRef.current) return;
    const container = containerRef.current;
    const previouslyFocused = document.activeElement as HTMLElement | null;

    // Move focus into the container
    const focusables = container.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR);
    const first = focusables[0] ?? container;
    first.focus();

    function onKeyDown(event: KeyboardEvent) {
      if (event.key !== 'Tab') return;
      const items = Array.from(
        container.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR),
      );
      if (items.length === 0) {
        event.preventDefault();
        return;
      }
      const firstItem = items[0];
      const lastItem = items[items.length - 1];
      if (event.shiftKey && document.activeElement === firstItem) {
        event.preventDefault();
        lastItem.focus();
      } else if (!event.shiftKey && document.activeElement === lastItem) {
        event.preventDefault();
        firstItem.focus();
      }
    }

    document.addEventListener('keydown', onKeyDown);
    return () => {
      document.removeEventListener('keydown', onKeyDown);
      previouslyFocused?.focus();
    };
  }, [active, containerRef]);
}
```

### 0.2 `src/hooks/use-body-scroll-lock.ts`

Reference-counted, iOS-safe lock. Uses a module-level counter so concurrent callers stack.

```ts
import { useEffect } from 'react';

let lockCount = 0;
let savedScrollY = 0;

export function useBodyScrollLock(active: boolean): void {
  useEffect(() => {
    if (!active || typeof window === 'undefined') return;
    if (lockCount === 0) {
      savedScrollY = window.scrollY;
      document.body.style.position = 'fixed';
      document.body.style.top = `-${savedScrollY}px`;
      document.body.style.width = '100%';
    }
    lockCount += 1;
    return () => {
      lockCount -= 1;
      if (lockCount === 0) {
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        window.scrollTo(0, savedScrollY);
      }
    };
  }, [active]);
}
```

### 0.3 `src/hooks/use-visual-viewport.ts`

```ts
import { useEffect, useState } from 'react';

type ViewportSnapshot = {
  offsetTop: number;
  offsetLeft: number;
  width: number;
  height: number;
};

function snapshot(): ViewportSnapshot {
  if (typeof window === 'undefined') {
    return { offsetTop: 0, offsetLeft: 0, width: 0, height: 0 };
  }
  const vv = window.visualViewport;
  if (vv) {
    return {
      offsetTop: vv.offsetTop,
      offsetLeft: vv.offsetLeft,
      width: vv.width,
      height: vv.height,
    };
  }
  return {
    offsetTop: 0,
    offsetLeft: 0,
    width: window.innerWidth,
    height: window.innerHeight,
  };
}

export function useVisualViewport(): ViewportSnapshot {
  const [state, setState] = useState<ViewportSnapshot>(snapshot);

  useEffect(() => {
    if (typeof window === 'undefined' || !window.visualViewport) return;
    const onChange = () => setState(snapshot());
    window.visualViewport.addEventListener('resize', onChange);
    window.visualViewport.addEventListener('scroll', onChange);
    return () => {
      window.visualViewport?.removeEventListener('resize', onChange);
      window.visualViewport?.removeEventListener('scroll', onChange);
    };
  }, []);

  return state;
}
```

### 0.4 `src/hooks/use-step-morph.ts`

```ts
import { useEffect, useState } from 'react';

type Phase = 'in' | 'out';

export function useStepMorph<S extends string>(
  activeStep: S,
  durationMs = 150,
): { renderedStep: S; phase: Phase } {
  const [renderedStep, setRenderedStep] = useState<S>(activeStep);
  const [phase, setPhase] = useState<Phase>('in');

  useEffect(() => {
    if (activeStep === renderedStep) return;
    setPhase('out');
    const timer = setTimeout(() => {
      setRenderedStep(activeStep);
      setPhase('in');
    }, durationMs);
    return () => clearTimeout(timer);
  }, [activeStep, renderedStep, durationMs]);

  return { renderedStep, phase };
}
```

### 0.5 Index of public API

No barrel file (`src/hooks/index.ts`) — the existing convention is per-hook imports. Match that.

## Test plan

### `src/hooks/__tests__/use-focus-trap.test.ts` (~6 cases)

| # | Case |
|---|---|
| 1 | When `active` becomes true, focus moves to the first focusable element in the container |
| 2 | When `active` becomes false (or component unmounts), focus returns to the previously-focused element |
| 3 | Tab on the last focusable element wraps to the first |
| 4 | Shift+Tab on the first focusable element wraps to the last |
| 5 | Empty container (no focusables) — Tab preventDefault, focus stays on container |
| 6 | SSR safety: hook does nothing if `containerRef.current` is null |

### `src/hooks/__tests__/use-body-scroll-lock.test.ts` (~5 cases)

| # | Case |
|---|---|
| 1 | `active=true` applies `position: fixed`, `top: -<scrollY>px`, `width: 100%` on body |
| 2 | `active=false` restores body styles and `window.scrollY` |
| 3 | Two concurrent hooks: only the second deactivation actually unlocks |
| 4 | Unmount while active: cleanup runs, lock count decrements |
| 5 | SSR safety: no errors when `typeof window === 'undefined'` |

### `src/hooks/__tests__/use-visual-viewport.test.ts` (~4 cases)

| # | Case |
|---|---|
| 1 | Returns current viewport dimensions on mount |
| 2 | Updates state when `visualViewport.resize` fires (simulate via mock) |
| 3 | Fallback to `window.innerWidth/Height` when `visualViewport` is undefined |
| 4 | Cleanup removes listeners on unmount |

### `src/hooks/__tests__/use-step-morph.test.ts` (~5 cases)

| # | Case |
|---|---|
| 1 | Initial render: `renderedStep === activeStep`, `phase === 'in'` |
| 2 | Changing `activeStep`: `phase` becomes `'out'` immediately, `renderedStep` lags by 150ms |
| 3 | After timer fires: `renderedStep` updates to the new step, `phase` becomes `'in'` |
| 4 | Rapid changes (3 changes within 100ms): only the final value is rendered |
| 5 | Unmount during pending timer: no setState on unmounted component (no warning) |

## Done criteria

- [x] `useFocusTrap` shipped, 6 unit tests green ([src/hooks/use-focus-trap.ts](../../../src/hooks/use-focus-trap.ts))
- [x] `useBodyScrollLock` shipped, 5 unit tests green ([src/hooks/use-body-scroll-lock.ts](../../../src/hooks/use-body-scroll-lock.ts))
- [x] `useVisualViewport` shipped, 4 unit tests green ([src/hooks/use-visual-viewport.ts](../../../src/hooks/use-visual-viewport.ts))
- [x] `useStepMorph` shipped, 5 unit tests green ([src/hooks/use-step-morph.ts](../../../src/hooks/use-step-morph.ts))
- [x] Vitest count delta: +20 exactly (539 → 559)
- [x] `npm run verify` clean (lint + typecheck + 559/559)
- [x] No new entries in `package.json`

## Done

- [x] AC1–AC5 (useFocusTrap): all six it-blocks GREEN — see `src/hooks/__tests__/use-focus-trap.test.tsx`
- [x] AC6–AC9 (useBodyScrollLock): all five it-blocks GREEN — see `src/hooks/__tests__/use-body-scroll-lock.test.tsx`
- [x] AC10–AC13 (useVisualViewport): all four it-blocks GREEN — see `src/hooks/__tests__/use-visual-viewport.test.tsx`
- [x] AC14–AC17 (useStepMorph): all five it-blocks GREEN — see `src/hooks/__tests__/use-step-morph.test.tsx`
- [x] RED captured (per hook):
  - `npm test -- use-focus-trap.test` → 4 failed / 2 passed (no-op-tolerant cases passed against the stub) on 2026-05-28
  - `npm test -- use-body-scroll-lock.test` → 4 failed / 1 passed on 2026-05-28
  - `npm test -- use-visual-viewport.test` → 4 failed on 2026-05-28
  - `npm test -- use-step-morph.test` → 3 failed / 2 passed on 2026-05-28
- [x] GREEN captured: `npm run verify` → 52 test files / 559 tests passed on 2026-05-28
- [x] Type check: `npm run typecheck` clean
- [x] Lint: `npm run lint` clean
- [x] No new HIGH cardinal-principle / privacy / security findings (pure hooks, no new deps, no new data path)
- [x] Walkthrough: N/A — Step 0 does not touch a screen; the brainfog/one-handed walkthrough lands in Step 4
- [x] Refactor pass: none needed — each hook was implemented straight from the plan code and the test cases match 1:1 with the ACs

### Evidence

- Run id: `npm run verify` 2026-05-28 20:21, duration 9.75s
- Bundle impact: 0 KB (no new deps; hooks are stripped to ~15-30 LOC each)
- Test deltas:
  - `use-focus-trap.test.tsx`: 6 new
  - `use-body-scroll-lock.test.tsx`: 5 new
  - `use-visual-viewport.test.tsx`: 4 new
  - `use-step-morph.test.tsx`: 5 new
  - Total: +20

### Side-quests caught during implementation

- **`useVisualViewport` resize-event needs `act()` in tests.** The first GREEN attempt assumed the synchronous `fireResize` would propagate to the next snapshot read, but React's state update batched. Wrapping `fireResize` in `act()` is the canonical fix and the test now demonstrates the pattern for any future hook that listens to non-React DOM events.
- **Stub-first RED is the right shape for new modules.** The doctrine line *"It must fail for the reason you expect — the assertion mismatches, not a syntax error or missing import"* almost made me skip stub-creation. Created a no-op stub for each hook so the import resolves and tests fail on real behaviour assertions. The handoff document says to prefer the more-specific doc when conflicts arise, but here both docs agree once you read carefully — the test must fail on the assertion, which means the import has to resolve.
- **Doc tension (`lab/` quarantine vs hooks in `src/hooks/`)**: per the BUILD-HANDOFF "all new code under `src/components/lab/`", but Step 0's plan explicitly places hooks in `src/hooks/`. The hooks are reusable across the app (settings modals, future bottom-sheets) so the placement is intentional. Resolved per the handoff's own guidance ("pick the more specific doc"); no doc edits needed — the lab/ rule applies to feature-specific UI, hooks are infrastructure.

## Open questions to settle during implementation

- **`useFocusTrap` and shadow-DOM:** the `FOCUSABLE_SELECTOR` doesn't traverse shadow roots. Not a concern for this feature (we don't use shadow DOM), but document the limitation in a JSDoc comment for future readers.
- **`useBodyScrollLock` and modal stacking:** if a future feature opens a modal-inside-a-modal, the reference-counting handles it correctly, but the saved scroll position is captured only at the first lock. Document this in JSDoc.
- **`useVisualViewport` on Android:** Android Chrome behaviour differs slightly from iOS Safari — the keyboard sometimes resizes the window (not just the viewport). Worth testing once we have the BottomSheet hooked up, but the hook abstracts the difference correctly.
