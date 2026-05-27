# Step 6: Middleware (protected-route gating)

**Estimated time:** 45 min
**Test layer:** Playwright e2e (real navigation against the dev server).
**Risk:** Low — one file, one cookie-presence check, well-trodden Next.js path.
**Prerequisite:** Step 5 (login + verify UI) — done.

> TDD: Playwright e2e tests RED-first, middleware file last.

---

## Acceptance criteria

- [ ] AC14: A navigation to any protected page without a `gs_session` cookie redirects to `/login`. Protected = "every page except `/login*`, `/api/auth/*`, `/api/health`, and static assets".
- [ ] With a `gs_session` cookie present (any value), the same navigation completes normally — middleware does NOT validate the cookie's value. The route handler / page does the actual session lookup when it uses the session.

## Technical constraints

- `middleware.ts` at the repo root (Next.js convention).
- Runs in Edge runtime → can import only Edge-compatible code. We re-import `SESSION_COOKIE_NAME` from `@/lib/auth/session.ts` (a string constant — Edge-safe).
- `matcher` config excludes:
  - `/login` and `/login/*` — the unauth pages themselves
  - `/api/auth/*` — auth endpoints handle their own logic
  - `/api/health` — Fly.io health probe, no auth
  - `/_next/static`, `/_next/image`, `favicon.ico` — static
- Presence-only check: `request.cookies.get(SESSION_COOKIE_NAME)?.value`. Validation lives downstream so middleware stays sub-millisecond.

## Test plan

New: `tests/e2e/middleware.spec.ts` — runs in the existing `chromium` Playwright project.

- GET `/` without cookie → redirected to `/login`.
- GET `/` with `gs_session` cookie set → page renders, no redirect.
- GET `/login` without cookie → page renders, no redirect (would loop otherwise).
- GET `/api/health` without cookie → 200 with `{ status: 'ok' }`.
- POST `/api/auth/login` without cookie → no 302 from middleware (handler returns its own status).

Update: `tests/e2e/home.spec.ts` — every test gains a `context.addCookies()` for `gs_session` before navigating, so the existing assertions still hold once middleware is in place.

---

## Done criteria

- [x] `middleware.ts` exists at `src/middleware.ts` (Next.js convention with `src/` layout — not repo root)
- [x] New middleware specs all green (5/5)
- [x] Updated home specs still green (3/3)
- [x] Existing Vitest + other Playwright suites still green (323 Vitest, 33 Playwright + 2 skipped)
- [x] `npm run typecheck` clean
- [x] `npm run lint` clean

### Captured evidence

- **RED**: middleware.spec.ts → 1 failed (the redirect test; the other 4 negative specs passed trivially because nothing was intercepting) on 2026-05-27.
- **First GREEN attempt**: middleware.ts at the repo root → didn't run. Next.js looks for middleware inside `src/` when the `src/` layout is used. Moved to `src/middleware.ts` → all middleware specs green.
- **Knock-on failures (caught by the full Playwright run)**: 3 login-flow specs began failing because their mocked `{ok: true}` responses didn't set a `gs_session` cookie; the post-success `router.push('/')` then hit middleware, no cookie present, redirect to `/login`, test timed out. Fixed by adding a `Set-Cookie` header to the mock responses (mirrors what the real route handler emits, minus `Secure` because tests run on HTTP).
- **GREEN**: full Playwright run 33 passed / 2 skipped (Step 4's deferred rate-limit specs). Vitest 323/323. Typecheck + lint clean.
- **Commit**: see Step 6 commit hash in git log.

### Side-quests caught

- Middleware location: `src/middleware.ts` not `middleware.ts`. Next.js docs say "same directory as `app` or `pages`, or inside `src/` if applicable" — and "applicable" means required when src/ is in use.
- Mock-response cookie pattern: Playwright e2e mocks of success responses must include a `Set-Cookie` header that satisfies middleware. This is now the project's pattern for any UI test that mocks a successful auth response.

## What this step does NOT do

- No `/login/2fa-setup` UI — Step 7
- No live-stack Playwright — Step 8
- No server-side session-value validation in middleware — that lives in route handlers; middleware is presence-only by design (fast path, Edge-safe)
