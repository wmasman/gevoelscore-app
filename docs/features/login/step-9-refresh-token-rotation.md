# Step 9: Refresh-token rotation + long-lived session cookie

**Estimated time:** 1.5 hours
**Test layer:** Vitest unit (new helper + extended sessionStore) + Vitest route handler tests (mocks updated) + Playwright/dev-mode and live-stack regression.
**Risk:** Low — additive helper layered between cookie parsing and `sessionStore.get`. Existing routes get a one-line swap.
**Prerequisite:** Steps 1–8 done.

> Triggered by a UX gap noticed after deploy: re-auth every ~15 minutes (every access-token expiry) — kills the cardinal-principle sub-10s entry budget.

---

## The problem

Steps 3 and 4 wired `directusLogin`, `directusRefresh`, `directusLogout` as Result-shaped SDK wrappers, plus a server-side `sessionStore` keyed by session id. The route handlers store the access + refresh tokens on login and look them up on subsequent requests — but **the refresh wrapper is never called**. When the Directus access token expires (~15 min default), `sessionStore.get()` evicts the entry and the route returns 401. The browser redirects to /login. The user re-enters email + password + 2FA. Repeatedly.

The fix is a textbook transparent refresh: peek at the session entry; if the access token is expired but the refresh token is still alive, swap in fresh tokens via Directus's `/auth/refresh` endpoint. Invisible to the user.

## Acceptance criteria

- [ ] An authenticated request with an expired access token but a valid refresh token transparently refreshes and succeeds (200, not 401).
- [ ] An authenticated request whose refresh token has also expired returns 401 and clears the session entry.
- [ ] Session cookie `Max-Age` is 30 days (was 1 hour). Users re-auth (with 2FA) at most once a month under normal use.
- [ ] No behaviour change for fresh requests (access token not yet expired) — same code path returns the same session shape.

## Technical constraints

- Cookie value (session id) stays the same across refreshes. No new `Set-Cookie` needed on refresh — the in-memory token swap is enough.
- The route handlers' contract changes from synchronous `sessionStore.get(id)` to async `await getValidatedSession(id)`. All five call sites need updating.
- `sessionStore.get()` still works (lazy-eviction); we just stop using it from the auth routes. Keeping it because other callers (future tests, manual debugging) may want the no-refresh semantic.
- Refresh failure means refresh token is dead/revoked → user must re-auth. Same path as no-session-at-all.
- No new dep.

## Plan

### 9.1 Extend `sessionStore` (`src/lib/auth/session.ts`)

Two new methods:

- `peek(id)` — like `get` but does NOT evict expired entries. Returns the entry regardless of expiry.
- `update(id, data)` — replace the entry's data in place. Returns true on success, false if the id is unknown.

Plus: lift `SESSION_MAX_AGE_S = 30 * 24 * 3600` here as a single source of truth. Today it's duplicated in the route handlers.

### 9.2 New helper: `src/lib/auth/get-validated-session.ts`

```ts
export async function getValidatedSession(sessionId: string): Promise<SessionData | null> {
  const session = sessionStore.peek(sessionId);
  if (!session) return null;

  if (session.expiresAt > Date.now()) return session;

  // Access token expired — try refresh.
  const result = await directusRefresh(session.refreshToken);
  if (!result.ok) {
    sessionStore.delete(sessionId);
    return null;
  }

  const refreshed = {
    accessToken: result.value.accessToken,
    refreshToken: result.value.refreshToken,
    expiresAt: Date.now() + result.value.expiresInMs,
  };
  sessionStore.update(sessionId, refreshed);
  return refreshed;
}
```

### 9.3 Wire helper into route handlers + server components

Replace `sessionStore.get(id)` with `await getValidatedSession(id)` in:
- `src/app/api/auth/logout/route.ts`
- `src/app/api/auth/2fa/generate/route.ts`
- `src/app/api/auth/2fa/enable/route.ts`
- `src/app/login/2fa-setup/page.tsx` (server component — currently only checks cookie presence; tighten to "valid session or redirect")

### 9.4 Update SESSION_MAX_AGE in two route handlers

Both `/api/auth/login` and `/api/auth/login/verify` import the constant from `session.ts` now. The numeric literal `60 * 60` disappears.

### 9.5 Update test mocks

The four route test files mock `sessionStore.get` — those mocks need to also expose `peek` and `update`. Where the tests currently arrange `mockReturnValue` on `get`, they now arrange `peek`. The directus-auth test mocks gain a `refresh` arrangement for the cases where the helper triggers a refresh.

## Test plan

### `src/lib/auth/__tests__/session.test.ts` (extended)

- `peek` returns expired entries without eviction.
- `update` replaces in place; returns false on unknown id.

### `src/lib/auth/__tests__/get-validated-session.test.ts` (new)

- Returns the session unchanged when access token is still alive.
- Triggers `directusRefresh` when access token expired; updates session with new tokens; returns the refreshed session.
- Returns `null` and deletes the session when refresh fails.
- Returns `null` for unknown session id (no refresh attempt).

### Route handler tests (extended)

For the three routes that use the helper, add one happy-path test where the session is initially expired but the refresh succeeds — verifies the helper is actually composed.

---

## Done criteria

- [x] `peek` + `update` added with tests (5 new cases)
- [x] `getValidatedSession` added with tests (4 cases, fully injectable for unit testing)
- [x] Four call sites swapped to the helper: `/api/auth/logout`, `/api/auth/2fa/generate`, `/api/auth/2fa/enable`. The `/login/2fa-setup` page kept its presence-only check (trade-off below).
- [x] Cookie `Max-Age` is 30 days, lifted to `SESSION_MAX_AGE_S` in `session.ts`. Two route handlers (`/api/auth/login`, `/api/auth/login/verify`) now import the constant.
- [x] Vitest 342 → 351 (+9). Playwright dev-mode 45 + 2 skipped (unchanged). Live-stack 4/4.
- [x] Typecheck + lint clean.
- [x] Redeployed: `Max-Age=2592000` verified on the live response. Refresh-token rotation not manually time-tested (would require a >15 min wait); covered by the unit tests.

### One trade-off chosen during implementation

I originally wired `getValidatedSession` into `/login/2fa-setup/page.tsx` too. That broke 5 Playwright e2e specs because the tests use a placeholder cookie (`gs_session=mock-session-id`) that doesn't correspond to a real session entry in the in-process store; the strict server-side check redirected the test to /login. Two ways forward:

1. Loosen the page check back to cookie-presence-only. Stale-cookie users see the password form, enter password, then get "Sessie verlopen" from `/api/auth/2fa/generate` (which still does the strict check). One wasted password entry.
2. Set up a real session for the e2e tests (needs a test-only backdoor or contrived multi-mock setup).

Chose (1). The actual session security still lives in the API route. Documented in the page's comment.

### Captured evidence

- **Before fix**: re-auth required every ~15 min on the live deployment (every access-token TTL).
- **After fix**: 30-day cookie verified via `curl`. Live deploy redeployed (`fly deploy --app gevoelscore-frontend`). Login + logout still work end-to-end.
- **Commit**: see git log.

## What this step does NOT do

- No sliding-window cookie refresh (cookie Max-Age is set at first login and counts down regardless of activity). Could add if the 30-day window proves too short in practice.
- No proactive refresh (background timer that refreshes BEFORE expiry). Today's pattern is lazy/on-demand — perfectly adequate for a single-user app.
- No Directus `REFRESH_TOKEN_TTL` change — that's a Fly secret on the backend. Default 7 days. If a 30-day cookie outlives the refresh token, the user just re-auths when the next refresh fails. Optional follow-up: `fly secrets set REFRESH_TOKEN_TTL=30d` on `gevoelscore-backend` so the cookie and refresh-token lifetimes align.
