# Step 4: Auth route handlers (login + verify + logout)

**Estimated time:** 2–3 hours
**Test layer:** Route Handler (Vitest with mocked deps) + Playwright API (unhappy paths)
**Risk:** Medium — composes 4 modules from earlier steps; cookie attrs must be exactly right; OTP flow has state across two requests.
**Prerequisite:** Steps 2 + 3 (rate-limit, session, origin-check, directus-auth) — done

> TDD is mandatory. Each route handler gets both a Vitest unit test (full flow with mocked Directus + stores) and a Playwright API spec (validation, origin, rate-limit — happy-path 200s defer to Step 7 against the live stack).

---

## Acceptance criteria (subset of the feature README's 18 ACs)

`/api/auth/login`:

- [ ] AC1: Valid creds against a non-2FA account → sets session cookie, returns 200 `{ ok: true }`.
- [ ] AC2: Valid creds against a 2FA account → stashes credentials server-side, sets `gs_pending_otp` short-lived cookie, returns 200 `{ requires_otp: true }`.
- [ ] AC3: Invalid creds → returns 401 with generic `{ error: 'invalid_credentials' }`. No info about which field was wrong.
- [ ] AC5: 6th attempt in 5 min from the same IP → 429.
- [ ] A08: Cross-origin POST → 403.
- [ ] AC11: Session cookie attrs HttpOnly + Secure + SameSite=Strict + Path=/ + Max-Age verified.

`/api/auth/login/verify`:

- [ ] AC6: Valid OTP + valid pending state → session cookie set + 200 `{ ok: true }`.
- [ ] AC7: Invalid OTP → 401 with generic `{ error: 'invalid_otp' }`. Pending cookie retained for retry.
- [ ] AC8: Rate-limited at 5/5 min — separate counter from `/api/auth/login`.
- [ ] AC10: POST without a valid pending-OTP cookie → 401 (no retry counter exposure).

`/api/auth/logout`:

- [ ] AC13: With valid session cookie → calls Directus logout, clears session, clears cookie, returns 200.
- [ ] Without session cookie → returns 200 (idempotent).

## Technical constraints (this step)

- Module-singleton stores in `src/lib/auth/stores.ts` (one process per Fly machine; persistence not needed for v1).
- Pending-OTP store has its own TTL (5 min) — separate from the main session store.
- Login + verify share a credentials cache via `gs_pending_otp` cookie (httpOnly, Path=/, Max-Age=300, SameSite=Strict).
- Generic error responses — never leak which field was wrong.
- IP source: `request.headers.get('x-forwarded-for')` first, falls back to `'unknown'`. Hashed for any logs.
- Body parsing: `request.json()` wrapped in try-catch → 400 on malformed JSON.
- Validation: email must be a non-empty string with `@`; password must be a non-empty string. No deeper format check (server-side; UI does the cardinal-principle prompts).

## Plan

### 4.1 New primitive: `pending-otp.ts`

Same shape as `session.ts` but stores `{ email, password, expiresAt }`. Cookie name `gs_pending_otp`.

### 4.2 Module singletons: `stores.ts`

Barrel exporting:
- `sessionStore` (1-hour TTL — matches Directus access-token expiry)
- `pendingOtpStore` (5-minute TTL)
- `loginRateLimiter` (5/5min)
- `verifyRateLimiter` (5/5min — distinct namespace from login)
- `getClientIp(request)` helper

### 4.3 Route handlers

Each handler under `src/app/api/auth/{name}/route.ts`. Composes:
1. Origin check (returns 403 if mismatch)
2. Body parse + validate (returns 400 if bad)
3. Rate limit check (returns 429 if exceeded)
4. Directus call via `directusLogin` / `directusLoginWithOtp` / `directusLogout`
5. Side effects: create/delete session, set/clear cookies
6. Response

### 4.4 Tests

Per route:
- `src/app/api/auth/{name}/__tests__/route.test.ts` — Vitest unit test, mocks the directus-auth module and the stores. Covers happy + unhappy.
- `tests/api/auth/{name}.spec.ts` — Playwright API spec hitting the real route. Covers validation, origin, rate-limit. Happy-path 200 with cookie deferred to Step 7 (needs live Directus user).

### 4.5 Playwright webServer env

`playwright.config.ts` already starts `next dev`. Add env so the dev server in tests doesn't accidentally hit production Directus during unhappy-path tests.

---

## Done criteria

- [ ] All route handlers + tests written
- [ ] Vitest 293 + ~20 new all green
- [ ] Playwright 5 + ~10 new all green
- [ ] Typecheck + lint clean
- [ ] No new HIGH gate findings

## What this step does NOT do

- No 2FA setup UI (`/login/2fa-setup`) — Step 6
- No middleware (`middleware.ts`) — Step 7
- No login form / verify form pages — Step 5
- No live-stack happy-path Playwright — Step 7
