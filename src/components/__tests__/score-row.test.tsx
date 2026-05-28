// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// ScoreRow owns useDayEntryUpsert(date) again (the 2026-05-28 audit's L2
// undid Step 4b's hook hoist and replaced it with a shared
// SaveStatusProvider). Tests mock the hook at the module boundary so
// `save` calls are observable without hitting the network.

const hookMocks = vi.hoisted(() => ({
  save: vi.fn(),
  status: 'idle' as 'idle' | 'saving' | 'saved' | 'error',
  lastError: null as string | null,
}));

vi.mock('@/hooks/use-day-entry-upsert', () => ({
  useDayEntryUpsert: () => ({
    save: hookMocks.save,
    status: hookMocks.status,
    lastError: hookMocks.lastError,
  }),
}));

import { ScoreRow } from '../score-row';

function renderRow(props: Partial<React.ComponentProps<typeof ScoreRow>> = {}) {
  return render(
    <ScoreRow date="2026-05-28" initialScore={null} {...props} />,
  );
}

describe('<ScoreRow />', () => {
  beforeEach(() => {
    Element.prototype.scrollTo = vi.fn() as unknown as Element['scrollTo'];
    hookMocks.save.mockReset();
    hookMocks.save.mockResolvedValue(undefined);
    hookMocks.status = 'idle';
    hookMocks.lastError = null;
  });

  afterEach(cleanup);

  it('renders 10 option items (1..10) with role=option', () => {
    renderRow();
    const items = screen.getAllByRole('option');
    expect(items).toHaveLength(10);
    expect(items.map((el) => el.textContent)).toEqual([
      '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
    ]);
  });

  it('fresh day (initialScore=null): centres at 5, no aria-selected, data-phase=idle', () => {
    renderRow();
    const row = screen.getByRole('listbox', { name: /score/i });
    expect(row).toHaveAttribute('data-phase', 'idle');
    expect(within(row).queryAllByRole('option', { selected: true })).toHaveLength(0);
    const five = within(row).getByRole('option', { name: '5' });
    expect(five).toHaveAttribute('data-centred', 'true');
  });

  it('existing entry (initialScore=7): centres at 7, aria-selected=true on 7, data-phase=set', () => {
    renderRow({ initialScore: 7 });
    const row = screen.getByRole('listbox', { name: /score/i });
    expect(row).toHaveAttribute('data-phase', 'set');
    const selected = within(row).getByRole('option', { selected: true });
    expect(selected).toHaveTextContent('7');
  });

  it('tap on visible value: fires save({score: n}) and promotes idle → set', async () => {
    const user = userEvent.setup();
    renderRow();

    await user.click(screen.getByRole('option', { name: '7' }));

    expect(hookMocks.save).toHaveBeenCalledOnce();
    expect(hookMocks.save).toHaveBeenCalledWith({ score: 7 }, expect.objectContaining({ flush: true }));

    const row = screen.getByRole('listbox', { name: /score/i });
    expect(row).toHaveAttribute('data-phase', 'set');
    const selected = within(row).getByRole('option', { selected: true });
    expect(selected).toHaveTextContent('7');
  });

  it('tap on already-set value is a no-op', async () => {
    const user = userEvent.setup();
    renderRow({ initialScore: 7 });

    await user.click(screen.getByRole('option', { name: '7' }));

    expect(hookMocks.save).not.toHaveBeenCalled();
  });

  it('tap on a different value on a set row: fires save WITHOUT flush (debounced)', async () => {
    const user = userEvent.setup();
    renderRow({ initialScore: 7 });

    await user.click(screen.getByRole('option', { name: '4' }));

    expect(hookMocks.save).toHaveBeenCalledOnce();
    const args = hookMocks.save.mock.calls[0]!;
    expect(args[0]).toEqual({ score: 4 });
    expect(args[1]?.flush ?? false).toBe(false);
  });

  it('ArrowRight moves centred toward 10 and saves (primary axis)', async () => {
    renderRow();
    const row = screen.getByRole('listbox', { name: /score/i });
    row.focus();
    await userEvent.keyboard('{ArrowRight}');

    expect(hookMocks.save).toHaveBeenCalledWith({ score: 6 }, expect.objectContaining({ flush: true }));
  });

  it('ArrowLeft moves centred toward 1 and saves (primary axis)', async () => {
    renderRow({ initialScore: 5 });
    const row = screen.getByRole('listbox', { name: /score/i });
    row.focus();
    await userEvent.keyboard('{ArrowLeft}');

    expect(hookMocks.save).toHaveBeenCalledWith({ score: 4 }, expect.anything());
  });

  it('ArrowDown is preserved as alias (Step 4 muscle memory + hardware keyboards)', async () => {
    renderRow();
    const row = screen.getByRole('listbox', { name: /score/i });
    row.focus();
    await userEvent.keyboard('{ArrowDown}');

    expect(hookMocks.save).toHaveBeenCalledWith({ score: 6 }, expect.objectContaining({ flush: true }));
  });

  it('ArrowUp is preserved as alias', async () => {
    renderRow({ initialScore: 5 });
    const row = screen.getByRole('listbox', { name: /score/i });
    row.focus();
    await userEvent.keyboard('{ArrowUp}');

    expect(hookMocks.save).toHaveBeenCalledWith({ score: 4 }, expect.anything());
  });

  it('Home jumps to 1; End jumps to 10', async () => {
    renderRow({ initialScore: 5 });
    const row = screen.getByRole('listbox', { name: /score/i });
    row.focus();

    await userEvent.keyboard('{Home}');
    expect(hookMocks.save).toHaveBeenLastCalledWith({ score: 1 }, expect.anything());

    await userEvent.keyboard('{End}');
    expect(hookMocks.save).toHaveBeenLastCalledWith({ score: 10 }, expect.anything());
  });

  it('keyboard navigation stays in [1..10] bounds', async () => {
    renderRow({ initialScore: 1 });
    const row = screen.getByRole('listbox', { name: /score/i });
    row.focus();
    await userEvent.keyboard('{ArrowLeft}');

    expect(hookMocks.save).not.toHaveBeenCalled();
  });
});
