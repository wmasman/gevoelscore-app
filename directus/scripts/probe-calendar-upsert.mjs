// Diagnostic: probe calendar_connections upsert directly via the admin
// token. Mimics what the callback route does in upsertConnection but
// surfaces the real Directus error message (which the wrapper swallows
// via classifyError -> generic 'directus_error').
//
// Usage:
//   $env:DIRECTUS_TOKEN = "<admin token>"
//   node directus/scripts/probe-calendar-upsert.mjs

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('probe-calendar-upsert');

const USER_ID = process.env.WILLEM_USER_ID ?? '16f6f68b-e683-4dc9-8afc-e80695c4259d';
const TEST_EMAIL = 'probe-' + Date.now() + '@example.com';

console.log('\n  ── Step 1: read calendar_connections (smoke) ──');
try {
  const list = await directusRequest('/items/calendar_connections?limit=5');
  console.log(`  ✅ read ok. ${list.data?.length ?? 0} existing row(s):`);
  for (const r of list.data ?? []) {
    console.log(`     - id=${r.id} provider=${r.provider} email=${r.provider_account_email} status=${r.status}`);
  }
} catch (e) {
  console.error('  ❌ read failed:');
  console.error(e.message);
  process.exit(1);
}

console.log('\n  ── Step 2: filtered read (the upsert helper does this first) ──');
try {
  const url = `/items/calendar_connections?filter[_and][0][user_id][_eq]=${encodeURIComponent(USER_ID)}&filter[_and][1][provider][_eq]=google&filter[_and][2][provider_account_email][_eq]=${encodeURIComponent(TEST_EMAIL)}&limit=1`;
  const filtered = await directusRequest(url);
  console.log(`  ✅ filtered read ok. ${filtered.data?.length ?? 0} match(es).`);
} catch (e) {
  console.error('  ❌ filtered read failed:');
  console.error(e.message);
  process.exit(1);
}

console.log('\n  ── Step 3: create a test row ──');
let createdId = null;
try {
  const created = await directusRequest('/items/calendar_connections', 'POST', {
    user_id: USER_ID,
    provider: 'google',
    provider_account_email: TEST_EMAIL,
    refresh_token_encrypted: 'v1.test.test.test',
    scope: 'https://www.googleapis.com/auth/calendar.readonly',
    connected_at: new Date().toISOString(),
    last_synced_at: null,
    last_sync_error: null,
    status: 'active',
    included_calendar_ids: [],
  });
  createdId = created.data?.id;
  console.log(`  ✅ create ok. id=${createdId}`);
} catch (e) {
  console.error('  ❌ create FAILED — this is the bug:');
  console.error('     ' + e.message);
  process.exit(1);
}

console.log('\n  ── Step 4: cleanup ──');
try {
  if (createdId) {
    await directusRequest(`/items/calendar_connections/${createdId}`, 'DELETE');
    console.log(`  ✅ test row ${createdId} deleted`);
  }
} catch (e) {
  console.error(`  ⚠️  cleanup failed (manual delete needed for id=${createdId}):`);
  console.error('     ' + e.message);
}

console.log('\n  ✅ Probe successful. Schema + permissions + admin token all OK.');
console.log('     If the callback still fails directus_error, the bug is in');
console.log('     how the Next.js process is calling Directus (URL, token env,');
console.log('     internal network resolution), not in Directus itself.\n');
