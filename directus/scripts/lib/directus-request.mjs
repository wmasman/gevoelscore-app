// Shared Directus REST API helper.
// Auth via static token from `DIRECTUS_TOKEN` env var.
// URL via `DIRECTUS_URL` env var (defaults to the gevoelscore backend on Fly).

export const URL =
  process.env.DIRECTUS_URL || 'https://gevoelscore-backend.fly.dev';
export const TOKEN = process.env.DIRECTUS_TOKEN;

if (!TOKEN) {
  console.error('\n❌ DIRECTUS_TOKEN env var is not set.');
  console.error(
    '   Get a static token from /admin → User Profile → Token → Generate, then:',
  );
  console.error('   $env:DIRECTUS_TOKEN = "your-token-here"   (PowerShell)');
  console.error('   export DIRECTUS_TOKEN=your-token-here     (bash)\n');
  process.exit(1);
}

export async function directusRequest(endpoint, method = 'GET', body = null) {
  const options = {
    method,
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      'Content-Type': 'application/json',
    },
  };
  if (body !== null) options.body = JSON.stringify(body);

  const res = await fetch(`${URL}${endpoint}`, options);

  if (!res.ok) {
    const errorBody = await res.text();
    throw new Error(
      `HTTP ${res.status} on ${method} ${endpoint}\n${errorBody}`,
    );
  }

  if (res.status === 204 || method === 'DELETE') return { success: true };
  return res.json();
}

/**
 * Returns true if a Directus user-collection with the given name exists.
 * Note: this checks /collections/{name} which returns 403 for non-existent
 * collections in some Directus versions; we treat 403/404 the same.
 */
export async function collectionExists(name) {
  try {
    await directusRequest(`/collections/${name}`);
    return true;
  } catch (e) {
    const msg = String(e.message);
    if (msg.includes('404') || msg.includes('FORBIDDEN')) return false;
    throw e;
  }
}

/**
 * Returns the field metadata (Directus + actual PostgreSQL type) for a given
 * collection.field. Used by verify-schema.mjs to confirm the one-POST rule
 * produced the right PostgreSQL type.
 */
export async function getField(collection, field) {
  const res = await directusRequest(`/fields/${collection}/${field}`);
  return res.data;
}

/**
 * Banner so you know which env you're hitting before damage happens.
 */
export function banner(scriptName) {
  console.log('\n' + '='.repeat(64));
  console.log(`  ${scriptName}`);
  console.log(`  Target: ${URL}`);
  console.log('='.repeat(64) + '\n');
}
