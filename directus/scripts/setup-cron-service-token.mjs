// Provisions a scoped Directus service user + token for the calendar
// cron (step-2 of the calendar-binding feature). Separate from the
// session store's scoped token (S-H1) because:
//   - The session store token is locked to frontend_sessions ONLY
//   - The cron needs CRUD on calendar_connections, calendar_events,
//     calendar_series_exclusions, cron_monitor — i.e. the same scope
//     as the existing user-action routes (per session.accessToken),
//     but operating system-wide on behalf of a schedule, not a user
//
// Design choice: REUSE the existing `gevoelscore-frontend-api` role
// (with the `gevoelscore-frontend-policy` already covering the calendar
// collections). Don't create a separate cron-only policy. Trade-off:
// the cron service token has slightly broader perms than strictly
// necessary (it could also CRUD tags/episodes/day_entries via that
// policy), but it lives only on the Fly machine + GHA, never in the
// browser. A future hardening pass can split into a cron-only policy
// if soak surfaces a real attack surface. Tracked as a follow-up.
//
// Idempotent: re-running rotates the token (overwrites the user's
// `token` field — Directus invalidates the previous on overwrite) and
// reconciles the role assignment if it drifted.
//
// USAGE:
//   $env:DIRECTUS_TOKEN = "<admin static token>"   # admin token from .env.local
//   node directus/scripts/setup-cron-service-token.mjs
//
// Prints the new token at the end. Capture it ONCE and set it as the
// frontend's Fly secret:
//   fly secrets set CALENDAR_CRON_DIRECTUS_TOKEN="<token>" -a gevoelscore-frontend
//
// The cron's `/api/calendars/sync` bearer path reads this env var
// (replacing the misleading process.env.DIRECTUS_TOKEN used in step-1
// per the TODO(step-2) comment in src/app/api/calendars/sync/route.ts).

import crypto from 'node:crypto';
import { banner, directusRequest } from './lib/directus-request.mjs';

banner('setup-cron-service-token');

// MUST match the role created by setup-permissions.mjs. If you change
// either, update both.
const ROLE_NAME = 'gevoelscore-frontend-api';
const USER_EMAIL = 'frontend-cron-service@example.com';

// 1) Look up the existing role (created by setup-permissions.mjs) -----------
let roleId;
{
  const res = await directusRequest(
    `/roles?filter[name][_eq]=${encodeURIComponent(ROLE_NAME)}&limit=1`,
  );
  if (!res.data || res.data.length === 0) {
    console.error(`\n❌ role "${ROLE_NAME}" not found.`);
    console.error('   Run setup-permissions.mjs first to create it.');
    process.exit(1);
  }
  roleId = res.data[0].id;
  console.log(`  ⏩ role "${ROLE_NAME}" found (${roleId})`);
}

// 2) Service user -----------------------------------------------------------
let userId;
{
  const res = await directusRequest(
    `/users?filter[email][_eq]=${encodeURIComponent(USER_EMAIL)}&limit=1`,
  );
  if (res.data && res.data.length > 0) {
    userId = res.data[0].id;
    console.log(`  ⏩ service user "${USER_EMAIL}" already exists (${userId})`);
    if (res.data[0].role !== roleId) {
      await directusRequest(`/users/${userId}`, 'PATCH', { role: roleId });
      console.log(`  ✅ re-assigned user to ${ROLE_NAME} role`);
    }
  } else {
    const created = await directusRequest('/users', 'POST', {
      email: USER_EMAIL,
      first_name: 'frontend-cron',
      last_name: 'service',
      role: roleId,
      status: 'active',
      description:
        'Service account for the calendar daily-sync cron (GHA-triggered). Do NOT log in interactively — used only to anchor a static token.',
    });
    userId = created.data.id;
    console.log(`  ✅ created service user (${userId})`);
  }
}

// 3) Mint a fresh token -----------------------------------------------------
// crypto.randomBytes is CSPRNG. 48 bytes → 64 base64url chars (no padding,
// URL-safe). Directus invalidates any previous token on overwrite.
const newToken = crypto.randomBytes(48).toString('base64url');
await directusRequest(`/users/${userId}`, 'PATCH', { token: newToken });
console.log(`  ✅ minted fresh static token (previous, if any, invalidated)`);

// 4) Output -----------------------------------------------------------------
console.log('\n' + '='.repeat(72));
console.log('NEW CRON DIRECTUS TOKEN — capture once and set on Fly immediately:');
console.log('='.repeat(72));
console.log(newToken);
console.log('='.repeat(72));
console.log('\nNext steps:');
console.log(
  '  1. fly secrets set CALENDAR_CRON_DIRECTUS_TOKEN="' +
    newToken +
    '" -a gevoelscore-frontend',
);
console.log('  2. Wait ~90 s for the Fly redeploy (or batch with other deploys).');
console.log(
  '  3. After deploy, the bearer-gated path of /api/calendars/sync uses\n     this token; manual `Ververs nu` (session path) is unaffected.',
);
console.log('  4. Trigger the GHA cron and confirm the watchdog reports OK.');
console.log('');
