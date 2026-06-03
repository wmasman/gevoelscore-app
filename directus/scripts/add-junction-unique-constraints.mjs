// Applies the junction-pair UNIQUE constraints (step-0 AC0.6) via direct
// PostgreSQL. Pre-flight: refuses to run if any duplicate junction rows
// exist (calls findDuplicateJunctions internally). Idempotent — the SQL
// uses IF NOT EXISTS, so safe to re-run.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."        # for the pre-flight audit
//   $env:DATABASE_URL   = "..."        # for the SQL migration
//   node directus/scripts/add-junction-unique-constraints.mjs

import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { banner, directusRequest } from './lib/directus-request.mjs';
import { findDuplicateJunctions } from './lib/audit-junctions.mjs';
import { runSqlFile } from './lib/sql-migration.mjs';

banner('add-junction-unique-constraints');

console.log('\n  ── Pre-flight: duplicate junction audit ──');
let totalDups = 0;
for (const collection of ['day_entries_tags', 'project_entries_tags']) {
  const result = await findDuplicateJunctions(directusRequest, collection);
  console.log(
    `  ${collection.padEnd(22)} dup groups: ${result.dupGroups}`,
  );
  totalDups += result.dupGroups;
}

if (totalDups > 0) {
  console.error('\n  ❌ Pre-flight failed: duplicate junction rows exist.');
  console.error('     Run `dedup-junctions.mjs --commit` first, then re-run this script.');
  process.exit(1);
}

console.log('  ✅ No duplicates. Applying UNIQUE indexes...\n');

const here = fileURLToPath(import.meta.url);
const sqlPath = resolve(here, '../../migrations/2026-06-03-junction-unique-pairs.sql');

await runSqlFile(sqlPath);

console.log('  ✅ day_entries_tags_unique_pair + project_entries_tags_unique_pair applied.');
console.log('     (idempotent — re-runs are safe)\n');
