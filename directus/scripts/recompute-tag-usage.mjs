// Recomputes Tag.usage_count by counting junction rows per tag in the
// day_entries_tags M2M relation. Idempotent.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."
//   node directus/scripts/recompute-tag-usage.mjs

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('recompute-tag-usage');

const tagsResp = await directusRequest('/items/tags?limit=-1&fields=id,label,category,usage_count');
const tags = tagsResp.data ?? [];
console.log(`  Tags: ${tags.length}`);

const junctionResp = await directusRequest('/items/day_entries_tags?limit=-1&fields=tags_id');
const junctionRows = junctionResp.data ?? [];
console.log(`  Junction rows: ${junctionRows.length}\n`);

const counts = new Map();
for (const j of junctionRows) {
  const id = typeof j.tags_id === 'string' ? j.tags_id : j.tags_id?.id;
  if (!id) continue;
  counts.set(id, (counts.get(id) ?? 0) + 1);
}

let updated = 0;
let unchanged = 0;
let failed = 0;

console.log('  Updating drifted counts:');
for (const tag of tags) {
  const newCount = counts.get(tag.id) ?? 0;
  if (newCount === tag.usage_count) {
    unchanged++;
    continue;
  }
  try {
    await directusRequest(`/items/tags/${tag.id}`, 'PATCH', { usage_count: newCount });
    console.log(`    ${tag.category.padEnd(13)} ${tag.label.padEnd(28)} ${String(tag.usage_count).padStart(4)} → ${String(newCount).padStart(4)}`);
    updated++;
  } catch (e) {
    failed++;
    console.error(`    ❌ ${tag.label}: ${e.message.split('\n')[0]}`);
  }
}

console.log('\n' + '─'.repeat(64));
console.log(`  Updated:   ${updated}`);
console.log(`  Unchanged: ${unchanged}`);
console.log(`  Failed:    ${failed}`);
console.log('─'.repeat(64));

const sorted = tags
  .map((t) => ({ ...t, currentCount: counts.get(t.id) ?? 0 }))
  .sort((a, b) => b.currentCount - a.currentCount);

console.log('\n  Top 10 most-used tags:');
for (const t of sorted.slice(0, 10)) {
  console.log(`    ${String(t.currentCount).padStart(4)}  ${t.category.padEnd(13)} ${t.label}`);
}

if (failed > 0) process.exit(1);
console.log('\n✅ Done.\n');
