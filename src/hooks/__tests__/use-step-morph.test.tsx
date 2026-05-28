// @vitest-environment jsdom
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { useEffect } from 'react';
import { act, cleanup, render } from '@testing-library/react';
import { useStepMorph } from '../use-step-morph';

type Step = 'score' | 'note' | 'tags';
type Snapshot = ReturnType<typeof useStepMorph<Step>>;

function Harness({
  step,
  duration,
  onSnapshot,
}: {
  step: Step;
  duration?: number;
  onSnapshot: (s: Snapshot) => void;
}) {
  const snap = useStepMorph<Step>(step, duration);
  useEffect(() => {
    onSnapshot(snap);
  });
  return null;
}

describe('useStepMorph', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });
  afterEach(() => {
    cleanup();
    vi.useRealTimers();
  });

  it('given initial render, when activeStep matches the rendered step, then phase is "in"', () => {
    const onSnap = vi.fn();
    render(<Harness step="score" onSnapshot={onSnap} />);

    const first = onSnap.mock.calls[0]![0] as Snapshot;
    expect(first).toEqual({ renderedStep: 'score', phase: 'in' });
  });

  it('given activeStep changes, when the change happens, then phase becomes "out" immediately and renderedStep stays on the old value', () => {
    const onSnap = vi.fn();
    const { rerender } = render(<Harness step="score" onSnapshot={onSnap} />);
    onSnap.mockClear();

    rerender(<Harness step="note" onSnapshot={onSnap} />);

    const next = onSnap.mock.lastCall![0] as Snapshot;
    expect(next).toEqual({ renderedStep: 'score', phase: 'out' });
  });

  it('given the timer fires, when durationMs elapses, then renderedStep updates and phase becomes "in"', () => {
    const onSnap = vi.fn();
    const { rerender } = render(<Harness step="score" duration={150} onSnapshot={onSnap} />);
    rerender(<Harness step="note" duration={150} onSnapshot={onSnap} />);
    onSnap.mockClear();

    act(() => {
      vi.advanceTimersByTime(150);
    });

    const last = onSnap.mock.lastCall![0] as Snapshot;
    expect(last).toEqual({ renderedStep: 'note', phase: 'in' });
  });

  it('given rapid step changes, when several happen within one duration, then only the latest step renders after the timer settles', () => {
    const onSnap = vi.fn();
    const { rerender } = render(<Harness step="score" duration={150} onSnapshot={onSnap} />);
    rerender(<Harness step="note" duration={150} onSnapshot={onSnap} />);
    act(() => { vi.advanceTimersByTime(50); });
    rerender(<Harness step="tags" duration={150} onSnapshot={onSnap} />);
    onSnap.mockClear();

    act(() => { vi.advanceTimersByTime(150); });

    const last = onSnap.mock.lastCall![0] as Snapshot;
    expect(last).toEqual({ renderedStep: 'tags', phase: 'in' });
  });

  it('given the consumer unmounts during a pending morph, when timers fire, then no warning fires about setState on unmounted component', () => {
    const warn = vi.spyOn(console, 'error').mockImplementation(() => {});
    const { rerender, unmount } = render(<Harness step="score" duration={150} onSnapshot={() => {}} />);
    rerender(<Harness step="note" duration={150} onSnapshot={() => {}} />);

    unmount();
    act(() => { vi.advanceTimersByTime(200); });

    const setStateWarning = warn.mock.calls.find((c) => /unmounted|update on/i.test(String(c[0])));
    expect(setStateWarning).toBeUndefined();

    warn.mockRestore();
  });
});
