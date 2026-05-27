# Step 8: Per-pending-id OTP attempt counter

**Estimated time:** 40 minutes
**Test layer:** Vitest unit (extend `pending-otp.test.ts` + the `/login/verify` route handler tests).
**Risk:** Low — adds a field + a small branch. The existing IP rate limiter remains the first gate.
**Prerequisite:** Steps 1–7 done.

> Triggered by audit finding **M5**: today an invalid OTP keeps the pending cookie alive (required by AC7 — UX retry within rate limit). Combined with the IP-only rate limit, an attacker who has the pending cookie can let the IP bucket reset (5 minutes) and retry indefinitely. Adding a per-pending-id attempt counter caps the OTP brute-force surface at 3 tries before the user must re-authenticate from `/login`.

---

## The problem

`PendingOtpData` today is `{ email, password, expiresAt }`. An OTP failure path in `/api/auth/login/verify`:

1. User submits wrong OTP → 401, pending cookie preserved.
2. IP rate limit eats 1 attempt (5/5min). After 5 wrong tries, IP is throttled.
3. Wait 5 min. IP bucket resets. Try again. The pending cookie is still alive (15-min TTL); the rate-limit counter is fresh.

Net effect: the OTP brute-force budget is `5 × ceil(15min / 5min) = 15 attempts` over the pending cookie's lifetime, not 5. With 1,000,000 possible 6-digit codes that's still long, but it's also 3x more than the design intent.

The fix is a counter that persists across IP bucket resets — keyed to the pending entry, not the IP. Three wrong tries and the pending entry dies; the user has to log in fully from `/login`.

## Acceptance criteria

- [ ] AC1: `PendingOtpData` gains an `attempts: number` field, default `0` on create.
- [ ] AC2: On wrong OTP, the route handler increments `attempts` on the pending entry before returning 401.
- [ ] AC3: If `attempts` reaches the cap (3), the pending entry is deleted, the pending cookie is cleared, and the response is 401 — same generic error message ("invalid OTP"). No information leak about why the pending state is gone.
- [ ] AC4: On successful OTP, `attempts` resets implicitly via the existing entry-delete path. No behaviour change for the happy path.

## Technical constraints

- The cap is `3` — three honest fumbles is the realistic ceiling for "I typed the wrong digit"; beyond that it's an attack. Defined as a constant in the route handler (or `pending-otp.ts`) for one-line tuning later.
- The pending entry's store needs an `incrementAttempts(id)` or a mutating `update(id, data)` method. Cleanest: extend the store API with `incrementAttempts(id) → number` returning the new count, lazy-evicting expired entries first.
- The route handler still preserves the pending cookie on the first two failures (AC7 unchanged). Only the third failure triggers the cookie clear.

## Plan

### 8.1 Extend `src/lib/auth/pending-otp.ts`

- Add `attempts: number` to `PendingOtpData`.
- Add `incrementAttempts(id): number | undefined` to the store, returning the new attempts count (or `undefined` if the id is unknown/expired). Lazy-evicts past-TTL entries the same way `get` does.
- Bump default on `create` from absent → `0`.

### 8.2 Update `src/app/api/auth/login/route.ts`

When creating a pending entry, set `attempts: 0`.

### 8.3 Update `src/app/api/auth/login/verify/route.ts`

```ts
const OTP_ATTEMPT_CAP = 3;
// ... (existing code up through 'if (!result.ok)')

if (!result.ok) {
  const attempts = pendingId ? pendingOtpStore.incrementAttempts(pendingId) ?? 0 : 0;
  if (attempts >= OTP_ATTEMPT_CAP) {
    if (pendingId) pendingOtpStore.delete(pendingId);
    const res = NextResponse.json({ error: 'invalid_otp' }, { status: 401 });
    res.headers.append('Set-Cookie', buildPendingOtpCookie(null, 0));
    return res;
  }
  return NextResponse.json({ error: 'invalid_otp' }, { status: 401 });
}
```

## Test plan

### `src/lib/auth/__tests__/pending-otp.test.ts` (extended, +2 cases)

- `incrementAttempts` returns 1, 2, 3 on successive calls; the stored data carries the same counter.
- `incrementAttempts` returns undefined for unknown / expired entries.

### `src/app/api/auth/login/verify/__tests__/route.test.ts` (extended, +2 cases)

- "3 wrong OTP attempts → cookie cleared on the 3rd response": mock pendingOtpStore.get to return a fresh entry; mock incrementAttempts to count up. Assert the response on attempt 3 carries a Set-Cookie clearing `gs_pending_otp`.
- "2 wrong OTP attempts keep the cookie alive" (sanity): assert no `Set-Cookie` clearing the pending cookie on attempts 1 and 2.

## Done criteria

- [x] `PendingOtpData.attempts` exists; `incrementAttempts` on the store
- [x] `/login` initialises `attempts: 0`
- [x] `/login/verify` increments on failure and clears the pending entry + cookie at cap (3)
- [x] Vitest count delta: +4 (373 → 377)
- [x] `npm run verify` clean
- [x] Audit doc M5 line marked `[Resolved 2026-05-27 — Step 8]`
