// Upgrades day_entries.tag_ids from a JSON-array field to a proper Directus
// M2M relation via a junction collection (day_entries_tags) with cascading
// deletes on both FKs.
//
// Phases (each phase is idempotent — safe to re-run individually):
//   A. Cache existing tag_ids → private/m2m-migration-cache.json
//   B. Create `day_entries_tags` junction collection (UUID PK + 2 FK fields + sort)
//   C. Create the two Directus relations (defines the M2M topology + cascade)
//   D. Backfill junction rows from cache
//   E. Verify counts
//   F. Drop the old day_entries.tag_ids JSON field
//
// Default: dry-run. Pass --commit to actually perform destructive operations
// (creates the junction, modifies the day_entries schema, deletes the old field).

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { existsSync } from 'node:fs';
import { banner, directusRequest, collectionExists } from './lib/directus-request.mjs';

const COMMIT = process.argv.includes('--commit');
const CACHE_PATH = resolve(process.cwd(), 'private/m2m-migration-cache.json');

banner(`upgrade-m2m-tags (${COMMIT ? 'COMMIT' : 'DRY-RUN'})`);

// ---------------------------------------------------------------------------
// Phase A: cache existing tag_ids
// ---------------------------------------------------------------------------

console.log('═ Phase A: cache existing tag_ids');

let cache;
if (existsSync(CACHE_PATH)) {
  console.log(`  Loading existing cache from ${CACHE_PATH}`);
  cache = JSON.parse(await readFile(CACHE_PATH, 'utf8'));
} else {
  console.log('  Pulling all day_entries with tag_ids from Directus...');
  const entriesResp = await directusRequest(
    '/items/day_entries?limit=-1&fields=id,date,tag_ids&filter[tag_ids][_nnull]=true',
  );
  cache = (entriesResp.data ?? [])
    .filter((e) => Array.isArray(e.tag_ids) && e.tag_ids.length > 0)
    .map((e) => ({ day_entry_id: e.id, date: e.date, tag_ids: e.tag_ids }));

  await mkdir(dirname(CACHE_PATH), { recursive: true });
  await writeFile(CACHE_PATH, JSON.stringify(cache, null, 2));
  console.log(`  Cached ${cache.length} day_entries to ${CACHE_PATH}`);
}

const totalJunctionRows = cache.reduce((s, e) => s + e.tag_ids.length, 0);
console.log(`  Junction rows to create: ${totalJunctionRows}`);

// ---------------------------------------------------------------------------
// Phase B: create junction collection
// ---------------------------------------------------------------------------

console.log('\n═ Phase B: junction collection day_entries_tags');

const junctionExists = await collectionExists('day_entries_tags');
if (junctionExists) {
  console.log('  ⏩ day_entries_tags already exists, skipping creation');
} else if (!COMMIT) {
  console.log('  [DRY-RUN] would create day_entries_tags with id + day_entries_id + tags_id + sort');
} else {
  console.log('  ➕ Creating day_entries_tags...');
  await directusRequest('/collections', 'POST', {
    collection: 'day_entries_tags',
    schema: { name: 'day_entries_tags' },
    meta: {
      icon: 'link',
      note: 'Junction for day_entries ↔ tags M2M. Cascading deletes from both sides.',
      hidden: true,
    },
    fields: [
      {
        field: 'id',
        type: 'uuid',
        schema: { is_primary_key: true, is_nullable: false },
        meta: { hidden: true, readonly: true, interface: 'input', special: ['uuid'] },
      },
      {
        field: 'day_entries_id',
        type: 'uuid',
        schema: { is_nullable: false },
        meta: { hidden: true, interface: 'select-dropdown-m2o' },
      },
      {
        field: 'tags_id',
        type: 'uuid',
        schema: { is_nullable: false },
        meta: { hidden: true, interface: 'select-dropdown-m2o' },
      },
      {
        field: 'sort',
        type: 'integer',
        schema: { is_nullable: true },
        meta: { hidden: true, interface: 'input' },
      },
    ],
  });
  console.log('  ✅ Created');
}

// ---------------------------------------------------------------------------
// Phase C: create the relations (defines M2M topology + cascade)
// ---------------------------------------------------------------------------

console.log('\n═ Phase C: relations');

async function relationExists(collection, field) {
  try {
    await directusRequest(`/relations/${collection}/${field}`);
    return true;
  } catch (e) {
    return false;
  }
}

const rel1Exists = await relationExists('day_entries_tags', 'day_entries_id');
const rel2Exists = await relationExists('day_entries_tags', 'tags_id');

if (rel1Exists && rel2Exists) {
  console.log('  ⏩ Both relations already exist, skipping');
} else if (!COMMIT) {
  console.log('  [DRY-RUN] would create 2 relations with on_delete=CASCADE');
} else {
  if (!rel1Exists) {
    console.log('  ➕ Creating relation: day_entries_tags.day_entries_id → day_entries.id');
    await directusRequest('/relations', 'POST', {
      collection: 'day_entries_tags',
      field: 'day_entries_id',
      related_collection: 'day_entries',
      meta: {
        one_field: 'tags',
        junction_field: 'tags_id',
        sort_field: 'sort',
      },
      schema: { on_delete: 'CASCADE', on_update: 'NO ACTION' },
    });
    console.log('  ✅');
  }
  if (!rel2Exists) {
    console.log('  ➕ Creating relation: day_entries_tags.tags_id → tags.id');
    await directusRequest('/relations', 'POST', {
      collection: 'day_entries_tags',
      field: 'tags_id',
      related_collection: 'tags',
      meta: {
        one_field: 'day_entries',
        junction_field: 'day_entries_id',
        sort_field: 'sort',
      },
      schema: { on_delete: 'CASCADE', on_update: 'NO ACTION' },
    });
    console.log('  ✅');
  }
}

// ---------------------------------------------------------------------------
// Phase D: backfill junction rows from cache
// ---------------------------------------------------------------------------

console.log('\n═ Phase D: backfill junction rows');

if (!COMMIT) {
  console.log(`  [DRY-RUN] would insert ${totalJunctionRows} junction rows`);
} else {
  // Check how many junction rows exist; if it matches, skip
  const existingResp = await directusRequest('/items/day_entries_tags?aggregate[count]=*');
  const existingCount = parseInt(existingResp.data?.[0]?.count ?? '0', 10);

  if (existingCount === totalJunctionRows) {
    console.log(`  ⏩ Junction already has ${existingCount} rows (matches expected). Skipping backfill.`);
  } else if (existingCount > 0) {
    console.log(`  ⚠️  Junction has ${existingCount} rows but expected ${totalJunctionRows}. Clearing and re-inserting.`);
    // For simplicity: don't auto-clear. Bail and let user investigate.
    console.log('  ❌ Refusing to backfill on top of a partially-populated junction. Inspect manually.');
    process.exit(1);
  } else {
    console.log(`  ➕ Inserting ${totalJunctionRows} junction rows (in batches)...`);
    // Build all rows first
    const rows = [];
    for (const e of cache) {
      for (let i = 0; i < e.tag_ids.length; i++) {
        rows.push({
          day_entries_id: e.day_entry_id,
          tags_id: e.tag_ids[i],
          sort: i + 1,
        });
      }
    }
    // Insert in batches of 100
    const BATCH = 100;
    let inserted = 0;
    for (let i = 0; i < rows.length; i += BATCH) {
      const batch = rows.slice(i, i + BATCH);
      await directusRequest('/items/day_entries_tags', 'POST', batch);
      inserted += batch.length;
      if (inserted % 500 === 0 || inserted === rows.length) {
        console.log(`    …${inserted}/${rows.length}`);
      }
    }
    console.log(`  ✅ Inserted ${inserted} junction rows`);
  }
}

// ---------------------------------------------------------------------------
// Phase E: verify
// ---------------------------------------------------------------------------

console.log('\n═ Phase E: verify');

if (COMMIT) {
  const count = parseInt(
    (await directusRequest('/items/day_entries_tags?aggregate[count]=*')).data?.[0]?.count ?? '0',
    10,
  );
  console.log(`  Junction row count: ${count} (expected ${totalJunctionRows})`);
  if (count !== totalJunctionRows) {
    console.log('  ❌ Mismatch! Skipping Phase F.');
    process.exit(1);
  }
  console.log('  ✅ Counts match.');
}

// ---------------------------------------------------------------------------
// Phase F: drop the old JSON tag_ids field
// ---------------------------------------------------------------------------

console.log('\n═ Phase F: drop old day_entries.tag_ids JSON field');

if (!COMMIT) {
  console.log('  [DRY-RUN] would DELETE /fields/day_entries/tag_ids');
} else {
  try {
    await directusRequest('/fields/day_entries/tag_ids');
    console.log('  ➖ Dropping the old JSON field...');
    await directusRequest('/fields/day_entries/tag_ids', 'DELETE');
    console.log('  ✅ Dropped');
  } catch (e) {
    if (e.message.includes('404')) {
      console.log('  ⏩ Field already gone');
    } else {
      console.error(`  ❌ ${e.message.split('\n')[0]}`);
      process.exit(1);
    }
  }
}

console.log('\n' + '═'.repeat(64));
if (!COMMIT) {
  console.log('🔍 DRY-RUN complete. Re-run with --commit to perform the migration.');
} else {
  console.log('✅ M2M upgrade complete.');
  console.log('   Next: update import-real-history.mjs to use the new payload shape.');
}
console.log('═'.repeat(64) + '\n');
