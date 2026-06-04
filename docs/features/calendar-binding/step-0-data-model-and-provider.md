# Step 0: Data model + CalendarProvider interface + cron_monitor

**Estimated time:** ~6 hours. Three new collections + one migration of an empty placeholder + envelope-encryption helper + CalendarProvider interface (no implementation) + smart-default-rules domain function + verify-schema extensions + stale-comment update on `episodes.calendar_binding`.
**Test layers:** Vitest unit tests for envelope-encryption (round-trip / tamper / wrong KEK), smart-default rules (3 rules + series-exclusion override), CalendarProvider interface contract (shape-check). Vitest unit tests for the new `src/lib/api/calendars.ts` Directus wrapper. Idempotent setup script smokes against the production Directus.
**Risk:** Medium. The schema migration drops Google-specific columns from the placeholder `calendar_events`. The collection is empty in production (per the v1 reservation rule); the migration script asserts `COUNT(*) = 0` before dropping columns. Refresh tokens don't exist yet (no connections), so the encryption helper has no production data to break.
**Prerequisite:** none (Step 0 is always first). Tag-merge step-0's `verify-schema.mjs` pattern + tier 3 CHECK constraint pattern (commits `36737f5..103ace6`) are the references to mirror.

> Step-0 ships only the data foundation. No OAuth, no UI, no routes, no cron jobs. Those come in step-1 + step-2.

---

## Acceptance criteria (subset of feature README's criteria delivered by this step)

### Domain: CalendarProvider interface + canonical CalendarEvent

- [ ] **AC0.1** `src/lib/integrations/calendar-provider.ts` exports a `CalendarProvider` interface with the 6 methods enumerated in the README's "Key types" section: `buildAuthUrl`, `exchangeCode`, `refreshAccessToken`, `listCalendars`, `fetchEvents`, `revoke`. Plus a `id` string discriminator (`'google' | 'outlook' | 'apple'`).
- [ ] **AC0.2** `src/lib/integrations/calendar-provider.ts` exports a canonical `CalendarEvent` type with the 9 fields in the README: `providerEventId`, `recurrenceId`, `startAt`, `endAt`, `allDay`, `title`, `location`, `attendeesCount`, `declined`. **No** provider-specific fields (no `googleEventId`, no `etag`, no `htmlLink` — those stay in the Google adapter).
- [ ] **AC0.3** No implementation. Interface only. The Google implementation lands in step-1.

### Domain: smart-default rules

- [ ] **AC0.4** `src/lib/domain/calendar-event.ts` exports `computeDefaultIncluded(event: CalendarEvent, seriesExclusions: Set<string>): { included: boolean; reason: 'all_day' | 'recurring' | 'declined' | 'series_excluded' | 'default' }`. The three rules in the README applied in order: series-exclusion check first (highest priority); declined RSVP → false; all-day → true; recurring (recurrenceId !== null) → true; else → true.
- [ ] **AC0.5** Reason field captures the rule that fired. Used by tests + future v2 learned-rules aggregation.
- [ ] **AC0.6** No keyword stoplist. The function does NOT look at event title content.
- [ ] **AC0.7** Pure function: same input → same output. No I/O, no Date.now(), no Math.random().

### Encryption: envelope-encryption helper

- [ ] **AC0.8** `src/lib/auth/envelope-encryption.ts` exports `encrypt(plaintext: string, kek: string): string` and `decrypt(ciphertext: string, kek: string): string`. The KEK is read from `CALENDAR_KEK` Fly secret at the call site, not embedded in the helper (so tests can inject test keys).
- [ ] **AC0.9** AES-GCM with a per-call random IV. Output format: `v1.<base64-iv>.<base64-ciphertext>.<base64-authtag>`. The `v1` prefix supports future algorithm rotation without breaking existing rows.
- [ ] **AC0.10** Round-trip: `decrypt(encrypt(p, k), k) === p`.
- [ ] **AC0.11** Tamper detection: flipping any byte of the ciphertext or authtag → decrypt throws.
- [ ] **AC0.12** Wrong KEK: decrypt with a different KEK → throws.
- [ ] **AC0.13** Built-in Node `crypto` only. No `node-forge`, no `crypto-js`, no `tweetnacl`.

### Directus wrapper (initial, no live methods yet — types + smoke read)

- [ ] **AC0.14** `src/lib/api/calendars.ts` exports the four Directus row types (`DirectusCalendarConnectionRow`, `DirectusCalendarEventRow`, `DirectusCalendarSeriesExclusionRow`, `DirectusCronMonitorRow`) matching the README's "Key types".
- [ ] **AC0.15** `src/lib/api/calendars.ts` extends the existing `DirectusSchema` type union with the four new collections so `tags.ts` / `episodes.ts` / `day-entries.ts` patterns can be followed in step-1 without re-defining the schema.
- [ ] **AC0.16** A minimal smoke method `getCronMonitorJob(accessToken, jobName: string): Promise<Result<DirectusCronMonitorRow | null, 'directus_error'>>` (used by step-2 health endpoint; needed in step-0 so the verify gate has something to test the wrapper against).

### Directus schema: migration of `calendar_events` placeholder

- [ ] **AC0.17** `directus/scripts/setup-calendar-collections.mjs` asserts `SELECT COUNT(*) FROM calendar_events = 0` before any destructive operation. If non-zero, errors with `calendar_events not empty; refusing to migrate. Run the v1.6.1 backfill (out of scope here) first.` Exit non-zero.
- [ ] **AC0.18** Migration drops these v1 placeholder columns from `calendar_events`: `google_event_id`, `calendar_source`, `relevance`, `category_hint`. The collection metadata note is updated from "v1.5: ..." to "v1.6: multi-provider calendar events; see docs/features/calendar-binding/".
- [ ] **AC0.19** Migration adds these v1.6 columns to `calendar_events`: `connection_id` (FK to `calendar_connections.id`, ON DELETE CASCADE), `provider` (string, max 20, NOT NULL), `provider_event_id` (string, max 200, NOT NULL — replaces `google_event_id`), `recurrence_id` (string, max 200, nullable), `start_at` (timestamptz NOT NULL — replaces `start_time`), `end_at` (timestamptz NOT NULL — replaces `end_time`), `declined` (boolean NOT NULL default false), `linked_tag_id` (FK to `tags.id`, nullable, ON DELETE SET NULL), `linked_episode_id` (FK to `episodes.id`, nullable, ON DELETE SET NULL), `included_as_context` (boolean NOT NULL default true), `user_decision` (string max 20 NOT NULL default 'auto').
- [ ] **AC0.20** `calendar_events.date` column is removed (the multi-provider shape uses `start_at` / `end_at`; date is derived). `title` + `all_day` + `location` + `attendees_count` are preserved (already exist).

### Directus schema: new collections

- [ ] **AC0.21** `calendar_connections` collection created with fields: `id` (uuid PK), `user_id` (FK to `directus_users.id` ON DELETE CASCADE), `provider` (string max 20 NOT NULL), `provider_account_email` (string max 320 NOT NULL), `refresh_token_encrypted` (text NOT NULL), `scope` (string max 500 NOT NULL), `connected_at` (timestamptz NOT NULL), `last_synced_at` (timestamptz nullable), `last_sync_error` (text nullable), `status` (string max 20 NOT NULL default `active`), `included_calendar_ids` (jsonb NOT NULL default `'[]'::jsonb`).
- [ ] **AC0.22** `calendar_series_exclusions` collection created with fields: `id` (uuid PK), `connection_id` (FK to `calendar_connections.id` ON DELETE CASCADE), `recurrence_id` (string max 200 NOT NULL), `excluded_at` (timestamptz NOT NULL).
- [ ] **AC0.23** `cron_monitor` collection created with fields: `id` (uuid PK), `job_name` (string max 100 NOT NULL), `last_run_at` (timestamptz nullable), `last_result` (text nullable, max 1000 chars enforced by app — see step-2), `expected_interval_hours` (integer NOT NULL default 26), `is_active` (boolean NOT NULL default true).

### Directus schema: UNIQUE / INDEX / CHECK constraints

- [ ] **AC0.24** `UNIQUE(connection_id, provider_event_id)` on `calendar_events` (idempotent upsert).
- [ ] **AC0.25** `UNIQUE(user_id, provider, provider_account_email)` on `calendar_connections` (idempotent connect).
- [ ] **AC0.26** `UNIQUE(connection_id, recurrence_id)` on `calendar_series_exclusions`.
- [ ] **AC0.27** `UNIQUE(job_name)` on `cron_monitor`.
- [ ] **AC0.28** `INDEX (connection_id, start_at)` on `calendar_events` for date-range queries.
- [ ] **AC0.29** `INDEX (connection_id, recurrence_id)` on `calendar_events` for series operations.
- [ ] **AC0.30** `CHECK (status IN ('active', 'disconnected', 'error'))` on `calendar_connections`.
- [ ] **AC0.31** `CHECK (provider IN ('google'))` on `calendar_connections` (will widen when step-5 Outlook lands).
- [ ] **AC0.32** `CHECK (provider IN ('google'))` on `calendar_events` (same widening trigger).
- [ ] **AC0.33** `CHECK (user_decision IN ('auto', 'user_included', 'user_excluded'))` on `calendar_events`.
- [ ] **AC0.34** `CHECK (end_at >= start_at)` on `calendar_events` (event end can't be before start).

### Directus schema: cron_monitor seed row

- [ ] **AC0.35** A `daily_calendar_sync` row exists in `cron_monitor` with `expected_interval_hours = 26` (24h + 2h buffer per programmeerprobeer's pattern), `is_active = true`, `last_run_at = NULL`. Inserted idempotently (`ON CONFLICT (job_name) DO NOTHING`).

### Stale comment update on episodes

- [ ] **AC0.36** `src/lib/domain/episode.ts` line 14-15 comment updated from "v1.6 calendar binding" to "v1.6.1 calendar-bound episodes (see docs/features/calendar-binding/ Future considerations)". No code change; the validator still rejects non-null calendar_binding.
- [ ] **AC0.37** `src/lib/api/episodes.ts` lines 105-108 comment updated identically.
- [ ] **AC0.38** Domain test `src/lib/domain/__tests__/episode.test.ts` line 215 description updated from `(v1.5 gate)` to `(v1.6 gate — column remains locked; reserved for v1.6.1)`. No behavior change.

### Verify-schema additions

- [ ] **AC0.39** `directus/scripts/verify-schema.mjs` adds 4 new UNIQUE assertions, 2 new INDEX assertions, 5 new CHECK assertions, 7 new FK on_delete assertions (cascade chain). Same pattern as the existing 56 assertions.
- [ ] **AC0.40** Running `node directus/scripts/verify-schema.mjs` against production reports `XX/XX OK` (current 56 + AC0.39 additions). All assertions GREEN before step-0 is checkpointed.

---

## Technical constraints (applicable to this step)

- **Migration assertion: `calendar_events` is empty in production.** The script reads `COUNT(*)` first and refuses to run if non-zero. Defensive; the column drops are non-reversible without a backup. v1 reservation rule guarantees emptiness, but the runtime check is non-negotiable.
- **No data migration logic.** The collection is empty. We drop the v1.5 columns + add v1.6 columns. No row-level rewrites. If the assertion fails, the developer is on their own to figure out where rows came from (manual admin writes?).
- **Envelope encryption uses Node built-in `crypto`.** No third-party crypto deps. The KEK is a 32-byte secret read from `CALENDAR_KEK` Fly env var; tests inject a test key.
- **Encryption helper is pure** (same KEK + same plaintext + same IV = same ciphertext). For test determinism, the IV is taken from a `crypto.randomBytes`-like injectable function. The default uses `crypto.randomBytes(12)` for AES-GCM. Test override exposes a deterministic IV generator.
- **No OAuth code in step-0.** The CalendarProvider interface is a typed shape only. Step-1 implements `google-provider.ts`.
- **No routes in step-0.** No `/api/calendars/*`. Those land in step-1.
- **No UI in step-0.** No Settings → Kalenders, no Context-tab section. Those land in step-1.
- **No cron in step-0.** No GHA workflow, no health endpoint. Those land in step-2. The `cron_monitor` collection + seed row land here so step-2 has a foundation.
- **`episodes.calendar_binding` stays locked.** Comment-only update; the validator still rejects non-null. No behavior change.
- **The 4 calendar collections + cron_monitor land in one idempotent setup script** that can be re-run safely. Pattern: `setup-calendar-collections.mjs` is the equivalent of programmeerprobeer's `setup-cron-monitor-reporting.js` — POST-or-skip every collection / field / relation / constraint.

### Standards-enforcement declaration

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01, A03, A04, A07, A08 | No | No routes in step-0. Routes added in step-1 + step-2. |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | Yes | 3 new collections (`calendar_connections`, `calendar_series_exclusions`, `cron_monitor`) + migrated `calendar_events`. Export coverage planned in step-1 (no export trigger in step-0). Retention: lifecycle managed by `Ontkoppel` + full-delete cascade in step-1. Audit-log INSERT NOT required (single-user app; existing convention is `created_at` field as audit). |
| New dependency | ADR or step rationale | No | No new external deps in step-0. Built-in `crypto` only. |
| `dangerouslySetInnerHTML` usage | A03 | No | No UI in step-0. |
| New env var with a secret | A02, A05 | Yes | `CALENDAR_KEK` Fly secret (32-byte base64). Set in step-0 setup checklist; never `NEXT_PUBLIC_*`; never committed. |
| New telemetry / observability dep | Cardinal "no telemetry" | No | None. |

---

## Test plan

Copy-pasteable test code below for each layer. One `it` block per AC (or per logical micro-AC where ACs are compound). File paths explicit.

### Domain: CalendarProvider interface contract

**File**: `src/lib/integrations/__tests__/calendar-provider.test.ts`

```typescript
import { describe, expect, it } from 'vitest';
import type { CalendarProvider, CalendarEvent } from '../calendar-provider';

describe('calendar-provider', () => {
  describe('CalendarProvider interface shape (AC0.1)', () => {
    it('has all 6 required methods + id discriminator', () => {
      // This test exists to lock the interface shape. If the interface
      // changes, the test must be updated explicitly.
      const mockProvider: CalendarProvider = {
        id: 'google',
        buildAuthUrl: () => 'https://example.test/auth',
        exchangeCode: async () => ({
          refreshToken: 't', accessToken: 'a',
          expiresAt: new Date(0), accountEmail: 'e@example.test',
        }),
        refreshAccessToken: async () => ({ accessToken: 'a', expiresAt: new Date(0) }),
        listCalendars: async () => [],
        fetchEvents: async () => [],
        revoke: async () => {},
      };
      expect(mockProvider.id).toBe('google');
    });
  });

  describe('CalendarEvent canonical shape (AC0.2)', () => {
    it('has all 9 required fields and no provider-specific extensions', () => {
      const event: CalendarEvent = {
        providerEventId: 'evt-1',
        recurrenceId: null,
        startAt: new Date('2026-06-04T10:00:00Z'),
        endAt: new Date('2026-06-04T11:00:00Z'),
        allDay: false,
        title: 'Fysiotherapie',
        location: 'Praktijk',
        attendeesCount: 1,
        declined: false,
      };
      const keys = Object.keys(event).sort();
      expect(keys).toEqual([
        'allDay', 'attendeesCount', 'declined', 'endAt', 'location',
        'providerEventId', 'recurrenceId', 'startAt', 'title',
      ]);
    });
  });
});
```

### Domain: smart-default rules

**File**: `src/lib/domain/__tests__/calendar-event.test.ts`

```typescript
import { describe, expect, it } from 'vitest';
import { computeDefaultIncluded } from '../calendar-event';
import type { CalendarEvent } from '../../integrations/calendar-provider';

function baseEvent(overrides: Partial<CalendarEvent> = {}): CalendarEvent {
  return {
    providerEventId: 'evt-default',
    recurrenceId: null,
    startAt: new Date('2026-06-04T10:00:00Z'),
    endAt: new Date('2026-06-04T11:00:00Z'),
    allDay: false,
    title: 'Default event',
    location: null,
    attendeesCount: 0,
    declined: false,
    ...overrides,
  };
}

describe('calendar-event', () => {
  describe('computeDefaultIncluded — three smart-default rules', () => {
    it('series-excluded event resolves to excluded with reason=series_excluded (AC0.4)', () => {
      const event = baseEvent({ recurrenceId: 'rec-yoga' });
      const result = computeDefaultIncluded(event, new Set(['rec-yoga']));
      expect(result).toEqual({ included: false, reason: 'series_excluded' });
    });

    it('declined RSVP resolves to excluded with reason=declined (AC0.4)', () => {
      const event = baseEvent({ declined: true });
      const result = computeDefaultIncluded(event, new Set());
      expect(result).toEqual({ included: false, reason: 'declined' });
    });

    it('all-day event resolves to included with reason=all_day (AC0.4)', () => {
      const event = baseEvent({ allDay: true });
      const result = computeDefaultIncluded(event, new Set());
      expect(result).toEqual({ included: true, reason: 'all_day' });
    });

    it('recurring event resolves to included with reason=recurring (AC0.4)', () => {
      const event = baseEvent({ recurrenceId: 'rec-coaching' });
      const result = computeDefaultIncluded(event, new Set());
      expect(result).toEqual({ included: true, reason: 'recurring' });
    });

    it('one-off non-declined event resolves to included with reason=default (AC0.4)', () => {
      const event = baseEvent();
      const result = computeDefaultIncluded(event, new Set());
      expect(result).toEqual({ included: true, reason: 'default' });
    });

    it('series-exclusion takes priority over all-day (AC0.4)', () => {
      const event = baseEvent({ allDay: true, recurrenceId: 'rec-holiday' });
      const result = computeDefaultIncluded(event, new Set(['rec-holiday']));
      expect(result).toEqual({ included: false, reason: 'series_excluded' });
    });

    it('series-exclusion takes priority over declined (AC0.4)', () => {
      // Defensive: if a series has been excluded and a member is also declined,
      // we honor the series rule. The user_decision is set explicitly when
      // they exclude; no ambiguity.
      const event = baseEvent({ declined: true, recurrenceId: 'rec-deep-meeting' });
      const result = computeDefaultIncluded(event, new Set(['rec-deep-meeting']));
      expect(result).toEqual({ included: false, reason: 'series_excluded' });
    });

    it('no keyword stoplist; title content is ignored (AC0.6)', () => {
      const event = baseEvent({ title: 'Standup with team' });
      const result = computeDefaultIncluded(event, new Set());
      expect(result).toEqual({ included: true, reason: 'default' });
    });

    it('pure: same input twice yields same output (AC0.7)', () => {
      const event = baseEvent({ recurrenceId: 'rec-foo' });
      const exclusions = new Set(['rec-foo']);
      const a = computeDefaultIncluded(event, exclusions);
      const b = computeDefaultIncluded(event, exclusions);
      expect(a).toEqual(b);
    });
  });
});
```

### Encryption: envelope-encryption helper

**File**: `src/lib/auth/__tests__/envelope-encryption.test.ts`

```typescript
import { describe, expect, it } from 'vitest';
import { encrypt, decrypt } from '../envelope-encryption';

// 32-byte base64 test KEKs. Generated with `openssl rand -base64 32`.
// SAFE TO COMMIT: these are test fixtures only.
const KEK_A = 'Pl/MWtPFs1lwGyN4nQqzhDtIRiOJfP8j+kHRsZ7TgXg=';
const KEK_B = 'YkW2K5sN0p7uVcD+aFr/I5LqxRz1y7sjJ4kP3vBgGoQ=';

describe('envelope-encryption', () => {
  describe('round-trip (AC0.10)', () => {
    it('decrypt(encrypt(p, k), k) === p for ascii', () => {
      const plaintext = 'fake_google_refresh_token_abc123';
      const ciphertext = encrypt(plaintext, KEK_A);
      expect(decrypt(ciphertext, KEK_A)).toBe(plaintext);
    });

    it('decrypt(encrypt(p, k), k) === p for utf-8', () => {
      const plaintext = 'ééé ñññ 한국어 🔐';
      const ciphertext = encrypt(plaintext, KEK_A);
      expect(decrypt(ciphertext, KEK_A)).toBe(plaintext);
    });

    it('decrypt(encrypt(p, k), k) === p for long strings (1KB)', () => {
      const plaintext = 'X'.repeat(1024);
      const ciphertext = encrypt(plaintext, KEK_A);
      expect(decrypt(ciphertext, KEK_A)).toBe(plaintext);
    });
  });

  describe('output format (AC0.9)', () => {
    it('output starts with v1. prefix and has three base64 segments separated by dots', () => {
      const ciphertext = encrypt('hello', KEK_A);
      expect(ciphertext).toMatch(/^v1\.[A-Za-z0-9+/=]+\.[A-Za-z0-9+/=]+\.[A-Za-z0-9+/=]+$/);
    });

    it('different calls produce different ciphertext (random IV)', () => {
      const a = encrypt('hello', KEK_A);
      const b = encrypt('hello', KEK_A);
      expect(a).not.toBe(b);
    });
  });

  describe('tamper detection (AC0.11)', () => {
    it('flipping a byte of the ciphertext segment throws on decrypt', () => {
      const ciphertext = encrypt('secret', KEK_A);
      const parts = ciphertext.split('.');
      // Mangle one byte of segment[2] (the ciphertext)
      const buf = Buffer.from(parts[2]!, 'base64');
      buf[0] = buf[0]! ^ 0x01;
      parts[2] = buf.toString('base64');
      const tampered = parts.join('.');
      expect(() => decrypt(tampered, KEK_A)).toThrow();
    });

    it('flipping a byte of the authtag segment throws on decrypt', () => {
      const ciphertext = encrypt('secret', KEK_A);
      const parts = ciphertext.split('.');
      const buf = Buffer.from(parts[3]!, 'base64');
      buf[0] = buf[0]! ^ 0x01;
      parts[3] = buf.toString('base64');
      const tampered = parts.join('.');
      expect(() => decrypt(tampered, KEK_A)).toThrow();
    });
  });

  describe('wrong KEK (AC0.12)', () => {
    it('decrypt with a different KEK throws', () => {
      const ciphertext = encrypt('secret', KEK_A);
      expect(() => decrypt(ciphertext, KEK_B)).toThrow();
    });
  });

  describe('version prefix (AC0.9)', () => {
    it('decrypt rejects ciphertext without v1. prefix', () => {
      expect(() => decrypt('v0.aaa.bbb.ccc', KEK_A)).toThrow(/unsupported version/i);
    });

    it('decrypt rejects ciphertext with too few segments', () => {
      expect(() => decrypt('v1.aaa.bbb', KEK_A)).toThrow();
    });
  });

  describe('no external deps (AC0.13)', () => {
    it('module imports only from "node:crypto"', async () => {
      // Static check: enforced by lint rule (eslint-no-restricted-imports
      // configured in step-0); this test documents the constraint.
      // Body: assert no `import` from anything other than node:crypto in the file.
      // (Lint catches it; this is a smoke for clarity.)
      const source = await import('node:fs/promises').then(fs =>
        fs.readFile('src/lib/auth/envelope-encryption.ts', 'utf8'),
      );
      const imports = source.match(/^import .* from ['"](.+)['"]/gm) || [];
      const externals = imports.filter(line => !line.includes('node:crypto'));
      expect(externals).toEqual([]);
    });
  });
});
```

### Directus wrapper: row types + cron_monitor smoke read

**File**: `src/lib/api/__tests__/calendars.test.ts`

```typescript
import { describe, expect, it, vi, beforeEach } from 'vitest';

const mocks = vi.hoisted(() => ({
  request: vi.fn(),
}));

vi.mock('@directus/sdk', () => ({
  createDirectus: () => ({
    with: () => ({
      with: () => ({ request: mocks.request }),
    }),
  }),
  rest: () => () => null,
  staticToken: () => () => null,
  readItems: (collection: string, opts: unknown) => ({ kind: 'readItems', collection, opts }),
}));

import { getCronMonitorJob } from '../calendars';

describe('calendars (Directus wrapper)', () => {
  beforeEach(() => {
    mocks.request.mockReset();
  });

  describe('getCronMonitorJob (AC0.16)', () => {
    it('returns the row when found', async () => {
      mocks.request.mockResolvedValue([{
        id: 'cm-1', job_name: 'daily_calendar_sync',
        last_run_at: '2026-06-03T03:00:00Z',
        last_result: 'ok',
        expected_interval_hours: 26, is_active: true,
      }]);
      const result = await getCronMonitorJob('fake-token', 'daily_calendar_sync');
      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value?.job_name).toBe('daily_calendar_sync');
        expect(result.value?.expected_interval_hours).toBe(26);
      }
    });

    it('returns null when no row found', async () => {
      mocks.request.mockResolvedValue([]);
      const result = await getCronMonitorJob('fake-token', 'unknown_job');
      expect(result).toEqual({ ok: true, value: null });
    });

    it('returns directus_error on network failure', async () => {
      mocks.request.mockRejectedValue(new Error('Network down'));
      const result = await getCronMonitorJob('fake-token', 'daily_calendar_sync');
      expect(result).toEqual({ ok: false, error: 'directus_error' });
    });
  });
});
```

### Directus collections setup (smoke against prod)

**File**: `directus/scripts/__tests__/setup-calendar-collections.test.ts`

```typescript
import { describe, expect, it } from 'vitest';
import { buildCollectionDefinitions } from '../lib/calendar-schema';

// The setup script is run via node (idempotent against prod). This unit
// test asserts the schema definitions match the README's "Key types"
// section before the script ever touches the wire.

describe('setup-calendar-collections schema', () => {
  it('calendar_connections has 11 fields including refresh_token_encrypted (AC0.21)', () => {
    const defs = buildCollectionDefinitions();
    const connections = defs.find(d => d.collection === 'calendar_connections');
    expect(connections).toBeDefined();
    const fieldNames = connections!.fields.map(f => f.field).sort();
    expect(fieldNames).toEqual([
      'connected_at', 'id', 'included_calendar_ids', 'last_sync_error',
      'last_synced_at', 'provider', 'provider_account_email',
      'refresh_token_encrypted', 'scope', 'status', 'user_id',
    ]);
  });

  it('calendar_events new shape has 14 fields, no google_event_id (AC0.18, AC0.19)', () => {
    const defs = buildCollectionDefinitions();
    const events = defs.find(d => d.collection === 'calendar_events');
    expect(events).toBeDefined();
    const fieldNames = events!.fields.map(f => f.field).sort();
    expect(fieldNames).toContain('provider');
    expect(fieldNames).toContain('provider_event_id');
    expect(fieldNames).toContain('recurrence_id');
    expect(fieldNames).toContain('start_at');
    expect(fieldNames).toContain('end_at');
    expect(fieldNames).toContain('linked_tag_id');
    expect(fieldNames).toContain('linked_episode_id');
    expect(fieldNames).toContain('included_as_context');
    expect(fieldNames).toContain('user_decision');
    expect(fieldNames).not.toContain('google_event_id');
    expect(fieldNames).not.toContain('calendar_source');
    expect(fieldNames).not.toContain('relevance');
    expect(fieldNames).not.toContain('category_hint');
  });

  it('calendar_series_exclusions has 4 fields (AC0.22)', () => {
    const defs = buildCollectionDefinitions();
    const exclusions = defs.find(d => d.collection === 'calendar_series_exclusions');
    expect(exclusions).toBeDefined();
    const fieldNames = exclusions!.fields.map(f => f.field).sort();
    expect(fieldNames).toEqual(['connection_id', 'excluded_at', 'id', 'recurrence_id']);
  });

  it('cron_monitor has 6 fields (AC0.23)', () => {
    const defs = buildCollectionDefinitions();
    const monitor = defs.find(d => d.collection === 'cron_monitor');
    expect(monitor).toBeDefined();
    const fieldNames = monitor!.fields.map(f => f.field).sort();
    expect(fieldNames).toEqual([
      'expected_interval_hours', 'id', 'is_active', 'job_name',
      'last_result', 'last_run_at',
    ]);
  });
});
```

### Migration empty-check (smoke against prod via a one-off script)

**File**: `directus/scripts/__tests__/calendar-events-migration-guard.test.ts`

```typescript
import { describe, expect, it } from 'vitest';
import { assertCalendarEventsEmpty } from '../lib/calendar-migration-guard';

describe('calendar-events migration guard (AC0.17)', () => {
  it('passes when count is 0', async () => {
    const fakeQuery = async () => [{ count: 0 }];
    await expect(assertCalendarEventsEmpty(fakeQuery)).resolves.toBeUndefined();
  });

  it('throws when count is > 0', async () => {
    const fakeQuery = async () => [{ count: 3 }];
    await expect(assertCalendarEventsEmpty(fakeQuery)).rejects.toThrow(/not empty/i);
  });

  it('throws on unexpected shape', async () => {
    const fakeQuery = async () => [];
    await expect(assertCalendarEventsEmpty(fakeQuery)).rejects.toThrow();
  });
});
```

### Verify-schema additions (smoke against prod)

**File**: `directus/scripts/__tests__/verify-relations-and-uniques.test.ts` (EXTEND existing file)

Add cases:

```typescript
describe('calendar-binding additions to verify-schema (AC0.39, AC0.40)', () => {
  it('detects UNIQUE(connection_id, provider_event_id) on calendar_events', async () => {
    // Pattern matches the existing assertions for day_entries_tags UNIQUE
    // from the v1.5c tag-merge step-0. See verify-relations-and-uniques.mjs:N.
  });

  it('detects UNIQUE(user_id, provider, provider_account_email) on calendar_connections', async () => {
    // ...
  });

  it('detects UNIQUE(connection_id, recurrence_id) on calendar_series_exclusions', async () => {
    // ...
  });

  it('detects UNIQUE(job_name) on cron_monitor', async () => {
    // ...
  });

  it('detects INDEX (connection_id, start_at) on calendar_events', async () => {
    // ...
  });

  it('detects INDEX (connection_id, recurrence_id) on calendar_events', async () => {
    // ...
  });

  it('detects CHECK status IN (active, disconnected, error) on calendar_connections', async () => {
    // ...
  });

  it('detects CHECK provider IN (google) on calendar_connections', async () => {
    // ...
  });

  it('detects CHECK provider IN (google) on calendar_events', async () => {
    // ...
  });

  it('detects CHECK user_decision IN (auto, user_included, user_excluded) on calendar_events', async () => {
    // ...
  });

  it('detects CHECK end_at >= start_at on calendar_events', async () => {
    // ...
  });

  it('detects FK on_delete CASCADE on calendar_events.connection_id', async () => {
    // ...
  });

  it('detects FK on_delete SET NULL on calendar_events.linked_tag_id', async () => {
    // ...
  });

  it('detects FK on_delete SET NULL on calendar_events.linked_episode_id', async () => {
    // ...
  });

  it('detects FK on_delete CASCADE on calendar_connections.user_id', async () => {
    // ...
  });

  it('detects FK on_delete CASCADE on calendar_series_exclusions.connection_id', async () => {
    // ...
  });
});
```

### Stale-comment update (smoke; just confirm the file content was edited)

**File**: `src/lib/domain/__tests__/episode.test.ts` (EXTEND existing test at line 215)

Update the existing test description from `(v1.5 gate)` → `(v1.6 gate — column reserved for v1.6.1)` per AC0.38. No new test code required; this is a description rename + a comment edit in the two source files.

---

## Done criteria

- [ ] Every AC above is GREEN
- [ ] RED was captured before implementation (output recorded below)
- [ ] GREEN was captured after implementation (output recorded below)
- [ ] Full suite still passes (no regressions; ~1233 tests + new tests stay GREEN)
- [ ] `npm run typecheck` clean
- [ ] `npm run lint` clean
- [ ] `node directus/scripts/verify-schema.mjs` reports XX/XX OK against production (current 56 + step-0 additions)
- [ ] `CALENDAR_KEK` Fly secret set (32-byte base64); confirmed via `fly secrets list -a gevoelscore-frontend` showing the name (NEVER the value)
- [ ] No new HIGH gate findings (cardinal / privacy / security / v1.5-v2)
- [ ] Walkthrough not applicable (no UI in step-0)
- [ ] Refactor pass complete (or "none needed" stated)

---

## Execution order (followed by `/build-step`)

### 0.1 Baseline

`calendar_events` is empty in production per the v1 reservation. Confirm:

```powershell
# Through Directus admin or the existing query helper.
# Manual sanity check; the setup script also asserts this at runtime.
```

Capture the existing production verifier output (`56/56 OK`) as the baseline — step-0 additions should bring it to `~70/70 OK`.

### 0.2 Write tests (RED)

For each test file enumerated above:

1. `src/lib/integrations/__tests__/calendar-provider.test.ts` — interface stub-throws-not-implemented in `calendar-provider.ts`.
2. `src/lib/domain/__tests__/calendar-event.test.ts` — function stub-throws-not-implemented in `calendar-event.ts`.
3. `src/lib/auth/__tests__/envelope-encryption.test.ts` — encrypt + decrypt stub-throws-not-implemented.
4. `src/lib/api/__tests__/calendars.test.ts` — `getCronMonitorJob` stub-throws-not-implemented.
5. `directus/scripts/__tests__/setup-calendar-collections.test.ts` — `buildCollectionDefinitions` stub.
6. `directus/scripts/__tests__/calendar-events-migration-guard.test.ts` — `assertCalendarEventsEmpty` stub.
7. `directus/scripts/__tests__/verify-relations-and-uniques.test.ts` — extend existing file.
8. `src/lib/domain/__tests__/episode.test.ts` — rename the existing v1.5-gate description.

Run:

```
npm test -- calendar-provider calendar-event envelope-encryption calendars setup-calendar-collections calendar-events-migration-guard
```

Must FAIL with `not implemented` for the stubs. Record the failure lines under Done.

### 0.3 Implement (GREEN)

Files to create:

- `src/lib/integrations/calendar-provider.ts` — interface + canonical CalendarEvent
- `src/lib/domain/calendar-event.ts` — `computeDefaultIncluded`
- `src/lib/auth/envelope-encryption.ts` — `encrypt` + `decrypt` (AES-GCM via `node:crypto`)
- `src/lib/api/calendars.ts` — row types + `getCronMonitorJob`
- `directus/scripts/lib/calendar-schema.mjs` — `buildCollectionDefinitions`
- `directus/scripts/lib/calendar-migration-guard.mjs` — `assertCalendarEventsEmpty`
- `directus/scripts/setup-calendar-collections.mjs` — idempotent POST-or-skip
- `directus/migrations/2026-XX-XX-calendar-binding-schema.sql` — DDL for indexes / constraints not creatable via Directus collection API
- `directus/scripts/add-calendar-unique-constraints.mjs` — runner wrapper
- `directus/scripts/add-cron-monitor.mjs` — seed `daily_calendar_sync` row

Files to modify:

- `directus/scripts/verify-schema.mjs` — add the assertions listed in AC0.39
- `directus/scripts/lib/verify-relations-and-uniques.mjs` — add helpers for CHECK + FK assertions if needed
- `src/lib/domain/episode.ts` — comment update on calendar_binding gate (v1.6 → v1.6.1)
- `src/lib/api/episodes.ts` — same comment update
- `src/lib/domain/__tests__/episode.test.ts` — description rename (line 215)

Run:

```
npm test -- calendar-provider calendar-event envelope-encryption calendars setup-calendar-collections calendar-events-migration-guard episode
```

Must PASS. Record the pass line under Done.

### 0.4 Apply to production (idempotent)

Set `CALENDAR_KEK`:

```powershell
$kek = [Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
# DO NOT echo. Pipe directly into fly secrets set.
fly secrets set CALENDAR_KEK=$kek -a gevoelscore-frontend
```

Run the setup script:

```powershell
# Wraps the admin token from .env.local without echoing it
.\scripts\run-setup-calendar-collections.ps1
```

Run the constraint adders:

```powershell
.\scripts\run-add-calendar-unique-constraints.ps1
.\scripts\run-add-cron-monitor.ps1
```

Verify:

```powershell
.\scripts\run-verify-schema.ps1
# Expected: 70/70 OK (or whatever 56 + AC0.39 additions sums to)
```

### 0.5 Regression check

```
npm test
```

Full suite GREEN — no regression on existing 1233 tests.

### 0.6 Refactor

Look for opportunities to:

- Hoist any duplicated row-type definitions from `calendars.ts` into a shared place (probably none — collections are unique to this feature).
- Extract any helper that's used by both the migration guard and the verify-schema additions.
- Consolidate CHECK / UNIQUE / FK assertions in `verify-relations-and-uniques.mjs` if there are obvious tooling patterns to lift out.

State "none needed" if nothing emerges.

### 0.7 Checkpoint

Safe to commit. Commit message:

```
calendar-binding/step-0: data model + provider interface + cron_monitor

Migrates the empty v1 placeholder `calendar_events` to the multi-provider
shape (provider + provider_event_id) and adds three new collections:
`calendar_connections` (encrypted refresh tokens), `calendar_series_exclusions`,
and `cron_monitor` (shared infrastructure for future scheduled jobs).

Adds the CalendarProvider interface + canonical CalendarEvent type (no
implementation; Google adapter lands in step-1). Adds smart-default-rules
domain function (3 rules: all-day include, recurring include, declined
exclude; no keyword stoplist). Adds AES-GCM envelope-encryption helper for
refresh-token at-rest encryption.

Updates the stale `episodes.calendar_binding` v1.6 comment to point at
v1.6.1 (calendar-bound episodes feature, deferred per the README's
Future considerations).

Acceptance criteria addressed: AC0.1 through AC0.40 (40/40).

Tests: 40 new tests across 8 files. Schema verifier ~70/70 GREEN against
production. Constraint-enforcement smoke pending step-1 (no events yet
to trigger CHECK violations).
```

---

## Done (filled in during `/build-step`)

- [x] **AC0.1-AC0.7** (CalendarProvider interface + canonical CalendarEvent + smart-default rules): tests in `src/lib/integrations/__tests__/calendar-provider.test.ts` (3) + `src/lib/domain/__tests__/calendar-event.test.ts` (9) GREEN.
- [x] **AC0.8-AC0.13** (AES-GCM envelope-encryption helper): tests in `src/lib/auth/__tests__/envelope-encryption.test.ts` (11) GREEN. Round-trip + tamper + wrong-KEK + version-prefix + no-external-deps all verified.
- [x] **AC0.14-AC0.16** (Directus wrapper row types + getCronMonitorJob): tests in `src/lib/api/__tests__/calendars.test.ts` (4) GREEN.
- [x] **AC0.17** (migration guard `assertCalendarEventsEmpty`): tests in `directus/scripts/__tests__/calendar-events-migration-guard.test.ts` (4) GREEN. Production guard ran successfully on 2026-06-04: confirmed `calendar_events` was empty before the destructive migration.
- [x] **AC0.18-AC0.23** (schema definitions for migrated + 3 new collections): tests in `directus/scripts/__tests__/setup-calendar-collections.test.ts` (5) GREEN. Schema applied to production successfully.
- [x] **AC0.24-AC0.34** (UNIQUE + INDEX + CHECK constraints + FK on_delete): applied via `directus/migrations/2026-06-03-calendar-binding-constraints.sql` + `directus/scripts/setup-calendar-collections.mjs` /relations registration. Verified by `verify-schema.mjs` against production.
- [x] **AC0.35** (cron_monitor seed row): `daily_calendar_sync` row seeded in production with `expected_interval_hours=26`, `is_active=true`. Idempotent.
- [x] **AC0.36-AC0.38** (v1.6 → v1.6.1 comment updates on `episodes.calendar_binding`): edits applied to [src/lib/domain/episode.ts](../../../src/lib/domain/episode.ts), [src/lib/api/episodes.ts](../../../src/lib/api/episodes.ts), and the test description at [src/lib/domain/__tests__/episode.test.ts:215](../../../src/lib/domain/__tests__/episode.test.ts#L215). No behavior change.
- [x] **AC0.39-AC0.40** (verify-schema extensions): added ~30 new field-level assertions + 5 FK relation + 4 UNIQUE + 2 INDEX + 5 CHECK + 1 status CHECK (from the amendment below). Production verifier reports **107/107 OK**.
- [x] **Amendment 2026-06-04** (eventType + status + transparency + organizerIsSelf + iCalUid + htmlLink): 6 additional fields added to the canonical `CalendarEvent` type + Directus column + verify-schema assertions. The status CHECK constraint enforces `IN ('confirmed','tentative','cancelled')`. Decision: capture-only in v1.6 (no new smart-default rules); v1.6.x keyword rules + v2 learned rules will use these signals.
- [x] **RED captured**: `npm test -- calendar` → `30 failed` (of 33 originally enumerated; 3 stub-tolerant passes for pure-type-shape assertions + 1 file-read static check) on 2026-06-03.
- [x] **GREEN captured**: `npm test` (full suite) → `1270 passing` on 2026-06-04 (was 1233 before step-0; +37 new tests, of which 35 from initial RED→GREEN and +2 from the amendment).
- [x] **Type check**: `npm run typecheck` clean.
- [x] **Lint**: `npm run lint` clean.
- [x] **Verify gate**: `npm run verify` clean (`93 test files / 1270 passed`).
- [x] **`CALENDAR_KEK` Fly secret set** on 2026-06-04 via [scripts/set-calendar-kek.ps1](../../../scripts/set-calendar-kek.ps1) (PowerShell 5.1-compatible RNG; value never echoed; Remove-Variable after).
- [x] **Production schema verifier**: `node directus/scripts/verify-schema.mjs` → `TOTAL passed: 107 / failed: 0` on 2026-06-04. 67 field-level + 11 FK + 10 UNIQUE/INDEX + 13 CHECK + 6 v1 placeholders.
- [x] **No new HIGH gate findings** (cardinal-principle / privacy / security / v1.5-v2 readiness all PASS — see README §5).
- [x] **Walkthrough**: not applicable (no UI in step-0).
- [x] **Refactor**: none needed. Each new file follows an established convention (`calendars.ts` mirrors `tags.ts`/`episodes.ts`; `setup-calendar-collections.mjs` mirrors `add-episodes.mjs`; `2026-06-03-calendar-binding-constraints.sql` mirrors `2026-06-03-tier3-check-constraints.sql`). The shared helpers (`idField`, `createdAtField`, `updatedAtField` in `calendar-schema.mjs` echo those in `setup-schema.mjs`) appear in only 2 places — the 3+-occurrence threshold for extraction isn't met.

---

## What this step does NOT do

- **No OAuth code.** No `google-provider.ts`, no token-exchange logic. The `CalendarProvider` interface is a typed shape only — the Google implementation lands in step-1.
- **No routes.** No `/api/calendars/*`. Those land in step-1 (OAuth + sync routes) and step-2 (cron + health).
- **No UI.** No Settings → Kalenders, no Context-tab section. Those land in step-1.
- **No cron / GHA / health endpoint.** Those land in step-2. The `cron_monitor` collection + seed row land here so step-2 has a foundation.
- **No unlock of `episodes.calendar_binding`.** Comment-only update (v1.6 → v1.6.1). The validator still rejects non-null. Calendar-bound episodes are v1.6.1 per Decision 7 in the README.
- **No data backfill or transformation.** Empty placeholder → empty new schema. The migration assertion guarantees this.
- **No keyword exclusion rules.** Deferred to v1.6.x per the README's Future considerations.
