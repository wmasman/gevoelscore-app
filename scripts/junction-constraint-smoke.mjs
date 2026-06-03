// Step 0 / AC0.12 — production smoke. Drives the new UNIQUE indexes by
// attempting a constraint violation through the Directus REST API. Each
// violation MUST be rejected (400/422 + PG error code 23505 in body).
//
// Skips project_entries_tags (collection empty in v1).
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."     # admin static token
//   node scripts/junction-constraint-smoke.mjs

import { banner, directusRequest } from '../directus/scripts/lib/directus-request.mjs';

banner('junction-constraint-smoke');

let failures = 0;
function assert(cond, message) {
  if (cond) {
    console.log(`  ✅ ${message}`);
  } else {
    console.log(`  ❌ ${message}`);
    failures += 1;
  }
}

function isUniqueViolation(err) {
  // The directus-request helper throws `HTTP {status} on ... \n{body}`.
  // Both 23505 (raw PG) and Directus' "RECORD_NOT_UNIQUE" surface here.
  const text = err && err.message ? err.message : String(err);
  return /23505|RECORD_NOT_UNIQUE|unique constraint|already exists/i.test(text);
}

// ─────────────────────────────────────────────────────────────────────────
// 1) Junction-pair UNIQUE on day_entries_tags
// ─────────────────────────────────────────────────────────────────────────

console.log('\n  ── 1) Junction-pair UNIQUE (day_entries_tags) ──');

const junctionsResp = await directusRequest(
  '/items/day_entries_tags?limit=1&fields=id,day_entries_id,tags_id',
);
const existingJunction = junctionsResp?.data?.[0];

if (!existingJunction) {
  console.log('  ⏩ no existing junction rows; cannot smoke junction-pair UNIQUE');
} else {
  const dupBody = {
    day_entries_id: existingJunction.day_entries_id,
    tags_id: existingJunction.tags_id,
    source: 'user',
    confidence: 1.0,
  };
  let caught = null;
  try {
    await directusRequest('/items/day_entries_tags', 'POST', dupBody);
  } catch (e) {
    caught = e;
  }
  assert(
    caught !== null,
    'POST duplicate junction row rejected by Directus',
  );
  assert(
    caught !== null && isUniqueViolation(caught),
    'rejection signals a unique-constraint violation (23505 / RECORD_NOT_UNIQUE / unique constraint)',
  );
}

// ─────────────────────────────────────────────────────────────────────────
// 2) Tag-label partial UNIQUE on tags
// ─────────────────────────────────────────────────────────────────────────

console.log('\n  ── 2) Tag-label partial UNIQUE (tags) ──');

const SMOKE_LABEL = '_smoke dup ' + Math.floor(Date.now() / 1000);
const SMOKE_CATEGORY = 'custom';

let createdId = null;
try {
  const createResp = await directusRequest('/items/tags', 'POST', {
    label: SMOKE_LABEL,
    category: SMOKE_CATEGORY,
    usage_count: 0,
  });
  createdId = createResp?.data?.id;
  assert(createdId !== null && createdId !== undefined, `seeded first tag ${SMOKE_LABEL}`);

  let caught = null;
  try {
    await directusRequest('/items/tags', 'POST', {
      label: SMOKE_LABEL,
      category: SMOKE_CATEGORY,
      usage_count: 0,
    });
  } catch (e) {
    caught = e;
  }
  assert(
    caught !== null,
    'POST second tag with same (label, category) rejected by Directus',
  );
  assert(
    caught !== null && isUniqueViolation(caught),
    'rejection signals a unique-constraint violation',
  );

  // Case-insensitive check: same label uppercased should also be rejected.
  caught = null;
  try {
    await directusRequest('/items/tags', 'POST', {
      label: SMOKE_LABEL.toUpperCase(),
      category: SMOKE_CATEGORY,
      usage_count: 0,
    });
  } catch (e) {
    caught = e;
  }
  assert(
    caught !== null,
    'POST case-different label in same category also rejected (partial unique is case-insensitive via LOWER())',
  );
} finally {
  // Cleanup: hard-delete the seeded tag. CASCADE removes any incidental junction.
  if (createdId) {
    try {
      await directusRequest(`/items/tags/${createdId}`, 'DELETE');
      console.log(`  🧹 cleaned up seeded tag ${createdId}`);
    } catch (e) {
      console.log(`  ⚠️  cleanup failed (manual remove needed for tag ${createdId}): ${(e && e.message ? e.message : e).split('\n')[0]}`);
    }
  }
}

// ─────────────────────────────────────────────────────────────────────────
// Exit
// ─────────────────────────────────────────────────────────────────────────

console.log('\n' + '─'.repeat(64));
if (failures === 0) {
  console.log('  ✅ All constraint-enforcement smoke checks passed.');
} else {
  console.log(`  ❌ ${failures} smoke check(s) failed.`);
}
console.log('─'.repeat(64) + '\n');

if (failures > 0) process.exit(1);
