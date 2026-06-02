// Directus 11 permissions setup.
//
// Directus 11 restructured permissions: they now belong to POLICIES, not
// directly to roles. The chain is:
//
//   Role ── (directus_access) ──> Policy ── (directus_permissions) ──> Permission
//
// So we:
//   1. Create the role `gevoelscore-frontend-api` (idempotent — reuse if exists)
//   2. Create the policy `gevoelscore-frontend-policy` (idempotent)
//   3. Link policy ↔ role via directus_access (idempotent)
//   4. Create permission entries on the policy for each collection+action (idempotent)
//
// Idempotent: re-running is safe.

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('setup-permissions');

const ROLE_NAME = 'gevoelscore-frontend-api';
const POLICY_NAME = 'gevoelscore-frontend-policy';
const POLICY_DESCRIPTION =
  'Permissions for the gevoelscore Next.js frontend. CRUD on user-data collections; nothing on v2-placeholder or directus_* system collections.';

const FRONTEND_CRUD_COLLECTIONS = [
  'day_entries',
  'tags',
  'projects',
  'project_entries',
  'project_field_configs',
  'calendar_events',
  // v1.5 verloop-and-episodes (user-facing tab: Periodes). The frontend role
  // gets all 4 CRUD actions on episodes — the route handler is what gates
  // the actual API surface (no DELETE exposed; hard-delete is Directus admin
  // only). Consistency with the other user-data collections wins over a
  // narrow service-token permission set.
  'episodes',
];

const ACTIONS = ['create', 'read', 'update', 'delete'];

// ----------------------------------------------------------------------------
// 1. Role
// ----------------------------------------------------------------------------

let roleId = null;
const existingRoles = await directusRequest(
  `/roles?filter[name][_eq]=${encodeURIComponent(ROLE_NAME)}&limit=1`,
);
if (existingRoles.data && existingRoles.data.length > 0) {
  roleId = existingRoles.data[0].id;
  console.log(`  ⏩ Role "${ROLE_NAME}" exists (${roleId})`);
} else {
  console.log(`  ➕ Creating role "${ROLE_NAME}"...`);
  const res = await directusRequest('/roles', 'POST', {
    name: ROLE_NAME,
    description:
      'Role for the gevoelscore Next.js frontend. Assigned to a frontend-app Directus user (separate from admin recovery user).',
    icon: 'verified',
  });
  roleId = res.data.id;
  console.log(`  ✅ Role created: ${roleId}`);
}

// ----------------------------------------------------------------------------
// 2. Policy
// ----------------------------------------------------------------------------

let policyId = null;
const existingPolicies = await directusRequest(
  `/policies?filter[name][_eq]=${encodeURIComponent(POLICY_NAME)}&limit=1`,
);
if (existingPolicies.data && existingPolicies.data.length > 0) {
  policyId = existingPolicies.data[0].id;
  console.log(`  ⏩ Policy "${POLICY_NAME}" exists (${policyId})`);
} else {
  console.log(`  ➕ Creating policy "${POLICY_NAME}"...`);
  const res = await directusRequest('/policies', 'POST', {
    name: POLICY_NAME,
    description: POLICY_DESCRIPTION,
    icon: 'shield',
    app_access: false, // not a Directus admin UI policy
    admin_access: false, // explicitly not admin
  });
  policyId = res.data.id;
  console.log(`  ✅ Policy created: ${policyId}`);
}

// ----------------------------------------------------------------------------
// 3. Link policy to role via directus_access
// ----------------------------------------------------------------------------

const existingLinks = await directusRequest(
  `/access?filter[role][_eq]=${roleId}&filter[policy][_eq]=${policyId}&limit=1`,
);
if (existingLinks.data && existingLinks.data.length > 0) {
  console.log(`  ⏩ Role ↔ Policy link exists`);
} else {
  console.log(`  ➕ Linking role to policy...`);
  await directusRequest('/access', 'POST', {
    role: roleId,
    policy: policyId,
    sort: 1,
  });
  console.log(`  ✅ Role ↔ Policy linked`);
}

// ----------------------------------------------------------------------------
// 4. Permissions
// ----------------------------------------------------------------------------

console.log('\nGranting CRUD permissions:');

// Fetch all existing permissions on this policy in one call to avoid 4 queries per collection
const allExisting = await directusRequest(
  `/permissions?filter[policy][_eq]=${policyId}&limit=-1&fields=collection,action`,
);
const existingKeys = new Set(
  (allExisting.data ?? []).map((p) => `${p.collection}:${p.action}`),
);

for (const collection of FRONTEND_CRUD_COLLECTIONS) {
  for (const action of ACTIONS) {
    const key = `${collection}:${action}`;
    if (existingKeys.has(key)) {
      console.log(`  ⏩ ${collection}.${action} already granted`);
      continue;
    }
    await directusRequest('/permissions', 'POST', {
      policy: policyId,
      collection,
      action,
      permissions: {}, // empty filter = all rows (single-user app)
      validation: null,
      presets: null,
      fields: ['*'],
    });
    console.log(`  ✅ ${collection}.${action}`);
  }
}

console.log('\n--- Permissions NOT granted (intentional) ---');
console.log('  ❌ garmin_daily, health_daily, weather_daily — v2 native iOS app territory');
console.log('  ❌ directus_users, directus_roles, etc. — admin-only');
console.log('  ❌ Public role: no anonymous access anywhere (Directus default)');

console.log('\n✅ Permissions setup complete.');
console.log(`   Role ID:   ${roleId}`);
console.log(`   Policy ID: ${policyId}`);
console.log(
  '\nNext step: create a Directus user with the gevoelscore-frontend-api role (separate from your admin recovery user) when wiring up the frontend.\n',
);
