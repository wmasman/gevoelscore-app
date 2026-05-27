# Step 1: Bind TFA secret server-side

**Estimated time:** 1 hour
**Test layer:** Vitest unit (new `pending-tfa.ts` store) + Vitest route handler tests (both 2FA routes) + live-stack regression (existing 2FA spec).
**Risk:** Low — additive store + one server-side lookup. Removing `body.secret` is a forced server-side migration, but the existing UI happens to send the secret it just received from `/generate`, so the value coming back from the store will be identical for honest clients.
**Prerequisite:** Login feature complete (steps 1–9). [Audit H2](../../audits/2026-05-27-auth-security-and-code-audit.md#high) is the trigger.

> Triggered by audit finding **H2**: `/api/auth/2fa/enable` reads `body.secret` and forwards it directly to Directus. An attacker with a valid session (briefly stolen, shared device, etc.) can plant their own TOTP secret — surviving the legitimate user's logout. This step removes the client's say in what secret gets activated.

---

## The problem

The flow today (post Step 7 of the login feature):

1. UI calls `POST /api/auth/2fa/generate` with `{ password }`. Server asks Directus to generate a TOTP secret, returns `{ secret, otpauth_url }`.
2. UI displays the QR + secret. User scans into authenticator, types the resulting 6-digit code.
3. UI calls `POST /api/auth/2fa/enable` with `{ secret, otp }`. Server forwards `secret + otp` to Directus's TFA-enable endpoint.

Step 3 is the bug: the client decides which secret gets activated. An honest client echoes whatever the server returned in step 1; a malicious client substitutes its own.

Fix: the server stashes the generated secret in a session-keyed in-memory store on step 1; on step 3 it looks the secret up itself and ignores the body's `secret` field.

## Acceptance criteria

Maps to [README](README.md) AC1–AC5:

- [ ] AC1: `POST /api/auth/2fa/generate` stashes the freshly-generated secret in a server-side `pendingTfaStore` keyed by session id; still returns the secret + `otpauth_url` to the user.
- [ ] AC2: `POST /api/auth/2fa/enable` looks up the secret from the store using the session id; the request body's `secret` field, if present, is ignored.
- [ ] AC3: If no pending TFA entry exists for the session (e.g. `enable` called without `generate`), the request returns 400 `invalid_request`.
- [ ] AC4: On successful enable, the pending entry is deleted from the store.
- [ ] AC5: The pending entry has a 10-minute TTL; lookups past TTL return undefined (lazy eviction) and the route returns 400 `invalid_request`.

## Technical constraints

- `pending-tfa.ts` mirrors the shape of `pending-otp.ts`: `create / get / delete / cleanupExpired / size`, injectable `now` + `idGenerator`, lazy expiry eviction on `get`. No cookie helpers — this store is keyed by the existing session cookie, not its own.
- Module singleton lives in `stores.ts` alongside the other stores.
- TTL is 10 minutes (longer than pending-OTP's 5 min — adding a TOTP factor on a phone with brainfog takes longer than typing a code from an authenticator that's already paired).
- `body.secret` is removed from the type and from the validation. Even if the client sends it, the server does not read it.
- No new dep.

## Plan

### 1.1 New file: `src/lib/auth/pending-tfa.ts`

```ts
export type PendingTfaData = {
  secret: string;
  expiresAt: number;
};

export type PendingTfaStore = {
  create: (sessionId: string, data: PendingTfaData) => void;
  get: (sessionId: string) => PendingTfaData | undefined;
  delete: (sessionId: string) => void;
  cleanupExpired: () => void;
  size: () => number;
};

export function createPendingTfaStore(config?: { now?: () => number }): PendingTfaStore {
  // ... mirror pending-otp shape; keyed by sessionId (not a generated id)
}
```

Key difference from `pendingOtpStore`: keyed by the **session id**, not by its own opaque id. There's no separate cookie — the session cookie does the addressing.

### 1.2 Add to `src/lib/auth/stores.ts`

One line: `export const pendingTfaStore = createPendingTfaStore();`

Plus an exported constant `PENDING_TFA_TTL_MS = 10 * 60_000` for the route handlers to use when computing `expiresAt`.

### 1.3 Modify `src/app/api/auth/2fa/generate/route.ts`

After `directusGenerateTfaSecret(...)` resolves with `ok: true`:

```ts
pendingTfaStore.create(sessionId, {
  secret: result.value.secret,
  expiresAt: Date.now() + PENDING_TFA_TTL_MS,
});
```

Response payload unchanged.

### 1.4 Modify `src/app/api/auth/2fa/enable/route.ts`

- Drop `secret` from the body type and validation.
- After `getValidatedSession` resolves, look up `pendingTfaStore.get(sessionId)`. If `undefined` → 400 `invalid_request`.
- Pass `pending.secret` (not `body.secret`) to `directusEnableTfa`.
- On `directusEnableTfa` ok → `pendingTfaStore.delete(sessionId)` before returning 200.
- On failure, leave the entry alone (so the user can retry the OTP without re-generating).

### 1.5 Update body schema for `/enable`

```ts
let body: { otp?: unknown };  // was { secret?: unknown; otp?: unknown }
// ...
const otp = typeof body.otp === 'string' ? body.otp.trim() : '';
if (!otp) {
  return NextResponse.json({ error: 'invalid_request' }, { status: 400 });
}
```

### 1.6 Frontend `setup-form.tsx`

No change required — it currently sends `{ secret, otp }`. The server will ignore `secret`. Honest clients are unaffected. Optionally drop `secret` from the request body in a follow-up to keep the wire payload tight; not blocking.

## Test plan

### `src/lib/auth/__tests__/pending-tfa.test.ts` (new, 5 cases)

| # | Case |
|---|---|
| 1 | `create + get` returns the same entry |
| 2 | `get` on unknown session id returns undefined |
| 3 | `get` past `expiresAt` returns undefined and evicts |
| 4 | `delete` removes the entry |
| 5 | `cleanupExpired` removes all past-TTL entries |

### `src/app/api/auth/2fa/generate/__tests__/route.test.ts` (extended, +1 case)

- New mock for `pendingTfaStore.create`. Assert it's called with the session id and the secret returned by Directus.

### `src/app/api/auth/2fa/enable/__tests__/route.test.ts` (rewritten, +2 cases)

- Mocks now include `pendingTfaStore.get / delete`.
- Existing "200 on valid session + secret + otp" becomes "200 on valid session + pending entry + otp" — body is `{ otp: '123456' }` only.
- New: "400 when no pending entry exists" — `pendingTfaStore.get` returns undefined.
- New: "client-supplied body.secret is ignored" — body is `{ secret: 'ATTACKER', otp: '123456' }`, mock `pendingTfaStore.get` returns `{ secret: 'LEGIT', ... }`. Assert `directusEnableTfa` is called with `'LEGIT'`, not `'ATTACKER'`.
- "On enable success, store.delete is called."

### Regression

- All existing 2FA route tests adjusted to the new body shape (drop `secret` where present).
- Playwright e2e `tests/e2e/2fa-setup.spec.ts` already POSTs `{ secret, otp }`; should keep working because the server ignores `secret` (the test sends the value the mocked `/generate` returned, which equals what the store returned).
- Live-stack `tests/live-stack/2fa-setup.spec.ts` (if any) regression unaffected.

## Done criteria

- [x] `pending-tfa.ts` exists with 6 unit-test cases green (added an extra "overwrite same session id" case)
- [x] `pendingTfaStore` + `PENDING_TFA_TTL_MS` exported from `stores.ts`
- [x] `/2fa/generate` stashes secret in store on success (+2 route tests green: stashes / doesn't stash on Directus failure)
- [x] `/2fa/enable` reads secret from store, ignores `body.secret`, deletes on success (+3 route tests green: uses stored, ignores body.secret, deletes)
- [x] No-pending-entry → 400 (+1 route test green); doesn't-delete-on-failure (+1)
- [x] Vitest count delta: +11 (6 store + 2 generate + 3 enable; finer-grained tests than the +8 plan)
- [x] `npm run lint` + `npm run typecheck` clean
- [x] Audit doc `H2` line marked `[Resolved 2026-05-27]`

### Side-quest caught during implementation

`parseSessionCookie` returns `string | null`, and the original handler narrowed with `sessionId ? await getValidatedSession(sessionId) : null`. After session resolution, TS still saw `sessionId` as `string | null` so `pendingTfaStore.create(sessionId, ...)` failed strict mode. **Fix**: narrowed `sessionId` first (early-return on null) before calling `getValidatedSession`. Applied symmetrically to both 2FA routes. No semantic change.
