/** @vitest-environment jsdom */
import '@testing-library/jest-dom/vitest';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { Episode } from '@/lib/domain/episode';
import type { Tag } from '@/lib/domain/tag';

import { LinkedTagsSection } from '../linked-tags-section';

const EPISODE_ID = '550e8400-e29b-41d4-a716-446655440000';
const OTHER_EPISODE_ID = '6ba7b810-9dad-11d1-80b4-00c04fd430c8';

function ep(overrides: Partial<Episode> = {}): Episode {
  return {
    id: EPISODE_ID,
    label: 'Coaching met Sarah',
    category: 'interventie',
    start_date: '2026-04-01',
    end_date: null,
    description: null,
    calendar_binding: null,
    archived_at: null,
    created_at: '2026-04-01T08:00:00.000Z',
    updated_at: '2026-04-01T08:00:00.000Z',
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
    created_at: '2026-06-01T00:00:00.000Z',
    ...overrides,
  };
}

afterEach(() => {
  cleanup();
});

describe('<LinkedTagsSection />', () => {
  it('renders the heading "Tags die hierbij horen"', () => {
    render(
      <LinkedTagsSection
        episode={ep()}
        tags={[]}
        onUnlink={vi.fn()}
        onOpenPicker={vi.fn()}
        disabled={false}
      />,
    );

    expect(
      screen.getByRole('heading', {
        level: 3,
        name: 'Tags die hierbij horen',
      }),
    ).toBeTruthy();
  });

  it('renders a chip for each tag whose parent_episode_id matches this episode', () => {
    const tags = [
      tag({ id: 't-1', label: 'coaching sessie', parent_episode_id: EPISODE_ID }),
      tag({ id: 't-2', label: 'huiswerk', parent_episode_id: EPISODE_ID }),
      tag({ id: 't-3', label: 'pacing', parent_episode_id: null }),
      tag({
        id: 't-4',
        label: 'paracetamol',
        parent_episode_id: OTHER_EPISODE_ID,
      }),
    ];
    render(
      <LinkedTagsSection
        episode={ep()}
        tags={tags}
        onUnlink={vi.fn()}
        onOpenPicker={vi.fn()}
        disabled={false}
      />,
    );

    expect(screen.getByText('coaching sessie')).toBeTruthy();
    expect(screen.getByText('huiswerk')).toBeTruthy();
    expect(screen.queryByText('pacing')).toBeNull();
    expect(screen.queryByText('paracetamol')).toBeNull();
  });

  it('renders the empty-state line when no tags are linked', () => {
    render(
      <LinkedTagsSection
        episode={ep()}
        tags={[tag({ parent_episode_id: null })]}
        onUnlink={vi.fn()}
        onOpenPicker={vi.fn()}
        disabled={false}
      />,
    );

    expect(screen.getByText('Nog geen gekoppelde tags.')).toBeTruthy();
  });

  it('renders the "+ Tag" button and calls onOpenPicker on click', async () => {
    const user = userEvent.setup();
    const onOpenPicker = vi.fn();
    render(
      <LinkedTagsSection
        episode={ep()}
        tags={[]}
        onUnlink={vi.fn()}
        onOpenPicker={onOpenPicker}
        disabled={false}
      />,
    );

    const button = screen.getByRole('button', { name: '+ Tag' });
    await user.click(button);

    expect(onOpenPicker).toHaveBeenCalledTimes(1);
  });

  it('each linked-tag chip has a remove button with the configured aria-label', () => {
    render(
      <LinkedTagsSection
        episode={ep()}
        tags={[
          tag({
            id: 't-1',
            label: 'coaching sessie',
            parent_episode_id: EPISODE_ID,
          }),
        ]}
        onUnlink={vi.fn()}
        onOpenPicker={vi.fn()}
        disabled={false}
      />,
    );

    expect(
      screen.getByRole('button', {
        name: 'Verwijder koppeling: coaching sessie',
      }),
    ).toBeTruthy();
  });

  it('clicking the chip remove button calls onUnlink with the tag id', async () => {
    const user = userEvent.setup();
    const onUnlink = vi.fn();
    render(
      <LinkedTagsSection
        episode={ep()}
        tags={[
          tag({
            id: 'tag-coaching',
            label: 'coaching sessie',
            parent_episode_id: EPISODE_ID,
          }),
        ]}
        onUnlink={onUnlink}
        onOpenPicker={vi.fn()}
        disabled={false}
      />,
    );

    const removeButton = screen.getByRole('button', {
      name: 'Verwijder koppeling: coaching sessie',
    });
    await user.click(removeButton);

    expect(onUnlink).toHaveBeenCalledWith('tag-coaching');
  });

  it('disables the + Tag and all remove buttons when disabled=true', () => {
    render(
      <LinkedTagsSection
        episode={ep()}
        tags={[
          tag({
            id: 't-1',
            label: 'coaching sessie',
            parent_episode_id: EPISODE_ID,
          }),
        ]}
        onUnlink={vi.fn()}
        onOpenPicker={vi.fn()}
        disabled={true}
      />,
    );

    expect(screen.getByRole('button', { name: '+ Tag' })).toBeDisabled();
    expect(
      screen.getByRole('button', {
        name: 'Verwijder koppeling: coaching sessie',
      }),
    ).toBeDisabled();
  });
});
