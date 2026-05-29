// Creates a Directus user for end-to-end verification without 2FA.
// The user gets the existing `gevoelscore-frontend-api` role so the auth
// flow + the app's CRUD against day_entries / tags work exactly as a real
// user — but no TOTP, so headless browsers can drive the login flow.
//
// Run:
//   $env:DIRECTUS_TOKEN = "<admin>"
//   node scripts/create-test-user.mjs
//
// Prints email + password. Run with DELETE=1 to tear down by email.

const URL = process.env.DIRECTUS_URL || 'https://gevoelscore-backend.fly.dev';
const TOKEN = process.env.DIRECTUS_TOKEN;
if (!TOKEN) {
  console.error('DIRECTUS_TOKEN not set');
  process.exit(1);
}

const EMAIL = process.env.TEST_EMAIL || 'verify-bot@gevoelscore.test';
const PASSWORD = process.env.TEST_PASSWORD || `Verify-${Math.random().toString(36).slice(2, 12)}-${Date.now().toString(36)}`;
const ROLE_NAME = 'gevoelscore-frontend-api';

async function api(path, init = {}) {
  const res = await fetch(`${URL}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      'Content-Type': 'application/json',
      ...(init.headers ?? {}),
    },
  });
  if (!res.ok) {
    throw new Error(`HTTP ${res.status} on ${init.method ?? 'GET'} ${path}\n${await res.text()}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

const roles = await api(`/roles?filter[name][_eq]=${encodeURIComponent(ROLE_NAME)}&limit=1`);
const role = roles.data?.[0];
if (!role) {
  console.error(`role "${ROLE_NAME}" not found`);
  process.exit(1);
}

const existing = await api(`/users?filter[email][_eq]=${encodeURIComponent(EMAIL)}&limit=1`);
const existingUser = existing.data?.[0];

if (process.env.DELETE === '1') {
  if (!existingUser) {
    console.log(`No user with email ${EMAIL} found.`);
    process.exit(0);
  }
  await api(`/users/${existingUser.id}`, { method: 'DELETE' });
  console.log(`Deleted user ${EMAIL} (${existingUser.id}).`);
  process.exit(0);
}

if (existingUser) {
  console.log(`User ${EMAIL} already exists (${existingUser.id}). Rotating password.`);
  await api(`/users/${existingUser.id}`, {
    method: 'PATCH',
    body: JSON.stringify({ password: PASSWORD, tfa_secret: null, status: 'active' }),
  });
  console.log(`EMAIL=${EMAIL}`);
  console.log(`PASSWORD=${PASSWORD}`);
  process.exit(0);
}

const created = await api('/users', {
  method: 'POST',
  body: JSON.stringify({
    email: EMAIL,
    password: PASSWORD,
    role: role.id,
    status: 'active',
    first_name: 'Verify',
    last_name: 'Bot',
  }),
});
console.log(`Created user ${EMAIL} (${created.data.id}).`);
console.log(`EMAIL=${EMAIL}`);
console.log(`PASSWORD=${PASSWORD}`);
