// One-shot rename: 'te veel gedaan' -> 'teveel gedaan' in the `tags`
// collection. The 2026-06-01 inline-tag-creation feature introduced a
// MAX_TAG_LABEL_WORDS = 2 rule in validateTagLabel. Exactly one seeded
// tag violated the new rule. This script reconciles production with the
// updated seed file in lib/tag-patterns.mjs.
//
// Tag ids do not change, so every existing day_entries_tags row remains
// attached. Only the human-readable label changes.
//
// Idempotent: re-running is safe. Finds rows with the OLD label only; if
// the rename already ran, the result is "0 rows updated".
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."
//   node directus/scripts/rename-tag-te-veel-gedaan.mjs

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('rename-tag-te-veel-gedaan');

const OLD_LABEL = 'te veel gedaan';
const NEW_LABEL = 'teveel gedaan';

const result = await directusRequest(
  `/items/tags?filter[label][_eq]=${encodeURIComponent(OLD_LABEL)}&fields=id,label,category`,
);
const rows = result.data ?? [];

if (rows.length === 0) {
  console.log(`  No tag with label "${OLD_LABEL}" found. Nothing to do.`);
  process.exit(0);
}

console.log(`  Found ${rows.length} row(s) with label "${OLD_LABEL}":`);
for (const row of rows) {
  console.log(`    id=${row.id} category=${row.category}`);
}

for (const row of rows) {
  await directusRequest(`/items/tags/${row.id}`, 'PATCH', { label: NEW_LABEL });
  console.log(`  Renamed id=${row.id} -> "${NEW_LABEL}"`);
}

console.log(`  Done. ${rows.length} row(s) updated.`);
