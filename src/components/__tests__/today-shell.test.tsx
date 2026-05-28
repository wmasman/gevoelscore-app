// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, describe, expect, it } from 'vitest';
import { cleanup, render, screen, within } from '@testing-library/react';
import { TodayShell } from '../today-shell';
import type { DayEntry } from '@/lib/domain/day-entry';
import { TAG_CATEGORIES } from '@/lib/domain/tag-category';

function sampleEntry(score: number): DayEntry {
  return {
    date: '2026-05-28',
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
    created_at: '2026-05-28T08:00:00.000Z',
    updated_at: '2026-05-28T08:00:00.000Z',
  };
}

describe('<TodayShell />', () => {
  afterEach(cleanup);

  it('renders the date heading in Dutch', () => {
    render(<TodayShell date="2026-05-27" entry={null} />);
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(
      /woensdag 27 mei 2026/i,
    );
  });

  it('renders a 10-item wheel column (1..10)', () => {
    render(<TodayShell date="2026-05-28" entry={null} />);
    const wheel = screen.getByRole('listbox', { name: /score/i });
    const items = within(wheel).getAllByRole('option');
    expect(items).toHaveLength(10);
    expect(items.map((el) => el.textContent)).toEqual([
      '1',
      '2',
      '3',
      '4',
      '5',
      '6',
      '7',
      '8',
      '9',
      '10',
    ]);
  });

  it('marks the centred value as "set" when an entry exists for that day', () => {
    render(<TodayShell date="2026-05-28" entry={sampleEntry(7)} />);
    const wheel = screen.getByRole('listbox', { name: /score/i });
    const set = within(wheel).getByRole('option', { selected: true });
    expect(set).toHaveTextContent('7');
  });

  it('marks the wheel as idle (no aria-selected) when no entry exists; centred value defaults to 5', () => {
    render(<TodayShell date="2026-05-28" entry={null} />);
    const wheel = screen.getByRole('listbox', { name: /score/i });
    // No item should be aria-selected in idle.
    const selected = within(wheel).queryAllByRole('option', { selected: true });
    expect(selected).toHaveLength(0);
    // Centre is 5 — exposed via data-default-score for Step 4's scroll-into-view.
    expect(wheel).toHaveAttribute('data-default-score', '5');
  });

  it('renders the 8 collapsed category-header buttons in the locked enum order', () => {
    render(<TodayShell date="2026-05-28" entry={null} />);
    for (const category of TAG_CATEGORIES) {
      // eslint-disable-next-line security/detect-non-literal-regexp -- test fixture iterating over a const-defined enum
      const header = screen.getByRole('button', { name: new RegExp(category, 'i') });
      expect(header).toHaveAttribute('aria-expanded', 'false');
    }
  });
});
