// Verifies that the one-POST rule produced the right PostgreSQL types.
// The TVO project lost 80% of a migration to a silent VARCHAR-where-INTEGER
// bug — see docs/architecture/directus-schema-management.md "Lesson 3".

import { banner, directusRequest } from './lib/directus-request.mjs';
import { queryPg } from './lib/sql-migration.mjs';
import {
  verifyCheckConstraints,
  verifyRelations,
  verifyUniqueIndexes,
} from './lib/verify-relations-and-uniques.mjs';

banner('verify-schema');

const expectations = [
  // [collection, field, expected_directus_type, expected_pg_data_type, extras]
  ['day_entries', 'date', 'date', 'date', { is_unique: true, is_nullable: false }],
  ['day_entries', 'score', 'integer', 'integer', { is_nullable: false }],
  ['day_entries', 'note', 'text', 'text', { is_nullable: true }],
  ['day_entries', 'sub_scores', 'json', 'json', { is_nullable: true }],
  ['day_entries', 'sleep_hours', 'float', 'real', { is_nullable: true }],
  ['day_entries', 'created_at', 'timestamp', 'timestamp with time zone', { is_nullable: true }],

  ['tags', 'label', 'string', 'character varying', { is_nullable: false }],
  ['tags', 'category', 'string', 'character varying', { is_nullable: false }],
  ['tags', 'parent_id', 'uuid', 'uuid', { is_nullable: true }],
  ['tags', 'parent_episode_id', 'uuid', 'uuid', { is_nullable: true }],
  ['tags', 'project_id', 'uuid', 'uuid', { is_nullable: true }],
  ['tags', 'usage_count', 'integer', 'integer', { is_nullable: false }],
  ['tags', 'archived_at', 'timestamp', 'timestamp with time zone', { is_nullable: true }],

  // episodes — v1.5 verloop-and-episodes feature
  ['episodes', 'label', 'string', 'character varying', { is_nullable: false }],
  ['episodes', 'category', 'string', 'character varying', { is_nullable: false }],
  ['episodes', 'start_date', 'date', 'date', { is_nullable: false }],
  ['episodes', 'end_date', 'date', 'date', { is_nullable: true }],
  ['episodes', 'description', 'text', 'text', { is_nullable: true }],
  ['episodes', 'calendar_binding', 'json', 'json', { is_nullable: true }],
  ['episodes', 'archived_at', 'timestamp', 'timestamp with time zone', { is_nullable: true }],
  ['episodes', 'created_at', 'timestamp', 'timestamp with time zone', { is_nullable: true }],
  ['episodes', 'updated_at', 'timestamp', 'timestamp with time zone', { is_nullable: true }],

  // M2M junctions
  ['day_entries_tags', 'day_entries_id', 'uuid', 'uuid', { is_nullable: false }],
  ['day_entries_tags', 'tags_id', 'uuid', 'uuid', { is_nullable: false }],
  ['day_entries_tags', 'source', 'string', 'character varying', { is_nullable: true }],
  ['day_entries_tags', 'confidence', 'float', 'real', { is_nullable: true }],
  ['day_entries_tags', 'confirmed_at', 'timestamp', 'timestamp with time zone', { is_nullable: true }],

  ['project_entries_tags', 'project_entries_id', 'uuid', 'uuid', { is_nullable: false }],
  ['project_entries_tags', 'tags_id', 'uuid', 'uuid', { is_nullable: false }],
  ['project_entries_tags', 'source', 'string', 'character varying', { is_nullable: true }],

  ['projects', 'name', 'string', 'character varying', { is_nullable: false }],
  ['projects', 'type', 'string', 'character varying', { is_nullable: false }],
  ['projects', 'start_date', 'date', 'date', { is_nullable: false }],
  ['projects', 'status', 'string', 'character varying', { is_nullable: false }],

  // calendar_events — v1.6 multi-provider shape. Migrated from the v1
  // Google-specific placeholder. See features/calendar-binding/step-0.
  ['calendar_events', 'connection_id', 'uuid', 'uuid', { is_nullable: false }],
  ['calendar_events', 'provider', 'string', 'character varying', { is_nullable: false }],
  ['calendar_events', 'provider_event_id', 'string', 'character varying', { is_nullable: false }],
  ['calendar_events', 'recurrence_id', 'string', 'character varying', { is_nullable: true }],
  ['calendar_events', 'start_at', 'timestamp', 'timestamp with time zone', { is_nullable: false }],
  ['calendar_events', 'end_at', 'timestamp', 'timestamp with time zone', { is_nullable: false }],
  ['calendar_events', 'all_day', 'boolean', 'boolean', { is_nullable: false }],
  ['calendar_events', 'title', 'string', 'character varying', { is_nullable: false }],
  ['calendar_events', 'attendees_count', 'integer', 'integer', { is_nullable: false }],
  ['calendar_events', 'declined', 'boolean', 'boolean', { is_nullable: false }],
  // Step-0 amendment 2026-06-04: 6 additional fields for v1.6.x rules + v2 learned rules
  ['calendar_events', 'event_type', 'string', 'character varying', { is_nullable: true }],
  ['calendar_events', 'status', 'string', 'character varying', { is_nullable: false }],
  ['calendar_events', 'transparency', 'string', 'character varying', { is_nullable: false }],
  ['calendar_events', 'organizer_is_self', 'boolean', 'boolean', { is_nullable: false }],
  ['calendar_events', 'ical_uid', 'string', 'character varying', { is_nullable: true }],
  ['calendar_events', 'html_link', 'string', 'character varying', { is_nullable: true }],
  ['calendar_events', 'linked_tag_id', 'uuid', 'uuid', { is_nullable: true }],
  ['calendar_events', 'linked_episode_id', 'uuid', 'uuid', { is_nullable: true }],
  ['calendar_events', 'included_as_context', 'boolean', 'boolean', { is_nullable: false }],
  ['calendar_events', 'user_decision', 'string', 'character varying', { is_nullable: false }],

  // calendar_connections — v1.6 per-user OAuth connection rows
  ['calendar_connections', 'user_id', 'uuid', 'uuid', { is_nullable: false }],
  ['calendar_connections', 'provider', 'string', 'character varying', { is_nullable: false }],
  ['calendar_connections', 'provider_account_email', 'string', 'character varying', { is_nullable: false }],
  ['calendar_connections', 'refresh_token_encrypted', 'text', 'text', { is_nullable: false }],
  ['calendar_connections', 'scope', 'string', 'character varying', { is_nullable: false }],
  ['calendar_connections', 'connected_at', 'timestamp', 'timestamp with time zone', { is_nullable: false }],
  ['calendar_connections', 'last_synced_at', 'timestamp', 'timestamp with time zone', { is_nullable: true }],
  ['calendar_connections', 'status', 'string', 'character varying', { is_nullable: false }],
  ['calendar_connections', 'included_calendar_ids', 'json', 'json', { is_nullable: false }],

  // calendar_series_exclusions — v1.6 user-excluded recurrences
  ['calendar_series_exclusions', 'connection_id', 'uuid', 'uuid', { is_nullable: false }],
  ['calendar_series_exclusions', 'recurrence_id', 'string', 'character varying', { is_nullable: false }],
  ['calendar_series_exclusions', 'excluded_at', 'timestamp', 'timestamp with time zone', { is_nullable: false }],

  // cron_monitor — shared infra (introduced v1.6)
  ['cron_monitor', 'job_name', 'string', 'character varying', { is_nullable: false }],
  ['cron_monitor', 'last_run_at', 'timestamp', 'timestamp with time zone', { is_nullable: true }],
  ['cron_monitor', 'expected_interval_hours', 'integer', 'integer', { is_nullable: false }],
  ['cron_monitor', 'is_active', 'boolean', 'boolean', { is_nullable: false }],

  ['garmin_daily', 'date', 'date', 'date', { is_unique: true, is_nullable: false }],
  ['health_daily', 'date', 'date', 'date', { is_unique: true, is_nullable: false }],
  ['weather_daily', 'date', 'date', 'date', { is_unique: true, is_nullable: false }],
];

const failures = [];
const passes = [];

for (const [collection, field, dType, pgType, extras] of expectations) {
  try {
    const res = await directusRequest(`/fields/${collection}/${field}`);
    const data = res.data;
    const actualDType = data.type;
    const actualPgType = data.schema?.data_type;

    const issues = [];
    if (actualDType !== dType) {
      issues.push(`directus type: expected ${dType}, got ${actualDType}`);
    }
    if (actualPgType !== pgType) {
      issues.push(`pg data_type: expected ${pgType}, got ${actualPgType}`);
    }
    for (const [key, expectedVal] of Object.entries(extras)) {
      const actualVal = data.schema?.[key];
      if (actualVal !== expectedVal) {
        issues.push(`schema.${key}: expected ${expectedVal}, got ${actualVal}`);
      }
    }

    if (issues.length === 0) {
      passes.push(`${collection}.${field}`);
      console.log(`  ✅ ${collection}.${field}`);
    } else {
      failures.push({ collection, field, issues });
      console.log(`  ❌ ${collection}.${field}`);
      issues.forEach((i) => console.log(`     - ${i}`));
    }
  } catch (e) {
    failures.push({ collection, field, issues: [`fetch failed: ${e.message}`] });
    console.log(`  ❌ ${collection}.${field} — ${e.message}`);
  }
}

console.log('\n' + '─'.repeat(64));
console.log(`  Field-level passed: ${passes.length}/${expectations.length}`);
console.log(`  Field-level failed: ${failures.length}/${expectations.length}`);
console.log('─'.repeat(64) + '\n');

// ────────────────────────────────────────────────────────────────────────
// Step 0 / AC0.10: FK on_delete behavior. Six relations defined in
// upgrade-m2m-tags.mjs + setup-schema.mjs + add-tag-hierarchy.mjs +
// add-episodes.mjs. The /relations API exposes schema.on_delete; CASCADE
// vs SET NULL is load-bearing and must not regress silently.
// ────────────────────────────────────────────────────────────────────────

console.log('─ Relation on_delete checks ─');

const relationExpectations = [
  { collection: 'day_entries_tags', field: 'day_entries_id', related_collection: 'day_entries', on_delete: 'CASCADE' },
  { collection: 'day_entries_tags', field: 'tags_id', related_collection: 'tags', on_delete: 'CASCADE' },
  { collection: 'project_entries_tags', field: 'project_entries_id', related_collection: 'project_entries', on_delete: 'CASCADE' },
  { collection: 'project_entries_tags', field: 'tags_id', related_collection: 'tags', on_delete: 'CASCADE' },
  { collection: 'tags', field: 'parent_id', related_collection: 'tags', on_delete: 'SET NULL' },
  { collection: 'tags', field: 'parent_episode_id', related_collection: 'episodes', on_delete: 'SET NULL' },

  // calendar-binding v1.6 — cascade chain on Ontkoppel: disconnecting
  // a calendar_connections row cascades to its events + series_exclusions.
  // Linked tag/episode references SET NULL so deletion of a tag/episode
  // doesn't drop the event row (the event survives as an unlinked event).
  { collection: 'calendar_events', field: 'connection_id', related_collection: 'calendar_connections', on_delete: 'CASCADE' },
  { collection: 'calendar_events', field: 'linked_tag_id', related_collection: 'tags', on_delete: 'SET NULL' },
  { collection: 'calendar_events', field: 'linked_episode_id', related_collection: 'episodes', on_delete: 'SET NULL' },
  { collection: 'calendar_connections', field: 'user_id', related_collection: 'directus_users', on_delete: 'CASCADE' },
  { collection: 'calendar_series_exclusions', field: 'connection_id', related_collection: 'calendar_connections', on_delete: 'CASCADE' },
];

const relationResult = await verifyRelations(directusRequest, relationExpectations);
for (const name of relationResult.passes) console.log(`  ✅ ${name}`);
for (const f of relationResult.failures) {
  console.log(`  ❌ ${f.name}`);
  for (const issue of f.issues) console.log(`     - ${issue}`);
}
console.log(`  ${relationResult.passes.length}/${relationExpectations.length} passed`);

// ────────────────────────────────────────────────────────────────────────
// Step 0 / AC0.11: UNIQUE indexes (composite + partial). Queried via
// pg_indexes since Directus' field API doesn't expose composite/partial
// uniqueness. Requires DATABASE_URL from the Neon connection string.
// ────────────────────────────────────────────────────────────────────────

console.log('\n─ UNIQUE index checks ─');

const indexExpectations = [
  {
    indexname: 'day_entries_tags_unique_pair',
    definitionMustMatch: /UNIQUE INDEX day_entries_tags_unique_pair.*ON.*day_entries_tags.*\(day_entries_id, tags_id\)/i,
  },
  {
    indexname: 'project_entries_tags_unique_pair',
    definitionMustMatch: /UNIQUE INDEX project_entries_tags_unique_pair.*ON.*project_entries_tags.*\(project_entries_id, tags_id\)/i,
  },
  {
    indexname: 'tags_label_category_active_unique',
    // PG renders the index def as `lower((label)::text), category` after
    // implicit text-casting. We assert lower() + label + category + the
    // partial WHERE; the exact tokenization between is PG's business.
    definitionMustMatch: /UNIQUE INDEX tags_label_category_active_unique.*ON.*tags.*lower.*label.*category.*WHERE \(?archived_at IS NULL\)?/i,
  },
  {
    indexname: 'episodes_label_category_active_unique',
    definitionMustMatch: /UNIQUE INDEX episodes_label_category_active_unique.*ON.*episodes.*lower.*label.*category.*WHERE \(?archived_at IS NULL\)?/i,
  },

  // calendar-binding v1.6 — UNIQUE composites for idempotent upsert + per-recurrence exclusion
  {
    indexname: 'calendar_events_provider_event_unique',
    definitionMustMatch: /UNIQUE INDEX calendar_events_provider_event_unique.*ON.*calendar_events.*\(connection_id, provider_event_id\)/i,
  },
  {
    indexname: 'calendar_connections_user_provider_email_unique',
    definitionMustMatch: /UNIQUE INDEX calendar_connections_user_provider_email_unique.*ON.*calendar_connections.*\(user_id, provider, provider_account_email\)/i,
  },
  {
    indexname: 'calendar_series_exclusions_unique',
    definitionMustMatch: /UNIQUE INDEX calendar_series_exclusions_unique.*ON.*calendar_series_exclusions.*\(connection_id, recurrence_id\)/i,
  },
  {
    indexname: 'cron_monitor_job_name_unique',
    definitionMustMatch: /UNIQUE INDEX cron_monitor_job_name_unique.*ON.*cron_monitor.*\(job_name\)/i,
  },

  // calendar-binding v1.6 — performance indexes (non-unique) for date-range + series queries
  {
    indexname: 'calendar_events_connection_start_idx',
    definitionMustMatch: /INDEX calendar_events_connection_start_idx.*ON.*calendar_events.*\(connection_id, start_at\)/i,
  },
  {
    indexname: 'calendar_events_connection_recurrence_idx',
    definitionMustMatch: /INDEX calendar_events_connection_recurrence_idx.*ON.*calendar_events.*\(connection_id, recurrence_id\)/i,
  },
];

let indexResult = { passes: [], failures: [] };
try {
  indexResult = await verifyUniqueIndexes(queryPg, indexExpectations);
  for (const name of indexResult.passes) console.log(`  ✅ ${name}`);
  for (const f of indexResult.failures) {
    console.log(`  ❌ ${f.name}`);
    for (const issue of f.issues) console.log(`     - ${issue}`);
  }
  console.log(`  ${indexResult.passes.length}/${indexExpectations.length} passed`);
} catch (e) {
  console.log(`  ⚠️  UNIQUE-index checks skipped: ${(e && e.message ? e.message : String(e)).split('\n')[0]}`);
  // Surface as a failure so verify-schema exit code reflects the gap.
  indexResult = {
    passes: [],
    failures: indexExpectations.map((x) => ({
      name: x.indexname,
      issues: ['PG check could not run; verify DATABASE_URL is set'],
    })),
  };
}

// ────────────────────────────────────────────────────────────────────────
// Step 0b / AC0b.5: CHECK constraints (tier 3 hardening).
// ────────────────────────────────────────────────────────────────────────

console.log('\n─ CHECK constraint checks ─');

const checkExpectations = [
  {
    conname: 'tags_category_check',
    table: 'tags',
    // PG canonicalizes `IN (...)` into `= ANY (ARRAY[...])`. Match the
    // actual rendered form by checking the enum values, not the syntax.
    definitionMustMatch: /category.*mentaal.*fysiek.*overall.*custom/i,
  },
  {
    conname: 'episodes_category_check',
    table: 'episodes',
    definitionMustMatch: /category.*interventie.*levensgebeurtenis/i,
  },
  {
    conname: 'day_entries_score_check',
    table: 'day_entries',
    definitionMustMatch: /score.*1.*10/i,
  },
  {
    conname: 'day_entries_sleep_hours_check',
    table: 'day_entries',
    definitionMustMatch: /sleep_hours.*(NULL|0).*24/i,
  },
  {
    conname: 'episodes_date_order_check',
    table: 'episodes',
    definitionMustMatch: /end_date.*NULL.*start_date/i,
  },
  {
    conname: 'day_entries_tags_confidence_check',
    table: 'day_entries_tags',
    definitionMustMatch: /confidence.*(NULL|0).*1/i,
  },
  {
    conname: 'project_entries_tags_confidence_check',
    table: 'project_entries_tags',
    definitionMustMatch: /confidence.*(NULL|0).*1/i,
  },

  // calendar-binding v1.6 — enum + range CHECK constraints
  {
    conname: 'calendar_connections_status_check',
    table: 'calendar_connections',
    definitionMustMatch: /status.*active.*disconnected.*error/i,
  },
  {
    conname: 'calendar_connections_provider_check',
    table: 'calendar_connections',
    definitionMustMatch: /provider.*google/i,
  },
  {
    conname: 'calendar_events_provider_check',
    table: 'calendar_events',
    definitionMustMatch: /provider.*google/i,
  },
  {
    conname: 'calendar_events_user_decision_check',
    table: 'calendar_events',
    definitionMustMatch: /user_decision.*auto.*user_included.*user_excluded/i,
  },
  {
    conname: 'calendar_events_end_after_start_check',
    table: 'calendar_events',
    definitionMustMatch: /end_at.*start_at/i,
  },
  // Step-0 amendment 2026-06-04: status enum CHECK
  {
    conname: 'calendar_events_status_check',
    table: 'calendar_events',
    definitionMustMatch: /status.*confirmed.*tentative.*cancelled/i,
  },
];

let checkResult = { passes: [], failures: [] };
try {
  checkResult = await verifyCheckConstraints(queryPg, checkExpectations);
  for (const name of checkResult.passes) console.log(`  ✅ ${name}`);
  for (const f of checkResult.failures) {
    console.log(`  ❌ ${f.name}`);
    for (const issue of f.issues) console.log(`     - ${issue}`);
  }
  console.log(`  ${checkResult.passes.length}/${checkExpectations.length} passed`);
} catch (e) {
  console.log(`  ⚠️  CHECK-constraint checks skipped: ${(e && e.message ? e.message : String(e)).split('\n')[0]}`);
  checkResult = {
    passes: [],
    failures: checkExpectations.map((x) => ({
      name: x.conname,
      issues: ['PG check could not run; verify DATABASE_URL is set'],
    })),
  };
}

// ────────────────────────────────────────────────────────────────────────
// Combined exit
// ────────────────────────────────────────────────────────────────────────

const totalFailures =
  failures.length +
  relationResult.failures.length +
  indexResult.failures.length +
  checkResult.failures.length;

console.log('\n' + '─'.repeat(64));
console.log(
  `  TOTAL passed: ${passes.length + relationResult.passes.length + indexResult.passes.length + checkResult.passes.length}` +
    ` / failed: ${totalFailures}`,
);
console.log('─'.repeat(64) + '\n');

if (totalFailures > 0) {
  if (failures.length > 0) {
    console.log('Field-level failures detail:');
    for (const f of failures) {
      console.log(`  ${f.collection}.${f.field}:`);
      f.issues.forEach((i) => console.log(`    - ${i}`));
    }
  }
  process.exit(1);
}

console.log('✅ All schema checks passed.\n');
