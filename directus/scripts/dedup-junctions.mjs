// CLI wrapper for dedupJunctions. Auto-removes duplicate (day_entries_id,
// tags_id) rows from day_entries_tags + (project_entries_id, tags_id)
// rows from project_entries_tags. Keeps the lowest-id row per group.
//
// Junction duplicates are commutative — same (day, tag) means the same
// fact, so dedup is loss-free.
//
// Default: dry-run (prints the plan, makes NO writes). Pass --commit to
// actually delete. After committing, calls recompute-tag-usage for any
// tag that lost a junction.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."
//   node directus/scripts/dedup-junctions.mjs              # dry-run
//   node directus/scripts/dedup-junctions.mjs --commit     # apply

import { banner, directusRequest } from './lib/directus-request.mjs';
import { dedupJunctions } from './lib/audit-junctions.mjs';

const COMMIT = process.argv.includes('--commit');

banner(`dedup-junctions (${COMMIT ? 'COMMIT' : 'DRY-RUN'})`);

// recompute-tag-usage is its own script. After dedup deletes rows for
// affected tags, call it to bring usage_count back into truth. We invoke
// the existing logic by re-reading + re-PATCHing only the affected tags.
async function recomputeTagUsage(tagIds) {
  if (tagIds.length === 0) return;
  console.log(`\n  Recomputing usage_count for ${tagIds.length} affected tag(s)...`);
  for (const tagId of tagIds) {
    const junctionsResp = await directusRequest(
      `/items/day_entries_tags?limit=-1&filter[tags_id][_eq]=${tagId}&fields=id&aggregate[count]=*`,
    );
    const newCount = Number(junctionsResp?.data?.[0]?.count ?? 0);
    await directusRequest(`/items/tags/${tagId}`, 'PATCH', { usage_count: newCount });
    console.log(`    ${tagId} → usage_count = ${newCount}`);
  }
}

const collections = ['day_entries_tags', 'project_entries_tags'];
let totalDeleted = 0;
for (const collection of collections) {
  console.log(`\n  Auditing ${collection}...`);
  const result = await dedupJunctions({
    directusRequest,
    recomputeTagUsage,
    collection,
    commit: COMMIT,
  });
  console.log(`    kept:    ${result.kept.length}`);
  console.log(`    deleted: ${result.deleted.length}${COMMIT ? '' : ' (planned)'}`);
  if (result.deleted.length > 0 && !COMMIT) {
    console.log(`    plan:    ${JSON.stringify({ kept: result.kept, delete: result.deleted })}`);
  }
  totalDeleted += result.deleted.length;
}

console.log('\n' + '─'.repeat(64));
if (COMMIT) {
  console.log(`  ✅ Removed ${totalDeleted} duplicate junction row(s).`);
} else if (totalDeleted === 0) {
  console.log('  ✅ No duplicates found. Nothing to do.');
} else {
  console.log(`  🔍 DRY-RUN: ${totalDeleted} row(s) would be deleted. Re-run with --commit.`);
}
console.log('─'.repeat(64) + '\n');
