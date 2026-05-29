// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { DayEntry } from '@/lib/domain/day-entry';

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
});
