// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ScoreCircle } from '../score-circle';

beforeEach(() => {
  // jsdom doesn't implement Pointer-capture APIs — stub so the handlers
  // don't throw. Identical pattern to BottomSheet's test setup.
  if (!Element.prototype.hasPointerCapture) {
    Element.prototype.hasPointerCapture = vi.fn().mockReturnValue(true);
  }
  if (!Element.prototype.setPointerCapture) {
    Element.prototype.setPointerCapture = vi.fn();
  }
  if (!Element.prototype.releasePointerCapture) {
    Element.prototype.releasePointerCapture = vi.fn();
  }
});
afterEach(cleanup);

describe('<ScoreCircle />', () => {
  it('given initialValue=5, when rendered, then the centre shows "5" and aria-valuenow is "5"', () => {
    const { getByRole, getByText } = render(
      <ScoreCircle initialValue={5} onCommit={() => {}} ariaLabel="Score" />,
    );
    const slider = getByRole('slider', { name: 'Score' });
    expect(slider).toHaveAttribute('aria-valuemin', '1');
    expect(slider).toHaveAttribute('aria-valuemax', '10');
    expect(slider).toHaveAttribute('aria-valuenow', '5');
    expect(getByText('5')).toBeInTheDocument();
  });

  it('given a pointer drag of 20px right, when released, then onCommit fires with initialValue + 1', () => {
    const onCommit = vi.fn();
    const { getByRole } = render(
      <ScoreCircle initialValue={5} onCommit={onCommit} ariaLabel="Score" />,
    );
    const slider = getByRole('slider');
    fireEvent.pointerDown(slider, { clientX: 100, pointerId: 1 });
    fireEvent.pointerMove(slider, { clientX: 120, pointerId: 1 });
    fireEvent.pointerUp(slider, { clientX: 120, pointerId: 1 });
    expect(onCommit).toHaveBeenCalledTimes(1);
    expect(onCommit).toHaveBeenCalledWith(6);
  });

  it('given a rapid drag of 80px right, when released, then onCommit fires once with initialValue + 4 (no intermediate commits)', () => {
    const onCommit = vi.fn();
    const { getByRole } = render(
      <ScoreCircle initialValue={5} onCommit={onCommit} ariaLabel="Score" />,
    );
    const slider = getByRole('slider');
    fireEvent.pointerDown(slider, { clientX: 100, pointerId: 1 });
    fireEvent.pointerMove(slider, { clientX: 140, pointerId: 1 });
    fireEvent.pointerMove(slider, { clientX: 180, pointerId: 1 });
    fireEvent.pointerUp(slider, { clientX: 180, pointerId: 1 });
    expect(onCommit).toHaveBeenCalledTimes(1);
    expect(onCommit).toHaveBeenCalledWith(9);
  });

  it('given a drag that would overshoot 10, when released, then the committed value is clamped to 10', () => {
    const onCommit = vi.fn();
    const { getByRole } = render(
      <ScoreCircle initialValue={5} onCommit={onCommit} ariaLabel="Score" />,
    );
    const slider = getByRole('slider');
    fireEvent.pointerDown(slider, { clientX: 100, pointerId: 1 });
    fireEvent.pointerMove(slider, { clientX: 500, pointerId: 1 }); // 400px right = +20 raw
    fireEvent.pointerUp(slider, { clientX: 500, pointerId: 1 });
    expect(onCommit).toHaveBeenCalledWith(10);
  });

  it('given a drag that would undershoot 1, when released, then the committed value is clamped to 1', () => {
    const onCommit = vi.fn();
    const { getByRole } = render(
      <ScoreCircle initialValue={5} onCommit={onCommit} ariaLabel="Score" />,
    );
    const slider = getByRole('slider');
    fireEvent.pointerDown(slider, { clientX: 100, pointerId: 1 });
    fireEvent.pointerMove(slider, { clientX: -500, pointerId: 1 });
    fireEvent.pointerUp(slider, { clientX: -500, pointerId: 1 });
    expect(onCommit).toHaveBeenCalledWith(1);
  });

  it('given an integer-cross during drag, when crossed, then the number element gets a pulse class that is removed after PULSE_MS', () => {
    vi.useFakeTimers();
    try {
      const { getByRole, getByTestId } = render(
        <ScoreCircle initialValue={5} onCommit={() => {}} ariaLabel="Score" />,
      );
      const slider = getByRole('slider');
      fireEvent.pointerDown(slider, { clientX: 100, pointerId: 1 });
      fireEvent.pointerMove(slider, { clientX: 120, pointerId: 1 });

      const numberEl = getByTestId('score-number');
      expect(numberEl.getAttribute('data-pulsing')).toBe('true');

      act(() => {
        vi.advanceTimersByTime(80);
      });
      expect(numberEl.getAttribute('data-pulsing')).toBe('false');
    } finally {
      vi.useRealTimers();
    }
  });

  it('given the ArrowRight key is pressed, when handled, then onCommit fires with currentValue + 1', async () => {
    const onCommit = vi.fn();
    const user = userEvent.setup();
    const { getByRole } = render(
      <ScoreCircle initialValue={5} onCommit={onCommit} ariaLabel="Score" />,
    );
    const slider = getByRole('slider');
    slider.focus();
    await user.keyboard('{ArrowRight}');
    expect(onCommit).toHaveBeenCalledWith(6);
  });

  it('given the ArrowLeft / ArrowUp / ArrowDown keys, when pressed, then onCommit fires with the expected delta', async () => {
    const onCommit = vi.fn();
    const user = userEvent.setup();
    const { getByRole } = render(
      <ScoreCircle initialValue={5} onCommit={onCommit} ariaLabel="Score" />,
    );
    const slider = getByRole('slider');
    slider.focus();
    await user.keyboard('{ArrowLeft}');
    expect(onCommit).toHaveBeenLastCalledWith(4);
    await user.keyboard('{ArrowUp}');
    expect(onCommit).toHaveBeenLastCalledWith(5);
    await user.keyboard('{ArrowDown}');
    expect(onCommit).toHaveBeenLastCalledWith(4);
  });

  it('given the Home / End keys, when pressed, then onCommit fires with 1 / 10', async () => {
    const onCommit = vi.fn();
    const user = userEvent.setup();
    const { getByRole } = render(
      <ScoreCircle initialValue={5} onCommit={onCommit} ariaLabel="Score" />,
    );
    const slider = getByRole('slider');
    slider.focus();
    await user.keyboard('{Home}');
    expect(onCommit).toHaveBeenLastCalledWith(1);
    await user.keyboard('{End}');
    expect(onCommit).toHaveBeenLastCalledWith(10);
  });

  it('given the component unmounts during a pending pulse, when timers fire, then no warning about setState on unmounted', () => {
    vi.useFakeTimers();
    const warn = vi.spyOn(console, 'error').mockImplementation(() => {});
    try {
      const { getByRole, unmount } = render(
        <ScoreCircle initialValue={5} onCommit={() => {}} ariaLabel="Score" />,
      );
      const slider = getByRole('slider');
      fireEvent.pointerDown(slider, { clientX: 100, pointerId: 1 });
      fireEvent.pointerMove(slider, { clientX: 120, pointerId: 1 });
      unmount();
      act(() => {
        vi.advanceTimersByTime(200);
      });
      const setStateWarning = warn.mock.calls.find((c) =>
        /unmounted|update on/i.test(String(c[0])),
      );
      expect(setStateWarning).toBeUndefined();
    } finally {
      warn.mockRestore();
      vi.useRealTimers();
    }
  });
});
