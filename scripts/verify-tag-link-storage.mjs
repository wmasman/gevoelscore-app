// Step-5 backend-storage verification.
//
// Round-trips POST /api/tags + PATCH /api/tags/[id] through the deployed
// frontend, then reads the row DIRECTLY from Directus via the admin
// token to confirm the persisted state matches the API's response. This
// closes the loop the smoke leaves implicit (the smoke trusts the
// frontend's response body; this script verifies the row in the DB).
//
// Stages:
//   1) login
//   2) POST /api/episodes — create a smoke episode
//   3) POST /api/tags { ..., parent_episode_id: episodeId } — link in one shot
//   4) GET Directus /items/tags/[id] — confirm parent_episode_id is set
//   5) PATCH /api/tags/[id] { parent_episode_id: null } — unlink
//   6) GET Directus — confirm parent_episode_id is null
//   7) PATCH /api/tags/[id] { parent_episode_id: episodeId } — re-link
//   8) GET Directus — confirm parent_episode_id is back
//   9) Hard-DELETE the smoke tag + smoke episode (FK order)
//  10) logout
//
// Credentials read from .env.local (gitignored). Wrap in PowerShell:
//   powershell -ExecutionPolicy Bypass -File scripts/run-verify-tag-link-storage.ps1

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
let episodeId = null;
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

async function cleanup() {
  if (tagId) {
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
  if (episodeId) {
    try {
      const res = await fetch(`${DIRECTUS_BASE}/items/episodes/${episodeId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${ADMIN_TOKEN}` },
      });
      console.log(`  cleanup: episode hard-DELETE status=${res.status}`);
    } catch (e) {
      console.log(`  cleanup: episode hard-DELETE threw ${e instanceof Error ? e.message : String(e)}`);
    }
  }
}

console.log(`Tag-link storage verify → ${BASE}`);
console.log(`Directus               → ${DIRECTUS_BASE}`);
console.log(`User                   → ${EMAIL}`);
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

  // 2) Create episode
  const today = new Date().toISOString().slice(0, 10);
  const createEpRes = await fetch(`${BASE}/api/episodes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Origin: origin, Cookie: cookieJar },
    body: JSON.stringify({
      label: '_storage-verify ep',
      category: 'interventie',
      start_date: today,
    }),
  });
  const createEpBody = await createEpRes.json().catch(() => ({}));
  episodeId = createEpBody.episode?.id;
  step('create episode', createEpRes.status === 200 && !!episodeId, `id=${episodeId}`);

  if (!episodeId) {
    console.log('  ! No episode id — aborting.');
    process.exit(1);
  }

  // 3) Create tag with parent_episode_id in one round-trip
  const createTagRes = await fetch(`${BASE}/api/tags`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Origin: origin, Cookie: cookieJar },
    body: JSON.stringify({
      label: '_storage-verify tag',
      category: 'interventie',
      parent_episode_id: episodeId,
    }),
  });
  const createTagBody = await createTagRes.json().catch(() => ({}));
  tagId = createTagBody.tag?.id;
  step(
    'POST /api/tags returns 200 + tag with parent_episode_id set',
    createTagRes.status === 200 &&
      !!tagId &&
      createTagBody.tag?.parent_episode_id === episodeId,
    `id=${tagId}`,
  );

  // 4) Read DIRECTLY from Directus — the row must have parent_episode_id set
  const row1 = await readTagFromDirectus(tagId);
  step(
    'Directus row has parent_episode_id = episodeId after create-with-parent',
    row1 !== null && row1.parent_episode_id === episodeId,
    `Directus parent_episode_id=${row1?.parent_episode_id}`,
  );
  step(
    'Directus row label + category match the input (no field corruption)',
    row1?.label === '_storage-verify tag' && row1?.category === 'interventie',
    `label=${row1?.label} category=${row1?.category}`,
  );

  // 5) PATCH unlink
  const unlinkRes = await fetch(`${BASE}/api/tags/${tagId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', Origin: origin, Cookie: cookieJar },
    body: JSON.stringify({ parent_episode_id: null }),
  });
  step('PATCH unlink returns 200', unlinkRes.status === 200, `status=${unlinkRes.status}`);

  // 6) Read DIRECTLY — parent_episode_id must be null
  const row2 = await readTagFromDirectus(tagId);
  step(
    'Directus row has parent_episode_id = null after unlink',
    row2 !== null && row2.parent_episode_id === null,
    `Directus parent_episode_id=${row2?.parent_episode_id}`,
  );

  // 7) PATCH re-link
  const relinkRes = await fetch(`${BASE}/api/tags/${tagId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', Origin: origin, Cookie: cookieJar },
    body: JSON.stringify({ parent_episode_id: episodeId }),
  });
  step('PATCH re-link returns 200', relinkRes.status === 200, `status=${relinkRes.status}`);

  // 8) Read DIRECTLY — parent_episode_id must be set again
  const row3 = await readTagFromDirectus(tagId);
  step(
    'Directus row has parent_episode_id = episodeId after re-link',
    row3 !== null && row3.parent_episode_id === episodeId,
    `Directus parent_episode_id=${row3?.parent_episode_id}`,
  );

  // 9) Sanity: a PATCH that tries to set an unknown key must NOT mutate the row
  const badPatchRes = await fetch(`${BASE}/api/tags/${tagId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', Origin: origin, Cookie: cookieJar },
    body: JSON.stringify({ label: 'sneaky', parent_episode_id: episodeId }),
  });
  step(
    'PATCH with unknown key rejected with 400 (no silent mutation)',
    badPatchRes.status === 400,
    `status=${badPatchRes.status}`,
  );
  const row4 = await readTagFromDirectus(tagId);
  step(
    'Directus row label unchanged after rejected patch',
    row4?.label === '_storage-verify tag',
    `label=${row4?.label}`,
  );
} finally {
  await cleanup();
  if (cookieJar) {
    const logoutRes = await fetch(`${BASE}/api/auth/logout`, {
      method: 'POST',
      headers: { Origin: origin, Cookie: cookieJar },
    });
    step('logout', logoutRes.status === 200, `status=${logoutRes.status}`);
  }
}

console.log('');
if (allPassed) {
  console.log('✓ STORAGE VERIFY PASS — Directus rows match the API contract.');
  process.exit(0);
} else {
  console.log('✗ STORAGE VERIFY FAIL — see above.');
  process.exit(1);
}
