/** @vitest-environment jsdom */
// Phase 1.E.1 — CalendarsSection (Settings → Kalenders surface).

import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

const routerMocks = vi.hoisted(() => ({
  refresh: vi.fn(),
  push: vi.fn(),
}));

vi.mock('next/navigation', () => ({
  useRouter: () => routerMocks,
}));

import { CalendarsSection } from '../calendars-section';
import type { DirectusCalendarConnectionRow } from '@/lib/api/calendars';

const NOW = new Date('2026-06-04T12:00:00Z');

function conn(overrides: Partial<DirectusCalendarConnectionRow> = {}): DirectusCalendarConnectionRow {
  return {
    id: 'conn-1',
    user_id: 'user-1',
    provider: 'google',
    provider_account_email: 'wmasman@gmail.com',
    refresh_token_encrypted: 'v1.iv.ct.tag',
    scope: 'https://www.googleapis.com/auth/calendar.readonly',
    connected_at: '2026-06-04T08:00:00.000Z',
    last_synced_at: '2026-06-04T10:00:00.000Z',
    last_sync_error: null,
    status: 'active',
    included_calendar_ids: ['wmasman@gmail.com'],
    ...overrides,
  };
}

// We rely on window.location.href assignment for the OAuth redirect.
// jsdom's window.location is read-only by default; we install a stub.
const originalLocation = window.location;
function stubLocation() {
  const href = { value: '' };
  Object.defineProperty(window, 'location', {
    value: {
      ...originalLocation,
      get href() {
        return href.value;
      },
      set href(v: string) {
        href.value = v;
      },
    },
    writable: true,
    configurable: true,
  });
  return href;
}

const fetchMock = vi.fn();
beforeEach(() => {
  routerMocks.refresh.mockReset();
  routerMocks.push.mockReset();
  fetchMock.mockReset();
  globalThis.fetch = fetchMock as unknown as typeof fetch;
});
afterEach(() => {
  cleanup();
  Object.defineProperty(window, 'location', {
    value: originalLocation,
    writable: true,
    configurable: true,
  });
});

describe('CalendarsSection', () => {
  describe('empty state', () => {
    it('renders empty message + Verbind Google Calendar button', () => {
      render(<CalendarsSection connections={[]} now={NOW} />);

      expect(screen.getByText('Geen kalenders verbonden.')).toBeInTheDocument();
      expect(
        screen.getByRole('button', { name: 'Verbind Google Calendar' }),
      ).toBeInTheDocument();
    });

    it('clicking Verbind POSTs to /api/calendars/google/connect and redirects', async () => {
      const href = stubLocation();
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ redirect_url: 'https://accounts.google.com/o/oauth2/v2/auth?x=1' }),
      });

      render(<CalendarsSection connections={[]} now={NOW} />);
      await userEvent.click(screen.getByRole('button', { name: 'Verbind Google Calendar' }));

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
      const [url, init] = fetchMock.mock.calls[0]!;
      expect(url).toBe('/api/calendars/google/connect');
      expect((init as RequestInit).method).toBe('POST');
      await waitFor(() => expect(href.value).toContain('accounts.google.com'));
    });

    it('connect failure shows the connectError text and stays on the page', async () => {
      stubLocation();
      fetchMock.mockResolvedValueOnce({ ok: false, json: async () => ({}) });

      render(<CalendarsSection connections={[]} now={NOW} />);
      await userEvent.click(screen.getByRole('button', { name: 'Verbind Google Calendar' }));

      expect(
        await screen.findByText('Verbinden lukte niet. Probeer opnieuw.'),
      ).toBeInTheDocument();
    });
  });

  describe('connected state — one active connection', () => {
    it('renders email, status, relative last-sync time, and refresh + disconnect buttons', () => {
      render(<CalendarsSection connections={[conn()]} now={NOW} />);

      expect(screen.getByText('wmasman@gmail.com')).toBeInTheDocument();
      expect(screen.getByText(/Verbonden/)).toBeInTheDocument();
      expect(screen.getByText(/2 uur geleden/)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Ververs nu' })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Ontkoppel' })).toBeInTheDocument();
    });

    it('shows neverSynced text when last_synced_at is null', () => {
      render(
        <CalendarsSection
          connections={[conn({ last_synced_at: null })]}
          now={NOW}
        />,
      );

      expect(screen.getByText(/Nog niet gesynchroniseerd/)).toBeInTheDocument();
    });

    it('error status surfaces the last_sync_error text', () => {
      render(
        <CalendarsSection
          connections={[
            conn({ status: 'error', last_sync_error: 'refresh_token_invalid' }),
          ]}
          now={NOW}
        />,
      );

      // status + relative time share one <p>, separated by "·"
      expect(screen.getByText(/Fout/)).toBeInTheDocument();
      expect(screen.getByText('refresh_token_invalid')).toBeInTheDocument();
    });

    it('Ververs nu POSTs to /api/calendars/sync and calls router.refresh on success', async () => {
      fetchMock.mockResolvedValueOnce({ ok: true, json: async () => ({ ok: true }) });

      render(<CalendarsSection connections={[conn()]} now={NOW} />);
      await userEvent.click(screen.getByRole('button', { name: 'Ververs nu' }));

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
      expect(fetchMock.mock.calls[0]![0]).toBe('/api/calendars/sync');
      await waitFor(() => expect(routerMocks.refresh).toHaveBeenCalledTimes(1));
    });

    it('shows in-flight text "Synchroniseren..." during sync', async () => {
      let resolve: (v: unknown) => void = () => {};
      fetchMock.mockReturnValueOnce(
        new Promise((r) => {
          resolve = r;
        }),
      );

      render(<CalendarsSection connections={[conn()]} now={NOW} />);
      await userEvent.click(screen.getByRole('button', { name: 'Ververs nu' }));

      expect(
        await screen.findByRole('button', { name: 'Synchroniseren...' }),
      ).toBeInTheDocument();

      resolve({ ok: true, json: async () => ({}) });
    });

    it('sync failure shows the refreshError text', async () => {
      fetchMock.mockResolvedValueOnce({ ok: false, json: async () => ({}) });

      render(<CalendarsSection connections={[conn()]} now={NOW} />);
      await userEvent.click(screen.getByRole('button', { name: 'Ververs nu' }));

      expect(
        await screen.findByText('Synchroniseren lukte niet. Probeer opnieuw.'),
      ).toBeInTheDocument();
    });
  });

  describe('disconnect flow', () => {
    it('Ontkoppel opens an alertdialog with focus on Annuleren', async () => {
      render(<CalendarsSection connections={[conn()]} now={NOW} />);
      await userEvent.click(screen.getByRole('button', { name: 'Ontkoppel' }));

      const dialog = await screen.findByRole('alertdialog');
      expect(dialog).toBeInTheDocument();
      const cancel = screen.getByRole('button', { name: 'Annuleren' });
      await waitFor(() => expect(cancel).toHaveFocus());
    });

    it('Annuleren closes the alertdialog without POSTing', async () => {
      render(<CalendarsSection connections={[conn()]} now={NOW} />);
      await userEvent.click(screen.getByRole('button', { name: 'Ontkoppel' }));
      await userEvent.click(screen.getByRole('button', { name: 'Annuleren' }));

      await waitFor(() =>
        expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument(),
      );
      expect(fetchMock).not.toHaveBeenCalled();
    });

    it('Ja, ontkoppel POSTs to /api/calendars/[id]/disconnect and refreshes', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ok: true, revoke_ok: true }),
      });

      render(<CalendarsSection connections={[conn()]} now={NOW} />);
      await userEvent.click(screen.getByRole('button', { name: 'Ontkoppel' }));
      await userEvent.click(screen.getByRole('button', { name: 'Ja, ontkoppel' }));

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
      expect(fetchMock.mock.calls[0]![0]).toBe('/api/calendars/conn-1/disconnect');
      await waitFor(() => expect(routerMocks.refresh).toHaveBeenCalledTimes(1));
    });

    it('shows revoke-failed warning when revoke_ok=false (local cascade still ran)', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ok: true, revoke_ok: false }),
      });

      render(<CalendarsSection connections={[conn()]} now={NOW} />);
      await userEvent.click(screen.getByRole('button', { name: 'Ontkoppel' }));
      await userEvent.click(screen.getByRole('button', { name: 'Ja, ontkoppel' }));

      expect(
        await screen.findByText(/intrekken bij Google lukte niet/),
      ).toBeInTheDocument();
    });

    it('disconnect failure shows the disconnectError text', async () => {
      fetchMock.mockResolvedValueOnce({ ok: false, json: async () => ({}) });

      render(<CalendarsSection connections={[conn()]} now={NOW} />);
      await userEvent.click(screen.getByRole('button', { name: 'Ontkoppel' }));
      await userEvent.click(screen.getByRole('button', { name: 'Ja, ontkoppel' }));

      expect(
        await screen.findByText('Ontkoppelen lukte niet. Probeer opnieuw.'),
      ).toBeInTheDocument();
    });
  });

  describe('forward-marker copy', () => {
    it('shows "Binnenkort: Outlook, Apple" when at least one calendar is connected', () => {
      render(<CalendarsSection connections={[conn()]} now={NOW} />);
      expect(screen.getByText('Binnenkort: Outlook, Apple')).toBeInTheDocument();
    });

    it('does NOT show the forward-marker copy on the empty state (cleaner first-time UX)', () => {
      render(<CalendarsSection connections={[]} now={NOW} />);
      expect(screen.queryByText('Binnenkort: Outlook, Apple')).not.toBeInTheDocument();
    });
  });
});
