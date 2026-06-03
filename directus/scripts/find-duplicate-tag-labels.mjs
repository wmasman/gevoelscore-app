// CLI wrapper for findDuplicateTagLabels. Read-only audit against `tags`
// + `episodes`, scoped to non-archived rows. Surfaces (LOWER(label),
// category) groups with count > 1 — the duplicate-tag pressure that the
// tag-merge feature exists to resolve.
//
// Exits 0 regardless of duplicate count. Audit, not gate; the constraint-
// add scripts (AC0.8 / AC0.9) consult this to refuse running while dups
// exist.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."
//   node directus/scripts/find-duplicate-tag-labels.mjs

import { banner, directusRequest } from './lib/directus-request.mjs';
import { findDuplicateTagLabels } from './lib/audit-tag-labels.mjs';

banner('find-duplicate-tag-labels');

const collections = ['tags', 'episodes'];
const results = [];
for (const collection of collections) {
  const result = await findDuplicateTagLabels(directusRequest, collection);
  results.push(result);
  console.log(
    `  ${collection.padEnd(10)} dup groups: ${String(result.dupGroups).padStart(3)} | extra rows: ${String(result.extraRows).padStart(4)}`,
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

if (totalDupGroups > 0) {
  console.log(
    '\n  ⚠️  Resolve via the UI (rename one to differ OR merge via',
  );
  console.log(
    '      tag-management settings) before running',
  );
  console.log(
    '      add-tag-label-unique-constraints.mjs.',
  );
}

console.log('\n' + JSON.stringify({ results, totalDupGroups, totalExtraRows }, null, 2));
