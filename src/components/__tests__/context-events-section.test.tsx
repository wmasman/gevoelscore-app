/** @vitest-environment jsdom */
// Phase 1.E.4 — ContextEventsSection (Context tab events list).

import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

const routerMocks = vi.hoisted(() => ({ refresh: vi.fn(), push: vi.fn() }));
vi.mock('next/navigation', () => ({ useRouter: () => routerMocks }));

import { ContextEventsSection } from '../context-events-section';
import type { DirectusCalendarEventRow } from '@/lib/api/calendars';

function evt(overrides: Partial<DirectusCalendarEventRow> = {}): DirectusCalendarEventRow {
  return {
    id: 'evt-default',
    connection_id: 'conn-1',
    provider: 'google',
    provider_event_id: 'pg-default',
    source_calendar_id: 'cal-primary@gmail.com',
    recurrence_id: null,
    start_at: '2026-06-04T10:00:00Z',
    end_at: '2026-06-04T11:00:00Z',
    all_day: false,
    title: 'Fysiotherapie',
    location: null,
    attendees_count: 0,
    declined: false,
    event_type: 'default',
    status: 'confirmed',
    transparency: 'opaque',
    organizer_is_self: false,
    ical_uid: null,
    html_link: null,
    linked_tag_id: null,
    linked_episode_id: null,
    included_as_context: true,
    user_decision: 'auto',
    created_at: '2026-06-04T10:00:00Z',
    updated_at: '2026-06-04T10:00:00Z',
    ...overrides,
  };
}

beforeEach(() => {
  routerMocks.refresh.mockReset();
  routerMocks.push.mockReset();
});
afterEach(() => cleanup());

describe('ContextEventsSection', () => {
  it('returns null (no DOM) when events is empty', () => {
    const { container } = render(
      <ContextEventsSection events={[]} tags={[]} episodes={[]} />,
    );

    expect(container.firstChild).toBeNull();
  });

  it('renders the heading + included events', () => {
    render(
      <ContextEventsSection
        events={[evt({ id: 'a', title: 'Yoga met Anna' })]}
        tags={[]}
        episodes={[]}
      />,
    );

    expect(screen.getByText('Activiteiten')).toBeInTheDocument();
    expect(screen.getByText('Yoga met Anna')).toBeInTheDocument();
  });

  it('all-day events render before timed events', () => {
    render(
      <ContextEventsSection
        events={[
          evt({
            id: 'timed',
            title: 'Standup',
            start_at: '2026-06-04T09:00:00Z',
            all_day: false,
          }),
          evt({
            id: 'allday',
            title: 'Vakantie',
            start_at: '2026-06-04T00:00:00Z',
            all_day: true,
          }),
        ]}
        tags={[]}
        episodes={[]}
      />,
    );

    const labels = screen.getAllByRole('button').map((b) => b.textContent);
    expect(labels[0]).toContain('Vakantie');
    expect(labels[1]).toContain('Standup');
  });

  it('timed events sort by start_at ascending', () => {
    render(
      <ContextEventsSection
        events={[
          evt({ id: 'late', title: 'Avond', start_at: '2026-06-04T19:00:00Z' }),
          evt({ id: 'morn', title: 'Ochtend', start_at: '2026-06-04T08:00:00Z' }),
        ]}
        tags={[]}
        episodes={[]}
      />,
    );

    const labels = screen.getAllByRole('button').map((b) => b.textContent);
    expect(labels[0]).toContain('Ochtend');
    expect(labels[1]).toContain('Avond');
  });

  it('all-day rows show "Hele dag" instead of a time', () => {
    render(
      <ContextEventsSection
        events={[
          evt({ id: 'a', title: 'Vakantie', all_day: true, start_at: '2026-06-04T00:00:00Z' }),
        ]}
        tags={[]}
        episodes={[]}
      />,
    );

    expect(screen.getByText('Hele dag')).toBeInTheDocument();
  });

  it('recurring events show a recurrence icon', () => {
    render(
      <ContextEventsSection
        events={[evt({ id: 'rec', recurrence_id: 'rec-yoga' })]}
        tags={[]}
        episodes={[]}
      />,
    );

    expect(screen.getByText('↻')).toBeInTheDocument();
  });

  describe('excluded events + toggle', () => {
    it('hides excluded events when the toggle is OFF (default)', () => {
      render(
        <ContextEventsSection
          events={[
            evt({ id: 'incl', title: 'Included' }),
            evt({ id: 'excl', title: 'Excluded', included_as_context: false }),
          ]}
          tags={[]}
          episodes={[]}
        />,
      );

      expect(screen.getByText('Included')).toBeInTheDocument();
      expect(screen.queryByText('Excluded')).not.toBeInTheDocument();
    });

    it('shows excluded events when toggle is ON, with reduced opacity + suffix', async () => {
      render(
        <ContextEventsSection
          events={[
            evt({ id: 'incl', title: 'Included' }),
            evt({ id: 'excl', title: 'Excluded', included_as_context: false }),
          ]}
          tags={[]}
          episodes={[]}
        />,
      );

      await userEvent.click(screen.getByLabelText('Toon overgeslagen events'));

      expect(screen.getByText('Excluded')).toBeInTheDocument();
      expect(screen.getByText('(overgeslagen)')).toBeInTheDocument();
    });

    it('toggle is NOT rendered when no excluded events exist (cleaner default UX)', () => {
      render(
        <ContextEventsSection
          events={[evt({ id: 'incl', title: 'Included' })]}
          tags={[]}
          episodes={[]}
        />,
      );

      expect(screen.queryByText('Toon overgeslagen events')).not.toBeInTheDocument();
    });

    it('toggle IS rendered when all visible events are excluded (so the user can recover them)', () => {
      render(
        <ContextEventsSection
          events={[
            evt({ id: 'a', title: 'A', included_as_context: false }),
            evt({ id: 'b', title: 'B', included_as_context: false }),
          ]}
          tags={[]}
          episodes={[]}
        />,
      );

      // Heading + toggle render even when nothing is currently included
      expect(screen.getByText('Activiteiten')).toBeInTheDocument();
      expect(screen.getByLabelText('Toon overgeslagen events')).toBeInTheDocument();
    });
  });

  describe('linked badges', () => {
    it('shows linked tag label when an event has linked_tag_id', () => {
      render(
        <ContextEventsSection
          events={[evt({ id: 'a', linked_tag_id: 'tag-1' })]}
          tags={[
            {
              id: 'tag-1',
              label: 'fysio',
              category: 'interventie',
              project_id: null,
              parent_episode_id: null,
              usage_count: 0,
              archived_at: null,
              created_at: '2026-01-01T00:00:00Z',
            },
          ]}
          episodes={[]}
        />,
      );

      expect(screen.getByText(/→ fysio/)).toBeInTheDocument();
    });

    it('shows linked episode label when an event has linked_episode_id', () => {
      render(
        <ContextEventsSection
          events={[evt({ id: 'a', linked_episode_id: 'ep-1' })]}
          tags={[]}
          episodes={[
            {
              id: 'ep-1',
              label: 'Coaching met Sarah',
              category: 'interventie',
              start_date: '2026-05-01',
              end_date: null,
              description: null,
              calendar_binding: null,
              archived_at: null,
              created_at: '2026-05-01T00:00:00Z',
              updated_at: '2026-05-01T00:00:00Z',
            },
          ]}
        />,
      );

      expect(screen.getByText(/↳ Coaching met Sarah/)).toBeInTheDocument();
    });
  });

  describe('sheet integration', () => {
    it('clicking an event row opens CalendarEventSheet for that event', async () => {
      render(
        <ContextEventsSection
          events={[evt({ id: 'a', title: 'Fysiotherapie' })]}
          tags={[]}
          episodes={[]}
        />,
      );

      await userEvent.click(screen.getByRole('button', { name: /Fysiotherapie/ }));

      // Sheet content rendered (title appears twice: in the row + in the sheet)
      const titleMatches = screen.getAllByText('Fysiotherapie');
      expect(titleMatches.length).toBeGreaterThanOrEqual(2);
    });
  });
});
