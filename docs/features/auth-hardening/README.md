# Auth hardening (Priority 1 — pre-daily-entry)

**Feature:** Close the 4 highest-severity findings from the 2026-05-27 security audit before the daily-entry feature lands on top of the auth layer.
**Version:** v1 (patch)
**Status:** Priority 1 + 2 shipped 2026-05-27 — 10 steps done (H1/H2/H4/M1 + DRY/M3/M2/M5/H3/L5). 380/380 Vitest, all live + e2e regression green.
**Parent docs:** [audit](../../audits/2026-05-27-auth-security-and-code-audit.md), [remediation plan](../../plans/2026-05-27-audit-remediation-and-standards-enforcement.md), [security-checklist](../../../.claude/security-checklist.md)

---

## Why this feature exists

The login feature shipped working. The follow-on audit found four high-severity issues that all sit on the auth surface. None are critical in isolation but together they're the kind of cluster you fix as one pass while the auth code is still warm in head — not three months later mixed into a daily-entry PR.

The four findings:

- **H1** — `/api/auth/2fa/{generate,enable}` are not rate-limited. Brute-force surface for password (generate) and 6-digit OTP (enable).
- **H2** — `/api/auth/2fa/enable` trusts a client-supplied `secret`. An attacker with a valid session can plant their own TOTP secret in Directus, surviving the legitimate user's logout.
- **H4** — `getClientIp()` prefers the first hop of `X-Forwarded-For`, which clients on Fly can prepend to. Rate-limit bypass.
- **M1** — Zero security response headers in production. The project's own checklist mandates five (CSP / HSTS / X-Content-Type-Options / Referrer-Policy / Permissions-Policy).

## Acceptance criteria

**H2 — server-side TFA-secret binding:**

- [ ] AC1: `POST /api/auth/2fa/generate` stashes the freshly-generated secret in a server-side `pendingTfaStore` keyed by session id; returns the secret + otpauth_url to the user as today.
- [ ] AC2: `POST /api/auth/2fa/enable` looks up the secret from the store using the session id; the request body no longer carries `secret`. A client posting `secret` in the body has it ignored.
- [ ] AC3: If no pending TFA entry exists for the session (e.g. `enable` called without `generate`), the request returns 400 `invalid_request`.
- [ ] AC4: On successful enable, the pending entry is deleted from the store.
- [ ] AC5: The pending entry has a TTL (10 minutes); requests past TTL return 400 `invalid_request` and the entry is evicted.

**H1 — 2FA endpoint rate limits:**

- [ ] AC6: `/api/auth/2fa/generate` is rate-limited at 5 attempts / 5 minutes per IP. 6th attempt returns 429.
- [ ] AC7: `/api/auth/2fa/enable` is rate-limited at 5 attempts / 5 minutes per IP. 6th attempt returns 429.
- [ ] AC8: Both limits are tracked by separate buckets (a user spamming `generate` doesn't burn through `enable`'s budget).

**H4 — IP source hardening:**

- [ ] AC9: `getClientIp(request)` prefers `Fly-Client-IP`, then `X-Real-IP`, then the **last** hop of `X-Forwarded-For`, then `'unknown'`.
- [ ] AC10: A client that prepends its own values to `X-Forwarded-For` does not change the rate-limit bucket (covered by unit test + live-stack proxy mock).

**M1 — Security response headers:**

- [ ] AC11: Every response from the production build carries `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` (camera/microphone/geolocation denied).
- [ ] AC12: `X-Powered-By` header is not reflected (`poweredByHeader: false` in `next.config.ts`).
- [ ] AC13: CSP is `default-src 'self'`; `script-src 'self' 'unsafe-inline'` (Next inlines hydration bootstrap script tags) — review-allowed list, no third-party origins.
- [ ] AC14: A new Playwright spec in `tests/live-stack/security-headers.spec.ts` asserts all five headers are present on `/login` and `/api/health`.

## Technical constraints

- No new runtime deps. `pendingTfaStore` mirrors `pendingOtpStore`'s shape.
- Module-singleton store, same single-process Fly machine assumption as the existing stores. Migration path documented but not implemented.
- Rate limiters reuse the existing `createRateLimiter` factory.
- Live-stack header verification must pass against the actual deployed Fly app — no asserting on dev-mode responses, where Next strips some headers.
- Per audit H4 description: the deploy assumption is "the app always runs behind Fly's proxy." Document this in [`current-state.md`](../../architecture/current-state.md) "Cloud resources" notes as part of Step 3.

## Steps

**Priority 1 (closed):**
1. **[Step 1 — Bind TFA secret server-side](step-1-bind-tfa-secret.md)** — H2 (AC1–AC5). ✅
2. **[Step 2 — 2FA endpoint rate limits](step-2-rate-limit-2fa.md)** — H1 (AC6–AC8). ✅
3. **[Step 3 — Trust Fly-Client-IP over XFF](step-3-fly-client-ip.md)** — H4 (AC9–AC10). ✅
4. **[Step 4 — Security response headers](step-4-security-headers.md)** — M1 (AC11–AC14). ✅

**Priority 2 (closed):**
5. **[Step 5 — Extract `allowedOrigins()` to shared util](step-5-extract-allowed-origins.md)** — DRY. ✅
6. **[Step 6 — Hard-require allowed origins in production](step-6-hard-require-origins.md)** — M3. ✅
7. **[Step 7 — API-aware middleware](step-7-api-aware-middleware.md)** — M2. ✅
8. **[Step 8 — Per-pending-id OTP attempt counter](step-8-otp-attempt-counter.md)** — M5. ✅
9. **[Step 9 — Pending-OTP password lifecycle hardening (cheap H3)](step-9-pending-otp-password-lifecycle.md)** — H3. ✅
10. **[Step 10 — Dockerfile `npm audit` gate](step-10-dockerfile-audit-gate.md)** — L5. ✅

Each step follows the strict RED → GREEN → REFACTOR loop with its own Done section.

## Verification

- Vitest count grows: 351 → ~370 by end of Step 4.
- Live-stack: 4/4 → 5/5 (Step 4 adds the security-headers spec).
- `curl -I https://gevoelscore-frontend.fly.dev/login` after deploy shows all 5 security headers + no `X-Powered-By`.
- Audit findings H1, H2, H4, M1 each get a `[Resolved: Step N]` marker appended to the audit doc.

## What this feature does NOT do

- Does not address H3 (plaintext password in `pendingOtpStore` for 5 minutes) — Priority 2.
- Does not extract `allowedOrigins()` into a shared util (Priority 2 DRY fix).
- Does not introduce CI / pre-commit hooks — that's Track B of the remediation plan, separate work.
- Does not change Directus role permissions, the Directus CORS config, or anything backend-side.
