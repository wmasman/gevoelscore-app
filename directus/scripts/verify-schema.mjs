// Verifies that the one-POST rule produced the right PostgreSQL types.
// The TVO project lost 80% of a migration to a silent VARCHAR-where-INTEGER
// bug — see docs/architecture/directus-schema-management.md "Lesson 3".

import { banner, directusRequest } from './lib/directus-request.mjs';

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

  ['calendar_events', 'google_event_id', 'string', 'character varying', { is_unique: true, is_nullable: false }],
  ['calendar_events', 'date', 'date', 'date', { is_nullable: false }],

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
console.log(`  Passed: ${passes.length}/${expectations.length}`);
console.log(`  Failed: ${failures.length}/${expectations.length}`);
console.log('─'.repeat(64) + '\n');

if (failures.length > 0) {
  console.log('Failures detail:');
  for (const f of failures) {
    console.log(`  ${f.collection}.${f.field}:`);
    f.issues.forEach((i) => console.log(`    - ${i}`));
  }
  process.exit(1);
}

console.log('✅ All schema checks passed.\n');
