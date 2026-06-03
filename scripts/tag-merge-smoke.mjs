// Tag-merge smoke against the deployed frontend (v1.5c step-1).
//
// Round-trip:
//   1) login (session cookie)
//   2) negative same_tag — POST merge with source===target → 400 same_tag
//      (lib short-circuits before any wire read; no seeds needed)
//   3) seed source + target + fake day_entry + junction via Directus admin
//   4) negative category_mismatch — create extra tag in another category;
//      POST merge → 400 category_mismatch; clean up extra
//   5) positive merge — POST merge with source + target → 200 with
//      affected_days === 1
//   6) Directus read-backs:
//      - source tag is gone (404)
//      - target tag's usage_count == 1
//      - no junction rows reference the source (CASCADE removed source-
//        side via the bulk PATCH path; the junction is now target-tagged)
//      - the junction on the fake day now points at target
//   7) cleanup — delete fake day_entry (CASCADE removes its junctions),
//      delete target tag
//
// Credentials read from .env.local (gitignored):
//   WILLEM_EMAIL, WILLEM_PASSWORD — frontend login
//   DIRECTUS_TOKEN               — admin token for seed + read-back +
//                                  cleanup
//
// Run via the PowerShell wrapper:
//   powershell -ExecutionPolicy Bypass -File scripts/run-tag-merge-smoke.ps1

import process from 'node:process';
import { randomUUID } from 'node:crypto';

const BASE = process.env.BASE_URL || 'https://gevoelscore-frontend.fly.dev';
const DIRECTUS_BASE =
  process.env.DIRECTUS_URL || 'https://gevoelscore-backend.fly.dev';
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

// Track seeded ids for cleanup-on-error.
let sourceTagId = null;
let targetTagId = null;
let fakeDayEntryId = null;
let extraCategoryTagId = null;

function step(label, ok, detail) {
  const mark = ok ? '✓' : '✗';
  console.log(`  ${mark} ${label}${detail ? `\n     ${detail}` : ''}`);
  if (!ok) allPassed = false;
}

function extractSessionCookie(res) {
  const headers = res.headers.getSetCookie?.() ?? [];
  for (const sc of headers) {
    const [pair] = sc.split(';');
    const [name, value] = pair.split('=');
    if (name?.trim() === 'gs_session') return `gs_session=${value ?? ''}`;
  }
  return '';
}

async function adminFetch(path, init = {}) {
  return fetch(`${DIRECTUS_BASE}${path}`, {
    ...init,
    headers: {
      ...(init.headers ?? {}),
      Authorization: `Bearer ${ADMIN_TOKEN}`,
      ...(init.body ? { 'Content-Type': 'application/json' } : {}),
    },
  });
}

async function adminCreate(collection, payload) {
  const res = await adminFetch(`/items/${collection}`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error(`admin POST ${collection} → ${res.status} ${await res.text()}`);
  }
  return (await res.json()).data;
}

async function adminRead(collection, id) {
  const res = await adminFetch(`/items/${collection}/${id}`);
  if (res.status === 404 || res.status === 403) return null;
  if (!res.ok) {
    throw new Error(`admin GET ${collection}/${id} → ${res.status} ${await res.text()}`);
  }
  return (await res.json()).data;
}

async function adminDelete(collection, id) {
  const res = await adminFetch(`/items/${collection}/${id}`, { method: 'DELETE' });
  return res.ok;
}

async function adminJunctionRowsForTag(tagId) {
  const res = await adminFetch(
    `/items/day_entries_tags?limit=-1&filter[tags_id][_eq]=${tagId}&fields=id,day_entries_id,tags_id`,
  );
  if (!res.ok) {
    throw new Error(`admin GET junctions for ${tagId} → ${res.status}`);
  }
  return (await res.json()).data ?? [];
}

async function cleanupSeeds() {
  console.log('\n  cleanup:');
  if (extraCategoryTagId) {
    const ok = await adminDelete('tags', extraCategoryTagId);
    console.log(`    extra-category tag ${extraCategoryTagId} delete: ${ok ? 'ok' : 'failed'}`);
  }
  // day_entry first — CASCADE removes any remaining junctions.
  if (fakeDayEntryId) {
    const ok = await adminDelete('day_entries', fakeDayEntryId);
    console.log(`    fake day_entry ${fakeDayEntryId} delete: ${ok ? 'ok' : 'failed'}`);
  }
  // target may still exist; source should be merge-deleted.
  if (targetTagId) {
    const ok = await adminDelete('tags', targetTagId);
    console.log(`    target tag ${targetTagId} delete: ${ok ? 'ok' : 'failed'}`);
  }
  if (sourceTagId) {
    const stillThere = await adminRead('tags', sourceTagId);
    if (stillThere) {
      const ok = await adminDelete('tags', sourceTagId);
      console.log(`    source tag ${sourceTagId} cleanup-delete: ${ok ? 'ok' : 'failed'}`);
    }
  }
}

async function main() {
  console.log(`\n  Target: ${BASE}`);

  // ---------------------------------------------------------------------
  // 1) Login
  // ---------------------------------------------------------------------
  const loginRes = await fetch(`${BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', origin },
    body: JSON.stringify({ email: EMAIL, password: PASSWORD }),
  });
  step('login', loginRes.status === 200, `status=${loginRes.status}`);
  if (loginRes.status !== 200) return;
  cookieJar = extractSessionCookie(loginRes);
  step('session cookie set', cookieJar.startsWith('gs_session='));

  // ---------------------------------------------------------------------
  // 2) Negative: same_tag (lib short-circuit; no DB seeds needed)
  // ---------------------------------------------------------------------
  const fakeId = randomUUID();
  const sameTagRes = await fetch(`${BASE}/api/tags/${fakeId}/merge`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', origin, cookie: cookieJar },
    body: JSON.stringify({ target_tag_id: fakeId }),
  });
  const sameTagBody = await sameTagRes.json();
  step(
    'negative: source===target → 400 same_tag',
    sameTagRes.status === 400 && sameTagBody.error === 'same_tag',
    `status=${sameTagRes.status} error=${sameTagBody.error}`,
  );

  // ---------------------------------------------------------------------
  // 3) Seed source + target + fake day_entry + junction
  // ---------------------------------------------------------------------
  const stamp = Math.floor(Date.now() / 1000);
  const sourceLabel = `_merge src ${stamp}`;
  const targetLabel = `_merge tgt ${stamp}`;

  const source = await adminCreate('tags', {
    label: sourceLabel,
    category: 'custom',
    usage_count: 0,
  });
  sourceTagId = source.id;

  const target = await adminCreate('tags', {
    label: targetLabel,
    category: 'custom',
    usage_count: 0,
  });
  targetTagId = target.id;

  const fakeDay = await adminCreate('day_entries', {
    date: '2099-12-31',
    score: 5,
  });
  fakeDayEntryId = fakeDay.id;

  await adminCreate('day_entries_tags', {
    day_entries_id: fakeDayEntryId,
    tags_id: sourceTagId,
    source: 'user',
    confidence: 1.0,
  });
  // Reflect the junction in the stored usage_count so the merge confirm
  // count + recount math have a non-trivial value to work with.
  await adminFetch(`/items/tags/${sourceTagId}`, {
    method: 'PATCH',
    body: JSON.stringify({ usage_count: 1 }),
  });
  step('seeded source + target + fake day_entry + junction', true);

  // ---------------------------------------------------------------------
  // 4) Negative: category_mismatch
  // ---------------------------------------------------------------------
  const extra = await adminCreate('tags', {
    label: `_merge mismatch ${stamp}`,
    category: 'mentaal',
    usage_count: 0,
  });
  extraCategoryTagId = extra.id;

  const mismatchRes = await fetch(`${BASE}/api/tags/${sourceTagId}/merge`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', origin, cookie: cookieJar },
    body: JSON.stringify({ target_tag_id: extraCategoryTagId }),
  });
  const mismatchBody = await mismatchRes.json();
  step(
    'negative: cross-category → 400 category_mismatch',
    mismatchRes.status === 400 && mismatchBody.error === 'category_mismatch',
    `status=${mismatchRes.status} error=${mismatchBody.error}`,
  );

  // Clean up the extra category tag immediately so it doesn't linger
  // through the positive case (and leave fewer things to forget at the
  // bottom).
  if (extraCategoryTagId) {
    await adminDelete('tags', extraCategoryTagId);
    extraCategoryTagId = null;
  }

  // ---------------------------------------------------------------------
  // 5) Positive merge
  // ---------------------------------------------------------------------
  const mergeRes = await fetch(`${BASE}/api/tags/${sourceTagId}/merge`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', origin, cookie: cookieJar },
    body: JSON.stringify({ target_tag_id: targetTagId }),
  });
  const mergeBody = await mergeRes.json();
  step(
    'positive: merge → 200 with affected_days === 1',
    mergeRes.status === 200 && mergeBody.affected_days === 1,
    `status=${mergeRes.status} body=${JSON.stringify(mergeBody)}`,
  );
  if (mergeRes.status === 200) {
    step(
      'response carries source_id + target_id',
      mergeBody.source_id === sourceTagId && mergeBody.target_id === targetTagId,
    );
  }

  // ---------------------------------------------------------------------
  // 6) Read-backs
  // ---------------------------------------------------------------------
  const sourceAfter = await adminRead('tags', sourceTagId);
  step('source tag is gone (admin 404)', sourceAfter === null);
  if (sourceAfter === null) sourceTagId = null; // skip cleanup for source

  const targetAfter = await adminRead('tags', targetTagId);
  step(
    'target tag exists with usage_count === 1',
    targetAfter !== null && targetAfter.usage_count === 1,
    `usage_count=${targetAfter?.usage_count}`,
  );

  const sourceJunctions = await adminJunctionRowsForTag(
    mergeBody.source_id ?? 'unknown',
  );
  step(
    'no junction rows reference the source',
    sourceJunctions.length === 0,
    `found=${sourceJunctions.length}`,
  );

  const targetJunctions = await adminJunctionRowsForTag(targetTagId);
  const targetOnFakeDay = targetJunctions.some(
    (j) => j.day_entries_id === fakeDayEntryId,
  );
  step(
    'target junction lands on the fake day (rewrite confirmed)',
    targetOnFakeDay,
  );
}

try {
  await main();
} catch (e) {
  console.error('\n  ✗ unexpected error:', e instanceof Error ? e.message : e);
  allPassed = false;
} finally {
  await cleanupSeeds();
}

console.log('\n' + '─'.repeat(64));
if (allPassed) {
  console.log('  ✅ All tag-merge smoke checks passed.');
} else {
  console.log('  ❌ Some smoke checks failed (see above).');
}
console.log('─'.repeat(64) + '\n');

process.exit(allPassed ? 0 : 1);
