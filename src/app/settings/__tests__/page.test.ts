import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

// Mirrors src/app/__tests__/page.test.ts: the redirect contract is the
// load-bearing thing, and the new "session-in-store === null" branch
// (ADR 0005) must hold for /settings too, not just /.

const REDIRECT_MARKER = Symbol('redirect');

const mocks = vi.hoisted(() => ({
  cookieValue: null as string | null,
  getValidatedSession: vi.fn(),
  redirectCalls: [] as string[],
}));

vi.mock('next/headers', () => ({
  cookies: async () => ({
    get: (name: string) =>
      name === 'gs_session' && mocks.cookieValue !== null
        ? { name, value: mocks.cookieValue }
        : undefined,
  }),
}));

vi.mock('next/navigation', () => ({
  redirect: (url: string) => {
    mocks.redirectCalls.push(url);
    const e = new Error(`NEXT_REDIRECT:${url}`);
    (e as Error & { __marker: symbol }).__marker = REDIRECT_MARKER;
    throw e;
  },
}));

vi.mock('@/lib/auth/get-validated-session', () => ({
  getValidatedSession: mocks.getValidatedSession,
}));

vi.mock('@/components/settings-view', () => ({
  SettingsView: () => null,
}));

async function runPage(): Promise<{ rendered: boolean; redirectedTo: string | null }> {
  const { default: SettingsPage } = await import('../page');
  try {
    await SettingsPage();
    return { rendered: true, redirectedTo: null };
  } catch (e) {
    if (
      e instanceof Error &&
      (e as Error & { __marker?: symbol }).__marker === REDIRECT_MARKER
    ) {
      return { rendered: false, redirectedTo: mocks.redirectCalls.at(-1) ?? null };
    }
    throw e;
  }
}

describe('SettingsPage redirect behaviour', () => {
  beforeEach(() => {
    mocks.cookieValue = null;
    mocks.getValidatedSession.mockReset();
    mocks.redirectCalls.length = 0;
  });

  afterEach(() => {
    vi.resetModules();
  });

  it('no session cookie → redirects to /login', async () => {
    mocks.cookieValue = null;
    const { rendered, redirectedTo } = await runPage();
    expect(rendered).toBe(false);
    expect(redirectedTo).toBe('/login');
    expect(mocks.getValidatedSession).not.toHaveBeenCalled();
  });

  it('stale cookie (session not in store) → redirects to /login', async () => {
    mocks.cookieValue = 'stale-session-id';
    mocks.getValidatedSession.mockResolvedValueOnce(null);
    const { rendered, redirectedTo } = await runPage();
    expect(rendered).toBe(false);
    expect(redirectedTo).toBe('/login');
  });

  it('cookie + valid session → renders the settings view', async () => {
    mocks.cookieValue = 'live-id';
    mocks.getValidatedSession.mockResolvedValueOnce({
      accessToken: 'at',
      refreshToken: 'rt',
      expiresAt: Date.now() + 60_000,
    });
    const { rendered, redirectedTo } = await runPage();
    expect(rendered).toBe(true);
    expect(redirectedTo).toBeNull();
  });
});
