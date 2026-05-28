// Directus-backed implementation of SessionStore.
//
// Why this exists: the default in-memory store loses every session on a
// Fly machine restart (deploy, OOM, host migration). Users then hold a
// cookie that resolves to nothing server-side. Pre-2026-05-28 the page
// silently rendered empty data; now it redirects to /login — but that
// still forces a re-login on every deploy. Persisting sessions in
// Directus fixes the root cause: the cookie keeps working as long as the
// underlying refresh token is alive.
//
// Authentication: uses the admin static token from `DIRECTUS_TOKEN` to
// talk to the `frontend_sessions` collection. We need a token that works
// BEFORE the user has authenticated, which rules out using their JWT.
// Storing an admin token on the frontend machine is a real exposure
// surface — minimize it later by issuing a dedicated service token
// scoped to just `frontend_sessions`. Tracked as a follow-up.
//
// Schema lives in directus/scripts/setup-frontend-sessions.mjs. The row
// shape is { id, access_token, refresh_token, expires_at, created_at }.

import {
  createDirectus,
  createItem,
  deleteItem,
  readItem,
  readItems,
  rest,
  staticToken,
  updateItem,
} from '@directus/sdk';
import type { SessionData, SessionStore, SessionStoreConfig } from './session';

type FrontendSessionRow = {
  id: string;
  access_token: string;
  refresh_token: string;
  expires_at: string;
  created_at?: string | null;
};

type Schema = { frontend_sessions: FrontendSessionRow[] };

export type DirectusSessionStoreConfig = SessionStoreConfig & {
  directusUrl: string;
  adminToken: string;
};

// Directus returns RECORD_NOT_FOUND for an unknown id, or FORBIDDEN if the
// policy hides existence. Both map to "absent" from the store's contract.
function isNotFound(e: unknown): boolean {
  if (typeof e !== 'object' || e === null) return false;
  const errors = (e as { errors?: unknown }).errors;
  if (!Array.isArray(errors) || errors.length === 0) return false;
  const code = (errors[0] as { extensions?: { code?: string } })?.extensions?.code;
  return code === 'RECORD_NOT_FOUND' || code === 'FORBIDDEN';
}

function rowToSession(row: FrontendSessionRow): SessionData {
  return {
    accessToken: row.access_token,
    refreshToken: row.refresh_token,
    expiresAt: Date.parse(row.expires_at),
  };
}

export function createDirectusSessionStore(
  config: DirectusSessionStoreConfig,
): SessionStore {
  const now = config.now ?? Date.now;
  const idGenerator = config.idGenerator ?? (() => crypto.randomUUID());
  const client = createDirectus<Schema>(config.directusUrl)
    .with(rest())
    .with(staticToken(config.adminToken));

  return {
    async create(data) {
      const id = idGenerator();
      await client.request(
        createItem('frontend_sessions', {
          id,
          access_token: data.accessToken,
          refresh_token: data.refreshToken,
          expires_at: new Date(data.expiresAt).toISOString(),
        }),
      );
      return id;
    },

    async get(id) {
      try {
        const row = (await client.request(
          readItem('frontend_sessions', id),
        )) as FrontendSessionRow;
        if (Date.parse(row.expires_at) <= now()) {
          // Expired. Evict and report absent — same contract as the in-mem store.
          await client.request(deleteItem('frontend_sessions', id)).catch(() => {});
          return undefined;
        }
        return rowToSession(row);
      } catch (e) {
        if (isNotFound(e)) return undefined;
        throw e;
      }
    },

    async peek(id) {
      try {
        const row = (await client.request(
          readItem('frontend_sessions', id),
        )) as FrontendSessionRow;
        return rowToSession(row);
      } catch (e) {
        if (isNotFound(e)) return undefined;
        throw e;
      }
    },

    async update(id, data) {
      try {
        await client.request(
          updateItem('frontend_sessions', id, {
            access_token: data.accessToken,
            refresh_token: data.refreshToken,
            expires_at: new Date(data.expiresAt).toISOString(),
          }),
        );
        return true;
      } catch (e) {
        if (isNotFound(e)) return false;
        throw e;
      }
    },

    async delete(id) {
      try {
        await client.request(deleteItem('frontend_sessions', id));
      } catch (e) {
        if (isNotFound(e)) return;
        throw e;
      }
    },

    async cleanupExpired() {
      const cutoff = new Date(now()).toISOString();
      const expired = (await client.request(
        readItems('frontend_sessions', {
          filter: { expires_at: { _lte: cutoff } } as never,
          fields: ['id'],
          limit: -1,
        }),
      )) as Array<{ id: string }>;
      for (const row of expired) {
        await client.request(deleteItem('frontend_sessions', row.id)).catch(() => {});
      }
    },

    async size() {
      const rows = (await client.request(
        readItems('frontend_sessions', { fields: ['id'], limit: -1 }),
      )) as Array<{ id: string }>;
      return rows.length;
    },
  };
}
