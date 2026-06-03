// Direct-PostgreSQL migration helper. Used for primitives Directus' REST
// API doesn't expose: partial unique indexes, composite unique constraints,
// CHECK constraints, anything PG-specific.
//
// Dependencies are injected so tests can supply a fake Client class +
// connection string without hitting a real database.
//
// Production wiring uses the `pg` npm package (devDep) and reads
// DATABASE_URL from the environment (sourced from .env.local via the
// existing run-directus-script.ps1 wrapper or a sibling).

import { readFile } from 'node:fs/promises';

const MISSING_URL_MESSAGE =
  'DATABASE_URL is not set. Get it from `fly secrets list -a gevoelscore-backend` and add to .env.local.';

async function resolveClientCtor(opts) {
  if (opts.Client) return opts.Client;
  const pg = await import('pg');
  return pg.default?.Client ?? pg.Client;
}

async function withClient(opts, fn) {
  const databaseUrl = opts.databaseUrl ?? process.env.DATABASE_URL;
  if (!databaseUrl) throw new Error(MISSING_URL_MESSAGE);
  const Client = await resolveClientCtor(opts);
  const client = new Client({ connectionString: databaseUrl });
  await client.connect();
  try {
    return await fn(client);
  } finally {
    await client.end();
  }
}

export async function runSqlFile(filePath, opts = {}) {
  // Fail BEFORE reading the file so missing-URL surfaces fast.
  const databaseUrl = opts.databaseUrl ?? process.env.DATABASE_URL;
  if (!databaseUrl) throw new Error(MISSING_URL_MESSAGE);

  const sql = await readFile(filePath, 'utf8');
  await withClient(opts, async (client) => {
    try {
      await client.query(sql);
    } catch (e) {
      const reason = e instanceof Error ? e.message : String(e);
      throw new Error(`SQL migration failed (${filePath}): ${reason}`);
    }
  });
}

export async function queryPg(sql, opts = {}) {
  return withClient(opts, async (client) => {
    const result = await client.query(sql);
    return result.rows;
  });
}

// re-exported for tests that want to assert the specific error message
export { MISSING_URL_MESSAGE };

// re-exported for downstream callers
export { withClient };
