# Step 7: /login/2fa-setup UI + 2FA route handlers

**Estimated time:** 2 hours
**Test layer:** Vitest unit (SDK + stores mocked) + Playwright e2e (mocked fetches).
**Risk:** Medium — two-step flow with state across requests, plus the SDK's three-call TFA flow.
**Prerequisite:** Steps 2–6 done.

> TDD: every test file RED-first.

---

## Acceptance criteria (subset of feature README's 18 ACs)

- [ ] AC16: `/login/2fa-setup` page shows the TOTP secret string + otpauth URL + a verification input.
- [ ] AC17: After entering a valid 6-digit verifying code, 2FA is activated on the user's Directus account.
- [ ] AC17.2: An invalid code shows a generic Dutch error and lets the user retry without re-entering the password.
- [ ] AC15 (partial): The page is reachable when authenticated. Direct navigation without a `gs_session` cookie redirects to `/login`. A nav link from a Settings page is deferred until the Settings feature lands.

### Deferred (out of scope for this step)

- AC18: "If 2FA is already active, the page shows the current state + a regenerate button (with confirmation)." Would require a "get current TFA state" query that the SDK doesn't expose cleanly, plus a `disableTwoFactor → re-enable` flow. Add when needed.
- QR code image rendering. The page shows the secret + otpauth URL as plain text — paste into 1Password / type into Google Authenticator. Adding a QR image needs a dep (~50KB) and isn't strictly required for the flow to work.

## Technical constraints

- New SDK wrappers in `src/lib/auth/directus-auth.ts`:
  - `directusGenerateTfaSecret(accessToken, password)` → Result<{ secret, otpauthUrl }, error>
  - `directusEnableTfa(accessToken, secret, otp)` → Result<void, error>
  - Both use the SDK's REST commands (`generateTwoFactorSecret`, `enableTwoFactor`) via `client.request(...)` with `setToken(accessToken)`.
- Two routes split for clarity (one POST each):
  - `POST /api/auth/2fa/generate` — body `{ password }` → 200 with `{ secret, otpauth_url }` or 401.
  - `POST /api/auth/2fa/enable` — body `{ secret, otp }` → 200 with `{ ok: true }` or 401.
- Both routes require a valid `gs_session` cookie. Validation is server-side: parse cookie → look up in `sessionStore` → use the access token. If cookie is missing or session not found, return 401.
- Origin check applies on both routes (A08).
- No new rate limiter for v1 — these endpoints are post-auth and behind 2FA already; abuse is low-risk for a single-user app. If multi-user lands, add one.
- UI page split: `page.tsx` is a server component that checks the session cookie and redirects to `/login` if absent; the form is a `'use client'` component.
- All Dutch UI text. Generic error messages — no Directus error codes leak.

## Test plan

### `src/lib/auth/__tests__/directus-auth.test.ts` (extended)

Add a `describe` for `directusGenerateTfaSecret` and one for `directusEnableTfa`. Each:
- Success path — returns expected shape.
- Invalid password / invalid OTP → typed error.
- Network failure → `network_error`.

### `src/app/api/auth/2fa/generate/__tests__/route.test.ts`

- 200 with valid session + correct password → returns `{ secret, otpauth_url }`.
- 401 when no session cookie.
- 401 when session cookie present but no server-side state.
- 401 when password rejected by Directus.
- 403 on cross-origin.
- 400 on missing password.

### `src/app/api/auth/2fa/enable/__tests__/route.test.ts`

Same shape, for enable: success, missing session, invalid OTP, etc.

### `tests/api/auth/2fa.spec.ts` (Playwright unhappy)

- POST /api/auth/2fa/generate without session → 401.
- POST /api/auth/2fa/enable without session → 401.
- 403 on cross-origin for both.

### `tests/e2e/2fa-setup.spec.ts`

- `/login/2fa-setup` without session → redirects to /login.
- With session: page shows password input. Submit valid password (mocked) → page shows secret + otpauth URL + OTP input. Submit valid OTP (mocked) → success state + auto-redirect to /. Submit invalid OTP (mocked) → error message + OTP input cleared.

---

## Done criteria

- [x] All new files exist + tests green
- [x] No regressions: Vitest 342/342 (323 → 342, +19), Playwright 45 passed / 2 skipped
- [x] Typecheck + lint clean
- [x] Documented deferrals (AC18, QR rendering, AC15 Settings link) acknowledged

### Captured evidence

- **RED → GREEN at each layer**:
  - `npm test -- directus-auth` → 19 passing (12 + 7 new TFA cases).
  - `npm test -- "2fa"` → 12 passing (route handler unit tests).
  - `npm run test:e2e` → 45 passing / 2 skipped (including 6 new 2fa-setup e2e specs and 6 new 2fa API specs).
- **No knock-on failures** — the Vitest + Playwright suites were stable through the whole step.
- **Commit**: see Step 7 commit hash in git log.

## What this step does NOT do

- No QR-code image rendering
- No "already enabled / regenerate" UX (AC18)
- No Settings page link to 2fa-setup (AC15's nav part)
- No live-stack integration test — that's Step 8
