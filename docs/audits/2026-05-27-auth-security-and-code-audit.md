# Auth feature — security and code audit (2026-05-27)

Comprehensive review of the login feature (steps 1–9, commits `45e356b`–`c4922e0`) plus the surrounding bootstrap (Dockerfile, fly.toml, middleware, configs). Conducted on the day the feature was deployed to `https://gevoelscore-frontend.fly.dev`.

**Scope**: everything under `src/lib/auth/`, `src/app/api/auth/`, `src/app/login/`, `src/middleware.ts`, `Dockerfile`, `fly.toml`, `next.config.ts`.

**Methodology**: Two-track. Track A: I did a higher-level review against compliance standards. Track B: an independent reviewer (general-purpose agent, fresh context) did a fine-grained line-by-line security review. Findings synthesized; cross-checked before logging.

**Verdict**: **No criticals**. Four high-severity findings worth fixing before the daily-entry feature ships. Several medium / low items worth doing as standalone hygiene work. One real architectural concern (multi-machine deploy fragility — already documented in `current-state.md`).

---

## Executive summary

| Severity | Count | Action |
|---|---|---|
| Critical | 0 | — |
| High | 4 | Fix before daily-entry feature |
| Medium | 7 | Address within a small dedicated hardening pass |
| Low | 7 | Backlog hygiene |
| Informational | 4 | Document; no immediate change |

**Top 5 to fix first** (priority order):

1. **H2** — `/api/auth/2fa/enable` accepts a client-controlled `secret`. An attacker with a valid session can plant their own TOTP secret in Directus. Bind the secret to the session server-side.
2. **H1** — 2FA-enable + 2FA-generate endpoints aren't rate-limited. Brute-force surface for password (generate) and OTP (enable). Add two new rate limiters.
3. **H4** — Rate-limit key derives from `X-Forwarded-For` first, which is appendable by clients on Fly. Use `Fly-Client-IP` first.
4. **M1** — Zero security headers in production (`Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`). The project's own checklist mandates them. Currently violated.
5. **H3** — Plaintext password held in `pendingOtpStore` for 5 minutes between login and verify. Heap-dump / swap leakage surface. Encrypt at rest or rework the flow.

---

## Section 1 — Security audit

### 1.1 Standards mapped to findings

#### OWASP Top 10 (2021)

| Category | Status | Notes / finding refs |
|---|---|---|
| A01 Broken Access Control | ⚠ Partial | Middleware gates browser nav; route handlers gate themselves. **M2**: middleware redirects `/api/*` clients to /login instead of 401-JSON. |
| A02 Cryptographic Failures | ✅ Mostly | TLS forced (`force_https`), cookies HttpOnly+Secure+SameSite=Strict, tokens never reach the browser. **H3**: plaintext password in memory between login + verify. |
| A03 Injection | ✅ | No `dangerouslySetInnerHTML`, no string-concat SQL (we go through `@directus/sdk` or `client.request` with REST commands), all body input typed-narrowed. |
| A04 Insecure Design | ⚠ Partial | Login + verify rate-limited. **H1**: 2FA endpoints are not. **M5**: no per-pending-id OTP-attempt cap. |
| A05 Security Misconfiguration | ❌ Real gap | **M1**: zero security headers. CORS on backend is locked. Source maps off in prod build. Debug routes don't exist. |
| A07 Identification & Auth Failures | ⚠ Partial | Passwords go through Directus (good — no homegrown crypto). 2FA flow has the **H2** secret-binding gap. Generic errors on login enforced. **L1**: no token-format validation before Map lookup. |
| A08 Data Integrity (CSRF) | ⚠ Partial | SameSite=Strict + Origin/Referer check on every POST. **M3**: `allowedOrigins()` is silently empty if `NEXT_PUBLIC_APP_URL` is unset in production. **M4**: header-less requests pass the origin check by design. |
| A09 Logging Failures | ✅ | No `console.log` of user PII anywhere. Directus error envelopes mapped to coarse buckets before responding. **I3**: no auth-event audit log persisted (required for NEN 7510). |
| A10 SSRF | ✅ | No user-controlled URLs reach `fetch()` server-side. The SDK targets a fixed `DIRECTUS_URL`. |

#### OWASP ASVS (curated checklist at [`.claude/security-checklist.md`](../../.claude/security-checklist.md))

The checklist has unchecked boxes. Cross-referenced status:

- **A01 Broken Access Control** — every collection requires auth: ✅ verified. Least-privilege role: ✅ `gevoelscore-frontend-api`. Static-token leaks in `NEXT_PUBLIC_*`: ✅ none.
- **A02 Cookie attrs** — verified live on the deployed app: `HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=2592000`. ✅
- **A03 Injection** — `@directus/sdk` parameterised: ✅. Zod schemas at boundaries: ⚠ none yet (no Directus data calls live; required when daily-entry lands).
- **A04 Login rate limit 5/5min**: ✅ wired and live-stack-verified (commit `86cef75`).
- **A05 CORS Directus-side**: ✅ exact match, no wildcards. **Security headers**: ❌ none configured.
- **A07 Generic error responses**: ✅ verified in route handlers + UI.
- **A08 SameSite=Strict + Origin check**: ✅ on every state-changing endpoint, including ones that don't have auth (origin check is the gate).
- **A09 No PII in logs**: ✅ no `console.log` of credentials or user content.

#### GDPR Article 9 — special category personal data (health)

The daily-entry payload (score, note, tags) is **special category data** under Article 9. Article 9(2) requires an explicit lawful basis. For a personal app where the user is also the data subject, Article 9(2)(a) "explicit consent" applies, but the data subject = data controller = author overlap doesn't auto-discharge the requirements.

- **Lawful basis recorded**: ❌ no `docs/privacy/article-9-basis.md` or equivalent recording the lawful basis. Trivial fix: write one paragraph.
- **Data minimisation**: ✅ schema is what the brief asks for; no over-collection.
- **Storage limitation**: ⚠ no retention policy documented; data lives forever in Neon by design. For single-user "this is my own data" use, indefinite is fine; record the choice.
- **Right of access / portability**: ⚠ no export endpoint yet. CSV export is on the v1 roadmap; not blocking but acknowledge.
- **Right to erasure**: ⚠ no delete-all endpoint. Same — on the roadmap.
- **Pseudonymisation / encryption**: ⚠ TLS in transit verified. At-rest: depends on Fly volume encryption + Neon's default encryption. Confirm explicitly (see **I3**).
- **Records of processing activities (Art 30)**: ❌ for sole-user processing under 250 records/sec, this is largely optional, but documenting "what's stored, where, why" is a useful artifact.

#### NEN 7510 (Dutch healthcare information security)

Most NEN 7510 controls assume institutional context. Relevant for a personal app:

- **§5.10 Cryptography** — TLS forced; at-rest depends on provider defaults. Action: confirm + document.
- **§9.4 Access control** — single-user with 2FA + least-privilege Directus role: ✅ adequate.
- **§12.4 Logging & monitoring** — ❌ no persistent auth event log. The in-memory rate-limit counters are not a substitute. Action: a `directus_auth_events` collection (timestamp, event-type, outcome, hashed IP) — even a minimal one closes this gap (see **I3**).
- **§13.1 Network security** — internal Fly Wireguard mesh between frontend and backend; TLS terminates at the edge: ✅ documented in [ADR 0003](../decisions/0003-directus-fly-infra-setup.md).
- **§16 Incident management** — ⚠ no documented response plan. Single-user app; one-paragraph "if my account is compromised, here's what I do" is enough.
- **§17 Business continuity** — Neon takes daily snapshots automatically. Quarterly restore-test recommendation in [`current-state.md`](../architecture/current-state.md) maintenance reminders.

### 1.2 Findings (synthesised)

#### High

**H1. 2FA endpoints lack rate limiting** — [`src/app/api/auth/2fa/generate/route.ts:32`](../../src/app/api/auth/2fa/generate/route.ts), [`src/app/api/auth/2fa/enable/route.ts`](../../src/app/api/auth/2fa/enable/route.ts). The generate endpoint accepts a `password` and forwards to Directus — an attacker with a stolen session cookie (or who shares the device briefly) can password-grind. The enable endpoint accepts a 6-digit OTP — brute-forceable at full request rate. **Fix**: add `tfaGenerateRateLimiter` and `tfaEnableRateLimiter` (5/5min by IP, ideally also by session id) to `stores.ts` and use them in both handlers. **[Resolved 2026-05-27 — [step-2-rate-limit-2fa.md](../features/auth-hardening/step-2-rate-limit-2fa.md)]**

**H2. `/api/auth/2fa/enable` trusts a client-supplied `secret`** — [`src/app/api/auth/2fa/enable/route.ts:43,49`](../../src/app/api/auth/2fa/enable/route.ts#L43-L49). The handler reads `body.secret` and passes it directly to `directusEnableTfa(accessToken, secret, otp)`. If a different secret is posted than the one `/2fa/generate` returned, Directus enables 2FA with the attacker-chosen secret. Result: an attacker who briefly controls a session plants their own TOTP factor, surviving the legitimate user's logout. **Fix**: stash the generated secret in a server-side `pendingTfaStore` keyed by session id when `/generate` succeeds; `/enable` looks it up and ignores the client's value. **[Resolved 2026-05-27 — [step-1-bind-tfa-secret.md](../features/auth-hardening/step-1-bind-tfa-secret.md)]**

**H3. Plaintext password retained in `pendingOtpStore` for 5 minutes** — [`src/lib/auth/pending-otp.ts:14`](../../src/lib/auth/pending-otp.ts), [`src/app/api/auth/login/route.ts:71-75`](../../src/app/api/auth/login/route.ts#L71-L75). Required by the current "user proves password once, OTP separately" UX. Surface: heap dump on the Fly VM, swap to disk, an unintentional future debug log of the store. **Fix (preferred)**: encrypt the store entry at rest with a per-process key (`crypto.subtle` AES-GCM). **Fix (cheap)**: assertion / explicit comment that this store must never be logged; rotate to null the moment verify resolves (already deleted, but a defensive overwrite is a small step).

**H4. Rate-limit IP source is client-controllable** — [`src/lib/auth/stores.ts:27-33`](../../src/lib/auth/stores.ts#L27-L33). `getClientIp()` takes the first value of `X-Forwarded-For`, then `X-Real-IP`, then `'unknown'`. Fly's edge proxy appends to XFF; an attacker can prepend their own header and rotate values per request, bypassing the 5/5min cap. **Fix**: prefer `Fly-Client-IP` (which Fly sets and the runtime can't append to), then `X-Real-IP`, fall back to the last XFF entry (not the first). Document the assumption that the app runs behind Fly's proxy. **[Resolved 2026-05-27 — [step-3-fly-client-ip.md](../features/auth-hardening/step-3-fly-client-ip.md)]**

#### Medium

**M1. Zero security headers in production** — confirmed via `curl -I https://gevoelscore-frontend.fly.dev/login`. None of CSP / HSTS / X-Content-Type-Options / Referrer-Policy / Permissions-Policy is set. The curated `.claude/security-checklist.md` A05 mandates all five. The auth flow stores nothing in JS, so a strict CSP (`default-src 'self'`) costs nothing and defangs any future XSS. **Fix**: add an async `headers()` to `next.config.ts` returning the five headers on `/(.*)`. Plus `X-Powered-By: Next.js` is reflected — disable via `poweredByHeader: false`. **[Resolved 2026-05-27 — [step-4-security-headers.md](../features/auth-hardening/step-4-security-headers.md). Live curl post-deploy confirms all 5 headers set on `https://gevoelscore-frontend.fly.dev/login` and no `X-Powered-By` reflected.]**

**M2. Middleware returns 307→/login for `/api/*` instead of 401** — [`src/middleware.ts:29`](../../src/middleware.ts). Today the matcher excludes `/api/auth/*` + `/api/health`. Future `/api/day-entries` is currently caught: unauth API call returns a redirect-to-HTML, not a 401-JSON. Breaks fetch clients silently. **Fix**: in the middleware function, branch on `pathname.startsWith('/api/')` → return `NextResponse.json({error: 'unauthenticated'}, { status: 401 })`; only redirect for browser nav.

**M3. `allowedOrigins()` is silently empty if config drifts** — every route handler. If `NEXT_PUBLIC_APP_URL` is unset in production (misconfig), the allowed list is `[]`, and `validateOrigin(null, null, [])` returns `true` (the same-origin fallback). Misconfigured deploy → CSRF protection silently off. **Fix**: throw at startup if `NEXT_PUBLIC_APP_URL` is unset in production, or hard-require at least one allowed origin in `validateOrigin`.

**M4. `validateOrigin` accepts header-less requests** — [`src/lib/auth/origin-check.ts:16`](../../src/lib/auth/origin-check.ts#L16). Header-less = no Origin AND no Referer = "trust this as same-origin." Browsers always send at least one on fetch from a page; the fallback exists for non-browser clients. Combined with **M3** it's a real failure mode. Even with M3 fixed, consider stricter: require Origin on POST, return 403 otherwise, document why.

**M5. No per-pending-id OTP attempt counter** — [`src/app/api/auth/login/verify/route.ts:69`](../../src/app/api/auth/login/verify/route.ts#L69). Wrong OTP keeps the pending cookie alive (required by AC7). Combined with IP rate-limit only, an attacker with the pending cookie can refresh and retry. **Fix**: add `attempts` to the `PendingOtpData` shape; bump on each failed OTP; invalidate at 3 → user re-logs in fully.

**M6. Logout doesn't clear cookie on origin failure** — [`src/app/api/auth/logout/route.ts:30`](../../src/app/api/auth/logout/route.ts#L30). Returns 403 with no `Set-Cookie`. Minor UX defence-in-depth: on origin mismatch, still clear the local cookie so a stuck-state user can recover. Lower priority.

**M7. `directus_error` is a catch-all that may swallow useful detail** — [`src/lib/auth/directus-auth.ts:191,215,238`](../../src/lib/auth/directus-auth.ts). Any unexpected Directus error becomes the same code. Fine for the API surface but means a future maintainer who adds `console.error(e)` for debugging will leak whatever Directus included. **Fix**: lock down to "only log `code`, never the raw `e`" — a comment + a `logError(code: string)` helper.

#### Low

- **L1. `parseSessionCookie` / `parsePendingOtpCookie` accept any non-empty value** — checklist A03 token-format validation. Should validate UUID shape before Map lookup.
- **L2. UUIDv4 has 122 bits of entropy** — ASVS 3.2.2 recommends ≥128. Switch to `crypto.randomBytes(32).toString('base64url')` for the session id generator.
- **L3. Cookie values not URL-encoded** — safe today (UUIDs only) but fragile if id format ever changes. Wrap in `encodeURIComponent`.
- **L4. Email is `.trim()`ed but not lowercased before Directus** — Directus is case-insensitive on email; functionally fine, but make the delegation explicit in a comment.
- **L5. Dockerfile has no `npm audit` gate** — supply chain checklist requires zero high/critical pre-merge. Add `RUN npm audit --audit-level=high` to the deps stage so a vulnerable lockfile fails the build.
- **L6. `.dockerignore` includes `.env*`** ✅ confirmed at line 16. Layer cache exposure is also not a concern (intermediate layers discarded).
- **L7. HSTS missing** — `force_https = true` is just the redirect. The `Strict-Transport-Security` *header* is missing (subsumed by M1).

#### Informational

**I1. Single-machine deployment is load-bearing** — `min_machines_running = 1` plus in-memory stores. The recent `fly scale count 1` was deliberate (commit `24e8a00`). Documented in [`current-state.md`](../architecture/current-state.md) "First-deploy notes". Future scaling forces a swap to a shared store (Redis or a Directus `sessions` collection); the auth library API is designed for that swap.

**I2. Refresh-token rotation doesn't re-issue the session cookie** — `getValidatedSession` updates the in-memory entry but the cookie value (session id) is stable. Means a stolen cookie remains valid until 30-day `Max-Age` regardless of refresh activity. Acceptable for a single user; revisit if multi-user.

**I3. NEN 7510 §12.4 audit log not persisted** — only the in-memory rate-limit counter records anything. **Fix when comfortable**: a `directus_auth_events` collection (timestamp, event ∈ {login_success, login_fail, otp_fail, logout, 2fa_enable}, outcome, hashed IP, session_id). Single column write per auth event; trivial. Gives an actual audit trail.

**I4. Project memory says "no source code yet"** — [`.claude/memory`](../../.claude) `MEMORY.md` claim "Pre-prototype: docs only, no source code yet" is stale. Update.

### 1.3 Deployment posture

| Check | Status |
|---|---|
| TLS forced (`force_https = true`) | ✅ |
| Cookie attrs on live response | ✅ HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=2592000 |
| CSP / HSTS / Permissions-Policy headers | ❌ (M1) |
| `X-Powered-By: Next.js` reflected | ⚠ minor info leak (fix: `poweredByHeader: false`) |
| Source maps in production | ✅ default off |
| Health endpoint reachable, no auth | ✅ |
| Fly internal network frontend ↔ backend | ✅ `DIRECTUS_URL=http://gevoelscore-backend.internal:8055` |
| Cron / scheduled tasks | none yet — N/A |
| Secrets management | ✅ all credentials in Fly secrets, `.env.local` gitignored, no `NEXT_PUBLIC_*` token leaks |

---

## Section 2 — Code audit

### 2.1 Adherence to project conventions

Cross-referenced against [`.claude/conventions.md`](../../.claude/conventions.md) + [`CLAUDE.md`](../../CLAUDE.md) "Key rules" + [`.claude/testing.md`](../../.claude/testing.md):

| Convention | Status | Notes |
|---|---|---|
| TypeScript strict + `noUncheckedIndexedAccess` | ✅ | `tsc --noEmit` clean across 351 tests |
| Filenames kebab-case | ✅ | Verified; tests in `__tests__/` |
| Tests co-located by module | ✅ | All tests in `src/**/__tests__/` |
| No telemetry deps | ✅ | `NEXT_TELEMETRY_DISABLED=1` in Dockerfile + fly.toml; 0 telemetry SDKs |
| User-facing Dutch | ✅ | All error messages, button labels, headings in NL |
| Code/comments English | ✅ | Spot-checked across auth library |
| Result-style error returns | ✅ | All 5 directus-auth wrappers return discriminated unions |
| TDD: tests before code | ✅ | Every step file's Done section records RED captured first |
| Don't add error handling for impossible scenarios | ✅ | Spot-checked — no `try/catch` around trivially-safe code |
| No comments unless WHY non-obvious | ⚠ Mostly | Some files err on the side of more-comment-than-needed in route handlers; not a bug |
| No PII in repo | ✅ | `private/` gitignored, no test fixtures contain real data |
| Architectural deps have ADRs | ✅ | `@directus/sdk` choice documented in step-3 + ADR 0002 |

### 2.2 Architecture observations

**The good:**
- Test-to-source LOC ratio: **2734 / 2242 ≈ 1.22**. Healthy for a TDD-led project. Tests outweigh source slightly — expected.
- Largest source file: [`src/lib/auth/directus-auth.ts`](../../src/lib/auth/directus-auth.ts) at 240 lines. Within bounds; cohesive (one concern: Directus SDK wrapping).
- Step files document RED/GREEN evidence + side-quests caught — high-quality TDD log.
- No `TODO` / `FIXME` / `XXX` / `HACK` comments anywhere in `src/`.
- Module boundaries clean: `auth/` library has zero `next/*` imports; the route handlers compose library + Next.js.
- Discriminated-union return types (`{ ok: true } | { ok: false }`) used consistently. TS narrows them properly.

**The DRY violations worth fixing:**

- **`allowedOrigins()` is duplicated across all 5 route handlers** (`src/app/api/auth/{login, login/verify, logout, 2fa/generate, 2fa/enable}/route.ts`). Each definition is identical (3 lines). Pulling it into `src/lib/auth/allowed-origins.ts` (one export, one source of truth) makes **M3** easier to fix once and forces the fix everywhere.

**The `as never` type laundering** ([`directus-auth.ts:147, 163, 179, 202, 227`](../../src/lib/auth/directus-auth.ts)):
- 5 instances of `as never` to bypass `@directus/sdk` typing on REST commands. This is a code smell — defeats the SDK's type system. The cause: SDK's generic `Schema` type parameter doesn't fit our use case (we never declared a typed schema). **Action**: not urgent (works fine at runtime), but when daily-entry lands and a Schema type is needed for `readItems('day_entries', ...)`, the `as never` pattern goes away naturally.

**Comment-to-code ratio in route handlers**:
- Route handlers (e.g. [`login/route.ts`](../../src/app/api/auth/login/route.ts)) carry ~20% comments. Per CLAUDE.md ("Default to writing no comments"), some of these are explaining what the code does rather than why. Not a bug, but a trim pass would tighten them.

### 2.3 Test pyramid

Test counts (`it` blocks):

| Area | Count | Notes |
|---|---|---|
| `src/lib/domain` | 79 | Score, Tag, DayEntry, Date, etc. — pure logic |
| `src/lib/import` | 21 | CSV parser |
| `src/lib/auth` | 64 | Rate-limit, session, pending-otp, origin-check, directus-auth, get-validated-session |
| `src/app/api/auth/*` route handlers | 33 | Unit-mocked Vitest |
| `tests/api/` Playwright (dev) | 13 | Real-HTTP unhappy paths |
| `tests/e2e/` Playwright (dev) | 17 | Browser navigation |
| `tests/live-stack/` Playwright | 4 | Production build + real Directus |
| **Total Vitest** | **351** | |
| **Total Playwright** | **34** (28 + 4 + 2 skipped) | |

**Pyramid shape** (target: many unit, fewer integration, very few e2e):
- Unit (domain + library): 164 — strong base
- API/route handler unit: 33 — medium layer
- API integration (Playwright dev): 13 — medium layer
- e2e browser: 17 — medium layer (overweight for what this is — half of these are 2fa-setup happy paths that could move to live-stack)
- Live-stack: 4 — apex

Shape is healthy. One observation: the 2 deferred rate-limit specs in `tests/api/auth/*` that skip in dev and run via `tests/live-stack/` is a clean pattern — keep using it.

**Coverage gaps**:
- No tests for `src/middleware.ts` directly (Edge runtime; Playwright e2e covers it via `tests/e2e/middleware.spec.ts`). Fine.
- No tests for `src/app/login/2fa-setup/setup-form.tsx` form-state machine — covered by Playwright e2e at `tests/e2e/2fa-setup.spec.ts`. Adequate.
- No Zod schemas yet (no Directus reads / writes live) — required when daily-entry lands.

### 2.4 Dependency hygiene

- **`npm audit`**: 0 critical, 0 high, **2 moderate** in `postcss` bundled inside Next.js itself. Both are upstream; `npm audit fix --force` would downgrade Next to v9 (worse). Status: monitored, awaits an upstream Next patch.
- **449 total deps** (21 prod, 394 dev, 101 optional). Reasonable for a Next+Tailwind+Playwright project. Tailwind v4's `lightningcss` brings several optional native binaries per platform — expected, used at build time only.
- **Lockfile committed**: ✅
- **No floating versions**: ✅ all caret ranges in `package.json` resolve to pinned versions in `package-lock.json`.
- **Architectural deps with ADRs**: ✅ Next.js (ADR 0002), Directus + Fly + Neon (ADR 0003), `@directus/sdk` (step-3 of login feature documents the choice).

### 2.5 What's surprisingly good

A few patterns worth keeping:
- **Step files with Done-section RED/GREEN captures** — preserves the TDD intent in the doc, not just the git log.
- **Injectable dependencies in `getValidatedSession`** — production passes nothing; tests pass a fake store + fake `now()` + fake `refresh`. Clean DI without a framework.
- **`as never` is contained to one file** — `directus-auth.ts`. The smell exists but doesn't spread.
- **Live-stack Playwright config is a separate file**, opt-in via `npm run test:live`, requires `.env.local`. Right level of friction for "real backend" tests.

---

## Section 3 — Remediation roadmap

### Priority 1 — before daily-entry feature ships (this week)

1. **H2**: Server-side bind the generated TFA secret to the session. Add `pendingTfaStore` (same shape as `pendingOtpStore`); `/2fa/generate` stashes the secret keyed by session id; `/2fa/enable` looks it up and ignores `body.secret`. Tests at both layers.
2. **H1**: Add `tfaGenerateRateLimiter` + `tfaEnableRateLimiter` to `stores.ts`; wire into both 2FA route handlers. Same 5/5min cap.
3. **H4**: Update `getClientIp` to prefer `Fly-Client-IP`, then `X-Real-IP`, then last hop of XFF. Document the deploy assumption (always behind Fly's proxy).
4. **M1**: `next.config.ts` `async headers()` block with CSP, HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy. `poweredByHeader: false`. Verify with a Playwright spec that runs `expect(headers['content-security-policy']).toBeDefined()`.

Estimated: 2–3 hours total.

### Priority 2 — small hardening pass (this month)

5. **H3**: Encrypt `pendingOtpStore` entries at rest with a per-process key (`crypto.subtle` AES-GCM). Or, simpler: tighten the comment + lifecycle, accept the residual risk.
6. **M2**: Middleware returns 401-JSON for `/api/*` instead of redirecting. Two new lines + one e2e spec.
7. **M3**: Throw at startup if `NEXT_PUBLIC_APP_URL` is unset in production. Or hard-require non-empty allowed-list in `validateOrigin`.
8. **M5**: Per-pending-id OTP attempt counter; invalidate at 3 attempts.
9. **DRY fix**: Extract `allowedOrigins()` to `src/lib/auth/allowed-origins.ts`. Removes 5 copies; M3 fix lands in one place.
10. **L5**: Add `RUN npm audit --audit-level=high` to Dockerfile deps stage.

Estimated: 2–3 hours total.

### Priority 3 — compliance + observability (this quarter)

11. **I3**: `directus_auth_events` collection (timestamp, event, outcome, hashed IP, session id). One INSERT per auth event from the route handlers. Closes the NEN 7510 §12.4 audit-log gap.
12. **GDPR Art 9 record**: one paragraph in `docs/privacy/article-9-basis.md` declaring lawful basis, data minimisation, retention, and pointing at the export / delete features (when shipped).
13. **At-rest encryption confirmation**: confirm Neon's default at-rest encryption explicitly, record in `docs/architecture/current-state.md` "Cloud resources" table. (Likely AES-256, but confirm.)
14. **Quarterly Neon restore-test**: already a maintenance reminder; add a calendar item.

### Won't do (and why)

- **L2 (UUID v4 → 32-byte random)**: cosmetic improvement; 122 bits is already past practical brute force. Defer.
- **L3 (URL-encode cookies)**: safe today; only relevant if session-id format changes. Document the invariant instead.
- **L4 (email lowercase before Directus)**: Directus handles it. Add a one-line comment.
- **L6 (.dockerignore review)**: confirmed adequate.
- **L7 (HSTS standalone)**: subsumed by M1.
- **I1 (multi-machine deploy fragility)**: already documented in `current-state.md`. Architectural; revisit at scale.
- **I2 (refresh doesn't re-issue cookie)**: acceptable for single user.

---

## Appendix A — Methodology

- **Track A** (this report, by me): standards mapping, GDPR/NEN 7510 audit, code/architecture review, test pyramid analysis, deployment posture check via `curl` against the live app.
- **Track B** (independent reviewer, `general-purpose` agent, fresh context): line-by-line security review of the 17 files in scope, ranked findings by severity.
- **Verification**: every high-severity finding from Track B was independently re-read in the actual source before being treated as a finding. H2 specifically traced through `enable/route.ts:43→49` to confirm `body.secret` reaches Directus unbound.

Both tracks largely agreed. Track B caught the H1/H2/H4 issues I would otherwise have rated lower; my own review caught the standards-mapping context (GDPR Art 9 + NEN 7510) and the architecture-level concerns (DRY, `as never`, comment density).

---

## Appendix B — What this audit deliberately does NOT cover

- The Directus backend's own security posture (assume the upstream project's hardening; verified the CORS + role + policy chain in [`current-state.md`](../architecture/current-state.md))
- Neon's database security (depends on Neon's provider hardening; trust at the same level as Fly's)
- Frontend XSS surface beyond auth (no user-content rendering live yet; revisit when daily-entry adds the note display)
- Service-worker / PWA security (PWA install not implemented yet)
- The `docs/sample-data.csv` / `private/real-history.csv` data files (one is anonymised + checked in; the other is gitignored — confirmed)
- Long-tail dependency CVEs beyond what `npm audit` reports

Revisit when daily-entry ships, when a Settings page lands, or when a second user is ever added.
