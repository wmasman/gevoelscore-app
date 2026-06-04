// Read directly from the directus_sessions collection (or whatever
// session-store collection the app uses per ADR 0005) to see what
// active sessions exist. Read-only; logs counts + ID prefixes only.

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('probe-sessions');

// Try a few candidate collection names. ADR 0005 introduced session
// persistence in Directus; the actual collection name lives in
// directus-session-store.ts.
const candidates = ['frontend_sessions'];

for (const c of candidates) {
  try {
    const res = await directusRequest(`/items/${c}?limit=50`);
    const items = res?.data ?? res;
    if (Array.isArray(items)) {
      console.log(`\n  ${c}: ${items.length} row(s)`);
      for (const row of items) {
        const id = row.id ?? '(no id)';
        const prefix = String(id).slice(0, 10);
        const exp = row.expires_at ?? 'no-expiry';
        console.log(`    ${prefix}... user=${row.user_id ?? '?'} exp=${exp}`);
      }
    } else {
      console.log(`  ${c}: non-array response`);
    }
  } catch (e) {
    const msg = String(e.message ?? e).slice(0, 200);
    console.log(`  ${c}: ${msg}`);
  }
}
