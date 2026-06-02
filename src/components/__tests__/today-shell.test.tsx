// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { DayEntry } from '@/lib/domain/day-entry';
import type { Episode } from '@/lib/domain/episode';

// next/navigation must be mocked because ContextView (rendered when the
// Context tab is selected) mounts EpisodeFormSheet, whose useEpisodeUpsert
// hook calls useRouter() — that throws outside a Next.js app context.
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    refresh: vi.fn(),
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
    prefetch: vi.fn(),
  }),
}));

// QuickEntryFlow is the composite under test in its own file. Here we only
// care that TodayShell wires the right props through and reacts to its
// callbacks — so stub the component with a data-attribute shim.
vi.mock('@/components/lab/quick-entry-flow', () => ({
  QuickEntryFlow: (props: {
    date: string;
    open: boolean;
    startStep: 'score' | 'note' | 'tags';
    isPastDay: boolean;
    onClose: () => void;
    onComplete: () => void;
  }) => (
    <div
      data-testid="quick-entry-flow"
      data-date={props.date}
      data-open={props.open ? 'true' : 'false'}
      data-start-step={props.startStep}
      data-is-past-day={props.isPastDay ? 'true' : 'false'}
    >
      <button type="button" onClick={props.onClose}>
        mock-close
      </button>
      <button type="button" onClick={props.onComplete}>
        mock-complete
      </button>
    </div>
  ),
}));

import { TodayShell } from '../today-shell';

function entry(date: string, score: number, note: string | null = null, tag_ids: string[] = []): DayEntry {
  return {
    date,
    score: score as DayEntry['score'],
    note,
    tag_ids,
    sub_scores: null,
    sleep_hours: null,
    special_event: null,
    project_entry_ids: [],
    calendar_event_ids: [],
    garmin: null,
    health: null,
    weather: null,
    derived: null,
    created_at: `${date}T08:00:00.000Z`,
    updated_at: `${date}T08:00:00.000Z`,
  };
}

const PAST_ENTRIES: DayEntry[] = [
  entry('2026-05-19', 4, 'Eerste'),
  entry('2026-05-20', 5),
  entry('2026-05-21', 6, 'Wandeling'),
  entry('2026-05-22', 5),
  entry('2026-05-23', 7, 'Goede dag, energiek'),
  entry('2026-05-24', 6),
  entry('2026-05-25', 5),
  entry('2026-05-26', 4),
  entry('2026-05-27', 6, 'Iets meer gedaan'),
  entry('2026-05-28', 7),
];

describe('<TodayShell />', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => ({}) }),
    );
  });
  afterEach(() => {
    vi.unstubAllGlobals();
    cleanup();
  });

  it('given the entry prop is replaced (after router.refresh upstream), when re-rendered, then the today-card display reflects the new prop — no useState shadow', async () => {
    // Why this exists: previously TodayShell mirrored the server prop
    // into local state and refetched via GET on every dismiss. The
    // architecture changed: useDayEntryUpsert now calls router.refresh()
    // on success, the server component re-runs, and a new `entry` prop
    // arrives. If we shadow the prop with useState the new value is
    // ignored and the card stays stale — exactly the bug we set out
    // to remove. This test pins the contract.
    const { rerender } = render(
      <TodayShell
        date="2026-05-29"
        entry={entry('2026-05-29', 4, 'oude notitie', [])}
        allTags={[]}
        timelineEntries={[]}
      />,
    );
    expect(screen.getByRole('button', { name: /^gevoelscore:/i })).toHaveTextContent('4');

    rerender(
      <TodayShell
        date="2026-05-29"
        entry={entry('2026-05-29', 9, 'verse notitie', [])}
        allTags={[]}
        timelineEntries={[]}
      />,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /^gevoelscore:/i })).toHaveTextContent('9');
    });
  });

  it('given any state, when rendered, then the H1 shows the date in Dutch', () => {
    render(
      <TodayShell date="2026-05-29" entry={null} allTags={[]} timelineEntries={[]} />,
    );
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(
      /vrijdag 29 mei 2026/i,
    );
  });

  it('given an existing entry, when rendered, then the today-card shows the saved score / note / tag count and the sheet stays closed', () => {
    render(
      <TodayShell
        date="2026-05-29"
        entry={entry('2026-05-29', 7, 'Vandaag iets beter dan gister', [])}
        allTags={[]}
        timelineEntries={PAST_ENTRIES}
      />,
    );
    const sheet = screen.getByTestId('quick-entry-flow');
    expect(sheet.dataset.open).toBe('false');
    // The today-card's score region shows 7 (in addition to any score
    // appearances in past-day cards). Card itself is identified by region label.
    const scoreRegion = screen.getByRole('button', { name: /^gevoelscore:/i });
    expect(scoreRegion).toHaveTextContent('7');
  });

  it('given entry === null, when first rendered, then the sheet auto-opens at the score step', () => {
    render(
      <TodayShell date="2026-05-29" entry={null} allTags={[]} timelineEntries={[]} />,
    );
    const sheet = screen.getByTestId('quick-entry-flow');
    expect(sheet.dataset.open).toBe('true');
    expect(sheet.dataset.startStep).toBe('score');
    expect(sheet.dataset.isPastDay).toBe('false');
  });

  it('given the today-card score region is tapped, when clicked, then the sheet opens at the score step', async () => {
    const user = userEvent.setup();
    render(
      <TodayShell
        date="2026-05-29"
        entry={entry('2026-05-29', 7)}
        allTags={[]}
        timelineEntries={[]}
      />,
    );
    await user.click(screen.getByRole('button', { name: /^gevoelscore:/i }));
    const sheet = screen.getByTestId('quick-entry-flow');
    expect(sheet.dataset.open).toBe('true');
    expect(sheet.dataset.startStep).toBe('score');
  });

  it('given the today-card note region is tapped, when clicked, then the sheet opens at the note step', async () => {
    const user = userEvent.setup();
    render(
      <TodayShell
        date="2026-05-29"
        entry={entry('2026-05-29', 7)}
        allTags={[]}
        timelineEntries={[]}
      />,
    );
    await user.click(screen.getByRole('button', { name: /^notitie:/i }));
    const sheet = screen.getByTestId('quick-entry-flow');
    expect(sheet.dataset.open).toBe('true');
    expect(sheet.dataset.startStep).toBe('note');
  });

  it('given the today-card tags region is tapped, when clicked, then the sheet opens at the tags step', async () => {
    const user = userEvent.setup();
    render(
      <TodayShell
        date="2026-05-29"
        entry={entry('2026-05-29', 7)}
        allTags={[]}
        timelineEntries={[]}
      />,
    );
    await user.click(screen.getByRole('button', { name: /^tags:/i }));
    const sheet = screen.getByTestId('quick-entry-flow');
    expect(sheet.dataset.open).toBe('true');
    expect(sheet.dataset.startStep).toBe('tags');
  });

  it('given past entries, when rendered, then the "Vorige dagen" section shows the 3 most-recent days by default', () => {
    render(
      <TodayShell
        date="2026-05-29"
        entry={entry('2026-05-29', 7)}
        allTags={[]}
        timelineEntries={PAST_ENTRIES}
      />,
    );
    // Past-day cards are buttons grouped under "Vorige dagen". The 3 most
    // recent should be 28, 27, 26 (today is 29; entries are excluded for
    // today's date).
    const buttons = screen.getAllByRole('button', { name: /^vorige dag/i });
    expect(buttons).toHaveLength(3);
  });

  it('given "Toon meer" is tapped, when clicked, then the past-day list reveals up to 10 entries inline', async () => {
    const user = userEvent.setup();
    render(
      <TodayShell
        date="2026-05-29"
        entry={entry('2026-05-29', 7)}
        allTags={[]}
        timelineEntries={PAST_ENTRIES}
      />,
    );
    await user.click(screen.getByRole('button', { name: /toon meer/i }));
    const buttons = screen.getAllByRole('button', { name: /^vorige dag/i });
    // PAST_ENTRIES has 10 distinct dates; today is 2026-05-29 which doesn't
    // appear in the fixture, so 10 past-day cards become visible.
    expect(buttons.length).toBeGreaterThanOrEqual(9);
  });

  it('given a past-day card is tapped, when clicked, then the sheet opens for that date with isPastDay=true', async () => {
    const user = userEvent.setup();
    render(
      <TodayShell
        date="2026-05-29"
        entry={entry('2026-05-29', 7)}
        allTags={[]}
        timelineEntries={PAST_ENTRIES}
      />,
    );
    const buttons = screen.getAllByRole('button', { name: /^vorige dag/i });
    await user.click(buttons[0]!); // most-recent past day = 2026-05-28
    const sheet = screen.getByTestId('quick-entry-flow');
    expect(sheet.dataset.open).toBe('true');
    expect(sheet.dataset.isPastDay).toBe('true');
    expect(sheet.dataset.date).toBe('2026-05-28');
  });

  it('given the sheet fires onComplete, when handled, then the sheet closes', async () => {
    const user = userEvent.setup();
    render(
      <TodayShell date="2026-05-29" entry={null} allTags={[]} timelineEntries={[]} />,
    );
    // Sheet auto-opened. Fire onComplete via the stub.
    await user.click(screen.getByText('mock-complete'));
    const sheet = screen.getByTestId('quick-entry-flow');
    expect(sheet.dataset.open).toBe('false');
  });

  it('given the sheet fires onComplete, when handled, then the target today-card receives a one-shot pulse class', () => {
    vi.useFakeTimers();
    try {
      render(
        <TodayShell
          date="2026-05-29"
          entry={null}
          allTags={[]}
          timelineEntries={[]}
        />,
      );
      const todayCard = screen.getByTestId('today-card');
      expect(todayCard.dataset.pulsing).toBe('false');

      // fireEvent.click is synchronous — playing well with fake timers,
      // unlike userEvent which internally schedules tasks.
      act(() => {
        screen.getByText('mock-complete').click();
      });
      expect(todayCard.dataset.pulsing).toBe('true');

      act(() => {
        vi.advanceTimersByTime(200);
      });
      expect(todayCard.dataset.pulsing).toBe('false');
    } finally {
      vi.useRealTimers();
    }
  });

  it('given an existing entry, when the popout fires onClose (dismiss in edit mode), then the today-card pulses — dismiss IS completion when editing', () => {
    // Why: the pulse is the only end-of-interaction signal on the
    // today-card. In edit mode the user rarely taps "Klaar" (which
    // is the tags step's button); they change one field and dismiss.
    // Without this, an edit feels like nothing happened.
    vi.useFakeTimers();
    try {
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7, 'note', [])}
          allTags={[]}
          timelineEntries={[]}
        />,
      );
      const todayCard = screen.getByTestId('today-card');
      expect(todayCard.dataset.pulsing).toBe('false');

      // Open the popout by tapping a pencil — any region works; pick note.
      act(() => {
        screen.getByRole('button', { name: /^notitie:/i }).click();
      });

      // Dismiss via the stub's onClose. In edit mode this should pulse.
      act(() => {
        screen.getByText('mock-close').click();
      });
      expect(todayCard.dataset.pulsing).toBe('true');

      act(() => {
        vi.advanceTimersByTime(200);
      });
      expect(todayCard.dataset.pulsing).toBe('false');
    } finally {
      vi.useRealTimers();
    }
  });

  it('given entry === null, when the popout fires onClose (dismiss without ever committing), then the today-card does NOT pulse', () => {
    // The "dismiss = complete" rule only applies in edit mode. A
    // fresh-day dismiss without commit is the user backing out, not
    // a save signal — pulsing would lie.
    render(
      <TodayShell date="2026-05-29" entry={null} allTags={[]} timelineEntries={[]} />,
    );
    const todayCard = screen.getByTestId('today-card');
    expect(todayCard.dataset.pulsing).toBe('false');

    // Sheet auto-opened. Dismiss without commit.
    act(() => {
      screen.getByText('mock-close').click();
    });
    expect(todayCard.dataset.pulsing).toBe('false');
  });

  it('given the Tijdlijn tab is selected, when tapped, then the timeline view replaces the today-card', async () => {
    const user = userEvent.setup();
    render(
      <TodayShell
        date="2026-05-29"
        entry={entry('2026-05-29', 7)}
        allTags={[]}
        timelineEntries={PAST_ENTRIES}
      />,
    );
    await user.click(screen.getByRole('tab', { name: /tijdlijn/i }));
    // Timeline view is identified by its aria-label'd section + the
    // streak / range / view controls (no visible h2 — the active tab is
    // the heading).
    expect(screen.getByRole('region', { name: /tijdlijn/i })).toBeInTheDocument();
    expect(screen.getByRole('radio', { name: /30 dagen/i })).toBeInTheDocument();
  });

  // ===========================================================================
  // Context tab (v1.5, step-3)
  //
  // Tab order: Context / Vandaag / Tijdlijn. Vandaag is centre-positioned
  // so the daily-flow action stays thumb-balanced; Context (less-frequent
  // management) goes left, Tijdlijn (less-frequent review) goes right.
  // The Context tab today holds a Periodes section; v1.6 will add Calendar
  // bindings as a sibling section under the same tab.
  // ===========================================================================

  describe('Context tab', () => {
    it('renders three tabs in order: Context, Vandaag, Tijdlijn', () => {
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7)}
          allTags={[]}
          timelineEntries={PAST_ENTRIES}
        />,
      );

      const tabs = screen.getAllByRole('tab').map((t) => t.textContent);
      expect(tabs).toEqual(['Context', 'Vandaag', 'Tijdlijn']);
    });

    it('given the Context tab is tapped, the today-card is replaced by the ContextView', async () => {
      const user = userEvent.setup();
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7)}
          allTags={[]}
          timelineEntries={PAST_ENTRIES}
        />,
      );

      await user.click(screen.getByRole('tab', { name: /context/i }));

      // The today-card is gone, ContextView region is in.
      expect(screen.queryByTestId('today-card')).toBeNull();
      expect(screen.getByRole('region', { name: 'Context' })).toBeInTheDocument();
    });

    it('given Context is selected and episodes is empty, renders the Periodes h2 + empty-state line', async () => {
      const user = userEvent.setup();
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7)}
          allTags={[]}
          timelineEntries={PAST_ENTRIES}
          episodes={[]}
        />,
      );

      await user.click(screen.getByRole('tab', { name: /context/i }));

      // The Periodes section heading is always present inside Context,
      // even when there's nothing to list.
      expect(screen.getByRole('heading', { level: 2, name: 'Periodes' })).toBeInTheDocument();
      expect(screen.getByText('Nog geen periodes.')).toBeInTheDocument();
    });

    it('given Context is selected and an active interventie is in the list, renders the Interventies (actief) h3 sub-group', async () => {
      const user = userEvent.setup();
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7)}
          allTags={[]}
          timelineEntries={PAST_ENTRIES}
          episodes={[
            {
              id: 'ep-a',
              label: 'Coaching met Sarah',
              category: 'interventie',
              start_date: '2026-04-01',
              end_date: null,
              description: null,
              calendar_binding: null,
              archived_at: null,
              created_at: '2026-04-01T08:00:00.000Z',
              updated_at: '2026-04-01T08:00:00.000Z',
            },
          ]}
        />,
      );

      await user.click(screen.getByRole('tab', { name: /context/i }));

      expect(
        screen.getByRole('heading', { level: 3, name: 'Interventies (actief)' }),
      ).toBeInTheDocument();
      expect(screen.getByText('Coaching met Sarah')).toBeInTheDocument();
    });

    it('tapping Vandaag after Context restores the today-card (no regression)', async () => {
      const user = userEvent.setup();
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7)}
          allTags={[]}
          timelineEntries={PAST_ENTRIES}
        />,
      );

      await user.click(screen.getByRole('tab', { name: /context/i }));
      expect(screen.queryByTestId('today-card')).toBeNull();

      await user.click(screen.getByRole('tab', { name: /vandaag/i }));

      expect(screen.getByTestId('today-card')).toBeInTheDocument();
      expect(screen.queryByRole('region', { name: 'Context' })).toBeNull();
    });
  });

  // ===========================================================================
  // Today-card: ongoing-episodes region (lopend only, below Tags)
  // ===========================================================================

  function ep(overrides: Partial<Episode> = {}): Episode {
    return {
      id: 'ep-default',
      label: 'Coaching met Sarah',
      category: 'interventie',
      start_date: '2026-05-01',
      end_date: null,
      description: null,
      calendar_binding: null,
      archived_at: null,
      created_at: '2026-05-01T00:00:00.000Z',
      updated_at: '2026-05-01T00:00:00.000Z',
      ...overrides,
    };
  }

  describe('ongoing-episodes region', () => {
    it('does not render the region when no episodes are ongoing', () => {
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7)}
          allTags={[]}
          timelineEntries={PAST_ENTRIES}
          episodes={[]}
        />,
      );
      expect(
        screen.queryByRole('heading', { name: /lopend|loopt/i }),
      ).toBeNull();
    });

    it('renders a row for each ongoing episode (end_date=null only)', () => {
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7)}
          allTags={[]}
          timelineEntries={PAST_ENTRIES}
          episodes={[
            ep({ id: 'a', label: 'Coaching met Sarah', end_date: null }),
            ep({
              id: 'b',
              label: 'Citalopram',
              category: 'interventie',
              end_date: null,
            }),
          ]}
        />,
      );
      expect(screen.getByText('Coaching met Sarah')).toBeInTheDocument();
      expect(screen.getByText('Citalopram')).toBeInTheDocument();
    });

    it('does NOT render episodes with end_date set (not lopend)', () => {
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7)}
          allTags={[]}
          timelineEntries={PAST_ENTRIES}
          episodes={[
            ep({ id: 'a', label: 'Lopende coaching', end_date: null }),
            ep({
              id: 'b',
              label: 'Vakantie Texel',
              category: 'levensgebeurtenis',
              end_date: '2026-07-22',
            }),
          ]}
        />,
      );
      expect(screen.getByText('Lopende coaching')).toBeInTheDocument();
      expect(screen.queryByText('Vakantie Texel')).toBeNull();
    });

    it('does NOT render archived episodes even if end_date is null', () => {
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7)}
          allTags={[]}
          timelineEntries={PAST_ENTRIES}
          episodes={[
            ep({
              id: 'a',
              label: 'Oude coaching',
              end_date: null,
              archived_at: '2026-04-01T00:00:00.000Z',
            }),
          ]}
        />,
      );
      expect(screen.queryByText('Oude coaching')).toBeNull();
    });

    it('each row is a button with an aria-label describing the action', () => {
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7)}
          allTags={[]}
          timelineEntries={PAST_ENTRIES}
          episodes={[ep({ id: 'a', label: 'Coaching met Sarah' })]}
        />,
      );
      const button = screen.getByRole('button', {
        name: /Coaching met Sarah.*tik om te bewerken/i,
      });
      expect(button).toBeInTheDocument();
    });

    it('tapping a row opens the EpisodeFormSheet for that episode', async () => {
      const user = userEvent.setup();
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7)}
          allTags={[]}
          timelineEntries={PAST_ENTRIES}
          episodes={[ep({ id: 'a', label: 'Coaching met Sarah' })]}
        />,
      );

      // Sheet not yet open.
      expect(
        screen.queryByRole('heading', { name: /bewerk interventie/i }),
      ).toBeNull();

      const row = screen.getByRole('button', {
        name: /Coaching met Sarah.*tik om te bewerken/i,
      });
      await user.click(row);

      expect(
        screen.getByRole('heading', { name: /bewerk interventie/i }),
      ).toBeInTheDocument();
    });

    it('the region sits BELOW the Tags region inside the today-card', () => {
      render(
        <TodayShell
          date="2026-05-29"
          entry={entry('2026-05-29', 7)}
          allTags={[]}
          timelineEntries={PAST_ENTRIES}
          episodes={[ep({ id: 'a', label: 'Coaching met Sarah' })]}
        />,
      );
      const card = screen.getByTestId('today-card');
      const tagsButton = card.querySelector('button[aria-label^="Tags"]');
      const episodeButton = card.querySelector(
        'button[aria-label*="Coaching met Sarah"]',
      );
      expect(tagsButton).not.toBeNull();
      expect(episodeButton).not.toBeNull();
      // Document order: Tags comes before the ongoing-episode row.
      const cmp = tagsButton!.compareDocumentPosition(episodeButton!);
      expect(cmp & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    });
  });
});
