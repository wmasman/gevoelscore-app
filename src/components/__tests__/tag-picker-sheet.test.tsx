/** @vitest-environment jsdom */
import '@testing-library/jest-dom/vitest';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { Episode } from '@/lib/domain/episode';
import type { Tag } from '@/lib/domain/tag';

import { TagPickerSheet } from '../tag-picker-sheet';

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

function defaultProps(overrides: Partial<React.ComponentProps<typeof TagPickerSheet>> = {}) {
  return {
    episode: ep(),
    tags: [] as Tag[],
    episodes: [] as Episode[],
    open: true,
    onClose: vi.fn(),
    onPickExisting: vi.fn(),
    onCreateNew: vi.fn(),
    saving: false,
    lastError: null as string | null,
    ...overrides,
  };
}

afterEach(() => {
  cleanup();
});

describe('<TagPickerSheet />', () => {
  it('renders the sheet title "Kies of maak een tag" when open', () => {
    render(<TagPickerSheet {...defaultProps()} />);

    expect(
      screen.getByRole('heading', { name: 'Kies of maak een tag' }),
    ).toBeTruthy();
  });

  it('renders the "+ Maak een nieuwe tag aan" CTA', () => {
    render(<TagPickerSheet {...defaultProps()} />);

    expect(
      screen.getByRole('button', { name: '+ Maak een nieuwe tag aan' }),
    ).toBeTruthy();
  });

  it('renders all non-this-episode tags grouped by category', () => {
    const tags = [
      tag({ id: 't-1', label: 'helder', category: 'mentaal' }),
      tag({ id: 't-2', label: 'pacing', category: 'mentaal' }),
      tag({ id: 't-3', label: 'hoofdpijn', category: 'fysiek' }),
    ];
    render(<TagPickerSheet {...defaultProps({ tags })} />);

    expect(
      screen.getByRole('heading', { level: 3, name: /Mentaal/i }),
    ).toBeTruthy();
    expect(
      screen.getByRole('heading', { level: 3, name: /Fysiek/i }),
    ).toBeTruthy();
    expect(screen.getByText('helder')).toBeTruthy();
    expect(screen.getByText('pacing')).toBeTruthy();
    expect(screen.getByText('hoofdpijn')).toBeTruthy();
  });

  it('hides tags already linked to THIS episode', () => {
    const tags = [
      tag({ id: 't-1', label: 'al-gelinkt', parent_episode_id: EPISODE_ID }),
      tag({ id: 't-2', label: 'pacing', parent_episode_id: null }),
    ];
    render(<TagPickerSheet {...defaultProps({ tags })} />);

    expect(screen.queryByText('al-gelinkt')).toBeNull();
    expect(screen.getByText('pacing')).toBeTruthy();
  });

  it('shows tags linked to a DIFFERENT episode WITH the (bij: <label>) suffix', () => {
    const other = ep({ id: OTHER_EPISODE_ID, label: 'Citalopram afbouw' });
    const tags = [
      tag({
        id: 't-1',
        label: 'paracetamol',
        parent_episode_id: OTHER_EPISODE_ID,
      }),
    ];
    render(
      <TagPickerSheet {...defaultProps({ tags, episodes: [other] })} />,
    );

    expect(screen.getByText('paracetamol')).toBeTruthy();
    expect(screen.getByText('(bij: Citalopram afbouw)')).toBeTruthy();
  });

  it('tapping a tag row calls onPickExisting with the tag id', async () => {
    const user = userEvent.setup();
    const onPickExisting = vi.fn();
    const tags = [tag({ id: 'tag-pacing', label: 'pacing' })];
    render(
      <TagPickerSheet {...defaultProps({ tags, onPickExisting })} />,
    );

    await user.click(screen.getByRole('button', { name: /pacing/ }));

    expect(onPickExisting).toHaveBeenCalledWith('tag-pacing');
  });

  it('tapping a tag linked elsewhere also calls onPickExisting (silent re-parent)', async () => {
    const user = userEvent.setup();
    const other = ep({ id: OTHER_EPISODE_ID, label: 'Citalopram afbouw' });
    const onPickExisting = vi.fn();
    const tags = [
      tag({
        id: 'tag-paracetamol',
        label: 'paracetamol',
        parent_episode_id: OTHER_EPISODE_ID,
      }),
    ];
    render(
      <TagPickerSheet
        {...defaultProps({ tags, episodes: [other], onPickExisting })}
      />,
    );

    await user.click(screen.getByRole('button', { name: /paracetamol/ }));

    expect(onPickExisting).toHaveBeenCalledWith('tag-paracetamol');
    // Silent re-parent: only the picker dialog is open. No confirm dialog
    // is inserted on top (we'd see two role="dialog" nodes if there were).
    expect(screen.getAllByRole('dialog')).toHaveLength(1);
  });

  it('tapping "+ Maak een nieuwe tag aan" expands the inline mini-form', async () => {
    const user = userEvent.setup();
    render(<TagPickerSheet {...defaultProps()} />);

    // Before tap: form fields not visible.
    expect(screen.queryByLabelText(/Naam/i)).toBeNull();

    await user.click(
      screen.getByRole('button', { name: '+ Maak een nieuwe tag aan' }),
    );

    expect(screen.getByLabelText('Tag naam')).toBeTruthy();
    expect(screen.getByLabelText(/Categorie/i)).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Toevoegen' })).toBeTruthy();
  });

  it('submitting the mini-form with valid label + category calls onCreateNew', async () => {
    const user = userEvent.setup();
    const onCreateNew = vi.fn();
    render(<TagPickerSheet {...defaultProps({ onCreateNew })} />);

    await user.click(
      screen.getByRole('button', { name: '+ Maak een nieuwe tag aan' }),
    );
    await user.type(screen.getByLabelText('Tag naam'), 'huiswerk');
    await user.selectOptions(screen.getByLabelText(/Categorie/i), 'interventie');
    await user.click(screen.getByRole('button', { name: 'Toevoegen' }));

    expect(onCreateNew).toHaveBeenCalledWith({
      label: 'huiswerk',
      category: 'interventie',
    });
  });

  it('mini-form validation: empty label shows inline error and does NOT call onCreateNew', async () => {
    const user = userEvent.setup();
    const onCreateNew = vi.fn();
    render(<TagPickerSheet {...defaultProps({ onCreateNew })} />);

    await user.click(
      screen.getByRole('button', { name: '+ Maak een nieuwe tag aan' }),
    );
    await user.selectOptions(screen.getByLabelText(/Categorie/i), 'interventie');
    await user.click(screen.getByRole('button', { name: 'Toevoegen' }));

    expect(onCreateNew).not.toHaveBeenCalled();
    expect(screen.getByText('Geef een naam.')).toBeTruthy();
  });

  it('mini-form validation: label > 40 chars shows the too-long error', async () => {
    const user = userEvent.setup();
    const onCreateNew = vi.fn();
    render(<TagPickerSheet {...defaultProps({ onCreateNew })} />);

    await user.click(
      screen.getByRole('button', { name: '+ Maak een nieuwe tag aan' }),
    );
    const input = screen.getByLabelText('Tag naam');
    // No maxLength on the input — the validator catches > 40 chars and
    // surfaces the Dutch error. Type past the cap.
    await user.type(input, 'a'.repeat(41));
    await user.selectOptions(screen.getByLabelText(/Categorie/i), 'interventie');
    await user.click(screen.getByRole('button', { name: 'Toevoegen' }));

    expect(onCreateNew).not.toHaveBeenCalled();
    expect(screen.getByText('Maximaal 40 tekens.')).toBeTruthy();
  });

  it('mini-form validation: no category selected shows the categoryMissing error', async () => {
    const user = userEvent.setup();
    const onCreateNew = vi.fn();
    render(<TagPickerSheet {...defaultProps({ onCreateNew })} />);

    await user.click(
      screen.getByRole('button', { name: '+ Maak een nieuwe tag aan' }),
    );
    await user.type(screen.getByLabelText('Tag naam'), 'huiswerk');
    await user.click(screen.getByRole('button', { name: 'Toevoegen' }));

    expect(onCreateNew).not.toHaveBeenCalled();
    expect(screen.getByText('Kies een categorie.')).toBeTruthy();
  });

  it('renders the server-error banner when lastError is set', () => {
    render(<TagPickerSheet {...defaultProps({ lastError: 'server_error' })} />);

    expect(screen.getByText('Opslaan lukte niet, probeer opnieuw.')).toBeTruthy();
  });

  it('empty-corpus state: only the create CTA + muted line render', () => {
    // No eligible tags — only this episode's already-linked tag exists.
    const tags = [
      tag({ id: 't-1', label: 'al-gelinkt', parent_episode_id: EPISODE_ID }),
    ];
    render(<TagPickerSheet {...defaultProps({ tags })} />);

    expect(
      screen.getByRole('button', { name: '+ Maak een nieuwe tag aan' }),
    ).toBeTruthy();
    expect(
      screen.getByText('Nog geen andere tags. Maak er een aan.'),
    ).toBeTruthy();
    // No category headings render.
    expect(screen.queryByRole('heading', { level: 3 })).toBeNull();
  });

  it('does NOT render when open=false', () => {
    render(<TagPickerSheet {...defaultProps({ open: false })} />);

    expect(
      screen.queryByRole('heading', { name: 'Kies of maak een tag' }),
    ).toBeNull();
  });
});
