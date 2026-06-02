// Episodes smoke against the deployed frontend. Closed-loop integration
// check covering the full CRUD round-trip:
//   1) login
//   2) POST /api/episodes — create
//   3) GET  /api/episodes — assert created episode is in the list
//   4) PATCH /api/episodes/[id] — update description
//   5) PATCH archive (archived_at = now)
//   6) GET — assert archived episode NOT in default list
//   7) GET ?archived=all — assert archived episode IS in list
//   8) PATCH un-archive (archived_at = null)
//   8a) Step-5: POST /api/tags with parent_episode_id (one round-trip
//       inline create + link)
//   8b) Step-5: PATCH /api/tags/[id] unlink
//   8c) Step-5: PATCH /api/tags/[id] re-link
//   8d) Step-5: PATCH /api/tags non-UUID id → 400 invalid_id
//   9) PATCH /api/episodes garbage [id] → 400 invalid_request
//  10) hard-DELETE via admin DIRECTUS_TOKEN — cleanup the test rows
//      (tag first, then episode, to honour the parent_episode_id FK)
//  11) logout
//
// Why hard-DELETE for cleanup: the frontend API does NOT expose a DELETE
// endpoint (per the verloop-and-episodes README — hard delete is admin
// only). The smoke uses the admin Directus token directly to clean up,
// keeping Willem's real data uncluttered.
//
// Credentials read from .env.local (gitignored):
//   WILLEM_EMAIL, WILLEM_PASSWORD — frontend login
//   DIRECTUS_TOKEN              — admin token, for the hard-DELETE cleanup
//
// Run via the PowerShell wrapper that sources .env.local:
//   powershell -ExecutionPolicy Bypass -File scripts/run-episodes-smoke.ps1

import process from 'node:process';

const BASE = process.env.BASE_URL || 'https://gevoelscore-frontend.fly.dev';
const DIRECTUS_BASE = process.env.DIRECTUS_URL || 'https://gevoelscore-backend.fly.dev';
const EMAIL = process.env.WILLEM_EMAIL;
const PASSWORD = process.env.WILLEM_PASSWORD;
const ADMIN_TOKEN = process.env.DIRECTUS_TOKEN;

if (!EMAIL || !PASSWORD) {
  console.error('Missing WILLEM_EMAIL or WILLEM_PASSWORD env var.');
  console.error('Add to .env.local then run scripts/run-episodes-smoke.ps1.');
  process.exit(2);
}
if (!ADMIN_TOKEN) {
  console.error('Missing DIRECTUS_TOKEN env var (needed for cleanup hard-DELETE).');
  console.error('Add to .env.local then run scripts/run-episodes-smoke.ps1.');
  process.exit(2);
}

const origin = BASE;
let cookieJar = '';
let allPassed = true;
let episodeId = null;
let smokeTagId = null;

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

async function cleanupIfNeeded() {
  // Step-5 added a smoke tag — clean that up first (FK to episode means
  // deleting the episode while a smoke tag still references it would
  // fail, depending on Directus's ON DELETE behaviour. Tag first is safe).
  if (smokeTagId) {
    try {
      const res = await fetch(`${DIRECTUS_BASE}/items/tags/${smokeTagId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${ADMIN_TOKEN}` },
      });
      if (res.ok) {
        console.log(`\n  cleanup: hard-DELETE tag ${smokeTagId} → 204`);
      } else {
        console.log(`\n  cleanup: tag hard-DELETE returned status ${res.status} — manual cleanup may be needed`);
      }
    } catch (e) {
      console.log(`\n  cleanup: tag hard-DELETE threw ${e instanceof Error ? e.message : String(e)} — manual cleanup may be needed`);
    }
  }
  if (!episodeId) return;
  try {
    const res = await fetch(`${DIRECTUS_BASE}/items/episodes/${episodeId}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${ADMIN_TOKEN}` },
    });
    if (res.ok) {
      console.log(`\n  cleanup: hard-DELETE episode ${episodeId} → 204`);
    } else {
      console.log(`\n  cleanup: hard-DELETE returned status ${res.status} — manual cleanup may be needed`);
    }
  } catch (e) {
    console.log(`\n  cleanup: hard-DELETE threw ${e instanceof Error ? e.message : String(e)} — manual cleanup may be needed`);
  }
}

console.log(`Episodes smoke → ${BASE}`);
console.log(`User           → ${EMAIL}`);
console.log('');

try {
  // ---------------------------------------------------------------------
  // 1) Login
  // ---------------------------------------------------------------------
  const loginRes = await fetch(`${BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Origin: origin },
    body: JSON.stringify({ email: EMAIL, password: PASSWORD }),
  });
  const loginBody = await loginRes.json().catch(() => ({}));

  if (loginBody.requires_otp === true) {
    console.log('  ! Login returned requires_otp:true — 2FA is on for this account.');
    console.log('    This smoke does not handle OTP. Disable 2FA for the smoke user OR extend this script.');
    process.exit(3);
  }

  step(
    'POST /api/auth/login',
    loginRes.status === 200 && loginBody.ok === true,
    `status=${loginRes.status}`,
  );
  cookieJar = extractSessionCookie(loginRes);
  step('Set-Cookie gs_session is non-empty', cookieJar.length > 12);

  // ---------------------------------------------------------------------
  // 2) POST /api/episodes — create a smoke episode
  // ---------------------------------------------------------------------
  const today = new Date().toISOString().slice(0, 10);
  const SMOKE_LABEL = '_smoke episode (delete me)';

  const createRes = await fetch(`${BASE}/api/episodes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Origin: origin,
      Cookie: cookieJar,
    },
    body: JSON.stringify({
      label: SMOKE_LABEL,
      category: 'interventie',
      start_date: today,
    }),
  });
  const createBody = await createRes.json().catch(() => ({}));
  step(
    'POST /api/episodes returns 200 with { episode }',
    createRes.status === 200 && !!createBody.episode?.id,
    `status=${createRes.status}`,
  );
  episodeId = createBody.episode?.id;
  step(
    'created episode has expected label + category',
    createBody.episode?.label === SMOKE_LABEL &&
      createBody.episode?.category === 'interventie',
  );

  if (!episodeId) {
    console.log('\n  ! No episode id — aborting remaining checks.');
    process.exit(allPassed ? 0 : 1);
  }

  // ---------------------------------------------------------------------
  // 3) GET /api/episodes — assert the new episode is in the active list
  // ---------------------------------------------------------------------
  const listActiveRes = await fetch(`${BASE}/api/episodes`, {
    headers: { Origin: origin, Cookie: cookieJar },
  });
  const listActiveBody = await listActiveRes.json().catch(() => ({}));
  step(
    'GET /api/episodes returns 200',
    listActiveRes.status === 200 && Array.isArray(listActiveBody.episodes),
    `status=${listActiveRes.status}`,
  );
  step(
    'created episode appears in the active list',
    listActiveBody.episodes?.some((e) => e.id === episodeId),
  );

  // ---------------------------------------------------------------------
  // 4) PATCH — update description
  // ---------------------------------------------------------------------
  const patchDescRes = await fetch(`${BASE}/api/episodes/${episodeId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Origin: origin,
      Cookie: cookieJar,
    },
    body: JSON.stringify({ description: '_smoke description' }),
  });
  const patchDescBody = await patchDescRes.json().catch(() => ({}));
  step(
    'PATCH description returns 200',
    patchDescRes.status === 200 && patchDescBody.episode?.description === '_smoke description',
    `status=${patchDescRes.status}`,
  );

  // ---------------------------------------------------------------------
  // 5) PATCH archive (archived_at = now)
  // ---------------------------------------------------------------------
  const archiveIso = new Date().toISOString();
  const archiveRes = await fetch(`${BASE}/api/episodes/${episodeId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Origin: origin,
      Cookie: cookieJar,
    },
    body: JSON.stringify({ archived_at: archiveIso }),
  });
  const archiveBody = await archiveRes.json().catch(() => ({}));
  step(
    'PATCH archive returns 200 with archived_at set',
    archiveRes.status === 200 && !!archiveBody.episode?.archived_at,
    `status=${archiveRes.status}`,
  );

  // ---------------------------------------------------------------------
  // 6) GET active list — archived episode should NOT be in it
  // ---------------------------------------------------------------------
  const listAfterArchiveRes = await fetch(`${BASE}/api/episodes`, {
    headers: { Origin: origin, Cookie: cookieJar },
  });
  const listAfterArchiveBody = await listAfterArchiveRes.json().catch(() => ({}));
  step(
    'archived episode is NOT in the default list',
    !listAfterArchiveBody.episodes?.some((e) => e.id === episodeId),
  );

  // ---------------------------------------------------------------------
  // 7) GET ?archived=all — archived episode IS in the list
  // ---------------------------------------------------------------------
  const listAllRes = await fetch(`${BASE}/api/episodes?archived=all`, {
    headers: { Origin: origin, Cookie: cookieJar },
  });
  const listAllBody = await listAllRes.json().catch(() => ({}));
  step(
    'archived episode IS in the ?archived=all list',
    listAllBody.episodes?.some((e) => e.id === episodeId),
  );

  // ---------------------------------------------------------------------
  // 8) PATCH un-archive (archived_at = null)
  // ---------------------------------------------------------------------
  const unarchiveRes = await fetch(`${BASE}/api/episodes/${episodeId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Origin: origin,
      Cookie: cookieJar,
    },
    body: JSON.stringify({ archived_at: null }),
  });
  const unarchiveBody = await unarchiveRes.json().catch(() => ({}));
  step(
    'PATCH un-archive returns 200 with archived_at null',
    unarchiveRes.status === 200 && unarchiveBody.episode?.archived_at === null,
    `status=${unarchiveRes.status}`,
  );

  // ---------------------------------------------------------------------
  // Step-5: tag-to-episode linking round-trip
  //
  // 8a) POST /api/tags with { parent_episode_id } in one round-trip
  // 8b) PATCH /api/tags/[id] with parent set to null → unlinked
  // 8c) PATCH /api/tags/[id] with parent set back → re-linked
  // 8d) PATCH /api/tags/[id] with bad UUID id → 400 invalid_id
  // ---------------------------------------------------------------------
  const SMOKE_TAG_LABEL = '_smoke tag';
  const createTagRes = await fetch(`${BASE}/api/tags`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Origin: origin,
      Cookie: cookieJar,
    },
    body: JSON.stringify({
      label: SMOKE_TAG_LABEL,
      category: 'interventie',
      parent_episode_id: episodeId,
    }),
  });
  const createTagBody = await createTagRes.json().catch(() => ({}));
  step(
    'POST /api/tags with parent_episode_id returns 200 + linked tag',
    createTagRes.status === 200 &&
      !!createTagBody.tag?.id &&
      createTagBody.tag?.parent_episode_id === episodeId,
    `status=${createTagRes.status}`,
  );
  smokeTagId = createTagBody.tag?.id ?? null;

  if (smokeTagId) {
    const unlinkRes = await fetch(`${BASE}/api/tags/${smokeTagId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        Origin: origin,
        Cookie: cookieJar,
      },
      body: JSON.stringify({ parent_episode_id: null }),
    });
    const unlinkBody = await unlinkRes.json().catch(() => ({}));
    step(
      'PATCH /api/tags/[id] unlink returns 200 + null parent',
      unlinkRes.status === 200 && unlinkBody.tag?.parent_episode_id === null,
      `status=${unlinkRes.status}`,
    );

    const relinkRes = await fetch(`${BASE}/api/tags/${smokeTagId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        Origin: origin,
        Cookie: cookieJar,
      },
      body: JSON.stringify({ parent_episode_id: episodeId }),
    });
    const relinkBody = await relinkRes.json().catch(() => ({}));
    step(
      'PATCH /api/tags/[id] re-link returns 200 + parent set',
      relinkRes.status === 200 &&
        relinkBody.tag?.parent_episode_id === episodeId,
      `status=${relinkRes.status}`,
    );
  }

  const badTagIdRes = await fetch(`${BASE}/api/tags/not-a-uuid`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Origin: origin,
      Cookie: cookieJar,
    },
    body: JSON.stringify({ parent_episode_id: null }),
  });
  step(
    'PATCH /api/tags non-UUID id rejected with 400',
    badTagIdRes.status === 400,
    `status=${badTagIdRes.status}`,
  );

  // ---------------------------------------------------------------------
  // 9) PATCH garbage [id] → 400 invalid_request (defense-in-depth check)
  // ---------------------------------------------------------------------
  const badIdRes = await fetch(`${BASE}/api/episodes/not-a-uuid`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Origin: origin,
      Cookie: cookieJar,
    },
    body: JSON.stringify({ label: 'x' }),
  });
  step(
    'PATCH non-UUID id is rejected with 400',
    badIdRes.status === 400,
    `status=${badIdRes.status}`,
  );
} finally {
  // -----------------------------------------------------------------------
  // Cleanup: hard-DELETE the smoke episode via admin token.
  // The frontend API does not expose DELETE; this goes direct to Directus.
  // -----------------------------------------------------------------------
  await cleanupIfNeeded();

  // ---------------------------------------------------------------------
  // 10) Logout
  // ---------------------------------------------------------------------
  if (cookieJar) {
    const logoutRes = await fetch(`${BASE}/api/auth/logout`, {
      method: 'POST',
      headers: { Origin: origin, Cookie: cookieJar },
    });
    step(
      'POST /api/auth/logout returns 200',
      logoutRes.status === 200,
      `status=${logoutRes.status}`,
    );
  }
}

console.log('');
if (allPassed) {
  console.log('✓ EPISODES SMOKE PASS — CRUD round-trip clean.');
  process.exit(0);
} else {
  console.log('✗ EPISODES SMOKE FAIL — see above.');
  process.exit(1);
}
