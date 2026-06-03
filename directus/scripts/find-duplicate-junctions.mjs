// CLI wrapper for findDuplicateJunctions. Read-only audit against
// day_entries_tags + project_entries_tags. Prints JSON-on-stdout +
// human-readable summary on stderr. Exits 0 regardless of duplicate
// count; this is an audit, not a gate.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."
//   node directus/scripts/find-duplicate-junctions.mjs

import { banner, directusRequest } from './lib/directus-request.mjs';
import { findDuplicateJunctions } from './lib/audit-junctions.mjs';

banner('find-duplicate-junctions');

const collections = ['day_entries_tags', 'project_entries_tags'];
const results = [];
for (const collection of collections) {
  const result = await findDuplicateJunctions(directusRequest, collection);
  results.push(result);
  console.log(
    `  ${collection.padEnd(22)} dup groups: ${String(result.dupGroups).padStart(3)} | extra rows: ${String(result.extraRows).padStart(4)}`,
  );
  for (const sample of result.samples) {
    console.log(`    └─ ${JSON.stringify(sample)}`);
  }
}

const totalDupGroups = results.reduce((s, r) => s + r.dupGroups, 0);
const totalExtraRows = results.reduce((s, r) => s + r.extraRows, 0);
console.log('\n' + '─'.repeat(64));
console.log(`  TOTAL  dup groups: ${totalDupGroups} | extra rows: ${totalExtraRows}`);
console.log('─'.repeat(64));

console.log('\n' + JSON.stringify({ results, totalDupGroups, totalExtraRows }, null, 2));
