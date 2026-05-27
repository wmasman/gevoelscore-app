// Module-level singletons for the auth stores. Route Handlers import from
// here so they all share the same in-memory state across requests within a
// single Node process.
//
// Single-process Fly machine per ADR 0003 makes this safe. If horizontally
// scaled later, swap each store's implementation (Redis / Directus collection)
// while keeping these exports stable.

import { createRateLimiter } from './rate-limit';
import { createSessionStore } from './session';
import { createPendingOtpStore } from './pending-otp';
import { createPendingTfaStore } from './pending-tfa';

const FIVE_MIN_MS = 5 * 60_000;

// Five attempts per five minutes per IP, per endpoint family. Login and verify
// are separate namespaces so they don't share counters.
export const loginRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });
export const verifyRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });
export const tfaGenerateRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });
export const tfaEnableRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });

export const sessionStore = createSessionStore();
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
