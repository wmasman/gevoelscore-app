// Resolves the public-facing origin (e.g. https://gevoelscore-frontend.fly.dev)
// from an incoming Request. Used by OAuth routes to build the redirect_uri
// that gets sent to Google.
//
// Why this exists:
//   Behind Fly's edge proxy, Node sees `request.url` as
//   `https://0.0.0.0:3000/...` (the internal listen address), NOT the
//   public domain the browser actually used. Sending that internal URL
//   to Google's OAuth flow results in a redirect_uri mismatch (Fout
//   400: invalid_request) because Google only accepts the URI
//   registered in the Cloud Console.
//
// Resolution priority:
//   1. APP_BASE_URL env var (if set explicitly — strongest signal,
//      single source of truth across all routes).
//   2. x-forwarded-host header (set by some proxies — Fly preserves
//      the client's Host header, sometimes also forwards x-forwarded-host).
//   3. host header (Fly preserves this from the client).
//   4. request.url fallback (local dev, no proxy).
//
// Skips host candidates that look like Node's internal listen address
// (0.0.0.0, localhost, 127.0.0.1) unless we're in the request.url
// fallback path — those are valid for local dev but never for prod.

const INTERNAL_HOST_PREFIXES = ['0.0.0.0', 'localhost', '127.0.0.1'];

function isInternalHost(host: string): boolean {
  return INTERNAL_HOST_PREFIXES.some((prefix) => host.startsWith(prefix));
}

export function getPublicOrigin(request: Request): string {
  // 1. Explicit env var wins.
  const envBase = process.env.APP_BASE_URL;
  if (envBase) {
    return envBase.replace(/\/+$/, ''); // strip trailing slashes
  }

  // 2. + 3. Header-derived (production behind a proxy).
  const proto = request.headers.get('x-forwarded-proto');
  const forwardedHost = request.headers.get('x-forwarded-host');
  const hostHeader = request.headers.get('host');
  const candidate = forwardedHost ?? hostHeader;

  if (candidate && !isInternalHost(candidate)) {
    // Behind a proxy that's preserving the public host. Default to
    // https unless x-forwarded-proto explicitly says otherwise.
    return `${proto ?? 'https'}://${candidate}`;
  }

  // 4. Local-dev fallback: use the request URL as-is.
  return new URL(request.url).origin;
}
