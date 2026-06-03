/** @vitest-environment jsdom */
import '@testing-library/jest-dom/vitest';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { DayEntry } from '@/lib/domain/day-entry';
import type { Episode } from '@/lib/domain/episode';
import type { Tag } from '@/lib/domain/tag';

// Mock TagFormSheet so the section test focuses on list-rendering +
// row-tap behaviour, not the form internals.
const sheetMock = vi.hoisted(() => ({
  rendered: vi.fn(),
}));
vi.mock('../tag-form-sheet', () => ({
  TagFormSheet: (props: {
    tag: Tag;
    open: boolean;
    onClose: () => void;
  }) => {
    sheetMock.rendered(props);
    return props.open ? (
      <div
        data-testid="tag-form-sheet"
        data-tag-id={props.tag.id}
        data-tag-label={props.tag.label}
      />
    ) : null;
  },
}));

import { TagManagementSection } from '../tag-management-section';

function tag(overrides: Partial<Tag> = {}): Tag {
  return {
    id: 'tag-default',
    label: 'pacing',
    category: 'mentaal',
    project_id: null,
    parent_episode_id: null,
    usage_count: 3,
    archived_at: null,
    created_at: '2026-05-01T00:00:00.000Z',
    ...overrides,
  };
}

function ep(overrides: Partial<Episode> = {}): Episode {
  return {
    id: 'ep-default',
    label: 'Coaching met Sarah',
    category: 'interventie',
    start_date: '2026-05-01',
    end_date: null,
    description: null,
    calendar_binding: null,
    archived_at: null,
    created_at: '2026-05-01T00:00:00.000Z',
    updated_at: '2026-05-01T00:00:00.000Z',
    ...overrides,
  };
}

function entry(overrides: Partial<DayEntry> = {}): DayEntry {
  return {
    date: '2026-05-30',
    score: 6 as DayEntry['score'],
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
    created_at: '2026-05-30T08:00:00.000Z',
    updated_at: '2026-05-30T08:00:00.000Z',
    ...overrides,
  };
}

afterEach(() => {
  sheetMock.rendered.mockReset();
  cleanup();
});

describe('<TagManagementSection />', () => {
  it('renders the Tag-beheer h2 heading', () => {
    render(
      <TagManagementSection tags={[]} episodes={[]} timelineEntries={[]} />,
    );

    expect(
      screen.getByRole('heading', { level: 2, name: 'Tag-beheer' }),
    ).toBeInTheDocument();
  });

  it('renders the empty-corpus line when there are no non-archived tags', () => {
    render(
      <TagManagementSection
        tags={[tag({ archived_at: '2026-05-01T00:00:00.000Z' })]}
        episodes={[]}
        timelineEntries={[]}
      />,
    );

    expect(
      screen.getByText('Geen tags. Tags maak je in het Vandaag-scherm.'),
    ).toBeInTheDocument();
  });

  it('groups tags by category in the canonical order (mentaal first)', () => {
    const tags = [
      tag({ id: 'f1', label: 'hoofdpijn', category: 'fysiek' }),
      tag({ id: 'm1', label: 'pacing', category: 'mentaal' }),
    ];
    render(
      <TagManagementSection
        tags={tags}
        episodes={[]}
        timelineEntries={[]}
      />,
    );

    const headings = screen.getAllByRole('heading', { level: 3 });
    const headingNames = headings.map((h) => h.textContent);
    // Mentaal comes BEFORE Fysiek in the canonical order.
    expect(headingNames.indexOf('Mentaal')).toBeLessThan(
      headingNames.indexOf('Fysiek'),
    );
  });

  it('sorts within category by last-used desc; never-used tags sink to bottom', () => {
    const tags = [
      tag({ id: 'never', label: 'never-used', category: 'mentaal' }),
      tag({ id: 'old', label: 'old', category: 'mentaal' }),
      tag({ id: 'recent', label: 'recent', category: 'mentaal' }),
    ];
    const entries = [
      entry({ date: '2026-05-29', tag_ids: ['recent'] }),
      entry({ date: '2026-05-15', tag_ids: ['old'] }),
    ];
    render(
      <TagManagementSection
        tags={tags}
        episodes={[]}
        timelineEntries={entries}
      />,
    );

    const buttons = screen
      .getAllByRole('button')
      .filter((b) => b.textContent?.match(/recent|old|never-used/));
    const order = buttons.map((b) =>
      b.textContent?.startsWith('recent')
        ? 'recent'
        : b.textContent?.startsWith('old')
          ? 'old'
          : 'never-used',
    );
    expect(order).toEqual(['recent', 'old', 'never-used']);
  });

  it('Toon gearchiveerd checkbox is unchecked by default + archived tags are hidden', () => {
    const tags = [
      tag({ id: 'a', label: 'live', category: 'mentaal' }),
      tag({
        id: 'b',
        label: 'gearchiveerd-tag',
        category: 'mentaal',
        archived_at: '2026-05-01T00:00:00.000Z',
      }),
    ];
    render(
      <TagManagementSection
        tags={tags}
        episodes={[]}
        timelineEntries={[]}
      />,
    );

    const checkbox = screen.getByRole('checkbox', {
      name: 'Toon gearchiveerd',
    });
    expect(checkbox).not.toBeChecked();
    expect(screen.getByText('live')).toBeInTheDocument();
    expect(screen.queryByText('gearchiveerd-tag')).toBeNull();
  });

  it('Toon gearchiveerd ON renders archived tags with the (gearchiveerd) suffix', async () => {
    const user = userEvent.setup();
    const tags = [
      tag({
        id: 'b',
        label: 'gearchiveerd-tag',
        category: 'mentaal',
        archived_at: '2026-05-01T00:00:00.000Z',
      }),
    ];
    render(
      <TagManagementSection
        tags={tags}
        episodes={[]}
        timelineEntries={[]}
      />,
    );

    await user.click(
      screen.getByRole('checkbox', { name: 'Toon gearchiveerd' }),
    );

    expect(screen.getByText('gearchiveerd-tag')).toBeInTheDocument();
    expect(screen.getByText(/\(gearchiveerd\)/)).toBeInTheDocument();
  });

  it('each row has the documented aria-label', () => {
    render(
      <TagManagementSection
        tags={[tag({ label: 'pacing', category: 'mentaal' })]}
        episodes={[]}
        timelineEntries={[]}
      />,
    );

    expect(
      screen.getByRole('button', {
        name: 'pacing, Mentaal, tik om te bewerken',
      }),
    ).toBeInTheDocument();
  });

  it('tapping a row opens TagFormSheet with that tag', async () => {
    const user = userEvent.setup();
    const targetTag = tag({ id: 'tag-X', label: 'pacing', category: 'mentaal' });
    render(
      <TagManagementSection
        tags={[targetTag]}
        episodes={[]}
        timelineEntries={[]}
      />,
    );

    expect(screen.queryByTestId('tag-form-sheet')).toBeNull();

    await user.click(
      screen.getByRole('button', { name: /pacing.*tik om te bewerken/ }),
    );

    const sheet = screen.getByTestId('tag-form-sheet');
    expect(sheet).toBeInTheDocument();
    expect(sheet.getAttribute('data-tag-id')).toBe('tag-X');
  });

  it('linked-tag rows show the right-aligned → {episodeLabel} suffix', () => {
    const linkedTag = tag({
      id: 'linked',
      label: 'coaching sessie',
      category: 'interventie',
      parent_episode_id: 'ep-default',
    });
    render(
      <TagManagementSection
        tags={[linkedTag]}
        episodes={[ep()]}
        timelineEntries={[]}
      />,
    );

    expect(screen.getByText(/Coaching met Sarah/)).toBeInTheDocument();
  });
});
