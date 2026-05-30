// Session lookup with transparent refresh-token rotation.
//
// Replaces the bare `sessionStore.get(id)` call in route handlers. If the
// access token is still alive, behaves identically (one map lookup). If it's
// expired, fires a Directus refresh, swaps in the new tokens, and returns
// the live session.
//
// Eviction policy — narrow on purpose. The store row is deleted ONLY when
// Directus reports the refresh token itself is invalid (terminal: user
// must log in again). Transient failures (network blip during a Directus
// deploy, unexpected Directus error code) return null for THIS request
// but leave the row in place so the next request retries. Previously
// every transient failure permanently destroyed the session, which is
// what "I keep getting logged out at random" felt like.
//
// Parallel-refresh coalescing — when an access token expires, concurrent
// requests for the same session would each call directusRefresh with the
// same refresh token. Directus consumes refresh tokens on use, so the
// second call lost the race and the session was deleted out from under
// both callers. The in-process `refreshLocks` map collapses concurrent
// refresh attempts for the same sessionId into a single Directus call;
// every waiter receives the same result. Map is per-Fly-machine; for
// the single-machine app this is sufficient.
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

// In-flight refresh promises keyed by sessionId. Settles + self-cleans
// via a finally hook. Module-level on purpose — the lock has to outlive
// any single call to coalesce concurrent waiters.
const refreshLocks = new Map<string, Promise<SessionData | null>>();

export async function getValidatedSession(
  sessionId: string,
  deps: Deps = {},
): Promise<SessionData | null> {
  const store = deps.store ?? sessionStore;
  const refresh = deps.refresh ?? directusRefresh;
  const now = deps.now ?? Date.now;

  // S-M4: peek can throw on Directus 5xx / network blip. Without
  // try/catch the exception bubbles to the route handler as an
  // uncaught 500, which contradicts the same "preserve the row,
  // retry next request" policy applied to refresh failures below.
  // Treat a peek failure as "not authenticated for this request" —
  // callers redirect to /login or return 401, the cookie stays and
  // the next request retries.
  let session: SessionData | undefined;
  try {
    session = await store.peek(sessionId);
  } catch {
    return null;
  }
  if (!session) return null;

  if (session.expiresAt > now()) return session;

  // Access token expired — refresh through the lock so a burst of
  // concurrent requests collapses to a single Directus call.
  let inflight = refreshLocks.get(sessionId);
  if (!inflight) {
    inflight = (async (): Promise<SessionData | null> => {
      const result = await refresh(session.refreshToken);
      if (!result.ok) {
        // Only invalid_refresh_token is terminal. network_error and
        // directus_error are transient — preserve the row so the next
        // request retries with the same (still-valid) refresh token.
        if (result.error === 'invalid_refresh_token') {
          await store.delete(sessionId);
        }
        return null;
      }
      const refreshed: SessionData = {
        accessToken: result.value.accessToken,
        refreshToken: result.value.refreshToken,
        expiresAt: now() + result.value.expiresInMs,
      };
      await store.update(sessionId, refreshed);
      return refreshed;
    })();
    refreshLocks.set(sessionId, inflight);
    // Self-clean after settle. Guarded so a brand-new refresh for the
    // same sessionId (started after settle) isn't accidentally dropped.
    void inflight.finally(() => {
      if (refreshLocks.get(sessionId) === inflight) {
        refreshLocks.delete(sessionId);
      }
    });
  }
  return inflight;
}
