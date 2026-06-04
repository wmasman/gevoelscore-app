// Diagnostic: shows how calendar_events is distributed across time,
// to answer "why are we pulling 0 events after 2024-03-24?".
//
// Groups by year-month + counts, plus a per-recurrence breakdown.
// No PII to chat unless the user pastes it back; raw titles are not
// printed here, only counts.

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('diagnose-calendar-coverage');

const res = await directusRequest(
  '/items/calendar_events?fields=start_at,connection_id,recurrence_id,included_as_context,user_decision&limit=-1&sort=start_at',
);
const events = res.data ?? [];

console.log(`\n  Total events in calendar_events: ${events.length}\n`);

if (events.length === 0) {
  console.log('  (no events; nothing to diagnose)');
  process.exit(0);
}

// ─────────────────────────────────────────────────────────────────
// Distribution by year-month
// ─────────────────────────────────────────────────────────────────

const byMonth = new Map(); // 'YYYY-MM' -> { total, included, excluded }
for (const e of events) {
  const ym = e.start_at.slice(0, 7);
  let bucket = byMonth.get(ym);
  if (!bucket) {
    bucket = { total: 0, included: 0, excluded: 0 };
    byMonth.set(ym, bucket);
  }
  bucket.total++;
  if (e.included_as_context) bucket.included++;
  else bucket.excluded++;
}

const months = [...byMonth.keys()].sort();
const first = months[0];
const last = months[months.length - 1];

console.log(`  Time range: ${first}  ..  ${last}`);
console.log(`  Span:       ${months.length} months containing events`);
console.log('');
console.log('  Distribution per month:');
console.log('');
console.log('    ' + 'YYYY-MM'.padEnd(10) + 'total'.padEnd(8) + 'inc'.padEnd(6) + 'exc'.padEnd(6) + 'bar');
console.log('    ' + '─'.repeat(80));

const maxTotal = Math.max(...[...byMonth.values()].map((b) => b.total));

for (const ym of months) {
  const b = byMonth.get(ym);
  const barWidth = Math.round((b.total / maxTotal) * 40);
  const bar = '█'.repeat(barWidth);
  console.log(
    '    ' +
      ym.padEnd(10) +
      String(b.total).padEnd(8) +
      String(b.included).padEnd(6) +
      String(b.excluded).padEnd(6) +
      bar,
  );
}

// ─────────────────────────────────────────────────────────────────
// Distribution by year (compact summary)
// ─────────────────────────────────────────────────────────────────

const byYear = new Map();
for (const e of events) {
  const y = e.start_at.slice(0, 4);
  byYear.set(y, (byYear.get(y) ?? 0) + 1);
}
const years = [...byYear.keys()].sort();
console.log('');
console.log('  Per-year totals:');
for (const y of years) {
  console.log(`    ${y}:  ${byYear.get(y)}`);
}

// ─────────────────────────────────────────────────────────────────
// Largest gap: longest stretch of zero events
// ─────────────────────────────────────────────────────────────────

if (events.length >= 2) {
  let maxGapDays = 0;
  let gapStart = '';
  let gapEnd = '';
  for (let i = 1; i < events.length; i++) {
    const prev = new Date(events[i - 1].start_at);
    const curr = new Date(events[i].start_at);
    const gap = (curr - prev) / (24 * 60 * 60 * 1000);
    if (gap > maxGapDays) {
      maxGapDays = gap;
      gapStart = events[i - 1].start_at.slice(0, 10);
      gapEnd = events[i].start_at.slice(0, 10);
    }
  }
  console.log('');
  console.log(`  Largest gap: ${Math.round(maxGapDays)} days between ${gapStart} and ${gapEnd}`);
}

// ─────────────────────────────────────────────────────────────────
// Today's anchor
// ─────────────────────────────────────────────────────────────────

const today = new Date().toISOString().slice(0, 10);
const lastEvent = events[events.length - 1].start_at.slice(0, 10);
const daysSinceLast = Math.round(
  (new Date(today) - new Date(lastEvent)) / (24 * 60 * 60 * 1000),
);
console.log('');
console.log(`  Today:                ${today}`);
console.log(`  Latest event in DB:   ${lastEvent}`);
console.log(`  Days since latest:    ${daysSinceLast}`);
console.log('');

if (daysSinceLast > 60) {
  console.log('  ⚠️  Latest event is > 60 days old. Two possibilities:');
  console.log('       a) Your 4 included calendars genuinely went quiet (you moved');
  console.log('          your scheduling to Todoist / another tool); OR');
  console.log('       b) Some silent fetch failure for the recent date range.');
  console.log('');
  console.log('  Easy check: open Google Calendar in a browser, look at recent');
  console.log('  weeks across Family / Parro / Willem en Jantine / wmasman@gmail.com.');
  console.log('  If events are visible there but not here, that\'s a bug to fix.');
}
