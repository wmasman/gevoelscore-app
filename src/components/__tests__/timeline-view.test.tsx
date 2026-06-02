// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { DayEntry } from '@/lib/domain/day-entry';
import type { Episode } from '@/lib/domain/episode';
import type { Tag } from '@/lib/domain/tag';

// Mock the upsert hook so DayDetailSheet (rendered when a chart point is
// tapped) doesn't try to fetch. status='idle' keeps the sheet quiet.
vi.mock('@/hooks/use-day-entry-upsert', () => ({
  useDayEntryUpsert: () => ({
    save: vi.fn().mockResolvedValue(undefined),
    status: 'idle' as const,
    lastError: null,
  }),
}));

// Step-1: mock the episode-upsert + tag-link hooks so the embedded
// EpisodeFormSheet (rendered when a band is tapped) doesn't try to fetch.
vi.mock('@/hooks/use-episode-upsert', () => ({
  useEpisodeUpsert: () => ({
    create: vi.fn().mockResolvedValue(null),
    update: vi.fn().mockResolvedValue(null),
    archive: vi.fn().mockResolvedValue(null),
    status: 'idle' as const,
    lastError: null,
  }),
}));
vi.mock('@/hooks/use-tag-link-upsert', () => ({
  useTagLinkUpsert: () => ({
    createWithParent: vi.fn().mockResolvedValue(null),
    link: vi.fn().mockResolvedValue(null),
    unlink: vi.fn().mockResolvedValue(null),
    status: 'idle' as const,
    lastError: null,
  }),
}));

import { TimelineView } from '../timeline-view';

function entry(date: string, score: number): DayEntry {
  return {
    date,
    score: score as DayEntry['score'],
    note: null,
    tag_ids: [],
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

const INITIAL: DayEntry[] = [
  entry('2026-05-26', 5),
  entry('2026-05-27', 7),
  entry('2026-05-28', 6),
];

const TAGS: Tag[] = [];

describe('<TimelineView />', () => {
  beforeEach(() => {
    Element.prototype.scrollTo = vi.fn() as unknown as Element['scrollTo'];
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('renders the streak counter + chart with initial 30-day data', () => {
    render(<TimelineView today="2026-05-28" initialEntries={INITIAL} allTags={TAGS} />);

    // Streak of 3 consecutive days from the fixture.
    expect(screen.getByText(/3 dagen achter elkaar/i)).toBeInTheDocument();
    // Chart present (role=img).
    expect(screen.getByRole('img', { name: /score-tijdlijn/i })).toBeInTheDocument();
  });

  it('toggling 30 → 90 fires a fetch and replaces entries', async () => {
    const user = userEvent.setup();
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        entries: [
          ...INITIAL,
          entry('2026-03-01', 4),
          entry('2026-03-02', 5),
        ],
      }),
    });
    vi.stubGlobal('fetch', fetchMock);

    render(<TimelineView today="2026-05-28" initialEntries={INITIAL} allTags={TAGS} />);

    await user.click(screen.getByRole('radio', { name: /90 dagen/i }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalled());
    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringMatching(/\/api\/day-entries\?from=\d{4}-\d{2}-\d{2}&to=2026-05-28$/),
      expect.objectContaining({ credentials: 'same-origin' }),
    );
  });

  it('tapping a chart point opens the QuickEntryFlow popout for that date with isPastDay=true', async () => {
    const user = userEvent.setup();
    render(<TimelineView today="2026-05-28" initialEntries={INITIAL} allTags={TAGS} />);

    // No popout yet.
    expect(screen.queryByRole('dialog')).toBeNull();

    const point = screen.getByRole('button', { name: /2026-05-27/ });
    await user.click(point);

    // QuickEntryFlow renders via BottomSheet → portal → role="dialog"
    // with the app's aria-label.
    const dialog = await screen.findByRole('dialog');
    expect(dialog).toBeInTheDocument();
    // Past tint: bg-surface-muted on the dialog confirms isPastDay=true
    // was threaded through.
    expect(dialog.className).toMatch(/bg-surface-muted/);
  });

  it('given the initialEntries prop is replaced (after router.refresh), when re-rendered with range=30 active, then the chart reflects the new prop — no useState shadow', async () => {
    // Same shape as the TodayShell prop-driven test: server-rendered
    // data must flow through to display without local-state shadowing,
    // otherwise router.refresh() never moves the UI.
    //
    // Matcher is "score 9" (logged-day aria-label form) rather than the
    // bare date, because the 2026-06-02 gap-indicator feature renders a
    // tappable "{date}: geen score" gap-dot for every unlogged day in
    // the range — so the bare-date matcher would match the gap-dot
    // before the rerender, defeating the assertion's intent.
    const { rerender } = render(
      <TimelineView today="2026-05-28" initialEntries={INITIAL} allTags={TAGS} />,
    );
    // Initially: 2026-05-25 has only a gap-dot, no logged-score button.
    expect(
      screen.queryByRole('button', { name: /2026-05-25:\s*score\s+\d/ }),
    ).toBeNull();

    const next: DayEntry[] = [entry('2026-05-25', 9), ...INITIAL];
    rerender(<TimelineView today="2026-05-28" initialEntries={next} allTags={TAGS} />);

    await waitFor(() => {
      expect(
        screen.getByRole('button', { name: /2026-05-25:\s*score\s+9/ }),
      ).toBeInTheDocument();
    });
  });

  it('sheet shows the day\'s saved score in the score-circle slider', async () => {
    const user = userEvent.setup();
    render(<TimelineView today="2026-05-28" initialEntries={INITIAL} allTags={TAGS} />);

    await user.click(screen.getByRole('button', { name: /2026-05-27/ }));

    // QuickEntryFlow's ScoreCircle has role="slider" with aria-valuenow
    // set to the saved score (7 for the 2026-05-27 fixture entry).
    const slider = screen.getByRole('slider', { name: /score/i });
    expect(slider).toHaveAttribute('aria-valuenow', '7');
  });

  // -------------------------------------------------------------------------
  // Step-1 episode-overlay: per-category toggles + in-place EpisodeFormSheet
  // -------------------------------------------------------------------------

  function ep(overrides: Partial<Episode> = {}): Episode {
    return {
      id: 'ep-coaching',
      label: 'Coaching met Sarah',
      category: 'interventie',
      start_date: '2026-05-20',
      end_date: '2026-05-28',
      description: null,
      calendar_binding: null,
      archived_at: null,
      created_at: '2026-05-20T00:00:00.000Z',
      updated_at: '2026-05-20T00:00:00.000Z',
      ...overrides,
    };
  }

  describe('episode overlay', () => {
    it('renders the per-category toggle group with both checkboxes checked by default', () => {
      render(
        <TimelineView
          today="2026-05-28"
          initialEntries={INITIAL}
          allTags={TAGS}
          episodes={[ep()]}
        />,
      );
      const interventiesToggle = screen.getByRole('checkbox', {
        name: 'Interventies',
      });
      const periodesToggle = screen.getByRole('checkbox', {
        name: 'Periodes',
      });
      expect(interventiesToggle).toBeChecked();
      expect(periodesToggle).toBeChecked();
    });

    it('unchecking Interventies hides interventie bands on the chart', async () => {
      const user = userEvent.setup();
      render(
        <TimelineView
          today="2026-05-28"
          initialEntries={INITIAL}
          allTags={TAGS}
          episodes={[ep({ id: 'ep-X', category: 'interventie' })]}
        />,
      );
      // Initially the band is present.
      expect(
        document.querySelector('rect[data-episode-id="ep-X"]'),
      ).not.toBeNull();

      await user.click(screen.getByRole('checkbox', { name: 'Interventies' }));

      expect(
        document.querySelector('rect[data-episode-id="ep-X"]'),
      ).toBeNull();
    });

    it('the two toggles are independent', async () => {
      const user = userEvent.setup();
      render(
        <TimelineView
          today="2026-05-28"
          initialEntries={INITIAL}
          allTags={TAGS}
          episodes={[
            ep({ id: 'ep-A', category: 'interventie' }),
            ep({ id: 'ep-B', category: 'levensgebeurtenis' }),
          ]}
        />,
      );

      await user.click(screen.getByRole('checkbox', { name: 'Interventies' }));

      // Interventie band gone; levensgebeurtenis still there.
      expect(
        document.querySelector('rect[data-episode-id="ep-A"]'),
      ).toBeNull();
      expect(
        document.querySelector('rect[data-episode-id="ep-B"]'),
      ).not.toBeNull();
    });

    it('tapping a band opens the EpisodeFormSheet in edit mode for that episode', async () => {
      const user = userEvent.setup();
      render(
        <TimelineView
          today="2026-05-28"
          initialEntries={INITIAL}
          allTags={TAGS}
          episodes={[
            ep({ id: 'ep-X', label: 'Coaching met Sarah' }),
          ]}
        />,
      );

      // Sheet not yet open.
      expect(
        screen.queryByRole('dialog', { name: /periode bewerken/i }),
      ).toBeNull();

      const band = screen.getByRole('button', {
        name: /Coaching met Sarah/i,
      });
      await user.click(band);

      // The EpisodeFormSheet's BottomSheet has aria-label "Periode bewerken".
      expect(
        screen.getByRole('dialog', { name: /periode bewerken/i }),
      ).toBeInTheDocument();
      // Title is "Bewerk interventie".
      expect(
        screen.getByRole('heading', { name: /bewerk interventie/i }),
      ).toBeInTheDocument();
    });

    it('closing the EpisodeFormSheet unmounts it', async () => {
      const user = userEvent.setup();
      render(
        <TimelineView
          today="2026-05-28"
          initialEntries={INITIAL}
          allTags={TAGS}
          episodes={[ep({ id: 'ep-X' })]}
        />,
      );
      const band = screen.getByRole('button', { name: /Coaching met Sarah/i });
      await user.click(band);

      // Sheet open. Click the ✕ button inside the EpisodeFormSheet.
      const closeButton = screen.getByRole('button', { name: 'Sluit' });
      await user.click(closeButton);

      await waitFor(() =>
        expect(
          screen.queryByRole('heading', { name: /bewerk interventie/i }),
        ).toBeNull(),
      );
    });
  });
});
