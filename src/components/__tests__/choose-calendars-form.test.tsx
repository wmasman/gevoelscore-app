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

  describe('v1.6.1: pre-checked from server + exclude-delete confirm flow', () => {
    it('pre-checks only the calendars in included_calendar_ids when the server returns them', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          calendars: SAMPLE_CALENDARS,
          included_calendar_ids: ['wmasman@gmail.com', 'family-cal-id'],
          event_counts_by_calendar_id: {},
        }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);

      await waitFor(() =>
        expect(screen.getByLabelText(/wmasman@gmail\.com/)).toBeChecked(),
      );
      expect(screen.getByLabelText(/^Family/)).toBeChecked();
      expect(screen.getByLabelText(/^Work/)).not.toBeChecked();
    });

    it('submitting WITHOUT removing any included calendar POSTs directly with delete_excluded_calendar_events=false', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          calendars: SAMPLE_CALENDARS,
          included_calendar_ids: ['wmasman@gmail.com'],
          event_counts_by_calendar_id: { 'wmasman@gmail.com': 312 },
        }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);
      await screen.findByLabelText(/wmasman@gmail\.com/);

      fetchMock.mockResolvedValueOnce({ ok: true, json: async () => ({ ok: true }) });
      await userEvent.click(screen.getByRole('button', { name: 'Verbinden' }));

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
      const init = fetchMock.mock.calls[1]![1] as RequestInit;
      const body = JSON.parse(init.body as string) as {
        included_calendar_ids: string[];
        delete_excluded_calendar_events: boolean;
      };
      expect(body.delete_excluded_calendar_events).toBe(false);
      // No confirm dialog should have appeared
      expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument();
    });

    it('unchecking an INCLUDED calendar that has events shows the exclude-confirm dialog before posting', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          calendars: SAMPLE_CALENDARS,
          included_calendar_ids: ['wmasman@gmail.com', 'family-cal-id'],
          event_counts_by_calendar_id: {
            'wmasman@gmail.com': 312,
            'family-cal-id': 42,
          },
        }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);
      const familyCb = await screen.findByLabelText(/^Family/);

      await userEvent.click(familyCb);
      await userEvent.click(screen.getByRole('button', { name: 'Verbinden' }));

      const dialog = await screen.findByRole('alertdialog');
      expect(dialog).toBeInTheDocument();
      // Counts surface in the dialog
      expect(screen.getByText(/Family: 42 events/)).toBeInTheDocument();
      // Three buttons are present
      expect(
        screen.getByRole('button', { name: 'Ja, verwijder bestaande events' }),
      ).toBeInTheDocument();
      expect(
        screen.getByRole('button', { name: 'Nee, alleen niet meer ophalen' }),
      ).toBeInTheDocument();
      // POST has NOT been sent yet — only the GET fired
      expect(fetchMock).toHaveBeenCalledTimes(1);
    });

    it('picking "Ja, verwijder" POSTs with delete_excluded_calendar_events=true', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          calendars: SAMPLE_CALENDARS,
          included_calendar_ids: ['wmasman@gmail.com', 'family-cal-id'],
          event_counts_by_calendar_id: { 'family-cal-id': 42 },
        }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);
      await userEvent.click(await screen.findByLabelText(/^Family/));
      await userEvent.click(screen.getByRole('button', { name: 'Verbinden' }));
      await screen.findByRole('alertdialog');

      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ok: true, events_deleted: 42 }),
      });
      await userEvent.click(
        screen.getByRole('button', { name: 'Ja, verwijder bestaande events' }),
      );

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
      const init = fetchMock.mock.calls[1]![1] as RequestInit;
      const body = JSON.parse(init.body as string) as {
        delete_excluded_calendar_events: boolean;
      };
      expect(body.delete_excluded_calendar_events).toBe(true);
      await waitFor(() =>
        expect(routerMocks.push).toHaveBeenCalledWith('/settings'),
      );
    });

    it('picking "Nee, alleen niet meer ophalen" POSTs with delete_excluded_calendar_events=false', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          calendars: SAMPLE_CALENDARS,
          included_calendar_ids: ['wmasman@gmail.com', 'family-cal-id'],
          event_counts_by_calendar_id: { 'family-cal-id': 42 },
        }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);
      await userEvent.click(await screen.findByLabelText(/^Family/));
      await userEvent.click(screen.getByRole('button', { name: 'Verbinden' }));
      await screen.findByRole('alertdialog');

      fetchMock.mockResolvedValueOnce({ ok: true, json: async () => ({ ok: true }) });
      await userEvent.click(
        screen.getByRole('button', { name: 'Nee, alleen niet meer ophalen' }),
      );

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
      const init = fetchMock.mock.calls[1]![1] as RequestInit;
      const body = JSON.parse(init.body as string) as {
        delete_excluded_calendar_events: boolean;
      };
      expect(body.delete_excluded_calendar_events).toBe(false);
    });

    it('picking "Annuleren" in the confirm dialog returns to ready state without POSTing', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          calendars: SAMPLE_CALENDARS,
          included_calendar_ids: ['family-cal-id'],
          event_counts_by_calendar_id: { 'family-cal-id': 42 },
        }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);
      await userEvent.click(await screen.findByLabelText(/^Family/));
      await userEvent.click(screen.getByRole('button', { name: 'Verbinden' }));
      const dialog = await screen.findByRole('alertdialog');

      // Pick the dialog's Annuleren, not the form's.
      const within = await import('@testing-library/react').then((m) => m.within);
      await userEvent.click(within(dialog).getByRole('button', { name: 'Annuleren' }));

      await waitFor(() =>
        expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument(),
      );
      // Only the GET fired
      expect(fetchMock).toHaveBeenCalledTimes(1);
    });

    it('unchecking an INCLUDED calendar with ZERO events does NOT show the confirm dialog', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          calendars: SAMPLE_CALENDARS,
          included_calendar_ids: ['wmasman@gmail.com', 'work-cal-id'],
          event_counts_by_calendar_id: { 'wmasman@gmail.com': 312 }, // work-cal-id: implicit 0
        }),
      });

      render(<ChooseCalendarsForm connectionId={CONN_ID} />);
      await userEvent.click(await screen.findByLabelText(/^Work/));

      fetchMock.mockResolvedValueOnce({ ok: true, json: async () => ({ ok: true }) });
      await userEvent.click(screen.getByRole('button', { name: 'Verbinden' }));

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
      expect(screen.queryByRole('alertdialog')).not.toBeInTheDocument();
      const init = fetchMock.mock.calls[1]![1] as RequestInit;
      const body = JSON.parse(init.body as string) as {
        delete_excluded_calendar_events: boolean;
      };
      expect(body.delete_excluded_calendar_events).toBe(false);
    });
  });
});
