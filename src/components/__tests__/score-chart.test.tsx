// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { DayEntry } from '@/lib/domain/day-entry';
import type { Episode } from '@/lib/domain/episode';
import type { Tag } from '@/lib/domain/tag';
import { ScoreChart } from '../score-chart';

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

describe('<ScoreChart />', () => {
  afterEach(cleanup);

  it('renders a tappable circle for each logged day', () => {
    const entries = [
      entry('2026-05-26', 5),
      entry('2026-05-27', 7),
      entry('2026-05-28', 6),
    ];
    render(
      <ScoreChart
        entries={entries}
        from="2026-05-26"
        to="2026-05-28"
        onPointTap={() => {}}
      />,
    );
    const points = screen.getAllByRole('button', { name: /score 5|score 6|score 7/i });
    expect(points).toHaveLength(3);
  });

  it('tapping a point fires onPointTap with that date', async () => {
    const user = userEvent.setup();
    const onPointTap = vi.fn();
    const entries = [entry('2026-05-27', 7), entry('2026-05-28', 6)];
    render(
      <ScoreChart
        entries={entries}
        from="2026-05-27"
        to="2026-05-28"
        onPointTap={onPointTap}
      />,
    );

    const point = screen.getByRole('button', { name: /2026-05-27/ });
    await user.click(point);

    expect(onPointTap).toHaveBeenCalledOnce();
    expect(onPointTap).toHaveBeenCalledWith('2026-05-27');
  });

  it('renders a smooth 7-day moving-average path (the primary visual) once ≥3 days are logged', () => {
    // 7 consecutive days → MA emits for days 3..7 (day 3 has 3-day window).
    const entries = Array.from({ length: 7 }, (_, i) =>
      entry(`2026-05-2${i}`, ((i % 5) + 4) as DayEntry['score']),
    );
    render(
      <ScoreChart
        entries={entries}
        from="2026-05-20"
        to="2026-05-26"
        onPointTap={() => {}}
      />,
    );
    const maPath = document.querySelector('svg path[data-line="ma"]');
    expect(maPath).not.toBeNull();
    // The MA line has its own d-attribute (not empty) — i.e. a real segment.
    expect(maPath!.getAttribute('d')!.length).toBeGreaterThan(0);
  });

  it('omits the MA path when fewer than 3 days are logged in the range', () => {
    const entries = [entry('2026-05-27', 5), entry('2026-05-28', 6)];
    render(
      <ScoreChart
        entries={entries}
        from="2026-05-27"
        to="2026-05-28"
        onPointTap={() => {}}
      />,
    );
    // The path element may exist but with no segment (empty d) OR not exist.
    const maPath = document.querySelector('svg path[data-line="ma"]');
    if (maPath !== null) {
      expect(maPath.getAttribute('d') ?? '').toBe('');
    }
  });

  it('adaptive Y-axis: when all scores fall in 6..8, the axis labels do NOT span 1..10', () => {
    const entries = [
      entry('2026-05-20', 6),
      entry('2026-05-21', 7),
      entry('2026-05-22', 8),
      entry('2026-05-23', 7),
      entry('2026-05-24', 6),
    ];
    render(
      <ScoreChart
        entries={entries}
        from="2026-05-20"
        to="2026-05-24"
        onPointTap={() => {}}
      />,
    );
    const labels = Array.from(document.querySelectorAll('svg text[data-axis="y"]')).map(
      (el) => el.textContent,
    );
    // Range 6..8 padded → roughly 5..9 (span ≥3 minimum). 1 must not appear.
    expect(labels).not.toContain('1');
    expect(labels).not.toContain('10');
    // At least one label inside the actual data range.
    expect(labels.some((l) => l === '6' || l === '7' || l === '8')).toBe(true);
  });

  it('adaptive Y-axis falls back to 1..10 when there are no entries', () => {
    render(
      <ScoreChart
        entries={[]}
        from="2026-05-20"
        to="2026-05-26"
        onPointTap={() => {}}
      />,
    );
    const labels = Array.from(document.querySelectorAll('svg text[data-axis="y"]')).map(
      (el) => el.textContent,
    );
    expect(labels).toContain('1');
    expect(labels).toContain('10');
  });

  // -------------------------------------------------------------------------
  // Gap indicator — added 2026-06-02 for features/timeline-gap-indicator
  // -------------------------------------------------------------------------

  describe('gap indicator for missing days', () => {
    it('renders one gap-dot per missing day in [from, to]', () => {
      // 3-day range, 1 logged day -> 2 gap-dots.
      render(
        <ScoreChart
          entries={[entry('2026-05-27', 6)]}
          from="2026-05-26"
          to="2026-05-28"
          onPointTap={() => {}}
        />,
      );
      const gaps = screen.getAllByRole('button', { name: /geen score/i });
      expect(gaps).toHaveLength(2);
    });

    it('renders no gap-dots when every day in range is logged', () => {
      render(
        <ScoreChart
          entries={[
            entry('2026-05-26', 5),
            entry('2026-05-27', 7),
            entry('2026-05-28', 6),
          ]}
          from="2026-05-26"
          to="2026-05-28"
          onPointTap={() => {}}
        />,
      );
      expect(screen.queryAllByRole('button', { name: /geen score/i })).toHaveLength(0);
    });

    it('renders a gap-dot for every day in range when no days are logged', () => {
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-26"
          to="2026-05-28"
          onPointTap={() => {}}
        />,
      );
      expect(screen.getAllByRole('button', { name: /geen score/i })).toHaveLength(3);
    });

    it('uses the exact aria-label form "{date}: geen score"', () => {
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-27"
          to="2026-05-27"
          onPointTap={() => {}}
        />,
      );
      expect(
        screen.getByRole('button', { name: '2026-05-27: geen score' }),
      ).toBeInTheDocument();
    });

    it('clicking a gap-dot fires onPointTap with that missing date', async () => {
      const user = userEvent.setup();
      const onPointTap = vi.fn();
      render(
        <ScoreChart
          entries={[entry('2026-05-27', 7)]}
          from="2026-05-26"
          to="2026-05-28"
          onPointTap={onPointTap}
        />,
      );
      await user.click(screen.getByRole('button', { name: '2026-05-26: geen score' }));
      expect(onPointTap).toHaveBeenCalledWith('2026-05-26');
    });

    it('Enter key on a focused gap-dot fires onPointTap (keyboard parity with logged points)', async () => {
      const user = userEvent.setup();
      const onPointTap = vi.fn();
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-27"
          to="2026-05-27"
          onPointTap={onPointTap}
        />,
      );
      const gap = screen.getByRole('button', { name: '2026-05-27: geen score' });
      gap.focus();
      await user.keyboard('{Enter}');
      expect(onPointTap).toHaveBeenCalledWith('2026-05-27');
    });

    it('does not render visible "geen score" text — the label lives only in aria-label', () => {
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-27"
          to="2026-05-27"
          onPointTap={() => {}}
        />,
      );
      // The accessible name comes via aria-label; no text node should
      // expose the words to a sighted user.
      expect(screen.queryByText(/geen score/i)).toBeNull();
    });

    it('positions the gap-dot near the chart bottom (above the x-axis baseline)', () => {
      // PADDING_TOP = 12, SVG_HEIGHT = 200, PADDING_BOTTOM = 24, so
      // chartH = 164 and the dot's cy should be 12 + 164 - 3 = 173.
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-27"
          to="2026-05-27"
          onPointTap={() => {}}
        />,
      );
      // Find the visible gap-dot — the 3-px radius one inside the
      // role=button group, not the 12-px transparent hit target.
      const dots = Array.from(
        document.querySelectorAll('svg circle[r="3"][fill="none"]'),
      );
      expect(dots.length).toBe(1);
      expect(dots[0]!.getAttribute('cy')).toBe('173');
    });

    it('does not inflate the existing "tappable circle per logged day" count', () => {
      // Regression: the original test counts buttons matching /score \d/i.
      // Gap-dots use "geen score" so they must NOT match that pattern.
      render(
        <ScoreChart
          entries={[entry('2026-05-27', 6)]}
          from="2026-05-26"
          to="2026-05-28"
          onPointTap={() => {}}
        />,
      );
      const loggedPoints = screen.getAllByRole('button', { name: /score \d/i });
      expect(loggedPoints).toHaveLength(1);
    });
  });

  // -------------------------------------------------------------------------
  // Episode-overlay — added 2026-06-02 for features/timeline-episode-overlay
  // -------------------------------------------------------------------------

  function ep(overrides: Partial<Episode> = {}): Episode {
    return {
      id: 'ep-coaching',
      label: 'Coaching met Sarah',
      category: 'interventie',
      start_date: '2026-05-05',
      end_date: '2026-05-15',
      description: null,
      calendar_binding: null,
      archived_at: null,
      created_at: '2026-05-05T00:00:00.000Z',
      updated_at: '2026-05-05T00:00:00.000Z',
      ...overrides,
    };
  }

  function tag(overrides: Partial<Tag> = {}): Tag {
    return {
      id: 'tag-default',
      label: 'pacing',
      category: 'mentaal',
      project_id: null,
      parent_episode_id: null,
      usage_count: 0,
      archived_at: null,
      created_at: '2026-05-01T00:00:00.000Z',
      ...overrides,
    };
  }

  function svgEl(): SVGSVGElement {
    return screen.getByRole('img', {
      name: /score-tijdlijn/i,
    }) as unknown as SVGSVGElement;
  }

  describe('episode bands on the line chart', () => {
    it('regression: with no episodes prop, no <rect data-episode-id> is rendered', () => {
      render(
        <ScoreChart
          entries={[entry('2026-05-10', 6)]}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={() => {}}
        />,
      );
      expect(document.querySelectorAll('rect[data-episode-id]')).toHaveLength(0);
    });

    it('regression: with no episodes prop, the SVG viewBox height is 200 (unchanged)', () => {
      render(
        <ScoreChart
          entries={[entry('2026-05-10', 6)]}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={() => {}}
        />,
      );
      expect(svgEl().getAttribute('viewBox')).toBe('0 0 600 200');
    });

    it('renders one <rect data-episode-id="X"> when one episode overlaps the range', () => {
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={() => {}}
          episodes={[ep({ id: 'ep-X' })]}
        />,
      );
      const rect = document.querySelector('rect[data-episode-id="ep-X"]');
      expect(rect).not.toBeNull();
    });

    it('extends the SVG height when bands are present', () => {
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={() => {}}
          episodes={[ep()]}
        />,
      );
      const vb = svgEl().getAttribute('viewBox')!.split(' ');
      const h = Number(vb[3]);
      expect(h).toBeGreaterThan(200);
    });

    it('stacks two concurrent episodes into two rows; SVG_HEIGHT grows accordingly', () => {
      const a = ep({
        id: 'ep-A',
        start_date: '2026-05-01',
        end_date: '2026-05-15',
        category: 'interventie',
      });
      const b = ep({
        id: 'ep-B',
        start_date: '2026-05-10',
        end_date: '2026-05-20',
        category: 'levensgebeurtenis',
      });
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={() => {}}
          episodes={[a, b]}
        />,
      );
      const rects = document.querySelectorAll('rect[data-episode-id]');
      expect(rects).toHaveLength(2);
      // Two rows → both bands have distinct y attributes.
      const ys = new Set(Array.from(rects).map((r) => r.getAttribute('y')));
      expect(ys.size).toBe(2);
    });

    it('each band has role=button and an aria-label naming the episode + range', () => {
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={() => {}}
          episodes={[
            ep({
              id: 'ep-X',
              label: 'Coaching met Sarah',
              start_date: '2026-05-05',
              end_date: '2026-05-15',
            }),
          ]}
        />,
      );
      const band = screen.getByRole('button', {
        name: /Coaching met Sarah.*tik om te bewerken/i,
      });
      expect(band).toBeInTheDocument();
    });

    it('clicking a band fires onEpisodeTap with the episode', async () => {
      const user = userEvent.setup();
      const onEpisodeTap = vi.fn();
      const episode = ep({ id: 'ep-X', label: 'Coaching met Sarah' });
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={() => {}}
          onEpisodeTap={onEpisodeTap}
          episodes={[episode]}
        />,
      );
      await user.click(
        screen.getByRole('button', { name: /Coaching met Sarah/i }),
      );
      expect(onEpisodeTap).toHaveBeenCalledTimes(1);
      expect(onEpisodeTap.mock.calls[0]![0]).toMatchObject({ id: 'ep-X' });
    });

    it('Enter on a focused band fires onEpisodeTap (keyboard parity)', async () => {
      const user = userEvent.setup();
      const onEpisodeTap = vi.fn();
      const episode = ep({ id: 'ep-X' });
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={() => {}}
          onEpisodeTap={onEpisodeTap}
          episodes={[episode]}
        />,
      );
      const band = screen.getByRole('button', { name: /Coaching met Sarah/i });
      band.focus();
      await user.keyboard('{Enter}');
      expect(onEpisodeTap).toHaveBeenCalledTimes(1);
    });

    it('renders a linked-tag dot on the band when a tag with parent_episode_id matches', () => {
      render(
        <ScoreChart
          entries={[entry('2026-05-10', 6) as DayEntry & { tag_ids: string[] }]
            .map((e) => ({ ...e, tag_ids: ['tag-coach-1'] }))}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={() => {}}
          episodes={[ep({ id: 'ep-X' })]}
          allTags={[
            tag({ id: 'tag-coach-1', parent_episode_id: 'ep-X' }),
          ]}
        />,
      );
      const dot = document.querySelector(
        'circle[data-tag-id="tag-coach-1"][data-episode-id="ep-X"]',
      );
      expect(dot).not.toBeNull();
    });

    it('clicking a linked-tag dot fires onPointTap with the date', async () => {
      const user = userEvent.setup();
      const onPointTap = vi.fn();
      const dayEntry: DayEntry = {
        ...entry('2026-05-10', 6),
        tag_ids: ['tag-coach-1'],
      };
      render(
        <ScoreChart
          entries={[dayEntry]}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={onPointTap}
          episodes={[ep({ id: 'ep-X' })]}
          allTags={[
            tag({ id: 'tag-coach-1', label: 'sessie', parent_episode_id: 'ep-X' }),
          ]}
        />,
      );
      const dotButton = screen.getByRole('button', {
        name: /sessie.*Coaching met Sarah/i,
      });
      await user.click(dotButton);
      expect(onPointTap).toHaveBeenCalledWith('2026-05-10');
    });

    it('category filter: interventie=false hides interventie bands AND their linked dots', () => {
      const dayEntry: DayEntry = {
        ...entry('2026-05-10', 6),
        tag_ids: ['tag-coach-1'],
      };
      render(
        <ScoreChart
          entries={[dayEntry]}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={() => {}}
          episodes={[
            ep({ id: 'ep-X', category: 'interventie' }),
            ep({ id: 'ep-Y', category: 'levensgebeurtenis' }),
          ]}
          allTags={[
            tag({ id: 'tag-coach-1', parent_episode_id: 'ep-X' }),
          ]}
          categoriesVisible={{ interventie: false, levensgebeurtenis: true }}
        />,
      );
      // ep-X (interventie) is gone, ep-Y (levensgebeurtenis) stays.
      expect(
        document.querySelector('rect[data-episode-id="ep-X"]'),
      ).toBeNull();
      expect(
        document.querySelector('rect[data-episode-id="ep-Y"]'),
      ).not.toBeNull();
      // Linked dot for ep-X is gone too.
      expect(
        document.querySelector('circle[data-tag-id="tag-coach-1"]'),
      ).toBeNull();
    });

    it('when all bands are filtered out, SVG_HEIGHT collapses back to 200', () => {
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={() => {}}
          episodes={[ep()]}
          categoriesVisible={{ interventie: false, levensgebeurtenis: false }}
        />,
      );
      expect(svgEl().getAttribute('viewBox')).toBe('0 0 600 200');
    });

    it('episode with end_date=null extends the band to the chart right edge', () => {
      render(
        <ScoreChart
          entries={[]}
          from="2026-05-01"
          to="2026-05-31"
          onPointTap={() => {}}
          episodes={[
            ep({ id: 'ep-X', start_date: '2026-05-15', end_date: null }),
          ]}
        />,
      );
      const rect = document.querySelector('rect[data-episode-id="ep-X"]')!;
      // x + width should reach the chart's right edge (SVG_WIDTH - PADDING_RIGHT).
      const x = Number(rect.getAttribute('x'));
      const width = Number(rect.getAttribute('width'));
      // SVG_WIDTH=600, PADDING_RIGHT=12 → right edge is at 588.
      expect(Math.round(x + width)).toBe(588);
    });
  });
});
