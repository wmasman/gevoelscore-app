// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ScoreRow } from '../score-row';

// Step 4b moved the hook ownership up to <TodayShell>. ScoreRow now
// receives `save` + `status` as props, so tests pass mocks directly —
// no module-level vi.mock of the hook is needed.

type RenderProps = Partial<React.ComponentProps<typeof ScoreRow>>;

function renderRow(props: RenderProps = {}) {
  const saveMock = vi.fn().mockResolvedValue(undefined);
  const utils = render(
    <ScoreRow
      initialScore={null}
      save={(props.save ?? saveMock) as React.ComponentProps<typeof ScoreRow>['save']}
      status="idle"
      {...props}
    />,
  );
  return { saveMock, ...utils };
}

describe('<ScoreRow />', () => {
  beforeEach(() => {
    // jsdom doesn't implement scrollTo; stub so scrollIntoView calls are no-ops.
    Element.prototype.scrollTo = vi.fn() as unknown as Element['scrollTo'];
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
    const { saveMock } = renderRow();

    await user.click(screen.getByRole('option', { name: '7' }));

    expect(saveMock).toHaveBeenCalledOnce();
    expect(saveMock).toHaveBeenCalledWith({ score: 7 }, expect.objectContaining({ flush: true }));

    const row = screen.getByRole('listbox', { name: /score/i });
    expect(row).toHaveAttribute('data-phase', 'set');
    const selected = within(row).getByRole('option', { selected: true });
    expect(selected).toHaveTextContent('7');
  });

  it('tap on already-set value is a no-op', async () => {
    const user = userEvent.setup();
    const { saveMock } = renderRow({ initialScore: 7 });

    await user.click(screen.getByRole('option', { name: '7' }));

    expect(saveMock).not.toHaveBeenCalled();
  });

  it('tap on a different value on a set row: fires save WITHOUT flush (debounced)', async () => {
    const user = userEvent.setup();
    const { saveMock } = renderRow({ initialScore: 7 });

    await user.click(screen.getByRole('option', { name: '4' }));

    expect(saveMock).toHaveBeenCalledOnce();
    const args = saveMock.mock.calls[0]!;
    expect(args[0]).toEqual({ score: 4 });
    expect(args[1]?.flush ?? false).toBe(false);
  });

  it('ArrowRight moves centred toward 10 and saves (primary axis)', async () => {
    const { saveMock } = renderRow();
    const row = screen.getByRole('listbox', { name: /score/i });
    row.focus();
    await userEvent.keyboard('{ArrowRight}');

    expect(saveMock).toHaveBeenCalledWith({ score: 6 }, expect.objectContaining({ flush: true }));
  });

  it('ArrowLeft moves centred toward 1 and saves (primary axis)', async () => {
    const { saveMock } = renderRow({ initialScore: 5 });
    const row = screen.getByRole('listbox', { name: /score/i });
    row.focus();
    await userEvent.keyboard('{ArrowLeft}');

    expect(saveMock).toHaveBeenCalledWith({ score: 4 }, expect.anything());
  });

  it('ArrowDown is preserved as alias (Step 4 muscle memory + hardware keyboards)', async () => {
    const { saveMock } = renderRow();
    const row = screen.getByRole('listbox', { name: /score/i });
    row.focus();
    await userEvent.keyboard('{ArrowDown}');

    expect(saveMock).toHaveBeenCalledWith({ score: 6 }, expect.objectContaining({ flush: true }));
  });

  it('ArrowUp is preserved as alias', async () => {
    const { saveMock } = renderRow({ initialScore: 5 });
    const row = screen.getByRole('listbox', { name: /score/i });
    row.focus();
    await userEvent.keyboard('{ArrowUp}');

    expect(saveMock).toHaveBeenCalledWith({ score: 4 }, expect.anything());
  });

  it('Home jumps to 1; End jumps to 10', async () => {
    const { saveMock } = renderRow({ initialScore: 5 });
    const row = screen.getByRole('listbox', { name: /score/i });
    row.focus();

    await userEvent.keyboard('{Home}');
    expect(saveMock).toHaveBeenLastCalledWith({ score: 1 }, expect.anything());

    await userEvent.keyboard('{End}');
    expect(saveMock).toHaveBeenLastCalledWith({ score: 10 }, expect.anything());
  });

  it('keyboard navigation stays in [1..10] bounds', async () => {
    const { saveMock } = renderRow({ initialScore: 1 });
    const row = screen.getByRole('listbox', { name: /score/i });
    row.focus();
    await userEvent.keyboard('{ArrowLeft}'); // would go to 0 — should clamp to 1

    expect(saveMock).not.toHaveBeenCalled();
  });
});
