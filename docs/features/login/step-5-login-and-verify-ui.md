# Step 5: /login + /login/verify UI pages

**Estimated time:** 1.5–2 hours
**Test layer:** Playwright e2e (real browser) — pages are thin enough that component-tier tests would duplicate coverage.
**Risk:** Low — pages compose the Step 4 routes through standard form-submit + fetch. No new auth logic.
**Prerequisite:** Step 4 (route handlers) — done.

> TDD: Playwright e2e specs are written RED-first, against the unbuilt pages.

---

## Acceptance criteria (subset of feature README's 18 ACs)

`/login`:

- [ ] AC1: Submitting valid creds against a non-2FA account → navigates to `/` (success cookie set by Step 4 route).
- [ ] AC2: Submitting valid creds against a 2FA account → navigates to `/login/verify` (server has set the pending cookie).
- [ ] AC3: Invalid creds → page shows a single generic "Onjuiste e-mail of wachtwoord" message. No "user not found" leaks.
- [ ] AC4 (cardinal-principle sub-10s):
  - Autofocus lands on the email input on page load
  - Email input has `autocomplete="email"` and `type="email"` so the browser autofill panel works
  - Password input has `autocomplete="current-password"` and `type="password"`
  - Pressing Enter from either field submits the form
  - The submit button is the primary, large element on the screen
  - During submission the button is disabled and shows a loading label

`/login/verify`:

- [ ] AC6: Valid OTP → navigates to `/`.
- [ ] AC7: Invalid OTP → page shows a single generic "Code ongeldig" message; the input is cleared so the user can retry.
- [ ] AC9 (cardinal-principle brainfog):
  - OTP input has `inputmode="numeric"` (mobile numeric keyboard)
  - Accepts at most 6 digits (non-digit input filtered out)
  - Auto-submits the moment the 6th digit lands (no extra Submit tap)
- [ ] AC10: Navigating directly to `/login/verify` without a `gs_pending_otp` cookie → server-side redirect to `/login`.

## Technical constraints (this step)

- All UI text in Dutch — primary daily-driver context. (TS strings only; no i18n library needed in v1.)
- `/login/page.tsx` is a client component (form interactivity).
- `/login/verify/page.tsx` is a **server component** that reads the `gs_pending_otp` cookie via `cookies()` from `next/headers`. If missing → `redirect('/login')`. The form itself is split into `verify-form.tsx` with `'use client'`.
- No new dependencies. Form state lives in `useState` + native form submit.
- Submit handlers POST to `/api/auth/login` and `/api/auth/login/verify`. Cookies set by the route handlers travel via `credentials: 'same-origin'` (the default for same-origin fetch).
- No retry counter exposed in the UI on either page (security-checklist A05/A07).
- Tailwind v4 for styling — utility classes inline, no separate stylesheet for these pages.

## Test plan

Two Playwright e2e specs. Mock the `/api/auth/login` and `/api/auth/login/verify` responses via `page.route()` to exercise the happy + branch paths without needing a live Directus user.

### `tests/e2e/login.spec.ts`

- Renders `/login`; email input is `[autocomplete=email]` and is focused on load.
- Submitting with an invalid format is blocked by the browser's HTML form validation.
- Submitting valid creds against a mocked `{ ok: true }` response → URL becomes `/`.
- Submitting valid creds against a mocked `{ requires_otp: true }` response → URL becomes `/login/verify`.
- Submitting valid creds against a real 401 response → page shows the Dutch invalid-credentials message.
- Enter from the password field submits.

### `tests/e2e/login-verify.spec.ts`

- Navigating to `/login/verify` without the pending cookie → URL becomes `/login`.
- Navigating with the pending cookie present → form renders, OTP input has `inputmode="numeric"`.
- Typing 6 digits triggers a POST to `/api/auth/login/verify` (mocked → `{ ok: true }`) → URL becomes `/`.
- Mocked invalid-otp response → page shows the Dutch invalid-code message and clears the input.

---

## Done criteria

- [x] Pages exist + Playwright specs all green (11/11 new pass)
- [x] Existing Vitest + Playwright suites still green (no regressions — 323 Vitest, 28 Playwright + 2 skipped)
- [x] `npm run typecheck` clean
- [x] `npm run lint` clean
- [ ] Brainfog walkthrough: deferred — needs actual deploy and a phone in hand; will batch with Step 8.

### Captured evidence

- **RED**: `npm run test:e2e -- tests/e2e/login.spec.ts tests/e2e/login-verify.spec.ts` → 11 failed (pages didn't exist yet) on 2026-05-27.
- **First GREEN attempt**: 2 strict-mode violations on `getByRole('alert')` — Next.js injects its own route announcer `<div role="alert" id="__next-route-announcer__">`. Switched both error assertions to scoped `getByText(/dutch error text/i).toBeVisible()`.
- **GREEN**: 11/11 new specs passing; full Playwright run 28 passed / 2 skipped (the rate-limit specs deferred to Step 8 against `next start`).
- **Commit**: see Step 5 commit hash in git log.

### Side-quests caught during execution

- Next.js 15's [`cookies()` from `next/headers`](https://nextjs.org/docs/app/api-reference/functions/cookies) is now async (`await cookies()`); the verify page uses the awaited form.
- The TOTP input filters non-digits client-side (`replace(/\D/g, '').slice(0, 6)`) and auto-submits when length hits 6. Guarded by an `inFlightRef` so the user can't double-fire.

## What this step does NOT do

- No `middleware.ts` — Step 6
- No `/login/2fa-setup` page or `/api/auth/2fa-enable` route — Step 7
- No live-stack Playwright runs against real Directus — Step 8
- No component-tier tests (`@testing-library/react`) — Playwright covers the same behaviors and v1 is small enough that adding the jsdom tooling isn't justified
