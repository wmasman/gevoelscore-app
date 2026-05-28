# Step 3: `/api/day-entries` write API (upsert by date)

**Estimated time:** 1.5 hours
**Test layer:** Vitest route-handler tests (mocked Directus SDK) + Playwright live-stack spec asserting an actual write lands in Postgres and is read back through the Step 1 endpoint.
**Risk:** Medium — first write path against the user's real historical data. The route must be safe-by-default and clearly auditable.
**Prerequisite:** Step 1 done.

> One endpoint, upsert semantics, single client call per tap. The route validates the body through the existing domain layer (`validateScore`, `validateNote`, `validateTagIds`, `validateDate`), runs through the standard auth/origin/rate-limit gates, and writes via the Directus SDK.

---

## Acceptance criteria

- [ ] AC1: `PUT /api/day-entries/[date]` with body `{ score: number, note?: string | null, tag_ids?: string[] }` upserts the row keyed by `date`. Returns 200 with `{ entry: DayEntry }`.
- [ ] AC2: Score is required, validated by `validateScore`. Invalid → 400 `invalid_request`.
- [ ] AC3: `note` is optional; null/empty/whitespace → stored as null (normalised by `normalizeNote`). No length cap (per data-model).
- [ ] AC4: `tag_ids` is optional; defaults to existing entry's tags if omitted, or `[]` if the row is new. Validated by `validateTagIds`. Unknown tag ids in the array → 400 `invalid_request`.
- [ ] AC5: `[date]` path param is validated by `validateDate`. Future dates rejected (per existing domain rule). Malformed → 400.
- [ ] AC6: Auth: 401 without a valid session. Origin: 403 on cross-origin. Rate limit: 5/5min by IP on writes (matching the login family).
- [ ] AC7: M2M tag updates are atomic — the route handler diff-syncs `tag_ids` against the existing junction rows (delete removed, insert added). Junction `source` is set to `'user'`, `confidence: 1.0`, `confirmed_at: now()`.
- [ ] AC8: Response includes the full updated `DayEntry` shape (same flattening as Step 1) so the client can replace its optimistic state with the server-confirmed truth in one round-trip.
- [ ] AC9: `// TODO(I3): audit-log entry` comment at the success path. No log infrastructure ships here; the placeholder lives so Track A3 can find every call site.
- [ ] AC10: No PII in logs. The note field never appears in any logged line. Per-request log: `{ ip-hashed, date, score, status, duration_ms }` — score is OK (not PII; the user is the only user).

## Technical constraints

- Path-as-key: `app/api/day-entries/[date]/route.ts`. Next 15 dynamic segment, validated by `validateDate` before any SDK call.
- The SDK wrapper grows: add `upsertDayEntry(accessToken, date, patch)` and `syncDayEntryTags(accessToken, entryId, tagIds)` to `src/lib/api/day-entries.ts`.
- Atomicity tradeoff: the upsert itself is one PATCH/POST; the tag-junction sync is two writes (delete-removed + insert-added). For a single-user app, the race window is irrelevant; for v2/native we'd revisit. Documented in the wrapper's comment.
- The route does NOT support DELETE in this step. Delete-all is a separate user-owned-data feature; per-day delete is not in the v1 UX (users should change a wrong score by tapping the right one, not by deleting and re-entering).

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01, A03, A04, A07, A08 | Yes | All five guards present: origin check, `getValidatedSession`, body validation via domain validators, rate limiter, Result wrapping |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | Yes | `day_entries` IS the Article 9 surface — `// TODO(I3): audit-log entry` placeholder + retention note in feature README |
| New dependency | ADR or step rationale | No | No new deps |
| `dangerouslySetInnerHTML` usage | A03 | No | — |
| New env var with a secret | A02, A05 | No | — |
| New telemetry / observability dep | Cardinal "no telemetry" | No | — |

## Plan

### 3.1 Extend `src/lib/api/day-entries.ts`

```ts
export async function upsertDayEntry(
  accessToken: string,
  date: string,
  patch: { score: Score; note?: string | null; tag_ids?: string[] },
): Promise<Result<DayEntry>>;
```

Internally:
1. Read existing row by date (single SDK `readItems` with filter).
2. If exists → `updateItem` + tag sync. If not → `createItem` + tag insert.
3. Re-read with full shape (same as Step 1) and return.

The "re-read at end" is deliberate — the server gives the client the canonical post-write shape so client state is reconciled.

### 3.2 New route handler: `src/app/api/day-entries/[date]/route.ts`

PUT only in this step. GET on the same path is a Step 1 candidate add later if needed (today it's served by the range endpoint).

Standard pipeline:
1. Origin check (`allowedOrigins`)
2. Rate limit (`dayEntryWriteRateLimiter` — new, 5/5min, added to `src/lib/auth/stores.ts`)
3. `getValidatedSession`
4. Validate path param `[date]` with `validateDate`
5. Parse + validate body (`validateScore`, `normalizeNote`, `validateTagIds`)
6. Call `upsertDayEntry`
7. Return 200 with `{ entry }` or map errors to 400/401/403/429/502

### 3.3 New rate limiter in `stores.ts`

`export const dayEntryWriteRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });` — same shape as the others. Tested via the existing rate-limiter unit suite (no new test needed).

## Test plan

### `src/lib/api/__tests__/day-entries.test.ts` (extend, +6 cases)

| # | Case |
|---|---|
| 7 | `upsertDayEntry` creates a row when none exists for the date |
| 8 | `upsertDayEntry` updates an existing row in place |
| 9 | `upsertDayEntry` syncs M2M tags: removes one, adds one |
| 10 | `upsertDayEntry` preserves note when patch omits it |
| 11 | `upsertDayEntry` clears note when patch sets `note: null` |
| 12 | network failure → `{ ok: false, error: 'network_error' }` |

### `src/app/api/day-entries/[date]/__tests__/route.test.ts` (new, ~9 cases)

| # | Case |
|---|---|
| 1 | 200 on valid score-only PUT |
| 2 | 200 on valid score + note + tags |
| 3 | 400 on missing score |
| 4 | 400 on out-of-range score |
| 5 | 400 on malformed date in path |
| 6 | 400 on future date |
| 7 | 401 without session |
| 8 | 403 cross-origin |
| 9 | 429 when rate limit exceeded |

### `tests/live-stack/day-entries.spec.ts` (extend, +2 cases)

| # | Case |
|---|---|
| 3 | Write a test entry for a non-historical date (e.g. `2099-12-31` if allowed; otherwise a fixture date) then read it back through Step 1's range endpoint. Cleanup: delete the row in `afterAll`. |
| 4 | Update an existing test entry's score; assert the change is reflected. Cleanup same. |

**Trade-off**: writing to the live Directus from tests means the 1,363-day dataset gets a temporary fixture row. The `afterAll` deletion mitigates but doesn't guarantee zero pollution if the test crashes between write and cleanup. Mitigation: fixture dates are `2099-*` so any leakage is visible and harmless.

## Done criteria

- [x] `upsertDayEntry` shipped with M2M tag sync inlined (no separate `syncDayEntryTags` export — see side-quest #1); 6 wrapper tests green
- [x] Route handler shipped at `src/app/api/day-entries/[date]/route.ts`; 10 unit tests green (planned 9; added one for the `score + note + tag_ids` full-patch happy path)
- [x] `dayEntryWriteRateLimiter` exported from `stores.ts` (5/5min by IP, same factory as the login family)
- [x] Live-stack spec extended (+2 cases: write fixture row at 2099-12-31, update fixture in place). Skip-when-no-token; runs against live Directus when `PLAYWRIGHT_TEST_FRONTEND_TOKEN` is set.
- [x] `// TODO(I3): audit-log entry` comment at the success path of the route handler
- [x] Vitest count delta: +16 (planned +15; the route-handler full-patch test put us over)
- [x] `npm run verify` clean: 432/432 Vitest, lint + typecheck both clean
- [x] Existing Playwright e2e 30/30 — no regressions from Step 3
- [ ] Manual: curl-based PUT against the deployed app — deferred to the Step 3 deploy moment (Step 3 alone has no UI; sensible to deploy when Step 4 lands so the manual test exercises real UX)

### Side-quests caught during implementation

1. **`syncDayEntryTags` inlined.** Originally planned as a separate exported function. While implementing, I extracted it into a helper that took a `ClientWithRequest` shim type — which stripped the SDK's `<DirectusSchema>` generic and broke type inference on `readItems('day_entries_tags', ...)` (the SDK collapses unknown collection names to `never`). Fix: inline the sync logic into `upsertDayEntry` so it shares the typed SDK client. Net: one fewer export, one fewer type, ~20 fewer LOC. The diff-and-sync algorithm is the same.

2. **Filter operators stay `as never`.** Same SDK typing gap from Step 1: `_in` / `_gte` / `_lte` on string-typed fields are typed `never`. Cast narrowly + comment.

3. **Test mock-call order matters.** My first take on the M2M sync test set up 6 sequential mock returns in the wrong order — I had assumed sync would read junction-rows BEFORE updating the day_entry score, but the impl does score-update first (no functional reason; just code flow). Two ways to reconcile: reorder the impl or reorder the mocks. Picked the latter — mocks now match the impl's natural sequence (read existing → update score → read junction → delete → create → re-read).

4. **`directusRowAt` test helper needed widened `note` type.** Defaulting to `note: null` made the literal type narrow; when one test wanted `note: 'existing'` the spread didn't widen. Fix: `null as string | null` at the helper's return.

### Evidence — verify pipeline

```
> npm run verify
✓ ESLint clean
✓ tsc --noEmit clean
✓ Test Files  32 passed (32)
  Tests  432 passed (432)
```

### Evidence — full Playwright suite

```
30 passed (chromium e2e) — no regression from Step 3
+ api project + live-stack day-entries.spec.ts (skip-if-no-token)
```
