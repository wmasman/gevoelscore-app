// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, within } from '@testing-library/react';
import { TodayShell } from '../today-shell';
import type { DayEntry } from '@/lib/domain/day-entry';
import { TAG_CATEGORIES } from '@/lib/domain/tag-category';

// The wheel embedded in TodayShell uses useDayEntryUpsert → fetch. We
// don't exercise interactions here (score-wheel.test.tsx covers that);
// just stub fetch so the render path is clean.

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

  it('renders the date heading in Dutch', () => {
    render(<TodayShell date="2026-05-27" entry={null} />);
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(
      /woensdag 27 mei 2026/i,
    );
  });

  it('composes the ScoreWheel — passes initialScore from entry', () => {
    render(<TodayShell date="2026-05-28" entry={sampleEntry(7)} />);
    const wheel = screen.getByRole('listbox', { name: /score/i });
    expect(wheel).toHaveAttribute('data-phase', 'set');
    const selected = within(wheel).getByRole('option', { selected: true });
    expect(selected).toHaveTextContent('7');
  });

  it('composes the ScoreWheel — null entry yields idle phase', () => {
    render(<TodayShell date="2026-05-28" entry={null} />);
    const wheel = screen.getByRole('listbox', { name: /score/i });
    expect(wheel).toHaveAttribute('data-phase', 'idle');
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
