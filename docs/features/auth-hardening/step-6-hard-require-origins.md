# Step 6: Hard-require allowed origins in production

**Estimated time:** 20 minutes
**Test layer:** Vitest unit (extend `allowed-origins.test.ts` with the throw case).
**Risk:** Low — guards a misconfiguration that shouldn't exist in any sane deploy.
**Prerequisite:** Step 5 done.

> Triggered by audit finding **M3**: if `NEXT_PUBLIC_APP_URL` is unset in production, `allowedOrigins()` returns `[]`. Combined with `validateOrigin`'s "header-less request = same-origin" fallback, the CSRF protection silently switches off. A misconfigured deploy = no CSRF defense, no warning.

---

## The problem

Today the util is permissive:

```ts
export function allowedOrigins(): string[] {
  const origins: string[] = [];
  if (process.env.NEXT_PUBLIC_APP_URL) origins.push(process.env.NEXT_PUBLIC_APP_URL);
  if (process.env.NODE_ENV !== 'production') origins.push('http://localhost:3000');
  return origins;
}
```

`NEXT_PUBLIC_APP_URL` unset in production yields `[]`. `validateOrigin(null, null, [])` returns `true` (header-less requests are treated as same-origin). Net effect: the origin check is functionally off until someone notices.

Fly secrets management makes this misconfiguration unlikely but trivially severe if it happens. The fix is a startup-time invariant: an empty production list is an error, not a "permit everything" state.

## Acceptance criteria

- [ ] AC1: In production (`NODE_ENV === 'production'`) with `NEXT_PUBLIC_APP_URL` unset, `allowedOrigins()` throws a clear, surgical error pointing at the missing env var.
- [ ] AC2: In production with `NEXT_PUBLIC_APP_URL` set, `allowedOrigins()` returns `[that URL]` (unchanged).
- [ ] AC3: In development, behaviour is unchanged regardless of `NEXT_PUBLIC_APP_URL` state (no throw, localhost added).
- [ ] AC4: The thrown error surfaces in the route handler's response cycle as a 500 with a generic body — not a stack trace to the client. (Already the default Next.js behaviour; the error message contains the misconfiguration detail for the server logs.)

## Technical constraints

- Throw at call time, not at module load. Module-load throws would crash the entire Next.js process before any route handler can respond; throwing at call time means the misconfigured deploy returns 500 instead of being unreachable. The 500 is still loud enough to notice.
- Error message names `NEXT_PUBLIC_APP_URL` explicitly. Vague errors waste debugging time on a misconfiguration that has one obvious cause.

## Plan

### 6.1 Update `src/lib/auth/allowed-origins.ts`

```ts
export function allowedOrigins(): string[] {
  const origins: string[] = [];
  if (process.env.NEXT_PUBLIC_APP_URL) origins.push(process.env.NEXT_PUBLIC_APP_URL);
  if (process.env.NODE_ENV !== 'production') origins.push('http://localhost:3000');
  if (process.env.NODE_ENV === 'production' && origins.length === 0) {
    throw new Error(
      'allowedOrigins: NEXT_PUBLIC_APP_URL must be set in production (CSRF defense relies on it).',
    );
  }
  return origins;
}
```

### 6.2 Extend `allowed-origins.test.ts`

Replace the Step 5 case 4 (`returns []`) with a `.toThrow` assertion.

## Test plan

### Updated cases in `src/lib/auth/__tests__/allowed-origins.test.ts`

| # | Env state | Expected |
|---|---|---|
| 1 | URL set + prod | `['url']` (unchanged) |
| 2 | URL set + dev | `['url', 'localhost']` (unchanged) |
| 3 | URL unset + dev | `['localhost']` (unchanged) |
| 4 | URL unset + prod | **throws** with message mentioning `NEXT_PUBLIC_APP_URL` |

## Done criteria

- [x] `allowedOrigins()` throws in the misconfigured production case
- [x] Test 4 converted to `.toThrow(/NEXT_PUBLIC_APP_URL/)`; all 4 cases pass
- [x] Vitest count unchanged at 373 (the failing-case test is converted, not added)
- [x] `npm run verify` clean
- [x] Audit doc M3 line marked `[Resolved 2026-05-27 — Step 6]`
