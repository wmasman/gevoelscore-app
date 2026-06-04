// Historical calendar backfill: pulls Google Calendar events from 2022-09-01
// (start of user's gevoelscore log) through today, chunked into 30-day
// windows so each sync stays within Google's per-request quota and our
// Directus API budget.
//
// Idempotent: re-running the same window upserts existing events by
// (connection_id, provider_event_id) UNIQUE — duplicates impossible.
//
// Prerequisites:
//   1. Step-1 OAuth + sync proven working (user has 1+ rows in
//      calendar_connections with status='active').
//   2. .env.local has GS_SESSION=<gs_session-cookie-value> from a logged-in
//      browser session.
//
// Usage:
//   $env:GS_SESSION = "<cookie>"
//   $env:CALENDAR_BACKFILL_FROM = "2022-09-01"   # optional, default 2022-09-01
//   $env:CALENDAR_BACKFILL_TO   = "2026-06-04"   # optional, default today
//   $env:CALENDAR_TEST_BASE     = "https://gevoelscore-frontend.fly.dev"  # optional
//   node scripts/calendar-historical-backfill.mjs

const BASE = process.env.CALENDAR_TEST_BASE ?? 'https://gevoelscore-frontend.fly.dev';
const SESSION = process.env.GS_SESSION;

if (!SESSION) {
  console.error('ERROR: GS_SESSION env var not set.');
  console.error('Source it via .env.local + the helper PowerShell wrapper.');
  process.exit(1);
}

const COOKIE = `gs_session=${SESSION}`;
const DEFAULT_FROM = '2022-09-01';
const CHUNK_DAYS = 30;
const MS_PER_DAY = 24 * 60 * 60 * 1000;

const fromArg = process.env.CALENDAR_BACKFILL_FROM ?? DEFAULT_FROM;
const toArg = process.env.CALENDAR_BACKFILL_TO ?? new Date().toISOString().slice(0, 10);

const startDate = new Date(fromArg + 'T00:00:00Z');
const endDate = new Date(toArg + 'T23:59:59Z');

if (Number.isNaN(startDate.getTime()) || Number.isNaN(endDate.getTime())) {
  console.error('ERROR: invalid from/to date. Use YYYY-MM-DD format.');
  process.exit(1);
}
if (startDate >= endDate) {
  console.error('ERROR: from must be before to.');
  process.exit(1);
}

const totalDays = Math.round((endDate.getTime() - startDate.getTime()) / MS_PER_DAY);
const chunks = Math.ceil(totalDays / CHUNK_DAYS);

console.log('=' .repeat(64));
console.log('  Calendar historical backfill');
console.log('=' .repeat(64));
console.log(`  Range:       ${fromArg}  ..  ${toArg}`);
console.log(`  Total days:  ${totalDays}`);
console.log(`  Chunk size:  ${CHUNK_DAYS} days`);
console.log(`  Chunks:      ${chunks}`);
console.log(`  Target:      ${BASE}`);
console.log('=' .repeat(64));
console.log('');

async function callSync(from, to) {
  const url = `${BASE}/api/calendars/sync?from=${encodeURIComponent(from.toISOString())}&to=${encodeURIComponent(to.toISOString())}`;
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      cookie: COOKIE,
      origin: BASE,
      'content-type': 'application/json',
    },
  });
  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = { error: 'non_json', raw: text.slice(0, 200) };
  }
  return { status: res.status, data };
}

function fmtDate(d) {
  return d.toISOString().slice(0, 10);
}

const totals = {
  chunks_succeeded: 0,
  chunks_failed: 0,
  events_pulled: 0,
  events_upserted: 0,
  events_excluded_by_series: 0,
  errors: [],
};

const startedAt = Date.now();

for (let i = 0; i < chunks; i++) {
  const chunkFrom = new Date(startDate.getTime() + i * CHUNK_DAYS * MS_PER_DAY);
  const chunkToCandidate = new Date(chunkFrom.getTime() + CHUNK_DAYS * MS_PER_DAY);
  const chunkTo = chunkToCandidate > endDate ? endDate : chunkToCandidate;

  process.stdout.write(
    `  [${String(i + 1).padStart(2)}/${chunks}]  ${fmtDate(chunkFrom)} → ${fmtDate(chunkTo)}  ... `,
  );

  const result = await callSync(chunkFrom, chunkTo);

  if (result.status !== 200) {
    console.log(`❌ ${result.status}`);
    console.log(`        error: ${JSON.stringify(result.data)}`);
    totals.chunks_failed++;
    totals.errors.push(`chunk ${i + 1}: HTTP ${result.status}`);
    // Continue with next chunk — don't abort the whole backfill on one
    // failure (e.g. transient Google API hiccup). Each chunk is
    // independent + idempotent.
    continue;
  }

  const d = result.data;
  totals.chunks_succeeded++;
  totals.events_pulled += d.events_pulled ?? 0;
  totals.events_upserted += d.events_upserted ?? 0;
  totals.events_excluded_by_series += d.events_excluded_by_series ?? 0;
  if (d.errors && d.errors.length > 0) {
    totals.errors.push(...d.errors.map((e) => `chunk ${i + 1}: ${e}`));
  }
  console.log(
    `✅ pulled=${d.events_pulled} upserted=${d.events_upserted} excluded=${d.events_excluded_by_series}`,
  );
}

const elapsedSec = Math.round((Date.now() - startedAt) / 1000);

console.log('');
console.log('=' .repeat(64));
console.log('  Backfill summary');
console.log('=' .repeat(64));
console.log(`  Chunks succeeded:          ${totals.chunks_succeeded}/${chunks}`);
console.log(`  Chunks failed:             ${totals.chunks_failed}`);
console.log(`  Events pulled (total):     ${totals.events_pulled}`);
console.log(`  Events upserted (total):   ${totals.events_upserted}`);
console.log(`  Excluded by series rules:  ${totals.events_excluded_by_series}`);
console.log(`  Per-chunk errors:          ${totals.errors.length}`);
console.log(`  Elapsed:                   ${elapsedSec}s`);
if (totals.errors.length > 0) {
  console.log('');
  console.log('  Error codes:');
  for (const e of totals.errors.slice(0, 20)) {
    console.log(`    - ${e}`);
  }
  if (totals.errors.length > 20) {
    console.log(`    ... and ${totals.errors.length - 20} more`);
  }
}
console.log('=' .repeat(64));
console.log('');
console.log('  Verify in Directus admin:');
console.log('    Open https://gevoelscore-backend.fly.dev/admin');
console.log('    Content → calendar_events  (filter by start_at)');
console.log('');

process.exit(totals.chunks_failed > 0 ? 1 : 0);
