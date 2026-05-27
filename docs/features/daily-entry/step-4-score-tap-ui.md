# Step 4: Score-tap UI (the cardinal moment)

**Estimated time:** 2 hours
**Test layer:** Vitest component (jsdom) for the tap logic + Playwright e2e for the full optimistic-update flow against the dev server.
**Risk:** Medium. This is the cardinal-principle moment — the sub-10s flow lives or dies here. Behaviour bugs in the optimistic update path are user-visible immediately.
**Prerequisite:** Steps 1–3 done.

> Wires the score row from "rendered but disabled" (Step 2) to "tap a number, it saves." Optimistic update on the client; PUT against `/api/day-entries/[date]` server-side; reconcile on response. AC1–AC4, AC8–AC10 from the feature README.

---

## Acceptance criteria

- [ ] AC1: Tapping any 1–10 button fires a PUT request to `/api/day-entries/[today]` with `{ score }`. The visual active state flips to the tapped number *before* the response lands.
- [ ] AC2: On 200, the visual state is replaced by the server's authoritative `entry` (a no-op for the score itself; ensures `updated_at` and any backend-side fields are in sync).
- [ ] AC3: On 4xx/5xx/network failure, the visual state reverts to the previous score and a small toast/banner shows "Niet opgeslagen — tik nogmaals om te proberen". Tapping the same number again retries.
- [ ] AC4: While a request is in flight, the score row is *not* disabled — a follow-up tap is allowed and supersedes the previous request (Stale-While-Revalidate-style with request cancellation via `AbortController`).
- [ ] AC5: The "tapped" button is focused + has a visible ring + a subtle scale animation (≤ 100ms). Keyboard users can tab through the row.
- [ ] AC6: Stopwatch test: from "tap the score" to "saved indicator visible" ≤ 1s on a dev-mode local connection. The optimistic update means this is mostly perceived; the server round-trip can take up to ~300ms without breaking the UX.
- [ ] AC7: Re-tapping the same score that's already active is a no-op visually + skips the network call (saves a wasted PUT).
- [ ] AC8: Network failure under DevTools Network Throttle = Offline produces the AC3 error path. Verified in Playwright with `context.setOffline(true)`.

## Technical constraints

- Client component for the score row. Server component passes the initial `entry` (from Step 2) as a prop.
- State machine: `{ status: 'idle' | 'saving' | 'error', score: number | null, lastError?: string }`. Three transitions only: `tap → saving`, `200 → idle`, `error → error`. A second tap during `saving` cancels the in-flight request and starts a new one.
- No new state-management dep. Plain React `useState` + a `useRef<AbortController>` for the in-flight cancel. The state machine is small; introducing Zustand/Redux/Jotai would be premature.
- `fetch` against same-origin `/api/day-entries/[date]` with `credentials: 'same-origin'` (cookie auto-sent). No client-side token handling.
- The component lives at `src/components/score-row.tsx`. The `TodayShell` from Step 2 imports it and drops it where the disabled stub was.

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | No | Route is Step 3; this is the client |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | Write flows through Step 3's logged route |
| New dependency | ADR or step rationale | No | No new deps; if a state lib is added later, ADR required |
| `dangerouslySetInnerHTML` usage | A03 | No | — |
| New env var with a secret | A02, A05 | No | — |
| New telemetry / observability dep | Cardinal "no telemetry" | No | — |

## Plan

### 4.1 New component: `src/components/score-row.tsx`

```tsx
'use client';
import { useRef, useState } from 'react';

type Props = { date: string; initialScore: number | null };

export function ScoreRow({ date, initialScore }: Props) {
  const [score, setScore] = useState(initialScore);
  const [status, setStatus] = useState<'idle' | 'saving' | 'error'>('idle');
  const abortRef = useRef<AbortController | null>(null);
  const lastSavedRef = useRef<number | null>(initialScore);

  async function tap(n: number) {
    if (n === score && status === 'idle') return; // AC7 — no-op for same score
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setScore(n);
    setStatus('saving');

    try {
      const res = await fetch(`/api/day-entries/${date}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ score: n }),
        signal: controller.signal,
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      lastSavedRef.current = data.entry.score;
      setStatus('idle');
    } catch (e) {
      if ((e as Error).name === 'AbortError') return; // superseded by next tap
      setScore(lastSavedRef.current); // revert
      setStatus('error');
    }
  }

  return (/* 10 buttons + error banner */);
}
```

### 4.2 Update `src/components/today-shell.tsx`

Replace the disabled stub with `<ScoreRow date={date} initialScore={entry?.score ?? null} />`.

### 4.3 Style budget

- Buttons: `w-12 h-12` minimum (≥ 48px = WCAG); tablet+ can grow.
- Active: ring + bg shift; subtle so it doesn't shout.
- Disabled state: removed (per AC4, taps remain allowed during saving).
- Error banner: red bg, white text, role="alert", dismissible by next successful tap.

## Test plan

### `src/components/__tests__/score-row.test.tsx` (new, jsdom, ~7 cases)

| # | Case |
|---|---|
| 1 | Renders 10 buttons, initial score has the active class |
| 2 | Tap on 7 calls fetch with `PUT /api/day-entries/2026-05-27` body `{score:7}` |
| 3 | 200 response → status returns to idle; lastSaved updated |
| 4 | 500 response → score reverts to previous; error banner visible |
| 5 | Network reject (AbortError) → no revert, no error (superseded tap path) |
| 6 | Tap on same active score → no fetch call (AC7) |
| 7 | Two taps in quick succession: first request aborted, second wins |

### `tests/e2e/daily-entry-score-tap.spec.ts` (new, ~3 cases)

| # | Case |
|---|---|
| 1 | Authenticated user taps score 5; the button shows active; a row exists in the (mocked) API call |
| 2 | Network offline (`context.setOffline(true)`) → tap shows error banner; score reverts |
| 3 | Tap → tap-different → second tap wins, first is aborted |

## Done criteria

- [ ] `ScoreRow` component shipped + 7 unit tests green
- [ ] `TodayShell` integrates `ScoreRow`
- [ ] Playwright e2e specs green (3 new)
- [ ] Stopwatch walkthrough: ≤ 5s from app-open to saved indicator (record in Done section)
- [ ] One-handed-low-light walkthrough: every score is reachable with a single thumb on iPhone 12 Safari
- [ ] Brainfog walkthrough: deliberate 2s delay between "see the row" and "tap"; flow does not require re-render or extra tap
- [ ] Vitest count delta: +7
- [ ] Playwright dev specs +3
- [ ] `npm run verify` clean
