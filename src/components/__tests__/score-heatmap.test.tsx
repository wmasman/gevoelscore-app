// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { DayEntry } from '@/lib/domain/day-entry';
import { ScoreHeatmap } from '../score-heatmap';

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

describe('<ScoreHeatmap />', () => {
  afterEach(cleanup);

  it('renders a tappable cell for each day in the [from, to] range', () => {
    render(
      <ScoreHeatmap
        entries={[
          entry('2026-05-26', 5),
          entry('2026-05-27', 7),
          entry('2026-05-28', 6),
        ]}
        from="2026-05-26"
        to="2026-05-28"
        onCellTap={() => {}}
      />,
    );
    expect(screen.getByRole('button', { name: /2026-05-26/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /2026-05-27/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /2026-05-28/i })).toBeInTheDocument();
  });

  it('missing days render as cells too but their aria-label indicates "geen score"', () => {
    render(
      <ScoreHeatmap
        entries={[entry('2026-05-26', 5), entry('2026-05-28', 6)]}
        from="2026-05-26"
        to="2026-05-28"
        onCellTap={() => {}}
      />,
    );
    // 27 had no entry — label should say "geen score" (aligned with
    // the line chart's gap-indicator copy, 2026-06-02).
    const missing = screen.getByRole('button', { name: /2026-05-27.*geen score/i });
    expect(missing).toBeInTheDocument();
  });

  it('tapping a cell fires onCellTap with that date (logged OR missing)', async () => {
    const user = userEvent.setup();
    const onCellTap = vi.fn();
    render(
      <ScoreHeatmap
        entries={[entry('2026-05-27', 7)]}
        from="2026-05-26"
        to="2026-05-28"
        onCellTap={onCellTap}
      />,
    );
    await user.click(screen.getByRole('button', { name: /2026-05-26.*geen score/i }));
    expect(onCellTap).toHaveBeenCalledWith('2026-05-26');
  });

  it('higher scores produce visually stronger cells (data-score attribute is present for visual regression)', () => {
    render(
      <ScoreHeatmap
        entries={[entry('2026-05-26', 2), entry('2026-05-27', 9)]}
        from="2026-05-26"
        to="2026-05-27"
        onCellTap={() => {}}
      />,
    );
    const low = screen.getByRole('button', { name: /2026-05-26/ });
    const high = screen.getByRole('button', { name: /2026-05-27/ });
    expect(low.getAttribute('data-score')).toBe('2');
    expect(high.getAttribute('data-score')).toBe('9');
  });

  it('lays out cells in a 7-column week grid (one row per ISO week)', () => {
    // 2026-05-25 is Monday. Range [05-25 .. 05-31] is exactly one week.
    const entries = Array.from({ length: 7 }, (_, i) =>
      entry(`2026-05-${25 + i}`, ((i % 5) + 4) as DayEntry['score']),
    );
    render(
      <ScoreHeatmap
        entries={entries}
        from="2026-05-25"
        to="2026-05-31"
        onCellTap={() => {}}
      />,
    );
    const grid = screen.getByRole('grid');
    // 7 day-of-week column headers (Ma..Zo) inside the row.
    const cols = grid.querySelectorAll('[role="columnheader"]');
    expect(cols).toHaveLength(7);
  });
});
