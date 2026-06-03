/** @vitest-environment jsdom */
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { Episode } from '@/lib/domain/episode';
import type { Tag } from '@/lib/domain/tag';

// Mock BottomSheet — render children when open.
vi.mock('@/components/lab/bottom-sheet', () => ({
  BottomSheet: ({
    open,
    ariaLabel,
    children,
  }: {
    open: boolean;
    ariaLabel: string;
    onClose: () => void;
    children: React.ReactNode;
  }) =>
    open ? (
      <div role="dialog" aria-label={ariaLabel}>
        {children}
      </div>
    ) : null,
}));

const hookMocks = vi.hoisted(() => ({
  save: vi.fn(),
  setArchived: vi.fn(),
  hardDelete: vi.fn(),
  merge: vi.fn(),
  status: 'idle' as 'idle' | 'saving' | 'saved' | 'error',
  lastError: null as string | null,
}));
vi.mock('@/hooks/use-tag-manage', () => ({
  useTagManage: () => hookMocks,
}));

import { TagFormSheet } from '../tag-form-sheet';

const EPISODE_ID = '550e8400-e29b-41d4-a716-446655440000';

function tag(overrides: Partial<Tag> = {}): Tag {
  return {
    id: 'tag-1',
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
    id: EPISODE_ID,
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

function defaultProps(
  overrides: Partial<React.ComponentProps<typeof TagFormSheet>> = {},
) {
  return {
    tag: tag(),
    episodes: [ep()],
    open: true,
    onClose: vi.fn(),
    onSaved: vi.fn(),
    onDeleted: vi.fn(),
    ...overrides,
  };
}

beforeEach(() => {
  hookMocks.save.mockReset().mockResolvedValue(tag());
  hookMocks.setArchived.mockReset().mockResolvedValue(tag());
  hookMocks.hardDelete.mockReset().mockResolvedValue({ deleted_id: 'tag-1' });
  hookMocks.merge.mockReset().mockResolvedValue({
    source_id: 'tag-1',
    target_id: 'tag-2',
    affected_days: 2,
  });
  hookMocks.status = 'idle';
  hookMocks.lastError = null;
});
afterEach(() => {
  cleanup();
});

describe('<TagFormSheet />', () => {
  it('renders title "Tag bewerken" + Naam + Categorie + Behoort bij + Status', () => {
    render(<TagFormSheet {...defaultProps()} />);

    expect(
      screen.getByRole('heading', { name: 'Tag bewerken' }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText('Naam')).toBeInTheDocument();
    expect(screen.getByLabelText('Categorie')).toBeInTheDocument();
    expect(screen.getByLabelText('Behoort bij')).toBeInTheDocument();
    // Status block: "3 keer gebruikt, laatst ..." (no last-used date in
    // the form's input — it shows just the count for v1.5b)
    expect(screen.getByText(/3 keer gebruikt/)).toBeInTheDocument();
  });

  it('seeds form fields from the tag prop on open', () => {
    render(
      <TagFormSheet
        {...defaultProps({
          tag: tag({ label: 'helder', category: 'mentaal' }),
        })}
      />,
    );

    const labelInput = screen.getByLabelText('Naam') as HTMLInputElement;
    expect(labelInput.value).toBe('helder');
    const categorySelect = screen.getByLabelText(
      'Categorie',
    ) as HTMLSelectElement;
    expect(categorySelect.value).toBe('mentaal');
  });

  it('Save button is disabled when no field differs from initialTag', () => {
    render(<TagFormSheet {...defaultProps()} />);

    const saveButton = screen.getByRole('button', { name: 'Bewaar' });
    expect(saveButton).toBeDisabled();
  });

  it('Save calls hook.save with ONLY the diff', async () => {
    const user = userEvent.setup();
    render(<TagFormSheet {...defaultProps({ tag: tag({ label: 'pacing' }) })} />);

    const labelInput = screen.getByLabelText('Naam');
    await user.clear(labelInput);
    await user.type(labelInput, 'pacing-strategy');
    await user.click(screen.getByRole('button', { name: 'Bewaar' }));

    expect(hookMocks.save).toHaveBeenCalledTimes(1);
    expect(hookMocks.save.mock.calls[0]?.[1]).toEqual({
      label: 'pacing-strategy',
    });
  });

  it('Archive button label toggles between "Archiveer" and "Activeer opnieuw"', () => {
    const { rerender } = render(
      <TagFormSheet {...defaultProps({ tag: tag({ archived_at: null }) })} />,
    );
    expect(
      screen.getByRole('button', { name: 'Archiveer' }),
    ).toBeInTheDocument();

    rerender(
      <TagFormSheet
        {...defaultProps({
          tag: tag({ archived_at: '2026-06-01T00:00:00.000Z' }),
        })}
      />,
    );
    expect(
      screen.getByRole('button', { name: 'Activeer opnieuw' }),
    ).toBeInTheDocument();
  });

  it('Hard-delete button is DISABLED when usage_count > 0', () => {
    render(<TagFormSheet {...defaultProps({ tag: tag({ usage_count: 3 }) })} />);

    const deleteButton = screen.getByRole('button', { name: 'Verwijder' });
    expect(deleteButton).toBeDisabled();
  });

  it('Hard-delete button is ENABLED when usage_count === 0', () => {
    render(<TagFormSheet {...defaultProps({ tag: tag({ usage_count: 0 }) })} />);

    const deleteButton = screen.getByRole('button', { name: 'Verwijder' });
    expect(deleteButton).toBeEnabled();
  });

  it('Tapping enabled Verwijder opens the inline confirm alertdialog', async () => {
    const user = userEvent.setup();
    render(<TagFormSheet {...defaultProps({ tag: tag({ usage_count: 0 }) })} />);

    expect(screen.queryByRole('alertdialog')).toBeNull();

    await user.click(screen.getByRole('button', { name: 'Verwijder' }));

    expect(screen.getByRole('alertdialog')).toBeInTheDocument();
  });

  it("confirm's default focus is on Annuleer (M5: brainfog protection)", async () => {
    const user = userEvent.setup();
    render(<TagFormSheet {...defaultProps({ tag: tag({ usage_count: 0 }) })} />);

    await user.click(screen.getByRole('button', { name: 'Verwijder' }));

    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'Annuleer' })).toHaveFocus();
    });
  });

  it('Tapping Annuleer returns to the form (alertdialog gone)', async () => {
    const user = userEvent.setup();
    render(<TagFormSheet {...defaultProps({ tag: tag({ usage_count: 0 }) })} />);

    await user.click(screen.getByRole('button', { name: 'Verwijder' }));
    await user.click(screen.getByRole('button', { name: 'Annuleer' }));

    expect(screen.queryByRole('alertdialog')).toBeNull();
    // Form remains
    expect(screen.getByLabelText('Naam')).toBeInTheDocument();
  });

  it('Tapping Ja, verwijder calls hook.hardDelete and fires onDeleted', async () => {
    const user = userEvent.setup();
    const onDeleted = vi.fn();
    render(
      <TagFormSheet
        {...defaultProps({ tag: tag({ usage_count: 0 }), onDeleted })}
      />,
    );

    await user.click(screen.getByRole('button', { name: 'Verwijder' }));
    await user.click(screen.getByRole('button', { name: 'Ja, verwijder' }));

    expect(hookMocks.hardDelete).toHaveBeenCalledWith('tag-1');
    await waitFor(() => expect(onDeleted).toHaveBeenCalledTimes(1));
  });

  it('Behoort bij dropdown lists Geen + every non-archived episode label', () => {
    const epA = ep({ id: 'ep-a', label: 'Coaching A' });
    const epB = ep({ id: 'ep-b', label: 'Vakantie B' });
    render(
      <TagFormSheet {...defaultProps({ episodes: [epA, epB] })} />,
    );

    const select = screen.getByLabelText('Behoort bij') as HTMLSelectElement;
    const options = Array.from(select.options).map((o) => o.text);
    expect(options).toContain('Geen');
    expect(options).toContain('Coaching A');
    expect(options).toContain('Vakantie B');
  });

  it('Selecting Geen from a previously-linked tag clears parent on save', async () => {
    const user = userEvent.setup();
    render(
      <TagFormSheet
        {...defaultProps({
          tag: tag({ parent_episode_id: EPISODE_ID }),
        })}
      />,
    );

    await user.selectOptions(screen.getByLabelText('Behoort bij'), '');
    await user.click(screen.getByRole('button', { name: 'Bewaar' }));

    expect(hookMocks.save.mock.calls[0]?.[1]).toEqual({
      parent_episode_id: null,
    });
  });

  it('Status block renders "Nog niet gebruikt" for usage_count === 0', () => {
    render(<TagFormSheet {...defaultProps({ tag: tag({ usage_count: 0 }) })} />);

    expect(screen.getByText('Nog niet gebruikt')).toBeInTheDocument();
  });

  it('Per-field server error surfaces in the banner (M1 dividend)', () => {
    hookMocks.lastError = 'invalid_label';
    render(<TagFormSheet {...defaultProps()} />);

    // The banner uses copy.settings.tagManagement.form.error.invalidLabel
    expect(screen.getByText('Naam is ongeldig.')).toBeInTheDocument();
  });

  // -------------------------------------------------------------------------
  // v1.5c merge integration. Tests 41-51 from
  // docs/features/tag-merge/step-1-tag-merge.md.
  // -------------------------------------------------------------------------

  describe('Samenvoegen integration', () => {
    function altTag(overrides: Partial<Tag> = {}): Tag {
      return tag({
        id: 'tag-2',
        label: 'pacing strikt',
        category: 'mentaal',
        ...overrides,
      });
    }

    it('test 41: accepts a `tags` prop (defaults to [] when omitted; default keeps merge button disabled)', () => {
      // Existing call sites that don't pass `tags` must still render
      // — the button is disabled but the form renders without crash.
      render(<TagFormSheet {...defaultProps()} />);
      const btn = screen.getByRole('button', { name: 'Samenvoegen met...' });
      expect(btn).toBeDisabled();
    });

    it('test 42: "Samenvoegen met..." button is rendered in the action row', () => {
      render(<TagFormSheet {...defaultProps({ tags: [tag(), altTag()] })} />);

      expect(
        screen.getByRole('button', { name: 'Samenvoegen met...' }),
      ).toBeInTheDocument();
    });

    it('test 43: button DISABLED when tag.archived_at !== null', () => {
      render(
        <TagFormSheet
          {...defaultProps({
            tag: tag({ archived_at: '2026-05-01T00:00:00Z' }),
            tags: [tag({ archived_at: '2026-05-01T00:00:00Z' }), altTag()],
          })}
        />,
      );

      expect(
        screen.getByRole('button', { name: 'Samenvoegen met...' }),
      ).toBeDisabled();
    });

    it('test 44: button DISABLED when no same-category non-archived alternatives in tags', () => {
      render(
        <TagFormSheet
          {...defaultProps({
            tags: [
              tag(), // self only
              altTag({ id: 'tag-archived', archived_at: '2026-01-01T00:00:00Z' }),
              altTag({ id: 'tag-other-cat', category: 'fysiek' }),
            ],
          })}
        />,
      );

      expect(
        screen.getByRole('button', { name: 'Samenvoegen met...' }),
      ).toBeDisabled();
    });

    it('test 45: button ENABLED with at least one same-category non-archived alternative', () => {
      render(
        <TagFormSheet {...defaultProps({ tags: [tag(), altTag()] })} />,
      );

      expect(
        screen.getByRole('button', { name: 'Samenvoegen met...' }),
      ).toBeEnabled();
    });

    it('test 46: tapping the button opens the merge picker', async () => {
      const user = userEvent.setup();
      render(<TagFormSheet {...defaultProps({ tags: [tag(), altTag()] })} />);

      await user.click(
        screen.getByRole('button', { name: 'Samenvoegen met...' }),
      );

      // Picker title "Samenvoegen met..." renders in the nested BottomSheet
      expect(screen.getAllByRole('heading', { name: 'Samenvoegen met...' }).length).toBeGreaterThan(
        0,
      );
      // The target row from `tags` shows up as a button
      expect(
        screen.getByRole('button', { name: 'pacing strikt' }),
      ).toBeInTheDocument();
    });

    it('test 47: tapping a target row in the picker renders a confirm with source.usage_count in the prompt', async () => {
      const user = userEvent.setup();
      render(
        <TagFormSheet
          {...defaultProps({
            tag: tag({ usage_count: 7, label: 'hoofdpijn' }),
            tags: [tag({ usage_count: 7, label: 'hoofdpijn' }), altTag({ label: 'migraine' })],
          })}
        />,
      );

      await user.click(
        screen.getByRole('button', { name: 'Samenvoegen met...' }),
      );
      await user.click(screen.getByRole('button', { name: 'migraine' }));

      const dlg = screen.getByRole('alertdialog');
      expect(dlg).toHaveTextContent(/7 dagen/i);
      expect(dlg).toHaveTextContent(/hoofdpijn/);
      expect(dlg).toHaveTextContent(/migraine/);
    });

    it('test 48: confirm dialog focus lands on Annuleer (brainfog protection)', async () => {
      const user = userEvent.setup();
      render(<TagFormSheet {...defaultProps({ tags: [tag(), altTag()] })} />);

      await user.click(
        screen.getByRole('button', { name: 'Samenvoegen met...' }),
      );
      await user.click(screen.getByRole('button', { name: 'pacing strikt' }));

      await waitFor(() =>
        expect(screen.getByRole('button', { name: 'Annuleer' })).toHaveFocus(),
      );
    });

    it('test 49: tapping Annuleer dismisses the confirm; picker stays open', async () => {
      const user = userEvent.setup();
      render(<TagFormSheet {...defaultProps({ tags: [tag(), altTag()] })} />);

      await user.click(
        screen.getByRole('button', { name: 'Samenvoegen met...' }),
      );
      await user.click(screen.getByRole('button', { name: 'pacing strikt' }));
      expect(screen.getByRole('alertdialog')).toBeInTheDocument();

      await user.click(screen.getByRole('button', { name: 'Annuleer' }));

      expect(screen.queryByRole('alertdialog')).toBeNull();
      expect(
        screen.getByRole('button', { name: 'pacing strikt' }),
      ).toBeInTheDocument();
      expect(hookMocks.merge).not.toHaveBeenCalled();
    });

    it('test 50: tapping "Ja, samenvoegen" calls hook.merge(source.id, target.id)', async () => {
      const user = userEvent.setup();
      render(<TagFormSheet {...defaultProps({ tags: [tag(), altTag()] })} />);

      await user.click(
        screen.getByRole('button', { name: 'Samenvoegen met...' }),
      );
      await user.click(screen.getByRole('button', { name: 'pacing strikt' }));
      await user.click(screen.getByRole('button', { name: 'Ja, samenvoegen' }));

      await waitFor(() => expect(hookMocks.merge).toHaveBeenCalledTimes(1));
      expect(hookMocks.merge).toHaveBeenCalledWith('tag-1', 'tag-2');
    });

    it('test 51: on merge success, onMerged + onClose both fire (form closes)', async () => {
      const onClose = vi.fn();
      const onMerged = vi.fn();
      const user = userEvent.setup();
      render(
        <TagFormSheet
          {...defaultProps({ tags: [tag(), altTag()], onClose, onMerged })}
        />,
      );

      await user.click(
        screen.getByRole('button', { name: 'Samenvoegen met...' }),
      );
      await user.click(screen.getByRole('button', { name: 'pacing strikt' }));
      await user.click(screen.getByRole('button', { name: 'Ja, samenvoegen' }));

      await waitFor(() => expect(onClose).toHaveBeenCalledTimes(1));
      expect(onMerged).toHaveBeenCalledWith(2); // affected_days from mock
    });
  });
});
