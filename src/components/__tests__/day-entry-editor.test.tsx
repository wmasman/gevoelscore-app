// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { DayEntry } from '@/lib/domain/day-entry';
import type { Tag } from '@/lib/domain/tag';

const hookMocks = vi.hoisted(() => ({
  save: vi.fn(),
}));

vi.mock('@/hooks/use-day-entry-upsert', () => ({
  useDayEntryUpsert: () => ({
    save: hookMocks.save,
    status: 'idle' as const,
    lastError: null,
  }),
}));

import { DayEntryEditor } from '../day-entry-editor';

function tag(id: string, label: string, category: Tag['category']): Tag {
  return {
    id,
    label,
    category,
    project_id: null,
    usage_count: 0,
    archived_at: null,
    created_at: '2026-01-01T00:00:00.000Z',
  };
}

const ALL_TAGS: Tag[] = [
  tag('m1', 'helder', 'mentaal'),
  tag('f1', 'moe', 'fysiek'),
];

const FILLED_ENTRY: DayEntry = {
  date: '2026-05-28',
  score: 7,
  note: 'goed',
  tag_ids: ['m1'],
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

describe('<DayEntryEditor />', () => {
  beforeEach(() => {
    hookMocks.save.mockReset();
    hookMocks.save.mockResolvedValue(undefined);
  });

  afterEach(cleanup);

  it('renders wheel + note + tag picker in order', () => {
    render(
      <DayEntryEditor
        date="2026-05-28"
        initialEntry={FILLED_ENTRY}
        allTags={ALL_TAGS}
      />,
    );

    const wheel = screen.getByRole('listbox', { name: /score/i });
    const textarea = screen.getByRole('textbox', { name: /notitie/i });
    const tagsHeading = screen.getByRole('heading', { level: 2, name: /tags/i });

    // DOM order check: wheel before textarea before tags section.
    const wheelIdx = Array.from(document.body.querySelectorAll('*')).indexOf(wheel);
    const textareaIdx = Array.from(document.body.querySelectorAll('*')).indexOf(textarea);
    const tagsIdx = Array.from(document.body.querySelectorAll('*')).indexOf(tagsHeading);
    expect(wheelIdx).toBeLessThan(textareaIdx);
    expect(textareaIdx).toBeLessThan(tagsIdx);
  });

  it('when initialEntry === null, note + tag headers are disabled', () => {
    render(
      <DayEntryEditor
        date="2026-05-28"
        initialEntry={null}
        allTags={ALL_TAGS}
      />,
    );

    expect(screen.getByRole('textbox', { name: /notitie/i })).toBeDisabled();
    // Every category header is a button; check the mentaal one is disabled.
    expect(screen.getByRole('button', { name: /mentaal/i })).toBeDisabled();
  });

  it('the wheel\'s first save enables note + tags without server re-fetch', async () => {
    const user = userEvent.setup();
    render(
      <DayEntryEditor
        date="2026-05-28"
        initialEntry={null}
        allTags={ALL_TAGS}
      />,
    );

    // Initially disabled.
    expect(screen.getByRole('textbox', { name: /notitie/i })).toBeDisabled();

    // Tap a score on the wheel → the composite should flip to editable.
    await user.click(screen.getByRole('option', { name: '7' }));

    expect(screen.getByRole('textbox', { name: /notitie/i })).not.toBeDisabled();
    expect(screen.getByRole('button', { name: /mentaal/i })).not.toBeDisabled();
  });
});
