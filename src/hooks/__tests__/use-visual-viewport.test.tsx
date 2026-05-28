// @vitest-environment jsdom
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, render } from '@testing-library/react';
import { useVisualViewport } from '../use-visual-viewport';

type Snapshot = ReturnType<typeof useVisualViewport>;

function Harness({ onSnapshot }: { onSnapshot: (s: Snapshot) => void }) {
  const snap = useVisualViewport();
  onSnapshot(snap);
  return null;
}

function installVisualViewportMock(
  initial: { offsetTop: number; offsetLeft: number; width: number; height: number },
): {
  listeners: Record<string, EventListener[]>;
  fireResize: (next: Partial<typeof initial>) => void;
  vv: VisualViewport;
} {
  const listeners: Record<string, EventListener[]> = {};
  const state = { ...initial };
  const vv = {
    get offsetTop() {
      return state.offsetTop;
    },
    get offsetLeft() {
      return state.offsetLeft;
    },
    get width() {
      return state.width;
    },
    get height() {
      return state.height;
    },
    addEventListener: (type: string, cb: EventListener) => {
      listeners[type] = listeners[type] ?? [];
      listeners[type]!.push(cb);
    },
    removeEventListener: (type: string, cb: EventListener) => {
      listeners[type] = (listeners[type] ?? []).filter((l) => l !== cb);
    },
  } as unknown as VisualViewport;
  Object.defineProperty(window, 'visualViewport', {
    configurable: true,
    value: vv,
  });
  function fireResize(next: Partial<typeof initial>): void {
    Object.assign(state, next);
    for (const cb of listeners['resize'] ?? []) cb(new Event('resize'));
  }
  return { listeners, fireResize, vv };
}

describe('useVisualViewport', () => {
  beforeEach(() => {
    Object.defineProperty(window, 'innerWidth', { configurable: true, value: 400 });
    Object.defineProperty(window, 'innerHeight', { configurable: true, value: 800 });
  });
  afterEach(() => {
    cleanup();
    delete (window as unknown as Record<string, unknown>).visualViewport;
  });

  it('given visualViewport exists, when the hook mounts, then it returns its current dimensions', () => {
    installVisualViewportMock({ offsetTop: 12, offsetLeft: 0, width: 400, height: 700 });
    const onSnap = vi.fn();
    render(<Harness onSnapshot={onSnap} />);

    const last = onSnap.mock.lastCall![0] as Snapshot;
    expect(last).toEqual({ offsetTop: 12, offsetLeft: 0, width: 400, height: 700 });
  });

  it('given visualViewport fires resize, when the size changes, then the hook re-snapshots', () => {
    const { fireResize } = installVisualViewportMock({
      offsetTop: 0,
      offsetLeft: 0,
      width: 400,
      height: 800,
    });
    const onSnap = vi.fn();
    render(<Harness onSnapshot={onSnap} />);

    act(() => {
      fireResize({ height: 500 }); // simulate iOS keyboard popping up
    });

    const last = onSnap.mock.lastCall![0] as Snapshot;
    expect(last.height).toBe(500);
  });

  it('given visualViewport is undefined, when the hook mounts, then it falls back to window.innerWidth/Height with offsetTop=0', () => {
    delete (window as unknown as Record<string, unknown>).visualViewport;
    const onSnap = vi.fn();
    render(<Harness onSnapshot={onSnap} />);

    const last = onSnap.mock.lastCall![0] as Snapshot;
    expect(last).toEqual({ offsetTop: 0, offsetLeft: 0, width: 400, height: 800 });
  });

  it('given the consumer unmounts, when teardown runs, then resize + scroll listeners are removed', () => {
    const { listeners } = installVisualViewportMock({
      offsetTop: 0,
      offsetLeft: 0,
      width: 400,
      height: 800,
    });
    const { unmount } = render(<Harness onSnapshot={() => {}} />);

    expect((listeners['resize'] ?? []).length).toBeGreaterThan(0);
    unmount();
    expect(listeners['resize']?.length ?? 0).toBe(0);
    expect(listeners['scroll']?.length ?? 0).toBe(0);
  });
});
