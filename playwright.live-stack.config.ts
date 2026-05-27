// Live-stack Playwright config — runs against the production build
// (`next start`) and the real Directus on Fly. Used only by `npm run test:live`.
//
// Why a separate config:
// - `next dev` resets module state between requests; rate-limit + session
//   integration tests need `next start` to behave correctly.
// - DIRECTUS_URL points at the real backend, not the unreachable safety
//   default from playwright.config.ts.
//
// Credentials come from .env.local (gitignored). See step-8 doc for the
// one-time Directus user setup.

import { defineConfig, devices } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

// Tiny .env.local loader — no dotenv dep. Lines like `KEY=value`, comments
// stripped. Idempotent: doesn't override variables already in process.env.
function loadDotenvLocal(): void {
  try {
    const content = readFileSync(resolve(process.cwd(), '.env.local'), 'utf-8');
    for (const line of content.split(/\r?\n/)) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const eq = trimmed.indexOf('=');
      if (eq < 0) continue;
      const key = trimmed.slice(0, eq).trim();
      const value = trimmed.slice(eq + 1).trim().replace(/^["']|["']$/g, '');
      if (key && !(key in process.env)) {
        process.env[key] = value;
      }
    }
  } catch {
    // .env.local missing or unreadable — that's fine; the specs will skip
    // gracefully if credentials aren't set.
  }
}

loadDotenvLocal();

const PORT = Number(process.env.PORT ?? 3000);
const BASE_URL = process.env.PLAYWRIGHT_BASE_URL ?? `http://localhost:${PORT}`;

export default defineConfig({
  testDir: './tests/live-stack',
  fullyParallel: false, // shared module state — serialise to avoid IP collisions
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 1,
  reporter: 'list',
  timeout: 60_000,
  use: {
    baseURL: BASE_URL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'live-stack',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    // Production build + start. Slower than dev mode but accurate.
    command: 'npm run build && npm run start',
    url: BASE_URL,
    reuseExistingServer: !process.env.CI,
    stdout: 'pipe',
    stderr: 'pipe',
    timeout: 180_000,
    env: {
      NODE_ENV: 'production',
      DIRECTUS_URL: process.env.DIRECTUS_URL ?? 'https://gevoelscore-backend.fly.dev',
      NEXT_PUBLIC_APP_URL: BASE_URL,
    },
  },
});
