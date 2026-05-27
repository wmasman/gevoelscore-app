# Step 9: Pending-OTP password lifecycle hardening (cheap H3)

**Estimated time:** 25 minutes
**Test layer:** Vitest unit (extend `pending-otp.test.ts` with the overwrite-on-delete behaviour).
**Risk:** Low — defensive only. No behavior change for any caller.
**Prerequisite:** Steps 1–8 done.

> Triggered by audit finding **H3**: the user's plaintext password sits in `pendingOtpStore` for up to 5 minutes between login and verify. Heap dump / swap / unintentional debug log leaks the credential. The audit listed two fixes: **(preferred)** AES-GCM at rest with a per-process key; **(cheap)** lifecycle tightening + assertions that the store is never logged. This step takes the cheap path — full encryption is deferred as a follow-up if a heap-dump threat materialises.

---

## What we're shipping (and why "cheap")

The audit's preferred fix wraps the store with AES-GCM. For a single-user app on a single Fly machine where the threat model is "someone snapshots my VM disk" (Fly volume is encrypted at rest; the snapshot path requires Fly account compromise), the residual risk after the cheap fixes is small. The expensive fix becomes worth it when:

- The store hosts secrets for multiple users (not this app).
- The runtime is shared with untrusted code (not this app — only our own image runs on the machine).
- A regulatory or insurance audit specifically calls for at-rest encryption of credential buffers (not this app's regime; Article 9 covers health data, not auth state).

What we DO ship here:

1. **Overwrite the password buffer on delete.** When a pending entry is removed (verify success, attempt-cap hit, manual delete, or TTL eviction), the stored password string is overwritten with random bytes before the entry object is garbage-collected. Strings in JS are immutable so this is "best effort" — the GC will eventually reclaim the original — but it shrinks the window during which a heap snapshot could capture the value.
2. **A guard comment + lint suppression in the test file.** The store object itself must NEVER be passed to `console.log`, `JSON.stringify`-then-log, or any logger. A `// @sensitive-store: do not log` comment near `pendingOtpStore` plus a runtime assertion that the store's `.toString()` returns a safe placeholder.

(Both are layered defenses, not silver bullets. The audit doc gets a follow-up "consider AES-GCM" line for the future.)

## Acceptance criteria

- [ ] AC1: When a pending entry is deleted via `store.delete(id)`, the entry's `password` field is overwritten (to a non-empty string of equal-or-greater length) before the Map entry is removed.
- [ ] AC2: Lazy TTL eviction (via `get` or `incrementAttempts` past `expiresAt`) also overwrites before removing.
- [ ] AC3: `cleanupExpired` overwrites every expired entry before removing.
- [ ] AC4: The store object's `toString()` (and any accidental `console.log(store)`) returns a placeholder like `[PendingOtpStore: 2 entries — do not log]`, not the actual `[object Object]` that exposes the Map via `inspect`.
- [ ] AC5: A `@sensitive-store: do not log` marker comment lives at the export site so future maintainers see the rule before they wire a logger.

## Technical constraints

- No new dep. `crypto.randomBytes` is Node-only — the store is server-side, so that's fine.
- The overwrite happens just before the Map delete call. After overwrite, the entry object is unreferenced from the Map and eligible for GC.
- Test the overwrite by snapshotting the entry reference before delete, then checking the password field changed. This proves the overwrite happened; it does NOT prove the JS engine has actually freed the original string (impossible to assert from inside JS).

## Plan

### 9.1 Update `src/lib/auth/pending-otp.ts`

```ts
import { randomBytes } from 'node:crypto';

function wipe(entry: PendingOtpData): void {
  // Overwrite the password buffer in place. Strings are immutable in JS so
  // the *original* allocation persists until GC, but this shortens the
  // window during which a heap snapshot would reveal the plaintext.
  entry.password = randomBytes(Math.max(32, entry.password.length)).toString('base64');
}
```

Wire `wipe(entry)` into `get` (TTL eviction branch), `delete`, `incrementAttempts` (TTL branch), and `cleanupExpired`.

### 9.2 Custom `toString()` on the store

The store factory returns an object literal. Add a non-enumerable `toString` property:

```ts
const store: PendingOtpStore = { ... };
Object.defineProperty(store, 'toString', {
  value: function () { return `[PendingOtpStore: ${entries.size} entries — do not log]`; },
  enumerable: false,
});
```

### 9.3 Add the marker comment

At the export site in `src/lib/auth/stores.ts`:

```ts
// @sensitive-store: do not pass to console.log, JSON.stringify, or any logger.
// Contains plaintext passwords between /login and /login/verify (audit H3).
export const pendingOtpStore = createPendingOtpStore();
```

## Test plan

### `src/lib/auth/__tests__/pending-otp.test.ts` (extended, +3 cases)

- "delete overwrites password before removing": create + capture entry reference + delete + assert reference.password no longer equals the original.
- "get on expired entry overwrites password before evicting": same shape, triggered via the TTL branch.
- "toString returns the safe placeholder, not the entries map": `String(store)` matches `/PendingOtpStore.*do not log/`.

## Done criteria

- [x] `wipe()` helper added; wired into delete/get-TTL/incrementAttempts-TTL/cleanupExpired
- [x] `store.toString()` returns the safe placeholder (`[PendingOtpStore: N entries — do not log]`)
- [x] `@sensitive-store` marker comment at the export site in `stores.ts`
- [x] 3 new unit tests green
- [x] Vitest count delta: +3 (377 → 380)
- [x] `npm run verify` clean
- [x] Audit doc H3 line marked `[Resolved 2026-05-27 — Step 9 (cheap fix). AES-GCM at rest deferred.]`
