// Adds a `user_created` column to day_entries, tags, and day_entries_tags
// (S-H3 prep, audit 2026-05-30).
//
// What this is:
//   The single-user gate (src/lib/auth/single-user-gate.ts) is the
//   RUNTIME enforcement of "one user only" until v1.5. This migration
//   adds the SCHEMA scaffolding so v1.5 multi-user can land without a
//   second migration cycle:
//
//   - `user_created` with `special: ['user-created']` — Directus
//     auto-fills it on CREATE from the requesting user's JWT. App
//     code does NOT need to set it explicitly.
//
// What this script does NOT do:
//   - Backfill existing rows. Rows created before today have
//     user_created = NULL. For a single-user app this is harmless —
//     all those rows belong to the same user implicitly. A v1.5
//     migration will backfill them via a single UPDATE.
//   - Enforce filtering. The app continues to read ALL rows by date
//     (no `filter[user_created][_eq]=$CURRENT_USER`). That's the
//     v1.5 work that pairs with this prep.
//   - Touch frontend_sessions. The frontend Fly machine writes
//     frontend_sessions with a SCOPED service token, so
//     user_created would always be the service user — useless for
//     per-app-user isolation. v1.5 will add a custom column on
//     frontend_sessions populated explicitly from the access token.
//
// Idempotent: re-running is a no-op (checks for existing fields).

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('add-user-created-columns');

const TARGETS = ['day_entries', 'tags', 'day_entries_tags'];

for (const collection of TARGETS) {
  // Probe whether the field exists. /fields/{collection}/{field}
  // returns 404 if absent — OR 403 (some Directus versions wrap
  // missing fields as FORBIDDEN to avoid leaking schema layout).
  // Treat both as "absent" — same pattern used by collectionExists.
  let exists = false;
  try {
    await directusRequest(`/fields/${collection}/user_created`);
    exists = true;
  } catch (e) {
    const msg = String(e.message);
    if (!msg.includes('404') && !msg.includes('FORBIDDEN')) throw e;
  }

  if (exists) {
    console.log(`  ⏩ ${collection}.user_created already exists`);
    continue;
  }

  console.log(`  ➕ adding ${collection}.user_created...`);
  await directusRequest(`/fields/${collection}`, 'POST', {
    field: 'user_created',
    type: 'uuid',
    schema: {
      is_nullable: true,
      // Foreign key to directus_users handled by Directus when
      // the `user-created` special is set.
    },
    meta: {
      special: ['user-created'],
      interface: 'select-dropdown-m2o',
      display: 'user',
      readonly: true,
      hidden: false,
      width: 'half',
      note: 'Auto-filled by Directus from the requesting token. v1.5 multi-user will filter by this.',
    },
  });
  console.log(`  ✅ ${collection}.user_created`);
}

console.log('\n✅ user_created columns added on:');
TARGETS.forEach((t) => console.log(`  - ${t}`));
console.log(
  '\nNote: app code does NOT filter by user_created yet — that ships with v1.5 multi-user. The runtime single-user gate (passesSingleUserGate) is the present enforcement.',
);
