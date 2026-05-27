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

const FIVE_MIN_MS = 5 * 60_000;

// Five attempts per five minutes per IP, per endpoint family. Login and verify
// are separate namespaces so they don't share counters.
export const loginRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });
export const verifyRateLimiter = createRateLimiter({ limit: 5, windowMs: FIVE_MIN_MS });

export const sessionStore = createSessionStore();
export const pendingOtpStore = createPendingOtpStore();

// Helper: extract the client IP from a Next.js request. Falls back to
// 'unknown' which is then a single rate-limit bucket (which is fine for v1 —
// the API is gated behind Fly.io's edge anyway).
export function getClientIp(request: Request): string {
  const xff = request.headers.get('x-forwarded-for');
  if (xff) {
    const first = xff.split(',')[0];
    if (first) return first.trim();
  }
  return request.headers.get('x-real-ip') ?? 'unknown';
}
