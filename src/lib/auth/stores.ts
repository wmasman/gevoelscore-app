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

// S-M5: permissive read limiter shared between /api/day-entries (range
// read) and /api/day-entries/today. Defence-in-depth against a leaked
// session cookie being hammered — 120/5min (24/min) leaves normal use
// (one range re-fetch per save + occasional toggles) wide open.
export const dayEntryReadRateLimiter = createRateLimiter({
  limit: 120,
  windowMs: FIVE_MIN_MS,
});

// Writes to /api/tags (inline tag creation + step-5 link/unlink + v1.5b
// tag-management Settings: rename / recategorize / archive / un-archive /
// hard-delete). Raised from 60 → 200 / 5min in v1.5b (M4 audit fix): a
// real cleanup-pass session might edit 30-60 tags in a few minutes, which
// burned half-to-all of the original 60/5min budget on legitimate use.
// 200/5min stays anti-abuse-shaped (no human typing on a mobile keyboard
// can sustain >40 writes/min) while comfortably absorbing a cleanup pass.
export const tagWriteRateLimiter = createRateLimiter({
  limit: 200,
  windowMs: FIVE_MIN_MS,
});

// Writes to /api/episodes and /api/episodes/[id] (v1.5 verloop-and-episodes,
// user-facing tab: Periodes). Same posture as tagWriteRateLimiter — a power-
// user editing one episode could fire several auto-save writes per minute,
// 60/5min leaves the normal flow unblocked while catching credential abuse.
export const episodeWriteRateLimiter = createRateLimiter({
  limit: 60,
  windowMs: FIVE_MIN_MS,
});

// Reads from /api/episodes. Matches dayEntryReadRateLimiter — primary read
// path is server-rendered (page.tsx) so the API GET is used for client-side
// refreshes only, with low traffic in normal use.
export const episodeReadRateLimiter = createRateLimiter({
  limit: 120,
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

// S-M3: periodic sweep across the in-memory stores so un-accessed
// entries don't accumulate forever. Lazy expiry on access (in
// rate-limit / pending-otp / pending-tfa) handles the read path; the
// sweep handles the cold-key tail. Per-Fly-machine; the interval
// keeps memory bounded under a sustained credential-stuffing burst
// from many distinct IPs.
//
// Guards:
// - global flag ensures Next.js's dev hot-reload doesn't pile up
//   intervals each time this module is re-evaluated.
// - .unref() lets the Node process exit even if the interval is
//   the only reason it'd stay alive (Vitest workers, dev SIGINT).
const SWEEP_INTERVAL_MS = 5 * FIVE_MIN_MS; // 25 min — plenty for 5-min windows
declare global {
  var __gsAuthSweeper: ReturnType<typeof setInterval> | undefined;
}
if (typeof globalThis !== 'undefined' && globalThis.__gsAuthSweeper === undefined) {
  const handle = setInterval(() => {
    loginRateLimiter.sweep();
    verifyRateLimiter.sweep();
    tfaGenerateRateLimiter.sweep();
    tfaEnableRateLimiter.sweep();
    dayEntryWriteRateLimiter.sweep();
    dayEntryReadRateLimiter.sweep();
    tagWriteRateLimiter.sweep();
    episodeWriteRateLimiter.sweep();
    episodeReadRateLimiter.sweep();
    pendingOtpStore.cleanupExpired();
    pendingTfaStore.cleanupExpired();
  }, SWEEP_INTERVAL_MS);
  // Node's Timeout.unref returns the Timeout in Node >= 14. Tests
  // running in jsdom may have a polyfilled setInterval without
  // .unref — guard with optional chaining.
  handle.unref?.();
  globalThis.__gsAuthSweeper = handle;
}

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
