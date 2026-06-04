// Seeds the cron_monitor collection with the daily_calendar_sync row.
// Idempotent via UPSERT (PATCH if row exists by job_name; INSERT otherwise).
//
// Run after setup-calendar-collections.mjs + add-calendar-constraints.mjs.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "<admin static token>"
//   node directus/scripts/add-cron-monitor.mjs

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('add-cron-monitor');

const JOB_NAME = 'daily_calendar_sync';
const EXPECTED_INTERVAL_HOURS = 26; // 24h cycle + 2h buffer

// ─────────────────────────────────────────────────────────────────
// Check if the row already exists
// ─────────────────────────────────────────────────────────────────

const existing = await directusRequest(
  `/items/cron_monitor?filter[job_name][_eq]=${encodeURIComponent(JOB_NAME)}&limit=1`,
);

const rows = existing?.data ?? [];

if (rows.length > 0) {
  console.log(`  ⏩ ${JOB_NAME} row already seeded (id: ${rows[0].id})`);
  console.log('     Re-running is a no-op.\n');
  process.exit(0);
}

// ─────────────────────────────────────────────────────────────────
// Insert the seed row
// ─────────────────────────────────────────────────────────────────

await directusRequest('/items/cron_monitor', 'POST', {
  job_name: JOB_NAME,
  last_run_at: null,
  last_result: null,
  expected_interval_hours: EXPECTED_INTERVAL_HOURS,
  is_active: true,
});

console.log(`  ✅ Seeded ${JOB_NAME}`);
console.log(`     expected_interval_hours: ${EXPECTED_INTERVAL_HOURS}`);
console.log('     is_active: true');
console.log('     last_run_at: NULL (set by first sync run)\n');
