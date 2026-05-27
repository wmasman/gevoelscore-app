// Health endpoint for the Fly.io HTTP health check (per fly.toml) and for
// Playwright API tests. Static response — no DB call, no auth — so we can tell
// "the frontend is alive" from "the backend or DB is broken."

export const dynamic = 'force-static';

export function GET() {
  return Response.json({ status: 'ok' });
}
