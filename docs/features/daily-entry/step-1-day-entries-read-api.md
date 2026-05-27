# Step 1: `/api/day-entries` read API

**Estimated time:** 1.5 hours
**Test layer:** Vitest route-handler tests (mocked Directus SDK) + Playwright live-stack spec (real Directus, asserts the 1,363-day baseline visible).
**Risk:** Low. Read-only, well-known Directus REST surface, narrow shape contract.
**Prerequisite:** Auth-hardening A1+A2 done; domain layer locked.

> Read-side first so the timeline view in Step 6 can be built against the live 1,363-day dataset without any write logic landing. Also unblocks the Step 2 "today screen shell" — we need to *read* today's entry to decide whether to render the empty score row or the existing one.

---

## Acceptance criteria

- [ ] AC1: `GET /api/day-entries/today` returns 200 with `{ entry: DayEntry | null }`. `null` means "no entry exists for today's local date." 401 without a valid session.
- [ ] AC2: `GET /api/day-entries?from=YYYY-MM-DD&to=YYYY-MM-DD` returns 200 with `{ entries: DayEntry[] }`, sorted by date ascending. Range is inclusive on both ends. Max range 90 days (server-side cap; further reduces the surface for accidental large reads).
- [ ] AC3: `from` and `to` are validated by `validateDate` from the domain layer. `to < from`, out-of-range, or malformed dates → 400 `invalid_request`.
- [ ] AC4: Both routes require a valid session (`getValidatedSession`); fail with 401 `unauthenticated` otherwise. Middleware (M2 fix) catches missing cookies first; the route handler is defense in depth.
- [ ] AC5: Both routes carry origin check via the shared `allowedOrigins` util. Cross-origin → 403 `forbidden`.
- [ ] AC6: Each returned `DayEntry` carries `tag_ids: string[]` populated from the M2M junction (not the verbose `tags: [{ id, name, category }]` shape that Directus returns by default). The route handler maps Directus's response into the domain shape.
- [ ] AC7: No PII in logs. The note field is never logged. Per-request log line is at most `{ ip-hashed, status, duration_ms }`.

## Technical constraints

- Uses `@directus/sdk` v18 via the existing pattern in [src/lib/auth/directus-auth.ts](../../../src/lib/auth/directus-auth.ts). A new wrapper file [src/lib/api/day-entries.ts](../../../src/lib/api/day-entries.ts) hosts the SDK calls — keeps the route handler thin and the SDK noise isolated.
- Result-style return shape: `{ ok: true; value: DayEntry[] } | { ok: false; error: 'network_error' | 'directus_error' }`.
- The SDK call uses `readItems('day_entries', { filter, sort, limit, fields })` with `fields: ['*', 'tags.tags_id']` so we get the junction's tag references inline; the route handler flattens to `tag_ids: string[]`.
- TTL caching deliberately omitted — read latency from Directus on the internal Fly network is already sub-30ms; adding a cache surface is premature.

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01, A03, A04, A07, A08 | Yes | Origin check + `getValidatedSession` + body/query validation + Result wrapping in the SDK wrapper |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | Reads existing collection; writes are Step 3 |
| New dependency | ADR or step rationale | No | No new deps |
| `dangerouslySetInnerHTML` usage | A03 | No | No JSX |
| New env var with a secret | A02, A05 | No | Uses existing `DIRECTUS_URL` + session cookie |
| New telemetry / observability dep | Cardinal "no telemetry" | No | — |

## Plan

### 1.1 New file: [src/lib/api/day-entries.ts](../../../src/lib/api/day-entries.ts)

Wrapper around the SDK. Two exports:

```ts
export async function readDayEntryByDate(accessToken: string, date: string)
  : Promise<{ ok: true; value: DayEntry | null } | { ok: false; error: ... }>;

export async function readDayEntriesInRange(accessToken: string, from: string, to: string)
  : Promise<{ ok: true; value: DayEntry[] } | { ok: false; error: ... }>;
```

Both flatten the Directus M2M shape to `tag_ids: string[]`.

### 1.2 New route handlers

- [src/app/api/day-entries/today/route.ts](../../../src/app/api/day-entries/today/route.ts) — GET handler.
- [src/app/api/day-entries/route.ts](../../../src/app/api/day-entries/route.ts) — GET handler for the range.

Both follow the established pattern from `src/app/api/auth/*/route.ts`: origin check → session lookup → query parse + validate → SDK call → response.

### 1.3 Today's date resolution

The "today" route uses the *server's* date in `Europe/Amsterdam` (the user's timezone — codified in the project as the single user's locale). Future: a header or query param to override for testing. For now: hard-coded TZ string; documented in code.

## Test plan

### `src/lib/api/__tests__/day-entries.test.ts` (new, ~6 cases)

| # | Case |
|---|---|
| 1 | `readDayEntryByDate` returns null when no entry exists |
| 2 | `readDayEntryByDate` flattens M2M `tags` to `tag_ids` |
| 3 | `readDayEntriesInRange` returns entries sorted by date |
| 4 | `readDayEntriesInRange` enforces the 90-day cap (Directus query limit) |
| 5 | network failure → `{ ok: false, error: 'network_error' }` |
| 6 | Directus 5xx → `{ ok: false, error: 'directus_error' }` |

### `src/app/api/day-entries/today/__tests__/route.test.ts` (new, ~5 cases)

| # | Case |
|---|---|
| 1 | 200 with `{ entry: null }` when no row for today |
| 2 | 200 with `{ entry: DayEntry }` when row exists |
| 3 | 401 without a session cookie |
| 4 | 403 cross-origin |
| 5 | 502 when the SDK wrapper returns `directus_error` |

### `src/app/api/day-entries/__tests__/route.test.ts` (new, ~6 cases)

Same shape; adds 400 cases for invalid `from`/`to` and the > 90-day range.

### `tests/live-stack/day-entries.spec.ts` (new, 2 cases)

- "the 1,363-day baseline is readable via the range endpoint" — read 2022-09-03 → 2026-05-27 in batches of 90; assert total rows match the known count.
- "today's entry is readable (or null)" — single call against the live endpoint.

Live-stack is added because dev-mode mocks don't catch Directus shape drift, and this is the first endpoint that talks to the real collection.

## Done criteria

- [ ] `src/lib/api/day-entries.ts` exists with 6 unit-test cases green
- [ ] Both route handlers exist with their unit-test suites green
- [ ] Live-stack spec passes against `https://gevoelscore-backend.fly.dev`
- [ ] Vitest count delta: +17 (6 SDK wrapper + 5 today + 6 range)
- [ ] Playwright dev specs unchanged; live-stack +2
- [ ] `npm run verify` clean
- [ ] One-line note in [`current-state.md`](../../architecture/current-state.md) when the live-stack passes — first non-auth API endpoint live
