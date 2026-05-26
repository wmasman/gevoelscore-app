# Data model

This document defines every entity in the system: fields, types, IDs, relationships, validation rules, and which schema layer owns which. It is the contract for `src/lib/domain/` and the source of truth for `src/lib/db/` migrations.

Companion documents (to be written):

- [identity.md](identity.md) — ID strategy, deletion strategy, multi-device sync implications, deeper rationale
- [persistence.md](persistence.md) — SQLite schema, migrations, encryption, sync seam
- [integrations.md](integrations.md) — plug interface for v1.5/v2 data sources
- [dependencies.md](dependencies.md) — per-package audit against cardinal principles + local-first + no-telemetry
- [overview.md](overview.md) — layer diagram and dependency direction

---

## Schema-readiness rule

**v1 ships with every entity defined, every table created, even ones it doesn't write to.** This is the explicit promise in [REQUIREMENTS.md](../REQUIREMENTS.md):

> Architecture readiness for v1.5/v2 (per REQUIREMENTS.md) is straightforward — schema includes nullable fields for v1.5/v2 data sources, left empty in v1 but present.

So we draw the schema for v1 + v1.5 + v2 right now. v1 populates only what its features need. Future versions fill in the rest without migrations beyond additive ones.

Concrete consequence: when you read this doc and think "but v1 doesn't use that," that's the point — v1 *won't* use that, but the field exists so v1.5 doesn't trigger a migration that touches data v1 wrote.

---

## Platform commitments

Per [ADR 0001](../decisions/0001-framework-expo.md), this is an Expo (React Native) project. The architecture commits to specific Expo packages where they apply. The domain layer is the only exception, and not for optionality reasons.

| Layer | Commitment | Why this layer |
|---|---|---|
| `src/lib/domain/` | **Pure TS only** — no `expo-*` or `react-native-*` imports | Vitest runs in Node and cannot load native modules. Domain tests must be fast and native-free. Pure TS types are the same regardless of framework — there is no "Expo-flavored" `DayEntry` type to commit to. |
| `src/lib/db/` | **`expo-sqlite`** | The SQLite engine. Encryption strategy (SQLCipher via `op-sqlite` vs OS-level disk encryption only) deferred to [persistence.md](persistence.md). |
| `src/lib/integrations/` | **`react-native-health`** (HealthKit, v2), **`expo-calendar`** (v1.5), **`expo-location`** (v2 weather), Open-Meteo via `fetch` (v2 weather) | All read-only, all opt-in per source. Documented in [integrations.md](integrations.md). |
| Crypto / IDs | **`expo-crypto`** for UUIDs and any future hashing | Native randomness; one fewer dep than a third-party UUID library. |
| Secrets / OAuth tokens (v1.5+) | **`expo-secure-store`** | Keychain (iOS) / Keystore (Android) backed. Never in SQLite, never in plain files. |
| File export / import | **`expo-file-system`**, **`expo-sharing`** | Mobile-native file handling, system share sheet for CSV export. |
| Local notifications (v2) | **`expo-notifications`** with local schedule only | No push server. Local schedule is offline-safe and zero-telemetry. |
| Tests (Node-runnable) | **Vitest** | Already chosen in scaffold. Domain + storage + integration logic tests. |
| Tests (UI / native) | **`@testing-library/react-native`** for components; **Maestro** for end-to-end flows (deferred) | Added once Expo and screens land. |

Every package on this list will be audited against the cardinal principles + local-first + no-telemetry rule in [dependencies.md](dependencies.md). Adding any package not on this list requires an ADR.

---

## Cross-cutting decisions

These apply to every entity below. Settle them once.

### ID strategy

| Entity | ID | Reason |
|---|---|---|
| `DayEntry` | `date` (ISO 8601 `YYYY-MM-DD` string) as natural primary key | One entry per day is the cardinal invariant of the system. A surrogate ID would invite duplicates. Date sorts naturally. |
| `Tag` | UUID v4 via `expo-crypto.randomUUID()` | Stable across rename; sync-friendly across devices; native randomness. |
| `Project` | UUID v4 via `expo-crypto.randomUUID()` | Same reasoning as Tag. |
| `ProjectEntry` | UUID v4 via `expo-crypto.randomUUID()`, with `UNIQUE(date, project_id)` | Composite would also work; UUID is cleaner for future sync conflict resolution. |
| `ProjectFieldConfig` | UUID v4 via `expo-crypto.randomUUID()` | One-to-many from Project; identity matters because fields can be renamed/reordered. |
| `CalendarEvent` | The Google event ID (string) | Already unique and stable upstream. No reason to add our own. |
| `GarminDaily`, `HealthDaily`, `WeatherDaily` | `date` as PK | One per day per source. Same reasoning as `DayEntry`. |

**Why UUID v4 via `expo-crypto`:** native randomness backed by the platform CSPRNG, no third-party UUID library to vet. At our scale (~365 rows/year per entity) the time-ordered B-tree locality of v7 would be invisible, and v7 would require an extra dependency that doesn't pass `dependencies.md` lightly.

**Source of UUIDs:** the client. Never the database. This keeps writes single-step and survives offline → sync flows trivially.

**Domain-layer caveat:** because `src/lib/domain/` is pure TS (no `expo-*` imports), the domain types declare `id: string` and the ID-generation call site lives in `src/lib/db/` or higher. Tests inject UUIDs as strings, never call `expo-crypto` directly.

### Timestamps and timezones

| Field | Type | Stored as | Displayed as |
|---|---|---|---|
| `created_at`, `updated_at` | ISO 8601 string | UTC (`2026-05-26T19:42:11.000Z`) | User's local timezone |
| `date` on `DayEntry` etc. | ISO 8601 date string | User's local date at write time (`2026-05-26`) | Same string, formatted per locale |

**Why split:** the score for a given day is bound to the user's local concept of "today." If you fly Amsterdam → New York and log a score after midnight local time, that's the *next* day in your local frame, even if UTC says it's still yesterday. We capture the local date at write time and never reinterpret.

**Implementation rule:** `date` fields are *strings*, never `Date` objects in domain code. JavaScript's `Date` is timezone-treacherous. Parse to `Date` only for arithmetic, never for storage.

### Soft delete vs hard delete

| Entity | Strategy | Reason |
|---|---|---|
| `DayEntry` | Hard overwrite, no edit history | Brief: "overschrijven mag, geen dubbele entries." Edit history is not a requirement. |
| `Tag` | Soft delete (`archived_at` nullable timestamp) | Historical entries still reference archived tags. UI hides archived tags from autocomplete. |
| `Project` | Status field (`active` / `paused` / `completed` / `archived`), no separate delete | Status is the user's mental model; hard delete is offered separately if user explicitly wants it gone. |
| `ProjectEntry` | Hard delete on day rewrite | Matches `DayEntry` semantics. |
| `CalendarEvent` | Hard delete on re-sync | Source of truth is Google; we can always re-fetch. |
| `GarminDaily`, `HealthDaily`, `WeatherDaily` | Hard overwrite on re-fetch | Same — source of truth is upstream. |

**Tag merge** (e.g., merge "moe" and "vermoeid" into one): is a UI feature, not a separate entity state. The merge operation updates every junction row from `tag_id = A` to `tag_id = B`, then soft-deletes Tag A. Reversibility is out of scope for v1.

### Nullability discipline

We use TypeScript strict + `noUncheckedIndexedAccess`. The rule:

- A field is `T | null` when its *absence* is a meaningful state (e.g., `DayEntry.note = null` means "no note today")
- A field is `T | undefined` only at parse boundaries, never in persisted shapes
- Optional fields (`field?: T`) are forbidden in domain types — explicit `T | null` is the convention

This makes every field reachable via type-safe access patterns and prevents `if (entry.note) { ... }` ambiguity.

---

## Entities

Every entity is defined as (1) a TypeScript type, (2) validation rules, (3) tests to write. The types live in `src/lib/domain/{entity-name}.ts`; their tests in `src/lib/domain/__tests__/{entity-name}.test.ts`.

### `DayEntry`

The cardinal entity. One row per local-date the user has logged.

```typescript
type DayEntry = {
  date: string;                          // ISO 8601 'YYYY-MM-DD', primary key
  score: 1 | 2 | 3 | 4 | 5 | 6;          // integer only — see "Score validation" below
  note: string | null;                   // free text, no length limit; null = no note today
  tag_ids: string[];                     // refs to Tag.id; order is presentation, not semantic
  sub_scores: SubScores | null;          // v2; null in v1
  sleep_hours: number | null;            // v2 bonus field; null in v1
  special_event: string | null;          // v1.5 manual "iets speciaals" field; null in v1
  project_entry_ids: string[];           // refs to ProjectEntry.id; empty in v1
  calendar_event_ids: string[];          // refs to CalendarEvent.id; empty in v1
  garmin: GarminDaily | null;            // v2; null in v1
  health: HealthDaily | null;            // v2; null in v1
  weather: WeatherDaily | null;          // v2; null in v1
  derived: DerivedIndicators | null;     // v2; null in v1
  created_at: string;                    // ISO 8601 UTC
  updated_at: string;                    // ISO 8601 UTC
};

type SubScores = {
  cognitive: 1 | 2 | 3 | 4 | 5 | 6 | null;   // same scale as overall score
  physical: 1 | 2 | 3 | 4 | 5 | 6 | null;
  mental: 1 | 2 | 3 | 4 | 5 | 6 | null;
};

type DerivedIndicators = {
  rhr_vs_baseline_30d: number | null;
  hrv_vs_baseline_30d: number | null;
  sleep_quality_score: number | null;    // 1-5
  activity_load: 'rust' | 'licht' | 'matig' | 'zwaar' | null;
};
```

**Validation rules:**

- `date` matches `^\d{4}-\d{2}-\d{2}$` and is a real calendar date (not `2026-02-30`)
- `date` is not in the future (>= 1 day past today rejected)
- `score` is one of: `1, 2, 3, 4, 5, 6` (integers only)
- `score` outside this set, including `2.5` or any decimal, is rejected at the domain boundary
- `note` is either `null` or a non-empty string after trim (empty string after trim becomes `null`)
- `tag_ids` contains no duplicates; references must resolve to existing tags at persist time
- `sub_scores.*` each follow the same `score` validation when non-null
- `sleep_hours` if non-null is `>= 0 && <= 24`
- `created_at <= updated_at`
- Reading a `DayEntry` from storage that violates any rule must throw at the boundary, not silently degrade

**Score validation — integers only (no halves):** the brief proposed half-values ("eventueel met halve waarden, 4.5 toelaten") but the locked decision is **integer-only**. Rationale: forcing a single integer choice (1–6) makes the user commit to a number rather than averaging away ambiguity. Nuance lives in `note` and `tag_ids`, which are richer than a 0.5-step refinement of the score. This is a tightening of the brief's range, captured here rather than as a separate ADR because the data-model is its locking surface.

**Tests to write:**

- `accepts integer score 1, 2, 3, 4, 5, 6`
- `rejects score 0`
- `rejects score 7`
- `rejects score 4.5 (halves not allowed)`
- `rejects score 3.1 (decimals not allowed)`
- `rejects score below 1`
- `rejects date '2026-02-30'`
- `rejects future date beyond today`
- `accepts today's date`
- `normalizes whitespace-only note to null`
- `rejects duplicate tag_ids`
- `accepts entry with all v1.5/v2 fields null`
- `accepts entry with sub_scores populated`
- `rejects sleep_hours = -1`
- `rejects sleep_hours = 25`

### `Tag`

```typescript
type Tag = {
  id: string;                                              // UUID v7
  label: string;                                           // trimmed, non-empty
  category: TagCategory;
  project_id: string | null;                               // FK to Project.id, only when category === 'project'
  usage_count: number;                                     // denormalized; recomputed by trigger or recalc job
  archived_at: string | null;                              // ISO 8601 UTC; null = active
  created_at: string;
};

type TagCategory =
  | 'fysiek'
  | 'mentaal'
  | 'positief'
  | 'activiteit'
  | 'interventie'
  | 'project'                                              // requires project_id
  | 'custom';
```

**Validation rules:**

- `label` is trimmed and non-empty
- `label` unique within `(category, archived_at IS NULL)` — case-insensitive
- `category === 'project'` requires `project_id` non-null; all other categories require `project_id === null`
- `usage_count >= 0`
- Renaming a tag updates `label` only; `id` is stable

**Tests to write:**

- `rejects empty label`
- `rejects whitespace-only label`
- `trims label before persist`
- `rejects duplicate active label in same category (case-insensitive)`
- `allows same label across different categories`
- `allows same label as archived tag in same category`
- `requires project_id when category is 'project'`
- `forbids project_id when category is not 'project'`
- `rename preserves id`
- `archive sets archived_at, does not delete`

### `Project` (v1.5)

Empty table in v1. Schema exists from day 1.

```typescript
type Project = {
  id: string;                                              // UUID v7
  name: string;                                            // trimmed, non-empty, user-facing label
  type: ProjectType;
  start_date: string;                                      // 'YYYY-MM-DD'
  end_date: string | null;                                 // 'YYYY-MM-DD' or null = open-ended
  status: ProjectStatus;
  description: string | null;
  field_config_ids: string[];                              // refs to ProjectFieldConfig.id
  created_at: string;
  updated_at: string;
};

type ProjectType = 'medicatie' | 'therapie' | 'oefening' | 'anders';
type ProjectStatus = 'active' | 'paused' | 'completed' | 'archived';
```

**Validation rules:**

- `name` trimmed, non-empty, unique among non-archived projects (case-insensitive)
- `start_date` is a valid date and `<= end_date` when `end_date !== null`
- `end_date === null` allowed only when `status === 'active' | 'paused'`
- `status === 'completed'` requires `end_date !== null`

**Tests to write:**

- `rejects empty name`
- `rejects start_date after end_date`
- `allows end_date null when active`
- `requires end_date when completed`
- `unique name among non-archived projects`
- `allows reused name for archived project`

### `ProjectEntry` (v1.5)

```typescript
type ProjectEntry = {
  id: string;                                              // UUID v7
  date: string;                                            // 'YYYY-MM-DD', the day this entry belongs to
  project_id: string;                                      // FK to Project.id
  note: string | null;
  tag_ids: string[];                                       // tags scoped to this project entry
  numeric_values: Record<string, number>;                  // keyed by ProjectFieldConfig.key
  created_at: string;
  updated_at: string;
};
```

**Validation rules:**

- `UNIQUE(date, project_id)` — one entry per day per project
- All keys in `numeric_values` must match a `ProjectFieldConfig.key` on the parent project, with `type === 'number'`
- All `tag_ids` must reference tags where `category === 'project' && project_id === this.project_id` OR `category === 'custom'`
- `date` must be `>= project.start_date` and (`<= project.end_date` or `project.end_date === null`)

**Tests to write:**

- `rejects entry on date before project start`
- `rejects entry on date after project end`
- `accepts entry on project boundary dates`
- `rejects unknown key in numeric_values`
- `rejects tag from a different project`
- `rejects duplicate (date, project_id)`

### `ProjectFieldConfig` (v1.5)

```typescript
type ProjectFieldConfig = {
  id: string;                                              // UUID v7
  project_id: string;                                      // FK to Project.id
  key: string;                                             // machine name, e.g. 'dose_mg'; stable within project
  label: string;                                           // user-facing
  type: FieldType;
  unit: string | null;                                     // e.g. 'mg', 'min'; relevant for type === 'number'
  default_visible: boolean;
  sort_order: number;                                      // for stable display ordering
};

type FieldType = 'text' | 'tag_set' | 'number';
```

**Validation rules:**

- `(project_id, key)` unique
- `key` matches `^[a-z][a-z0-9_]*$` (snake_case, lowercase, ASCII)
- `label` non-empty
- `unit !== null` only when `type === 'number'`

**Tests to write:**

- `rejects duplicate key within same project`
- `allows same key in different projects`
- `rejects uppercase key`
- `rejects key starting with digit`
- `rejects unit on text field`

### `CalendarEvent` (v1.5)

```typescript
type CalendarEvent = {
  id: string;                                              // Google event id
  date: string;                                            // 'YYYY-MM-DD' (event's local date)
  title: string;
  start_time: string | null;                               // ISO 8601 UTC, null if all-day
  end_time: string | null;                                 // ISO 8601 UTC, null if all-day
  all_day: boolean;
  calendar_source: string;                                 // Google calendar ID
  attendees_count: number | null;
  location: string | null;
  relevance: CalendarRelevance;
  category_hint: string | null;                            // auto-tagged 'werk' | 'sociaal' | etc.; user can override
  synced_at: string;                                       // ISO 8601 UTC, last successful sync
};

type CalendarRelevance = 'high' | 'normal' | 'hidden';
```

**Validation rules:**

- `all_day === true` requires `start_time === null && end_time === null`
- `all_day === false` requires `start_time !== null` (end_time may be null for point events)
- `start_time <= end_time` when both non-null

**Tests to write:**

- `accepts all-day event with null times`
- `rejects all-day event with start_time set`
- `rejects timed event with null start_time`
- `rejects start_time > end_time`
- `category_hint can be null (no auto-tag matched)`

### `GarminDaily` (v2)

Empty table in v1. Populated by the Garmin integration when active.

```typescript
type GarminDaily = {
  date: string;                                            // 'YYYY-MM-DD'
  rhr: number | null;                                      // bpm
  hrv_overnight_avg: number | null;                        // ms
  body_battery_morning: number | null;                     // 0-100
  body_battery_evening: number | null;                     // 0-100
  stress_avg: number | null;                               // 0-100
  sleep_total_min: number | null;
  sleep_deep_min: number | null;
  sleep_rem_min: number | null;
  sleep_light_min: number | null;
  sleep_awake_min: number | null;
  steps: number | null;
  active_calories: number | null;
  workouts: WorkoutSummary[];                              // empty array if no workouts
  source: 'apple_health' | 'garmin_direct';
  fetched_at: string;                                      // ISO 8601 UTC
};

type WorkoutSummary = {
  type: string;                                            // e.g. 'running', 'cycling'
  duration_min: number;
  avg_hr: number | null;
  max_hr: number | null;
  distance_m: number | null;
};
```

**Validation rules:**

- All numeric fields: `>= 0` when non-null
- `body_battery_*`, `stress_avg`: `0..100`
- `sleep_deep_min + sleep_rem_min + sleep_light_min + sleep_awake_min` should approximately equal `sleep_total_min` (within tolerance — Garmin's own data is imprecise)

**Tests to write:** (deferred until v2 integration ships; the table exists but isn't written to in v1)

### `HealthDaily` (v2)

```typescript
type HealthDaily = {
  date: string;
  resting_heart_rate: number | null;
  heart_rate_variability_sdnn: number | null;              // ms
  sleep_total_min: number | null;
  sleep_deep_min: number | null;
  sleep_rem_min: number | null;
  sleep_core_min: number | null;
  sleep_awake_min: number | null;
  step_count: number | null;
  active_energy_kcal: number | null;
  respiratory_rate: number | null;
  mindful_minutes: number | null;
  time_in_daylight_min: number | null;                     // iOS 17.2+
  workouts: WorkoutSummary[];
  fetched_at: string;
};
```

**Tests:** deferred to v2.

### `WeatherDaily` (v2)

```typescript
type WeatherDaily = {
  date: string;
  temp_min: number;
  temp_max: number;
  temp_avg: number;
  humidity_avg: number;
  pressure_avg: number;                                    // hPa
  pressure_delta_24h: number;                              // hPa
  precipitation_mm: number;
  daylight_minutes: number;
  uv_index_max: number;
  air_quality_index: number | null;                        // PM2.5; null when source unavailable
  location_lat: number;
  location_lon: number;
  location_label: string | null;
  fetched_at: string;
};
```

**Tests:** deferred to v2.

---

## Cross-entity invariants

These hold across the schema and need integration-level tests (`src/lib/db/__tests__/`):

- **No orphan junction rows**: every `tag_id` in `DayEntry.tag_ids` resolves to a `Tag` row (including archived tags)
- **No orphan project entries**: every `project_id` in `ProjectEntry` resolves to a `Project` row
- **One `DayEntry` per date** — `date` is unique, enforced by PK
- **Tag merge atomicity**: merging tag A → B updates all junction rows in one transaction; partial merge is forbidden
- **Date consistency**: a `DayEntry` exists for every `ProjectEntry` and every `CalendarEvent` we want to display on a day (UI joins by date, no FK enforced because passive data can arrive before the user logs)

---

## What v1 actually populates

Schema-wide picture of v1 reality:

| Table | v1 populates? | Notes |
|---|---|---|
| `day_entries` | yes — `date`, `score`, `note`, `tag_ids`, timestamps | other fields stay null |
| `tags` | yes — full lifecycle (create, rename, archive, merge) | |
| `day_entry_tags` (junction) | yes | |
| `projects` | no — table exists, never written | |
| `project_entries` | no | |
| `project_entry_tags` (junction) | no | |
| `project_field_configs` | no | |
| `calendar_events` | no | |
| `garmin_daily` | no | |
| `health_daily` | no | |
| `weather_daily` | no | |

v1.5 adds projects + calendar (4 tables go live). v2 adds the passive data tables.

---

## Open questions

These need a decision before code, but are deferred to other architecture docs to avoid bloating this one:

1. **Encryption at rest** — engine is `expo-sqlite`; the question is whether to add SQLCipher (which would mean swapping the engine to `op-sqlite` since `expo-sqlite` doesn't ship SQLCipher), or rely on OS-level full-disk encryption only, or use app-level field encryption for sensitive columns. → `persistence.md`
2. **Schema migration runner** — hand-rolled `PRAGMA user_version` ladder vs. a small library. → `persistence.md`
3. **Sync seam** — what columns/timestamps does every entity need to support eventual sync (e.g., `last_modified_at` per row, tombstones for deletes)? → `identity.md`
4. **Junction storage** — `tag_ids: string[]` in the type, but stored as separate junction tables in SQLite. Domain-layer round-trip details. → `persistence.md`
5. **Validation library** — Zod for boundary parsing (CSV import, future API responses) vs. hand-rolled type guards. → `overview.md`
6. **Tag merge log** — do we keep a record of "tag A was merged into tag B at time T" for audit / undo? Brief doesn't require it; v1 says no, v2 may revisit. → `identity.md`

---

## Done criteria for this document

The data model is "locked" when:

- [ ] Every entity above has a corresponding type file in `src/lib/domain/`
- [ ] Every "Tests to write" list has at least one RED test for each line item
- [ ] No additions to this document without a matching ADR or `docs/decisions/` entry
- [ ] Cross-entity invariants are testable from the storage layer (`src/lib/db/__tests__/`)
