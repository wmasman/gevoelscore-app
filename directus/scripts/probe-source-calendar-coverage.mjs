// Read-only probe: how many calendar_events have source_calendar_id
// populated vs NULL, and which connection / which source calendars
// have which counts. Used to verify the Ververs-nu sync populated
// source_calendar_id as expected, and to see how big the remaining
// historical-backfill gap is.

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('probe-source-calendar-coverage');

const rowsRes = await directusRequest(
  '/items/calendar_events?limit=-1&fields=connection_id,source_calendar_id',
);
const rows = rowsRes?.data ?? rowsRes;

const totals = { total: 0, withSrc: 0, withoutSrc: 0 };
const byKey = new Map();

for (const r of rows) {
  totals.total++;
  const conn = r.connection_id ?? '(no conn)';
  const src = r.source_calendar_id;
  if (src) {
    totals.withSrc++;
  } else {
    totals.withoutSrc++;
  }
  const key = `${conn}|${src ?? '(NULL)'}`;
  byKey.set(key, (byKey.get(key) ?? 0) + 1);
}

console.log(`\n  TOTAL ROWS: ${totals.total}`);
console.log(`  with source_calendar_id:    ${totals.withSrc}`);
console.log(`  without source_calendar_id: ${totals.withoutSrc} (pre-v1.6.1, never re-synced)`);

console.log(`\n  Breakdown by (connection_id, source_calendar_id):`);
const entries = [...byKey.entries()].sort((a, b) => b[1] - a[1]);
for (const [key, count] of entries) {
  const [conn, src] = key.split('|');
  const connShort = conn.slice(0, 8);
  console.log(`    ${connShort}... ${src.padEnd(40)} ${count}`);
}
