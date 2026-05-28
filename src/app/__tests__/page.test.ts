import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

// HomePage redirect contract.
//
// This test is the *only* unit-level guard for the auth-redirect behaviour
// of the home screen. The bug it pins down (2026-05-28 investigation): when
// a session cookie exists but the in-memory store has no matching record
// — e.g. after a Fly machine restart — the page used to render the shell
// with empty data and no signal to the user. Now it must redirect to
// /login, same as the no-cookie case.
//
// We mock all the page's dependencies because Next's RSC harness is not
// the unit under test — the unit is HomePage's branch logic.

const REDIRECT_MARKER = Symbol('redirect');

const mocks = vi.hoisted(() => ({
  cookieValue: null as string | null,
  getValidatedSession: vi.fn(),
  readDayEntryByDate: vi.fn(),
  readAllTags: vi.fn(),
  readDayEntriesInRange: vi.fn(),
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
    // Next's real redirect() throws — mirror that so the page function aborts.
    const e = new Error(`NEXT_REDIRECT:${url}`);
    (e as Error & { __marker: symbol }).__marker = REDIRECT_MARKER;
    throw e;
  },
}));

vi.mock('@/lib/auth/get-validated-session', () => ({
  getValidatedSession: mocks.getValidatedSession,
}));

vi.mock('@/lib/api/day-entries', () => ({
  readDayEntryByDate: mocks.readDayEntryByDate,
  readDayEntriesInRange: mocks.readDayEntriesInRange,
}));

vi.mock('@/lib/api/tags', () => ({
  readAllTags: mocks.readAllTags,
}));

vi.mock('@/components/today-shell', () => ({
  TodayShell: () => null,
}));

vi.mock('@/lib/domain/date', async () => {
  const actual = await vi.importActual<typeof import('@/lib/domain/date')>(
    '@/lib/domain/date',
  );
  return { ...actual, todayInAmsterdam: () => '2026-05-28' };
});

async function runPage(): Promise<{ rendered: boolean; redirectedTo: string | null }> {
  const { default: HomePage } = await import('../page');
  try {
    await HomePage();
    return { rendered: true, redirectedTo: null };
  } catch (e) {
    if (
      e instanceof Error &&
      (e as Error & { __marker?: symbol }).__marker === REDIRECT_MARKER
    ) {
      return {
        rendered: false,
        redirectedTo: mocks.redirectCalls.at(-1) ?? null,
      };
    }
    throw e;
  }
}

describe('HomePage redirect behaviour', () => {
  beforeEach(() => {
    mocks.cookieValue = null;
    mocks.getValidatedSession.mockReset();
    mocks.readDayEntryByDate.mockReset().mockResolvedValue({ ok: true, value: null });
    mocks.readAllTags.mockReset().mockResolvedValue({ ok: true, value: [] });
    mocks.readDayEntriesInRange.mockReset().mockResolvedValue({ ok: true, value: [] });
    mocks.redirectCalls.length = 0;
  });

  afterEach(() => {
    vi.resetModules();
  });

  it('no session cookie → redirects to /login (does not call getValidatedSession)', async () => {
    mocks.cookieValue = null;
    const { rendered, redirectedTo } = await runPage();
    expect(rendered).toBe(false);
    expect(redirectedTo).toBe('/login');
    expect(mocks.getValidatedSession).not.toHaveBeenCalled();
  });

  it('cookie present + getValidatedSession returns null → redirects to /login (no data fetched)', async () => {
    // Reproduces the Fly-restart bug: the browser sends an id that no
    // longer exists in the server-side store, so getValidatedSession can't
    // resolve to a live session. Pre-fix, the page rendered an empty shell.
    mocks.cookieValue = 'stale-session-id';
    mocks.getValidatedSession.mockResolvedValueOnce(null);

    const { rendered, redirectedTo } = await runPage();

    expect(rendered).toBe(false);
    expect(redirectedTo).toBe('/login');
    // Critically: no data reads attempted with an invalid session.
    expect(mocks.readDayEntryByDate).not.toHaveBeenCalled();
    expect(mocks.readAllTags).not.toHaveBeenCalled();
    expect(mocks.readDayEntriesInRange).not.toHaveBeenCalled();
  });

  it('cookie + valid session → fetches data and renders (no redirect)', async () => {
    mocks.cookieValue = 'live-id';
    mocks.getValidatedSession.mockResolvedValueOnce({
      accessToken: 'token',
      refreshToken: 'refresh',
      expiresAt: Date.now() + 60_000,
    });

    const { rendered, redirectedTo } = await runPage();

    expect(rendered).toBe(true);
    expect(redirectedTo).toBeNull();
    expect(mocks.readDayEntryByDate).toHaveBeenCalledWith('token', '2026-05-28');
    expect(mocks.readAllTags).toHaveBeenCalledWith('token');
    // 30-day window ending today.
    expect(mocks.readDayEntriesInRange).toHaveBeenCalledWith(
      'token',
      '2026-04-29',
      '2026-05-28',
    );
  });
});
