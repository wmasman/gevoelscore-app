/** @vitest-environment jsdom */
import '@testing-library/jest-dom/vitest';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { Tag } from '@/lib/domain/tag';

// Mock BottomSheet — render children when open + expose onClose so the
// drag-down test path can fire it.
vi.mock('@/components/lab/bottom-sheet', () => ({
  BottomSheet: ({
    open,
    ariaLabel,
    onClose,
    children,
  }: {
    open: boolean;
    ariaLabel: string;
    onClose: () => void;
    children: React.ReactNode;
  }) =>
    open ? (
      <div role="dialog" aria-label={ariaLabel}>
        <button data-testid="dragdown" onClick={onClose}>
          dragdown
        </button>
        {children}
      </div>
    ) : null,
}));

import { TagMergeTargetPickerSheet } from '../tag-merge-target-picker-sheet';

function tag(overrides: Partial<Tag> = {}): Tag {
  return {
    id: 'tag-x',
    label: 'pacing',
    category: 'mentaal',
    project_id: null,
    parent_episode_id: null,
    usage_count: 0,
    archived_at: null,
    created_at: '2026-05-01T00:00:00.000Z',
    ...overrides,
  };
}

const SOURCE = tag({ id: 'src', label: 'hoofdpijn', category: 'fysiek', usage_count: 5 });
const TARGET = tag({ id: 'tgt', label: 'migraine', category: 'fysiek' });

function defaultProps(
  overrides: Partial<React.ComponentProps<typeof TagMergeTargetPickerSheet>> = {},
) {
  return {
    source: SOURCE,
    tags: [SOURCE, TARGET, tag({ id: 'other-cat', label: 'helder', category: 'mentaal' })],
    open: true,
    onClose: vi.fn(),
    onMergeConfirmed: vi.fn(),
    saving: false,
    lastError: null,
    ...overrides,
  };
}

afterEach(() => {
  cleanup();
});

describe('<TagMergeTargetPickerSheet />', () => {
  it('test 32: renders BottomSheet with title "Samenvoegen met..."', () => {
    render(<TagMergeTargetPickerSheet {...defaultProps()} />);

    expect(
      screen.getByRole('heading', { name: 'Samenvoegen met...' }),
    ).toBeInTheDocument();
  });

  it('test 33: lists ONLY same-category non-archived tags, sorted alphabetically; excludes self', () => {
    const tags = [
      SOURCE,
      tag({ id: 't-1', label: 'zware migraine', category: 'fysiek' }),
      tag({ id: 't-2', label: 'cluster', category: 'fysiek' }),
      tag({ id: 't-3', label: 'gearchiveerd', category: 'fysiek', archived_at: '2026-01-01T00:00:00Z' }),
      tag({ id: 't-4', label: 'andere-categorie', category: 'mentaal' }),
    ];
    render(<TagMergeTargetPickerSheet {...defaultProps({ tags })} />);

    const buttons = screen.getAllByRole('button').filter((b) => {
      const text = b.textContent ?? '';
      return text !== '' && text !== 'dragdown' && text !== '✕';
    });
    const labels = buttons.map((b) => b.textContent);
    expect(labels).toEqual(['cluster', 'zware migraine']);
  });

  it('test 34: excludes source from the list (no self-merge)', () => {
    render(<TagMergeTargetPickerSheet {...defaultProps()} />);

    // SOURCE.label is "hoofdpijn"; it must NOT appear as a row.
    expect(screen.queryByRole('button', { name: 'hoofdpijn' })).toBeNull();
  });

  it('test 35: tapping a row switches the picker into confirm-mode (alertdialog renders) and does NOT call onMergeConfirmed yet', async () => {
    const onMergeConfirmed = vi.fn();
    const user = userEvent.setup();
    render(<TagMergeTargetPickerSheet {...defaultProps({ onMergeConfirmed })} />);

    await user.click(screen.getByRole('button', { name: 'migraine' }));

    expect(screen.getByRole('alertdialog')).toBeInTheDocument();
    expect(onMergeConfirmed).not.toHaveBeenCalled();
  });

  it('test 36: tapping "Ja, samenvoegen" in confirm calls onMergeConfirmed(target)', async () => {
    const onMergeConfirmed = vi.fn();
    const user = userEvent.setup();
    render(<TagMergeTargetPickerSheet {...defaultProps({ onMergeConfirmed })} />);

    await user.click(screen.getByRole('button', { name: 'migraine' }));
    await user.click(screen.getByRole('button', { name: 'Ja, samenvoegen' }));

    expect(onMergeConfirmed).toHaveBeenCalledTimes(1);
    expect(onMergeConfirmed).toHaveBeenCalledWith(
      expect.objectContaining({ id: 'tgt', label: 'migraine' }),
    );
  });

  it('test 37: tapping "Annuleer" in confirm returns to list mode and does NOT call onMergeConfirmed', async () => {
    const onMergeConfirmed = vi.fn();
    const user = userEvent.setup();
    render(<TagMergeTargetPickerSheet {...defaultProps({ onMergeConfirmed })} />);

    await user.click(screen.getByRole('button', { name: 'migraine' }));
    expect(screen.getByRole('alertdialog')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Annuleer' }));

    expect(screen.queryByRole('alertdialog')).toBeNull();
    expect(screen.getByRole('button', { name: 'migraine' })).toBeInTheDocument();
    expect(onMergeConfirmed).not.toHaveBeenCalled();
  });

  it('test 38: server error banner renders when lastError is set', () => {
    render(
      <TagMergeTargetPickerSheet
        {...defaultProps({ lastError: 'category_mismatch' })}
      />,
    );

    const alert = screen.getByRole('alert');
    expect(alert).toHaveTextContent(/dezelfde categorie/i);
  });

  it('test 39: empty-state line renders when no eligible targets exist', () => {
    render(
      <TagMergeTargetPickerSheet {...defaultProps({ tags: [SOURCE] })} />,
    );

    expect(
      screen.getByText(/geen andere tags in deze categorie/i),
    ).toBeInTheDocument();
  });

  it('test 40: close button calls onClose; drag-down (BottomSheet onClose) also calls it', async () => {
    const onClose = vi.fn();
    const user = userEvent.setup();
    render(<TagMergeTargetPickerSheet {...defaultProps({ onClose })} />);

    await user.click(screen.getByRole('button', { name: 'Sluit' }));
    expect(onClose).toHaveBeenCalledTimes(1);

    await user.click(screen.getByTestId('dragdown'));
    expect(onClose).toHaveBeenCalledTimes(2);
  });
});
