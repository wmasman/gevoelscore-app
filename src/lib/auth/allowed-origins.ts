// Returns the list of origins that the auth route handlers will accept on the
// `Origin` / `Referer` headers for state-changing requests (CSRF defense A08).
// Reads env vars at call time so tests can stub them per-case.
//
// In production an empty list is treated as a misconfiguration and throws —
// `validateOrigin(null, null, [])` would otherwise treat header-less requests
// as same-origin and silently disable CSRF protection (audit M3). The throw
// happens at call time rather than module load so a misconfigured deploy
// returns 500 (loud) instead of refusing to start (impossible to triage from
// the outside).

export function allowedOrigins(): string[] {
  const origins: string[] = [];
  if (process.env.NEXT_PUBLIC_APP_URL) origins.push(process.env.NEXT_PUBLIC_APP_URL);
  if (process.env.NODE_ENV !== 'production') {
    origins.push(
      'http://localhost:3000',
      'http://localhost:3001',
      'http://localhost:3002',
      'http://localhost:3003',
    );
  }
  if (process.env.NODE_ENV === 'production' && origins.length === 0) {
    throw new Error(
      'allowedOrigins: NEXT_PUBLIC_APP_URL must be set in production (CSRF defense relies on it).',
    );
  }
  return origins;
}
