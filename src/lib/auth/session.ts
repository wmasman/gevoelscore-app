// Server-side session store + cookie helpers for the login feature.
//
// The cookie carries only an opaque session id. The actual Directus tokens
// (access + refresh) live in a server-side Map keyed by that id. Browser JS
// never sees the access token.
//
// In-memory only. Single-process Fly machine (ADR 0003: min_machines_running = 1).
// If scaled later, swap the Map for Redis or a Directus collection — the
// public API (create / get / delete / cleanupExpired) stays.

export const SESSION_COOKIE_NAME = 'gs_session';

// Cookie Max-Age — single source of truth used by every route that emits the
// gs_session cookie. 30 days. The cookie holds an opaque session id; tokens
// underneath get rotated transparently via the refresh flow in
// get-validated-session.ts, so this Max-Age only governs the cookie itself,
// not the access-token lifetime.
export const SESSION_MAX_AGE_S = 30 * 24 * 60 * 60;

export type SessionData = {
  accessToken: string;
  refreshToken: string;
  expiresAt: number;
};

export type SessionStoreConfig = {
  now?: () => number;
  idGenerator?: () => string;
};

export type SessionStore = {
  create: (data: SessionData) => string;
  // Returns the session, evicting it if expired. Use when you want
  // "give me a valid session or nothing" without refresh.
  get: (id: string) => SessionData | undefined;
  // Returns the entry as-is, even if expired. No eviction. Use when the
  // caller wants to decide what to do about expiry (e.g. refresh-token
  // rotation in get-validated-session.ts).
  peek: (id: string) => SessionData | undefined;
  // Replaces the entry in place. Returns true on success, false if the id is
  // unknown (no new entry is created — use create() for that).
  update: (id: string, data: SessionData) => boolean;
  delete: (id: string) => void;
  cleanupExpired: () => void;
  size: () => number;
};

export function createSessionStore(config: SessionStoreConfig = {}): SessionStore {
  const now = config.now ?? Date.now;
  const idGenerator = config.idGenerator ?? (() => crypto.randomUUID());
  const sessions = new Map<string, SessionData>();

  return {
    create(data) {
      const id = idGenerator();
      sessions.set(id, data);
      return id;
    },

    get(id) {
      const session = sessions.get(id);
      if (!session) return undefined;
      if (session.expiresAt <= now()) {
        sessions.delete(id);
        return undefined;
      }
      return session;
    },

    peek(id) {
      return sessions.get(id);
    },

    update(id, data) {
      if (!sessions.has(id)) return false;
      sessions.set(id, data);
      return true;
    },

    delete(id) {
      sessions.delete(id);
    },

    cleanupExpired() {
      const t = now();
      for (const [id, session] of sessions) {
        if (session.expiresAt <= t) sessions.delete(id);
      }
    },

    size() {
      return sessions.size;
    },
  };
}

export function buildSessionCookie(sessionId: string | null, maxAgeSeconds: number): string {
  const value = sessionId ?? '';
  return [
    `${SESSION_COOKIE_NAME}=${value}`,
    'HttpOnly',
    'Secure',
    'SameSite=Strict',
    'Path=/',
    `Max-Age=${maxAgeSeconds}`,
  ].join('; ');
}

export function parseSessionCookie(header: string | null): string | null {
  if (!header) return null;

  const pairs = header.split(';');
  for (const raw of pairs) {
    const [name, ...rest] = raw.trim().split('=');
    if (name === SESSION_COOKIE_NAME) {
      const value = rest.join('=');
      return value.length > 0 ? value : null;
    }
  }
  return null;
}
