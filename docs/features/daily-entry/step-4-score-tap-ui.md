# Step 4: Score wheel UI (the cardinal moment)

**Estimated time:** 2.5 hours
**Test layer:** Vitest component (jsdom + happy-dom-style scroll events) for the wheel state machine + Playwright e2e for the full optimistic-update flow against the dev server.
**Risk:** Medium-High. Scroll wheels are notoriously fiddly on the web, and this is the cardinal-principle moment — the sub-10s flow lives or dies here. The wheel must work for touch (drag), mouse (wheel), and keyboard (arrows).
**Prerequisite:** Steps 1–3 done.

> Wires the wheel from "rendered but inert" (Step 2) to a real interaction. First *deliberate* interaction promotes a fresh-day wheel from idle `5` to "set" + fires the PUT. Subsequent changes debounce-save 500ms after the wheel settles on a new integer. Touch/mouse/keyboard all map to the same state machine.

---

## Acceptance criteria

- [ ] AC1: A *fresh* day (no entry exists) opens the wheel at `5` in **idle** state — no accent ring, no PUT fired on page load. The wheel value is visually de-emphasised (lower opacity on the centred number, no surrounding badge) to communicate "not yet saved".
- [ ] AC2: First deliberate interaction on a fresh day — defined as any of: a touch-drag, a wheel-scroll event, an arrow-up/down keypress, or a tap on a visible non-centred value — **promotes the wheel to "set"** and immediately fires PUT `/api/day-entries/[today]` with the current centred value (which may still be `5` if the user just tapped `5`).
- [ ] AC3: After promotion, subsequent changes debounce-save 500ms after the wheel settles on a different integer than the last-saved value. "Settles" = the scroll-snap has come to rest on a new value AND no new scroll event has fired in 500ms.
- [ ] AC4: Re-positioning to the same integer that's already saved is a no-op (no PUT). Includes the "interactive but stable" case where the user wiggles past `7` to `8` and back to `7`.
- [ ] AC5: Tap on a visible non-centred value (e.g. `7` is offset two slots above centre, user taps it) smoothly scrolls the wheel to that value and triggers the save (subject to AC4's no-op rule).
- [ ] AC6: Arrow-up = centre moves to next-higher value (towards `10`); arrow-down = towards `1`. Page-up/page-down jump 3 values. Home = `1`, End = `10`.
- [ ] AC7: Stopwatch test: from "open app on fresh day" to "saved indicator visible after one scroll" ≤ 2s. The optimistic update means the indicator flips before the response lands.
- [ ] AC8: Network failure path (DevTools throttle = Offline) reverts the wheel to the last-saved value (or back to idle if it was the first save) and shows the same "Niet opgeslagen — probeer nogmaals" banner used in Step 5/6.
- [ ] AC9: Two rapid changes (e.g. scroll past `4` to `5` to `6` to `7` in under 500ms) result in **one** PUT for the final settled value, not three.
- [ ] AC10: The visible accent ring on the centred value appears the moment the wheel is "set", regardless of save success/failure. The save status (saving / saved / failed) is communicated by a small adjacent indicator, not by changing the ring itself.

## Technical constraints

- **No new dependency.** The wheel is a CSS-scroll-snap column + an `IntersectionObserver` (to detect which value is centred) + a small state machine. Total LOC budget: ~120 across the component file + its test.
- The wheel container has `scroll-snap-type: y mandatory; overflow-y: auto; height: 5 * 44px` (shows 5 items: the centred value + 2 each side). Each item has `scroll-snap-align: center; height: 44px`.
- `IntersectionObserver` with `rootMargin: -44%` brackets the centre-line; the item that's `isIntersecting` is the current value.
- Detect "settled" via the `scrollend` event (now broadly supported) — fallback: a 500ms `setTimeout` reset on every `scroll` event.
- The state machine has three states: `idle` (fresh day, no save yet), `set` (saved at least once; subsequent changes auto-save), `error` (last save failed; UI revert + banner; next interaction tries to save again).

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | No | Route is Step 3; this is the client |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | Write flows through Step 3's logged route |
| New dependency | ADR or step rationale | No | No new deps; the wheel is custom |
| `dangerouslySetInnerHTML` usage | A03 | No | — |
| New env var with a secret | A02, A05 | No | — |
| New telemetry / observability dep | Cardinal "no telemetry" | No | — |

## Plan

> **Reuse strategy.** This step also introduces the two shared primitives the rest of the daily-entry feature will lean on: `useDayEntryUpsert(date)` hook and `<SaveStatus />` component. See the README's "Component architecture" section. The wheel is the first caller of both — Steps 5 and 6 reuse them rather than duplicate.

### 4.0 New shared hook: `src/hooks/use-day-entry-upsert.ts`

```ts
export function useDayEntryUpsert(date: string) {
  const [status, setStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');
  const [lastError, setLastError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const settleRef = useRef<number | null>(null);
  const pendingRef = useRef<Partial<DayEntryPatch> | null>(null);

  async function save(patch: Partial<DayEntryPatch>) {
    // 1. merge into pendingRef
    // 2. reset settle timer
    // 3. fire after 500ms idle (or immediately if `flush: true` opt-in)
    // 4. AbortController-cancel in-flight; new request wins
    // 5. setStatus per response
  }

  return { save, status, lastError };
}
```

The hook is the *only* place that talks to `/api/day-entries/[date]`. Components send `patch` shapes; the hook handles transport, debounce, abort, and status. Tested independently of any UI.

### 4.1 New shared component: `src/components/save-status.tsx`

```tsx
type Props = { status: 'idle' | 'saving' | 'saved' | 'error'; error?: string | null };
export function SaveStatus({ status, error }: Props) { /* renders per AC of README */ }
```

Pure render based on its props. No state. Tested via 4 snapshots (one per status).

### 4.2 New component: `src/components/score-wheel.tsx`

```tsx
'use client';
import { useRef, useState } from 'react';
import { useDayEntryUpsert } from '@/hooks/use-day-entry-upsert';
import { SaveStatus } from '@/components/save-status';

type Props = { date: string; initialScore: number | null };

export function ScoreWheel({ date, initialScore }: Props) {
  const wheelRef = useRef<HTMLDivElement>(null);
  const lastSavedRef = useRef<number | null>(initialScore);
  const [centred, setCentred] = useState<number>(initialScore ?? 5);
  const [phase, setPhase] = useState<'idle' | 'set'>(initialScore ? 'set' : 'idle');
  const { save, status, lastError } = useDayEntryUpsert(date);

  // IntersectionObserver tracks which value is centred
  // First interaction in idle phase → promote to set + save({ score: centred })
  // Settled change in set phase → save({ score: centred }) (hook debounces)
  // Hook handles abort / status / revert
  // ...
  return (
    <div>
      <div ref={wheelRef} /* wheel column */ />
      <SaveStatus status={status} error={lastError} />
    </div>
  );
}
```

Key behaviours:
- On mount: pre-scroll to `initialScore ?? 5` using `wheelRef.current.scrollTop`.
- `IntersectionObserver` updates `centred` on every snap.
- Any scroll/keyboard/tap event in `idle` → promote to `set` and fire save with the new `centred` (don't wait for settle on first save — feels more responsive).
- After `set`, save fires on `scrollend` (or 500ms after last scroll if `scrollend` unavailable) IF `centred !== lastSavedRef.current`.

### 4.2 Update `src/components/today-shell.tsx`

Replace the static wheel placeholder from Step 2 with `<ScoreWheel date={date} initialScore={entry?.score ?? null} />`.

### 4.3 The save call

The wheel doesn't implement save logic — it calls `save({ score: centred })` from `useDayEntryUpsert`. The hook handles:
- AbortController-cancel of in-flight requests
- 500ms settle debounce when called rapidly (the wheel can scroll past multiple values; only the final one saves)
- Status transitions (`idle → saving → saved` / `→ error`)
- Optimistic revert on failure (the wheel reads `lastSavedRef` to decide what to display on error)
- The PUT body: just the patch from the caller — the route handler preserves unspecified fields per Step 3's upsert semantics

### 4.4 Visual states

- **Idle**: centred number ≤ 50% opacity, no ring. Above + below neighbours visible at lower opacity.
- **Set + saved**: centred number 100% opacity, single 2px ring, small green check fade-in next to it for 800ms.
- **Set + saving**: centred number 100% opacity, ring present, small spinner or "…" next to it.
- **Set + error**: centred number reverts to lastSaved value, ring present, red banner above with retry hint.

### 4.5 Keyboard

`onKeyDown` on the wheel container:
- `ArrowUp` / `ArrowDown` → `scrollBy({top: ±44, behavior: 'smooth'})`. The snap + IntersectionObserver handles the rest.
- `Home` → `scrollTop = 0`. `End` → `scrollTop = scrollHeight`.
- `PageUp` / `PageDown` → `scrollBy(±132)`.
- Wheel container has `tabIndex={0}` so it can receive keyboard focus.

## Test plan

### `src/hooks/__tests__/use-day-entry-upsert.test.ts` (new, jsdom, ~8 cases)

| # | Case |
|---|---|
| 1 | `save` with a patch fires PUT to `/api/day-entries/[date]` with the patch body |
| 2 | Rapid `save` calls (3 in 200ms) coalesce to one PUT with the merged final patch |
| 3 | 200 response → status `saved`; lastError null |
| 4 | 500 response → status `error`; lastError populated |
| 5 | AbortError on superseded request → status unchanged |
| 6 | Network failure (fetch reject) → status `error` |
| 7 | After error, next `save` call clears the error and tries again |
| 8 | Component unmount aborts any pending request |

### `src/components/__tests__/save-status.test.tsx` (new, jsdom, 4 cases)

One render-snapshot per status (`idle`, `saving`, `saved`, `error`).

### `src/components/__tests__/score-wheel.test.tsx` (new, jsdom, ~10 cases)

| # | Case |
|---|---|
| 1 | Fresh day: renders centred at `5` in idle state (no ring) |
| 2 | Existing entry: renders centred at saved score in set state (ring visible) |
| 3 | First scroll on idle wheel → fires PUT with current `centred` value + state becomes set |
| 4 | Settled scroll change after set → fires PUT with new value |
| 5 | Scrolling past a value back to the saved one → no PUT (AC4) |
| 6 | Tap on visible non-centred value → smooth scroll + save |
| 7 | ArrowUp key → centred increments toward 10 + save |
| 8 | 500 response → state reverts, error banner visible |
| 9 | Rapid scrolls (3 events in 200ms) → debounce coalesces to 1 PUT |
| 10 | AbortError on superseded request → no UI revert, no error |

(jsdom doesn't natively fire `scrollend`. Test workaround: dispatch a `scroll` event then `vi.advanceTimersByTime(500)` to trigger the settle-timer fallback path.)

### `tests/e2e/daily-entry-score-wheel.spec.ts` (new, ~4 cases)

| # | Case |
|---|---|
| 1 | Fresh day: load `/`, wheel at `5` in idle (no ring); scroll/keyboard down to `4` → PUT lands; ring + saved indicator appear |
| 2 | Existing entry: load `/`, wheel at saved score; scroll to a new value → PUT lands |
| 3 | Offline (`context.setOffline(true)`) + scroll → error banner; wheel reverts |
| 4 | Rapid scroll across 3 values → exactly 1 PUT in the network log |

## Done criteria

- [ ] `useDayEntryUpsert` hook shipped, 8 unit tests green (the foundation Steps 5 + 6 build on)
- [ ] `SaveStatus` component shipped, 4 render-snapshot tests green
- [ ] `ScoreWheel` shipped, 10 unit tests green
- [ ] `TodayShell` integrates `ScoreWheel` (replaces the Step 2 inert placeholder)
- [ ] Playwright e2e: 4 new specs green
- [ ] Stopwatch walkthrough (open → scroll → saved indicator) ≤ 2s on phone — recorded in Done section
- [ ] One-handed thumb scroll works (vertical wheel is thumb-native)
- [ ] Brainfog walkthrough: deliberate 2s pause before scrolling — the wheel doesn't time out or require a wake-up tap
- [ ] Keyboard walkthrough: tab to wheel, arrow keys change value, save fires
- [ ] Vitest count delta: +22 (8 hook + 4 SaveStatus + 10 wheel)
- [ ] Playwright dev specs +4
- [ ] `npm run verify` clean

## Open questions to settle during implementation

- **`scrollend` browser support**: as of mid-2026 Chrome/Edge/Firefox support it; Safari shipped in 17.2. If a tested-version of iOS Safari fails on `scrollend`, the 500ms-after-last-scroll fallback handles it. Document the fallback explicitly in the code.
- **Wheel "overshoot" on heavy scroll**: a hard flick on iOS scrolls past several values before snapping. That's fine for the UX (user can see where they ended up) and the debounce ensures only one save. No special handling needed.
- **Reduced-motion preference**: `prefers-reduced-motion: reduce` should disable the smooth-scroll animation on keyboard-driven changes (use `scrollTo({behavior: 'auto'})` instead of `'smooth'`). Trivial CSS+JS handling, included.
