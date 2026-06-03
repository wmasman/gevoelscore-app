// CLI wrapper for findCheckViolations (step-0b AC0b.2). Read-only.
// Exits 0 regardless of violation count — audit, not gate. The
// add-tier3-check-constraints script uses this internally as a hard
// pre-flight.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."
//   node directus/scripts/find-check-violations.mjs

import { banner, directusRequest } from './lib/directus-request.mjs';
import { findCheckViolations } from './lib/audit-check-violations.mjs';

banner('find-check-violations');

const results = await findCheckViolations(directusRequest);

for (const r of results) {
  console.log(`  ${r.name.padEnd(45)} count: ${String(r.count).padStart(4)}`);
  for (const s of r.samples) {
    console.log(`    └─ ${JSON.stringify(s)}`);
  }
}

const total = results.reduce((sum, r) => sum + r.count, 0);
console.log('\n' + '─'.repeat(64));
console.log(`  TOTAL violations across 7 constraints: ${total}`);
console.log('─'.repeat(64));

if (total > 0) {
  console.log(
    '\n  ⚠️  Resolve violations in the affected rows before running',
  );
  console.log('      add-tier3-check-constraints.mjs.');
}

console.log('\n' + JSON.stringify({ results, total }, null, 2));
