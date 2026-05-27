// Short-lived store for credentials stashed between /api/auth/login and
// /api/auth/login/verify when the user's account requires 2FA. Mirrors the
// shape of `session.ts` but with a different payload and a much shorter TTL
// (5 minutes — long enough to walk to the authenticator app, short enough
// to limit blast radius if the cookie somehow leaks).
//
// Same single-process-Fly-machine assumption as the session store.

export const PENDING_OTP_COOKIE_NAME = 'gs_pending_otp';

export type PendingOtpData = {
  email: string;
  password: string;
  expiresAt: number;
};

export type PendingOtpStoreConfig = {
  now?: () => number;
  idGenerator?: () => string;
};

export type PendingOtpStore = {
  create: (data: PendingOtpData) => string;
  get: (id: string) => PendingOtpData | undefined;
  delete: (id: string) => void;
  cleanupExpired: () => void;
  size: () => number;
};

export function createPendingOtpStore(config: PendingOtpStoreConfig = {}): PendingOtpStore {
  const now = config.now ?? Date.now;
  const idGenerator = config.idGenerator ?? (() => crypto.randomUUID());
  const entries = new Map<string, PendingOtpData>();

  return {
    create(data) {
      const id = idGenerator();
      entries.set(id, data);
      return id;
    },

    get(id) {
      const entry = entries.get(id);
      if (!entry) return undefined;
      if (entry.expiresAt <= now()) {
        entries.delete(id);
        return undefined;
      }
      return entry;
    },

    delete(id) {
      entries.delete(id);
    },

    cleanupExpired() {
      const t = now();
      for (const [id, entry] of entries) {
        if (entry.expiresAt <= t) entries.delete(id);
      }
    },

    size() {
      return entries.size;
    },
  };
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
