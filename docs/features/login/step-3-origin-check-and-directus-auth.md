# Step 3: Origin check + Directus auth client

**Estimated time:** 1–2 hours
**Test layer:** Domain (pure logic) + API client (SDK-mocked)
**Risk:** Low — both modules are stateless. Origin check has zero I/O; the Directus auth client is a thin wrapper around `@directus/sdk`.
**Prerequisite:** Step 2 (rate-limit + session) — done

> TDD is mandatory — see [`.claude/testing.md`](../../../.claude/testing.md).
> This step ships the last two server-side primitives before the route handlers can be built. After this, Step 4 wires everything to `/api/auth/*`.

---

## Decision: use `@directus/sdk` (matching the README, matching programmeerprobeer)

The feature README originally committed to `@directus/sdk`. An earlier draft of this step proposed plain fetch instead — that draft was wrong and is now reversed.

Why the SDK wins for this project:

| Aspect | Plain fetch | `@directus/sdk` |
|---|---|---|
| Auth-only surface (4 endpoints) | Trivially simple, ~80 lines | One dep, slightly more setup |
| Data calls (`day_entries` + M2M `tags`, `projects`, etc.) | Tedious URL construction, fragile field-expansion strings, manual filter encoding | Typed query builder: `readItems('day_entries', { fields: ['*', 'tags.tags_id.label'], filter: {...} })` |
| Token refresh | Manual orchestration | Built-in `client.refresh()` |
| Error shape | Manually decode Directus's `{ errors: [{ extensions: { code } }] }` envelope | SDK throws typed errors |
| Bundle size | 0 | ~15 KB gzipped, server-side only |
| Match with programmeerprobeer/TVO | Diverges | Matches their proven pattern (TVO uses SDK across 20+ files) |

**Scripts dir stays plain fetch** because: dep-free constraint, no field expansion needed, batch one-shots. **Frontend uses SDK** because: Next.js already has `node_modules`, lots of data calls with M2M shapes are coming.

Pinned to `^18.0.3` to match programmeerprobeer's version.

---

## Acceptance criteria (subset of the feature README's 18 ACs)

- [ ] AC3 (partial): The Directus auth client maps invalid-credentials responses to a typed `{ ok: false, error: 'invalid_credentials' }`. The route handler will translate this to the generic "Invalid email or password" message in Step 4.
- [ ] AC2 (partial): When Directus returns the `INVALID_OTP` / `OTP_REQUIRED` shape, the client returns `{ ok: false, error: 'otp_required' }` so the route handler can branch to the verify flow.
- [ ] AC6 (partial): `loginWithOtp(email, password, otp)` completes the 2FA challenge against Directus and returns the access + refresh tokens on success.
- [ ] AC8 (partial): Same client supports the verify endpoint's needs; rate-limit enforcement happens in the route handler (Step 4), not in the client.
- [ ] AC13 (partial): `logout(refreshToken)` calls Directus to invalidate the refresh token. Idempotent: 401/404 from Directus is treated as success.
- [ ] AC8 / A08 (partial): `validateOrigin(originHeader, refererHeader, allowedOrigins)` returns `true` only when the request comes from a known origin. Same-origin requests (no Origin header) are also allowed. Strict equality — no subdomain or wildcard matching.

What this step does NOT cover (deferred):
- Mounting these primitives on `/api/auth/*` — Step 4
- Rate-limit + origin-check enforcement (the route handler composes both) — Step 4
- The `/login` UI page — Step 5
- The middleware that redirects unauthenticated requests — Step 7

## Technical constraints (this step)

- [ ] Pure server-side TS — both modules are imported only from Route Handlers and tests, never from `'use client'` components.
- [ ] Uses `@directus/sdk` ^18.0.3.
- [ ] No `localStorage` references anywhere (security-checklist A02).
- [ ] No PII in logs — failures log error code only; never the email or password.
- [ ] Functions over classes.
- [ ] Result-style returns: `{ ok: true, value } | { ok: false, error: '<typed-string>' }`.
- [ ] Configurable Directus URL via env var (`DIRECTUS_URL` — server-side only). Default falls back to `NEXT_PUBLIC_DIRECTUS_URL`, then to `http://localhost:8055` for dev.
- [ ] Stateless wrappers — `logout`/`refresh` take the refresh token as an arg (use `client.request(logout({ refresh_token }))`), not via stored SDK state. Route handlers are stateless across requests.

## Test plan

Two new test files. Both pure Vitest.

### File 1: `src/lib/auth/__tests__/origin-check.test.ts`

(Unchanged from previous draft — pure logic, no SDK involvement.)

### File 2: `src/lib/auth/__tests__/directus-auth.test.ts`

The SDK is mocked at the module boundary via `vi.mock('@directus/sdk', ...)` with hoisted mock functions. We mock:

- `createDirectus(url).with(authentication(...)).with(rest())` → returns a fake client
- `client.login(email, password, options?)` → controllable (positional args per @directus/sdk@18.0.3)
- `client.request(...)` → controllable (used for `readMe`, `logout`, `refresh`)
- The named export `readMe`, `logout`, `refresh` — return marker objects we can identify in `request` calls

Test cases (one `it` per AC slice):

- `directusLogin` success → returns `{ ok: true, value: { accessToken, refreshToken, expiresInMs } }`
- `directusLogin` OTP-required → `{ ok: false, error: 'otp_required' }`
- `directusLogin` invalid creds → `{ ok: false, error: 'invalid_credentials' }`
- `directusLogin` network failure → `{ ok: false, error: 'network_error' }`
- `directusLogin` unexpected error → `{ ok: false, error: 'directus_error' }`
- `directusLoginWithOtp` success → forwards `otp` in options object
- `directusLoginWithOtp` invalid otp → `{ ok: false, error: 'invalid_otp' }`
- `directusRefresh` success → returns fresh tokens, calls `request(refresh({ refresh_token }))`
- `directusLogout` success → calls `request(logout({ refresh_token }))`
- `directusLogout` idempotent on 401 → still returns `{ ok: true }`
- `directusGetMe` success → calls `client.request(readMe())` with token set
- `directusGetMe` invalid token → `{ ok: false, error: 'invalid_token' }`

---

## Done criteria

- [ ] Both test files exist and FAIL before implementation (RED captured)
- [ ] `src/lib/auth/origin-check.ts` exists and tests pass
- [ ] `src/lib/auth/directus-auth.ts` exists and tests pass
- [ ] Full Vitest suite still green (272 + ~20 new)
- [ ] `npm run typecheck` clean
- [ ] `npm run lint` clean
- [ ] No new HIGH gate findings

---

## Execution order

### 3.1 Baseline

No baseline — new modules.

### 3.2 RED

Both test files paste-in. Run `npm test -- origin-check directus-auth`. Must fail with `Cannot find module`.

### 3.3 GREEN

Implement:
- `src/lib/auth/origin-check.ts` — `validateOrigin(origin, referer, allowed)` → boolean.
- `src/lib/auth/directus-auth.ts` — five exported functions wrapping the SDK, all returning Result types. Reads `process.env.DIRECTUS_URL` at call time (so tests can override per-test).

### 3.4 Regression

`npm test` — all green.

### 3.5 Refactor

Likely: extract a small `Result<T, E>` type alias to `src/lib/auth/types.ts` if it starts repeating across the auth library.

### 3.6 Checkpoint commit

```
feat(auth): origin-check + Directus auth client (login step 3)
```

---

## What this step does NOT do

- No route handlers — Step 4
- No rate-limit *enforcement* — composed in the route handler
- No UI — Step 5
- No middleware — Step 7
- Auth client is **stateless** — every call creates a fresh SDK client. The stored-token features of the SDK are not used because route handlers don't share state across requests.
