/** @vitest-environment jsdom */
// Step-2 Phase 2.D — TodayEventsRegion (today-card events section).

import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

const routerMocks = vi.hoisted(() => ({ refresh: vi.fn(), push: vi.fn() }));
vi.mock('next/navigation', () => ({ useRouter: () => routerMocks }));

import { TodayEventsRegion } from '../today-events-region';
import type { DirectusCalendarEventRow } from '@/lib/api/calendars';
import type { Tag } from '@/lib/domain/tag';

function evt(
  overrides: Partial<DirectusCalendarEventRow> = {},
): DirectusCalendarEventRow {
  return {
    id: 'evt-default',
    connection_id: 'conn-1',
    provider: 'google',
    provider_event_id: 'pg-default',
    source_calendar_id: 'cal-primary@gmail.com',
    recurrence_id: null,
    start_at: '2026-06-05T10:00:00Z',
    end_at: '2026-06-05T11:00:00Z',
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
    created_at: '2026-06-05T10:00:00Z',
    updated_at: '2026-06-05T10:00:00Z',
    ...overrides,
  };
}

function tag(id: string, label: string): Tag {
  return {
    id,
    label,
    category: 'activiteit',
    project_id: null,
    parent_episode_id: null,
    usage_count: 0,
    archived_at: null,
    created_at: '2026-06-01T00:00:00Z',
  };
}

let fetchSpy: ReturnType<typeof vi.fn>;

beforeEach(() => {
  routerMocks.refresh.mockReset();
  routerMocks.push.mockReset();
  fetchSpy = vi.fn();
  globalThis.fetch = fetchSpy as unknown as typeof fetch;
});
afterEach(() => cleanup());

describe('TodayEventsRegion', () => {
  it('test 79 (AC2.25): renders the included events passed in', () => {
    render(
      <TodayEventsRegion
        events={[evt({ id: 'a', title: 'Yoga met Anna' })]}
        tags={[]}
        episodes={[]}
      />,
    );

    expect(screen.getByText('Yoga met Anna')).toBeInTheDocument();
  });

  it('test 80 (AC2.25): drops events with included_as_context=false (caller may pass them; component filters)', () => {
    render(
      <TodayEventsRegion
        events={[
          evt({ id: 'in', title: 'Visible event', included_as_context: true }),
          evt({ id: 'out', title: 'Excluded event', included_as_context: false }),
        ]}
        tags={[]}
        episodes={[]}
      />,
    );

    expect(screen.getByText('Visible event')).toBeInTheDocument();
    expect(screen.queryByText('Excluded event')).not.toBeInTheDocument();
  });

  it('test 81 (AC2.25): sorts all-day first, then timed events ascending by start_at', () => {
    render(
      <TodayEventsRegion
        events={[
          evt({ id: 'c', title: 'Late', start_at: '2026-06-05T15:00:00Z' }),
          evt({ id: 'a', title: 'All-day thing', all_day: true }),
          evt({ id: 'b', title: 'Early', start_at: '2026-06-05T08:00:00Z' }),
        ]}
        tags={[]}
        episodes={[]}
      />,
    );

    const items = screen.getAllByRole('listitem');
    expect(items).toHaveLength(3);
    expect(within(items[0]!).getByText('All-day thing')).toBeInTheDocument();
    expect(within(items[1]!).getByText('Early')).toBeInTheDocument();
    expect(within(items[2]!).getByText('Late')).toBeInTheDocument();
  });

  it('test 82 (AC2.26): each row shows time + title; all-day shows "Hele dag"', () => {
    render(
      <TodayEventsRegion
        events={[
          evt({ id: 't', title: 'Standup', start_at: '2026-06-05T09:30:00Z' }),
          evt({ id: 'a', title: 'Verjaardag', all_day: true }),
        ]}
        tags={[]}
        episodes={[]}
      />,
    );

    expect(screen.getByText('Hele dag')).toBeInTheDocument();
    // Time is rendered in local time. We don't assert the literal HH:mm
    // because jsdom uses the host TZ — instead assert title presence and
    // that SOMETHING resembling a HH:mm sits next to it.
    expect(screen.getByText('Standup')).toBeInTheDocument();
    expect(screen.getByText(/\d{2}:\d{2}/)).toBeInTheDocument();
  });

  it('test 83 (AC2.26): linked-tag badge rendered when linked_tag_id set; absent otherwise', () => {
    render(
      <TodayEventsRegion
        events={[
          evt({ id: 'a', title: 'With tag', linked_tag_id: 'tag-1' }),
          evt({ id: 'b', title: 'No tag' }),
        ]}
        tags={[tag('tag-1', 'Fysio')]}
        episodes={[]}
      />,
    );

    expect(screen.getByText('Fysio')).toBeInTheDocument();
    // The "No tag" row has only one nested span at the badge slot — so
    // the badge text Fysio should appear once total.
    expect(screen.getAllByText('Fysio')).toHaveLength(1);
  });

  it('test 84 (AC2.28): empty events list → returns null (no DOM)', () => {
    const { container } = render(
      <TodayEventsRegion events={[]} tags={[]} episodes={[]} />,
    );

    expect(container.firstChild).toBeNull();
  });

  it('test 85 (AC2.27): 1-3 events → all rendered; no expand link', () => {
    render(
      <TodayEventsRegion
        events={[
          evt({ id: '1', title: 'One' }),
          evt({ id: '2', title: 'Two', start_at: '2026-06-05T11:00:00Z' }),
          evt({ id: '3', title: 'Three', start_at: '2026-06-05T12:00:00Z' }),
        ]}
        tags={[]}
        episodes={[]}
      />,
    );

    expect(screen.getAllByRole('listitem')).toHaveLength(3);
    expect(screen.queryByText(/meer$/)).not.toBeInTheDocument();
  });

  it('test 86 (AC2.27): 4+ events → first 3 rendered + "+ N meer" expand button', () => {
    render(
      <TodayEventsRegion
        events={[
          evt({ id: '1', title: 'One', start_at: '2026-06-05T08:00:00Z' }),
          evt({ id: '2', title: 'Two', start_at: '2026-06-05T09:00:00Z' }),
          evt({ id: '3', title: 'Three', start_at: '2026-06-05T10:00:00Z' }),
          evt({ id: '4', title: 'Four', start_at: '2026-06-05T11:00:00Z' }),
          evt({ id: '5', title: 'Five', start_at: '2026-06-05T12:00:00Z' }),
        ]}
        tags={[]}
        episodes={[]}
      />,
    );

    expect(screen.getAllByRole('listitem')).toHaveLength(3);
    expect(screen.getByRole('button', { name: '+ 2 meer' })).toBeInTheDocument();
    expect(screen.queryByText('Four')).not.toBeInTheDocument();
  });

  it('test 87 (AC2.27): clicking "+ N meer" expands inline to show all', async () => {
    const user = userEvent.setup();
    render(
      <TodayEventsRegion
        events={[
          evt({ id: '1', title: 'One', start_at: '2026-06-05T08:00:00Z' }),
          evt({ id: '2', title: 'Two', start_at: '2026-06-05T09:00:00Z' }),
          evt({ id: '3', title: 'Three', start_at: '2026-06-05T10:00:00Z' }),
          evt({ id: '4', title: 'Four', start_at: '2026-06-05T11:00:00Z' }),
        ]}
        tags={[]}
        episodes={[]}
      />,
    );

    await user.click(screen.getByRole('button', { name: '+ 1 meer' }));

    expect(screen.getAllByRole('listitem')).toHaveLength(4);
    expect(screen.getByText('Four')).toBeInTheDocument();
  });

  it('test 88 (AC2.29): tapping an event row opens the CalendarEventSheet', async () => {
    const user = userEvent.setup();
    render(
      <TodayEventsRegion
        events={[evt({ id: 'a', title: 'Fysiotherapie' })]}
        tags={[]}
        episodes={[]}
      />,
    );

    // Sheet is closed before tap.
    expect(screen.queryByLabelText('Event details')).not.toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /Fysiotherapie/ }));

    expect(screen.getByLabelText('Event details')).toBeInTheDocument();
  });

  it('test 89 (AC2.30): no client-side fetch on render — no useEffect HTTP', () => {
    render(
      <TodayEventsRegion
        events={[
          evt({ id: '1', title: 'One' }),
          evt({ id: '2', title: 'Two', start_at: '2026-06-05T11:00:00Z' }),
        ]}
        tags={[]}
        episodes={[]}
      />,
    );

    expect(fetchSpy).not.toHaveBeenCalled();
  });
});
