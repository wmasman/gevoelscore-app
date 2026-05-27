// Seeds the v1 tag set in Directus from lib/tag-patterns.mjs.
// Idempotent: re-running is safe (existing labels are skipped via filter-check).
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."
//   node directus/scripts/seed-tags.mjs

import { banner, directusRequest } from './lib/directus-request.mjs';
import { flatTagList } from './lib/tag-patterns.mjs';

banner('seed-tags');

const tags = flatTagList();
console.log(`  Tag map: ${tags.length} tags across ${new Set(tags.map((t) => t.category)).size} categories\n`);

// Pull existing tags in one call so we don't make N round-trips
const existing = await directusRequest('/items/tags?limit=-1&fields=id,label,category');
const existingByLabel = new Map();
for (const t of existing.data ?? []) {
  existingByLabel.set(`${t.category}:${t.label}`, t);
}

console.log(`  Existing tags in Directus: ${existingByLabel.size}\n`);

let created = 0;
let skipped = 0;
let failed = 0;

for (const { label, category } of tags) {
  const key = `${category}:${label}`;
  if (existingByLabel.has(key)) {
    skipped++;
    continue;
  }
  try {
    await directusRequest('/items/tags', 'POST', {
      label,
      category,
      project_id: null,
      usage_count: 0,
      archived_at: null,
    });
    console.log(`  ➕ ${category.padEnd(13)} ${label}`);
    created++;
  } catch (e) {
    failed++;
    console.error(`  ❌ ${category.padEnd(13)} ${label} — ${e.message.split('\n')[0]}`);
  }
}

console.log('\n' + '─'.repeat(64));
console.log(`  Created: ${created}`);
console.log(`  Skipped (already existed): ${skipped}`);
console.log(`  Failed: ${failed}`);
console.log('─'.repeat(64));
if (failed > 0) process.exit(1);
console.log('\n✅ Tags seeded.\n');
