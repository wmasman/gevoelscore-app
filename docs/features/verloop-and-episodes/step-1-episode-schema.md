# Step 1: Episode schema + domain validators

**Estimated time:** ~3 hours
**Test layers:** Vitest unit for the new `Episode` validator + the new `validateEpisodeLabel`, `validateEpisodeCategory`, `validateDateRange` helpers in `src/lib/domain/`. No component tests yet (UI lands in step-3). No e2e — schema change is verified by a Directus REST round-trip in the script's own sanity-check block.
**Risk:** Low. New collection + one nullable FK column. Idempotent migration script. No existing data affected. No code path reads `episodes` or `parent_episode_id` yet — those wire up in step-2.
**Prerequisite:** None. Builds on the existing Directus REST-API pattern documented in [memory: reference_directus_schema_approach](../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/reference_directus_schema_approach.md) and existing scripts like [add-tag-provenance.mjs](../../../directus/scripts/add-tag-provenance.mjs) and [add-tag-hierarchy.mjs](../../../directus/scripts/add-tag-hierarchy.mjs).

> Adds the `episodes` Directus collection and the `tags.parent_episode_id` nullable FK column. Adds the matching domain types + validators in `src/lib/domain/episode.ts` and the shared `src/lib/domain/date-range.ts`. **No API surface, no React, no UI** — those are step-2 and step-3. This step is pure data-model + pure-function validators, which is the smallest commit that can stand on its own and be reverted cleanly if the model needs to shift before step-2 commits to it.

---

## Acceptance criteria

- [ ] **AC1: `episodes` Directus collection exists** with exactly these fields (matching the README data-model table):
  - `id` (UUID, PK)
  - `label` (string, max 40 chars, NOT NULL)
  - `category` (string, enum `interventie` | `levensgebeurtenis`, NOT NULL)
  - `start_date` (DATE, NOT NULL)
  - `end_date` (DATE, nullable)
  - `description` (text, nullable)
  - `calendar_binding` (JSON, nullable — reserved for v1.6, always null in v1.5)
  - `archived_at` (timestamp, nullable)
  - `created_at` (timestamp, auto on insert)
  - `updated_at` (timestamp, auto on update)
- [ ] **AC2: `tags.parent_episode_id` nullable FK exists**, pointing at `episodes.id`, with ON DELETE SET NULL behaviour at the DB level so a future hard-delete of an episode (Directus admin only — see README §Out of scope) doesn't leave dangling references. Default null.
- [ ] **AC3: Migration script is idempotent.** Running `directus/scripts/add-episodes.mjs` twice produces no errors and no schema churn. Each field-add is gated by a `fieldExists` check (same pattern as `add-tag-provenance.mjs`); the collection itself is gated by a similar `collectionExists` check.
- [ ] **AC4: Existing tag rows are unaffected.** After running the migration, `SELECT count(*) FROM tags WHERE parent_episode_id IS NOT NULL` returns 0. No backfill, no data movement.
- [ ] **AC5: `Episode` domain type + validator exist** in [src/lib/domain/episode.ts](../../../src/lib/domain/episode.ts). Strict shape validation following the `validateTag` pattern: REQUIRED_KEYS check, per-field type guards, all-or-nothing.
- [ ] **AC6: `validateEpisodeLabel` rejects:** empty string, whitespace-only string, strings longer than 40 chars after whitespace normalisation, non-string input. Trims surrounding whitespace AND collapses runs of internal whitespace to a single space (same shape as `validateTagLabel`). **Does NOT enforce a word-count limit** — accepts any number of words within the 40-char ceiling. Accepts strings 1-40 chars after normalisation.
- [ ] **AC7: `validateEpisodeCategory` accepts** only `'interventie'` and `'levensgebeurtenis'`. Rejects all other strings including `'project'` and `'patroon'` (v2 categories — schema gate enforced at the domain layer too).
- [ ] **AC8: `validateDateRange` accepts** any valid ISO YYYY-MM-DD `start_date` (past, present, OR future), and a nullable `end_date` that, when non-null, is `>=` start_date. Rejects: malformed dates, `end_date < start_date`, non-string types.
- [ ] **AC9: Episode validator round-trips** a Directus REST response shape (snake_case keys, ISO timestamps) into the domain type with no lossy conversion.
- [ ] **AC10: Verify gate green.** `npm run verify` clean. No new lint disables. No dependency added.
- [ ] **AC11: Schema verifier extended.** [`directus/scripts/verify-schema.mjs`](../../../directus/scripts/verify-schema.mjs) gets two new assertions: `episodes` collection has the expected fields; `tags.parent_episode_id` exists. Running the verifier post-migration passes.

---

## Technical constraints

- **Idempotent REST-API script, no `schema apply`.** Per the locked convention in [memory: reference_directus_schema_approach](../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/reference_directus_schema_approach.md). One-POST-per-field; gated by existence checks; never use `npx directus schema apply` or a `schema.yml`.
- **No `owner` column on `episodes`.** Matches the existing pattern for `day_entries` and `tags` — v1.5 stays single-user. Multi-user data scoping is a v2 schema migration covering all collections together (see [roadmap.md](../../roadmap.md)).
- **`calendar_binding` JSON column reserved**. Always null in v1.5. The schema column exists so v1.6 doesn't need a follow-up migration, but the domain validator MUST reject any non-null value to prevent accidental writes from leaking in via the API in step-2. (Once v1.6 ships, the validator is updated alongside the calendar-binding feature.)
- **`description` is plain text, not Markdown.** Same shape as `day_entries.note`. No rendering layer; the textarea displays it raw. Avoids the security + accessibility cost of a Markdown renderer for a low-value formatting upgrade.
- **`archived_at` is a soft-delete marker, not a status field.** Non-archived = `archived_at IS NULL`. Archived = `archived_at = <timestamp>`. Same convention as `tags.archived_at`. Avoids a separate `is_archived` boolean (single source of truth, easy to query "archived between X and Y").
- **`parent_episode_id` is nullable AND has ON DELETE SET NULL.** If an episode is hard-deleted in Directus admin (the README's only documented hard-delete path), referencing tags don't dangle — they revert to standalone tags. Confirmed safe because nullification is information loss, not corruption: a standalone tag is a valid state in the existing schema.
- **No new dependency.** All validators are pure TypeScript using the existing patterns.
- **Step-1 ships independently.** Reverting it (drop column, drop collection) is a one-script operation if the model shifts between step-1 and step-2.

---

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New collection storing user data | GDPR Art 9 (health data) | Yes | `episodes.description` may contain medical context (medications, therapist names). Same posture as `day_entries.note` — self-hosted Directus, export + full-delete remain first-class. No new privacy surface added; same data category as already handled. |
| New env var | A02 (secrets) | No | Migration script uses the existing `$env:DIRECTUS_TOKEN` admin token; no new secret. |
| New route handler | A01–A08 | No | No HTTP surface added in this step. Step-2 introduces routes. |
| New dependency | ADR / lockfile | No | Pure TypeScript, REST-API JS script using existing helpers. |
| Reduced motion / animation | WCAG 2.3.3 | No | No UI. |
| Aria labelling | WCAG 1.1.1 | No | No UI. |
| Logging contains PII | A09 (log hygiene) | Yes | The migration script may print row counts during the sanity-check tail. Make sure it does NOT print `description` content or `label` values — only counts and field names. (Existing scripts already follow this; sanity-check should too.) |

---

## Plan

### 1.0 New helper module `src/lib/domain/date-range.ts`

A tiny shared module — extracted now because Episode is the first consumer but the helper is generic enough that a future feature (calendar binding, project entity) will want it.

```ts
// src/lib/domain/date-range.ts
// Validate an ISO YYYY-MM-DD pair where start is required and end is
// optional. When end is provided it must be >= start. No timezone
// assumptions — these are calendar dates, not timestamps.

const ISO_DATE_REGEX = /^\d{4}-\d{2}-\d{2}$/;

export type DateRangeError =
  | 'invalid_start_date'
  | 'invalid_end_date'
  | 'end_before_start';

export type ValidateDateRangeResult =
  | { ok: true; value: { start_date: string; end_date: string | null } }
  | { ok: false; error: DateRangeError };

export function validateDateRange(
  start: unknown,
  end: unknown,
): ValidateDateRangeResult {
  if (typeof start !== 'string' || !ISO_DATE_REGEX.test(start) || isNaN(new Date(start).getTime())) {
    return { ok: false, error: 'invalid_start_date' };
  }
  if (end !== null) {
    if (typeof end !== 'string' || !ISO_DATE_REGEX.test(end) || isNaN(new Date(end).getTime())) {
      return { ok: false, error: 'invalid_end_date' };
    }
    if (end < start) {
      return { ok: false, error: 'end_before_start' };
    }
  }
  return { ok: true, value: { start_date: start, end_date: end as string | null } };
}
```

### 1.1 New helper module `src/lib/domain/episode-category.ts`

Mirrors `src/lib/domain/tag-category.ts`. Two-value enum.

```ts
// src/lib/domain/episode-category.ts
export const EPISODE_CATEGORIES = ['interventie', 'levensgebeurtenis'] as const;
export type EpisodeCategory = (typeof EPISODE_CATEGORIES)[number];

export type ValidateEpisodeCategoryResult =
  | { ok: true; value: EpisodeCategory }
  | { ok: false; error: 'invalid_episode_category' };

export function validateEpisodeCategory(
  input: unknown,
): ValidateEpisodeCategoryResult {
  if (
    typeof input === 'string' &&
    (EPISODE_CATEGORIES as readonly string[]).includes(input)
  ) {
    return { ok: true, value: input as EpisodeCategory };
  }
  return { ok: false, error: 'invalid_episode_category' };
}
```

### 1.2 New helper module `src/lib/domain/episode-label.ts`

Mirrors `src/lib/domain/tag-label.ts` but with the 80-char ceiling.

```ts
// src/lib/domain/episode-label.ts
// Same character ceiling as MAX_TAG_LABEL_LENGTH (40), but episodes
// have NO word-count limit (tags cap at 2 words; episodes naturally
// run 3-4 words: "Coaching met Sarah", "Wekelijkse fysio bij Marieke").
// Narrative content goes in `description`, not the label.

export const MAX_EPISODE_LABEL_LENGTH = 40;

export type EpisodeLabelError = 'wrong_type' | 'empty' | 'too_long';

export type ValidateEpisodeLabelResult =
  | { ok: true; value: string }
  | { ok: false; error: EpisodeLabelError };

export function validateEpisodeLabel(input: unknown): ValidateEpisodeLabelResult {
  if (typeof input !== 'string') {
    return { ok: false, error: 'wrong_type' };
  }
  // Trim + collapse internal whitespace runs to a single space (mirrors
  // validateTagLabel) — required so "coaching  sarah" and "coaching sarah"
  // compare equal on dedup.
  const normalised = input.trim().replace(/\s+/g, ' ');
  if (normalised.length === 0) {
    return { ok: false, error: 'empty' };
  }
  if (normalised.length > MAX_EPISODE_LABEL_LENGTH) {
    return { ok: false, error: 'too_long' };
  }
  return { ok: true, value: normalised };
}
```

### 1.3 New domain type + validator `src/lib/domain/episode.ts`

Strict shape validator following `validateTag`. Composes the three sub-validators above plus the existing iso-timestamp guard.

```ts
// src/lib/domain/episode.ts
import { validateDateRange } from './date-range';
import { validateEpisodeCategory, type EpisodeCategory } from './episode-category';
import { validateEpisodeLabel } from './episode-label';

export type Episode = {
  id: string;
  label: string;
  category: EpisodeCategory;
  start_date: string;
  end_date: string | null;
  description: string | null;
  calendar_binding: unknown | null;  // typed `unknown | null` in v1.5; locked to null in the validator. Will be properly typed in v1.6.
  archived_at: string | null;
  created_at: string;
  updated_at: string;
};

export type EpisodeError =
  | 'invalid_shape'
  | 'invalid_id'
  | 'invalid_label'
  | 'invalid_category'
  | 'invalid_date_range'
  | 'invalid_description'
  | 'invalid_calendar_binding'
  | 'invalid_archived_at'
  | 'invalid_created_at'
  | 'invalid_updated_at';

export type ValidateEpisodeResult =
  | { ok: true; value: Episode }
  | { ok: false; error: EpisodeError };

const REQUIRED_KEYS = [
  'archived_at',
  'calendar_binding',
  'category',
  'created_at',
  'description',
  'end_date',
  'id',
  'label',
  'start_date',
  'updated_at',
] as const;

const ISO_UTC_TIMESTAMP_REGEX =
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;

export function validateEpisode(input: unknown): ValidateEpisodeResult {
  if (input === null || typeof input !== 'object' || Array.isArray(input)) {
    return { ok: false, error: 'invalid_shape' };
  }
  const obj = input as Record<string, unknown>;
  const actualKeys = Object.keys(obj).sort();
  if (
    actualKeys.length !== REQUIRED_KEYS.length ||
    !actualKeys.every((k, i) => k === REQUIRED_KEYS[i])
  ) {
    return { ok: false, error: 'invalid_shape' };
  }

  if (typeof obj.id !== 'string' || obj.id.length === 0) {
    return { ok: false, error: 'invalid_id' };
  }

  const labelResult = validateEpisodeLabel(obj.label);
  if (!labelResult.ok) return { ok: false, error: 'invalid_label' };

  const categoryResult = validateEpisodeCategory(obj.category);
  if (!categoryResult.ok) return { ok: false, error: 'invalid_category' };

  const rangeResult = validateDateRange(obj.start_date, obj.end_date);
  if (!rangeResult.ok) return { ok: false, error: 'invalid_date_range' };

  if (obj.description !== null && typeof obj.description !== 'string') {
    return { ok: false, error: 'invalid_description' };
  }

  // v1.5: calendar_binding must be null. The column exists for v1.6 but
  // accepting any non-null shape now would lock us in before that design lands.
  if (obj.calendar_binding !== null) {
    return { ok: false, error: 'invalid_calendar_binding' };
  }

  if (obj.archived_at !== null && !isIsoUtcTimestamp(obj.archived_at)) {
    return { ok: false, error: 'invalid_archived_at' };
  }
  if (!isIsoUtcTimestamp(obj.created_at)) {
    return { ok: false, error: 'invalid_created_at' };
  }
  if (!isIsoUtcTimestamp(obj.updated_at)) {
    return { ok: false, error: 'invalid_updated_at' };
  }

  return {
    ok: true,
    value: {
      id: obj.id,
      label: labelResult.value,
      category: categoryResult.value,
      start_date: rangeResult.value.start_date,
      end_date: rangeResult.value.end_date,
      description: obj.description as string | null,
      calendar_binding: null,
      archived_at: obj.archived_at as string | null,
      created_at: obj.created_at,
      updated_at: obj.updated_at,
    },
  };
}

function isIsoUtcTimestamp(input: unknown): input is string {
  if (typeof input !== 'string') return false;
  if (!ISO_UTC_TIMESTAMP_REGEX.test(input)) return false;
  const parsed = new Date(input);
  return !Number.isNaN(parsed.getTime());
}
```

### 1.4 New migration script `directus/scripts/add-episodes.mjs`

Idempotent REST-API script. Pattern lifted from `add-tag-provenance.mjs` + `add-tag-hierarchy.mjs`.

Outline (full code in implementation):

```js
import { banner, directusRequest } from './lib/directus-request.mjs';
banner('add-episodes');

// 1) Create collection if missing.
async function collectionExists(name) {
  try { await directusRequest(`/collections/${name}`); return true; }
  catch { return false; }
}

if (!(await collectionExists('episodes'))) {
  console.log('  + Creating episodes collection');
  await directusRequest('/collections', 'POST', {
    collection: 'episodes',
    meta: {
      icon: 'event_note',
      note: 'Multi-day Episodes (interventies + levensgebeurtenissen). See features/verloop-and-episodes/.',
      display_template: '{{label}}',
      sort_field: 'start_date',
    },
    schema: { name: 'episodes' },
  });
}

// 2) Per-field add, gated by fieldExists.
const fields = [
  { field: 'label',            type: 'string',    schema: { is_nullable: false, max_length: 40 } },
  { field: 'category',         type: 'string',    schema: { is_nullable: false, max_length: 32 }, meta: { interface: 'select-dropdown', options: { choices: [{text:'Interventie',value:'interventie'},{text:'Levensgebeurtenis',value:'levensgebeurtenis'}] } } },
  { field: 'start_date',       type: 'date',      schema: { is_nullable: false } },
  { field: 'end_date',         type: 'date',      schema: { is_nullable: true } },
  { field: 'description',      type: 'text',      schema: { is_nullable: true } },
  { field: 'calendar_binding', type: 'json',      schema: { is_nullable: true }, meta: { note: 'Reserved for v1.6 (Google Calendar). Always null in v1.5.' } },
  { field: 'archived_at',      type: 'timestamp', schema: { is_nullable: true } },
  { field: 'created_at',       type: 'timestamp', schema: {}, meta: { special: ['date-created'] } },
  { field: 'updated_at',       type: 'timestamp', schema: {}, meta: { special: ['date-updated'] } },
];

// 3) Add tags.parent_episode_id with the FK relation.
//    Two REST calls: POST /fields/tags (the column), POST /relations (the FK).
//    Gated by fieldExists('tags', 'parent_episode_id').
const tagParentFkField = {
  field: 'parent_episode_id',
  type: 'uuid',
  schema: { is_nullable: true },
  meta: { interface: 'select-dropdown-m2o', note: 'Optional FK: when set, this tag is an occurrence of an Episode.' },
};
const tagParentFkRelation = {
  collection: 'tags',
  field: 'parent_episode_id',
  related_collection: 'episodes',
  schema: { on_delete: 'SET NULL' },
};

// 4) Sanity-check counts (no PII printed).
//    - count of episodes (expected 0)
//    - count of tags.parent_episode_id IS NOT NULL (expected 0)

console.log('\n✅ Done.\n');
```

### 1.5 Extend `directus/scripts/verify-schema.mjs`

Add two assertions:
- `episodes` collection exists; all 10 fields present with the right types.
- `tags.parent_episode_id` exists; FK relation present with ON DELETE SET NULL.

### 1.6 No copy changes

No new strings in `src/copy.ts`. Step-1 is data-model only.

---

## Test list (RED-first)

### Unit: `src/lib/domain/__tests__/date-range.test.ts` (new)

- [ ] `accepts a valid start_date and null end_date (ongoing episode)`
- [ ] `accepts a valid start_date and a later end_date (closed range)`
- [ ] `accepts start_date == end_date (single-day episode is OK)`
- [ ] `accepts a future start_date (no upper bound on start_date)`
- [ ] `rejects end_date strictly before start_date with end_before_start`
- [ ] `rejects malformed start_date (e.g. '2026-13-01', '2026/06/01', empty string)`
- [ ] `rejects malformed end_date when non-null`
- [ ] `rejects non-string start_date or end_date`
- [ ] `treats end_date undefined as invalid_end_date (only null is accepted for ongoing)`

### Unit: `src/lib/domain/__tests__/episode-category.test.ts` (new)

- [ ] `accepts 'interventie'`
- [ ] `accepts 'levensgebeurtenis'`
- [ ] `rejects 'project' (v2 category — gate enforced at the domain layer too)`
- [ ] `rejects 'patroon' (v2 category)`
- [ ] `rejects 'mentaal' (tag category, not an episode category)`
- [ ] `rejects empty string, null, undefined, number, object`

### Unit: `src/lib/domain/__tests__/episode-label.test.ts` (new)

- [ ] `accepts a normal 2-word label ("Coaching Sarah")`
- [ ] `accepts a 3-word label ("Coaching met Sarah") — no word-count constraint`
- [ ] `accepts a 4-word label ("Wekelijkse fysio bij Marieke") — no word-count constraint`
- [ ] `accepts the longest valid label (40 chars exactly after normalisation)`
- [ ] `accepts a label that's 40 chars after normalisation but >40 with leading/trailing whitespace`
- [ ] `collapses runs of internal whitespace: "hoofd  pijn" normalises to "hoofd pijn"`
- [ ] `rejects empty string → empty`
- [ ] `rejects whitespace-only string → empty`
- [ ] `rejects 41 chars after normalisation → too_long`
- [ ] `rejects non-string input (number, null, undefined, object) → wrong_type`
- [ ] `returns the NORMALISED value when accepted (trimmed + collapsed)`

### Unit: `src/lib/domain/__tests__/episode.test.ts` (new)

- [ ] `accepts a complete Directus REST response shape with all 10 fields`
- [ ] `accepts a response with end_date null (ongoing)`
- [ ] `accepts a response with archived_at set (archived episode)`
- [ ] `rejects missing keys → invalid_shape`
- [ ] `rejects extra keys → invalid_shape`
- [ ] `rejects empty id → invalid_id`
- [ ] `rejects bad label → invalid_label`
- [ ] `rejects category 'project' → invalid_category (gate on v2 categories)`
- [ ] `rejects end_date < start_date → invalid_date_range`
- [ ] `rejects non-string description (when not null) → invalid_description`
- [ ] `rejects non-null calendar_binding → invalid_calendar_binding (v1.5 gate)`
- [ ] `rejects bad archived_at format → invalid_archived_at`
- [ ] `rejects bad created_at / updated_at → invalid_created_at / invalid_updated_at`
- [ ] `round-trips a valid Directus shape: validator output keys + values match input`

### Schema sanity (integration, manual, not in CI)

These run against a live Directus instance after the migration script. They aren't automated Vitest tests — they're a checklist for the developer running the script.

- [ ] After running `node directus/scripts/add-episodes.mjs` once: collection appears in Directus admin with all 10 fields; types and constraints match AC1.
- [ ] Running the script a SECOND time produces only `⏩ already exists` lines; no errors, no churn.
- [ ] After running once: `node directus/scripts/verify-schema.mjs` exits 0.
- [ ] `SELECT count(*) FROM tags WHERE parent_episode_id IS NOT NULL` returns 0.
- [ ] Manual smoke via Directus REST: POST a minimal episode → 200 + id; GET it back → matches the domain validator's accepted shape; PATCH it → updated_at advances; DELETE the test row.

### Existing tests stay green

No existing code path reads `episodes` or `parent_episode_id`. The Tag validator already ignores unknown keys for forward-compatibility... wait — actually it DOESN'T. `validateTag` is strict-keys (REQUIRED_KEYS check). **Adding `parent_episode_id` to the schema will break `validateTag` round-trips** unless we extend it in this step.

→ **Action**: in 1.3, also extend `src/lib/domain/tag.ts` to accept the new `parent_episode_id` field. Add it to REQUIRED_KEYS, add a validator (UUID or null), thread through the returned value object. This is a one-test-list extension of the existing `tag.test.ts` — 4-5 new cases — but it MUST happen in step-1 so the Directus migration doesn't break the existing tag read path.

Concretely add to `src/lib/domain/tag.ts`:
- New field on the `Tag` type: `parent_episode_id: string | null`.
- New `'invalid_parent_episode_id'` error variant.
- New required key in REQUIRED_KEYS.
- Per-field validator: UUID-like non-empty string OR null.
- Extend the returned-value object.

And in `src/lib/domain/__tests__/tag.test.ts`:
- [ ] `accepts a tag with parent_episode_id set to a UUID-like string`
- [ ] `accepts a tag with parent_episode_id null`
- [ ] `rejects parent_episode_id empty string → invalid_parent_episode_id`
- [ ] `rejects parent_episode_id number / object → invalid_parent_episode_id`
- [ ] `rejects parent_episode_id undefined (must be present, even if null) → invalid_shape`

---

## Done-when

- [ ] All listed unit tests written and RED first.
- [ ] All listed implementation lands; all unit tests GREEN.
- [ ] `npm run verify` clean (lint + typecheck + Vitest).
- [ ] Migration script runs cleanly on the dev Directus (twice — second run prints only `⏩` lines).
- [ ] `verify-schema.mjs` passes against dev Directus.
- [ ] Manual REST smoke (POST / GET / PATCH / DELETE a test episode) round-trips through the validator.
- [ ] No data is left behind from the smoke test.
- [ ] README ACs F1, F2 ticked (the schema-level ones).
- [ ] Commit message: `feat(episodes): add episodes collection + tags.parent_episode_id FK + domain validators (step-1)`.

---

## Out of scope (step-1)

- **API surface.** `src/lib/api/episodes.ts` + `src/app/api/episodes/route.ts` land in step-2.
- **UI.** No new components, no new pages, no copy. Step-3 introduces the Periodes tab.
- **Backfill of any kind.** No existing data is moved or transformed. `episodes` starts empty; `tags.parent_episode_id` starts all-null.
- **Calendar binding logic.** The column exists; the validator forces null; no read path uses it.
- **Episode archive semantics in code.** The column exists; the FK-preservation rule (resolved in the README) only matters once step-2's update + archive endpoints are wired. Step-1's validator accepts `archived_at` as a nullable timestamp; nothing more.
- **Soft-delete cascading.** If a user (or admin) sets `archived_at` on an episode, the linked tags' `parent_episode_id` stays pointing at it — that's the resolved design. But there's no archive endpoint to test against yet; step-2 owns it.
- **Display-side label truncation.** ~30-char ellipsis in the list view lives in step-3 (the list-view component); not relevant to the schema.

---

## Notes for step-2

What step-2 (`step-2-episodes-api.md`) needs to remember from step-1:

- `parent_episode_id` is now a required key on `Tag`. Every API write path that constructs a Tag for return must include it (default null).
- `validateEpisode` enforces `calendar_binding === null` — the create + update endpoints must not accept any non-null value here in v1.5, even if a client sends one.
- `archived_at` is the only "status" field. There's no `is_archived` bool. Active-vs-archived filtering is `archived_at IS NULL` vs `IS NOT NULL`.
- The Tag domain validator now has a `parent_episode_id` key. Existing API code paths returning Tag objects need to be audited in step-2 to ensure they include this field — running tests after step-1 lands will surface any that don't.
