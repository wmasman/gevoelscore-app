// Read-only sanity check: pulls today's day_entry from Directus, including
// its M2M tag links, and prints what's actually persisted. Use after a
// frontend save to confirm the round-trip landed.
//
// Run with:
//   $env:DIRECTUS_TOKEN = "<admin-static-token>"
//   node scripts/verify-todays-entry.mjs
//
// Or pass a specific date:
//   node scripts/verify-todays-entry.mjs 2026-05-28

import { directusRequest, banner, URL as DIRECTUS_URL } from '../directus/scripts/lib/directus-request.mjs';

function todayInAmsterdam() {
  return new Intl.DateTimeFormat('sv-SE', {
    timeZone: 'Europe/Amsterdam',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date());
}

const date = process.argv[2] || todayInAmsterdam();

banner(`verify-todays-entry — reading day_entry for ${date}`);
console.log(`Backend: ${DIRECTUS_URL}\n`);

try {
  // 1) The day_entry row + its expanded tag IDs.
  const entryRes = await directusRequest(
    `/items/day_entries?filter[date][_eq]=${date}&fields=*,tags.tags_id&limit=1`,
  );
  const rows = entryRes.data ?? [];

  if (rows.length === 0) {
    console.log(`No day_entry exists for ${date} yet.`);
    process.exit(0);
  }

  const row = rows[0];
  console.log('day_entries row:');
  console.log(`  id          : ${row.id}`);
  console.log(`  date        : ${row.date}`);
  console.log(`  score       : ${row.score}`);
  console.log(`  note        : ${row.note === null ? '(null)' : JSON.stringify(row.note)}`);
  console.log(`  created_at  : ${row.created_at}`);
  console.log(`  updated_at  : ${row.updated_at}`);

  const tagJunctions = row.tags ?? [];
  console.log(`  tag_count   : ${tagJunctions.length}`);

  if (tagJunctions.length > 0) {
    // 2) Resolve tag labels for readability.
    const tagIds = tagJunctions.map((t) => t.tags_id);
    const tagsRes = await directusRequest(
      `/items/tags?filter[id][_in]=${tagIds.join(',')}&fields=id,label,category&limit=-1`,
    );
    const labelMap = new Map((tagsRes.data ?? []).map((t) => [t.id, t]));
    console.log('\n  selected tags:');
    for (const j of tagJunctions) {
      const t = labelMap.get(j.tags_id);
      if (t) console.log(`    - ${t.category.padEnd(12)} ${t.label}`);
      else console.log(`    - <unknown tag-id ${j.tags_id}>`);
    }
  }

  // 3) Was the row edited? (updated_at meaningfully later than created_at)
  const created = Date.parse(row.created_at);
  const updated = Date.parse(row.updated_at);
  const editGapMs = updated - created;
  console.log(`\n  edit gap    : ${editGapMs}ms (${editGapMs > 5000 ? 'edited' : 'fresh'})`);

  console.log('\nRound-trip confirmed: the frontend save persisted to Directus.\n');
} catch (err) {
  console.error('\nFailed to read from Directus:');
  console.error(err.message ?? err);
  process.exit(1);
}
