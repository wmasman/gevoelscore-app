// Module-level singletons for the auth stores. Route Handlers import from
// here so they all share state across requests within a single Node process.
//
// sessionStore is Directus-backed when `DIRECTUS_TOKEN` is configured (prod
// and any dev environment that wants to test the real path); it falls back
// to an in-memory Map otherwise — useful for tests and minimal local setups.
// The fallback keeps the contract identical: a swap-in implementation, no
// caller change.
//
// The other stores (pending-otp, pending-tfa, rate-limiter) remain in-memory
// for now. Pending stores are short-lived (5-min TTL) so a restart-induced
// wipe is barely user-visible; rate-limiters reset on restart but the cost
// is "an attacker gets a fresh window after each deploy", not "all users
// get logged out".

import { createDirectusSessionStore } from './directus-session-store';
import { createRateLimiter } from './rate-limit';
import { createSessionStore, type SessionStore } from './session';
import { createPendingOtpStore } from './pending-otp';
import { createPendingTfaStore } from './pending-tfa';

const FIVE_MIN_MS = 5 * 60_000;

// Five attempts per five minutes per IP, per endpoint family. Login and verify
// are separate namespaces so they don't share counters.
export const loginRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });
export const verifyRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });
export const tfaGenerateRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });
export const tfaEnableRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });

// Writes to /api/day-entries/[date] — guards a stolen-session attacker from
// dumping arbitrary scores. Tighter limits (e.g. 5/5min) trip on normal
// use: one editing session can easily fire score + note + multiple tag
// toggles in 10s. 60/5min (12/min) catches abuse while leaving normal
// bursts unblocked.
export const dayEntryWriteRateLimiter = createRateLimiter({
  limit: 60,
  windowMs: FIVE_MIN_MS,
});

function buildSessionStore(): SessionStore {
  const adminToken = process.env.DIRECTUS_TOKEN;
  const directusUrl =
    process.env.DIRECTUS_URL ??
    process.env.NEXT_PUBLIC_DIRECTUS_URL ??
    null;
  if (!adminToken || !directusUrl) {
    // No service token configured. Fall back to the in-memory store.
    // The page-level redirect (page.tsx) still guards the UX failure mode;
    // the only regression vs. Directus storage is "sessions don't survive
    // a process restart", which is fine for tests and minimal-config dev.
    return createSessionStore();
  }
  return createDirectusSessionStore({ directusUrl, adminToken });
}

export const sessionStore = buildSessionStore();

// @sensitive-store: do not pass to console.log, JSON.stringify, or any logger.
// Contains the user's plaintext password between /login and /login/verify so
// the OTP step can re-auth without prompting again. Lifecycle hardened in
// pending-otp.ts (audit H3 cheap fix); full AES-GCM at rest deferred.
export const pendingOtpStore = createPendingOtpStore();

export const pendingTfaStore = createPendingTfaStore();

// Resolve the client IP. Precedence:
//   1. `Fly-Client-IP` — set by Fly's edge, not appendable by the client.
//   2. `X-Real-IP` — set by some reverse proxies; same trust posture.
//   3. *Last* entry of `X-Forwarded-For` — the address closest to our proxy.
//      Earlier entries are client-controlled in single-proxy hops (audit H4).
//   4. 'unknown' fallback — single bucket; safe because the app sits behind
//      Fly's edge in production.
// Assumes the app always runs behind Fly.io's edge proxy. If moving off Fly,
// audit the rate-limit bypass surface.
export function getClientIp(request: Request): string {
  const fly = request.headers.get('fly-client-ip');
  if (fly) return fly.trim();
  const real = request.headers.get('x-real-ip');
  if (real) return real.trim();
  const xff = request.headers.get('x-forwarded-for');
  if (xff) {
    const parts = xff.split(',').map((p) => p.trim()).filter(Boolean);
    if (parts.length > 0) return parts[parts.length - 1]!;
  }
  return 'unknown';
}
