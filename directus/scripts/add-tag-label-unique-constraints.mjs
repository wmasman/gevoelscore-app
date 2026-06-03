// Applies the (LOWER(label), category) partial UNIQUE indexes on `tags`
// and `episodes` (step-0 AC0.7) via direct PostgreSQL.
//
// Pre-flight: refuses to run if any (lowered-label, category) groups
// with > 1 non-archived rows exist. Two same-label tags encode user
// intent ambiguity — the user must merge them via the v1.5c UI (or
// manually rename) before the constraint can be applied.
//
// Idempotent — IF NOT EXISTS. Safe to re-run.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."
//   $env:DATABASE_URL   = "..."
//   node directus/scripts/add-tag-label-unique-constraints.mjs

import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { banner, directusRequest } from './lib/directus-request.mjs';
import { findDuplicateTagLabels } from './lib/audit-tag-labels.mjs';
import { runSqlFile } from './lib/sql-migration.mjs';

banner('add-tag-label-unique-constraints');

console.log('\n  ── Pre-flight: duplicate label audit ──');
let totalDups = 0;
for (const collection of ['tags', 'episodes']) {
  const result = await findDuplicateTagLabels(directusRequest, collection);
  console.log(`  ${collection.padEnd(10)} dup groups: ${result.dupGroups}`);
  totalDups += result.dupGroups;
}

if (totalDups > 0) {
  console.error('\n  ❌ Pre-flight failed: duplicate label/category groups exist.');
  console.error('     Resolve via the UI (rename one to differ OR merge via tag-management)');
  console.error('     and re-run this script.');
  process.exit(1);
}

console.log('  ✅ No duplicates. Applying partial UNIQUE indexes...\n');

const here = fileURLToPath(import.meta.url);
const sqlPath = resolve(here, '../../migrations/2026-06-03-tag-label-uniqueness.sql');

await runSqlFile(sqlPath);

console.log('  ✅ tags_label_category_active_unique + episodes_label_category_active_unique applied.');
console.log('     (idempotent — re-runs are safe)\n');
