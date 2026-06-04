// Lists all recurring event series currently in calendar_events,
// grouped by recurrence_id, sorted by instance count desc.
//
// Output is human-readable: title sample, calendar id, count, first
// and last start_at. Drives the pre-backfill curation step where you
// pick which series to add to calendar_series_exclusions before
// pulling years of historical events.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "<admin token>"
//   node directus/scripts/list-recurring-series.mjs

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('list-recurring-series');

// ─────────────────────────────────────────────────────────────────
// Fetch all events with non-null recurrence_id
// ─────────────────────────────────────────────────────────────────

// Directus REST API: filter calendar_events for recurrence_id != null,
// limit -1 = no pagination cap.
const url =
  '/items/calendar_events?' +
  'filter[recurrence_id][_nnull]=true&' +
  'fields=connection_id,recurrence_id,start_at,end_at,title,event_type,status,attendees_count&' +
  'limit=-1';

const response = await directusRequest(url);
const events = response.data ?? [];

console.log(`\n  Total recurring instances in calendar_events: ${events.length}\n`);

if (events.length === 0) {
  console.log('  (no recurring events found; nothing to curate)');
  process.exit(0);
}

// ─────────────────────────────────────────────────────────────────
// Group by recurrence_id
// ─────────────────────────────────────────────────────────────────

const groups = new Map();
for (const evt of events) {
  const key = `${evt.connection_id}::${evt.recurrence_id}`;
  let g = groups.get(key);
  if (!g) {
    g = {
      connection_id: evt.connection_id,
      recurrence_id: evt.recurrence_id,
      titles: new Map(), // title -> count, picks most common
      event_types: new Set(),
      statuses: new Set(),
      first_start: evt.start_at,
      last_start: evt.start_at,
      instances: 0,
      total_attendees: 0,
    };
    groups.set(key, g);
  }
  g.instances++;
  g.titles.set(evt.title, (g.titles.get(evt.title) ?? 0) + 1);
  if (evt.event_type) g.event_types.add(evt.event_type);
  g.statuses.add(evt.status);
  if (evt.start_at < g.first_start) g.first_start = evt.start_at;
  if (evt.start_at > g.last_start) g.last_start = evt.start_at;
  g.total_attendees += evt.attendees_count ?? 0;
}

// Resolve most-common title per group
for (const g of groups.values()) {
  let best = '';
  let bestCount = 0;
  for (const [t, c] of g.titles) {
    if (c > bestCount) {
      best = t;
      bestCount = c;
    }
  }
  g.title = best;
  g.avg_attendees = g.instances ? Math.round(g.total_attendees / g.instances) : 0;
}

// Sort by instance count desc (loudest series first)
const sorted = [...groups.values()].sort((a, b) => b.instances - a.instances);

// ─────────────────────────────────────────────────────────────────
// Lookup connection email per connection_id (for display only)
// ─────────────────────────────────────────────────────────────────

const connectionIds = [...new Set(sorted.map((g) => g.connection_id))];
const connEmails = new Map();
for (const cid of connectionIds) {
  try {
    const cres = await directusRequest(
      `/items/calendar_connections/${cid}?fields=provider_account_email`,
    );
    connEmails.set(cid, cres.data?.provider_account_email ?? '(unknown)');
  } catch {
    connEmails.set(cid, '(error)');
  }
}

// ─────────────────────────────────────────────────────────────────
// Print
// ─────────────────────────────────────────────────────────────────

console.log(`  ${sorted.length} unique recurrence series across ${connectionIds.length} connection(s):\n`);

console.log(
  '  ' +
    '#'.padEnd(4) +
    'count'.padEnd(7) +
    'first → last'.padEnd(26) +
    'type'.padEnd(13) +
    'attn'.padEnd(6) +
    'title',
);
console.log('  ' + '─'.repeat(110));

for (let i = 0; i < sorted.length; i++) {
  const g = sorted[i];
  const span = `${g.first_start.slice(0, 10)} → ${g.last_start.slice(0, 10)}`;
  const types = [...g.event_types].join(',') || 'default';
  const titleTrim = g.title.length > 50 ? g.title.slice(0, 47) + '...' : g.title;
  console.log(
    '  ' +
      String(i + 1).padEnd(4) +
      String(g.instances).padEnd(7) +
      span.padEnd(26) +
      types.padEnd(13) +
      String(g.avg_attendees).padEnd(6) +
      titleTrim,
  );
}

// ─────────────────────────────────────────────────────────────────
// Print the machine-readable list at the end for easy curation
// ─────────────────────────────────────────────────────────────────

console.log('\n  ── Machine-readable list (for add-series-exclusions input) ──\n');
console.log('  // Copy the recurrence_id of each series you want to exclude');
console.log('  // into directus/scripts/add-series-exclusions.mjs SERIES_TO_EXCLUDE array.');
console.log('');
for (let i = 0; i < sorted.length; i++) {
  const g = sorted[i];
  const safeTitle = g.title.replace(/\*\//g, '*\\/'); // avoid breaking the JS comment
  console.log(
    `  // #${i + 1} (${g.instances}× ${g.title.slice(0, 60)})  conn=${connEmails.get(g.connection_id)}`,
  );
  console.log(`  { recurrence_id: '${g.recurrence_id}', connection_id: '${g.connection_id}' },`);
}
console.log('');
