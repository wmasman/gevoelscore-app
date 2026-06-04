// Inserts series-exclusion rows into calendar_series_exclusions for a
// hand-curated list. Idempotent: existing exclusions are skipped (UNIQUE
// on connection_id, recurrence_id catches duplicates).
//
// For each excluded recurrence, ALSO updates every existing event row
// in that series to included_as_context=false + user_decision='user_excluded'
// so subsequent reads (Context tab, sync re-pulls) honour the rule.
//
// Workflow:
//   1. Run list-recurring-series.mjs to see what's there.
//   2. Edit the SERIES_TO_EXCLUDE array below with the rows you want.
//   3. Run this script.
//   4. (Optional) Edit again for additional anticipated patterns.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "<admin token>"
//   node directus/scripts/add-series-exclusions.mjs

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('add-series-exclusions');

// ─────────────────────────────────────────────────────────────────
// EDIT THIS LIST.
//
// Each entry: { recurrence_id, connection_id, reason? }
// reason is for human bookkeeping only; not stored.
// ─────────────────────────────────────────────────────────────────

// Pre-backfill curation 2026-06-04: all 10 recurring series surfaced by
// list-recurring-series.mjs in the initial 37-day pull. User judgment
// (Willem): all of them are calendar noise that he chooses to ignore.
// There's no clean algorithmic rule — noise/signal is per-user, which is
// exactly why the per-series exclusion UI (Phase 1.E) is the design.
const SERIES_TO_EXCLUDE = [
  { recurrence_id: 'gj9q4igmv6rfi36fqrvn5p0dss', connection_id: 'fa049661-9119-4d00-8871-9b1c5e262adc', reason: 'JM (6×, weekly)' },
  { recurrence_id: '4j28a9ofq83cqmp66h8b52lh53', connection_id: 'fa049661-9119-4d00-8871-9b1c5e262adc', reason: 'W (6×, weekly)' },
  { recurrence_id: 'lmmcbt3l6f0mt0ktvngsq3niug', connection_id: 'fa049661-9119-4d00-8871-9b1c5e262adc', reason: 'Datenight (willem)' },
  { recurrence_id: 'i4jljihbjfa5ro8htn7gbp0nag', connection_id: 'fa049661-9119-4d00-8871-9b1c5e262adc', reason: 'Datenight (Jantine)' },
  { recurrence_id: '0t0foa7ppa1aelvui25casd7jg_R20231201T170000', connection_id: 'fa049661-9119-4d00-8871-9b1c5e262adc', reason: 'Bestuurseten' },
  { recurrence_id: '8t6uscvq1d9nujtfjodf2flhnk_R20231201T160000', connection_id: 'fa049661-9119-4d00-8871-9b1c5e262adc', reason: 'Bestuurseten vrijdag of zaterdag' },
  { recurrence_id: 'fucfkunfdlsnckni3tgfq3sljc', connection_id: 'fa049661-9119-4d00-8871-9b1c5e262adc', reason: 'reunistenborrel op de buis' },
  { recurrence_id: 't2r4tsaa1gr86aik55bge5j658', connection_id: 'fa049661-9119-4d00-8871-9b1c5e262adc', reason: 'Willem Hans' },
  { recurrence_id: 'tputjrbdlch8f9r1m1hllmeb4g', connection_id: 'fa049661-9119-4d00-8871-9b1c5e262adc', reason: 'Happy birthday! (Google auto-birthday)' },
  { recurrence_id: '_64skcgi46sq42b9n8op4cb9k70s3cba28ks3gba174ojgd258d332chi8o', connection_id: 'fa049661-9119-4d00-8871-9b1c5e262adc', reason: 'Willem Hans (duplicate / orphan)' },
];

if (SERIES_TO_EXCLUDE.length === 0) {
  console.log('\n  ⚠️  SERIES_TO_EXCLUDE is empty. Edit this file with the recurrences');
  console.log('     to exclude (use list-recurring-series.mjs output to find them).');
  console.log('     Re-run this script after editing.\n');
  process.exit(0);
}

console.log(`\n  Processing ${SERIES_TO_EXCLUDE.length} series exclusion(s)...\n`);

let inserted = 0;
let skipped = 0;
let totalEventsFlipped = 0;
const failures = [];

const nowIso = new Date().toISOString();

for (let i = 0; i < SERIES_TO_EXCLUDE.length; i++) {
  const { recurrence_id, connection_id, reason } = SERIES_TO_EXCLUDE[i];
  if (!recurrence_id || !connection_id) {
    console.error(`  ❌ entry ${i + 1}: missing recurrence_id or connection_id`);
    failures.push(`entry ${i + 1}: missing fields`);
    continue;
  }

  const label = reason ? `"${reason.slice(0, 60)}"` : '(no reason)';
  process.stdout.write(`  [${i + 1}/${SERIES_TO_EXCLUDE.length}] ${recurrence_id.slice(0, 30)}...  ${label}\n`);

  // 1. Check if exclusion already exists.
  const existingExcl = await directusRequest(
    `/items/calendar_series_exclusions?filter[_and][0][connection_id][_eq]=${encodeURIComponent(connection_id)}&filter[_and][1][recurrence_id][_eq]=${encodeURIComponent(recurrence_id)}&limit=1`,
  );
  if ((existingExcl.data ?? []).length > 0) {
    console.log(`        ⏩ exclusion already present`);
    skipped++;
  } else {
    // 2. INSERT exclusion.
    try {
      await directusRequest('/items/calendar_series_exclusions', 'POST', {
        connection_id,
        recurrence_id,
        excluded_at: nowIso,
      });
      console.log(`        + inserted exclusion`);
      inserted++;
    } catch (e) {
      console.error(`        ❌ INSERT failed: ${e.message.slice(0, 200)}`);
      failures.push(`${recurrence_id}: insert failed`);
      continue;
    }
  }

  // 3. Find all existing event rows with this recurrence_id + flip them.
  try {
    const eventsRes = await directusRequest(
      `/items/calendar_events?filter[_and][0][connection_id][_eq]=${encodeURIComponent(connection_id)}&filter[_and][1][recurrence_id][_eq]=${encodeURIComponent(recurrence_id)}&fields=id,included_as_context,user_decision&limit=-1`,
    );
    const rows = eventsRes.data ?? [];
    const toFlip = rows.filter((r) => r.included_as_context !== false || r.user_decision !== 'user_excluded');
    if (toFlip.length === 0) {
      console.log(`        ⏩ ${rows.length} events already excluded`);
      continue;
    }
    // PATCH each — Directus REST doesn't have a clean bulk-PATCH-by-filter
    // surface; do them one at a time. The bulk-PATCH-by-id surface IS
    // available but the script lib doesn't wrap it; one-by-one is fine
    // for this volume.
    for (const r of toFlip) {
      await directusRequest(`/items/calendar_events/${r.id}`, 'PATCH', {
        included_as_context: false,
        user_decision: 'user_excluded',
      });
      totalEventsFlipped++;
    }
    console.log(`        + flipped ${toFlip.length} event(s) to excluded`);
  } catch (e) {
    console.error(`        ❌ event flip failed: ${e.message.slice(0, 200)}`);
    failures.push(`${recurrence_id}: event flip failed`);
  }
}

console.log('\n  ── Summary ──');
console.log(`    Series-exclusion rows inserted:    ${inserted}`);
console.log(`    Series-exclusion rows skipped:     ${skipped} (already present)`);
console.log(`    Existing events flipped:           ${totalEventsFlipped}`);
console.log(`    Failures:                          ${failures.length}`);
if (failures.length > 0) {
  console.log('');
  for (const f of failures.slice(0, 10)) console.log(`      - ${f}`);
}
console.log('');
console.log('  Future syncs (incl. the historical backfill) will respect these');
console.log('  exclusions: new events fetched with recurrence_id in the list will');
console.log('  default to included_as_context=false + user_decision=user_excluded.');
console.log('');

process.exit(failures.length > 0 ? 1 : 0);
