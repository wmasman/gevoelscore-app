// Adds provenance columns to the `day_entries_tags` junction so we can
// distinguish "user explicitly chose this tag" from "regex matched the note"
// and from "imported from historical CSV". Without this, every junction row
// looks the same and re-running the pattern matcher would clobber user choices.
//
// New columns on day_entries_tags:
//   source         enum-like string: 'user' | 'note_pattern' | 'csv_import' | 'inferred'
//   confidence     float 0..1, nullable (null = user-chosen, full confidence)
//   confirmed_at   timestamp, nullable (set when the user reviews/accepts an inferred tag)
//
// Backfill: every existing junction row was created by import-real-history.mjs
// matching regex patterns from lib/tag-patterns.mjs against the historical CSV
// notes. So the correct backfill value is source='note_pattern', confidence=1.0.
//
// Idempotent: re-running checks each field and skips if already present.
// Re-running the backfill is also safe — it only touches rows where source IS NULL.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."
//   node directus/scripts/add-tag-provenance.mjs

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('add-tag-provenance');

async function fieldExists(collection, field) {
  try {
    await directusRequest(`/fields/${collection}/${field}`);
    return true;
  } catch (e) {
    return false;
  }
}

const fields = [
  {
    field: 'source',
    type: 'string',
    schema: { is_nullable: true, max_length: 20 },
    meta: {
      interface: 'select-dropdown',
      options: {
        choices: [
          { text: 'User chose', value: 'user' },
          { text: 'Note pattern match', value: 'note_pattern' },
          { text: 'CSV import', value: 'csv_import' },
          { text: 'Inferred', value: 'inferred' },
        ],
      },
      note: 'Where this junction row came from. null = legacy (treat as note_pattern).',
    },
  },
  {
    field: 'confidence',
    type: 'float',
    schema: { is_nullable: true },
    meta: {
      interface: 'input',
      note: '0..1. null when source=user (full confidence by definition).',
    },
  },
  {
    field: 'confirmed_at',
    type: 'timestamp',
    schema: { is_nullable: true },
    meta: {
      interface: 'datetime',
      note: 'Set when the user reviews and accepts an auto-inferred tag.',
    },
  },
];

console.log('  Schema:');
for (const spec of fields) {
  if (await fieldExists('day_entries_tags', spec.field)) {
    console.log(`    ⏩ day_entries_tags.${spec.field} already exists`);
    continue;
  }
  console.log(`    ➕ Adding day_entries_tags.${spec.field} (${spec.type})`);
  await directusRequest('/fields/day_entries_tags', 'POST', spec);
}

console.log('\n  Backfill:');
const rowsResp = await directusRequest(
  '/items/day_entries_tags?limit=-1&fields=id,source&filter[source][_null]=true',
);
const toBackfill = rowsResp.data ?? [];
console.log(`    Rows with source IS NULL: ${toBackfill.length}`);

if (toBackfill.length === 0) {
  console.log('    ⏩ nothing to backfill');
} else {
  // PATCH in batches to avoid huge payloads. Directus /items/{collection} with
  // body { keys, data } updates multiple rows atomically.
  const BATCH = 200;
  let done = 0;
  for (let i = 0; i < toBackfill.length; i += BATCH) {
    const slice = toBackfill.slice(i, i + BATCH);
    await directusRequest('/items/day_entries_tags', 'PATCH', {
      keys: slice.map((r) => r.id),
      data: { source: 'note_pattern', confidence: 1.0 },
    });
    done += slice.length;
    process.stdout.write(`\r    ${done}/${toBackfill.length} rows`);
  }
  console.log('\n    ✅ backfill complete');
}

// Sanity-check: count by source
const counts = {};
for (const source of ['user', 'note_pattern', 'csv_import', 'inferred']) {
  const r = await directusRequest(
    `/items/day_entries_tags?aggregate[count]=id&filter[source][_eq]=${source}`,
  );
  counts[source] = Number(r.data?.[0]?.count?.id ?? r.data?.[0]?.count ?? 0);
}
const nullR = await directusRequest(
  '/items/day_entries_tags?aggregate[count]=id&filter[source][_null]=true',
);
counts['(null)'] = Number(nullR.data?.[0]?.count?.id ?? nullR.data?.[0]?.count ?? 0);

console.log('\n  Junction rows by source:');
for (const [k, v] of Object.entries(counts)) {
  console.log(`    ${k.padEnd(15)} ${String(v).padStart(5)}`);
}

console.log('\n✅ Done.\n');
