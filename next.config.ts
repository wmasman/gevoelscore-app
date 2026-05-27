import type { NextConfig } from 'next';

const config: NextConfig = {
  // Standalone build for Docker / Fly.io — outputs a minimal server bundle.
  // See ADR 0003 for the Fly.io deployment shape.
  output: 'standalone',

  // No telemetry — per the cardinal principles (see CLAUDE.md and ADR 0002).
  // NEXT_TELEMETRY_DISABLED=1 is also set in fly.toml, but belt-and-braces.
  // Note: Next reads NEXT_TELEMETRY_DISABLED from env; this comment is a marker.

  reactStrictMode: true,
};

export default config;
