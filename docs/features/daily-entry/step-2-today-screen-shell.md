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

- [x] `src/app/page.tsx` renders the shell with real data; presence-only auth check per the documented trade-off (matches `/login/2fa-setup` pattern). Stale-cookie users see the shell with `entry=null`; Step 4's first save triggers the 401 + /login redirect via the standard error handler.
- [x] `todayInAmsterdam` helper exists and is tested (added in Step 1 — was originally planned for Step 2.2)
- [x] `formatDateDutch` helper added to `src/lib/domain/date.ts` (3 unit tests)
- [x] `TodayShell` renders the wheel column (CSS scroll-snap, pre-positioned), 8 category-header buttons (inert per Step 5 plan), and note placeholder. ARIA: `role="listbox"` + `role="option"` for the wheel (proper WAI-ARIA pattern for picker); `aria-expanded={false}` on each category header.
- [x] Vitest count delta: +8 (3 date + 5 shell)
- [x] Playwright dev specs: +2 today-shell + 3 updated home-spec heading assertions; full chromium suite 30/30 plus 2 deferred (rate-limit live-stack); api project clean.
- [x] `npm run verify` clean: 416/416 Vitest, lint + typecheck both clean
- [ ] Visual walkthrough on phone (deferred — pending real session for the wheel to be useful)

### Side-quests caught during implementation

1. **JSX in tests needed the React plugin.** `@vitejs/plugin-react` added to `vitest.config.ts`; per-file `// @vitest-environment jsdom` opts component tests into jsdom while leaving the 400+ pure-logic tests in the (faster) Node environment. Also installed `@testing-library/react`, `@testing-library/jest-dom`, `@testing-library/user-event`, `jsdom`.

2. **Testing Library auto-cleanup doesn't fire with `globals: false`.** Each test's `render()` accumulated in the DOM, breaking subsequent `getByRole` queries with "found multiple elements". Fix: explicit `afterEach(cleanup)` at the top of the component-test describe block. Pattern carries forward to Steps 4+.

3. **CSP from audit-hardening Step 4 (M1) blocked dev-mode HMR.** This was the big one. The strict `script-src 'self' 'unsafe-inline'` ships to prod correctly (verified by live curl). But in dev mode, Next.js + webpack's hot-reload pipeline uses `eval()` to apply updates. With strict CSP, every page silently failed to hydrate — client-side JS never ran. 12 pre-existing e2e tests had been failing dormantly since the CSP shipped on 2026-05-27; nobody noticed because we'd run targeted specs (axe baseline, middleware) rather than the full chromium suite. **Fix:** dev-mode adds `'unsafe-eval'` to `script-src`; production CSP unchanged. See `next.config.ts` comment + `docs/features/auth-hardening/step-4-security-headers.md` follow-up note.

4. **Next/font/google introduced cold-load latency in dev mode.** Initial plan included `Inter` via `next/font`. Local testing showed 30s+ timeouts on subsequent Playwright runs — Inter was downloaded on each cold page request. Reverted to system-ui (already declared in `globals.css`); custom font deferred until a privacy + perf path is clearer.

5. **`role="group"` collided with the wheel's accessible name.** Original wheel used `role="group" aria-label="Score"`. Testing Library's `getByRole('group', { name: /score/i })` matched multiple elements (the wheel + the section that wrapped it after labelling). **Fix:** `role="listbox"` + `role="option"` — proper WAI-ARIA picker pattern, semantically richer, no collisions.

6. **`<ul role="list">` is redundant.** ESLint `jsx-a11y/no-redundant-roles` caught it. `<ul>` already has implicit role `list`. Dropped the explicit role; net: cleaner JSX.

### Evidence — full Playwright suite

```
50 passed, 2 skipped (deferred rate-limit live-stack)
  18 api (auth handler unhappy paths)
  30 chromium e2e (login + verify + 2fa-setup + middleware + home + a11y baseline + today-shell)
  2 skipped (rate-limit specs that run via npm run test:live)
```
