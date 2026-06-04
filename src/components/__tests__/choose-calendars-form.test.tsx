/** @vitest-environment jsdom */
// Phase 1.E.2 — ChooseCalendarsForm (/settings/kalenders/choose screen).

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

import { ChooseCalendarsForm } from '../choose-calendars-form';

const CONN_ID = 'fa049661-9119-4d00-8871-9b1c5e262adc';

const SAMPLE_CALENDARS = [
  { id: 'wmasman@gmail.com', displayName: 'wmasman@gmail.com', isPrimary: true },
  { id: 'family-cal-id', displayName: 'Family', isPrimary: false },
  { id: 'work-cal-id', displayName: 'Work', isPrimary: false },
];

const fetchMock = vi.fn();
beforeEach(() => {
  routerMocks.refresh.mockReset();
  routerMocks.push.mockReset();
  fetchMock.mockReset();
  globalThis.fetch = fetchMock as unknown as typeof fetch;
});
afterEach(() => cleanup());

describe('ChooseCalendarsForm', () => {
  describe('loading + ready', () => {
    it('shows loading state initially', () => {
      fetchMock.mockReturnValueOnce(new Promise(() => {}));
      render(<ChooseCalendarsForm connectionId={CONN_ID} />);
      expect(screen.getByText('Kalenders laden...')).toBeInTheDocument();
    });

    it('renders one checkbox per calendar with all checked by default (AC1.58)', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ calendars: SAMPLE_CALENDARS }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);

      await waitFor(() =>
        expect(screen.getByLabelText(/wmasman@gmail\.com/)).toBeInTheDocument(),
      );
      const checkboxes = screen.getAllByRole('checkbox');
      expect(checkboxes).toHaveLength(3);
      for (const cb of checkboxes) expect(cb).toBeChecked();
    });

    it('renders Primary "Hoofd" badge on the primary calendar', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ calendars: SAMPLE_CALENDARS }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);

      await waitFor(() => expect(screen.getByText('Hoofd')).toBeInTheDocument());
    });

    it('GET request URL is /api/calendars/[id]/calendars', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ calendars: [] }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
      expect(fetchMock.mock.calls[0]![0]).toBe(`/api/calendars/${CONN_ID}/calendars`);
    });
  });

  describe('load error + retry', () => {
    it('shows loadError text and a retry button on non-200 response', async () => {
      fetchMock.mockResolvedValueOnce({ ok: false, json: async () => ({}) });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);

      expect(
        await screen.findByText('Kalenders ophalen lukte niet. Probeer opnieuw.'),
      ).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Opnieuw laden' })).toBeInTheDocument();
    });

    it('clicking retry refires the GET request', async () => {
      fetchMock.mockResolvedValueOnce({ ok: false, json: async () => ({}) });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);
      await screen.findByText('Kalenders ophalen lukte niet. Probeer opnieuw.');

      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ calendars: SAMPLE_CALENDARS }),
      });
      await userEvent.click(screen.getByRole('button', { name: 'Opnieuw laden' }));

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
      await waitFor(() => expect(screen.getAllByRole('checkbox')).toHaveLength(3));
    });
  });

  describe('toggle + submit', () => {
    it('clicking a checkbox toggles its state', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ calendars: SAMPLE_CALENDARS }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);
      const cbs = await screen.findAllByRole('checkbox');
      expect(cbs[0]).toBeChecked();

      await userEvent.click(cbs[0]!);
      expect(cbs[0]).not.toBeChecked();
    });

    it('Verbinden POSTs the checked IDs and navigates to /settings', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ calendars: SAMPLE_CALENDARS }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);
      const workCb = await screen.findByLabelText(/^Work/);
      // Uncheck Work
      await userEvent.click(workCb);

      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ok: true, included_calendar_ids: [] }),
      });
      await userEvent.click(screen.getByRole('button', { name: 'Verbinden' }));

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
      const [url, init] = fetchMock.mock.calls[1]!;
      expect(url).toBe(`/api/calendars/${CONN_ID}/calendars`);
      expect((init as RequestInit).method).toBe('POST');
      const body = JSON.parse((init as RequestInit).body as string) as {
        included_calendar_ids: string[];
      };
      expect(body.included_calendar_ids).toEqual(['wmasman@gmail.com', 'family-cal-id']);
      await waitFor(() => expect(routerMocks.push).toHaveBeenCalledWith('/settings'));
    });

    it('Annuleren navigates to /settings without POSTing', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ calendars: SAMPLE_CALENDARS }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);
      await screen.findAllByRole('checkbox');

      await userEvent.click(screen.getByRole('button', { name: 'Annuleren' }));

      expect(routerMocks.push).toHaveBeenCalledWith('/settings');
      // Only the initial GET; no POST
      expect(fetchMock).toHaveBeenCalledTimes(1);
    });

    it('submit failure shows submitError text and leaves the form interactive', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ calendars: SAMPLE_CALENDARS }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);
      await screen.findAllByRole('checkbox');

      fetchMock.mockResolvedValueOnce({ ok: false, json: async () => ({}) });
      await userEvent.click(screen.getByRole('button', { name: 'Verbinden' }));

      expect(
        await screen.findByText('Opslaan lukte niet. Probeer opnieuw.'),
      ).toBeInTheDocument();
      // Verbinden button is still rendered (not 'Bezig...')
      expect(screen.getByRole('button', { name: 'Verbinden' })).toBeInTheDocument();
    });
  });
});
