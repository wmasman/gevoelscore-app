# Step 1: Inline tag creation

**Estimated time:** ~3 hours
**Test layers:** Vitest unit tests for the new lib function and the extended `validateTagLabel`; Vitest route handler tests for the new API route; Vitest component tests extending the existing `tag-category-list.test.tsx`; one Playwright e2e for the score-only-path regression check.
**Risk:** Low-to-medium. The lib + route are straightforward. The component edit touches a brainfog-sensitive surface (the daily tag picker) — the score-only-path regression test is the guardrail. **Post-audit (2026-06-01):** plan revised to drop a partial-success API contract, add reactivation-column reset, name a TOCTOU follow-up, fix the optimistic-UI shape, and extend the shared label validator with a max-length cap.
**Prerequisite:** None. Builds on the existing Tag domain ([features/tag/](../tag/)), the existing `useDayEntryUpsert` hook, and the existing `TagCategoryList` component.

> Add an inline `+ nieuw` chip to each expanded category in the daily tag picker. Tapping it reveals a label input + `Toevoegen` button. Saving creates (or dedup/reactivates) the tag server-side, then chains into the existing day-entries write path to attach the tag to today's entry. The empty-state "Geen tags hier nog" message is replaced by the input itself, so no dead-ends.

---

## Acceptance criteria

Mirrors the README's feature-level criteria, restated here so `/build-step` has a checklist. AC labels match the README where possible; numbering is sequential.

- [ ] **AC1: `+ nieuw` chip renders** at the end of every expanded category's chip row (4 primary + 4 extra categories = 8 places). Same size/shape as other chips, outline-only with a `+` glyph. Has `aria-label="Voeg tag toe aan {category}"`.
- [ ] **AC2: Disabled gate respected.** When `disabled={true}` (no score committed yet), the `+ nieuw` chip is disabled with `disabled:opacity-60`. Same gate as the existing tag chips.
- [ ] **AC3: Tap reveals inline input.** Clicking `+ nieuw` swaps the chip for an inline text field with placeholder "Nieuwe tag", a `Toevoegen` button, and an implicit Cancel via Escape / blur. Focus moves into the input on reveal. Input has `aria-label="Nieuwe tag"`.
- [ ] **AC4: Submit triggers.** Enter key submits, `Toevoegen` button submits, Escape cancels, blur (clicking outside) cancels. Empty / whitespace-only label is a no-op (do not submit). Blur-vs-Toevoegen-click race is solved by `onMouseDown` `preventDefault` on the Toevoegen button (m2 audit fix).
- [ ] **AC5: Category inheritance.** The new tag's category is the section the `+ nieuw` chip was in. No category picker.
- [ ] **AC6: Server-side dedup (4 branches + reactivation column reset).**
  - Trim whitespace before comparing.
  - Case-insensitive **exact** match within the same category. Directus has no `_iequals` operator (confirmed 2026-06-01 against the [Directus filter-rules docs](https://github.com/directus/docs/blob/main/content/guides/04.connect/2.filter-rules.md) and the programmeerprobeer reference). Implementation: filter with `_icontains` as a coarse case-insensitive query, then post-filter in JS for exact equality on the lowercased trimmed label. Match → return existing id; if it's archived, reactivate it (see AC6b).
  - Same label in a different category → create as a new tag.
  - No match → create fresh.
- [ ] **AC6b: Reactivation resets stale columns (B2 audit fix).** When a matched row is archived and is being reactivated, the PATCH sets `archived_at = null` AND `project_id = null` AND `usage_count = 0`. `created_at` is left untouched (the row's history is preserved). This prevents stale `project_id`/`usage_count` from a previous lifetime resurfacing silently. Documented in the function's TSDoc.
- [ ] **AC7: Two clean save events (B1 audit fix).** The new POST route does ONE thing: create-or-upsert a tag. It does NOT attach to a day_entry. The client performs the attach by calling the existing `PUT /api/day-entries/[date]` with the new tag-id appended to `tag_ids`. Both saves report through the existing `useReportSaveStatus('tags', …)` channel. No partial-success body shape, no `attach_error` field. The "single round trip" wording from the README is interpreted as "one user-visible save status, not one HTTP request" — and the existing save-status channel already coalesces.
- [ ] **AC8: Empty-category state replaced.** The "Geen tags hier nog" copy is removed from the empty branch in `TagCategoryList`. An empty expanded category shows only the `+ nieuw` chip. The `copy.daily.tags.empty` key is removed from [src/copy.ts](../../../src/copy.ts) once nothing references it.
- [ ] **AC9: Pending-chip UI during save (M3 audit fix).** On submit, the input collapses into a "pending chip" (`data-pending="true"`, label-as-typed visible, dimmed, no id, `aria-disabled="true"`). When the create response lands, the pending chip is replaced by a real chip with the returned id and `aria-pressed="true"`. On server error, the pending chip is removed and the input re-opens with the typed label preserved for retry. This avoids the "add-by-id-before-id-exists" impossibility in the previous draft.
- [ ] **AC10: Focus management on save.** On success, the input collapses; focus moves to the newly-created chip (so screen-reader users get audible feedback and keyboard users keep their place). The pending chip's focus state forwards to the real chip after replacement to avoid a focus drop mid-replacement.
- [ ] **AC11: Score-only path is unaffected.** A user who taps a score on Vandaag and dismisses the popout without expanding any category takes exactly the same number of taps and renders no extra DOM nodes compared to before this feature. Verified by a regression test.
- [ ] **AC12: Verify gate green.** `npm run verify` (lint + typecheck + Vitest) passes. No new lint disables. No new TypeScript `any`.
- [ ] **AC13: Label has bounded length AND a 2-word maximum (M4 audit fix + 2026-06-01 user constraint).** `validateTagLabel` is extended with two new error codes:
  - `'too_long'` — trimmed length > `MAX_TAG_LABEL_LENGTH` (40 chars). Sanity bound to prevent pathological input.
  - `'too_many_words'` — trimmed label has > 2 whitespace-separated tokens. The primary user-facing constraint. Matches the existing seeded vocabulary (tags are nouns or 2-word noun phrases like "fysiotherapie", "minder slapen", "naar fysio").
  Both caps are exported as constants (`MAX_TAG_LABEL_LENGTH`, `MAX_TAG_LABEL_WORDS`). Existing call sites (tag composer in admin path) inherit both. The UI surfaces a friendly Dutch error per code: `"Max 2 woorden"` for `too_many_words`, `"Te lang"` for `too_long`.

---

## Technical constraints

- **No new dependency.** Uses the existing Directus SDK, the existing Tag domain validators ([src/lib/domain/tag-label.ts](../../../src/lib/domain/tag-label.ts), [src/lib/domain/tag-category.ts](../../../src/lib/domain/tag-category.ts)), and the existing API-route patterns from [src/app/api/day-entries/](../../../src/app/api/day-entries/).
- **No admin / static token is used by the route.** The new POST route follows the exact pattern of the existing day-entries read route: validate the `gs_session` cookie → `getValidatedSession` returns the user's Directus access token → pass that token into `createOrUpsertTag(session.accessToken, …)`. Directus enforces collection permissions based on the user's role at the moment of the call. The frontend Fly app's scoped service token ([[project-scoped-directus-token]]) is unchanged — it remains `frontend_sessions`-only and is NOT used by this route.
- **Today's permission model.** Willem's user is `Administrator` in Directus, so his session token has CRUD on `tags` by default. The route works without any Directus permission change today.
- **Forward-looking (multi-user).** When the user table grows beyond Willem, the per-user role applied to non-admin users MUST include `tags: read, create, update` (no delete needed for this feature — archive is the delete path). Documented here so the future role-setup script doesn't omit it.
- **Audit logging is free (m3 audit fix).** Every Directus SDK call through `session.accessToken` is recorded by Directus's built-in `directus_activity` collection (with corresponding `directus_revisions` rows for create/update). This includes the tag create, the reactivation PATCH, and the day-entry tag-attach. **No custom audit-log code is required.** The TODO(I3) note in [docs/compliance/gdpr-art9.md §5](../../compliance/gdpr-art9.md) is misleading on this row and is flagged as a separate small follow-up (see "Follow-ups" below).
- **Reuse Tag validators.** Label and category go through the extended `validateTagLabel` and `validateTagCategory` before any Directus call.
- **Status reporting.** The component reuses `useReportSaveStatus('tags', …)`. Both the create-or-upsert call and the subsequent day-entry PUT report through the same channel; the user sees one Saving → Saved transition.
- **No new schema columns.** Schema unchanged — `user_owner` is a future feature (see [features/tag-intelligence/](../tag-intelligence/)). New tags created here are implicitly owned by Willem; future multi-user migration is a backfill.
- **Rate limit (M2 audit fix).** State-changing route — apply origin check + 60 req / 5 min / IP using a new `tagWriteRateLimiter` in `stores.ts`. Matches `dayEntryWriteRateLimiter`'s budget. 30/5min from the pre-audit draft was too tight.
- **TOCTOU on dedup (M1 audit fix).** Read-then-write dedup has a race window when two simultaneous creates of the same label arrive. For a single-user PWA today: functionally impossible (one client). For tomorrow: a DB-level unique index on `(category, lower(trim(label)))` is the correct fix. Named in the test list and tracked in `docs/audits/OPEN.md` as a follow-up.
- **LOC budget:** ~120 lines added to `src/components/tag-category-list.tsx`, ~80 lines for the new lib function, ~80 lines for the new route (smaller after dropping attach), ~15 lines added to `tag-label.ts` for the max-length cap, plus tests.

---

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | **Yes** | Origin check, session-validated, rate-limited, input-validated. Mirrors the day-entries write route. |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | Uses existing `tags` collection. |
| New dependency | ADR or step rationale | No | Reuses Directus SDK + existing primitives. |
| `dangerouslySetInnerHTML` usage | A03 | No | — |
| New env var with a secret | A02, A05 | No | — |
| New telemetry / observability dep | Cardinal "no telemetry" | No | — |
| User input written to DB | A03 input validation | **Yes** | Label validated via extended `validateTagLabel` (trim, non-empty, max-2-words, max-40-chars sanity bound); category enum-checked. |
| State-changing endpoint | Audit M-H series | **Yes** | Origin check + 60/5min rate limit + session validation. |
| Audit logging for Art 9 writes | GDPR Art 9 §5, NEN 7510 | **Yes — satisfied by Directus built-in** | `directus_activity` + `directus_revisions` log every create/update/PATCH via SDK with `session.accessToken`. No custom code. Compliance-doc row needs separate small update (see Follow-ups). |

---

## Plan

### 1.0 Extend `src/lib/domain/tag-label.ts`

Add both a length cap and a word-count cap. The current validator only handles `wrong_type` and `empty`.

```ts
export const MAX_TAG_LABEL_LENGTH = 40;       // sanity bound
export const MAX_TAG_LABEL_WORDS = 2;         // user-facing constraint
export type TagLabelError =
  | 'wrong_type'
  | 'empty'
  | 'too_long'
  | 'too_many_words';

export function validateTagLabel(input: unknown): ValidateTagLabelResult {
  if (typeof input !== 'string') return { ok: false, error: 'wrong_type' };
  const trimmed = input.trim();
  if (trimmed.length === 0) return { ok: false, error: 'empty' };
  if (trimmed.length > MAX_TAG_LABEL_LENGTH) return { ok: false, error: 'too_long' };
  // Word count: split on any run of whitespace. Hyphens / dashes are kept
  // inside the word (matches Dutch convention: "post-COVID" is one word,
  // "minder slapen" is two).
  const wordCount = trimmed.split(/\s+/).length;
  if (wordCount > MAX_TAG_LABEL_WORDS) return { ok: false, error: 'too_many_words' };
  return { ok: true, value: trimmed };
}
```

Shared validator — the existing tag composer in the admin UI inherits both caps. Verify no existing seeded tag exceeds 2 words OR 40 chars before changing (one-shot script: read tags from Directus, assert all current labels pass the new validator — would catch a regression where 1.363 days of habit conflicts with the new rule). If any existing tag fails, decision needed: edit the seed value, raise the cap, or change the rule.

### 1.1 Extend `src/lib/api/tags.ts`

Add a `createOrUpsertTag` function alongside the existing `readAllTags`. Shape:

```ts
export type CreateOrUpsertTagInput = {
  label: string;   // un-trimmed; trimming is done inside, before validation + dedup
  category: TagCategory;
};

export type CreateOrUpsertTagOutcome =
  | { kind: 'created'; tag: Tag }
  | { kind: 'matched_active'; tag: Tag }
  | { kind: 'matched_reactivated'; tag: Tag };

export type CreateOrUpsertTagError =
  | 'invalid_label'   // includes too_long
  | 'invalid_category'
  | 'network_error'
  | 'directus_error';

export async function createOrUpsertTag(
  accessToken: string,
  input: CreateOrUpsertTagInput,
): Promise<Result<CreateOrUpsertTagOutcome, CreateOrUpsertTagError>>;
```

Logic:
1. Trim `label`, validate via the extended `validateTagLabel`. Reject `invalid_label` on `wrong_type`, `empty`, or `too_long`.
2. Validate `category` via `validateTagCategory`. Reject `invalid_category` if not OK.
3. Query Directus `tags` with **`filter: { category: { _eq }, label: { _icontains: trimmed } }`** plus a JS post-filter for `row.label.toLowerCase() === trimmed.toLowerCase()`. Directus has no `_iequals` operator; this is the canonical Directus pattern for exact case-insensitive matching (see programmeerprobeer's `tvoo_frontend/src/lib/editorial/author-matching.ts` and `tvoo_frontend/src/lib/directus/search.ts` for sibling-project precedent). Limit 50 so `_icontains` substring false positives don't push the actual exact match off the result page in the small tags collection (~83 rows).
4. If a match exists:
   - If `archived_at !== null`: PATCH the row with `{ archived_at: null, project_id: null, usage_count: 0 }` (B2 audit fix). Return `matched_reactivated` with the fully-updated tag. Document the column-reset list in TSDoc.
   - Else: return `matched_active` with the existing tag.
5. If no match: POST a new row, return `created` with the new tag.
6. Wrap network/directus errors per the existing pattern.

### 1.2 New route `src/app/api/tags/route.ts`

POST handler — **single-purpose, no attach (B1 audit fix)**.

```
// POST /api/tags
// Body: { label: string, category: TagCategory }
// 200: { outcome: 'created'|'matched_active'|'matched_reactivated', tag: Tag }
// 400: invalid input (with sub-code: invalid_label | invalid_category | malformed_body)
// 401: no/invalid session
// 403: bad origin
// 429: rate-limited
// 502: directus_error
```

Order of operations (mirrors `day-entries/route.ts`):

1. `validateOrigin(req, 'POST')` → 403 if mismatched.
2. `parseSessionCookie(req)` → 401 if missing.
3. `getValidatedSession(sessionId)` → 401 if not valid.
4. Rate-limit by IP via `tagWriteRateLimiter` → 429 with `retry_after_ms` if exceeded.
5. Parse + validate JSON body. Schema: `label: string`, `category: TagCategory`. Reject 400 `malformed_body` on shape errors.
6. Call `createOrUpsertTag(session.accessToken, { label, category })`. Map errors:
   - `invalid_label` → 400 with sub-code
   - `invalid_category` → 400 with sub-code
   - `network_error` / `directus_error` → 502
7. Respond 200 with `{ outcome, tag }`.

**The route does NOT touch `day_entries`** — that's the client's job via the existing PUT path. This removes ~30 lines of duplicated junction-write code and avoids the partial-success contract trap.

### 1.3 New rate-limit bucket in `src/lib/auth/stores.ts`

```ts
export const tagWriteRateLimiter = createIpRateLimiter({
  max: 60,
  windowMs: 5 * 60 * 1000,
});
```

Matches `dayEntryWriteRateLimiter`'s budget (M2 audit fix). The existing sweep guard handles cleanup.

### 1.4 Edit `src/components/tag-category-list.tsx`

Two-request flow with a pending-chip UI:

1. After the existing `tags.map(...)`, append a `+ nieuw` `<button>` (always rendered, regardless of `tags.length`). The `tags.length === 0` empty branch no longer renders the "empty" copy — the `+ nieuw` chip is shown alone.
2. Local state: `composing: { category: TagCategory; label: string; status: 'idle' | 'pending' | 'error' } | null`.
3. On click of `+ nieuw`: set `composing = { category, label: '', status: 'idle' }`. Render an `<input aria-label="Nieuwe tag">` + `<button>Toevoegen</button>` in place of the chip. Use `onMouseDown` `preventDefault` on Toevoegen to defeat the blur-vs-click race (m2 audit fix). Focus moves into the input.
4. On submit (Enter or Toevoegen): trim, no-op if empty. Set `composing.status = 'pending'` AND render a "pending chip" inline (the chip row layout swaps input → pending chip; the input is hidden during pending). The pending chip has `data-pending="true"`, the typed label visible, dimmed via `opacity-60`, `aria-disabled="true"`, no id.
5. Two-step save (chained):
   a. POST `/api/tags` with `{ label, category }`. On success, get back `{ outcome, tag }`.
   b. Append `tag.id` to the current `selected` Set. Call the existing `save({ tag_ids: Array.from(nextSet) }, { flush: true })` (same path the chip-toggle uses). This second call goes through `useDayEntryUpsert` which PUTs `/api/day-entries/[date]`.
   c. Replace the pending chip with a real chip for `tag.id`, `aria-pressed="true"`. Move focus to the new chip. Clear `composing`.
6. On either-step error: set `composing.status = 'error'`, remove the pending chip, re-open the input with the typed label preserved. The existing `useReportSaveStatus('tags', …)` channel surfaces the error in the header save-status (M3 + B1 audit fix).
7. Escape key in input → clear `composing`. Blur on input → clear `composing` ONLY if `composing.status === 'idle'` (don't cancel a pending save).

### 1.5 Remove dead `empty` copy key

Once nothing references `copy.daily.tags.empty`:
- Remove the key from [src/copy.ts](../../../src/copy.ts).
- Update [src/__tests__/copy.test.ts](../../../src/__tests__/copy.test.ts) — verify the snapshot lock's exact form (a single-key removal versus a whole-object diff). If it's a key-presence assertion, remove that one line. If it's a full-object snapshot, regenerate.

### 1.6 Track follow-ups in `docs/audits/OPEN.md`

Add two checkbox entries:
- [ ] **Unique index on `tags(category, lower(trim(label)))`** — closes the TOCTOU race window in `createOrUpsertTag`. Schema migration via `directus/scripts/`. Tracked as M1 from the 2026-06-01 inline-tag-creation audit.
- [ ] **gdpr-art9.md §5 audit-log row** — update from `Placeholder TODO(I3)` to `Satisfied by directus_activity + directus_revisions (built-in)`. Tracked as m3 from the same audit.

---

## Test list (RED-first)

Every test below must be **named and failing** before the corresponding code is written. Per [.claude/testing.md](../../../.claude/testing.md).

### Domain: extend `src/lib/domain/__tests__/tag-label.test.ts`

- [ ] `validateTagLabel rejects labels exceeding MAX_TAG_LABEL_LENGTH with 'too_long'` — 41-char string returns `{ ok: false, error: 'too_long' }`.
- [ ] `validateTagLabel accepts labels at exactly MAX_TAG_LABEL_LENGTH` — 40-char string returns `{ ok: true, value }`.
- [ ] `validateTagLabel trims before length check` — `"   " + 38×'a' + "   "` is 44 chars input but 38 trimmed, returns OK.
- [ ] `validateTagLabel rejects 3-word labels with 'too_many_words'` — `"naar de fysio"` returns `{ ok: false, error: 'too_many_words' }`.
- [ ] `validateTagLabel accepts 1-word and 2-word labels` — `"hoofdpijn"` OK; `"minder slapen"` OK.
- [ ] `validateTagLabel treats multiple internal spaces as a single separator` — `"minder    slapen"` is 2 words, returns OK.
- [ ] `validateTagLabel treats hyphenated tokens as one word` — `"post-COVID"` returns OK (1 word). `"post COVID symptomen"` returns `too_many_words` (3 words).
- [ ] `validateTagLabel checks length cap before word count` — a 50-char single word fails with `too_long`, not `too_many_words`. Error precedence is `too_long` > `too_many_words` (length is the harder bound).
- [ ] `validateTagLabel checks the seeded tag set` (one-time guard, can be a separate test or a script) — every currently-seeded tag label passes the new validator. If any fails, the test fails loudly so the constraint is reconciled before shipping.

### Lib: `src/lib/api/__tests__/tags.test.ts` (new)

- [ ] `createOrUpsertTag trims whitespace before comparing` — `"  Pacing  "` matches existing `"Pacing"`, no duplicate created.
- [ ] `createOrUpsertTag matches case-insensitively within category via _icontains + JS exact-match post-filter` — `"PACING"` matches existing `"pacing"` in same category, returns `matched_active`. Asserts the filter shape uses `_icontains` (the only documented case-insensitive Directus operator).
- [ ] `createOrUpsertTag post-filters _icontains substring false positives` — a tag labelled `"pacing-strategy"` exists; a request for `"pacing"` does NOT match it; a fresh tag is created instead.
- [ ] `createOrUpsertTag does NOT match across categories` — `"Paracetamol"` in `interventie` + `"Paracetamol"` in `custom` produces two distinct tags.
- [ ] `createOrUpsertTag reactivates archived tag and clears stale columns` — archived row with `project_id: 'p-1'` and `usage_count: 17` becomes `{ archived_at: null, project_id: null, usage_count: 0 }`; returns `matched_reactivated`. (B2 audit fix.)
- [ ] `createOrUpsertTag creates new tag when no match` — no existing match → POST → returns `created`.
- [ ] `createOrUpsertTag rejects empty / whitespace-only label` → `invalid_label`.
- [ ] `createOrUpsertTag rejects too-long label` → `invalid_label` (with the underlying `too_long` domain error).
- [ ] `createOrUpsertTag rejects too-many-words label` → `invalid_label` (underlying `too_many_words` domain error). E.g. `"naar de fysio"` rejected.
- [ ] `createOrUpsertTag rejects invalid category` → `invalid_category`.
- [ ] `createOrUpsertTag surfaces network errors` → `network_error`.
- [ ] `createOrUpsertTag surfaces directus errors` → `directus_error`.
- [ ] `createOrUpsertTag concurrent calls with same label may produce duplicates (TOCTOU known limit)` — explicitly names the M1 race: two simultaneous calls with the same `(category, label)` and no existing row may both return `created` with distinct ids. Test asserts the function does NOT crash on this pattern; documents the limit until the DB-level unique index lands. Comment in the test references `audits/OPEN.md`.

### Route: `src/app/api/tags/__tests__/route.test.ts` (new)

- [ ] `POST /api/tags happy path` — valid session + body → 200 with `{ outcome: 'created', tag }`. No call to day_entries.
- [ ] `POST /api/tags rejects bad origin` — origin not in allowlist → 403, no Directus call.
- [ ] `POST /api/tags rejects missing session cookie` → 401.
- [ ] `POST /api/tags rejects invalid session` → 401.
- [ ] `POST /api/tags rate-limits at the 61st request in 5 min from same IP` → 429 with `retry_after_ms`.
- [ ] `POST /api/tags rejects malformed body` — missing `label` or `category` → 400 `malformed_body`.
- [ ] `POST /api/tags rejects invalid label` — empty / too long / too many words → 400 `invalid_label` (route's `invalid_label` sub-code, regardless of which underlying domain error fired).
- [ ] `POST /api/tags rejects invalid category` → 400 `invalid_category`.
- [ ] `POST /api/tags returns matched_active outcome unchanged` — happy path for the dedup branch.
- [ ] `POST /api/tags returns matched_reactivated outcome` — archived tag reactivation propagates through the route.

### Component: extend `src/components/__tests__/tag-category-list.test.tsx`

- [ ] `+ nieuw chip renders at end of each expanded category` — count = tags + 1, last button has `aria-label="Voeg tag toe aan {category}"`.
- [ ] `+ nieuw chip is disabled when component is disabled`.
- [ ] `Tapping + nieuw reveals the input and Toevoegen button` — focus moves into input.
- [ ] `Empty category shows + nieuw chip and no "empty" copy` — no "Geen tags hier nog" text in the DOM.
- [ ] `Enter in input triggers submit` — POSTs to /api/tags with trimmed label + section's category.
- [ ] `Toevoegen button triggers submit` — same as Enter. Click does NOT race with blur (onMouseDown preventDefault).
- [ ] `Escape cancels` — composing state clears, chip returns, typed label discarded.
- [ ] `Blur cancels when status is idle, NOT when pending` — clicking outside while pending does not cancel mid-save.
- [ ] `Whitespace-only submit is a no-op` — does not POST; composing stays open.
- [ ] `Pending chip renders during save with data-pending attribute and dimmed style` — assertable by `data-pending="true"` + opacity class; no id present in the DOM yet (M3 audit fix).
- [ ] `Successful save replaces pending chip with real chip, aria-pressed=true, focus moves to it` — combined visual+focus assertion.
- [ ] `Tag-create error reopens input with label preserved` — pending chip removed; input visible with the typed label retained for retry.
- [ ] `Day-entry PUT error after successful tag create leaves the tag selectable but reverts day_entries_tags optimistic state` — uses the existing `lastSavedRef` pattern (the new chip is real, but the join didn't persist).
- [ ] `Dedup happy path: matched_active outcome simply selects the existing chip` — no new chip rendered; existing chip becomes `aria-pressed="true"`.
- [ ] `Reactivated tag becomes visible after matched_reactivated` — previously archived (not rendered) tag now appears in the chip row.

### E2E regression: `tests/e2e/score-only-path.spec.ts`

- [ ] `Score-only path unaffected` — open Vandaag popout, tap a score, close. Assert: no extra network calls beyond the score save, no `+ nieuw` chip rendered without expanding a category, tap count is unchanged versus a baseline snapshot.

---

## Done-when

- [ ] All test files above are written **first**, all RED.
- [ ] Implementation lands in the five code locations: domain (`tag-label.ts`), lib (`tags.ts`), route (`api/tags/route.ts`), stores (`stores.ts`), component (`tag-category-list.tsx`).
- [ ] All tests GREEN.
- [ ] `npm run verify` clean — no new lint warnings, no new TS errors.
- [ ] `powershell -ExecutionPolicy Bypass -File scripts/run-auth-smoke.ps1` PASSES (route handler touches auth-adjacent code paths; smoke is the integration guardrail).
- [ ] Manual check on the dev server:
  - Expand each of the 8 categories — `+ nieuw` chip present in each.
  - Create a tag in two categories (one happy-path, one whitespace-padded to test dedup visually).
  - Verify (i) pending chip renders during save, (ii) replaced by real chip on success, (iii) auto-selected, (iv) survives reload, (v) save-status visible in the header.
  - In Directus admin: open `directus_activity` and confirm a `create` (or `update` for reactivation) row appears for the tag — audit-log verification.
- [ ] `docs/audits/OPEN.md` has the two new follow-up checkboxes (unique index, gdpr-art9.md row).
- [ ] All 13 README + step ACs ticked.

---

## Follow-ups (tracked separately, not part of this step)

- **Unique index on `tags(category, lower(trim(label)))`** — closes M1 TOCTOU. `directus/scripts/`. Tracked in `docs/audits/OPEN.md`.
- **gdpr-art9.md §5 audit-log row correction** — change the `Placeholder TODO(I3)` text to reflect the built-in `directus_activity` reality. One-line edit, not blocking.
- **Scoping the Directus permissions of future non-admin users** — when multi-user lands, the per-user role MUST include `tags: read, create, update`. Not actionable today; flagged in [features/tag-intelligence/](../tag-intelligence/) "Per-user tag universe".

---

## Out of scope of this step

- Recent-tags-first sorting (deferred to [features/tag-intelligence/](../tag-intelligence/)).
- Tag inference from notes (deferred — needs the locality/privacy brainstorm).
- Merge / rename / archive UX (deferred — Tag intelligence vision).
- DB-level unique index (follow-up above).
- An admin UI for un-archiving without re-typing the label.
