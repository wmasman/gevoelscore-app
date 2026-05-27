# Step 5: Extract `allowedOrigins()` to a shared util

**Estimated time:** 20 minutes
**Test layer:** Vitest unit (new util) + existing route handler tests unchanged (they don't care about the implementation source).
**Risk:** Trivial — copy/paste/import. Tests catch any wiring mistake.
**Prerequisite:** Steps 1–4 done.

> Triggered by the audit's "DRY violations worth fixing" section. The same 4-line `allowedOrigins()` function is defined inline in all 5 route handlers. The DRY fix is the prerequisite for Step 6 (audit M3): "throw at startup if `NEXT_PUBLIC_APP_URL` is unset in production" needs a single source of truth to thread through.

---

## The problem

Every route handler under `src/app/api/auth/*` declares:

```ts
function allowedOrigins(): string[] {
  const origins: string[] = [];
  if (process.env.NEXT_PUBLIC_APP_URL) origins.push(process.env.NEXT_PUBLIC_APP_URL);
  if (process.env.NODE_ENV !== 'production') origins.push('http://localhost:3000');
  return origins;
}
```

Five copies. If we change the policy in one place (e.g. add a staging origin), the other four drift. Worse: Step 6's M3 fix requires hardening behaviour in production. With five copies, that's five places to patch and four places to forget.

## Acceptance criteria

- [ ] AC1: `allowedOrigins()` lives in `src/lib/auth/allowed-origins.ts` as a named export.
- [ ] AC2: All 5 route handlers (`login`, `login/verify`, `logout`, `2fa/generate`, `2fa/enable`) import the function from the shared util; their inline copies are deleted.
- [ ] AC3: Behaviour preserved exactly — `npm test` stays at 369 (no test count delta beyond the new util's own coverage).
- [ ] AC4: Unit-test the util's three cases: env var set + dev → both origins; env var set + prod → only the env-var origin; env var unset + dev → only localhost; env var unset + prod → empty (will become a thrown error in Step 6, but Step 5 keeps current behaviour).

## Technical constraints

- Pure function. No side effects, no caching, reads env vars at call time so test env-var stubbing works.
- Returns `string[]`. Empty is allowed for now; Step 6 will tighten the production case.
- The function is server-only — no `'use client'` files import from `src/lib/auth/`.

## Plan

### 5.1 New file: `src/lib/auth/allowed-origins.ts`

```ts
export function allowedOrigins(): string[] {
  const origins: string[] = [];
  if (process.env.NEXT_PUBLIC_APP_URL) origins.push(process.env.NEXT_PUBLIC_APP_URL);
  if (process.env.NODE_ENV !== 'production') origins.push('http://localhost:3000');
  return origins;
}
```

### 5.2 Update 5 route handlers

For each of:
- `src/app/api/auth/login/route.ts`
- `src/app/api/auth/login/verify/route.ts`
- `src/app/api/auth/logout/route.ts`
- `src/app/api/auth/2fa/generate/route.ts`
- `src/app/api/auth/2fa/enable/route.ts`

Replace the inline `function allowedOrigins(): string[] { ... }` with `import { allowedOrigins } from '@/lib/auth/allowed-origins';`. The call sites (one per handler, inside the origin-check block) stay unchanged.

### 5.3 Unit-test the util

`src/lib/auth/__tests__/allowed-origins.test.ts` — 4 cases per AC4, with `process.env` stubbing via `vi.stubEnv` / `vi.unstubAllEnvs` in `beforeEach`.

## Test plan

### `src/lib/auth/__tests__/allowed-origins.test.ts` (new, 4 cases)

| # | Env state | Expected |
|---|---|---|
| 1 | NEXT_PUBLIC_APP_URL=https://app.example.com, NODE_ENV=production | `['https://app.example.com']` |
| 2 | NEXT_PUBLIC_APP_URL=https://app.example.com, NODE_ENV=development | `['https://app.example.com', 'http://localhost:3000']` |
| 3 | NEXT_PUBLIC_APP_URL unset, NODE_ENV=development | `['http://localhost:3000']` |
| 4 | NEXT_PUBLIC_APP_URL unset, NODE_ENV=production | `[]` (Step 6 will change this to throw) |

## Done criteria

- [x] `src/lib/auth/allowed-origins.ts` exists with 4 unit-test cases green
- [x] All 5 route handlers import from the shared util; their inline copies are deleted
- [x] Vitest count delta: +4 (369 → 373). All existing tests stay green.
- [x] `npm run verify` clean
- [x] Audit doc DRY-violations marker appended
