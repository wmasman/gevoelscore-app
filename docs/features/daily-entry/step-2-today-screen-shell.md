# Step 2: Today screen shell (read-only)

**Estimated time:** 1 hour
**Test layer:** Vitest component test (jsdom) for the layout rendering + Playwright e2e against the dev server.
**Risk:** Low. No writes, no state machine — just a server component that fetches today's entry and renders the inert layout (wheel placeholder + collapsed tag stack).
**Prerequisite:** Step 1 done.

> Replaces the current "Pre-prototype shell" home page with the real Blok 1 layout. No save logic yet — the wheel is a static placeholder showing today's score (or `5` if no entry), and the tag stack renders its 8 collapsed category headers but tapping them is inert. This step is about getting the page structure, the auth gate, and the "today's entry from server" data path right before any interaction lands.

---

## Acceptance criteria

- [ ] AC1: `src/app/page.tsx` is a server component that fetches today's entry via the Step 1 `/api/day-entries/today` endpoint (or the SDK wrapper directly — see Technical constraints) before rendering.
- [ ] AC2: If today's entry exists, the wheel renders centred at the saved score and is marked "set" (note + tags interactive once Step 5 lands).
- [ ] AC3: If no entry exists for today, the wheel renders centred at `5` in idle state (no accent ring; visually de-emphasised vs. the "set" appearance). Note + tags are visually disabled (greyed) until the wheel is promoted to "set" in Step 4.
- [ ] AC4: An unauthenticated user lands on `/login` via middleware (existing behaviour). The page itself does not need its own auth check beyond what middleware enforces.
- [ ] AC5: The wheel is a vertical scroll-snap column of values 1–10. Visible items: the centred value at full opacity + 2 above + 2 below at decreasing opacity (so the user can see neighbours). Each item ≥ 44px tall. Scroll position is settable in this step (CSS only) but no save handler — Step 4 wires that.
- [ ] AC6: Below the wheel, eight collapsed category headers in a vertical stack: "mentaal", "fysiek", "overall", "activiteit", "gebeurtenis", "interventie", "project", "custom". Each header is tappable (visual hover/active state) but the expand action is inert in this step — Step 5 wires it.
- [ ] AC7: The page has a deliberate visual hierarchy: today's date prominent (Dutch format: "woensdag 27 mei 2026"), wheel below, note placeholder below, then the 8 category headers. Single column on phone; centred max-width 480px on desktop.
- [ ] AC8: First contentful paint with cached SSR ≤ 200ms on a Slow 3G simulation (DevTools throttle). The server component does the data fetch + the tag list fetch; the client receives HTML with the wheel pre-positioned and the category headers pre-rendered.

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

Client component (`'use client'`) so future steps can wire interaction. For now: pure render.

Layout:
- `<h1>` date in Dutch
- `<div className="score-wheel-frame" role="group" aria-label="Score">` containing 10 `<div data-score={n}>` items in a vertical scroll-snap column. CSS only: `scroll-snap-type: y mandatory`; each item `scroll-snap-align: center`. Item heights ≥ 44px. Initial scroll position set inline via `scrollTop` based on `entry?.score ?? 5`.
- `<section>` "Notitie" placeholder text + visually-disabled state when `entry === null`.
- `<section>` "Tags" with 8 `<button data-category={c}>` headers. No expanded chips in this step.

### 2.4 Style budget

Tailwind utility classes only. No new tokens. Font sizes from Tailwind's default ramp; contrast verified against WCAG AA at the component level.

## Test plan

### `src/lib/domain/__tests__/date.test.ts` (extend, +2 cases)

| # | Case |
|---|---|
| 1 | `todayInAmsterdam()` returns YYYY-MM-DD shape |
| 2 | At UTC midnight, `todayInAmsterdam()` returns the Amsterdam-local date (which may differ by 1) |

### `src/components/__tests__/today-shell.test.tsx` (new, jsdom, ~5 cases)

| # | Case |
|---|---|
| 1 | Renders the date in Dutch |
| 2 | Renders the wheel column with 10 `<div data-score>` items |
| 3 | Wheel is centred on `entry.score` when an entry exists (assert via inline `scrollTop` style) |
| 4 | Wheel is centred on `5` when no entry exists; "set" indicator is absent |
| 5 | Renders 8 category-header buttons matching the locked enum |

### `tests/e2e/daily-entry-today-shell.spec.ts` (new, 2 cases)

| # | Case |
|---|---|
| 1 | Authenticated user lands on `/` and sees the date + score row |
| 2 | Unauthenticated user is redirected to `/login` (already covered by `middleware.spec.ts` for `/`; sanity check that the new page didn't break the redirect) |

## Done criteria

- [ ] `src/app/page.tsx` renders the shell with real data
- [ ] `todayInAmsterdam` helper exists and is tested
- [ ] `TodayShell` renders the wheel column (CSS scroll-snap, pre-positioned) + 8 category-header buttons + note placeholder
- [ ] Vitest count delta: +7 (2 date + 5 shell)
- [ ] Playwright e2e +2
- [ ] `npm run verify` clean
- [ ] Visual walkthrough recorded (one-line in Done section): "on iPhone 12 Safari, the layout fits without scrolling; the wheel sits centred at the correct value; tapping a category header gives visible feedback even though the expand action is inert"
