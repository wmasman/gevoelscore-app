// Idempotent setup of the calendar-binding v1.6 schema:
//   - migrates the v1 calendar_events placeholder to the multi-provider shape
//     (asserts COUNT(*) = 0 first via assertCalendarEventsEmpty)
//   - creates calendar_connections, calendar_series_exclusions, cron_monitor
//   - registers Directus relations (FK in admin UI) for the 5 FK columns
//
// SQL constraints (UNIQUE composites, perf indexes, CHECK) live in
// directus/migrations/2026-06-03-calendar-binding-constraints.sql and are
// applied separately by add-calendar-constraints.mjs.
//
// The daily_calendar_sync cron_monitor seed row is inserted by
// add-cron-monitor.mjs (separate step, run after this).
//
// Usage:
//   $env:DIRECTUS_TOKEN = "<admin static token>"
//   $env:DATABASE_URL   = "<pg connection string>"   # for the migration guard
//   node directus/scripts/setup-calendar-collections.mjs

import {
  banner,
  collectionExists,
  directusRequest,
} from './lib/directus-request.mjs';
import { buildCollectionDefinitions } from './lib/calendar-schema.mjs';
import { assertCalendarEventsEmpty } from './lib/calendar-migration-guard.mjs';
import { queryPg } from './lib/sql-migration.mjs';

banner('setup-calendar-collections');

// ─────────────────────────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────────────────────────

async function fieldExists(collection, field) {
  try {
    await directusRequest(`/fields/${collection}/${field}`);
    return true;
  } catch (e) {
    const msg = String(e.message);
    if (msg.includes('404') || msg.includes('FORBIDDEN')) return false;
    throw e;
  }
}

async function relationExists(collection, field) {
  try {
    await directusRequest(`/relations/${collection}/${field}`);
    return true;
  } catch (e) {
    const msg = String(e.message);
    if (msg.includes('404') || msg.includes('FORBIDDEN')) return false;
    throw e;
  }
}

async function dropFieldIfExists(collection, field) {
  if (!(await fieldExists(collection, field))) {
    console.log(`  ⏩ ${collection}.${field} already gone`);
    return;
  }
  await directusRequest(`/fields/${collection}/${field}`, 'DELETE');
  console.log(`  🗑  dropped ${collection}.${field}`);
}

async function addFieldIfMissing(collection, fieldDef) {
  if (await fieldExists(collection, fieldDef.field)) {
    console.log(`  ⏩ ${collection}.${fieldDef.field} already exists`);
    return;
  }
  await directusRequest(`/fields/${collection}`, 'POST', fieldDef);
  console.log(`  + added ${collection}.${fieldDef.field}`);
}

async function addRelationIfMissing(spec) {
  if (await relationExists(spec.collection, spec.field)) {
    console.log(`  ⏩ relation ${spec.collection}.${spec.field} already exists`);
    return;
  }
  await directusRequest('/relations', 'POST', spec);
  console.log(`  ↔  relation ${spec.collection}.${spec.field} -> ${spec.related_collection}`);
}

// ─────────────────────────────────────────────────────────────────
// Step A — migrate calendar_events placeholder
// ─────────────────────────────────────────────────────────────────

console.log('\n  ── A. Migrating calendar_events placeholder ──');

const V1_PLACEHOLDER_FIELDS = [
  'google_event_id',
  'calendar_source',
  'relevance',
  'category_hint',
  'date',
  'start_time',
  'end_time',
  // attendees_count: existed in v1 with is_nullable=true and no default.
  // v1.6 shape: is_nullable=false, default=0. Dropping forces re-add with
  // the new schema; safe because the collection is empty per the guard.
  'attendees_count',
];

// Guard: refuse to drop columns if rows exist.
console.log('  Running migration guard (assert calendar_events empty)...');
await assertCalendarEventsEmpty(queryPg);
console.log('  ✅ calendar_events is empty');

// Drop v1 placeholder columns. Idempotent: skipped if already gone.
for (const field of V1_PLACEHOLDER_FIELDS) {
  await dropFieldIfExists('calendar_events', field);
}

// ─────────────────────────────────────────────────────────────────
// Step B — create the 4 collections (or add missing fields to existing)
// ─────────────────────────────────────────────────────────────────

console.log('\n  ── B. Creating / extending collections ──');

const definitions = buildCollectionDefinitions();

for (const def of definitions) {
  const exists = await collectionExists(def.collection);
  if (!exists) {
    // ONE POST with all fields (per the schema-management one-POST rule)
    await directusRequest('/collections', 'POST', def);
    console.log(`  + created ${def.collection} (${def.fields.length} fields)`);
  } else {
    // Existing collection (calendar_events is the only one in v1).
    // Idempotently ensure every field defined in the new shape exists.
    console.log(`  ⏩ ${def.collection} already exists; ensuring fields`);
    for (const fieldDef of def.fields) {
      await addFieldIfMissing(def.collection, fieldDef);
    }
  }
}

// ─────────────────────────────────────────────────────────────────
// Step C — register Directus relations (FK in admin UI)
// ─────────────────────────────────────────────────────────────────

console.log('\n  ── C. Registering Directus relations ──');

const RELATION_SPECS = [
  {
    collection: 'calendar_events',
    field: 'connection_id',
    related_collection: 'calendar_connections',
    schema: { on_delete: 'CASCADE' },
    meta: { many_collection: 'calendar_events', many_field: 'connection_id', one_collection: 'calendar_connections' },
  },
  {
    collection: 'calendar_events',
    field: 'linked_tag_id',
    related_collection: 'tags',
    schema: { on_delete: 'SET NULL' },
    meta: { many_collection: 'calendar_events', many_field: 'linked_tag_id', one_collection: 'tags' },
  },
  {
    collection: 'calendar_events',
    field: 'linked_episode_id',
    related_collection: 'episodes',
    schema: { on_delete: 'SET NULL' },
    meta: { many_collection: 'calendar_events', many_field: 'linked_episode_id', one_collection: 'episodes' },
  },
  {
    collection: 'calendar_connections',
    field: 'user_id',
    related_collection: 'directus_users',
    schema: { on_delete: 'CASCADE' },
    meta: { many_collection: 'calendar_connections', many_field: 'user_id', one_collection: 'directus_users' },
  },
  {
    collection: 'calendar_series_exclusions',
    field: 'connection_id',
    related_collection: 'calendar_connections',
    schema: { on_delete: 'CASCADE' },
    meta: { many_collection: 'calendar_series_exclusions', many_field: 'connection_id', one_collection: 'calendar_connections' },
  },
];

for (const spec of RELATION_SPECS) {
  await addRelationIfMissing(spec);
}

console.log('\n  ✅ Done.');
console.log('     Next: node directus/scripts/add-calendar-constraints.mjs');
console.log('           node directus/scripts/add-cron-monitor.mjs');
