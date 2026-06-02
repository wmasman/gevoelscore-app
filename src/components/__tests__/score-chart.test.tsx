// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { DayEntry } from '@/lib/domain/day-entry';
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
});
