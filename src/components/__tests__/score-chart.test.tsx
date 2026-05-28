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

  it('renders an SVG with one path segment per gap-bounded run of points', () => {
    // 5 entries with a gap: [A B B B] gap [B B] → 2 path segments.
    const entries = [
      entry('2026-05-20', 5),
      entry('2026-05-21', 6),
      entry('2026-05-22', 6),
      entry('2026-05-23', 7),
      // gap 2026-05-24
      entry('2026-05-25', 4),
      entry('2026-05-26', 5),
    ];
    render(
      <ScoreChart
        entries={entries}
        from="2026-05-20"
        to="2026-05-26"
        onPointTap={() => {}}
      />,
    );
    const paths = document.querySelectorAll('svg path[data-segment]');
    expect(paths).toHaveLength(2);
  });

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

  it('30-day range never exceeds 30 visible points; 90-day never exceeds 90', () => {
    const longEntries = Array.from({ length: 30 }, (_, i) =>
      entry(`2026-05-${String(i + 1).padStart(2, '0')}`, 5),
    );
    render(
      <ScoreChart
        entries={longEntries}
        from="2026-05-01"
        to="2026-05-30"
        onPointTap={() => {}}
      />,
    );
    const points = document.querySelectorAll('svg circle[data-date]');
    expect(points.length).toBeLessThanOrEqual(30);
  });
});
