// Short-lived store for credentials stashed between /api/auth/login and
// /api/auth/login/verify when the user's account requires 2FA. Mirrors the
// shape of `session.ts` but with a different payload and a much shorter TTL
// (5 minutes — long enough to walk to the authenticator app, short enough
// to limit blast radius if the cookie somehow leaks).
//
// Same single-process-Fly-machine assumption as the session store.
//
// H3 (audit): password is overwritten with random bytes immediately before
// the entry leaves the Map, shrinking the window during which a heap
// snapshot could capture the plaintext. Strings in JS are immutable so the
// original allocation persists until GC — this is best-effort. Full AES-GCM
// at rest is deferred per the Step 9 trade-off.

import { randomBytes } from 'node:crypto';

export const PENDING_OTP_COOKIE_NAME = 'gs_pending_otp';

function wipe(entry: PendingOtpData): void {
  entry.password = randomBytes(Math.max(32, entry.password.length)).toString('base64');
}

export type PendingOtpData = {
  email: string;
  password: string;
  expiresAt: number;
  attempts: number;
};

export type PendingOtpStoreConfig = {
  now?: () => number;
  idGenerator?: () => string;
};

export type PendingOtpStore = {
  create: (data: PendingOtpData) => string;
  get: (id: string) => PendingOtpData | undefined;
  delete: (id: string) => void;
  // Returns the new attempt count, or undefined if the id is unknown/expired
  // (audit M5: per-pending-id OTP attempt counter).
  incrementAttempts: (id: string) => number | undefined;
  cleanupExpired: () => void;
  size: () => number;
};

export function createPendingOtpStore(config: PendingOtpStoreConfig = {}): PendingOtpStore {
  const now = config.now ?? Date.now;
  const idGenerator = config.idGenerator ?? (() => crypto.randomUUID());
  const entries = new Map<string, PendingOtpData>();

  const store: PendingOtpStore = {
    create(data) {
      const id = idGenerator();
      entries.set(id, data);
      return id;
    },

    get(id) {
      const entry = entries.get(id);
      if (!entry) return undefined;
      if (entry.expiresAt <= now()) {
        wipe(entry);
        entries.delete(id);
        return undefined;
      }
      return entry;
    },

    delete(id) {
      const entry = entries.get(id);
      if (entry) wipe(entry);
      entries.delete(id);
    },

    incrementAttempts(id) {
      const entry = entries.get(id);
      if (!entry) return undefined;
      if (entry.expiresAt <= now()) {
        wipe(entry);
        entries.delete(id);
        return undefined;
      }
      entry.attempts += 1;
      return entry.attempts;
    },

    cleanupExpired() {
      const t = now();
      for (const [id, entry] of entries) {
        if (entry.expiresAt <= t) {
          wipe(entry);
          entries.delete(id);
        }
      }
    },

    size() {
      return entries.size;
    },
  };

  // Safe stringification: a stray `console.log(pendingOtpStore)` must not
  // print the entries map. The override stays non-enumerable so JSON.stringify
  // also returns `{}` rather than the entries.
  Object.defineProperty(store, 'toString', {
    value: function (): string {
      return `[PendingOtpStore: ${entries.size} entries — do not log]`;
    },
    enumerable: false,
  });

  return store;
}

export function buildPendingOtpCookie(id: string | null, maxAgeSeconds: number): string {
  const value = id ?? '';
  return [
    `${PENDING_OTP_COOKIE_NAME}=${value}`,
    'HttpOnly',
    'Secure',
    'SameSite=Strict',
    'Path=/',
    `Max-Age=${maxAgeSeconds}`,
  ].join('; ');
}

export function parsePendingOtpCookie(header: string | null): string | null {
  if (!header) return null;
  for (const raw of header.split(';')) {
    const [name, ...rest] = raw.trim().split('=');
    if (name === PENDING_OTP_COOKIE_NAME) {
      const value = rest.join('=');
      return value.length > 0 ? value : null;
    }
  }
  return null;
}
