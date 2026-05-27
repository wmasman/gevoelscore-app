# Login + 2FA flow

**Feature:** Email + password login with mandatory TOTP 2FA. Establishes an `httpOnly` session cookie that all subsequent Directus calls use.
**Version:** v1
**Status:** ✅ Shipped 2026-05-27 — all 8 steps done. Frontend-app Directus user created, 4/4 live-stack Playwright specs green against `gevoelscore-backend.fly.dev`.
**Parent doc:** [REQUIREMENTS.md "Auth"](../../REQUIREMENTS.md), [security-checklist](../../../.claude/security-checklist.md), [ADR 0002](../../decisions/0002-pwa-with-directus-backend.md), [ADR 0003](../../decisions/0003-directus-fly-infra-setup.md)

---

## Prerequisites (not part of this feature)

These must be in place before this feature can be implemented:

1. **Next.js 15 app exists** in the repo root (App Router, TS strict). `pnpm create next-app` or equivalent. Adds dependencies: `next`, `react`, `react-dom`, `@directus/sdk`. **Do this in a separate session at the terminal** — it's a real dep-tree commitment.
2. **Directus is deployed** per [directus-setup.md](../../architecture/directus-setup.md) Phases 1–4.
3. **The frontend's user account exists** in Directus — an account with role `gevoelscore-frontend-api`, 2FA enabled. This is the account YOU log in with. Created via Directus admin UI by you, the admin.
4. **Both Fly.io apps are running** and the frontend can reach `gevoelscore-backend.internal:8055`.

Until all four are true, this feature stays in `Planning` status.

---

## Overview

- **What:** Two screens (`/login`, `/login/verify`) + one Route Handler (`/api/auth/login`) that handles the Directus login flow including the 2FA second factor. Plus a one-time `/login/2fa-setup` screen for first-time TOTP pairing.
- **Why:** Per REQUIREMENTS.md, every visit to the app starts behind a login gate with 2FA. No anonymous read of any user data.
- **Impact:** Unlocks every other v1 screen. Until login works, the daily-entry screen has nothing to fetch.

## User need

The user opens the PWA on their phone. They tap "Log in," type their email + password (browser autofill works), and on success see a TOTP prompt. They tap to their authenticator app, copy the 6-digit code, paste/type it, and land on the Daily screen. Total target: ≤ 5 seconds combined (the daily screen still has to hit its ≤ 10-second budget on top, but login is outside that budget per REQUIREMENTS.md "Auth").

## Acceptance criteria

**`/login` screen + `POST /api/auth/login`:**

- [ ] AC1: Submitting valid email + password (no 2FA required on the account) sets an `httpOnly` session cookie and redirects to `/`.
- [ ] AC2: Submitting valid email + password against a 2FA-enabled account returns a `requires_otp` response; the UI navigates to `/login/verify`.
- [ ] AC3: Submitting invalid credentials shows a generic error message ("Invalid email or password"). No information about whether the email exists, whether the password was wrong, or whether 2FA was needed — per [security-checklist A07](../../../.claude/security-checklist.md).
- [ ] AC4: The login form has the cardinal-principle sub-10s target — autofocus on the email field, browser autofill enabled, submit on Enter, large primary button.
- [ ] AC5: Failed login is rate-limited at 5 attempts per 5 minutes per IP. The 6th attempt within 5 minutes returns 429 with a user-facing "Too many attempts" message.

**`/login/verify` screen + `POST /api/auth/login/verify`:**

- [ ] AC6: Entering a valid TOTP code completes login: sets the session cookie, redirects to `/`.
- [ ] AC7: Entering an invalid TOTP code shows a generic error ("Invalid code"). No retry counter visible to the user.
- [ ] AC8: TOTP verification is also rate-limited (5 attempts per 5 minutes).
- [ ] AC9: The TOTP input is `inputmode="numeric"` for mobile keyboards, accepts 6 digits, auto-submits when 6 digits are entered (no extra Submit tap).
- [ ] AC10: Returning to `/login/verify` directly (without first hitting `/login`) redirects to `/login` — no partial-state leaks.

**Session + cookie management:**

- [ ] AC11: The session cookie is `httpOnly`, `Secure`, `SameSite=Strict`, with `Max-Age` matching Directus's refresh-token expiry.
- [ ] AC12: All subsequent API calls from the browser to `/api/*` automatically include the cookie. The Route Handler uses the cookie to look up the Directus access token (stored server-side in memory or in a Directus session). Browser JS never touches the access token.
- [ ] AC13: `POST /api/auth/logout` clears the cookie and invalidates the Directus refresh token.
- [ ] AC14: A request to a protected route without a valid session redirects to `/login`. Tested via middleware on every page except `/login`, `/login/verify`, `/login/2fa-setup`.

**`/login/2fa-setup` screen (one-time for new devices, or as 2FA bootstrap):**

- [ ] AC15: Authenticated user can reach `/login/2fa-setup` from Settings → 2FA Management.
- [ ] AC16: The page shows the TOTP QR code + manual secret string + a verification input.
- [ ] AC17: After scanning + entering a verifying code, 2FA is activated on the account.
- [ ] AC18: If 2FA is already active, the page shows the current state + a "regenerate" button (with confirmation).

---

## Technical constraints

- **No client-side OAuth library.** Direct calls to Directus via `@directus/sdk` from Route Handlers only. Browser JS never sees the Directus URL or token.
- **`SameSite=Strict` + Origin check** for CSRF protection per [security-checklist A08](../../../.claude/security-checklist.md). No double-submit token plumbing.
- **CORS already locked** at the Directus side per the runbook — frontend origin only.
- **No PII in logs.** Failed-login logs include rate-limit hit count and IP (hashed) but never the email tried.
- **Rate limit store:** in-memory `Map<ip, { count, resetAt }>`, cleaned up every 5 min. Single-process Fly machine (`min_machines_running = 1`) makes this fine; if scaled later, move to Directus collection or Redis.

## Test plan

| File | Cases (one per `it`) |
|------|----------------------|
| `src/lib/auth/__tests__/login-flow.test.ts` | AC3 (generic error), AC5 (rate limit), AC11 (cookie attrs), AC13 (logout invalidation), AC14 (middleware redirect). Server-side logic tested against a mocked Directus SDK. |
| `src/lib/auth/__tests__/totp-flow.test.ts` | AC6 (valid OTP), AC7 (invalid OTP), AC8 (rate limit), AC10 (no direct entry). |
| `e2e/login.spec.ts` (Playwright, deferred until Next.js + Directus actually run) | AC1, AC2, AC4 (form behavior), AC9 (mobile TOTP input), AC15–AC18 (2FA setup flow). |

Server-side logic is unit-tested with `@directus/sdk` mocked at the module boundary. UI/browser behavior is e2e-tested with Playwright against a running stack (Phase 5 deliverable, not v1's first cut).

## Cardinal-principle impact

| Principle | Impact | How we stay inside |
|-----------|--------|--------------------|
| One-tap entry | Login is the gate — happens before any daily-entry tap. Out-of-flow but slow login still kills the experience. | ≤ 5s budget for login + 2FA; autofill enabled; auto-submit on 6 digits |
| Sub-10-second flow | Independent budget — login doesn't count against the daily ≤ 10s | Each screen ≤ 2.5s |
| Brainfog-friendly | TOTP input is the friction point on a brainfog day | Large touch targets; numeric keyboard; auto-submit; no retry counter shown |
| No notifications / ads / analytics | N/A | No telemetry deps; no PostHog |
| User-owned data | Auth goes to the author's own Directus | Cookie scoped to the frontend origin |
| Export / delete still works | Logout doesn't touch user data; just kills the session | |

## Alternatives considered

### Decision: TOTP via Directus built-in (vs. WebAuthn / passkey / email-OTP)

Per ADR 0002 + REQUIREMENTS.md. Settled. Not re-litigated here.

### Decision: `SameSite=Strict` cookie + Origin check (vs. double-submit CSRF token)

Per [security-checklist](../../../.claude/security-checklist.md). Frontend and backend are on different Fly origins (different subdomains of `*.fly.dev`); `SameSite=Strict` blocks cross-site cookies; server-side `Origin` header check is the second factor. Simpler than double-submit token plumbing — no token endpoint, no `fetchWithCsrf` wrapper.

### Decision: Session cookie storing Directus token (vs. server-side session map)

- **Chose:** Store an encrypted/signed reference in the cookie; resolve to Directus access token server-side via a short-lived in-memory map keyed by a session ID. The cookie carries only the session ID.
- **Considered and rejected:** Store the access token directly in the cookie. Simpler but expands the secret-leak blast radius if the cookie ever leaks.
- **Migration path:** if the in-memory map becomes a problem (multi-machine scaling), replace with a Directus `sessions` collection — same key, same API.

## Privacy & permissions

- **Cookie**: `httpOnly`, `Secure`, `SameSite=Strict`, scoped to the frontend origin only.
- **Email and password**: posted from the form to `/api/auth/login` over TLS. Never logged.
- **TOTP secret**: never leaves Directus's server.
- **Logout**: clears cookie + calls Directus refresh-token invalidation. Server-side session map entry removed.
- **Delete account**: out of scope for v1 — there's only one user. If needed: drop the user row in Directus admin, also `fly secrets unset` anything user-specific.

## Security

The hard rules from the security checklist that this feature ESPECIALLY must respect:

- A01: every page except `/login*` redirects through middleware to `/login` if no valid session.
- A02: tokens never in `localStorage`. Period.
- A05: error responses are generic. No stack traces. No "user not found" leaks.
- A07: rate-limit 5/5min on both login endpoints.
- A08: SameSite=Strict + Origin check on every state-changing request.
- A09: no PII in logs. IP is hashed if logged at all.

## v1.5 / v2 readiness

- The session-cookie design carries forward unchanged when a v2 native iOS app is added (per ADR 0002): the iOS app uses the same Directus auth flow but stores tokens in iOS Keychain instead of cookies.
- "Forgot password" flow: deliberately omitted in v1 (single user, admin can reset via Directus UI). When added later, it joins the `/login` family of routes and follows the same rate-limit pattern.

## Architecture

```
src/
  app/
    login/
      page.tsx               — email + password form, posts to /api/auth/login
      verify/
        page.tsx             — TOTP form, posts to /api/auth/login/verify
      2fa-setup/
        page.tsx             — TOTP QR + verifying input, posts to /api/auth/2fa-enable
      layout.tsx             — minimal layout (no nav chrome on login)
    api/
      auth/
        login/
          route.ts           — POST: proxies to Directus.login(); handles INVALID_OTP_REQUIRED
        login/verify/
          route.ts           — POST: completes login with OTP
        logout/
          route.ts           — POST: clears cookie + Directus refresh-token invalidate
        2fa-enable/
          route.ts           — POST: enables TOTP on the current user
        2fa-qr/
          route.ts           — GET: returns the QR (or secret) for the current user
  lib/
    auth/
      directus-client.ts     — module-scoped Directus SDK instance (server-only)
      session.ts             — session-id ↔ access-token map; cookie helpers
      rate-limit.ts          — in-memory IP rate limiter
      origin-check.ts        — middleware-friendly Origin/Referer validator
      __tests__/
        login-flow.test.ts
        totp-flow.test.ts
        session.test.ts
        rate-limit.test.ts
        origin-check.test.ts
  middleware.ts              — Next.js middleware: redirects unauthenticated requests to /login
```

## Steps

The original plan bundled "server-side auth library" into a single Step 2. During execution it split into two cleaner TDD-sized chunks (rate-limit + session, then origin-check + Directus client). Numbering below reflects what was actually shipped — the step files in this folder are the source of truth.

1. **Step 1**: Next.js bootstrap — Next 15 + React 19 + Tailwind v4 + Playwright + ESLint flat config. Closed-loop test setup (Vitest + Playwright API + Playwright e2e). Commit `45e356b`. **Done 2026-05-27.**
2. **Step 2**: [Rate-limit + session map](step-2-rate-limit-and-session.md) — `src/lib/auth/rate-limit.ts` + `session.ts`, both injectable-clock for deterministic tests. ~18 ACs partially covered (AC5, AC8, AC11, AC12, AC13). Commit `5ddd622`. **Done 2026-05-27.**
3. **Step 3**: [Origin check + Directus auth client](step-3-origin-check-and-directus-auth.md) — `origin-check.ts` (CSRF defence A08) + `directus-auth.ts` (wraps `@directus/sdk@18.0.3`, Result-shaped). Includes the explicit decision to use the SDK over plain fetch. Commit `94c1a3d`. **Done 2026-05-27.**
4. **Step 4**: [Login + verify + logout route handlers](step-4-auth-route-handlers.md) — `src/app/api/auth/{login, login/verify, logout}/route.ts`, plus `pending-otp.ts` for stashing creds between login and verify, plus `stores.ts` barrel for module-singletons. Vitest unit tests + Playwright API specs. ~10 ACs covered (AC1–AC3, AC5–AC8, AC10, AC11, AC13). Commit `dbf59e5`. **Done 2026-05-27.**
5. **Step 5**: `/login` and `/login/verify` UI pages — forms that POST to the Step 4 routes. Component-level tests + Playwright e2e for form behavior. Covers AC4 (autofocus, autofill, large primary button), AC9 (mobile TOTP input). **Next up.**
6. **Step 6**: Middleware (`middleware.ts`) — protects every page except `/login*`. Covers AC14.
7. **Step 7**: [/login/2fa-setup UI + 2FA route handlers](step-7-2fa-setup.md) — `directusGenerateTfaSecret` + `directusEnableTfa` SDK wrappers, two-phase setup UI (password → secret reveal + OTP input). Commit `f86ade3`. **Done 2026-05-27.**
8. **Step 8**: [Live-stack Playwright](step-8-live-stack-playwright.md) — production build (`next start`) + real `gevoelscore-backend.fly.dev`. Unskipped the 2 rate-limit specs; validated AC1/AC2/AC3/AC5/AC8 against real Directus envelopes. Commit hash in git log. **Done 2026-05-27.**

Each step file follows the TDD template and records its own RED/GREEN evidence in a `Done` section.

## Verification

- Automated: unit tests + Playwright e2e
- Manual: walk the actual login flow on Safari iOS (the primary daily-driver context). Stopwatch login + 2FA combined ≤ 5s.
- Security: walk the [security-checklist A01/A05/A07/A08/A09 sections](../../../.claude/security-checklist.md) line by line against the implemented routes.

## What this feature does NOT do

- Does NOT install Next.js — that's a prerequisite, done at the terminal.
- Does NOT provision Directus or the user account — that's the runbook.
- Does NOT implement a forgot-password flow (deferred to "if ever needed").
- Does NOT implement registration (single-user app — admin creates accounts via Directus UI).
- Does NOT implement social login (Google, GitHub, etc.) — out of scope.
