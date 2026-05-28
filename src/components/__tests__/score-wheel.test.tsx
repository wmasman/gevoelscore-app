// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

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

import { ScoreWheel } from '../score-wheel';

describe('<ScoreWheel />', () => {
  beforeEach(() => {
    hookMocks.save.mockReset();
    hookMocks.save.mockResolvedValue(undefined);
  });

  afterEach(cleanup);

  it('renders 10 option items (1..10) with role=option', () => {
    render(<ScoreWheel date="2026-05-28" initialScore={null} />);
    const items = screen.getAllByRole('option');
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

  it('fresh day (initialScore=null): centres at 5, no aria-selected, data-phase=idle', () => {
    render(<ScoreWheel date="2026-05-28" initialScore={null} />);
    const wheel = screen.getByRole('listbox', { name: /score/i });
    expect(wheel).toHaveAttribute('data-phase', 'idle');
    expect(within(wheel).queryAllByRole('option', { selected: true })).toHaveLength(0);
    // Centre-of-wheel is 5 — exposed via data-centred on the button itself.
    const five = within(wheel).getByRole('option', { name: '5' });
    expect(five).toHaveAttribute('data-centred', 'true');
  });

  it('existing entry (initialScore=7): centres at 7, aria-selected=true on 7, data-phase=set', () => {
    render(<ScoreWheel date="2026-05-28" initialScore={7} />);
    const wheel = screen.getByRole('listbox', { name: /score/i });
    expect(wheel).toHaveAttribute('data-phase', 'set');
    const selected = within(wheel).getByRole('option', { selected: true });
    expect(selected).toHaveTextContent('7');
  });

  it('tap on visible value: fires save({score: n}) and promotes idle → set', async () => {
    const user = userEvent.setup();
    render(<ScoreWheel date="2026-05-28" initialScore={null} />);

    await user.click(screen.getByRole('option', { name: '7' }));

    expect(hookMocks.save).toHaveBeenCalledOnce();
    expect(hookMocks.save).toHaveBeenCalledWith({ score: 7 }, expect.objectContaining({ flush: true }));

    const wheel = screen.getByRole('listbox', { name: /score/i });
    expect(wheel).toHaveAttribute('data-phase', 'set');
    const selected = within(wheel).getByRole('option', { selected: true });
    expect(selected).toHaveTextContent('7');
  });

  it('tap on already-set value is a no-op (AC4)', async () => {
    const user = userEvent.setup();
    render(<ScoreWheel date="2026-05-28" initialScore={7} />);

    await user.click(screen.getByRole('option', { name: '7' }));

    expect(hookMocks.save).not.toHaveBeenCalled();
  });

  it('tap on a different value on a set wheel: fires save WITHOUT flush (debounced)', async () => {
    const user = userEvent.setup();
    render(<ScoreWheel date="2026-05-28" initialScore={7} />);

    await user.click(screen.getByRole('option', { name: '4' }));

    expect(hookMocks.save).toHaveBeenCalledOnce();
    const args = hookMocks.save.mock.calls[0]!;
    expect(args[0]).toEqual({ score: 4 });
    // Either undefined opts or { flush: false } — anything that isn't flush:true.
    expect(args[1]?.flush ?? false).toBe(false);
  });

  it('ArrowDown moves centred up to the next-higher value (towards 10) and saves', async () => {
    render(<ScoreWheel date="2026-05-28" initialScore={null} />);
    const wheel = screen.getByRole('listbox', { name: /score/i });
    wheel.focus();
    // Idle starts centred at 5 → ArrowDown should move to 6 (next, towards 10).
    await userEvent.keyboard('{ArrowDown}');

    expect(hookMocks.save).toHaveBeenCalledWith({ score: 6 }, expect.objectContaining({ flush: true }));
  });

  it('ArrowUp moves centred down to the next-lower value (towards 1) and saves', async () => {
    render(<ScoreWheel date="2026-05-28" initialScore={5} />);
    const wheel = screen.getByRole('listbox', { name: /score/i });
    wheel.focus();
    await userEvent.keyboard('{ArrowUp}');

    expect(hookMocks.save).toHaveBeenCalledWith({ score: 4 }, expect.anything());
  });

  it('Home jumps to 1; End jumps to 10', async () => {
    render(<ScoreWheel date="2026-05-28" initialScore={5} />);
    const wheel = screen.getByRole('listbox', { name: /score/i });
    wheel.focus();

    await userEvent.keyboard('{Home}');
    expect(hookMocks.save).toHaveBeenLastCalledWith({ score: 1 }, expect.anything());

    await userEvent.keyboard('{End}');
    expect(hookMocks.save).toHaveBeenLastCalledWith({ score: 10 }, expect.anything());
  });

  it('keyboard navigation stays in [1..10] bounds', async () => {
    render(<ScoreWheel date="2026-05-28" initialScore={1} />);
    const wheel = screen.getByRole('listbox', { name: /score/i });
    wheel.focus();
    await userEvent.keyboard('{ArrowUp}'); // would go to 0 — should clamp to 1

    // No save fired because clamped value equals current → no-op
    expect(hookMocks.save).not.toHaveBeenCalled();
  });
});
