import type { NextConfig } from 'next';

// Security response headers — audit finding M1. Single source of truth so
// `next.config.ts` is the only place these are configured.
//
// Dev mode adds 'unsafe-eval' to script-src because Next.js + webpack's
// hot-reload pipeline uses eval() for HMR. Without it, dev-mode pages
// never hydrate and every client-component interaction (form submits,
// state updates, navigation) silently fails. Prod build (next start)
// uses the strict CSP. Verified by the live-stack security-headers spec
// and the live curl evidence from the auth-hardening step-4 deploy.
const SCRIPT_SRC =
  process.env.NODE_ENV === 'production'
    ? "script-src 'self' 'unsafe-inline'"
    : "script-src 'self' 'unsafe-inline' 'unsafe-eval'";

const SECURITY_HEADERS = [
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      SCRIPT_SRC,
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data:",
      "connect-src 'self'",
      "frame-ancestors 'none'",
      "base-uri 'self'",
      "form-action 'self'",
    ].join('; '),
  },
  { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
];

const config: NextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  poweredByHeader: false,
  async headers() {
    return [{ source: '/:path*', headers: SECURITY_HEADERS }];
  },
};

export default config;
