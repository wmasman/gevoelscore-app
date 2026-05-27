// In-memory rate limiter for auth endpoints.
//
// One limiter instance per namespace (e.g. one for /api/auth/login, one for
// /api/auth/login/verify) — counters do NOT share across instances. Each
// instance keeps a Map<key, { count, windowEndsAt }>.
//
// Single-process Fly machine assumed (ADR 0003: min_machines_running = 1).
// If scaled later, swap implementation for a shared store; the API stays.

export type RateLimitResult =
  | { allowed: true; remaining: number }
  | { allowed: false; retryAfterMs: number };

export type RateLimiterConfig = {
  limit: number;
  windowMs: number;
  now?: () => number;
};

export type RateLimiter = {
  check: (key: string) => RateLimitResult;
  sweep: () => void;
  size: () => number;
};

type Entry = { count: number; windowEndsAt: number };

export function createRateLimiter(config: RateLimiterConfig): RateLimiter {
  const { limit, windowMs } = config;
  const now = config.now ?? Date.now;
  const entries = new Map<string, Entry>();

  return {
    check(key) {
      const t = now();
      const existing = entries.get(key);

      if (!existing || existing.windowEndsAt <= t) {
        entries.set(key, { count: 1, windowEndsAt: t + windowMs });
        return { allowed: true, remaining: limit - 1 };
      }

      if (existing.count >= limit) {
        return { allowed: false, retryAfterMs: existing.windowEndsAt - t };
      }

      existing.count += 1;
      return { allowed: true, remaining: limit - existing.count };
    },

    sweep() {
      const t = now();
      for (const [key, entry] of entries) {
        if (entry.windowEndsAt <= t) entries.delete(key);
      }
    },

    size() {
      return entries.size;
    },
  };
}
