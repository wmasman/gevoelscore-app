// Production smoke for the calendar-binding step-1 backend.
//
// Architecture note: the OAuth connect step MUST be initiated from the
// browser (not from this Node script). When connect POSTs from Node,
// the Set-Cookie response containing the cal_oauth_state cookie is
// dropped — Node fetch doesn't have a cookie jar — so by the time
// Google redirects back to our callback, the browser has no state
// cookie and callback fails with `state_missing`.
//
// Workflow:
//   1. You initiate OAuth from your browser's devtools console (see
//      printed instructions). The browser handles the state cookie
//      correctly, OAuth completes, and you land at a 404 page with
//      ?connection_id=<UUID> in the URL.
//   2. You paste that connection_id into this script.
//   3. This script does the rest via Node fetch using your session
//      cookie (set in .env.local as GS_SESSION). list-calendars +
//      choose + sync don't need any cookies that browser-side
//      navigations create — only the session cookie, which Node
//      fetch can carry in the `cookie` request header.
//
// Prerequisites:
//   1. You're logged into https://gevoelscore-frontend.fly.dev in a browser.
//   2. .env.local has GS_SESSION=<gs_session-cookie-value>
//   3. The cookie was issued after the SameSite=Lax fix (commit 1a95d2b).

import readline from 'node:readline';

const BASE = process.env.CALENDAR_TEST_BASE ?? 'https://gevoelscore-frontend.fly.dev';
const SESSION = process.env.GS_SESSION;

if (!SESSION) {
  console.error('ERROR: GS_SESSION env var not set.');
  console.error('Set it via .env.local (sourced by run-calendar-binding-smoke.ps1).');
  process.exit(1);
}

const COOKIE = `gs_session=${SESSION}`;
const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function rl() {
  const r = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  return {
    ask: (q) => new Promise((resolve) => r.question(q, (a) => resolve(a.trim()))),
    close: () => r.close(),
  };
}

async function call(method, path, body) {
  const headers = {
    cookie: COOKIE,
    origin: BASE,
    'content-type': 'application/json',
  };
  const init = { method, headers };
  if (body !== undefined) init.body = JSON.stringify(body);
  const res = await fetch(`${BASE}${path}`, init);
  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = text;
  }
  return { status: res.status, data };
}

function banner(title) {
  console.log('\n' + '='.repeat(64));
  console.log(`  ${title}`);
  console.log('='.repeat(64));
}

const prompt = rl();

try {
  // ───────────────────────────────────────────────────────────────
  // 1. OAuth must run from the browser (cookie reasons; see header)
  // ───────────────────────────────────────────────────────────────
  banner('1. Initiate OAuth in your browser');
  console.log(`
   Why this can't run from this script:
     The cal_oauth_state cookie set by /api/calendars/google/connect
     must be stored IN the browser so it travels on Google's redirect
     back to our callback. A Node fetch can't put the cookie in your
     browser.

   Steps:
     a) Open this URL in your browser (where you are logged in to
        gevoelscore):

          ${BASE}/

     b) Open DevTools (F12) -> Console tab.

     c) Paste and run this snippet:

          fetch('/api/calendars/google/connect', { method: 'POST', credentials: 'include' })
            .then(r => r.json())
            .then(({ redirect_url }) => { window.location.href = redirect_url; });

     d) The browser will navigate to Google. Complete consent (you
        are listed as a test user). Google redirects back to:

          ${BASE}/api/calendars/google/callback?code=...

        The callback completes the data work + redirects to:

          ${BASE}/settings/kalenders/choose?connection_id=<UUID>

     e) The choose page doesn't exist yet (Phase 1.E), so you'll see
        a "Pagina niet gevonden" 404. EXPECTED. Read the URL bar:
        copy the value of the connection_id query parameter (a UUID).

     f) Verify in your browser DevTools -> Application -> Cookies:
        the cal_oauth_state cookie should now be GONE (the callback
        cleared it with Max-Age=0).
  `);
  const connectionId = await prompt.ask('   Paste the connection_id UUID from the URL bar: ');
  if (!connectionId) {
    console.error('   ❌ No connection_id provided. Aborting.');
    process.exit(1);
  }
  if (!UUID_REGEX.test(connectionId)) {
    console.error(`   ❌ "${connectionId}" is not a UUID.`);
    console.error('      You may still be at the callback URL (which means OAuth failed).');
    console.error('      Check the page body for a {"error":"..."} JSON response and');
    console.error('      share that error code. Aborting.');
    process.exit(1);
  }
  console.log(`   ✅ Using connection_id: ${connectionId}`);

  // ───────────────────────────────────────────────────────────────
  // 2. List calendars
  // ───────────────────────────────────────────────────────────────
  banner('2. GET /api/calendars/{connection_id}/calendars');
  const list = await call('GET', `/api/calendars/${connectionId}/calendars`);
  console.log(`   status: ${list.status}`);
  if (list.status !== 200) {
    console.error('   ❌ Expected 200. response:', JSON.stringify(list.data, null, 2));
    process.exit(1);
  }
  const calendars = list.data.calendars ?? [];
  console.log(`   ✅ ${calendars.length} calendar(s) found:`);
  for (const c of calendars) {
    console.log(`        - ${c.displayName}${c.isPrimary ? ' (PRIMARY)' : ''}  [${c.id}]`);
  }

  // ───────────────────────────────────────────────────────────────
  // 3. Choose calendars (all)
  // ───────────────────────────────────────────────────────────────
  banner('3. POST /api/calendars/{connection_id}/calendars  (include ALL)');
  const choose = await call('POST', `/api/calendars/${connectionId}/calendars`, {
    included_calendar_ids: calendars.map((c) => c.id),
  });
  console.log(`   status: ${choose.status}`);
  if (choose.status !== 200) {
    console.error('   ❌ Expected 200. response:', JSON.stringify(choose.data, null, 2));
    process.exit(1);
  }
  console.log(`   ✅ included_calendar_ids set (${calendars.length})`);

  // ───────────────────────────────────────────────────────────────
  // 4. Sync
  // ───────────────────────────────────────────────────────────────
  banner('4. POST /api/calendars/sync  (Ververs nu)');
  const sync = await call('POST', '/api/calendars/sync');
  console.log(`   status: ${sync.status}`);
  if (sync.status !== 200) {
    console.error('   ❌ Expected 200. response:', JSON.stringify(sync.data, null, 2));
    process.exit(1);
  }
  console.log('   ✅ sync result:');
  console.log(`        connections:               ${sync.data.connections}`);
  console.log(`        events_pulled:             ${sync.data.events_pulled}`);
  console.log(`        events_upserted:           ${sync.data.events_upserted}`);
  console.log(`        events_excluded_by_series: ${sync.data.events_excluded_by_series}`);
  console.log(`        errors:                    ${sync.data.errors.length}`);
  if (sync.data.errors.length > 0) {
    console.log('        error codes:               ' + sync.data.errors.join(', '));
  }

  // ───────────────────────────────────────────────────────────────
  // 5. Done
  // ───────────────────────────────────────────────────────────────
  banner('5. Done');
  console.log(`
   To verify in Directus admin:
     1. Open https://gevoelscore-backend.fly.dev/admin
     2. Content -> calendar_events
     3. You should see ${sync.data.events_upserted} row(s) in the window
        of (today - 7 days) to (today + 30 days).
     4. Content -> calendar_connections — your connection row with
        status='active' and last_synced_at populated.

   To re-test, repeat from step 1 (browser console snippet). The
   OAuth flow is idempotent — the second connect UPDATEs the
   existing connection row's refresh token.
  `);

  prompt.close();
} catch (e) {
  console.error('\n   ❌ Smoke failed:');
  console.error(e);
  prompt.close();
  process.exit(1);
}
