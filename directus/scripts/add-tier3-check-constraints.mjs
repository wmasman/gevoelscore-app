// Applies the 7 tier-3 CHECK constraints (step-0b AC0b.4) via direct
// PostgreSQL. Pre-flight: refuses to run if any current row would
// violate any of the constraints.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."        # for the pre-flight audit
//   $env:DATABASE_URL   = "..."        # for the SQL migration
//   node directus/scripts/add-tier3-check-constraints.mjs

import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { banner, directusRequest } from './lib/directus-request.mjs';
import { findCheckViolations } from './lib/audit-check-violations.mjs';
import { runSqlFile } from './lib/sql-migration.mjs';

banner('add-tier3-check-constraints');

console.log('\n  ── Pre-flight: row-level audit ──');
const results = await findCheckViolations(directusRequest);
let total = 0;
for (const r of results) {
  console.log(`  ${r.name.padEnd(45)} count: ${r.count}`);
  total += r.count;
}

if (total > 0) {
  console.error('\n  ❌ Pre-flight failed: violating rows exist.');
  console.error('     Fix the rows surfaced above (samples in JSON), then re-run.');
  process.exit(1);
}

console.log('  ✅ No violations. Applying CHECK constraints...\n');

const here = fileURLToPath(import.meta.url);
const sqlPath = resolve(here, '../../migrations/2026-06-03-tier3-check-constraints.sql');

await runSqlFile(sqlPath);

console.log('  ✅ All 7 CHECK constraints applied.');
console.log('     (idempotent — re-runs are safe)\n');
