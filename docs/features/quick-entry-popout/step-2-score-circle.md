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

- [x] `ScoreCircle` component shipped at [`src/components/lab/score-circle.tsx`](../../../src/components/lab/score-circle.tsx) — single file, Tailwind utilities via `cn()`, ~125 LOC including comments
- [x] 10 unit tests green (2 over plan: split AC5 keyboard navigation into "ArrowRight" / "ArrowLeft+aliases" / "Home+End" for clarity; split clamp behaviour into upper + lower bound cases)
- [ ] 2 e2e tests green — **deferred to the Step-1-and-Step-2 batched e2e spec** noted at the head of step-1. The unit tests fully cover the pointer-mechanic contract jsdom can simulate; the real-touch and axe-core scans gain more signal when the circle is mounted inside the sheet inside the flow (Step 3).
- [x] Vitest count delta: +10 (570 → 580)
- [ ] Playwright count delta: 0 this step; batched after Step 3 lands
- [x] `npm run verify` clean (lint + typecheck + 580/580)
- [x] No new entries in `package.json`

## Done

- [x] AC1 (280px circle, score in centre, accent colour): static Tailwind classes + render-shape test "given initialValue=5..." GREEN; visual verification deferred to walkthrough
- [x] AC2 (horizontal drag, ~20px per integer): two it-blocks GREEN — "given a pointer drag of 20px right" + "given a rapid drag of 80px right"
- [x] AC3 (per-integer pulse, 80ms): "given an integer-cross during drag" GREEN with fake-timer advance verifying the pulse class clears
- [x] AC4 (snap on release, onCommit fires): every drag-based it-block asserts on onCommit's last call
- [x] AC5 (keyboard nav, role=slider + aria-valuemin/max/now): three it-blocks GREEN (ArrowRight, Arrow-aliases, Home/End)
- [x] AC6 (no tick marks, no rim labels): static render — no tick-mark elements rendered
- [x] AC7 (presentational, onCommit is the only egress): no other props or side-effects; review confirmed
- [x] AC8 (touch-action: none + setPointerCapture): `touch-none` Tailwind class + `setPointerCapture(pointerId)` on `pointerdown`. Stub-aware tests confirm the call.
- [x] AC9 (SSR-safe): no window/document access at render time; all DOM touches inside event handlers
- [x] RED captured: `npm test -- score-circle.test` → 10 failed against the null-returning stub on 2026-05-29
- [x] GREEN captured: `npm run verify` → 54 files / 580 tests on 2026-05-29
- [x] Type check + lint: clean
- [x] No new HIGH cardinal-principle / privacy / security findings (presentational primitive, no new deps, no new data path)
- [x] Walkthrough: N/A — Step 2 is a primitive. Visual + gesture walkthrough comes after Step 3 mounts the circle inside the sheet inside the flow.

### Evidence

- Run id: `npm run verify` 2026-05-29 01:06, duration 10.89s
- Bundle impact: 0 KB (no new deps)
- Visual contract verified against the source prototype `docs/design/explorations/score-circle-prototype.html`. The React port preserves the prototype's constants (`PIXELS_PER_INTEGER = 20`, `PULSE_MS = 80`, `MIN/MAX = 1/10`) and the pointer-down/move/up shape verbatim.

### Side-quests caught during implementation

- **`initialValue` as one-time read, not synced.** The component initialises state from `initialValue` once on mount and never reacts to prop changes. This matches the prototype's "one source of truth for the drag value" and the parent's typical usage (parent fetches the existing entry once, hands it down). If a future use case needs prop-controlled mode, add an `value` prop variant rather than mutating this behaviour — same separation as `defaultValue` vs `value` in React inputs.
- **Stale-closure trap in keyboard handler.** First draft called `setValue(value + 1)` then `onCommit(value)` — `value` is the closure-captured pre-update value, which leaks one keystroke of staleness. Reshaped to compute `next` synchronously and pass it to both `applyValue` and `onCommit` so the commit always carries the value the user just produced.
- **Stub-aware pulse cleanup.** Pulse uses a setTimeout; if the consumer unmounts mid-drag, the timer fires after unmount. Guarded with a `mountedRef` plus `clearTimeout` in the unmount cleanup. The "unmount during pending pulse" test confirms no setState-on-unmounted warning.

## Open questions (resolved)

- ~~**Fast drag pulse behaviour:**~~ Single integer-cross fires one pulse; subsequent crosses clear+restart the timer (the `clearTimeout` in `triggerPulse`). A 6-integer sweep yields six visible pulses spread across the move time. Visual verification deferred to mobile walkthrough — but the prototype already validated this on iPhone.
- ~~**Initial render flicker:**~~ See "initialValue as one-time read" above. No re-render on prop change; no flicker.
- ~~**Reduced motion:**~~ The 80ms transition flattens to 0.01ms under the global `prefers-reduced-motion: reduce` rule in `globals.css`. No per-component code needed.

---

## Open questions to settle during implementation

- **Fast drag pulse behaviour:** if user sweeps from 3 to 9 in 200ms, do we fire 6 individual pulses or coalesce? Prototype fires all 6 (with timers stacking via the latest-clear pattern). Visually fine on desktop; verify on iPhone after deploy.
- **Initial render flicker:** if `initialValue` arrives async (from a parent fetch), the component re-renders. Should be fine since the component reads it once into local state on mount. Verify no jump.
- **Reduced motion:** the 80ms pulse is below the 100ms threshold most users notice; `prefers-reduced-motion` flattens it via the global CSS rule. No special handling needed.
