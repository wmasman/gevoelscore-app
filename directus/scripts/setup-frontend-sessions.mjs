// Creates the frontend_sessions collection in Directus + grants CRUD to
// the gevoelscore-frontend-policy. Idempotent.
//
// Why a Directus collection: the auth flow stored sessions in a process-
// local Map on the Fly frontend machine. Every deploy/restart wiped the
// store, leaving phones with stale cookies that pointed to nothing — the
// home page rendered empty data and the user had no signal to log back in.
// Persisting sessions in Directus survives all frontend restarts.
//
// What it stores: { id (uuid), access_token, refresh_token, expires_at }.
// The id IS the session id sent in the gs_session cookie; access/refresh
// tokens are the Directus tokens issued at login. expires_at lets us evict
// stale rows.
//
// Tokens are stored in plaintext for v1. The collection lives inside the
// user's own self-hosted Directus, alongside their day_entries, and a
// hosted-Directus breach already exposes the source data anyway. If/when
// multi-user lands, add field-level encryption with a separate KMS-held
// key before opening up.
//
// Permissions: granted to the existing gevoelscore-frontend-policy. The
// frontend Fly machine reads `DIRECTUS_TOKEN` (the admin service token)
// at runtime to talk to this collection, since the user has no JWT yet
// at the moment we create their session.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "<admin static token>"
//   node directus/scripts/setup-frontend-sessions.mjs

import {
  banner,
  collectionExists,
  directusRequest,
} from './lib/directus-request.mjs';

banner('setup-frontend-sessions');

const COLLECTION = 'frontend_sessions';
const POLICY_NAME = 'gevoelscore-frontend-policy';

// ----------------------------------------------------------------------------
// 1. Create the collection
// ----------------------------------------------------------------------------

if (await collectionExists(COLLECTION)) {
  console.log(`  ⏩ ${COLLECTION} already exists`);
} else {
  console.log(`  ➕ Creating ${COLLECTION}...`);
  await directusRequest('/collections', 'POST', {
    collection: COLLECTION,
    schema: { name: COLLECTION },
    meta: {
      icon: 'fingerprint',
      hidden: true,
      note: 'Server-side session store for the Next.js frontend. Survives Fly restarts.',
    },
    fields: [
      {
        field: 'id',
        type: 'uuid',
        // The app generates the session id (crypto.randomUUID) and POSTs it
        // alongside the row — no DB-side auto-increment, no Directus uuid
        // special handler, so the id we set is the id we get back.
        schema: { is_primary_key: true, has_auto_increment: false, is_nullable: false },
        meta: { hidden: true, readonly: true, interface: 'input' },
      },
      {
        field: 'access_token',
        type: 'text',
        schema: { is_nullable: false },
        meta: { hidden: true, interface: 'input-multiline' },
      },
      {
        field: 'refresh_token',
        type: 'text',
        schema: { is_nullable: false },
        meta: { hidden: true, interface: 'input-multiline' },
      },
      {
        field: 'expires_at',
        type: 'timestamp',
        schema: { is_nullable: false },
        meta: {
          interface: 'datetime',
          note: 'Access-token expiry. After this point getValidatedSession will refresh.',
        },
      },
      {
        field: 'created_at',
        type: 'timestamp',
        schema: { is_nullable: true },
        meta: { special: ['date-created'], readonly: true, interface: 'datetime' },
      },
    ],
  });
  console.log(`  ✅ ${COLLECTION}`);
}

// ----------------------------------------------------------------------------
// 2. Grant CRUD on the existing frontend policy
// ----------------------------------------------------------------------------

const policyRes = await directusRequest(
  `/policies?filter[name][_eq]=${encodeURIComponent(POLICY_NAME)}&limit=1`,
);
if (!policyRes.data || policyRes.data.length === 0) {
  console.error(
    `\n  ❌ Policy "${POLICY_NAME}" not found. Run setup-permissions.mjs first.\n`,
  );
  process.exit(1);
}
const policyId = policyRes.data[0].id;
console.log(`\n  Policy: ${POLICY_NAME} (${policyId})`);

const ACTIONS = ['create', 'read', 'update', 'delete'];

const existingPerms = await directusRequest(
  `/permissions?filter[policy][_eq]=${policyId}&filter[collection][_eq]=${COLLECTION}&fields=collection,action&limit=-1`,
);
const granted = new Set((existingPerms.data ?? []).map((p) => p.action));

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
  console.log(`  ✅ ${COLLECTION}.${action}`);
}

console.log('\n✅ frontend_sessions setup complete.');
console.log(
  '\nNext: set DIRECTUS_TOKEN on the Fly frontend machine:',
);
console.log('  flyctl secrets set DIRECTUS_TOKEN="<admin-static-token>" -a gevoelscore-frontend\n');
