# Step 3: Trust Fly-Client-IP over X-Forwarded-For

**Estimated time:** 20 minutes
**Test layer:** Vitest unit (`getClientIp` precedence cases) + lightweight integration coverage via the existing route tests (still pass with the new logic).
**Risk:** Low — pure function rewrite with full unit coverage.
**Prerequisite:** Steps 1–2 done.

> Triggered by audit finding **H4**: `getClientIp()` reads the *first* hop of `X-Forwarded-For`. On Fly, that's whatever the client sent — appendable per request, defeating the 5/5min cap. Fly's edge sets `Fly-Client-IP` which the runtime cannot append to.

---

## The problem

Today in [`src/lib/auth/stores.ts:26-33`](../../../src/lib/auth/stores.ts#L26-L33):

```ts
export function getClientIp(request: Request): string {
  const xff = request.headers.get('x-forwarded-for');
  if (xff) {
    const first = xff.split(',')[0];
    if (first) return first.trim();
  }
  return request.headers.get('x-real-ip') ?? 'unknown';
}
```

`X-Forwarded-For: 1.2.3.4, 5.6.7.8` means "1.2.3.4 was the originating client, 5.6.7.8 was the first proxy." But anyone can send `X-Forwarded-For: rotating-value` to Fly, and Fly *appends* its own observed source, producing `X-Forwarded-For: rotating-value, real.ip`. We trust the first entry — the rotating value — so the attacker burns through a fresh rate-limit bucket on every request.

Fly populates `Fly-Client-IP` with the address it actually saw at the edge. That header is what we want.

## Acceptance criteria

Maps to [README](README.md) AC9–AC10:

- [ ] AC9: `getClientIp(request)` precedence is `Fly-Client-IP` → `X-Real-IP` → last hop of `X-Forwarded-For` → `'unknown'`.
- [ ] AC10: A request that prepends its own value to `X-Forwarded-For` (`X-Forwarded-For: poisoned, real.ip` with `Fly-Client-IP: real.ip`) returns `real.ip`, not `poisoned`.

## Technical constraints

- Pure function rewrite. Same signature, same return type.
- Comments document the deploy assumption: "this app always runs behind Fly.io's edge proxy" — explicit so a future move off Fly is reviewed against this assumption.
- Existing callers (`login`, `login/verify`, `logout`, `2fa/generate`, `2fa/enable`) need no changes.

## Plan

### 3.1 Rewrite `getClientIp` in `src/lib/auth/stores.ts`

```ts
// Resolve the client IP. Precedence:
//   1. `Fly-Client-IP` — set by Fly's edge, not appendable by the client.
//   2. `X-Real-IP` — set by some reverse proxies; same trust posture.
//   3. *Last* entry of `X-Forwarded-For` — the address closest to our proxy.
//      Earlier entries are client-controlled in single-proxy hops.
//   4. 'unknown' fallback — single bucket; safe because the app sits behind
//      Fly's edge in production.
// Assumes the app always runs behind Fly.io's edge proxy.
export function getClientIp(request: Request): string {
  const fly = request.headers.get('fly-client-ip');
  if (fly) return fly.trim();
  const real = request.headers.get('x-real-ip');
  if (real) return real.trim();
  const xff = request.headers.get('x-forwarded-for');
  if (xff) {
    const parts = xff.split(',').map((p) => p.trim()).filter(Boolean);
    if (parts.length > 0) return parts[parts.length - 1]!;
  }
  return 'unknown';
}
```

### 3.2 Document deploy assumption

Append a one-line note to [`docs/architecture/current-state.md`](../../architecture/current-state.md) "Cloud resources" section: "`getClientIp` trusts `Fly-Client-IP`. If moving off Fly, audit rate-limit bypass surface."

## Test plan

### `src/lib/auth/__tests__/stores.test.ts` (new file, 5 cases)

| # | Case |
|---|---|
| 1 | `Fly-Client-IP` present alone → returned |
| 2 | `Fly-Client-IP` + spoofed `X-Forwarded-For` → returns Fly-Client-IP, not XFF first hop (AC10 bypass attempt) |
| 3 | No `Fly-Client-IP`, `X-Real-IP` present → returned |
| 4 | Only `X-Forwarded-For` present → returns *last* hop, not first |
| 5 | No headers at all → returns `'unknown'` |

Plus an existing-behaviour test that catches the regression: AC10's "first XFF hop is no longer returned."

## Done criteria

- [x] `getClientIp` rewritten with new precedence
- [x] 5 new unit tests green in `src/lib/auth/__tests__/stores.test.ts` (including the explicit AC10 bypass-attempt case: Fly-Client-IP wins even when XFF carries `attacker-rotating-value, real.ip`)
- [x] All existing route tests still green (369/369 total)
- [x] Vitest count delta: +5
- [x] `npm run lint` + `npm run typecheck` clean
- [x] Audit doc `H4` line marked `[Resolved 2026-05-27]`
- [x] `current-state.md` "First-deploy notes" extended with item 3 documenting the Fly-Client-IP assumption
