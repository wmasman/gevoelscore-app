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
});
