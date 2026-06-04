// Validates that an incoming request's Origin (or Referer) header points at
// an allowed origin. Used by state-changing Route Handlers as part of the
// CSRF defence (alongside SameSite=Lax cookies — see security-checklist A08).
//
// SameSite=Lax blocks cross-site POST/fetch/XHR (the typical CSRF vector)
// but allows top-level cross-site GET navigation (OAuth redirects, magic
// link emails, payment callbacks). This Origin check is the explicit guard
// on mutations — it rejects state-changing requests whose Origin / Referer
// doesn't match an allowed origin, independent of any SameSite behaviour.
//
// Strict equality only — no wildcards, no subdomain matching.
// Same-origin requests (no Origin header AND no Referer) are allowed, since
// some browsers omit Origin on same-origin requests.

const STATE_CHANGING = /^(POST|PUT|PATCH|DELETE)$/i;

export function validateOrigin(
  originHeader: string | null,
  refererHeader: string | null,
  allowedOrigins: readonly string[],
  // Optional HTTP method. When omitted, the lenient (legacy) path is
  // taken — preserved for existing tests. Production callers should
  // ALWAYS pass `request.method` so state-changing requests without
  // an Origin or Referer header are rejected (S-M2 in audit
  // 2026-05-30 — defence-in-depth alongside the SameSite cookie attr).
  method?: string,
): boolean {
  // No Origin and no Referer:
  //   - Safe methods (GET/HEAD/OPTIONS) or method-unknown: lenient.
  //     Some browsers (Safari) omit Origin on same-origin GETs.
  //   - State-changing methods: reject. Fetch spec requires at least
  //     one of Origin/Referer for cross-origin POST/PUT/PATCH/DELETE,
  //     and accepting headerless mutations from non-browsers (curl,
  //     SSRF chains, header-stripping proxies that already have the
  //     cookie) defeats the CSRF defence-in-depth.
  if (!originHeader && !refererHeader) {
    if (method && STATE_CHANGING.test(method)) return false;
    return true;
  }

  if (originHeader) {
    return isAllowed(originHeader, allowedOrigins);
  }

  // Origin missing → fall back to Referer's origin
  const refOrigin = parseOrigin(refererHeader);
  if (refOrigin === null) return false;
  return allowedOrigins.includes(refOrigin);
}

function isAllowed(rawOrigin: string, allowedOrigins: readonly string[]): boolean {
  const parsed = parseOrigin(rawOrigin);
  if (parsed === null) return false;
  return allowedOrigins.includes(parsed);
}

function parseOrigin(raw: string | null): string | null {
  if (!raw) return null;
  try {
    const url = new URL(raw);
    return url.origin;
  } catch {
    return null;
  }
}
