# Step 2: Episodes API surface

**Estimated time:** ~3.5 hours
**Test layers:** Vitest unit on the new `src/lib/api/episodes.ts` (SDK mocked); Vitest unit on `src/app/api/episodes/route.ts` and `[id]/route.ts` (`vi.mock` of stores + getValidatedSession, full status-code + cookie coverage); Playwright API integration suite at `tests/api/episodes.spec.ts` (real HTTP, unhappy paths + rate-limit enforcement). No component tests yet — UI lands in step-3.
**Risk:** Low–medium. New code paths only; no migration; the schema is forward-compatible. The Tag domain extension landed in step-1 so existing read paths through `readAllTags` already include `parent_episode_id` and have not regressed.
**Prerequisite:** Step-1 GREEN + deployed migration (`ffabdf3` + `36fdadb`). The `episodes` collection exists in production Directus and the domain validators are committed.

> SDK wrapper + Next.js Route Handlers for the `episodes` collection. Mirrors `lib/api/tags.ts` and the `/api/day-entries` route family one-for-one — same shape, same gates, same Result returns. **No UI yet** — step-3 introduces the Periodes tab and renders the data. Step-2 ends GREEN with auth-smoke + a new episodes-smoke confirming the new endpoints work against live Fly Directus.

## Audit findings (logged before build)

Step-2 was audited against `CLAUDE.md`, `.claude/conventions.md`, `.claude/security-checklist.md`, and `.claude/testing.md` on 2026-06-02. Two convention drifts were found between the project rules and the existing codebase. Step-2 matches the existing-code pattern in both cases; these are flagged so they get a deliberate resolution (update rule, or commit to a refactor) — not silently absorbed:

- **Unicode emojis in scripts.** `CLAUDE.md` says NEVER. Every existing `directus/scripts/*.mjs` uses `⏩ ➕ ✅ ──`. Step-2's new scripts (`setup-episodes-permissions.mjs`, `episodes-smoke.mjs`) match existing convention. **Action**: update `CLAUDE.md` (or remove the rule) so doc and code agree. Tracked outside this step.
- **Zod at API boundaries.** `.claude/conventions.md` says "External data ... validated at the boundary with Zod schemas in `src/lib/validation/`". Existing code (`tags.ts`, `day-entries.ts`) uses domain validators, no Zod imports anywhere in the project. Step-2 matches existing-code pattern. **Action**: either drop the Zod sentence from `conventions.md` or open a refactor ticket for the API-boundary upgrade. Tracked outside this step.

Three concrete plan improvements landed from the audit and are now in this file (search "AC9a", "AC5a", "Error responses do not echo input back" for the resolutions):
- AC9a: UUID-format validation on the `[id]` path param before the SDK call.
- AC5a: 10K server-side cap on `description` via new `validateEpisodeDescription`.
- "Error responses do not echo input back" added to Technical constraints.

---

## API surface (resolved before drafting)

The shape was selected by mirroring the existing surface. The decisions:

| Concern | Decision | Reason |
|---|---|---|
| Update verb | **PATCH /api/episodes/[id]** with a partial body | Episodes have an internal UUID, not a natural key — REST PATCH is the right semantics. day-entries uses PUT because date IS the natural key (upsert-by-date) and the contracts differ. |
| Archive endpoint | **Field-write via PATCH**, no separate `/archive` endpoint | Archive is `archived_at: <ISO timestamp>`; un-archive is `archived_at: null`. Same model as tags-reactivation. Avoids fan-out of endpoints for what is one column write. |
| Hard delete | **Not exposed in the API.** Directus admin UI only | Per the README §Out of scope. `archived_at` is the only deletion semantics the UI surface knows about. |
| List filter | `GET /api/episodes` returns ACTIVE only by default; `?archived=all` includes archived | Mirrors the `tags` read pattern (`filter[archived_at][_null]=true`). The "afgerond" group in the Periodes list view is non-null `end_date` but non-null `archived_at` is the separate "archived" state. Match what the UI actually needs. |
| Sort | `start_date` DESC | Most recent first. Stable. The list view in step-3 will additionally sort active-before-archived in the client. |
| Single-item GET | **Not in step-2.** | The list returns the whole set (tens of rows max in v1). The client can filter. Defer GET /api/episodes/[id] until a real caller appears. |
| Linked tags | **Not embedded in episode response.** | Tags-with-`parent_episode_id` are read via the existing `readAllTags` server-render path (now returning the new column). The Periodes detail view filters in the client. No N+1 fetch on episode list. |
| Rate limit | Two new tiered limiters: `episodeReadRateLimiter` (120 / 5 min / IP, same as day-entry reads) and `episodeWriteRateLimiter` (30 / min / IP, same as tag/day-entry writes) | Same posture as the rest of the app. Defence-in-depth against a leaked session cookie. |
| Auth | Session cookie → sessionId → `getValidatedSession` → `session.accessToken` passed to the SDK wrapper. Directus enforces collection permissions | Same as every other API route. The single-user permissions on `episodes` are set up below in §1.5. |

---

## Acceptance criteria

- [ ] **AC1: `src/lib/api/episodes.ts` exists** with three exported functions, all Result-shaped:
  - `readAllEpisodes(accessToken, opts?: { includeArchived?: boolean }): Promise<Result<Episode[], EpisodesError>>`
  - `createEpisode(accessToken, input: CreateEpisodeInput): Promise<Result<Episode, CreateEpisodeError>>`
  - `updateEpisode(accessToken, id, patch: UpdateEpisodePatch): Promise<Result<Episode, UpdateEpisodeError>>`
- [ ] **AC2: `CreateEpisodeInput` is the minimal write shape**: `{ label, category, start_date, end_date?, description? }`. Server fills id, created_at, updated_at, calendar_binding (null), archived_at (null). Every field is validated by the existing domain validators before the SDK call.
- [ ] **AC3: `UpdateEpisodePatch` is a partial of `CreateEpisodeInput` PLUS `archived_at`**: any non-empty subset of `{ label, category, start_date, end_date, description, archived_at }`. Empty patch → `empty_patch` error (400). Whichever fields are present run their domain validator. **True PATCH semantics** — sending only one of `start_date` / `end_date` is allowed; the wrapper reads the current row, merges, and validates the date range against the merged candidate (see AC3a).
- [ ] **AC3a: Date-range validation on partial PATCH**: when either `start_date` or `end_date` is in the patch (but not both), the wrapper performs a read-before-write: it fetches the current row, fills in the absent half from the DB value, validates the merged pair via `validateDateRange`, and only then PATCHes. If the merged pair is invalid → `invalid_date_range`, no write. If the read itself fails (404 / network) the error is mapped accordingly. The wrapper only sends to Directus the keys the caller put in the patch — the read is purely for validation, not echoed back.
- [ ] **AC4: `archived_at` semantics on PATCH**: setting it to an ISO timestamp archives; setting it to `null` un-archives. Any other shape → `invalid_request`.
- [ ] **AC5: `calendar_binding` cannot be written** through the API in v1.5. Domain validator enforces `=== null`; SDK wrapper never sends the field on create/update; route handler doesn't accept it in the body. The schema column exists for v1.6.
- [ ] **AC5a: `description` has a 10,000-character server-side cap.** New domain validator `validateEpisodeDescription(input)` in `src/lib/domain/episode-description.ts`. Accepts `null` (no description) OR a string ≤10,000 chars. Rejects anything else. Wrapper calls it in both create and update paths before sending to Directus. Matches the security-checklist note-length pattern (notes use the same ~10K soft cap). Defense-in-depth — the form in step-4 will also enforce client-side with a visible counter, but the API boundary rejects oversized payloads independently.
- [ ] **AC6: `GET /api/episodes` returns active episodes only by default**, sorted by `start_date` DESC. Status 200. Body shape `{ episodes: Episode[] }`. Empty result returns `{ episodes: [] }`, not 404.
- [ ] **AC7: `GET /api/episodes?archived=all` returns active AND archived**, same sort. Any other value of the query param → `invalid_request` (400). Empty query param treated as default (active only).
- [ ] **AC8: `POST /api/episodes`** validates origin + rate-limit + session + body in that order; returns 200 with `{ episode: Episode }`; returns 400 with the per-field error variant on validator failure; returns 502 on Directus error.
- [ ] **AC9: `PATCH /api/episodes/[id]`** runs the same gates; takes a partial body; on empty body returns 400 `empty_patch`; on a 404 from Directus returns 404 `not_found`.
- [ ] **AC9a: `[id]` path param is validated as a UUID-shape string** at the route handler, before the SDK wrapper is called. Non-UUID input (empty string, garbage, JS-injection probes like `javascript:alert(1)`, paths missing the dashes) → 400 `invalid_request`, no SDK round-trip. Matches the pattern set by `/api/day-entries/[date]` which validates the date param via `validateDate` before the SDK call. Defense-in-depth: even though Directus would reject a non-UUID with 404, gating at the route boundary avoids reflecting user input into error paths and saves a network round-trip on malicious probes.
- [ ] **AC10: Route handlers use the standard gate order**: origin → rate-limit → session → request validation → SDK call → error mapping. Matches `/api/day-entries/[date]` and `/api/tags`.
- [ ] **AC11: All routes validate the `Origin` and `Referer` headers** against `allowedOrigins()` for writes. GET also gated.
- [ ] **AC12: Rate limit hits return 429** with `{ error: 'rate_limited', retry_after_ms: number }`.
- [ ] **AC13: All endpoints return 401 with `{ error: 'unauthenticated' }`** when the session cookie is absent or the session resolves to null.
- [ ] **AC14: New rate-limiters wired in `src/lib/auth/stores.ts`** with the standard fixed-window pattern. Named `episodeReadRateLimiter` (120 / 5min) and `episodeWriteRateLimiter` (30 / min).
- [ ] **AC15: Directus single-user permissions for `episodes` set up** via a new idempotent script `directus/scripts/setup-episodes-permissions.mjs`. The Administrator (Willem) role gets `read`, `create`, `update`, `delete` on `episodes` with no filter; the gevoelscore-frontend service token's role gets `read`, `create`, `update` (no delete) on `episodes` with the same filter shape as the existing tag permissions (none — single-user app).
- [ ] **AC16: New episodes-smoke `scripts/episodes-smoke.mjs`** posts a test episode, reads it back, archives it via PATCH, un-archives, then PATCH-renames it, then runs the same GET assertions on `?archived=all`. Cleans up by hard-DELETE via the admin token (the smoke is allowed admin operations the UI isn't). Wrapped by `scripts/run-episodes-smoke.ps1` matching the auth-smoke pattern.
- [ ] **AC17: Existing auth-smoke continues PASS** after step-2 lands. No regression on the `/api/day-entries/today` round-trip.
- [ ] **AC18: Verify gate green.** `npm run verify` clean — lint + typecheck + Vitest (route-handler tests + lib/api tests all GREEN).
- [ ] **AC19: Playwright API tests** at `tests/api/episodes.spec.ts` cover: origin-blocked, rate-limit enforcement, malformed body, invalid query param on list, 401 without cookie, 404 on PATCH against a non-existent id.

---

## Technical constraints

- **No new dependency.** Reuses `@directus/sdk` (already present), `next/server`, and the existing auth + rate-limit primitives.
- **Stateless wrapper functions, fresh client per call.** Same shape as `tags.ts` and `day-entries.ts` — no module-level Directus client state. Avoids the "what if the access token changed" question.
- **Domain validators are the single source of truth.** Route handlers do a coarse shape check (`typeof body.label === 'string'`); the SDK wrapper feeds inputs through `validateEpisodeLabel`, `validateEpisodeCategory`, `validateDateRange`. Validators are not duplicated in the handler.
- **Result type imported from `tags.ts`** — already exported there (`export type Result<T, E> = ...`). When a third caller needs it, extract to `src/lib/api/result.ts` per the 3+ rule. Step-2 is the third; **extract it as part of this step** rather than adding a third copy.
- **No retries, no backoff.** Same as existing API code. The user retries from the UI if a network blip eats a request.
- **`updated_at` is server-managed** via the `date-updated` special — the wrapper never sends it on create or update; Directus stamps it.
- **Permissions are LIVE-WRITTEN** by `setup-episodes-permissions.mjs` to gevoelscore-backend.fly.dev. Idempotent: each ACL gated by an existence check. The script uses admin token (same `DIRECTUS_TOKEN` env var as setup-schema scripts).
- **Empty patch is rejected** in the route handler BEFORE the SDK call. Avoids a no-op write that bumps `updated_at` for nothing.
- **Error responses do not echo input back.** `{ error: 'invalid_label' }`, never `{ error: 'invalid_label', received: '<what the user typed>' }`. Matches existing routes (`/api/tags`, `/api/day-entries`) and the security-checklist A04 "Error responses are generic" rule. Reflecting input into error paths makes the surface a tiny but real XSS vector when an error message reaches an HTML context downstream.
- **Known TOCTOU window on partial date PATCH** (read-before-write in `updateEpisode`): between the read and the PATCH a concurrent writer could change the absent half, leaving the row in an invalid `start > end` state. For v1.5 single-user / single-active-device this is vanishingly improbable, and the failure mode is loud (next read fails `validateEpisode` with `invalid_date_range`) and reversible. Optimistic concurrency control (`expected_updated_at` header → 409 on mismatch) is the textbook fix and lands alongside whichever triggers the need first: calendar webhook (v1.6), multi-user migration (v2), or sustained autosave-overlap evidence from soak.

---

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 (origin, rate-limit, auth, content-type, body size) | Yes | Full gate stack identical to `/api/tags` and `/api/day-entries`. |
| New collection storing user data (health context) | GDPR Art 9 | Yes | `episodes.description` and `episodes.label` may contain medical narrative. Same posture as `day_entries.note` — self-hosted, exports + full-delete remain first-class. |
| New env var | A02 (secrets) | No | Reuses existing `DIRECTUS_TOKEN` (for the permissions + smoke scripts) and the existing scoped service token (for the runtime API). |
| New dependency | ADR | No | Pure use of existing libraries. |
| Reduced motion / animation | WCAG 2.3.3 | No | No UI. |
| Aria labelling | WCAG 1.1.1 | No | No UI. |
| Logging contains PII | A09 (log hygiene) | Yes | The smoke script + permissions setup script must NOT print `label` or `description` content. Counts and field names only — same constraint as `add-episodes.mjs`. |
| TOCTOU (read-then-write race) | Concurrency review | No | Single-user app, single device per session. The `add-episodes` migration created no unique-by-label constraint and none is needed. |

---

## Plan

### 2.-1 New domain helper `src/lib/domain/episode-description.ts`

Small validator for the description field — enforces the 10K server-side cap. Same shape as `validateEpisodeLabel` but description-specific (nullable, no whitespace normalisation since multi-line text is valid):

```ts
// src/lib/domain/episode-description.ts
// Server-side cap on episode description text. The schema column is
// `text` (effectively unlimited); the cap is defense against accidental
// "paste a whole PDF" or malicious payloads. Matches the note-length
// soft cap from .claude/security-checklist.md.

export const MAX_EPISODE_DESCRIPTION_LENGTH = 10_000;

export type EpisodeDescriptionError = 'wrong_type' | 'too_long';

export type ValidateEpisodeDescriptionResult =
  | { ok: true; value: string | null }
  | { ok: false; error: EpisodeDescriptionError };

export function validateEpisodeDescription(
  input: unknown,
): ValidateEpisodeDescriptionResult {
  if (input === null || input === undefined) {
    return { ok: true, value: null };
  }
  if (typeof input !== 'string') {
    return { ok: false, error: 'wrong_type' };
  }
  if (input.length > MAX_EPISODE_DESCRIPTION_LENGTH) {
    return { ok: false, error: 'too_long' };
  }
  // NOTE: no trim/normalise — description is multi-line free-text;
  // preserving whitespace is intentional.
  return { ok: true, value: input };
}
```

### 2.0 Extract `Result` helper

Per the 3+ rule, today `Result` is duplicated in `tags.ts` and `day-entries.ts`. Episodes makes it the third caller. Extract to `src/lib/api/result.ts`:

```ts
// src/lib/api/result.ts
export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
```

Replace local definitions in `tags.ts` and `day-entries.ts` with an import. Verify gate must remain green; no behaviour change.

### 2.1 SDK wrapper `src/lib/api/episodes.ts`

Mirrors `tags.ts` structurally. Types first, then `readAllEpisodes`, then `createEpisode`, then `updateEpisode`.

```ts
import { createDirectus, createItem, readItems, rest, staticToken, updateItem }
  from '@directus/sdk';
import type { Episode } from '@/lib/domain/episode';
import type { EpisodeCategory } from '@/lib/domain/episode-category';
import { validateEpisode } from '@/lib/domain/episode';
import { validateEpisodeCategory } from '@/lib/domain/episode-category';
import { validateEpisodeLabel } from '@/lib/domain/episode-label';
import { validateEpisodeDescription } from '@/lib/domain/episode-description';
import { validateDateRange } from '@/lib/domain/date-range';
import type { Result } from './result';

export type EpisodesError = 'network_error' | 'directus_error';
export type CreateEpisodeError =
  | 'invalid_label'
  | 'invalid_category'
  | 'invalid_date_range'
  | 'invalid_description'
  | 'network_error'
  | 'directus_error';
export type UpdateEpisodeError =
  | CreateEpisodeError
  | 'invalid_archived_at'
  | 'not_found'
  | 'empty_patch';

export type CreateEpisodeInput = {
  label: string;
  category: EpisodeCategory;
  start_date: string;
  end_date?: string | null;
  description?: string | null;
};

export type UpdateEpisodePatch = {
  label?: string;
  category?: EpisodeCategory;
  start_date?: string;
  end_date?: string | null;
  description?: string | null;
  archived_at?: string | null;
};

type DirectusEpisodeRow = {
  id: string;
  label: string;
  category: EpisodeCategory;
  start_date: string;
  end_date: string | null;
  description: string | null;
  calendar_binding: unknown | null;
  archived_at: string | null;
  created_at: string;
  updated_at: string;
};

type DirectusSchema = { episodes: DirectusEpisodeRow[] };

function directusUrl(): string {
  return process.env.DIRECTUS_URL
    ?? process.env.NEXT_PUBLIC_DIRECTUS_URL
    ?? 'http://localhost:8055';
}

function isNetworkError(e: unknown): boolean {
  return e instanceof TypeError && /fetch/i.test(e.message);
}

function rowToEpisode(r: DirectusEpisodeRow): Episode {
  // Force calendar_binding to null per the v1.5 gate. The validator will
  // reject any non-null shape, so a corrupt DB row surfaces immediately
  // rather than being silently passed through.
  return {
    id: r.id,
    label: r.label,
    category: r.category,
    start_date: r.start_date,
    end_date: r.end_date,
    description: r.description,
    calendar_binding: null,
    archived_at: r.archived_at,
    created_at: r.created_at,
    updated_at: r.updated_at,
  };
}

export async function readAllEpisodes(
  accessToken: string,
  opts: { includeArchived?: boolean } = {},
): Promise<Result<Episode[], EpisodesError>> {
  try {
    const client = createDirectus<DirectusSchema>(directusUrl())
      .with(rest())
      .with(staticToken(accessToken));

    const filter = opts.includeArchived
      ? undefined
      : ({ archived_at: { _null: true } } as never);

    const rows = (await client.request(
      readItems('episodes', {
        ...(filter ? { filter } : {}),
        sort: ['-start_date'],
        limit: -1,
      }),
    )) as DirectusEpisodeRow[];

    return { ok: true, value: rows.map(rowToEpisode) };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    return { ok: false, error: 'directus_error' };
  }
}

export async function createEpisode(
  accessToken: string,
  input: CreateEpisodeInput,
): Promise<Result<Episode, CreateEpisodeError>> {
  const labelResult = validateEpisodeLabel(input.label);
  if (!labelResult.ok) return { ok: false, error: 'invalid_label' };

  const categoryResult = validateEpisodeCategory(input.category);
  if (!categoryResult.ok) return { ok: false, error: 'invalid_category' };

  const rangeResult = validateDateRange(input.start_date, input.end_date ?? null);
  if (!rangeResult.ok) return { ok: false, error: 'invalid_date_range' };

  const descResult = validateEpisodeDescription(input.description ?? null);
  if (!descResult.ok) return { ok: false, error: 'invalid_description' };

  try {
    const client = createDirectus<DirectusSchema>(directusUrl())
      .with(rest())
      .with(staticToken(accessToken));

    const row = (await client.request(
      createItem('episodes', {
        label: labelResult.value,
        category: categoryResult.value,
        start_date: rangeResult.value.start_date,
        end_date: rangeResult.value.end_date,
        description: input.description ?? null,
      } as never),
    )) as DirectusEpisodeRow;

    return { ok: true, value: rowToEpisode(row) };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    return { ok: false, error: 'directus_error' };
  }
}

export async function updateEpisode(
  accessToken: string,
  id: string,
  patch: UpdateEpisodePatch,
): Promise<Result<Episode, UpdateEpisodeError>> {
  const fields = Object.keys(patch);
  if (fields.length === 0) return { ok: false, error: 'empty_patch' };

  const cleaned: Record<string, unknown> = {};

  if ('label' in patch) {
    const r = validateEpisodeLabel(patch.label);
    if (!r.ok) return { ok: false, error: 'invalid_label' };
    cleaned.label = r.value;
  }
  if ('category' in patch) {
    const r = validateEpisodeCategory(patch.category);
    if (!r.ok) return { ok: false, error: 'invalid_category' };
    cleaned.category = r.value;
  }
  // Date-range branch: if either start_date or end_date is in the patch,
  // run validateDateRange against the MERGED candidate (caller value +
  // DB value for the absent half). True PATCH semantics — caller can
  // send just one date and the wrapper validates the resulting pair.
  // The "merge" only happens for validation; the PATCH itself sends
  // only the keys the caller provided. Documented in AC3 + AC3a.
  let mergedDates: { start_date: string; end_date: string | null } | null = null;
  if ('start_date' in patch || 'end_date' in patch) {
    // Read current row to fill in the absent half.
    let current: DirectusEpisodeRow;
    try {
      const readClient = createDirectus<DirectusSchema>(directusUrl())
        .with(rest())
        .with(staticToken(accessToken));
      current = (await readClient.request(
        readItems('episodes', { filter: { id: { _eq: id } } as never, limit: 1 }),
      ))[0] as DirectusEpisodeRow;
      if (!current) return { ok: false, error: 'not_found' };
    } catch (e) {
      if (isNetworkError(e)) return { ok: false, error: 'network_error' };
      const msg = String((e as { message?: string }).message ?? '');
      if (msg.includes('404') || msg.includes('FORBIDDEN')) {
        return { ok: false, error: 'not_found' };
      }
      return { ok: false, error: 'directus_error' };
    }
    const candidateStart = 'start_date' in patch ? patch.start_date : current.start_date;
    const candidateEnd = 'end_date' in patch ? (patch.end_date ?? null) : current.end_date;
    const r = validateDateRange(candidateStart, candidateEnd);
    if (!r.ok) return { ok: false, error: 'invalid_date_range' };
    mergedDates = r.value;
    // Only echo back the keys the CALLER sent — don't overwrite the
    // absent half with the value we read.
    if ('start_date' in patch) cleaned.start_date = r.value.start_date;
    if ('end_date' in patch) cleaned.end_date = r.value.end_date;
  }
  void mergedDates;  // present for the validation side-effect above
  if ('description' in patch) {
    const r = validateEpisodeDescription(patch.description);
    if (!r.ok) return { ok: false, error: 'invalid_description' };
    cleaned.description = r.value;
  }
  if ('archived_at' in patch) {
    // archived_at: null = un-archive. ISO timestamp = archive.
    if (patch.archived_at !== null) {
      if (typeof patch.archived_at !== 'string'
          || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/.test(patch.archived_at)) {
        return { ok: false, error: 'invalid_archived_at' };
      }
    }
    cleaned.archived_at = patch.archived_at;
  }

  try {
    const client = createDirectus<DirectusSchema>(directusUrl())
      .with(rest())
      .with(staticToken(accessToken));

    const row = (await client.request(
      updateItem('episodes', id, cleaned as never),
    )) as DirectusEpisodeRow;

    return { ok: true, value: rowToEpisode(row) };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    // Directus returns 403 for "row not found by FILTER" + 404 for hard
    // not-found. Map both to not_found at the wrapper boundary; the
    // route handler converts to HTTP 404.
    const msg = String((e as { message?: string }).message ?? '');
    if (msg.includes('404') || msg.includes('FORBIDDEN')) {
      return { ok: false, error: 'not_found' };
    }
    return { ok: false, error: 'directus_error' };
  }
}
```

### 2.2 Route handler `src/app/api/episodes/route.ts` (GET + POST)

Standard gate order. List query param `?archived=all` toggles `includeArchived`.

### 2.3 Route handler `src/app/api/episodes/[id]/route.ts` (PATCH)

Standard gate order. Parses the id from `context.params`, builds the patch from the body keys that are present, calls `updateEpisode`. Empty body → 400 `empty_patch`. Wrapper-level `not_found` → 404.

### 2.4 Rate-limiter wiring in `src/lib/auth/stores.ts`

Add two named exports following the existing patterns:

```ts
export const episodeReadRateLimiter = makeFixedWindowLimiter({
  windowMs: 5 * 60 * 1000,
  maxPerWindow: 120,
  name: 'episode_read',
});

export const episodeWriteRateLimiter = makeFixedWindowLimiter({
  windowMs: 60 * 1000,
  maxPerWindow: 30,
  name: 'episode_write',
});
```

(Names will match the existing `tagWriteRateLimiter` / `dayEntryReadRateLimiter` shape; the actual API surface of `makeFixedWindowLimiter` will be checked against the existing source — this is illustrative.)

### 2.5 Permissions script `directus/scripts/setup-episodes-permissions.mjs`

Adds Directus role permissions on the new `episodes` collection. Idempotent — each permission row gated by a check on `/permissions?filter[collection][_eq]=episodes&filter[role][_eq]=<role-id>&filter[action][_eq]=<action>`.

Roles:
- **Administrator** (Willem) — full CRUD, no filter.
- **gevoelscore-frontend** (scoped service-token role) — read + create + update (no delete), no filter (single-user app).

### 2.6 Smoke script `scripts/episodes-smoke.mjs` + `scripts/run-episodes-smoke.ps1`

Closed-loop integration sanity-check. Reads `WILLEM_EMAIL` + `WILLEM_PASSWORD` from `.env.local`. Cycle:

1. Login → cookie.
2. POST /api/episodes with `{ label: 'soak test', category: 'interventie', start_date: '<today>' }` → 200, capture id.
3. GET /api/episodes → assert the new episode is in the list.
4. PATCH /api/episodes/[id] with `{ description: '_smoke' }` → 200.
5. PATCH /api/episodes/[id] with `{ archived_at: '<now ISO>' }` → 200.
6. GET /api/episodes → assert the archived episode is NOT in the list.
7. GET /api/episodes?archived=all → assert it IS in the list.
8. PATCH /api/episodes/[id] with `{ archived_at: null }` → 200, un-archived.
9. Hard-DELETE via the admin token (separate request, NOT through the frontend) to clean up.
10. Logout.

### 2.7 Update `validateOrigin` / `allowedOrigins` if needed

Spot-check: no change expected. The new routes inherit the existing origin policy.

---

## Test list (RED-first)

### Unit: `src/lib/domain/__tests__/episode-description.test.ts` (new)

- [ ] `accepts null → ok with value null`
- [ ] `accepts undefined → ok with value null (coerced)`
- [ ] `accepts empty string → ok with value '' (empty description is valid, distinct from null)`
- [ ] `accepts a normal multi-line description (newlines preserved, no trim)`
- [ ] `accepts a description at exactly MAX_EPISODE_DESCRIPTION_LENGTH chars (10,000)`
- [ ] `rejects 10,001 chars with too_long`
- [ ] `rejects non-string non-null input (number, object, array) with wrong_type`

### Unit: `src/lib/api/__tests__/episodes.test.ts` (new)

Mock `@directus/sdk` via `vi.mock` exactly as `tags.test.ts` does it. Tests are organised by exported function.

**Anti-pattern guard** (per [testing.md §Anti-patterns](../../../.claude/testing.md)): each test asserts on EITHER the request shape sent to the SDK mock (filter / sort / limit / body content) OR the response-mapping logic — both halves are covered by the test list below. Tests that only assert "the mock returned what we told it" don't earn their keep and must be deleted or tightened.

**For `readAllEpisodes`:**
- [ ] `returns the empty list when Directus returns no rows`
- [ ] `returns episodes mapped through rowToEpisode (calendar_binding forced to null)`
- [ ] `default call passes archived_at: { _null: true } filter`
- [ ] `with includeArchived: true does NOT pass the filter`
- [ ] `sort is start_date DESC`
- [ ] `limit is -1 (unbounded)`
- [ ] `network error → { ok: false, error: 'network_error' }`
- [ ] `non-network SDK error → { ok: false, error: 'directus_error' }`

**For `createEpisode`:**
- [ ] `valid minimal input → POST { label, category, start_date, end_date: null, description: null }`
- [ ] `valid input with all optional fields → POST with all set`
- [ ] `invalid label → invalid_label (no SDK call)`
- [ ] `invalid category → invalid_category (no SDK call)`
- [ ] `invalid date range (end < start) → invalid_date_range (no SDK call)`
- [ ] `description as number → invalid_description (no SDK call)`
- [ ] `description >10,000 chars → invalid_description (no SDK call)`
- [ ] `network error → network_error`
- [ ] `SDK error → directus_error`
- [ ] `returned row is mapped via rowToEpisode`

**For `updateEpisode`:**
- [ ] `empty patch → empty_patch (no SDK call)`
- [ ] `partial { description } → PATCH only description (no read of current row)`
- [ ] `partial { label } → PATCH only label (no read of current row)`
- [ ] `partial { archived_at: ISO } → PATCH archives`
- [ ] `partial { archived_at: null } → PATCH un-archives`
- [ ] `partial { start_date, end_date } pair → reads current row, validates the pair, PATCHes BOTH keys`
- [ ] `partial { start_date } alone → reads current row, fills in end_date from DB, validates merged pair, PATCHes ONLY start_date`
- [ ] `partial { end_date } alone (end_date: new ISO) → reads current row, fills in start_date from DB, validates merged pair, PATCHes ONLY end_date`
- [ ] `partial { end_date: null } alone (un-complete) → reads current row, validates merged pair (start_date stays, end_date becomes null), PATCHes ONLY end_date`
- [ ] `partial { start_date: future-date } where DB end_date is in the past → merged pair fails ordering → invalid_date_range (no write attempted)`
- [ ] `partial { start_date } where the row does not exist (404 on read) → not_found (no write attempted)`
- [ ] `partial { start_date } where the read fails with network → network_error (no write attempted)`
- [ ] `partial { label: '' } → invalid_label (no read, no SDK write)`
- [ ] `archived_at as non-ISO string → invalid_archived_at`
- [ ] `archived_at as undefined (vs missing key) is rejected as invalid_archived_at`
- [ ] `SDK 404 on write → not_found`
- [ ] `network error on write → network_error`

### Unit: `src/app/api/episodes/__tests__/route.test.ts` (new)

Mock the stores + getValidatedSession + lib/api/episodes via `vi.mock`. Cover GET + POST.

**GET happy path:**
- [ ] `200 with empty list when readAllEpisodes returns []`
- [ ] `200 with the list when readAllEpisodes returns rows`
- [ ] `200 with archived included when ?archived=all`

**GET unhappy:**
- [ ] `403 forbidden when origin not allowed`
- [ ] `429 rate_limited`
- [ ] `401 unauthenticated when no session cookie`
- [ ] `401 unauthenticated when session resolves null`
- [ ] `400 invalid_request when ?archived has any other value`
- [ ] `502 server_error when wrapper returns directus_error`

**POST happy path:**
- [ ] `200 with { episode } on valid body`

**POST unhappy:**
- [ ] `403 / 429 / 401 (same as GET)`
- [ ] `400 malformed_body on non-JSON body`
- [ ] `400 invalid_label / invalid_category / invalid_date_range / invalid_description`
- [ ] `502 server_error on directus_error / network_error`

### Unit: `src/app/api/episodes/[id]/__tests__/route.test.ts` (new)

**PATCH happy path:**
- [ ] `200 with { episode } on valid partial body`
- [ ] `200 archives when body is { archived_at: ISO }`
- [ ] `200 un-archives when body is { archived_at: null }`

**PATCH unhappy:**
- [ ] `403 / 429 / 401 (same as POST)`
- [ ] `400 empty_patch on empty body`
- [ ] `400 invalid_archived_at on garbage timestamp`
- [ ] `400 invalid_request when [id] is empty string`
- [ ] `400 invalid_request when [id] is not UUID-shape ("not-a-uuid", "javascript:alert(1)") — no SDK call attempted`
- [ ] `404 not_found when wrapper returns not_found`
- [ ] `502 server_error on directus_error`

### Playwright API spec: `tests/api/episodes.spec.ts` (new)

Real HTTP against `next dev`. Tests the WIRING — that the route is reachable, that origin-block actually works mid-flight, that rate-limit is enforced (send 31 writes / 121 reads quickly, expect 429 on the last). Happy-path 200 against live Directus is deferred (covered by `scripts/episodes-smoke.mjs`).

- [ ] `403 from wrong origin`
- [ ] `401 without cookie`
- [ ] `400 on malformed body`
- [ ] `400 on ?archived=garbage`
- [ ] `429 after burst`
- [ ] `404 on PATCH for non-existent uuid (after a valid login)`

### Schema sanity (manual)

- [ ] After deploy: `scripts/run-episodes-smoke.ps1` PASS end-to-end against live Fly.
- [ ] Existing `scripts/run-auth-smoke.ps1` PASS (regression check on the rest of the API surface).
- [ ] Check Directus admin UI: a row created via the smoke appears in the episodes collection; archive sets `archived_at`; un-archive clears it; hard-delete via the admin token removes it.

---

## Done-when

The Done section is ordered: the sequence below is the exact order the boxes get checked. Cross dependencies require it — smoke can't run until permissions + deploy are live, and verify must pass before commit.

**Local — TDD loop:**
- [ ] (1) All listed Vitest unit tests written and RED first.
- [ ] (2) All listed implementation lands; all Vitest unit tests GREEN.
- [ ] (3) `npm run verify` clean (lint + typecheck + Vitest 800+/800+).
- [ ] (4) Playwright API specs GREEN locally (`npm run test:e2e -- --project=api`).

**Production prep — Directus permissions:**
- [ ] (5) `powershell -ExecutionPolicy Bypass -File scripts/run-directus-script.ps1 -Script directus/scripts/setup-episodes-permissions.mjs` runs cleanly against gevoelscore-backend.fly.dev (idempotent; second run prints only `⏩` lines).
- [ ] (6) Permissions visible in Directus admin UI: new ACLs on `episodes` for Administrator AND the scoped service-token role.

**Commit + deploy:**
- [ ] (7) Commit + push. Pre-push hook runs verify gate (must stay green).
- [ ] (8) Fly auto-deploys gevoelscore-frontend. Wait for the deploy to complete (`fly status -a gevoelscore-frontend` shows the new version live).

**Live smoke checks:**
- [ ] (9) `scripts/run-episodes-smoke.ps1` PASSES end-to-end against gevoelscore-frontend.fly.dev — login → POST → GET → PATCH archive → GET filter → PATCH un-archive → cleanup.
- [ ] (10) `scripts/run-auth-smoke.ps1` PASSES (regression check — confirms day-entries and tags read paths still work post-deploy).

**Documentation:**
- [ ] (11) README ACs F1, F2 (schema) confirmed live by the smoke; AC-F6 (archive reversible) demonstrated end-to-end. Tick those boxes in `docs/features/verloop-and-episodes/README.md`.

**Commit message:** `feat(episodes): step-2 — episodes API surface (read/create/update/archive)`.

Step-2 is NOT complete if any of (1)–(11) is unchecked. If smoke fails post-deploy, the right move is fix-forward (new commit) or roll back to 36fdadb (the schema-only state) — both are reversible.

---

## Out of scope (step-2)

- **UI.** No new components, no new pages, no copy keys. The Periodes tab + VerloopView land in step-3.
- **Single-item GET (`GET /api/episodes/[id]`)**. Defer until a real caller appears. The list returns the whole set.
- **Linked-tag embedding** in episode responses. Tags-with-`parent_episode_id` come via `readAllTags` server-render. The detail view filters in the client. Step-5 wires the linking UI.
- **Hard-delete endpoint**. Directus admin only.
- **Bulk operations** (archive-multiple, delete-multiple).
- **Calendar binding write**. v1.6.
- **Episode → linked-tags via `?with_tags=true`**. If perf becomes an issue at scale we'll revisit; deferred until then.
- **Filtering by category / date overlap**. The list is small; client-side filtering suffices in v1.5. Server filters can be added in v1.6 when the timeline overlay needs a "fetch episodes whose range intersects this window" query.
- **Rate-limit telemetry / counters in Directus**. Existing limiters are process-local; same posture as the rest of the app.
- **Concurrency safety (TOCTOU on label collisions)**. Episodes have no unique-by-label constraint — labels can collide and that's fine ("Vakantie Texel" twice is two distinct trips). The UI will warn but not block.

---

## Notes for step-3

What step-3 (`step-3-periodes-tab-list.md`) needs to remember from step-2:

- The Page tree should fetch episodes server-side in `page.tsx` via `readAllEpisodes(session.accessToken)` and thread `episodes: Episode[]` down through `<TodayShell>`. Same pattern as `initialEntries`.
- Mutations (create / archive) trigger `router.refresh()` to re-run the server fetch. The API GET endpoint exists for client-side refetch but the primary read path stays server-rendered.
- The 3-tab nav (Vandaag / Periodes / Tijdlijn) lives inside TodayShell; step-3 introduces the tab switcher.
- "Active vs afgerond" grouping is client-side: active = `archived_at === null && (end_date === null || end_date >= today)`. "afgerond" = `archived_at === null && end_date !== null && end_date < today`. "archived" hidden by default; surface in a follow-up step.
- The PATCH endpoint expects ISO timestamps for `archived_at`. The client constructs this with `new Date().toISOString()` at click time.
- The tab switcher will need state lifted into TodayShell — currently TodayShell delegates to TimelineView via the existing prop chain. Step-3 introduces a `<TabContent>` switch keyed by `'vandaag' | 'periodes' | 'tijdlijn'`.
