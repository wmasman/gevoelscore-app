# Step 2: Today screen shell (read-only)

**Estimated time:** 1 hour
**Test layer:** Vitest component test (jsdom) for the score-row rendering + Playwright e2e against the dev server.
**Risk:** Low. No writes, no state machine — just a server component that fetches today's entry and renders it.
**Prerequisite:** Step 1 done.

> Replaces the current "Pre-prototype shell" home page with the real Blok 1 layout. No tap-to-save yet — the score row is rendered but disabled. This step is about getting the page structure, the auth gate, and the "today's entry from server" data path right before any state machine lands.

---

## Acceptance criteria

- [ ] AC1: `src/app/page.tsx` is a server component that fetches today's entry via the Step 1 `/api/day-entries/today` endpoint (or the SDK wrapper directly — see Technical constraints) before rendering.
- [ ] AC2: If today's entry exists, the score row shows the existing score as "active" (visual ring or fill) and the note + tags are rendered below.
- [ ] AC3: If no entry exists for today, the score row renders with no active state. Note + tags areas show their empty placeholders.
- [ ] AC4: An unauthenticated user lands on `/login` via middleware (existing behaviour). The page itself does not need its own auth check beyond what middleware enforces.
- [ ] AC5: The score row is 10 buttons (1–10), each ≥ 44px touch target, evenly spaced, ARIA-labelled per number, focus visible. **Buttons are `disabled` in this step** — Step 4 wires the tap.
- [ ] AC6: The page has a deliberate visual hierarchy: today's date prominent (Dutch format: "woensdag 27 mei 2026"), score row below, note + tags below. Single column on phone; centred max-width 480px on desktop.
- [ ] AC7: First contentful paint with cached SSR ≤ 200ms on a Slow 3G simulation (DevTools throttle). The server component does the data fetch; the client gets HTML with the score row pre-rendered.

## Technical constraints

- Server component — uses `fetch` against the same-origin `/api/day-entries/today` OR calls the SDK wrapper directly (cleaner, no extra HTTP hop). **Chose: SDK wrapper directly** — same-process call, no double-trip through the auth route.
- Auth: server components in Next 15 can read cookies via `cookies()` from `next/headers`. The page resolves the session like `2fa-setup/page.tsx` does today — uses `getValidatedSession` to ensure the access token is still valid (transparent refresh).
- Tailwind v4 for styling. No new UI dep. The 10-button row uses CSS grid with `grid-template-columns: repeat(10, 1fr)`.
- The note + tags areas are placeholder slots in this step — Step 5 fills them in. Empty state copy is Dutch: "Geen notitie" / "Geen tags".

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01, A03, A04, A07, A08 | No | This step is UI only |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | Read-only |
| New dependency | ADR or step rationale | No | Tailwind already in stack |
| `dangerouslySetInnerHTML` usage | A03 | No | Pure JSX |
| New env var with a secret | A02, A05 | No | — |
| New telemetry / observability dep | Cardinal "no telemetry" | No | — |

## Plan

### 2.1 Update `src/app/page.tsx`

Replace the prototype shell. Pseudocode:

```tsx
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { SESSION_COOKIE_NAME, parseSessionCookie } from '@/lib/auth/session';
import { getValidatedSession } from '@/lib/auth/get-validated-session';
import { readDayEntryByDate } from '@/lib/api/day-entries';
import { todayInAmsterdam } from '@/lib/domain/date';
import { TodayShell } from '@/components/today-shell';

export default async function HomePage() {
  const cookieStore = await cookies();
  const sessionId = parseSessionCookie(cookieStore.get(SESSION_COOKIE_NAME)?.value ?? null);
  const session = sessionId ? await getValidatedSession(sessionId) : null;
  if (!session) redirect('/login');

  const today = todayInAmsterdam();
  const result = await readDayEntryByDate(session.accessToken, today);
  const entry = result.ok ? result.value : null;

  return <TodayShell date={today} entry={entry} />;
}
```

### 2.2 New file: `src/lib/domain/date.ts` — `todayInAmsterdam()`

The data model says `date` is the user's local date. The user is in Amsterdam. Hard-coded TZ string `'Europe/Amsterdam'`. Returns `YYYY-MM-DD`.

```ts
export function todayInAmsterdam(): string {
  const fmt = new Intl.DateTimeFormat('sv-SE', { timeZone: 'Europe/Amsterdam' });
  return fmt.format(new Date());
}
```

(Sweden locale yields `YYYY-MM-DD` natively; avoids manual padding.)

### 2.3 New component: `src/components/today-shell.tsx`

Client component (`'use client'`) so future steps can wire `onClick`. For now: pure render.

Layout:
- `<h1>` date in Dutch
- `<div role="group" aria-label="Score">` with 10 buttons, all `disabled` and visually plain (Step 4 styles them)
- `<section>` "Notitie" with placeholder text
- `<section>` "Tags" with placeholder text

### 2.4 Style budget

Tailwind utility classes only. No new tokens. Font sizes from Tailwind's default ramp; contrast verified against WCAG AA at the component level.

## Test plan

### `src/lib/domain/__tests__/date.test.ts` (extend, +2 cases)

| # | Case |
|---|---|
| 1 | `todayInAmsterdam()` returns YYYY-MM-DD shape |
| 2 | At UTC midnight, `todayInAmsterdam()` returns the Amsterdam-local date (which may differ by 1) |

### `src/components/__tests__/today-shell.test.tsx` (new, jsdom, ~4 cases)

| # | Case |
|---|---|
| 1 | Renders the date in Dutch |
| 2 | Renders 10 score buttons, all disabled (this step) |
| 3 | Active button has the visible ring when `entry.score` matches |
| 4 | No active button when `entry` is null |

### `tests/e2e/daily-entry-today-shell.spec.ts` (new, 2 cases)

| # | Case |
|---|---|
| 1 | Authenticated user lands on `/` and sees the date + score row |
| 2 | Unauthenticated user is redirected to `/login` (already covered by `middleware.spec.ts` for `/`; sanity check that the new page didn't break the redirect) |

## Done criteria

- [ ] `src/app/page.tsx` renders the shell with real data
- [ ] `todayInAmsterdam` helper exists and is tested
- [ ] `TodayShell` component renders 10 disabled buttons + placeholders
- [ ] Vitest count delta: +6
- [ ] Playwright e2e +2
- [ ] `npm run verify` clean
- [ ] Visual walkthrough recorded (one-line in Done section): "on iPhone 12 Safari, the layout fits without scrolling and the score row is reachable with one thumb"
