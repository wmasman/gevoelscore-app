// Find the anchor dates we need to lock down the Garmin investigation
// timeline:
//   - Ardennes cycling weekend (suspected LC-onset trigger event)
//   - First gevoelscore day_entry (start of subjective-label window)
//   - Any crash-related tags in the system (to inform crash_v1 definition)
//
// READ-ONLY. Uses the project's standard DIRECTUS_TOKEN wrapper — run via
// powershell -ExecutionPolicy Bypass -File scripts/run-directus-script.ps1
//   -Script docs/research/garmin/scripts/04_query_anchor_dates.mjs

import { directusRequest, URL } from '../../../../directus/scripts/lib/directus-request.mjs';

console.log(`Target: ${URL}\n`);

// ─────────────────────────────────────────────────────────────────
// 1. Ardennes search — title/location contains "arden" (covers
//    "Ardennen" / "Ardennes" / "ardennen"), and a wider net for
//    "fiets" / "cycling" weekends in late 2021 / early 2022.
// ─────────────────────────────────────────────────────────────────
async function searchEvents(filterDesc, filter, limit = 25) {
  const qs = new URLSearchParams({
    fields: 'id,start_at,end_at,all_day,title,location,event_type,status,attendees_count',
    sort: 'start_at',
    limit: String(limit),
    filter: JSON.stringify(filter),
  });
  const r = await directusRequest(`/items/calendar_events?${qs}`);
  console.log(`\n--- ${filterDesc} (${r.data.length} hit${r.data.length === 1 ? '' : 's'}) ---`);
  for (const ev of r.data) {
    const start = (ev.start_at || '').slice(0, 16);
    const end = (ev.end_at || '').slice(0, 16);
    console.log(`  ${start} → ${end}  ${ev.all_day ? '[allday]' : ''}  ${ev.title || '(no title)'}  ${ev.location ? `@ ${ev.location}` : ''}`);
  }
}

await searchEvents(
  'calendar events with "arden" in title (case-insensitive)',
  { title: { _icontains: 'arden' } },
);

await searchEvents(
  'calendar events with "arden" in location (case-insensitive)',
  { location: { _icontains: 'arden' } },
);

await searchEvents(
  'cycling-themed events in the 2021-09 → 2022-06 onset window',
  {
    _and: [
      { start_at: { _between: ['2021-09-01', '2022-06-01'] } },
      {
        _or: [
          { title: { _icontains: 'fiets' } },
          { title: { _icontains: 'cycling' } },
          { title: { _icontains: 'bike' } },
          { title: { _icontains: 'weekend' } },
        ],
      },
    ],
  },
  50,
);

// ─────────────────────────────────────────────────────────────────
// 2. First gevoelscore day_entry — earliest entry_date.
//    Just need the boundary; pull only what's necessary.
// ─────────────────────────────────────────────────────────────────
const firstEntries = await directusRequest(
  '/items/day_entries?fields=id,date,score&sort=date&limit=5',
);
console.log('\n--- first 5 day_entries (gevoelscore tracking start) ---');
for (const e of firstEntries.data) {
  console.log(`  ${e.date}  score=${e.score}  id=${e.id}`);
}

const totalEntries = await directusRequest(
  '/items/day_entries?aggregate[count]=id&limit=0',
);
console.log(`  total day_entries: ${totalEntries.data?.[0]?.count?.id ?? totalEntries.data}`);

// Calendar coverage: how early do calendar events go?
const earliestEvents = await directusRequest(
  '/items/calendar_events?fields=id,start_at,title&sort=start_at&limit=5',
);
console.log('\n--- earliest 5 calendar_events (calendar coverage start) ---');
for (const ev of earliestEvents.data) {
  console.log(`  ${(ev.start_at || '').slice(0, 16)}  ${ev.title || '(no title)'}  id=${ev.id}`);
}

// ─────────────────────────────────────────────────────────────────
// 3. Crash-related tags — informs crash_v1 operational definition.
// ─────────────────────────────────────────────────────────────────
const crashTags = await directusRequest(
  `/items/tags?fields=id,label,category&filter=${encodeURIComponent(
    JSON.stringify({
      _or: [
        { label: { _icontains: 'crash' } },
        { label: { _icontains: 'pem' } },
        { label: { _icontains: 'dip' } },
      ],
    }),
  )}&limit=25`,
);
console.log('\n--- tags matching crash / pem / dip ---');
for (const t of crashTags.data) {
  console.log(`  [${t.category}] ${t.label}  id=${t.id}`);
}
if (crashTags.data.length === 0) {
  console.log('  (none found — crash_v1 will need to be derived from score, not tags)');
}

console.log('\nDone.');
