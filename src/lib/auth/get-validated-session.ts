// Session lookup with transparent refresh-token rotation.
//
// Replaces the bare `sessionStore.get(id)` call in route handlers. If the
// access token is still alive, behaves identically (one map lookup). If it's
// expired, fires a Directus refresh, swaps in the new tokens, and returns
// the live session. If refresh also fails, the session is evicted and null
// is returned (caller should respond with 401 and clear the cookie).
//
// The session id never changes — only the underlying token pair rotates —
// so no new Set-Cookie is needed on refresh. The cookie itself lasts as
// long as SESSION_MAX_AGE_S (currently 30 days).

import { directusRefresh } from './directus-auth';
import { sessionStore } from './stores';
import type { SessionData, SessionStore } from './session';

// Injectable for tests. Defaults to the module-singleton stores + the real
// directus-auth wrapper. Production code never passes these explicitly.
type Deps = {
  store?: Pick<SessionStore, 'peek' | 'update' | 'delete'>;
  refresh?: typeof directusRefresh;
  now?: () => number;
};

export async function getValidatedSession(
  sessionId: string,
  deps: Deps = {},
): Promise<SessionData | null> {
  const store = deps.store ?? sessionStore;
  const refresh = deps.refresh ?? directusRefresh;
  const now = deps.now ?? Date.now;

  const session = store.peek(sessionId);
  if (!session) return null;

  if (session.expiresAt > now()) return session;

  // Access token expired — attempt refresh.
  const result = await refresh(session.refreshToken);
  if (!result.ok) {
    store.delete(sessionId);
    return null;
  }

  const refreshed: SessionData = {
    accessToken: result.value.accessToken,
    refreshToken: result.value.refreshToken,
    expiresAt: now() + result.value.expiresInMs,
  };
  store.update(sessionId, refreshed);
  return refreshed;
}
