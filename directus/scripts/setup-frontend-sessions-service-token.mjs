// Provisions a scoped Directus service user + token for the Next.js
// frontend session store (S-H1 in the 2026-05-30 audit).
//
// What it creates:
//   - Policy `gevoelscore-frontend-sessions-only-policy` with CRUD on
//     the frontend_sessions collection ONLY. No admin_access, no
//     app_access — the token can't read users, day_entries, tags,
//     anything else. Single-purpose.
//   - Role `gevoelscore-frontend-sessions-service-role` with that
//     policy attached via directus_access.
//   - User `frontend-sessions-service@gevoelscore.internal`
//     (status=active, role=above). Email is a non-routable internal
//     value — this user never logs in interactively, it exists only
//     to anchor a token.
//   - Static token on that user (48 random bytes, base64url).
//
// After running this you swap the Fly secret on the frontend app and
// the Next.js machine stops holding the Directus admin token. That
// closes audit finding S-H1 — single-token bypass of all access
// control.
//
// Idempotent: re-run rotates the token (overwrites the user's `token`
// field — Directus invalidates the previous on overwrite) and
// reconciles the policy/role/permissions if any drifted. Safe to run
// any number of times.
//
// USAGE:
//   $env:DIRECTUS_TOKEN = "<admin static token>"   # current admin token
//   node directus/scripts/setup-frontend-sessions-service-token.mjs
//
// The script prints the new token at the end. Capture it ONCE and set
// it as the frontend's Fly secret immediately:
//   fly secrets set DIRECTUS_TOKEN="<token>" -a gevoelscore-frontend
//
// AFTER you've verified the frontend session store still works with
// the scoped token, you may rotate the OLD admin token. See
// docs/operations/runbooks/rotate-credentials.md.

import crypto from 'node:crypto';
import { banner, directusRequest } from './lib/directus-request.mjs';

banner('setup-frontend-sessions-service-token');

const COLLECTION = 'frontend_sessions';
const POLICY_NAME = 'gevoelscore-frontend-sessions-only-policy';
const ROLE_NAME = 'gevoelscore-frontend-sessions-service-role';
// Email uses RFC 2606's reserved `example.com` so it passes Directus's
// strict email validator without colliding with any real mailbox.
// This account is never used interactively — the email is a label,
// not a routable address.
const USER_EMAIL = 'frontend-sessions-service@example.com';
const ACTIONS = ['create', 'read', 'update', 'delete'];

// 1) Policy ------------------------------------------------------------------
let policyId;
{
  const res = await directusRequest(
    `/policies?filter[name][_eq]=${encodeURIComponent(POLICY_NAME)}&limit=1`,
  );
  if (res.data && res.data.length > 0) {
    policyId = res.data[0].id;
    console.log(`  ⏩ policy "${POLICY_NAME}" already exists (${policyId})`);
  } else {
    const created = await directusRequest('/policies', 'POST', {
      name: POLICY_NAME,
      icon: 'lock',
      description:
        'CRUD on frontend_sessions only. Scoped service-token policy for the Next.js frontend.',
      admin_access: false,
      app_access: false,
    });
    policyId = created.data.id;
    console.log(`  ✅ created policy (${policyId})`);
  }
}

// 2) Permissions on frontend_sessions ---------------------------------------
{
  const existing = await directusRequest(
    `/permissions?filter[policy][_eq]=${policyId}&filter[collection][_eq]=${COLLECTION}&fields=action&limit=-1`,
  );
  const granted = new Set((existing.data ?? []).map((p) => p.action));
  for (const action of ACTIONS) {
    if (granted.has(action)) {
      console.log(`  ⏩ ${COLLECTION}.${action} already granted`);
      continue;
    }
    await directusRequest('/permissions', 'POST', {
      policy: policyId,
      collection: COLLECTION,
      action,
      permissions: {},
      validation: null,
      presets: null,
      fields: ['*'],
    });
    console.log(`  ✅ granted ${COLLECTION}.${action}`);
  }
}

// 3) Role -------------------------------------------------------------------
let roleId;
{
  const res = await directusRequest(
    `/roles?filter[name][_eq]=${encodeURIComponent(ROLE_NAME)}&limit=1`,
  );
  if (res.data && res.data.length > 0) {
    roleId = res.data[0].id;
    console.log(`  ⏩ role "${ROLE_NAME}" already exists (${roleId})`);
  } else {
    const created = await directusRequest('/roles', 'POST', {
      name: ROLE_NAME,
      icon: 'shield',
      description:
        'Service role for the Next.js frontend session store. Do NOT assign to interactive users.',
    });
    roleId = created.data.id;
    console.log(`  ✅ created role (${roleId})`);
  }
}

// 4) Attach policy to role (directus_access pivot) --------------------------
{
  const res = await directusRequest(
    `/access?filter[role][_eq]=${roleId}&filter[policy][_eq]=${policyId}&fields=id&limit=1`,
  );
  if (res.data && res.data.length > 0) {
    console.log(`  ⏩ policy already attached to role`);
  } else {
    await directusRequest('/access', 'POST', {
      role: roleId,
      policy: policyId,
    });
    console.log(`  ✅ attached policy to role`);
  }
}

// 5) Service user ----------------------------------------------------------
let userId;
{
  const res = await directusRequest(
    `/users?filter[email][_eq]=${encodeURIComponent(USER_EMAIL)}&limit=1`,
  );
  if (res.data && res.data.length > 0) {
    userId = res.data[0].id;
    console.log(`  ⏩ service user "${USER_EMAIL}" already exists (${userId})`);
    // Ensure role is correctly assigned in case it drifted.
    if (res.data[0].role !== roleId) {
      await directusRequest(`/users/${userId}`, 'PATCH', { role: roleId });
      console.log(`  ✅ re-assigned user to scoped role`);
    }
  } else {
    const created = await directusRequest('/users', 'POST', {
      email: USER_EMAIL,
      first_name: 'frontend-sessions',
      last_name: 'service',
      role: roleId,
      status: 'active',
      description:
        'Service account for the Next.js frontend session store. Do NOT log in interactively — used only to anchor a static token.',
    });
    userId = created.data.id;
    console.log(`  ✅ created service user (${userId})`);
  }
}

// 6) Mint a fresh token -----------------------------------------------------
// crypto.randomBytes is CSPRNG. 48 bytes → 64 base64url chars (no
// padding, URL-safe). Directus stores tokens plaintext in
// directus_users.token; overwriting invalidates the previous value.
const newToken = crypto.randomBytes(48).toString('base64url');
await directusRequest(`/users/${userId}`, 'PATCH', { token: newToken });
console.log(`  ✅ minted fresh static token (previous, if any, invalidated)`);

// 7) Output ----------------------------------------------------------------
console.log('\n' + '='.repeat(72));
console.log('NEW SCOPED DIRECTUS TOKEN — capture once and set on Fly immediately:');
console.log('='.repeat(72));
console.log(newToken);
console.log('='.repeat(72));
console.log('\nNext steps:');
console.log(
  '  1. fly secrets set DIRECTUS_TOKEN="' + newToken + '" -a gevoelscore-frontend',
);
console.log('  2. Wait ~90 s for the Fly redeploy.');
console.log('  3. Open https://gevoelscore-frontend.fly.dev/ in incognito.');
console.log('  4. Log in; confirm the session survives a page reload.');
console.log('\nAFTER successful verification you may rotate the OLD admin token.');
console.log('See docs/operations/runbooks/rotate-credentials.md (section: scoped token).');
console.log('');
