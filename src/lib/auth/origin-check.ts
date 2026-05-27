// Validates that an incoming request's Origin (or Referer) header points at
// an allowed origin. Used by state-changing Route Handlers as part of the
// CSRF defence (alongside SameSite=Strict cookies — see security-checklist A08).
//
// Strict equality only — no wildcards, no subdomain matching.
// Same-origin requests (no Origin header AND no Referer) are allowed, since
// some browsers omit Origin on same-origin requests.

export function validateOrigin(
  originHeader: string | null,
  refererHeader: string | null,
  allowedOrigins: readonly string[],
): boolean {
  // No Origin and no Referer → trust the same-origin path. Cross-origin
  // requests must include at least one of these per the Fetch spec.
  if (!originHeader && !refererHeader) return true;

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
