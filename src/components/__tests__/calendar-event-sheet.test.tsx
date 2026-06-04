/** @vitest-environment jsdom */
// Phase 1.E.3 — CalendarEventSheet (per-event detail BottomSheet).

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

import { CalendarEventSheet } from '../calendar-event-sheet';
import type { DirectusCalendarEventRow } from '@/lib/api/calendars';
import type { Tag } from '@/lib/domain/tag';
import type { Episode } from '@/lib/domain/episode';

const EVENT_ID = '550e8400-e29b-41d4-a716-446655440000';
const TAG_ID = '770e8400-e29b-41d4-a716-446655440002';
const EPISODE_ID = '880e8400-e29b-41d4-a716-446655440003';

function makeEvent(
  overrides: Partial<DirectusCalendarEventRow> = {},
): DirectusCalendarEventRow {
  return {
    id: EVENT_ID,
    connection_id: 'conn-1',
    provider: 'google',
    provider_event_id: 'evt-default',
    recurrence_id: null,
    start_at: '2026-06-04T10:00:00Z',
    end_at: '2026-06-04T11:00:00Z',
    all_day: false,
    title: 'Fysiotherapie',
    location: 'Praktijk Amstelveen',
    attendees_count: 1,
    declined: false,
    event_type: 'default',
    status: 'confirmed',
    transparency: 'opaque',
    organizer_is_self: false,
    ical_uid: 'evt@google.com',
    html_link: 'https://calendar.google.com/x',
    linked_tag_id: null,
    linked_episode_id: null,
    included_as_context: true,
    user_decision: 'auto',
    created_at: '2026-06-04T10:00:00Z',
    updated_at: '2026-06-04T10:00:00Z',
    ...overrides,
  };
}

function tag(overrides: Partial<Tag> = {}): Tag {
  return {
    id: TAG_ID,
    label: 'fysio',
    category: 'interventie',
    project_id: null,
    parent_episode_id: null,
    usage_count: 3,
    archived_at: null,
    created_at: '2026-05-01T00:00:00Z',
    ...overrides,
  };
}

function episode(overrides: Partial<Episode> = {}): Episode {
  return {
    id: EPISODE_ID,
    label: 'Coaching met Sarah',
    category: 'interventie',
    start_date: '2026-05-01',
    end_date: null,
    description: null,
    calendar_binding: null,
    archived_at: null,
    created_at: '2026-05-01T00:00:00Z',
    updated_at: '2026-05-01T00:00:00Z',
    ...overrides,
  };
}

const fetchMock = vi.fn();
beforeEach(() => {
  routerMocks.refresh.mockReset();
  routerMocks.push.mockReset();
  fetchMock.mockReset();
  globalThis.fetch = fetchMock as unknown as typeof fetch;
});
afterEach(() => cleanup());

describe('CalendarEventSheet', () => {
  describe('main view', () => {
    it('renders title, datetime, location, and the two link buttons + Sluit uit', () => {
      const onClose = vi.fn();
      render(
        <CalendarEventSheet
          event={makeEvent()}
          tags={[tag()]}
          episodes={[episode()]}
          open={true}
          onClose={onClose}
        />,
      );

      expect(screen.getByText('Fysiotherapie')).toBeInTheDocument();
      expect(screen.getByText(/Praktijk Amstelveen/)).toBeInTheDocument();
      // dateTime label rendered by formatEventDateTime helper; we just
      // check a substring that's stable regardless of timezone offset.
      expect(screen.getByText(/juni 2026/)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Koppel aan tag' })).toBeInTheDocument();
      expect(
        screen.getByRole('button', { name: 'Koppel aan periode' }),
      ).toBeInTheDocument();
      expect(
        screen.getByRole('button', { name: 'Sluit uit als context' }),
      ).toBeInTheDocument();
    });

    it('shows "Sluit hele serie uit" wording on a RECURRING event', () => {
      render(
        <CalendarEventSheet
          event={makeEvent({ recurrence_id: 'rec-yoga' })}
          tags={[]}
          episodes={[]}
          open={true}
          onClose={() => {}}
        />,
      );

      expect(
        screen.getByRole('button', { name: 'Sluit hele serie uit' }),
      ).toBeInTheDocument();
      expect(
        screen.queryByRole('button', { name: 'Sluit uit als context' }),
      ).not.toBeInTheDocument();
      expect(screen.getByText('Herhalend')).toBeInTheDocument();
    });

    it('shows the linked tag label inline when one is set', () => {
      render(
        <CalendarEventSheet
          event={makeEvent({ linked_tag_id: TAG_ID })}
          tags={[tag()]}
          episodes={[]}
          open={true}
          onClose={() => {}}
        />,
      );

      expect(screen.getByText('Tag: fysio')).toBeInTheDocument();
    });

    it('shows the linked episode label inline when one is set', () => {
      render(
        <CalendarEventSheet
          event={makeEvent({ linked_episode_id: EPISODE_ID })}
          tags={[]}
          episodes={[episode()]}
          open={true}
          onClose={() => {}}
        />,
      );

      expect(screen.getByText('Periode: Coaching met Sarah')).toBeInTheDocument();
    });
  });

  describe('tag picker', () => {
    it('opens the tag picker on "Koppel aan tag" click', async () => {
      render(
        <CalendarEventSheet
          event={makeEvent()}
          tags={[tag()]}
          episodes={[]}
          open={true}
          onClose={() => {}}
        />,
      );

      await userEvent.click(screen.getByRole('button', { name: 'Koppel aan tag' }));

      expect(screen.getByText('Kies een tag')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'fysio' })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Geen' })).toBeInTheDocument();
    });

    it('picking a tag PATCHes /api/calendars/events/[id] with linked_tag_id', async () => {
      fetchMock.mockResolvedValueOnce({ ok: true, json: async () => ({}) });
      const onClose = vi.fn();
      render(
        <CalendarEventSheet
          event={makeEvent()}
          tags={[tag()]}
          episodes={[]}
          open={true}
          onClose={onClose}
        />,
      );

      await userEvent.click(screen.getByRole('button', { name: 'Koppel aan tag' }));
      await userEvent.click(screen.getByRole('button', { name: 'fysio' }));

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
      const [url, init] = fetchMock.mock.calls[0]!;
      expect(url).toBe(`/api/calendars/events/${EVENT_ID}`);
      expect((init as RequestInit).method).toBe('PATCH');
      const body = JSON.parse((init as RequestInit).body as string);
      expect(body).toEqual({ linked_tag_id: TAG_ID });
      await waitFor(() => expect(routerMocks.refresh).toHaveBeenCalled());
      await waitFor(() => expect(onClose).toHaveBeenCalled());
    });

    it('clicking "Geen" unlinks (sends null)', async () => {
      fetchMock.mockResolvedValueOnce({ ok: true, json: async () => ({}) });
      render(
        <CalendarEventSheet
          event={makeEvent({ linked_tag_id: TAG_ID })}
          tags={[tag()]}
          episodes={[]}
          open={true}
          onClose={() => {}}
        />,
      );

      await userEvent.click(screen.getByRole('button', { name: 'Tag: fysio' }));
      await userEvent.click(screen.getByRole('button', { name: 'Geen' }));

      const body = JSON.parse((fetchMock.mock.calls[0]![1] as RequestInit).body as string);
      expect(body).toEqual({ linked_tag_id: null });
    });

    it('"Terug" returns to main view without POSTing', async () => {
      render(
        <CalendarEventSheet
          event={makeEvent()}
          tags={[tag()]}
          episodes={[]}
          open={true}
          onClose={() => {}}
        />,
      );

      await userEvent.click(screen.getByRole('button', { name: 'Koppel aan tag' }));
      await userEvent.click(screen.getByRole('button', { name: 'Terug' }));

      expect(screen.getByRole('button', { name: 'Koppel aan tag' })).toBeInTheDocument();
      expect(fetchMock).not.toHaveBeenCalled();
    });
  });

  describe('episode picker', () => {
    it('picking an episode PATCHes with linked_episode_id', async () => {
      fetchMock.mockResolvedValueOnce({ ok: true, json: async () => ({}) });
      render(
        <CalendarEventSheet
          event={makeEvent()}
          tags={[]}
          episodes={[episode()]}
          open={true}
          onClose={() => {}}
        />,
      );

      await userEvent.click(
        screen.getByRole('button', { name: 'Koppel aan periode' }),
      );
      await userEvent.click(
        screen.getByRole('button', { name: 'Coaching met Sarah' }),
      );

      const body = JSON.parse((fetchMock.mock.calls[0]![1] as RequestInit).body as string);
      expect(body).toEqual({ linked_episode_id: EPISODE_ID });
    });
  });

  describe('sluit-uit + re-include', () => {
    it('non-recurring sluit-uit PATCHes included_as_context=false', async () => {
      fetchMock.mockResolvedValueOnce({ ok: true, json: async () => ({}) });
      const onClose = vi.fn();
      render(
        <CalendarEventSheet
          event={makeEvent()}
          tags={[]}
          episodes={[]}
          open={true}
          onClose={onClose}
        />,
      );

      await userEvent.click(
        screen.getByRole('button', { name: 'Sluit uit als context' }),
      );

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
      const body = JSON.parse((fetchMock.mock.calls[0]![1] as RequestInit).body as string);
      expect(body).toEqual({ included_as_context: false });
      await waitFor(() => expect(onClose).toHaveBeenCalled());
    });

    it('recurring "Sluit hele serie uit" PATCHes included_as_context=false (route applies series rule)', async () => {
      fetchMock.mockResolvedValueOnce({ ok: true, json: async () => ({}) });
      render(
        <CalendarEventSheet
          event={makeEvent({ recurrence_id: 'rec-yoga' })}
          tags={[]}
          episodes={[]}
          open={true}
          onClose={() => {}}
        />,
      );

      await userEvent.click(
        screen.getByRole('button', { name: 'Sluit hele serie uit' }),
      );

      const body = JSON.parse((fetchMock.mock.calls[0]![1] as RequestInit).body as string);
      expect(body).toEqual({ included_as_context: false });
    });

    it('excluded non-recurring event shows "Weer meenemen"', () => {
      render(
        <CalendarEventSheet
          event={makeEvent({
            included_as_context: false,
            user_decision: 'user_excluded',
          })}
          tags={[]}
          episodes={[]}
          open={true}
          onClose={() => {}}
        />,
      );

      expect(screen.getByRole('button', { name: 'Weer meenemen' })).toBeInTheDocument();
      expect(
        screen.queryByRole('button', { name: 'Voeg hele serie weer toe' }),
      ).not.toBeInTheDocument();
    });

    it('excluded recurring event shows BOTH "Weer meenemen" and "Voeg hele serie weer toe"', () => {
      render(
        <CalendarEventSheet
          event={makeEvent({
            recurrence_id: 'rec-yoga',
            included_as_context: false,
            user_decision: 'user_excluded',
          })}
          tags={[]}
          episodes={[]}
          open={true}
          onClose={() => {}}
        />,
      );

      expect(screen.getByRole('button', { name: 'Weer meenemen' })).toBeInTheDocument();
      expect(
        screen.getByRole('button', { name: 'Voeg hele serie weer toe' }),
      ).toBeInTheDocument();
    });

    it('"Weer meenemen" PATCHes included_as_context=true', async () => {
      fetchMock.mockResolvedValueOnce({ ok: true, json: async () => ({}) });
      render(
        <CalendarEventSheet
          event={makeEvent({
            included_as_context: false,
            user_decision: 'user_excluded',
          })}
          tags={[]}
          episodes={[]}
          open={true}
          onClose={() => {}}
        />,
      );

      await userEvent.click(screen.getByRole('button', { name: 'Weer meenemen' }));

      const body = JSON.parse((fetchMock.mock.calls[0]![1] as RequestInit).body as string);
      expect(body).toEqual({ included_as_context: true });
    });

    it('"Voeg hele serie weer toe" POSTs to /include-series', async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ recurrence_id: 'rec-yoga', events_updated: 5 }),
      });
      const onClose = vi.fn();
      render(
        <CalendarEventSheet
          event={makeEvent({
            recurrence_id: 'rec-yoga',
            included_as_context: false,
            user_decision: 'user_excluded',
          })}
          tags={[]}
          episodes={[]}
          open={true}
          onClose={onClose}
        />,
      );

      await userEvent.click(
        screen.getByRole('button', { name: 'Voeg hele serie weer toe' }),
      );

      const [url, init] = fetchMock.mock.calls[0]!;
      expect(url).toBe(`/api/calendars/events/${EVENT_ID}/include-series`);
      expect((init as RequestInit).method).toBe('POST');
      await waitFor(() => expect(onClose).toHaveBeenCalled());
    });
  });

  describe('error handling', () => {
    it('PATCH failure shows actionError and leaves the sheet open', async () => {
      fetchMock.mockResolvedValueOnce({ ok: false, json: async () => ({}) });
      const onClose = vi.fn();
      render(
        <CalendarEventSheet
          event={makeEvent()}
          tags={[]}
          episodes={[]}
          open={true}
          onClose={onClose}
        />,
      );

      await userEvent.click(
        screen.getByRole('button', { name: 'Sluit uit als context' }),
      );

      expect(await screen.findByText('Actie lukte niet. Probeer opnieuw.')).toBeInTheDocument();
      expect(onClose).not.toHaveBeenCalled();
    });
  });

  describe('no copy contains em-dash', () => {
    it('no rendered text contains the em-dash character (per memory)', () => {
      const { container } = render(
        <CalendarEventSheet
          event={makeEvent({ recurrence_id: 'rec-yoga' })}
          tags={[tag()]}
          episodes={[episode()]}
          open={true}
          onClose={() => {}}
        />,
      );

      expect(container.textContent).not.toContain('—');
    });
  });
});
