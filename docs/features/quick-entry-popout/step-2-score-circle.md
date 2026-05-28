# Step 2: ScoreCircle component

**Estimated time:** 2.5 hours
**Test layer:** Vitest component tests (jsdom + pointer-event simulation) for value commit, snap-to-integer, scale-pulse, keyboard navigation. Playwright e2e for the gesture on a real touchscreen target.
**Risk:** Low. The gesture mechanic is fully validated by the score-circle HTML prototype on iPhone PWA (see [validation log](../../design/explorations/quick-entry-popout.md#validation-log)).
**Prerequisite:** None code-wise. Spec-wise: the score-circle mechanic in the [feature README AC11–AC16](README.md#score-step) is the contract this component fulfills.

> **Status: outline.** Full step detail will be filled in as we approach `/build-step`. This file captures scope, ACs, and the implementation shape so the work is unambiguous before we start coding.

---

## Scope summary

A presentational React component that wraps the validated score-circle mechanic. Native pointer events, no library. Lives at `src/components/lab/score-circle.tsx`.

```tsx
type Props = {
  initialValue?: number;            // default: 5
  onCommit: (value: number) => void; // fires on pointer release after a drag
  ariaLabel: string;
};
```

The component owns its drag state and the displayed value during drag. The consumer hooks into `onCommit` to save. Snap-to-integer happens automatically. Scale-pulse fires on every integer cross.

---

## Acceptance criteria

Inherited verbatim from the feature README — AC11 through AC16. Replicated here for self-containment:

- [ ] AC1 (== README AC11): Decorative circle ~280px diameter, max 80vw, capped to viewport. Current score in centre, display-size weight 600 `--color-accent`.
- [ ] AC2 (== README AC12): Horizontal drag inside the circle changes value. ~20px per integer step. Drag-zone is the circle itself, not the parent.
- [ ] AC3 (== README AC13): Number updates per integer crossed during drag, no decimals shown. 80ms scale-pulse (1.0 → 1.05 → 1.0) on each integer-cross.
- [ ] AC4 (== README AC14): On pointer release, snap to nearest integer = commit. `onCommit(value)` fires.
- [ ] AC5 (== README AC15): Keyboard navigation — `ArrowLeft`/`Right` (and `ArrowDown`/`Up` aliases) ±1; `Home` = 1, `End` = 10. `role="slider"` + `aria-valuemin/max/now`.
- [ ] AC6 (== README AC16): No tick marks rendered on the rim; no labels at "1" or "10".

Additional component-level:

- [ ] AC7: Component is presentational — no calls to any hook from `daily-entry/`. `onCommit` is the only way state leaves the component.
- [ ] AC8: `touch-action: none` set on the circle element via CSS. `setPointerCapture()` called on pointerdown. Tested in unit + e2e to confirm the gesture isolation contract from the prototype holds.
- [ ] AC9: Component is server-render safe (the gesture logic lives in event handlers, not render).

---

## Implementation reference

The single-piece prototype at [`docs/design/explorations/score-circle-prototype.html`](../../design/explorations/score-circle-prototype.html) is the source of truth for the gesture logic. The React port is a near-direct translation:

- `pointerdown` → set `dragStartValue`, `dragStartX`, capture pointer, prevent default
- `pointermove` → compute `delta / 20`, call internal `setValue` (only re-renders on integer change)
- `pointerup` / `pointercancel` → release capture, fire `onCommit`
- `setValue` triggers a pulse class on the number; cleared after 80ms via `setTimeout`

Total component LOC: ~80 (TypeScript + CSS module).

---

## Test plan (stub — to be expanded at `/build-step` time)

### `src/components/lab/__tests__/score-circle.test.tsx` (~8 cases)

1. Initial render: shows `initialValue ?? 5`, no pulse, `aria-valuenow` matches
2. `pointerdown` + `pointermove` 20px right + `pointerup`: `onCommit` fires with `initialValue + 1`
3. Rapid `pointermove` 80px right + `pointerup`: `onCommit` fires with `initialValue + 4` (no intermediate commits)
4. `pointermove` past bounds: clamped to 1..10
5. Integer-cross during drag: pulse class added to number element, removed after 80ms
6. `ArrowRight` key: `onCommit` fires with `currentValue + 1`
7. `Home` key: `onCommit` fires with 1
8. Unmount during drag: no setState on unmounted (no warning)

### `tests/e2e/quick-entry-popout-score-circle.spec.ts` (~2 cases)

1. Touch-drag horizontally on the circle: number updates smoothly, snaps on release
2. axe-core scan: zero violations on the circle's `role="slider"` semantics

---

## Done criteria

- [ ] `ScoreCircle` component shipped, 8 unit tests green
- [ ] 2 e2e tests green
- [ ] Vitest count delta: +8
- [ ] Playwright count delta: +2
- [ ] `npm run verify` clean
- [ ] No new entries in `package.json`

---

## Open questions to settle during implementation

- **Fast drag pulse behaviour:** if user sweeps from 3 to 9 in 200ms, do we fire 6 individual pulses or coalesce? Prototype fires all 6 (with timers stacking via the latest-clear pattern). Visually fine on desktop; verify on iPhone after deploy.
- **Initial render flicker:** if `initialValue` arrives async (from a parent fetch), the component re-renders. Should be fine since the component reads it once into local state on mount. Verify no jump.
- **Reduced motion:** the 80ms pulse is below the 100ms threshold most users notice; `prefers-reduced-motion` flattens it via the global CSS rule. No special handling needed.
