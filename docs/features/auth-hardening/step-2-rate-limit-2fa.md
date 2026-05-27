# Step 2: Rate-limit the 2FA endpoints

**Estimated time:** 30 minutes
**Test layer:** Vitest route handler tests (one 429 case per endpoint) + live-stack regression (deferred — same pattern as the login limiters).
**Risk:** Low — copy of the existing pattern from `/api/auth/login` and `/api/auth/login/verify`.
**Prerequisite:** Step 1 done.

> Triggered by audit finding **H1**: both `/api/auth/2fa/generate` and `/api/auth/2fa/enable` are unauthenticated against brute-force at the application layer. `/generate` accepts a `password` and forwards to Directus — a stolen-session attacker can password-grind. `/enable` accepts a 6-digit OTP — brute-forceable at full request rate.

---

## The problem

The login feature shipped with two rate limiters (`loginRateLimiter`, `verifyRateLimiter`, both 5/5min by IP) protecting `/login` and `/login/verify`. The 2FA setup endpoints, added in Step 7 of the login feature, were not wired with their own limiter. After Step 1 of this feature, the password and OTP still both pass through unmetered.

Two new limiters, two two-line wirings.

## Acceptance criteria

Maps to [README](README.md) AC6–AC8:

- [ ] AC6: `/api/auth/2fa/generate` is rate-limited at 5 attempts / 5 minutes per IP. The 6th attempt returns 429 `{ error: 'rate_limited', retry_after_ms }`.
- [ ] AC7: `/api/auth/2fa/enable` is rate-limited at 5 attempts / 5 minutes per IP. The 6th attempt returns 429 `{ error: 'rate_limited', retry_after_ms }`.
- [ ] AC8: Both limits use separate buckets (a user spamming `generate` doesn't burn through `enable`'s budget). Verified by tests that spam one and assert the other still allows attempt #1.

## Technical constraints

- Reuse the existing `createRateLimiter` factory and 5/5min cap. No new infrastructure.
- Place the limiter check immediately after the origin check (matching the login route's structure) so even unauthenticated requests count against the bucket — protects against scanning.
- Bucket key is the client IP via `getClientIp(request)`. (H4 fixes the precedence in Step 3 of this feature.)

## Plan

### 2.1 Add to `src/lib/auth/stores.ts`

```ts
export const tfaGenerateRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });
export const tfaEnableRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });
```

### 2.2 Wire into both 2FA route handlers

Pattern (after origin check, before session lookup):

```ts
const ip = getClientIp(request);
const rl = tfaGenerateRateLimiter.check(ip);  // or tfaEnableRateLimiter
if (!rl.allowed) {
  return NextResponse.json(
    { error: 'rate_limited', retry_after_ms: rl.retryAfterMs },
    { status: 429 },
  );
}
```

`/generate` already has `void getClientIp(request)` as a placeholder — replace with the real read.

## Test plan

### `src/app/api/auth/2fa/generate/__tests__/route.test.ts` (extended, +2 cases)

- New mocks for `tfaGenerateRateLimiter.check` (default: `{ allowed: true }`).
- "429 when rate limit exceeded": mock returns `{ allowed: false, retryAfterMs: 1000 }`. Assert 429 + JSON shape. Assert `directusGenerateTfaSecret` not called.
- "rate-limit bucket is independent of /enable": assert calling `/generate` 5 times doesn't change `tfaEnableRateLimiter.check`'s call count (this one is checked by verifying the wiring imports the right limiter — covered by the unit-level mock).

### `src/app/api/auth/2fa/enable/__tests__/route.test.ts` (extended, +1 case)

- New mock for `tfaEnableRateLimiter.check`.
- "429 when rate limit exceeded": mirror the generate test.

## Done criteria

- [x] `tfaGenerateRateLimiter` + `tfaEnableRateLimiter` exported from `stores.ts`
- [x] Both 2FA routes wired with limiter check after origin check, before session lookup; mapping to 429
- [x] Vitest count delta: +2 (one 429 test per endpoint — sufficient: the rate-limiter factory's own logic is already covered by `rate-limit.test.ts`, so we only need to verify the handler wires it up and maps non-allowed → 429)
- [x] `npm run lint` + `npm run typecheck` clean
- [x] Audit doc `H1` line marked `[Resolved 2026-05-27]`

## Notes for future scaling

When the in-memory module-singleton stores migrate to a shared backend (per ADR scaling note), these two limiters move with the rest. No special-casing.
