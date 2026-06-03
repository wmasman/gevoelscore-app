// Tag-management smoke against the deployed frontend.
//
// Round-trips the v1.5b additions: extended PATCH (label / category /
// archived_at / parent_episode_id) + new DELETE (gated by usage_count).
// Verifies via direct Directus reads that the persisted state matches
// each API response.
//
// Steps:
//   1) login
//   2) POST /api/tags — create smoke tag (usage_count = 0)
//   3) PATCH rename + Directus read-back
//   4) PATCH recategorize + Directus read-back
//   5) PATCH archive + Directus read-back
//   6) PATCH un-archive + Directus read-back
//   7) DELETE on usage_count === 0 → 200 + Directus row gone
//   8) Negative: DELETE on a non-existent UUID → 502 (M5 boundary check)
//   9) logout
//
// Note: the "DELETE blocked when usage_count > 0" case requires writing
// to day_entries (Willem's real data) to seed a referenced tag — too
// risky for a smoke. Covered by the route-handler unit test instead.
//
// Credentials read from .env.local (gitignored):
//   WILLEM_EMAIL, WILLEM_PASSWORD — frontend login
//   DIRECTUS_TOKEN              — admin token for direct reads + cleanup
//
// Run via the PowerShell wrapper that sources .env.local:
//   powershell -ExecutionPolicy Bypass -File scripts/run-tag-management-smoke.ps1

import process from 'node:process';

const BASE = process.env.BASE_URL || 'https://gevoelscore-frontend.fly.dev';
const DIRECTUS_BASE = process.env.DIRECTUS_URL || 'https://gevoelscore-backend.fly.dev';
const EMAIL = process.env.WILLEM_EMAIL;
const PASSWORD = process.env.WILLEM_PASSWORD;
const ADMIN_TOKEN = process.env.DIRECTUS_TOKEN;

if (!EMAIL || !PASSWORD || !ADMIN_TOKEN) {
  console.error('Missing WILLEM_EMAIL / WILLEM_PASSWORD / DIRECTUS_TOKEN in .env.local.');
  process.exit(2);
}

const origin = BASE;
let cookieJar = '';
let allPassed = true;
let tagId = null;

function extractSessionCookie(res) {
  const headers = res.headers.getSetCookie?.() ?? [];
  for (const sc of headers) {
    const [pair] = sc.split(';');
    const [name, value] = pair.split('=');
    if (name?.trim() === 'gs_session') return `gs_session=${value ?? ''}`;
  }
  return '';
}

function step(label, ok, detail) {
  const mark = ok ? '✓' : '✗';
  console.log(`  ${mark} ${label}${detail ? `\n     ${detail}` : ''}`);
  if (!ok) allPassed = false;
}

async function readTagFromDirectus(id) {
  const res = await fetch(`${DIRECTUS_BASE}/items/tags/${id}`, {
    headers: { Authorization: `Bearer ${ADMIN_TOKEN}` },
  });
  if (!res.ok) return null;
  const body = await res.json();
  return body.data ?? null;
}

async function cleanupIfNeeded() {
  if (!tagId) return;
  try {
    const res = await fetch(`${DIRECTUS_BASE}/items/tags/${tagId}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${ADMIN_TOKEN}` },
    });
    console.log(`\n  cleanup: tag hard-DELETE status=${res.status}`);
  } catch (e) {
    console.log(`\n  cleanup: tag hard-DELETE threw ${e instanceof Error ? e.message : String(e)}`);
  }
}

console.log(`Tag-management smoke → ${BASE}`);
console.log(`Directus            → ${DIRECTUS_BASE}`);
console.log(`User                → ${EMAIL}`);
console.log('');

try {
  // 1) Login
  const loginRes = await fetch(`${BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Origin: origin },
    body: JSON.stringify({ email: EMAIL, password: PASSWORD }),
  });
  const loginBody = await loginRes.json().catch(() => ({}));
  if (loginBody.requires_otp === true) {
    console.log('  ! 2FA required — disable for the smoke user or extend this script.');
    process.exit(3);
  }
  step('login', loginRes.status === 200 && loginBody.ok === true, `status=${loginRes.status}`);
  cookieJar = extractSessionCookie(loginRes);

  // 2) Create smoke tag (usage_count = 0)
  const SMOKE_LABEL = '_tag-mgmt smoke';
  const createRes = await fetch(`${BASE}/api/tags`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Origin: origin, Cookie: cookieJar },
    body: JSON.stringify({ label: SMOKE_LABEL, category: 'custom' }),
  });
  const createBody = await createRes.json().catch(() => ({}));
  tagId = createBody.tag?.id ?? null;
  step(
    'POST /api/tags creates a smoke tag',
    createRes.status === 200 && !!tagId && createBody.tag?.usage_count === 0,
    `id=${tagId}`,
  );

  if (!tagId) process.exit(1);

  // 3) PATCH rename
  const renameRes = await fetch(`${BASE}/api/tags/${tagId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', Origin: origin, Cookie: cookieJar },
    body: JSON.stringify({ label: '_tag-mgmt renamed' }),
  });
  step('PATCH rename returns 200', renameRes.status === 200);
  const row1 = await readTagFromDirectus(tagId);
  step(
    'Directus row reflects renamed label',
    row1?.label === '_tag-mgmt renamed',
    `label=${row1?.label}`,
  );

  // 4) PATCH recategorize
  const recatRes = await fetch(`${BASE}/api/tags/${tagId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', Origin: origin, Cookie: cookieJar },
    body: JSON.stringify({ category: 'mentaal' }),
  });
  step('PATCH recategorize returns 200', recatRes.status === 200);
  const row2 = await readTagFromDirectus(tagId);
  step(
    'Directus row reflects new category',
    row2?.category === 'mentaal',
    `category=${row2?.category}`,
  );

  // 5) PATCH archive
  const iso = new Date().toISOString();
  const archiveRes = await fetch(`${BASE}/api/tags/${tagId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', Origin: origin, Cookie: cookieJar },
    body: JSON.stringify({ archived_at: iso }),
  });
  step('PATCH archive returns 200', archiveRes.status === 200);
  const row3 = await readTagFromDirectus(tagId);
  step(
    'Directus row has archived_at set',
    row3?.archived_at !== null,
    `archived_at=${row3?.archived_at}`,
  );

  // 6) PATCH un-archive
  const unarchiveRes = await fetch(`${BASE}/api/tags/${tagId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', Origin: origin, Cookie: cookieJar },
    body: JSON.stringify({ archived_at: null }),
  });
  step('PATCH un-archive returns 200', unarchiveRes.status === 200);
  const row4 = await readTagFromDirectus(tagId);
  step(
    'Directus row has archived_at null',
    row4?.archived_at === null,
    `archived_at=${row4?.archived_at}`,
  );

  // 7) DELETE on usage_count === 0
  const deleteRes = await fetch(`${BASE}/api/tags/${tagId}`, {
    method: 'DELETE',
    headers: { Origin: origin, Cookie: cookieJar },
  });
  const deleteBody = await deleteRes.json().catch(() => ({}));
  step(
    'DELETE on usage_count===0 returns 200 with deleted_id',
    deleteRes.status === 200 && deleteBody.deleted_id === tagId,
    `status=${deleteRes.status}`,
  );
  const row5 = await readTagFromDirectus(tagId);
  step(
    'Directus row is gone after DELETE',
    row5 === null,
  );
  // Mark cleared so the finally block skips its own cleanup.
  if (row5 === null) tagId = null;

  // 8) DELETE on a non-existent UUID → 502 (M5 boundary check)
  const FAKE_UUID = '00000000-0000-0000-0000-000000000000';
  const deleteFakeRes = await fetch(`${BASE}/api/tags/${FAKE_UUID}`, {
    method: 'DELETE',
    headers: { Origin: origin, Cookie: cookieJar },
  });
  step(
    'DELETE on non-existent UUID returns 502 (M5)',
    deleteFakeRes.status === 502,
    `status=${deleteFakeRes.status}`,
  );
} finally {
  await cleanupIfNeeded();
  if (cookieJar) {
    const logoutRes = await fetch(`${BASE}/api/auth/logout`, {
      method: 'POST',
      headers: { Origin: origin, Cookie: cookieJar },
    });
    step('POST /api/auth/logout returns 200', logoutRes.status === 200);
  }
}

console.log('');
if (allPassed) {
  console.log('✓ TAG-MANAGEMENT SMOKE PASS — extended PATCH + DELETE round-trip clean.');
  process.exit(0);
} else {
  console.log('✗ TAG-MANAGEMENT SMOKE FAIL — see above.');
  process.exit(1);
}
