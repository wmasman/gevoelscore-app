// One-off probe: list which v1 placeholder fields still exist on
// calendar_events. Tells us why setup-calendar-collections is still
// running its guard. Read-only.

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('probe-placeholder-fields');

const V1_PLACEHOLDER_FIELDS = [
  'google_event_id',
  'calendar_source',
  'relevance',
  'category_hint',
  'date',
  'start_time',
  'end_time',
  'attendees_count',
];

async function fieldExists(collection, field) {
  try {
    await directusRequest(`/fields/${collection}/${field}`);
    return true;
  } catch (e) {
    const msg = String(e.message);
    if (msg.includes('404') || msg.includes('FORBIDDEN')) return false;
    throw e;
  }
}

for (const f of V1_PLACEHOLDER_FIELDS) {
  const present = await fieldExists('calendar_events', f);
  console.log(`  ${present ? 'PRESENT' : 'gone   '} ${f}`);
}
