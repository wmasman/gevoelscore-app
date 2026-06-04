// Applies the calendar-binding SQL constraints (UNIQUE composites,
// performance indexes, CHECK constraints) via direct PostgreSQL.
//
// Pre-flight: requires that setup-calendar-collections.mjs has been
// run (so the columns + tables exist). Idempotent — the SQL uses
// CREATE ... IF NOT EXISTS + DO blocks, so safe to re-run.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."  # banner-only; constraints go via DATABASE_URL
//   $env:DATABASE_URL   = "..."
//   node directus/scripts/add-calendar-constraints.mjs

import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { banner } from './lib/directus-request.mjs';
import { runSqlFile } from './lib/sql-migration.mjs';

banner('add-calendar-constraints');

const here = fileURLToPath(import.meta.url);
const sqlPath = resolve(
  here,
  '../../migrations/2026-06-03-calendar-binding-constraints.sql',
);

console.log(`\n  Applying SQL: ${sqlPath}\n`);
await runSqlFile(sqlPath);

console.log('  ✅ Constraints applied:');
console.log('     - 4 UNIQUE composite indexes');
console.log('     - 2 performance indexes');
console.log('     - 6 CHECK constraints');
console.log('     (idempotent — re-runs are safe)\n');
